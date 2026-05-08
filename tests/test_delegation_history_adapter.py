from chanta_core.delegation.history_adapter import (
    delegated_process_runs_to_history_entries,
    delegation_packets_to_history_entries,
    delegation_results_to_history_entries,
)
from chanta_core.delegation.models import DelegatedProcessRun, DelegationPacket, DelegationResult
from chanta_core.utility.time import utc_now_iso


def _packet() -> DelegationPacket:
    return DelegationPacket(
        packet_id="delegation_packet:history",
        packet_name=None,
        parent_session_id="session:parent",
        parent_turn_id=None,
        parent_message_id=None,
        parent_process_instance_id="process_instance:parent",
        goal="History conversion.",
        context_summary=None,
        structured_inputs={},
        object_refs=[],
        allowed_capabilities=[],
        expected_output_schema=None,
        termination_conditions={},
        permission_request_ids=["permission_request:1"],
        session_permission_resolution_ids=["session_permission_resolution:1"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:1"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:1"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:1"],
        created_at=utc_now_iso(),
        packet_attrs={},
    )


def _run(status: str = "started") -> DelegatedProcessRun:
    return DelegatedProcessRun(
        delegated_run_id="delegated_process_run:history",
        packet_id="delegation_packet:history",
        parent_session_id="session:parent",
        child_session_id="session:child",
        parent_process_instance_id="process_instance:parent",
        child_process_instance_id="process_instance:child",
        delegation_type="analysis",
        isolation_mode="packet_only",
        status=status,
        requested_at=utc_now_iso(),
        started_at=None,
        completed_at=None,
        failed_at=None,
        requester_type=None,
        requester_id=None,
        allowed_capabilities=[],
        inherited_permissions=False,
        run_attrs={},
    )


def _result(status: str = "failed") -> DelegationResult:
    return DelegationResult(
        result_id="delegation_result:history",
        delegated_run_id="delegated_process_run:history",
        packet_id="delegation_packet:history",
        status=status,
        output_summary="Result.",
        output_payload={},
        evidence_refs=[],
        recommendation_refs=[],
        failure={"message": "failed"} if status == "failed" else None,
        created_at=utc_now_iso(),
        result_attrs={},
    )


def test_delegation_history_adapter_converts_packets_runs_and_results() -> None:
    packet_entry = delegation_packets_to_history_entries([_packet()])[0]
    run_entry = delegated_process_runs_to_history_entries([_run()])[0]
    result_entry = delegation_results_to_history_entries([_result()])[0]
    inconclusive_entry = delegation_results_to_history_entries([_result("inconclusive")])[0]

    assert packet_entry.source == "delegation"
    assert packet_entry.role == "context"
    assert packet_entry.refs[0]["packet_id"] == "delegation_packet:history"
    assert packet_entry.refs[0]["permission_request_ids"] == ["permission_request:1"]
    assert run_entry.refs[0]["delegated_run_id"] == "delegated_process_run:history"
    assert run_entry.refs[0]["child_session_id"] == "session:child"
    assert result_entry.refs[0]["result_id"] == "delegation_result:history"
    assert result_entry.priority >= 90
    assert inconclusive_entry.priority >= 80
