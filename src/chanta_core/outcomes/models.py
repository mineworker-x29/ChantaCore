from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.outcomes.errors import (
    ProcessOutcomeContractError,
    ProcessOutcomeCriterionError,
    ProcessOutcomeEvaluationError,
    ProcessOutcomeSignalError,
    ProcessOutcomeTargetError,
)


CONTRACT_TYPES = {
    "process_completion",
    "turn_quality",
    "message_quality",
    "verification_coverage",
    "trace_integrity",
    "memory_integrity",
    "materialized_view_integrity",
    "tool_registry_integrity",
    "manual",
    "other",
}
LIFECYCLE_STATUSES = {"active", "draft", "deprecated", "archived", "withdrawn"}
SEVERITIES = {"info", "low", "medium", "high", "critical"}
CRITERION_TYPES = {
    "verification_passed",
    "verification_failed_absent",
    "evidence_coverage_minimum",
    "required_evidence_present",
    "trace_exists",
    "message_exists",
    "manual_review_required",
    "other",
}
TARGET_TYPES = {
    "session",
    "conversation_turn",
    "message",
    "process_instance",
    "verification_run",
    "materialized_view",
    "tool_registry_snapshot",
    "manual",
    "other",
}
SIGNAL_TYPES = {
    "verification_passed",
    "verification_failed",
    "verification_inconclusive",
    "evidence_missing",
    "trace_missing",
    "manual_positive",
    "manual_negative",
    "needs_review",
    "error_signal",
    "other",
}
SOURCE_KINDS = {
    "verification_result",
    "verification_evidence",
    "pig_report",
    "ocpx_query",
    "manual",
    "service",
    "test",
    "other",
}
OUTCOME_STATUSES = {
    "success",
    "partial_success",
    "failed",
    "inconclusive",
    "needs_review",
    "skipped",
    "error",
}


def _require_value(value: str, allowed: set[str], error_type: type[Exception], field_name: str) -> None:
    if value not in allowed:
        raise error_type(f"Unsupported {field_name}: {value}")


def _require_probability(
    value: float | None,
    error_type: type[Exception],
    field_name: str,
) -> None:
    if value is None:
        return
    if value < 0.0 or value > 1.0:
        raise error_type(f"{field_name} must be between 0.0 and 1.0")


@dataclass(frozen=True)
class ProcessOutcomeContract:
    contract_id: str
    contract_name: str
    contract_type: str
    description: str | None
    status: str
    target_type: str | None
    required_verification_contract_ids: list[str]
    min_required_pass_rate: float | None
    min_evidence_coverage: float | None
    severity: str | None
    created_at: str
    updated_at: str
    contract_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.contract_type, CONTRACT_TYPES, ProcessOutcomeContractError, "contract_type")
        _require_value(self.status, LIFECYCLE_STATUSES, ProcessOutcomeContractError, "status")
        if self.target_type is not None:
            _require_value(self.target_type, TARGET_TYPES, ProcessOutcomeContractError, "target_type")
        if self.severity is not None:
            _require_value(self.severity, SEVERITIES, ProcessOutcomeContractError, "severity")
        _require_probability(self.min_required_pass_rate, ProcessOutcomeContractError, "min_required_pass_rate")
        _require_probability(self.min_evidence_coverage, ProcessOutcomeContractError, "min_evidence_coverage")

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "contract_name": self.contract_name,
            "contract_type": self.contract_type,
            "description": self.description,
            "status": self.status,
            "target_type": self.target_type,
            "required_verification_contract_ids": self.required_verification_contract_ids,
            "min_required_pass_rate": self.min_required_pass_rate,
            "min_evidence_coverage": self.min_evidence_coverage,
            "severity": self.severity,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "contract_attrs": self.contract_attrs,
        }


@dataclass(frozen=True)
class ProcessOutcomeCriterion:
    criterion_id: str
    contract_id: str
    criterion_type: str
    description: str
    required: bool
    weight: float | None
    expected_statuses: list[str]
    status: str
    criterion_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.criterion_type, CRITERION_TYPES, ProcessOutcomeCriterionError, "criterion_type")
        _require_value(self.status, LIFECYCLE_STATUSES, ProcessOutcomeCriterionError, "status")
        _require_probability(self.weight, ProcessOutcomeCriterionError, "weight")

    def to_dict(self) -> dict[str, Any]:
        return {
            "criterion_id": self.criterion_id,
            "contract_id": self.contract_id,
            "criterion_type": self.criterion_type,
            "description": self.description,
            "required": self.required,
            "weight": self.weight,
            "expected_statuses": self.expected_statuses,
            "status": self.status,
            "criterion_attrs": self.criterion_attrs,
        }


@dataclass(frozen=True)
class ProcessOutcomeTarget:
    target_id: str
    target_type: str
    target_ref: str
    target_label: str | None
    session_id: str | None
    turn_id: str | None
    message_id: str | None
    process_instance_id: str | None
    status: str
    created_at: str
    target_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.target_type, TARGET_TYPES, ProcessOutcomeTargetError, "target_type")
        _require_value(self.status, LIFECYCLE_STATUSES, ProcessOutcomeTargetError, "status")

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_id": self.target_id,
            "target_type": self.target_type,
            "target_ref": self.target_ref,
            "target_label": self.target_label,
            "session_id": self.session_id,
            "turn_id": self.turn_id,
            "message_id": self.message_id,
            "process_instance_id": self.process_instance_id,
            "status": self.status,
            "created_at": self.created_at,
            "target_attrs": self.target_attrs,
        }


@dataclass(frozen=True)
class ProcessOutcomeSignal:
    signal_id: str
    target_id: str | None
    signal_type: str
    signal_value: str
    strength: float | None
    source_kind: str | None
    source_ref: str | None
    created_at: str
    signal_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.signal_type, SIGNAL_TYPES, ProcessOutcomeSignalError, "signal_type")
        if self.source_kind is not None:
            _require_value(self.source_kind, SOURCE_KINDS, ProcessOutcomeSignalError, "source_kind")
        _require_probability(self.strength, ProcessOutcomeSignalError, "strength")

    def to_dict(self) -> dict[str, Any]:
        return {
            "signal_id": self.signal_id,
            "target_id": self.target_id,
            "signal_type": self.signal_type,
            "signal_value": self.signal_value,
            "strength": self.strength,
            "source_kind": self.source_kind,
            "source_ref": self.source_ref,
            "created_at": self.created_at,
            "signal_attrs": self.signal_attrs,
        }


@dataclass(frozen=True)
class ProcessOutcomeEvaluation:
    evaluation_id: str
    contract_id: str
    target_id: str
    outcome_status: str
    score: float | None
    confidence: float | None
    evidence_coverage: float | None
    passed_criteria_ids: list[str]
    failed_criteria_ids: list[str]
    signal_ids: list[str]
    verification_result_ids: list[str]
    reason: str | None
    created_at: str
    evaluation_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_value(self.outcome_status, OUTCOME_STATUSES, ProcessOutcomeEvaluationError, "outcome_status")
        if self.outcome_status in {"success", "partial_success", "failed"}:
            if not self.signal_ids and not self.verification_result_ids:
                raise ProcessOutcomeEvaluationError(
                    "success/partial_success/failed outcome evaluations require signal_ids or verification_result_ids"
                )
        _require_probability(self.score, ProcessOutcomeEvaluationError, "score")
        _require_probability(self.confidence, ProcessOutcomeEvaluationError, "confidence")
        _require_probability(self.evidence_coverage, ProcessOutcomeEvaluationError, "evidence_coverage")

    def to_dict(self) -> dict[str, Any]:
        return {
            "evaluation_id": self.evaluation_id,
            "contract_id": self.contract_id,
            "target_id": self.target_id,
            "outcome_status": self.outcome_status,
            "score": self.score,
            "confidence": self.confidence,
            "evidence_coverage": self.evidence_coverage,
            "passed_criteria_ids": self.passed_criteria_ids,
            "failed_criteria_ids": self.failed_criteria_ids,
            "signal_ids": self.signal_ids,
            "verification_result_ids": self.verification_result_ids,
            "reason": self.reason,
            "created_at": self.created_at,
            "evaluation_attrs": self.evaluation_attrs,
        }
