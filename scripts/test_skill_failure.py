from __future__ import annotations

from dataclasses import dataclass

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


class FakeFailingLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        raise RuntimeError("fake skill failure")


def main() -> None:
    store = OCELStore()
    process_instance_id = "process_instance:script-skill-failure"
    session_id = "script-session-skill-failure"
    loop = ProcessRunLoop(
        llm_client=FakeFailingLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(raise_on_failure=False),
    )
    result = loop.run(
        process_instance_id=process_instance_id,
        session_id=session_id,
        agent_id="chanta_core_default",
        user_input="Trigger fake skill failure.",
        system_prompt="You are ChantaCore running a skill failure test.",
    )
    view = OCPXLoader(store).load_process_instance_view(process_instance_id)
    print("status:", result.status)
    print("observations:", [item.to_dict() for item in result.observations])
    print("activity_sequence:", OCPXEngine().activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()
