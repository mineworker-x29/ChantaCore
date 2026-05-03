from __future__ import annotations

import json
from pathlib import Path
from typing import Any
from uuid import uuid4

from chanta_core.ocel.external_source import ExternalOCELSource
from chanta_core.ocel.export import CHANTA_OCEL_JSON_FORMAT
from chanta_core.ocel.importers import OCELImporter
from chanta_core.ocel.ingestion import OCELIngestionBatch, OCELIngestionResult
from chanta_core.ocel.models import OCELObject, OCELRecord, OCELRelation, OCELEvent
from chanta_core.ocel.store import OCELStore
from chanta_core.utility.time import utc_now_iso


class ExternalOCELNormalizer:
    def normalize_record(
        self,
        source: ExternalOCELSource,
        raw_record: dict[str, Any],
    ) -> OCELRecord:
        if not isinstance(raw_record, dict):
            raise ValueError("raw_record must be a dictionary")
        event_raw = raw_record.get("event")
        if not isinstance(event_raw, dict):
            raise ValueError("raw_record.event must be a dictionary")

        original_event_id = self._required_text(event_raw, "event_id")
        event_activity = self._required_text(event_raw, "event_activity")
        event_timestamp = self._required_text(event_raw, "event_timestamp")
        event_id = self._event_id(source, original_event_id)
        event_attrs = {
            **self._dict_value(event_raw.get("event_attrs")),
            "external_source_id": source.source_id,
            "external_source_name": source.source_name,
            "external_event_id": original_event_id,
            "imported": True,
        }
        event = OCELEvent(
            event_id=event_id,
            event_activity=event_activity,
            event_timestamp=event_timestamp,
            event_attrs=event_attrs,
        )

        objects = []
        object_id_map: dict[str, str] = {}
        for object_raw in self._list_value(raw_record.get("objects"), "objects"):
            if not isinstance(object_raw, dict):
                raise ValueError("objects entries must be dictionaries")
            original_object_id = self._required_text(object_raw, "object_id")
            object_id = self._object_id(source, original_object_id)
            object_id_map[original_object_id] = object_id
            objects.append(
                OCELObject(
                    object_id=object_id,
                    object_type=self._required_text(object_raw, "object_type"),
                    object_attrs={
                        **self._dict_value(object_raw.get("object_attrs")),
                        "external_source_id": source.source_id,
                        "external_object_id": original_object_id,
                        "imported": True,
                    },
                )
            )

        relations = []
        for relation_raw in self._list_value(raw_record.get("relations"), "relations"):
            if not isinstance(relation_raw, dict):
                raise ValueError("relations entries must be dictionaries")
            relation_kind = self._required_text(relation_raw, "relation_kind")
            source_id = self._required_text(relation_raw, "source_id")
            target_id = self._required_text(relation_raw, "target_id")
            qualifier = self._required_text(relation_raw, "qualifier")
            relation_attrs = {
                **self._dict_value(relation_raw.get("relation_attrs")),
                "external_source_id": source.source_id,
                "imported": True,
            }
            if relation_kind == "event_object":
                if source_id != original_event_id:
                    raise ValueError("event_object relation source_id must match event_id")
                if target_id not in object_id_map:
                    raise ValueError("event_object relation target_id is unknown")
                relations.append(
                    OCELRelation.event_object(
                        event_id=event_id,
                        object_id=object_id_map[target_id],
                        qualifier=qualifier,
                        relation_attrs=relation_attrs,
                    )
                )
            elif relation_kind == "object_object":
                if source_id not in object_id_map or target_id not in object_id_map:
                    raise ValueError("object_object relation references unknown object")
                relations.append(
                    OCELRelation.object_object(
                        source_object_id=object_id_map[source_id],
                        target_object_id=object_id_map[target_id],
                        qualifier=qualifier,
                        relation_attrs=relation_attrs,
                    )
                )
            else:
                raise ValueError(f"Unsupported relation_kind: {relation_kind}")

        return OCELRecord(event=event, objects=objects, relations=relations)

    @staticmethod
    def _event_id(source: ExternalOCELSource, original_event_id: str) -> str:
        return f"external:{source.source_id}:event:{original_event_id}"

    @staticmethod
    def _object_id(source: ExternalOCELSource, original_object_id: str) -> str:
        return f"external:{source.source_id}:object:{original_object_id}"

    @staticmethod
    def _required_text(item: dict[str, Any], key: str) -> str:
        value = item.get(key)
        if value is None or str(value).strip() == "":
            raise ValueError(f"Missing required field: {key}")
        return str(value)

    @staticmethod
    def _dict_value(value: Any) -> dict[str, Any]:
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("Expected dictionary value")
        return dict(value)

    @staticmethod
    def _list_value(value: Any, field_name: str) -> list[Any]:
        if value is None:
            return []
        if not isinstance(value, list):
            raise ValueError(f"{field_name} must be a list")
        return value


class ExternalOCELIngestionService:
    def __init__(
        self,
        *,
        store: OCELStore | None = None,
        normalizer: ExternalOCELNormalizer | None = None,
    ) -> None:
        self.store = store or OCELStore()
        self.normalizer = normalizer or ExternalOCELNormalizer()

    def ingest_records(
        self,
        source: ExternalOCELSource,
        raw_records: list[dict[str, Any]],
    ) -> OCELIngestionResult:
        accepted_record_ids: list[str] = []
        rejected_records: list[dict[str, Any]] = []
        errors: list[str] = []
        warnings: list[str] = []

        for index, raw_record in enumerate(raw_records):
            try:
                record = self.normalizer.normalize_record(source, raw_record)
                self.store.append_record(record, raw_event=raw_record)
                accepted_record_ids.append(record.event.event_id)
            except Exception as error:
                message = str(error)
                errors.append(message)
                rejected_records.append(
                    {
                        "index": index,
                        "error": message,
                        "raw_record": raw_record,
                    }
                )

        batch = OCELIngestionBatch(
            batch_id=f"ocel_ingestion:{uuid4()}",
            source=source,
            imported_at=utc_now_iso(),
            records_seen=len(raw_records),
            records_accepted=len(accepted_record_ids),
            records_rejected=len(rejected_records),
            warnings=warnings,
            errors=errors,
            batch_attrs={"normalizer": "ExternalOCELNormalizer"},
        )
        return OCELIngestionResult(
            success=bool(accepted_record_ids),
            batch=batch,
            accepted_record_ids=accepted_record_ids,
            rejected_records=rejected_records,
            result_attrs={"store_path": str(self.store.db_path)},
        )

    def ingest_json_file(
        self,
        source: ExternalOCELSource,
        path: str | Path,
    ) -> OCELIngestionResult:
        file_path = Path(path)
        loaded = json.loads(file_path.read_text(encoding="utf-8"))
        if isinstance(loaded, dict) and loaded.get("format") == CHANTA_OCEL_JSON_FORMAT:
            return OCELImporter(self.store).import_chanta_json(file_path)
        if isinstance(loaded, dict) and isinstance(loaded.get("records"), list):
            raw_records = loaded["records"]
        elif isinstance(loaded, list):
            raw_records = loaded
        else:
            raise ValueError("External OCEL JSON must be a list or contain records list")
        return self.ingest_records(source, raw_records)
