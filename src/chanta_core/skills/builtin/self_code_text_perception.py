from __future__ import annotations

from pathlib import Path

from chanta_core.self_awareness.code_text_perception import (
    SelfCodeTextPerceptionSkillService,
    SelfTextReadRequest,
)
from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_text_read_skill() -> Skill:
    return Skill(
        skill_id="skill:self_awareness_text_read",
        skill_name="self_awareness_text_read",
        description="Read a bounded, policy-gated, redacted text slice under an explicit workspace root.",
        execution_type="builtin",
        input_schema={
            "root_path": "str",
            "path": "str",
            "mode": "str",
            "start_line": "int",
            "end_line": "int",
            "max_bytes": "int",
            "max_lines": "int",
        },
        output_schema={"result": "SelfTextReadResult"},
        tags=["self_awareness", "workspace", "text", "bounded", "redacted", "read_only", "explicit"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "bounded_read": True,
            "redaction_enabled": True,
        },
    )


def execute_self_awareness_text_read_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        root_path = _required(context, "root_path")
        path_value = _required(context, "path")
        path_policy = SelfWorkspacePathPolicyService(workspace_root=root_path)
        service = SelfCodeTextPerceptionSkillService(path_policy_service=path_policy)
        result = service.read_text(
            SelfTextReadRequest(
                path=path_value,
                root_id=context.context_attrs.get("root_id"),
                mode=str(context.context_attrs.get("mode") or "preview"),
                start_line=_optional_int(context.context_attrs.get("start_line")),
                end_line=_optional_int(context.context_attrs.get("end_line")),
                max_bytes=int(context.context_attrs.get("max_bytes", 16384)),
                max_lines=int(context.context_attrs.get("max_lines", 300)),
                allow_redacted_secret_preview=bool(
                    context.context_attrs.get("allow_redacted_secret_preview", False)
                ),
            )
        )
        result_dict = result.to_dict()
        text_slice = result_dict.get("slice") or {}
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not result.blocked,
            output_text=None if result.blocked else str(text_slice.get("content", "")),
            output_attrs={
                "execution_type": skill.execution_type,
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                **result_dict,
            },
            error=None if not result.blocked else result.policy_decision.reason,
        )
    except Exception as error:
        return _failure(skill, error)


def _required(context: SkillExecutionContext, key: str) -> str:
    value = context.context_attrs.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"{key} is required for self-code/text perception skills")
    return str(Path(str(value)) if key == "root_path" else value)


def _optional_int(value: object) -> int | None:
    if value is None or str(value) == "":
        return None
    return int(value)


def _failure(skill: Skill, error: Exception) -> SkillExecutionResult:
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=False,
        output_text=None,
        output_attrs={
            "execution_type": skill.execution_type,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "exception_type": type(error).__name__,
            "read_only": True,
            "bounded_read": True,
            "policy_gated": True,
            "workspace_write_used": False,
            "shell_execution_used": False,
            "network_access_used": False,
            "mcp_connection_used": False,
            "plugin_loading_used": False,
            "external_harness_execution_used": False,
        },
        error=str(error),
    )
