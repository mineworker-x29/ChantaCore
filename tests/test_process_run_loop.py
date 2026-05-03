from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.pig.context import PIGContext
from chanta_core.pig.feedback import PIGFeedbackService
from chanta_core.runtime.loop import ProcessRunLoop
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
        return "Hello from loop."


def test_process_run_loop_records_bounded_loop_shape(tmp_path) -> None:
    assert PIGContext is not None
    assert PIGFeedbackService is not None

    store = OCELStore(tmp_path / "loop.sqlite")
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )

    result = loop.run(
        process_instance_id="process_instance:test-loop",
        session_id="test-session-loop",
        agent_id="chanta_core_default",
        user_input="loop test",
        system_prompt="You are a test agent.",
    )

    assert result.status == "completed"
    assert result.response_text == "Hello from loop."
    assert len(result.observations) == 1
    assert result.observations[0].success is True

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-loop")
    ]
    assert activities == [
        "start_process_run_loop",
        "decide_next_activity",
        "select_skill",
        "execute_skill",
        "assemble_context",
        "call_llm",
        "receive_llm_response",
        "observe_result",
        "record_outcome",
        "complete_process_instance",
    ]
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
