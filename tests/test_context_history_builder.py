from chanta_core.context import (
    ContextHistoryBuilder,
    ContextHistoryEntry,
    ContextHistoryPolicy,
    SessionContextPolicy,
)


def entry(
    entry_id: str,
    *,
    session_id: str = "session:1",
    process_instance_id: str = "pi:1",
    created_at: str,
) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=entry_id,
        session_id=session_id,
        process_instance_id=process_instance_id,
        role="assistant",
        content=entry_id,
        created_at=created_at,
        source="chat",
        priority=50,
    )


def test_build_from_entries_creates_blocks_in_deterministic_order() -> None:
    entries = [
        entry("history:2", created_at="2026-05-05T00:02:00Z"),
        entry("history:1", created_at="2026-05-05T00:01:00Z"),
    ]

    blocks = ContextHistoryBuilder().build_from_entries(entries)

    assert [block.content for block in blocks] == ["history:1", "history:2"]


def test_build_recent_history_blocks_respects_include_history_false() -> None:
    policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        include_history=False,
    )

    blocks = ContextHistoryBuilder().build_recent_history_blocks(
        [entry("history:1", created_at="2026-05-05T00:01:00Z")],
        session_policy=policy,
    )

    assert blocks == []


def test_build_recent_history_blocks_filters_session_and_process() -> None:
    entries = [
        entry("keep", created_at="2026-05-05T00:01:00Z"),
        entry("wrong-session", session_id="session:2", created_at="2026-05-05T00:02:00Z"),
        entry("wrong-process", process_instance_id="pi:2", created_at="2026-05-05T00:03:00Z"),
    ]
    policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        history_policy=ContextHistoryPolicy(max_history_blocks=5, max_recent_history_blocks=5),
    )

    blocks = ContextHistoryBuilder().build_recent_history_blocks(
        entries,
        session_policy=policy,
    )

    assert [block.content for block in blocks] == ["keep"]


def test_build_recent_history_blocks_limits_to_recent_blocks() -> None:
    entries = [
        entry(f"history:{index}", created_at=f"2026-05-05T00:0{index}:00Z")
        for index in range(5)
    ]
    policy = SessionContextPolicy(
        session_id="session:1",
        process_instance_id="pi:1",
        history_policy=ContextHistoryPolicy(max_history_blocks=3, max_recent_history_blocks=3),
    )

    blocks = ContextHistoryBuilder().build_recent_history_blocks(
        entries,
        session_policy=policy,
    )

    assert [block.content for block in blocks] == ["history:2", "history:3", "history:4"]
