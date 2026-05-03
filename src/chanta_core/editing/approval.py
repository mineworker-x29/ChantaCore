from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.editing.errors import EditProposalValidationError
from chanta_core.utility.time import utc_now_iso


APPROVAL_PHRASE = "I APPROVE PATCH APPLICATION"


def new_patch_approval_id() -> str:
    return f"patch_approval:{uuid4()}"


@dataclass(frozen=True)
class PatchApproval:
    approval_id: str
    proposal_id: str
    approved_by: str
    approval_text: str
    approved_at: str = field(default_factory=utc_now_iso)
    approval_attrs: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        *,
        proposal_id: str,
        approved_by: str,
        approval_text: str,
        approval_attrs: dict[str, Any] | None = None,
    ) -> "PatchApproval":
        return cls(
            approval_id=new_patch_approval_id(),
            proposal_id=proposal_id,
            approved_by=approved_by,
            approval_text=approval_text,
            approval_attrs=approval_attrs or {},
        )

    def validate(self) -> None:
        if not self.proposal_id:
            raise EditProposalValidationError("proposal_id is required for patch approval.")
        if not self.approved_by:
            raise EditProposalValidationError("approved_by is required for patch approval.")
        if APPROVAL_PHRASE not in self.approval_text:
            raise EditProposalValidationError(
                f"approval_text must contain exact phrase: {APPROVAL_PHRASE}"
            )

    def is_valid(self) -> bool:
        try:
            self.validate()
            return True
        except EditProposalValidationError:
            return False

    def to_dict(self) -> dict[str, Any]:
        return {
            "approval_id": self.approval_id,
            "proposal_id": self.proposal_id,
            "approved_by": self.approved_by,
            "approval_text": self.approval_text,
            "approved_at": self.approved_at,
            "approval_attrs": self.approval_attrs,
        }
