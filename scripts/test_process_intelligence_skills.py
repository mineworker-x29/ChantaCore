from __future__ import annotations

from dataclasses import dataclass

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.runtime.loop import ProcessRunLoop
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry
from chanta_core.traces.trace_service import TraceService


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(self, messages, temperature: float = 0.7, max_tokens: int = 384) -> str:
        return "Fake LLM response."


def main() -> None:
    store = OCELStore()
    trace_service = TraceService(ocel_store=store)
    loop = ProcessRunLoop(llm_client=FakeLLMClient(), trace_service=trace_service)
    loop_result = loop.run(
        process_instance_id="process_instance:script-pi-skills",
        session_id="script-session-pi-skills",
        agent_id="chanta_core_default",
        user_input="Create a deterministic trace for PI skill inspection.",
        skill_id="skill:echo",
    )

    registry = SkillRegistry()
    registry.register_builtin_skills()
    executor = SkillExecutor(llm_client=FakeLLMClient(), trace_service=trace_service)
    context = SkillExecutionContext(
        process_instance_id=loop_result.process_instance_id,
        session_id=loop_result.session_id,
        agent_id=loop_result.agent_id,
        user_input="Inspect the current ChantaCore process trace.",
        system_prompt=None,
        event_attrs={},
        context_attrs={"process_instance_id": loop_result.process_instance_id},
    )

    inspect_result = executor.execute(registry.require("inspect_ocel_recent"), context)
    summary_result = executor.execute(registry.require("summarize_process_trace"), context)
    view = OCPXLoader(store).load_process_instance_view(loop_result.process_instance_id)

    print("inspect_ocel_recent:", inspect_result.output_attrs)
    print("summarize_process_trace:", summary_result.output_attrs)
    print("activity_sequence:", OCPXEngine().activity_sequence(view))
    print("duplicate_relations:", OCELValidator(store).validate_duplicate_relations())


if __name__ == "__main__":
    main()
