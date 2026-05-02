from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.runtime.loop.context import ProcessContextAssembler
from chanta_core.skills.builtin import create_llm_chat_skill
from chanta_core.skills.context import SkillExecutionContext
from chanta_core.skills.executor import SkillExecutor
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
        raise RuntimeError("fake skill failure")


def test_skill_executor_normalizes_failing_llm_skill(tmp_path) -> None:
    store = OCELStore(tmp_path / "skill_executor_failure.sqlite")
    executor = SkillExecutor(
        llm_client=FakeFailingLLMClient(),
        context_assembler=ProcessContextAssembler(),
        trace_service=TraceService(ocel_store=store),
    )

    result = executor.execute(
        create_llm_chat_skill(),
        SkillExecutionContext(
            process_instance_id="process_instance:skill-executor-failure",
            session_id="test-session-skill-executor-failure",
            agent_id="chanta_core_default",
            user_input="skill executor failure test",
            system_prompt="You are a test agent.",
            event_attrs={},
            context_attrs={"iteration": 0},
        ),
    )

    assert result.success is False
    assert result.output_text is None
    assert "fake skill failure" in str(result.error)
    assert result.output_attrs["exception_type"] == "RuntimeError"
    assert result.output_attrs["failure_stage"] == "call_llm"
    assert result.output_attrs["skill_id"] == "skill:llm_chat"

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-skill-executor-failure")
    ]
    assert activities == ["assemble_context", "call_llm", "fail_skill_execution"]
    assert store.fetch_objects_by_type("error")
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
