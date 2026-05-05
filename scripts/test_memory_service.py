from chanta_core.memory import MemoryService


def main() -> None:
    service = MemoryService()
    memory = service.create_memory_entry(
        memory_type="semantic",
        title="OCEL-native memory",
        content="Memory facts are persisted as OCEL records.",
        session_id="session:script-memory",
    )
    revised, revision = service.revise_memory_entry(
        memory=memory,
        new_content="Memory facts are persisted as OCEL event/object/relation records.",
        reason="make persistence explicit",
    )
    service.attach_memory_to_session(
        memory_id=revised.memory_id,
        session_id="session:script-memory",
    )

    print(f"memory_id={revised.memory_id}")
    print(f"revision_id={revision.revision_id}")
    print(f"revision_operation={revision.operation}")
    print(f"content_hash={revised.content_hash}")


if __name__ == "__main__":
    main()
