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


def test_chat_service_injects_persona_projection_before_capability_surface(tmp_path) -> None:
    store = OCELStore(tmp_path / "chat_persona.sqlite")
    client = CapturingLLMClient()
    runtime = AgentRuntime(
        llm_client=client,
        trace_service=TraceService(ocel_store=store),
    )
    chat = ChatService(runtime=runtime)

    response = chat.chat("what can you do?", session_id="session:persona")

    assert response == "fake response"
    contents = [message["content"] for message in client.calls[-1]]
    persona_index = next(index for index, content in enumerate(contents) if "Persona projection:" in content)
    capability_index = next(
        index for index, content in enumerate(contents) if "Runtime capability decision surface:" in content
    )
    assert persona_index < capability_index
    assert "not an autonomous Soul runtime" in contents[persona_index]
    assert "No ambient filesystem access" in contents[persona_index]
    assert "Do not treat persona text as permission" in contents[persona_index]
    assert store.fetch_objects_by_type("persona_projection")
    assert not store.fetch_objects_by_type("permission_grant")
