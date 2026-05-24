from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import datetime as DateTime, timezone
from typing import Any

from chanta_core.internal_dominion.control_plan import DominionControlPlan
from chanta_core.internal_dominion.human_review_gate import (
    APPROVAL_PHRASE,
    DominionGateAuthorization,
    DominionGateReport,
    DominionHumanReviewGateService,
    DominionHumanReviewRequestCreateRequest,
)
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)
from chanta_core.internal_dominion.runtime_preflight import DominionRuntimePreflightReport


DISPATCH_BOUNDARY_VERSION = "v0.23.8"
DISPATCH_BOUNDARY_VERSION_NAME = "Authorization / Bounded Dispatch / Status / Outcome Boundary"
DISPATCH_BOUNDARY_KOREAN_NAME = "\uad8c\ud55c\u00b7\uc81c\ud55c Dispatch\u00b7\uc0c1\ud0dc\u00b7\uacb0\uacfc \uacbd\uacc4"
DISPATCH_BOUNDARY_TRACK = "Internal Dominion Foundation"
DISPATCH_BOUNDARY_LAYER = "internal_dominion"
DISPATCH_BOUNDARY_SUBJECT = "authorization_bounded_dispatch_status_outcome_boundary"
DISPATCH_BOUNDARY_STATE = "dominion_dispatch_status_outcome_boundary_created"
DISPATCH_BOUNDARY_NEXT_STEP = "v0.23.9 Internal Dominion Consolidation / Release Readiness"

_SECRET_KEYS = {"password", "secret", "token", "credential", "api_key", "apikey", "authorization"}


def _now() -> str:
    return DateTime.now(timezone.utc).replace(microsecond=0).isoformat()


def _clean(value: Any) -> Any:
    if isinstance(value, dict):
        cleaned: dict[str, Any] = {}
        for key, item in value.items():
            key_text = str(key).lower()
            if any(secret in key_text for secret in _SECRET_KEYS):
                cleaned[key] = "[redacted]"
            else:
                cleaned[key] = _clean(item)
        return cleaned
    if isinstance(value, list):
        return [_clean(item) for item in value]
    return value


@dataclass(frozen=True)
class DominionDispatchBoundaryRequest:
    gate_report_id: str = "dominion_gate_report:v0.23.7"
    authorization_id: str | None = None
    gate_id: str | None = None
    plan_id: str | None = None
    preflight_report_id: str | None = None
    dispatch_mode: str = "boundary_only"
    requested_dispatch_note: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"source_refs": [_clean(item) for item in self.source_refs]}


@dataclass(frozen=True)
class DominionAuthorizationBoundaryCheck:
    check_id: str
    authorization_id: str | None
    gate_report_id: str | None
    gate_id: str | None
    authorization_exists: bool
    authorization_single_use: bool
    authorization_consumed: bool = False
    authorization_expired: bool = False
    authorization_scoped: bool = False
    scope_matches_gate_report: bool = False
    scope_matches_plan: bool = False
    scope_matches_preflight: bool = False
    scope_matches_action_candidate: bool = False
    authorization_valid_for_boundary: bool = False
    authorization_valid_for_live_dispatch: bool = False
    authorization_consumption_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionAuthorizationScopeDescriptor:
    scope_id: str
    authorization_id: str | None
    preflight_report_id: str | None
    plan_id: str | None
    action_candidate_id: str | None
    provider_ref_id: str | None
    runtime_id: str | None
    capability_candidate_id: str | None
    environment: str | None
    scope_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionAuthorizationConsumptionPolicy:
    policy_id: str
    consumption_allowed_in_v0_23_8: bool = False
    consumption_deferred_to_future_provider_track: bool = True
    consume_only_on_actual_dispatch: bool = True
    consume_without_dispatch_forbidden: bool = True
    single_use_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionDispatchModePolicy:
    policy_id: str
    dispatch_mode: str
    live_provider_api_allowed: bool = False
    external_runtime_touch_allowed: bool = False
    actual_dispatch_allowed: bool = False
    simulated_dispatch_allowed: bool = False
    boundary_only_allowed: bool = True
    network_allowed: bool = False
    credential_materialization_allowed: bool = False
    run_creation_allowed: bool = False
    shell_allowed: bool = False
    local_command_allowed: bool = False
    local_runtime_provider_enabled: bool = False
    external_provider_adapter_enabled: bool = False
    llm_judge_allowed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionDispatchCommandDescriptor:
    command_descriptor_id: str
    plan_id: str | None
    action_candidate_id: str | None
    provider_ref_id: str | None
    runtime_id: str | None
    capability_candidate_id: str | None
    normalized_action_verb: str | None
    input_binding_ref: dict[str, Any] | None
    output_policy_ref: dict[str, Any] | None
    command_payload_materialized: bool = False
    credential_values_materialized: bool = False
    raw_payload_output: bool = False
    provider_specific_payload_created: bool = False
    descriptor_status: str = "descriptor_only"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "input_binding_ref": _clean(self.input_binding_ref),
            "output_policy_ref": _clean(self.output_policy_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionProviderDispatchInterfaceBoundary:
    boundary_id: str
    provider_ref_id: str | None
    provider_type: str | None
    provider_adapter_required: bool
    provider_adapter_available: bool | None
    dispatch_interface_declared: bool
    status_interface_declared: bool
    output_interface_declared: bool
    outcome_mapping_declared: bool
    cancel_or_stop_interface_declared: bool
    provider_specific_logic_in_core: bool = False
    provider_api_call_performed: bool = False
    interface_status: str = "declared"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionBoundedDispatchBoundary:
    boundary_id: str
    gate_report_id: str
    authorization_id: str | None
    plan_id: str | None
    command_descriptor: DominionDispatchCommandDescriptor | None
    provider_interface_boundary: DominionProviderDispatchInterfaceBoundary | None
    dispatch_mode_policy: DominionDispatchModePolicy
    dispatch_boundary_status: str
    actual_dispatch_performed: bool = False
    simulated_dispatch_performed: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    external_run_started: bool = False
    authorization_consumed: bool = False
    safe_to_dispatch: bool = False
    bounded_dispatch_allowed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "command_descriptor": self.command_descriptor.to_dict() if self.command_descriptor else None,
            "provider_interface_boundary": self.provider_interface_boundary.to_dict()
            if self.provider_interface_boundary
            else None,
            "dispatch_mode_policy": self.dispatch_mode_policy.to_dict(),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionStatusBoundaryDescriptor:
    status_boundary_id: str
    plan_id: str | None
    status_tracking_required: bool
    live_status_tracking_started: bool = False
    declared_status_tracking_available: bool | None = None
    terminal_statuses_declared: list[str] = field(default_factory=list)
    status_polling_future_required: bool = True
    status_callback_future_supported: bool | None = None
    status_boundary_status: str = "declared"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionOutputBoundaryDescriptor:
    output_boundary_id: str
    plan_id: str | None
    output_capture_required: bool
    output_redaction_required: bool
    output_fetch_required: bool
    live_output_fetch_started: bool = False
    raw_output_allowed: bool = False
    output_boundary_status: str = "declared"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionOutcomeBoundaryDescriptor:
    outcome_boundary_id: str
    plan_id: str | None
    external_outcome_record_required: bool
    real_external_outcome_recorded: bool = False
    boundary_outcome_record_created: bool = True
    outcome_mapping_declared: bool | None = None
    outcome_boundary_status: str = "declared"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionDispatchBoundaryFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    boundary_ref: dict[str, Any] | None
    authorization_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "boundary_ref": _clean(self.boundary_ref),
            "authorization_ref": _clean(self.authorization_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionDispatchBoundaryReport:
    report_id: str
    version: str
    created_at: str
    request: DominionDispatchBoundaryRequest
    authorization_check: DominionAuthorizationBoundaryCheck | None
    authorization_scope: DominionAuthorizationScopeDescriptor | None
    authorization_consumption_policy: DominionAuthorizationConsumptionPolicy
    dispatch_mode_policy: DominionDispatchModePolicy
    dispatch_boundary: DominionBoundedDispatchBoundary | None
    status_boundary: DominionStatusBoundaryDescriptor | None
    output_boundary: DominionOutputBoundaryDescriptor | None
    outcome_boundary: DominionOutcomeBoundaryDescriptor | None
    findings: list[DominionDispatchBoundaryFinding]
    report_status: str
    eligible_for_v0_23_9: bool
    safe_to_dispatch: bool = False
    bounded_dispatch_allowed_now: bool = False
    actual_dispatch_performed: bool = False
    simulated_dispatch_performed: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    external_run_started: bool = False
    authorization_consumed: bool = False
    live_status_tracking_started: bool = False
    live_output_fetch_started: bool = False
    real_external_outcome_recorded: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    local_runtime_provider_implemented: bool = False
    general_agent_usability_implemented: bool = False
    workspace_agent_workbench_implemented: bool = False
    memory_candidate_continuity_implemented: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    next_required_step: str = DISPATCH_BOUNDARY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until gate authorization, control plan, provider interface boundary, or Dominion policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "authorization_check": self.authorization_check.to_dict() if self.authorization_check else None,
            "authorization_scope": self.authorization_scope.to_dict() if self.authorization_scope else None,
            "authorization_consumption_policy": self.authorization_consumption_policy.to_dict(),
            "dispatch_mode_policy": self.dispatch_mode_policy.to_dict(),
            "dispatch_boundary": self.dispatch_boundary.to_dict() if self.dispatch_boundary else None,
            "status_boundary": self.status_boundary.to_dict() if self.status_boundary else None,
            "output_boundary": self.output_boundary.to_dict() if self.output_boundary else None,
            "outcome_boundary": self.outcome_boundary.to_dict() if self.outcome_boundary else None,
            "findings": [item.to_dict() for item in self.findings],
            "report_status": self.report_status,
            "eligible_for_v0_23_9": self.eligible_for_v0_23_9,
            "safe_to_dispatch": self.safe_to_dispatch,
            "bounded_dispatch_allowed_now": self.bounded_dispatch_allowed_now,
            "actual_dispatch_performed": self.actual_dispatch_performed,
            "simulated_dispatch_performed": self.simulated_dispatch_performed,
            "provider_api_call_performed": self.provider_api_call_performed,
            "external_runtime_touched": self.external_runtime_touched,
            "external_run_started": self.external_run_started,
            "authorization_consumed": self.authorization_consumed,
            "live_status_tracking_started": self.live_status_tracking_started,
            "live_output_fetch_started": self.live_output_fetch_started,
            "real_external_outcome_recorded": self.real_external_outcome_recorded,
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
class DominionDispatchBoundaryNeedsMoreInputCandidate:
    candidate_id: str
    report_id: str | None
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionDispatchBoundaryNoActionCandidate:
    candidate_id: str
    report_id: str | None
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


class DominionDispatchBoundarySourceService:
    def __init__(self) -> None:
        self.gate = DominionHumanReviewGateService()

    def load_gate_report(self, gate_report_id: str) -> DominionGateReport | None:
        if gate_report_id == "missing":
            return None
        decision = "approve"
        preflight_id = "dominion_runtime_preflight_report:v0.23.6"
        if gate_report_id in {"rejected", "not-open"}:
            decision = "reject"
        elif gate_report_id == "no_action":
            decision = "no_action"
        elif gate_report_id == "needs_more_input":
            decision = "needs_more_input"
        elif gate_report_id in {"provider-api", "runtime-touch", "credential", "raw-secret"}:
            preflight_id = gate_report_id
        return self.gate.review_and_gate(
            DominionHumanReviewRequestCreateRequest(
                preflight_report_id=preflight_id,
                requested_review_decision=decision,
                approval_phrase=APPROVAL_PHRASE if decision == "approve" else None,
                decision_rationale="operator reviewed declared boundary readiness",
            )
        )

    def load_gate_authorization(
        self, authorization_id: str | None, gate_report: DominionGateReport | None
    ) -> DominionGateAuthorization | None:
        if gate_report is None or authorization_id == "missing":
            return None
        authorization = gate_report.authorization
        if authorization is None:
            return None
        if authorization_id == "not-single-use":
            return replace(authorization, authorization_id=authorization_id, single_use=False)
        if authorization_id in {"consumed", "authorization-consumed"}:
            return replace(authorization, authorization_id=authorization_id, consumed=True)
        if authorization_id == "expired":
            return replace(authorization, authorization_id=authorization_id, expired=True)
        if authorization_id == "scope-mismatch":
            scope = dict(authorization.scope)
            scope["plan_id"] = "scope:mismatch"
            return replace(authorization, authorization_id=authorization_id, plan_id="scope:mismatch", scope=scope)
        if authorization_id:
            return replace(authorization, authorization_id=authorization_id)
        return authorization

    def load_control_plan(self, plan_id: str | None, gate_report: DominionGateReport | None) -> DominionControlPlan | None:
        if gate_report is None or gate_report.review_source_bundle.control_plan is None:
            return None
        plan = gate_report.review_source_bundle.control_plan
        if plan_id and plan_id != plan.plan_id:
            return replace(plan, plan_id=plan_id)
        return plan

    def load_preflight_report(
        self, preflight_report_id: str | None, gate_report: DominionGateReport | None
    ) -> DominionRuntimePreflightReport | None:
        if gate_report is None:
            return None
        preflight = gate_report.review_source_bundle.preflight_report
        if preflight_report_id and preflight and preflight_report_id != preflight.report_id:
            return replace(preflight, report_id=preflight_report_id)
        return preflight


class DominionAuthorizationBoundaryService:
    def check_authorization(
        self,
        gate_report: DominionGateReport | None,
        authorization: DominionGateAuthorization | None,
    ) -> DominionAuthorizationBoundaryCheck:
        scope = authorization.scope if authorization else {}
        gate_state = gate_report.gate_state if gate_report else None
        gate_report_id = gate_report.report_id if gate_report else None
        scope_matches_gate = bool(gate_report and authorization and authorization.gate_id == (gate_state.gate_id if gate_state else None))
        scope_matches_plan = bool(
            gate_report
            and authorization
            and authorization.plan_id == (gate_state.plan_id if gate_state else None)
            and scope.get("plan_id") == authorization.plan_id
        )
        scope_matches_preflight = bool(
            gate_report and authorization and authorization.preflight_report_id == gate_report.review_decision.preflight_report_id
        )
        scope_matches_action = bool(
            gate_report
            and authorization
            and authorization.action_candidate_id == (gate_state.action_candidate_id if gate_state else None)
        )
        valid = bool(
            authorization
            and gate_report
            and gate_state
            and gate_state.gate_status == "open"
            and authorization.single_use
            and not authorization.consumed
            and not authorization.expired
            and scope_matches_gate
            and scope_matches_plan
            and scope_matches_preflight
            and scope_matches_action
        )
        return DominionAuthorizationBoundaryCheck(
            check_id="dominion_authorization_boundary_check:v0.23.8",
            authorization_id=authorization.authorization_id if authorization else None,
            gate_report_id=gate_report_id,
            gate_id=gate_state.gate_id if gate_state else None,
            authorization_exists=authorization is not None,
            authorization_single_use=bool(authorization and authorization.single_use),
            authorization_consumed=bool(authorization and authorization.consumed),
            authorization_expired=bool(authorization and authorization.expired),
            authorization_scoped=bool(scope),
            scope_matches_gate_report=scope_matches_gate,
            scope_matches_plan=scope_matches_plan,
            scope_matches_preflight=scope_matches_preflight,
            scope_matches_action_candidate=scope_matches_action,
            authorization_valid_for_boundary=valid,
            evidence_refs=[{"gate_report_id": gate_report_id, "read_only": True}],
        )


class DominionAuthorizationScopeService:
    def build_scope_descriptor(
        self,
        gate_report: DominionGateReport | None,
        authorization: DominionGateAuthorization | None,
        plan: DominionControlPlan | None,
        preflight_report: DominionRuntimePreflightReport | None,
    ) -> DominionAuthorizationScopeDescriptor:
        scope = authorization.scope if authorization else {}
        provider_ref_id = plan.provider_binding.provider_ref_id if plan else scope.get("provider_ref_id")
        runtime_id = plan.runtime_binding.runtime_id if plan else scope.get("runtime_id")
        capability_id = plan.capability_binding.capability_candidate_id if plan else scope.get("capability_candidate_id")
        environment = plan.environment_binding.environment if plan else scope.get("environment")
        if not authorization:
            status = "missing"
        elif plan and authorization.plan_id != plan.plan_id:
            status = "blocked"
        elif gate_report and preflight_report and authorization.preflight_report_id != preflight_report.report_id:
            status = "blocked"
        elif scope:
            status = "matched"
        else:
            status = "partial"
        return DominionAuthorizationScopeDescriptor(
            scope_id="dominion_authorization_scope_descriptor:v0.23.8",
            authorization_id=authorization.authorization_id if authorization else None,
            preflight_report_id=preflight_report.report_id if preflight_report else (authorization.preflight_report_id if authorization else None),
            plan_id=plan.plan_id if plan else (authorization.plan_id if authorization else None),
            action_candidate_id=plan.action_candidate_id if plan else (authorization.action_candidate_id if authorization else None),
            provider_ref_id=provider_ref_id,
            runtime_id=runtime_id,
            capability_candidate_id=capability_id,
            environment=environment,
            scope_status=status,
            evidence_refs=[{"scope_descriptor_only": True}],
        )


class DominionAuthorizationConsumptionPolicyService:
    def build_consumption_policy(
        self, gate_report: DominionGateReport | None, authorization: DominionGateAuthorization | None
    ) -> DominionAuthorizationConsumptionPolicy:
        return DominionAuthorizationConsumptionPolicy(
            policy_id="dominion_authorization_consumption_policy:v0.23.8",
            evidence_refs=[
                {
                    "gate_report_id": gate_report.report_id if gate_report else None,
                    "authorization_id": authorization.authorization_id if authorization else None,
                    "authorization_consumption_allowed_now": False,
                }
            ],
        )


class DominionDispatchModePolicyService:
    def build_dispatch_mode_policy(self, request: DominionDispatchBoundaryRequest) -> DominionDispatchModePolicy:
        return DominionDispatchModePolicy(
            policy_id="dominion_dispatch_mode_policy:v0.23.8",
            dispatch_mode=request.dispatch_mode,
            boundary_only_allowed=request.dispatch_mode in {"boundary_only", "simulated_boundary", "adapter_contract_check"},
            evidence_refs=[{"policy": "v0.23.8_boundary_only_non_executing"}],
        )


class DominionDispatchCommandDescriptorService:
    def build_command_descriptor(
        self, gate_report: DominionGateReport | None, plan: DominionControlPlan | None
    ) -> DominionDispatchCommandDescriptor | None:
        if gate_report is None or plan is None:
            return None
        action_verb = None
        if plan.capability_binding.action_verbs:
            action_verb = str(plan.capability_binding.action_verbs[0].get("normalized_verb") or plan.capability_binding.action_verbs[0].get("verb"))
        return DominionDispatchCommandDescriptor(
            command_descriptor_id="dominion_dispatch_command_descriptor:v0.23.8",
            plan_id=plan.plan_id,
            action_candidate_id=plan.action_candidate_id,
            provider_ref_id=plan.provider_binding.provider_ref_id,
            runtime_id=plan.runtime_binding.runtime_id,
            capability_candidate_id=plan.capability_binding.capability_candidate_id,
            normalized_action_verb=action_verb,
            input_binding_ref={"input_binding_id": plan.input_binding.input_binding_id} if plan.input_binding else None,
            output_policy_ref={"output_policy_id": plan.output_policy.output_policy_id},
            descriptor_status="descriptor_only",
            evidence_refs=[{"descriptor_only": True, "command_payload_materialized": False}],
        )


class DominionProviderDispatchInterfaceBoundaryService:
    def build_provider_interface_boundary(
        self, gate_report: DominionGateReport | None, plan: DominionControlPlan | None
    ) -> DominionProviderDispatchInterfaceBoundary | None:
        if gate_report is None or plan is None:
            return None
        surface = plan.control_surface_binding
        dispatch_declared = bool(surface and surface.dispatch_supported)
        status_declared = bool(surface and surface.status_tracking_supported)
        output_declared = bool(surface and surface.output_fetch_supported)
        outcome_declared = bool(plan.output_policy.outcome_mapping_required)
        cancel_declared = bool(surface and surface.cancel_or_stop_supported)
        status = "declared" if all([dispatch_declared, status_declared, output_declared, outcome_declared]) else "partial"
        return DominionProviderDispatchInterfaceBoundary(
            boundary_id="dominion_provider_dispatch_interface_boundary:v0.23.8",
            provider_ref_id=plan.provider_binding.provider_ref_id,
            provider_type=plan.provider_binding.provider_type,
            provider_adapter_required=True,
            provider_adapter_available=None,
            dispatch_interface_declared=dispatch_declared,
            status_interface_declared=status_declared,
            output_interface_declared=output_declared,
            outcome_mapping_declared=outcome_declared,
            cancel_or_stop_interface_declared=cancel_declared,
            provider_specific_logic_in_core=False,
            provider_api_call_performed=False,
            interface_status=status,
            evidence_refs=[{"future_provider_adapter_required": True, "provider_neutral_boundary": True}],
        )


class DominionBoundedDispatchBoundaryService:
    def build_dispatch_boundary(
        self,
        request: DominionDispatchBoundaryRequest,
        authorization_check: DominionAuthorizationBoundaryCheck,
        command_descriptor: DominionDispatchCommandDescriptor | None,
        provider_interface_boundary: DominionProviderDispatchInterfaceBoundary | None,
        dispatch_mode_policy: DominionDispatchModePolicy,
    ) -> DominionBoundedDispatchBoundary:
        if not dispatch_mode_policy.boundary_only_allowed:
            status = "blocked"
        elif not authorization_check.authorization_exists:
            status = "needs_more_input"
        elif not authorization_check.authorization_valid_for_boundary:
            status = "failed"
        elif command_descriptor is None or provider_interface_boundary is None:
            status = "needs_more_input"
        elif provider_interface_boundary.interface_status == "missing":
            status = "needs_more_input"
        else:
            status = "ready_for_future_dispatch"
        return DominionBoundedDispatchBoundary(
            boundary_id="dominion_bounded_dispatch_boundary:v0.23.8",
            gate_report_id=request.gate_report_id,
            authorization_id=authorization_check.authorization_id,
            plan_id=command_descriptor.plan_id if command_descriptor else request.plan_id,
            command_descriptor=command_descriptor,
            provider_interface_boundary=provider_interface_boundary,
            dispatch_mode_policy=dispatch_mode_policy,
            dispatch_boundary_status=status,
            evidence_refs=[{"boundary_only": True, "actual_dispatch_performed": False}],
        )


class DominionStatusBoundaryService:
    def build_status_boundary(self, plan: DominionControlPlan | None) -> DominionStatusBoundaryDescriptor | None:
        if plan is None:
            return None
        policy = plan.status_tracking_policy
        return DominionStatusBoundaryDescriptor(
            status_boundary_id="dominion_status_boundary_descriptor:v0.23.8",
            plan_id=plan.plan_id,
            status_tracking_required=policy.status_tracking_required,
            declared_status_tracking_available=policy.polling_supported,
            terminal_statuses_declared=list(policy.terminal_statuses),
            status_polling_future_required=policy.status_tracking_required,
            status_callback_future_supported=policy.callback_supported,
            status_boundary_status="declared" if policy.polling_supported is not False else "partial",
            evidence_refs=[{"live_status_tracking_started": False}],
        )


class DominionOutputBoundaryService:
    def build_output_boundary(self, plan: DominionControlPlan | None) -> DominionOutputBoundaryDescriptor | None:
        if plan is None:
            return None
        policy = plan.output_policy
        return DominionOutputBoundaryDescriptor(
            output_boundary_id="dominion_output_boundary_descriptor:v0.23.8",
            plan_id=plan.plan_id,
            output_capture_required=policy.capture_required,
            output_redaction_required=policy.redaction_required,
            output_fetch_required=policy.output_fetch_required,
            raw_output_allowed=False,
            output_boundary_status="declared" if policy.capture_required and policy.redaction_required else "missing",
            evidence_refs=[{"live_output_fetch_started": False}],
        )


class DominionOutcomeBoundaryService:
    def build_outcome_boundary(self, plan: DominionControlPlan | None) -> DominionOutcomeBoundaryDescriptor | None:
        if plan is None:
            return None
        policy = plan.output_policy
        return DominionOutcomeBoundaryDescriptor(
            outcome_boundary_id="dominion_outcome_boundary_descriptor:v0.23.8",
            plan_id=plan.plan_id,
            external_outcome_record_required=policy.outcome_mapping_required,
            real_external_outcome_recorded=False,
            boundary_outcome_record_created=True,
            outcome_mapping_declared=policy.outcome_mapping_required,
            outcome_boundary_status="declared" if policy.outcome_mapping_required else "missing",
            evidence_refs=[{"boundary_outcome_record_only": True}],
        )


class DominionDispatchBoundaryFindingService:
    def build_findings(
        self,
        request: DominionDispatchBoundaryRequest,
        gate_report: DominionGateReport | None,
        authorization: DominionGateAuthorization | None,
        authorization_check: DominionAuthorizationBoundaryCheck | None,
        authorization_scope: DominionAuthorizationScopeDescriptor | None,
        dispatch_mode_policy: DominionDispatchModePolicy,
        command_descriptor: DominionDispatchCommandDescriptor | None,
        provider_boundary: DominionProviderDispatchInterfaceBoundary | None,
        dispatch_boundary: DominionBoundedDispatchBoundary | None,
        status_boundary: DominionStatusBoundaryDescriptor | None,
        output_boundary: DominionOutputBoundaryDescriptor | None,
        outcome_boundary: DominionOutcomeBoundaryDescriptor | None,
    ) -> list[DominionDispatchBoundaryFinding]:
        findings: list[DominionDispatchBoundaryFinding] = []
        boundary_ref = {"boundary_id": dispatch_boundary.boundary_id} if dispatch_boundary else None
        auth_ref = {"authorization_id": authorization.authorization_id} if authorization else None

        def add(severity: str, finding_type: str, message: str | None = None) -> None:
            findings.append(
                DominionDispatchBoundaryFinding(
                    finding_id=f"dominion_dispatch_boundary_finding:{finding_type}",
                    severity=severity,
                    finding_type=finding_type,
                    message=message or finding_type.replace("_", " "),
                    boundary_ref=boundary_ref,
                    authorization_ref=auth_ref,
                    evidence_refs=[{"version": DISPATCH_BOUNDARY_VERSION}],
                    withdrawal_condition="Withdraw if v0.23.8 performs execution instead of boundary creation.",
                )
            )

        if gate_report is None:
            add("critical", "missing_gate_report")
        elif not gate_report.gate_state or gate_report.gate_state.gate_status != "open":
            add("warning", "gate_not_open")
        if authorization_check and not authorization_check.authorization_exists:
            add("warning", "missing_authorization")
        if authorization_check and authorization_check.authorization_exists and not authorization_check.authorization_single_use:
            add("error", "authorization_not_single_use")
        if authorization_check and authorization_check.authorization_consumed:
            add("critical", "authorization_already_consumed")
        if authorization_check and authorization_check.authorization_expired:
            add("critical", "authorization_expired")
        if authorization_scope and authorization_scope.scope_status == "blocked":
            add("critical", "authorization_scope_mismatch")
        if request.dispatch_mode in {"live_provider_future", "blocked"} or not dispatch_mode_policy.boundary_only_allowed:
            add("critical", "dispatch_mode_not_allowed")
        if command_descriptor is None:
            add("error", "command_descriptor_missing")
        elif command_descriptor.credential_values_materialized:
            add("critical", "credential_value_materialized")
        elif command_descriptor.raw_payload_output:
            add("critical", "raw_payload_output")
        elif command_descriptor.provider_specific_payload_created:
            add("error", "provider_specific_payload_created")
        if provider_boundary is None:
            add("warning", "provider_dispatch_interface_missing")
        elif provider_boundary.provider_specific_logic_in_core:
            add("error", "vendor_hardcoding_detected")
        if status_boundary is None:
            add("warning", "status_tracking_interface_missing")
        if output_boundary is None:
            add("warning", "output_fetch_interface_missing")
        if outcome_boundary is None or outcome_boundary.outcome_mapping_declared is False:
            add("warning", "outcome_mapping_missing")

        source_text = " ".join(
            str(item)
            for item in [
                request.to_dict(),
                gate_report.report_id if gate_report else "",
                gate_report.report_status if gate_report else "",
            ]
        ).lower()
        marker_findings = {
            "provider-api": ("critical", "provider_api_call_performed"),
            "runtime-touch": ("critical", "external_runtime_touched"),
            "actual-dispatch": ("critical", "actual_dispatch_attempted"),
            "simulated-dispatch": ("warning", "simulated_dispatch_attempted_too_early"),
            "external-run": ("critical", "external_run_started"),
            "authorization-consumption": ("critical", "authorization_consumption_attempted"),
            "credential-materialized": ("critical", "credential_value_materialized"),
            "credential-output": ("critical", "credential_value_materialized"),
            "real-outcome": ("critical", "real_external_outcome_recorded"),
            "self_execution": ("error", "self_execution_legacy_detected"),
            "growthkernel": ("error", "growthkernel_dependency_detected"),
            "vendor-hardcoding": ("error", "vendor_hardcoding_detected"),
            "local-runtime-provider": ("error", "local_runtime_provider_attempted_too_early"),
            "general-agent-usability": ("error", "general_agent_usability_attempted_too_early"),
            "schumpeter": ("error", "schumpeter_split_attempted_too_early"),
        }
        for marker, (severity, finding_type) in marker_findings.items():
            if marker in source_text:
                add(severity, finding_type)
        if not findings:
            add("info", "ok")
        return findings


class DominionDispatchBoundaryReportService:
    def __init__(self) -> None:
        self.sources = DominionDispatchBoundarySourceService()
        self.authorization_boundary = DominionAuthorizationBoundaryService()
        self.authorization_scope = DominionAuthorizationScopeService()
        self.consumption_policy = DominionAuthorizationConsumptionPolicyService()
        self.dispatch_mode_policy = DominionDispatchModePolicyService()
        self.command_descriptor = DominionDispatchCommandDescriptorService()
        self.provider_boundary = DominionProviderDispatchInterfaceBoundaryService()
        self.dispatch_boundary = DominionBoundedDispatchBoundaryService()
        self.status_boundary = DominionStatusBoundaryService()
        self.output_boundary = DominionOutputBoundaryService()
        self.outcome_boundary = DominionOutcomeBoundaryService()
        self.findings = DominionDispatchBoundaryFindingService()

    def build_report(self, request: DominionDispatchBoundaryRequest | None = None) -> DominionDispatchBoundaryReport:
        request = request or DominionDispatchBoundaryRequest()
        gate_report = self.sources.load_gate_report(request.gate_report_id)
        authorization = self.sources.load_gate_authorization(request.authorization_id, gate_report)
        plan = self.sources.load_control_plan(request.plan_id, gate_report)
        preflight = self.sources.load_preflight_report(request.preflight_report_id, gate_report)
        authorization_check = self.authorization_boundary.check_authorization(gate_report, authorization)
        authorization_scope = self.authorization_scope.build_scope_descriptor(gate_report, authorization, plan, preflight)
        consumption_policy = self.consumption_policy.build_consumption_policy(gate_report, authorization)
        mode_policy = self.dispatch_mode_policy.build_dispatch_mode_policy(request)
        command_descriptor = self.command_descriptor.build_command_descriptor(gate_report, plan)
        provider_boundary = self.provider_boundary.build_provider_interface_boundary(gate_report, plan)
        dispatch_boundary = self.dispatch_boundary.build_dispatch_boundary(
            request,
            authorization_check,
            command_descriptor,
            provider_boundary,
            mode_policy,
        )
        status_boundary = self.status_boundary.build_status_boundary(plan)
        output_boundary = self.output_boundary.build_output_boundary(plan)
        outcome_boundary = self.outcome_boundary.build_outcome_boundary(plan)
        findings = self.findings.build_findings(
            request,
            gate_report,
            authorization,
            authorization_check,
            authorization_scope,
            mode_policy,
            command_descriptor,
            provider_boundary,
            dispatch_boundary,
            status_boundary,
            output_boundary,
            outcome_boundary,
        )
        report_status = _report_status(gate_report, authorization_check, authorization_scope, dispatch_boundary, findings)
        return DominionDispatchBoundaryReport(
            report_id="dominion_dispatch_boundary_report:v0.23.8",
            version=DISPATCH_BOUNDARY_VERSION,
            created_at=_now(),
            request=request,
            authorization_check=authorization_check,
            authorization_scope=authorization_scope,
            authorization_consumption_policy=consumption_policy,
            dispatch_mode_policy=mode_policy,
            dispatch_boundary=dispatch_boundary,
            status_boundary=status_boundary,
            output_boundary=output_boundary,
            outcome_boundary=outcome_boundary,
            findings=findings,
            report_status=report_status,
            eligible_for_v0_23_9=report_status == "ready_for_consolidation",
            provider_api_call_performed=False,
            external_runtime_touched=False,
            external_run_started=False,
            authorization_consumed=False,
            credential_exposed=False,
            raw_secret_output=False,
            limitations=[
                "v0.23.8 creates authorization, dispatch, status, output, and outcome boundary artifacts only.",
                "Authorization is checked but not consumed; actual dispatch remains outside v0.23.8.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider APIs, runtime touch, dispatch, authorization consumption, live status tracking, output fetch, or real external outcome recording is introduced.",
                "Withdraw if v0.23.8 implements v0.24+ roadmap items or company-specific deployment logic.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": DISPATCH_BOUNDARY_VERSION,
            "layer": DISPATCH_BOUNDARY_LAYER,
            "subject": DISPATCH_BOUNDARY_SUBJECT,
            "principles": [
                "authorization boundary is not authorization consumption",
                "bounded dispatch boundary is not dispatch",
                "status boundary is not live status tracking",
                "output boundary is not output fetch",
                "outcome boundary is not real external outcome record",
                "v0.23.8 remains provider-neutral and non-executing",
            ],
            "safety_boundary": {
                "boundary_state_created": True,
                "authorization_consumed": False,
                "safe_to_dispatch": False,
                "bounded_dispatch_allowed_now": False,
                "actual_dispatch_performed": False,
                "provider_api_call_performed": False,
                "external_runtime_touched": False,
                "external_run_started": False,
                "live_status_tracking_started": False,
                "live_output_fetch_started": False,
                "real_external_outcome_recorded": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "local_runtime_provider_implemented": False,
                "general_agent_usability_implemented": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": DISPATCH_BOUNDARY_NEXT_STEP,
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
            "state": DISPATCH_BOUNDARY_STATE,
            "version": DISPATCH_BOUNDARY_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionGateState",
                "DominionGateAuthorizationState",
                "DominionRuntimePreflightState",
                "DominionControlPlanState",
                "ExternalActionCandidateState",
            ],
            "target_read_models": [
                "DominionDispatchBoundaryState",
                "DominionAuthorizationBoundaryState",
                "DominionStatusBoundaryState",
                "DominionOutputBoundaryState",
                "DominionOutcomeBoundaryState",
                "DominionV0239EligibilityState",
                "DominionRoadmapBoundaryState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(
        self, report: DominionDispatchBoundaryReport | None = None, section: str = "summary"
    ) -> str:
        report = report or self.build_report()
        boundary = report.dispatch_boundary
        auth_check = report.authorization_check
        auth_id = auth_check.authorization_id if auth_check else "none"
        lines = [
            "Dominion Dispatch Boundary",
            f"version={report.version}",
            f"layer={DISPATCH_BOUNDARY_LAYER}",
            f"report_id={report.report_id}",
            f"boundary_id={boundary.boundary_id if boundary else 'missing'}",
            f"authorization_id={auth_id}",
            f"report_status={report.report_status}",
            f"authorization.single_use={str(auth_check.authorization_single_use if auth_check else False).lower()}",
            f"authorization.consumed={str(auth_check.authorization_consumed if auth_check else False).lower()}",
            f"authorization_consumed={str(report.authorization_consumed).lower()}",
            f"safe_to_dispatch={str(report.safe_to_dispatch).lower()}",
            f"bounded_dispatch_allowed_now={str(report.bounded_dispatch_allowed_now).lower()}",
            f"actual_dispatch_performed={str(report.actual_dispatch_performed).lower()}",
            f"provider_api_call_performed={str(report.provider_api_call_performed).lower()}",
            f"external_runtime_touched={str(report.external_runtime_touched).lower()}",
            f"external_run_started={str(report.external_run_started).lower()}",
            f"live_status_tracking_started={str(report.live_status_tracking_started).lower()}",
            f"live_output_fetch_started={str(report.live_output_fetch_started).lower()}",
            f"real_external_outcome_recorded={str(report.real_external_outcome_recorded).lower()}",
            f"credential_exposed={str(report.credential_exposed).lower()}",
            f"local_runtime_provider_implemented={str(report.local_runtime_provider_implemented).lower()}",
            f"general_agent_usability_implemented={str(report.general_agent_usability_implemented).lower()}",
            f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
            f"eligible_for_v0_23_9={str(report.eligible_for_v0_23_9).lower()}",
        ]
        if section == "authorization" and auth_check:
            lines.extend(
                [
                    f"authorization_exists={str(auth_check.authorization_exists).lower()}",
                    f"authorization_valid_for_boundary={str(auth_check.authorization_valid_for_boundary).lower()}",
                    f"authorization_valid_for_live_dispatch={str(auth_check.authorization_valid_for_live_dispatch).lower()}",
                    f"authorization_consumption_allowed_now={str(auth_check.authorization_consumption_allowed_now).lower()}",
                ]
            )
        elif section == "status" and report.status_boundary:
            lines.extend(
                [
                    f"status_boundary_id={report.status_boundary.status_boundary_id}",
                    f"status_boundary_status={report.status_boundary.status_boundary_status}",
                    f"live_status_tracking_started={str(report.status_boundary.live_status_tracking_started).lower()}",
                ]
            )
        elif section == "outcome" and report.outcome_boundary:
            lines.extend(
                [
                    f"outcome_boundary_id={report.outcome_boundary.outcome_boundary_id}",
                    f"boundary_outcome_record_created={str(report.outcome_boundary.boundary_outcome_record_created).lower()}",
                    f"real_external_outcome_recorded={str(report.outcome_boundary.real_external_outcome_recorded).lower()}",
                ]
            )
        elif section == "findings":
            lines.extend(f"- finding={item.finding_type} severity={item.severity}" for item in report.findings)
        lines.extend(
            [
                f"next_required_step={report.next_required_step}",
                "raw_secrets_printed=false",
                "private_full_paths_printed=false",
                "credential_values_printed=false",
            ]
        )
        return "\n".join(lines)

    def build_needs_more_input_candidate(
        self, report: DominionDispatchBoundaryReport | None = None
    ) -> DominionDispatchBoundaryNeedsMoreInputCandidate:
        return DominionDispatchBoundaryNeedsMoreInputCandidate(
            candidate_id="dominion_dispatch_boundary_needs_more_input_candidate:v0.23.8",
            report_id=report.report_id if report else None,
            reason="Dispatch boundary requires additional declared authorization, scope, or interface inputs.",
            missing_inputs=["authorization", "provider_interface_boundary"],
            evidence_refs=[{"candidate_only": True}],
        )

    def build_no_action_candidate(
        self, report: DominionDispatchBoundaryReport | None = None
    ) -> DominionDispatchBoundaryNoActionCandidate:
        return DominionDispatchBoundaryNoActionCandidate(
            candidate_id="dominion_dispatch_boundary_no_action_candidate:v0.23.8",
            report_id=report.report_id if report else None,
            reason="Gate is not open or dispatch boundary is no longer relevant.",
            evidence_refs=[{"candidate_only": True}],
        )


class DominionDispatchBoundaryService(DominionDispatchBoundaryReportService):
    def create_boundary(self, request: DominionDispatchBoundaryRequest | None = None) -> DominionDispatchBoundaryReport:
        return self.build_report(request)


def _has_finding(findings: list[DominionDispatchBoundaryFinding], finding_type: str) -> bool:
    return any(item.finding_type == finding_type for item in findings)


def _report_status(
    gate_report: DominionGateReport | None,
    authorization_check: DominionAuthorizationBoundaryCheck,
    authorization_scope: DominionAuthorizationScopeDescriptor,
    dispatch_boundary: DominionBoundedDispatchBoundary,
    findings: list[DominionDispatchBoundaryFinding],
) -> str:
    critical_types = {item.finding_type for item in findings if item.severity == "critical"}
    if critical_types & {
        "authorization_already_consumed",
        "authorization_consumption_attempted",
        "provider_api_call_performed",
        "external_runtime_touched",
        "actual_dispatch_attempted",
        "external_run_started",
        "credential_value_materialized",
        "raw_payload_output",
        "real_external_outcome_recorded",
    }:
        return "blocked"
    if gate_report is None:
        return "blocked"
    if not gate_report.gate_state or gate_report.gate_state.gate_status in {"rejected", "no_action", "needs_more_input"}:
        return "no_action"
    if not authorization_check.authorization_exists:
        return "needs_more_input"
    if authorization_scope.scope_status == "blocked" or authorization_check.authorization_expired:
        return "failed"
    if not authorization_check.authorization_valid_for_boundary:
        return "failed"
    if dispatch_boundary.dispatch_boundary_status == "needs_more_input":
        return "needs_more_input"
    if dispatch_boundary.dispatch_boundary_status == "blocked":
        return "blocked"
    if any(item.severity == "error" for item in findings):
        return "failed"
    return "ready_for_consolidation"
