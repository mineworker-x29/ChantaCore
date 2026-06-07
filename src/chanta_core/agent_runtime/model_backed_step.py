from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .model_output_quarantine import (
    ModelOutputActionCandidate,
    ModelOutputActionCandidateKind,
    ModelOutputActionQuarantinePacket,
    ModelOutputActionRouteKind,
    ModelOutputActionSafeRoute,
    build_model_output_action_quarantine_packet_from_candidates,
    extract_model_output_action_candidates_from_response_envelope,
    validate_model_output_action_quarantine_packet,
)
from .model_request import ModelRequestEnvelope
from .model_response import ModelResponseEnvelope, build_model_response_envelope_from_supplied_text
from .provider_adapter import (
    ExistingProviderBoundaryAdapterDescriptor,
    ExistingProviderBoundaryInvocationInput,
    ExistingProviderBoundaryInvocationResult,
    ExistingProviderInvocationMode,
    build_existing_provider_boundary_invocation_input,
    invoke_existing_provider_boundary_adapter,
)
from .step_runner import (
    AgentStepInput,
    AgentStepOutput,
    AgentStepResultKind,
    AgentStepRunnerMVP,
    AgentStepStatus,
    AgentSuppliedModelOutput,
    WorkspaceInspectionPathPolicy,
    build_agent_step_input,
    build_agent_supplied_model_output,
    run_agent_step_mvp,
)


V0346_VERSION = "v0.34.6"
V0346_RELEASE_NAME = "v0.34.6 Agent Step Runner Model Integration"
DEFAULT_MAX_MODEL_BACKED_STEP_TEXT_CHARS = 4000

DEFAULT_MODEL_BACKED_STEP_PROHIBITED_ACTIONS = [
    "direct provider SDK",
    "direct provider invocation",
    "direct network",
    "credential access",
    "secret read",
    "unquarantined action",
    "general agent execution",
    "autonomous loop",
    "general tool",
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch proposal",
    "patch application",
    "reference execution",
    "reference import",
    "reference dependency install",
    "raw prompt persistence",
    "raw response persistence",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_MODEL_BACKED_STEP_WITHDRAWAL_CONDITIONS = [
    "Any direct provider SDK, direct network, credential, secret, shell, command, write, edit, patch, or raw persistence path is introduced.",
    "Any autonomous agent loop, general tool execution, unquarantined action execution, reference execution, or unsafe readiness flag is introduced.",
    "Any bounded step path bypasses v0.34.5 quarantine or v0.33.6 Agent Step Runner.",
]

UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_direct_provider_invocation",
    "ready_for_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_direct_network_access",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_proposal",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_raw_prompt_persistence",
    "ready_for_raw_response_persistence",
    "ready_for_raw_model_output_persistence",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

SAFE_MODEL_BACKED_STEP_ROUTES = {
    "final_response_step_route",
    "ask_user_step_route",
    "no_op_step_route",
    "safe_workspace_inspection_step_route",
}


class ModelBackedStepIntegrationMode(StrEnum):
    RESPONSE_ENVELOPE_ONLY = "response_envelope_only"
    QUARANTINE_PACKET_ONLY = "quarantine_packet_only"
    EXISTING_BOUNDARY_THEN_QUARANTINE = "existing_boundary_then_quarantine"
    SUPPLIED_RESPONSE_THEN_QUARANTINE = "supplied_response_then_quarantine"
    MOCK_RESPONSE_THEN_QUARANTINE = "mock_response_then_quarantine"
    BOUNDED_AGENT_STEP_RUNNER_BRIDGE = "bounded_agent_step_runner_bridge"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ModelBackedStepStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    INPUT_VALIDATED = "input_validated"
    REQUEST_ENVELOPE_ATTACHED = "request_envelope_attached"
    RESPONSE_ENVELOPE_ATTACHED = "response_envelope_attached"
    QUARANTINE_PACKET_ATTACHED = "quarantine_packet_attached"
    QUARANTINE_VALIDATED = "quarantine_validated"
    STEP_RUNNER_INPUT_BUILT = "step_runner_input_built"
    BOUNDED_STEP_ALLOWED = "bounded_step_allowed"
    BOUNDED_STEP_COMPLETED = "bounded_step_completed"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    ASK_USER_REQUIRED = "ask_user_required"
    SAFE_FAILED = "safe_failed"
    FUTURE_GATED = "future_gated"
    COMPLETED = "completed"


class ModelBackedStepSourceKind(StrEnum):
    V0345_QUARANTINE_PACKET = "v0345_quarantine_packet"
    V0344_PROVIDER_BOUNDARY_RESULT = "v0344_provider_boundary_result"
    V0343_RESPONSE_ENVELOPE = "v0343_response_envelope"
    V0342_REQUEST_ENVELOPE = "v0342_request_envelope"
    V0341_PROVIDER_PROFILE = "v0341_provider_profile"
    V0336_AGENT_STEP_RUNNER = "v0336_agent_step_runner"
    V0335_WORKSPACE_INSPECTION_TOOL_PACK = "v0335_workspace_inspection_tool_pack"
    V0332_PROMPT_ASSEMBLY = "v0332_prompt_assembly"
    SUPPLIED_RESPONSE_FIXTURE = "supplied_response_fixture"
    MOCK_RESPONSE_FIXTURE = "mock_response_fixture"
    TEST_FIXTURE = "test_fixture"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    UNKNOWN = "unknown"


class ModelBackedStepDecisionKind(StrEnum):
    ALLOW_NON_MUTATING_FINAL_RESPONSE_STEP = "allow_non_mutating_final_response_step"
    ALLOW_NON_MUTATING_ASK_USER_STEP = "allow_non_mutating_ask_user_step"
    ALLOW_NON_MUTATING_NO_OP_STEP = "allow_non_mutating_no_op_step"
    ALLOW_SAFE_WORKSPACE_INSPECTION_STEP = "allow_safe_workspace_inspection_step"
    BLOCK_UNSAFE_CANDIDATE = "block_unsafe_candidate"
    BLOCK_MISSING_QUARANTINE = "block_missing_quarantine"
    BLOCK_MISSING_RESPONSE_ENVELOPE = "block_missing_response_envelope"
    BLOCK_MISSING_RUNNER = "block_missing_runner"
    BLOCK_POLICY_VIOLATION = "block_policy_violation"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ModelBackedStepRouteKind(StrEnum):
    FINAL_RESPONSE_STEP_ROUTE = "final_response_step_route"
    ASK_USER_STEP_ROUTE = "ask_user_step_route"
    NO_OP_STEP_ROUTE = "no_op_step_route"
    SAFE_WORKSPACE_INSPECTION_STEP_ROUTE = "safe_workspace_inspection_step_route"
    BLOCKED_ROUTE = "blocked_route"
    REVIEW_REQUIRED_ROUTE = "review_required_route"
    FUTURE_GATE_ROUTE = "future_gate_route"
    UNKNOWN = "unknown"


class ModelBackedStepRiskKind(StrEnum):
    UNQUARANTINED_MODEL_OUTPUT_RISK = "unquarantined_model_output_risk"
    UNSAFE_ACTION_CANDIDATE_RISK = "unsafe_action_candidate_risk"
    GENERAL_TOOL_EXECUTION_RISK = "general_tool_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    PATCH_PROPOSAL_RISK = "patch_proposal_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    DIRECT_PROVIDER_INVOCATION_RISK = "direct_provider_invocation_risk"
    PROVIDER_SDK_BYPASS_RISK = "provider_sdk_bypass_risk"
    DIRECT_NETWORK_ACCESS_RISK = "direct_network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_READ_RISK = "secret_read_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    EXTERNAL_HARNESS_EXECUTION_RISK = "external_harness_execution_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    RAW_PROMPT_PERSISTENCE_RISK = "raw_prompt_persistence_risk"
    RAW_RESPONSE_PERSISTENCE_RISK = "raw_response_persistence_risk"
    UNKNOWN = "unknown"


class ModelBackedStepOutcomeKind(StrEnum):
    FINAL_RESPONSE_OUTPUT = "final_response_output"
    ASK_USER_OUTPUT = "ask_user_output"
    NO_OP_OUTPUT = "no_op_output"
    SAFE_WORKSPACE_INSPECTION_OUTPUT = "safe_workspace_inspection_output"
    BLOCKED_OUTPUT = "blocked_output"
    SAFE_FAIL_OUTPUT = "safe_fail_output"
    FUTURE_GATED_OUTPUT = "future_gated_output"
    UNKNOWN = "unknown"


class ModelBackedStepReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    INTEGRATION_CONTRACT_READY = "integration_contract_ready"
    QUARANTINE_BRIDGE_READY = "quarantine_bridge_ready"
    BOUNDED_MODEL_BACKED_STEP_READY = "bounded_model_backed_step_ready"
    DESIGN_HANDOFF_READY_FOR_V0347 = "design_handoff_ready_for_v0347"
    DESIGN_HANDOFF_READY_FOR_V0348 = "design_handoff_ready_for_v0348"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version_includes_v0346(version: str) -> None:
    _require_non_blank("version", version)
    if V0346_VERSION not in version:
        raise ValueError("version must include v0.34.6")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.6")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.6")


def _validate_non_negative(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_metadata_no_unsafe_side_effect(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be dict")
    if _metadata_flag_true(
        metadata,
        {
            "direct_provider_invocation",
            "provider_sdk_invocation",
            "direct_network_access",
            "network_access",
            "credential_access",
            "secret_read",
            "general_tool_execution",
            "unquarantined_action_execution",
            "general_agent_execution",
            "autonomous_agent_runtime",
            "shell_execution",
            "subprocess_execution",
            "command_execution",
            "workspace_write",
            "code_edit",
            "patch_proposal",
            "patch_application",
            "reference_code_execution",
            "reference_import",
            "raw_prompt_persistence",
            "raw_response_persistence",
            "persistent_trace_write",
            "ui_runtime",
            "authority_grant",
        },
    ):
        raise ValueError("v0.34.6 metadata cannot imply unsafe side effects")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


def _bounded_text(value: str | None, limit: int = DEFAULT_MAX_MODEL_BACKED_STEP_TEXT_CHARS) -> tuple[str | None, bool]:
    if value is None:
        return None, False
    if len(value) <= limit:
        return value, False
    return value[:limit], True


def _route_from_quarantine_route(route_kind: ModelOutputActionRouteKind | str) -> ModelBackedStepRouteKind:
    route = ModelOutputActionRouteKind(route_kind)
    if route == ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE:
        return ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE
    if route == ModelOutputActionRouteKind.ASK_USER_ROUTE:
        return ModelBackedStepRouteKind.ASK_USER_STEP_ROUTE
    if route == ModelOutputActionRouteKind.NO_OP_ROUTE:
        return ModelBackedStepRouteKind.NO_OP_STEP_ROUTE
    if route in {ModelOutputActionRouteKind.FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE, ModelOutputActionRouteKind.FUTURE_AGENT_STEP_RUNNER_ROUTE}:
        return ModelBackedStepRouteKind.SAFE_WORKSPACE_INSPECTION_STEP_ROUTE
    return ModelBackedStepRouteKind.BLOCKED_ROUTE


def _candidate_by_id(packet: ModelOutputActionQuarantinePacket, candidate_id: str | None) -> ModelOutputActionCandidate | None:
    if candidate_id is None:
        return None
    for candidate in packet.candidate_set.candidates:
        if candidate.candidate_id == candidate_id:
            return candidate
    return None


def _select_safe_route(packet: ModelOutputActionQuarantinePacket) -> tuple[ModelOutputActionSafeRoute | None, ModelOutputActionCandidate | None]:
    for route in packet.safe_routes:
        candidate = _candidate_by_id(packet, route.candidate_id)
        if candidate is None:
            continue
        if ModelOutputActionRouteKind(route.route_kind) == ModelOutputActionRouteKind.FUTURE_PATCH_PROPOSAL_TRACK:
            continue
        return route, candidate
    return None, None


@dataclass(frozen=True)
class ModelBackedStepFlagSet:
    flag_set_id: str
    version: str = V0346_VERSION
    model_backed_step_integration_constructed: bool = False
    quarantine_bridge_available: bool = False
    step_runner_bridge_available: bool = False
    bounded_model_backed_step_execution_available: bool = False
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_execution: bool = False
    ready_for_bounded_model_backed_step_execution: bool = False
    ready_for_agent_step_runner_model_integration: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0346(self.version)
        _validate_false(self, UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.6")
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepSourceRef:
    source_ref_id: str
    source_kind: ModelBackedStepSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ModelBackedStepSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_unsafe_side_effect(self.metadata)

    @property
    def execution(self) -> bool:
        return False

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelBackedStepIntegrationPolicy:
    integration_policy_id: str
    allowed_modes: list[ModelBackedStepIntegrationMode | str] = field(default_factory=list)
    allowed_routes: list[ModelBackedStepRouteKind | str] = field(default_factory=list)
    blocked_routes: list[ModelBackedStepRouteKind | str] = field(default_factory=list)
    prohibited_risks: list[ModelBackedStepRiskKind | str] = field(default_factory=list)
    allow_existing_boundary_adapter_call: bool = False
    allow_quarantine_packet_input: bool = True
    allow_response_envelope_input: bool = True
    allow_final_response_step: bool = True
    allow_ask_user_step: bool = True
    allow_no_op_step: bool = True
    allow_safe_workspace_inspection_step: bool = True
    allow_general_tool_execution: bool = False
    allow_unquarantined_action_execution: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_patch_proposal: bool = False
    allow_patch_application: bool = False
    allow_shell_execution: bool = False
    allow_direct_provider_invocation: bool = False
    allow_provider_sdk_invocation: bool = False
    allow_direct_network_access: bool = False
    allow_credential_access: bool = False
    allow_secret_read: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("integration_policy_id", self.integration_policy_id)
        _validate_enum_list("allowed_modes", self.allowed_modes, ModelBackedStepIntegrationMode)
        _validate_enum_list("allowed_routes", self.allowed_routes, ModelBackedStepRouteKind)
        _validate_enum_list("blocked_routes", self.blocked_routes, ModelBackedStepRouteKind)
        _validate_enum_list("prohibited_risks", self.prohibited_risks, ModelBackedStepRiskKind)
        _validate_false(
            self,
            (
                "allow_general_tool_execution",
                "allow_unquarantined_action_execution",
                "allow_workspace_write",
                "allow_code_edit",
                "allow_patch_proposal",
                "allow_patch_application",
                "allow_shell_execution",
                "allow_direct_provider_invocation",
                "allow_provider_sdk_invocation",
                "allow_direct_network_access",
                "allow_credential_access",
                "allow_secret_read",
            ),
        )
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepInput:
    step_input_id: str
    source_version: str
    request_envelope_id: str | None = None
    response_envelope_id: str | None = None
    quarantine_packet_id: str | None = None
    provider_boundary_result_id: str | None = None
    agent_step_runner_id: str | None = None
    workspace_tool_pack_id: str | None = None
    integration_mode: ModelBackedStepIntegrationMode | str = ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY
    task_summary: str = "Bounded model-backed step integration input."
    source_refs: list[ModelBackedStepSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_BACKED_STEP_PROHIBITED_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("step_input_id", self.step_input_id)
        _require_non_blank("source_version", self.source_version)
        _validate_version_includes_v0346(self.source_version)
        ModelBackedStepIntegrationMode(self.integration_mode)
        _require_non_blank("task_summary", self.task_summary)
        _validate_object_list("source_refs", self.source_refs, ModelBackedStepSourceRef)
        _validate_contains_terms(
            "prohibited_runtime_actions",
            self.prohibited_runtime_actions,
            [
                "direct provider SDK",
                "direct network",
                "credential access",
                "secret read",
                "unquarantined action",
                "general tool",
                "shell",
                "command",
                "write",
                "edit",
                "patch proposal",
                "patch application",
                "reference execution",
                "reference import",
                "install",
            ],
        )
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepPlan:
    step_plan_id: str
    step_input_id: str
    integration_mode: ModelBackedStepIntegrationMode | str
    selected_route: ModelBackedStepRouteKind | str | None = None
    required_artifacts: list[str] = field(default_factory=list)
    missing_artifacts: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    summary: str = "Model-backed step plan artifact only."
    ready_for_bounded_step: bool = False
    ready_for_general_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("step_plan_id", self.step_plan_id)
        _require_non_blank("step_input_id", self.step_input_id)
        ModelBackedStepIntegrationMode(self.integration_mode)
        if self.selected_route is not None:
            ModelBackedStepRouteKind(self.selected_route)
        for name in ("required_artifacts", "missing_artifacts", "blocked_reasons"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_general_execution",))
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepDecision:
    decision_id: str
    step_input_id: str
    decision_kind: ModelBackedStepDecisionKind | str
    route_kind: ModelBackedStepRouteKind | str
    reason: str
    risk_kinds: list[ModelBackedStepRiskKind | str] = field(default_factory=list)
    bounded_step_allowed: bool = False
    safe_workspace_inspection_allowed: bool = False
    existing_boundary_adapter_call_allowed: bool = False
    general_tool_execution_allowed: bool = False
    unquarantined_action_execution_allowed: bool = False
    direct_provider_invocation_allowed: bool = False
    provider_sdk_allowed: bool = False
    network_allowed: bool = False
    credential_access_allowed: bool = False
    workspace_write_allowed: bool = False
    patch_proposal_allowed: bool = False
    patch_application_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("step_input_id", self.step_input_id)
        decision_kind = ModelBackedStepDecisionKind(self.decision_kind)
        route_kind = ModelBackedStepRouteKind(self.route_kind)
        _require_non_blank("reason", self.reason)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelBackedStepRiskKind)
        if self.bounded_step_allowed and route_kind.value not in SAFE_MODEL_BACKED_STEP_ROUTES:
            raise ValueError("bounded_step_allowed requires a safe model-backed route")
        if self.safe_workspace_inspection_allowed and route_kind != ModelBackedStepRouteKind.SAFE_WORKSPACE_INSPECTION_STEP_ROUTE:
            raise ValueError("safe_workspace_inspection_allowed only applies to safe workspace route")
        if decision_kind in {
            ModelBackedStepDecisionKind.BLOCK_UNSAFE_CANDIDATE,
            ModelBackedStepDecisionKind.BLOCK_MISSING_QUARANTINE,
            ModelBackedStepDecisionKind.BLOCK_MISSING_RESPONSE_ENVELOPE,
            ModelBackedStepDecisionKind.BLOCK_MISSING_RUNNER,
            ModelBackedStepDecisionKind.BLOCK_POLICY_VIOLATION,
        } and self.bounded_step_allowed:
            raise ValueError("blocked model-backed decisions cannot allow bounded step")
        _validate_false(
            self,
            (
                "general_tool_execution_allowed",
                "unquarantined_action_execution_allowed",
                "direct_provider_invocation_allowed",
                "provider_sdk_allowed",
                "network_allowed",
                "credential_access_allowed",
                "workspace_write_allowed",
                "patch_proposal_allowed",
                "patch_application_allowed",
            ),
        )
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepQuarantineBridge:
    quarantine_bridge_id: str
    quarantine_packet_id: str
    selected_safe_route_id: str | None
    selected_candidate_id: str | None
    selected_route_kind: ModelBackedStepRouteKind | str | None
    bridge_summary: str
    safe_route_available: bool = False
    blocked: bool = False
    blocked_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("quarantine_bridge_id", self.quarantine_bridge_id)
        _require_non_blank("quarantine_packet_id", self.quarantine_packet_id)
        if self.selected_route_kind is not None:
            ModelBackedStepRouteKind(self.selected_route_kind)
        _require_non_blank("bridge_summary", self.bridge_summary)
        if self.safe_route_available and self.blocked:
            raise ValueError("safe route cannot be both available and blocked")
        _validate_metadata_no_unsafe_side_effect(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelBackedStepRunnerBridge:
    runner_bridge_id: str
    step_input_id: str
    decision_id: str
    agent_step_input_ref: str | None
    agent_step_output_ref: str | None
    bridge_summary: str
    called_v0336_runner: bool = False
    called_general_tool: bool = False
    called_shell: bool = False
    wrote_workspace: bool = False
    produced_bounded_output: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("runner_bridge_id", "step_input_id", "decision_id", "bridge_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_false(self, ("called_general_tool", "called_shell", "wrote_workspace"))
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepExecutionRecord:
    execution_record_id: str
    step_input_id: str
    decision_id: str
    status: ModelBackedStepStatus | str
    provider_boundary_result_id: str | None = None
    response_envelope_id: str | None = None
    quarantine_packet_id: str | None = None
    agent_step_output_id: str | None = None
    executed_bounded_model_backed_step: bool = False
    executed_existing_boundary_adapter_call: bool = False
    executed_direct_provider_call: bool = False
    executed_provider_sdk: bool = False
    used_direct_network: bool = False
    read_credentials: bool = False
    read_secrets: bool = False
    executed_general_tool: bool = False
    executed_unquarantined_action: bool = False
    executed_shell: bool = False
    wrote_workspace: bool = False
    generated_patch_proposal: bool = False
    applied_patch: bool = False
    persisted_raw_prompt: bool = False
    persisted_raw_response: bool = False
    summary: str = "Model-backed step execution record; not persistent log."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("execution_record_id", "step_input_id", "decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        ModelBackedStepStatus(self.status)
        _validate_false(
            self,
            (
                "executed_direct_provider_call",
                "executed_provider_sdk",
                "used_direct_network",
                "read_credentials",
                "read_secrets",
                "executed_general_tool",
                "executed_unquarantined_action",
                "executed_shell",
                "wrote_workspace",
                "generated_patch_proposal",
                "applied_patch",
                "persisted_raw_prompt",
                "persisted_raw_response",
            ),
        )
        _validate_metadata_no_unsafe_side_effect(self.metadata)

    @property
    def persistent_log(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelBackedStepOutput:
    step_output_id: str
    step_input_id: str
    status: ModelBackedStepStatus | str
    outcome_kind: ModelBackedStepOutcomeKind | str
    final_response_text: str | None
    ask_user_message: str | None
    no_op_reason: str | None
    blocked_reason: str | None
    safe_fail_reason: str | None
    agent_step_output_ref: str | None
    provider_boundary_result_ref: str | None
    quarantine_packet_ref: str | None
    execution_record: ModelBackedStepExecutionRecord
    summary: str
    redacted: bool = False
    truncated: bool = False
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("step_output_id", "step_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        ModelBackedStepStatus(self.status)
        ModelBackedStepOutcomeKind(self.outcome_kind)
        if self.final_response_text is not None and len(self.final_response_text) > DEFAULT_MAX_MODEL_BACKED_STEP_TEXT_CHARS:
            raise ValueError("final_response_text must be bounded")
        if self.ask_user_message is not None and len(self.ask_user_message) > DEFAULT_MAX_MODEL_BACKED_STEP_TEXT_CHARS:
            raise ValueError("ask_user_message must be bounded")
        if not isinstance(self.execution_record, ModelBackedStepExecutionRecord):
            raise TypeError("execution_record must be ModelBackedStepExecutionRecord")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_no_unsafe_side_effect(self.metadata)

    @property
    def persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelBackedStepReport:
    report_id: str
    version: str
    step_input_id: str
    step_output_id: str | None = None
    status: ModelBackedStepStatus | str = ModelBackedStepStatus.COMPLETED
    readiness_level: ModelBackedStepReadinessLevel | str = ModelBackedStepReadinessLevel.BOUNDED_MODEL_BACKED_STEP_READY
    summary: str = "Model-backed step report; not production certification."
    bounded_step_count: int = 0
    blocked_step_count: int = 0
    safe_fail_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_bounded_model_backed_step_execution: bool = False
    ready_for_general_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "step_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0346(self.version)
        ModelBackedStepStatus(self.status)
        ModelBackedStepReadinessLevel(self.readiness_level)
        for name in ("bounded_step_count", "blocked_step_count", "safe_fail_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_general_execution",))
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepRunPreview:
    run_preview_id: str
    step_input_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_direct_provider_invocation_guarantee: bool = True
    no_provider_sdk_invocation_guarantee: bool = True
    no_direct_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_general_tool_execution_guarantee: bool = True
    no_unquarantined_action_execution_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_proposal_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_dependency_install_guarantee: bool = True
    no_raw_prompt_persistence_guarantee: bool = True
    no_raw_response_persistence_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelBackedStepNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_direct_provider_invocation: bool = True
    no_provider_sdk_invocation: bool = True
    no_direct_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_general_tool_execution: bool = True
    no_unquarantined_action_execution: bool = True
    no_general_agent_execution: bool = True
    no_autonomous_agent_runtime: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_proposal: bool = True
    no_patch_application: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_raw_prompt_persistence: bool = True
    no_raw_response_persistence: bool = True
    no_persistent_trace_write: bool = True
    no_external_trace_sink: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0346(self.version)
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_unsafe_side_effect(self.metadata)


@dataclass(frozen=True)
class V0346ReadinessReport:
    report_id: str
    version: str
    step_output_id: str | None = None
    step_report_id: str | None = None
    execution_record_id: str | None = None
    summary: str = "v0.34.6 bounded model-backed step integration readiness only."
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_execution: bool = False
    ready_for_bounded_model_backed_step_execution: bool = False
    ready_for_agent_step_runner_model_integration: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_direct_provider_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_BACKED_STEP_PROHIBITED_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_BACKED_STEP_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0346(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            [
                "direct provider invocation",
                "provider SDK",
                "direct network",
                "credential access",
                "secret read",
                "general tool",
                "unquarantined action",
                "general agent",
                "autonomous",
                "shell",
                "subprocess",
                "command",
                "workspace write",
                "code edit",
                "patch proposal",
                "patch application",
                "reference execution",
                "reference import",
                "install",
                "raw prompt persistence",
                "raw response persistence",
                "persistent trace",
                "external trace sink",
                "UI runtime",
                "external control",
                "authority grant",
            ],
        )
        _validate_metadata_no_unsafe_side_effect(self.metadata)

    @property
    def general_execution_ready(self) -> bool:
        return False


def build_model_backed_step_flags(flag_set_id: str = "model_backed_step_flags:v0.34.6", **kwargs: Any) -> ModelBackedStepFlagSet:
    return ModelBackedStepFlagSet(flag_set_id=flag_set_id, version=kwargs.pop("version", V0346_VERSION), **kwargs)


def build_model_backed_step_source_ref(
    source_ref_id: str = "model_backed_step_source_ref:v0.34.6",
    source_kind: ModelBackedStepSourceKind | str = ModelBackedStepSourceKind.TEST_FIXTURE,
    source_id: str = "model_backed_step_source:v0.34.6",
    source_summary: str = "Model-backed step source reference metadata only.",
    **kwargs: Any,
) -> ModelBackedStepSourceRef:
    return ModelBackedStepSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_model_backed_step_integration_policy(
    integration_policy_id: str = "model_backed_step_integration_policy:v0.34.6",
    **kwargs: Any,
) -> ModelBackedStepIntegrationPolicy:
    return ModelBackedStepIntegrationPolicy(integration_policy_id=integration_policy_id, **kwargs)


def default_model_backed_step_integration_policy(**kwargs: Any) -> ModelBackedStepIntegrationPolicy:
    return build_model_backed_step_integration_policy(
        allowed_modes=kwargs.pop(
            "allowed_modes",
            [
                ModelBackedStepIntegrationMode.RESPONSE_ENVELOPE_ONLY,
                ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY,
                ModelBackedStepIntegrationMode.SUPPLIED_RESPONSE_THEN_QUARANTINE,
                ModelBackedStepIntegrationMode.MOCK_RESPONSE_THEN_QUARANTINE,
                ModelBackedStepIntegrationMode.BOUNDED_AGENT_STEP_RUNNER_BRIDGE,
            ],
        ),
        allowed_routes=kwargs.pop(
            "allowed_routes",
            [
                ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE,
                ModelBackedStepRouteKind.ASK_USER_STEP_ROUTE,
                ModelBackedStepRouteKind.NO_OP_STEP_ROUTE,
                ModelBackedStepRouteKind.SAFE_WORKSPACE_INSPECTION_STEP_ROUTE,
            ],
        ),
        blocked_routes=kwargs.pop("blocked_routes", [ModelBackedStepRouteKind.BLOCKED_ROUTE, ModelBackedStepRouteKind.UNKNOWN]),
        prohibited_risks=kwargs.pop(
            "prohibited_risks",
            [
                ModelBackedStepRiskKind.UNSAFE_ACTION_CANDIDATE_RISK,
                ModelBackedStepRiskKind.GENERAL_TOOL_EXECUTION_RISK,
                ModelBackedStepRiskKind.WORKSPACE_WRITE_RISK,
                ModelBackedStepRiskKind.PATCH_PROPOSAL_RISK,
                ModelBackedStepRiskKind.PATCH_APPLICATION_RISK,
                ModelBackedStepRiskKind.DIRECT_PROVIDER_INVOCATION_RISK,
                ModelBackedStepRiskKind.PROVIDER_SDK_BYPASS_RISK,
                ModelBackedStepRiskKind.DIRECT_NETWORK_ACCESS_RISK,
                ModelBackedStepRiskKind.CREDENTIAL_ACCESS_RISK,
                ModelBackedStepRiskKind.SECRET_READ_RISK,
                ModelBackedStepRiskKind.REFERENCE_EXECUTION_RISK,
            ],
        ),
        **kwargs,
    )


def build_model_backed_step_input(step_input_id: str = "model_backed_step_input:v0.34.6", **kwargs: Any) -> ModelBackedStepInput:
    return ModelBackedStepInput(step_input_id=step_input_id, source_version=kwargs.pop("source_version", V0346_VERSION), **kwargs)


def build_model_backed_step_plan(step_plan_id: str = "model_backed_step_plan:v0.34.6", **kwargs: Any) -> ModelBackedStepPlan:
    return ModelBackedStepPlan(
        step_plan_id=step_plan_id,
        step_input_id=kwargs.pop("step_input_id", "model_backed_step_input:v0.34.6"),
        integration_mode=kwargs.pop("integration_mode", ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY),
        **kwargs,
    )


def build_model_backed_step_decision(decision_id: str = "model_backed_step_decision:v0.34.6", **kwargs: Any) -> ModelBackedStepDecision:
    return ModelBackedStepDecision(
        decision_id=decision_id,
        step_input_id=kwargs.pop("step_input_id", "model_backed_step_input:v0.34.6"),
        decision_kind=kwargs.pop("decision_kind", ModelBackedStepDecisionKind.ALLOW_NON_MUTATING_FINAL_RESPONSE_STEP),
        route_kind=kwargs.pop("route_kind", ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE),
        reason=kwargs.pop("reason", "Bounded model-backed step allowed only through quarantined safe route."),
        **kwargs,
    )


def build_model_backed_step_quarantine_bridge(quarantine_bridge_id: str = "model_backed_step_quarantine_bridge:v0.34.6", **kwargs: Any) -> ModelBackedStepQuarantineBridge:
    return ModelBackedStepQuarantineBridge(
        quarantine_bridge_id=quarantine_bridge_id,
        quarantine_packet_id=kwargs.pop("quarantine_packet_id", "model_output_action_quarantine_packet:v0.34.5"),
        selected_safe_route_id=kwargs.pop("selected_safe_route_id", None),
        selected_candidate_id=kwargs.pop("selected_candidate_id", None),
        selected_route_kind=kwargs.pop("selected_route_kind", None),
        bridge_summary=kwargs.pop("bridge_summary", "Quarantine bridge metadata; not execution."),
        **kwargs,
    )


def build_model_backed_step_runner_bridge(runner_bridge_id: str = "model_backed_step_runner_bridge:v0.34.6", **kwargs: Any) -> ModelBackedStepRunnerBridge:
    return ModelBackedStepRunnerBridge(
        runner_bridge_id=runner_bridge_id,
        step_input_id=kwargs.pop("step_input_id", "model_backed_step_input:v0.34.6"),
        decision_id=kwargs.pop("decision_id", "model_backed_step_decision:v0.34.6"),
        agent_step_input_ref=kwargs.pop("agent_step_input_ref", None),
        agent_step_output_ref=kwargs.pop("agent_step_output_ref", None),
        bridge_summary=kwargs.pop("bridge_summary", "v0.33.6 runner bridge; bounded only."),
        **kwargs,
    )


def build_model_backed_step_execution_record(execution_record_id: str = "model_backed_step_execution_record:v0.34.6", **kwargs: Any) -> ModelBackedStepExecutionRecord:
    return ModelBackedStepExecutionRecord(
        execution_record_id=execution_record_id,
        step_input_id=kwargs.pop("step_input_id", "model_backed_step_input:v0.34.6"),
        decision_id=kwargs.pop("decision_id", "model_backed_step_decision:v0.34.6"),
        status=kwargs.pop("status", ModelBackedStepStatus.PLANNED),
        **kwargs,
    )


def build_model_backed_step_output(step_output_id: str = "model_backed_step_output:v0.34.6", **kwargs: Any) -> ModelBackedStepOutput:
    return ModelBackedStepOutput(
        step_output_id=step_output_id,
        step_input_id=kwargs.pop("step_input_id", "model_backed_step_input:v0.34.6"),
        status=kwargs.pop("status", ModelBackedStepStatus.COMPLETED),
        outcome_kind=kwargs.pop("outcome_kind", ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT),
        final_response_text=kwargs.pop("final_response_text", None),
        ask_user_message=kwargs.pop("ask_user_message", None),
        no_op_reason=kwargs.pop("no_op_reason", None),
        blocked_reason=kwargs.pop("blocked_reason", None),
        safe_fail_reason=kwargs.pop("safe_fail_reason", None),
        agent_step_output_ref=kwargs.pop("agent_step_output_ref", None),
        provider_boundary_result_ref=kwargs.pop("provider_boundary_result_ref", None),
        quarantine_packet_ref=kwargs.pop("quarantine_packet_ref", None),
        execution_record=kwargs.pop("execution_record", build_model_backed_step_execution_record()),
        summary=kwargs.pop("summary", "Model-backed step output; not persistence."),
        **kwargs,
    )


def build_model_backed_step_report(report_id: str = "model_backed_step_report:v0.34.6", **kwargs: Any) -> ModelBackedStepReport:
    return ModelBackedStepReport(report_id=report_id, version=kwargs.pop("version", V0346_VERSION), step_input_id=kwargs.pop("step_input_id", "model_backed_step_input:v0.34.6"), **kwargs)


def build_model_backed_step_run_preview(run_preview_id: str = "model_backed_step_run_preview:v0.34.6", **kwargs: Any) -> ModelBackedStepRunPreview:
    return ModelBackedStepRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_model_backed_step_no_external_side_effect_guarantee(
    guarantee_id: str = "model_backed_step_no_external_side_effect_guarantee:v0.34.6",
    **kwargs: Any,
) -> ModelBackedStepNoExternalSideEffectGuarantee:
    return ModelBackedStepNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0346_VERSION), **kwargs)


def build_v0346_readiness_report(report_id: str = "v0346_readiness_report", **kwargs: Any) -> V0346ReadinessReport:
    return V0346ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0346_VERSION),
        ready_for_v0347_model_invocation_ocel_trace_packet=kwargs.pop("ready_for_v0347_model_invocation_ocel_trace_packet", True),
        ready_for_v0348_cli_model_backed_agent_step_surface=kwargs.pop("ready_for_v0348_cli_model_backed_agent_step_surface", True),
        ready_for_bounded_model_backed_step_execution=kwargs.pop("ready_for_bounded_model_backed_step_execution", True),
        ready_for_agent_step_runner_model_integration=kwargs.pop("ready_for_agent_step_runner_model_integration", True),
        completed_items=kwargs.pop("completed_items", ["quarantine bridge", "v0.33.6 runner bridge", "bounded model-backed step output"]),
        future_track_items=kwargs.pop("future_track_items", ["model invocation OCEL trace packet", "CLI model-backed agent step surface"]),
        **kwargs,
    )


def plan_model_backed_step(input: ModelBackedStepInput, policy: ModelBackedStepIntegrationPolicy | None = None) -> ModelBackedStepPlan:
    if not isinstance(input, ModelBackedStepInput):
        raise TypeError("input must be ModelBackedStepInput")
    policy = policy or default_model_backed_step_integration_policy()
    mode = ModelBackedStepIntegrationMode(input.integration_mode)
    missing: list[str] = []
    required = ["v0.34.5 quarantine packet", "v0.33.6 agent step runner"]
    if mode == ModelBackedStepIntegrationMode.RESPONSE_ENVELOPE_ONLY:
        required.append("v0.34.3 response envelope")
    if mode == ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE:
        required.append("v0.34.4 existing boundary adapter")
    if mode not in policy.allowed_modes:
        missing.append("policy_allowed_mode")
    if input.quarantine_packet_id is None and mode in {
        ModelBackedStepIntegrationMode.QUARANTINE_PACKET_ONLY,
        ModelBackedStepIntegrationMode.BOUNDED_AGENT_STEP_RUNNER_BRIDGE,
    }:
        missing.append("quarantine_packet")
    selected_route = None if missing else ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE
    return build_model_backed_step_plan(
        step_input_id=input.step_input_id,
        integration_mode=mode,
        selected_route=selected_route,
        required_artifacts=required,
        missing_artifacts=missing,
        blocked_reasons=[] if not missing else ["missing_required_artifact_or_policy_gate"],
        ready_for_bounded_step=not missing,
        summary="Model-backed step planned without general runtime expansion.",
    )


def _decision_for_route(
    step_input_id: str,
    route_kind: ModelBackedStepRouteKind,
    policy: ModelBackedStepIntegrationPolicy,
) -> ModelBackedStepDecision:
    if route_kind not in policy.allowed_routes or route_kind in policy.blocked_routes:
        return build_model_backed_step_decision(
            step_input_id=step_input_id,
            decision_kind=ModelBackedStepDecisionKind.BLOCK_POLICY_VIOLATION,
            route_kind=ModelBackedStepRouteKind.BLOCKED_ROUTE,
            bounded_step_allowed=False,
            reason="Selected quarantine route is not allowed by v0.34.6 integration policy.",
            risk_kinds=[ModelBackedStepRiskKind.UNSAFE_ACTION_CANDIDATE_RISK],
        )
    if route_kind == ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE and policy.allow_final_response_step:
        return build_model_backed_step_decision(step_input_id=step_input_id, bounded_step_allowed=True)
    if route_kind == ModelBackedStepRouteKind.ASK_USER_STEP_ROUTE and policy.allow_ask_user_step:
        return build_model_backed_step_decision(
            step_input_id=step_input_id,
            decision_kind=ModelBackedStepDecisionKind.ALLOW_NON_MUTATING_ASK_USER_STEP,
            route_kind=route_kind,
            bounded_step_allowed=True,
            reason="Ask-user route allowed only as bounded non-mutating step.",
        )
    if route_kind == ModelBackedStepRouteKind.NO_OP_STEP_ROUTE and policy.allow_no_op_step:
        return build_model_backed_step_decision(
            step_input_id=step_input_id,
            decision_kind=ModelBackedStepDecisionKind.ALLOW_NON_MUTATING_NO_OP_STEP,
            route_kind=route_kind,
            bounded_step_allowed=True,
            reason="No-op route allowed only as bounded non-mutating step.",
        )
    if route_kind == ModelBackedStepRouteKind.SAFE_WORKSPACE_INSPECTION_STEP_ROUTE and policy.allow_safe_workspace_inspection_step:
        return build_model_backed_step_decision(
            step_input_id=step_input_id,
            decision_kind=ModelBackedStepDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION_STEP,
            route_kind=route_kind,
            bounded_step_allowed=True,
            safe_workspace_inspection_allowed=True,
            reason="Safe workspace route may run only through v0.33.6/v0.33.5 bounded bridge.",
        )
    return build_model_backed_step_decision(
        step_input_id=step_input_id,
        decision_kind=ModelBackedStepDecisionKind.BLOCK_POLICY_VIOLATION,
        route_kind=ModelBackedStepRouteKind.BLOCKED_ROUTE,
        bounded_step_allowed=False,
        reason="Safe route was disabled by v0.34.6 policy.",
        risk_kinds=[ModelBackedStepRiskKind.UNSAFE_ACTION_CANDIDATE_RISK],
    )


def decide_model_backed_step(
    input: ModelBackedStepInput,
    quarantine_packet: ModelOutputActionQuarantinePacket | None = None,
    policy: ModelBackedStepIntegrationPolicy | None = None,
) -> ModelBackedStepDecision:
    if not isinstance(input, ModelBackedStepInput):
        raise TypeError("input must be ModelBackedStepInput")
    policy = policy or default_model_backed_step_integration_policy()
    if quarantine_packet is None:
        return build_model_backed_step_decision(
            step_input_id=input.step_input_id,
            decision_kind=ModelBackedStepDecisionKind.BLOCK_MISSING_QUARANTINE,
            route_kind=ModelBackedStepRouteKind.BLOCKED_ROUTE,
            bounded_step_allowed=False,
            reason="Model-backed step requires v0.34.5 quarantine packet.",
            risk_kinds=[ModelBackedStepRiskKind.UNQUARANTINED_MODEL_OUTPUT_RISK],
        )
    validate_model_output_action_quarantine_packet(quarantine_packet)
    safe_route, _candidate = _select_safe_route(quarantine_packet)
    if safe_route is None:
        return build_model_backed_step_decision(
            step_input_id=input.step_input_id,
            decision_kind=ModelBackedStepDecisionKind.BLOCK_UNSAFE_CANDIDATE,
            route_kind=ModelBackedStepRouteKind.BLOCKED_ROUTE,
            bounded_step_allowed=False,
            reason="Quarantine packet does not contain a v0.34.6-safe route.",
            risk_kinds=[ModelBackedStepRiskKind.UNSAFE_ACTION_CANDIDATE_RISK],
        )
    return _decision_for_route(input.step_input_id, _route_from_quarantine_route(safe_route.route_kind), policy)


def _structured_action_from_route(route: ModelBackedStepRouteKind, candidate: ModelOutputActionCandidate) -> dict[str, Any]:
    preview = candidate.candidate_preview
    if route == ModelBackedStepRouteKind.FINAL_RESPONSE_STEP_ROUTE:
        return {"kind": "final_response", "final_response": preview}
    if route == ModelBackedStepRouteKind.ASK_USER_STEP_ROUTE:
        return {"kind": "ask_user", "final_response": preview or "User input is required."}
    if route == ModelBackedStepRouteKind.NO_OP_STEP_ROUTE:
        return {"kind": "no_op", "final_response": preview or "No operation requested."}
    tool_name = candidate.metadata.get("tool_name", "inspect_project_tree_readonly")
    tool_input = candidate.metadata.get("tool_input", {})
    if not isinstance(tool_input, dict):
        tool_input = {}
    return {"kind": str(tool_name), "tool_input": tool_input}


def build_agent_step_input_from_model_quarantine(
    step_input: ModelBackedStepInput,
    quarantine_packet: ModelOutputActionQuarantinePacket,
    selected_route: ModelOutputActionSafeRoute | None = None,
) -> AgentStepInput:
    if not isinstance(step_input, ModelBackedStepInput):
        raise TypeError("step_input must be ModelBackedStepInput")
    if not isinstance(quarantine_packet, ModelOutputActionQuarantinePacket):
        raise TypeError("quarantine_packet must be ModelOutputActionQuarantinePacket")
    route = selected_route
    candidate: ModelOutputActionCandidate | None = None
    if route is None:
        route, candidate = _select_safe_route(quarantine_packet)
    elif route is not None:
        candidate = _candidate_by_id(quarantine_packet, route.candidate_id)
    if route is None or candidate is None:
        raise ValueError("safe quarantine route is required to build AgentStepInput")
    model_route = _route_from_quarantine_route(route.route_kind)
    structured_action = _structured_action_from_route(model_route, candidate)
    supplied_output = build_agent_supplied_model_output(
        f"{step_input.step_input_id}:agent_supplied_model_output",
        source_kind="supplied_model_output",
        structured_action=structured_action,
        raw_text=candidate.candidate_preview,
        output_summary="v0.34.6 bounded bridge output from v0.34.5 quarantined safe route.",
        redacted=True,
    )
    return build_agent_step_input(
        f"{step_input.step_input_id}:v0336_agent_step_input",
        supplied_model_output=supplied_output,
        task_summary=step_input.task_summary,
        workspace_tool_pack_id=step_input.workspace_tool_pack_id,
    )


def _blocked_output(
    step_input: ModelBackedStepInput,
    decision: ModelBackedStepDecision,
    reason: str,
    outcome_kind: ModelBackedStepOutcomeKind = ModelBackedStepOutcomeKind.BLOCKED_OUTPUT,
    status: ModelBackedStepStatus = ModelBackedStepStatus.BLOCKED,
    provider_boundary_result_id: str | None = None,
    quarantine_packet_id: str | None = None,
) -> ModelBackedStepOutput:
    record = build_model_backed_step_execution_record(
        f"{step_input.step_input_id}:record:block",
        step_input_id=step_input.step_input_id,
        decision_id=decision.decision_id,
        status=status,
        provider_boundary_result_id=provider_boundary_result_id,
        quarantine_packet_id=quarantine_packet_id,
        summary="Model-backed step blocked before unsafe side effects.",
    )
    return build_model_backed_step_output(
        f"{step_input.step_input_id}:output:block",
        step_input_id=step_input.step_input_id,
        status=status,
        outcome_kind=outcome_kind,
        blocked_reason=reason if outcome_kind == ModelBackedStepOutcomeKind.BLOCKED_OUTPUT else None,
        safe_fail_reason=reason if outcome_kind == ModelBackedStepOutcomeKind.SAFE_FAIL_OUTPUT else None,
        quarantine_packet_ref=quarantine_packet_id,
        provider_boundary_result_ref=provider_boundary_result_id,
        execution_record=record,
        summary="Model-backed step returned safe blocked output.",
    )


def _packet_from_response_envelope(response_envelope: ModelResponseEnvelope) -> ModelOutputActionQuarantinePacket:
    candidate_set = extract_model_output_action_candidates_from_response_envelope(response_envelope)
    return build_model_output_action_quarantine_packet_from_candidates(
        candidate_set.candidates,
        source_response_envelope_id=response_envelope.response_envelope_id,
    )


def _packet_from_provider_result(result: ExistingProviderBoundaryInvocationResult) -> ModelOutputActionQuarantinePacket | None:
    if result.response_text_preview is None:
        return None
    response_envelope = build_model_response_envelope_from_supplied_text(
        result.response_text_preview,
        response_envelope_id=f"model_response_envelope:{result.invocation_result_id}:v0.34.6",
    )
    return _packet_from_response_envelope(response_envelope)


def _output_from_agent_step_output(
    step_input: ModelBackedStepInput,
    decision: ModelBackedStepDecision,
    agent_output: AgentStepOutput,
    quarantine_packet_id: str,
    provider_result_id: str | None = None,
) -> ModelBackedStepOutput:
    final_text, final_truncated = _bounded_text(agent_output.final_response_text)
    ask_text, ask_truncated = _bounded_text(agent_output.ask_user_message)
    outcome_kind = ModelBackedStepOutcomeKind.BLOCKED_OUTPUT
    status = ModelBackedStepStatus.BOUNDED_STEP_COMPLETED
    if AgentStepResultKind(agent_output.result_kind) == AgentStepResultKind.FINAL_RESPONSE_RESULT:
        outcome_kind = ModelBackedStepOutcomeKind.FINAL_RESPONSE_OUTPUT
    elif AgentStepResultKind(agent_output.result_kind) == AgentStepResultKind.ASK_USER_RESULT:
        outcome_kind = ModelBackedStepOutcomeKind.ASK_USER_OUTPUT
        status = ModelBackedStepStatus.ASK_USER_REQUIRED
    elif AgentStepResultKind(agent_output.result_kind) == AgentStepResultKind.NO_OP_RESULT:
        outcome_kind = ModelBackedStepOutcomeKind.NO_OP_OUTPUT
        status = ModelBackedStepStatus.NO_OP
    elif AgentStepResultKind(agent_output.result_kind) == AgentStepResultKind.SAFE_TOOL_RESULT:
        outcome_kind = ModelBackedStepOutcomeKind.SAFE_WORKSPACE_INSPECTION_OUTPUT
    elif AgentStepResultKind(agent_output.result_kind) == AgentStepResultKind.SAFE_FAIL_RESULT:
        outcome_kind = ModelBackedStepOutcomeKind.SAFE_FAIL_OUTPUT
        status = ModelBackedStepStatus.SAFE_FAILED
    else:
        status = ModelBackedStepStatus.BLOCKED
    record = build_model_backed_step_execution_record(
        f"{step_input.step_input_id}:record:completed",
        step_input_id=step_input.step_input_id,
        decision_id=decision.decision_id,
        status=status,
        provider_boundary_result_id=provider_result_id,
        quarantine_packet_id=quarantine_packet_id,
        agent_step_output_id=agent_output.step_output_id,
        executed_bounded_model_backed_step=True,
        executed_existing_boundary_adapter_call=provider_result_id is not None,
        summary="One bounded model-backed step completed through v0.33.6 bridge.",
    )
    return build_model_backed_step_output(
        f"{step_input.step_input_id}:output",
        step_input_id=step_input.step_input_id,
        status=status,
        outcome_kind=outcome_kind,
        final_response_text=final_text,
        ask_user_message=ask_text,
        no_op_reason=agent_output.no_op_reason,
        blocked_reason=agent_output.blocked_reason,
        safe_fail_reason=agent_output.safe_fail_reason,
        agent_step_output_ref=agent_output.step_output_id,
        provider_boundary_result_ref=provider_result_id,
        quarantine_packet_ref=quarantine_packet_id,
        execution_record=record,
        redacted=True,
        truncated=final_truncated or ask_truncated,
        ready_for_v0347_model_invocation_ocel_trace_packet=True,
        ready_for_v0348_cli_model_backed_agent_step_surface=True,
        summary="Bounded model-backed step output; no general runtime readiness.",
    )


def run_model_backed_agent_step(
    input: ModelBackedStepInput,
    policy: ModelBackedStepIntegrationPolicy | None = None,
    quarantine_packet: ModelOutputActionQuarantinePacket | None = None,
    response_envelope: ModelResponseEnvelope | None = None,
    request_envelope: ModelRequestEnvelope | None = None,
    provider_adapter: ExistingProviderBoundaryAdapterDescriptor | None = None,
    provider_boundary_callable: Any | None = None,
    agent_step_runner: AgentStepRunnerMVP | None = None,
    workspace_policy: WorkspaceInspectionPathPolicy | None = None,
) -> ModelBackedStepOutput:
    if not isinstance(input, ModelBackedStepInput):
        raise TypeError("input must be ModelBackedStepInput")
    policy = policy or default_model_backed_step_integration_policy()
    mode = ModelBackedStepIntegrationMode(input.integration_mode)
    provider_result: ExistingProviderBoundaryInvocationResult | None = None

    if mode == ModelBackedStepIntegrationMode.EXISTING_BOUNDARY_THEN_QUARANTINE:
        if not policy.allow_existing_boundary_adapter_call or provider_adapter is None:
            decision = build_model_backed_step_decision(
                step_input_id=input.step_input_id,
                decision_kind=ModelBackedStepDecisionKind.BLOCK_POLICY_VIOLATION,
                route_kind=ModelBackedStepRouteKind.BLOCKED_ROUTE,
                bounded_step_allowed=False,
                reason="Existing boundary adapter path was not explicitly supplied and policy-approved.",
                risk_kinds=[ModelBackedStepRiskKind.DIRECT_PROVIDER_INVOCATION_RISK],
            )
            return _blocked_output(input, decision, decision.reason)
        invocation_input: ExistingProviderBoundaryInvocationInput = build_existing_provider_boundary_invocation_input(
            f"{input.step_input_id}:provider_invocation_input",
            request_envelope_id=input.request_envelope_id or "model_request_envelope:v0.34.6",
            adapter_id=provider_adapter.adapter_id,
            invocation_mode=ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY,
            prompt_payload_preview=input.task_summary,
            bounded_prompt_payload={"task_summary": input.task_summary},
            task_summary=input.task_summary,
        )
        provider_result = invoke_existing_provider_boundary_adapter(
            invocation_input,
            provider_adapter,
            request_envelope=request_envelope,
            boundary_callable=provider_boundary_callable,
        )
        quarantine_packet = _packet_from_provider_result(provider_result)

    if quarantine_packet is None and response_envelope is not None:
        quarantine_packet = _packet_from_response_envelope(response_envelope)

    decision = decide_model_backed_step(input, quarantine_packet, policy)
    if quarantine_packet is None:
        return _blocked_output(input, decision, decision.reason, quarantine_packet_id=input.quarantine_packet_id, provider_boundary_result_id=provider_result.invocation_result_id if provider_result else None)
    if not decision.bounded_step_allowed:
        return _blocked_output(input, decision, decision.reason, quarantine_packet_id=quarantine_packet.quarantine_packet_id, provider_boundary_result_id=provider_result.invocation_result_id if provider_result else None)
    if agent_step_runner is None:
        missing_runner_decision = build_model_backed_step_decision(
            step_input_id=input.step_input_id,
            decision_kind=ModelBackedStepDecisionKind.BLOCK_MISSING_RUNNER,
            route_kind=ModelBackedStepRouteKind.FUTURE_GATE_ROUTE,
            bounded_step_allowed=False,
            reason="v0.33.6 Agent Step Runner must be explicitly supplied for v0.34.6 execution.",
            risk_kinds=[ModelBackedStepRiskKind.UNSAFE_ACTION_CANDIDATE_RISK],
        )
        return _blocked_output(
            input,
            missing_runner_decision,
            missing_runner_decision.reason,
            outcome_kind=ModelBackedStepOutcomeKind.FUTURE_GATED_OUTPUT,
            status=ModelBackedStepStatus.FUTURE_GATED,
            quarantine_packet_id=quarantine_packet.quarantine_packet_id,
            provider_boundary_result_id=provider_result.invocation_result_id if provider_result else None,
        )
    safe_route, _candidate = _select_safe_route(quarantine_packet)
    if safe_route is None:
        return _blocked_output(input, decision, "No v0.34.6-safe route is available.", quarantine_packet_id=quarantine_packet.quarantine_packet_id)
    agent_input = build_agent_step_input_from_model_quarantine(input, quarantine_packet, safe_route)
    try:
        agent_output = run_agent_step_mvp(agent_input, agent_step_runner, workspace_policy=workspace_policy)
    except Exception as exc:
        safe_fail_decision = build_model_backed_step_decision(
            step_input_id=input.step_input_id,
            decision_kind=ModelBackedStepDecisionKind.REQUIRE_REVIEW,
            route_kind=decision.route_kind,
            bounded_step_allowed=False,
            reason="v0.33.6 runner safe-failed during bounded model-backed step.",
            risk_kinds=[ModelBackedStepRiskKind.UNSAFE_ACTION_CANDIDATE_RISK],
        )
        return _blocked_output(
            input,
            safe_fail_decision,
            str(exc),
            outcome_kind=ModelBackedStepOutcomeKind.SAFE_FAIL_OUTPUT,
            status=ModelBackedStepStatus.SAFE_FAILED,
            quarantine_packet_id=quarantine_packet.quarantine_packet_id,
            provider_boundary_result_id=provider_result.invocation_result_id if provider_result else None,
        )
    return _output_from_agent_step_output(
        input,
        decision,
        agent_output,
        quarantine_packet.quarantine_packet_id,
        provider_result_id=provider_result.invocation_result_id if provider_result else None,
    )


def model_backed_step_flags_preserve_unsafe_false(flags: ModelBackedStepFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES) and flags.production_certified is False


def model_backed_step_decision_blocks_unsafe(decision: ModelBackedStepDecision) -> bool:
    return (
        decision.general_tool_execution_allowed is False
        and decision.unquarantined_action_execution_allowed is False
        and decision.direct_provider_invocation_allowed is False
        and decision.provider_sdk_allowed is False
        and decision.network_allowed is False
        and decision.credential_access_allowed is False
        and decision.workspace_write_allowed is False
        and decision.patch_proposal_allowed is False
        and decision.patch_application_allowed is False
    )


def model_backed_step_output_is_not_persistence(output: ModelBackedStepOutput) -> bool:
    return output.persistence is False and output.ready_for_execution is False and output.execution_record.persisted_raw_response is False


def model_backed_step_execution_record_confirms_no_unsafe_side_effect(record: ModelBackedStepExecutionRecord) -> bool:
    return (
        record.executed_direct_provider_call is False
        and record.executed_provider_sdk is False
        and record.used_direct_network is False
        and record.read_credentials is False
        and record.read_secrets is False
        and record.executed_general_tool is False
        and record.executed_unquarantined_action is False
        and record.executed_shell is False
        and record.wrote_workspace is False
        and record.generated_patch_proposal is False
        and record.applied_patch is False
        and record.persisted_raw_prompt is False
        and record.persisted_raw_response is False
    )


def v0346_readiness_report_is_not_general_execution_ready(report: V0346ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_MODEL_BACKED_STEP_FLAG_NAMES) and report.general_execution_ready is False
