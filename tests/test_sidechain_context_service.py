from chanta_core.delegation import DelegatedProcessRunService, SidechainContextService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _packet_and_run(tmp_path):
    store = OCELStore(tmp_path / "sidechain_service.sqlite")
    trace_service = TraceService(ocel_store=store)
    delegation_service = DelegatedProcessRunService(trace_service=trace_service)
    sidechain_service = SidechainContextService(trace_service=trace_service)
    packet = delegation_service.create_delegation_packet(
        goal="Build sidechain context.",
        context_summary="Summary only.",
        structured_inputs={"target": "context"},
        object_refs=[{"object_type": "artifact", "object_id": "artifact:1"}],
        allowed_capabilities=["read_context"],
        expected_output_schema={"type": "object"},
        termination_conditions={"max_steps": 0},
        parent_session_id="session:parent",
        parent_process_instance_id="process_instance:parent",
        permission_request_ids=["permission_request:1"],
        session_permission_resolution_ids=["session_permission_resolution:1"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:1"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:1"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:1"],
    )
    run = delegation_service.create_delegated_process_run(
        packet_id=packet.packet_id,
        parent_session_id=packet.parent_session_id,
        child_session_id="session:child",
        parent_process_instance_id=packet.parent_process_instance_id,
        child_process_instance_id="process_instance:child",
    )
    return store, sidechain_service, packet, run


def test_sidechain_service_records_context_entries_snapshot_and_envelope(tmp_path) -> None:
    store, service, packet, run = _packet_and_run(tmp_path)

    context = service.create_sidechain_context_from_packet(packet=packet, delegated_run=run)
    entries = service.build_entries_from_packet(context=context, packet=packet)
    ready = service.mark_context_ready(context=context, entry_ids=[entry.entry_id for entry in entries])
    sealed = service.seal_context(context=ready)
    archived = service.archive_context(context=sealed)
    error = service.mark_context_error(context=context, failure={"reason": "test"})
    snapshot = service.build_snapshot(context=sealed, entries=entries, summary="Snapshot.")
    envelope = service.record_return_envelope(
        sidechain_context_id=sealed.sidechain_context_id,
        packet_id=packet.packet_id,
        delegated_run_id=run.delegated_run_id,
        status="completed",
        summary="Summary only.",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(200)}
    entry_types = {entry.entry_type for entry in entries}

    assert {
        "sidechain_context_created",
        "sidechain_parent_transcript_excluded",
        "sidechain_permission_inheritance_prevented",
        "sidechain_context_entry_added",
        "sidechain_safety_refs_attached",
        "sidechain_context_ready",
        "sidechain_context_sealed",
        "sidechain_context_archived",
        "sidechain_context_error",
        "sidechain_context_snapshot_created",
        "sidechain_return_envelope_recorded",
    }.issubset(activities)
    assert {
        "goal",
        "context_summary",
        "structured_input",
        "object_ref",
        "allowed_capability",
        "expected_output_schema",
        "termination_condition",
        "permission_ref",
        "sandbox_ref",
        "risk_ref",
        "outcome_ref",
    }.issubset(entry_types)
    assert context.contains_full_parent_transcript is False
    assert context.inherited_permissions is False
    assert ready.status == "ready"
    assert sealed.status == "sealed"
    assert archived.status == "archived"
    assert error.status == "error"
    assert snapshot.entry_count == len(entries)
    assert envelope.contains_full_child_transcript is False


def test_sidechain_service_records_without_runtime_execution(tmp_path) -> None:
    store, service, packet, run = _packet_and_run(tmp_path)

    context = service.create_sidechain_context_from_packet(packet=packet, delegated_run=run)

    assert context.status == "created"
    assert context.contains_full_parent_transcript is False
    assert context.inherited_permissions is False
    object_attrs = store.fetch_objects_by_type("sidechain_context")[0]["object_attrs"]
    assert object_attrs["contains_full_parent_transcript"] is False
    assert object_attrs["inherited_permissions"] is False
