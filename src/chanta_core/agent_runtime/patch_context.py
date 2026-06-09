from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_intent import (
    PatchIntentScopeBundle,
    PatchScopePolicy,
    PatchTargetKind,
    PatchTargetSelector,
)
from .patch_proposal_boundary import ReferenceCorpusKind


V0352_VERSION = "v0.35.2"
V0352_RELEASE_NAME = "v0.35.2 Read-only Patch Context & Reference Corpus Collector"
DEFAULT_V0352_DOC_PATH = "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"

DEFAULT_PROHIBITED_RUNTIME_ACTIONS = [
    "patch_plan_generation",
    "change_set_graph_generation",
    "diff_proposal_generation",
    "patch_proposal_generation",
    "patch_application",
    "workspace_write",
    "code_edit",
    "apply_patch",
    "git_apply",
    "test_execution",
    "shell_execution",
    "subprocess_execution",
    "command_execution",
    "dependency_install",
    "reference_execution",
    "reference_import",
    "provider_invocation",
    "direct_network_access",
    "credential_access",
    "secret_read",
]

UNSAFE_PATCH_CONTEXT_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_patch_plan",
    "ready_for_change_set_graph",
    "ready_for_diff_proposal",
    "ready_for_patch_proposal",
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
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_raw_source_dump",
    "ready_for_persistent_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)

SECRET_MARKERS = (".env", "secret", "credential", "token", "api_key", "password", ".pem", "id_rsa", "id_ed25519")
BINARY_SUFFIXES = (".png", ".jpg", ".jpeg", ".gif", ".ico", ".exe", ".dll", ".zip", ".gz", ".7z", ".pdf", ".bin", ".pyc")


class PatchContextCollectionMode(StrEnum):
    INTENT_SCOPE_BUNDLE_ONLY = "intent_scope_bundle_only"
    READONLY_WORKSPACE_CONTEXT = "readonly_workspace_context"
    READONLY_REFERENCE_CORPUS_CONTEXT = "readonly_reference_corpus_context"
    COMBINED_WORKSPACE_AND_REFERENCE_CONTEXT = "combined_workspace_and_reference_context"
    DIGEST_METADATA_ONLY = "digest_metadata_only"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchContextSourceKind(StrEnum):
    V0351_PATCH_INTENT_SCOPE_BUNDLE = "v0351_patch_intent_scope_bundle"
    V0351_PATCH_SCOPE_POLICY = "v0351_patch_scope_policy"
    V0351_PATCH_TARGET_SELECTOR = "v0351_patch_target_selector"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    V0335_SAFE_WORKSPACE_INSPECTION = "v0335_safe_workspace_inspection"
    WORKSPACE_SOURCE_FILE = "workspace_source_file"
    WORKSPACE_TEST_FILE = "workspace_test_file"
    WORKSPACE_DOC_FILE = "workspace_doc_file"
    REFERENCE_CORPUS_OPENCODE = "reference_corpus_opencode"
    REFERENCE_CORPUS_HERMES = "reference_corpus_hermes"
    REFERENCE_CORPUS_OPENCLAW = "reference_corpus_openclaw"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchContextTargetStatus(StrEnum):
    UNKNOWN = "unknown"
    SELECTED = "selected"
    ALLOWED_READONLY = "allowed_readonly"
    COLLECTED = "collected"
    COLLECTED_WITH_WARNINGS = "collected_with_warnings"
    SKIPPED = "skipped"
    DENIED = "denied"
    BLOCKED = "blocked"
    TOO_LARGE = "too_large"
    BINARY_SKIPPED = "binary_skipped"
    SECRET_SKIPPED = "secret_skipped"
    OUTSIDE_SCOPE = "outside_scope"
    NO_OP = "no_op"


class PatchContextReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTEXT_CONTRACT_READY = "context_contract_ready"
    READONLY_COLLECTION_READY = "readonly_collection_ready"
    CONTEXT_SNAPSHOT_READY = "context_snapshot_ready"
    EVIDENCE_BUNDLE_READY = "evidence_bundle_ready"
    DESIGN_HANDOFF_READY_FOR_V0353 = "design_handoff_ready_for_v0353"
    DESIGN_HANDOFF_READY_FOR_V0354 = "design_handoff_ready_for_v0354"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchContextDecisionKind(StrEnum):
    ALLOW_READONLY_METADATA = "allow_readonly_metadata"
    ALLOW_BOUNDED_TEXT_EXCERPT = "allow_bounded_text_excerpt"
    ALLOW_BOUNDED_SEARCH = "allow_bounded_search"
    ALLOW_REFERENCE_DIGEST_METADATA = "allow_reference_digest_metadata"
    ALLOW_REFERENCE_READONLY_SUMMARY = "allow_reference_readonly_summary"
    DENY = "deny"
    BLOCK = "block"
    SKIP = "skip"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchContextRiskKind(StrEnum):
    SCOPE_ESCAPE_RISK = "scope_escape_risk"
    OUTSIDE_ROOT_RISK = "outside_root_risk"
    SECRET_FILE_RISK = "secret_file_risk"
    CREDENTIAL_FILE_RISK = "credential_file_risk"
    BINARY_FILE_RISK = "binary_file_risk"
    OVERSIZED_FILE_RISK = "oversized_file_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    REFERENCE_IMPORT_RISK = "reference_import_risk"
    RAW_SOURCE_DUMP_RISK = "raw_source_dump_risk"
    UNBOUNDED_CONTEXT_RISK = "unbounded_context_risk"
    COPIED_CODE_RISK = "copied_code_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    UNKNOWN = "unknown"


class PatchContextEvidenceKind(StrEnum):
    FILE_METADATA = "file_metadata"
    BOUNDED_TEXT_EXCERPT = "bounded_text_excerpt"
    BOUNDED_SEARCH_FINDING = "bounded_search_finding"
    SYMBOL_OR_HEADING_SUMMARY = "symbol_or_heading_summary"
    TEST_FILE_SUMMARY = "test_file_summary"
    DOCUMENTATION_SUMMARY = "documentation_summary"
    REFERENCE_DIGEST_SUMMARY = "reference_digest_summary"
    REFERENCE_STATIC_PATTERN_SUMMARY = "reference_static_pattern_summary"
    SKIPPED_TARGET_RECORD = "skipped_target_record"
    DENIED_TARGET_RECORD = "denied_target_record"
    GAP_RECORD = "gap_record"
    UNKNOWN = "unknown"


class PatchContextFileRole(StrEnum):
    SOURCE_UNDER_CONSIDERATION = "source_under_consideration"
    TEST_UNDER_CONSIDERATION = "test_under_consideration"
    DOCUMENTATION_UNDER_CONSIDERATION = "documentation_under_consideration"
    VERSION_DOC = "version_doc"
    CONFIG_METADATA = "config_metadata"
    REFERENCE_DOC = "reference_doc"
    REFERENCE_SOURCE_SUMMARY = "reference_source_summary"
    BLOCKED_SECRET = "blocked_secret"
    BLOCKED_BINARY = "blocked_binary"
    UNKNOWN = "unknown"


class PatchContextReferenceRole(StrEnum):
    OPENCODE_CLI_PATTERN_SOURCE = "opencode_cli_pattern_source"
    OPENCODE_AGENT_LOOP_PATTERN_SOURCE = "opencode_agent_loop_pattern_source"
    OPENCODE_PATCH_PATTERN_SOURCE = "opencode_patch_pattern_source"
    HERMES_CLI_PATTERN_SOURCE = "hermes_cli_pattern_source"
    HERMES_AGENT_LOOP_PATTERN_SOURCE = "hermes_agent_loop_pattern_source"
    HERMES_PATCH_PATTERN_SOURCE = "hermes_patch_pattern_source"
    OPENCLAW_OPTIONAL_PATTERN_SOURCE = "openclaw_optional_pattern_source"
    REFERENCE_DIGEST_ONLY = "reference_digest_only"
    REJECTED_REFERENCE_PATTERN = "rejected_reference_pattern"
    FUTURE_TRACK_REFERENCE_PATTERN = "future_track_reference_pattern"
    UNKNOWN = "unknown"


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0352_VERSION not in value:
        raise ValueError("version must include v0.35.2")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    for key in metadata:
        lower = str(key).lower()
        if any(token in lower for token in ("secret", "credential", "api_key", "token", "password")):
            raise ValueError("metadata must not contain secret-like keys")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_enum_list(name: str, value: list[Any], enum_type: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_type(item)


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.2")


def _bounded(value: str, limit: int = 480) -> tuple[str, bool]:
    if len(value) <= limit:
        return value, False
    return value[:limit], True


@dataclass(frozen=True)
class PatchContextFlagSet:
    flag_set_id: str
    version: str
    patch_context_collector_constructed: bool
    readonly_collection_policy_defined: bool
    context_snapshot_constructed: bool
    evidence_bundle_constructed: bool
    reference_digest_consumed: bool
    reference_corpus_readonly_summary_available: bool
    ready_for_v0353_reference_informed_patch_plan: bool
    ready_for_v0354_diff_proposal_envelope: bool
    ready_for_readonly_patch_context_collection: bool
    ready_for_patch_context_snapshot: bool
    ready_for_patch_context_evidence_bundle: bool
    ready_for_execution: bool = False
    ready_for_patch_plan: bool = False
    ready_for_change_set_graph: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
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
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_raw_source_dump: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_PATCH_CONTEXT_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextSourceRef:
    source_ref_id: str
    source_kind: PatchContextSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PatchContextSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextCollectionPolicy:
    policy_id: str
    version: str
    collection_mode: PatchContextCollectionMode | str
    allowed_root_refs: list[str] = field(default_factory=list)
    blocked_root_refs: list[str] = field(default_factory=list)
    allowed_path_patterns: list[str] = field(default_factory=list)
    blocked_path_patterns: list[str] = field(default_factory=list)
    allowed_file_roles: list[PatchContextFileRole | str] = field(default_factory=list)
    blocked_file_roles: list[PatchContextFileRole | str] = field(default_factory=list)
    max_target_count: int = 12
    max_files_per_target: int = 12
    max_file_size_bytes: int = 20000
    max_excerpt_chars: int = 700
    max_total_excerpt_chars: int = 5000
    max_search_findings: int = 8
    allow_file_metadata: bool = True
    allow_bounded_text_excerpt: bool = True
    allow_bounded_search: bool = True
    allow_reference_digest_metadata: bool = True
    allow_reference_corpus_readonly_summary: bool = True
    allow_secret_file_read: bool = False
    allow_credential_file_read: bool = False
    allow_binary_file_read: bool = False
    allow_outside_scope_read: bool = False
    allow_shell: bool = False
    allow_subprocess: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_patch_application: bool = False
    allow_raw_source_dump: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        PatchContextCollectionMode(self.collection_mode)
        for name in ("allowed_root_refs", "blocked_root_refs", "allowed_path_patterns", "blocked_path_patterns"):
            _validate_string_list(name, getattr(self, name))
        _validate_enum_list("allowed_file_roles", self.allowed_file_roles, PatchContextFileRole)
        _validate_enum_list("blocked_file_roles", self.blocked_file_roles, PatchContextFileRole)
        for name in ("max_target_count", "max_files_per_target", "max_file_size_bytes", "max_excerpt_chars", "max_total_excerpt_chars", "max_search_findings"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        for name in (
            "allow_secret_file_read",
            "allow_credential_file_read",
            "allow_binary_file_read",
            "allow_outside_scope_read",
            "allow_shell",
            "allow_subprocess",
            "allow_workspace_write",
            "allow_code_edit",
            "allow_patch_application",
            "allow_raw_source_dump",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.2")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextRequest:
    context_request_id: str
    version: str
    intent_id: str | None
    scope_policy_id: str | None
    intent_scope_bundle_id: str | None
    requested_mode: PatchContextCollectionMode | str
    requested_target_refs: list[str]
    requested_reference_corpus: list[PatchContextSourceKind | str]
    task_summary: str
    source_refs: list[PatchContextSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("context_request_id", self.context_request_id)
        _validate_version(self.version)
        for name in ("intent_id", "scope_policy_id", "intent_scope_bundle_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        PatchContextCollectionMode(self.requested_mode)
        _validate_string_list("requested_target_refs", self.requested_target_refs)
        _validate_enum_list("requested_reference_corpus", self.requested_reference_corpus, PatchContextSourceKind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"workspace_write", "code_edit", "patch_application", "shell_execution", "test_execution", "dependency_install", "reference_execution", "provider_invocation", "direct_network_access", "credential_access"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include unsafe runtime actions")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextTarget:
    context_target_id: str
    target_selector_id: str | None
    target_path_ref: str
    target_kind: PatchTargetKind | str
    file_role: PatchContextFileRole | str
    status: PatchContextTargetStatus | str
    decision_kind: PatchContextDecisionKind | str
    risk_kinds: list[PatchContextRiskKind | str]
    allowed_readonly: bool
    collected: bool
    skipped: bool
    blocked: bool
    block_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("context_target_id", self.context_target_id)
        if self.target_selector_id is not None:
            _require_non_blank("target_selector_id", self.target_selector_id)
        _require_non_blank("target_path_ref", self.target_path_ref)
        PatchTargetKind(self.target_kind)
        PatchContextFileRole(self.file_role)
        status = PatchContextTargetStatus(self.status)
        PatchContextDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchContextRiskKind)
        if self.collected and not self.allowed_readonly:
            raise ValueError("collected targets must be allowed_readonly")
        if (self.skipped or self.blocked or status in {PatchContextTargetStatus.DENIED, PatchContextTargetStatus.BLOCKED, PatchContextTargetStatus.SKIPPED, PatchContextTargetStatus.TOO_LARGE, PatchContextTargetStatus.BINARY_SKIPPED, PatchContextTargetStatus.SECRET_SKIPPED, PatchContextTargetStatus.OUTSIDE_SCOPE}) and not self.block_reason:
            raise ValueError("skipped/blocked targets must include block_reason")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextFileSummary:
    file_summary_id: str
    context_target_id: str
    path_ref: str
    file_role: PatchContextFileRole | str
    size_bytes: int | None
    line_count_estimate: int | None
    excerpt_preview: str
    structural_summary: str
    relevant_symbols_or_headings: list[str]
    redacted: bool
    truncated: bool
    skipped: bool
    skip_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("file_summary_id", "context_target_id", "path_ref", "structural_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchContextFileRole(self.file_role)
        if self.size_bytes is not None and self.size_bytes < 0:
            raise ValueError("size_bytes must be None or >= 0")
        if self.line_count_estimate is not None and self.line_count_estimate < 0:
            raise ValueError("line_count_estimate must be None or >= 0")
        if len(self.excerpt_preview) > 1200:
            raise ValueError("excerpt_preview must be bounded")
        _validate_string_list("relevant_symbols_or_headings", self.relevant_symbols_or_headings)
        if self.skipped and not self.skip_reason:
            raise ValueError("skipped file summaries must include skip_reason")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextSearchFinding:
    search_finding_id: str
    context_target_id: str
    path_ref: str
    query: str
    line_number: int | None
    finding_preview: str
    relevance_summary: str
    redacted: bool
    truncated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("search_finding_id", "context_target_id", "path_ref", "query", "relevance_summary"):
            _require_non_blank(name, getattr(self, name))
        if self.line_number is not None and self.line_number < 1:
            raise ValueError("line_number must be None or >= 1")
        if len(self.finding_preview) > 1200:
            raise ValueError("finding_preview must be bounded")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextReferenceSummary:
    reference_summary_id: str
    corpus_kind: ReferenceCorpusKind | str
    reference_role: PatchContextReferenceRole | str
    root_path_ref: str
    summary: str
    observed_patterns: list[str] = field(default_factory=list)
    adapted_notes: list[str] = field(default_factory=list)
    rejected_notes: list[str] = field(default_factory=list)
    future_track_notes: list[str] = field(default_factory=list)
    inspected_readonly: bool = True
    executed_reference: bool = False
    imported_reference: bool = False
    installed_dependency: bool = False
    ran_reference_tests: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("reference_summary_id", self.reference_summary_id)
        ReferenceCorpusKind(self.corpus_kind)
        PatchContextReferenceRole(self.reference_role)
        _require_non_blank("root_path_ref", self.root_path_ref)
        _require_non_blank("summary", self.summary)
        for name in ("observed_patterns", "adapted_notes", "rejected_notes", "future_track_notes"):
            _validate_string_list(name, getattr(self, name))
        for name in ("executed_reference", "imported_reference", "installed_dependency", "ran_reference_tests"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextEvidenceItem:
    evidence_item_id: str
    evidence_kind: PatchContextEvidenceKind | str
    source_ref_id: str | None
    context_target_id: str | None
    path_ref: str | None
    evidence_summary: str
    evidence_preview: str
    confidence: str
    redacted: bool
    truncated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evidence_item_id", self.evidence_item_id)
        PatchContextEvidenceKind(self.evidence_kind)
        for name in ("source_ref_id", "context_target_id", "path_ref"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        _require_non_blank("evidence_summary", self.evidence_summary)
        _require_non_blank("confidence", self.confidence)
        if len(self.evidence_preview) > 1200:
            raise ValueError("evidence_preview must be bounded")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextEvidenceBundle:
    evidence_bundle_id: str
    version: str
    context_request_id: str
    evidence_items: list[PatchContextEvidenceItem]
    file_summary_ids: list[str]
    search_finding_ids: list[str]
    reference_summary_ids: list[str]
    gap_items: list[str]
    summary: str
    ready_for_patch_plan: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_bundle_id", "context_request_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_items", self.evidence_items)
        for name in ("file_summary_ids", "search_finding_ids", "reference_summary_ids", "gap_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_patch_plan", "ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextSnapshot:
    context_snapshot_id: str
    version: str
    context_request_id: str
    collection_mode: PatchContextCollectionMode | str
    targets: list[PatchContextTarget]
    file_summaries: list[PatchContextFileSummary]
    search_findings: list[PatchContextSearchFinding]
    reference_summaries: list[PatchContextReferenceSummary]
    evidence_bundle: PatchContextEvidenceBundle
    status: PatchContextTargetStatus | str
    readiness_level: PatchContextReadinessLevel | str
    summary: str
    redacted: bool
    truncated: bool
    ready_for_v0353_reference_informed_patch_plan: bool = True
    ready_for_v0354_diff_proposal_envelope: bool = True
    ready_for_patch_plan: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("context_snapshot_id", "context_request_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchContextCollectionMode(self.collection_mode)
        for name in ("targets", "file_summaries", "search_findings", "reference_summaries"):
            _validate_list(name, getattr(self, name))
        PatchContextTargetStatus(self.status)
        PatchContextReadinessLevel(self.readiness_level)
        _validate_false(self, ("ready_for_patch_plan", "ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_patch_application", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextCollectionDecision:
    decision_id: str
    context_request_id: str
    decision_kind: PatchContextDecisionKind | str
    reason: str
    risk_kinds: list[PatchContextRiskKind | str]
    readonly_collection_allowed: bool
    bounded_excerpt_allowed: bool
    bounded_search_allowed: bool
    reference_summary_allowed: bool
    workspace_write_allowed: bool = False
    code_edit_allowed: bool = False
    patch_application_allowed: bool = False
    shell_allowed: bool = False
    test_execution_allowed: bool = False
    dependency_install_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "context_request_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        PatchContextDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchContextRiskKind)
        _validate_false(self, ("workspace_write_allowed", "code_edit_allowed", "patch_application_allowed", "shell_allowed", "test_execution_allowed", "dependency_install_allowed"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextValidationFinding:
    finding_id: str
    decision_kind: PatchContextDecisionKind | str
    risk_kinds: list[PatchContextRiskKind | str]
    message: str
    blocks_validation: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        PatchContextDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchContextRiskKind)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextValidationReport:
    validation_report_id: str
    version: str
    context_snapshot_id: str | None
    findings: list[PatchContextValidationFinding]
    valid: bool
    summary: str
    no_write_confirmed: bool = True
    no_code_edit_confirmed: bool = True
    no_patch_application_confirmed: bool = True
    no_raw_source_dump_confirmed: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        if self.context_snapshot_id is not None:
            _require_non_blank("context_snapshot_id", self.context_snapshot_id)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        for name in ("no_write_confirmed", "no_code_edit_confirmed", "no_patch_application_confirmed", "no_raw_source_dump_confirmed"):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextCollectionReport:
    collection_report_id: str
    version: str
    context_request_id: str
    context_snapshot_id: str | None
    summary: str
    target_count: int
    collected_count: int
    skipped_count: int
    blocked_count: int
    gap_items: list[str]
    ready_for_readonly_patch_context_collection: bool = True
    ready_for_patch_context_snapshot: bool = True
    ready_for_patch_context_evidence_bundle: bool = True
    ready_for_patch_plan: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("collection_report_id", "context_request_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.context_snapshot_id is not None:
            _require_non_blank("context_snapshot_id", self.context_snapshot_id)
        for name in ("target_count", "collected_count", "skipped_count", "blocked_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_string_list("gap_items", self.gap_items)
        _validate_false(self, ("ready_for_patch_plan", "ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_patch_plan_guarantee: bool = True
    no_change_set_graph_guarantee: bool = True
    no_diff_proposal_guarantee: bool = True
    no_patch_proposal_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_test_execution_guarantee: bool = True
    no_dependency_install_guarantee: bool = True
    no_reference_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchContextNoWriteGuarantee:
    guarantee_id: str
    version: str
    no_patch_plan: bool = True
    no_change_set_graph: bool = True
    no_diff_proposal: bool = True
    no_patch_proposal: bool = True
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_test_execution: bool = True
    no_dependency_install: bool = True
    no_reference_execution: bool = True
    no_reference_import: bool = True
    no_provider_invocation: bool = True
    no_direct_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_autonomous_runtime: bool = True
    no_general_tool_execution: bool = True
    no_persistent_trace_write: bool = True
    no_ui_runtime: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0352ReadinessReport:
    report_id: str
    version: str
    context_snapshot_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0353_reference_informed_patch_plan: bool = True
    ready_for_v0354_diff_proposal_envelope: bool = True
    ready_for_readonly_patch_context_collection: bool = True
    ready_for_patch_context_snapshot: bool = True
    ready_for_patch_context_evidence_bundle: bool = True
    ready_for_execution: bool = False
    ready_for_patch_plan: bool = False
    ready_for_change_set_graph: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        if self.context_snapshot_id is not None:
            _require_non_blank("context_snapshot_id", self.context_snapshot_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_PATCH_CONTEXT_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_patch_context_flags(flag_set_id: str = "patch_context_flags:v0.35.2", **kwargs: Any) -> PatchContextFlagSet:
    return PatchContextFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0352_VERSION),
        patch_context_collector_constructed=kwargs.pop("patch_context_collector_constructed", True),
        readonly_collection_policy_defined=kwargs.pop("readonly_collection_policy_defined", True),
        context_snapshot_constructed=kwargs.pop("context_snapshot_constructed", True),
        evidence_bundle_constructed=kwargs.pop("evidence_bundle_constructed", True),
        reference_digest_consumed=kwargs.pop("reference_digest_consumed", True),
        reference_corpus_readonly_summary_available=kwargs.pop("reference_corpus_readonly_summary_available", True),
        ready_for_v0353_reference_informed_patch_plan=kwargs.pop("ready_for_v0353_reference_informed_patch_plan", True),
        ready_for_v0354_diff_proposal_envelope=kwargs.pop("ready_for_v0354_diff_proposal_envelope", True),
        ready_for_readonly_patch_context_collection=kwargs.pop("ready_for_readonly_patch_context_collection", True),
        ready_for_patch_context_snapshot=kwargs.pop("ready_for_patch_context_snapshot", True),
        ready_for_patch_context_evidence_bundle=kwargs.pop("ready_for_patch_context_evidence_bundle", True),
        **kwargs,
    )


def build_patch_context_source_ref(source_ref_id: str = "context_source:v0.35.2", **kwargs: Any) -> PatchContextSourceRef:
    return PatchContextSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchContextSourceKind.V0351_PATCH_INTENT_SCOPE_BUNDLE),
        source_id=kwargs.pop("source_id", "bundle:v0.35.1"),
        source_summary=kwargs.pop("source_summary", "Patch intent/scope metadata source for read-only context collection."),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.35/v0.35.1_patch_intent_scope_policy.md"]),
        **kwargs,
    )


def build_patch_context_collection_policy(policy_id: str = "context_policy:v0.35.2", **kwargs: Any) -> PatchContextCollectionPolicy:
    return PatchContextCollectionPolicy(
        policy_id=policy_id,
        version=kwargs.pop("version", V0352_VERSION),
        collection_mode=kwargs.pop("collection_mode", PatchContextCollectionMode.COMBINED_WORKSPACE_AND_REFERENCE_CONTEXT),
        allowed_root_refs=kwargs.pop("allowed_root_refs", ["src/chanta_core/agent_runtime", "tests", "docs/versions/v0.35", "references/OpenCode", "references/Hermes"]),
        blocked_root_refs=kwargs.pop("blocked_root_refs", [".git", ".env", "references/OpenClaw"]),
        allowed_path_patterns=kwargs.pop("allowed_path_patterns", [".py", ".md", ".txt", ".json", ".toml", ".yaml", ".yml", ".ts", ".tsx"]),
        blocked_path_patterns=kwargs.pop("blocked_path_patterns", list(SECRET_MARKERS)),
        allowed_file_roles=kwargs.pop("allowed_file_roles", [PatchContextFileRole.SOURCE_UNDER_CONSIDERATION, PatchContextFileRole.TEST_UNDER_CONSIDERATION, PatchContextFileRole.DOCUMENTATION_UNDER_CONSIDERATION, PatchContextFileRole.VERSION_DOC, PatchContextFileRole.REFERENCE_DOC, PatchContextFileRole.REFERENCE_SOURCE_SUMMARY]),
        blocked_file_roles=kwargs.pop("blocked_file_roles", [PatchContextFileRole.BLOCKED_SECRET, PatchContextFileRole.BLOCKED_BINARY]),
        **kwargs,
    )


def default_patch_context_collection_policy() -> PatchContextCollectionPolicy:
    return build_patch_context_collection_policy()


def build_patch_context_request(context_request_id: str = "context_request:v0.35.2", **kwargs: Any) -> PatchContextRequest:
    return PatchContextRequest(
        context_request_id=context_request_id,
        version=kwargs.pop("version", V0352_VERSION),
        intent_id=kwargs.pop("intent_id", "intent:v0.35.1"),
        scope_policy_id=kwargs.pop("scope_policy_id", "scope_policy:v0.35.1"),
        intent_scope_bundle_id=kwargs.pop("intent_scope_bundle_id", "bundle:v0.35.1"),
        requested_mode=kwargs.pop("requested_mode", PatchContextCollectionMode.COMBINED_WORKSPACE_AND_REFERENCE_CONTEXT),
        requested_target_refs=kwargs.pop("requested_target_refs", []),
        requested_reference_corpus=kwargs.pop("requested_reference_corpus", [PatchContextSourceKind.REFERENCE_CORPUS_OPENCODE, PatchContextSourceKind.REFERENCE_CORPUS_HERMES]),
        task_summary=kwargs.pop("task_summary", "Collect bounded read-only context for future v0.35 planning."),
        source_refs=kwargs.pop("source_refs", [build_patch_context_source_ref()]),
        **kwargs,
    )


def build_patch_context_request_from_intent_scope_bundle(bundle: PatchIntentScopeBundle, **kwargs: Any) -> PatchContextRequest:
    target_refs = [selector.target_path_ref for selector in bundle.target_selectors if selector.selected_for_future_context and not selector.blocked]
    return build_patch_context_request(
        intent_id=bundle.intent.intent_id,
        scope_policy_id=bundle.scope_policy.scope_policy_id,
        intent_scope_bundle_id=bundle.bundle_id,
        requested_target_refs=kwargs.pop("requested_target_refs", target_refs),
        **kwargs,
    )


def build_patch_context_target(context_target_id: str = "context_target:v0.35.2", **kwargs: Any) -> PatchContextTarget:
    return PatchContextTarget(
        context_target_id=context_target_id,
        target_selector_id=kwargs.pop("target_selector_id", None),
        target_path_ref=kwargs.pop("target_path_ref", DEFAULT_V0352_DOC_PATH),
        target_kind=kwargs.pop("target_kind", PatchTargetKind.VERSION_DOCUMENT),
        file_role=kwargs.pop("file_role", PatchContextFileRole.VERSION_DOC),
        status=kwargs.pop("status", PatchContextTargetStatus.ALLOWED_READONLY),
        decision_kind=kwargs.pop("decision_kind", PatchContextDecisionKind.ALLOW_BOUNDED_TEXT_EXCERPT),
        risk_kinds=kwargs.pop("risk_kinds", []),
        allowed_readonly=kwargs.pop("allowed_readonly", True),
        collected=kwargs.pop("collected", False),
        skipped=kwargs.pop("skipped", False),
        blocked=kwargs.pop("blocked", False),
        **kwargs,
    )


def build_patch_context_file_summary(file_summary_id: str = "file_summary:v0.35.2", **kwargs: Any) -> PatchContextFileSummary:
    return PatchContextFileSummary(
        file_summary_id=file_summary_id,
        context_target_id=kwargs.pop("context_target_id", "context_target:v0.35.2"),
        path_ref=kwargs.pop("path_ref", DEFAULT_V0352_DOC_PATH),
        file_role=kwargs.pop("file_role", PatchContextFileRole.VERSION_DOC),
        size_bytes=kwargs.pop("size_bytes", 0),
        line_count_estimate=kwargs.pop("line_count_estimate", 0),
        excerpt_preview=kwargs.pop("excerpt_preview", ""),
        structural_summary=kwargs.pop("structural_summary", "Bounded read-only file metadata summary."),
        relevant_symbols_or_headings=kwargs.pop("relevant_symbols_or_headings", []),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        skipped=kwargs.pop("skipped", False),
        **kwargs,
    )


def build_patch_context_search_finding(search_finding_id: str = "search_finding:v0.35.2", **kwargs: Any) -> PatchContextSearchFinding:
    return PatchContextSearchFinding(
        search_finding_id=search_finding_id,
        context_target_id=kwargs.pop("context_target_id", "context_target:v0.35.2"),
        path_ref=kwargs.pop("path_ref", DEFAULT_V0352_DOC_PATH),
        query=kwargs.pop("query", "PatchContext"),
        line_number=kwargs.pop("line_number", None),
        finding_preview=kwargs.pop("finding_preview", ""),
        relevance_summary=kwargs.pop("relevance_summary", "Bounded in-memory search finding metadata."),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        **kwargs,
    )


def build_patch_context_reference_summary(reference_summary_id: str = "reference_summary:v0.35.2", **kwargs: Any) -> PatchContextReferenceSummary:
    return PatchContextReferenceSummary(
        reference_summary_id=reference_summary_id,
        corpus_kind=kwargs.pop("corpus_kind", ReferenceCorpusKind.OPENCODE),
        reference_role=kwargs.pop("reference_role", PatchContextReferenceRole.REFERENCE_DIGEST_ONLY),
        root_path_ref=kwargs.pop("root_path_ref", DEFAULT_V0350_DIGEST_REF),
        summary=kwargs.pop("summary", "Reference corpus represented as static read-only metadata."),
        observed_patterns=kwargs.pop("observed_patterns", []),
        adapted_notes=kwargs.pop("adapted_notes", []),
        rejected_notes=kwargs.pop("rejected_notes", ["Reference execution/import/install remains prohibited."]),
        future_track_notes=kwargs.pop("future_track_notes", []),
        **kwargs,
    )


def build_patch_context_evidence_item(evidence_item_id: str = "evidence_item:v0.35.2", **kwargs: Any) -> PatchContextEvidenceItem:
    return PatchContextEvidenceItem(
        evidence_item_id=evidence_item_id,
        evidence_kind=kwargs.pop("evidence_kind", PatchContextEvidenceKind.FILE_METADATA),
        source_ref_id=kwargs.pop("source_ref_id", None),
        context_target_id=kwargs.pop("context_target_id", "context_target:v0.35.2"),
        path_ref=kwargs.pop("path_ref", DEFAULT_V0352_DOC_PATH),
        evidence_summary=kwargs.pop("evidence_summary", "Bounded read-only evidence metadata."),
        evidence_preview=kwargs.pop("evidence_preview", ""),
        confidence=kwargs.pop("confidence", "medium"),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        **kwargs,
    )


def build_patch_context_evidence_bundle(evidence_bundle_id: str = "evidence_bundle:v0.35.2", **kwargs: Any) -> PatchContextEvidenceBundle:
    return PatchContextEvidenceBundle(
        evidence_bundle_id=evidence_bundle_id,
        version=kwargs.pop("version", V0352_VERSION),
        context_request_id=kwargs.pop("context_request_id", "context_request:v0.35.2"),
        evidence_items=kwargs.pop("evidence_items", [build_patch_context_evidence_item()]),
        file_summary_ids=kwargs.pop("file_summary_ids", ["file_summary:v0.35.2"]),
        search_finding_ids=kwargs.pop("search_finding_ids", []),
        reference_summary_ids=kwargs.pop("reference_summary_ids", []),
        gap_items=kwargs.pop("gap_items", []),
        summary=kwargs.pop("summary", "Evidence bundle is read-only metadata, not a plan, diff, or proposal."),
        **kwargs,
    )


def build_patch_context_snapshot(context_snapshot_id: str = "context_snapshot:v0.35.2", **kwargs: Any) -> PatchContextSnapshot:
    evidence_bundle = kwargs.pop("evidence_bundle", build_patch_context_evidence_bundle())
    return PatchContextSnapshot(
        context_snapshot_id=context_snapshot_id,
        version=kwargs.pop("version", V0352_VERSION),
        context_request_id=kwargs.pop("context_request_id", evidence_bundle.context_request_id),
        collection_mode=kwargs.pop("collection_mode", PatchContextCollectionMode.COMBINED_WORKSPACE_AND_REFERENCE_CONTEXT),
        targets=kwargs.pop("targets", [build_patch_context_target()]),
        file_summaries=kwargs.pop("file_summaries", [build_patch_context_file_summary()]),
        search_findings=kwargs.pop("search_findings", []),
        reference_summaries=kwargs.pop("reference_summaries", []),
        evidence_bundle=evidence_bundle,
        status=kwargs.pop("status", PatchContextTargetStatus.COLLECTED_WITH_WARNINGS),
        readiness_level=kwargs.pop("readiness_level", PatchContextReadinessLevel.CONTEXT_SNAPSHOT_READY),
        summary=kwargs.pop("summary", "Context snapshot is read-only metadata, not a patch plan or proposal."),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        **kwargs,
    )


def build_patch_context_collection_decision(decision_id: str = "context_decision:v0.35.2", **kwargs: Any) -> PatchContextCollectionDecision:
    return PatchContextCollectionDecision(
        decision_id=decision_id,
        context_request_id=kwargs.pop("context_request_id", "context_request:v0.35.2"),
        decision_kind=kwargs.pop("decision_kind", PatchContextDecisionKind.ALLOW_BOUNDED_TEXT_EXCERPT),
        reason=kwargs.pop("reason", "Read-only bounded context collection is allowed by policy."),
        risk_kinds=kwargs.pop("risk_kinds", []),
        readonly_collection_allowed=kwargs.pop("readonly_collection_allowed", True),
        bounded_excerpt_allowed=kwargs.pop("bounded_excerpt_allowed", True),
        bounded_search_allowed=kwargs.pop("bounded_search_allowed", True),
        reference_summary_allowed=kwargs.pop("reference_summary_allowed", True),
        **kwargs,
    )


def build_patch_context_validation_finding(finding_id: str = "context_finding:v0.35.2:ok", **kwargs: Any) -> PatchContextValidationFinding:
    return PatchContextValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchContextDecisionKind.ALLOW_READONLY_METADATA),
        risk_kinds=kwargs.pop("risk_kinds", []),
        message=kwargs.pop("message", "Context artifacts remain read-only and bounded."),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_context_validation_report(validation_report_id: str = "context_validation:v0.35.2", **kwargs: Any) -> PatchContextValidationReport:
    findings = kwargs.pop("findings", [build_patch_context_validation_finding()])
    return PatchContextValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0352_VERSION),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Validation confirms no write/edit/apply/raw source dump readiness."),
        **kwargs,
    )


def build_patch_context_collection_report(collection_report_id: str = "context_report:v0.35.2", **kwargs: Any) -> PatchContextCollectionReport:
    return PatchContextCollectionReport(
        collection_report_id=collection_report_id,
        version=kwargs.pop("version", V0352_VERSION),
        context_request_id=kwargs.pop("context_request_id", "context_request:v0.35.2"),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        summary=kwargs.pop("summary", "Read-only context collection completed with bounded artifacts."),
        target_count=kwargs.pop("target_count", 1),
        collected_count=kwargs.pop("collected_count", 1),
        skipped_count=kwargs.pop("skipped_count", 0),
        blocked_count=kwargs.pop("blocked_count", 0),
        gap_items=kwargs.pop("gap_items", []),
        **kwargs,
    )


def build_patch_context_run_preview(run_preview_id: str = "context_run_preview:v0.35.2", **kwargs: Any) -> PatchContextRunPreview:
    return PatchContextRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["validate request", "summarize allowed files read-only", "create evidence bundle", "create context snapshot"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["PatchContextFileSummary", "PatchContextEvidenceBundle", "PatchContextSnapshot"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["patch plan", "change-set graph", "diff proposal", "patch proposal", "patch apply", "workspace write"]),
        **kwargs,
    )


def build_patch_context_no_write_guarantee(guarantee_id: str = "context_no_write:v0.35.2", **kwargs: Any) -> PatchContextNoWriteGuarantee:
    return PatchContextNoWriteGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0352_VERSION), **kwargs)


def build_v0352_readiness_report(report_id: str = "readiness:v0.35.2", **kwargs: Any) -> V0352ReadinessReport:
    return V0352ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0352_VERSION),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        summary=kwargs.pop("summary", "v0.35.2 is ready for v0.35.3/v0.35.4 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["Read-only context policy", "File summaries", "Search findings", "Reference summaries", "Evidence bundle", "Context snapshot"]),
        blocked_items=kwargs.pop("blocked_items", ["patch planning", "change-set graph", "diff proposal", "patch proposal", "patch application", "workspace write"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.3 Reference-informed Patch Plan", "v0.35.4 Diff Proposal Envelope"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0352_DOC_PATH, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any patch plan/diff/proposal/apply/write/execution path is introduced."]),
        **kwargs,
    )


def _path_ref(path: Path) -> str:
    return path.as_posix()


def _is_secret_like(path: Path) -> bool:
    lower = path.name.lower()
    return any(marker in lower for marker in SECRET_MARKERS)


def _is_binary_like(path: Path) -> bool:
    return path.suffix.lower() in BINARY_SUFFIXES


def _matches_allowed_suffix(path: Path, policy: PatchContextCollectionPolicy) -> bool:
    if not policy.allowed_path_patterns:
        return True
    lower = path.as_posix().lower()
    return any(pattern.lower().lstrip("*") in lower for pattern in policy.allowed_path_patterns)


def _within_roots(path: Path, roots: list[str]) -> bool:
    if not roots:
        return True
    resolved = path.resolve(strict=False)
    for root in roots:
        root_resolved = Path(root).resolve(strict=False)
        try:
            resolved.relative_to(root_resolved)
            return True
        except ValueError:
            continue
    return False


def _file_role_for_path(path: Path) -> PatchContextFileRole:
    lower = path.as_posix().lower()
    if "references/" in lower or "references\\" in lower:
        if path.suffix.lower() in {".md", ".txt", ".mdx"}:
            return PatchContextFileRole.REFERENCE_DOC
        return PatchContextFileRole.REFERENCE_SOURCE_SUMMARY
    if lower.endswith(".md"):
        if "docs/versions" in lower or "docs\\versions" in lower:
            return PatchContextFileRole.VERSION_DOC
        return PatchContextFileRole.DOCUMENTATION_UNDER_CONSIDERATION
    if "test" in lower:
        return PatchContextFileRole.TEST_UNDER_CONSIDERATION
    if path.suffix.lower() in {".toml", ".json", ".yaml", ".yml"}:
        return PatchContextFileRole.CONFIG_METADATA
    return PatchContextFileRole.SOURCE_UNDER_CONSIDERATION


def _target_kind_for_path(path: Path) -> PatchTargetKind:
    role = _file_role_for_path(path)
    if role == PatchContextFileRole.TEST_UNDER_CONSIDERATION:
        return PatchTargetKind.TEST_FILE
    if role in {PatchContextFileRole.DOCUMENTATION_UNDER_CONSIDERATION, PatchContextFileRole.VERSION_DOC, PatchContextFileRole.REFERENCE_DOC}:
        return PatchTargetKind.DOCUMENTATION_FILE
    if role == PatchContextFileRole.CONFIG_METADATA:
        return PatchTargetKind.PACKAGE_METADATA
    if role == PatchContextFileRole.REFERENCE_SOURCE_SUMMARY:
        return PatchTargetKind.REFERENCE_CORPUS_PATH
    return PatchTargetKind.SOURCE_FILE


def _deny_target(path: Path, status: PatchContextTargetStatus, risk: PatchContextRiskKind, reason: str) -> tuple[PatchContextTarget, PatchContextFileSummary]:
    target_id = f"context_target:{abs(hash(path.as_posix()))}:denied"
    role = PatchContextFileRole.BLOCKED_SECRET if risk in {PatchContextRiskKind.SECRET_FILE_RISK, PatchContextRiskKind.CREDENTIAL_FILE_RISK} else PatchContextFileRole.BLOCKED_BINARY if risk == PatchContextRiskKind.BINARY_FILE_RISK else PatchContextFileRole.UNKNOWN
    target = build_patch_context_target(
        context_target_id=target_id,
        target_path_ref=_path_ref(path),
        target_kind=PatchTargetKind.SECRET_LIKE_FILE if risk == PatchContextRiskKind.SECRET_FILE_RISK else PatchTargetKind.CREDENTIAL_LIKE_FILE if risk == PatchContextRiskKind.CREDENTIAL_FILE_RISK else PatchTargetKind.BINARY_FILE if risk == PatchContextRiskKind.BINARY_FILE_RISK else PatchTargetKind.UNKNOWN,
        file_role=role,
        status=status,
        decision_kind=PatchContextDecisionKind.SKIP if status != PatchContextTargetStatus.OUTSIDE_SCOPE else PatchContextDecisionKind.DENY,
        risk_kinds=[risk],
        allowed_readonly=False,
        collected=False,
        skipped=True,
        blocked=status in {PatchContextTargetStatus.BLOCKED, PatchContextTargetStatus.OUTSIDE_SCOPE},
        block_reason=reason,
    )
    summary = build_patch_context_file_summary(
        file_summary_id=f"file_summary:{target_id}",
        context_target_id=target.context_target_id,
        path_ref=_path_ref(path),
        file_role=role,
        size_bytes=None,
        line_count_estimate=None,
        excerpt_preview="",
        structural_summary="Target was skipped or denied before file content was read.",
        relevant_symbols_or_headings=[],
        redacted=True,
        truncated=False,
        skipped=True,
        skip_reason=reason,
    )
    return target, summary


def summarize_patch_context_file_readonly(path_ref: str | Path, policy: PatchContextCollectionPolicy | None = None) -> tuple[PatchContextTarget, PatchContextFileSummary]:
    policy = policy or default_patch_context_collection_policy()
    path = Path(path_ref)
    if not _within_roots(path, policy.allowed_root_refs):
        return _deny_target(path, PatchContextTargetStatus.OUTSIDE_SCOPE, PatchContextRiskKind.OUTSIDE_ROOT_RISK, "Target is outside allowed roots.")
    if _within_roots(path, policy.blocked_root_refs):
        return _deny_target(path, PatchContextTargetStatus.BLOCKED, PatchContextRiskKind.SCOPE_ESCAPE_RISK, "Target is under blocked root.")
    if path.is_symlink():
        return _deny_target(path, PatchContextTargetStatus.BLOCKED, PatchContextRiskKind.SYMLINK_ESCAPE_RISK, "Symlink targets are not followed.")
    if _is_secret_like(path):
        risk = PatchContextRiskKind.CREDENTIAL_FILE_RISK if any(token in path.as_posix().lower() for token in ("credential", "token", "key", "password")) else PatchContextRiskKind.SECRET_FILE_RISK
        return _deny_target(path, PatchContextTargetStatus.SECRET_SKIPPED, risk, "Secret-like target was skipped.")
    if _is_binary_like(path):
        return _deny_target(path, PatchContextTargetStatus.BINARY_SKIPPED, PatchContextRiskKind.BINARY_FILE_RISK, "Binary-like target was skipped.")
    if not path.exists() or not path.is_file():
        return _deny_target(path, PatchContextTargetStatus.SKIPPED, PatchContextRiskKind.AMBIGUOUS_TARGET_RISK if hasattr(PatchContextRiskKind, "AMBIGUOUS_TARGET_RISK") else PatchContextRiskKind.UNKNOWN, "Target does not exist as a regular file.")
    if not _matches_allowed_suffix(path, policy):
        return _deny_target(path, PatchContextTargetStatus.SKIPPED, PatchContextRiskKind.SCOPE_ESCAPE_RISK, "Target suffix is not allowed by policy.")
    size = path.stat().st_size
    if size > policy.max_file_size_bytes:
        return _deny_target(path, PatchContextTargetStatus.TOO_LARGE, PatchContextRiskKind.OVERSIZED_FILE_RISK, "Target exceeds max_file_size_bytes.")
    text = path.read_text(encoding="utf-8", errors="replace")
    if "\x00" in text[: min(len(text), 512)]:
        return _deny_target(path, PatchContextTargetStatus.BINARY_SKIPPED, PatchContextRiskKind.BINARY_FILE_RISK, "Binary-like null byte content was skipped.")
    excerpt, truncated = _bounded(text, policy.max_excerpt_chars)
    headings = [line.strip()[:120] for line in text.splitlines() if line.strip().startswith(("#", "class ", "def ", "function ", "export "))][:12]
    role = _file_role_for_path(path)
    target = build_patch_context_target(
        context_target_id=f"context_target:{abs(hash(path.as_posix()))}:collected",
        target_path_ref=_path_ref(path),
        target_kind=_target_kind_for_path(path),
        file_role=role,
        status=PatchContextTargetStatus.COLLECTED,
        decision_kind=PatchContextDecisionKind.ALLOW_BOUNDED_TEXT_EXCERPT,
        risk_kinds=[],
        allowed_readonly=True,
        collected=True,
        skipped=False,
        blocked=False,
    )
    summary = build_patch_context_file_summary(
        file_summary_id=f"file_summary:{abs(hash(path.as_posix()))}",
        context_target_id=target.context_target_id,
        path_ref=_path_ref(path),
        file_role=role,
        size_bytes=size,
        line_count_estimate=text.count("\n") + (1 if text else 0),
        excerpt_preview=excerpt,
        structural_summary="Bounded read-only text summary with headings/symbol markers only.",
        relevant_symbols_or_headings=headings,
        redacted=False,
        truncated=truncated,
        skipped=False,
    )
    return target, summary


def search_patch_context_readonly(path_ref: str | Path, query: str, policy: PatchContextCollectionPolicy | None = None) -> list[PatchContextSearchFinding]:
    policy = policy or default_patch_context_collection_policy()
    _require_non_blank("query", query)
    target, summary = summarize_patch_context_file_readonly(path_ref, policy)
    if not target.collected:
        return []
    text = Path(path_ref).read_text(encoding="utf-8", errors="replace")
    findings: list[PatchContextSearchFinding] = []
    for index, line in enumerate(text.splitlines(), start=1):
        if query.lower() in line.lower():
            preview, truncated = _bounded(line.strip(), policy.max_excerpt_chars)
            findings.append(
                build_patch_context_search_finding(
                    search_finding_id=f"search_finding:{abs(hash(str(path_ref)))}:{index}",
                    context_target_id=summary.context_target_id,
                    path_ref=_path_ref(Path(path_ref)),
                    query=query,
                    line_number=index,
                    finding_preview=preview,
                    relevance_summary="In-memory bounded string match; not shell grep output.",
                    redacted=False,
                    truncated=truncated,
                )
            )
            if len(findings) >= policy.max_search_findings:
                break
    return findings


def collect_reference_corpus_context_readonly(root_ref: str | Path, corpus_kind: ReferenceCorpusKind | str, policy: PatchContextCollectionPolicy | None = None) -> PatchContextReferenceSummary:
    policy = policy or default_patch_context_collection_policy()
    root = Path(root_ref)
    corpus = ReferenceCorpusKind(corpus_kind)
    if not root.exists():
        return build_patch_context_reference_summary(
            reference_summary_id=f"reference_summary:{corpus.value}:missing",
            corpus_kind=corpus,
            reference_role=PatchContextReferenceRole.REFERENCE_DIGEST_ONLY,
            root_path_ref=_path_ref(root),
            summary="Reference corpus was not found; no reference code was executed or imported.",
            observed_patterns=[],
            adapted_notes=["Use v0.35.0 ReferencePatternDigest metadata when available."],
            inspected_readonly=False,
        )
    observed: list[str] = []
    rejected: list[str] = ["Execution, import, install, and reference test behavior remain rejected."]
    future: list[str] = []
    count = 0
    for candidate in root.rglob("*"):
        if count >= policy.max_files_per_target:
            future.append("Additional reference files were not inspected because max_files_per_target was reached.")
            break
        if not candidate.is_file() or candidate.is_symlink() or _is_secret_like(candidate) or _is_binary_like(candidate):
            continue
        if candidate.stat().st_size > policy.max_file_size_bytes or not _matches_allowed_suffix(candidate, policy):
            continue
        text = candidate.read_text(encoding="utf-8", errors="replace")
        excerpt, _ = _bounded(text, policy.max_excerpt_chars)
        observed.append(f"{candidate.as_posix()}: {excerpt[:160]}")
        count += 1
    role = PatchContextReferenceRole.OPENCODE_PATCH_PATTERN_SOURCE if corpus == ReferenceCorpusKind.OPENCODE else PatchContextReferenceRole.HERMES_PATCH_PATTERN_SOURCE if corpus == ReferenceCorpusKind.HERMES else PatchContextReferenceRole.OPENCLAW_OPTIONAL_PATTERN_SOURCE
    return build_patch_context_reference_summary(
        reference_summary_id=f"reference_summary:{corpus.value}:v0.35.2",
        corpus_kind=corpus,
        reference_role=role,
        root_path_ref=_path_ref(root),
        summary="Reference corpus summarized through bounded read-only static inspection only.",
        observed_patterns=observed,
        adapted_notes=["Map static patterns into future patch-context metadata only."],
        rejected_notes=rejected,
        future_track_notes=future,
        inspected_readonly=True,
    )


def collect_patch_context_readonly(request: PatchContextRequest, policy: PatchContextCollectionPolicy | None = None) -> PatchContextSnapshot:
    policy = policy or default_patch_context_collection_policy()
    targets: list[PatchContextTarget] = []
    summaries: list[PatchContextFileSummary] = []
    findings: list[PatchContextSearchFinding] = []
    refs: list[PatchContextReferenceSummary] = []
    evidence: list[PatchContextEvidenceItem] = []
    gaps: list[str] = []
    for path_ref in request.requested_target_refs[: policy.max_target_count]:
        target, summary = summarize_patch_context_file_readonly(path_ref, policy)
        targets.append(target)
        summaries.append(summary)
        evidence_kind = PatchContextEvidenceKind.BOUNDED_TEXT_EXCERPT if target.collected else PatchContextEvidenceKind.SKIPPED_TARGET_RECORD
        evidence.append(
            build_patch_context_evidence_item(
                evidence_item_id=f"evidence:{summary.file_summary_id}",
                evidence_kind=evidence_kind,
                context_target_id=target.context_target_id,
                path_ref=summary.path_ref,
                evidence_summary=summary.structural_summary,
                evidence_preview=summary.excerpt_preview,
                confidence="medium" if target.collected else "high",
                redacted=summary.redacted,
                truncated=summary.truncated,
            )
        )
        if not target.collected:
            gaps.append(f"{summary.path_ref}: {summary.skip_reason}")
    for source_kind in request.requested_reference_corpus:
        if source_kind == PatchContextSourceKind.REFERENCE_CORPUS_OPENCODE:
            refs.append(collect_reference_corpus_context_readonly("references/OpenCode", ReferenceCorpusKind.OPENCODE, policy))
        elif source_kind == PatchContextSourceKind.REFERENCE_CORPUS_HERMES:
            refs.append(collect_reference_corpus_context_readonly("references/Hermes", ReferenceCorpusKind.HERMES, policy))
        elif source_kind == PatchContextSourceKind.REFERENCE_CORPUS_OPENCLAW:
            refs.append(collect_reference_corpus_context_readonly("references/OpenClaw", ReferenceCorpusKind.OPENCLAW, policy))
    for ref_summary in refs:
        evidence.append(
            build_patch_context_evidence_item(
                evidence_item_id=f"evidence:{ref_summary.reference_summary_id}",
                evidence_kind=PatchContextEvidenceKind.REFERENCE_STATIC_PATTERN_SUMMARY,
                context_target_id=None,
                path_ref=ref_summary.root_path_ref,
                evidence_summary=ref_summary.summary,
                evidence_preview="; ".join(ref_summary.observed_patterns)[: policy.max_excerpt_chars],
                confidence="medium",
                redacted=True,
                truncated=len("; ".join(ref_summary.observed_patterns)) > policy.max_excerpt_chars,
            )
        )
    bundle = build_patch_context_evidence_bundle(
        context_request_id=request.context_request_id,
        evidence_items=evidence or [build_patch_context_evidence_item(evidence_kind=PatchContextEvidenceKind.GAP_RECORD, evidence_summary="No context targets were collected.", evidence_preview="")],
        file_summary_ids=[item.file_summary_id for item in summaries],
        search_finding_ids=[item.search_finding_id for item in findings],
        reference_summary_ids=[item.reference_summary_id for item in refs],
        gap_items=gaps,
    )
    status = PatchContextTargetStatus.COLLECTED_WITH_WARNINGS if gaps else PatchContextTargetStatus.COLLECTED
    return build_patch_context_snapshot(
        context_request_id=request.context_request_id,
        collection_mode=request.requested_mode,
        targets=targets,
        file_summaries=summaries,
        search_findings=findings,
        reference_summaries=refs,
        evidence_bundle=bundle,
        status=status,
        summary="Read-only patch context snapshot created from bounded metadata and excerpts.",
        redacted=True,
        truncated=any(item.truncated for item in summaries),
    )


def validate_patch_context_snapshot(snapshot: PatchContextSnapshot) -> PatchContextValidationReport:
    findings: list[PatchContextValidationFinding] = []
    if not patch_context_snapshot_is_not_patch_plan(snapshot):
        findings.append(
            build_patch_context_validation_finding(
                "context_finding:unsafe_readiness",
                decision_kind=PatchContextDecisionKind.BLOCK,
                risk_kinds=[PatchContextRiskKind.PATCH_APPLY_RISK],
                message="Snapshot cannot be patch plan/diff/proposal/apply/execution ready.",
                blocks_validation=True,
            )
        )
    if any(not ref.executed_reference is False or not ref.imported_reference is False for ref in snapshot.reference_summaries):
        findings.append(
            build_patch_context_validation_finding(
                "context_finding:reference_runtime",
                decision_kind=PatchContextDecisionKind.BLOCK,
                risk_kinds=[PatchContextRiskKind.REFERENCE_EXECUTION_RISK, PatchContextRiskKind.REFERENCE_IMPORT_RISK],
                message="Reference summaries must confirm no execution/import.",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_patch_context_validation_finding())
    return build_patch_context_validation_report(context_snapshot_id=snapshot.context_snapshot_id, findings=findings)


def patch_context_flags_preserve_no_write(flags: PatchContextFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_CONTEXT_FLAG_NAMES) and flags.production_certified is False


def patch_context_collection_policy_blocks_write(policy: PatchContextCollectionPolicy) -> bool:
    return (
        policy.allow_secret_file_read is False
        and policy.allow_credential_file_read is False
        and policy.allow_binary_file_read is False
        and policy.allow_outside_scope_read is False
        and policy.allow_shell is False
        and policy.allow_subprocess is False
        and policy.allow_workspace_write is False
        and policy.allow_code_edit is False
        and policy.allow_patch_application is False
        and policy.allow_raw_source_dump is False
    )


def patch_context_snapshot_is_not_patch_plan(snapshot: PatchContextSnapshot) -> bool:
    return (
        snapshot.ready_for_patch_plan is False
        and snapshot.ready_for_diff_proposal is False
        and snapshot.ready_for_patch_proposal is False
        and snapshot.ready_for_patch_application is False
        and snapshot.ready_for_execution is False
    )


def patch_context_evidence_bundle_is_not_diff_proposal(bundle: PatchContextEvidenceBundle) -> bool:
    return bundle.ready_for_patch_plan is False and bundle.ready_for_diff_proposal is False and bundle.ready_for_patch_proposal is False and bundle.ready_for_execution is False


def v0352_readiness_report_is_not_execution_ready(report: V0352ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_PATCH_CONTEXT_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
