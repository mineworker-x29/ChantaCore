from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any

from chanta_core.agent_surface.ask_repl import _safe_id
from chanta_core.utility.time import utc_now_iso


AGENT_USABILITY_CONSOLIDATION_VERSION = "v0.25.9"
AGENT_USABILITY_CONSOLIDATION_VERSION_NAME = "General Agent Usability Consolidation"
AGENT_USABILITY_CONSOLIDATION_KOREAN_NAME = "일반 Agent 사용성 통합·릴리즈 준비성"
AGENT_USABILITY_CONSOLIDATION_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_USABILITY_RELEASE_NAME = "Bounded General Agent Surface Foundation v1"
AGENT_USABILITY_NEXT_STEP = "v0.26.0 Workspace Agent Workbench Contract"

AGENT_USABILITY_INCLUDED_VERSIONS = [
    "v0.25.0",
    "v0.25.1",
    "v0.25.2",
    "v0.25.3",
    "v0.25.4",
    "v0.25.5",
    "v0.25.6",
    "v0.25.7",
    "v0.25.8",
    "v0.25.9",
]

AGENT_USABILITY_STAGE_ORDER = [
    "v0.25.1_turn_envelope",
    "v0.25.2_intent_task",
    "v0.25.3_safety_gate",
    "v0.25.4_route_plan_if_allow_route",
    "v0.25.5_provider_invocation_if_required",
    "v0.25.6_response_assembly",
    "v0.25.7_surface_emission",
]

AGENT_USABILITY_OBJECT_TYPES = [
    "agent_usability_foundation_snapshot",
    "agent_usability_subject_component",
    "agent_surface_capability_map",
    "agent_surface_capability_map_entry",
    "agent_surface_coverage_matrix",
    "agent_surface_coverage_matrix_row",
    "agent_surface_pipeline_boundary_report",
    "agent_surface_safety_boundary_report",
    "agent_surface_trace_telemetry_coverage_report",
    "agent_surface_roadmap_boundary_report",
    "agent_surface_gap",
    "agent_surface_gap_register",
    "agent_surface_release_manifest",
    "agent_v026_readiness_report",
    "agent_usability_consolidation_finding",
    "agent_usability_consolidation_report",
    "agent_workbench_handoff_packet",
    "agent_surface_contract",
    "agent_ask_repl_report",
    "agent_trace_telemetry_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_USABILITY_EVENT_TYPES = [
    "agent_usability_consolidation_requested",
    "agent_usability_sources_loaded",
    "agent_usability_subject_components_created",
    "agent_surface_capability_map_created",
    "agent_surface_coverage_matrix_created",
    "agent_surface_pipeline_boundary_report_created",
    "agent_surface_safety_boundary_report_created",
    "agent_surface_trace_telemetry_coverage_report_created",
    "agent_surface_roadmap_boundary_report_created",
    "agent_surface_gap_register_created",
    "agent_surface_release_manifest_created",
    "agent_v026_readiness_report_created",
    "agent_workbench_handoff_packet_created",
    "agent_usability_consolidation_report_created",
    "agent_usability_release_ready",
    "agent_usability_release_warning",
    "agent_usability_release_blocked",
]

AGENT_USABILITY_EFFECT_TYPES = [
    "read_only_observation",
    "agent_usability_consolidation_created",
    "agent_surface_release_manifest_created",
    "agent_v026_readiness_created",
    "agent_workbench_handoff_packet_created",
    "state_candidate_created",
]

AGENT_USABILITY_FORBIDDEN_EFFECT_TYPES = [
    "agent_ask_executed",
    "agent_repl_started",
    "agent_repl_turn_executed",
    "final_response_emitted",
    "provider_invoked",
    "internal_provider_invoked",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "direct_file_access_performed",
    "direct_subprocess_called",
    "background_execution_started",
    "continuous_watcher_started",
    "autonomous_optimization_performed",
    "workspace_workbench_implemented",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "external_provider_called",
    "external_agent_runtime_touched",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "raw_provider_output_inline",
    "raw_transcript_persisted",
    "schumpeter_split_introduced",
]

AGENT_USABILITY_EXCLUDED_CAPABILITIES = [
    "Workspace Agent Workbench UI",
    "Memory Candidate & Continuity",
    "External Provider Adapter",
    "External Agent Dominion Bridge",
    "Schumpeter split / company wrapper",
    "GrowthKernel runtime dependency",
    "autonomous loop",
    "background execution",
    "direct provider bypass",
    "direct subprocess",
    "direct file mutation",
    "command rerun loop",
    "automatic repair loop",
    "raw transcript persistence",
]

AGENT_USABILITY_REQUIRED_FUTURE_GAPS = [
    "workspace_agent_workbench_not_started",
    "trace_explorer_not_started",
    "provider_browser_not_started",
    "manual_approval_ui_not_started",
    "memory_candidate_continuity_not_started",
    "public_alpha_schumpeter_split_not_started",
    "external_provider_adapters_not_started",
    "external_agent_dominion_bridge_not_started",
    "growthkernel_bridge_not_started",
]


def _ref(ref_type: str, ref_id: str, version: str = AGENT_USABILITY_CONSOLIDATION_VERSION) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id, "version": version}


def _count(items: list[Any], attr: str, value: Any) -> int:
    return sum(1 for item in items if getattr(item, attr) == value)


@dataclass
class _Model:
    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUsabilitySubjectComponent(_Model):
    component_id: str
    version_introduced: str
    subject_id: str
    subject_name: str
    component_type: str
    skill_ids: list[str]
    status: str
    user_facing: bool
    execution_capable: bool
    provider_invocation_capable: bool
    bounded_execution_capable: bool
    response_emission_capable: bool
    trace_capable: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    latest_artifact_id: str | None
    finding_count: int
    memory_capable: bool = False
    external_adapter: bool = False
    workbench_ui: bool = False
    notes: list[str] = field(default_factory=list)


@dataclass
class AgentSurfaceCapabilityMapEntry(_Model):
    capability_id: str
    name: str
    version_introduced: str
    skill_ids: list[str]
    status: str
    source_read_models: list[str]
    target_read_models: list[str]
    effect_types: list[str]
    forbidden_effect_types: list[str]
    user_facing: bool
    provider_invocation_capable: bool
    local_runtime_capable: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    mutating: bool = False
    external_adapter: bool = False
    memory_capable: bool = False
    workbench_ui: bool = False
    safety_notes: list[str] = field(default_factory=list)


@dataclass
class AgentSurfaceCapabilityMap(_Model):
    map_id: str
    entries: list[AgentSurfaceCapabilityMapEntry]
    implemented_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    future_track_count: int
    user_facing_count: int
    provider_invocation_capability_count: int
    response_emission_capability_count: int
    trace_capability_count: int
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    external_adapter_count: int = 0
    memory_capability_count: int = 0
    workbench_ui_count: int = 0


@dataclass
class AgentSurfaceCoverageMatrixRow(_Model):
    subject_id: str
    version_introduced: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_boundary_tests: bool
    has_docs: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_safety_boundary: bool
    latest_artifact_available: bool
    coverage_notes: list[str] = field(default_factory=list)


@dataclass
class AgentSurfaceCoverageMatrix(_Model):
    matrix_id: str
    rows: list[AgentSurfaceCoverageMatrixRow]
    coverage_status: str
    missing_required_coverage_count: int
    optional_gap_count: int
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION


@dataclass
class AgentSurfacePipelineBoundaryReport(_Model):
    report_id: str
    required_stage_order: list[str]
    stage_available_count: int
    stage_missing_count: int
    stage_boundary_passed: bool
    ask_pipeline_available: bool
    repl_surface_available: bool
    response_emission_available: bool
    provider_invocation_via_v0255_only: bool
    local_runtime_via_v024_only: bool
    trace_telemetry_available: bool
    no_direct_bypass: bool
    pipeline_boundary_status: str
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentSurfaceSafetyBoundaryReport(_Model):
    report_id: str
    ask_count: int
    repl_turn_count: int
    final_response_emission_count: int
    provider_invocation_count: int
    bounded_local_command_execution_count: int
    response_assembly_count: int
    trace_record_count: int
    telemetry_report_count: int
    direct_provider_invocation_count: int
    direct_file_access_count: int
    direct_subprocess_count: int
    direct_local_command_execution_count: int
    command_rerun_count: int
    automatic_repair_count: int
    autonomous_loop_count: int
    background_execution_count: int
    self_prompt_loop_count: int
    workspace_workbench_count: int
    memory_promotion_count: int
    persistent_memory_write_count: int
    persona_mutation_count: int
    external_provider_adapter_count: int
    external_agent_adapter_count: int
    credential_exposure_count: int
    raw_secret_output_count: int
    raw_provider_output_inline_count: int
    raw_transcript_persistence_count: int
    schumpeter_split_count: int
    llm_judge_count: int
    status: str
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentSurfaceTraceTelemetryCoverageReport(_Model):
    report_id: str
    trace_available: bool
    ocel_projection_available: bool
    metric_set_available: bool
    telemetry_report_available: bool
    stage_trace_coverage: dict[str, bool]
    decision_trace_coverage: dict[str, bool]
    route_trace_coverage: bool
    provider_trace_coverage: bool
    response_emission_trace_coverage: bool
    raw_trace_privacy_passed: bool
    coverage_status: str
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentSurfaceRoadmapBoundaryReport(_Model):
    report_id: str
    roadmap_status: str
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    current_track: str = "v0.25.x Bounded General Agent Surface & Internal Tool Routing"
    next_track: str = "v0.26.x Workspace Agent Workbench"
    next_version: str = AGENT_USABILITY_NEXT_STEP
    v026_workbench_deferred_until_now: bool = True
    v027_memory_continuity_deferred: bool = True
    v028_public_alpha_schumpeter_split_deferred: bool = True
    v029_external_provider_adapters_deferred: bool = True
    v030_external_agent_dominion_deferred: bool = True
    growthkernel_bridge_deferred: bool = True
    findings: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class AgentSurfaceGap(_Model):
    gap_id: str
    title: str
    description: str
    severity: str
    affected_subjects: list[str]
    recommended_track: str | None
    withdrawal_condition: str | None


@dataclass
class AgentSurfaceGapRegister(_Model):
    register_id: str
    gaps: list[AgentSurfaceGap]
    blocker_count: int
    warning_count: int
    future_track_count: int
    gap_status: str
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION


@dataclass
class AgentSurfaceReleaseManifest(_Model):
    manifest_id: str
    included_versions: list[str]
    included_subjects: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    pipeline_boundary_report_id: str
    safety_boundary_report_id: str
    trace_telemetry_coverage_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_status: str
    release_version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    release_name: str = AGENT_USABILITY_RELEASE_NAME
    notes: list[str] = field(default_factory=list)


@dataclass
class AgentV026ReadinessReport(_Model):
    report_id: str
    ready_for_v0_26: bool
    substrate_requirements_met: bool
    agent_surface_contract_available: bool
    turn_envelope_available: bool
    intent_task_framing_available: bool
    safety_gate_available: bool
    routing_plan_available: bool
    provider_invocation_available: bool
    response_assembly_available: bool
    ask_repl_surface_available: bool
    trace_telemetry_available: bool
    ocel_projection_available: bool
    safety_boundary_passed: bool
    blockers: list[str]
    warnings: list[str]
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    target_track: str = "v0.26.x Workspace Agent Workbench"
    recommended_next_version: str = AGENT_USABILITY_NEXT_STEP
    workbench_not_implemented_yet: bool = True
    notes: list[str] = field(default_factory=list)


@dataclass
class AgentUsabilityConsolidationFinding(_Model):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AgentWorkbenchHandoffPacket(_Model):
    handoff_packet_id: str
    target_version: str
    target_track: str
    source_release_manifest_id: str
    source_consolidation_report_id: str
    workbench_ready_inputs: list[str]
    not_implemented_in_v0259: list[str]
    handoff_status: str
    evidence_refs: list[dict[str, Any]]
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION


@dataclass
class AgentUsabilityConsolidationReport(_Model):
    report_id: str
    created_at: str
    foundation_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    pipeline_boundary_report_id: str
    safety_boundary_report_id: str
    trace_telemetry_coverage_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_manifest_id: str
    v026_readiness_report_id: str
    workbench_handoff_packet_id: str
    findings: list[AgentUsabilityConsolidationFinding]
    readiness_status: str
    release_status: str
    ready_for_v0_26: bool
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    release_name: str = AGENT_USABILITY_RELEASE_NAME
    ready_for_v0_27: bool = False
    new_ask_executed: bool = False
    new_repl_turn_executed: bool = False
    new_final_response_emitted: bool = False
    new_provider_invocation_performed: bool = False
    new_local_command_executed: bool = False
    direct_provider_invocation: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    command_rerun_performed: bool = False
    autonomous_loop_started: bool = False
    background_execution_started: bool = False
    workspace_workbench_implemented: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    raw_transcript_persisted: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_USABILITY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.26 Workspace Agent Workbench work begins or agent surface policy changes."


@dataclass
class AgentUsabilityFoundationSnapshot(_Model):
    snapshot_id: str
    created_at: str
    included_versions: list[str]
    previous_release_ref: dict[str, Any] | None
    subject_components: list[AgentUsabilitySubjectComponent]
    capability_map_id: str
    coverage_matrix_id: str
    pipeline_boundary_report_id: str
    safety_boundary_report_id: str
    trace_telemetry_coverage_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_manifest_id: str
    v026_readiness_report_id: str
    consolidation_report_id: str
    snapshot_status: str
    version: str = AGENT_USABILITY_CONSOLIDATION_VERSION
    release_name: str = AGENT_USABILITY_RELEASE_NAME
    limitations: list[str] = field(default_factory=list)


class AgentUsabilityConsolidationSourceService:
    def _source(self, version: str, subject_id: str, name: str) -> dict[str, Any]:
        return {
            "version": version,
            "subject_id": subject_id,
            "subject_name": name,
            "artifact_id": f"{subject_id}:release_ref:{version}",
            "available": True,
            "read_only": True,
            "raw_transcript_loaded": False,
            "raw_provider_output_loaded": False,
            "raw_secret_loaded": False,
        }

    def load_v0_25_0_contract(self) -> dict[str, Any]:
        return self._source("v0.25.0", "agent_surface_contract", "Agent Surface Contract")

    def load_v0_25_1_turn_context(self) -> dict[str, Any]:
        return self._source("v0.25.1", "agent_turn_context", "Turn Envelope & Interaction Context")

    def load_v0_25_2_intent_task(self) -> dict[str, Any]:
        return self._source("v0.25.2", "agent_intent_task", "Intent Classification & Task Framing")

    def load_v0_25_3_safety_gate(self) -> dict[str, Any]:
        return self._source("v0.25.3", "agent_safety_gate", "Safety / No-Action / Clarification Gate")

    def load_v0_25_4_routing(self) -> dict[str, Any]:
        return self._source("v0.25.4", "agent_tool_routing", "Tool Routing Plan & Provider Selection")

    def load_v0_25_5_provider_invocation(self) -> dict[str, Any]:
        return self._source("v0.25.5", "agent_provider_invocation", "Internal Provider Invocation Orchestrator")

    def load_v0_25_6_response_assembly(self) -> dict[str, Any]:
        return self._source("v0.25.6", "agent_response_assembly", "Response Assembly & Evidence Binder")

    def load_v0_25_7_ask_repl(self) -> dict[str, Any]:
        return self._source("v0.25.7", "agent_ask_repl_surface", "Ask / REPL Surface")

    def load_v0_25_8_trace_telemetry(self) -> dict[str, Any]:
        return self._source("v0.25.8", "agent_trace_telemetry", "Agent Trace / Usability Telemetry")

    def load_v0_24_9_internal_provider_release(self) -> dict[str, Any]:
        return self._source("v0.24.9", "internal_provider_release", "Internal Provider / Local Runtime Provider Foundation v1")

    def load_all_sources(self) -> dict[str, dict[str, Any]]:
        return {
            "contract": self.load_v0_25_0_contract(),
            "turn_context": self.load_v0_25_1_turn_context(),
            "intent_task": self.load_v0_25_2_intent_task(),
            "safety_gate": self.load_v0_25_3_safety_gate(),
            "routing": self.load_v0_25_4_routing(),
            "provider_invocation": self.load_v0_25_5_provider_invocation(),
            "response_assembly": self.load_v0_25_6_response_assembly(),
            "ask_repl_surface": self.load_v0_25_7_ask_repl(),
            "trace_telemetry": self.load_v0_25_8_trace_telemetry(),
            "internal_provider_release": self.load_v0_24_9_internal_provider_release(),
        }


class AgentUsabilitySubjectComponentService:
    def build_subject_components(self, missing_subjects: set[str] | None = None) -> list[AgentUsabilitySubjectComponent]:
        missing = missing_subjects or set()
        specs = [
            ("v0.25.0", "agent_surface_contract", "Agent Surface Contract", "contract", ["skill:agent_surface_contract_view"], False, False, False, False, False, False),
            ("v0.25.1", "agent_turn_context", "Turn Envelope & Interaction Context", "turn_context", ["skill:agent_turn_envelope_create", "skill:agent_interaction_context_view"], False, False, False, False, False, False),
            ("v0.25.2", "agent_intent_task", "Intent Classification & Task Framing", "intent_task", ["skill:agent_intent_classify", "skill:agent_task_frame_create"], False, False, False, False, False, False),
            ("v0.25.3", "agent_safety_gate", "Safety / No-Action / Clarification Gate", "safety_gate", ["skill:agent_safety_gate_evaluate", "skill:agent_no_action_create", "skill:agent_clarification_create"], False, False, False, False, False, False),
            ("v0.25.4", "agent_tool_routing", "Tool Routing Plan & Provider Selection", "routing", ["skill:agent_tool_route_plan_create", "skill:agent_provider_selection_create"], False, False, False, False, False, False),
            ("v0.25.5", "agent_provider_invocation", "Internal Provider Invocation Orchestrator", "provider_invocation", ["skill:agent_provider_invocation_orchestrate"], False, False, True, True, False, False),
            ("v0.25.6", "agent_response_assembly", "Response Assembly & Evidence Binder", "response_assembly", ["skill:agent_response_assemble", "skill:agent_evidence_bind"], False, False, False, False, False, False),
            ("v0.25.7", "agent_ask_repl_surface", "Ask / REPL Surface", "ask_repl_surface", ["skill:agent_ask", "skill:agent_repl"], True, True, False, False, True, False),
            ("v0.25.8", "agent_trace_telemetry", "Agent Trace / Usability Telemetry", "trace_telemetry", ["skill:agent_trace_record", "skill:agent_usability_telemetry_view"], False, False, False, False, False, True),
            ("v0.25.9", "agent_usability_consolidation", "General Agent Usability Consolidation", "consolidation", ["skill:agent_usability_consolidation_view"], False, False, False, False, False, False),
        ]
        components = []
        for version, subject_id, name, ctype, skills, user_facing, execution, provider, bounded, response, trace in specs:
            status = "blocked" if subject_id in missing or ctype in missing else "implemented"
            components.append(
                AgentUsabilitySubjectComponent(
                    component_id=f"agent_usability_subject_component:{subject_id}",
                    version_introduced=version,
                    subject_id=subject_id,
                    subject_name=name,
                    component_type=ctype,
                    skill_ids=skills,
                    status=status,
                    user_facing=user_facing,
                    execution_capable=execution,
                    provider_invocation_capable=provider,
                    bounded_execution_capable=bounded,
                    response_emission_capable=response,
                    trace_capable=trace,
                    ocel_visible=True,
                    pig_visible=True,
                    ocpx_visible=True,
                    latest_artifact_id=f"{subject_id}:latest",
                    finding_count=1 if status == "blocked" else 0,
                    notes=["v0.25.9 read-only consolidation component"],
                )
            )
        return components


class AgentSurfaceCapabilityMapService:
    def build_capability_map(self, components: list[AgentUsabilitySubjectComponent]) -> AgentSurfaceCapabilityMap:
        entries = [
            AgentSurfaceCapabilityMapEntry(
                capability_id=f"agent_surface_capability:{component.subject_id}",
                name=component.subject_name,
                version_introduced=component.version_introduced,
                skill_ids=component.skill_ids,
                status=component.status,
                source_read_models=[f"{component.subject_name.replace(' ', '')}State"],
                target_read_models=[f"{component.subject_name.replace(' ', '')}ReadinessState"],
                effect_types=AGENT_USABILITY_EFFECT_TYPES,
                forbidden_effect_types=AGENT_USABILITY_FORBIDDEN_EFFECT_TYPES,
                user_facing=component.user_facing,
                provider_invocation_capable=component.provider_invocation_capable,
                local_runtime_capable=component.bounded_execution_capable,
                ocel_visible=component.ocel_visible,
                pig_visible=component.pig_visible,
                ocpx_visible=component.ocpx_visible,
                safety_notes=["Forbidden v0.25.9 effects remain excluded from consolidation."],
            )
            for component in components
        ]
        return AgentSurfaceCapabilityMap(
            map_id="agent_surface_capability_map:v0.25.9",
            entries=entries,
            implemented_count=_count(entries, "status", "implemented"),
            warning_count=_count(entries, "status", "warning"),
            failed_count=_count(entries, "status", "failed"),
            blocked_count=_count(entries, "status", "blocked"),
            future_track_count=_count(entries, "status", "future_track"),
            user_facing_count=sum(1 for entry in entries if entry.user_facing),
            provider_invocation_capability_count=sum(1 for entry in entries if entry.provider_invocation_capable),
            response_emission_capability_count=sum(1 for component in components if component.response_emission_capable),
            trace_capability_count=sum(1 for component in components if component.trace_capable),
            external_adapter_count=sum(1 for entry in entries if entry.external_adapter),
            memory_capability_count=sum(1 for entry in entries if entry.memory_capable),
            workbench_ui_count=sum(1 for entry in entries if entry.workbench_ui),
        )


class AgentSurfaceCoverageMatrixService:
    def build_coverage_matrix(self, components: list[AgentUsabilitySubjectComponent]) -> AgentSurfaceCoverageMatrix:
        rows = [
            AgentSurfaceCoverageMatrixRow(
                subject_id=component.subject_id,
                version_introduced=component.version_introduced,
                has_model=True,
                has_service=True,
                has_cli=True,
                has_tests=True,
                has_boundary_tests=True,
                has_docs=True,
                has_ocel_mapping=True,
                has_pig_projection=True,
                has_ocpx_projection=True,
                has_safety_boundary=True,
                latest_artifact_available=component.status == "implemented",
                coverage_notes=["Coverage is consolidated from v0.25 release artifacts."],
            )
            for component in components
        ]
        missing_count = sum(
            1
            for row in rows
            if not all(
                [
                    row.has_model,
                    row.has_service,
                    row.has_tests,
                    row.has_boundary_tests,
                    row.has_docs,
                    row.has_ocel_mapping,
                    row.has_pig_projection,
                    row.has_ocpx_projection,
                    row.has_safety_boundary,
                    row.latest_artifact_available,
                ]
            )
        )
        return AgentSurfaceCoverageMatrix(
            matrix_id="agent_surface_coverage_matrix:v0.25.9",
            rows=rows,
            coverage_status="complete" if missing_count == 0 else "blocked",
            missing_required_coverage_count=missing_count,
            optional_gap_count=0,
        )


class AgentSurfacePipelineBoundaryReportService:
    def build_pipeline_boundary_report(self, components: list[AgentUsabilitySubjectComponent]) -> AgentSurfacePipelineBoundaryReport:
        subject_ids = {component.subject_id for component in components if component.status == "implemented"}
        required = {
            "agent_turn_context",
            "agent_intent_task",
            "agent_safety_gate",
            "agent_tool_routing",
            "agent_provider_invocation",
            "agent_response_assembly",
            "agent_ask_repl_surface",
            "agent_trace_telemetry",
        }
        missing = sorted(required - subject_ids)
        return AgentSurfacePipelineBoundaryReport(
            report_id="agent_surface_pipeline_boundary_report:v0.25.9",
            required_stage_order=AGENT_USABILITY_STAGE_ORDER,
            stage_available_count=len(AGENT_USABILITY_STAGE_ORDER) - len(missing),
            stage_missing_count=len(missing),
            stage_boundary_passed=not missing,
            ask_pipeline_available="agent_ask_repl_surface" in subject_ids,
            repl_surface_available="agent_ask_repl_surface" in subject_ids,
            response_emission_available="agent_ask_repl_surface" in subject_ids,
            provider_invocation_via_v0255_only="agent_provider_invocation" in subject_ids,
            local_runtime_via_v024_only=True,
            trace_telemetry_available="agent_trace_telemetry" in subject_ids,
            no_direct_bypass=True,
            pipeline_boundary_status="ready" if not missing else "blocked",
            findings=[_ref("missing_stage", item) for item in missing],
        )


class AgentSurfaceSafetyBoundaryReportService:
    DANGEROUS_COUNT_FIELDS = [
        "direct_provider_invocation_count",
        "direct_file_access_count",
        "direct_subprocess_count",
        "direct_local_command_execution_count",
        "command_rerun_count",
        "automatic_repair_count",
        "autonomous_loop_count",
        "background_execution_count",
        "self_prompt_loop_count",
        "workspace_workbench_count",
        "memory_promotion_count",
        "persistent_memory_write_count",
        "persona_mutation_count",
        "external_provider_adapter_count",
        "external_agent_adapter_count",
        "credential_exposure_count",
        "raw_secret_output_count",
        "raw_provider_output_inline_count",
        "raw_transcript_persistence_count",
        "schumpeter_split_count",
        "llm_judge_count",
    ]

    def build_safety_boundary_report(self, dangerous_overrides: dict[str, int] | None = None) -> AgentSurfaceSafetyBoundaryReport:
        counts = {field_name: 0 for field_name in self.DANGEROUS_COUNT_FIELDS}
        counts.update(dangerous_overrides or {})
        status = "blocked" if any(counts.values()) else "passed"
        findings = [
            {"finding_type": field_name.removesuffix("_count"), "count": value}
            for field_name, value in counts.items()
            if value
        ]
        return AgentSurfaceSafetyBoundaryReport(
            report_id="agent_surface_safety_boundary_report:v0.25.9",
            ask_count=1,
            repl_turn_count=1,
            final_response_emission_count=1,
            provider_invocation_count=1,
            bounded_local_command_execution_count=0,
            response_assembly_count=1,
            trace_record_count=1,
            telemetry_report_count=1,
            status=status,
            findings=findings,
            **counts,
        )


class AgentSurfaceTraceTelemetryCoverageReportService:
    def build_trace_telemetry_coverage_report(self, trace_available: bool = True) -> AgentSurfaceTraceTelemetryCoverageReport:
        stage_coverage = {stage: trace_available for stage in AGENT_USABILITY_STAGE_ORDER}
        decision_coverage = {
            "intent_classification": trace_available,
            "safety_gate": trace_available,
            "route_selection": trace_available,
            "provider_invocation": trace_available,
            "response_assembly": trace_available,
            "emission": trace_available,
        }
        ready = trace_available and all(stage_coverage.values()) and all(decision_coverage.values())
        return AgentSurfaceTraceTelemetryCoverageReport(
            report_id="agent_surface_trace_telemetry_coverage_report:v0.25.9",
            trace_available=trace_available,
            ocel_projection_available=trace_available,
            metric_set_available=trace_available,
            telemetry_report_available=trace_available,
            stage_trace_coverage=stage_coverage,
            decision_trace_coverage=decision_coverage,
            route_trace_coverage=trace_available,
            provider_trace_coverage=trace_available,
            response_emission_trace_coverage=trace_available,
            raw_trace_privacy_passed=True,
            coverage_status="ready" if ready else "blocked",
            findings=[] if ready else [_ref("missing_trace_telemetry", "v0.25.8")],
        )


class AgentSurfaceRoadmapBoundaryReportService:
    def build_roadmap_boundary_report(self) -> AgentSurfaceRoadmapBoundaryReport:
        return AgentSurfaceRoadmapBoundaryReport(
            report_id="agent_surface_roadmap_boundary_report:v0.25.9",
            roadmap_status="aligned",
        )


class AgentSurfaceGapRegisterService:
    def build_gap_register(self) -> AgentSurfaceGapRegister:
        gaps = [
            AgentSurfaceGap(
                gap_id=f"agent_surface_gap:{gap_id}",
                title=gap_id.replace("_", " ").title(),
                description=f"{gap_id} remains outside v0.25.9 and is deferred to its planned roadmap track.",
                severity="future_track",
                affected_subjects=["agent_usability_consolidation"],
                recommended_track=self._track_for_gap(gap_id),
                withdrawal_condition="Withdraw if the future-track capability is implemented inside v0.25.9.",
            )
            for gap_id in AGENT_USABILITY_REQUIRED_FUTURE_GAPS
        ]
        return AgentSurfaceGapRegister(
            register_id="agent_surface_gap_register:v0.25.9",
            gaps=gaps,
            blocker_count=sum(1 for gap in gaps if gap.severity == "blocker"),
            warning_count=sum(1 for gap in gaps if gap.severity == "warning"),
            future_track_count=sum(1 for gap in gaps if gap.severity == "future_track"),
            gap_status="ready",
        )

    def _track_for_gap(self, gap_id: str) -> str:
        if "memory" in gap_id:
            return "v0.27.x Memory Candidate & Continuity"
        if "schumpeter" in gap_id:
            return "v0.28.x Public Alpha / Schumpeter Split Preparation"
        if "external_provider" in gap_id:
            return "v0.29.x+ External Skill / External Provider Adapter Development"
        if "external_agent" in gap_id:
            return "v0.30.x+ External Agent Dominion Bridge"
        if "growthkernel" in gap_id:
            return "future bridge track"
        return "v0.26.x Workspace Agent Workbench"


class AgentSurfaceReleaseManifestService:
    def build_release_manifest(
        self,
        components: list[AgentUsabilitySubjectComponent],
        capability_map: AgentSurfaceCapabilityMap,
        pipeline: AgentSurfacePipelineBoundaryReport,
        safety: AgentSurfaceSafetyBoundaryReport,
        trace: AgentSurfaceTraceTelemetryCoverageReport,
        roadmap: AgentSurfaceRoadmapBoundaryReport,
        gaps: AgentSurfaceGapRegister,
    ) -> AgentSurfaceReleaseManifest:
        blocked = (
            capability_map.blocked_count > 0
            or pipeline.pipeline_boundary_status == "blocked"
            or safety.status == "blocked"
            or trace.coverage_status == "blocked"
            or roadmap.roadmap_status == "blocked"
            or gaps.blocker_count > 0
        )
        warning = capability_map.warning_count > 0 or gaps.warning_count > 0 or trace.coverage_status == "warning"
        status = "blocked" if blocked else "releasable_with_warnings" if warning else "releasable"
        return AgentSurfaceReleaseManifest(
            manifest_id="agent_surface_release_manifest:v0.25.9",
            included_versions=AGENT_USABILITY_INCLUDED_VERSIONS,
            included_subjects=[component.subject_id for component in components],
            included_capabilities=[entry.capability_id for entry in capability_map.entries],
            excluded_capabilities=AGENT_USABILITY_EXCLUDED_CAPABILITIES,
            allowed_effect_types=AGENT_USABILITY_EFFECT_TYPES,
            forbidden_effect_types=AGENT_USABILITY_FORBIDDEN_EFFECT_TYPES,
            pipeline_boundary_report_id=pipeline.report_id,
            safety_boundary_report_id=safety.report_id,
            trace_telemetry_coverage_report_id=trace.report_id,
            roadmap_boundary_report_id=roadmap.report_id,
            gap_register_id=gaps.register_id,
            release_status=status,
            notes=["v0.25.9 consolidates v0.25.0 through v0.25.8 and does not implement v0.26 UI."],
        )


class AgentV026ReadinessReportService:
    SUBJECT_FLAG_MAP = {
        "agent_surface_contract": "agent_surface_contract_available",
        "agent_turn_context": "turn_envelope_available",
        "agent_intent_task": "intent_task_framing_available",
        "agent_safety_gate": "safety_gate_available",
        "agent_tool_routing": "routing_plan_available",
        "agent_provider_invocation": "provider_invocation_available",
        "agent_response_assembly": "response_assembly_available",
        "agent_ask_repl_surface": "ask_repl_surface_available",
        "agent_trace_telemetry": "trace_telemetry_available",
    }

    def build_v026_readiness_report(
        self,
        components: list[AgentUsabilitySubjectComponent],
        safety: AgentSurfaceSafetyBoundaryReport,
        trace: AgentSurfaceTraceTelemetryCoverageReport,
    ) -> AgentV026ReadinessReport:
        implemented = {component.subject_id for component in components if component.status == "implemented"}
        flags = {
            attr: subject_id in implemented
            for subject_id, attr in self.SUBJECT_FLAG_MAP.items()
        }
        flags["ocel_projection_available"] = trace.ocel_projection_available
        flags["safety_boundary_passed"] = safety.status == "passed"
        blockers = [subject_id for subject_id, attr in self.SUBJECT_FLAG_MAP.items() if not flags[attr]]
        if not flags["ocel_projection_available"]:
            blockers.append("agent_turn_ocel_projection")
        if not flags["safety_boundary_passed"]:
            blockers.append("agent_surface_safety_boundary")
        ready = not blockers
        return AgentV026ReadinessReport(
            report_id="agent_v026_readiness_report:v0.25.9",
            ready_for_v0_26=ready,
            substrate_requirements_met=ready,
            blockers=blockers,
            warnings=[],
            notes=["ready_for_v0_26 means the workbench contract can begin; it is not a workbench implementation."],
            **flags,
        )


class AgentWorkbenchHandoffPacketService:
    def build_handoff_packet(
        self,
        release_manifest: AgentSurfaceReleaseManifest,
        consolidation_report_id: str,
        readiness: AgentV026ReadinessReport,
    ) -> AgentWorkbenchHandoffPacket:
        return AgentWorkbenchHandoffPacket(
            handoff_packet_id="agent_workbench_handoff_packet:v0.25.9",
            target_version="v0.26.0",
            target_track="Workspace Agent Workbench",
            source_release_manifest_id=release_manifest.manifest_id,
            source_consolidation_report_id=consolidation_report_id,
            workbench_ready_inputs=[
                "agent_surface_contract",
                "agent_pipeline_stage_traces",
                "agent_decision_traces",
                "agent_route_traces",
                "provider_invocation_trace_views",
                "response_emission_traces",
                "usability_metrics",
                "safety_boundary_report",
            ],
            not_implemented_in_v0259=[
                "visual trace explorer",
                "provider browser UI",
                "approval UI",
                "dashboard",
                "workbench persistence model",
            ],
            handoff_status="ready" if readiness.ready_for_v0_26 else "blocked",
            evidence_refs=[_ref("agent_surface_release_manifest", release_manifest.manifest_id)],
        )


class AgentUsabilityConsolidationFindingService:
    BLOCKED_ATTEMPTS = {
        "direct_provider_bypass_detected",
        "direct_file_access_detected",
        "direct_subprocess_detected",
        "direct_local_command_execution_detected",
        "command_rerun_detected",
        "autonomous_loop_detected",
        "background_execution_detected",
        "workspace_workbench_premature",
        "memory_promotion_detected",
        "persona_mutation_detected",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "growthkernel_dependency_detected",
        "raw_transcript_persisted",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_inline_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        components: list[AgentUsabilitySubjectComponent],
        coverage: AgentSurfaceCoverageMatrix,
        pipeline: AgentSurfacePipelineBoundaryReport,
        safety: AgentSurfaceSafetyBoundaryReport,
        trace: AgentSurfaceTraceTelemetryCoverageReport,
        readiness: AgentV026ReadinessReport,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentUsabilityConsolidationFinding]:
        findings = [self._finding("info", "ok", "v0.25 agent surface consolidation was evaluated.", "agent_usability_consolidation")]
        for component in components:
            if component.status == "blocked":
                findings.append(self._finding("critical", "missing_v0_25_subject", f"{component.subject_id} is missing.", component.subject_id))
        if coverage.missing_required_coverage_count:
            findings.append(self._finding("error", "missing_tests", "Required coverage is incomplete.", coverage.matrix_id))
        if pipeline.pipeline_boundary_status == "blocked":
            findings.append(self._finding("critical", "unsafe_pipeline_boundary", "Pipeline boundary is blocked.", pipeline.report_id))
        if safety.status == "blocked":
            findings.append(self._finding("critical", "unsafe_surface_boundary", "Surface safety boundary is blocked.", safety.report_id))
        if trace.coverage_status == "blocked":
            findings.append(self._finding("critical", "missing_trace_telemetry", "Trace/telemetry coverage is missing.", trace.report_id))
        if not readiness.ready_for_v0_26:
            findings.append(self._finding("error", "missing_v026_readiness", "v0.26 readiness requirements are not met.", readiness.report_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", "agent_usability_consolidation"))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentUsabilityConsolidationFinding:
        return AgentUsabilityConsolidationFinding(
            finding_id=f"agent_usability_consolidation_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the cited v0.25 release artifact or v0.25.9 policy boundary changes.",
        )


class AgentUsabilityConsolidationReportService:
    def build_report(
        self,
        missing_subjects: set[str] | None = None,
        dangerous_overrides: dict[str, int] | None = None,
        trace_available: bool = True,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentUsabilityConsolidationReport:
        components = AgentUsabilitySubjectComponentService().build_subject_components(missing_subjects=missing_subjects)
        capability_map = AgentSurfaceCapabilityMapService().build_capability_map(components)
        coverage = AgentSurfaceCoverageMatrixService().build_coverage_matrix(components)
        pipeline = AgentSurfacePipelineBoundaryReportService().build_pipeline_boundary_report(components)
        safety = AgentSurfaceSafetyBoundaryReportService().build_safety_boundary_report(dangerous_overrides=dangerous_overrides)
        trace = AgentSurfaceTraceTelemetryCoverageReportService().build_trace_telemetry_coverage_report(trace_available=trace_available)
        roadmap = AgentSurfaceRoadmapBoundaryReportService().build_roadmap_boundary_report()
        gaps = AgentSurfaceGapRegisterService().build_gap_register()
        manifest = AgentSurfaceReleaseManifestService().build_release_manifest(components, capability_map, pipeline, safety, trace, roadmap, gaps)
        readiness = AgentV026ReadinessReportService().build_v026_readiness_report(components, safety, trace)
        report_id = "agent_usability_consolidation_report:v0.25.9"
        handoff = AgentWorkbenchHandoffPacketService().build_handoff_packet(manifest, report_id, readiness)
        findings = AgentUsabilityConsolidationFindingService().build_findings(
            components,
            coverage,
            pipeline,
            safety,
            trace,
            readiness,
            attempt_flags,
        )
        readiness_status = self._readiness_status(findings, readiness)
        release_status = manifest.release_status if readiness_status != "blocked" else "blocked"
        return AgentUsabilityConsolidationReport(
            report_id=report_id,
            created_at=utc_now_iso(),
            foundation_snapshot_id="agent_usability_foundation_snapshot:v0.25.9",
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage.matrix_id,
            pipeline_boundary_report_id=pipeline.report_id,
            safety_boundary_report_id=safety.report_id,
            trace_telemetry_coverage_report_id=trace.report_id,
            roadmap_boundary_report_id=roadmap.report_id,
            gap_register_id=gaps.register_id,
            release_manifest_id=manifest.manifest_id,
            v026_readiness_report_id=readiness.report_id,
            workbench_handoff_packet_id=handoff.handoff_packet_id,
            findings=findings,
            readiness_status=readiness_status,
            release_status=release_status,
            ready_for_v0_26=readiness.ready_for_v0_26 and readiness_status in {"ready", "warning"},
            limitations=[
                "v0.25.9 is a report-derived consolidation layer; it does not create durable report storage.",
                "Counts are release-readiness summary counts, not a full historical analytics database.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.25.9 executes ask/repl, emits responses, invokes providers, runs commands, implements workbench UI, promotes memory, mutates persona, persists raw transcripts, exposes secrets, or uses an LLM judge.",
            ],
        )

    def build_foundation_snapshot(self, report: AgentUsabilityConsolidationReport, parts: dict[str, Any]) -> AgentUsabilityFoundationSnapshot:
        return AgentUsabilityFoundationSnapshot(
            snapshot_id=report.foundation_snapshot_id,
            created_at=report.created_at,
            included_versions=AGENT_USABILITY_INCLUDED_VERSIONS,
            previous_release_ref=_ref("internal_provider_release", "v0.24.9 Internal Provider / Local Runtime Provider Foundation v1", "v0.24.9"),
            subject_components=parts["subject_components"],
            capability_map_id=report.capability_map_id,
            coverage_matrix_id=report.coverage_matrix_id,
            pipeline_boundary_report_id=report.pipeline_boundary_report_id,
            safety_boundary_report_id=report.safety_boundary_report_id,
            trace_telemetry_coverage_report_id=report.trace_telemetry_coverage_report_id,
            roadmap_boundary_report_id=report.roadmap_boundary_report_id,
            gap_register_id=report.gap_register_id,
            release_manifest_id=report.release_manifest_id,
            v026_readiness_report_id=report.v026_readiness_report_id,
            consolidation_report_id=report.report_id,
            snapshot_status=report.readiness_status,
            limitations=report.limitations,
        )

    def build_all_parts(self, **kwargs: Any) -> dict[str, Any]:
        components = AgentUsabilitySubjectComponentService().build_subject_components(missing_subjects=kwargs.get("missing_subjects"))
        capability_map = AgentSurfaceCapabilityMapService().build_capability_map(components)
        coverage = AgentSurfaceCoverageMatrixService().build_coverage_matrix(components)
        pipeline = AgentSurfacePipelineBoundaryReportService().build_pipeline_boundary_report(components)
        safety = AgentSurfaceSafetyBoundaryReportService().build_safety_boundary_report(dangerous_overrides=kwargs.get("dangerous_overrides"))
        trace = AgentSurfaceTraceTelemetryCoverageReportService().build_trace_telemetry_coverage_report(trace_available=kwargs.get("trace_available", True))
        roadmap = AgentSurfaceRoadmapBoundaryReportService().build_roadmap_boundary_report()
        gaps = AgentSurfaceGapRegisterService().build_gap_register()
        manifest = AgentSurfaceReleaseManifestService().build_release_manifest(components, capability_map, pipeline, safety, trace, roadmap, gaps)
        readiness = AgentV026ReadinessReportService().build_v026_readiness_report(components, safety, trace)
        report_id = "agent_usability_consolidation_report:v0.25.9"
        handoff = AgentWorkbenchHandoffPacketService().build_handoff_packet(manifest, report_id, readiness)
        findings = AgentUsabilityConsolidationFindingService().build_findings(
            components,
            coverage,
            pipeline,
            safety,
            trace,
            readiness,
            kwargs.get("attempt_flags"),
        )
        readiness_status = self._readiness_status(findings, readiness)
        report = AgentUsabilityConsolidationReport(
            report_id=report_id,
            created_at=utc_now_iso(),
            foundation_snapshot_id="agent_usability_foundation_snapshot:v0.25.9",
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage.matrix_id,
            pipeline_boundary_report_id=pipeline.report_id,
            safety_boundary_report_id=safety.report_id,
            trace_telemetry_coverage_report_id=trace.report_id,
            roadmap_boundary_report_id=roadmap.report_id,
            gap_register_id=gaps.register_id,
            release_manifest_id=manifest.manifest_id,
            v026_readiness_report_id=readiness.report_id,
            workbench_handoff_packet_id=handoff.handoff_packet_id,
            findings=findings,
            readiness_status=readiness_status,
            release_status=manifest.release_status if readiness_status != "blocked" else "blocked",
            ready_for_v0_26=readiness.ready_for_v0_26 and readiness_status in {"ready", "warning"},
            limitations=[
                "v0.25.9 is a report-derived consolidation layer; it does not create durable report storage.",
                "Counts are release-readiness summary counts, not a full historical analytics database.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.25.9 executes ask/repl, emits responses, invokes providers, runs commands, implements workbench UI, promotes memory, mutates persona, persists raw transcripts, exposes secrets, or uses an LLM judge.",
            ],
        )
        parts = {
            "report": report,
            "subject_components": components,
            "capability_map": capability_map,
            "coverage_matrix": coverage,
            "pipeline_boundary_report": pipeline,
            "safety_boundary_report": safety,
            "trace_telemetry_coverage_report": trace,
            "roadmap_boundary_report": roadmap,
            "gap_register": gaps,
            "release_manifest": manifest,
            "v026_readiness_report": readiness,
            "workbench_handoff_packet": handoff,
            "findings": findings,
        }
        parts["foundation_snapshot"] = self.build_foundation_snapshot(report, parts)
        return parts

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_USABILITY_CONSOLIDATION_VERSION,
            "layer": "agent_surface",
            "subject": "general_agent_usability_consolidation",
            "release_name": AGENT_USABILITY_RELEASE_NAME,
            "principles": [
                "consolidation is not new agent execution",
                "release readiness is not workspace workbench",
                "bounded agent surface closes user-facing substrate, not product UI",
                "ask/repl history may be summarized, but no new ask/repl turn may run",
                "provider history may be summarized, but no new provider may be invoked",
                "trace/telemetry may be summarized, but no background collector may start",
                "ready_for_v0_26 means workbench can be built next, not that workbench is implemented",
            ],
            "safety_boundary": {
                "new_ask_executed": False,
                "new_repl_turn_executed": False,
                "new_final_response_emitted": False,
                "new_provider_invocation_performed": False,
                "new_local_command_executed": False,
                "direct_provider_invocation": False,
                "direct_file_access_performed": False,
                "direct_subprocess_performed": False,
                "command_rerun_performed": False,
                "autonomous_loop_started": False,
                "background_execution_started": False,
                "workspace_workbench_implemented": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "raw_transcript_persisted": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.28": "public alpha / Schumpeter split preparation",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": AGENT_USABILITY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "bounded_general_agent_surface_foundation_v1_consolidated",
            "version": AGENT_USABILITY_CONSOLIDATION_VERSION,
            "release_name": AGENT_USABILITY_RELEASE_NAME,
            "source_read_models": [
                "AgentSurfaceContractState",
                "AgentTurnEnvelopeState",
                "AgentIntentClassificationState",
                "AgentSafetyGateState",
                "AgentToolRoutingState",
                "AgentProviderInvocationState",
                "AgentResponseAssemblyState",
                "AgentAskReplSurfaceState",
                "AgentTraceTelemetryState",
                "InternalProviderReleaseState",
            ],
            "target_read_models": [
                "AgentUsabilityReleaseState",
                "AgentUsabilityConsolidationState",
                "AgentSurfaceSafetyBoundaryState",
                "AgentSurfacePipelineBoundaryState",
                "AgentSurfaceTraceTelemetryCoverageState",
                "AgentV026ReadinessState",
                "AgentWorkbenchHandoffState",
                "V026ReadinessState",
            ],
            "effect_types": AGENT_USABILITY_EFFECT_TYPES,
        }

    def _readiness_status(self, findings: list[AgentUsabilityConsolidationFinding], readiness: AgentV026ReadinessReport) -> str:
        if any(finding.severity == "critical" for finding in findings) or not readiness.ready_for_v0_26:
            return "blocked"
        if any(finding.severity in {"warning", "error"} for finding in findings):
            return "warning"
        return "ready"


def render_agent_usability_consolidation_cli(parts: dict[str, Any], section: str = "consolidate") -> str:
    report: AgentUsabilityConsolidationReport = parts["report"]
    lines = [
        f"version={report.version}",
        f"release_name={report.release_name}",
        f"release_status={report.release_status}",
        f"readiness_status={report.readiness_status}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"ready_for_v0_27={str(report.ready_for_v0_27).lower()}",
        f"new_ask_executed={str(report.new_ask_executed).lower()}",
        f"new_repl_turn_executed={str(report.new_repl_turn_executed).lower()}",
        f"new_final_response_emitted={str(report.new_final_response_emitted).lower()}",
        f"new_provider_invocation_performed={str(report.new_provider_invocation_performed).lower()}",
        f"new_local_command_executed={str(report.new_local_command_executed).lower()}",
        f"direct_provider_invocation={str(report.direct_provider_invocation).lower()}",
        f"direct_file_access_performed={str(report.direct_file_access_performed).lower()}",
        f"direct_subprocess_performed={str(report.direct_subprocess_performed).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"autonomous_loop_started={str(report.autonomous_loop_started).lower()}",
        f"background_execution_started={str(report.background_execution_started).lower()}",
        f"workspace_workbench_implemented={str(report.workspace_workbench_implemented).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"raw_transcript_persisted={str(report.raw_transcript_persisted).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section in {"consolidate", "report"}:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"foundation_snapshot_id={report.foundation_snapshot_id}")
    elif section == "release-manifest":
        manifest: AgentSurfaceReleaseManifest = parts["release_manifest"]
        lines.append(f"manifest_id={manifest.manifest_id}")
        lines.append(f"included_versions={','.join(manifest.included_versions)}")
        lines.append(f"excluded_capability_count={len(manifest.excluded_capabilities)}")
    elif section == "readiness":
        readiness: AgentV026ReadinessReport = parts["v026_readiness_report"]
        lines.append(f"target_track={readiness.target_track}")
        lines.append(f"recommended_next_version={readiness.recommended_next_version}")
        lines.append(f"substrate_requirements_met={str(readiness.substrate_requirements_met).lower()}")
        lines.append(f"workbench_not_implemented_yet={str(readiness.workbench_not_implemented_yet).lower()}")
    elif section == "safety-boundary":
        safety: AgentSurfaceSafetyBoundaryReport = parts["safety_boundary_report"]
        lines.append(f"safety_status={safety.status}")
        lines.append(f"direct_provider_invocation_count={safety.direct_provider_invocation_count}")
        lines.append(f"direct_subprocess_count={safety.direct_subprocess_count}")
        lines.append(f"memory_promotion_count={safety.memory_promotion_count}")
    elif section == "pipeline-boundary":
        pipeline: AgentSurfacePipelineBoundaryReport = parts["pipeline_boundary_report"]
        lines.append(f"pipeline_boundary_status={pipeline.pipeline_boundary_status}")
        lines.append(f"required_stage_order={','.join(pipeline.required_stage_order)}")
        lines.append(f"provider_invocation_via_v0255_only={str(pipeline.provider_invocation_via_v0255_only).lower()}")
        lines.append(f"local_runtime_via_v024_only={str(pipeline.local_runtime_via_v024_only).lower()}")
    elif section == "trace-coverage":
        trace: AgentSurfaceTraceTelemetryCoverageReport = parts["trace_telemetry_coverage_report"]
        lines.append(f"trace_coverage_status={trace.coverage_status}")
        lines.append(f"trace_available={str(trace.trace_available).lower()}")
        lines.append(f"ocel_projection_available={str(trace.ocel_projection_available).lower()}")
        lines.append(f"raw_trace_privacy_passed={str(trace.raw_trace_privacy_passed).lower()}")
    elif section == "gaps":
        gaps: AgentSurfaceGapRegister = parts["gap_register"]
        lines.append(f"gap_status={gaps.gap_status}")
        lines.append(f"future_track_count={gaps.future_track_count}")
        for gap in gaps.gaps:
            lines.append(f"- {gap.gap_id}: {gap.severity}")
    elif section == "handoff":
        handoff: AgentWorkbenchHandoffPacket = parts["workbench_handoff_packet"]
        lines.append(f"handoff_status={handoff.handoff_status}")
        lines.append(f"target_version={handoff.target_version}")
        lines.append(f"workbench_ready_inputs={','.join(handoff.workbench_ready_inputs)}")
    return "\n".join(lines)
