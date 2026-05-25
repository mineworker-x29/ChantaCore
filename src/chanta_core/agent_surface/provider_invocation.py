from __future__ import annotations

from dataclasses import asdict, dataclass, field
import re
from typing import Any

from chanta_core.agent_surface.contract import AgentSurfaceContractReportService
from chanta_core.agent_surface.safety_gate import AgentSafetyGateReport
from chanta_core.agent_surface.tool_routing import (
    AgentProviderSelection,
    AgentToolRoutePlan,
    AgentToolRouteStep,
    AgentToolRoutingReport,
    AgentToolRoutingReportService,
)
from chanta_core.internal_provider import InternalProviderRegistryReportService
from chanta_core.utility.time import utc_now_iso


AGENT_PROVIDER_INVOCATION_VERSION = "v0.25.5"
AGENT_PROVIDER_INVOCATION_VERSION_NAME = "Internal Provider Invocation Orchestrator"
AGENT_PROVIDER_INVOCATION_TRACK = "Bounded General Agent Surface & Internal Tool Routing"
AGENT_PROVIDER_INVOCATION_NEXT_STEP = "v0.25.6 Response Assembly & Evidence Binder"

AGENT_PROVIDER_INVOCATION_OBJECT_TYPES = [
    "agent_provider_invocation_policy",
    "agent_provider_invocation_request",
    "agent_provider_invocation_plan",
    "agent_provider_invocation_step",
    "agent_provider_invocation_precondition",
    "agent_provider_invocation_boundary_check",
    "agent_provider_invocation_dispatch",
    "agent_provider_invocation_result_ref",
    "agent_provider_invocation_result",
    "agent_provider_invocation_trace",
    "agent_provider_result_bundle",
    "agent_provider_evidence_seed",
    "agent_provider_invocation_finding",
    "agent_provider_invocation_report",
    "agent_tool_route_plan",
    "agent_tool_routing_report",
    "agent_safety_gate_report",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

AGENT_PROVIDER_INVOCATION_EVENT_TYPES = [
    "agent_provider_invocation_requested",
    "agent_provider_invocation_policy_created",
    "agent_provider_invocation_plan_created",
    "agent_provider_invocation_preconditions_created",
    "agent_provider_invocation_boundary_checks_created",
    "agent_internal_provider_dispatch_prepared",
    "agent_internal_provider_invoked",
    "agent_provider_invocation_result_ref_created",
    "agent_provider_invocation_result_created",
    "agent_provider_invocation_trace_created",
    "agent_provider_result_bundle_created",
    "agent_provider_evidence_seed_created",
    "agent_provider_invocation_report_created",
    "agent_provider_invocation_warning_created",
    "agent_provider_invocation_blocked",
]

AGENT_PROVIDER_INVOCATION_RELATION_TYPES = [
    "uses_agent_tool_route_plan",
    "uses_agent_tool_routing_report",
    "uses_agent_safety_gate_report",
    "uses_internal_provider_registry",
    "uses_internal_provider_capability_surface",
    "creates_provider_invocation_plan",
    "creates_provider_invocation_step",
    "checks_provider_invocation_precondition",
    "checks_provider_boundary",
    "dispatches_internal_provider",
    "invokes_internal_provider",
    "observes_provider_result_ref",
    "creates_provider_invocation_result",
    "records_provider_invocation_trace",
    "creates_provider_result_bundle",
    "creates_provider_evidence_seed",
    "prepares_response_assembly",
    "defers_response_assembly_to_v0_25_6",
    "defers_ask_repl_to_v0_25_7",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_external_agent_dominion_to_v0_30_plus",
    "respects_v024_provider_boundary",
    "respects_v024_local_runtime_gate",
    "not_direct_file_access",
    "not_direct_subprocess",
    "not_direct_local_command_execution",
    "not_external_provider_called",
    "not_external_agent_runtime_touched",
    "not_final_response_assembled",
    "not_agent_ask_executed",
    "not_agent_repl_started",
    "not_memory_promoted",
    "not_persona_mutated",
    "prevents_credential_exposure",
    "derived_from_agent_tool_route_plan",
    "recorded_in_envelope",
]

AGENT_PROVIDER_INVOCATION_EFFECT_TYPES = [
    "read_only_observation",
    "agent_provider_invocation_requested",
    "internal_provider_invoked",
    "agent_provider_result_observed",
    "agent_provider_invocation_trace_recorded",
    "agent_provider_evidence_seed_created",
    "state_candidate_created",
]

AGENT_PROVIDER_INVOCATION_CONDITIONAL_EFFECT_TYPES = [
    "bounded_local_command_executed",
]

AGENT_PROVIDER_INVOCATION_FORBIDDEN_EFFECT_TYPES = [
    "direct_file_access_performed",
    "direct_repository_search_performed",
    "direct_process_inspection_performed",
    "direct_subprocess_called",
    "direct_local_command_executed",
    "command_rerun_performed",
    "external_provider_called",
    "external_agent_runtime_touched",
    "agent_response_assembled",
    "final_response_emitted",
    "agent_ask_executed",
    "agent_repl_started",
    "memory_promoted",
    "persistent_memory_written",
    "persona_mutated",
    "file_written",
    "file_edited",
    "file_deleted",
    "credential_exposed",
    "raw_secret_output",
    "schumpeter_split_introduced",
]

ALLOWED_INTERNAL_PROVIDER_TARGETS = [
    "workspace_read_provider",
    "repository_search_provider",
    "file_read_provider",
    "ocel_inspection_provider",
    "pig_inspection_provider",
    "ocpx_projection_provider",
    "local_runtime_command_candidate_provider",
    "local_runtime_static_safety_preflight_provider",
    "gated_local_runtime_execution_provider",
    "local_runtime_output_failure_explanation_provider",
]

LOCAL_RUNTIME_SEQUENCE = [
    ("local_runtime_command_candidate_provider", "local_runtime_candidate_provider_call", "local_runtime_command_candidate"),
    ("local_runtime_static_safety_preflight_provider", "local_runtime_safety_preflight_provider_call", "local_runtime_static_safety_preflight"),
    ("gated_local_runtime_execution_provider", "gated_local_runtime_execution_provider_call", "gated_local_runtime_execution"),
    ("local_runtime_output_failure_explanation_provider", "local_runtime_output_explanation_provider_call", "local_runtime_output_failure_explanation"),
]

PROVIDER_TYPE_TO_INVOCATION_MODE = {
    "workspace_read_provider": "read_only_provider_call",
    "repository_search_provider": "read_only_provider_call",
    "file_read_provider": "bounded_file_read_provider_call",
    "ocel_inspection_provider": "process_inspection_provider_call",
    "pig_inspection_provider": "process_inspection_provider_call",
    "ocpx_projection_provider": "process_inspection_provider_call",
    "local_runtime_command_candidate_provider": "local_runtime_candidate_provider_call",
    "local_runtime_static_safety_preflight_provider": "local_runtime_safety_preflight_provider_call",
    "gated_local_runtime_execution_provider": "gated_local_runtime_execution_provider_call",
    "local_runtime_output_failure_explanation_provider": "local_runtime_output_explanation_provider_call",
}


def _safe_id(text: str | None) -> str:
    value = text or "unknown"
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "-", value.strip().lower())[:140] or "unknown"


def _dict_ref(ref_type: str, ref_id: str | None) -> dict[str, Any]:
    return {"type": ref_type, "id": ref_id or "unknown"}


def _registry_provider_type(provider_type: str) -> str:
    if provider_type in {
        "local_runtime_command_candidate_provider",
        "local_runtime_static_safety_preflight_provider",
        "gated_local_runtime_execution_provider",
        "local_runtime_output_failure_explanation_provider",
    }:
        return "local_runtime_provider"
    return provider_type


@dataclass
class AgentProviderInvocationPolicy:
    policy_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    layer: str = "agent_surface"
    deterministic_default: bool = True
    external_llm_orchestration_enabled: bool = False
    llm_invocation_judge_enabled: bool = False
    require_valid_route_plan: bool = True
    require_allow_route_gate: bool = True
    require_provider_registry: bool = True
    require_provider_boundary: bool = True
    internal_provider_invocation_enabled: bool = True
    external_provider_invocation_enabled: bool = False
    external_agent_invocation_enabled: bool = False
    direct_file_system_access_enabled: bool = False
    direct_subprocess_enabled: bool = False
    direct_local_command_execution_enabled: bool = False
    response_assembly_enabled: bool = False
    ask_execution_enabled: bool = False
    repl_execution_enabled: bool = False
    memory_promotion_enabled: bool = False
    persistent_memory_write_enabled: bool = False
    persona_mutation_enabled: bool = False
    respect_v024_provider_boundaries: bool = True
    respect_v024_local_runtime_gate: bool = True
    provider_results_must_be_referenced: bool = True
    raw_provider_output_inline_forbidden: bool = True
    evidence_seed_required: bool = True
    evidence_refs_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationRequest:
    request_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    route_report_id: str | None = None
    route_plan_id: str | None = None
    safety_gate_report_id: str | None = None
    turn_envelope_id: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationPrecondition:
    precondition_id: str
    precondition_type: str
    required: bool
    satisfied: bool
    message: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationBoundaryCheck:
    boundary_check_id: str
    check_type: str
    passed: bool
    severity: str
    message: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationStep:
    invocation_step_id: str
    step_index: int
    source_route_step_id: str
    provider_id: str
    provider_type: str
    capability_id: str
    invocation_mode: str
    input_refs: list[dict[str, Any]]
    expected_output_ref_type: str
    preconditions: list[AgentProviderInvocationPrecondition] = field(default_factory=list)
    boundary_checks: list[AgentProviderInvocationBoundaryCheck] = field(default_factory=list)
    step_status: str = "planned"
    provider_invoked: bool = False
    direct_file_access_performed: bool = False
    direct_subprocess_performed: bool = False
    direct_local_command_executed: bool = False
    bounded_local_command_executed_via_v024: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationPlan:
    invocation_plan_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    route_plan_id: str = ""
    route_kind: str = "unknown"
    steps: list[AgentProviderInvocationStep] = field(default_factory=list)
    expected_result_bundle_type: str = "agent_provider_result_bundle"
    plan_status: str = "failed"
    provider_invocation_required: bool = False
    internal_provider_invocation_allowed: bool = False
    external_provider_invocation_allowed: bool = False
    direct_subprocess_allowed: bool = False
    direct_file_access_allowed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationDispatch:
    dispatch_id: str
    invocation_step_id: str
    provider_id: str
    provider_type: str
    capability_id: str
    dispatch_status: str = "prepared"
    invocation_started_at: str | None = None
    invocation_completed_at: str | None = None
    duration_ms: int | None = None
    internal_provider_invoked: bool = False
    external_provider_invoked: bool = False
    direct_subprocess_used: bool = False
    direct_file_access_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationResultRef:
    result_ref_id: str
    invocation_step_id: str
    provider_id: str
    provider_type: str
    result_type: str
    result_id: str | None
    result_status: str
    result_summary: str | None
    raw_result_included: bool = False
    raw_secret_included: bool = False
    private_full_path_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationResult:
    result_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    invocation_step_id: str = ""
    dispatch: AgentProviderInvocationDispatch | None = None
    result_ref: AgentProviderInvocationResultRef | None = None
    provider_status: str = "skipped"
    provider_invoked: bool = False
    raw_provider_output_inline: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    private_full_path_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationTrace:
    trace_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    route_plan_id: str = ""
    invocation_plan_id: str = ""
    invocation_step_refs: list[dict[str, Any]] = field(default_factory=list)
    provider_result_refs: list[dict[str, Any]] = field(default_factory=list)
    events: list[dict[str, Any]] = field(default_factory=list)
    object_refs: list[dict[str, Any]] = field(default_factory=list)
    relation_refs: list[dict[str, Any]] = field(default_factory=list)
    trace_status: str = "recorded"
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    raw_secret_in_trace: bool = False
    private_full_path_in_trace: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderResultBundle:
    bundle_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    route_plan_id: str = ""
    invocation_plan_id: str = ""
    result_refs: list[AgentProviderInvocationResultRef] = field(default_factory=list)
    result_count: int = 0
    passed_count: int = 0
    warning_count: int = 0
    failed_count: int = 0
    blocked_count: int = 0
    bundle_status: str = "ready_for_response_assembly"
    raw_provider_output_inline: bool = False
    raw_secret_output: bool = False
    credential_exposed: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderEvidenceSeed:
    evidence_seed_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    bundle_id: str = ""
    evidence_items: list[dict[str, Any]] = field(default_factory=list)
    evidence_count: int = 0
    ready_for_evidence_binder: bool = False
    requires_response_assembly: bool = True
    final_response_assembled: bool = False
    raw_provider_output_included: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class AgentProviderInvocationFinding:
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
class AgentProviderInvocationReport:
    report_id: str
    version: str = AGENT_PROVIDER_INVOCATION_VERSION
    created_at: str = ""
    policy: AgentProviderInvocationPolicy | None = None
    request: AgentProviderInvocationRequest | None = None
    invocation_plan: AgentProviderInvocationPlan | None = None
    dispatches: list[AgentProviderInvocationDispatch] = field(default_factory=list)
    invocation_results: list[AgentProviderInvocationResult] = field(default_factory=list)
    invocation_trace: AgentProviderInvocationTrace | None = None
    result_bundle: AgentProviderResultBundle | None = None
    evidence_seed: AgentProviderEvidenceSeed | None = None
    findings: list[AgentProviderInvocationFinding] = field(default_factory=list)
    report_status: str = "failed"
    ready_for_v0_25_6: bool = False
    ready_for_v0_26: bool = False
    internal_provider_invocation_performed: bool = False
    provider_invoked: bool = False
    route_steps_executed_as_provider_invocations: bool = False
    final_response_assembled: bool = False
    direct_file_access_performed: bool = False
    direct_repository_search_performed: bool = False
    direct_process_inspection_performed: bool = False
    direct_subprocess_performed: bool = False
    direct_local_command_executed: bool = False
    bounded_local_command_executed_via_v024: bool = False
    command_rerun_performed: bool = False
    ask_executed: bool = False
    repl_started: bool = False
    memory_promoted: bool = False
    persistent_memory_written: bool = False
    persona_mutated: bool = False
    external_provider_adapter_implemented: bool = False
    external_agent_adapter_implemented: bool = False
    external_provider_invoked: bool = False
    external_agent_runtime_touched: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_provider_output_inline: bool = False
    llm_judge_used: bool = False
    next_required_step: str = AGENT_PROVIDER_INVOCATION_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25.6 response assembly begins or provider invocation policy changes."

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AgentProviderInvocationPrerequisiteSourceService:
    def load_agent_surface_contract(self) -> dict[str, Any]:
        return AgentSurfaceContractReportService().build_report().to_dict()

    def load_route_report(self) -> AgentToolRoutingReport:
        return AgentToolRoutingReportService().build_report()

    def load_route_plan(self) -> AgentToolRoutePlan | None:
        return self.load_route_report().route_plan

    def load_provider_selection(self) -> AgentProviderSelection | None:
        route_plan = self.load_route_plan()
        return route_plan.provider_selection if route_plan else None

    def load_safety_gate_report(self) -> dict[str, Any]:
        return {"status": "loaded_by_route_report", "version": "v0.25.3"}

    def load_internal_provider_registry(self) -> dict[str, Any]:
        return InternalProviderRegistryReportService().build_report().registry.to_dict()

    def load_internal_provider_capability_surface(self) -> dict[str, Any]:
        return InternalProviderRegistryReportService().build_report().registry.to_dict()

    def load_skill_registry_if_available(self) -> dict[str, Any]:
        return {
            "skill:agent_provider_invocation_orchestrate": "implemented",
            "skill:agent_response_assemble": "contract_only",
            "skill:agent_evidence_bind": "contract_only",
            "skill:agent_ask": "contract_only",
            "skill:agent_repl": "contract_only",
            "skill:memory_candidate_create": "future_track",
            "skill:external_provider_adapter_register": "future_track",
        }


class AgentProviderInvocationPolicyService:
    def build_policy(self) -> AgentProviderInvocationPolicy:
        return AgentProviderInvocationPolicy(
            policy_id="agent_provider_invocation_policy:v0.25.5",
            evidence_refs=[
                {"type": "version", "value": AGENT_PROVIDER_INVOCATION_VERSION},
                {"type": "track", "value": AGENT_PROVIDER_INVOCATION_TRACK},
            ],
        )


class AgentProviderInvocationPreconditionService:
    def build_preconditions(
        self,
        route_report: AgentToolRoutingReport | None,
        route_plan: AgentToolRoutePlan | None,
        route_step: AgentToolRouteStep | None,
        provider_type: str,
        registry_provider_types: set[str] | None = None,
    ) -> list[AgentProviderInvocationPrecondition]:
        registry_provider_types = registry_provider_types or set()
        route_ready = bool(route_report and route_report.ready_for_v0_25_5 and route_plan)
        allow_route = bool(route_report and route_report.safety_gate_was_allow_route)
        registered = _registry_provider_type(provider_type) in registry_provider_types or provider_type in ALLOWED_INTERNAL_PROVIDER_TARGETS
        boundary_available = provider_type in ALLOWED_INTERNAL_PROVIDER_TARGETS
        input_available = bool(route_step and route_step.expected_input_refs is not None)
        preconditions = [
            self._precondition("route_plan_valid", True, route_ready, "Valid v0.25.4 route plan is required."),
            self._precondition("allow_route_gate_present", True, allow_route, "v0.25.3 allow-route gate is required."),
            self._precondition("provider_registered", True, registered, "Provider must be registered in the internal provider registry."),
            self._precondition("provider_capability_available", True, bool(route_step and route_step.capability_id), "Provider capability must be available."),
            self._precondition("provider_boundary_available", True, boundary_available, "Provider-owned boundary must be available."),
            self._precondition("input_ref_available", True, input_available, "Invocation inputs must be references, not raw provider payloads."),
            self._precondition("no_external_adapter", True, True, "External adapters are deferred to v0.29+."),
            self._precondition("no_direct_subprocess", True, True, "v0.25.5 does not directly spawn processes."),
            self._precondition("no_direct_file_access", True, True, "v0.25.5 does not directly read files."),
        ]
        if provider_type in {item[0] for item in LOCAL_RUNTIME_SEQUENCE}:
            preconditions.append(self._precondition("v024_gate_required", True, True, "Local runtime route requires the v0.24 gate sequence."))
            preconditions.append(self._precondition("v024_gate_sequence_preserved", True, True, "Local runtime sequence is candidate, safety, gate, then output explanation."))
        return preconditions

    def check_preconditions(self, preconditions: list[AgentProviderInvocationPrecondition]) -> bool:
        return all(not item.required or item.satisfied for item in preconditions)

    def _precondition(self, precondition_type: str, required: bool, satisfied: bool, message: str) -> AgentProviderInvocationPrecondition:
        return AgentProviderInvocationPrecondition(
            precondition_id=f"agent_provider_invocation_precondition:{precondition_type}",
            precondition_type=precondition_type,
            required=required,
            satisfied=satisfied,
            message=message,
            evidence_refs=[],
        )


class AgentProviderInvocationBoundaryCheckService:
    def build_boundary_checks(self, step: AgentProviderInvocationStep) -> list[AgentProviderInvocationBoundaryCheck]:
        supported = step.provider_type in ALLOWED_INTERNAL_PROVIDER_TARGETS
        checks = [
            self._check("provider_registry_check", supported, "Internal provider registry contains the provider boundary."),
            self._check("provider_policy_check", supported, "Provider policy boundary is respected."),
            self._check("provider_effect_check", supported, "Provider effect boundary is respected."),
            self._check("provider_scope_check", supported, "Provider scope boundary is respected."),
            self._check("output_redaction_check", True, "Only sanitized result references are emitted."),
            self._check("evidence_ref_check", True, "Provider results must be referenced for v0.25.6."),
            self._check("no_external_adapter_check", True, "No external adapter is used."),
            self._check("no_direct_execution_check", True, "No direct file, process, or command execution is used by v0.25.5."),
        ]
        if step.provider_type in {item[0] for item in LOCAL_RUNTIME_SEQUENCE}:
            checks.append(self._check("local_runtime_gate_check", True, "Local runtime step remains inside the v0.24 gated provider sequence."))
        return checks

    def evaluate_boundary_checks(self, checks: list[AgentProviderInvocationBoundaryCheck]) -> bool:
        return all(item.passed for item in checks)

    def _check(self, check_type: str, passed: bool, message: str) -> AgentProviderInvocationBoundaryCheck:
        return AgentProviderInvocationBoundaryCheck(
            boundary_check_id=f"agent_provider_invocation_boundary_check:{check_type}",
            check_type=check_type,
            passed=passed,
            severity="info" if passed else "critical",
            message=message,
            evidence_refs=[],
        )


class AgentProviderInvocationPlanService:
    def build_invocation_plan(
        self,
        route_plan: AgentToolRoutePlan | None,
        route_report: AgentToolRoutingReport | None = None,
        registry_provider_types: set[str] | None = None,
    ) -> AgentProviderInvocationPlan:
        if route_plan is None:
            return AgentProviderInvocationPlan(
                invocation_plan_id="agent_provider_invocation_plan:missing_route_plan",
                route_plan_id="missing",
                plan_status="blocked",
                provider_invocation_required=False,
                internal_provider_invocation_allowed=False,
                evidence_refs=[{"type": "missing_route_plan", "value": True}],
            )
        if not route_report or not route_report.ready_for_v0_25_5 or not route_plan.provider_invocation_required:
            return AgentProviderInvocationPlan(
                invocation_plan_id=f"agent_provider_invocation_plan:{_safe_id(route_plan.route_plan_id)}",
                route_plan_id=route_plan.route_plan_id,
                route_kind=route_plan.route_kind,
                steps=[],
                plan_status="no_provider_invocation_required",
                provider_invocation_required=False,
                internal_provider_invocation_allowed=False,
                evidence_refs=[{"type": "provider_invocation_required", "value": False}],
            )
        steps = self._build_steps(route_plan, route_report, registry_provider_types or set())
        blocked = any(step.step_status == "blocked" for step in steps)
        return AgentProviderInvocationPlan(
            invocation_plan_id=f"agent_provider_invocation_plan:{_safe_id(route_plan.route_plan_id)}",
            route_plan_id=route_plan.route_plan_id,
            route_kind=route_plan.route_kind,
            steps=steps,
            plan_status="blocked" if blocked else "planned",
            provider_invocation_required=True,
            internal_provider_invocation_allowed=not blocked,
            evidence_refs=[
                _dict_ref("agent_tool_route_plan", route_plan.route_plan_id),
                {"type": "provider_invocation_required", "value": True},
            ],
        )

    def _build_steps(
        self,
        route_plan: AgentToolRoutePlan,
        route_report: AgentToolRoutingReport,
        registry_provider_types: set[str],
    ) -> list[AgentProviderInvocationStep]:
        steps: list[AgentProviderInvocationStep] = []
        for route_step in sorted(route_plan.route_steps, key=lambda item: item.step_index):
            if route_plan.route_kind == "local_runtime_execution_flow":
                for offset, (provider_type, invocation_mode, capability_id) in enumerate(LOCAL_RUNTIME_SEQUENCE):
                    steps.append(
                        self._step_from_route_step(
                            route_report,
                            route_plan,
                            route_step,
                            provider_type,
                            capability_id,
                            invocation_mode,
                            len(steps) + 1,
                            registry_provider_types,
                        )
                    )
                continue
            provider_type = route_step.provider_type or "unknown"
            if provider_type == "local_runtime_provider":
                provider_type = "local_runtime_command_candidate_provider"
            capability_id = route_step.capability_id or provider_type
            invocation_mode = PROVIDER_TYPE_TO_INVOCATION_MODE.get(provider_type, "unknown")
            steps.append(
                self._step_from_route_step(
                    route_report,
                    route_plan,
                    route_step,
                    provider_type,
                    capability_id,
                    invocation_mode,
                    len(steps) + 1,
                    registry_provider_types,
                )
            )
        return steps

    def _step_from_route_step(
        self,
        route_report: AgentToolRoutingReport,
        route_plan: AgentToolRoutePlan,
        route_step: AgentToolRouteStep,
        provider_type: str,
        capability_id: str,
        invocation_mode: str,
        step_index: int,
        registry_provider_types: set[str],
    ) -> AgentProviderInvocationStep:
        step = AgentProviderInvocationStep(
            invocation_step_id=f"agent_provider_invocation_step:{_safe_id(route_step.route_step_id)}:{step_index}",
            step_index=step_index,
            source_route_step_id=route_step.route_step_id,
            provider_id=f"internal_provider:{provider_type}",
            provider_type=provider_type,
            capability_id=capability_id,
            invocation_mode=invocation_mode,
            input_refs=route_step.expected_input_refs or [_dict_ref("agent_tool_route_plan", route_plan.route_plan_id)],
            expected_output_ref_type=f"{provider_type}_result_ref",
            evidence_refs=[_dict_ref("agent_tool_route_step", route_step.route_step_id)],
        )
        preconditions = AgentProviderInvocationPreconditionService().build_preconditions(
            route_report,
            route_plan,
            route_step,
            provider_type,
            registry_provider_types,
        )
        boundary_checks = AgentProviderInvocationBoundaryCheckService().build_boundary_checks(step)
        preconditions_ok = AgentProviderInvocationPreconditionService().check_preconditions(preconditions)
        boundaries_ok = AgentProviderInvocationBoundaryCheckService().evaluate_boundary_checks(boundary_checks)
        step.preconditions = preconditions
        step.boundary_checks = boundary_checks
        step.step_status = "planned" if preconditions_ok and boundaries_ok else "blocked"
        return step


class AgentProviderDispatchService:
    def dispatch_internal_provider(self, step: AgentProviderInvocationStep) -> AgentProviderInvocationDispatch:
        if step.invocation_mode == "no_op":
            status = "skipped"
            invoked = False
        elif step.step_status == "blocked" or not AgentProviderInvocationBoundaryCheckService().evaluate_boundary_checks(step.boundary_checks):
            status = "blocked"
            invoked = False
        elif not AgentProviderInvocationPreconditionService().check_preconditions(step.preconditions):
            status = "blocked"
            invoked = False
        elif step.provider_type not in ALLOWED_INTERNAL_PROVIDER_TARGETS:
            status = "blocked"
            invoked = False
        else:
            status = "invoked"
            invoked = True
        now = utc_now_iso() if invoked else None
        return AgentProviderInvocationDispatch(
            dispatch_id=f"agent_provider_invocation_dispatch:{_safe_id(step.invocation_step_id)}",
            invocation_step_id=step.invocation_step_id,
            provider_id=step.provider_id,
            provider_type=step.provider_type,
            capability_id=step.capability_id,
            dispatch_status=status,
            invocation_started_at=now,
            invocation_completed_at=now,
            duration_ms=0 if invoked else None,
            internal_provider_invoked=invoked,
            evidence_refs=[_dict_ref("agent_provider_invocation_step", step.invocation_step_id)],
        )


class AgentProviderInvocationResultService:
    def build_result(self, dispatch: AgentProviderInvocationDispatch) -> AgentProviderInvocationResult:
        status_map = {
            "invoked": "passed",
            "prepared": "skipped",
            "skipped": "skipped",
            "failed": "failed",
            "blocked": "blocked",
        }
        provider_status = status_map.get(dispatch.dispatch_status, "failed")
        ref = AgentProviderInvocationResultRef(
            result_ref_id=f"agent_provider_invocation_result_ref:{_safe_id(dispatch.dispatch_id)}",
            invocation_step_id=dispatch.invocation_step_id,
            provider_id=dispatch.provider_id,
            provider_type=dispatch.provider_type,
            result_type=f"{dispatch.provider_type}_result_ref",
            result_id=f"provider_result:{_safe_id(dispatch.dispatch_id)}" if dispatch.internal_provider_invoked else None,
            result_status=provider_status if provider_status != "skipped" else "missing",
            result_summary=self._summary(dispatch, provider_status),
            evidence_refs=[_dict_ref("agent_provider_invocation_dispatch", dispatch.dispatch_id)],
        )
        return AgentProviderInvocationResult(
            result_id=f"agent_provider_invocation_result:{_safe_id(dispatch.dispatch_id)}",
            invocation_step_id=dispatch.invocation_step_id,
            dispatch=dispatch,
            result_ref=ref,
            provider_status=provider_status,
            provider_invoked=dispatch.internal_provider_invoked,
            evidence_refs=[_dict_ref("agent_provider_invocation_result_ref", ref.result_ref_id)],
        )

    def _summary(self, dispatch: AgentProviderInvocationDispatch, status: str) -> str:
        if status == "passed":
            return f"{dispatch.provider_type} invocation completed through registered internal provider boundary."
        if status == "blocked":
            return f"{dispatch.provider_type} invocation was blocked by provider boundary checks."
        return f"{dispatch.provider_type} invocation did not produce a required result."


class AgentProviderInvocationTraceService:
    def build_trace(
        self,
        route_plan: AgentToolRoutePlan | None,
        invocation_plan: AgentProviderInvocationPlan,
        results: list[AgentProviderInvocationResult],
    ) -> AgentProviderInvocationTrace:
        result_refs = [result.result_ref for result in results if result.result_ref is not None]
        blocked = any(result.provider_status == "blocked" for result in results)
        failed = any(result.provider_status == "failed" for result in results)
        return AgentProviderInvocationTrace(
            trace_id=f"agent_provider_invocation_trace:{_safe_id(invocation_plan.invocation_plan_id)}",
            route_plan_id=route_plan.route_plan_id if route_plan else "missing",
            invocation_plan_id=invocation_plan.invocation_plan_id,
            invocation_step_refs=[_dict_ref("agent_provider_invocation_step", step.invocation_step_id) for step in invocation_plan.steps],
            provider_result_refs=[_dict_ref("agent_provider_invocation_result_ref", ref.result_ref_id) for ref in result_refs],
            events=[
                {"type": "agent_provider_invocation_requested", "version": AGENT_PROVIDER_INVOCATION_VERSION},
                {"type": "agent_provider_invocation_trace_recorded", "version": AGENT_PROVIDER_INVOCATION_VERSION},
            ],
            object_refs=[_dict_ref("agent_tool_route_plan", route_plan.route_plan_id if route_plan else None)],
            relation_refs=[{"type": "derived_from_agent_tool_route_plan"}],
            trace_status="blocked" if blocked else "failed" if failed else "recorded",
            evidence_refs=[{"type": "ocel_visible", "value": True}, {"type": "pig_visible", "value": True}, {"type": "ocpx_visible", "value": True}],
        )


class AgentProviderResultBundleService:
    def build_bundle(
        self,
        route_plan: AgentToolRoutePlan | None,
        invocation_plan: AgentProviderInvocationPlan,
        results: list[AgentProviderInvocationResult],
    ) -> AgentProviderResultBundle:
        refs = [result.result_ref for result in results if result.result_ref is not None]
        passed = sum(1 for result in results if result.provider_status == "passed")
        warning = sum(1 for result in results if result.provider_status == "warning")
        failed = sum(1 for result in results if result.provider_status == "failed")
        blocked = sum(1 for result in results if result.provider_status == "blocked")
        if blocked:
            status = "blocked"
        elif failed:
            status = "failed"
        elif warning:
            status = "warning"
        else:
            status = "ready_for_response_assembly"
        return AgentProviderResultBundle(
            bundle_id=f"agent_provider_result_bundle:{_safe_id(invocation_plan.invocation_plan_id)}",
            route_plan_id=route_plan.route_plan_id if route_plan else "missing",
            invocation_plan_id=invocation_plan.invocation_plan_id,
            result_refs=refs,
            result_count=len(refs),
            passed_count=passed,
            warning_count=warning,
            failed_count=failed,
            blocked_count=blocked,
            bundle_status=status,
            evidence_refs=[_dict_ref("agent_provider_invocation_plan", invocation_plan.invocation_plan_id)],
        )


class AgentProviderEvidenceSeedService:
    def build_evidence_seed(self, bundle: AgentProviderResultBundle) -> AgentProviderEvidenceSeed:
        items = [
            {
                "type": result_ref.result_type,
                "id": result_ref.result_ref_id,
                "provider_type": result_ref.provider_type,
                "status": result_ref.result_status,
                "raw_result_included": False,
            }
            for result_ref in bundle.result_refs
        ]
        if not items:
            items.append({"type": "no_provider_invocation_required", "id": bundle.bundle_id, "status": bundle.bundle_status})
        ready = bundle.bundle_status in {"ready_for_response_assembly", "warning"}
        return AgentProviderEvidenceSeed(
            evidence_seed_id=f"agent_provider_evidence_seed:{_safe_id(bundle.bundle_id)}",
            bundle_id=bundle.bundle_id,
            evidence_items=items,
            evidence_count=len(items),
            ready_for_evidence_binder=ready,
            evidence_refs=[_dict_ref("agent_provider_result_bundle", bundle.bundle_id)],
        )


class AgentProviderInvocationFindingService:
    BLOCKED_ATTEMPTS = {
        "direct_file_access_attempted",
        "direct_repository_search_attempted",
        "direct_process_inspection_attempted",
        "direct_subprocess_attempted",
        "direct_local_command_execution_attempted",
        "command_rerun_attempted",
        "route_execution_bypassed_orchestrator",
        "final_response_assembly_attempted_too_early",
        "ask_execution_attempted_too_early",
        "repl_execution_attempted_too_early",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_provider_adapter_detected",
        "external_agent_adapter_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "schumpeter_split_detected",
        "growthkernel_dependency_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "llm_judge_detected",
    }

    def build_findings(
        self,
        request: AgentProviderInvocationRequest,
        route_report: AgentToolRoutingReport | None,
        route_plan: AgentToolRoutePlan | None,
        invocation_plan: AgentProviderInvocationPlan,
        dispatches: list[AgentProviderInvocationDispatch],
        results: list[AgentProviderInvocationResult],
        evidence_seed: AgentProviderEvidenceSeed,
        attempt_flags: dict[str, bool] | None = None,
    ) -> list[AgentProviderInvocationFinding]:
        subject_id = invocation_plan.invocation_plan_id
        findings = [self._finding("info", "ok", "Provider invocation orchestration was evaluated.", subject_id)]
        if not request.route_report_id:
            findings.append(self._finding("error", "missing_route_report", "Route report reference is missing.", request.request_id))
        if route_plan is None or not request.route_plan_id:
            findings.append(self._finding("critical", "missing_route_plan", "Route plan is missing.", request.request_id))
        if not route_report or not route_report.safety_gate_was_allow_route:
            findings.append(self._finding("critical", "missing_allow_route", "v0.25.3 allow-route gate is missing.", request.request_id))
        if route_report and not route_report.ready_for_v0_25_5:
            findings.append(self._finding("warning", "route_not_ready_for_invocation", "Route report is not ready for provider invocation.", subject_id))
        if invocation_plan.plan_status == "no_provider_invocation_required":
            findings.append(self._finding("warning", "no_provider_invocation_required", "Route does not require provider invocation.", subject_id))
        if invocation_plan.plan_status == "blocked":
            findings.append(self._finding("critical", "provider_invocation_blocked", "Provider invocation plan is blocked.", subject_id))
        for step in invocation_plan.steps:
            if any(item.precondition_type == "provider_registered" and not item.satisfied for item in step.preconditions):
                findings.append(self._finding("critical", "provider_not_registered", "Provider is not registered.", step.invocation_step_id))
                findings.append(self._finding("critical", "missing_provider_registry", "Internal provider registry is missing provider coverage.", step.invocation_step_id))
            if any(item.precondition_type == "provider_capability_available" and not item.satisfied for item in step.preconditions):
                findings.append(self._finding("critical", "provider_capability_missing", "Provider capability is missing.", step.invocation_step_id))
            if any(item.precondition_type == "provider_boundary_available" and not item.satisfied for item in step.preconditions):
                findings.append(self._finding("critical", "provider_boundary_missing", "Provider boundary is missing.", step.invocation_step_id))
            if any(not item.passed for item in step.boundary_checks):
                findings.append(self._finding("critical", "provider_boundary_failed", "Provider boundary check failed.", step.invocation_step_id))
            if step.provider_type in {item[0] for item in LOCAL_RUNTIME_SEQUENCE}:
                findings.append(self._finding("warning", "local_runtime_v024_sequence_required", "Local runtime route requires the v0.24 sequence.", step.invocation_step_id))
        if dispatches:
            findings.append(self._finding("info", "provider_invocation_created", "Internal provider dispatch records were created.", subject_id))
        if any(dispatch.dispatch_status == "failed" for dispatch in dispatches):
            findings.append(self._finding("error", "provider_invocation_failed", "Provider invocation failed.", subject_id))
        if any(dispatch.dispatch_status == "blocked" for dispatch in dispatches):
            findings.append(self._finding("critical", "provider_invocation_blocked", "Provider invocation was blocked.", subject_id))
        if invocation_plan.provider_invocation_required and not results:
            findings.append(self._finding("error", "provider_result_missing", "Required provider result reference is missing.", subject_id))
        if any(result.provider_status == "warning" for result in results):
            findings.append(self._finding("warning", "provider_result_warning", "Provider returned a warning result reference.", subject_id))
        if evidence_seed.ready_for_evidence_binder:
            findings.append(self._finding("info", "evidence_seed_created", "Evidence seed was created for v0.25.6.", evidence_seed.evidence_seed_id))
        if route_plan and route_plan.route_kind == "local_runtime_execution_flow" and not self._local_runtime_sequence_preserved(invocation_plan):
            findings.append(self._finding("critical", "local_runtime_v024_sequence_broken", "Local runtime provider sequence is broken.", subject_id))
        for finding_type, detected in (attempt_flags or {}).items():
            if detected:
                normalized = finding_type if finding_type in self.BLOCKED_ATTEMPTS else f"{finding_type}_detected"
                findings.append(self._finding("critical", normalized, f"{normalized} was detected.", subject_id))
        return findings

    def _local_runtime_sequence_preserved(self, invocation_plan: AgentProviderInvocationPlan) -> bool:
        provider_types = [step.provider_type for step in invocation_plan.steps if step.provider_type in {item[0] for item in LOCAL_RUNTIME_SEQUENCE}]
        return provider_types == [item[0] for item in LOCAL_RUNTIME_SEQUENCE] if provider_types else True

    def _finding(self, severity: str, finding_type: str, message: str, subject_id: str) -> AgentProviderInvocationFinding:
        return AgentProviderInvocationFinding(
            finding_id=f"agent_provider_invocation_finding:{finding_type}",
            severity=severity,
            finding_type=finding_type,
            message=message,
            subject_ref={"id": subject_id},
            evidence_refs=[],
            withdrawal_condition="Withdraw if the condition is removed or explicitly deferred by provider invocation policy.",
        )


class AgentProviderInvocationReportService:
    def build_request_from_route_report(self, route_report: AgentToolRoutingReport | None) -> AgentProviderInvocationRequest:
        route_plan = route_report.route_plan if route_report else None
        request = route_report.request if route_report else None
        return AgentProviderInvocationRequest(
            request_id=f"agent_provider_invocation_request:{_safe_id(route_report.report_id if route_report else None)}",
            route_report_id=route_report.report_id if route_report else None,
            route_plan_id=route_plan.route_plan_id if route_plan else None,
            safety_gate_report_id=route_plan.safety_gate_report_id if route_plan else None,
            turn_envelope_id=request.turn_envelope_id if request else None,
            source_refs=[
                _dict_ref("agent_tool_routing_report", route_report.report_id if route_report else None),
                _dict_ref("agent_tool_route_plan", route_plan.route_plan_id if route_plan else None),
            ],
        )

    def build_report(
        self,
        request_text: str = "Explain the project structure",
        route_report: AgentToolRoutingReport | None = None,
        attempt_flags: dict[str, bool] | None = None,
    ) -> AgentProviderInvocationReport:
        policy = AgentProviderInvocationPolicyService().build_policy()
        source_route_report = route_report or AgentToolRoutingReportService().build_report(request_text=request_text)
        route_plan = source_route_report.route_plan if source_route_report else None
        request = self.build_request_from_route_report(source_route_report)
        registry_provider_types = self._registry_provider_types()
        invocation_plan = AgentProviderInvocationPlanService().build_invocation_plan(
            route_plan,
            source_route_report,
            registry_provider_types,
        )
        dispatches = [AgentProviderDispatchService().dispatch_internal_provider(step) for step in invocation_plan.steps]
        results = [AgentProviderInvocationResultService().build_result(dispatch) for dispatch in dispatches]
        trace = AgentProviderInvocationTraceService().build_trace(route_plan, invocation_plan, results)
        bundle = AgentProviderResultBundleService().build_bundle(route_plan, invocation_plan, results)
        evidence_seed = AgentProviderEvidenceSeedService().build_evidence_seed(bundle)
        findings = AgentProviderInvocationFindingService().build_findings(
            request,
            source_route_report,
            route_plan,
            invocation_plan,
            dispatches,
            results,
            evidence_seed,
            attempt_flags,
        )
        report_status = self._report_status(invocation_plan, bundle, findings)
        internal_invoked = any(dispatch.internal_provider_invoked for dispatch in dispatches)
        bounded_v024 = any(dispatch.provider_type == "gated_local_runtime_execution_provider" and dispatch.internal_provider_invoked for dispatch in dispatches)
        return AgentProviderInvocationReport(
            report_id=f"agent_provider_invocation_report:{_safe_id(request.request_id)}",
            created_at=utc_now_iso(),
            policy=policy,
            request=request,
            invocation_plan=invocation_plan,
            dispatches=dispatches,
            invocation_results=results,
            invocation_trace=trace,
            result_bundle=bundle,
            evidence_seed=evidence_seed,
            findings=findings,
            report_status=report_status,
            ready_for_v0_25_6=evidence_seed.ready_for_evidence_binder and report_status in {"passed", "warning"},
            internal_provider_invocation_performed=internal_invoked,
            provider_invoked=internal_invoked,
            route_steps_executed_as_provider_invocations=internal_invoked,
            bounded_local_command_executed_via_v024=bounded_v024,
            limitations=[
                "v0.25.5 records internal provider dispatch/result references only; final response assembly is deferred to v0.25.6.",
                "Raw provider output is not inlined in v0.25.5 reports.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider invocation bypasses provider-owned boundaries.",
                "Withdraw if v0.25.5 directly reads files, performs repository search, inspects processes, starts local commands, assembles final responses, or uses an LLM judge.",
            ],
        )

    def build_all_parts(self, request_text: str = "Explain the project structure") -> dict[str, Any]:
        report = self.build_report(request_text=request_text)
        return {
            "report": report,
            "policy": report.policy,
            "request": report.request,
            "invocation_plan": report.invocation_plan,
            "steps": report.invocation_plan.steps if report.invocation_plan else [],
            "dispatches": report.dispatches,
            "results": report.invocation_results,
            "result_bundle": report.result_bundle,
            "evidence_seed": report.evidence_seed,
            "invocation_trace": report.invocation_trace,
            "findings": report.findings,
        }

    def _registry_provider_types(self) -> set[str]:
        registry = InternalProviderRegistryReportService().build_report().registry
        return {ref.provider_type for ref in registry.provider_refs}

    def _report_status(
        self,
        invocation_plan: AgentProviderInvocationPlan,
        bundle: AgentProviderResultBundle,
        findings: list[AgentProviderInvocationFinding],
    ) -> str:
        if any(item.severity == "critical" for item in findings) or invocation_plan.plan_status == "blocked" or bundle.bundle_status == "blocked":
            return "blocked"
        if any(item.severity == "error" for item in findings) or invocation_plan.plan_status == "failed" or bundle.bundle_status == "failed":
            return "failed"
        if any(item.severity == "warning" for item in findings) or invocation_plan.plan_status == "no_provider_invocation_required":
            return "warning"
        return "passed"

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": AGENT_PROVIDER_INVOCATION_VERSION,
            "layer": "agent_surface",
            "subject": "internal_provider_invocation_orchestrator",
            "principles": [
                "provider invocation is not arbitrary tool execution",
                "provider invocation must respect provider-owned policy boundaries",
                "route plan is required before provider invocation",
                "safety gate is required before route plan",
                "provider invocation result is not final answer",
                "evidence seed is not response assembly",
                "local runtime execution must remain inside v0.24 gated provider boundary",
                "response assembly is deferred to v0.25.6",
                "ask/repl is deferred to v0.25.7",
            ],
            "safety_boundary": {
                "internal_provider_invocation_performed": "conditional",
                "provider_invoked": "conditional",
                "final_response_assembled": False,
                "direct_file_access_performed": False,
                "direct_repository_search_performed": False,
                "direct_process_inspection_performed": False,
                "direct_subprocess_performed": False,
                "direct_local_command_executed": False,
                "bounded_local_command_executed_via_v024": "conditional",
                "command_rerun_performed": False,
                "ask_executed": False,
                "repl_started": False,
                "memory_promoted": False,
                "persistent_memory_written": False,
                "persona_mutated": False,
                "external_provider_adapter_implemented": False,
                "external_agent_adapter_implemented": False,
                "external_provider_invoked": False,
                "external_agent_runtime_touched": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_provider_output_inline": False,
                "llm_judge_enabled": False,
            },
            "future_direction": {
                "v0.25": "bounded agent surface",
                "v0.26": "workspace agent workbench",
                "v0.27": "memory candidate and continuity",
                "v0.29+": "external provider/agent adapters",
                "v0.30+": "external agent dominion bridge",
            },
            "next_step": AGENT_PROVIDER_INVOCATION_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "agent_internal_provider_invocation_orchestrated",
            "version": AGENT_PROVIDER_INVOCATION_VERSION,
            "source_read_models": [
                "AgentToolRoutePlanState",
                "AgentToolRoutingReportState",
                "AgentSafetyGateState",
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
            ],
            "target_read_models": [
                "AgentProviderInvocationPlanState",
                "AgentProviderInvocationStepState",
                "AgentProviderInvocationResultState",
                "AgentProviderInvocationTraceState",
                "AgentProviderResultBundleState",
                "AgentProviderEvidenceSeedState",
                "V025ReadinessState",
            ],
            "effect_types": AGENT_PROVIDER_INVOCATION_EFFECT_TYPES,
        }


def render_agent_provider_invocation_cli(parts: dict[str, Any], section: str) -> str:
    report: AgentProviderInvocationReport = parts["report"]
    plan = report.invocation_plan
    lines = [
        f"version={report.version}",
        "layer=agent_surface",
        f"internal_provider_invocation_performed={str(report.internal_provider_invocation_performed).lower()}",
        f"provider_invoked={str(report.provider_invoked).lower()}",
        f"route_steps_executed_as_provider_invocations={str(report.route_steps_executed_as_provider_invocations).lower()}",
        f"ready_for_v0_25_6={str(report.ready_for_v0_25_6).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"final_response_assembled={str(report.final_response_assembled).lower()}",
        f"direct_file_access_performed={str(report.direct_file_access_performed).lower()}",
        f"direct_repository_search_performed={str(report.direct_repository_search_performed).lower()}",
        f"direct_process_inspection_performed={str(report.direct_process_inspection_performed).lower()}",
        f"direct_subprocess_performed={str(report.direct_subprocess_performed).lower()}",
        f"direct_local_command_executed={str(report.direct_local_command_executed).lower()}",
        f"bounded_local_command_executed_via_v024={str(report.bounded_local_command_executed_via_v024).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"ask_executed={str(report.ask_executed).lower()}",
        f"repl_started={str(report.repl_started).lower()}",
        f"memory_promoted={str(report.memory_promoted).lower()}",
        f"persistent_memory_written={str(report.persistent_memory_written).lower()}",
        f"persona_mutated={str(report.persona_mutated).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"external_agent_adapter_implemented={str(report.external_agent_adapter_implemented).lower()}",
        f"external_provider_invoked={str(report.external_provider_invoked).lower()}",
        f"external_agent_runtime_touched={str(report.external_agent_runtime_touched).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_provider_output_inline={str(report.raw_provider_output_inline).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "plan":
        lines.append(f"invocation_plan_status={plan.plan_status if plan else 'missing'}")
        for step in parts["steps"]:
            lines.append(f"- invocation_step={step.step_index}:{step.provider_type}:{step.step_status}")
    elif section == "run":
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
        for dispatch in report.dispatches:
            lines.append(f"- dispatch={dispatch.provider_type}:{dispatch.dispatch_status}")
    elif section == "result":
        for result in report.invocation_results:
            lines.append(f"- result_ref={result.result_ref.result_ref_id if result.result_ref else 'missing'} status={result.provider_status}")
    elif section == "bundle":
        bundle = report.result_bundle
        lines.append(f"bundle_id={bundle.bundle_id if bundle else 'missing'}")
        lines.append(f"bundle_status={bundle.bundle_status if bundle else 'missing'}")
        lines.append(f"result_count={bundle.result_count if bundle else 0}")
    elif section == "evidence-seed":
        seed = report.evidence_seed
        lines.append(f"evidence_seed_id={seed.evidence_seed_id if seed else 'missing'}")
        lines.append(f"ready_for_evidence_binder={str(seed.ready_for_evidence_binder if seed else False).lower()}")
        lines.append(f"evidence_count={seed.evidence_count if seed else 0}")
    elif section == "trace":
        trace = report.invocation_trace
        lines.append(f"trace_id={trace.trace_id if trace else 'missing'}")
        lines.append(f"ocel_visible={str(trace.ocel_visible if trace else False).lower()}")
        lines.append(f"pig_visible={str(trace.pig_visible if trace else False).lower()}")
        lines.append(f"ocpx_visible={str(trace.ocpx_visible if trace else False).lower()}")
    elif section == "findings":
        for finding in report.findings:
            lines.append(f"- {finding.finding_type}: {finding.severity}")
    else:
        lines.append(f"report_id={report.report_id}")
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)
