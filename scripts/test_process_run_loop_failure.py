from dataclasses import dataclass
import sys

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
        raise RuntimeError("fake LLM failure")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    store = OCELStore()
    loop = ProcessRunLoop(
        llm_client=FakeFailingLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(raise_on_failure=False),
    )
    result = loop.run(
        process_instance_id="process_instance:script-failure",
        session_id="script-session-loop-failure",
        agent_id="chanta_core_default",
        user_input="Demonstrate a failed ProcessRunLoop run.",
        system_prompt="You are a test agent.",
    )

    loader = OCPXLoader(store)
    view = loader.load_process_instance_view("process_instance:script-failure")
    engine = OCPXEngine()

    print("status:", result.status)
    print("observations:", [item.to_dict() for item in result.observations])
    print("activity_sequence:", engine.activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()
