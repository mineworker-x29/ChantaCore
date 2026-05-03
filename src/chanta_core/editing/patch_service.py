from __future__ import annotations

from pathlib import Path
from typing import Any

from chanta_core.editing.approval import PatchApproval
from chanta_core.editing.diff import safe_preview
from chanta_core.editing.errors import EditProposalError, EditProposalValidationError
from chanta_core.editing.patch import PatchApplication, new_patch_application_id
from chanta_core.editing.patch_store import PatchApplicationStore
from chanta_core.editing.backup import PatchBackupService
from chanta_core.editing.store import EditProposalStore
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace import WorkspaceInspector


class PatchApplicationService:
    def __init__(
        self,
        *,
        workspace_inspector: WorkspaceInspector,
        proposal_store: EditProposalStore,
        patch_store: PatchApplicationStore | None = None,
        backup_service: PatchBackupService | None = None,
    ) -> None:
        self.workspace_inspector = workspace_inspector
        self.proposal_store = proposal_store
        self.patch_store = patch_store or PatchApplicationStore()
        self.backup_service = backup_service or PatchBackupService(
            workspace_inspector.config
        )

    def apply_approved_proposal(
        self,
        *,
        proposal_id: str,
        approval: PatchApproval,
    ) -> PatchApplication:
        backup_path: str | None = None
        try:
            proposal, current = self._validate_application(proposal_id, approval)
            original_text = str(current["text"])
            target_path = str(current["path"])
            backup_path = self.backup_service.create_backup(
                target_path=target_path,
                original_text=original_text,
                proposal_id=proposal_id,
            )
            target = self.workspace_inspector.guard.validate_read_path(target_path)
            proposed_text = str(proposal.proposed_text)
            target.write_text(proposed_text, encoding="utf-8")
            application = PatchApplication(
                patch_application_id=new_patch_application_id(),
                proposal_id=proposal_id,
                approval_id=approval.approval_id,
                target_path=target_path,
                status="applied",
                applied_at=utc_now_iso(),
                backup_path=backup_path,
                original_size_bytes=len(original_text.encode("utf-8")),
                new_size_bytes=len(proposed_text.encode("utf-8")),
                diff_preview=safe_preview(proposal.proposed_diff or "", max_chars=2000),
                error=None,
                patch_attrs={
                    "approval_validated": True,
                    "workspace_file_mutated": True,
                    "rollback_available": bool(backup_path),
                },
            )
            self.patch_store.append(application)
            return application
        except Exception as error:
            application = PatchApplication(
                patch_application_id=new_patch_application_id(),
                proposal_id=proposal_id,
                approval_id=getattr(approval, "approval_id", ""),
                target_path="",
                status="failed",
                applied_at=None,
                backup_path=backup_path,
                original_size_bytes=None,
                new_size_bytes=None,
                diff_preview=None,
                error=str(error),
                patch_attrs={"workspace_file_mutated": False},
            )
            self.patch_store.append(application)
            raise

    def dry_run_approved_proposal(
        self,
        *,
        proposal_id: str,
        approval: PatchApproval,
    ) -> PatchApplication:
        proposal, current = self._validate_application(proposal_id, approval)
        application = PatchApplication(
            patch_application_id=new_patch_application_id(),
            proposal_id=proposal_id,
            approval_id=approval.approval_id,
            target_path=str(current["path"]),
            status="pending",
            applied_at=None,
            backup_path=None,
            original_size_bytes=int(current["size_bytes"]),
            new_size_bytes=len(str(proposal.proposed_text).encode("utf-8")),
            diff_preview=safe_preview(proposal.proposed_diff or "", max_chars=2000),
            error=None,
            patch_attrs={
                "dry_run": True,
                "approval_validated": True,
                "workspace_file_mutated": False,
            },
        )
        self.patch_store.append(application)
        return application

    def summarize_recent_patch_applications(self, limit: int = 20) -> dict[str, Any]:
        applications = self.patch_store.recent(limit=limit)
        statuses: dict[str, int] = {}
        targets: dict[str, int] = {}
        for application in applications:
            statuses[application.status] = statuses.get(application.status, 0) + 1
            targets[application.target_path] = targets.get(application.target_path, 0) + 1
        return {
            "patch_application_count": len(applications),
            "statuses": statuses,
            "targets": targets,
            "recent_patch_applications": [item.to_dict() for item in applications],
        }

    def _validate_application(self, proposal_id: str, approval: PatchApproval):
        if not proposal_id:
            raise EditProposalValidationError("proposal_id is required.")
        approval.validate()
        if approval.proposal_id != proposal_id:
            raise EditProposalValidationError("approval.proposal_id does not match proposal_id.")
        proposal = self.proposal_store.get(proposal_id)
        if proposal is None:
            raise EditProposalError(f"Edit proposal not found: {proposal_id}")
        if proposal.status not in {"proposed", "approved"}:
            raise EditProposalValidationError(
                f"Proposal status cannot be applied: {proposal.status}"
            )
        if proposal.proposal_type != "replace_file":
            raise EditProposalValidationError(
                f"Only replace_file proposals can be applied in v0.8.5: {proposal.proposal_type}"
            )
        if proposal.proposed_text is None:
            raise EditProposalValidationError("Proposal has no proposed_text.")
        current = self.workspace_inspector.read_text_file(proposal.target_path)
        return proposal, current
