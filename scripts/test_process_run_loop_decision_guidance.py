from __future__ import annotations

from dataclasses import dataclass

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

    def chat_messages(self, messages, temperature: float = 0.7, max_tokens: int = 384) -> str:
        return "Fake LLM fallback response."


def main() -> None:
    store = OCELStore()
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )
    result = loop.run(
        process_instance_id="process_instance:script-decision-guidance",
        session_id="script-session-decision-guidance",
        agent_id="chanta_core_default",
        user_input="Please summarize the process trace history.",
    )
    view = OCPXLoader(store).load_process_instance_view(result.process_instance_id)

    print("selected_skill_id:", result.result_attrs.get("selected_skill_id"))
    print("decision_mode:", result.result_attrs.get("decision_mode"))
    print("applied_guidance_ids:", result.result_attrs.get("applied_guidance_ids"))
    print("activity_sequence:", OCPXEngine().activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()
