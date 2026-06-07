from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any

from .boundary import _metadata_flag_true, _require_non_blank, _validate_string_list


V0350_VERSION = "v0.35.0"
V0350_RELEASE_NAME = "v0.35.0 Controlled Patch Proposal Boundary Foundation"
V035_TRACK_NAME = "Controlled Patch Proposal Layer"

DEFAULT_DIGEST_DOC_PATH = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"
DEFAULT_BOUNDARY_DOC_PATH = "docs/versions/v0.35/v0.35.0_controlled_patch_proposal_boundary.md"

DEFAULT_ALLOWED_REFERENCE_ROOTS = ["references/OpenCode", "references/Hermes", "references/OpenClaw"]
DEFAULT_BLOCKED_FILE_PATTERNS = [".env", "secret", "key", "token", "credential", ".pem", "id_rsa", "id_ed25519"]
DEFAULT_ALLOWED_FILE_PATTERNS = [".md", ".txt", ".py", ".ts", ".tsx", ".json", ".yaml", ".yml", ".toml", ".mdx"]
DEFAULT_PROHIBITED_RUNTIME_ACTIONS = [
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
    "general_agent_execution",
    "autonomous_agent_runtime",
    "general_tool_execution",
    "unquarantined_action_execution",
    "persistent_trace_write",
    "ui_runtime",
    "external_control",
    "authority_grant",
]
DEFAULT_WITHDRAWAL_CONDITIONS = [
    "Any runtime patch application, workspace write, code edit, apply_patch, or git apply path is introduced.",
    "Any shell, subprocess, command, test, dependency install, provider, network, credential, or secret path is introduced.",
    "Any reference execution/import/install path is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]
DEFAULT_V035_ROADMAP = [
    "v0.35.0 Controlled Patch Proposal Boundary Foundation",
    "v0.35.1 Patch Intent & Scope Policy",
    "v0.35.2 Read-only Patch Context & Reference Corpus Collector",
    "v0.35.3 Reference-informed Patch Plan & Change Set Graph",
    "v0.35.4 Diff Proposal Envelope",
    "v0.35.5 Patch Risk & Conformance Scanner",
    "v0.35.6 Human Review Packet & Approval Gate Metadata",
    "v0.35.7 Patch Proposal OCEL Trace Packet",
    "v0.35.8 CLI Patch Proposal Surface",
    "v0.35.9 Controlled Patch Proposal Layer Consolidation",
]

UNSAFE_PATCH_FLAG_NAMES = (
    "ready_for_execution",
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
    "ready_for_persistent_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class ControlledPatchProposalTrackKind(StrEnum):
    BOUNDARY_FOUNDATION = "boundary_foundation"
    PATCH_INTENT_SCOPE_POLICY = "patch_intent_scope_policy"
    READONLY_PATCH_CONTEXT_COLLECTOR = "readonly_patch_context_collector"
    REFERENCE_INFORMED_PATCH_PLAN = "reference_informed_patch_plan"
    DIFF_PROPOSAL_ENVELOPE = "diff_proposal_envelope"
    PATCH_RISK_CONFORMANCE_SCANNER = "patch_risk_conformance_scanner"
    HUMAN_REVIEW_PACKET = "human_review_packet"
    PATCH_PROPOSAL_OCEL_TRACE_PACKET = "patch_proposal_ocel_trace_packet"
    CLI_PATCH_PROPOSAL_SURFACE = "cli_patch_proposal_surface"
    CONSOLIDATION = "consolidation"
    UNKNOWN = "unknown"


class PatchProposalSurfaceKind(StrEnum):
    PATCH_INTENT = "patch_intent"
    PATCH_SCOPE_POLICY = "patch_scope_policy"
    READONLY_CONTEXT_SNAPSHOT = "readonly_context_snapshot"
    REFERENCE_PATTERN_DIGEST = "reference_pattern_digest"
    PATCH_PLAN = "patch_plan"
    CHANGE_SET_GRAPH = "change_set_graph"
    DIFF_PROPOSAL_ENVELOPE = "diff_proposal_envelope"
    UNIFIED_DIFF_TEXT = "unified_diff_text"
    STRUCTURED_PATCH_PROPOSAL = "structured_patch_proposal"
    PATCH_RISK_REPORT = "patch_risk_report"
    HUMAN_REVIEW_PACKET = "human_review_packet"
    APPROVAL_METADATA = "approval_metadata"
    PATCH_APPLY = "patch_apply"
    FILE_WRITE = "file_write"
    CODE_EDIT = "code_edit"
    GIT_APPLY = "git_apply"
    APPLY_PATCH = "apply_patch"
    SHELL_COMMAND = "shell_command"
    TEST_EXECUTION = "test_execution"
    DEPENDENCY_INSTALL = "dependency_install"
    REFERENCE_CODE_EXECUTION = "reference_code_execution"
    PROVIDER_INVOCATION = "provider_invocation"
    CREDENTIAL_ACCESS = "credential_access"
    UI_RUNTIME = "ui_runtime"
    UNKNOWN = "unknown"


class PatchProposalCapabilityKind(StrEnum):
    DEFINE_BOUNDARY = "define_boundary"
    INSPECT_REFERENCE_CORPUS_READONLY = "inspect_reference_corpus_readonly"
    CREATE_REFERENCE_PATTERN_DIGEST = "create_reference_pattern_digest"
    DEFINE_PATCH_INTENT_POLICY = "define_patch_intent_policy"
    DEFINE_PATCH_SCOPE_POLICY = "define_patch_scope_policy"
    COLLECT_READONLY_PATCH_CONTEXT = "collect_readonly_patch_context"
    CREATE_PATCH_PLAN = "create_patch_plan"
    CREATE_CHANGE_SET_GRAPH = "create_change_set_graph"
    CREATE_DIFF_PROPOSAL_ARTIFACT = "create_diff_proposal_artifact"
    SCAN_PATCH_RISK = "scan_patch_risk"
    CREATE_HUMAN_REVIEW_PACKET = "create_human_review_packet"
    CREATE_PATCH_PROPOSAL_TRACE_PACKET = "create_patch_proposal_trace_packet"
    CLI_PATCH_PROPOSAL_PREVIEW = "cli_patch_proposal_preview"
    EXECUTE_PATCH_APPLY = "execute_patch_apply"
    WRITE_WORKSPACE_FILE = "write_workspace_file"
    EDIT_CODE_FILE = "edit_code_file"
    RUN_GIT_APPLY = "run_git_apply"
    RUN_APPLY_PATCH = "run_apply_patch"
    RUN_TESTS = "run_tests"
    EXECUTE_SHELL = "execute_shell"
    INSTALL_DEPENDENCY = "install_dependency"
    EXECUTE_REFERENCE_HARNESS = "execute_reference_harness"
    READ_SECRET = "read_secret"
    ACCESS_CREDENTIAL = "access_credential"
    UNKNOWN = "unknown"


class PatchProposalRiskKind(StrEnum):
    PATCH_APPLY_RISK = "patch_apply_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    SCOPE_ESCAPE_RISK = "scope_escape_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    UNSAFE_READINESS_FLAG_RISK = "unsafe_readiness_flag_risk"
    PROVIDER_NETWORK_OPENING_RISK = "provider_network_opening_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    SUBPROCESS_EXECUTION_RISK = "subprocess_execution_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    REFERENCE_IMPORT_RISK = "reference_import_risk"
    COPIED_CODE_RISK = "copied_code_risk"
    LICENSE_OR_ATTRIBUTION_RISK = "license_or_attribution_risk"
    UNSAFE_DIFF_GENERATION_RISK = "unsafe_diff_generation_risk"
    UNBOUNDED_CONTEXT_RISK = "unbounded_context_risk"
    RAW_SOURCE_DUMP_RISK = "raw_source_dump_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class PatchProposalDecisionKind(StrEnum):
    ALLOW_BOUNDARY_DEFINITION = "allow_boundary_definition"
    ALLOW_REFERENCE_DIGEST_GENERATION = "allow_reference_digest_generation"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchProposalBoundaryStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_READY = "boundary_ready"
    BOUNDARY_READY_WITH_GAPS = "boundary_ready_with_gaps"
    DIGEST_CREATED = "digest_created"
    DIGEST_CREATED_WITH_GAPS = "digest_created_with_gaps"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class PatchProposalReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_CONTRACT_READY = "boundary_contract_ready"
    REFERENCE_DIGEST_READY = "reference_digest_ready"
    DESIGN_HANDOFF_READY_FOR_V0351 = "design_handoff_ready_for_v0351"
    DESIGN_HANDOFF_READY_FOR_V0352 = "design_handoff_ready_for_v0352"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchWritePosture(StrEnum):
    NO_WRITE = "no_write"
    PROPOSAL_ARTIFACT_ONLY = "proposal_artifact_only"
    REVIEW_METADATA_ONLY = "review_metadata_only"
    FUTURE_APPLY_SANDBOX = "future_apply_sandbox"
    WRITE_BLOCKED = "write_blocked"
    UNKNOWN = "unknown"


class PatchApplyPosture(StrEnum):
    NO_APPLY = "no_apply"
    APPLY_BLOCKED = "apply_blocked"
    APPROVAL_METADATA_ONLY = "approval_metadata_only"
    FUTURE_HUMAN_APPROVED_APPLY_SANDBOX = "future_human_approved_apply_sandbox"
    UNKNOWN = "unknown"


class ReferenceCorpusKind(StrEnum):
    OPENCODE = "opencode"
    HERMES = "hermes"
    OPENCLAW = "openclaw"
    GENERIC_REFERENCE_HARNESS = "generic_reference_harness"
    MISSING_REFERENCE = "missing_reference"
    UNKNOWN = "unknown"


class ReferenceCorpusInspectionStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_FOUND = "not_found"
    FOUND = "found"
    PARTIALLY_INSPECTED = "partially_inspected"
    INSPECTED_READONLY = "inspected_readonly"
    SKIPPED_TOO_LARGE = "skipped_too_large"
    BLOCKED_SECRET_LIKE = "blocked_secret_like"
    BLOCKED_UNSAFE = "blocked_unsafe"
    FAILED_SAFE = "failed_safe"


class ReferenceHarnessPatternKind(StrEnum):
    CLI_SURFACE_PATTERN = "cli_surface_pattern"
    AGENT_LOOP_PATTERN = "agent_loop_pattern"
    CONTEXT_COLLECTION_PATTERN = "context_collection_pattern"
    TOOL_REGISTRY_PATTERN = "tool_registry_pattern"
    PERMISSION_GATE_PATTERN = "permission_gate_pattern"
    FILE_EDIT_PLANNING_PATTERN = "file_edit_planning_pattern"
    DIFF_PROPOSAL_PATTERN = "diff_proposal_pattern"
    REVIEW_WORKFLOW_PATTERN = "review_workflow_pattern"
    LOGGING_TRACE_SESSION_PATTERN = "logging_trace_session_pattern"
    FAILURE_HANDLING_PATTERN = "failure_handling_pattern"
    UNSAFE_EXECUTION_PATTERN = "unsafe_execution_pattern"
    REJECTED_PATTERN = "rejected_pattern"
    FUTURE_TRACK_PATTERN = "future_track_pattern"
    UNKNOWN = "unknown"


class ReferencePatternDisposition(StrEnum):
    OBSERVED = "observed"
    ADAPTED_TO_CHANTACORE = "adapted_to_chantacore"
    REJECTED_FOR_SAFETY = "rejected_for_safety"
    FUTURE_TRACK = "future_track"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    UNKNOWN = "unknown"


def _validate_version_includes_v0350(version: str) -> None:
    _require_non_blank("version", version)
    if V0350_VERSION not in version:
        raise ValueError("version must include v0.35.0")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict) or not all(isinstance(key, str) for key in value):
        raise TypeError(f"{name} must be dict[str, Any]")


def _validate_non_negative_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.0")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must be True in v0.35.0")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "runtime_patch_apply",
            "runtime_file_write",
            "runtime_code_edit",
            "patch_proposal_generation",
            "shell_execution",
            "reference_execution",
            "reference_import",
            "dependency_install",
            "provider_invocation",
            "network_access",
            "credential_access",
            "secret_read",
            "authority_grant",
        },
    ):
        raise ValueError("v0.35.0 metadata cannot imply runtime patch/write/execution authority")


def _validate_object_list(name: str, values: list[Any], expected_type: type) -> None:
    if not isinstance(values, list) or not all(isinstance(item, expected_type) for item in values):
        raise TypeError(f"{name} must be list[{expected_type.__name__}]")


def _enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


@dataclass(frozen=True)
class ControlledPatchProposalFlagSet:
    flag_set_id: str
    version: str = V0350_VERSION
    patch_proposal_boundary_constructed: bool = False
    reference_corpus_policy_defined: bool = False
    reference_pattern_digest_created: bool = False
    patch_proposal_surface_policy_defined: bool = False
    patch_proposal_risk_register_defined: bool = False
    ready_for_v0351_patch_intent_scope_policy: bool = False
    ready_for_v0352_readonly_patch_context_collector: bool = False
    ready_for_reference_pattern_digest: bool = False
    ready_for_execution: bool = False
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
    ready_for_persistent_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0350(self.version)
        _validate_false(self, UNSAFE_PATCH_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.35.0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalSourceRef:
    source_ref_id: str
    source_kind: "ControlledPatchProposalSourceKind | str"
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ControlledPatchProposalSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


class ControlledPatchProposalSourceKind(StrEnum):
    V0349_HANDOFF_PACKET = "v0349_handoff_packet"
    V0348_CLI_MODEL_BACKED_SURFACE = "v0348_cli_model_backed_surface"
    V0346_MODEL_BACKED_STEP = "v0346_model_backed_step"
    V0335_WORKSPACE_INSPECTION_TOOL_PACK = "v0335_workspace_inspection_tool_pack"
    REFERENCE_CORPUS_OPENCODE = "reference_corpus_opencode"
    REFERENCE_CORPUS_HERMES = "reference_corpus_hermes"
    REFERENCE_CORPUS_OPENCLAW = "reference_corpus_openclaw"
    REFERENCE_PATTERN_DIGEST_DOC = "reference_pattern_digest_doc"
    MANUAL_DESIGN_NOTE = "manual_design_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ReferenceCorpusInspectionPolicy:
    policy_id: str
    allowed_reference_roots: list[str] = field(default_factory=lambda: list(DEFAULT_ALLOWED_REFERENCE_ROOTS))
    blocked_reference_roots: list[str] = field(default_factory=list)
    allowed_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_ALLOWED_FILE_PATTERNS))
    blocked_file_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_BLOCKED_FILE_PATTERNS))
    max_files_per_corpus: int = 80
    max_file_chars: int = 6000
    max_excerpt_chars: int = 320
    allow_execution: bool = False
    allow_import: bool = False
    allow_dependency_install: bool = False
    allow_test_run: bool = False
    allow_shell: bool = False
    allow_secret_file_read: bool = False
    allow_raw_source_dump: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        for name in ("allowed_reference_roots", "blocked_reference_roots", "allowed_file_patterns", "blocked_file_patterns"):
            _validate_string_list(name, getattr(self, name))
        for name in ("max_files_per_corpus", "max_file_chars", "max_excerpt_chars"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("allow_execution", "allow_import", "allow_dependency_install", "allow_test_run", "allow_shell", "allow_secret_file_read", "allow_raw_source_dump"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ReferenceCorpusInventory:
    inventory_id: str
    corpus_kind: ReferenceCorpusKind | str
    root_path_ref: str
    inspection_status: ReferenceCorpusInspectionStatus | str
    inspected_file_refs: list[str] = field(default_factory=list)
    skipped_file_refs: list[str] = field(default_factory=list)
    skipped_reasons: list[str] = field(default_factory=list)
    package_or_config_refs: list[str] = field(default_factory=list)
    doc_refs: list[str] = field(default_factory=list)
    source_refs: list[str] = field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("inventory_id", self.inventory_id)
        ReferenceCorpusKind(self.corpus_kind)
        _require_non_blank("root_path_ref", self.root_path_ref)
        ReferenceCorpusInspectionStatus(self.inspection_status)
        for name in ("inspected_file_refs", "skipped_file_refs", "skipped_reasons", "package_or_config_refs", "doc_refs", "source_refs"):
            _validate_string_list(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _validate_metadata_safe(self.metadata)

    @property
    def import_or_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferenceHarnessPattern:
    pattern_id: str
    corpus_kind: ReferenceCorpusKind | str
    pattern_kind: ReferenceHarnessPatternKind | str
    disposition: ReferencePatternDisposition | str
    pattern_summary: str
    observed_evidence_refs: list[str] = field(default_factory=list)
    chantacore_adaptation: str = ""
    rejection_reason: str | None = None
    future_track_note: str | None = None
    confidence: str = "medium"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("pattern_id", self.pattern_id)
        ReferenceCorpusKind(self.corpus_kind)
        ReferenceHarnessPatternKind(self.pattern_kind)
        disposition = ReferencePatternDisposition(self.disposition)
        _require_non_blank("pattern_summary", self.pattern_summary)
        _validate_string_list("observed_evidence_refs", self.observed_evidence_refs)
        _require_non_blank("confidence", self.confidence)
        if disposition == ReferencePatternDisposition.REJECTED_FOR_SAFETY and not self.rejection_reason:
            raise ValueError("rejected patterns must have rejection_reason")
        if disposition == ReferencePatternDisposition.FUTURE_TRACK and not self.future_track_note:
            raise ValueError("future-track patterns should have future_track_note")
        _validate_metadata_safe(self.metadata)

    @property
    def copied_implementation(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferencePatternDigest:
    digest_id: str
    version: str
    digest_doc_path: str
    corpus_inventories: list[ReferenceCorpusInventory]
    patterns: list[ReferenceHarnessPattern]
    adaptation_summary: str
    rejected_pattern_count: int
    future_track_count: int
    no_execution_confirmed: bool
    no_import_confirmed: bool
    no_install_confirmed: bool
    no_test_run_confirmed: bool
    no_secret_read_confirmed: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("digest_id", self.digest_id)
        _validate_version_includes_v0350(self.version)
        _require_non_blank("digest_doc_path", self.digest_doc_path)
        _validate_object_list("corpus_inventories", self.corpus_inventories, ReferenceCorpusInventory)
        _validate_object_list("patterns", self.patterns, ReferenceHarnessPattern)
        _require_non_blank("adaptation_summary", self.adaptation_summary)
        _validate_non_negative_int("rejected_pattern_count", self.rejected_pattern_count)
        _validate_non_negative_int("future_track_count", self.future_track_count)
        _validate_true(self, ("no_execution_confirmed", "no_import_confirmed", "no_install_confirmed", "no_test_run_confirmed", "no_secret_read_confirmed"))
        _require_non_blank("summary", self.summary)
        _validate_metadata_safe(self.metadata)

    @property
    def executable(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferencePatternAdaptationMap:
    adaptation_map_id: str
    version: str
    source_pattern_ids: list[str] = field(default_factory=list)
    adapted_to_v035_artifacts: dict[str, str] = field(default_factory=dict)
    rejected_pattern_ids: list[str] = field(default_factory=list)
    future_track_pattern_ids: list[str] = field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("adaptation_map_id", self.adaptation_map_id)
        _validate_version_includes_v0350(self.version)
        for name in ("source_pattern_ids", "rejected_pattern_ids", "future_track_pattern_ids"):
            _validate_string_list(name, getattr(self, name))
        _validate_dict("adapted_to_v035_artifacts", self.adapted_to_v035_artifacts)
        if not all(isinstance(value, str) for value in self.adapted_to_v035_artifacts.values()):
            raise TypeError("adapted_to_v035_artifacts must be dict[str, str]")
        _require_non_blank("summary", self.summary)
        _validate_metadata_safe(self.metadata)

    @property
    def implementation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ReferencePatternRejectionRecord:
    rejection_id: str
    pattern_id: str | None
    corpus_kind: ReferenceCorpusKind | str
    rejected_surface: str
    risk_kinds: list[PatchProposalRiskKind | str]
    reason: str
    safe_alternative: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("rejection_id", self.rejection_id)
        if self.pattern_id is not None:
            _require_non_blank("pattern_id", self.pattern_id)
        ReferenceCorpusKind(self.corpus_kind)
        _require_non_blank("rejected_surface", self.rejected_surface)
        _enum_list("risk_kinds", self.risk_kinds, PatchProposalRiskKind)
        _require_non_blank("reason", self.reason)
        _require_non_blank("safe_alternative", self.safe_alternative)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchProposalSurfacePolicy:
    policy_id: str
    write_posture: PatchWritePosture | str = PatchWritePosture.NO_WRITE
    apply_posture: PatchApplyPosture | str = PatchApplyPosture.NO_APPLY
    allowed_surfaces: list[PatchProposalSurfaceKind | str] = field(default_factory=list)
    prohibited_surfaces: list[PatchProposalSurfaceKind | str] = field(default_factory=list)
    prohibited_capabilities: list[PatchProposalCapabilityKind | str] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    allow_reference_digest: bool = False
    allow_patch_intent_artifact: bool = False
    allow_patch_scope_policy: bool = False
    allow_patch_context_collection_future_gate: bool = False
    allow_patch_plan_future_gate: bool = False
    allow_diff_proposal_future_gate: bool = False
    allow_patch_risk_scan_future_gate: bool = False
    allow_human_review_packet_future_gate: bool = False
    allow_patch_apply: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_shell: bool = False
    allow_test_execution: bool = False
    allow_dependency_install: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        PatchWritePosture(self.write_posture)
        PatchApplyPosture(self.apply_posture)
        _enum_list("allowed_surfaces", self.allowed_surfaces, PatchProposalSurfaceKind)
        _enum_list("prohibited_surfaces", self.prohibited_surfaces, PatchProposalSurfaceKind)
        _enum_list("prohibited_capabilities", self.prohibited_capabilities, PatchProposalCapabilityKind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        for name in ("allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_shell", "allow_test_execution", "allow_dependency_install"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalAllowedSurface:
    allowed_surface_id: str
    surface_kind: PatchProposalSurfaceKind | str
    capability_kind: PatchProposalCapabilityKind | str
    description: str
    allowed_only_for_design_stage: bool = True
    executable_in_v0350: bool = False
    writes_files: bool = False
    applies_patch: bool = False
    source_refs: list[ControlledPatchProposalSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("allowed_surface_id", self.allowed_surface_id)
        PatchProposalSurfaceKind(self.surface_kind)
        PatchProposalCapabilityKind(self.capability_kind)
        _require_non_blank("description", self.description)
        if self.executable_in_v0350 is not False or self.writes_files is not False or self.applies_patch is not False:
            raise ValueError("v0.35.0 allowed surfaces cannot be executable, write files, or apply patches")
        _validate_object_list("source_refs", self.source_refs, ControlledPatchProposalSourceRef)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalProhibitedSurface:
    prohibited_surface_id: str
    surface_kind: PatchProposalSurfaceKind | str
    risk_kind: PatchProposalRiskKind | str
    capability_kind: PatchProposalCapabilityKind | str
    reason: str
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    blocks_apply: bool = True
    blocks_write: bool = True
    blocks_runtime_readiness: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("prohibited_surface_id", self.prohibited_surface_id)
        PatchProposalSurfaceKind(self.surface_kind)
        PatchProposalRiskKind(self.risk_kind)
        PatchProposalCapabilityKind(self.capability_kind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_true(self, ("blocks_apply", "blocks_write", "blocks_runtime_readiness"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalBoundary:
    boundary_id: str
    version: str
    release_name: str
    surface_policy: PatchProposalSurfacePolicy
    reference_inspection_policy: ReferenceCorpusInspectionPolicy
    reference_digest: ReferencePatternDigest | None
    allowed_surfaces: list[ControlledPatchProposalAllowedSurface]
    prohibited_surfaces: list[ControlledPatchProposalProhibitedSurface]
    flags: ControlledPatchProposalFlagSet
    status: PatchProposalBoundaryStatus | str
    readiness_level: PatchProposalReadinessLevel | str
    summary: str
    gaps: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_WITHDRAWAL_CONDITIONS))
    ready_for_v0351_patch_intent_scope_policy: bool = False
    ready_for_v0352_readonly_patch_context_collector: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version_includes_v0350(self.version)
        _require_non_blank("release_name", self.release_name)
        if not isinstance(self.surface_policy, PatchProposalSurfacePolicy):
            raise TypeError("surface_policy must be PatchProposalSurfacePolicy")
        if not isinstance(self.reference_inspection_policy, ReferenceCorpusInspectionPolicy):
            raise TypeError("reference_inspection_policy must be ReferenceCorpusInspectionPolicy")
        if self.reference_digest is not None and not isinstance(self.reference_digest, ReferencePatternDigest):
            raise TypeError("reference_digest must be ReferencePatternDigest or None")
        _validate_object_list("allowed_surfaces", self.allowed_surfaces, ControlledPatchProposalAllowedSurface)
        _validate_object_list("prohibited_surfaces", self.prohibited_surfaces, ControlledPatchProposalProhibitedSurface)
        if not isinstance(self.flags, ControlledPatchProposalFlagSet):
            raise TypeError("flags must be ControlledPatchProposalFlagSet")
        if not controlled_patch_proposal_flags_preserve_no_apply(self.flags):
            raise ValueError("flags must preserve no apply/write/execution")
        PatchProposalBoundaryStatus(self.status)
        PatchProposalReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_patch_proposal or self.ready_for_patch_application or self.ready_for_workspace_write or self.ready_for_code_edit or self.ready_for_execution:
            raise ValueError("v0.35.0 boundary cannot be ready for proposal generation, apply, write, edit, or execution")
        _validate_metadata_safe(self.metadata)

    @property
    def patch_proposal_generation(self) -> bool:
        return False

    @property
    def patch_application(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledPatchProposalPermissionRequest:
    request_id: str
    surface_kind: PatchProposalSurfaceKind | str
    capability_kind: PatchProposalCapabilityKind | str
    requested_action: str
    source_refs: list[ControlledPatchProposalSourceRef] = field(default_factory=list)
    summary: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("request_id", self.request_id)
        PatchProposalSurfaceKind(self.surface_kind)
        PatchProposalCapabilityKind(self.capability_kind)
        _require_non_blank("requested_action", self.requested_action)
        _validate_object_list("source_refs", self.source_refs, ControlledPatchProposalSourceRef)
        _require_non_blank("summary", self.summary)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalPermissionDecision:
    decision_id: str
    request_id: str
    decision_kind: PatchProposalDecisionKind | str
    reason: str
    risk_kinds: list[PatchProposalRiskKind | str] = field(default_factory=list)
    patch_apply_allowed: bool = False
    workspace_write_allowed: bool = False
    code_edit_allowed: bool = False
    shell_allowed: bool = False
    test_execution_allowed: bool = False
    dependency_install_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("request_id", self.request_id)
        PatchProposalDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _enum_list("risk_kinds", self.risk_kinds, PatchProposalRiskKind)
        for name in ("patch_apply_allowed", "workspace_write_allowed", "code_edit_allowed", "shell_allowed", "test_execution_allowed", "dependency_install_allowed"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.0")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalDeniedAction:
    denied_action_id: str
    request_id: str | None
    decision_id: str | None
    surface_kind: PatchProposalSurfaceKind | str
    risk_kinds: list[PatchProposalRiskKind | str]
    reason: str
    safe_alternatives: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_action_id", self.denied_action_id)
        if self.request_id is not None:
            _require_non_blank("request_id", self.request_id)
        if self.decision_id is not None:
            _require_non_blank("decision_id", self.decision_id)
        PatchProposalSurfaceKind(self.surface_kind)
        _enum_list("risk_kinds", self.risk_kinds, PatchProposalRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalGateEvaluation:
    gate_evaluation_id: str
    request_id: str
    decision: ControlledPatchProposalPermissionDecision
    denied_action: ControlledPatchProposalDeniedAction | None
    status: PatchProposalBoundaryStatus | str
    summary: str
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gate_evaluation_id", self.gate_evaluation_id)
        _require_non_blank("request_id", self.request_id)
        if not isinstance(self.decision, ControlledPatchProposalPermissionDecision):
            raise TypeError("decision must be ControlledPatchProposalPermissionDecision")
        if self.denied_action is not None and not isinstance(self.denied_action, ControlledPatchProposalDeniedAction):
            raise TypeError("denied_action must be ControlledPatchProposalDeniedAction or None")
        PatchProposalBoundaryStatus(self.status)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution or self.ready_for_patch_application:
            raise ValueError("gate evaluation cannot enable execution or patch application")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalRiskRegister:
    risk_register_id: str
    version: str
    risk_kinds: list[PatchProposalRiskKind | str] = field(default_factory=list)
    high_risk_surfaces: list[PatchProposalSurfaceKind | str] = field(default_factory=list)
    mitigations: list[str] = field(default_factory=list)
    unresolved_risks: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version_includes_v0350(self.version)
        _enum_list("risk_kinds", self.risk_kinds, PatchProposalRiskKind)
        _enum_list("high_risk_surfaces", self.high_risk_surfaces, PatchProposalSurfaceKind)
        for name in ("mitigations", "unresolved_risks", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        required = {
            PatchProposalRiskKind.PATCH_APPLY_RISK,
            PatchProposalRiskKind.WORKSPACE_WRITE_RISK,
            PatchProposalRiskKind.CODE_EDIT_RISK,
            PatchProposalRiskKind.SHELL_EXECUTION_RISK,
            PatchProposalRiskKind.TEST_EXECUTION_RISK,
            PatchProposalRiskKind.DEPENDENCY_INSTALL_RISK,
            PatchProposalRiskKind.REFERENCE_EXECUTION_RISK,
            PatchProposalRiskKind.REFERENCE_IMPORT_RISK,
            PatchProposalRiskKind.SECRET_EXPOSURE_RISK,
            PatchProposalRiskKind.SCOPE_ESCAPE_RISK,
        }
        if not required.issubset({PatchProposalRiskKind(value) for value in self.risk_kinds}):
            raise ValueError("risk_register must include apply/write/edit/shell/test/install/reference/secret/scope risks")
        _validate_metadata_safe(self.metadata)

    @property
    def permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ControlledPatchProposalNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_patch_proposal_generation: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_test_execution: bool = True
    no_dependency_install: bool = True
    no_reference_execution: bool = True
    no_reference_import: bool = True
    no_reference_install: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
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
        _validate_version_includes_v0350(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V035RoadmapOverview:
    roadmap_id: str
    version: str
    track_name: str
    stages: list[str]
    summary: str
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("roadmap_id", self.roadmap_id)
        _validate_version_includes_v0350(self.version)
        _require_non_blank("track_name", self.track_name)
        _validate_string_list("stages", self.stages)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution or self.ready_for_patch_application:
            raise ValueError("roadmap is not execution or patch application readiness")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0350ReadinessReport:
    report_id: str
    version: str
    boundary_id: str | None
    digest_id: str | None
    summary: str
    readiness_level: PatchProposalReadinessLevel | str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    ready_for_v0351_patch_intent_scope_policy: bool = False
    ready_for_v0352_readonly_patch_context_collector: bool = False
    ready_for_reference_pattern_digest: bool = False
    ready_for_execution: bool = False
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
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0350(self.version)
        if self.boundary_id is not None:
            _require_non_blank("boundary_id", self.boundary_id)
        if self.digest_id is not None:
            _require_non_blank("digest_id", self.digest_id)
        _require_non_blank("summary", self.summary)
        PatchProposalReadinessLevel(self.readiness_level)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        for name in (
            "ready_for_execution",
            "ready_for_patch_proposal",
            "ready_for_patch_application",
            "ready_for_workspace_write",
            "ready_for_code_edit",
            "ready_for_apply_patch",
            "ready_for_git_apply",
            "ready_for_test_execution",
            "ready_for_shell_execution",
            "ready_for_dependency_install",
            "ready_for_reference_execution",
            "ready_for_reference_import",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.0")
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_controlled_patch_proposal_flags(flag_set_id: str = "patch_proposal_flags:v0.35.0", **kwargs: Any) -> ControlledPatchProposalFlagSet:
    return ControlledPatchProposalFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0350_VERSION),
        patch_proposal_boundary_constructed=kwargs.pop("patch_proposal_boundary_constructed", True),
        reference_corpus_policy_defined=kwargs.pop("reference_corpus_policy_defined", True),
        reference_pattern_digest_created=kwargs.pop("reference_pattern_digest_created", True),
        patch_proposal_surface_policy_defined=kwargs.pop("patch_proposal_surface_policy_defined", True),
        patch_proposal_risk_register_defined=kwargs.pop("patch_proposal_risk_register_defined", True),
        ready_for_v0351_patch_intent_scope_policy=kwargs.pop("ready_for_v0351_patch_intent_scope_policy", True),
        ready_for_v0352_readonly_patch_context_collector=kwargs.pop("ready_for_v0352_readonly_patch_context_collector", True),
        ready_for_reference_pattern_digest=kwargs.pop("ready_for_reference_pattern_digest", True),
        **kwargs,
    )


def build_controlled_patch_proposal_source_ref(source_ref_id: str = "source:v0.35.0", **kwargs: Any) -> ControlledPatchProposalSourceRef:
    return ControlledPatchProposalSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", ControlledPatchProposalSourceKind.MANUAL_DESIGN_NOTE),
        source_id=kwargs.pop("source_id", "v0.35.0"),
        source_summary=kwargs.pop("source_summary", "Controlled patch proposal boundary source metadata."),
        **kwargs,
    )


def build_reference_corpus_inspection_policy(policy_id: str = "reference_policy:v0.35.0", **kwargs: Any) -> ReferenceCorpusInspectionPolicy:
    return ReferenceCorpusInspectionPolicy(policy_id=policy_id, **kwargs)


def build_reference_corpus_inventory(inventory_id: str = "inventory:reference:v0.35.0", **kwargs: Any) -> ReferenceCorpusInventory:
    return ReferenceCorpusInventory(
        inventory_id=inventory_id,
        corpus_kind=kwargs.pop("corpus_kind", ReferenceCorpusKind.MISSING_REFERENCE),
        root_path_ref=kwargs.pop("root_path_ref", "references/missing"),
        inspection_status=kwargs.pop("inspection_status", ReferenceCorpusInspectionStatus.NOT_FOUND),
        summary=kwargs.pop("summary", "Reference corpus was not found."),
        **kwargs,
    )


def build_reference_harness_pattern(pattern_id: str = "pattern:reference:v0.35.0", **kwargs: Any) -> ReferenceHarnessPattern:
    return ReferenceHarnessPattern(
        pattern_id=pattern_id,
        corpus_kind=kwargs.pop("corpus_kind", ReferenceCorpusKind.GENERIC_REFERENCE_HARNESS),
        pattern_kind=kwargs.pop("pattern_kind", ReferenceHarnessPatternKind.CLI_SURFACE_PATTERN),
        disposition=kwargs.pop("disposition", ReferencePatternDisposition.OBSERVED),
        pattern_summary=kwargs.pop("pattern_summary", "Observed reference pattern summarized as bounded metadata."),
        observed_evidence_refs=kwargs.pop("observed_evidence_refs", []),
        chantacore_adaptation=kwargs.pop("chantacore_adaptation", "Adapt only as v0.35 design metadata."),
        **kwargs,
    )


def build_reference_pattern_digest(digest_id: str = "reference_pattern_digest:v0.35.0", **kwargs: Any) -> ReferencePatternDigest:
    patterns = kwargs.pop(
        "patterns",
        [
            build_reference_harness_pattern("pattern:opencode:cli", corpus_kind=ReferenceCorpusKind.OPENCODE, pattern_kind=ReferenceHarnessPatternKind.CLI_SURFACE_PATTERN, observed_evidence_refs=["references/OpenCode/notes/01_codebase_structure_map.md"]),
            build_reference_harness_pattern("pattern:hermes:approval", corpus_kind=ReferenceCorpusKind.HERMES, pattern_kind=ReferenceHarnessPatternKind.PERMISSION_GATE_PATTERN, observed_evidence_refs=["references/Hermes/hermes-agent/acp_adapter/edit_approval.py"]),
        ],
    )
    rejected = sum(1 for item in patterns if ReferencePatternDisposition(item.disposition) == ReferencePatternDisposition.REJECTED_FOR_SAFETY)
    future = sum(1 for item in patterns if ReferencePatternDisposition(item.disposition) == ReferencePatternDisposition.FUTURE_TRACK)
    return ReferencePatternDigest(
        digest_id=digest_id,
        version=kwargs.pop("version", V0350_VERSION),
        digest_doc_path=kwargs.pop("digest_doc_path", DEFAULT_DIGEST_DOC_PATH),
        corpus_inventories=kwargs.pop("corpus_inventories", [build_reference_corpus_inventory()]),
        patterns=patterns,
        adaptation_summary=kwargs.pop("adaptation_summary", "Reference patterns inform v0.35 metadata only; no reference code is copied or executed."),
        rejected_pattern_count=kwargs.pop("rejected_pattern_count", rejected),
        future_track_count=kwargs.pop("future_track_count", future),
        no_execution_confirmed=kwargs.pop("no_execution_confirmed", True),
        no_import_confirmed=kwargs.pop("no_import_confirmed", True),
        no_install_confirmed=kwargs.pop("no_install_confirmed", True),
        no_test_run_confirmed=kwargs.pop("no_test_run_confirmed", True),
        no_secret_read_confirmed=kwargs.pop("no_secret_read_confirmed", True),
        summary=kwargs.pop("summary", "Bounded read-only reference pattern digest."),
        **kwargs,
    )


def build_reference_pattern_adaptation_map(adaptation_map_id: str = "adaptation_map:v0.35.0", **kwargs: Any) -> ReferencePatternAdaptationMap:
    return ReferencePatternAdaptationMap(
        adaptation_map_id=adaptation_map_id,
        version=kwargs.pop("version", V0350_VERSION),
        source_pattern_ids=kwargs.pop("source_pattern_ids", ["pattern:opencode:cli", "pattern:hermes:approval"]),
        adapted_to_v035_artifacts=kwargs.pop("adapted_to_v035_artifacts", {"cli_surface_pattern": "future CLI patch proposal preview", "permission_gate_pattern": "human review packet metadata"}),
        rejected_pattern_ids=kwargs.pop("rejected_pattern_ids", ["pattern:unsafe:apply"]),
        future_track_pattern_ids=kwargs.pop("future_track_pattern_ids", ["pattern:future:diff-envelope"]),
        summary=kwargs.pop("summary", "Adaptation map is metadata, not implementation execution."),
        **kwargs,
    )


def build_reference_pattern_rejection_record(rejection_id: str = "rejection:unsafe:v0.35.0", **kwargs: Any) -> ReferencePatternRejectionRecord:
    return ReferencePatternRejectionRecord(
        rejection_id=rejection_id,
        pattern_id=kwargs.pop("pattern_id", None),
        corpus_kind=kwargs.pop("corpus_kind", ReferenceCorpusKind.GENERIC_REFERENCE_HARNESS),
        rejected_surface=kwargs.pop("rejected_surface", "runtime patch apply"),
        risk_kinds=kwargs.pop("risk_kinds", [PatchProposalRiskKind.PATCH_APPLY_RISK, PatchProposalRiskKind.WORKSPACE_WRITE_RISK]),
        reason=kwargs.pop("reason", "Patch application is outside v0.35.0 and outside v0.35."),
        safe_alternative=kwargs.pop("safe_alternative", "Record review metadata and future-track the apply sandbox."),
        **kwargs,
    )


def build_patch_proposal_surface_policy(policy_id: str = "patch_surface_policy:v0.35.0", **kwargs: Any) -> PatchProposalSurfacePolicy:
    return PatchProposalSurfacePolicy(
        policy_id=policy_id,
        allowed_surfaces=kwargs.pop("allowed_surfaces", [PatchProposalSurfaceKind.REFERENCE_PATTERN_DIGEST, PatchProposalSurfaceKind.PATCH_INTENT, PatchProposalSurfaceKind.PATCH_SCOPE_POLICY]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [PatchProposalSurfaceKind.PATCH_APPLY, PatchProposalSurfaceKind.FILE_WRITE, PatchProposalSurfaceKind.CODE_EDIT, PatchProposalSurfaceKind.GIT_APPLY, PatchProposalSurfaceKind.APPLY_PATCH, PatchProposalSurfaceKind.SHELL_COMMAND, PatchProposalSurfaceKind.TEST_EXECUTION, PatchProposalSurfaceKind.DEPENDENCY_INSTALL]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", [PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY, PatchProposalCapabilityKind.WRITE_WORKSPACE_FILE, PatchProposalCapabilityKind.EDIT_CODE_FILE, PatchProposalCapabilityKind.RUN_GIT_APPLY, PatchProposalCapabilityKind.RUN_APPLY_PATCH, PatchProposalCapabilityKind.RUN_TESTS, PatchProposalCapabilityKind.EXECUTE_SHELL, PatchProposalCapabilityKind.INSTALL_DEPENDENCY]),
        allow_reference_digest=kwargs.pop("allow_reference_digest", True),
        allow_patch_intent_artifact=kwargs.pop("allow_patch_intent_artifact", True),
        allow_patch_scope_policy=kwargs.pop("allow_patch_scope_policy", True),
        allow_patch_context_collection_future_gate=kwargs.pop("allow_patch_context_collection_future_gate", True),
        allow_patch_plan_future_gate=kwargs.pop("allow_patch_plan_future_gate", True),
        allow_diff_proposal_future_gate=kwargs.pop("allow_diff_proposal_future_gate", True),
        allow_patch_risk_scan_future_gate=kwargs.pop("allow_patch_risk_scan_future_gate", True),
        allow_human_review_packet_future_gate=kwargs.pop("allow_human_review_packet_future_gate", True),
        **kwargs,
    )


def build_controlled_patch_proposal_allowed_surface(allowed_surface_id: str = "allowed:reference_digest:v0.35.0", **kwargs: Any) -> ControlledPatchProposalAllowedSurface:
    return ControlledPatchProposalAllowedSurface(
        allowed_surface_id=allowed_surface_id,
        surface_kind=kwargs.pop("surface_kind", PatchProposalSurfaceKind.REFERENCE_PATTERN_DIGEST),
        capability_kind=kwargs.pop("capability_kind", PatchProposalCapabilityKind.CREATE_REFERENCE_PATTERN_DIGEST),
        description=kwargs.pop("description", "Read-only reference pattern digest metadata surface."),
        **kwargs,
    )


def build_controlled_patch_proposal_prohibited_surface(prohibited_surface_id: str = "prohibited:patch_apply:v0.35.0", **kwargs: Any) -> ControlledPatchProposalProhibitedSurface:
    return ControlledPatchProposalProhibitedSurface(
        prohibited_surface_id=prohibited_surface_id,
        surface_kind=kwargs.pop("surface_kind", PatchProposalSurfaceKind.PATCH_APPLY),
        risk_kind=kwargs.pop("risk_kind", PatchProposalRiskKind.PATCH_APPLY_RISK),
        capability_kind=kwargs.pop("capability_kind", PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY),
        reason=kwargs.pop("reason", "Patch application remains prohibited in v0.35.0."),
        **kwargs,
    )


def build_controlled_patch_proposal_boundary(boundary_id: str = "controlled_patch_proposal_boundary:v0.35.0", **kwargs: Any) -> ControlledPatchProposalBoundary:
    digest = kwargs.pop("reference_digest", build_reference_pattern_digest())
    return ControlledPatchProposalBoundary(
        boundary_id=boundary_id,
        version=kwargs.pop("version", V0350_VERSION),
        release_name=kwargs.pop("release_name", V0350_RELEASE_NAME),
        surface_policy=kwargs.pop("surface_policy", build_patch_proposal_surface_policy()),
        reference_inspection_policy=kwargs.pop("reference_inspection_policy", build_reference_corpus_inspection_policy()),
        reference_digest=digest,
        allowed_surfaces=kwargs.pop("allowed_surfaces", [build_controlled_patch_proposal_allowed_surface()]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [build_controlled_patch_proposal_prohibited_surface()]),
        flags=kwargs.pop("flags", build_controlled_patch_proposal_flags()),
        status=kwargs.pop("status", PatchProposalBoundaryStatus.DIGEST_CREATED_WITH_GAPS),
        readiness_level=kwargs.pop("readiness_level", PatchProposalReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0351),
        summary=kwargs.pop("summary", "v0.35.0 defines the controlled patch proposal boundary only."),
        gaps=kwargs.pop("gaps", ["Patch intent/scope and context collector remain future-stage."]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_BOUNDARY_DOC_PATH, DEFAULT_DIGEST_DOC_PATH]),
        ready_for_v0351_patch_intent_scope_policy=kwargs.pop("ready_for_v0351_patch_intent_scope_policy", True),
        ready_for_v0352_readonly_patch_context_collector=kwargs.pop("ready_for_v0352_readonly_patch_context_collector", True),
        **kwargs,
    )


def build_controlled_patch_proposal_permission_request(request_id: str = "patch_permission_request:v0.35.0", **kwargs: Any) -> ControlledPatchProposalPermissionRequest:
    return ControlledPatchProposalPermissionRequest(
        request_id=request_id,
        surface_kind=kwargs.pop("surface_kind", PatchProposalSurfaceKind.REFERENCE_PATTERN_DIGEST),
        capability_kind=kwargs.pop("capability_kind", PatchProposalCapabilityKind.CREATE_REFERENCE_PATTERN_DIGEST),
        requested_action=kwargs.pop("requested_action", "create read-only reference pattern digest metadata"),
        summary=kwargs.pop("summary", "Permission request is metadata, not patch application."),
        **kwargs,
    )


def build_controlled_patch_proposal_permission_decision(decision_id: str = "patch_permission_decision:v0.35.0", **kwargs: Any) -> ControlledPatchProposalPermissionDecision:
    return ControlledPatchProposalPermissionDecision(
        decision_id=decision_id,
        request_id=kwargs.pop("request_id", "patch_permission_request:v0.35.0"),
        decision_kind=kwargs.pop("decision_kind", PatchProposalDecisionKind.ALLOW_REFERENCE_DIGEST_GENERATION),
        reason=kwargs.pop("reason", "Read-only reference digest metadata is allowed; apply/write/edit remain blocked."),
        risk_kinds=kwargs.pop("risk_kinds", [PatchProposalRiskKind.SCOPE_ESCAPE_RISK]),
        **kwargs,
    )


def build_controlled_patch_proposal_denied_action(denied_action_id: str = "patch_denied_action:v0.35.0", **kwargs: Any) -> ControlledPatchProposalDeniedAction:
    return ControlledPatchProposalDeniedAction(
        denied_action_id=denied_action_id,
        request_id=kwargs.pop("request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        surface_kind=kwargs.pop("surface_kind", PatchProposalSurfaceKind.PATCH_APPLY),
        risk_kinds=kwargs.pop("risk_kinds", [PatchProposalRiskKind.PATCH_APPLY_RISK]),
        reason=kwargs.pop("reason", "Patch application is prohibited."),
        safe_alternatives=kwargs.pop("safe_alternatives", ["Create bounded review metadata in later stages."]),
        **kwargs,
    )


def build_controlled_patch_proposal_gate_evaluation(gate_evaluation_id: str = "patch_gate:v0.35.0", **kwargs: Any) -> ControlledPatchProposalGateEvaluation:
    return ControlledPatchProposalGateEvaluation(
        gate_evaluation_id=gate_evaluation_id,
        request_id=kwargs.pop("request_id", "patch_permission_request:v0.35.0"),
        decision=kwargs.pop("decision", build_controlled_patch_proposal_permission_decision()),
        denied_action=kwargs.pop("denied_action", None),
        status=kwargs.pop("status", PatchProposalBoundaryStatus.BOUNDARY_READY_WITH_GAPS),
        summary=kwargs.pop("summary", "Gate evaluation preserves no apply/write readiness."),
        **kwargs,
    )


def build_controlled_patch_proposal_risk_register(risk_register_id: str = "patch_risk_register:v0.35.0", **kwargs: Any) -> ControlledPatchProposalRiskRegister:
    risks = kwargs.pop(
        "risk_kinds",
        [
            PatchProposalRiskKind.PATCH_APPLY_RISK,
            PatchProposalRiskKind.WORKSPACE_WRITE_RISK,
            PatchProposalRiskKind.CODE_EDIT_RISK,
            PatchProposalRiskKind.SCOPE_ESCAPE_RISK,
            PatchProposalRiskKind.SECRET_EXPOSURE_RISK,
            PatchProposalRiskKind.CREDENTIAL_EXPOSURE_RISK,
            PatchProposalRiskKind.SHELL_EXECUTION_RISK,
            PatchProposalRiskKind.SUBPROCESS_EXECUTION_RISK,
            PatchProposalRiskKind.COMMAND_EXECUTION_RISK,
            PatchProposalRiskKind.DEPENDENCY_INSTALL_RISK,
            PatchProposalRiskKind.TEST_EXECUTION_RISK,
            PatchProposalRiskKind.REFERENCE_EXECUTION_RISK,
            PatchProposalRiskKind.REFERENCE_IMPORT_RISK,
            PatchProposalRiskKind.COPIED_CODE_RISK,
            PatchProposalRiskKind.UNSAFE_DIFF_GENERATION_RISK,
            PatchProposalRiskKind.UNBOUNDED_CONTEXT_RISK,
        ],
    )
    return ControlledPatchProposalRiskRegister(
        risk_register_id=risk_register_id,
        version=kwargs.pop("version", V0350_VERSION),
        risk_kinds=risks,
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", [PatchProposalSurfaceKind.PATCH_APPLY, PatchProposalSurfaceKind.FILE_WRITE, PatchProposalSurfaceKind.CODE_EDIT, PatchProposalSurfaceKind.SHELL_COMMAND, PatchProposalSurfaceKind.TEST_EXECUTION, PatchProposalSurfaceKind.DEPENDENCY_INSTALL, PatchProposalSurfaceKind.REFERENCE_CODE_EXECUTION]),
        mitigations=kwargs.pop("mitigations", ["deny apply/write/edit", "read-only reference digest", "future-stage patch proposal artifacts only"]),
        **kwargs,
    )


def build_controlled_patch_proposal_no_apply_guarantee(guarantee_id: str = "patch_no_apply_guarantee:v0.35.0", **kwargs: Any) -> ControlledPatchProposalNoApplyGuarantee:
    return ControlledPatchProposalNoApplyGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0350_VERSION), **kwargs)


def build_v035_roadmap_overview(roadmap_id: str = "v035_roadmap:v0.35.0", **kwargs: Any) -> V035RoadmapOverview:
    return V035RoadmapOverview(
        roadmap_id=roadmap_id,
        version=kwargs.pop("version", V0350_VERSION),
        track_name=kwargs.pop("track_name", V035_TRACK_NAME),
        stages=kwargs.pop("stages", list(DEFAULT_V035_ROADMAP)),
        summary=kwargs.pop("summary", "v0.35 roadmap is patch proposal only; patch apply remains later-track."),
        **kwargs,
    )


def build_v0350_readiness_report(report_id: str = "v0350_readiness_report", **kwargs: Any) -> V0350ReadinessReport:
    return V0350ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0350_VERSION),
        boundary_id=kwargs.pop("boundary_id", "controlled_patch_proposal_boundary:v0.35.0"),
        digest_id=kwargs.pop("digest_id", "reference_pattern_digest:v0.35.0"),
        summary=kwargs.pop("summary", "v0.35.0 is boundary foundation only and ready for design-stage v0.35.1/v0.35.2 handoff."),
        readiness_level=kwargs.pop("readiness_level", PatchProposalReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0351),
        completed_items=kwargs.pop("completed_items", ["boundary contract", "reference inspection policy", "reference pattern digest"]),
        future_track_items=kwargs.pop("future_track_items", ["patch intent policy", "read-only context collector", "diff proposal envelope", "human review packet"]),
        ready_for_v0351_patch_intent_scope_policy=kwargs.pop("ready_for_v0351_patch_intent_scope_policy", True),
        ready_for_v0352_readonly_patch_context_collector=kwargs.pop("ready_for_v0352_readonly_patch_context_collector", True),
        ready_for_reference_pattern_digest=kwargs.pop("ready_for_reference_pattern_digest", True),
        **kwargs,
    )


def _relative_ref(path: Path, base: Path) -> str:
    try:
        return str(path.resolve().relative_to(base.resolve())).replace("\\", "/")
    except ValueError:
        return str(path).replace("\\", "/")


def _is_blocked_ref(path: Path, policy: ReferenceCorpusInspectionPolicy) -> bool:
    lowered = path.name.lower()
    return any(pattern.lower() in lowered for pattern in policy.blocked_file_patterns)


def _is_allowed_ref(path: Path, policy: ReferenceCorpusInspectionPolicy) -> bool:
    lowered = path.name.lower()
    return any(lowered.endswith(pattern.lower()) for pattern in policy.allowed_file_patterns)


def _pattern_kind_for_ref(ref: str) -> ReferenceHarnessPatternKind | None:
    lowered = ref.lower()
    if "cli" in lowered or "command" in lowered or "tui" in lowered:
        return ReferenceHarnessPatternKind.CLI_SURFACE_PATTERN
    if "agent" in lowered or "session" in lowered or "loop" in lowered or "gateway" in lowered:
        return ReferenceHarnessPatternKind.AGENT_LOOP_PATTERN
    if "context" in lowered or "prompt" in lowered:
        return ReferenceHarnessPatternKind.CONTEXT_COLLECTION_PATTERN
    if "tool" in lowered or "mcp" in lowered or "plugin" in lowered:
        return ReferenceHarnessPatternKind.TOOL_REGISTRY_PATTERN
    if "permission" in lowered or "approval" in lowered or "auth" in lowered or "security" in lowered:
        return ReferenceHarnessPatternKind.PERMISSION_GATE_PATTERN
    if "edit" in lowered or "write" in lowered or "patch" in lowered or "diff" in lowered:
        return ReferenceHarnessPatternKind.FILE_EDIT_PLANNING_PATTERN
    if "review" in lowered or "pr" in lowered:
        return ReferenceHarnessPatternKind.REVIEW_WORKFLOW_PATTERN
    if "log" in lowered or "trace" in lowered or "state" in lowered or "event" in lowered:
        return ReferenceHarnessPatternKind.LOGGING_TRACE_SESSION_PATTERN
    if "error" in lowered or "failure" in lowered or "retry" in lowered:
        return ReferenceHarnessPatternKind.FAILURE_HANDLING_PATTERN
    return None


def inspect_reference_corpus_readonly(root_path: str | Path, corpus_kind: ReferenceCorpusKind | str, policy: ReferenceCorpusInspectionPolicy | None = None) -> tuple[ReferenceCorpusInventory, list[ReferenceHarnessPattern]]:
    policy = policy or build_reference_corpus_inspection_policy()
    root = Path(root_path)
    corpus = ReferenceCorpusKind(corpus_kind)
    root_ref = str(root).replace("\\", "/")
    if not root.exists():
        inventory = build_reference_corpus_inventory(
            inventory_id=f"inventory:{corpus.value}:missing",
            corpus_kind=corpus,
            root_path_ref=root_ref,
            inspection_status=ReferenceCorpusInspectionStatus.NOT_FOUND,
            summary=f"{root_ref} was not found; absence recorded without execution.",
        )
        return inventory, [
            build_reference_harness_pattern(
                pattern_id=f"pattern:{corpus.value}:missing",
                corpus_kind=corpus,
                pattern_kind=ReferenceHarnessPatternKind.UNKNOWN,
                disposition=ReferencePatternDisposition.INSUFFICIENT_EVIDENCE,
                pattern_summary=f"{root_ref} missing; no pattern inferred.",
                confidence="high",
            )
        ]

    inspected: list[str] = []
    skipped: list[str] = []
    skipped_reasons: list[str] = []
    package_refs: list[str] = []
    doc_refs: list[str] = []
    source_refs: list[str] = []
    patterns_by_kind: dict[ReferenceHarnessPatternKind, set[str]] = {}

    for path in root.rglob("*"):
        if len(inspected) >= policy.max_files_per_corpus:
            skipped_reasons.append("max_files_per_corpus reached")
            break
        if not path.is_file():
            continue
        rel = _relative_ref(path, Path.cwd())
        if _is_blocked_ref(path, policy):
            skipped.append(rel)
            skipped_reasons.append(f"blocked secret-like file name: {rel}")
            continue
        if not _is_allowed_ref(path, policy):
            skipped.append(rel)
            continue
        try:
            if path.stat().st_size > policy.max_file_chars:
                skipped.append(rel)
                skipped_reasons.append(f"skipped oversized file: {rel}")
                continue
            excerpt = path.read_text(encoding="utf-8", errors="replace")[
                : policy.max_excerpt_chars
            ]
        except OSError:
            skipped.append(rel)
            skipped_reasons.append(f"failed safe reading metadata: {rel}")
            continue
        inspected.append(rel)
        lower = rel.lower()
        if lower.endswith((".json", ".yaml", ".yml", ".toml")) or "package" in lower:
            package_refs.append(rel)
        elif lower.endswith((".md", ".mdx", ".txt")):
            doc_refs.append(rel)
        else:
            source_refs.append(rel)
        kind = _pattern_kind_for_ref(f"{rel} {excerpt}")
        if kind:
            patterns_by_kind.setdefault(kind, set()).add(rel)

    status = ReferenceCorpusInspectionStatus.INSPECTED_READONLY if inspected else ReferenceCorpusInspectionStatus.PARTIALLY_INSPECTED
    inventory = ReferenceCorpusInventory(
        inventory_id=f"inventory:{corpus.value}:v0.35.0",
        corpus_kind=corpus,
        root_path_ref=root_ref,
        inspection_status=status,
        inspected_file_refs=inspected,
        skipped_file_refs=skipped[: policy.max_files_per_corpus],
        skipped_reasons=list(dict.fromkeys(skipped_reasons))[:20],
        package_or_config_refs=package_refs,
        doc_refs=doc_refs,
        source_refs=source_refs,
        summary=f"{root_ref} inspected read-only with bounded file and excerpt limits.",
    )
    patterns = [
        build_reference_harness_pattern(
            pattern_id=f"pattern:{corpus.value}:{kind.value}",
            corpus_kind=corpus,
            pattern_kind=kind,
            disposition=ReferencePatternDisposition.OBSERVED,
            pattern_summary=f"Observed {kind.value.replace('_', ' ')} evidence in {corpus.value} reference files.",
            observed_evidence_refs=sorted(refs)[:8],
            chantacore_adaptation="Adapt as v0.35 metadata/policy shape only; do not copy implementation bodies.",
            confidence="medium" if len(refs) < 3 else "high",
        )
        for kind, refs in sorted(patterns_by_kind.items(), key=lambda item: item[0].value)
    ]
    patterns.append(
        build_reference_harness_pattern(
            pattern_id=f"pattern:{corpus.value}:unsafe_execution_rejected",
            corpus_kind=corpus,
            pattern_kind=ReferenceHarnessPatternKind.UNSAFE_EXECUTION_PATTERN,
            disposition=ReferencePatternDisposition.REJECTED_FOR_SAFETY,
            pattern_summary="Reference runtime execution/import/install/test patterns are rejected for ChantaCore v0.35.0.",
            observed_evidence_refs=inspected[:5],
            chantacore_adaptation="Record only no-execution boundary and future-track review metadata.",
            rejection_reason="v0.35.0 is boundary/digest only and cannot execute, import, install, test, write, or apply patches.",
            confidence="high",
        )
    )
    return inventory, patterns


def build_reference_pattern_digest_from_reference_roots(reference_roots: dict[ReferenceCorpusKind | str, str | Path], policy: ReferenceCorpusInspectionPolicy | None = None, digest_doc_path: str = DEFAULT_DIGEST_DOC_PATH) -> ReferencePatternDigest:
    policy = policy or build_reference_corpus_inspection_policy()
    inventories: list[ReferenceCorpusInventory] = []
    patterns: list[ReferenceHarnessPattern] = []
    for corpus_kind, root in reference_roots.items():
        inventory, corpus_patterns = inspect_reference_corpus_readonly(root, corpus_kind, policy)
        inventories.append(inventory)
        patterns.extend(corpus_patterns)
    rejected = sum(1 for item in patterns if ReferencePatternDisposition(item.disposition) == ReferencePatternDisposition.REJECTED_FOR_SAFETY)
    future = sum(1 for item in patterns if ReferencePatternDisposition(item.disposition) == ReferencePatternDisposition.FUTURE_TRACK)
    return build_reference_pattern_digest(
        corpus_inventories=inventories,
        patterns=patterns,
        digest_doc_path=digest_doc_path,
        rejected_pattern_count=rejected,
        future_track_count=future,
        summary="Reference pattern digest built from read-only static reference roots.",
    )


def controlled_patch_proposal_flags_preserve_no_apply(flags: ControlledPatchProposalFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_FLAG_NAMES) and flags.production_certified is False


def reference_pattern_digest_confirms_no_execution(digest: ReferencePatternDigest) -> bool:
    return digest.executable is False and digest.no_execution_confirmed and digest.no_import_confirmed and digest.no_install_confirmed and digest.no_test_run_confirmed and digest.no_secret_read_confirmed


def patch_proposal_surface_policy_blocks_apply(policy: PatchProposalSurfacePolicy) -> bool:
    return policy.allow_patch_apply is False and policy.allow_workspace_write is False and policy.allow_code_edit is False and policy.allow_shell is False and policy.allow_test_execution is False and policy.allow_dependency_install is False


def controlled_patch_proposal_boundary_is_not_apply(boundary: ControlledPatchProposalBoundary) -> bool:
    return boundary.patch_application is False and boundary.patch_proposal_generation is False and boundary.ready_for_execution is False and boundary.ready_for_patch_application is False and boundary.ready_for_workspace_write is False and boundary.ready_for_code_edit is False


def controlled_patch_proposal_decision_is_not_apply(decision: ControlledPatchProposalPermissionDecision) -> bool:
    return not (decision.patch_apply_allowed or decision.workspace_write_allowed or decision.code_edit_allowed or decision.shell_allowed or decision.test_execution_allowed or decision.dependency_install_allowed)


def v0350_readiness_report_is_not_execution_ready(report: V0350ReadinessReport) -> bool:
    return (
        report.ready_for_execution is False
        and report.ready_for_patch_proposal is False
        and report.ready_for_patch_application is False
        and report.ready_for_workspace_write is False
        and report.ready_for_code_edit is False
        and report.ready_for_apply_patch is False
        and report.ready_for_git_apply is False
        and report.ready_for_test_execution is False
        and report.ready_for_shell_execution is False
        and report.ready_for_dependency_install is False
        and report.ready_for_reference_execution is False
        and report.ready_for_reference_import is False
        and report.production_certified is False
    )
