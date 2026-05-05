from chanta_core.ocel.store import OCELStore
from chanta_core.tool_registry import ToolRegistryViewService
from chanta_core.traces.trace_service import TraceService


def test_write_tool_views_writes_noncanonical_files_and_overwrite_false_skips(tmp_path) -> None:
    store = OCELStore(tmp_path / "tool_views.sqlite")
    service = ToolRegistryViewService(trace_service=TraceService(ocel_store=store), root=tmp_path)
    descriptor = service.register_tool_descriptor(
        tool_name="write_file",
        tool_type="builtin",
        risk_level="high",
    )
    snapshot = service.create_registry_snapshot(tools=[descriptor])
    note = service.register_tool_policy_note(
        tool_id=descriptor.tool_id,
        tool_name=descriptor.tool_name,
        note_type="review_needed",
        text="Review write tools.",
    )
    annotation = service.register_tool_risk_annotation(
        tool_id=descriptor.tool_id,
        risk_level="high",
        risk_category="write",
    )

    results = service.write_tool_views(
        tools=[descriptor],
        snapshot=snapshot,
        policy_notes=[note],
        risk_annotations=[annotation],
        root=tmp_path,
    )
    skipped = service.write_tool_views(
        tools=[descriptor],
        snapshot=snapshot,
        policy_notes=[note],
        risk_annotations=[annotation],
        root=tmp_path,
        overwrite=False,
    )

    tools_path = tmp_path / ".chanta" / "TOOLS.md"
    policy_path = tmp_path / ".chanta" / "TOOL_POLICY.md"
    assert results["tools"]["written"] is True
    assert tools_path.exists()
    assert policy_path.exists()
    assert "not the canonical tool registry" in tools_path.read_text(encoding="utf-8")
    assert "not PermissionPolicy" in policy_path.read_text(encoding="utf-8")
    assert skipped["tools"]["written"] is False
    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert "tool_registry_view_written" in activities
    assert "tool_policy_view_written" in activities
