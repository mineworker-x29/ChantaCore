from __future__ import annotations

from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_summarize_pi_artifacts_skill() -> Skill:
    return Skill(
        skill_id="skill:summarize_pi_artifacts",
        skill_name="summarize_pi_artifacts",
        description="Summarize recent advisory PIG PI artifacts.",
        execution_type="builtin_process_intelligence",
        input_schema={},
        output_schema={},
        tags=["builtin", "pig", "pi-artifact", "readonly"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_pig": True,
        },
    )


def execute_summarize_pi_artifacts_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    **_,
) -> SkillExecutionResult:
    store_path = context.context_attrs.get("pi_artifact_store_path")
    limit = int(context.context_attrs.get("limit", 20))
    store = PIArtifactStore(store_path) if store_path else PIArtifactStore()
    artifacts = store.recent(limit=limit)
    artifact_types: dict[str, int] = {}
    for artifact in artifacts:
        artifact_types[artifact.artifact_type] = (
            artifact_types.get(artifact.artifact_type, 0) + 1
        )
    recent_titles = [artifact.title for artifact in artifacts[-5:]]
    if artifacts:
        output_text = (
            f"PI artifact summary: {len(artifacts)} artifacts, "
            f"{len(artifact_types)} artifact types."
        )
    else:
        output_text = "PI artifact summary: 0 artifacts."
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=output_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "artifact_count": len(artifacts),
            "artifact_types": artifact_types,
            "recent_titles": recent_titles,
            "store_warnings": store.warnings,
        },
    )
