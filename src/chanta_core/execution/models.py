from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ExecutionEnvelope:
    envelope_id: str
    execution_kind: str
    execution_subject_id: str | None
    skill_id: str | None
    session_id: str | None
    turn_id: str | None
    process_instance_id: str | None
    status: str
    execution_allowed: bool
    execution_performed: bool
    blocked: bool
    started_at: str | None
    completed_at: str | None
    created_at: str
    envelope_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "envelope_id": self.envelope_id,
            "execution_kind": self.execution_kind,
            "execution_subject_id": self.execution_subject_id,
            "skill_id": self.skill_id,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "execution_allowed": self.execution_allowed,
            "execution_performed": self.execution_performed,
            "blocked": self.blocked,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "created_at": self.created_at,
            "envelope_attrs": dict(self.envelope_attrs),
        }


@dataclass(frozen=True)
class ExecutionProvenanceRecord:
    provenance_id: str
    envelope_id: str
    actor_type: str | None
    actor_id: str | None
    runtime_kind: str | None
    invocation_mode: str | None
    proposal_id: str | None
    explicit_invocation_request_id: str | None
    explicit_invocation_result_id: str | None
    gate_request_id: str | None
    gate_decision_id: str | None
    gate_result_id: str | None
    capability_decision_id: str | None
    permission_request_id: str | None
    permission_decision_id: str | None
    session_permission_resolution_id: str | None
    sandbox_ref_ids: list[str]
    risk_ref_ids: list[str]
    created_at: str
    provenance_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "provenance_id": self.provenance_id,
            "envelope_id": self.envelope_id,
            "actor_type": self.actor_type,
            "actor_id": self.actor_id,
            "runtime_kind": self.runtime_kind,
            "invocation_mode": self.invocation_mode,
            "proposal_id": self.proposal_id,
            "explicit_invocation_request_id": self.explicit_invocation_request_id,
            "explicit_invocation_result_id": self.explicit_invocation_result_id,
            "gate_request_id": self.gate_request_id,
            "gate_decision_id": self.gate_decision_id,
            "gate_result_id": self.gate_result_id,
            "capability_decision_id": self.capability_decision_id,
            "permission_request_id": self.permission_request_id,
            "permission_decision_id": self.permission_decision_id,
            "session_permission_resolution_id": self.session_permission_resolution_id,
            "sandbox_ref_ids": list(self.sandbox_ref_ids),
            "risk_ref_ids": list(self.risk_ref_ids),
            "created_at": self.created_at,
            "provenance_attrs": dict(self.provenance_attrs),
        }


@dataclass(frozen=True)
class ExecutionInputSnapshot:
    input_snapshot_id: str
    envelope_id: str
    input_kind: str
    input_preview: dict[str, Any]
    input_hash: str | None
    redacted_fields: list[str]
    full_input_stored: bool
    created_at: str
    input_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_snapshot_id": self.input_snapshot_id,
            "envelope_id": self.envelope_id,
            "input_kind": self.input_kind,
            "input_preview": dict(self.input_preview),
            "input_hash": self.input_hash,
            "redacted_fields": list(self.redacted_fields),
            "full_input_stored": self.full_input_stored,
            "created_at": self.created_at,
            "input_attrs": dict(self.input_attrs),
        }


@dataclass(frozen=True)
class ExecutionOutputSnapshot:
    output_snapshot_id: str
    envelope_id: str
    output_kind: str
    output_preview: dict[str, Any]
    output_hash: str | None
    output_ref: str | None
    truncated: bool
    redacted_fields: list[str]
    full_output_stored: bool
    created_at: str
    output_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_snapshot_id": self.output_snapshot_id,
            "envelope_id": self.envelope_id,
            "output_kind": self.output_kind,
            "output_preview": dict(self.output_preview),
            "output_hash": self.output_hash,
            "output_ref": self.output_ref,
            "truncated": self.truncated,
            "redacted_fields": list(self.redacted_fields),
            "full_output_stored": self.full_output_stored,
            "created_at": self.created_at,
            "output_attrs": dict(self.output_attrs),
        }


@dataclass(frozen=True)
class ExecutionArtifactRef:
    artifact_ref_id: str
    envelope_id: str
    artifact_kind: str
    artifact_ref: str
    artifact_hash: str | None
    artifact_preview: dict[str, Any]
    private: bool
    created_at: str
    artifact_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "artifact_ref_id": self.artifact_ref_id,
            "envelope_id": self.envelope_id,
            "artifact_kind": self.artifact_kind,
            "artifact_ref": self.artifact_ref,
            "artifact_hash": self.artifact_hash,
            "artifact_preview": dict(self.artifact_preview),
            "private": self.private,
            "created_at": self.created_at,
            "artifact_attrs": dict(self.artifact_attrs),
        }


@dataclass(frozen=True)
class ExecutionOutcomeSummary:
    summary_id: str
    envelope_id: str
    status: str
    succeeded: bool
    blocked: bool
    failed: bool
    skipped: bool
    violation_ids: list[str]
    finding_ids: list[str]
    output_snapshot_id: str | None
    reason: str | None
    created_at: str
    summary_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "summary_id": self.summary_id,
            "envelope_id": self.envelope_id,
            "status": self.status,
            "succeeded": self.succeeded,
            "blocked": self.blocked,
            "failed": self.failed,
            "skipped": self.skipped,
            "violation_ids": list(self.violation_ids),
            "finding_ids": list(self.finding_ids),
            "output_snapshot_id": self.output_snapshot_id,
            "reason": self.reason,
            "created_at": self.created_at,
            "summary_attrs": dict(self.summary_attrs),
        }
