from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.editing import (
    APPROVAL_PHRASE,
    EditProposalService,
    EditProposalStore,
    PatchApplicationService,
    PatchApplicationStore,
    PatchApproval,
)
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def main() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        target = root / "sample.py"
        target.write_text("print('old')\n", encoding="utf-8")

        inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=root))
        proposal_store = EditProposalStore(root / "proposals.jsonl")
        patch_store = PatchApplicationStore(root / "patches.jsonl")
        proposal_service = EditProposalService(
            workspace_inspector=inspector,
            store=proposal_store,
        )
        patch_service = PatchApplicationService(
            workspace_inspector=inspector,
            proposal_store=proposal_store,
            patch_store=patch_store,
        )

        proposal = proposal_service.propose_text_replacement(
            target_path="sample.py",
            proposed_text="print('new')\n",
            title="Replace sample output",
            rationale="Smoke test approved patch application.",
        )
        approval = PatchApproval.create(
            proposal_id=proposal.proposal_id,
            approved_by="script",
            approval_text=APPROVAL_PHRASE,
        )
        dry_run = patch_service.dry_run_approved_proposal(
            proposal_id=proposal.proposal_id,
            approval=approval,
        )
        applied = patch_service.apply_approved_proposal(
            proposal_id=proposal.proposal_id,
            approval=approval,
        )

        print(f"proposal_id={proposal.proposal_id}")
        print(f"dry_run_status={dry_run.status}")
        print(f"patch_application_id={applied.patch_application_id}")
        print(f"patch_status={applied.status}")
        file_changed = target.read_text(encoding="utf-8") == "print('new')\n"
        print(f"backup_exists={Path(applied.backup_path or '').exists()}")
        print(f"file_changed={file_changed}")


if __name__ == "__main__":
    main()
