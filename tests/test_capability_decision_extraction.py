from chanta_core.capabilities import CapabilityDecisionSurfaceService


def _operation(prompt: str) -> str:
    service = CapabilityDecisionSurfaceService()
    return service.create_request_intent(prompt).requested_operation


def test_extracts_workspace_file_read() -> None:
    assert _operation("/PersonalDirectory/sample_profile.md read markdown") == "workspace_file_read"


def test_extracts_shell_network_mcp_plugin() -> None:
    assert _operation("run powershell command") == "shell_execution"
    assert _operation("call https://example.com") == "network_access"
    assert _operation("connect MCP server") == "mcp_connection"
    assert _operation("load plugin") == "plugin_loading"


def test_extracts_external_and_session_context() -> None:
    assert _operation("external OCEL import candidate") == "external_ocel_import"
    assert _operation("summarize previous conversation") == "session_context"
    assert _operation("what can you do") == "chat"

