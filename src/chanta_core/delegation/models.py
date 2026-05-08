from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.delegation.errors import (
    DelegatedProcessRunError,
    DelegationLinkError,
    DelegationPacketError,
    DelegationResultError,
)


DELEGATION_TYPES = {
    "subprocess",
    "subagent",
    "verification",
    "analysis",
    "review",
    "manual",
    "other",
}
ISOLATION_MODES = {
    "none",
    "packet_only",
    "sidechain_pending",
    "sidechain",
    "external",
    "other",
}
RUN_STATUSES = {"created", "requested", "started", "completed", "failed", "cancelled", "skipped"}
RESULT_STATUSES = {"completed", "failed", "cancelled", "skipped", "inconclusive"}
LINK_RELATION_TYPES = {"delegated_to", "forked_delegation", "manual_link", "other"}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


@dataclass(frozen=True)
class DelegationPacket:
    packet_id: str
    packet_name: str | None
    parent_session_id: str | None
    parent_turn_id: str | None
    parent_message_id: str | None
    parent_process_instance_id: str | None
    goal: str
    context_summary: str | None
    structured_inputs: dict[str, Any]
    object_refs: list[dict[str, Any]]
    allowed_capabilities: list[str]
    expected_output_schema: dict[str, Any] | None
    termination_conditions: dict[str, Any]
    permission_request_ids: list[str]
    session_permission_resolution_ids: list[str]
    workspace_write_sandbox_decision_ids: list[str]
    shell_network_pre_sandbox_decision_ids: list[str]
    process_outcome_evaluation_ids: list[str]
    created_at: str
    packet_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.goal:
            raise DelegationPacketError("goal is required")
        if self.packet_attrs.get("contains_full_parent_transcript") is not False:
            object.__setattr__(
                self,
                "packet_attrs",
                {**self.packet_attrs, "contains_full_parent_transcript": False},
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "packet_id": self.packet_id,
            "packet_name": self.packet_name,
            "parent_session_id": self.parent_session_id,
            "parent_turn_id": self.parent_turn_id,
            "parent_message_id": self.parent_message_id,
            "parent_process_instance_id": self.parent_process_instance_id,
            "goal": self.goal,
            "context_summary": self.context_summary,
            "structured_inputs": self.structured_inputs,
            "object_refs": self.object_refs,
            "allowed_capabilities": self.allowed_capabilities,
            "expected_output_schema": self.expected_output_schema,
            "termination_conditions": self.termination_conditions,
            "permission_request_ids": self.permission_request_ids,
            "session_permission_resolution_ids": self.session_permission_resolution_ids,
            "workspace_write_sandbox_decision_ids": self.workspace_write_sandbox_decision_ids,
            "shell_network_pre_sandbox_decision_ids": self.shell_network_pre_sandbox_decision_ids,
            "process_outcome_evaluation_ids": self.process_outcome_evaluation_ids,
            "created_at": self.created_at,
            "packet_attrs": self.packet_attrs,
        }


@dataclass(frozen=True)
class DelegatedProcessRun:
    delegated_run_id: str
    packet_id: str
    parent_session_id: str | None
    child_session_id: str | None
    parent_process_instance_id: str | None
    child_process_instance_id: str | None
    delegation_type: str
    isolation_mode: str
    status: str
    requested_at: str
    started_at: str | None
    completed_at: str | None
    failed_at: str | None
    requester_type: str | None
    requester_id: str | None
    allowed_capabilities: list[str]
    inherited_permissions: bool
    run_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.delegation_type, DELEGATION_TYPES, DelegatedProcessRunError, "delegation_type")
        _require_value(self.isolation_mode, ISOLATION_MODES, DelegatedProcessRunError, "isolation_mode")
        _require_value(self.status, RUN_STATUSES, DelegatedProcessRunError, "status")
        if self.inherited_permissions is not False:
            raise DelegatedProcessRunError("inherited_permissions must be False in v0.13.0")

    def to_dict(self) -> dict[str, Any]:
        return {
            "delegated_run_id": self.delegated_run_id,
            "packet_id": self.packet_id,
            "parent_session_id": self.parent_session_id,
            "child_session_id": self.child_session_id,
            "parent_process_instance_id": self.parent_process_instance_id,
            "child_process_instance_id": self.child_process_instance_id,
            "delegation_type": self.delegation_type,
            "isolation_mode": self.isolation_mode,
            "status": self.status,
            "requested_at": self.requested_at,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "failed_at": self.failed_at,
            "requester_type": self.requester_type,
            "requester_id": self.requester_id,
            "allowed_capabilities": self.allowed_capabilities,
            "inherited_permissions": self.inherited_permissions,
            "run_attrs": self.run_attrs,
        }


@dataclass(frozen=True)
class DelegationResult:
    result_id: str
    delegated_run_id: str
    packet_id: str
    status: str
    output_summary: str | None
    output_payload: dict[str, Any]
    evidence_refs: list[dict[str, Any]]
    recommendation_refs: list[dict[str, Any]]
    failure: dict[str, Any] | None
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.status, RESULT_STATUSES, DelegationResultError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "delegated_run_id": self.delegated_run_id,
            "packet_id": self.packet_id,
            "status": self.status,
            "output_summary": self.output_summary,
            "output_payload": self.output_payload,
            "evidence_refs": self.evidence_refs,
            "recommendation_refs": self.recommendation_refs,
            "failure": self.failure,
            "created_at": self.created_at,
            "result_attrs": self.result_attrs,
        }


@dataclass(frozen=True)
class DelegationLink:
    link_id: str
    delegated_run_id: str
    parent_process_instance_id: str | None
    child_process_instance_id: str | None
    parent_session_id: str | None
    child_session_id: str | None
    relation_type: str
    created_at: str
    link_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.relation_type, LINK_RELATION_TYPES, DelegationLinkError, "relation_type")

    def to_dict(self) -> dict[str, Any]:
        return {
            "link_id": self.link_id,
            "delegated_run_id": self.delegated_run_id,
            "parent_process_instance_id": self.parent_process_instance_id,
            "child_process_instance_id": self.child_process_instance_id,
            "parent_session_id": self.parent_session_id,
            "child_session_id": self.child_session_id,
            "relation_type": self.relation_type,
            "created_at": self.created_at,
            "link_attrs": self.link_attrs,
        }
