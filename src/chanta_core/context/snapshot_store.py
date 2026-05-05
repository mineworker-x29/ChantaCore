from __future__ import annotations

import json
import warnings
from pathlib import Path

from chanta_core.context.snapshot import ContextAssemblySnapshot


class ContextSnapshotStore:
    def __init__(self, path: str | Path | None = None) -> None:
        self.path = Path(path or "data/context/context_snapshots.jsonl")

    def append(self, snapshot: ContextAssemblySnapshot) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(snapshot.to_dict(), ensure_ascii=False, sort_keys=True))
            handle.write("\n")

    def load_all(self) -> list[ContextAssemblySnapshot]:
        if not self.path.exists():
            return []
        snapshots: list[ContextAssemblySnapshot] = []
        with self.path.open("r", encoding="utf-8") as handle:
            for line_number, line in enumerate(handle, start=1):
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    snapshots.append(ContextAssemblySnapshot.from_dict(data))
                except Exception as error:
                    warnings.warn(
                        f"Skipping invalid context snapshot row {line_number}: {error}",
                        RuntimeWarning,
                        stacklevel=2,
                    )
        return snapshots

    def recent(self, limit: int = 20) -> list[ContextAssemblySnapshot]:
        if limit <= 0:
            return []
        return self.load_all()[-limit:]

    def get(self, snapshot_id: str) -> ContextAssemblySnapshot | None:
        for snapshot in self.load_all():
            if snapshot.snapshot_id == snapshot_id:
                return snapshot
        return None
