from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.service import PIGService
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_summarize_process_trace_skill() -> Skill:
    return Skill(
        skill_id="skill:summarize_process_trace",
        skill_name="summarize_process_trace",
        description="Summarize recent or process-instance-centered traces using OCPX and PIG.",
        execution_type="builtin_process_intelligence",
        input_schema={},
        output_schema={},
        tags=["builtin", "ocpx", "pig", "process-intelligence", "readonly"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_ocpx": True,
            "uses_pig": True,
        },
    )


def execute_summarize_process_trace_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    ocel_store: OCELStore | None = None,
    **_,
) -> SkillExecutionResult:
    store = ocel_store or OCELStore()
    loader = OCPXLoader(store)
    engine = OCPXEngine()
    pig_service = PIGService(loader=loader)
    process_instance_id = context.context_attrs.get("process_instance_id") or context.process_instance_id
    if process_instance_id:
        view = loader.load_process_instance_view(str(process_instance_id))
        pig_result = pig_service.analyze_process_instance(str(process_instance_id))
        scope = "process_instance"
    else:
        limit = int(context.context_attrs.get("limit", 20))
        view = loader.load_recent_view(limit=limit)
        pig_result = pig_service.analyze_recent(limit=limit)
        scope = "recent"

    activity_sequence = engine.activity_sequence(view)
    summary = engine.summarize_view(view)
    diagnostics = pig_result["diagnostics"]
    recommendations = pig_result["recommendations"]
    guide = pig_result["guide"]
    output_text = (
        f"Process trace summary ({scope}): {summary['event_count']} events, "
        f"{summary['object_count']} objects, {len(diagnostics)} diagnostics, "
        f"{len(recommendations)} recommendations."
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=output_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "activity_sequence": activity_sequence,
            "event_count": summary["event_count"],
            "object_count": summary["object_count"],
            "guide": guide,
            "diagnostics": diagnostics,
            "recommendations": recommendations,
            "scope": scope,
        },
    )
