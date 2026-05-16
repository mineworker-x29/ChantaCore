from __future__ import annotations

from pathlib import Path

from chanta_core.self_awareness.code_search_awareness import (
    SelfCodeSearchAwarenessSkillService,
    SelfWorkspaceSearchRequest,
)
from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_workspace_search_skill() -> Skill:
    return Skill(
        skill_id="skill:self_awareness_workspace_search",
        skill_name="self_awareness_workspace_search",
        description="Search bounded, policy-gated, redacted literal text slices inside the workspace.",
        execution_type="builtin",
        input_schema={
            "root_path": "str",
            "query": "str",
            "relative_path": "str",
            "include_globs": "list[str]",
            "exclude_globs": "list[str]",
            "case_sensitive": "bool",
            "match_mode": "str",
            "context_lines": "int",
            "max_files": "int",
            "max_matches": "int",
            "max_matches_per_file": "int",
            "max_bytes_per_file": "int",
            "max_total_bytes": "int",
            "include_hidden": "bool",
        },
        output_schema={"result": "SelfWorkspaceSearchResult"},
        tags=["self_awareness", "workspace", "search", "literal", "bounded", "redacted", "read_only", "explicit"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "bounded_search": True,
            "literal_match_only": True,
            "redaction_enabled": True,
        },
    )


def execute_self_awareness_workspace_search_skill(
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
        service = SelfCodeSearchAwarenessSkillService(path_policy_service=path_policy)
        result = service.search_workspace(
            SelfWorkspaceSearchRequest(
                query=str(context.context_attrs.get("query") or ""),
                root_id=context.context_attrs.get("root_id"),
                relative_path=str(context.context_attrs.get("relative_path") or "."),
                include_globs=_list_value(context.context_attrs.get("include_globs")),
                exclude_globs=_list_value(context.context_attrs.get("exclude_globs")),
                case_sensitive=bool(context.context_attrs.get("case_sensitive", False)),
                match_mode=str(context.context_attrs.get("match_mode") or "literal"),
                context_lines=int(context.context_attrs.get("context_lines", 2)),
                max_files=int(context.context_attrs.get("max_files", 200)),
                max_matches=int(context.context_attrs.get("max_matches", 200)),
                max_matches_per_file=int(context.context_attrs.get("max_matches_per_file", 20)),
                max_bytes_per_file=int(context.context_attrs.get("max_bytes_per_file", 65536)),
                max_total_bytes=int(context.context_attrs.get("max_total_bytes", 1048576)),
                include_hidden=bool(context.context_attrs.get("include_hidden", False)),
            )
        )
        result_dict = result.to_dict()
        return SkillExecutionResult(
            skill_id=skill.skill_id,
            skill_name=skill.skill_name,
            success=not result.blocked,
            output_text=None,
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
        raise ValueError(f"{key} is required for self-code search awareness skills")
    return str(Path(str(value)) if key == "root_path" else value)


def _list_value(value: object) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


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
            "bounded_search": True,
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
