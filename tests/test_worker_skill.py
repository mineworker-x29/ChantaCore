from dataclasses import dataclass

from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.registry import SkillRegistry


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake"
    model: str = "fake"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(self, *_args, **_kwargs) -> str:
        return "unused"


def test_run_worker_once_skill_returns_result() -> None:
    result = SkillExecutor(llm_client=FakeLLMClient()).execute(
        SkillRegistry().require("skill:run_worker_once"),
        SkillExecutionContext(
            process_instance_id="process_instance:worker-skill",
            session_id="session-worker-skill",
            agent_id="chanta_core_default",
            user_input="run worker once",
            system_prompt=None,
        ),
    )

    assert result.success is True
    assert result.output_attrs["run_once"]["status"] == "idle"
