from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill


def create_inspect_ocel_recent_skill() -> Skill:
    return Skill(
        skill_id="skill:inspect_ocel_recent",
        skill_name="inspect_ocel_recent",
        description=(
            "Inspect recent OCEL events, objects, and relations from the "
            "ChantaCore OCELStore."
        ),
        execution_type="builtin_process_introspection",
        input_schema={},
        output_schema={},
        tags=["builtin", "ocel", "process-intelligence", "readonly"],
        skill_attrs={
            "is_builtin": True,
            "requires_llm": False,
            "requires_external_tool": False,
            "uses_ocel_store": True,
        },
    )


def execute_inspect_ocel_recent_skill(
    *,
    skill: Skill,
    context: SkillExecutionContext,
    ocel_store: OCELStore | None = None,
    **_,
) -> SkillExecutionResult:
    store = ocel_store or OCELStore()
    limit = int(context.context_attrs.get("limit", 10))
    recent_events = store.fetch_recent_events(limit=limit)
    duplicate_validation = OCELValidator(store).validate_duplicate_relations()
    recent_activities = [str(event["event_activity"]) for event in recent_events]
    event_count = store.fetch_event_count()
    object_count = store.fetch_object_count()
    event_object_relation_count = store.fetch_event_object_relation_count()
    object_object_relation_count = store.fetch_object_object_relation_count()
    output_text = (
        "OCEL recent inspection: "
        f"{event_count} events, {object_count} objects, "
        f"{event_object_relation_count} event-object relations, "
        f"{object_object_relation_count} object-object relations."
    )
    return SkillExecutionResult(
        skill_id=skill.skill_id,
        skill_name=skill.skill_name,
        success=True,
        output_text=output_text,
        output_attrs={
            "execution_type": skill.execution_type,
            "event_count": event_count,
            "object_count": object_count,
            "event_object_relation_count": event_object_relation_count,
            "object_object_relation_count": object_object_relation_count,
            "recent_event_activities": recent_activities,
            "duplicate_relations_valid": bool(duplicate_validation.get("valid")),
        },
    )
