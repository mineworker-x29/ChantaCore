from chanta_core.context import ContextSnapshotStore


def main() -> None:
    store = ContextSnapshotStore()
    snapshots = store.recent(limit=20)
    if not snapshots:
        print("no context snapshots found")
        return

    for snapshot in snapshots:
        print(
            " ".join(
                [
                    f"snapshot_id={snapshot.snapshot_id}",
                    f"storage_mode={snapshot.storage_mode}",
                    f"blocks={len(snapshot.block_snapshots)}",
                    f"messages={len(snapshot.message_snapshots)}",
                    f"warnings={len(snapshot.warnings)}",
                ]
            )
        )


if __name__ == "__main__":
    main()
