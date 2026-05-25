from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import time
from typing import Any


AGENT_SURFACE_CONTRACT_VERSION = "v0.25.0"
AGENT_SURFACE_CONTRACT_VERSION_NAME = "Agent Surface Contract"
AGENT_SURFACE_CONTRACT_KOREAN_NAME = "Agent 표면 계약"
AGENT_SURFACE_CONTRACT_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_SURFACE_CONTRACT_NEXT_STEP = "v0.25.1 Turn Envelope & Interaction Context"

AGENT_SURFACE_CONTRACT_OBJECT_TYPES = [
    "agent_surface_contract",
    "agent_surface_mode_descriptor",
    "agent_request_envelope_contract",
    "agent_response_envelope_contract",
    "agent_surface_outcome_policy",
    "agent_surface_permission_policy",
    "agent_surface_effect_policy",
    "agent_surface_routing_boundary",
    "agent_surface_evidence_policy",
    "agent_surface_observability_contract",
    "agent_surface_safety_boundary",
    "agent_surface_roadmap_boundary",
    "agent_reference_architecture_policy",
    "agent_surface_contract_finding",
    "agent_surface_contract_report",
    "internal_provider_consolidation_report",
    "internal_provider_v025_readiness_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_SURFACE_CONTRACT_EVENT_TYPES = [
    "agent_surface_contract_requested",
    "agent_surface_modes_declared",
    "agent_request_envelope_contract_created",
    "agent_response_envelope_contract_created",
    "agent_surface_outcome_policy_created",
    "agent_surface_permission_policy_created",
    "agent_surface_effect_policy_created",
    "agent_surface_routing_boundary_created",
    "agent_surface_evidence_policy_created",
    "agent_surface_observability_contract_created",
    "agent_surface_safety_boundary_created",
    "agent_surface_roadmap_boundary_created",
    "agent_reference_architecture_policy_created",
    "agent_surface_contract_report_created",
    "agent_surface_contract_blocked",
]

AGENT_SURFACE_CONTRACT_RELATION_TYPES = [
    "declares_agent_surface_contract",
    "declares_agent_surface_mode",
    "declares_agent_request_envelope_contract",
    "declares_agent_response_envelope_contract",
    "declares_agent_outcome_policy",
    "declares_agent_permission_policy",
    "declares_agent_effect_policy",
    "declares_agent_routing_boundary",
    "declares_agent_evidence_policy",
    "declares_agent_observability_contract",
    "declares_agent_safety_boundary",
    "declares_agent_roadmap_boundary",
    "declares_agent_reference_architecture_policy",
    "prepares_turn_envelope",
    "prepares_intent_classification",
    "prepares_safety_gate",
    "prepares_tool_routing",
    "prepares_provider_invocation_orchestration",
    "prepares_response_assembly",
    "prepares_ask_repl_surface",
    "prepares_agent_trace",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_schumpeter_split_to_v0_28",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "borrows_patterns_from_opencode_without_runtime_dependency",
    "borrows_patterns_from_openclaw_without_runtime_dependency",
    "borrows_patterns_from_hermes_without_runtime_dependency",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_tool_route_executed",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_memory_promoted",
    "not_external_agent_runtime_touched",
    "prevents_credential_exposure",
    "recorded_in_envelope",
    "derived_from_internal_provider_consolidation",
]

AGENT_SURFACE_CONTRACT_EFFECT_TYPES = [
    "read_only_observation",
    "state_candidate_created",
    "agent_surface_contract_declared",
]

AGENT_SURFACE_CONTRACT_FUTURE_EFFECT_TYPES = [
    "agent_turn_received",
    "agent_intent_classified",
    "agent_task_framed",
    "agent_safety_gate_evaluated",
    "agent_no_action_created",
    "agent_clarification_requested",
    "agent_tool_route_plan_created",
    "agent_provider_invocation_requested",
    "agent_provider_result_observed",
    "agent_response_assembled",
    "agent_response_emitted",
    "agent_trace_recorded",
    "agent_usability_metric_created",
]

AGENT_SURFACE_CONTRACT_CONDITIONAL_FUTURE_EFFECT_TYPES = [
    "internal_provider_invoked",
    "bounded_local_command_execution_requested",
    "bounded_local_command_executed",
]

AGENT_SURFACE_CONTRACT_FORBIDDEN_EFFECT_TYPES = [
    "agent_ask_executed",
    "agent_repl_started",
    "tool_route_executed",
    "provider_invoked",
    "internal_provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "unrestricted_shell_executed",
    "arbitrary_subprocess_executed",
    "external_provider_called",
    "external_agent_runtime_touched",
    "memory_promoted",
    "persona_mutated",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "schumpeter_split_introduced",
    "general_agent_usability_invoked",
]

AGENT_SURFACE_ALLOWED_OUTCOMES = [
    "answered",
    "routed_future",
    "needs_more_input",
    "clarification_requested",
    "no_action",
    "blocked",
    "deferred",
    "failed",
]

AGENT_SURFACE_FUTURE_SKILL_IDS = [
    "skill:agent_turn_envelope_create",
    "skill:agent_interaction_context_view",
    "skill:agent_intent_classify",
    "skill:agent_task_frame_create",
    "skill:agent_safety_gate_evaluate",
    "skill:agent_no_action_create",
    "skill:agent_clarification_create",
    "skill:agent_tool_route_plan_create",
    "skill:agent_provider_selection_create",
    "skill:agent_provider_invocation_orchestrate",
    "skill:agent_response_assemble",
    "skill:agent_evidence_bind",
    "skill:agent_ask",
    "skill:agent_repl",
    "skill:agent_trace_record",
    "skill:agent_usability_telemetry_view",
    "skill:agent_usability_consolidation_view",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


class AgentSurfacePrerequisiteSourceService:
    """Returns read-only prerequisite references without invoking providers."""

    def _source(self, source_id: str, subject: str, available: bool = True) -> dict[str, Any]:
        return {
            "source_id": source_id,
            "subject": subject,
            "available": available,
            "read_only": True,
            "new_provider_invocation_performed": False,
            "new_repository_search_performed": False,
            "new_file_read_performed": False,
            "new_process_inspection_performed": False,
            "new_local_command_executed": False,
            "command_rerun_performed": False,
            "credential_read_performed": False,
        }

    def load_v0_24_9_consolidation(self) -> dict[str, Any]:
        return self._source("internal_provider_consolidation_report_v0_24_9", "v0.24.9 Internal Provider Consolidation")

    def load_v0_24_9_v025_readiness(self) -> dict[str, Any]:
        return self._source("internal_provider_v025_readiness_report_v0_24_9", "v0.24.9 v0.25 readiness")

    def load_provider_registry(self) -> dict[str, Any]:
        return self._source("internal_provider_registry_report_v0_24_1", "provider registry")

    def load_skill_registry(self) -> dict[str, Any]:
        return self._source("agent_surface_skill_registry_contract_v0_25_0", "skill registry")

    def load_all_sources(self) -> dict[str, dict[str, Any]]:
        return {
            "v0.24.9_consolidation": self.load_v0_24_9_consolidation(),
            "v0.24.9_v025_readiness": self.load_v0_24_9_v025_readiness(),
            "provider_registry": self.load_provider_registry(),
            "skill_registry": self.load_skill_registry(),
        }


@dataclass
class AgentSurfaceModeDescriptor:
    mode_id: str
    mode_name: str
    description: str
    activation_version: str | None
    implementation_status: str
    user_facing: bool
    provider_invocation_capable_future: bool
    local_runtime_execution_capable_future: bool
    allowed_outcomes: list[str]
    forbidden_effect_types: list[str]
    introduced_in: str = AGENT_SURFACE_CONTRACT_VERSION
    memory_capable_future: bool = False
    external_adapter_capable_future: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentRequestEnvelopeContract:
    contract_id: str
    user_request_required: bool = True
    request_id_required: bool = True
    surface_mode_required: bool = True
    turn_context_ref_allowed: bool = True
    provider_context_ref_allowed: bool = True
    source_channel_ref_allowed: bool = True
    raw_secret_input_storage_forbidden: bool = True
    private_material_export_forbidden: bool = True
    persistent_memory_write_forbidden: bool = True
    persona_mutation_forbidden: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentResponseEnvelopeContract:
    contract_id: str
    response_id_required: bool = True
    request_ref_required: bool = True
    outcome_required: bool = True
    response_body_required_if_answered: bool = True
    evidence_bundle_required_if_provider_used: bool = True
    uncertainty_notes_supported: bool = True
    limitations_supported: bool = True
    no_action_rationale_required: bool = True
    blocked_rationale_required: bool = True
    raw_secret_output_forbidden: bool = True
    private_path_sanitization_required: bool = True
    final_conclusion_once: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceOutcomePolicy:
    policy_id: str
    allowed_outcomes: list[str]
    no_action_is_valid: bool = True
    clarification_is_valid: bool = True
    blocked_is_valid: bool = True
    route_requires_safety_gate_future: bool = True
    provider_invocation_requires_route_plan_future: bool = True
    local_runtime_execution_requires_v0_24_gate: bool = True
    evidence_required_for_provider_result: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfacePermissionPolicy:
    policy_id: str
    deny_by_default: bool = True
    user_request_not_permission: bool = True
    provider_invocation_requires_policy: bool = True
    local_runtime_execution_requires_v0_24_gate: bool = True
    local_runtime_execution_requires_single_use_authorization: bool = True
    external_provider_adapter_forbidden: bool = True
    external_agent_adapter_forbidden: bool = True
    memory_promotion_forbidden: bool = True
    persona_mutation_forbidden: bool = True
    file_mutation_forbidden_by_default: bool = True
    raw_secret_output_forbidden: bool = True
    llm_safety_judge_forbidden: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceEffectPolicy:
    policy_id: str
    allowed_effect_types_v0_25_0: list[str]
    future_effect_types_v0_25: list[str]
    conditional_future_effect_types: list[str]
    forbidden_effect_types_v0_25_0: list[str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceRoutingBoundary:
    boundary_id: str
    route_plan_enabled_v0_25_0: bool = False
    provider_invocation_enabled_v0_25_0: bool = False
    local_runtime_execution_enabled_v0_25_0: bool = False
    ask_enabled_v0_25_0: bool = False
    repl_enabled_v0_25_0: bool = False
    direct_tool_call_forbidden: bool = True
    v024_provider_boundary_must_be_respected: bool = True
    no_provider_boundary_bypass: bool = True
    no_direct_subprocess: bool = True
    no_external_adapter: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceEvidencePolicy:
    policy_id: str
    evidence_required_for_provider_outputs: bool = True
    fact_inference_uncertainty_separation_required: bool = True
    provider_result_label_required: bool = True
    no_action_rationale_required: bool = True
    uncertainty_note_required_when_incomplete: bool = True
    limitation_note_supported: bool = True
    raw_provider_output_dump_forbidden: bool = True
    raw_secret_output_forbidden: bool = True
    private_path_sanitization_required: bool = True
    final_conclusion_once: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceObservabilityContract:
    contract_id: str
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    execution_envelope_visible: bool = True
    agent_turn_must_emit_event_future: bool = True
    intent_classification_must_emit_event_future: bool = True
    safety_gate_must_emit_event_future: bool = True
    route_plan_must_emit_event_future: bool = True
    provider_invocation_must_emit_event_future: bool = True
    response_assembly_must_emit_event_future: bool = True
    no_action_must_be_recorded: bool = True
    blocked_decision_must_be_recorded: bool = True
    raw_secret_output_forbidden: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceSafetyBoundary:
    boundary_id: str
    agent_ask_execution_count: int = 0
    agent_repl_execution_count: int = 0
    tool_route_execution_count: int = 0
    provider_invocation_count: int = 0
    local_command_execution_count: int = 0
    command_rerun_count: int = 0
    unrestricted_shell_count: int = 0
    arbitrary_subprocess_count: int = 0
    external_provider_call_count: int = 0
    external_agent_runtime_touch_count: int = 0
    memory_promotion_count: int = 0
    persona_mutation_count: int = 0
    file_mutation_count: int = 0
    credential_exposure_count: int = 0
    raw_secret_output_count: int = 0
    llm_judge_for_safety_count: int = 0
    schumpeter_split_count: int = 0
    status: str = "passed"
    findings: list[dict[str, Any]] = field(default_factory=list)
    version: str = AGENT_SURFACE_CONTRACT_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceRoadmapBoundary:
    boundary_id: str
    current_track: str = "v0.25.x Bounded General Agent Surface & Internal Tool Routing"
    current_version_scope: str = "v0.25.0 contract_only"
    next_version: str = AGENT_SURFACE_CONTRACT_NEXT_STEP
    workspace_workbench_deferred_to: str = "v0.26.x"
    memory_continuity_deferred_to: str = "v0.27.x"
    public_alpha_schumpeter_split_deferred_to: str = "v0.28.x"
    external_provider_adapters_deferred_to: str = "v0.29.x+"
    external_agent_dominion_deferred_to: str = "v0.30.x+"
    growthkernel_bridge_deferred: bool = True
    roadmap_status: str = "aligned"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentReferenceArchitecturePolicy:
    policy_id: str
    reference_notes: list[str]
    version: str = AGENT_SURFACE_CONTRACT_VERSION
    direct_implementation_strategy: bool = True
    opencode_reference_allowed: bool = True
    openclaw_reference_allowed: bool = True
    hermes_reference_allowed: bool = True
    opencode_runtime_dependency_allowed: bool = False
    openclaw_runtime_dependency_allowed: bool = False
    hermes_runtime_dependency_allowed: bool = False
    external_agent_runtime_control_allowed: bool = False
    source_code_copying_without_review_forbidden: bool = True
    architecture_pattern_absorption_allowed: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceContract:
    contract_id: str
    definition: str
    surface_modes: list[AgentSurfaceModeDescriptor]
    request_envelope_contract: AgentRequestEnvelopeContract
    response_envelope_contract: AgentResponseEnvelopeContract
    outcome_policy: AgentSurfaceOutcomePolicy
    permission_policy: AgentSurfacePermissionPolicy
    effect_policy: AgentSurfaceEffectPolicy
    routing_boundary: AgentSurfaceRoutingBoundary
    evidence_policy: AgentSurfaceEvidencePolicy
    observability_contract: AgentSurfaceObservabilityContract
    safety_boundary: AgentSurfaceSafetyBoundary
    roadmap_boundary: AgentSurfaceRoadmapBoundary
    reference_architecture_policy: AgentReferenceArchitecturePolicy
    version: str = AGENT_SURFACE_CONTRACT_VERSION
    layer: str = "agent_surface"
    release_track: str = AGENT_SURFACE_CONTRACT_TRACK
    status: str = "contract_only"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class AgentSurfaceContractFinding:
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
class AgentSurfaceContractReport:
    report_id: str
    created_at: str
    contract: AgentSurfaceContract
    findings: list[AgentSurfaceContractFinding]
    report_status: str
    ready_for_v0_25_1: bool
    version: str = AGENT_SURFACE_CONTRACT_VERSION
    ready_for_v0_26: bool = False
    agent_ask_enabled: bool = False
    agent_repl_enabled: bool = False
    tool_route_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    memory_continuity_implemented: bool = False
    workspace_workbench_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_SURFACE_CONTRACT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.1 turn envelope implementation begins or agent surface policy changes."

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class AgentSurfaceModeService:
    def build_surface_modes(self) -> list[AgentSurfaceModeDescriptor]:
        specs = [
            ("contract_view", "contract_only", AGENT_SURFACE_CONTRACT_VERSION, True, False, False, "Inspect the v0.25.0 agent surface contract."),
            ("single_turn_ask_future", "future_track", "v0.25.x", True, True, False, "Future single-turn ask surface; not executable in v0.25.0."),
            ("repl_future", "future_track", "v0.25.x", True, True, False, "Future REPL surface; not executable in v0.25.0."),
            ("provider_routing_future", "future_track", "v0.25.x", False, True, False, "Future route planning and provider selection."),
            ("diagnostic_future", "future_track", "v0.25.x", False, True, False, "Future diagnostic response path."),
            ("read_only_answer_future", "future_track", "v0.25.x", True, True, False, "Future evidence-bound read-only answer assembly."),
            ("bounded_execution_future", "future_track", "v0.25.x", False, True, True, "Future bounded execution request path through the v0.24 gate."),
            ("blocked", "blocked", None, False, False, False, "Blocked surface outcome for unsafe or disallowed requests."),
            ("unknown", "disabled", None, False, False, False, "Unknown surface mode is disabled until classified."),
        ]
        return [
            AgentSurfaceModeDescriptor(
                mode_id=f"agent_surface_mode:{mode_name}",
                mode_name=mode_name,
                description=description,
                activation_version=activation,
                implementation_status=status,
                user_facing=user_facing,
                provider_invocation_capable_future=provider_future,
                local_runtime_execution_capable_future=local_future,
                allowed_outcomes=AGENT_SURFACE_ALLOWED_OUTCOMES.copy(),
                forbidden_effect_types=AGENT_SURFACE_CONTRACT_FORBIDDEN_EFFECT_TYPES.copy(),
                evidence_refs=[{"type": "contract", "version": AGENT_SURFACE_CONTRACT_VERSION}],
            )
            for mode_name, status, activation, user_facing, provider_future, local_future, description in specs
        ]


class AgentSurfaceOutcomePolicyService:
    def build_outcome_policy(self) -> AgentSurfaceOutcomePolicy:
        return AgentSurfaceOutcomePolicy(
            policy_id="agent_surface_outcome_policy:v0.25.0",
            allowed_outcomes=AGENT_SURFACE_ALLOWED_OUTCOMES.copy(),
            notes=["No-action, clarification, and blocked are first-class outcomes."],
        )


class AgentSurfacePermissionPolicyService:
    def build_permission_policy(self) -> AgentSurfacePermissionPolicy:
        return AgentSurfacePermissionPolicy(
            policy_id="agent_surface_permission_policy:v0.25.0",
            notes=["User request is not automatic permission; provider and runtime use remain gated future work."],
        )


class AgentSurfaceEffectPolicyService:
    def build_effect_policy(self) -> AgentSurfaceEffectPolicy:
        return AgentSurfaceEffectPolicy(
            policy_id="agent_surface_effect_policy:v0.25.0",
            allowed_effect_types_v0_25_0=AGENT_SURFACE_CONTRACT_EFFECT_TYPES.copy(),
            future_effect_types_v0_25=AGENT_SURFACE_CONTRACT_FUTURE_EFFECT_TYPES.copy(),
            conditional_future_effect_types=AGENT_SURFACE_CONTRACT_CONDITIONAL_FUTURE_EFFECT_TYPES.copy(),
            forbidden_effect_types_v0_25_0=AGENT_SURFACE_CONTRACT_FORBIDDEN_EFFECT_TYPES.copy(),
            notes=["v0.25.0 declares only contract state; executable effects are future-gated."],
        )


class AgentSurfaceRoutingBoundaryService:
    def build_routing_boundary(self) -> AgentSurfaceRoutingBoundary:
        return AgentSurfaceRoutingBoundary(
            boundary_id="agent_surface_routing_boundary:v0.25.0",
            notes=["Route planning, provider invocation, ask, REPL, and local runtime execution are disabled in v0.25.0."],
        )


class AgentSurfaceEvidencePolicyService:
    def build_evidence_policy(self) -> AgentSurfaceEvidencePolicy:
        return AgentSurfaceEvidencePolicy(
            policy_id="agent_surface_evidence_policy:v0.25.0",
            notes=["Provider outputs must be evidence-bound and separated from inference and uncertainty."],
        )


class AgentSurfaceObservabilityContractService:
    def build_observability_contract(self) -> AgentSurfaceObservabilityContract:
        return AgentSurfaceObservabilityContract(
            contract_id="agent_surface_observability_contract:v0.25.0",
            notes=["Future agent turns must be visible through OCEL, PIG, OCPX, and execution envelope views."],
        )


class AgentSurfaceSafetyBoundaryService:
    def build_safety_boundary(self) -> AgentSurfaceSafetyBoundary:
        return AgentSurfaceSafetyBoundary(
            boundary_id="agent_surface_safety_boundary:v0.25.0",
            findings=[{"finding_type": "ok", "message": "v0.25.0 contract-only safety counts are zero."}],
        )


class AgentSurfaceRoadmapBoundaryService:
    def build_roadmap_boundary(self) -> AgentSurfaceRoadmapBoundary:
        return AgentSurfaceRoadmapBoundary(
            boundary_id="agent_surface_roadmap_boundary:v0.25.0",
            notes=[
                "v0.25.1 begins turn envelope and interaction context.",
                "v0.26 workspace workbench, v0.27 memory continuity, v0.29+ adapters, and v0.30+ external agent dominion remain deferred.",
            ],
        )


class AgentReferenceArchitecturePolicyService:
    def build_reference_architecture_policy(self) -> AgentReferenceArchitecturePolicy:
        notes = [
            "OpenCode patterns may inform session/tool registry/permission/provider abstraction.",
            "Hermes patterns may inform future isolation/delegation/bounded memory design.",
            "OpenClaw patterns may inform future personal assistant UX and external agent risk model.",
            "Actual external agent domination is deferred to v0.30+.",
            "Memory continuity is deferred to v0.27.",
            "Workspace workbench is deferred to v0.26.",
            "External provider and agent adapters are deferred to v0.29+.",
        ]
        return AgentReferenceArchitecturePolicy(
            policy_id="agent_reference_architecture_policy:v0.25.0",
            reference_notes=notes,
            evidence_refs=[{"type": "roadmap_policy", "version": AGENT_SURFACE_CONTRACT_VERSION}],
        )


class AgentSurfaceContractService:
    def build_contract(self) -> AgentSurfaceContract:
        return AgentSurfaceContract(
            contract_id="agent_surface_contract:v0.25.0",
            definition=(
                "Contract-only bounded general agent surface foundation for request envelopes, "
                "response envelopes, outcomes, permissions, effects, routing boundaries, evidence, "
                "observability, safety, roadmap, and reference architecture."
            ),
            surface_modes=AgentSurfaceModeService().build_surface_modes(),
            request_envelope_contract=AgentRequestEnvelopeContract(
                contract_id="agent_request_envelope_contract:v0.25.0",
                notes=["Raw secrets and persistent memory writes are forbidden in the v0.25.0 request envelope."],
            ),
            response_envelope_contract=AgentResponseEnvelopeContract(
                contract_id="agent_response_envelope_contract:v0.25.0",
                notes=["Responses must declare outcomes and preserve evidence, uncertainty, and limitation separation."],
            ),
            outcome_policy=AgentSurfaceOutcomePolicyService().build_outcome_policy(),
            permission_policy=AgentSurfacePermissionPolicyService().build_permission_policy(),
            effect_policy=AgentSurfaceEffectPolicyService().build_effect_policy(),
            routing_boundary=AgentSurfaceRoutingBoundaryService().build_routing_boundary(),
            evidence_policy=AgentSurfaceEvidencePolicyService().build_evidence_policy(),
            observability_contract=AgentSurfaceObservabilityContractService().build_observability_contract(),
            safety_boundary=AgentSurfaceSafetyBoundaryService().build_safety_boundary(),
            roadmap_boundary=AgentSurfaceRoadmapBoundaryService().build_roadmap_boundary(),
            reference_architecture_policy=AgentReferenceArchitecturePolicyService().build_reference_architecture_policy(),
            notes=[
                "Agent surface is not arbitrary autonomous execution.",
                "ChantaCore directly implements its own OCEL-native agent spine.",
                "v0.25.0 does not execute ask, REPL, routing, providers, tools, memory, or local commands.",
            ],
        )

    def view_contract(self) -> AgentSurfaceContract:
        return self.build_contract()


class AgentSurfaceContractFindingService:
    def build_findings(self, contract: AgentSurfaceContract) -> list[AgentSurfaceContractFinding]:
        findings = [
            AgentSurfaceContractFinding(
                finding_id="agent_surface_contract_finding:ok",
                severity="info",
                finding_type="ok",
                message="Agent surface contract is declared as contract-only.",
                subject_ref={"contract_id": contract.contract_id},
                evidence_refs=[{"type": "contract_section", "section": "agent_surface_contract"}],
                withdrawal_condition="Withdraw if any ask, REPL, route execution, provider invocation, local execution, memory, adapter, or runtime dependency is enabled in v0.25.0.",
            )
        ]
        routing = contract.routing_boundary
        if routing.ask_enabled_v0_25_0:
            findings.append(self._critical("ask_enabled_too_early", "Ask is enabled too early."))
        if routing.repl_enabled_v0_25_0:
            findings.append(self._critical("repl_enabled_too_early", "REPL is enabled too early."))
        if routing.route_plan_enabled_v0_25_0:
            findings.append(self._critical("tool_route_execution_enabled_too_early", "Route execution is enabled too early."))
        if routing.provider_invocation_enabled_v0_25_0:
            findings.append(self._critical("provider_invocation_enabled_too_early", "Provider invocation is enabled too early."))
        if routing.local_runtime_execution_enabled_v0_25_0:
            findings.append(self._critical("local_runtime_execution_enabled_too_early", "Local runtime execution is enabled too early."))
        return findings

    def _critical(self, finding_type: str, message: str) -> AgentSurfaceContractFinding:
        return AgentSurfaceContractFinding(
            finding_id=f"agent_surface_contract_finding:{finding_type}",
            severity="critical",
            finding_type=finding_type,
            message=message,
            subject_ref=None,
            evidence_refs=[],
            withdrawal_condition="Withdraw if v0.25.0 is restored to contract-only boundaries.",
        )


class AgentSurfaceContractReportService:
    def build_report(self) -> AgentSurfaceContractReport:
        sources = AgentSurfacePrerequisiteSourceService().load_all_sources()
        contract = AgentSurfaceContractService().build_contract()
        findings = AgentSurfaceContractFindingService().build_findings(contract)
        blocked = any(finding.severity == "critical" for finding in findings)
        missing_readiness = not sources["v0.24.9_v025_readiness"]["available"]
        status = "blocked" if blocked else "warning" if missing_readiness else "passed"
        return AgentSurfaceContractReport(
            report_id="agent_surface_contract_report:v0.25.0",
            created_at=_utc_now(),
            contract=contract,
            findings=findings,
            report_status=status,
            ready_for_v0_25_1=not blocked,
            limitations=["v0.25.0 is contract-only and does not execute ask, REPL, routing, providers, tools, memory, or local commands."],
            withdrawal_conditions=[
                "Withdraw if OpenCode, OpenClaw, or Hermes becomes a runtime dependency.",
                "Withdraw if provider invocation, local command execution, memory continuity, workspace workbench, Schumpeter split, or an LLM judge is introduced in v0.25.0.",
            ],
        )

    def build_all_parts(self) -> dict[str, Any]:
        report = self.build_report()
        contract = report.contract
        return {
            "report": report,
            "contract": contract,
            "modes": contract.surface_modes,
            "request-envelope": contract.request_envelope_contract,
            "response-envelope": contract.response_envelope_contract,
            "outcome-policy": contract.outcome_policy,
            "permission-policy": contract.permission_policy,
            "effect-policy": contract.effect_policy,
            "routing-boundary": contract.routing_boundary,
            "evidence-policy": contract.evidence_policy,
            "observability": contract.observability_contract,
            "safety-boundary": contract.safety_boundary,
            "roadmap-boundary": contract.roadmap_boundary,
            "reference-architecture": contract.reference_architecture_policy,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_SURFACE_CONTRACT_VERSION,
            "layer": "agent_surface",
            "subject": "agent_surface_contract",
            "principles": [
                "agent surface is not arbitrary autonomous execution",
                "user request is not automatic permission",
                "ask/repl surface is not unrestricted shell",
                "tool routing is not arbitrary tool execution",
                "no-action is a valid agent outcome",
                "provider result must be evidence-bound",
                "local runtime execution must go through v0.24.7 gate",
                "ChantaCore directly implements its own OCEL-native agent spine",
            ],
            "future_direction": {
                "v0.25": "bounded general agent surface",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.28": "public alpha / Schumpeter split preparation",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "reference_architecture": [
                "OpenCode patterns may inform session/tool/permission/provider abstraction.",
                "Hermes patterns may inform future isolation/delegation/bounded memory.",
                "OpenClaw patterns may inform future assistant UX and external-agent risk handling.",
                "No runtime dependency on these projects in v0.25.0.",
            ],
            "safety_boundary": {
                "agent_ask_enabled": False,
                "agent_repl_enabled": False,
                "tool_route_execution_enabled": False,
                "provider_invocation_enabled": False,
                "local_runtime_execution_enabled": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "memory_continuity_implemented": False,
                "workspace_workbench_implemented": False,
                "schumpeter_split_introduced": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "llm_judge_enabled": False,
            },
            "next_step": AGENT_SURFACE_CONTRACT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_surface_contract_declared",
            "version": AGENT_SURFACE_CONTRACT_VERSION,
            "source_read_models": [
                "InternalProviderConsolidationState",
                "InternalProviderV025ReadinessState",
                "InternalProviderReleaseState",
            ],
            "target_read_models": [
                "AgentSurfaceContractState",
                "AgentSurfaceModeState",
                "AgentSurfacePermissionPolicyState",
                "AgentSurfaceEffectPolicyState",
                "AgentSurfaceRoutingBoundaryState",
                "AgentSurfaceEvidencePolicyState",
                "AgentSurfaceRoadmapBoundaryState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_SURFACE_CONTRACT_EFFECT_TYPES,
        }


def render_agent_surface_contract_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentSurfaceContractReport = parts["report"]
    contract = report.contract
    lines = [
        f"version={report.version}",
        f"layer={contract.layer}",
        f"status={contract.status}",
        f"ready_for_v0_25_1={str(report.ready_for_v0_25_1).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"agent_ask_enabled={str(report.agent_ask_enabled).lower()}",
        f"agent_repl_enabled={str(report.agent_repl_enabled).lower()}",
        f"tool_route_execution_enabled={str(report.tool_route_execution_enabled).lower()}",
        f"provider_invocation_enabled={str(report.provider_invocation_enabled).lower()}",
        f"local_runtime_execution_enabled={str(report.local_runtime_execution_enabled).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"memory_continuity_implemented={str(report.memory_continuity_implemented).lower()}",
        f"workspace_workbench_implemented={str(report.workspace_workbench_implemented).lower()}",
        f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"direct_implementation_strategy={str(contract.reference_architecture_policy.direct_implementation_strategy).lower()}",
        f"opencode_runtime_dependency_allowed={str(contract.reference_architecture_policy.opencode_runtime_dependency_allowed).lower()}",
        f"openclaw_runtime_dependency_allowed={str(contract.reference_architecture_policy.openclaw_runtime_dependency_allowed).lower()}",
        f"hermes_runtime_dependency_allowed={str(contract.reference_architecture_policy.hermes_runtime_dependency_allowed).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "modes":
        for mode in contract.surface_modes:
            lines.append(f"- {mode.mode_name}: {mode.implementation_status}")
    elif section == "outcome-policy":
        lines.append(f"allowed_outcomes={','.join(contract.outcome_policy.allowed_outcomes)}")
        lines.append(f"no_action_is_valid={str(contract.outcome_policy.no_action_is_valid).lower()}")
    elif section == "permission-policy":
        lines.append(f"deny_by_default={str(contract.permission_policy.deny_by_default).lower()}")
        lines.append(f"user_request_not_permission={str(contract.permission_policy.user_request_not_permission).lower()}")
    elif section == "effect-policy":
        lines.append(f"allowed_effect_types={','.join(contract.effect_policy.allowed_effect_types_v0_25_0)}")
    elif section == "routing-boundary":
        lines.append(f"direct_tool_call_forbidden={str(contract.routing_boundary.direct_tool_call_forbidden).lower()}")
        lines.append(f"no_provider_boundary_bypass={str(contract.routing_boundary.no_provider_boundary_bypass).lower()}")
    elif section == "evidence-policy":
        lines.append(f"fact_inference_uncertainty_separation_required={str(contract.evidence_policy.fact_inference_uncertainty_separation_required).lower()}")
        lines.append(f"raw_provider_output_dump_forbidden={str(contract.evidence_policy.raw_provider_output_dump_forbidden).lower()}")
    elif section == "observability":
        lines.append(f"ocel_visible={str(contract.observability_contract.ocel_visible).lower()}")
        lines.append(f"pig_visible={str(contract.observability_contract.pig_visible).lower()}")
        lines.append(f"ocpx_visible={str(contract.observability_contract.ocpx_visible).lower()}")
    elif section == "safety-boundary":
        lines.append(f"safety_status={contract.safety_boundary.status}")
        lines.append(f"agent_ask_execution_count={contract.safety_boundary.agent_ask_execution_count}")
        lines.append(f"provider_invocation_count={contract.safety_boundary.provider_invocation_count}")
    elif section == "roadmap-boundary":
        lines.append(f"current_track={contract.roadmap_boundary.current_track}")
        lines.append(f"next_version={contract.roadmap_boundary.next_version}")
        lines.append(f"external_agent_dominion_deferred_to={contract.roadmap_boundary.external_agent_dominion_deferred_to}")
    elif section == "reference-architecture":
        for note in contract.reference_architecture_policy.reference_notes:
            lines.append(f"- {note}")
    else:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)
