from __future__ import annotations

from chanta_core.self_awareness.self_directed_intention import (
    INTENTION_CANDIDATE_EFFECTS,
    SelfDirectedIntentionRequest,
    SelfDirectedIntentionSkillService,
)
from chanta_core.self_awareness.workspace_awareness import READ_ONLY_OBSERVATION_EFFECT
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_plan_candidate_skill() -> Skill:
    return _candidate_skill(
        "skill:self_awareness_plan_candidate",
        "self_awareness_plan_candidate",
        "Create candidate-only self-directed plan intentions from verified self-awareness sources.",
        {"bundle": "SelfDirectedIntentionCandidateBundle"},
    )


def create_self_awareness_todo_candidate_skill() -> Skill:
    return _candidate_skill(
        "skill:self_awareness_todo_candidate",
        "self_awareness_todo_candidate",
        "Create candidate-only self-directed todo intentions from verified self-awareness sources.",
        {"bundle": "SelfDirectedIntentionCandidateBundle"},
    )


def execute_self_awareness_intention_candidate_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        request = SelfDirectedIntentionRequest(
            goal_text=context.context_attrs.get("goal_text"),
            root_id=context.context_attrs.get("root_id"),
            source_candidate_ids=_string_list(context.context_attrs.get("source_candidate_ids")),
            source_report_ids=_string_list(context.context_attrs.get("source_report_ids")),
            target_scope=str(context.context_attrs.get("target_scope") or "self_awareness"),
            candidate_types=_string_list(
                context.context_attrs.get("candidate_types"),
                default=["plan", "todo", "no_action", "needs_more_input"],
            ),
            strictness=str(context.context_attrs.get("strictness") or "standard"),
            max_plan_steps=int(context.context_attrs.get("max_plan_steps") or 8),
            max_todo_items=int(context.context_attrs.get("max_todo_items") or 12),
            include_no_action=bool(context.context_attrs.get("include_no_action", True)),
            include_needs_more_input=bool(context.context_attrs.get("include_needs_more_input", True)),
        )
        service = SelfDirectedIntentionSkillService()
        bundle = (
            service.create_todo_candidate(request)
            if skill.skill_id == "skill:self_awareness_todo_candidate"
            else service.create_plan_candidate(request)
        )
        output = bundle.to_dict()
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=True,
            output_text=None,
            output_attrs={
                "execution_type": skill.execution_type,
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                "effect_types": list(INTENTION_CANDIDATE_EFFECTS),
                **output,
            },
            error=None,
        )
    except Exception as error:
        return _failure(skill, error)


def _candidate_skill(
    skill_id: str,
    skill_name: str,
    description: str,
    output_schema: dict[str, str],
) -> Skill:
    return Skill(
        skill_id=skill_id,
        skill_name=skill_name,
        description=description,
        execution_type="builtin",
        input_schema={
            "goal_text": "str",
            "source_candidate_ids": "list[str]",
            "source_report_ids": "list[str]",
            "strictness": "str",
            "candidate_types": "list[str]",
        },
        output_schema=output_schema,
        tags=[
            "self_awareness",
            "intention_candidate",
            "candidate_only",
            "read_only",
            "explicit",
        ],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "effect_types": list(INTENTION_CANDIDATE_EFFECTS),
            "candidate_only": True,
            "execution_enabled": False,
            "materialized": False,
            "canonical_promotion_enabled": False,
            "promoted": False,
            "mutates_workspace": False,
            "mutates_memory": False,
            "mutates_persona": False,
            "mutates_overlay": False,
            "uses_shell": False,
            "uses_network": False,
            "uses_mcp": False,
            "loads_plugin": False,
            "executes_external_harness": False,
            "dangerous_capability": False,
        },
    )


def _string_list(value: object, *, default: list[str] | None = None) -> list[str]:
    if value is None:
        return list(default or [])
    if isinstance(value, list):
        return [str(item) for item in value if str(item)]
    text = str(value).strip()
    if not text:
        return list(default or [])
    return [item.strip() for item in text.split(",") if item.strip()]


def _failure(skill: Skill, error: Exception) -> SkillExecutionResult:
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=False,
        output_text=None,
        output_attrs={
            "execution_type": skill.execution_type,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "effect_types": list(INTENTION_CANDIDATE_EFFECTS),
            "exception_type": type(error).__name__,
            "read_only": True,
            "policy_gated": True,
            "execution_enabled": False,
            "materialized": False,
            "canonical_promotion_enabled": False,
            "promoted": False,
            "workspace_write_used": False,
            "shell_execution_used": False,
            "network_access_used": False,
            "mcp_connection_used": False,
            "plugin_loading_used": False,
            "external_harness_execution_used": False,
        },
        error=str(error),
    )
