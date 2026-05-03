from __future__ import annotations

from dataclasses import dataclass, field

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy
from chanta_core.traces.trace_service import TraceService
from tests.test_ocel_store import make_record


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


@dataclass
class CapturingFakeLLMClient:
    settings: FakeLLMSettings = field(default_factory=FakeLLMSettings)
    received_messages: list[list[ChatMessage]] = field(default_factory=list)

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        self.received_messages.append(messages)
        return "Hello with optional PIG context."


def test_process_run_loop_injects_pig_context_when_enabled(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_pig_enabled.sqlite")
    store.append_record(make_record())
    fake_llm = CapturingFakeLLMClient()
    loop = ProcessRunLoop(
        llm_client=fake_llm,
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(include_pig_context=True),
    )

    result = loop.run(
        process_instance_id="process_instance:pig-loop",
        session_id="test-session-pig-loop",
        agent_id="chanta_core_default",
        user_input="loop test",
        system_prompt="You are a test agent.",
    )

    assert result.status == "completed"
    assert result.result_attrs["pig_context_included"] is True
    assert any(
        "Process Intelligence Context" in message["content"]
        for messages in fake_llm.received_messages
        for message in messages
    )
    assert store.fetch_event_count() > 0
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True


def test_process_run_loop_does_not_inject_pig_context_by_default(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_pig_default_off.sqlite")
    store.append_record(make_record())
    fake_llm = CapturingFakeLLMClient()
    loop = ProcessRunLoop(
        llm_client=fake_llm,
        trace_service=TraceService(ocel_store=store),
    )

    result = loop.run(
        process_instance_id="process_instance:pig-loop-default",
        session_id="test-session-pig-loop-default",
        agent_id="chanta_core_default",
        user_input="loop test",
        system_prompt="You are a test agent.",
    )

    assert result.status == "completed"
    assert "pig_context_included" not in result.result_attrs
    assert not any(
        "Process Intelligence Context" in message["content"]
        for messages in fake_llm.received_messages
        for message in messages
    )
