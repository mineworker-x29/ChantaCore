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


def test_run_scheduler_once_skill_returns_result(tmp_path) -> None:
    result = SkillExecutor(llm_client=FakeLLMClient()).execute(
        SkillRegistry().require("skill:run_scheduler_once"),
        SkillExecutionContext(
            process_instance_id="process_instance:scheduler-skill",
            session_id="session-scheduler-skill",
            agent_id="chanta_core_default",
            user_input="run scheduler once",
            system_prompt=None,
            context_attrs={
                "process_schedule_store_path": str(tmp_path / "schedules.jsonl"),
                "process_job_store_path": str(tmp_path / "jobs.jsonl"),
            },
        ),
    )

    assert result.success is True
    assert result.output_attrs["summary"]["enqueued_count"] == 0
