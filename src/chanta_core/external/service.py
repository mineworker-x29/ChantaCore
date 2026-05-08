from __future__ import annotations

from dataclasses import replace
from typing import Any
from uuid import uuid4

from chanta_core.external.errors import (
    ExternalAssimilationCandidateError,
    ExternalCapabilityDescriptorError,
)
from chanta_core.external.ids import (
    new_external_assimilation_candidate_id,
    new_external_capability_descriptor_id,
    new_external_capability_import_batch_id,
    new_external_capability_normalization_id,
    new_external_capability_risk_note_id,
    new_external_capability_source_id,
)
from chanta_core.external.models import (
    ExternalAssimilationCandidate,
    ExternalCapabilityDescriptor,
    ExternalCapabilityImportBatch,
    ExternalCapabilityNormalizationResult,
    ExternalCapabilityRiskNote,
    ExternalCapabilitySource,
)
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


_CAPABILITY_TYPE_ALIASES = {
    "tool": "tool",
    "skill": "skill",
    "adapter": "adapter",
    "connector": "connector",
    "mcp": "mcp_server",
    "mcp_server": "mcp_server",
    "plugin": "plugin",
    "agent": "agent",
    "workflow": "workflow",
}
_PERMISSION_ALIASES = {
    "read_file": "filesystem_read",
    "filesystem_read": "filesystem_read",
    "write_file": "filesystem_write",
    "filesystem_write": "filesystem_write",
    "shell": "shell_execution",
    "shell_execution": "shell_execution",
    "network": "network_access",
    "network_access": "network_access",
    "secrets": "credential_access",
    "credential_access": "credential_access",
    "external_code": "external_code_execution",
    "external_code_execution": "external_code_execution",
    "data_exfiltration": "data_exfiltration",
    "permission_escalation": "permission_escalation",
}
_RISK_ALIASES = {
    **_PERMISSION_ALIASES,
    "exfiltration": "data_exfiltration",
    "credentials": "credential_access",
    "unknown": "unknown",
    "other": "other",
}
_HIGH_RISK_CATEGORIES = {
    "shell_execution",
    "credential_access",
    "permission_escalation",
}
_CRITICAL_RISK_CATEGORIES = {
    "external_code_execution",
    "data_exfiltration",
}
_MEDIUM_RISK_CATEGORIES = {
    "filesystem_write",
    "network_access",
}


def normalize_capability_type(value: str | None) -> str:
    key = _normalize_token(value)
    return _CAPABILITY_TYPE_ALIASES.get(key, "other")


def normalize_permission(value: str) -> str:
    key = _normalize_token(value)
    return _PERMISSION_ALIASES.get(key, "other")


def normalize_risk_category(value: str) -> str:
    key = _normalize_token(value)
    return _RISK_ALIASES.get(key, "unknown" if not key else "other")


def infer_risk_level(risk_categories: list[str]) -> str:
    categories = {normalize_risk_category(item) for item in risk_categories}
    if categories & _CRITICAL_RISK_CATEGORIES:
        return "critical"
    if categories & _HIGH_RISK_CATEGORIES:
        return "high"
    if categories & _MEDIUM_RISK_CATEGORIES:
        return "medium"
    if "unknown" in categories:
        return "unknown"
    if categories - {"other"}:
        return "low"
    return "unknown" if not categories else "low"


def extract_descriptor_name(raw_descriptor: dict[str, Any]) -> str:
    for key in ["name", "capability_name", "tool_name", "skill_name", "id"]:
        value = raw_descriptor.get(key)
        if value:
            return str(value)
    return "unnamed_external_capability"


def extract_descriptor_type(raw_descriptor: dict[str, Any]) -> str:
    for key in ["type", "capability_type", "kind"]:
        value = raw_descriptor.get(key)
        if value:
            return normalize_capability_type(str(value))
    return "other"


class ExternalCapabilityImportService:
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
        source_type: str,
        source_ref: str | None = None,
        trust_level: str = "unknown",
        status: str = "active",
        source_attrs: dict[str, Any] | None = None,
    ) -> ExternalCapabilitySource:
        now = utc_now_iso()
        source = ExternalCapabilitySource(
            source_id=new_external_capability_source_id(),
            source_name=source_name,
            source_type=source_type,
            source_ref=source_ref,
            trust_level=trust_level,
            status=status,
            created_at=now,
            updated_at=now,
            source_attrs=dict(source_attrs or {}),
        )
        self._record_event(
            "external_capability_source_registered",
            source=source,
            event_attrs={"source_type": source.source_type, "trust_level": source.trust_level},
            event_relations=[("source_object", source.source_id)],
            object_relations=[],
        )
        return source

    def import_descriptor(
        self,
        *,
        raw_descriptor: dict[str, Any],
        source_id: str | None = None,
        descriptor_attrs: dict[str, Any] | None = None,
    ) -> ExternalCapabilityDescriptor:
        if not isinstance(raw_descriptor, dict):
            self._record_event(
                "external_capability_descriptor_invalid",
                event_attrs={"reason": "raw_descriptor must be a dict"},
                event_relations=[("source_object", source_id or "")],
                object_relations=[],
            )
            raise ExternalCapabilityDescriptorError("raw_descriptor must be a dict")
        permissions = _list_of_strings(
            raw_descriptor.get("permissions")
            or raw_descriptor.get("declared_permissions")
            or raw_descriptor.get("requires")
            or []
        )
        risks = _list_of_strings(raw_descriptor.get("risks") or raw_descriptor.get("declared_risks") or [])
        descriptor = ExternalCapabilityDescriptor(
            descriptor_id=new_external_capability_descriptor_id(),
            source_id=source_id,
            capability_name=extract_descriptor_name(raw_descriptor),
            capability_type=extract_descriptor_type(raw_descriptor),
            description=_optional_string(raw_descriptor.get("description")),
            provider=_optional_string(raw_descriptor.get("provider")),
            version=_optional_string(raw_descriptor.get("version")),
            declared_inputs=_dict_value(raw_descriptor.get("inputs") or raw_descriptor.get("declared_inputs")),
            declared_outputs=_dict_value(raw_descriptor.get("outputs") or raw_descriptor.get("declared_outputs")),
            declared_permissions=permissions,
            declared_risks=risks,
            declared_entrypoint=_optional_string(
                raw_descriptor.get("entrypoint") or raw_descriptor.get("declared_entrypoint")
            ),
            raw_descriptor=dict(raw_descriptor),
            normalized=False,
            status="imported",
            created_at=utc_now_iso(),
            descriptor_attrs={**dict(descriptor_attrs or {}), "untrusted_input": True},
        )
        self._record_event(
            "external_capability_descriptor_imported",
            descriptor=descriptor,
            event_attrs={"capability_type": descriptor.capability_type, "untrusted_input": True},
            event_relations=[
                ("descriptor_object", descriptor.descriptor_id),
                ("source_object", source_id or ""),
            ],
            object_relations=[
                (descriptor.descriptor_id, source_id or "", "from_source"),
            ],
        )
        return descriptor

    def import_descriptors(
        self,
        *,
        raw_descriptors: list[dict[str, Any]],
        source_id: str | None = None,
        batch_name: str | None = None,
        batch_attrs: dict[str, Any] | None = None,
    ) -> ExternalCapabilityImportBatch:
        batch = ExternalCapabilityImportBatch(
            batch_id=new_external_capability_import_batch_id(),
            source_id=source_id,
            batch_name=batch_name,
            imported_descriptor_ids=[],
            failed_descriptor_refs=[],
            status="started",
            created_at=utc_now_iso(),
            batch_attrs=dict(batch_attrs or {}),
        )
        self._record_batch_event(
            "external_capability_import_started",
            batch=batch,
            source_id=source_id,
            descriptor_ids=[],
        )
        imported_ids: list[str] = []
        failed_refs: list[str] = []
        for index, raw_descriptor in enumerate(raw_descriptors):
            try:
                descriptor = self.import_descriptor(raw_descriptor=raw_descriptor, source_id=source_id)
                imported_ids.append(descriptor.descriptor_id)
            except Exception:
                failed_refs.append(_failed_descriptor_ref(raw_descriptor, index))
        if failed_refs and imported_ids:
            status = "completed_with_errors"
            activity = "external_capability_import_completed"
        elif failed_refs:
            status = "failed"
            activity = "external_capability_import_failed"
        else:
            status = "completed"
            activity = "external_capability_import_completed"
        completed = replace(
            batch,
            imported_descriptor_ids=imported_ids,
            failed_descriptor_refs=failed_refs,
            status=status,
        )
        self._record_batch_event(
            activity,
            batch=completed,
            source_id=source_id,
            descriptor_ids=imported_ids,
        )
        return completed

    def normalize_descriptor(
        self,
        *,
        descriptor: ExternalCapabilityDescriptor,
    ) -> ExternalCapabilityNormalizationResult:
        normalized_type = normalize_capability_type(descriptor.capability_type)
        normalized_permissions = [normalize_permission(item) for item in descriptor.declared_permissions]
        normalized_risks = [normalize_risk_category(item) for item in descriptor.declared_risks]
        for permission in normalized_permissions:
            if permission not in normalized_risks and permission != "other":
                normalized_risks.append(permission)
        messages: list[str] = []
        status = "normalized"
        if normalized_type == "other":
            status = "needs_review"
            messages.append("Unknown or unsupported capability type normalized to other.")
        if not descriptor.capability_name:
            status = "invalid"
            messages.append("Descriptor name is required.")
        if "unknown" in normalized_risks:
            status = "needs_review" if status == "normalized" else status
            messages.append("Unknown risk category requires review.")
        normalization = ExternalCapabilityNormalizationResult(
            normalization_id=new_external_capability_normalization_id(),
            descriptor_id=descriptor.descriptor_id,
            status=status,
            normalized_capability_type=normalized_type,
            normalized_name=descriptor.capability_name,
            normalized_permissions=normalized_permissions,
            normalized_risk_categories=normalized_risks,
            validation_messages=messages,
            created_at=utc_now_iso(),
            normalization_attrs={
                "risk_level": infer_risk_level(normalized_risks),
                "metadata_only": True,
            },
        )
        activity = (
            "external_capability_normalization_failed"
            if normalization.status in {"invalid", "error"}
            else "external_capability_normalized"
        )
        self._record_event(
            activity,
            descriptor=descriptor,
            normalization=normalization,
            event_attrs={"status": normalization.status},
            event_relations=[
                ("normalization_object", normalization.normalization_id),
                ("descriptor_object", descriptor.descriptor_id),
            ],
            object_relations=[
                (normalization.normalization_id, descriptor.descriptor_id, "normalizes_descriptor"),
            ],
        )
        return normalization

    def create_assimilation_candidate(
        self,
        *,
        descriptor: ExternalCapabilityDescriptor,
        normalization: ExternalCapabilityNormalizationResult | None = None,
        review_status: str = "pending_review",
        activation_status: str = "disabled",
        recommended_next_step: str | None = None,
        linked_tool_descriptor_id: str | None = None,
        linked_permission_scope_id: str | None = None,
        linked_risk_note_ids: list[str] | None = None,
        candidate_attrs: dict[str, Any] | None = None,
    ) -> ExternalAssimilationCandidate:
        if activation_status == "active":
            raise ExternalAssimilationCandidateError("active external candidates must not be created in v0.14.0")
        candidate = ExternalAssimilationCandidate(
            candidate_id=new_external_assimilation_candidate_id(),
            descriptor_id=descriptor.descriptor_id,
            source_id=descriptor.source_id,
            candidate_type=(
                normalization.normalized_capability_type
                if normalization and normalization.normalized_capability_type
                else descriptor.capability_type
            ),
            candidate_name=(
                normalization.normalized_name
                if normalization and normalization.normalized_name
                else descriptor.capability_name
            ),
            review_status=review_status,
            activation_status=activation_status,
            execution_enabled=False,
            recommended_next_step=recommended_next_step,
            linked_tool_descriptor_id=linked_tool_descriptor_id,
            linked_permission_scope_id=linked_permission_scope_id,
            linked_risk_note_ids=list(linked_risk_note_ids or []),
            created_at=utc_now_iso(),
            candidate_attrs={**dict(candidate_attrs or {}), "runtime_effect": False},
        )
        event_relations = [
            ("candidate_object", candidate.candidate_id),
            ("descriptor_object", descriptor.descriptor_id),
            ("source_object", descriptor.source_id or ""),
            ("tool_descriptor_object", linked_tool_descriptor_id or ""),
            ("permission_scope_object", linked_permission_scope_id or ""),
        ]
        object_relations = [
            (candidate.candidate_id, descriptor.descriptor_id, "derived_from_descriptor"),
            (candidate.candidate_id, descriptor.source_id or "", "from_source"),
            (candidate.candidate_id, linked_tool_descriptor_id or "", "candidate_for_tool_descriptor"),
            (candidate.candidate_id, linked_permission_scope_id or "", "references_permission_scope"),
        ]
        self._record_event(
            "external_assimilation_candidate_created",
            descriptor=descriptor,
            candidate=candidate,
            event_attrs={"activation_status": "disabled", "execution_enabled": False},
            event_relations=event_relations,
            object_relations=object_relations,
        )
        return candidate

    def record_risk_note(
        self,
        *,
        descriptor_id: str | None = None,
        candidate_id: str | None = None,
        risk_level: str,
        risk_categories: list[str],
        message: str,
        review_required: bool = True,
        source_kind: str | None = None,
        risk_attrs: dict[str, Any] | None = None,
    ) -> ExternalCapabilityRiskNote:
        note = ExternalCapabilityRiskNote(
            risk_note_id=new_external_capability_risk_note_id(),
            descriptor_id=descriptor_id,
            candidate_id=candidate_id,
            risk_level=risk_level,
            risk_categories=[normalize_risk_category(item) for item in risk_categories],
            message=message,
            review_required=review_required,
            source_kind=source_kind,
            created_at=utc_now_iso(),
            risk_attrs=dict(risk_attrs or {}),
        )
        self._record_event(
            "external_capability_risk_note_recorded",
            risk_note=note,
            event_attrs={"risk_level": note.risk_level, "review_required": note.review_required},
            event_relations=[
                ("risk_note_object", note.risk_note_id),
                ("descriptor_object", descriptor_id or ""),
                ("candidate_object", candidate_id or ""),
            ],
            object_relations=[
                (note.risk_note_id, descriptor_id or "", "describes_descriptor"),
                (note.risk_note_id, candidate_id or "", "describes_candidate"),
            ],
        )
        return note

    def import_as_disabled_candidate(
        self,
        *,
        raw_descriptor: dict[str, Any],
        source: ExternalCapabilitySource | None = None,
        recommended_next_step: str | None = None,
    ) -> tuple[ExternalCapabilityDescriptor, ExternalCapabilityNormalizationResult, ExternalAssimilationCandidate]:
        descriptor = self.import_descriptor(
            raw_descriptor=raw_descriptor,
            source_id=source.source_id if source else None,
        )
        normalization = self.normalize_descriptor(descriptor=descriptor)
        risk_level = infer_risk_level(normalization.normalized_risk_categories)
        linked_risk_note_ids: list[str] = []
        if risk_level in {"medium", "high", "critical"}:
            note = self.record_risk_note(
                descriptor_id=descriptor.descriptor_id,
                risk_level=risk_level,
                risk_categories=normalization.normalized_risk_categories,
                message="External capability descriptor requires review before any activation.",
                review_required=True,
                source_kind=descriptor.capability_type,
            )
            linked_risk_note_ids.append(note.risk_note_id)
        candidate = self.create_assimilation_candidate(
            descriptor=descriptor,
            normalization=normalization,
            review_status="pending_review",
            activation_status="disabled",
            recommended_next_step=recommended_next_step,
            linked_risk_note_ids=linked_risk_note_ids,
        )
        return descriptor, normalization, candidate

    def _record_batch_event(
        self,
        event_activity: str,
        *,
        batch: ExternalCapabilityImportBatch,
        source_id: str | None,
        descriptor_ids: list[str],
    ) -> None:
        event_relations = [("batch_object", batch.batch_id), ("source_object", source_id or "")]
        event_relations.extend(("descriptor_object", descriptor_id) for descriptor_id in descriptor_ids)
        object_relations = [(batch.batch_id, descriptor_id, "imports_descriptor") for descriptor_id in descriptor_ids]
        self._record_event(
            event_activity,
            batch=batch,
            event_attrs={"status": batch.status},
            event_relations=event_relations,
            object_relations=object_relations,
        )

    def _record_event(
        self,
        event_activity: str,
        *,
        source: ExternalCapabilitySource | None = None,
        descriptor: ExternalCapabilityDescriptor | None = None,
        batch: ExternalCapabilityImportBatch | None = None,
        normalization: ExternalCapabilityNormalizationResult | None = None,
        candidate: ExternalAssimilationCandidate | None = None,
        risk_note: ExternalCapabilityRiskNote | None = None,
        event_attrs: dict[str, Any],
        event_relations: list[tuple[str, str]],
        object_relations: list[tuple[str, str, str]],
    ) -> None:
        event = OCELEvent(
            event_id=f"evt:{uuid4()}",
            event_activity=event_activity,
            event_timestamp=utc_now_iso(),
            event_attrs={
                **event_attrs,
                "runtime_event_type": event_activity,
                "source_runtime": "chanta_core",
                "observability_only": True,
                "external_capability_import_only": True,
                "runtime_effect": False,
                "enforcement_enabled": False,
            },
        )
        objects = self._objects_for_event(
            source=source,
            descriptor=descriptor,
            batch=batch,
            normalization=normalization,
            candidate=candidate,
            risk_note=risk_note,
            event_relations=event_relations,
        )
        relations = [
            OCELRelation.event_object(event_id=event.event_id, object_id=object_id, qualifier=qualifier)
            for qualifier, object_id in event_relations
            if object_id
        ]
        relations.extend(
            OCELRelation.object_object(source_object_id=source_id, target_object_id=target_id, qualifier=qualifier)
            for source_id, target_id, qualifier in object_relations
            if source_id and target_id
        )
        self.trace_service.record_session_ocel_record(OCELRecord(event=event, objects=objects, relations=relations))

    def _objects_for_event(
        self,
        *,
        source: ExternalCapabilitySource | None,
        descriptor: ExternalCapabilityDescriptor | None,
        batch: ExternalCapabilityImportBatch | None,
        normalization: ExternalCapabilityNormalizationResult | None,
        candidate: ExternalAssimilationCandidate | None,
        risk_note: ExternalCapabilityRiskNote | None,
        event_relations: list[tuple[str, str]],
    ) -> list[OCELObject]:
        objects: list[OCELObject] = []
        if source is not None:
            objects.append(_source_object(source))
        if descriptor is not None:
            objects.append(_descriptor_object(descriptor))
        if batch is not None:
            objects.append(_batch_object(batch))
        if normalization is not None:
            objects.append(_normalization_object(normalization))
        if candidate is not None:
            objects.append(_candidate_object(candidate))
        if risk_note is not None:
            objects.append(_risk_note_object(risk_note))
        known_ids = {item.object_id for item in objects}
        for qualifier, object_id in event_relations:
            if not object_id or object_id in known_ids:
                continue
            placeholder = _placeholder_object(qualifier, object_id)
            if placeholder is not None:
                objects.append(placeholder)
                known_ids.add(object_id)
        return objects


def _source_object(source: ExternalCapabilitySource) -> OCELObject:
    return OCELObject(
        object_id=source.source_id,
        object_type="external_capability_source",
        object_attrs={
            **source.to_dict(),
            "object_key": source.source_id,
            "display_name": source.source_name,
        },
    )


def _descriptor_object(descriptor: ExternalCapabilityDescriptor) -> OCELObject:
    return OCELObject(
        object_id=descriptor.descriptor_id,
        object_type="external_capability_descriptor",
        object_attrs={
            **descriptor.to_dict(),
            "object_key": descriptor.descriptor_id,
            "display_name": descriptor.capability_name,
            "execution_enabled": False,
        },
    )


def _batch_object(batch: ExternalCapabilityImportBatch) -> OCELObject:
    return OCELObject(
        object_id=batch.batch_id,
        object_type="external_capability_import_batch",
        object_attrs={**batch.to_dict(), "object_key": batch.batch_id, "display_name": batch.batch_name or batch.status},
    )


def _normalization_object(normalization: ExternalCapabilityNormalizationResult) -> OCELObject:
    return OCELObject(
        object_id=normalization.normalization_id,
        object_type="external_capability_normalization_result",
        object_attrs={
            **normalization.to_dict(),
            "object_key": normalization.normalization_id,
            "display_name": normalization.status,
        },
    )


def _candidate_object(candidate: ExternalAssimilationCandidate) -> OCELObject:
    return OCELObject(
        object_id=candidate.candidate_id,
        object_type="external_assimilation_candidate",
        object_attrs={
            **candidate.to_dict(),
            "object_key": candidate.candidate_id,
            "display_name": candidate.candidate_name,
            "execution_enabled": False,
        },
    )


def _risk_note_object(note: ExternalCapabilityRiskNote) -> OCELObject:
    return OCELObject(
        object_id=note.risk_note_id,
        object_type="external_capability_risk_note",
        object_attrs={**note.to_dict(), "object_key": note.risk_note_id, "display_name": note.risk_level},
    )


def _placeholder_object(qualifier: str, object_id: str) -> OCELObject | None:
    placeholder_types = {
        "source_object": "external_capability_source",
        "descriptor_object": "external_capability_descriptor",
        "batch_object": "external_capability_import_batch",
        "normalization_object": "external_capability_normalization_result",
        "candidate_object": "external_assimilation_candidate",
        "risk_note_object": "external_capability_risk_note",
        "tool_descriptor_object": "tool_descriptor",
        "permission_scope_object": "permission_scope",
    }
    object_type = placeholder_types.get(qualifier)
    if object_type is None:
        return None
    attrs: dict[str, Any] = {"object_key": object_id}
    if object_type in {"external_capability_descriptor", "external_assimilation_candidate"}:
        attrs["execution_enabled"] = False
    return OCELObject(object_id=object_id, object_type=object_type, object_attrs=attrs)


def _normalize_token(value: str | None) -> str:
    return str(value or "").strip().lower().replace("-", "_").replace(" ", "_")


def _optional_string(value: Any) -> str | None:
    if value is None:
        return None
    return str(value)


def _dict_value(value: Any) -> dict[str, Any]:
    return dict(value) if isinstance(value, dict) else {}


def _list_of_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]


def _failed_descriptor_ref(raw_descriptor: Any, index: int) -> str:
    if isinstance(raw_descriptor, dict):
        return str(raw_descriptor.get("name") or raw_descriptor.get("id") or f"index:{index}")
    return f"index:{index}"
