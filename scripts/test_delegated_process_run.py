from chanta_core.delegation import DelegatedProcessRunService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    store = OCELStore("data/ocel/delegated_process_run_demo.sqlite")
    service = DelegatedProcessRunService(trace_service=TraceService(ocel_store=store))
    packet = service.create_delegation_packet(
        goal="Summarize delegation foundation status.",
        context_summary="Demo packet for v0.13.0 delegated process run records.",
        structured_inputs={"scope": "demo"},
        allowed_capabilities=["read_context"],
        permission_request_ids=["permission_request:demo"],
        session_permission_resolution_ids=["session_permission_resolution:demo"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:demo"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:demo"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:demo"],
        parent_session_id="session:demo-parent",
        parent_process_instance_id="process_instance:demo-parent",
    )
    run = service.create_delegated_process_run(
        packet_id=packet.packet_id,
        parent_session_id=packet.parent_session_id,
        child_session_id="session:demo-child",
        parent_process_instance_id=packet.parent_process_instance_id,
        child_process_instance_id="process_instance:demo-child",
    )
    run = service.request_delegated_process_run(run=run)
    run = service.start_delegated_process_run(run=run)
    result = service.record_delegation_result(
        delegated_run_id=run.delegated_run_id,
        packet_id=packet.packet_id,
        status="completed",
        output_summary="Demo result recorded without executing a child runtime.",
        output_payload={"executed": False},
    )
    run = service.complete_delegated_process_run(run=run)
    link = service.record_delegation_link(
        delegated_run_id=run.delegated_run_id,
        parent_process_instance_id=run.parent_process_instance_id,
        child_process_instance_id=run.child_process_instance_id,
        parent_session_id=run.parent_session_id,
        child_session_id=run.child_session_id,
    )
    print(f"packet_id={packet.packet_id}")
    print(f"delegated_run_id={run.delegated_run_id} status={run.status}")
    print(f"result_id={result.result_id} status={result.status}")
    print(f"link_id={link.link_id} relation_type={link.relation_type}")


if __name__ == "__main__":
    main()
