from __future__ import annotations

from chanta_core.pig.artifact_store import PIArtifactStore
from chanta_core.pig.assimilation import HumanPIAssimilator
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_ingest_human_pi_skill() -> Skill:
    return Skill(
        skill_id="skill:ingest_human_pi",
        skill_name="ingest_human_pi",
        description="Assimilate human process intelligence text as advisory PIG artifact.",
        execution_type="builtin_process_intelligence",
        input_schema={},
        output_schema={},
        tags=["builtin", "pig", "human-pi", "assimilation"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_pig": True,
        },
    )


def execute_ingest_human_pi_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    **_,
) -> SkillExecutionResult:
    store_path = context.context_attrs.get("pi_artifact_store_path")
    store = PIArtifactStore(store_path) if store_path else PIArtifactStore()
    artifact = HumanPIAssimilator(store=store).assimilate_text(
        context.user_input,
        source_type=str(context.context_attrs.get("source_type") or "human_pi"),
        artifact_type=str(context.context_attrs.get("artifact_type") or "process_note"),
        title=context.context_attrs.get("title"),
        scope=dict(context.context_attrs.get("scope") or {}),
        evidence_refs=list(context.context_attrs.get("evidence_refs") or []),
        object_refs=list(context.context_attrs.get("object_refs") or []),
        confidence=float(context.context_attrs.get("confidence", 0.5)),
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=f"Human PI artifact ingested: {artifact.title}",
        output_attrs={
            "execution_type": skill.execution_type,
            "artifact_id": artifact.artifact_id,
            "artifact_type": artifact.artifact_type,
            "source_type": artifact.source_type,
            "confidence": artifact.confidence,
            "status": artifact.status,
        },
    )
