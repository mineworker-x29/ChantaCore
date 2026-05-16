from __future__ import annotations

from pathlib import Path

from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspaceAwarenessSkillService,
    SelfWorkspacePathPolicyService,
    WorkspaceInventoryRequest,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_workspace_inventory_skill() -> Skill:
    return Skill(
        skill_id="skill:self_awareness_workspace_inventory",
        skill_name="self_awareness_workspace_inventory",
        description="Build a metadata-only inventory under an explicit workspace root.",
        execution_type="builtin",
        input_schema={
            "root_path": "str",
            "relative_path": "str",
            "max_depth": "int",
            "max_entries": "int",
        },
        output_schema={"report": "WorkspaceInventoryReport"},
        tags=["self_awareness", "workspace", "metadata_only", "read_only", "explicit"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "file_content_read": False,
        },
    )


def create_self_awareness_path_verify_skill() -> Skill:
    return Skill(
        skill_id="skill:self_awareness_path_verify",
        skill_name="self_awareness_path_verify",
        description="Verify whether a path stays inside an explicit workspace root.",
        execution_type="builtin",
        input_schema={"root_path": "str", "input_path": "str"},
        output_schema={"resolution": "WorkspacePathResolution"},
        tags=["self_awareness", "workspace", "path_policy", "read_only", "explicit"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "file_content_read": False,
        },
    )


def execute_self_awareness_workspace_inventory_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        root_path = _required(context, "root_path")
        path_policy = SelfWorkspacePathPolicyService(workspace_root=root_path)
        service = SelfWorkspaceAwarenessSkillService(path_policy_service=path_policy)
        report = service.inventory_workspace(
            WorkspaceInventoryRequest(
                root_id=context.context_attrs.get("root_id"),
                relative_path=str(context.context_attrs.get("relative_path") or context.context_attrs.get("input_path") or "."),
                max_depth=int(context.context_attrs.get("max_depth", 3)),
                max_entries=int(context.context_attrs.get("max_entries", 500)),
                include_hidden=bool(context.context_attrs.get("include_hidden", False)),
                include_ignored=bool(context.context_attrs.get("include_ignored", False)),
                include_files=bool(context.context_attrs.get("include_files", True)),
                include_dirs=bool(context.context_attrs.get("include_dirs", True)),
            )
        )
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=report.blocked_count == 0,
            output_text=f"{report.total_entries_returned} metadata entries",
            output_attrs={
                "execution_type": skill.execution_type,
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                **report.to_dict(),
            },
            error=None if report.blocked_count == 0 else "Workspace inventory blocked by policy",
        )
    except Exception as error:
        return _failure(skill, error)


def execute_self_awareness_path_verify_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    trace_service=None,
    ocel_store=None,
    **_,
) -> SkillExecutionResult:
    try:
        root_path = _required(context, "root_path")
        input_path = _required(context, "input_path")
        path_policy = SelfWorkspacePathPolicyService(workspace_root=root_path)
        service = SelfWorkspaceAwarenessSkillService(path_policy_service=path_policy)
        resolution = service.verify_path(input_path, root_id=context.context_attrs.get("root_id"))
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not resolution.blocked,
            output_text=resolution.reason,
            output_attrs={
                "execution_type": skill.execution_type,
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                **resolution.to_dict(),
            },
            error=None if not resolution.blocked else resolution.reason,
        )
    except Exception as error:
        return _failure(skill, error)


def _required(context: SkillExecutionContext, key: str) -> str:
    value = context.context_attrs.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"{key} is required for self-workspace awareness skills")
    return str(Path(str(value)) if key == "root_path" else value)


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
            "workspace_write_used": False,
            "shell_execution_used": False,
            "network_access_used": False,
            "file_content_read": False,
        },
        error=str(error),
    )
