from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0360_VERSION = "v0.36.0"
V0360_RELEASE_NAME = "v0.36.0 Human-approved Patch Apply Sandbox Boundary Foundation"

V036_ROADMAP = [
    "v0.36.0 Human-approved Patch Apply Sandbox Boundary Foundation",
    "v0.36.1 Apply Candidate & Human Approval Contract",
    "v0.36.2 Dry-run Patch Apply Simulation",
    "v0.36.3 Sandbox Workspace / Overlay Policy",
    "v0.36.4 Sandbox Patch Apply Engine",
    "v0.36.5 Sandbox Post-Apply Validation & Reconciliation",
    "v0.36.6 Bounded Agentic Function/Task Operation Cycle",
    "v0.36.7 Patch Apply Sandbox OCEL Trace Packet",
    "v0.36.8 CLI Sandbox Apply & Agentic Task Surface",
    "v0.36.9 Human-approved Patch Apply Sandbox Consolidation",
]

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_dry_run_apply_simulation",
    "ready_for_sandbox_patch_apply",
    "ready_for_sandbox_workspace_write",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_test_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_reference_execution",
    "ready_for_reference_import",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_DECISION_NAMES = (
    "dry_run_apply_simulation_allowed",
    "sandbox_patch_apply_allowed",
    "sandbox_workspace_write_allowed",
    "live_workspace_write_allowed",
    "patch_application_allowed",
    "workspace_write_allowed",
    "code_edit_allowed",
    "apply_patch_allowed",
    "git_apply_allowed",
    "test_execution_allowed",
    "shell_execution_allowed",
    "subprocess_allowed",
    "command_execution_allowed",
    "dependency_install_allowed",
    "reference_execution_allowed",
    "reference_import_allowed",
    "external_agent_execution_allowed",
    "claude_code_invocation_allowed",
    "codex_cli_invocation_allowed",
    "dominion_runtime_allowed",
    "infinite_agent_loop_allowed",
    "autonomous_agent_runtime_allowed",
    "independent_agent_runtime_allowed",
    "multi_cycle_agentic_loop_allowed",
    "provider_invocation_allowed",
    "network_access_allowed",
    "credential_access_allowed",
    "secret_read_allowed",
    "persistent_trace_write_allowed",
    "ui_runtime_allowed",
    "authority_grant_allowed",
    "ready_for_execution",
)


class PatchApplySandboxTrackKind(StrEnum):
    BOUNDARY_FOUNDATION = "boundary_foundation"
    APPLY_CANDIDATE_HUMAN_APPROVAL_CONTRACT = "apply_candidate_human_approval_contract"
    DRY_RUN_PATCH_APPLY_SIMULATION = "dry_run_patch_apply_simulation"
    SANDBOX_WORKSPACE_OVERLAY_POLICY = "sandbox_workspace_overlay_policy"
    SANDBOX_PATCH_APPLY_ENGINE = "sandbox_patch_apply_engine"
    SANDBOX_POST_APPLY_VALIDATION = "sandbox_post_apply_validation"
    BOUNDED_AGENTIC_TASK_OPERATION_CYCLE = "bounded_agentic_task_operation_cycle"
    PATCH_APPLY_SANDBOX_OCEL_TRACE_PACKET = "patch_apply_sandbox_ocel_trace_packet"
    CLI_SANDBOX_APPLY_AGENTIC_SURFACE = "cli_sandbox_apply_agentic_surface"
    CONSOLIDATION = "consolidation"
    UNKNOWN = "unknown"


class PatchApplySandboxSurfaceKind(StrEnum):
    APPLY_CANDIDATE_ENVELOPE = "apply_candidate_envelope"
    HUMAN_APPROVAL_CONTRACT = "human_approval_contract"
    DRY_RUN_APPLY_SIMULATION = "dry_run_apply_simulation"
    SANDBOX_WORKSPACE_POLICY = "sandbox_workspace_policy"
    SANDBOX_OVERLAY_POLICY = "sandbox_overlay_policy"
    SANDBOX_PATCH_APPLY = "sandbox_patch_apply"
    SANDBOX_POST_APPLY_VALIDATION = "sandbox_post_apply_validation"
    BOUNDED_AGENTIC_TASK_OPERATION = "bounded_agentic_task_operation"
    AGENTIC_FUNCTION_TASK_EXECUTION = "agentic_function_task_execution"
    PATCH_APPLY_TRACE_PACKET = "patch_apply_trace_packet"
    CLI_SANDBOX_APPLY_SURFACE = "cli_sandbox_apply_surface"
    LIVE_WORKSPACE_WRITE = "live_workspace_write"
    UNRESTRICTED_PATCH_APPLY = "unrestricted_patch_apply"
    GIT_APPLY = "git_apply"
    APPLY_PATCH = "apply_patch"
    TEST_EXECUTION = "test_execution"
    SHELL_COMMAND = "shell_command"
    DEPENDENCY_INSTALL = "dependency_install"
    EXTERNAL_AGENT_EXECUTION = "external_agent_execution"
    DOMINION_RUNTIME = "dominion_runtime"
    INFINITE_AGENT_LOOP = "infinite_agent_loop"
    UNKNOWN = "unknown"


class PatchApplySandboxCapabilityKind(StrEnum):
    DEFINE_APPLY_SANDBOX_BOUNDARY = "define_apply_sandbox_boundary"
    DEFINE_HUMAN_APPROVAL_BOUNDARY = "define_human_approval_boundary"
    DEFINE_BOUNDED_AGENTIC_TASK_BOUNDARY = "define_bounded_agentic_task_boundary"
    CREATE_APPLY_CANDIDATE_FUTURE_GATE = "create_apply_candidate_future_gate"
    CREATE_HUMAN_APPROVAL_CONTRACT_FUTURE_GATE = "create_human_approval_contract_future_gate"
    CREATE_DRY_RUN_APPLY_SIMULATION_FUTURE_GATE = "create_dry_run_apply_simulation_future_gate"
    CREATE_SANDBOX_WORKSPACE_FUTURE_GATE = "create_sandbox_workspace_future_gate"
    PERFORM_SANDBOX_PATCH_APPLY = "perform_sandbox_patch_apply"
    PERFORM_LIVE_PATCH_APPLY = "perform_live_patch_apply"
    WRITE_SANDBOX_FILE = "write_sandbox_file"
    WRITE_LIVE_WORKSPACE_FILE = "write_live_workspace_file"
    EDIT_CODE_FILE = "edit_code_file"
    CALL_APPLY_PATCH = "call_apply_patch"
    CALL_GIT_APPLY = "call_git_apply"
    RUN_TESTS = "run_tests"
    EXECUTE_SHELL = "execute_shell"
    INSTALL_DEPENDENCY = "install_dependency"
    EXECUTE_EXTERNAL_AGENT = "execute_external_agent"
    INVOKE_CLAUDE_CODE = "invoke_claude_code"
    INVOKE_CODEX_CLI = "invoke_codex_cli"
    RUN_DOMINION_RUNTIME = "run_dominion_runtime"
    RUN_INFINITE_AGENT_LOOP = "run_infinite_agent_loop"
    UNKNOWN = "unknown"


class PatchApplySandboxRiskKind(StrEnum):
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    SANDBOX_ESCAPE_RISK = "sandbox_escape_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    OUTSIDE_ROOT_WRITE_RISK = "outside_root_write_risk"
    HUMAN_APPROVAL_FORGERY_RISK = "human_approval_forgery_risk"
    MODEL_GENERATED_APPROVAL_RISK = "model_generated_approval_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    SUBPROCESS_EXECUTION_RISK = "subprocess_execution_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    CLAUDE_CODE_INVOCATION_RISK = "claude_code_invocation_risk"
    CODEX_CLI_INVOCATION_RISK = "codex_cli_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    AUTONOMOUS_AGENT_RUNTIME_RISK = "autonomous_agent_runtime_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class PatchApplySandboxDecisionKind(StrEnum):
    ALLOW_BOUNDARY_DEFINITION = "allow_boundary_definition"
    ALLOW_HUMAN_APPROVAL_BOUNDARY_DEFINITION = "allow_human_approval_boundary_definition"
    ALLOW_BOUNDED_AGENTIC_TASK_BOUNDARY_DEFINITION = "allow_bounded_agentic_task_boundary_definition"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchApplySandboxStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_READY = "boundary_ready"
    BOUNDARY_READY_WITH_GAPS = "boundary_ready_with_gaps"
    HUMAN_APPROVAL_BOUNDARY_READY = "human_approval_boundary_ready"
    BOUNDED_AGENTIC_TASK_BOUNDARY_READY = "bounded_agentic_task_boundary_ready"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class PatchApplySandboxReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_CONTRACT_READY = "boundary_contract_ready"
    APPLY_SANDBOX_BOUNDARY_READY = "apply_sandbox_boundary_ready"
    HUMAN_APPROVAL_BOUNDARY_READY = "human_approval_boundary_ready"
    BOUNDED_AGENTIC_TASK_BOUNDARY_READY = "bounded_agentic_task_boundary_ready"
    DESIGN_HANDOFF_READY_FOR_V0361 = "design_handoff_ready_for_v0361"
    DESIGN_HANDOFF_READY_FOR_V0362 = "design_handoff_ready_for_v0362"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchApplyWritePosture(StrEnum):
    NO_WRITE = "no_write"
    SANDBOX_WRITE_FUTURE_GATED = "sandbox_write_future_gated"
    SANDBOX_WRITE_ALLOWED_LATER = "sandbox_write_allowed_later"
    LIVE_WRITE_BLOCKED = "live_write_blocked"
    WRITE_BLOCKED = "write_blocked"
    UNKNOWN = "unknown"


class PatchApplyExecutionPosture(StrEnum):
    NO_APPLY = "no_apply"
    DRY_RUN_FUTURE_GATED = "dry_run_future_gated"
    SANDBOX_APPLY_FUTURE_GATED = "sandbox_apply_future_gated"
    LIVE_APPLY_BLOCKED = "live_apply_blocked"
    APPLY_BLOCKED = "apply_blocked"
    UNKNOWN = "unknown"


class HumanApprovalPosture(StrEnum):
    APPROVAL_NOT_REQUIRED_FOR_BOUNDARY = "approval_not_required_for_boundary"
    HUMAN_APPROVAL_CONTRACT_FUTURE_GATED = "human_approval_contract_future_gated"
    OPERATOR_SUPPLIED_APPROVAL_REQUIRED = "operator_supplied_approval_required"
    MODEL_GENERATED_APPROVAL_INVALID = "model_generated_approval_invalid"
    APPROVAL_METADATA_ONLY = "approval_metadata_only"
    UNKNOWN = "unknown"


class AgenticTaskExecutionPosture(StrEnum):
    NO_AGENTIC_EXECUTION = "no_agentic_execution"
    BOUNDED_FUNCTION_TASK_BOUNDARY_ONLY = "bounded_function_task_boundary_only"
    SINGLE_CYCLE_FUTURE_GATED = "single_cycle_future_gated"
    INDEPENDENT_AGENT_RUNTIME_BLOCKED = "independent_agent_runtime_blocked"
    MULTI_CYCLE_LOOP_BLOCKED = "multi_cycle_loop_blocked"
    EXTERNAL_AGENT_LOOP_BLOCKED = "external_agent_loop_blocked"
    DOMINION_RUNTIME_BLOCKED = "dominion_runtime_blocked"
    UNKNOWN = "unknown"


class AgenticTaskRuntimeKind(StrEnum):
    BOUNDED_FUNCTION_TASK = "bounded_function_task"
    SINGLE_CYCLE_AGENTIC_OPERATION = "single_cycle_agentic_operation"
    MULTI_CYCLE_AGENTIC_LOOP = "multi_cycle_agentic_loop"
    INDEPENDENT_AUTONOMOUS_AGENT = "independent_autonomous_agent"
    EXTERNAL_AGENT_ORCHESTRATION = "external_agent_orchestration"
    DOMINION_RUNTIME = "dominion_runtime"
    INFINITE_AGENT_LOOP = "infinite_agent_loop"
    NO_RUNTIME = "no_runtime"
    UNKNOWN = "unknown"


class PatchApplySandboxSourceKind(StrEnum):
    V0359_HANDOFF_PACKET = "v0359_handoff_packet"
    V0359_CONSOLIDATION_REPORT = "v0359_consolidation_report"
    V0358_CLI_PATCH_PROPOSAL_SURFACE = "v0358_cli_patch_proposal_surface"
    V0357_PATCH_PROPOSAL_TRACE_PACKET = "v0357_patch_proposal_trace_packet"
    V0356_PATCH_REVIEW_PACKET = "v0356_patch_review_packet"
    V0355_PATCH_RISK_REPORT = "v0355_patch_risk_report"
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    MANUAL_DESIGN_NOTE = "manual_design_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0360_VERSION not in version:
        raise ValueError("version must include v0.36.0")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.0")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.36.0")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret", "credential", "api_key", "token")):
            raise ValueError("metadata keys must not request credential or secret material")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


@dataclass(frozen=True)
class PatchApplySandboxFlagSet:
    flag_set_id: str
    version: str
    patch_apply_sandbox_boundary_constructed: bool
    patch_apply_sandbox_policy_defined: bool
    human_approval_boundary_defined: bool
    bounded_agentic_task_boundary_defined: bool
    patch_apply_risk_register_defined: bool
    ready_for_v0361_apply_candidate_human_approval_contract: bool
    ready_for_v0362_dry_run_patch_apply_simulation: bool
    ready_for_patch_apply_sandbox_boundary: bool
    ready_for_human_approval_boundary: bool
    ready_for_bounded_agentic_task_boundary: bool
    ready_for_agentic_function_task_execution_boundary: bool
    ready_for_execution: bool = False
    ready_for_dry_run_apply_simulation: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxSourceRef:
    source_ref_id: str
    source_kind: PatchApplySandboxSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplySandboxSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxPolicy:
    policy_id: str
    version: str
    write_posture: PatchApplyWritePosture | str
    execution_posture: PatchApplyExecutionPosture | str
    human_approval_posture: HumanApprovalPosture | str
    agentic_task_posture: AgenticTaskExecutionPosture | str
    allowed_surfaces: list[PatchApplySandboxSurfaceKind | str]
    prohibited_surfaces: list[PatchApplySandboxSurfaceKind | str]
    prohibited_capabilities: list[PatchApplySandboxCapabilityKind | str]
    prohibited_runtime_actions: list[str]
    allow_boundary_definition: bool
    allow_human_approval_boundary_definition: bool
    allow_bounded_agentic_task_boundary_definition: bool
    allow_apply_candidate_future_gate: bool
    allow_dry_run_future_gate: bool
    allow_sandbox_workspace_future_gate: bool
    allow_sandbox_apply_future_gate: bool
    allow_dry_run_apply_simulation: bool = False
    allow_sandbox_patch_apply: bool = False
    allow_sandbox_workspace_write: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    allow_infinite_agent_loop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("policy_id", "version"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchApplyWritePosture(self.write_posture)
        PatchApplyExecutionPosture(self.execution_posture)
        HumanApprovalPosture(self.human_approval_posture)
        AgenticTaskExecutionPosture(self.agentic_task_posture)
        _validate_enum_list("allowed_surfaces", self.allowed_surfaces, PatchApplySandboxSurfaceKind)
        _validate_enum_list("prohibited_surfaces", self.prohibited_surfaces, PatchApplySandboxSurfaceKind)
        _validate_enum_list("prohibited_capabilities", self.prohibited_capabilities, PatchApplySandboxCapabilityKind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, ("allow_dry_run_apply_simulation", "allow_sandbox_patch_apply", "allow_sandbox_workspace_write", "allow_live_workspace_write", "allow_patch_application", "allow_workspace_write", "allow_code_edit", "allow_apply_patch", "allow_git_apply", "allow_test_execution", "allow_shell", "allow_dependency_install", "allow_external_agent_execution", "allow_dominion_runtime", "allow_infinite_agent_loop"))
        for surface in (PatchApplySandboxSurfaceKind.LIVE_WORKSPACE_WRITE, PatchApplySandboxSurfaceKind.UNRESTRICTED_PATCH_APPLY, PatchApplySandboxSurfaceKind.GIT_APPLY, PatchApplySandboxSurfaceKind.APPLY_PATCH, PatchApplySandboxSurfaceKind.TEST_EXECUTION, PatchApplySandboxSurfaceKind.SHELL_COMMAND, PatchApplySandboxSurfaceKind.EXTERNAL_AGENT_EXECUTION, PatchApplySandboxSurfaceKind.DOMINION_RUNTIME, PatchApplySandboxSurfaceKind.INFINITE_AGENT_LOOP):
            if surface not in [PatchApplySandboxSurfaceKind(item) for item in self.prohibited_surfaces]:
                raise ValueError(f"prohibited_surfaces missing {surface.value}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class HumanApprovalBoundaryPolicy:
    human_approval_policy_id: str
    version: str
    posture: HumanApprovalPosture | str
    require_operator_supplied_approval: bool
    allow_model_generated_approval: bool
    allow_review_metadata_as_apply_approval: bool
    allow_approval_contract_future_gate: bool
    allow_apply_without_human_approval: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("human_approval_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        HumanApprovalPosture(self.posture)
        _validate_false(self, ("allow_model_generated_approval", "allow_review_metadata_as_apply_approval", "allow_apply_without_human_approval"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class AgenticTaskBoundaryPolicy:
    agentic_task_policy_id: str
    version: str
    posture: AgenticTaskExecutionPosture | str
    allowed_runtime_kinds: list[AgenticTaskRuntimeKind | str]
    blocked_runtime_kinds: list[AgenticTaskRuntimeKind | str]
    allow_bounded_function_task_boundary: bool
    allow_single_cycle_future_gate: bool
    allow_single_cycle_execution: bool
    allow_multi_cycle_loop: bool
    allow_independent_agent_runtime: bool
    allow_external_agent_orchestration: bool
    allow_dominion_runtime: bool
    allow_infinite_agent_loop: bool
    require_human_handoff_after_cycle: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("agentic_task_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        AgenticTaskExecutionPosture(self.posture)
        _validate_enum_list("allowed_runtime_kinds", self.allowed_runtime_kinds, AgenticTaskRuntimeKind)
        _validate_enum_list("blocked_runtime_kinds", self.blocked_runtime_kinds, AgenticTaskRuntimeKind)
        _validate_false(self, ("allow_single_cycle_execution", "allow_multi_cycle_loop", "allow_independent_agent_runtime", "allow_external_agent_orchestration", "allow_dominion_runtime", "allow_infinite_agent_loop"))
        if self.require_human_handoff_after_cycle is not True:
            raise ValueError("require_human_handoff_after_cycle should be True as a future rule")
        for blocked in (AgenticTaskRuntimeKind.MULTI_CYCLE_AGENTIC_LOOP, AgenticTaskRuntimeKind.INDEPENDENT_AUTONOMOUS_AGENT, AgenticTaskRuntimeKind.EXTERNAL_AGENT_ORCHESTRATION, AgenticTaskRuntimeKind.DOMINION_RUNTIME, AgenticTaskRuntimeKind.INFINITE_AGENT_LOOP):
            if blocked not in [AgenticTaskRuntimeKind(item) for item in self.blocked_runtime_kinds]:
                raise ValueError(f"blocked_runtime_kinds missing {blocked.value}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxAllowedSurface:
    allowed_surface_id: str
    surface_kind: PatchApplySandboxSurfaceKind | str
    capability_kind: PatchApplySandboxCapabilityKind | str
    description: str
    allowed_only_for_design_stage: bool
    executable_in_v0360: bool
    writes_sandbox: bool
    writes_live_workspace: bool
    applies_patch: bool
    source_refs: list[PatchApplySandboxSourceRef]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("allowed_surface_id", "description"):
            _require_non_blank(name, getattr(self, name))
        PatchApplySandboxSurfaceKind(self.surface_kind)
        PatchApplySandboxCapabilityKind(self.capability_kind)
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, ("executable_in_v0360", "writes_sandbox", "writes_live_workspace", "applies_patch"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxProhibitedSurface:
    prohibited_surface_id: str
    surface_kind: PatchApplySandboxSurfaceKind | str
    risk_kind: PatchApplySandboxRiskKind | str
    capability_kind: PatchApplySandboxCapabilityKind | str
    reason: str
    prohibited_runtime_actions: list[str]
    blocks_sandbox_apply: bool
    blocks_live_write: bool
    blocks_runtime_readiness: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("prohibited_surface_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        PatchApplySandboxSurfaceKind(self.surface_kind)
        PatchApplySandboxRiskKind(self.risk_kind)
        PatchApplySandboxCapabilityKind(self.capability_kind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_true(self, ("blocks_sandbox_apply", "blocks_live_write", "blocks_runtime_readiness"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxBoundary:
    boundary_id: str
    version: str
    release_name: str
    sandbox_policy: PatchApplySandboxPolicy
    human_approval_policy: HumanApprovalBoundaryPolicy
    agentic_task_policy: AgenticTaskBoundaryPolicy
    allowed_surfaces: list[PatchApplySandboxAllowedSurface]
    prohibited_surfaces: list[PatchApplySandboxProhibitedSurface]
    flags: PatchApplySandboxFlagSet
    status: PatchApplySandboxStatus | str
    readiness_level: PatchApplySandboxReadinessLevel | str
    summary: str
    gaps: list[str]
    blocked_reasons: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0361_apply_candidate_human_approval_contract: bool
    ready_for_v0362_dry_run_patch_apply_simulation: bool
    ready_for_patch_apply_sandbox_boundary: bool
    ready_for_human_approval_boundary: bool
    ready_for_bounded_agentic_task_boundary: bool
    ready_for_execution: bool = False
    ready_for_dry_run_apply_simulation: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("boundary_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("allowed_surfaces", self.allowed_surfaces)
        _validate_list("prohibited_surfaces", self.prohibited_surfaces)
        for name in ("gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        PatchApplySandboxStatus(self.status)
        PatchApplySandboxReadinessLevel(self.readiness_level)
        if not patch_apply_sandbox_flags_preserve_no_apply(self.flags):
            raise ValueError("flags must preserve no apply/write/execution")
        _validate_false(self, ("ready_for_execution", "ready_for_dry_run_apply_simulation", "ready_for_sandbox_patch_apply", "ready_for_sandbox_workspace_write", "ready_for_live_workspace_write", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxPermissionRequest:
    request_id: str
    requested_surface: PatchApplySandboxSurfaceKind | str
    requested_capability: PatchApplySandboxCapabilityKind | str
    source_refs: list[PatchApplySandboxSourceRef]
    request_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("request_id", "request_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplySandboxSurfaceKind(self.requested_surface)
        PatchApplySandboxCapabilityKind(self.requested_capability)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxPermissionDecision:
    decision_id: str
    request_id: str
    decision_kind: PatchApplySandboxDecisionKind | str
    reason: str
    bounded_boundary_definition_allowed: bool
    human_approval_boundary_definition_allowed: bool
    bounded_agentic_task_boundary_definition_allowed: bool
    design_stage_handoff_allowed: bool
    dry_run_apply_simulation_allowed: bool = False
    sandbox_patch_apply_allowed: bool = False
    sandbox_workspace_write_allowed: bool = False
    live_workspace_write_allowed: bool = False
    patch_application_allowed: bool = False
    workspace_write_allowed: bool = False
    code_edit_allowed: bool = False
    apply_patch_allowed: bool = False
    git_apply_allowed: bool = False
    test_execution_allowed: bool = False
    shell_execution_allowed: bool = False
    subprocess_allowed: bool = False
    command_execution_allowed: bool = False
    dependency_install_allowed: bool = False
    reference_execution_allowed: bool = False
    reference_import_allowed: bool = False
    external_agent_execution_allowed: bool = False
    claude_code_invocation_allowed: bool = False
    codex_cli_invocation_allowed: bool = False
    dominion_runtime_allowed: bool = False
    infinite_agent_loop_allowed: bool = False
    autonomous_agent_runtime_allowed: bool = False
    independent_agent_runtime_allowed: bool = False
    multi_cycle_agentic_loop_allowed: bool = False
    provider_invocation_allowed: bool = False
    network_access_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    persistent_trace_write_allowed: bool = False
    ui_runtime_allowed: bool = False
    authority_grant_allowed: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "request_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        PatchApplySandboxDecisionKind(self.decision_kind)
        _validate_false(self, UNSAFE_DECISION_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxDeniedAction:
    denied_action_id: str
    request_id: str | None
    decision_id: str | None
    surface_kind: PatchApplySandboxSurfaceKind | str
    risk_kinds: list[PatchApplySandboxRiskKind | str]
    reason: str
    safe_alternatives: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("denied_action_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        if self.request_id is not None:
            _require_non_blank("request_id", self.request_id)
        if self.decision_id is not None:
            _require_non_blank("decision_id", self.decision_id)
        PatchApplySandboxSurfaceKind(self.surface_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchApplySandboxRiskKind)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxGateEvaluation:
    gate_evaluation_id: str
    request_id: str
    decision: PatchApplySandboxPermissionDecision
    status: PatchApplySandboxStatus | str
    summary: str
    blocked_reasons: list[str]
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_live_workspace_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("gate_evaluation_id", "request_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplySandboxStatus(self.status)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application", "ready_for_sandbox_patch_apply", "ready_for_live_workspace_write"))
        if not patch_apply_sandbox_decision_is_not_apply_permission(self.decision):
            raise ValueError("decision must not allow apply/write/execution")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxRiskRegister:
    risk_register_id: str
    version: str
    risk_kinds: list[PatchApplySandboxRiskKind | str]
    high_risk_surfaces: list[PatchApplySandboxSurfaceKind | str]
    mitigations: list[str]
    blocked_runtime_actions: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version(self.version)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchApplySandboxRiskKind)
        _validate_enum_list("high_risk_surfaces", self.high_risk_surfaces, PatchApplySandboxSurfaceKind)
        _validate_string_list("mitigations", self.mitigations)
        _validate_string_list("blocked_runtime_actions", self.blocked_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        required = [
            PatchApplySandboxRiskKind.LIVE_WORKSPACE_WRITE_RISK,
            PatchApplySandboxRiskKind.SANDBOX_ESCAPE_RISK,
            PatchApplySandboxRiskKind.HUMAN_APPROVAL_FORGERY_RISK,
            PatchApplySandboxRiskKind.MODEL_GENERATED_APPROVAL_RISK,
            PatchApplySandboxRiskKind.APPLY_PATCH_RISK,
            PatchApplySandboxRiskKind.GIT_APPLY_RISK,
            PatchApplySandboxRiskKind.SHELL_EXECUTION_RISK,
            PatchApplySandboxRiskKind.TEST_EXECUTION_RISK,
            PatchApplySandboxRiskKind.DEPENDENCY_INSTALL_RISK,
            PatchApplySandboxRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
            PatchApplySandboxRiskKind.DOMINION_RUNTIME_RISK,
            PatchApplySandboxRiskKind.INFINITE_AGENT_LOOP_RISK,
        ]
        present = [PatchApplySandboxRiskKind(item) for item in self.risk_kinds]
        for item in required:
            if item not in present:
                raise ValueError(f"risk_kinds missing {item.value}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApplySandboxNoLiveWriteGuarantee:
    guarantee_id: str
    version: str
    no_dry_run_apply_simulation: bool
    no_sandbox_workspace_creation: bool
    no_sandbox_patch_apply: bool
    no_sandbox_write: bool
    no_live_workspace_write: bool
    no_patch_application: bool
    no_workspace_write: bool
    no_code_edit: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_test_execution: bool
    no_shell_execution: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_autonomous_agent_runtime: bool
    no_independent_agent_runtime: bool
    no_multi_cycle_agentic_loop: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V036RoadmapOverview:
    roadmap_id: str
    version: str
    track_name: str
    releases: list[str]
    current_release: str
    next_handoff_releases: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("roadmap_id", "track_name", "current_release", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("releases", self.releases)
        _validate_string_list("next_handoff_releases", self.next_handoff_releases)
        if V0360_RELEASE_NAME not in self.current_release:
            raise ValueError("current_release must be v0.36.0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0360ReadinessReport:
    report_id: str
    version: str
    release_name: str
    boundary_id: str
    readiness_level: PatchApplySandboxReadinessLevel | str
    summary: str
    ready_for_v0361_apply_candidate_human_approval_contract: bool
    ready_for_v0362_dry_run_patch_apply_simulation: bool
    ready_for_patch_apply_sandbox_boundary: bool
    ready_for_human_approval_boundary: bool
    ready_for_bounded_agentic_task_boundary: bool
    ready_for_agentic_function_task_execution_boundary: bool
    ready_for_execution: bool = False
    ready_for_dry_run_apply_simulation: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "release_name", "boundary_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchApplySandboxReadinessLevel(self.readiness_level)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_string_list("withdrawal_conditions", self.withdrawal_conditions)
        _validate_metadata_safe(self.metadata)


def build_patch_apply_sandbox_flags(flag_set_id: str = "patch_apply_sandbox_flags:v0.36.0", **kwargs: Any) -> PatchApplySandboxFlagSet:
    return PatchApplySandboxFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0360_VERSION),
        patch_apply_sandbox_boundary_constructed=kwargs.pop("patch_apply_sandbox_boundary_constructed", True),
        patch_apply_sandbox_policy_defined=kwargs.pop("patch_apply_sandbox_policy_defined", True),
        human_approval_boundary_defined=kwargs.pop("human_approval_boundary_defined", True),
        bounded_agentic_task_boundary_defined=kwargs.pop("bounded_agentic_task_boundary_defined", True),
        patch_apply_risk_register_defined=kwargs.pop("patch_apply_risk_register_defined", True),
        ready_for_v0361_apply_candidate_human_approval_contract=kwargs.pop("ready_for_v0361_apply_candidate_human_approval_contract", True),
        ready_for_v0362_dry_run_patch_apply_simulation=kwargs.pop("ready_for_v0362_dry_run_patch_apply_simulation", True),
        ready_for_patch_apply_sandbox_boundary=kwargs.pop("ready_for_patch_apply_sandbox_boundary", True),
        ready_for_human_approval_boundary=kwargs.pop("ready_for_human_approval_boundary", True),
        ready_for_bounded_agentic_task_boundary=kwargs.pop("ready_for_bounded_agentic_task_boundary", True),
        ready_for_agentic_function_task_execution_boundary=kwargs.pop("ready_for_agentic_function_task_execution_boundary", True),
        **kwargs,
    )


def build_patch_apply_sandbox_source_ref(source_ref_id: str = "patch_apply_source:v0.36.0", **kwargs: Any) -> PatchApplySandboxSourceRef:
    return PatchApplySandboxSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchApplySandboxSourceKind.V0359_HANDOFF_PACKET),
        source_id=kwargs.pop("source_id", "v036_handoff:v0.35.9"),
        source_summary=kwargs.pop("source_summary", "v0.35.9 design-stage handoff metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.35/v0.35.9_controlled_patch_proposal_layer_consolidation.md"]),
        **kwargs,
    )


def build_patch_apply_sandbox_policy(policy_id: str = "patch_apply_sandbox_policy:v0.36.0", **kwargs: Any) -> PatchApplySandboxPolicy:
    return PatchApplySandboxPolicy(
        policy_id=policy_id,
        version=kwargs.pop("version", V0360_VERSION),
        write_posture=kwargs.pop("write_posture", PatchApplyWritePosture.NO_WRITE),
        execution_posture=kwargs.pop("execution_posture", PatchApplyExecutionPosture.NO_APPLY),
        human_approval_posture=kwargs.pop("human_approval_posture", HumanApprovalPosture.HUMAN_APPROVAL_CONTRACT_FUTURE_GATED),
        agentic_task_posture=kwargs.pop("agentic_task_posture", AgenticTaskExecutionPosture.BOUNDED_FUNCTION_TASK_BOUNDARY_ONLY),
        allowed_surfaces=kwargs.pop("allowed_surfaces", [PatchApplySandboxSurfaceKind.APPLY_CANDIDATE_ENVELOPE, PatchApplySandboxSurfaceKind.HUMAN_APPROVAL_CONTRACT, PatchApplySandboxSurfaceKind.BOUNDED_AGENTIC_TASK_OPERATION, PatchApplySandboxSurfaceKind.AGENTIC_FUNCTION_TASK_EXECUTION]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [PatchApplySandboxSurfaceKind.LIVE_WORKSPACE_WRITE, PatchApplySandboxSurfaceKind.UNRESTRICTED_PATCH_APPLY, PatchApplySandboxSurfaceKind.GIT_APPLY, PatchApplySandboxSurfaceKind.APPLY_PATCH, PatchApplySandboxSurfaceKind.TEST_EXECUTION, PatchApplySandboxSurfaceKind.SHELL_COMMAND, PatchApplySandboxSurfaceKind.DEPENDENCY_INSTALL, PatchApplySandboxSurfaceKind.EXTERNAL_AGENT_EXECUTION, PatchApplySandboxSurfaceKind.DOMINION_RUNTIME, PatchApplySandboxSurfaceKind.INFINITE_AGENT_LOOP]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", [PatchApplySandboxCapabilityKind.PERFORM_SANDBOX_PATCH_APPLY, PatchApplySandboxCapabilityKind.PERFORM_LIVE_PATCH_APPLY, PatchApplySandboxCapabilityKind.WRITE_SANDBOX_FILE, PatchApplySandboxCapabilityKind.WRITE_LIVE_WORKSPACE_FILE, PatchApplySandboxCapabilityKind.EDIT_CODE_FILE, PatchApplySandboxCapabilityKind.CALL_APPLY_PATCH, PatchApplySandboxCapabilityKind.CALL_GIT_APPLY, PatchApplySandboxCapabilityKind.RUN_TESTS, PatchApplySandboxCapabilityKind.EXECUTE_SHELL, PatchApplySandboxCapabilityKind.INSTALL_DEPENDENCY, PatchApplySandboxCapabilityKind.EXECUTE_EXTERNAL_AGENT, PatchApplySandboxCapabilityKind.RUN_DOMINION_RUNTIME, PatchApplySandboxCapabilityKind.RUN_INFINITE_AGENT_LOOP]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["dry_run_apply_simulation", "sandbox_patch_apply", "sandbox_workspace_write", "live_workspace_write", "patch_application", "workspace_write", "code_edit", "apply_patch", "git_apply", "test_execution", "shell_execution", "external_agent_execution", "dominion_runtime", "infinite_agent_loop"]),
        allow_boundary_definition=kwargs.pop("allow_boundary_definition", True),
        allow_human_approval_boundary_definition=kwargs.pop("allow_human_approval_boundary_definition", True),
        allow_bounded_agentic_task_boundary_definition=kwargs.pop("allow_bounded_agentic_task_boundary_definition", True),
        allow_apply_candidate_future_gate=kwargs.pop("allow_apply_candidate_future_gate", True),
        allow_dry_run_future_gate=kwargs.pop("allow_dry_run_future_gate", True),
        allow_sandbox_workspace_future_gate=kwargs.pop("allow_sandbox_workspace_future_gate", True),
        allow_sandbox_apply_future_gate=kwargs.pop("allow_sandbox_apply_future_gate", True),
        **kwargs,
    )


def build_human_approval_boundary_policy(human_approval_policy_id: str = "human_approval_boundary_policy:v0.36.0", **kwargs: Any) -> HumanApprovalBoundaryPolicy:
    return HumanApprovalBoundaryPolicy(
        human_approval_policy_id=human_approval_policy_id,
        version=kwargs.pop("version", V0360_VERSION),
        posture=kwargs.pop("posture", HumanApprovalPosture.HUMAN_APPROVAL_CONTRACT_FUTURE_GATED),
        require_operator_supplied_approval=kwargs.pop("require_operator_supplied_approval", True),
        allow_model_generated_approval=kwargs.pop("allow_model_generated_approval", False),
        allow_review_metadata_as_apply_approval=kwargs.pop("allow_review_metadata_as_apply_approval", False),
        allow_approval_contract_future_gate=kwargs.pop("allow_approval_contract_future_gate", True),
        allow_apply_without_human_approval=kwargs.pop("allow_apply_without_human_approval", False),
        summary=kwargs.pop("summary", "Human approval boundary defined; approval contract remains v0.36.1 future gate."),
        **kwargs,
    )


def build_agentic_task_boundary_policy(agentic_task_policy_id: str = "agentic_task_boundary_policy:v0.36.0", **kwargs: Any) -> AgenticTaskBoundaryPolicy:
    return AgenticTaskBoundaryPolicy(
        agentic_task_policy_id=agentic_task_policy_id,
        version=kwargs.pop("version", V0360_VERSION),
        posture=kwargs.pop("posture", AgenticTaskExecutionPosture.BOUNDED_FUNCTION_TASK_BOUNDARY_ONLY),
        allowed_runtime_kinds=kwargs.pop("allowed_runtime_kinds", [AgenticTaskRuntimeKind.BOUNDED_FUNCTION_TASK, AgenticTaskRuntimeKind.NO_RUNTIME]),
        blocked_runtime_kinds=kwargs.pop("blocked_runtime_kinds", [AgenticTaskRuntimeKind.SINGLE_CYCLE_AGENTIC_OPERATION, AgenticTaskRuntimeKind.MULTI_CYCLE_AGENTIC_LOOP, AgenticTaskRuntimeKind.INDEPENDENT_AUTONOMOUS_AGENT, AgenticTaskRuntimeKind.EXTERNAL_AGENT_ORCHESTRATION, AgenticTaskRuntimeKind.DOMINION_RUNTIME, AgenticTaskRuntimeKind.INFINITE_AGENT_LOOP]),
        allow_bounded_function_task_boundary=kwargs.pop("allow_bounded_function_task_boundary", True),
        allow_single_cycle_future_gate=kwargs.pop("allow_single_cycle_future_gate", True),
        allow_single_cycle_execution=kwargs.pop("allow_single_cycle_execution", False),
        allow_multi_cycle_loop=kwargs.pop("allow_multi_cycle_loop", False),
        allow_independent_agent_runtime=kwargs.pop("allow_independent_agent_runtime", False),
        allow_external_agent_orchestration=kwargs.pop("allow_external_agent_orchestration", False),
        allow_dominion_runtime=kwargs.pop("allow_dominion_runtime", False),
        allow_infinite_agent_loop=kwargs.pop("allow_infinite_agent_loop", False),
        require_human_handoff_after_cycle=kwargs.pop("require_human_handoff_after_cycle", True),
        summary=kwargs.pop("summary", "Agentic operation means bounded function/task boundary only in v0.36.0."),
        **kwargs,
    )


def build_patch_apply_sandbox_allowed_surface(allowed_surface_id: str = "allowed_surface:v0.36.0:boundary", **kwargs: Any) -> PatchApplySandboxAllowedSurface:
    return PatchApplySandboxAllowedSurface(
        allowed_surface_id=allowed_surface_id,
        surface_kind=kwargs.pop("surface_kind", PatchApplySandboxSurfaceKind.APPLY_CANDIDATE_ENVELOPE),
        capability_kind=kwargs.pop("capability_kind", PatchApplySandboxCapabilityKind.CREATE_APPLY_CANDIDATE_FUTURE_GATE),
        description=kwargs.pop("description", "Design-stage future gate surface only."),
        allowed_only_for_design_stage=kwargs.pop("allowed_only_for_design_stage", True),
        executable_in_v0360=kwargs.pop("executable_in_v0360", False),
        writes_sandbox=kwargs.pop("writes_sandbox", False),
        writes_live_workspace=kwargs.pop("writes_live_workspace", False),
        applies_patch=kwargs.pop("applies_patch", False),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_sandbox_source_ref()]),
        **kwargs,
    )


def build_patch_apply_sandbox_prohibited_surface(prohibited_surface_id: str = "prohibited_surface:v0.36.0:apply", **kwargs: Any) -> PatchApplySandboxProhibitedSurface:
    return PatchApplySandboxProhibitedSurface(
        prohibited_surface_id=prohibited_surface_id,
        surface_kind=kwargs.pop("surface_kind", PatchApplySandboxSurfaceKind.UNRESTRICTED_PATCH_APPLY),
        risk_kind=kwargs.pop("risk_kind", PatchApplySandboxRiskKind.PATCH_APPLY_RISK),
        capability_kind=kwargs.pop("capability_kind", PatchApplySandboxCapabilityKind.PERFORM_LIVE_PATCH_APPLY),
        reason=kwargs.pop("reason", "v0.36.0 defines boundary only and does not apply patches."),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["patch_application", "workspace_write", "code_edit"]),
        blocks_sandbox_apply=kwargs.pop("blocks_sandbox_apply", True),
        blocks_live_write=kwargs.pop("blocks_live_write", True),
        blocks_runtime_readiness=kwargs.pop("blocks_runtime_readiness", True),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.0_human_approved_patch_apply_sandbox_boundary.md"]),
        **kwargs,
    )


def build_patch_apply_sandbox_boundary(boundary_id: str = "patch_apply_sandbox_boundary:v0.36.0", **kwargs: Any) -> PatchApplySandboxBoundary:
    return PatchApplySandboxBoundary(
        boundary_id=boundary_id,
        version=kwargs.pop("version", V0360_VERSION),
        release_name=kwargs.pop("release_name", V0360_RELEASE_NAME),
        sandbox_policy=kwargs.pop("sandbox_policy", build_patch_apply_sandbox_policy()),
        human_approval_policy=kwargs.pop("human_approval_policy", build_human_approval_boundary_policy()),
        agentic_task_policy=kwargs.pop("agentic_task_policy", build_agentic_task_boundary_policy()),
        allowed_surfaces=kwargs.pop("allowed_surfaces", [build_patch_apply_sandbox_allowed_surface()]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [build_patch_apply_sandbox_prohibited_surface()]),
        flags=kwargs.pop("flags", build_patch_apply_sandbox_flags()),
        status=kwargs.pop("status", PatchApplySandboxStatus.BOUNDARY_READY),
        readiness_level=kwargs.pop("readiness_level", PatchApplySandboxReadinessLevel.APPLY_SANDBOX_BOUNDARY_READY),
        summary=kwargs.pop("summary", "Human-approved patch apply sandbox boundary foundation only; no apply/write/execution."),
        gaps=kwargs.pop("gaps", ["human approval contract is v0.36.1", "dry-run apply simulation is v0.36.2"]),
        blocked_reasons=kwargs.pop("blocked_reasons", []),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.35/v0.35.9_controlled_patch_proposal_layer_consolidation.md"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any dry-run apply, sandbox apply, workspace write, shell execution, external agent execution, or Dominion runtime is introduced."]),
        ready_for_v0361_apply_candidate_human_approval_contract=kwargs.pop("ready_for_v0361_apply_candidate_human_approval_contract", True),
        ready_for_v0362_dry_run_patch_apply_simulation=kwargs.pop("ready_for_v0362_dry_run_patch_apply_simulation", True),
        ready_for_patch_apply_sandbox_boundary=kwargs.pop("ready_for_patch_apply_sandbox_boundary", True),
        ready_for_human_approval_boundary=kwargs.pop("ready_for_human_approval_boundary", True),
        ready_for_bounded_agentic_task_boundary=kwargs.pop("ready_for_bounded_agentic_task_boundary", True),
        **kwargs,
    )


def build_patch_apply_sandbox_permission_request(request_id: str = "patch_apply_permission_request:v0.36.0", **kwargs: Any) -> PatchApplySandboxPermissionRequest:
    return PatchApplySandboxPermissionRequest(
        request_id=request_id,
        requested_surface=kwargs.pop("requested_surface", PatchApplySandboxSurfaceKind.APPLY_CANDIDATE_ENVELOPE),
        requested_capability=kwargs.pop("requested_capability", PatchApplySandboxCapabilityKind.DEFINE_APPLY_SANDBOX_BOUNDARY),
        source_refs=kwargs.pop("source_refs", [build_patch_apply_sandbox_source_ref()]),
        request_summary=kwargs.pop("request_summary", "Boundary definition request only."),
        **kwargs,
    )


def build_patch_apply_sandbox_permission_decision(decision_id: str = "patch_apply_permission_decision:v0.36.0", **kwargs: Any) -> PatchApplySandboxPermissionDecision:
    return PatchApplySandboxPermissionDecision(
        decision_id=decision_id,
        request_id=kwargs.pop("request_id", "patch_apply_permission_request:v0.36.0"),
        decision_kind=kwargs.pop("decision_kind", PatchApplySandboxDecisionKind.ALLOW_BOUNDARY_DEFINITION),
        reason=kwargs.pop("reason", "Boundary definition allowed; apply/write/execution denied."),
        bounded_boundary_definition_allowed=kwargs.pop("bounded_boundary_definition_allowed", True),
        human_approval_boundary_definition_allowed=kwargs.pop("human_approval_boundary_definition_allowed", True),
        bounded_agentic_task_boundary_definition_allowed=kwargs.pop("bounded_agentic_task_boundary_definition_allowed", True),
        design_stage_handoff_allowed=kwargs.pop("design_stage_handoff_allowed", True),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.0_human_approved_patch_apply_sandbox_boundary.md"]),
        **kwargs,
    )


def build_patch_apply_sandbox_denied_action(denied_action_id: str = "patch_apply_denied_action:v0.36.0", **kwargs: Any) -> PatchApplySandboxDeniedAction:
    return PatchApplySandboxDeniedAction(
        denied_action_id=denied_action_id,
        request_id=kwargs.pop("request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        surface_kind=kwargs.pop("surface_kind", PatchApplySandboxSurfaceKind.UNRESTRICTED_PATCH_APPLY),
        risk_kinds=kwargs.pop("risk_kinds", [PatchApplySandboxRiskKind.PATCH_APPLY_RISK]),
        reason=kwargs.pop("reason", "Patch apply is not available in v0.36.0."),
        safe_alternatives=kwargs.pop("safe_alternatives", ["define boundary metadata", "handoff to v0.36.1/v0.36.2"]),
        **kwargs,
    )


def build_patch_apply_sandbox_gate_evaluation(gate_evaluation_id: str = "patch_apply_gate_evaluation:v0.36.0", decision: PatchApplySandboxPermissionDecision | None = None, **kwargs: Any) -> PatchApplySandboxGateEvaluation:
    decision = decision or kwargs.pop("decision", build_patch_apply_sandbox_permission_decision())
    return PatchApplySandboxGateEvaluation(
        gate_evaluation_id=gate_evaluation_id,
        request_id=kwargs.pop("request_id", decision.request_id),
        decision=decision,
        status=kwargs.pop("status", PatchApplySandboxStatus.BOUNDARY_READY),
        summary=kwargs.pop("summary", "Gate permits boundary metadata only."),
        blocked_reasons=kwargs.pop("blocked_reasons", []),
        **kwargs,
    )


def build_patch_apply_sandbox_risk_register(risk_register_id: str = "patch_apply_risk_register:v0.36.0", **kwargs: Any) -> PatchApplySandboxRiskRegister:
    return PatchApplySandboxRiskRegister(
        risk_register_id=risk_register_id,
        version=kwargs.pop("version", V0360_VERSION),
        risk_kinds=kwargs.pop("risk_kinds", list(PatchApplySandboxRiskKind)),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", [PatchApplySandboxSurfaceKind.LIVE_WORKSPACE_WRITE, PatchApplySandboxSurfaceKind.UNRESTRICTED_PATCH_APPLY, PatchApplySandboxSurfaceKind.APPLY_PATCH, PatchApplySandboxSurfaceKind.GIT_APPLY, PatchApplySandboxSurfaceKind.SHELL_COMMAND, PatchApplySandboxSurfaceKind.EXTERNAL_AGENT_EXECUTION, PatchApplySandboxSurfaceKind.DOMINION_RUNTIME, PatchApplySandboxSurfaceKind.INFINITE_AGENT_LOOP]),
        mitigations=kwargs.pop("mitigations", ["boundary only", "human approval future gate", "sandbox and dry-run future-gated", "agentic task is bounded function/task boundary only"]),
        blocked_runtime_actions=kwargs.pop("blocked_runtime_actions", ["patch_application", "workspace_write", "code_edit", "apply_patch", "git_apply", "test_execution", "shell_execution", "dependency_install", "external_agent_execution", "dominion_runtime", "infinite_agent_loop"]),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.0_human_approved_patch_apply_sandbox_boundary.md"]),
        **kwargs,
    )


def build_patch_apply_sandbox_no_live_write_guarantee(guarantee_id: str = "patch_apply_no_live_write_guarantee:v0.36.0", **kwargs: Any) -> PatchApplySandboxNoLiveWriteGuarantee:
    return PatchApplySandboxNoLiveWriteGuarantee(
        guarantee_id=guarantee_id,
        version=kwargs.pop("version", V0360_VERSION),
        no_dry_run_apply_simulation=kwargs.pop("no_dry_run_apply_simulation", True),
        no_sandbox_workspace_creation=kwargs.pop("no_sandbox_workspace_creation", True),
        no_sandbox_patch_apply=kwargs.pop("no_sandbox_patch_apply", True),
        no_sandbox_write=kwargs.pop("no_sandbox_write", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_patch_application=kwargs.pop("no_patch_application", True),
        no_workspace_write=kwargs.pop("no_workspace_write", True),
        no_code_edit=kwargs.pop("no_code_edit", True),
        no_apply_patch=kwargs.pop("no_apply_patch", True),
        no_git_apply=kwargs.pop("no_git_apply", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        no_autonomous_agent_runtime=kwargs.pop("no_autonomous_agent_runtime", True),
        no_independent_agent_runtime=kwargs.pop("no_independent_agent_runtime", True),
        no_multi_cycle_agentic_loop=kwargs.pop("no_multi_cycle_agentic_loop", True),
        summary=kwargs.pop("summary", "v0.36.0 introduces no live write, sandbox write, apply, or autonomous runtime."),
        **kwargs,
    )


def build_v036_roadmap_overview(roadmap_id: str = "v036_roadmap:v0.36.0", **kwargs: Any) -> V036RoadmapOverview:
    return V036RoadmapOverview(
        roadmap_id=roadmap_id,
        version=kwargs.pop("version", V0360_VERSION),
        track_name=kwargs.pop("track_name", "Human-approved Patch Apply Sandbox"),
        releases=kwargs.pop("releases", list(V036_ROADMAP)),
        current_release=kwargs.pop("current_release", V0360_RELEASE_NAME),
        next_handoff_releases=kwargs.pop("next_handoff_releases", ["v0.36.1 Apply Candidate & Human Approval Contract", "v0.36.2 Dry-run Patch Apply Simulation"]),
        summary=kwargs.pop("summary", "v0.36 starts with boundary foundation only."),
        **kwargs,
    )


def build_v0360_readiness_report(report_id: str = "v0360_readiness_report", **kwargs: Any) -> V0360ReadinessReport:
    return V0360ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0360_VERSION),
        release_name=kwargs.pop("release_name", V0360_RELEASE_NAME),
        boundary_id=kwargs.pop("boundary_id", "patch_apply_sandbox_boundary:v0.36.0"),
        readiness_level=kwargs.pop("readiness_level", PatchApplySandboxReadinessLevel.APPLY_SANDBOX_BOUNDARY_READY),
        summary=kwargs.pop("summary", "Patch apply sandbox boundary is ready; apply/write/execution remain false."),
        ready_for_v0361_apply_candidate_human_approval_contract=kwargs.pop("ready_for_v0361_apply_candidate_human_approval_contract", True),
        ready_for_v0362_dry_run_patch_apply_simulation=kwargs.pop("ready_for_v0362_dry_run_patch_apply_simulation", True),
        ready_for_patch_apply_sandbox_boundary=kwargs.pop("ready_for_patch_apply_sandbox_boundary", True),
        ready_for_human_approval_boundary=kwargs.pop("ready_for_human_approval_boundary", True),
        ready_for_bounded_agentic_task_boundary=kwargs.pop("ready_for_bounded_agentic_task_boundary", True),
        ready_for_agentic_function_task_execution_boundary=kwargs.pop("ready_for_agentic_function_task_execution_boundary", True),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.0_human_approved_patch_apply_sandbox_boundary.md"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any dry-run apply, sandbox apply, workspace write, external agent execution, Dominion runtime, autonomous runtime, or unsafe readiness flag is introduced."]),
        **kwargs,
    )


def patch_apply_sandbox_flags_preserve_no_apply(flags: PatchApplySandboxFlagSet) -> bool:
    return isinstance(flags, PatchApplySandboxFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def patch_apply_sandbox_policy_blocks_live_write(policy: PatchApplySandboxPolicy) -> bool:
    return not any(getattr(policy, name) for name in ("allow_dry_run_apply_simulation", "allow_sandbox_patch_apply", "allow_sandbox_workspace_write", "allow_live_workspace_write", "allow_patch_application", "allow_workspace_write", "allow_code_edit", "allow_apply_patch", "allow_git_apply", "allow_test_execution", "allow_shell", "allow_dependency_install", "allow_external_agent_execution", "allow_dominion_runtime", "allow_infinite_agent_loop"))


def human_approval_boundary_rejects_model_approval(policy: HumanApprovalBoundaryPolicy) -> bool:
    return policy.allow_model_generated_approval is False and policy.allow_review_metadata_as_apply_approval is False and policy.allow_apply_without_human_approval is False


def agentic_task_boundary_blocks_autonomous_runtime(policy: AgenticTaskBoundaryPolicy) -> bool:
    return not any(getattr(policy, name) for name in ("allow_single_cycle_execution", "allow_multi_cycle_loop", "allow_independent_agent_runtime", "allow_external_agent_orchestration", "allow_dominion_runtime", "allow_infinite_agent_loop"))


def patch_apply_sandbox_boundary_is_not_apply(boundary: PatchApplySandboxBoundary) -> bool:
    return not any(getattr(boundary, name) for name in ("ready_for_execution", "ready_for_dry_run_apply_simulation", "ready_for_sandbox_patch_apply", "ready_for_sandbox_workspace_write", "ready_for_live_workspace_write", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit"))


def patch_apply_sandbox_decision_is_not_apply_permission(decision: PatchApplySandboxPermissionDecision) -> bool:
    return isinstance(decision, PatchApplySandboxPermissionDecision) and all(getattr(decision, name) is False for name in UNSAFE_DECISION_NAMES)


def v0360_readiness_report_is_not_execution_ready(report: V0360ReadinessReport) -> bool:
    return isinstance(report, V0360ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
