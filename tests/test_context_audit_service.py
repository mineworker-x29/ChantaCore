from chanta_core.context import (
    ContextAuditService,
    ContextBudget,
    ContextCompactionLayerResult,
    ContextCompactionResult,
    ContextSnapshotPolicy,
    make_context_block,
)
from chanta_core.context.snapshot_store import ContextSnapshotStore


def make_result(blocks):
    return ContextCompactionResult(
        blocks=blocks,
        layer_results=[
            ContextCompactionLayerResult(
                layer_name="SnipLayer",
                blocks=blocks,
                changed=True,
                dropped_block_ids=["block:dropped"],
                warnings=["snipped history"],
            )
        ],
        total_chars=sum(block.char_length for block in blocks),
        total_estimated_tokens=sum(block.token_estimate for block in blocks),
        dropped_block_ids=["block:dropped"],
        warnings=["snipped history"],
    )


def test_audit_service_metadata_only_stores_no_message_content(tmp_path) -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Tool",
        content="API_KEY=secret",
        priority=40,
        source="tool",
    )
    service = ContextAuditService(
        snapshot_policy=ContextSnapshotPolicy(
            enabled=True,
            storage_mode="metadata_only",
        ),
        snapshot_store=ContextSnapshotStore(tmp_path / "snapshots.jsonl"),
    )

    snapshot = service.build_snapshot(
        blocks=[block],
        messages=[{"role": "user", "content": "API_KEY=secret"}],
    )

    assert snapshot.message_snapshots[0].content_preview is None
    assert "content" not in snapshot.block_snapshots[0].to_dict()


def test_audit_service_preview_redacts_and_truncates(tmp_path) -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Tool",
        content="tool raw content",
        priority=40,
        source="tool",
    )
    service = ContextAuditService(
        snapshot_policy=ContextSnapshotPolicy(
            enabled=True,
            storage_mode="preview",
            max_preview_chars=50,
        ),
        snapshot_store=ContextSnapshotStore(tmp_path / "snapshots.jsonl"),
    )

    snapshot = service.build_snapshot(
        blocks=[block],
        messages=[{"role": "user", "content": "API_KEY=secret\n" + ("safe " * 30)}],
        compaction_result=make_result([block]),
        budget=ContextBudget(),
    )

    preview = snapshot.message_snapshots[0].content_preview or ""
    assert len(preview) == 50
    assert "secret" not in preview
    assert snapshot.warnings == ["snipped history"]
    assert snapshot.compaction_result is not None


def test_audit_service_full_mode_redacts_when_enabled(tmp_path) -> None:
    block = make_context_block(
        block_type="system",
        title="System",
        content="system",
        priority=100,
        source="runtime",
    )
    service = ContextAuditService(
        snapshot_policy=ContextSnapshotPolicy(
            enabled=True,
            storage_mode="full",
            redact_sensitive=True,
        ),
        snapshot_store=ContextSnapshotStore(tmp_path / "snapshots.jsonl"),
    )

    snapshot = service.maybe_store_snapshot(
        blocks=[block],
        messages=[{"role": "user", "content": "Bearer abc.def.ghi"}],
    )

    assert snapshot is not None
    assert snapshot.message_snapshots[0].content_preview == "Bearer [REDACTED]"
    assert service.snapshot_store.recent(limit=1)[0].snapshot_id == snapshot.snapshot_id
