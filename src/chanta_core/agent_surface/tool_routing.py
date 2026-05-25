from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any

from chanta_core.agent_surface.contract import AgentSurfaceContractReportService
from chanta_core.agent_surface.intent_task import (
    AgentIntentClassificationReport,
    AgentIntentClassificationReportService,
    AgentTaskFrame,
)
from chanta_core.agent_surface.safety_gate import (
    AgentGateOutcomeEnvelope,
    AgentSafetyGateReport,
    AgentSafetyGateReportService,
)
from chanta_core.agent_surface.turn_context import AgentTurnReportService
from chanta_core.utility.time import utc_now_iso


AGENT_TOOL_ROUTING_VERSION = "v0.25.4"
AGENT_TOOL_ROUTING_VERSION_NAME = "Tool Routing Plan & Provider Selection"
AGENT_TOOL_ROUTING_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP = "v0.25.5 Internal Provider Invocation Orchestrator"
AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP = "v0.25.6 Response Assembly & Evidence Binder"

AGENT_TOOL_ROUTING_OBJECT_TYPES = [
    "agent_tool_routing_policy",
    "agent_tool_routing_request",
    "agent_provider_capability_catalog_view",
    "agent_provider_capability_ref",
    "agent_route_intent_mapping",
    "agent_provider_selection_candidate",
    "agent_provider_selection",
    "agent_route_precondition",
    "agent_tool_route_step",
    "agent_tool_route_dependency",
    "agent_route_risk_review",
    "agent_tool_route_plan",
    "agent_tool_routing_finding",
    "agent_tool_routing_report",
    "agent_safety_gate_report",
    "agent_gate_outcome_envelope",
    "agent_intent_classification_report",
    "agent_task_frame",
    "agent_turn_envelope",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_TOOL_ROUTING_EVENT_TYPES = [
    "agent_tool_routing_requested",
    "agent_tool_routing_policy_created",
    "agent_provider_capability_catalog_view_created",
    "agent_route_intent_mapping_created",
    "agent_provider_selection_candidate_created",
    "agent_provider_selection_created",
    "agent_route_precondition_created",
    "agent_tool_route_step_created",
    "agent_tool_route_dependency_created",
    "agent_route_risk_review_created",
    "agent_tool_route_plan_created",
    "agent_tool_routing_report_created",
    "agent_tool_routing_warning_created",
    "agent_tool_routing_blocked",
]

AGENT_TOOL_ROUTING_RELATION_TYPES = [
    "uses_agent_safety_gate_report",
    "uses_agent_gate_outcome_envelope",
    "uses_agent_intent_classification_report",
    "uses_agent_task_frame",
    "uses_internal_provider_registry",
    "views_provider_capability_catalog",
    "maps_intent_to_route_kind",
    "creates_provider_selection_candidate",
    "creates_provider_selection",
    "creates_route_precondition",
    "creates_tool_route_step",
    "creates_tool_route_dependency",
    "reviews_route_risk",
    "creates_tool_route_plan",
    "prepares_provider_invocation",
    "defers_provider_invocation_to_v0_25_5",
    "defers_response_assembly_to_v0_25_6",
    "defers_ask_repl_to_v0_25_7",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "enforces_read_only_before_execution",
    "enforces_search_before_file_read",
    "enforces_candidate_before_safety",
    "enforces_safety_before_execution",
    "enforces_execution_before_output_explanation",
    "not_tool_route_executed",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "derived_from_agent_safety_gate",
    "recorded_in_envelope",
]

AGENT_TOOL_ROUTING_EFFECT_TYPES = [
    "read_only_observation",
    "agent_tool_route_plan_created",
    "agent_provider_selection_created",
    "agent_route_risk_review_created",
    "state_candidate_created",
]

AGENT_TOOL_ROUTING_FORBIDDEN_EFFECT_TYPES = [
    "tool_route_executed",
    "agent_provider_invocation_requested",
    "provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "agent_ask_executed",
    "agent_repl_started",
    "agent_response_assembled",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "credential_exposed",
    "raw_secret_output",
    "schumpeter_split_introduced",
]

RESPONSE_ONLY_ROUTE_KINDS = {"response_only", "no_route"}
PROVIDER_ROUTE_KINDS = {
    "workspace_read",
    "repository_search",
    "file_read",
    "process_state_inspection",
    "local_runtime_candidate",
    "local_runtime_execution_flow",
    "diagnostic_flow",
    "prompt_generation_flow",
    "verification_flow",
    "checklist_flow",
    "consolidation_flow",
}


def _safe_id(text: str | None) -> str:
    value = text or "unknown"
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "-", value.strip().lower())[:120] or "unknown"


@dataclass
class AgentToolRoutingPolicy:
    policy_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    layer: str = "agent_surface"
    deterministic_default: bool = True
    external_llm_routing_enabled: bool = False
    llm_routing_judge_enabled: bool = False
    require_safety_gate_allow_route: bool = True
    create_route_plan_enabled: bool = True
    provider_selection_enabled: bool = True
    route_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    provider_execution_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    ask_execution_enabled: bool = False
    repl_execution_enabled: bool = False
    response_assembly_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_provider_adapter_enabled: bool = False
    external_agent_adapter_enabled: bool = False
    respect_v024_provider_boundaries: bool = True
    respect_v024_local_runtime_gate: bool = True
    read_only_before_execution: bool = True
    search_before_file_read: bool = True
    command_candidate_before_safety: bool = True
    safety_before_execution: bool = True
    execution_before_output_explanation: bool = True
    evidence_refs_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentToolRoutingRequest:
    request_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    safety_gate_report_id: str | None = None
    gate_outcome_envelope_id: str | None = None
    intent_report_id: str | None = None
    task_frame_id: str | None = None
    turn_envelope_id: str | None = None
    sanitized_request_text: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderCapabilityRef:
    capability_ref_id: str
    provider_id: str
    provider_type: str
    capability_id: str
    capability_name: str
    source_version: str | None
    read_only: bool
    bounded_execution_capable: bool
    requires_safety_gate: bool
    requires_v024_gate: bool
    invocation_enabled_in_v025_4: bool = False
    executable_in_v025_4: bool = False
    allowed_for_route_plan: bool = True
    external_adapter: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderCapabilityCatalogView:
    catalog_view_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    source_registry_ref: dict[str, Any] | None = None
    provider_capabilities: list[AgentProviderCapabilityRef] = field(default_factory=list)
    provider_count: int = 0
    capability_count: int = 0
    catalog_status: str = "ready"
    external_provider_adapter_count: int = 0
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentRouteIntentMapping:
    mapping_id: str
    intent_category: str
    recommended_route_kind: str
    required_provider_types: list[str]
    optional_provider_types: list[str]
    route_constraints: list[str]
    next_stage: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderSelectionCandidate:
    selection_candidate_id: str
    provider_ref: AgentProviderCapabilityRef
    route_kind: str
    reason: str
    priority: int
    required: bool
    preconditions: list[str]
    expected_output_ref_type: str
    risk_notes: list[str]
    selected: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderSelection:
    selection_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    selected_candidates: list[AgentProviderSelectionCandidate] = field(default_factory=list)
    rejected_candidates: list[AgentProviderSelectionCandidate] = field(default_factory=list)
    provider_count: int = 0
    required_provider_count: int = 0
    selection_status: str = "selected"
    provider_invoked: bool = False
    route_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentRoutePrecondition:
    precondition_id: str
    precondition_type: str
    description: str
    required: bool
    satisfied_now: bool
    required_future_stage: str | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentToolRouteStep:
    route_step_id: str
    step_index: int
    step_name: str
    route_kind: str
    provider_id: str | None
    provider_type: str | None
    capability_id: str | None
    planned_action: str
    expected_input_refs: list[dict[str, Any]]
    expected_output_ref_type: str
    preconditions: list[AgentRoutePrecondition]
    route_step_status: str
    executes_now: bool = False
    provider_invoked_now: bool = False
    local_command_executed_now: bool = False
    mutates_state_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentToolRouteDependency:
    dependency_id: str
    upstream_step_id: str
    downstream_step_id: str
    dependency_type: str
    required: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentRouteRiskReview:
    risk_review_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    route_kind: str = "unknown"
    risk_level: str = "unknown"
    risk_categories: list[str] = field(default_factory=list)
    requires_v024_gate: bool = False
    requires_v0255_invocation_boundary: bool = True
    blocks_route_plan: bool = False
    rationale: str = ""
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentToolRoutePlan:
    route_plan_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    created_at: str = ""
    safety_gate_report_id: str = ""
    intent_report_id: str | None = None
    task_frame_id: str | None = None
    primary_intent_category: str = "unknown"
    route_kind: str = "unknown"
    provider_selection: AgentProviderSelection | None = None
    route_steps: list[AgentToolRouteStep] = field(default_factory=list)
    route_dependencies: list[AgentToolRouteDependency] = field(default_factory=list)
    risk_review: AgentRouteRiskReview | None = None
    expected_next_stage: str = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
    route_plan_status: str = "failed"
    provider_invocation_required: bool = False
    provider_invocation_allowed_now: bool = False
    route_execution_allowed_now: bool = False
    local_runtime_execution_allowed_now: bool = False
    tool_route_created: bool = True
    tool_route_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentToolRoutingFinding:
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
class AgentToolRoutingReport:
    report_id: str
    version: str = AGENT_TOOL_ROUTING_VERSION
    created_at: str = ""
    policy: AgentToolRoutingPolicy | None = None
    request: AgentToolRoutingRequest | None = None
    capability_catalog_view: AgentProviderCapabilityCatalogView | None = None
    route_mappings: list[AgentRouteIntentMapping] = field(default_factory=list)
    route_plan: AgentToolRoutePlan | None = None
    findings: list[AgentToolRoutingFinding] = field(default_factory=list)
    report_status: str = "failed"
    ready_for_v0_25_5: bool = False
    ready_for_v0_25_6: bool = False
    ready_for_v0_26: bool = False
    safety_gate_was_allow_route: bool = False
    tool_route_plan_created: bool = False
    provider_selection_created: bool = False
    tool_route_executed: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    response_assembled: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.5 provider invocation begins or routing/provider policy changes."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentToolRoutingPrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        return AgentSurfaceContractReportService().build_report().to_dict()

    def load_safety_gate_report(self) -> AgentSafetyGateReport:
        return AgentSafetyGateReportService().build_report()

    def load_gate_outcome_envelope(self) -> AgentGateOutcomeEnvelope:
        return self.load_safety_gate_report().outcome_envelope

    def load_intent_report(self) -> AgentIntentClassificationReport:
        return AgentIntentClassificationReportService().build_report()

    def load_task_frame(self) -> AgentTaskFrame:
        return self.load_intent_report().task_frame

    def load_internal_provider_registry(self) -> dict[str, Any]:
        return {"status": "available", "version": "v0.24.9", "invoked": False}

    def load_internal_provider_capability_surface(self) -> dict[str, Any]:
        return {"status": "available", "source": "v0.24 internal provider foundation", "invoked": False}

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return {
            "skill:agent_tool_route_plan_create": "implemented",
            "skill:agent_provider_selection_create": "implemented",
            "skill:agent_provider_invocation_orchestrate": "contract_only",
            "skill:agent_response_assemble": "contract_only",
            "skill:agent_ask": "contract_only",
            "skill:agent_repl": "contract_only",
        }


class AgentToolRoutingPolicyService:
    def build_policy(self) -> AgentToolRoutingPolicy:
        return AgentToolRoutingPolicy(
            policy_id="agent_tool_routing_policy:v0.25.4",
            evidence_refs=[
                {"type": "version", "value": AGENT_TOOL_ROUTING_VERSION},
                {"type": "track", "value": AGENT_TOOL_ROUTING_TRACK},
            ],
        )


class AgentProviderCapabilityCatalogService:
    def build_catalog_view(self) -> AgentProviderCapabilityCatalogView:
        refs = [
            self._ref("workspace_read_provider", "workspace_tree", "Workspace Tree / Metadata Read", True, False),
            self._ref("repository_search_provider", "repository_search", "Bounded Repository Search", True, False),
            self._ref("file_read_provider", "file_read", "Bounded Sanitized File Read", True, False),
            self._ref("ocel_inspection_provider", "ocel_inspection", "OCEL Inspection", True, False),
            self._ref("pig_inspection_provider", "pig_inspection", "PIG Inspection", True, False),
            self._ref("ocpx_projection_provider", "ocpx_projection", "OCPX Projection", True, False),
            self._ref("local_runtime_provider", "local_runtime_candidate", "Local Runtime Command Candidate", False, True),
            self._ref("diagnostic_provider", "diagnostic", "Diagnostic Provider Planning", True, False),
            self._ref("candidate_generation_provider", "candidate_generation", "Candidate Generation Planning", True, False),
        ]
        provider_ids = {item.provider_id for item in refs}
        return AgentProviderCapabilityCatalogView(
            catalog_view_id="agent_provider_capability_catalog_view:v0.25.4",
            source_registry_ref={"type": "internal_provider_registry", "version": "v0.24.9"},
            provider_capabilities=refs,
            provider_count=len(provider_ids),
            capability_count=len(refs),
            catalog_status="ready",
            external_provider_adapter_count=0,
            evidence_refs=[{"type": "catalog_source", "value": "v0.24 internal provider foundation"}],
        )

    def _ref(
        self,
        provider_type: str,
        capability_id: str,
        capability_name: str,
        read_only: bool,
        requires_v024_gate: bool,
    ) -> AgentProviderCapabilityRef:
        return AgentProviderCapabilityRef(
            capability_ref_id=f"agent_provider_capability_ref:{provider_type}:{capability_id}",
            provider_id=f"internal_provider:{provider_type}",
            provider_type=provider_type,
            capability_id=capability_id,
            capability_name=capability_name,
            source_version="v0.24.9",
            read_only=read_only,
            bounded_execution_capable=requires_v024_gate,
            requires_safety_gate=True,
            requires_v024_gate=requires_v024_gate,
            allowed_for_route_plan=True,
            evidence_refs=[{"type": "invocation_enabled_in_v025_4", "value": False}],
        )


class AgentRouteIntentMappingService:
    ROUTE_MAPPINGS: dict[str, tuple[str, list[str], list[str], list[str]]] = {
        "general_answer": ("response_only", [], [], ["response_assembly_deferred"]),
        "workspace_overview": ("workspace_read", ["workspace_read_provider"], [], ["read_only_before_execution"]),
        "repository_search": ("repository_search", ["repository_search_provider"], [], ["read_only_before_execution"]),
        "file_read": ("file_read", ["repository_search_provider", "file_read_provider"], [], ["search_before_file_read"]),
        "process_state_inspection": ("process_state_inspection", ["ocel_inspection_provider"], ["pig_inspection_provider", "ocpx_projection_provider"], ["read_only_before_execution"]),
        "local_runtime_candidate": ("local_runtime_candidate", ["local_runtime_provider"], [], ["command_candidate_before_safety"]),
        "local_runtime_execution_request": ("local_runtime_execution_flow", ["local_runtime_provider"], [], ["candidate_before_safety", "safety_before_execution", "execution_before_output_explanation"]),
        "diagnostic_request": ("diagnostic_flow", ["diagnostic_provider"], ["ocel_inspection_provider"], ["read_only_before_execution"]),
        "explanation_request": ("response_only", [], ["workspace_read_provider"], ["response_assembly_deferred"]),
        "planning_request": ("response_only", [], ["repository_search_provider"], ["response_assembly_deferred"]),
        "architecture_design": ("response_only", [], ["repository_search_provider", "ocel_inspection_provider"], ["response_assembly_deferred"]),
        "implementation_prompt_request": ("prompt_generation_flow", ["candidate_generation_provider"], [], ["provider_invocation_deferred"]),
        "verification_prompt_request": ("verification_flow", ["candidate_generation_provider"], ["repository_search_provider"], ["provider_invocation_deferred"]),
        "checklist_request": ("checklist_flow", ["candidate_generation_provider"], [], ["provider_invocation_deferred"]),
        "consolidation_request": ("consolidation_flow", ["candidate_generation_provider"], ["ocel_inspection_provider"], ["provider_invocation_deferred"]),
        "no_action_candidate": ("no_route", [], [], ["non_route_gate_outcome"]),
        "needs_more_input_candidate": ("no_route", [], [], ["non_route_gate_outcome"]),
        "blocked_candidate": ("no_route", [], [], ["non_route_gate_outcome"]),
        "unknown": ("no_route", [], [], ["unknown_route_kind"]),
    }

    def build_route_mappings(self) -> list[AgentRouteIntentMapping]:
        return [
            AgentRouteIntentMapping(
                mapping_id=f"agent_route_intent_mapping:{intent_category}",
                intent_category=intent_category,
                recommended_route_kind=route_kind,
                required_provider_types=required,
                optional_provider_types=optional,
                route_constraints=constraints,
                next_stage=AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP if route_kind in RESPONSE_ONLY_ROUTE_KINDS else AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP,
                evidence_refs=[{"type": "deterministic_mapping", "intent_category": intent_category}],
            )
            for intent_category, (route_kind, required, optional, constraints) in self.ROUTE_MAPPINGS.items()
        ]

    def map_intent_to_route_kind(self, intent_category: str) -> AgentRouteIntentMapping:
        mappings = {mapping.intent_category: mapping for mapping in self.build_route_mappings()}
        return mappings.get(intent_category, mappings["unknown"])


class AgentProviderSelectionCandidateService:
    def build_selection_candidates(
        self,
        mapping: AgentRouteIntentMapping,
        catalog: AgentProviderCapabilityCatalogView,
    ) -> list[AgentProviderSelectionCandidate]:
        candidates: list[AgentProviderSelectionCandidate] = []
        provider_types = mapping.required_provider_types + mapping.optional_provider_types
        for provider_type in provider_types:
            provider_ref = next((item for item in catalog.provider_capabilities if item.provider_type == provider_type), None)
            if provider_ref is None:
                continue
            required = provider_type in mapping.required_provider_types
            selected = provider_ref.allowed_for_route_plan and required
            candidates.append(
                AgentProviderSelectionCandidate(
                    selection_candidate_id=f"agent_provider_selection_candidate:{mapping.recommended_route_kind}:{provider_type}",
                    provider_ref=provider_ref,
                    route_kind=mapping.recommended_route_kind,
                    reason="Required provider for deterministic route mapping." if required else "Optional provider retained as rejected candidate.",
                    priority=provider_types.index(provider_type) + 1,
                    required=required,
                    preconditions=mapping.route_constraints,
                    expected_output_ref_type=self._expected_output_ref_type(provider_type),
                    risk_notes=["requires_v024_gate"] if provider_ref.requires_v024_gate else [],
                    selected=selected,
                    evidence_refs=[{"type": "provider_invoked", "value": False}],
                )
            )
        return candidates

    def _expected_output_ref_type(self, provider_type: str) -> str:
        return {
            "workspace_read_provider": "workspace_snapshot_ref",
            "repository_search_provider": "repository_search_result_ref",
            "file_read_provider": "file_excerpt_ref",
            "ocel_inspection_provider": "ocel_inspection_ref",
            "pig_inspection_provider": "pig_report_ref",
            "ocpx_projection_provider": "ocpx_projection_ref",
            "local_runtime_provider": "local_runtime_candidate_ref",
            "diagnostic_provider": "diagnostic_report_ref",
            "candidate_generation_provider": "agent_candidate_ref",
        }.get(provider_type, "unknown")


class AgentProviderSelectionService:
    def select_providers(
        self,
        mapping: AgentRouteIntentMapping,
        candidates: list[AgentProviderSelectionCandidate],
    ) -> AgentProviderSelection:
        selected = [candidate for candidate in candidates if candidate.selected]
        rejected = [candidate for candidate in candidates if not candidate.selected]
        if mapping.recommended_route_kind in RESPONSE_ONLY_ROUTE_KINDS:
            status = "no_route"
        elif len(selected) >= len(mapping.required_provider_types):
            status = "selected"
        elif candidates:
            status = "warning"
        else:
            status = "failed"
        return AgentProviderSelection(
            selection_id=f"agent_provider_selection:{mapping.recommended_route_kind}",
            selected_candidates=selected,
            rejected_candidates=rejected,
            provider_count=len(selected),
            required_provider_count=len(mapping.required_provider_types),
            selection_status=status,
            evidence_refs=[{"type": "provider_invoked", "value": False}],
        )


class AgentRoutePreconditionService:
    def build_preconditions(
        self,
        route_kind: str,
        provider_ref: AgentProviderCapabilityRef | None,
        gate_allow_route: bool,
    ) -> list[AgentRoutePrecondition]:
        preconditions = [
            self._precondition("gate_allow_route", "v0.25.3 gate outcome must be allow_route.", True, gate_allow_route, None),
            self._precondition("evidence_required", "Route plan must retain evidence refs.", True, True, None),
        ]
        if provider_ref is not None:
            preconditions.append(self._precondition("provider_available", "Selected provider capability must exist.", True, True, None))
            preconditions.append(self._precondition("capability_available", "Selected capability must exist.", True, True, None))
        if route_kind == "file_read":
            preconditions.append(self._precondition("repository_context_available", "Repository search context should precede file read.", True, False, AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP))
        if route_kind in {"local_runtime_candidate", "local_runtime_execution_flow"}:
            preconditions.append(self._precondition("local_runtime_candidate_required", "Local runtime command candidate must be created before safety.", True, False, "v0.24.5 Local Runtime Command Candidate"))
            preconditions.append(self._precondition("static_safety_required", "Static safety/preflight must run before execution.", True, False, "v0.24.6 Static Safety / Preflight"))
            preconditions.append(self._precondition("execution_gate_required", "Execution gate must authorize before execution.", True, False, "v0.24.7 Gated Local Runtime Execution"))
            preconditions.append(self._precondition("output_explanation_required", "Output/failure explanation must follow execution.", True, False, "v0.24.8 Output Failure Explanation"))
        return preconditions

    def _precondition(
        self,
        precondition_type: str,
        description: str,
        required: bool,
        satisfied_now: bool,
        required_future_stage: str | None,
    ) -> AgentRoutePrecondition:
        return AgentRoutePrecondition(
            precondition_id=f"agent_route_precondition:{precondition_type}",
            precondition_type=precondition_type,
            description=description,
            required=required,
            satisfied_now=satisfied_now,
            required_future_stage=required_future_stage,
            evidence_refs=[{"type": "precondition", "value": precondition_type}],
        )


class AgentToolRouteStepService:
    def build_steps(
        self,
        mapping: AgentRouteIntentMapping,
        selection: AgentProviderSelection,
        gate_allow_route: bool,
    ) -> list[AgentToolRouteStep]:
        if mapping.recommended_route_kind == "no_route":
            return [
                self._step(1, "No executable route due to gate outcome", mapping.recommended_route_kind, None, gate_allow_route, "no_route")
            ]
        if mapping.recommended_route_kind == "response_only":
            return [
                self._step(1, "Response-only route for v0.25.6", mapping.recommended_route_kind, None, gate_allow_route, "planned")
            ]
        steps: list[AgentToolRouteStep] = []
        for index, candidate in enumerate(selection.selected_candidates, start=1):
            steps.append(
                self._step(
                    index,
                    candidate.provider_ref.capability_name,
                    mapping.recommended_route_kind,
                    candidate.provider_ref,
                    gate_allow_route,
                    "planned",
                )
            )
        return steps or [
            self._step(1, "Provider capability unavailable", mapping.recommended_route_kind, None, gate_allow_route, "failed")
        ]

    def _step(
        self,
        index: int,
        name: str,
        route_kind: str,
        provider_ref: AgentProviderCapabilityRef | None,
        gate_allow_route: bool,
        status: str,
    ) -> AgentToolRouteStep:
        preconditions = AgentRoutePreconditionService().build_preconditions(route_kind, provider_ref, gate_allow_route)
        return AgentToolRouteStep(
            route_step_id=f"agent_tool_route_step:{route_kind}:{index}",
            step_index=index,
            step_name=name,
            route_kind=route_kind,
            provider_id=provider_ref.provider_id if provider_ref else None,
            provider_type=provider_ref.provider_type if provider_ref else None,
            capability_id=provider_ref.capability_id if provider_ref else None,
            planned_action="Plan provider invocation for v0.25.5 only." if provider_ref else "No provider invocation planned now.",
            expected_input_refs=[{"type": "agent_safety_gate_report"}],
            expected_output_ref_type="response_assembly_ref" if provider_ref is None else f"{provider_ref.capability_id}_ref",
            preconditions=preconditions,
            route_step_status=status,
            evidence_refs=[{"type": "executes_now", "value": False}],
        )


class AgentToolRouteDependencyService:
    def build_dependencies(self, route_kind: str, steps: list[AgentToolRouteStep]) -> list[AgentToolRouteDependency]:
        dependencies: list[AgentToolRouteDependency] = []
        if route_kind == "file_read" and len(steps) >= 2:
            dependencies.append(self._dependency(steps[0], steps[1], "search_before_file_read"))
        if route_kind == "local_runtime_execution_flow":
            dependencies.extend(
                [
                    AgentToolRouteDependency(
                        dependency_id="agent_tool_route_dependency:candidate_before_safety",
                        upstream_step_id=steps[0].route_step_id if steps else "local_runtime_candidate",
                        downstream_step_id="v0.24.6_static_safety",
                        dependency_type="candidate_before_safety",
                        required=True,
                        evidence_refs=[{"type": "v024_gate_sequence", "value": True}],
                    ),
                    AgentToolRouteDependency(
                        dependency_id="agent_tool_route_dependency:safety_before_execution",
                        upstream_step_id="v0.24.6_static_safety",
                        downstream_step_id="v0.24.7_execution_gate",
                        dependency_type="safety_before_execution",
                        required=True,
                        evidence_refs=[{"type": "v024_gate_sequence", "value": True}],
                    ),
                    AgentToolRouteDependency(
                        dependency_id="agent_tool_route_dependency:execution_before_explanation",
                        upstream_step_id="v0.24.7_execution_gate",
                        downstream_step_id="v0.24.8_output_explanation",
                        dependency_type="execution_before_explanation",
                        required=True,
                        evidence_refs=[{"type": "v024_gate_sequence", "value": True}],
                    ),
                ]
            )
        for upstream, downstream in zip(steps, steps[1:]):
            if not any(item.upstream_step_id == upstream.route_step_id and item.downstream_step_id == downstream.route_step_id for item in dependencies):
                dependencies.append(self._dependency(upstream, downstream, "output_to_input"))
        return dependencies

    def _dependency(
        self,
        upstream: AgentToolRouteStep,
        downstream: AgentToolRouteStep,
        dependency_type: str,
    ) -> AgentToolRouteDependency:
        return AgentToolRouteDependency(
            dependency_id=f"agent_tool_route_dependency:{dependency_type}:{_safe_id(upstream.route_step_id)}:{_safe_id(downstream.route_step_id)}",
            upstream_step_id=upstream.route_step_id,
            downstream_step_id=downstream.route_step_id,
            dependency_type=dependency_type,
            required=True,
            evidence_refs=[{"type": "dependency", "value": dependency_type}],
        )


class AgentRouteRiskReviewService:
    def build_risk_review(
        self,
        mapping: AgentRouteIntentMapping,
        task_frame: AgentTaskFrame,
        gate_allow_route: bool,
    ) -> AgentRouteRiskReview:
        categories = set(task_frame.risk_preview.risk_categories)
        route_kind = mapping.recommended_route_kind
        if route_kind in {"repository_search", "file_read", "workspace_read"}:
            categories.add("file_read" if route_kind == "file_read" else "provider_boundary")
        if route_kind == "process_state_inspection":
            categories.add("process_state_inspection")
        if route_kind == "local_runtime_execution_flow":
            categories.update({"local_runtime_execution", "provider_boundary"})
        if not gate_allow_route:
            categories.add("out_of_scope_track")
        blocked_categories = {"credential_exposure", "raw_secret_output", "external_adapter", "memory_mutation"}
        blocks = bool(categories & blocked_categories)
        if blocks:
            risk_level = "blocked"
        elif "local_runtime_execution" in categories:
            risk_level = "high"
        elif categories:
            risk_level = "medium" if "provider_boundary" in categories or "out_of_scope_track" in categories else "low"
        else:
            risk_level = "none"
        return AgentRouteRiskReview(
            risk_review_id=f"agent_route_risk_review:{route_kind}",
            route_kind=route_kind,
            risk_level=risk_level,
            risk_categories=sorted(categories),
            requires_v024_gate=route_kind in {"local_runtime_candidate", "local_runtime_execution_flow"},
            requires_v0255_invocation_boundary=route_kind not in RESPONSE_ONLY_ROUTE_KINDS,
            blocks_route_plan=blocks,
            rationale="Risk review is planning-only and does not invoke providers or execute route steps.",
            evidence_refs=[{"type": "gate_allow_route", "value": gate_allow_route}],
        )


class AgentToolRoutePlanService:
    def build_route_plan(
        self,
        request: AgentToolRoutingRequest,
        safety_gate_report: AgentSafetyGateReport,
        intent_report: AgentIntentClassificationReport,
        mapping: AgentRouteIntentMapping,
        selection: AgentProviderSelection,
        steps: list[AgentToolRouteStep],
        dependencies: list[AgentToolRouteDependency],
        risk_review: AgentRouteRiskReview,
    ) -> AgentToolRoutePlan:
        gate_allow_route = safety_gate_report.allow_route
        if not gate_allow_route:
            route_kind = "no_route"
            status = "no_route_due_to_gate"
            provider_required = False
            next_stage = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
        else:
            route_kind = mapping.recommended_route_kind
            provider_required = bool(selection.selected_candidates) and route_kind not in RESPONSE_ONLY_ROUTE_KINDS
            if route_kind == "response_only":
                status = "response_only"
                next_stage = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
            elif risk_review.blocks_route_plan:
                status = "blocked"
                next_stage = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
                provider_required = False
            elif route_kind == "no_route":
                status = "no_route_due_to_gate"
                next_stage = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
                provider_required = False
            elif selection.selection_status in {"selected", "warning"}:
                status = "planned"
                next_stage = AGENT_TOOL_ROUTING_INVOCATION_NEXT_STEP
            else:
                status = "failed"
                next_stage = AGENT_TOOL_ROUTING_RESPONSE_NEXT_STEP
                provider_required = False
        return AgentToolRoutePlan(
            route_plan_id=f"agent_tool_route_plan:{_safe_id(request.request_id)}",
            created_at=utc_now_iso(),
            safety_gate_report_id=safety_gate_report.report_id,
            intent_report_id=intent_report.report_id,
            task_frame_id=intent_report.task_frame.task_frame_id,
            primary_intent_category=intent_report.intent_descriptor.primary_category,
            route_kind=route_kind,
            provider_selection=selection,
            route_steps=steps,
            route_dependencies=dependencies,
            risk_review=risk_review,
            expected_next_stage=next_stage,
            route_plan_status=status,
            provider_invocation_required=provider_required,
            evidence_refs=[{"type": "provider_invocation_allowed_now", "value": False}],
        )


class AgentToolRoutingFindingService:
    BLOCKED_ATTEMPTS = {
        "route_execution_attempted",
        "provider_invocation_attempted",
        "local_command_execution_attempted",
        "ask_execution_attempted_too_early",
        "repl_execution_attempted_too_early",
        "response_assembly_attempted_too_early",
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
        request: AgentToolRoutingRequest,
        catalog: AgentProviderCapabilityCatalogView,
        mapping: AgentRouteIntentMapping,
        route_plan: AgentToolRoutePlan,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentToolRoutingFinding]:
        subject_id = route_plan.route_plan_id
        findings = [self._finding("info", "ok", "Tool route plan and provider selection were created without execution.", subject_id)]
        if not request.safety_gate_report_id:
            findings.append(self._finding("error", "missing_safety_gate_report", "Safety gate report is missing.", request.request_id))
        if route_plan.route_plan_status == "no_route_due_to_gate":
            findings.append(self._finding("warning", "missing_allow_route", "Safety gate did not allow route.", subject_id))
            findings.append(self._finding("warning", "non_route_gate_outcome", "Non-route gate outcome must go to response assembly.", subject_id))
            findings.append(self._finding("warning", "no_route_due_to_gate", "No executable provider route was created.", subject_id))
        if not request.intent_report_id:
            findings.append(self._finding("error", "missing_intent_report", "Intent report reference is missing.", request.request_id))
        if not request.task_frame_id:
            findings.append(self._finding("error", "missing_task_frame", "Task frame reference is missing.", request.request_id))
        if catalog.catalog_status in {"missing", "blocked"}:
            findings.append(self._finding("error", "missing_provider_registry", "Provider registry is unavailable.", catalog.catalog_view_id))
            findings.append(self._finding("error", "missing_provider_capability_catalog", "Provider capability catalog is unavailable.", catalog.catalog_view_id))
        if mapping.recommended_route_kind == "unknown":
            findings.append(self._finding("warning", "unknown_route_kind", "Unknown route kind selected.", subject_id))
            findings.append(self._finding("warning", "no_route_mapping", "No deterministic route mapping exists.", subject_id))
        if route_plan.provider_invocation_required and not route_plan.provider_selection.selected_candidates:
            findings.append(self._finding("error", "required_provider_unavailable", "Required provider is unavailable.", subject_id))
            findings.append(self._finding("error", "provider_capability_missing", "Provider capability is missing.", subject_id))
        if route_plan.route_kind == "response_only":
            findings.append(self._finding("warning", "response_only_route", "Response-only route must go to v0.25.6.", subject_id))
        if route_plan.route_plan_status in {"planned", "response_only"}:
            findings.append(self._finding("info", "route_plan_created", "Route plan created without execution.", subject_id))
        if route_plan.provider_selection is not None:
            findings.append(self._finding("info", "provider_selection_created", "Provider selection created without invocation.", subject_id))
        if route_plan.provider_invocation_required:
            findings.append(self._finding("warning", "provider_boundary_required", "Provider invocation boundary is deferred to v0.25.5.", subject_id))
            findings.append(self._finding("warning", "tool_routing_deferred_to_invocation", "Tool routing plan awaits invocation orchestrator.", subject_id))
            findings.append(self._finding("warning", "provider_invocation_deferred", "Provider invocation is deferred to v0.25.5.", subject_id))
        findings.append(self._finding("warning", "local_command_execution_deferred", "Local command execution is not allowed in v0.25.4.", subject_id))
        if route_plan.risk_review and route_plan.risk_review.requires_v024_gate:
            findings.append(self._finding("warning", "local_runtime_gate_required", "Local runtime route must preserve v0.24 gate sequence.", subject_id))
        risk_types = set(route_plan.risk_review.risk_categories if route_plan.risk_review else [])
        if "external_adapter" in risk_types:
            findings.append(self._finding("critical", "external_adapter_request_blocked", "External adapter request is blocked or deferred outside v0.25.", subject_id))
        if "memory_mutation" in risk_types:
            findings.append(self._finding("warning", "memory_continuity_deferred", "Memory continuity is deferred to v0.27.", subject_id))
        text = (request.sanitized_request_text or "").lower()
        if "workspace workbench" in text:
            findings.append(self._finding("warning", "workspace_workbench_deferred", "Workspace workbench is deferred to v0.26.", subject_id))
        if "schumpeter" in text:
            findings.append(self._finding("warning", "schumpeter_split_deferred", "Schumpeter split is deferred to v0.28.", subject_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", subject_id))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentToolRoutingFinding:
        return AgentToolRoutingFinding(
            finding_id=f"agent_tool_routing_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by policy.",
        )


class AgentToolRoutingReportService:
    def build_request_from_reports(
        self,
        safety_gate_report: AgentSafetyGateReport,
        intent_report: AgentIntentClassificationReport,
    ) -> AgentToolRoutingRequest:
        return AgentToolRoutingRequest(
            request_id=f"agent_tool_routing_request:{_safe_id(safety_gate_report.report_id)}",
            safety_gate_report_id=safety_gate_report.report_id,
            gate_outcome_envelope_id=safety_gate_report.outcome_envelope.outcome_envelope_id if safety_gate_report.outcome_envelope else None,
            intent_report_id=intent_report.report_id,
            task_frame_id=intent_report.task_frame.task_frame_id,
            turn_envelope_id=intent_report.request.turn_envelope_id,
            sanitized_request_text=intent_report.request.sanitized_request_text,
            source_refs=[
                {"type": "agent_safety_gate_report", "id": safety_gate_report.report_id},
                {"type": "agent_intent_classification_report", "id": intent_report.report_id},
            ],
        )

    def build_report(
        self,
        request_text: str = "Explain the project structure",
        safety_gate_report: AgentSafetyGateReport | None = None,
        intent_report: AgentIntentClassificationReport | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentToolRoutingReport:
        policy = AgentToolRoutingPolicyService().build_policy()
        source_intent_report = intent_report or AgentIntentClassificationReportService().build_report(request_text=request_text)
        source_safety_report = safety_gate_report or AgentSafetyGateReportService().build_report(
            request_text=request_text,
            intent_report=source_intent_report,
        )
        request = self.build_request_from_reports(source_safety_report, source_intent_report)
        catalog = AgentProviderCapabilityCatalogService().build_catalog_view()
        mappings = AgentRouteIntentMappingService().build_route_mappings()
        if not source_safety_report.allow_route:
            mapping = AgentRouteIntentMappingService().map_intent_to_route_kind("no_action_candidate")
        else:
            mapping = AgentRouteIntentMappingService().map_intent_to_route_kind(source_intent_report.intent_descriptor.primary_category)
        candidates = AgentProviderSelectionCandidateService().build_selection_candidates(mapping, catalog)
        selection = AgentProviderSelectionService().select_providers(mapping, candidates)
        steps = AgentToolRouteStepService().build_steps(mapping, selection, source_safety_report.allow_route)
        dependencies = AgentToolRouteDependencyService().build_dependencies(mapping.recommended_route_kind, steps)
        risk_review = AgentRouteRiskReviewService().build_risk_review(mapping, source_intent_report.task_frame, source_safety_report.allow_route)
        route_plan = AgentToolRoutePlanService().build_route_plan(
            request,
            source_safety_report,
            source_intent_report,
            mapping,
            selection,
            steps,
            dependencies,
            risk_review,
        )
        findings = AgentToolRoutingFindingService().build_findings(request, catalog, mapping, route_plan, attempt_flags)
        report_status = self._report_status(route_plan, findings)
        return AgentToolRoutingReport(
            report_id=f"agent_tool_routing_report:{_safe_id(request.request_id)}",
            created_at=utc_now_iso(),
            policy=policy,
            request=request,
            capability_catalog_view=catalog,
            route_mappings=mappings,
            route_plan=route_plan,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_5=route_plan.route_plan_status == "planned" and route_plan.provider_invocation_required,
            ready_for_v0_25_6=route_plan.route_plan_status in {"response_only", "no_route_due_to_gate", "failed", "blocked"},
            safety_gate_was_allow_route=source_safety_report.allow_route,
            tool_route_plan_created=route_plan.tool_route_created,
            provider_selection_created=route_plan.provider_selection is not None,
            next_required_step=route_plan.expected_next_stage,
            limitations=["v0.25.4 creates route plans and provider selections only; provider invocation is deferred to v0.25.5."],
            withdrawal_conditions=["Withdraw if v0.25.4 invokes providers, executes routes, executes commands, assembles responses, promotes memory, mutates persona, or uses an LLM judge."],
        )

    def build_all_parts(self, request_text: str = "Explain the project structure") -> dict[str, Any]:
        report = self.build_report(request_text=request_text)
        return {
            "report": report,
            "policy": report.policy,
            "request": report.request,
            "catalog": report.capability_catalog_view,
            "providers": report.capability_catalog_view.provider_capabilities,
            "mappings": report.route_mappings,
            "route_plan": report.route_plan,
            "selection": report.route_plan.provider_selection if report.route_plan else None,
            "steps": report.route_plan.route_steps if report.route_plan else [],
            "dependencies": report.route_plan.route_dependencies if report.route_plan else [],
            "risk_review": report.route_plan.risk_review if report.route_plan else None,
            "findings": report.findings,
        }

    def _report_status(self, route_plan: AgentToolRoutePlan, findings: list[AgentToolRoutingFinding]) -> str:
        if any(item.severity == "critical" for item in findings) or route_plan.route_plan_status == "blocked":
            return "blocked"
        if any(item.severity == "error" for item in findings) or route_plan.route_plan_status == "failed":
            return "failed"
        if any(item.severity == "warning" for item in findings) or route_plan.route_plan_status in {"response_only", "no_route_due_to_gate"}:
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_TOOL_ROUTING_VERSION,
            "layer": "agent_surface",
            "subject": "tool_routing_plan_provider_selection",
            "principles": [
                "tool route plan is not provider invocation",
                "provider selection is not provider execution",
                "route step is not action execution",
                "allow-route is not provider permission",
                "local runtime execution must go through v0.24 gate sequence",
                "provider invocation is deferred to v0.25.5",
                "response assembly is deferred to v0.25.6",
                "ask/repl is deferred to v0.25.7",
            ],
            "safety_boundary": {
                "tool_route_plan_created": "conditional",
                "provider_selection_created": "conditional",
                "tool_route_executed": False,
                "provider_invoked": False,
                "local_command_executed": False,
                "ask_executed": False,
                "repl_started": False,
                "response_assembled": False,
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
            "next_step": "v0.25.5 Internal Provider Invocation Orchestrator when provider route exists, otherwise v0.25.6 Response Assembly & Evidence Binder",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_tool_route_plan_created",
            "version": AGENT_TOOL_ROUTING_VERSION,
            "source_read_models": [
                "AgentSafetyGateState",
                "AgentGateOutcomeState",
                "AgentIntentClassificationState",
                "AgentTaskFrameState",
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
            ],
            "target_read_models": [
                "AgentToolRoutingState",
                "AgentProviderCapabilityCatalogViewState",
                "AgentProviderSelectionState",
                "AgentToolRoutePlanState",
                "AgentRouteRiskReviewState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_TOOL_ROUTING_EFFECT_TYPES,
        }


def render_agent_route_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentToolRoutingReport = parts["report"]
    route_plan = report.route_plan
    selection = route_plan.provider_selection if route_plan else None
    selected_providers = selection.selected_candidates if selection else []
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"tool_route_plan_created={str(report.tool_route_plan_created).lower()}",
        f"provider_selection_created={str(report.provider_selection_created).lower()}",
        f"route_kind={route_plan.route_kind if route_plan else 'unknown'}",
        f"selected_providers={','.join(candidate.provider_ref.provider_type for candidate in selected_providers)}",
        f"ready_for_v0_25_5={str(report.ready_for_v0_25_5).lower()}",
        f"ready_for_v0_25_6={str(report.ready_for_v0_25_6).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"tool_route_executed={str(report.tool_route_executed).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_started={str(report.repl_started).lower()}",
        f"response_assembled={str(report.response_assembled).lower()}",
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
    if section == "plan":
        for step in route_plan.route_steps:
            lines.append(f"- route_step={step.step_index}:{step.step_name}:{step.route_step_status}")
    elif section == "providers":
        for provider in parts["providers"]:
            lines.append(f"- provider={provider.provider_type} invocation_enabled_in_v025_4={str(provider.invocation_enabled_in_v025_4).lower()} executable_in_v025_4={str(provider.executable_in_v025_4).lower()}")
    elif section == "mappings":
        for mapping in parts["mappings"]:
            lines.append(f"- mapping={mapping.intent_category}->{mapping.recommended_route_kind}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    else:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)
