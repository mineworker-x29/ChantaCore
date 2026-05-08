from chanta_core.capabilities import CapabilityDecisionSurfaceService


def _operation(prompt: str) -> str:
    service = CapabilityDecisionSurfaceService()
    return service.create_request_intent(prompt).requested_operation


def test_extracts_workspace_file_read() -> None:
    assert _operation("/Souls/ChantaVeraAide markdown 파일 읽어") == "workspace_file_read"


def test_extracts_shell_network_mcp_plugin() -> None:
    assert _operation("powershell 명령어 실행") == "shell_execution"
    assert _operation("https://example.com 호출") == "network_access"
    assert _operation("MCP 연결해줘") == "mcp_connection"
    assert _operation("plugin 로딩해줘") == "plugin_loading"


def test_extracts_external_and_session_context() -> None:
    assert _operation("external OCEL import candidate 등록") == "external_ocel_import"
    assert _operation("방금 이전 대화 기준으로 답해줘") == "session_context"
    assert _operation("넌 뭘 할 수 있어?") == "chat"
