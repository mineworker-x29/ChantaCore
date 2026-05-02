from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
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
        return "Hello from ChantaCore skill dispatch."


def main() -> None:
    store = OCELStore()
    process_instance_id = "process_instance:script-skill-dispatch"
    session_id = "script-session-skill-dispatch"
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )
    result = loop.run(
        process_instance_id=process_instance_id,
        session_id=session_id,
        agent_id="chanta_core_default",
        user_input="Say hello through the skill dispatch runtime.",
        system_prompt="You are ChantaCore running a skill dispatch test.",
    )

    loader = OCPXLoader(store)
    view = loader.load_process_instance_view(process_instance_id)
    engine = OCPXEngine()

    print("response_text:", result.response_text)
    print("process_instance_id:", process_instance_id)
    print("selected_skill_id:", result.result_attrs.get("selected_skill_id"))
    print("activity_sequence:", engine.activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()
