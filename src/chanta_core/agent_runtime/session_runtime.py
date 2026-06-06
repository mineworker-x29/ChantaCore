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


V0333_VERSION = "v0.33.3"
V0333_RELEASE_NAME = "v0.33.3 Session Runtime / Turn State Machine"

DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS = [
    "model_invocation",
    "model invocation",
    "provider_invocation",
    "provider invocation",
    "agent_step_execution",
    "agent step execution",
    "model_step_execution",
    "model step execution",
    "tool_execution",
    "tool execution",
    "read_only_tool_execution",
    "read-only tool execution",
    "workspace_inspection_execution",
    "workspace inspection execution",
    "network_access",
    "network access",
    "credential_access",
    "credential access",
    "command_execution",
    "command execution",
    "workspace_write",
    "workspace write",
    "code_edit",
    "code edit",
    "patch_application",
    "patch application",
    "reference_file_access",
    "reference file access",
    "reference_code_execution",
    "reference code execution",
    "reference_import",
    "reference import",
    "dependency_install",
    "dependency install",
    "secret_file_read",
    "secret file read",
    "registry_mutation",
    "registry mutation",
    "memory_mutation",
    "memory mutation",
    "ocel_emission",
    "OCEL emission",
    "runtime_trace_persistence",
    "runtime trace persistence",
    "ui_runtime",
    "UI runtime",
    "external_control",
    "external control",
    "authority_grant",
    "authority grant",
]


class AgentRuntimeSessionState(StrEnum):
    UNKNOWN = "unknown"
    CREATED = "created"
    BOUNDARY_ATTACHED = "boundary_attached"
    PROFILE_ATTACHED = "profile_attached"
    PROMPT_ATTACHED = "prompt_attached"
    TURN_OPEN = "turn_open"
    AWAITING_MODEL_STEP = "awaiting_model_step"
    MODEL_STEP_BLOCKED = "model_step_blocked"
    AWAITING_TOOL_PROPOSAL = "awaiting_tool_proposal"
    TOOL_PROPOSAL_BLOCKED = "tool_proposal_blocked"
    AWAITING_USER_INPUT = "awaiting_user_input"
    RESPONSE_READY = "response_ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class AgentRuntimeTurnState(StrEnum):
    UNKNOWN = "unknown"
    CREATED = "created"
    INPUT_ATTACHED = "input_attached"
    PROMPT_CONTEXT_ATTACHED = "prompt_context_attached"
    MODEL_STEP_PLANNED = "model_step_planned"
    MODEL_STEP_BLOCKED = "model_step_blocked"
    TOOL_CALL_PLANNED = "tool_call_planned"
    TOOL_CALL_BLOCKED = "tool_call_blocked"
    OBSERVATION_ATTACHED = "observation_attached"
    RESPONSE_DRAFTED = "response_drafted"
    RESPONSE_READY = "response_ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"
    BLOCKED = "blocked"


class AgentRuntimeStepKind(StrEnum):
    BOUNDARY_ATTACH = "boundary_attach"
    PROFILE_ATTACH = "profile_attach"
    PROMPT_ATTACH = "prompt_attach"
    USER_INPUT_ATTACH = "user_input_attach"
    MODEL_STEP_PLAN = "model_step_plan"
    MODEL_STEP_BLOCK = "model_step_block"
    TOOL_CALL_PLAN = "tool_call_plan"
    TOOL_CALL_BLOCK = "tool_call_block"
    OBSERVATION_ATTACH = "observation_attach"
    RESPONSE_DRAFT_ATTACH = "response_draft_attach"
    RESPONSE_READY_MARK = "response_ready_mark"
    SAFE_FAIL_RECORD = "safe_fail_record"
    NO_OP_RECORD = "no_op_record"
    CANCELLATION_RECORD = "cancellation_record"
    COMPLETION_MARK = "completion_mark"
    UNKNOWN = "unknown"


class AgentRuntimeTransitionKind(StrEnum):
    CREATE_SESSION = "create_session"
    ATTACH_BOUNDARY = "attach_boundary"
    ATTACH_PROFILE = "attach_profile"
    ATTACH_PROMPT = "attach_prompt"
    OPEN_TURN = "open_turn"
    ATTACH_USER_INPUT = "attach_user_input"
    ATTACH_PROMPT_CONTEXT = "attach_prompt_context"
    PLAN_MODEL_STEP = "plan_model_step"
    BLOCK_MODEL_STEP = "block_model_step"
    PLAN_TOOL_CALL = "plan_tool_call"
    BLOCK_TOOL_CALL = "block_tool_call"
    ATTACH_OBSERVATION = "attach_observation"
    ATTACH_RESPONSE_DRAFT = "attach_response_draft"
    MARK_RESPONSE_READY = "mark_response_ready"
    COMPLETE_TURN = "complete_turn"
    COMPLETE_SESSION = "complete_session"
    SAFE_FAIL = "safe_fail"
    NO_OP = "no_op"
    CANCEL = "cancel"
    BLOCK = "block"
    FUTURE_GATE = "future_gate"
    UNKNOWN = "unknown"


class AgentRuntimeTransitionDecisionKind(StrEnum):
    ALLOWED_STATE_TRANSITION = "allowed_state_transition"
    DENIED_INVALID_TRANSITION = "denied_invalid_transition"
    BLOCKED_BY_RUNTIME_BOUNDARY = "blocked_by_runtime_boundary"
    BLOCKED_BY_PERMISSION_GATE = "blocked_by_permission_gate"
    BLOCKED_BY_MISSING_PROFILE = "blocked_by_missing_profile"
    BLOCKED_BY_MISSING_PROMPT = "blocked_by_missing_prompt"
    BLOCKED_BY_RUNTIME_PROHIBITION = "blocked_by_runtime_prohibition"
    SAFE_FAIL_REQUIRED = "safe_fail_required"
    NO_OP_REQUIRED = "no_op_required"
    ASK_USER_REQUIRED = "ask_user_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class AgentRuntimeTerminalOutcomeKind(StrEnum):
    COMPLETED = "completed"
    RESPONSE_READY = "response_ready"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"
    BLOCKED = "blocked"
    CANCELLED = "cancelled"
    FUTURE_TRACK = "future_track"
    UNKNOWN = "unknown"


class AgentRuntimeFailureKind(StrEnum):
    INVALID_TRANSITION = "invalid_transition"
    MISSING_BOUNDARY = "missing_boundary"
    MISSING_PROFILE = "missing_profile"
    MISSING_PROMPT = "missing_prompt"
    PROHIBITED_RUNTIME_SURFACE = "prohibited_runtime_surface"
    PERMISSION_DENIED = "permission_denied"
    MODEL_INVOCATION_BLOCKED = "model_invocation_blocked"
    TOOL_EXECUTION_BLOCKED = "tool_execution_blocked"
    WORKSPACE_INSPECTION_BLOCKED = "workspace_inspection_blocked"
    PROVIDER_INVOCATION_BLOCKED = "provider_invocation_blocked"
    REFERENCE_ACCESS_BLOCKED = "reference_access_blocked"
    OCEL_EMISSION_BLOCKED = "ocel_emission_blocked"
    EXTERNAL_CONTROL_BLOCKED = "external_control_blocked"
    AUTHORITY_GRANT_BLOCKED = "authority_grant_blocked"
    UNKNOWN = "unknown"


class AgentRuntimeSourceKind(StrEnum):
    V0330_RUNTIME_BOUNDARY = "v0330_runtime_boundary"
    V0331_RUNTIME_PROFILE = "v0331_runtime_profile"
    V0332_PROMPT_ASSEMBLY_OUTPUT = "v0332_prompt_assembly_output"
    USER_INPUT_REF = "user_input_ref"
    TEST_FIXTURE = "test_fixture"
    REFERENCE_CONTEXT_REF = "reference_context_ref"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    MANUAL_SESSION_SPEC = "manual_session_spec"
    UNKNOWN = "unknown"


class AgentRuntimeReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    STATE_MACHINE_CONTRACT_READY = "state_machine_contract_ready"
    STATE_TRANSITION_READY = "state_transition_ready"
    DESIGN_HANDOFF_READY_FOR_V0334 = "design_handoff_ready_for_v0334"
    DESIGN_HANDOFF_READY_FOR_V0336 = "design_handoff_ready_for_v0336"
    DESIGN_HANDOFF_READY_FOR_V0337 = "design_handoff_ready_for_v0337"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_agent_step_execution",
    "ready_for_model_step_execution",
    "ready_for_tool_execution",
    "ready_for_read_only_tool_execution",
    "ready_for_workspace_inspection_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_command_execution",
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


def _validate_version_includes_v0333(version: str) -> None:
    _require_non_blank("version", version)
    if V0333_VERSION not in version:
        raise ValueError("version must include v0.33.3")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.3")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_source_ref_list(values: list["AgentRuntimeSourceRef"]) -> None:
    _validate_object_list("source_refs", values, AgentRuntimeSourceRef)


def _validate_non_negative_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_prohibited_runtime_actions(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    missing = set(DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS) - set(values)
    if missing:
        raise ValueError(f"{name} missing v0.33.3 prohibitions: {sorted(missing)}")


@dataclass(frozen=True)
class AgentRuntimeSessionFlagSet:
    flag_set_id: str
    version: str = V0333_VERSION
    state_machine_constructed: bool = False
    transition_validation_available: bool = False
    ready_for_v0334_readonly_tool_registry: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_execution: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_model_step_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
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
        _validate_version_includes_v0333(self.version)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "model_invocation", "provider_invocation", "trace_persistence"}):
            raise ValueError("AgentRuntimeSessionFlagSet is not runtime enablement")


@dataclass(frozen=True)
class AgentRuntimeSourceRef:
    source_ref_id: str
    source_kind: AgentRuntimeSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        AgentRuntimeSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "file_read", "execution"}):
            raise ValueError("AgentRuntimeSourceRef is not fetch, file read, or execution")

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
class AgentRuntimeSessionBoundaryView:
    boundary_view_id: str
    runtime_boundary_id: str | None = None
    runtime_profile_id: str | None = None
    prompt_output_id: str | None = None
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS))
    allowed_transition_kinds: list[AgentRuntimeTransitionKind | str] = field(default_factory=list)
    prohibited_transition_kinds: list[AgentRuntimeTransitionKind | str] = field(default_factory=lambda: [
        AgentRuntimeTransitionKind.PLAN_MODEL_STEP,
        AgentRuntimeTransitionKind.PLAN_TOOL_CALL,
    ])
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_view_id", self.boundary_view_id)
        _validate_prohibited_runtime_actions("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_enum_list("allowed_transition_kinds", self.allowed_transition_kinds, AgentRuntimeTransitionKind)
        _validate_enum_list("prohibited_transition_kinds", self.prohibited_transition_kinds, AgentRuntimeTransitionKind)
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"runtime_enforcement", "execution"}):
            raise ValueError("AgentRuntimeSessionBoundaryView is not runtime enforcement")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeSession:
    session_id: str
    state: AgentRuntimeSessionState | str
    boundary_view: AgentRuntimeSessionBoundaryView
    runtime_profile_id: str | None = None
    prompt_output_id: str | None = None
    active_turn_ids: list[str] = field(default_factory=list)
    completed_turn_ids: list[str] = field(default_factory=list)
    transition_ids: list[str] = field(default_factory=list)
    failure_record_ids: list[str] = field(default_factory=list)
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    summary: str = "In-memory session state artifact only."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("session_id", self.session_id)
        AgentRuntimeSessionState(self.state)
        if not isinstance(self.boundary_view, AgentRuntimeSessionBoundaryView):
            raise TypeError("boundary_view must be AgentRuntimeSessionBoundaryView")
        for name in ("active_turn_ids", "completed_turn_ids", "transition_ids", "failure_record_ids"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"provider_execution", "runtime_execution"}):
            raise ValueError("AgentRuntimeSession is not provider execution")

    @property
    def provider_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeTurn:
    turn_id: str
    session_id: str
    state: AgentRuntimeTurnState | str
    user_input_summary: str | None = None
    prompt_output_id: str | None = None
    step_ids: list[str] = field(default_factory=list)
    transition_ids: list[str] = field(default_factory=list)
    failure_record_ids: list[str] = field(default_factory=list)
    response_draft_ref: str | None = None
    response_ready: bool = False
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    ready_for_model_invocation: bool = False
    ready_for_tool_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("turn_id", self.turn_id)
        _require_non_blank("session_id", self.session_id)
        AgentRuntimeTurnState(self.state)
        for name in ("step_ids", "transition_ids", "failure_record_ids"):
            _validate_string_list(name, getattr(self, name))
        _validate_source_ref_list(self.source_refs)
        _validate_false(self, ("ready_for_model_invocation", "ready_for_tool_execution", "ready_for_execution"))
        if _metadata_flag_true(self.metadata, {"model_invocation", "tool_execution", "execution"}):
            raise ValueError("AgentRuntimeTurn is not model/tool execution")

    @property
    def model_or_tool_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeStep:
    step_id: str
    session_id: str
    turn_id: str | None
    step_kind: AgentRuntimeStepKind | str
    title: str
    summary: str
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    proposed_next_transition: AgentRuntimeTransitionKind | str | None = None
    blocked: bool = False
    no_op: bool = False
    safe_failed: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("step_id", "session_id", "title", "summary"):
            _require_non_blank(name, getattr(self, name))
        AgentRuntimeStepKind(self.step_kind)
        if self.proposed_next_transition is not None:
            AgentRuntimeTransitionKind(self.proposed_next_transition)
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"step_execution", "execution"}):
            raise ValueError("AgentRuntimeStep is not step execution")

    @property
    def step_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeTransitionRequest:
    transition_request_id: str
    session_id: str
    turn_id: str | None
    current_session_state: AgentRuntimeSessionState | str
    current_turn_state: AgentRuntimeTurnState | str | None
    requested_transition: AgentRuntimeTransitionKind | str
    reason: str
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("transition_request_id", self.transition_request_id)
        _require_non_blank("session_id", self.session_id)
        AgentRuntimeSessionState(self.current_session_state)
        if self.current_turn_state is not None:
            AgentRuntimeTurnState(self.current_turn_state)
        AgentRuntimeTransitionKind(self.requested_transition)
        _require_non_blank("reason", self.reason)
        _validate_source_ref_list(self.source_refs)
        if _metadata_flag_true(self.metadata, {"transition_execution", "side_effect"}):
            raise ValueError("AgentRuntimeTransitionRequest is not transition execution")

    @property
    def transition_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeTransitionDecision:
    transition_decision_id: str
    transition_request_id: str
    decision_kind: AgentRuntimeTransitionDecisionKind | str
    reason: str
    allowed_next_session_state: AgentRuntimeSessionState | str | None = None
    allowed_next_turn_state: AgentRuntimeTurnState | str | None = None
    denied_failure_kind: AgentRuntimeFailureKind | str | None = None
    requires_user_input: bool = False
    safe_fail_required: bool = False
    no_op_required: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("transition_decision_id", self.transition_decision_id)
        _require_non_blank("transition_request_id", self.transition_request_id)
        AgentRuntimeTransitionDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        if self.allowed_next_session_state is not None:
            AgentRuntimeSessionState(self.allowed_next_session_state)
        if self.allowed_next_turn_state is not None:
            AgentRuntimeTurnState(self.allowed_next_turn_state)
        if self.denied_failure_kind is not None:
            AgentRuntimeFailureKind(self.denied_failure_kind)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"side_effect_execution", "model_response"}):
            raise ValueError("AgentRuntimeTransitionDecision is deterministic validation only")

    @property
    def side_effect_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeStateTransition:
    transition_id: str
    transition_request_id: str
    transition_decision_id: str
    session_id: str
    turn_id: str | None
    transition_kind: AgentRuntimeTransitionKind | str
    from_session_state: AgentRuntimeSessionState | str
    to_session_state: AgentRuntimeSessionState | str
    from_turn_state: AgentRuntimeTurnState | str | None
    to_turn_state: AgentRuntimeTurnState | str | None
    terminal_outcome: AgentRuntimeTerminalOutcomeKind | str | None
    summary: str
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("transition_id", "transition_request_id", "transition_decision_id", "session_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        AgentRuntimeTransitionKind(self.transition_kind)
        AgentRuntimeSessionState(self.from_session_state)
        AgentRuntimeSessionState(self.to_session_state)
        if self.from_turn_state is not None:
            AgentRuntimeTurnState(self.from_turn_state)
        if self.to_turn_state is not None:
            AgentRuntimeTurnState(self.to_turn_state)
        if self.terminal_outcome is not None:
            AgentRuntimeTerminalOutcomeKind(self.terminal_outcome)
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"side_effect_execution", "execution"}):
            raise ValueError("AgentRuntimeStateTransition is not side-effect execution")

    @property
    def side_effect_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeStateMachine:
    state_machine_id: str
    version: str = V0333_VERSION
    allowed_transition_matrix: dict[str, list[str]] = field(default_factory=dict)
    terminal_session_states: list[AgentRuntimeSessionState | str] = field(default_factory=lambda: [
        AgentRuntimeSessionState.COMPLETED,
        AgentRuntimeSessionState.CANCELLED,
        AgentRuntimeSessionState.SAFE_FAILED,
        AgentRuntimeSessionState.NO_OP,
        AgentRuntimeSessionState.BLOCKED,
    ])
    terminal_turn_states: list[AgentRuntimeTurnState | str] = field(default_factory=lambda: [
        AgentRuntimeTurnState.COMPLETED,
        AgentRuntimeTurnState.CANCELLED,
        AgentRuntimeTurnState.SAFE_FAILED,
        AgentRuntimeTurnState.NO_OP,
        AgentRuntimeTurnState.BLOCKED,
    ])
    safe_failure_states: list[str] = field(default_factory=lambda: ["safe_failed", "no_op", "blocked"])
    prohibited_runtime_transitions: list[AgentRuntimeTransitionKind | str] = field(default_factory=lambda: [
        AgentRuntimeTransitionKind.PLAN_MODEL_STEP,
        AgentRuntimeTransitionKind.PLAN_TOOL_CALL,
    ])
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    ready_for_transition_validation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("state_machine_id", self.state_machine_id)
        _validate_version_includes_v0333(self.version)
        if not isinstance(self.allowed_transition_matrix, dict):
            raise TypeError("allowed_transition_matrix must be dict")
        for key, values in self.allowed_transition_matrix.items():
            AgentRuntimeSessionState(key)
            if not isinstance(values, list):
                raise TypeError("allowed_transition_matrix values must be list[str]")
            for value in values:
                AgentRuntimeTransitionKind(value)
        _validate_enum_list("terminal_session_states", self.terminal_session_states, AgentRuntimeSessionState)
        _validate_enum_list("terminal_turn_states", self.terminal_turn_states, AgentRuntimeTurnState)
        _validate_string_list("safe_failure_states", self.safe_failure_states)
        _validate_enum_list("prohibited_runtime_transitions", self.prohibited_runtime_transitions, AgentRuntimeTransitionKind)
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"runtime_execution", "side_effect"}):
            raise ValueError("AgentRuntimeStateMachine is not runtime execution")

    @property
    def runtime_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeFailureRecord:
    failure_record_id: str
    session_id: str
    turn_id: str | None
    failure_kind: AgentRuntimeFailureKind | str
    summary: str
    safe_outcome: AgentRuntimeTerminalOutcomeKind | str
    source_refs: list[AgentRuntimeSourceRef] = field(default_factory=list)
    ready_for_retry: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("failure_record_id", self.failure_record_id)
        _require_non_blank("session_id", self.session_id)
        AgentRuntimeFailureKind(self.failure_kind)
        _require_non_blank("summary", self.summary)
        AgentRuntimeTerminalOutcomeKind(self.safe_outcome)
        _validate_source_ref_list(self.source_refs)
        _validate_false(self, ("ready_for_retry", "ready_for_execution"))

    @property
    def safe_diagnostic_metadata(self) -> bool:
        return True


@dataclass(frozen=True)
class AgentRuntimeSessionSnapshot:
    snapshot_id: str
    version: str
    session: AgentRuntimeSession
    turns: list[AgentRuntimeTurn] = field(default_factory=list)
    steps: list[AgentRuntimeStep] = field(default_factory=list)
    transitions: list[AgentRuntimeStateTransition] = field(default_factory=list)
    failures: list[AgentRuntimeFailureRecord] = field(default_factory=list)
    state_machine_id: str | None = None
    summary: str = "In-memory session snapshot artifact only."
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version_includes_v0333(self.version)
        if not isinstance(self.session, AgentRuntimeSession):
            raise TypeError("session must be AgentRuntimeSession")
        _validate_object_list("turns", self.turns, AgentRuntimeTurn)
        _validate_object_list("steps", self.steps, AgentRuntimeStep)
        _validate_object_list("transitions", self.transitions, AgentRuntimeStateTransition)
        _validate_object_list("failures", self.failures, AgentRuntimeFailureRecord)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"persistence", "trace_persistence", "database_write"}):
            raise ValueError("AgentRuntimeSessionSnapshot is not persistence")

    @property
    def persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeSessionReport:
    report_id: str
    version: str
    session_id: str
    snapshot_id: str | None
    state_machine_id: str | None
    status: AgentRuntimeSessionState | str
    readiness_level: AgentRuntimeReadinessLevel | str
    summary: str
    transition_count: int = 0
    failure_count: int = 0
    completed_turn_count: int = 0
    active_turn_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0334_readonly_tool_registry: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "session_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0333(self.version)
        AgentRuntimeSessionState(self.status)
        AgentRuntimeReadinessLevel(self.readiness_level)
        for name in ("transition_count", "failure_count", "completed_turn_count", "active_turn_count"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if (self.ready_for_v0334_readonly_tool_registry or self.ready_for_v0336_agent_step_runner or self.ready_for_v0337_runtime_ocel_trace_emitter) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_execution", "trace_persistence"}):
            raise ValueError("AgentRuntimeSessionReport is not runtime execution")

    @property
    def runtime_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeRunPreview:
    run_preview_id: str
    session_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["construct in-memory session state", "validate deterministic transition"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["AgentRuntimeSessionSnapshot", "AgentRuntimeSessionReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: ["model invocation", "agent step execution", "tool execution", "OCEL emission", "runtime trace persistence"])
    no_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_read_only_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_reference_file_access_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
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
                raise ValueError(f"{name} must be True in v0.33.3")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class AgentRuntimeNoSideEffectGuarantee:
    guarantee_id: str
    version: str = V0333_VERSION
    no_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_agent_step_execution: bool = True
    no_model_step_execution: bool = True
    no_tool_execution: bool = True
    no_read_only_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_reference_file_access: bool = True
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
        _validate_version_includes_v0333(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.3")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0333ReadinessReport:
    report_id: str
    version: str = V0333_VERSION
    session_report_id: str | None = None
    session_snapshot_id: str | None = None
    state_machine_id: str | None = None
    summary: str = "v0.33.3 constructs session state-machine artifacts only."
    ready_for_v0334_readonly_tool_registry: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_execution: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_model_step_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_read_only_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
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
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_SESSION_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0333(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, RUNTIME_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_prohibited_runtime_actions("prohibited_until_later_gate", self.prohibited_until_later_gate)
        if (self.ready_for_v0334_readonly_tool_registry or self.ready_for_v0336_agent_step_runner or self.ready_for_v0337_runtime_ocel_trace_emitter) and self.blocked_items:
            raise ValueError("design-stage readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"runtime_enablement", "model_invocation", "ocel_emission"}):
            raise ValueError("V0333ReadinessReport is not runtime enablement")

    @property
    def runtime_enablement(self) -> bool:
        return False


def default_agent_runtime_transition_matrix() -> dict[str, list[str]]:
    return {
        AgentRuntimeSessionState.UNKNOWN.value: [AgentRuntimeTransitionKind.CREATE_SESSION.value],
        AgentRuntimeSessionState.CREATED.value: [
            AgentRuntimeTransitionKind.ATTACH_BOUNDARY.value,
            AgentRuntimeTransitionKind.SAFE_FAIL.value,
            AgentRuntimeTransitionKind.NO_OP.value,
            AgentRuntimeTransitionKind.CANCEL.value,
            AgentRuntimeTransitionKind.BLOCK.value,
        ],
        AgentRuntimeSessionState.BOUNDARY_ATTACHED.value: [
            AgentRuntimeTransitionKind.ATTACH_PROFILE.value,
            AgentRuntimeTransitionKind.SAFE_FAIL.value,
            AgentRuntimeTransitionKind.NO_OP.value,
            AgentRuntimeTransitionKind.CANCEL.value,
            AgentRuntimeTransitionKind.BLOCK.value,
        ],
        AgentRuntimeSessionState.PROFILE_ATTACHED.value: [
            AgentRuntimeTransitionKind.ATTACH_PROMPT.value,
            AgentRuntimeTransitionKind.SAFE_FAIL.value,
            AgentRuntimeTransitionKind.NO_OP.value,
            AgentRuntimeTransitionKind.CANCEL.value,
            AgentRuntimeTransitionKind.BLOCK.value,
        ],
        AgentRuntimeSessionState.PROMPT_ATTACHED.value: [
            AgentRuntimeTransitionKind.OPEN_TURN.value,
            AgentRuntimeTransitionKind.SAFE_FAIL.value,
            AgentRuntimeTransitionKind.NO_OP.value,
            AgentRuntimeTransitionKind.CANCEL.value,
            AgentRuntimeTransitionKind.BLOCK.value,
        ],
        AgentRuntimeSessionState.TURN_OPEN.value: [
            AgentRuntimeTransitionKind.ATTACH_USER_INPUT.value,
            AgentRuntimeTransitionKind.ATTACH_PROMPT_CONTEXT.value,
            AgentRuntimeTransitionKind.ATTACH_RESPONSE_DRAFT.value,
            AgentRuntimeTransitionKind.MARK_RESPONSE_READY.value,
            AgentRuntimeTransitionKind.COMPLETE_TURN.value,
            AgentRuntimeTransitionKind.SAFE_FAIL.value,
            AgentRuntimeTransitionKind.NO_OP.value,
            AgentRuntimeTransitionKind.CANCEL.value,
            AgentRuntimeTransitionKind.BLOCK.value,
        ],
        AgentRuntimeSessionState.AWAITING_USER_INPUT.value: [
            AgentRuntimeTransitionKind.ATTACH_USER_INPUT.value,
            AgentRuntimeTransitionKind.NO_OP.value,
            AgentRuntimeTransitionKind.CANCEL.value,
        ],
        AgentRuntimeSessionState.RESPONSE_READY.value: [
            AgentRuntimeTransitionKind.COMPLETE_TURN.value,
            AgentRuntimeTransitionKind.COMPLETE_SESSION.value,
            AgentRuntimeTransitionKind.CANCEL.value,
        ],
    }


SESSION_TRANSITION_TARGETS: dict[AgentRuntimeTransitionKind, AgentRuntimeSessionState] = {
    AgentRuntimeTransitionKind.CREATE_SESSION: AgentRuntimeSessionState.CREATED,
    AgentRuntimeTransitionKind.ATTACH_BOUNDARY: AgentRuntimeSessionState.BOUNDARY_ATTACHED,
    AgentRuntimeTransitionKind.ATTACH_PROFILE: AgentRuntimeSessionState.PROFILE_ATTACHED,
    AgentRuntimeTransitionKind.ATTACH_PROMPT: AgentRuntimeSessionState.PROMPT_ATTACHED,
    AgentRuntimeTransitionKind.OPEN_TURN: AgentRuntimeSessionState.TURN_OPEN,
    AgentRuntimeTransitionKind.ATTACH_USER_INPUT: AgentRuntimeSessionState.TURN_OPEN,
    AgentRuntimeTransitionKind.ATTACH_PROMPT_CONTEXT: AgentRuntimeSessionState.TURN_OPEN,
    AgentRuntimeTransitionKind.ATTACH_RESPONSE_DRAFT: AgentRuntimeSessionState.TURN_OPEN,
    AgentRuntimeTransitionKind.MARK_RESPONSE_READY: AgentRuntimeSessionState.RESPONSE_READY,
    AgentRuntimeTransitionKind.COMPLETE_TURN: AgentRuntimeSessionState.RESPONSE_READY,
    AgentRuntimeTransitionKind.COMPLETE_SESSION: AgentRuntimeSessionState.COMPLETED,
    AgentRuntimeTransitionKind.SAFE_FAIL: AgentRuntimeSessionState.SAFE_FAILED,
    AgentRuntimeTransitionKind.NO_OP: AgentRuntimeSessionState.NO_OP,
    AgentRuntimeTransitionKind.CANCEL: AgentRuntimeSessionState.CANCELLED,
    AgentRuntimeTransitionKind.BLOCK: AgentRuntimeSessionState.BLOCKED,
    AgentRuntimeTransitionKind.FUTURE_GATE: AgentRuntimeSessionState.FUTURE_TRACK,
}

TURN_TRANSITION_TARGETS: dict[AgentRuntimeTransitionKind, AgentRuntimeTurnState | None] = {
    AgentRuntimeTransitionKind.OPEN_TURN: AgentRuntimeTurnState.CREATED,
    AgentRuntimeTransitionKind.ATTACH_USER_INPUT: AgentRuntimeTurnState.INPUT_ATTACHED,
    AgentRuntimeTransitionKind.ATTACH_PROMPT_CONTEXT: AgentRuntimeTurnState.PROMPT_CONTEXT_ATTACHED,
    AgentRuntimeTransitionKind.BLOCK_MODEL_STEP: AgentRuntimeTurnState.MODEL_STEP_BLOCKED,
    AgentRuntimeTransitionKind.BLOCK_TOOL_CALL: AgentRuntimeTurnState.TOOL_CALL_BLOCKED,
    AgentRuntimeTransitionKind.ATTACH_OBSERVATION: AgentRuntimeTurnState.OBSERVATION_ATTACHED,
    AgentRuntimeTransitionKind.ATTACH_RESPONSE_DRAFT: AgentRuntimeTurnState.RESPONSE_DRAFTED,
    AgentRuntimeTransitionKind.MARK_RESPONSE_READY: AgentRuntimeTurnState.RESPONSE_READY,
    AgentRuntimeTransitionKind.COMPLETE_TURN: AgentRuntimeTurnState.COMPLETED,
    AgentRuntimeTransitionKind.SAFE_FAIL: AgentRuntimeTurnState.SAFE_FAILED,
    AgentRuntimeTransitionKind.NO_OP: AgentRuntimeTurnState.NO_OP,
    AgentRuntimeTransitionKind.CANCEL: AgentRuntimeTurnState.CANCELLED,
    AgentRuntimeTransitionKind.BLOCK: AgentRuntimeTurnState.BLOCKED,
}


def build_agent_runtime_session_flags(flag_set_id: str = "agent_runtime_session_flags:v0.33.3", **kwargs: Any) -> AgentRuntimeSessionFlagSet:
    return AgentRuntimeSessionFlagSet(flag_set_id=flag_set_id, version=V0333_VERSION, **kwargs)


def build_agent_runtime_source_ref(
    source_ref_id: str,
    source_kind: AgentRuntimeSourceKind | str = AgentRuntimeSourceKind.MANUAL_SESSION_SPEC,
    source_id: str = "manual_session_spec",
    source_summary: str = "Provided in-memory session metadata.",
    **kwargs: Any,
) -> AgentRuntimeSourceRef:
    return AgentRuntimeSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_agent_runtime_session_boundary_view(boundary_view_id: str = "session_boundary_view:v0.33.3", **kwargs: Any) -> AgentRuntimeSessionBoundaryView:
    return AgentRuntimeSessionBoundaryView(boundary_view_id=boundary_view_id, **kwargs)


def build_agent_runtime_session(session_id: str, boundary_view: AgentRuntimeSessionBoundaryView | None = None, **kwargs: Any) -> AgentRuntimeSession:
    return AgentRuntimeSession(
        session_id=session_id,
        state=kwargs.pop("state", AgentRuntimeSessionState.CREATED),
        boundary_view=boundary_view or build_agent_runtime_session_boundary_view(),
        **kwargs,
    )


def build_agent_runtime_turn(turn_id: str, session_id: str, **kwargs: Any) -> AgentRuntimeTurn:
    return AgentRuntimeTurn(turn_id=turn_id, session_id=session_id, state=kwargs.pop("state", AgentRuntimeTurnState.CREATED), **kwargs)


def build_agent_runtime_step(step_id: str, session_id: str, **kwargs: Any) -> AgentRuntimeStep:
    return AgentRuntimeStep(
        step_id=step_id,
        session_id=session_id,
        turn_id=kwargs.pop("turn_id", None),
        step_kind=kwargs.pop("step_kind", AgentRuntimeStepKind.UNKNOWN),
        title=kwargs.pop("title", "Session state-machine step record"),
        summary=kwargs.pop("summary", "Step record only; no step execution."),
        **kwargs,
    )


def build_agent_runtime_transition_request(transition_request_id: str, session_id: str, requested_transition: AgentRuntimeTransitionKind | str, **kwargs: Any) -> AgentRuntimeTransitionRequest:
    return AgentRuntimeTransitionRequest(
        transition_request_id=transition_request_id,
        session_id=session_id,
        turn_id=kwargs.pop("turn_id", None),
        current_session_state=kwargs.pop("current_session_state", AgentRuntimeSessionState.CREATED),
        current_turn_state=kwargs.pop("current_turn_state", None),
        requested_transition=requested_transition,
        reason=kwargs.pop("reason", "Validate deterministic state transition."),
        **kwargs,
    )


def build_agent_runtime_transition_decision(transition_decision_id: str, transition_request_id: str, **kwargs: Any) -> AgentRuntimeTransitionDecision:
    return AgentRuntimeTransitionDecision(
        transition_decision_id=transition_decision_id,
        transition_request_id=transition_request_id,
        decision_kind=kwargs.pop("decision_kind", AgentRuntimeTransitionDecisionKind.ALLOWED_STATE_TRANSITION),
        reason=kwargs.pop("reason", "Allowed deterministic state transition only."),
        **kwargs,
    )


def build_agent_runtime_state_transition(transition_id: str, transition_request_id: str, transition_decision_id: str, session_id: str, transition_kind: AgentRuntimeTransitionKind | str, **kwargs: Any) -> AgentRuntimeStateTransition:
    return AgentRuntimeStateTransition(
        transition_id=transition_id,
        transition_request_id=transition_request_id,
        transition_decision_id=transition_decision_id,
        session_id=session_id,
        turn_id=kwargs.pop("turn_id", None),
        transition_kind=transition_kind,
        from_session_state=kwargs.pop("from_session_state", AgentRuntimeSessionState.CREATED),
        to_session_state=kwargs.pop("to_session_state", AgentRuntimeSessionState.CREATED),
        from_turn_state=kwargs.pop("from_turn_state", None),
        to_turn_state=kwargs.pop("to_turn_state", None),
        terminal_outcome=kwargs.pop("terminal_outcome", None),
        summary=kwargs.pop("summary", "State transition record only; no side effect execution."),
        **kwargs,
    )


def build_agent_runtime_state_machine(state_machine_id: str = "agent_runtime_state_machine:v0.33.3", **kwargs: Any) -> AgentRuntimeStateMachine:
    return AgentRuntimeStateMachine(
        state_machine_id=state_machine_id,
        version=V0333_VERSION,
        allowed_transition_matrix=kwargs.pop("allowed_transition_matrix", default_agent_runtime_transition_matrix()),
        ready_for_transition_validation=kwargs.pop("ready_for_transition_validation", True),
        **kwargs,
    )


def build_agent_runtime_failure_record(failure_record_id: str, session_id: str, **kwargs: Any) -> AgentRuntimeFailureRecord:
    return AgentRuntimeFailureRecord(
        failure_record_id=failure_record_id,
        session_id=session_id,
        turn_id=kwargs.pop("turn_id", None),
        failure_kind=kwargs.pop("failure_kind", AgentRuntimeFailureKind.INVALID_TRANSITION),
        summary=kwargs.pop("summary", "Safe diagnostic failure record."),
        safe_outcome=kwargs.pop("safe_outcome", AgentRuntimeTerminalOutcomeKind.BLOCKED),
        **kwargs,
    )


def build_agent_runtime_session_snapshot(snapshot_id: str, session: AgentRuntimeSession, **kwargs: Any) -> AgentRuntimeSessionSnapshot:
    return AgentRuntimeSessionSnapshot(snapshot_id=snapshot_id, version=V0333_VERSION, session=session, **kwargs)


def build_agent_runtime_session_report(report_id: str, session_id: str, **kwargs: Any) -> AgentRuntimeSessionReport:
    return AgentRuntimeSessionReport(
        report_id=report_id,
        version=V0333_VERSION,
        session_id=session_id,
        snapshot_id=kwargs.pop("snapshot_id", None),
        state_machine_id=kwargs.pop("state_machine_id", None),
        status=kwargs.pop("status", AgentRuntimeSessionState.CREATED),
        readiness_level=kwargs.pop("readiness_level", AgentRuntimeReadinessLevel.STATE_TRANSITION_READY),
        summary=kwargs.pop("summary", "Session runtime report is not runtime execution."),
        **kwargs,
    )


def build_agent_runtime_run_preview(run_preview_id: str, **kwargs: Any) -> AgentRuntimeRunPreview:
    return AgentRuntimeRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_agent_runtime_no_side_effect_guarantee(guarantee_id: str = "agent_runtime_no_side_effect:v0.33.3", **kwargs: Any) -> AgentRuntimeNoSideEffectGuarantee:
    return AgentRuntimeNoSideEffectGuarantee(guarantee_id=guarantee_id, version=V0333_VERSION, **kwargs)


def build_v0333_readiness_report(report_id: str = "v0333_readiness_report", **kwargs: Any) -> V0333ReadinessReport:
    return V0333ReadinessReport(report_id=report_id, version=V0333_VERSION, **kwargs)


def _blocked_decision(request: AgentRuntimeTransitionRequest, failure_kind: AgentRuntimeFailureKind, reason: str) -> AgentRuntimeTransitionDecision:
    return build_agent_runtime_transition_decision(
        f"{request.transition_request_id}:decision",
        request.transition_request_id,
        decision_kind=AgentRuntimeTransitionDecisionKind.BLOCKED_BY_RUNTIME_PROHIBITION,
        reason=reason,
        allowed_next_session_state=AgentRuntimeSessionState.BLOCKED,
        allowed_next_turn_state=AgentRuntimeTurnState.BLOCKED if request.current_turn_state is not None else None,
        denied_failure_kind=failure_kind,
        safe_fail_required=True,
    )


def validate_agent_runtime_transition_request(
    state_machine: AgentRuntimeStateMachine,
    request: AgentRuntimeTransitionRequest,
) -> AgentRuntimeTransitionDecision:
    if not isinstance(state_machine, AgentRuntimeStateMachine):
        raise TypeError("state_machine must be AgentRuntimeStateMachine")
    if not isinstance(request, AgentRuntimeTransitionRequest):
        raise TypeError("request must be AgentRuntimeTransitionRequest")
    transition = AgentRuntimeTransitionKind(request.requested_transition)
    current_state = AgentRuntimeSessionState(request.current_session_state)

    if transition == AgentRuntimeTransitionKind.PLAN_MODEL_STEP:
        return _blocked_decision(request, AgentRuntimeFailureKind.MODEL_INVOCATION_BLOCKED, "Model step planning remains blocked in v0.33.3.")
    if transition == AgentRuntimeTransitionKind.PLAN_TOOL_CALL:
        return _blocked_decision(request, AgentRuntimeFailureKind.TOOL_EXECUTION_BLOCKED, "Tool call planning remains blocked in v0.33.3.")
    if transition in {AgentRuntimeTransitionKind.BLOCK_MODEL_STEP, AgentRuntimeTransitionKind.BLOCK_TOOL_CALL}:
        next_session = AgentRuntimeSessionState.MODEL_STEP_BLOCKED if transition == AgentRuntimeTransitionKind.BLOCK_MODEL_STEP else AgentRuntimeSessionState.TOOL_PROPOSAL_BLOCKED
        next_turn = AgentRuntimeTurnState.MODEL_STEP_BLOCKED if transition == AgentRuntimeTransitionKind.BLOCK_MODEL_STEP else AgentRuntimeTurnState.TOOL_CALL_BLOCKED
        return build_agent_runtime_transition_decision(
            f"{request.transition_request_id}:decision",
            request.transition_request_id,
            decision_kind=AgentRuntimeTransitionDecisionKind.BLOCKED_BY_RUNTIME_BOUNDARY,
            reason="Blocked transition records a safe non-executing outcome.",
            allowed_next_session_state=next_session,
            allowed_next_turn_state=next_turn,
            denied_failure_kind=AgentRuntimeFailureKind.PROHIBITED_RUNTIME_SURFACE,
            safe_fail_required=False,
        )

    allowed = state_machine.allowed_transition_matrix.get(current_state.value, [])
    if transition.value not in allowed:
        return build_agent_runtime_transition_decision(
            f"{request.transition_request_id}:decision",
            request.transition_request_id,
            decision_kind=AgentRuntimeTransitionDecisionKind.DENIED_INVALID_TRANSITION,
            reason="Transition is not allowed by the deterministic v0.33.3 matrix.",
            denied_failure_kind=AgentRuntimeFailureKind.INVALID_TRANSITION,
        )

    next_session = SESSION_TRANSITION_TARGETS.get(transition, current_state)
    next_turn = TURN_TRANSITION_TARGETS.get(transition, request.current_turn_state)
    return build_agent_runtime_transition_decision(
        f"{request.transition_request_id}:decision",
        request.transition_request_id,
        decision_kind=AgentRuntimeTransitionDecisionKind.ALLOWED_STATE_TRANSITION,
        reason="Allowed deterministic state transition only; no side effects.",
        allowed_next_session_state=next_session,
        allowed_next_turn_state=next_turn,
    )


def derive_agent_runtime_state_transition(
    request: AgentRuntimeTransitionRequest,
    decision: AgentRuntimeTransitionDecision,
) -> AgentRuntimeStateTransition:
    if not isinstance(request, AgentRuntimeTransitionRequest):
        raise TypeError("request must be AgentRuntimeTransitionRequest")
    if not isinstance(decision, AgentRuntimeTransitionDecision):
        raise TypeError("decision must be AgentRuntimeTransitionDecision")

    decision_kind = AgentRuntimeTransitionDecisionKind(decision.decision_kind)
    transition = AgentRuntimeTransitionKind(request.requested_transition)
    from_session = AgentRuntimeSessionState(request.current_session_state)
    from_turn = AgentRuntimeTurnState(request.current_turn_state) if request.current_turn_state is not None else None
    to_session = AgentRuntimeSessionState(decision.allowed_next_session_state) if decision.allowed_next_session_state is not None else from_session
    to_turn = AgentRuntimeTurnState(decision.allowed_next_turn_state) if decision.allowed_next_turn_state is not None else from_turn
    terminal = None
    if to_session == AgentRuntimeSessionState.COMPLETED:
        terminal = AgentRuntimeTerminalOutcomeKind.COMPLETED
    elif to_session == AgentRuntimeSessionState.RESPONSE_READY:
        terminal = AgentRuntimeTerminalOutcomeKind.RESPONSE_READY
    elif to_session == AgentRuntimeSessionState.SAFE_FAILED:
        terminal = AgentRuntimeTerminalOutcomeKind.SAFE_FAILED
    elif to_session == AgentRuntimeSessionState.NO_OP:
        terminal = AgentRuntimeTerminalOutcomeKind.NO_OP
    elif to_session == AgentRuntimeSessionState.BLOCKED or decision_kind.name.startswith("BLOCKED"):
        terminal = AgentRuntimeTerminalOutcomeKind.BLOCKED
    elif to_session == AgentRuntimeSessionState.CANCELLED:
        terminal = AgentRuntimeTerminalOutcomeKind.CANCELLED

    return build_agent_runtime_state_transition(
        f"{request.transition_request_id}:transition",
        request.transition_request_id,
        decision.transition_decision_id,
        request.session_id,
        transition,
        turn_id=request.turn_id,
        from_session_state=from_session,
        to_session_state=to_session,
        from_turn_state=from_turn,
        to_turn_state=to_turn,
        terminal_outcome=terminal,
        source_refs=list(request.source_refs),
        summary="Derived deterministic state transition artifact only.",
    )


def agent_runtime_flags_preserve_runtime_false(flags: AgentRuntimeSessionFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in RUNTIME_FLAG_NAMES)


def agent_runtime_session_is_not_execution(session: AgentRuntimeSession) -> bool:
    return session.ready_for_execution is False and session.provider_execution is False


def agent_runtime_transition_is_not_side_effect(transition: AgentRuntimeStateTransition) -> bool:
    return transition.ready_for_execution is False and transition.side_effect_execution is False


def agent_runtime_snapshot_is_not_persistence(snapshot: AgentRuntimeSessionSnapshot) -> bool:
    return snapshot.ready_for_execution is False and snapshot.persistence is False


def v0333_readiness_report_is_not_runtime_ready(report: V0333ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in RUNTIME_FLAG_NAMES) and report.runtime_enablement is False
