from __future__ import annotations

import json
import shutil
from pathlib import Path
from uuid import uuid4

from chanta_core.ocel.export import CHANTA_OCEL_JSON_FORMAT
from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.ingestion import OCELIngestionBatch, OCELIngestionResult
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELRelation, OCELEvent
from chanta_core.ocel.store import OCELStore
from chanta_core.utility.time import utc_now_iso


class OCELImporter:
    """Safe importer for ChantaCore canonical JSON and SQLite copy placeholders."""

    def __init__(self, store: OCELStore | None = None) -> None:
        self.store = store or OCELStore()

    def import_sqlite(self, source_path: str | Path) -> None:
        source = Path(source_path)
        if not source.is_file():
            raise FileNotFoundError(source)
        self.store.db_path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, self.store.db_path)

    def import_chanta_json(self, source_path: str | Path) -> OCELIngestionResult:
        source = Path(source_path)
        loaded = json.loads(source.read_text(encoding="utf-8"))
        if not isinstance(loaded, dict) or loaded.get("format") != CHANTA_OCEL_JSON_FORMAT:
            raise ValueError("JSON file is not ChantaCore canonical OCEL JSON")

        events = _list_of_dicts(loaded.get("events"), "events")
        objects = _list_of_dicts(loaded.get("objects"), "objects")
        relations = _list_of_dicts(loaded.get("relations"), "relations")
        object_items = [_object_from_dict(item) for item in objects]
        relation_items = [_relation_from_dict(item) for item in relations]

        accepted_record_ids: list[str] = []
        rejected_records: list[dict] = []
        errors: list[str] = []
        for index, event_raw in enumerate(events):
            try:
                event = _event_from_dict(event_raw)
                record = OCELRecord(
                    event=event,
                    objects=object_items,
                    relations=relation_items,
                )
                self.store.append_record(record)
                accepted_record_ids.append(event.event_id)
            except Exception as error:
                errors.append(str(error))
                rejected_records.append(
                    {"index": index, "error": str(error), "raw_record": event_raw}
                )

        batch = OCELIngestionBatch(
            batch_id=f"ocel_ingestion:{uuid4()}",
            source=ExternalOCELSource(
                source_id=f"chanta_json:{source.stem}",
                source_name=str(source),
                source_type="file",
                source_format=CHANTA_OCEL_JSON_FORMAT,
                source_attrs={
                    "internal_canonical": True,
                    "idempotent_ids": True,
                    "full_ocel2_json": False,
                },
            ),
            imported_at=utc_now_iso(),
            records_seen=len(events),
            records_accepted=len(accepted_record_ids),
            records_rejected=len(rejected_records),
            warnings=[],
            errors=errors,
            batch_attrs={"importer": "OCELImporter.import_chanta_json"},
        )
        return OCELIngestionResult(
            success=bool(accepted_record_ids) and not rejected_records,
            batch=batch,
            accepted_record_ids=accepted_record_ids,
            rejected_records=rejected_records,
            result_attrs={
                "store_path": str(self.store.db_path),
                "source_path": str(source),
                "id_collision_strategy": "idempotent_insert_or_replace",
            },
        )


def _event_from_dict(data: dict) -> OCELEvent:
    attrs = dict(data.get("event_attrs") or {})
    attrs["imported_from_chanta_json"] = True
    return OCELEvent(
        event_id=str(data["event_id"]),
        event_activity=str(data["event_activity"]),
        event_timestamp=str(data["event_timestamp"]),
        event_attrs=attrs,
    )


def _object_from_dict(data: dict) -> OCELObject:
    attrs = dict(data.get("object_attrs") or {})
    attrs["imported_from_chanta_json"] = True
    return OCELObject(
        object_id=str(data["object_id"]),
        object_type=str(data["object_type"]),
        object_attrs=attrs,
    )


def _relation_from_dict(data: dict) -> OCELRelation:
    attrs = dict(data.get("relation_attrs") or {})
    attrs["imported_from_chanta_json"] = True
    return OCELRelation(
        relation_kind=str(data["relation_kind"]),
        source_id=str(data["source_id"]),
        target_id=str(data["target_id"]),
        qualifier=str(data["qualifier"]),
        relation_attrs=attrs,
    )


def _list_of_dicts(value, field_name: str) -> list[dict]:
    if value is None:
        return []
    if not isinstance(value, list):
        raise ValueError(f"{field_name} must be a list")
    if not all(isinstance(item, dict) for item in value):
        raise ValueError(f"{field_name} entries must be objects")
    return value
