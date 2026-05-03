from __future__ import annotations

from chanta_core.pig.guidance import PIGGuidance
from chanta_core.runtime.decision import DecisionContext, DecisionPolicy, DecisionService
from chanta_core.skills.registry import SkillRegistry


def guidance(
    guidance_id: str,
    skill_id: str,
    *,
    confidence: float,
    score_delta: float,
) -> PIGGuidance:
    return PIGGuidance(
        guidance_id=guidance_id,
        guidance_type="skill_bias",
        title="Script guidance",
        target_scope={},
        suggested_skill_id=skill_id,
        suggested_activity=None,
        score_delta=score_delta,
        rationale="script advisory guidance",
        evidence_refs=[],
        confidence=confidence,
        status="active",
        guidance_attrs={"advisory": True, "hard_policy": False},
    )


def main() -> None:
    registry = SkillRegistry()
    policy = DecisionPolicy(
        min_guidance_confidence=0.45,
        max_guidance_boost_per_skill=0.1,
        tie_break_order=["skill:summarize_process_trace", "skill:llm_chat"],
    )
    service = DecisionService(skill_registry=registry, policy=policy)
    context = DecisionContext(
        process_instance_id="process_instance:script-tightening",
        session_id="script-session-tightening",
        agent_id="chanta_core_default",
        user_input="hello",
        available_skill_ids=[skill.skill_id for skill in registry.list_skills()],
        explicit_skill_id=None,
        pig_guidance=[
            guidance(
                "pig_guidance:low",
                "skill:inspect_ocel_recent",
                confidence=0.2,
                score_delta=1.0,
            ),
            guidance(
                "pig_guidance:high",
                "skill:summarize_process_trace",
                confidence=0.8,
                score_delta=1.0,
            ),
        ],
        context_attrs={},
    )
    decision = service.decide_skill(context)

    print("selected_skill_id:", decision.selected_skill_id)
    print("decision_mode:", decision.decision_mode)
    print("applied_guidance_ids:", decision.applied_guidance_ids)
    print("ignored_guidance:", decision.decision_attrs["ignored_guidance"])
    print("capped_skills:", decision.decision_attrs["capped_skills"])
    print("boost_by_skill:", decision.decision_attrs["boost_by_skill"])
    print("tie_break_used:", decision.decision_attrs["tie_break_used"])
    print("fallback_used:", decision.decision_attrs["fallback_used"])


if __name__ == "__main__":
    main()
