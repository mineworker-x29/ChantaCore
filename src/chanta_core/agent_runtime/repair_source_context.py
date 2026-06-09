from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from hashlib import sha256
from pathlib import Path, PurePath
import re
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0382_VERSION = "v0.38.2"
V0382_RELEASE_NAME = "v0.38.2 Read-only Sandbox Source Context Snapshot"

SAFE_SOURCE_CONTEXT_FLAG_NAMES = (
    "ready_for_v0383_repair_scope_planner_change_intent",
    "ready_for_v0384_proposed_diff_code_hunk_metadata",
    "ready_for_read_only_sandbox_source_context",
    "ready_for_validated_sandbox_root_context",
    "ready_for_validated_read_only_sandbox_source_read",
    "ready_for_sandbox_source_read",
    "ready_for_source_context_snapshot",
    "ready_for_bounded_source_excerpt",
    "ready_for_source_path_validation",
    "ready_for_source_context_redaction",
    "ready_for_symbol_context_hint",
    "ready_for_source_context_sufficiency_assessment",
    "ready_for_future_repair_scope_planning_input",
    "ready_for_future_change_intent_input",
    "ready_for_future_proposed_diff_metadata_input",
    "ready_for_future_proposed_code_hunk_metadata_input",
)

UNSAFE_SOURCE_CONTEXT_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_live_workspace_read",
    "ready_for_unbounded_source_read",
    "ready_for_reference_source_read",
    "ready_for_secret_read",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
    "ready_for_repair_proposal_generation",
    "ready_for_proposed_diff_generation",
    "ready_for_proposed_code_hunk_generation",
    "ready_for_proposed_patch_envelope_generation",
    "ready_for_repair_patch_proposal",
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_repair_execution",
    "ready_for_repair_apply",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_automatic_repair",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_repair_loop",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_model_provider_invocation",
    "ready_for_tool_execution",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_SOURCE_CONTEXT_POLICY_ALLOW_NAMES = (
    "allow_live_workspace_read",
    "allow_unbounded_source_read",
    "allow_reference_source_read",
    "allow_secret_read",
    "allow_source_file_write",
    "allow_sandbox_source_write",
    "allow_repair_proposal_generation",
    "allow_proposed_diff_generation",
    "allow_proposed_code_hunk_generation",
    "allow_proposed_patch_envelope_generation",
    "allow_repair_execution",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_READ_DECISION_NAMES = (
    "live_workspace_read_allowed",
    "reference_read_allowed",
    "secret_read_allowed",
    "write_allowed",
    "proposal_generation_allowed",
    "diff_generation_allowed",
    "hunk_generation_allowed",
    "repair_execution_allowed",
)

UNSAFE_SOURCE_CONTEXT_SNAPSHOT_NAMES = (
    "live_workspace_read_performed",
    "reference_source_read_performed",
    "secret_read_performed",
    "unbounded_read_performed",
    "write_performed",
    "proposal_generated",
    "diff_generated",
    "hunk_generated",
    "patch_envelope_generated",
    "repair_executed",
    "production_certified",
    "ready_for_execution",
)

REQUIRED_SOURCE_CONTEXT_PROHIBITED_ACTIONS = (
    "live_read",
    "unbounded_read",
    "reference_read",
    "secret_read",
    "file_write",
    "proposal_generation",
    "diff_generation",
    "hunk_generation",
    "patch_apply",
    "repair_execution",
    "test_execution",
    "subprocess",
    "shell",
    "dependency_install",
    "network",
    "model_provider",
    "external_agent",
    "dominion",
)

SECRET_NAME_PATTERNS = (
    ".env",
    "credential",
    "credentials",
    "secret",
    "secrets",
    "token",
    "key",
    "private_key",
    "id_rsa",
    "cert",
    "certificate",
)

REFERENCE_PATH_FRAGMENTS = (
    "references/opencode",
    "references\\opencode",
    "references/hermes",
    "references\\hermes",
    "references/openclaw",
    "references\\openclaw",
)

SECRET_CONTENT_PATTERN = re.compile(
    r"(?i)(api[_-]?key|token|secret|password|private[_-]?key|credential)\s*[:=]\s*['\"]?[^'\"\s]+"
)


class RepairSourceContextMode(StrEnum):
    READ_ONLY_SANDBOX_SOURCE_CONTEXT = "read_only_sandbox_source_context"
    SANDBOX_ROOT_VALIDATION = "sandbox_root_validation"
    SOURCE_PATH_VALIDATION = "source_path_validation"
    BOUNDED_SOURCE_FILE_SNAPSHOT = "bounded_source_file_snapshot"
    BOUNDED_SOURCE_EXCERPT = "bounded_source_excerpt"
    SYMBOL_CONTEXT_HINT = "symbol_context_hint"
    SOURCE_CONTEXT_ASSESSMENT = "source_context_assessment"
    FUTURE_SCOPE_PLANNING_INPUT = "future_scope_planning_input"
    FUTURE_PATCH_METADATA_INPUT = "future_patch_metadata_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairSourceContextSourceKind(StrEnum):
    V0381_REPAIR_PROPOSAL_EVIDENCE_CONTRACT = "v0381_repair_proposal_evidence_contract"
    V0381_REPAIR_PROPOSAL_EVIDENCE_BUNDLE = "v0381_repair_proposal_evidence_bundle"
    V0381_REPAIR_PROPOSAL_ELIGIBILITY_DECISION = "v0381_repair_proposal_eligibility_decision"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0379_TEST_RUNNER_CONSOLIDATION = "v0379_test_runner_consolidation"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    V0375_REPAIR_SUGGESTION_ENVELOPE = "v0375_repair_suggestion_envelope"
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    SANDBOX_ROOT_ARGUMENT = "sandbox_root_argument"
    EXPLICIT_RELATIVE_PATH_CANDIDATE = "explicit_relative_path_candidate"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairSourceContextStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    SANDBOX_ROOT_VALIDATED = "sandbox_root_validated"
    PATH_CANDIDATES_VALIDATED = "path_candidates_validated"
    SOURCE_SNAPSHOT_CREATED = "source_snapshot_created"
    SOURCE_SNAPSHOT_CREATED_WITH_WARNINGS = "source_snapshot_created_with_warnings"
    CONTEXT_ASSESSED = "context_assessed"
    READY_FOR_FUTURE_SCOPE_PLANNING = "ready_for_future_scope_planning"
    READY_FOR_FUTURE_PATCH_METADATA = "ready_for_future_patch_metadata"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairSourceContextReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SOURCE_CONTEXT_CONTRACT_READY = "source_context_contract_ready"
    SANDBOX_ROOT_VALIDATION_READY = "sandbox_root_validation_ready"
    PATH_VALIDATION_READY = "path_validation_ready"
    BOUNDED_SOURCE_SNAPSHOT_READY = "bounded_source_snapshot_ready"
    BOUNDED_SOURCE_EXCERPT_READY = "bounded_source_excerpt_ready"
    SYMBOL_CONTEXT_HINT_READY = "symbol_context_hint_ready"
    SOURCE_CONTEXT_ASSESSMENT_READY = "source_context_assessment_ready"
    FUTURE_SCOPE_PLANNING_INPUT_READY = "future_scope_planning_input_ready"
    FUTURE_PATCH_METADATA_INPUT_READY = "future_patch_metadata_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0383 = "design_handoff_ready_for_v0383"
    DESIGN_HANDOFF_READY_FOR_V0384 = "design_handoff_ready_for_v0384"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairSourceContextDecisionKind(StrEnum):
    ALLOW_SANDBOX_ROOT_VALIDATION = "allow_sandbox_root_validation"
    ALLOW_SOURCE_PATH_VALIDATION = "allow_source_path_validation"
    ALLOW_BOUNDED_READ_ONLY_SANDBOX_SOURCE_READ = "allow_bounded_read_only_sandbox_source_read"
    ALLOW_BOUNDED_SOURCE_SNAPSHOT = "allow_bounded_source_snapshot"
    ALLOW_BOUNDED_SOURCE_EXCERPT = "allow_bounded_source_excerpt"
    ALLOW_SYMBOL_CONTEXT_HINT = "allow_symbol_context_hint"
    ALLOW_SOURCE_CONTEXT_ASSESSMENT = "allow_source_context_assessment"
    ALLOW_FUTURE_SCOPE_PLANNING_INPUT = "allow_future_scope_planning_input"
    ALLOW_FUTURE_PATCH_METADATA_INPUT = "allow_future_patch_metadata_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW = "choose_human_review"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairSourceContextRiskKind(StrEnum):
    MISSING_EVIDENCE_CONTRACT_RISK = "missing_evidence_contract_risk"
    MISSING_SANDBOX_ROOT_RISK = "missing_sandbox_root_risk"
    INVALID_SANDBOX_ROOT_RISK = "invalid_sandbox_root_risk"
    LIVE_WORKSPACE_READ_RISK = "live_workspace_read_risk"
    ABSOLUTE_PATH_RISK = "absolute_path_risk"
    PARENT_TRAVERSAL_RISK = "parent_traversal_risk"
    SYMLINK_ESCAPE_RISK = "symlink_escape_risk"
    REFERENCE_SOURCE_READ_RISK = "reference_source_read_risk"
    SECRET_FILE_READ_RISK = "secret_file_read_risk"
    BINARY_FILE_READ_RISK = "binary_file_read_risk"
    OVERSIZED_FILE_RISK = "oversized_file_risk"
    UNBOUNDED_READ_RISK = "unbounded_read_risk"
    IMPLICIT_PROJECT_SCAN_RISK = "implicit_project_scan_risk"
    SOURCE_MUTATION_RISK = "source_mutation_risk"
    SOURCE_EXECUTION_RISK = "source_execution_risk"
    IMPORT_EXECUTION_RISK = "import_execution_risk"
    PROPOSAL_GENERATION_CONFUSION_RISK = "proposal_generation_confusion_risk"
    DIFF_GENERATION_CONFUSION_RISK = "diff_generation_confusion_risk"
    HUNK_GENERATION_CONFUSION_RISK = "hunk_generation_confusion_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairSourceFileKind(StrEnum):
    PYTHON_SOURCE = "python_source"
    MARKDOWN = "markdown"
    TEXT = "text"
    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    CONFIG_NON_SECRET = "config_non_secret"
    TEST_SOURCE = "test_source"
    UNKNOWN_TEXT = "unknown_text"
    BINARY = "binary"
    SECRET_LIKE = "secret_like"
    UNSUPPORTED = "unsupported"


class RepairSourcePathDisposition(StrEnum):
    ACCEPTED = "accepted"
    ACCEPTED_WITH_WARNINGS = "accepted_with_warnings"
    DENIED_ABSOLUTE_PATH = "denied_absolute_path"
    DENIED_PARENT_TRAVERSAL = "denied_parent_traversal"
    DENIED_SYMLINK = "denied_symlink"
    DENIED_OUTSIDE_SANDBOX = "denied_outside_sandbox"
    DENIED_REFERENCE_PATH = "denied_reference_path"
    DENIED_SECRET_PATH = "denied_secret_path"
    DENIED_BINARY = "denied_binary"
    DENIED_OVERSIZED = "denied_oversized"
    DENIED_UNSUPPORTED_EXTENSION = "denied_unsupported_extension"
    DENIED_MISSING_FILE = "denied_missing_file"
    DENIED_DIRECTORY = "denied_directory"
    DENIED_UNKNOWN = "denied_unknown"
    REVIEW_REQUIRED = "review_required"


class RepairSourceExcerptKind(StrEnum):
    FULL_BOUNDED_FILE_EXCERPT = "full_bounded_file_excerpt"
    FOCUSED_LINE_WINDOW = "focused_line_window"
    SYMBOL_HINT_WINDOW = "symbol_hint_window"
    IMPORT_BLOCK_EXCERPT = "import_block_excerpt"
    FAILURE_RELATED_EXCERPT = "failure_related_excerpt"
    REDACTED_EXCERPT = "redacted_excerpt"
    TRUNCATED_EXCERPT = "truncated_excerpt"
    NO_EXCERPT = "no_excerpt"
    UNKNOWN = "unknown"


class RepairSourceContextSufficiencyKind(StrEnum):
    SUFFICIENT_FOR_FUTURE_SCOPE_PLANNING = "sufficient_for_future_scope_planning"
    SUFFICIENT_FOR_FUTURE_PATCH_METADATA = "sufficient_for_future_patch_metadata"
    SUFFICIENT_FOR_HUMAN_REVIEW = "sufficient_for_human_review"
    INSUFFICIENT_MISSING_SOURCE = "insufficient_missing_source"
    INSUFFICIENT_DENIED_PATHS = "insufficient_denied_paths"
    INSUFFICIENT_LOW_CONFIDENCE = "insufficient_low_confidence"
    BLOCKED_BY_SAFETY = "blocked_by_safety"
    NO_REPAIR_NEEDED = "no_repair_needed"
    UNKNOWN = "unknown"


class RepairSourceContextConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0382_VERSION not in version:
        raise ValueError("version must include v0.38.2")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.2")


def _validate_true(instance: Any, prefix: str = "no_") -> None:
    for name in instance.__dataclass_fields__:
        if name.startswith(prefix) and getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_metadata(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _is_absolute_path(raw_path: str) -> bool:
    path = PurePath(raw_path)
    return path.is_absolute() or bool(re.match(r"^[A-Za-z]:[\\/]", raw_path))


def _contains_parent_traversal(raw_path: str) -> bool:
    parts = PurePath(raw_path.replace("\\", "/")).parts
    return any(part == ".." for part in parts)


def _contains_reference_fragment(path_text: str) -> bool:
    lowered = path_text.lower().replace("\\", "/")
    return any(fragment.replace("\\", "/") in lowered for fragment in REFERENCE_PATH_FRAGMENTS)


def _is_secret_like_path(path_text: str, policy: RepairSourceContextPolicy | None = None) -> bool:
    lowered = path_text.lower()
    patterns = list(SECRET_NAME_PATTERNS)
    if policy is not None:
        patterns.extend(policy.prohibited_secret_name_patterns)
    return any(pattern.lower() in lowered for pattern in patterns)


def _redact_secret_like_text(text: str) -> tuple[str, bool]:
    redacted = SECRET_CONTENT_PATTERN.sub(r"\1=[REDACTED]", text)
    return redacted, redacted != text


def _path_has_symlink(root: Path, relative_path: str) -> bool:
    current = root
    for part in PurePath(relative_path.replace("\\", "/")).parts:
        current = current / part
        if current.exists() and current.is_symlink():
            return True
    return False


def _is_relative_to(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextFlagSet:
    flag_set_id: str
    version: str
    repair_source_context_layer_constructed: bool
    source_context_policy_available: bool
    sandbox_root_validation_available: bool
    source_path_validation_available: bool
    bounded_source_snapshot_available: bool
    bounded_source_excerpt_available: bool
    symbol_context_hint_available: bool
    source_context_assessment_available: bool
    ready_for_v0383_repair_scope_planner_change_intent: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_read_only_sandbox_source_context: bool
    ready_for_validated_sandbox_root_context: bool
    ready_for_validated_read_only_sandbox_source_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_source_context_snapshot: bool
    ready_for_bounded_source_excerpt: bool
    ready_for_source_path_validation: bool
    ready_for_source_context_redaction: bool
    ready_for_symbol_context_hint: bool
    ready_for_source_context_sufficiency_assessment: bool
    ready_for_future_repair_scope_planning_input: bool
    ready_for_future_change_intent_input: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_live_workspace_read: bool
    ready_for_unbounded_source_read: bool
    ready_for_reference_source_read: bool
    ready_for_secret_read: bool
    ready_for_source_file_write: bool
    ready_for_sandbox_source_write: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_proposed_code_hunk_generation: bool
    ready_for_proposed_patch_envelope_generation: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_repair_execution: bool
    ready_for_repair_apply: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_automatic_repair: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_repair_loop: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_model_provider_invocation: bool
    ready_for_tool_execution: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_provider_invocation: bool
    ready_for_direct_network_access: bool
    ready_for_credential_access: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_independent_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_ui_runtime: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        if self.ready_for_sandbox_source_read and not self.ready_for_validated_read_only_sandbox_source_read:
            raise ValueError("sandbox source read readiness requires validated read-only sandbox source read readiness")
        _validate_false(self, UNSAFE_SOURCE_CONTEXT_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextSourceRef:
    source_ref_id: str
    source_kind: RepairSourceContextSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairSourceContextSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextPolicy:
    source_context_policy_id: str
    version: str
    allowed_modes: list[RepairSourceContextMode | str]
    allowed_file_kinds: list[RepairSourceFileKind | str]
    denied_path_dispositions: list[RepairSourcePathDisposition | str]
    allowed_extensions: list[str]
    prohibited_path_fragments: list[str]
    prohibited_secret_name_patterns: list[str]
    max_file_bytes: int
    max_total_snapshot_chars: int
    max_excerpt_chars: int
    max_excerpts_per_file: int
    max_files: int
    allow_sandbox_root_validation: bool
    allow_explicit_relative_path_candidates: bool
    allow_bounded_read_only_sandbox_source_read: bool
    allow_bounded_source_snapshot: bool
    allow_bounded_source_excerpt: bool
    allow_symbol_context_hint: bool
    allow_future_scope_planning_input: bool
    allow_future_patch_metadata_input: bool
    allow_live_workspace_read: bool
    allow_unbounded_source_read: bool
    allow_reference_source_read: bool
    allow_secret_read: bool
    allow_source_file_write: bool
    allow_sandbox_source_write: bool
    allow_repair_proposal_generation: bool
    allow_proposed_diff_generation: bool
    allow_proposed_code_hunk_generation: bool
    allow_proposed_patch_envelope_generation: bool
    allow_repair_execution: bool
    allow_patch_application: bool
    allow_apply_patch: bool
    allow_git_apply: bool
    allow_test_execution: bool
    allow_subprocess: bool
    allow_shell: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_model_provider_invocation: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_context_policy_id", self.source_context_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, RepairSourceContextMode)
        _validate_enum_list("allowed_file_kinds", self.allowed_file_kinds, RepairSourceFileKind)
        _validate_enum_list("denied_path_dispositions", self.denied_path_dispositions, RepairSourcePathDisposition)
        for list_name in ("allowed_extensions", "prohibited_path_fragments", "prohibited_secret_name_patterns"):
            _validate_string_list(list_name, getattr(self, list_name))
        for name in ("max_file_bytes", "max_total_snapshot_chars", "max_excerpt_chars", "max_excerpts_per_file", "max_files"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(self, UNSAFE_SOURCE_CONTEXT_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSandboxRootValidationReport:
    sandbox_root_validation_id: str
    version: str
    sandbox_root_ref: str
    root_exists: bool
    root_is_directory: bool
    root_resolved_under_expected_parent: bool
    root_declared_sandbox: bool
    root_is_live_workspace: bool
    root_is_reference_corpus: bool
    root_contains_disallowed_marker: bool
    valid_for_read_only_context: bool
    validation_summary: str
    risk_kinds: list[RepairSourceContextRiskKind | str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("sandbox_root_validation_id", "sandbox_root_ref", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairSourceContextRiskKind)
        if self.valid_for_read_only_context and (
            not self.root_exists
            or not self.root_is_directory
            or not self.root_resolved_under_expected_parent
            or not self.root_declared_sandbox
            or self.root_is_live_workspace
            or self.root_is_reference_corpus
            or self.root_contains_disallowed_marker
        ):
            raise ValueError("invalid sandbox root cannot be valid_for_read_only_context")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextRequest:
    source_context_request_id: str
    version: str
    evidence_bundle_id: str | None
    eligibility_decision_id: str | None
    sandbox_root_ref: str
    requested_mode: RepairSourceContextMode | str
    path_candidates: list[str]
    requested_symbols: list[str]
    source_refs: list[RepairSourceContextSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_context_request_id", "sandbox_root_ref", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairSourceContextMode(self.requested_mode)
        _validate_string_list("path_candidates", self.path_candidates)
        _validate_string_list("requested_symbols", self.requested_symbols)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        for raw_path in self.path_candidates:
            if _is_absolute_path(raw_path) or _contains_parent_traversal(raw_path):
                raise ValueError("path_candidates must be explicit relative paths")
        missing = [item for item in REQUIRED_SOURCE_CONTEXT_PROHIBITED_ACTIONS if item not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError("prohibited_runtime_actions must include all unsafe surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourcePathCandidate:
    path_candidate_id: str
    raw_path: str
    normalized_relative_path: str | None
    file_kind: RepairSourceFileKind | str
    requested_excerpt_kind: RepairSourceExcerptKind | str
    rationale: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("path_candidate_id", "raw_path", "rationale"):
            _require_non_blank(name, getattr(self, name))
        RepairSourceFileKind(self.file_kind)
        RepairSourceExcerptKind(self.requested_excerpt_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourcePathValidationResult:
    path_validation_id: str
    path_candidate_id: str
    raw_path: str
    normalized_relative_path: str | None
    resolved_path_ref: str | None
    disposition: RepairSourcePathDisposition | str
    file_kind: RepairSourceFileKind | str
    exists: bool
    is_file: bool
    is_directory: bool
    is_symlink: bool
    is_inside_sandbox_root: bool
    is_reference_path: bool
    is_secret_like_path: bool
    is_binary_like: bool
    file_size_bytes: int | None
    read_allowed: bool
    denial_reason: str | None
    risk_kinds: list[RepairSourceContextRiskKind | str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("path_validation_id", "path_candidate_id", "raw_path"):
            _require_non_blank(name, getattr(self, name))
        disposition = RepairSourcePathDisposition(self.disposition)
        RepairSourceFileKind(self.file_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairSourceContextRiskKind)
        denied_dispositions = {item for item in RepairSourcePathDisposition if item not in (
            RepairSourcePathDisposition.ACCEPTED,
            RepairSourcePathDisposition.ACCEPTED_WITH_WARNINGS,
        )}
        unsafe_path_state = (
            self.is_symlink
            or not self.is_inside_sandbox_root
            or self.is_reference_path
            or self.is_secret_like_path
            or self.is_binary_like
            or not self.exists
            or not self.is_file
            or self.is_directory
        )
        if self.read_allowed and (disposition in denied_dispositions or unsafe_path_state):
            raise ValueError("read_allowed must be False for denied or unsafe path validation results")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceReadDecision:
    read_decision_id: str
    path_validation_id: str
    decision_kind: RepairSourceContextDecisionKind | str
    decision_summary: str
    read_allowed: bool
    source_read_performed: bool
    live_workspace_read_allowed: bool
    reference_read_allowed: bool
    secret_read_allowed: bool
    write_allowed: bool
    proposal_generation_allowed: bool
    diff_generation_allowed: bool
    hunk_generation_allowed: bool
    repair_execution_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("read_decision_id", "path_validation_id", "decision_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairSourceContextDecisionKind(self.decision_kind)
        if self.source_read_performed is not False:
            raise ValueError("source_read_performed must be False until snapshot builder performs validated read")
        _validate_false(self, UNSAFE_READ_DECISION_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceFileSnapshot:
    file_snapshot_id: str
    version: str
    path_validation_id: str
    normalized_relative_path: str
    file_kind: RepairSourceFileKind | str
    file_size_bytes: int | None
    content_digest: str | None
    bounded_content_preview: str
    redacted: bool
    truncated: bool
    source_read_performed: bool
    write_performed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("file_snapshot_id", "path_validation_id", "normalized_relative_path"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairSourceFileKind(self.file_kind)
        if self.write_performed is not False:
            raise ValueError("write_performed must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceExcerpt:
    source_excerpt_id: str
    file_snapshot_id: str
    excerpt_kind: RepairSourceExcerptKind | str
    normalized_relative_path: str
    start_line: int | None
    end_line: int | None
    excerpt_text: str
    excerpt_summary: str
    redacted: bool
    truncated: bool
    secret_like_content_detected: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_excerpt_id", "file_snapshot_id", "normalized_relative_path", "excerpt_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairSourceExcerptKind(self.excerpt_kind)
        if self.secret_like_content_detected and not self.redacted:
            raise ValueError("secret-like excerpt content must be redacted")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSymbolContextHint:
    symbol_context_hint_id: str
    source_excerpt_id: str | None
    normalized_relative_path: str
    symbol_name: str | None
    hint_summary: str
    line_range_summary: str | None
    confidence: RepairSourceContextConfidenceLevel | str
    imported_or_executed_source: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("symbol_context_hint_id", "normalized_relative_path", "hint_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairSourceContextConfidenceLevel(self.confidence)
        if self.imported_or_executed_source is not False:
            raise ValueError("symbol context hints must not import or execute source")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextAssessment:
    context_assessment_id: str
    sufficiency_kind: RepairSourceContextSufficiencyKind | str
    confidence: RepairSourceContextConfidenceLevel | str
    assessment_summary: str
    source_snapshot_ids: list[str]
    excerpt_ids: list[str]
    symbol_hint_ids: list[str]
    missing_context_items: list[str]
    denied_context_items: list[str]
    sufficient_for_future_scope_planning: bool
    sufficient_for_future_patch_metadata: bool
    human_review_required: bool
    do_nothing_remains_valid: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("context_assessment_id", "assessment_summary"):
            _require_non_blank(name, getattr(self, name))
        sufficiency = RepairSourceContextSufficiencyKind(self.sufficiency_kind)
        RepairSourceContextConfidenceLevel(self.confidence)
        for list_name in ("source_snapshot_ids", "excerpt_ids", "symbol_hint_ids", "missing_context_items", "denied_context_items"):
            _validate_string_list(list_name, getattr(self, list_name))
        if sufficiency in (
            RepairSourceContextSufficiencyKind.INSUFFICIENT_MISSING_SOURCE,
            RepairSourceContextSufficiencyKind.INSUFFICIENT_DENIED_PATHS,
            RepairSourceContextSufficiencyKind.INSUFFICIENT_LOW_CONFIDENCE,
            RepairSourceContextSufficiencyKind.BLOCKED_BY_SAFETY,
            RepairSourceContextSufficiencyKind.NO_REPAIR_NEEDED,
        ) and (self.sufficient_for_future_scope_planning or self.sufficient_for_future_patch_metadata):
            raise ValueError("future sufficiency flags must be False for insufficient/blocked/no-repair context")
        if self.do_nothing_remains_valid is not True:
            raise ValueError("do_nothing_remains_valid must remain True")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextSnapshot:
    source_context_snapshot_id: str
    version: str
    source_context_request_id: str
    sandbox_root_validation: RepairSandboxRootValidationReport
    path_candidates: list[RepairSourcePathCandidate]
    path_validation_results: list[RepairSourcePathValidationResult]
    read_decisions: list[RepairSourceReadDecision]
    file_snapshots: list[RepairSourceFileSnapshot]
    source_excerpts: list[RepairSourceExcerpt]
    symbol_context_hints: list[RepairSymbolContextHint]
    context_assessment: RepairSourceContextAssessment
    source_refs: list[RepairSourceContextSourceRef]
    snapshot_summary: str
    ready_for_future_scope_planning_input: bool
    ready_for_future_patch_metadata_input: bool
    live_workspace_read_performed: bool
    reference_source_read_performed: bool
    secret_read_performed: bool
    unbounded_read_performed: bool
    write_performed: bool
    proposal_generated: bool
    diff_generated: bool
    hunk_generated: bool
    patch_envelope_generated: bool
    repair_executed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_context_snapshot_id", "source_context_request_id", "snapshot_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if not isinstance(self.sandbox_root_validation, RepairSandboxRootValidationReport):
            raise TypeError("sandbox_root_validation must be RepairSandboxRootValidationReport")
        for list_name in ("path_candidates", "path_validation_results", "read_decisions", "file_snapshots", "source_excerpts", "symbol_context_hints", "source_refs"):
            _validate_list(list_name, getattr(self, list_name))
        if not isinstance(self.context_assessment, RepairSourceContextAssessment):
            raise TypeError("context_assessment must be RepairSourceContextAssessment")
        if self.ready_for_future_scope_planning_input and not self.context_assessment.sufficient_for_future_scope_planning:
            raise ValueError("future scope planning readiness requires context assessment support")
        if self.ready_for_future_patch_metadata_input and not self.context_assessment.sufficient_for_future_patch_metadata:
            raise ValueError("future patch metadata readiness requires context assessment support")
        _validate_false(self, UNSAFE_SOURCE_CONTEXT_SNAPSHOT_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairSourceContextRiskKind | str
    decision_kind: RepairSourceContextDecisionKind | str
    blocks_future_scope_planning: bool
    blocks_future_patch_metadata: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairSourceContextRiskKind(self.risk_kind)
        RepairSourceContextDecisionKind(self.decision_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextValidationReport:
    validation_report_id: str
    version: str
    source_context_snapshot_id: str
    findings: list[RepairSourceContextValidationFinding]
    validation_summary: str
    sandbox_root_validation_confirmed: bool
    path_validation_confirmed: bool
    bounded_excerpts_confirmed: bool
    redaction_confirmed: bool
    no_live_workspace_read_confirmed: bool
    no_reference_read_confirmed: bool
    no_secret_read_confirmed: bool
    no_unbounded_read_confirmed: bool
    no_write_confirmed: bool
    no_proposal_generation_confirmed: bool
    no_diff_generation_confirmed: bool
    no_hunk_generation_confirmed: bool
    no_patch_envelope_generation_confirmed: bool
    no_repair_execution_confirmed: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "source_context_snapshot_id", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        for name in self.__dataclass_fields__:
            if name.endswith("_confirmed") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextReport:
    source_context_report_id: str
    version: str
    source_context_snapshot_id: str
    validation_report_id: str
    readiness_level: RepairSourceContextReadinessLevel | str
    status: RepairSourceContextStatus | str
    report_summary: str
    ready_for_future_scope_planning_input: bool
    ready_for_future_patch_metadata_input: bool
    ready_for_execution: bool
    production_certified: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_context_report_id", "source_context_snapshot_id", "validation_report_id", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairSourceContextReadinessLevel(self.readiness_level)
        RepairSourceContextStatus(self.status)
        if self.ready_for_execution is not False or self.production_certified is not False:
            raise ValueError("source context report is not execution or production readiness")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextRunPreview:
    run_preview_id: str
    version: str
    requested_mode: RepairSourceContextMode | str
    preview_summary: str
    would_validate_root: bool
    would_validate_paths: bool
    would_read_bounded_sandbox_source: bool
    would_create_snapshot: bool
    would_read_live_workspace: bool
    would_read_reference_source: bool
    would_read_secret: bool
    would_write: bool
    would_generate_proposal: bool
    would_generate_diff: bool
    would_generate_hunk: bool
    would_execute_repair: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairSourceContextMode(self.requested_mode)
        for name in (
            "would_read_live_workspace",
            "would_read_reference_source",
            "would_read_secret",
            "would_write",
            "would_generate_proposal",
            "would_generate_diff",
            "would_generate_hunk",
            "would_execute_repair",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextNoMutationGuarantee:
    guarantee_id: str
    version: str
    no_live_workspace_read: bool
    no_unbounded_source_read: bool
    no_reference_source_read: bool
    no_secret_read: bool
    no_write: bool
    no_edit: bool
    no_apply: bool
    no_repair: bool
    no_generation: bool
    no_source_file_write: bool
    no_sandbox_source_write: bool
    no_repair_proposal_generation: bool
    no_proposed_diff_generation: bool
    no_proposed_code_hunk_generation: bool
    no_proposed_patch_envelope_generation: bool
    no_patch_application: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_test_execution: bool
    no_subprocess_execution: bool
    no_shell_execution: bool
    no_dependency_install: bool
    no_network_access: bool
    no_model_provider_invocation: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_persistent_trace_write: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0382ReadinessReport:
    readiness_report_id: str
    version: str
    source_context_snapshot_id: str
    readiness_level: RepairSourceContextReadinessLevel | str
    status: RepairSourceContextStatus | str
    summary: str
    evidence_refs: list[str]
    repair_source_context_layer_constructed: bool
    ready_for_v0383_repair_scope_planner_change_intent: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_read_only_sandbox_source_context: bool
    ready_for_validated_sandbox_root_context: bool
    ready_for_validated_read_only_sandbox_source_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_source_context_snapshot: bool
    ready_for_bounded_source_excerpt: bool
    ready_for_source_path_validation: bool
    ready_for_source_context_redaction: bool
    ready_for_symbol_context_hint: bool
    ready_for_source_context_sufficiency_assessment: bool
    ready_for_future_repair_scope_planning_input: bool
    ready_for_future_change_intent_input: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_live_workspace_read: bool
    ready_for_unbounded_source_read: bool
    ready_for_reference_source_read: bool
    ready_for_secret_read: bool
    ready_for_source_file_write: bool
    ready_for_sandbox_source_write: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_proposed_code_hunk_generation: bool
    ready_for_proposed_patch_envelope_generation: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_execution: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_patch_application: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_automatic_repair: bool
    ready_for_test_execution: bool
    ready_for_shell_execution: bool
    ready_for_model_provider_invocation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "source_context_snapshot_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairSourceContextReadinessLevel(self.readiness_level)
        RepairSourceContextStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, tuple(name for name in UNSAFE_SOURCE_CONTEXT_FLAG_NAMES if hasattr(self, name)))
        _validate_metadata(self.metadata)


def build_repair_source_context_flags(**kwargs: Any) -> RepairSourceContextFlagSet:
    safe_defaults = {
        "repair_source_context_layer_constructed": True,
        "source_context_policy_available": True,
        "sandbox_root_validation_available": True,
        "source_path_validation_available": True,
        "bounded_source_snapshot_available": True,
        "bounded_source_excerpt_available": True,
        "symbol_context_hint_available": True,
        "source_context_assessment_available": True,
        **{name: True for name in SAFE_SOURCE_CONTEXT_FLAG_NAMES},
    }
    return RepairSourceContextFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_source_context_flags:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_SOURCE_CONTEXT_FLAG_NAMES},
    )


def build_repair_source_context_source_ref(**kwargs: Any) -> RepairSourceContextSourceRef:
    source_kind = kwargs.pop("source_kind", RepairSourceContextSourceKind.V0381_REPAIR_PROPOSAL_EVIDENCE_BUNDLE)
    return RepairSourceContextSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", f"repair_source_context_source_ref:{str(source_kind)}"),
        source_kind=source_kind,
        source_id=kwargs.pop("source_id", "repair-proposal-evidence-bundle"),
        source_summary=kwargs.pop("source_summary", "source context metadata reference only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence bundle"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_source_context_policy(**kwargs: Any) -> RepairSourceContextPolicy:
    return RepairSourceContextPolicy(
        source_context_policy_id=kwargs.pop("source_context_policy_id", "repair_source_context_policy:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            RepairSourceContextMode.READ_ONLY_SANDBOX_SOURCE_CONTEXT,
            RepairSourceContextMode.SANDBOX_ROOT_VALIDATION,
            RepairSourceContextMode.SOURCE_PATH_VALIDATION,
            RepairSourceContextMode.BOUNDED_SOURCE_FILE_SNAPSHOT,
            RepairSourceContextMode.BOUNDED_SOURCE_EXCERPT,
            RepairSourceContextMode.SYMBOL_CONTEXT_HINT,
            RepairSourceContextMode.SOURCE_CONTEXT_ASSESSMENT,
            RepairSourceContextMode.FUTURE_SCOPE_PLANNING_INPUT,
            RepairSourceContextMode.FUTURE_PATCH_METADATA_INPUT,
        ]),
        allowed_file_kinds=kwargs.pop("allowed_file_kinds", [
            RepairSourceFileKind.PYTHON_SOURCE,
            RepairSourceFileKind.MARKDOWN,
            RepairSourceFileKind.TEXT,
            RepairSourceFileKind.JSON,
            RepairSourceFileKind.YAML,
            RepairSourceFileKind.TOML,
            RepairSourceFileKind.CONFIG_NON_SECRET,
            RepairSourceFileKind.TEST_SOURCE,
            RepairSourceFileKind.UNKNOWN_TEXT,
        ]),
        denied_path_dispositions=kwargs.pop("denied_path_dispositions", [
            RepairSourcePathDisposition.DENIED_ABSOLUTE_PATH,
            RepairSourcePathDisposition.DENIED_PARENT_TRAVERSAL,
            RepairSourcePathDisposition.DENIED_SYMLINK,
            RepairSourcePathDisposition.DENIED_OUTSIDE_SANDBOX,
            RepairSourcePathDisposition.DENIED_REFERENCE_PATH,
            RepairSourcePathDisposition.DENIED_SECRET_PATH,
            RepairSourcePathDisposition.DENIED_BINARY,
            RepairSourcePathDisposition.DENIED_OVERSIZED,
            RepairSourcePathDisposition.DENIED_UNSUPPORTED_EXTENSION,
            RepairSourcePathDisposition.DENIED_MISSING_FILE,
            RepairSourcePathDisposition.DENIED_DIRECTORY,
            RepairSourcePathDisposition.DENIED_UNKNOWN,
        ]),
        allowed_extensions=kwargs.pop("allowed_extensions", [".py", ".md", ".txt", ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg"]),
        prohibited_path_fragments=kwargs.pop("prohibited_path_fragments", [".git", *REFERENCE_PATH_FRAGMENTS]),
        prohibited_secret_name_patterns=kwargs.pop("prohibited_secret_name_patterns", list(SECRET_NAME_PATTERNS)),
        max_file_bytes=kwargs.pop("max_file_bytes", 64_000),
        max_total_snapshot_chars=kwargs.pop("max_total_snapshot_chars", 20_000),
        max_excerpt_chars=kwargs.pop("max_excerpt_chars", 2_000),
        max_excerpts_per_file=kwargs.pop("max_excerpts_per_file", 4),
        max_files=kwargs.pop("max_files", 8),
        allow_sandbox_root_validation=kwargs.pop("allow_sandbox_root_validation", True),
        allow_explicit_relative_path_candidates=kwargs.pop("allow_explicit_relative_path_candidates", True),
        allow_bounded_read_only_sandbox_source_read=kwargs.pop("allow_bounded_read_only_sandbox_source_read", True),
        allow_bounded_source_snapshot=kwargs.pop("allow_bounded_source_snapshot", True),
        allow_bounded_source_excerpt=kwargs.pop("allow_bounded_source_excerpt", True),
        allow_symbol_context_hint=kwargs.pop("allow_symbol_context_hint", True),
        allow_future_scope_planning_input=kwargs.pop("allow_future_scope_planning_input", True),
        allow_future_patch_metadata_input=kwargs.pop("allow_future_patch_metadata_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SOURCE_CONTEXT_POLICY_ALLOW_NAMES},
    )


def default_repair_source_context_policy(**kwargs: Any) -> RepairSourceContextPolicy:
    return build_repair_source_context_policy(**kwargs)


def build_repair_sandbox_root_validation_report(**kwargs: Any) -> RepairSandboxRootValidationReport:
    return RepairSandboxRootValidationReport(
        sandbox_root_validation_id=kwargs.pop("sandbox_root_validation_id", "repair_sandbox_root_validation:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "sandbox-root"),
        root_exists=kwargs.pop("root_exists", True),
        root_is_directory=kwargs.pop("root_is_directory", True),
        root_resolved_under_expected_parent=kwargs.pop("root_resolved_under_expected_parent", True),
        root_declared_sandbox=kwargs.pop("root_declared_sandbox", True),
        root_is_live_workspace=kwargs.pop("root_is_live_workspace", False),
        root_is_reference_corpus=kwargs.pop("root_is_reference_corpus", False),
        root_contains_disallowed_marker=kwargs.pop("root_contains_disallowed_marker", False),
        valid_for_read_only_context=kwargs.pop("valid_for_read_only_context", True),
        validation_summary=kwargs.pop("validation_summary", "sandbox root valid for bounded read-only context"),
        risk_kinds=kwargs.pop("risk_kinds", []),
        metadata=kwargs.pop("metadata", {}),
    )


def validate_repair_sandbox_root(
    sandbox_root: str | Path,
    *,
    declared_sandbox: bool = True,
    expected_parent: str | Path | None = None,
) -> RepairSandboxRootValidationReport:
    root = Path(sandbox_root)
    root_exists = root.exists()
    root_is_directory = root.is_dir()
    resolved = root.resolve(strict=False)
    expected_ok = True
    if expected_parent is not None:
        expected_ok = _is_relative_to(resolved, Path(expected_parent).resolve(strict=False))
    lowered = str(resolved).lower().replace("\\", "/")
    is_reference = _contains_reference_fragment(lowered)
    is_live_workspace = (resolved / ".git").exists()
    has_marker = is_reference or (resolved / ".git").exists()
    risks: list[RepairSourceContextRiskKind] = []
    if not root_exists or not root_is_directory or not declared_sandbox or not expected_ok:
        risks.append(RepairSourceContextRiskKind.INVALID_SANDBOX_ROOT_RISK)
    if is_live_workspace:
        risks.append(RepairSourceContextRiskKind.LIVE_WORKSPACE_READ_RISK)
    if is_reference:
        risks.append(RepairSourceContextRiskKind.REFERENCE_SOURCE_READ_RISK)
    valid = root_exists and root_is_directory and expected_ok and declared_sandbox and not is_live_workspace and not is_reference and not has_marker
    return build_repair_sandbox_root_validation_report(
        sandbox_root_ref=str(resolved),
        root_exists=root_exists,
        root_is_directory=root_is_directory,
        root_resolved_under_expected_parent=expected_ok,
        root_declared_sandbox=declared_sandbox,
        root_is_live_workspace=is_live_workspace,
        root_is_reference_corpus=is_reference,
        root_contains_disallowed_marker=has_marker,
        valid_for_read_only_context=valid,
        validation_summary="sandbox root accepted" if valid else "sandbox root denied",
        risk_kinds=risks,
    )


def build_repair_source_context_request(**kwargs: Any) -> RepairSourceContextRequest:
    return RepairSourceContextRequest(
        source_context_request_id=kwargs.pop("source_context_request_id", "repair_source_context_request:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"),
        eligibility_decision_id=kwargs.pop("eligibility_decision_id", "repair_proposal_eligibility_decision:v0.38.1"),
        sandbox_root_ref=kwargs.pop("sandbox_root_ref", "sandbox-root"),
        requested_mode=kwargs.pop("requested_mode", RepairSourceContextMode.READ_ONLY_SANDBOX_SOURCE_CONTEXT),
        path_candidates=kwargs.pop("path_candidates", ["src/example.py"]),
        requested_symbols=kwargs.pop("requested_symbols", []),
        source_refs=kwargs.pop("source_refs", [build_repair_source_context_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(REQUIRED_SOURCE_CONTEXT_PROHIBITED_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "read-only sandbox source context request only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_source_context_request_from_evidence_bundle(**kwargs: Any) -> RepairSourceContextRequest:
    return build_repair_source_context_request(**kwargs)


def normalize_repair_source_relative_path(raw_path: str) -> str | None:
    _require_non_blank("raw_path", raw_path)
    if _is_absolute_path(raw_path) or _contains_parent_traversal(raw_path):
        return None
    normalized = PurePath(raw_path.replace("\\", "/")).as_posix().lstrip("/")
    if not normalized or normalized in (".", ".."):
        return None
    return normalized


def classify_repair_source_file_kind(raw_path: str) -> RepairSourceFileKind:
    lowered = raw_path.lower()
    name = PurePath(lowered.replace("\\", "/")).name
    if _is_secret_like_path(lowered):
        return RepairSourceFileKind.SECRET_LIKE
    if name.startswith("test_") and lowered.endswith(".py"):
        return RepairSourceFileKind.TEST_SOURCE
    if lowered.endswith(".py"):
        return RepairSourceFileKind.PYTHON_SOURCE
    if lowered.endswith(".md"):
        return RepairSourceFileKind.MARKDOWN
    if lowered.endswith(".txt"):
        return RepairSourceFileKind.TEXT
    if lowered.endswith(".json"):
        return RepairSourceFileKind.JSON
    if lowered.endswith((".yaml", ".yml")):
        return RepairSourceFileKind.YAML
    if lowered.endswith(".toml"):
        return RepairSourceFileKind.TOML
    if lowered.endswith((".ini", ".cfg")):
        return RepairSourceFileKind.CONFIG_NON_SECRET
    if lowered.endswith((".png", ".jpg", ".jpeg", ".gif", ".pdf", ".exe", ".dll", ".so", ".zip", ".pyc")):
        return RepairSourceFileKind.BINARY
    return RepairSourceFileKind.UNSUPPORTED if "." in name else RepairSourceFileKind.UNKNOWN_TEXT


def build_repair_source_path_candidate(**kwargs: Any) -> RepairSourcePathCandidate:
    raw_path = kwargs.pop("raw_path", "src/example.py")
    return RepairSourcePathCandidate(
        path_candidate_id=kwargs.pop("path_candidate_id", "repair_source_path_candidate:v0.38.2"),
        raw_path=raw_path,
        normalized_relative_path=kwargs.pop("normalized_relative_path", normalize_repair_source_relative_path(raw_path)),
        file_kind=kwargs.pop("file_kind", classify_repair_source_file_kind(raw_path)),
        requested_excerpt_kind=kwargs.pop("requested_excerpt_kind", RepairSourceExcerptKind.FULL_BOUNDED_FILE_EXCERPT),
        rationale=kwargs.pop("rationale", "explicit relative path candidate from evidence metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence bundle"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_source_path_validation_result(**kwargs: Any) -> RepairSourcePathValidationResult:
    return RepairSourcePathValidationResult(
        path_validation_id=kwargs.pop("path_validation_id", "repair_source_path_validation:v0.38.2"),
        path_candidate_id=kwargs.pop("path_candidate_id", "repair_source_path_candidate:v0.38.2"),
        raw_path=kwargs.pop("raw_path", "src/example.py"),
        normalized_relative_path=kwargs.pop("normalized_relative_path", "src/example.py"),
        resolved_path_ref=kwargs.pop("resolved_path_ref", None),
        disposition=kwargs.pop("disposition", RepairSourcePathDisposition.ACCEPTED),
        file_kind=kwargs.pop("file_kind", RepairSourceFileKind.PYTHON_SOURCE),
        exists=kwargs.pop("exists", True),
        is_file=kwargs.pop("is_file", True),
        is_directory=kwargs.pop("is_directory", False),
        is_symlink=kwargs.pop("is_symlink", False),
        is_inside_sandbox_root=kwargs.pop("is_inside_sandbox_root", True),
        is_reference_path=kwargs.pop("is_reference_path", False),
        is_secret_like_path=kwargs.pop("is_secret_like_path", False),
        is_binary_like=kwargs.pop("is_binary_like", False),
        file_size_bytes=kwargs.pop("file_size_bytes", 100),
        read_allowed=kwargs.pop("read_allowed", True),
        denial_reason=kwargs.pop("denial_reason", None),
        risk_kinds=kwargs.pop("risk_kinds", []),
        metadata=kwargs.pop("metadata", {}),
    )


def validate_repair_source_path_candidate(
    sandbox_root_validation: RepairSandboxRootValidationReport,
    candidate: RepairSourcePathCandidate,
    policy: RepairSourceContextPolicy | None = None,
) -> RepairSourcePathValidationResult:
    policy = policy or default_repair_source_context_policy()
    raw_path = candidate.raw_path
    file_kind = classify_repair_source_file_kind(raw_path)
    risks: list[RepairSourceContextRiskKind] = []
    normalized = normalize_repair_source_relative_path(raw_path)
    disposition = RepairSourcePathDisposition.ACCEPTED
    denial_reason: str | None = None
    resolved_path_ref: str | None = None
    exists = False
    is_file = False
    is_directory = False
    is_symlink = False
    is_inside = False
    is_reference = _contains_reference_fragment(raw_path)
    is_secret = _is_secret_like_path(raw_path, policy)
    is_binary = file_kind == RepairSourceFileKind.BINARY
    file_size: int | None = None

    if not sandbox_root_validation.valid_for_read_only_context:
        disposition = RepairSourcePathDisposition.DENIED_OUTSIDE_SANDBOX
        denial_reason = "sandbox root is not valid for read-only context"
        risks.append(RepairSourceContextRiskKind.INVALID_SANDBOX_ROOT_RISK)
    elif _is_absolute_path(raw_path):
        disposition = RepairSourcePathDisposition.DENIED_ABSOLUTE_PATH
        denial_reason = "absolute paths are denied"
        risks.append(RepairSourceContextRiskKind.ABSOLUTE_PATH_RISK)
    elif _contains_parent_traversal(raw_path):
        disposition = RepairSourcePathDisposition.DENIED_PARENT_TRAVERSAL
        denial_reason = "parent traversal is denied"
        risks.append(RepairSourceContextRiskKind.PARENT_TRAVERSAL_RISK)
    elif normalized is None:
        disposition = RepairSourcePathDisposition.DENIED_UNKNOWN
        denial_reason = "path cannot be normalized"
        risks.append(RepairSourceContextRiskKind.UNKNOWN)
    else:
        root = Path(sandbox_root_validation.sandbox_root_ref).resolve(strict=False)
        target = root / normalized
        resolved = target.resolve(strict=False)
        resolved_path_ref = str(resolved)
        is_inside = _is_relative_to(resolved, root)
        is_symlink = _path_has_symlink(root, normalized)
        exists = target.exists()
        is_file = target.is_file()
        is_directory = target.is_dir()
        is_reference = is_reference or _contains_reference_fragment(normalized)
        is_secret = is_secret or _is_secret_like_path(normalized, policy)
        suffix = PurePath(normalized).suffix.lower()
        if is_symlink:
            disposition = RepairSourcePathDisposition.DENIED_SYMLINK
            denial_reason = "symlink paths are denied"
            risks.append(RepairSourceContextRiskKind.SYMLINK_ESCAPE_RISK)
        elif not is_inside:
            disposition = RepairSourcePathDisposition.DENIED_OUTSIDE_SANDBOX
            denial_reason = "path resolves outside sandbox root"
            risks.append(RepairSourceContextRiskKind.PARENT_TRAVERSAL_RISK)
        elif is_reference:
            disposition = RepairSourcePathDisposition.DENIED_REFERENCE_PATH
            denial_reason = "reference corpus paths are denied"
            risks.append(RepairSourceContextRiskKind.REFERENCE_SOURCE_READ_RISK)
        elif ".git" in normalized.lower().split("/"):
            disposition = RepairSourcePathDisposition.DENIED_SECRET_PATH
            denial_reason = ".git paths are denied"
            risks.append(RepairSourceContextRiskKind.SECRET_FILE_READ_RISK)
        elif is_secret:
            disposition = RepairSourcePathDisposition.DENIED_SECRET_PATH
            denial_reason = "secret-like paths are denied"
            risks.append(RepairSourceContextRiskKind.SECRET_FILE_READ_RISK)
        elif is_binary:
            disposition = RepairSourcePathDisposition.DENIED_BINARY
            denial_reason = "binary-like paths are denied"
            risks.append(RepairSourceContextRiskKind.BINARY_FILE_READ_RISK)
        elif suffix not in policy.allowed_extensions and file_kind != RepairSourceFileKind.UNKNOWN_TEXT:
            disposition = RepairSourcePathDisposition.DENIED_UNSUPPORTED_EXTENSION
            denial_reason = "extension is not allowed"
        elif not exists:
            disposition = RepairSourcePathDisposition.DENIED_MISSING_FILE
            denial_reason = "file does not exist"
        elif is_directory:
            disposition = RepairSourcePathDisposition.DENIED_DIRECTORY
            denial_reason = "directories are denied"
        elif not is_file:
            disposition = RepairSourcePathDisposition.DENIED_UNKNOWN
            denial_reason = "path is not a regular file"
        else:
            file_size = target.stat().st_size
            if file_size > policy.max_file_bytes:
                disposition = RepairSourcePathDisposition.DENIED_OVERSIZED
                denial_reason = "file exceeds max_file_bytes"
                risks.append(RepairSourceContextRiskKind.OVERSIZED_FILE_RISK)
            elif file_kind not in policy.allowed_file_kinds:
                disposition = RepairSourcePathDisposition.DENIED_UNSUPPORTED_EXTENSION
                denial_reason = "file kind is not allowed"

    accepted = disposition in (RepairSourcePathDisposition.ACCEPTED, RepairSourcePathDisposition.ACCEPTED_WITH_WARNINGS)
    return build_repair_source_path_validation_result(
        path_validation_id=f"repair_source_path_validation:{candidate.path_candidate_id}",
        path_candidate_id=candidate.path_candidate_id,
        raw_path=raw_path,
        normalized_relative_path=normalized,
        resolved_path_ref=resolved_path_ref,
        disposition=disposition,
        file_kind=file_kind,
        exists=exists,
        is_file=is_file,
        is_directory=is_directory,
        is_symlink=is_symlink,
        is_inside_sandbox_root=is_inside if resolved_path_ref else False,
        is_reference_path=is_reference,
        is_secret_like_path=is_secret,
        is_binary_like=is_binary,
        file_size_bytes=file_size,
        read_allowed=accepted,
        denial_reason=denial_reason,
        risk_kinds=risks,
    )


def build_repair_source_read_decision(**kwargs: Any) -> RepairSourceReadDecision:
    return RepairSourceReadDecision(
        read_decision_id=kwargs.pop("read_decision_id", "repair_source_read_decision:v0.38.2"),
        path_validation_id=kwargs.pop("path_validation_id", "repair_source_path_validation:v0.38.2"),
        decision_kind=kwargs.pop("decision_kind", RepairSourceContextDecisionKind.ALLOW_BOUNDED_READ_ONLY_SANDBOX_SOURCE_READ),
        decision_summary=kwargs.pop("decision_summary", "bounded read-only sandbox source read decision"),
        read_allowed=kwargs.pop("read_allowed", True),
        source_read_performed=kwargs.pop("source_read_performed", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 path validation"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_READ_DECISION_NAMES},
    )


def decide_repair_source_read(
    path_validation: RepairSourcePathValidationResult,
    policy: RepairSourceContextPolicy | None = None,
) -> RepairSourceReadDecision:
    policy = policy or default_repair_source_context_policy()
    allowed = path_validation.read_allowed and policy.allow_bounded_read_only_sandbox_source_read
    return build_repair_source_read_decision(
        path_validation_id=path_validation.path_validation_id,
        decision_kind=RepairSourceContextDecisionKind.ALLOW_BOUNDED_READ_ONLY_SANDBOX_SOURCE_READ if allowed else RepairSourceContextDecisionKind.DENY,
        decision_summary="bounded read-only sandbox source read allowed" if allowed else "source read denied by path validation",
        read_allowed=allowed,
    )


def read_bounded_read_only_sandbox_source_file(
    sandbox_root_validation: RepairSandboxRootValidationReport,
    path_validation: RepairSourcePathValidationResult,
    policy: RepairSourceContextPolicy | None = None,
) -> tuple[str, bool, bool, str | None, int | None]:
    policy = policy or default_repair_source_context_policy()
    if not sandbox_root_validation.valid_for_read_only_context:
        raise ValueError("sandbox root is not valid for read-only context")
    if not path_validation.read_allowed or path_validation.resolved_path_ref is None:
        raise ValueError("path validation does not allow read")
    target = Path(path_validation.resolved_path_ref)
    root = Path(sandbox_root_validation.sandbox_root_ref).resolve(strict=False)
    resolved = target.resolve(strict=False)
    if not _is_relative_to(resolved, root):
        raise ValueError("validated path escaped sandbox root")
    if target.is_symlink() or _is_secret_like_path(str(target), policy) or _contains_reference_fragment(str(target)):
        raise ValueError("unsafe source path cannot be read")
    file_size = target.stat().st_size
    if file_size > policy.max_file_bytes:
        raise ValueError("file exceeds max_file_bytes")
    data = target.read_bytes()
    digest = sha256(data).hexdigest()
    text = data.decode("utf-8", errors="replace")
    redacted_text, redacted = _redact_secret_like_text(text)
    truncated = len(redacted_text) > policy.max_total_snapshot_chars
    preview = redacted_text[: policy.max_total_snapshot_chars]
    return preview, redacted, truncated, digest, file_size


def build_repair_source_file_snapshot(**kwargs: Any) -> RepairSourceFileSnapshot:
    return RepairSourceFileSnapshot(
        file_snapshot_id=kwargs.pop("file_snapshot_id", "repair_source_file_snapshot:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        path_validation_id=kwargs.pop("path_validation_id", "repair_source_path_validation:v0.38.2"),
        normalized_relative_path=kwargs.pop("normalized_relative_path", "src/example.py"),
        file_kind=kwargs.pop("file_kind", RepairSourceFileKind.PYTHON_SOURCE),
        file_size_bytes=kwargs.pop("file_size_bytes", 100),
        content_digest=kwargs.pop("content_digest", None),
        bounded_content_preview=kwargs.pop("bounded_content_preview", "def example():\n    return True\n"),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        source_read_performed=kwargs.pop("source_read_performed", True),
        write_performed=kwargs.pop("write_performed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def create_repair_source_file_snapshot(
    sandbox_root_validation: RepairSandboxRootValidationReport,
    path_validation: RepairSourcePathValidationResult,
    policy: RepairSourceContextPolicy | None = None,
) -> RepairSourceFileSnapshot:
    policy = policy or default_repair_source_context_policy()
    preview, redacted, truncated, digest, file_size = read_bounded_read_only_sandbox_source_file(
        sandbox_root_validation,
        path_validation,
        policy,
    )
    return build_repair_source_file_snapshot(
        file_snapshot_id=f"repair_source_file_snapshot:{path_validation.path_validation_id}",
        path_validation_id=path_validation.path_validation_id,
        normalized_relative_path=path_validation.normalized_relative_path or path_validation.raw_path,
        file_kind=path_validation.file_kind,
        file_size_bytes=file_size,
        content_digest=digest,
        bounded_content_preview=preview,
        redacted=redacted,
        truncated=truncated,
        source_read_performed=True,
    )


def build_repair_source_excerpt(**kwargs: Any) -> RepairSourceExcerpt:
    return RepairSourceExcerpt(
        source_excerpt_id=kwargs.pop("source_excerpt_id", "repair_source_excerpt:v0.38.2"),
        file_snapshot_id=kwargs.pop("file_snapshot_id", "repair_source_file_snapshot:v0.38.2"),
        excerpt_kind=kwargs.pop("excerpt_kind", RepairSourceExcerptKind.FULL_BOUNDED_FILE_EXCERPT),
        normalized_relative_path=kwargs.pop("normalized_relative_path", "src/example.py"),
        start_line=kwargs.pop("start_line", 1),
        end_line=kwargs.pop("end_line", 1),
        excerpt_text=kwargs.pop("excerpt_text", "def example(): ..."),
        excerpt_summary=kwargs.pop("excerpt_summary", "bounded source excerpt metadata"),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        secret_like_content_detected=kwargs.pop("secret_like_content_detected", False),
        metadata=kwargs.pop("metadata", {}),
    )


def create_repair_source_excerpts(
    snapshot: RepairSourceFileSnapshot,
    policy: RepairSourceContextPolicy | None = None,
) -> list[RepairSourceExcerpt]:
    policy = policy or default_repair_source_context_policy()
    text = snapshot.bounded_content_preview
    excerpt_text = text[: policy.max_excerpt_chars]
    redacted_text, secret_detected = _redact_secret_like_text(excerpt_text)
    secret_detected = secret_detected or snapshot.redacted
    lines = redacted_text.splitlines()
    return [build_repair_source_excerpt(
        source_excerpt_id=f"repair_source_excerpt:{snapshot.file_snapshot_id}:1",
        file_snapshot_id=snapshot.file_snapshot_id,
        excerpt_kind=RepairSourceExcerptKind.REDACTED_EXCERPT if snapshot.redacted or secret_detected else RepairSourceExcerptKind.FULL_BOUNDED_FILE_EXCERPT,
        normalized_relative_path=snapshot.normalized_relative_path,
        start_line=1,
        end_line=max(1, len(lines)),
        excerpt_text=redacted_text,
        excerpt_summary="bounded and redacted source excerpt",
        redacted=snapshot.redacted or secret_detected,
        truncated=snapshot.truncated or len(text) > policy.max_excerpt_chars,
        secret_like_content_detected=secret_detected,
    )]


def build_repair_symbol_context_hint(**kwargs: Any) -> RepairSymbolContextHint:
    return RepairSymbolContextHint(
        symbol_context_hint_id=kwargs.pop("symbol_context_hint_id", "repair_symbol_context_hint:v0.38.2"),
        source_excerpt_id=kwargs.pop("source_excerpt_id", None),
        normalized_relative_path=kwargs.pop("normalized_relative_path", "src/example.py"),
        symbol_name=kwargs.pop("symbol_name", None),
        hint_summary=kwargs.pop("hint_summary", "non-executing text heuristic symbol hint"),
        line_range_summary=kwargs.pop("line_range_summary", None),
        confidence=kwargs.pop("confidence", RepairSourceContextConfidenceLevel.MEDIUM),
        imported_or_executed_source=kwargs.pop("imported_or_executed_source", False),
        metadata=kwargs.pop("metadata", {}),
    )


def create_repair_symbol_context_hints(
    excerpts: list[RepairSourceExcerpt],
    requested_symbols: list[str] | None = None,
) -> list[RepairSymbolContextHint]:
    requested = set(requested_symbols or [])
    hints: list[RepairSymbolContextHint] = []
    for excerpt in excerpts:
        lines = excerpt.excerpt_text.splitlines()
        for index, line in enumerate(lines, start=1):
            stripped = line.strip()
            symbol: str | None = None
            if stripped.startswith("def "):
                symbol = stripped[4:].split("(", 1)[0].strip()
            elif stripped.startswith("class "):
                symbol = stripped[6:].split("(", 1)[0].split(":", 1)[0].strip()
            elif stripped.startswith("function "):
                symbol = stripped[9:].split("(", 1)[0].strip()
            if symbol and (not requested or symbol in requested):
                hints.append(build_repair_symbol_context_hint(
                    symbol_context_hint_id=f"repair_symbol_context_hint:{excerpt.source_excerpt_id}:{symbol}",
                    source_excerpt_id=excerpt.source_excerpt_id,
                    normalized_relative_path=excerpt.normalized_relative_path,
                    symbol_name=symbol,
                    hint_summary=f"symbol {symbol} found by non-executing text heuristic",
                    line_range_summary=f"line {index}",
                    confidence=RepairSourceContextConfidenceLevel.MEDIUM,
                ))
    return hints


def build_repair_source_context_assessment(**kwargs: Any) -> RepairSourceContextAssessment:
    return RepairSourceContextAssessment(
        context_assessment_id=kwargs.pop("context_assessment_id", "repair_source_context_assessment:v0.38.2"),
        sufficiency_kind=kwargs.pop("sufficiency_kind", RepairSourceContextSufficiencyKind.SUFFICIENT_FOR_FUTURE_SCOPE_PLANNING),
        confidence=kwargs.pop("confidence", RepairSourceContextConfidenceLevel.MEDIUM),
        assessment_summary=kwargs.pop("assessment_summary", "source context sufficient for future-gated planning input"),
        source_snapshot_ids=kwargs.pop("source_snapshot_ids", ["repair_source_file_snapshot:v0.38.2"]),
        excerpt_ids=kwargs.pop("excerpt_ids", ["repair_source_excerpt:v0.38.2"]),
        symbol_hint_ids=kwargs.pop("symbol_hint_ids", []),
        missing_context_items=kwargs.pop("missing_context_items", []),
        denied_context_items=kwargs.pop("denied_context_items", []),
        sufficient_for_future_scope_planning=kwargs.pop("sufficient_for_future_scope_planning", True),
        sufficient_for_future_patch_metadata=kwargs.pop("sufficient_for_future_patch_metadata", False),
        human_review_required=kwargs.pop("human_review_required", True),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        metadata=kwargs.pop("metadata", {}),
    )


def assess_repair_source_context(
    file_snapshots: list[RepairSourceFileSnapshot],
    source_excerpts: list[RepairSourceExcerpt],
    symbol_context_hints: list[RepairSymbolContextHint],
    denied_context_items: list[str] | None = None,
) -> RepairSourceContextAssessment:
    denied = denied_context_items or []
    if not file_snapshots or not source_excerpts:
        return build_repair_source_context_assessment(
            sufficiency_kind=RepairSourceContextSufficiencyKind.INSUFFICIENT_MISSING_SOURCE,
            confidence=RepairSourceContextConfidenceLevel.LOW,
            assessment_summary="source context is insufficient because no bounded snapshot/excerpt is present",
            source_snapshot_ids=[snapshot.file_snapshot_id for snapshot in file_snapshots],
            excerpt_ids=[excerpt.source_excerpt_id for excerpt in source_excerpts],
            symbol_hint_ids=[hint.symbol_context_hint_id for hint in symbol_context_hints],
            missing_context_items=["bounded source snapshot or excerpt"],
            denied_context_items=denied,
            sufficient_for_future_scope_planning=False,
            sufficient_for_future_patch_metadata=False,
        )
    if denied:
        return build_repair_source_context_assessment(
            sufficiency_kind=RepairSourceContextSufficiencyKind.INSUFFICIENT_DENIED_PATHS,
            confidence=RepairSourceContextConfidenceLevel.LOW,
            assessment_summary="source context has denied path candidates and requires review",
            source_snapshot_ids=[snapshot.file_snapshot_id for snapshot in file_snapshots],
            excerpt_ids=[excerpt.source_excerpt_id for excerpt in source_excerpts],
            symbol_hint_ids=[hint.symbol_context_hint_id for hint in symbol_context_hints],
            missing_context_items=[],
            denied_context_items=denied,
            sufficient_for_future_scope_planning=False,
            sufficient_for_future_patch_metadata=False,
        )
    return build_repair_source_context_assessment(
        sufficiency_kind=RepairSourceContextSufficiencyKind.SUFFICIENT_FOR_FUTURE_PATCH_METADATA if symbol_context_hints else RepairSourceContextSufficiencyKind.SUFFICIENT_FOR_FUTURE_SCOPE_PLANNING,
        confidence=RepairSourceContextConfidenceLevel.MEDIUM,
        source_snapshot_ids=[snapshot.file_snapshot_id for snapshot in file_snapshots],
        excerpt_ids=[excerpt.source_excerpt_id for excerpt in source_excerpts],
        symbol_hint_ids=[hint.symbol_context_hint_id for hint in symbol_context_hints],
        missing_context_items=[],
        denied_context_items=[],
        sufficient_for_future_scope_planning=True,
        sufficient_for_future_patch_metadata=bool(symbol_context_hints),
    )


def build_repair_source_context_snapshot(**kwargs: Any) -> RepairSourceContextSnapshot:
    assessment = kwargs.pop("context_assessment", build_repair_source_context_assessment())
    return RepairSourceContextSnapshot(
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        source_context_request_id=kwargs.pop("source_context_request_id", "repair_source_context_request:v0.38.2"),
        sandbox_root_validation=kwargs.pop("sandbox_root_validation", build_repair_sandbox_root_validation_report()),
        path_candidates=kwargs.pop("path_candidates", [build_repair_source_path_candidate()]),
        path_validation_results=kwargs.pop("path_validation_results", [build_repair_source_path_validation_result()]),
        read_decisions=kwargs.pop("read_decisions", [build_repair_source_read_decision()]),
        file_snapshots=kwargs.pop("file_snapshots", [build_repair_source_file_snapshot()]),
        source_excerpts=kwargs.pop("source_excerpts", [build_repair_source_excerpt()]),
        symbol_context_hints=kwargs.pop("symbol_context_hints", []),
        context_assessment=assessment,
        source_refs=kwargs.pop("source_refs", [build_repair_source_context_source_ref()]),
        snapshot_summary=kwargs.pop("snapshot_summary", "read-only sandbox source context snapshot metadata only"),
        ready_for_future_scope_planning_input=kwargs.pop("ready_for_future_scope_planning_input", assessment.sufficient_for_future_scope_planning),
        ready_for_future_patch_metadata_input=kwargs.pop("ready_for_future_patch_metadata_input", assessment.sufficient_for_future_patch_metadata),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SOURCE_CONTEXT_SNAPSHOT_NAMES},
    )


def create_repair_source_context_snapshot(
    request: RepairSourceContextRequest,
    policy: RepairSourceContextPolicy | None = None,
) -> RepairSourceContextSnapshot:
    policy = policy or default_repair_source_context_policy()
    root_validation = validate_repair_sandbox_root(request.sandbox_root_ref)
    candidates = [build_repair_source_path_candidate(raw_path=raw_path) for raw_path in request.path_candidates[: policy.max_files]]
    validations = [validate_repair_source_path_candidate(root_validation, candidate, policy) for candidate in candidates]
    decisions = [decide_repair_source_read(validation, policy) for validation in validations]
    file_snapshots: list[RepairSourceFileSnapshot] = []
    excerpts: list[RepairSourceExcerpt] = []
    denied: list[str] = []
    for validation, decision in zip(validations, decisions):
        if decision.read_allowed:
            snapshot = create_repair_source_file_snapshot(root_validation, validation, policy)
            file_snapshots.append(snapshot)
            excerpts.extend(create_repair_source_excerpts(snapshot, policy))
        else:
            denied.append(validation.raw_path)
    hints = create_repair_symbol_context_hints(excerpts, request.requested_symbols)
    assessment = assess_repair_source_context(file_snapshots, excerpts, hints, denied)
    return build_repair_source_context_snapshot(
        source_context_request_id=request.source_context_request_id,
        sandbox_root_validation=root_validation,
        path_candidates=candidates,
        path_validation_results=validations,
        read_decisions=decisions,
        file_snapshots=file_snapshots,
        source_excerpts=excerpts,
        symbol_context_hints=hints,
        context_assessment=assessment,
        source_refs=request.source_refs,
    )


def build_repair_source_context_validation_finding(**kwargs: Any) -> RepairSourceContextValidationFinding:
    return RepairSourceContextValidationFinding(
        finding_id=kwargs.pop("finding_id", "repair_source_context_validation_finding:v0.38.2"),
        finding_summary=kwargs.pop("finding_summary", "source context snapshot preserves no mutation or generation"),
        risk_kind=kwargs.pop("risk_kind", RepairSourceContextRiskKind.SOURCE_MUTATION_RISK),
        decision_kind=kwargs.pop("decision_kind", RepairSourceContextDecisionKind.ALLOW_BOUNDED_SOURCE_SNAPSHOT),
        blocks_future_scope_planning=kwargs.pop("blocks_future_scope_planning", False),
        blocks_future_patch_metadata=kwargs.pop("blocks_future_patch_metadata", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 source context validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_source_context_validation_report(**kwargs: Any) -> RepairSourceContextValidationReport:
    return RepairSourceContextValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "repair_source_context_validation_report:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"),
        findings=kwargs.pop("findings", [build_repair_source_context_validation_finding()]),
        validation_summary=kwargs.pop("validation_summary", "source context validation confirms bounded read-only posture"),
        sandbox_root_validation_confirmed=kwargs.pop("sandbox_root_validation_confirmed", True),
        path_validation_confirmed=kwargs.pop("path_validation_confirmed", True),
        bounded_excerpts_confirmed=kwargs.pop("bounded_excerpts_confirmed", True),
        redaction_confirmed=kwargs.pop("redaction_confirmed", True),
        no_live_workspace_read_confirmed=kwargs.pop("no_live_workspace_read_confirmed", True),
        no_reference_read_confirmed=kwargs.pop("no_reference_read_confirmed", True),
        no_secret_read_confirmed=kwargs.pop("no_secret_read_confirmed", True),
        no_unbounded_read_confirmed=kwargs.pop("no_unbounded_read_confirmed", True),
        no_write_confirmed=kwargs.pop("no_write_confirmed", True),
        no_proposal_generation_confirmed=kwargs.pop("no_proposal_generation_confirmed", True),
        no_diff_generation_confirmed=kwargs.pop("no_diff_generation_confirmed", True),
        no_hunk_generation_confirmed=kwargs.pop("no_hunk_generation_confirmed", True),
        no_patch_envelope_generation_confirmed=kwargs.pop("no_patch_envelope_generation_confirmed", True),
        no_repair_execution_confirmed=kwargs.pop("no_repair_execution_confirmed", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def validate_repair_source_context_snapshot(snapshot: RepairSourceContextSnapshot) -> RepairSourceContextValidationReport:
    return build_repair_source_context_validation_report(source_context_snapshot_id=snapshot.source_context_snapshot_id)


def build_repair_source_context_report(**kwargs: Any) -> RepairSourceContextReport:
    snapshot = kwargs.pop("snapshot", None)
    validation_report = kwargs.pop("validation_report", None)
    return RepairSourceContextReport(
        source_context_report_id=kwargs.pop("source_context_report_id", "repair_source_context_report:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", snapshot.source_context_snapshot_id if snapshot else "repair_source_context_snapshot:v0.38.2"),
        validation_report_id=kwargs.pop("validation_report_id", validation_report.validation_report_id if validation_report else "repair_source_context_validation_report:v0.38.2"),
        readiness_level=kwargs.pop("readiness_level", RepairSourceContextReadinessLevel.BOUNDED_SOURCE_SNAPSHOT_READY),
        status=kwargs.pop("status", RepairSourceContextStatus.SOURCE_SNAPSHOT_CREATED),
        report_summary=kwargs.pop("report_summary", "source context report metadata only"),
        ready_for_future_scope_planning_input=kwargs.pop("ready_for_future_scope_planning_input", snapshot.ready_for_future_scope_planning_input if snapshot else True),
        ready_for_future_patch_metadata_input=kwargs.pop("ready_for_future_patch_metadata_input", snapshot.ready_for_future_patch_metadata_input if snapshot else False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 source context snapshot"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_source_context_run_preview(**kwargs: Any) -> RepairSourceContextRunPreview:
    return RepairSourceContextRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "repair_source_context_run_preview:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        requested_mode=kwargs.pop("requested_mode", RepairSourceContextMode.READ_ONLY_SANDBOX_SOURCE_CONTEXT),
        preview_summary=kwargs.pop("preview_summary", "would validate root and read bounded sandbox source only"),
        would_validate_root=kwargs.pop("would_validate_root", True),
        would_validate_paths=kwargs.pop("would_validate_paths", True),
        would_read_bounded_sandbox_source=kwargs.pop("would_read_bounded_sandbox_source", True),
        would_create_snapshot=kwargs.pop("would_create_snapshot", True),
        would_read_live_workspace=kwargs.pop("would_read_live_workspace", False),
        would_read_reference_source=kwargs.pop("would_read_reference_source", False),
        would_read_secret=kwargs.pop("would_read_secret", False),
        would_write=kwargs.pop("would_write", False),
        would_generate_proposal=kwargs.pop("would_generate_proposal", False),
        would_generate_diff=kwargs.pop("would_generate_diff", False),
        would_generate_hunk=kwargs.pop("would_generate_hunk", False),
        would_execute_repair=kwargs.pop("would_execute_repair", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_source_context_no_mutation_guarantee(**kwargs: Any) -> RepairSourceContextNoMutationGuarantee:
    no_names = tuple(name for name in RepairSourceContextNoMutationGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return RepairSourceContextNoMutationGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_source_context_no_mutation_guarantee:v0.38.2"),
        version=kwargs.pop("version", V0382_VERSION),
        summary=kwargs.pop("summary", "v0.38.2 reads bounded sandbox source only and mutates/generates nothing"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0382_readiness_report(**kwargs: Any) -> V0382ReadinessReport:
    safe_defaults = {
        "repair_source_context_layer_constructed": True,
        **{name: True for name in SAFE_SOURCE_CONTEXT_FLAG_NAMES},
    }
    return V0382ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0382_readiness_report"),
        version=kwargs.pop("version", V0382_VERSION),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"),
        readiness_level=kwargs.pop("readiness_level", RepairSourceContextReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0383),
        status=kwargs.pop("status", RepairSourceContextStatus.SOURCE_SNAPSHOT_CREATED),
        summary=kwargs.pop("summary", "v0.38.2 read-only sandbox source context ready; unsafe runtime remains false"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence bundle"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_SOURCE_CONTEXT_FLAG_NAMES if name in V0382ReadinessReport.__dataclass_fields__},
    )


def repair_source_context_flags_preserve_no_mutation(flags: RepairSourceContextFlagSet) -> bool:
    return isinstance(flags, RepairSourceContextFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_SOURCE_CONTEXT_FLAG_NAMES)


def repair_source_context_policy_blocks_live_and_unbounded_read(policy: RepairSourceContextPolicy) -> bool:
    return isinstance(policy, RepairSourceContextPolicy) and all(getattr(policy, name) is False for name in UNSAFE_SOURCE_CONTEXT_POLICY_ALLOW_NAMES)


def repair_source_path_validation_blocks_escape(result: RepairSourcePathValidationResult) -> bool:
    if not isinstance(result, RepairSourcePathValidationResult):
        return False
    if result.disposition in (
        RepairSourcePathDisposition.DENIED_ABSOLUTE_PATH,
        RepairSourcePathDisposition.DENIED_PARENT_TRAVERSAL,
        RepairSourcePathDisposition.DENIED_SYMLINK,
        RepairSourcePathDisposition.DENIED_OUTSIDE_SANDBOX,
        RepairSourcePathDisposition.DENIED_REFERENCE_PATH,
        RepairSourcePathDisposition.DENIED_SECRET_PATH,
    ):
        return result.read_allowed is False
    return True


def repair_source_snapshot_is_not_proposal(snapshot: RepairSourceFileSnapshot) -> bool:
    return isinstance(snapshot, RepairSourceFileSnapshot) and snapshot.write_performed is False


def repair_source_context_snapshot_is_not_generation(snapshot: RepairSourceContextSnapshot) -> bool:
    return isinstance(snapshot, RepairSourceContextSnapshot) and all(
        getattr(snapshot, name) is False for name in UNSAFE_SOURCE_CONTEXT_SNAPSHOT_NAMES
    )


def v0382_readiness_report_is_not_execution_ready(report: V0382ReadinessReport) -> bool:
    return isinstance(report, V0382ReadinessReport) and all(
        getattr(report, name) is False for name in UNSAFE_SOURCE_CONTEXT_FLAG_NAMES if hasattr(report, name)
    )
