import pytest

from chanta_core.ocel.store import OCELStore
from chanta_core.tool_registry import ToolRegistryViewService
from chanta_core.tool_registry.errors import ToolPolicyNoteError
from chanta_core.tools import ToolDispatcher, ToolRegistry
from chanta_core.traces.trace_service import TraceService


def test_tool_registry_service_records_lifecycle_to_ocel(tmp_path) -> None:
    store = OCELStore(tmp_path / "tool_registry.sqlite")
    service = ToolRegistryViewService(trace_service=TraceService(ocel_store=store))
    descriptor = service.register_tool_descriptor(
        tool_name="read_file",
        tool_type="builtin",
        risk_level="read_only",
        capability_tags=["read"],
    )
    updated = service.update_tool_descriptor(
        descriptor=descriptor,
        description="Read file descriptor",
        risk_level="read_only",
    )
    snapshot = service.create_registry_snapshot(tools=[updated], snapshot_name="test")
    note = service.register_tool_policy_note(
        tool_id=updated.tool_id,
        tool_name=updated.tool_name,
        note_type="review_needed",
        text="Review later.",
    )
    annotation = service.register_tool_risk_annotation(
        tool_id=updated.tool_id,
        risk_level="read_only",
        risk_category="read",
    )
    service.update_tool_policy_note(note=note, text="Updated note.")
    service.update_tool_risk_annotation(annotation=annotation, rationale="Updated rationale.")

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}

    assert snapshot.tool_ids == [updated.tool_id]
    assert "tool_descriptor_registered" in activities
    assert "tool_descriptor_updated" in activities
    assert "tool_registry_snapshot_created" in activities
    assert "tool_policy_note_registered" in activities
    assert "tool_policy_note_updated" in activities
    assert "tool_risk_annotation_registered" in activities
    assert "tool_risk_annotation_updated" in activities
    assert store.fetch_objects_by_type("tool_descriptor")
    assert store.fetch_objects_by_type("tool_registry_snapshot")
    assert store.fetch_objects_by_type("tool_policy_note")
    assert store.fetch_objects_by_type("tool_risk_annotation")


def test_tool_registry_service_rejects_forbidden_note_type_and_does_not_mutate_dispatcher(tmp_path) -> None:
    store = OCELStore(tmp_path / "tool_registry_boundary.sqlite")
    service = ToolRegistryViewService(trace_service=TraceService(ocel_store=store))
    runtime_registry = ToolRegistry(include_builtins=False)
    ToolDispatcher(registry=runtime_registry)
    before = runtime_registry.list_tools()

    service.register_tool_descriptor(tool_name="view_only", tool_type="builtin")
    with pytest.raises(ToolPolicyNoteError):
        service.register_tool_policy_note(note_type="deny", text="forbidden")

    assert runtime_registry.list_tools() == before
