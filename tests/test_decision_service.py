from chanta_core.pig.guidance import PIGGuidance
from chanta_core.runtime.decision.context import DecisionContext
from chanta_core.runtime.decision.policy import DecisionPolicy
from chanta_core.runtime.decision.service import DecisionService
from chanta_core.skills.registry import SkillRegistry


def context(
    user_input: str,
    *,
    explicit_skill_id: str | None = None,
    guidance: list[PIGGuidance] | None = None,
) -> DecisionContext:
    registry = SkillRegistry()
    return DecisionContext(
        process_instance_id="process_instance:test",
        session_id="session-test",
        agent_id="chanta_core_default",
        user_input=user_input,
        available_skill_ids=[skill.skill_id for skill in registry.list_skills()],
        explicit_skill_id=explicit_skill_id,
        pig_guidance=guidance or [],
        context_attrs={},
    )


def guidance(skill_id: str, score_delta: float = 0.5, confidence: float = 0.8) -> PIGGuidance:
    return PIGGuidance(
        guidance_id=f"pig_guidance:{skill_id}",
        guidance_type="skill_bias",
        title="Bias skill",
        target_scope={},
        suggested_skill_id=skill_id,
        suggested_activity=None,
        score_delta=score_delta,
        rationale="advisory",
        evidence_refs=[],
        confidence=confidence,
        status="active",
        guidance_attrs={"advisory": True, "hard_policy": False},
    )


def service() -> DecisionService:
    return DecisionService(skill_registry=SkillRegistry())


def service_with_policy(policy: DecisionPolicy) -> DecisionService:
    return DecisionService(skill_registry=SkillRegistry(), policy=policy)


def test_explicit_skill_wins() -> None:
    decision = service().decide_skill(
        context(
            "trace relation",
            explicit_skill_id="skill:echo",
            guidance=[guidance("skill:inspect_ocel_recent")],
        )
    )

    assert decision.selected_skill_id == "skill:echo"
    assert decision.decision_mode == "explicit"
    assert decision.applied_guidance_ids == []


def test_trace_query_selects_trace_summary() -> None:
    decision = service().decide_skill(context("please review trace history"))

    assert decision.selected_skill_id == "skill:summarize_process_trace"


def test_ocel_query_selects_ocel_inspection() -> None:
    decision = service().decide_skill(context("inspect event object relation coverage"))

    assert decision.selected_skill_id == "skill:inspect_ocel_recent"


def test_echo_query_selects_echo() -> None:
    decision = service().decide_skill(context("echo this"))

    assert decision.selected_skill_id == "skill:echo"


def test_guidance_can_bias_selected_skill() -> None:
    decision = service().decide_skill(
        context("hello", guidance=[guidance("skill:inspect_ocel_recent")])
    )

    assert decision.selected_skill_id == "skill:inspect_ocel_recent"
    assert decision.decision_mode == "guidance_bias"
    assert decision.applied_guidance_ids


def test_fallback_selects_llm_chat() -> None:
    decision = service().decide_skill(context("hello"))

    assert decision.selected_skill_id == "skill:llm_chat"
    assert decision.decision_mode == "fallback"
    assert decision.decision_attrs["fallback_used"] is True


def test_decision_is_deterministic() -> None:
    decision_a = service().decide_skill(context("please review trace history"))
    decision_b = service().decide_skill(context("please review trace history"))

    assert decision_a.selected_skill_id == decision_b.selected_skill_id
    assert decision_a.final_scores == decision_b.final_scores
    assert decision_a.to_dict() == decision_b.to_dict()


def test_low_confidence_guidance_is_ignored() -> None:
    decision = service().decide_skill(
        context("hello", guidance=[guidance("skill:inspect_ocel_recent", confidence=0.2)])
    )

    assert decision.selected_skill_id == "skill:llm_chat"
    assert decision.decision_attrs["ignored_guidance"][0]["reason"] == (
        "confidence_below_threshold"
    )


def test_unavailable_skill_guidance_is_ignored() -> None:
    decision = service().decide_skill(
        context("hello", guidance=[guidance("skill:not_available")])
    )

    assert decision.decision_attrs["ignored_guidance"][0]["reason"] == "skill_not_available"


def test_guidance_boost_is_capped_per_skill() -> None:
    decision = service_with_policy(
        DecisionPolicy(max_guidance_boost_per_skill=0.1)
    ).decide_skill(
        context(
            "hello",
            guidance=[
                guidance("skill:inspect_ocel_recent", score_delta=1.0),
                guidance("skill:inspect_ocel_recent", score_delta=1.0),
            ],
        )
    )

    assert decision.decision_attrs["boost_by_skill"] == {
        "skill:inspect_ocel_recent": 0.1
    }
    assert decision.decision_attrs["capped_skills"] == ["skill:inspect_ocel_recent"]


def test_tie_break_is_deterministic() -> None:
    decision = service_with_policy(
        DecisionPolicy(
            tie_break_order=["skill:summarize_process_trace", "skill:llm_chat"]
        )
    ).decide_skill(
        context(
            "hello",
            guidance=[guidance("skill:summarize_process_trace", score_delta=0.125)],
        )
    )

    assert decision.selected_skill_id == "skill:summarize_process_trace"
    assert decision.decision_mode == "tie_break"
    assert decision.decision_attrs["tie_break_used"] is True


def test_fallback_used_when_no_available_skills() -> None:
    decision = service().decide_skill(
        DecisionContext(
            process_instance_id="process_instance:test",
            session_id="session-test",
            agent_id="chanta_core_default",
            user_input="hello",
            available_skill_ids=[],
            explicit_skill_id=None,
            pig_guidance=[],
            context_attrs={},
        )
    )

    assert decision.selected_skill_id == "skill:llm_chat"
    assert decision.decision_attrs["fallback_used"] is True
