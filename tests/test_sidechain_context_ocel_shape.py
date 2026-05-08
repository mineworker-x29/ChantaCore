from chanta_core.delegation import DelegatedProcessRunService, SidechainContextService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.traces.trace_service import TraceService


def test_sidechain_context_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "sidechain_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    delegation_service = DelegatedProcessRunService(trace_service=trace_service)
    sidechain_service = SidechainContextService(trace_service=trace_service)
    packet = delegation_service.create_delegation_packet(
        goal="Shape sidechain.",
        context_summary="Summary.",
        parent_session_id="session:parent",
        parent_process_instance_id="process_instance:parent",
        permission_request_ids=["permission_request:shape"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:shape"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:shape"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:shape"],
    )
    run = delegation_service.create_delegated_process_run(
        packet_id=packet.packet_id,
        parent_session_id=packet.parent_session_id,
        child_session_id="session:child",
        parent_process_instance_id=packet.parent_process_instance_id,
        child_process_instance_id="process_instance:child",
    )
    context = sidechain_service.create_sidechain_context_from_packet(packet=packet, delegated_run=run)
    entries = sidechain_service.build_entries_from_packet(context=context, packet=packet)
    context = sidechain_service.mark_context_ready(context=context, entry_ids=[entry.entry_id for entry in entries])
    context = sidechain_service.seal_context(context=context)
    snapshot = sidechain_service.build_snapshot(context=context, entries=entries)
    envelope = sidechain_service.record_return_envelope(
        sidechain_context_id=context.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=run.delegated_run_id,
        status="completed",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(200)}

    assert {
        "sidechain_context_created",
        "sidechain_context_entry_added",
        "sidechain_context_snapshot_created",
        "sidechain_return_envelope_recorded",
        "sidechain_parent_transcript_excluded",
        "sidechain_permission_inheritance_prevented",
        "sidechain_safety_refs_attached",
    }.issubset(activities)
    assert store.fetch_objects_by_type("sidechain_context")
    assert store.fetch_objects_by_type("sidechain_context_entry")
    assert store.fetch_objects_by_type("sidechain_context_snapshot")
    assert store.fetch_objects_by_type("sidechain_return_envelope")
    assert store.fetch_object_object_relations_for_object(context.sidechain_context_id)
    assert store.fetch_object_object_relations_for_object(entries[0].entry_id)
    assert store.fetch_object_object_relations_for_object(snapshot.snapshot_id)
    assert store.fetch_object_object_relations_for_object(envelope.envelope_id)

    loader = OCPXLoader(store=store)
    parent_view = loader.load_session_view("session:parent")
    child_process_view = loader.load_process_instance_view("process_instance:child")
    assert "sidechain_context_created" in {event.event_activity for event in parent_view.events}
    assert "sidechain_context_sealed" in {event.event_activity for event in child_process_view.events}
