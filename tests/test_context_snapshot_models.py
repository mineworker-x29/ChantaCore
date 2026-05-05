from chanta_core.context.snapshot import (
    ContextAssemblySnapshot,
    ContextBlockSnapshot,
    ContextMessageSnapshot,
    new_context_snapshot_id,
)
from chanta_core.utility.time import utc_now_iso


def test_context_snapshot_id_prefix() -> None:
    assert new_context_snapshot_id().startswith("context_snapshot:")


def test_context_block_snapshot_to_dict() -> None:
    snapshot = ContextBlockSnapshot(
        block_id="block:1",
        block_type="tool_result",
        title="Tool",
        source="tool",
        priority=40,
        char_length=12,
        token_estimate=3,
        was_truncated=True,
        was_dropped=False,
        was_collapsed=False,
        refs=[{"ref_type": "tool_result", "ref_id": "tool:1"}],
    )

    data = snapshot.to_dict()

    assert data["block_id"] == "block:1"
    assert data["was_truncated"] is True
    assert "content" not in data


def test_context_message_snapshot_to_dict() -> None:
    snapshot = ContextMessageSnapshot(
        role="user",
        content_preview="hello",
        char_length=5,
        token_estimate=1,
    )

    assert snapshot.to_dict()["content_preview"] == "hello"


def test_context_assembly_snapshot_to_dict() -> None:
    snapshot = ContextAssemblySnapshot(
        snapshot_id="context_snapshot:test",
        session_id="session:1",
        process_instance_id="process:1",
        created_at=utc_now_iso(),
        storage_mode="preview",
        budget={"max_total_chars": 1000},
        block_snapshots=[],
        message_snapshots=[],
        compaction_result=None,
        warnings=["warning"],
    )

    data = snapshot.to_dict()

    assert data["snapshot_id"] == "context_snapshot:test"
    assert data["storage_mode"] == "preview"
    assert data["warnings"] == ["warning"]
