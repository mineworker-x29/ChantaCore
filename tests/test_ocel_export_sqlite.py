import sqlite3

import pytest

from chanta_core.ocel.export import OCELExporter
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELRelation, OCELEvent
from chanta_core.ocel.store import OCELStore


def test_export_sqlite_copy_creates_openable_copy(tmp_path) -> None:
    store = OCELStore(tmp_path / "source.sqlite")
    event = OCELEvent("event:sqlite-copy", "receive_user_request", "2026-05-03T00:00:00Z")
    obj = OCELObject("session:sqlite-copy", "session")
    store.append_record(
        OCELRecord(
            event=event,
            objects=[obj],
            relations=[
                OCELRelation.event_object(
                    event_id=event.event_id,
                    object_id=obj.object_id,
                    qualifier="session_context",
                )
            ],
        )
    )

    target = OCELExporter(store).export_sqlite_copy(tmp_path / "exports" / "copy.sqlite")

    assert target.exists()
    with sqlite3.connect(target) as connection:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    assert "event" in tables
    assert "chanta_event_payload" in tables


def test_export_sqlite_copy_missing_source_fails(tmp_path) -> None:
    with pytest.raises(FileNotFoundError):
        OCELExporter(OCELStore(tmp_path / "missing.sqlite")).export_sqlite_copy(
            tmp_path / "copy.sqlite"
        )
