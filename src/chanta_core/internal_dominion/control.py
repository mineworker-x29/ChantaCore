from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.capability import (
    CapabilityObservationDigestReportService,
    ExternalCapabilityCandidate,
)
from chanta_core.internal_dominion.inventory import RuntimeInventoryReportService
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)


CONTROL_REQUEST_VERSION = "v0.23.3"
CONTROL_REQUEST_VERSION_NAME = "Control Request & Action Candidate"
CONTROL_REQUEST_TRACK = "Internal Dominion Foundation"
CONTROL_REQUEST_LAYER = "internal_dominion"
CONTROL_REQUEST_SUBJECT = "control_request_action_candidate"
CONTROL_REQUEST_STATE = "dominion_external_action_candidate_created"
CONTROL_REQUEST_NEXT_STEP = "v0.23.4 Control Plan & Target Binding"

SECRET_KEYS = {"credential_value", "token", "secret", "password", "api_key", "private_key", "raw_secret"}
READ_VERBS = {"observe", "status", "list", "describe", "inspect", "read", "get"}
LOW_VERBS = {"validate", "prepare"}
HIGH_VERBS = {"trigger", "start", "run", "stop", "cancel", "create", "update", "assign", "approve", "reject"}
DESTRUCTIVE_VERBS = {"delete", "remove", "destroy"}


def _now() -> str:
    return utc_now_iso()


def _clean(value: dict[str, Any] | None) -> dict[str, Any]:
    if not value:
        return {}
    return {str(key): item for key, item in value.items() if str(key).lower() not in SECRET_KEYS}


def _has_secret(value: dict[str, Any]) -> bool:
    return any(str(key).lower() in SECRET_KEYS for key in value)


@dataclass(frozen=True)
class DominionControlRequestCreateRequest:
    goal_text: str
    capability_candidate_ids: list[str] = field(default_factory=list)
    runtime_ids: list[str] = field(default_factory=list)
    provider_ref_ids: list[str] = field(default_factory=list)
    requested_action_verb: str | None = None
    requested_inputs: dict[str, Any] = field(default_factory=dict)
    requester_type: str = "operator"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    constraints: list[str] = field(default_factory=list)
    allow_no_action: bool = True
    allow_needs_more_input: bool = True
    max_candidates: int = 5
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal_text": self.goal_text,
            "capability_candidate_ids": list(self.capability_candidate_ids),
            "runtime_ids": list(self.runtime_ids),
            "provider_ref_ids": list(self.provider_ref_ids),
            "requested_action_verb": self.requested_action_verb,
            "requested_inputs": _clean(self.requested_inputs),
            "requester_type": self.requester_type,
            "source_refs": [_clean(item) for item in self.source_refs],
            "constraints": list(self.constraints),
            "allow_no_action": self.allow_no_action,
            "allow_needs_more_input": self.allow_needs_more_input,
            "max_candidates": self.max_candidates,
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class ControlTargetRef:
    target_ref_id: str
    target_type: str
    provider_ref_id: str | None = None
    runtime_id: str | None = None
    capability_candidate_id: str | None = None
    agent_id: str | None = None
    tool_id: str | None = None
    system_id: str | None = None
    environment: str = "unknown"
    target_status: str = "unknown"
    production_impacting: bool = False
    credential_sensitive: bool = False
    dispatch_enabled: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionActionIntentDescriptor:
    intent_id: str
    goal_text: str
    raw_action_verb: str | None
    normalized_action_verb: str
    intent_type: str
    risk_class: str
    requires_control_plan: bool
    requires_target_binding: bool
    requires_static_safety: bool
    requires_preflight: bool
    requires_human_gate: bool
    requires_strong_gate: bool
    requires_authorization: bool
    requires_status_tracking: bool
    requires_outcome_record: bool
    forbidden_until_provider_adapter: bool
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionActionInputDraft:
    input_draft_id: str
    capability_candidate_id: str | None
    schema_ref: dict[str, Any] | None
    provided_fields: dict[str, Any]
    missing_required_fields: list[str]
    sensitive_fields_present: list[str]
    credential_values_present: bool
    raw_secret_output: bool = False
    input_status: str = "draft_only"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "schema_ref": _clean(self.schema_ref),
            "provided_fields": _clean(self.provided_fields),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionControlConstraint:
    constraint_id: str
    constraint_type: str
    description: str
    severity: str
    source_ref: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"source_ref": _clean(self.source_ref)}


@dataclass(frozen=True)
class DominionPreliminaryActionRisk:
    risk_id: str
    risk_class: str
    risk_reasons: list[str]
    production_impacting: bool
    destructive: bool
    credential_sensitive: bool
    provider_adapter_required: bool
    preflight_required: bool
    human_gate_required: bool
    strong_gate_required: bool
    status_tracking_required: bool
    outcome_record_required: bool
    safe_to_plan: bool
    safe_to_dispatch: bool = False
    dispatch_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionControlRequest:
    request_id: str
    created_at: str
    goal_text: str
    requester_type: str
    target_refs: list[ControlTargetRef]
    intent: DominionActionIntentDescriptor
    input_draft: DominionActionInputDraft | None
    constraints: list[DominionControlConstraint]
    source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    request_status: str
    review_status: str = "request_only"
    control_plan_created: bool = False
    preflight_checked: bool = False
    human_gate_opened: bool = False
    authorization_created: bool = False
    dispatched: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_id": self.request_id,
            "created_at": self.created_at,
            "goal_text": self.goal_text,
            "requester_type": self.requester_type,
            "target_refs": [item.to_dict() for item in self.target_refs],
            "intent": self.intent.to_dict(),
            "input_draft": self.input_draft.to_dict() if self.input_draft else None,
            "constraints": [item.to_dict() for item in self.constraints],
            "source_refs": [_clean(item) for item in self.source_refs],
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
            "request_status": self.request_status,
            "review_status": self.review_status,
            "control_plan_created": self.control_plan_created,
            "preflight_checked": self.preflight_checked,
            "human_gate_opened": self.human_gate_opened,
            "authorization_created": self.authorization_created,
            "dispatched": self.dispatched,
            "external_runtime_touched": self.external_runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
        }


@dataclass(frozen=True)
class DominionActionCandidateFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    target_ref: dict[str, Any] | None = None
    capability_ref: dict[str, Any] | None = None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "severity": self.severity,
            "finding_type": self.finding_type,
            "message": self.message,
            "target_ref": _clean(self.target_ref),
            "capability_ref": _clean(self.capability_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
            "withdrawal_condition": self.withdrawal_condition,
        }


@dataclass(frozen=True)
class ExternalActionCandidate:
    action_candidate_id: str
    request_id: str
    created_at: str
    title: str
    goal_text: str
    target_refs: list[ControlTargetRef]
    capability_candidate_refs: list[dict[str, Any]]
    intent: DominionActionIntentDescriptor
    input_draft: DominionActionInputDraft | None
    constraints: list[DominionControlConstraint]
    preliminary_risk: DominionPreliminaryActionRisk
    findings: list[DominionActionCandidateFinding]
    evidence_refs: list[dict[str, Any]]
    lifecycle_state: str = "action_candidate_created"
    candidate_status: str = "candidate_only"
    control_plan_required: bool = True
    target_binding_required: bool = True
    static_safety_required: bool = True
    preflight_required: bool = True
    human_gate_required: bool = True
    authorization_required: bool = True
    status_tracking_required: bool = True
    outcome_record_required: bool = True
    control_plan_created: bool = False
    target_bound: bool = False
    static_safety_checked: bool = False
    preflight_checked: bool = False
    human_gate_opened: bool = False
    authorization_created: bool = False
    dispatch_enabled: bool = False
    dispatched: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "target_refs": [item.to_dict() for item in self.target_refs],
            "capability_candidate_refs": [_clean(item) for item in self.capability_candidate_refs],
            "intent": self.intent.to_dict(),
            "input_draft": self.input_draft.to_dict() if self.input_draft else None,
            "constraints": [item.to_dict() for item in self.constraints],
            "preliminary_risk": self.preliminary_risk.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionNoActionCandidate:
    candidate_id: str
    request_id: str
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionNeedsMoreInputCandidate:
    candidate_id: str
    request_id: str
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "needs_more_input"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionControlRequestCandidateReport:
    report_id: str
    version: str
    created_at: str
    request: DominionControlRequest
    action_candidate: ExternalActionCandidate | None
    no_action_candidate: DominionNoActionCandidate | None
    needs_more_input_candidate: DominionNeedsMoreInputCandidate | None
    findings: list[DominionActionCandidateFinding]
    report_status: str
    next_required_step: str = CONTROL_REQUEST_NEXT_STEP
    control_plan_created: bool = False
    preflight_checked: bool = False
    human_gate_opened: bool = False
    authorization_created: bool = False
    dispatched: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    credential_exposed: bool = False
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until capability candidates, inventory, requested target, or Dominion policy changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "request": self.request.to_dict(),
            "action_candidate": self.action_candidate.to_dict() if self.action_candidate else None,
            "no_action_candidate": self.no_action_candidate.to_dict() if self.no_action_candidate else None,
            "needs_more_input_candidate": self.needs_more_input_candidate.to_dict()
            if self.needs_more_input_candidate
            else None,
            "findings": [item.to_dict() for item in self.findings],
            "report_status": self.report_status,
            "next_required_step": self.next_required_step,
            "control_plan_created": self.control_plan_created,
            "preflight_checked": self.preflight_checked,
            "human_gate_opened": self.human_gate_opened,
            "authorization_created": self.authorization_created,
            "dispatched": self.dispatched,
            "external_runtime_touched": self.external_runtime_touched,
            "provider_api_call_performed": self.provider_api_call_performed,
            "credential_exposed": self.credential_exposed,
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
        }


class DominionControlSourceService:
    def __init__(self) -> None:
        self.inventory_reports = RuntimeInventoryReportService()
        self.capability_reports = CapabilityObservationDigestReportService()

    def load_runtime_inventory(self, inventory_report_id: str | None = None) -> Any:
        return self.inventory_reports.build_report()

    def load_capability_candidates(self, capability_candidate_ids: list[str]) -> list[ExternalCapabilityCandidate]:
        candidates = self.capability_reports.build_report().snapshot.candidates
        if capability_candidate_ids:
            selected = [item for item in candidates if item.candidate_id in set(capability_candidate_ids)]
            return selected
        return candidates


class ControlTargetResolver:
    def resolve_targets(
        self,
        request: DominionControlRequestCreateRequest,
        inventory: Any,
        capability_candidates: list[ExternalCapabilityCandidate],
    ) -> list[ControlTargetRef]:
        targets: list[ControlTargetRef] = []
        for candidate in capability_candidates[: request.max_candidates]:
            risk = str(candidate.risk_profile_ref.get("risk_class", "unknown"))
            targets.append(
                ControlTargetRef(
                    target_ref_id=f"control_target:{candidate.candidate_id}",
                    target_type="capability",
                    provider_ref_id=candidate.provider_ref_id,
                    runtime_id=candidate.runtime_id,
                    capability_candidate_id=candidate.candidate_id,
                    environment="unknown",
                    target_status="resolved",
                    production_impacting=risk == "production_impacting",
                    credential_sensitive=risk == "credential_sensitive",
                    evidence_refs=[{"read_only_source": True}],
                )
            )
        if not targets:
            targets.append(
                ControlTargetRef(
                    target_ref_id="control_target:missing",
                    target_type="unknown",
                    target_status="missing",
                    evidence_refs=[{"missing_capability_candidate": True}],
                )
            )
        return targets


class DominionActionIntentClassifier:
    def classify(
        self,
        request: DominionControlRequestCreateRequest,
        capability_candidates: list[ExternalCapabilityCandidate],
    ) -> DominionActionIntentDescriptor:
        verb = (request.requested_action_verb or _first_candidate_verb(capability_candidates) or "unknown").lower()
        risk = _risk_for_verb(verb)
        future_required = risk != "read_only"
        return DominionActionIntentDescriptor(
            intent_id="dominion_action_intent:v0.23.3",
            goal_text=request.goal_text,
            raw_action_verb=request.requested_action_verb,
            normalized_action_verb=verb,
            intent_type="external_action_candidate",
            risk_class=risk,
            requires_control_plan=True,
            requires_target_binding=True,
            requires_static_safety=True,
            requires_preflight=future_required,
            requires_human_gate=future_required,
            requires_strong_gate=risk in {"production_impacting", "destructive", "credential_sensitive"},
            requires_authorization=True,
            requires_status_tracking=True,
            requires_outcome_record=True,
            forbidden_until_provider_adapter=future_required,
            notes=["request_only", "not_dispatch"],
        )


class DominionActionInputDraftService:
    def build_input_draft(
        self,
        request: DominionControlRequestCreateRequest,
        capability_candidates: list[ExternalCapabilityCandidate],
    ) -> DominionActionInputDraft:
        candidate = capability_candidates[0] if capability_candidates else None
        schema_ref = candidate.input_schema_ref if candidate else None
        required = [str(item) for item in (schema_ref or {}).get("required_fields", [])]
        missing = [field for field in required if field not in request.requested_inputs]
        sensitive = [field for field in request.requested_inputs if "credential" in field.lower() or "token" in field.lower()]
        credential_present = _has_secret(request.requested_inputs)
        return DominionActionInputDraft(
            input_draft_id="dominion_action_input_draft:v0.23.3",
            capability_candidate_id=candidate.candidate_id if candidate else None,
            schema_ref=schema_ref,
            provided_fields=_clean(request.requested_inputs),
            missing_required_fields=missing,
            sensitive_fields_present=sensitive,
            credential_values_present=credential_present,
            input_status="blocked" if credential_present else ("incomplete" if missing else "draft_only"),
            evidence_refs=[{"metadata_only": True}],
        )


class DominionControlConstraintService:
    def build_constraints(
        self,
        request: DominionControlRequestCreateRequest,
        targets: list[ControlTargetRef],
        intent: DominionActionIntentDescriptor,
    ) -> list[DominionControlConstraint]:
        return [
            DominionControlConstraint(name, name, name.replace("_", " "), "hard_block" if name.startswith("no_") else "warning")
            for name in [
                "no_dispatch_in_v0_23_3",
                "no_control_plan_in_v0_23_3",
                "no_preflight_in_v0_23_3",
                "no_authorization_in_v0_23_3",
                "requires_control_plan_v0_23_4",
                "requires_static_safety_v0_23_5",
                "requires_preflight_v0_23_6",
                "requires_dominion_gate_v0_23_7",
                "requires_status_tracking_v0_23_8",
                "requires_outcome_record_v0_23_8",
                "no_credential_value_materialization",
                "provider_adapter_future_track",
            ]
        ]


class DominionPreliminaryRiskService:
    def assess(
        self,
        request: DominionControlRequestCreateRequest,
        targets: list[ControlTargetRef],
        intent: DominionActionIntentDescriptor,
        input_draft: DominionActionInputDraft,
    ) -> DominionPreliminaryActionRisk:
        destructive = intent.risk_class == "destructive"
        credential_sensitive = input_draft.credential_values_present or any(target.credential_sensitive for target in targets)
        production = intent.risk_class == "production_impacting" or any(target.production_impacting for target in targets)
        return DominionPreliminaryActionRisk(
            risk_id="dominion_preliminary_action_risk:v0.23.3",
            risk_class="credential_sensitive" if credential_sensitive else intent.risk_class,
            risk_reasons=[intent.risk_class],
            production_impacting=production,
            destructive=destructive,
            credential_sensitive=credential_sensitive,
            provider_adapter_required=intent.forbidden_until_provider_adapter,
            preflight_required=True,
            human_gate_required=True,
            strong_gate_required=production or destructive or credential_sensitive,
            status_tracking_required=True,
            outcome_record_required=True,
            safe_to_plan=not input_draft.credential_values_present and not destructive,
            evidence_refs=[{"candidate_only": True}],
        )


class DominionActionCandidateFindingService:
    def build_findings(
        self,
        request: DominionControlRequestCreateRequest,
        targets: list[ControlTargetRef],
        intent: DominionActionIntentDescriptor,
        input_draft: DominionActionInputDraft,
        risk: DominionPreliminaryActionRisk,
    ) -> list[DominionActionCandidateFinding]:
        findings: list[DominionActionCandidateFinding] = []
        if any(target.target_status == "missing" for target in targets):
            findings.append(_finding("warning", "missing_capability_candidate"))
            findings.append(_finding("warning", "needs_more_input"))
        if intent.normalized_action_verb == "unknown":
            findings.append(_finding("warning", "unknown_action_verb"))
        if input_draft.missing_required_fields:
            findings.append(_finding("warning", "required_input_missing"))
            findings.append(_finding("warning", "needs_more_input"))
        if input_draft.credential_values_present:
            findings.append(_finding("critical", "credential_value_detected"))
        if risk.production_impacting:
            findings.append(_finding("warning", "production_action_requested"))
        if risk.destructive:
            findings.append(_finding("error", "destructive_action_requested"))
            findings.append(_finding("warning", "no_action_recommended"))
        if risk.provider_adapter_required:
            findings.append(_finding("warning", "provider_adapter_required"))
        for finding_type in ["control_plan_required", "preflight_required", "human_gate_required", "dispatch_not_allowed"]:
            findings.append(_finding("info", finding_type))
        lowered = " ".join([request.goal_text, *request.constraints]).lower()
        if "self_execution" in lowered:
            findings.append(_finding("error", "self_execution_legacy_detected"))
        if "growthkernel dependency" in lowered or "requires growthkernel" in lowered:
            findings.append(_finding("error", "growthkernel_dependency_detected"))
        if "vendor hardcoding" in lowered:
            findings.append(_finding("critical", "vendor_hardcoding_detected"))
        if not findings:
            findings.append(_finding("info", "ok"))
        return findings


class ExternalActionCandidateService:
    def build_candidate(
        self,
        request: DominionControlRequestCreateRequest,
        control_request: DominionControlRequest,
        capability_candidates: list[ExternalCapabilityCandidate],
        preliminary_risk: DominionPreliminaryActionRisk,
        findings: list[DominionActionCandidateFinding],
    ) -> ExternalActionCandidate:
        return ExternalActionCandidate(
            action_candidate_id="external_action_candidate:v0.23.3",
            request_id=control_request.request_id,
            created_at=control_request.created_at,
            title=request.goal_text[:80] or "Dominion action candidate",
            goal_text=request.goal_text,
            target_refs=control_request.target_refs,
            capability_candidate_refs=[{"candidate_id": item.candidate_id} for item in capability_candidates],
            intent=control_request.intent,
            input_draft=control_request.input_draft,
            constraints=control_request.constraints,
            preliminary_risk=preliminary_risk,
            findings=findings,
            evidence_refs=[{"candidate_only": True}],
        )


class DominionControlRequestCandidateService:
    def __init__(self) -> None:
        self.sources = DominionControlSourceService()
        self.targets = ControlTargetResolver()
        self.intent = DominionActionIntentClassifier()
        self.inputs = DominionActionInputDraftService()
        self.constraints = DominionControlConstraintService()
        self.risk = DominionPreliminaryRiskService()
        self.findings = DominionActionCandidateFindingService()
        self.candidates = ExternalActionCandidateService()

    def create_request_and_candidate(
        self,
        request: DominionControlRequestCreateRequest,
    ) -> DominionControlRequestCandidateReport:
        created_at = _now()
        inventory = self.sources.load_runtime_inventory(None)
        capability_candidates = self.sources.load_capability_candidates(request.capability_candidate_ids)
        targets = self.targets.resolve_targets(request, inventory, capability_candidates)
        intent = self.intent.classify(request, capability_candidates)
        input_draft = self.inputs.build_input_draft(request, capability_candidates)
        constraints = self.constraints.build_constraints(request, targets, intent)
        risk = self.risk.assess(request, targets, intent, input_draft)
        findings = self.findings.build_findings(request, targets, intent, input_draft, risk)
        status = _report_status(findings, request, risk)
        control_request = DominionControlRequest(
            request_id="dominion_control_request:v0.23.3",
            created_at=created_at,
            goal_text=request.goal_text,
            requester_type=request.requester_type,
            target_refs=targets,
            intent=intent,
            input_draft=input_draft,
            constraints=constraints,
            source_refs=[_clean(item) for item in request.source_refs],
            evidence_refs=[{"runtime_inventory_read_only": True, "capability_candidates_read_only": True}],
            request_status=status,
        )
        action_candidate = None
        no_action = None
        needs_more = None
        if status == "candidate_created":
            action_candidate = self.candidates.build_candidate(request, control_request, capability_candidates, risk, findings)
        elif status == "no_action":
            no_action = DominionNoActionCandidate(
                candidate_id="dominion_no_action_candidate:v0.23.3",
                request_id=control_request.request_id,
                reason="risk outweighs value or destructive action is not justified",
                evidence_refs=[{"candidate_only": True}],
            )
        elif status == "needs_more_input":
            needs_more = DominionNeedsMoreInputCandidate(
                candidate_id="dominion_needs_more_input_candidate:v0.23.3",
                request_id=control_request.request_id,
                reason="additional target, capability, action, or input fields are required",
                missing_inputs=input_draft.missing_required_fields or ["capability_candidate_id"],
                evidence_refs=[{"candidate_only": True}],
            )
        return DominionControlRequestCandidateReport(
            report_id="dominion_control_request_candidate_report:v0.23.3",
            version=CONTROL_REQUEST_VERSION,
            created_at=created_at,
            request=control_request,
            action_candidate=action_candidate,
            no_action_candidate=no_action,
            needs_more_input_candidate=needs_more,
            findings=findings,
            report_status=status,
            limitations=[
                "v0.23.3 creates request/action candidates only.",
                "No control plan, target binding, preflight, gate, authorization, dispatch, provider API call, or runtime touch is enabled.",
            ],
            withdrawal_conditions=[
                "Withdraw if control plan, preflight, authorization, dispatch, provider API call, runtime touch, or credential output is introduced.",
                "Withdraw if v0.23.x is described as Self-Execution Safety.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": CONTROL_REQUEST_VERSION,
            "layer": CONTROL_REQUEST_LAYER,
            "subject": CONTROL_REQUEST_SUBJECT,
            "principles": [
                "control request is not dispatch",
                "control request is not control plan",
                "action candidate is not external runtime touch",
                "action candidate is not preflight",
                "action candidate is not authorization",
                "no-action and needs-more-input are valid outcomes",
            ],
            "safety_boundary": {
                "control_plan_created": False,
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
            "next_step": CONTROL_REQUEST_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": CONTROL_REQUEST_STATE,
            "version": CONTROL_REQUEST_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionRuntimeInventoryState",
                "ExternalCapabilityCandidateState",
                "CapabilityRiskProfileState",
                "CapabilityBoundaryState",
                "CapabilitySchemaState",
            ],
            "target_read_models": [
                "DominionControlRequestState",
                "ExternalActionCandidateState",
                "ControlTargetState",
                "DominionActionIntentState",
                "DominionPreliminaryRiskState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: DominionControlRequestCandidateReport) -> str:
        candidate_id = report.action_candidate.action_candidate_id if report.action_candidate else ""
        return "\n".join(
            [
                "Dominion Control Request & Action Candidate",
                f"version={report.version}",
                f"layer={CONTROL_REQUEST_LAYER}",
                f"status={report.report_status}",
                f"request_id={report.request.request_id}",
                f"action_candidate_id={candidate_id}",
                "candidate_status=candidate_only",
                f"control_plan_created={str(report.control_plan_created).lower()}",
                f"preflight_checked={str(report.preflight_checked).lower()}",
                f"human_gate_opened={str(report.human_gate_opened).lower()}",
                f"authorization_created={str(report.authorization_created).lower()}",
                "dispatch_enabled=false",
                f"dispatched={str(report.dispatched).lower()}",
                f"external_runtime_touched={str(report.external_runtime_touched).lower()}",
                f"provider_api_call_performed={str(report.provider_api_call_performed).lower()}",
                f"credential_exposed={str(report.credential_exposed).lower()}",
                f"next_required_step={report.next_required_step}",
                "raw_secrets_printed=False",
                "private_full_paths_printed=False",
            ]
        )


def _first_candidate_verb(candidates: list[ExternalCapabilityCandidate]) -> str | None:
    if not candidates or not candidates[0].action_verbs:
        return None
    return candidates[0].action_verbs[0].normalized_verb


def _risk_for_verb(verb: str) -> str:
    if verb in READ_VERBS:
        return "read_only"
    if verb in LOW_VERBS:
        return "low"
    if verb in DESTRUCTIVE_VERBS:
        return "destructive"
    if verb in HIGH_VERBS:
        return "high"
    return "unknown"


def _finding(severity: str, finding_type: str) -> DominionActionCandidateFinding:
    return DominionActionCandidateFinding(
        finding_id=f"dominion_action_candidate_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=finding_type.replace("_", " "),
        evidence_refs=[{"policy": "v0.23.3_candidate_only"}],
        withdrawal_condition="Withdraw this finding if sanitized request/candidate evidence changes.",
    )


def _report_status(
    findings: list[DominionActionCandidateFinding],
    request: DominionControlRequestCreateRequest,
    risk: DominionPreliminaryActionRisk,
) -> str:
    severities = {item.severity for item in findings}
    if "critical" in severities:
        return "blocked"
    if risk.destructive and request.allow_no_action:
        return "no_action"
    if any(item.finding_type in {"missing_capability_candidate", "required_input_missing", "unknown_action_verb"} for item in findings):
        return "needs_more_input"
    return "candidate_created"
