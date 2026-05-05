import pytest

from chanta_core.context import MicrocompactPolicy
from chanta_core.context.errors import ContextBudgetError


def test_default_microcompact_policy_validates() -> None:
    policy = MicrocompactPolicy()

    policy.validate()

    assert policy.to_dict()["max_lines"] == 40


def test_invalid_microcompact_policy_values_raise() -> None:
    for field_name in [
        "max_lines",
        "max_line_chars",
        "max_activity_items",
        "max_mapping_items",
        "max_report_chars",
        "max_json_chars",
    ]:
        with pytest.raises(ContextBudgetError):
            MicrocompactPolicy(**{field_name: 0}).validate()

    with pytest.raises(ContextBudgetError):
        MicrocompactPolicy(preserve_refs="yes").validate()
