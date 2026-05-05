import pytest

from chanta_core.context import ContextBudget
from chanta_core.context.errors import ContextBudgetError


def test_default_budget_validates() -> None:
    budget = ContextBudget()

    budget.validate()

    assert budget.usable_chars() == 11000


def test_invalid_budget_values_raise() -> None:
    with pytest.raises(ContextBudgetError):
        ContextBudget(max_total_chars=100, reserve_chars=100).validate()
    with pytest.raises(ContextBudgetError):
        ContextBudget(max_tool_result_chars=0).validate()
    with pytest.raises(ContextBudgetError):
        ContextBudget(reserve_chars=-1).validate()


def test_usable_chars_subtracts_reserve() -> None:
    assert ContextBudget(max_total_chars=500, reserve_chars=125).usable_chars() == 375
