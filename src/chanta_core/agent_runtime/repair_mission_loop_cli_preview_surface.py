"""v0.40.8 CLI execution-test preview surface metadata.

This module defines preview-only command specifications and deterministic
read-only view records. It does not register a real command surface, execute
commands, run tests, submit prompts, invoke providers, invoke subagents, create
child sessions, mutate files, use network access, or open standalone runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank
from .repair_mission_loop_evidence_matrix import (
    BoundaryCoverageReadinessReport,
    BoundaryCoverageRecord,
    BoundaryCoverageSafetyReport,
    CheckpointCoverageRecord,
    DeniedActionCoverageRecord,
    ProviderPromptBoundaryCoverageRecord,
    ReadinessFlagCoverageRecord,
    RehearsalEvidenceMatrix,
    RestoreCoverageRecord,
    RuntimeClosureCoverageRecord,
    V0407IntegratedRestorePacket,
    V0408CLIExecutionTestPreviewSurfaceHandoff,
    VerifierSubagentBoundaryCoverageRecord,
    build_rehearsal_evidence_matrix,
    create_checkpoint_coverage_record,
    create_denied_action_coverage_record,
    create_provider_prompt_boundary_coverage_record,
    create_readiness_flag_coverage_record,
    create_restore_coverage_record,
    create_runtime_closure_coverage_record,
    create_verifier_subagent_boundary_coverage_record,
)
from .repair_mission_loop_provider_prompt_boundary import ProviderPromptBoundaryReadinessReport
from .repair_mission_loop_verifier_subagent_boundary import VerifierSubagentBoundaryReadinessReport


V0408_VERSION = "v0.40.8"
V0408_RELEASE_NAME = "v0.40.8 CLI Execution-Test Preview Surface & Integrated Restore Handoff"
V0408_TRACK_NAME = (
    "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + "
    "Sandbox Rehearsal + Manual Checkpoint Gate + Negative Runtime Gate "
    "Regression + Scope-Bound Human Approval + Provider / Prompt Boundary "
    "Deepening + Verifier Subagent Boundary Deepening + Rehearsal Evidence "
    "Matrix & Boundary Coverage Consolidation + CLI Execution-Test Preview Surface"
)
INTEGRATED_DOC_PATH = "docs/versions/v0.40/v0.40.8_cli_execution_test_preview_surface_restore.md"


class CLIPreviewSurfaceKind(StrEnum):
    STATUS_PREVIEW = "status_preview"
    EVIDENCE_MATRIX_PREVIEW = "evidence_matrix_preview"
    BOUNDARY_COVERAGE_PREVIEW = "boundary_coverage_preview"
    DENIED_ACTION_PREVIEW = "denied_action_preview"
    CHECKPOINT_PREVIEW = "checkpoint_preview"
    PROVIDER_PROMPT_PREVIEW = "provider_prompt_preview"
    VERIFIER_SUBAGENT_PREVIEW = "verifier_subagent_preview"
    RESTORE_SUMMARY_PREVIEW = "restore_summary_preview"
    V041_READINESS_PREVIEW = "v041_readiness_preview"
    UNSAFE_FLAG_PREVIEW = "unsafe_flag_preview"
    UNSUPPORTED_COMMAND_PREVIEW = "unsupported_command_preview"


class CLIPreviewCommandKind(StrEnum):
    REPAIR_LOOP_STATUS_PREVIEW = "repair_loop_status_preview"
    EVIDENCE_MATRIX_PREVIEW = "evidence_matrix_preview"
    BOUNDARY_COVERAGE_PREVIEW = "boundary_coverage_preview"
    DENIED_ACTIONS_PREVIEW = "denied_actions_preview"
    CHECKPOINTS_PREVIEW = "checkpoints_preview"
    PROVIDER_PROMPT_PREVIEW = "provider_prompt_preview"
    VERIFIER_SUBAGENT_PREVIEW = "verifier_subagent_preview"
    RESTORE_SUMMARY_PREVIEW = "restore_summary_preview"
    V041_READINESS_PREVIEW = "v041_readiness_preview"
    UNSAFE_FLAGS_PREVIEW = "unsafe_flags_preview"
    APPLY = "apply"
    RETEST = "retest"
    RUN_TESTS = "run_tests"
    SUBMIT_PROMPT = "submit_prompt"
    INVOKE_PROVIDER = "invoke_provider"
    INVOKE_SUBAGENT = "invoke_subagent"
    CREATE_CHILD_SESSION = "create_child_session"
    LIVE_WORKSPACE_APPLY = "live_workspace_apply"
    AUTONOMOUS_LOOP = "autonomous_loop"
    RETRY_LOOP = "retry_loop"
    DOMINION_RUNTIME = "dominion_runtime"
    PRODUCTION_CERTIFY = "production_certify"


class CLIPreviewCommandStatus(StrEnum):
    PREVIEW_ONLY = "preview_only"
    RENDERED = "rendered"
    BLOCKED = "blocked"
    UNSUPPORTED = "unsupported"
    UNSAFE_DENIED = "unsafe_denied"
    METADATA_ONLY = "metadata_only"
    NOT_EXECUTED = "not_executed"


class CLIPreviewFalseClaimKind(StrEnum):
    CLI_EXECUTION_READY = "cli_execution_ready"
    APPLY_COMMAND_READY = "apply_command_ready"
    RETEST_COMMAND_READY = "retest_command_ready"
    PROMPT_SUBMISSION_READY = "prompt_submission_ready"
    PROVIDER_INVOCATION_READY = "provider_invocation_ready"
    SUBAGENT_INVOCATION_READY = "subagent_invocation_ready"
    CHILD_SESSION_CREATION_READY = "child_session_creation_ready"
    STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY = "standalone_default_personal_runtime_ready"
    DOMINION_RUNTIME_READY = "dominion_runtime_ready"
    PRODUCTION_CERTIFIED = "production_certified"


PREVIEW_COMMAND_KINDS: tuple[str, ...] = (
    CLIPreviewCommandKind.REPAIR_LOOP_STATUS_PREVIEW.value,
    CLIPreviewCommandKind.EVIDENCE_MATRIX_PREVIEW.value,
    CLIPreviewCommandKind.BOUNDARY_COVERAGE_PREVIEW.value,
    CLIPreviewCommandKind.DENIED_ACTIONS_PREVIEW.value,
    CLIPreviewCommandKind.CHECKPOINTS_PREVIEW.value,
    CLIPreviewCommandKind.PROVIDER_PROMPT_PREVIEW.value,
    CLIPreviewCommandKind.VERIFIER_SUBAGENT_PREVIEW.value,
    CLIPreviewCommandKind.RESTORE_SUMMARY_PREVIEW.value,
    CLIPreviewCommandKind.V041_READINESS_PREVIEW.value,
    CLIPreviewCommandKind.UNSAFE_FLAGS_PREVIEW.value,
)
UNSUPPORTED_COMMAND_KINDS: tuple[str, ...] = (
    CLIPreviewCommandKind.APPLY.value,
    CLIPreviewCommandKind.RETEST.value,
    CLIPreviewCommandKind.RUN_TESTS.value,
    CLIPreviewCommandKind.SUBMIT_PROMPT.value,
    CLIPreviewCommandKind.INVOKE_PROVIDER.value,
    CLIPreviewCommandKind.INVOKE_SUBAGENT.value,
    CLIPreviewCommandKind.CREATE_CHILD_SESSION.value,
    CLIPreviewCommandKind.LIVE_WORKSPACE_APPLY.value,
    CLIPreviewCommandKind.AUTONOMOUS_LOOP.value,
    CLIPreviewCommandKind.RETRY_LOOP.value,
    CLIPreviewCommandKind.DOMINION_RUNTIME.value,
    CLIPreviewCommandKind.PRODUCTION_CERTIFY.value,
)
SAFE_ALTERNATIVES: tuple[str, ...] = (
    "view_status",
    "view_evidence_matrix",
    "view_boundary_coverage",
    "view_denied_actions",
    "view_restore_summary",
    "defer_to_v0409",
    "defer_to_v041",
    "stop",
    "do_nothing",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_cli_runtime_execution",
    "ready_for_apply_command",
    "ready_for_retest_command",
    "ready_for_test_execution",
    "ready_for_live_workspace_apply",
    "ready_for_prompt_submission_to_model",
    "ready_for_model_provider_invocation",
    "ready_for_subagent_invocation",
    "ready_for_child_session_creation",
    "ready_for_parent_raw_transcript_sharing",
    "ready_for_external_agent_execution",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_standalone_default_personal_runtime",
    "ready_for_dominion_runtime",
    "production_certified",
)
BASELINE_VERSIONS: tuple[str, ...] = (
    "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation",
    "v0.40.1 Sandbox Rehearsal Runner & Standalone Agent Readiness Clarification",
    "v0.40.2 Manual Two-Iteration Rehearsal & Human Checkpoint Enforcement",
    "v0.40.3 Negative Runtime Gate Regression & Denied Runtime Action Coverage",
    "v0.40.4 Human Checkpoint Hardening & Scope-Bound Approval Contract",
    "v0.40.5 Provider / Prompt Boundary Deepening & Integrated Restore Handoff",
    "v0.40.6 Verifier Subagent Boundary Deepening & Integrated Restore Handoff",
    "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation",
    "v0.40.8 CLI Execution-Test Preview Surface & Integrated Restore Handoff",
)
OPEN_CAPABILITIES: tuple[str, ...] = (
    "mission_loop_boundary",
    "dry_run_simulation",
    "sandbox_rehearsal",
    "manual_two_iteration_rehearsal",
    "negative_runtime_gate_regression",
    "scope_bound_checkpoint_approval",
    "prompt_dispatch_candidate_metadata",
    "prompt_submission_gate",
    "provider_invocation_gate",
    "provider_output_quarantine_contract",
    "verifier_subagent_request_draft",
    "verifier_context_isolation_contract",
    "verifier_dispatch_gate",
    "rehearsal_evidence_matrix",
    "boundary_coverage_consolidation",
    "cli_preview_surface",
    "cli_status_preview",
    "cli_evidence_matrix_preview",
    "cli_boundary_coverage_preview",
    "cli_restore_summary_preview",
    "integrated_restore_document",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "standalone_default_personal_runtime",
    "actual_cli_runtime_execution",
    "actual_apply_command",
    "actual_retest_command",
    "actual_test_execution",
    "actual_prompt_submission",
    "actual_model_provider_invocation",
    "actual_subagent_invocation",
    "actual_child_session_creation",
    "parent_raw_transcript_sharing",
    "subagent_permission_grant",
    "live_workspace_apply",
    "autonomous_loop_runtime",
    "automatic_repair_loop",
    "retry_loop",
    "network_access",
    "credential_access",
    "dominion_runtime",
    "production_certification",
)
REQUIRED_RESTORE_SECTION_IDS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "repository_baseline_assumptions",
    "version_chain_summary",
    "current_implemented_modules",
    "current_test_files",
    "current_documentation_files",
    "cli_preview_surface_summary",
    "preview_command_catalog",
    "unsupported_command_policy",
    "read_only_view_contract",
    "evidence_matrix_preview_summary",
    "boundary_coverage_preview_summary",
    "denied_action_preview_summary",
    "v041_readiness_preview_summary",
    "capability_matrix",
    "safety_flag_canonical_values",
    "standalone_runtime_status",
    "how_to_verify_this_state",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0409_handoff",
    "v041_smoke_run_status",
    "copy_paste_restore_prompt",
)


def _validate_tuple(field_name: str, value: Any) -> None:
    if not isinstance(value, tuple):
        raise TypeError(f"{field_name} must be a tuple")


def _validate_dict(field_name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{field_name} must be a dict")


def _validate_false(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False")


def _validate_true(instance: object, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must remain True")


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


@dataclass(frozen=True)
class CLIPreviewCommandSpec:
    command_id: str
    command_name: str
    command_kind: str
    description: str
    preview_only: bool
    read_only: bool
    metadata_only: bool
    execution_allowed: bool
    mutates_workspace: bool
    submits_prompt: bool
    invokes_provider: bool
    invokes_subagent: bool
    creates_child_session: bool
    uses_network: bool
    accesses_credentials: bool
    safe_alternatives: tuple[str, ...]
    expected_output_sections: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("command_id", "command_name", "command_kind", "description"):
            _require_non_blank(name, getattr(self, name))
        if self.command_kind not in set(PREVIEW_COMMAND_KINDS).union(UNSUPPORTED_COMMAND_KINDS):
            raise ValueError("command_kind must be declared")
        _validate_tuple("safe_alternatives", self.safe_alternatives)
        _validate_tuple("expected_output_sections", self.expected_output_sections)
        if not set(self.safe_alternatives).issubset(SAFE_ALTERNATIVES):
            raise ValueError("safe alternatives must be declared")
        _validate_true(self, ("preview_only", "read_only", "metadata_only"))
        _validate_false(
            self,
            (
                "execution_allowed",
                "mutates_workspace",
                "submits_prompt",
                "invokes_provider",
                "invokes_subagent",
                "creates_child_session",
                "uses_network",
                "accesses_credentials",
            ),
        )


@dataclass(frozen=True)
class CLIPreviewCommandInput:
    input_id: str
    command_kind: str
    args: tuple[str, ...]
    source: str
    requested_execution: bool
    metadata_only: bool

    def __post_init__(self) -> None:
        for name in ("input_id", "command_kind", "source"):
            _require_non_blank(name, getattr(self, name))
        _validate_tuple("args", self.args)
        if self.command_kind not in set(PREVIEW_COMMAND_KINDS).union(UNSUPPORTED_COMMAND_KINDS):
            raise ValueError("command_kind must be declared")
        _validate_true(self, ("metadata_only",))


@dataclass(frozen=True)
class CLIPreviewCommandResult:
    result_id: str
    input_id: str
    command_kind: str
    status: str
    rendered_text: str
    blocked_reason: str | None
    safe_alternative: str
    executed: bool
    mutated_workspace: bool
    submitted_prompt: bool
    invoked_provider: bool
    invoked_subagent: bool
    created_child_session: bool
    used_network: bool
    accessed_credentials: bool

    def __post_init__(self) -> None:
        for name in ("result_id", "input_id", "command_kind", "status", "rendered_text", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        if self.status not in {status.value for status in CLIPreviewCommandStatus}:
            raise ValueError("status must be declared")
        if self.safe_alternative not in SAFE_ALTERNATIVES:
            raise ValueError("safe_alternative must be declared")
        _validate_false(
            self,
            (
                "executed",
                "mutated_workspace",
                "submitted_prompt",
                "invoked_provider",
                "invoked_subagent",
                "created_child_session",
                "used_network",
                "accessed_credentials",
            ),
        )


@dataclass(frozen=True)
class CLIReadOnlyViewContract:
    contract_id: str
    view_only: bool
    read_only: bool
    preview_only: bool
    no_execution: bool
    no_workspace_mutation: bool
    no_prompt_submission: bool
    no_provider_invocation: bool
    no_subagent_invocation: bool
    no_child_session_creation: bool
    no_network: bool
    no_credentials: bool

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _validate_true(
            self,
            (
                "view_only",
                "read_only",
                "preview_only",
                "no_execution",
                "no_workspace_mutation",
                "no_prompt_submission",
                "no_provider_invocation",
                "no_subagent_invocation",
                "no_child_session_creation",
                "no_network",
                "no_credentials",
            ),
        )


@dataclass(frozen=True)
class CLIExecutionTestPreviewSurface:
    surface_id: str
    surface_kind: str
    command_specs: tuple[CLIPreviewCommandSpec, ...]
    read_only_contract: CLIReadOnlyViewContract
    preview_only: bool
    execution_surface_registered: bool
    runtime_authority_granted: bool

    def __post_init__(self) -> None:
        _require_non_blank("surface_id", self.surface_id)
        _require_non_blank("surface_kind", self.surface_kind)
        _validate_tuple("command_specs", self.command_specs)
        if self.surface_kind != "cli_execution_test_preview_surface":
            raise ValueError("surface_kind must be preview surface")
        kinds = {spec.command_kind for spec in self.command_specs}
        if set(PREVIEW_COMMAND_KINDS) != kinds:
            raise ValueError("preview surface must include only required preview command specs")
        _validate_true(self, ("preview_only",))
        _validate_false(self, ("execution_surface_registered", "runtime_authority_granted"))


@dataclass(frozen=True)
class CLIStatusPreviewView:
    view_id: str
    current_version: str
    track_name: str
    coverage_status: str
    closed_runtime_capabilities: tuple[str, ...]
    next_version_handoff: str
    standalone_runtime_status: str
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        for name in ("view_id", "current_version", "track_name", "coverage_status", "next_version_handoff", "standalone_runtime_status", "rendered_text"):
            _require_non_blank(name, getattr(self, name))
        _validate_tuple("closed_runtime_capabilities", self.closed_runtime_capabilities)
        _validate_true(self, ("metadata_only", "read_only"))


@dataclass(frozen=True)
class CLIEvidenceMatrixPreviewView:
    view_id: str
    matrix_row_count: int
    coverage_status: str
    missing_evidence_count: int
    unsafe_gap_count: int
    advisory_only_rows: tuple[str, ...]
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("coverage_status", self.coverage_status)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_tuple("advisory_only_rows", self.advisory_only_rows)
        _validate_true(self, ("metadata_only", "read_only"))


@dataclass(frozen=True)
class CLIBoundaryCoveragePreviewView:
    view_id: str
    covered_boundaries: tuple[str, ...]
    standalone_runtime_closed_boundary: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_tuple("covered_boundaries", self.covered_boundaries)
        _validate_true(self, ("standalone_runtime_closed_boundary", "metadata_only", "read_only"))


@dataclass(frozen=True)
class CLIDeniedActionPreviewView:
    view_id: str
    denied_actions: tuple[str, ...]
    decision_status: str
    safe_alternatives: tuple[str, ...]
    runtime_authority_granted: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("decision_status", self.decision_status)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_tuple("denied_actions", self.denied_actions)
        _validate_tuple("safe_alternatives", self.safe_alternatives)
        _validate_false(self, ("runtime_authority_granted",))
        _validate_true(self, ("metadata_only", "read_only"))


@dataclass(frozen=True)
class CLICheckpointPreviewView:
    view_id: str
    checkpoint_required: bool
    stale_checkpoint_invalid: bool
    broad_approval_rejected: bool
    artifact_binding_required: bool
    approval_grants_runtime_authority: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_true(self, ("checkpoint_required", "stale_checkpoint_invalid", "broad_approval_rejected", "artifact_binding_required", "metadata_only", "read_only"))
        _validate_false(self, ("approval_grants_runtime_authority",))


@dataclass(frozen=True)
class CLIProviderPromptPreviewView:
    view_id: str
    prompt_submission_blocked: bool
    provider_invocation_blocked: bool
    provider_output_quarantine_required: bool
    network_blocked: bool
    credential_blocked: bool
    provider_client_creation_blocked: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_true(
            self,
            (
                "prompt_submission_blocked",
                "provider_invocation_blocked",
                "provider_output_quarantine_required",
                "network_blocked",
                "credential_blocked",
                "provider_client_creation_blocked",
                "metadata_only",
                "read_only",
            ),
        )


@dataclass(frozen=True)
class CLIVerifierSubagentPreviewView:
    view_id: str
    verifier_request_draft_only: bool
    subagent_invocation_blocked: bool
    child_session_creation_blocked: bool
    parent_raw_transcript_sharing_blocked: bool
    verifier_result_quarantine_required: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_true(
            self,
            (
                "verifier_request_draft_only",
                "subagent_invocation_blocked",
                "child_session_creation_blocked",
                "parent_raw_transcript_sharing_blocked",
                "verifier_result_quarantine_required",
                "metadata_only",
                "read_only",
            ),
        )


@dataclass(frozen=True)
class CLIRestoreSummaryPreviewView:
    view_id: str
    integrated_doc_path: str
    copy_paste_restore_prompt_present: bool
    version_chain: tuple[str, ...]
    safety_flags_summary: str
    next_handoff: str
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        for name in ("view_id", "integrated_doc_path", "safety_flags_summary", "next_handoff", "rendered_text"):
            _require_non_blank(name, getattr(self, name))
        _validate_tuple("version_chain", self.version_chain)
        _validate_true(self, ("copy_paste_restore_prompt_present", "metadata_only", "read_only"))


@dataclass(frozen=True)
class CLIV041ReadinessPreviewView:
    view_id: str
    missing_standalone_runtime_components: tuple[str, ...]
    conservative_smoke_target: str
    possible_acceleration_signal: str
    claims_standalone_runtime_ready: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        for name in ("view_id", "conservative_smoke_target", "possible_acceleration_signal", "rendered_text"):
            _require_non_blank(name, getattr(self, name))
        _validate_tuple("missing_standalone_runtime_components", self.missing_standalone_runtime_components)
        _validate_false(self, ("claims_standalone_runtime_ready",))
        _validate_true(self, ("metadata_only", "read_only"))


@dataclass(frozen=True)
class CLIUnsafeFlagPreviewView:
    view_id: str
    unsafe_flags: dict[str, bool]
    all_unsafe_flags_false: bool
    rendered_text: str
    metadata_only: bool
    read_only: bool

    def __post_init__(self) -> None:
        _require_non_blank("view_id", self.view_id)
        _require_non_blank("rendered_text", self.rendered_text)
        _validate_dict("unsafe_flags", self.unsafe_flags)
        missing = [flag for flag in REQUIRED_FALSE_FLAGS if flag not in self.unsafe_flags]
        if missing:
            raise ValueError("unsafe flags must include all required flags")
        if self.all_unsafe_flags_false and any(self.unsafe_flags.values()):
            raise ValueError("unsafe flags must remain false")
        _validate_true(self, ("all_unsafe_flags_false", "metadata_only", "read_only"))


@dataclass(frozen=True)
class CLIUnsupportedCommandDecision:
    decision_id: str
    command_kind: str
    blocked: bool
    status: str
    reason: str
    safe_alternative: str
    executed: bool

    def __post_init__(self) -> None:
        for name in ("decision_id", "command_kind", "status", "reason", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        if self.command_kind not in UNSUPPORTED_COMMAND_KINDS:
            raise ValueError("unsupported decision must target unsupported command kind")
        if self.status not in {CLIPreviewCommandStatus.UNSAFE_DENIED.value, CLIPreviewCommandStatus.UNSUPPORTED.value}:
            raise ValueError("unsupported command status must deny or mark unsupported")
        if self.safe_alternative not in SAFE_ALTERNATIVES:
            raise ValueError("safe_alternative must be declared")
        _validate_true(self, ("blocked",))
        _validate_false(self, ("executed",))


@dataclass(frozen=True)
class CLIPreviewFalseClaimRequest:
    claim_id: str
    claim_kind: str
    claim_text: str
    source: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("claim_id", "claim_kind", "claim_text", "source"):
            _require_non_blank(name, getattr(self, name))
        _validate_tuple("evidence_refs", self.evidence_refs)
        if self.claim_kind not in {kind.value for kind in CLIPreviewFalseClaimKind}:
            raise ValueError("claim_kind must be declared")


@dataclass(frozen=True)
class CLIPreviewFalseClaimAudit:
    audit_id: str
    claim_id: str
    claim_kind: str
    claim_detected: bool
    claim_allowed: bool
    readiness_flag_modified: bool
    corrective_statement: str

    def __post_init__(self) -> None:
        for name in ("audit_id", "claim_id", "claim_kind", "corrective_statement"):
            _require_non_blank(name, getattr(self, name))
        _validate_true(self, ("claim_detected",))
        _validate_false(self, ("claim_allowed", "readiness_flag_modified"))


@dataclass(frozen=True)
class CLIPreviewSurfaceAuditRecord:
    audit_id: str
    checked_preview_specs: bool
    checked_read_only_views: bool
    checked_unsupported_denials: bool
    checked_false_claims: bool
    checked_integrated_restore_single_document: bool
    checked_no_execution_authority: bool
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _validate_tuple("notes", self.notes)
        _validate_true(
            self,
            (
                "checked_preview_specs",
                "checked_read_only_views",
                "checked_unsupported_denials",
                "checked_false_claims",
                "checked_integrated_restore_single_document",
                "checked_no_execution_authority",
            ),
        )


@dataclass(frozen=True)
class CLIPreviewSurfaceSafetyReport:
    report_id: str
    safe_for_v0408_cli_preview_surface: bool
    safe_for_cli_runtime_execution: bool
    safe_for_apply_command: bool
    safe_for_retest_command: bool
    safe_for_test_execution: bool
    safe_for_live_workspace_apply: bool
    safe_for_prompt_submission: bool
    safe_for_model_provider_invocation: bool
    safe_for_subagent_invocation: bool
    safe_for_child_session_creation: bool
    safe_for_network_access: bool
    safe_for_credential_access: bool
    safe_for_standalone_default_personal_runtime: bool
    safe_for_dominion_runtime: bool
    production_certified: bool
    requires_v0409_consolidation: bool

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_true(self, ("safe_for_v0408_cli_preview_surface", "requires_v0409_consolidation"))
        _validate_false(
            self,
            (
                "safe_for_cli_runtime_execution",
                "safe_for_apply_command",
                "safe_for_retest_command",
                "safe_for_test_execution",
                "safe_for_live_workspace_apply",
                "safe_for_prompt_submission",
                "safe_for_model_provider_invocation",
                "safe_for_subagent_invocation",
                "safe_for_child_session_creation",
                "safe_for_network_access",
                "safe_for_credential_access",
                "safe_for_standalone_default_personal_runtime",
                "safe_for_dominion_runtime",
                "production_certified",
            ),
        )


@dataclass(frozen=True)
class CLIPreviewSurfaceReadinessReport:
    report_id: str
    cli_preview_surface_defined: bool
    cli_status_preview_ready: bool
    cli_evidence_matrix_preview_ready: bool
    cli_boundary_coverage_preview_ready: bool
    cli_denied_action_preview_ready: bool
    cli_restore_summary_preview_ready: bool
    cli_v041_readiness_preview_ready: bool
    integrated_restore_document_ready: bool
    v0409_handoff_ready: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_cli_runtime_execution: bool
    ready_for_apply_command: bool
    ready_for_retest_command: bool
    ready_for_test_execution: bool
    ready_for_live_workspace_apply: bool
    ready_for_prompt_submission_to_model: bool
    ready_for_model_provider_invocation: bool
    ready_for_subagent_invocation: bool
    ready_for_child_session_creation: bool
    ready_for_parent_raw_transcript_sharing: bool
    ready_for_external_agent_execution: bool
    ready_for_autonomous_loop_runtime: bool
    ready_for_automatic_repair: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_loop: bool
    ready_for_standalone_default_personal_runtime: bool
    ready_for_dominion_runtime: bool
    production_certified: bool

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_true(
            self,
            (
                "cli_preview_surface_defined",
                "cli_status_preview_ready",
                "cli_evidence_matrix_preview_ready",
                "cli_boundary_coverage_preview_ready",
                "cli_denied_action_preview_ready",
                "cli_restore_summary_preview_ready",
                "cli_v041_readiness_preview_ready",
                "integrated_restore_document_ready",
                "v0409_handoff_ready",
            ),
        )
        _validate_false(self, REQUIRED_FALSE_FLAGS)


@dataclass(frozen=True)
class V0408IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str

    def __post_init__(self) -> None:
        for name in ("section_id", "title", "content_summary", "restore_value"):
            _require_non_blank(name, getattr(self, name))
        if self.section_id not in REQUIRED_RESTORE_SECTION_IDS:
            raise ValueError("section_id must be required for v0.40.8 restore")
        _validate_true(self, ("required",))


@dataclass(frozen=True)
class V0408IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    implemented_modules: tuple[str, ...]
    test_files: tuple[str, ...]
    docs: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    next_recommended_version: str
    next_recommended_focus: str

    def __post_init__(self) -> None:
        for name in ("snapshot_id", "current_version", "current_track", "next_recommended_version", "next_recommended_focus"):
            _require_non_blank(name, getattr(self, name))
        for name in ("baseline_versions", "implemented_modules", "test_files", "docs", "open_capabilities", "closed_capabilities"):
            _validate_tuple(name, getattr(self, name))
        if self.baseline_versions != BASELINE_VERSIONS:
            raise ValueError("baseline_versions must list v0.40.0 through v0.40.8")
        if not set(OPEN_CAPABILITIES).issubset(self.open_capabilities):
            raise ValueError("open capabilities must include v0.40.8 preview capabilities")
        if not set(CLOSED_CAPABILITIES).issubset(self.closed_capabilities):
            raise ValueError("closed capabilities must include v0.40.8 runtime closures")


@dataclass(frozen=True)
class V0408IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0408IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0408IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    required_false_flags: tuple[str, ...]
    restore_prompt_summary: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool

    def __post_init__(self) -> None:
        _require_non_blank("restore_packet_id", self.restore_packet_id)
        _require_non_blank("restore_prompt_summary", self.restore_prompt_summary)
        _require_non_blank("single_integrated_doc_path", self.single_integrated_doc_path)
        _validate_tuple("restore_sections", self.restore_sections)
        _validate_tuple("required_test_commands", self.required_test_commands)
        _validate_tuple("required_false_flags", self.required_false_flags)
        if self.single_integrated_doc_path != INTEGRATED_DOC_PATH:
            raise ValueError("v0.40.8 must use the single integrated doc path")
        if {section.section_id for section in self.restore_sections} != set(REQUIRED_RESTORE_SECTION_IDS):
            raise ValueError("all v0.40.8 restore sections must be present")
        _validate_false(self, ("separate_restore_doc_created",))


@dataclass(frozen=True)
class V0408IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool

    def __post_init__(self) -> None:
        _require_non_blank("manifest_id", self.manifest_id)
        _require_non_blank("integrated_doc_path", self.integrated_doc_path)
        if self.integrated_doc_path != INTEGRATED_DOC_PATH:
            raise ValueError("manifest must point to v0.40.8 integrated doc")
        _validate_true(self, ("integrated_doc_required", "copy_paste_restore_prompt_required", "required_sections_present", "suitable_for_new_session_handoff"))
        _validate_false(self, ("separate_restore_doc_allowed", "separate_restore_doc_created"))


@dataclass(frozen=True)
class V0409ConsolidationHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0408: tuple[str, ...]
    risk_notes: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track"):
            _require_non_blank(name, getattr(self, name))
        for name in ("recommended_focus", "required_inputs_from_v0408", "risk_notes"):
            _validate_tuple(name, getattr(self, name))
        if self.target_version != "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff":
            raise ValueError("handoff target must be v0.40.9 consolidation")


@dataclass(frozen=True)
class V041SmokeRunAccelerationCLISignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    cli_preview_surface_passed: bool
    missing_runtime_components: tuple[str, ...]
    safety_conditions_for_acceleration: tuple[str, ...]
    recommendation: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("signal_id", self.signal_id)
        _require_non_blank("conservative_target", self.conservative_target)
        _require_non_blank("recommendation", self.recommendation)
        _validate_tuple("missing_runtime_components", self.missing_runtime_components)
        _validate_tuple("safety_conditions_for_acceleration", self.safety_conditions_for_acceleration)
        _validate_dict("metadata", self.metadata)
        if self.metadata.get("ready_for_standalone_default_personal_runtime") is not False:
            raise ValueError("CLI acceleration signal must not open standalone runtime")


def create_cli_preview_command_spec(command_kind: str = CLIPreviewCommandKind.REPAIR_LOOP_STATUS_PREVIEW.value, **overrides: Any) -> CLIPreviewCommandSpec:
    defaults = {
        "command_id": f"cli-preview-{command_kind}",
        "command_name": command_kind.replace("_", "-"),
        "command_kind": command_kind,
        "description": f"Preview-only {command_kind} command metadata.",
        "preview_only": True,
        "read_only": True,
        "metadata_only": True,
        "execution_allowed": False,
        "mutates_workspace": False,
        "submits_prompt": False,
        "invokes_provider": False,
        "invokes_subagent": False,
        "creates_child_session": False,
        "uses_network": False,
        "accesses_credentials": False,
        "safe_alternatives": ("view_status", "do_nothing"),
        "expected_output_sections": ("status", "safety", "handoff"),
    }
    return CLIPreviewCommandSpec(**_with_overrides(defaults, overrides))


def create_cli_preview_command_input(command_kind: str = CLIPreviewCommandKind.REPAIR_LOOP_STATUS_PREVIEW.value, **overrides: Any) -> CLIPreviewCommandInput:
    defaults = {
        "input_id": f"cli-preview-input-{command_kind}",
        "command_kind": command_kind,
        "args": (),
        "source": "test_fixture",
        "requested_execution": False,
        "metadata_only": True,
    }
    return CLIPreviewCommandInput(**_with_overrides(defaults, overrides))


def render_cli_preview_command(command_input: CLIPreviewCommandInput | None = None, **overrides: Any) -> CLIPreviewCommandResult:
    command_input = command_input or create_cli_preview_command_input()
    if command_input.command_kind in UNSUPPORTED_COMMAND_KINDS:
        decision = create_cli_unsupported_command_decision(command_input.command_kind)
        status = decision.status
        blocked_reason = decision.reason
        safe_alternative = decision.safe_alternative
        rendered_text = f"{command_input.command_kind} is {status}; use {safe_alternative}."
    else:
        status = CLIPreviewCommandStatus.RENDERED.value
        blocked_reason = None
        safe_alternative = "view_status"
        rendered_text = f"{command_input.command_kind} rendered as preview-only metadata."
    defaults = {
        "result_id": f"cli-preview-result-{command_input.command_kind}",
        "input_id": command_input.input_id,
        "command_kind": command_input.command_kind,
        "status": status,
        "rendered_text": rendered_text,
        "blocked_reason": blocked_reason,
        "safe_alternative": safe_alternative,
        "executed": False,
        "mutated_workspace": False,
        "submitted_prompt": False,
        "invoked_provider": False,
        "invoked_subagent": False,
        "created_child_session": False,
        "used_network": False,
        "accessed_credentials": False,
    }
    return CLIPreviewCommandResult(**_with_overrides(defaults, overrides))


def create_cli_read_only_view_contract(**overrides: Any) -> CLIReadOnlyViewContract:
    defaults = {
        "contract_id": "cli-read-only-view-contract-v0408",
        "view_only": True,
        "read_only": True,
        "preview_only": True,
        "no_execution": True,
        "no_workspace_mutation": True,
        "no_prompt_submission": True,
        "no_provider_invocation": True,
        "no_subagent_invocation": True,
        "no_child_session_creation": True,
        "no_network": True,
        "no_credentials": True,
    }
    return CLIReadOnlyViewContract(**_with_overrides(defaults, overrides))


def create_cli_execution_test_preview_surface(**overrides: Any) -> CLIExecutionTestPreviewSurface:
    defaults = {
        "surface_id": "cli-execution-test-preview-surface-v0408",
        "surface_kind": "cli_execution_test_preview_surface",
        "command_specs": tuple(create_cli_preview_command_spec(command_kind=kind) for kind in PREVIEW_COMMAND_KINDS),
        "read_only_contract": create_cli_read_only_view_contract(),
        "preview_only": True,
        "execution_surface_registered": False,
        "runtime_authority_granted": False,
    }
    return CLIExecutionTestPreviewSurface(**_with_overrides(defaults, overrides))


def render_cli_status_preview_view(**overrides: Any) -> CLIStatusPreviewView:
    defaults = {
        "view_id": "cli-status-preview-v0408",
        "current_version": V0408_RELEASE_NAME,
        "track_name": V0408_TRACK_NAME,
        "coverage_status": "covered",
        "closed_runtime_capabilities": CLOSED_CAPABILITIES,
        "next_version_handoff": "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
        "standalone_runtime_status": "closed",
        "rendered_text": "v0.40.8 preview status: standalone runtime closed; v0.40.9 handoff next.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIStatusPreviewView(**_with_overrides(defaults, overrides))


def render_cli_evidence_matrix_preview_view(matrix: RehearsalEvidenceMatrix | None = None, **overrides: Any) -> CLIEvidenceMatrixPreviewView:
    matrix = matrix or build_rehearsal_evidence_matrix()
    defaults = {
        "view_id": "cli-evidence-matrix-preview-v0408",
        "matrix_row_count": len(matrix.rows),
        "coverage_status": "complete" if matrix.coverage_complete else "incomplete",
        "missing_evidence_count": matrix.missing_evidence_count,
        "unsafe_gap_count": matrix.unsafe_gap_count,
        "advisory_only_rows": tuple(row.row_id for row in matrix.rows if row.coverage_status == "advisory_only"),
        "rendered_text": f"Evidence matrix rows={len(matrix.rows)} missing={matrix.missing_evidence_count} unsafe_gaps={matrix.unsafe_gap_count}.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIEvidenceMatrixPreviewView(**_with_overrides(defaults, overrides))


def render_cli_boundary_coverage_preview_view(**overrides: Any) -> CLIBoundaryCoveragePreviewView:
    defaults = {
        "view_id": "cli-boundary-coverage-preview-v0408",
        "covered_boundaries": (
            "mission_loop_boundary",
            "sandbox_rehearsal_boundary",
            "checkpoint_boundary",
            "negative_gate_boundary",
            "provider_prompt_boundary",
            "verifier_subagent_boundary",
            "restore_boundary",
            "standalone_runtime_closed_boundary",
        ),
        "standalone_runtime_closed_boundary": True,
        "rendered_text": "Boundary coverage preview includes mission, rehearsal, checkpoint, negative gate, provider/prompt, verifier/subagent, restore, and standalone closure.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIBoundaryCoveragePreviewView(**_with_overrides(defaults, overrides))


def render_cli_denied_action_preview_view(record: DeniedActionCoverageRecord | None = None, **overrides: Any) -> CLIDeniedActionPreviewView:
    record = record or create_denied_action_coverage_record()
    defaults = {
        "view_id": "cli-denied-action-preview-v0408",
        "denied_actions": tuple(record.action_coverage),
        "decision_status": "blocked",
        "safe_alternatives": ("view_denied_actions", "do_nothing"),
        "runtime_authority_granted": False,
        "rendered_text": "Denied actions remain blocked; runtime authority is false.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIDeniedActionPreviewView(**_with_overrides(defaults, overrides))


def render_cli_checkpoint_preview_view(record: CheckpointCoverageRecord | None = None, **overrides: Any) -> CLICheckpointPreviewView:
    record = record or create_checkpoint_coverage_record()
    defaults = {
        "view_id": "cli-checkpoint-preview-v0408",
        "checkpoint_required": record.checkpoint_required_between_iterations,
        "stale_checkpoint_invalid": record.stale_checkpoint_invalid,
        "broad_approval_rejected": record.broad_approval_rejected,
        "artifact_binding_required": record.artifact_mismatch_invalid,
        "approval_grants_runtime_authority": record.approval_grants_runtime_authority,
        "rendered_text": "Checkpoint preview: stale/broad/mismatched approval blocked; no runtime authority.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLICheckpointPreviewView(**_with_overrides(defaults, overrides))


def render_cli_provider_prompt_preview_view(record: ProviderPromptBoundaryCoverageRecord | None = None, **overrides: Any) -> CLIProviderPromptPreviewView:
    record = record or create_provider_prompt_boundary_coverage_record()
    defaults = {
        "view_id": "cli-provider-prompt-preview-v0408",
        "prompt_submission_blocked": record.prompt_submission_blocked,
        "provider_invocation_blocked": record.provider_invocation_blocked,
        "provider_output_quarantine_required": record.provider_output_quarantine_required,
        "network_blocked": record.network_blocked,
        "credential_blocked": record.credential_blocked,
        "provider_client_creation_blocked": record.provider_client_creation_blocked,
        "rendered_text": "Provider/prompt preview: submission, provider, network, credential, and client creation blocked.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIProviderPromptPreviewView(**_with_overrides(defaults, overrides))


def render_cli_verifier_subagent_preview_view(record: VerifierSubagentBoundaryCoverageRecord | None = None, **overrides: Any) -> CLIVerifierSubagentPreviewView:
    record = record or create_verifier_subagent_boundary_coverage_record()
    defaults = {
        "view_id": "cli-verifier-subagent-preview-v0408",
        "verifier_request_draft_only": record.verifier_request_draft_metadata_only,
        "subagent_invocation_blocked": record.subagent_invocation_blocked,
        "child_session_creation_blocked": record.child_session_creation_blocked,
        "parent_raw_transcript_sharing_blocked": record.parent_raw_transcript_sharing_blocked,
        "verifier_result_quarantine_required": record.verifier_result_quarantine_required,
        "rendered_text": "Verifier/subagent preview: request draft only; subagent, child session, parent transcript sharing blocked.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIVerifierSubagentPreviewView(**_with_overrides(defaults, overrides))


def render_cli_restore_summary_preview_view(record: RestoreCoverageRecord | None = None, **overrides: Any) -> CLIRestoreSummaryPreviewView:
    record = record or create_restore_coverage_record()
    defaults = {
        "view_id": "cli-restore-summary-preview-v0408",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "copy_paste_restore_prompt_present": record.copy_paste_restore_prompt_exists,
        "version_chain": BASELINE_VERSIONS,
        "safety_flags_summary": "all unsafe v0.40.8 flags remain false",
        "next_handoff": "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
        "rendered_text": f"Restore summary preview: {INTEGRATED_DOC_PATH}; copy-paste prompt present.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIRestoreSummaryPreviewView(**_with_overrides(defaults, overrides))


def render_cli_v041_readiness_preview_view(**overrides: Any) -> CLIV041ReadinessPreviewView:
    defaults = {
        "view_id": "cli-v041-readiness-preview-v0408",
        "missing_standalone_runtime_components": ("ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"),
        "conservative_smoke_target": "v0.41.6",
        "possible_acceleration_signal": "non_authoritative_possible_v0414_or_v0415_if_components_narrow",
        "claims_standalone_runtime_ready": False,
        "rendered_text": "v0.41 readiness preview is non-authoritative; standalone runtime remains closed.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIV041ReadinessPreviewView(**_with_overrides(defaults, overrides))


def render_cli_unsafe_flag_preview_view(record: ReadinessFlagCoverageRecord | None = None, **overrides: Any) -> CLIUnsafeFlagPreviewView:
    record = record or create_readiness_flag_coverage_record()
    unsafe_flags = {flag: False for flag in REQUIRED_FALSE_FLAGS}
    unsafe_flags.update({flag: value for flag, value in record.unsafe_readiness_flags.items() if flag in REQUIRED_FALSE_FLAGS})
    defaults = {
        "view_id": "cli-unsafe-flag-preview-v0408",
        "unsafe_flags": unsafe_flags,
        "all_unsafe_flags_false": all(value is False for value in unsafe_flags.values()),
        "rendered_text": "Unsafe flag preview: all unsafe flags remain false.",
        "metadata_only": True,
        "read_only": True,
    }
    return CLIUnsafeFlagPreviewView(**_with_overrides(defaults, overrides))


def create_cli_unsupported_command_decision(command_kind: str = CLIPreviewCommandKind.APPLY.value, **overrides: Any) -> CLIUnsupportedCommandDecision:
    defaults = {
        "decision_id": f"unsupported-cli-command-{command_kind}",
        "command_kind": command_kind,
        "blocked": True,
        "status": CLIPreviewCommandStatus.UNSAFE_DENIED.value,
        "reason": f"{command_kind} is not available in v0.40.8 preview-only CLI surface.",
        "safe_alternative": "view_status",
        "executed": False,
    }
    return CLIUnsupportedCommandDecision(**_with_overrides(defaults, overrides))


def audit_cli_preview_false_claim(
    claim_kind: str = CLIPreviewFalseClaimKind.CLI_EXECUTION_READY.value,
    **overrides: Any,
) -> CLIPreviewFalseClaimAudit:
    request = CLIPreviewFalseClaimRequest(
        claim_id=f"claim-{claim_kind}",
        claim_kind=claim_kind,
        claim_text=f"{claim_kind} is ready.",
        source="test_fixture",
        evidence_refs=("v0408",),
    )
    defaults = {
        "audit_id": f"audit-{claim_kind}",
        "claim_id": request.claim_id,
        "claim_kind": request.claim_kind,
        "claim_detected": True,
        "claim_allowed": False,
        "readiness_flag_modified": False,
        "corrective_statement": f"{claim_kind} remains blocked in v0.40.8.",
    }
    return CLIPreviewFalseClaimAudit(**_with_overrides(defaults, overrides))


def create_cli_preview_surface_audit_record(**overrides: Any) -> CLIPreviewSurfaceAuditRecord:
    defaults = {
        "audit_id": "cli-preview-surface-audit-v0408",
        "checked_preview_specs": True,
        "checked_read_only_views": True,
        "checked_unsupported_denials": True,
        "checked_false_claims": True,
        "checked_integrated_restore_single_document": True,
        "checked_no_execution_authority": True,
        "notes": ("v0.40.8 CLI surface is preview-only",),
    }
    return CLIPreviewSurfaceAuditRecord(**_with_overrides(defaults, overrides))


def create_cli_preview_surface_safety_report(**overrides: Any) -> CLIPreviewSurfaceSafetyReport:
    defaults = {
        "report_id": "cli-preview-surface-safety-v0408",
        "safe_for_v0408_cli_preview_surface": True,
        "safe_for_cli_runtime_execution": False,
        "safe_for_apply_command": False,
        "safe_for_retest_command": False,
        "safe_for_test_execution": False,
        "safe_for_live_workspace_apply": False,
        "safe_for_prompt_submission": False,
        "safe_for_model_provider_invocation": False,
        "safe_for_subagent_invocation": False,
        "safe_for_child_session_creation": False,
        "safe_for_network_access": False,
        "safe_for_credential_access": False,
        "safe_for_standalone_default_personal_runtime": False,
        "safe_for_dominion_runtime": False,
        "production_certified": False,
        "requires_v0409_consolidation": True,
    }
    return CLIPreviewSurfaceSafetyReport(**_with_overrides(defaults, overrides))


def create_cli_preview_surface_readiness_report(**overrides: Any) -> CLIPreviewSurfaceReadinessReport:
    defaults = {
        "report_id": "cli-preview-surface-readiness-v0408",
        "cli_preview_surface_defined": True,
        "cli_status_preview_ready": True,
        "cli_evidence_matrix_preview_ready": True,
        "cli_boundary_coverage_preview_ready": True,
        "cli_denied_action_preview_ready": True,
        "cli_restore_summary_preview_ready": True,
        "cli_v041_readiness_preview_ready": True,
        "integrated_restore_document_ready": True,
        "v0409_handoff_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return CLIPreviewSurfaceReadinessReport(**_with_overrides(defaults, overrides))


def create_v0408_integrated_restore_sections() -> tuple[V0408IntegratedRestoreSection, ...]:
    return tuple(
        V0408IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.40.8 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0408_integrated_restore_context_snapshot(**overrides: Any) -> V0408IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0408",
        "current_version": V0408_RELEASE_NAME,
        "current_track": V0408_TRACK_NAME,
        "baseline_versions": BASELINE_VERSIONS,
        "implemented_modules": (
            "repair_mission_loop_boundary",
            "repair_mission_loop_rehearsal",
            "repair_mission_loop_two_iteration",
            "repair_mission_loop_negative_gates",
            "repair_mission_loop_checkpoint_hardening",
            "repair_mission_loop_provider_prompt_boundary",
            "repair_mission_loop_verifier_subagent_boundary",
            "repair_mission_loop_evidence_matrix",
            "repair_mission_loop_cli_preview_surface",
        ),
        "test_files": (
            "tests/test_v0408_cli_execution_test_preview_surface_restore.py",
            "tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py",
            "tests/test_v0406_verifier_subagent_boundary_deepening_restore.py",
            "tests/test_v0405_provider_prompt_boundary_deepening_restore.py",
            "tests/test_v0404_human_checkpoint_hardening_restore.py",
            "tests/test_v0403_negative_runtime_gate_regression.py",
            "tests/test_v0402_manual_two_iteration_rehearsal.py",
            "tests/test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",
            "tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
            "tests/test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        ),
        "docs": (INTEGRATED_DOC_PATH,),
        "open_capabilities": OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "next_recommended_version": "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
        "next_recommended_focus": "Final v0.40 consolidation and v0.41 Default Personal runtime handoff without runtime expansion",
    }
    return V0408IntegratedRestoreContextSnapshot(**_with_overrides(defaults, overrides))


def create_v0408_integrated_restore_packet(**overrides: Any) -> V0408IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0408",
        "snapshot": create_v0408_integrated_restore_context_snapshot(),
        "restore_sections": create_v0408_integrated_restore_sections(),
        "required_test_commands": (
            "focused_v0408_cli_preview_surface",
            "v0407_evidence_matrix_regression",
            "v0406_verifier_subagent_regression",
            "v0405_provider_prompt_regression",
            "v0404_checkpoint_hardening_regression",
            "v0403_negative_gate_regression",
            "v0402_manual_checkpoint_regression",
            "v0401_sandbox_rehearsal_regression",
            "v0400_boundary_regression",
            "v0399_sandbox_repair_regression",
        ),
        "required_false_flags": REQUIRED_FALSE_FLAGS,
        "restore_prompt_summary": "Continue ChantaCore after v0.40.8 without opening CLI execution authority.",
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0408IntegratedRestorePacket(**_with_overrides(defaults, overrides))


def create_v0408_integrated_restore_document_manifest(**overrides: Any) -> V0408IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0408",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0408IntegratedRestoreDocumentManifest(**_with_overrides(defaults, overrides))


def create_v0409_consolidation_handoff(**overrides: Any) -> V0409ConsolidationHandoff:
    defaults = {
        "handoff_id": "v0409-consolidation-handoff",
        "target_version": "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
        "target_track": "Standalone-Agent Preparation Track: Controlled Mission Loop Preparation Consolidation",
        "recommended_focus": (
            "consolidate v0.40.0 through v0.40.8",
            "produce final v0.40 capability matrix",
            "produce final v0.41 standalone runtime gap register",
            "produce v0.41 profile runtime startup plan",
            "no runtime expansion",
            "no actual CLI execution",
            "prepare v0.41.0 Default Personal Profile Runtime",
        ),
        "required_inputs_from_v0408": (
            "CLIExecutionTestPreviewSurface",
            "CLIPreviewSurfaceSafetyReport",
            "CLIPreviewSurfaceReadinessReport",
            "V0408IntegratedRestorePacket",
        ),
        "risk_notes": (
            "preview-only CLI must not become execution surface",
            "v0.40.9 consolidation must not start standalone runtime",
        ),
    }
    return V0409ConsolidationHandoff(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_cli_signal(
    cli_preview_surface_passed: bool = True,
    missing_runtime_components: tuple[str, ...] = ("ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"),
    **overrides: Any,
) -> V041SmokeRunAccelerationCLISignal:
    if not cli_preview_surface_passed:
        earliest = None
        recommendation = "do_not_accelerate"
    elif set(missing_runtime_components) == {"ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"}:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    elif set(missing_runtime_components).issubset({"ProfileRuntime", "CLI", "ReadOnlySkillRegistry", "AgentLoop"}):
        earliest = "v0.41.5"
        recommendation = "possible_mild_acceleration"
    else:
        earliest = "v0.41.4"
        recommendation = "possible_acceleration_after_v0409"
    defaults = {
        "signal_id": "v041-smoke-run-cli-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "cli_preview_surface_passed": cli_preview_surface_passed,
        "missing_runtime_components": missing_runtime_components,
        "safety_conditions_for_acceleration": (
            "cli_preview_surface_remains_read_only",
            "unsupported_commands_remain_denied",
            "standalone_runtime_components_remain_future_gated",
        ),
        "recommendation": recommendation,
        "metadata": {"ready_for_standalone_default_personal_runtime": False},
    }
    return V041SmokeRunAccelerationCLISignal(**_with_overrides(defaults, overrides))


def cli_preview_command_spec_preserves_no_execution(spec: CLIPreviewCommandSpec) -> bool:
    return (
        spec.preview_only
        and spec.read_only
        and spec.metadata_only
        and not spec.execution_allowed
        and not spec.mutates_workspace
        and not spec.submits_prompt
        and not spec.invokes_provider
        and not spec.invokes_subagent
        and not spec.creates_child_session
        and not spec.uses_network
        and not spec.accesses_credentials
    )


def cli_preview_result_preserves_no_execution(result: CLIPreviewCommandResult) -> bool:
    return (
        not result.executed
        and not result.mutated_workspace
        and not result.submitted_prompt
        and not result.invoked_provider
        and not result.invoked_subagent
        and not result.created_child_session
        and not result.used_network
        and not result.accessed_credentials
    )


def cli_preview_surface_is_preview_only(surface: CLIExecutionTestPreviewSurface) -> bool:
    return (
        surface.preview_only
        and not surface.execution_surface_registered
        and not surface.runtime_authority_granted
        and {spec.command_kind for spec in surface.command_specs} == set(PREVIEW_COMMAND_KINDS)
    )


def cli_readiness_preserves_no_unsafe_runtime(report: CLIPreviewSurfaceReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0408IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def v041_cli_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationCLISignal) -> bool:
    return signal.metadata.get("ready_for_standalone_default_personal_runtime") is False
