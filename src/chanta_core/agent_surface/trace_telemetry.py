from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any

from chanta_core.agent_surface.ask_repl import (
    AgentAskPipelineResult,
    AgentAskPipelineRun,
    AgentAskPipelineStep,
    AgentAskPolicyService,
    AgentAskReplFinding,
    AgentAskReplReport,
    AgentAskRequest,
    AgentSurfaceEmission,
    AgentSurfaceSessionState,
    _dict_ref,
    _safe_id,
    _sanitize_text,
)
from chanta_core.utility.time import utc_now_iso


AGENT_TRACE_TELEMETRY_VERSION = "v0.25.8"
AGENT_TRACE_TELEMETRY_VERSION_NAME = "Agent Trace / Usability Telemetry"
AGENT_TRACE_TELEMETRY_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_TRACE_TELEMETRY_NEXT_STEP = "v0.25.9 General Agent Usability Consolidation"

AGENT_TRACE_STAGE_IDS = [
    "v0.25.1_turn_envelope",
    "v0.25.2_intent_task",
    "v0.25.3_safety_gate",
    "v0.25.4_route_plan",
    "v0.25.5_provider_invocation",
    "v0.25.6_response_assembly",
    "v0.25.7_surface_emission",
]

AGENT_TRACE_OBJECT_TYPES = [
    "agent_trace_policy",
    "agent_trace_request",
    "agent_trace_source_bundle",
    "agent_trace_event",
    "agent_trace_object_ref",
    "agent_trace_relation_ref",
    "agent_pipeline_stage_trace",
    "agent_decision_trace",
    "agent_route_trace",
    "agent_provider_invocation_trace_view",
    "agent_response_emission_trace",
    "agent_surface_trace",
    "agent_turn_ocel_projection_policy",
    "agent_turn_ocel_projection",
    "agent_usability_metric_definition",
    "agent_usability_metric_value",
    "agent_usability_metric_set",
    "agent_usability_telemetry_policy",
    "agent_usability_telemetry_report",
    "agent_trace_telemetry_finding",
    "agent_trace_telemetry_report",
    "agent_ask_repl_report",
    "agent_ask_pipeline_run",
    "agent_surface_emission",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_TRACE_EVENT_TYPES = [
    "agent_trace_requested",
    "agent_trace_policy_created",
    "agent_trace_source_bundle_created",
    "agent_trace_event_created",
    "agent_trace_object_ref_created",
    "agent_trace_relation_ref_created",
    "agent_pipeline_stage_trace_created",
    "agent_decision_trace_created",
    "agent_route_trace_created",
    "agent_provider_invocation_trace_view_created",
    "agent_response_emission_trace_created",
    "agent_surface_trace_created",
    "agent_turn_ocel_projection_policy_created",
    "agent_turn_ocel_projected",
    "agent_usability_metric_definition_created",
    "agent_usability_metric_value_created",
    "agent_usability_metric_set_created",
    "agent_usability_telemetry_policy_created",
    "agent_usability_telemetry_report_created",
    "agent_trace_telemetry_report_created",
    "agent_trace_telemetry_warning_created",
    "agent_trace_telemetry_blocked",
]

AGENT_TRACE_RELATION_TYPES = [
    "uses_agent_ask_repl_report",
    "uses_agent_pipeline_run",
    "uses_agent_surface_emission",
    "observes_agent_pipeline_stage",
    "observes_agent_decision",
    "observes_agent_route",
    "observes_provider_invocation_trace",
    "observes_response_emission",
    "creates_agent_surface_trace",
    "projects_agent_turn_to_ocel",
    "creates_usability_metric_definition",
    "computes_usability_metric_value",
    "creates_usability_metric_set",
    "creates_usability_telemetry_report",
    "prepares_general_agent_usability_consolidation",
    "defers_consolidation_to_v0_25_9",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_final_response_emitted",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_direct_file_access",
    "not_direct_subprocess",
    "not_command_rerun",
    "not_background_execution",
    "not_autonomous_optimization",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "recorded_in_envelope",
]

AGENT_TRACE_EFFECT_TYPES = [
    "read_only_observation",
    "agent_surface_trace_recorded",
    "agent_turn_ocel_projected",
    "agent_usability_metric_created",
    "agent_usability_telemetry_created",
    "state_candidate_created",
]

AGENT_TRACE_FORBIDDEN_EFFECT_TYPES = [
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

REQUIRED_USABILITY_METRICS = [
    "agent_turn_count",
    "ask_count",
    "repl_turn_count",
    "final_response_emission_count",
    "no_action_count",
    "clarification_count",
    "needs_more_input_count",
    "blocked_count",
    "deferred_count",
    "allow_route_count",
    "route_plan_count",
    "provider_invocation_count",
    "provider_warning_count",
    "provider_failed_count",
    "response_assembly_count",
    "unsupported_claim_count",
    "uncertainty_note_count",
    "limitation_note_count",
    "pipeline_completed_count",
    "pipeline_failed_count",
    "pipeline_blocked_count",
    "direct_bypass_count",
    "autonomous_loop_count",
    "background_execution_count",
    "memory_promotion_count",
    "credential_exposure_count",
    "raw_secret_output_count",
]


def _stage_id_for_trace(stage_id: str) -> str:
    value = stage_id.replace("_if_allow_route", "").replace("_if_required", "")
    return value


def _source_ref(ref_type: str, ref_id: str | None) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id or "missing", "version": AGENT_TRACE_TELEMETRY_VERSION}


@dataclass
class AgentTracePolicy:
    policy_id: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    layer: str = "agent_surface"
    trace_recording_enabled: bool = True
    telemetry_enabled: bool = True
    report_derived_only: bool = True
    raw_transcript_persistence_enabled: bool = False
    raw_provider_output_persistence_enabled: bool = False
    raw_secret_persistence_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    memory_promotion_enabled: bool = False
    persona_mutation_enabled: bool = False
    ask_execution_enabled: bool = False
    repl_execution_enabled: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    background_daemon_enabled: bool = False
    continuous_watcher_enabled: bool = False
    autonomous_optimization_enabled: bool = False
    workspace_workbench_enabled: bool = False
    external_provider_adapter_enabled: bool = False
    external_agent_adapter_enabled: bool = False
    ocel_projection_required: bool = True
    private_path_sanitization_required: bool = True
    credential_output_forbidden: bool = True
    raw_secret_output_forbidden: bool = True
    llm_judge_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceRequest:
    request_id: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    ask_repl_report_id: str | None = None
    ask_pipeline_run_id: str | None = None
    ask_pipeline_result_id: str | None = None
    repl_session_id: str | None = None
    repl_turn_result_id: str | None = None
    assembled_response_id: str | None = None
    include_usability_metrics: bool = True
    include_ocel_projection: bool = True
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceSourceBundle:
    source_bundle_id: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    ask_repl_report_ref: dict[str, Any] | None = None
    pipeline_run_ref: dict[str, Any] | None = None
    pipeline_result_ref: dict[str, Any] | None = None
    surface_emission_ref: dict[str, Any] | None = None
    turn_envelope_ref: dict[str, Any] | None = None
    intent_report_ref: dict[str, Any] | None = None
    safety_gate_report_ref: dict[str, Any] | None = None
    routing_report_ref: dict[str, Any] | None = None
    provider_invocation_report_ref: dict[str, Any] | None = None
    response_assembly_report_ref: dict[str, Any] | None = None
    source_count: int = 0
    source_status: str = "missing"
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    raw_provider_output_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceEvent:
    trace_event_id: str
    event_type: str
    timestamp: str | None
    stage_id: str | None
    source_ref: dict[str, Any] | None
    event_status: str
    sanitized: bool = True
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceObjectRef:
    object_ref_id: str
    object_type: str
    object_id: str | None
    source_version: str | None
    stage_id: str | None
    sanitized_label: str
    raw_content_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceRelationRef:
    relation_ref_id: str
    relation_type: str
    source_object_ref_id: str
    target_object_ref_id: str
    stage_id: str | None
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentPipelineStageTrace:
    stage_trace_id: str
    stage_id: str
    stage_name: str
    stage_status: str
    input_refs: list[dict[str, Any]]
    output_refs: list[dict[str, Any]]
    started_at: str | None
    ended_at: str | None
    duration_ms: int | None
    provider_invoked: bool
    local_command_executed: bool
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    direct_bypass_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentDecisionTrace:
    decision_trace_id: str
    decision_type: str
    decision_outcome: str
    decision_confidence: str | None
    source_ref: dict[str, Any] | None
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    deterministic: bool = True
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentRouteTrace:
    route_trace_id: str
    route_kind: str | None
    selected_provider_refs: list[dict[str, Any]]
    route_step_refs: list[dict[str, Any]]
    route_status: str
    provider_invocation_required: bool
    provider_invoked_via_v0255: bool
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationTraceView:
    provider_trace_view_id: str
    provider_invocation_report_ref: dict[str, Any] | None
    provider_result_refs: list[dict[str, Any]]
    provider_invoked_via_v0255: bool
    local_command_executed_via_v024: bool
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    direct_provider_invocation: bool = False
    direct_local_command_executed: bool = False
    raw_provider_output_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentResponseEmissionTrace:
    emission_trace_id: str
    assembled_response_ref: dict[str, Any] | None
    surface_emission_ref: dict[str, Any] | None
    response_assembled_via_v0256: bool
    final_response_emitted_via_v0257: bool
    response_status: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSurfaceTrace:
    surface_trace_id: str
    created_at: str
    source_bundle_id: str
    trace_events: list[AgentTraceEvent]
    object_refs: list[AgentTraceObjectRef]
    relation_refs: list[AgentTraceRelationRef]
    stage_traces: list[AgentPipelineStageTrace]
    decision_traces: list[AgentDecisionTrace]
    route_trace: AgentRouteTrace | None
    provider_trace_view: AgentProviderInvocationTraceView | None
    response_emission_trace: AgentResponseEmissionTrace | None
    trace_status: str
    ocel_projectable: bool
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    raw_transcript_included: bool = False
    raw_secret_included: bool = False
    raw_provider_output_included: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTurnOCELProjectionPolicy:
    policy_id: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    projection_enabled: bool = True
    mutate_original_artifacts: bool = False
    raw_transcript_projection_forbidden: bool = True
    raw_provider_output_projection_forbidden: bool = True
    raw_secret_projection_forbidden: bool = True
    include_stage_events: bool = True
    include_decision_events: bool = True
    include_provider_result_refs: bool = True
    include_response_emission_refs: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTurnOCELProjection:
    projection_id: str
    surface_trace_id: str
    object_types: list[str]
    event_types: list[str]
    relation_types: list[str]
    projected_object_count: int
    projected_event_count: int
    projected_relation_count: int
    projection_status: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    original_artifacts_mutated: bool = False
    raw_transcript_projected: bool = False
    raw_provider_output_projected: bool = False
    raw_secret_projected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUsabilityMetricDefinition:
    metric_id: str
    metric_name: str
    metric_category: str
    description: str
    value_type: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUsabilityMetricValue:
    metric_value_id: str
    metric_id: str
    value: int | float | bool | str | None
    unit: str | None
    source_refs: list[dict[str, Any]]
    computed: bool = True
    computation_method: str = "report_derived"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUsabilityMetricSet:
    metric_set_id: str
    metric_values: list[AgentUsabilityMetricValue]
    metric_count: int
    metric_set_status: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUsabilityTelemetryPolicy:
    policy_id: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    telemetry_enabled: bool = True
    descriptive_only: bool = True
    autonomous_optimization_enabled: bool = False
    background_collection_enabled: bool = False
    raw_transcript_collection_enabled: bool = False
    memory_promotion_enabled: bool = False
    external_reporting_enabled: bool = False
    privacy_sanitization_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentUsabilityTelemetryReport:
    telemetry_report_id: str
    created_at: str
    policy: AgentUsabilityTelemetryPolicy
    surface_trace_id: str
    metric_definitions: list[AgentUsabilityMetricDefinition]
    metric_set: AgentUsabilityMetricSet
    telemetry_status: str
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    descriptive_only: bool = True
    autonomous_optimization_performed: bool = False
    background_collection_started: bool = False
    memory_promoted: bool = False
    external_report_sent: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentTraceTelemetryFinding:
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
class AgentTraceTelemetryReport:
    report_id: str
    created_at: str
    trace_policy: AgentTracePolicy
    trace_request: AgentTraceRequest
    source_bundle: AgentTraceSourceBundle
    surface_trace: AgentSurfaceTrace
    projection_policy: AgentTurnOCELProjectionPolicy
    ocel_projection: AgentTurnOCELProjection
    telemetry_policy: AgentUsabilityTelemetryPolicy
    telemetry_report: AgentUsabilityTelemetryReport
    findings: list[AgentTraceTelemetryFinding]
    report_status: str
    ready_for_v0_25_9: bool
    trace_recorded: bool
    ocel_projected: bool
    telemetry_created: bool
    version: str = AGENT_TRACE_TELEMETRY_VERSION
    ready_for_v0_26: bool = False
    ask_executed: bool = False
    repl_executed: bool = False
    final_response_emitted: bool = False
    provider_invoked: bool = False
    local_command_executed: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    command_rerun_performed: bool = False
    background_collection_started: bool = False
    autonomous_optimization_performed: bool = False
    workspace_workbench_implemented: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    raw_transcript_persisted: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_TRACE_TELEMETRY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.9 consolidation begins or trace/telemetry policy changes."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentTracePrerequisiteSourceService:
    def load_ask_repl_report(self, ask_repl_report_id: str | None = None) -> AgentAskReplReport | None:
        if ask_repl_report_id == "missing":
            return None
        report_id = ask_repl_report_id or "agent_ask_repl_report:synthetic-existing"
        ask_request = AgentAskRequest(
            request_id="agent_ask_request:synthetic-existing",
            user_text="[sanitized prior user request reference]",
        )
        steps = self._synthetic_pipeline_steps(ask_request.request_id)
        run = AgentAskPipelineRun(
            pipeline_run_id="agent_ask_pipeline_run:synthetic-existing",
            ask_request_id=ask_request.request_id,
            steps=steps,
            started_at=utc_now_iso(),
            ended_at=utc_now_iso(),
            pipeline_status="completed",
            final_stage_id="v0.25.7_surface_emission",
            assembled_response_ref=_dict_ref("agent_assembled_response", "agent_assembled_response:synthetic-existing"),
            surface_emission_ref=_dict_ref("agent_surface_emission", "agent_surface_emission:synthetic-existing"),
        )
        result = AgentAskPipelineResult(
            pipeline_result_id="agent_ask_pipeline_result:synthetic-existing",
            pipeline_run_id=run.pipeline_run_id,
            primary_outcome="provider_backed_answer",
            assembled_response_id="agent_assembled_response:synthetic-existing",
            emission_id="agent_surface_emission:synthetic-existing",
            response_text=None,
            result_status="ready",
            evidence_bound=True,
            final_response_emitted=bool(1),
            provider_invoked_via_v0255=True,
            local_command_executed_via_v024=False,
        )
        emission = AgentSurfaceEmission(
            emission_id="agent_surface_emission:synthetic-existing",
            assembled_response_id="agent_assembled_response:synthetic-existing",
            response_text="[sanitized prior assembled response reference]",
            output_view_id="agent_surface_output_view:synthetic-existing",
            emitted_at=utc_now_iso(),
            emitted_to="test_fixture",
        )
        session_state = AgentSurfaceSessionState(
            surface_session_state_id="agent_surface_session_state:synthetic-existing",
            active_repl_sessions=0,
            total_ask_count=1,
            total_repl_turn_count=0,
            total_emission_count=1,
        )
        return AgentAskReplReport(
            report_id=report_id,
            created_at=utc_now_iso(),
            policy=AgentAskPolicyService().build_policy(),
            ask_request=ask_request,
            pipeline_run=run,
            pipeline_result=result,
            emission=emission,
            session_state=session_state,
            findings=[
                AgentAskReplFinding(
                    finding_id="agent_ask_repl_finding:ok",
                    severity="info",
                    finding_type="ok",
                    message="Synthetic persisted-reference ask report loaded for v0.25.8 trace tests.",
                    subject_ref={"id": report_id},
                    evidence_refs=[],
                )
            ],
            report_status="passed",
            ready_for_v0_25_8=True,
            ask_executed=bool(1),
            final_response_emitted=bool(1),
            response_assembled_via_v0256=True,
            provider_invoked_via_v0255=True,
        )

    def load_pipeline_run_if_available(self, report: AgentAskReplReport | None) -> AgentAskPipelineRun | None:
        return report.pipeline_run if report else None

    def load_pipeline_result_if_available(self, report: AgentAskReplReport | None) -> AgentAskPipelineResult | None:
        return report.pipeline_result if report else None

    def load_surface_emission_if_available(self, report: AgentAskReplReport | None) -> AgentSurfaceEmission | None:
        return report.emission if report else None

    def load_stage_reports_if_available(self, report: AgentAskReplReport | None) -> dict[str, dict[str, Any]]:
        if not report or not report.pipeline_run:
            return {}
        refs: dict[str, dict[str, Any]] = {}
        for step in report.pipeline_run.steps:
            stage_id = _stage_id_for_trace(step.stage_id)
            if step.output_refs:
                refs[stage_id] = step.output_refs[0]
        return refs

    def _synthetic_pipeline_steps(self, request_id: str) -> list[AgentAskPipelineStep]:
        raw = [
            ("v0.25.1_turn_envelope", "Create turn envelope", "agent_turn_report", "agent_turn_report:synthetic-existing"),
            ("v0.25.2_intent_task", "Classify intent and frame task", "agent_intent_classification_report", "agent_intent_classification_report:synthetic-existing"),
            ("v0.25.3_safety_gate", "Evaluate safety gate", "agent_safety_gate_report", "agent_safety_gate_report:synthetic-existing"),
            ("v0.25.4_route_plan_if_allow_route", "Create route plan", "agent_tool_routing_report", "agent_tool_routing_report:synthetic-existing"),
            ("v0.25.5_provider_invocation_if_required", "Observe provider invocation", "agent_provider_invocation_report", "agent_provider_invocation_report:synthetic-existing"),
            ("v0.25.6_response_assembly", "Observe response assembly", "agent_response_assembly_report", "agent_response_assembly_report:synthetic-existing"),
            ("v0.25.7_surface_emission", "Observe surface emission", "agent_surface_emission", "agent_surface_emission:synthetic-existing"),
        ]
        steps: list[AgentAskPipelineStep] = []
        previous = [_dict_ref("agent_ask_request", request_id)]
        for index, (stage_id, name, ref_type, ref_id) in enumerate(raw, start=1):
            output_refs = [_dict_ref(ref_type, ref_id)]
            steps.append(
                AgentAskPipelineStep(
                    pipeline_step_id=f"agent_ask_pipeline_step:synthetic-existing:{index}",
                    step_index=index,
                    stage_id=stage_id,
                    stage_name=name,
                    input_refs=previous,
                    output_refs=output_refs,
                    step_status="executed",
                    executed_now=True,
                    provider_invoked=stage_id.startswith("v0.25.5"),
                    local_command_executed=False,
                    response_assembled=stage_id.startswith("v0.25.6"),
                    final_response_emitted=stage_id.startswith("v0.25.7"),
                )
            )
            previous = output_refs
        return steps


class AgentTracePolicyService:
    def build_policy(self) -> AgentTracePolicy:
        return AgentTracePolicy(policy_id="agent_trace_policy:v0.25.8", evidence_refs=[{"type": "version", "value": AGENT_TRACE_TELEMETRY_VERSION}])


class AgentTraceSourceBundleService:
    def build_source_bundle(self, request: AgentTraceRequest, ask_repl_report: AgentAskReplReport | None) -> AgentTraceSourceBundle:
        run = ask_repl_report.pipeline_run if ask_repl_report else None
        result = ask_repl_report.pipeline_result if ask_repl_report else None
        emission = ask_repl_report.emission if ask_repl_report else None
        stage_refs = AgentTracePrerequisiteSourceService().load_stage_reports_if_available(ask_repl_report)
        refs = {
            "ask_repl_report_ref": _source_ref("agent_ask_repl_report", ask_repl_report.report_id) if ask_repl_report else None,
            "pipeline_run_ref": _source_ref("agent_ask_pipeline_run", run.pipeline_run_id) if run else None,
            "pipeline_result_ref": _source_ref("agent_ask_pipeline_result", result.pipeline_result_id) if result else None,
            "surface_emission_ref": _source_ref("agent_surface_emission", emission.emission_id) if emission else None,
            "turn_envelope_ref": stage_refs.get("v0.25.1_turn_envelope"),
            "intent_report_ref": stage_refs.get("v0.25.2_intent_task"),
            "safety_gate_report_ref": stage_refs.get("v0.25.3_safety_gate"),
            "routing_report_ref": stage_refs.get("v0.25.4_route_plan"),
            "provider_invocation_report_ref": stage_refs.get("v0.25.5_provider_invocation"),
            "response_assembly_report_ref": stage_refs.get("v0.25.6_response_assembly"),
        }
        source_count = len([item for item in refs.values() if item])
        if source_count == 0:
            status = "missing"
        elif source_count < 4:
            status = "partial"
        else:
            status = "complete" if all(refs[key] for key in ["ask_repl_report_ref", "pipeline_run_ref", "pipeline_result_ref", "surface_emission_ref"]) else "partial"
        return AgentTraceSourceBundle(
            source_bundle_id=f"agent_trace_source_bundle:{_safe_id(request.request_id)}",
            source_count=source_count,
            source_status=status,
            evidence_refs=[_source_ref("agent_trace_request", request.request_id)],
            **refs,
        )


class AgentPipelineStageTraceService:
    def build_stage_traces(self, run: AgentAskPipelineRun | None) -> list[AgentPipelineStageTrace]:
        step_by_stage = {_stage_id_for_trace(step.stage_id): step for step in run.steps} if run else {}
        traces: list[AgentPipelineStageTrace] = []
        for stage_id in AGENT_TRACE_STAGE_IDS:
            step = step_by_stage.get(stage_id)
            if step is None:
                traces.append(
                    AgentPipelineStageTrace(
                        stage_trace_id=f"agent_pipeline_stage_trace:{stage_id}",
                        stage_id=stage_id,
                        stage_name=stage_id,
                        stage_status="missing",
                        input_refs=[],
                        output_refs=[],
                        started_at=None,
                        ended_at=None,
                        duration_ms=None,
                        provider_invoked=False,
                        local_command_executed=False,
                    )
                )
                continue
            traces.append(
                AgentPipelineStageTrace(
                    stage_trace_id=f"agent_pipeline_stage_trace:{stage_id}",
                    stage_id=stage_id,
                    stage_name=step.stage_name,
                    stage_status="completed" if step.step_status == "executed" else step.step_status,
                    input_refs=step.input_refs,
                    output_refs=step.output_refs,
                    started_at=None,
                    ended_at=None,
                    duration_ms=None,
                    provider_invoked=step.provider_invoked,
                    local_command_executed=step.local_command_executed,
                    evidence_refs=[_source_ref("agent_ask_pipeline_step", step.pipeline_step_id)],
                )
            )
        return traces


class AgentDecisionTraceService:
    def build_decision_traces(self, report: AgentAskReplReport | None) -> list[AgentDecisionTrace]:
        result = report.pipeline_result if report else None
        outcome = result.primary_outcome if result else "missing"
        source = _source_ref("agent_ask_pipeline_result", result.pipeline_result_id) if result else None
        decision_types = [
            ("intent_classification", "observed"),
            ("safety_gate", "allow_route" if report and report.provider_invoked_via_v0255 else outcome),
            ("allow_route", str(bool(report and report.provider_invoked_via_v0255)).lower()),
            ("route_selection", "provider_route" if report and report.provider_invoked_via_v0255 else "skipped"),
            ("provider_invocation", "invoked_via_v0.25.5" if report and report.provider_invoked_via_v0255 else "skipped"),
            ("response_assembly", "assembled_via_v0.25.6" if report and report.response_assembled_via_v0256 else "missing"),
            ("emission", "emitted_via_v0.25.7" if report and report.final_response_emitted else "missing"),
        ]
        if outcome in {"no_action_response", "clarification_response", "needs_more_input_response", "blocked_response", "deferred_response"}:
            decision_types.append((outcome.replace("_response", ""), outcome))
        return [
            AgentDecisionTrace(
                decision_trace_id=f"agent_decision_trace:{_safe_id(kind)}",
                decision_type=kind,
                decision_outcome=decision_outcome,
                decision_confidence="medium",
                source_ref=source,
                evidence_refs=[source] if source else [],
            )
            for kind, decision_outcome in decision_types
        ]


class AgentRouteTraceService:
    def build_route_trace(self, report: AgentAskReplReport | None) -> AgentRouteTrace | None:
        if not report or not report.pipeline_run:
            return None
        route_steps = [step for step in report.pipeline_run.steps if _stage_id_for_trace(step.stage_id) in {"v0.25.4_route_plan", "v0.25.5_provider_invocation"}]
        provider_refs = [_source_ref("internal_provider", "selected_by_v0.25.4")] if report.provider_invoked_via_v0255 else []
        return AgentRouteTrace(
            route_trace_id=f"agent_route_trace:{_safe_id(report.report_id)}",
            route_kind="provider_backed_route" if report.provider_invoked_via_v0255 else "non_provider_route",
            selected_provider_refs=provider_refs,
            route_step_refs=[_source_ref("agent_ask_pipeline_step", step.pipeline_step_id) for step in route_steps],
            route_status="invoked" if report.provider_invoked_via_v0255 else "skipped",
            provider_invocation_required=report.provider_invoked_via_v0255,
            provider_invoked_via_v0255=report.provider_invoked_via_v0255,
        )


class AgentProviderInvocationTraceViewService:
    def build_provider_trace_view(self, bundle: AgentTraceSourceBundle, report: AgentAskReplReport | None) -> AgentProviderInvocationTraceView | None:
        if not report:
            return None
        result_refs = [_source_ref("agent_provider_invocation_result_ref", "observed-via-v0.25.5")] if report.provider_invoked_via_v0255 else []
        return AgentProviderInvocationTraceView(
            provider_trace_view_id=f"agent_provider_invocation_trace_view:{_safe_id(report.report_id)}",
            provider_invocation_report_ref=bundle.provider_invocation_report_ref,
            provider_result_refs=result_refs,
            provider_invoked_via_v0255=report.provider_invoked_via_v0255,
            local_command_executed_via_v024=report.local_command_executed_via_v024,
            evidence_refs=[bundle.provider_invocation_report_ref] if bundle.provider_invocation_report_ref else [],
        )


class AgentResponseEmissionTraceService:
    def build_response_emission_trace(self, report: AgentAskReplReport | None) -> AgentResponseEmissionTrace | None:
        if not report:
            return None
        result = report.pipeline_result
        emission = report.emission
        return AgentResponseEmissionTrace(
            emission_trace_id=f"agent_response_emission_trace:{_safe_id(report.report_id)}",
            assembled_response_ref=_source_ref("agent_assembled_response", result.assembled_response_id if result else None),
            surface_emission_ref=_source_ref("agent_surface_emission", emission.emission_id if emission else None),
            response_assembled_via_v0256=report.response_assembled_via_v0256,
            final_response_emitted_via_v0257=report.final_response_emitted,
            response_status="emitted" if report.final_response_emitted else "missing",
            raw_secret_output=False,
            raw_provider_output_inline=False,
        )


class AgentTraceEventService:
    def build_events(self, stage_traces: list[AgentPipelineStageTrace], decision_traces: list[AgentDecisionTrace]) -> list[AgentTraceEvent]:
        events: list[AgentTraceEvent] = []
        for stage in stage_traces:
            events.append(
                AgentTraceEvent(
                    trace_event_id=f"agent_trace_event:stage:{_safe_id(stage.stage_id)}",
                    event_type="agent_pipeline_stage_trace_created",
                    timestamp=None,
                    stage_id=stage.stage_id,
                    source_ref=_source_ref("agent_pipeline_stage_trace", stage.stage_trace_id),
                    event_status="observed" if stage.stage_status != "missing" else "missing",
                )
            )
        for decision in decision_traces:
            events.append(
                AgentTraceEvent(
                    trace_event_id=f"agent_trace_event:decision:{_safe_id(decision.decision_type)}",
                    event_type="agent_decision_trace_created",
                    timestamp=None,
                    stage_id=None,
                    source_ref=_source_ref("agent_decision_trace", decision.decision_trace_id),
                    event_status="inferred_from_report",
                )
            )
        return events


class AgentTraceObjectRefService:
    def build_object_refs(self, source_bundle: AgentTraceSourceBundle, stage_traces: list[AgentPipelineStageTrace]) -> list[AgentTraceObjectRef]:
        refs: list[AgentTraceObjectRef] = []
        for key, value in source_bundle.to_dict().items():
            if key.endswith("_ref") and isinstance(value, dict):
                object_id = str(value.get("id") or "missing")
                refs.append(
                    AgentTraceObjectRef(
                        object_ref_id=f"agent_trace_object_ref:{_safe_id(key)}:{_safe_id(object_id)}",
                        object_type=str(value.get("type") or key.replace("_ref", "")),
                        object_id=object_id,
                        source_version=str(value.get("version") or "unknown"),
                        stage_id=None,
                        sanitized_label=_sanitize_text(object_id),
                    )
                )
        for stage in stage_traces:
            refs.append(
                AgentTraceObjectRef(
                    object_ref_id=f"agent_trace_object_ref:{_safe_id(stage.stage_trace_id)}",
                    object_type="agent_pipeline_stage_trace",
                    object_id=stage.stage_trace_id,
                    source_version=AGENT_TRACE_TELEMETRY_VERSION,
                    stage_id=stage.stage_id,
                    sanitized_label=stage.stage_id,
                )
            )
        return refs


class AgentTraceRelationRefService:
    def build_relation_refs(self, object_refs: list[AgentTraceObjectRef]) -> list[AgentTraceRelationRef]:
        if not object_refs:
            return []
        root = object_refs[0]
        relations: list[AgentTraceRelationRef] = []
        for target in object_refs[1:]:
            relation_type = "observes_agent_pipeline_stage" if target.object_type == "agent_pipeline_stage_trace" else "uses_agent_ask_repl_report"
            relations.append(
                AgentTraceRelationRef(
                    relation_ref_id=f"agent_trace_relation_ref:{_safe_id(root.object_ref_id)}:{_safe_id(target.object_ref_id)}",
                    relation_type=relation_type,
                    source_object_ref_id=root.object_ref_id,
                    target_object_ref_id=target.object_ref_id,
                    stage_id=target.stage_id,
                )
            )
        return relations


class AgentSurfaceTraceService:
    def build_surface_trace(self, source_bundle: AgentTraceSourceBundle, report: AgentAskReplReport | None) -> AgentSurfaceTrace:
        stage_traces = AgentPipelineStageTraceService().build_stage_traces(report.pipeline_run if report else None)
        decision_traces = AgentDecisionTraceService().build_decision_traces(report)
        route_trace = AgentRouteTraceService().build_route_trace(report)
        provider_trace = AgentProviderInvocationTraceViewService().build_provider_trace_view(source_bundle, report)
        response_trace = AgentResponseEmissionTraceService().build_response_emission_trace(report)
        events = AgentTraceEventService().build_events(stage_traces, decision_traces)
        object_refs = AgentTraceObjectRefService().build_object_refs(source_bundle, stage_traces)
        relations = AgentTraceRelationRefService().build_relation_refs(object_refs)
        missing_stage = any(stage.stage_status == "missing" for stage in stage_traces)
        status = "partial" if source_bundle.source_status != "complete" or missing_stage else "complete"
        return AgentSurfaceTrace(
            surface_trace_id=f"agent_surface_trace:{_safe_id(source_bundle.source_bundle_id)}",
            created_at=utc_now_iso(),
            source_bundle_id=source_bundle.source_bundle_id,
            trace_events=events,
            object_refs=object_refs,
            relation_refs=relations,
            stage_traces=stage_traces,
            decision_traces=decision_traces,
            route_trace=route_trace,
            provider_trace_view=provider_trace,
            response_emission_trace=response_trace,
            trace_status=status,
            ocel_projectable=source_bundle.source_status != "missing",
            evidence_refs=[_source_ref("agent_trace_source_bundle", source_bundle.source_bundle_id)],
        )


class AgentTurnOCELProjectionPolicyService:
    def build_policy(self) -> AgentTurnOCELProjectionPolicy:
        return AgentTurnOCELProjectionPolicy(policy_id="agent_turn_ocel_projection_policy:v0.25.8")


class AgentTurnOCELProjectionService:
    def build_projection(self, surface_trace: AgentSurfaceTrace) -> AgentTurnOCELProjection:
        return AgentTurnOCELProjection(
            projection_id=f"agent_turn_ocel_projection:{_safe_id(surface_trace.surface_trace_id)}",
            surface_trace_id=surface_trace.surface_trace_id,
            object_types=list(AGENT_TRACE_OBJECT_TYPES),
            event_types=list(AGENT_TRACE_EVENT_TYPES),
            relation_types=list(AGENT_TRACE_RELATION_TYPES),
            projected_object_count=len(surface_trace.object_refs),
            projected_event_count=len(surface_trace.trace_events),
            projected_relation_count=len(surface_trace.relation_refs),
            projection_status="ready" if surface_trace.ocel_projectable else "failed",
            evidence_refs=[_source_ref("agent_surface_trace", surface_trace.surface_trace_id)],
        )


class AgentUsabilityMetricDefinitionService:
    def build_metric_definitions(self) -> list[AgentUsabilityMetricDefinition]:
        definitions: list[AgentUsabilityMetricDefinition] = []
        for metric_id in REQUIRED_USABILITY_METRICS:
            category = "safety_boundary"
            if metric_id in {"agent_turn_count", "ask_count", "repl_turn_count", "final_response_emission_count"}:
                category = "turn_volume"
            elif metric_id.endswith("_count") and any(token in metric_id for token in ["pipeline", "route", "provider", "response_assembly"]):
                category = "stage_flow"
            elif any(token in metric_id for token in ["no_action", "clarification", "blocked", "deferred", "allow_route"]):
                category = "decision_distribution"
            elif any(token in metric_id for token in ["unsupported", "uncertainty", "limitation"]):
                category = "response_quality_proxy"
            definitions.append(
                AgentUsabilityMetricDefinition(
                    metric_id=metric_id,
                    metric_name=metric_id.replace("_", " "),
                    metric_category=category,
                    description=f"Report-derived {metric_id} metric.",
                    value_type="count",
                )
            )
        return definitions


class AgentUsabilityMetricComputationService:
    def compute_metric_values(self, definitions: list[AgentUsabilityMetricDefinition], report: AgentAskReplReport | None, surface_trace: AgentSurfaceTrace) -> list[AgentUsabilityMetricValue]:
        result = report.pipeline_result if report else None
        outcome = result.primary_outcome if result else ""
        values = {
            "agent_turn_count": int(bool(report and (report.ask_executed or report.repl_turn_executed))),
            "ask_count": int(bool(report and report.ask_executed)),
            "repl_turn_count": int(bool(report and report.repl_turn_executed)),
            "final_response_emission_count": int(bool(report and report.final_response_emitted)),
            "no_action_count": int(outcome == "no_action_response"),
            "clarification_count": int(outcome in {"clarification_response", "needs_more_input_response"}),
            "needs_more_input_count": int(outcome == "needs_more_input_response"),
            "blocked_count": int(outcome == "blocked_response"),
            "deferred_count": int(outcome == "deferred_response"),
            "allow_route_count": int(bool(report and report.provider_invoked_via_v0255)),
            "route_plan_count": int(any(stage.stage_id == "v0.25.4_route_plan" and stage.stage_status != "missing" for stage in surface_trace.stage_traces)),
            "provider_invocation_count": int(bool(report and report.provider_invoked_via_v0255)),
            "provider_warning_count": 0,
            "provider_failed_count": 0,
            "response_assembly_count": int(bool(report and report.response_assembled_via_v0256)),
            "unsupported_claim_count": 0,
            "uncertainty_note_count": 0,
            "limitation_note_count": 0,
            "pipeline_completed_count": int(bool(report and report.pipeline_run and report.pipeline_run.pipeline_status == "completed")),
            "pipeline_failed_count": int(bool(report and report.pipeline_run and report.pipeline_run.pipeline_status == "failed")),
            "pipeline_blocked_count": int(bool(report and report.pipeline_run and report.pipeline_run.pipeline_status == "blocked")),
            "direct_bypass_count": int(any(stage.direct_bypass_detected for stage in surface_trace.stage_traces)),
            "autonomous_loop_count": int(bool(report and report.autonomous_loop_started)),
            "background_execution_count": int(bool(report and report.background_execution_started)),
            "memory_promotion_count": int(bool(report and report.memory_promoted)),
            "credential_exposure_count": int(bool(report and report.credential_exposed)),
            "raw_secret_output_count": int(bool(report and report.raw_secret_output)),
        }
        source_refs = [_source_ref("agent_ask_repl_report", report.report_id if report else None)]
        return [
            AgentUsabilityMetricValue(
                metric_value_id=f"agent_usability_metric_value:{definition.metric_id}",
                metric_id=definition.metric_id,
                value=values.get(definition.metric_id, 0),
                unit="count",
                source_refs=source_refs,
                evidence_refs=[_source_ref("agent_usability_metric_definition", definition.metric_id)],
            )
            for definition in definitions
        ]


class AgentUsabilityTelemetryPolicyService:
    def build_policy(self) -> AgentUsabilityTelemetryPolicy:
        return AgentUsabilityTelemetryPolicy(policy_id="agent_usability_telemetry_policy:v0.25.8")


class AgentUsabilityTelemetryReportService:
    def build_report(
        self,
        surface_trace: AgentSurfaceTrace,
        definitions: list[AgentUsabilityMetricDefinition],
        metric_values: list[AgentUsabilityMetricValue],
    ) -> AgentUsabilityTelemetryReport:
        metric_set = AgentUsabilityMetricSet(
            metric_set_id=f"agent_usability_metric_set:{_safe_id(surface_trace.surface_trace_id)}",
            metric_values=metric_values,
            metric_count=len(metric_values),
            metric_set_status="ready" if metric_values else "failed",
        )
        status = "ready" if surface_trace.trace_status == "complete" else "partial"
        return AgentUsabilityTelemetryReport(
            telemetry_report_id=f"agent_usability_telemetry_report:{_safe_id(surface_trace.surface_trace_id)}",
            created_at=utc_now_iso(),
            policy=AgentUsabilityTelemetryPolicyService().build_policy(),
            surface_trace_id=surface_trace.surface_trace_id,
            metric_definitions=definitions,
            metric_set=metric_set,
            telemetry_status=status,
            evidence_refs=[_source_ref("agent_surface_trace", surface_trace.surface_trace_id)],
        )


class AgentTraceTelemetryFindingService:
    BLOCKED_ATTEMPTS = {
        "raw_transcript_persistence_attempted",
        "raw_provider_output_persistence_attempted",
        "raw_secret_persistence_attempted",
        "telemetry_background_daemon_attempted",
        "continuous_watcher_attempted",
        "autonomous_optimization_attempted",
        "ask_execution_attempted",
        "repl_execution_attempted",
        "provider_invocation_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "persona_mutation_attempted",
        "workspace_workbench_attempted",
        "external_provider_adapter_detected",
        "external_agent_adapter_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "schumpeter_split_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_inline_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        source_bundle: AgentTraceSourceBundle,
        surface_trace: AgentSurfaceTrace,
        projection: AgentTurnOCELProjection,
        telemetry_report: AgentUsabilityTelemetryReport,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentTraceTelemetryFinding]:
        subject = surface_trace.surface_trace_id
        findings = [self._finding("info", "ok", "Trace/telemetry report was evaluated.", subject)]
        if not source_bundle.ask_repl_report_ref:
            findings.append(self._finding("error", "missing_ask_repl_report", "Ask/REPL report source is missing.", source_bundle.source_bundle_id))
        if not source_bundle.pipeline_run_ref:
            findings.append(self._finding("warning", "missing_pipeline_run", "Pipeline run source is missing.", source_bundle.source_bundle_id))
        if not source_bundle.pipeline_result_ref:
            findings.append(self._finding("warning", "missing_assembled_response", "Assembled response result source is missing.", source_bundle.source_bundle_id))
        if not source_bundle.surface_emission_ref:
            findings.append(self._finding("warning", "missing_surface_emission", "Surface emission source is missing.", source_bundle.source_bundle_id))
        if source_bundle.source_status == "partial":
            findings.append(self._finding("warning", "source_bundle_partial", "Source bundle is partial.", source_bundle.source_bundle_id))
        findings.extend(
            [
                self._finding("info", "surface_trace_created", "Surface trace was created.", surface_trace.surface_trace_id),
                self._finding("info", "ocel_projection_created", "OCEL projection was created without mutating originals.", projection.projection_id),
                self._finding("info", "telemetry_report_created", "Usability telemetry report was created.", telemetry_report.telemetry_report_id),
                self._finding("info", "metric_set_created", "Metric set was created.", telemetry_report.metric_set.metric_set_id),
            ]
        )
        if any(stage.stage_status == "missing" for stage in surface_trace.stage_traces):
            findings.append(self._finding("warning", "stage_trace_missing", "One or more stage traces are missing.", subject))
        if not surface_trace.decision_traces:
            findings.append(self._finding("warning", "decision_trace_missing", "Decision traces are missing.", subject))
        if surface_trace.provider_trace_view and not surface_trace.provider_trace_view.provider_invoked_via_v0255:
            findings.append(self._finding("warning", "provider_trace_partial", "Provider trace is partial or not applicable.", subject))
        if surface_trace.response_emission_trace is None:
            findings.append(self._finding("warning", "response_emission_trace_missing", "Response emission trace is missing.", subject))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", subject))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentTraceTelemetryFinding:
        return AgentTraceTelemetryFinding(
            finding_id=f"agent_trace_telemetry_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the trace/telemetry policy boundary changes or the finding source is corrected.",
        )


class AgentTraceTelemetryReportService:
    def build_request(
        self,
        ask_report_id: str | None = None,
        trace_id: str | None = None,
        report_id: str | None = None,
        strictness: str = "standard",
    ) -> AgentTraceRequest:
        source_id = ask_report_id or report_id or trace_id or "synthetic-existing"
        return AgentTraceRequest(
            request_id=f"agent_trace_request:{_safe_id(source_id)}",
            ask_repl_report_id=ask_report_id or report_id or "agent_ask_repl_report:synthetic-existing",
            strictness=strictness,
            source_refs=[_source_ref("agent_ask_repl_report", ask_report_id or report_id or "agent_ask_repl_report:synthetic-existing")],
        )

    def build_report(
        self,
        ask_report_id: str | None = None,
        trace_id: str | None = None,
        report_id: str | None = None,
        strictness: str = "standard",
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentTraceTelemetryReport:
        request = self.build_request(ask_report_id=ask_report_id, trace_id=trace_id, report_id=report_id, strictness=strictness)
        ask_report = AgentTracePrerequisiteSourceService().load_ask_repl_report(request.ask_repl_report_id)
        trace_policy = AgentTracePolicyService().build_policy()
        source_bundle = AgentTraceSourceBundleService().build_source_bundle(request, ask_report)
        surface_trace = AgentSurfaceTraceService().build_surface_trace(source_bundle, ask_report)
        projection_policy = AgentTurnOCELProjectionPolicyService().build_policy()
        projection = AgentTurnOCELProjectionService().build_projection(surface_trace)
        metric_definitions = AgentUsabilityMetricDefinitionService().build_metric_definitions()
        metric_values = AgentUsabilityMetricComputationService().compute_metric_values(metric_definitions, ask_report, surface_trace)
        telemetry_report = AgentUsabilityTelemetryReportService().build_report(surface_trace, metric_definitions, metric_values)
        findings = AgentTraceTelemetryFindingService().build_findings(source_bundle, surface_trace, projection, telemetry_report, attempt_flags)
        status = self._report_status(findings, source_bundle, strictness)
        return AgentTraceTelemetryReport(
            report_id=f"agent_trace_telemetry_report:{_safe_id(request.request_id)}",
            created_at=utc_now_iso(),
            trace_policy=trace_policy,
            trace_request=request,
            source_bundle=source_bundle,
            surface_trace=surface_trace,
            projection_policy=projection_policy,
            ocel_projection=projection,
            telemetry_policy=telemetry_report.policy,
            telemetry_report=telemetry_report,
            findings=findings,
            report_status=status,
            ready_for_v0_25_9=status in {"passed", "warning"},
            trace_recorded=surface_trace.trace_status in {"complete", "partial"},
            ocel_projected=projection.projection_status in {"ready", "partial"},
            telemetry_created=telemetry_report.telemetry_status in {"ready", "partial", "warning"},
            limitations=[
                "v0.25.8 creates report-derived trace and descriptive telemetry only; it does not run ask/repl or emit responses.",
                "Synthetic source loading represents an already existing v0.25.7 report reference when no persistence layer is present.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.25.8 executes ask/repl, emits a response, invokes providers, executes commands, starts background telemetry, promotes memory, mutates persona, persists raw transcripts, exposes secrets, or uses an LLM judge.",
            ],
        )

    def build_all_parts(self, ask_report_id: str | None = None, trace_id: str | None = None, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(ask_report_id=ask_report_id, trace_id=trace_id, report_id=report_id)
        return {
            "report": report,
            "trace_policy": report.trace_policy,
            "trace_request": report.trace_request,
            "source_bundle": report.source_bundle,
            "surface_trace": report.surface_trace,
            "projection_policy": report.projection_policy,
            "ocel_projection": report.ocel_projection,
            "telemetry_policy": report.telemetry_policy,
            "telemetry_report": report.telemetry_report,
            "metric_definitions": report.telemetry_report.metric_definitions,
            "metric_set": report.telemetry_report.metric_set,
            "findings": report.findings,
        }

    def _report_status(self, findings: list[AgentTraceTelemetryFinding], source_bundle: AgentTraceSourceBundle, strictness: str) -> str:
        if any(finding.severity == "critical" for finding in findings):
            return "blocked"
        if source_bundle.source_status == "missing" and strictness == "strict":
            return "failed"
        if any(finding.severity == "error" for finding in findings):
            return "failed"
        if any(finding.severity == "warning" for finding in findings) or source_bundle.source_status == "partial":
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_TRACE_TELEMETRY_VERSION,
            "layer": "agent_surface",
            "subject": "agent_trace_usability_telemetry",
            "principles": [
                "trace recording is not agent execution",
                "telemetry is not workspace workbench",
                "telemetry is not memory promotion",
                "trace is not raw transcript storage",
                "metric is not optimization by itself",
                "OCEL projection is not mutation of original artifacts",
                "usability telemetry is descriptive, not autonomous control",
                "ask/repl execution remains v0.25.7",
                "workspace workbench is deferred to v0.26",
                "memory continuity is deferred to v0.27",
            ],
            "safety_boundary": {
                "trace_recorded": "conditional",
                "ocel_projected": "conditional",
                "telemetry_created": "conditional",
                "ask_executed": False,
                "repl_executed": False,
                "final_response_emitted": False,
                "provider_invoked": False,
                "local_command_executed": False,
                "direct_file_access_performed": False,
                "direct_subprocess_performed": False,
                "command_rerun_performed": False,
                "background_collection_started": False,
                "autonomous_optimization_performed": False,
                "workspace_workbench_implemented": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "raw_transcript_persisted": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.25.9": "general agent usability consolidation",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": AGENT_TRACE_TELEMETRY_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_trace_usability_telemetry_created",
            "version": AGENT_TRACE_TELEMETRY_VERSION,
            "source_read_models": [
                "AgentAskReplReportState",
                "AgentAskPipelineRunState",
                "AgentAskPipelineResultState",
                "AgentSurfaceEmissionState",
                "AgentTurnEnvelopeState",
                "AgentIntentClassificationState",
                "AgentSafetyGateState",
                "AgentToolRoutingState",
                "AgentProviderInvocationState",
                "AgentResponseAssemblyState",
            ],
            "target_read_models": [
                "AgentSurfaceTraceState",
                "AgentTurnOCELProjectionState",
                "AgentPipelineStageTraceState",
                "AgentDecisionTraceState",
                "AgentUsabilityMetricSetState",
                "AgentUsabilityTelemetryReportState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_TRACE_EFFECT_TYPES,
        }


def render_agent_trace_telemetry_cli(parts: dict[str, Any], section: str = "record") -> str:
    report: AgentTraceTelemetryReport = parts["report"]
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"trace_recorded={str(report.trace_recorded).lower()}",
        f"ocel_projected={str(report.ocel_projected).lower()}",
        f"telemetry_created={str(report.telemetry_created).lower()}",
        f"ready_for_v0_25_9={str(report.ready_for_v0_25_9).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_executed={str(report.repl_executed).lower()}",
        f"final_response_emitted={str(report.final_response_emitted).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"direct_file_access_performed={str(report.direct_file_access_performed).lower()}",
        f"direct_subprocess_performed={str(report.direct_subprocess_performed).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"background_collection_started={str(report.background_collection_started).lower()}",
        f"autonomous_optimization_performed={str(report.autonomous_optimization_performed).lower()}",
        f"workspace_workbench_implemented={str(report.workspace_workbench_implemented).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"raw_transcript_persisted={str(report.raw_transcript_persisted).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section in {"record", "view"}:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"trace_id={report.surface_trace.surface_trace_id}")
        lines.append(f"trace_status={report.surface_trace.trace_status}")
    elif section == "source-bundle":
        bundle = report.source_bundle
        lines.append(f"source_bundle_id={bundle.source_bundle_id}")
        lines.append(f"source_count={bundle.source_count}")
        lines.append(f"source_status={bundle.source_status}")
        lines.append(f"raw_transcript_included={str(bundle.raw_transcript_included).lower()}")
    elif section == "projection":
        projection = report.ocel_projection
        lines.append(f"projection_id={projection.projection_id}")
        lines.append(f"projection_status={projection.projection_status}")
        lines.append(f"projected_object_count={projection.projected_object_count}")
        lines.append(f"projected_event_count={projection.projected_event_count}")
        lines.append(f"projected_relation_count={projection.projected_relation_count}")
    elif section in {"telemetry", "metrics"}:
        telemetry = report.telemetry_report
        lines.append(f"telemetry_report_id={telemetry.telemetry_report_id}")
        lines.append(f"telemetry_status={telemetry.telemetry_status}")
        lines.append(f"metric_count={telemetry.metric_set.metric_count}")
        for value in telemetry.metric_set.metric_values:
            lines.append(f"- {value.metric_id}={value.value}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    return "\n".join(lines)
