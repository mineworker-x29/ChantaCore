from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
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

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        return "fake"


def test_check_self_conformance_skill_runs_without_llm(tmp_path) -> None:
    store = OCELStore(tmp_path / "self_conformance_skill.sqlite")
    trace_service = TraceService(ocel_store=store)
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )
    loop.run(
        process_instance_id="process_instance:self-conformance-skill",
        session_id="session-self-conformance-skill",
        agent_id="chanta_core_default",
        user_input="seed trace",
        system_prompt="You are a test agent.",
        skill_id="skill:echo",
    )
    executor = SkillExecutor(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )

    result = executor.execute(
        SkillRegistry().require("skill:check_self_conformance"),
        SkillExecutionContext(
            process_instance_id="process_instance:self-conformance-skill",
            session_id="session-check-self-conformance",
            agent_id="chanta_core_default",
            user_input="check self conformance",
            system_prompt=None,
            event_attrs={},
            context_attrs={
                "process_instance_id": "process_instance:self-conformance-skill"
            },
        ),
    )

    assert result.success is True
    assert result.output_text
    assert result.output_attrs["status"] in {
        "conformant",
        "warning",
        "nonconformant",
        "unknown",
    }
    assert isinstance(result.output_attrs["issues"], list)
    assert result.output_attrs["diagnostic_only"] is True
