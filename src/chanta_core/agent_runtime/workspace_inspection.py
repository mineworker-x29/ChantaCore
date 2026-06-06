from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any
import fnmatch

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)


V0335_VERSION = "v0.33.5"
V0335_RELEASE_NAME = "v0.33.5 Safe Workspace Inspection Tool Pack"

DEFAULT_WORKSPACE_SECRET_PATTERNS = [
    ".env",
    "*.env",
    "*secret*",
    "*key*",
    "*token*",
    "*credential*",
    "*.pem",
    "id_rsa",
    "*id_rsa*",
]

DEFAULT_ALLOWED_TEXT_EXTENSIONS = [
    ".cfg",
    ".csv",
    ".ini",
    ".json",
    ".log",
    ".md",
    ".py",
    ".rst",
    ".toml",
    ".tsv",
    ".txt",
    ".yaml",
    ".yml",
]

DEFAULT_PROHIBITED_UNTIL_LATER_GATE = [
    "shell command",
    "subprocess",
    "network access",
    "credential access",
    "workspace write",
    "code edit",
    "patch application",
    "reference code execution",
    "reference import",
    "dependency install",
    "secret file read",
    "binary file read",
    "model invocation",
    "provider invocation",
    "agent step execution",
    "registry mutation",
    "memory mutation",
    "OCEL emission",
    "runtime trace persistence",
    "UI runtime",
    "external control",
    "authority grant",
]


class WorkspaceInspectionToolKind(StrEnum):
    INSPECT_PROJECT_TREE_READONLY = "inspect_project_tree_readonly"
    INSPECT_FILE_METADATA_READONLY = "inspect_file_metadata_readonly"
    READ_TEXT_FILE_SAFE = "read_text_file_safe"
    SEARCH_TEXT_IN_WORKSPACE_READONLY = "search_text_in_workspace_readonly"
    SUMMARIZE_REFERENCE_INVENTORY_READONLY = "summarize_reference_inventory_readonly"
    INSPECT_WORKSPACE_PATH_READONLY = "inspect_workspace_path_readonly"
    TEST_WORKSPACE_INSPECTION_TOOL = "test_workspace_inspection_tool"
    UNKNOWN = "unknown"


class WorkspaceInspectionRequestKind(StrEnum):
    INSPECT_TREE = "inspect_tree"
    INSPECT_METADATA = "inspect_metadata"
    READ_SAFE_TEXT = "read_safe_text"
    SEARCH_SAFE_TEXT = "search_safe_text"
    SUMMARIZE_REFERENCE_INVENTORY = "summarize_reference_inventory"
    INSPECT_PATH = "inspect_path"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class WorkspaceInspectionDecisionKind(StrEnum):
    ALLOW_SAFE_METADATA_INSPECTION = "allow_safe_metadata_inspection"
    ALLOW_SAFE_TREE_INSPECTION = "allow_safe_tree_inspection"
    ALLOW_SAFE_TEXT_READ = "allow_safe_text_read"
    ALLOW_SAFE_TEXT_SEARCH = "allow_safe_text_search"
    ALLOW_SAFE_REFERENCE_INVENTORY_SUMMARY = "allow_safe_reference_inventory_summary"
    DENY = "deny"
    BLOCK = "block"
    SKIP = "skip"
    NO_OP = "no_op"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class WorkspaceInspectionSkipReasonKind(StrEnum):
    OUTSIDE_ALLOWED_ROOT = "outside_allowed_root"
    PATH_NOT_FOUND = "path_not_found"
    PATH_IS_SYMLINK_OUTSIDE_ROOT = "path_is_symlink_outside_root"
    PATH_IS_SECRET_LIKE = "path_is_secret_like"
    PATH_MATCHES_PROHIBITED_PATTERN = "path_matches_prohibited_pattern"
    PATH_IS_BINARY = "path_is_binary"
    FILE_TOO_LARGE = "file_too_large"
    EXTENSION_NOT_ALLOWED = "extension_not_allowed"
    DIRECTORY_DEPTH_EXCEEDED = "directory_depth_exceeded"
    ITEM_LIMIT_EXCEEDED = "item_limit_exceeded"
    OUTPUT_LIMIT_EXCEEDED = "output_limit_exceeded"
    PERMISSION_ERROR = "permission_error"
    DECODE_ERROR = "decode_error"
    UNSUPPORTED_REQUEST = "unsupported_request"
    UNSAFE_REFERENCE_PATH = "unsafe_reference_path"
    UNKNOWN = "unknown"


class WorkspaceInspectionRiskKind(StrEnum):
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    SECRET_FILE_RISK = "secret_file_risk"
    BINARY_FILE_RISK = "binary_file_risk"
    OVERSIZED_FILE_RISK = "oversized_file_risk"
    UNBOUNDED_TRAVERSAL_RISK = "unbounded_traversal_risk"
    UNBOUNDED_OUTPUT_RISK = "unbounded_output_risk"
    REFERENCE_CODE_EXECUTION_RISK = "reference_code_execution_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    UNKNOWN = "unknown"


class WorkspaceInspectionResultKind(StrEnum):
    TREE_RESULT = "tree_result"
    METADATA_RESULT = "metadata_result"
    SAFE_TEXT_READ_RESULT = "safe_text_read_result"
    TEXT_SEARCH_RESULT = "text_search_result"
    REFERENCE_INVENTORY_SUMMARY = "reference_inventory_summary"
    DENIED_RESULT = "denied_result"
    SKIPPED_RESULT = "skipped_result"
    NO_OP_RESULT = "no_op_result"
    ERROR_RESULT = "error_result"
    UNKNOWN = "unknown"


class WorkspaceInspectionStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    POLICY_CHECKED = "policy_checked"
    ALLOWED = "allowed"
    DENIED = "denied"
    SKIPPED = "skipped"
    COMPLETED = "completed"
    COMPLETED_WITH_SKIPS = "completed_with_skips"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class WorkspaceInspectionReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    POLICY_CONTRACT_READY = "policy_contract_ready"
    SAFE_METADATA_INSPECTION_READY = "safe_metadata_inspection_ready"
    SAFE_READONLY_INSPECTION_READY = "safe_readonly_inspection_ready"
    DESIGN_HANDOFF_READY_FOR_V0336 = "design_handoff_ready_for_v0336"
    DESIGN_HANDOFF_READY_FOR_V0337 = "design_handoff_ready_for_v0337"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class WorkspaceInspectionSourceKind(StrEnum):
    V0334_READONLY_TOOL_REGISTRY = "v0334_readonly_tool_registry"
    V0333_SESSION_RUNTIME = "v0333_session_runtime"
    V0332_PROMPT_ASSEMBLY = "v0332_prompt_assembly"
    V0331_PROFILE_RUNTIME = "v0331_profile_runtime"
    V0330_RUNTIME_BOUNDARY = "v0330_runtime_boundary"
    WORKSPACE_ROOT = "workspace_root"
    REFERENCES_ROOT = "references_root"
    OPENCODE_REFERENCE_PATH = "opencode_reference_path"
    HERMES_REFERENCE_PATH = "hermes_reference_path"
    OPENCLAW_REFERENCE_PATH = "openclaw_reference_path"
    TEST_FIXTURE = "test_fixture"
    MANUAL_INSPECTION_REQUEST = "manual_inspection_request"
    UNKNOWN = "unknown"


UNSAFE_RUNTIME_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_tool_execution",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_agent_step_execution",
    "ready_for_model_step_execution",
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

ALLOWED_DECISION_KINDS = {
    WorkspaceInspectionDecisionKind.ALLOW_SAFE_METADATA_INSPECTION,
    WorkspaceInspectionDecisionKind.ALLOW_SAFE_TREE_INSPECTION,
    WorkspaceInspectionDecisionKind.ALLOW_SAFE_TEXT_READ,
    WorkspaceInspectionDecisionKind.ALLOW_SAFE_TEXT_SEARCH,
    WorkspaceInspectionDecisionKind.ALLOW_SAFE_REFERENCE_INVENTORY_SUMMARY,
}


def _validate_version_includes_v0335(version: str) -> None:
    _require_non_blank("version", version)
    if V0335_VERSION not in version:
        raise ValueError("version must include v0.33.5")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.5")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_non_negative_int(name: str, value: int | None) -> None:
    if value is not None and (not isinstance(value, int) or value < 0):
        raise ValueError(f"{name} must be None or >= 0")


def _validate_source_ref_list(values: list["WorkspaceInspectionSourceRef"]) -> None:
    _validate_object_list("source_refs", values, WorkspaceInspectionSourceRef)


def _validate_denied_record_list(name: str, values: list["WorkspaceInspectionDeniedRecord"]) -> None:
    _validate_object_list(name, values, WorkspaceInspectionDeniedRecord)


def _validate_secret_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited_file_patterns", values)
    lowered = [value.lower() for value in values]
    for required in (".env", "secret", "key", "token", "credential", "pem", "id_rsa"):
        if not any(required in value for value in lowered):
            raise ValueError("prohibited_file_patterns must include secret-like defaults")


def _path_is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def _normalize_extension(extension: str) -> str:
    value = extension.lower()
    return value if value.startswith(".") else f".{value}"


@dataclass(frozen=True)
class WorkspaceInspectionFlagSet:
    flag_set_id: str
    version: str = V0335_VERSION
    safe_workspace_inspection_tool_pack_constructed: bool = False
    safe_path_policy_available: bool = False
    safe_metadata_inspection_enabled: bool = False
    safe_tree_inspection_enabled: bool = False
    safe_text_read_enabled: bool = False
    safe_text_search_enabled: bool = False
    safe_reference_inventory_summary_enabled: bool = False
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_file_read: bool = False
    ready_for_reference_file_access: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_model_step_execution: bool = False
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
        _validate_version_includes_v0335(self.version)
        _validate_false(self, UNSAFE_RUNTIME_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"general_runtime", "command_execution", "workspace_write"}):
            raise ValueError("WorkspaceInspectionFlagSet is not general runtime readiness")


@dataclass(frozen=True)
class WorkspaceInspectionSourceRef:
    source_ref_id: str
    source_kind: WorkspaceInspectionSourceKind | str
    source_id: str
    source_summary: str
    path_ref: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        WorkspaceInspectionSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"execution", "reference_code_execution"}):
            raise ValueError("WorkspaceInspectionSourceRef is not execution")

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class WorkspaceInspectionLimits:
    limits_id: str
    max_depth: int = 3
    max_entries: int = 200
    max_file_size_bytes: int = 128_000
    max_read_chars: int = 8_000
    max_search_matches: int = 50
    max_search_files: int = 100
    max_line_length: int = 400
    allowed_text_extensions: list[str] = field(default_factory=lambda: list(DEFAULT_ALLOWED_TEXT_EXTENSIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("limits_id", self.limits_id)
        for name in (
            "max_depth",
            "max_entries",
            "max_file_size_bytes",
            "max_read_chars",
            "max_search_matches",
            "max_search_files",
            "max_line_length",
        ):
            _validate_non_negative_int(name, getattr(self, name))
        _validate_string_list("allowed_text_extensions", self.allowed_text_extensions)
        object.__setattr__(self, "allowed_text_extensions", [_normalize_extension(value) for value in self.allowed_text_extensions])
        if _metadata_flag_true(self.metadata, {"unbounded_traversal", "unbounded_output"}):
            raise ValueError("WorkspaceInspectionLimits must prevent unbounded traversal/output")


@dataclass(frozen=True)
class WorkspaceInspectionRootPolicy:
    root_policy_id: str
    allowed_root_refs: list[str]
    blocked_root_refs: list[str] = field(default_factory=list)
    allow_references_root: bool = False
    allow_opencode_reference_root: bool = False
    allow_hermes_reference_root: bool = False
    allow_openclaw_reference_root: bool = False
    allow_symlinks: bool = False
    allow_symlink_escape: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("root_policy_id", self.root_policy_id)
        _validate_string_list("allowed_root_refs", self.allowed_root_refs)
        _validate_string_list("blocked_root_refs", self.blocked_root_refs)
        if self.allow_symlink_escape is not False:
            raise ValueError("allow_symlink_escape must always be False")
        if _metadata_flag_true(self.metadata, {"reference_execution", "dependency_install"}):
            raise ValueError("Reference roots do not permit execution/import/install")


@dataclass(frozen=True)
class WorkspaceInspectionPathPolicy:
    path_policy_id: str
    root_policy: WorkspaceInspectionRootPolicy
    limits: WorkspaceInspectionLimits
    prohibited_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_WORKSPACE_SECRET_PATTERNS))
    prohibited_dir_patterns: list[str] = field(default_factory=list)
    prohibited_extensions: list[str] = field(default_factory=list)
    allowed_text_extensions: list[str] = field(default_factory=lambda: list(DEFAULT_ALLOWED_TEXT_EXTENSIONS))
    allow_binary_read: bool = False
    allow_secret_read: bool = False
    allow_workspace_write: bool = False
    allow_command_execution: bool = False
    allow_network_access: bool = False
    allow_credential_access: bool = False
    allow_reference_code_execution: bool = False
    allow_reference_import: bool = False
    allow_dependency_install: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("path_policy_id", self.path_policy_id)
        if not isinstance(self.root_policy, WorkspaceInspectionRootPolicy):
            raise TypeError("root_policy must be WorkspaceInspectionRootPolicy")
        if not isinstance(self.limits, WorkspaceInspectionLimits):
            raise TypeError("limits must be WorkspaceInspectionLimits")
        _validate_secret_patterns(self.prohibited_file_patterns)
        for name in ("prohibited_dir_patterns", "prohibited_extensions", "allowed_text_extensions"):
            _validate_string_list(name, getattr(self, name))
        object.__setattr__(self, "allowed_text_extensions", [_normalize_extension(value) for value in self.allowed_text_extensions])
        object.__setattr__(self, "prohibited_extensions", [_normalize_extension(value) for value in self.prohibited_extensions])
        _validate_false(
            self,
            (
                "allow_binary_read",
                "allow_secret_read",
                "allow_workspace_write",
                "allow_command_execution",
                "allow_network_access",
                "allow_credential_access",
                "allow_reference_code_execution",
                "allow_reference_import",
                "allow_dependency_install",
            ),
        )


@dataclass(frozen=True)
class WorkspaceInspectionRequest:
    request_id: str
    request_kind: WorkspaceInspectionRequestKind | str
    tool_kind: WorkspaceInspectionToolKind | str
    path_ref: str | None = None
    query: str | None = None
    source_refs: list[WorkspaceInspectionSourceRef] = field(default_factory=list)
    request_summary: str = "Safe workspace inspection request pending policy validation."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("request_id", self.request_id)
        WorkspaceInspectionRequestKind(self.request_kind)
        WorkspaceInspectionToolKind(self.tool_kind)
        if self.query is not None and (not isinstance(self.query, str) or len(self.query) > 500):
            raise ValueError("query must be None or bounded string")
        _validate_source_ref_list(self.source_refs)
        _require_non_blank("request_summary", self.request_summary)
        if _metadata_flag_true(self.metadata, {"command_execution", "general_tool_execution"}):
            raise ValueError("WorkspaceInspectionRequest is not execution until policy allows safe inspection")


@dataclass(frozen=True)
class WorkspaceInspectionDecision:
    decision_id: str
    request_id: str
    decision_kind: WorkspaceInspectionDecisionKind | str
    status: WorkspaceInspectionStatus | str
    normalized_path_ref: str | None
    reason: str
    skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] = field(default_factory=list)
    risk_kinds: list[WorkspaceInspectionRiskKind | str] = field(default_factory=list)
    safe_readonly_allowed: bool = False
    file_read_allowed: bool = False
    reference_file_access_allowed: bool = False
    command_execution_allowed: bool = False
    network_access_allowed: bool = False
    credential_access_allowed: bool = False
    workspace_write_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("request_id", self.request_id)
        decision_kind = WorkspaceInspectionDecisionKind(self.decision_kind)
        WorkspaceInspectionStatus(self.status)
        _require_non_blank("reason", self.reason)
        _validate_enum_list("skip_reasons", self.skip_reasons, WorkspaceInspectionSkipReasonKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, WorkspaceInspectionRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(
            self,
            (
                "command_execution_allowed",
                "network_access_allowed",
                "credential_access_allowed",
                "workspace_write_allowed",
            ),
        )
        if self.safe_readonly_allowed and decision_kind not in ALLOWED_DECISION_KINDS:
            raise ValueError("safe_readonly_allowed may be True only for allow safe inspection decisions")
        if self.file_read_allowed and decision_kind != WorkspaceInspectionDecisionKind.ALLOW_SAFE_TEXT_READ:
            raise ValueError("file_read_allowed may be True only for safe text read")
        if _metadata_flag_true(self.metadata, {"shell_execution", "command_execution"}):
            raise ValueError("WorkspaceInspectionDecision is not shell/command execution")


@dataclass(frozen=True)
class WorkspaceInspectionDeniedRecord:
    denied_record_id: str
    request_id: str | None = None
    decision_id: str | None = None
    path_ref: str | None = None
    skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] = field(default_factory=list)
    risk_kinds: list[WorkspaceInspectionRiskKind | str] = field(default_factory=list)
    reason: str = "Denied by safe workspace inspection policy."
    safe_alternatives: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_record_id", self.denied_record_id)
        _validate_enum_list("skip_reasons", self.skip_reasons, WorkspaceInspectionSkipReasonKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, WorkspaceInspectionRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        if _metadata_flag_true(self.metadata, {"sensitive_content", "secret_content"}):
            raise ValueError("WorkspaceInspectionDeniedRecord must not include sensitive file content")


@dataclass(frozen=True)
class WorkspacePathMetadata:
    metadata_id: str
    path_ref: str
    name: str
    suffix: str | None
    is_file: bool
    is_dir: bool
    is_symlink: bool
    size_bytes: int | None = None
    modified_time: float | None = None
    skipped: bool = False
    skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("metadata_id", self.metadata_id)
        _require_non_blank("path_ref", self.path_ref)
        _require_non_blank("name", self.name)
        _validate_non_negative_int("size_bytes", self.size_bytes)
        _validate_enum_list("skip_reasons", self.skip_reasons, WorkspaceInspectionSkipReasonKind)
        if _metadata_flag_true(self.metadata, {"file_content", "raw_content"}):
            raise ValueError("WorkspacePathMetadata must not contain file content")


@dataclass(frozen=True)
class WorkspaceTreeEntry:
    entry_id: str
    path_metadata: WorkspacePathMetadata
    depth: int
    child_count: int | None = None
    included: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("entry_id", self.entry_id)
        if not isinstance(self.path_metadata, WorkspacePathMetadata):
            raise TypeError("path_metadata must be WorkspacePathMetadata")
        _validate_non_negative_int("depth", self.depth)
        _validate_non_negative_int("child_count", self.child_count)
        if _metadata_flag_true(self.metadata, {"file_content", "raw_content"}):
            raise ValueError("WorkspaceTreeEntry must not contain file content")


@dataclass(frozen=True)
class WorkspaceTreeInspectionResult:
    result_id: str
    request_id: str
    decision_id: str
    root_path_ref: str
    entries: list[WorkspaceTreeEntry]
    skipped_paths: list[WorkspaceInspectionDeniedRecord] = field(default_factory=list)
    truncated: bool = False
    status: WorkspaceInspectionStatus | str = WorkspaceInspectionStatus.COMPLETED
    summary: str = "Read-only tree metadata result."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "request_id", "decision_id", "root_path_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_object_list("entries", self.entries, WorkspaceTreeEntry)
        _validate_denied_record_list("skipped_paths", self.skipped_paths)
        WorkspaceInspectionStatus(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")


@dataclass(frozen=True)
class WorkspaceFileMetadataResult:
    result_id: str
    request_id: str
    decision_id: str
    path_metadata: WorkspacePathMetadata
    status: WorkspaceInspectionStatus | str = WorkspaceInspectionStatus.COMPLETED
    summary: str = "Read-only file metadata result."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "request_id", "decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        if not isinstance(self.path_metadata, WorkspacePathMetadata):
            raise TypeError("path_metadata must be WorkspacePathMetadata")
        WorkspaceInspectionStatus(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        if _metadata_flag_true(self.metadata, {"file_content", "raw_content"}):
            raise ValueError("WorkspaceFileMetadataResult must not contain file content")


@dataclass(frozen=True)
class WorkspaceSafeTextReadResult:
    result_id: str
    request_id: str
    decision_id: str
    path_ref: str
    text_excerpt: str
    encoding: str | None
    chars_returned: int
    file_size_bytes: int | None
    truncated: bool
    redacted: bool
    skipped: bool
    skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] = field(default_factory=list)
    status: WorkspaceInspectionStatus | str = WorkspaceInspectionStatus.COMPLETED
    summary: str = "Bounded safe text read result."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "request_id", "decision_id", "path_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_non_negative_int("chars_returned", self.chars_returned)
        _validate_non_negative_int("file_size_bytes", self.file_size_bytes)
        _validate_enum_list("skip_reasons", self.skip_reasons, WorkspaceInspectionSkipReasonKind)
        WorkspaceInspectionStatus(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        max_chars = self.metadata.get("max_read_chars")
        if isinstance(max_chars, int) and len(self.text_excerpt) > max_chars:
            raise ValueError("text_excerpt must be bounded by max_read_chars")
        if WorkspaceInspectionSkipReasonKind.PATH_IS_SECRET_LIKE in self.skip_reasons and self.text_excerpt:
            raise ValueError("secret-like file content must not be returned")


@dataclass(frozen=True)
class WorkspaceTextSearchMatch:
    match_id: str
    path_ref: str
    line_number: int | None
    line_excerpt: str
    match_preview: str
    redacted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("match_id", self.match_id)
        _require_non_blank("path_ref", self.path_ref)
        if self.line_number is not None and self.line_number < 1:
            raise ValueError("line_number must be None or >= 1")
        max_line_length = self.metadata.get("max_line_length")
        if isinstance(max_line_length, int):
            if len(self.line_excerpt) > max_line_length or len(self.match_preview) > max_line_length:
                raise ValueError("line excerpts must be bounded")
        if _metadata_flag_true(self.metadata, {"secret_content", "secret_file"}):
            raise ValueError("WorkspaceTextSearchMatch must not be from secret-like file")


@dataclass(frozen=True)
class WorkspaceTextSearchResult:
    result_id: str
    request_id: str
    decision_id: str
    query: str
    root_path_ref: str
    matches: list[WorkspaceTextSearchMatch]
    skipped_paths: list[WorkspaceInspectionDeniedRecord] = field(default_factory=list)
    searched_file_count: int = 0
    truncated: bool = False
    status: WorkspaceInspectionStatus | str = WorkspaceInspectionStatus.COMPLETED
    summary: str = "Bounded safe text search result."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "request_id", "decision_id", "query", "root_path_ref", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_object_list("matches", self.matches, WorkspaceTextSearchMatch)
        _validate_denied_record_list("skipped_paths", self.skipped_paths)
        _validate_non_negative_int("searched_file_count", self.searched_file_count)
        WorkspaceInspectionStatus(self.status)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        max_matches = self.metadata.get("max_search_matches")
        max_files = self.metadata.get("max_search_files")
        if isinstance(max_matches, int) and len(self.matches) > max_matches:
            raise ValueError("matches must be bounded by max_search_matches")
        if isinstance(max_files, int) and self.searched_file_count > max_files:
            raise ValueError("searched_file_count must be bounded by max_search_files")


@dataclass(frozen=True)
class WorkspaceInspectionToolResult:
    tool_result_id: str
    request_id: str
    decision_id: str
    result_kind: WorkspaceInspectionResultKind | str
    tree_result: WorkspaceTreeInspectionResult | None = None
    metadata_result: WorkspaceFileMetadataResult | None = None
    text_read_result: WorkspaceSafeTextReadResult | None = None
    text_search_result: WorkspaceTextSearchResult | None = None
    denied_records: list[WorkspaceInspectionDeniedRecord] = field(default_factory=list)
    status: WorkspaceInspectionStatus | str = WorkspaceInspectionStatus.COMPLETED
    summary: str = "Safe workspace inspection result."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("tool_result_id", "request_id", "decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        result_kind = WorkspaceInspectionResultKind(self.result_kind)
        WorkspaceInspectionStatus(self.status)
        _validate_denied_record_list("denied_records", self.denied_records)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        primary_count = sum(
            value is not None
            for value in (self.tree_result, self.metadata_result, self.text_read_result, self.text_search_result)
        )
        if result_kind in {
            WorkspaceInspectionResultKind.TREE_RESULT,
            WorkspaceInspectionResultKind.METADATA_RESULT,
            WorkspaceInspectionResultKind.SAFE_TEXT_READ_RESULT,
            WorkspaceInspectionResultKind.TEXT_SEARCH_RESULT,
            WorkspaceInspectionResultKind.REFERENCE_INVENTORY_SUMMARY,
        } and primary_count != 1:
            raise ValueError("completed result kinds require exactly one primary result")
        if result_kind in {
            WorkspaceInspectionResultKind.DENIED_RESULT,
            WorkspaceInspectionResultKind.SKIPPED_RESULT,
            WorkspaceInspectionResultKind.NO_OP_RESULT,
            WorkspaceInspectionResultKind.ERROR_RESULT,
        } and primary_count > 1:
            raise ValueError("denied/skipped/no-op/error result cannot contain multiple primary results")


@dataclass(frozen=True)
class WorkspaceInspectionToolPack:
    tool_pack_id: str
    version: str
    supported_tool_kinds: list[WorkspaceInspectionToolKind | str]
    path_policy: WorkspaceInspectionPathPolicy
    flags: WorkspaceInspectionFlagSet
    source_refs: list[WorkspaceInspectionSourceRef] = field(default_factory=list)
    summary: str = "v0.33.5 bounded safe read-only workspace inspection tool pack."
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("tool_pack_id", "version", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0335(self.version)
        _validate_enum_list("supported_tool_kinds", self.supported_tool_kinds, WorkspaceInspectionToolKind)
        if not isinstance(self.path_policy, WorkspaceInspectionPathPolicy):
            raise TypeError("path_policy must be WorkspaceInspectionPathPolicy")
        if not isinstance(self.flags, WorkspaceInspectionFlagSet):
            raise TypeError("flags must be WorkspaceInspectionFlagSet")
        if not workspace_inspection_flags_preserve_unsafe_runtime_false(self.flags):
            raise ValueError("flags must preserve unsafe runtime readiness false")
        _validate_source_ref_list(self.source_refs)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")


@dataclass(frozen=True)
class WorkspaceInspectionValidationReport:
    validation_report_id: str
    tool_pack_id: str | None = None
    request_id: str | None = None
    decision_id: str | None = None
    validated_path_ref: str | None = None
    validation_passed: bool = False
    denied_records: list[WorkspaceInspectionDeniedRecord] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    summary: str = "Safe workspace inspection validation report."
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_denied_record_list("denied_records", self.denied_records)
        _validate_string_list("warnings", self.warnings)
        _require_non_blank("summary", self.summary)
        if self.validation_passed and self.denied_records:
            raise ValueError("validation_passed cannot be True with denied_records")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")


@dataclass(frozen=True)
class WorkspaceInspectionReport:
    report_id: str
    version: str
    tool_pack_id: str | None = None
    result_ids: list[str] = field(default_factory=list)
    status: WorkspaceInspectionStatus | str = WorkspaceInspectionStatus.COMPLETED
    summary: str = "Safe workspace inspection report is not persistence."
    inspected_path_count: int = 0
    skipped_path_count: int = 0
    denied_count: int = 0
    truncated_result_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0335(self.version)
        WorkspaceInspectionStatus(self.status)
        for name in ("inspected_path_count", "skipped_path_count", "denied_count", "truncated_result_count"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("result_ids", "completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if (self.ready_for_v0336_agent_step_runner or self.ready_for_v0337_runtime_ocel_trace_emitter) and self.blocked_items:
            raise ValueError("design-stage readiness is not allowed with blocked_items")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")


@dataclass(frozen=True)
class WorkspaceInspectionRunPreview:
    run_preview_id: str
    tool_pack_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_shell_command_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_reference_dependency_install_guarantee: bool = True
    no_secret_file_read_guarantee: bool = True
    no_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
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
                raise ValueError(f"{name} must be True in v0.33.5")


@dataclass(frozen=True)
class WorkspaceInspectionNoWriteGuarantee:
    guarantee_id: str
    version: str
    no_shell_command: bool = True
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
    no_binary_file_read: bool = True
    no_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_agent_step_execution: bool = True
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
        _validate_version_includes_v0335(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.33.5")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0335ReadinessReport:
    report_id: str
    version: str = V0335_VERSION
    tool_pack_id: str | None = None
    inspection_report_id: str | None = None
    validation_report_id: str | None = None
    summary: str = "v0.33.5 enables bounded safe read-only workspace inspection only."
    ready_for_v0336_agent_step_runner: bool = False
    ready_for_v0337_runtime_ocel_trace_emitter: bool = False
    safe_readonly_workspace_inspection_enabled: bool = False
    ready_for_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_readonly_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_file_read: bool = False
    ready_for_reference_file_access: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_model_step_execution: bool = False
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
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0335(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_RUNTIME_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        for required in DEFAULT_PROHIBITED_UNTIL_LATER_GATE:
            if required not in self.prohibited_until_later_gate:
                raise ValueError("prohibited_until_later_gate missing v0.33.5 prohibition")
        if (self.ready_for_v0336_agent_step_runner or self.ready_for_v0337_runtime_ocel_trace_emitter) and self.blocked_items:
            raise ValueError("design-stage readiness is not allowed with blocked_items")
        if _metadata_flag_true(self.metadata, {"general_runtime", "provider_invocation", "ocel_emission"}):
            raise ValueError("V0335ReadinessReport is not general runtime enablement")


def build_workspace_inspection_flags(flag_set_id: str = "workspace_inspection_flags:v0.33.5", **kwargs: Any) -> WorkspaceInspectionFlagSet:
    return WorkspaceInspectionFlagSet(flag_set_id=flag_set_id, version=V0335_VERSION, **kwargs)


def build_workspace_inspection_source_ref(
    source_ref_id: str,
    source_kind: WorkspaceInspectionSourceKind | str = WorkspaceInspectionSourceKind.MANUAL_INSPECTION_REQUEST,
    source_id: str = "manual_inspection_request",
    source_summary: str = "In-memory workspace inspection request metadata.",
    **kwargs: Any,
) -> WorkspaceInspectionSourceRef:
    return WorkspaceInspectionSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_workspace_inspection_limits(limits_id: str = "workspace_inspection_limits:v0.33.5", **kwargs: Any) -> WorkspaceInspectionLimits:
    return WorkspaceInspectionLimits(limits_id=limits_id, **kwargs)


def build_workspace_inspection_root_policy(root_policy_id: str, allowed_root_refs: list[str], **kwargs: Any) -> WorkspaceInspectionRootPolicy:
    return WorkspaceInspectionRootPolicy(root_policy_id=root_policy_id, allowed_root_refs=allowed_root_refs, **kwargs)


def build_workspace_inspection_path_policy(
    path_policy_id: str,
    root_policy: WorkspaceInspectionRootPolicy,
    limits: WorkspaceInspectionLimits | None = None,
    **kwargs: Any,
) -> WorkspaceInspectionPathPolicy:
    return WorkspaceInspectionPathPolicy(path_policy_id=path_policy_id, root_policy=root_policy, limits=limits or default_workspace_inspection_limits(), **kwargs)


def build_workspace_inspection_request(request_id: str, request_kind: WorkspaceInspectionRequestKind | str, tool_kind: WorkspaceInspectionToolKind | str, **kwargs: Any) -> WorkspaceInspectionRequest:
    return WorkspaceInspectionRequest(request_id=request_id, request_kind=request_kind, tool_kind=tool_kind, **kwargs)


def build_workspace_inspection_decision(decision_id: str, request_id: str, decision_kind: WorkspaceInspectionDecisionKind | str, **kwargs: Any) -> WorkspaceInspectionDecision:
    return WorkspaceInspectionDecision(
        decision_id=decision_id,
        request_id=request_id,
        decision_kind=decision_kind,
        status=kwargs.pop("status", WorkspaceInspectionStatus.ALLOWED if WorkspaceInspectionDecisionKind(decision_kind) in ALLOWED_DECISION_KINDS else WorkspaceInspectionStatus.DENIED),
        normalized_path_ref=kwargs.pop("normalized_path_ref", None),
        reason=kwargs.pop("reason", "Safe workspace inspection policy decision."),
        **kwargs,
    )


def build_workspace_inspection_denied_record(denied_record_id: str, **kwargs: Any) -> WorkspaceInspectionDeniedRecord:
    return WorkspaceInspectionDeniedRecord(denied_record_id=denied_record_id, **kwargs)


def build_workspace_path_metadata(metadata_id: str, path_ref: str, name: str, **kwargs: Any) -> WorkspacePathMetadata:
    return WorkspacePathMetadata(metadata_id=metadata_id, path_ref=path_ref, name=name, **kwargs)


def build_workspace_tree_entry(entry_id: str, path_metadata: WorkspacePathMetadata, depth: int, **kwargs: Any) -> WorkspaceTreeEntry:
    return WorkspaceTreeEntry(entry_id=entry_id, path_metadata=path_metadata, depth=depth, **kwargs)


def build_workspace_tree_inspection_result(result_id: str, request_id: str, decision_id: str, root_path_ref: str, entries: list[WorkspaceTreeEntry], **kwargs: Any) -> WorkspaceTreeInspectionResult:
    return WorkspaceTreeInspectionResult(result_id=result_id, request_id=request_id, decision_id=decision_id, root_path_ref=root_path_ref, entries=entries, **kwargs)


def build_workspace_file_metadata_result(result_id: str, request_id: str, decision_id: str, path_metadata: WorkspacePathMetadata, **kwargs: Any) -> WorkspaceFileMetadataResult:
    return WorkspaceFileMetadataResult(result_id=result_id, request_id=request_id, decision_id=decision_id, path_metadata=path_metadata, **kwargs)


def build_workspace_safe_text_read_result(result_id: str, request_id: str, decision_id: str, path_ref: str, text_excerpt: str, **kwargs: Any) -> WorkspaceSafeTextReadResult:
    return WorkspaceSafeTextReadResult(
        result_id=result_id,
        request_id=request_id,
        decision_id=decision_id,
        path_ref=path_ref,
        text_excerpt=text_excerpt,
        encoding=kwargs.pop("encoding", "utf-8"),
        chars_returned=kwargs.pop("chars_returned", len(text_excerpt)),
        file_size_bytes=kwargs.pop("file_size_bytes", None),
        truncated=kwargs.pop("truncated", False),
        redacted=kwargs.pop("redacted", False),
        skipped=kwargs.pop("skipped", False),
        **kwargs,
    )


def build_workspace_text_search_match(match_id: str, path_ref: str, line_number: int | None, line_excerpt: str, match_preview: str, **kwargs: Any) -> WorkspaceTextSearchMatch:
    return WorkspaceTextSearchMatch(match_id=match_id, path_ref=path_ref, line_number=line_number, line_excerpt=line_excerpt, match_preview=match_preview, **kwargs)


def build_workspace_text_search_result(result_id: str, request_id: str, decision_id: str, query: str, root_path_ref: str, matches: list[WorkspaceTextSearchMatch], **kwargs: Any) -> WorkspaceTextSearchResult:
    return WorkspaceTextSearchResult(result_id=result_id, request_id=request_id, decision_id=decision_id, query=query, root_path_ref=root_path_ref, matches=matches, **kwargs)


def build_workspace_inspection_tool_result(tool_result_id: str, request_id: str, decision_id: str, result_kind: WorkspaceInspectionResultKind | str, **kwargs: Any) -> WorkspaceInspectionToolResult:
    return WorkspaceInspectionToolResult(tool_result_id=tool_result_id, request_id=request_id, decision_id=decision_id, result_kind=result_kind, **kwargs)


def build_workspace_inspection_tool_pack(tool_pack_id: str, path_policy: WorkspaceInspectionPathPolicy, **kwargs: Any) -> WorkspaceInspectionToolPack:
    return WorkspaceInspectionToolPack(
        tool_pack_id=tool_pack_id,
        version=V0335_VERSION,
        supported_tool_kinds=kwargs.pop(
            "supported_tool_kinds",
            [
                WorkspaceInspectionToolKind.INSPECT_PROJECT_TREE_READONLY,
                WorkspaceInspectionToolKind.INSPECT_FILE_METADATA_READONLY,
                WorkspaceInspectionToolKind.READ_TEXT_FILE_SAFE,
                WorkspaceInspectionToolKind.SEARCH_TEXT_IN_WORKSPACE_READONLY,
                WorkspaceInspectionToolKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY,
                WorkspaceInspectionToolKind.INSPECT_WORKSPACE_PATH_READONLY,
            ],
        ),
        path_policy=path_policy,
        flags=kwargs.pop(
            "flags",
            build_workspace_inspection_flags(
                safe_workspace_inspection_tool_pack_constructed=True,
                safe_path_policy_available=True,
                safe_metadata_inspection_enabled=True,
                safe_tree_inspection_enabled=True,
                safe_text_read_enabled=True,
                safe_text_search_enabled=True,
                safe_reference_inventory_summary_enabled=True,
                ready_for_safe_readonly_tool_execution=True,
                ready_for_safe_workspace_inspection_execution=True,
                ready_for_file_read=True,
            ),
        ),
        **kwargs,
    )


def build_workspace_inspection_validation_report(validation_report_id: str, **kwargs: Any) -> WorkspaceInspectionValidationReport:
    return WorkspaceInspectionValidationReport(validation_report_id=validation_report_id, **kwargs)


def build_workspace_inspection_report(report_id: str, **kwargs: Any) -> WorkspaceInspectionReport:
    return WorkspaceInspectionReport(report_id=report_id, version=V0335_VERSION, **kwargs)


def build_workspace_inspection_run_preview(run_preview_id: str, **kwargs: Any) -> WorkspaceInspectionRunPreview:
    return WorkspaceInspectionRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_workspace_inspection_no_write_guarantee(guarantee_id: str = "workspace_inspection_no_write:v0.33.5", **kwargs: Any) -> WorkspaceInspectionNoWriteGuarantee:
    return WorkspaceInspectionNoWriteGuarantee(guarantee_id=guarantee_id, version=V0335_VERSION, **kwargs)


def build_v0335_readiness_report(report_id: str = "v0335_readiness_report", **kwargs: Any) -> V0335ReadinessReport:
    return V0335ReadinessReport(report_id=report_id, version=V0335_VERSION, **kwargs)


def default_workspace_inspection_limits() -> WorkspaceInspectionLimits:
    return build_workspace_inspection_limits()


def default_workspace_inspection_root_policy(
    workspace_root: str | Path,
    *,
    allow_references_root: bool = False,
    references_root: str | Path | None = None,
    allow_opencode_reference_root: bool = False,
    allow_hermes_reference_root: bool = False,
    allow_openclaw_reference_root: bool = False,
) -> WorkspaceInspectionRootPolicy:
    roots = [str(Path(workspace_root).expanduser().resolve(strict=False))]
    if references_root is not None:
        roots.append(str(Path(references_root).expanduser().resolve(strict=False)))
    return build_workspace_inspection_root_policy(
        "workspace_inspection_root_policy:v0.33.5",
        roots,
        allow_references_root=allow_references_root,
        allow_opencode_reference_root=allow_opencode_reference_root,
        allow_hermes_reference_root=allow_hermes_reference_root,
        allow_openclaw_reference_root=allow_openclaw_reference_root,
    )


def default_workspace_inspection_path_policy(
    workspace_root: str | Path,
    *,
    allow_references_root: bool = False,
    references_root: str | Path | None = None,
    limits: WorkspaceInspectionLimits | None = None,
) -> WorkspaceInspectionPathPolicy:
    root_policy = default_workspace_inspection_root_policy(
        workspace_root,
        allow_references_root=allow_references_root,
        references_root=references_root,
    )
    return build_workspace_inspection_path_policy(
        "workspace_inspection_path_policy:v0.33.5",
        root_policy,
        limits or default_workspace_inspection_limits(),
    )


def _allowed_roots(policy: WorkspaceInspectionPathPolicy) -> list[Path]:
    return [Path(root).expanduser().resolve(strict=False) for root in policy.root_policy.allowed_root_refs]


def _is_under_allowed_root(path: Path, policy: WorkspaceInspectionPathPolicy) -> bool:
    return any(_path_is_relative_to(path, root) for root in _allowed_roots(policy))


def _matches_any_pattern(path: Path, patterns: list[str]) -> bool:
    name = path.name.lower()
    full = str(path).lower()
    for pattern in patterns:
        lowered = pattern.lower()
        if fnmatch.fnmatch(name, lowered) or fnmatch.fnmatch(full, lowered) or lowered.strip("*") in name:
            return True
    return False


def _is_secret_like_path(path: Path, policy: WorkspaceInspectionPathPolicy) -> bool:
    return _matches_any_pattern(path, policy.prohibited_file_patterns)


def _is_reference_path(path: Path, policy: WorkspaceInspectionPathPolicy) -> bool:
    parts = [part.lower() for part in path.parts]
    if "references" in parts:
        return True
    for root in _allowed_roots(policy):
        if _path_is_relative_to(path, root) and root.name.lower() in {"references", "opencode", "hermes", "openclaw"}:
            return True
    return False


def _reference_allowed(path: Path, policy: WorkspaceInspectionPathPolicy) -> bool:
    if not _is_reference_path(path, policy):
        return False
    parts = [part.lower() for part in path.parts]
    if "opencode" in parts:
        return policy.root_policy.allow_opencode_reference_root or policy.root_policy.allow_references_root
    if "hermes" in parts:
        return policy.root_policy.allow_hermes_reference_root or policy.root_policy.allow_references_root
    if "openclaw" in parts:
        return policy.root_policy.allow_openclaw_reference_root or policy.root_policy.allow_references_root
    return policy.root_policy.allow_references_root


def _extension_allowed(path: Path, policy: WorkspaceInspectionPathPolicy) -> bool:
    suffix = path.suffix.lower()
    if suffix in policy.prohibited_extensions:
        return False
    return suffix in policy.allowed_text_extensions or suffix in policy.limits.allowed_text_extensions


def _safe_path_metadata(path: Path, *, skipped: bool = False, skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] | None = None) -> WorkspacePathMetadata:
    size_bytes: int | None = None
    modified_time: float | None = None
    try:
        stat = path.stat()
        size_bytes = stat.st_size
        modified_time = stat.st_mtime
    except OSError:
        pass
    return build_workspace_path_metadata(
        f"metadata:{str(path)}",
        str(path),
        path.name or str(path),
        suffix=path.suffix or None,
        is_file=path.is_file(),
        is_dir=path.is_dir(),
        is_symlink=path.is_symlink(),
        size_bytes=size_bytes,
        modified_time=modified_time,
        skipped=skipped,
        skip_reasons=skip_reasons or [],
    )


def _denied_record_from_decision(decision: WorkspaceInspectionDecision, path_ref: str | None = None) -> WorkspaceInspectionDeniedRecord:
    return build_workspace_inspection_denied_record(
        f"{decision.request_id}:denied:{len(decision.skip_reasons)}",
        request_id=decision.request_id,
        decision_id=decision.decision_id,
        path_ref=path_ref or decision.normalized_path_ref,
        skip_reasons=list(decision.skip_reasons),
        risk_kinds=list(decision.risk_kinds),
        reason=decision.reason,
        safe_alternatives=["Use an allowed in-root, non-secret, bounded text path."],
    )


def _denied_tool_result(request: WorkspaceInspectionRequest, decision: WorkspaceInspectionDecision, result_kind: WorkspaceInspectionResultKind = WorkspaceInspectionResultKind.DENIED_RESULT) -> WorkspaceInspectionToolResult:
    return build_workspace_inspection_tool_result(
        f"{request.request_id}:result",
        request.request_id,
        decision.decision_id,
        result_kind,
        denied_records=[_denied_record_from_decision(decision, request.path_ref)],
        status=decision.status,
        summary=decision.reason,
    )


def _make_decision(
    request_id: str,
    decision_kind: WorkspaceInspectionDecisionKind,
    status: WorkspaceInspectionStatus,
    reason: str,
    *,
    normalized_path_ref: str | None = None,
    skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] | None = None,
    risk_kinds: list[WorkspaceInspectionRiskKind | str] | None = None,
    safe_readonly_allowed: bool = False,
    file_read_allowed: bool = False,
    reference_file_access_allowed: bool = False,
) -> WorkspaceInspectionDecision:
    return build_workspace_inspection_decision(
        f"{request_id}:decision",
        request_id,
        decision_kind,
        status=status,
        normalized_path_ref=normalized_path_ref,
        reason=reason,
        skip_reasons=skip_reasons or [],
        risk_kinds=risk_kinds or [],
        safe_readonly_allowed=safe_readonly_allowed,
        file_read_allowed=file_read_allowed,
        reference_file_access_allowed=reference_file_access_allowed,
    )


def normalize_and_validate_workspace_path(path_ref: str | Path | None, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionDecision:
    if not isinstance(policy, WorkspaceInspectionPathPolicy):
        raise TypeError("policy must be WorkspaceInspectionPathPolicy")
    if path_ref is None or str(path_ref).strip() == "":
        return _make_decision(
            "path:blank",
            WorkspaceInspectionDecisionKind.DENY,
            WorkspaceInspectionStatus.DENIED,
            "Path reference is required for safe workspace inspection.",
            skip_reasons=[WorkspaceInspectionSkipReasonKind.UNSUPPORTED_REQUEST],
            risk_kinds=[WorkspaceInspectionRiskKind.PATH_TRAVERSAL_RISK],
        )

    raw_path = Path(path_ref).expanduser()
    if raw_path.exists() and raw_path.is_symlink() and _is_under_allowed_root(raw_path.parent.resolve(strict=False), policy):
        target = raw_path.resolve(strict=True)
        if not policy.root_policy.allow_symlinks or not _is_under_allowed_root(target, policy):
            return _make_decision(
                f"path:{raw_path}",
                WorkspaceInspectionDecisionKind.SKIP,
                WorkspaceInspectionStatus.SKIPPED,
                "Symlink is not allowed or escapes allowed roots.",
                normalized_path_ref=str(raw_path),
                skip_reasons=[WorkspaceInspectionSkipReasonKind.PATH_IS_SYMLINK_OUTSIDE_ROOT],
                risk_kinds=[WorkspaceInspectionRiskKind.SYMLINK_ESCAPE_RISK],
            )
    normalized = raw_path.resolve(strict=False)
    if not _is_under_allowed_root(normalized, policy):
        return _make_decision(
            f"path:{raw_path}",
            WorkspaceInspectionDecisionKind.DENY,
            WorkspaceInspectionStatus.DENIED,
            "Path is outside allowed roots.",
            normalized_path_ref=str(normalized),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.OUTSIDE_ALLOWED_ROOT],
            risk_kinds=[WorkspaceInspectionRiskKind.PATH_TRAVERSAL_RISK],
        )
    if not normalized.exists():
        return _make_decision(
            f"path:{raw_path}",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Path does not exist.",
            normalized_path_ref=str(normalized),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.PATH_NOT_FOUND],
        )
    if normalized.is_symlink():
        target = normalized.resolve(strict=True)
        if not policy.root_policy.allow_symlinks or not _is_under_allowed_root(target, policy):
            return _make_decision(
                f"path:{raw_path}",
                WorkspaceInspectionDecisionKind.SKIP,
                WorkspaceInspectionStatus.SKIPPED,
                "Symlink is not allowed or escapes allowed roots.",
                normalized_path_ref=str(normalized),
                skip_reasons=[WorkspaceInspectionSkipReasonKind.PATH_IS_SYMLINK_OUTSIDE_ROOT],
                risk_kinds=[WorkspaceInspectionRiskKind.SYMLINK_ESCAPE_RISK],
            )
    if _is_secret_like_path(normalized, policy):
        return _make_decision(
            f"path:{raw_path}",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Secret-like path is skipped before content access.",
            normalized_path_ref=str(normalized),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.PATH_IS_SECRET_LIKE],
            risk_kinds=[WorkspaceInspectionRiskKind.SECRET_FILE_RISK],
        )
    if _is_reference_path(normalized, policy) and not _reference_allowed(normalized, policy):
        return _make_decision(
            f"path:{raw_path}",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Reference path is not enabled for bounded safe inspection.",
            normalized_path_ref=str(normalized),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.UNSAFE_REFERENCE_PATH],
            risk_kinds=[WorkspaceInspectionRiskKind.REFERENCE_CODE_EXECUTION_RISK],
        )
    return _make_decision(
        f"path:{raw_path}",
        WorkspaceInspectionDecisionKind.ALLOW_SAFE_METADATA_INSPECTION,
        WorkspaceInspectionStatus.ALLOWED,
        "Path is inside allowed roots and passed metadata policy checks.",
        normalized_path_ref=str(normalized),
        safe_readonly_allowed=True,
        reference_file_access_allowed=_reference_allowed(normalized, policy),
    )


def _check_safe_text_file(path: Path, request_id: str, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionDecision:
    decision = normalize_and_validate_workspace_path(path, policy)
    if not decision.safe_readonly_allowed:
        return decision
    if not path.is_file():
        return _make_decision(
            f"{request_id}:text",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Safe text read requires a file path.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.UNSUPPORTED_REQUEST],
        )
    if not _extension_allowed(path, policy):
        return _make_decision(
            f"{request_id}:text",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "File extension is not allowed for safe text inspection.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.EXTENSION_NOT_ALLOWED],
        )
    try:
        size = path.stat().st_size
    except PermissionError:
        return _make_decision(
            f"{request_id}:text",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Permission error while checking file metadata.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.PERMISSION_ERROR],
        )
    if size > policy.limits.max_file_size_bytes:
        return _make_decision(
            f"{request_id}:text",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "File exceeds max_file_size_bytes.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.FILE_TOO_LARGE],
            risk_kinds=[WorkspaceInspectionRiskKind.OVERSIZED_FILE_RISK],
        )
    if _looks_binary(path):
        return _make_decision(
            f"{request_id}:text",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Binary-like file is skipped.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.PATH_IS_BINARY],
            risk_kinds=[WorkspaceInspectionRiskKind.BINARY_FILE_RISK],
        )
    return _make_decision(
        f"{request_id}:text",
        WorkspaceInspectionDecisionKind.ALLOW_SAFE_TEXT_READ,
        WorkspaceInspectionStatus.ALLOWED,
        "File passed bounded safe text read policy.",
        normalized_path_ref=str(path),
        safe_readonly_allowed=True,
        file_read_allowed=True,
        reference_file_access_allowed=_reference_allowed(path, policy),
    )


def _looks_binary(path: Path) -> bool:
    try:
        with path.open("rb") as handle:
            sample = handle.read(2048)
    except OSError:
        return True
    if b"\x00" in sample:
        return True
    if not sample:
        return False
    control = sum(1 for byte in sample if byte < 9 or (13 < byte < 32))
    return control / len(sample) > 0.20


def inspect_file_metadata_readonly(request: WorkspaceInspectionRequest, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    if not isinstance(request, WorkspaceInspectionRequest):
        raise TypeError("request must be WorkspaceInspectionRequest")
    decision = normalize_and_validate_workspace_path(request.path_ref, policy)
    if not decision.safe_readonly_allowed:
        return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.SKIPPED_RESULT)
    path = Path(decision.normalized_path_ref or "")
    metadata = _safe_path_metadata(path)
    result = build_workspace_file_metadata_result(
        f"{request.request_id}:metadata",
        request.request_id,
        decision.decision_id,
        metadata,
        summary="Read-only metadata inspection completed without file content.",
    )
    return build_workspace_inspection_tool_result(
        f"{request.request_id}:result",
        request.request_id,
        decision.decision_id,
        WorkspaceInspectionResultKind.METADATA_RESULT,
        metadata_result=result,
        status=WorkspaceInspectionStatus.COMPLETED,
        summary="Metadata result contains no file content.",
    )


def inspect_project_tree_readonly(request: WorkspaceInspectionRequest, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    if not isinstance(request, WorkspaceInspectionRequest):
        raise TypeError("request must be WorkspaceInspectionRequest")
    decision = normalize_and_validate_workspace_path(request.path_ref, policy)
    if not decision.safe_readonly_allowed:
        return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.SKIPPED_RESULT)
    root = Path(decision.normalized_path_ref or "")
    entries: list[WorkspaceTreeEntry] = []
    skipped: list[WorkspaceInspectionDeniedRecord] = []
    truncated = False
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack:
        current, depth = stack.pop()
        if len(entries) >= policy.limits.max_entries:
            truncated = True
            skipped.append(
                build_workspace_inspection_denied_record(
                    f"{request.request_id}:tree:item_limit:{len(skipped)}",
                    request_id=request.request_id,
                    decision_id=decision.decision_id,
                    path_ref=str(current),
                    skip_reasons=[WorkspaceInspectionSkipReasonKind.ITEM_LIMIT_EXCEEDED],
                    risk_kinds=[WorkspaceInspectionRiskKind.UNBOUNDED_TRAVERSAL_RISK],
                    reason="Tree inspection item limit reached.",
                )
            )
            break
        skip_reasons: list[WorkspaceInspectionSkipReasonKind | str] = []
        included = True
        if depth > policy.limits.max_depth:
            included = False
            skip_reasons.append(WorkspaceInspectionSkipReasonKind.DIRECTORY_DEPTH_EXCEEDED)
        if _is_secret_like_path(current, policy):
            included = False
            skip_reasons.append(WorkspaceInspectionSkipReasonKind.PATH_IS_SECRET_LIKE)
        if current.is_symlink() and not policy.root_policy.allow_symlinks:
            included = False
            skip_reasons.append(WorkspaceInspectionSkipReasonKind.PATH_IS_SYMLINK_OUTSIDE_ROOT)
        metadata = _safe_path_metadata(current, skipped=not included, skip_reasons=skip_reasons)
        entries.append(
            build_workspace_tree_entry(
                f"{request.request_id}:entry:{len(entries)}",
                metadata,
                depth,
                child_count=None,
                included=included,
            )
        )
        if not included:
            skipped.append(
                build_workspace_inspection_denied_record(
                    f"{request.request_id}:tree:skip:{len(skipped)}",
                    request_id=request.request_id,
                    decision_id=decision.decision_id,
                    path_ref=str(current),
                    skip_reasons=skip_reasons,
                    reason="Path skipped by tree inspection policy.",
                )
            )
            continue
        if current.is_dir() and depth < policy.limits.max_depth:
            try:
                children = sorted(current.iterdir(), key=lambda item: item.name.lower(), reverse=True)
            except PermissionError:
                skipped.append(
                    build_workspace_inspection_denied_record(
                        f"{request.request_id}:tree:permission:{len(skipped)}",
                        request_id=request.request_id,
                        decision_id=decision.decision_id,
                        path_ref=str(current),
                        skip_reasons=[WorkspaceInspectionSkipReasonKind.PERMISSION_ERROR],
                        reason="Permission error during read-only directory metadata inspection.",
                    )
                )
                continue
            for child in children:
                stack.append((child, depth + 1))
    result = build_workspace_tree_inspection_result(
        f"{request.request_id}:tree",
        request.request_id,
        decision.decision_id,
        str(root),
        entries,
        skipped_paths=skipped,
        truncated=truncated,
        status=WorkspaceInspectionStatus.COMPLETED_WITH_SKIPS if skipped else WorkspaceInspectionStatus.COMPLETED,
        summary="Bounded read-only project tree metadata inspection completed.",
    )
    return build_workspace_inspection_tool_result(
        f"{request.request_id}:result",
        request.request_id,
        decision.decision_id,
        WorkspaceInspectionResultKind.TREE_RESULT,
        tree_result=result,
        denied_records=skipped,
        status=result.status,
        summary="Tree inspection result is metadata only.",
    )


def read_text_file_safe(request: WorkspaceInspectionRequest, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    if not isinstance(request, WorkspaceInspectionRequest):
        raise TypeError("request must be WorkspaceInspectionRequest")
    if request.path_ref is None:
        decision = normalize_and_validate_workspace_path(request.path_ref, policy)
        return _denied_tool_result(request, decision)
    path = Path(request.path_ref).expanduser().resolve(strict=False)
    decision = _check_safe_text_file(path, request.request_id, policy)
    if not decision.file_read_allowed:
        empty = build_workspace_safe_text_read_result(
            f"{request.request_id}:text",
            request.request_id,
            decision.decision_id,
            str(path),
            "",
            encoding=None,
            chars_returned=0,
            file_size_bytes=path.stat().st_size if path.exists() and path.is_file() else None,
            truncated=False,
            redacted=True,
            skipped=True,
            skip_reasons=list(decision.skip_reasons),
            status=WorkspaceInspectionStatus.SKIPPED,
            summary=decision.reason,
            metadata={"max_read_chars": policy.limits.max_read_chars},
        )
        return build_workspace_inspection_tool_result(
            f"{request.request_id}:result",
            request.request_id,
            decision.decision_id,
            WorkspaceInspectionResultKind.SKIPPED_RESULT,
            text_read_result=empty,
            denied_records=[_denied_record_from_decision(decision, str(path))],
            status=WorkspaceInspectionStatus.SKIPPED,
            summary=decision.reason,
        )
    try:
        with path.open("r", encoding="utf-8", errors="replace") as handle:
            text = handle.read(policy.limits.max_read_chars + 1)
    except UnicodeError:
        decision = _make_decision(
            f"{request.request_id}:decode",
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Decode error during safe text read.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.DECODE_ERROR],
        )
        return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.SKIPPED_RESULT)
    truncated = len(text) > policy.limits.max_read_chars
    excerpt = text[: policy.limits.max_read_chars]
    text_result = build_workspace_safe_text_read_result(
        f"{request.request_id}:text",
        request.request_id,
        decision.decision_id,
        str(path),
        excerpt,
        encoding="utf-8",
        chars_returned=len(excerpt),
        file_size_bytes=path.stat().st_size,
        truncated=truncated,
        redacted=False,
        skipped=False,
        status=WorkspaceInspectionStatus.COMPLETED,
        summary="Bounded safe text read completed after policy approval.",
        metadata={"max_read_chars": policy.limits.max_read_chars},
    )
    return build_workspace_inspection_tool_result(
        f"{request.request_id}:result",
        request.request_id,
        decision.decision_id,
        WorkspaceInspectionResultKind.SAFE_TEXT_READ_RESULT,
        text_read_result=text_result,
        status=WorkspaceInspectionStatus.COMPLETED,
        summary="Safe text read returned bounded excerpt only.",
    )


def search_text_in_workspace_readonly(request: WorkspaceInspectionRequest, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    if not isinstance(request, WorkspaceInspectionRequest):
        raise TypeError("request must be WorkspaceInspectionRequest")
    if request.query is None or request.query == "":
        decision = _make_decision(
            request.request_id,
            WorkspaceInspectionDecisionKind.NO_OP,
            WorkspaceInspectionStatus.NO_OP,
            "Search query is required.",
            skip_reasons=[WorkspaceInspectionSkipReasonKind.UNSUPPORTED_REQUEST],
        )
        return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.NO_OP_RESULT)
    decision = normalize_and_validate_workspace_path(request.path_ref, policy)
    if not decision.safe_readonly_allowed:
        return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.SKIPPED_RESULT)
    root = Path(decision.normalized_path_ref or "")
    roots = [root] if root.is_file() else [item for item in _iter_tree_files(root, policy)]
    matches: list[WorkspaceTextSearchMatch] = []
    skipped: list[WorkspaceInspectionDeniedRecord] = []
    searched_file_count = 0
    truncated = False
    for path in roots:
        if searched_file_count >= policy.limits.max_search_files:
            truncated = True
            skipped.append(
                build_workspace_inspection_denied_record(
                    f"{request.request_id}:search:file_limit:{len(skipped)}",
                    request_id=request.request_id,
                    decision_id=decision.decision_id,
                    path_ref=str(path),
                    skip_reasons=[WorkspaceInspectionSkipReasonKind.ITEM_LIMIT_EXCEEDED],
                    risk_kinds=[WorkspaceInspectionRiskKind.UNBOUNDED_TRAVERSAL_RISK],
                    reason="Search file limit reached.",
                )
            )
            break
        text_decision = _check_safe_text_file(path, request.request_id, policy)
        if not text_decision.file_read_allowed:
            skipped.append(_denied_record_from_decision(text_decision, str(path)))
            continue
        searched_file_count += 1
        try:
            with path.open("r", encoding="utf-8", errors="replace") as handle:
                for line_number, line in enumerate(handle, start=1):
                    if request.query.lower() in line.lower():
                        line_excerpt = line.rstrip("\n")[: policy.limits.max_line_length]
                        matches.append(
                            build_workspace_text_search_match(
                                f"{request.request_id}:match:{len(matches)}",
                                str(path),
                                line_number,
                                line_excerpt,
                                request.query[: policy.limits.max_line_length],
                                metadata={"max_line_length": policy.limits.max_line_length},
                            )
                        )
                        if len(matches) >= policy.limits.max_search_matches:
                            truncated = True
                            break
                    if truncated:
                        break
        except OSError:
            skipped.append(
                build_workspace_inspection_denied_record(
                    f"{request.request_id}:search:permission:{len(skipped)}",
                    request_id=request.request_id,
                    decision_id=decision.decision_id,
                    path_ref=str(path),
                    skip_reasons=[WorkspaceInspectionSkipReasonKind.PERMISSION_ERROR],
                    reason="Permission error during bounded text search.",
                )
            )
        if truncated:
            break
    search_result = build_workspace_text_search_result(
        f"{request.request_id}:search",
        request.request_id,
        decision.decision_id,
        request.query,
        str(root),
        matches,
        skipped_paths=skipped,
        searched_file_count=searched_file_count,
        truncated=truncated,
        status=WorkspaceInspectionStatus.COMPLETED_WITH_SKIPS if skipped else WorkspaceInspectionStatus.COMPLETED,
        summary="Bounded safe text search completed.",
        metadata={
            "max_search_matches": policy.limits.max_search_matches,
            "max_search_files": policy.limits.max_search_files,
        },
    )
    return build_workspace_inspection_tool_result(
        f"{request.request_id}:result",
        request.request_id,
        decision.decision_id,
        WorkspaceInspectionResultKind.TEXT_SEARCH_RESULT,
        text_search_result=search_result,
        denied_records=skipped,
        status=search_result.status,
        summary="Text search returned bounded matches only.",
    )


def _iter_tree_files(root: Path, policy: WorkspaceInspectionPathPolicy) -> list[Path]:
    files: list[Path] = []
    stack: list[tuple[Path, int]] = [(root, 0)]
    while stack and len(files) < policy.limits.max_search_files:
        current, depth = stack.pop()
        if depth > policy.limits.max_depth:
            continue
        if current.is_symlink() or _is_secret_like_path(current, policy):
            continue
        if current.is_file():
            files.append(current)
            continue
        if current.is_dir():
            try:
                children = sorted(current.iterdir(), key=lambda item: item.name.lower(), reverse=True)
            except PermissionError:
                continue
            for child in children:
                stack.append((child, depth + 1))
    return files


def summarize_reference_inventory_readonly(request: WorkspaceInspectionRequest, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    decision = normalize_and_validate_workspace_path(request.path_ref, policy)
    if decision.normalized_path_ref is None:
        return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.SKIPPED_RESULT)
    path = Path(decision.normalized_path_ref)
    if not _is_reference_path(path, policy) or not _reference_allowed(path, policy):
        blocked = _make_decision(
            request.request_id,
            WorkspaceInspectionDecisionKind.SKIP,
            WorkspaceInspectionStatus.SKIPPED,
            "Reference inventory summary requires an explicitly allowed references path.",
            normalized_path_ref=str(path),
            skip_reasons=[WorkspaceInspectionSkipReasonKind.UNSAFE_REFERENCE_PATH],
            risk_kinds=[WorkspaceInspectionRiskKind.REFERENCE_CODE_EXECUTION_RISK],
        )
        return _denied_tool_result(request, blocked, WorkspaceInspectionResultKind.SKIPPED_RESULT)
    tree_request = build_workspace_inspection_request(
        request.request_id,
        WorkspaceInspectionRequestKind.INSPECT_TREE,
        WorkspaceInspectionToolKind.SUMMARIZE_REFERENCE_INVENTORY_READONLY,
        path_ref=str(path),
        request_summary="Bounded reference inventory metadata summary.",
    )
    result = inspect_project_tree_readonly(tree_request, policy)
    if result.tree_result is None:
        return result
    return build_workspace_inspection_tool_result(
        f"{request.request_id}:result",
        request.request_id,
        result.decision_id,
        WorkspaceInspectionResultKind.REFERENCE_INVENTORY_SUMMARY,
        tree_result=result.tree_result,
        denied_records=result.denied_records,
        status=result.status,
        summary="Reference inventory summary is bounded metadata only.",
    )


def inspect_workspace_path_readonly(request: WorkspaceInspectionRequest, policy: WorkspaceInspectionPathPolicy) -> WorkspaceInspectionToolResult:
    request_kind = WorkspaceInspectionRequestKind(request.request_kind)
    if request_kind == WorkspaceInspectionRequestKind.INSPECT_TREE:
        return inspect_project_tree_readonly(request, policy)
    if request_kind == WorkspaceInspectionRequestKind.INSPECT_METADATA:
        return inspect_file_metadata_readonly(request, policy)
    if request_kind == WorkspaceInspectionRequestKind.READ_SAFE_TEXT:
        return read_text_file_safe(request, policy)
    if request_kind == WorkspaceInspectionRequestKind.SEARCH_SAFE_TEXT:
        return search_text_in_workspace_readonly(request, policy)
    if request_kind == WorkspaceInspectionRequestKind.SUMMARIZE_REFERENCE_INVENTORY:
        return summarize_reference_inventory_readonly(request, policy)
    if request_kind == WorkspaceInspectionRequestKind.INSPECT_PATH:
        metadata_result = inspect_file_metadata_readonly(request, policy)
        if metadata_result.metadata_result and metadata_result.metadata_result.path_metadata.is_dir:
            return inspect_project_tree_readonly(
                build_workspace_inspection_request(
                    request.request_id,
                    WorkspaceInspectionRequestKind.INSPECT_TREE,
                    WorkspaceInspectionToolKind.INSPECT_PROJECT_TREE_READONLY,
                    path_ref=request.path_ref,
                    request_summary=request.request_summary,
                ),
                policy,
            )
        return metadata_result
    decision = _make_decision(
        request.request_id,
        WorkspaceInspectionDecisionKind.NO_OP,
        WorkspaceInspectionStatus.NO_OP,
        "Unsupported or no-op workspace inspection request.",
        skip_reasons=[WorkspaceInspectionSkipReasonKind.UNSUPPORTED_REQUEST],
    )
    return _denied_tool_result(request, decision, WorkspaceInspectionResultKind.NO_OP_RESULT)


def workspace_inspection_flags_preserve_unsafe_runtime_false(flags: WorkspaceInspectionFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_RUNTIME_FLAG_NAMES)


def workspace_inspection_decision_is_safe_readonly(decision: WorkspaceInspectionDecision) -> bool:
    return (
        decision.command_execution_allowed is False
        and decision.network_access_allowed is False
        and decision.credential_access_allowed is False
        and decision.workspace_write_allowed is False
        and (not decision.safe_readonly_allowed or WorkspaceInspectionDecisionKind(decision.decision_kind) in ALLOWED_DECISION_KINDS)
    )


def workspace_inspection_result_has_no_write(result: WorkspaceInspectionToolResult) -> bool:
    return result.ready_for_execution is False


def workspace_inspection_policy_blocks_secret_paths(policy: WorkspaceInspectionPathPolicy) -> bool:
    required = (".env", "secret", "key", "token", "credential", "pem", "id_rsa")
    lowered = [value.lower() for value in policy.prohibited_file_patterns]
    return policy.allow_secret_read is False and all(any(item in value for value in lowered) for item in required)


def v0335_readiness_report_is_not_general_runtime_ready(report: V0335ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_RUNTIME_FLAG_NAMES)
