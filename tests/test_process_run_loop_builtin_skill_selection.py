from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.runtime.loop import ProcessRunLoop
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
        return "fake llm"


def run_loop_with_skill(tmp_path, skill_id: str, suffix: str):
    store = OCELStore(tmp_path / f"{suffix}.sqlite")
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )
    result = loop.run(
        process_instance_id=f"process_instance:{suffix}",
        session_id=f"test-session-{suffix}",
        agent_id="chanta_core_default",
        user_input=f"{suffix} input",
        system_prompt="You are a test agent.",
        skill_id=skill_id,
    )
    return store, result


def test_process_run_loop_can_select_echo_skill(tmp_path) -> None:
    store, result = run_loop_with_skill(tmp_path, "skill:echo", "loop-echo")

    assert result.status == "completed"
    assert result.response_text == "loop-echo input"
    assert result.result_attrs["selected_skill_id"] == "skill:echo"
    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-loop-echo")
    ]
    assert "select_skill" in activities
    assert "execute_skill" in activities
    assert "call_llm" not in activities
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True


def test_process_run_loop_can_select_process_intelligence_skills(tmp_path) -> None:
    inspect_store, inspect_result = run_loop_with_skill(
        tmp_path,
        "skill:inspect_ocel_recent",
        "loop-inspect",
    )
    trace_store, trace_result = run_loop_with_skill(
        tmp_path,
        "skill:summarize_process_trace",
        "loop-trace",
    )

    assert inspect_result.status == "completed"
    assert inspect_result.response_text
    assert inspect_result.result_attrs["selected_skill_id"] == "skill:inspect_ocel_recent"
    assert trace_result.status == "completed"
    assert trace_result.response_text
    assert trace_result.result_attrs["selected_skill_id"] == "skill:summarize_process_trace"
    assert OCELValidator(inspect_store).validate_duplicate_relations()["valid"] is True
    assert OCELValidator(trace_store).validate_duplicate_relations()["valid"] is True
