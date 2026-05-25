from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any

from chanta_core.agent_surface.contract import AgentSurfaceContractReportService
from chanta_core.agent_surface.intent_task import (
    AgentIntentClassificationReport,
    AgentIntentClassificationReportService,
    AgentTaskFrame,
    AgentTaskFrameCandidate,
    AgentTaskInputRequirement,
    AgentTaskRiskPreview,
)
from chanta_core.agent_surface.turn_context import AgentTurnReport, AgentTurnReportService
from chanta_core.utility.time import utc_now_iso


AGENT_SAFETY_GATE_VERSION = "v0.25.3"
AGENT_SAFETY_GATE_VERSION_NAME = "Safety / No-Action / Clarification Gate"
AGENT_SAFETY_GATE_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_SAFETY_GATE_ROUTE_NEXT_STEP = "v0.25.4 Tool Routing Plan & Provider Selection"
AGENT_SAFETY_GATE_RESPONSE_NEXT_STEP = "v0.25.6 Response Assembly & Evidence Binder"

AGENT_SAFETY_GATE_OBJECT_TYPES = [
    "agent_safety_gate_policy",
    "agent_safety_gate_request",
    "agent_safety_rule",
    "agent_safety_rule_result",
    "agent_safety_gate_decision",
    "agent_no_action_policy",
    "agent_no_action_decision",
    "agent_clarification_policy",
    "agent_clarification_question",
    "agent_clarification_decision",
    "agent_needs_more_input_decision",
    "agent_blocked_decision",
    "agent_deferred_decision",
    "agent_gate_outcome_envelope",
    "agent_safety_gate_finding",
    "agent_safety_gate_report",
    "agent_intent_classification_report",
    "agent_task_frame",
    "agent_task_frame_candidate",
    "agent_turn_envelope",
    "agent_surface_contract",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_SAFETY_GATE_EVENT_TYPES = [
    "agent_safety_gate_requested",
    "agent_safety_gate_policy_created",
    "agent_safety_rules_loaded",
    "agent_safety_rules_evaluated",
    "agent_safety_gate_evaluated",
    "agent_no_action_decision_created",
    "agent_clarification_question_created",
    "agent_clarification_decision_created",
    "agent_needs_more_input_decision_created",
    "agent_blocked_decision_created",
    "agent_deferred_decision_created",
    "agent_allow_route_decision_created",
    "agent_gate_outcome_envelope_created",
    "agent_safety_gate_report_created",
    "agent_safety_gate_warning_created",
    "agent_safety_gate_blocked",
]

AGENT_SAFETY_GATE_RELATION_TYPES = [
    "uses_agent_intent_classification_report",
    "uses_agent_task_frame_candidate",
    "uses_agent_turn_envelope",
    "uses_agent_surface_contract",
    "evaluates_agent_safety_rule",
    "creates_agent_safety_gate_decision",
    "creates_agent_no_action_decision",
    "creates_agent_clarification_question",
    "creates_agent_clarification_decision",
    "creates_agent_needs_more_input_decision",
    "creates_agent_blocked_decision",
    "creates_agent_deferred_decision",
    "creates_agent_gate_outcome_envelope",
    "prepares_tool_routing",
    "defers_tool_routing_to_v0_25_4",
    "defers_provider_invocation_to_v0_25_5",
    "defers_response_assembly_to_v0_25_6",
    "defers_ask_repl_to_v0_25_7",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_tool_route_executed",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "blocks_raw_secret_output",
    "derived_from_agent_task_frame",
    "recorded_in_envelope",
]

AGENT_SAFETY_GATE_EFFECT_TYPES = [
    "read_only_observation",
    "agent_safety_gate_evaluated",
    "agent_no_action_finalized",
    "agent_clarification_finalized",
    "agent_needs_more_input_finalized",
    "agent_blocked_decision_finalized",
    "agent_deferred_decision_finalized",
    "agent_allow_route_finalized",
    "state_candidate_created",
]

AGENT_SAFETY_GATE_FORBIDDEN_EFFECT_TYPES = [
    "agent_tool_route_plan_created",
    "tool_route_executed",
    "agent_provider_invocation_requested",
    "provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "agent_ask_executed",
    "agent_repl_started",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "credential_exposed",
    "raw_secret_output",
    "schumpeter_split_introduced",
]

SAFETY_OUTCOMES = [
    "allow_route",
    "needs_more_input",
    "clarification_requested",
    "no_action",
    "blocked",
    "deferred",
    "failed",
]

REQUIRED_SAFETY_RULE_IDS = [
    "task_frame_must_exist",
    "sanitized_request_must_exist",
    "user_request_not_permission",
    "no_action_allowed_for_explanation_only",
    "no_action_allowed_for_low_value_or_redundant_action",
    "clarification_required_for_ambiguous_target",
    "clarification_required_for_missing_path_or_scope",
    "needs_more_input_for_missing_required_input",
    "blocked_for_credential_exposure_request",
    "blocked_for_raw_secret_output_request",
    "blocked_for_provider_boundary_bypass",
    "blocked_for_external_adapter_request_in_v0_25",
    "deferred_for_memory_continuity_request",
    "deferred_for_workspace_workbench_request",
    "deferred_for_schumpeter_split_request",
    "local_runtime_execution_requires_v0_24_gate",
    "allow_route_only_to_v0_25_4",
    "no_provider_invocation_in_v0_25_3",
    "no_tool_route_plan_in_v0_25_3",
    "no_local_command_execution_in_v0_25_3",
    "no_memory_promotion_in_v0_25_3",
    "no_llm_safety_judge",
]


def _utc_now() -> str:
    return utc_now_iso()


def _safe_id(text: str | None) -> str:
    value = text or "unknown"
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "-", value.strip().lower())[:120] or "unknown"


def _contains_any(text: str, needles: list[str]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


@dataclass
class AgentSafetyGatePolicy:
    policy_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    layer: str = "agent_surface"
    deterministic_default: bool = True
    external_llm_safety_enabled: bool = False
    llm_safety_judge_enabled: bool = False
    evaluate_from_task_frame_only: bool = True
    tool_routing_enabled: bool = False
    provider_invocation_enabled: bool = False
    provider_selection_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    ask_execution_enabled: bool = False
    repl_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    allow_route_decision_enabled: bool = True
    no_action_decision_enabled: bool = True
    clarification_decision_enabled: bool = True
    needs_more_input_decision_enabled: bool = True
    blocked_decision_enabled: bool = True
    deferred_decision_enabled: bool = True
    raw_secret_storage_forbidden: bool = True
    credential_exposure_forbidden: bool = True
    private_path_sanitization_required: bool = True
    evidence_refs_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyGateRequest:
    request_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    intent_report_id: str | None = None
    task_frame_id: str | None = None
    task_frame_candidate_id: str | None = None
    turn_envelope_id: str | None = None
    sanitized_request_text: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyRule:
    rule_id: str
    rule_name: str
    rule_category: str
    description: str
    severity_if_failed: str
    outcome_hint: str
    enabled: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyRuleResult:
    result_id: str
    rule_id: str
    rule_category: str
    passed: bool
    outcome_hint: str
    severity: str
    message: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyGateDecision:
    decision_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    primary_outcome: str = "failed"
    secondary_outcomes: list[str] = field(default_factory=list)
    decision_reason: str = ""
    decision_confidence: str = "medium"
    decision_method: str = "deterministic_rules"
    matched_rule_results: list[AgentSafetyRuleResult] = field(default_factory=list)
    expected_next_stage: str | None = None
    final_no_action_decision: bool = False
    final_clarification_decision: bool = False
    final_needs_more_input_decision: bool = False
    final_blocked_decision: bool = False
    final_deferred_decision: bool = False
    allow_route: bool = False
    tool_route_created: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentNoActionPolicy:
    policy_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    no_action_valid: bool = True
    no_action_requires_rationale: bool = True
    no_action_allowed_when_explanation_sufficient: bool = True
    no_action_allowed_when_provider_unnecessary: bool = True
    no_action_allowed_when_risk_exceeds_value: bool = True
    no_action_allowed_when_duplicate_or_redundant: bool = True
    no_action_must_be_recorded: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentNoActionDecision:
    decision_id: str
    reason: str
    rationale: str
    safe_alternative: str | None = None
    provider_invocation_avoided: bool = True
    local_command_execution_avoided: bool = True
    final_no_action_decision: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentClarificationPolicy:
    policy_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    clarification_valid: bool = True
    clarification_requires_specific_missing_inputs: bool = True
    max_questions: int = 3
    prefer_minimal_questions: bool = True
    avoid_reasking_known_context: bool = True
    no_provider_invocation_before_clarification: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentClarificationQuestion:
    question_id: str
    question_text: str
    missing_input_type: str
    required_for_next_stage: bool
    options: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentClarificationDecision:
    decision_id: str
    questions: list[AgentClarificationQuestion]
    rationale: str
    final_clarification_decision: bool = True
    provider_invocation_avoided: bool = True
    local_command_execution_avoided: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentNeedsMoreInputDecision:
    decision_id: str
    missing_inputs: list[dict[str, Any]]
    rationale: str
    final_needs_more_input_decision: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentBlockedDecision:
    decision_id: str
    blocked_reason: str
    policy_refs: list[dict[str, Any]]
    safe_alternative: str | None = None
    final_blocked_decision: bool = True
    provider_invocation_avoided: bool = True
    local_command_execution_avoided: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentDeferredDecision:
    decision_id: str
    deferred_to_track: str
    deferred_reason: str
    current_track_boundary: str
    final_deferred_decision: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentGateOutcomeEnvelope:
    outcome_envelope_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    gate_decision: AgentSafetyGateDecision | None = None
    no_action_decision: AgentNoActionDecision | None = None
    clarification_decision: AgentClarificationDecision | None = None
    needs_more_input_decision: AgentNeedsMoreInputDecision | None = None
    blocked_decision: AgentBlockedDecision | None = None
    deferred_decision: AgentDeferredDecision | None = None
    expected_next_stage: str | None = None
    response_assembly_required: bool = False
    route_plan_allowed_next: bool = False
    provider_invocation_allowed_now: bool = False
    local_command_execution_allowed_now: bool = False
    tool_route_created: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyGateFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSafetyGateReport:
    report_id: str
    version: str = AGENT_SAFETY_GATE_VERSION
    created_at: str = ""
    policy: AgentSafetyGatePolicy | None = None
    request: AgentSafetyGateRequest | None = None
    rule_results: list[AgentSafetyRuleResult] = field(default_factory=list)
    gate_decision: AgentSafetyGateDecision | None = None
    outcome_envelope: AgentGateOutcomeEnvelope | None = None
    findings: list[AgentSafetyGateFinding] = field(default_factory=list)
    report_status: str = "failed"
    ready_for_v0_25_4: bool = False
    ready_for_v0_25_6: bool = False
    ready_for_v0_26: bool = False
    safety_gate_evaluated: bool = True
    allow_route: bool = False
    final_no_action_decision: bool = False
    final_clarification_decision: bool = False
    final_needs_more_input_decision: bool = False
    final_blocked_decision: bool = False
    final_deferred_decision: bool = False
    tool_route_created: bool = False
    tool_route_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_SAFETY_GATE_RESPONSE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.4 routing begins or safety/no-action/clarification policy changes."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentSafetyGatePrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        return AgentSurfaceContractReportService().build_report().to_dict()

    def load_turn_envelope(self) -> dict[str, Any]:
        return AgentTurnReportService().build_report().envelope.to_dict()

    def load_intent_classification_report(self) -> AgentIntentClassificationReport:
        return AgentIntentClassificationReportService().build_report()

    def load_task_frame_candidate(self) -> AgentTaskFrameCandidate:
        return self.load_intent_classification_report().task_frame_candidate

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return {
            "skill:agent_safety_gate_evaluate": "implemented",
            "skill:agent_no_action_create": "implemented",
            "skill:agent_clarification_create": "implemented",
            "skill:agent_tool_route_plan_create": "contract_only",
            "skill:agent_provider_selection_create": "contract_only",
            "skill:agent_provider_invocation_orchestrate": "contract_only",
            "skill:agent_ask": "contract_only",
            "skill:agent_repl": "contract_only",
        }

    def load_provider_registry_if_available(self) -> dict[str, Any]:
        return {"status": "reference_only", "provider_invocation_performed": False}


class AgentSafetyGatePolicyService:
    def build_policy(self) -> AgentSafetyGatePolicy:
        return AgentSafetyGatePolicy(
            policy_id="agent_safety_gate_policy:v0.25.3",
            evidence_refs=[
                {"type": "version", "value": AGENT_SAFETY_GATE_VERSION},
                {"type": "track", "value": AGENT_SAFETY_GATE_TRACK},
            ],
        )


class AgentSafetyRuleRegistry:
    RULE_DEFINITIONS: dict[str, tuple[str, str, str, str, str]] = {
        "task_frame_must_exist": ("request_validity", "Task frame must exist.", "error", "failed", "Task frame must exist"),
        "sanitized_request_must_exist": ("request_validity", "Sanitized request text must exist.", "error", "failed", "Sanitized request must exist"),
        "user_request_not_permission": ("provider_boundary", "A user request is not execution permission.", "warning", "none", "User request is not permission"),
        "no_action_allowed_for_explanation_only": ("no_action", "No-action is valid when explanation or stop is sufficient.", "info", "no_action", "No-action allowed for explanation-only"),
        "no_action_allowed_for_low_value_or_redundant_action": ("no_action", "No-action is valid for redundant or low-value action.", "info", "no_action", "No-action allowed for redundant action"),
        "clarification_required_for_ambiguous_target": ("clarification", "Ambiguous target requires clarification.", "warning", "clarification_requested", "Clarification required for ambiguous target"),
        "clarification_required_for_missing_path_or_scope": ("clarification", "Missing path or scope requires clarification.", "warning", "clarification_requested", "Clarification required for missing path or scope"),
        "needs_more_input_for_missing_required_input": ("needs_more_input", "Missing required input can produce needs-more-input.", "warning", "needs_more_input", "Needs more input for missing required input"),
        "blocked_for_credential_exposure_request": ("credential_safety", "Credential exposure risk must block.", "critical", "blocked", "Credential exposure blocked"),
        "blocked_for_raw_secret_output_request": ("credential_safety", "Raw secret output risk must block.", "critical", "blocked", "Raw secret output blocked"),
        "blocked_for_provider_boundary_bypass": ("provider_boundary", "Provider boundary bypass must block.", "critical", "blocked", "Provider boundary bypass blocked"),
        "blocked_for_external_adapter_request_in_v0_25": ("external_adapter_boundary", "External adapter implementation is outside v0.25.", "warning", "deferred", "External adapter deferred or blocked"),
        "deferred_for_memory_continuity_request": ("memory_boundary", "Memory continuity is deferred to v0.27.", "warning", "deferred", "Memory continuity deferred"),
        "deferred_for_workspace_workbench_request": ("track_boundary", "Workspace workbench is deferred to v0.26.", "warning", "deferred", "Workspace workbench deferred"),
        "deferred_for_schumpeter_split_request": ("track_boundary", "Schumpeter split preparation is deferred to v0.28.", "warning", "deferred", "Schumpeter split deferred"),
        "local_runtime_execution_requires_v0_24_gate": ("local_runtime_boundary", "Local runtime execution requires the v0.24 gate later.", "warning", "allow_route", "Local runtime execution requires gate"),
        "allow_route_only_to_v0_25_4": ("track_boundary", "Allow-route can only prepare v0.25.4 routing.", "info", "allow_route", "Allow-route only to v0.25.4"),
        "no_provider_invocation_in_v0_25_3": ("provider_boundary", "v0.25.3 must not invoke providers.", "critical", "blocked", "No provider invocation in v0.25.3"),
        "no_tool_route_plan_in_v0_25_3": ("track_boundary", "v0.25.3 must not create tool route plans.", "critical", "blocked", "No tool route plan in v0.25.3"),
        "no_local_command_execution_in_v0_25_3": ("local_runtime_boundary", "v0.25.3 must not execute local commands.", "critical", "blocked", "No local command execution in v0.25.3"),
        "no_memory_promotion_in_v0_25_3": ("memory_boundary", "v0.25.3 must not promote memory.", "critical", "blocked", "No memory promotion in v0.25.3"),
        "no_llm_safety_judge": ("evidence_requirement", "Safety judgment must be deterministic by default.", "critical", "blocked", "No LLM safety judge"),
    }

    def list_rules(self) -> list[AgentSafetyRule]:
        return [
            AgentSafetyRule(
                rule_id=rule_id,
                rule_name=name,
                rule_category=category,
                description=description,
                severity_if_failed=severity,
                outcome_hint=outcome_hint,
                evidence_refs=[{"type": "required_rule", "value": rule_id}],
            )
            for rule_id, (category, description, severity, outcome_hint, name) in self.RULE_DEFINITIONS.items()
        ]


class AgentSafetyRuleEngine:
    def evaluate_rules(
        self,
        request: AgentSafetyGateRequest,
        task_frame_candidate: AgentTaskFrameCandidate | None,
        risk_preview: AgentTaskRiskPreview | None,
        rules: list[AgentSafetyRule],
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentSafetyRuleResult]:
        results: list[AgentSafetyRuleResult] = []
        text = (request.sanitized_request_text or "").lower()
        risks = set(risk_preview.risk_categories if risk_preview else [])
        missing_requirements = self._missing_requirements(task_frame_candidate)
        attempt_flags = attempt_flags or {}
        for rule in rules:
            passed, active, message = self._evaluate_rule(rule.rule_id, text, risks, missing_requirements, request, task_frame_candidate, attempt_flags)
            severity = "info" if passed else rule.severity_if_failed
            outcome_hint = rule.outcome_hint if active and not passed else "none"
            results.append(
                AgentSafetyRuleResult(
                    result_id=f"agent_safety_rule_result:{rule.rule_id}",
                    rule_id=rule.rule_id,
                    rule_category=rule.rule_category,
                    passed=passed,
                    outcome_hint=outcome_hint,
                    severity=severity,
                    message=message,
                    evidence_refs=[{"type": "rule", "id": rule.rule_id}],
                )
            )
        return results

    def _missing_requirements(self, task_frame_candidate: AgentTaskFrameCandidate | None) -> list[AgentTaskInputRequirement]:
        if task_frame_candidate is None:
            return []
        return [item for item in task_frame_candidate.task_frame.input_requirements if item.missing]

    def _evaluate_rule(
        self,
        rule_id: str,
        text: str,
        risks: set[str],
        missing_requirements: list[AgentTaskInputRequirement],
        request: AgentSafetyGateRequest,
        task_frame_candidate: AgentTaskFrameCandidate | None,
        attempt_flags: dict[str, bool],
    ) -> tuple[bool, bool, str]:
        if rule_id == "task_frame_must_exist":
            passed = task_frame_candidate is not None
            return passed, True, "Task frame candidate is present." if passed else "Task frame candidate is missing."
        if rule_id == "sanitized_request_must_exist":
            passed = bool(request.sanitized_request_text)
            return passed, True, "Sanitized request is present." if passed else "Sanitized request is missing."
        if rule_id == "user_request_not_permission":
            return True, False, "User request was treated as input, not permission."
        if rule_id == "no_action_allowed_for_explanation_only":
            active = _contains_any(text, ["do nothing", "no action", "stop here", "nothing to do"])
            return not active, active, "No-action candidate detected." if active else "No no-action request detected."
        if rule_id == "no_action_allowed_for_low_value_or_redundant_action":
            active = _contains_any(text, ["redundant", "duplicate", "already done"])
            return not active, active, "Redundant action candidate detected." if active else "No redundant action detected."
        if rule_id == "clarification_required_for_ambiguous_target":
            active = _contains_any(text, ["unclear", "ambiguous", "not sure", "something"]) or (
                task_frame_candidate is not None and task_frame_candidate.task_frame.risk_preview.requires_clarification_candidate
            )
            local_runtime = "local_runtime_execution" in risks
            return (not active) or local_runtime, active and not local_runtime, "Ambiguous target requires clarification." if active and not local_runtime else "No resolvable ambiguity detected."
        if rule_id == "clarification_required_for_missing_path_or_scope":
            path_like = any(token in text for token in [".py", ".md", "/", "\\"])
            active = any(item.requirement_type == "target_path" and item.missing for item in missing_requirements) or (
                "read" in text and "file" in text and not path_like
            )
            return not active, active, "Missing target path requires clarification." if active else "No missing path or scope detected."
        if rule_id == "needs_more_input_for_missing_required_input":
            non_path_missing = [item for item in missing_requirements if item.requirement_type not in {"target_path", "execution_authorization"}]
            active = bool(non_path_missing)
            return not active, active, "Missing required input detected." if active else "No needs-more-input condition detected."
        if rule_id == "blocked_for_credential_exposure_request":
            active = "credential_exposure" in risks
            return not active, active, "Credential exposure risk must block." if active else "No credential exposure risk detected."
        if rule_id == "blocked_for_raw_secret_output_request":
            active = "raw_secret_output" in risks
            return not active, active, "Raw secret output risk must block." if active else "No raw secret output risk detected."
        if rule_id == "blocked_for_provider_boundary_bypass":
            active = "provider_boundary_bypass" in risks
            return not active, active, "Provider boundary bypass must block." if active else "No provider boundary bypass detected."
        if rule_id == "blocked_for_external_adapter_request_in_v0_25":
            active = "external_adapter" in risks or "external agent dominion" in text
            return not active, active, "External adapter request is deferred outside v0.25." if active else "No external adapter request detected."
        if rule_id == "deferred_for_memory_continuity_request":
            active = "memory_mutation" in risks
            return not active, active, "Memory continuity request is deferred to v0.27." if active else "No memory continuity request detected."
        if rule_id == "deferred_for_workspace_workbench_request":
            active = "workspace workbench" in text
            return not active, active, "Workspace workbench request is deferred to v0.26." if active else "No workspace workbench request detected."
        if rule_id == "deferred_for_schumpeter_split_request":
            active = "schumpeter" in text
            return not active, active, "Schumpeter split request is deferred to v0.28." if active else "No Schumpeter split request detected."
        if rule_id == "local_runtime_execution_requires_v0_24_gate":
            active = "local_runtime_execution" in risks
            return not active, active, "Local runtime request may route next but still requires v0.24 gate later." if active else "No local runtime request detected."
        attempted_rules = {
            "no_provider_invocation_in_v0_25_3": "provider_invocation_attempted",
            "no_tool_route_plan_in_v0_25_3": "tool_routing_attempted",
            "no_local_command_execution_in_v0_25_3": "local_command_execution_attempted",
            "no_memory_promotion_in_v0_25_3": "memory_promotion_attempted",
            "no_llm_safety_judge": "llm_judge_detected",
        }
        if rule_id in attempted_rules:
            active = bool(attempt_flags.get(attempted_rules[rule_id], False))
            return not active, active, f"{rule_id} violation detected." if active else f"{rule_id} boundary preserved."
        return True, False, "Rule passed."


class AgentSafetyGateDecisionService:
    def build_decision(
        self,
        rule_results: list[AgentSafetyRuleResult],
        task_frame_candidate: AgentTaskFrameCandidate | None,
        request: AgentSafetyGateRequest,
    ) -> AgentSafetyGateDecision:
        failed_active = [item for item in rule_results if not item.passed and item.outcome_hint != "none"]
        outcome = self._select_primary_outcome(failed_active, task_frame_candidate, request)
        expected_next = AGENT_SAFETY_GATE_ROUTE_NEXT_STEP if outcome == "allow_route" else AGENT_SAFETY_GATE_RESPONSE_NEXT_STEP
        confidence = "high" if outcome in {"allow_route", "blocked", "deferred"} else "medium"
        if outcome == "failed":
            confidence = "low"
        return AgentSafetyGateDecision(
            decision_id=f"agent_safety_gate_decision:{_safe_id(request.request_id)}",
            primary_outcome=outcome,
            secondary_outcomes=sorted({item.outcome_hint for item in failed_active if item.outcome_hint != outcome}),
            decision_reason=self._reason_for(outcome, failed_active),
            decision_confidence=confidence,
            matched_rule_results=rule_results,
            expected_next_stage=expected_next,
            final_no_action_decision=outcome == "no_action",
            final_clarification_decision=outcome == "clarification_requested",
            final_needs_more_input_decision=outcome == "needs_more_input",
            final_blocked_decision=outcome == "blocked",
            final_deferred_decision=outcome == "deferred",
            allow_route=outcome == "allow_route",
            evidence_refs=[{"type": "decision_method", "value": "deterministic_rules"}],
        )

    def _select_primary_outcome(
        self,
        failed_active: list[AgentSafetyRuleResult],
        task_frame_candidate: AgentTaskFrameCandidate | None,
        request: AgentSafetyGateRequest,
    ) -> str:
        hints = {item.outcome_hint for item in failed_active}
        text = (request.sanitized_request_text or "").lower()
        if "failed" in hints:
            return "failed"
        if "blocked" in hints:
            return "blocked"
        if "deferred" in hints:
            return "deferred"
        if "clarification_requested" in hints:
            return "clarification_requested"
        if "needs_more_input" in hints:
            return "needs_more_input"
        if "no_action" in hints:
            return "no_action"
        if task_frame_candidate is None:
            return "failed"
        if "local_runtime_execution" in task_frame_candidate.task_frame.risk_preview.risk_categories:
            return "allow_route"
        if task_frame_candidate.candidate_status == "no_action_candidate" or _contains_any(text, ["do nothing", "no action"]):
            return "no_action"
        if task_frame_candidate.candidate_status == "blocked_candidate":
            return "blocked"
        if task_frame_candidate.candidate_status == "needs_more_input_candidate":
            return "clarification_requested"
        return "allow_route"

    def _reason_for(self, outcome: str, failed_active: list[AgentSafetyRuleResult]) -> str:
        if failed_active:
            return "; ".join(item.message for item in failed_active[:3])
        if outcome == "allow_route":
            return "Safety gate allows only a future v0.25.4 route plan; no route plan or provider invocation is created now."
        return f"{outcome} selected by deterministic safety gate."


class AgentNoActionPolicyService:
    def build_policy(self) -> AgentNoActionPolicy:
        return AgentNoActionPolicy(policy_id="agent_no_action_policy:v0.25.3")


class AgentNoActionDecisionService:
    def build_decision(self, gate_decision: AgentSafetyGateDecision) -> AgentNoActionDecision | None:
        if gate_decision.primary_outcome != "no_action":
            return None
        return AgentNoActionDecision(
            decision_id=f"agent_no_action_decision:{_safe_id(gate_decision.decision_id)}",
            reason=gate_decision.decision_reason,
            rationale="No-action is a final agent decision in v0.25.3 when action is unnecessary or explicitly avoided.",
            safe_alternative="Return a concise response explaining that no action was taken.",
            evidence_refs=[{"type": "gate_decision", "id": gate_decision.decision_id}],
        )


class AgentClarificationPolicyService:
    def build_policy(self) -> AgentClarificationPolicy:
        return AgentClarificationPolicy(policy_id="agent_clarification_policy:v0.25.3")


class AgentClarificationDecisionService:
    def build_decision(
        self,
        gate_decision: AgentSafetyGateDecision,
        input_requirements: list[AgentTaskInputRequirement],
        policy: AgentClarificationPolicy | None = None,
    ) -> AgentClarificationDecision | None:
        if gate_decision.primary_outcome != "clarification_requested":
            return None
        policy = policy or AgentClarificationPolicyService().build_policy()
        questions: list[AgentClarificationQuestion] = []
        missing_items = [item for item in input_requirements if item.missing]
        result_text = " ".join(result.message for result in gate_decision.matched_rule_results if not result.passed).lower()
        if "missing target path" in result_text and not any(item.requirement_type == "target_path" for item in missing_items):
            missing_items.insert(
                0,
                AgentTaskInputRequirement(
                    input_requirement_id="agent_task_input_requirement:target_path",
                    requirement_type="target_path",
                    description="Target file path is required for a future file read.",
                    required_for_next_stage=True,
                    missing=True,
                    evidence_refs=[{"type": "safety_rule", "id": "clarification_required_for_missing_path_or_scope"}],
                ),
            )
        if not missing_items:
            if "missing target path" in result_text:
                missing_items = [
                    AgentTaskInputRequirement(
                        input_requirement_id="agent_task_input_requirement:target_path",
                        requirement_type="target_path",
                        description="Target file path is required for a future file read.",
                        required_for_next_stage=True,
                        missing=True,
                        evidence_refs=[{"type": "safety_rule", "id": "clarification_required_for_missing_path_or_scope"}],
                    )
                ]
        if not missing_items:
            missing_items = [
                AgentTaskInputRequirement(
                    input_requirement_id="agent_task_input_requirement:clarification",
                    requirement_type="clarification",
                    description="Clarify the target, scope, or desired outcome.",
                    required_for_next_stage=True,
                    missing=True,
                    evidence_refs=[{"type": "safety_rule", "id": "clarification_required_for_ambiguous_target"}],
                )
            ]
        for item in missing_items[: policy.max_questions]:
            questions.append(
                AgentClarificationQuestion(
                    question_id=f"agent_clarification_question:{_safe_id(item.requirement_type)}",
                    question_text=self._question_text(item),
                    missing_input_type=item.requirement_type,
                    required_for_next_stage=True,
                    options=[],
                    evidence_refs=[{"type": "input_requirement", "id": item.input_requirement_id}],
                )
            )
        return AgentClarificationDecision(
            decision_id=f"agent_clarification_decision:{_safe_id(gate_decision.decision_id)}",
            questions=questions,
            rationale="Clarification is requested before any provider invocation, routing execution, or local command execution.",
            evidence_refs=[{"type": "gate_decision", "id": gate_decision.decision_id}],
        )

    def _question_text(self, requirement: AgentTaskInputRequirement) -> str:
        if requirement.requirement_type == "target_path":
            return "Which target path or file should the next stage consider?"
        if requirement.requirement_type == "execution_authorization":
            return "What explicit execution authorization should future local-runtime gates require?"
        return "What missing detail should be supplied before the next stage?"


class AgentNeedsMoreInputDecisionService:
    def build_decision(
        self,
        gate_decision: AgentSafetyGateDecision,
        input_requirements: list[AgentTaskInputRequirement],
    ) -> AgentNeedsMoreInputDecision | None:
        if gate_decision.primary_outcome != "needs_more_input":
            return None
        missing_inputs = [item.to_dict() for item in input_requirements if item.missing]
        return AgentNeedsMoreInputDecision(
            decision_id=f"agent_needs_more_input_decision:{_safe_id(gate_decision.decision_id)}",
            missing_inputs=missing_inputs,
            rationale="Required input is missing; v0.25.3 records the final needs-more-input decision without executing anything.",
            evidence_refs=[{"type": "gate_decision", "id": gate_decision.decision_id}],
        )


class AgentBlockedDecisionService:
    def build_decision(self, gate_decision: AgentSafetyGateDecision) -> AgentBlockedDecision | None:
        if gate_decision.primary_outcome != "blocked":
            return None
        policy_refs = [
            {"rule_id": item.rule_id, "category": item.rule_category}
            for item in gate_decision.matched_rule_results
            if not item.passed and item.outcome_hint == "blocked"
        ]
        return AgentBlockedDecision(
            decision_id=f"agent_blocked_decision:{_safe_id(gate_decision.decision_id)}",
            blocked_reason=gate_decision.decision_reason,
            policy_refs=policy_refs,
            safe_alternative="Provide a sanitized explanation and do not expose credentials, raw secrets, or bypass boundaries.",
            evidence_refs=[{"type": "gate_decision", "id": gate_decision.decision_id}],
        )


class AgentDeferredDecisionService:
    def build_decision(self, gate_decision: AgentSafetyGateDecision, request: AgentSafetyGateRequest) -> AgentDeferredDecision | None:
        if gate_decision.primary_outcome != "deferred":
            return None
        text = (request.sanitized_request_text or "").lower()
        if "workspace workbench" in text:
            target = "v0.26.x Workspace Agent Workbench"
        elif "memory" in text:
            target = "v0.27.x Memory Candidate & Continuity"
        elif "schumpeter" in text:
            target = "v0.28.x Public Alpha / Schumpeter Split Preparation"
        elif "external agent dominion" in text:
            target = "v0.30.x+ External Agent Dominion Bridge"
        else:
            target = "v0.29.x+ External Skill / External Provider Adapter Development"
        return AgentDeferredDecision(
            decision_id=f"agent_deferred_decision:{_safe_id(gate_decision.decision_id)}",
            deferred_to_track=target,
            deferred_reason=gate_decision.decision_reason,
            current_track_boundary="v0.25.x Bounded General Agent Surface & Internal Tool Routing",
            evidence_refs=[{"type": "gate_decision", "id": gate_decision.decision_id}],
        )


class AgentGateOutcomeEnvelopeService:
    def build_outcome_envelope(
        self,
        gate_decision: AgentSafetyGateDecision,
        no_action_decision: AgentNoActionDecision | None,
        clarification_decision: AgentClarificationDecision | None,
        needs_more_input_decision: AgentNeedsMoreInputDecision | None,
        blocked_decision: AgentBlockedDecision | None,
        deferred_decision: AgentDeferredDecision | None,
    ) -> AgentGateOutcomeEnvelope:
        route_allowed = gate_decision.primary_outcome == "allow_route"
        return AgentGateOutcomeEnvelope(
            outcome_envelope_id=f"agent_gate_outcome_envelope:{_safe_id(gate_decision.decision_id)}",
            gate_decision=gate_decision,
            no_action_decision=no_action_decision,
            clarification_decision=clarification_decision,
            needs_more_input_decision=needs_more_input_decision,
            blocked_decision=blocked_decision,
            deferred_decision=deferred_decision,
            expected_next_stage=gate_decision.expected_next_stage,
            response_assembly_required=not route_allowed,
            route_plan_allowed_next=route_allowed,
            evidence_refs=[{"type": "provider_invocation_allowed_now", "value": False}],
        )


class AgentSafetyGateFindingService:
    WARNING_TYPES = {
        "no_action_selected",
        "clarification_selected",
        "needs_more_input_selected",
        "deferred_selected",
        "ambiguous_request_requires_clarification",
        "missing_required_input",
        "external_adapter_request_deferred_or_blocked",
        "memory_continuity_deferred",
        "workspace_workbench_deferred",
        "schumpeter_split_deferred",
        "local_runtime_execution_requires_gate",
        "safety_gate_required_before_routing",
        "tool_routing_deferred",
        "provider_invocation_deferred",
    }
    BLOCKED_ATTEMPTS = {
        "ask_execution_attempted_too_early",
        "repl_execution_attempted_too_early",
        "tool_routing_attempted_too_early",
        "provider_invocation_attempted_too_early",
        "local_command_execution_attempted",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_adapter_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "schumpeter_split_detected",
        "growthkernel_dependency_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        request: AgentSafetyGateRequest,
        task_frame_candidate: AgentTaskFrameCandidate | None,
        gate_decision: AgentSafetyGateDecision,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentSafetyGateFinding]:
        subject_id = gate_decision.decision_id
        findings = [self._finding("info", "ok", "Safety gate evaluated deterministically without execution.", subject_id)]
        if not request.intent_report_id:
            findings.append(self._finding("error", "missing_intent_report", "Intent report reference is missing.", request.request_id))
        if not request.task_frame_id:
            findings.append(self._finding("error", "missing_task_frame", "Task frame reference is missing.", request.request_id))
        if not request.task_frame_candidate_id:
            findings.append(self._finding("error", "missing_task_frame_candidate", "Task frame candidate reference is missing.", request.request_id))
        if not request.sanitized_request_text:
            findings.append(self._finding("error", "missing_sanitized_request", "Sanitized request text is missing.", request.request_id))
        if gate_decision.primary_outcome == "allow_route":
            findings.append(self._finding("info", "allow_route_selected", "Allow-route selected for v0.25.4 only.", subject_id))
        if gate_decision.primary_outcome == "no_action":
            findings.append(self._finding("warning", "no_action_selected", "No-action selected as a valid v0.25.3 outcome.", subject_id))
        if gate_decision.primary_outcome == "clarification_requested":
            findings.append(self._finding("warning", "clarification_selected", "Clarification selected before routing or provider invocation.", subject_id))
            findings.append(self._finding("warning", "ambiguous_request_requires_clarification", "Ambiguous request requires clarification.", subject_id))
        if gate_decision.primary_outcome == "needs_more_input":
            findings.append(self._finding("warning", "needs_more_input_selected", "Needs-more-input selected before routing.", subject_id))
            findings.append(self._finding("warning", "missing_required_input", "Required input is missing.", subject_id))
        if gate_decision.primary_outcome == "blocked":
            findings.append(self._finding("critical", "blocked_selected", "Blocked selected by safety policy.", subject_id))
        if gate_decision.primary_outcome == "deferred":
            findings.append(self._finding("warning", "deferred_selected", "Deferred selected for future-track work.", subject_id))
        rule_ids = {item.rule_id for item in gate_decision.matched_rule_results if not item.passed}
        rule_to_finding = {
            "blocked_for_credential_exposure_request": ("critical", "credential_exposure_risk_blocked", "Credential exposure risk blocked."),
            "blocked_for_raw_secret_output_request": ("critical", "raw_secret_output_risk_blocked", "Raw secret output risk blocked."),
            "blocked_for_provider_boundary_bypass": ("critical", "provider_boundary_bypass_blocked", "Provider boundary bypass blocked."),
            "blocked_for_external_adapter_request_in_v0_25": ("warning", "external_adapter_request_deferred_or_blocked", "External adapter request deferred or blocked."),
            "deferred_for_memory_continuity_request": ("warning", "memory_continuity_deferred", "Memory continuity deferred to v0.27."),
            "deferred_for_workspace_workbench_request": ("warning", "workspace_workbench_deferred", "Workspace workbench deferred to v0.26."),
            "deferred_for_schumpeter_split_request": ("warning", "schumpeter_split_deferred", "Schumpeter split deferred to v0.28."),
            "local_runtime_execution_requires_v0_24_gate": ("warning", "local_runtime_execution_requires_gate", "Local runtime execution requires the v0.24 gate later."),
        }
        for rule_id, payload in rule_to_finding.items():
            if rule_id in rule_ids:
                findings.append(self._finding(payload[0], payload[1], payload[2], subject_id))
        findings.append(self._finding("warning", "safety_gate_required_before_routing", "Safety gate is required before v0.25.4 routing.", subject_id))
        findings.append(self._finding("warning", "tool_routing_deferred", "Tool routing is deferred to v0.25.4.", subject_id))
        findings.append(self._finding("warning", "provider_invocation_deferred", "Provider invocation is deferred to v0.25.5.", subject_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", subject_id))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentSafetyGateFinding:
        return AgentSafetyGateFinding(
            finding_id=f"agent_safety_gate_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by policy.",
        )


class AgentSafetyGateReportService:
    def build_request_from_intent_report(self, intent_report: AgentIntentClassificationReport) -> AgentSafetyGateRequest:
        return AgentSafetyGateRequest(
            request_id=f"agent_safety_gate_request:{_safe_id(intent_report.report_id)}",
            intent_report_id=intent_report.report_id,
            task_frame_id=intent_report.task_frame.task_frame_id,
            task_frame_candidate_id=intent_report.task_frame_candidate.candidate_id,
            turn_envelope_id=intent_report.request.turn_envelope_id,
            sanitized_request_text=intent_report.request.sanitized_request_text,
            source_refs=[{"type": "agent_intent_classification_report", "id": intent_report.report_id}],
        )

    def build_report(
        self,
        request_text: str = "Explain the project structure",
        intent_report: AgentIntentClassificationReport | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentSafetyGateReport:
        policy = AgentSafetyGatePolicyService().build_policy()
        source_report = intent_report or AgentIntentClassificationReportService().build_report(request_text=request_text)
        request = self.build_request_from_intent_report(source_report)
        candidate = source_report.task_frame_candidate
        risk_preview = source_report.task_frame.risk_preview
        rules = AgentSafetyRuleRegistry().list_rules()
        rule_results = AgentSafetyRuleEngine().evaluate_rules(request, candidate, risk_preview, rules, attempt_flags)
        gate_decision = AgentSafetyGateDecisionService().build_decision(rule_results, candidate, request)
        input_requirements = candidate.task_frame.input_requirements
        no_action = AgentNoActionDecisionService().build_decision(gate_decision)
        clarification_policy = AgentClarificationPolicyService().build_policy()
        clarification = AgentClarificationDecisionService().build_decision(gate_decision, input_requirements, clarification_policy)
        needs_more_input = AgentNeedsMoreInputDecisionService().build_decision(gate_decision, input_requirements)
        blocked = AgentBlockedDecisionService().build_decision(gate_decision)
        deferred = AgentDeferredDecisionService().build_decision(gate_decision, request)
        outcome_envelope = AgentGateOutcomeEnvelopeService().build_outcome_envelope(
            gate_decision,
            no_action,
            clarification,
            needs_more_input,
            blocked,
            deferred,
        )
        findings = AgentSafetyGateFindingService().build_findings(request, candidate, gate_decision, attempt_flags)
        report_status = self._report_status(gate_decision, findings)
        return AgentSafetyGateReport(
            report_id=f"agent_safety_gate_report:{_safe_id(request.request_id)}",
            created_at=_utc_now(),
            policy=policy,
            request=request,
            rule_results=rule_results,
            gate_decision=gate_decision,
            outcome_envelope=outcome_envelope,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_4=gate_decision.allow_route,
            ready_for_v0_25_6=not gate_decision.allow_route,
            allow_route=gate_decision.allow_route,
            final_no_action_decision=gate_decision.final_no_action_decision,
            final_clarification_decision=gate_decision.final_clarification_decision,
            final_needs_more_input_decision=gate_decision.final_needs_more_input_decision,
            final_blocked_decision=gate_decision.final_blocked_decision,
            final_deferred_decision=gate_decision.final_deferred_decision,
            next_required_step=gate_decision.expected_next_stage or AGENT_SAFETY_GATE_RESPONSE_NEXT_STEP,
            limitations=["v0.25.3 decides safety/no-action/clarification outcomes only; routing and provider invocation remain deferred."],
            withdrawal_conditions=["Withdraw if v0.25.3 creates tool route plans, selects or invokes providers, executes commands, promotes memory, mutates persona, or uses an LLM judge."],
        )

    def build_all_parts(self, request_text: str = "Explain the project structure") -> dict[str, Any]:
        report = self.build_report(request_text=request_text)
        rules = AgentSafetyRuleRegistry().list_rules()
        return {
            "report": report,
            "policy": report.policy,
            "request": report.request,
            "rules": rules,
            "rule_results": report.rule_results,
            "decision": report.gate_decision,
            "outcome_envelope": report.outcome_envelope,
            "no_action": report.outcome_envelope.no_action_decision,
            "clarification": report.outcome_envelope.clarification_decision,
            "needs_more_input": report.outcome_envelope.needs_more_input_decision,
            "blocked": report.outcome_envelope.blocked_decision,
            "deferred": report.outcome_envelope.deferred_decision,
            "findings": report.findings,
        }

    def _report_status(self, gate_decision: AgentSafetyGateDecision, findings: list[AgentSafetyGateFinding]) -> str:
        if gate_decision.primary_outcome == "blocked":
            return "blocked"
        if any(item.severity == "critical" for item in findings):
            return "blocked"
        if gate_decision.primary_outcome == "failed" or any(item.severity == "error" for item in findings):
            return "failed"
        if gate_decision.primary_outcome in {"no_action", "clarification_requested", "needs_more_input", "deferred"}:
            return "warning"
        if any(item.severity == "warning" for item in findings):
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_SAFETY_GATE_VERSION,
            "layer": "agent_surface",
            "subject": "safety_no_action_clarification_gate",
            "principles": [
                "safety gate is not tool routing",
                "no-action is a valid agent decision",
                "clarification is a valid agent decision",
                "blocked decision is a policy outcome, not an error",
                "allow-route is not provider invocation",
                "allow-route is not execution authorization",
                "user request is not permission",
                "LLM proposal is not safety judgment",
                "tool routing is deferred to v0.25.4",
                "provider invocation is deferred to v0.25.5",
            ],
            "safety_boundary": {
                "safety_gate_evaluated": "conditional",
                "final_no_action_decision": "conditional",
                "final_clarification_decision": "conditional",
                "final_needs_more_input_decision": "conditional",
                "final_blocked_decision": "conditional",
                "final_deferred_decision": "conditional",
                "allow_route": "conditional",
                "tool_route_created": False,
                "tool_route_executed": False,
                "provider_invoked": False,
                "local_command_executed": False,
                "ask_executed": False,
                "repl_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.25": "bounded agent surface",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": "v0.25.4 Tool Routing Plan & Provider Selection when allow_route=true, otherwise v0.25.6 Response Assembly & Evidence Binder",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_safety_gate_decision_created",
            "version": AGENT_SAFETY_GATE_VERSION,
            "source_read_models": [
                "AgentSurfaceContractState",
                "AgentTurnEnvelopeState",
                "AgentIntentClassificationState",
                "AgentTaskFrameState",
                "AgentTaskRiskPreviewState",
                "AgentTaskFrameCandidateState",
            ],
            "target_read_models": [
                "AgentSafetyGateState",
                "AgentNoActionDecisionState",
                "AgentClarificationDecisionState",
                "AgentNeedsMoreInputDecisionState",
                "AgentBlockedDecisionState",
                "AgentDeferredDecisionState",
                "AgentGateOutcomeState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_SAFETY_GATE_EFFECT_TYPES,
        }


def render_agent_safety_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentSafetyGateReport = parts["report"]
    decision = report.gate_decision
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"safety_gate_evaluated={str(report.safety_gate_evaluated).lower()}",
        f"primary_outcome={decision.primary_outcome}",
        f"allow_route={str(report.allow_route).lower()}",
        f"final_no_action_decision={str(report.final_no_action_decision).lower()}",
        f"final_clarification_decision={str(report.final_clarification_decision).lower()}",
        f"final_needs_more_input_decision={str(report.final_needs_more_input_decision).lower()}",
        f"final_blocked_decision={str(report.final_blocked_decision).lower()}",
        f"final_deferred_decision={str(report.final_deferred_decision).lower()}",
        f"ready_for_v0_25_4={str(report.ready_for_v0_25_4).lower()}",
        f"ready_for_v0_25_6={str(report.ready_for_v0_25_6).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"tool_route_created={str(report.tool_route_created).lower()}",
        f"tool_route_executed={str(report.tool_route_executed).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_started={str(report.repl_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "gate":
        lines.append(f"decision_confidence={decision.decision_confidence}")
        lines.append(f"decision_method={decision.decision_method}")
    elif section == "rules":
        for rule in parts["rules"]:
            lines.append(f"- {rule.rule_id}: {rule.rule_category}")
    elif section == "no-action":
        selected = parts["no_action"]
        lines.append(f"no_action_decision_id={selected.decision_id if selected else ''}")
        lines.append(f"no_action_valid={str(selected is not None).lower()}")
    elif section == "clarify":
        selected = parts["clarification"]
        lines.append(f"clarification_decision_id={selected.decision_id if selected else ''}")
        if selected:
            for question in selected.questions:
                lines.append(f"- question={question.question_text}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    else:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)
