from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
import time
from typing import Any

from chanta_core.agent_surface.contract import AgentSurfaceContractReportService
from chanta_core.agent_surface.turn_context import AgentTurnEnvelope, AgentTurnReport, AgentTurnReportService


AGENT_INTENT_TASK_VERSION = "v0.25.2"
AGENT_INTENT_TASK_VERSION_NAME = "Intent Classification & Task Framing"
AGENT_INTENT_TASK_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_INTENT_TASK_NEXT_STEP = "v0.25.3 Safety / No-Action / Clarification Gate"

AGENT_INTENT_OBJECT_TYPES = [
    "agent_intent_classification_policy",
    "agent_intent_classification_request",
    "agent_intent_taxonomy",
    "agent_intent_rule",
    "agent_intent_rule_result",
    "agent_intent_descriptor",
    "agent_task_goal",
    "agent_task_constraint",
    "agent_task_input_requirement",
    "agent_task_risk_preview",
    "agent_task_frame",
    "agent_task_frame_candidate",
    "agent_intent_finding",
    "agent_intent_classification_report",
    "agent_turn_envelope",
    "agent_turn_report",
    "agent_surface_contract",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_INTENT_EVENT_TYPES = [
    "agent_intent_classification_requested",
    "agent_intent_classification_policy_created",
    "agent_intent_taxonomy_created",
    "agent_intent_rules_loaded",
    "agent_intent_rules_evaluated",
    "agent_intent_classified",
    "agent_task_goal_created",
    "agent_task_constraint_created",
    "agent_task_input_requirement_created",
    "agent_task_risk_preview_created",
    "agent_task_framed",
    "agent_task_frame_candidate_created",
    "agent_intent_classification_report_created",
    "agent_intent_warning_created",
    "agent_intent_blocked",
]

AGENT_INTENT_RELATION_TYPES = [
    "uses_agent_turn_envelope",
    "uses_agent_surface_contract",
    "classifies_agent_intent",
    "evaluates_agent_intent_rule",
    "creates_agent_task_goal",
    "creates_agent_task_constraint",
    "creates_agent_input_requirement",
    "previews_agent_task_risk",
    "creates_agent_task_frame",
    "creates_agent_task_frame_candidate",
    "prepares_safety_gate",
    "defers_safety_gate_to_v0_25_3",
    "defers_tool_routing_to_v0_25_4",
    "defers_provider_invocation_to_v0_25_5",
    "defers_response_assembly_to_v0_25_6",
    "defers_ask_repl_to_v0_25_7",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_safety_gate_evaluated",
    "not_tool_route_executed",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_memory_promoted",
    "prevents_credential_exposure",
    "derived_from_agent_turn_envelope",
    "recorded_in_envelope",
]

AGENT_INTENT_EFFECT_TYPES = [
    "read_only_observation",
    "agent_intent_classified",
    "agent_task_framed",
    "agent_task_risk_preview_created",
    "state_candidate_created",
]

AGENT_INTENT_FORBIDDEN_EFFECT_TYPES = [
    "agent_safety_gate_evaluated",
    "agent_no_action_finalized",
    "agent_clarification_finalized",
    "agent_blocked_decision_finalized",
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

INTENT_CATEGORIES = [
    "general_answer",
    "workspace_overview",
    "repository_search",
    "file_read",
    "process_state_inspection",
    "local_runtime_candidate",
    "local_runtime_execution_request",
    "diagnostic_request",
    "explanation_request",
    "planning_request",
    "architecture_design",
    "implementation_prompt_request",
    "verification_prompt_request",
    "checklist_request",
    "consolidation_request",
    "no_action_candidate",
    "needs_more_input_candidate",
    "blocked_candidate",
    "unknown",
]

RISK_CATEGORIES = {
    "ambiguous_request",
    "unsafe_execution_request",
    "local_runtime_execution",
    "file_mutation",
    "memory_mutation",
    "external_adapter",
    "credential_exposure",
    "raw_secret_output",
    "private_path_exposure",
    "out_of_scope_track",
    "provider_boundary_bypass",
    "unknown",
}


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _safe_id(text: str | None) -> str:
    value = re.sub(r"[^a-zA-Z0-9_.:-]+", "_", text or "none").strip("_")
    return value[:100] or "none"


def _excerpt(text: str, pattern: str) -> str:
    lowered = text.lower()
    lowered_pattern = pattern.lower()
    index = lowered.find(lowered_pattern)
    if index < 0:
        return ""
    return text[index : index + min(len(pattern), 80)]


@dataclass
class AgentIntentClassificationPolicy:
    policy_id: str
    version: str = AGENT_INTENT_TASK_VERSION
    layer: str = "agent_surface"
    deterministic_default: bool = True
    external_llm_classification_enabled: bool = False
    llm_safety_judge_enabled: bool = False
    classify_from_turn_envelope_only: bool = True
    safety_gate_enabled: bool = False
    tool_routing_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    final_no_action_decision_enabled: bool = False
    final_clarification_decision_enabled: bool = False
    final_blocked_decision_enabled: bool = False
    memory_promotion_enabled: bool = False
    persona_mutation_enabled: bool = False
    raw_secret_storage_forbidden: bool = True
    private_path_sanitization_required: bool = True
    confidence_must_be_bounded: bool = True
    evidence_refs_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentClassificationRequest:
    request_id: str
    sanitized_request_text: str
    version: str = AGENT_INTENT_TASK_VERSION
    turn_envelope_id: str | None = None
    turn_report_id: str | None = None
    context_view_ref: dict[str, Any] | None = None
    surface_mode: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentTaxonomy:
    taxonomy_id: str
    categories: list[str]
    category_descriptions: dict[str, str]
    taxonomy_status: str
    version: str = AGENT_INTENT_TASK_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentRule:
    rule_id: str
    category: str
    rule_type: str
    patterns: list[str]
    positive_score: float
    negative_score: float
    risk_hint: str | None
    requires_context: bool = False
    enabled: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentRuleResult:
    result_id: str
    rule_id: str
    category: str
    matched: bool
    score_delta: float
    matched_text_excerpt: str | None
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentDescriptor:
    intent_id: str
    primary_category: str
    secondary_categories: list[str]
    confidence: str
    confidence_score: float
    classification_method: str
    matched_rules: list[AgentIntentRuleResult]
    requires_tool_routing_future: bool
    requires_provider_invocation_future: bool
    requires_local_runtime_gate_future: bool
    likely_needs_more_input: bool
    likely_no_action: bool
    likely_blocked: bool
    version: str = AGENT_INTENT_TASK_VERSION
    requires_safety_gate_next: bool = True
    final_no_action_decision: bool = False
    final_blocked_decision: bool = False
    final_clarification_decision: bool = False
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTaskGoal:
    goal_id: str
    goal_text: str
    normalized_goal: str
    goal_type: str
    measurable: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTaskConstraint:
    constraint_id: str
    constraint_type: str
    description: str
    hard: bool
    source: str
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTaskInputRequirement:
    input_requirement_id: str
    requirement_type: str
    description: str
    required_for_next_stage: bool
    missing: bool
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTaskRiskPreview:
    risk_preview_id: str
    risk_level: str
    risk_categories: list[str]
    requires_clarification_candidate: bool
    recommends_no_action_candidate: bool
    recommends_blocked_candidate: bool
    rationale: str
    requires_safety_gate_next: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTaskFrame:
    task_frame_id: str
    intent_id: str
    goals: list[AgentTaskGoal]
    constraints: list[AgentTaskConstraint]
    input_requirements: list[AgentTaskInputRequirement]
    risk_preview: AgentTaskRiskPreview
    task_frame_status: str
    version: str = AGENT_INTENT_TASK_VERSION
    expected_next_stage: str = AGENT_INTENT_TASK_NEXT_STEP
    safety_gate_evaluated: bool = False
    tool_route_created: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentTaskFrameCandidate:
    candidate_id: str
    task_frame: AgentTaskFrame
    candidate_status: str
    version: str = AGENT_INTENT_TASK_VERSION
    recommended_next_stage: str = AGENT_INTENT_TASK_NEXT_STEP
    executes_now: bool = False
    routes_now: bool = False
    invokes_provider_now: bool = False
    mutates_state_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentIntentClassificationReport:
    report_id: str
    created_at: str
    policy: AgentIntentClassificationPolicy
    request: AgentIntentClassificationRequest
    taxonomy: AgentIntentTaxonomy
    intent_descriptor: AgentIntentDescriptor
    task_frame: AgentTaskFrame
    task_frame_candidate: AgentTaskFrameCandidate
    findings: list[AgentIntentFinding]
    report_status: str
    ready_for_v0_25_3: bool
    intent_classified: bool
    task_framed: bool
    version: str = AGENT_INTENT_TASK_VERSION
    ready_for_v0_26: bool = False
    safety_gate_evaluated: bool = False
    final_no_action_decision: bool = False
    final_clarification_decision: bool = False
    final_blocked_decision: bool = False
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
    next_required_step: str = AGENT_INTENT_TASK_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.3 safety gate begins or intent/task classification policy changes."

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class AgentIntentPrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        return {
            "source_id": "agent_surface_contract_report:v0.25.0",
            "available": AgentSurfaceContractReportService().build_report().report_status in {"passed", "warning"},
            "read_only": True,
        }

    def load_turn_envelope(self, request_text: str = "Explain the project structure") -> AgentTurnEnvelope:
        return AgentTurnReportService().build_report(request_text=request_text).envelope

    def load_turn_report(self, request_text: str = "Explain the project structure") -> AgentTurnReport:
        return AgentTurnReportService().build_report(request_text=request_text)

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return {"source_id": "agent_surface_skill_registry:v0.25.2", "available": True, "read_only": True}

    def load_provider_registry_if_available(self) -> dict[str, Any]:
        return {"source_id": "internal_provider_registry:v0.24.9", "available": True, "read_only": True}


class AgentIntentClassificationPolicyService:
    def build_policy(self) -> AgentIntentClassificationPolicy:
        return AgentIntentClassificationPolicy(
            policy_id="agent_intent_classification_policy:v0.25.2",
            evidence_refs=[{"type": "turn_envelope_policy", "version": "v0.25.1"}],
        )


class AgentIntentTaxonomyService:
    def build_taxonomy(self) -> AgentIntentTaxonomy:
        descriptions = {
            category: category.replace("_", " ") + " intent category."
            for category in INTENT_CATEGORIES
        }
        return AgentIntentTaxonomy(
            taxonomy_id="agent_intent_taxonomy:v0.25.2",
            categories=list(INTENT_CATEGORIES),
            category_descriptions=descriptions,
            taxonomy_status="ready",
            evidence_refs=[{"type": "deterministic_taxonomy", "version": AGENT_INTENT_TASK_VERSION}],
        )


class AgentIntentRuleRegistry:
    def list_rules(self) -> list[AgentIntentRule]:
        rule_data = [
            ("general_answer", "keyword", ["what is", "how do", "explain", "tell me", "answer"], 1.0, None),
            ("workspace_overview", "phrase", ["project structure", "workspace overview", "workspace tree", "repo structure"], 1.6, None),
            ("repository_search", "keyword", ["search", "find in repository", "repository search", "rg ", "grep"], 1.6, None),
            ("file_read", "keyword", ["read file", "open file", "show file", "file content", ".py", ".md"], 1.5, None),
            ("process_state_inspection", "phrase", ["process state", "running process", "pid", "runtime state"], 1.7, None),
            ("local_runtime_candidate", "phrase", ["command candidate", "candidate command", "suggest command", "local runtime candidate"], 1.8, None),
            ("local_runtime_execution_request", "keyword", ["run ", "execute", "pytest", "ruff", "mypy", "compileall", "git status"], 2.0, "local_runtime_execution"),
            ("diagnostic_request", "keyword", ["diagnose", "debug", "failure", "error", "why failed"], 1.4, None),
            ("explanation_request", "keyword", ["explain", "why", "what happened", "무슨 말"], 1.3, None),
            ("planning_request", "keyword", ["plan", "roadmap", "next steps", "tomorrow", "내일"], 1.3, None),
            ("architecture_design", "keyword", ["architecture", "design", "contract", "boundary", "policy"], 1.4, None),
            ("implementation_prompt_request", "phrase", ["codex 생성", "implementation prompt", "implement v", "target version"], 1.9, None),
            ("verification_prompt_request", "keyword", ["검증", "review", "verify", "validation", "audit"], 1.7, None),
            ("checklist_request", "keyword", ["checklist", "체크리스트", "[ ]"], 1.7, None),
            ("consolidation_request", "keyword", ["consolidation", "consolidate", "release manifest", "readiness"], 1.8, None),
            ("no_action_candidate", "phrase", ["do nothing", "stop here", "여기까지", "대기"], 1.9, None),
            ("needs_more_input_candidate", "keyword", ["unclear", "ambiguous", "뭐하지", "모르겠"], 1.5, "ambiguous_request"),
            ("blocked_candidate", "keyword", ["credential", "secret", "token", "password", "schumpeter"], 1.9, "credential_exposure"),
            ("blocked_candidate", "phrase", ["external adapter", "provider adapter", "opencode runtime", "openclaw runtime", "hermes runtime"], 1.9, "external_adapter"),
            ("blocked_candidate", "phrase", ["memory continuity", "promote memory", "persistent memory", "workspace workbench"], 1.8, "out_of_scope_track"),
        ]
        return [
            AgentIntentRule(
                rule_id=f"agent_intent_rule:{idx}:{category}",
                category=category,
                rule_type=rule_type,
                patterns=patterns,
                positive_score=score,
                negative_score=0.0,
                risk_hint=risk_hint,
                evidence_refs=[{"type": "deterministic_rule"}],
            )
            for idx, (category, rule_type, patterns, score, risk_hint) in enumerate(rule_data)
        ] + [
            AgentIntentRule(
                rule_id="agent_intent_rule:fallback:unknown",
                category="unknown",
                rule_type="fallback",
                patterns=[],
                positive_score=0.2,
                negative_score=0.0,
                risk_hint="unknown",
                evidence_refs=[{"type": "fallback_rule"}],
            )
        ]


class AgentIntentRuleEngine:
    def evaluate_rules(
        self,
        request: AgentIntentClassificationRequest,
        taxonomy: AgentIntentTaxonomy,
        rules: list[AgentIntentRule] | None = None,
    ) -> list[AgentIntentRuleResult]:
        text = request.sanitized_request_text or ""
        lowered = text.lower()
        active_rules = rules or AgentIntentRuleRegistry().list_rules()
        results: list[AgentIntentRuleResult] = []
        matched_any = False
        for rule in active_rules:
            if not rule.enabled:
                continue
            if rule.rule_type == "fallback":
                continue
            matched_pattern = next((pattern for pattern in rule.patterns if pattern.lower() in lowered), None)
            matched = matched_pattern is not None and rule.category in taxonomy.categories
            if matched:
                matched_any = True
            results.append(
                AgentIntentRuleResult(
                    result_id=f"agent_intent_rule_result:{_safe_id(rule.rule_id)}",
                    rule_id=rule.rule_id,
                    category=rule.category,
                    matched=matched,
                    score_delta=rule.positive_score if matched else -rule.negative_score,
                    matched_text_excerpt=_excerpt(text, matched_pattern) if matched_pattern else None,
                    evidence_refs=[{"type": "rule_type", "value": rule.rule_type}],
                )
            )
        fallback = next(rule for rule in active_rules if rule.rule_type == "fallback")
        results.append(
            AgentIntentRuleResult(
                result_id="agent_intent_rule_result:fallback:unknown",
                rule_id=fallback.rule_id,
                category=fallback.category,
                matched=not matched_any,
                score_delta=fallback.positive_score if not matched_any else 0.0,
                matched_text_excerpt=None,
                evidence_refs=[{"type": "fallback_rule"}],
            )
        )
        return results


class AgentIntentDescriptorService:
    ROUTING_CATEGORIES = {
        "repository_search",
        "file_read",
        "process_state_inspection",
        "local_runtime_candidate",
        "local_runtime_execution_request",
        "diagnostic_request",
    }

    PROVIDER_CATEGORIES = {
        "workspace_overview",
        "repository_search",
        "file_read",
        "process_state_inspection",
        "local_runtime_candidate",
        "diagnostic_request",
    }

    def build_intent_descriptor(
        self,
        rule_results: list[AgentIntentRuleResult],
        request: AgentIntentClassificationRequest,
    ) -> AgentIntentDescriptor:
        scores: dict[str, float] = {}
        matched = [result for result in rule_results if result.matched]
        for result in matched:
            scores[result.category] = scores.get(result.category, 0.0) + result.score_delta
        if not scores:
            scores = {"unknown": 0.2}
        ordered = sorted(scores.items(), key=lambda item: item[1], reverse=True)
        primary, top_score = ordered[0]
        secondary = [category for category, score in ordered[1:] if score >= 1.0]
        confidence_score = min(max(top_score / 3.0, 0.0), 1.0)
        confidence = "high" if confidence_score >= 0.7 else "medium" if confidence_score >= 0.4 else "low"
        likely_needs_more_input = primary in {"unknown", "needs_more_input_candidate"} or len(request.sanitized_request_text.strip()) < 3
        likely_no_action = primary == "no_action_candidate"
        likely_blocked = primary == "blocked_candidate"
        return AgentIntentDescriptor(
            intent_id=f"agent_intent_descriptor:{_safe_id(request.request_id)}",
            primary_category=primary,
            secondary_categories=secondary,
            confidence=confidence,
            confidence_score=round(confidence_score, 3),
            classification_method="deterministic_rules",
            matched_rules=matched,
            requires_tool_routing_future=primary in self.ROUTING_CATEGORIES,
            requires_provider_invocation_future=primary in self.PROVIDER_CATEGORIES,
            requires_local_runtime_gate_future=primary == "local_runtime_execution_request",
            likely_needs_more_input=likely_needs_more_input,
            likely_no_action=likely_no_action,
            likely_blocked=likely_blocked,
            evidence_refs=[{"type": "rule_result_count", "count": len(rule_results)}],
        )


class AgentTaskGoalService:
    GOAL_TYPES = {
        "general_answer": "answer",
        "workspace_overview": "inspect",
        "repository_search": "search",
        "file_read": "read",
        "process_state_inspection": "inspect",
        "local_runtime_candidate": "plan",
        "local_runtime_execution_request": "execute_candidate_future",
        "diagnostic_request": "explain",
        "explanation_request": "explain",
        "planning_request": "plan",
        "architecture_design": "plan",
        "implementation_prompt_request": "generate_prompt",
        "verification_prompt_request": "verify",
        "checklist_request": "checklist",
        "consolidation_request": "consolidate",
    }

    def extract_goals(self, request: AgentIntentClassificationRequest, intent: AgentIntentDescriptor) -> list[AgentTaskGoal]:
        goal_type = self.GOAL_TYPES.get(intent.primary_category, "unknown")
        normalized = request.sanitized_request_text.strip() or "unknown"
        return [
            AgentTaskGoal(
                goal_id=f"agent_task_goal:{_safe_id(intent.intent_id)}",
                goal_text=normalized[:500],
                normalized_goal=normalized.lower()[:500],
                goal_type=goal_type,
                measurable=goal_type not in {"unknown"},
                evidence_refs=[{"type": "primary_category", "value": intent.primary_category}],
            )
        ]


class AgentTaskConstraintService:
    def extract_constraints(
        self,
        request: AgentIntentClassificationRequest,
        intent: AgentIntentDescriptor,
        policy: AgentIntentClassificationPolicy,
    ) -> list[AgentTaskConstraint]:
        constraints = [
            AgentTaskConstraint(
                constraint_id="agent_task_constraint:no_execution:v0.25.2",
                constraint_type="no_execution",
                description="v0.25.2 must not execute commands, ask/REPL, providers, or routes.",
                hard=True,
                source="policy",
                evidence_refs=[{"type": "policy", "policy_id": policy.policy_id}],
            ),
            AgentTaskConstraint(
                constraint_id="agent_task_constraint:requires_safety_gate:v0.25.2",
                constraint_type="requires_evidence",
                description="The task frame must proceed to v0.25.3 safety/no-action/clarification gate before action.",
                hard=True,
                source="policy",
                evidence_refs=[{"type": "next_stage", "value": AGENT_INTENT_TASK_NEXT_STEP}],
            ),
        ]
        if intent.requires_provider_invocation_future:
            constraints.append(
                AgentTaskConstraint(
                    constraint_id="agent_task_constraint:provider_boundary:v0.25.2",
                    constraint_type="requires_provider_boundary",
                    description="Future provider use must respect internal provider boundaries.",
                    hard=True,
                    source="policy",
                    evidence_refs=[{"type": "primary_category", "value": intent.primary_category}],
                )
            )
        if intent.likely_needs_more_input:
            constraints.append(
                AgentTaskConstraint(
                    constraint_id="agent_task_constraint:needs_clarification_candidate:v0.25.2",
                    constraint_type="requires_user_clarification",
                    description="The request may need more input, but v0.25.2 does not finalize clarification.",
                    hard=False,
                    source="inferred",
                    evidence_refs=[{"type": "confidence", "value": intent.confidence}],
                )
            )
        return constraints


class AgentTaskInputRequirementService:
    def infer_input_requirements(
        self,
        request: AgentIntentClassificationRequest,
        intent: AgentIntentDescriptor,
        constraints: list[AgentTaskConstraint],
    ) -> list[AgentTaskInputRequirement]:
        requirements: list[AgentTaskInputRequirement] = []
        text = request.sanitized_request_text.lower()
        if intent.primary_category == "file_read":
            missing = not any(token in text for token in [".py", ".md", "/", "\\"])
            requirements.append(self._requirement("target_path", "Target file path is required for a future file read.", missing))
        if intent.primary_category in {"repository_search", "process_state_inspection"}:
            requirements.append(self._requirement("repository_context", "Repository or process context may be required by future stages.", False))
        if intent.primary_category == "local_runtime_execution_request":
            requirements.append(self._requirement("execution_authorization", "Future local runtime execution requires v0.24 gate authorization.", True))
        if intent.likely_needs_more_input:
            requirements.append(self._requirement("clarification", "The next gate may request clarification.", True))
        if not requirements:
            requirements.append(self._requirement("none", "No required input was detected for task framing.", False))
        return requirements

    def _requirement(self, requirement_type: str, description: str, missing: bool) -> AgentTaskInputRequirement:
        return AgentTaskInputRequirement(
            input_requirement_id=f"agent_task_input_requirement:{requirement_type}",
            requirement_type=requirement_type,
            description=description,
            required_for_next_stage=missing,
            missing=missing,
            evidence_refs=[{"type": "input_requirement", "requirement_type": requirement_type}],
        )


class AgentTaskRiskPreviewService:
    def build_risk_preview(
        self,
        request: AgentIntentClassificationRequest,
        intent: AgentIntentDescriptor,
        constraints: list[AgentTaskConstraint],
    ) -> AgentTaskRiskPreview:
        text = request.sanitized_request_text.lower()
        risk_categories: set[str] = set()
        if intent.primary_category in {"unknown", "needs_more_input_candidate"}:
            risk_categories.add("ambiguous_request")
        if intent.primary_category == "local_runtime_execution_request":
            risk_categories.update({"unsafe_execution_request", "local_runtime_execution"})
        if any(word in text for word in ["write", "edit", "delete", "patch", "modify"]):
            risk_categories.add("file_mutation")
        if any(word in text for word in ["memory", "persistent memory", "promote memory"]):
            risk_categories.update({"memory_mutation", "out_of_scope_track"})
        if any(word in text for word in ["external adapter", "provider adapter", "agent adapter"]):
            risk_categories.update({"external_adapter", "out_of_scope_track"})
        if any(word in text for word in ["credential", "secret", "token", "password", "<redacted"]):
            risk_categories.update({"credential_exposure", "raw_secret_output"})
        if "private path" in text or "<sanitized_private_path>" in text:
            risk_categories.add("private_path_exposure")
        if any(word in text for word in ["bypass", "ignore boundary", "skip gate"]):
            risk_categories.add("provider_boundary_bypass")
        if "schumpeter" in text or "workspace workbench" in text:
            risk_categories.add("out_of_scope_track")
        if not risk_categories:
            risk_categories.add("unknown" if intent.primary_category == "unknown" else "ambiguous_request" if intent.confidence == "low" else "")
            risk_categories.discard("")
        if {"credential_exposure", "raw_secret_output", "external_adapter"} & risk_categories:
            risk_level = "blocked"
        elif {"local_runtime_execution", "file_mutation", "memory_mutation", "provider_boundary_bypass"} & risk_categories:
            risk_level = "high"
        elif risk_categories:
            risk_level = "medium" if "ambiguous_request" in risk_categories or "out_of_scope_track" in risk_categories else "low"
        else:
            risk_level = "none"
        return AgentTaskRiskPreview(
            risk_preview_id=f"agent_task_risk_preview:{_safe_id(intent.intent_id)}",
            risk_level=risk_level,
            risk_categories=sorted(risk_categories),
            requires_clarification_candidate=intent.likely_needs_more_input or "ambiguous_request" in risk_categories,
            recommends_no_action_candidate=intent.likely_no_action,
            recommends_blocked_candidate=intent.likely_blocked or risk_level == "blocked",
            rationale="Risk preview only; v0.25.3 must make any safety, no-action, clarification, or blocked decision.",
            evidence_refs=[{"type": "primary_category", "value": intent.primary_category}],
        )


class AgentTaskFrameService:
    def build_task_frame(
        self,
        intent: AgentIntentDescriptor,
        goals: list[AgentTaskGoal],
        constraints: list[AgentTaskConstraint],
        input_requirements: list[AgentTaskInputRequirement],
        risk_preview: AgentTaskRiskPreview,
    ) -> AgentTaskFrame:
        if intent.likely_blocked or risk_preview.recommends_blocked_candidate:
            status = "blocked_candidate"
        elif intent.likely_no_action:
            status = "no_action_candidate"
        elif intent.likely_needs_more_input or any(item.missing for item in input_requirements):
            status = "needs_more_input_candidate"
        else:
            status = "framed"
        return AgentTaskFrame(
            task_frame_id=f"agent_task_frame:{_safe_id(intent.intent_id)}",
            intent_id=intent.intent_id,
            goals=goals,
            constraints=constraints,
            input_requirements=input_requirements,
            risk_preview=risk_preview,
            task_frame_status=status,
            evidence_refs=[{"type": "next_stage", "value": AGENT_INTENT_TASK_NEXT_STEP}],
        )


class AgentTaskFrameCandidateService:
    def build_candidate(self, task_frame: AgentTaskFrame) -> AgentTaskFrameCandidate:
        status = "ready_for_safety_gate" if task_frame.task_frame_status == "framed" else task_frame.task_frame_status
        return AgentTaskFrameCandidate(
            candidate_id=f"agent_task_frame_candidate:{_safe_id(task_frame.task_frame_id)}",
            task_frame=task_frame,
            candidate_status=status,
            evidence_refs=[{"type": "candidate_only", "executes_now": False}],
        )


class AgentIntentFindingService:
    WARNING_TYPES = {
        "ambiguous_request",
        "unknown_intent",
        "multiple_intents_detected",
        "likely_needs_more_input",
        "likely_no_action",
        "likely_blocked",
        "local_runtime_execution_request_detected",
        "provider_boundary_required",
        "external_adapter_request_detected",
        "memory_continuity_request_detected",
        "workspace_workbench_request_detected",
        "schumpeter_split_request_detected",
        "safety_gate_required_next",
        "tool_routing_deferred",
        "provider_invocation_deferred",
        "raw_secret_input_detected",
        "credential_like_input_detected",
        "private_path_like_input_detected",
    }

    CRITICAL_ATTEMPTS = {
        "ask_execution_attempted_too_early",
        "repl_execution_attempted_too_early",
        "safety_gate_attempted_too_early",
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
        request: AgentIntentClassificationRequest,
        intent: AgentIntentDescriptor,
        task_frame: AgentTaskFrame,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentIntentFinding]:
        findings = [
            self._finding("info", "ok", "Intent was classified and task frame was created without execution.", intent.intent_id)
        ]
        if not request.turn_envelope_id:
            findings.append(self._finding("error", "missing_turn_envelope", "Turn envelope reference is missing.", request.request_id))
        if not request.sanitized_request_text:
            findings.append(self._finding("error", "missing_sanitized_request", "Sanitized request text is missing.", request.request_id))
            findings.append(self._finding("error", "empty_request", "Request text is empty.", request.request_id))
        if intent.confidence == "low":
            findings.append(self._finding("warning", "ambiguous_request", "Intent confidence is low.", intent.intent_id))
        if intent.primary_category == "unknown":
            findings.append(self._finding("warning", "unknown_intent", "Intent category is unknown.", intent.intent_id))
        if intent.secondary_categories:
            findings.append(self._finding("warning", "multiple_intents_detected", "Multiple intent categories were detected.", intent.intent_id))
        if intent.likely_needs_more_input:
            findings.append(self._finding("warning", "likely_needs_more_input", "The request may need more input, but v0.25.2 does not finalize clarification.", intent.intent_id))
        if intent.likely_no_action:
            findings.append(self._finding("warning", "likely_no_action", "The request may be a no-action candidate, but v0.25.2 does not finalize no-action.", intent.intent_id))
        if intent.likely_blocked:
            findings.append(self._finding("warning", "likely_blocked", "The request may be blocked, but v0.25.2 does not finalize blocked decisions.", intent.intent_id))
        if intent.primary_category == "local_runtime_execution_request":
            findings.append(self._finding("warning", "local_runtime_execution_request_detected", "Local runtime execution request detected for future gate.", intent.intent_id))
        if intent.requires_provider_invocation_future:
            findings.append(self._finding("warning", "provider_boundary_required", "Future provider boundary may be required.", intent.intent_id))
            findings.append(self._finding("warning", "provider_invocation_deferred", "Provider invocation is deferred to v0.25.5.", intent.intent_id))
        if intent.requires_tool_routing_future:
            findings.append(self._finding("warning", "tool_routing_deferred", "Tool routing is deferred to v0.25.4.", intent.intent_id))
        findings.append(self._finding("warning", "safety_gate_required_next", "Safety/no-action/clarification gate is deferred to v0.25.3.", task_frame.task_frame_id))
        risk_types = set(task_frame.risk_preview.risk_categories)
        if "external_adapter" in risk_types:
            findings.append(self._finding("warning", "external_adapter_request_detected", "External adapter request detected as future-track risk.", intent.intent_id))
        if "memory_mutation" in risk_types:
            findings.append(self._finding("warning", "memory_continuity_request_detected", "Memory continuity request detected as future-track risk.", intent.intent_id))
        if "out_of_scope_track" in risk_types and "workspace workbench" in request.sanitized_request_text.lower():
            findings.append(self._finding("warning", "workspace_workbench_request_detected", "Workspace workbench request detected as future-track risk.", intent.intent_id))
        if "schumpeter" in request.sanitized_request_text.lower():
            findings.append(self._finding("warning", "schumpeter_split_request_detected", "Schumpeter split request detected as future-track risk.", intent.intent_id))
        if "raw_secret_output" in risk_types:
            findings.append(self._finding("warning", "raw_secret_input_detected", "Secret-like input was detected from sanitized turn view.", intent.intent_id))
        if "credential_exposure" in risk_types:
            findings.append(self._finding("warning", "credential_like_input_detected", "Credential-like input was detected from sanitized turn view.", intent.intent_id))
        if "private_path_exposure" in risk_types:
            findings.append(self._finding("warning", "private_path_like_input_detected", "Private-path-like input was detected from sanitized turn view.", intent.intent_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                severity = "critical" if finding_type in self.CRITICAL_ATTEMPTS else "warning"
                findings.append(self._finding(severity, finding_type, f"{finding_type} was detected.", intent.intent_id))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentIntentFinding:
        return AgentIntentFinding(
            finding_id=f"agent_intent_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by policy.",
        )


class AgentIntentClassificationReportService:
    def build_request_from_turn_report(self, turn_report: AgentTurnReport) -> AgentIntentClassificationRequest:
        envelope = turn_report.envelope
        return AgentIntentClassificationRequest(
            request_id=f"agent_intent_classification_request:{_safe_id(envelope.request_id)}",
            turn_envelope_id=envelope.envelope_id,
            turn_report_id=turn_report.report_id,
            sanitized_request_text=envelope.user_request_view.sanitized_request_text,
            context_view_ref={"context_view_id": turn_report.context_view.context_view_id},
            surface_mode=envelope.surface_mode,
            source_refs=[{"type": "agent_turn_report", "id": turn_report.report_id}],
        )

    def build_report(
        self,
        request_text: str = "Explain the project structure",
        turn_report: AgentTurnReport | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentIntentClassificationReport:
        policy = AgentIntentClassificationPolicyService().build_policy()
        source_report = turn_report or AgentTurnReportService().build_report(request_text=request_text)
        request = self.build_request_from_turn_report(source_report)
        taxonomy = AgentIntentTaxonomyService().build_taxonomy()
        rules = AgentIntentRuleRegistry().list_rules()
        rule_results = AgentIntentRuleEngine().evaluate_rules(request, taxonomy, rules)
        intent = AgentIntentDescriptorService().build_intent_descriptor(rule_results, request)
        goals = AgentTaskGoalService().extract_goals(request, intent)
        constraints = AgentTaskConstraintService().extract_constraints(request, intent, policy)
        input_requirements = AgentTaskInputRequirementService().infer_input_requirements(request, intent, constraints)
        risk_preview = AgentTaskRiskPreviewService().build_risk_preview(request, intent, constraints)
        task_frame = AgentTaskFrameService().build_task_frame(intent, goals, constraints, input_requirements, risk_preview)
        candidate = AgentTaskFrameCandidateService().build_candidate(task_frame)
        findings = AgentIntentFindingService().build_findings(request, intent, task_frame, attempt_flags)
        blocked = any(finding.severity == "critical" for finding in findings)
        failed = any(finding.severity == "error" for finding in findings)
        warning = any(finding.severity == "warning" for finding in findings)
        report_status = "blocked" if blocked else "failed" if failed else "warning" if warning else "passed"
        return AgentIntentClassificationReport(
            report_id=f"agent_intent_classification_report:{_safe_id(request.request_id)}",
            created_at=_utc_now(),
            policy=policy,
            request=request,
            taxonomy=taxonomy,
            intent_descriptor=intent,
            task_frame=task_frame,
            task_frame_candidate=candidate,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_3=report_status in {"passed", "warning"},
            intent_classified=True,
            task_framed=True,
            limitations=["v0.25.2 classifies intent and frames tasks only; v0.25.3 must make safety/no-action/clarification decisions."],
            withdrawal_conditions=["Withdraw if v0.25.2 executes ask/REPL, runs safety gate, routes tools, invokes providers, executes commands, writes memory, mutates persona, or uses an LLM judge."],
        )

    def build_all_parts(self, request_text: str = "Explain the project structure") -> dict[str, Any]:
        report = self.build_report(request_text=request_text)
        rules = AgentIntentRuleRegistry().list_rules()
        return {
            "report": report,
            "policy": report.policy,
            "request": report.request,
            "taxonomy": report.taxonomy,
            "rules": rules,
            "intent": report.intent_descriptor,
            "task_frame": report.task_frame,
            "candidate": report.task_frame_candidate,
            "findings": report.findings,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_INTENT_TASK_VERSION,
            "layer": "agent_surface",
            "subject": "intent_classification_task_framing",
            "principles": [
                "intent classification is not safety approval",
                "task framing is not tool routing",
                "intent category is not provider selection",
                "risk preview is not safety gate",
                "needs-more-input candidate is not clarification gate",
                "blocked candidate is not final blocked decision",
                "no-action candidate is not final no-action decision",
                "provider invocation is deferred to v0.25.5",
                "safety/no-action/clarification gate is deferred to v0.25.3",
                "tool routing is deferred to v0.25.4",
            ],
            "safety_boundary": {
                "intent_classified": "conditional",
                "task_framed": "conditional",
                "safety_gate_evaluated": False,
                "final_no_action_decision": False,
                "final_clarification_decision": False,
                "final_blocked_decision": False,
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
            "next_step": AGENT_INTENT_TASK_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_intent_task_frame_created",
            "version": AGENT_INTENT_TASK_VERSION,
            "source_read_models": [
                "AgentSurfaceContractState",
                "AgentTurnEnvelopeState",
                "AgentInteractionSessionState",
                "AgentRequestContextViewState",
                "AgentTurnTraceState",
            ],
            "target_read_models": [
                "AgentIntentClassificationState",
                "AgentIntentDescriptorState",
                "AgentTaskFrameState",
                "AgentTaskRiskPreviewState",
                "AgentTaskFrameCandidateState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_INTENT_EFFECT_TYPES,
        }


def render_agent_intent_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentIntentClassificationReport = parts["report"]
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"intent_classified={str(report.intent_classified).lower()}",
        f"task_framed={str(report.task_framed).lower()}",
        f"ready_for_v0_25_3={str(report.ready_for_v0_25_3).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"safety_gate_evaluated={str(report.safety_gate_evaluated).lower()}",
        f"final_no_action_decision={str(report.final_no_action_decision).lower()}",
        f"final_clarification_decision={str(report.final_clarification_decision).lower()}",
        f"final_blocked_decision={str(report.final_blocked_decision).lower()}",
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
    if section == "classify":
        lines.append(f"primary_category={report.intent_descriptor.primary_category}")
        lines.append(f"confidence={report.intent_descriptor.confidence}")
        lines.append(f"confidence_score={report.intent_descriptor.confidence_score}")
    elif section == "frame":
        lines.append(f"task_frame_id={report.task_frame.task_frame_id}")
        lines.append(f"task_frame_status={report.task_frame.task_frame_status}")
        lines.append(f"candidate_status={report.task_frame_candidate.candidate_status}")
    elif section == "taxonomy":
        lines.append(f"taxonomy_id={report.taxonomy.taxonomy_id}")
        lines.append(f"categories={','.join(report.taxonomy.categories)}")
    elif section == "rules":
        for rule in parts["rules"]:
            lines.append(f"- {rule.rule_id}: {rule.category}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    else:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)
