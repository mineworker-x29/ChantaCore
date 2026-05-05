from chanta_core.memory import (
    MemoryEntry,
    MemoryRevision,
    hash_content,
    new_memory_entry_id,
    new_memory_revision_id,
    preview_text,
)


def test_memory_ids_use_expected_prefixes() -> None:
    assert new_memory_entry_id().startswith("memory:")
    assert new_memory_revision_id().startswith("memory_revision:")


def test_memory_hash_and_preview_are_stable() -> None:
    assert hash_content("memory") == hash_content("memory")
    assert preview_text("short") == "short"
    assert preview_text("x" * 300).endswith("...[memory preview truncated]...")


def test_memory_entry_to_dict() -> None:
    entry = MemoryEntry(
        memory_id="memory:test",
        memory_type="semantic",
        title="Test",
        content="content",
        content_preview="content",
        content_hash=hash_content("content"),
        status="active",
        confidence=0.9,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        valid_from=None,
        valid_until=None,
        contradiction_status="none",
        source_kind="manual_entry",
        scope="project",
    )

    data = entry.to_dict()

    assert data["memory_type"] == "semantic"
    assert data["content_hash"] == hash_content("content")


def test_memory_revision_to_dict() -> None:
    revision = MemoryRevision(
        revision_id="memory_revision:test",
        memory_id="memory:test",
        revision_index=1,
        operation="create",
        before_hash=None,
        after_hash="after",
        content_preview="content",
        content_hash="after",
        reason="reason",
        created_at="2026-05-05T00:00:00Z",
        actor_type="test",
    )

    assert revision.to_dict()["operation"] == "create"
