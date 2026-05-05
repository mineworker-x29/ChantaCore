import pytest

from chanta_core.context import ContextBudgetError
from chanta_core.context.snapshot_policy import ContextSnapshotPolicy


def test_default_snapshot_policy_is_disabled_preview() -> None:
    policy = ContextSnapshotPolicy()

    policy.validate()

    assert policy.enabled is False
    assert policy.storage_mode == "preview"


def test_preview_mode_validates() -> None:
    policy = ContextSnapshotPolicy(enabled=True, storage_mode="preview")

    policy.validate()

    assert policy.to_dict()["storage_mode"] == "preview"


def test_invalid_storage_mode_fails() -> None:
    with pytest.raises(ContextBudgetError):
        ContextSnapshotPolicy(storage_mode="raw").validate()


def test_invalid_preview_limit_fails() -> None:
    with pytest.raises(ContextBudgetError):
        ContextSnapshotPolicy(max_preview_chars=0).validate()
