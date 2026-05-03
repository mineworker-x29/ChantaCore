import pytest

from chanta_core.editing import EditProposalService, EditProposalStore
from chanta_core.workspace import WorkspaceAccessError, WorkspaceConfig, WorkspaceInspector


def service(tmp_path):
    (tmp_path / "app.py").write_text("print('old')\n", encoding="utf-8")
    (tmp_path / ".env").write_text("SECRET=1\n", encoding="utf-8")
    inspector = WorkspaceInspector(WorkspaceConfig(workspace_root=tmp_path))
    store = EditProposalStore(tmp_path / "proposals.jsonl")
    return EditProposalService(workspace_inspector=inspector, store=store), store


def test_propose_text_replacement_does_not_mutate_file(tmp_path) -> None:
    edit_service, store = service(tmp_path)

    proposal = edit_service.propose_text_replacement(
        target_path="app.py",
        proposed_text="print('new')\n",
        title="Update print",
        rationale="Test proposal",
    )

    assert proposal.status == "proposed"
    assert "-print('old')" in proposal.proposed_diff
    assert "+print('new')" in proposal.proposed_diff
    assert (tmp_path / "app.py").read_text(encoding="utf-8") == "print('old')\n"
    assert store.get(proposal.proposal_id) is not None


def test_propose_comment_only(tmp_path) -> None:
    edit_service, _ = service(tmp_path)

    proposal = edit_service.propose_comment_only(
        target_path="app.py",
        title="Review note",
        rationale="Consider clarifying this file.",
    )

    assert proposal.proposal_type == "comment_only"
    assert proposal.proposed_diff is None


def test_blocked_path_fails(tmp_path) -> None:
    edit_service, _ = service(tmp_path)

    with pytest.raises(WorkspaceAccessError):
        edit_service.propose_comment_only(
            target_path=".env",
            title="No",
            rationale="Blocked",
        )
