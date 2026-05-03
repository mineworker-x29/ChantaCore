import pytest
from pathlib import Path

from chanta_core.editing import (
    APPROVAL_PHRASE,
    EditProposalService,
    EditProposalStore,
    PatchApplicationService,
    PatchApplicationStore,
    PatchApproval,
)
from chanta_core.editing.errors import EditProposalError, EditProposalValidationError
from chanta_core.workspace import WorkspaceConfig, WorkspaceInspector


def setup_workspace(tmp_path: Path):
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    proposal_store = EditProposalStore(tmp_path / "proposals.jsonl")
    patch_store = PatchApplicationStore(tmp_path / "patches.jsonl")
    proposal = EditProposalService(inspector, proposal_store).propose_text_replacement(
        target_path="app.py",
        proposed_text="new\n",
        title="Replace",
        rationale="Test",
    )
    service = PatchApplicationService(
        workspace_inspector=inspector,
        proposal_store=proposal_store,
        patch_store=patch_store,
    )
    return service, proposal, patch_store


def valid_approval(proposal_id: str) -> PatchApproval:
    return PatchApproval.create(
        proposal_id=proposal_id,
        approved_by="tester",
        approval_text=APPROVAL_PHRASE,
    )


def test_invalid_approval_no_file_change(tmp_path) -> None:
    service, proposal, _ = setup_workspace(tmp_path)

    with pytest.raises(EditProposalValidationError):
        service.apply_approved_proposal(
            proposal_id=proposal.proposal_id,
            approval=PatchApproval.create(
                proposal_id=proposal.proposal_id,
                approved_by="tester",
                approval_text="no",
            ),
        )

    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"


def test_valid_approval_applies_patch_and_backup(tmp_path) -> None:
    service, proposal, patch_store = setup_workspace(tmp_path)

    application = service.apply_approved_proposal(
        proposal_id=proposal.proposal_id,
        approval=valid_approval(proposal.proposal_id),
    )

    assert application.status == "applied"
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "new\n"
    assert application.backup_path
    assert Path(application.backup_path).read_text(encoding="utf-8") == "old\n"
    assert patch_store.get(application.patch_application_id) is not None


def test_dry_run_does_not_write(tmp_path) -> None:
    service, proposal, _ = setup_workspace(tmp_path)

    application = service.dry_run_approved_proposal(
        proposal_id=proposal.proposal_id,
        approval=valid_approval(proposal.proposal_id),
    )

    assert application.status == "pending"
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "old\n"


def test_missing_proposal_fails(tmp_path) -> None:
    service, _, _ = setup_workspace(tmp_path)

    with pytest.raises(EditProposalError):
        service.apply_approved_proposal(
            proposal_id="edit_proposal:missing",
            approval=valid_approval("edit_proposal:missing"),
        )


def test_comment_only_cannot_be_applied(tmp_path) -> None:
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    proposal_store = EditProposalStore(tmp_path / "proposals.jsonl")
    proposal = EditProposalService(inspector, proposal_store).propose_comment_only(
        target_path="app.py",
        title="Comment",
        rationale="No write",
    )
    service = PatchApplicationService(
        workspace_inspector=inspector,
        proposal_store=proposal_store,
        patch_store=PatchApplicationStore(tmp_path / "patches.jsonl"),
    )

    with pytest.raises(EditProposalValidationError):
        service.apply_approved_proposal(
            proposal_id=proposal.proposal_id,
            approval=valid_approval(proposal.proposal_id),
        )
