from chanta_core.editing import EditProposal, EditProposalStore, new_edit_proposal_id


def proposal(target_path: str = "app.py") -> EditProposal:
    return EditProposal(
        proposal_id=new_edit_proposal_id(),
        target_path=target_path,
        proposal_type="comment_only",
        title="Title",
        rationale="Rationale",
        original_text_preview=None,
        proposed_text=None,
        proposed_diff=None,
        risk_level="low",
        status="proposed",
    )


def test_store_append_load_recent_get_find(tmp_path) -> None:
    store = EditProposalStore(tmp_path / "proposals.jsonl")
    first = proposal("app.py")
    second = proposal("other.py")

    store.append(first)
    store.append(second)

    assert [item.proposal_id for item in store.load_all()] == [
        first.proposal_id,
        second.proposal_id,
    ]
    assert store.recent(1)[0].proposal_id == second.proposal_id
    assert store.get(first.proposal_id).target_path == "app.py"
    assert store.find_by_target_path("app.py")[0].proposal_id == first.proposal_id


def test_invalid_jsonl_row_skipped(tmp_path) -> None:
    path = tmp_path / "proposals.jsonl"
    path.write_text("{not-json}\n", encoding="utf-8")

    assert EditProposalStore(path).load_all() == []
