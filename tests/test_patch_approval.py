import pytest

from chanta_core.editing import APPROVAL_PHRASE, PatchApproval
from chanta_core.editing.errors import EditProposalValidationError


def test_valid_approval_phrase() -> None:
    approval = PatchApproval.create(
        proposal_id="edit_proposal:1",
        approved_by="tester",
        approval_text=f"Please apply. {APPROVAL_PHRASE}",
    )

    approval.validate()
    assert approval.is_valid() is True
    assert approval.to_dict()["proposal_id"] == "edit_proposal:1"


def test_missing_phrase_invalid() -> None:
    approval = PatchApproval.create(
        proposal_id="edit_proposal:1",
        approved_by="tester",
        approval_text="please apply",
    )

    with pytest.raises(EditProposalValidationError):
        approval.validate()


def test_missing_approved_by_invalid() -> None:
    approval = PatchApproval.create(
        proposal_id="edit_proposal:1",
        approved_by="",
        approval_text=APPROVAL_PHRASE,
    )

    with pytest.raises(EditProposalValidationError):
        approval.validate()
