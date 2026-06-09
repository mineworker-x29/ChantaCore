from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_validation import SandboxPostApplyValidationReport


V0366_VERSION = "v0.36.6"
V0366_RELEASE_NAME = "v0.36.6 Bounded Agentic Function/Task Operation Cycle"
MAX_PREVIEW_CHARS = 600

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_independent_agent_runtime",
    "ready_for_autonomous_agent_runtime",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_recursive_self_invocation",
    "ready_for_automatic_retry",
    "ready_for_automatic_repair",
    "ready_for_sandbox_repair",
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
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

PROHIBITED_RUNTIME_ACTIONS = (
    "multi_cycle_loop",
    "automatic_retry",
    "automatic_repair",
    "independent_agent_runtime",
    "live_write",
    "apply",
    "shell",
    "test_execution",
    "dependency_install",
    "external_agent_execution",
    "dominion_runtime",
)


class AgenticOperationMode(StrEnum):
    METADATA_ONLY_CYCLE = "metadata_only_cycle"
    SUPPLIED_ARTIFACT_CYCLE = "supplied_artifact_cycle"
    BOUNDED_FUNCTION_TASK_CYCLE = "bounded_function_task_cycle"
    SANDBOX_APPLY_VALIDATION_CYCLE = "sandbox_apply_validation_cycle"
    HUMAN_HANDOFF_CYCLE = "human_handoff_cycle"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class AgenticOperationSourceKind(StrEnum):
    V0365_POST_APPLY_VALIDATION_REPORT = "v0365_post_apply_validation_report"
    V0365_SANDBOX_RECONCILIATION_REPORT = "v0365_sandbox_reconciliation_report"
    V0365_SANDBOX_SAFETY_REPORT = "v0365_sandbox_safety_report"
    V0364_SANDBOX_PATCH_APPLY_RESULT = "v0364_sandbox_patch_apply_result"
    V0363_SANDBOX_WORKSPACE_MANIFEST = "v0363_sandbox_workspace_manifest"
    V0362_DRY_RUN_APPLY_SIMULATION_RESULT = "v0362_dry_run_apply_simulation_result"
    V0361_APPLY_CANDIDATE_ENVELOPE = "v0361_apply_candidate_envelope"
    V0361_HUMAN_APPROVAL_CONTRACT = "v0361_human_approval_contract"
    V0359_CONTROLLED_PATCH_PROPOSAL_CONSOLIDATION = "v0359_controlled_patch_proposal_consolidation"
    MANUAL_OPERATOR_TASK = "manual_operator_task"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class AgenticOperationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    CYCLE_READY = "cycle_ready"
    CYCLE_COMPLETED = "cycle_completed"
    CYCLE_COMPLETED_WITH_WARNINGS = "cycle_completed_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    STOPPED = "stopped"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class AgenticOperationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    OPERATION_CONTRACT_READY = "operation_contract_ready"
    SINGLE_CYCLE_PACKET_READY = "single_cycle_packet_ready"
    STEP_SEQUENCE_READY = "step_sequence_ready"
    SAFETY_REPORT_READY = "safety_report_ready"
    HUMAN_HANDOFF_READY = "human_handoff_ready"
    DESIGN_HANDOFF_READY_FOR_V0367 = "design_handoff_ready_for_v0367"
    DESIGN_HANDOFF_READY_FOR_V0368 = "design_handoff_ready_for_v0368"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class AgenticOperationDecisionKind(StrEnum):
    ALLOW_METADATA_CYCLE = "allow_metadata_cycle"
    ALLOW_SINGLE_CYCLE_PACKET = "allow_single_cycle_packet"
    ALLOW_STEP_RECORDING = "allow_step_recording"
    ALLOW_SAFETY_REPORT = "allow_safety_report"
    ALLOW_HUMAN_HANDOFF = "allow_human_handoff"
    ALLOW_FUTURE_TRACE_INPUT = "allow_future_trace_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class AgenticOperationRiskKind(StrEnum):
    MISSING_STAGE_ARTIFACT_RISK = "missing_stage_artifact_risk"
    FAILED_POST_APPLY_VALIDATION_RISK = "failed_post_apply_validation_risk"
    BLOCKING_SAFETY_FINDING_RISK = "blocking_safety_finding_risk"
    AUTOMATIC_RETRY_RISK = "automatic_retry_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    RECURSIVE_SELF_INVOCATION_RISK = "recursive_self_invocation_risk"
    INDEPENDENT_AGENT_RUNTIME_RISK = "independent_agent_runtime_risk"
    AUTONOMOUS_AGENT_RUNTIME_RISK = "autonomous_agent_runtime_risk"
    GENERAL_TOOL_EXECUTION_RISK = "general_tool_execution_risk"
    MODEL_INVOCATION_RISK = "model_invocation_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    CLAUDE_CODE_INVOCATION_RISK = "claude_code_invocation_risk"
    CODEX_CLI_INVOCATION_RISK = "codex_cli_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class AgenticOperationStepKind(StrEnum):
    VALIDATE_OPERATION_INPUT = "validate_operation_input"
    VERIFY_HUMAN_APPROVAL_CONTRACT = "verify_human_approval_contract"
    VERIFY_DRY_RUN_RESULT = "verify_dry_run_result"
    VERIFY_SANDBOX_MANIFEST = "verify_sandbox_manifest"
    VERIFY_SANDBOX_APPLY_RESULT = "verify_sandbox_apply_result"
    VERIFY_POST_APPLY_VALIDATION = "verify_post_apply_validation"
    VERIFY_SAFETY_REPORT = "verify_safety_report"
    CREATE_STEP_SEQUENCE = "create_step_sequence"
    CREATE_OPERATION_RESULT = "create_operation_result"
    CREATE_HUMAN_HANDOFF = "create_human_handoff"
    RECORD_DIGESTION_DOMINION_BOUNDARY = "record_digestion_dominion_boundary"
    BLOCK_EXTERNAL_AGENT_PATH = "block_external_agent_path"
    BLOCK_MULTI_CYCLE_LOOP = "block_multi_cycle_loop"
    NO_OP_STEP = "no_op_step"
    UNKNOWN = "unknown"


class AgenticOperationStepStatus(StrEnum):
    UNKNOWN = "unknown"
    PENDING = "pending"
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FAILED_SAFE = "failed_safe"
    NO_OP = "no_op"


class AgenticOperationStopReasonKind(StrEnum):
    COMPLETED_SINGLE_CYCLE = "completed_single_cycle"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    BLOCKED_BY_MISSING_ARTIFACT = "blocked_by_missing_artifact"
    BLOCKED_BY_SAFETY_REPORT = "blocked_by_safety_report"
    BLOCKED_BY_FAILED_VALIDATION = "blocked_by_failed_validation"
    BLOCKED_BY_POLICY = "blocked_by_policy"
    STOPPED_FOR_HUMAN_HANDOFF = "stopped_for_human_handoff"
    STOPPED_NO_RETRY_ALLOWED = "stopped_no_retry_allowed"
    STOPPED_NO_REPAIR_ALLOWED = "stopped_no_repair_allowed"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class AgenticOperationRuntimeKind(StrEnum):
    BOUNDED_FUNCTION_TASK = "bounded_function_task"
    SINGLE_CYCLE_OPERATION = "single_cycle_operation"
    METADATA_ONLY_OPERATION = "metadata_only_operation"
    INDEPENDENT_AUTONOMOUS_AGENT = "independent_autonomous_agent"
    MULTI_CYCLE_AGENTIC_LOOP = "multi_cycle_agentic_loop"
    RECURSIVE_SELF_INVOCATION = "recursive_self_invocation"
    EXTERNAL_AGENT_ORCHESTRATION = "external_agent_orchestration"
    DOMINION_RUNTIME = "dominion_runtime"
    GENERAL_TOOL_RUNTIME = "general_tool_runtime"
    UNKNOWN = "unknown"


class AgenticOperationHandoffKind(StrEnum):
    HUMAN_HANDOFF_REQUIRED = "human_handoff_required"
    FUTURE_TRACE_PACKET_HANDOFF = "future_trace_packet_handoff"
    FUTURE_CLI_SURFACE_HANDOFF = "future_cli_surface_handoff"
    FUTURE_TEST_RUNNER_HANDOFF = "future_test_runner_handoff"
    FUTURE_REPAIR_LOOP_HANDOFF = "future_repair_loop_handoff"
    BLOCKED_HANDOFF = "blocked_handoff"
    NO_OP_HANDOFF = "no_op_handoff"
    UNKNOWN = "unknown"


class AgenticOperationSafetyCheckKind(StrEnum):
    NO_MULTI_CYCLE_LOOP_CHECK = "no_multi_cycle_loop_check"
    NO_AUTOMATIC_RETRY_CHECK = "no_automatic_retry_check"
    NO_AUTOMATIC_REPAIR_CHECK = "no_automatic_repair_check"
    NO_RECURSIVE_SELF_INVOCATION_CHECK = "no_recursive_self_invocation_check"
    NO_INDEPENDENT_AGENT_RUNTIME_CHECK = "no_independent_agent_runtime_check"
    NO_EXTERNAL_AGENT_EXECUTION_CHECK = "no_external_agent_execution_check"
    NO_DOMINION_RUNTIME_CHECK = "no_dominion_runtime_check"
    NO_LIVE_WORKSPACE_WRITE_CHECK = "no_live_workspace_write_check"
    NO_PATCH_APPLICATION_CHECK = "no_patch_application_check"
    NO_SHELL_EXECUTION_CHECK = "no_shell_execution_check"
    NO_TEST_EXECUTION_CHECK = "no_test_execution_check"
    NO_DEPENDENCY_INSTALL_CHECK = "no_dependency_install_check"
    NO_MODEL_INVOCATION_CHECK = "no_model_invocation_check"
    NO_GENERAL_TOOL_EXECUTION_CHECK = "no_general_tool_execution_check"
    POST_APPLY_VALIDATION_SUCCESS_CHECK = "post_apply_validation_success_check"
    HUMAN_HANDOFF_REQUIRED_CHECK = "human_handoff_required_check"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0366_VERSION not in version:
        raise ValueError("version must include v0.36.6")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.6")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _bounded_preview(value: str, max_chars: int = MAX_PREVIEW_CHARS) -> str:
    if not isinstance(value, str):
        raise TypeError("preview value must be str")
    redacted = value
    for token in ("secret", "credential", "api_key", "token", "password"):
        redacted = redacted.replace(token, "[redacted]")
        redacted = redacted.replace(token.upper(), "[redacted]")
    return redacted[:max_chars]


@dataclass(frozen=True, kw_only=True)
class AgenticOperationFlagSet:
    flag_set_id: str
    version: str
    agentic_operation_cycle_constructed: bool
    bounded_function_task_policy_defined: bool
    single_cycle_operation_packet_available: bool
    agentic_step_recording_available: bool
    agentic_safety_report_available: bool
    human_handoff_after_cycle_available: bool
    ready_for_v0367_patch_apply_sandbox_ocel_trace_packet: bool
    ready_for_v0368_cli_sandbox_apply_agentic_surface: bool
    ready_for_bounded_agentic_task_operation_cycle: bool
    ready_for_agentic_function_task_execution: bool
    ready_for_single_cycle_operation_packet: bool
    ready_for_agentic_step_recording: bool
    ready_for_agentic_operation_safety_report: bool
    ready_for_human_handoff_after_cycle: bool
    ready_for_future_trace_input: bool
    ready_for_execution: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_recursive_self_invocation: bool = False
    ready_for_automatic_retry: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_sandbox_repair: bool = False
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


@dataclass(frozen=True, kw_only=True)
class AgenticOperationSourceRef:
    source_ref_id: str
    source_kind: AgenticOperationSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        AgenticOperationSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationPolicy:
    operation_policy_id: str
    version: str
    allowed_modes: list[AgenticOperationMode | str]
    blocked_runtime_kinds: list[AgenticOperationRuntimeKind | str]
    required_safety_checks: list[AgenticOperationSafetyCheckKind | str]
    max_cycle_count: int
    max_step_count: int
    require_human_approval_contract: bool
    require_post_apply_validation_success: bool
    require_human_handoff_after_cycle: bool
    allow_bounded_function_task: bool
    allow_single_cycle_operation: bool
    allow_metadata_only_operation: bool
    allow_automatic_retry: bool = False
    allow_automatic_repair: bool = False
    allow_multi_cycle_loop: bool = False
    allow_recursive_self_invocation: bool = False
    allow_independent_agent_runtime: bool = False
    allow_external_agent_orchestration: bool = False
    allow_dominion_runtime: bool = False
    allow_model_invocation: bool = False
    allow_general_tool_execution: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("operation_policy_id", self.operation_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, AgenticOperationMode)
        _validate_enum_list("blocked_runtime_kinds", self.blocked_runtime_kinds, AgenticOperationRuntimeKind)
        _validate_enum_list("required_safety_checks", self.required_safety_checks, AgenticOperationSafetyCheckKind)
        if self.max_cycle_count != 1:
            raise ValueError("max_cycle_count must be exactly 1 in v0.36.6")
        if self.max_step_count < 1:
            raise ValueError("max_step_count must be >= 1")
        if self.require_human_handoff_after_cycle is not True:
            raise ValueError("human handoff after cycle is mandatory")
        _validate_false(
            self,
            (
                "allow_automatic_retry",
                "allow_automatic_repair",
                "allow_multi_cycle_loop",
                "allow_recursive_self_invocation",
                "allow_independent_agent_runtime",
                "allow_external_agent_orchestration",
                "allow_dominion_runtime",
                "allow_model_invocation",
                "allow_general_tool_execution",
                "allow_live_workspace_write",
                "allow_patch_application",
                "allow_test_execution",
                "allow_shell",
                "allow_dependency_install",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationInput:
    operation_input_id: str
    version: str
    requested_mode: AgenticOperationMode | str
    task_summary: str
    operator_task_ref: str | None
    post_apply_validation_report_id: str | None
    sandbox_apply_result_id: str | None
    dry_run_result_id: str | None
    apply_candidate_id: str | None
    human_approval_contract_id: str | None
    source_refs: list[AgenticOperationSourceRef]
    prohibited_runtime_actions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("operation_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        AgenticOperationMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_RUNTIME_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing {missing}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationIntent:
    operation_intent_id: str
    version: str
    task_summary: str
    expected_outcome: str
    non_goals: list[str]
    runtime_kind: AgenticOperationRuntimeKind | str
    single_cycle_only: bool
    human_handoff_required: bool
    automatic_retry_allowed: bool = False
    automatic_repair_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("operation_intent_id", "task_summary", "expected_outcome"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("non_goals", self.non_goals)
        runtime_kind = AgenticOperationRuntimeKind(self.runtime_kind)
        if runtime_kind not in {
            AgenticOperationRuntimeKind.BOUNDED_FUNCTION_TASK,
            AgenticOperationRuntimeKind.SINGLE_CYCLE_OPERATION,
            AgenticOperationRuntimeKind.METADATA_ONLY_OPERATION,
        }:
            raise ValueError("intent runtime kind must be bounded/metadata-only")
        if self.single_cycle_only is not True:
            raise ValueError("intent must be single-cycle only")
        if self.human_handoff_required is not True:
            raise ValueError("intent must require human handoff")
        _validate_false(self, ("automatic_retry_allowed", "automatic_repair_allowed"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationStageArtifactRef:
    stage_artifact_ref_id: str
    stage_name: str
    artifact_id: str | None
    artifact_summary: str
    required: bool
    present: bool
    valid_for_cycle: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("stage_artifact_ref_id", "stage_name", "artifact_summary"):
            _require_non_blank(name, getattr(self, name))
        if self.required and not self.present:
            object.__setattr__(self, "valid_for_cycle", False)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationStepRecord:
    step_record_id: str
    step_kind: AgenticOperationStepKind | str
    step_status: AgenticOperationStepStatus | str
    step_index: int
    step_summary: str
    source_artifact_refs: list[AgenticOperationStageArtifactRef]
    risk_kinds: list[AgenticOperationRiskKind | str]
    blocked: bool
    block_reason: str | None
    executed_external_tool: bool = False
    executed_shell: bool = False
    executed_test: bool = False
    wrote_live_workspace: bool = False
    performed_repair: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("step_record_id", "step_summary"):
            _require_non_blank(name, getattr(self, name))
        AgenticOperationStepKind(self.step_kind)
        AgenticOperationStepStatus(self.step_status)
        if self.step_index < 0:
            raise ValueError("step_index must be >= 0")
        _validate_list("source_artifact_refs", self.source_artifact_refs)
        _validate_enum_list("risk_kinds", self.risk_kinds, AgenticOperationRiskKind)
        if self.blocked and not self.block_reason:
            raise ValueError("blocked step must include block_reason")
        _validate_false(
            self,
            ("executed_external_tool", "executed_shell", "executed_test", "wrote_live_workspace", "performed_repair"),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationStepSequence:
    step_sequence_id: str
    version: str
    step_records: list[AgenticOperationStepRecord]
    max_step_count: int
    actual_step_count: int
    sequence_summary: str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("step_sequence_id", self.step_sequence_id)
        _require_non_blank("sequence_summary", self.sequence_summary)
        _validate_version(self.version)
        _validate_list("step_records", self.step_records)
        if self.max_step_count < 1:
            raise ValueError("max_step_count must be >= 1")
        if self.actual_step_count < 0 or self.actual_step_count > self.max_step_count:
            raise ValueError("actual_step_count must be >= 0 and <= max_step_count")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationSafetyFinding:
    safety_finding_id: str
    check_kind: AgenticOperationSafetyCheckKind | str
    severity: str
    finding_summary: str
    evidence_preview: str
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_finding_id", "severity", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        AgenticOperationSafetyCheckKind(self.check_kind)
        if _bounded_preview(self.evidence_preview) != self.evidence_preview:
            raise ValueError("evidence_preview must be bounded and redacted")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationSafetyReport:
    safety_report_id: str
    version: str
    safety_findings: list[AgenticOperationSafetyFinding]
    required_checks: list[AgenticOperationSafetyCheckKind | str]
    passed_checks: list[AgenticOperationSafetyCheckKind | str]
    failed_checks: list[AgenticOperationSafetyCheckKind | str]
    blocked: bool
    requires_review: bool
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safety_report_id", self.safety_report_id)
        _require_non_blank("summary", self.summary)
        _validate_version(self.version)
        _validate_list("safety_findings", self.safety_findings)
        _validate_enum_list("required_checks", self.required_checks, AgenticOperationSafetyCheckKind)
        _validate_enum_list("passed_checks", self.passed_checks, AgenticOperationSafetyCheckKind)
        _validate_enum_list("failed_checks", self.failed_checks, AgenticOperationSafetyCheckKind)
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationStopReason:
    stop_reason_id: str
    stop_reason_kind: AgenticOperationStopReasonKind | str
    stop_summary: str
    human_handoff_required: bool
    allows_continuation: bool = False
    allows_retry: bool = False
    allows_repair: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("stop_reason_id", "stop_summary"):
            _require_non_blank(name, getattr(self, name))
        AgenticOperationStopReasonKind(self.stop_reason_kind)
        if self.human_handoff_required is not True:
            raise ValueError("stop reason must require human handoff")
        _validate_false(self, ("allows_continuation", "allows_retry", "allows_repair"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationResult:
    operation_result_id: str
    version: str
    operation_input_id: str
    status: AgenticOperationStatus | str
    readiness_level: AgenticOperationReadinessLevel | str
    step_sequence: AgenticOperationStepSequence
    safety_report: AgenticOperationSafetyReport
    stop_reason: AgenticOperationStopReason
    result_summary: str
    completed_single_cycle: bool
    completed_successfully: bool
    human_handoff_required: bool
    ready_for_v0367_patch_apply_sandbox_ocel_trace_packet: bool
    ready_for_v0368_cli_sandbox_apply_agentic_surface: bool
    ready_for_future_trace_input: bool
    production_certified: bool = False
    ready_for_execution: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("operation_result_id", "operation_input_id", "result_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        AgenticOperationStatus(self.status)
        AgenticOperationReadinessLevel(self.readiness_level)
        if self.human_handoff_required is not True:
            raise ValueError("operation result must require human handoff")
        _validate_false(
            self,
            (
                "production_certified",
                "ready_for_execution",
                "ready_for_independent_agent_runtime",
                "ready_for_multi_cycle_agentic_loop",
                "ready_for_live_workspace_write",
                "ready_for_patch_application",
                "ready_for_test_execution",
                "ready_for_shell_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationRunPacket:
    run_packet_id: str
    version: str
    operation_intent: AgenticOperationIntent
    operation_input: AgenticOperationInput
    operation_policy: AgenticOperationPolicy
    stage_artifact_refs: list[AgenticOperationStageArtifactRef]
    result: AgenticOperationResult
    source_refs: list[AgenticOperationSourceRef]
    max_cycle_count: int
    cycle_count: int
    automatic_retry_allowed: bool
    automatic_repair_allowed: bool
    human_handoff_required: bool
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_packet_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("stage_artifact_refs", self.stage_artifact_refs)
        _validate_list("source_refs", self.source_refs)
        if self.max_cycle_count != 1:
            raise ValueError("run packet max_cycle_count must be exactly 1")
        if self.cycle_count not in (0, 1):
            raise ValueError("cycle_count must be 0 or 1")
        if self.human_handoff_required is not True:
            raise ValueError("run packet must require human handoff")
        _validate_false(self, ("automatic_retry_allowed", "automatic_repair_allowed", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationDecision:
    decision_id: str
    decision_kind: AgenticOperationDecisionKind | str
    status: AgenticOperationStatus | str
    summary: str
    allow_bounded_single_cycle_packet: bool
    allow_future_trace_input: bool
    allow_autonomous_runtime: bool = False
    allow_multi_cycle_loop: bool = False
    allow_automatic_retry: bool = False
    allow_automatic_repair: bool = False
    allow_shell: bool = False
    allow_test_execution: bool = False
    allow_live_workspace_write: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        AgenticOperationDecisionKind(self.decision_kind)
        AgenticOperationStatus(self.status)
        _validate_false(
            self,
            (
                "allow_autonomous_runtime",
                "allow_multi_cycle_loop",
                "allow_automatic_retry",
                "allow_automatic_repair",
                "allow_shell",
                "allow_test_execution",
                "allow_live_workspace_write",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationValidationFinding:
    validation_finding_id: str
    risk_kind: AgenticOperationRiskKind | str
    decision_kind: AgenticOperationDecisionKind | str
    summary: str
    blocks_operation_success: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_finding_id", self.validation_finding_id)
        _require_non_blank("summary", self.summary)
        AgenticOperationRiskKind(self.risk_kind)
        AgenticOperationDecisionKind(self.decision_kind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationValidationReport:
    validation_report_id: str
    version: str
    findings: list[AgenticOperationValidationFinding]
    summary: str
    confirms_single_cycle_limit: bool
    confirms_stop_reason_present: bool
    confirms_human_handoff_required: bool
    confirms_no_automatic_retry: bool
    confirms_no_automatic_repair: bool
    validation_successful: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _require_non_blank("summary", self.summary)
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        for name in (
            "confirms_single_cycle_limit",
            "confirms_stop_reason_present",
            "confirms_human_handoff_required",
            "confirms_no_automatic_retry",
            "confirms_no_automatic_repair",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.6")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationReport:
    report_id: str
    operation_result: AgenticOperationResult
    validation_report: AgenticOperationValidationReport
    decision: AgenticOperationDecision
    summary: str
    bounded_task_cycle_complete: bool
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("production_certified",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationRunPreview:
    run_preview_id: str
    operation_input_id: str
    preview_summary: str
    planned_metadata_actions: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_bounded_agentic_task_operation_cycle: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "operation_input_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("planned_metadata_actions", self.planned_metadata_actions)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class AgenticOperationNoAutonomyGuarantee:
    guarantee_id: str
    version: str
    no_independent_autonomous_agent_runtime: bool
    no_multi_cycle_agentic_loop: bool
    no_recursive_self_invocation: bool
    no_automatic_retry: bool
    no_automatic_repair: bool
    no_model_invocation: bool
    no_tool_execution: bool
    no_live_workspace_write: bool
    no_patch_application: bool
    no_shell_execution: bool
    no_test_execution: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_authority_grant: bool
    mandatory_human_handoff_after_cycle: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in (
            "no_independent_autonomous_agent_runtime",
            "no_multi_cycle_agentic_loop",
            "no_recursive_self_invocation",
            "no_automatic_retry",
            "no_automatic_repair",
            "no_model_invocation",
            "no_tool_execution",
            "no_live_workspace_write",
            "no_patch_application",
            "no_shell_execution",
            "no_test_execution",
            "no_external_agent_execution",
            "no_dominion_runtime",
            "no_authority_grant",
            "mandatory_human_handoff_after_cycle",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.6")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0366ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    status: AgenticOperationStatus | str
    readiness_level: AgenticOperationReadinessLevel | str
    ready_for_v0367_patch_apply_sandbox_ocel_trace_packet: bool
    ready_for_v0368_cli_sandbox_apply_agentic_surface: bool
    ready_for_bounded_agentic_task_operation_cycle: bool
    ready_for_agentic_function_task_execution: bool
    ready_for_single_cycle_operation_packet: bool
    ready_for_agentic_step_recording: bool
    ready_for_agentic_operation_safety_report: bool
    ready_for_human_handoff_after_cycle: bool
    ready_for_future_trace_input: bool
    digestion_first_policy_applied: bool
    dominion_runtime_blocked: bool
    external_agent_execution_blocked: bool
    infinite_agent_loop_blocked: bool
    recursive_self_invocation_blocked: bool
    automatic_repair_loop_blocked: bool
    bounded_agentic_task_only: bool
    no_independent_autonomous_agent_runtime: bool
    mandatory_human_handoff_after_cycle: bool
    ready_for_execution: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_recursive_self_invocation: bool = False
    ready_for_automatic_retry: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_sandbox_repair: bool = False
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
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _require_non_blank("release_name", self.release_name)
        _validate_version(self.version)
        AgenticOperationStatus(self.status)
        AgenticOperationReadinessLevel(self.readiness_level)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_agentic_operation_flags(**kwargs: Any) -> AgenticOperationFlagSet:
    return AgenticOperationFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "agentic_operation_flags:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        agentic_operation_cycle_constructed=kwargs.pop("agentic_operation_cycle_constructed", True),
        bounded_function_task_policy_defined=kwargs.pop("bounded_function_task_policy_defined", True),
        single_cycle_operation_packet_available=kwargs.pop("single_cycle_operation_packet_available", True),
        agentic_step_recording_available=kwargs.pop("agentic_step_recording_available", True),
        agentic_safety_report_available=kwargs.pop("agentic_safety_report_available", True),
        human_handoff_after_cycle_available=kwargs.pop("human_handoff_after_cycle_available", True),
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=kwargs.pop("ready_for_v0367_patch_apply_sandbox_ocel_trace_packet", True),
        ready_for_v0368_cli_sandbox_apply_agentic_surface=kwargs.pop("ready_for_v0368_cli_sandbox_apply_agentic_surface", True),
        ready_for_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_bounded_agentic_task_operation_cycle", True),
        ready_for_agentic_function_task_execution=kwargs.pop("ready_for_agentic_function_task_execution", True),
        ready_for_single_cycle_operation_packet=kwargs.pop("ready_for_single_cycle_operation_packet", True),
        ready_for_agentic_step_recording=kwargs.pop("ready_for_agentic_step_recording", True),
        ready_for_agentic_operation_safety_report=kwargs.pop("ready_for_agentic_operation_safety_report", True),
        ready_for_human_handoff_after_cycle=kwargs.pop("ready_for_human_handoff_after_cycle", True),
        ready_for_future_trace_input=kwargs.pop("ready_for_future_trace_input", True),
        **kwargs,
    )


def build_agentic_operation_source_ref(**kwargs: Any) -> AgenticOperationSourceRef:
    return AgenticOperationSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "agentic_operation_source_ref:v0.36.6"),
        source_kind=kwargs.pop("source_kind", AgenticOperationSourceKind.TEST_FIXTURE),
        source_id=kwargs.pop("source_id", "source:v0.36.6"),
        source_summary=kwargs.pop("source_summary", "agentic operation source metadata; not execution"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        **kwargs,
    )


def build_agentic_operation_policy(**kwargs: Any) -> AgenticOperationPolicy:
    return AgenticOperationPolicy(
        operation_policy_id=kwargs.pop("operation_policy_id", "agentic_operation_policy:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        allowed_modes=kwargs.pop(
            "allowed_modes",
            [
                AgenticOperationMode.METADATA_ONLY_CYCLE,
                AgenticOperationMode.SUPPLIED_ARTIFACT_CYCLE,
                AgenticOperationMode.BOUNDED_FUNCTION_TASK_CYCLE,
                AgenticOperationMode.SANDBOX_APPLY_VALIDATION_CYCLE,
                AgenticOperationMode.HUMAN_HANDOFF_CYCLE,
            ],
        ),
        blocked_runtime_kinds=kwargs.pop(
            "blocked_runtime_kinds",
            [
                AgenticOperationRuntimeKind.INDEPENDENT_AUTONOMOUS_AGENT,
                AgenticOperationRuntimeKind.MULTI_CYCLE_AGENTIC_LOOP,
                AgenticOperationRuntimeKind.RECURSIVE_SELF_INVOCATION,
                AgenticOperationRuntimeKind.EXTERNAL_AGENT_ORCHESTRATION,
                AgenticOperationRuntimeKind.DOMINION_RUNTIME,
                AgenticOperationRuntimeKind.GENERAL_TOOL_RUNTIME,
            ],
        ),
        required_safety_checks=kwargs.pop(
            "required_safety_checks",
            [
                AgenticOperationSafetyCheckKind.NO_MULTI_CYCLE_LOOP_CHECK,
                AgenticOperationSafetyCheckKind.NO_AUTOMATIC_RETRY_CHECK,
                AgenticOperationSafetyCheckKind.NO_AUTOMATIC_REPAIR_CHECK,
                AgenticOperationSafetyCheckKind.NO_RECURSIVE_SELF_INVOCATION_CHECK,
                AgenticOperationSafetyCheckKind.NO_INDEPENDENT_AGENT_RUNTIME_CHECK,
                AgenticOperationSafetyCheckKind.NO_EXTERNAL_AGENT_EXECUTION_CHECK,
                AgenticOperationSafetyCheckKind.NO_DOMINION_RUNTIME_CHECK,
                AgenticOperationSafetyCheckKind.POST_APPLY_VALIDATION_SUCCESS_CHECK,
                AgenticOperationSafetyCheckKind.HUMAN_HANDOFF_REQUIRED_CHECK,
            ],
        ),
        max_cycle_count=kwargs.pop("max_cycle_count", 1),
        max_step_count=kwargs.pop("max_step_count", 12),
        require_human_approval_contract=kwargs.pop("require_human_approval_contract", True),
        require_post_apply_validation_success=kwargs.pop("require_post_apply_validation_success", True),
        require_human_handoff_after_cycle=kwargs.pop("require_human_handoff_after_cycle", True),
        allow_bounded_function_task=kwargs.pop("allow_bounded_function_task", True),
        allow_single_cycle_operation=kwargs.pop("allow_single_cycle_operation", True),
        allow_metadata_only_operation=kwargs.pop("allow_metadata_only_operation", True),
        **kwargs,
    )


def default_agentic_operation_policy(**kwargs: Any) -> AgenticOperationPolicy:
    return build_agentic_operation_policy(**kwargs)


def build_agentic_operation_input(**kwargs: Any) -> AgenticOperationInput:
    return AgenticOperationInput(
        operation_input_id=kwargs.pop("operation_input_id", "agentic_operation_input:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        requested_mode=kwargs.pop("requested_mode", AgenticOperationMode.SANDBOX_APPLY_VALIDATION_CYCLE),
        task_summary=kwargs.pop("task_summary", "bounded single-cycle operation request; not autonomous runtime"),
        operator_task_ref=kwargs.pop("operator_task_ref", None),
        post_apply_validation_report_id=kwargs.pop("post_apply_validation_report_id", None),
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", None),
        dry_run_result_id=kwargs.pop("dry_run_result_id", None),
        apply_candidate_id=kwargs.pop("apply_candidate_id", None),
        human_approval_contract_id=kwargs.pop("human_approval_contract_id", None),
        source_refs=kwargs.pop("source_refs", [build_agentic_operation_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        **kwargs,
    )


def build_agentic_operation_intent(**kwargs: Any) -> AgenticOperationIntent:
    return AgenticOperationIntent(
        operation_intent_id=kwargs.pop("operation_intent_id", "agentic_operation_intent:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        task_summary=kwargs.pop("task_summary", "bounded agentic function/task operation"),
        expected_outcome=kwargs.pop("expected_outcome", "single-cycle metadata packet with mandatory human handoff"),
        non_goals=kwargs.pop(
            "non_goals",
            [
                "independent autonomous agent runtime",
                "multi-cycle loop",
                "automatic retry",
                "automatic repair",
                "model/tool execution",
                "live workspace write",
            ],
        ),
        runtime_kind=kwargs.pop("runtime_kind", AgenticOperationRuntimeKind.BOUNDED_FUNCTION_TASK),
        single_cycle_only=kwargs.pop("single_cycle_only", True),
        human_handoff_required=kwargs.pop("human_handoff_required", True),
        **kwargs,
    )


def build_agentic_operation_stage_artifact_ref(**kwargs: Any) -> AgenticOperationStageArtifactRef:
    return AgenticOperationStageArtifactRef(
        stage_artifact_ref_id=kwargs.pop("stage_artifact_ref_id", "agentic_stage_artifact_ref:v0.36.6"),
        stage_name=kwargs.pop("stage_name", "post_apply_validation"),
        artifact_id=kwargs.pop("artifact_id", "artifact:v0.36"),
        artifact_summary=kwargs.pop("artifact_summary", "supplied stage artifact metadata"),
        required=kwargs.pop("required", True),
        present=kwargs.pop("present", True),
        valid_for_cycle=kwargs.pop("valid_for_cycle", True),
        **kwargs,
    )


def build_agentic_operation_step_record(**kwargs: Any) -> AgenticOperationStepRecord:
    return AgenticOperationStepRecord(
        step_record_id=kwargs.pop("step_record_id", "agentic_step_record:v0.36.6"),
        step_kind=kwargs.pop("step_kind", AgenticOperationStepKind.VALIDATE_OPERATION_INPUT),
        step_status=kwargs.pop("step_status", AgenticOperationStepStatus.COMPLETED),
        step_index=kwargs.pop("step_index", 0),
        step_summary=kwargs.pop("step_summary", "bounded metadata step record; no tool execution"),
        source_artifact_refs=kwargs.pop("source_artifact_refs", []),
        risk_kinds=kwargs.pop("risk_kinds", []),
        blocked=kwargs.pop("blocked", False),
        block_reason=kwargs.pop("block_reason", None),
        **kwargs,
    )


def build_agentic_operation_step_sequence(**kwargs: Any) -> AgenticOperationStepSequence:
    step_records = kwargs.pop("step_records", [build_agentic_operation_step_record()])
    return AgenticOperationStepSequence(
        step_sequence_id=kwargs.pop("step_sequence_id", "agentic_step_sequence:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        step_records=step_records,
        max_step_count=kwargs.pop("max_step_count", 12),
        actual_step_count=kwargs.pop("actual_step_count", len(step_records)),
        sequence_summary=kwargs.pop("sequence_summary", "single-cycle step sequence metadata"),
        blocked=kwargs.pop("blocked", any(step.blocked for step in step_records)),
        **kwargs,
    )


def build_agentic_operation_safety_finding(**kwargs: Any) -> AgenticOperationSafetyFinding:
    return AgenticOperationSafetyFinding(
        safety_finding_id=kwargs.pop("safety_finding_id", "agentic_safety_finding:v0.36.6"),
        check_kind=kwargs.pop("check_kind", AgenticOperationSafetyCheckKind.NO_MULTI_CYCLE_LOOP_CHECK),
        severity=kwargs.pop("severity", "blocked"),
        finding_summary=kwargs.pop("finding_summary", "bounded operation safety finding"),
        evidence_preview=kwargs.pop("evidence_preview", ""),
        blocked=kwargs.pop("blocked", True),
        requires_review=kwargs.pop("requires_review", True),
        **kwargs,
    )


def build_agentic_operation_safety_report(**kwargs: Any) -> AgenticOperationSafetyReport:
    findings = kwargs.pop("safety_findings", [])
    required = kwargs.pop("required_checks", build_agentic_operation_policy().required_safety_checks)
    failed = kwargs.pop("failed_checks", [])
    passed = kwargs.pop("passed_checks", [check for check in required if check not in failed])
    return AgenticOperationSafetyReport(
        safety_report_id=kwargs.pop("safety_report_id", "agentic_safety_report:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        safety_findings=findings,
        required_checks=required,
        passed_checks=passed,
        failed_checks=failed,
        blocked=kwargs.pop("blocked", any(finding.blocked for finding in findings)),
        requires_review=kwargs.pop("requires_review", any(finding.requires_review for finding in findings)),
        summary=kwargs.pop("summary", "bounded operation safety report; not execution readiness"),
        **kwargs,
    )


def build_agentic_operation_stop_reason(**kwargs: Any) -> AgenticOperationStopReason:
    return AgenticOperationStopReason(
        stop_reason_id=kwargs.pop("stop_reason_id", "agentic_stop_reason:v0.36.6"),
        stop_reason_kind=kwargs.pop("stop_reason_kind", AgenticOperationStopReasonKind.COMPLETED_SINGLE_CYCLE),
        stop_summary=kwargs.pop("stop_summary", "single cycle stopped for mandatory human handoff"),
        human_handoff_required=kwargs.pop("human_handoff_required", True),
        **kwargs,
    )


def build_agentic_operation_result(**kwargs: Any) -> AgenticOperationResult:
    step_sequence = kwargs.pop("step_sequence", build_agentic_operation_step_sequence())
    safety_report = kwargs.pop("safety_report", build_agentic_operation_safety_report())
    stop_reason = kwargs.pop("stop_reason", build_agentic_operation_stop_reason())
    successful = kwargs.pop("completed_successfully", not step_sequence.blocked and not safety_report.blocked)
    return AgenticOperationResult(
        operation_result_id=kwargs.pop("operation_result_id", "agentic_operation_result:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        operation_input_id=kwargs.pop("operation_input_id", "agentic_operation_input:v0.36.6"),
        status=kwargs.pop("status", AgenticOperationStatus.CYCLE_COMPLETED if successful else AgenticOperationStatus.REVIEW_REQUIRED),
        readiness_level=kwargs.pop(
            "readiness_level",
            AgenticOperationReadinessLevel.HUMAN_HANDOFF_READY if successful else AgenticOperationReadinessLevel.BLOCKED,
        ),
        step_sequence=step_sequence,
        safety_report=safety_report,
        stop_reason=stop_reason,
        result_summary=kwargs.pop("result_summary", "bounded single-cycle operation result; not production certification"),
        completed_single_cycle=kwargs.pop("completed_single_cycle", True),
        completed_successfully=successful,
        human_handoff_required=kwargs.pop("human_handoff_required", True),
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=kwargs.pop("ready_for_v0367_patch_apply_sandbox_ocel_trace_packet", successful),
        ready_for_v0368_cli_sandbox_apply_agentic_surface=kwargs.pop("ready_for_v0368_cli_sandbox_apply_agentic_surface", successful),
        ready_for_future_trace_input=kwargs.pop("ready_for_future_trace_input", successful),
        **kwargs,
    )


def build_agentic_operation_run_packet(**kwargs: Any) -> AgenticOperationRunPacket:
    intent = kwargs.pop("operation_intent", build_agentic_operation_intent())
    operation_input = kwargs.pop("operation_input", build_agentic_operation_input())
    policy = kwargs.pop("operation_policy", build_agentic_operation_policy())
    result = kwargs.pop("result", build_agentic_operation_result(operation_input_id=operation_input.operation_input_id))
    return AgenticOperationRunPacket(
        run_packet_id=kwargs.pop("run_packet_id", "agentic_run_packet:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        operation_intent=intent,
        operation_input=operation_input,
        operation_policy=policy,
        stage_artifact_refs=kwargs.pop("stage_artifact_refs", []),
        result=result,
        source_refs=kwargs.pop("source_refs", operation_input.source_refs),
        max_cycle_count=kwargs.pop("max_cycle_count", 1),
        cycle_count=kwargs.pop("cycle_count", 1),
        automatic_retry_allowed=kwargs.pop("automatic_retry_allowed", False),
        automatic_repair_allowed=kwargs.pop("automatic_repair_allowed", False),
        human_handoff_required=kwargs.pop("human_handoff_required", True),
        summary=kwargs.pop("summary", "bounded single-cycle operation packet; not self-directed control loop"),
        **kwargs,
    )


def build_agentic_operation_decision(**kwargs: Any) -> AgenticOperationDecision:
    return AgenticOperationDecision(
        decision_id=kwargs.pop("decision_id", "agentic_operation_decision:v0.36.6"),
        decision_kind=kwargs.pop("decision_kind", AgenticOperationDecisionKind.ALLOW_FUTURE_TRACE_INPUT),
        status=kwargs.pop("status", AgenticOperationStatus.CYCLE_COMPLETED),
        summary=kwargs.pop("summary", "bounded single-cycle packet and future trace input allowed only"),
        allow_bounded_single_cycle_packet=kwargs.pop("allow_bounded_single_cycle_packet", True),
        allow_future_trace_input=kwargs.pop("allow_future_trace_input", True),
        **kwargs,
    )


def build_agentic_operation_validation_finding(**kwargs: Any) -> AgenticOperationValidationFinding:
    return AgenticOperationValidationFinding(
        validation_finding_id=kwargs.pop("validation_finding_id", "agentic_validation_finding:v0.36.6"),
        risk_kind=kwargs.pop("risk_kind", AgenticOperationRiskKind.MISSING_STAGE_ARTIFACT_RISK),
        decision_kind=kwargs.pop("decision_kind", AgenticOperationDecisionKind.REQUIRE_REVIEW),
        summary=kwargs.pop("summary", "agentic operation validation finding"),
        blocks_operation_success=kwargs.pop("blocks_operation_success", True),
        **kwargs,
    )


def build_agentic_operation_validation_report(**kwargs: Any) -> AgenticOperationValidationReport:
    findings = kwargs.pop("findings", [])
    return AgenticOperationValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "agentic_validation_report:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        findings=findings,
        summary=kwargs.pop("summary", "validated single-cycle stop reason and human handoff"),
        confirms_single_cycle_limit=kwargs.pop("confirms_single_cycle_limit", True),
        confirms_stop_reason_present=kwargs.pop("confirms_stop_reason_present", True),
        confirms_human_handoff_required=kwargs.pop("confirms_human_handoff_required", True),
        confirms_no_automatic_retry=kwargs.pop("confirms_no_automatic_retry", True),
        confirms_no_automatic_repair=kwargs.pop("confirms_no_automatic_repair", True),
        validation_successful=kwargs.pop("validation_successful", not findings),
        **kwargs,
    )


def build_agentic_operation_report(**kwargs: Any) -> AgenticOperationReport:
    result = kwargs.pop("operation_result", build_agentic_operation_result())
    return AgenticOperationReport(
        report_id=kwargs.pop("report_id", "agentic_operation_report:v0.36.6"),
        operation_result=result,
        validation_report=kwargs.pop("validation_report", build_agentic_operation_validation_report()),
        decision=kwargs.pop("decision", build_agentic_operation_decision()),
        summary=kwargs.pop("summary", "bounded agentic operation report; not production certification"),
        bounded_task_cycle_complete=kwargs.pop("bounded_task_cycle_complete", result.completed_single_cycle),
        **kwargs,
    )


def build_agentic_operation_run_preview(**kwargs: Any) -> AgenticOperationRunPreview:
    return AgenticOperationRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "agentic_operation_run_preview:v0.36.6"),
        operation_input_id=kwargs.pop("operation_input_id", "agentic_operation_input:v0.36.6"),
        preview_summary=kwargs.pop("preview_summary", "preview of one bounded metadata cycle"),
        planned_metadata_actions=kwargs.pop("planned_metadata_actions", ["validate stage artifacts", "record steps", "create stop reason", "handoff to human"]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        ready_for_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_bounded_agentic_task_operation_cycle", True),
        **kwargs,
    )


def build_agentic_operation_no_autonomy_guarantee(**kwargs: Any) -> AgenticOperationNoAutonomyGuarantee:
    return AgenticOperationNoAutonomyGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "agentic_no_autonomy_guarantee:v0.36.6"),
        version=kwargs.pop("version", V0366_VERSION),
        no_independent_autonomous_agent_runtime=kwargs.pop("no_independent_autonomous_agent_runtime", True),
        no_multi_cycle_agentic_loop=kwargs.pop("no_multi_cycle_agentic_loop", True),
        no_recursive_self_invocation=kwargs.pop("no_recursive_self_invocation", True),
        no_automatic_retry=kwargs.pop("no_automatic_retry", True),
        no_automatic_repair=kwargs.pop("no_automatic_repair", True),
        no_model_invocation=kwargs.pop("no_model_invocation", True),
        no_tool_execution=kwargs.pop("no_tool_execution", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_patch_application=kwargs.pop("no_patch_application", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        no_authority_grant=kwargs.pop("no_authority_grant", True),
        mandatory_human_handoff_after_cycle=kwargs.pop("mandatory_human_handoff_after_cycle", True),
        **kwargs,
    )


def build_v0366_readiness_report(**kwargs: Any) -> V0366ReadinessReport:
    return V0366ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0366_readiness_report"),
        version=kwargs.pop("version", V0366_VERSION),
        release_name=kwargs.pop("release_name", V0366_RELEASE_NAME),
        status=kwargs.pop("status", AgenticOperationStatus.CYCLE_COMPLETED),
        readiness_level=kwargs.pop("readiness_level", AgenticOperationReadinessLevel.HUMAN_HANDOFF_READY),
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=kwargs.pop("ready_for_v0367_patch_apply_sandbox_ocel_trace_packet", True),
        ready_for_v0368_cli_sandbox_apply_agentic_surface=kwargs.pop("ready_for_v0368_cli_sandbox_apply_agentic_surface", True),
        ready_for_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_bounded_agentic_task_operation_cycle", True),
        ready_for_agentic_function_task_execution=kwargs.pop("ready_for_agentic_function_task_execution", True),
        ready_for_single_cycle_operation_packet=kwargs.pop("ready_for_single_cycle_operation_packet", True),
        ready_for_agentic_step_recording=kwargs.pop("ready_for_agentic_step_recording", True),
        ready_for_agentic_operation_safety_report=kwargs.pop("ready_for_agentic_operation_safety_report", True),
        ready_for_human_handoff_after_cycle=kwargs.pop("ready_for_human_handoff_after_cycle", True),
        ready_for_future_trace_input=kwargs.pop("ready_for_future_trace_input", True),
        digestion_first_policy_applied=kwargs.pop("digestion_first_policy_applied", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_agent_loop_blocked=kwargs.pop("infinite_agent_loop_blocked", True),
        recursive_self_invocation_blocked=kwargs.pop("recursive_self_invocation_blocked", True),
        automatic_repair_loop_blocked=kwargs.pop("automatic_repair_loop_blocked", True),
        bounded_agentic_task_only=kwargs.pop("bounded_agentic_task_only", True),
        no_independent_autonomous_agent_runtime=kwargs.pop("no_independent_autonomous_agent_runtime", True),
        mandatory_human_handoff_after_cycle=kwargs.pop("mandatory_human_handoff_after_cycle", True),
        **kwargs,
    )


def build_agentic_operation_input_from_post_apply_validation(
    report: SandboxPostApplyValidationReport,
    **kwargs: Any,
) -> AgenticOperationInput:
    return build_agentic_operation_input(
        post_apply_validation_report_id=report.validation_report_id,
        sandbox_apply_result_id=report.sandbox_apply_result_id,
        source_refs=[
            build_agentic_operation_source_ref(
                source_kind=AgenticOperationSourceKind.V0365_POST_APPLY_VALIDATION_REPORT,
                source_id=report.validation_report_id,
                source_summary="v0.36.5 sandbox post-apply validation report metadata",
            )
        ],
        metadata={
            "validation_successful": report.validation_successful,
            "ready_for_future_agentic_task_operation_input": report.ready_for_future_agentic_task_operation_input,
        },
        **kwargs,
    )


def build_agentic_operation_stage_refs_from_v036_artifacts(**kwargs: Any) -> list[AgenticOperationStageArtifactRef]:
    artifact_specs = [
        ("apply_candidate", kwargs.get("apply_candidate_id"), True),
        ("human_approval_contract", kwargs.get("human_approval_contract_id"), True),
        ("dry_run_result", kwargs.get("dry_run_result_id"), True),
        ("sandbox_manifest", kwargs.get("sandbox_manifest_id"), True),
        ("sandbox_apply_result", kwargs.get("sandbox_apply_result_id"), True),
        ("post_apply_validation_report", kwargs.get("post_apply_validation_report_id"), True),
    ]
    refs: list[AgenticOperationStageArtifactRef] = []
    for index, (stage_name, artifact_id, required) in enumerate(artifact_specs, start=1):
        present = bool(artifact_id)
        refs.append(
            build_agentic_operation_stage_artifact_ref(
                stage_artifact_ref_id=f"agentic_stage_artifact_ref:v0.36.6:{index}",
                stage_name=stage_name,
                artifact_id=artifact_id,
                artifact_summary=f"{stage_name} artifact {'present' if present else 'missing'}",
                required=required,
                present=present,
                valid_for_cycle=present,
            )
        )
    return refs


def build_agentic_step_sequence_from_stage_refs(
    stage_artifact_refs: list[AgenticOperationStageArtifactRef],
    policy: AgenticOperationPolicy | None = None,
) -> AgenticOperationStepSequence:
    active_policy = policy or default_agentic_operation_policy()
    step_records: list[AgenticOperationStepRecord] = []
    for index, ref in enumerate(stage_artifact_refs, start=1):
        blocked = ref.required and (not ref.present or not ref.valid_for_cycle)
        risk_kinds = [AgenticOperationRiskKind.MISSING_STAGE_ARTIFACT_RISK] if blocked else []
        step_records.append(
            build_agentic_operation_step_record(
                step_record_id=f"agentic_step_record:v0.36.6:{index}",
                step_kind=AgenticOperationStepKind.VALIDATE_OPERATION_INPUT,
                step_status=AgenticOperationStepStatus.BLOCKED if blocked else AgenticOperationStepStatus.COMPLETED,
                step_index=index,
                step_summary=f"stage artifact {ref.stage_name} {'blocked' if blocked else 'accepted'} for single-cycle metadata packet",
                source_artifact_refs=[ref],
                risk_kinds=risk_kinds,
                blocked=blocked,
                block_reason="required stage artifact missing or invalid" if blocked else None,
            )
        )
    return build_agentic_operation_step_sequence(
        step_records=step_records,
        max_step_count=active_policy.max_step_count,
        actual_step_count=len(step_records),
    )


def build_agentic_safety_report_from_stage_refs(
    stage_artifact_refs: list[AgenticOperationStageArtifactRef],
    post_apply_validation_successful: bool = True,
    policy: AgenticOperationPolicy | None = None,
    extra_findings: list[AgenticOperationSafetyFinding] | None = None,
) -> AgenticOperationSafetyReport:
    active_policy = policy or default_agentic_operation_policy()
    findings = list(extra_findings or [])
    if any(ref.required and (not ref.present or not ref.valid_for_cycle) for ref in stage_artifact_refs):
        findings.append(
            build_agentic_operation_safety_finding(
                safety_finding_id="agentic_safety_finding:v0.36.6:missing_artifact",
                check_kind=AgenticOperationSafetyCheckKind.POST_APPLY_VALIDATION_SUCCESS_CHECK,
                severity="blocked",
                finding_summary="required stage artifact missing or invalid",
                evidence_preview="missing required artifact",
                blocked=True,
                requires_review=True,
            )
        )
    if active_policy.require_post_apply_validation_success and not post_apply_validation_successful:
        findings.append(
            build_agentic_operation_safety_finding(
                safety_finding_id="agentic_safety_finding:v0.36.6:failed_validation",
                check_kind=AgenticOperationSafetyCheckKind.POST_APPLY_VALIDATION_SUCCESS_CHECK,
                severity="blocked",
                finding_summary="post-apply validation was not successful",
                evidence_preview="validation_successful=False",
                blocked=True,
                requires_review=True,
            )
        )
    failed_checks = [finding.check_kind for finding in findings]
    return build_agentic_operation_safety_report(
        safety_findings=findings,
        required_checks=active_policy.required_safety_checks,
        failed_checks=failed_checks,
        blocked=any(finding.blocked for finding in findings),
        requires_review=any(finding.requires_review for finding in findings),
    )


def decide_agentic_operation(
    step_sequence: AgenticOperationStepSequence,
    safety_report: AgenticOperationSafetyReport,
) -> AgenticOperationDecision:
    if step_sequence.blocked or safety_report.blocked:
        return build_agentic_operation_decision(
            decision_kind=AgenticOperationDecisionKind.REQUIRE_REVIEW,
            status=AgenticOperationStatus.REVIEW_REQUIRED,
            summary="bounded cycle requires review because stage or safety checks blocked",
            allow_bounded_single_cycle_packet=False,
            allow_future_trace_input=False,
        )
    return build_agentic_operation_decision()


def run_bounded_agentic_operation_cycle(
    operation_input: AgenticOperationInput,
    stage_artifact_refs: list[AgenticOperationStageArtifactRef],
    post_apply_validation_report: SandboxPostApplyValidationReport | None = None,
    policy: AgenticOperationPolicy | None = None,
    safety_findings: list[AgenticOperationSafetyFinding] | None = None,
) -> AgenticOperationRunPacket:
    active_policy = policy or default_agentic_operation_policy()
    intent = build_agentic_operation_intent(task_summary=operation_input.task_summary)
    step_sequence = build_agentic_step_sequence_from_stage_refs(stage_artifact_refs, active_policy)
    validation_successful = True
    if post_apply_validation_report is not None:
        validation_successful = post_apply_validation_report.validation_successful
    safety_report = build_agentic_safety_report_from_stage_refs(
        stage_artifact_refs,
        post_apply_validation_successful=validation_successful,
        policy=active_policy,
        extra_findings=safety_findings,
    )
    decision = decide_agentic_operation(step_sequence, safety_report)
    successful = decision.status == AgenticOperationStatus.CYCLE_COMPLETED
    missing_required_artifact = any(ref.required and (not ref.present or not ref.valid_for_cycle) for ref in stage_artifact_refs)
    if successful:
        stop_reason = build_agentic_operation_stop_reason()
        status = AgenticOperationStatus.CYCLE_COMPLETED
        readiness = AgenticOperationReadinessLevel.HUMAN_HANDOFF_READY
    elif missing_required_artifact:
        stop_reason = build_agentic_operation_stop_reason(
            stop_reason_kind=AgenticOperationStopReasonKind.BLOCKED_BY_MISSING_ARTIFACT,
            stop_summary="single cycle stopped because required artifact was missing",
        )
        status = AgenticOperationStatus.BLOCKED
        readiness = AgenticOperationReadinessLevel.BLOCKED
    else:
        stop_reason_kind = (
            AgenticOperationStopReasonKind.BLOCKED_BY_FAILED_VALIDATION
            if not validation_successful
            else AgenticOperationStopReasonKind.BLOCKED_BY_SAFETY_REPORT
        )
        stop_reason = build_agentic_operation_stop_reason(
            stop_reason_kind=stop_reason_kind,
            stop_summary="single cycle stopped before continuation; human handoff required",
        )
        status = AgenticOperationStatus.REVIEW_REQUIRED
        readiness = AgenticOperationReadinessLevel.BLOCKED
    result = build_agentic_operation_result(
        operation_input_id=operation_input.operation_input_id,
        status=status,
        readiness_level=readiness,
        step_sequence=step_sequence,
        safety_report=safety_report,
        stop_reason=stop_reason,
        completed_successfully=successful,
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=successful,
        ready_for_v0368_cli_sandbox_apply_agentic_surface=successful,
        ready_for_future_trace_input=successful,
    )
    return build_agentic_operation_run_packet(
        operation_intent=intent,
        operation_input=operation_input,
        operation_policy=active_policy,
        stage_artifact_refs=stage_artifact_refs,
        result=result,
        source_refs=operation_input.source_refs,
    )


def validate_agentic_operation_run_packet(packet: AgenticOperationRunPacket) -> AgenticOperationValidationReport:
    findings: list[AgenticOperationValidationFinding] = []
    if packet.max_cycle_count != 1 or packet.cycle_count not in (0, 1):
        findings.append(
            build_agentic_operation_validation_finding(
                risk_kind=AgenticOperationRiskKind.MULTI_CYCLE_LOOP_RISK,
                summary="run packet violates single-cycle limit",
            )
        )
    if packet.automatic_retry_allowed or packet.automatic_repair_allowed:
        findings.append(
            build_agentic_operation_validation_finding(
                risk_kind=AgenticOperationRiskKind.AUTOMATIC_RETRY_RISK,
                summary="run packet allowed retry or repair",
            )
        )
    if not packet.human_handoff_required or not packet.result.stop_reason:
        findings.append(
            build_agentic_operation_validation_finding(
                risk_kind=AgenticOperationRiskKind.AUTONOMOUS_AGENT_RUNTIME_RISK,
                summary="run packet lacks mandatory stop reason or human handoff",
            )
        )
    return build_agentic_operation_validation_report(findings=findings)


def agentic_operation_flags_preserve_no_autonomy(flags: AgenticOperationFlagSet) -> bool:
    return isinstance(flags, AgenticOperationFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def agentic_operation_policy_blocks_autonomy(policy: AgenticOperationPolicy) -> bool:
    return not any(
        getattr(policy, name)
        for name in (
            "allow_automatic_retry",
            "allow_automatic_repair",
            "allow_multi_cycle_loop",
            "allow_recursive_self_invocation",
            "allow_independent_agent_runtime",
            "allow_external_agent_orchestration",
            "allow_dominion_runtime",
            "allow_model_invocation",
            "allow_general_tool_execution",
            "allow_live_workspace_write",
            "allow_patch_application",
            "allow_test_execution",
            "allow_shell",
            "allow_dependency_install",
        )
    ) and policy.max_cycle_count == 1


def agentic_operation_run_packet_is_single_cycle(packet: AgenticOperationRunPacket) -> bool:
    return (
        packet.max_cycle_count == 1
        and packet.cycle_count in (0, 1)
        and packet.automatic_retry_allowed is False
        and packet.automatic_repair_allowed is False
        and packet.human_handoff_required is True
        and packet.ready_for_execution is False
    )


def agentic_operation_result_is_not_production_certification(result: AgenticOperationResult) -> bool:
    return not any(
        getattr(result, name)
        for name in (
            "production_certified",
            "ready_for_execution",
            "ready_for_independent_agent_runtime",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_live_workspace_write",
            "ready_for_patch_application",
            "ready_for_test_execution",
            "ready_for_shell_execution",
        )
    )


def agentic_operation_stop_reason_prevents_continuation(stop_reason: AgenticOperationStopReason) -> bool:
    return (
        stop_reason.human_handoff_required is True
        and stop_reason.allows_continuation is False
        and stop_reason.allows_retry is False
        and stop_reason.allows_repair is False
    )


def v0366_readiness_report_is_not_execution_ready(report: V0366ReadinessReport) -> bool:
    return isinstance(report, V0366ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
