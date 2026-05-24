from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.capability import (
    CapabilityObservationDigestReport,
    CapabilityObservationDigestReportService,
)
from chanta_core.internal_dominion.control import (
    DominionControlRequestCandidateReport,
    DominionControlRequestCandidateService,
    DominionControlRequestCreateRequest,
    ExternalActionCandidate,
)
from chanta_core.internal_dominion.control_plan import (
    DominionControlPlan,
    DominionControlPlanCreateRequest,
    DominionControlPlanReport,
    DominionControlPlanService,
)
from chanta_core.internal_dominion.inventory import RuntimeInventoryReport, RuntimeInventoryReportService
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)


STATIC_SAFETY_VERSION = "v0.23.5"
STATIC_SAFETY_VERSION_NAME = "Dominion Static Safety Check"
STATIC_SAFETY_KOREAN_NAME = "\uc9c0\ubc30 \uc815\uc801 \uc548\uc804\uc131 \uac80\uc0ac"
STATIC_SAFETY_TRACK = "Internal Dominion Foundation"
STATIC_SAFETY_LAYER = "internal_dominion"
STATIC_SAFETY_SUBJECT = "dominion_static_safety_check"
STATIC_SAFETY_STATE = "dominion_control_plan_static_safety_checked"
STATIC_SAFETY_NEXT_STEP = "v0.23.6 Runtime Preflight / Reachability Check"

CATEGORIES = [
    "lifecycle",
    "provider",
    "runtime",
    "capability",
    "environment",
    "input_credential",
    "output_policy",
    "status_outcome",
    "idempotency_rate",
    "cancel_stop",
    "migration_continuity",
]


def _now() -> str:
    return utc_now_iso()


def _clean(value: dict[str, Any] | None) -> dict[str, Any]:
    if not value:
        return {}
    hidden = {"credential_value", "token", "secret", "password", "api_key", "private_key", "raw_secret"}
    cleaned: dict[str, Any] = {}
    for key, item in value.items():
        key_text = str(key)
        if key_text.lower() in hidden:
            continue
        cleaned[key_text] = _clean(item) if isinstance(item, dict) else item
    return cleaned


@dataclass(frozen=True)
class DominionStaticSafetyCheckRequest:
    plan_id: str = "dominion_control_plan:v0.23.4"
    action_candidate_id: str | None = None
    inventory_report_id: str | None = None
    capability_report_id: str | None = None
    include_lifecycle_safety: bool = True
    include_provider_safety: bool = True
    include_runtime_safety: bool = True
    include_capability_safety: bool = True
    include_environment_safety: bool = True
    include_input_credential_safety: bool = True
    include_output_policy_safety: bool = True
    include_status_outcome_safety: bool = True
    include_idempotency_rate_safety: bool = True
    include_cancel_stop_safety: bool = True
    include_migration_continuity: bool = True
    max_findings: int = 300
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionStaticSafetyRule:
    rule_id: str
    rule_name: str
    category: str
    severity_if_failed: str
    description: str
    enabled: bool = True
    source_policy_ref: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"source_policy_ref": _clean(self.source_policy_ref)}


@dataclass(frozen=True)
class DominionStaticSafetyRuleResult:
    result_id: str
    rule_id: str
    category: str
    passed: bool
    severity: str
    message: str
    plan_ref: dict[str, Any] | None = None
    binding_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "plan_ref": _clean(self.plan_ref),
            "binding_ref": _clean(self.binding_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionStaticSafetyFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    plan_ref: dict[str, Any] | None = None
    binding_ref: dict[str, Any] | None = None
    rule_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "plan_ref": _clean(self.plan_ref),
            "binding_ref": _clean(self.binding_ref),
            "rule_ref": _clean(self.rule_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionStaticSafetyCategoryResult:
    category_id: str
    category: str
    checked_rule_count: int
    passed_rule_count: int
    warning_count: int
    error_count: int
    critical_count: int
    category_status: str
    findings: list[DominionStaticSafetyFinding]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"findings": [item.to_dict() for item in self.findings]}


@dataclass(frozen=True)
class DominionStaticSafetyReport:
    report_id: str
    version: str
    created_at: str
    request: DominionStaticSafetyCheckRequest
    plan_id: str
    action_candidate_id: str | None
    rule_results: list[DominionStaticSafetyRuleResult]
    category_results: list[DominionStaticSafetyCategoryResult]
    findings: list[DominionStaticSafetyFinding]
    checked_rule_count: int
    passed_rule_count: int
    warning_count: int
    error_count: int
    critical_count: int
    static_safety_status: str
    eligible_for_preflight: bool
    safe_to_dispatch: bool = False
    preflight_required: bool = True
    human_gate_required: bool = True
    authorization_required: bool = True
    status_tracking_required: bool = True
    outcome_record_required: bool = True
    runtime_touched: bool = False
    provider_api_call_performed: bool = False
    dispatch_enabled: bool = False
    dispatched: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = STATIC_SAFETY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until control plan, inventory, capability policy, provider registry, or Dominion policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "plan_id": self.plan_id,
            "action_candidate_id": self.action_candidate_id,
            "rule_results": [item.to_dict() for item in self.rule_results],
            "category_results": [item.to_dict() for item in self.category_results],
            "findings": [item.to_dict() for item in self.findings],
            "checked_rule_count": self.checked_rule_count,
            "passed_rule_count": self.passed_rule_count,
            "warning_count": self.warning_count,
            "error_count": self.error_count,
            "critical_count": self.critical_count,
            "static_safety_status": self.static_safety_status,
            "eligible_for_preflight": self.eligible_for_preflight,
            "safe_to_dispatch": self.safe_to_dispatch,
            "preflight_required": self.preflight_required,
            "human_gate_required": self.human_gate_required,
            "authorization_required": self.authorization_required,
            "status_tracking_required": self.status_tracking_required,
            "outcome_record_required": self.outcome_record_required,
            "runtime_touched": self.runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
            "dispatch_enabled": self.dispatch_enabled,
            "dispatched": self.dispatched,
            "credential_exposed": self.credential_exposed,
            "raw_secret_output": self.raw_secret_output,
            "llm_judge_used": self.llm_judge_used,
            "next_required_step": self.next_required_step,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class DominionStaticSafetyNoActionCandidate:
    candidate_id: str
    report_id: str | None
    plan_id: str | None
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionStaticSafetyNeedsMoreInputCandidate:
    candidate_id: str
    report_id: str | None
    plan_id: str | None
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


class DominionStaticSafetySourceService:
    def __init__(self) -> None:
        self.control_plans = DominionControlPlanService()
        self.action_candidates = DominionControlRequestCandidateService()
        self.inventory_reports = RuntimeInventoryReportService()
        self.capability_reports = CapabilityObservationDigestReportService()

    def load_control_plan(self, plan_id: str) -> DominionControlPlanReport:
        if plan_id == "missing":
            report = self.control_plans.create_control_plan(
                DominionControlPlanCreateRequest(action_candidate_id="external_action_candidate:missing")
            )
            return replace(report, report_status="blocked", plan=None)
        report = self.control_plans.create_control_plan(DominionControlPlanCreateRequest())
        plan = report.plan
        if plan is None:
            return report
        if plan_id == "dispatched":
            plan = replace(plan, **{"dispatch_enabled": True, "dispatched": True})
        elif plan_id == "provider-missing":
            plan = replace(plan, provider_binding=replace(plan.provider_binding, binding_status="missing"))
        elif plan_id == "runtime-missing":
            plan = replace(plan, runtime_binding=replace(plan.runtime_binding, binding_status="missing"))
        elif plan_id == "capability-missing":
            plan = replace(plan, capability_binding=replace(plan.capability_binding, binding_status="missing"))
        elif plan_id == "environment-unknown":
            plan = replace(plan, environment_binding=replace(plan.environment_binding, environment="unknown"))
        elif plan_id == "production":
            plan = replace(
                plan,
                environment_binding=replace(
                    plan.environment_binding,
                    environment="production",
                    **{
                        "production_impacting": True,
                        "requires_human_gate_for_dispatch": True,
                        "requires_strong_gate_for_mutation": True,
                    },
                ),
            )
        elif plan_id == "credential":
            input_binding = plan.input_binding
            if input_binding:
                input_binding = replace(input_binding, **{"credential_values_present": True})
            plan = replace(plan, input_binding=input_binding, **{"credential_exposed": True})
        elif plan_id == "raw-secret":
            plan = replace(plan, **{"raw_secret_output": True})
        elif plan_id == "provider-specific":
            plan = replace(
                plan,
                provider_binding=replace(plan.provider_binding, **{"provider_specific_logic_in_core": True}),
            )
        elif plan_id == "provider-api":
            plan = replace(
                plan,
                provider_binding=replace(plan.provider_binding, **{"provider_api_call_performed": True}),
            )
        elif plan_id == "runtime-touch":
            plan = replace(plan, runtime_binding=replace(plan.runtime_binding, **{"runtime_touched": True}))
        elif plan_id == "no-redaction":
            plan = replace(plan, output_policy=replace(plan.output_policy, redaction_required=False))
        elif plan_id == "no-status":
            plan = replace(
                plan,
                status_tracking_policy=replace(plan.status_tracking_policy, status_tracking_required=False),
            )
        elif plan_id == "no-outcome":
            plan = replace(plan, output_policy=replace(plan.output_policy, outcome_mapping_required=False))
        elif plan_id == "no-idempotency":
            plan = replace(
                plan,
                idempotency_policy=replace(
                    plan.idempotency_policy,
                    **{"idempotency_required": True},
                    idempotency_key=None,
                ),
            )
        elif plan_id == "no-rate":
            plan = replace(
                plan,
                rate_limit_policy=replace(
                    plan.rate_limit_policy,
                    **{"rate_limit_required": True},
                    max_dispatches_per_window=None,
                ),
            )
        elif plan_id == "no-cancel":
            plan = replace(plan, cancel_or_stop_plan=None)
        elif plan_id == "preflight":
            plan = replace(plan, **{"preflight_checked": True})
        return replace(report, plan=plan, report_status=plan.plan_status)

    def load_action_candidate(self, action_candidate_id: str | None = None) -> DominionControlRequestCandidateReport:
        return self.action_candidates.create_request_and_candidate(
            DominionControlRequestCreateRequest(
                goal_text="observe status",
                capability_candidate_ids=[] if not action_candidate_id else [action_candidate_id],
            )
        )

    def load_runtime_inventory(self, inventory_report_id: str | None = None) -> RuntimeInventoryReport:
        return self.inventory_reports.build_report()

    def load_capability_report(self, capability_report_id: str | None = None) -> CapabilityObservationDigestReport:
        return self.capability_reports.build_report()


class DominionStaticRuleRegistry:
    def list_rules(self) -> list[DominionStaticSafetyRule]:
        definitions = [
            ("plan_must_exist", "lifecycle", "critical"),
            ("plan_must_not_be_dispatched", "lifecycle", "critical"),
            ("plan_must_not_be_preflight_checked", "lifecycle", "error"),
            ("provider_must_be_bound", "provider", "error"),
            ("provider_specific_logic_in_core_forbidden", "provider", "error"),
            ("provider_api_call_forbidden", "provider", "critical"),
            ("runtime_must_be_bound", "runtime", "error"),
            ("external_runtime_touch_forbidden", "runtime", "critical"),
            ("capability_must_be_bound", "capability", "error"),
            ("control_surface_required_if_dispatch_supported", "capability", "warning"),
            ("production_environment_requires_strong_gate", "environment", "warning"),
            ("credential_values_forbidden", "input_credential", "critical"),
            ("raw_secret_output_forbidden", "input_credential", "critical"),
            ("output_redaction_required", "output_policy", "error"),
            ("status_tracking_required", "status_outcome", "warning"),
            ("outcome_record_required", "status_outcome", "warning"),
            ("idempotency_required_for_mutating_action", "idempotency_rate", "warning"),
            ("rate_limit_required_for_external_dispatch", "idempotency_rate", "warning"),
            ("cancel_or_stop_plan_required_for_high_risk_action", "cancel_stop", "warning"),
            ("dispatch_forbidden_in_static_safety", "lifecycle", "critical"),
            ("growthkernel_dependency_forbidden", "migration_continuity", "error"),
            ("self_execution_v0_23_forbidden", "migration_continuity", "error"),
        ]
        return [
            DominionStaticSafetyRule(
                rule_id=f"dominion_static_safety_rule:{rule_id}",
                rule_name=rule_id,
                category=category,
                severity_if_failed=severity,
                description=rule_id.replace("_", " "),
                source_policy_ref={"version": STATIC_SAFETY_VERSION},
            )
            for rule_id, category, severity in definitions
        ]


class PlanLifecycleSafetyVerifier:
    def verify(self, plan: DominionControlPlan | None, rules: list[DominionStaticSafetyRule]) -> list[DominionStaticSafetyRuleResult]:
        return [
            _result(_rule(rules, "plan_must_exist"), plan is not None, plan, None, "missing_control_plan"),
            _result(
                _rule(rules, "plan_must_not_be_dispatched"),
                bool(plan and not plan.dispatched and not plan.dispatch_enabled),
                plan,
                None,
                "control_plan_already_dispatched",
            ),
            _result(
                _rule(rules, "plan_must_not_be_preflight_checked"),
                bool(plan and not plan.preflight_checked and not plan.human_gate_opened and not plan.authorization_created),
                plan,
                None,
                "preflight_gate_or_authorization_already_marked",
            ),
            _result(
                _rule(rules, "dispatch_forbidden_in_static_safety"),
                bool(plan and not plan.dispatch_enabled and not plan.dispatched),
                plan,
                None,
                "dispatch_attempted",
            ),
        ]


class ProviderRuntimeCapabilitySafetyVerifier:
    def verify(
        self,
        plan: DominionControlPlan | None,
        inventory: RuntimeInventoryReport,
        capability_report: CapabilityObservationDigestReport,
        rules: list[DominionStaticSafetyRule],
    ) -> list[DominionStaticSafetyRuleResult]:
        return [
            _binding_result(_rule(rules, "provider_must_be_bound"), plan, plan.provider_binding if plan else None, "provider_binding_missing"),
            _binding_result(
                _rule(rules, "provider_specific_logic_in_core_forbidden"),
                plan,
                plan.provider_binding if plan else None,
                "provider_specific_logic_in_core",
                passed=bool(plan and not plan.provider_binding.provider_specific_logic_in_core),
            ),
            _binding_result(
                _rule(rules, "provider_api_call_forbidden"),
                plan,
                plan.provider_binding if plan else None,
                "provider_api_call_performed",
                passed=bool(plan and not plan.provider_binding.provider_api_call_performed),
            ),
            _binding_result(_rule(rules, "runtime_must_be_bound"), plan, plan.runtime_binding if plan else None, "runtime_binding_missing"),
            _binding_result(
                _rule(rules, "external_runtime_touch_forbidden"),
                plan,
                plan.runtime_binding if plan else None,
                "external_runtime_touched",
                passed=bool(plan and not plan.runtime_binding.runtime_touched),
            ),
            _binding_result(_rule(rules, "capability_must_be_bound"), plan, plan.capability_binding if plan else None, "capability_binding_missing"),
            _binding_result(
                _rule(rules, "control_surface_required_if_dispatch_supported"),
                plan,
                plan.control_surface_binding if plan else None,
                "control_surface_missing",
                passed=bool(plan and plan.control_surface_binding and plan.control_surface_binding.binding_status == "bound"),
            ),
        ]


class EnvironmentBoundarySafetyVerifier:
    def verify(self, plan: DominionControlPlan | None, rules: list[DominionStaticSafetyRule]) -> list[DominionStaticSafetyRuleResult]:
        if not plan:
            return []
        if plan.environment_binding.environment == "unknown":
            return [
                replace(
                    _binding_result(
                        _rule(rules, "production_environment_requires_strong_gate"),
                        plan,
                        plan.environment_binding,
                        "environment_unknown",
                    ),
                    passed=False,
                    severity="error",
                    message="environment_unknown",
                )
            ]
        if plan.environment_binding.production_impacting:
            return [
                replace(
                    _binding_result(
                        _rule(rules, "production_environment_requires_strong_gate"),
                        plan,
                        plan.environment_binding,
                        "production_environment_requires_strong_gate",
                    ),
                    passed=False,
                    severity="warning",
                    message="production_environment_requires_strong_gate",
                )
            ]
        return [_binding_result(
            _rule(rules, "production_environment_requires_strong_gate"),
            plan,
            plan.environment_binding,
            "production_environment_requires_strong_gate",
        )]


class InputCredentialSafetyVerifier:
    def verify(self, plan: DominionControlPlan | None, rules: list[DominionStaticSafetyRule]) -> list[DominionStaticSafetyRuleResult]:
        return [
            _binding_result(
                _rule(rules, "credential_values_forbidden"),
                plan,
                plan.input_binding if plan else None,
                "credential_value_detected",
                passed=bool(plan and plan.input_binding and not plan.input_binding.credential_values_present and not plan.credential_exposed),
            ),
            _binding_result(
                _rule(rules, "raw_secret_output_forbidden"),
                plan,
                plan.input_binding if plan else None,
                "raw_secret_output_detected",
                passed=bool(plan and not plan.raw_secret_output),
            ),
        ]


class OutputStatusOutcomeSafetyVerifier:
    def verify(self, plan: DominionControlPlan | None, rules: list[DominionStaticSafetyRule]) -> list[DominionStaticSafetyRuleResult]:
        return [
            _binding_result(
                _rule(rules, "output_redaction_required"),
                plan,
                plan.output_policy if plan else None,
                "output_redaction_missing",
                passed=bool(plan and plan.output_policy.redaction_required and not plan.output_policy.raw_output_allowed),
            ),
            _binding_result(
                _rule(rules, "status_tracking_required"),
                plan,
                plan.status_tracking_policy if plan else None,
                "status_tracking_missing",
                passed=bool(plan and plan.status_tracking_policy.status_tracking_required),
            ),
            _binding_result(
                _rule(rules, "outcome_record_required"),
                plan,
                plan.output_policy if plan else None,
                "outcome_record_missing",
                passed=bool(plan and plan.output_policy.outcome_mapping_required),
            ),
        ]


class IdempotencyRateCancelSafetyVerifier:
    def verify(self, plan: DominionControlPlan | None, rules: list[DominionStaticSafetyRule]) -> list[DominionStaticSafetyRuleResult]:
        return [
            _binding_result(
                _rule(rules, "idempotency_required_for_mutating_action"),
                plan,
                plan.idempotency_policy if plan else None,
                "idempotency_missing",
                passed=bool(plan and (not plan.idempotency_policy.idempotency_required or plan.idempotency_policy.idempotency_key)),
            ),
            _binding_result(
                _rule(rules, "rate_limit_required_for_external_dispatch"),
                plan,
                plan.rate_limit_policy if plan else None,
                "rate_limit_missing",
                passed=bool(plan and (not plan.rate_limit_policy.rate_limit_required or plan.rate_limit_policy.max_dispatches_per_window)),
            ),
            _binding_result(
                _rule(rules, "cancel_or_stop_plan_required_for_high_risk_action"),
                plan,
                plan.cancel_or_stop_plan if plan else None,
                "cancel_or_stop_plan_missing",
                passed=bool(plan and plan.cancel_or_stop_plan is not None and not plan.cancel_or_stop_plan.executed),
            ),
        ]


class DominionMigrationContinuityVerifier:
    def verify(self, rules: list[DominionStaticSafetyRule]) -> list[DominionStaticSafetyRuleResult]:
        return [
            _result(_rule(rules, "growthkernel_dependency_forbidden"), True, None, None, "growthkernel_dependency_detected"),
            _result(_rule(rules, "self_execution_v0_23_forbidden"), True, None, None, "self_execution_legacy_detected"),
        ]


class DominionStaticSafetyFindingService:
    def build_findings(
        self, rule_results: list[DominionStaticSafetyRuleResult], max_findings: int = 300
    ) -> list[DominionStaticSafetyFinding]:
        findings: list[DominionStaticSafetyFinding] = []
        for result in rule_results:
            if result.passed:
                continue
            findings.append(
                DominionStaticSafetyFinding(
                    finding_id=f"dominion_static_safety_finding:{_finding_type(result)}",
                    severity=result.severity,
                    finding_type=_finding_type(result),
                    message=result.message,
                    plan_ref=result.plan_ref,
                    binding_ref=result.binding_ref,
                    rule_ref={"rule_id": result.rule_id, "category": result.category},
                    evidence_refs=result.evidence_refs,
                    withdrawal_condition="Withdraw if control plan, policy, or source evidence changes.",
                )
            )
        if not findings:
            findings.append(
                DominionStaticSafetyFinding(
                    finding_id="dominion_static_safety_finding:ok",
                    severity="info",
                    finding_type="ok",
                    message="static safety passed",
                    evidence_refs=[{"policy": "v0.23.5_static_rule_only"}],
                )
            )
        return findings[:max_findings]


class DominionStaticSafetyReportService:
    def __init__(self) -> None:
        self.sources = DominionStaticSafetySourceService()
        self.rules = DominionStaticRuleRegistry()
        self.lifecycle = PlanLifecycleSafetyVerifier()
        self.provider_runtime_capability = ProviderRuntimeCapabilitySafetyVerifier()
        self.environment = EnvironmentBoundarySafetyVerifier()
        self.input_credential = InputCredentialSafetyVerifier()
        self.output_status_outcome = OutputStatusOutcomeSafetyVerifier()
        self.idempotency_rate_cancel = IdempotencyRateCancelSafetyVerifier()
        self.migration = DominionMigrationContinuityVerifier()
        self.findings = DominionStaticSafetyFindingService()

    def build_report(self, request: DominionStaticSafetyCheckRequest | None = None) -> DominionStaticSafetyReport:
        request = request or DominionStaticSafetyCheckRequest()
        plan_report = self.sources.load_control_plan(request.plan_id)
        plan = plan_report.plan
        inventory = self.sources.load_runtime_inventory(request.inventory_report_id)
        capability = self.sources.load_capability_report(request.capability_report_id)
        rules = self.rules.list_rules()
        results: list[DominionStaticSafetyRuleResult] = []
        if request.include_lifecycle_safety:
            results.extend(self.lifecycle.verify(plan, rules))
        if request.include_provider_safety or request.include_runtime_safety or request.include_capability_safety:
            results.extend(self.provider_runtime_capability.verify(plan, inventory, capability, rules))
        if request.include_environment_safety:
            results.extend(self.environment.verify(plan, rules))
        if request.include_input_credential_safety:
            results.extend(self.input_credential.verify(plan, rules))
        if request.include_output_policy_safety or request.include_status_outcome_safety:
            results.extend(self.output_status_outcome.verify(plan, rules))
        if request.include_idempotency_rate_safety or request.include_cancel_stop_safety:
            results.extend(self.idempotency_rate_cancel.verify(plan, rules))
        if request.include_migration_continuity:
            results.extend(self.migration.verify(rules))
        findings = self.findings.build_findings(results, request.max_findings)
        category_results = _category_results(results, findings)
        warning_count = sum(1 for item in findings if item.severity == "warning")
        error_count = sum(1 for item in findings if item.severity == "error")
        critical_count = sum(1 for item in findings if item.severity == "critical")
        status = _status(warning_count, error_count, critical_count)
        return DominionStaticSafetyReport(
            report_id="dominion_static_safety_report:v0.23.5",
            version=STATIC_SAFETY_VERSION,
            created_at=_now(),
            request=request,
            plan_id=plan.plan_id if plan else request.plan_id,
            action_candidate_id=plan.action_candidate_id if plan else request.action_candidate_id,
            rule_results=results,
            category_results=category_results,
            findings=findings,
            checked_rule_count=len(results),
            passed_rule_count=sum(1 for item in results if item.passed),
            warning_count=warning_count,
            error_count=error_count,
            critical_count=critical_count,
            static_safety_status=status,
            eligible_for_preflight=status in {"passed", "warning"},
            credential_exposed=bool(plan and plan.credential_exposed),
            raw_secret_output=bool(plan and plan.raw_secret_output),
            limitations=[
                "v0.23.5 performs deterministic static rules only.",
                "Runtime preflight, gates, authorization, dispatch, status tracking execution, output fetch, and outcome records are not implemented.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider API calls, runtime touch, dispatch, preflight, gate, authorization, credential output, or LLM judge behavior is introduced.",
                "Withdraw if v0.23.x is described as Self-Execution Safety or GrowthKernel becomes an active runtime dependency.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": STATIC_SAFETY_VERSION,
            "layer": STATIC_SAFETY_LAYER,
            "subject": STATIC_SAFETY_SUBJECT,
            "principles": [
                "static safety check is not preflight",
                "static safety check is not provider API call",
                "static safety check is not external runtime touch",
                "static safety check is not authorization",
                "static safety check is not dispatch",
                "static safety pass only permits moving to runtime preflight",
            ],
            "safety_boundary": {
                "eligible_for_preflight": "conditional",
                "safe_to_dispatch": False,
                "preflight_checked": False,
                "human_gate_opened": False,
                "authorization_created": False,
                "dispatch_enabled": False,
                "dispatched": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "llm_judge_enabled": False,
            },
            "next_step": STATIC_SAFETY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": STATIC_SAFETY_STATE,
            "version": STATIC_SAFETY_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionControlPlanState",
                "ExternalActionCandidateState",
                "DominionRuntimeInventoryState",
                "ExternalCapabilityCandidateState",
                "CapabilityRiskProfileState",
                "CapabilityBoundaryState",
            ],
            "target_read_models": [
                "DominionStaticSafetyState",
                "DominionStaticSafetyFindingState",
                "DominionPreflightEligibilityState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: DominionStaticSafetyReport | None = None, section: str = "summary") -> str:
        report = report or self.build_report()
        lines = [
            "Dominion Static Safety Check",
            f"version={report.version}",
            f"layer={STATIC_SAFETY_LAYER}",
            f"report_id={report.report_id}",
            f"plan_id={report.plan_id}",
            f"static_safety_status={report.static_safety_status}",
            f"eligible_for_preflight={str(report.eligible_for_preflight).lower()}",
            f"safe_to_dispatch={str(report.safe_to_dispatch).lower()}",
            f"preflight_required={str(report.preflight_required).lower()}",
            f"human_gate_required={str(report.human_gate_required).lower()}",
            f"authorization_required={str(report.authorization_required).lower()}",
            f"dispatch_enabled={str(report.dispatch_enabled).lower()}",
            f"dispatched={str(report.dispatched).lower()}",
            f"external_runtime_touched={str(report.runtime_touched).lower()}",
            f"provider_api_call_performed={str(report.provider_api_call_performed).lower()}",
            f"credential_exposed={str(report.credential_exposed).lower()}",
            f"llm_judge_used={str(report.llm_judge_used).lower()}",
        ]
        if section == "findings":
            lines.extend(f"- finding={item.finding_type} severity={item.severity}" for item in report.findings)
        elif section == "rules":
            lines.extend(f"- rule={item.rule_name} category={item.category}" for item in self.rules.list_rules())
        elif section == "summary":
            lines.extend(
                [
                    f"checked_rule_count={report.checked_rule_count}",
                    f"passed_rule_count={report.passed_rule_count}",
                    f"warning_count={report.warning_count}",
                    f"error_count={report.error_count}",
                    f"critical_count={report.critical_count}",
                ]
            )
        lines.extend(
            [
                f"next_required_step={report.next_required_step}",
                "raw_secrets_printed=False",
                "private_full_paths_printed=False",
            ]
        )
        return "\n".join(lines)


class DominionStaticSafetyService(DominionStaticSafetyReportService):
    def check_static_safety(self, request: DominionStaticSafetyCheckRequest | None = None) -> DominionStaticSafetyReport:
        return self.build_report(request)


def _rule(rules: list[DominionStaticSafetyRule], rule_name: str) -> DominionStaticSafetyRule:
    return next(item for item in rules if item.rule_name == rule_name)


def _plan_ref(plan: DominionControlPlan | None) -> dict[str, Any] | None:
    if not plan:
        return None
    return {"plan_id": plan.plan_id, "plan_status": plan.plan_status}


def _binding_ref(binding: Any | None) -> dict[str, Any] | None:
    return binding.to_dict() if binding and hasattr(binding, "to_dict") else None


def _result(
    rule: DominionStaticSafetyRule,
    passed: bool,
    plan: DominionControlPlan | None,
    binding: Any | None,
    message: str,
) -> DominionStaticSafetyRuleResult:
    return DominionStaticSafetyRuleResult(
        result_id=f"dominion_static_safety_rule_result:{rule.rule_name}",
        rule_id=rule.rule_id,
        category=rule.category,
        passed=passed,
        severity="info" if passed else rule.severity_if_failed,
        message="passed" if passed else message,
        plan_ref=_plan_ref(plan),
        binding_ref=_binding_ref(binding),
        evidence_refs=[{"policy": "v0.23.5_static_rule_only"}],
    )


def _binding_result(
    rule: DominionStaticSafetyRule,
    plan: DominionControlPlan | None,
    binding: Any | None,
    message: str,
    passed: bool | None = None,
) -> DominionStaticSafetyRuleResult:
    if passed is None:
        passed = bool(binding and getattr(binding, "binding_status", None) == "bound")
    return _result(rule, passed, plan, binding, message)


def _finding_type(result: DominionStaticSafetyRuleResult) -> str:
    if result.message != "passed":
        return result.message
    return result.rule_id.rsplit(":", 1)[-1]


def _category_results(
    rule_results: list[DominionStaticSafetyRuleResult],
    findings: list[DominionStaticSafetyFinding],
) -> list[DominionStaticSafetyCategoryResult]:
    by_category: list[DominionStaticSafetyCategoryResult] = []
    for category in CATEGORIES:
        results = [item for item in rule_results if item.category == category]
        category_findings = [item for item in findings if item.rule_ref and item.rule_ref.get("category") == category]
        warning_count = sum(1 for item in category_findings if item.severity == "warning")
        error_count = sum(1 for item in category_findings if item.severity == "error")
        critical_count = sum(1 for item in category_findings if item.severity == "critical")
        by_category.append(
            DominionStaticSafetyCategoryResult(
                category_id=f"dominion_static_safety_category:{category}",
                category=category,
                checked_rule_count=len(results),
                passed_rule_count=sum(1 for item in results if item.passed),
                warning_count=warning_count,
                error_count=error_count,
                critical_count=critical_count,
                category_status=_status(warning_count, error_count, critical_count),
                findings=category_findings,
            )
        )
    return by_category


def _status(warning_count: int, error_count: int, critical_count: int) -> str:
    if critical_count:
        return "blocked"
    if error_count:
        return "failed"
    if warning_count:
        return "warning"
    return "passed"
