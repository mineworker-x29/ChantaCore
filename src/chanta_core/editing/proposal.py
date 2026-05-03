from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.utility.time import utc_now_iso


def new_edit_proposal_id() -> str:
    return f"edit_proposal:{uuid4()}"


@dataclass(frozen=True)
class EditProposal:
    proposal_id: str
    target_path: str
    proposal_type: str
    title: str
    rationale: str
    original_text_preview: str | None
    proposed_text: str | None
    proposed_diff: str | None
    risk_level: str
    status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now_iso)
    proposal_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "proposal_id": self.proposal_id,
            "target_path": self.target_path,
            "proposal_type": self.proposal_type,
            "title": self.title,
            "rationale": self.rationale,
            "original_text_preview": self.original_text_preview,
            "proposed_text": self.proposed_text,
            "proposed_diff": self.proposed_diff,
            "risk_level": self.risk_level,
            "status": self.status,
            "evidence_refs": self.evidence_refs,
            "created_at": self.created_at,
            "proposal_attrs": self.proposal_attrs,
        }
