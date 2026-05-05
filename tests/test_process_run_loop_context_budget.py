from __future__ import annotations

from dataclasses import dataclass, field

from chanta_core.context import ContextBudget
from chanta_core.llm.types import ChatMessage
from chanta_core.pig.context import PIGContext
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


@dataclass
class CapturingFakeLLMClient:
    settings: FakeLLMSettings = field(default_factory=FakeLLMSettings)
    received_messages: list[list[ChatMessage]] = field(default_factory=list)

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        self.received_messages.append(messages)
        return "budgeted response"


class FakePIGFeedbackService:
    def build_recent_context(self) -> PIGContext:
        return PIGContext(
            source="pig",
            scope="recent",
            process_instance_id="pi:loop-budget",
            session_id="session:loop-budget",
            activity_sequence=[],
            event_activity_counts={},
            object_type_counts={},
            relation_coverage={},
            basic_variant={},
            performance_summary={},
            guide={},
            diagnostics=[],
            recommendations=[],
            context_text="Process Intelligence Context:\n" + ("x" * 3000),
        )


def test_process_run_loop_compacts_long_pig_context_without_lm_studio() -> None:
    fake_llm = CapturingFakeLLMClient()
    loop = ProcessRunLoop(
        llm_client=fake_llm,
        pig_feedback_service=FakePIGFeedbackService(),
        policy=ProcessRunPolicy(
            include_pig_context=True,
            context_budget=ContextBudget(
                max_total_chars=1000,
                reserve_chars=100,
                max_pig_context_chars=300,
            ),
        ),
    )

    result = loop.run(
        process_instance_id="pi:loop-budget",
        session_id="session:loop-budget",
        agent_id="chanta_core_default",
        user_input="hello",
        system_prompt="system",
    )

    rendered = "\n".join(
        message["content"]
        for messages in fake_llm.received_messages
        for message in messages
    )
    assert result.status == "completed"
    assert "BudgetReductionLayer" in rendered
    assert "context_compaction" in result.result_attrs
    assert result.result_attrs["context_compaction"]["truncated_block_count"] >= 1
    assert len(rendered) < 900
