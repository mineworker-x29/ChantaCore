from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from pathlib import Path
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_engine import (
    SandboxFileWriteRecord,
    SandboxPatchApplyResult,
    validate_sandbox_apply_path_containment,
)


V0365_VERSION = "v0.36.5"
V0365_RELEASE_NAME = "v0.36.5 Sandbox Post-Apply Validation & Reconciliation"
MAX_PREVIEW_CHARS = 600
MAX_FILE_READ_CHARS = 12000

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_sandbox_repair",
    "ready_for_automatic_repair",
    "ready_for_multi_cycle_repair_loop",
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

PROHIBITED_RUNTIME_ACTIONS = (
    "write",
    "apply",
    "apply_patch",
    "git_apply",
    "shell",
    "test_execution",
    "dependency_install",
    "external_agent_execution",
    "dominion_runtime",
    "repair_loop",
)


class SandboxPostApplyValidationMode(StrEnum):
    VALIDATE_WRITE_RECORDS_ONLY = "validate_write_records_only"
    VALIDATE_SANDBOX_FILE_SNAPSHOTS = "validate_sandbox_file_snapshots"
    VALIDATE_EXPECTED_VS_ACTUAL_CONTENT = "validate_expected_vs_actual_content"
    VALIDATE_SCOPE_AND_SAFETY = "validate_scope_and_safety"
    FULL_STATIC_RECONCILIATION = "full_static_reconciliation"
    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxValidationSourceKind(StrEnum):
    V0364_SANDBOX_PATCH_APPLY_RESULT = "v0364_sandbox_patch_apply_result"
    V0364_SANDBOX_ENGINE_FILE_RESULT = "v0364_sandbox_engine_file_result"
    V0364_SANDBOX_FILE_WRITE_RECORD = "v0364_sandbox_file_write_record"
    V0364_SANDBOX_FILE_WRITE_OPERATION = "v0364_sandbox_file_write_operation"
    V0363_SANDBOX_WORKSPACE_MANIFEST = "v0363_sandbox_workspace_manifest"
    V0363_SANDBOX_WORKSPACE_PLAN = "v0363_sandbox_workspace_plan"
    V0362_DRY_RUN_APPLY_SIMULATION_RESULT = "v0362_dry_run_apply_simulation_result"
    V0362_SIMULATED_FILE_RESULT = "v0362_simulated_file_result"
    V0362_SIMULATED_FILE_DELTA = "v0362_simulated_file_delta"
    V0361_APPLY_CANDIDATE_ENVELOPE = "v0361_apply_candidate_envelope"
    SANDBOX_FILE_SNAPSHOT = "sandbox_file_snapshot"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxValidationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    VALIDATION_COMPLETED = "validation_completed"
    VALIDATION_COMPLETED_WITH_WARNINGS = "validation_completed_with_warnings"
    RECONCILIATION_COMPLETED = "reconciliation_completed"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxValidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    VALIDATION_CONTRACT_READY = "validation_contract_ready"
    STATIC_VALIDATION_READY = "static_validation_ready"
    RECONCILIATION_REPORT_READY = "reconciliation_report_ready"
    SAFETY_REGRESSION_REPORT_READY = "safety_regression_report_ready"
    DESIGN_HANDOFF_READY_FOR_V0366 = "design_handoff_ready_for_v0366"
    DESIGN_HANDOFF_READY_FOR_V0367 = "design_handoff_ready_for_v0367"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxValidationDecisionKind(StrEnum):
    ALLOW_STATIC_VALIDATION = "allow_static_validation"
    ALLOW_SANDBOX_FILE_READ = "allow_sandbox_file_read"
    ALLOW_EXPECTED_ACTUAL_COMPARISON = "allow_expected_actual_comparison"
    ALLOW_RECONCILIATION_REPORT = "allow_reconciliation_report"
    ALLOW_FUTURE_AGENTIC_TASK_INPUT = "allow_future_agentic_task_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxValidationRiskKind(StrEnum):
    MISSING_APPLY_RESULT_RISK = "missing_apply_result_risk"
    MISSING_WRITE_RECORD_RISK = "missing_write_record_risk"
    MISSING_SANDBOX_FILE_RISK = "missing_sandbox_file_risk"
    SANDBOX_FILE_MISMATCH_RISK = "sandbox_file_mismatch_risk"
    UNEXPECTED_SANDBOX_FILE_RISK = "unexpected_sandbox_file_risk"
    OUTSIDE_SANDBOX_READ_RISK = "outside_sandbox_read_risk"
    OUTSIDE_SANDBOX_WRITE_RISK = "outside_sandbox_write_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    UNSAFE_READINESS_FLAG_RISK = "unsafe_readiness_flag_risk"
    PROVIDER_NETWORK_OPENING_RISK = "provider_network_opening_risk"
    CREDENTIAL_ACCESS_OPENING_RISK = "credential_access_opening_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    SHELL_EXECUTION_OPENING_RISK = "shell_execution_opening_risk"
    TEST_EXECUTION_OPENING_RISK = "test_execution_opening_risk"
    DEPENDENCY_INSTALL_OPENING_RISK = "dependency_install_opening_risk"
    REFERENCE_EXECUTION_OPENING_RISK = "reference_execution_opening_risk"
    EXTERNAL_AGENT_EXECUTION_OPENING_RISK = "external_agent_execution_opening_risk"
    DOMINION_RUNTIME_OPENING_RISK = "dominion_runtime_opening_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    UNKNOWN = "unknown"


class SandboxValidationCheckKind(StrEnum):
    WRITE_RECORD_INTEGRITY_CHECK = "write_record_integrity_check"
    SANDBOX_PATH_CONTAINMENT_CHECK = "sandbox_path_containment_check"
    EXPECTED_ACTUAL_CONTENT_CHECK = "expected_actual_content_check"
    INTENDED_FILES_ONLY_CHECK = "intended_files_only_check"
    NO_LIVE_WRITE_CHECK = "no_live_write_check"
    NO_OUTSIDE_SANDBOX_WRITE_CHECK = "no_outside_sandbox_write_check"
    NO_UNSAFE_READINESS_FLAG_CHECK = "no_unsafe_readiness_flag_check"
    NO_PROVIDER_NETWORK_OPENING_CHECK = "no_provider_network_opening_check"
    NO_CREDENTIAL_SECRET_CHECK = "no_credential_secret_check"
    NO_SHELL_COMMAND_CHECK = "no_shell_command_check"
    NO_TEST_EXECUTION_CHECK = "no_test_execution_check"
    NO_DEPENDENCY_INSTALL_CHECK = "no_dependency_install_check"
    NO_EXTERNAL_AGENT_CHECK = "no_external_agent_check"
    NO_DOMINION_RUNTIME_CHECK = "no_dominion_runtime_check"
    NO_AUTOMATIC_REPAIR_CHECK = "no_automatic_repair_check"
    UNKNOWN = "unknown"


class SandboxFileObservationStatus(StrEnum):
    UNKNOWN = "unknown"
    OBSERVED = "observed"
    OBSERVED_WITH_WARNINGS = "observed_with_warnings"
    MISSING = "missing"
    MISMATCHED = "mismatched"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    SAFE_FAILED = "safe_failed"


class SandboxReconciliationFindingKind(StrEnum):
    MATCHES_EXPECTED = "matches_expected"
    CONTENT_MISMATCH = "content_mismatch"
    MISSING_EXPECTED_FILE = "missing_expected_file"
    UNEXPECTED_FILE = "unexpected_file"
    UNEXPECTED_WRITE_RECORD = "unexpected_write_record"
    MISSING_WRITE_RECORD = "missing_write_record"
    PATH_MISMATCH = "path_mismatch"
    SCOPE_MISMATCH = "scope_mismatch"
    BLOCKED_PATH_WRITTEN = "blocked_path_written"
    NO_CHANGE = "no_change"
    UNKNOWN = "unknown"


class SandboxSafetyRegressionKind(StrEnum):
    UNSAFE_READINESS_FLAG_INTRODUCED = "unsafe_readiness_flag_introduced"
    PROVIDER_NETWORK_BOUNDARY_OPENED = "provider_network_boundary_opened"
    CREDENTIAL_BOUNDARY_OPENED = "credential_boundary_opened"
    SECRET_LIKE_CONTENT_INTRODUCED = "secret_like_content_introduced"
    SHELL_COMMAND_INTRODUCED = "shell_command_introduced"
    SUBPROCESS_OR_COMMAND_EXECUTION_INTRODUCED = "subprocess_or_command_execution_introduced"
    TEST_EXECUTION_INTRODUCED = "test_execution_introduced"
    DEPENDENCY_INSTALL_INTRODUCED = "dependency_install_introduced"
    REFERENCE_EXECUTION_INTRODUCED = "reference_execution_introduced"
    EXTERNAL_AGENT_INVOCATION_INTRODUCED = "external_agent_invocation_introduced"
    DOMINION_RUNTIME_INTRODUCED = "dominion_runtime_introduced"
    PERSISTENT_TRACE_WRITE_INTRODUCED = "persistent_trace_write_introduced"
    LIVE_WRITE_INDICATOR_INTRODUCED = "live_write_indicator_introduced"
    AUTOMATIC_REPAIR_LOOP_INTRODUCED = "automatic_repair_loop_introduced"
    UNKNOWN = "unknown"


class SandboxValidationSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0365_VERSION not in version:
        raise ValueError("version must include v0.36.5")


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
            raise ValueError(f"{name} must always be False in v0.36.5")


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


def _hash_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def _high_or_blocking(severity: SandboxValidationSeverity | str) -> bool:
    return SandboxValidationSeverity(severity) in {
        SandboxValidationSeverity.HIGH,
        SandboxValidationSeverity.CRITICAL,
        SandboxValidationSeverity.BLOCKED,
    }


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationFlagSet:
    flag_set_id: str
    version: str
    sandbox_post_apply_validation_constructed: bool
    sandbox_static_validation_available: bool
    sandbox_reconciliation_available: bool
    sandbox_safety_regression_scan_available: bool
    sandbox_scope_validation_available: bool
    sandbox_validation_report_available: bool
    ready_for_v0366_bounded_agentic_task_operation_cycle: bool
    ready_for_v0367_patch_apply_sandbox_ocel_trace_packet: bool
    ready_for_sandbox_post_apply_validation: bool
    ready_for_sandbox_static_validation: bool
    ready_for_sandbox_reconciliation_report: bool
    ready_for_sandbox_safety_regression_scan: bool
    ready_for_sandbox_scope_validation: bool
    ready_for_future_agentic_task_operation_input: bool
    ready_for_execution: bool = False
    ready_for_sandbox_repair: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_multi_cycle_repair_loop: bool = False
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


@dataclass(frozen=True, kw_only=True)
class SandboxValidationSourceRef:
    source_ref_id: str
    source_kind: SandboxValidationSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxValidationSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationPolicy:
    validation_policy_id: str
    version: str
    allowed_modes: list[SandboxPostApplyValidationMode | str]
    blocked_modes: list[SandboxPostApplyValidationMode | str]
    required_checks: list[SandboxValidationCheckKind | str]
    blocked_risks: list[SandboxValidationRiskKind | str]
    max_files_to_read: int
    max_file_read_chars: int
    max_total_read_chars: int
    max_findings: int
    allow_sandbox_file_read: bool
    allow_write_record_validation: bool
    allow_expected_actual_comparison: bool
    allow_static_safety_scan: bool
    allow_reconciliation_report: bool
    allow_future_agentic_task_input: bool
    allow_sandbox_file_write: bool = False
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
    allow_automatic_repair: bool = False
    allow_multi_cycle_repair_loop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_policy_id", self.validation_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, SandboxPostApplyValidationMode)
        _validate_enum_list("blocked_modes", self.blocked_modes, SandboxPostApplyValidationMode)
        _validate_enum_list("required_checks", self.required_checks, SandboxValidationCheckKind)
        _validate_enum_list("blocked_risks", self.blocked_risks, SandboxValidationRiskKind)
        for name in ("max_files_to_read", "max_file_read_chars", "max_total_read_chars", "max_findings"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(
            self,
            (
                "allow_sandbox_file_write",
                "allow_live_workspace_write",
                "allow_patch_application",
                "allow_workspace_write",
                "allow_code_edit",
                "allow_apply_patch",
                "allow_git_apply",
                "allow_test_execution",
                "allow_shell",
                "allow_dependency_install",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
                "allow_automatic_repair",
                "allow_multi_cycle_repair_loop",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationInput:
    validation_input_id: str
    version: str
    sandbox_apply_result_id: str | None
    sandbox_root_ref: str
    manifest_id: str | None
    dry_run_result_id: str | None
    apply_candidate_id: str | None
    requested_mode: SandboxPostApplyValidationMode | str
    source_refs: list[SandboxValidationSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_input_id", "sandbox_root_ref", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxPostApplyValidationMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_RUNTIME_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing {missing}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxExpectedFileState:
    expected_state_id: str
    target_path_ref: str
    expected_content_preview: str
    expected_content_hash: str | None
    expected_summary: str
    source_delta_ids: list[str]
    redacted: bool
    truncated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("expected_state_id", "target_path_ref", "expected_summary"):
            _require_non_blank(name, getattr(self, name))
        if _bounded_preview(self.expected_content_preview) != self.expected_content_preview:
            raise ValueError("expected_content_preview must be bounded and redacted")
        _validate_string_list("source_delta_ids", self.source_delta_ids)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxActualFileState:
    actual_state_id: str
    sandbox_path_ref: str
    actual_content_preview: str
    actual_content_hash: str | None
    actual_summary: str
    file_exists: bool
    bytes_read: int
    redacted: bool
    truncated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("actual_state_id", "sandbox_path_ref", "actual_summary"):
            _require_non_blank(name, getattr(self, name))
        if _bounded_preview(self.actual_content_preview) != self.actual_content_preview:
            raise ValueError("actual_content_preview must be bounded and redacted")
        if self.bytes_read < 0:
            raise ValueError("bytes_read must be >= 0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxAppliedFileObservation:
    observation_id: str
    sandbox_root_ref: str
    sandbox_path_ref: str
    observation_status: SandboxFileObservationStatus | str
    expected_state: SandboxExpectedFileState | None
    actual_state: SandboxActualFileState | None
    observation_summary: str
    risks: list[SandboxValidationRiskKind | str]
    ready_for_write: bool = False
    ready_for_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("observation_id", "sandbox_root_ref", "sandbox_path_ref", "observation_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxFileObservationStatus(self.observation_status)
        _validate_enum_list("risks", self.risks, SandboxValidationRiskKind)
        _validate_false(self, ("ready_for_write", "ready_for_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxFileContentComparison:
    comparison_id: str
    observation_id: str
    target_path_ref: str
    matches_expected: bool
    mismatch_summary: str | None
    expected_hash: str | None
    actual_hash: str | None
    finding_kind: SandboxReconciliationFindingKind | str
    severity: SandboxValidationSeverity | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("comparison_id", "observation_id", "target_path_ref"):
            _require_non_blank(name, getattr(self, name))
        SandboxReconciliationFindingKind(self.finding_kind)
        SandboxValidationSeverity(self.severity)
        if not self.matches_expected and not self.mismatch_summary:
            raise ValueError("mismatch comparison must include mismatch_summary")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxValidationFinding:
    finding_id: str
    check_kind: SandboxValidationCheckKind | str
    risk_kind: SandboxValidationRiskKind | str
    severity: SandboxValidationSeverity | str
    summary: str
    evidence_preview: str
    blocks_future_agentic_task_input: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxValidationCheckKind(self.check_kind)
        SandboxValidationRiskKind(self.risk_kind)
        SandboxValidationSeverity(self.severity)
        if _bounded_preview(self.evidence_preview) != self.evidence_preview:
            raise ValueError("evidence_preview must be bounded and redacted")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxScopeValidationFinding:
    scope_finding_id: str
    sandbox_path_ref: str
    risk_kind: SandboxValidationRiskKind | str
    severity: SandboxValidationSeverity | str
    summary: str
    blocks_validation_success: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_finding_id", "sandbox_path_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxValidationRiskKind(self.risk_kind)
        SandboxValidationSeverity(self.severity)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxSafetyRegressionFinding:
    safety_finding_id: str
    regression_kind: SandboxSafetyRegressionKind | str
    risk_kind: SandboxValidationRiskKind | str
    severity: SandboxValidationSeverity | str
    target_path_ref: str
    evidence_preview: str
    summary: str
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_finding_id", "target_path_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxSafetyRegressionKind(self.regression_kind)
        SandboxValidationRiskKind(self.risk_kind)
        SandboxValidationSeverity(self.severity)
        if _bounded_preview(self.evidence_preview) != self.evidence_preview:
            raise ValueError("evidence_preview must be bounded and redacted")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxReconciliationFinding:
    reconciliation_finding_id: str
    finding_kind: SandboxReconciliationFindingKind | str
    target_path_ref: str
    severity: SandboxValidationSeverity | str
    summary: str
    repair_triggered: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("reconciliation_finding_id", "target_path_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxReconciliationFindingKind(self.finding_kind)
        SandboxValidationSeverity(self.severity)
        _validate_false(self, ("repair_triggered",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxProposalReconciliationReport:
    reconciliation_report_id: str
    sandbox_apply_result_id: str
    observations: list[SandboxAppliedFileObservation]
    comparisons: list[SandboxFileContentComparison]
    findings: list[SandboxReconciliationFinding]
    summary: str
    matches_expected: bool
    repair_triggered: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("reconciliation_report_id", "sandbox_apply_result_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        for name in ("observations", "comparisons", "findings"):
            _validate_list(name, getattr(self, name))
        _validate_false(self, ("repair_triggered",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxStaticValidationReport:
    static_validation_report_id: str
    findings: list[SandboxValidationFinding]
    summary: str
    static_validation_successful: bool
    test_execution_performed: bool = False
    command_execution_performed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("static_validation_report_id", self.static_validation_report_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_false(self, ("test_execution_performed", "command_execution_performed"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxSafetyRegressionReport:
    safety_regression_report_id: str
    findings: list[SandboxSafetyRegressionFinding]
    summary: str
    safety_regression_detected: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safety_regression_report_id", self.safety_regression_report_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxScopeValidationReport:
    scope_validation_report_id: str
    findings: list[SandboxScopeValidationFinding]
    summary: str
    no_outside_sandbox_paths: bool
    no_live_workspace_paths: bool
    no_reference_paths: bool
    scope_valid: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scope_validation_report_id", self.scope_validation_report_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationDecision:
    decision_id: str
    decision_kind: SandboxValidationDecisionKind | str
    status: SandboxValidationStatus | str
    summary: str
    allow_future_agentic_task_input: bool
    allow_repair: bool = False
    allow_write: bool = False
    allow_apply: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxValidationDecisionKind(self.decision_kind)
        SandboxValidationStatus(self.status)
        _validate_false(
            self,
            (
                "allow_repair",
                "allow_write",
                "allow_apply",
                "allow_test_execution",
                "allow_shell",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationReport:
    validation_report_id: str
    version: str
    validation_input_id: str
    sandbox_apply_result_id: str
    status: SandboxValidationStatus | str
    readiness_level: SandboxValidationReadinessLevel | str
    reconciliation_report: SandboxProposalReconciliationReport
    static_validation_report: SandboxStaticValidationReport
    safety_regression_report: SandboxSafetyRegressionReport
    scope_validation_report: SandboxScopeValidationReport
    decision: SandboxPostApplyValidationDecision
    summary: str
    validation_successful: bool
    ready_for_v0366_bounded_agentic_task_operation_cycle: bool
    ready_for_v0367_patch_apply_sandbox_ocel_trace_packet: bool
    ready_for_future_agentic_task_operation_input: bool
    production_certified: bool = False
    test_execution_performed: bool = False
    live_workspace_write_performed: bool = False
    sandbox_file_write_performed: bool = False
    patch_application_performed: bool = False
    automatic_repair_performed: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "validation_input_id", "sandbox_apply_result_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxValidationStatus(self.status)
        SandboxValidationReadinessLevel(self.readiness_level)
        _validate_false(
            self,
            (
                "production_certified",
                "test_execution_performed",
                "live_workspace_write_performed",
                "sandbox_file_write_performed",
                "patch_application_performed",
                "automatic_repair_performed",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationRunPreview:
    run_preview_id: str
    validation_input_id: str
    preview_summary: str
    planned_validation_actions: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_sandbox_post_apply_validation: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "validation_input_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("planned_validation_actions", self.planned_validation_actions)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyNoLiveWriteNoTestGuarantee:
    guarantee_id: str
    version: str
    no_sandbox_write: bool
    no_live_workspace_write: bool
    no_live_code_edit: bool
    no_additional_patch_application: bool
    no_automatic_repair: bool
    no_multi_cycle_repair_loop: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_shell_execution: bool
    no_subprocess_execution: bool
    no_command_execution: bool
    no_test_execution: bool
    no_dependency_install: bool
    no_reference_execution: bool
    no_reference_import: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_infinite_agent_loop: bool
    no_authority_grant: bool
    no_sandbox_read: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in (
            "no_sandbox_write",
            "no_live_workspace_write",
            "no_live_code_edit",
            "no_additional_patch_application",
            "no_automatic_repair",
            "no_multi_cycle_repair_loop",
            "no_apply_patch",
            "no_git_apply",
            "no_shell_execution",
            "no_subprocess_execution",
            "no_command_execution",
            "no_test_execution",
            "no_dependency_install",
            "no_reference_execution",
            "no_reference_import",
            "no_external_agent_execution",
            "no_dominion_runtime",
            "no_infinite_agent_loop",
            "no_authority_grant",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.5")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0365ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    status: SandboxValidationStatus | str
    readiness_level: SandboxValidationReadinessLevel | str
    ready_for_v0366_bounded_agentic_task_operation_cycle: bool
    ready_for_v0367_patch_apply_sandbox_ocel_trace_packet: bool
    ready_for_sandbox_post_apply_validation: bool
    ready_for_sandbox_static_validation: bool
    ready_for_sandbox_reconciliation_report: bool
    ready_for_sandbox_safety_regression_scan: bool
    ready_for_sandbox_scope_validation: bool
    ready_for_future_agentic_task_operation_input: bool
    digestion_first_policy_applied: bool
    dominion_runtime_blocked: bool
    external_agent_execution_blocked: bool
    infinite_agent_loop_blocked: bool
    bounded_agentic_task_only: bool
    no_independent_autonomous_agent_runtime: bool
    automatic_repair_loop_blocked: bool
    ready_for_execution: bool = False
    ready_for_sandbox_repair: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_multi_cycle_repair_loop: bool = False
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
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _require_non_blank("release_name", self.release_name)
        _validate_version(self.version)
        SandboxValidationStatus(self.status)
        SandboxValidationReadinessLevel(self.readiness_level)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_sandbox_post_apply_validation_flags(**kwargs: Any) -> SandboxPostApplyValidationFlagSet:
    return SandboxPostApplyValidationFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_post_apply_validation_flags:v0.36.5"),
        version=kwargs.pop("version", V0365_VERSION),
        sandbox_post_apply_validation_constructed=kwargs.pop("sandbox_post_apply_validation_constructed", True),
        sandbox_static_validation_available=kwargs.pop("sandbox_static_validation_available", True),
        sandbox_reconciliation_available=kwargs.pop("sandbox_reconciliation_available", True),
        sandbox_safety_regression_scan_available=kwargs.pop("sandbox_safety_regression_scan_available", True),
        sandbox_scope_validation_available=kwargs.pop("sandbox_scope_validation_available", True),
        sandbox_validation_report_available=kwargs.pop("sandbox_validation_report_available", True),
        ready_for_v0366_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_v0366_bounded_agentic_task_operation_cycle", True),
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=kwargs.pop("ready_for_v0367_patch_apply_sandbox_ocel_trace_packet", True),
        ready_for_sandbox_post_apply_validation=kwargs.pop("ready_for_sandbox_post_apply_validation", True),
        ready_for_sandbox_static_validation=kwargs.pop("ready_for_sandbox_static_validation", True),
        ready_for_sandbox_reconciliation_report=kwargs.pop("ready_for_sandbox_reconciliation_report", True),
        ready_for_sandbox_safety_regression_scan=kwargs.pop("ready_for_sandbox_safety_regression_scan", True),
        ready_for_sandbox_scope_validation=kwargs.pop("ready_for_sandbox_scope_validation", True),
        ready_for_future_agentic_task_operation_input=kwargs.pop("ready_for_future_agentic_task_operation_input", True),
        **kwargs,
    )


def build_sandbox_validation_source_ref(**kwargs: Any) -> SandboxValidationSourceRef:
    return SandboxValidationSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_validation_source_ref:v0.36.5"),
        source_kind=kwargs.pop("source_kind", SandboxValidationSourceKind.TEST_FIXTURE),
        source_id=kwargs.pop("source_id", "source:v0.36.5"),
        source_summary=kwargs.pop("source_summary", "sandbox validation source metadata; not execution"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        **kwargs,
    )


def default_sandbox_post_apply_validation_policy(**kwargs: Any) -> SandboxPostApplyValidationPolicy:
    return build_sandbox_post_apply_validation_policy(**kwargs)


def build_sandbox_post_apply_validation_policy(**kwargs: Any) -> SandboxPostApplyValidationPolicy:
    return SandboxPostApplyValidationPolicy(
        validation_policy_id=kwargs.pop("validation_policy_id", "sandbox_post_apply_validation_policy:v0.36.5"),
        version=kwargs.pop("version", V0365_VERSION),
        allowed_modes=kwargs.pop(
            "allowed_modes",
            [
                SandboxPostApplyValidationMode.VALIDATE_WRITE_RECORDS_ONLY,
                SandboxPostApplyValidationMode.VALIDATE_SANDBOX_FILE_SNAPSHOTS,
                SandboxPostApplyValidationMode.VALIDATE_EXPECTED_VS_ACTUAL_CONTENT,
                SandboxPostApplyValidationMode.VALIDATE_SCOPE_AND_SAFETY,
                SandboxPostApplyValidationMode.FULL_STATIC_RECONCILIATION,
                SandboxPostApplyValidationMode.METADATA_ONLY,
            ],
        ),
        blocked_modes=kwargs.pop("blocked_modes", [SandboxPostApplyValidationMode.UNKNOWN, SandboxPostApplyValidationMode.BLOCKED]),
        required_checks=kwargs.pop(
            "required_checks",
            [
                SandboxValidationCheckKind.WRITE_RECORD_INTEGRITY_CHECK,
                SandboxValidationCheckKind.SANDBOX_PATH_CONTAINMENT_CHECK,
                SandboxValidationCheckKind.EXPECTED_ACTUAL_CONTENT_CHECK,
                SandboxValidationCheckKind.NO_LIVE_WRITE_CHECK,
                SandboxValidationCheckKind.NO_OUTSIDE_SANDBOX_WRITE_CHECK,
                SandboxValidationCheckKind.NO_UNSAFE_READINESS_FLAG_CHECK,
                SandboxValidationCheckKind.NO_AUTOMATIC_REPAIR_CHECK,
            ],
        ),
        blocked_risks=kwargs.pop(
            "blocked_risks",
            [
                SandboxValidationRiskKind.OUTSIDE_SANDBOX_READ_RISK,
                SandboxValidationRiskKind.OUTSIDE_SANDBOX_WRITE_RISK,
                SandboxValidationRiskKind.LIVE_WORKSPACE_WRITE_RISK,
                SandboxValidationRiskKind.AUTOMATIC_REPAIR_RISK,
                SandboxValidationRiskKind.MULTI_CYCLE_LOOP_RISK,
            ],
        ),
        max_files_to_read=kwargs.pop("max_files_to_read", 100),
        max_file_read_chars=kwargs.pop("max_file_read_chars", MAX_FILE_READ_CHARS),
        max_total_read_chars=kwargs.pop("max_total_read_chars", MAX_FILE_READ_CHARS * 10),
        max_findings=kwargs.pop("max_findings", 200),
        allow_sandbox_file_read=kwargs.pop("allow_sandbox_file_read", True),
        allow_write_record_validation=kwargs.pop("allow_write_record_validation", True),
        allow_expected_actual_comparison=kwargs.pop("allow_expected_actual_comparison", True),
        allow_static_safety_scan=kwargs.pop("allow_static_safety_scan", True),
        allow_reconciliation_report=kwargs.pop("allow_reconciliation_report", True),
        allow_future_agentic_task_input=kwargs.pop("allow_future_agentic_task_input", True),
        **kwargs,
    )


def build_sandbox_post_apply_validation_input(**kwargs: Any) -> SandboxPostApplyValidationInput:
    return SandboxPostApplyValidationInput(
        validation_input_id=kwargs.pop("validation_input_id", "sandbox_post_apply_validation_input:v0.36.5"),
        version=kwargs.pop("version", V0365_VERSION),
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", None),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "virtual-sandbox-root"),
        manifest_id=kwargs.pop("manifest_id", None),
        dry_run_result_id=kwargs.pop("dry_run_result_id", None),
        apply_candidate_id=kwargs.pop("apply_candidate_id", None),
        requested_mode=kwargs.pop("requested_mode", SandboxPostApplyValidationMode.FULL_STATIC_RECONCILIATION),
        source_refs=kwargs.pop("source_refs", [build_sandbox_validation_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "sandbox post-apply validation request; no write/apply/test permission"),
        **kwargs,
    )


def build_sandbox_expected_file_state(**kwargs: Any) -> SandboxExpectedFileState:
    expected_content = kwargs.pop("expected_content", None)
    preview = kwargs.pop("expected_content_preview", _bounded_preview(expected_content or ""))
    return SandboxExpectedFileState(
        expected_state_id=kwargs.pop("expected_state_id", "sandbox_expected_file_state:v0.36.5"),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        expected_content_preview=preview,
        expected_content_hash=kwargs.pop("expected_content_hash", _hash_text(expected_content) if expected_content is not None else None),
        expected_summary=kwargs.pop("expected_summary", "expected dry-run after-content metadata"),
        source_delta_ids=kwargs.pop("source_delta_ids", []),
        redacted=kwargs.pop("redacted", preview != (expected_content or preview)),
        truncated=kwargs.pop("truncated", len(expected_content or preview) > MAX_PREVIEW_CHARS),
        **kwargs,
    )


def build_sandbox_actual_file_state(**kwargs: Any) -> SandboxActualFileState:
    actual_content = kwargs.pop("actual_content", None)
    preview = kwargs.pop("actual_content_preview", _bounded_preview(actual_content or ""))
    return SandboxActualFileState(
        actual_state_id=kwargs.pop("actual_state_id", "sandbox_actual_file_state:v0.36.5"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        actual_content_preview=preview,
        actual_content_hash=kwargs.pop("actual_content_hash", _hash_text(actual_content) if actual_content is not None else None),
        actual_summary=kwargs.pop("actual_summary", "actual sandbox file snapshot metadata"),
        file_exists=kwargs.pop("file_exists", actual_content is not None),
        bytes_read=kwargs.pop("bytes_read", len((actual_content or "").encode("utf-8"))),
        redacted=kwargs.pop("redacted", preview != (actual_content or preview)),
        truncated=kwargs.pop("truncated", len(actual_content or preview) > MAX_PREVIEW_CHARS),
        **kwargs,
    )


def build_sandbox_applied_file_observation(**kwargs: Any) -> SandboxAppliedFileObservation:
    return SandboxAppliedFileObservation(
        observation_id=kwargs.pop("observation_id", "sandbox_file_observation:v0.36.5"),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "virtual-sandbox-root"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        observation_status=kwargs.pop("observation_status", SandboxFileObservationStatus.OBSERVED),
        expected_state=kwargs.pop("expected_state", build_sandbox_expected_file_state()),
        actual_state=kwargs.pop("actual_state", build_sandbox_actual_file_state(actual_content="")),
        observation_summary=kwargs.pop("observation_summary", "sandbox file observed by read-only validation"),
        risks=kwargs.pop("risks", []),
        **kwargs,
    )


def build_sandbox_file_content_comparison(**kwargs: Any) -> SandboxFileContentComparison:
    return SandboxFileContentComparison(
        comparison_id=kwargs.pop("comparison_id", "sandbox_file_content_comparison:v0.36.5"),
        observation_id=kwargs.pop("observation_id", "sandbox_file_observation:v0.36.5"),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        matches_expected=kwargs.pop("matches_expected", True),
        mismatch_summary=kwargs.pop("mismatch_summary", None),
        expected_hash=kwargs.pop("expected_hash", None),
        actual_hash=kwargs.pop("actual_hash", None),
        finding_kind=kwargs.pop("finding_kind", SandboxReconciliationFindingKind.MATCHES_EXPECTED),
        severity=kwargs.pop("severity", SandboxValidationSeverity.INFO),
        **kwargs,
    )


def build_sandbox_validation_finding(**kwargs: Any) -> SandboxValidationFinding:
    return SandboxValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_validation_finding:v0.36.5"),
        check_kind=kwargs.pop("check_kind", SandboxValidationCheckKind.NO_UNSAFE_READINESS_FLAG_CHECK),
        risk_kind=kwargs.pop("risk_kind", SandboxValidationRiskKind.UNSAFE_READINESS_FLAG_RISK),
        severity=kwargs.pop("severity", SandboxValidationSeverity.HIGH),
        summary=kwargs.pop("summary", "static sandbox validation finding"),
        evidence_preview=kwargs.pop("evidence_preview", ""),
        blocks_future_agentic_task_input=kwargs.pop("blocks_future_agentic_task_input", True),
        **kwargs,
    )


def build_sandbox_scope_validation_finding(**kwargs: Any) -> SandboxScopeValidationFinding:
    return SandboxScopeValidationFinding(
        scope_finding_id=kwargs.pop("scope_finding_id", "sandbox_scope_finding:v0.36.5"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        risk_kind=kwargs.pop("risk_kind", SandboxValidationRiskKind.OUTSIDE_SANDBOX_WRITE_RISK),
        severity=kwargs.pop("severity", SandboxValidationSeverity.BLOCKED),
        summary=kwargs.pop("summary", "sandbox scope finding"),
        blocks_validation_success=kwargs.pop("blocks_validation_success", True),
        **kwargs,
    )


def build_sandbox_safety_regression_finding(**kwargs: Any) -> SandboxSafetyRegressionFinding:
    return SandboxSafetyRegressionFinding(
        safety_finding_id=kwargs.pop("safety_finding_id", "sandbox_safety_regression_finding:v0.36.5"),
        regression_kind=kwargs.pop("regression_kind", SandboxSafetyRegressionKind.UNSAFE_READINESS_FLAG_INTRODUCED),
        risk_kind=kwargs.pop("risk_kind", SandboxValidationRiskKind.UNSAFE_READINESS_FLAG_RISK),
        severity=kwargs.pop("severity", SandboxValidationSeverity.HIGH),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        evidence_preview=kwargs.pop("evidence_preview", ""),
        summary=kwargs.pop("summary", "static safety regression detected"),
        requires_review=kwargs.pop("requires_review", True),
        **kwargs,
    )


def build_sandbox_reconciliation_finding(**kwargs: Any) -> SandboxReconciliationFinding:
    return SandboxReconciliationFinding(
        reconciliation_finding_id=kwargs.pop("reconciliation_finding_id", "sandbox_reconciliation_finding:v0.36.5"),
        finding_kind=kwargs.pop("finding_kind", SandboxReconciliationFindingKind.CONTENT_MISMATCH),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        severity=kwargs.pop("severity", SandboxValidationSeverity.HIGH),
        summary=kwargs.pop("summary", "sandbox reconciliation finding; no repair triggered"),
        **kwargs,
    )


def build_sandbox_proposal_reconciliation_report(**kwargs: Any) -> SandboxProposalReconciliationReport:
    return SandboxProposalReconciliationReport(
        reconciliation_report_id=kwargs.pop("reconciliation_report_id", "sandbox_reconciliation_report:v0.36.5"),
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", "sandbox_apply_result:v0.36.4"),
        observations=kwargs.pop("observations", []),
        comparisons=kwargs.pop("comparisons", []),
        findings=kwargs.pop("findings", []),
        summary=kwargs.pop("summary", "expected-vs-actual sandbox reconciliation report; no repair"),
        matches_expected=kwargs.pop("matches_expected", True),
        **kwargs,
    )


def build_sandbox_static_validation_report(**kwargs: Any) -> SandboxStaticValidationReport:
    findings = kwargs.pop("findings", [])
    return SandboxStaticValidationReport(
        static_validation_report_id=kwargs.pop("static_validation_report_id", "sandbox_static_validation_report:v0.36.5"),
        findings=findings,
        summary=kwargs.pop("summary", "static sandbox validation completed without test execution"),
        static_validation_successful=kwargs.pop("static_validation_successful", not findings),
        **kwargs,
    )


def build_sandbox_safety_regression_report(**kwargs: Any) -> SandboxSafetyRegressionReport:
    findings = kwargs.pop("findings", [])
    return SandboxSafetyRegressionReport(
        safety_regression_report_id=kwargs.pop("safety_regression_report_id", "sandbox_safety_regression_report:v0.36.5"),
        findings=findings,
        summary=kwargs.pop("summary", "sandbox safety regression scan metadata"),
        safety_regression_detected=kwargs.pop("safety_regression_detected", bool(findings)),
        **kwargs,
    )


def build_sandbox_scope_validation_report(**kwargs: Any) -> SandboxScopeValidationReport:
    findings = kwargs.pop("findings", [])
    return SandboxScopeValidationReport(
        scope_validation_report_id=kwargs.pop("scope_validation_report_id", "sandbox_scope_validation_report:v0.36.5"),
        findings=findings,
        summary=kwargs.pop("summary", "sandbox scope validation metadata"),
        no_outside_sandbox_paths=kwargs.pop("no_outside_sandbox_paths", not findings),
        no_live_workspace_paths=kwargs.pop("no_live_workspace_paths", not findings),
        no_reference_paths=kwargs.pop("no_reference_paths", not findings),
        scope_valid=kwargs.pop("scope_valid", not findings),
        **kwargs,
    )


def build_sandbox_post_apply_validation_decision(**kwargs: Any) -> SandboxPostApplyValidationDecision:
    return SandboxPostApplyValidationDecision(
        decision_id=kwargs.pop("decision_id", "sandbox_post_apply_validation_decision:v0.36.5"),
        decision_kind=kwargs.pop("decision_kind", SandboxValidationDecisionKind.ALLOW_FUTURE_AGENTIC_TASK_INPUT),
        status=kwargs.pop("status", SandboxValidationStatus.VALIDATION_COMPLETED),
        summary=kwargs.pop("summary", "future bounded agentic task input allowed; no repair/write/apply/test permission"),
        allow_future_agentic_task_input=kwargs.pop("allow_future_agentic_task_input", True),
        **kwargs,
    )


def build_sandbox_post_apply_validation_report(**kwargs: Any) -> SandboxPostApplyValidationReport:
    reconciliation_report = kwargs.pop("reconciliation_report", build_sandbox_proposal_reconciliation_report())
    static_report = kwargs.pop("static_validation_report", build_sandbox_static_validation_report())
    safety_report = kwargs.pop("safety_regression_report", build_sandbox_safety_regression_report())
    scope_report = kwargs.pop("scope_validation_report", build_sandbox_scope_validation_report())
    successful = kwargs.pop(
        "validation_successful",
        reconciliation_report.matches_expected
        and static_report.static_validation_successful
        and not safety_report.safety_regression_detected
        and scope_report.scope_valid,
    )
    return SandboxPostApplyValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_post_apply_validation_report:v0.36.5"),
        version=kwargs.pop("version", V0365_VERSION),
        validation_input_id=kwargs.pop("validation_input_id", "sandbox_post_apply_validation_input:v0.36.5"),
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", reconciliation_report.sandbox_apply_result_id),
        status=kwargs.pop(
            "status",
            SandboxValidationStatus.VALIDATION_COMPLETED if successful else SandboxValidationStatus.REVIEW_REQUIRED,
        ),
        readiness_level=kwargs.pop(
            "readiness_level",
            SandboxValidationReadinessLevel.RECONCILIATION_REPORT_READY if successful else SandboxValidationReadinessLevel.BLOCKED,
        ),
        reconciliation_report=reconciliation_report,
        static_validation_report=static_report,
        safety_regression_report=safety_report,
        scope_validation_report=scope_report,
        decision=kwargs.pop("decision", build_sandbox_post_apply_validation_decision(allow_future_agentic_task_input=successful)),
        summary=kwargs.pop("summary", "sandbox post-apply validation report; not test success or production certification"),
        validation_successful=successful,
        ready_for_v0366_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_v0366_bounded_agentic_task_operation_cycle", successful),
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=kwargs.pop("ready_for_v0367_patch_apply_sandbox_ocel_trace_packet", successful),
        ready_for_future_agentic_task_operation_input=kwargs.pop("ready_for_future_agentic_task_operation_input", successful),
        **kwargs,
    )


def build_sandbox_post_apply_validation_run_preview(**kwargs: Any) -> SandboxPostApplyValidationRunPreview:
    return SandboxPostApplyValidationRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_post_apply_validation_run_preview:v0.36.5"),
        validation_input_id=kwargs.pop("validation_input_id", "sandbox_post_apply_validation_input:v0.36.5"),
        preview_summary=kwargs.pop("preview_summary", "read-only sandbox validation preview"),
        planned_validation_actions=kwargs.pop("planned_validation_actions", ["read sandbox files", "compare expected vs actual", "scan static safety"]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        ready_for_sandbox_post_apply_validation=kwargs.pop("ready_for_sandbox_post_apply_validation", True),
        **kwargs,
    )


def build_sandbox_post_apply_no_live_write_no_test_guarantee(**kwargs: Any) -> SandboxPostApplyNoLiveWriteNoTestGuarantee:
    return SandboxPostApplyNoLiveWriteNoTestGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_post_apply_no_live_write_no_test_guarantee:v0.36.5"),
        version=kwargs.pop("version", V0365_VERSION),
        no_sandbox_write=kwargs.pop("no_sandbox_write", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_live_code_edit=kwargs.pop("no_live_code_edit", True),
        no_additional_patch_application=kwargs.pop("no_additional_patch_application", True),
        no_automatic_repair=kwargs.pop("no_automatic_repair", True),
        no_multi_cycle_repair_loop=kwargs.pop("no_multi_cycle_repair_loop", True),
        no_apply_patch=kwargs.pop("no_apply_patch", True),
        no_git_apply=kwargs.pop("no_git_apply", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_subprocess_execution=kwargs.pop("no_subprocess_execution", True),
        no_command_execution=kwargs.pop("no_command_execution", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_dependency_install=kwargs.pop("no_dependency_install", True),
        no_reference_execution=kwargs.pop("no_reference_execution", True),
        no_reference_import=kwargs.pop("no_reference_import", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        no_infinite_agent_loop=kwargs.pop("no_infinite_agent_loop", True),
        no_authority_grant=kwargs.pop("no_authority_grant", True),
        **kwargs,
    )


def build_v0365_readiness_report(**kwargs: Any) -> V0365ReadinessReport:
    return V0365ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0365_readiness_report"),
        version=kwargs.pop("version", V0365_VERSION),
        release_name=kwargs.pop("release_name", V0365_RELEASE_NAME),
        status=kwargs.pop("status", SandboxValidationStatus.VALIDATION_COMPLETED),
        readiness_level=kwargs.pop("readiness_level", SandboxValidationReadinessLevel.RECONCILIATION_REPORT_READY),
        ready_for_v0366_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_v0366_bounded_agentic_task_operation_cycle", True),
        ready_for_v0367_patch_apply_sandbox_ocel_trace_packet=kwargs.pop("ready_for_v0367_patch_apply_sandbox_ocel_trace_packet", True),
        ready_for_sandbox_post_apply_validation=kwargs.pop("ready_for_sandbox_post_apply_validation", True),
        ready_for_sandbox_static_validation=kwargs.pop("ready_for_sandbox_static_validation", True),
        ready_for_sandbox_reconciliation_report=kwargs.pop("ready_for_sandbox_reconciliation_report", True),
        ready_for_sandbox_safety_regression_scan=kwargs.pop("ready_for_sandbox_safety_regression_scan", True),
        ready_for_sandbox_scope_validation=kwargs.pop("ready_for_sandbox_scope_validation", True),
        ready_for_future_agentic_task_operation_input=kwargs.pop("ready_for_future_agentic_task_operation_input", True),
        digestion_first_policy_applied=kwargs.pop("digestion_first_policy_applied", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_agent_loop_blocked=kwargs.pop("infinite_agent_loop_blocked", True),
        bounded_agentic_task_only=kwargs.pop("bounded_agentic_task_only", True),
        no_independent_autonomous_agent_runtime=kwargs.pop("no_independent_autonomous_agent_runtime", True),
        automatic_repair_loop_blocked=kwargs.pop("automatic_repair_loop_blocked", True),
        **kwargs,
    )


def build_sandbox_post_apply_validation_input_from_apply_result(
    result: SandboxPatchApplyResult,
    **kwargs: Any,
) -> SandboxPostApplyValidationInput:
    return build_sandbox_post_apply_validation_input(
        sandbox_apply_result_id=result.sandbox_apply_result_id,
        sandbox_root_ref=result.sandbox_root_ref,
        source_refs=[
            build_sandbox_validation_source_ref(
                source_kind=SandboxValidationSourceKind.V0364_SANDBOX_PATCH_APPLY_RESULT,
                source_id=result.sandbox_apply_result_id,
                source_summary="v0.36.4 sandbox patch apply result metadata",
            )
        ],
        metadata={
            "sandbox_apply_successful": result.sandbox_apply_successful,
            "write_record_count": len(result.write_records),
            "dry_run_result_id": result.materialization_plan.metadata.get("dry_run_result_id"),
            "manifest_id": result.materialization_plan.metadata.get("manifest_id"),
        },
        **kwargs,
    )


def validate_sandbox_validation_path_containment(sandbox_root_ref: str, sandbox_path_ref: str) -> Path:
    return validate_sandbox_apply_path_containment(sandbox_root_ref, sandbox_path_ref)


def read_sandbox_file_snapshot_under_policy(
    sandbox_root_ref: str,
    sandbox_path_ref: str,
    policy: SandboxPostApplyValidationPolicy | None = None,
) -> SandboxActualFileState:
    active_policy = policy or default_sandbox_post_apply_validation_policy()
    if not active_policy.allow_sandbox_file_read:
        raise ValueError("sandbox file read is blocked by policy")
    target_path = validate_sandbox_validation_path_containment(sandbox_root_ref, sandbox_path_ref)
    if not target_path.exists():
        return build_sandbox_actual_file_state(
            actual_state_id=f"sandbox_actual_file_state:v0.36.5:missing:{sandbox_path_ref}",
            sandbox_path_ref=sandbox_path_ref,
            actual_content="",
            actual_content_hash=None,
            actual_summary="sandbox file is missing under validated root",
            file_exists=False,
            bytes_read=0,
        )
    if target_path.is_symlink():
        raise ValueError("sandbox validation blocks symlink file reads")
    text = target_path.read_text(encoding="utf-8")
    if len(text) > active_policy.max_file_read_chars:
        text = text[: active_policy.max_file_read_chars]
        truncated = True
    else:
        truncated = False
    preview = _bounded_preview(text)
    return build_sandbox_actual_file_state(
        actual_state_id=f"sandbox_actual_file_state:v0.36.5:{sandbox_path_ref}",
        sandbox_path_ref=sandbox_path_ref,
        actual_content_preview=preview,
        actual_content_hash=_hash_text(text),
        actual_summary="sandbox file read under validated sandbox root",
        file_exists=True,
        bytes_read=len(text.encode("utf-8")),
        redacted=preview != text[:MAX_PREVIEW_CHARS],
        truncated=truncated or len(text) > MAX_PREVIEW_CHARS,
    )


def compare_expected_actual_sandbox_file_state(
    expected_state: SandboxExpectedFileState,
    actual_state: SandboxActualFileState,
    observation_id: str = "sandbox_file_observation:v0.36.5",
) -> SandboxFileContentComparison:
    matches = actual_state.file_exists and expected_state.expected_content_hash == actual_state.actual_content_hash
    if matches:
        return build_sandbox_file_content_comparison(
            observation_id=observation_id,
            target_path_ref=expected_state.target_path_ref,
            matches_expected=True,
            expected_hash=expected_state.expected_content_hash,
            actual_hash=actual_state.actual_content_hash,
        )
    if not actual_state.file_exists:
        kind = SandboxReconciliationFindingKind.MISSING_EXPECTED_FILE
        summary = "expected sandbox file is missing"
    else:
        kind = SandboxReconciliationFindingKind.CONTENT_MISMATCH
        summary = "sandbox file content does not match expected dry-run after-content"
    return build_sandbox_file_content_comparison(
        observation_id=observation_id,
        target_path_ref=expected_state.target_path_ref,
        matches_expected=False,
        mismatch_summary=summary,
        expected_hash=expected_state.expected_content_hash,
        actual_hash=actual_state.actual_content_hash,
        finding_kind=kind,
        severity=SandboxValidationSeverity.HIGH,
    )


SAFETY_SCAN_PATTERNS: tuple[tuple[SandboxSafetyRegressionKind, SandboxValidationRiskKind, SandboxValidationCheckKind, SandboxValidationSeverity, tuple[str, ...]], ...] = (
    (
        SandboxSafetyRegressionKind.UNSAFE_READINESS_FLAG_INTRODUCED,
        SandboxValidationRiskKind.UNSAFE_READINESS_FLAG_RISK,
        SandboxValidationCheckKind.NO_UNSAFE_READINESS_FLAG_CHECK,
        SandboxValidationSeverity.HIGH,
        tuple(f"{name}=True" for name in UNSAFE_FLAG_NAMES),
    ),
    (
        SandboxSafetyRegressionKind.PROVIDER_NETWORK_BOUNDARY_OPENED,
        SandboxValidationRiskKind.PROVIDER_NETWORK_OPENING_RISK,
        SandboxValidationCheckKind.NO_PROVIDER_NETWORK_OPENING_CHECK,
        SandboxValidationSeverity.HIGH,
        ("import requests", "import httpx", "import urllib", "import aiohttp", "import socket"),
    ),
    (
        SandboxSafetyRegressionKind.CREDENTIAL_BOUNDARY_OPENED,
        SandboxValidationRiskKind.CREDENTIAL_ACCESS_OPENING_RISK,
        SandboxValidationCheckKind.NO_CREDENTIAL_SECRET_CHECK,
        SandboxValidationSeverity.CRITICAL,
        ("os.environ", "API_KEY", ".env", "credential", "token"),
    ),
    (
        SandboxSafetyRegressionKind.SECRET_LIKE_CONTENT_INTRODUCED,
        SandboxValidationRiskKind.SECRET_EXPOSURE_RISK,
        SandboxValidationCheckKind.NO_CREDENTIAL_SECRET_CHECK,
        SandboxValidationSeverity.CRITICAL,
        ("SECRET", "password", "private_key"),
    ),
    (
        SandboxSafetyRegressionKind.SHELL_COMMAND_INTRODUCED,
        SandboxValidationRiskKind.SHELL_EXECUTION_OPENING_RISK,
        SandboxValidationCheckKind.NO_SHELL_COMMAND_CHECK,
        SandboxValidationSeverity.HIGH,
        ("os." "system", "shell" "=True", "powershell", "cmd.exe", "bash "),
    ),
    (
        SandboxSafetyRegressionKind.SUBPROCESS_OR_COMMAND_EXECUTION_INTRODUCED,
        SandboxValidationRiskKind.SHELL_EXECUTION_OPENING_RISK,
        SandboxValidationCheckKind.NO_SHELL_COMMAND_CHECK,
        SandboxValidationSeverity.HIGH,
        ("subprocess", "run_command", "execute_command"),
    ),
    (
        SandboxSafetyRegressionKind.TEST_EXECUTION_INTRODUCED,
        SandboxValidationRiskKind.TEST_EXECUTION_OPENING_RISK,
        SandboxValidationCheckKind.NO_TEST_EXECUTION_CHECK,
        SandboxValidationSeverity.HIGH,
        ("pytest", "unittest.main", "run tests"),
    ),
    (
        SandboxSafetyRegressionKind.DEPENDENCY_INSTALL_INTRODUCED,
        SandboxValidationRiskKind.DEPENDENCY_INSTALL_OPENING_RISK,
        SandboxValidationCheckKind.NO_DEPENDENCY_INSTALL_CHECK,
        SandboxValidationSeverity.HIGH,
        ("pip install", "npm install", "poetry install", "cargo install", "go get"),
    ),
    (
        SandboxSafetyRegressionKind.REFERENCE_EXECUTION_INTRODUCED,
        SandboxValidationRiskKind.REFERENCE_EXECUTION_OPENING_RISK,
        SandboxValidationCheckKind.NO_EXTERNAL_AGENT_CHECK,
        SandboxValidationSeverity.HIGH,
        ("references/OpenCode", "references/Hermes", "references/OpenClaw"),
    ),
    (
        SandboxSafetyRegressionKind.EXTERNAL_AGENT_INVOCATION_INTRODUCED,
        SandboxValidationRiskKind.EXTERNAL_AGENT_EXECUTION_OPENING_RISK,
        SandboxValidationCheckKind.NO_EXTERNAL_AGENT_CHECK,
        SandboxValidationSeverity.HIGH,
        ("Claude Code", "Codex CLI", "external_agent", "invoke_agent"),
    ),
    (
        SandboxSafetyRegressionKind.DOMINION_RUNTIME_INTRODUCED,
        SandboxValidationRiskKind.DOMINION_RUNTIME_OPENING_RISK,
        SandboxValidationCheckKind.NO_DOMINION_RUNTIME_CHECK,
        SandboxValidationSeverity.BLOCKED,
        ("DominionAuthority", "dominion_runtime", "grant D4", "grant D9"),
    ),
    (
        SandboxSafetyRegressionKind.PERSISTENT_TRACE_WRITE_INTRODUCED,
        SandboxValidationRiskKind.UNKNOWN,
        SandboxValidationCheckKind.UNKNOWN,
        SandboxValidationSeverity.MEDIUM,
        (".jsonl", "write_ocel", "database", "trace sink"),
    ),
    (
        SandboxSafetyRegressionKind.AUTOMATIC_REPAIR_LOOP_INTRODUCED,
        SandboxValidationRiskKind.AUTOMATIC_REPAIR_RISK,
        SandboxValidationCheckKind.NO_AUTOMATIC_REPAIR_CHECK,
        SandboxValidationSeverity.BLOCKED,
        ("automatic_repair", "repair_loop", "while True"),
    ),
)


def scan_sandbox_file_static_safety(
    actual_state: SandboxActualFileState,
    policy: SandboxPostApplyValidationPolicy | None = None,
) -> SandboxSafetyRegressionReport:
    active_policy = policy or default_sandbox_post_apply_validation_policy()
    if not active_policy.allow_static_safety_scan:
        return build_sandbox_safety_regression_report(summary="static safety scan disabled by policy")
    content = str(actual_state.metadata.get("full_text", actual_state.actual_content_preview))
    findings: list[SandboxSafetyRegressionFinding] = []
    for regression_kind, risk_kind, _check_kind, severity, patterns in SAFETY_SCAN_PATTERNS:
        for pattern in patterns:
            if pattern in content:
                findings.append(
                    build_sandbox_safety_regression_finding(
                        safety_finding_id=f"sandbox_safety_regression_finding:v0.36.5:{len(findings) + 1}",
                        regression_kind=regression_kind,
                        risk_kind=risk_kind,
                        severity=severity,
                        target_path_ref=actual_state.sandbox_path_ref,
                        evidence_preview=_bounded_preview(pattern),
                        summary=f"static safety scan found blocked pattern for {regression_kind}",
                        requires_review=True,
                    )
                )
                break
    return build_sandbox_safety_regression_report(findings=findings)


def validate_sandbox_scope_after_apply(
    result: SandboxPatchApplyResult,
    policy: SandboxPostApplyValidationPolicy | None = None,
) -> SandboxScopeValidationReport:
    _ = policy or default_sandbox_post_apply_validation_policy()
    findings: list[SandboxScopeValidationFinding] = []
    for index, record in enumerate(result.write_records, start=1):
        if record.live_write:
            findings.append(
                build_sandbox_scope_validation_finding(
                    scope_finding_id=f"sandbox_scope_finding:v0.36.5:live:{index}",
                    sandbox_path_ref=record.sandbox_path_ref,
                    risk_kind=SandboxValidationRiskKind.LIVE_WORKSPACE_WRITE_RISK,
                    summary="write record reported live workspace write",
                )
            )
        if record.wrote_outside_sandbox:
            findings.append(
                build_sandbox_scope_validation_finding(
                    scope_finding_id=f"sandbox_scope_finding:v0.36.5:outside:{index}",
                    sandbox_path_ref=record.sandbox_path_ref,
                    risk_kind=SandboxValidationRiskKind.OUTSIDE_SANDBOX_WRITE_RISK,
                    summary="write record reported outside sandbox write",
                )
            )
        try:
            validate_sandbox_validation_path_containment(record.sandbox_root_ref, record.sandbox_path_ref)
        except ValueError as exc:
            findings.append(
                build_sandbox_scope_validation_finding(
                    scope_finding_id=f"sandbox_scope_finding:v0.36.5:path:{index}",
                    sandbox_path_ref=record.sandbox_path_ref,
                    risk_kind=SandboxValidationRiskKind.OUTSIDE_SANDBOX_WRITE_RISK,
                    summary=str(exc),
                )
            )
    return build_sandbox_scope_validation_report(findings=findings)


def _expected_states_from_apply_result(result: SandboxPatchApplyResult) -> list[SandboxExpectedFileState]:
    expected_states: list[SandboxExpectedFileState] = []
    for index, file_plan in enumerate(result.materialization_plan.file_plans, start=1):
        if file_plan.blocked:
            continue
        content_text = str(file_plan.metadata.get("content_text", file_plan.content_preview))
        expected_states.append(
            build_sandbox_expected_file_state(
                expected_state_id=f"sandbox_expected_file_state:v0.36.5:{index}",
                target_path_ref=file_plan.sandbox_path_ref,
                expected_content=content_text,
                source_delta_ids=[value for value in (file_plan.source_overlay_entry_id, file_plan.source_simulated_file_result_id) if value],
            )
        )
    return expected_states


def reconcile_sandbox_apply_result(
    result: SandboxPatchApplyResult,
    expected_states: list[SandboxExpectedFileState] | None = None,
    actual_states: list[SandboxActualFileState] | None = None,
) -> SandboxProposalReconciliationReport:
    expected = expected_states or _expected_states_from_apply_result(result)
    actual_by_path = {state.sandbox_path_ref: state for state in (actual_states or [])}
    written_paths = {record.sandbox_path_ref for record in result.write_records}
    observations: list[SandboxAppliedFileObservation] = []
    comparisons: list[SandboxFileContentComparison] = []
    findings: list[SandboxReconciliationFinding] = []
    for index, expected_state in enumerate(expected, start=1):
        actual_state = actual_by_path.get(expected_state.target_path_ref)
        if actual_state is None:
            actual_state = build_sandbox_actual_file_state(
                actual_state_id=f"sandbox_actual_file_state:v0.36.5:missing:{index}",
                sandbox_path_ref=expected_state.target_path_ref,
                actual_content="",
                actual_content_hash=None,
                actual_summary="expected sandbox file was not observed",
                file_exists=False,
                bytes_read=0,
            )
        comparison = compare_expected_actual_sandbox_file_state(expected_state, actual_state, f"sandbox_file_observation:v0.36.5:{index}")
        comparisons.append(comparison)
        status = SandboxFileObservationStatus.OBSERVED if comparison.matches_expected else SandboxFileObservationStatus.MISMATCHED
        observations.append(
            build_sandbox_applied_file_observation(
                observation_id=comparison.observation_id,
                sandbox_root_ref=result.sandbox_root_ref,
                sandbox_path_ref=expected_state.target_path_ref,
                observation_status=status,
                expected_state=expected_state,
                actual_state=actual_state,
                observation_summary="expected and actual sandbox file state compared",
                risks=[] if comparison.matches_expected else [SandboxValidationRiskKind.SANDBOX_FILE_MISMATCH_RISK],
            )
        )
        if not comparison.matches_expected:
            findings.append(
                build_sandbox_reconciliation_finding(
                    reconciliation_finding_id=f"sandbox_reconciliation_finding:v0.36.5:{len(findings) + 1}",
                    finding_kind=comparison.finding_kind,
                    target_path_ref=expected_state.target_path_ref,
                    summary=comparison.mismatch_summary or "sandbox reconciliation mismatch",
                )
            )
        if expected_state.target_path_ref not in written_paths:
            findings.append(
                build_sandbox_reconciliation_finding(
                    reconciliation_finding_id=f"sandbox_reconciliation_finding:v0.36.5:{len(findings) + 1}",
                    finding_kind=SandboxReconciliationFindingKind.MISSING_WRITE_RECORD,
                    target_path_ref=expected_state.target_path_ref,
                    severity=SandboxValidationSeverity.MEDIUM,
                    summary="expected sandbox file has no write record",
                )
            )
    expected_paths = {state.target_path_ref for state in expected}
    for record in result.write_records:
        if record.sandbox_path_ref not in expected_paths:
            findings.append(
                build_sandbox_reconciliation_finding(
                    reconciliation_finding_id=f"sandbox_reconciliation_finding:v0.36.5:{len(findings) + 1}",
                    finding_kind=SandboxReconciliationFindingKind.UNEXPECTED_WRITE_RECORD,
                    target_path_ref=record.sandbox_path_ref,
                    severity=SandboxValidationSeverity.HIGH,
                    summary="write record target was not part of expected dry-run state",
                )
            )
    return build_sandbox_proposal_reconciliation_report(
        sandbox_apply_result_id=result.sandbox_apply_result_id,
        observations=observations,
        comparisons=comparisons,
        findings=findings,
        matches_expected=not findings and all(comparison.matches_expected for comparison in comparisons),
    )


def run_sandbox_post_apply_validation(
    validation_input: SandboxPostApplyValidationInput,
    apply_result: SandboxPatchApplyResult,
    policy: SandboxPostApplyValidationPolicy | None = None,
) -> SandboxPostApplyValidationReport:
    active_policy = policy or default_sandbox_post_apply_validation_policy()
    if validation_input.sandbox_root_ref != apply_result.sandbox_root_ref:
        raise ValueError("validation input sandbox root must match sandbox apply result root")
    expected_states = _expected_states_from_apply_result(apply_result)
    actual_states: list[SandboxActualFileState] = []
    safety_findings: list[SandboxSafetyRegressionFinding] = []
    total_read = 0
    for expected_state in expected_states[: active_policy.max_files_to_read]:
        actual_state = read_sandbox_file_snapshot_under_policy(apply_result.sandbox_root_ref, expected_state.target_path_ref, active_policy)
        total_read += actual_state.bytes_read
        if total_read > active_policy.max_total_read_chars:
            raise ValueError("sandbox validation read bound exceeded")
        target_path = validate_sandbox_validation_path_containment(apply_result.sandbox_root_ref, expected_state.target_path_ref)
        if actual_state.file_exists:
            actual_state = build_sandbox_actual_file_state(
                actual_state_id=actual_state.actual_state_id,
                sandbox_path_ref=actual_state.sandbox_path_ref,
                actual_content_preview=actual_state.actual_content_preview,
                actual_content_hash=actual_state.actual_content_hash,
                actual_summary=actual_state.actual_summary,
                file_exists=actual_state.file_exists,
                bytes_read=actual_state.bytes_read,
                redacted=actual_state.redacted,
                truncated=actual_state.truncated,
                metadata={"full_text": target_path.read_text(encoding="utf-8")[: active_policy.max_file_read_chars]},
            )
        actual_states.append(actual_state)
        safety_findings.extend(scan_sandbox_file_static_safety(actual_state, active_policy).findings)
    reconciliation_report = reconcile_sandbox_apply_result(apply_result, expected_states, actual_states)
    scope_report = validate_sandbox_scope_after_apply(apply_result, active_policy)
    static_findings = [
        build_sandbox_validation_finding(
            finding_id=f"sandbox_validation_finding:v0.36.5:safety:{index}",
            check_kind=SandboxValidationCheckKind.NO_UNSAFE_READINESS_FLAG_CHECK,
            risk_kind=finding.risk_kind,
            severity=finding.severity,
            summary=finding.summary,
            evidence_preview=finding.evidence_preview,
            blocks_future_agentic_task_input=_high_or_blocking(finding.severity),
        )
        for index, finding in enumerate(safety_findings, start=1)
    ]
    for index, finding in enumerate(scope_report.findings, start=1):
        static_findings.append(
            build_sandbox_validation_finding(
                finding_id=f"sandbox_validation_finding:v0.36.5:scope:{index}",
                check_kind=SandboxValidationCheckKind.SANDBOX_PATH_CONTAINMENT_CHECK,
                risk_kind=finding.risk_kind,
                severity=finding.severity,
                summary=finding.summary,
                evidence_preview=finding.sandbox_path_ref,
                blocks_future_agentic_task_input=True,
            )
        )
    safety_report = build_sandbox_safety_regression_report(findings=safety_findings)
    static_report = build_sandbox_static_validation_report(findings=static_findings)
    successful = (
        apply_result.sandbox_apply_successful
        and reconciliation_report.matches_expected
        and static_report.static_validation_successful
        and not safety_report.safety_regression_detected
        and scope_report.scope_valid
    )
    return build_sandbox_post_apply_validation_report(
        validation_input_id=validation_input.validation_input_id,
        sandbox_apply_result_id=apply_result.sandbox_apply_result_id,
        reconciliation_report=reconciliation_report,
        static_validation_report=static_report,
        safety_regression_report=safety_report,
        scope_validation_report=scope_report,
        validation_successful=successful,
    )


def validate_sandbox_post_apply_validation_report(
    report: SandboxPostApplyValidationReport,
) -> SandboxStaticValidationReport:
    findings: list[SandboxValidationFinding] = []
    if report.test_execution_performed:
        findings.append(
            build_sandbox_validation_finding(
                finding_id="sandbox_validation_finding:v0.36.5:test_execution_reported",
                check_kind=SandboxValidationCheckKind.NO_TEST_EXECUTION_CHECK,
                risk_kind=SandboxValidationRiskKind.TEST_EXECUTION_OPENING_RISK,
                summary="post-apply validation report claimed test execution",
            )
        )
    if report.sandbox_file_write_performed or report.live_workspace_write_performed:
        findings.append(
            build_sandbox_validation_finding(
                finding_id="sandbox_validation_finding:v0.36.5:write_reported",
                check_kind=SandboxValidationCheckKind.NO_OUTSIDE_SANDBOX_WRITE_CHECK,
                risk_kind=SandboxValidationRiskKind.LIVE_WORKSPACE_WRITE_RISK,
                summary="post-apply validation report claimed file write",
            )
        )
    return build_sandbox_static_validation_report(
        findings=findings,
        static_validation_successful=not findings,
        summary="validated post-apply validation report remains read-only and not test execution",
    )


def sandbox_post_apply_flags_preserve_no_write_no_test(flags: SandboxPostApplyValidationFlagSet) -> bool:
    return isinstance(flags, SandboxPostApplyValidationFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def sandbox_post_apply_policy_blocks_write_test(policy: SandboxPostApplyValidationPolicy) -> bool:
    return not any(
        getattr(policy, name)
        for name in (
            "allow_sandbox_file_write",
            "allow_live_workspace_write",
            "allow_patch_application",
            "allow_workspace_write",
            "allow_code_edit",
            "allow_apply_patch",
            "allow_git_apply",
            "allow_test_execution",
            "allow_shell",
            "allow_dependency_install",
            "allow_external_agent_execution",
            "allow_dominion_runtime",
            "allow_automatic_repair",
            "allow_multi_cycle_repair_loop",
        )
    )


def sandbox_validation_report_is_not_test_execution(report: SandboxPostApplyValidationReport) -> bool:
    return not any(
        getattr(report, name)
        for name in (
            "test_execution_performed",
            "live_workspace_write_performed",
            "sandbox_file_write_performed",
            "patch_application_performed",
            "automatic_repair_performed",
            "production_certified",
            "ready_for_execution",
        )
    )


def sandbox_reconciliation_report_is_not_repair(report: SandboxProposalReconciliationReport) -> bool:
    return report.repair_triggered is False and all(finding.repair_triggered is False for finding in report.findings)


def sandbox_post_apply_decision_is_not_apply_permission(decision: SandboxPostApplyValidationDecision) -> bool:
    return not any(
        getattr(decision, name)
        for name in (
            "allow_repair",
            "allow_write",
            "allow_apply",
            "allow_test_execution",
            "allow_shell",
            "allow_external_agent_execution",
            "allow_dominion_runtime",
        )
    )


def v0365_readiness_report_is_not_execution_ready(report: V0365ReadinessReport) -> bool:
    return isinstance(report, V0365ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
