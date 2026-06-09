from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_dry_run import (
    DryRunApplySimulationResult,
    DryRunSimulatedFileDelta,
    DryRunSimulatedFileResult,
)


V0363_VERSION = "v0.36.3"
V0363_RELEASE_NAME = "v0.36.3 Sandbox Workspace / Overlay Policy"
MAX_PREVIEW_CHARS = 600

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_sandbox_workspace_materialization",
    "ready_for_sandbox_workspace_write",
    "ready_for_sandbox_patch_apply",
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
    "directory_creation",
    "file_write",
    "sandbox_apply",
    "live_write",
    "apply_patch",
    "git_apply",
    "shell",
    "test_execution",
    "dependency_install",
    "external_agent_execution",
    "dominion_runtime",
)

SECRET_PATH_TOKENS = ("secret", "secrets", ".env", "password")
CREDENTIAL_PATH_TOKENS = ("credential", "credentials", "token", "api_key", "apikey")
BINARY_EXTENSIONS = (
    ".bin",
    ".dll",
    ".exe",
    ".gif",
    ".jpg",
    ".jpeg",
    ".pdf",
    ".png",
    ".zip",
)


class SandboxWorkspaceMode(StrEnum):
    MANIFEST_ONLY = "manifest_only"
    OVERLAY_POLICY_ONLY = "overlay_policy_only"
    IN_MEMORY_OVERLAY_PLAN = "in_memory_overlay_plan"
    FUTURE_MATERIALIZATION_INPUT = "future_materialization_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxWorkspaceSourceKind(StrEnum):
    V0362_DRY_RUN_APPLY_SIMULATION_RESULT = "v0362_dry_run_apply_simulation_result"
    V0362_SIMULATED_FILE_RESULT = "v0362_simulated_file_result"
    V0362_SIMULATED_FILE_DELTA = "v0362_simulated_file_delta"
    V0361_APPLY_CANDIDATE_ENVELOPE = "v0361_apply_candidate_envelope"
    V0361_HUMAN_APPROVAL_CONTRACT = "v0361_human_approval_contract"
    V0360_PATCH_APPLY_SANDBOX_BOUNDARY = "v0360_patch_apply_sandbox_boundary"
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxWorkspaceStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    POLICY_CREATED = "policy_created"
    MANIFEST_CREATED = "manifest_created"
    MANIFEST_VALIDATED = "manifest_validated"
    MANIFEST_VALIDATED_WITH_GAPS = "manifest_validated_with_gaps"
    FUTURE_MATERIALIZATION_READY = "future_materialization_ready"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxWorkspaceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SANDBOX_POLICY_READY = "sandbox_policy_ready"
    OVERLAY_POLICY_READY = "overlay_policy_ready"
    MANIFEST_READY = "manifest_ready"
    FILE_MAP_READY = "file_map_ready"
    LIVE_WRITE_BLOCK_READY = "live_write_block_ready"
    DESIGN_HANDOFF_READY_FOR_V0364 = "design_handoff_ready_for_v0364"
    DESIGN_HANDOFF_READY_FOR_V0365 = "design_handoff_ready_for_v0365"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxWorkspaceDecisionKind(StrEnum):
    ALLOW_MANIFEST_METADATA = "allow_manifest_metadata"
    ALLOW_OVERLAY_POLICY_METADATA = "allow_overlay_policy_metadata"
    ALLOW_FILE_MAP_METADATA = "allow_file_map_metadata"
    ALLOW_FUTURE_MATERIALIZATION_INPUT = "allow_future_materialization_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxWorkspaceRiskKind(StrEnum):
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    SANDBOX_WORKSPACE_WRITE_CONFUSION_RISK = "sandbox_workspace_write_confusion_risk"
    SANDBOX_ESCAPE_RISK = "sandbox_escape_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    OUTSIDE_ROOT_WRITE_RISK = "outside_root_write_risk"
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    ABSOLUTE_PATH_RISK = "absolute_path_risk"
    REFERENCE_ROOT_WRITE_RISK = "reference_root_write_risk"
    SECRET_PATH_RISK = "secret_path_risk"
    CREDENTIAL_PATH_RISK = "credential_path_risk"
    BINARY_TARGET_RISK = "binary_target_risk"
    BLOCKED_TARGET_RISK = "blocked_target_risk"
    UNRESOLVED_DRY_RUN_CONFLICT_RISK = "unresolved_dry_run_conflict_risk"
    PATCH_APPLY_CONFUSION_RISK = "patch_apply_confusion_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class SandboxPathRole(StrEnum):
    SANDBOX_ROOT = "sandbox_root"
    SANDBOX_MANIFEST_PATH = "sandbox_manifest_path"
    SANDBOX_OVERLAY_ROOT = "sandbox_overlay_root"
    VIRTUAL_TARGET_FILE = "virtual_target_file"
    VIRTUAL_SOURCE_FILE = "virtual_source_file"
    FUTURE_MATERIALIZATION_TARGET = "future_materialization_target"
    LIVE_WORKSPACE_ROOT = "live_workspace_root"
    REFERENCE_ROOT = "reference_root"
    BLOCKED_SECRET_PATH = "blocked_secret_path"
    BLOCKED_CREDENTIAL_PATH = "blocked_credential_path"
    BLOCKED_BINARY_PATH = "blocked_binary_path"
    EXTERNAL_PATH = "external_path"
    UNKNOWN = "unknown"


class SandboxPathStatus(StrEnum):
    UNKNOWN = "unknown"
    VALID_METADATA_PATH = "valid_metadata_path"
    VALID_FUTURE_MATERIALIZATION_PATH = "valid_future_materialization_path"
    BLOCKED = "blocked"
    OUTSIDE_ROOT = "outside_root"
    TRAVERSAL_DETECTED = "traversal_detected"
    ABSOLUTE_PATH_BLOCKED = "absolute_path_blocked"
    SYMLINK_RISK = "symlink_risk"
    SECRET_BLOCKED = "secret_blocked"
    CREDENTIAL_BLOCKED = "credential_blocked"
    BINARY_BLOCKED = "binary_blocked"
    REFERENCE_ROOT_BLOCKED = "reference_root_blocked"
    EXTERNAL_BLOCKED = "external_blocked"
    NO_OP = "no_op"


class SandboxPathDecisionKind(StrEnum):
    ALLOW_PATH_METADATA = "allow_path_metadata"
    ALLOW_FUTURE_MATERIALIZATION_PATH = "allow_future_materialization_path"
    BLOCK_PATH = "block_path"
    BLOCK_LIVE_WORKSPACE = "block_live_workspace"
    BLOCK_REFERENCE_ROOT = "block_reference_root"
    BLOCK_SECRET = "block_secret"
    BLOCK_CREDENTIAL = "block_credential"
    BLOCK_BINARY = "block_binary"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxEscapeKind(StrEnum):
    NO_ESCAPE_DETECTED = "no_escape_detected"
    PATH_TRAVERSAL = "path_traversal"
    ABSOLUTE_PATH = "absolute_path"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    OUTSIDE_SANDBOX_ROOT = "outside_sandbox_root"
    LIVE_WORKSPACE_TARGET = "live_workspace_target"
    REFERENCE_ROOT_TARGET = "reference_root_target"
    EXTERNAL_ROOT_TARGET = "external_root_target"
    UNKNOWN = "unknown"


class OverlayWriteMode(StrEnum):
    NO_WRITE = "no_write"
    VIRTUAL_OVERLAY_METADATA = "virtual_overlay_metadata"
    FUTURE_OVERLAY_MATERIALIZATION = "future_overlay_materialization"
    FUTURE_SANDBOX_WRITE = "future_sandbox_write"
    LIVE_WRITE_BLOCKED = "live_write_blocked"
    UNKNOWN = "unknown"


class OverlayMaterializationMode(StrEnum):
    NOT_MATERIALIZED = "not_materialized"
    METADATA_ONLY = "metadata_only"
    FUTURE_SANDBOX_MATERIALIZATION = "future_sandbox_materialization"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0363_VERSION not in version:
        raise ValueError("version must include v0.36.3")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.3")


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


def _bounded_preview(value: str, max_chars: int = MAX_PREVIEW_CHARS) -> str:
    if not isinstance(value, str):
        raise TypeError("preview value must be str")
    redacted = value
    for token in ("secret", "credential", "api_key", "token", "password"):
        redacted = redacted.replace(token, "[redacted]")
        redacted = redacted.replace(token.upper(), "[redacted]")
    return redacted[:max_chars]


def _is_absolute_path_ref(path_ref: str) -> bool:
    stripped = path_ref.strip()
    return (
        stripped.startswith("/")
        or stripped.startswith("\\")
        or "://" in stripped
        or (len(stripped) >= 2 and stripped[1] == ":")
    )


def _split_path_ref(path_ref: str) -> list[str]:
    return [part for part in path_ref.replace("\\", "/").split("/") if part not in ("", ".")]


def _path_has_traversal(path_ref: str) -> bool:
    return any(part == ".." for part in _split_path_ref(path_ref))


def _blocked_path_status(status: SandboxPathStatus | str) -> bool:
    return SandboxPathStatus(status) in {
        SandboxPathStatus.BLOCKED,
        SandboxPathStatus.OUTSIDE_ROOT,
        SandboxPathStatus.TRAVERSAL_DETECTED,
        SandboxPathStatus.ABSOLUTE_PATH_BLOCKED,
        SandboxPathStatus.SYMLINK_RISK,
        SandboxPathStatus.SECRET_BLOCKED,
        SandboxPathStatus.CREDENTIAL_BLOCKED,
        SandboxPathStatus.BINARY_BLOCKED,
        SandboxPathStatus.REFERENCE_ROOT_BLOCKED,
        SandboxPathStatus.EXTERNAL_BLOCKED,
        SandboxPathStatus.UNKNOWN,
    }


def _blocking_escape(escape_kind: SandboxEscapeKind | str) -> bool:
    return SandboxEscapeKind(escape_kind) != SandboxEscapeKind.NO_ESCAPE_DETECTED


def _blocked_role(path_role: SandboxPathRole | str) -> bool:
    return SandboxPathRole(path_role) in {
        SandboxPathRole.LIVE_WORKSPACE_ROOT,
        SandboxPathRole.REFERENCE_ROOT,
        SandboxPathRole.BLOCKED_SECRET_PATH,
        SandboxPathRole.BLOCKED_CREDENTIAL_PATH,
        SandboxPathRole.BLOCKED_BINARY_PATH,
        SandboxPathRole.EXTERNAL_PATH,
        SandboxPathRole.UNKNOWN,
    }


@dataclass(frozen=True)
class SandboxWorkspaceFlagSet:
    flag_set_id: str
    version: str
    sandbox_workspace_policy_constructed: bool
    sandbox_root_policy_defined: bool
    overlay_policy_defined: bool
    sandbox_manifest_available: bool
    sandbox_file_map_available: bool
    live_workspace_write_block_available: bool
    ready_for_v0364_sandbox_patch_apply_engine: bool
    ready_for_v0365_sandbox_post_apply_validation: bool
    ready_for_sandbox_workspace_policy: bool
    ready_for_sandbox_root_policy: bool
    ready_for_overlay_policy: bool
    ready_for_sandbox_workspace_manifest: bool
    ready_for_sandbox_file_map: bool
    ready_for_live_workspace_write_block: bool
    ready_for_future_sandbox_materialization_input: bool
    ready_for_execution: bool = False
    ready_for_sandbox_workspace_materialization: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_sandbox_patch_apply: bool = False
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
class SandboxWorkspaceSourceRef:
    source_ref_id: str
    source_kind: SandboxWorkspaceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxWorkspaceSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxRootPolicy:
    root_policy_id: str
    version: str
    sandbox_root_ref: str
    allowed_root_patterns: list[str]
    blocked_root_patterns: list[str]
    blocked_live_root_refs: list[str]
    blocked_reference_root_refs: list[str]
    require_relative_targets: bool
    block_absolute_targets: bool
    block_path_traversal: bool
    block_symlink_escape_risk: bool
    block_outside_root: bool
    allow_directory_creation: bool = False
    allow_file_write: bool = False
    allow_live_workspace_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("root_policy_id", "sandbox_root_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in (
            "allowed_root_patterns",
            "blocked_root_patterns",
            "blocked_live_root_refs",
            "blocked_reference_root_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "require_relative_targets",
            "block_absolute_targets",
            "block_path_traversal",
            "block_symlink_escape_risk",
            "block_outside_root",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} should be True in v0.36.3")
        _validate_false(self, ("allow_directory_creation", "allow_file_write", "allow_live_workspace_write"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxOverlayPolicy:
    overlay_policy_id: str
    version: str
    write_mode: OverlayWriteMode | str
    materialization_mode: OverlayMaterializationMode | str
    allow_virtual_overlay_metadata: bool
    allow_future_materialization_input: bool
    allow_sandbox_materialization: bool = False
    allow_sandbox_file_write: bool = False
    allow_live_file_write: bool = False
    allow_patch_apply: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    max_overlay_entries: int = 100
    max_preview_chars: int = MAX_PREVIEW_CHARS
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("overlay_policy_id", self.overlay_policy_id)
        _validate_version(self.version)
        OverlayWriteMode(self.write_mode)
        OverlayMaterializationMode(self.materialization_mode)
        _validate_false(
            self,
            (
                "allow_sandbox_materialization",
                "allow_sandbox_file_write",
                "allow_live_file_write",
                "allow_patch_apply",
                "allow_apply_patch",
                "allow_git_apply",
            ),
        )
        for name in ("max_overlay_entries", "max_preview_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspacePolicy:
    workspace_policy_id: str
    version: str
    workspace_mode: SandboxWorkspaceMode | str
    root_policy: SandboxRootPolicy
    overlay_policy: SandboxOverlayPolicy
    allowed_path_roles: list[SandboxPathRole | str]
    blocked_path_roles: list[SandboxPathRole | str]
    blocked_escape_kinds: list[SandboxEscapeKind | str]
    max_manifest_entries: int
    require_dry_run_success: bool
    require_no_blocking_conflicts: bool
    require_human_approval_contract: bool
    allow_manifest_metadata: bool
    allow_file_map_metadata: bool
    allow_future_materialization_input: bool
    allow_directory_creation: bool = False
    allow_sandbox_file_write: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("workspace_policy_id", self.workspace_policy_id)
        _validate_version(self.version)
        SandboxWorkspaceMode(self.workspace_mode)
        if not isinstance(self.root_policy, SandboxRootPolicy):
            raise TypeError("root_policy must be SandboxRootPolicy")
        if not isinstance(self.overlay_policy, SandboxOverlayPolicy):
            raise TypeError("overlay_policy must be SandboxOverlayPolicy")
        _validate_enum_list("allowed_path_roles", self.allowed_path_roles, SandboxPathRole)
        _validate_enum_list("blocked_path_roles", self.blocked_path_roles, SandboxPathRole)
        _validate_enum_list("blocked_escape_kinds", self.blocked_escape_kinds, SandboxEscapeKind)
        if self.max_manifest_entries < 0:
            raise ValueError("max_manifest_entries must be >= 0")
        _validate_false(
            self,
            (
                "allow_directory_creation",
                "allow_sandbox_file_write",
                "allow_live_workspace_write",
                "allow_patch_application",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceInput:
    workspace_input_id: str
    version: str
    dry_run_result_id: str | None
    apply_candidate_id: str | None
    human_approval_contract_id: str | None
    requested_mode: SandboxWorkspaceMode | str
    requested_sandbox_root_ref: str
    requested_target_path_refs: list[str]
    source_refs: list[SandboxWorkspaceSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("workspace_input_id", "requested_sandbox_root_ref", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxWorkspaceMode(self.requested_mode)
        _validate_string_list("requested_target_path_refs", self.requested_target_path_refs)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_RUNTIME_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing {missing}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxPathRef:
    path_ref_id: str
    raw_path_ref: str
    normalized_path_ref: str
    path_role: SandboxPathRole | str
    path_status: SandboxPathStatus | str
    decision_kind: SandboxPathDecisionKind | str
    escape_kind: SandboxEscapeKind | str
    risk_kinds: list[SandboxWorkspaceRiskKind | str]
    blocked: bool
    block_reason: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("path_ref_id", "raw_path_ref", "normalized_path_ref"):
            _require_non_blank(name, getattr(self, name))
        SandboxPathRole(self.path_role)
        SandboxPathStatus(self.path_status)
        SandboxPathDecisionKind(self.decision_kind)
        SandboxEscapeKind(self.escape_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, SandboxWorkspaceRiskKind)
        should_block = (
            _blocked_path_status(self.path_status)
            or _blocking_escape(self.escape_kind)
            or _blocked_role(self.path_role)
            or SandboxWorkspaceRiskKind.BLOCKED_TARGET_RISK in [SandboxWorkspaceRiskKind(risk) for risk in self.risk_kinds]
        )
        if should_block and not self.blocked:
            raise ValueError("blocked path status, role, escape, or risk must set blocked=True")
        if self.blocked and not self.block_reason:
            raise ValueError("blocked path must include block_reason")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxFileMapEntry:
    file_map_entry_id: str
    virtual_path_ref: str
    source_path_ref: str | None
    target_path_ref: str
    path_ref_id: str
    simulated_delta_ids: list[str]
    entry_summary: str
    eligible_for_future_materialization: bool
    ready_for_write: bool = False
    ready_for_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("file_map_entry_id", "virtual_path_ref", "target_path_ref", "path_ref_id", "entry_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("simulated_delta_ids", self.simulated_delta_ids)
        if self.eligible_for_future_materialization and self.metadata.get("path_blocked"):
            raise ValueError("blocked path cannot be eligible for future materialization")
        if self.eligible_for_future_materialization and self.metadata.get("blocking_conflicts"):
            raise ValueError("blocking conflicts prevent future materialization eligibility")
        _validate_false(self, ("ready_for_write", "ready_for_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxOverlayEntry:
    overlay_entry_id: str
    file_map_entry_id: str
    target_path_ref: str
    overlay_summary: str
    simulated_after_preview: str
    delta_kind_summary: str
    materialization_mode: OverlayMaterializationMode | str
    eligible_for_future_materialization: bool
    materialized: bool = False
    ready_for_write: bool = False
    ready_for_apply: bool = False
    redacted: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("overlay_entry_id", "file_map_entry_id", "target_path_ref", "overlay_summary"):
            _require_non_blank(name, getattr(self, name))
        OverlayMaterializationMode(self.materialization_mode)
        if _bounded_preview(self.simulated_after_preview) != self.simulated_after_preview:
            raise ValueError("simulated_after_preview must be bounded and redacted")
        _validate_false(self, ("materialized", "ready_for_write", "ready_for_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceManifest:
    manifest_id: str
    version: str
    workspace_input_id: str
    sandbox_root_ref: str
    workspace_mode: SandboxWorkspaceMode | str
    path_refs: list[SandboxPathRef]
    file_map_entries: list[SandboxFileMapEntry]
    overlay_entries: list[SandboxOverlayEntry]
    source_refs: list[SandboxWorkspaceSourceRef]
    manifest_summary: str
    blocked_path_count: int
    eligible_entry_count: int
    materialized: bool = False
    ready_for_future_materialization_input: bool = False
    ready_for_sandbox_workspace_materialization: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("manifest_id", "workspace_input_id", "sandbox_root_ref", "manifest_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxWorkspaceMode(self.workspace_mode)
        for name in ("path_refs", "file_map_entries", "overlay_entries", "source_refs"):
            _validate_list(name, getattr(self, name))
        for name in ("blocked_path_count", "eligible_entry_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        if self.blocked_path_count != sum(1 for path_ref in self.path_refs if path_ref.blocked):
            raise ValueError("blocked_path_count must match blocked path refs")
        if self.eligible_entry_count != sum(1 for entry in self.file_map_entries if entry.eligible_for_future_materialization):
            raise ValueError("eligible_entry_count must match eligible file-map entries")
        if self.ready_for_future_materialization_input:
            if self.blocked_path_count > 0:
                raise ValueError("blocked paths prevent future materialization input readiness")
            if self.metadata.get("dry_run_successful") is False or self.metadata.get("blocking_conflicts"):
                raise ValueError("dry-run gaps prevent future materialization input readiness")
        _validate_false(
            self,
            (
                "materialized",
                "ready_for_sandbox_workspace_materialization",
                "ready_for_sandbox_workspace_write",
                "ready_for_sandbox_patch_apply",
                "ready_for_live_workspace_write",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspacePlan:
    workspace_plan_id: str
    version: str
    manifest_id: str
    planned_materialization_steps: list[str]
    blocked_materialization_steps: list[str]
    live_write_blocks: list[str]
    future_handoff_notes: list[str]
    summary: str
    ready_for_v0364_sandbox_patch_apply_engine: bool
    ready_for_sandbox_workspace_materialization: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("workspace_plan_id", "manifest_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("planned_materialization_steps", "blocked_materialization_steps", "live_write_blocks", "future_handoff_notes"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_sandbox_workspace_materialization",
                "ready_for_sandbox_workspace_write",
                "ready_for_sandbox_patch_apply",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxLiveWriteBlock:
    live_write_block_id: str
    version: str
    blocked_root_refs: list[str]
    blocked_path_refs: list[str]
    blocked_reason: str
    live_workspace_write_allowed: bool = False
    workspace_write_allowed: bool = False
    code_edit_allowed: bool = False
    patch_application_allowed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("live_write_block_id", "blocked_reason"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("blocked_root_refs", self.blocked_root_refs)
        _validate_string_list("blocked_path_refs", self.blocked_path_refs)
        _validate_false(
            self,
            (
                "live_workspace_write_allowed",
                "workspace_write_allowed",
                "code_edit_allowed",
                "patch_application_allowed",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceGateDecision:
    gate_decision_id: str
    decision_kind: SandboxWorkspaceDecisionKind | str
    status: SandboxWorkspaceStatus | str
    summary: str
    ready_for_future_materialization_input: bool
    allow_directory_creation: bool = False
    allow_sandbox_workspace_write: bool = False
    allow_sandbox_patch_apply: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    allow_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("gate_decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxWorkspaceDecisionKind(self.decision_kind)
        SandboxWorkspaceStatus(self.status)
        _validate_false(
            self,
            (
                "allow_directory_creation",
                "allow_sandbox_workspace_write",
                "allow_sandbox_patch_apply",
                "allow_live_workspace_write",
                "allow_patch_application",
                "allow_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceValidationFinding:
    finding_id: str
    risk_kind: SandboxWorkspaceRiskKind | str
    decision_kind: SandboxWorkspaceDecisionKind | str
    path_ref_id: str | None
    summary: str
    blocks_future_materialization: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        SandboxWorkspaceRiskKind(self.risk_kind)
        SandboxWorkspaceDecisionKind(self.decision_kind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceValidationReport:
    validation_report_id: str
    manifest_id: str
    findings: list[SandboxWorkspaceValidationFinding]
    status: SandboxWorkspaceStatus | str
    summary: str
    certifies_filesystem_mutation: bool = False
    ready_for_future_materialization_input: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "manifest_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("findings", self.findings)
        SandboxWorkspaceStatus(self.status)
        _validate_false(self, ("certifies_filesystem_mutation",))
        if self.ready_for_future_materialization_input and any(finding.blocks_future_materialization for finding in self.findings):
            raise ValueError("blocking findings prevent future materialization input readiness")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceReport:
    report_id: str
    manifest: SandboxWorkspaceManifest
    validation_report: SandboxWorkspaceValidationReport
    gate_decision: SandboxWorkspaceGateDecision
    summary: str
    manifest_ready: bool
    ready_for_future_materialization_input: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        if not isinstance(self.manifest, SandboxWorkspaceManifest):
            raise TypeError("manifest must be SandboxWorkspaceManifest")
        if not isinstance(self.validation_report, SandboxWorkspaceValidationReport):
            raise TypeError("validation_report must be SandboxWorkspaceValidationReport")
        if not isinstance(self.gate_decision, SandboxWorkspaceGateDecision):
            raise TypeError("gate_decision must be SandboxWorkspaceGateDecision")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceRunPreview:
    run_preview_id: str
    manifest_id: str
    preview_summary: str
    planned_metadata_actions: list[str]
    prohibited_runtime_actions: list[str]
    ready_for_future_materialization_input: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "manifest_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("planned_metadata_actions", self.planned_metadata_actions)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class SandboxWorkspaceNoLiveWriteGuarantee:
    guarantee_id: str
    version: str
    no_sandbox_directory_creation: bool
    no_sandbox_workspace_materialization: bool
    no_sandbox_file_write: bool
    no_live_workspace_write: bool
    no_sandbox_patch_apply: bool
    no_patch_application: bool
    no_workspace_write: bool
    no_code_edit: bool
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
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.3")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0363ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    status: SandboxWorkspaceStatus | str
    readiness_level: SandboxWorkspaceReadinessLevel | str
    ready_for_v0364_sandbox_patch_apply_engine: bool
    ready_for_v0365_sandbox_post_apply_validation: bool
    ready_for_sandbox_workspace_policy: bool
    ready_for_sandbox_root_policy: bool
    ready_for_overlay_policy: bool
    ready_for_sandbox_workspace_manifest: bool
    ready_for_sandbox_file_map: bool
    ready_for_live_workspace_write_block: bool
    ready_for_future_sandbox_materialization_input: bool
    digestion_first_policy_applied: bool
    dominion_runtime_blocked: bool
    external_agent_execution_blocked: bool
    infinite_agent_loop_blocked: bool
    bounded_agentic_task_only: bool
    no_independent_autonomous_agent_runtime: bool
    ready_for_execution: bool = False
    ready_for_sandbox_workspace_materialization: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_sandbox_patch_apply: bool = False
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
    summary: str = "v0.36.3 sandbox workspace and overlay policy metadata only"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        SandboxWorkspaceStatus(self.status)
        SandboxWorkspaceReadinessLevel(self.readiness_level)
        for name in (
            "digestion_first_policy_applied",
            "dominion_runtime_blocked",
            "external_agent_execution_blocked",
            "infinite_agent_loop_blocked",
            "bounded_agentic_task_only",
            "no_independent_autonomous_agent_runtime",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.36.3")
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_sandbox_workspace_flags(**kwargs: Any) -> SandboxWorkspaceFlagSet:
    return SandboxWorkspaceFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_workspace_flags:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        sandbox_workspace_policy_constructed=kwargs.pop("sandbox_workspace_policy_constructed", True),
        sandbox_root_policy_defined=kwargs.pop("sandbox_root_policy_defined", True),
        overlay_policy_defined=kwargs.pop("overlay_policy_defined", True),
        sandbox_manifest_available=kwargs.pop("sandbox_manifest_available", True),
        sandbox_file_map_available=kwargs.pop("sandbox_file_map_available", True),
        live_workspace_write_block_available=kwargs.pop("live_workspace_write_block_available", True),
        ready_for_v0364_sandbox_patch_apply_engine=kwargs.pop("ready_for_v0364_sandbox_patch_apply_engine", True),
        ready_for_v0365_sandbox_post_apply_validation=kwargs.pop("ready_for_v0365_sandbox_post_apply_validation", True),
        ready_for_sandbox_workspace_policy=kwargs.pop("ready_for_sandbox_workspace_policy", True),
        ready_for_sandbox_root_policy=kwargs.pop("ready_for_sandbox_root_policy", True),
        ready_for_overlay_policy=kwargs.pop("ready_for_overlay_policy", True),
        ready_for_sandbox_workspace_manifest=kwargs.pop("ready_for_sandbox_workspace_manifest", True),
        ready_for_sandbox_file_map=kwargs.pop("ready_for_sandbox_file_map", True),
        ready_for_live_workspace_write_block=kwargs.pop("ready_for_live_workspace_write_block", True),
        ready_for_future_sandbox_materialization_input=kwargs.pop("ready_for_future_sandbox_materialization_input", True),
        **kwargs,
    )


def build_sandbox_workspace_source_ref(**kwargs: Any) -> SandboxWorkspaceSourceRef:
    return SandboxWorkspaceSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_source:v0.36.3:dry_run_result"),
        source_kind=kwargs.pop("source_kind", SandboxWorkspaceSourceKind.V0362_DRY_RUN_APPLY_SIMULATION_RESULT),
        source_id=kwargs.pop("source_id", "dry_run_result:v0.36.2"),
        source_summary=kwargs.pop("source_summary", "dry-run simulation metadata source; not file access"),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.2_dry_run_patch_apply_simulation.md"]),
        **kwargs,
    )


def build_sandbox_root_policy(**kwargs: Any) -> SandboxRootPolicy:
    return SandboxRootPolicy(
        root_policy_id=kwargs.pop("root_policy_id", "sandbox_root_policy:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "virtual-sandbox-root"),
        allowed_root_patterns=kwargs.pop("allowed_root_patterns", ["virtual-sandbox-root/**"]),
        blocked_root_patterns=kwargs.pop("blocked_root_patterns", ["../*", "/*", "references/**", ".git/**"]),
        blocked_live_root_refs=kwargs.pop("blocked_live_root_refs", ["workspace-root", ".git"]),
        blocked_reference_root_refs=kwargs.pop("blocked_reference_root_refs", ["references/OpenCode", "references/Hermes", "references/OpenClaw"]),
        require_relative_targets=kwargs.pop("require_relative_targets", True),
        block_absolute_targets=kwargs.pop("block_absolute_targets", True),
        block_path_traversal=kwargs.pop("block_path_traversal", True),
        block_symlink_escape_risk=kwargs.pop("block_symlink_escape_risk", True),
        block_outside_root=kwargs.pop("block_outside_root", True),
        **kwargs,
    )


def build_sandbox_overlay_policy(**kwargs: Any) -> SandboxOverlayPolicy:
    return SandboxOverlayPolicy(
        overlay_policy_id=kwargs.pop("overlay_policy_id", "sandbox_overlay_policy:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        write_mode=kwargs.pop("write_mode", OverlayWriteMode.VIRTUAL_OVERLAY_METADATA),
        materialization_mode=kwargs.pop("materialization_mode", OverlayMaterializationMode.METADATA_ONLY),
        allow_virtual_overlay_metadata=kwargs.pop("allow_virtual_overlay_metadata", True),
        allow_future_materialization_input=kwargs.pop("allow_future_materialization_input", True),
        **kwargs,
    )


def default_sandbox_workspace_policy(**kwargs: Any) -> SandboxWorkspacePolicy:
    root_policy = kwargs.pop("root_policy", build_sandbox_root_policy())
    overlay_policy = kwargs.pop("overlay_policy", build_sandbox_overlay_policy())
    return build_sandbox_workspace_policy(root_policy=root_policy, overlay_policy=overlay_policy, **kwargs)


def build_sandbox_workspace_policy(**kwargs: Any) -> SandboxWorkspacePolicy:
    return SandboxWorkspacePolicy(
        workspace_policy_id=kwargs.pop("workspace_policy_id", "sandbox_workspace_policy:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        workspace_mode=kwargs.pop("workspace_mode", SandboxWorkspaceMode.MANIFEST_ONLY),
        root_policy=kwargs.pop("root_policy", build_sandbox_root_policy()),
        overlay_policy=kwargs.pop("overlay_policy", build_sandbox_overlay_policy()),
        allowed_path_roles=kwargs.pop(
            "allowed_path_roles",
            [
                SandboxPathRole.SANDBOX_ROOT,
                SandboxPathRole.SANDBOX_MANIFEST_PATH,
                SandboxPathRole.SANDBOX_OVERLAY_ROOT,
                SandboxPathRole.VIRTUAL_TARGET_FILE,
                SandboxPathRole.VIRTUAL_SOURCE_FILE,
                SandboxPathRole.FUTURE_MATERIALIZATION_TARGET,
            ],
        ),
        blocked_path_roles=kwargs.pop(
            "blocked_path_roles",
            [
                SandboxPathRole.LIVE_WORKSPACE_ROOT,
                SandboxPathRole.REFERENCE_ROOT,
                SandboxPathRole.BLOCKED_SECRET_PATH,
                SandboxPathRole.BLOCKED_CREDENTIAL_PATH,
                SandboxPathRole.BLOCKED_BINARY_PATH,
                SandboxPathRole.EXTERNAL_PATH,
                SandboxPathRole.UNKNOWN,
            ],
        ),
        blocked_escape_kinds=kwargs.pop(
            "blocked_escape_kinds",
            [
                SandboxEscapeKind.PATH_TRAVERSAL,
                SandboxEscapeKind.ABSOLUTE_PATH,
                SandboxEscapeKind.SYMLINK_ESCAPE_RISK,
                SandboxEscapeKind.OUTSIDE_SANDBOX_ROOT,
                SandboxEscapeKind.LIVE_WORKSPACE_TARGET,
                SandboxEscapeKind.REFERENCE_ROOT_TARGET,
                SandboxEscapeKind.EXTERNAL_ROOT_TARGET,
                SandboxEscapeKind.UNKNOWN,
            ],
        ),
        max_manifest_entries=kwargs.pop("max_manifest_entries", 100),
        require_dry_run_success=kwargs.pop("require_dry_run_success", True),
        require_no_blocking_conflicts=kwargs.pop("require_no_blocking_conflicts", True),
        require_human_approval_contract=kwargs.pop("require_human_approval_contract", True),
        allow_manifest_metadata=kwargs.pop("allow_manifest_metadata", True),
        allow_file_map_metadata=kwargs.pop("allow_file_map_metadata", True),
        allow_future_materialization_input=kwargs.pop("allow_future_materialization_input", True),
        **kwargs,
    )


def build_sandbox_workspace_input(**kwargs: Any) -> SandboxWorkspaceInput:
    return SandboxWorkspaceInput(
        workspace_input_id=kwargs.pop("workspace_input_id", "sandbox_workspace_input:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        dry_run_result_id=kwargs.pop("dry_run_result_id", "dry_run_result:v0.36.2"),
        apply_candidate_id=kwargs.pop("apply_candidate_id", "apply_candidate:v0.36.1"),
        human_approval_contract_id=kwargs.pop("human_approval_contract_id", "human_approval_contract:v0.36.1"),
        requested_mode=kwargs.pop("requested_mode", SandboxWorkspaceMode.MANIFEST_ONLY),
        requested_sandbox_root_ref=kwargs.pop("requested_sandbox_root_ref", "virtual-sandbox-root"),
        requested_target_path_refs=kwargs.pop("requested_target_path_refs", ["src/example.py"]),
        source_refs=kwargs.pop("source_refs", [build_sandbox_workspace_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "Build sandbox manifest metadata only; no workspace creation"),
        **kwargs,
    )


def normalize_sandbox_relative_path_ref(raw_path_ref: str) -> str:
    _require_non_blank("raw_path_ref", raw_path_ref)
    if _is_absolute_path_ref(raw_path_ref):
        raise ValueError("absolute path refs are blocked")
    if _path_has_traversal(raw_path_ref):
        raise ValueError("path traversal is blocked")
    parts = _split_path_ref(raw_path_ref)
    if not parts:
        raise ValueError("path ref must contain at least one path segment")
    return "/".join(parts)


def build_sandbox_path_ref(**kwargs: Any) -> SandboxPathRef:
    return SandboxPathRef(
        path_ref_id=kwargs.pop("path_ref_id", "sandbox_path_ref:v0.36.3:src_example"),
        raw_path_ref=kwargs.pop("raw_path_ref", "src/example.py"),
        normalized_path_ref=kwargs.pop("normalized_path_ref", "src/example.py"),
        path_role=kwargs.pop("path_role", SandboxPathRole.FUTURE_MATERIALIZATION_TARGET),
        path_status=kwargs.pop("path_status", SandboxPathStatus.VALID_FUTURE_MATERIALIZATION_PATH),
        decision_kind=kwargs.pop("decision_kind", SandboxPathDecisionKind.ALLOW_FUTURE_MATERIALIZATION_PATH),
        escape_kind=kwargs.pop("escape_kind", SandboxEscapeKind.NO_ESCAPE_DETECTED),
        risk_kinds=kwargs.pop("risk_kinds", []),
        blocked=kwargs.pop("blocked", False),
        block_reason=kwargs.pop("block_reason", None),
        **kwargs,
    )


def _blocked_path_ref(
    raw_path_ref: str,
    normalized_path_ref: str,
    status: SandboxPathStatus,
    decision: SandboxPathDecisionKind,
    escape: SandboxEscapeKind,
    role: SandboxPathRole,
    risks: list[SandboxWorkspaceRiskKind],
    reason: str,
) -> SandboxPathRef:
    return build_sandbox_path_ref(
        path_ref_id=f"sandbox_path_ref:v0.36.3:blocked:{abs(hash((raw_path_ref, reason))) % 100000}",
        raw_path_ref=raw_path_ref,
        normalized_path_ref=normalized_path_ref,
        path_role=role,
        path_status=status,
        decision_kind=decision,
        escape_kind=escape,
        risk_kinds=risks,
        blocked=True,
        block_reason=reason,
    )


def classify_sandbox_path_ref(raw_path_ref: str, path_role: SandboxPathRole | str = SandboxPathRole.FUTURE_MATERIALIZATION_TARGET) -> SandboxPathRef:
    try:
        normalized = normalize_sandbox_relative_path_ref(raw_path_ref)
    except ValueError as exc:
        reason = str(exc)
        if "absolute" in reason:
            return _blocked_path_ref(
                raw_path_ref,
                raw_path_ref.strip().replace("\\", "/"),
                SandboxPathStatus.ABSOLUTE_PATH_BLOCKED,
                SandboxPathDecisionKind.BLOCK_PATH,
                SandboxEscapeKind.ABSOLUTE_PATH,
                SandboxPathRole.EXTERNAL_PATH,
                [SandboxWorkspaceRiskKind.ABSOLUTE_PATH_RISK, SandboxWorkspaceRiskKind.OUTSIDE_ROOT_WRITE_RISK],
                reason,
            )
        return _blocked_path_ref(
            raw_path_ref,
            raw_path_ref.strip().replace("\\", "/"),
            SandboxPathStatus.TRAVERSAL_DETECTED,
            SandboxPathDecisionKind.BLOCK_PATH,
            SandboxEscapeKind.PATH_TRAVERSAL,
            SandboxPathRole.EXTERNAL_PATH,
            [SandboxWorkspaceRiskKind.PATH_TRAVERSAL_RISK, SandboxWorkspaceRiskKind.SANDBOX_ESCAPE_RISK],
            reason,
        )
    lowered = normalized.lower()
    first_segment = _split_path_ref(normalized)[0].lower()
    if first_segment in {"references", "reference"}:
        return _blocked_path_ref(
            raw_path_ref,
            normalized,
            SandboxPathStatus.REFERENCE_ROOT_BLOCKED,
            SandboxPathDecisionKind.BLOCK_REFERENCE_ROOT,
            SandboxEscapeKind.REFERENCE_ROOT_TARGET,
            SandboxPathRole.REFERENCE_ROOT,
            [SandboxWorkspaceRiskKind.REFERENCE_ROOT_WRITE_RISK],
            "reference roots are blocked for sandbox materialization targets",
        )
    if first_segment in {"live", "workspace", ".git"}:
        return _blocked_path_ref(
            raw_path_ref,
            normalized,
            SandboxPathStatus.EXTERNAL_BLOCKED,
            SandboxPathDecisionKind.BLOCK_LIVE_WORKSPACE,
            SandboxEscapeKind.LIVE_WORKSPACE_TARGET,
            SandboxPathRole.LIVE_WORKSPACE_ROOT,
            [SandboxWorkspaceRiskKind.LIVE_WORKSPACE_WRITE_RISK],
            "live workspace roots are blocked",
        )
    if any(token in lowered for token in SECRET_PATH_TOKENS):
        return _blocked_path_ref(
            raw_path_ref,
            normalized,
            SandboxPathStatus.SECRET_BLOCKED,
            SandboxPathDecisionKind.BLOCK_SECRET,
            SandboxEscapeKind.NO_ESCAPE_DETECTED,
            SandboxPathRole.BLOCKED_SECRET_PATH,
            [SandboxWorkspaceRiskKind.SECRET_PATH_RISK],
            "secret-like target path is blocked",
        )
    if any(token in lowered for token in CREDENTIAL_PATH_TOKENS):
        return _blocked_path_ref(
            raw_path_ref,
            normalized,
            SandboxPathStatus.CREDENTIAL_BLOCKED,
            SandboxPathDecisionKind.BLOCK_CREDENTIAL,
            SandboxEscapeKind.NO_ESCAPE_DETECTED,
            SandboxPathRole.BLOCKED_CREDENTIAL_PATH,
            [SandboxWorkspaceRiskKind.CREDENTIAL_PATH_RISK],
            "credential-like target path is blocked",
        )
    if lowered.endswith(BINARY_EXTENSIONS):
        return _blocked_path_ref(
            raw_path_ref,
            normalized,
            SandboxPathStatus.BINARY_BLOCKED,
            SandboxPathDecisionKind.BLOCK_BINARY,
            SandboxEscapeKind.NO_ESCAPE_DETECTED,
            SandboxPathRole.BLOCKED_BINARY_PATH,
            [SandboxWorkspaceRiskKind.BINARY_TARGET_RISK],
            "binary-like target path is blocked",
        )
    return build_sandbox_path_ref(
        path_ref_id=f"sandbox_path_ref:v0.36.3:{normalized.replace('/', '_')}",
        raw_path_ref=raw_path_ref,
        normalized_path_ref=normalized,
        path_role=path_role,
    )


def build_sandbox_file_map_entry(**kwargs: Any) -> SandboxFileMapEntry:
    return SandboxFileMapEntry(
        file_map_entry_id=kwargs.pop("file_map_entry_id", "sandbox_file_map_entry:v0.36.3:src_example"),
        virtual_path_ref=kwargs.pop("virtual_path_ref", "virtual-sandbox-root/src/example.py"),
        source_path_ref=kwargs.pop("source_path_ref", "src/example.py"),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        path_ref_id=kwargs.pop("path_ref_id", "sandbox_path_ref:v0.36.3:src_example"),
        simulated_delta_ids=kwargs.pop("simulated_delta_ids", ["simulated_delta:v0.36.2"]),
        entry_summary=kwargs.pop("entry_summary", "sandbox file map metadata only; no file write"),
        eligible_for_future_materialization=kwargs.pop("eligible_for_future_materialization", True),
        **kwargs,
    )


def build_sandbox_overlay_entry(**kwargs: Any) -> SandboxOverlayEntry:
    return SandboxOverlayEntry(
        overlay_entry_id=kwargs.pop("overlay_entry_id", "sandbox_overlay_entry:v0.36.3:src_example"),
        file_map_entry_id=kwargs.pop("file_map_entry_id", "sandbox_file_map_entry:v0.36.3:src_example"),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        overlay_summary=kwargs.pop("overlay_summary", "virtual overlay metadata only; no materialization"),
        simulated_after_preview=kwargs.pop("simulated_after_preview", "alpha\nBETA\ngamma"),
        delta_kind_summary=kwargs.pop("delta_kind_summary", "simulated_replacement"),
        materialization_mode=kwargs.pop("materialization_mode", OverlayMaterializationMode.METADATA_ONLY),
        eligible_for_future_materialization=kwargs.pop("eligible_for_future_materialization", True),
        **kwargs,
    )


def build_sandbox_workspace_manifest(**kwargs: Any) -> SandboxWorkspaceManifest:
    path_refs = kwargs.pop("path_refs", [build_sandbox_path_ref()])
    file_map_entries = kwargs.pop("file_map_entries", [build_sandbox_file_map_entry()])
    return SandboxWorkspaceManifest(
        manifest_id=kwargs.pop("manifest_id", "sandbox_manifest:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        workspace_input_id=kwargs.pop("workspace_input_id", "sandbox_workspace_input:v0.36.3"),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "virtual-sandbox-root"),
        workspace_mode=kwargs.pop("workspace_mode", SandboxWorkspaceMode.MANIFEST_ONLY),
        path_refs=path_refs,
        file_map_entries=file_map_entries,
        overlay_entries=kwargs.pop("overlay_entries", [build_sandbox_overlay_entry()]),
        source_refs=kwargs.pop("source_refs", [build_sandbox_workspace_source_ref()]),
        manifest_summary=kwargs.pop("manifest_summary", "sandbox workspace manifest metadata only; not materialized"),
        blocked_path_count=kwargs.pop("blocked_path_count", sum(1 for path_ref in path_refs if path_ref.blocked)),
        eligible_entry_count=kwargs.pop("eligible_entry_count", sum(1 for entry in file_map_entries if entry.eligible_for_future_materialization)),
        ready_for_future_materialization_input=kwargs.pop("ready_for_future_materialization_input", True),
        metadata=kwargs.pop("metadata", {"dry_run_successful": True, "blocking_conflicts": 0}),
        **kwargs,
    )


def build_sandbox_workspace_plan(**kwargs: Any) -> SandboxWorkspacePlan:
    return SandboxWorkspacePlan(
        workspace_plan_id=kwargs.pop("workspace_plan_id", "sandbox_workspace_plan:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        manifest_id=kwargs.pop("manifest_id", "sandbox_manifest:v0.36.3"),
        planned_materialization_steps=kwargs.pop("planned_materialization_steps", ["handoff manifest metadata to v0.36.4"]),
        blocked_materialization_steps=kwargs.pop("blocked_materialization_steps", ["directory creation", "file write", "patch apply"]),
        live_write_blocks=kwargs.pop("live_write_blocks", ["live workspace write remains blocked"]),
        future_handoff_notes=kwargs.pop("future_handoff_notes", ["v0.36.4 must add explicit future gate before materialization"]),
        summary=kwargs.pop("summary", "workspace plan metadata only; no workspace creation"),
        ready_for_v0364_sandbox_patch_apply_engine=kwargs.pop("ready_for_v0364_sandbox_patch_apply_engine", True),
        **kwargs,
    )


def build_sandbox_live_write_block(**kwargs: Any) -> SandboxLiveWriteBlock:
    return SandboxLiveWriteBlock(
        live_write_block_id=kwargs.pop("live_write_block_id", "sandbox_live_write_block:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        blocked_root_refs=kwargs.pop("blocked_root_refs", ["workspace-root", ".git", "references"]),
        blocked_path_refs=kwargs.pop("blocked_path_refs", ["live/**", "workspace/**", "../*", "/*"]),
        blocked_reason=kwargs.pop("blocked_reason", "v0.36.3 defines metadata only and blocks live/workspace writes"),
        **kwargs,
    )


def build_sandbox_workspace_gate_decision(**kwargs: Any) -> SandboxWorkspaceGateDecision:
    return SandboxWorkspaceGateDecision(
        gate_decision_id=kwargs.pop("gate_decision_id", "sandbox_gate_decision:v0.36.3"),
        decision_kind=kwargs.pop("decision_kind", SandboxWorkspaceDecisionKind.ALLOW_FUTURE_MATERIALIZATION_INPUT),
        status=kwargs.pop("status", SandboxWorkspaceStatus.FUTURE_MATERIALIZATION_READY),
        summary=kwargs.pop("summary", "future materialization input metadata allowed; no write/apply permission"),
        ready_for_future_materialization_input=kwargs.pop("ready_for_future_materialization_input", True),
        **kwargs,
    )


def build_sandbox_workspace_validation_finding(**kwargs: Any) -> SandboxWorkspaceValidationFinding:
    return SandboxWorkspaceValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_validation_finding:v0.36.3"),
        risk_kind=kwargs.pop("risk_kind", SandboxWorkspaceRiskKind.SANDBOX_WORKSPACE_WRITE_CONFUSION_RISK),
        decision_kind=kwargs.pop("decision_kind", SandboxWorkspaceDecisionKind.REQUIRE_REVIEW),
        path_ref_id=kwargs.pop("path_ref_id", None),
        summary=kwargs.pop("summary", "metadata-only validation finding"),
        blocks_future_materialization=kwargs.pop("blocks_future_materialization", False),
        **kwargs,
    )


def build_sandbox_workspace_validation_report(**kwargs: Any) -> SandboxWorkspaceValidationReport:
    return SandboxWorkspaceValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_validation_report:v0.36.3"),
        manifest_id=kwargs.pop("manifest_id", "sandbox_manifest:v0.36.3"),
        findings=kwargs.pop("findings", []),
        status=kwargs.pop("status", SandboxWorkspaceStatus.MANIFEST_VALIDATED),
        summary=kwargs.pop("summary", "sandbox manifest validation metadata; no filesystem mutation certified"),
        ready_for_future_materialization_input=kwargs.pop("ready_for_future_materialization_input", True),
        **kwargs,
    )


def build_sandbox_workspace_report(**kwargs: Any) -> SandboxWorkspaceReport:
    manifest = kwargs.pop("manifest", build_sandbox_workspace_manifest())
    validation_report = kwargs.pop("validation_report", build_sandbox_workspace_validation_report(manifest_id=manifest.manifest_id))
    gate_decision = kwargs.pop("gate_decision", build_sandbox_workspace_gate_decision())
    return SandboxWorkspaceReport(
        report_id=kwargs.pop("report_id", "sandbox_workspace_report:v0.36.3"),
        manifest=manifest,
        validation_report=validation_report,
        gate_decision=gate_decision,
        summary=kwargs.pop("summary", "sandbox workspace policy report metadata only"),
        manifest_ready=kwargs.pop("manifest_ready", True),
        ready_for_future_materialization_input=kwargs.pop("ready_for_future_materialization_input", manifest.ready_for_future_materialization_input),
        **kwargs,
    )


def build_sandbox_workspace_run_preview(**kwargs: Any) -> SandboxWorkspaceRunPreview:
    return SandboxWorkspaceRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_workspace_run_preview:v0.36.3"),
        manifest_id=kwargs.pop("manifest_id", "sandbox_manifest:v0.36.3"),
        preview_summary=kwargs.pop("preview_summary", "preview describes metadata construction only"),
        planned_metadata_actions=kwargs.pop("planned_metadata_actions", ["classify paths", "build manifest", "build overlay metadata"]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        ready_for_future_materialization_input=kwargs.pop("ready_for_future_materialization_input", True),
        **kwargs,
    )


def build_sandbox_workspace_no_live_write_guarantee(**kwargs: Any) -> SandboxWorkspaceNoLiveWriteGuarantee:
    return SandboxWorkspaceNoLiveWriteGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_no_live_write_guarantee:v0.36.3"),
        version=kwargs.pop("version", V0363_VERSION),
        no_sandbox_directory_creation=kwargs.pop("no_sandbox_directory_creation", True),
        no_sandbox_workspace_materialization=kwargs.pop("no_sandbox_workspace_materialization", True),
        no_sandbox_file_write=kwargs.pop("no_sandbox_file_write", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_sandbox_patch_apply=kwargs.pop("no_sandbox_patch_apply", True),
        no_patch_application=kwargs.pop("no_patch_application", True),
        no_workspace_write=kwargs.pop("no_workspace_write", True),
        no_code_edit=kwargs.pop("no_code_edit", True),
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


def build_v0363_readiness_report(**kwargs: Any) -> V0363ReadinessReport:
    return V0363ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0363_readiness_report"),
        version=kwargs.pop("version", V0363_VERSION),
        release_name=kwargs.pop("release_name", V0363_RELEASE_NAME),
        status=kwargs.pop("status", SandboxWorkspaceStatus.FUTURE_MATERIALIZATION_READY),
        readiness_level=kwargs.pop("readiness_level", SandboxWorkspaceReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0364),
        ready_for_v0364_sandbox_patch_apply_engine=kwargs.pop("ready_for_v0364_sandbox_patch_apply_engine", True),
        ready_for_v0365_sandbox_post_apply_validation=kwargs.pop("ready_for_v0365_sandbox_post_apply_validation", True),
        ready_for_sandbox_workspace_policy=kwargs.pop("ready_for_sandbox_workspace_policy", True),
        ready_for_sandbox_root_policy=kwargs.pop("ready_for_sandbox_root_policy", True),
        ready_for_overlay_policy=kwargs.pop("ready_for_overlay_policy", True),
        ready_for_sandbox_workspace_manifest=kwargs.pop("ready_for_sandbox_workspace_manifest", True),
        ready_for_sandbox_file_map=kwargs.pop("ready_for_sandbox_file_map", True),
        ready_for_live_workspace_write_block=kwargs.pop("ready_for_live_workspace_write_block", True),
        ready_for_future_sandbox_materialization_input=kwargs.pop("ready_for_future_sandbox_materialization_input", True),
        digestion_first_policy_applied=kwargs.pop("digestion_first_policy_applied", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_agent_loop_blocked=kwargs.pop("infinite_agent_loop_blocked", True),
        bounded_agentic_task_only=kwargs.pop("bounded_agentic_task_only", True),
        no_independent_autonomous_agent_runtime=kwargs.pop("no_independent_autonomous_agent_runtime", True),
        **kwargs,
    )


def build_sandbox_workspace_input_from_dry_run_result(result: DryRunApplySimulationResult, **kwargs: Any) -> SandboxWorkspaceInput:
    target_refs = [file_result.target_path_ref for file_result in result.file_results]
    return build_sandbox_workspace_input(
        dry_run_result_id=result.simulation_result_id,
        requested_target_path_refs=target_refs,
        source_refs=[build_sandbox_workspace_source_ref(source_id=result.simulation_result_id)],
        metadata={
            "dry_run_successful": result.simulation_successful,
            "blocking_conflicts": result.blocking_conflict_count,
            "dry_run_status": str(result.status),
        },
        **kwargs,
    )


def _file_map_and_overlay_from_delta(
    delta: DryRunSimulatedFileDelta,
    path_ref: SandboxPathRef,
    blocking_conflicts: int,
    index: int,
) -> tuple[SandboxFileMapEntry, SandboxOverlayEntry]:
    eligible = not path_ref.blocked and blocking_conflicts == 0 and not delta.conflict_ids
    file_map = build_sandbox_file_map_entry(
        file_map_entry_id=f"sandbox_file_map_entry:v0.36.3:{index}",
        virtual_path_ref=f"virtual-sandbox-root/{path_ref.normalized_path_ref}",
        source_path_ref=delta.target_path_ref,
        target_path_ref=delta.target_path_ref,
        path_ref_id=path_ref.path_ref_id,
        simulated_delta_ids=[delta.simulated_delta_id],
        eligible_for_future_materialization=eligible,
        metadata={"path_blocked": path_ref.blocked, "blocking_conflicts": blocking_conflicts + len(delta.conflict_ids)},
    )
    overlay = build_sandbox_overlay_entry(
        overlay_entry_id=f"sandbox_overlay_entry:v0.36.3:{index}",
        file_map_entry_id=file_map.file_map_entry_id,
        target_path_ref=delta.target_path_ref,
        simulated_after_preview=_bounded_preview(delta.after_preview),
        delta_kind_summary=str(delta.delta_kind),
        eligible_for_future_materialization=eligible,
        redacted=_bounded_preview(delta.after_preview) != delta.after_preview,
        truncated=len(delta.after_preview) > MAX_PREVIEW_CHARS,
        metadata={"path_ref_id": path_ref.path_ref_id},
    )
    return file_map, overlay


def build_sandbox_manifest_from_dry_run_result(
    result: DryRunApplySimulationResult,
    workspace_input: SandboxWorkspaceInput | None = None,
    policy: SandboxWorkspacePolicy | None = None,
    **kwargs: Any,
) -> SandboxWorkspaceManifest:
    active_input = workspace_input or build_sandbox_workspace_input_from_dry_run_result(result)
    active_policy = policy or default_sandbox_workspace_policy()
    path_refs: list[SandboxPathRef] = []
    file_map_entries: list[SandboxFileMapEntry] = []
    overlay_entries: list[SandboxOverlayEntry] = []
    index = 1
    for file_result in result.file_results:
        if not isinstance(file_result, DryRunSimulatedFileResult):
            raise TypeError("file_results must contain DryRunSimulatedFileResult")
        deltas = file_result.simulated_deltas or []
        if not deltas:
            path_ref = classify_sandbox_path_ref(file_result.target_path_ref)
            path_refs.append(path_ref)
            continue
        for delta in deltas:
            if not isinstance(delta, DryRunSimulatedFileDelta):
                raise TypeError("simulated_deltas must contain DryRunSimulatedFileDelta")
            path_ref = classify_sandbox_path_ref(delta.target_path_ref)
            path_refs.append(path_ref)
            file_map, overlay = _file_map_and_overlay_from_delta(delta, path_ref, result.blocking_conflict_count, index)
            file_map_entries.append(file_map)
            overlay_entries.append(overlay)
            index += 1
    blocked_path_count = sum(1 for path_ref in path_refs if path_ref.blocked)
    ready_for_future = (
        active_policy.allow_future_materialization_input
        and result.simulation_successful
        and result.blocking_conflict_count == 0
        and blocked_path_count == 0
        and all(entry.eligible_for_future_materialization for entry in file_map_entries)
    )
    return build_sandbox_workspace_manifest(
        manifest_id=kwargs.pop("manifest_id", f"sandbox_manifest:v0.36.3:{result.simulation_result_id}"),
        workspace_input_id=active_input.workspace_input_id,
        sandbox_root_ref=active_input.requested_sandbox_root_ref,
        workspace_mode=active_input.requested_mode,
        path_refs=path_refs,
        file_map_entries=file_map_entries,
        overlay_entries=overlay_entries,
        source_refs=active_input.source_refs,
        blocked_path_count=blocked_path_count,
        eligible_entry_count=sum(1 for entry in file_map_entries if entry.eligible_for_future_materialization),
        ready_for_future_materialization_input=ready_for_future,
        metadata={
            "dry_run_result_id": result.simulation_result_id,
            "dry_run_successful": result.simulation_successful,
            "blocking_conflicts": result.blocking_conflict_count,
        },
        **kwargs,
    )


def validate_sandbox_workspace_manifest(manifest: SandboxWorkspaceManifest) -> SandboxWorkspaceValidationReport:
    findings: list[SandboxWorkspaceValidationFinding] = []
    for path_ref in manifest.path_refs:
        if path_ref.blocked:
            risk = path_ref.risk_kinds[0] if path_ref.risk_kinds else SandboxWorkspaceRiskKind.BLOCKED_TARGET_RISK
            findings.append(
                build_sandbox_workspace_validation_finding(
                    finding_id=f"sandbox_validation_finding:v0.36.3:{path_ref.path_ref_id}",
                    risk_kind=risk,
                    decision_kind=SandboxWorkspaceDecisionKind.BLOCK,
                    path_ref_id=path_ref.path_ref_id,
                    summary=path_ref.block_reason or "blocked sandbox path",
                    blocks_future_materialization=True,
                )
            )
    if manifest.metadata.get("blocking_conflicts"):
        findings.append(
            build_sandbox_workspace_validation_finding(
                finding_id="sandbox_validation_finding:v0.36.3:blocking_dry_run_conflict",
                risk_kind=SandboxWorkspaceRiskKind.UNRESOLVED_DRY_RUN_CONFLICT_RISK,
                decision_kind=SandboxWorkspaceDecisionKind.BLOCK,
                path_ref_id=None,
                summary="dry-run result has blocking conflicts",
                blocks_future_materialization=True,
            )
        )
    ready = manifest.ready_for_future_materialization_input and not findings
    return build_sandbox_workspace_validation_report(
        manifest_id=manifest.manifest_id,
        findings=findings,
        status=SandboxWorkspaceStatus.MANIFEST_VALIDATED if ready else SandboxWorkspaceStatus.MANIFEST_VALIDATED_WITH_GAPS,
        ready_for_future_materialization_input=ready,
    )


def sandbox_workspace_flags_preserve_no_write(flags: SandboxWorkspaceFlagSet) -> bool:
    return isinstance(flags, SandboxWorkspaceFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def sandbox_root_policy_blocks_live_write(policy: SandboxRootPolicy) -> bool:
    return (
        policy.allow_directory_creation is False
        and policy.allow_file_write is False
        and policy.allow_live_workspace_write is False
        and policy.block_absolute_targets is True
        and policy.block_path_traversal is True
        and policy.block_outside_root is True
    )


def sandbox_overlay_policy_blocks_materialization(policy: SandboxOverlayPolicy) -> bool:
    return not any(
        getattr(policy, name)
        for name in (
            "allow_sandbox_materialization",
            "allow_sandbox_file_write",
            "allow_live_file_write",
            "allow_patch_apply",
            "allow_apply_patch",
            "allow_git_apply",
        )
    )


def sandbox_workspace_manifest_is_not_materialized(manifest: SandboxWorkspaceManifest) -> bool:
    return not any(
        getattr(manifest, name)
        for name in (
            "materialized",
            "ready_for_sandbox_workspace_materialization",
            "ready_for_sandbox_workspace_write",
            "ready_for_sandbox_patch_apply",
            "ready_for_live_workspace_write",
            "ready_for_execution",
        )
    )


def sandbox_live_write_block_blocks_live_write(block: SandboxLiveWriteBlock) -> bool:
    return not any(
        getattr(block, name)
        for name in (
            "live_workspace_write_allowed",
            "workspace_write_allowed",
            "code_edit_allowed",
            "patch_application_allowed",
        )
    )


def v0363_readiness_report_is_not_execution_ready(report: V0363ReadinessReport) -> bool:
    return isinstance(report, V0363ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
