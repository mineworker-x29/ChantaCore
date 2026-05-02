from __future__ import annotations

import json
from pathlib import Path

from chanta_core.ocel.store import OCELStore


class OCELExporter:
    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def export_sqlite_copy(self, target_path: str | Path) -> Path:
        return self.store.copy_database_to(target_path)

    def export_json_stub(self, target_path: str | Path) -> Path:
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "status": "not_implemented",
            "message": (
                "OCEL JSON export is not implemented yet. SQLite store is "
                "canonical in v0.3."
            ),
        }
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return target
