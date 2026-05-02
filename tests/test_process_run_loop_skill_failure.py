from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.service import PIGService
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy
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
        raise RuntimeError("fake loop skill failure")


def test_process_run_loop_records_skill_and_process_failure(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_skill_failure.sqlite")
    loop = ProcessRunLoop(
        llm_client=FakeFailingLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(raise_on_failure=False),
    )

    result = loop.run(
        process_instance_id="process_instance:test-loop-skill-failure",
        session_id="test-session-loop-skill-failure",
        agent_id="chanta_core_default",
        user_input="loop skill failure test",
        system_prompt="You are a test agent.",
    )

    assert result.status == "failed"
    assert result.observations[-1].success is False
    assert result.observations[-1].output_attrs["skill_id"] == "skill:llm_chat"
    assert result.observations[-1].output_attrs["failure_stage"] == "call_llm"

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-loop-skill-failure")
    ]
    assert activities == [
        "start_process_run_loop",
        "decide_next_activity",
        "select_skill",
        "execute_skill",
        "assemble_context",
        "call_llm",
        "fail_skill_execution",
        "observe_result",
        "fail_process_instance",
    ]
    assert store.fetch_objects_by_type("error")
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True

    loader = OCPXLoader(store)
    view = loader.load_process_instance_view("process_instance:test-loop-skill-failure")
    assert "fail_skill_execution" in [event.event_activity for event in view.events]

    pig_result = PIGService(loader=loader).analyze_recent(limit=20)
    assert "graph" in pig_result
