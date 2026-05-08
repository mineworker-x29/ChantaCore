from chanta_core.delegation.ids import (
    new_delegated_process_run_id,
    new_delegation_link_id,
    new_delegation_packet_id,
    new_delegation_result_id,
)
from chanta_core.delegation.models import (
    DelegatedProcessRun,
    DelegationLink,
    DelegationPacket,
    DelegationResult,
)
from chanta_core.utility.time import utc_now_iso


def test_delegation_ids_use_expected_prefixes() -> None:
    assert new_delegation_packet_id().startswith("delegation_packet:")
    assert new_delegated_process_run_id().startswith("delegated_process_run:")
    assert new_delegation_result_id().startswith("delegation_result:")
    assert new_delegation_link_id().startswith("delegation_link:")


def test_delegation_packet_to_dict_defaults_transcript_flag() -> None:
    packet = DelegationPacket(
        packet_id="delegation_packet:test",
        packet_name="packet",
        parent_session_id="session:parent",
        parent_turn_id="turn:parent",
        parent_message_id="message:parent",
        parent_process_instance_id="process_instance:parent",
        goal="Analyze a bounded task.",
        context_summary="Summary only.",
        structured_inputs={"key": "value"},
        object_refs=[{"object_id": "object:1"}],
        allowed_capabilities=["read_context"],
        expected_output_schema={"type": "object"},
        termination_conditions={"max_steps": 1},
        permission_request_ids=["permission_request:1"],
        session_permission_resolution_ids=["session_permission_resolution:1"],
        workspace_write_sandbox_decision_ids=["workspace_write_sandbox_decision:1"],
        shell_network_pre_sandbox_decision_ids=["shell_network_pre_sandbox_decision:1"],
        process_outcome_evaluation_ids=["process_outcome_evaluation:1"],
        created_at=utc_now_iso(),
        packet_attrs={},
    )

    data = packet.to_dict()

    assert data["packet_id"] == "delegation_packet:test"
    assert data["goal"] == "Analyze a bounded task."
    assert data["packet_attrs"]["contains_full_parent_transcript"] is False


def test_delegated_process_run_to_dict_requires_no_permission_inheritance() -> None:
    run = DelegatedProcessRun(
        delegated_run_id="delegated_process_run:test",
        packet_id="delegation_packet:test",
        parent_session_id="session:parent",
        child_session_id="session:child",
        parent_process_instance_id="process_instance:parent",
        child_process_instance_id="process_instance:child",
        delegation_type="subprocess",
        isolation_mode="packet_only",
        status="created",
        requested_at=utc_now_iso(),
        started_at=None,
        completed_at=None,
        failed_at=None,
        requester_type="agent",
        requester_id="agent:parent",
        allowed_capabilities=["read_context"],
        inherited_permissions=False,
        run_attrs={},
    )

    data = run.to_dict()

    assert data["delegated_run_id"] == "delegated_process_run:test"
    assert data["inherited_permissions"] is False


def test_delegation_result_and_link_to_dict() -> None:
    result = DelegationResult(
        result_id="delegation_result:test",
        delegated_run_id="delegated_process_run:test",
        packet_id="delegation_packet:test",
        status="completed",
        output_summary="Done.",
        output_payload={"value": 1},
        evidence_refs=[{"ref": "evidence"}],
        recommendation_refs=[{"ref": "recommendation"}],
        failure=None,
        created_at=utc_now_iso(),
        result_attrs={},
    )
    link = DelegationLink(
        link_id="delegation_link:test",
        delegated_run_id="delegated_process_run:test",
        parent_process_instance_id="process_instance:parent",
        child_process_instance_id="process_instance:child",
        parent_session_id="session:parent",
        child_session_id="session:child",
        relation_type="delegated_to",
        created_at=utc_now_iso(),
        link_attrs={},
    )

    assert result.to_dict()["status"] == "completed"
    assert result.to_dict()["evidence_refs"]
    assert link.to_dict()["relation_type"] == "delegated_to"
    assert link.to_dict()["child_session_id"] == "session:child"
