from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_intent import PatchTargetKind
from .patch_plan import PatchPlan, PatchTargetFilePlan


V0354_VERSION = "v0.35.4"
V0354_RELEASE_NAME = "v0.35.4 Diff Proposal Envelope"
DEFAULT_V0354_DOC_PATH = "docs/versions/v0.35/v0.35.4_diff_proposal_envelope.md"
DEFAULT_V0353_PLAN_DOC_REF = "docs/versions/v0.35/v0.35.3_reference_informed_patch_plan_change_set_graph.md"
DEFAULT_V0352_CONTEXT_DOC_REF = "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"

DEFAULT_MAX_UNIFIED_DIFF_CHARS = 4000
DEFAULT_MAX_HUNK_PREVIEW_CHARS = 800

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

UNSAFE_DIFF_PROPOSAL_FLAG_NAMES = (
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


class DiffProposalMode(StrEnum):
    PLAN_ONLY_NO_DIFF = "plan_only_no_diff"
    UNIFIED_DIFF_ARTIFACT = "unified_diff_artifact"
    STRUCTURED_PATCH_ARTIFACT = "structured_patch_artifact"
    COMBINED_UNIFIED_AND_STRUCTURED_ARTIFACT = "combined_unified_and_structured_artifact"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class DiffProposalFormat(StrEnum):
    UNIFIED_DIFF = "unified_diff"
    STRUCTURED_PATCH = "structured_patch"
    FILE_LEVEL_SUMMARY = "file_level_summary"
    HUNK_LEVEL_SUMMARY = "hunk_level_summary"
    BEFORE_AFTER_PREVIEW = "before_after_preview"
    PROPOSAL_METADATA_ONLY = "proposal_metadata_only"
    NO_DIFF = "no_diff"
    UNKNOWN = "unknown"


class DiffProposalSourceKind(StrEnum):
    V0353_PATCH_PLAN = "v0353_patch_plan"
    V0353_CHANGE_SET_GRAPH = "v0353_change_set_graph"
    V0353_TARGET_FILE_PLAN = "v0353_target_file_plan"
    V0352_PATCH_CONTEXT_SNAPSHOT = "v0352_patch_context_snapshot"
    V0352_EVIDENCE_BUNDLE = "v0352_evidence_bundle"
    V0351_PATCH_INTENT_SCOPE_BUNDLE = "v0351_patch_intent_scope_bundle"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    REFERENCE_INFORMED_PATTERN_USE = "reference_informed_pattern_use"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class DiffProposalStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    PROPOSAL_CREATED = "proposal_created"
    PROPOSAL_CREATED_WITH_GAPS = "proposal_created_with_gaps"
    PROPOSAL_VALIDATED = "proposal_validated"
    PROPOSAL_VALIDATED_WITH_WARNINGS = "proposal_validated_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class DiffProposalReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    DIFF_CONTRACT_READY = "diff_contract_ready"
    UNIFIED_DIFF_ARTIFACT_READY = "unified_diff_artifact_ready"
    STRUCTURED_PATCH_ARTIFACT_READY = "structured_patch_artifact_ready"
    DIFF_ENVELOPE_READY = "diff_envelope_ready"
    DESIGN_HANDOFF_READY_FOR_V0355 = "design_handoff_ready_for_v0355"
    DESIGN_HANDOFF_READY_FOR_V0356 = "design_handoff_ready_for_v0356"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DiffProposalDecisionKind(StrEnum):
    ALLOW_DIFF_ARTIFACT = "allow_diff_artifact"
    ALLOW_STRUCTURED_PATCH_ARTIFACT = "allow_structured_patch_artifact"
    ALLOW_METADATA_ONLY_ARTIFACT = "allow_metadata_only_artifact"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class DiffProposalRiskKind(StrEnum):
    INSUFFICIENT_CONTEXT_RISK = "insufficient_context_risk"
    UNGROUNDED_DIFF_RISK = "ungrounded_diff_risk"
    OVERBROAD_DIFF_RISK = "overbroad_diff_risk"
    SCOPE_ESCAPE_RISK = "scope_escape_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    COPIED_CODE_RISK = "copied_code_risk"
    LICENSE_OR_ATTRIBUTION_RISK = "license_or_attribution_risk"
    UNSAFE_READINESS_FLAG_RISK = "unsafe_readiness_flag_risk"
    PROVIDER_NETWORK_OPENING_RISK = "provider_network_opening_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    RAW_SOURCE_DUMP_RISK = "raw_source_dump_risk"
    UNKNOWN = "unknown"


class DiffProposalTargetKind(StrEnum):
    SOURCE_FILE_PROPOSAL = "source_file_proposal"
    TEST_FILE_PROPOSAL = "test_file_proposal"
    DOCUMENTATION_FILE_PROPOSAL = "documentation_file_proposal"
    VERSION_DOC_PROPOSAL = "version_doc_proposal"
    METADATA_FILE_PROPOSAL = "metadata_file_proposal"
    REFERENCE_DIGEST_DOC_PROPOSAL = "reference_digest_doc_proposal"
    BLOCKED_SECRET_TARGET = "blocked_secret_target"
    BLOCKED_CREDENTIAL_TARGET = "blocked_credential_target"
    BLOCKED_BINARY_TARGET = "blocked_binary_target"
    BLOCKED_EXTERNAL_TARGET = "blocked_external_target"
    UNKNOWN = "unknown"


class DiffProposalHunkKind(StrEnum):
    ADD_BLOCK = "add_block"
    REMOVE_BLOCK = "remove_block"
    REPLACE_BLOCK = "replace_block"
    INSERT_BEFORE = "insert_before"
    INSERT_AFTER = "insert_after"
    METADATA_ONLY_CHANGE = "metadata_only_change"
    DOCUMENTATION_CHANGE = "documentation_change"
    TEST_CHANGE = "test_change"
    SAFETY_BOUNDARY_CHANGE = "safety_boundary_change"
    NO_OP_HUNK = "no_op_hunk"
    UNKNOWN = "unknown"


class DiffProposalValidationKind(StrEnum):
    SYNTAX_SHAPE_CHECK = "syntax_shape_check"
    SCOPE_ALIGNMENT_CHECK = "scope_alignment_check"
    SOURCE_CONTEXT_ALIGNMENT_CHECK = "source_context_alignment_check"
    NO_APPLY_CHECK = "no_apply_check"
    NO_WRITE_CHECK = "no_write_check"
    NO_SECRET_CHECK = "no_secret_check"
    NO_COMMAND_CHECK = "no_command_check"
    NO_DEPENDENCY_INSTALL_CHECK = "no_dependency_install_check"
    NO_REFERENCE_EXECUTION_CHECK = "no_reference_execution_check"
    REVIEW_REQUIRED_CHECK = "review_required_check"
    UNKNOWN = "unknown"


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0354_VERSION not in value:
        raise ValueError("version must include v0.35.4")


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
            raise ValueError(f"{name} must always be False in v0.35.4")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _bounded(value: str, limit: int, marker: str = "\n[truncated by v0.35.4 boundary]") -> tuple[str, bool]:
    if limit < 0:
        raise ValueError("limit must be >= 0")
    if len(value) <= limit:
        return value, False
    if limit <= len(marker):
        return value[:limit], True
    return value[: limit - len(marker)] + marker, True


def _target_kind_from_patch_target_kind(target_kind: PatchTargetKind | str) -> DiffProposalTargetKind:
    mapped = {
        PatchTargetKind.SOURCE_FILE: DiffProposalTargetKind.SOURCE_FILE_PROPOSAL,
        PatchTargetKind.TEST_FILE: DiffProposalTargetKind.TEST_FILE_PROPOSAL,
        PatchTargetKind.DOCUMENTATION_FILE: DiffProposalTargetKind.DOCUMENTATION_FILE_PROPOSAL,
        PatchTargetKind.VERSION_DOCUMENT: DiffProposalTargetKind.VERSION_DOC_PROPOSAL,
        PatchTargetKind.PACKAGE_METADATA: DiffProposalTargetKind.METADATA_FILE_PROPOSAL,
        PatchTargetKind.REFERENCE_DIGEST_DOCUMENT: DiffProposalTargetKind.REFERENCE_DIGEST_DOC_PROPOSAL,
        PatchTargetKind.SECRET_LIKE_FILE: DiffProposalTargetKind.BLOCKED_SECRET_TARGET,
        PatchTargetKind.CREDENTIAL_LIKE_FILE: DiffProposalTargetKind.BLOCKED_CREDENTIAL_TARGET,
        PatchTargetKind.BINARY_FILE: DiffProposalTargetKind.BLOCKED_BINARY_TARGET,
        PatchTargetKind.EXTERNAL_PATH: DiffProposalTargetKind.BLOCKED_EXTERNAL_TARGET,
    }
    return mapped.get(PatchTargetKind(target_kind), DiffProposalTargetKind.UNKNOWN)


@dataclass(frozen=True)
class DiffProposalFlagSet:
    flag_set_id: str
    version: str
    diff_proposal_layer_constructed: bool
    unified_diff_artifact_available: bool
    structured_patch_artifact_available: bool
    patch_file_proposal_available: bool
    patch_hunk_proposal_available: bool
    diff_validation_available: bool
    ready_for_v0355_patch_risk_conformance_scanner: bool
    ready_for_v0356_human_review_packet: bool
    ready_for_diff_proposal_envelope: bool
    ready_for_unified_diff_proposal: bool
    ready_for_structured_patch_proposal: bool
    ready_for_patch_hunk_proposal: bool
    ready_for_patch_proposal_artifact: bool
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
        _validate_false(self, UNSAFE_DIFF_PROPOSAL_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalSourceRef:
    source_ref_id: str
    source_kind: DiffProposalSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        DiffProposalSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalGenerationPolicy:
    generation_policy_id: str
    version: str
    allowed_formats: list[DiffProposalFormat | str]
    blocked_formats: list[DiffProposalFormat | str]
    allowed_target_kinds: list[DiffProposalTargetKind | str]
    blocked_target_kinds: list[DiffProposalTargetKind | str]
    allowed_hunk_kinds: list[DiffProposalHunkKind | str]
    blocked_hunk_kinds: list[DiffProposalHunkKind | str]
    max_file_proposals: int
    max_hunks_per_file: int
    max_total_hunks: int
    max_unified_diff_chars: int
    max_hunk_preview_chars: int
    require_patch_plan: bool
    require_context_snapshot: bool
    require_scope_alignment: bool
    require_no_apply: bool
    require_no_write: bool
    allow_unified_diff_text: bool
    allow_structured_patch: bool
    allow_before_after_preview: bool
    allow_patch_apply: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("generation_policy_id", self.generation_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_formats", self.allowed_formats, DiffProposalFormat)
        _validate_enum_list("blocked_formats", self.blocked_formats, DiffProposalFormat)
        _validate_enum_list("allowed_target_kinds", self.allowed_target_kinds, DiffProposalTargetKind)
        _validate_enum_list("blocked_target_kinds", self.blocked_target_kinds, DiffProposalTargetKind)
        _validate_enum_list("allowed_hunk_kinds", self.allowed_hunk_kinds, DiffProposalHunkKind)
        _validate_enum_list("blocked_hunk_kinds", self.blocked_hunk_kinds, DiffProposalHunkKind)
        for name in ("max_file_proposals", "max_hunks_per_file", "max_total_hunks", "max_unified_diff_chars", "max_hunk_preview_chars"):
            _validate_non_negative(name, getattr(self, name))
        if self.require_no_apply is not True or self.require_no_write is not True:
            raise ValueError("require_no_apply and require_no_write must be True")
        for name in ("allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_shell", "allow_dependency_install"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.4")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalInput:
    diff_input_id: str
    version: str
    patch_plan_id: str | None
    change_set_graph_id: str | None
    context_snapshot_id: str | None
    evidence_bundle_id: str | None
    intent_scope_bundle_id: str | None
    requested_mode: DiffProposalMode | str
    task_summary: str
    source_refs: list[DiffProposalSourceRef]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("diff_input_id", self.diff_input_id)
        _validate_version(self.version)
        for name in ("patch_plan_id", "change_set_graph_id", "context_snapshot_id", "evidence_bundle_id", "intent_scope_bundle_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        DiffProposalMode(self.requested_mode)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"patch_application", "workspace_write", "code_edit", "shell_execution", "command_execution", "test_execution", "dependency_install", "reference_execution", "provider_invocation", "direct_network_access", "credential_access"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include unsafe runtime actions")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalTargetFile:
    target_file_id: str
    target_path_ref: str
    target_kind: DiffProposalTargetKind | str
    source_target_plan_id: str | None
    proposal_summary: str
    allowed_for_diff_artifact: bool
    allowed_for_apply: bool = False
    allowed_for_write: bool = False
    risk_kinds: list[DiffProposalRiskKind | str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("target_file_id", self.target_file_id)
        _require_non_blank("target_path_ref", self.target_path_ref)
        DiffProposalTargetKind(self.target_kind)
        if self.source_target_plan_id is not None:
            _require_non_blank("source_target_plan_id", self.source_target_plan_id)
        _require_non_blank("proposal_summary", self.proposal_summary)
        _validate_false(self, ("allowed_for_apply", "allowed_for_write"))
        _validate_enum_list("risk_kinds", self.risk_kinds, DiffProposalRiskKind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchHunkProposal:
    hunk_proposal_id: str
    target_file_id: str
    hunk_kind: DiffProposalHunkKind | str
    hunk_summary: str
    rationale: str
    before_preview: str
    after_preview: str
    proposed_hunk_text: str
    risk_kinds: list[DiffProposalRiskKind | str]
    source_change_node_ids: list[str]
    redacted: bool
    truncated: bool
    ready_for_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("hunk_proposal_id", self.hunk_proposal_id)
        _require_non_blank("target_file_id", self.target_file_id)
        DiffProposalHunkKind(self.hunk_kind)
        _require_non_blank("hunk_summary", self.hunk_summary)
        _require_non_blank("rationale", self.rationale)
        for name in ("before_preview", "after_preview", "proposed_hunk_text"):
            if len(getattr(self, name)) > DEFAULT_MAX_UNIFIED_DIFF_CHARS:
                raise ValueError(f"{name} must be bounded")
        _validate_enum_list("risk_kinds", self.risk_kinds, DiffProposalRiskKind)
        _validate_string_list("source_change_node_ids", self.source_change_node_ids)
        _validate_false(self, ("ready_for_apply",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchFileProposal:
    file_proposal_id: str
    target_file: DiffProposalTargetFile
    hunk_proposals: list[PatchHunkProposal]
    file_proposal_summary: str
    proposed_file_diff_preview: str
    risk_kinds: list[DiffProposalRiskKind | str]
    ready_for_apply: bool = False
    ready_for_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("file_proposal_id", self.file_proposal_id)
        _validate_list("hunk_proposals", self.hunk_proposals)
        _require_non_blank("file_proposal_summary", self.file_proposal_summary)
        if len(self.proposed_file_diff_preview) > DEFAULT_MAX_UNIFIED_DIFF_CHARS:
            raise ValueError("proposed_file_diff_preview must be bounded")
        _validate_enum_list("risk_kinds", self.risk_kinds, DiffProposalRiskKind)
        _validate_false(self, ("ready_for_apply", "ready_for_write"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class UnifiedDiffProposal:
    unified_diff_id: str
    version: str
    diff_text: str
    diff_summary: str
    file_proposal_ids: list[str]
    hunk_count: int
    redacted: bool
    truncated: bool
    ready_for_apply: bool = False
    ready_for_git_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("unified_diff_id", self.unified_diff_id)
        _validate_version(self.version)
        _require_non_blank("diff_summary", self.diff_summary)
        if len(self.diff_text) > DEFAULT_MAX_UNIFIED_DIFF_CHARS:
            raise ValueError("diff_text must be bounded")
        _validate_string_list("file_proposal_ids", self.file_proposal_ids)
        _validate_non_negative("hunk_count", self.hunk_count)
        _validate_false(self, ("ready_for_apply", "ready_for_git_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class StructuredPatchProposal:
    structured_patch_id: str
    version: str
    file_proposals: list[PatchFileProposal]
    proposal_summary: str
    proposal_rationale: str
    risk_kinds: list[DiffProposalRiskKind | str]
    ready_for_apply: bool = False
    ready_for_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("structured_patch_id", self.structured_patch_id)
        _validate_version(self.version)
        _validate_list("file_proposals", self.file_proposals)
        _require_non_blank("proposal_summary", self.proposal_summary)
        _require_non_blank("proposal_rationale", self.proposal_rationale)
        _validate_enum_list("risk_kinds", self.risk_kinds, DiffProposalRiskKind)
        _validate_false(self, ("ready_for_apply", "ready_for_write"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalEnvelope:
    diff_envelope_id: str
    version: str
    mode: DiffProposalMode | str
    status: DiffProposalStatus | str
    readiness_level: DiffProposalReadinessLevel | str
    diff_input_id: str
    unified_diff: UnifiedDiffProposal | None
    structured_patch: StructuredPatchProposal | None
    source_refs: list[DiffProposalSourceRef]
    summary: str
    gaps: list[str]
    risk_kinds: list[DiffProposalRiskKind | str]
    ready_for_v0355_patch_risk_conformance_scanner: bool
    ready_for_v0356_human_review_packet: bool
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("diff_envelope_id", "diff_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        DiffProposalMode(self.mode)
        DiffProposalStatus(self.status)
        DiffProposalReadinessLevel(self.readiness_level)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("gaps", self.gaps)
        _validate_enum_list("risk_kinds", self.risk_kinds, DiffProposalRiskKind)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalValidationFinding:
    finding_id: str
    validation_kind: DiffProposalValidationKind | str
    decision_kind: DiffProposalDecisionKind | str
    risk_kinds: list[DiffProposalRiskKind | str]
    message: str
    blocks_validation: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        DiffProposalValidationKind(self.validation_kind)
        DiffProposalDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, DiffProposalRiskKind)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalValidationReport:
    validation_report_id: str
    version: str
    diff_envelope_id: str | None
    findings: list[DiffProposalValidationFinding]
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
        if self.diff_envelope_id is not None:
            _require_non_blank("diff_envelope_id", self.diff_envelope_id)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalReport:
    report_id: str
    version: str
    diff_envelope_id: str
    summary: str
    diff_proposal_envelope_ready: bool
    unified_diff_artifact_ready: bool
    structured_patch_artifact_ready: bool
    patch_hunk_artifact_ready: bool
    gap_items: list[str]
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "diff_envelope_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("gap_items", self.gap_items)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DiffProposalRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
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
class DiffProposalNoApplyGuarantee:
    guarantee_id: str
    version: str
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
class V0354ReadinessReport:
    report_id: str
    version: str
    diff_envelope_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0355_patch_risk_conformance_scanner: bool = True
    ready_for_v0356_human_review_packet: bool = True
    ready_for_diff_proposal_envelope: bool = True
    ready_for_unified_diff_proposal: bool = True
    ready_for_structured_patch_proposal: bool = True
    ready_for_patch_hunk_proposal: bool = True
    ready_for_patch_proposal_artifact: bool = True
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
        if self.diff_envelope_id is not None:
            _require_non_blank("diff_envelope_id", self.diff_envelope_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_DIFF_PROPOSAL_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_diff_proposal_flags(flag_set_id: str = "diff_proposal_flags:v0.35.4", **kwargs: Any) -> DiffProposalFlagSet:
    return DiffProposalFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0354_VERSION),
        diff_proposal_layer_constructed=kwargs.pop("diff_proposal_layer_constructed", True),
        unified_diff_artifact_available=kwargs.pop("unified_diff_artifact_available", True),
        structured_patch_artifact_available=kwargs.pop("structured_patch_artifact_available", True),
        patch_file_proposal_available=kwargs.pop("patch_file_proposal_available", True),
        patch_hunk_proposal_available=kwargs.pop("patch_hunk_proposal_available", True),
        diff_validation_available=kwargs.pop("diff_validation_available", True),
        ready_for_v0355_patch_risk_conformance_scanner=kwargs.pop("ready_for_v0355_patch_risk_conformance_scanner", True),
        ready_for_v0356_human_review_packet=kwargs.pop("ready_for_v0356_human_review_packet", True),
        ready_for_diff_proposal_envelope=kwargs.pop("ready_for_diff_proposal_envelope", True),
        ready_for_unified_diff_proposal=kwargs.pop("ready_for_unified_diff_proposal", True),
        ready_for_structured_patch_proposal=kwargs.pop("ready_for_structured_patch_proposal", True),
        ready_for_patch_hunk_proposal=kwargs.pop("ready_for_patch_hunk_proposal", True),
        ready_for_patch_proposal_artifact=kwargs.pop("ready_for_patch_proposal_artifact", True),
        **kwargs,
    )


def build_diff_proposal_source_ref(source_ref_id: str = "diff_source:v0.35.4", **kwargs: Any) -> DiffProposalSourceRef:
    return DiffProposalSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", DiffProposalSourceKind.V0353_PATCH_PLAN),
        source_id=kwargs.pop("source_id", "patch_plan:v0.35.3"),
        source_summary=kwargs.pop("source_summary", "Supplied v0.35.3 patch plan metadata."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0353_PLAN_DOC_REF]),
        **kwargs,
    )


def build_diff_proposal_generation_policy(generation_policy_id: str = "diff_policy:v0.35.4", **kwargs: Any) -> DiffProposalGenerationPolicy:
    return DiffProposalGenerationPolicy(
        generation_policy_id=generation_policy_id,
        version=kwargs.pop("version", V0354_VERSION),
        allowed_formats=kwargs.pop("allowed_formats", [DiffProposalFormat.UNIFIED_DIFF, DiffProposalFormat.STRUCTURED_PATCH, DiffProposalFormat.BEFORE_AFTER_PREVIEW, DiffProposalFormat.PROPOSAL_METADATA_ONLY]),
        blocked_formats=kwargs.pop("blocked_formats", [DiffProposalFormat.UNKNOWN]),
        allowed_target_kinds=kwargs.pop("allowed_target_kinds", [DiffProposalTargetKind.SOURCE_FILE_PROPOSAL, DiffProposalTargetKind.TEST_FILE_PROPOSAL, DiffProposalTargetKind.DOCUMENTATION_FILE_PROPOSAL, DiffProposalTargetKind.VERSION_DOC_PROPOSAL, DiffProposalTargetKind.METADATA_FILE_PROPOSAL]),
        blocked_target_kinds=kwargs.pop("blocked_target_kinds", [DiffProposalTargetKind.BLOCKED_SECRET_TARGET, DiffProposalTargetKind.BLOCKED_CREDENTIAL_TARGET, DiffProposalTargetKind.BLOCKED_BINARY_TARGET, DiffProposalTargetKind.BLOCKED_EXTERNAL_TARGET]),
        allowed_hunk_kinds=kwargs.pop("allowed_hunk_kinds", [DiffProposalHunkKind.ADD_BLOCK, DiffProposalHunkKind.REPLACE_BLOCK, DiffProposalHunkKind.METADATA_ONLY_CHANGE, DiffProposalHunkKind.DOCUMENTATION_CHANGE, DiffProposalHunkKind.TEST_CHANGE, DiffProposalHunkKind.SAFETY_BOUNDARY_CHANGE]),
        blocked_hunk_kinds=kwargs.pop("blocked_hunk_kinds", [DiffProposalHunkKind.UNKNOWN]),
        max_file_proposals=kwargs.pop("max_file_proposals", 8),
        max_hunks_per_file=kwargs.pop("max_hunks_per_file", 3),
        max_total_hunks=kwargs.pop("max_total_hunks", 16),
        max_unified_diff_chars=kwargs.pop("max_unified_diff_chars", DEFAULT_MAX_UNIFIED_DIFF_CHARS),
        max_hunk_preview_chars=kwargs.pop("max_hunk_preview_chars", DEFAULT_MAX_HUNK_PREVIEW_CHARS),
        require_patch_plan=kwargs.pop("require_patch_plan", True),
        require_context_snapshot=kwargs.pop("require_context_snapshot", True),
        require_scope_alignment=kwargs.pop("require_scope_alignment", True),
        require_no_apply=kwargs.pop("require_no_apply", True),
        require_no_write=kwargs.pop("require_no_write", True),
        allow_unified_diff_text=kwargs.pop("allow_unified_diff_text", True),
        allow_structured_patch=kwargs.pop("allow_structured_patch", True),
        allow_before_after_preview=kwargs.pop("allow_before_after_preview", True),
        **kwargs,
    )


def default_diff_proposal_generation_policy() -> DiffProposalGenerationPolicy:
    return build_diff_proposal_generation_policy()


def build_diff_proposal_input(diff_input_id: str = "diff_input:v0.35.4", **kwargs: Any) -> DiffProposalInput:
    return DiffProposalInput(
        diff_input_id=diff_input_id,
        version=kwargs.pop("version", V0354_VERSION),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        change_set_graph_id=kwargs.pop("change_set_graph_id", "change_set_graph:v0.35.3"),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "evidence_bundle:v0.35.2"),
        intent_scope_bundle_id=kwargs.pop("intent_scope_bundle_id", "intent_scope_bundle:v0.35.1"),
        requested_mode=kwargs.pop("requested_mode", DiffProposalMode.COMBINED_UNIFIED_AND_STRUCTURED_ARTIFACT),
        task_summary=kwargs.pop("task_summary", "Create bounded diff proposal artifacts from supplied planning metadata only."),
        source_refs=kwargs.pop("source_refs", [build_diff_proposal_source_ref()]),
        **kwargs,
    )


def build_diff_proposal_input_from_patch_plan(patch_plan: PatchPlan | None = None, **kwargs: Any) -> DiffProposalInput:
    if patch_plan is None:
        return build_diff_proposal_input(
            patch_plan_id=None,
            change_set_graph_id=None,
            context_snapshot_id=None,
            evidence_bundle_id=None,
            requested_mode=DiffProposalMode.REVIEW_REQUIRED,
            task_summary="Diff proposal input is review-required because patch plan/context metadata is missing.",
            metadata={"gap": "missing_patch_plan_or_context_metadata"},
            **kwargs,
        )
    graph = patch_plan.change_set_graph
    return build_diff_proposal_input(
        patch_plan_id=patch_plan.patch_plan_id,
        change_set_graph_id=graph.change_set_graph_id,
        context_snapshot_id=patch_plan.context_snapshot_id,
        intent_scope_bundle_id=patch_plan.intent_id,
        source_refs=[
            build_diff_proposal_source_ref(source_id=patch_plan.patch_plan_id),
            build_diff_proposal_source_ref(
                "diff_source:v0.35.4:graph",
                source_kind=DiffProposalSourceKind.V0353_CHANGE_SET_GRAPH,
                source_id=graph.change_set_graph_id,
                source_summary="Supplied v0.35.3 change-set graph metadata.",
            ),
        ],
        **kwargs,
    )


def build_diff_proposal_target_file(target_file_id: str = "diff_target_file:v0.35.4:model", **kwargs: Any) -> DiffProposalTargetFile:
    return DiffProposalTargetFile(
        target_file_id=target_file_id,
        target_path_ref=kwargs.pop("target_path_ref", "src/chanta_core/agent_runtime/patch_diff_proposal.py"),
        target_kind=kwargs.pop("target_kind", DiffProposalTargetKind.SOURCE_FILE_PROPOSAL),
        source_target_plan_id=kwargs.pop("source_target_plan_id", "target_file_plan:v0.35.3:model"),
        proposal_summary=kwargs.pop("proposal_summary", "Target file may receive a bounded diff artifact proposal only."),
        allowed_for_diff_artifact=kwargs.pop("allowed_for_diff_artifact", True),
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_patch_hunk_proposal(hunk_proposal_id: str = "hunk_proposal:v0.35.4:model", **kwargs: Any) -> PatchHunkProposal:
    before_preview, before_truncated = _bounded(kwargs.pop("before_preview", "Existing text is represented only by supplied context metadata."), DEFAULT_MAX_HUNK_PREVIEW_CHARS)
    after_preview, after_truncated = _bounded(kwargs.pop("after_preview", "Proposed text remains an unapplied in-memory artifact."), DEFAULT_MAX_HUNK_PREVIEW_CHARS)
    proposed_hunk_text, hunk_truncated = _bounded(kwargs.pop("proposed_hunk_text", "@@ metadata proposal @@\n- supplied context placeholder\n+ proposed artifact placeholder"), DEFAULT_MAX_UNIFIED_DIFF_CHARS)
    return PatchHunkProposal(
        hunk_proposal_id=hunk_proposal_id,
        target_file_id=kwargs.pop("target_file_id", "diff_target_file:v0.35.4:model"),
        hunk_kind=kwargs.pop("hunk_kind", DiffProposalHunkKind.METADATA_ONLY_CHANGE),
        hunk_summary=kwargs.pop("hunk_summary", "Bounded hunk proposal metadata."),
        rationale=kwargs.pop("rationale", "Hunk proposal is not applied and does not write files."),
        before_preview=before_preview,
        after_preview=after_preview,
        proposed_hunk_text=proposed_hunk_text,
        risk_kinds=kwargs.pop("risk_kinds", []),
        source_change_node_ids=kwargs.pop("source_change_node_ids", ["change_node:v0.35.3:model"]),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", before_truncated or after_truncated or hunk_truncated),
        **kwargs,
    )


def build_patch_file_proposal(file_proposal_id: str = "file_proposal:v0.35.4:model", **kwargs: Any) -> PatchFileProposal:
    target_file = kwargs.pop("target_file", build_diff_proposal_target_file())
    hunks = kwargs.pop("hunk_proposals", [build_patch_hunk_proposal(target_file_id=target_file.target_file_id)])
    preview, truncated = _bounded(kwargs.pop("proposed_file_diff_preview", "\n".join(hunk.proposed_hunk_text for hunk in hunks)), DEFAULT_MAX_UNIFIED_DIFF_CHARS)
    return PatchFileProposal(
        file_proposal_id=file_proposal_id,
        target_file=target_file,
        hunk_proposals=hunks,
        file_proposal_summary=kwargs.pop("file_proposal_summary", "File proposal is bounded diff metadata, not file write."),
        proposed_file_diff_preview=preview,
        risk_kinds=kwargs.pop("risk_kinds", []),
        metadata=kwargs.pop("metadata", {"truncated": truncated}),
        **kwargs,
    )


def build_unified_diff_proposal(unified_diff_id: str = "unified_diff:v0.35.4", **kwargs: Any) -> UnifiedDiffProposal:
    diff_text, truncated = _bounded(kwargs.pop("diff_text", "--- a/metadata\n+++ b/metadata\n@@ proposal @@\n- planned context\n+ proposed artifact"), kwargs.pop("max_diff_chars", DEFAULT_MAX_UNIFIED_DIFF_CHARS))
    return UnifiedDiffProposal(
        unified_diff_id=unified_diff_id,
        version=kwargs.pop("version", V0354_VERSION),
        diff_text=diff_text,
        diff_summary=kwargs.pop("diff_summary", "Unified diff proposal is bounded artifact text only."),
        file_proposal_ids=kwargs.pop("file_proposal_ids", ["file_proposal:v0.35.4:model"]),
        hunk_count=kwargs.pop("hunk_count", 1),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", truncated),
        **kwargs,
    )


def build_structured_patch_proposal(structured_patch_id: str = "structured_patch:v0.35.4", **kwargs: Any) -> StructuredPatchProposal:
    return StructuredPatchProposal(
        structured_patch_id=structured_patch_id,
        version=kwargs.pop("version", V0354_VERSION),
        file_proposals=kwargs.pop("file_proposals", [build_patch_file_proposal()]),
        proposal_summary=kwargs.pop("proposal_summary", "Structured patch proposal is metadata/artifact only."),
        proposal_rationale=kwargs.pop("proposal_rationale", "Proposal may support later human review but does not write or apply patches."),
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_structured_patch_proposal_from_patch_plan(patch_plan: PatchPlan | None = None, policy: DiffProposalGenerationPolicy | None = None, **kwargs: Any) -> StructuredPatchProposal:
    policy = policy or default_diff_proposal_generation_policy()
    if patch_plan is None:
        return build_structured_patch_proposal(
            file_proposals=[],
            proposal_summary="Structured patch proposal blocked because required plan/context metadata is missing.",
            proposal_rationale="Missing metadata must produce gaps or review-required state, not unsafe inference.",
            risk_kinds=[DiffProposalRiskKind.INSUFFICIENT_CONTEXT_RISK],
            metadata={"gap": "missing_patch_plan"},
            **kwargs,
        )
    file_proposals: list[PatchFileProposal] = []
    total_hunks = 0
    for index, target_plan in enumerate(patch_plan.change_set_graph.target_file_plans[: policy.max_file_proposals]):
        if total_hunks >= policy.max_total_hunks:
            break
        file_proposals.append(_build_file_proposal_from_target_plan(index, target_plan, policy))
        total_hunks += len(file_proposals[-1].hunk_proposals)
    risk_kinds = [DiffProposalRiskKind.INSUFFICIENT_CONTEXT_RISK] if patch_plan.gaps else []
    return build_structured_patch_proposal(
        file_proposals=file_proposals,
        proposal_summary="Structured patch proposal derived from supplied v0.35.3 planning metadata only.",
        proposal_rationale="Each file and hunk proposal remains an unapplied bounded artifact.",
        risk_kinds=risk_kinds,
        metadata={"source_patch_plan_id": patch_plan.patch_plan_id, "source_change_set_graph_id": patch_plan.change_set_graph.change_set_graph_id},
        **kwargs,
    )


def _build_file_proposal_from_target_plan(index: int, target_plan: PatchTargetFilePlan, policy: DiffProposalGenerationPolicy) -> PatchFileProposal:
    target_kind = _target_kind_from_patch_target_kind(target_plan.target_kind)
    target = build_diff_proposal_target_file(
        target_file_id=f"diff_target_file:v0.35.4:{index}",
        target_path_ref=target_plan.target_path_ref,
        target_kind=target_kind,
        source_target_plan_id=target_plan.target_file_plan_id,
        proposal_summary=f"Bounded diff artifact proposal for {target_plan.target_path_ref}.",
        allowed_for_diff_artifact=target_kind not in set(policy.blocked_target_kinds),
        risk_kinds=[DiffProposalRiskKind.SCOPE_ESCAPE_RISK] if target_kind in set(policy.blocked_target_kinds) else [],
    )
    before_preview, before_truncated = _bounded(f"Current file context is represented by v0.35.2 snapshot metadata for {target_plan.target_path_ref}.", policy.max_hunk_preview_chars)
    after_preview, after_truncated = _bounded(f"Future artifact should express planned role: {target_plan.planned_role}.", policy.max_hunk_preview_chars)
    hunk_text, hunk_truncated = _bounded(
        f"@@ proposal:{target_plan.target_file_plan_id} @@\n- {before_preview}\n+ {after_preview}\n",
        policy.max_unified_diff_chars,
    )
    hunk = build_patch_hunk_proposal(
        hunk_proposal_id=f"hunk_proposal:v0.35.4:{index}:0",
        target_file_id=target.target_file_id,
        hunk_kind=DiffProposalHunkKind.METADATA_ONLY_CHANGE,
        hunk_summary=f"Metadata hunk proposal for {target_plan.target_path_ref}.",
        rationale=target_plan.rationale,
        before_preview=before_preview,
        after_preview=after_preview,
        proposed_hunk_text=hunk_text,
        source_change_node_ids=target_plan.planned_change_node_ids,
        truncated=before_truncated or after_truncated or hunk_truncated,
    )
    preview, preview_truncated = _bounded(hunk.proposed_hunk_text, policy.max_unified_diff_chars)
    return build_patch_file_proposal(
        file_proposal_id=f"file_proposal:v0.35.4:{index}",
        target_file=target,
        hunk_proposals=[hunk][: policy.max_hunks_per_file],
        file_proposal_summary=f"File-level proposal artifact for {target_plan.target_path_ref}.",
        proposed_file_diff_preview=preview,
        metadata={"truncated": preview_truncated},
    )


def build_unified_diff_proposal_from_structured_patch(structured_patch: StructuredPatchProposal, policy: DiffProposalGenerationPolicy | None = None, **kwargs: Any) -> UnifiedDiffProposal:
    policy = policy or default_diff_proposal_generation_policy()
    lines: list[str] = []
    hunk_count = 0
    for file_proposal in structured_patch.file_proposals[: policy.max_file_proposals]:
        path_ref = file_proposal.target_file.target_path_ref
        lines.extend([f"--- a/{path_ref}", f"+++ b/{path_ref}"])
        for hunk in file_proposal.hunk_proposals[: policy.max_hunks_per_file]:
            if hunk_count >= policy.max_total_hunks:
                break
            lines.append(hunk.proposed_hunk_text)
            hunk_count += 1
    diff_text, truncated = _bounded("\n".join(lines), policy.max_unified_diff_chars)
    return build_unified_diff_proposal(
        diff_text=diff_text,
        file_proposal_ids=[proposal.file_proposal_id for proposal in structured_patch.file_proposals],
        hunk_count=hunk_count,
        truncated=truncated,
        metadata={"source_structured_patch_id": structured_patch.structured_patch_id},
        **kwargs,
    )


def build_diff_proposal_envelope(diff_envelope_id: str = "diff_envelope:v0.35.4", **kwargs: Any) -> DiffProposalEnvelope:
    structured_patch = kwargs.pop("structured_patch", build_structured_patch_proposal())
    unified_diff = kwargs.pop("unified_diff", build_unified_diff_proposal_from_structured_patch(structured_patch))
    gaps = kwargs.pop("gaps", [])
    return DiffProposalEnvelope(
        diff_envelope_id=diff_envelope_id,
        version=kwargs.pop("version", V0354_VERSION),
        mode=kwargs.pop("mode", DiffProposalMode.COMBINED_UNIFIED_AND_STRUCTURED_ARTIFACT if structured_patch or unified_diff else DiffProposalMode.REVIEW_REQUIRED),
        status=kwargs.pop("status", DiffProposalStatus.PROPOSAL_CREATED_WITH_GAPS if gaps else DiffProposalStatus.PROPOSAL_CREATED),
        readiness_level=kwargs.pop("readiness_level", DiffProposalReadinessLevel.DIFF_ENVELOPE_READY if not gaps else DiffProposalReadinessLevel.BLOCKED),
        diff_input_id=kwargs.pop("diff_input_id", "diff_input:v0.35.4"),
        unified_diff=unified_diff,
        structured_patch=structured_patch,
        source_refs=kwargs.pop("source_refs", [build_diff_proposal_source_ref()]),
        summary=kwargs.pop("summary", "Diff proposal envelope contains bounded artifacts only; it is not apply/write authority."),
        gaps=gaps,
        risk_kinds=kwargs.pop("risk_kinds", [DiffProposalRiskKind.INSUFFICIENT_CONTEXT_RISK] if gaps else []),
        ready_for_v0355_patch_risk_conformance_scanner=kwargs.pop("ready_for_v0355_patch_risk_conformance_scanner", True),
        ready_for_v0356_human_review_packet=kwargs.pop("ready_for_v0356_human_review_packet", True),
        **kwargs,
    )


def build_diff_proposal_validation_finding(finding_id: str = "diff_finding:v0.35.4:ok", **kwargs: Any) -> DiffProposalValidationFinding:
    return DiffProposalValidationFinding(
        finding_id=finding_id,
        validation_kind=kwargs.pop("validation_kind", DiffProposalValidationKind.NO_APPLY_CHECK),
        decision_kind=kwargs.pop("decision_kind", DiffProposalDecisionKind.ALLOW_DIFF_ARTIFACT),
        risk_kinds=kwargs.pop("risk_kinds", []),
        message=kwargs.pop("message", "Diff proposal remains bounded artifact metadata only."),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_diff_proposal_validation_report(validation_report_id: str = "diff_validation:v0.35.4", **kwargs: Any) -> DiffProposalValidationReport:
    findings = kwargs.pop("findings", [build_diff_proposal_validation_finding()])
    return DiffProposalValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0354_VERSION),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Diff validation does not certify apply, write, edit, or execution."),
        **kwargs,
    )


def build_diff_proposal_report(report_id: str = "diff_report:v0.35.4", **kwargs: Any) -> DiffProposalReport:
    return DiffProposalReport(
        report_id=report_id,
        version=kwargs.pop("version", V0354_VERSION),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        summary=kwargs.pop("summary", "Diff proposal artifacts are ready for risk scan/review handoff only."),
        diff_proposal_envelope_ready=kwargs.pop("diff_proposal_envelope_ready", True),
        unified_diff_artifact_ready=kwargs.pop("unified_diff_artifact_ready", True),
        structured_patch_artifact_ready=kwargs.pop("structured_patch_artifact_ready", True),
        patch_hunk_artifact_ready=kwargs.pop("patch_hunk_artifact_ready", True),
        gap_items=kwargs.pop("gap_items", []),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0354_DOC_PATH, DEFAULT_V0353_PLAN_DOC_REF]),
        **kwargs,
    )


def build_diff_proposal_run_preview(run_preview_id: str = "diff_run_preview:v0.35.4", **kwargs: Any) -> DiffProposalRunPreview:
    return DiffProposalRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["validate supplied plan metadata", "create structured artifact", "create bounded unified diff artifact", "create envelope report"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["StructuredPatchProposal", "UnifiedDiffProposal", "DiffProposalEnvelope"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["patch application", "workspace write", "code edit", "apply_patch", "git apply", "test execution", "shell execution"]),
        **kwargs,
    )


def build_diff_proposal_no_apply_guarantee(guarantee_id: str = "no_apply:v0.35.4", **kwargs: Any) -> DiffProposalNoApplyGuarantee:
    return DiffProposalNoApplyGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0354_VERSION), **kwargs)


def build_v0354_readiness_report(report_id: str = "readiness:v0.35.4", **kwargs: Any) -> V0354ReadinessReport:
    return V0354ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0354_VERSION),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        summary=kwargs.pop("summary", "v0.35.4 is ready for v0.35.5/v0.35.6 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["DiffProposalEnvelope", "UnifiedDiffProposal", "StructuredPatchProposal", "PatchFileProposal", "PatchHunkProposal"]),
        blocked_items=kwargs.pop("blocked_items", ["patch application", "workspace write", "code edit", "apply_patch", "git apply", "test execution", "shell execution"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.5 Patch Risk & Conformance Scanner", "v0.35.6 Human Review Packet"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0354_DOC_PATH, DEFAULT_V0353_PLAN_DOC_REF, DEFAULT_V0352_CONTEXT_DOC_REF, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any apply/write/edit/test/shell/reference execution path is introduced."]),
        **kwargs,
    )


def validate_patch_hunk_proposal(hunk: PatchHunkProposal) -> DiffProposalValidationReport:
    findings: list[DiffProposalValidationFinding] = []
    if hunk.ready_for_apply:
        findings.append(
            build_diff_proposal_validation_finding(
                "diff_finding:hunk_apply_ready",
                validation_kind=DiffProposalValidationKind.NO_APPLY_CHECK,
                decision_kind=DiffProposalDecisionKind.BLOCK,
                risk_kinds=[DiffProposalRiskKind.PATCH_APPLY_RISK],
                message="Hunk proposal cannot be ready for apply.",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_diff_proposal_validation_finding())
    return build_diff_proposal_validation_report(diff_envelope_id=None, findings=findings)


def validate_patch_file_proposal(file_proposal: PatchFileProposal) -> DiffProposalValidationReport:
    findings: list[DiffProposalValidationFinding] = []
    if not structured_patch_proposal_is_not_write(build_structured_patch_proposal(file_proposals=[file_proposal])):
        findings.append(
            build_diff_proposal_validation_finding(
                "diff_finding:file_write_ready",
                validation_kind=DiffProposalValidationKind.NO_WRITE_CHECK,
                decision_kind=DiffProposalDecisionKind.BLOCK,
                risk_kinds=[DiffProposalRiskKind.WORKSPACE_WRITE_RISK],
                message="File proposal cannot be ready for apply or write.",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_diff_proposal_validation_finding())
    return build_diff_proposal_validation_report(diff_envelope_id=None, findings=findings)


def validate_diff_proposal_envelope(envelope: DiffProposalEnvelope) -> DiffProposalValidationReport:
    findings: list[DiffProposalValidationFinding] = []
    if not diff_proposal_envelope_is_not_apply(envelope):
        findings.append(
            build_diff_proposal_validation_finding(
                "diff_finding:envelope_apply_ready",
                validation_kind=DiffProposalValidationKind.NO_APPLY_CHECK,
                decision_kind=DiffProposalDecisionKind.BLOCK,
                risk_kinds=[DiffProposalRiskKind.PATCH_APPLY_RISK, DiffProposalRiskKind.WORKSPACE_WRITE_RISK],
                message="Envelope cannot be apply/write/edit/execution ready.",
                blocks_validation=True,
            )
        )
    if envelope.gaps:
        findings.append(
            build_diff_proposal_validation_finding(
                "diff_finding:gaps",
                validation_kind=DiffProposalValidationKind.REVIEW_REQUIRED_CHECK,
                decision_kind=DiffProposalDecisionKind.REQUIRE_REVIEW,
                risk_kinds=[DiffProposalRiskKind.INSUFFICIENT_CONTEXT_RISK],
                message="Envelope contains gaps and requires review before future risk scan/review handoff.",
                blocks_validation=False,
            )
        )
    if not findings:
        findings.append(build_diff_proposal_validation_finding())
    return build_diff_proposal_validation_report(diff_envelope_id=envelope.diff_envelope_id, findings=findings)


def diff_proposal_flags_preserve_no_apply(flags: DiffProposalFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_DIFF_PROPOSAL_FLAG_NAMES) and flags.production_certified is False


def diff_proposal_policy_blocks_apply(policy: DiffProposalGenerationPolicy) -> bool:
    return (
        policy.require_no_apply is True
        and policy.require_no_write is True
        and policy.allow_patch_apply is False
        and policy.allow_workspace_write is False
        and policy.allow_code_edit is False
        and policy.allow_test_execution is False
        and policy.allow_shell is False
        and policy.allow_dependency_install is False
    )


def unified_diff_proposal_is_not_git_apply(diff: UnifiedDiffProposal) -> bool:
    return diff.ready_for_apply is False and diff.ready_for_git_apply is False


def structured_patch_proposal_is_not_write(proposal: StructuredPatchProposal) -> bool:
    return proposal.ready_for_apply is False and proposal.ready_for_write is False and all(file.ready_for_apply is False and file.ready_for_write is False for file in proposal.file_proposals)


def diff_proposal_envelope_is_not_apply(envelope: DiffProposalEnvelope) -> bool:
    return envelope.ready_for_patch_application is False and envelope.ready_for_workspace_write is False and envelope.ready_for_code_edit is False and envelope.ready_for_execution is False


def v0354_readiness_report_is_not_execution_ready(report: V0354ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_DIFF_PROPOSAL_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
