from chanta_core.context.redaction import make_preview, redact_sensitive_text


def test_redacts_obvious_secret_assignment_lines() -> None:
    text = "name=public\nAPI_KEY=secret-value\npassword: hunter2"

    redacted = redact_sensitive_text(text)

    assert "name=public" in redacted
    assert "secret-value" not in redacted
    assert "hunter2" not in redacted
    assert "API_KEY=[REDACTED]" in redacted


def test_redacts_bearer_token_and_private_key_block() -> None:
    text = (
        "Authorization: Bearer abc.def.ghi\n"
        "-----BEGIN RSA PRIVATE KEY-----\n"
        "very-secret\n"
        "-----END RSA PRIVATE KEY-----"
    )

    redacted = redact_sensitive_text(text)

    assert "Bearer [REDACTED]" in redacted
    assert "very-secret" not in redacted
    assert "[REDACTED PRIVATE KEY]" in redacted


def test_make_preview_redacts_and_truncates_deterministically() -> None:
    text = "API_KEY=secret\n" + ("safe " * 30)

    preview = make_preview(text, max_chars=40, redact=True)

    assert len(preview) == 40
    assert "secret" not in preview
    assert preview.endswith("...[preview truncated]...")
