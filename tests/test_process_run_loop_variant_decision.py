from __future__ import annotations

from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.pig.guidance import PIGGuidance
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy
from chanta_core.traces.trace_service import TraceService


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
        raise AssertionError("Variant decision tests should select non-LLM skills")


class StaticGuidanceService:
    def __init__(self, guidance: list[PIGGuidance]) -> None:
        self._guidance = guidance

    def build_recent_guidance(self, limit: int = 20) -> list[PIGGuidance]:
        return self._guidance


def variant_guidance() -> PIGGuidance:
    return PIGGuidance(
        guidance_id="pig_guidance:variant-failure",
        guidance_type="variant_skill_bias",
        title="Inspect trace for failure-prone variant",
        target_scope={
            "variant_key": "start_process_run_loop>fail_process_instance",
            "failure_count": 1,
            "success_count": 0,
            "similarity_basis": "activity_sequence",
        },
        suggested_skill_id="skill:inspect_ocel_recent",
        suggested_activity=None,
        score_delta=0.25,
        rationale="This variant includes failed executions.",
        evidence_refs=[
            {
                "ref_type": "variant",
                "ref_id": "start_process_run_loop>fail_process_instance",
                "attrs": {},
            }
        ],
        confidence=0.6,
        status="active",
        guidance_attrs={
            "variant_key": "start_process_run_loop>fail_process_instance",
            "advisory": True,
            "hard_policy": False,
        },
    )


def test_variant_guidance_biases_process_run_loop_selection(tmp_path) -> None:
    store = OCELStore(tmp_path / "variant_decision.sqlite")
    loop = ProcessRunLoop(
        llm_client=FailingFakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(use_pig_guidance=True),
        pig_guidance_service=StaticGuidanceService([variant_guidance()]),
    )

    result = loop.run(
        process_instance_id="process_instance:variant-decision",
        session_id="session-variant-decision",
        agent_id="chanta_core_default",
        user_input="hello",
    )
    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("session-variant-decision")
    ]

    assert result.status == "completed"
    assert result.result_attrs["selected_skill_id"] == "skill:inspect_ocel_recent"
    assert result.result_attrs["decision_mode"] == "guidance_bias"
    assert result.result_attrs["decision_attrs"]["boost_by_skill"] == {
        "skill:inspect_ocel_recent": 0.15
    }
    assert "select_skill" in activities
    assert "execute_skill" in activities
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True


def test_explicit_skill_overrides_variant_guidance(tmp_path) -> None:
    store = OCELStore(tmp_path / "variant_decision_explicit.sqlite")
    loop = ProcessRunLoop(
        llm_client=FailingFakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(use_pig_guidance=True),
        pig_guidance_service=StaticGuidanceService([variant_guidance()]),
    )

    result = loop.run(
        process_instance_id="process_instance:variant-explicit",
        session_id="session-variant-explicit",
        agent_id="chanta_core_default",
        user_input="hello",
        skill_id="skill:echo",
    )

    assert result.status == "completed"
    assert result.result_attrs["selected_skill_id"] == "skill:echo"
    assert result.result_attrs["decision_mode"] == "explicit"
    assert result.result_attrs["applied_guidance_ids"] == []
