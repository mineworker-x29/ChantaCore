from chanta_core.memory import MemoryEntry, hash_content, memory_entries_to_history_entries


def test_memory_entries_to_history_entries_preserves_refs() -> None:
    memory = MemoryEntry(
        memory_id="memory:test",
        memory_type="semantic",
        title="Test",
        content="Remember this.",
        content_preview="Remember this.",
        content_hash=hash_content("Remember this."),
        status="active",
        confidence=0.8,
        created_at="2026-05-05T00:00:00Z",
        updated_at="2026-05-05T00:00:00Z",
        valid_from=None,
        valid_until=None,
        contradiction_status="none",
        source_kind="manual_entry",
        scope="project",
    )

    entries = memory_entries_to_history_entries([memory])

    assert entries[0].source == "memory"
    assert entries[0].role == "context"
    assert entries[0].priority == 80
    assert entries[0].refs[0]["ref_id"] == "memory:test"
    assert entries[0].refs[0]["confidence"] == 0.8
    assert entries[0].refs[0]["contradiction_status"] == "none"
