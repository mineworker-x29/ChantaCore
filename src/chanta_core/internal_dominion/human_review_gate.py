from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso

from chanta_core.internal_dominion.control_plan import DominionControlPlan
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)
from chanta_core.internal_dominion.runtime_preflight import (
    DominionRuntimePreflightReport,
    DominionRuntimePreflightRequest,
    DominionRuntimePreflightService,
)
from chanta_core.internal_dominion.static_safety import DominionStaticSafetyReport


HUMAN_REVIEW_GATE_VERSION = "v0.23.7"
HUMAN_REVIEW_GATE_VERSION_NAME = "Human Review & Dominion Gate"
HUMAN_REVIEW_GATE_KOREAN_NAME = "\uc778\uac04 \uac80\ud1a0\u00b7\uc9c0\ubc30 \uac8c\uc774\ud2b8"
HUMAN_REVIEW_GATE_TRACK = "Internal Dominion Foundation"
HUMAN_REVIEW_GATE_LAYER = "internal_dominion"
HUMAN_REVIEW_GATE_SUBJECT = "human_review_dominion_gate"
HUMAN_REVIEW_GATE_STATE = "dominion_gate_opened_or_review_recorded"
HUMAN_REVIEW_GATE_NEXT_STEP = "v0.23.8 Authorization / Bounded Dispatch / Status / Outcome Boundary"
APPROVAL_PHRASE = "I approve this Dominion gate for v0.23.8 boundary review"

SECRET_KEYS = {"credential_value", "token", "secret", "password", "api_key", "private_key", "raw_secret"}
ALLOWED_DECISIONS = {"approve", "reject", "revise", "no_action", "needs_more_input", "defer"}
HIGH_RISK_CLASSES = {"mutating", "destructive", "high", "high_risk", "production", "credential_sensitive"}


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
class DominionHumanReviewRequestCreateRequest:
    preflight_report_id: str = "dominion_runtime_preflight_report:v0.23.6"
    static_safety_report_id: str | None = None
    plan_id: str | None = None
    action_candidate_id: str | None = None
    requested_review_decision: str | None = None
    reviewer_type: str = "operator"
    reviewer_ref: dict[str, Any] | None = None
    decision_rationale: str | None = None
    approval_phrase: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return {
            "preflight_report_id": self.preflight_report_id,
            "static_safety_report_id": self.static_safety_report_id,
            "plan_id": self.plan_id,
            "action_candidate_id": self.action_candidate_id,
            "requested_review_decision": self.requested_review_decision,
            "reviewer_type": self.reviewer_type,
            "reviewer_ref": _clean(self.reviewer_ref),
            "decision_rationale": self.decision_rationale,
            "approval_phrase_present": bool(self.approval_phrase),
            "source_refs": [_clean(item) for item in self.source_refs],
            "strictness": self.strictness,
        }


@dataclass(frozen=True)
class DominionReviewSourceBundle:
    bundle_id: str
    preflight_report_ref: dict[str, Any] | None
    static_safety_report_ref: dict[str, Any] | None
    control_plan_ref: dict[str, Any] | None
    action_candidate_ref: dict[str, Any] | None
    inventory_ref: dict[str, Any] | None
    capability_report_ref: dict[str, Any] | None
    source_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    preflight_report: DominionRuntimePreflightReport | None = field(default=None, repr=False, compare=False)
    static_safety_report: DominionStaticSafetyReport | None = field(default=None, repr=False, compare=False)
    control_plan: DominionControlPlan | None = field(default=None, repr=False, compare=False)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "preflight_report_ref": _clean(self.preflight_report_ref),
            "static_safety_report_ref": _clean(self.static_safety_report_ref),
            "control_plan_ref": _clean(self.control_plan_ref),
            "action_candidate_ref": _clean(self.action_candidate_ref),
            "inventory_ref": _clean(self.inventory_ref),
            "capability_report_ref": _clean(self.capability_report_ref),
            "source_status": self.source_status,
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionReviewSummary:
    summary_id: str
    plan_id: str | None
    action_candidate_id: str | None
    goal_text: str | None
    provider_summary: str | None
    runtime_summary: str | None
    capability_summary: str | None
    environment: str | None
    risk_class: str
    production_impacting: bool
    destructive: bool
    credential_sensitive: bool
    static_safety_status: str | None
    preflight_status: str | None
    eligible_for_dominion_gate: bool
    safe_to_dispatch: bool = False
    summary_status: str = "ready_for_review"
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionReviewDecisionInput:
    decision_input_id: str
    requested_review_decision: str
    reviewer_type: str
    reviewer_ref: dict[str, Any] | None
    decision_rationale: str | None
    approval_phrase: str | None
    explicit_human_approval: bool
    approval_phrase_required: bool
    approval_phrase_matches: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "reviewer_ref": _clean(self.reviewer_ref),
            "approval_phrase": "<redacted>" if self.approval_phrase else None,
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionReviewDecision:
    decision_id: str
    created_at: str
    preflight_report_id: str
    plan_id: str | None
    decision: str
    reviewer_type: str
    explicit_human_approval: bool
    rationale_required: bool
    rationale_present: bool
    approval_phrase_required: bool
    approval_phrase_matches: bool
    decision_status: str
    dispatch_authorized: bool = False
    authorization_created: bool = False
    authorization_consumed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionGateCondition:
    condition_id: str
    condition_type: str
    description: str
    passed: bool
    severity_if_failed: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionGateState:
    gate_id: str
    created_at: str
    preflight_report_id: str
    plan_id: str | None
    action_candidate_id: str | None
    review_decision_id: str
    gate_status: str
    conditions: list[DominionGateCondition]
    condition_status: str
    authorized_next_stage: str | None = HUMAN_REVIEW_GATE_NEXT_STEP
    bounded_dispatch_allowed_now: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    dispatched: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "conditions": [item.to_dict() for item in self.conditions],
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionGateAuthorization:
    authorization_id: str
    created_at: str
    gate_id: str
    preflight_report_id: str
    plan_id: str | None
    action_candidate_id: str | None
    authorized_for_stage: str = "dominion_bounded_dispatch_boundary"
    authorized_next_version: str = "v0.23.8"
    scope: dict[str, Any] = field(default_factory=dict)
    single_use: bool = True
    consumed: bool = False
    expired: bool = False
    expires_at: str | None = None
    dispatch_performed: bool = False
    external_runtime_touched: bool = False
    provider_api_call_performed: bool = False
    credential_exposed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "scope": _clean(self.scope),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionGateFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    gate_ref: dict[str, Any] | None
    decision_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {
            "gate_ref": _clean(self.gate_ref),
            "decision_ref": _clean(self.decision_ref),
            "evidence_refs": [_clean(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class DominionGateReport:
    report_id: str
    version: str
    created_at: str
    review_source_bundle: DominionReviewSourceBundle
    review_summary: DominionReviewSummary
    decision_input: DominionReviewDecisionInput
    review_decision: DominionReviewDecision
    gate_state: DominionGateState | None
    authorization: DominionGateAuthorization | None
    findings: list[DominionGateFinding]
    report_status: str
    eligible_for_v0_23_8: bool
    safe_to_dispatch: bool = False
    bounded_dispatch_allowed_now: bool = False
    authorization_created: bool = False
    authorization_consumed: bool = False
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
    next_required_step: str = HUMAN_REVIEW_GATE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until review decision, preflight report, control plan, risk profile, or Dominion policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "created_at": self.created_at,
            "review_source_bundle": self.review_source_bundle.to_dict(),
            "review_summary": self.review_summary.to_dict(),
            "decision_input": self.decision_input.to_dict(),
            "review_decision": self.review_decision.to_dict(),
            "gate_state": self.gate_state.to_dict() if self.gate_state else None,
            "authorization": self.authorization.to_dict() if self.authorization else None,
            "findings": [item.to_dict() for item in self.findings],
            "report_status": self.report_status,
            "eligible_for_v0_23_8": self.eligible_for_v0_23_8,
            "safe_to_dispatch": self.safe_to_dispatch,
            "bounded_dispatch_allowed_now": self.bounded_dispatch_allowed_now,
            "authorization_created": self.authorization_created,
            "authorization_consumed": self.authorization_consumed,
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
class DominionGateNeedsMoreInputCandidate:
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
class DominionGateNoActionCandidate:
    candidate_id: str
    report_id: str | None
    reason: str
    evidence_refs: list[dict[str, Any]]
    recommended_review_decision: str = "no_action"
    candidate_status: str = "candidate_only"
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


@dataclass(frozen=True)
class DominionGateRejectionRecord:
    rejection_id: str
    report_id: str | None
    reason: str
    rejected_stage: str = "dominion_gate"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    dispatch_allowed: bool = False
    dispatched: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__) | {"evidence_refs": [_clean(item) for item in self.evidence_refs]}


class DominionGateSourceService:
    def __init__(self) -> None:
        self.preflight = DominionRuntimePreflightService()

    def load_preflight_report(self, preflight_report_id: str) -> DominionRuntimePreflightReport | None:
        if preflight_report_id == "missing":
            return None
        plan_id = "dominion_control_plan:v0.23.4"
        static_report_id: str | None = "dominion_static_safety_report:v0.23.5"
        mode = "declared_only"
        if preflight_report_id in {
            "not-eligible",
            "static-failed",
            "provider-api",
            "runtime-touch",
            "dispatch",
            "credential",
            "raw-secret",
            "production",
            "no-status",
        }:
            variants = {
                "not-eligible": ("missing", "dominion_static_safety_report:v0.23.5", "declared_only"),
                "static-failed": ("dominion_control_plan:v0.23.4", "failed", "declared_only"),
                "provider-api": ("provider-api", "dominion_static_safety_report:v0.23.5", "declared_only"),
                "runtime-touch": ("runtime-touch", "dominion_static_safety_report:v0.23.5", "declared_only"),
                "dispatch": ("dominion_control_plan:v0.23.4", "dominion_static_safety_report:v0.23.5", "live_read_only_future"),
                "credential": ("credential", "dominion_static_safety_report:v0.23.5", "declared_only"),
                "raw-secret": ("raw-secret", "dominion_static_safety_report:v0.23.5", "declared_only"),
                "production": ("production", "dominion_static_safety_report:v0.23.5", "declared_only"),
                "no-status": ("no-status", "dominion_static_safety_report:v0.23.5", "declared_only"),
            }
            plan_id, static_report_id, mode = variants[preflight_report_id]
        return self.preflight.check_preflight(
            DominionRuntimePreflightRequest(
                plan_id=plan_id,
                static_safety_report_id=static_report_id,
                preflight_mode=mode,
            )
        )

    def load_static_safety_report(self, static_safety_report_id: str | None, preflight: DominionRuntimePreflightReport | None) -> DominionStaticSafetyReport | None:
        return None if preflight is None else self.preflight.sources.load_static_safety_report(static_safety_report_id or preflight.static_safety_report_id, preflight.plan_id)

    def load_control_plan(self, plan_id: str | None, preflight: DominionRuntimePreflightReport | None) -> DominionControlPlan | None:
        if preflight is None:
            return None
        return self.preflight.sources.load_control_plan(plan_id or preflight.plan_id)

    def load_action_candidate(self, action_candidate_id: str | None, plan: DominionControlPlan | None) -> dict[str, Any] | None:
        if plan is None:
            return None
        return {"action_candidate_id": action_candidate_id or plan.action_candidate_id, "candidate_status": "candidate_only"}

    def build_source_bundle(self, request: DominionHumanReviewRequestCreateRequest) -> DominionReviewSourceBundle:
        preflight = self.load_preflight_report(request.preflight_report_id)
        static_report_id = request.static_safety_report_id
        if static_report_id is None and request.preflight_report_id in {"static-failed", "raw-secret"}:
            static_report_id = "failed" if request.preflight_report_id == "static-failed" else "blocked"
        static_report = self.load_static_safety_report(static_report_id, preflight)
        plan = self.load_control_plan(request.plan_id, preflight)
        action = self.load_action_candidate(request.action_candidate_id, plan)
        missing = [preflight is None, static_report is None, plan is None, action is None]
        source_status = "complete" if not any(missing) else ("missing" if preflight is None else "partial")
        return DominionReviewSourceBundle(
            bundle_id="dominion_review_source_bundle:v0.23.7",
            preflight_report_ref=_preflight_ref(preflight),
            static_safety_report_ref=_static_ref(static_report),
            control_plan_ref=_plan_ref(plan),
            action_candidate_ref=action,
            inventory_ref={"runtime_inventory_report_id": request.source_refs[0].get("inventory_report_id")} if request.source_refs else None,
            capability_report_ref={"capability_report_id": request.source_refs[0].get("capability_report_id")} if request.source_refs else None,
            source_status=source_status,
            evidence_refs=[{"policy": "v0.23.7_read_only_source_bundle"}],
            preflight_report=preflight,
            static_safety_report=static_report,
            control_plan=plan,
        )


class DominionReviewSummaryService:
    def build_summary(self, source_bundle: DominionReviewSourceBundle) -> DominionReviewSummary:
        plan = source_bundle.control_plan
        preflight = source_bundle.preflight_report
        static = source_bundle.static_safety_report
        risk_class = _risk_class(plan)
        production = bool(plan and plan.environment_binding.production_impacting)
        destructive = risk_class in {"destructive", "high_risk"}
        credential_sensitive = bool(plan and plan.runtime_binding.credential_sensitive)
        if source_bundle.source_status == "missing":
            status = "blocked"
        elif preflight and preflight.preflight_status in {"failed", "blocked"}:
            status = "blocked"
        elif static and static.static_safety_status in {"failed", "blocked"}:
            status = "blocked"
        elif preflight and preflight.preflight_status == "warning":
            status = "warning"
        else:
            status = "ready_for_review"
        return DominionReviewSummary(
            summary_id="dominion_review_summary:v0.23.7",
            plan_id=plan.plan_id if plan else None,
            action_candidate_id=plan.action_candidate_id if plan else None,
            goal_text=plan.goal_text if plan else None,
            provider_summary=plan.provider_binding.provider_type if plan else None,
            runtime_summary=plan.runtime_binding.runtime_type if plan else None,
            capability_summary=plan.capability_binding.capability_name if plan else None,
            environment=plan.environment_binding.environment if plan else None,
            risk_class=risk_class,
            production_impacting=production,
            destructive=destructive,
            credential_sensitive=credential_sensitive,
            static_safety_status=static.static_safety_status if static else None,
            preflight_status=preflight.preflight_status if preflight else None,
            eligible_for_dominion_gate=bool(preflight and preflight.eligible_for_dominion_gate),
            summary_status=status,
            raw_secret_output=bool((preflight and preflight.raw_secret_output) or (plan and plan.raw_secret_output)),
            evidence_refs=[{"source_bundle_id": source_bundle.bundle_id}],
        )


class DominionReviewDecisionService:
    def build_decision_input(
        self, request: DominionHumanReviewRequestCreateRequest, review_summary: DominionReviewSummary
    ) -> DominionReviewDecisionInput:
        decision = request.requested_review_decision or "unknown"
        if decision not in ALLOWED_DECISIONS:
            decision = "unknown"
        phrase_required = _requires_approval_phrase(review_summary)
        phrase_matches = bool(request.approval_phrase and request.approval_phrase.strip() == APPROVAL_PHRASE)
        explicit = bool(
            decision == "approve"
            and request.reviewer_type == "operator"
            and (request.decision_rationale or request.approval_phrase)
        )
        return DominionReviewDecisionInput(
            decision_input_id="dominion_review_decision_input:v0.23.7",
            requested_review_decision=decision,
            reviewer_type=request.reviewer_type if request.reviewer_type in {"operator", "system_policy", "delegated_reviewer", "unknown"} else "unknown",
            reviewer_ref=_clean(request.reviewer_ref),
            decision_rationale=request.decision_rationale,
            approval_phrase=request.approval_phrase,
            explicit_human_approval=explicit,
            approval_phrase_required=phrase_required,
            approval_phrase_matches=phrase_matches,
            evidence_refs=[{"policy": "explicit_review_input_only"}],
        )

    def record_review_decision(
        self, decision_input: DominionReviewDecisionInput, source_bundle: DominionReviewSourceBundle
    ) -> DominionReviewDecision:
        decision = decision_input.requested_review_decision
        rationale_required = decision in {"approve", "reject", "revise", "defer"}
        rationale_present = bool(decision_input.decision_rationale)
        if decision == "approve":
            if not decision_input.explicit_human_approval:
                decision_status = "blocked"
                decision = "blocked"
            elif decision_input.approval_phrase_required and not decision_input.approval_phrase_matches:
                decision_status = "rejected"
                decision = "reject"
            elif rationale_required and not rationale_present and not decision_input.approval_phrase:
                decision_status = "needs_more_input"
                decision = "needs_more_input"
            else:
                decision_status = "accepted"
        elif decision == "reject":
            decision_status = "rejected"
        elif decision == "no_action":
            decision_status = "rejected"
        elif decision == "needs_more_input":
            decision_status = "needs_more_input"
        elif decision in {"revise", "defer"}:
            decision_status = "needs_more_input"
        else:
            decision_status = "needs_more_input"
            decision = "needs_more_input"
        return DominionReviewDecision(
            decision_id="dominion_review_decision:v0.23.7",
            created_at=_now(),
            preflight_report_id=(source_bundle.preflight_report.report_id if source_bundle.preflight_report else "missing"),
            plan_id=(source_bundle.control_plan.plan_id if source_bundle.control_plan else None),
            decision=decision,
            reviewer_type=decision_input.reviewer_type,
            explicit_human_approval=decision_input.explicit_human_approval,
            rationale_required=rationale_required,
            rationale_present=rationale_present,
            approval_phrase_required=decision_input.approval_phrase_required,
            approval_phrase_matches=decision_input.approval_phrase_matches,
            decision_status=decision_status,
            evidence_refs=[{"decision_input_id": decision_input.decision_input_id}],
        )


class DominionGateConditionService:
    def build_conditions(
        self,
        source_bundle: DominionReviewSourceBundle,
        review_decision: DominionReviewDecision,
        review_summary: DominionReviewSummary,
    ) -> list[DominionGateCondition]:
        preflight = source_bundle.preflight_report
        static = source_bundle.static_safety_report
        plan = source_bundle.control_plan
        text = " ".join(str(item) for item in [
            review_decision.to_dict(),
            review_summary.to_dict(),
            source_bundle.to_dict(),
        ]).lower()
        conditions = [
            _condition("preflight_report_exists", preflight is not None, "critical"),
            _condition("preflight_eligible_for_gate", bool(preflight and preflight.eligible_for_dominion_gate), "critical"),
            _condition(
                "static_safety_passed_or_acceptable_warning",
                bool(static and static.static_safety_status in {"passed", "warning"}),
                "critical",
            ),
            _condition("control_plan_exists", plan is not None, "critical"),
            _condition("action_candidate_exists", bool(plan and plan.action_candidate_id), "critical"),
            _condition("no_provider_api_call", not bool(preflight and preflight.provider_api_call_performed), "critical"),
            _condition("no_external_runtime_touch", not bool(preflight and preflight.external_runtime_touched), "critical"),
            _condition("no_dispatch_yet", not bool(preflight and preflight.dispatched), "critical"),
            _condition("no_credential_exposure", not bool(preflight and preflight.credential_exposed), "critical"),
            _condition(
                "explicit_human_approval_required_for_approve",
                review_decision.decision != "approve" or review_decision.explicit_human_approval,
                "error",
            ),
            _condition(
                "approval_phrase_required_for_high_risk",
                not review_decision.approval_phrase_required or review_decision.approval_phrase_matches,
                "error",
            ),
            _condition(
                "approval_phrase_matches_if_required",
                not review_decision.approval_phrase_required or review_decision.approval_phrase_matches,
                "error",
            ),
            _condition(
                "strong_gate_required_for_production",
                not review_summary.production_impacting or review_decision.approval_phrase_matches,
                "warning",
            ),
            _condition("no_vendor_hardcoding_in_core", "vendor hardcoding" not in text, "critical"),
            _condition("no_growthkernel_dependency", "growthkernel dependency" not in text, "critical"),
            _condition("no_premature_local_runtime_provider", "local runtime provider attempted" not in text, "critical"),
            _condition("no_premature_general_agent_usability", "general agent usability attempted" not in text, "critical"),
            _condition("no_schumpeter_split", "schumpeter split attempted" not in text, "critical"),
        ]
        return conditions


class DominionGateEvaluationService:
    def evaluate_gate(
        self,
        source_bundle: DominionReviewSourceBundle,
        review_decision: DominionReviewDecision,
        conditions: list[DominionGateCondition],
    ) -> DominionGateState:
        condition_status = _condition_status(conditions)
        hard_failed = condition_status in {"failed", "blocked"}
        if hard_failed:
            gate_status = "blocked"
        elif review_decision.decision == "approve" and review_decision.decision_status == "accepted":
            gate_status = "open"
        elif review_decision.decision == "no_action":
            gate_status = "no_action"
        elif review_decision.decision == "needs_more_input":
            gate_status = "needs_more_input"
        elif review_decision.decision in {"reject", "blocked"}:
            gate_status = "rejected" if review_decision.decision == "reject" else "blocked"
        else:
            gate_status = "needs_more_input"
        return DominionGateState(
            gate_id="dominion_gate_state:v0.23.7",
            created_at=_now(),
            preflight_report_id=(source_bundle.preflight_report.report_id if source_bundle.preflight_report else "missing"),
            plan_id=(source_bundle.control_plan.plan_id if source_bundle.control_plan else None),
            action_candidate_id=(source_bundle.control_plan.action_candidate_id if source_bundle.control_plan else None),
            review_decision_id=review_decision.decision_id,
            gate_status=gate_status,
            conditions=conditions,
            condition_status=condition_status,
            evidence_refs=[{"policy": "gate_state_only_no_dispatch"}],
        )


class DominionGateAuthorizationService:
    def create_authorization(
        self,
        gate_state: DominionGateState,
        review_decision: DominionReviewDecision,
        source_bundle: DominionReviewSourceBundle,
    ) -> DominionGateAuthorization | None:
        if gate_state.gate_status != "open" or review_decision.decision != "approve":
            return None
        plan = source_bundle.control_plan
        scope = {
            "preflight_report_id": gate_state.preflight_report_id,
            "plan_id": gate_state.plan_id,
            "action_candidate_id": gate_state.action_candidate_id,
            "provider_ref_id": plan.provider_binding.provider_ref_id if plan else None,
            "runtime_id": plan.runtime_binding.runtime_id if plan else None,
            "capability_candidate_id": plan.capability_binding.capability_candidate_id if plan else None,
            "authorized_next_version": "v0.23.8",
            "provider_api_call_allowed": False,
            "dispatch_allowed_now": False,
        }
        return DominionGateAuthorization(
            authorization_id="dominion_gate_authorization:v0.23.7",
            created_at=_now(),
            gate_id=gate_state.gate_id,
            preflight_report_id=gate_state.preflight_report_id,
            plan_id=gate_state.plan_id,
            action_candidate_id=gate_state.action_candidate_id,
            scope=scope,
            evidence_refs=[{"review_decision_id": review_decision.decision_id}],
        )


class DominionGateFindingService:
    def build_findings(
        self,
        source_bundle: DominionReviewSourceBundle,
        review_decision: DominionReviewDecision,
        gate_state: DominionGateState,
        authorization: DominionGateAuthorization | None,
        decision_input: DominionReviewDecisionInput,
        request: DominionHumanReviewRequestCreateRequest,
    ) -> list[DominionGateFinding]:
        findings: list[DominionGateFinding] = []
        for condition in gate_state.conditions:
            if not condition.passed:
                findings.append(_finding(condition.severity_if_failed, _condition_finding_type(condition.condition_type), gate_state, review_decision))
        if decision_input.requested_review_decision == "approve" and not decision_input.explicit_human_approval:
            findings.append(_finding("error", "explicit_human_approval_missing", gate_state, review_decision))
        if decision_input.approval_phrase_required and not decision_input.approval_phrase:
            findings.append(_finding("error", "approval_phrase_missing", gate_state, review_decision))
        if decision_input.approval_phrase_required and decision_input.approval_phrase and not decision_input.approval_phrase_matches:
            findings.append(_finding("error", "approval_phrase_mismatch", gate_state, review_decision))
        if gate_state.gate_status == "open":
            findings.append(_finding("info", "gate_opened", gate_state, review_decision))
        elif gate_state.gate_status == "rejected":
            findings.append(_finding("warning", "gate_rejected", gate_state, review_decision))
        elif gate_state.gate_status == "needs_more_input":
            findings.append(_finding("warning", "gate_needs_more_input", gate_state, review_decision))
        elif gate_state.gate_status == "no_action":
            findings.append(_finding("info", "gate_no_action", gate_state, review_decision))
        if authorization:
            findings.append(_finding("info", "authorization_created", gate_state, review_decision))
        else:
            findings.append(_finding("info", "authorization_not_created", gate_state, review_decision))
        findings.extend(_source_text_findings(request, gate_state, review_decision))
        if not findings:
            findings.append(_finding("info", "ok", gate_state, review_decision))
        return findings


class DominionGateReportService:
    def __init__(self) -> None:
        self.sources = DominionGateSourceService()
        self.summary = DominionReviewSummaryService()
        self.decisions = DominionReviewDecisionService()
        self.conditions = DominionGateConditionService()
        self.evaluation = DominionGateEvaluationService()
        self.authorization = DominionGateAuthorizationService()
        self.findings = DominionGateFindingService()

    def build_report(self, request: DominionHumanReviewRequestCreateRequest | None = None) -> DominionGateReport:
        request = request or DominionHumanReviewRequestCreateRequest()
        bundle = self.sources.build_source_bundle(request)
        summary = self.summary.build_summary(bundle)
        decision_input = self.decisions.build_decision_input(request, summary)
        decision = self.decisions.record_review_decision(decision_input, bundle)
        conditions = self.conditions.build_conditions(bundle, decision, summary)
        gate_state = self.evaluation.evaluate_gate(bundle, decision, conditions)
        authorization = self.authorization.create_authorization(gate_state, decision, bundle)
        findings = self.findings.build_findings(bundle, decision, gate_state, authorization, decision_input, request)
        report_status = gate_state.gate_status
        provider_api_call = bool(bundle.preflight_report and bundle.preflight_report.provider_api_call_performed)
        runtime_touched = bool(bundle.preflight_report and bundle.preflight_report.external_runtime_touched)
        credential_exposed = bool(bundle.preflight_report and bundle.preflight_report.credential_exposed)
        raw_secret_output = bool(bundle.preflight_report and bundle.preflight_report.raw_secret_output)
        return DominionGateReport(
            report_id="dominion_gate_report:v0.23.7",
            version=HUMAN_REVIEW_GATE_VERSION,
            created_at=_now(),
            review_source_bundle=bundle,
            review_summary=summary,
            decision_input=decision_input,
            review_decision=decision,
            gate_state=gate_state,
            authorization=authorization,
            findings=findings,
            report_status=report_status,
            eligible_for_v0_23_8=bool(gate_state.gate_status == "open" and authorization is not None),
            authorization_created=authorization is not None,
            provider_api_call_performed=provider_api_call,
            external_runtime_touched=runtime_touched,
            credential_exposed=credential_exposed,
            raw_secret_output=raw_secret_output,
            limitations=[
                "v0.23.7 creates review, gate state, and optional single-use authorization artifacts only.",
                "Authorization is not consumed and bounded dispatch remains deferred to v0.23.8.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider API calls, runtime touch, dispatch, authorization consumption, credential output, local command execution, or LLM judge behavior is introduced.",
                "Withdraw if v0.23.7 implements v0.24+ roadmap items or company-specific Schumpeter split logic.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": HUMAN_REVIEW_GATE_VERSION,
            "layer": HUMAN_REVIEW_GATE_LAYER,
            "subject": HUMAN_REVIEW_GATE_SUBJECT,
            "principles": [
                "human review is not dispatch",
                "dominion gate is not dispatch",
                "gate authorization is not execution",
                "gate authorization is single-use and scoped",
                "approval is not sufficient without v0.23.8 boundary handling",
                "no-action and needs-more-input are valid review outcomes",
            ],
            "safety_boundary": {
                "gate_state_created": True,
                "authorization_created": "conditional",
                "authorization_consumed": False,
                "safe_to_dispatch": False,
                "bounded_dispatch_allowed_now": False,
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
            "next_step": HUMAN_REVIEW_GATE_NEXT_STEP,
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
            "state": HUMAN_REVIEW_GATE_STATE,
            "version": HUMAN_REVIEW_GATE_VERSION,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionRuntimePreflightState",
                "DominionStaticSafetyState",
                "DominionControlPlanState",
                "ExternalActionCandidateState",
            ],
            "target_read_models": [
                "DominionHumanReviewState",
                "DominionGateState",
                "DominionGateAuthorizationState",
                "DominionV0238EligibilityState",
                "DominionRoadmapBoundaryState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_report_cli(self, report: DominionGateReport | None = None, section: str = "summary") -> str:
        report = report or self.build_report()
        auth = report.authorization
        lines = [
            "Dominion Human Review & Gate",
            f"version={report.version}",
            f"layer={HUMAN_REVIEW_GATE_LAYER}",
            f"report_id={report.report_id}",
            f"gate_id={report.gate_state.gate_id if report.gate_state else 'missing'}",
            f"gate_status={report.gate_state.gate_status if report.gate_state else 'missing'}",
            f"review_decision={report.review_decision.decision}",
            f"authorization_id={auth.authorization_id if auth else 'none'}",
            f"authorization.single_use={str(auth.single_use if auth else False).lower()}",
            f"authorization.consumed={str(auth.consumed if auth else False).lower()}",
            f"eligible_for_v0_23_8={str(report.eligible_for_v0_23_8).lower()}",
            f"safe_to_dispatch={str(report.safe_to_dispatch).lower()}",
            f"bounded_dispatch_allowed_now={str(report.bounded_dispatch_allowed_now).lower()}",
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
        elif section == "state" and report.gate_state:
            lines.extend(
                f"- condition={item.condition_type} passed={str(item.passed).lower()} severity={item.severity_if_failed}"
                for item in report.gate_state.conditions
            )
        elif section == "authorization" and auth:
            lines.extend(
                [
                    f"authorized_for_stage={auth.authorized_for_stage}",
                    f"authorized_next_version={auth.authorized_next_version}",
                    f"scope.preflight_report_id={auth.scope.get('preflight_report_id')}",
                    f"scope.plan_id={auth.scope.get('plan_id')}",
                    f"scope.action_candidate_id={auth.scope.get('action_candidate_id')}",
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

    def create_needs_more_input_candidate(self, report: DominionGateReport, reason: str = "missing review input") -> DominionGateNeedsMoreInputCandidate:
        return DominionGateNeedsMoreInputCandidate(
            candidate_id="dominion_gate_needs_more_input_candidate:v0.23.7",
            report_id=report.report_id,
            reason=reason,
            missing_inputs=["decision_rationale"],
            evidence_refs=[{"report_id": report.report_id}],
        )

    def create_no_action_candidate(self, report: DominionGateReport, reason: str = "review selected no_action") -> DominionGateNoActionCandidate:
        return DominionGateNoActionCandidate(
            candidate_id="dominion_gate_no_action_candidate:v0.23.7",
            report_id=report.report_id,
            reason=reason,
            evidence_refs=[{"report_id": report.report_id}],
        )

    def create_rejection_record(self, report: DominionGateReport, reason: str = "review rejected") -> DominionGateRejectionRecord:
        return DominionGateRejectionRecord(
            rejection_id="dominion_gate_rejection_record:v0.23.7",
            report_id=report.report_id,
            reason=reason,
            evidence_refs=[{"report_id": report.report_id}],
        )


class DominionHumanReviewGateService(DominionGateReportService):
    def review_and_gate(self, request: DominionHumanReviewRequestCreateRequest | None = None) -> DominionGateReport:
        return self.build_report(request)


def _condition(condition_type: str, passed: bool, severity: str) -> DominionGateCondition:
    return DominionGateCondition(
        condition_id=f"dominion_gate_condition:{condition_type}",
        condition_type=condition_type,
        description=condition_type.replace("_", " "),
        passed=passed,
        severity_if_failed=severity,
        evidence_refs=[{"policy": "v0.23.7_gate_condition"}],
    )


def _condition_status(conditions: list[DominionGateCondition]) -> str:
    severities = {item.severity_if_failed for item in conditions if not item.passed}
    if "critical" in severities:
        return "blocked"
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warning"
    return "passed"


def _condition_finding_type(condition_type: str) -> str:
    mapping = {
        "preflight_report_exists": "missing_preflight_report",
        "preflight_eligible_for_gate": "preflight_not_eligible",
        "static_safety_passed_or_acceptable_warning": "static_safety_not_passed",
        "control_plan_exists": "missing_control_plan",
        "action_candidate_exists": "missing_action_candidate",
        "no_provider_api_call": "provider_api_call_performed",
        "no_external_runtime_touch": "external_runtime_touched",
        "no_dispatch_yet": "dispatch_attempted",
        "no_credential_exposure": "credential_exposure_risk",
        "strong_gate_required_for_production": "production_action_requires_strong_gate",
        "no_vendor_hardcoding_in_core": "vendor_hardcoding_detected",
        "no_growthkernel_dependency": "growthkernel_dependency_detected",
        "no_premature_local_runtime_provider": "premature_local_runtime_provider_detected",
        "no_premature_general_agent_usability": "premature_general_agent_usability_detected",
        "no_schumpeter_split": "schumpeter_split_detected",
    }
    return mapping.get(condition_type, condition_type)


def _finding(severity: str, finding_type: str, gate: DominionGateState, decision: DominionReviewDecision) -> DominionGateFinding:
    return DominionGateFinding(
        finding_id=f"dominion_gate_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=finding_type.replace("_", " "),
        gate_ref={"gate_id": gate.gate_id, "gate_status": gate.gate_status},
        decision_ref={"decision_id": decision.decision_id, "decision": decision.decision},
        evidence_refs=[{"policy": "v0.23.7_review_gate_only"}],
        withdrawal_condition="Withdraw if review decision, preflight report, control plan, or Dominion policy changes.",
    )


def _source_text_findings(
    request: DominionHumanReviewRequestCreateRequest,
    gate: DominionGateState,
    decision: DominionReviewDecision,
) -> list[DominionGateFinding]:
    text = " ".join(str(value) for value in request.to_dict().values()).lower()
    findings: list[DominionGateFinding] = []
    markers = [
        ("self_execution", "self_execution_legacy_detected", "error"),
        ("self-execution safety", "self_execution_legacy_detected", "error"),
        ("growthkernel dependency", "growthkernel_dependency_detected", "error"),
        ("requires growthkernel", "growthkernel_dependency_detected", "error"),
        ("vendor hardcoding", "vendor_hardcoding_detected", "critical"),
        ("provider api call performed", "provider_api_call_performed", "critical"),
        ("external runtime touched", "external_runtime_touched", "critical"),
        ("dispatch attempted", "dispatch_attempted", "critical"),
        ("authorization consumed", "authorization_consumed_too_early", "critical"),
        ("local runtime provider attempted", "premature_local_runtime_provider_detected", "critical"),
        ("general agent usability attempted", "premature_general_agent_usability_detected", "critical"),
        ("schumpeter split attempted", "schumpeter_split_detected", "critical"),
    ]
    seen: set[str] = set()
    for marker, finding_type, severity in markers:
        if marker in text and finding_type not in seen:
            findings.append(_finding(severity, finding_type, gate, decision))
            seen.add(finding_type)
    return findings


def _preflight_ref(report: DominionRuntimePreflightReport | None) -> dict[str, Any] | None:
    if report is None:
        return None
    return {
        "report_id": report.report_id,
        "preflight_status": report.preflight_status,
        "eligible_for_dominion_gate": report.eligible_for_dominion_gate,
    }


def _static_ref(report: DominionStaticSafetyReport | None) -> dict[str, Any] | None:
    if report is None:
        return None
    return {"report_id": report.report_id, "static_safety_status": report.static_safety_status}


def _plan_ref(plan: DominionControlPlan | None) -> dict[str, Any] | None:
    if plan is None:
        return None
    return {
        "plan_id": plan.plan_id,
        "action_candidate_id": plan.action_candidate_id,
        "plan_status": plan.plan_status,
    }


def _risk_class(plan: DominionControlPlan | None) -> str:
    if plan is None:
        return "unknown"
    risk_ref = plan.capability_binding.risk_profile_ref or {}
    risk = str(risk_ref.get("risk_class") or risk_ref.get("risk_level") or "")
    if risk:
        return risk
    if plan.environment_binding.production_impacting:
        return "production"
    if plan.runtime_binding.credential_sensitive:
        return "credential_sensitive"
    return "read_only"


def _requires_approval_phrase(summary: DominionReviewSummary) -> bool:
    return bool(
        summary.production_impacting
        or summary.destructive
        or summary.credential_sensitive
        or summary.risk_class in HIGH_RISK_CLASSES
    )
