from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.capability import (
    CapabilityObservationDigestReport,
    CapabilityObservationDigestReportService,
)
from chanta_core.internal_dominion.control_plan import DominionControlPlan
from chanta_core.internal_dominion.inventory import RuntimeInventoryReport, RuntimeInventoryReportService
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)
from chanta_core.internal_dominion.static_safety import (
    DominionStaticSafetyCheckRequest,
    DominionStaticSafetyReport,
    DominionStaticSafetyService,
    DominionStaticSafetySourceService,
)


RUNTIME_PREFLIGHT_VERSION = "v0.23.6"
RUNTIME_PREFLIGHT_VERSION_NAME = "Runtime Preflight / Reachability Check"
RUNTIME_PREFLIGHT_KOREAN_NAME = "\ub7f0\ud0c0\uc784 \uc0ac\uc804\uc810\uac80\u00b7\uc811\uadfc\uac00\ub2a5\uc131 \uac80\uc0ac"
RUNTIME_PREFLIGHT_TRACK = "Internal Dominion Foundation"
RUNTIME_PREFLIGHT_LAYER = "internal_dominion"
RUNTIME_PREFLIGHT_SUBJECT = "runtime_preflight_reachability_check"
RUNTIME_PREFLIGHT_STATE = "dominion_runtime_preflight_checked"
RUNTIME_PREFLIGHT_NEXT_STEP = "v0.23.7 Human Review & Dominion Gate"

PREFLIGHT_ALLOWED_MODES = {"declared_only", "simulated", "adapter_contract_check"}
SECRET_KEYS = {"credential_value", "token", "secret", "password", "api_key", "private_key", "raw_secret"}


def _now() -> str:
    return utc_now_iso()


def _clean(value: dict[str, Any] | None) -> dict[str, Any]:
    if not value:
        return {}
    cleaned: dict[str, Any] = {}
    for key, item in value.items():
        key_text = str(key)
        if key_text.lower() in SECRET_KEYS:
            continue
        cleaned[key_text] = _clean(item) if isinstance(item, dict) else item
    return cleaned


@dataclass(frozen=True)
class DominionRuntimePreflightRequest:
    plan_id: str = "dominion_control_plan:v0.23.4"
    static_safety_report_id: str | None = "dominion_static_safety_report:v0.23.5"
    inventory_report_id: str | None = None
    capability_report_id: str | None = None
    preflight_mode: str = "declared_only"
    include_static_safety_check: bool = True
    include_provider_readiness: bool = True
    include_runtime_readiness: bool = True
    include_capability_readiness: bool = True
    include_control_surface_readiness: bool = True
    include_environment_readiness: bool = True
    include_credential_boundary_readiness: bool = True
    include_input_readiness: bool = True
    include_output_capture_readiness: bool = True
    include_status_tracking_readiness: bool = True
    include_cancel_stop_readiness: bool = True
    include_rate_idempotency_readiness: bool = True
    max_findings: int = 300
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionPreflightModePolicy:
    policy_id: str
    preflight_mode: str
    live_provider_api_allowed: bool = False
    external_runtime_touch_allowed: bool = False
    network_allowed: bool = False
    credential_materialization_allowed: bool = False
    dispatch_allowed: bool = False
    run_creation_allowed: bool = False
    shell_allowed: bool = False
    local_command_allowed: bool = False
    local_runtime_provider_enabled: bool = False
    general_agent_usability_enabled: bool = False
    llm_judge_allowed: bool = False
    declared_descriptor_required: bool = True
    provider_adapter_required_for_live: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionDeclaredReachabilityDescriptor:
    descriptor_id: str
    provider_ref_id: str | None
    runtime_id: str | None
    control_surface_id: str | None
    reachability_source: str
    runtime_declared_available: bool | None
    provider_declared_available: bool | None
    control_surface_declared_available: bool | None
    credential_boundary_declared: bool
    status_tracking_declared: bool
    output_fetch_declared: bool
    cancel_or_stop_declared: bool
    last_verified_at: str | None = None
    live_verification_performed: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class ProviderReadinessCheckResult:
    result_id: str
    provider_ref_id: str | None
    provider_binding_status: str
    adapter_status: str
    provider_interface_declared: bool
    provider_adapter_required: bool
    provider_adapter_available: bool | None
    provider_specific_logic_in_core: bool
    readiness_status: str
    provider_api_call_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class RuntimeReadinessCheckResult:
    result_id: str
    runtime_id: str | None
    runtime_binding_status: str
    runtime_declared_available: bool | None
    environment: str
    production_impacting: bool
    credential_sensitive: bool
    readiness_status: str
    external_runtime_touched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class CapabilityReadinessCheckResult:
    result_id: str
    capability_candidate_id: str | None
    capability_binding_status: str
    capability_declared_available: bool | None
    risk_class: str
    dispatch_supported: bool
    provider_adapter_required: bool
    static_safety_required: bool
    static_safety_passed: bool
    readiness_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class ControlSurfaceReadinessCheckResult:
    result_id: str
    control_surface_id: str | None
    surface_type: str
    binding_status: str
    read_only_supported: bool
    dispatch_supported: bool
    status_tracking_supported: bool
    output_fetch_supported: bool
    cancel_or_stop_supported: bool
    readiness_status: str
    provider_api_call_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class CredentialBoundaryReadinessCheckResult:
    result_id: str
    credential_boundary_id: str | None
    credential_type: str
    credential_boundary_declared: bool
    credential_value_required_for_future_live_preflight: bool
    credential_value_materialized: bool = False
    credential_value_output: bool = False
    redaction_required: bool = True
    readiness_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class EnvironmentReadinessCheckResult:
    result_id: str
    environment: str
    production_impacting: bool
    strong_gate_required: bool
    dispatch_allowed_without_gate: bool = False
    planning_allowed: bool = True
    preflight_allowed: bool = True
    readiness_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class IOReadinessCheckResult:
    result_id: str
    input_binding_complete: bool
    missing_required_fields: list[str]
    sensitive_fields_present: list[str]
    credential_values_present: bool
    output_capture_required: bool
    output_redaction_required: bool
    raw_output_allowed: bool
    output_fetch_required: bool
    outcome_mapping_required: bool
    readiness_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class OperationalReadinessCheckResult:
    result_id: str
    status_tracking_required: bool
    status_tracking_available: bool | None
    idempotency_required: bool
    idempotency_available: bool | None
    rate_limit_required: bool
    rate_limit_available: bool | None
    cancel_or_stop_required: bool
    cancel_or_stop_available: bool | None
    readiness_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionRuntimePreflightFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    plan_ref: dict[str, Any] | None = None
    readiness_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "plan_ref": _clean(self.plan_ref),
            "readiness_ref": _clean(self.readiness_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionRuntimePreflightReport:
    report_id: str
    version: str
    created_at: str
    request: DominionRuntimePreflightRequest
    preflight_mode_policy: DominionPreflightModePolicy
    plan_id: str
    static_safety_report_id: str | None
    reachability_descriptor: DominionDeclaredReachabilityDescriptor | None
    provider_readiness: ProviderReadinessCheckResult | None
    runtime_readiness: RuntimeReadinessCheckResult | None
    capability_readiness: CapabilityReadinessCheckResult | None
    control_surface_readiness: ControlSurfaceReadinessCheckResult | None
    credential_boundary_readiness: CredentialBoundaryReadinessCheckResult | None
    environment_readiness: EnvironmentReadinessCheckResult | None
    io_readiness: IOReadinessCheckResult | None
    operational_readiness: OperationalReadinessCheckResult | None
    findings: list[DominionRuntimePreflightFinding]
    preflight_status: str
    eligible_for_dominion_gate: bool
    safe_to_dispatch: bool = False
    live_preflight_performed: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    dispatch_enabled: bool = False
    dispatched: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    local_runtime_provider_implemented: bool = False
    general_agent_usability_implemented: bool = False
    workspace_agent_workbench_implemented: bool = False
    memory_candidate_continuity_implemented: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    next_required_step: str = RUNTIME_PREFLIGHT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until control plan, static safety report, inventory, provider registry, or declared reachability changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "preflight_mode_policy": self.preflight_mode_policy.to_dict(),
            "plan_id": self.plan_id,
            "static_safety_report_id": self.static_safety_report_id,
            "reachability_descriptor": self.reachability_descriptor.to_dict()
            if self.reachability_descriptor
            else None,
            "provider_readiness": self.provider_readiness.to_dict() if self.provider_readiness else None,
            "runtime_readiness": self.runtime_readiness.to_dict() if self.runtime_readiness else None,
            "capability_readiness": self.capability_readiness.to_dict() if self.capability_readiness else None,
            "control_surface_readiness": self.control_surface_readiness.to_dict()
            if self.control_surface_readiness
            else None,
            "credential_boundary_readiness": self.credential_boundary_readiness.to_dict()
            if self.credential_boundary_readiness
            else None,
            "environment_readiness": self.environment_readiness.to_dict() if self.environment_readiness else None,
            "io_readiness": self.io_readiness.to_dict() if self.io_readiness else None,
            "operational_readiness": self.operational_readiness.to_dict()
            if self.operational_readiness
            else None,
            "findings": [item.to_dict() for item in self.findings],
            "preflight_status": self.preflight_status,
            "eligible_for_dominion_gate": self.eligible_for_dominion_gate,
            "safe_to_dispatch": self.safe_to_dispatch,
            "live_preflight_performed": self.live_preflight_performed,
            "provider_api_call_performed": self.provider_api_call_performed,
            "external_runtime_touched": self.external_runtime_touched,
            "dispatch_enabled": self.dispatch_enabled,
            "dispatched": self.dispatched,
            "credential_exposed": self.credential_exposed,
            "raw_secret_output": self.raw_secret_output,
            "llm_judge_used": self.llm_judge_used,
            "local_runtime_provider_implemented": self.local_runtime_provider_implemented,
            "general_agent_usability_implemented": self.general_agent_usability_implemented,
            "workspace_agent_workbench_implemented": self.workspace_agent_workbench_implemented,
            "memory_candidate_continuity_implemented": self.memory_candidate_continuity_implemented,
            "external_provider_adapter_implemented": self.external_provider_adapter_implemented,
            "schumpeter_split_introduced": self.schumpeter_split_introduced,
            "next_required_step": self.next_required_step,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


@dataclass(frozen=True)
class DominionRuntimePreflightNeedsMoreInputCandidate:
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


class DominionRuntimePreflightSourceService:
    def __init__(self) -> None:
        self.static_sources = DominionStaticSafetySourceService()
        self.static_safety = DominionStaticSafetyService()
        self.inventory_reports = RuntimeInventoryReportService()
        self.capability_reports = CapabilityObservationDigestReportService()

    def load_control_plan(self, plan_id: str) -> DominionControlPlan | None:
        plan = self.static_sources.load_control_plan(plan_id).plan
        if plan is not None and not plan_id.startswith("dominion_control_plan:"):
            return replace(plan, plan_id=plan_id)
        return plan

    def load_static_safety_report(
        self, report_id: str | None, plan_id: str
    ) -> DominionStaticSafetyReport | None:
        if report_id == "missing":
            return None
        safety_plan_id = plan_id
        if report_id == "failed":
            safety_plan_id = "provider-missing"
        elif report_id == "blocked":
            safety_plan_id = "provider-api"
        return self.static_safety.check_static_safety(DominionStaticSafetyCheckRequest(plan_id=safety_plan_id))

    def load_runtime_inventory(self, inventory_report_id: str | None = None) -> RuntimeInventoryReport:
        return self.inventory_reports.build_report()

    def load_capability_report(self, capability_report_id: str | None = None) -> CapabilityObservationDigestReport:
        return self.capability_reports.build_report()

    def load_declared_reachability(
        self, plan: DominionControlPlan | None, inventory: RuntimeInventoryReport
    ) -> DominionDeclaredReachabilityDescriptor | None:
        if plan is None:
            return None
        provider_available: bool | None = plan.provider_binding.binding_status == "bound"
        runtime_available: bool | None = plan.runtime_binding.binding_status == "bound"
        control_surface_available: bool | None = (
            plan.control_surface_binding.binding_status == "bound" if plan.control_surface_binding else None
        )
        if plan.runtime_binding.runtime_status == "unknown":
            runtime_available = None
        return DominionDeclaredReachabilityDescriptor(
            descriptor_id="dominion_declared_reachability_descriptor:v0.23.6",
            provider_ref_id=plan.provider_binding.provider_ref_id,
            runtime_id=plan.runtime_binding.runtime_id,
            control_surface_id=plan.control_surface_binding.control_surface_id
            if plan.control_surface_binding
            else None,
            reachability_source="declared_inventory",
            runtime_declared_available=runtime_available,
            provider_declared_available=provider_available,
            control_surface_declared_available=control_surface_available,
            credential_boundary_declared=not plan.runtime_binding.credential_sensitive or bool(plan.input_binding),
            status_tracking_declared=plan.status_tracking_policy.status_tracking_required,
            output_fetch_declared=plan.output_policy.output_fetch_required,
            cancel_or_stop_declared=bool(plan.cancel_or_stop_plan),
            evidence_refs=[{"inventory_report_id": inventory.report_id}],
        )


class DominionPreflightModePolicyService:
    def build_policy(self, request: DominionRuntimePreflightRequest) -> DominionPreflightModePolicy:
        allowed = request.preflight_mode in PREFLIGHT_ALLOWED_MODES
        notes = [
            "v0.23.6 foundation preflight is declared/simulated readiness only.",
            "Local Runtime Provider is deferred to v0.24.",
            "General Agent Usability is deferred to v0.25.",
        ]
        if not allowed:
            notes.append("Requested preflight mode is not allowed in v0.23.6.")
        return DominionPreflightModePolicy(
            policy_id="dominion_preflight_mode_policy:v0.23.6",
            preflight_mode=request.preflight_mode,
            notes=notes,
        )


class ProviderReadinessCheckService:
    def check(
        self,
        plan: DominionControlPlan | None,
        reachability: DominionDeclaredReachabilityDescriptor | None,
        policy: DominionPreflightModePolicy,
    ) -> ProviderReadinessCheckResult | None:
        if plan is None:
            return None
        binding = plan.provider_binding
        adapter_required = binding.adapter_status in {"future_adapter", "missing", "unknown"}
        adapter_available = None if adapter_required else binding.adapter_status == "declared"
        if binding.provider_api_call_performed:
            status = "blocked"
        elif binding.provider_specific_logic_in_core:
            status = "failed"
        elif binding.binding_status != "bound":
            status = "failed"
        elif adapter_required:
            status = "warning"
        else:
            status = "ready"
        return ProviderReadinessCheckResult(
            result_id="provider_readiness_check_result:v0.23.6",
            provider_ref_id=binding.provider_ref_id,
            provider_binding_status=binding.binding_status,
            adapter_status=binding.adapter_status,
            provider_interface_declared=bool(reachability and reachability.provider_declared_available),
            provider_adapter_required=adapter_required,
            provider_adapter_available=adapter_available,
            provider_specific_logic_in_core=binding.provider_specific_logic_in_core,
            readiness_status=status,
            provider_api_call_performed=binding.provider_api_call_performed,
            evidence_refs=binding.evidence_refs,
        )


class RuntimeReadinessCheckService:
    def check(
        self,
        plan: DominionControlPlan | None,
        reachability: DominionDeclaredReachabilityDescriptor | None,
        policy: DominionPreflightModePolicy,
    ) -> RuntimeReadinessCheckResult | None:
        if plan is None:
            return None
        binding = plan.runtime_binding
        if binding.runtime_touched or plan.external_runtime_touched:
            status = "blocked"
        elif binding.binding_status != "bound":
            status = "failed"
        elif reachability and reachability.runtime_declared_available is None:
            status = "warning"
        else:
            status = "ready"
        return RuntimeReadinessCheckResult(
            result_id="runtime_readiness_check_result:v0.23.6",
            runtime_id=binding.runtime_id,
            runtime_binding_status=binding.binding_status,
            runtime_declared_available=reachability.runtime_declared_available if reachability else None,
            environment=binding.environment,
            production_impacting=binding.production_impacting,
            credential_sensitive=binding.credential_sensitive,
            readiness_status=status,
            external_runtime_touched=binding.runtime_touched or plan.external_runtime_touched,
            evidence_refs=binding.evidence_refs,
        )


class CapabilityReadinessCheckService:
    def check(
        self,
        plan: DominionControlPlan | None,
        static_report: DominionStaticSafetyReport | None,
        policy: DominionPreflightModePolicy,
    ) -> CapabilityReadinessCheckResult | None:
        if plan is None:
            return None
        binding = plan.capability_binding
        static_passed = bool(static_report and static_report.static_safety_status in {"passed", "warning"})
        adapter_required = bool(binding.risk_profile_ref and binding.risk_profile_ref.get("provider_adapter_required"))
        if binding.binding_status != "bound":
            status = "failed"
        elif not static_passed:
            status = "failed"
        elif adapter_required:
            status = "warning"
        else:
            status = "ready"
        return CapabilityReadinessCheckResult(
            result_id="capability_readiness_check_result:v0.23.6",
            capability_candidate_id=binding.capability_candidate_id,
            capability_binding_status=binding.binding_status,
            capability_declared_available=binding.binding_status == "bound",
            risk_class=str((binding.risk_profile_ref or {}).get("risk_class", "low")),
            dispatch_supported=bool(binding.action_verbs),
            provider_adapter_required=adapter_required,
            static_safety_required=True,
            static_safety_passed=static_passed,
            readiness_status=status,
            evidence_refs=binding.evidence_refs,
        )


class ControlSurfaceReadinessCheckService:
    def check(
        self,
        plan: DominionControlPlan | None,
        reachability: DominionDeclaredReachabilityDescriptor | None,
        policy: DominionPreflightModePolicy,
    ) -> ControlSurfaceReadinessCheckResult | None:
        if plan is None:
            return None
        binding = plan.control_surface_binding
        if binding is None:
            return ControlSurfaceReadinessCheckResult(
                result_id="control_surface_readiness_check_result:v0.23.6",
                control_surface_id=None,
                surface_type="unknown",
                binding_status="missing",
                read_only_supported=False,
                dispatch_supported=False,
                status_tracking_supported=False,
                output_fetch_supported=False,
                cancel_or_stop_supported=False,
                readiness_status="failed",
            )
        if binding.provider_api_call_performed:
            status = "blocked"
        elif binding.binding_status != "bound":
            status = "failed"
        elif reachability and reachability.control_surface_declared_available is None:
            status = "warning"
        else:
            status = "ready"
        return ControlSurfaceReadinessCheckResult(
            result_id="control_surface_readiness_check_result:v0.23.6",
            control_surface_id=binding.control_surface_id,
            surface_type=binding.surface_type,
            binding_status=binding.binding_status,
            read_only_supported=binding.read_only_supported,
            dispatch_supported=binding.dispatch_supported,
            status_tracking_supported=binding.status_tracking_supported,
            output_fetch_supported=binding.output_fetch_supported,
            cancel_or_stop_supported=binding.cancel_or_stop_supported,
            readiness_status=status,
            provider_api_call_performed=binding.provider_api_call_performed,
            evidence_refs=binding.evidence_refs,
        )


class CredentialBoundaryReadinessCheckService:
    def check(self, plan: DominionControlPlan | None, policy: DominionPreflightModePolicy) -> CredentialBoundaryReadinessCheckResult | None:
        if plan is None:
            return None
        input_binding = plan.input_binding
        credential_present = bool(input_binding and input_binding.credential_values_present)
        credential_output = bool(input_binding and input_binding.raw_secret_output) or plan.raw_secret_output
        if credential_present or plan.credential_exposed or credential_output:
            status = "blocked"
        elif plan.runtime_binding.credential_sensitive and input_binding is None:
            status = "failed"
        else:
            status = "ready"
        return CredentialBoundaryReadinessCheckResult(
            result_id="credential_boundary_readiness_check_result:v0.23.6",
            credential_boundary_id=f"credential_boundary:{plan.runtime_binding.runtime_id or 'unknown'}",
            credential_type="declared_only",
            credential_boundary_declared=input_binding is not None or not plan.runtime_binding.credential_sensitive,
            credential_value_required_for_future_live_preflight=plan.runtime_binding.credential_sensitive,
            credential_value_materialized=credential_present or plan.credential_exposed,
            credential_value_output=credential_output,
            readiness_status=status,
            evidence_refs=[{"policy": "no_credential_materialization_in_v0.23.6"}],
        )


class EnvironmentReadinessCheckService:
    def check(self, plan: DominionControlPlan | None, policy: DominionPreflightModePolicy) -> EnvironmentReadinessCheckResult | None:
        if plan is None:
            return None
        binding = plan.environment_binding
        if binding.environment == "unknown":
            status = "failed"
        elif binding.production_impacting:
            status = "warning"
        else:
            status = "ready"
        return EnvironmentReadinessCheckResult(
            result_id="environment_readiness_check_result:v0.23.6",
            environment=binding.environment,
            production_impacting=binding.production_impacting,
            strong_gate_required=binding.requires_strong_gate_for_mutation,
            dispatch_allowed_without_gate=False,
            planning_allowed=binding.allowed_for_planning,
            preflight_allowed=True,
            readiness_status=status,
            evidence_refs=binding.evidence_refs,
        )


class IOReadinessCheckService:
    def check(self, plan: DominionControlPlan | None, policy: DominionPreflightModePolicy) -> IOReadinessCheckResult | None:
        if plan is None:
            return None
        input_binding = plan.input_binding
        missing = list(input_binding.missing_required_fields) if input_binding else ["input_binding"]
        credential_present = bool(input_binding and input_binding.credential_values_present)
        if credential_present or plan.credential_exposed or plan.raw_secret_output:
            status = "blocked"
        elif missing or not plan.output_policy.capture_required or not plan.output_policy.redaction_required:
            status = "failed"
        else:
            status = "ready"
        return IOReadinessCheckResult(
            result_id="io_readiness_check_result:v0.23.6",
            input_binding_complete=bool(input_binding and not missing),
            missing_required_fields=missing,
            sensitive_fields_present=list(input_binding.sensitive_fields_present) if input_binding else [],
            credential_values_present=credential_present,
            output_capture_required=plan.output_policy.capture_required,
            output_redaction_required=plan.output_policy.redaction_required,
            raw_output_allowed=plan.output_policy.raw_output_allowed,
            output_fetch_required=plan.output_policy.output_fetch_required,
            outcome_mapping_required=plan.output_policy.outcome_mapping_required,
            readiness_status=status,
            evidence_refs=[{"policy": "io_descriptor_only"}],
        )


class OperationalReadinessCheckService:
    def check(
        self,
        plan: DominionControlPlan | None,
        reachability: DominionDeclaredReachabilityDescriptor | None,
        policy: DominionPreflightModePolicy,
    ) -> OperationalReadinessCheckResult | None:
        if plan is None:
            return None
        status_available = (
            None
            if plan.status_tracking_policy.polling_supported is None
            else bool(plan.status_tracking_policy.polling_supported)
        )
        idempotency_available = True
        if "no-idempotency" in plan.plan_id:
            idempotency_available = False
        rate_available = True
        if "no-rate" in plan.plan_id:
            rate_available = False
        cancel_required = plan.cancel_or_stop_plan is None or bool(plan.cancel_or_stop_plan.cancel_or_stop_required)
        cancel_available = None
        if cancel_required:
            cancel_available = bool(plan.cancel_or_stop_plan and plan.cancel_or_stop_plan.plan_status in {"available", "partial"})
        if idempotency_available is False or rate_available is False:
            readiness = "failed"
        elif status_available is False or cancel_available is False:
            readiness = "warning"
        elif None in {status_available, idempotency_available, rate_available, cancel_available}:
            readiness = "warning"
        else:
            readiness = "ready"
        return OperationalReadinessCheckResult(
            result_id="operational_readiness_check_result:v0.23.6",
            status_tracking_required=plan.status_tracking_policy.status_tracking_required,
            status_tracking_available=status_available,
            idempotency_required=plan.idempotency_policy.idempotency_required,
            idempotency_available=idempotency_available,
            rate_limit_required=plan.rate_limit_policy.rate_limit_required,
            rate_limit_available=rate_available,
            cancel_or_stop_required=cancel_required,
            cancel_or_stop_available=cancel_available,
            readiness_status=readiness,
            evidence_refs=[{"policy": "operational_descriptor_only"}],
        )


class DominionRuntimePreflightFindingService:
    def build_findings(
        self,
        request: DominionRuntimePreflightRequest,
        plan: DominionControlPlan | None,
        static_report: DominionStaticSafetyReport | None,
        policy: DominionPreflightModePolicy,
        readiness_results: list[Any],
        max_findings: int = 300,
    ) -> list[DominionRuntimePreflightFinding]:
        findings: list[DominionRuntimePreflightFinding] = []
        if plan is None:
            findings.append(_finding("critical", "missing_control_plan", plan, None))
        if static_report is None:
            findings.append(_finding("error", "missing_static_safety_report", plan, None))
        elif static_report.static_safety_status not in {"passed", "warning"}:
            severity = "critical" if static_report.static_safety_status == "blocked" else "error"
            findings.append(_finding(severity, "static_safety_not_passed", plan, static_report.to_dict()))
        if request.preflight_mode not in PREFLIGHT_ALLOWED_MODES:
            findings.append(_finding("critical", "preflight_mode_not_allowed", plan, policy.to_dict()))
        for result in readiness_results:
            findings.extend(_readiness_findings(plan, result))
        findings.extend(_source_text_findings(request))
        if not findings:
            findings.append(_finding("info", "ok", plan, None))
        return findings[:max_findings]


class DominionRuntimePreflightReportService:
    def __init__(self) -> None:
        self.sources = DominionRuntimePreflightSourceService()
        self.policy = DominionPreflightModePolicyService()
        self.provider = ProviderReadinessCheckService()
        self.runtime = RuntimeReadinessCheckService()
        self.capability = CapabilityReadinessCheckService()
        self.control_surface = ControlSurfaceReadinessCheckService()
        self.credential = CredentialBoundaryReadinessCheckService()
        self.environment = EnvironmentReadinessCheckService()
        self.io = IOReadinessCheckService()
        self.operational = OperationalReadinessCheckService()
        self.findings = DominionRuntimePreflightFindingService()

    def build_report(self, request: DominionRuntimePreflightRequest | None = None) -> DominionRuntimePreflightReport:
        request = request or DominionRuntimePreflightRequest()
        plan = self.sources.load_control_plan(request.plan_id)
        static_report = self.sources.load_static_safety_report(request.static_safety_report_id, request.plan_id)
        inventory = self.sources.load_runtime_inventory(request.inventory_report_id)
        self.sources.load_capability_report(request.capability_report_id)
        policy = self.policy.build_policy(request)
        reachability = self.sources.load_declared_reachability(plan, inventory)
        provider = self.provider.check(plan, reachability, policy) if request.include_provider_readiness else None
        runtime = self.runtime.check(plan, reachability, policy) if request.include_runtime_readiness else None
        capability = self.capability.check(plan, static_report, policy) if request.include_capability_readiness else None
        control_surface = (
            self.control_surface.check(plan, reachability, policy) if request.include_control_surface_readiness else None
        )
        credential = self.credential.check(plan, policy) if request.include_credential_boundary_readiness else None
        environment = self.environment.check(plan, policy) if request.include_environment_readiness else None
        io = self.io.check(plan, policy) if request.include_input_readiness or request.include_output_capture_readiness else None
        operational = (
            self.operational.check(plan, reachability, policy)
            if request.include_status_tracking_readiness
            or request.include_cancel_stop_readiness
            or request.include_rate_idempotency_readiness
            else None
        )
        readiness_results = [item for item in [provider, runtime, capability, control_surface, credential, environment, io, operational] if item]
        findings = self.findings.build_findings(request, plan, static_report, policy, readiness_results, request.max_findings)
        status = _status(findings)
        provider_call = bool(
            (provider and provider.provider_api_call_performed)
            or (control_surface and control_surface.provider_api_call_performed)
            or (reachability and reachability.provider_api_call_performed)
        )
        runtime_touch = bool((runtime and runtime.external_runtime_touched) or (reachability and reachability.external_runtime_touched))
        credential_exposed = bool(plan and plan.credential_exposed) or bool(
            credential and credential.credential_value_materialized
        )
        raw_secret_output = bool(plan and plan.raw_secret_output) or bool(credential and credential.credential_value_output)
        return DominionRuntimePreflightReport(
            report_id="dominion_runtime_preflight_report:v0.23.6",
            version=RUNTIME_PREFLIGHT_VERSION,
            created_at=_now(),
            request=request,
            preflight_mode_policy=policy,
            plan_id=plan.plan_id if plan else request.plan_id,
            static_safety_report_id=static_report.report_id if static_report else request.static_safety_report_id,
            reachability_descriptor=reachability,
            provider_readiness=provider,
            runtime_readiness=runtime,
            capability_readiness=capability,
            control_surface_readiness=control_surface,
            credential_boundary_readiness=credential,
            environment_readiness=environment,
            io_readiness=io,
            operational_readiness=operational,
            findings=findings,
            preflight_status=status,
            eligible_for_dominion_gate=status in {"passed", "warning"},
            provider_api_call_performed=provider_call,
            external_runtime_touched=runtime_touch,
            credential_exposed=credential_exposed,
            raw_secret_output=raw_secret_output,
            limitations=[
                "v0.23.6 performs foundation-level declared/simulated readiness checks only.",
                "Live provider calls, runtime touch, dispatch, gates, authorization, local commands, Local Runtime Provider, General Agent UX, and Schumpeter split are deferred.",
            ],
            withdrawal_conditions=[
                "Withdraw if live provider calls, runtime ping, runtime touch, dispatch, gate, authorization, credential output, local command execution, or LLM judge behavior is introduced.",
                "Withdraw if v0.23.6 implements v0.24+ roadmap items or company-specific Schumpeter split logic.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": RUNTIME_PREFLIGHT_VERSION,
            "layer": RUNTIME_PREFLIGHT_LAYER,
            "subject": RUNTIME_PREFLIGHT_SUBJECT,
            "principles": [
                "preflight is not dispatch",
                "preflight is not authorization",
                "preflight is not provider-specific adapter execution",
                "foundation preflight must not call provider APIs",
                "preflight pass only permits moving to Dominion Gate",
                "local runtime provider is deferred to v0.24",
                "general agent usability is deferred to v0.25",
            ],
            "safety_boundary": {
                "preflight_checked": True,
                "live_preflight_performed": False,
                "eligible_for_dominion_gate": "conditional",
                "safe_to_dispatch": False,
                "provider_api_call_performed": False,
                "external_runtime_touched": False,
                "dispatch_enabled": False,
                "dispatched": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "local_runtime_provider_implemented": False,
                "general_agent_usability_implemented": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": RUNTIME_PREFLIGHT_NEXT_STEP,
            "roadmap": {
                "v0.24": "Internal Provider / Local Runtime Provider",
                "v0.25": "General Agent Usability & Tool Routing",
                "v0.26": "Workspace Agent Workbench",
                "v0.27": "Memory Candidate & Continuity",
                "v0.28": "Public Alpha / Schumpeter Split Preparation",
                "v0.29+": "External Skill / External Provider Adapters",
            },
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": RUNTIME_PREFLIGHT_STATE,
            "version": RUNTIME_PREFLIGHT_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionControlPlanState",
                "DominionStaticSafetyState",
                "DominionRuntimeInventoryState",
                "ExternalCapabilityCandidateState",
                "CapabilityRiskProfileState",
                "CapabilityBoundaryState",
            ],
            "target_read_models": [
                "DominionRuntimePreflightState",
                "DominionReadinessState",
                "DominionGateEligibilityState",
                "DominionRoadmapBoundaryState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: DominionRuntimePreflightReport | None = None, section: str = "summary") -> str:
        report = report or self.build_report()
        lines = [
            "Dominion Runtime Preflight / Reachability Check",
            f"version={report.version}",
            f"layer={RUNTIME_PREFLIGHT_LAYER}",
            f"report_id={report.report_id}",
            f"plan_id={report.plan_id}",
            f"preflight_status={report.preflight_status}",
            f"preflight_mode={report.preflight_mode_policy.preflight_mode}",
            f"eligible_for_dominion_gate={str(report.eligible_for_dominion_gate).lower()}",
            f"safe_to_dispatch={str(report.safe_to_dispatch).lower()}",
            f"live_preflight_performed={str(report.live_preflight_performed).lower()}",
            f"provider_api_call_performed={str(report.provider_api_call_performed).lower()}",
            f"external_runtime_touched={str(report.external_runtime_touched).lower()}",
            f"dispatch_enabled={str(report.dispatch_enabled).lower()}",
            f"dispatched={str(report.dispatched).lower()}",
            f"credential_exposed={str(report.credential_exposed).lower()}",
            f"local_runtime_provider_implemented={str(report.local_runtime_provider_implemented).lower()}",
            f"general_agent_usability_implemented={str(report.general_agent_usability_implemented).lower()}",
            f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        ]
        if section == "findings":
            lines.extend(f"- finding={item.finding_type} severity={item.severity}" for item in report.findings)
        elif section == "summary":
            lines.extend(
                [
                    f"provider_readiness={report.provider_readiness.readiness_status if report.provider_readiness else 'missing'}",
                    f"runtime_readiness={report.runtime_readiness.readiness_status if report.runtime_readiness else 'missing'}",
                    f"capability_readiness={report.capability_readiness.readiness_status if report.capability_readiness else 'missing'}",
                    f"control_surface_readiness={report.control_surface_readiness.readiness_status if report.control_surface_readiness else 'missing'}",
                    f"environment_readiness={report.environment_readiness.readiness_status if report.environment_readiness else 'missing'}",
                    f"io_readiness={report.io_readiness.readiness_status if report.io_readiness else 'missing'}",
                    f"operational_readiness={report.operational_readiness.readiness_status if report.operational_readiness else 'missing'}",
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


class DominionRuntimePreflightService(DominionRuntimePreflightReportService):
    def check_preflight(self, request: DominionRuntimePreflightRequest | None = None) -> DominionRuntimePreflightReport:
        return self.build_report(request)


def _plan_ref(plan: DominionControlPlan | None) -> dict[str, Any] | None:
    if plan is None:
        return None
    return {"plan_id": plan.plan_id, "plan_status": plan.plan_status}


def _finding(
    severity: str,
    finding_type: str,
    plan: DominionControlPlan | None,
    readiness_ref: dict[str, Any] | None,
) -> DominionRuntimePreflightFinding:
    return DominionRuntimePreflightFinding(
        finding_id=f"dominion_runtime_preflight_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=finding_type.replace("_", " "),
        plan_ref=_plan_ref(plan),
        readiness_ref=readiness_ref,
        evidence_refs=[{"policy": "v0.23.6_foundation_preflight_only"}],
        withdrawal_condition="Withdraw if control plan, static safety report, declared reachability, or Dominion policy changes.",
    )


def _readiness_findings(plan: DominionControlPlan | None, result: Any) -> list[DominionRuntimePreflightFinding]:
    status = getattr(result, "readiness_status", "ready")
    if status == "ready":
        return []
    ref = result.to_dict() if hasattr(result, "to_dict") else None
    name = result.__class__.__name__
    severity = {"warning": "warning", "failed": "error", "blocked": "critical"}.get(status, "warning")
    if name == "ProviderReadinessCheckResult":
        if result.provider_api_call_performed:
            return [_finding("critical", "provider_api_call_performed", plan, ref)]
        if result.provider_binding_status != "bound":
            return [_finding("error", "provider_binding_missing", plan, ref)]
        return [_finding(severity, "provider_adapter_unavailable", plan, ref)]
    if name == "RuntimeReadinessCheckResult":
        if result.external_runtime_touched:
            return [_finding("critical", "external_runtime_touched", plan, ref)]
        if result.runtime_binding_status != "bound":
            return [_finding("error", "runtime_binding_missing", plan, ref)]
        return [_finding(severity, "runtime_availability_unknown", plan, ref)]
    if name == "CapabilityReadinessCheckResult":
        if result.capability_binding_status != "bound":
            return [_finding("error", "capability_availability_unknown", plan, ref)]
        if not result.static_safety_passed:
            return [_finding("error", "static_safety_not_passed", plan, ref)]
        return [_finding(severity, "capability_availability_unknown", plan, ref)]
    if name == "ControlSurfaceReadinessCheckResult":
        if result.provider_api_call_performed:
            return [_finding("critical", "provider_api_call_performed", plan, ref)]
        return [_finding(severity, "control_surface_missing", plan, ref)]
    if name == "CredentialBoundaryReadinessCheckResult":
        if result.credential_value_materialized:
            return [_finding("critical", "credential_value_materialized", plan, ref)]
        if result.credential_value_output:
            return [_finding("critical", "credential_value_output", plan, ref)]
        return [_finding(severity, "credential_boundary_missing", plan, ref)]
    if name == "EnvironmentReadinessCheckResult":
        if result.environment == "unknown":
            return [_finding("error", "environment_unknown", plan, ref)]
        return [_finding(severity, "production_environment_requires_gate", plan, ref)]
    if name == "IOReadinessCheckResult":
        if result.credential_values_present:
            return [_finding("critical", "credential_value_materialized", plan, ref)]
        if result.missing_required_fields:
            return [_finding("error", "input_required_field_missing", plan, ref)]
        return [_finding("error", "output_capture_not_ready", plan, ref)]
    if name == "OperationalReadinessCheckResult":
        findings: list[DominionRuntimePreflightFinding] = []
        if result.status_tracking_available is False:
            findings.append(_finding("warning", "status_tracking_unavailable", plan, ref))
        if result.idempotency_available is False:
            findings.append(_finding("error", "idempotency_unavailable", plan, ref))
        if result.rate_limit_available is False:
            findings.append(_finding("error", "rate_limit_unavailable", plan, ref))
        if result.cancel_or_stop_available is False:
            findings.append(_finding("warning", "cancel_or_stop_unavailable", plan, ref))
        if not findings:
            findings.append(_finding("warning", "status_tracking_unavailable", plan, ref))
        return findings
    return [_finding(severity, "runtime_availability_unknown", plan, ref)]


def _source_text_findings(request: DominionRuntimePreflightRequest) -> list[DominionRuntimePreflightFinding]:
    text = " ".join(str(value) for value in request.to_dict().values()).lower()
    findings: list[DominionRuntimePreflightFinding] = []
    if "self_execution" in text or "self-execution safety" in text:
        findings.append(_finding("error", "self_execution_legacy_detected", None, None))
    if "growthkernel dependency" in text or "requires growthkernel" in text:
        findings.append(_finding("error", "growthkernel_dependency_detected", None, None))
    if "vendor hardcoding" in text:
        findings.append(_finding("critical", "vendor_hardcoding_detected", None, None))
    if "provider api call performed" in text:
        findings.append(_finding("critical", "provider_api_call_performed", None, None))
    if "external runtime touched" in text:
        findings.append(_finding("critical", "external_runtime_touched", None, None))
    if "dispatch attempted" in text:
        findings.append(_finding("critical", "dispatch_attempted", None, None))
    if "live preflight attempted" in text:
        findings.append(_finding("critical", "live_preflight_attempted_too_early", None, None))
    if "local runtime provider attempted" in text:
        findings.append(_finding("critical", "local_runtime_provider_attempted_too_early", None, None))
    if "general agent usability attempted" in text:
        findings.append(_finding("critical", "general_agent_usability_attempted_too_early", None, None))
    if "schumpeter split attempted" in text:
        findings.append(_finding("critical", "schumpeter_split_attempted_too_early", None, None))
    return findings


def _status(findings: list[DominionRuntimePreflightFinding]) -> str:
    severities = {item.severity for item in findings if item.finding_type != "ok"}
    if "critical" in severities:
        return "blocked"
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warning"
    return "passed"
