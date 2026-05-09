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


def test_chat_service_injects_capability_decision_guidance_without_execution(tmp_path) -> None:
    store = OCELStore(tmp_path / "chat_capability.sqlite")
    client = CapturingLLMClient()
    runtime = AgentRuntime(
        llm_client=client,
        trace_service=TraceService(ocel_store=store),
    )
    chat = ChatService(runtime=runtime)

    response = chat.chat(
        "/PersonalDirectory/sample_profile.md read markdown",
        session_id="session:test",
    )

    assert response == "fake response"
    prompt_text = "\n".join(message["content"] for message in client.calls[-1])
    assert "Runtime capability decision surface:" in prompt_text
    assert "workspace file read -> requires_explicit_skill" in prompt_text
    assert "Do not execute tools" in prompt_text
    assert store.fetch_objects_by_type("capability_decision_surface")
    assert not store.fetch_objects_by_type("permission_grant")

