from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.pig.context import PIGContext
from chanta_core.pig.feedback import PIGFeedbackService
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

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        return "fake"


def test_process_intelligence_skills_read_ocel_ocpx_pig_without_llm(tmp_path) -> None:
    assert PIGContext is not None
    assert PIGFeedbackService is not None

    store = OCELStore(tmp_path / "pi_skills.sqlite")
    trace_service = TraceService(ocel_store=store)
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )
    loop.run(
        process_instance_id="process_instance:pi-skill-trace",
        session_id="test-session-pi-skill-trace",
        agent_id="chanta_core_default",
        user_input="trace seed",
        system_prompt="You are a test agent.",
        skill_id="skill:echo",
    )
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )
    registry = SkillRegistry()

    base_context = SkillExecutionContext(
        process_instance_id="process_instance:pi-skill-trace",
        session_id="test-session-pi-skill-run",
        agent_id="chanta_core_default",
        user_input="inspect",
        system_prompt=None,
        event_attrs={},
        context_attrs={"process_instance_id": "process_instance:pi-skill-trace"},
    )
    inspect_result = executor.execute(
        registry.require("skill:inspect_ocel_recent"),
        base_context,
    )
    trace_result = executor.execute(
        registry.require("skill:summarize_process_trace"),
        base_context,
    )

    assert inspect_result.success is True
    assert inspect_result.output_text
    assert inspect_result.output_attrs["event_count"] > 0
    assert "recent_event_activities" in inspect_result.output_attrs
    assert inspect_result.output_attrs["duplicate_relations_valid"] is True

    assert trace_result.success is True
    assert trace_result.output_text
    assert trace_result.output_attrs["event_count"] > 0
    assert trace_result.output_attrs["object_count"] > 0
    assert trace_result.output_attrs["activity_sequence"]
    assert "guide" in trace_result.output_attrs
    assert "diagnostics" in trace_result.output_attrs
    assert "recommendations" in trace_result.output_attrs
