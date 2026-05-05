import pytest

from chanta_core.context import ContextCollapsePolicy
from chanta_core.context.errors import ContextBudgetError


def test_default_context_collapse_policy_validates() -> None:
    policy = ContextCollapsePolicy()

    policy.validate()

    assert policy.enabled is True
    assert policy.to_dict()["max_references"] == 20


def test_disabled_context_collapse_policy_validates() -> None:
    policy = ContextCollapsePolicy(enabled=False)

    policy.validate()

    assert policy.to_dict()["enabled"] is False


def test_invalid_context_collapse_policy_values_fail() -> None:
    with pytest.raises(ContextBudgetError):
        ContextCollapsePolicy(enabled="yes").validate()
    with pytest.raises(ContextBudgetError):
        ContextCollapsePolicy(min_blocks_to_collapse=0).validate()
    with pytest.raises(ContextBudgetError):
        ContextCollapsePolicy(max_collapsed_block_chars=0).validate()
    with pytest.raises(ContextBudgetError):
        ContextCollapsePolicy(max_references=0).validate()
    with pytest.raises(ContextBudgetError):
        ContextCollapsePolicy(collapse_block_priority="low").validate()
