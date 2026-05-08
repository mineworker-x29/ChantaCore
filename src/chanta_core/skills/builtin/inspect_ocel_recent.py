from __future__ import annotations

from chanta_core.ocel.store import OCELStore
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.result import SkillExecutionResult
from chanta_core.skills.skill import Skill
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest


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
    trace_service=None,
    **_,
) -> SkillExecutionResult:
    store = ocel_store or OCELStore()
    limit = int(context.context_attrs.get("limit", 10))
    dispatcher = ToolDispatcher(trace_service=trace_service, ocel_store=store)
    tool_context = ToolExecutionContext(
        process_instance_id=context.process_instance_id,
        session_id=context.session_id,
        agent_id=context.agent_id,
        context_attrs=context.context_attrs,
    )
    recent_result = _dispatch_ocel(
        dispatcher,
        tool_context,
        context,
        skill.skill_id,
        "query_recent_events",
        {"limit": limit},
    )
    events_result = _dispatch_ocel(dispatcher, tool_context, context, skill.skill_id, "count_events")
    objects_result = _dispatch_ocel(dispatcher, tool_context, context, skill.skill_id, "count_objects")
    relations_result = _dispatch_ocel(dispatcher, tool_context, context, skill.skill_id, "count_relations")
    validation_result = _dispatch_ocel(dispatcher, tool_context, context, skill.skill_id, "validate_relations")
    recent_events = list(recent_result.output_attrs.get("recent_events") or [])
    duplicate_validation = dict(validation_result.output_attrs.get("validation") or {})
    recent_activities = [str(event["event_activity"]) for event in recent_events]
    event_count = int(events_result.output_attrs.get("event_count") or 0)
    object_count = int(objects_result.output_attrs.get("object_count") or 0)
    event_object_relation_count = int(
        relations_result.output_attrs.get("event_object_relation_count") or 0
    )
    object_object_relation_count = int(
        relations_result.output_attrs.get("object_object_relation_count") or 0
    )
    inspection_scope = "recent_global"
    persistence_scope = "persisted_store"
    output_text = (
        "OCEL recent inspection "
        f"(inspection_scope={inspection_scope}, persistence_scope={persistence_scope}): "
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
            "inspection_scope": inspection_scope,
            "persistence_scope": persistence_scope,
            "current_session_scope_enabled": False,
            "current_process_instance_scope_enabled": False,
            "recent_event_activities": recent_activities,
            "duplicate_relations_valid": bool(duplicate_validation.get("valid")),
            "tool_results": [
                recent_result.to_dict(),
                events_result.to_dict(),
                objects_result.to_dict(),
                relations_result.to_dict(),
                validation_result.to_dict(),
            ],
        },
    )


def _dispatch_ocel(
    dispatcher: ToolDispatcher,
    tool_context: ToolExecutionContext,
    context: SkillExecutionContext,
    skill_id: str,
    operation: str,
    input_attrs: dict | None = None,
):
    result = dispatcher.dispatch(
        ToolRequest.create(
            tool_id="tool:ocel",
            operation=operation,
            process_instance_id=context.process_instance_id,
            session_id=context.session_id,
            agent_id=context.agent_id,
            input_attrs=input_attrs or {},
            request_attrs={"source_skill_id": skill_id},
        ),
        tool_context,
    )
    if not result.success:
        raise RuntimeError(result.error or f"tool:ocel {operation} failed")
    return result
