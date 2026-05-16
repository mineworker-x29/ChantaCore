from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal
from uuid import uuid4

from chanta_core.self_awareness.workspace_awareness import READ_ONLY_OBSERVATION_EFFECT


INTENTION_CANDIDATE_EFFECTS = [READ_ONLY_OBSERVATION_EFFECT, "state_candidate_created"]
INTENTION_CANDIDATE_STATE = "self_directed_intention_candidate_awareness"
SUPPORTED_CANDIDATE_TYPES = {"plan", "todo", "no_action", "needs_more_input"}
SUPPORTED_STRICTNESS = {"lenient", "standard", "strict"}
BLOCKED_CAPABILITIES = [
    "write",
    "shell",
    "network",
    "mcp",
    "plugin",
    "external_harness",
    "task_queue",
    "scheduler",
    "memory_mutation",
    "persona_mutation",
    "overlay_mutation",
    "canonical_promotion",
]


@dataclass(frozen=True)
class SelfDirectedIntentionRequest:
    goal_text: str | None = None
    root_id: str | None = None
    source_candidate_ids: list[str] = field(default_factory=list)
    source_report_ids: list[str] = field(default_factory=list)
    target_scope: str = "self_awareness"
    candidate_types: list[str] = field(
        default_factory=lambda: ["plan", "todo", "no_action", "needs_more_input"]
    )
    strictness: str = "standard"
    max_plan_steps: int = 8
    max_todo_items: int = 12
    include_no_action: bool = True
    include_needs_more_input: bool = True

    def normalized(self) -> "SelfDirectedIntentionRequest":
        candidate_types = [
            item for item in self.candidate_types if item in SUPPORTED_CANDIDATE_TYPES
        ] or ["plan", "todo", "no_action", "needs_more_input"]
        return SelfDirectedIntentionRequest(
            goal_text=(self.goal_text or None),
            root_id=self.root_id,
            source_candidate_ids=list(self.source_candidate_ids),
            source_report_ids=list(self.source_report_ids),
            target_scope=self.target_scope or "self_awareness",
            candidate_types=candidate_types,
            strictness=self.strictness if self.strictness in SUPPORTED_STRICTNESS else "standard",
            max_plan_steps=min(max(1, int(self.max_plan_steps)), 8),
            max_todo_items=min(max(1, int(self.max_todo_items)), 12),
            include_no_action=bool(self.include_no_action),
            include_needs_more_input=bool(self.include_needs_more_input),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "goal_text": self.goal_text,
            "root_id": self.root_id,
            "source_candidate_ids": list(self.source_candidate_ids),
            "source_report_ids": list(self.source_report_ids),
            "target_scope": self.target_scope,
            "candidate_types": list(self.candidate_types),
            "strictness": self.strictness,
            "max_plan_steps": self.max_plan_steps,
            "max_todo_items": self.max_todo_items,
            "include_no_action": self.include_no_action,
            "include_needs_more_input": self.include_needs_more_input,
        }


@dataclass(frozen=True)
class IntentionSourceRef:
    ref_type: str
    ref_id: str
    source_kind: str
    summary: str | None
    confidence: Literal["low", "medium", "high"]
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return {
            "ref_type": self.ref_type,
            "ref_id": self.ref_id,
            "source_kind": self.source_kind,
            "summary": self.summary,
            "confidence": self.confidence,
            "evidence_refs": [dict(item) for item in self.evidence_refs],
        }


@dataclass(frozen=True)
class IntentionConstraint:
    constraint_type: str
    description: str
    severity: Literal["info", "warning", "hard_block"]
    source_ref: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "constraint_type": self.constraint_type,
            "description": self.description,
            "severity": self.severity,
            "source_ref": dict(self.source_ref) if self.source_ref else None,
        }


@dataclass(frozen=True)
class IntentionRiskAssessment:
    risk_level: Literal["low", "medium", "high", "blocked"]
    risk_reasons: list[str]
    blocked_capabilities: list[str]
    required_review: bool
    safe_to_materialize: bool = False
    safe_to_execute: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "risk_level": self.risk_level,
            "risk_reasons": list(self.risk_reasons),
            "blocked_capabilities": list(self.blocked_capabilities),
            "required_review": self.required_review,
            "safe_to_materialize": self.safe_to_materialize,
            "safe_to_execute": self.safe_to_execute,
        }


@dataclass(frozen=True)
class SelfPlanStepCandidate:
    step_id: str
    title: str
    description: str
    step_type: Literal[
        "observe",
        "read",
        "search",
        "summarize",
        "verify",
        "review",
        "no_action",
        "needs_more_input",
        "future_write_candidate",
        "future_shell_candidate",
        "future_network_candidate",
        "future_mcp_candidate",
        "future_plugin_candidate",
        "blocked",
    ]
    suggested_skill_id: str | None
    required_evidence_refs: list[dict[str, Any]]
    expected_output: str | None
    risk_assessment: IntentionRiskAssessment
    execution_enabled: bool = False
    materialized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "step_id": self.step_id,
            "title": self.title,
            "description": self.description,
            "step_type": self.step_type,
            "suggested_skill_id": self.suggested_skill_id,
            "required_evidence_refs": [dict(item) for item in self.required_evidence_refs],
            "expected_output": self.expected_output,
            "risk_assessment": self.risk_assessment.to_dict(),
            "execution_enabled": self.execution_enabled,
            "materialized": self.materialized,
        }


@dataclass(frozen=True)
class SelfPlanCandidate:
    candidate_id: str
    title: str
    goal_text: str | None
    source_refs: list[IntentionSourceRef]
    constraints: list[IntentionConstraint]
    steps: list[SelfPlanStepCandidate]
    confidence: Literal["low", "medium", "high"]
    risk_assessment: IntentionRiskAssessment
    limitations: list[str]
    review_status: str = "candidate_only"
    requires_review: bool = True
    materialized: bool = False
    execution_enabled: bool = False
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "title": self.title,
            "goal_text": self.goal_text,
            "source_refs": [item.to_dict() for item in self.source_refs],
            "constraints": [item.to_dict() for item in self.constraints],
            "steps": [item.to_dict() for item in self.steps],
            "confidence": self.confidence,
            "risk_assessment": self.risk_assessment.to_dict(),
            "limitations": list(self.limitations),
            "review_status": self.review_status,
            "requires_review": self.requires_review,
            "materialized": self.materialized,
            "execution_enabled": self.execution_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


@dataclass(frozen=True)
class SelfTodoItemCandidate:
    item_id: str
    title: str
    description: str
    item_type: str
    priority: Literal["low", "medium", "high"]
    source_refs: list[IntentionSourceRef]
    required_review: bool = True
    materialized: bool = False
    execution_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "item_id": self.item_id,
            "title": self.title,
            "description": self.description,
            "item_type": self.item_type,
            "priority": self.priority,
            "source_refs": [item.to_dict() for item in self.source_refs],
            "required_review": self.required_review,
            "materialized": self.materialized,
            "execution_enabled": self.execution_enabled,
        }


@dataclass(frozen=True)
class SelfTodoCandidate:
    candidate_id: str
    title: str
    source_refs: list[IntentionSourceRef]
    items: list[SelfTodoItemCandidate]
    confidence: Literal["low", "medium", "high"]
    risk_assessment: IntentionRiskAssessment
    limitations: list[str]
    review_status: str = "candidate_only"
    requires_review: bool = True
    materialized: bool = False
    execution_enabled: bool = False
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "title": self.title,
            "source_refs": [item.to_dict() for item in self.source_refs],
            "items": [item.to_dict() for item in self.items],
            "confidence": self.confidence,
            "risk_assessment": self.risk_assessment.to_dict(),
            "limitations": list(self.limitations),
            "review_status": self.review_status,
            "requires_review": self.requires_review,
            "materialized": self.materialized,
            "execution_enabled": self.execution_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


@dataclass(frozen=True)
class SelfNoActionCandidate:
    candidate_id: str
    reason: str
    source_refs: list[IntentionSourceRef]
    confidence: Literal["low", "medium", "high"]
    recommended_review_decision: str = "no_action"
    review_status: str = "candidate_only"
    execution_enabled: bool = False
    materialized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "reason": self.reason,
            "source_refs": [item.to_dict() for item in self.source_refs],
            "confidence": self.confidence,
            "recommended_review_decision": self.recommended_review_decision,
            "review_status": self.review_status,
            "execution_enabled": self.execution_enabled,
            "materialized": self.materialized,
        }


@dataclass(frozen=True)
class SelfNeedsMoreInputCandidate:
    candidate_id: str
    reason: str
    missing_inputs: list[str]
    source_refs: list[IntentionSourceRef]
    confidence: Literal["low", "medium", "high"]
    recommended_review_decision: str = "needs_more_input"
    review_status: str = "candidate_only"
    execution_enabled: bool = False
    materialized: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "reason": self.reason,
            "missing_inputs": list(self.missing_inputs),
            "source_refs": [item.to_dict() for item in self.source_refs],
            "confidence": self.confidence,
            "recommended_review_decision": self.recommended_review_decision,
            "review_status": self.review_status,
            "execution_enabled": self.execution_enabled,
            "materialized": self.materialized,
        }


@dataclass(frozen=True)
class SelfDirectedIntentionCandidateBundle:
    bundle_id: str
    request: SelfDirectedIntentionRequest
    source_refs: list[IntentionSourceRef]
    plan_candidates: list[SelfPlanCandidate]
    todo_candidates: list[SelfTodoCandidate]
    no_action_candidates: list[SelfNoActionCandidate]
    needs_more_input_candidates: list[SelfNeedsMoreInputCandidate]
    constraints: list[IntentionConstraint]
    evidence_refs: list[dict[str, Any]]
    limitations: list[str]
    review_status: str = "candidate_only"
    requires_review: bool = True
    materialized: bool = False
    execution_enabled: bool = False
    canonical_promotion_enabled: bool = False
    promoted: bool = False
    bundle_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "bundle_id": self.bundle_id,
            "request": self.request.to_dict(),
            "source_refs": [item.to_dict() for item in self.source_refs],
            "plan_candidates": [item.to_dict() for item in self.plan_candidates],
            "todo_candidates": [item.to_dict() for item in self.todo_candidates],
            "no_action_candidates": [item.to_dict() for item in self.no_action_candidates],
            "needs_more_input_candidates": [
                item.to_dict() for item in self.needs_more_input_candidates
            ],
            "constraints": [item.to_dict() for item in self.constraints],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "limitations": list(self.limitations),
            "review_status": self.review_status,
            "requires_review": self.requires_review,
            "materialized": self.materialized,
            "execution_enabled": self.execution_enabled,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
            "bundle_attrs": dict(self.bundle_attrs),
        }


class SelfDirectedIntentionPolicyService:
    def decide(self, request: SelfDirectedIntentionRequest) -> list[IntentionConstraint]:
        normalized = request.normalized()
        constraints = [
            _constraint("read_only_only", "Only read-only observation and candidate creation are allowed.", "hard_block"),
            _constraint("no_write", "Workspace write/edit/materialization is not allowed.", "hard_block"),
            _constraint("no_shell", "Shell, test, and lint execution are not allowed.", "hard_block"),
            _constraint("no_network", "Network and web fetch are not allowed.", "hard_block"),
            _constraint("no_mcp", "MCP connection is not allowed.", "hard_block"),
            _constraint("no_plugin", "Plugin loading is not allowed.", "hard_block"),
            _constraint("candidate_only", "Outputs remain candidate_only and require review.", "hard_block"),
        ]
        if normalized.target_scope != "self_awareness":
            constraints.append(
                _constraint("unsupported_scope", "Only self_awareness target scope is supported.", "warning")
            )
        return constraints


class IntentionSourceCollector:
    def collect(self, request: SelfDirectedIntentionRequest) -> list[IntentionSourceRef]:
        normalized = request.normalized()
        refs: list[IntentionSourceRef] = []
        if normalized.goal_text:
            refs.append(
                IntentionSourceRef(
                    ref_type="goal_text",
                    ref_id=f"directed_intention_goal:{uuid4()}",
                    source_kind="user_supplied_goal",
                    summary=_short_text(normalized.goal_text),
                    confidence="medium",
                    evidence_refs=[{"source": "goal_text", "target_scope": normalized.target_scope}],
                )
            )
        for candidate_id in normalized.source_candidate_ids:
            refs.append(
                IntentionSourceRef(
                    ref_type="source_candidate",
                    ref_id=candidate_id,
                    source_kind=_source_kind(candidate_id),
                    summary="Referenced self-awareness candidate id.",
                    confidence="high",
                    evidence_refs=[{"candidate_id": candidate_id}],
                )
            )
        for report_id in normalized.source_report_ids:
            refs.append(
                IntentionSourceRef(
                    ref_type="source_report",
                    ref_id=report_id,
                    source_kind="surface_verification_report",
                    summary="Referenced self-awareness verification report id.",
                    confidence="high",
                    evidence_refs=[{"report_id": report_id}],
                )
            )
        return refs


class PlanCandidateBuilder:
    def build(
        self,
        request: SelfDirectedIntentionRequest,
        source_refs: list[IntentionSourceRef],
        constraints: list[IntentionConstraint],
    ) -> list[SelfPlanCandidate]:
        if "plan" not in request.candidate_types or not source_refs:
            return []
        risk = _candidate_risk()
        steps = [
            _step("observe", "Review available self-awareness sources", "Inspect supplied source refs without executing actions.", "observe", None, source_refs, risk),
            _step("verify", "Verify candidate boundaries", "Check candidate-only, evidence, and read-only boundary status.", "verify", "skill:self_awareness_surface_verify", source_refs, risk),
            _step("review", "Human review of candidate direction", "A reviewer decides whether any future work should be requested.", "review", None, source_refs, risk),
            _blocked_step("future write remains blocked", "future_write_candidate", source_refs, risk),
            _blocked_step("future shell remains blocked", "future_shell_candidate", source_refs, risk),
            _blocked_step("future network remains blocked", "future_network_candidate", source_refs, risk),
            _blocked_step("future MCP remains blocked", "future_mcp_candidate", source_refs, risk),
            _blocked_step("future plugin remains blocked", "future_plugin_candidate", source_refs, risk),
        ][: request.max_plan_steps]
        return [
            SelfPlanCandidate(
                candidate_id=f"self_plan_candidate:{uuid4()}",
                title="Self-awareness next safe steps candidate",
                goal_text=request.goal_text,
                source_refs=source_refs,
                constraints=constraints,
                steps=steps,
                confidence=_confidence(source_refs),
                risk_assessment=risk,
                limitations=_limitations(),
            )
        ]


class TodoCandidateBuilder:
    def build(
        self,
        request: SelfDirectedIntentionRequest,
        source_refs: list[IntentionSourceRef],
        constraints: list[IntentionConstraint],
    ) -> list[SelfTodoCandidate]:
        if "todo" not in request.candidate_types or not source_refs:
            return []
        risk = _candidate_risk()
        base_items = [
            ("review_sources", "Review supplied self-awareness sources", "Confirm the source refs are sufficient and public-safe.", "review", "high"),
            ("verify_boundaries", "Verify candidate-only boundaries", "Check no execution, materialization, or promotion flags are enabled.", "verification", "high"),
            ("choose_no_action_or_next_request", "Choose review outcome", "Select no_action, needs_more_input, or request a future bounded implementation.", "review", "medium"),
        ]
        items = [
            SelfTodoItemCandidate(
                item_id=f"self_todo_item_candidate:{slug}:{uuid4()}",
                title=title,
                description=description,
                item_type=item_type,
                priority=priority,  # type: ignore[arg-type]
                source_refs=source_refs,
            )
            for slug, title, description, item_type, priority in base_items[: request.max_todo_items]
        ]
        return [
            SelfTodoCandidate(
                candidate_id=f"self_todo_candidate:{uuid4()}",
                title="Self-awareness review todo candidate",
                source_refs=source_refs,
                items=items,
                confidence=_confidence(source_refs),
                risk_assessment=risk,
                limitations=_limitations(),
            )
        ]


class NoActionCandidateBuilder:
    def build(
        self,
        request: SelfDirectedIntentionRequest,
        source_refs: list[IntentionSourceRef],
        constraints: list[IntentionConstraint],
    ) -> list[SelfNoActionCandidate]:
        if not request.include_no_action or "no_action" not in request.candidate_types:
            return []
        reason = (
            "No-action remains valid because self-directed intention candidates do not execute, materialize, or promote anything."
        )
        return [
            SelfNoActionCandidate(
                candidate_id=f"self_no_action_candidate:{uuid4()}",
                reason=reason,
                source_refs=source_refs,
                confidence="medium" if source_refs else "high",
            )
        ]


class NeedsMoreInputCandidateBuilder:
    def build(
        self,
        request: SelfDirectedIntentionRequest,
        source_refs: list[IntentionSourceRef],
        constraints: list[IntentionConstraint],
    ) -> list[SelfNeedsMoreInputCandidate]:
        if not request.include_needs_more_input or "needs_more_input" not in request.candidate_types:
            return []
        if source_refs and request.goal_text:
            return []
        missing: list[str] = []
        if not source_refs:
            missing.append("source_candidate_id_or_source_report_id")
        if not request.goal_text:
            missing.append("goal_text")
        return [
            SelfNeedsMoreInputCandidate(
                candidate_id=f"self_needs_more_input_candidate:{uuid4()}",
                reason="Insufficient verified self-awareness evidence for a stronger intention candidate.",
                missing_inputs=missing or ["review_decision"],
                source_refs=source_refs,
                confidence="high",
            )
        ]


class SelfDirectedIntentionService:
    def __init__(self) -> None:
        self.policy_service = SelfDirectedIntentionPolicyService()
        self.source_collector = IntentionSourceCollector()
        self.plan_builder = PlanCandidateBuilder()
        self.todo_builder = TodoCandidateBuilder()
        self.no_action_builder = NoActionCandidateBuilder()
        self.needs_more_input_builder = NeedsMoreInputCandidateBuilder()

    def create_candidates(
        self,
        request: SelfDirectedIntentionRequest,
    ) -> SelfDirectedIntentionCandidateBundle:
        normalized = request.normalized()
        constraints = self.policy_service.decide(normalized)
        source_refs = self.source_collector.collect(normalized)
        if not source_refs:
            constraints.append(
                _constraint(
                    "insufficient_evidence",
                    "No source candidate, source report, or goal text was supplied.",
                    "warning",
                )
            )
        plans = self.plan_builder.build(normalized, source_refs, constraints)
        todos = self.todo_builder.build(normalized, source_refs, constraints)
        no_actions = self.no_action_builder.build(normalized, source_refs, constraints)
        needs_input = self.needs_more_input_builder.build(normalized, source_refs, constraints)
        evidence_refs = _bundle_evidence_refs(source_refs, constraints)
        limitations = _limitations()
        if not source_refs:
            limitations.append("insufficient_source_evidence")
        blocked = not source_refs and not normalized.goal_text
        return SelfDirectedIntentionCandidateBundle(
            bundle_id=f"self_directed_intention_candidate_bundle:{uuid4()}",
            request=normalized,
            source_refs=source_refs,
            plan_candidates=plans,
            todo_candidates=todos,
            no_action_candidates=no_actions,
            needs_more_input_candidates=needs_input,
            constraints=constraints,
            evidence_refs=evidence_refs,
            limitations=limitations,
            bundle_attrs=_bundle_attrs(blocked=blocked),
        )


class SelfDirectedIntentionSkillService:
    def __init__(self) -> None:
        self.service = SelfDirectedIntentionService()

    def create_plan_candidate(self, request: SelfDirectedIntentionRequest) -> SelfDirectedIntentionCandidateBundle:
        return self.service.create_candidates(request)

    def create_todo_candidate(self, request: SelfDirectedIntentionRequest) -> SelfDirectedIntentionCandidateBundle:
        return self.service.create_candidates(request)


def _constraint(
    constraint_type: str,
    description: str,
    severity: Literal["info", "warning", "hard_block"],
    source_ref: dict[str, Any] | None = None,
) -> IntentionConstraint:
    return IntentionConstraint(
        constraint_type=constraint_type,
        description=description,
        severity=severity,
        source_ref=source_ref,
    )


def _candidate_risk() -> IntentionRiskAssessment:
    return IntentionRiskAssessment(
        risk_level="medium",
        risk_reasons=[
            "candidate_only_output",
            "requires_human_review_before_any_future_materialization",
        ],
        blocked_capabilities=list(BLOCKED_CAPABILITIES),
        required_review=True,
    )


def _step(
    slug: str,
    title: str,
    description: str,
    step_type: str,
    suggested_skill_id: str | None,
    source_refs: list[IntentionSourceRef],
    risk: IntentionRiskAssessment,
) -> SelfPlanStepCandidate:
    return SelfPlanStepCandidate(
        step_id=f"self_plan_step_candidate:{slug}:{uuid4()}",
        title=title,
        description=description,
        step_type=step_type,  # type: ignore[arg-type]
        suggested_skill_id=suggested_skill_id,
        required_evidence_refs=_source_evidence_refs(source_refs),
        expected_output="candidate-only review evidence",
        risk_assessment=risk,
    )


def _blocked_step(
    title: str,
    step_type: str,
    source_refs: list[IntentionSourceRef],
    risk: IntentionRiskAssessment,
) -> SelfPlanStepCandidate:
    return SelfPlanStepCandidate(
        step_id=f"self_plan_step_candidate:{step_type}:{uuid4()}",
        title=title,
        description="This future capability is recorded only as blocked and non-executable.",
        step_type=step_type,  # type: ignore[arg-type]
        suggested_skill_id=None,
        required_evidence_refs=_source_evidence_refs(source_refs),
        expected_output="blocked_future_candidate_only",
        risk_assessment=IntentionRiskAssessment(
            risk_level="blocked",
            risk_reasons=["blocked_future_capability"],
            blocked_capabilities=list(BLOCKED_CAPABILITIES),
            required_review=True,
        ),
    )


def _source_evidence_refs(source_refs: list[IntentionSourceRef]) -> list[dict[str, Any]]:
    refs: list[dict[str, Any]] = []
    for source in source_refs:
        refs.append({"ref_type": source.ref_type, "ref_id": source.ref_id})
    return refs


def _bundle_evidence_refs(
    source_refs: list[IntentionSourceRef],
    constraints: list[IntentionConstraint],
) -> list[dict[str, Any]]:
    refs = _source_evidence_refs(source_refs)
    refs.extend({"constraint_type": item.constraint_type, "severity": item.severity} for item in constraints)
    return refs or [{"evidence_status": "insufficient"}]


def _limitations() -> list[str]:
    return [
        "candidate_generation_only",
        "no_execution",
        "no_materialization",
        "no_task_queue_creation",
        "no_todo_file_write",
        "no_memory_persona_overlay_mutation",
        "no_llm_planner",
    ]


def _bundle_attrs(*, blocked: bool) -> dict[str, Any]:
    return {
        "effect_types": list(INTENTION_CANDIDATE_EFFECTS),
        "read_only": True,
        "state_candidate_created": True,
        "deterministic_rules_used": True,
        "llm_planner_used": False,
        "actual_execution_occurred": False,
        "todo_file_written": False,
        "task_queue_entry_created": False,
        "canonical_promotion_enabled": False,
        "promoted": False,
        "materialized": False,
        "execution_enabled": False,
        "blocked": blocked,
        "workspace_write_used": False,
        "shell_execution_used": False,
        "network_access_used": False,
        "mcp_connection_used": False,
        "plugin_loading_used": False,
        "external_harness_execution_used": False,
        "memory_mutation_used": False,
        "persona_mutation_used": False,
        "overlay_mutation_used": False,
    }


def _confidence(source_refs: list[IntentionSourceRef]) -> Literal["low", "medium", "high"]:
    if any(item.confidence == "high" for item in source_refs):
        return "medium"
    return "low"


def _source_kind(ref_id: str) -> str:
    lowered = ref_id.casefold()
    if "project_structure" in lowered:
        return "project_structure_candidate"
    if "summary" in lowered:
        return "summary_candidate"
    if "search" in lowered:
        return "search_result"
    return "self_awareness_candidate"


def _short_text(value: str, *, limit: int = 200) -> str:
    text = " ".join(value.split())
    return text[:limit]
