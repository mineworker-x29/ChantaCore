"""v0.40.7 rehearsal evidence matrix and boundary coverage metadata.

This layer consolidates evidence and coverage for v0.40.0 through v0.40.6. It
does not execute rehearsals, submit prompts, invoke providers, invoke
subagents, create child sessions, share parent raw transcripts, mutate a live
workspace, open standalone runtime, or certify production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank
from .repair_mission_loop_boundary import (
    DeniedRuntimeActionMetadata,
    HumanCheckpointGate,
    IterationState,
    LoopBudgetGate,
    LoopDecisionRecord,
    MissionLoopEnvelope,
    PromptSubmissionBoundary,
    ProviderBoundaryGate,
    StopConditionContract,
    V040ReadinessReport,
    VerifierSubagentBoundary,
)
from .repair_mission_loop_checkpoint_hardening import (
    CheckpointApprovalValidationResult,
    CheckpointHardeningReadinessReport,
    CheckpointHardeningSafetyReport,
    ScopeBoundCheckpointDecision,
    V0404RestorePacket,
)
from .repair_mission_loop_negative_gates import (
    DeniedRuntimeActionCoverageMatrix,
    NegativeRuntimeGateReadinessReport,
    NegativeRuntimeGateRegressionSuite,
    NegativeRuntimeGateSafetyReport,
)
from .repair_mission_loop_provider_prompt_boundary import (
    PromptDispatchCandidate,
    PromptSubmissionGateEvaluation,
    ProviderInvocationGateEvaluation,
    ProviderOutputQuarantineContract,
    ProviderPromptBoundaryReadinessReport,
    ProviderPromptBoundarySafetyReport,
    V0405IntegratedRestorePacket,
)
from .repair_mission_loop_rehearsal import (
    DefaultPersonalStandaloneGapRegister,
    SandboxRehearsalReadinessReport,
    SandboxRehearsalResult,
    SandboxRehearsalSafetyReport,
)
from .repair_mission_loop_two_iteration import (
    ManualTwoIterationReadinessReport,
    ManualTwoIterationRehearsalResult,
    ManualTwoIterationSafetyReport,
    NoAutonomousContinuationGuarantee,
    StandaloneRuntimeStillClosedRecord,
)
from .repair_mission_loop_verifier_subagent_boundary import (
    SubagentVerificationRequestDraft,
    V0406IntegratedRestorePacket,
    VerifierContextIsolationContract,
    VerifierEvidenceRequirementEvaluation,
    VerifierResultQuarantineContract,
    VerifierSubagentBoundaryReadinessReport,
    VerifierSubagentBoundarySafetyReport,
    VerifierSubagentDispatchGateEvaluation,
)


V0407_VERSION = "v0.40.7"
V0407_RELEASE_NAME = "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation"
V0407_TRACK_NAME = (
    "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + "
    "Sandbox Rehearsal + Manual Checkpoint Gate + Negative Runtime Gate "
    "Regression + Scope-Bound Human Approval + Provider / Prompt Boundary "
    "Deepening + Verifier Subagent Boundary Deepening + Rehearsal Evidence "
    "Matrix & Boundary Coverage Consolidation"
)
INTEGRATED_DOC_PATH = "docs/versions/v0.40/v0.40.7_rehearsal_evidence_matrix_boundary_coverage_restore.md"


class EvidenceCoverageKind(StrEnum):
    IMPLEMENTATION_ARTIFACT = "implementation_artifact"
    TEST_ARTIFACT = "test_artifact"
    DOCUMENTATION_ARTIFACT = "documentation_artifact"
    READINESS_FLAG = "readiness_flag"
    SAFETY_REPORT = "safety_report"
    RESTORE_PACKET = "restore_packet"
    HANDOFF_PACKET = "handoff_packet"
    AUDIT_RECORD = "audit_record"
    FALSE_CLAIM_AUDIT = "false_claim_audit"
    WITHDRAWAL_CONDITION = "withdrawal_condition"


class BoundaryCoverageKind(StrEnum):
    MISSION_LOOP_BOUNDARY = "mission_loop_boundary"
    DRY_RUN_SIMULATION = "dry_run_simulation"
    SANDBOX_REHEARSAL = "sandbox_rehearsal"
    MANUAL_TWO_ITERATION_REHEARSAL = "manual_two_iteration_rehearsal"
    HUMAN_CHECKPOINT_GATE = "human_checkpoint_gate"
    NEGATIVE_RUNTIME_GATE = "negative_runtime_gate"
    SCOPE_BOUND_CHECKPOINT_APPROVAL = "scope_bound_checkpoint_approval"
    PROMPT_SUBMISSION_GATE = "prompt_submission_gate"
    PROVIDER_INVOCATION_GATE = "provider_invocation_gate"
    PROVIDER_OUTPUT_QUARANTINE = "provider_output_quarantine"
    VERIFIER_SUBAGENT_REQUEST_DRAFT = "verifier_subagent_request_draft"
    VERIFIER_EVIDENCE_REQUIREMENT = "verifier_evidence_requirement"
    VERIFIER_CONTEXT_ISOLATION = "verifier_context_isolation"
    VERIFIER_DISPATCH_GATE = "verifier_dispatch_gate"
    VERIFIER_RESULT_QUARANTINE = "verifier_result_quarantine"
    RESTORE_HANDOFF = "restore_handoff"
    STANDALONE_RUNTIME_CLOSED = "standalone_runtime_closed"
    UNSAFE_RUNTIME_CLOSED = "unsafe_runtime_closed"


class CoverageStatus(StrEnum):
    COVERED = "covered"
    PARTIALLY_COVERED = "partially_covered"
    MISSING = "missing"
    STALE = "stale"
    ADVISORY_ONLY = "advisory_only"
    BLOCKED = "blocked"
    NOT_APPLICABLE = "not_applicable"


class EvidenceFreshnessStatus(StrEnum):
    FRESH = "fresh"
    STALE = "stale"
    UNKNOWN = "unknown"
    VERSION_MISMATCH = "version_mismatch"
    ARTIFACT_MISMATCH = "artifact_mismatch"
    TEST_MISSING = "test_missing"
    DOC_MISSING = "doc_missing"


REQUIRED_BOUNDARY_ROWS: tuple[str, ...] = (
    "v0400_mission_loop_boundary",
    "v0401_sandbox_rehearsal",
    "v0402_manual_checkpoint",
    "v0403_negative_runtime_gate",
    "v0404_scope_bound_checkpoint",
    "v0405_provider_prompt_boundary",
    "v0406_verifier_subagent_boundary",
    "restore_coverage",
    "standalone_runtime_closed",
    "unsafe_runtime_closed",
)
REQUIRED_DENIED_ACTIONS: tuple[str, ...] = (
    "model_provider_invocation",
    "prompt_submission",
    "subagent_invocation",
    "external_agent_execution",
    "automatic_repair",
    "retry_loop",
    "unbounded_multi_cycle_loop",
    "live_workspace_apply",
    "standalone_runtime_claim",
    "dominion_runtime",
    "production_certification",
    "shell_subprocess_command",
    "dependency_install",
    "network_access",
    "credential_access",
    "child_session_creation",
    "parent_raw_transcript_sharing",
    "provider_client_creation",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_execution",
    "ready_for_general_execution",
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
RUNTIME_CLOSURE_CAPABILITIES: tuple[str, ...] = (
    "standalone_default_personal_runtime",
    "actual_prompt_submission",
    "actual_model_provider_invocation",
    "actual_subagent_invocation",
    "actual_child_session_creation",
    "parent_raw_transcript_sharing",
    "live_workspace_apply",
    "autonomous_loop_runtime",
    "retry_loop",
    "network_access",
    "credential_access",
    "dominion_runtime",
    "production_certification",
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
    "verifier_role_contract",
    "verifier_evidence_requirement",
    "verifier_context_isolation_contract",
    "verifier_dispatch_gate",
    "verifier_result_quarantine_contract",
    "rehearsal_evidence_matrix",
    "boundary_coverage_consolidation",
    "integrated_restore_document",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "standalone_default_personal_runtime",
    "actual_prompt_submission",
    "actual_model_provider_invocation",
    "actual_subagent_invocation",
    "actual_child_session_creation",
    "parent_raw_transcript_sharing",
    "subagent_permission_grant",
    "subagent_chaining",
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
    "rehearsal_evidence_matrix_summary",
    "boundary_coverage_summary",
    "denied_action_coverage_summary",
    "checkpoint_coverage_summary",
    "provider_prompt_boundary_coverage_summary",
    "verifier_subagent_boundary_coverage_summary",
    "restore_coverage_summary",
    "readiness_flag_coverage_summary",
    "runtime_closure_coverage_summary",
    "capability_matrix",
    "safety_flag_canonical_values",
    "standalone_runtime_status",
    "how_to_verify_this_state",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0408_handoff",
    "v041_smoke_run_status",
    "copy_paste_restore_prompt",
)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if "v0.40" not in version and V0407_VERSION not in version:
        raise ValueError("version must be a v0.40 coverage version")


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
class RehearsalEvidenceRef:
    evidence_id: str
    version: str
    evidence_kind: str
    artifact_name: str
    artifact_path: str
    test_ref: str
    doc_ref: str
    freshness_status: str
    coverage_status: str
    note: str

    def __post_init__(self) -> None:
        for name in ("evidence_id", "version", "evidence_kind", "artifact_name", "artifact_path", "test_ref", "doc_ref", "freshness_status", "coverage_status", "note"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.evidence_kind not in {kind.value for kind in EvidenceCoverageKind}:
            raise ValueError("evidence_kind must be declared")
        if self.freshness_status not in {status.value for status in EvidenceFreshnessStatus}:
            raise ValueError("freshness_status must be declared")
        if self.coverage_status not in {status.value for status in CoverageStatus}:
            raise ValueError("coverage_status must be declared")


@dataclass(frozen=True)
class BoundaryEvidenceRef:
    evidence_id: str
    boundary_kind: str
    version: str
    implementation_ref: str
    test_ref: str
    doc_ref: str
    readiness_ref: str
    coverage_status: str
    freshness_status: str
    note: str

    def __post_init__(self) -> None:
        for name in ("evidence_id", "boundary_kind", "version", "implementation_ref", "test_ref", "doc_ref", "readiness_ref", "coverage_status", "freshness_status", "note"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.boundary_kind not in {kind.value for kind in BoundaryCoverageKind}:
            raise ValueError("boundary_kind must be declared")


@dataclass(frozen=True)
class RehearsalEvidenceMatrixRow:
    row_id: str
    version: str
    boundary_kind: str
    boundary_name: str
    implementation_evidence_refs: tuple[str, ...]
    test_evidence_refs: tuple[str, ...]
    documentation_evidence_refs: tuple[str, ...]
    readiness_flag_refs: tuple[str, ...]
    safety_report_refs: tuple[str, ...]
    restore_refs: tuple[str, ...]
    coverage_status: str
    freshness_status: str
    missing_evidence: tuple[str, ...]
    blocked_runtime_capabilities: tuple[str, ...]
    note: str

    def __post_init__(self) -> None:
        for name in ("row_id", "version", "boundary_kind", "boundary_name", "coverage_status", "freshness_status", "note"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in (
            "implementation_evidence_refs",
            "test_evidence_refs",
            "documentation_evidence_refs",
            "readiness_flag_refs",
            "safety_report_refs",
            "restore_refs",
            "missing_evidence",
            "blocked_runtime_capabilities",
        ):
            _validate_tuple(name, getattr(self, name))
        if self.boundary_kind not in {kind.value for kind in BoundaryCoverageKind}:
            raise ValueError("boundary_kind must be declared")
        if self.coverage_status not in {status.value for status in CoverageStatus}:
            raise ValueError("coverage_status must be declared")
        if self.freshness_status not in {status.value for status in EvidenceFreshnessStatus}:
            raise ValueError("freshness_status must be declared")


@dataclass(frozen=True)
class RehearsalEvidenceMatrix:
    matrix_id: str
    rows: tuple[RehearsalEvidenceMatrixRow, ...]
    required_row_ids: tuple[str, ...]
    coverage_complete: bool
    unsafe_gap_count: int
    missing_evidence_count: int
    runtime_authority_granted: bool
    production_certified: bool
    version: str = V0407_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("matrix_id", self.matrix_id)
        _validate_version(self.version)
        _validate_tuple("rows", self.rows)
        _validate_tuple("required_row_ids", self.required_row_ids)
        _validate_dict("metadata", self.metadata)
        row_ids = {row.row_id for row in self.rows}
        missing_required = tuple(row_id for row_id in self.required_row_ids if row_id not in row_ids)
        calculated_missing = sum(len(row.missing_evidence) for row in self.rows) + len(missing_required)
        if calculated_missing != self.missing_evidence_count:
            raise ValueError("missing_evidence_count must match missing evidence")
        if self.coverage_complete:
            invalid_rows = [
                row
                for row in self.rows
                if row.row_id in self.required_row_ids
                and row.coverage_status not in {CoverageStatus.COVERED.value, CoverageStatus.ADVISORY_ONLY.value}
            ]
            if missing_required or invalid_rows or self.unsafe_gap_count != 0 or self.missing_evidence_count != 0:
                raise ValueError("complete matrix requires required coverage and no unsafe or missing gaps")
        _validate_false(self, ("runtime_authority_granted", "production_certified"))


@dataclass(frozen=True)
class BoundaryCoverageRecord:
    boundary_id: str
    boundary_kind: str
    version_introduced: str
    owner_artifact: str
    owner_test: str
    owner_doc: str
    opened_as_metadata_only: bool
    runtime_authority_granted: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("boundary_id", "boundary_kind", "version_introduced", "owner_artifact", "owner_test", "owner_doc", "coverage_status"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version_introduced)
        _validate_tuple("evidence_refs", self.evidence_refs)
        if self.boundary_kind not in {kind.value for kind in BoundaryCoverageKind}:
            raise ValueError("boundary_kind must be declared")
        _validate_false(self, ("runtime_authority_granted",))


@dataclass(frozen=True)
class DeniedActionCoverageRecord:
    record_id: str
    action_coverage: dict[str, str]
    all_required_actions_covered: bool
    all_denied_actions_blocked: bool
    authority_granted: bool
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_dict("action_coverage", self.action_coverage)
        _validate_tuple("evidence_refs", self.evidence_refs)
        missing = [action for action in REQUIRED_DENIED_ACTIONS if action not in self.action_coverage]
        if self.all_required_actions_covered and missing:
            raise ValueError("all required denied actions must be covered")
        invalid = [status for status in self.action_coverage.values() if status not in {CoverageStatus.BLOCKED.value, CoverageStatus.NOT_APPLICABLE.value}]
        if self.all_denied_actions_blocked and invalid:
            raise ValueError("denied actions must be blocked or not applicable")
        _validate_false(self, ("authority_granted",))


@dataclass(frozen=True)
class CheckpointCoverageRecord:
    record_id: str
    checkpoint_required_between_iterations: bool
    missing_checkpoint_blocks_second_iteration: bool
    stale_checkpoint_invalid: bool
    artifact_mismatch_invalid: bool
    broad_approval_rejected: bool
    approval_grants_runtime_authority: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_true(
            self,
            (
                "checkpoint_required_between_iterations",
                "missing_checkpoint_blocks_second_iteration",
                "stale_checkpoint_invalid",
                "artifact_mismatch_invalid",
                "broad_approval_rejected",
            ),
        )
        _validate_false(self, ("approval_grants_runtime_authority",))


@dataclass(frozen=True)
class ProviderPromptBoundaryCoverageRecord:
    record_id: str
    prompt_candidate_metadata_only: bool
    prompt_submission_blocked: bool
    provider_invocation_blocked: bool
    provider_client_creation_blocked: bool
    network_blocked: bool
    credential_blocked: bool
    provider_output_quarantine_required: bool
    direct_provider_output_persistence_blocked: bool
    direct_provider_output_execution_blocked: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_true(
            self,
            (
                "prompt_candidate_metadata_only",
                "prompt_submission_blocked",
                "provider_invocation_blocked",
                "provider_client_creation_blocked",
                "network_blocked",
                "credential_blocked",
                "provider_output_quarantine_required",
                "direct_provider_output_persistence_blocked",
                "direct_provider_output_execution_blocked",
            ),
        )


@dataclass(frozen=True)
class VerifierSubagentBoundaryCoverageRecord:
    record_id: str
    verifier_request_draft_metadata_only: bool
    subagent_invocation_blocked: bool
    child_session_creation_blocked: bool
    parent_raw_transcript_sharing_blocked: bool
    subagent_permission_grant_blocked: bool
    context_isolation_required: bool
    evidence_requirement_required: bool
    verifier_result_quarantine_required: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_true(
            self,
            (
                "verifier_request_draft_metadata_only",
                "subagent_invocation_blocked",
                "child_session_creation_blocked",
                "parent_raw_transcript_sharing_blocked",
                "subagent_permission_grant_blocked",
                "context_isolation_required",
                "evidence_requirement_required",
                "verifier_result_quarantine_required",
            ),
        )


@dataclass(frozen=True)
class RestoreCoverageRecord:
    record_id: str
    v0404_restore_document_exists: bool
    v0405_integrated_restore_document_exists: bool
    v0406_integrated_restore_document_exists: bool
    v0407_integrated_restore_document_exists: bool
    copy_paste_restore_prompt_exists: bool
    capability_matrix_exists: bool
    safety_flags_table_exists: bool
    next_version_handoff_exists: bool
    restore_claims_standalone_runtime_opened: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_true(
            self,
            (
                "v0404_restore_document_exists",
                "v0405_integrated_restore_document_exists",
                "v0406_integrated_restore_document_exists",
                "v0407_integrated_restore_document_exists",
                "copy_paste_restore_prompt_exists",
                "capability_matrix_exists",
                "safety_flags_table_exists",
                "next_version_handoff_exists",
            ),
        )
        _validate_false(self, ("restore_claims_standalone_runtime_opened",))


@dataclass(frozen=True)
class ReadinessFlagCoverageRecord:
    record_id: str
    unsafe_readiness_flags: dict[str, bool]
    all_unsafe_flags_false: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_dict("unsafe_readiness_flags", self.unsafe_readiness_flags)
        _validate_tuple("evidence_refs", self.evidence_refs)
        missing = [flag for flag in REQUIRED_FALSE_FLAGS if flag not in self.unsafe_readiness_flags]
        if missing:
            raise ValueError("all unsafe readiness flags must be represented")
        if self.all_unsafe_flags_false and any(self.unsafe_readiness_flags.values()):
            raise ValueError("unsafe readiness flags must remain false")


@dataclass(frozen=True)
class RuntimeClosureCoverageRecord:
    record_id: str
    closed_capabilities: dict[str, bool]
    all_required_runtime_capabilities_closed: bool
    coverage_status: str
    evidence_refs: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_dict("closed_capabilities", self.closed_capabilities)
        _validate_tuple("evidence_refs", self.evidence_refs)
        missing = [capability for capability in RUNTIME_CLOSURE_CAPABILITIES if capability not in self.closed_capabilities]
        if missing:
            raise ValueError("all runtime closure capabilities must be represented")
        if self.all_required_runtime_capabilities_closed and any(value is not True for value in self.closed_capabilities.values()):
            raise ValueError("all runtime capabilities must be closed")


@dataclass(frozen=True)
class BoundaryCoverageGap:
    gap_id: str
    gap_kind: str
    description: str
    blocking: bool
    evidence_refs: tuple[str, ...]
    recommended_target: str

    def __post_init__(self) -> None:
        for name in ("gap_id", "gap_kind", "description", "recommended_target"):
            _require_non_blank(name, getattr(self, name))
        _validate_tuple("evidence_refs", self.evidence_refs)
        if self.gap_kind not in {
            "blocking_gap",
            "non_blocking_gap",
            "documentation_gap",
            "test_gap",
            "future_track_gap",
            "v0408_handoff_item",
            "v041_runtime_item",
        }:
            raise ValueError("gap_kind must be declared")
        if self.gap_kind == "blocking_gap" and self.blocking is not True:
            raise ValueError("blocking_gap must be blocking")


@dataclass(frozen=True)
class BoundaryCoverageGapRegister:
    register_id: str
    gaps: tuple[BoundaryCoverageGap, ...]
    blocking_gap_count: int
    non_blocking_gap_count: int
    unsafe_runtime_gap_count: int
    coverage_can_complete: bool

    def __post_init__(self) -> None:
        _require_non_blank("register_id", self.register_id)
        _validate_tuple("gaps", self.gaps)
        if sum(1 for gap in self.gaps if gap.blocking) != self.blocking_gap_count:
            raise ValueError("blocking_gap_count must match blocking gaps")
        if sum(1 for gap in self.gaps if not gap.blocking) != self.non_blocking_gap_count:
            raise ValueError("non_blocking_gap_count must match non-blocking gaps")
        if self.coverage_can_complete and (self.blocking_gap_count or self.unsafe_runtime_gap_count):
            raise ValueError("coverage cannot complete with blocking or unsafe runtime gaps")


@dataclass(frozen=True)
class BoundaryCoverageAuditRecord:
    audit_id: str
    checked_matrix_rows: bool
    checked_boundary_records: bool
    checked_denied_action_coverage: bool
    checked_checkpoint_coverage: bool
    checked_provider_prompt_coverage: bool
    checked_verifier_subagent_coverage: bool
    checked_restore_coverage: bool
    checked_readiness_flags: bool
    checked_runtime_closure: bool
    checked_no_runtime_authority: bool
    notes: tuple[str, ...]

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _validate_tuple("notes", self.notes)
        _validate_true(
            self,
            (
                "checked_matrix_rows",
                "checked_boundary_records",
                "checked_denied_action_coverage",
                "checked_checkpoint_coverage",
                "checked_provider_prompt_coverage",
                "checked_verifier_subagent_coverage",
                "checked_restore_coverage",
                "checked_readiness_flags",
                "checked_runtime_closure",
                "checked_no_runtime_authority",
            ),
        )


@dataclass(frozen=True)
class BoundaryCoverageSafetyReport:
    report_id: str
    safe_for_v0407_coverage_consolidation: bool
    safe_for_runtime_execution: bool
    safe_for_live_workspace_apply: bool
    safe_for_model_provider_invocation: bool
    safe_for_prompt_submission: bool
    safe_for_subagent_invocation: bool
    safe_for_child_session_creation: bool
    safe_for_parent_raw_transcript_sharing: bool
    safe_for_network_access: bool
    safe_for_credential_access: bool
    safe_for_standalone_default_personal_runtime: bool
    safe_for_dominion_runtime: bool
    production_certified: bool
    requires_v0408_cli_preview_surface: bool

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_true(self, ("safe_for_v0407_coverage_consolidation", "requires_v0408_cli_preview_surface"))
        _validate_false(
            self,
            (
                "safe_for_runtime_execution",
                "safe_for_live_workspace_apply",
                "safe_for_model_provider_invocation",
                "safe_for_prompt_submission",
                "safe_for_subagent_invocation",
                "safe_for_child_session_creation",
                "safe_for_parent_raw_transcript_sharing",
                "safe_for_network_access",
                "safe_for_credential_access",
                "safe_for_standalone_default_personal_runtime",
                "safe_for_dominion_runtime",
                "production_certified",
            ),
        )


@dataclass(frozen=True)
class BoundaryCoverageReadinessReport:
    report_id: str
    rehearsal_evidence_matrix_defined: bool
    boundary_coverage_consolidation_ready: bool
    denied_action_coverage_ready: bool
    checkpoint_coverage_ready: bool
    provider_prompt_boundary_coverage_ready: bool
    verifier_subagent_boundary_coverage_ready: bool
    restore_coverage_ready: bool
    integrated_restore_document_ready: bool
    v0408_handoff_ready: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
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
                "rehearsal_evidence_matrix_defined",
                "boundary_coverage_consolidation_ready",
                "denied_action_coverage_ready",
                "checkpoint_coverage_ready",
                "provider_prompt_boundary_coverage_ready",
                "verifier_subagent_boundary_coverage_ready",
                "restore_coverage_ready",
                "integrated_restore_document_ready",
                "v0408_handoff_ready",
            ),
        )
        _validate_false(self, REQUIRED_FALSE_FLAGS)


@dataclass(frozen=True)
class V0407IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str

    def __post_init__(self) -> None:
        for name in ("section_id", "title", "content_summary", "restore_value"):
            _require_non_blank(name, getattr(self, name))
        if self.section_id not in REQUIRED_RESTORE_SECTION_IDS:
            raise ValueError("section_id must be required for v0.40.7 restore")
        _validate_true(self, ("required",))


@dataclass(frozen=True)
class V0407IntegratedRestoreContextSnapshot:
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
        if tuple(self.baseline_versions) != BASELINE_VERSIONS:
            raise ValueError("baseline_versions must list v0.40.0 through v0.40.7")
        if not set(OPEN_CAPABILITIES).issubset(set(self.open_capabilities)):
            raise ValueError("open capabilities must include v0.40.7 coverage capabilities")
        if not set(CLOSED_CAPABILITIES).issubset(set(self.closed_capabilities)):
            raise ValueError("closed capabilities must include unsafe runtime closures")


@dataclass(frozen=True)
class V0407IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0407IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0407IntegratedRestoreSection, ...]
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
            raise ValueError("v0.40.7 must use the single integrated doc path")
        if {section.section_id for section in self.restore_sections} != set(REQUIRED_RESTORE_SECTION_IDS):
            raise ValueError("all restore sections must be present")
        _validate_false(self, ("separate_restore_doc_created",))


@dataclass(frozen=True)
class V0407IntegratedRestoreDocumentManifest:
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
            raise ValueError("manifest must point to v0.40.7 integrated doc")
        _validate_true(self, ("integrated_doc_required", "copy_paste_restore_prompt_required", "required_sections_present", "suitable_for_new_session_handoff"))
        _validate_false(self, ("separate_restore_doc_allowed", "separate_restore_doc_created"))


@dataclass(frozen=True)
class V0408CLIExecutionTestPreviewSurfaceHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0407: tuple[str, ...]
    risk_notes: tuple[str, ...]

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track"):
            _require_non_blank(name, getattr(self, name))
        for name in ("recommended_focus", "required_inputs_from_v0407", "risk_notes"):
            _validate_tuple(name, getattr(self, name))
        if self.target_version != "v0.40.8 CLI Execution-Test Preview Surface":
            raise ValueError("handoff target must be v0.40.8 CLI Execution-Test Preview Surface")


@dataclass(frozen=True)
class V041SmokeRunAccelerationCoverageSignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    coverage_passed: bool
    blocking_runtime_gaps: tuple[str, ...]
    safety_conditions_for_acceleration: tuple[str, ...]
    recommendation: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("signal_id", self.signal_id)
        _require_non_blank("conservative_target", self.conservative_target)
        _require_non_blank("recommendation", self.recommendation)
        _validate_tuple("blocking_runtime_gaps", self.blocking_runtime_gaps)
        _validate_tuple("safety_conditions_for_acceleration", self.safety_conditions_for_acceleration)
        _validate_dict("metadata", self.metadata)
        if self.metadata.get("ready_for_standalone_default_personal_runtime") is not False:
            raise ValueError("coverage acceleration signal must not open standalone runtime")


def create_rehearsal_evidence_ref(**overrides: Any) -> RehearsalEvidenceRef:
    defaults = {
        "evidence_id": "evidence-ref-v0407",
        "version": V0407_VERSION,
        "evidence_kind": EvidenceCoverageKind.IMPLEMENTATION_ARTIFACT.value,
        "artifact_name": "RehearsalEvidenceMatrix",
        "artifact_path": "src/chanta_core/agent_runtime/repair_mission_loop_evidence_matrix.py",
        "test_ref": "tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py",
        "doc_ref": INTEGRATED_DOC_PATH,
        "freshness_status": EvidenceFreshnessStatus.FRESH.value,
        "coverage_status": CoverageStatus.COVERED.value,
        "note": "v0.40.7 coverage evidence metadata",
    }
    return RehearsalEvidenceRef(**_with_overrides(defaults, overrides))


def create_boundary_evidence_ref(**overrides: Any) -> BoundaryEvidenceRef:
    defaults = {
        "evidence_id": "boundary-evidence-ref-v0407",
        "boundary_kind": BoundaryCoverageKind.MISSION_LOOP_BOUNDARY.value,
        "version": "v0.40.0",
        "implementation_ref": "repair_mission_loop_boundary.py",
        "test_ref": "tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
        "doc_ref": "docs/versions/v0.40/v0.40.0_controlled_multi_iteration_mission_loop_boundary_foundation.md",
        "readiness_ref": "V040ReadinessReport",
        "coverage_status": CoverageStatus.COVERED.value,
        "freshness_status": EvidenceFreshnessStatus.FRESH.value,
        "note": "boundary evidence is covered",
    }
    return BoundaryEvidenceRef(**_with_overrides(defaults, overrides))


def create_rehearsal_evidence_matrix_row(**overrides: Any) -> RehearsalEvidenceMatrixRow:
    defaults = {
        "row_id": "v0407_default_row",
        "version": V0407_VERSION,
        "boundary_kind": BoundaryCoverageKind.RESTORE_HANDOFF.value,
        "boundary_name": "v0.40.7 integrated restore and coverage",
        "implementation_evidence_refs": ("repair_mission_loop_evidence_matrix.py",),
        "test_evidence_refs": ("tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py",),
        "documentation_evidence_refs": (INTEGRATED_DOC_PATH,),
        "readiness_flag_refs": ("BoundaryCoverageReadinessReport",),
        "safety_report_refs": ("BoundaryCoverageSafetyReport",),
        "restore_refs": ("V0407IntegratedRestorePacket",),
        "coverage_status": CoverageStatus.COVERED.value,
        "freshness_status": EvidenceFreshnessStatus.FRESH.value,
        "missing_evidence": (),
        "blocked_runtime_capabilities": CLOSED_CAPABILITIES,
        "note": "coverage-only row",
    }
    return RehearsalEvidenceMatrixRow(**_with_overrides(defaults, overrides))


def _default_matrix_rows() -> tuple[RehearsalEvidenceMatrixRow, ...]:
    row_specs = (
        ("v0400_mission_loop_boundary", "v0.40.0", BoundaryCoverageKind.MISSION_LOOP_BOUNDARY.value, "mission loop boundary / dry-run", "repair_mission_loop_boundary.py", "tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py", "docs/versions/v0.40/v0.40.0_controlled_multi_iteration_mission_loop_boundary_foundation.md", "V040ReadinessReport", "BoundaryCoverageSafetyReport"),
        ("v0401_sandbox_rehearsal", "v0.40.1", BoundaryCoverageKind.SANDBOX_REHEARSAL.value, "sandbox rehearsal", "repair_mission_loop_rehearsal.py", "tests/test_v0401_sandbox_rehearsal_runner_standalone_readiness.py", "docs/versions/v0.40/v0.40.1_sandbox_rehearsal_runner_standalone_readiness.md", "SandboxRehearsalReadinessReport", "SandboxRehearsalSafetyReport"),
        ("v0402_manual_checkpoint", "v0.40.2", BoundaryCoverageKind.HUMAN_CHECKPOINT_GATE.value, "manual two-iteration checkpoint", "repair_mission_loop_two_iteration.py", "tests/test_v0402_manual_two_iteration_rehearsal.py", "docs/versions/v0.40/v0.40.2_human_checkpoint_enforcement.md", "ManualTwoIterationReadinessReport", "ManualTwoIterationSafetyReport"),
        ("v0403_negative_runtime_gate", "v0.40.3", BoundaryCoverageKind.NEGATIVE_RUNTIME_GATE.value, "negative runtime gate", "repair_mission_loop_negative_gates.py", "tests/test_v0403_negative_runtime_gate_regression.py", "docs/versions/v0.40/v0.40.3_negative_runtime_gate_regression.md", "NegativeRuntimeGateReadinessReport", "NegativeRuntimeGateSafetyReport"),
        ("v0404_scope_bound_checkpoint", "v0.40.4", BoundaryCoverageKind.SCOPE_BOUND_CHECKPOINT_APPROVAL.value, "scope-bound checkpoint approval", "repair_mission_loop_checkpoint_hardening.py", "tests/test_v0404_human_checkpoint_hardening_restore.py", "docs/versions/v0.40/v0.40.4_human_checkpoint_hardening.md", "CheckpointHardeningReadinessReport", "CheckpointHardeningSafetyReport"),
        ("v0405_provider_prompt_boundary", "v0.40.5", BoundaryCoverageKind.PROVIDER_INVOCATION_GATE.value, "provider / prompt boundary", "repair_mission_loop_provider_prompt_boundary.py", "tests/test_v0405_provider_prompt_boundary_deepening_restore.py", "docs/versions/v0.40/v0.40.5_provider_prompt_boundary_deepening_restore.md", "ProviderPromptBoundaryReadinessReport", "ProviderPromptBoundarySafetyReport"),
        ("v0406_verifier_subagent_boundary", "v0.40.6", BoundaryCoverageKind.VERIFIER_DISPATCH_GATE.value, "verifier subagent boundary", "repair_mission_loop_verifier_subagent_boundary.py", "tests/test_v0406_verifier_subagent_boundary_deepening_restore.py", "docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening_restore.md", "VerifierSubagentBoundaryReadinessReport", "VerifierSubagentBoundarySafetyReport"),
        ("restore_coverage", V0407_VERSION, BoundaryCoverageKind.RESTORE_HANDOFF.value, "restore coverage", "repair_mission_loop_evidence_matrix.py", "tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py", INTEGRATED_DOC_PATH, "BoundaryCoverageReadinessReport", "BoundaryCoverageSafetyReport"),
        ("standalone_runtime_closed", V0407_VERSION, BoundaryCoverageKind.STANDALONE_RUNTIME_CLOSED.value, "standalone runtime closed coverage", "repair_mission_loop_evidence_matrix.py", "tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py", INTEGRATED_DOC_PATH, "ready_for_standalone_default_personal_runtime=False", "BoundaryCoverageSafetyReport"),
        ("unsafe_runtime_closed", V0407_VERSION, BoundaryCoverageKind.UNSAFE_RUNTIME_CLOSED.value, "unsafe runtime closed coverage", "repair_mission_loop_evidence_matrix.py", "tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py", INTEGRATED_DOC_PATH, "unsafe readiness flags false", "BoundaryCoverageSafetyReport"),
    )
    return tuple(
        create_rehearsal_evidence_matrix_row(
            row_id=row_id,
            version=version,
            boundary_kind=boundary_kind,
            boundary_name=boundary_name,
            implementation_evidence_refs=(implementation_ref,),
            test_evidence_refs=(test_ref,),
            documentation_evidence_refs=(doc_ref,),
            readiness_flag_refs=(readiness_ref,),
            safety_report_refs=(safety_ref,),
            restore_refs=("V0407IntegratedRestorePacket",),
            blocked_runtime_capabilities=CLOSED_CAPABILITIES,
            note=f"{boundary_name} covered by v0.40.7 matrix",
        )
        for row_id, version, boundary_kind, boundary_name, implementation_ref, test_ref, doc_ref, readiness_ref, safety_ref in row_specs
    )


def build_rehearsal_evidence_matrix(**overrides: Any) -> RehearsalEvidenceMatrix:
    rows = overrides.pop("rows", _default_matrix_rows())
    missing_evidence_count = sum(len(row.missing_evidence) for row in rows)
    defaults = {
        "matrix_id": "rehearsal-evidence-matrix-v0407",
        "rows": rows,
        "required_row_ids": REQUIRED_BOUNDARY_ROWS,
        "coverage_complete": missing_evidence_count == 0,
        "unsafe_gap_count": 0,
        "missing_evidence_count": missing_evidence_count,
        "runtime_authority_granted": False,
        "production_certified": False,
    }
    return RehearsalEvidenceMatrix(**_with_overrides(defaults, overrides))


def create_boundary_coverage_record(**overrides: Any) -> BoundaryCoverageRecord:
    defaults = {
        "boundary_id": "boundary-coverage-v0407",
        "boundary_kind": BoundaryCoverageKind.MISSION_LOOP_BOUNDARY.value,
        "version_introduced": "v0.40.0",
        "owner_artifact": "MissionLoopEnvelope",
        "owner_test": "tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
        "owner_doc": "docs/versions/v0.40/v0.40.0_controlled_multi_iteration_mission_loop_boundary_foundation.md",
        "opened_as_metadata_only": True,
        "runtime_authority_granted": False,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("mission-loop-boundary",),
    }
    return BoundaryCoverageRecord(**_with_overrides(defaults, overrides))


def create_denied_action_coverage_record(**overrides: Any) -> DeniedActionCoverageRecord:
    action_coverage = {action: CoverageStatus.BLOCKED.value for action in REQUIRED_DENIED_ACTIONS}
    defaults = {
        "record_id": "denied-action-coverage-v0407",
        "action_coverage": action_coverage,
        "all_required_actions_covered": True,
        "all_denied_actions_blocked": True,
        "authority_granted": False,
        "evidence_refs": ("DeniedRuntimeActionCoverageMatrix",),
    }
    return DeniedActionCoverageRecord(**_with_overrides(defaults, overrides))


def create_checkpoint_coverage_record(**overrides: Any) -> CheckpointCoverageRecord:
    defaults = {
        "record_id": "checkpoint-coverage-v0407",
        "checkpoint_required_between_iterations": True,
        "missing_checkpoint_blocks_second_iteration": True,
        "stale_checkpoint_invalid": True,
        "artifact_mismatch_invalid": True,
        "broad_approval_rejected": True,
        "approval_grants_runtime_authority": False,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("ManualTwoIterationReadinessReport", "CheckpointHardeningReadinessReport"),
    }
    return CheckpointCoverageRecord(**_with_overrides(defaults, overrides))


def create_provider_prompt_boundary_coverage_record(**overrides: Any) -> ProviderPromptBoundaryCoverageRecord:
    defaults = {
        "record_id": "provider-prompt-boundary-coverage-v0407",
        "prompt_candidate_metadata_only": True,
        "prompt_submission_blocked": True,
        "provider_invocation_blocked": True,
        "provider_client_creation_blocked": True,
        "network_blocked": True,
        "credential_blocked": True,
        "provider_output_quarantine_required": True,
        "direct_provider_output_persistence_blocked": True,
        "direct_provider_output_execution_blocked": True,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("ProviderPromptBoundaryReadinessReport", "ProviderOutputQuarantineContract"),
    }
    return ProviderPromptBoundaryCoverageRecord(**_with_overrides(defaults, overrides))


def create_verifier_subagent_boundary_coverage_record(**overrides: Any) -> VerifierSubagentBoundaryCoverageRecord:
    defaults = {
        "record_id": "verifier-subagent-boundary-coverage-v0407",
        "verifier_request_draft_metadata_only": True,
        "subagent_invocation_blocked": True,
        "child_session_creation_blocked": True,
        "parent_raw_transcript_sharing_blocked": True,
        "subagent_permission_grant_blocked": True,
        "context_isolation_required": True,
        "evidence_requirement_required": True,
        "verifier_result_quarantine_required": True,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("VerifierSubagentBoundaryReadinessReport", "VerifierResultQuarantineContract"),
    }
    return VerifierSubagentBoundaryCoverageRecord(**_with_overrides(defaults, overrides))


def create_restore_coverage_record(**overrides: Any) -> RestoreCoverageRecord:
    defaults = {
        "record_id": "restore-coverage-v0407",
        "v0404_restore_document_exists": True,
        "v0405_integrated_restore_document_exists": True,
        "v0406_integrated_restore_document_exists": True,
        "v0407_integrated_restore_document_exists": True,
        "copy_paste_restore_prompt_exists": True,
        "capability_matrix_exists": True,
        "safety_flags_table_exists": True,
        "next_version_handoff_exists": True,
        "restore_claims_standalone_runtime_opened": False,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("V0407IntegratedRestorePacket", INTEGRATED_DOC_PATH),
    }
    return RestoreCoverageRecord(**_with_overrides(defaults, overrides))


def create_readiness_flag_coverage_record(**overrides: Any) -> ReadinessFlagCoverageRecord:
    defaults = {
        "record_id": "readiness-flag-coverage-v0407",
        "unsafe_readiness_flags": {flag: False for flag in REQUIRED_FALSE_FLAGS},
        "all_unsafe_flags_false": True,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("BoundaryCoverageReadinessReport",),
    }
    return ReadinessFlagCoverageRecord(**_with_overrides(defaults, overrides))


def create_runtime_closure_coverage_record(**overrides: Any) -> RuntimeClosureCoverageRecord:
    defaults = {
        "record_id": "runtime-closure-coverage-v0407",
        "closed_capabilities": {capability: True for capability in RUNTIME_CLOSURE_CAPABILITIES},
        "all_required_runtime_capabilities_closed": True,
        "coverage_status": CoverageStatus.COVERED.value,
        "evidence_refs": ("BoundaryCoverageSafetyReport", "BoundaryCoverageReadinessReport"),
    }
    return RuntimeClosureCoverageRecord(**_with_overrides(defaults, overrides))


def create_boundary_coverage_gap(**overrides: Any) -> BoundaryCoverageGap:
    defaults = {
        "gap_id": "v0408-cli-preview-handoff-gap",
        "gap_kind": "v0408_handoff_item",
        "description": "CLI preview surface is deferred to v0.40.8.",
        "blocking": False,
        "evidence_refs": ("V0408CLIExecutionTestPreviewSurfaceHandoff",),
        "recommended_target": "v0.40.8 CLI Execution-Test Preview Surface",
    }
    return BoundaryCoverageGap(**_with_overrides(defaults, overrides))


def build_boundary_coverage_gap_register(
    gaps: tuple[BoundaryCoverageGap, ...] | None = None,
    **overrides: Any,
) -> BoundaryCoverageGapRegister:
    gaps = gaps if gaps is not None else (create_boundary_coverage_gap(),)
    blocking_gap_count = sum(1 for gap in gaps if gap.blocking)
    non_blocking_gap_count = sum(1 for gap in gaps if not gap.blocking)
    unsafe_runtime_gap_count = sum(1 for gap in gaps if gap.blocking and "runtime" in gap.description.lower())
    defaults = {
        "register_id": "boundary-coverage-gap-register-v0407",
        "gaps": gaps,
        "blocking_gap_count": blocking_gap_count,
        "non_blocking_gap_count": non_blocking_gap_count,
        "unsafe_runtime_gap_count": unsafe_runtime_gap_count,
        "coverage_can_complete": blocking_gap_count == 0 and unsafe_runtime_gap_count == 0,
    }
    return BoundaryCoverageGapRegister(**_with_overrides(defaults, overrides))


def create_boundary_coverage_audit_record(**overrides: Any) -> BoundaryCoverageAuditRecord:
    defaults = {
        "audit_id": "boundary-coverage-audit-v0407",
        "checked_matrix_rows": True,
        "checked_boundary_records": True,
        "checked_denied_action_coverage": True,
        "checked_checkpoint_coverage": True,
        "checked_provider_prompt_coverage": True,
        "checked_verifier_subagent_coverage": True,
        "checked_restore_coverage": True,
        "checked_readiness_flags": True,
        "checked_runtime_closure": True,
        "checked_no_runtime_authority": True,
        "notes": ("v0.40.7 consolidates coverage only",),
    }
    return BoundaryCoverageAuditRecord(**_with_overrides(defaults, overrides))


def create_boundary_coverage_safety_report(
    matrix: RehearsalEvidenceMatrix | None = None,
    **overrides: Any,
) -> BoundaryCoverageSafetyReport:
    matrix = matrix or build_rehearsal_evidence_matrix()
    defaults = {
        "report_id": "boundary-coverage-safety-v0407",
        "safe_for_v0407_coverage_consolidation": matrix.coverage_complete and matrix.unsafe_gap_count == 0,
        "safe_for_runtime_execution": False,
        "safe_for_live_workspace_apply": False,
        "safe_for_model_provider_invocation": False,
        "safe_for_prompt_submission": False,
        "safe_for_subagent_invocation": False,
        "safe_for_child_session_creation": False,
        "safe_for_parent_raw_transcript_sharing": False,
        "safe_for_network_access": False,
        "safe_for_credential_access": False,
        "safe_for_standalone_default_personal_runtime": False,
        "safe_for_dominion_runtime": False,
        "production_certified": False,
        "requires_v0408_cli_preview_surface": True,
    }
    return BoundaryCoverageSafetyReport(**_with_overrides(defaults, overrides))


def create_boundary_coverage_readiness_report(**overrides: Any) -> BoundaryCoverageReadinessReport:
    defaults = {
        "report_id": "boundary-coverage-readiness-v0407",
        "rehearsal_evidence_matrix_defined": True,
        "boundary_coverage_consolidation_ready": True,
        "denied_action_coverage_ready": True,
        "checkpoint_coverage_ready": True,
        "provider_prompt_boundary_coverage_ready": True,
        "verifier_subagent_boundary_coverage_ready": True,
        "restore_coverage_ready": True,
        "integrated_restore_document_ready": True,
        "v0408_handoff_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return BoundaryCoverageReadinessReport(**_with_overrides(defaults, overrides))


def create_v0407_integrated_restore_sections() -> tuple[V0407IntegratedRestoreSection, ...]:
    return tuple(
        V0407IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.40.7 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0407_integrated_restore_context_snapshot(**overrides: Any) -> V0407IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0407",
        "current_version": V0407_RELEASE_NAME,
        "current_track": V0407_TRACK_NAME,
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
        ),
        "test_files": (
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
        "next_recommended_version": "v0.40.8 CLI Execution-Test Preview Surface",
        "next_recommended_focus": "Preview-only CLI views for status, evidence matrix, coverage, restore summary, and readiness gaps",
    }
    return V0407IntegratedRestoreContextSnapshot(**_with_overrides(defaults, overrides))


def create_v0407_integrated_restore_packet(**overrides: Any) -> V0407IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0407",
        "snapshot": create_v0407_integrated_restore_context_snapshot(),
        "restore_sections": create_v0407_integrated_restore_sections(),
        "required_test_commands": (
            r"py -m pytest tests\test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py",
            r"py -m pytest tests\test_v0406_verifier_subagent_boundary_deepening_restore.py",
            r"py -m pytest tests\test_v0405_provider_prompt_boundary_deepening_restore.py",
            r"py -m pytest tests\test_v0404_human_checkpoint_hardening_restore.py",
            r"py -m pytest tests\test_v0403_negative_runtime_gate_regression.py",
            r"py -m pytest tests\test_v0402_manual_two_iteration_rehearsal.py",
            r"py -m pytest tests\test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",
            r"py -m pytest tests\test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
            r"py -m pytest tests\test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        ),
        "required_false_flags": REQUIRED_FALSE_FLAGS,
        "restore_prompt_summary": "Continue ChantaCore after v0.40.7 without opening runtime authority.",
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0407IntegratedRestorePacket(**_with_overrides(defaults, overrides))


def create_v0407_integrated_restore_document_manifest(**overrides: Any) -> V0407IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0407",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0407IntegratedRestoreDocumentManifest(**_with_overrides(defaults, overrides))


def create_v0408_cli_execution_test_preview_surface_handoff(**overrides: Any) -> V0408CLIExecutionTestPreviewSurfaceHandoff:
    defaults = {
        "handoff_id": "v0408-cli-execution-test-preview-surface-handoff",
        "target_version": "v0.40.8 CLI Execution-Test Preview Surface",
        "target_track": "Standalone-Agent Preparation Track: CLI Execution-Test Preview Surface",
        "recommended_focus": (
            "preview-only CLI surface",
            "status command",
            "evidence matrix view command",
            "boundary coverage view command",
            "denied action coverage view command",
            "restore summary view command",
            "v0.41 readiness gap view command",
            "no apply",
            "no retest execution",
            "no prompt submission",
            "no provider invocation",
            "no subagent invocation",
            "no standalone runtime",
        ),
        "required_inputs_from_v0407": (
            "RehearsalEvidenceMatrix",
            "BoundaryCoverageGapRegister",
            "BoundaryCoverageSafetyReport",
            "V0407IntegratedRestorePacket",
        ),
        "risk_notes": (
            "CLI preview must remain view-only",
            "execution-test wording must not become command execution",
        ),
    }
    return V0408CLIExecutionTestPreviewSurfaceHandoff(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_coverage_signal(
    coverage_passed: bool = True,
    blocking_runtime_gaps: tuple[str, ...] = ("ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"),
    **overrides: Any,
) -> V041SmokeRunAccelerationCoverageSignal:
    if not coverage_passed:
        earliest = None
        recommendation = "do_not_accelerate"
    elif set(blocking_runtime_gaps) == {"ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"}:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    elif set(blocking_runtime_gaps).issubset({"CLI", "ProfileRuntime"}):
        earliest = "v0.41.5"
        recommendation = "possible_mild_acceleration"
    else:
        earliest = "v0.41.4"
        recommendation = "possible_acceleration_after_v0408_and_read_only_registry"
    defaults = {
        "signal_id": "v041-smoke-run-coverage-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "coverage_passed": coverage_passed,
        "blocking_runtime_gaps": blocking_runtime_gaps,
        "safety_conditions_for_acceleration": (
            "coverage_matrix_complete",
            "unsafe_gap_count_zero",
            "cli_preview_surface_read_only",
            "standalone_runtime_components_remain_future_gated",
        ),
        "recommendation": recommendation,
        "metadata": {"ready_for_standalone_default_personal_runtime": False},
    }
    return V041SmokeRunAccelerationCoverageSignal(**_with_overrides(defaults, overrides))


def rehearsal_evidence_matrix_is_coverage_only(matrix: RehearsalEvidenceMatrix) -> bool:
    return matrix.runtime_authority_granted is False and matrix.production_certified is False


def denied_action_coverage_blocks_all_required_actions(record: DeniedActionCoverageRecord) -> bool:
    return (
        record.all_required_actions_covered
        and record.all_denied_actions_blocked
        and record.authority_granted is False
        and all(record.action_coverage[action] in {CoverageStatus.BLOCKED.value, CoverageStatus.NOT_APPLICABLE.value} for action in REQUIRED_DENIED_ACTIONS)
    )


def readiness_flag_coverage_preserves_false(record: ReadinessFlagCoverageRecord) -> bool:
    return record.all_unsafe_flags_false and all(record.unsafe_readiness_flags[flag] is False for flag in REQUIRED_FALSE_FLAGS)


def runtime_closure_coverage_preserves_closed(record: RuntimeClosureCoverageRecord) -> bool:
    return record.all_required_runtime_capabilities_closed and all(record.closed_capabilities[capability] is True for capability in RUNTIME_CLOSURE_CAPABILITIES)


def boundary_coverage_readiness_preserves_no_unsafe_runtime(report: BoundaryCoverageReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0407IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def v041_coverage_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationCoverageSignal) -> bool:
    return signal.metadata.get("ready_for_standalone_default_personal_runtime") is False
