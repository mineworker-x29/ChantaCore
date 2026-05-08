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
        return f"assistant response {len(self.calls)}"


def test_chat_service_projects_same_session_prior_turns(tmp_path) -> None:
    client = CapturingLLMClient()
    trace_service = TraceService(ocel_store=OCELStore(tmp_path / "ocel.sqlite"))
    runtime = AgentRuntime(llm_client=client, trace_service=trace_service)
    chat = ChatService(runtime=runtime)

    assert chat.chat("first question", session_id="session:test") == "assistant response 1"
    assert chat.chat("second question", session_id="session:test") == "assistant response 2"

    second_call = client.calls[-1]
    contents = [message["content"] for message in second_call]
    assert "first question" in contents
    assert "assistant response 1" in contents
    assert contents.count("second question") == 1
    assert all(message["role"] in {"system", "user", "assistant"} for message in second_call)


def test_chat_service_does_not_project_different_session_messages(tmp_path) -> None:
    client = CapturingLLMClient()
    trace_service = TraceService(ocel_store=OCELStore(tmp_path / "ocel.sqlite"))
    runtime = AgentRuntime(llm_client=client, trace_service=trace_service)
    chat = ChatService(runtime=runtime)

    chat.chat("first session question", session_id="session:one")
    chat.chat("second session question", session_id="session:two")

    second_session_call = client.calls[-1]
    contents = [message["content"] for message in second_session_call]
    assert "first session question" not in contents
    assert contents.count("second session question") == 1
