from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_sandbox import (
    SandboxOverlayEntry,
    SandboxWorkspaceManifest,
    SandboxWorkspacePlan,
    SandboxWorkspacePolicy,
    normalize_sandbox_relative_path_ref,
)


V0364_VERSION = "v0.36.4"
V0364_RELEASE_NAME = "v0.36.4 Sandbox Patch Apply Engine"
MAX_CONTENT_CHARS = 12000
MAX_PREVIEW_CHARS = 600

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
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
    "live_write",
    "apply_patch",
    "git_apply",
    "shell",
    "test_execution",
    "dependency_install",
    "external_agent_execution",
    "dominion_runtime",
)


class SandboxPatchApplyMode(StrEnum):
    MATERIALIZE_FROM_DRY_RUN_RESULT = "materialize_from_dry_run_result"
    MATERIALIZE_FROM_OVERLAY_MANIFEST = "materialize_from_overlay_manifest"
    SANDBOX_APPLY_STRUCTURED_PATCH = "sandbox_apply_structured_patch"
    SANDBOX_APPLY_UNIFIED_DIFF_AFTER_DRY_RUN = "sandbox_apply_unified_diff_after_dry_run"
    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxPatchApplySourceKind(StrEnum):
    V0363_SANDBOX_WORKSPACE_MANIFEST = "v0363_sandbox_workspace_manifest"
    V0363_SANDBOX_WORKSPACE_PLAN = "v0363_sandbox_workspace_plan"
    V0363_SANDBOX_WORKSPACE_POLICY = "v0363_sandbox_workspace_policy"
    V0362_DRY_RUN_APPLY_SIMULATION_RESULT = "v0362_dry_run_apply_simulation_result"
    V0362_SIMULATED_FILE_RESULT = "v0362_simulated_file_result"
    V0362_SIMULATED_FILE_DELTA = "v0362_simulated_file_delta"
    V0361_APPLY_CANDIDATE_ENVELOPE = "v0361_apply_candidate_envelope"
    V0361_HUMAN_APPROVAL_CONTRACT = "v0361_human_approval_contract"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxPatchApplyStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    MATERIALIZATION_PLANNED = "materialization_planned"
    SANDBOX_MATERIALIZED = "sandbox_materialized"
    SANDBOX_APPLY_COMPLETED = "sandbox_apply_completed"
    SANDBOX_APPLY_COMPLETED_WITH_WARNINGS = "sandbox_apply_completed_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxPatchApplyReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SANDBOX_APPLY_CONTRACT_READY = "sandbox_apply_contract_ready"
    SANDBOX_MATERIALIZATION_READY = "sandbox_materialization_ready"
    SANDBOX_FILE_WRITE_READY = "sandbox_file_write_ready"
    SANDBOX_APPLY_RESULT_READY = "sandbox_apply_result_ready"
    DESIGN_HANDOFF_READY_FOR_V0365 = "design_handoff_ready_for_v0365"
    DESIGN_HANDOFF_READY_FOR_V0366 = "design_handoff_ready_for_v0366"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxPatchApplyDecisionKind(StrEnum):
    ALLOW_SANDBOX_MATERIALIZATION = "allow_sandbox_materialization"
    ALLOW_SANDBOX_FILE_WRITE = "allow_sandbox_file_write"
    ALLOW_SANDBOX_PATCH_APPLY = "allow_sandbox_patch_apply"
    ALLOW_FUTURE_POST_APPLY_VALIDATION_INPUT = "allow_future_post_apply_validation_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxPatchApplyRiskKind(StrEnum):
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    SANDBOX_ESCAPE_RISK = "sandbox_escape_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    OUTSIDE_ROOT_WRITE_RISK = "outside_root_write_risk"
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    ABSOLUTE_PATH_RISK = "absolute_path_risk"
    REFERENCE_ROOT_WRITE_RISK = "reference_root_write_risk"
    SECRET_PATH_RISK = "secret_path_risk"
    CREDENTIAL_PATH_RISK = "credential_path_risk"
    BINARY_TARGET_RISK = "binary_target_risk"
    UNRESOLVED_DRY_RUN_CONFLICT_RISK = "unresolved_dry_run_conflict_risk"
    STALE_MANIFEST_RISK = "stale_manifest_risk"
    PARTIAL_APPLY_RISK = "partial_apply_risk"
    WRITE_RECORD_MISSING_RISK = "write_record_missing_risk"
    PATCH_APPLY_CONFUSION_RISK = "patch_apply_confusion_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class SandboxMaterializationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_MATERIALIZED = "not_materialized"
    PLANNED = "planned"
    MATERIALIZED = "materialized"
    MATERIALIZED_WITH_WARNINGS = "materialized_with_warnings"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    SAFE_FAILED = "safe_failed"


class SandboxFileWriteKind(StrEnum):
    CREATE_SANDBOX_FILE = "create_sandbox_file"
    OVERWRITE_SANDBOX_FILE = "overwrite_sandbox_file"
    UPDATE_SANDBOX_FILE = "update_sandbox_file"
    CREATE_SANDBOX_DIRECTORY = "create_sandbox_directory"
    WRITE_SANDBOX_MANIFEST_COPY = "write_sandbox_manifest_copy"
    BLOCKED_LIVE_WRITE = "blocked_live_write"
    BLOCKED_REFERENCE_WRITE = "blocked_reference_write"
    BLOCKED_OUTSIDE_ROOT_WRITE = "blocked_outside_root_write"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxFileWriteStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    WRITTEN = "written"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    FAILED_SAFE = "failed_safe"
    NO_OP = "no_op"


class SandboxPatchEngineStrategy(StrEnum):
    WRITE_SIMULATED_AFTER_CONTENT = "write_simulated_after_content"
    APPLY_STRUCTURED_PATCH_IN_MEMORY_THEN_WRITE_SANDBOX = "apply_structured_patch_in_memory_then_write_sandbox"
    APPLY_UNIFIED_DIFF_IN_MEMORY_THEN_WRITE_SANDBOX = "apply_unified_diff_in_memory_then_write_sandbox"
    MATERIALIZE_OVERLAY_ENTRIES = "materialize_overlay_entries"
    METADATA_ONLY = "metadata_only"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class SandboxPatchEngineStatus(StrEnum):
    UNKNOWN = "unknown"
    INITIALIZED = "initialized"
    VALIDATED = "validated"
    APPLIED_TO_SANDBOX = "applied_to_sandbox"
    APPLIED_TO_SANDBOX_WITH_WARNINGS = "applied_to_sandbox_with_warnings"
    BLOCKED = "blocked"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0364_VERSION not in version:
        raise ValueError("version must include v0.36.4")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.4")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _bounded_text(value: str, max_chars: int = MAX_CONTENT_CHARS) -> str:
    if not isinstance(value, str):
        raise TypeError("content value must be str")
    if len(value) > max_chars:
        raise ValueError("content value exceeds sandbox apply bound")
    return value


def _bounded_preview(value: str, max_chars: int = MAX_PREVIEW_CHARS) -> str:
    text = _bounded_text(value)
    redacted = text
    for token in ("secret", "credential", "api_key", "token", "password"):
        redacted = redacted.replace(token, "[redacted]")
        redacted = redacted.replace(token.upper(), "[redacted]")
    return redacted[:max_chars]


def _looks_reference_or_live_root(path_ref: str) -> bool:
    lowered = path_ref.replace("\\", "/").lower()
    parts = [part for part in lowered.split("/") if part]
    return any(part in {"references", "opencode", "hermes", "openclaw", ".git", "workspace", "live"} for part in parts)


def _is_bad_root(path_ref: str) -> bool:
    stripped = path_ref.strip()
    return not stripped or _looks_reference_or_live_root(stripped)


@dataclass(frozen=True)
class SandboxPatchApplyFlagSet:
    flag_set_id: str
    version: str
    sandbox_patch_apply_engine_constructed: bool
    sandbox_materialization_available: bool
    sandbox_file_write_available: bool
    sandbox_patch_apply_available: bool
    sandbox_write_record_available: bool
    sandbox_apply_result_available: bool
    ready_for_v0365_sandbox_post_apply_validation: bool
    ready_for_v0366_bounded_agentic_task_operation_cycle: bool
    ready_for_sandbox_workspace_materialization: bool
    ready_for_sandbox_workspace_write: bool
    ready_for_sandbox_patch_apply: bool
    ready_for_sandbox_file_materialization: bool
    ready_for_sandbox_patch_apply_result: bool
    ready_for_future_post_apply_validation_input: bool
    ready_for_execution: bool = False
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
class SandboxPatchApplySourceRef:
    source_ref_id: str
    source_kind: SandboxPatchApplySourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxPatchApplySourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyPolicy:
    apply_policy_id: str
    version: str
    allowed_modes: list[SandboxPatchApplyMode | str]
    blocked_modes: list[SandboxPatchApplyMode | str]
    allowed_engine_strategies: list[SandboxPatchEngineStrategy | str]
    blocked_engine_strategies: list[SandboxPatchEngineStrategy | str]
    max_files: int
    max_total_write_chars: int
    max_file_write_chars: int
    require_valid_manifest: bool
    require_successful_dry_run: bool
    require_human_approval_contract: bool
    require_no_blocking_conflicts: bool
    require_sandbox_root: bool
    require_write_records: bool
    allow_sandbox_directory_creation: bool
    allow_sandbox_file_write: bool
    allow_sandbox_patch_apply: bool
    allow_partial_safe_apply: bool
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
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("apply_policy_id", self.apply_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, SandboxPatchApplyMode)
        _validate_enum_list("blocked_modes", self.blocked_modes, SandboxPatchApplyMode)
        _validate_enum_list("allowed_engine_strategies", self.allowed_engine_strategies, SandboxPatchEngineStrategy)
        _validate_enum_list("blocked_engine_strategies", self.blocked_engine_strategies, SandboxPatchEngineStrategy)
        for name in ("max_files", "max_total_write_chars", "max_file_write_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(
            self,
            (
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
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyInput:
    sandbox_apply_input_id: str
    version: str
    manifest_id: str | None
    workspace_plan_id: str | None
    dry_run_result_id: str | None
    apply_candidate_id: str | None
    human_approval_contract_id: str | None
    requested_mode: SandboxPatchApplyMode | str
    engine_strategy: SandboxPatchEngineStrategy | str
    sandbox_root_ref: str
    source_refs: list[SandboxPatchApplySourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("sandbox_apply_input_id", "sandbox_root_ref", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxPatchApplyMode(self.requested_mode)
        SandboxPatchEngineStrategy(self.engine_strategy)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_RUNTIME_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing {missing}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxDirectoryMaterializationPlan:
    directory_plan_id: str
    sandbox_path_ref: str
    directory_summary: str
    create_directory: bool
    blocked: bool
    block_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("directory_plan_id", "sandbox_path_ref", "directory_summary"):
            _require_non_blank(name, getattr(self, name))
        if self.blocked and not self.block_reason:
            raise ValueError("blocked directory plan must include block_reason")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxFileMaterializationPlan:
    file_plan_id: str
    sandbox_path_ref: str
    source_overlay_entry_id: str | None
    source_simulated_file_result_id: str | None
    file_summary: str
    content_preview: str
    content_length: int
    write_kind: SandboxFileWriteKind | str
    ready_for_sandbox_write: bool
    ready_for_live_write: bool = False
    blocked: bool = False
    block_reason: str | None = None
    redacted: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("file_plan_id", "sandbox_path_ref", "file_summary"):
            _require_non_blank(name, getattr(self, name))
        if _bounded_preview(self.content_preview) != self.content_preview:
            raise ValueError("content_preview must be bounded and redacted")
        if self.content_length < 0:
            raise ValueError("content_length must be >= 0")
        SandboxFileWriteKind(self.write_kind)
        _validate_false(self, ("ready_for_live_write",))
        if self.blocked and not self.block_reason:
            raise ValueError("blocked file plan must include block_reason")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxMaterializationPlan:
    materialization_plan_id: str
    version: str
    sandbox_apply_input_id: str
    sandbox_root_ref: str
    directory_plans: list[SandboxDirectoryMaterializationPlan]
    file_plans: list[SandboxFileMaterializationPlan]
    materialization_summary: str
    ready_for_materialization: bool
    ready_for_live_write: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("materialization_plan_id", "sandbox_apply_input_id", "sandbox_root_ref", "materialization_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("directory_plans", self.directory_plans)
        _validate_list("file_plans", self.file_plans)
        _validate_false(self, ("ready_for_live_write", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxFileWriteOperation:
    write_operation_id: str
    file_plan_id: str
    sandbox_root_ref: str
    sandbox_path_ref: str
    write_kind: SandboxFileWriteKind | str
    content_text: str
    content_summary: str
    allowed_under_policy: bool
    live_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("write_operation_id", "file_plan_id", "sandbox_root_ref", "sandbox_path_ref", "content_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxFileWriteKind(self.write_kind)
        _bounded_text(self.content_text)
        _validate_false(self, ("live_write",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxFileWriteRecord:
    write_record_id: str
    write_operation_id: str
    sandbox_root_ref: str
    sandbox_path_ref: str
    write_status: SandboxFileWriteStatus | str
    bytes_written: int
    write_summary: str
    live_write: bool = False
    wrote_outside_sandbox: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("write_record_id", "write_operation_id", "sandbox_root_ref", "sandbox_path_ref", "write_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxFileWriteStatus(self.write_status)
        if self.bytes_written < 0:
            raise ValueError("bytes_written must be >= 0")
        _validate_false(self, ("live_write", "wrote_outside_sandbox"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchEngineOperation:
    engine_operation_id: str
    sandbox_apply_input_id: str
    engine_strategy: SandboxPatchEngineStrategy | str
    file_write_operations: list[SandboxFileWriteOperation]
    operation_summary: str
    allowed_under_policy: bool
    used_apply_patch: bool = False
    used_git_apply: bool = False
    used_shell: bool = False
    live_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("engine_operation_id", "sandbox_apply_input_id", "operation_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxPatchEngineStrategy(self.engine_strategy)
        _validate_list("file_write_operations", self.file_write_operations)
        _validate_false(self, ("used_apply_patch", "used_git_apply", "used_shell", "live_write"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchEngineFileResult:
    engine_file_result_id: str
    sandbox_path_ref: str
    source_file_plan_id: str | None
    write_records: list[SandboxFileWriteRecord]
    file_result_summary: str
    materialization_status: SandboxMaterializationStatus | str
    write_status: SandboxFileWriteStatus | str
    sandbox_write_successful: bool
    live_write: bool = False
    ready_for_live_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("engine_file_result_id", "sandbox_path_ref", "file_result_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("write_records", self.write_records)
        SandboxMaterializationStatus(self.materialization_status)
        SandboxFileWriteStatus(self.write_status)
        _validate_false(self, ("live_write", "ready_for_live_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyResult:
    sandbox_apply_result_id: str
    version: str
    sandbox_apply_input_id: str
    mode: SandboxPatchApplyMode | str
    status: SandboxPatchApplyStatus | str
    readiness_level: SandboxPatchApplyReadinessLevel | str
    sandbox_root_ref: str
    materialization_plan: SandboxMaterializationPlan
    engine_operation: SandboxPatchEngineOperation
    file_results: list[SandboxPatchEngineFileResult]
    write_records: list[SandboxFileWriteRecord]
    source_refs: list[SandboxPatchApplySourceRef]
    summary: str
    files_written_count: int
    bytes_written_total: int
    sandbox_apply_successful: bool
    live_write_performed: bool = False
    used_apply_patch: bool = False
    used_git_apply: bool = False
    used_shell: bool = False
    ready_for_v0365_sandbox_post_apply_validation: bool = False
    ready_for_v0366_bounded_agentic_task_operation_cycle: bool = False
    ready_for_future_post_apply_validation_input: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("sandbox_apply_result_id", "sandbox_apply_input_id", "sandbox_root_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxPatchApplyMode(self.mode)
        SandboxPatchApplyStatus(self.status)
        SandboxPatchApplyReadinessLevel(self.readiness_level)
        if not isinstance(self.materialization_plan, SandboxMaterializationPlan):
            raise TypeError("materialization_plan must be SandboxMaterializationPlan")
        if not isinstance(self.engine_operation, SandboxPatchEngineOperation):
            raise TypeError("engine_operation must be SandboxPatchEngineOperation")
        for name in ("file_results", "write_records", "source_refs"):
            _validate_list(name, getattr(self, name))
        for name in ("files_written_count", "bytes_written_total"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(
            self,
            (
                "live_write_performed",
                "used_apply_patch",
                "used_git_apply",
                "used_shell",
                "ready_for_live_workspace_write",
                "ready_for_patch_application",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyDecision:
    decision_id: str
    decision_kind: SandboxPatchApplyDecisionKind | str
    status: SandboxPatchApplyStatus | str
    summary: str
    allow_sandbox_materialization: bool
    allow_sandbox_file_write: bool
    allow_sandbox_patch_apply: bool
    allow_live_workspace_write: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_shell: bool = False
    allow_test_execution: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxPatchApplyDecisionKind(self.decision_kind)
        SandboxPatchApplyStatus(self.status)
        _validate_false(
            self,
            (
                "allow_live_workspace_write",
                "allow_apply_patch",
                "allow_git_apply",
                "allow_shell",
                "allow_test_execution",
                "allow_external_agent_execution",
                "allow_dominion_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyValidationFinding:
    finding_id: str
    risk_kind: SandboxPatchApplyRiskKind | str
    decision_kind: SandboxPatchApplyDecisionKind | str
    summary: str
    blocks_future_validation: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxPatchApplyRiskKind(self.risk_kind)
        SandboxPatchApplyDecisionKind(self.decision_kind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyValidationReport:
    validation_report_id: str
    sandbox_apply_result_id: str
    findings: list[SandboxPatchApplyValidationFinding]
    status: SandboxPatchApplyStatus | str
    summary: str
    verified_no_live_write: bool
    verified_no_outside_sandbox_write: bool
    verified_no_apply_patch: bool
    verified_no_git_apply: bool
    verified_no_shell: bool
    ready_for_future_post_apply_validation_input: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "sandbox_apply_result_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("findings", self.findings)
        SandboxPatchApplyStatus(self.status)
        for name in (
            "verified_no_live_write",
            "verified_no_outside_sandbox_write",
            "verified_no_apply_patch",
            "verified_no_git_apply",
            "verified_no_shell",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.4")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyReport:
    report_id: str
    apply_result: SandboxPatchApplyResult
    validation_report: SandboxPatchApplyValidationReport
    decision: SandboxPatchApplyDecision
    summary: str
    sandbox_apply_successful: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        if not isinstance(self.apply_result, SandboxPatchApplyResult):
            raise TypeError("apply_result must be SandboxPatchApplyResult")
        if not isinstance(self.validation_report, SandboxPatchApplyValidationReport):
            raise TypeError("validation_report must be SandboxPatchApplyValidationReport")
        if not isinstance(self.decision, SandboxPatchApplyDecision):
            raise TypeError("decision must be SandboxPatchApplyDecision")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyRunPreview:
    run_preview_id: str
    sandbox_apply_input_id: str
    preview_summary: str
    planned_sandbox_actions: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_sandbox_patch_apply: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "sandbox_apply_input_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("planned_sandbox_actions", self.planned_sandbox_actions)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPatchApplyNoLiveWriteGuarantee:
    guarantee_id: str
    version: str
    no_live_workspace_write: bool
    no_live_code_edit: bool
    no_unrestricted_patch_application: bool
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
    no_sandbox_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and name != "no_sandbox_write" and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.4")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0364ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    status: SandboxPatchApplyStatus | str
    readiness_level: SandboxPatchApplyReadinessLevel | str
    ready_for_v0365_sandbox_post_apply_validation: bool
    ready_for_v0366_bounded_agentic_task_operation_cycle: bool
    ready_for_sandbox_workspace_materialization: bool
    ready_for_sandbox_workspace_write: bool
    ready_for_sandbox_patch_apply: bool
    ready_for_sandbox_file_materialization: bool
    ready_for_sandbox_patch_apply_result: bool
    ready_for_future_post_apply_validation_input: bool
    digestion_first_policy_applied: bool
    dominion_runtime_blocked: bool
    external_agent_execution_blocked: bool
    infinite_agent_loop_blocked: bool
    bounded_agentic_task_only: bool
    no_independent_autonomous_agent_runtime: bool
    ready_for_execution: bool = False
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
    summary: str = "v0.36.4 sandbox patch apply engine is sandbox-only"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxPatchApplyStatus(self.status)
        SandboxPatchApplyReadinessLevel(self.readiness_level)
        for name in (
            "digestion_first_policy_applied",
            "dominion_runtime_blocked",
            "external_agent_execution_blocked",
            "infinite_agent_loop_blocked",
            "bounded_agentic_task_only",
            "no_independent_autonomous_agent_runtime",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.4")
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_sandbox_patch_apply_flags(**kwargs: Any) -> SandboxPatchApplyFlagSet:
    return SandboxPatchApplyFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_patch_apply_flags:v0.36.4"),
        version=kwargs.pop("version", V0364_VERSION),
        sandbox_patch_apply_engine_constructed=kwargs.pop("sandbox_patch_apply_engine_constructed", True),
        sandbox_materialization_available=kwargs.pop("sandbox_materialization_available", True),
        sandbox_file_write_available=kwargs.pop("sandbox_file_write_available", True),
        sandbox_patch_apply_available=kwargs.pop("sandbox_patch_apply_available", True),
        sandbox_write_record_available=kwargs.pop("sandbox_write_record_available", True),
        sandbox_apply_result_available=kwargs.pop("sandbox_apply_result_available", True),
        ready_for_v0365_sandbox_post_apply_validation=kwargs.pop("ready_for_v0365_sandbox_post_apply_validation", True),
        ready_for_v0366_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_v0366_bounded_agentic_task_operation_cycle", True),
        ready_for_sandbox_workspace_materialization=kwargs.pop("ready_for_sandbox_workspace_materialization", True),
        ready_for_sandbox_workspace_write=kwargs.pop("ready_for_sandbox_workspace_write", True),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        ready_for_sandbox_file_materialization=kwargs.pop("ready_for_sandbox_file_materialization", True),
        ready_for_sandbox_patch_apply_result=kwargs.pop("ready_for_sandbox_patch_apply_result", True),
        ready_for_future_post_apply_validation_input=kwargs.pop("ready_for_future_post_apply_validation_input", True),
        **kwargs,
    )


def build_sandbox_patch_apply_source_ref(**kwargs: Any) -> SandboxPatchApplySourceRef:
    return SandboxPatchApplySourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_apply_source:v0.36.4:manifest"),
        source_kind=kwargs.pop("source_kind", SandboxPatchApplySourceKind.V0363_SANDBOX_WORKSPACE_MANIFEST),
        source_id=kwargs.pop("source_id", "sandbox_manifest:v0.36.3"),
        source_summary=kwargs.pop("source_summary", "sandbox manifest metadata source; not live write"),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.3_sandbox_workspace_overlay_policy.md"]),
        **kwargs,
    )


def build_sandbox_patch_apply_policy(**kwargs: Any) -> SandboxPatchApplyPolicy:
    return SandboxPatchApplyPolicy(
        apply_policy_id=kwargs.pop("apply_policy_id", "sandbox_patch_apply_policy:v0.36.4"),
        version=kwargs.pop("version", V0364_VERSION),
        allowed_modes=kwargs.pop(
            "allowed_modes",
            [SandboxPatchApplyMode.MATERIALIZE_FROM_OVERLAY_MANIFEST, SandboxPatchApplyMode.MATERIALIZE_FROM_DRY_RUN_RESULT],
        ),
        blocked_modes=kwargs.pop("blocked_modes", [SandboxPatchApplyMode.UNKNOWN, SandboxPatchApplyMode.BLOCKED]),
        allowed_engine_strategies=kwargs.pop(
            "allowed_engine_strategies",
            [SandboxPatchEngineStrategy.WRITE_SIMULATED_AFTER_CONTENT, SandboxPatchEngineStrategy.MATERIALIZE_OVERLAY_ENTRIES],
        ),
        blocked_engine_strategies=kwargs.pop(
            "blocked_engine_strategies",
            [SandboxPatchEngineStrategy.UNKNOWN, SandboxPatchEngineStrategy.BLOCKED],
        ),
        max_files=kwargs.pop("max_files", 100),
        max_total_write_chars=kwargs.pop("max_total_write_chars", MAX_CONTENT_CHARS * 100),
        max_file_write_chars=kwargs.pop("max_file_write_chars", MAX_CONTENT_CHARS),
        require_valid_manifest=kwargs.pop("require_valid_manifest", True),
        require_successful_dry_run=kwargs.pop("require_successful_dry_run", True),
        require_human_approval_contract=kwargs.pop("require_human_approval_contract", True),
        require_no_blocking_conflicts=kwargs.pop("require_no_blocking_conflicts", True),
        require_sandbox_root=kwargs.pop("require_sandbox_root", True),
        require_write_records=kwargs.pop("require_write_records", True),
        allow_sandbox_directory_creation=kwargs.pop("allow_sandbox_directory_creation", True),
        allow_sandbox_file_write=kwargs.pop("allow_sandbox_file_write", True),
        allow_sandbox_patch_apply=kwargs.pop("allow_sandbox_patch_apply", True),
        allow_partial_safe_apply=kwargs.pop("allow_partial_safe_apply", False),
        **kwargs,
    )


def default_sandbox_patch_apply_policy(**kwargs: Any) -> SandboxPatchApplyPolicy:
    return build_sandbox_patch_apply_policy(**kwargs)


def build_sandbox_patch_apply_input(**kwargs: Any) -> SandboxPatchApplyInput:
    return SandboxPatchApplyInput(
        sandbox_apply_input_id=kwargs.pop("sandbox_apply_input_id", "sandbox_patch_apply_input:v0.36.4"),
        version=kwargs.pop("version", V0364_VERSION),
        manifest_id=kwargs.pop("manifest_id", "sandbox_manifest:v0.36.3"),
        workspace_plan_id=kwargs.pop("workspace_plan_id", "sandbox_workspace_plan:v0.36.3"),
        dry_run_result_id=kwargs.pop("dry_run_result_id", "dry_run_result:v0.36.2"),
        apply_candidate_id=kwargs.pop("apply_candidate_id", "apply_candidate:v0.36.1"),
        human_approval_contract_id=kwargs.pop("human_approval_contract_id", "human_approval_contract:v0.36.1"),
        requested_mode=kwargs.pop("requested_mode", SandboxPatchApplyMode.MATERIALIZE_FROM_OVERLAY_MANIFEST),
        engine_strategy=kwargs.pop("engine_strategy", SandboxPatchEngineStrategy.WRITE_SIMULATED_AFTER_CONTENT),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "explicit-sandbox-root"),
        source_refs=kwargs.pop("source_refs", [build_sandbox_patch_apply_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "sandbox-only patch apply under validated sandbox root"),
        **kwargs,
    )


def build_sandbox_patch_apply_input_from_manifest(
    manifest: SandboxWorkspaceManifest,
    workspace_plan: SandboxWorkspacePlan | None = None,
    sandbox_root_ref: str | None = None,
    **kwargs: Any,
) -> SandboxPatchApplyInput:
    return build_sandbox_patch_apply_input(
        manifest_id=manifest.manifest_id,
        workspace_plan_id=workspace_plan.workspace_plan_id if workspace_plan else None,
        dry_run_result_id=str(manifest.metadata.get("dry_run_result_id")) if manifest.metadata.get("dry_run_result_id") else None,
        sandbox_root_ref=sandbox_root_ref or manifest.sandbox_root_ref,
        source_refs=[build_sandbox_patch_apply_source_ref(source_id=manifest.manifest_id)],
        **kwargs,
    )


def build_sandbox_directory_materialization_plan(**kwargs: Any) -> SandboxDirectoryMaterializationPlan:
    return SandboxDirectoryMaterializationPlan(
        directory_plan_id=kwargs.pop("directory_plan_id", "sandbox_directory_plan:v0.36.4"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src"),
        directory_summary=kwargs.pop("directory_summary", "create sandbox directory under sandbox root"),
        create_directory=kwargs.pop("create_directory", True),
        blocked=kwargs.pop("blocked", False),
        **kwargs,
    )


def build_sandbox_file_materialization_plan(**kwargs: Any) -> SandboxFileMaterializationPlan:
    content = kwargs.pop("content_preview", "alpha\nBETA\ngamma")
    return SandboxFileMaterializationPlan(
        file_plan_id=kwargs.pop("file_plan_id", "sandbox_file_plan:v0.36.4"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        source_overlay_entry_id=kwargs.pop("source_overlay_entry_id", "sandbox_overlay_entry:v0.36.3:src_example"),
        source_simulated_file_result_id=kwargs.pop("source_simulated_file_result_id", None),
        file_summary=kwargs.pop("file_summary", "write simulated after-content to sandbox file"),
        content_preview=content,
        content_length=kwargs.pop("content_length", len(content)),
        write_kind=kwargs.pop("write_kind", SandboxFileWriteKind.CREATE_SANDBOX_FILE),
        ready_for_sandbox_write=kwargs.pop("ready_for_sandbox_write", True),
        **kwargs,
    )


def build_sandbox_materialization_plan(**kwargs: Any) -> SandboxMaterializationPlan:
    return SandboxMaterializationPlan(
        materialization_plan_id=kwargs.pop("materialization_plan_id", "sandbox_materialization_plan:v0.36.4"),
        version=kwargs.pop("version", V0364_VERSION),
        sandbox_apply_input_id=kwargs.pop("sandbox_apply_input_id", "sandbox_patch_apply_input:v0.36.4"),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "explicit-sandbox-root"),
        directory_plans=kwargs.pop("directory_plans", [build_sandbox_directory_materialization_plan()]),
        file_plans=kwargs.pop("file_plans", [build_sandbox_file_materialization_plan()]),
        materialization_summary=kwargs.pop("materialization_summary", "sandbox materialization plan; no live write"),
        ready_for_materialization=kwargs.pop("ready_for_materialization", True),
        **kwargs,
    )


def build_sandbox_materialization_plan_from_manifest(
    manifest: SandboxWorkspaceManifest,
    sandbox_apply_input: SandboxPatchApplyInput | None = None,
    **kwargs: Any,
) -> SandboxMaterializationPlan:
    active_input = sandbox_apply_input or build_sandbox_patch_apply_input_from_manifest(manifest)
    if not manifest.ready_for_future_materialization_input:
        return build_sandbox_materialization_plan(
            sandbox_apply_input_id=active_input.sandbox_apply_input_id,
            sandbox_root_ref=active_input.sandbox_root_ref,
            directory_plans=[],
            file_plans=[],
            ready_for_materialization=False,
            materialization_summary="manifest is not ready for sandbox materialization",
            metadata={"blocked_manifest": True},
            **kwargs,
        )
    directory_paths: set[str] = set()
    file_plans: list[SandboxFileMaterializationPlan] = []
    overlays_by_target = {entry.target_path_ref: entry for entry in manifest.overlay_entries}
    for index, file_map in enumerate(manifest.file_map_entries, start=1):
        if not file_map.eligible_for_future_materialization:
            continue
        overlay = overlays_by_target.get(file_map.target_path_ref)
        content = overlay.simulated_after_preview if overlay else ""
        path = normalize_sandbox_relative_path_ref(file_map.target_path_ref)
        parent = "/".join(path.split("/")[:-1])
        if parent:
            directory_paths.add(parent)
        file_plans.append(
            build_sandbox_file_materialization_plan(
                file_plan_id=f"sandbox_file_plan:v0.36.4:{index}",
                sandbox_path_ref=path,
                source_overlay_entry_id=overlay.overlay_entry_id if overlay else None,
                file_summary="materialize overlay after-content into sandbox file only",
                content_preview=_bounded_preview(content),
                content_length=len(content),
                metadata={"content_text": content},
            )
        )
    directory_plans = [
        build_sandbox_directory_materialization_plan(
            directory_plan_id=f"sandbox_directory_plan:v0.36.4:{index}",
            sandbox_path_ref=path,
        )
        for index, path in enumerate(sorted(directory_paths), start=1)
    ]
    return build_sandbox_materialization_plan(
        sandbox_apply_input_id=active_input.sandbox_apply_input_id,
        sandbox_root_ref=active_input.sandbox_root_ref,
        directory_plans=directory_plans,
        file_plans=file_plans,
        ready_for_materialization=bool(file_plans),
        metadata={"manifest_id": manifest.manifest_id},
        **kwargs,
    )


def build_sandbox_file_write_operation(**kwargs: Any) -> SandboxFileWriteOperation:
    return SandboxFileWriteOperation(
        write_operation_id=kwargs.pop("write_operation_id", "sandbox_write_operation:v0.36.4"),
        file_plan_id=kwargs.pop("file_plan_id", "sandbox_file_plan:v0.36.4"),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "explicit-sandbox-root"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        write_kind=kwargs.pop("write_kind", SandboxFileWriteKind.CREATE_SANDBOX_FILE),
        content_text=kwargs.pop("content_text", "alpha\nBETA\ngamma"),
        content_summary=kwargs.pop("content_summary", "sandbox-only write operation"),
        allowed_under_policy=kwargs.pop("allowed_under_policy", True),
        **kwargs,
    )


def build_sandbox_file_write_record(**kwargs: Any) -> SandboxFileWriteRecord:
    return SandboxFileWriteRecord(
        write_record_id=kwargs.pop("write_record_id", "sandbox_write_record:v0.36.4"),
        write_operation_id=kwargs.pop("write_operation_id", "sandbox_write_operation:v0.36.4"),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "explicit-sandbox-root"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        write_status=kwargs.pop("write_status", SandboxFileWriteStatus.WRITTEN),
        bytes_written=kwargs.pop("bytes_written", 16),
        write_summary=kwargs.pop("write_summary", "sandbox-only file write recorded"),
        **kwargs,
    )


def build_sandbox_patch_engine_operation(**kwargs: Any) -> SandboxPatchEngineOperation:
    return SandboxPatchEngineOperation(
        engine_operation_id=kwargs.pop("engine_operation_id", "sandbox_engine_operation:v0.36.4"),
        sandbox_apply_input_id=kwargs.pop("sandbox_apply_input_id", "sandbox_patch_apply_input:v0.36.4"),
        engine_strategy=kwargs.pop("engine_strategy", SandboxPatchEngineStrategy.WRITE_SIMULATED_AFTER_CONTENT),
        file_write_operations=kwargs.pop("file_write_operations", [build_sandbox_file_write_operation()]),
        operation_summary=kwargs.pop("operation_summary", "internal Python sandbox write operation; no external tools"),
        allowed_under_policy=kwargs.pop("allowed_under_policy", True),
        **kwargs,
    )


def build_sandbox_patch_engine_file_result(**kwargs: Any) -> SandboxPatchEngineFileResult:
    return SandboxPatchEngineFileResult(
        engine_file_result_id=kwargs.pop("engine_file_result_id", "sandbox_engine_file_result:v0.36.4"),
        sandbox_path_ref=kwargs.pop("sandbox_path_ref", "src/example.py"),
        source_file_plan_id=kwargs.pop("source_file_plan_id", "sandbox_file_plan:v0.36.4"),
        write_records=kwargs.pop("write_records", [build_sandbox_file_write_record()]),
        file_result_summary=kwargs.pop("file_result_summary", "sandbox file materialized under validated root"),
        materialization_status=kwargs.pop("materialization_status", SandboxMaterializationStatus.MATERIALIZED),
        write_status=kwargs.pop("write_status", SandboxFileWriteStatus.WRITTEN),
        sandbox_write_successful=kwargs.pop("sandbox_write_successful", True),
        **kwargs,
    )


def build_sandbox_patch_apply_result(**kwargs: Any) -> SandboxPatchApplyResult:
    plan = kwargs.pop("materialization_plan", build_sandbox_materialization_plan())
    engine_operation = kwargs.pop("engine_operation", build_sandbox_patch_engine_operation())
    write_records = kwargs.pop("write_records", [build_sandbox_file_write_record()])
    file_results = kwargs.pop("file_results", [build_sandbox_patch_engine_file_result(write_records=write_records)])
    return SandboxPatchApplyResult(
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", "sandbox_apply_result:v0.36.4"),
        version=kwargs.pop("version", V0364_VERSION),
        sandbox_apply_input_id=kwargs.pop("sandbox_apply_input_id", "sandbox_patch_apply_input:v0.36.4"),
        mode=kwargs.pop("mode", SandboxPatchApplyMode.MATERIALIZE_FROM_OVERLAY_MANIFEST),
        status=kwargs.pop("status", SandboxPatchApplyStatus.SANDBOX_APPLY_COMPLETED),
        readiness_level=kwargs.pop("readiness_level", SandboxPatchApplyReadinessLevel.SANDBOX_APPLY_RESULT_READY),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "explicit-sandbox-root"),
        materialization_plan=plan,
        engine_operation=engine_operation,
        file_results=file_results,
        write_records=write_records,
        source_refs=kwargs.pop("source_refs", [build_sandbox_patch_apply_source_ref()]),
        summary=kwargs.pop("summary", "sandbox patch apply completed under validated sandbox root"),
        files_written_count=kwargs.pop("files_written_count", len(write_records)),
        bytes_written_total=kwargs.pop("bytes_written_total", sum(record.bytes_written for record in write_records)),
        sandbox_apply_successful=kwargs.pop("sandbox_apply_successful", True),
        ready_for_v0365_sandbox_post_apply_validation=kwargs.pop("ready_for_v0365_sandbox_post_apply_validation", True),
        ready_for_v0366_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_v0366_bounded_agentic_task_operation_cycle", True),
        ready_for_future_post_apply_validation_input=kwargs.pop("ready_for_future_post_apply_validation_input", True),
        **kwargs,
    )


def build_sandbox_patch_apply_decision(**kwargs: Any) -> SandboxPatchApplyDecision:
    return SandboxPatchApplyDecision(
        decision_id=kwargs.pop("decision_id", "sandbox_apply_decision:v0.36.4"),
        decision_kind=kwargs.pop("decision_kind", SandboxPatchApplyDecisionKind.ALLOW_SANDBOX_PATCH_APPLY),
        status=kwargs.pop("status", SandboxPatchApplyStatus.INPUT_VALIDATED),
        summary=kwargs.pop("summary", "sandbox-only materialization/write/apply allowed"),
        allow_sandbox_materialization=kwargs.pop("allow_sandbox_materialization", True),
        allow_sandbox_file_write=kwargs.pop("allow_sandbox_file_write", True),
        allow_sandbox_patch_apply=kwargs.pop("allow_sandbox_patch_apply", True),
        **kwargs,
    )


def build_sandbox_patch_apply_validation_finding(**kwargs: Any) -> SandboxPatchApplyValidationFinding:
    return SandboxPatchApplyValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_apply_validation_finding:v0.36.4"),
        risk_kind=kwargs.pop("risk_kind", SandboxPatchApplyRiskKind.PATCH_APPLY_CONFUSION_RISK),
        decision_kind=kwargs.pop("decision_kind", SandboxPatchApplyDecisionKind.REQUIRE_REVIEW),
        summary=kwargs.pop("summary", "sandbox apply validation metadata"),
        blocks_future_validation=kwargs.pop("blocks_future_validation", False),
        **kwargs,
    )


def build_sandbox_patch_apply_validation_report(**kwargs: Any) -> SandboxPatchApplyValidationReport:
    return SandboxPatchApplyValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_apply_validation_report:v0.36.4"),
        sandbox_apply_result_id=kwargs.pop("sandbox_apply_result_id", "sandbox_apply_result:v0.36.4"),
        findings=kwargs.pop("findings", []),
        status=kwargs.pop("status", SandboxPatchApplyStatus.SANDBOX_APPLY_COMPLETED),
        summary=kwargs.pop("summary", "validated sandbox-only apply result"),
        verified_no_live_write=kwargs.pop("verified_no_live_write", True),
        verified_no_outside_sandbox_write=kwargs.pop("verified_no_outside_sandbox_write", True),
        verified_no_apply_patch=kwargs.pop("verified_no_apply_patch", True),
        verified_no_git_apply=kwargs.pop("verified_no_git_apply", True),
        verified_no_shell=kwargs.pop("verified_no_shell", True),
        ready_for_future_post_apply_validation_input=kwargs.pop("ready_for_future_post_apply_validation_input", True),
        **kwargs,
    )


def build_sandbox_patch_apply_report(**kwargs: Any) -> SandboxPatchApplyReport:
    result = kwargs.pop("apply_result", build_sandbox_patch_apply_result())
    validation_report = kwargs.pop("validation_report", build_sandbox_patch_apply_validation_report(sandbox_apply_result_id=result.sandbox_apply_result_id))
    decision = kwargs.pop("decision", build_sandbox_patch_apply_decision())
    return SandboxPatchApplyReport(
        report_id=kwargs.pop("report_id", "sandbox_apply_report:v0.36.4"),
        apply_result=result,
        validation_report=validation_report,
        decision=decision,
        summary=kwargs.pop("summary", "sandbox apply report; not live apply"),
        sandbox_apply_successful=kwargs.pop("sandbox_apply_successful", result.sandbox_apply_successful),
        **kwargs,
    )


def build_sandbox_patch_apply_run_preview(**kwargs: Any) -> SandboxPatchApplyRunPreview:
    return SandboxPatchApplyRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_apply_run_preview:v0.36.4"),
        sandbox_apply_input_id=kwargs.pop("sandbox_apply_input_id", "sandbox_patch_apply_input:v0.36.4"),
        preview_summary=kwargs.pop("preview_summary", "preview of sandbox-only apply function"),
        planned_sandbox_actions=kwargs.pop("planned_sandbox_actions", ["create sandbox directories", "write sandbox files"]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        **kwargs,
    )


def build_sandbox_patch_apply_no_live_write_guarantee(**kwargs: Any) -> SandboxPatchApplyNoLiveWriteGuarantee:
    return SandboxPatchApplyNoLiveWriteGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_apply_no_live_write_guarantee:v0.36.4"),
        version=kwargs.pop("version", V0364_VERSION),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_live_code_edit=kwargs.pop("no_live_code_edit", True),
        no_unrestricted_patch_application=kwargs.pop("no_unrestricted_patch_application", True),
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
        no_sandbox_write=kwargs.pop("no_sandbox_write", False),
        **kwargs,
    )


def build_v0364_readiness_report(**kwargs: Any) -> V0364ReadinessReport:
    return V0364ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0364_readiness_report"),
        version=kwargs.pop("version", V0364_VERSION),
        release_name=kwargs.pop("release_name", V0364_RELEASE_NAME),
        status=kwargs.pop("status", SandboxPatchApplyStatus.SANDBOX_APPLY_COMPLETED),
        readiness_level=kwargs.pop("readiness_level", SandboxPatchApplyReadinessLevel.SANDBOX_APPLY_RESULT_READY),
        ready_for_v0365_sandbox_post_apply_validation=kwargs.pop("ready_for_v0365_sandbox_post_apply_validation", True),
        ready_for_v0366_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_v0366_bounded_agentic_task_operation_cycle", True),
        ready_for_sandbox_workspace_materialization=kwargs.pop("ready_for_sandbox_workspace_materialization", True),
        ready_for_sandbox_workspace_write=kwargs.pop("ready_for_sandbox_workspace_write", True),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        ready_for_sandbox_file_materialization=kwargs.pop("ready_for_sandbox_file_materialization", True),
        ready_for_sandbox_patch_apply_result=kwargs.pop("ready_for_sandbox_patch_apply_result", True),
        ready_for_future_post_apply_validation_input=kwargs.pop("ready_for_future_post_apply_validation_input", True),
        digestion_first_policy_applied=kwargs.pop("digestion_first_policy_applied", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_agent_loop_blocked=kwargs.pop("infinite_agent_loop_blocked", True),
        bounded_agentic_task_only=kwargs.pop("bounded_agentic_task_only", True),
        no_independent_autonomous_agent_runtime=kwargs.pop("no_independent_autonomous_agent_runtime", True),
        **kwargs,
    )


def validate_sandbox_apply_path_containment(sandbox_root_ref: str, sandbox_path_ref: str) -> Path:
    _require_non_blank("sandbox_root_ref", sandbox_root_ref)
    normalized_path = normalize_sandbox_relative_path_ref(sandbox_path_ref)
    if _is_bad_root(sandbox_root_ref):
        raise ValueError("sandbox root is blank, live, reference, or otherwise unsafe")
    if _looks_reference_or_live_root(normalized_path):
        raise ValueError("sandbox target path points to live/reference root")
    lowered_target = normalized_path.lower()
    if any(token in lowered_target for token in ("secret", "secrets", ".env", "password", "credential", "credentials", "token", "api_key", "apikey")):
        raise ValueError("sandbox target path is secret-like or credential-like")
    if lowered_target.endswith((".bin", ".dll", ".exe", ".gif", ".jpg", ".jpeg", ".pdf", ".png", ".zip")):
        raise ValueError("sandbox target path is binary-like")
    sandbox_root = Path(sandbox_root_ref).resolve()
    target_path = (sandbox_root / normalized_path).resolve()
    try:
        target_path.relative_to(sandbox_root)
    except ValueError as exc:
        raise ValueError("sandbox target escapes sandbox root") from exc
    return target_path


def materialize_sandbox_workspace_from_plan(plan: SandboxMaterializationPlan, policy: SandboxPatchApplyPolicy | None = None) -> list[SandboxFileWriteRecord]:
    active_policy = policy or default_sandbox_patch_apply_policy()
    if not active_policy.allow_sandbox_directory_creation:
        raise ValueError("sandbox directory creation is not allowed by policy")
    records: list[SandboxFileWriteRecord] = []
    for directory_plan in plan.directory_plans:
        if directory_plan.blocked or not directory_plan.create_directory:
            continue
        directory_path = validate_sandbox_apply_path_containment(plan.sandbox_root_ref, directory_plan.sandbox_path_ref)
        directory_path.mkdir(parents=True, exist_ok=True)
        records.append(
            build_sandbox_file_write_record(
                write_record_id=f"sandbox_write_record:v0.36.4:dir:{len(records) + 1}",
                write_operation_id=directory_plan.directory_plan_id,
                sandbox_root_ref=plan.sandbox_root_ref,
                sandbox_path_ref=directory_plan.sandbox_path_ref,
                write_status=SandboxFileWriteStatus.WRITTEN,
                bytes_written=0,
                write_summary="sandbox directory created under validated sandbox root",
            )
        )
    return records


def write_sandbox_file_under_policy(
    operation: SandboxFileWriteOperation,
    policy: SandboxPatchApplyPolicy | None = None,
) -> SandboxFileWriteRecord:
    active_policy = policy or default_sandbox_patch_apply_policy()
    if not active_policy.allow_sandbox_file_write or not operation.allowed_under_policy:
        return build_sandbox_file_write_record(
            write_record_id=f"sandbox_write_record:v0.36.4:block:{operation.write_operation_id}",
            write_operation_id=operation.write_operation_id,
            sandbox_root_ref=operation.sandbox_root_ref,
            sandbox_path_ref=operation.sandbox_path_ref,
            write_status=SandboxFileWriteStatus.BLOCKED,
            bytes_written=0,
            write_summary="sandbox file write blocked by policy",
        )
    if len(operation.content_text) > active_policy.max_file_write_chars:
        raise ValueError("sandbox file content exceeds policy bound")
    target_path = validate_sandbox_apply_path_containment(operation.sandbox_root_ref, operation.sandbox_path_ref)
    target_path.parent.mkdir(parents=True, exist_ok=True)
    with target_path.open("w", encoding="utf-8", newline="") as sandbox_file:
        sandbox_file.write(operation.content_text)
    return build_sandbox_file_write_record(
        write_record_id=f"sandbox_write_record:v0.36.4:{operation.write_operation_id}",
        write_operation_id=operation.write_operation_id,
        sandbox_root_ref=operation.sandbox_root_ref,
        sandbox_path_ref=operation.sandbox_path_ref,
        write_status=SandboxFileWriteStatus.WRITTEN,
        bytes_written=len(operation.content_text.encode("utf-8")),
        write_summary="sandbox file written under validated sandbox root",
    )


def run_sandbox_patch_apply(
    sandbox_apply_input: SandboxPatchApplyInput,
    materialization_plan: SandboxMaterializationPlan,
    policy: SandboxPatchApplyPolicy | None = None,
) -> SandboxPatchApplyResult:
    active_policy = policy or default_sandbox_patch_apply_policy()
    if not active_policy.allow_sandbox_patch_apply:
        return build_sandbox_patch_apply_result(
            sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
            sandbox_root_ref=sandbox_apply_input.sandbox_root_ref,
            materialization_plan=materialization_plan,
            engine_operation=build_sandbox_patch_engine_operation(file_write_operations=[]),
            file_results=[],
            write_records=[],
            status=SandboxPatchApplyStatus.BLOCKED,
            readiness_level=SandboxPatchApplyReadinessLevel.BLOCKED,
            sandbox_apply_successful=False,
            ready_for_v0365_sandbox_post_apply_validation=False,
            ready_for_v0366_bounded_agentic_task_operation_cycle=False,
            ready_for_future_post_apply_validation_input=False,
            summary="sandbox patch apply blocked by policy",
        )
    if not active_policy.allow_partial_safe_apply and any(plan.blocked for plan in materialization_plan.file_plans):
        return build_sandbox_patch_apply_result(
            sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
            sandbox_root_ref=sandbox_apply_input.sandbox_root_ref,
            materialization_plan=materialization_plan,
            engine_operation=build_sandbox_patch_engine_operation(file_write_operations=[]),
            file_results=[],
            write_records=[],
            status=SandboxPatchApplyStatus.BLOCKED,
            readiness_level=SandboxPatchApplyReadinessLevel.BLOCKED,
            sandbox_apply_successful=False,
            ready_for_v0365_sandbox_post_apply_validation=False,
            ready_for_v0366_bounded_agentic_task_operation_cycle=False,
            ready_for_future_post_apply_validation_input=False,
            summary="sandbox patch apply fail-closed because a file plan is blocked",
        )
    materialize_sandbox_workspace_from_plan(materialization_plan, active_policy)
    operations: list[SandboxFileWriteOperation] = []
    write_records: list[SandboxFileWriteRecord] = []
    file_results: list[SandboxPatchEngineFileResult] = []
    total_chars = 0
    for index, file_plan in enumerate(materialization_plan.file_plans, start=1):
        if file_plan.blocked or not file_plan.ready_for_sandbox_write:
            continue
        content_text = str(file_plan.metadata.get("content_text", file_plan.content_preview))
        total_chars += len(content_text)
        if total_chars > active_policy.max_total_write_chars:
            raise ValueError("sandbox total write content exceeds policy bound")
        operation = build_sandbox_file_write_operation(
            write_operation_id=f"sandbox_write_operation:v0.36.4:{index}",
            file_plan_id=file_plan.file_plan_id,
            sandbox_root_ref=materialization_plan.sandbox_root_ref,
            sandbox_path_ref=file_plan.sandbox_path_ref,
            write_kind=file_plan.write_kind,
            content_text=content_text,
            content_summary=file_plan.file_summary,
            allowed_under_policy=True,
        )
        record = write_sandbox_file_under_policy(operation, active_policy)
        operations.append(operation)
        write_records.append(record)
        file_results.append(
            build_sandbox_patch_engine_file_result(
                engine_file_result_id=f"sandbox_engine_file_result:v0.36.4:{index}",
                sandbox_path_ref=file_plan.sandbox_path_ref,
                source_file_plan_id=file_plan.file_plan_id,
                write_records=[record],
                sandbox_write_successful=record.write_status == SandboxFileWriteStatus.WRITTEN,
            )
        )
    successful = bool(write_records) and all(record.write_status == SandboxFileWriteStatus.WRITTEN for record in write_records)
    operation = build_sandbox_patch_engine_operation(
        sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
        engine_strategy=sandbox_apply_input.engine_strategy,
        file_write_operations=operations,
        allowed_under_policy=True,
    )
    return build_sandbox_patch_apply_result(
        sandbox_apply_input_id=sandbox_apply_input.sandbox_apply_input_id,
        mode=sandbox_apply_input.requested_mode,
        sandbox_root_ref=materialization_plan.sandbox_root_ref,
        materialization_plan=materialization_plan,
        engine_operation=operation,
        file_results=file_results,
        write_records=write_records,
        source_refs=sandbox_apply_input.source_refs,
        files_written_count=len(write_records),
        bytes_written_total=sum(record.bytes_written for record in write_records),
        sandbox_apply_successful=successful,
        status=SandboxPatchApplyStatus.SANDBOX_APPLY_COMPLETED if successful else SandboxPatchApplyStatus.SAFE_FAILED,
        readiness_level=SandboxPatchApplyReadinessLevel.SANDBOX_APPLY_RESULT_READY if successful else SandboxPatchApplyReadinessLevel.BLOCKED,
        ready_for_v0365_sandbox_post_apply_validation=successful,
        ready_for_v0366_bounded_agentic_task_operation_cycle=successful,
        ready_for_future_post_apply_validation_input=successful,
    )


def validate_sandbox_patch_apply_result(result: SandboxPatchApplyResult) -> SandboxPatchApplyValidationReport:
    findings: list[SandboxPatchApplyValidationFinding] = []
    if result.live_write_performed:
        findings.append(
            build_sandbox_patch_apply_validation_finding(
                risk_kind=SandboxPatchApplyRiskKind.LIVE_WORKSPACE_WRITE_RISK,
                decision_kind=SandboxPatchApplyDecisionKind.BLOCK,
                summary="live write was reported",
                blocks_future_validation=True,
            )
        )
    if any(record.wrote_outside_sandbox for record in result.write_records):
        findings.append(
            build_sandbox_patch_apply_validation_finding(
                risk_kind=SandboxPatchApplyRiskKind.OUTSIDE_ROOT_WRITE_RISK,
                decision_kind=SandboxPatchApplyDecisionKind.BLOCK,
                summary="outside sandbox write was reported",
                blocks_future_validation=True,
            )
        )
    ready = result.sandbox_apply_successful and not findings
    return build_sandbox_patch_apply_validation_report(
        sandbox_apply_result_id=result.sandbox_apply_result_id,
        findings=findings,
        status=result.status,
        ready_for_future_post_apply_validation_input=ready,
    )


def sandbox_patch_apply_flags_preserve_no_live_write(flags: SandboxPatchApplyFlagSet) -> bool:
    return isinstance(flags, SandboxPatchApplyFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def sandbox_patch_apply_policy_blocks_live_write(policy: SandboxPatchApplyPolicy) -> bool:
    return not any(
        getattr(policy, name)
        for name in (
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
        )
    )


def sandbox_file_write_record_is_sandbox_only(record: SandboxFileWriteRecord) -> bool:
    return record.live_write is False and record.wrote_outside_sandbox is False


def sandbox_patch_apply_result_is_not_live_apply(result: SandboxPatchApplyResult) -> bool:
    return not any(
        getattr(result, name)
        for name in (
            "live_write_performed",
            "used_apply_patch",
            "used_git_apply",
            "used_shell",
            "ready_for_live_workspace_write",
            "ready_for_patch_application",
            "ready_for_execution",
        )
    )


def sandbox_patch_apply_decision_is_not_live_apply_permission(decision: SandboxPatchApplyDecision) -> bool:
    return not any(
        getattr(decision, name)
        for name in (
            "allow_live_workspace_write",
            "allow_apply_patch",
            "allow_git_apply",
            "allow_shell",
            "allow_test_execution",
            "allow_external_agent_execution",
            "allow_dominion_runtime",
        )
    )


def v0364_readiness_report_is_not_execution_ready(report: V0364ReadinessReport) -> bool:
    return isinstance(report, V0364ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
