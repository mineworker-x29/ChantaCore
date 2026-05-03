from __future__ import annotations

from dataclasses import dataclass

from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(self, messages, temperature: float = 0.7, max_tokens: int = 384) -> str:
        raise RuntimeError("PI skills should not call LLM")


def main() -> None:
    registry = SkillRegistry()
    executor = SkillExecutor(llm_client=FakeLLMClient())
    context = SkillExecutionContext(
        process_instance_id="process_instance:script-pi-artifacts",
        session_id="script-session-pi-artifacts",
        agent_id="chanta_core_default",
        user_input="Human PI: repeated failed skill execution should be reviewed.",
        system_prompt=None,
        context_attrs={"artifact_type": "diagnostic", "confidence": 0.7},
    )
    ingest_result = executor.execute(registry.require("skill:ingest_human_pi"), context)
    summary_context = SkillExecutionContext(
        process_instance_id=context.process_instance_id,
        session_id=context.session_id,
        agent_id=context.agent_id,
        user_input="summarize",
        system_prompt=None,
        context_attrs={},
    )
    summary_result = executor.execute(
        registry.require("skill:summarize_pi_artifacts"),
        summary_context,
    )

    print("ingest_human_pi:", ingest_result.to_dict())
    print("summarize_pi_artifacts:", summary_result.to_dict())


if __name__ == "__main__":
    main()
