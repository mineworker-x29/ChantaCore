from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.pig.guidance import PIGGuidance
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy
from chanta_core.traces.trace_service import TraceService
from tests.test_ocel_store import make_record


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FailingFakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        raise AssertionError("This test should select a non-LLM skill")


class StaticGuidanceService:
    def __init__(self, guidance: list[PIGGuidance]) -> None:
        self._guidance = guidance

    def build_recent_guidance(self, limit: int = 20) -> list[PIGGuidance]:
        return self._guidance

    def build_process_instance_guidance(self, process_instance_id: str) -> list[PIGGuidance]:
        return self._guidance


def guidance(skill_id: str) -> PIGGuidance:
    return PIGGuidance(
        guidance_id=f"pig_guidance:{skill_id}",
        guidance_type="skill_bias",
        title="Bias selected skill",
        target_scope={},
        suggested_skill_id=skill_id,
        suggested_activity=None,
        score_delta=0.5,
        rationale="advisory",
        evidence_refs=[{"ref_type": "test", "ref_id": "test"}],
        confidence=0.8,
        status="active",
        guidance_attrs={"advisory": True, "hard_policy": False},
    )


def test_process_run_loop_uses_decision_service_for_trace_query(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_decision_trace.sqlite")
    store.append_record(make_record())
    loop = ProcessRunLoop(
        llm_client=FailingFakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )

    result = loop.run(
        process_instance_id="process_instance:decision-trace",
        session_id="session-decision-trace",
        agent_id="chanta_core_default",
        user_input="Please summarize the process trace history.",
    )

    activities = [event["event_activity"] for event in store.fetch_events_by_session("session-decision-trace")]
    assert result.status == "completed"
    assert result.result_attrs["selected_skill_id"] == "skill:summarize_process_trace"
    assert result.result_attrs["decision_mode"] in {"heuristic", "tie_break"}
    assert "decide_skill" in activities


def test_process_run_loop_guidance_biases_skill_selection(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_decision_guidance.sqlite")
    store.append_record(make_record())
    loop = ProcessRunLoop(
        llm_client=FailingFakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(use_pig_guidance=True),
        pig_guidance_service=StaticGuidanceService(
            [guidance("skill:inspect_ocel_recent")]
        ),
    )

    result = loop.run(
        process_instance_id="process_instance:decision-guidance",
        session_id="session-decision-guidance",
        agent_id="chanta_core_default",
        user_input="hello",
    )

    activities = [event["event_activity"] for event in store.fetch_events_by_session("session-decision-guidance")]
    assert result.status == "completed"
    assert result.result_attrs["selected_skill_id"] == "skill:inspect_ocel_recent"
    assert result.result_attrs["decision_mode"] == "guidance_bias"
    assert result.result_attrs["applied_guidance_ids"]
    assert "execute_skill" in activities
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True


def test_explicit_skill_id_overrides_guidance(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_decision_explicit.sqlite")
    loop = ProcessRunLoop(
        llm_client=FailingFakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(use_pig_guidance=True),
        pig_guidance_service=StaticGuidanceService(
            [guidance("skill:inspect_ocel_recent")]
        ),
    )

    result = loop.run(
        process_instance_id="process_instance:decision-explicit",
        session_id="session-decision-explicit",
        agent_id="chanta_core_default",
        user_input="trace relation",
        skill_id="skill:echo",
    )

    assert result.status == "completed"
    assert result.result_attrs["selected_skill_id"] == "skill:echo"
    assert result.result_attrs["decision_mode"] == "explicit"
    assert result.result_attrs["applied_guidance_ids"] == []
