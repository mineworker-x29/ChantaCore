from __future__ import annotations

from pathlib import Path

from chanta_core.self_awareness.structure_summarization import (
    SelfStructureSummarizationSkillService,
    SelfStructureSummaryRequest,
    STRUCTURE_SUMMARY_EFFECTS,
)
from chanta_core.self_awareness.workspace_awareness import (
    READ_ONLY_OBSERVATION_EFFECT,
    SelfWorkspacePathPolicyService,
)
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_self_awareness_markdown_structure_skill() -> Skill:
    return _create_structure_skill(
        skill_id="skill:self_awareness_markdown_structure",
        skill_name="self_awareness_markdown_structure",
        description="Create a deterministic markdown structure summary candidate from an allowed workspace file.",
        summary_mode="markdown",
    )


def create_self_awareness_python_symbols_skill() -> Skill:
    return _create_structure_skill(
        skill_id="skill:self_awareness_python_symbols",
        skill_name="self_awareness_python_symbols",
        description="Create a deterministic top-level Python symbol summary candidate from an allowed workspace file.",
        summary_mode="python",
    )


def execute_self_awareness_structure_summary_skill(
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
        service = SelfStructureSummarizationSkillService(path_policy_service=path_policy)
        mode = str(context.context_attrs.get("summary_mode") or _mode_for_skill(skill.skill_id))
        candidate = service.summarize(
            SelfStructureSummaryRequest(
                path=_required(context, "path"),
                root_id=context.context_attrs.get("root_id"),
                summary_mode=mode,
                max_bytes=int(context.context_attrs.get("max_bytes", 65536)),
                max_lines=int(context.context_attrs.get("max_lines", 1000)),
                include_private_sections=bool(context.context_attrs.get("include_private_sections", False)),
                include_body_preview=bool(context.context_attrs.get("include_body_preview", False)),
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
                "effect_types": list(STRUCTURE_SUMMARY_EFFECTS),
                **output,
            },
            error=None if not blocked else candidate.policy_decision.reason,
        )
    except Exception as error:
        return _failure(skill, error)


def _create_structure_skill(*, skill_id: str, skill_name: str, description: str, summary_mode: str) -> Skill:
    return Skill(
        skill_id=skill_id,
        skill_name=skill_name,
        description=description,
        execution_type="builtin",
        input_schema={
            "root_path": "str",
            "path": "str",
            "summary_mode": "str",
            "max_bytes": "int",
            "max_lines": "int",
        },
        output_schema={"candidate": "SelfStructureSummaryCandidate"},
        tags=["self_awareness", "workspace", "structure", summary_mode, "candidate_only", "read_only", "explicit"],
        skill_attrs={
            "is_builtin": True,
            "read_only": True,
            "ambient_access": False,
            "effect_type": READ_ONLY_OBSERVATION_EFFECT,
            "effect_types": list(STRUCTURE_SUMMARY_EFFECTS),
            "summary_mode": summary_mode,
            "deterministic_structure_extraction": True,
            "canonical_promotion_enabled": False,
        },
    )


def _mode_for_skill(skill_id: str) -> str:
    if skill_id == "skill:self_awareness_python_symbols":
        return "python"
    return "markdown"


def _required(context: SkillExecutionContext, key: str) -> str:
    value = context.context_attrs.get(key)
    if value is None or str(value) == "":
        raise ValueError(f"{key} is required for self-structure summarization skills")
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
            "effect_types": list(STRUCTURE_SUMMARY_EFFECTS),
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
