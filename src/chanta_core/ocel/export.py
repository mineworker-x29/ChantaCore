from __future__ import annotations

import json
import shutil
import sqlite3
from pathlib import Path
from typing import Any

from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.query import OCELQueryService
from chanta_core.utility.time import utc_now_iso


CHANTA_OCEL_JSON_FORMAT = "chanta_ocel_json"
CHANTA_OCEL_JSON_VERSION = "0.8.9"


class OCELExporter:
    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def export_sqlite_copy(self, target_path: str | Path) -> Path:
        source = self.store.db_path
        if not source.is_file():
            raise FileNotFoundError(f"OCEL SQLite source DB does not exist: {source}")
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
        return target

    def export_chanta_json(self, target_path: str | Path) -> Path:
        self.store.initialize()
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "format": CHANTA_OCEL_JSON_FORMAT,
            "version": CHANTA_OCEL_JSON_VERSION,
            "exported_at": utc_now_iso(),
            "events": self._events(),
            "objects": self._objects(),
            "relations": self._relations(),
            "export_attrs": {
                "source": "chanta_core",
                "compatibility": "internal_canonical",
                "full_ocel2_json": False,
            },
        }
        target.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return target

    def export_json_stub(self, target_path: str | Path) -> Path:
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "status": "not_implemented",
            "message": (
                "Full OCEL 2.0 JSON export is not implemented yet. Use "
                "export_chanta_json for ChantaCore internal canonical JSON."
            ),
            "full_ocel2_json": False,
            "chanta_canonical_json_available": True,
        }
        target.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        return target

    def export_summary(self, target_path: str | Path) -> Path:
        target = Path(target_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        recent_events = self.store.fetch_recent_events(20)
        payload = {
            "format": "chanta_ocel_export_summary",
            "version": CHANTA_OCEL_JSON_VERSION,
            "exported_at": utc_now_iso(),
            "event_count": self.store.fetch_event_count(),
            "object_count": self.store.fetch_object_count(),
            "event_object_relation_count": self.store.fetch_event_object_relation_count(),
            "object_object_relation_count": self.store.fetch_object_object_relation_count(),
            "object_type_counts": OCELQueryService(self.store).object_type_counts(),
            "recent_event_activities": [item["event_activity"] for item in recent_events],
        }
        target.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )
        return target

    def _events(self) -> list[dict[str, Any]]:
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT
                    event_id,
                    event_activity,
                    event_timestamp,
                    event_attrs_json
                FROM chanta_event_payload
                ORDER BY event_timestamp ASC, event_id ASC
                """
            ).fetchall()
        return [
            {
                "event_id": row["event_id"],
                "event_activity": row["event_activity"],
                "event_timestamp": row["event_timestamp"],
                "event_attrs": _loads(row["event_attrs_json"]),
            }
            for row in rows
        ]

    def _objects(self) -> list[dict[str, Any]]:
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            rows = connection.execute(
                """
                SELECT object_id, object_type, object_attrs_json
                FROM chanta_object_state
                ORDER BY object_type ASC, object_id ASC
                """
            ).fetchall()
        return [
            {
                "object_id": row["object_id"],
                "object_type": row["object_type"],
                "object_attrs": _loads(row["object_attrs_json"]),
            }
            for row in rows
        ]

    def _relations(self) -> list[dict[str, Any]]:
        relations: list[dict[str, Any]] = []
        with sqlite3.connect(self.store.db_path) as connection:
            connection.row_factory = sqlite3.Row
            event_object_rows = connection.execute(
                """
                SELECT event_id, object_id, qualifier, relation_attrs_json
                FROM chanta_event_object_relation_ext
                ORDER BY event_id ASC, object_id ASC, qualifier ASC
                """
            ).fetchall()
            object_object_rows = connection.execute(
                """
                SELECT source_object_id, target_object_id, qualifier, relation_attrs_json
                FROM chanta_object_object_relation_ext
                ORDER BY source_object_id ASC, target_object_id ASC, qualifier ASC
                """
            ).fetchall()
        for row in event_object_rows:
            relations.append(
                {
                    "relation_kind": "event_object",
                    "source_id": row["event_id"],
                    "target_id": row["object_id"],
                    "qualifier": row["qualifier"],
                    "relation_attrs": _loads(row["relation_attrs_json"]),
                }
            )
        for row in object_object_rows:
            relations.append(
                {
                    "relation_kind": "object_object",
                    "source_id": row["source_object_id"],
                    "target_id": row["target_object_id"],
                    "qualifier": row["qualifier"],
                    "relation_attrs": _loads(row["relation_attrs_json"]),
                }
            )
        return relations


def _loads(raw: str | None) -> dict[str, Any]:
    if not raw:
        return {}
    loaded = json.loads(raw)
    return loaded if isinstance(loaded, dict) else {"value": loaded}
