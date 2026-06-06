from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.certification import (
    ExternalDominionV0308PreviewGateHandoff,
)
from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level


V0308_MAX_ALLOWED_LEVEL = DominionLevel.D3_SIMULATE


class LimitedExternalDominionPreviewGateStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    ELIGIBLE_FOR_GATE_REVIEW = "eligible_for_gate_review"
    IN_GATE_REVIEW = "in_gate_review"
    GATE_PASSED_FOR_CONSOLIDATION = "gate_passed_for_consolidation"
    PASSED_WITH_LIMITATIONS_FOR_CONSOLIDATION = "passed_with_limitations_for_consolidation"
    DENIED = "denied"
    DEFERRED = "deferred"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class LimitedExternalDominionPreviewDecisionType(StrEnum):
    PASS_FOR_V0309_CONSOLIDATION = "pass_for_v0309_consolidation"
    PASS_WITH_LIMITATIONS_FOR_V0309_CONSOLIDATION = "pass_with_limitations_for_v0309_consolidation"
    REQUIRE_MORE_EVIDENCE = "require_more_evidence"
    REQUIRE_MORE_BOUNDARY_WORK = "require_more_boundary_work"
    REQUIRE_MORE_CERTIFICATION_WORK = "require_more_certification_work"
    DENY = "deny"
    DEFER = "defer"
    BLOCK = "block"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class LimitedExternalDominionPreviewScopeKind(StrEnum):
    OBSERVATION_PREVIEW = "observation_preview"
    DIGESTION_PREVIEW = "digestion_preview"
    DOMINION_AUTHORITY_PREVIEW = "dominion_authority_preview"
    DELEGATION_PACKET_PREVIEW = "delegation_packet_preview"
    DRY_RUN_PLAN_PREVIEW = "dry_run_plan_preview"
    DRY_RUN_REPORT_PREVIEW = "dry_run_report_preview"
    APPROVAL_BOUNDARY_PREVIEW = "approval_boundary_preview"
    AUDIT_BOUNDARY_PREVIEW = "audit_boundary_preview"
    RESULT_BOUNDARY_PREVIEW = "result_boundary_preview"
    ROLLBACK_NO_OP_PREVIEW = "rollback_no_op_preview"
    CERTIFICATION_MATRIX_PREVIEW = "certification_matrix_preview"
    HANDOFF_PREVIEW = "handoff_preview"
    UNKNOWN = "unknown"


class LimitedExternalDominionPreviewDenyDeferReason(StrEnum):
    INSUFFICIENT_CERTIFICATION = "insufficient_certification"
    UNRESOLVED_BLOCKING_CASE = "unresolved_blocking_case"
    MISSING_APPROVAL_BOUNDARY = "missing_approval_boundary"
    MISSING_AUDIT_POLICY = "missing_audit_policy"
    MISSING_RESULT_BOUNDARY = "missing_result_boundary"
    MISSING_ROLLBACK_OR_NO_OP = "missing_rollback_or_no_op"
    OCEL_VISIBILITY_MISSING = "ocel_visibility_missing"
    PROVIDER_GATE_INHERITANCE_MISSING = "provider_gate_inheritance_missing"
    READY_FOR_EXECUTION_NOT_FALSE = "ready_for_execution_not_false"
    LIMITED_PREVIEW_EXECUTION_REQUESTED = "limited_preview_execution_requested"
    PRODUCTION_CERTIFICATION_REQUESTED = "production_certification_requested"
    NETWORK_SURFACE_UNRESOLVED = "network_surface_unresolved"
    CREDENTIAL_SURFACE_UNRESOLVED = "credential_surface_unresolved"
    COMMAND_SURFACE_UNRESOLVED = "command_surface_unresolved"
    PROVIDER_SURFACE_UNRESOLVED = "provider_surface_unresolved"
    BROWSER_SURFACE_UNRESOLVED = "browser_surface_unresolved"
    RPA_SURFACE_UNRESOLVED = "rpa_surface_unresolved"
    GATEWAY_SURFACE_UNRESOLVED = "gateway_surface_unresolved"
    DELEGATION_SURFACE_UNRESOLVED = "delegation_surface_unresolved"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    SECRET_LOGGING_RISK = "secret_logging_risk"
    MEMORY_CONTAMINATION_RISK = "memory_contamination_risk"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    UNKNOWN = "unknown"


REQUIRED_RUNTIME_PROHIBITIONS = [
    "external execution",
    "network access",
    "credential access",
    "command execution",
    "provider invocation",
    "browser automation",
    "RPA control",
    "gateway control",
    "packet send",
    "rollback execution",
]


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _normalize_status(value: LimitedExternalDominionPreviewGateStatus | str) -> LimitedExternalDominionPreviewGateStatus:
    if isinstance(value, LimitedExternalDominionPreviewGateStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("preview gate status must not be blank")
        return LimitedExternalDominionPreviewGateStatus(stripped)
    raise TypeError(f"unsupported preview gate status: {value!r}")


def _normalize_decision(value: LimitedExternalDominionPreviewDecisionType | str) -> LimitedExternalDominionPreviewDecisionType:
    if isinstance(value, LimitedExternalDominionPreviewDecisionType):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("preview decision must not be blank")
        return LimitedExternalDominionPreviewDecisionType(stripped)
    raise TypeError(f"unsupported preview decision: {value!r}")


def _normalize_scope_kind(value: LimitedExternalDominionPreviewScopeKind | str) -> LimitedExternalDominionPreviewScopeKind:
    if isinstance(value, LimitedExternalDominionPreviewScopeKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("scope_kind must not be blank")
        return LimitedExternalDominionPreviewScopeKind(stripped)
    raise TypeError(f"unsupported preview scope kind: {value!r}")


def _normalize_reason(
    value: LimitedExternalDominionPreviewDenyDeferReason | str,
) -> LimitedExternalDominionPreviewDenyDeferReason:
    if isinstance(value, LimitedExternalDominionPreviewDenyDeferReason):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("deny/defer reason must not be blank")
        return LimitedExternalDominionPreviewDenyDeferReason(stripped)
    raise TypeError(f"unsupported deny/defer reason: {value!r}")


def _is_pass_decision(decision: LimitedExternalDominionPreviewDecisionType) -> bool:
    return decision in {
        LimitedExternalDominionPreviewDecisionType.PASS_FOR_V0309_CONSOLIDATION,
        LimitedExternalDominionPreviewDecisionType.PASS_WITH_LIMITATIONS_FOR_V0309_CONSOLIDATION,
    }


@dataclass(frozen=True)
class LimitedExternalDominionPreviewEligibilityMatrix:
    eligibility_matrix_id: str
    target_id: str
    candidate_id: str | None
    certification_matrix_id: str | None
    certification_report_id: str | None
    required_gate_conditions: list[str]
    passed_gate_conditions: list[str] = field(default_factory=list)
    failed_gate_conditions: list[str] = field(default_factory=list)
    unresolved_gate_conditions: list[str] = field(default_factory=list)
    deny_defer_reasons: list[LimitedExternalDominionPreviewDenyDeferReason | str] = field(default_factory=list)
    ready_for_gate_review: bool = False
    ready_for_v0309_consolidation: bool = False
    ready_for_limited_preview_execution: bool = False
    ready_for_execution: bool = False
    production_certified: bool = False
    live_adapter_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("eligibility_matrix_id", self.eligibility_matrix_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("required_gate_conditions", self.required_gate_conditions)
        _validate_string_list("passed_gate_conditions", self.passed_gate_conditions)
        _validate_string_list("failed_gate_conditions", self.failed_gate_conditions)
        _validate_string_list("unresolved_gate_conditions", self.unresolved_gate_conditions)
        [_normalize_reason(reason) for reason in self.deny_defer_reasons]
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.ready_for_limited_preview_execution is not False:
            raise ValueError("ready_for_limited_preview_execution must always be False in v0.30.8")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.8")
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.30.8")
        if self.live_adapter_certified is not False:
            raise ValueError("live_adapter_certified must always be False in v0.30.8")
        if self.ready_for_v0309_consolidation:
            if not self.ready_for_gate_review or self.failed_gate_conditions or self.unresolved_gate_conditions:
                raise ValueError("ready_for_v0309_consolidation requires passed gate review conditions")

    @property
    def approves_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class LimitedExternalDominionPreviewScope:
    preview_scope_id: str
    target_id: str
    candidate_id: str | None
    scope_kind: LimitedExternalDominionPreviewScopeKind | str
    allowed_artifact_refs: list[str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(REQUIRED_RUNTIME_PROHIBITIONS))
    max_allowed_level: DominionLevel | int | str = DominionLevel.D3_SIMULATE
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_scope_id", self.preview_scope_id)
        _require_non_blank("target_id", self.target_id)
        _normalize_scope_kind(self.scope_kind)
        _validate_string_list("allowed_artifact_refs", self.allowed_artifact_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("limitations", self.limitations)
        if normalize_dominion_level(self.max_allowed_level) > V0308_MAX_ALLOWED_LEVEL:
            raise ValueError("preview scope max_allowed_level cannot exceed D3_SIMULATE")
        lower = " ".join(self.prohibited_runtime_actions).lower()
        for required in REQUIRED_RUNTIME_PROHIBITIONS:
            if required.lower() not in lower:
                raise ValueError("prohibited_runtime_actions must include all runtime prohibitions")

    @property
    def allows_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class LimitedExternalDominionPreviewCandidate:
    preview_candidate_id: str
    target_id: str
    candidate_id: str | None
    eligibility_matrix_id: str
    preview_scope: LimitedExternalDominionPreviewScope
    requested_preview_kind: LimitedExternalDominionPreviewScopeKind | str
    source_certification_report_id: str | None = None
    source_handoff_id: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    unresolved_requirements: list[str] = field(default_factory=list)
    requested_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_candidate_id", self.preview_candidate_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("eligibility_matrix_id", self.eligibility_matrix_id)
        if self.preview_scope.target_id != self.target_id:
            raise ValueError("preview_scope.target_id must match preview candidate target_id")
        _normalize_scope_kind(self.requested_preview_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("unresolved_requirements", self.unresolved_requirements)
        if self.requested_execution is not False:
            raise ValueError("requested_execution must be False in v0.30.8")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.8")

    @property
    def executes_preview(self) -> bool:
        return False


@dataclass(frozen=True)
class LimitedExternalDominionPreviewDecision:
    preview_decision_id: str
    preview_candidate_id: str
    target_id: str
    decision: LimitedExternalDominionPreviewDecisionType | str
    status: LimitedExternalDominionPreviewGateStatus | str
    approved_for_v0309_consolidation: bool
    approved_for_limited_preview_execution: bool
    approved_for_execution: bool
    reason: str
    limitations: list[str] = field(default_factory=list)
    deny_defer_reasons: list[LimitedExternalDominionPreviewDenyDeferReason | str] = field(default_factory=list)
    required_followups: list[str] = field(default_factory=list)
    future_gate_required: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_decision_id", self.preview_decision_id)
        _require_non_blank("preview_candidate_id", self.preview_candidate_id)
        _require_non_blank("target_id", self.target_id)
        decision = _normalize_decision(self.decision)
        _normalize_status(self.status)
        _require_non_blank("reason", self.reason)
        _validate_string_list("limitations", self.limitations)
        [_normalize_reason(reason) for reason in self.deny_defer_reasons]
        _validate_string_list("required_followups", self.required_followups)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.approved_for_limited_preview_execution is not False:
            raise ValueError("approved_for_limited_preview_execution must always be False")
        if self.approved_for_execution is not False:
            raise ValueError("approved_for_execution must always be False")
        if self.approved_for_v0309_consolidation and not _is_pass_decision(decision):
            raise ValueError("approved_for_v0309_consolidation is only valid for pass consolidation decisions")
        if decision is LimitedExternalDominionPreviewDecisionType.PASS_WITH_LIMITATIONS_FOR_V0309_CONSOLIDATION and not self.limitations:
            raise ValueError("pass_with_limitations requires limitations")
        if decision in {
            LimitedExternalDominionPreviewDecisionType.DENY,
            LimitedExternalDominionPreviewDecisionType.DEFER,
            LimitedExternalDominionPreviewDecisionType.BLOCK,
            LimitedExternalDominionPreviewDecisionType.FUTURE_TRACK,
        } and not self.deny_defer_reasons:
            raise ValueError("deny/defer/block/future_track requires deny_defer_reasons")

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class LimitedExternalDominionPreviewAuditOCELPlan:
    preview_audit_ocel_plan_id: str
    target_id: str
    candidate_id: str | None
    preview_candidate_id: str | None
    planned_event_types: list[str]
    planned_object_types: list[str]
    planned_relation_types: list[str]
    planned_audit_artifacts: list[str]
    require_append_only: bool = True
    require_no_raw_payload_logging: bool = True
    require_no_secret_logging: bool = True
    require_result_boundary_refs: bool = True
    ocel_visibility_required: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_audit_ocel_plan_id", self.preview_audit_ocel_plan_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("planned_event_types", self.planned_event_types)
        _validate_string_list("planned_object_types", self.planned_object_types)
        _validate_string_list("planned_relation_types", self.planned_relation_types)
        _validate_string_list("planned_audit_artifacts", self.planned_audit_artifacts)
        _validate_string_list("evidence_refs", self.evidence_refs)
        for name in (
            "require_append_only",
            "require_no_raw_payload_logging",
            "require_no_secret_logging",
            "require_result_boundary_refs",
            "ocel_visibility_required",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must default True")

    @property
    def emits_events(self) -> bool:
        return False


@dataclass(frozen=True)
class LimitedExternalDominionPreviewNoOpPlan:
    preview_no_op_id: str
    target_id: str
    candidate_id: str | None
    preview_candidate_id: str | None
    reason: str
    deny_defer_reasons: list[LimitedExternalDominionPreviewDenyDeferReason | str] = field(default_factory=list)
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_no_op_id", self.preview_no_op_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("reason", self.reason)
        [_normalize_reason(reason) for reason in self.deny_defer_reasons]
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class LimitedExternalDominionPreviewGateReport:
    preview_gate_report_id: str
    target_id: str
    candidate_id: str | None
    eligibility_matrix_id: str
    preview_decision_id: str | None
    summary: str
    status: LimitedExternalDominionPreviewGateStatus | str
    decision: LimitedExternalDominionPreviewDecisionType | str
    approved_for_v0309_consolidation: bool
    approved_for_limited_preview_execution: bool
    approved_for_execution: bool
    limitations: list[str] = field(default_factory=list)
    deny_defer_reasons: list[LimitedExternalDominionPreviewDenyDeferReason | str] = field(default_factory=list)
    required_followups: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_gate_report_id", self.preview_gate_report_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("eligibility_matrix_id", self.eligibility_matrix_id)
        _require_non_blank("summary", self.summary)
        decision = _normalize_decision(self.decision)
        _normalize_status(self.status)
        _validate_string_list("limitations", self.limitations)
        [_normalize_reason(reason) for reason in self.deny_defer_reasons]
        _validate_string_list("required_followups", self.required_followups)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.approved_for_limited_preview_execution is not False:
            raise ValueError("approved_for_limited_preview_execution must always be False")
        if self.approved_for_execution is not False:
            raise ValueError("approved_for_execution must always be False")
        if self.approved_for_v0309_consolidation and not _is_pass_decision(decision):
            raise ValueError("approved_for_v0309_consolidation is only valid for pass consolidation decisions")

    @property
    def executes_preview(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionV0309ConsolidationHandoff:
    handoff_id: str
    target_id: str
    candidate_id: str | None
    preview_gate_report_id: str
    preview_decision_id: str | None
    ready_for_v0309_consolidation: bool
    ready_for_limited_preview_execution: bool
    ready_for_execution: bool
    approved_for_v0309_consolidation: bool
    approved_for_limited_preview_execution: bool
    approved_for_execution: bool
    unresolved_requirements: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("preview_gate_report_id", self.preview_gate_report_id)
        _validate_string_list("unresolved_requirements", self.unresolved_requirements)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.ready_for_limited_preview_execution is not False:
            raise ValueError("ready_for_limited_preview_execution must always be False")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if self.approved_for_limited_preview_execution is not False:
            raise ValueError("approved_for_limited_preview_execution must always be False")
        if self.approved_for_execution is not False:
            raise ValueError("approved_for_execution must always be False")
        if self.ready_for_v0309_consolidation and (not self.approved_for_v0309_consolidation or self.unresolved_requirements):
            raise ValueError("ready_for_v0309_consolidation requires consolidation approval and no unresolved requirements")

    @property
    def executes(self) -> bool:
        return False


def build_preview_eligibility_matrix_from_certification_handoff(
    handoff: ExternalDominionV0308PreviewGateHandoff,
) -> LimitedExternalDominionPreviewEligibilityMatrix:
    required = [
        "certification matrix present",
        "certification report present",
        "ready for v0.30.8 gate review",
        "ready_for_limited_preview_execution false",
        "ready_for_execution false",
        "production_certified false",
        "live_adapter_certified false",
    ]
    failed: list[str] = []
    reasons: list[LimitedExternalDominionPreviewDenyDeferReason] = []
    if not handoff.ready_for_v0308_limited_preview_gate_review:
        failed.append("ready for v0.30.8 gate review")
        reasons.append(LimitedExternalDominionPreviewDenyDeferReason.INSUFFICIENT_CERTIFICATION)
    if handoff.ready_for_limited_preview_execution:
        failed.append("ready_for_limited_preview_execution false")
        reasons.append(LimitedExternalDominionPreviewDenyDeferReason.LIMITED_PREVIEW_EXECUTION_REQUESTED)
    if handoff.ready_for_execution or handoff.production_certified or handoff.live_adapter_certified:
        failed.append("runtime readiness flags false")
        reasons.append(LimitedExternalDominionPreviewDenyDeferReason.READY_FOR_EXECUTION_NOT_FALSE)
    unresolved = list(handoff.unresolved_requirements)
    if unresolved:
        reasons.append(LimitedExternalDominionPreviewDenyDeferReason.UNRESOLVED_BLOCKING_CASE)
    passed = [condition for condition in required if condition not in failed]
    ready_gate = not failed and not unresolved
    return LimitedExternalDominionPreviewEligibilityMatrix(
        eligibility_matrix_id=f"limited_external_dominion_preview_eligibility:{handoff.handoff_id}",
        target_id=handoff.target_id,
        candidate_id=handoff.candidate_id,
        certification_matrix_id=handoff.certification_matrix_id,
        certification_report_id=handoff.certification_report_id,
        required_gate_conditions=required,
        passed_gate_conditions=passed,
        failed_gate_conditions=failed,
        unresolved_gate_conditions=unresolved,
        deny_defer_reasons=reasons,
        ready_for_gate_review=ready_gate,
        ready_for_v0309_consolidation=ready_gate,
        ready_for_limited_preview_execution=False,
        ready_for_execution=False,
        production_certified=False,
        live_adapter_certified=False,
        evidence_refs=list(handoff.evidence_refs),
        metadata={"v0308_contract_only": True, "source_handoff_id": handoff.handoff_id},
    )


def build_preview_scope_from_eligibility(
    matrix: LimitedExternalDominionPreviewEligibilityMatrix,
    scope_kind: LimitedExternalDominionPreviewScopeKind | str | None = None,
) -> LimitedExternalDominionPreviewScope:
    return LimitedExternalDominionPreviewScope(
        preview_scope_id=f"limited_external_dominion_preview_scope:{matrix.eligibility_matrix_id}",
        target_id=matrix.target_id,
        candidate_id=matrix.candidate_id,
        scope_kind=scope_kind or LimitedExternalDominionPreviewScopeKind.CERTIFICATION_MATRIX_PREVIEW,
        allowed_artifact_refs=[
            ref for ref in [matrix.certification_matrix_id, matrix.certification_report_id] if ref
        ],
        prohibited_runtime_actions=list(REQUIRED_RUNTIME_PROHIBITIONS),
        max_allowed_level=V0308_MAX_ALLOWED_LEVEL,
        evidence_refs=list(matrix.evidence_refs),
        limitations=[],
        metadata={"v0308_contract_only": True},
    )


def build_limited_preview_candidate(
    matrix: LimitedExternalDominionPreviewEligibilityMatrix,
    scope: LimitedExternalDominionPreviewScope,
    source_handoff: ExternalDominionV0308PreviewGateHandoff | None = None,
) -> LimitedExternalDominionPreviewCandidate:
    return LimitedExternalDominionPreviewCandidate(
        preview_candidate_id=f"limited_external_dominion_preview_candidate:{matrix.eligibility_matrix_id}",
        target_id=matrix.target_id,
        candidate_id=matrix.candidate_id,
        eligibility_matrix_id=matrix.eligibility_matrix_id,
        preview_scope=scope,
        requested_preview_kind=scope.scope_kind,
        source_certification_report_id=matrix.certification_report_id,
        source_handoff_id=source_handoff.handoff_id if source_handoff is not None else None,
        evidence_refs=list(matrix.evidence_refs),
        limitations=[],
        unresolved_requirements=list(matrix.unresolved_gate_conditions),
        requested_execution=False,
        ready_for_execution=False,
        metadata={"v0308_contract_only": True},
    )


def make_limited_preview_decision(
    candidate: LimitedExternalDominionPreviewCandidate,
    decision: LimitedExternalDominionPreviewDecisionType | str | None = None,
    reason: str | None = None,
) -> LimitedExternalDominionPreviewDecision:
    if decision is None:
        decision_type = (
            LimitedExternalDominionPreviewDecisionType.REQUIRE_MORE_BOUNDARY_WORK
            if candidate.unresolved_requirements
            else LimitedExternalDominionPreviewDecisionType.PASS_WITH_LIMITATIONS_FOR_V0309_CONSOLIDATION
            if candidate.limitations
            else LimitedExternalDominionPreviewDecisionType.PASS_FOR_V0309_CONSOLIDATION
        )
    else:
        decision_type = _normalize_decision(decision)
    status = (
        LimitedExternalDominionPreviewGateStatus.GATE_PASSED_FOR_CONSOLIDATION
        if decision_type is LimitedExternalDominionPreviewDecisionType.PASS_FOR_V0309_CONSOLIDATION
        else LimitedExternalDominionPreviewGateStatus.PASSED_WITH_LIMITATIONS_FOR_CONSOLIDATION
        if decision_type is LimitedExternalDominionPreviewDecisionType.PASS_WITH_LIMITATIONS_FOR_V0309_CONSOLIDATION
        else LimitedExternalDominionPreviewGateStatus.DEFERRED
        if decision_type
        in {
            LimitedExternalDominionPreviewDecisionType.REQUIRE_MORE_EVIDENCE,
            LimitedExternalDominionPreviewDecisionType.REQUIRE_MORE_BOUNDARY_WORK,
            LimitedExternalDominionPreviewDecisionType.REQUIRE_MORE_CERTIFICATION_WORK,
            LimitedExternalDominionPreviewDecisionType.DEFER,
        }
        else LimitedExternalDominionPreviewGateStatus.BLOCKED
        if decision_type is LimitedExternalDominionPreviewDecisionType.BLOCK
        else LimitedExternalDominionPreviewGateStatus.FUTURE_TRACK
        if decision_type is LimitedExternalDominionPreviewDecisionType.FUTURE_TRACK
        else LimitedExternalDominionPreviewGateStatus.NO_OP
        if decision_type is LimitedExternalDominionPreviewDecisionType.NO_OP
        else LimitedExternalDominionPreviewGateStatus.DENIED
    )
    deny_reasons: list[LimitedExternalDominionPreviewDenyDeferReason] = []
    if not _is_pass_decision(decision_type):
        deny_reasons.append(
            LimitedExternalDominionPreviewDenyDeferReason.UNRESOLVED_BLOCKING_CASE
            if candidate.unresolved_requirements
            else LimitedExternalDominionPreviewDenyDeferReason.INSUFFICIENT_CERTIFICATION
        )
    return LimitedExternalDominionPreviewDecision(
        preview_decision_id=f"limited_external_dominion_preview_decision:{candidate.preview_candidate_id}",
        preview_candidate_id=candidate.preview_candidate_id,
        target_id=candidate.target_id,
        decision=decision_type,
        status=status,
        approved_for_v0309_consolidation=_is_pass_decision(decision_type),
        approved_for_limited_preview_execution=False,
        approved_for_execution=False,
        reason=reason or "Preview gate decision is consolidation-only and non-executing.",
        limitations=list(candidate.limitations),
        deny_defer_reasons=deny_reasons,
        required_followups=list(candidate.unresolved_requirements),
        future_gate_required=decision_type is LimitedExternalDominionPreviewDecisionType.FUTURE_TRACK,
        evidence_refs=list(candidate.evidence_refs),
        withdrawal_conditions=[
            "preview gate decision is treated as execution approval",
            "limited preview execution readiness becomes true",
        ],
        metadata={"v0308_contract_only": True},
    )


def build_preview_audit_ocel_plan(
    candidate_or_decision: LimitedExternalDominionPreviewCandidate | LimitedExternalDominionPreviewDecision,
) -> LimitedExternalDominionPreviewAuditOCELPlan:
    target_id = candidate_or_decision.target_id
    candidate_id = getattr(candidate_or_decision, "candidate_id", None)
    preview_candidate_id = getattr(candidate_or_decision, "preview_candidate_id", None)
    return LimitedExternalDominionPreviewAuditOCELPlan(
        preview_audit_ocel_plan_id=f"limited_external_dominion_preview_audit_ocel_plan:{preview_candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        preview_candidate_id=preview_candidate_id,
        planned_event_types=["preview_gate_reviewed", "preview_gate_report_created", "v0309_handoff_created"],
        planned_object_types=["external_target", "preview_candidate", "preview_gate_report"],
        planned_relation_types=["references", "gates", "hands_off_to"],
        planned_audit_artifacts=["eligibility_matrix", "preview_decision", "preview_gate_report"],
        require_append_only=True,
        require_no_raw_payload_logging=True,
        require_no_secret_logging=True,
        require_result_boundary_refs=True,
        ocel_visibility_required=True,
        evidence_refs=list(candidate_or_decision.evidence_refs),
        metadata={"v0308_contract_only": True},
    )


def build_preview_no_op_plan(
    candidate_or_decision: LimitedExternalDominionPreviewCandidate | LimitedExternalDominionPreviewDecision,
    reason: str,
    deny_defer_reasons: list[LimitedExternalDominionPreviewDenyDeferReason | str] | None = None,
) -> LimitedExternalDominionPreviewNoOpPlan:
    return LimitedExternalDominionPreviewNoOpPlan(
        preview_no_op_id=f"limited_external_dominion_preview_no_op:{getattr(candidate_or_decision, 'preview_candidate_id', candidate_or_decision.target_id)}",
        target_id=candidate_or_decision.target_id,
        candidate_id=getattr(candidate_or_decision, "candidate_id", None),
        preview_candidate_id=getattr(candidate_or_decision, "preview_candidate_id", None),
        reason=reason,
        deny_defer_reasons=list(deny_defer_reasons or []),
        safe_alternatives=["defer to v0.30.9 consolidation without execution", "keep future-track", "request more boundary evidence"],
        evidence_refs=list(candidate_or_decision.evidence_refs),
        metadata={"v0308_contract_only": True},
    )


def build_preview_gate_report(
    matrix: LimitedExternalDominionPreviewEligibilityMatrix,
    decision: LimitedExternalDominionPreviewDecision | None = None,
    no_op_plan: LimitedExternalDominionPreviewNoOpPlan | None = None,
) -> LimitedExternalDominionPreviewGateReport:
    decision_type = (
        _normalize_decision(decision.decision)
        if decision is not None
        else LimitedExternalDominionPreviewDecisionType.NO_OP
        if no_op_plan is not None
        else LimitedExternalDominionPreviewDecisionType.DEFER
    )
    status = (
        _normalize_status(decision.status)
        if decision is not None
        else LimitedExternalDominionPreviewGateStatus.NO_OP
        if no_op_plan is not None
        else LimitedExternalDominionPreviewGateStatus.DEFERRED
    )
    approved_consolidation = decision.approved_for_v0309_consolidation if decision is not None else False
    return LimitedExternalDominionPreviewGateReport(
        preview_gate_report_id=f"limited_external_dominion_preview_gate_report:{matrix.eligibility_matrix_id}",
        target_id=matrix.target_id,
        candidate_id=matrix.candidate_id,
        eligibility_matrix_id=matrix.eligibility_matrix_id,
        preview_decision_id=decision.preview_decision_id if decision is not None else None,
        summary="Limited external dominion preview gate report; consolidation-only.",
        status=status,
        decision=decision_type,
        approved_for_v0309_consolidation=approved_consolidation,
        approved_for_limited_preview_execution=False,
        approved_for_execution=False,
        limitations=list(decision.limitations if decision is not None else []),
        deny_defer_reasons=list(decision.deny_defer_reasons if decision is not None else matrix.deny_defer_reasons),
        required_followups=list(decision.required_followups if decision is not None else matrix.unresolved_gate_conditions),
        evidence_refs=list(matrix.evidence_refs),
        withdrawal_conditions=[
            "preview gate report is treated as preview execution",
            "approved_for_limited_preview_execution becomes true",
        ],
        metadata={"v0308_contract_only": True},
    )


def build_v0309_consolidation_handoff(
    report: LimitedExternalDominionPreviewGateReport,
    decision: LimitedExternalDominionPreviewDecision | None = None,
) -> ExternalDominionV0309ConsolidationHandoff:
    approved = report.approved_for_v0309_consolidation and (decision.approved_for_v0309_consolidation if decision is not None else True)
    unresolved = list(report.required_followups)
    return ExternalDominionV0309ConsolidationHandoff(
        handoff_id=f"external_dominion_v0309_consolidation_handoff:{report.preview_gate_report_id}",
        target_id=report.target_id,
        candidate_id=report.candidate_id,
        preview_gate_report_id=report.preview_gate_report_id,
        preview_decision_id=report.preview_decision_id,
        ready_for_v0309_consolidation=approved and not unresolved,
        ready_for_limited_preview_execution=False,
        ready_for_execution=False,
        approved_for_v0309_consolidation=approved,
        approved_for_limited_preview_execution=False,
        approved_for_execution=False,
        unresolved_requirements=unresolved,
        limitations=list(report.limitations),
        evidence_refs=list(report.evidence_refs),
        withdrawal_conditions=[
            "v0.30.9 handoff is treated as runtime readiness",
            "execution readiness becomes true",
        ],
        metadata={"v0308_contract_only": True},
    )


def preview_scope_blocks_runtime_actions(scope: LimitedExternalDominionPreviewScope) -> bool:
    lower = " ".join(scope.prohibited_runtime_actions).lower()
    return scope.allows_execution is False and all(required.lower() in lower for required in REQUIRED_RUNTIME_PROHIBITIONS)


def preview_decision_preserves_execution_false(decision: LimitedExternalDominionPreviewDecision) -> bool:
    return (
        decision.approved_for_limited_preview_execution is False
        and decision.approved_for_execution is False
        and decision.executes is False
    )


def preview_gate_preserves_no_execution(obj: Any) -> bool:
    return (
        getattr(obj, "ready_for_limited_preview_execution", False) is False
        and getattr(obj, "ready_for_execution", False) is False
        and getattr(obj, "approved_for_limited_preview_execution", False) is False
        and getattr(obj, "approved_for_execution", False) is False
        and getattr(obj, "production_certified", False) is False
        and getattr(obj, "live_adapter_certified", False) is False
    )


def preview_gate_allows_consolidation_only(obj: Any) -> bool:
    return preview_gate_preserves_no_execution(obj) and bool(
        getattr(obj, "ready_for_v0309_consolidation", True)
        or getattr(obj, "approved_for_v0309_consolidation", True)
        or getattr(obj, "ready_for_gate_review", True)
    )
