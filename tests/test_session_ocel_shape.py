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
        return "shape response"


def test_session_ocel_shape_after_agent_runtime_run(tmp_path) -> None:
    store = OCELStore(tmp_path / "session_shape.sqlite")
    runtime = AgentRuntime(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )

    result = runtime.run("shape", session_id="session-shape")

    object_types = {
        object_type
        for object_type in [
            "session",
            "conversation_turn",
            "message",
            "process_instance",
        ]
        if store.fetch_objects_by_type(object_type)
    }
    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session(result.session_id)
    ]

    assert object_types == {
        "session",
        "conversation_turn",
        "message",
        "process_instance",
    }
    for activity in [
        "session_started",
        "conversation_turn_started",
        "user_message_received",
        "assistant_message_emitted",
        "conversation_turn_completed",
    ]:
        assert activity in activities
