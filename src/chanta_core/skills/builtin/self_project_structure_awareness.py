from __future__ import annotations

from pathlib import Path

from chanta_core.self_awareness.project_structure_awareness import (
    PROJECT_STRUCTURE_EFFECTS,
    SelfProjectStructureAwarenessSkillService,
    SelfProjectStructureRequest,
)
from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_project_structure_skill() -> Skill:
    return Skill(
        skill_id="skill:self_awareness_project_structure",
        skill_name="self_awareness_project_structure",
        description="Create a deterministic metadata-only project surface structure candidate.",
        execution_type="builtin",
        input_schema={
            "root_path": "str",
            "relative_path": "str",
            "max_depth": "int",
            "max_entries": "int",
            "include_hidden": "bool",
            "include_ignored": "bool",
            "include_summary_candidates": "bool",
        },
        output_schema={"candidate": "SelfProjectStructureCandidate"},
        tags=[
            "self_awareness",
            "workspace",
            "project_structure",
            "surface_mapping",
            "candidate_only",
            "read_only",
            "explicit",
        ],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "effect_types": list(PROJECT_STRUCTURE_EFFECTS),
            "metadata_only_tree": True,
            "deterministic_surface_mapping": True,
            "canonical_promotion_enabled": False,
        },
    )


def execute_self_awareness_project_structure_skill(
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
        service = SelfProjectStructureAwarenessSkillService(path_policy_service=path_policy)
        candidate = service.inspect_project_structure(
            SelfProjectStructureRequest(
                root_id=context.context_attrs.get("root_id"),
                relative_path=str(context.context_attrs.get("relative_path") or context.context_attrs.get("path") or "."),
                max_depth=int(context.context_attrs.get("max_depth", 5)),
                max_entries=int(context.context_attrs.get("max_entries", 2000)),
                include_hidden=bool(context.context_attrs.get("include_hidden", False)),
                include_ignored=bool(context.context_attrs.get("include_ignored", False)),
                include_summary_candidates=bool(context.context_attrs.get("include_summary_candidates", True)),
                include_candidate_surfaces=bool(context.context_attrs.get("include_candidate_surfaces", True)),
            )
        )
        output = candidate.to_dict()
        blocked = bool(candidate.policy_decision and candidate.policy_decision.blocked)
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not blocked,
            output_text=None,
            output_attrs={
                "execution_type": skill.execution_type,
                "effect_type": READ_ONLY_OBSERVATION_EFFECT,
                "effect_types": list(PROJECT_STRUCTURE_EFFECTS),
                **output,
            },
            error=None if not blocked else candidate.policy_decision.reason,
        )
    except Exception as error:
        return _failure(skill, error)


def _required(context: SkillExecutionContext, key: str) -> str:
    value = context.context_attrs.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"{key} is required for self-project structure awareness")
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
            "effect_types": list(PROJECT_STRUCTURE_EFFECTS),
            "exception_type": type(error).__name__,
            "read_only": True,
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
