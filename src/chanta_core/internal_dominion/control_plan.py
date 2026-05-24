from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.capability import (
    CapabilityObservationDigestReport,
    CapabilityObservationDigestReportService,
    ExternalCapabilityCandidate,
)
from chanta_core.internal_dominion.control import (
    DominionControlRequestCandidateReport,
    DominionControlRequestCandidateService,
    DominionControlRequestCreateRequest,
    ExternalActionCandidate,
)
from chanta_core.internal_dominion.inventory import RuntimeInventoryReport, RuntimeInventoryReportService
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)


CONTROL_PLAN_VERSION = "v0.23.4"
CONTROL_PLAN_VERSION_NAME = "Control Plan & Target Binding"
CONTROL_PLAN_KOREAN_NAME = "제어 계획·대상 바인딩"
CONTROL_PLAN_TRACK = "Internal Dominion Foundation"
CONTROL_PLAN_LAYER = "internal_dominion"
CONTROL_PLAN_SUBJECT = "control_plan_target_binding"
CONTROL_PLAN_STATE = "dominion_control_plan_bound"
CONTROL_PLAN_NEXT_STEP = "v0.23.5 Dominion Static Safety Check"

SECRET_KEYS = {"credential_value", "token", "secret", "password", "api_key", "private_key", "raw_secret"}
ENVIRONMENTS = {"local", "dev", "test", "staging", "production", "sandbox", "unknown"}


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


def _has_secret(value: dict[str, Any] | None) -> bool:
    return bool(value) and any(str(key).lower() in SECRET_KEYS for key in value)


def _source_flag(source_refs: list[dict[str, Any]], key: str) -> bool:
    return any(bool(item.get(key)) for item in source_refs)


@dataclass(frozen=True)
class DominionControlPlanCreateRequest:
    action_candidate_id: str = "external_action_candidate:v0.23.3"
    request_id: str | None = None
    inventory_report_id: str | None = None
    capability_report_id: str | None = None
    requested_environment: str | None = None
    requested_provider_ref_id: str | None = None
    requested_runtime_id: str | None = None
    requested_control_surface_id: str | None = None
    requested_input_overrides: dict[str, Any] = field(default_factory=dict)
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    allow_no_action: bool = True
    allow_needs_more_input: bool = True
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return {
            "action_candidate_id": self.action_candidate_id,
            "request_id": self.request_id,
            "inventory_report_id": self.inventory_report_id,
            "capability_report_id": self.capability_report_id,
            "requested_environment": self.requested_environment,
            "requested_provider_ref_id": self.requested_provider_ref_id,
            "requested_runtime_id": self.requested_runtime_id,
            "requested_control_surface_id": self.requested_control_surface_id,
            "requested_input_overrides": _clean(self.requested_input_overrides),
            "source_refs": [_clean(item) for item in self.source_refs],
            "constraints": list(self.constraints),
            "allow_no_action": self.allow_no_action,
            "allow_needs_more_input": self.allow_needs_more_input,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class ProviderBinding:
    binding_id: str
    provider_ref_id: str | None
    provider_type: str
    vendor_name: str | None
    adapter_status: str
    binding_status: str
    provider_specific_logic_in_core: bool = False
    provider_api_call_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class RuntimeBinding:
    binding_id: str
    runtime_id: str | None
    runtime_type: str
    runtime_name: str | None
    environment: str
    runtime_status: str
    binding_status: str
    production_impacting: bool
    credential_sensitive: bool
    runtime_touched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class CapabilityBinding:
    binding_id: str
    capability_candidate_id: str | None
    capability_name: str | None
    normalized_capability_type: str
    action_verbs: list[dict[str, Any]]
    risk_profile_ref: dict[str, Any] | None
    boundary_ref: dict[str, Any] | None
    binding_status: str
    dispatch_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "risk_profile_ref": _clean(self.risk_profile_ref),
            "boundary_ref": _clean(self.boundary_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class ControlSurfaceBinding:
    binding_id: str
    control_surface_id: str | None
    surface_type: str
    provider_ref_id: str | None
    runtime_id: str | None
    read_only_supported: bool
    dispatch_supported: bool
    status_tracking_supported: bool
    output_fetch_supported: bool
    cancel_or_stop_supported: bool
    binding_status: str
    dispatch_enabled: bool = False
    provider_api_call_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class EnvironmentBinding:
    binding_id: str
    environment: str
    production_impacting: bool
    requires_human_gate_for_dispatch: bool
    requires_strong_gate_for_mutation: bool
    allowed_for_planning: bool = True
    dispatch_allowed: bool = False
    binding_status: str = "bound"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionInputBinding:
    input_binding_id: str
    action_candidate_id: str
    input_schema_ref: dict[str, Any] | None
    bound_fields: dict[str, Any]
    missing_required_fields: list[str]
    sensitive_fields_present: list[str]
    credential_values_present: bool
    raw_secret_output: bool = False
    binding_status: str = "draft_bound"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "input_schema_ref": _clean(self.input_schema_ref),
            "bound_fields": _clean(self.bound_fields),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionOutputPolicy:
    output_policy_id: str
    output_schema_ref: dict[str, Any] | None
    capture_required: bool = True
    redaction_required: bool = True
    raw_output_allowed: bool = False
    max_output_bytes: int | None = None
    sensitive_output_fields: list[str] = field(default_factory=list)
    output_fetch_required: bool = True
    outcome_mapping_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "output_schema_ref": _clean(self.output_schema_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionStatusTrackingPolicy:
    status_policy_id: str
    status_tracking_required: bool = True
    polling_supported: bool | None = None
    callback_supported: bool | None = None
    terminal_statuses: list[str] = field(default_factory=list)
    unknown_status_allowed: bool = False
    status_tracking_owner: str | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionIdempotencyPolicy:
    idempotency_policy_id: str
    idempotency_required: bool
    idempotency_key: str | None
    duplicate_dispatch_protection_required: bool
    duplicate_dispatch_protection_available: bool | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionRateLimitPolicy:
    rate_limit_policy_id: str
    rate_limit_required: bool
    max_dispatches_per_window: int | None
    concurrency_limit_required: bool
    max_concurrent_runs: int | None
    burst_allowed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionCancelOrStopPlanDescriptor:
    cancel_plan_id: str
    action_candidate_id: str
    cancel_or_stop_required: bool
    cancel_supported: bool | None
    stop_supported: bool | None
    manual_intervention_required: bool
    cancel_surface_ref: dict[str, Any] | None
    stop_surface_ref: dict[str, Any] | None
    plan_status: str
    execution_enabled: bool = False
    executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "cancel_surface_ref": _clean(self.cancel_surface_ref),
            "stop_surface_ref": _clean(self.stop_surface_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionControlPlanConstraint:
    constraint_id: str
    constraint_type: str
    description: str
    severity: str
    source_ref: dict[str, Any] | None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"source_ref": _clean(self.source_ref)}


@dataclass(frozen=True)
class DominionControlPlanFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    binding_ref: dict[str, Any] | None = None
    plan_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "binding_ref": _clean(self.binding_ref),
            "plan_ref": _clean(self.plan_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionControlPlan:
    plan_id: str
    action_candidate_id: str
    request_id: str | None
    created_at: str
    title: str
    goal_text: str
    provider_binding: ProviderBinding
    runtime_binding: RuntimeBinding
    capability_binding: CapabilityBinding
    control_surface_binding: ControlSurfaceBinding | None
    environment_binding: EnvironmentBinding
    input_binding: DominionInputBinding | None
    output_policy: DominionOutputPolicy
    status_tracking_policy: DominionStatusTrackingPolicy
    idempotency_policy: DominionIdempotencyPolicy
    rate_limit_policy: DominionRateLimitPolicy
    cancel_or_stop_plan: DominionCancelOrStopPlanDescriptor | None
    constraints: list[DominionControlPlanConstraint]
    findings: list[DominionControlPlanFinding]
    plan_status: str
    readiness: str
    static_safety_required: bool = True
    static_safety_checked: bool = False
    preflight_required: bool = True
    preflight_checked: bool = False
    human_gate_required: bool = True
    human_gate_opened: bool = False
    authorization_required: bool = True
    authorization_created: bool = False
    dispatch_enabled: bool = False
    dispatched: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "plan_id": self.plan_id,
            "action_candidate_id": self.action_candidate_id,
            "request_id": self.request_id,
            "created_at": self.created_at,
            "title": self.title,
            "goal_text": self.goal_text,
            "provider_binding": self.provider_binding.to_dict(),
            "runtime_binding": self.runtime_binding.to_dict(),
            "capability_binding": self.capability_binding.to_dict(),
            "control_surface_binding": self.control_surface_binding.to_dict() if self.control_surface_binding else None,
            "environment_binding": self.environment_binding.to_dict(),
            "input_binding": self.input_binding.to_dict() if self.input_binding else None,
            "output_policy": self.output_policy.to_dict(),
            "status_tracking_policy": self.status_tracking_policy.to_dict(),
            "idempotency_policy": self.idempotency_policy.to_dict(),
            "rate_limit_policy": self.rate_limit_policy.to_dict(),
            "cancel_or_stop_plan": self.cancel_or_stop_plan.to_dict() if self.cancel_or_stop_plan else None,
            "constraints": [item.to_dict() for item in self.constraints],
            "findings": [item.to_dict() for item in self.findings],
            "plan_status": self.plan_status,
            "readiness": self.readiness,
            "static_safety_required": self.static_safety_required,
            "static_safety_checked": self.static_safety_checked,
            "preflight_required": self.preflight_required,
            "preflight_checked": self.preflight_checked,
            "human_gate_required": self.human_gate_required,
            "human_gate_opened": self.human_gate_opened,
            "authorization_required": self.authorization_required,
            "authorization_created": self.authorization_created,
            "dispatch_enabled": self.dispatch_enabled,
            "dispatched": self.dispatched,
            "external_runtime_touched": self.external_runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
            "credential_exposed": self.credential_exposed,
            "raw_secret_output": self.raw_secret_output,
        }


@dataclass(frozen=True)
class DominionControlPlanReport:
    report_id: str
    version: str
    created_at: str
    plan: DominionControlPlan | None
    findings: list[DominionControlPlanFinding]
    report_status: str
    next_required_step: str = CONTROL_PLAN_NEXT_STEP
    static_safety_checked: bool = False
    preflight_checked: bool = False
    human_gate_opened: bool = False
    authorization_created: bool = False
    dispatch_enabled: bool = False
    dispatched: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    credential_exposed: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until action candidate, inventory, capability bindings, environment policy, or Dominion policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "plan": self.plan.to_dict() if self.plan else None,
            "findings": [item.to_dict() for item in self.findings],
            "report_status": self.report_status,
            "next_required_step": self.next_required_step,
            "static_safety_checked": self.static_safety_checked,
            "preflight_checked": self.preflight_checked,
            "human_gate_opened": self.human_gate_opened,
            "authorization_created": self.authorization_created,
            "dispatch_enabled": self.dispatch_enabled,
            "dispatched": self.dispatched,
            "external_runtime_touched": self.external_runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
            "credential_exposed": self.credential_exposed,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


class DominionControlPlanSourceService:
    def __init__(self) -> None:
        self.action_candidates = DominionControlRequestCandidateService()
        self.inventory_reports = RuntimeInventoryReportService()
        self.capability_reports = CapabilityObservationDigestReportService()

    def load_action_candidate(
        self, request: DominionControlPlanCreateRequest
    ) -> tuple[DominionControlRequestCandidateReport, ExternalActionCandidate | None]:
        source_request = DominionControlRequestCreateRequest(
            goal_text="observe status",
            capability_candidate_ids=[item for item in [request.action_candidate_id] if item.startswith("external_capability_candidate:")],
            requested_action_verb=None,
            requested_inputs={},
            source_refs=request.source_refs,
        )
        report = self.action_candidates.create_request_and_candidate(source_request)
        candidate = report.action_candidate
        if candidate and request.action_candidate_id not in {candidate.action_candidate_id, "external_action_candidate:v0.23.3"}:
            candidate = None
        if candidate and _source_flag(request.source_refs, "action_candidate_dispatched"):
            candidate = replace(candidate, **{"dispatch_enabled": True, "dispatched": True})
        if candidate and candidate.input_draft and _source_flag(request.source_refs, "required_input_missing"):
            candidate = replace(
                candidate,
                input_draft=replace(candidate.input_draft, missing_required_fields=["target_ref"], input_status="incomplete"),
            )
        return report, candidate

    def load_runtime_inventory(self, inventory_report_id: str | None = None) -> RuntimeInventoryReport:
        return self.inventory_reports.build_report()

    def load_capability_report(self, capability_report_id: str | None = None) -> CapabilityObservationDigestReport:
        return self.capability_reports.build_report()


class ProviderBindingService:
    def bind_provider(
        self,
        request: DominionControlPlanCreateRequest,
        action_candidate: ExternalActionCandidate | None,
        inventory: RuntimeInventoryReport,
    ) -> ProviderBinding:
        target_provider = request.requested_provider_ref_id or _candidate_provider(action_candidate)
        providers = inventory.snapshot.providers
        provider = _find_by_attr(providers, "provider_ref_id", target_provider) if target_provider else (providers[0] if providers else None)
        if provider is None:
            return ProviderBinding(
                "provider_binding:v0.23.4:missing",
                target_provider,
                "unknown",
                None,
                "none",
                "missing",
                evidence_refs=[{"missing_provider": True}],
            )
        return ProviderBinding(
            binding_id=f"provider_binding:v0.23.4:{provider.provider_ref_id}",
            provider_ref_id=provider.provider_ref_id,
            provider_type=provider.provider_type,
            vendor_name=provider.vendor_name,
            adapter_status=provider.adapter_status,
            binding_status="blocked" if provider.provider_specific_logic_in_core else "bound",
            provider_specific_logic_in_core=provider.provider_specific_logic_in_core,
            provider_api_call_performed=False,
            evidence_refs=[{"runtime_inventory_read_only": True}],
        )


class RuntimeBindingService:
    def bind_runtime(
        self,
        request: DominionControlPlanCreateRequest,
        action_candidate: ExternalActionCandidate | None,
        inventory: RuntimeInventoryReport,
    ) -> RuntimeBinding:
        target_runtime = request.requested_runtime_id or _candidate_runtime(action_candidate)
        runtimes = inventory.snapshot.runtimes
        runtime = _find_by_attr(runtimes, "runtime_id", target_runtime) if target_runtime else (runtimes[0] if runtimes else None)
        if runtime is None:
            return RuntimeBinding(
                "runtime_binding:v0.23.4:missing",
                target_runtime,
                "unknown",
                None,
                request.requested_environment or "unknown",
                "unknown",
                "missing",
                False,
                False,
                evidence_refs=[{"missing_runtime": True}],
            )
        environment = request.requested_environment or runtime.environment
        return RuntimeBinding(
            binding_id=f"runtime_binding:v0.23.4:{runtime.runtime_id}",
            runtime_id=runtime.runtime_id,
            runtime_type=runtime.runtime_type,
            runtime_name=runtime.runtime_name,
            environment=environment if environment in ENVIRONMENTS else "unknown",
            runtime_status=runtime.runtime_status,
            binding_status="bound",
            production_impacting=environment == "production" or runtime.production_impacting,
            credential_sensitive=bool(runtime.credential_boundary_ref and runtime.credential_boundary_ref.get("credential_boundary_id") != "credential:none"),
            runtime_touched=False,
            evidence_refs=[{"runtime_inventory_read_only": True}],
        )


class CapabilityBindingService:
    def bind_capability(
        self,
        action_candidate: ExternalActionCandidate | None,
        capability_report: CapabilityObservationDigestReport,
    ) -> CapabilityBinding:
        candidate_id = _candidate_capability(action_candidate)
        candidates = capability_report.snapshot.candidates
        candidate = _find_by_attr(candidates, "candidate_id", candidate_id) if candidate_id else (candidates[0] if candidates else None)
        if candidate is None:
            return CapabilityBinding(
                "capability_binding:v0.23.4:missing",
                candidate_id,
                None,
                "unknown",
                [],
                None,
                None,
                "missing",
                evidence_refs=[{"missing_capability": True}],
            )
        return CapabilityBinding(
            binding_id=f"capability_binding:v0.23.4:{candidate.candidate_id}",
            capability_candidate_id=candidate.candidate_id,
            capability_name=candidate.capability_name,
            normalized_capability_type=candidate.normalized_capability_type,
            action_verbs=[item.to_dict() for item in candidate.action_verbs],
            risk_profile_ref=candidate.risk_profile_ref,
            boundary_ref=candidate.boundary_ref,
            binding_status="bound",
            dispatch_enabled=False,
            evidence_refs=[{"capability_report_read_only": True}],
        )


class ControlSurfaceBindingService:
    def bind_control_surface(
        self,
        request: DominionControlPlanCreateRequest,
        provider_binding: ProviderBinding,
        runtime_binding: RuntimeBinding,
        inventory: RuntimeInventoryReport,
    ) -> ControlSurfaceBinding:
        surface_id = request.requested_control_surface_id
        surfaces = inventory.snapshot.control_surfaces
        if not surface_id and runtime_binding.runtime_id:
            runtime_surfaces = [item for item in surfaces if item.runtime_id == runtime_binding.runtime_id]
            surface = runtime_surfaces[0] if runtime_surfaces else (surfaces[0] if surfaces else None)
        else:
            surface = _find_by_attr(surfaces, "control_surface_id", surface_id) if surface_id else None
        if surface is None:
            return ControlSurfaceBinding(
                "control_surface_binding:v0.23.4:missing",
                surface_id,
                "unknown",
                provider_binding.provider_ref_id,
                runtime_binding.runtime_id,
                False,
                False,
                False,
                False,
                False,
                "missing",
                evidence_refs=[{"missing_control_surface": True}],
            )
        return ControlSurfaceBinding(
            binding_id=f"control_surface_binding:v0.23.4:{surface.control_surface_id}",
            control_surface_id=surface.control_surface_id,
            surface_type=surface.surface_type,
            provider_ref_id=surface.provider_ref_id,
            runtime_id=surface.runtime_id,
            read_only_supported=surface.read_only_supported,
            dispatch_supported=surface.dispatch_supported,
            status_tracking_supported=surface.status_tracking_supported,
            output_fetch_supported=surface.output_fetch_supported,
            cancel_or_stop_supported=surface.cancel_or_stop_supported,
            binding_status="bound",
            dispatch_enabled=False,
            provider_api_call_performed=False,
            evidence_refs=[{"runtime_inventory_read_only": True}],
        )


class EnvironmentBindingService:
    def bind_environment(self, request: DominionControlPlanCreateRequest, runtime_binding: RuntimeBinding) -> EnvironmentBinding:
        environment = request.requested_environment or runtime_binding.environment or "unknown"
        environment = environment if environment in ENVIRONMENTS else "unknown"
        production = environment == "production" or runtime_binding.production_impacting
        return EnvironmentBinding(
            binding_id=f"environment_binding:v0.23.4:{environment}",
            environment=environment,
            production_impacting=production,
            requires_human_gate_for_dispatch=production,
            requires_strong_gate_for_mutation=production or runtime_binding.credential_sensitive,
            allowed_for_planning=True,
            dispatch_allowed=False,
            binding_status="unknown" if environment == "unknown" else "bound",
            evidence_refs=[{"metadata_only": True}],
        )


class DominionInputBindingService:
    def bind_input(
        self,
        request: DominionControlPlanCreateRequest,
        action_candidate: ExternalActionCandidate | None,
        capability_binding: CapabilityBinding,
    ) -> DominionInputBinding | None:
        if action_candidate is None:
            return None
        draft = action_candidate.input_draft
        schema_ref = draft.schema_ref if draft else None
        base_fields = draft.provided_fields if draft else {}
        bound_fields = dict(base_fields) | _clean(request.requested_input_overrides)
        missing = list(draft.missing_required_fields if draft else [])
        sensitive = list(draft.sensitive_fields_present if draft else [])
        sensitive.extend(field for field in request.requested_input_overrides if "credential" in field.lower() or "token" in field.lower())
        credential_values = bool(draft and draft.credential_values_present) or _has_secret(request.requested_input_overrides)
        status = "blocked" if credential_values else ("incomplete" if missing else "complete")
        return DominionInputBinding(
            input_binding_id=f"dominion_input_binding:v0.23.4:{action_candidate.action_candidate_id}",
            action_candidate_id=action_candidate.action_candidate_id,
            input_schema_ref=schema_ref,
            bound_fields=bound_fields,
            missing_required_fields=missing,
            sensitive_fields_present=sorted(set(sensitive)),
            credential_values_present=credential_values,
            raw_secret_output=False,
            binding_status=status,
            evidence_refs=[{"draft_binding_only": True}],
        )


class DominionOutputPolicyService:
    def build_output_policy(
        self, capability_binding: CapabilityBinding, action_candidate: ExternalActionCandidate | None
    ) -> DominionOutputPolicy:
        return DominionOutputPolicy(
            output_policy_id=f"dominion_output_policy:v0.23.4:{capability_binding.capability_candidate_id or 'unknown'}",
            output_schema_ref={"source": "capability_binding"} if capability_binding.binding_status == "bound" else None,
            capture_required=True,
            redaction_required=True,
            raw_output_allowed=False,
            output_fetch_required=True,
            outcome_mapping_required=True,
            evidence_refs=[{"policy_only": True}],
        )


class DominionStatusTrackingPolicyService:
    def build_status_policy(
        self, control_surface_binding: ControlSurfaceBinding, capability_binding: CapabilityBinding
    ) -> DominionStatusTrackingPolicy:
        return DominionStatusTrackingPolicy(
            status_policy_id=f"dominion_status_tracking_policy:v0.23.4:{control_surface_binding.control_surface_id or 'unknown'}",
            status_tracking_required=True,
            polling_supported=control_surface_binding.status_tracking_supported,
            callback_supported=None,
            terminal_statuses=["succeeded", "failed", "cancelled"],
            unknown_status_allowed=False,
            status_tracking_owner="future_provider_adapter",
            evidence_refs=[{"policy_only": True}],
        )


class DominionIdempotencyPolicyService:
    def build_idempotency_policy(
        self, action_candidate: ExternalActionCandidate | None, environment_binding: EnvironmentBinding
    ) -> DominionIdempotencyPolicy:
        required = environment_binding.production_impacting or _candidate_is_mutating(action_candidate)
        return DominionIdempotencyPolicy(
            idempotency_policy_id="dominion_idempotency_policy:v0.23.4",
            idempotency_required=required,
            idempotency_key=None,
            duplicate_dispatch_protection_required=required,
            duplicate_dispatch_protection_available=None,
            evidence_refs=[{"policy_only": True}],
        )


class DominionRateLimitPolicyService:
    def build_rate_limit_policy(
        self,
        provider_binding: ProviderBinding,
        runtime_binding: RuntimeBinding,
        environment_binding: EnvironmentBinding,
    ) -> DominionRateLimitPolicy:
        required = environment_binding.production_impacting or runtime_binding.runtime_type not in {"local_runtime", "unknown"}
        return DominionRateLimitPolicy(
            rate_limit_policy_id="dominion_rate_limit_policy:v0.23.4",
            rate_limit_required=required,
            max_dispatches_per_window=None,
            concurrency_limit_required=required,
            max_concurrent_runs=None,
            burst_allowed=False,
            evidence_refs=[{"policy_only": True}],
        )


class DominionCancelOrStopPlanService:
    def build_cancel_or_stop_plan(
        self, control_surface_binding: ControlSurfaceBinding, capability_binding: CapabilityBinding, action_candidate: ExternalActionCandidate | None
    ) -> DominionCancelOrStopPlanDescriptor:
        required = _candidate_is_mutating(action_candidate)
        supported = control_surface_binding.cancel_or_stop_supported
        return DominionCancelOrStopPlanDescriptor(
            cancel_plan_id="dominion_cancel_or_stop_plan:v0.23.4",
            action_candidate_id=action_candidate.action_candidate_id if action_candidate else "",
            cancel_or_stop_required=required,
            cancel_supported=supported,
            stop_supported=supported,
            manual_intervention_required=required and not supported,
            cancel_surface_ref={"control_surface_id": control_surface_binding.control_surface_id} if supported else None,
            stop_surface_ref={"control_surface_id": control_surface_binding.control_surface_id} if supported else None,
            plan_status="available" if required and supported else ("unavailable" if required else "not_required"),
            execution_enabled=False,
            executed=False,
            evidence_refs=[{"descriptor_only": True}],
        )


class DominionControlPlanConstraintService:
    def build_constraints(self, request: DominionControlPlanCreateRequest) -> list[DominionControlPlanConstraint]:
        constraint_names = [
            "no_dispatch_in_v0_23_4",
            "no_preflight_in_v0_23_4",
            "no_static_safety_pass_in_v0_23_4",
            "no_human_gate_in_v0_23_4",
            "no_authorization_in_v0_23_4",
            "requires_static_safety_v0_23_5",
            "requires_preflight_v0_23_6",
            "requires_dominion_gate_v0_23_7",
            "requires_bounded_dispatch_v0_23_8",
            "requires_status_tracking_v0_23_8",
            "requires_outcome_record_v0_23_8",
            "no_credential_value_materialization",
            "provider_adapter_future_track",
        ]
        return [
            DominionControlPlanConstraint(
                constraint_id=f"dominion_control_plan_constraint:{name}",
                constraint_type=name,
                description=name.replace("_", " "),
                severity="hard_block" if name.startswith("no_") else "info",
                source_ref={"policy": CONTROL_PLAN_VERSION},
            )
            for name in [*constraint_names, *request.constraints]
        ]


class DominionControlPlanFindingService:
    def build_findings(
        self,
        *,
        request: DominionControlPlanCreateRequest,
        source_report: DominionControlRequestCandidateReport,
        action_candidate: ExternalActionCandidate | None,
        provider_binding: ProviderBinding,
        runtime_binding: RuntimeBinding,
        capability_binding: CapabilityBinding,
        control_surface_binding: ControlSurfaceBinding,
        environment_binding: EnvironmentBinding,
        input_binding: DominionInputBinding | None,
        output_policy: DominionOutputPolicy,
        status_policy: DominionStatusTrackingPolicy,
        idempotency_policy: DominionIdempotencyPolicy,
        rate_limit_policy: DominionRateLimitPolicy,
        cancel_or_stop_plan: DominionCancelOrStopPlanDescriptor,
        constraints: list[DominionControlPlanConstraint],
    ) -> list[DominionControlPlanFinding]:
        findings: list[DominionControlPlanFinding] = []
        if _has_secret(request.requested_input_overrides):
            findings.append(_binding_finding("critical", "credential_value_detected", request.to_dict()))
        if action_candidate is None:
            findings.append(_finding("warning", "missing_action_candidate"))
        elif action_candidate.dispatched:
            findings.append(_finding("error", "candidate_already_dispatched"))
        if source_report.report_status == "blocked":
            findings.append(_finding("error", "action_candidate_blocked"))
        if provider_binding.binding_status != "bound":
            findings.append(_binding_finding("warning", "provider_binding_missing", provider_binding.to_dict()))
        if runtime_binding.binding_status != "bound":
            findings.append(_binding_finding("warning", "runtime_binding_missing", runtime_binding.to_dict()))
        if capability_binding.binding_status != "bound":
            findings.append(_binding_finding("warning", "capability_binding_missing", capability_binding.to_dict()))
        if control_surface_binding.binding_status != "bound":
            findings.append(_binding_finding("warning", "control_surface_missing", control_surface_binding.to_dict()))
        if environment_binding.environment == "unknown":
            findings.append(_binding_finding("warning", "environment_unknown", environment_binding.to_dict()))
        if environment_binding.production_impacting:
            findings.append(_binding_finding("warning", "production_environment_bound", environment_binding.to_dict()))
        if input_binding and input_binding.missing_required_fields:
            findings.append(_binding_finding("warning", "input_required_field_missing", input_binding.to_dict()))
        if input_binding and input_binding.credential_values_present:
            findings.append(_binding_finding("critical", "credential_value_detected", input_binding.to_dict()))
        if output_policy is None:
            findings.append(_finding("error", "output_policy_missing"))
        if status_policy.status_tracking_required and status_policy.polling_supported is False and _candidate_is_mutating(action_candidate):
            findings.append(_finding("warning", "status_tracking_missing"))
        if idempotency_policy.idempotency_required and idempotency_policy.idempotency_key is None:
            findings.append(_finding("warning", "idempotency_missing"))
        if rate_limit_policy.rate_limit_required and rate_limit_policy.max_dispatches_per_window is None:
            findings.append(_finding("warning", "rate_limit_missing"))
        if cancel_or_stop_plan.cancel_or_stop_required and cancel_or_stop_plan.plan_status == "unavailable":
            findings.append(_finding("warning", "cancel_or_stop_plan_missing"))
        if _candidate_requires_adapter(action_candidate):
            findings.append(_finding("warning", "provider_adapter_required"))
        if provider_binding.provider_specific_logic_in_core:
            findings.append(_binding_finding("error", "provider_specific_logic_in_core", provider_binding.to_dict()))
        if capability_binding.dispatch_enabled or control_surface_binding.dispatch_enabled:
            findings.append(_finding("error", "dispatch_enabled_too_early"))
        if provider_binding.provider_api_call_performed or control_surface_binding.provider_api_call_performed:
            findings.append(_finding("critical", "provider_api_call_performed"))
        if runtime_binding.runtime_touched:
            findings.append(_finding("critical", "external_runtime_touched"))
        findings.extend(_source_text_findings(request))
        findings.extend(_constraint_findings(constraints))
        if not findings:
            findings.append(_finding("info", "ok"))
        return findings


class DominionControlPlanService:
    def __init__(self) -> None:
        self.sources = DominionControlPlanSourceService()
        self.provider_binding = ProviderBindingService()
        self.runtime_binding = RuntimeBindingService()
        self.capability_binding = CapabilityBindingService()
        self.control_surface_binding = ControlSurfaceBindingService()
        self.environment_binding = EnvironmentBindingService()
        self.input_binding = DominionInputBindingService()
        self.output_policy = DominionOutputPolicyService()
        self.status_policy = DominionStatusTrackingPolicyService()
        self.idempotency_policy = DominionIdempotencyPolicyService()
        self.rate_limit_policy = DominionRateLimitPolicyService()
        self.cancel_or_stop_plan = DominionCancelOrStopPlanService()
        self.constraints = DominionControlPlanConstraintService()
        self.findings = DominionControlPlanFindingService()

    def create_control_plan(self, request: DominionControlPlanCreateRequest | None = None) -> DominionControlPlanReport:
        request = request or DominionControlPlanCreateRequest()
        created_at = _now()
        source_report, action_candidate = self.sources.load_action_candidate(request)
        inventory = self.sources.load_runtime_inventory(request.inventory_report_id)
        capability_report = self.sources.load_capability_report(request.capability_report_id)
        provider_binding = self.provider_binding.bind_provider(request, action_candidate, inventory)
        runtime_binding = self.runtime_binding.bind_runtime(request, action_candidate, inventory)
        capability_binding = self.capability_binding.bind_capability(action_candidate, capability_report)
        control_surface_binding = self.control_surface_binding.bind_control_surface(
            request,
            provider_binding,
            runtime_binding,
            inventory,
        )
        environment_binding = self.environment_binding.bind_environment(request, runtime_binding)
        input_binding = self.input_binding.bind_input(request, action_candidate, capability_binding)
        output_policy = self.output_policy.build_output_policy(capability_binding, action_candidate)
        status_policy = self.status_policy.build_status_policy(control_surface_binding, capability_binding)
        idempotency_policy = self.idempotency_policy.build_idempotency_policy(action_candidate, environment_binding)
        rate_limit_policy = self.rate_limit_policy.build_rate_limit_policy(provider_binding, runtime_binding, environment_binding)
        cancel_or_stop_plan = self.cancel_or_stop_plan.build_cancel_or_stop_plan(
            control_surface_binding,
            capability_binding,
            action_candidate,
        )
        constraints = self.constraints.build_constraints(request)
        findings = self.findings.build_findings(
            request=request,
            source_report=source_report,
            action_candidate=action_candidate,
            provider_binding=provider_binding,
            runtime_binding=runtime_binding,
            capability_binding=capability_binding,
            control_surface_binding=control_surface_binding,
            environment_binding=environment_binding,
            input_binding=input_binding,
            output_policy=output_policy,
            status_policy=status_policy,
            idempotency_policy=idempotency_policy,
            rate_limit_policy=rate_limit_policy,
            cancel_or_stop_plan=cancel_or_stop_plan,
            constraints=constraints,
        )
        plan_status, readiness = _plan_status(findings, request)
        plan = None
        if action_candidate is not None:
            plan = DominionControlPlan(
                plan_id="dominion_control_plan:v0.23.4",
                action_candidate_id=action_candidate.action_candidate_id,
                request_id=request.request_id or action_candidate.request_id,
                created_at=created_at,
                title=action_candidate.title,
                goal_text=action_candidate.goal_text,
                provider_binding=provider_binding,
                runtime_binding=runtime_binding,
                capability_binding=capability_binding,
                control_surface_binding=control_surface_binding,
                environment_binding=environment_binding,
                input_binding=input_binding,
                output_policy=output_policy,
                status_tracking_policy=status_policy,
                idempotency_policy=idempotency_policy,
                rate_limit_policy=rate_limit_policy,
                cancel_or_stop_plan=cancel_or_stop_plan,
                constraints=constraints,
                findings=findings,
                plan_status=plan_status,
                readiness=readiness,
                credential_exposed=bool(input_binding and input_binding.credential_values_present),
            )
        return DominionControlPlanReport(
            report_id="dominion_control_plan_report:v0.23.4",
            version=CONTROL_PLAN_VERSION,
            created_at=created_at,
            plan=plan,
            findings=findings,
            report_status=plan_status,
            credential_exposed=bool(plan and plan.credential_exposed),
            limitations=[
                "v0.23.4 creates plan-only control plans and metadata bindings.",
                "Static safety, preflight, human gate, authorization, dispatch, provider API calls, runtime touch, status tracking execution, output fetch, and outcome records are not implemented.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider API calls, runtime touch, dispatch, preflight, gate, authorization, credential output, or vendor-specific core adapter logic is introduced.",
                "Withdraw if v0.23.x is described as Self-Execution Safety or GrowthKernel becomes an active runtime dependency.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": CONTROL_PLAN_VERSION,
            "layer": CONTROL_PLAN_LAYER,
            "subject": CONTROL_PLAN_SUBJECT,
            "principles": [
                "control plan is not dispatch",
                "target binding is not runtime touch",
                "input binding is not credential materialization",
                "control plan is not preflight",
                "control plan is not authorization",
                "control plan is not execution",
            ],
            "safety_boundary": {
                "static_safety_checked": False,
                "preflight_checked": False,
                "human_gate_opened": False,
                "authorization_created": False,
                "dispatch_enabled": False,
                "dispatched": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
            },
            "next_step": CONTROL_PLAN_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": CONTROL_PLAN_STATE,
            "version": CONTROL_PLAN_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionRuntimeInventoryState",
                "ExternalCapabilityCandidateState",
                "ExternalActionCandidateState",
                "CapabilityRiskProfileState",
                "CapabilityBoundaryState",
            ],
            "target_read_models": [
                "DominionControlPlanState",
                "ProviderBindingState",
                "RuntimeBindingState",
                "CapabilityBindingState",
                "EnvironmentBindingState",
                "DominionPlanPolicyState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: DominionControlPlanReport | None = None, section: str = "summary") -> str:
        report = report or self.create_control_plan()
        plan = report.plan
        plan_id = plan.plan_id if plan else ""
        action_candidate_id = plan.action_candidate_id if plan else ""
        provider_status = plan.provider_binding.binding_status if plan else "missing"
        runtime_status = plan.runtime_binding.binding_status if plan else "missing"
        capability_status = plan.capability_binding.binding_status if plan else "missing"
        environment = plan.environment_binding.environment if plan else "unknown"
        lines = [
            "Dominion Control Plan & Target Binding",
            f"version={report.version}",
            f"layer={CONTROL_PLAN_LAYER}",
            f"status={report.report_status}",
            f"plan_id={plan_id}",
            f"action_candidate_id={action_candidate_id}",
            f"plan_status={plan.plan_status if plan else report.report_status}",
            f"readiness={plan.readiness if plan else 'needs_more_input'}",
            f"provider_binding_status={provider_status}",
            f"runtime_binding_status={runtime_status}",
            f"capability_binding_status={capability_status}",
            f"environment={environment}",
        ]
        if plan and section == "bindings":
            lines.extend(
                [
                    f"control_surface_binding_status={plan.control_surface_binding.binding_status if plan.control_surface_binding else 'missing'}",
                    f"input_binding_status={plan.input_binding.binding_status if plan.input_binding else 'missing'}",
                    f"environment_binding_status={plan.environment_binding.binding_status}",
                ]
            )
        if plan and section == "policies":
            lines.extend(
                [
                    f"output_redaction_required={str(plan.output_policy.redaction_required).lower()}",
                    f"raw_output_allowed={str(plan.output_policy.raw_output_allowed).lower()}",
                    f"status_tracking_required={str(plan.status_tracking_policy.status_tracking_required).lower()}",
                    f"idempotency_required={str(plan.idempotency_policy.idempotency_required).lower()}",
                    f"rate_limit_required={str(plan.rate_limit_policy.rate_limit_required).lower()}",
                    f"cancel_or_stop_execution_enabled={str(plan.cancel_or_stop_plan.execution_enabled if plan.cancel_or_stop_plan else False).lower()}",
                ]
            )
        if section == "findings":
            lines.extend(f"- finding={item.finding_type} severity={item.severity}" for item in report.findings)
        lines.extend(
            [
                f"static_safety_checked={str(report.static_safety_checked).lower()}",
                f"preflight_checked={str(report.preflight_checked).lower()}",
                f"human_gate_opened={str(report.human_gate_opened).lower()}",
                f"authorization_created={str(report.authorization_created).lower()}",
                f"dispatch_enabled={str(report.dispatch_enabled).lower()}",
                f"dispatched={str(report.dispatched).lower()}",
                f"external_runtime_touched={str(report.external_runtime_touched).lower()}",
                f"provider_api_call_performed={str(report.provider_api_call_performed).lower()}",
                f"credential_exposed={str(report.credential_exposed).lower()}",
                f"next_required_step={report.next_required_step}",
                "raw_secrets_printed=False",
                "private_full_paths_printed=False",
            ]
        )
        return "\n".join(lines)


def _find_by_attr(items: list[Any], attr: str, value: str | None) -> Any | None:
    if value is None:
        return None
    return next((item for item in items if getattr(item, attr, None) == value), None)


def _candidate_provider(action_candidate: ExternalActionCandidate | None) -> str | None:
    if not action_candidate or not action_candidate.target_refs:
        return None
    return action_candidate.target_refs[0].provider_ref_id


def _candidate_runtime(action_candidate: ExternalActionCandidate | None) -> str | None:
    if not action_candidate or not action_candidate.target_refs:
        return None
    return action_candidate.target_refs[0].runtime_id


def _candidate_capability(action_candidate: ExternalActionCandidate | None) -> str | None:
    if not action_candidate or not action_candidate.capability_candidate_refs:
        return None
    return action_candidate.capability_candidate_refs[0].get("candidate_id")


def _candidate_is_mutating(action_candidate: ExternalActionCandidate | None) -> bool:
    if not action_candidate:
        return False
    return action_candidate.intent.risk_class not in {"read_only", "unknown"}


def _candidate_requires_adapter(action_candidate: ExternalActionCandidate | None) -> bool:
    return bool(action_candidate and action_candidate.preliminary_risk.provider_adapter_required)


def _finding(severity: str, finding_type: str) -> DominionControlPlanFinding:
    return DominionControlPlanFinding(
        finding_id=f"dominion_control_plan_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=finding_type.replace("_", " "),
        evidence_refs=[{"policy": "v0.23.4_plan_only"}],
        withdrawal_condition="Withdraw this finding if sanitized action candidate, inventory, capability, or policy evidence changes.",
    )


def _binding_finding(severity: str, finding_type: str, binding_ref: dict[str, Any]) -> DominionControlPlanFinding:
    finding = _finding(severity, finding_type)
    return replace(finding, binding_ref=binding_ref)


def _source_text_findings(request: DominionControlPlanCreateRequest) -> list[DominionControlPlanFinding]:
    text = " ".join([*request.constraints, *(str(item) for item in request.source_refs)]).lower()
    findings: list[DominionControlPlanFinding] = []
    if "self_execution" in text or "self-execution safety" in text:
        findings.append(_finding("error", "self_execution_legacy_detected"))
    if "growthkernel dependency" in text or "requires growthkernel" in text:
        findings.append(_finding("error", "growthkernel_dependency_detected"))
    if "vendor hardcoding" in text:
        findings.append(_finding("critical", "vendor_hardcoding_detected"))
    if "provider api call performed" in text:
        findings.append(_finding("critical", "provider_api_call_performed"))
    if "external runtime touched" in text:
        findings.append(_finding("critical", "external_runtime_touched"))
    if "dispatch enabled too early" in text:
        findings.append(_finding("error", "dispatch_enabled_too_early"))
    return findings


def _constraint_findings(constraints: list[DominionControlPlanConstraint]) -> list[DominionControlPlanFinding]:
    types = {item.constraint_type for item in constraints}
    findings: list[DominionControlPlanFinding] = []
    if "static_safety_checked" in types:
        findings.append(_finding("error", "static_safety_not_performed"))
    if "preflight_checked" in types:
        findings.append(_finding("error", "preflight_not_performed"))
    if "human_gate_opened" in types:
        findings.append(_finding("error", "human_gate_not_opened"))
    if "authorization_created" in types:
        findings.append(_finding("error", "authorization_not_created"))
    return findings


def _plan_status(findings: list[DominionControlPlanFinding], request: DominionControlPlanCreateRequest) -> tuple[str, str]:
    types = {item.finding_type for item in findings}
    severities = {item.severity for item in findings}
    if "critical" in severities:
        return "blocked", "blocked"
    if "error" in severities:
        return "failed", "blocked"
    if "missing_action_candidate" in types or "input_required_field_missing" in types or "environment_unknown" in types:
        return "needs_more_input", "needs_more_input"
    if "provider_adapter_required" in types and request.allow_no_action and _source_flag(request.source_refs, "no_safe_provider_path"):
        return "no_action", "blocked"
    return "planned", "ready_for_static_safety"
