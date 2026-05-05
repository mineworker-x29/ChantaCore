import pytest

from chanta_core.context import ContextHistoryPolicy, SessionContextPolicy
from chanta_core.context.errors import ContextBudgetError


def test_default_context_history_policy_validates() -> None:
    policy = ContextHistoryPolicy()

    policy.validate()

    assert policy.to_dict()["max_history_blocks"] == 12


def test_invalid_context_history_policy_fails() -> None:
    with pytest.raises(ContextBudgetError):
        ContextHistoryPolicy(max_history_blocks=0).validate()
    with pytest.raises(ContextBudgetError):
        ContextHistoryPolicy(max_recent_history_blocks=0).validate()
    with pytest.raises(ContextBudgetError):
        ContextHistoryPolicy(preserve_last_user_blocks=-1).validate()
    with pytest.raises(ContextBudgetError):
        ContextHistoryPolicy(min_priority_to_keep=101).validate()
    with pytest.raises(ContextBudgetError):
        ContextHistoryPolicy(history_block_priority_decay=-1).validate()


def test_session_context_policy_to_dict() -> None:
    policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        include_history=True,
    )

    data = policy.to_dict()

    assert data["session_id"] == "session:1"
    assert data["process_instance_id"] == "pi:1"
    assert data["include_history"] is True
    assert data["history_policy"]["max_history_blocks"] == 12
