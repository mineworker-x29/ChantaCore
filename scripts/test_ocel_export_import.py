from __future__ import annotations

import tempfile
from pathlib import Path

from chanta_core.ocel.export import OCELExporter
from chanta_core.ocel.importers import OCELImporter
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELRelation, OCELEvent
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator


def main() -> None:
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as tmp:
        root = Path(tmp)
        source = OCELStore(root / "source.sqlite")
        event = OCELEvent(
            "event:script-export",
            "receive_user_request",
            "2026-05-03T00:00:00Z",
            {"source": "script"},
        )
        obj = OCELObject("session:script-export", "session", {})
        source.append_record(
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
        export_path = OCELExporter(source).export_chanta_json(root / "export.json")
        target = OCELStore(root / "target.sqlite")
        result = OCELImporter(target).import_chanta_json(export_path)
        readiness = OCELValidator(target).validate_export_readiness()
        print(f"success={result.success}")
        print(f"accepted={len(result.accepted_record_ids)}")
        print(f"event_count={target.fetch_event_count()}")
        print(f"export_readiness={readiness['valid']}")


if __name__ == "__main__":
    main()
