from __future__ import annotations

from dataclasses import dataclass, field

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy
from chanta_core.traces.trace_service import TraceService


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


@dataclass
class FakeLLMClient:
    settings: FakeLLMSettings = field(default_factory=FakeLLMSettings)
    received_messages: list[list[ChatMessage]] = field(default_factory=list)

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        self.received_messages.append(messages)
        return "Fake LLM response with optional PIG context."


def main() -> None:
    store = OCELStore()
    fake_llm = FakeLLMClient()
    trace_service = TraceService(ocel_store=store)
    loop = ProcessRunLoop(
        llm_client=fake_llm,
        trace_service=trace_service,
        policy=ProcessRunPolicy(include_pig_context=True),
    )
    result = loop.run(
        process_instance_id="process_instance:script-pig-context",
        session_id="script-session-pig-context",
        agent_id="chanta_core_default",
        user_input="Run a fake LLM loop with PIG context.",
        system_prompt="You are a test agent.",
    )
    view = OCPXLoader(store).load_process_instance_view(result.process_instance_id)
    injected = any(
        "Process Intelligence Context" in message["content"]
        for messages in fake_llm.received_messages
        for message in messages
    )

    print("response:", result.response_text)
    print("pig_context_injected:", injected)
    print("activity_sequence:", OCPXEngine().activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()
