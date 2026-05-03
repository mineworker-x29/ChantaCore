from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.editing import (
    APPROVAL_PHRASE,
    EditProposal,
    EditProposalStore,
    PatchApplicationService,
    PatchApplicationStore,
    PatchApproval,
    create_unified_diff,
)
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / ".env").write_text("SECRET=value\n", encoding="utf-8")
        proposal_store = EditProposalStore(root / "proposals.jsonl")
        patch_service = PatchApplicationService(
            workspace_inspector=WorkspaceInspector(WorkspaceConfig(workspace_root=root)),
            proposal_store=proposal_store,
            patch_store=PatchApplicationStore(root / "patches.jsonl"),
        )

        proposal = EditProposal(
            proposal_id="edit_proposal:blocked-env",
            target_path=".env",
            proposal_type="replace_file",
            title="Blocked env proposal",
            rationale="Safety smoke test.",
            original_text_preview="SECRET=value\n",
            proposed_text="SECRET=changed\n",
            proposed_diff=create_unified_diff(
                original_text="SECRET=value\n",
                proposed_text="SECRET=changed\n",
                fromfile=".env",
                tofile=".env",
            ),
            risk_level="high",
            status="proposed",
            evidence_refs=[],
            created_at=utc_now_iso(),
            proposal_attrs={},
        )
        proposal_store.append(proposal)
        approval = PatchApproval.create(
            proposal_id=proposal.proposal_id,
            approved_by="script",
            approval_text=APPROVAL_PHRASE,
        )

        try:
            patch_service.apply_approved_proposal(
                proposal_id=proposal.proposal_id,
                approval=approval,
            )
            denied = False
        except Exception as error:
            denied = True
            print(f"blocked_error={type(error).__name__}: {error}")

        unchanged = (root / ".env").read_text(encoding="utf-8") == "SECRET=value\n"
        print(f"blocked_path_denied={denied}")
        print(f"blocked_file_unchanged={unchanged}")
        print(f"recorded_attempts={len(patch_service.patch_store.load_all())}")


if __name__ == "__main__":
    main()
