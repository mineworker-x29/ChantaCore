from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.authority import (
    DominionAuthorityDecision,
    DominionAuthorityDecisionType,
    DominionAuthorityScope,
    decision_preserves_v0304_boundary,
)
from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level


class ExternalDelegationIntentKind(StrEnum):
    INSPECT_EXTERNAL_CAPABILITY = "inspect_external_capability"
    SUMMARIZE_EXTERNAL_HARNESS = "summarize_external_harness"
    COMPARE_EXTERNAL_SKILL = "compare_external_skill"
    VALIDATE_EXTERNAL_CLAIM = "validate_external_claim"
    ANALYZE_EXTERNAL_TRACE = "analyze_external_trace"
    PROPOSE_INTERNALIZATION = "propose_internalization"
    REVIEW_DOMINION_TARGET = "review_dominion_target"
    SIMULATE_EXTERNAL_RESPONSE = "simulate_external_response"
    UNKNOWN = "unknown"


class ExternalDelegationCandidateStatus(StrEnum):
    UNKNOWN = "unknown"
    CANDIDATE = "candidate"
    DRAFT_PACKET = "draft_packet"
    DRY_RUN_PLANNED = "dry_run_planned"
    DRY_RUN_REPORTED = "dry_run_reported"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


V0305_MAX_ALLOWED_LEVEL = DominionLevel.D3_SIMULATE

DANGEROUS_DELEGATION_TERMS = frozenset(
    {
        "private",
        "secret",
        "credential",
        "network",
        "provider",
        "gateway",
        "rpa",
        "browser",
        "command",
        "shell",
        "delegation",
        "external_side_effect",
    }
)


def _require_non_blank(name: str, value: str) -> None:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must not be blank")


def _validate_string_list(name: str, values: list[str]) -> None:
    if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
        raise TypeError(f"{name} must be list[str]")


def _contains_risk_term(values: list[str] | dict[str, Any]) -> bool:
    if isinstance(values, dict):
        text = " ".join(str(item).lower() for pair in values.items() for item in pair)
    else:
        text = " ".join(str(item).lower() for item in values)
    return any(term in text for term in DANGEROUS_DELEGATION_TERMS)


def _unique(values: list[str]) -> list[str]:
    result: list[str] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def normalize_delegation_intent_kind(value: ExternalDelegationIntentKind | str) -> ExternalDelegationIntentKind:
    if isinstance(value, ExternalDelegationIntentKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("intent_kind must not be blank")
        return ExternalDelegationIntentKind(stripped)
    raise TypeError(f"unsupported delegation intent kind: {value!r}")


def normalize_delegation_candidate_status(
    value: ExternalDelegationCandidateStatus | str,
) -> ExternalDelegationCandidateStatus:
    if isinstance(value, ExternalDelegationCandidateStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("status must not be blank")
        return ExternalDelegationCandidateStatus(stripped)
    raise TypeError(f"unsupported delegation candidate status: {value!r}")


@dataclass(frozen=True)
class ExternalDelegationIntent:
    intent_id: str
    target_id: str
    intent_kind: ExternalDelegationIntentKind | str
    goal_summary: str
    reason: str
    source_decision_ids: list[str] = field(default_factory=list)
    source_candidate_ids: list[str] = field(default_factory=list)
    source_report_ids: list[str] = field(default_factory=list)
    requested_level: DominionLevel | int | str = DominionLevel.D2_PLAN
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("intent_id", self.intent_id)
        _require_non_blank("target_id", self.target_id)
        normalize_delegation_intent_kind(self.intent_kind)
        _require_non_blank("goal_summary", self.goal_summary)
        _require_non_blank("reason", self.reason)
        _validate_string_list("source_decision_ids", self.source_decision_ids)
        _validate_string_list("source_candidate_ids", self.source_candidate_ids)
        _validate_string_list("source_report_ids", self.source_report_ids)
        _validate_string_list("evidence_refs", self.evidence_refs)
        normalize_dominion_level(self.requested_level)

    @property
    def creates_delegation_runtime(self) -> bool:
        return False

    @property
    def triggers_execution(self) -> bool:
        return False

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationInputEnvelope:
    envelope_id: str
    candidate_id: str
    target_id: str
    context_summary: str
    structured_inputs: dict[str, Any] = field(default_factory=dict)
    allowed_capability_refs: list[str] = field(default_factory=list)
    prohibited_capabilities: list[str] = field(default_factory=list)
    object_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    data_boundary_notes: list[str] = field(default_factory=list)
    redaction_required: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("envelope_id", self.envelope_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("context_summary", self.context_summary)
        if not isinstance(self.structured_inputs, dict):
            raise TypeError("structured_inputs must be a dict")
        _validate_string_list("allowed_capability_refs", self.allowed_capability_refs)
        _validate_string_list("prohibited_capabilities", self.prohibited_capabilities)
        _validate_string_list("object_refs", self.object_refs)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("data_boundary_notes", self.data_boundary_notes)
        risk_present = any(
            (
                _contains_risk_term(self.prohibited_capabilities),
                _contains_risk_term(self.data_boundary_notes),
                _contains_risk_term(self.structured_inputs),
                _contains_risk_term(self.metadata),
            )
        )
        if risk_present and self.redaction_required is not True:
            raise ValueError("redaction_required must be true when high-risk delegation data is present")

    @property
    def packet_sent(self) -> bool:
        return False

    @property
    def submitted_to_external_runtime(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationExpectedOutputSchema:
    schema_id: str
    candidate_id: str
    target_id: str
    required_fields: list[str]
    optional_fields: list[str] = field(default_factory=list)
    forbidden_fields: list[str] = field(default_factory=lambda: ["raw_output", "credential_value", "secret_value"])
    evidence_required: bool = True
    raw_output_allowed: bool = False
    result_envelope_required: bool = True
    max_summary_length: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("schema_id", self.schema_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("required_fields", self.required_fields)
        _validate_string_list("optional_fields", self.optional_fields)
        _validate_string_list("forbidden_fields", self.forbidden_fields)
        if self.raw_output_allowed is not False:
            raise ValueError("raw_output_allowed must remain False in v0.30.5")
        if self.result_envelope_required is not True:
            raise ValueError("result_envelope_required must remain True in v0.30.5")
        if self.evidence_required is not True:
            raise ValueError("evidence_required must remain True in v0.30.5")
        if self.max_summary_length is not None and self.max_summary_length <= 0:
            raise ValueError("max_summary_length must be positive when provided")

    @property
    def is_external_output(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationEffectPreview:
    preview_id: str
    candidate_id: str
    target_id: str
    expected_effect_surfaces: list[str] = field(default_factory=list)
    expected_boundary_surfaces: list[str] = field(default_factory=list)
    expected_risk_signals: list[str] = field(default_factory=list)
    side_effect_free_expected: bool = True
    private_data_possible: bool = False
    credential_exposure_possible: bool = False
    network_effect_possible: bool = False
    command_effect_possible: bool = False
    provider_effect_possible: bool = False
    browser_effect_possible: bool = False
    rpa_effect_possible: bool = False
    gateway_effect_possible: bool = False
    delegation_effect_possible: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_id", self.preview_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("expected_effect_surfaces", self.expected_effect_surfaces)
        _validate_string_list("expected_boundary_surfaces", self.expected_boundary_surfaces)
        _validate_string_list("expected_risk_signals", self.expected_risk_signals)
        if self.any_dangerous_effect_possible and self.side_effect_free_expected is not False:
            raise ValueError("dangerous effect flags require side_effect_free_expected=False")

    @property
    def any_dangerous_effect_possible(self) -> bool:
        return any(
            (
                self.credential_exposure_possible,
                self.network_effect_possible,
                self.command_effect_possible,
                self.provider_effect_possible,
                self.browser_effect_possible,
                self.rpa_effect_possible,
                self.gateway_effect_possible,
                self.delegation_effect_possible,
            )
        )

    @property
    def descriptive_only(self) -> bool:
        return True


@dataclass(frozen=True)
class ExternalDelegationRiskPreview:
    risk_preview_id: str
    candidate_id: str
    target_id: str
    risk_signals: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    required_reviews: list[str] = field(default_factory=list)
    future_gate_required: bool = False
    human_approval_required: bool = False
    no_op_recommended: bool = False
    rationale: str = "Delegation risk preview is conservative."
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_preview_id", self.risk_preview_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("risk_signals", self.risk_signals)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("required_reviews", self.required_reviews)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _require_non_blank("rationale", self.rationale)
        high_risk = _contains_risk_term(self.risk_signals + self.blocked_reasons)
        if high_risk and not (self.future_gate_required or self.human_approval_required):
            raise ValueError("high-risk external delegation requires future_gate_required or human_approval_required")

    @property
    def approval_granted(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False

    @property
    def blocks_by_itself(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationCandidate:
    candidate_id: str
    target_id: str
    intent: ExternalDelegationIntent
    input_envelope: ExternalDelegationInputEnvelope
    expected_output_schema: ExternalDelegationExpectedOutputSchema
    effect_preview: ExternalDelegationEffectPreview
    risk_preview: ExternalDelegationRiskPreview
    status: ExternalDelegationCandidateStatus | str
    requested_level: DominionLevel | int | str
    max_allowed_level: DominionLevel | int | str
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        status = normalize_delegation_candidate_status(self.status)
        if self.intent.target_id != self.target_id:
            raise ValueError("intent target_id must match delegation candidate target_id")
        for nested in (
            self.input_envelope,
            self.expected_output_schema,
            self.effect_preview,
            self.risk_preview,
        ):
            if nested.target_id != self.target_id:
                raise ValueError("nested target_id must match delegation candidate target_id")
            if nested.candidate_id != self.candidate_id:
                raise ValueError("nested candidate_id must match delegation candidate candidate_id")
        requested = normalize_dominion_level(self.requested_level)
        max_allowed = normalize_dominion_level(self.max_allowed_level)
        if max_allowed > V0305_MAX_ALLOWED_LEVEL:
            raise ValueError("v0.30.5 delegation max_allowed_level cannot exceed D3_SIMULATE")
        if requested == DominionLevel.D8_DELEGATE_AGENT and max_allowed > V0305_MAX_ALLOWED_LEVEL:
            raise ValueError("D8_DELEGATE_AGENT cannot raise max_allowed_level above D3_SIMULATE")
        if status not in set(ExternalDelegationCandidateStatus):
            raise ValueError("unsupported delegation candidate status")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)

    @property
    def grants_delegation_authority(self) -> bool:
        return False

    @property
    def creates_runtime(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationDryRunStep:
    step_id: str
    candidate_id: str
    order: int
    description: str
    simulated_action: str
    expected_artifact: str
    uses_external_runtime: bool = False
    uses_network: bool = False
    uses_credentials: bool = False
    uses_command: bool = False
    uses_browser: bool = False
    uses_rpa: bool = False
    uses_gateway: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("step_id", self.step_id)
        _require_non_blank("candidate_id", self.candidate_id)
        if self.order < 0:
            raise ValueError("order must be >= 0")
        _require_non_blank("description", self.description)
        _require_non_blank("simulated_action", self.simulated_action)
        _require_non_blank("expected_artifact", self.expected_artifact)
        if any(
            (
                self.uses_external_runtime,
                self.uses_network,
                self.uses_credentials,
                self.uses_command,
                self.uses_browser,
                self.uses_rpa,
                self.uses_gateway,
            )
        ):
            raise ValueError("all uses_* flags must be False in v0.30.5")
        lowered = self.simulated_action.lower()
        if any(term in lowered for term in ("execute ", "invoke ", "spawn ", "submit ", "transmit ", "contact ")):
            raise ValueError("simulated_action must not imply actual execution")

    @property
    def simulation_plan_only(self) -> bool:
        return True


@dataclass(frozen=True)
class ExternalDelegationDryRunPlan:
    plan_id: str
    candidate_id: str
    target_id: str
    steps: list[ExternalDelegationDryRunStep]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_execution_guarantee: bool
    no_external_contact_guarantee: bool
    no_credential_use_guarantee: bool
    no_network_use_guarantee: bool
    no_command_use_guarantee: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("plan_id", self.plan_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        if not isinstance(self.steps, list):
            raise TypeError("steps must be a list")
        if any(step.candidate_id != self.candidate_id for step in self.steps):
            raise ValueError("all dry-run step candidate_ids must match plan candidate_id")
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.no_execution_guarantee is not True:
            raise ValueError("no_execution_guarantee must be True")
        if self.no_external_contact_guarantee is not True:
            raise ValueError("no_external_contact_guarantee must be True")
        if self.no_credential_use_guarantee is not True:
            raise ValueError("no_credential_use_guarantee must be True")
        if self.no_network_use_guarantee is not True:
            raise ValueError("no_network_use_guarantee must be True")
        if self.no_command_use_guarantee is not True:
            raise ValueError("no_command_use_guarantee must be True")

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationDryRunReport:
    report_id: str
    plan_id: str
    candidate_id: str
    target_id: str
    simulated_steps_completed: list[str]
    simulated_findings: list[str]
    blocked_reasons: list[str]
    no_op_recommended: bool
    future_gate_required: bool
    ready_for_v0306_approval_boundary: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("plan_id", self.plan_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _validate_string_list("simulated_steps_completed", self.simulated_steps_completed)
        _validate_string_list("simulated_findings", self.simulated_findings)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("evidence_refs", self.evidence_refs)

    @property
    def derived_from_plan_only(self) -> bool:
        return True

    @property
    def is_external_runtime_output(self) -> bool:
        return False

    @property
    def approval_granted(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationNoOpPlan:
    no_op_id: str
    candidate_id: str
    target_id: str
    reason: str
    blocked_reasons: list[str] = field(default_factory=list)
    alternative_safe_actions: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("no_op_id", self.no_op_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("reason", self.reason)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("alternative_safe_actions", self.alternative_safe_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)

    @property
    def is_failure(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalDelegationHandoffPreview:
    handoff_id: str
    candidate_id: str
    target_id: str
    dry_run_plan_id: str | None
    dry_run_report_id: str | None
    no_op_plan_id: str | None
    next_stage: str
    ready_for_v0306_approval_audit_boundary: bool
    ready_for_execution: bool
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("handoff_id", self.handoff_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("target_id", self.target_id)
        _require_non_blank("next_stage", self.next_stage)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.30.5")
        allowed = ("v0.30.6", "no_op", "future_track")
        if not any(self.next_stage.startswith(prefix) for prefix in allowed):
            raise ValueError("next_stage must point to v0.30.6, no_op, or future_track")

    @property
    def executes_handoff(self) -> bool:
        return False


def make_external_delegation_intent_from_authority_decision(
    decision: DominionAuthorityDecision,
) -> ExternalDelegationIntent | None:
    if not decision_preserves_v0304_boundary(decision):
        return None
    decision_type = DominionAuthorityDecisionType(decision.decision)
    if decision_type in {DominionAuthorityDecisionType.DENY, DominionAuthorityDecisionType.NO_OP}:
        return None
    intent_kind = (
        ExternalDelegationIntentKind.SIMULATE_EXTERNAL_RESPONSE
        if decision_type is DominionAuthorityDecisionType.SIMULATE_ONLY
        else ExternalDelegationIntentKind.REVIEW_DOMINION_TARGET
    )
    return ExternalDelegationIntent(
        intent_id=f"external_delegation_intent:{decision.decision_id}",
        target_id=decision.target_id,
        intent_kind=intent_kind,
        goal_summary="Model a possible future external delegation without external contact.",
        reason=f"Derived from authority decision {decision.decision}; not permission.",
        source_decision_ids=[decision.decision_id],
        source_candidate_ids=[],
        source_report_ids=[],
        requested_level=decision.requested_level,
        evidence_refs=list(decision.evidence_refs),
        metadata={
            "approval_required": decision.approval_required,
            "human_review_required": decision.human_review_required,
            "future_gate_required": decision.future_gate_required,
            "blocked_reasons": list(decision.blocked_reasons),
            "decision": str(decision.decision),
            "v0305_contract_only": True,
        },
    )


def build_delegation_input_envelope(
    intent: ExternalDelegationIntent,
    prohibited_capabilities: list[str] | None = None,
    structured_inputs: dict[str, Any] | None = None,
) -> ExternalDelegationInputEnvelope:
    prohibited = list(
        prohibited_capabilities
        if prohibited_capabilities is not None
        else [
            "external runtime contact",
            "provider invocation",
            "network access",
            "credential access",
            "command execution",
            "browser automation",
            "RPA control",
            "gateway message control",
            "delegation execution",
        ]
    )
    structured = dict(structured_inputs or {"goal_summary": intent.goal_summary, "reason": intent.reason})
    redaction_required = _contains_risk_term(prohibited) or _contains_risk_term(structured) or bool(intent.metadata.get("approval_required"))
    return ExternalDelegationInputEnvelope(
        envelope_id=f"external_delegation_input_envelope:{intent.intent_id}",
        candidate_id=f"external_delegation_candidate:{intent.intent_id}",
        target_id=intent.target_id,
        context_summary=intent.goal_summary,
        structured_inputs=structured,
        allowed_capability_refs=[],
        prohibited_capabilities=prohibited,
        object_refs=list(intent.source_candidate_ids + intent.source_report_ids),
        evidence_refs=list(intent.evidence_refs),
        data_boundary_notes=["redact private, credential, provider, network, gateway, RPA, browser, and command surfaces"],
        redaction_required=redaction_required,
        metadata={"v0305_contract_only": True},
    )


def build_expected_output_schema(
    candidate_or_intent: ExternalDelegationCandidate | ExternalDelegationIntent,
) -> ExternalDelegationExpectedOutputSchema:
    candidate_id = (
        candidate_or_intent.candidate_id
        if isinstance(candidate_or_intent, ExternalDelegationCandidate)
        else f"external_delegation_candidate:{candidate_or_intent.intent_id}"
    )
    return ExternalDelegationExpectedOutputSchema(
        schema_id=f"external_delegation_expected_output_schema:{candidate_id}",
        candidate_id=candidate_id,
        target_id=candidate_or_intent.target_id,
        required_fields=["summary", "evidence_refs", "boundary_notes"],
        optional_fields=["risk_notes", "open_questions"],
        forbidden_fields=["raw_output", "credential_value", "secret_value", "unredacted_private_data"],
        evidence_required=True,
        raw_output_allowed=False,
        result_envelope_required=True,
        max_summary_length=4000,
        metadata={"schema_only": True, "v0305_contract_only": True},
    )


def preview_delegation_effects(
    candidate_or_intent: ExternalDelegationCandidate | ExternalDelegationIntent,
) -> ExternalDelegationEffectPreview:
    candidate_id = (
        candidate_or_intent.candidate_id
        if isinstance(candidate_or_intent, ExternalDelegationCandidate)
        else f"external_delegation_candidate:{candidate_or_intent.intent_id}"
    )
    metadata = candidate_or_intent.metadata
    high_risk = bool(
        metadata.get("future_gate_required")
        or metadata.get("approval_required")
        or metadata.get("human_review_required")
        or metadata.get("blocked_reasons")
    )
    return ExternalDelegationEffectPreview(
        preview_id=f"external_delegation_effect_preview:{candidate_id}",
        candidate_id=candidate_id,
        target_id=candidate_or_intent.target_id,
        expected_effect_surfaces=["planning_only"] + (["delegation_future_track"] if high_risk else []),
        expected_boundary_surfaces=["delegation_boundary", "data_boundary"],
        expected_risk_signals=["future_gate_required"] if high_risk else [],
        side_effect_free_expected=not high_risk,
        private_data_possible=high_risk,
        credential_exposure_possible=False,
        network_effect_possible=False,
        command_effect_possible=False,
        provider_effect_possible=False,
        browser_effect_possible=False,
        rpa_effect_possible=False,
        gateway_effect_possible=False,
        delegation_effect_possible=high_risk,
        metadata={"descriptive_only": True, "v0305_contract_only": True},
    )


def preview_delegation_risks(
    candidate_or_intent: ExternalDelegationCandidate | ExternalDelegationIntent,
) -> ExternalDelegationRiskPreview:
    candidate_id = (
        candidate_or_intent.candidate_id
        if isinstance(candidate_or_intent, ExternalDelegationCandidate)
        else f"external_delegation_candidate:{candidate_or_intent.intent_id}"
    )
    metadata = candidate_or_intent.metadata
    risk_signals = list(metadata.get("risk_signals", []))
    blocked_reasons = list(metadata.get("blocked_reasons", []))
    if metadata.get("future_gate_required"):
        risk_signals.append("delegation_future_track")
    if metadata.get("approval_required") or metadata.get("human_review_required"):
        risk_signals.append("human_approval_required")
    high_risk = bool(risk_signals or blocked_reasons)
    return ExternalDelegationRiskPreview(
        risk_preview_id=f"external_delegation_risk_preview:{candidate_id}",
        candidate_id=candidate_id,
        target_id=candidate_or_intent.target_id,
        risk_signals=_unique(risk_signals),
        blocked_reasons=_unique(blocked_reasons),
        required_reviews=["v0.30.6_approval_audit_boundary"] if high_risk else [],
        future_gate_required=bool(metadata.get("future_gate_required")),
        human_approval_required=bool(metadata.get("approval_required") or metadata.get("human_review_required")),
        no_op_recommended=bool(blocked_reasons),
        rationale="Risk preview preserves authority review without granting delegation.",
        evidence_refs=list(candidate_or_intent.evidence_refs),
        metadata={"v0305_contract_only": True},
    )


def make_external_delegation_candidate(
    intent: ExternalDelegationIntent,
    authority_decision_or_scope: DominionAuthorityDecision | DominionAuthorityScope,
    evidence_refs: list[str] | None = None,
) -> ExternalDelegationCandidate:
    candidate_id = f"external_delegation_candidate:{intent.intent_id}"
    if isinstance(authority_decision_or_scope, DominionAuthorityDecision):
        decision = authority_decision_or_scope
        max_allowed = min(
            normalize_dominion_level(decision.granted_level) if decision.granted_level is not None else DominionLevel.D1_DESCRIBE,
            V0305_MAX_ALLOWED_LEVEL,
        )
        decision_type = DominionAuthorityDecisionType(decision.decision)
        status = (
            ExternalDelegationCandidateStatus.BLOCKED
            if decision_type is DominionAuthorityDecisionType.BLOCKED
            else ExternalDelegationCandidateStatus.FUTURE_TRACK
            if decision.future_gate_required or normalize_dominion_level(decision.requested_level) == DominionLevel.D8_DELEGATE_AGENT
            else ExternalDelegationCandidateStatus.NO_OP
            if decision_type in {DominionAuthorityDecisionType.DENY, DominionAuthorityDecisionType.NO_OP}
            else ExternalDelegationCandidateStatus.CANDIDATE
        )
        merged_metadata = {
            **intent.metadata,
            "approval_required": decision.approval_required,
            "human_review_required": decision.human_review_required,
            "future_gate_required": decision.future_gate_required,
            "blocked_reasons": list(decision.blocked_reasons),
            "decision_id": decision.decision_id,
            "decision": str(decision.decision),
        }
    else:
        max_allowed = min(normalize_dominion_level(authority_decision_or_scope.max_level), V0305_MAX_ALLOWED_LEVEL)
        status = ExternalDelegationCandidateStatus.CANDIDATE
        merged_metadata = dict(intent.metadata)
    intent_for_nested = ExternalDelegationIntent(
        intent.intent_id,
        intent.target_id,
        intent.intent_kind,
        intent.goal_summary,
        intent.reason,
        source_decision_ids=list(intent.source_decision_ids),
        source_candidate_ids=list(intent.source_candidate_ids),
        source_report_ids=list(intent.source_report_ids),
        requested_level=intent.requested_level,
        evidence_refs=list(evidence_refs if evidence_refs is not None else intent.evidence_refs),
        metadata={**merged_metadata, "v0305_contract_only": True},
    )
    envelope = build_delegation_input_envelope(intent_for_nested)
    schema = build_expected_output_schema(intent_for_nested)
    effects = preview_delegation_effects(intent_for_nested)
    risks = preview_delegation_risks(intent_for_nested)
    return ExternalDelegationCandidate(
        candidate_id=candidate_id,
        target_id=intent.target_id,
        intent=intent_for_nested,
        input_envelope=envelope,
        expected_output_schema=schema,
        effect_preview=effects,
        risk_preview=risks,
        status=status,
        requested_level=intent.requested_level,
        max_allowed_level=max_allowed,
        evidence_refs=list(evidence_refs if evidence_refs is not None else intent.evidence_refs),
        withdrawal_conditions=[
            "delegation candidate is treated as delegation authority, packet transfer, or external runtime contact",
            "D8_DELEGATE_AGENT is granted or ready_for_execution becomes true",
        ],
        metadata={"v0305_contract_only": True},
    )


def build_external_delegation_dry_run_plan(candidate: ExternalDelegationCandidate) -> ExternalDelegationDryRunPlan:
    steps = [
        ExternalDelegationDryRunStep(
            step_id=f"external_delegation_dry_run_step:{candidate.candidate_id}:0",
            candidate_id=candidate.candidate_id,
            order=0,
            description="Inspect candidate envelope and schema as local planning artifacts.",
            simulated_action="simulate local envelope validation",
            expected_artifact="validated envelope summary",
        ),
        ExternalDelegationDryRunStep(
            step_id=f"external_delegation_dry_run_step:{candidate.candidate_id}:1",
            candidate_id=candidate.candidate_id,
            order=1,
            description="Compare risk preview with v0.30.6 approval boundary needs.",
            simulated_action="simulate risk review handoff",
            expected_artifact="approval boundary checklist",
        ),
    ]
    return ExternalDelegationDryRunPlan(
        plan_id=f"external_delegation_dry_run_plan:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        target_id=candidate.target_id,
        steps=steps,
        expected_artifacts=["validated envelope summary", "approval boundary checklist"],
        explicitly_not_performed=[
            "external contact",
            "packet transfer",
            "credential use",
            "network use",
            "command use",
            "provider use",
            "browser, RPA, or gateway use",
        ],
        no_execution_guarantee=True,
        no_external_contact_guarantee=True,
        no_credential_use_guarantee=True,
        no_network_use_guarantee=True,
        no_command_use_guarantee=True,
        evidence_refs=list(candidate.evidence_refs),
        metadata={"v0305_contract_only": True},
    )


def build_external_delegation_dry_run_report(plan: ExternalDelegationDryRunPlan) -> ExternalDelegationDryRunReport:
    findings = [
        "Dry-run plan remains local planning only.",
        "No external result envelope exists in v0.30.5.",
    ]
    return ExternalDelegationDryRunReport(
        report_id=f"external_delegation_dry_run_report:{plan.plan_id}",
        plan_id=plan.plan_id,
        candidate_id=plan.candidate_id,
        target_id=plan.target_id,
        simulated_steps_completed=[step.step_id for step in plan.steps],
        simulated_findings=findings,
        blocked_reasons=[],
        no_op_recommended=False,
        future_gate_required=False,
        ready_for_v0306_approval_boundary=True,
        evidence_refs=list(plan.evidence_refs),
        metadata={"v0305_contract_only": True, "derived_from_plan_id": plan.plan_id},
    )


def build_external_delegation_no_op_plan(
    candidate: ExternalDelegationCandidate,
    reason: str,
    blocked_reasons: list[str] | None = None,
) -> ExternalDelegationNoOpPlan:
    return ExternalDelegationNoOpPlan(
        no_op_id=f"external_delegation_no_op_plan:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        target_id=candidate.target_id,
        reason=reason,
        blocked_reasons=list(blocked_reasons or candidate.risk_preview.blocked_reasons),
        alternative_safe_actions=[
            "keep capability under observation",
            "route to v0.30.6 approval/audit boundary",
            "leave future-track without runtime action",
        ],
        evidence_refs=list(candidate.evidence_refs),
        metadata={"v0305_contract_only": True},
    )


def build_external_delegation_handoff_preview(
    candidate: ExternalDelegationCandidate,
    dry_run_plan: ExternalDelegationDryRunPlan | None = None,
    dry_run_report: ExternalDelegationDryRunReport | None = None,
    no_op_plan: ExternalDelegationNoOpPlan | None = None,
) -> ExternalDelegationHandoffPreview:
    status = normalize_delegation_candidate_status(candidate.status)
    if status is ExternalDelegationCandidateStatus.FUTURE_TRACK:
        next_stage = "future_track"
    elif no_op_plan is not None or status is ExternalDelegationCandidateStatus.NO_OP:
        next_stage = "no_op"
    else:
        next_stage = "v0.30.6 approval/audit/rollback boundary"
    return ExternalDelegationHandoffPreview(
        handoff_id=f"external_delegation_handoff_preview:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        target_id=candidate.target_id,
        dry_run_plan_id=dry_run_plan.plan_id if dry_run_plan is not None else None,
        dry_run_report_id=dry_run_report.report_id if dry_run_report is not None else None,
        no_op_plan_id=no_op_plan.no_op_id if no_op_plan is not None else None,
        next_stage=next_stage,
        ready_for_v0306_approval_audit_boundary=next_stage.startswith("v0.30.6"),
        ready_for_execution=False,
        evidence_refs=list(candidate.evidence_refs),
        withdrawal_conditions=[
            "handoff preview is treated as handoff execution",
            "ready_for_execution becomes true in v0.30.5",
        ],
        metadata={"v0305_contract_only": True},
    )


def delegation_candidate_preserves_v0305_boundary(candidate: ExternalDelegationCandidate) -> bool:
    max_allowed = normalize_dominion_level(candidate.max_allowed_level)
    return (
        max_allowed <= V0305_MAX_ALLOWED_LEVEL
        and candidate.grants_delegation_authority is False
        and candidate.creates_runtime is False
        and candidate.executes is False
    )


def dry_run_plan_preserves_no_execution(plan: ExternalDelegationDryRunPlan) -> bool:
    return (
        plan.executes is False
        and plan.no_execution_guarantee is True
        and plan.no_external_contact_guarantee is True
        and plan.no_credential_use_guarantee is True
        and plan.no_network_use_guarantee is True
        and plan.no_command_use_guarantee is True
        and all(
            not any(
                (
                    step.uses_external_runtime,
                    step.uses_network,
                    step.uses_credentials,
                    step.uses_command,
                    step.uses_browser,
                    step.uses_rpa,
                    step.uses_gateway,
                )
            )
            for step in plan.steps
        )
    )
