from chanta_core.execution import ExecutionEnvelopeService, hash_payload, preview_payload, redact_sensitive_fields


def test_sensitive_fields_are_redacted_from_snapshot_preview() -> None:
    payload = {
        "relative_path": "docs/example.txt",
        "token": "secret-token",
        "nested": {"api_key": "secret-key"},
    }
    service = ExecutionEnvelopeService()
    envelope = service.create_envelope(
        execution_kind="test",
        execution_subject_id="subject:test",
        skill_id="skill:read_workspace_text_file",
        status="completed",
        execution_allowed=True,
        execution_performed=False,
        blocked=False,
    )

    snapshot = service.record_input_snapshot(envelope=envelope, input_payload=payload)

    assert snapshot.input_preview["token"] == "<REDACTED>"
    assert "token" in snapshot.redacted_fields
    assert "nested.api_key" in snapshot.redacted_fields
    assert snapshot.full_input_stored is False


def test_payload_helpers_are_deterministic_and_preview_only() -> None:
    payload = {"value": "abc", "password": "hidden"}
    redacted, fields = redact_sensitive_fields(payload)

    assert hash_payload(payload) == hash_payload({"password": "hidden", "value": "abc"})
    assert preview_payload({"long": "x" * 3000})["long"] == "x" * 2000
    assert redacted["password"] == "<REDACTED>"
    assert fields == ["password"]
