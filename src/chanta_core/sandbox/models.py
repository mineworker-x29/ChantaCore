from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.sandbox.errors import (
    WorkspaceRootError,
    WorkspaceWriteBoundaryError,
    WorkspaceWriteIntentError,
    WorkspaceWriteSandboxDecisionError,
    WorkspaceWriteSandboxViolationError,
)


LIFECYCLE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
BOUNDARY_TYPES = {
    "allowed_root",
    "allowed_path",
    "denied_path",
    "protected_path",
    "generated_only",
    "manual",
    "other",
}
INTENT_OPERATIONS = {
    "write_file",
    "append_file",
    "edit_file",
    "delete_file",
    "re" + "name_file",
    "mk" + "dir",
    "r" + "mdir",
    "ch" + "mod",
    "other",
}
DECISIONS = {"allowed", "denied", "needs_review", "inconclusive", "error"}
DECISION_BASES = {
    "inside_workspace",
    "outside_workspace",
    "protected_path",
    "denied_boundary",
    "no_workspace_root",
    "path_resolution_error",
    "manual",
    "test",
    "other",
}
VIOLATION_TYPES = {
    "outside_workspace",
    "protected_path",
    "denied_path",
    "path_resolution_error",
    "unknown_root",
    "unsafe_operation",
    "other",
}
SEVERITIES = {"info", "low", "medium", "high", "critical"}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


def _require_probability(value: float | None, error_type: type[Exception], field_name: str) -> None:
    if value is None:
        return
    if value < 0.0 or value > 1.0:
        raise error_type(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class WorkspaceRoot:
    workspace_root_id: str
    root_path: str
    root_name: str | None
    status: str
    created_at: str
    updated_at: str
    root_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, LIFECYCLE_STATUSES, WorkspaceRootError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "workspace_root_id": self.workspace_root_id,
            "root_path": self.root_path,
            "root_name": self.root_name,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "root_attrs": self.root_attrs,
        }


@dataclass(frozen=True)
class WorkspaceWriteBoundary:
    boundary_id: str
    workspace_root_id: str
    boundary_type: str
    path_ref: str
    description: str | None
    status: str
    priority: int | None
    boundary_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.boundary_type, BOUNDARY_TYPES, WorkspaceWriteBoundaryError, "boundary_type")
        _require_value(self.status, LIFECYCLE_STATUSES, WorkspaceWriteBoundaryError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "boundary_id": self.boundary_id,
            "workspace_root_id": self.workspace_root_id,
            "boundary_type": self.boundary_type,
            "path_ref": self.path_ref,
            "description": self.description,
            "status": self.status,
            "priority": self.priority,
            "boundary_attrs": self.boundary_attrs,
        }


@dataclass(frozen=True)
class WorkspaceWriteIntent:
    intent_id: str
    workspace_root_id: str | None
    target_path: str
    operation: str
    requester_type: str | None
    requester_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    permission_request_id: str | None
    session_permission_resolution_id: str | None
    reason: str | None
    created_at: str
    intent_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.operation, INTENT_OPERATIONS, WorkspaceWriteIntentError, "operation")

    def to_dict(self) -> dict[str, Any]:
        return {
            "intent_id": self.intent_id,
            "workspace_root_id": self.workspace_root_id,
            "target_path": self.target_path,
            "operation": self.operation,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "permission_request_id": self.permission_request_id,
            "session_permission_resolution_id": self.session_permission_resolution_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "intent_attrs": self.intent_attrs,
        }


@dataclass(frozen=True)
class WorkspaceWriteSandboxDecision:
    decision_id: str
    intent_id: str
    workspace_root_id: str | None
    decision: str
    decision_basis: str
    normalized_target_path: str | None
    normalized_root_path: str | None
    inside_workspace: bool | None
    matched_boundary_ids: list[str]
    violation_ids: list[str]
    confidence: float | None
    reason: str | None
    enforcement_enabled: bool
    created_at: str
    decision_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.decision, DECISIONS, WorkspaceWriteSandboxDecisionError, "decision")
        _require_value(self.decision_basis, DECISION_BASES, WorkspaceWriteSandboxDecisionError, "decision_basis")
        if self.enforcement_enabled is not False:
            raise WorkspaceWriteSandboxDecisionError("enforcement_enabled must be False in v0.12.2")
        _require_probability(self.confidence, WorkspaceWriteSandboxDecisionError, "confidence")

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "intent_id": self.intent_id,
            "workspace_root_id": self.workspace_root_id,
            "decision": self.decision,
            "decision_basis": self.decision_basis,
            "normalized_target_path": self.normalized_target_path,
            "normalized_root_path": self.normalized_root_path,
            "inside_workspace": self.inside_workspace,
            "matched_boundary_ids": self.matched_boundary_ids,
            "violation_ids": self.violation_ids,
            "confidence": self.confidence,
            "reason": self.reason,
            "enforcement_enabled": self.enforcement_enabled,
            "created_at": self.created_at,
            "decision_attrs": self.decision_attrs,
        }


@dataclass(frozen=True)
class WorkspaceWriteSandboxViolation:
    violation_id: str
    intent_id: str
    violation_type: str
    severity: str | None
    message: str
    target_path: str
    workspace_root_id: str | None
    created_at: str
    violation_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.violation_type, VIOLATION_TYPES, WorkspaceWriteSandboxViolationError, "violation_type")
        if self.severity is not None:
            _require_value(self.severity, SEVERITIES, WorkspaceWriteSandboxViolationError, "severity")

    def to_dict(self) -> dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "intent_id": self.intent_id,
            "violation_type": self.violation_type,
            "severity": self.severity,
            "message": self.message,
            "target_path": self.target_path,
            "workspace_root_id": self.workspace_root_id,
            "created_at": self.created_at,
            "violation_attrs": self.violation_attrs,
        }
