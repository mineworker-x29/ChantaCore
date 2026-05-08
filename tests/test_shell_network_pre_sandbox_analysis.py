from chanta_core.sandbox import (
    detect_shell_risk_tokens,
    infer_network_risk_level,
    infer_shell_risk_level,
    parse_network_intent,
    tokenize_shell_command,
)


def test_safe_command_classified_low_or_read_only() -> None:
    detected = detect_shell_risk_tokens("echo hello")

    assert tokenize_shell_command("echo hello") == ["echo", "hello"]
    assert detected["risk_categories"] == ["read_only"]
    assert infer_shell_risk_level(detected["risk_categories"]) == "low"


def test_destructive_command_detects_destructive_category() -> None:
    detected = detect_shell_risk_tokens("rm -rf ./data")

    assert "destructive_filesystem" in detected["risk_categories"]
    assert infer_shell_risk_level(detected["risk_categories"]) == "critical"


def test_network_command_detects_network_category() -> None:
    detected = detect_shell_risk_tokens("curl https://example.com")

    assert "network_access" in detected["risk_categories"]
    assert "https://example.com" in detected["detected_targets"]


def test_write_like_command_detects_filesystem_write_category() -> None:
    detected = detect_shell_risk_tokens("echo x > file.txt")

    assert "filesystem_write" in detected["risk_categories"]


def test_credential_indicator_detects_credential_exposure() -> None:
    detected = detect_shell_risk_tokens("echo AWS_ACCESS_KEY=abc")

    assert "credential_exposure" in detected["risk_categories"]
    assert infer_shell_risk_level(detected["risk_categories"]) == "critical"


def test_url_parsing_is_deterministic_without_access() -> None:
    parsed = parse_network_intent("https://example.com:443/path", None, None, None)

    assert parsed["protocol"] == "https"
    assert parsed["host"] == "example.com"
    assert parsed["port"] == 443
    assert parsed["target"] == "https://example.com:443"
    assert infer_network_risk_level(parsed["protocol"], parsed["host"], parsed["port"]) == "medium"


def test_localhost_network_risk_is_lower_than_external() -> None:
    assert infer_network_risk_level("http", "localhost", 8000) == "low"
    assert infer_network_risk_level("ssh", "example.com", 22) == "high"
