from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.delegation import (
    ExternalDelegationCandidate,
    ExternalDelegationHandoffPreview,
)
from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level


V0306_MAX_GRANTABLE_LEVEL = DominionLevel.D3_SIMULATE


class ExternalDominionApprovalRequirementStatus(StrEnum):
    UNKNOWN = "unknown"
    REQUIRED = "required"
    EVIDENCE_REQUIRED = "evidence_required"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    APPROVAL_CANDIDATE_READY = "approval_candidate_ready"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    DENIED = "denied"
    DEFERRED = "deferred"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalDominionApprovalDecisionType(StrEnum):
    DENY = "deny"
    DEFER = "defer"
    NO_OP = "no_op"
    REQUIRE_MORE_EVIDENCE = "require_more_evidence"
    REQUIRE_HUMAN_REVIEW = "require_human_review"
    ALLOW_CERTIFICATION_REVIEW = "allow_certification_review"
    FUTURE_TRACK = "future_track"
    BLOCKED = "blocked"


class ExternalDominionAuditEventKind(StrEnum):
    APPROVAL_REQUIREMENT_CREATED = "approval_requirement_created"
    APPROVAL_CANDIDATE_CREATED = "approval_candidate_created"
    APPROVAL_DECISION_RECORDED = "approval_decision_recorded"
    RESULT_BOUNDARY_DEFINED = "result_boundary_defined"
    ROLLBACK_PLAN_CREATED = "rollback_plan_created"
    NO_OP_BOUNDARY_CREATED = "no_op_boundary_created"
    FAILURE_CLASSIFIED = "failure_classified"
    RETRY_DEFERRED = "retry_deferred"
    CERTIFICATION_HANDOFF_CREATED = "certification_handoff_created"
    UNKNOWN = "unknown"


class ExternalDominionResultBoundaryAction(StrEnum):
    REJECT_RAW_OUTPUT = "reject_raw_output"
    REQUIRE_RESULT_ENVELOPE = "require_result_envelope"
    REQUIRE_SUMMARY_ONLY = "require_summary_only"
    REQUIRE_EVIDENCE_REFS = "require_evidence_refs"
    REQUIRE_REDACTION = "require_redaction"
    REQUIRE_NO_MEMORY_PERSISTENCE = "require_no_memory_persistence"
    REQUIRE_HUMAN_REVIEW = "require_human_review"
    ALLOW_SCHEMA_ONLY = "allow_schema_only"
    BLOCK_RESULT_INGESTION = "block_result_ingestion"
    NO_OP = "no_op"


class ExternalDominionFailureClass(StrEnum):
    UNKNOWN = "unknown"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    TRUST_BOUNDARY_VIOLATION = "trust_boundary_violation"
    APPROVAL_MISSING = "approval_missing"
    RESULT_BOUNDARY_VIOLATION = "result_boundary_violation"
    ROLLBACK_UNAVAILABLE = "rollback_unavailable"
    UNSAFE_EXTERNAL_SURFACE = "unsafe_external_surface"
    CREDENTIAL_RISK = "credential_risk"
    NETWORK_RISK = "network_risk"
    COMMAND_RISK = "command_risk"
    PROVIDER_RISK = "provider_risk"
    BROWSER_RISK = "browser_risk"
    RPA_RISK = "rpa_risk"
    GATEWAY_RISK = "gateway_risk"
    DELEGATION_RISK = "delegation_risk"
    MEMORY_CONTAMINATION_RISK = "memory_contamination_risk"
    RAW_OUTPUT_RISK = "raw_output_risk"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    BLOCKED_BY_POLICY = "blocked_by_policy"


HIGH_RISK_TERMS = frozenset(
    {
        "provider",
        "network",
        "credential",
        "command",
        "browser",
        "rpa",
        "gateway",
        "delegation",
        "raw_output",
        "memory",
        "external",
        "future_gate",
    }
)


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def _has_high_risk(values: list[str] | dict[str, Any]) -> bool:
    if isinstance(values, dict):
        text = " ".join(str(item).lower() for pair in values.items() for item in pair)
    else:
        text = " ".join(str(item).lower() for item in values)
    return any(term in text for term in HIGH_RISK_TERMS)


def _normalize_requirement_status(
    value: ExternalDominionApprovalRequirementStatus | str,
) -> ExternalDominionApprovalRequirementStatus:
    if isinstance(value, ExternalDominionApprovalRequirementStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("status must not be blank")
        return ExternalDominionApprovalRequirementStatus(stripped)
    raise TypeError(f"unsupported approval requirement status: {value!r}")


def _normalize_approval_decision(
    value: ExternalDominionApprovalDecisionType | str,
) -> ExternalDominionApprovalDecisionType:
    if isinstance(value, ExternalDominionApprovalDecisionType):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("decision must not be blank")
        return ExternalDominionApprovalDecisionType(stripped)
    raise TypeError(f"unsupported approval decision type: {value!r}")


def _normalize_result_action(
    value: ExternalDominionResultBoundaryAction | str,
) -> ExternalDominionResultBoundaryAction:
    if isinstance(value, ExternalDominionResultBoundaryAction):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("result boundary action must not be blank")
        return ExternalDominionResultBoundaryAction(stripped)
    raise TypeError(f"unsupported result boundary action: {value!r}")


def _normalize_failure_class(value: ExternalDominionFailureClass | str) -> ExternalDominionFailureClass:
    if isinstance(value, ExternalDominionFailureClass):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("failure_class must not be blank")
        return ExternalDominionFailureClass(stripped)
    raise TypeError(f"unsupported failure class: {value!r}")


def _default_result_actions() -> list[ExternalDominionResultBoundaryAction]:
    return [
        ExternalDominionResultBoundaryAction.REJECT_RAW_OUTPUT,
        ExternalDominionResultBoundaryAction.REQUIRE_RESULT_ENVELOPE,
        ExternalDominionResultBoundaryAction.REQUIRE_EVIDENCE_REFS,
        ExternalDominionResultBoundaryAction.REQUIRE_NO_MEMORY_PERSISTENCE,
        ExternalDominionResultBoundaryAction.ALLOW_SCHEMA_ONLY,
    ]


@dataclass(frozen=True)
class ExternalDominionApprovalRequirement:
    requirement_id: str
    target_id: str
    candidate_id: str | None
    dry_run_plan_id: str | None
    dry_run_report_id: str | None
    requested_level: DominionLevel | int | str
    status: ExternalDominionApprovalRequirementStatus | str
    required_evidence_refs: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    required_boundary_checks: list[str] = field(default_factory=list)
    required_result_boundary_actions: list[ExternalDominionResultBoundaryAction | str] = field(
        default_factory=_default_result_actions
    )
    requires_human_review: bool = True
    requires_future_gate: bool = False
    reason: str = "Approval boundary requirement is contract-only."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("requirement_id", self.requirement_id)
        _require_non_blank("target_id", self.target_id)
        requested = normalize_dominion_level(self.requested_level)
        _normalize_requirement_status(self.status)
        _validate_string_list("required_evidence_refs", self.required_evidence_refs)
        _validate_string_list("required_reviews", self.required_reviews)
        _validate_string_list("required_boundary_checks", self.required_boundary_checks)
        [_normalize_result_action(action) for action in self.required_result_boundary_actions]
        _require_non_blank("reason", self.reason)
        if requested > V0306_MAX_GRANTABLE_LEVEL and self.requires_future_gate is not True:
            raise ValueError("D4-D9 approval requirements require future gate in v0.30.6")

    @property
    def approval_granted(self) -> bool:
        return False

    @property
    def approves_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionApprovalCandidate:
    approval_candidate_id: str
    requirement_id: str
    target_id: str
    candidate_id: str | None
    requested_decision: ExternalDominionApprovalDecisionType | str
    requested_level: DominionLevel | int | str
    proposed_scope_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    ready_for_decision_record: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_candidate_id", self.approval_candidate_id)
        _require_non_blank("requirement_id", self.requirement_id)
        _require_non_blank("target_id", self.target_id)
        decision = _normalize_approval_decision(self.requested_decision)
        requested = normalize_dominion_level(self.requested_level)
        _validate_string_list("proposed_scope_refs", self.proposed_scope_refs)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("unresolved_risks", self.unresolved_risks)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.6")
        if requested > V0306_MAX_GRANTABLE_LEVEL and self.ready_for_execution is not False:
            raise ValueError("D4-D9 requested levels must not become execution-ready")
        if (
            decision is ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW
            and _has_high_risk(self.unresolved_risks)
            and not bool(self.metadata.get("future_gate_required"))
        ):
            raise ValueError("unresolved high-risk surfaces require future gate before certification review")

    @property
    def approval_granted(self) -> bool:
        return False

    @property
    def approves_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionApprovalDecisionRecord:
    approval_decision_id: str
    approval_candidate_id: str
    requirement_id: str
    target_id: str
    decision: ExternalDominionApprovalDecisionType | str
    approved_for_certification_review: bool
    approved_for_execution: bool
    reason: str
    evidence_refs: list[str] = field(default_factory=list)
    reviewer_refs: list[str] = field(default_factory=list)
    required_next_stage: str = "v0.30.7 certification matrix"
    future_gate_required: bool = False
    blocked_reasons: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_decision_id", self.approval_decision_id)
        _require_non_blank("approval_candidate_id", self.approval_candidate_id)
        _require_non_blank("requirement_id", self.requirement_id)
        _require_non_blank("target_id", self.target_id)
        decision = _normalize_approval_decision(self.decision)
        _require_non_blank("reason", self.reason)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("reviewer_refs", self.reviewer_refs)
        _require_non_blank("required_next_stage", self.required_next_stage)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.approved_for_execution is not False:
            raise ValueError("approved_for_execution must always be False in v0.30.6")
        if self.approved_for_certification_review and decision is not ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW:
            raise ValueError("approved_for_certification_review is only valid for allow_certification_review")
        if decision is ExternalDominionApprovalDecisionType.BLOCKED and not self.blocked_reasons:
            raise ValueError("blocked approval decision requires blocked_reasons")
        if decision is ExternalDominionApprovalDecisionType.FUTURE_TRACK and self.future_gate_required is not True:
            raise ValueError("future_track approval decision requires future_gate_required=True")

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionAuditPolicy:
    audit_policy_id: str
    target_id: str
    candidate_id: str | None
    required_event_kinds: list[ExternalDominionAuditEventKind | str] = field(default_factory=list)
    required_object_refs: list[str] = field(default_factory=list)
    required_evidence_refs: list[str] = field(default_factory=list)
    require_ocel_visibility: bool = True
    require_append_only: bool = True
    require_redaction_log: bool = True
    prohibit_raw_payload_logging: bool = True
    prohibit_secret_logging: bool = True
    retention_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_policy_id", self.audit_policy_id)
        _require_non_blank("target_id", self.target_id)
        for event_kind in self.required_event_kinds:
            if isinstance(event_kind, str):
                ExternalDominionAuditEventKind(event_kind)
            elif not isinstance(event_kind, ExternalDominionAuditEventKind):
                raise TypeError("required_event_kinds must contain audit event kinds or strings")
        _validate_string_list("required_object_refs", self.required_object_refs)
        _validate_string_list("required_evidence_refs", self.required_evidence_refs)
        _validate_string_list("retention_notes", self.retention_notes)
        if self.require_ocel_visibility is not True:
            raise ValueError("require_ocel_visibility must default to True")
        if self.require_append_only is not True:
            raise ValueError("require_append_only must default to True")
        if self.prohibit_raw_payload_logging is not True:
            raise ValueError("prohibit_raw_payload_logging must default to True")
        if self.prohibit_secret_logging is not True:
            raise ValueError("prohibit_secret_logging must default to True")

    @property
    def executes_audit(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionAuditTrailPlan:
    audit_trail_plan_id: str
    audit_policy_id: str
    target_id: str
    candidate_id: str | None
    planned_event_kinds: list[ExternalDominionAuditEventKind | str]
    planned_object_refs: list[str]
    planned_evidence_refs: list[str]
    explicitly_not_logged: list[str] = field(default_factory=lambda: ["raw external payload", "credential value"])
    no_raw_payload_guarantee: bool = True
    no_secret_logging_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_plan_id", self.audit_trail_plan_id)
        _require_non_blank("audit_policy_id", self.audit_policy_id)
        _require_non_blank("target_id", self.target_id)
        for event_kind in self.planned_event_kinds:
            if isinstance(event_kind, str):
                ExternalDominionAuditEventKind(event_kind)
            elif not isinstance(event_kind, ExternalDominionAuditEventKind):
                raise TypeError("planned_event_kinds must contain audit event kinds or strings")
        _validate_string_list("planned_object_refs", self.planned_object_refs)
        _validate_string_list("planned_evidence_refs", self.planned_evidence_refs)
        _validate_string_list("explicitly_not_logged", self.explicitly_not_logged)
        if self.no_raw_payload_guarantee is not True:
            raise ValueError("no_raw_payload_guarantee must be True")
        if self.no_secret_logging_guarantee is not True:
            raise ValueError("no_secret_logging_guarantee must be True")

    @property
    def emits_events(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionOCELTracePlan:
    trace_plan_id: str
    target_id: str
    candidate_id: str | None
    process_instance_type: str
    planned_event_types: list[str]
    planned_object_types: list[str]
    planned_relation_types: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    ocel_visibility_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_plan_id", self.trace_plan_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("process_instance_type", self.process_instance_type)
        _validate_string_list("planned_event_types", self.planned_event_types)
        _validate_string_list("planned_object_types", self.planned_object_types)
        _validate_string_list("planned_relation_types", self.planned_relation_types)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.ocel_visibility_required is not True:
            raise ValueError("ocel_visibility_required must default to True")

    @property
    def emits_events(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionResultBoundaryPolicy:
    result_boundary_policy_id: str
    target_id: str
    candidate_id: str | None
    required_actions: list[ExternalDominionResultBoundaryAction | str] = field(default_factory=_default_result_actions)
    forbidden_result_fields: list[str] = field(default_factory=lambda: ["raw_output", "credential_value", "secret_value"])
    required_result_fields: list[str] = field(default_factory=lambda: ["summary", "evidence_refs", "boundary_notes"])
    raw_output_allowed: bool = False
    memory_persistence_allowed: bool = False
    result_envelope_required: bool = True
    summary_only_required: bool = True
    redaction_required: bool = True
    evidence_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("result_boundary_policy_id", self.result_boundary_policy_id)
        _require_non_blank("target_id", self.target_id)
        actions = {_normalize_result_action(action) for action in self.required_actions}
        _validate_string_list("forbidden_result_fields", self.forbidden_result_fields)
        _validate_string_list("required_result_fields", self.required_result_fields)
        if self.raw_output_allowed is not False:
            raise ValueError("raw_output_allowed must default to False")
        if self.memory_persistence_allowed is not False:
            raise ValueError("memory_persistence_allowed must default to False")
        if self.result_envelope_required is not True:
            raise ValueError("result_envelope_required must default to True")
        if self.evidence_required is not True:
            raise ValueError("evidence_required must default to True")
        required = {
            ExternalDominionResultBoundaryAction.REJECT_RAW_OUTPUT,
            ExternalDominionResultBoundaryAction.REQUIRE_RESULT_ENVELOPE,
            ExternalDominionResultBoundaryAction.REQUIRE_NO_MEMORY_PERSISTENCE,
        }
        if not required.issubset(actions):
            raise ValueError("result boundary must reject raw output and memory persistence by default")

    @property
    def ingests_result(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionRollbackPlan:
    rollback_plan_id: str
    target_id: str
    candidate_id: str | None
    rollback_available: bool = False
    rollback_steps: list[str] = field(default_factory=list)
    rollback_limitations: list[str] = field(default_factory=list)
    no_rollback_execution_guarantee: bool = True
    fallback_no_op_required: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("rollback_plan_id", self.rollback_plan_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("rollback_steps", self.rollback_steps)
        _validate_string_list("rollback_limitations", self.rollback_limitations)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.no_rollback_execution_guarantee is not True:
            raise ValueError("no_rollback_execution_guarantee must be True")
        if self.rollback_available is False and self.fallback_no_op_required is not True:
            raise ValueError("fallback_no_op_required must be True if rollback is unavailable")
        lowered = " ".join(self.rollback_steps).lower()
        if any(term in lowered for term in ("execute ", "invoke ", "call ", "run ", "send ")):
            raise ValueError("rollback_steps must be descriptive only")

    @property
    def executes_rollback(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionNoOpBoundary:
    no_op_boundary_id: str
    target_id: str
    candidate_id: str | None
    reason: str
    safe_alternatives: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_boundary_id", self.no_op_boundary_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("evidence_refs", self.evidence_refs)

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionFailureClassification:
    failure_classification_id: str
    target_id: str
    candidate_id: str | None
    failure_class: ExternalDominionFailureClass | str
    description: str
    severity: str = "unknown"
    recoverable: bool = False
    retry_allowed: bool = False
    retry_deferred: bool = True
    no_op_recommended: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("failure_classification_id", self.failure_classification_id)
        _require_non_blank("target_id", self.target_id)
        _normalize_failure_class(self.failure_class)
        _require_non_blank("description", self.description)
        _require_non_blank("severity", self.severity)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.retry_allowed is not False:
            raise ValueError("retry_allowed must default False for external dominion failures")
        if self.retry_allowed is False and self.retry_deferred is not True:
            raise ValueError("retry_deferred should be True when retry is not currently allowed")

    @property
    def retries(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionRetryDeferralPolicy:
    retry_policy_id: str
    target_id: str
    candidate_id: str | None = None
    retry_allowed_now: bool = False
    retry_future_track: bool = True
    max_retry_count: int = 0
    deferral_reason: str = "Retry is deferred by v0.30.6 boundary."
    required_future_gate: str | None = "v0.30.7 certification matrix"
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("retry_policy_id", self.retry_policy_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("deferral_reason", self.deferral_reason)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.retry_allowed_now is not False:
            raise ValueError("retry_allowed_now must default False in v0.30.6")
        if self.max_retry_count != 0:
            raise ValueError("max_retry_count must be 0 in v0.30.6")

    @property
    def retries(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionV0307CertificationHandoff:
    handoff_id: str
    target_id: str
    candidate_id: str | None
    approval_decision_id: str | None
    audit_policy_id: str | None
    result_boundary_policy_id: str | None
    rollback_plan_id: str | None
    no_op_boundary_id: str | None
    ready_for_v0307_certification_matrix: bool
    ready_for_execution: bool
    unresolved_requirements: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("unresolved_requirements", self.unresolved_requirements)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if self.ready_for_v0307_certification_matrix:
            has_required_artifacts = all(
                (
                    self.approval_decision_id,
                    self.audit_policy_id,
                    self.result_boundary_policy_id,
                    self.rollback_plan_id or self.no_op_boundary_id,
                )
            )
            if not has_required_artifacts:
                raise ValueError("v0.30.7 handoff readiness requires approval, audit, result boundary, and rollback/no-op artifacts")

    @property
    def is_certification(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


def _candidate_id_from(value: Any) -> str | None:
    return getattr(value, "candidate_id", None)


def _target_id_from(value: Any) -> str:
    target_id = getattr(value, "target_id", "")
    _require_non_blank("target_id", target_id)
    return target_id


def _evidence_refs_from(value: Any) -> list[str]:
    refs = getattr(value, "evidence_refs", [])
    return list(refs) if isinstance(refs, list) else []


def make_approval_requirement_from_delegation_handoff(
    handoff_preview: ExternalDelegationHandoffPreview,
) -> ExternalDominionApprovalRequirement:
    requested_level = normalize_dominion_level(handoff_preview.metadata.get("requested_level", DominionLevel.D3_SIMULATE))
    future_gate = requested_level > V0306_MAX_GRANTABLE_LEVEL or handoff_preview.next_stage == "future_track"
    status = (
        ExternalDominionApprovalRequirementStatus.FUTURE_TRACK
        if future_gate
        else ExternalDominionApprovalRequirementStatus.REQUIRED
    )
    return ExternalDominionApprovalRequirement(
        requirement_id=f"external_dominion_approval_requirement:{handoff_preview.handoff_id}",
        target_id=handoff_preview.target_id,
        candidate_id=handoff_preview.candidate_id,
        dry_run_plan_id=handoff_preview.dry_run_plan_id,
        dry_run_report_id=handoff_preview.dry_run_report_id,
        requested_level=requested_level,
        status=status,
        required_evidence_refs=list(handoff_preview.evidence_refs),
        required_reviews=["human_review", "approval_boundary_review"],
        required_boundary_checks=["audit_policy", "result_boundary", "rollback_or_no_op"],
        required_result_boundary_actions=_default_result_actions(),
        requires_human_review=True,
        requires_future_gate=future_gate,
        reason="Delegation handoff preview requires approval/audit boundary; not execution approval.",
        metadata={"v0306_contract_only": True, "source_handoff_id": handoff_preview.handoff_id},
    )


def make_approval_candidate(
    requirement: ExternalDominionApprovalRequirement,
    evidence_refs: list[str] | None = None,
) -> ExternalDominionApprovalCandidate:
    requested = normalize_dominion_level(requirement.requested_level)
    risk = _has_high_risk(requirement.required_boundary_checks) or requirement.requires_future_gate
    decision = (
        ExternalDominionApprovalDecisionType.FUTURE_TRACK
        if requested > V0306_MAX_GRANTABLE_LEVEL or requirement.requires_future_gate
        else ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW
        if requirement.requires_human_review
        else ExternalDominionApprovalDecisionType.REQUIRE_MORE_EVIDENCE
        if not (evidence_refs or requirement.required_evidence_refs)
        else ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW
    )
    return ExternalDominionApprovalCandidate(
        approval_candidate_id=f"external_dominion_approval_candidate:{requirement.requirement_id}",
        requirement_id=requirement.requirement_id,
        target_id=requirement.target_id,
        candidate_id=requirement.candidate_id,
        requested_decision=decision,
        requested_level=requested,
        proposed_scope_refs=[],
        evidence_refs=list(evidence_refs if evidence_refs is not None else requirement.required_evidence_refs),
        unresolved_risks=["future gate required"] if risk else [],
        blocked_reasons=[],
        ready_for_decision_record=True,
        ready_for_execution=False,
        metadata={"v0306_contract_only": True, "future_gate_required": requirement.requires_future_gate},
    )


def make_approval_decision_record(
    candidate: ExternalDominionApprovalCandidate,
    decision: ExternalDominionApprovalDecisionType | str,
    reason: str,
    evidence_refs: list[str] | None = None,
) -> ExternalDominionApprovalDecisionRecord:
    decision_type = _normalize_approval_decision(decision)
    blocked_reasons = list(candidate.blocked_reasons)
    if decision_type is ExternalDominionApprovalDecisionType.BLOCKED and not blocked_reasons:
        blocked_reasons.append("blocked by approval boundary")
    future_gate_required = (
        decision_type is ExternalDominionApprovalDecisionType.FUTURE_TRACK
        or normalize_dominion_level(candidate.requested_level) > V0306_MAX_GRANTABLE_LEVEL
        or bool(candidate.metadata.get("future_gate_required"))
    )
    return ExternalDominionApprovalDecisionRecord(
        approval_decision_id=f"external_dominion_approval_decision:{candidate.approval_candidate_id}",
        approval_candidate_id=candidate.approval_candidate_id,
        requirement_id=candidate.requirement_id,
        target_id=candidate.target_id,
        decision=decision_type,
        approved_for_certification_review=decision_type is ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW,
        approved_for_execution=False,
        reason=reason,
        evidence_refs=list(evidence_refs if evidence_refs is not None else candidate.evidence_refs),
        reviewer_refs=["symbolic_human_reviewer"] if decision_type is ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW else [],
        required_next_stage="v0.30.7 certification matrix"
        if decision_type is ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW
        else "no_op_or_future_track",
        future_gate_required=future_gate_required,
        blocked_reasons=blocked_reasons,
        withdrawal_conditions=[
            "approval decision record is treated as execution approval",
            "approved_for_execution becomes true",
        ],
        metadata={"v0306_contract_only": True},
    )


def build_audit_policy_for_candidate(candidate_or_requirement: Any) -> ExternalDominionAuditPolicy:
    target_id = _target_id_from(candidate_or_requirement)
    candidate_id = _candidate_id_from(candidate_or_requirement)
    return ExternalDominionAuditPolicy(
        audit_policy_id=f"external_dominion_audit_policy:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        required_event_kinds=[
            ExternalDominionAuditEventKind.APPROVAL_REQUIREMENT_CREATED,
            ExternalDominionAuditEventKind.APPROVAL_CANDIDATE_CREATED,
            ExternalDominionAuditEventKind.APPROVAL_DECISION_RECORDED,
            ExternalDominionAuditEventKind.RESULT_BOUNDARY_DEFINED,
        ],
        required_object_refs=[ref for ref in [candidate_id] if ref],
        required_evidence_refs=_evidence_refs_from(candidate_or_requirement),
        require_ocel_visibility=True,
        require_append_only=True,
        require_redaction_log=True,
        prohibit_raw_payload_logging=True,
        prohibit_secret_logging=True,
        retention_notes=["contract-only audit plan; no payload persistence"],
        metadata={"v0306_contract_only": True},
    )


def build_audit_trail_plan(policy: ExternalDominionAuditPolicy) -> ExternalDominionAuditTrailPlan:
    return ExternalDominionAuditTrailPlan(
        audit_trail_plan_id=f"external_dominion_audit_trail_plan:{policy.audit_policy_id}",
        audit_policy_id=policy.audit_policy_id,
        target_id=policy.target_id,
        candidate_id=policy.candidate_id,
        planned_event_kinds=list(policy.required_event_kinds),
        planned_object_refs=list(policy.required_object_refs),
        planned_evidence_refs=list(policy.required_evidence_refs),
        explicitly_not_logged=["raw external payload", "credential value", "secret value", "unredacted private data"],
        no_raw_payload_guarantee=True,
        no_secret_logging_guarantee=True,
        metadata={"v0306_contract_only": True},
    )


def build_ocel_trace_plan_for_candidate(candidate_or_requirement: Any) -> ExternalDominionOCELTracePlan:
    target_id = _target_id_from(candidate_or_requirement)
    candidate_id = _candidate_id_from(candidate_or_requirement)
    return ExternalDominionOCELTracePlan(
        trace_plan_id=f"external_dominion_ocel_trace_plan:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        process_instance_type="external_dominion_approval_boundary_preview",
        planned_event_types=[
            "approval_requirement_created",
            "approval_decision_recorded",
            "result_boundary_defined",
            "certification_handoff_created",
        ],
        planned_object_types=["external_target", "delegation_candidate", "approval_boundary"],
        planned_relation_types=["references", "requires", "hands_off_to"],
        evidence_refs=_evidence_refs_from(candidate_or_requirement),
        ocel_visibility_required=True,
        metadata={"v0306_contract_only": True},
    )


def build_result_boundary_policy(candidate_or_requirement: Any) -> ExternalDominionResultBoundaryPolicy:
    target_id = _target_id_from(candidate_or_requirement)
    candidate_id = _candidate_id_from(candidate_or_requirement)
    return ExternalDominionResultBoundaryPolicy(
        result_boundary_policy_id=f"external_dominion_result_boundary_policy:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        required_actions=_default_result_actions(),
        raw_output_allowed=False,
        memory_persistence_allowed=False,
        result_envelope_required=True,
        summary_only_required=True,
        redaction_required=True,
        evidence_required=True,
        metadata={"v0306_contract_only": True},
    )


def build_rollback_plan(
    candidate_or_requirement: Any,
    rollback_available: bool = False,
) -> ExternalDominionRollbackPlan:
    target_id = _target_id_from(candidate_or_requirement)
    candidate_id = _candidate_id_from(candidate_or_requirement)
    return ExternalDominionRollbackPlan(
        rollback_plan_id=f"external_dominion_rollback_plan:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        rollback_available=rollback_available,
        rollback_steps=["describe reversal prerequisites only"] if rollback_available else [],
        rollback_limitations=["no external rollback can be performed in v0.30.6"],
        no_rollback_execution_guarantee=True,
        fallback_no_op_required=not rollback_available,
        evidence_refs=_evidence_refs_from(candidate_or_requirement),
        metadata={"v0306_contract_only": True},
    )


def build_no_op_boundary(
    candidate_or_requirement: Any,
    reason: str,
    blocked_reasons: list[str] | None = None,
) -> ExternalDominionNoOpBoundary:
    target_id = _target_id_from(candidate_or_requirement)
    candidate_id = _candidate_id_from(candidate_or_requirement)
    return ExternalDominionNoOpBoundary(
        no_op_boundary_id=f"external_dominion_no_op_boundary:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        reason=reason,
        safe_alternatives=["keep as observation artifact", "route to future certification review", "leave future-track"],
        blocked_reasons=list(blocked_reasons or []),
        evidence_refs=_evidence_refs_from(candidate_or_requirement),
        metadata={"v0306_contract_only": True},
    )


def classify_external_dominion_failure(
    target_id: str,
    candidate_id: str | None,
    failure_class: ExternalDominionFailureClass | str,
    description: str,
) -> ExternalDominionFailureClassification:
    normalized = _normalize_failure_class(failure_class)
    return ExternalDominionFailureClassification(
        failure_classification_id=f"external_dominion_failure:{target_id}:{normalized.value}",
        target_id=target_id,
        candidate_id=candidate_id,
        failure_class=normalized,
        description=description,
        severity="high" if normalized.value.endswith("_risk") or normalized is ExternalDominionFailureClass.BLOCKED_BY_POLICY else "medium",
        recoverable=False,
        retry_allowed=False,
        retry_deferred=True,
        no_op_recommended=True,
        evidence_refs=[],
        metadata={"v0306_contract_only": True},
    )


def build_retry_deferral_policy(
    target_id: str,
    candidate_id: str | None = None,
    reason: str | None = None,
) -> ExternalDominionRetryDeferralPolicy:
    return ExternalDominionRetryDeferralPolicy(
        retry_policy_id=f"external_dominion_retry_deferral:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        retry_allowed_now=False,
        retry_future_track=True,
        max_retry_count=0,
        deferral_reason=reason or "Retry is deferred until later explicit certification and approval gates.",
        required_future_gate="v0.30.7 certification matrix",
        evidence_refs=[],
        metadata={"v0306_contract_only": True},
    )


def build_v0307_certification_handoff(
    target_id: str,
    candidate_id: str | None = None,
    approval_decision: ExternalDominionApprovalDecisionRecord | None = None,
    audit_policy: ExternalDominionAuditPolicy | None = None,
    result_boundary_policy: ExternalDominionResultBoundaryPolicy | None = None,
    rollback_plan: ExternalDominionRollbackPlan | None = None,
    no_op_boundary: ExternalDominionNoOpBoundary | None = None,
    evidence_refs: list[str] | None = None,
) -> ExternalDominionV0307CertificationHandoff:
    ready = all((approval_decision, audit_policy, result_boundary_policy, rollback_plan or no_op_boundary))
    unresolved: list[str] = []
    if approval_decision is None:
        unresolved.append("approval decision record")
    if audit_policy is None:
        unresolved.append("audit policy")
    if result_boundary_policy is None:
        unresolved.append("result boundary policy")
    if rollback_plan is None and no_op_boundary is None:
        unresolved.append("rollback plan or no-op boundary")
    return ExternalDominionV0307CertificationHandoff(
        handoff_id=f"external_dominion_v0307_certification_handoff:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        approval_decision_id=approval_decision.approval_decision_id if approval_decision is not None else None,
        audit_policy_id=audit_policy.audit_policy_id if audit_policy is not None else None,
        result_boundary_policy_id=result_boundary_policy.result_boundary_policy_id
        if result_boundary_policy is not None
        else None,
        rollback_plan_id=rollback_plan.rollback_plan_id if rollback_plan is not None else None,
        no_op_boundary_id=no_op_boundary.no_op_boundary_id if no_op_boundary is not None else None,
        ready_for_v0307_certification_matrix=ready,
        ready_for_execution=False,
        unresolved_requirements=unresolved,
        evidence_refs=list(evidence_refs or []),
        withdrawal_conditions=[
            "v0.30.7 handoff is treated as certification completion",
            "ready_for_execution becomes true",
        ],
        metadata={"v0306_contract_only": True},
    )


def approval_boundary_preserves_v0306_no_execution(
    decision_or_candidate: ExternalDominionApprovalDecisionRecord | ExternalDominionApprovalCandidate,
) -> bool:
    if isinstance(decision_or_candidate, ExternalDominionApprovalDecisionRecord):
        return decision_or_candidate.approved_for_execution is False and decision_or_candidate.executes is False
    return decision_or_candidate.ready_for_execution is False and decision_or_candidate.approves_execution is False


def audit_policy_preserves_no_raw_secret_logging(policy: ExternalDominionAuditPolicy) -> bool:
    return policy.prohibit_raw_payload_logging is True and policy.prohibit_secret_logging is True


def result_boundary_rejects_raw_memory_persistence(policy: ExternalDominionResultBoundaryPolicy) -> bool:
    return (
        policy.raw_output_allowed is False
        and policy.memory_persistence_allowed is False
        and ExternalDominionResultBoundaryAction.REJECT_RAW_OUTPUT
        in {_normalize_result_action(action) for action in policy.required_actions}
        and ExternalDominionResultBoundaryAction.REQUIRE_NO_MEMORY_PERSISTENCE
        in {_normalize_result_action(action) for action in policy.required_actions}
    )


def rollback_plan_preserves_no_execution(plan: ExternalDominionRollbackPlan) -> bool:
    return plan.no_rollback_execution_guarantee is True and plan.executes_rollback is False


def high_risk_approval_decision_type(risk_terms: list[str]) -> ExternalDominionApprovalDecisionType:
    if _has_high_risk(risk_terms):
        return ExternalDominionApprovalDecisionType.REQUIRE_HUMAN_REVIEW
    return ExternalDominionApprovalDecisionType.ALLOW_CERTIFICATION_REVIEW
