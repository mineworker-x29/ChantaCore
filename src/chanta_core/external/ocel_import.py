from __future__ import annotations

import hashlib
import json
from collections import Counter
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.external.errors import (
    ExternalOCELImportCandidateError,
    ExternalOCELPayloadDescriptorError,
    ExternalOCELRiskNoteError,
    ExternalOCELSourceError,
    ExternalOCELValidationError,
)
from chanta_core.external.ids import (
    new_external_ocel_import_candidate_id,
    new_external_ocel_import_risk_note_id,
    new_external_ocel_payload_descriptor_id,
    new_external_ocel_preview_snapshot_id,
    new_external_ocel_source_id,
    new_external_ocel_validation_result_id,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


SOURCE_TYPES = {"provided_dict", "provided_json", "local_file_reference", "external_export", "manual", "other"}
TRUST_LEVELS = {"unknown", "untrusted", "local_user_provided", "trusted_project", "trusted_internal", "other"}
SOURCE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
PAYLOAD_KINDS = {"ocel_2_0", "ocel_like", "event_log", "object_log", "unknown", "other"}
DESCRIPTOR_STATUSES = {"registered", "validated", "invalid", "previewed", "archived"}
CANDIDATE_STATUSES = {"pending_review", "needs_more_info", "approved_for_design", "rejected", "archived"}
REVIEW_STATUSES = {"pending_review", "reviewed", "needs_more_info", "rejected", "archived"}
MERGE_STATUSES = {"not_merged", "merge_candidate", "rejected", "archived"}
VALIDATION_STATUSES = {"valid", "valid_with_warnings", "invalid", "needs_review", "error"}
SCHEMA_STATUSES = {"ocel_2_0_like", "ocel_like", "unknown", "invalid"}
RISK_LEVELS = {"unknown", "low", "medium", "high", "critical"}
RISK_CATEGORIES = {
    "untrusted_source",
    "large_payload",
    "unknown_schema",
    "missing_timestamps",
    "missing_object_relations",
    "potential_pii",
    "potential_secrets",
    "canonical_pollution_risk",
    "unknown",
    "other",
}


@dataclass(frozen=True)
class ExternalOCELSource:
    source_id: str
    source_name: str
    source_type: str
    source_ref: str | None
    trust_level: str
    status: str
    created_at: str
    updated_at: str
    source_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.source_name:
            raise ExternalOCELSourceError("source_name is required")
        _require(self.source_type, SOURCE_TYPES, ExternalOCELSourceError, "source_type")
        _require(self.trust_level, TRUST_LEVELS, ExternalOCELSourceError, "trust_level")
        _require(self.status, SOURCE_STATUSES, ExternalOCELSourceError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_type": self.source_type,
            "source_ref": self.source_ref,
            "trust_level": self.trust_level,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "source_attrs": dict(self.source_attrs),
        }


@dataclass(frozen=True)
class ExternalOCELPayloadDescriptor:
    descriptor_id: str
    source_id: str | None
    payload_name: str | None
    payload_kind: str
    declared_format: str | None
    declared_schema_version: str | None
    event_count: int | None
    object_count: int | None
    relation_count: int | None
    raw_payload_ref: str | None
    raw_payload_hash: str | None
    raw_payload_preview: dict[str, Any]
    status: str
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require(self.payload_kind, PAYLOAD_KINDS, ExternalOCELPayloadDescriptorError, "payload_kind")
        _require(self.status, DESCRIPTOR_STATUSES, ExternalOCELPayloadDescriptorError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "descriptor_id": self.descriptor_id,
            "source_id": self.source_id,
            "payload_name": self.payload_name,
            "payload_kind": self.payload_kind,
            "declared_format": self.declared_format,
            "declared_schema_version": self.declared_schema_version,
            "event_count": self.event_count,
            "object_count": self.object_count,
            "relation_count": self.relation_count,
            "raw_payload_ref": self.raw_payload_ref,
            "raw_payload_hash": self.raw_payload_hash,
            "raw_payload_preview": dict(self.raw_payload_preview),
            "status": self.status,
            "created_at": self.created_at,
            "descriptor_attrs": dict(self.descriptor_attrs),
        }


@dataclass(frozen=True)
class ExternalOCELImportCandidate:
    candidate_id: str
    descriptor_id: str
    source_id: str | None
    candidate_name: str | None
    candidate_status: str = "pending_review"
    review_status: str = "pending_review"
    merge_status: str = "not_merged"
    canonical_import_enabled: bool = False
    recommended_next_step: str | None = None
    validation_result_ids: list[str] = field(default_factory=list)
    preview_snapshot_ids: list[str] = field(default_factory=list)
    risk_note_ids: list[str] = field(default_factory=list)
    created_at: str = ""
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.descriptor_id:
            raise ExternalOCELImportCandidateError("descriptor_id is required")
        _require(self.candidate_status, CANDIDATE_STATUSES, ExternalOCELImportCandidateError, "candidate_status")
        _require(self.review_status, REVIEW_STATUSES, ExternalOCELImportCandidateError, "review_status")
        _require(self.merge_status, MERGE_STATUSES, ExternalOCELImportCandidateError, "merge_status")
        if self.canonical_import_enabled is not False:
            raise ExternalOCELImportCandidateError("canonical_import_enabled must be False in v0.14.4")

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "descriptor_id": self.descriptor_id,
            "source_id": self.source_id,
            "candidate_name": self.candidate_name,
            "candidate_status": self.candidate_status,
            "review_status": self.review_status,
            "merge_status": self.merge_status,
            "canonical_import_enabled": self.canonical_import_enabled,
            "recommended_next_step": self.recommended_next_step,
            "validation_result_ids": list(self.validation_result_ids),
            "preview_snapshot_ids": list(self.preview_snapshot_ids),
            "risk_note_ids": list(self.risk_note_ids),
            "created_at": self.created_at,
            "candidate_attrs": dict(self.candidate_attrs),
        }


@dataclass(frozen=True)
class ExternalOCELValidationResult:
    validation_id: str
    descriptor_id: str
    candidate_id: str | None
    status: str
    schema_status: str
    event_count: int | None
    object_count: int | None
    relation_count: int | None
    missing_fields: list[str]
    warning_messages: list[str]
    error_messages: list[str]
    created_at: str
    validation_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.descriptor_id:
            raise ExternalOCELValidationError("descriptor_id is required")
        _require(self.status, VALIDATION_STATUSES, ExternalOCELValidationError, "status")
        _require(self.schema_status, SCHEMA_STATUSES, ExternalOCELValidationError, "schema_status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "validation_id": self.validation_id,
            "descriptor_id": self.descriptor_id,
            "candidate_id": self.candidate_id,
            "status": self.status,
            "schema_status": self.schema_status,
            "event_count": self.event_count,
            "object_count": self.object_count,
            "relation_count": self.relation_count,
            "missing_fields": list(self.missing_fields),
            "warning_messages": list(self.warning_messages),
            "error_messages": list(self.error_messages),
            "created_at": self.created_at,
            "validation_attrs": dict(self.validation_attrs),
        }


@dataclass(frozen=True)
class ExternalOCELPreviewSnapshot:
    preview_id: str
    descriptor_id: str
    candidate_id: str | None
    event_count: int
    object_count: int
    relation_count: int
    event_activity_counts: dict[str, int]
    object_type_counts: dict[str, int]
    relation_type_counts: dict[str, int]
    timestamp_min: str | None
    timestamp_max: str | None
    sample_event_ids: list[str]
    sample_object_ids: list[str]
    created_at: str
    preview_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "preview_id": self.preview_id,
            "descriptor_id": self.descriptor_id,
            "candidate_id": self.candidate_id,
            "event_count": self.event_count,
            "object_count": self.object_count,
            "relation_count": self.relation_count,
            "event_activity_counts": dict(self.event_activity_counts),
            "object_type_counts": dict(self.object_type_counts),
            "relation_type_counts": dict(self.relation_type_counts),
            "timestamp_min": self.timestamp_min,
            "timestamp_max": self.timestamp_max,
            "sample_event_ids": list(self.sample_event_ids),
            "sample_object_ids": list(self.sample_object_ids),
            "created_at": self.created_at,
            "preview_attrs": dict(self.preview_attrs),
        }


@dataclass(frozen=True)
class ExternalOCELImportRiskNote:
    risk_note_id: str
    descriptor_id: str | None
    candidate_id: str | None
    risk_level: str
    risk_categories: list[str]
    message: str
    review_required: bool
    created_at: str
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require(self.risk_level, RISK_LEVELS, ExternalOCELRiskNoteError, "risk_level")
        for category in self.risk_categories:
            _require(category, RISK_CATEGORIES, ExternalOCELRiskNoteError, "risk_category")

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_note_id": self.risk_note_id,
            "descriptor_id": self.descriptor_id,
            "candidate_id": self.candidate_id,
            "risk_level": self.risk_level,
            "risk_categories": list(self.risk_categories),
            "message": self.message,
            "review_required": self.review_required,
            "created_at": self.created_at,
            "risk_attrs": dict(self.risk_attrs),
        }


def hash_payload_preview(payload: dict[str, Any]) -> str:
    preview = build_payload_preview(payload)
    encoded = json.dumps(preview, sort_keys=True, ensure_ascii=False, default=str).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def build_payload_preview(payload: dict[str, Any], max_items: int = 5) -> dict[str, Any]:
    events = _preview_items(extract_events(payload), max_items)
    objects = _preview_items(extract_objects(payload), max_items)
    relations = _preview_items(extract_relations(payload), max_items)
    return {
        "top_level_keys": sorted(str(key) for key in payload.keys()),
        "events": events,
        "objects": objects,
        "relations": relations,
    }


def detect_payload_kind(payload: dict[str, Any], declared_format: str | None = None) -> str:
    declared = _token(declared_format)
    if declared in {"ocel_2_0", "ocel2", "ocel_2"}:
        return "ocel_2_0"
    if declared in {"ocel", "ocel_like"}:
        return "ocel_like"
    keys = {_token(key) for key in payload.keys()}
    if {"ocel_events", "ocel_objects"}.issubset(keys) or {"events", "objects"}.issubset(keys):
        if "ocel_version" in keys or "ocel_global_log" in keys:
            return "ocel_2_0"
        return "ocel_like"
    if "events" in keys or "ocel_events" in keys:
        return "event_log"
    if "objects" in keys or "ocel_objects" in keys:
        return "object_log"
    return "unknown"


def extract_events(payload: dict[str, Any]) -> list[Any] | dict[str, Any]:
    return _first_payload_value(payload, ["events", "ocel:events", "ocel_events", "event_log"])


def extract_objects(payload: dict[str, Any]) -> list[Any] | dict[str, Any]:
    return _first_payload_value(payload, ["objects", "ocel:objects", "ocel_objects", "object_log"])


def extract_relations(payload: dict[str, Any]) -> list[Any] | dict[str, Any]:
    return _first_payload_value(
        payload,
        ["relations", "event_object_relations", "object_relations", "ocel:relations"],
    )


def count_event_activities(events: Any) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for _, event in _iter_items(events):
        if isinstance(event, dict):
            counter[_first_text(event, ["activity", "event_activity", "ocel:activity"], "unknown")] += 1
        else:
            counter["unknown"] += 1
    return dict(sorted(counter.items()))


def count_object_types(objects: Any) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for _, item in _iter_items(objects):
        if isinstance(item, dict):
            counter[_first_text(item, ["type", "object_type", "ocel:type"], "unknown")] += 1
        else:
            counter["unknown"] += 1
    return dict(sorted(counter.items()))


def count_relation_types(relations: Any) -> dict[str, int]:
    counter: Counter[str] = Counter()
    for _, item in _iter_items(relations):
        if isinstance(item, dict):
            counter[_first_text(item, ["type", "relation_type", "qualifier", "ocel:qualifier"], "unknown")] += 1
        else:
            counter["unknown"] += 1
    return dict(sorted(counter.items()))


def extract_timestamp_range(events: Any) -> tuple[str | None, str | None]:
    timestamps = []
    for _, event in _iter_items(events):
        if isinstance(event, dict):
            timestamp = _first_text(event, ["timestamp", "time", "event_time", "ocel:timestamp"], "")
            if timestamp:
                timestamps.append(timestamp)
    if not timestamps:
        return None, None
    return min(timestamps), max(timestamps)


def sample_ids(items: Any, id_keys: list[str]) -> list[str]:
    ids: list[str] = []
    for key, item in _iter_items(items):
        value = None
        if isinstance(item, dict):
            for id_key in id_keys:
                if item.get(id_key):
                    value = item[id_key]
                    break
        if value is None and key is not None:
            value = key
        if value is not None:
            ids.append(str(value))
        if len(ids) >= 5:
            break
    return ids


class ExternalOCELImportCandidateService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()

    def register_source(
        self,
        *,
        source_name: str,
        source_type: str = "provided_dict",
        source_ref: str | None = None,
        trust_level: str = "untrusted",
        status: str = "active",
        source_attrs: dict[str, Any] | None = None,
    ) -> ExternalOCELSource:
        now = utc_now_iso()
        source = ExternalOCELSource(
            source_id=new_external_ocel_source_id(),
            source_name=source_name,
            source_type=source_type,
            source_ref=source_ref,
            trust_level=trust_level,
            status=status,
            created_at=now,
            updated_at=now,
            source_attrs=dict(source_attrs or {}),
        )
        self._record(
            "external_ocel_source_registered",
            attrs={"source_type": source.source_type, "trust_level": source.trust_level},
            objects=[_source_object(source)],
            links=[("source_object", source.source_id)],
            object_links=[],
        )
        return source

    def register_payload_descriptor(
        self,
        *,
        payload: dict[str, Any],
        source_id: str | None = None,
        payload_name: str | None = None,
        declared_format: str | None = None,
        declared_schema_version: str | None = None,
        raw_payload_ref: str | None = None,
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> ExternalOCELPayloadDescriptor:
        if not isinstance(payload, dict):
            raise ExternalOCELPayloadDescriptorError("payload must be a dict")
        events = extract_events(payload)
        objects = extract_objects(payload)
        relations = extract_relations(payload)
        descriptor = ExternalOCELPayloadDescriptor(
            descriptor_id=new_external_ocel_payload_descriptor_id(),
            source_id=source_id,
            payload_name=payload_name or _optional_string(payload.get("name") or payload.get("id")),
            payload_kind=detect_payload_kind(payload, declared_format),
            declared_format=declared_format,
            declared_schema_version=declared_schema_version or _optional_string(payload.get("ocel:version") or payload.get("ocel_version")),
            event_count=_count_items(events),
            object_count=_count_items(objects),
            relation_count=_count_items(relations),
            raw_payload_ref=raw_payload_ref,
            raw_payload_hash=hash_payload_preview(payload),
            raw_payload_preview=build_payload_preview(payload),
            status="registered",
            created_at=utc_now_iso(),
            descriptor_attrs={
                **dict(descriptor_attrs or {}),
                "untrusted_input": True,
                "canonical_import_enabled": False,
                "canonical_merge_performed": False,
            },
        )
        self._record(
            "external_ocel_payload_registered",
            attrs={"payload_kind": descriptor.payload_kind, "canonical_import_enabled": False},
            objects=[_descriptor_object(descriptor)],
            links=[("descriptor_object", descriptor.descriptor_id), ("source_object", source_id or "")],
            object_links=[(descriptor.descriptor_id, source_id or "", "from_source")],
        )
        return descriptor

    def validate_payload(
        self,
        *,
        payload: dict[str, Any],
        descriptor: ExternalOCELPayloadDescriptor,
        candidate_id: str | None = None,
    ) -> ExternalOCELValidationResult:
        self._record(
            "external_ocel_validation_started",
            attrs={"descriptor_id": descriptor.descriptor_id, "canonical_import_enabled": False},
            objects=[_descriptor_object(descriptor)],
            links=[("descriptor_object", descriptor.descriptor_id), ("candidate_object", candidate_id or "")],
            object_links=[],
        )
        events = extract_events(payload)
        objects = extract_objects(payload)
        relations = extract_relations(payload)
        missing: list[str] = []
        warnings: list[str] = []
        errors: list[str] = []
        if _count_items(events) == 0:
            missing.append("events")
            errors.append("No events found in external OCEL payload.")
        if _count_items(objects) == 0:
            missing.append("objects")
            warnings.append("No objects found in external OCEL payload.")
        if _count_items(relations) == 0:
            missing.append("relations")
            warnings.append("No relations found in external OCEL payload.")
        if extract_timestamp_range(events) == (None, None) and _count_items(events) > 0:
            warnings.append("No event timestamps found in external OCEL payload.")
        schema_status = _schema_status(descriptor.payload_kind, missing, errors)
        status = "invalid" if errors else "valid_with_warnings" if warnings else "valid"
        if schema_status == "unknown" and status == "valid":
            status = "needs_review"
        validation = ExternalOCELValidationResult(
            validation_id=new_external_ocel_validation_result_id(),
            descriptor_id=descriptor.descriptor_id,
            candidate_id=candidate_id,
            status=status,
            schema_status=schema_status,
            event_count=_count_items(events),
            object_count=_count_items(objects),
            relation_count=_count_items(relations),
            missing_fields=missing,
            warning_messages=warnings,
            error_messages=errors,
            created_at=utc_now_iso(),
            validation_attrs={
                "structural_only": True,
                "canonical_import_enabled": False,
                "canonical_merge_performed": False,
            },
        )
        self._record(
            "external_ocel_validation_recorded",
            attrs={"status": validation.status, "schema_status": validation.schema_status},
            objects=[_descriptor_object(descriptor), _validation_object(validation)],
            links=[
                ("validation_object", validation.validation_id),
                ("descriptor_object", descriptor.descriptor_id),
                ("candidate_object", candidate_id or ""),
            ],
            object_links=[
                (validation.validation_id, descriptor.descriptor_id, "validates_descriptor"),
                (validation.validation_id, candidate_id or "", "validates_candidate"),
            ],
        )
        return validation

    def create_preview_snapshot(
        self,
        *,
        payload: dict[str, Any],
        descriptor_id: str,
        candidate_id: str | None = None,
    ) -> ExternalOCELPreviewSnapshot:
        events = extract_events(payload)
        objects = extract_objects(payload)
        relations = extract_relations(payload)
        timestamp_min, timestamp_max = extract_timestamp_range(events)
        preview = ExternalOCELPreviewSnapshot(
            preview_id=new_external_ocel_preview_snapshot_id(),
            descriptor_id=descriptor_id,
            candidate_id=candidate_id,
            event_count=_count_items(events),
            object_count=_count_items(objects),
            relation_count=_count_items(relations),
            event_activity_counts=count_event_activities(events),
            object_type_counts=count_object_types(objects),
            relation_type_counts=count_relation_types(relations),
            timestamp_min=timestamp_min,
            timestamp_max=timestamp_max,
            sample_event_ids=sample_ids(events, ["id", "event_id", "ocel:eid"]),
            sample_object_ids=sample_ids(objects, ["id", "object_id", "ocel:oid"]),
            created_at=utc_now_iso(),
            preview_attrs={
                "read_model_only": True,
                "canonical_import_enabled": False,
                "canonical_merge_performed": False,
            },
        )
        self._record(
            "external_ocel_preview_created",
            attrs={"event_count": preview.event_count, "object_count": preview.object_count},
            objects=[_preview_object(preview)],
            links=[
                ("preview_object", preview.preview_id),
                ("descriptor_object", descriptor_id),
                ("candidate_object", candidate_id or ""),
            ],
            object_links=[
                (preview.preview_id, descriptor_id, "previews_descriptor"),
                (preview.preview_id, candidate_id or "", "previews_candidate"),
            ],
        )
        return preview

    def record_risk_note(
        self,
        *,
        descriptor_id: str | None = None,
        candidate_id: str | None = None,
        risk_level: str,
        risk_categories: list[str],
        message: str,
        review_required: bool = True,
        risk_attrs: dict[str, Any] | None = None,
    ) -> ExternalOCELImportRiskNote:
        normalized = [_normalize_risk_category(item) for item in risk_categories]
        note = ExternalOCELImportRiskNote(
            risk_note_id=new_external_ocel_import_risk_note_id(),
            descriptor_id=descriptor_id,
            candidate_id=candidate_id,
            risk_level=risk_level,
            risk_categories=normalized,
            message=message,
            review_required=review_required,
            created_at=utc_now_iso(),
            risk_attrs=dict(risk_attrs or {}),
        )
        self._record(
            "external_ocel_risk_note_recorded",
            attrs={"risk_level": note.risk_level, "review_required": note.review_required},
            objects=[_risk_note_object(note)],
            links=[
                ("risk_note_object", note.risk_note_id),
                ("descriptor_object", descriptor_id or ""),
                ("candidate_object", candidate_id or ""),
            ],
            object_links=[
                (note.risk_note_id, descriptor_id or "", "describes_descriptor"),
                (note.risk_note_id, candidate_id or "", "describes_candidate"),
            ],
        )
        return note

    def create_import_candidate(
        self,
        *,
        descriptor: ExternalOCELPayloadDescriptor,
        candidate_name: str | None = None,
        recommended_next_step: str | None = None,
        validation_result_ids: list[str] | None = None,
        preview_snapshot_ids: list[str] | None = None,
        risk_note_ids: list[str] | None = None,
        candidate_attrs: dict[str, Any] | None = None,
    ) -> ExternalOCELImportCandidate:
        candidate = ExternalOCELImportCandidate(
            candidate_id=new_external_ocel_import_candidate_id(),
            descriptor_id=descriptor.descriptor_id,
            source_id=descriptor.source_id,
            candidate_name=candidate_name or descriptor.payload_name,
            candidate_status="pending_review",
            review_status="pending_review",
            merge_status="not_merged",
            canonical_import_enabled=False,
            recommended_next_step=recommended_next_step,
            validation_result_ids=list(validation_result_ids or []),
            preview_snapshot_ids=list(preview_snapshot_ids or []),
            risk_note_ids=list(risk_note_ids or []),
            created_at=utc_now_iso(),
            candidate_attrs={
                **dict(candidate_attrs or {}),
                "review_required": True,
                "canonical_merge_performed": False,
            },
        )
        self._record(
            "external_ocel_candidate_created",
            attrs={"canonical_import_enabled": False, "merge_status": "not_merged"},
            objects=[_descriptor_object(descriptor), _candidate_object(candidate)],
            links=[
                ("candidate_object", candidate.candidate_id),
                ("descriptor_object", descriptor.descriptor_id),
                ("source_object", descriptor.source_id or ""),
            ],
            object_links=[
                (candidate.candidate_id, descriptor.descriptor_id, "derived_from_descriptor"),
                (candidate.candidate_id, descriptor.source_id or "", "from_source"),
            ],
        )
        self._record(
            "external_ocel_candidate_review_required",
            attrs={"review_status": "pending_review", "canonical_import_enabled": False},
            objects=[_candidate_object(candidate)],
            links=[("candidate_object", candidate.candidate_id)],
            object_links=[],
        )
        return candidate

    def register_as_candidate(
        self,
        *,
        payload: dict[str, Any],
        source: ExternalOCELSource | None = None,
        payload_name: str | None = None,
        declared_format: str | None = None,
        declared_schema_version: str | None = None,
        recommended_next_step: str | None = None,
    ) -> tuple[
        ExternalOCELPayloadDescriptor,
        ExternalOCELValidationResult,
        ExternalOCELPreviewSnapshot,
        ExternalOCELImportCandidate,
    ]:
        descriptor = self.register_payload_descriptor(
            payload=payload,
            source_id=source.source_id if source else None,
            payload_name=payload_name,
            declared_format=declared_format,
            declared_schema_version=declared_schema_version,
        )
        validation = self.validate_payload(payload=payload, descriptor=descriptor)
        preview = self.create_preview_snapshot(payload=payload, descriptor_id=descriptor.descriptor_id)
        risk_note_ids: list[str] = []
        risk_categories = _risk_categories_for_payload(
            source=source,
            validation=validation,
            preview=preview,
            payload_kind=descriptor.payload_kind,
        )
        if risk_categories:
            note = self.record_risk_note(
                descriptor_id=descriptor.descriptor_id,
                risk_level=_risk_level_for_categories(risk_categories),
                risk_categories=risk_categories,
                message="External OCEL payload is review-required and not merged into canonical OCEL.",
                review_required=True,
                risk_attrs={"structural_validation_status": validation.status},
            )
            risk_note_ids.append(note.risk_note_id)
        candidate = self.create_import_candidate(
            descriptor=descriptor,
            candidate_name=payload_name or descriptor.payload_name,
            recommended_next_step=recommended_next_step or "Review external OCEL preview before any future controlled import.",
            validation_result_ids=[validation.validation_id],
            preview_snapshot_ids=[preview.preview_id],
            risk_note_ids=risk_note_ids,
        )
        return descriptor, validation, preview, candidate

    def _record(
        self,
        activity: str,
        *,
        attrs: dict[str, Any],
        objects: list[OCELObject],
        links: list[tuple[str, str]],
        object_links: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **attrs,
                "runtime_event_type": activity,
                "source_runtime": "chanta_core",
                "external_ocel_import_candidate_only": True,
                "observability_only": True,
                "canonical_import_enabled": False,
                "canonical_merge_performed": False,
                "runtime_effect": False,
            },
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in links
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_links
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))


def _source_object(source: ExternalOCELSource) -> OCELObject:
    return OCELObject(
        object_id=source.source_id,
        object_type="external_ocel_source",
        object_attrs={**source.to_dict(), "object_key": source.source_id, "display_name": source.source_name},
    )


def _descriptor_object(descriptor: ExternalOCELPayloadDescriptor) -> OCELObject:
    return OCELObject(
        object_id=descriptor.descriptor_id,
        object_type="external_ocel_payload_descriptor",
        object_attrs={
            **descriptor.to_dict(),
            "object_key": descriptor.descriptor_id,
            "display_name": descriptor.payload_name or descriptor.payload_kind,
            "canonical_import_enabled": False,
        },
    )


def _candidate_object(candidate: ExternalOCELImportCandidate) -> OCELObject:
    return OCELObject(
        object_id=candidate.candidate_id,
        object_type="external_ocel_import_candidate",
        object_attrs={
            **candidate.to_dict(),
            "object_key": candidate.candidate_id,
            "display_name": candidate.candidate_name or candidate.candidate_id,
            "canonical_import_enabled": False,
            "merge_status": "not_merged",
        },
    )


def _validation_object(validation: ExternalOCELValidationResult) -> OCELObject:
    return OCELObject(
        object_id=validation.validation_id,
        object_type="external_ocel_validation_result",
        object_attrs={**validation.to_dict(), "object_key": validation.validation_id, "display_name": validation.status},
    )


def _preview_object(preview: ExternalOCELPreviewSnapshot) -> OCELObject:
    return OCELObject(
        object_id=preview.preview_id,
        object_type="external_ocel_preview_snapshot",
        object_attrs={**preview.to_dict(), "object_key": preview.preview_id, "display_name": "external_ocel_preview"},
    )


def _risk_note_object(note: ExternalOCELImportRiskNote) -> OCELObject:
    return OCELObject(
        object_id=note.risk_note_id,
        object_type="external_ocel_import_risk_note",
        object_attrs={**note.to_dict(), "object_key": note.risk_note_id, "display_name": note.risk_level},
    )


def _require(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


def _first_payload_value(payload: dict[str, Any], keys: list[str]) -> list[Any] | dict[str, Any]:
    for key in keys:
        if key in payload:
            value = payload[key]
            if isinstance(value, (list, dict)):
                return value
    return []


def _iter_items(items: Any):
    if isinstance(items, dict):
        for key, value in items.items():
            yield str(key), value
    elif isinstance(items, list):
        for value in items:
            yield None, value


def _count_items(items: Any) -> int:
    if isinstance(items, (list, dict)):
        return len(items)
    return 0


def _preview_items(items: Any, max_items: int) -> list[Any] | dict[str, Any]:
    if isinstance(items, list):
        return items[:max_items]
    if isinstance(items, dict):
        return {key: items[key] for key in list(items.keys())[:max_items]}
    return []


def _first_text(item: dict[str, Any], keys: list[str], default: str) -> str:
    for key in keys:
        if item.get(key) is not None:
            return str(item[key])
    return default


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _token(value: Any) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_").replace(":", "_")


def _schema_status(payload_kind: str, missing: list[str], errors: list[str]) -> str:
    if errors:
        return "invalid"
    if payload_kind == "ocel_2_0":
        return "ocel_2_0_like"
    if payload_kind in {"ocel_like", "event_log", "object_log"}:
        return "ocel_like"
    return "unknown" if missing else "ocel_like"


def _normalize_risk_category(value: str) -> str:
    token = _token(value)
    return token if token in RISK_CATEGORIES else "other"


def _risk_categories_for_payload(
    *,
    source: ExternalOCELSource | None,
    validation: ExternalOCELValidationResult,
    preview: ExternalOCELPreviewSnapshot,
    payload_kind: str,
) -> list[str]:
    categories = ["canonical_pollution_risk"]
    if source is None or source.trust_level in {"unknown", "untrusted"}:
        categories.append("untrusted_source")
    if payload_kind == "unknown" or validation.schema_status == "unknown":
        categories.append("unknown_schema")
    if any("timestamp" in message for message in validation.warning_messages):
        categories.append("missing_timestamps")
    if "relations" in validation.missing_fields:
        categories.append("missing_object_relations")
    if preview.event_count + preview.object_count + preview.relation_count > 10000:
        categories.append("large_payload")
    return list(dict.fromkeys(categories))


def _risk_level_for_categories(categories: list[str]) -> str:
    if "canonical_pollution_risk" in categories and "unknown_schema" in categories:
        return "high"
    if "large_payload" in categories:
        return "high"
    if "untrusted_source" in categories or "missing_object_relations" in categories:
        return "medium"
    return "low"
