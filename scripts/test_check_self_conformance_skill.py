from __future__ import annotations

from dataclasses import dataclass

from chanta_core.ocel.store import OCELStore
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
    result = loop.run(
        process_instance_id="process_instance:script-self-conformance",
        session_id="script-session-self-conformance",
        agent_id="chanta_core_default",
        user_input="Create a trace for self-conformance inspection.",
        skill_id="skill:echo",
    )

    executor = SkillExecutor(llm_client=FakeLLMClient(), trace_service=trace_service)
    context = SkillExecutionContext(
        process_instance_id=result.process_instance_id,
        session_id=result.session_id,
        agent_id=result.agent_id,
        user_input="Check self conformance.",
        system_prompt=None,
        event_attrs={},
        context_attrs={"process_instance_id": result.process_instance_id},
    )
    skill_result = executor.execute(
        SkillRegistry().require("skill:check_self_conformance"),
        context,
    )

    print(skill_result.output_text)
    print("output_attrs:", skill_result.output_attrs)


if __name__ == "__main__":
    main()
