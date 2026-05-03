from __future__ import annotations

from chanta_core.pig.guidance import PIGGuidance
from chanta_core.runtime.decision import DecisionContext, DecisionService
from chanta_core.skills.registry import SkillRegistry


def make_guidance() -> PIGGuidance:
    return PIGGuidance(
        guidance_id="pig_guidance:script",
        guidance_type="skill_bias",
        title="Inspect recent OCEL",
        target_scope={},
        suggested_skill_id="skill:inspect_ocel_recent",
        suggested_activity=None,
        score_delta=0.5,
        rationale="script advisory guidance",
        evidence_refs=[],
        confidence=0.8,
        status="active",
        guidance_attrs={"advisory": True, "hard_policy": False},
    )


def decide(user_input: str, guidance: list[PIGGuidance] | None = None) -> None:
    registry = SkillRegistry()
    service = DecisionService(skill_registry=registry)
    context = DecisionContext(
        process_instance_id="process_instance:script-decision",
        session_id="script-session-decision",
        agent_id="chanta_core_default",
        user_input=user_input,
        available_skill_ids=[skill.skill_id for skill in registry.list_skills()],
        explicit_skill_id=None,
        pig_guidance=guidance or [],
        context_attrs={},
    )
    decision = service.decide_skill(context)
    print(user_input, "->", decision.selected_skill_id, decision.decision_mode, decision.rationale)


def main() -> None:
    decide("please summarize process trace history")
    decide("inspect ocel event relation coverage")
    decide("hello", guidance=[make_guidance()])
    decide("hello")


if __name__ == "__main__":
    main()
