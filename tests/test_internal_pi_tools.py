from chanta_core.ocel.store import OCELStore
from chanta_core.tools.context import ToolExecutionContext
from chanta_core.tools.dispatcher import ToolDispatcher
from chanta_core.tools.request import ToolRequest
from tests.test_ocel_store import make_record


def tool_context() -> ToolExecutionContext:
    return ToolExecutionContext(
        process_instance_id="process_instance:pi-tools",
        session_id="session-pi-tools",
        agent_id="chanta_core_default",
    )


def dispatch(dispatcher: ToolDispatcher, tool_id: str, operation: str, **input_attrs):
    return dispatcher.dispatch(
        ToolRequest.create(
            tool_id=tool_id,
            operation=operation,
            process_instance_id="process_instance:pi-tools",
            session_id="session-pi-tools",
            agent_id="chanta_core_default",
            input_attrs=input_attrs,
        ),
        tool_context(),
    )


def test_ocel_tool_operations(tmp_path) -> None:
    store = OCELStore(tmp_path / "ocel_tool.sqlite")
    store.append_record(make_record())
    dispatcher = ToolDispatcher(ocel_store=store)

    assert dispatch(dispatcher, "tool:ocel", "query_recent_events").success is True
    assert dispatch(dispatcher, "tool:ocel", "count_events").output_attrs["event_count"] == 1
    assert dispatch(dispatcher, "tool:ocel", "count_objects").output_attrs["object_count"] == 2
    assert dispatch(dispatcher, "tool:ocel", "count_relations").output_attrs["relation_count"] == 2
    assert dispatch(dispatcher, "tool:ocel", "validate_relations").output_attrs["validation"]["valid"] is True


def test_ocpx_tool_operations(tmp_path) -> None:
    store = OCELStore(tmp_path / "ocpx_tool.sqlite")
    store.append_record(make_record())
    dispatcher = ToolDispatcher(ocel_store=store)

    assert dispatch(dispatcher, "tool:ocpx", "compute_activity_sequence").output_attrs["activity_sequence"]
    assert dispatch(dispatcher, "tool:ocpx", "compute_variant_summary").output_attrs["variant_summary"]["trace_count"] == 1
    assert dispatch(dispatcher, "tool:ocpx", "compute_relation_coverage").output_attrs["relation_coverage"]["events_total"] == 1
    assert dispatch(dispatcher, "tool:ocpx", "compute_basic_performance").output_attrs["performance_summary"]["event_count"] == 1
    assert dispatch(dispatcher, "tool:ocpx", "summarize_for_pig_context").output_attrs["pig_context_summary"]["activity_sequence"]


def test_pig_tool_operations(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_tool.sqlite")
    store.append_record(make_record())
    dispatcher = ToolDispatcher(ocel_store=store)

    context_result = dispatch(dispatcher, "tool:pig", "build_context")
    conformance_result = dispatch(dispatcher, "tool:pig", "check_self_conformance")
    guidance_result = dispatch(dispatcher, "tool:pig", "build_guidance")
    artifacts_result = dispatch(dispatcher, "tool:pig", "summarize_pi_artifacts")

    assert context_result.success is True
    assert "Process Intelligence Context" in context_result.output_attrs["context_text"]
    assert conformance_result.output_attrs["status"]
    assert isinstance(guidance_result.output_attrs["guidance"], list)
    assert "artifact_count" in artifacts_result.output_attrs
