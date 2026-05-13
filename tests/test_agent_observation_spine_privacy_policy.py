from chanta_core.observation import AgentObservationSpineService


def test_default_redaction_and_export_policies_are_safe() -> None:
    service = AgentObservationSpineService()
    redaction = service.create_redaction_policy()
    export = service.create_export_policy()

    assert redaction.redact_private_paths is True
    assert redaction.redact_full_bodies is True
    assert redaction.redact_secrets is True
    assert redaction.redact_user_identifiers is True
    assert "raw_transcript" in redaction.denied_export_fields
    assert export.allow_raw_transcript_export is False
    assert export.allow_full_file_body_export is False
    assert export.allow_private_memory_export is False
    assert export.require_operator_approval is True
    assert export.require_redaction is True
