from chanta_core.execution import ExecutionEnvelopeService
from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_gate_blocked_wraps_to_blocked_envelope() -> None:
    gate_service = SkillExecutionGateService()
    gate_result = gate_service.gate_explicit_invocation(
        skill_id="skill:write_file",
        input_payload={"root_path": "<ROOT>", "relative_path": "docs/example.txt"},
    )
    envelope_service = ExecutionEnvelopeService()

    envelope = envelope_service.wrap_gated_invocation_result(
        gate_result=gate_result,
        gate_request=gate_service.last_request,
        gate_decision=gate_service.last_decision,
    )

    assert envelope.status == "blocked"
    assert envelope.execution_performed is False
    assert envelope.blocked is True
    assert envelope_service.last_provenance.gate_result_id == gate_result.gate_result_id
    assert envelope_service.last_outcome_summary.finding_ids == gate_result.finding_ids


def test_gate_allowed_and_invocation_completed_wraps_to_completed_envelope(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    gate_service = SkillExecutionGateService()
    gate_result = gate_service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )
    invocation_service = ExplicitSkillInvocationService()
    invocation_result = invocation_service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )
    envelope_service = ExecutionEnvelopeService()

    envelope = envelope_service.wrap_gated_invocation_result(
        gate_result=gate_result,
        gate_request=gate_service.last_request,
        gate_decision=gate_service.last_decision,
        invocation_result=invocation_result,
        invocation_request=invocation_service.last_request,
        invocation_input=invocation_service.last_input,
    )

    assert envelope.status == "completed"
    assert envelope.execution_performed is True
    assert envelope_service.last_provenance.gate_request_id == gate_result.gate_request_id
    assert envelope_service.last_provenance.explicit_invocation_result_id == gate_result.explicit_invocation_result_id
