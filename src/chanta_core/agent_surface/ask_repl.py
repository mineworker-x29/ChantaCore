from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any

from chanta_core.agent_surface.intent_task import AgentIntentClassificationReportService
from chanta_core.agent_surface.provider_invocation import AgentProviderInvocationReport, AgentProviderInvocationReportService
from chanta_core.agent_surface.response_assembly import (
    AgentAssembledResponse,
    AgentResponseAssemblyReport,
    AgentResponseAssemblyReportService,
)
from chanta_core.agent_surface.safety_gate import AgentSafetyGateReport, AgentSafetyGateReportService
from chanta_core.agent_surface.tool_routing import AgentToolRoutingReport, AgentToolRoutingReportService
from chanta_core.agent_surface.turn_context import AgentTurnReportService
from chanta_core.utility.time import utc_now_iso


AGENT_ASK_REPL_VERSION = "v0.25.7"
AGENT_ASK_REPL_VERSION_NAME = "Ask / REPL Surface"
AGENT_ASK_REPL_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_ASK_REPL_NEXT_STEP = "v0.25.8 Agent Trace / Usability Telemetry"

AGENT_ASK_REPL_STAGE_ORDER = [
    "v0.25.1_turn_envelope",
    "v0.25.2_intent_task",
    "v0.25.3_safety_gate",
    "v0.25.4_route_plan_if_allow_route",
    "v0.25.5_provider_invocation_if_required",
    "v0.25.6_response_assembly",
    "v0.25.7_surface_emission",
]

AGENT_ASK_REPL_OBJECT_TYPES = [
    "agent_ask_policy",
    "agent_ask_request",
    "agent_ask_pipeline_policy",
    "agent_ask_pipeline_step",
    "agent_ask_pipeline_run",
    "agent_ask_pipeline_result",
    "agent_surface_emission_policy",
    "agent_surface_emission",
    "agent_surface_output_view",
    "agent_repl_policy",
    "agent_repl_session",
    "agent_repl_turn_request",
    "agent_repl_turn_result",
    "agent_surface_command_history_entry",
    "agent_surface_session_state",
    "agent_ask_repl_finding",
    "agent_ask_repl_report",
    "agent_assembled_response",
    "agent_response_assembly_report",
    "agent_turn_envelope",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_ASK_REPL_EVENT_TYPES = [
    "agent_ask_requested",
    "agent_ask_policy_created",
    "agent_ask_pipeline_policy_created",
    "agent_ask_pipeline_run_started",
    "agent_ask_pipeline_step_executed",
    "agent_ask_pipeline_run_completed",
    "agent_surface_emission_policy_created",
    "agent_surface_response_emitted",
    "agent_surface_output_view_created",
    "agent_repl_session_started",
    "agent_repl_turn_requested",
    "agent_repl_turn_completed",
    "agent_repl_session_closed",
    "agent_surface_command_history_recorded",
    "agent_surface_session_state_created",
    "agent_ask_repl_report_created",
    "agent_ask_repl_warning_created",
    "agent_ask_repl_blocked",
]

AGENT_ASK_REPL_RELATION_TYPES = [
    "uses_agent_assembled_response",
    "uses_agent_response_assembly_report",
    "runs_bounded_agent_pipeline",
    "executes_agent_pipeline_step",
    "emits_assembled_response",
    "creates_surface_output_view",
    "starts_repl_session",
    "processes_user_driven_repl_turn",
    "records_surface_command_history",
    "creates_surface_session_state",
    "prepares_agent_trace_telemetry",
    "defers_agent_trace_telemetry_to_v0_25_8",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "enforces_one_pipeline_per_user_turn",
    "enforces_no_autonomous_loop",
    "enforces_no_background_execution",
    "enforces_no_self_prompting",
    "not_direct_provider_invocation",
    "not_direct_file_access",
    "not_direct_subprocess",
    "not_direct_local_command_execution",
    "not_command_rerun",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "blocks_raw_provider_output_inline",
    "blocks_raw_secret_output",
    "recorded_in_envelope",
]

AGENT_ASK_REPL_EFFECT_TYPES = [
    "read_only_observation",
    "agent_ask_executed",
    "agent_repl_started",
    "agent_repl_turn_executed",
    "final_response_emitted",
    "agent_surface_output_view_created",
    "agent_surface_command_history_recorded",
    "state_candidate_created",
]

AGENT_ASK_REPL_CONDITIONAL_EFFECT_TYPES = [
    "internal_provider_invoked",
    "bounded_local_command_executed",
]

AGENT_ASK_REPL_FORBIDDEN_EFFECT_TYPES = [
    "autonomous_loop_started",
    "background_execution_started",
    "self_prompt_loop_started",
    "direct_provider_invocation",
    "direct_file_access_performed",
    "direct_repository_search_performed",
    "direct_process_inspection_performed",
    "direct_subprocess_called",
    "direct_local_command_executed",
    "command_rerun_performed",
    "automatic_repair_performed",
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
    "schumpeter_split_introduced",
]


def _safe_id(text: str | None) -> str:
    value = text or "unknown"
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "-", value.strip().lower())[:140] or "unknown"


def _dict_ref(ref_type: str, ref_id: str | None) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id or "unknown"}


def _sanitize_text(text: str) -> str:
    value = text or ""
    value = re.sub(r"[A-Za-z]:\\[^\s`\"']+", "[private-path]", value)
    value = re.sub(r"(?i)(api[_-]?key|token|secret|password)=\S+", r"\1=[redacted]", value)
    return value[:20000]


@dataclass
class AgentAskPolicy:
    policy_id: str
    version: str = AGENT_ASK_REPL_VERSION
    layer: str = "agent_surface"
    ask_enabled: bool = True
    repl_enabled: bool = True
    synchronous_only: bool = True
    autonomous_loop_enabled: bool = False
    background_execution_enabled: bool = False
    self_prompting_enabled: bool = False
    direct_provider_invocation_enabled: bool = False
    direct_file_access_enabled: bool = False
    direct_subprocess_enabled: bool = False
    direct_local_command_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    external_provider_adapter_enabled: bool = False
    external_agent_adapter_enabled: bool = False
    require_v025_pipeline: bool = True
    require_v0256_assembled_response_for_emission: bool = True
    raw_secret_output_forbidden: bool = True
    raw_provider_output_inline_forbidden: bool = True
    private_path_sanitization_required: bool = True
    llm_judge_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAskRequest:
    request_id: str
    user_text: str
    version: str = AGENT_ASK_REPL_VERSION
    source_type: str = "cli"
    surface_mode: str = "single_turn_ask"
    run_full_pipeline: bool = True
    assembled_response_id: str | None = None
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAskPipelinePolicy:
    policy_id: str
    version: str = AGENT_ASK_REPL_VERSION
    required_stage_order: list[str] = field(default_factory=lambda: list(AGENT_ASK_REPL_STAGE_ORDER))
    allow_stage_skip_for_non_route_outcome: bool = True
    allow_provider_stage_only_when_route_requires_provider: bool = True
    allow_local_runtime_only_through_v024_gate: bool = True
    allow_response_emission_only_after_v0256: bool = True
    max_pipeline_turns_per_ask: int = 1
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAskPipelineStep:
    pipeline_step_id: str
    step_index: int
    stage_id: str
    stage_name: str
    input_refs: list[dict[str, Any]]
    output_refs: list[dict[str, Any]]
    step_status: str
    executed_now: bool
    provider_invoked: bool = False
    local_command_executed: bool = False
    response_assembled: bool = False
    final_response_emitted: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAskPipelineRun:
    pipeline_run_id: str
    ask_request_id: str
    steps: list[AgentAskPipelineStep]
    started_at: str
    version: str = AGENT_ASK_REPL_VERSION
    ended_at: str | None = None
    pipeline_status: str = "completed"
    final_stage_id: str | None = None
    assembled_response_ref: dict[str, Any] | None = None
    surface_emission_ref: dict[str, Any] | None = None
    autonomous_loop_started: bool = False
    background_execution_started: bool = False
    self_prompt_loop_started: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAskPipelineResult:
    pipeline_result_id: str
    pipeline_run_id: str
    primary_outcome: str
    assembled_response_id: str | None
    emission_id: str | None
    response_text: str | None
    result_status: str
    evidence_bound: bool
    final_response_emitted: bool
    provider_invoked_via_v0255: bool
    local_command_executed_via_v024: bool
    direct_provider_invocation: bool = False
    direct_local_command_execution: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSurfaceEmissionPolicy:
    policy_id: str
    version: str = AGENT_ASK_REPL_VERSION
    emit_only_assembled_response: bool = True
    require_v0256_report: bool = True
    require_evidence_bound_or_policy_response: bool = True
    raw_secret_output_forbidden: bool = True
    credential_output_forbidden: bool = True
    raw_provider_output_inline_forbidden: bool = True
    private_path_sanitization_required: bool = True
    max_output_chars: int = 20000
    final_response_emission_enabled: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSurfaceEmission:
    emission_id: str
    assembled_response_id: str
    response_text: str
    output_view_id: str
    emitted_at: str
    emitted_to: str
    version: str = AGENT_ASK_REPL_VERSION
    final_response_emitted: bool = True
    response_truncated: bool = False
    sanitized: bool = True
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSurfaceOutputView:
    output_view_id: str
    response_text: str
    display_format: str
    version: str = AGENT_ASK_REPL_VERSION
    bounded: bool = True
    sanitized: bool = True
    evidence_summary_included: bool = False
    limitations_included: bool = False
    uncertainty_included: bool = False
    conclusion_once: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentReplPolicy:
    policy_id: str
    version: str = AGENT_ASK_REPL_VERSION
    repl_enabled: bool = True
    user_driven_turns_only: bool = True
    max_turns_per_session: int = 100
    one_pipeline_run_per_user_turn: bool = True
    no_autonomous_loop: bool = True
    no_background_execution: bool = True
    no_self_prompting: bool = True
    persistent_memory_write_enabled: bool = False
    memory_promotion_enabled: bool = False
    persona_mutation_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentReplSession:
    repl_session_id: str
    created_at: str
    version: str = AGENT_ASK_REPL_VERSION
    closed_at: str | None = None
    session_status: str = "active"
    turn_count: int = 0
    user_driven: bool = True
    autonomous_loop_started: bool = False
    background_execution_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentReplTurnRequest:
    repl_turn_request_id: str
    repl_session_id: str
    user_text: str
    turn_index: int
    run_full_pipeline: bool = True
    source_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentReplTurnResult:
    repl_turn_result_id: str
    repl_session_id: str
    turn_index: int
    ask_request_id: str
    pipeline_result_id: str
    emission_id: str | None
    turn_status: str
    final_response_emitted: bool
    autonomous_followup_created: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSurfaceCommandHistoryEntry:
    history_entry_id: str
    command_type: str
    request_ref: dict[str, Any] | None
    result_ref: dict[str, Any] | None
    timestamp: str
    version: str = AGENT_ASK_REPL_VERSION
    sanitized: bool = True
    raw_secret_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentSurfaceSessionState:
    surface_session_state_id: str
    active_repl_sessions: int
    total_ask_count: int
    total_repl_turn_count: int
    total_emission_count: int
    version: str = AGENT_ASK_REPL_VERSION
    autonomous_loop_count: int = 0
    background_execution_count: int = 0
    memory_promotion_count: int = 0
    external_adapter_count: int = 0
    state_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentAskReplFinding:
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
class AgentAskReplReport:
    report_id: str
    created_at: str
    policy: AgentAskPolicy
    session_state: AgentSurfaceSessionState
    version: str = AGENT_ASK_REPL_VERSION
    ask_request: AgentAskRequest | None = None
    pipeline_run: AgentAskPipelineRun | None = None
    pipeline_result: AgentAskPipelineResult | None = None
    emission: AgentSurfaceEmission | None = None
    repl_session: AgentReplSession | None = None
    repl_turn_result: AgentReplTurnResult | None = None
    findings: list[AgentAskReplFinding] = field(default_factory=list)
    report_status: str = "failed"
    ready_for_v0_25_8: bool = False
    ready_for_v0_26: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    repl_turn_executed: bool = False
    final_response_emitted: bool = False
    response_assembled_via_v0256: bool = False
    provider_invoked_via_v0255: bool = False
    local_command_executed_via_v024: bool = False
    direct_provider_invocation: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    direct_local_command_executed: bool = False
    command_rerun_performed: bool = False
    autonomous_loop_started: bool = False
    background_execution_started: bool = False
    self_prompt_loop_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_ASK_REPL_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.8 trace/telemetry begins or ask/repl surface policy changes."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentAskPrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        from chanta_core.agent_surface.contract import AgentSurfaceContractReportService

        return AgentSurfaceContractReportService().build_report().to_dict()

    def load_assembled_response_if_given(self, assembled_response_id: str | None, request_text: str) -> AgentResponseAssemblyReport:
        report = AgentResponseAssemblyReportService().build_report(request_text=request_text)
        if assembled_response_id and report.assembled_response:
            report.assembled_response.assembled_response_id = assembled_response_id
            report.report_id = f"agent_response_assembly_report:{_safe_id(assembled_response_id)}"
        return report

    def load_v025_stage_services(self) -> dict[str, Any]:
        return {
            "turn": AgentTurnReportService,
            "intent": AgentIntentClassificationReportService,
            "safety": AgentSafetyGateReportService,
            "route": AgentToolRoutingReportService,
            "provider_invocation": AgentProviderInvocationReportService,
            "response_assembly": AgentResponseAssemblyReportService,
        }


class AgentAskPolicyService:
    def build_policy(self) -> AgentAskPolicy:
        return AgentAskPolicy(policy_id="agent_ask_policy:v0.25.7", evidence_refs=[{"type": "version", "value": AGENT_ASK_REPL_VERSION}])


class AgentAskPipelinePolicyService:
    def build_policy(self) -> AgentAskPipelinePolicy:
        return AgentAskPipelinePolicy(policy_id="agent_ask_pipeline_policy:v0.25.7")


class AgentSurfaceEmissionPolicyService:
    def build_policy(self) -> AgentSurfaceEmissionPolicy:
        return AgentSurfaceEmissionPolicy(policy_id="agent_surface_emission_policy:v0.25.7")


class AgentReplPolicyService:
    def build_policy(self) -> AgentReplPolicy:
        return AgentReplPolicy(policy_id="agent_repl_policy:v0.25.7")


class AgentSurfaceOutputViewService:
    def build_output_view(self, assembled_response: AgentAssembledResponse, display_format: str = "plain_text") -> AgentSurfaceOutputView:
        text = _sanitize_text(assembled_response.response_text)
        return AgentSurfaceOutputView(
            output_view_id=f"agent_surface_output_view:{_safe_id(assembled_response.assembled_response_id)}",
            response_text=text,
            display_format=display_format if display_format in {"plain_text", "markdown", "json_summary"} else "unknown",
            evidence_summary_included="Evidence" in text or "근거" in text,
            limitations_included="Limitation" in text or "제한" in text,
            uncertainty_included="Uncertainty" in text or "불확실" in text,
            conclusion_once=text.lower().count("conclusion") <= 1,
        )


class AgentSurfaceEmissionService:
    def emit_assembled_response(
        self,
        assembled_response: AgentAssembledResponse | None,
        emitted_to: str = "cli",
        display_format: str = "plain_text",
    ) -> tuple[AgentSurfaceEmission | None, AgentSurfaceOutputView | None]:
        if assembled_response is None:
            return None, None
        policy = AgentSurfaceEmissionPolicyService().build_policy()
        view = AgentSurfaceOutputViewService().build_output_view(assembled_response, display_format)
        truncated = len(view.response_text) > policy.max_output_chars
        output_text = view.response_text[: policy.max_output_chars]
        return (
            AgentSurfaceEmission(
                emission_id=f"agent_surface_emission:{_safe_id(assembled_response.assembled_response_id)}",
                assembled_response_id=assembled_response.assembled_response_id,
                response_text=output_text,
                output_view_id=view.output_view_id,
                emitted_at=utc_now_iso(),
                emitted_to=emitted_to if emitted_to in {"cli", "repl", "test_fixture"} else "unknown",
                response_truncated=truncated,
                evidence_refs=[_dict_ref("agent_assembled_response", assembled_response.assembled_response_id)],
            ),
            view,
        )


class AgentAskPipelineRunnerService:
    def run_single_turn_pipeline(
        self,
        ask_request: AgentAskRequest,
        assembled_response: AgentAssembledResponse | None = None,
        response_report: AgentResponseAssemblyReport | None = None,
        emitted_to: str = "cli",
    ) -> tuple[AgentAskPipelineRun, AgentAskPipelineResult, AgentSurfaceEmission | None, AgentSurfaceOutputView | None, dict[str, Any]]:
        started_at = utc_now_iso()
        steps: list[AgentAskPipelineStep] = []
        artifacts: dict[str, Any] = {}
        previous_refs = [_dict_ref("agent_ask_request", ask_request.request_id)]

        def add_step(index: int, stage_id: str, name: str, outputs: list[dict[str, Any]], status: str = "executed", **flags: bool) -> None:
            nonlocal previous_refs
            steps.append(
                AgentAskPipelineStep(
                    pipeline_step_id=f"agent_ask_pipeline_step:{ask_request.request_id}:{index}",
                    step_index=index,
                    stage_id=stage_id,
                    stage_name=name,
                    input_refs=previous_refs,
                    output_refs=outputs,
                    step_status=status,
                    executed_now=status == "executed",
                    provider_invoked=flags.get("provider_invoked", False),
                    local_command_executed=flags.get("local_command_executed", False),
                    response_assembled=flags.get("response_assembled", False),
                    final_response_emitted=flags.get("final_response_emitted", False),
                )
            )
            previous_refs = outputs or previous_refs

        if not ask_request.run_full_pipeline and assembled_response is not None:
            add_step(1, "v0.25.6_response_assembly", "Use existing v0.25.6 assembled response", [_dict_ref("agent_assembled_response", assembled_response.assembled_response_id)])
        else:
            turn_report = AgentTurnReportService().build_report(request_text=ask_request.user_text)
            artifacts["turn_report"] = turn_report
            add_step(1, "v0.25.1_turn_envelope", "Create turn envelope", [_dict_ref("agent_turn_report", turn_report.report_id)])

            intent_report = AgentIntentClassificationReportService().build_report(request_text=ask_request.user_text)
            artifacts["intent_report"] = intent_report
            add_step(2, "v0.25.2_intent_task", "Classify intent and frame task", [_dict_ref("agent_intent_classification_report", intent_report.report_id)])

            safety_report = AgentSafetyGateReportService().build_report(request_text=ask_request.user_text)
            artifacts["safety_report"] = safety_report
            add_step(3, "v0.25.3_safety_gate", "Evaluate safety/no-action/clarification gate", [_dict_ref("agent_safety_gate_report", safety_report.report_id)])

            provider_report: AgentProviderInvocationReport | None = None
            route_report: AgentToolRoutingReport | None = None
            if safety_report.allow_route:
                route_report = AgentToolRoutingReportService().build_report(request_text=ask_request.user_text, safety_gate_report=safety_report, intent_report=intent_report)
                artifacts["route_report"] = route_report
                add_step(4, "v0.25.4_route_plan_if_allow_route", "Create route plan if allow-route", [_dict_ref("agent_tool_routing_report", route_report.report_id)])
                if route_report.ready_for_v0_25_5 and route_report.route_plan and route_report.route_plan.provider_invocation_required:
                    provider_report = AgentProviderInvocationReportService().build_report(request_text=ask_request.user_text, route_report=route_report)
                    artifacts["provider_report"] = provider_report
                    add_step(
                        5,
                        "v0.25.5_provider_invocation_if_required",
                        "Invoke internal provider only through v0.25.5",
                        [_dict_ref("agent_provider_invocation_report", provider_report.report_id)],
                        provider_invoked=provider_report.provider_invoked,
                        local_command_executed=provider_report.bounded_local_command_executed_via_v024,
                    )
                else:
                    add_step(5, "v0.25.5_provider_invocation_if_required", "Skip provider invocation when not required", [], "skipped")
            else:
                add_step(4, "v0.25.4_route_plan_if_allow_route", "Skip routing for non-route outcome", [], "skipped")
                add_step(5, "v0.25.5_provider_invocation_if_required", "Skip provider invocation for non-route outcome", [], "skipped")

            response_report = AgentResponseAssemblyReportService().build_report(
                request_text=ask_request.user_text,
                provider_report=provider_report,
                safety_gate_report=safety_report if provider_report is None else None,
                use_provider_report=provider_report is not None,
            )
            artifacts["response_report"] = response_report
            assembled_response = response_report.assembled_response
            add_step(
                6,
                "v0.25.6_response_assembly",
                "Assemble response and bind evidence",
                [_dict_ref("agent_response_assembly_report", response_report.report_id), _dict_ref("agent_assembled_response", assembled_response.assembled_response_id if assembled_response else None)],
                response_assembled=bool(response_report.response_assembled),
            )

        emission, output_view = AgentSurfaceEmissionService().emit_assembled_response(assembled_response, emitted_to=emitted_to)
        add_step(
            7,
            "v0.25.7_surface_emission",
            "Emit assembled response to user surface",
            [_dict_ref("agent_surface_emission", emission.emission_id if emission else None)],
            "executed" if emission else "failed",
            final_response_emitted=bool(emission and emission.final_response_emitted),
        )

        run_id = f"agent_ask_pipeline_run:{_safe_id(ask_request.request_id)}"
        pipeline_status = "completed" if emission else "failed"
        run = AgentAskPipelineRun(
            pipeline_run_id=run_id,
            ask_request_id=ask_request.request_id,
            steps=steps,
            started_at=started_at,
            ended_at=utc_now_iso(),
            pipeline_status=pipeline_status,
            final_stage_id="v0.25.7_surface_emission" if emission else None,
            assembled_response_ref=_dict_ref("agent_assembled_response", assembled_response.assembled_response_id if assembled_response else None),
            surface_emission_ref=_dict_ref("agent_surface_emission", emission.emission_id if emission else None),
        )
        provider_invoked = any(step.provider_invoked for step in steps)
        local_v024 = any(step.local_command_executed for step in steps)
        primary_outcome = "answered"
        if response_report and response_report.answer_draft:
            primary_outcome = response_report.answer_draft.response_mode
        result = AgentAskPipelineResult(
            pipeline_result_id=f"agent_ask_pipeline_result:{_safe_id(run_id)}",
            pipeline_run_id=run.pipeline_run_id,
            primary_outcome=primary_outcome,
            assembled_response_id=assembled_response.assembled_response_id if assembled_response else None,
            emission_id=emission.emission_id if emission else None,
            response_text=emission.response_text if emission else None,
            result_status="ready" if emission else "failed",
            evidence_bound=bool(response_report.evidence_bound if response_report else True),
            final_response_emitted=bool(emission and emission.final_response_emitted),
            provider_invoked_via_v0255=provider_invoked,
            local_command_executed_via_v024=local_v024,
        )
        artifacts["assembled_response"] = assembled_response
        artifacts["emission"] = emission
        artifacts["output_view"] = output_view
        return run, result, emission, output_view, artifacts


class AgentSurfaceCommandHistoryService:
    def record_history_entry(self, command_type: str, request_ref: dict[str, Any] | None, result_ref: dict[str, Any] | None) -> AgentSurfaceCommandHistoryEntry:
        return AgentSurfaceCommandHistoryEntry(
            history_entry_id=f"agent_surface_command_history_entry:{_safe_id(command_type)}:{_safe_id((request_ref or {}).get('id'))}",
            command_type=command_type if command_type in {"ask", "repl_turn", "repl_start", "repl_exit"} else "unknown",
            request_ref=request_ref,
            result_ref=result_ref,
            timestamp=utc_now_iso(),
        )


class AgentSurfaceSessionStateService:
    def build_session_state(
        self,
        ask_count: int = 0,
        repl_turn_count: int = 0,
        emission_count: int = 0,
        active_repl_sessions: int = 0,
    ) -> AgentSurfaceSessionState:
        return AgentSurfaceSessionState(
            surface_session_state_id="agent_surface_session_state:v0.25.7",
            active_repl_sessions=active_repl_sessions,
            total_ask_count=ask_count,
            total_repl_turn_count=repl_turn_count,
            total_emission_count=emission_count,
        )


class AgentReplSessionService:
    def start_session(self, session_id: str | None = None) -> AgentReplSession:
        return AgentReplSession(repl_session_id=session_id or f"agent_repl_session:{_safe_id(utc_now_iso())}", created_at=utc_now_iso())

    def close_session(self, session: AgentReplSession) -> AgentReplSession:
        session.closed_at = utc_now_iso()
        session.session_status = "closed"
        return session

    def run_user_turn(self, session: AgentReplSession, user_text: str) -> tuple[AgentReplTurnRequest, AgentReplTurnResult, AgentAskReplReport]:
        turn_index = session.turn_count + 1
        request = AgentReplTurnRequest(
            repl_turn_request_id=f"agent_repl_turn_request:{_safe_id(session.repl_session_id)}:{turn_index}",
            repl_session_id=session.repl_session_id,
            user_text=_sanitize_text(user_text),
            turn_index=turn_index,
        )
        report = AgentAskReplReportService().build_report(user_text=user_text, source_type="repl", emitted_to="repl", repl_session=session, repl_turn_request=request)
        session.turn_count = turn_index
        result = AgentReplTurnResult(
            repl_turn_result_id=f"agent_repl_turn_result:{_safe_id(request.repl_turn_request_id)}",
            repl_session_id=session.repl_session_id,
            turn_index=turn_index,
            ask_request_id=report.ask_request.request_id if report.ask_request else "unknown",
            pipeline_result_id=report.pipeline_result.pipeline_result_id if report.pipeline_result else "unknown",
            emission_id=report.emission.emission_id if report.emission else None,
            turn_status="completed" if report.final_response_emitted else report.report_status,
            final_response_emitted=report.final_response_emitted,
        )
        report.repl_turn_result = result
        report.repl_turn_executed = True
        return request, result, report


class AgentAskReplFindingService:
    BLOCKED_ATTEMPTS = {
        "autonomous_loop_attempted",
        "background_execution_attempted",
        "self_prompting_attempted",
        "direct_provider_invocation_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "direct_local_command_execution_attempted",
        "command_rerun_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "persona_mutation_attempted",
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
        ask_request: AgentAskRequest | None,
        pipeline_run: AgentAskPipelineRun | None,
        pipeline_result: AgentAskPipelineResult | None,
        emission: AgentSurfaceEmission | None,
        repl_session: AgentReplSession | None = None,
        repl_turn_request: AgentReplTurnRequest | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentAskReplFinding]:
        subject_id = ask_request.request_id if ask_request else repl_session.repl_session_id if repl_session else "agent_ask_repl"
        findings = [self._finding("info", "ok", "Ask/REPL surface was evaluated.", subject_id)]
        if ask_request:
            findings.append(self._finding("info", "ask_request_created", "Ask request was created.", ask_request.request_id))
        if repl_session:
            findings.append(self._finding("info", "repl_session_created", "REPL session was created.", repl_session.repl_session_id))
        if repl_turn_request:
            findings.append(self._finding("info", "repl_turn_created", "User-driven REPL turn was created.", repl_turn_request.repl_turn_request_id))
        if pipeline_run:
            findings.append(self._finding("info", "pipeline_run_created", "Bounded pipeline run was created.", pipeline_run.pipeline_run_id))
            for step in pipeline_run.steps:
                if step.step_status == "failed":
                    findings.append(self._finding("error", "pipeline_stage_failed", "Pipeline stage failed.", step.pipeline_step_id))
                if step.step_status == "blocked":
                    findings.append(self._finding("critical", "pipeline_stage_blocked", "Pipeline stage was blocked.", step.pipeline_step_id))
        if emission:
            findings.append(self._finding("info", "response_emitted", "Assembled response was emitted to the surface.", emission.emission_id))
            if emission.response_truncated:
                findings.append(self._finding("warning", "response_truncated", "Surface response was truncated.", emission.emission_id))
        else:
            findings.append(self._finding("error", "assembled_response_missing", "No v0.25.6 assembled response was available for emission.", subject_id))
        outcome = pipeline_result.primary_outcome if pipeline_result else ""
        outcome_findings = {
            "no_action_response": "no_action_emitted",
            "clarification_response": "clarification_emitted",
            "needs_more_input_response": "clarification_emitted",
            "blocked_response": "blocked_emitted",
            "deferred_response": "deferred_emitted",
        }
        if outcome in outcome_findings:
            findings.append(self._finding("warning", outcome_findings[outcome], f"{outcome} was emitted.", subject_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", subject_id))
        return findings

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentAskReplFinding:
        return AgentAskReplFinding(
            finding_id=f"agent_ask_repl_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by ask/repl policy.",
        )


class AgentAskReplReportService:
    def build_request(
        self,
        user_text: str = "Explain the project structure",
        source_type: str = "cli",
        surface_mode: str = "single_turn_ask",
        assembled_response_id: str | None = None,
        run_full_pipeline: bool = True,
    ) -> AgentAskRequest:
        return AgentAskRequest(
            request_id=f"agent_ask_request:{_safe_id(source_type)}:{_safe_id(user_text)}",
            user_text=_sanitize_text(user_text),
            source_type=source_type,
            surface_mode=surface_mode,
            run_full_pipeline=run_full_pipeline,
            assembled_response_id=assembled_response_id,
        )

    def build_report(
        self,
        user_text: str = "Explain the project structure",
        source_type: str = "cli",
        surface_mode: str = "single_turn_ask",
        assembled_response_id: str | None = None,
        run_full_pipeline: bool = True,
        emitted_to: str = "cli",
        repl_session: AgentReplSession | None = None,
        repl_turn_request: AgentReplTurnRequest | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentAskReplReport:
        policy = AgentAskPolicyService().build_policy()
        ask_request = self.build_request(user_text, source_type, surface_mode, assembled_response_id, run_full_pipeline)
        response_report = None
        assembled_response = None
        if assembled_response_id:
            response_report = AgentAskPrerequisiteSourceService().load_assembled_response_if_given(assembled_response_id, user_text)
            assembled_response = response_report.assembled_response
        run, result, emission, _output_view, artifacts = AgentAskPipelineRunnerService().run_single_turn_pipeline(
            ask_request,
            assembled_response=assembled_response,
            response_report=response_report,
            emitted_to=emitted_to,
        )
        response_report = artifacts.get("response_report", response_report)
        history = AgentSurfaceCommandHistoryService().record_history_entry(
            "repl_turn" if source_type == "repl" else "ask",
            _dict_ref("agent_ask_request", ask_request.request_id),
            _dict_ref("agent_ask_pipeline_result", result.pipeline_result_id),
        )
        session_state = AgentSurfaceSessionStateService().build_session_state(
            ask_count=0 if source_type == "repl" else 1,
            repl_turn_count=1 if source_type == "repl" else 0,
            emission_count=1 if emission else 0,
            active_repl_sessions=1 if repl_session and repl_session.session_status == "active" else 0,
        )
        findings = AgentAskReplFindingService().build_findings(
            ask_request,
            run,
            result,
            emission,
            repl_session,
            repl_turn_request,
            attempt_flags,
        )
        report_status = self._report_status(findings, result)
        return AgentAskReplReport(
            report_id=f"agent_ask_repl_report:{_safe_id(ask_request.request_id)}",
            created_at=utc_now_iso(),
            policy=policy,
            ask_request=ask_request,
            pipeline_run=run,
            pipeline_result=result,
            emission=emission,
            repl_session=repl_session,
            session_state=session_state,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_8=report_status in {"passed", "warning"},
            ask_executed=source_type != "repl",
            repl_started=bool(repl_session),
            repl_turn_executed=source_type == "repl",
            final_response_emitted=result.final_response_emitted,
            response_assembled_via_v0256=bool(response_report and response_report.response_assembled),
            provider_invoked_via_v0255=result.provider_invoked_via_v0255,
            local_command_executed_via_v024=result.local_command_executed_via_v024,
            limitations=[
                "v0.25.7 exposes a synchronous user surface only; trace and usability telemetry are deferred to v0.25.8.",
                "One ask or REPL turn creates at most one bounded v0.25 pipeline run.",
            ],
            withdrawal_conditions=[
                "Withdraw if ask/repl self-prompts, starts background work, bypasses v0.25 stages, directly invokes providers, directly reads files, executes commands, promotes memory, mutates persona, emits raw secrets, or uses an LLM judge.",
            ],
        )

    def build_repl_start_report(self, repl_session: AgentReplSession | None = None) -> AgentAskReplReport:
        session = repl_session or AgentReplSessionService().start_session()
        policy = AgentAskPolicyService().build_policy()
        session_state = AgentSurfaceSessionStateService().build_session_state(active_repl_sessions=1)
        findings = [
            AgentAskReplFindingService()._finding("info", "ok", "REPL surface session was evaluated.", session.repl_session_id),
            AgentAskReplFindingService()._finding("info", "repl_session_created", "REPL session was created without a user turn.", session.repl_session_id),
        ]
        return AgentAskReplReport(
            report_id=f"agent_ask_repl_report:{_safe_id(session.repl_session_id)}",
            created_at=utc_now_iso(),
            policy=policy,
            repl_session=session,
            session_state=session_state,
            findings=findings,
            report_status="passed",
            ready_for_v0_25_8=True,
            repl_started=True,
            limitations=[
                "REPL start creates a user-driven session surface only; no turn is executed until explicit user input is provided.",
            ],
            withdrawal_conditions=[
                "Withdraw if REPL start self-prompts, starts background work, executes a turn without user input, promotes memory, mutates persona, or uses an LLM judge.",
            ],
        )

    def build_all_parts(self, user_text: str = "Explain the project structure", source_type: str = "cli", assembled_response_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(user_text=user_text, source_type=source_type, assembled_response_id=assembled_response_id, run_full_pipeline=assembled_response_id is None)
        return {
            "report": report,
            "policy": report.policy,
            "ask_request": report.ask_request,
            "pipeline_run": report.pipeline_run,
            "pipeline_result": report.pipeline_result,
            "emission": report.emission,
            "repl_session": report.repl_session,
            "repl_turn_result": report.repl_turn_result,
            "session_state": report.session_state,
            "findings": report.findings,
        }

    def _report_status(self, findings: list[AgentAskReplFinding], result: AgentAskPipelineResult) -> str:
        if any(item.severity == "critical" for item in findings):
            return "blocked"
        if any(item.severity == "error" for item in findings) or result.result_status == "failed":
            return "failed"
        if any(item.severity == "warning" for item in findings) or result.result_status == "warning":
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_ASK_REPL_VERSION,
            "layer": "agent_surface",
            "subject": "ask_repl_surface",
            "principles": [
                "ask surface is not autonomous execution",
                "repl is user-driven, not self-driven",
                "one user turn creates at most one bounded pipeline run",
                "surface emission is not response assembly",
                "surface emission must use assembled response from v0.25.6",
                "ask/repl must not bypass stage boundaries",
                "provider invocation must occur only through v0.25.5",
                "local runtime execution must remain inside v0.24 gated provider boundary",
                "no-action, clarification, blocked, and deferred are valid emitted responses",
            ],
            "safety_boundary": {
                "ask_executed": "conditional",
                "repl_started": "conditional",
                "repl_turn_executed": "conditional",
                "final_response_emitted": "conditional",
                "response_assembled_via_v0256": "conditional",
                "provider_invoked_via_v0255": "conditional",
                "local_command_executed_via_v024": "conditional",
                "direct_provider_invocation": False,
                "direct_file_access_performed": False,
                "direct_subprocess_performed": False,
                "direct_local_command_executed": False,
                "command_rerun_performed": False,
                "autonomous_loop_started": False,
                "background_execution_started": False,
                "self_prompt_loop_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.25.8": "agent trace / usability telemetry",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": AGENT_ASK_REPL_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_ask_repl_surface_enabled",
            "version": AGENT_ASK_REPL_VERSION,
            "source_read_models": [
                "AgentAssembledResponseState",
                "AgentResponseAssemblyReportState",
                "AgentTurnEnvelopeState",
                "AgentSurfaceContractState",
            ],
            "target_read_models": [
                "AgentAskPipelineRunState",
                "AgentAskPipelineResultState",
                "AgentSurfaceEmissionState",
                "AgentSurfaceOutputViewState",
                "AgentReplSessionState",
                "AgentSurfaceSessionState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_ASK_REPL_EFFECT_TYPES,
        }


def render_agent_ask_repl_cli(parts: dict[str, Any], section: str = "ask") -> str:
    report: AgentAskReplReport = parts["report"]
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_started={str(report.repl_started).lower()}",
        f"repl_turn_executed={str(report.repl_turn_executed).lower()}",
        f"final_response_emitted={str(report.final_response_emitted).lower()}",
        f"response_assembled_via_v0256={str(report.response_assembled_via_v0256).lower()}",
        f"provider_invoked_via_v0255={str(report.provider_invoked_via_v0255).lower()}",
        f"local_command_executed_via_v024={str(report.local_command_executed_via_v024).lower()}",
        f"direct_provider_invocation={str(report.direct_provider_invocation).lower()}",
        f"direct_file_access_performed={str(report.direct_file_access_performed).lower()}",
        f"direct_subprocess_performed={str(report.direct_subprocess_performed).lower()}",
        f"direct_local_command_executed={str(report.direct_local_command_executed).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"autonomous_loop_started={str(report.autonomous_loop_started).lower()}",
        f"background_execution_started={str(report.background_execution_started).lower()}",
        f"self_prompt_loop_started={str(report.self_prompt_loop_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"ready_for_v0_25_8={str(report.ready_for_v0_25_8).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "ask":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
        if report.emission:
            lines.append("response_text:")
            lines.append(report.emission.response_text)
    elif section == "report":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"pipeline_status={report.pipeline_run.pipeline_status if report.pipeline_run else 'missing'}")
    elif section == "history":
        lines.append("history_entry_status=synthetic_non_persistent")
        lines.append("raw_secret_included=false")
    elif section == "session":
        session = report.repl_session
        lines.append(f"repl_session_id={session.repl_session_id if session else 'missing'}")
        lines.append(f"session_status={session.session_status if session else 'missing'}")
        lines.append(f"turn_count={session.turn_count if session else 0}")
    elif section == "state":
        state = report.session_state
        lines.append(f"active_repl_sessions={state.active_repl_sessions}")
        lines.append(f"total_ask_count={state.total_ask_count}")
        lines.append(f"total_repl_turn_count={state.total_repl_turn_count}")
        lines.append(f"total_emission_count={state.total_emission_count}")
        lines.append(f"autonomous_loop_count={state.autonomous_loop_count}")
        lines.append(f"background_execution_count={state.background_execution_count}")
        lines.append(f"memory_promotion_count={state.memory_promotion_count}")
        lines.append(f"external_adapter_count={state.external_adapter_count}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    return "\n".join(lines)
