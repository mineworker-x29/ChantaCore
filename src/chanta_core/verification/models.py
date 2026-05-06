from __future__ import annotations

import hashlib
from dataclasses import dataclass, field
from typing import Any

from chanta_core.verification.errors import (
    VerificationContractError,
    VerificationEvidenceError,
    VerificationRequirementError,
    VerificationResultError,
    VerificationRunError,
    VerificationTargetError,
)


CONTRACT_TYPES = {
    "file_existence",
    "tool_availability",
    "runtime_status",
    "ocel_shape",
    "relation_integrity",
    "message_integrity",
    "memory_integrity",
    "materialized_view_integrity",
    "tool_registry_integrity",
    "process_trace_integrity",
    "manual",
    "other",
}

LIFECYCLE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
SEVERITIES = {"info", "low", "medium", "high", "critical"}
TARGET_TYPES = {
    "file",
    "tool",
    "runtime",
    "session",
    "conversation_turn",
    "message",
    "process_instance",
    "memory_entry",
    "instruction_artifact",
    "materialized_view",
    "hook_definition",
    "tool_descriptor",
    "ocel_object",
    "ocel_relation",
    "other",
}
REQUIREMENT_TYPES = {
    "must_exist",
    "must_be_available",
    "must_have_relation",
    "must_have_event",
    "must_have_status",
    "must_match_hash",
    "must_be_noncanonical_view",
    "manual_check",
    "other",
}
RUN_STATUSES = {"planned", "running", "completed", "failed", "skipped", "cancelled"}
EVIDENCE_KINDS = {
    "observation",
    "file_exists",
    "file_missing",
    "tool_available",
    "tool_unavailable",
    "runtime_status",
    "ocel_object_exists",
    "ocel_relation_exists",
    "event_activity_exists",
    "hash_match",
    "manual_note",
    "other",
}
SOURCE_KINDS = {"manual", "service", "read_only_skill", "pig_report", "ocpx_query", "test", "other"}
RESULT_STATUSES = {"passed", "failed", "inconclusive", "skipped", "error"}


def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def preview_text(text: str, max_chars: int = 240) -> str:
    if max_chars <= 0:
        raise VerificationEvidenceError("max_chars must be positive")
    if len(text) <= max_chars:
        return text
    marker = "...[preview truncated]..."
    head_chars = max(0, max_chars - len(marker))
    return f"{text[:head_chars]}{marker}"


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


@dataclass(frozen=True)
class VerificationContract:
    contract_id: str
    contract_name: str
    contract_type: str
    description: str | None
    status: str
    subject_type: str | None
    required_evidence_kinds: list[str]
    pass_criteria: dict[str, Any]
    fail_criteria: dict[str, Any]
    severity: str | None
    created_at: str
    updated_at: str
    contract_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.contract_type, CONTRACT_TYPES, VerificationContractError, "contract_type")
        _require_value(self.status, LIFECYCLE_STATUSES, VerificationContractError, "status")
        if self.severity is not None:
            _require_value(self.severity, SEVERITIES, VerificationContractError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "contract_name": self.contract_name,
            "contract_type": self.contract_type,
            "description": self.description,
            "status": self.status,
            "subject_type": self.subject_type,
            "required_evidence_kinds": self.required_evidence_kinds,
            "pass_criteria": self.pass_criteria,
            "fail_criteria": self.fail_criteria,
            "severity": self.severity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "contract_attrs": self.contract_attrs,
        }


@dataclass(frozen=True)
class VerificationTarget:
    target_id: str
    target_type: str
    target_ref: str
    target_label: str | None
    status: str
    created_at: str
    target_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.target_type, TARGET_TYPES, VerificationTargetError, "target_type")
        _require_value(self.status, LIFECYCLE_STATUSES, VerificationTargetError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "target_label": self.target_label,
            "status": self.status,
            "created_at": self.created_at,
            "target_attrs": self.target_attrs,
        }


@dataclass(frozen=True)
class VerificationRequirement:
    requirement_id: str
    contract_id: str
    requirement_type: str
    description: str
    required: bool
    evidence_kind: str | None
    priority: int | None
    status: str
    requirement_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.requirement_type, REQUIREMENT_TYPES, VerificationRequirementError, "requirement_type")
        _require_value(self.status, LIFECYCLE_STATUSES, VerificationRequirementError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "requirement_id": self.requirement_id,
            "contract_id": self.contract_id,
            "requirement_type": self.requirement_type,
            "description": self.description,
            "required": self.required,
            "evidence_kind": self.evidence_kind,
            "priority": self.priority,
            "status": self.status,
            "requirement_attrs": self.requirement_attrs,
        }


@dataclass(frozen=True)
class VerificationRun:
    run_id: str
    contract_id: str
    target_ids: list[str]
    status: str
    started_at: str
    completed_at: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    run_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, RUN_STATUSES, VerificationRunError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "target_ids": self.target_ids,
            "status": self.status,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "run_attrs": self.run_attrs,
        }


@dataclass(frozen=True)
class VerificationEvidence:
    evidence_id: str
    run_id: str | None
    target_id: str | None
    evidence_kind: str
    source_kind: str | None
    content: str
    content_preview: str
    content_hash: str
    confidence: float | None
    collected_at: str
    evidence_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.evidence_kind, EVIDENCE_KINDS, VerificationEvidenceError, "evidence_kind")
        if self.source_kind is not None:
            _require_value(self.source_kind, SOURCE_KINDS, VerificationEvidenceError, "source_kind")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evidence_id": self.evidence_id,
            "run_id": self.run_id,
            "target_id": self.target_id,
            "evidence_kind": self.evidence_kind,
            "source_kind": self.source_kind,
            "content": self.content,
            "content_preview": self.content_preview,
            "content_hash": self.content_hash,
            "confidence": self.confidence,
            "collected_at": self.collected_at,
            "evidence_attrs": self.evidence_attrs,
        }


@dataclass(frozen=True)
class VerificationResult:
    result_id: str
    run_id: str | None
    contract_id: str
    target_id: str | None
    status: str
    confidence: float | None
    reason: str | None
    evidence_ids: list[str]
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, RESULT_STATUSES, VerificationResultError, "status")
        if self.status in {"passed", "failed"} and not self.evidence_ids:
            raise VerificationResultError("passed/failed verification results require evidence_ids")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "run_id": self.run_id,
            "contract_id": self.contract_id,
            "target_id": self.target_id,
            "status": self.status,
            "confidence": self.confidence,
            "reason": self.reason,
            "evidence_ids": self.evidence_ids,
            "created_at": self.created_at,
            "result_attrs": self.result_attrs,
        }
