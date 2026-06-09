from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_diff_proposal import (
    DiffProposalEnvelope,
    DiffProposalTargetKind,
    PatchFileProposal,
    PatchHunkProposal,
    StructuredPatchProposal,
    UnifiedDiffProposal,
)


V0355_VERSION = "v0.35.5"
V0355_RELEASE_NAME = "v0.35.5 Patch Risk & Conformance Scanner"
DEFAULT_V0355_DOC_PATH = "docs/versions/v0.35/v0.35.5_patch_risk_conformance_scanner.md"
DEFAULT_V0354_DIFF_DOC_REF = "docs/versions/v0.35/v0.35.4_diff_proposal_envelope.md"
DEFAULT_V0353_PLAN_DOC_REF = "docs/versions/v0.35/v0.35.3_reference_informed_patch_plan_change_set_graph.md"
DEFAULT_V0352_CONTEXT_DOC_REF = "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"
DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS = 600
DEFAULT_MAX_DIFF_SCAN_CHARS = 8000

DEFAULT_PROHIBITED_RUNTIME_ACTIONS = [
    "patch_application",
    "workspace_write",
    "code_edit",
    "apply_patch",
    "git_apply",
    "shell_execution",
    "subprocess_execution",
    "command_execution",
    "test_execution",
    "dependency_install",
    "reference_execution",
    "reference_import",
    "provider_invocation",
    "direct_network_access",
    "credential_access",
    "secret_read",
]

UNSAFE_PATCH_RISK_FLAG_NAMES = (
    "ready_for_execution",
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
    "ready_for_persistent_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class PatchRiskScannerMode(StrEnum):
    DIFF_ENVELOPE_SCAN = "diff_envelope_scan"
    UNIFIED_DIFF_SCAN = "unified_diff_scan"
    STRUCTURED_PATCH_SCAN = "structured_patch_scan"
    COMBINED_DIFF_AND_STRUCTURED_SCAN = "combined_diff_and_structured_scan"
    METADATA_ONLY_SCAN = "metadata_only_scan"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchRiskSourceKind(StrEnum):
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    V0354_UNIFIED_DIFF_PROPOSAL = "v0354_unified_diff_proposal"
    V0354_STRUCTURED_PATCH_PROPOSAL = "v0354_structured_patch_proposal"
    V0354_PATCH_FILE_PROPOSAL = "v0354_patch_file_proposal"
    V0354_PATCH_HUNK_PROPOSAL = "v0354_patch_hunk_proposal"
    V0353_PATCH_PLAN = "v0353_patch_plan"
    V0353_CHANGE_SET_GRAPH = "v0353_change_set_graph"
    V0352_CONTEXT_SNAPSHOT = "v0352_context_snapshot"
    V0352_EVIDENCE_BUNDLE = "v0352_evidence_bundle"
    V0351_PATCH_INTENT_SCOPE_BUNDLE = "v0351_patch_intent_scope_bundle"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    REFERENCE_REJECTION_RECORD = "reference_rejection_record"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchRiskScannerStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    SCAN_INPUT_CREATED = "scan_input_created"
    SCAN_COMPLETED = "scan_completed"
    SCAN_COMPLETED_WITH_WARNINGS = "scan_completed_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class PatchRiskReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    RISK_CONTRACT_READY = "risk_contract_ready"
    SCANNER_READY = "scanner_ready"
    RISK_REPORT_READY = "risk_report_ready"
    CONFORMANCE_REPORT_READY = "conformance_report_ready"
    DESIGN_HANDOFF_READY_FOR_V0356 = "design_handoff_ready_for_v0356"
    DESIGN_HANDOFF_READY_FOR_V0357 = "design_handoff_ready_for_v0357"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchRiskDecisionKind(StrEnum):
    ACCEPTABLE_FOR_REVIEW = "acceptable_for_review"
    REVIEW_REQUIRED = "review_required"
    BLOCK_PROPOSAL = "block_proposal"
    BLOCK_UNSAFE_SURFACE = "block_unsafe_surface"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    NO_OP = "no_op"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNKNOWN = "unknown"


class PatchRiskSeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class PatchRiskSignalKind(StrEnum):
    SCOPE_ESCAPE_SIGNAL = "scope_escape_signal"
    SECRET_EXPOSURE_SIGNAL = "secret_exposure_signal"
    CREDENTIAL_EXPOSURE_SIGNAL = "credential_exposure_signal"
    TOKEN_EXPOSURE_SIGNAL = "token_exposure_signal"
    UNSAFE_READINESS_TRUE_SIGNAL = "unsafe_readiness_true_signal"
    PROVIDER_INVOCATION_OPENING_SIGNAL = "provider_invocation_opening_signal"
    NETWORK_ACCESS_OPENING_SIGNAL = "network_access_opening_signal"
    CREDENTIAL_ACCESS_OPENING_SIGNAL = "credential_access_opening_signal"
    SHELL_EXECUTION_SIGNAL = "shell_execution_signal"
    SUBPROCESS_EXECUTION_SIGNAL = "subprocess_execution_signal"
    COMMAND_EXECUTION_SIGNAL = "command_execution_signal"
    WORKSPACE_WRITE_SIGNAL = "workspace_write_signal"
    CODE_EDIT_SIGNAL = "code_edit_signal"
    PATCH_APPLY_SIGNAL = "patch_apply_signal"
    APPLY_PATCH_SIGNAL = "apply_patch_signal"
    GIT_APPLY_SIGNAL = "git_apply_signal"
    DEPENDENCY_INSTALL_SIGNAL = "dependency_install_signal"
    TEST_EXECUTION_SIGNAL = "test_execution_signal"
    REFERENCE_EXECUTION_SIGNAL = "reference_execution_signal"
    REFERENCE_IMPORT_SIGNAL = "reference_import_signal"
    RAW_SOURCE_DUMP_SIGNAL = "raw_source_dump_signal"
    COPIED_REFERENCE_CODE_SIGNAL = "copied_reference_code_signal"
    LICENSE_OR_ATTRIBUTION_SIGNAL = "license_or_attribution_signal"
    SAFETY_DOC_DELETION_SIGNAL = "safety_doc_deletion_signal"
    TEST_DELETION_SIGNAL = "test_deletion_signal"
    AUTHORITY_GRANT_SIGNAL = "authority_grant_signal"
    NO_RISK_SIGNAL = "no_risk_signal"
    UNKNOWN = "unknown"


class PatchConformanceRuleKind(StrEnum):
    NO_APPLY_RULE = "no_apply_rule"
    NO_WRITE_RULE = "no_write_rule"
    NO_CODE_EDIT_RULE = "no_code_edit_rule"
    NO_SHELL_RULE = "no_shell_rule"
    NO_TEST_EXECUTION_RULE = "no_test_execution_rule"
    NO_DEPENDENCY_INSTALL_RULE = "no_dependency_install_rule"
    NO_REFERENCE_EXECUTION_RULE = "no_reference_execution_rule"
    NO_PROVIDER_NETWORK_OPENING_RULE = "no_provider_network_opening_rule"
    NO_CREDENTIAL_SECRET_RULE = "no_credential_secret_rule"
    SCOPE_ALIGNMENT_RULE = "scope_alignment_rule"
    INTENT_ALIGNMENT_RULE = "intent_alignment_rule"
    CONTEXT_ALIGNMENT_RULE = "context_alignment_rule"
    PLAN_ALIGNMENT_RULE = "plan_alignment_rule"
    DIFF_SHAPE_RULE = "diff_shape_rule"
    BOUNDED_ARTIFACT_RULE = "bounded_artifact_rule"
    REVIEW_REQUIRED_RULE = "review_required_rule"
    UNKNOWN = "unknown"


class PatchConformanceFindingKind(StrEnum):
    CONFORMANT = "conformant"
    WARNING = "warning"
    VIOLATION = "violation"
    BLOCKING_VIOLATION = "blocking_violation"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    SKIPPED = "skipped"
    UNKNOWN = "unknown"


class PatchSafetyRegressionKind(StrEnum):
    UNSAFE_READINESS_FLAG_REGRESSION = "unsafe_readiness_flag_regression"
    PROVIDER_NETWORK_BOUNDARY_REGRESSION = "provider_network_boundary_regression"
    CREDENTIAL_BOUNDARY_REGRESSION = "credential_boundary_regression"
    SHELL_COMMAND_BOUNDARY_REGRESSION = "shell_command_boundary_regression"
    WORKSPACE_WRITE_BOUNDARY_REGRESSION = "workspace_write_boundary_regression"
    PATCH_APPLY_BOUNDARY_REGRESSION = "patch_apply_boundary_regression"
    REFERENCE_EXECUTION_BOUNDARY_REGRESSION = "reference_execution_boundary_regression"
    TEST_EXECUTION_BOUNDARY_REGRESSION = "test_execution_boundary_regression"
    DEPENDENCY_INSTALL_BOUNDARY_REGRESSION = "dependency_install_boundary_regression"
    TRACE_PERSISTENCE_BOUNDARY_REGRESSION = "trace_persistence_boundary_regression"
    UI_RUNTIME_BOUNDARY_REGRESSION = "ui_runtime_boundary_regression"
    AUTHORITY_GRANT_BOUNDARY_REGRESSION = "authority_grant_boundary_regression"
    SAFETY_DOCUMENTATION_REGRESSION = "safety_documentation_regression"
    UNKNOWN = "unknown"


class PatchScopeViolationKind(StrEnum):
    OUTSIDE_ALLOWED_ROOT = "outside_allowed_root"
    BLOCKED_PATH_PATTERN = "blocked_path_pattern"
    BLOCKED_TARGET_KIND = "blocked_target_kind"
    SECRET_LIKE_TARGET = "secret_like_target"
    CREDENTIAL_LIKE_TARGET = "credential_like_target"
    BINARY_TARGET = "binary_target"
    REFERENCE_EXECUTION_TARGET = "reference_execution_target"
    EXTERNAL_PATH_TARGET = "external_path_target"
    TOO_MANY_TARGETS = "too_many_targets"
    AMBIGUOUS_TARGET = "ambiguous_target"
    UNKNOWN = "unknown"


DANGEROUS_SIGNALS = {
    PatchRiskSignalKind.SECRET_EXPOSURE_SIGNAL,
    PatchRiskSignalKind.CREDENTIAL_EXPOSURE_SIGNAL,
    PatchRiskSignalKind.TOKEN_EXPOSURE_SIGNAL,
    PatchRiskSignalKind.UNSAFE_READINESS_TRUE_SIGNAL,
    PatchRiskSignalKind.PROVIDER_INVOCATION_OPENING_SIGNAL,
    PatchRiskSignalKind.NETWORK_ACCESS_OPENING_SIGNAL,
    PatchRiskSignalKind.CREDENTIAL_ACCESS_OPENING_SIGNAL,
    PatchRiskSignalKind.SHELL_EXECUTION_SIGNAL,
    PatchRiskSignalKind.SUBPROCESS_EXECUTION_SIGNAL,
    PatchRiskSignalKind.COMMAND_EXECUTION_SIGNAL,
    PatchRiskSignalKind.WORKSPACE_WRITE_SIGNAL,
    PatchRiskSignalKind.CODE_EDIT_SIGNAL,
    PatchRiskSignalKind.PATCH_APPLY_SIGNAL,
    PatchRiskSignalKind.APPLY_PATCH_SIGNAL,
    PatchRiskSignalKind.GIT_APPLY_SIGNAL,
    PatchRiskSignalKind.DEPENDENCY_INSTALL_SIGNAL,
    PatchRiskSignalKind.TEST_EXECUTION_SIGNAL,
    PatchRiskSignalKind.REFERENCE_EXECUTION_SIGNAL,
    PatchRiskSignalKind.REFERENCE_IMPORT_SIGNAL,
    PatchRiskSignalKind.AUTHORITY_GRANT_SIGNAL,
}


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0355_VERSION not in value:
        raise ValueError("version must include v0.35.5")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    for key in metadata:
        if any(token in str(key).lower() for token in ("secret", "credential", "api_key", "token")):
            raise ValueError("metadata keys must not request credential or secret material")


def _validate_list(name: str, values: list[Any]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be a list")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    _validate_list(name, values)
    for value in values:
        enum_type(value)


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.5")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _bounded(value: str, limit: int = DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS, marker: str = "\n[truncated by v0.35.5 scanner boundary]") -> tuple[str, bool]:
    if limit < 0:
        raise ValueError("limit must be >= 0")
    if len(value) <= limit:
        return value, False
    if limit <= len(marker):
        return value[:limit], True
    return value[: limit - len(marker)] + marker, True


def _proposal_text(envelope: DiffProposalEnvelope | None = None, unified_diff: UnifiedDiffProposal | None = None, structured_patch: StructuredPatchProposal | None = None, max_chars: int = DEFAULT_MAX_DIFF_SCAN_CHARS) -> str:
    chunks: list[str] = []
    if envelope is not None:
        chunks.extend([envelope.summary, " ".join(envelope.gaps), " ".join(str(item) for item in envelope.risk_kinds)])
        unified_diff = unified_diff or envelope.unified_diff
        structured_patch = structured_patch or envelope.structured_patch
    if unified_diff is not None:
        chunks.append(unified_diff.diff_text)
    if structured_patch is not None:
        chunks.extend([structured_patch.proposal_summary, structured_patch.proposal_rationale])
        for file_proposal in structured_patch.file_proposals:
            chunks.append(file_proposal.target_file.target_path_ref)
            chunks.append(file_proposal.file_proposal_summary)
            chunks.append(file_proposal.proposed_file_diff_preview)
            for hunk in file_proposal.hunk_proposals:
                chunks.extend([hunk.before_preview, hunk.after_preview, hunk.proposed_hunk_text])
    return _bounded("\n".join(chunks), max_chars)[0]


@dataclass(frozen=True)
class PatchRiskFlagSet:
    flag_set_id: str
    version: str
    patch_risk_scanner_constructed: bool
    patch_conformance_scanner_constructed: bool
    patch_safety_regression_scanner_constructed: bool
    patch_scope_violation_scanner_constructed: bool
    patch_risk_report_available: bool
    ready_for_v0356_human_review_packet: bool
    ready_for_v0357_patch_proposal_ocel_trace_packet: bool
    ready_for_patch_risk_scan: bool
    ready_for_patch_conformance_scan: bool
    ready_for_patch_safety_regression_scan: bool
    ready_for_patch_scope_violation_scan: bool
    ready_for_patch_review_packet_input: bool
    ready_for_execution: bool = False
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
    ready_for_persistent_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_PATCH_RISK_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskSourceRef:
    source_ref_id: str
    source_kind: PatchRiskSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PatchRiskSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskScannerPolicy:
    scanner_policy_id: str
    version: str
    scanner_mode: PatchRiskScannerMode | str
    enabled_signal_kinds: list[PatchRiskSignalKind | str]
    mandatory_conformance_rules: list[PatchConformanceRuleKind | str]
    blocked_signal_kinds: list[PatchRiskSignalKind | str]
    review_required_signal_kinds: list[PatchRiskSignalKind | str]
    max_diff_chars_to_scan: int
    max_findings: int
    allow_acceptable_for_review: bool
    allow_approved_for_apply: bool = False
    allow_patch_apply: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_reference_execution: bool = False
    allow_provider_invocation: bool = False
    allow_network_access: bool = False
    allow_credential_access: bool = False
    allow_secret_read: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scanner_policy_id", self.scanner_policy_id)
        _validate_version(self.version)
        PatchRiskScannerMode(self.scanner_mode)
        _validate_enum_list("enabled_signal_kinds", self.enabled_signal_kinds, PatchRiskSignalKind)
        _validate_enum_list("mandatory_conformance_rules", self.mandatory_conformance_rules, PatchConformanceRuleKind)
        _validate_enum_list("blocked_signal_kinds", self.blocked_signal_kinds, PatchRiskSignalKind)
        _validate_enum_list("review_required_signal_kinds", self.review_required_signal_kinds, PatchRiskSignalKind)
        _validate_non_negative("max_diff_chars_to_scan", self.max_diff_chars_to_scan)
        _validate_non_negative("max_findings", self.max_findings)
        for name in ("allow_approved_for_apply", "allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_shell", "allow_dependency_install", "allow_reference_execution", "allow_provider_invocation", "allow_network_access", "allow_credential_access", "allow_secret_read"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.5")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskScanInput:
    scan_input_id: str
    version: str
    diff_envelope_id: str | None
    unified_diff_id: str | None
    structured_patch_id: str | None
    patch_plan_id: str | None
    context_snapshot_id: str | None
    intent_scope_bundle_id: str | None
    requested_mode: PatchRiskScannerMode | str
    task_summary: str
    source_refs: list[PatchRiskSourceRef]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scan_input_id", self.scan_input_id)
        _validate_version(self.version)
        for name in ("diff_envelope_id", "unified_diff_id", "structured_patch_id", "patch_plan_id", "context_snapshot_id", "intent_scope_bundle_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        PatchRiskScannerMode(self.requested_mode)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"patch_application", "workspace_write", "code_edit", "shell_execution", "test_execution", "dependency_install", "reference_execution", "provider_invocation", "direct_network_access", "credential_access"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include unsafe runtime actions")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskSignal:
    risk_signal_id: str
    signal_kind: PatchRiskSignalKind | str
    severity: PatchRiskSeverity | str
    source_ref_id: str | None
    finding_summary: str
    evidence_preview: str
    recommendation: str
    blocked: bool
    requires_review: bool
    future_gated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        signal_kind = PatchRiskSignalKind(self.signal_kind)
        PatchRiskSeverity(self.severity)
        if self.source_ref_id is not None:
            _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("finding_summary", self.finding_summary)
        if len(self.evidence_preview) > DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS:
            raise ValueError("evidence_preview must be bounded")
        _require_non_blank("recommendation", self.recommendation)
        if signal_kind in DANGEROUS_SIGNALS and not (self.blocked or self.requires_review):
            raise ValueError("dangerous risk signals must block or require review")
        if signal_kind in DANGEROUS_SIGNALS and PatchRiskSeverity(self.severity) not in {PatchRiskSeverity.HIGH, PatchRiskSeverity.CRITICAL, PatchRiskSeverity.BLOCKED}:
            raise ValueError("dangerous risk signals must be high, critical, or blocked severity")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchConformanceRule:
    conformance_rule_id: str
    rule_kind: PatchConformanceRuleKind | str
    rule_summary: str
    mandatory: bool
    blocked_if_violated: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("conformance_rule_id", self.conformance_rule_id)
        rule_kind = PatchConformanceRuleKind(self.rule_kind)
        _require_non_blank("rule_summary", self.rule_summary)
        if rule_kind in {PatchConformanceRuleKind.NO_APPLY_RULE, PatchConformanceRuleKind.NO_WRITE_RULE, PatchConformanceRuleKind.NO_SHELL_RULE} and not (self.mandatory and self.blocked_if_violated):
            raise ValueError("mandatory no-apply/no-write/no-shell rules must block if violated")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchConformanceFinding:
    finding_id: str
    rule_id: str | None
    rule_kind: PatchConformanceRuleKind | str
    finding_kind: PatchConformanceFindingKind | str
    severity: PatchRiskSeverity | str
    finding_summary: str
    evidence_preview: str
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        if self.rule_id is not None:
            _require_non_blank("rule_id", self.rule_id)
        PatchConformanceRuleKind(self.rule_kind)
        finding_kind = PatchConformanceFindingKind(self.finding_kind)
        PatchRiskSeverity(self.severity)
        _require_non_blank("finding_summary", self.finding_summary)
        if len(self.evidence_preview) > DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS:
            raise ValueError("evidence_preview must be bounded")
        if finding_kind == PatchConformanceFindingKind.BLOCKING_VIOLATION and self.blocked is not True:
            raise ValueError("blocking violations must set blocked True")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchSafetyRegressionSignal:
    regression_signal_id: str
    regression_kind: PatchSafetyRegressionKind | str
    severity: PatchRiskSeverity | str
    affected_boundary: str
    finding_summary: str
    evidence_preview: str
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("regression_signal_id", self.regression_signal_id)
        regression_kind = PatchSafetyRegressionKind(self.regression_kind)
        PatchRiskSeverity(self.severity)
        _require_non_blank("affected_boundary", self.affected_boundary)
        _require_non_blank("finding_summary", self.finding_summary)
        if len(self.evidence_preview) > DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS:
            raise ValueError("evidence_preview must be bounded")
        if regression_kind != PatchSafetyRegressionKind.UNKNOWN and not (self.blocked or self.requires_review):
            raise ValueError("unsafe regressions must block or require review")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchSafetyRegressionReport:
    safety_regression_report_id: str
    version: str
    scan_input_id: str
    regression_signals: list[PatchSafetyRegressionSignal]
    unsafe_readiness_flag_count: int
    boundary_regression_count: int
    blocked: bool
    requires_review: bool
    summary: str
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_regression_report_id", "scan_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("regression_signals", self.regression_signals)
        _validate_non_negative("unsafe_readiness_flag_count", self.unsafe_readiness_flag_count)
        _validate_non_negative("boundary_regression_count", self.boundary_regression_count)
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchScopeViolation:
    scope_violation_id: str
    violation_kind: PatchScopeViolationKind | str
    target_path_ref: str | None
    severity: PatchRiskSeverity | str
    finding_summary: str
    evidence_preview: str
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scope_violation_id", self.scope_violation_id)
        violation_kind = PatchScopeViolationKind(self.violation_kind)
        if self.target_path_ref is not None:
            _require_non_blank("target_path_ref", self.target_path_ref)
        PatchRiskSeverity(self.severity)
        _require_non_blank("finding_summary", self.finding_summary)
        if len(self.evidence_preview) > DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS:
            raise ValueError("evidence_preview must be bounded")
        if violation_kind != PatchScopeViolationKind.UNKNOWN and not (self.blocked or self.requires_review):
            raise ValueError("scope violations should block or require review")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchScopeViolationReport:
    scope_violation_report_id: str
    version: str
    scan_input_id: str
    scope_violations: list[PatchScopeViolation]
    violation_count: int
    blocked: bool
    requires_review: bool
    summary: str
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_violation_report_id", "scan_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("scope_violations", self.scope_violations)
        _validate_non_negative("violation_count", self.violation_count)
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchDiffRiskSummary:
    diff_risk_summary_id: str
    version: str
    diff_envelope_id: str | None
    unified_diff_id: str | None
    structured_patch_id: str | None
    risk_signals: list[PatchRiskSignal]
    conformance_findings: list[PatchConformanceFinding]
    risk_count: int
    blocking_risk_count: int
    review_required_count: int
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("diff_risk_summary_id", self.diff_risk_summary_id)
        _validate_version(self.version)
        for name in ("diff_envelope_id", "unified_diff_id", "structured_patch_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        _validate_list("risk_signals", self.risk_signals)
        _validate_list("conformance_findings", self.conformance_findings)
        for name in ("risk_count", "blocking_risk_count", "review_required_count"):
            _validate_non_negative(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalRiskReport:
    proposal_risk_report_id: str
    version: str
    scan_input_id: str
    diff_risk_summary: PatchDiffRiskSummary
    safety_regression_report: PatchSafetyRegressionReport
    scope_violation_report: PatchScopeViolationReport
    overall_decision: PatchRiskDecisionKind | str
    overall_severity: PatchRiskSeverity | str
    blocked: bool
    requires_review: bool
    acceptable_for_review: bool
    approved_for_apply: bool
    summary: str
    ready_for_v0356_human_review_packet: bool
    ready_for_v0357_patch_proposal_ocel_trace_packet: bool
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("proposal_risk_report_id", "scan_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchRiskDecisionKind(self.overall_decision)
        PatchRiskSeverity(self.overall_severity)
        if self.approved_for_apply is not False:
            raise ValueError("approved_for_apply must always be False")
        _validate_false(self, ("ready_for_patch_application", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskScanDecision:
    decision_id: str
    scan_input_id: str
    decision_kind: PatchRiskDecisionKind | str
    severity: PatchRiskSeverity | str
    reason: str
    blocked: bool
    requires_review: bool
    acceptable_for_review: bool
    approved_for_apply: bool = False
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("scan_input_id", self.scan_input_id)
        PatchRiskDecisionKind(self.decision_kind)
        PatchRiskSeverity(self.severity)
        _require_non_blank("reason", self.reason)
        if self.approved_for_apply is not False:
            raise ValueError("approved_for_apply must always be False")
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskValidationFinding:
    finding_id: str
    decision_kind: PatchRiskDecisionKind | str
    severity: PatchRiskSeverity | str
    finding_summary: str
    evidence_preview: str
    blocks_validation: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        PatchRiskDecisionKind(self.decision_kind)
        PatchRiskSeverity(self.severity)
        _require_non_blank("finding_summary", self.finding_summary)
        if len(self.evidence_preview) > DEFAULT_MAX_EVIDENCE_PREVIEW_CHARS:
            raise ValueError("evidence_preview must be bounded")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskValidationReport:
    validation_report_id: str
    version: str
    proposal_risk_report_id: str | None
    findings: list[PatchRiskValidationFinding]
    valid: bool
    summary: str
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        if self.proposal_risk_report_id is not None:
            _require_non_blank("proposal_risk_report_id", self.proposal_risk_report_id)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskScanReport:
    scan_report_id: str
    version: str
    scan_input_id: str
    proposal_risk_report_id: str
    summary: str
    risk_scan_ready: bool
    conformance_scan_ready: bool
    safety_regression_scan_ready: bool
    scope_violation_scan_ready: bool
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scan_report_id", "scan_input_id", "proposal_risk_report_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchRiskRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_patch_approval_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_apply_patch_runtime_call_guarantee: bool = True
    no_git_apply_runtime_call_guarantee: bool = True
    no_test_execution_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_reference_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
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
class PatchRiskNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_patch_approval: bool = True
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_test_execution: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
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
class V0355ReadinessReport:
    report_id: str
    version: str
    proposal_risk_report_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0356_human_review_packet: bool = True
    ready_for_v0357_patch_proposal_ocel_trace_packet: bool = True
    ready_for_patch_risk_scan: bool = True
    ready_for_patch_conformance_scan: bool = True
    ready_for_patch_safety_regression_scan: bool = True
    ready_for_patch_scope_violation_scan: bool = True
    ready_for_patch_review_packet_input: bool = True
    ready_for_execution: bool = False
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
        if self.proposal_risk_report_id is not None:
            _require_non_blank("proposal_risk_report_id", self.proposal_risk_report_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_PATCH_RISK_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_patch_risk_flags(flag_set_id: str = "patch_risk_flags:v0.35.5", **kwargs: Any) -> PatchRiskFlagSet:
    return PatchRiskFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0355_VERSION),
        patch_risk_scanner_constructed=kwargs.pop("patch_risk_scanner_constructed", True),
        patch_conformance_scanner_constructed=kwargs.pop("patch_conformance_scanner_constructed", True),
        patch_safety_regression_scanner_constructed=kwargs.pop("patch_safety_regression_scanner_constructed", True),
        patch_scope_violation_scanner_constructed=kwargs.pop("patch_scope_violation_scanner_constructed", True),
        patch_risk_report_available=kwargs.pop("patch_risk_report_available", True),
        ready_for_v0356_human_review_packet=kwargs.pop("ready_for_v0356_human_review_packet", True),
        ready_for_v0357_patch_proposal_ocel_trace_packet=kwargs.pop("ready_for_v0357_patch_proposal_ocel_trace_packet", True),
        ready_for_patch_risk_scan=kwargs.pop("ready_for_patch_risk_scan", True),
        ready_for_patch_conformance_scan=kwargs.pop("ready_for_patch_conformance_scan", True),
        ready_for_patch_safety_regression_scan=kwargs.pop("ready_for_patch_safety_regression_scan", True),
        ready_for_patch_scope_violation_scan=kwargs.pop("ready_for_patch_scope_violation_scan", True),
        ready_for_patch_review_packet_input=kwargs.pop("ready_for_patch_review_packet_input", True),
        **kwargs,
    )


def build_patch_risk_source_ref(source_ref_id: str = "patch_risk_source:v0.35.5", **kwargs: Any) -> PatchRiskSourceRef:
    return PatchRiskSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchRiskSourceKind.V0354_DIFF_PROPOSAL_ENVELOPE),
        source_id=kwargs.pop("source_id", "diff_envelope:v0.35.4"),
        source_summary=kwargs.pop("source_summary", "Supplied v0.35.4 diff proposal envelope metadata."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0354_DIFF_DOC_REF]),
        **kwargs,
    )


def build_patch_risk_scanner_policy(scanner_policy_id: str = "patch_risk_policy:v0.35.5", **kwargs: Any) -> PatchRiskScannerPolicy:
    return PatchRiskScannerPolicy(
        scanner_policy_id=scanner_policy_id,
        version=kwargs.pop("version", V0355_VERSION),
        scanner_mode=kwargs.pop("scanner_mode", PatchRiskScannerMode.COMBINED_DIFF_AND_STRUCTURED_SCAN),
        enabled_signal_kinds=kwargs.pop("enabled_signal_kinds", [item for item in PatchRiskSignalKind if item != PatchRiskSignalKind.UNKNOWN]),
        mandatory_conformance_rules=kwargs.pop("mandatory_conformance_rules", [PatchConformanceRuleKind.NO_APPLY_RULE, PatchConformanceRuleKind.NO_WRITE_RULE, PatchConformanceRuleKind.NO_SHELL_RULE, PatchConformanceRuleKind.NO_TEST_EXECUTION_RULE, PatchConformanceRuleKind.NO_DEPENDENCY_INSTALL_RULE, PatchConformanceRuleKind.NO_REFERENCE_EXECUTION_RULE, PatchConformanceRuleKind.NO_PROVIDER_NETWORK_OPENING_RULE, PatchConformanceRuleKind.NO_CREDENTIAL_SECRET_RULE, PatchConformanceRuleKind.BOUNDED_ARTIFACT_RULE]),
        blocked_signal_kinds=kwargs.pop("blocked_signal_kinds", list(DANGEROUS_SIGNALS)),
        review_required_signal_kinds=kwargs.pop("review_required_signal_kinds", [PatchRiskSignalKind.SCOPE_ESCAPE_SIGNAL, PatchRiskSignalKind.RAW_SOURCE_DUMP_SIGNAL, PatchRiskSignalKind.COPIED_REFERENCE_CODE_SIGNAL, PatchRiskSignalKind.LICENSE_OR_ATTRIBUTION_SIGNAL, PatchRiskSignalKind.SAFETY_DOC_DELETION_SIGNAL, PatchRiskSignalKind.TEST_DELETION_SIGNAL]),
        max_diff_chars_to_scan=kwargs.pop("max_diff_chars_to_scan", DEFAULT_MAX_DIFF_SCAN_CHARS),
        max_findings=kwargs.pop("max_findings", 40),
        allow_acceptable_for_review=kwargs.pop("allow_acceptable_for_review", True),
        **kwargs,
    )


def default_patch_risk_scanner_policy() -> PatchRiskScannerPolicy:
    return build_patch_risk_scanner_policy()


def build_patch_risk_scan_input(scan_input_id: str = "patch_risk_scan_input:v0.35.5", **kwargs: Any) -> PatchRiskScanInput:
    return PatchRiskScanInput(
        scan_input_id=scan_input_id,
        version=kwargs.pop("version", V0355_VERSION),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        unified_diff_id=kwargs.pop("unified_diff_id", "unified_diff:v0.35.4"),
        structured_patch_id=kwargs.pop("structured_patch_id", "structured_patch:v0.35.4"),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        intent_scope_bundle_id=kwargs.pop("intent_scope_bundle_id", "intent_scope_bundle:v0.35.1"),
        requested_mode=kwargs.pop("requested_mode", PatchRiskScannerMode.COMBINED_DIFF_AND_STRUCTURED_SCAN),
        task_summary=kwargs.pop("task_summary", "Scan bounded diff proposal artifacts as metadata only."),
        source_refs=kwargs.pop("source_refs", [build_patch_risk_source_ref()]),
        **kwargs,
    )


def build_patch_risk_scan_input_from_diff_envelope(envelope: DiffProposalEnvelope | None = None, **kwargs: Any) -> PatchRiskScanInput:
    if envelope is None:
        return build_patch_risk_scan_input(
            diff_envelope_id=None,
            unified_diff_id=None,
            structured_patch_id=None,
            requested_mode=PatchRiskScannerMode.REVIEW_REQUIRED,
            task_summary="Risk scan input is review-required because diff proposal metadata is missing.",
            metadata={"gap": "missing_diff_envelope"},
            **kwargs,
        )
    return build_patch_risk_scan_input(
        diff_envelope_id=envelope.diff_envelope_id,
        unified_diff_id=getattr(envelope.unified_diff, "unified_diff_id", None),
        structured_patch_id=getattr(envelope.structured_patch, "structured_patch_id", None),
        source_refs=[build_patch_risk_source_ref(source_id=envelope.diff_envelope_id)],
        **kwargs,
    )


def build_patch_risk_signal(risk_signal_id: str = "patch_risk_signal:v0.35.5:ok", **kwargs: Any) -> PatchRiskSignal:
    return PatchRiskSignal(
        risk_signal_id=risk_signal_id,
        signal_kind=kwargs.pop("signal_kind", PatchRiskSignalKind.NO_RISK_SIGNAL),
        severity=kwargs.pop("severity", PatchRiskSeverity.INFO),
        source_ref_id=kwargs.pop("source_ref_id", "patch_risk_source:v0.35.5"),
        finding_summary=kwargs.pop("finding_summary", "No blocking patch risk signal detected."),
        evidence_preview=kwargs.pop("evidence_preview", "metadata-only scan"),
        recommendation=kwargs.pop("recommendation", "Proceed only to human review packet input, not apply."),
        blocked=kwargs.pop("blocked", False),
        requires_review=kwargs.pop("requires_review", False),
        future_gated=kwargs.pop("future_gated", False),
        **kwargs,
    )


def build_patch_conformance_rule(conformance_rule_id: str = "conformance_rule:v0.35.5:no_apply", **kwargs: Any) -> PatchConformanceRule:
    return PatchConformanceRule(
        conformance_rule_id=conformance_rule_id,
        rule_kind=kwargs.pop("rule_kind", PatchConformanceRuleKind.NO_APPLY_RULE),
        rule_summary=kwargs.pop("rule_summary", "Diff proposal must not apply patches."),
        mandatory=kwargs.pop("mandatory", True),
        blocked_if_violated=kwargs.pop("blocked_if_violated", True),
        **kwargs,
    )


def build_patch_conformance_finding(finding_id: str = "conformance_finding:v0.35.5:ok", **kwargs: Any) -> PatchConformanceFinding:
    return PatchConformanceFinding(
        finding_id=finding_id,
        rule_id=kwargs.pop("rule_id", "conformance_rule:v0.35.5:no_apply"),
        rule_kind=kwargs.pop("rule_kind", PatchConformanceRuleKind.NO_APPLY_RULE),
        finding_kind=kwargs.pop("finding_kind", PatchConformanceFindingKind.CONFORMANT),
        severity=kwargs.pop("severity", PatchRiskSeverity.INFO),
        finding_summary=kwargs.pop("finding_summary", "No apply behavior is present in the proposal artifact."),
        evidence_preview=kwargs.pop("evidence_preview", "bounded artifact metadata"),
        blocked=kwargs.pop("blocked", False),
        requires_review=kwargs.pop("requires_review", False),
        **kwargs,
    )


def build_patch_safety_regression_signal(regression_signal_id: str = "safety_regression:v0.35.5", **kwargs: Any) -> PatchSafetyRegressionSignal:
    return PatchSafetyRegressionSignal(
        regression_signal_id=regression_signal_id,
        regression_kind=kwargs.pop("regression_kind", PatchSafetyRegressionKind.UNSAFE_READINESS_FLAG_REGRESSION),
        severity=kwargs.pop("severity", PatchRiskSeverity.HIGH),
        affected_boundary=kwargs.pop("affected_boundary", "Controlled Patch Proposal Layer"),
        finding_summary=kwargs.pop("finding_summary", "Unsafe readiness regression detected."),
        evidence_preview=kwargs.pop("evidence_preview", "ready_for_execution=True"),
        blocked=kwargs.pop("blocked", True),
        requires_review=kwargs.pop("requires_review", True),
        **kwargs,
    )


def build_patch_safety_regression_report(safety_regression_report_id: str = "safety_regression_report:v0.35.5", **kwargs: Any) -> PatchSafetyRegressionReport:
    signals = kwargs.pop("regression_signals", [])
    return PatchSafetyRegressionReport(
        safety_regression_report_id=safety_regression_report_id,
        version=kwargs.pop("version", V0355_VERSION),
        scan_input_id=kwargs.pop("scan_input_id", "patch_risk_scan_input:v0.35.5"),
        regression_signals=signals,
        unsafe_readiness_flag_count=kwargs.pop("unsafe_readiness_flag_count", sum(1 for item in signals if item.regression_kind == PatchSafetyRegressionKind.UNSAFE_READINESS_FLAG_REGRESSION)),
        boundary_regression_count=kwargs.pop("boundary_regression_count", len(signals)),
        blocked=kwargs.pop("blocked", any(item.blocked for item in signals)),
        requires_review=kwargs.pop("requires_review", any(item.requires_review for item in signals)),
        summary=kwargs.pop("summary", "Safety regression report is metadata only and does not remediate or execute."),
        **kwargs,
    )


def build_patch_scope_violation(scope_violation_id: str = "scope_violation:v0.35.5", **kwargs: Any) -> PatchScopeViolation:
    return PatchScopeViolation(
        scope_violation_id=scope_violation_id,
        violation_kind=kwargs.pop("violation_kind", PatchScopeViolationKind.BLOCKED_TARGET_KIND),
        target_path_ref=kwargs.pop("target_path_ref", "references/OpenCode/run.sh"),
        severity=kwargs.pop("severity", PatchRiskSeverity.HIGH),
        finding_summary=kwargs.pop("finding_summary", "Target violates patch proposal scope boundary."),
        evidence_preview=kwargs.pop("evidence_preview", "blocked target metadata"),
        blocked=kwargs.pop("blocked", True),
        requires_review=kwargs.pop("requires_review", True),
        **kwargs,
    )


def build_patch_scope_violation_report(scope_violation_report_id: str = "scope_violation_report:v0.35.5", **kwargs: Any) -> PatchScopeViolationReport:
    violations = kwargs.pop("scope_violations", [])
    return PatchScopeViolationReport(
        scope_violation_report_id=scope_violation_report_id,
        version=kwargs.pop("version", V0355_VERSION),
        scan_input_id=kwargs.pop("scan_input_id", "patch_risk_scan_input:v0.35.5"),
        scope_violations=violations,
        violation_count=kwargs.pop("violation_count", len(violations)),
        blocked=kwargs.pop("blocked", any(item.blocked for item in violations)),
        requires_review=kwargs.pop("requires_review", any(item.requires_review for item in violations)),
        summary=kwargs.pop("summary", "Scope violation report is metadata only and does not grant file access."),
        **kwargs,
    )


def build_patch_diff_risk_summary(diff_risk_summary_id: str = "diff_risk_summary:v0.35.5", **kwargs: Any) -> PatchDiffRiskSummary:
    signals = kwargs.pop("risk_signals", [])
    findings = kwargs.pop("conformance_findings", [])
    return PatchDiffRiskSummary(
        diff_risk_summary_id=diff_risk_summary_id,
        version=kwargs.pop("version", V0355_VERSION),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        unified_diff_id=kwargs.pop("unified_diff_id", "unified_diff:v0.35.4"),
        structured_patch_id=kwargs.pop("structured_patch_id", "structured_patch:v0.35.4"),
        risk_signals=signals,
        conformance_findings=findings,
        risk_count=kwargs.pop("risk_count", len([signal for signal in signals if signal.signal_kind != PatchRiskSignalKind.NO_RISK_SIGNAL])),
        blocking_risk_count=kwargs.pop("blocking_risk_count", sum(1 for signal in signals if signal.blocked)),
        review_required_count=kwargs.pop("review_required_count", sum(1 for signal in signals if signal.requires_review)),
        summary=kwargs.pop("summary", "Diff risk summary is review-input metadata, not approval."),
        **kwargs,
    )


def build_patch_proposal_risk_report(proposal_risk_report_id: str = "proposal_risk_report:v0.35.5", **kwargs: Any) -> PatchProposalRiskReport:
    diff_summary = kwargs.pop("diff_risk_summary", build_patch_diff_risk_summary(risk_signals=[build_patch_risk_signal()], conformance_findings=[build_patch_conformance_finding()]))
    safety_report = kwargs.pop("safety_regression_report", build_patch_safety_regression_report())
    scope_report = kwargs.pop("scope_violation_report", build_patch_scope_violation_report())
    blocked = kwargs.pop("blocked", diff_summary.blocking_risk_count > 0 or safety_report.blocked or scope_report.blocked)
    requires_review = kwargs.pop("requires_review", diff_summary.review_required_count > 0 or safety_report.requires_review or scope_report.requires_review)
    acceptable = kwargs.pop("acceptable_for_review", not blocked and not requires_review)
    return PatchProposalRiskReport(
        proposal_risk_report_id=proposal_risk_report_id,
        version=kwargs.pop("version", V0355_VERSION),
        scan_input_id=kwargs.pop("scan_input_id", "patch_risk_scan_input:v0.35.5"),
        diff_risk_summary=diff_summary,
        safety_regression_report=safety_report,
        scope_violation_report=scope_report,
        overall_decision=kwargs.pop("overall_decision", PatchRiskDecisionKind.BLOCK_PROPOSAL if blocked else (PatchRiskDecisionKind.REVIEW_REQUIRED if requires_review else PatchRiskDecisionKind.ACCEPTABLE_FOR_REVIEW)),
        overall_severity=kwargs.pop("overall_severity", PatchRiskSeverity.BLOCKED if blocked else (PatchRiskSeverity.MEDIUM if requires_review else PatchRiskSeverity.INFO)),
        blocked=blocked,
        requires_review=requires_review,
        acceptable_for_review=acceptable,
        approved_for_apply=kwargs.pop("approved_for_apply", False),
        summary=kwargs.pop("summary", "Patch proposal risk report is review input, not apply approval."),
        ready_for_v0356_human_review_packet=kwargs.pop("ready_for_v0356_human_review_packet", True),
        ready_for_v0357_patch_proposal_ocel_trace_packet=kwargs.pop("ready_for_v0357_patch_proposal_ocel_trace_packet", True),
        **kwargs,
    )


def build_patch_risk_scan_decision(decision_id: str = "patch_risk_decision:v0.35.5", **kwargs: Any) -> PatchRiskScanDecision:
    return PatchRiskScanDecision(
        decision_id=decision_id,
        scan_input_id=kwargs.pop("scan_input_id", "patch_risk_scan_input:v0.35.5"),
        decision_kind=kwargs.pop("decision_kind", PatchRiskDecisionKind.ACCEPTABLE_FOR_REVIEW),
        severity=kwargs.pop("severity", PatchRiskSeverity.INFO),
        reason=kwargs.pop("reason", "Acceptable for review only; not approved for apply."),
        blocked=kwargs.pop("blocked", False),
        requires_review=kwargs.pop("requires_review", False),
        acceptable_for_review=kwargs.pop("acceptable_for_review", True),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0355_DOC_PATH]),
        **kwargs,
    )


def build_patch_risk_validation_finding(finding_id: str = "patch_risk_validation:v0.35.5:ok", **kwargs: Any) -> PatchRiskValidationFinding:
    return PatchRiskValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchRiskDecisionKind.ACCEPTABLE_FOR_REVIEW),
        severity=kwargs.pop("severity", PatchRiskSeverity.INFO),
        finding_summary=kwargs.pop("finding_summary", "Risk report does not certify apply/write/execution."),
        evidence_preview=kwargs.pop("evidence_preview", "review-input metadata"),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_risk_validation_report(validation_report_id: str = "patch_risk_validation_report:v0.35.5", **kwargs: Any) -> PatchRiskValidationReport:
    findings = kwargs.pop("findings", [build_patch_risk_validation_finding()])
    return PatchRiskValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0355_VERSION),
        proposal_risk_report_id=kwargs.pop("proposal_risk_report_id", "proposal_risk_report:v0.35.5"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Risk validation does not certify approval, apply, write, or execution."),
        **kwargs,
    )


def build_patch_risk_scan_report(scan_report_id: str = "patch_risk_scan_report:v0.35.5", **kwargs: Any) -> PatchRiskScanReport:
    return PatchRiskScanReport(
        scan_report_id=scan_report_id,
        version=kwargs.pop("version", V0355_VERSION),
        scan_input_id=kwargs.pop("scan_input_id", "patch_risk_scan_input:v0.35.5"),
        proposal_risk_report_id=kwargs.pop("proposal_risk_report_id", "proposal_risk_report:v0.35.5"),
        summary=kwargs.pop("summary", "Risk scan report is ready for review packet input only."),
        risk_scan_ready=kwargs.pop("risk_scan_ready", True),
        conformance_scan_ready=kwargs.pop("conformance_scan_ready", True),
        safety_regression_scan_ready=kwargs.pop("safety_regression_scan_ready", True),
        scope_violation_scan_ready=kwargs.pop("scope_violation_scan_ready", True),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0355_DOC_PATH, DEFAULT_V0354_DIFF_DOC_REF]),
        **kwargs,
    )


def build_patch_risk_run_preview(run_preview_id: str = "patch_risk_run_preview:v0.35.5", **kwargs: Any) -> PatchRiskRunPreview:
    return PatchRiskRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["scan supplied diff artifact text", "classify risks", "build conformance findings", "build review-input risk report"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["PatchRiskSignal", "PatchConformanceFinding", "PatchProposalRiskReport"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["patch approval", "patch application", "workspace write", "code edit", "apply_patch", "git apply", "test execution", "shell execution"]),
        **kwargs,
    )


def build_patch_risk_no_apply_guarantee(guarantee_id: str = "patch_risk_no_apply:v0.35.5", **kwargs: Any) -> PatchRiskNoApplyGuarantee:
    return PatchRiskNoApplyGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0355_VERSION), **kwargs)


def build_v0355_readiness_report(report_id: str = "readiness:v0.35.5", **kwargs: Any) -> V0355ReadinessReport:
    return V0355ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0355_VERSION),
        proposal_risk_report_id=kwargs.pop("proposal_risk_report_id", "proposal_risk_report:v0.35.5"),
        summary=kwargs.pop("summary", "v0.35.5 is ready for v0.35.6/v0.35.7 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["PatchRiskSignal", "PatchConformanceFinding", "PatchSafetyRegressionReport", "PatchScopeViolationReport", "PatchProposalRiskReport"]),
        blocked_items=kwargs.pop("blocked_items", ["patch approval", "patch application", "workspace write", "code edit", "apply_patch", "git apply", "test execution", "shell execution"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.6 Human Review Packet", "v0.35.7 Patch Proposal OCEL Trace Packet"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0355_DOC_PATH, DEFAULT_V0354_DIFF_DOC_REF, DEFAULT_V0353_PLAN_DOC_REF, DEFAULT_V0352_CONTEXT_DOC_REF, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any approval/apply/write/edit/test/shell/reference execution path is introduced."]),
        **kwargs,
    )


def _signal_from_match(index: int, signal_kind: PatchRiskSignalKind, evidence: str, summary: str, policy: PatchRiskScannerPolicy) -> PatchRiskSignal:
    blocked = signal_kind in set(policy.blocked_signal_kinds)
    requires_review = blocked or signal_kind in set(policy.review_required_signal_kinds)
    severity = PatchRiskSeverity.BLOCKED if blocked else PatchRiskSeverity.HIGH if requires_review else PatchRiskSeverity.MEDIUM
    preview, _ = _bounded(evidence)
    return build_patch_risk_signal(
        risk_signal_id=f"patch_risk_signal:v0.35.5:{index}",
        signal_kind=signal_kind,
        severity=severity,
        finding_summary=summary,
        evidence_preview=preview,
        recommendation="Block or require review; do not approve or apply.",
        blocked=blocked,
        requires_review=requires_review,
    )


def scan_diff_proposal_risks(envelope: DiffProposalEnvelope | None = None, policy: PatchRiskScannerPolicy | None = None, unified_diff: UnifiedDiffProposal | None = None, structured_patch: StructuredPatchProposal | None = None) -> list[PatchRiskSignal]:
    policy = policy or default_patch_risk_scanner_policy()
    text = _proposal_text(envelope=envelope, unified_diff=unified_diff, structured_patch=structured_patch, max_chars=policy.max_diff_chars_to_scan)
    lowered = text.lower()
    compact = lowered.replace(" ", "")
    write_text_pattern = ".write" + "_text("
    write_bytes_pattern = ".write" + "_bytes("
    open_call_pattern = "open" + "("
    subprocess_attr_pattern = "sub" + "process."
    subprocess_import_pattern = "import " + "subprocess"
    os_system_pattern = "os." + "system"
    requests_pattern = "requests" + "."
    httpx_pattern = "httpx" + "."
    urllib_pattern = "urllib" + "."
    aiohttp_pattern = "aiohttp" + "."
    socket_pattern = "socket" + "."
    pattern_specs = [
        (PatchRiskSignalKind.UNSAFE_READINESS_TRUE_SIGNAL, ["ready_for_execution=true", "ready_for_patch_application=true", "ready_for_workspace_write=true", "ready_for_code_edit=true"], "Unsafe readiness flag appears true."),
        (PatchRiskSignalKind.WORKSPACE_WRITE_SIGNAL, ["path.write" + "_text", write_text_pattern, write_bytes_pattern, open_call_pattern, "\"w\"", "'w'", "remove-item", "set-content"], "Workspace write or file mutation pattern detected."),
        (PatchRiskSignalKind.CODE_EDIT_SIGNAL, ["code_edit", "edit_code_file"], "Code edit surface pattern detected."),
        (PatchRiskSignalKind.APPLY_PATCH_SIGNAL, ["apply_patch"], "apply_patch pattern detected."),
        (PatchRiskSignalKind.GIT_APPLY_SIGNAL, ["git apply"], "git apply pattern detected."),
        (PatchRiskSignalKind.PATCH_APPLY_SIGNAL, ["patch_application", "ready_for_apply=true", "approved_for_apply=true"], "Patch apply/approval pattern detected."),
        (PatchRiskSignalKind.SUBPROCESS_EXECUTION_SIGNAL, [subprocess_attr_pattern, subprocess_import_pattern], "Subprocess execution pattern detected."),
        (PatchRiskSignalKind.SHELL_EXECUTION_SIGNAL, [os_system_pattern, "shell=true", "powershell", "cmd.exe", "bash "], "Shell execution pattern detected."),
        (PatchRiskSignalKind.COMMAND_EXECUTION_SIGNAL, ["command_execution", "run command"], "Command execution pattern detected."),
        (PatchRiskSignalKind.TEST_EXECUTION_SIGNAL, ["pytest", "python -m pytest", "npm test", "cargo test", "go test"], "Test execution command pattern detected."),
        (PatchRiskSignalKind.DEPENDENCY_INSTALL_SIGNAL, ["pip install", "npm install", "pnpm install", "yarn add", "poetry add", "cargo add"], "Dependency install pattern detected."),
        (PatchRiskSignalKind.REFERENCE_EXECUTION_SIGNAL, ["opencode run", "hermes run", "openclaw run", "execute opencode", "execute hermes"], "Reference execution pattern detected."),
        (PatchRiskSignalKind.REFERENCE_IMPORT_SIGNAL, ["import opencode", "import hermes", "from opencode", "from hermes", "import openclaw"], "Reference import pattern detected."),
        (PatchRiskSignalKind.SECRET_EXPOSURE_SIGNAL, [".env", "secret=", "secret_key", "private_key"], "Secret-like content detected."),
        (PatchRiskSignalKind.CREDENTIAL_EXPOSURE_SIGNAL, ["credential", "password=", "api_key"], "Credential-like content detected."),
        (PatchRiskSignalKind.TOKEN_EXPOSURE_SIGNAL, ["token=", "bearer ", "sk-"], "Token-like content detected."),
        (PatchRiskSignalKind.PROVIDER_INVOCATION_OPENING_SIGNAL, ["openai.", "anthropic.", "provider_invocation"], "Provider invocation opening detected."),
        (PatchRiskSignalKind.NETWORK_ACCESS_OPENING_SIGNAL, [requests_pattern, httpx_pattern, urllib_pattern, aiohttp_pattern, socket_pattern, "http://", "https://"], "Network access opening detected."),
        (PatchRiskSignalKind.AUTHORITY_GRANT_SIGNAL, ["dominionauthority", "grant d4", "grant d5", "grant d6", "grant d7", "grant d8", "grant d9"], "Authority grant pattern detected."),
    ]
    signals: list[PatchRiskSignal] = []
    for signal_kind, patterns, summary in pattern_specs:
        matched = next((pattern for pattern in patterns if pattern in lowered or pattern.replace(" ", "") in compact), None)
        if matched:
            signals.append(_signal_from_match(len(signals), signal_kind, matched, summary, policy))
        if len(signals) >= policy.max_findings:
            break
    if not signals:
        signals.append(build_patch_risk_signal())
    return signals


def scan_patch_conformance(envelope: DiffProposalEnvelope | None = None, policy: PatchRiskScannerPolicy | None = None) -> list[PatchConformanceFinding]:
    policy = policy or default_patch_risk_scanner_policy()
    signals = scan_diff_proposal_risks(envelope, policy)
    findings: list[PatchConformanceFinding] = []
    for rule_kind in policy.mandatory_conformance_rules:
        related_signal = next((signal for signal in signals if _rule_violated_by_signal(PatchConformanceRuleKind(rule_kind), PatchRiskSignalKind(signal.signal_kind))), None)
        if related_signal:
            findings.append(
                build_patch_conformance_finding(
                    finding_id=f"conformance_finding:v0.35.5:{len(findings)}",
                    rule_kind=rule_kind,
                    finding_kind=PatchConformanceFindingKind.BLOCKING_VIOLATION if related_signal.blocked else PatchConformanceFindingKind.VIOLATION,
                    severity=related_signal.severity,
                    finding_summary=f"Conformance rule {rule_kind} violated by {related_signal.signal_kind}.",
                    evidence_preview=related_signal.evidence_preview,
                    blocked=related_signal.blocked,
                    requires_review=related_signal.requires_review,
                )
            )
        else:
            findings.append(
                build_patch_conformance_finding(
                    finding_id=f"conformance_finding:v0.35.5:{len(findings)}",
                    rule_kind=rule_kind,
                    finding_summary=f"Conformance rule {rule_kind} has no detected violation.",
                )
            )
    return findings


def _rule_violated_by_signal(rule_kind: PatchConformanceRuleKind, signal_kind: PatchRiskSignalKind) -> bool:
    mapping = {
        PatchConformanceRuleKind.NO_APPLY_RULE: {PatchRiskSignalKind.PATCH_APPLY_SIGNAL, PatchRiskSignalKind.APPLY_PATCH_SIGNAL, PatchRiskSignalKind.GIT_APPLY_SIGNAL},
        PatchConformanceRuleKind.NO_WRITE_RULE: {PatchRiskSignalKind.WORKSPACE_WRITE_SIGNAL},
        PatchConformanceRuleKind.NO_CODE_EDIT_RULE: {PatchRiskSignalKind.CODE_EDIT_SIGNAL},
        PatchConformanceRuleKind.NO_SHELL_RULE: {PatchRiskSignalKind.SHELL_EXECUTION_SIGNAL, PatchRiskSignalKind.SUBPROCESS_EXECUTION_SIGNAL, PatchRiskSignalKind.COMMAND_EXECUTION_SIGNAL},
        PatchConformanceRuleKind.NO_TEST_EXECUTION_RULE: {PatchRiskSignalKind.TEST_EXECUTION_SIGNAL},
        PatchConformanceRuleKind.NO_DEPENDENCY_INSTALL_RULE: {PatchRiskSignalKind.DEPENDENCY_INSTALL_SIGNAL},
        PatchConformanceRuleKind.NO_REFERENCE_EXECUTION_RULE: {PatchRiskSignalKind.REFERENCE_EXECUTION_SIGNAL, PatchRiskSignalKind.REFERENCE_IMPORT_SIGNAL},
        PatchConformanceRuleKind.NO_PROVIDER_NETWORK_OPENING_RULE: {PatchRiskSignalKind.PROVIDER_INVOCATION_OPENING_SIGNAL, PatchRiskSignalKind.NETWORK_ACCESS_OPENING_SIGNAL},
        PatchConformanceRuleKind.NO_CREDENTIAL_SECRET_RULE: {PatchRiskSignalKind.SECRET_EXPOSURE_SIGNAL, PatchRiskSignalKind.CREDENTIAL_EXPOSURE_SIGNAL, PatchRiskSignalKind.TOKEN_EXPOSURE_SIGNAL},
    }
    return signal_kind in mapping.get(rule_kind, set())


def scan_patch_safety_regressions(signals: list[PatchRiskSignal]) -> PatchSafetyRegressionReport:
    regression_map = {
        PatchRiskSignalKind.UNSAFE_READINESS_TRUE_SIGNAL: PatchSafetyRegressionKind.UNSAFE_READINESS_FLAG_REGRESSION,
        PatchRiskSignalKind.PROVIDER_INVOCATION_OPENING_SIGNAL: PatchSafetyRegressionKind.PROVIDER_NETWORK_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.NETWORK_ACCESS_OPENING_SIGNAL: PatchSafetyRegressionKind.PROVIDER_NETWORK_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.CREDENTIAL_EXPOSURE_SIGNAL: PatchSafetyRegressionKind.CREDENTIAL_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.SECRET_EXPOSURE_SIGNAL: PatchSafetyRegressionKind.CREDENTIAL_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.SHELL_EXECUTION_SIGNAL: PatchSafetyRegressionKind.SHELL_COMMAND_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.SUBPROCESS_EXECUTION_SIGNAL: PatchSafetyRegressionKind.SHELL_COMMAND_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.WORKSPACE_WRITE_SIGNAL: PatchSafetyRegressionKind.WORKSPACE_WRITE_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.CODE_EDIT_SIGNAL: PatchSafetyRegressionKind.WORKSPACE_WRITE_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.PATCH_APPLY_SIGNAL: PatchSafetyRegressionKind.PATCH_APPLY_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.APPLY_PATCH_SIGNAL: PatchSafetyRegressionKind.PATCH_APPLY_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.GIT_APPLY_SIGNAL: PatchSafetyRegressionKind.PATCH_APPLY_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.REFERENCE_EXECUTION_SIGNAL: PatchSafetyRegressionKind.REFERENCE_EXECUTION_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.REFERENCE_IMPORT_SIGNAL: PatchSafetyRegressionKind.REFERENCE_EXECUTION_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.TEST_EXECUTION_SIGNAL: PatchSafetyRegressionKind.TEST_EXECUTION_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.DEPENDENCY_INSTALL_SIGNAL: PatchSafetyRegressionKind.DEPENDENCY_INSTALL_BOUNDARY_REGRESSION,
        PatchRiskSignalKind.AUTHORITY_GRANT_SIGNAL: PatchSafetyRegressionKind.AUTHORITY_GRANT_BOUNDARY_REGRESSION,
    }
    regression_signals: list[PatchSafetyRegressionSignal] = []
    for signal in signals:
        kind = regression_map.get(PatchRiskSignalKind(signal.signal_kind))
        if kind is None:
            continue
        regression_signals.append(
            build_patch_safety_regression_signal(
                regression_signal_id=f"safety_regression:v0.35.5:{len(regression_signals)}",
                regression_kind=kind,
                severity=signal.severity,
                affected_boundary="Controlled Patch Proposal Layer",
                finding_summary=signal.finding_summary,
                evidence_preview=signal.evidence_preview,
                blocked=signal.blocked,
                requires_review=signal.requires_review,
            )
        )
    return build_patch_safety_regression_report(regression_signals=regression_signals)


def scan_patch_scope_violations(envelope: DiffProposalEnvelope | None = None) -> PatchScopeViolationReport:
    violations: list[PatchScopeViolation] = []
    structured = envelope.structured_patch if envelope is not None else None
    if structured is not None:
        for file_proposal in structured.file_proposals:
            target = file_proposal.target_file
            path = target.target_path_ref
            lowered = path.lower()
            violation_kind: PatchScopeViolationKind | None = None
            if path.startswith("../") or path.startswith("..\\") or ":/" in path or ":\\" in path:
                violation_kind = PatchScopeViolationKind.OUTSIDE_ALLOWED_ROOT
            elif "secret" in lowered or ".env" in lowered:
                violation_kind = PatchScopeViolationKind.SECRET_LIKE_TARGET
            elif "credential" in lowered or "token" in lowered:
                violation_kind = PatchScopeViolationKind.CREDENTIAL_LIKE_TARGET
            elif target.target_kind in {DiffProposalTargetKind.BLOCKED_SECRET_TARGET, DiffProposalTargetKind.BLOCKED_CREDENTIAL_TARGET, DiffProposalTargetKind.BLOCKED_BINARY_TARGET, DiffProposalTargetKind.BLOCKED_EXTERNAL_TARGET}:
                violation_kind = PatchScopeViolationKind.BLOCKED_TARGET_KIND
            elif "references/opencode" in lowered or "references/hermes" in lowered or "references/openclaw" in lowered:
                violation_kind = PatchScopeViolationKind.REFERENCE_EXECUTION_TARGET
            if violation_kind is not None:
                violations.append(
                    build_patch_scope_violation(
                        scope_violation_id=f"scope_violation:v0.35.5:{len(violations)}",
                        violation_kind=violation_kind,
                        target_path_ref=path,
                        finding_summary=f"Target path violates scope: {path}",
                        evidence_preview=path,
                    )
                )
    return build_patch_scope_violation_report(scope_violations=violations)


def build_patch_proposal_risk_report_from_scan(envelope: DiffProposalEnvelope | None = None, policy: PatchRiskScannerPolicy | None = None) -> PatchProposalRiskReport:
    policy = policy or default_patch_risk_scanner_policy()
    signals = scan_diff_proposal_risks(envelope, policy)
    conformance = scan_patch_conformance(envelope, policy)
    safety_report = scan_patch_safety_regressions(signals)
    scope_report = scan_patch_scope_violations(envelope)
    diff_summary = build_patch_diff_risk_summary(
        diff_envelope_id=getattr(envelope, "diff_envelope_id", None),
        unified_diff_id=getattr(getattr(envelope, "unified_diff", None), "unified_diff_id", None),
        structured_patch_id=getattr(getattr(envelope, "structured_patch", None), "structured_patch_id", None),
        risk_signals=signals,
        conformance_findings=conformance,
    )
    return build_patch_proposal_risk_report(diff_risk_summary=diff_summary, safety_regression_report=safety_report, scope_violation_report=scope_report)


def validate_patch_proposal_risk_report(report: PatchProposalRiskReport) -> PatchRiskValidationReport:
    findings: list[PatchRiskValidationFinding] = []
    if not patch_risk_report_is_not_approval(report):
        findings.append(
            build_patch_risk_validation_finding(
                "patch_risk_validation:v0.35.5:approval",
                decision_kind=PatchRiskDecisionKind.BLOCK_PROPOSAL,
                severity=PatchRiskSeverity.BLOCKED,
                finding_summary="Risk report cannot approve apply or execution.",
                evidence_preview="approved/apply/execution readiness",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_patch_risk_validation_finding())
    return build_patch_risk_validation_report(proposal_risk_report_id=report.proposal_risk_report_id, findings=findings)


def patch_risk_flags_preserve_no_apply(flags: PatchRiskFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_RISK_FLAG_NAMES) and flags.production_certified is False


def patch_risk_scanner_policy_blocks_apply(policy: PatchRiskScannerPolicy) -> bool:
    return (
        policy.allow_approved_for_apply is False
        and policy.allow_patch_apply is False
        and policy.allow_workspace_write is False
        and policy.allow_code_edit is False
        and policy.allow_test_execution is False
        and policy.allow_shell is False
        and policy.allow_dependency_install is False
        and policy.allow_reference_execution is False
        and policy.allow_provider_invocation is False
        and policy.allow_network_access is False
        and policy.allow_credential_access is False
        and policy.allow_secret_read is False
    )


def patch_risk_report_is_not_approval(report: PatchProposalRiskReport) -> bool:
    return report.approved_for_apply is False and report.ready_for_patch_application is False and report.ready_for_execution is False


def patch_risk_decision_is_not_apply_permission(decision: PatchRiskScanDecision) -> bool:
    return decision.approved_for_apply is False and decision.ready_for_apply is False and decision.ready_for_execution is False


def v0355_readiness_report_is_not_execution_ready(report: V0355ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_PATCH_RISK_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
