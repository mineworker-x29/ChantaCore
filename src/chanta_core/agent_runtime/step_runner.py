from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any
import json

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .readonly_tools import ReadOnlyToolRegistry
from .workspace_inspection import (
    WorkspaceInspectionPathPolicy,
    WorkspaceInspectionRequest,
    WorkspaceInspectionRequestKind,
    WorkspaceInspectionResultKind,
    WorkspaceInspectionToolKind,
    WorkspaceInspectionToolResult,
    build_workspace_inspection_request,
    inspect_file_metadata_readonly,
    inspect_project_tree_readonly,
    inspect_workspace_path_readonly,
    read_text_file_safe,
    search_text_in_workspace_readonly,
    summarize_reference_inventory_readonly,
)


V0336_VERSION = "v0.33.6"
V0336_RELEASE_NAME = "v0.33.6 Agent Step Runner MVP"

MAX_SUPPLIED_MODEL_OUTPUT_CHARS = 20_000

DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS = [
    "real model invocation",
    "provider invocation",
    "general agent execution",
    "general tool execution",
    "command execution",
    "network access",
    "credential access",
    "workspace write",
    "code edit",
    "patch application",
    "reference code execution",
    "reference import",
    "dependency install",
    "secret file read",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
    "runtime trace persistence",
    "UI runtime",
    "external control",
    "authority grant",
]


class AgentStepExecutionMode(StrEnum):
    SUPPLIED_MODEL_OUTPUT_ONLY = "supplied_model_output_only"
    MOCK_MODEL_OUTPUT_ONLY = "mock_model_output_only"
    SAFE_TOOL_ONLY = "safe_tool_only"
    BOUNDED_INTERNAL_STEP = "bounded_internal_step"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class AgentStepStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    INPUT_VALIDATED = "input_validated"
    MODEL_OUTPUT_ATTACHED = "model_output_attached"
    ACTION_PROPOSED = "action_proposed"
    ACTION_ALLOWED = "action_allowed"
    ACTION_BLOCKED = "action_blocked"
    SAFE_TOOL_EXECUTED = "safe_tool_executed"
    RESPONSE_READY = "response_ready"
    COMPLETED = "completed"
    COMPLETED_WITH_BLOCKED_ACTION = "completed_with_blocked_action"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"
    BLOCKED = "blocked"


class AgentStepSourceKind(StrEnum):
    V0333_SESSION_RUNTIME = "v0333_session_runtime"
    V0332_PROMPT_ASSEMBLY_OUTPUT = "v0332_prompt_assembly_output"
    V0331_RUNTIME_PROFILE = "v0331_runtime_profile"
    V0330_RUNTIME_BOUNDARY = "v0330_runtime_boundary"
    V0334_READONLY_TOOL_REGISTRY = "v0334_readonly_tool_registry"
    V0335_WORKSPACE_INSPECTION_TOOL_PACK = "v0335_workspace_inspection_tool_pack"
    SUPPLIED_MODEL_OUTPUT = "supplied_model_output"
    MOCK_MODEL_OUTPUT = "mock_model_output"
    USER_REQUEST_REF = "user_request_ref"
    TEST_FIXTURE = "test_fixture"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    UNKNOWN = "unknown"


class AgentActionProposalKind(StrEnum):
    FINAL_RESPONSE = "final_response"
    SAFE_WORKSPACE_INSPECTION_TOOL_CALL = "safe_workspace_inspection_tool_call"
    INSPECT_PROJECT_TREE_READONLY = "inspect_project_tree_readonly"
    INSPECT_FILE_METADATA_READONLY = "inspect_file_metadata_readonly"
    READ_TEXT_FILE_SAFE = "read_text_file_safe"
    SEARCH_TEXT_IN_WORKSPACE_READONLY = "search_text_in_workspace_readonly"
    SUMMARIZE_REFERENCE_INVENTORY_READONLY = "summarize_reference_inventory_readonly"
    ASK_USER = "ask_user"
    NO_OP = "no_op"
    BLOCK = "block"
    UNSUPPORTED_TOOL_CALL = "unsupported_tool_call"
    PROHIBITED_COMMAND = "prohibited_command"
    PROHIBITED_WRITE = "prohibited_write"
    PROHIBITED_PROVIDER_INVOCATION = "prohibited_provider_invocation"
    PROHIBITED_NETWORK_ACCESS = "prohibited_network_access"
    PROHIBITED_CREDENTIAL_ACCESS = "prohibited_credential_access"
    PROHIBITED_EXTERNAL_CONTROL = "prohibited_external_control"
    UNKNOWN = "unknown"


class AgentActionDecisionKind(StrEnum):
    ALLOW_FINAL_RESPONSE = "allow_final_response"
    ALLOW_SAFE_WORKSPACE_INSPECTION = "allow_safe_workspace_inspection"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class AgentStepRiskKind(StrEnum):
    MODEL_OUTPUT_INJECTION_RISK = "model_output_injection_risk"
    BOUNDARY_OVERRIDE_RISK = "boundary_override_risk"
    UNSAFE_TOOL_REQUEST_RISK = "unsafe_tool_request_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    PROVIDER_INVOCATION_RISK = "provider_invocation_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_FILE_RISK = "secret_file_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    EXTERNAL_HARNESS_EXECUTION_RISK = "external_harness_execution_risk"
    EXTERNAL_CONTROL_RISK = "external_control_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    OCEL_EMISSION_RISK = "ocel_emission_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    UNKNOWN = "unknown"


class AgentStepResultKind(StrEnum):
    FINAL_RESPONSE_RESULT = "final_response_result"
    SAFE_TOOL_RESULT = "safe_tool_result"
    BLOCKED_ACTION_RESULT = "blocked_action_result"
    ASK_USER_RESULT = "ask_user_result"
    NO_OP_RESULT = "no_op_result"
    SAFE_FAIL_RESULT = "safe_fail_result"
    UNKNOWN = "unknown"


class AgentStepToolExecutionPosture(StrEnum):
    NO_TOOL_EXECUTION = "no_tool_execution"
    SAFE_WORKSPACE_INSPECTION_ONLY = "safe_workspace_inspection_only"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


UNSAFE_STEP_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_agent_execution",
    "ready_for_real_model_invocation",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_general_tool_execution",
    "ready_for_command_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ocel_emission",
    "ready_for_runtime_trace_persistence",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

SAFE_WORKSPACE_TOOL_NAMES = {
    "inspect_project_tree_readonly",
    "inspect_file_metadata_readonly",
    "read_text_file_safe",
    "search_text_in_workspace_readonly",
    "summarize_reference_inventory_readonly",
    "inspect_workspace_path_readonly",
}

SAFE_WORKSPACE_PROPOSAL_KINDS = {
    AgentActionProposalKind.SAFE_WORKSPACE_INSPECTION_TOOL_CALL,
    AgentActionProposalKind.INSPECT_PROJECT_TREE_READONLY,
    AgentActionProposalKind.INSPECT_FILE_METADATA_READONLY,
    AgentActionProposalKind.READ_TEXT_FILE_SAFE,
    AgentActionProposalKind.SEARCH_TEXT_IN_WORKSPACE_READONLY,
    AgentActionProposalKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY,
}

PROHIBITED_PROPOSAL_RISKS = {
    AgentActionProposalKind.PROHIBITED_COMMAND: AgentStepRiskKind.COMMAND_EXECUTION_RISK,
    AgentActionProposalKind.PROHIBITED_WRITE: AgentStepRiskKind.WORKSPACE_WRITE_RISK,
    AgentActionProposalKind.PROHIBITED_PROVIDER_INVOCATION: AgentStepRiskKind.PROVIDER_INVOCATION_RISK,
    AgentActionProposalKind.PROHIBITED_NETWORK_ACCESS: AgentStepRiskKind.NETWORK_ACCESS_RISK,
    AgentActionProposalKind.PROHIBITED_CREDENTIAL_ACCESS: AgentStepRiskKind.CREDENTIAL_ACCESS_RISK,
    AgentActionProposalKind.PROHIBITED_EXTERNAL_CONTROL: AgentStepRiskKind.EXTERNAL_CONTROL_RISK,
    AgentActionProposalKind.UNSUPPORTED_TOOL_CALL: AgentStepRiskKind.UNSAFE_TOOL_REQUEST_RISK,
    AgentActionProposalKind.UNKNOWN: AgentStepRiskKind.UNKNOWN,
}


def _validate_version_includes_v0336(version: str) -> None:
    _require_non_blank("version", version)
    if V0336_VERSION not in version:
        raise ValueError("version must include v0.33.6")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.6")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_non_negative_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_source_ref_list(values: list["AgentStepSourceRef"]) -> None:
    _validate_object_list("source_refs", values, AgentStepSourceRef)


def _validate_prohibited_runtime_actions(values: list[str]) -> None:
    _validate_string_list("prohibited_runtime_actions", values)
    lowered = [value.lower() for value in values]
    for required in DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS:
        if required.lower() not in lowered:
            raise ValueError("prohibited_runtime_actions missing v0.33.6 prohibition")


@dataclass(frozen=True)
class AgentStepFlagSet:
    flag_set_id: str
    version: str = V0336_VERSION
    agent_step_runner_constructed: bool = False
    bounded_agent_step_execution_enabled: bool = False
    supplied_model_output_processing_enabled: bool = False
    mock_model_output_processing_enabled: bool = False
    safe_workspace_tool_bridge_enabled: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0336(self.version)
        _validate_false(self, UNSAFE_STEP_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"provider_invocation", "general_tool_execution", "workspace_write"}):
            raise ValueError("AgentStepFlagSet is not general runtime readiness")


@dataclass(frozen=True)
class AgentStepSourceRef:
    source_ref_id: str
    source_kind: AgentStepSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        AgentStepSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "file_read", "execution"}):
            raise ValueError("AgentStepSourceRef is not fetch, file read, or execution")

    @property
    def fetch(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentModelStepBoundary:
    model_boundary_id: str
    execution_mode: AgentStepExecutionMode | str = AgentStepExecutionMode.SUPPLIED_MODEL_OUTPUT_ONLY
    allowed_model_output_sources: list[AgentStepSourceKind | str] = field(
        default_factory=lambda: [AgentStepSourceKind.SUPPLIED_MODEL_OUTPUT, AgentStepSourceKind.MOCK_MODEL_OUTPUT]
    )
    prohibited_model_actions: list[str] = field(default_factory=lambda: list(DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS))
    allow_real_provider_invocation: bool = False
    allow_supplied_model_output: bool = True
    allow_mock_model_output: bool = True
    allow_raw_model_output_persistence: bool = False
    source_refs: list[AgentStepSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("model_boundary_id", self.model_boundary_id)
        AgentStepExecutionMode(self.execution_mode)
        _validate_enum_list("allowed_model_output_sources", self.allowed_model_output_sources, AgentStepSourceKind)
        _validate_string_list("prohibited_model_actions", self.prohibited_model_actions)
        if self.allow_real_provider_invocation is not False:
            raise ValueError("allow_real_provider_invocation must always be False")
        if self.allow_raw_model_output_persistence is not False:
            raise ValueError("allow_raw_model_output_persistence must always be False")
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"provider_invocation", "model_invocation"}):
            raise ValueError("AgentModelStepBoundary is not provider invocation")


@dataclass(frozen=True)
class AgentSuppliedModelOutput:
    model_output_id: str
    source_kind: AgentStepSourceKind | str = AgentStepSourceKind.SUPPLIED_MODEL_OUTPUT
    raw_text: str = ""
    structured_action: dict[str, Any] | None = None
    output_summary: str = "Supplied/mock model output artifact."
    trusted: bool = False
    redacted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("model_output_id", self.model_output_id)
        AgentStepSourceKind(self.source_kind)
        if not isinstance(self.raw_text, str):
            raise TypeError("raw_text must be string")
        max_chars = self.metadata.get("max_chars", MAX_SUPPLIED_MODEL_OUTPUT_CHARS)
        if isinstance(max_chars, int) and len(self.raw_text) > max_chars:
            raise ValueError("raw_text must be bounded")
        if self.structured_action is not None and not isinstance(self.structured_action, dict):
            raise TypeError("structured_action must be dict or None")
        _require_non_blank("output_summary", self.output_summary)
        if self.trusted is not False:
            raise ValueError("trusted must default False for supplied model output")
        if _metadata_flag_true(self.metadata, {"provider_invocation", "raw_output_persistence"}):
            raise ValueError("AgentSuppliedModelOutput is not provider invocation or persistence")

    @property
    def provider_invocation(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentActionProposal:
    proposal_id: str
    model_output_id: str | None
    proposal_kind: AgentActionProposalKind | str
    proposed_tool_name: str | None = None
    proposed_tool_input: dict[str, Any] = field(default_factory=dict)
    proposed_final_response: str | None = None
    proposal_summary: str = "Agent action proposal artifact only."
    risk_kinds: list[AgentStepRiskKind | str] = field(default_factory=list)
    source_refs: list[AgentStepSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("proposal_id", self.proposal_id)
        AgentActionProposalKind(self.proposal_kind)
        if not isinstance(self.proposed_tool_input, dict):
            raise TypeError("proposed_tool_input must be dict")
        _require_non_blank("proposal_summary", self.proposal_summary)
        _validate_enum_list("risk_kinds", self.risk_kinds, AgentStepRiskKind)
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"execution", "provider_invocation", "command_execution"}):
            raise ValueError("AgentActionProposal is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentActionDecision:
    decision_id: str
    proposal_id: str
    decision_kind: AgentActionDecisionKind | str
    reason: str
    allowed_tool_name: str | None = None
    allowed_only_for_safe_workspace_inspection: bool = False
    execution_allowed: bool = False
    general_tool_execution_allowed: bool = False
    provider_invocation_allowed: bool = False
    command_execution_allowed: bool = False
    workspace_write_allowed: bool = False
    network_access_allowed: bool = False
    credential_access_allowed: bool = False
    ocel_emission_allowed: bool = False
    block_reasons: list[str] = field(default_factory=list)
    risk_kinds: list[AgentStepRiskKind | str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("proposal_id", self.proposal_id)
        decision_kind = AgentActionDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_false(
            self,
            (
                "general_tool_execution_allowed",
                "provider_invocation_allowed",
                "command_execution_allowed",
                "workspace_write_allowed",
                "network_access_allowed",
                "credential_access_allowed",
                "ocel_emission_allowed",
            ),
        )
        _validate_string_list("block_reasons", self.block_reasons)
        _validate_enum_list("risk_kinds", self.risk_kinds, AgentStepRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.execution_allowed and decision_kind != AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION:
            raise ValueError("execution_allowed may be True only for bounded safe workspace inspection")
        if decision_kind == AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION:
            if self.allowed_only_for_safe_workspace_inspection is not True:
                raise ValueError("allow_safe_workspace_inspection requires safe workspace only flag")
            if self.allowed_tool_name not in SAFE_WORKSPACE_TOOL_NAMES:
                raise ValueError("allowed_tool_name must be v0.33.5 safe workspace inspection tool")


@dataclass(frozen=True)
class AgentSafeToolExecutionRequest:
    safe_tool_request_id: str
    proposal_id: str
    decision_id: str
    tool_name: str
    tool_input: dict[str, Any] = field(default_factory=dict)
    workspace_inspection_request_ref: str | None = None
    source_refs: list[AgentStepSourceRef] = field(default_factory=list)
    ready_for_safe_workspace_inspection: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safe_tool_request_id", "proposal_id", "decision_id", "tool_name"):
            _require_non_blank(name, getattr(self, name))
        if self.tool_name not in SAFE_WORKSPACE_TOOL_NAMES:
            raise ValueError("tool_name must be v0.33.5 safe workspace inspection tool")
        if not isinstance(self.tool_input, dict):
            raise TypeError("tool_input must be dict")
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_safe_workspace_inspection and self.tool_name not in SAFE_WORKSPACE_TOOL_NAMES:
            raise ValueError("ready_for_safe_workspace_inspection is only for v0.33.5 safe tools")
        _validate_false(self, ("ready_for_general_tool_execution", "ready_for_execution"))


@dataclass(frozen=True)
class AgentSafeToolExecutionResult:
    safe_tool_result_id: str
    safe_tool_request_id: str
    tool_name: str
    workspace_inspection_result_ref: str | None
    result_summary: str
    result_kind: AgentStepResultKind | str = AgentStepResultKind.SAFE_TOOL_RESULT
    bounded_readonly: bool = True
    skipped_or_denied: bool = False
    risk_kinds: list[AgentStepRiskKind | str] = field(default_factory=list)
    source_refs: list[AgentStepSourceRef] = field(default_factory=list)
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safe_tool_result_id", "safe_tool_request_id", "tool_name", "result_summary"):
            _require_non_blank(name, getattr(self, name))
        AgentStepResultKind(self.result_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, AgentStepRiskKind)
        _validate_source_ref_list(self.source_refs)
        if self.result_kind == AgentStepResultKind.SAFE_TOOL_RESULT and self.bounded_readonly is not True:
            raise ValueError("bounded_readonly must be True for completed safe tool results")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"secret_content", "persistence"}):
            raise ValueError("AgentSafeToolExecutionResult must not contain secret content or persistence")


@dataclass(frozen=True)
class AgentStepInput:
    step_input_id: str
    source_version: str
    session_id: str | None = None
    turn_id: str | None = None
    runtime_profile_id: str | None = None
    prompt_output_id: str | None = None
    readonly_tool_registry_id: str | None = None
    workspace_tool_pack_id: str | None = None
    model_boundary: AgentModelStepBoundary = field(default_factory=lambda: build_agent_model_step_boundary())
    supplied_model_output: AgentSuppliedModelOutput | None = None
    execution_mode: AgentStepExecutionMode | str = AgentStepExecutionMode.SUPPLIED_MODEL_OUTPUT_ONLY
    task_summary: str = "Bounded internal agent step input."
    source_refs: list[AgentStepSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("step_input_id", self.step_input_id)
        _require_non_blank("source_version", self.source_version)
        _validate_version_includes_v0336(self.source_version)
        if not isinstance(self.model_boundary, AgentModelStepBoundary):
            raise TypeError("model_boundary must be AgentModelStepBoundary")
        mode = AgentStepExecutionMode(self.execution_mode)
        _require_non_blank("task_summary", self.task_summary)
        _validate_source_ref_list(self.source_refs)
        _validate_prohibited_runtime_actions(self.prohibited_runtime_actions)
        if mode == AgentStepExecutionMode.SUPPLIED_MODEL_OUTPUT_ONLY and self.supplied_model_output is None:
            raise ValueError("supplied_model_output is required for supplied_model_output_only mode")
        if _metadata_flag_true(self.metadata, {"real_model_invocation", "provider_invocation"}):
            raise ValueError("AgentStepInput is not real model invocation request")


@dataclass(frozen=True)
class AgentStepPlan:
    step_plan_id: str
    step_input_id: str
    execution_mode: AgentStepExecutionMode | str
    planned_actions: list[AgentActionProposalKind | str] = field(default_factory=list)
    allowed_tool_names: list[str] = field(default_factory=list)
    prohibited_actions: list[str] = field(default_factory=lambda: list(DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS))
    summary: str = "Bounded step plan artifact only."
    ready_for_bounded_step: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("step_plan_id", "step_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        AgentStepExecutionMode(self.execution_mode)
        _validate_enum_list("planned_actions", self.planned_actions, AgentActionProposalKind)
        _validate_string_list("allowed_tool_names", self.allowed_tool_names)
        _validate_string_list("prohibited_actions", self.prohibited_actions)
        _validate_false(self, ("ready_for_real_model_invocation", "ready_for_general_tool_execution", "ready_for_execution"))


@dataclass(frozen=True)
class AgentStepExecutionRecord:
    execution_record_id: str
    step_input_id: str
    status: AgentStepStatus | str
    proposal_id: str | None = None
    decision_id: str | None = None
    safe_tool_request_id: str | None = None
    safe_tool_result_id: str | None = None
    transition_ids: list[str] = field(default_factory=list)
    summary: str = "Bounded step execution record, not persistence."
    executed_bounded_step: bool = False
    executed_real_model_call: bool = False
    executed_general_tool_call: bool = False
    executed_command: bool = False
    wrote_workspace: bool = False
    emitted_ocel: bool = False
    source_refs: list[AgentStepSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("execution_record_id", self.execution_record_id)
        _require_non_blank("step_input_id", self.step_input_id)
        AgentStepStatus(self.status)
        _validate_string_list("transition_ids", self.transition_ids)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            ("executed_real_model_call", "executed_general_tool_call", "executed_command", "wrote_workspace", "emitted_ocel"),
        )
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"persistence", "trace_persistence"}):
            raise ValueError("AgentStepExecutionRecord is not persistence")


@dataclass(frozen=True)
class AgentStepOutput:
    step_output_id: str
    step_input_id: str
    status: AgentStepStatus | str
    result_kind: AgentStepResultKind | str
    action_proposal: AgentActionProposal | None
    action_decision: AgentActionDecision | None
    safe_tool_result: AgentSafeToolExecutionResult | None
    final_response_text: str | None
    ask_user_message: str | None
    blocked_reason: str | None
    no_op_reason: str | None
    safe_fail_reason: str | None
    execution_record: AgentStepExecutionRecord
    summary: str
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("step_output_id", "step_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        result_kind = AgentStepResultKind(self.result_kind)
        AgentStepStatus(self.status)
        if not isinstance(self.execution_record, AgentStepExecutionRecord):
            raise TypeError("execution_record must be AgentStepExecutionRecord")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if result_kind == AgentStepResultKind.SAFE_TOOL_RESULT:
            if self.safe_tool_result is None or self.safe_tool_result.bounded_readonly is not True:
                raise ValueError("safe_tool_result must be bounded read-only if present")
        if _metadata_flag_true(self.metadata, {"persistence", "provider_invocation"}):
            raise ValueError("AgentStepOutput is not persistence or provider invocation")


@dataclass(frozen=True)
class AgentStepReport:
    report_id: str
    version: str
    step_input_id: str
    step_output_id: str | None = None
    status: AgentStepStatus | str = AgentStepStatus.COMPLETED
    summary: str = "Agent step report is not runtime persistence."
    proposal_count: int = 0
    allowed_action_count: int = 0
    blocked_action_count: int = 0
    safe_tool_execution_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "step_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0336(self.version)
        AgentStepStatus(self.status)
        for name in ("proposal_count", "allowed_action_count", "blocked_action_count", "safe_tool_execution_count"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_general_agent_execution",
                "ready_for_real_model_invocation",
                "ready_for_provider_invocation",
                "ready_for_general_tool_execution",
            ),
        )


@dataclass(frozen=True)
class AgentStepRunnerMVP:
    runner_id: str
    version: str
    supported_execution_modes: list[AgentStepExecutionMode | str]
    supported_action_proposals: list[AgentActionProposalKind | str]
    allowed_safe_tool_names: list[str]
    flags: AgentStepFlagSet
    summary: str = "v0.33.6 bounded internal agent step runner."
    ready_for_bounded_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("runner_id", "version", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0336(self.version)
        _validate_enum_list("supported_execution_modes", self.supported_execution_modes, AgentStepExecutionMode)
        _validate_enum_list("supported_action_proposals", self.supported_action_proposals, AgentActionProposalKind)
        _validate_string_list("allowed_safe_tool_names", self.allowed_safe_tool_names)
        if not isinstance(self.flags, AgentStepFlagSet):
            raise TypeError("flags must be AgentStepFlagSet")
        if not agent_step_flags_preserve_unsafe_runtime_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        _validate_false(self, ("ready_for_general_agent_execution", "ready_for_real_model_invocation", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"autonomous_runtime", "provider_invocation"}):
            raise ValueError("AgentStepRunnerMVP is not autonomous runtime")


@dataclass(frozen=True)
class AgentStepRunPreview:
    run_preview_id: str
    runner_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_real_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_general_tool_execution_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_reference_dependency_install_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    no_registry_mutation_guarantee: bool = True
    no_memory_mutation_guarantee: bool = True
    no_ocel_emission_guarantee: bool = True
    no_runtime_trace_persistence_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.6")


@dataclass(frozen=True)
class AgentStepNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_real_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_general_tool_execution: bool = True
    no_command_execution: bool = True
    no_subprocess: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_file_creation: bool = True
    no_file_deletion: bool = True
    no_file_rename: bool = True
    no_chmod_chown: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_secret_file_read: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ocel_emission: bool = True
    no_runtime_trace_persistence: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0336(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.6")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0336ReadinessReport:
    report_id: str
    version: str = V0336_VERSION
    runner_id: str | None = None
    step_report_id: str | None = None
    step_output_id: str | None = None
    summary: str = "v0.33.6 enables one bounded internal agent step only."
    bounded_agent_step_execution_enabled: bool = False
    supplied_model_output_processing_enabled: bool = False
    safe_workspace_tool_bridge_enabled: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ocel_emission: bool = False
    ready_for_runtime_trace_persistence: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0336(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_STEP_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        lowered = [value.lower() for value in self.prohibited_until_later_gate]
        for required in DEFAULT_AGENT_STEP_PROHIBITED_ACTIONS:
            if required.lower() not in lowered:
                raise ValueError("prohibited_until_later_gate missing v0.33.6 prohibition")
        if _metadata_flag_true(self.metadata, {"general_runtime", "provider_invocation", "ocel_emission"}):
            raise ValueError("V0336ReadinessReport is not general runtime enablement")


def build_agent_step_flags(flag_set_id: str = "agent_step_flags:v0.33.6", **kwargs: Any) -> AgentStepFlagSet:
    return AgentStepFlagSet(flag_set_id=flag_set_id, version=V0336_VERSION, **kwargs)


def build_agent_step_source_ref(
    source_ref_id: str,
    source_kind: AgentStepSourceKind | str = AgentStepSourceKind.TEST_FIXTURE,
    source_id: str = "test_fixture",
    source_summary: str = "In-memory agent step source metadata.",
    **kwargs: Any,
) -> AgentStepSourceRef:
    return AgentStepSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_agent_model_step_boundary(model_boundary_id: str = "agent_model_step_boundary:v0.33.6", **kwargs: Any) -> AgentModelStepBoundary:
    return AgentModelStepBoundary(model_boundary_id=model_boundary_id, **kwargs)


def build_agent_supplied_model_output(model_output_id: str, **kwargs: Any) -> AgentSuppliedModelOutput:
    return AgentSuppliedModelOutput(model_output_id=model_output_id, **kwargs)


def build_agent_action_proposal(proposal_id: str, proposal_kind: AgentActionProposalKind | str, **kwargs: Any) -> AgentActionProposal:
    return AgentActionProposal(proposal_id=proposal_id, proposal_kind=proposal_kind, **kwargs)


def build_agent_action_decision(decision_id: str, proposal_id: str, decision_kind: AgentActionDecisionKind | str, **kwargs: Any) -> AgentActionDecision:
    return AgentActionDecision(
        decision_id=decision_id,
        proposal_id=proposal_id,
        decision_kind=decision_kind,
        reason=kwargs.pop("reason", "Agent action decision metadata only."),
        **kwargs,
    )


def build_agent_safe_tool_execution_request(safe_tool_request_id: str, proposal_id: str, decision_id: str, tool_name: str, **kwargs: Any) -> AgentSafeToolExecutionRequest:
    return AgentSafeToolExecutionRequest(safe_tool_request_id=safe_tool_request_id, proposal_id=proposal_id, decision_id=decision_id, tool_name=tool_name, **kwargs)


def build_agent_safe_tool_execution_result(safe_tool_result_id: str, safe_tool_request_id: str, tool_name: str, **kwargs: Any) -> AgentSafeToolExecutionResult:
    return AgentSafeToolExecutionResult(
        safe_tool_result_id=safe_tool_result_id,
        safe_tool_request_id=safe_tool_request_id,
        tool_name=tool_name,
        workspace_inspection_result_ref=kwargs.pop("workspace_inspection_result_ref", None),
        result_summary=kwargs.pop("result_summary", "Bounded safe workspace inspection tool result."),
        **kwargs,
    )


def build_agent_step_input(step_input_id: str, **kwargs: Any) -> AgentStepInput:
    return AgentStepInput(step_input_id=step_input_id, source_version=kwargs.pop("source_version", V0336_VERSION), **kwargs)


def build_agent_step_plan(step_plan_id: str, step_input_id: str, execution_mode: AgentStepExecutionMode | str = AgentStepExecutionMode.BOUNDED_INTERNAL_STEP, **kwargs: Any) -> AgentStepPlan:
    return AgentStepPlan(step_plan_id=step_plan_id, step_input_id=step_input_id, execution_mode=execution_mode, **kwargs)


def build_agent_step_execution_record(execution_record_id: str, step_input_id: str, status: AgentStepStatus | str = AgentStepStatus.COMPLETED, **kwargs: Any) -> AgentStepExecutionRecord:
    return AgentStepExecutionRecord(execution_record_id=execution_record_id, step_input_id=step_input_id, status=status, **kwargs)


def build_agent_step_output(step_output_id: str, step_input_id: str, status: AgentStepStatus | str, result_kind: AgentStepResultKind | str, execution_record: AgentStepExecutionRecord, **kwargs: Any) -> AgentStepOutput:
    return AgentStepOutput(
        step_output_id=step_output_id,
        step_input_id=step_input_id,
        status=status,
        result_kind=result_kind,
        action_proposal=kwargs.pop("action_proposal", None),
        action_decision=kwargs.pop("action_decision", None),
        safe_tool_result=kwargs.pop("safe_tool_result", None),
        final_response_text=kwargs.pop("final_response_text", None),
        ask_user_message=kwargs.pop("ask_user_message", None),
        blocked_reason=kwargs.pop("blocked_reason", None),
        no_op_reason=kwargs.pop("no_op_reason", None),
        safe_fail_reason=kwargs.pop("safe_fail_reason", None),
        execution_record=execution_record,
        summary=kwargs.pop("summary", "Bounded agent step output artifact."),
        **kwargs,
    )


def build_agent_step_report(report_id: str, step_input_id: str, **kwargs: Any) -> AgentStepReport:
    return AgentStepReport(report_id=report_id, version=V0336_VERSION, step_input_id=step_input_id, **kwargs)


def build_agent_step_runner_mvp(runner_id: str = "agent_step_runner_mvp:v0.33.6", **kwargs: Any) -> AgentStepRunnerMVP:
    return AgentStepRunnerMVP(
        runner_id=runner_id,
        version=V0336_VERSION,
        supported_execution_modes=kwargs.pop(
            "supported_execution_modes",
            [
                AgentStepExecutionMode.SUPPLIED_MODEL_OUTPUT_ONLY,
                AgentStepExecutionMode.MOCK_MODEL_OUTPUT_ONLY,
                AgentStepExecutionMode.SAFE_TOOL_ONLY,
                AgentStepExecutionMode.BOUNDED_INTERNAL_STEP,
            ],
        ),
        supported_action_proposals=kwargs.pop(
            "supported_action_proposals",
            [
                AgentActionProposalKind.FINAL_RESPONSE,
                AgentActionProposalKind.SAFE_WORKSPACE_INSPECTION_TOOL_CALL,
                AgentActionProposalKind.INSPECT_PROJECT_TREE_READONLY,
                AgentActionProposalKind.INSPECT_FILE_METADATA_READONLY,
                AgentActionProposalKind.READ_TEXT_FILE_SAFE,
                AgentActionProposalKind.SEARCH_TEXT_IN_WORKSPACE_READONLY,
                AgentActionProposalKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY,
                AgentActionProposalKind.ASK_USER,
                AgentActionProposalKind.NO_OP,
                AgentActionProposalKind.BLOCK,
            ],
        ),
        allowed_safe_tool_names=kwargs.pop("allowed_safe_tool_names", sorted(SAFE_WORKSPACE_TOOL_NAMES)),
        flags=kwargs.pop(
            "flags",
            build_agent_step_flags(
                agent_step_runner_constructed=True,
                bounded_agent_step_execution_enabled=True,
                supplied_model_output_processing_enabled=True,
                mock_model_output_processing_enabled=True,
                safe_workspace_tool_bridge_enabled=True,
                ready_for_safe_readonly_tool_execution=True,
                ready_for_safe_workspace_inspection_execution=True,
            ),
        ),
        ready_for_bounded_step_execution=kwargs.pop("ready_for_bounded_step_execution", True),
        **kwargs,
    )


def build_agent_step_run_preview(run_preview_id: str, **kwargs: Any) -> AgentStepRunPreview:
    return AgentStepRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_agent_step_no_external_side_effect_guarantee(guarantee_id: str = "agent_step_no_external_side_effect:v0.33.6", **kwargs: Any) -> AgentStepNoExternalSideEffectGuarantee:
    return AgentStepNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=V0336_VERSION, **kwargs)


def build_v0336_readiness_report(report_id: str = "v0336_readiness_report", **kwargs: Any) -> V0336ReadinessReport:
    return V0336ReadinessReport(report_id=report_id, version=V0336_VERSION, **kwargs)


def _structured_action_from_output(output: AgentSuppliedModelOutput) -> dict[str, Any]:
    if output.structured_action is not None:
        return dict(output.structured_action)
    text = output.raw_text.strip()
    if text.startswith("{") and len(text) <= MAX_SUPPLIED_MODEL_OUTPUT_CHARS:
        try:
            parsed = json.loads(text)
        except json.JSONDecodeError:
            return {"kind": "final_response", "final_response": output.raw_text}
        return parsed if isinstance(parsed, dict) else {"kind": "final_response", "final_response": output.raw_text}
    return {"kind": "final_response", "final_response": output.raw_text}


def parse_agent_action_proposal_from_supplied_output(output: AgentSuppliedModelOutput) -> AgentActionProposal:
    if not isinstance(output, AgentSuppliedModelOutput):
        raise TypeError("output must be AgentSuppliedModelOutput")
    action = _structured_action_from_output(output)
    kind_value = action.get("proposal_kind") or action.get("kind") or action.get("action") or "unknown"
    try:
        proposal_kind = AgentActionProposalKind(kind_value)
    except ValueError:
        proposal_kind = AgentActionProposalKind.UNKNOWN

    tool_name = action.get("tool_name") or action.get("proposed_tool_name")
    if proposal_kind == AgentActionProposalKind.SAFE_WORKSPACE_INSPECTION_TOOL_CALL and tool_name in SAFE_WORKSPACE_TOOL_NAMES:
        proposal_kind = AgentActionProposalKind(tool_name)
    tool_input = action.get("tool_input") or action.get("input") or {}
    if not isinstance(tool_input, dict):
        tool_input = {}
    final_response = action.get("final_response") or action.get("response")
    risks: list[AgentStepRiskKind | str] = [AgentStepRiskKind.MODEL_OUTPUT_INJECTION_RISK]
    if proposal_kind in PROHIBITED_PROPOSAL_RISKS:
        risks.append(PROHIBITED_PROPOSAL_RISKS[proposal_kind])
    return build_agent_action_proposal(
        f"{output.model_output_id}:proposal",
        proposal_kind,
        model_output_id=output.model_output_id,
        proposed_tool_name=tool_name if isinstance(tool_name, str) else None,
        proposed_tool_input=tool_input,
        proposed_final_response=final_response if isinstance(final_response, str) else None,
        proposal_summary="Parsed bounded action proposal from supplied/mock model output.",
        risk_kinds=risks,
    )


def evaluate_agent_action_proposal(
    proposal: AgentActionProposal,
    runner: AgentStepRunnerMVP,
    registry: ReadOnlyToolRegistry | None = None,
) -> AgentActionDecision:
    if not isinstance(proposal, AgentActionProposal):
        raise TypeError("proposal must be AgentActionProposal")
    if not isinstance(runner, AgentStepRunnerMVP):
        raise TypeError("runner must be AgentStepRunnerMVP")
    proposal_kind = AgentActionProposalKind(proposal.proposal_kind)

    if proposal_kind == AgentActionProposalKind.FINAL_RESPONSE:
        return build_agent_action_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            AgentActionDecisionKind.ALLOW_FINAL_RESPONSE,
            reason="Final response may be constructed from supplied/mock model output; no provider call.",
            risk_kinds=list(proposal.risk_kinds),
        )
    if proposal_kind == AgentActionProposalKind.ASK_USER:
        return build_agent_action_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            AgentActionDecisionKind.ASK_USER_REQUIRED,
            reason="Proposal requires user input and performs no external action.",
            risk_kinds=list(proposal.risk_kinds),
        )
    if proposal_kind == AgentActionProposalKind.NO_OP:
        return build_agent_action_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            AgentActionDecisionKind.NO_OP,
            reason="No-op proposal performs no action.",
            risk_kinds=list(proposal.risk_kinds),
        )
    if proposal_kind in SAFE_WORKSPACE_PROPOSAL_KINDS:
        tool_name = proposal.proposed_tool_name or (
            proposal_kind.value if proposal_kind != AgentActionProposalKind.SAFE_WORKSPACE_INSPECTION_TOOL_CALL else None
        )
        if tool_name not in runner.allowed_safe_tool_names or tool_name not in SAFE_WORKSPACE_TOOL_NAMES:
            return build_agent_action_decision(
                f"{proposal.proposal_id}:decision",
                proposal.proposal_id,
                AgentActionDecisionKind.BLOCK,
                reason="Safe tool proposal is not whitelisted for v0.33.6 runner.",
                block_reasons=["tool_not_whitelisted"],
                risk_kinds=list(proposal.risk_kinds) + [AgentStepRiskKind.UNSAFE_TOOL_REQUEST_RISK],
            )
        if registry is not None and registry.enabled_tool_names and tool_name not in registry.enabled_tool_names:
            return build_agent_action_decision(
                f"{proposal.proposal_id}:decision",
                proposal.proposal_id,
                AgentActionDecisionKind.BLOCK,
                reason="Tool is not enabled by supplied v0.33.4 registry metadata.",
                block_reasons=["tool_not_enabled_in_registry"],
                risk_kinds=list(proposal.risk_kinds) + [AgentStepRiskKind.UNSAFE_TOOL_REQUEST_RISK],
            )
        return build_agent_action_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION,
            reason="Allowed only for v0.33.5 bounded safe workspace inspection.",
            allowed_tool_name=tool_name,
            allowed_only_for_safe_workspace_inspection=True,
            execution_allowed=True,
            risk_kinds=list(proposal.risk_kinds),
        )
    if proposal_kind == AgentActionProposalKind.BLOCK:
        return build_agent_action_decision(
            f"{proposal.proposal_id}:decision",
            proposal.proposal_id,
            AgentActionDecisionKind.BLOCK,
            reason="Model output requested a blocked outcome.",
            block_reasons=["blocked_by_model_output_proposal"],
            risk_kinds=list(proposal.risk_kinds),
        )
    return build_agent_action_decision(
        f"{proposal.proposal_id}:decision",
        proposal.proposal_id,
        AgentActionDecisionKind.BLOCK,
        reason="Unsupported, unknown, or prohibited proposal is blocked.",
        block_reasons=["unsupported_or_prohibited_action"],
        risk_kinds=list(proposal.risk_kinds) + [PROHIBITED_PROPOSAL_RISKS.get(proposal_kind, AgentStepRiskKind.UNSAFE_TOOL_REQUEST_RISK)],
    )


def build_safe_workspace_inspection_request_from_action(
    proposal: AgentActionProposal,
    decision: AgentActionDecision,
) -> WorkspaceInspectionRequest:
    if AgentActionDecisionKind(decision.decision_kind) != AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION:
        raise ValueError("safe workspace inspection request requires allow decision")
    tool_name = decision.allowed_tool_name
    if tool_name not in SAFE_WORKSPACE_TOOL_NAMES:
        raise ValueError("allowed tool is not v0.33.5 safe workspace inspection tool")
    tool_input = proposal.proposed_tool_input
    path_ref = tool_input.get("path_ref") or tool_input.get("path")
    query = tool_input.get("query")
    request_kind_by_tool = {
        "inspect_project_tree_readonly": WorkspaceInspectionRequestKind.INSPECT_TREE,
        "inspect_file_metadata_readonly": WorkspaceInspectionRequestKind.INSPECT_METADATA,
        "read_text_file_safe": WorkspaceInspectionRequestKind.READ_SAFE_TEXT,
        "search_text_in_workspace_readonly": WorkspaceInspectionRequestKind.SEARCH_SAFE_TEXT,
        "summarize_reference_inventory_readonly": WorkspaceInspectionRequestKind.SUMMARIZE_REFERENCE_INVENTORY,
        "inspect_workspace_path_readonly": WorkspaceInspectionRequestKind.INSPECT_PATH,
    }
    return build_workspace_inspection_request(
        f"{proposal.proposal_id}:workspace_request",
        request_kind_by_tool[tool_name],
        WorkspaceInspectionToolKind(tool_name),
        path_ref=str(path_ref) if path_ref is not None else None,
        query=str(query) if query is not None else None,
        request_summary="v0.33.6 approved bridge request for v0.33.5 safe workspace inspection.",
    )


def execute_safe_workspace_tool_from_decision(
    proposal: AgentActionProposal,
    decision: AgentActionDecision,
    workspace_policy: WorkspaceInspectionPathPolicy,
) -> AgentSafeToolExecutionResult:
    if not isinstance(workspace_policy, WorkspaceInspectionPathPolicy):
        raise TypeError("workspace_policy must be WorkspaceInspectionPathPolicy")
    workspace_request = build_safe_workspace_inspection_request_from_action(proposal, decision)
    tool_name = decision.allowed_tool_name or ""
    safe_request = build_agent_safe_tool_execution_request(
        f"{proposal.proposal_id}:safe_tool_request",
        proposal.proposal_id,
        decision.decision_id,
        tool_name,
        tool_input=dict(proposal.proposed_tool_input),
        workspace_inspection_request_ref=workspace_request.request_id,
        ready_for_safe_workspace_inspection=True,
    )
    result_by_tool = {
        "inspect_project_tree_readonly": inspect_project_tree_readonly,
        "inspect_file_metadata_readonly": inspect_file_metadata_readonly,
        "read_text_file_safe": read_text_file_safe,
        "search_text_in_workspace_readonly": search_text_in_workspace_readonly,
        "summarize_reference_inventory_readonly": summarize_reference_inventory_readonly,
        "inspect_workspace_path_readonly": inspect_workspace_path_readonly,
    }
    workspace_result: WorkspaceInspectionToolResult = result_by_tool[tool_name](workspace_request, workspace_policy)
    skipped_or_denied = WorkspaceInspectionResultKind(workspace_result.result_kind) in {
        WorkspaceInspectionResultKind.DENIED_RESULT,
        WorkspaceInspectionResultKind.SKIPPED_RESULT,
        WorkspaceInspectionResultKind.ERROR_RESULT,
        WorkspaceInspectionResultKind.NO_OP_RESULT,
    }
    risk_kinds: list[AgentStepRiskKind | str] = list(proposal.risk_kinds)
    if skipped_or_denied:
        risk_kinds.append(AgentStepRiskKind.UNSAFE_TOOL_REQUEST_RISK)
    return build_agent_safe_tool_execution_result(
        f"{proposal.proposal_id}:safe_tool_result",
        safe_request.safe_tool_request_id,
        tool_name,
        workspace_inspection_result_ref=workspace_result.tool_result_id,
        result_summary=workspace_result.summary,
        bounded_readonly=True,
        skipped_or_denied=skipped_or_denied,
        risk_kinds=risk_kinds,
        metadata={"workspace_result_kind": str(workspace_result.result_kind)},
    )


def _record_for_output(
    step_input_id: str,
    status: AgentStepStatus,
    proposal: AgentActionProposal | None,
    decision: AgentActionDecision | None,
    safe_tool_result: AgentSafeToolExecutionResult | None = None,
) -> AgentStepExecutionRecord:
    return build_agent_step_execution_record(
        f"{step_input_id}:execution_record",
        step_input_id,
        status,
        proposal_id=proposal.proposal_id if proposal else None,
        decision_id=decision.decision_id if decision else None,
        safe_tool_result_id=safe_tool_result.safe_tool_result_id if safe_tool_result else None,
        executed_bounded_step=True,
    )


def run_agent_step_mvp(
    step_input: AgentStepInput,
    runner: AgentStepRunnerMVP,
    workspace_policy: WorkspaceInspectionPathPolicy | None = None,
    registry: ReadOnlyToolRegistry | None = None,
) -> AgentStepOutput:
    if not isinstance(step_input, AgentStepInput):
        raise TypeError("step_input must be AgentStepInput")
    if not isinstance(runner, AgentStepRunnerMVP):
        raise TypeError("runner must be AgentStepRunnerMVP")
    if step_input.supplied_model_output is None:
        proposal = build_agent_action_proposal(
            f"{step_input.step_input_id}:proposal:no_output",
            AgentActionProposalKind.BLOCK,
            proposal_summary="No supplied/mock model output was provided.",
            risk_kinds=[AgentStepRiskKind.MODEL_OUTPUT_INJECTION_RISK],
        )
        decision = evaluate_agent_action_proposal(proposal, runner, registry)
        record = _record_for_output(step_input.step_input_id, AgentStepStatus.BLOCKED, proposal, decision)
        return build_agent_step_output(
            f"{step_input.step_input_id}:output",
            step_input.step_input_id,
            AgentStepStatus.BLOCKED,
            AgentStepResultKind.BLOCKED_ACTION_RESULT,
            record,
            action_proposal=proposal,
            action_decision=decision,
            blocked_reason=decision.reason,
            summary="Blocked because supplied/mock model output is required.",
        )

    proposal = parse_agent_action_proposal_from_supplied_output(step_input.supplied_model_output)
    decision = evaluate_agent_action_proposal(proposal, runner, registry)
    decision_kind = AgentActionDecisionKind(decision.decision_kind)
    if decision_kind == AgentActionDecisionKind.ALLOW_FINAL_RESPONSE:
        final_response = proposal.proposed_final_response or step_input.supplied_model_output.raw_text
        record = _record_for_output(step_input.step_input_id, AgentStepStatus.RESPONSE_READY, proposal, decision)
        return build_agent_step_output(
            f"{step_input.step_input_id}:output",
            step_input.step_input_id,
            AgentStepStatus.RESPONSE_READY,
            AgentStepResultKind.FINAL_RESPONSE_RESULT,
            record,
            action_proposal=proposal,
            action_decision=decision,
            final_response_text=final_response,
            summary="Final response constructed from supplied/mock model output only.",
        )
    if decision_kind == AgentActionDecisionKind.ALLOW_SAFE_WORKSPACE_INSPECTION:
        if workspace_policy is None:
            blocked = build_agent_action_decision(
                f"{proposal.proposal_id}:decision:blocked_no_policy",
                proposal.proposal_id,
                AgentActionDecisionKind.BLOCK,
                reason="Workspace policy is required for safe workspace inspection bridge.",
                block_reasons=["missing_workspace_policy"],
                risk_kinds=list(proposal.risk_kinds) + [AgentStepRiskKind.UNSAFE_TOOL_REQUEST_RISK],
            )
            record = _record_for_output(step_input.step_input_id, AgentStepStatus.ACTION_BLOCKED, proposal, blocked)
            return build_agent_step_output(
                f"{step_input.step_input_id}:output",
                step_input.step_input_id,
                AgentStepStatus.ACTION_BLOCKED,
                AgentStepResultKind.BLOCKED_ACTION_RESULT,
                record,
                action_proposal=proposal,
                action_decision=blocked,
                blocked_reason=blocked.reason,
                summary="Safe tool bridge blocked because policy was missing.",
            )
        safe_tool_result = execute_safe_workspace_tool_from_decision(proposal, decision, workspace_policy)
        record = _record_for_output(step_input.step_input_id, AgentStepStatus.SAFE_TOOL_EXECUTED, proposal, decision, safe_tool_result)
        return build_agent_step_output(
            f"{step_input.step_input_id}:output",
            step_input.step_input_id,
            AgentStepStatus.SAFE_TOOL_EXECUTED,
            AgentStepResultKind.SAFE_TOOL_RESULT,
            record,
            action_proposal=proposal,
            action_decision=decision,
            safe_tool_result=safe_tool_result,
            summary="Executed only approved v0.33.5 bounded safe workspace inspection tool.",
        )
    if decision_kind == AgentActionDecisionKind.ASK_USER_REQUIRED:
        record = _record_for_output(step_input.step_input_id, AgentStepStatus.NO_OP, proposal, decision)
        return build_agent_step_output(
            f"{step_input.step_input_id}:output",
            step_input.step_input_id,
            AgentStepStatus.NO_OP,
            AgentStepResultKind.ASK_USER_RESULT,
            record,
            action_proposal=proposal,
            action_decision=decision,
            ask_user_message=proposal.proposed_final_response or decision.reason,
            summary="Ask-user result performs no external action.",
        )
    if decision_kind == AgentActionDecisionKind.NO_OP:
        record = _record_for_output(step_input.step_input_id, AgentStepStatus.NO_OP, proposal, decision)
        return build_agent_step_output(
            f"{step_input.step_input_id}:output",
            step_input.step_input_id,
            AgentStepStatus.NO_OP,
            AgentStepResultKind.NO_OP_RESULT,
            record,
            action_proposal=proposal,
            action_decision=decision,
            no_op_reason=decision.reason,
            summary="No-op result performs no external action.",
        )
    record = _record_for_output(step_input.step_input_id, AgentStepStatus.ACTION_BLOCKED, proposal, decision)
    return build_agent_step_output(
        f"{step_input.step_input_id}:output",
        step_input.step_input_id,
        AgentStepStatus.ACTION_BLOCKED,
        AgentStepResultKind.BLOCKED_ACTION_RESULT,
        record,
        action_proposal=proposal,
        action_decision=decision,
        blocked_reason=decision.reason,
        summary="Unsafe or unsupported model-output action proposal was blocked.",
    )


def agent_step_flags_preserve_unsafe_runtime_false(flags: AgentStepFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_STEP_FLAG_NAMES)


def agent_step_output_is_not_persistence(output: AgentStepOutput) -> bool:
    return output.ready_for_execution is False and output.execution_record.emitted_ocel is False


def agent_step_decision_preserves_no_external_side_effect(decision: AgentActionDecision) -> bool:
    return (
        decision.general_tool_execution_allowed is False
        and decision.provider_invocation_allowed is False
        and decision.command_execution_allowed is False
        and decision.workspace_write_allowed is False
        and decision.network_access_allowed is False
        and decision.credential_access_allowed is False
        and decision.ocel_emission_allowed is False
    )


def agent_step_runner_is_not_autonomous_runtime(runner: AgentStepRunnerMVP) -> bool:
    return (
        runner.ready_for_bounded_step_execution is True
        and runner.ready_for_general_agent_execution is False
        and runner.ready_for_real_model_invocation is False
        and runner.ready_for_execution is False
    )


def v0336_readiness_report_is_not_general_runtime_ready(report: V0336ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_STEP_FLAG_NAMES)
