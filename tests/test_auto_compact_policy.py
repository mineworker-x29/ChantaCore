import pytest

from chanta_core.context import AutoCompactPolicy
from chanta_core.context.errors import ContextBudgetError


def test_auto_compact_policy_default_is_safe() -> None:
    policy = AutoCompactPolicy()

    policy.validate()

    assert policy.enabled is False
    assert policy.allow_llm_summarizer is False
    assert policy.to_dict()["require_explicit_enable"] is True


def test_auto_compact_policy_invalid_values_raise() -> None:
    with pytest.raises(ContextBudgetError):
        AutoCompactPolicy(max_input_chars=0).validate()
    with pytest.raises(ContextBudgetError):
        AutoCompactPolicy(max_output_chars=0).validate()
    with pytest.raises(ContextBudgetError):
        AutoCompactPolicy(enabled="yes").validate()
    with pytest.raises(ContextBudgetError):
        AutoCompactPolicy(allow_llm_summarizer="yes").validate()
