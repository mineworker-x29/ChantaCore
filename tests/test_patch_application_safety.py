import pytest

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


def service(tmp_path):
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    proposal_store = EditProposalStore(tmp_path / "proposals.jsonl")
    return EditProposalService(inspector, proposal_store), PatchApplicationService(
        workspace_inspector=inspector,
        proposal_store=proposal_store,
        patch_store=PatchApplicationStore(tmp_path / "patches.jsonl"),
    )


def approval(proposal_id: str) -> PatchApproval:
    return PatchApproval.create(
        proposal_id=proposal_id,
        approved_by="tester",
        approval_text=APPROVAL_PHRASE,
    )


@pytest.mark.parametrize("target", [".env", "data/test.sqlite", "../outside.txt"])
def test_blocked_targets_denied(tmp_path, target: str) -> None:
    (tmp_path / ".env").write_text("secret\n", encoding="utf-8")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "test.sqlite").write_text("db\n", encoding="utf-8")
    proposal_service, _ = service(tmp_path)

    with pytest.raises(Exception):
        proposal_service.propose_text_replacement(
            target_path=target,
            proposed_text="new\n",
            title="Blocked",
            rationale="Blocked",
        )


def test_approval_for_different_proposal_fails(tmp_path) -> None:
    (tmp_path / "app.py").write_text("old\n", encoding="utf-8")
    proposal_service, patch_service = service(tmp_path)
    proposal = proposal_service.propose_text_replacement(
        target_path="app.py",
        proposed_text="new\n",
        title="Replace",
        rationale="Test",
    )

    with pytest.raises(EditProposalValidationError):
        patch_service.apply_approved_proposal(
            proposal_id=proposal.proposal_id,
            approval=approval("edit_proposal:other"),
        )


def test_invalid_proposal_id_fails(tmp_path) -> None:
    _, patch_service = service(tmp_path)

    with pytest.raises(EditProposalError):
        patch_service.apply_approved_proposal(
            proposal_id="edit_proposal:missing",
            approval=approval("edit_proposal:missing"),
        )
