from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.runtime.loop.context import ProcessContextAssembler
from chanta_core.skills.builtin import create_llm_chat_skill
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
from chanta_core.skills.skill import Skill
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
        return "Hello from skill executor."


def test_skill_executor_runs_builtin_llm_chat(tmp_path) -> None:
    store = OCELStore(tmp_path / "skill_executor.sqlite")
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        context_assembler=ProcessContextAssembler(),
        trace_service=TraceService(ocel_store=store),
    )
    result = executor.execute(
        create_llm_chat_skill(),
        SkillExecutionContext(
            process_instance_id="process_instance:skill-executor",
            session_id="test-session-skill-executor",
            agent_id="chanta_core_default",
            user_input="skill executor test",
            system_prompt="You are a test agent.",
            event_attrs={},
            context_attrs={"iteration": 0},
        ),
    )

    assert result.success is True
    assert result.output_text == "Hello from skill executor."
    assert result.output_attrs["execution_type"] == "llm"
    assert result.output_attrs["response_length"] == len("Hello from skill executor.")

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-skill-executor")
    ]
    assert activities == ["assemble_context", "call_llm", "receive_llm_response"]


def test_skill_executor_returns_failed_result_for_unsupported_skill(tmp_path) -> None:
    store = OCELStore(tmp_path / "unsupported.sqlite")
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )
    result = executor.execute(
        Skill(
            skill_id="skill:unsupported",
            skill_name="unsupported",
            description="Unsupported test skill.",
            execution_type="unsupported",
            input_schema={},
            output_schema={},
            tags=["test"],
            skill_attrs={},
        ),
        SkillExecutionContext(
            process_instance_id="process_instance:unsupported",
            session_id="test-session-unsupported",
            agent_id="chanta_core_default",
            user_input="unsupported",
            system_prompt=None,
            event_attrs={},
            context_attrs={},
        ),
    )

    assert result.success is False
    assert result.output_text is None
    assert result.output_attrs["failure_stage"] == "skill_dispatch"
    assert result.output_attrs["exception_type"] == "UnsupportedSkillExecution"
    assert "Unsupported skill execution_type" in str(result.error)

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-unsupported")
    ]
    assert activities == ["fail_skill_execution"]
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
