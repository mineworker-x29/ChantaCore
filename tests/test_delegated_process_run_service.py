from chanta_core.delegation import DelegatedProcessRunService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_delegated_process_run_service_records_packet_run_result_and_link(tmp_path) -> None:
    store = OCELStore(tmp_path / "delegation_service.sqlite")
    service = DelegatedProcessRunService(trace_service=TraceService(ocel_store=store))

    packet = service.create_delegation_packet(
        goal="Check delegated record shape.",
        context_summary="Summary only.",
        structured_inputs={"item": "value"},
        allowed_capabilities=["read_context"],
        parent_session_id="session:parent",
        parent_turn_id="turn:parent",
        parent_message_id="message:parent",
        parent_process_instance_id="process_instance:parent",
        permission_request_ids=["permission_request:1"],
        session_permission_resolution_ids=["session_permission_resolution:1"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:1"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:1"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:1"],
    )
    run = service.create_delegated_process_run(
        packet_id=packet.packet_id,
        parent_session_id=packet.parent_session_id,
        child_session_id="session:child",
        parent_process_instance_id=packet.parent_process_instance_id,
        child_process_instance_id="process_instance:child",
    )
    requested = service.request_delegated_process_run(run=run)
    started = service.start_delegated_process_run(run=requested)
    completed = service.complete_delegated_process_run(run=started)
    failed = service.fail_delegated_process_run(run=run, failure={"reason": "test"})
    cancelled = service.cancel_delegated_process_run(run=run)
    skipped = service.skip_delegated_process_run(run=run)
    result = service.record_delegation_result(
        delegated_run_id=completed.delegated_run_id,
        packet_id=packet.packet_id,
        status="completed",
        output_summary="Recorded only.",
    )
    link = service.record_delegation_link(
        delegated_run_id=completed.delegated_run_id,
        parent_process_instance_id=completed.parent_process_instance_id,
        child_process_instance_id=completed.child_process_instance_id,
        parent_session_id=completed.parent_session_id,
        child_session_id=completed.child_session_id,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    assert {
        "delegation_packet_created",
        "delegated_process_run_created",
        "delegated_process_requested",
        "delegated_process_started",
        "delegated_process_completed",
        "delegated_process_failed",
        "delegated_process_cancelled",
        "delegated_process_skipped",
        "delegation_result_recorded",
        "delegation_link_recorded",
        "delegation_permission_context_referenced",
        "delegation_safety_context_referenced",
    }.issubset(activities)
    assert run.inherited_permissions is False
    assert completed.status == "completed"
    assert failed.status == "failed"
    assert cancelled.status == "cancelled"
    assert skipped.status == "skipped"
    assert result.delegated_run_id == completed.delegated_run_id
    assert link.delegated_run_id == completed.delegated_run_id


def test_delegated_process_run_service_records_without_child_runtime_calls(tmp_path) -> None:
    store = OCELStore(tmp_path / "delegation_no_child_runtime.sqlite")
    service = DelegatedProcessRunService(ocel_store=store)

    packet = service.create_delegation_packet(goal="Record only.")
    run = service.create_delegated_process_run(packet_id=packet.packet_id)

    assert run.status == "created"
    assert run.inherited_permissions is False
    assert store.fetch_objects_by_type("delegated_process_run")[0]["object_attrs"]["inherited_permissions"] is False
