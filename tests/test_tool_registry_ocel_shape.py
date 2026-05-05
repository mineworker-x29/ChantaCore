from chanta_core.ocel.store import OCELStore
from chanta_core.tool_registry import ToolRegistryViewService
from chanta_core.traces.trace_service import TraceService


def test_tool_registry_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "tool_registry_shape.sqlite")
    service = ToolRegistryViewService(trace_service=TraceService(ocel_store=store), root=tmp_path)
    descriptor = service.register_tool_descriptor(tool_name="verify_file_exists", tool_type="verification")
    snapshot = service.create_registry_snapshot(tools=[descriptor])
    note = service.register_tool_policy_note(
        tool_id=descriptor.tool_id,
        tool_name=descriptor.tool_name,
        note_type="informational",
        text="View only.",
    )
    annotation = service.register_tool_risk_annotation(
        tool_id=descriptor.tool_id,
        risk_level="read_only",
        risk_category="read",
    )
    service.write_tool_views(
        tools=[descriptor],
        snapshot=snapshot,
        policy_notes=[note],
        risk_annotations=[annotation],
        root=tmp_path,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}

    assert {
        "tool_descriptor_registered",
        "tool_registry_snapshot_created",
        "tool_policy_note_registered",
        "tool_risk_annotation_registered",
        "tool_registry_view_written",
        "tool_policy_view_written",
    }.issubset(activities)
    assert store.fetch_objects_by_type("tool_descriptor")
    assert store.fetch_objects_by_type("tool_registry_snapshot")
    assert store.fetch_objects_by_type("tool_policy_note")
    assert store.fetch_objects_by_type("tool_risk_annotation")
