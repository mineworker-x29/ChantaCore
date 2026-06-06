from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ExternalDominionCertificationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_REVIEW = "in_review"
    PASSED = "passed"
    PASSED_WITH_LIMITATIONS = "passed_with_limitations"
    FAILED = "failed"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalDominionCertificationDecision(StrEnum):
    PASS_FOR_LIMITED_PREVIEW_GATE_REVIEW = "pass_for_limited_preview_gate_review"
    PASS_WITH_LIMITATIONS_FOR_LIMITED_PREVIEW_GATE_REVIEW = (
        "pass_with_limitations_for_limited_preview_gate_review"
    )
    REQUIRE_MORE_EVIDENCE = "require_more_evidence"
    REQUIRE_MORE_BOUNDARY_WORK = "require_more_boundary_work"
    FAIL = "fail"
    BLOCK = "block"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ExternalDominionCertificationCaseKind(StrEnum):
    OBSERVATION_COVERAGE = "observation_coverage"
    IDENTITY_TRUST_BOUNDARY_COVERAGE = "identity_trust_boundary_coverage"
    CAPABILITY_OBSERVATION_COVERAGE = "capability_observation_coverage"
    DIGESTION_DECISION_COVERAGE = "digestion_decision_coverage"
    AUTHORITY_BOUNDARY_COVERAGE = "authority_boundary_coverage"
    DELEGATION_DRY_RUN_COVERAGE = "delegation_dry_run_coverage"
    APPROVAL_AUDIT_ROLLBACK_COVERAGE = "approval_audit_rollback_coverage"
    NO_EXECUTION = "no_execution"
    NO_NETWORK = "no_network"
    NO_CREDENTIAL = "no_credential"
    NO_COMMAND = "no_command"
    NO_PROVIDER_BYPASS = "no_provider_bypass"
    NO_RPA = "no_rpa"
    NO_BROWSER = "no_browser"
    NO_GATEWAY = "no_gateway"
    NO_RAW_OUTPUT_PERSISTENCE = "no_raw_output_persistence"
    NO_SECRET_LOGGING = "no_secret_logging"
    RESULT_BOUNDARY = "result_boundary"
    ROLLBACK_NO_OP = "rollback_no_op"
    OCEL_VISIBILITY = "ocel_visibility"
    PROVIDER_GATE_INHERITANCE = "provider_gate_inheritance"
    D4_D9_FUTURE_TRACK = "d4_d9_future_track"
    READY_FOR_EXECUTION_FALSE = "ready_for_execution_false"
    UNKNOWN = "unknown"


class ExternalDominionCertificationSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


NO_RUNTIME_CASE_KINDS = frozenset(
    {
        ExternalDominionCertificationCaseKind.NO_EXECUTION,
        ExternalDominionCertificationCaseKind.NO_NETWORK,
        ExternalDominionCertificationCaseKind.NO_CREDENTIAL,
        ExternalDominionCertificationCaseKind.NO_COMMAND,
        ExternalDominionCertificationCaseKind.NO_PROVIDER_BYPASS,
        ExternalDominionCertificationCaseKind.NO_RPA,
        ExternalDominionCertificationCaseKind.NO_BROWSER,
        ExternalDominionCertificationCaseKind.NO_GATEWAY,
        ExternalDominionCertificationCaseKind.NO_RAW_OUTPUT_PERSISTENCE,
        ExternalDominionCertificationCaseKind.NO_SECRET_LOGGING,
        ExternalDominionCertificationCaseKind.READY_FOR_EXECUTION_FALSE,
    }
)


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _normalize_status(value: ExternalDominionCertificationStatus | str) -> ExternalDominionCertificationStatus:
    if isinstance(value, ExternalDominionCertificationStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("certification status must not be blank")
        return ExternalDominionCertificationStatus(stripped)
    raise TypeError(f"unsupported certification status: {value!r}")


def _normalize_decision(value: ExternalDominionCertificationDecision | str) -> ExternalDominionCertificationDecision:
    if isinstance(value, ExternalDominionCertificationDecision):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("certification decision must not be blank")
        return ExternalDominionCertificationDecision(stripped)
    raise TypeError(f"unsupported certification decision: {value!r}")


def _normalize_case_kind(
    value: ExternalDominionCertificationCaseKind | str,
) -> ExternalDominionCertificationCaseKind:
    if isinstance(value, ExternalDominionCertificationCaseKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("case_kind must not be blank")
        return ExternalDominionCertificationCaseKind(stripped)
    raise TypeError(f"unsupported certification case kind: {value!r}")


def _normalize_severity(value: ExternalDominionCertificationSeverity | str) -> ExternalDominionCertificationSeverity:
    if isinstance(value, ExternalDominionCertificationSeverity):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("severity must not be blank")
        return ExternalDominionCertificationSeverity(stripped)
    raise TypeError(f"unsupported certification severity: {value!r}")


def _default_case_kinds() -> list[ExternalDominionCertificationCaseKind]:
    return [
        ExternalDominionCertificationCaseKind.OBSERVATION_COVERAGE,
        ExternalDominionCertificationCaseKind.IDENTITY_TRUST_BOUNDARY_COVERAGE,
        ExternalDominionCertificationCaseKind.CAPABILITY_OBSERVATION_COVERAGE,
        ExternalDominionCertificationCaseKind.DIGESTION_DECISION_COVERAGE,
        ExternalDominionCertificationCaseKind.AUTHORITY_BOUNDARY_COVERAGE,
        ExternalDominionCertificationCaseKind.DELEGATION_DRY_RUN_COVERAGE,
        ExternalDominionCertificationCaseKind.APPROVAL_AUDIT_ROLLBACK_COVERAGE,
        ExternalDominionCertificationCaseKind.NO_EXECUTION,
        ExternalDominionCertificationCaseKind.NO_NETWORK,
        ExternalDominionCertificationCaseKind.NO_CREDENTIAL,
        ExternalDominionCertificationCaseKind.NO_COMMAND,
        ExternalDominionCertificationCaseKind.NO_PROVIDER_BYPASS,
        ExternalDominionCertificationCaseKind.NO_RPA,
        ExternalDominionCertificationCaseKind.NO_BROWSER,
        ExternalDominionCertificationCaseKind.NO_GATEWAY,
        ExternalDominionCertificationCaseKind.NO_RAW_OUTPUT_PERSISTENCE,
        ExternalDominionCertificationCaseKind.NO_SECRET_LOGGING,
        ExternalDominionCertificationCaseKind.RESULT_BOUNDARY,
        ExternalDominionCertificationCaseKind.ROLLBACK_NO_OP,
        ExternalDominionCertificationCaseKind.OCEL_VISIBILITY,
        ExternalDominionCertificationCaseKind.PROVIDER_GATE_INHERITANCE,
        ExternalDominionCertificationCaseKind.D4_D9_FUTURE_TRACK,
        ExternalDominionCertificationCaseKind.READY_FOR_EXECUTION_FALSE,
    ]


@dataclass(frozen=True)
class ExternalDominionCertificationPolicy:
    policy_id: str
    target_id: str
    candidate_id: str | None = None
    required_case_kinds: list[ExternalDominionCertificationCaseKind | str] = field(
        default_factory=_default_case_kinds
    )
    blocking_case_kinds: list[ExternalDominionCertificationCaseKind | str] = field(
        default_factory=lambda: [
            ExternalDominionCertificationCaseKind.NO_EXECUTION,
            ExternalDominionCertificationCaseKind.NO_NETWORK,
            ExternalDominionCertificationCaseKind.NO_CREDENTIAL,
            ExternalDominionCertificationCaseKind.NO_COMMAND,
            ExternalDominionCertificationCaseKind.NO_PROVIDER_BYPASS,
            ExternalDominionCertificationCaseKind.RESULT_BOUNDARY,
            ExternalDominionCertificationCaseKind.OCEL_VISIBILITY,
            ExternalDominionCertificationCaseKind.PROVIDER_GATE_INHERITANCE,
            ExternalDominionCertificationCaseKind.READY_FOR_EXECUTION_FALSE,
        ]
    )
    minimum_required_status: ExternalDominionCertificationStatus | str = ExternalDominionCertificationStatus.PASSED
    require_all_blocking_cases_pass: bool = True
    require_no_execution_proof: bool = True
    require_no_network_proof: bool = True
    require_no_credential_proof: bool = True
    require_no_command_proof: bool = True
    require_result_boundary: bool = True
    require_ocel_visibility_plan: bool = True
    require_provider_gate_inheritance: bool = True
    require_ready_for_execution_false: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _require_non_blank("target_id", self.target_id)
        [_normalize_case_kind(kind) for kind in self.required_case_kinds]
        [_normalize_case_kind(kind) for kind in self.blocking_case_kinds]
        _normalize_status(self.minimum_required_status)
        for name in (
            "require_all_blocking_cases_pass",
            "require_no_execution_proof",
            "require_no_network_proof",
            "require_no_credential_proof",
            "require_no_command_proof",
            "require_result_boundary",
            "require_ocel_visibility_plan",
            "require_provider_gate_inheritance",
            "require_ready_for_execution_false",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must default True")

    @property
    def is_certification_result(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCertificationCase:
    case_id: str
    target_id: str
    candidate_id: str | None
    case_kind: ExternalDominionCertificationCaseKind | str
    title: str
    description: str
    severity: ExternalDominionCertificationSeverity | str
    required_evidence_refs: list[str] = field(default_factory=list)
    source_artifact_refs: list[str] = field(default_factory=list)
    blocking: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("case_id", self.case_id)
        _require_non_blank("target_id", self.target_id)
        _normalize_case_kind(self.case_kind)
        _require_non_blank("title", self.title)
        _require_non_blank("description", self.description)
        _normalize_severity(self.severity)
        _validate_string_list("required_evidence_refs", self.required_evidence_refs)
        _validate_string_list("source_artifact_refs", self.source_artifact_refs)

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCertificationCaseResult:
    result_id: str
    case_id: str
    target_id: str
    candidate_id: str | None
    case_kind: ExternalDominionCertificationCaseKind | str
    status: ExternalDominionCertificationStatus | str
    passed: bool
    blocking: bool
    limitations: list[str] = field(default_factory=list)
    failed_reasons: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    reviewer_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("result_id", self.result_id)
        _require_non_blank("case_id", self.case_id)
        _require_non_blank("target_id", self.target_id)
        _normalize_case_kind(self.case_kind)
        status = _normalize_status(self.status)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("failed_reasons", self.failed_reasons)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("reviewer_refs", self.reviewer_refs)
        if self.passed and status not in {
            ExternalDominionCertificationStatus.PASSED,
            ExternalDominionCertificationStatus.PASSED_WITH_LIMITATIONS,
        }:
            raise ValueError("passed=True is only allowed for passed or passed_with_limitations status")
        if status is ExternalDominionCertificationStatus.PASSED_WITH_LIMITATIONS and not self.limitations:
            raise ValueError("passed_with_limitations requires limitations")
        if status in {ExternalDominionCertificationStatus.FAILED, ExternalDominionCertificationStatus.BLOCKED} and not self.failed_reasons:
            raise ValueError("failed or blocked certification results require failed_reasons")

    @property
    def is_production_certification(self) -> bool:
        return False

    @property
    def grants_execution(self) -> bool:
        return False

    @property
    def blocks_matrix_pass(self) -> bool:
        return self.blocking and _normalize_status(self.status) in {
            ExternalDominionCertificationStatus.FAILED,
            ExternalDominionCertificationStatus.BLOCKED,
        }


@dataclass(frozen=True)
class ExternalDominionCertificationMatrix:
    matrix_id: str
    target_id: str
    candidate_id: str | None
    policy_id: str
    cases: list[ExternalDominionCertificationCase]
    results: list[ExternalDominionCertificationCaseResult]
    aggregate_status: ExternalDominionCertificationStatus | str
    aggregate_decision: ExternalDominionCertificationDecision | str
    passed_case_count: int
    failed_case_count: int
    blocked_case_count: int
    limitation_count: int
    unresolved_case_ids: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0308_limited_preview_gate_review: bool = False
    ready_for_execution: bool = False
    production_certified: bool = False
    live_adapter_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("matrix_id", self.matrix_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("policy_id", self.policy_id)
        if not isinstance(self.cases, list):
            raise TypeError("cases must be a list")
        if not isinstance(self.results, list):
            raise TypeError("results must be a list")
        status = _normalize_status(self.aggregate_status)
        decision = _normalize_decision(self.aggregate_decision)
        _validate_string_list("unresolved_case_ids", self.unresolved_case_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.7")
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.30.7")
        if self.live_adapter_certified is not False:
            raise ValueError("live_adapter_certified must always be False in v0.30.7")
        if self.passed_case_count != sum(1 for result in self.results if result.passed):
            raise ValueError("passed_case_count must match case results")
        if self.failed_case_count != sum(
            1 for result in self.results if _normalize_status(result.status) is ExternalDominionCertificationStatus.FAILED
        ):
            raise ValueError("failed_case_count must match failed case results")
        if self.blocked_case_count != sum(
            1 for result in self.results if _normalize_status(result.status) is ExternalDominionCertificationStatus.BLOCKED
        ):
            raise ValueError("blocked_case_count must match blocked case results")
        if self.limitation_count != sum(len(result.limitations) for result in self.results):
            raise ValueError("limitation_count must match result limitations")
        blocking_case_ids = {case.case_id for case in self.cases if case.blocking}
        blocking_failed = any(result.blocks_matrix_pass for result in self.results)
        unresolved_blocking = bool(blocking_case_ids & set(self.unresolved_case_ids))
        review_decisions = {
            ExternalDominionCertificationDecision.PASS_FOR_LIMITED_PREVIEW_GATE_REVIEW,
            ExternalDominionCertificationDecision.PASS_WITH_LIMITATIONS_FOR_LIMITED_PREVIEW_GATE_REVIEW,
        }
        if self.ready_for_v0308_limited_preview_gate_review:
            if decision not in review_decisions:
                raise ValueError("preview gate review readiness requires pass/pass_with_limitations review decision")
            if status not in {
                ExternalDominionCertificationStatus.PASSED,
                ExternalDominionCertificationStatus.PASSED_WITH_LIMITATIONS,
            }:
                raise ValueError("preview gate review readiness requires passed aggregate status")
            if blocking_failed or unresolved_blocking:
                raise ValueError("unresolved or failed blocking cases prevent preview gate review readiness")

    @property
    def grants_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDominionCertificationReport:
    report_id: str
    matrix_id: str
    target_id: str
    candidate_id: str | None
    summary: str
    aggregate_status: ExternalDominionCertificationStatus | str
    aggregate_decision: ExternalDominionCertificationDecision | str
    passed_case_count: int
    failed_case_count: int
    blocked_case_count: int
    limitation_count: int
    limitations: list[str] = field(default_factory=list)
    failed_reasons: list[str] = field(default_factory=list)
    required_followups: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_v0308_limited_preview_gate_review: bool = False
    ready_for_execution: bool = False
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("matrix_id", self.matrix_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("summary", self.summary)
        _normalize_status(self.aggregate_status)
        _normalize_decision(self.aggregate_decision)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("failed_reasons", self.failed_reasons)
        _validate_string_list("required_followups", self.required_followups)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.7")

    @property
    def grants_execution_permission(self) -> bool:
        return False

    @property
    def is_production_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class SpecializedCertificationReport:
    report_id: str
    target_id: str
    candidate_id: str | None
    status: ExternalDominionCertificationStatus | str
    passed: bool
    evidence_refs: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    failed_reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("target_id", self.target_id)
        status = _normalize_status(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("failed_reasons", self.failed_reasons)
        if self.passed and status not in {
            ExternalDominionCertificationStatus.PASSED,
            ExternalDominionCertificationStatus.PASSED_WITH_LIMITATIONS,
        }:
            raise ValueError("passed=True does not imply execution and requires passed status")

    @property
    def grants_runtime_permission(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class DigestionCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class AuthorityCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class DelegationDryRunCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class ApprovalAuditRollbackCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoExecutionCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoNetworkCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoCredentialCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoCommandCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoProviderBypassCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoRPACertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoBrowserCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class NoGatewayCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class OCELVisibilityCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class ResultBoundaryCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class RollbackNoOpCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class ProviderGateInheritanceCertificationReport(SpecializedCertificationReport):
    pass


@dataclass(frozen=True)
class ExternalDominionV0308PreviewGateHandoff:
    handoff_id: str
    target_id: str
    candidate_id: str | None
    certification_matrix_id: str
    certification_report_id: str
    ready_for_v0308_limited_preview_gate_review: bool
    ready_for_limited_preview_execution: bool
    ready_for_execution: bool
    production_certified: bool
    live_adapter_certified: bool
    unresolved_requirements: list[str] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("certification_matrix_id", self.certification_matrix_id)
        _require_non_blank("certification_report_id", self.certification_report_id)
        _validate_string_list("unresolved_requirements", self.unresolved_requirements)
        _validate_string_list("limitations", self.limitations)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.ready_for_limited_preview_execution is not False:
            raise ValueError("ready_for_limited_preview_execution must always be False in v0.30.7")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.7")
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.30.7")
        if self.live_adapter_certified is not False:
            raise ValueError("live_adapter_certified must always be False in v0.30.7")

    @property
    def executes_preview(self) -> bool:
        return False

    @property
    def is_production_certification(self) -> bool:
        return False


def build_default_certification_policy(
    target_id: str,
    candidate_id: str | None = None,
) -> ExternalDominionCertificationPolicy:
    _require_non_blank("target_id", target_id)
    return ExternalDominionCertificationPolicy(
        policy_id=f"external_dominion_certification_policy:{candidate_id or target_id}",
        target_id=target_id,
        candidate_id=candidate_id,
        metadata={"v0307_contract_only": True},
    )


def build_certification_cases_from_policy(
    policy: ExternalDominionCertificationPolicy,
) -> list[ExternalDominionCertificationCase]:
    blocking_kinds = {_normalize_case_kind(kind) for kind in policy.blocking_case_kinds}
    cases: list[ExternalDominionCertificationCase] = []
    for kind_value in policy.required_case_kinds:
        kind = _normalize_case_kind(kind_value)
        cases.append(
            ExternalDominionCertificationCase(
                case_id=f"external_dominion_certification_case:{policy.policy_id}:{kind.value}",
                target_id=policy.target_id,
                candidate_id=policy.candidate_id,
                case_kind=kind,
                title=f"{kind.value} certification case",
                description=f"Verify {kind.value} using contract artifacts only.",
                severity=ExternalDominionCertificationSeverity.CRITICAL
                if kind in blocking_kinds
                else ExternalDominionCertificationSeverity.MEDIUM,
                required_evidence_refs=[],
                source_artifact_refs=[],
                blocking=kind in blocking_kinds,
                metadata={"v0307_contract_only": True},
            )
        )
    return cases


def evaluate_certification_case(
    case: ExternalDominionCertificationCase,
    source_artifacts: dict[str, Any] | None = None,
    evidence_refs: list[str] | None = None,
) -> ExternalDominionCertificationCaseResult:
    artifacts = dict(source_artifacts or {})
    evidence = list(evidence_refs or case.required_evidence_refs)
    kind = _normalize_case_kind(case.case_kind)
    missing_required = False
    if kind is ExternalDominionCertificationCaseKind.RESULT_BOUNDARY:
        missing_required = not bool(artifacts.get("result_boundary_policy"))
    elif kind is ExternalDominionCertificationCaseKind.PROVIDER_GATE_INHERITANCE:
        missing_required = not bool(artifacts.get("provider_gate_inheritance", True))
    elif kind is ExternalDominionCertificationCaseKind.OCEL_VISIBILITY:
        missing_required = not bool(artifacts.get("ocel_visibility_plan", True))
    elif kind is ExternalDominionCertificationCaseKind.ROLLBACK_NO_OP:
        missing_required = not bool(artifacts.get("rollback_plan") or artifacts.get("no_op_boundary") or artifacts.get("rollback_or_no_op", True))
    elif kind is ExternalDominionCertificationCaseKind.READY_FOR_EXECUTION_FALSE:
        missing_required = bool(artifacts.get("ready_for_execution", False))
    elif kind in NO_RUNTIME_CASE_KINDS:
        missing_required = bool(artifacts.get(kind.value, False))
    if missing_required:
        status = ExternalDominionCertificationStatus.FAILED
        return ExternalDominionCertificationCaseResult(
            result_id=f"external_dominion_certification_case_result:{case.case_id}",
            case_id=case.case_id,
            target_id=case.target_id,
            candidate_id=case.candidate_id,
            case_kind=kind,
            status=status,
            passed=False,
            blocking=case.blocking,
            failed_reasons=[f"{kind.value} contract evidence is missing or violated"],
            evidence_refs=evidence,
            metadata={"v0307_contract_only": True},
        )
    return ExternalDominionCertificationCaseResult(
        result_id=f"external_dominion_certification_case_result:{case.case_id}",
        case_id=case.case_id,
        target_id=case.target_id,
        candidate_id=case.candidate_id,
        case_kind=kind,
        status=ExternalDominionCertificationStatus.PASSED,
        passed=True,
        blocking=case.blocking,
        evidence_refs=evidence,
        metadata={"v0307_contract_only": True},
    )


def build_certification_matrix(
    policy: ExternalDominionCertificationPolicy,
    cases: list[ExternalDominionCertificationCase],
    results: list[ExternalDominionCertificationCaseResult],
) -> ExternalDominionCertificationMatrix:
    result_case_ids = {result.case_id for result in results}
    unresolved = [case.case_id for case in cases if case.case_id not in result_case_ids]
    failed_count = sum(
        1 for result in results if _normalize_status(result.status) is ExternalDominionCertificationStatus.FAILED
    )
    blocked_count = sum(
        1 for result in results if _normalize_status(result.status) is ExternalDominionCertificationStatus.BLOCKED
    )
    limitation_count = sum(len(result.limitations) for result in results)
    blocking_failure = any(result.blocks_matrix_pass for result in results)
    unresolved_blocking = any(case.blocking and case.case_id in unresolved for case in cases)
    if blocked_count:
        aggregate_status = ExternalDominionCertificationStatus.BLOCKED
        decision = ExternalDominionCertificationDecision.BLOCK
    elif failed_count or blocking_failure:
        aggregate_status = ExternalDominionCertificationStatus.FAILED
        decision = ExternalDominionCertificationDecision.FAIL
    elif unresolved_blocking:
        aggregate_status = ExternalDominionCertificationStatus.IN_REVIEW
        decision = ExternalDominionCertificationDecision.REQUIRE_MORE_EVIDENCE
    elif limitation_count:
        aggregate_status = ExternalDominionCertificationStatus.PASSED_WITH_LIMITATIONS
        decision = ExternalDominionCertificationDecision.PASS_WITH_LIMITATIONS_FOR_LIMITED_PREVIEW_GATE_REVIEW
    else:
        aggregate_status = ExternalDominionCertificationStatus.PASSED
        decision = ExternalDominionCertificationDecision.PASS_FOR_LIMITED_PREVIEW_GATE_REVIEW
    ready = decision in {
        ExternalDominionCertificationDecision.PASS_FOR_LIMITED_PREVIEW_GATE_REVIEW,
        ExternalDominionCertificationDecision.PASS_WITH_LIMITATIONS_FOR_LIMITED_PREVIEW_GATE_REVIEW,
    } and not unresolved_blocking
    return ExternalDominionCertificationMatrix(
        matrix_id=f"external_dominion_certification_matrix:{policy.policy_id}",
        target_id=policy.target_id,
        candidate_id=policy.candidate_id,
        policy_id=policy.policy_id,
        cases=cases,
        results=results,
        aggregate_status=aggregate_status,
        aggregate_decision=decision,
        passed_case_count=sum(1 for result in results if result.passed),
        failed_case_count=failed_count,
        blocked_case_count=blocked_count,
        limitation_count=limitation_count,
        unresolved_case_ids=unresolved,
        evidence_refs=[ref for result in results for ref in result.evidence_refs],
        ready_for_v0308_limited_preview_gate_review=ready,
        ready_for_execution=False,
        production_certified=False,
        live_adapter_certified=False,
        metadata={"v0307_contract_only": True},
    )


def build_certification_report(
    matrix: ExternalDominionCertificationMatrix,
) -> ExternalDominionCertificationReport:
    limitations = [limitation for result in matrix.results for limitation in result.limitations]
    failed_reasons = [reason for result in matrix.results for reason in result.failed_reasons]
    followups: list[str] = []
    if matrix.unresolved_case_ids:
        followups.append("resolve certification case evidence gaps")
    if failed_reasons:
        followups.append("repair failed certification boundaries")
    return ExternalDominionCertificationReport(
        report_id=f"external_dominion_certification_report:{matrix.matrix_id}",
        matrix_id=matrix.matrix_id,
        target_id=matrix.target_id,
        candidate_id=matrix.candidate_id,
        summary="External Dominion certification matrix report for v0.30.8 gate review only.",
        aggregate_status=matrix.aggregate_status,
        aggregate_decision=matrix.aggregate_decision,
        passed_case_count=matrix.passed_case_count,
        failed_case_count=matrix.failed_case_count,
        blocked_case_count=matrix.blocked_case_count,
        limitation_count=matrix.limitation_count,
        limitations=limitations,
        failed_reasons=failed_reasons,
        required_followups=followups,
        evidence_refs=list(matrix.evidence_refs),
        ready_for_v0308_limited_preview_gate_review=matrix.ready_for_v0308_limited_preview_gate_review,
        ready_for_execution=False,
        withdrawal_conditions=[
            "certification report is treated as execution approval",
            "ready_for_execution, production_certified, or live_adapter_certified becomes true",
        ],
        metadata={"v0307_contract_only": True},
    )


def _build_specialized_report(
    cls: type[SpecializedCertificationReport],
    report_id: str,
    target_id: str,
    candidate_id: str | None,
    evidence_refs: list[str] | None,
) -> SpecializedCertificationReport:
    return cls(
        report_id=report_id,
        target_id=target_id,
        candidate_id=candidate_id,
        status=ExternalDominionCertificationStatus.PASSED,
        passed=True,
        evidence_refs=list(evidence_refs or []),
        limitations=[],
        failed_reasons=[],
        metadata={"contract_artifact_check_only": True, "v0307_contract_only": True},
    )


def build_no_execution_certification_report(
    target_id: str,
    candidate_id: str | None = None,
    evidence_refs: list[str] | None = None,
) -> NoExecutionCertificationReport:
    return _build_specialized_report(
        NoExecutionCertificationReport,
        f"no_execution_certification_report:{candidate_id or target_id}",
        target_id,
        candidate_id,
        evidence_refs,
    )


def build_no_network_certification_report(
    target_id: str,
    candidate_id: str | None = None,
    evidence_refs: list[str] | None = None,
) -> NoNetworkCertificationReport:
    return _build_specialized_report(
        NoNetworkCertificationReport,
        f"no_network_certification_report:{candidate_id or target_id}",
        target_id,
        candidate_id,
        evidence_refs,
    )


def build_no_credential_certification_report(
    target_id: str,
    candidate_id: str | None = None,
    evidence_refs: list[str] | None = None,
) -> NoCredentialCertificationReport:
    return _build_specialized_report(
        NoCredentialCertificationReport,
        f"no_credential_certification_report:{candidate_id or target_id}",
        target_id,
        candidate_id,
        evidence_refs,
    )


def build_no_command_certification_report(
    target_id: str,
    candidate_id: str | None = None,
    evidence_refs: list[str] | None = None,
) -> NoCommandCertificationReport:
    return _build_specialized_report(
        NoCommandCertificationReport,
        f"no_command_certification_report:{candidate_id or target_id}",
        target_id,
        candidate_id,
        evidence_refs,
    )


def build_result_boundary_certification_report(
    target_id: str,
    candidate_id: str | None = None,
    evidence_refs: list[str] | None = None,
) -> ResultBoundaryCertificationReport:
    return _build_specialized_report(
        ResultBoundaryCertificationReport,
        f"result_boundary_certification_report:{candidate_id or target_id}",
        target_id,
        candidate_id,
        evidence_refs,
    )


def build_provider_gate_inheritance_certification_report(
    target_id: str,
    candidate_id: str | None = None,
    evidence_refs: list[str] | None = None,
) -> ProviderGateInheritanceCertificationReport:
    return _build_specialized_report(
        ProviderGateInheritanceCertificationReport,
        f"provider_gate_inheritance_certification_report:{candidate_id or target_id}",
        target_id,
        candidate_id,
        evidence_refs,
    )


def certification_matrix_preserves_no_execution(matrix: ExternalDominionCertificationMatrix) -> bool:
    return (
        matrix.ready_for_execution is False
        and matrix.production_certified is False
        and matrix.live_adapter_certified is False
        and matrix.grants_execution is False
    )


def certification_matrix_preserves_v0307_boundaries(matrix: ExternalDominionCertificationMatrix) -> bool:
    return certification_matrix_preserves_no_execution(matrix) and all(
        result.grants_execution is False and result.is_production_certification is False for result in matrix.results
    )


def certification_report_allows_v0308_gate_review_only(report: ExternalDominionCertificationReport) -> bool:
    return report.ready_for_execution is False and report.grants_execution_permission is False


def build_v0308_preview_gate_handoff(
    matrix: ExternalDominionCertificationMatrix,
    report: ExternalDominionCertificationReport,
) -> ExternalDominionV0308PreviewGateHandoff:
    if report.matrix_id != matrix.matrix_id:
        raise ValueError("certification report matrix_id must match matrix")
    return ExternalDominionV0308PreviewGateHandoff(
        handoff_id=f"external_dominion_v0308_preview_gate_handoff:{matrix.matrix_id}",
        target_id=matrix.target_id,
        candidate_id=matrix.candidate_id,
        certification_matrix_id=matrix.matrix_id,
        certification_report_id=report.report_id,
        ready_for_v0308_limited_preview_gate_review=matrix.ready_for_v0308_limited_preview_gate_review
        and report.ready_for_v0308_limited_preview_gate_review,
        ready_for_limited_preview_execution=False,
        ready_for_execution=False,
        production_certified=False,
        live_adapter_certified=False,
        unresolved_requirements=list(matrix.unresolved_case_ids + report.required_followups),
        limitations=list(report.limitations),
        evidence_refs=list(report.evidence_refs),
        withdrawal_conditions=[
            "preview gate review handoff is treated as preview execution",
            "ready_for_limited_preview_execution or ready_for_execution becomes true",
        ],
        metadata={"v0307_contract_only": True},
    )
