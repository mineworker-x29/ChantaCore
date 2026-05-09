from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.runtime.chat_service import ChatService
from chanta_core.traces.trace_service import TraceService


class CapturingLLMClient:
    settings = type("Settings", (), {"provider": "fake", "model": "fake-model"})()

    def __init__(self) -> None:
        self.calls: list[list[dict[str, str]]] = []

    def chat_messages(self, *, messages, temperature, max_tokens):
        self.calls.append(messages)
        return "fake response"


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_chat_service_personal_overlay_absent_is_noop(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "chat_personal_overlay_absent.sqlite")
    client = CapturingLLMClient()
    runtime = AgentRuntime(
        llm_client=client,
        trace_service=TraceService(ocel_store=store),
    )
    chat = ChatService(runtime=runtime)

    response = chat.chat("hello", session_id="session:personal-overlay-absent")
    prompt_text = "\n".join(message["content"] for message in client.calls[-1])

    assert response == "fake response"
    assert "Personal Overlay projection:" not in prompt_text
    assert not store.fetch_objects_by_type("personal_directory_manifest")


def test_chat_service_attaches_personal_overlay_when_env_is_safe(monkeypatch, tmp_path) -> None:
    root = tmp_path / "dummy_personal_directory"
    _write(root / "source" / "identity.md", "source body must stay out")
    _write(root / "overlay" / "core.md", "overlay prompt block")
    _write(root / "letters" / "note.md", "letter body must stay out")
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(root))
    store = OCELStore(tmp_path / "chat_personal_overlay.sqlite")
    client = CapturingLLMClient()
    runtime = AgentRuntime(
        llm_client=client,
        trace_service=TraceService(ocel_store=store),
        personal_overlay_public_repo_root=tmp_path / "public_repo",
    )
    chat = ChatService(runtime=runtime)

    response = chat.chat("hello", session_id="session:personal-overlay")
    prompt_text = "\n".join(message["content"] for message in client.calls[-1])

    assert response == "fake response"
    assert "Personal Overlay projection:" in prompt_text
    assert "overlay prompt block" in prompt_text
    assert "source body must stay out" not in prompt_text
    assert "letter body must stay out" not in prompt_text
    assert store.fetch_objects_by_type("personal_overlay_load_result")
    assert not store.fetch_objects_by_type("permission_grant")


def test_chat_service_denies_personal_overlay_when_boundary_fails(monkeypatch, tmp_path) -> None:
    public_repo = tmp_path / "public_repo"
    root = public_repo / "local_personal_directory"
    _write(root / "overlay" / "core.md", "overlay prompt block")
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(root))
    store = OCELStore(tmp_path / "chat_personal_overlay_denied.sqlite")
    client = CapturingLLMClient()
    runtime = AgentRuntime(
        llm_client=client,
        trace_service=TraceService(ocel_store=store),
        personal_overlay_public_repo_root=public_repo,
    )
    chat = ChatService(runtime=runtime)

    response = chat.chat("hello", session_id="session:personal-overlay-denied")
    prompt_text = "\n".join(message["content"] for message in client.calls[-1])

    assert response == "fake response"
    assert "Personal Overlay projection:" not in prompt_text
    assert "overlay prompt block" not in prompt_text
    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert "personal_overlay_load_denied" in activities




