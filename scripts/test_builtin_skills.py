from __future__ import annotations

from dataclasses import dataclass

from chanta_core.ocel.store import OCELStore
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
        return "Fake LLM summary."


def main() -> None:
    store = OCELStore()
    trace_service = TraceService(ocel_store=store)
    executor = SkillExecutor(llm_client=FakeLLMClient(), trace_service=trace_service)
    registry = SkillRegistry()
    registry.register_builtin_skills()

    loop = ProcessRunLoop(llm_client=FakeLLMClient(), trace_service=trace_service)
    seeded = loop.run(
        process_instance_id="process_instance:script-builtin-seed",
        session_id="script-session-builtin-seed",
        agent_id="chanta_core_default",
        user_input="Seed a trace for built-in skill inspection.",
        skill_id="skill:echo",
    )

    context = SkillExecutionContext(
        process_instance_id=seeded.process_instance_id,
        session_id=seeded.session_id,
        agent_id=seeded.agent_id,
        user_input="Summarize this short text.",
        system_prompt=None,
        event_attrs={},
        context_attrs={"process_instance_id": seeded.process_instance_id},
    )

    for skill_name in [
        "echo",
        "summarize_text",
        "inspect_ocel_recent",
        "summarize_process_trace",
    ]:
        skill = registry.require(skill_name)
        result = executor.execute(skill, context)
        print(skill.skill_id, "success:", result.success)
        print("output:", result.output_text)

    view = OCPXLoader(store).load_process_instance_view(seeded.process_instance_id)
    print("activity_sequence:", OCPXEngine().activity_sequence(view))


if __name__ == "__main__":
    main()
