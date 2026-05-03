from __future__ import annotations

from typing import Any

from chanta_core.editing.diff import create_unified_diff, safe_preview
from chanta_core.editing.proposal import EditProposal, new_edit_proposal_id
from chanta_core.editing.store import EditProposalStore
from chanta_core.workspace import WorkspaceInspector


class EditProposalService:
    def __init__(
        self,
        workspace_inspector: WorkspaceInspector,
        store: EditProposalStore | None = None,
    ) -> None:
        self.workspace_inspector = workspace_inspector
        self.store = store or EditProposalStore()

    def propose_text_replacement(
        self,
        *,
        target_path: str,
        proposed_text: str,
        title: str,
        rationale: str,
        evidence_refs: list[dict[str, Any]] | None = None,
        proposal_attrs: dict[str, Any] | None = None,
    ) -> EditProposal:
        original = self.workspace_inspector.read_text_file(target_path)
        original_text = str(original["text"])
        relative_path = str(original["path"])
        proposal = EditProposal(
            proposal_id=new_edit_proposal_id(),
            target_path=relative_path,
            proposal_type="replace_file",
            title=title,
            rationale=rationale,
            original_text_preview=safe_preview(original_text),
            proposed_text=proposed_text,
            proposed_diff=create_unified_diff(
                original_text=original_text,
                proposed_text=proposed_text,
                fromfile=relative_path,
                tofile=f"{relative_path} (proposed)",
            ),
            risk_level=str((proposal_attrs or {}).get("risk_level") or "medium"),
            status="proposed",
            evidence_refs=evidence_refs or [],
            proposal_attrs={
                **(proposal_attrs or {}),
                "proposal_only": True,
                "workspace_file_mutated": False,
            },
        )
        self.store.append(proposal)
        return proposal

    def propose_comment_only(
        self,
        *,
        target_path: str,
        title: str,
        rationale: str,
        evidence_refs: list[dict[str, Any]] | None = None,
        proposal_attrs: dict[str, Any] | None = None,
    ) -> EditProposal:
        original = self.workspace_inspector.read_text_file(target_path)
        relative_path = str(original["path"])
        proposal = EditProposal(
            proposal_id=new_edit_proposal_id(),
            target_path=relative_path,
            proposal_type="comment_only",
            title=title,
            rationale=rationale,
            original_text_preview=safe_preview(str(original["text"])),
            proposed_text=None,
            proposed_diff=None,
            risk_level=str((proposal_attrs or {}).get("risk_level") or "low"),
            status="proposed",
            evidence_refs=evidence_refs or [],
            proposal_attrs={
                **(proposal_attrs or {}),
                "proposal_only": True,
                "workspace_file_mutated": False,
            },
        )
        self.store.append(proposal)
        return proposal

    def summarize_recent_proposals(self, limit: int = 20) -> dict[str, Any]:
        proposals = self.store.recent(limit=limit)
        statuses: dict[str, int] = {}
        targets: dict[str, int] = {}
        for proposal in proposals:
            statuses[proposal.status] = statuses.get(proposal.status, 0) + 1
            targets[proposal.target_path] = targets.get(proposal.target_path, 0) + 1
        return {
            "proposal_count": len(proposals),
            "statuses": statuses,
            "targets": targets,
            "recent_proposals": [proposal.to_dict() for proposal in proposals],
            "proposal_only": True,
        }
