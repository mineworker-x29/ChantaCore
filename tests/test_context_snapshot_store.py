import pytest

from chanta_core.context.snapshot import ContextAssemblySnapshot
from chanta_core.context.snapshot_store import ContextSnapshotStore
from chanta_core.utility.time import utc_now_iso


def make_snapshot(snapshot_id: str) -> ContextAssemblySnapshot:
    return ContextAssemblySnapshot(
        snapshot_id=snapshot_id,
        session_id=None,
        process_instance_id=None,
        created_at=utc_now_iso(),
        storage_mode="preview",
        budget=None,
        block_snapshots=[],
        message_snapshots=[],
        compaction_result=None,
    )


def test_snapshot_store_append_load_recent_and_get(tmp_path) -> None:
    store = ContextSnapshotStore(tmp_path / "snapshots.jsonl")
    first = make_snapshot("context_snapshot:1")
    second = make_snapshot("context_snapshot:2")

    store.append(first)
    store.append(second)

    assert [snapshot.snapshot_id for snapshot in store.load_all()] == [
        "context_snapshot:1",
        "context_snapshot:2",
    ]
    assert [snapshot.snapshot_id for snapshot in store.recent(limit=1)] == [
        "context_snapshot:2"
    ]
    assert store.get("context_snapshot:1") == first
    assert store.get("missing") is None


def test_snapshot_store_skips_invalid_jsonl_rows(tmp_path) -> None:
    path = tmp_path / "snapshots.jsonl"
    store = ContextSnapshotStore(path)
    store.append(make_snapshot("context_snapshot:ok"))
    path.write_text(path.read_text(encoding="utf-8") + "{invalid\n", encoding="utf-8")

    with pytest.warns(RuntimeWarning):
        snapshots = store.load_all()

    assert [snapshot.snapshot_id for snapshot in snapshots] == ["context_snapshot:ok"]
