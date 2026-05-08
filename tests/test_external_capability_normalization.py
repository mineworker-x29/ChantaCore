from chanta_core.external import (
    extract_descriptor_name,
    extract_descriptor_type,
    infer_risk_level,
    normalize_capability_type,
    normalize_permission,
    normalize_risk_category,
)


def test_capability_type_normalization() -> None:
    assert normalize_capability_type("tool") == "tool"
    assert normalize_capability_type("skill") == "skill"
    assert normalize_capability_type("adapter") == "adapter"
    assert normalize_capability_type("connector") == "connector"
    assert normalize_capability_type("mcp") == "mcp_server"
    assert normalize_capability_type("plugin") == "plugin"
    assert normalize_capability_type("unknown") == "other"
    assert extract_descriptor_type({"kind": "mcp_server"}) == "mcp_server"


def test_permission_and_risk_normalization() -> None:
    assert normalize_permission("read_file") == "filesystem_read"
    assert normalize_permission("write_file") == "filesystem_write"
    assert normalize_permission("shell") == "shell_execution"
    assert normalize_permission("network") == "network_access"
    assert normalize_permission("secrets") == "credential_access"
    assert normalize_permission("external_code") == "external_code_execution"
    assert normalize_risk_category("credentials") == "credential_access"
    assert normalize_risk_category("") == "unknown"


def test_risk_level_inference_and_name_extraction() -> None:
    assert infer_risk_level(["filesystem_write"]) == "medium"
    assert infer_risk_level(["network_access"]) == "medium"
    assert infer_risk_level(["shell_execution"]) == "high"
    assert infer_risk_level(["credential_access"]) == "high"
    assert infer_risk_level(["external_code_execution"]) == "critical"
    assert infer_risk_level(["data_exfiltration"]) == "critical"
    assert infer_risk_level(["unknown"]) == "unknown"
    assert extract_descriptor_name({"name": "x"}) == "x"
    assert extract_descriptor_name({}) == "unnamed_external_capability"
