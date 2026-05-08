from __future__ import annotations

from typing import Any

from chanta_core.agents.default_agent import load_default_agent_profile
from chanta_core.runtime.execution_context import ExecutionContext
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_llm_chat_skill() -> Skill:
    return Skill(
        skill_id="skill:llm_chat",
        skill_name="llm_chat",
        description=(
            "Use the configured local or remote LLM provider to answer the "
            "user request."
        ),
        execution_type="llm",
        input_schema={},
        output_schema={},
        tags=["llm", "chat", "default"],
        skill_attrs={
            "is_builtin": True,
            "provider_mode": "configured",
        },
    )


def execute_llm_chat_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    llm_client: Any,
    context_assembler: Any,
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
    provided_messages = context.context_attrs.get("prompt_messages")
    if provided_messages:
        messages = _sanitize_prompt_messages(provided_messages)
    else:
        messages = context_assembler.assemble_for_llm_chat(
            user_input=context.user_input,
            system_prompt=context.system_prompt,
            pig_context=context.pig_context or context.context_attrs.get("pig_context"),
            context_budget=context.context_attrs.get("context_budget"),
            compaction_pipeline=context.context_attrs.get("compaction_pipeline"),
            context_snapshot_policy=context.context_attrs.get("context_snapshot_policy"),
            context_snapshot_store=context.context_attrs.get("context_snapshot_store"),
            context_audit_service=context.context_attrs.get("context_audit_service"),
            session_id=context.session_id,
            process_instance_id=context.process_instance_id,
        )
    iteration = int(context.context_attrs.get("iteration", 0))
    trace_service.record_context_assembled(
        execution_context,
        messages,
        profile=profile,
        iteration=iteration,
    )

    provider_name = getattr(getattr(llm_client, "settings", None), "provider", None)
    model_id = getattr(getattr(llm_client, "settings", None), "model", None)
    trace_service.record_llm_call_started(
        execution_context,
        messages,
        provider_name=provider_name,
        model_id=model_id,
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
                "exception_type": type(error).__name__,
                "failure_stage": "call_llm",
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
            "execution_type": "llm",
            "response_length": len(response_text),
        },
    )


def _sanitize_prompt_messages(raw_messages: Any) -> list[dict[str, str]]:
    messages: list[dict[str, str]] = []
    if not isinstance(raw_messages, list):
        return messages
    for item in raw_messages:
        if not isinstance(item, dict):
            continue
        role = str(item.get("role") or "")
        content = str(item.get("content") or "")
        if role in {"system", "user", "assistant", "tool"} and content:
            messages.append({"role": role, "content": content})
    return messages
