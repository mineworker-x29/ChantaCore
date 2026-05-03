import pytest

from chanta_core.runtime.decision.policy import DecisionPolicy


def test_decision_policy_validates_defaults() -> None:
    policy = DecisionPolicy()

    policy.validate()
    assert policy.tie_break_order[0] == "skill:llm_chat"


def test_decision_policy_rejects_invalid_confidence_threshold() -> None:
    with pytest.raises(ValueError):
        DecisionPolicy(min_guidance_confidence=1.5).validate()


def test_decision_policy_rejects_empty_fallback() -> None:
    with pytest.raises(ValueError):
        DecisionPolicy(fallback_skill_id="").validate()


def test_decision_policy_rejects_empty_tie_break_order() -> None:
    with pytest.raises(ValueError):
        DecisionPolicy(tie_break_order=[]).validate()
