from chanta_core.context import (
    ContextAuditService,
    ContextSnapshotPolicy,
    ContextSnapshotStore,
    make_context_block,
)


def main() -> None:
    block = make_context_block(
        block_type="tool_result",
        title="Demo Tool Result",
        content="API_KEY=secret-value\nresult=ok",
        priority=40,
        source="script",
        refs=[{"ref_type": "tool_result", "ref_id": "tool_result:demo"}],
    )
    messages = [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "Please inspect API_KEY=secret-value"},
    ]
    service = ContextAuditService(
        snapshot_policy=ContextSnapshotPolicy(enabled=True, storage_mode="preview"),
        snapshot_store=ContextSnapshotStore(),
    )

    snapshot = service.maybe_store_snapshot(
        blocks=[block],
        messages=messages,
        session_id="session:demo",
        process_instance_id="process:demo",
    )

    assert snapshot is not None
    print(f"snapshot_id={snapshot.snapshot_id}")
    print(f"storage_mode={snapshot.storage_mode}")
    for index, message in enumerate(snapshot.message_snapshots, start=1):
        print(f"message_{index}_preview={message.content_preview}")


if __name__ == "__main__":
    main()
