from chanta_core.delegation import DelegatedProcessRunService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.traces.trace_service import TraceService


def test_delegation_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "delegation_shape.sqlite")
    service = DelegatedProcessRunService(trace_service=TraceService(ocel_store=store))
    packet = service.create_delegation_packet(
        goal="Shape.",
        parent_session_id="session:parent",
        parent_turn_id="turn:parent",
        parent_message_id="message:parent",
        parent_process_instance_id="process_instance:parent",
        permission_request_ids=["permission_request:shape"],
        session_permission_resolution_ids=["session_permission_resolution:shape"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:shape"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:shape"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:shape"],
    )
    run = service.create_delegated_process_run(
        packet_id=packet.packet_id,
        parent_session_id="session:parent",
        child_session_id="session:child",
        parent_process_instance_id="process_instance:parent",
        child_process_instance_id="process_instance:child",
    )
    run = service.request_delegated_process_run(run=run)
    run = service.start_delegated_process_run(run=run)
    run = service.complete_delegated_process_run(run=run)
    result = service.record_delegation_result(
        delegated_run_id=run.delegated_run_id,
        packet_id=packet.packet_id,
        status="completed",
    )
    link = service.record_delegation_link(
        delegated_run_id=run.delegated_run_id,
        parent_session_id=run.parent_session_id,
        child_session_id=run.child_session_id,
        parent_process_instance_id=run.parent_process_instance_id,
        child_process_instance_id=run.child_process_instance_id,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    assert {
        "delegation_packet_created",
        "delegated_process_run_created",
        "delegated_process_requested",
        "delegated_process_started",
        "delegated_process_completed",
        "delegation_result_recorded",
        "delegation_link_recorded",
        "delegation_permission_context_referenced",
        "delegation_safety_context_referenced",
    }.issubset(activities)
    assert store.fetch_objects_by_type("delegation_packet")
    assert store.fetch_objects_by_type("delegated_process_run")
    assert store.fetch_objects_by_type("delegation_result")
    assert store.fetch_objects_by_type("delegation_link")
    assert store.fetch_object_object_relations_for_object(run.delegated_run_id)
    assert store.fetch_object_object_relations_for_object(result.result_id)
    assert store.fetch_object_object_relations_for_object(link.link_id)

    loader = OCPXLoader(store=store)
    parent_session_view = loader.load_session_view("session:parent")
    child_process_view = loader.load_process_instance_view("process_instance:child")
    assert "delegation_packet_created" in {event.event_activity for event in parent_session_view.events}
    assert "delegated_process_completed" in {event.event_activity for event in child_process_view.events}
