from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
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


def skill_context(name: str) -> SkillExecutionContext:
    return SkillExecutionContext(
        process_instance_id=f"process_instance:{name}",
        session_id=f"session-{name}",
        agent_id="chanta_core_default",
        user_input=f"{name} text",
        system_prompt=None,
        event_attrs={},
        context_attrs={},
    )


def test_echo_skill_uses_tool_echo(tmp_path) -> None:
    store = OCELStore(tmp_path / "echo_skill_tool.sqlite")
    trace_service = TraceService(ocel_store=store)
    executor = SkillExecutor(llm_client=FakeLLMClient(), trace_service=trace_service)

    result = executor.execute(SkillRegistry().require("skill:echo"), skill_context("echo-tool"))

    assert result.success is True
    assert result.output_attrs["tool_result"]["tool_id"] == "tool:echo"
    assert "create_tool_request" in [
        event["event_activity"] for event in store.fetch_events_by_session("session-echo-tool")
    ]


def test_inspect_ocel_recent_skill_uses_tool_ocel(tmp_path) -> None:
    store = OCELStore(tmp_path / "inspect_skill_tool.sqlite")
    trace_service = TraceService(ocel_store=store)
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )
    loop.run(
        process_instance_id="process_instance:inspect-seed",
        session_id="session-inspect-seed",
        agent_id="chanta_core_default",
        user_input="seed",
        skill_id="skill:echo",
    )
    executor = SkillExecutor(llm_client=FakeLLMClient(), trace_service=trace_service)

    result = executor.execute(
        SkillRegistry().require("skill:inspect_ocel_recent"),
        skill_context("inspect-tool"),
    )

    assert result.success is True
    assert "inspection_scope=recent_global" in str(result.output_text)
    assert result.output_attrs["inspection_scope"] == "recent_global"
    assert result.output_attrs["persistence_scope"] == "persisted_store"
    assert result.output_attrs["tool_results"]
    assert {item["tool_id"] for item in result.output_attrs["tool_results"]} == {"tool:ocel"}
    activities = [
        event["event_activity"] for event in store.fetch_events_by_session("session-inspect-tool")
    ]
    assert "create_tool_request" in activities
    assert "complete_tool_operation" in activities
    assert store.fetch_objects_by_type("tool")
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
