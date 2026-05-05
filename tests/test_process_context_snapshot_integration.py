from chanta_core.context import ContextBudget, ContextSnapshotPolicy
from chanta_core.context.snapshot_store import ContextSnapshotStore
from chanta_core.runtime.loop.context import ProcessContextAssembler


def test_context_assembler_snapshot_disabled_keeps_legacy_behavior() -> None:
    assembler = ProcessContextAssembler()

    messages = assembler.assemble_for_llm_chat(
        user_input="hello API_KEY=secret",
        system_prompt="system",
    )

    assert messages == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "hello API_KEY=secret"},
    ]
    assert assembler.last_snapshot is None


def test_context_assembler_can_store_preview_snapshot(tmp_path) -> None:
    assembler = ProcessContextAssembler()
    store = ContextSnapshotStore(tmp_path / "snapshots.jsonl")
    policy = ContextSnapshotPolicy(
        enabled=True,
        storage_mode="preview",
        max_preview_chars=80,
    )

    messages = assembler.assemble_for_llm_chat(
        user_input="hello API_KEY=secret",
        system_prompt="system",
        context_snapshot_policy=policy,
        context_snapshot_store=store,
        session_id="session:snapshot",
        process_instance_id="process:snapshot",
    )

    assert messages == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "hello API_KEY=secret"},
    ]
    assert assembler.last_snapshot is not None
    assert assembler.last_snapshot.session_id == "session:snapshot"
    previews = [
        snapshot.content_preview or ""
        for snapshot in assembler.last_snapshot.message_snapshots
    ]
    assert any("hello API_KEY=[REDACTED]" in preview for preview in previews)
    assert all("secret" not in preview for preview in previews)
    assert store.recent(limit=1)[0].snapshot_id == assembler.last_snapshot.snapshot_id


def test_context_assembler_snapshot_with_budget_includes_compaction_result(tmp_path) -> None:
    assembler = ProcessContextAssembler()
    store = ContextSnapshotStore(tmp_path / "snapshots.jsonl")

    messages = assembler.assemble_for_llm_chat(
        user_input="hello",
        system_prompt="system",
        extra_blocks=[],
        context_budget=ContextBudget(max_total_chars=800, reserve_chars=100),
        context_snapshot_policy=ContextSnapshotPolicy(enabled=True),
        context_snapshot_store=store,
    )

    assert [message["content"] for message in messages if message["role"] == "user"] == [
        "hello"
    ]
    assert assembler.last_snapshot is not None
    assert assembler.last_snapshot.compaction_result is not None
