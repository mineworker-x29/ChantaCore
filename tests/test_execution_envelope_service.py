from chanta_core.execution import ExecutionEnvelopeService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_explicit_invocation_completed_wraps_to_completed_envelope(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    invocation_service = ExplicitSkillInvocationService()
    invocation_result = invocation_service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )
    envelope_service = ExecutionEnvelopeService()

    envelope = envelope_service.wrap_explicit_invocation_result(
        invocation_result=invocation_result,
        invocation_request=invocation_service.last_request,
        invocation_input=invocation_service.last_input,
    )

    assert envelope.status == "completed"
    assert envelope.execution_kind == "explicit_skill_invocation"
    assert envelope.execution_performed is True
    assert envelope_service.last_input_snapshot.full_input_stored is False
    assert envelope_service.last_output_snapshot.full_output_stored is False
    assert envelope_service.last_outcome_summary.succeeded is True


def test_render_envelope_summary() -> None:
    service = ExecutionEnvelopeService()
    envelope = service.create_envelope(
        execution_kind="manual",
        execution_subject_id="subject:test",
        skill_id=None,
        status="skipped",
        execution_allowed=False,
        execution_performed=False,
        blocked=False,
    )

    rendered = service.render_envelope_summary(envelope)

    assert "Execution Envelope" in rendered
    assert "full_input_stored=false" in rendered
    assert "full_output_stored=false" in rendered
