from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.traces.trace_service import TraceService


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        return "session runtime response"


def test_agent_runtime_records_session_turn_and_messages(tmp_path) -> None:
    store = OCELStore(tmp_path / "agent_runtime_session.sqlite")
    runtime = AgentRuntime(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )

    result = runtime.run("hello session", session_id="runtime-session")

    assert result.response_text == "session runtime response"
    assert result.metadata["turn_id"].startswith("conversation_turn:")
    assert result.metadata["user_message_id"].startswith("message:")
    assert result.metadata["assistant_message_id"].startswith("message:")

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("runtime-session")
    ]
    assert "session_started" in activities
    assert "conversation_turn_started" in activities
    assert "user_message_received" in activities
    assert "assistant_message_emitted" in activities
    assert "conversation_turn_completed" in activities
