from chanta_core.editing import EditProposal, create_unified_diff, new_edit_proposal_id, safe_preview


def test_edit_proposal_to_dict_and_id() -> None:
    proposal = EditProposal(
        proposal_id=new_edit_proposal_id(),
        target_path="app.py",
        proposal_type="comment_only",
        title="Title",
        rationale="Rationale",
        original_text_preview="old",
        proposed_text=None,
        proposed_diff=None,
        risk_level="low",
        status="proposed",
    )

    assert proposal.proposal_id.startswith("edit_proposal:")
    assert proposal.to_dict()["status"] == "proposed"


def test_create_unified_diff() -> None:
    diff = create_unified_diff(
        original_text="a\nb\n",
        proposed_text="a\nc\n",
        fromfile="old",
        tofile="new",
    )

    assert "--- old" in diff
    assert "+++ new" in diff
    assert "-b" in diff
    assert "+c" in diff


def test_safe_preview_truncates() -> None:
    assert safe_preview("x" * 10, max_chars=5) == "xx..."
