from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.permissions.errors import (
    PermissionDecisionError,
    PermissionGrantError,
    PermissionModelError,
    PermissionPolicyNoteError,
    PermissionRequestError,
    PermissionScopeError,
)


SCOPE_TYPES = {
    "session",
    "workspace",
    "tool",
    "skill",
    "file",
    "directory",
    "shell",
    "network",
    "memory",
    "materialized_view",
    "manual",
    "other",
}
LIFECYCLE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
REQUEST_TYPES = {
    "tool_use",
    "file_read",
    "file_write",
    "shell",
    "network",
    "memory_update",
    "view_refresh",
    "manual",
    "other",
}
REQUEST_STATUSES = {"created", "pending", "decided", "cancelled", "expired", "error"}
DECISIONS = {"allow", "deny", "ask", "defer", "inconclusive"}
DECISION_MODES = {"manual", "model_suggested", "policy_note", "service_recorded", "test", "other"}
GRANT_STATUSES = {"active", "draft", "expired", "revoked", "superseded"}
NOTE_TYPES = {
    "informational",
    "risk_note",
    "review_needed",
    "future_" + "en" + "forcement_candidate",
    "manual",
    "other",
}
FORBIDDEN_NOTE_TYPES = {"en" + "force", "auto_allow", "auto_" + "deny", "auto_block", "sand" + "box"}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


def _require_probability(value: float | None, error_type: type[Exception], field_name: str) -> None:
    if value is None:
        return
    if value < 0.0 or value > 1.0:
        raise error_type(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class PermissionScope:
    scope_id: str
    scope_name: str
    scope_type: str
    description: str | None
    target_type: str | None
    target_ref: str | None
    allowed_operations: list[str]
    denied_operations: list[str]
    risk_level: str | None
    status: str
    created_at: str
    updated_at: str
    scope_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.scope_type, SCOPE_TYPES, PermissionScopeError, "scope_type")
        _require_value(self.status, LIFECYCLE_STATUSES, PermissionScopeError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "scope_id": self.scope_id,
            "scope_name": self.scope_name,
            "scope_type": self.scope_type,
            "description": self.description,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "allowed_operations": self.allowed_operations,
            "denied_operations": self.denied_operations,
            "risk_level": self.risk_level,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "scope_attrs": self.scope_attrs,
        }


@dataclass(frozen=True)
class PermissionRequest:
    request_id: str
    request_type: str
    requester_type: str | None
    requester_id: str | None
    target_type: str
    target_ref: str
    operation: str
    scope_id: str | None
    risk_level: str | None
    reason: str | None
    status: str
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    tool_descriptor_id: str | None
    verification_result_ids: list[str]
    outcome_evaluation_ids: list[str]
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.request_type, REQUEST_TYPES, PermissionRequestError, "request_type")
        _require_value(self.status, REQUEST_STATUSES, PermissionRequestError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "request_type": self.request_type,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "operation": self.operation,
            "scope_id": self.scope_id,
            "risk_level": self.risk_level,
            "reason": self.reason,
            "status": self.status,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "tool_descriptor_id": self.tool_descriptor_id,
            "verification_result_ids": self.verification_result_ids,
            "outcome_evaluation_ids": self.outcome_evaluation_ids,
            "created_at": self.created_at,
            "request_attrs": self.request_attrs,
        }


@dataclass(frozen=True)
class PermissionDecision:
    decision_id: str
    request_id: str
    decision: str
    decision_mode: str
    reason: str | None
    decided_by: str | None
    confidence: float | None
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.decision, DECISIONS, PermissionDecisionError, "decision")
        _require_value(self.decision_mode, DECISION_MODES, PermissionDecisionError, "decision_mode")
        _require_probability(self.confidence, PermissionDecisionError, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "request_id": self.request_id,
            "decision": self.decision,
            "decision_mode": self.decision_mode,
            "reason": self.reason,
            "decided_by": self.decided_by,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "decision_attrs": self.decision_attrs,
        }


@dataclass(frozen=True)
class PermissionGrant:
    grant_id: str
    request_id: str | None
    scope_id: str | None
    target_type: str
    target_ref: str
    operation: str
    status: str
    granted_by: str | None
    granted_at: str
    expires_at: str | None
    session_id: str | None
    grant_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, GRANT_STATUSES, PermissionGrantError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "grant_id": self.grant_id,
            "request_id": self.request_id,
            "scope_id": self.scope_id,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "operation": self.operation,
            "status": self.status,
            "granted_by": self.granted_by,
            "granted_at": self.granted_at,
            "expires_at": self.expires_at,
            "session_id": self.session_id,
            "grant_attrs": self.grant_attrs,
        }


@dataclass(frozen=True)
class PermissionDenial:
    denial_id: str
    request_id: str | None
    scope_id: str | None
    target_type: str
    target_ref: str
    operation: str
    reason: str | None
    denied_by: str | None
    denied_at: str
    session_id: str | None
    denial_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "denial_id": self.denial_id,
            "request_id": self.request_id,
            "scope_id": self.scope_id,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "operation": self.operation,
            "reason": self.reason,
            "denied_by": self.denied_by,
            "denied_at": self.denied_at,
            "session_id": self.session_id,
            "denial_attrs": self.denial_attrs,
        }


@dataclass(frozen=True)
class PermissionPolicyNote:
    policy_note_id: str
    scope_id: str | None
    target_type: str | None
    target_ref: str | None
    note_type: str
    text: str
    status: str
    priority: int | None
    source_kind: str | None
    created_at: str
    updated_at: str
    note_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.note_type in FORBIDDEN_NOTE_TYPES:
            raise PermissionPolicyNoteError(f"Unsupported note_type: {self.note_type}")
        _require_value(self.note_type, NOTE_TYPES, PermissionPolicyNoteError, "note_type")
        _require_value(self.status, LIFECYCLE_STATUSES, PermissionPolicyNoteError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_note_id": self.policy_note_id,
            "scope_id": self.scope_id,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "note_type": self.note_type,
            "text": self.text,
            "status": self.status,
            "priority": self.priority,
            "source_kind": self.source_kind,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "note_attrs": self.note_attrs,
        }


def reject_forbidden_note_type(note_type: str) -> None:
    if note_type in FORBIDDEN_NOTE_TYPES:
        raise PermissionPolicyNoteError(f"Unsupported note_type: {note_type}")
    if note_type not in NOTE_TYPES:
        raise PermissionModelError(f"Unsupported note_type: {note_type}")
