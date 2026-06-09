from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_candidate import (
    ApplyCandidateEnvelope,
    ApplyEligibilityDecision,
    HumanApprovalContract,
)


V0362_VERSION = "v0.36.2"
V0362_RELEASE_NAME = "v0.36.2 Dry-run Patch Apply Simulation"
MAX_SOURCE_CHARS = 12000
MAX_PREVIEW_CHARS = 600

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_sandbox_patch_apply",
    "ready_for_sandbox_workspace_write",
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
    "apply",
    "write",
    "edit",
    "shell",
    "test_execution",
    "dependency_install",
    "reference_execution",
    "reference_import",
    "external_agent_execution",
    "dominion_runtime",
    "provider_invocation",
    "direct_network_access",
    "credential_access",
)


class DryRunApplyMode(StrEnum):
    UNIFIED_DIFF_DRY_RUN = "unified_diff_dry_run"
    STRUCTURED_PATCH_DRY_RUN = "structured_patch_dry_run"
    COMBINED_DIFF_DRY_RUN = "combined_diff_dry_run"
    METADATA_ONLY_DRY_RUN = "metadata_only_dry_run"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class DryRunApplySourceKind(StrEnum):
    V0361_APPLY_CANDIDATE_ENVELOPE = "v0361_apply_candidate_envelope"
    V0361_HUMAN_APPROVAL_CONTRACT = "v0361_human_approval_contract"
    V0361_APPLY_ELIGIBILITY_DECISION = "v0361_apply_eligibility_decision"
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    V0354_UNIFIED_DIFF_PROPOSAL = "v0354_unified_diff_proposal"
    V0354_STRUCTURED_PATCH_PROPOSAL = "v0354_structured_patch_proposal"
    V0352_PATCH_CONTEXT_SNAPSHOT = "v0352_patch_context_snapshot"
    V0352_EVIDENCE_BUNDLE = "v0352_evidence_bundle"
    IN_MEMORY_SOURCE_IMAGE = "in_memory_source_image"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class DryRunApplyStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    SIMULATION_READY = "simulation_ready"
    SIMULATION_COMPLETED = "simulation_completed"
    SIMULATION_COMPLETED_WITH_CONFLICTS = "simulation_completed_with_conflicts"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class DryRunApplyReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    DRY_RUN_CONTRACT_READY = "dry_run_contract_ready"
    DRY_RUN_INPUT_READY = "dry_run_input_ready"
    HUNK_ALIGNMENT_READY = "hunk_alignment_ready"
    CONFLICT_REPORT_READY = "conflict_report_ready"
    SIMULATED_DELTA_READY = "simulated_delta_ready"
    DESIGN_HANDOFF_READY_FOR_V0363 = "design_handoff_ready_for_v0363"
    DESIGN_HANDOFF_READY_FOR_V0364 = "design_handoff_ready_for_v0364"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class DryRunApplyDecisionKind(StrEnum):
    ALLOW_DRY_RUN_SIMULATION = "allow_dry_run_simulation"
    ALLOW_HUNK_ALIGNMENT = "allow_hunk_alignment"
    ALLOW_CONFLICT_DETECTION = "allow_conflict_detection"
    ALLOW_SIMULATED_DELTA_METADATA = "allow_simulated_delta_metadata"
    ELIGIBLE_FOR_FUTURE_SANDBOX_WORKSPACE = "eligible_for_future_sandbox_workspace"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class DryRunApplyRiskKind(StrEnum):
    INVALID_APPLY_CANDIDATE_RISK = "invalid_apply_candidate_risk"
    MISSING_HUMAN_APPROVAL_RISK = "missing_human_approval_risk"
    INVALID_HUMAN_APPROVAL_RISK = "invalid_human_approval_risk"
    MISSING_DIFF_RISK = "missing_diff_risk"
    MALFORMED_DIFF_RISK = "malformed_diff_risk"
    MISSING_SOURCE_IMAGE_RISK = "missing_source_image_risk"
    STALE_SOURCE_CONTEXT_RISK = "stale_source_context_risk"
    HUNK_ALIGNMENT_FAILURE_RISK = "hunk_alignment_failure_risk"
    PATCH_CONFLICT_RISK = "patch_conflict_risk"
    SCOPE_MISMATCH_RISK = "scope_mismatch_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    SANDBOX_WRITE_CONFUSION_RISK = "sandbox_write_confusion_risk"
    PATCH_APPLY_CONFUSION_RISK = "patch_apply_confusion_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class DryRunHunkAlignmentStatus(StrEnum):
    UNKNOWN = "unknown"
    ALIGNED_EXACT = "aligned_exact"
    ALIGNED_WITH_OFFSET = "aligned_with_offset"
    ALIGNED_WITH_FUZZ = "aligned_with_fuzz"
    NOT_FOUND = "not_found"
    AMBIGUOUS = "ambiguous"
    STALE_CONTEXT = "stale_context"
    BLOCKED = "blocked"
    SKIPPED = "skipped"


class DryRunConflictKind(StrEnum):
    NO_CONFLICT = "no_conflict"
    MISSING_TARGET_SOURCE = "missing_target_source"
    MALFORMED_HUNK = "malformed_hunk"
    CONTEXT_NOT_FOUND = "context_not_found"
    AMBIGUOUS_CONTEXT = "ambiguous_context"
    STALE_SOURCE = "stale_source"
    OVERLAPPING_HUNKS = "overlapping_hunks"
    BLOCKED_TARGET = "blocked_target"
    SCOPE_VIOLATION = "scope_violation"
    SECRET_TARGET = "secret_target"
    BINARY_TARGET = "binary_target"
    UNSUPPORTED_OPERATION = "unsupported_operation"
    UNKNOWN = "unknown"


class DryRunFileDeltaKind(StrEnum):
    NO_CHANGE = "no_change"
    SIMULATED_ADDITION = "simulated_addition"
    SIMULATED_DELETION = "simulated_deletion"
    SIMULATED_REPLACEMENT = "simulated_replacement"
    SIMULATED_FILE_CREATE = "simulated_file_create"
    SIMULATED_FILE_DELETE = "simulated_file_delete"
    SIMULATED_METADATA_CHANGE = "simulated_metadata_change"
    UNSUPPORTED_DELTA = "unsupported_delta"
    BLOCKED_DELTA = "blocked_delta"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0362_VERSION not in version:
        raise ValueError("version must include v0.36.2")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.2")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.36.2")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret", "credential", "api_key", "token")):
            raise ValueError("metadata keys must not request credential or secret material")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _bounded_preview(value: str, max_chars: int = MAX_PREVIEW_CHARS) -> str:
    if not isinstance(value, str):
        raise TypeError("preview value must be str")
    redacted = value
    for token in ("secret", "credential", "api_key", "token", "password"):
        redacted = redacted.replace(token, "[redacted]")
        redacted = redacted.replace(token.upper(), "[redacted]")
    return redacted[:max_chars]


def _split_lines(value: str) -> list[str]:
    return value.splitlines()


def _join_lines(lines: list[str]) -> str:
    return "\n".join(lines)


@dataclass(frozen=True)
class DryRunApplyFlagSet:
    flag_set_id: str
    version: str
    dry_run_apply_layer_constructed: bool
    dry_run_policy_defined: bool
    dry_run_input_available: bool
    hunk_alignment_available: bool
    conflict_detection_available: bool
    simulated_delta_available: bool
    ready_for_v0363_sandbox_workspace_overlay_policy: bool
    ready_for_v0364_sandbox_patch_apply_engine: bool
    ready_for_dry_run_apply_simulation: bool
    ready_for_dry_run_hunk_alignment: bool
    ready_for_dry_run_conflict_detection: bool
    ready_for_simulated_file_delta: bool
    ready_for_future_sandbox_workspace_input: bool
    ready_for_execution: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_sandbox_workspace_write: bool = False
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
class DryRunApplySourceRef:
    source_ref_id: str
    source_kind: DryRunApplySourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        DryRunApplySourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyPolicy:
    dry_run_policy_id: str
    version: str
    allowed_modes: list[DryRunApplyMode | str]
    blocked_modes: list[DryRunApplyMode | str]
    max_files: int
    max_hunks: int
    max_source_chars: int
    max_after_preview_chars: int
    allow_unified_diff_parse: bool
    allow_structured_patch_parse: bool
    allow_hunk_alignment: bool
    allow_conflict_detection: bool
    allow_simulated_delta: bool
    allow_future_sandbox_workspace_input: bool
    allow_sandbox_patch_apply: bool = False
    allow_sandbox_workspace_write: bool = False
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
        _require_non_blank("dry_run_policy_id", self.dry_run_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, DryRunApplyMode)
        _validate_enum_list("blocked_modes", self.blocked_modes, DryRunApplyMode)
        for name in ("max_files", "max_hunks", "max_source_chars", "max_after_preview_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(
            self,
            (
                "allow_sandbox_patch_apply",
                "allow_sandbox_workspace_write",
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
class DryRunApplyInput:
    dry_run_input_id: str
    version: str
    apply_candidate_id: str | None
    human_approval_contract_id: str | None
    apply_eligibility_decision_id: str | None
    diff_envelope_id: str | None
    unified_diff_id: str | None
    structured_patch_id: str | None
    context_snapshot_id: str | None
    requested_mode: DryRunApplyMode | str
    task_summary: str
    source_refs: list[DryRunApplySourceRef]
    prohibited_runtime_actions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("dry_run_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        DryRunApplyMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [action for action in PROHIBITED_RUNTIME_ACTIONS if action not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing {missing}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunSourceImage:
    source_image_id: str
    path_ref: str
    source_text: str
    source_summary: str
    line_count: int
    redacted: bool
    truncated: bool
    safe_for_simulation: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_image_id", "path_ref", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        if not isinstance(self.source_text, str):
            raise TypeError("source_text must be str")
        if len(self.source_text) > MAX_SOURCE_CHARS:
            raise ValueError("source_text must be bounded")
        if self.line_count < 0:
            raise ValueError("line_count must be >= 0")
        _validate_metadata_safe(self.metadata)
        unsafe_markers = ("secret", "binary", "oversized")
        if any(self.metadata.get(marker) for marker in unsafe_markers) and self.safe_for_simulation:
            raise ValueError("unsafe source image cannot be safe_for_simulation")


@dataclass(frozen=True)
class DryRunTargetFileImage:
    target_file_image_id: str
    path_ref: str
    original_source_image_id: str | None
    simulated_after_preview: str
    simulated_summary: str
    changed: bool
    redacted: bool
    truncated: bool
    ready_for_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("target_file_image_id", "path_ref", "simulated_summary"):
            _require_non_blank(name, getattr(self, name))
        if _bounded_preview(self.simulated_after_preview) != self.simulated_after_preview:
            raise ValueError("simulated_after_preview must be bounded and redacted")
        _validate_false(self, ("ready_for_write",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunHunkInput:
    hunk_input_id: str
    target_path_ref: str
    hunk_header: str
    original_context: list[str]
    proposed_lines: list[str]
    removed_lines: list[str]
    source_hunk_ref: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("hunk_input_id", "target_path_ref", "hunk_header"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("original_context", self.original_context)
        _validate_string_list("proposed_lines", self.proposed_lines)
        _validate_string_list("removed_lines", self.removed_lines)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunHunkAlignment:
    hunk_alignment_id: str
    hunk_input_id: str
    target_path_ref: str
    alignment_status: DryRunHunkAlignmentStatus | str
    matched_line_start: int | None
    matched_line_end: int | None
    fuzz_used: int
    confidence: str
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("hunk_alignment_id", "hunk_input_id", "target_path_ref", "confidence", "summary"):
            _require_non_blank(name, getattr(self, name))
        DryRunHunkAlignmentStatus(self.alignment_status)
        for name in ("matched_line_start", "matched_line_end"):
            value = getattr(self, name)
            if value is not None and value < 1:
                raise ValueError(f"{name} must be None or >= 1")
        if self.fuzz_used < 0:
            raise ValueError("fuzz_used must be >= 0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunConflict:
    conflict_id: str
    conflict_kind: DryRunConflictKind | str
    target_path_ref: str | None
    hunk_input_id: str | None
    severity: str
    conflict_summary: str
    evidence_preview: str
    blocks_future_sandbox_apply: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("conflict_id", "severity", "conflict_summary"):
            _require_non_blank(name, getattr(self, name))
        DryRunConflictKind(self.conflict_kind)
        if _bounded_preview(self.evidence_preview) != self.evidence_preview:
            raise ValueError("evidence_preview must be bounded and redacted")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunSimulatedFileDelta:
    simulated_delta_id: str
    target_path_ref: str
    delta_kind: DryRunFileDeltaKind | str
    hunk_alignment_ids: list[str]
    conflict_ids: list[str]
    before_preview: str
    after_preview: str
    delta_summary: str
    changed: bool
    redacted: bool
    truncated: bool
    ready_for_write: bool = False
    ready_for_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("simulated_delta_id", "target_path_ref", "delta_summary"):
            _require_non_blank(name, getattr(self, name))
        DryRunFileDeltaKind(self.delta_kind)
        _validate_string_list("hunk_alignment_ids", self.hunk_alignment_ids)
        _validate_string_list("conflict_ids", self.conflict_ids)
        if _bounded_preview(self.before_preview) != self.before_preview:
            raise ValueError("before_preview must be bounded and redacted")
        if _bounded_preview(self.after_preview) != self.after_preview:
            raise ValueError("after_preview must be bounded and redacted")
        _validate_false(self, ("ready_for_write", "ready_for_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunSimulatedFileResult:
    file_result_id: str
    target_path_ref: str
    source_image_id: str | None
    target_file_image: DryRunTargetFileImage | None
    simulated_deltas: list[DryRunSimulatedFileDelta]
    conflicts: list[DryRunConflict]
    file_result_summary: str
    simulation_successful: bool
    ready_for_future_sandbox_workspace_input: bool
    ready_for_write: bool = False
    ready_for_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("file_result_id", "target_path_ref", "file_result_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("simulated_deltas", self.simulated_deltas)
        _validate_list("conflicts", self.conflicts)
        if self.ready_for_future_sandbox_workspace_input and any(conflict.blocks_future_sandbox_apply for conflict in self.conflicts):
            raise ValueError("blocking conflicts prevent future sandbox workspace input")
        _validate_false(self, ("ready_for_write", "ready_for_apply"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplySimulationResult:
    simulation_result_id: str
    version: str
    dry_run_input_id: str
    mode: DryRunApplyMode | str
    status: DryRunApplyStatus | str
    readiness_level: DryRunApplyReadinessLevel | str
    file_results: list[DryRunSimulatedFileResult]
    hunk_alignments: list[DryRunHunkAlignment]
    conflicts: list[DryRunConflict]
    source_refs: list[DryRunApplySourceRef]
    summary: str
    conflict_count: int
    blocking_conflict_count: int
    simulation_successful: bool
    eligible_for_future_sandbox_workspace_input: bool
    ready_for_v0363_sandbox_workspace_overlay_policy: bool
    ready_for_v0364_sandbox_patch_apply_engine: bool
    ready_for_sandbox_patch_apply: bool = False
    ready_for_sandbox_workspace_write: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("simulation_result_id", "dry_run_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        DryRunApplyMode(self.mode)
        DryRunApplyStatus(self.status)
        DryRunApplyReadinessLevel(self.readiness_level)
        for name in ("file_results", "hunk_alignments", "conflicts", "source_refs"):
            _validate_list(name, getattr(self, name))
        for name in ("conflict_count", "blocking_conflict_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        if self.eligible_for_future_sandbox_workspace_input and (not self.simulation_successful or self.blocking_conflict_count):
            raise ValueError("future sandbox input requires successful simulation with no blocking conflicts")
        _validate_false(
            self,
            (
                "ready_for_sandbox_patch_apply",
                "ready_for_sandbox_workspace_write",
                "ready_for_live_workspace_write",
                "ready_for_patch_application",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyDecision:
    decision_id: str
    decision_kind: DryRunApplyDecisionKind | str
    status: DryRunApplyStatus | str
    summary: str
    ready_for_future_sandbox_workspace_input: bool
    ready_for_sandbox_patch_apply: bool = False
    ready_for_write: bool = False
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        DryRunApplyDecisionKind(self.decision_kind)
        DryRunApplyStatus(self.status)
        _validate_false(self, ("ready_for_sandbox_patch_apply", "ready_for_write", "ready_for_apply", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyValidationFinding:
    finding_id: str
    risk_kind: DryRunApplyRiskKind | str
    decision_kind: DryRunApplyDecisionKind | str
    summary: str
    blocks_future_sandbox_workspace_input: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        DryRunApplyRiskKind(self.risk_kind)
        DryRunApplyDecisionKind(self.decision_kind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyValidationReport:
    validation_report_id: str
    simulation_result_id: str
    findings: list[DryRunApplyValidationFinding]
    status: DryRunApplyStatus | str
    summary: str
    certifies_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "simulation_result_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("findings", self.findings)
        DryRunApplyStatus(self.status)
        _validate_false(self, ("certifies_patch_application",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyReport:
    report_id: str
    simulation_result: DryRunApplySimulationResult
    validation_report: DryRunApplyValidationReport
    decision: DryRunApplyDecision
    summary: str
    simulation_successful: bool
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyRunPreview:
    run_preview_id: str
    simulation_result_id: str
    preview_summary: str
    ready_for_future_sandbox_workspace_input: bool
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "simulation_result_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DryRunApplyNoWriteGuarantee:
    guarantee_id: str
    version: str
    no_sandbox_workspace_creation: bool
    no_sandbox_file_write: bool
    no_live_workspace_write: bool
    no_sandbox_patch_apply: bool
    no_patch_application: bool
    no_workspace_write: bool
    no_code_edit: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_test_execution: bool
    no_shell_execution: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_autonomous_agent_runtime: bool
    no_independent_agent_runtime: bool
    no_multi_cycle_agentic_loop: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0362ReadinessReport:
    report_id: str
    version: str
    release_name: str
    summary: str
    ready_for_v0363_sandbox_workspace_overlay_policy: bool
    ready_for_v0364_sandbox_patch_apply_engine: bool
    ready_for_dry_run_apply_simulation: bool
    ready_for_dry_run_hunk_alignment: bool
    ready_for_dry_run_conflict_detection: bool
    ready_for_simulated_file_delta: bool
    ready_for_future_sandbox_workspace_input: bool
    ready_for_execution: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_sandbox_workspace_write: bool = False
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
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


def build_dry_run_apply_flags(flag_set_id: str = "dry_run_apply_flags:v0.36.2", **kwargs: Any) -> DryRunApplyFlagSet:
    return DryRunApplyFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0362_VERSION),
        dry_run_apply_layer_constructed=kwargs.pop("dry_run_apply_layer_constructed", True),
        dry_run_policy_defined=kwargs.pop("dry_run_policy_defined", True),
        dry_run_input_available=kwargs.pop("dry_run_input_available", True),
        hunk_alignment_available=kwargs.pop("hunk_alignment_available", True),
        conflict_detection_available=kwargs.pop("conflict_detection_available", True),
        simulated_delta_available=kwargs.pop("simulated_delta_available", True),
        ready_for_v0363_sandbox_workspace_overlay_policy=kwargs.pop("ready_for_v0363_sandbox_workspace_overlay_policy", True),
        ready_for_v0364_sandbox_patch_apply_engine=kwargs.pop("ready_for_v0364_sandbox_patch_apply_engine", True),
        ready_for_dry_run_apply_simulation=kwargs.pop("ready_for_dry_run_apply_simulation", True),
        ready_for_dry_run_hunk_alignment=kwargs.pop("ready_for_dry_run_hunk_alignment", True),
        ready_for_dry_run_conflict_detection=kwargs.pop("ready_for_dry_run_conflict_detection", True),
        ready_for_simulated_file_delta=kwargs.pop("ready_for_simulated_file_delta", True),
        ready_for_future_sandbox_workspace_input=kwargs.pop("ready_for_future_sandbox_workspace_input", True),
        **kwargs,
    )


def build_dry_run_apply_source_ref(source_ref_id: str = "dry_run_source:v0.36.2", **kwargs: Any) -> DryRunApplySourceRef:
    return DryRunApplySourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", DryRunApplySourceKind.V0361_APPLY_CANDIDATE_ENVELOPE),
        source_id=kwargs.pop("source_id", "apply_candidate:v0.36.1"),
        source_summary=kwargs.pop("source_summary", "bounded dry-run metadata source"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.36.1", "v0.35.4", "v0.35.2"]),
        **kwargs,
    )


def build_dry_run_apply_policy(dry_run_policy_id: str = "dry_run_policy:v0.36.2", **kwargs: Any) -> DryRunApplyPolicy:
    return DryRunApplyPolicy(
        dry_run_policy_id=dry_run_policy_id,
        version=kwargs.pop("version", V0362_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [DryRunApplyMode.UNIFIED_DIFF_DRY_RUN, DryRunApplyMode.STRUCTURED_PATCH_DRY_RUN, DryRunApplyMode.METADATA_ONLY_DRY_RUN]),
        blocked_modes=kwargs.pop("blocked_modes", [DryRunApplyMode.BLOCKED, DryRunApplyMode.UNKNOWN]),
        max_files=kwargs.pop("max_files", 8),
        max_hunks=kwargs.pop("max_hunks", 64),
        max_source_chars=kwargs.pop("max_source_chars", MAX_SOURCE_CHARS),
        max_after_preview_chars=kwargs.pop("max_after_preview_chars", MAX_PREVIEW_CHARS),
        allow_unified_diff_parse=kwargs.pop("allow_unified_diff_parse", True),
        allow_structured_patch_parse=kwargs.pop("allow_structured_patch_parse", True),
        allow_hunk_alignment=kwargs.pop("allow_hunk_alignment", True),
        allow_conflict_detection=kwargs.pop("allow_conflict_detection", True),
        allow_simulated_delta=kwargs.pop("allow_simulated_delta", True),
        allow_future_sandbox_workspace_input=kwargs.pop("allow_future_sandbox_workspace_input", True),
        **kwargs,
    )


def default_dry_run_apply_policy(**kwargs: Any) -> DryRunApplyPolicy:
    return build_dry_run_apply_policy(**kwargs)


def build_dry_run_apply_input(dry_run_input_id: str = "dry_run_input:v0.36.2", **kwargs: Any) -> DryRunApplyInput:
    return DryRunApplyInput(
        dry_run_input_id=dry_run_input_id,
        version=kwargs.pop("version", V0362_VERSION),
        apply_candidate_id=kwargs.pop("apply_candidate_id", "apply_candidate:v0.36.1"),
        human_approval_contract_id=kwargs.pop("human_approval_contract_id", "human_approval_contract:v0.36.1"),
        apply_eligibility_decision_id=kwargs.pop("apply_eligibility_decision_id", "apply_eligibility_decision:v0.36.1"),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:test"),
        unified_diff_id=kwargs.pop("unified_diff_id", "unified_diff:test"),
        structured_patch_id=kwargs.pop("structured_patch_id", "structured_patch:test"),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:test"),
        requested_mode=kwargs.pop("requested_mode", DryRunApplyMode.UNIFIED_DIFF_DRY_RUN),
        task_summary=kwargs.pop("task_summary", "In-memory dry-run simulation request only."),
        source_refs=kwargs.pop("source_refs", [build_dry_run_apply_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(PROHIBITED_RUNTIME_ACTIONS)),
        **kwargs,
    )


def build_dry_run_source_image(source_image_id: str = "source_image:v0.36.2", **kwargs: Any) -> DryRunSourceImage:
    source_text = kwargs.pop("source_text", "alpha\nbeta\ngamma\n")
    return DryRunSourceImage(
        source_image_id=source_image_id,
        path_ref=kwargs.pop("path_ref", "src/example.py"),
        source_text=source_text,
        source_summary=kwargs.pop("source_summary", "bounded in-memory source image"),
        line_count=kwargs.pop("line_count", len(_split_lines(source_text))),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        safe_for_simulation=kwargs.pop("safe_for_simulation", True),
        **kwargs,
    )


def build_dry_run_target_file_image(target_file_image_id: str = "target_file_image:v0.36.2", **kwargs: Any) -> DryRunTargetFileImage:
    preview = _bounded_preview(kwargs.pop("simulated_after_preview", "alpha\nBETA\ngamma"))
    return DryRunTargetFileImage(
        target_file_image_id=target_file_image_id,
        path_ref=kwargs.pop("path_ref", "src/example.py"),
        original_source_image_id=kwargs.pop("original_source_image_id", "source_image:v0.36.2"),
        simulated_after_preview=preview,
        simulated_summary=kwargs.pop("simulated_summary", "virtual after-content preview only"),
        changed=kwargs.pop("changed", True),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", len(preview) >= MAX_PREVIEW_CHARS),
        ready_for_write=kwargs.pop("ready_for_write", False),
        **kwargs,
    )


def build_dry_run_hunk_input(hunk_input_id: str = "hunk_input:v0.36.2", **kwargs: Any) -> DryRunHunkInput:
    old_lines = kwargs.pop("old_lines", ["alpha", "beta", "gamma"])
    new_lines = kwargs.pop("new_lines", ["alpha", "BETA", "gamma"])
    return DryRunHunkInput(
        hunk_input_id=hunk_input_id,
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        hunk_header=kwargs.pop("hunk_header", "@@ -1,3 +1,3 @@"),
        original_context=kwargs.pop("original_context", old_lines),
        proposed_lines=kwargs.pop("proposed_lines", new_lines),
        removed_lines=kwargs.pop("removed_lines", [line for line in old_lines if line not in new_lines]),
        source_hunk_ref=kwargs.pop("source_hunk_ref", "unified_diff:test#hunk-1"),
        metadata=kwargs.pop("metadata", {"old_lines": old_lines, "new_lines": new_lines}),
        **kwargs,
    )


def build_dry_run_hunk_alignment(hunk_alignment_id: str = "hunk_alignment:v0.36.2", **kwargs: Any) -> DryRunHunkAlignment:
    return DryRunHunkAlignment(
        hunk_alignment_id=hunk_alignment_id,
        hunk_input_id=kwargs.pop("hunk_input_id", "hunk_input:v0.36.2"),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        alignment_status=kwargs.pop("alignment_status", DryRunHunkAlignmentStatus.ALIGNED_EXACT),
        matched_line_start=kwargs.pop("matched_line_start", 1),
        matched_line_end=kwargs.pop("matched_line_end", 3),
        fuzz_used=kwargs.pop("fuzz_used", 0),
        confidence=kwargs.pop("confidence", "exact"),
        summary=kwargs.pop("summary", "hunk aligned in memory; not applied"),
        **kwargs,
    )


def build_dry_run_conflict(conflict_id: str = "dry_run_conflict:v0.36.2", **kwargs: Any) -> DryRunConflict:
    return DryRunConflict(
        conflict_id=conflict_id,
        conflict_kind=kwargs.pop("conflict_kind", DryRunConflictKind.CONTEXT_NOT_FOUND),
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        hunk_input_id=kwargs.pop("hunk_input_id", "hunk_input:v0.36.2"),
        severity=kwargs.pop("severity", "blocking"),
        conflict_summary=kwargs.pop("conflict_summary", "dry-run conflict metadata"),
        evidence_preview=_bounded_preview(kwargs.pop("evidence_preview", "context unavailable")),
        blocks_future_sandbox_apply=kwargs.pop("blocks_future_sandbox_apply", True),
        requires_review=kwargs.pop("requires_review", True),
        **kwargs,
    )


def build_dry_run_simulated_file_delta(simulated_delta_id: str = "simulated_delta:v0.36.2", **kwargs: Any) -> DryRunSimulatedFileDelta:
    return DryRunSimulatedFileDelta(
        simulated_delta_id=simulated_delta_id,
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        delta_kind=kwargs.pop("delta_kind", DryRunFileDeltaKind.SIMULATED_REPLACEMENT),
        hunk_alignment_ids=kwargs.pop("hunk_alignment_ids", ["hunk_alignment:v0.36.2"]),
        conflict_ids=kwargs.pop("conflict_ids", []),
        before_preview=_bounded_preview(kwargs.pop("before_preview", "alpha\nbeta\ngamma")),
        after_preview=_bounded_preview(kwargs.pop("after_preview", "alpha\nBETA\ngamma")),
        delta_summary=kwargs.pop("delta_summary", "simulated delta metadata only"),
        changed=kwargs.pop("changed", True),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        ready_for_write=kwargs.pop("ready_for_write", False),
        ready_for_apply=kwargs.pop("ready_for_apply", False),
        **kwargs,
    )


def build_dry_run_simulated_file_result(file_result_id: str = "file_result:v0.36.2", **kwargs: Any) -> DryRunSimulatedFileResult:
    conflicts = kwargs.pop("conflicts", [])
    return DryRunSimulatedFileResult(
        file_result_id=file_result_id,
        target_path_ref=kwargs.pop("target_path_ref", "src/example.py"),
        source_image_id=kwargs.pop("source_image_id", "source_image:v0.36.2"),
        target_file_image=kwargs.pop("target_file_image", build_dry_run_target_file_image()),
        simulated_deltas=kwargs.pop("simulated_deltas", [build_dry_run_simulated_file_delta()]),
        conflicts=conflicts,
        file_result_summary=kwargs.pop("file_result_summary", "simulated file result metadata only"),
        simulation_successful=kwargs.pop("simulation_successful", not any(conflict.blocks_future_sandbox_apply for conflict in conflicts)),
        ready_for_future_sandbox_workspace_input=kwargs.pop("ready_for_future_sandbox_workspace_input", not any(conflict.blocks_future_sandbox_apply for conflict in conflicts)),
        ready_for_write=kwargs.pop("ready_for_write", False),
        ready_for_apply=kwargs.pop("ready_for_apply", False),
        **kwargs,
    )


def build_dry_run_apply_simulation_result(simulation_result_id: str = "simulation_result:v0.36.2", **kwargs: Any) -> DryRunApplySimulationResult:
    file_results = kwargs.pop("file_results", [build_dry_run_simulated_file_result()])
    conflicts = kwargs.pop("conflicts", [conflict for result in file_results for conflict in result.conflicts])
    blocking_count = kwargs.pop("blocking_conflict_count", sum(1 for conflict in conflicts if conflict.blocks_future_sandbox_apply))
    successful = kwargs.pop("simulation_successful", blocking_count == 0)
    return DryRunApplySimulationResult(
        simulation_result_id=simulation_result_id,
        version=kwargs.pop("version", V0362_VERSION),
        dry_run_input_id=kwargs.pop("dry_run_input_id", "dry_run_input:v0.36.2"),
        mode=kwargs.pop("mode", DryRunApplyMode.UNIFIED_DIFF_DRY_RUN),
        status=kwargs.pop("status", DryRunApplyStatus.SIMULATION_COMPLETED if successful else DryRunApplyStatus.SIMULATION_COMPLETED_WITH_CONFLICTS),
        readiness_level=kwargs.pop("readiness_level", DryRunApplyReadinessLevel.SIMULATED_DELTA_READY if successful else DryRunApplyReadinessLevel.CONFLICT_REPORT_READY),
        file_results=file_results,
        hunk_alignments=kwargs.pop("hunk_alignments", [build_dry_run_hunk_alignment()]),
        conflicts=conflicts,
        source_refs=kwargs.pop("source_refs", [build_dry_run_apply_source_ref()]),
        summary=kwargs.pop("summary", "dry-run simulation result metadata only"),
        conflict_count=kwargs.pop("conflict_count", len(conflicts)),
        blocking_conflict_count=blocking_count,
        simulation_successful=successful,
        eligible_for_future_sandbox_workspace_input=kwargs.pop("eligible_for_future_sandbox_workspace_input", successful and blocking_count == 0),
        ready_for_v0363_sandbox_workspace_overlay_policy=kwargs.pop("ready_for_v0363_sandbox_workspace_overlay_policy", successful and blocking_count == 0),
        ready_for_v0364_sandbox_patch_apply_engine=kwargs.pop("ready_for_v0364_sandbox_patch_apply_engine", successful and blocking_count == 0),
        **kwargs,
    )


def build_dry_run_apply_decision(decision_id: str = "dry_run_decision:v0.36.2", **kwargs: Any) -> DryRunApplyDecision:
    ready = kwargs.pop("ready_for_future_sandbox_workspace_input", True)
    return DryRunApplyDecision(
        decision_id=decision_id,
        decision_kind=kwargs.pop("decision_kind", DryRunApplyDecisionKind.ELIGIBLE_FOR_FUTURE_SANDBOX_WORKSPACE if ready else DryRunApplyDecisionKind.REQUIRE_REVIEW),
        status=kwargs.pop("status", DryRunApplyStatus.SIMULATION_COMPLETED if ready else DryRunApplyStatus.REVIEW_REQUIRED),
        summary=kwargs.pop("summary", "dry-run decision metadata only"),
        ready_for_future_sandbox_workspace_input=ready,
        **kwargs,
    )


def build_dry_run_apply_validation_finding(finding_id: str = "dry_run_finding:v0.36.2", **kwargs: Any) -> DryRunApplyValidationFinding:
    return DryRunApplyValidationFinding(
        finding_id=finding_id,
        risk_kind=kwargs.pop("risk_kind", DryRunApplyRiskKind.UNKNOWN),
        decision_kind=kwargs.pop("decision_kind", DryRunApplyDecisionKind.ALLOW_SIMULATED_DELTA_METADATA),
        summary=kwargs.pop("summary", "dry-run validation finding"),
        blocks_future_sandbox_workspace_input=kwargs.pop("blocks_future_sandbox_workspace_input", False),
        **kwargs,
    )


def build_dry_run_apply_validation_report(validation_report_id: str = "dry_run_validation:v0.36.2", **kwargs: Any) -> DryRunApplyValidationReport:
    return DryRunApplyValidationReport(
        validation_report_id=validation_report_id,
        simulation_result_id=kwargs.pop("simulation_result_id", "simulation_result:v0.36.2"),
        findings=kwargs.pop("findings", []),
        status=kwargs.pop("status", DryRunApplyStatus.SIMULATION_COMPLETED),
        summary=kwargs.pop("summary", "dry-run validation report; not patch application certification"),
        certifies_patch_application=kwargs.pop("certifies_patch_application", False),
        **kwargs,
    )


def build_dry_run_apply_report(report_id: str = "dry_run_report:v0.36.2", **kwargs: Any) -> DryRunApplyReport:
    result = kwargs.pop("simulation_result", build_dry_run_apply_simulation_result())
    return DryRunApplyReport(
        report_id=report_id,
        simulation_result=result,
        validation_report=kwargs.pop("validation_report", build_dry_run_apply_validation_report(simulation_result_id=result.simulation_result_id)),
        decision=kwargs.pop("decision", build_dry_run_apply_decision(ready_for_future_sandbox_workspace_input=result.eligible_for_future_sandbox_workspace_input)),
        summary=kwargs.pop("summary", "dry-run apply report metadata only"),
        simulation_successful=kwargs.pop("simulation_successful", result.simulation_successful),
        **kwargs,
    )


def build_dry_run_apply_run_preview(run_preview_id: str = "dry_run_preview:v0.36.2", **kwargs: Any) -> DryRunApplyRunPreview:
    return DryRunApplyRunPreview(
        run_preview_id=run_preview_id,
        simulation_result_id=kwargs.pop("simulation_result_id", "simulation_result:v0.36.2"),
        preview_summary=kwargs.pop("preview_summary", "future sandbox input preview only"),
        ready_for_future_sandbox_workspace_input=kwargs.pop("ready_for_future_sandbox_workspace_input", True),
        **kwargs,
    )


def build_dry_run_apply_no_write_guarantee(guarantee_id: str = "dry_run_no_write:v0.36.2", **kwargs: Any) -> DryRunApplyNoWriteGuarantee:
    return DryRunApplyNoWriteGuarantee(
        guarantee_id=guarantee_id,
        version=kwargs.pop("version", V0362_VERSION),
        no_sandbox_workspace_creation=kwargs.pop("no_sandbox_workspace_creation", True),
        no_sandbox_file_write=kwargs.pop("no_sandbox_file_write", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_sandbox_patch_apply=kwargs.pop("no_sandbox_patch_apply", True),
        no_patch_application=kwargs.pop("no_patch_application", True),
        no_workspace_write=kwargs.pop("no_workspace_write", True),
        no_code_edit=kwargs.pop("no_code_edit", True),
        no_apply_patch=kwargs.pop("no_apply_patch", True),
        no_git_apply=kwargs.pop("no_git_apply", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        no_autonomous_agent_runtime=kwargs.pop("no_autonomous_agent_runtime", True),
        no_independent_agent_runtime=kwargs.pop("no_independent_agent_runtime", True),
        no_multi_cycle_agentic_loop=kwargs.pop("no_multi_cycle_agentic_loop", True),
        summary=kwargs.pop("summary", "v0.36.2 dry-run writes nothing and applies nothing."),
        **kwargs,
    )


def build_v0362_readiness_report(report_id: str = "v0362_readiness_report", **kwargs: Any) -> V0362ReadinessReport:
    return V0362ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0362_VERSION),
        release_name=kwargs.pop("release_name", V0362_RELEASE_NAME),
        summary=kwargs.pop("summary", "In-memory dry-run simulation ready; write/apply/execution remain false."),
        ready_for_v0363_sandbox_workspace_overlay_policy=kwargs.pop("ready_for_v0363_sandbox_workspace_overlay_policy", True),
        ready_for_v0364_sandbox_patch_apply_engine=kwargs.pop("ready_for_v0364_sandbox_patch_apply_engine", True),
        ready_for_dry_run_apply_simulation=kwargs.pop("ready_for_dry_run_apply_simulation", True),
        ready_for_dry_run_hunk_alignment=kwargs.pop("ready_for_dry_run_hunk_alignment", True),
        ready_for_dry_run_conflict_detection=kwargs.pop("ready_for_dry_run_conflict_detection", True),
        ready_for_simulated_file_delta=kwargs.pop("ready_for_simulated_file_delta", True),
        ready_for_future_sandbox_workspace_input=kwargs.pop("ready_for_future_sandbox_workspace_input", True),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.2_dry_run_patch_apply_simulation.md"]),
        **kwargs,
    )


def build_dry_run_apply_input_from_apply_candidate(
    candidate: ApplyCandidateEnvelope,
    approval_contract: HumanApprovalContract | None = None,
    eligibility_decision: ApplyEligibilityDecision | None = None,
    **kwargs: Any,
) -> DryRunApplyInput:
    contract = approval_contract or candidate.approval_contract
    decision_id = eligibility_decision.eligibility_decision_id if eligibility_decision else "apply_eligibility_decision:v0.36.1"
    return build_dry_run_apply_input(
        apply_candidate_id=candidate.apply_candidate_id,
        human_approval_contract_id=contract.approval_contract_id,
        apply_eligibility_decision_id=decision_id,
        diff_envelope_id=candidate.diff_envelope_id,
        unified_diff_id=candidate.unified_diff_id,
        structured_patch_id=candidate.structured_patch_id,
        **kwargs,
    )


def parse_unified_diff_to_dry_run_hunks(unified_diff_text: str, policy: DryRunApplyPolicy | None = None) -> list[DryRunHunkInput]:
    active_policy = policy or default_dry_run_apply_policy()
    if not active_policy.allow_unified_diff_parse:
        return []
    if len(unified_diff_text) > active_policy.max_source_chars:
        raise ValueError("unified diff text exceeds dry-run policy bound")
    lines = unified_diff_text.splitlines()
    target_path = "unknown"
    hunks: list[DryRunHunkInput] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        if line.startswith("+++ "):
            target_path = line[4:].strip()
            if target_path.startswith("b/"):
                target_path = target_path[2:]
            index += 1
            continue
        if not line.startswith("@@"):
            index += 1
            continue
        header = line
        old_lines: list[str] = []
        new_lines: list[str] = []
        removed_lines: list[str] = []
        original_context: list[str] = []
        index += 1
        while index < len(lines) and not lines[index].startswith("@@") and not lines[index].startswith("--- ") and not lines[index].startswith("+++ "):
            body = lines[index]
            if body.startswith("\\"):
                index += 1
                continue
            marker = body[:1]
            text = body[1:] if marker in (" ", "-", "+") else body
            if marker == " ":
                old_lines.append(text)
                new_lines.append(text)
                original_context.append(text)
            elif marker == "-":
                old_lines.append(text)
                removed_lines.append(text)
                original_context.append(text)
            elif marker == "+":
                new_lines.append(text)
            else:
                old_lines.append(text)
                new_lines.append(text)
                original_context.append(text)
            index += 1
        if not old_lines and not new_lines:
            raise ValueError("malformed unified diff hunk")
        if len(hunks) >= active_policy.max_hunks:
            raise ValueError("too many hunks for dry-run policy")
        hunks.append(
            build_dry_run_hunk_input(
                hunk_input_id=f"hunk_input:v0.36.2:{len(hunks) + 1}",
                target_path_ref=target_path,
                hunk_header=header,
                original_context=original_context,
                proposed_lines=new_lines,
                removed_lines=removed_lines,
                source_hunk_ref=f"unified_diff:hunk:{len(hunks) + 1}",
                metadata={"old_lines": old_lines, "new_lines": new_lines},
            )
        )
    if not hunks:
        raise ValueError("no hunks found in unified diff text")
    return hunks


def align_dry_run_hunk_to_source_image(hunk: DryRunHunkInput, source_image: DryRunSourceImage) -> DryRunHunkAlignment:
    if not source_image.safe_for_simulation:
        return build_dry_run_hunk_alignment(
            hunk_input_id=hunk.hunk_input_id,
            target_path_ref=hunk.target_path_ref,
            alignment_status=DryRunHunkAlignmentStatus.BLOCKED,
            matched_line_start=None,
            matched_line_end=None,
            confidence="blocked",
            summary="source image is not safe for simulation",
        )
    source_lines = _split_lines(source_image.source_text)
    old_lines = list(hunk.metadata.get("old_lines", hunk.original_context))
    matches: list[int] = []
    if old_lines:
        span = len(old_lines)
        for start in range(0, len(source_lines) - span + 1):
            if source_lines[start : start + span] == old_lines:
                matches.append(start)
    if not matches:
        return build_dry_run_hunk_alignment(
            hunk_input_id=hunk.hunk_input_id,
            target_path_ref=hunk.target_path_ref,
            alignment_status=DryRunHunkAlignmentStatus.NOT_FOUND,
            matched_line_start=None,
            matched_line_end=None,
            confidence="none",
            summary="hunk context not found in supplied source image",
        )
    if len(matches) > 1:
        return build_dry_run_hunk_alignment(
            hunk_input_id=hunk.hunk_input_id,
            target_path_ref=hunk.target_path_ref,
            alignment_status=DryRunHunkAlignmentStatus.AMBIGUOUS,
            matched_line_start=matches[0] + 1,
            matched_line_end=matches[0] + len(old_lines),
            confidence="ambiguous",
            summary="hunk context matched multiple locations",
        )
    start = matches[0]
    return build_dry_run_hunk_alignment(
        hunk_input_id=hunk.hunk_input_id,
        target_path_ref=hunk.target_path_ref,
        alignment_status=DryRunHunkAlignmentStatus.ALIGNED_EXACT,
        matched_line_start=start + 1,
        matched_line_end=start + len(old_lines),
        confidence="exact",
        summary="hunk context aligned exactly in memory",
    )


def _conflict_from_alignment(alignment: DryRunHunkAlignment) -> DryRunConflict | None:
    status = DryRunHunkAlignmentStatus(alignment.alignment_status)
    if status == DryRunHunkAlignmentStatus.NOT_FOUND:
        return build_dry_run_conflict(
            conflict_id=f"conflict:{alignment.hunk_input_id}",
            conflict_kind=DryRunConflictKind.CONTEXT_NOT_FOUND,
            target_path_ref=alignment.target_path_ref,
            hunk_input_id=alignment.hunk_input_id,
            conflict_summary="hunk context not found",
        )
    if status == DryRunHunkAlignmentStatus.AMBIGUOUS:
        return build_dry_run_conflict(
            conflict_id=f"conflict:{alignment.hunk_input_id}",
            conflict_kind=DryRunConflictKind.AMBIGUOUS_CONTEXT,
            target_path_ref=alignment.target_path_ref,
            hunk_input_id=alignment.hunk_input_id,
            conflict_summary="hunk context is ambiguous",
        )
    if status == DryRunHunkAlignmentStatus.BLOCKED:
        return build_dry_run_conflict(
            conflict_id=f"conflict:{alignment.hunk_input_id}",
            conflict_kind=DryRunConflictKind.BLOCKED_TARGET,
            target_path_ref=alignment.target_path_ref,
            hunk_input_id=alignment.hunk_input_id,
            conflict_summary="target source image blocked",
        )
    return None


def simulate_dry_run_file_delta(hunk: DryRunHunkInput, source_image: DryRunSourceImage, alignment: DryRunHunkAlignment | None = None) -> DryRunSimulatedFileResult:
    active_alignment = alignment or align_dry_run_hunk_to_source_image(hunk, source_image)
    conflict = _conflict_from_alignment(active_alignment)
    if conflict is not None:
        delta = build_dry_run_simulated_file_delta(
            target_path_ref=hunk.target_path_ref,
            delta_kind=DryRunFileDeltaKind.BLOCKED_DELTA,
            hunk_alignment_ids=[active_alignment.hunk_alignment_id],
            conflict_ids=[conflict.conflict_id],
            before_preview=_bounded_preview(source_image.source_text),
            after_preview=_bounded_preview(source_image.source_text),
            delta_summary="simulation blocked by dry-run conflict",
            changed=False,
        )
        return build_dry_run_simulated_file_result(
            target_path_ref=hunk.target_path_ref,
            source_image_id=source_image.source_image_id,
            target_file_image=build_dry_run_target_file_image(
                path_ref=hunk.target_path_ref,
                original_source_image_id=source_image.source_image_id,
                simulated_after_preview=_bounded_preview(source_image.source_text),
                changed=False,
            ),
            simulated_deltas=[delta],
            conflicts=[conflict],
            simulation_successful=False,
            ready_for_future_sandbox_workspace_input=False,
        )
    source_lines = _split_lines(source_image.source_text)
    old_lines = list(hunk.metadata.get("old_lines", hunk.original_context))
    new_lines = list(hunk.metadata.get("new_lines", hunk.proposed_lines))
    start = (active_alignment.matched_line_start or 1) - 1
    end = start + len(old_lines)
    after_lines = source_lines[:start] + new_lines + source_lines[end:]
    before_preview = _bounded_preview(_join_lines(source_lines))
    after_preview = _bounded_preview(_join_lines(after_lines))
    delta_kind = DryRunFileDeltaKind.SIMULATED_REPLACEMENT
    if not old_lines and new_lines:
        delta_kind = DryRunFileDeltaKind.SIMULATED_ADDITION
    elif old_lines and not new_lines:
        delta_kind = DryRunFileDeltaKind.SIMULATED_DELETION
    delta = build_dry_run_simulated_file_delta(
        target_path_ref=hunk.target_path_ref,
        delta_kind=delta_kind,
        hunk_alignment_ids=[active_alignment.hunk_alignment_id],
        conflict_ids=[],
        before_preview=before_preview,
        after_preview=after_preview,
        delta_summary="simulated in-memory file delta; not write/apply",
        changed=before_preview != after_preview,
        truncated=len(_join_lines(after_lines)) > MAX_PREVIEW_CHARS,
    )
    target_image = build_dry_run_target_file_image(
        path_ref=hunk.target_path_ref,
        original_source_image_id=source_image.source_image_id,
        simulated_after_preview=after_preview,
        changed=delta.changed,
        truncated=delta.truncated,
    )
    return build_dry_run_simulated_file_result(
        target_path_ref=hunk.target_path_ref,
        source_image_id=source_image.source_image_id,
        target_file_image=target_image,
        simulated_deltas=[delta],
        conflicts=[],
        simulation_successful=True,
        ready_for_future_sandbox_workspace_input=True,
    )


def run_dry_run_apply_simulation(
    dry_run_input: DryRunApplyInput,
    unified_diff_text: str,
    source_images: list[DryRunSourceImage],
    policy: DryRunApplyPolicy | None = None,
) -> DryRunApplySimulationResult:
    active_policy = policy or default_dry_run_apply_policy()
    if dry_run_input.apply_candidate_id is None or dry_run_input.human_approval_contract_id is None:
        conflict = build_dry_run_conflict(
            conflict_id="conflict:missing_candidate_or_approval",
            conflict_kind=DryRunConflictKind.UNSUPPORTED_OPERATION,
            target_path_ref=None,
            hunk_input_id=None,
            conflict_summary="missing apply candidate or human approval metadata",
        )
        file_result = build_dry_run_simulated_file_result(
            target_path_ref="unknown",
            source_image_id=None,
            target_file_image=None,
            simulated_deltas=[],
            conflicts=[conflict],
            file_result_summary="simulation blocked before hunk alignment",
            simulation_successful=False,
            ready_for_future_sandbox_workspace_input=False,
        )
        return build_dry_run_apply_simulation_result(
            dry_run_input_id=dry_run_input.dry_run_input_id,
            status=DryRunApplyStatus.BLOCKED,
            readiness_level=DryRunApplyReadinessLevel.BLOCKED,
            file_results=[file_result],
            hunk_alignments=[],
            conflicts=[conflict],
            blocking_conflict_count=1,
            simulation_successful=False,
            eligible_for_future_sandbox_workspace_input=False,
            ready_for_v0363_sandbox_workspace_overlay_policy=False,
            ready_for_v0364_sandbox_patch_apply_engine=False,
        )
    try:
        hunks = parse_unified_diff_to_dry_run_hunks(unified_diff_text, active_policy)
    except ValueError as exc:
        conflict = build_dry_run_conflict(
            conflict_id="conflict:malformed_diff",
            conflict_kind=DryRunConflictKind.MALFORMED_HUNK,
            target_path_ref=None,
            hunk_input_id=None,
            conflict_summary="malformed unified diff for dry-run simulation",
            evidence_preview=str(exc),
        )
        file_result = build_dry_run_simulated_file_result(
            target_path_ref="unknown",
            source_image_id=None,
            target_file_image=None,
            simulated_deltas=[],
            conflicts=[conflict],
            file_result_summary="simulation safe-failed during diff parse",
            simulation_successful=False,
            ready_for_future_sandbox_workspace_input=False,
        )
        return build_dry_run_apply_simulation_result(
            dry_run_input_id=dry_run_input.dry_run_input_id,
            status=DryRunApplyStatus.SAFE_FAILED,
            readiness_level=DryRunApplyReadinessLevel.CONFLICT_REPORT_READY,
            file_results=[file_result],
            hunk_alignments=[],
            conflicts=[conflict],
            blocking_conflict_count=1,
            simulation_successful=False,
            eligible_for_future_sandbox_workspace_input=False,
            ready_for_v0363_sandbox_workspace_overlay_policy=False,
            ready_for_v0364_sandbox_patch_apply_engine=False,
        )
    images_by_path = {image.path_ref: image for image in source_images}
    file_results: list[DryRunSimulatedFileResult] = []
    alignments: list[DryRunHunkAlignment] = []
    conflicts: list[DryRunConflict] = []
    for hunk in hunks:
        source_image = images_by_path.get(hunk.target_path_ref)
        if source_image is None:
            conflict = build_dry_run_conflict(
                conflict_id=f"conflict:missing_source:{hunk.hunk_input_id}",
                conflict_kind=DryRunConflictKind.MISSING_TARGET_SOURCE,
                target_path_ref=hunk.target_path_ref,
                hunk_input_id=hunk.hunk_input_id,
                conflict_summary="missing in-memory source image for target",
            )
            file_result = build_dry_run_simulated_file_result(
                target_path_ref=hunk.target_path_ref,
                source_image_id=None,
                target_file_image=None,
                simulated_deltas=[],
                conflicts=[conflict],
                file_result_summary="simulation blocked by missing source image",
                simulation_successful=False,
                ready_for_future_sandbox_workspace_input=False,
            )
            file_results.append(file_result)
            conflicts.append(conflict)
            continue
        alignment = align_dry_run_hunk_to_source_image(hunk, source_image)
        alignments.append(alignment)
        file_result = simulate_dry_run_file_delta(hunk, source_image, alignment)
        file_results.append(file_result)
        conflicts.extend(file_result.conflicts)
    blocking_count = sum(1 for conflict in conflicts if conflict.blocks_future_sandbox_apply)
    successful = blocking_count == 0
    return build_dry_run_apply_simulation_result(
        dry_run_input_id=dry_run_input.dry_run_input_id,
        status=DryRunApplyStatus.SIMULATION_COMPLETED if successful else DryRunApplyStatus.SIMULATION_COMPLETED_WITH_CONFLICTS,
        readiness_level=DryRunApplyReadinessLevel.SIMULATED_DELTA_READY if successful else DryRunApplyReadinessLevel.CONFLICT_REPORT_READY,
        file_results=file_results,
        hunk_alignments=alignments,
        conflicts=conflicts,
        source_refs=dry_run_input.source_refs,
        conflict_count=len(conflicts),
        blocking_conflict_count=blocking_count,
        simulation_successful=successful,
        eligible_for_future_sandbox_workspace_input=successful,
        ready_for_v0363_sandbox_workspace_overlay_policy=successful,
        ready_for_v0364_sandbox_patch_apply_engine=successful,
    )


def validate_dry_run_apply_simulation_result(result: DryRunApplySimulationResult) -> DryRunApplyValidationReport:
    findings = [
        build_dry_run_apply_validation_finding(
            risk_kind=DryRunApplyRiskKind.PATCH_CONFLICT_RISK,
            decision_kind=DryRunApplyDecisionKind.REQUIRE_REVIEW,
            summary=conflict.conflict_summary,
            blocks_future_sandbox_workspace_input=conflict.blocks_future_sandbox_apply,
        )
        for conflict in result.conflicts
    ]
    return build_dry_run_apply_validation_report(
        simulation_result_id=result.simulation_result_id,
        findings=findings,
        status=result.status,
    )


def dry_run_apply_flags_preserve_no_write(flags: DryRunApplyFlagSet) -> bool:
    return isinstance(flags, DryRunApplyFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def dry_run_apply_policy_blocks_write_apply(policy: DryRunApplyPolicy) -> bool:
    return not any(
        getattr(policy, name)
        for name in (
            "allow_sandbox_patch_apply",
            "allow_sandbox_workspace_write",
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


def dry_run_simulated_delta_is_not_write(delta: DryRunSimulatedFileDelta) -> bool:
    return delta.ready_for_write is False and delta.ready_for_apply is False


def dry_run_apply_result_is_not_apply(result: DryRunApplySimulationResult) -> bool:
    return not any(
        getattr(result, name)
        for name in (
            "ready_for_sandbox_patch_apply",
            "ready_for_sandbox_workspace_write",
            "ready_for_live_workspace_write",
            "ready_for_patch_application",
            "ready_for_execution",
        )
    )


def dry_run_apply_decision_is_not_apply_permission(decision: DryRunApplyDecision) -> bool:
    return not any(getattr(decision, name) for name in ("ready_for_sandbox_patch_apply", "ready_for_write", "ready_for_apply", "ready_for_execution"))


def v0362_readiness_report_is_not_execution_ready(report: V0362ReadinessReport) -> bool:
    return isinstance(report, V0362ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)

