from __future__ import annotations

import json
import warnings
from pathlib import Path
from typing import Any

from chanta_core.editing.proposal import EditProposal


class EditProposalStore:
    def __init__(self, path: str | Path = "data/editing/edit_proposals.jsonl") -> None:
        self.path = Path(path)

    def append(self, proposal: EditProposal) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(proposal.to_dict(), ensure_ascii=False, sort_keys=True))
            handle.write("\n")

    def load_all(self) -> list[EditProposal]:
        if not self.path.exists():
            return []
        proposals: list[EditProposal] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                raw = line.strip()
                if not raw:
                    continue
                try:
                    loaded = json.loads(raw)
                    if isinstance(loaded, dict):
                        proposals.append(_proposal_from_dict(loaded))
                except Exception as error:
                    warnings.warn(
                        f"Skipping invalid edit proposal JSONL row {line_number}: {error}",
                        RuntimeWarning,
                        stacklevel=2,
                    )
        return proposals

    def recent(self, limit: int = 20) -> list[EditProposal]:
        return self.load_all()[-limit:]

    def get(self, proposal_id: str) -> EditProposal | None:
        for proposal in self.load_all():
            if proposal.proposal_id == proposal_id:
                return proposal
        return None

    def find_by_target_path(self, target_path: str) -> list[EditProposal]:
        return [
            proposal
            for proposal in self.load_all()
            if proposal.target_path == target_path
        ]


def _proposal_from_dict(data: dict[str, Any]) -> EditProposal:
    return EditProposal(
        proposal_id=str(data["proposal_id"]),
        target_path=str(data["target_path"]),
        proposal_type=str(data["proposal_type"]),
        title=str(data["title"]),
        rationale=str(data["rationale"]),
        original_text_preview=data.get("original_text_preview"),
        proposed_text=data.get("proposed_text"),
        proposed_diff=data.get("proposed_diff"),
        risk_level=str(data.get("risk_level") or "unknown"),
        status=str(data.get("status") or "proposed"),
        evidence_refs=list(data.get("evidence_refs") or []),
        created_at=str(data.get("created_at") or ""),
        proposal_attrs=dict(data.get("proposal_attrs") or {}),
    )
