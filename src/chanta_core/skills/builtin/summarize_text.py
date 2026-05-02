from __future__ import annotations

from typing import Any

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_summarize_text_skill() -> Skill:
    return Skill(
        skill_id="skill:summarize_text",
        skill_name="summarize_text",
        description="Summarize input text using the configured LLM provider.",
        execution_type="llm",
        input_schema={},
        output_schema={},
        tags=["llm", "summarization", "builtin"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": True,
            "requires_external_tool": False,
        },
    )


def execute_summarize_text_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    llm_client: Any,
    trace_service: Any,
    **_,
) -> SkillExecutionResult:
    profile = context.context_attrs.get("agent_profile") or load_default_agent_profile()
    execution_context = ExecutionContext.create(
        agent_id=context.agent_id,
        user_input=context.user_input,
        session_id=context.session_id,
        metadata={"process_instance_id": context.process_instance_id},
    )
    messages = [
        {
            "role": "system",
            "content": (
                "Summarize the user's text concisely. Preserve key facts and "
                "avoid adding unsupported claims."
            ),
        },
        {"role": "user", "content": context.user_input},
    ]
    trace_service.record_llm_call_started(
        execution_context,
        messages,
        provider_name=getattr(getattr(llm_client, "settings", None), "provider", None),
        model_id=getattr(getattr(llm_client, "settings", None), "model", None),
        profile=profile,
    )
    try:
        response_text = llm_client.chat_messages(
            messages=messages,
            temperature=float(context.context_attrs.get("temperature", profile.default_temperature)),
            max_tokens=int(context.context_attrs.get("max_tokens", profile.max_tokens)),
        )
    except Exception as error:
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=False,
            output_text=None,
            output_attrs={
                "execution_type": skill.execution_type,
                "summary_mode": "builtin_summarize_text",
                "input_length": len(context.user_input),
                "failure_stage": "call_llm",
                "exception_type": type(error).__name__,
                "skill_id": skill.skill_id,
                "skill_name": skill.skill_name,
            },
            error=str(error),
        )

    trace_service.record_llm_response_received(
        execution_context,
        response_text,
        profile=profile,
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=response_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "summary_mode": "builtin_summarize_text",
            "input_length": len(context.user_input),
            "response_length": len(response_text),
        },
    )
