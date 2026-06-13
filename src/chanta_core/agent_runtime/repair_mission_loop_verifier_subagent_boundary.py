"""v0.40.6 verifier subagent boundary deepening metadata.

This layer separates verifier request drafts, role contracts, evidence checks,
context isolation, dispatch gates, and result quarantine from actual verifier
subagent invocation. It does not create child sessions, share parent raw
transcripts, grant subagent permissions, invoke providers, submit prompts, open
standalone runtime, or certify production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank
from .repair_mission_loop_boundary import (
    DeniedRuntimeActionMetadata,
    LoopDecisionRecord,
    V040ReadinessReport,
    VerifierSubagentBoundary,
)
from .repair_mission_loop_negative_gates import (
    NegativeRuntimeGateDecision,
    NegativeRuntimeGateReadinessReport,
    NegativeRuntimeRequest,
    RuntimeFalseClaimDetection,
)
from .repair_mission_loop_provider_prompt_boundary import (
    PromptDispatchCandidate,
    PromptSubmissionGatePolicy,
    ProviderInvocationGatePolicy,
    ProviderPromptBoundaryReadinessReport,
    V0405IntegratedRestorePacket,
    V0406VerifierSubagentBoundaryHandoff,
)


V0406_VERSION = "v0.40.6"
V0406_RELEASE_NAME = "v0.40.6 Verifier Subagent Boundary Deepening & Integrated Restore Handoff"
V0406_TRACK_NAME = (
    "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + "
    "Sandbox Rehearsal + Manual Checkpoint Gate + Negative Runtime Gate "
    "Regression + Scope-Bound Human Approval + Provider / Prompt Boundary "
    "Deepening + Verifier Subagent Boundary Deepening"
)


class VerifierSubagentBoundaryKind(StrEnum):
    REQUEST_DRAFT = "verifier_request_draft"
    ROLE_CONTRACT = "verifier_role_contract"
    EVIDENCE_REQUIREMENT = "verifier_evidence_requirement"
    CONTEXT_ISOLATION = "verifier_context_isolation"
    PERMISSION_SCOPE = "verifier_permission_scope"
    DISPATCH_GATE = "verifier_dispatch_gate"
    RESULT_QUARANTINE = "verifier_result_quarantine"


class VerifierRoleKind(StrEnum):
    EVIDENCE_REVIEWER = "evidence_reviewer"
    BOUNDARY_REVIEWER = "boundary_reviewer"
    SAFETY_INVARIANT_REVIEWER = "safety_invariant_reviewer"
    RESTORE_DOCUMENT_REVIEWER = "restore_document_reviewer"
    TEST_RESULT_REVIEWER = "test_result_reviewer"
    READINESS_FLAG_REVIEWER = "readiness_flag_reviewer"


class VerifierRequestStatus(StrEnum):
    DRAFT = "draft"
    EVIDENCE_INCOMPLETE = "evidence_incomplete"
    EVIDENCE_ELIGIBLE_FOR_DRAFT = "evidence_eligible_for_draft"
    DISPATCH_BLOCKED = "dispatch_blocked"


class VerifierDispatchStatus(StrEnum):
    NOT_REQUESTED = "not_requested"
    REQUESTED_AS_METADATA = "requested_as_metadata"
    BLOCKED = "blocked"
    NO_OP = "no_op"


class VerifierSubagentFalseClaimKind(StrEnum):
    VERIFIER_SUBAGENT_INVOCATION_READY = "verifier_subagent_invocation_ready"
    VERIFIER_CHILD_SESSION_READY = "verifier_child_session_ready"
    PARENT_RAW_TRANSCRIPT_SHARING_READY = "parent_raw_transcript_sharing_ready"
    VERIFIER_PERMISSION_GRANT_READY = "verifier_permission_grant_ready"
    VERIFIER_RESULT_TRUSTED = "verifier_result_trusted"
    VERIFIER_RESULT_DIRECT_PERSISTENCE_READY = "verifier_result_direct_persistence_ready"
    VERIFIER_RESULT_DIRECT_PROCESS_STATE_UPDATE_READY = "verifier_result_direct_process_state_update_ready"
    VERIFIER_RESULT_DIRECT_MEMORY_WRITE_READY = "verifier_result_direct_memory_write_ready"
    SUBAGENT_CHAINING_READY = "subagent_chaining_ready"
    STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY = "standalone_default_personal_runtime_ready"
    PRODUCTION_CERTIFIED = "production_certified"


ALLOWED_VERIFIER_ROLES: tuple[str, ...] = tuple(role.value for role in VerifierRoleKind)
FORBIDDEN_VERIFIER_ROLES: tuple[str, ...] = (
    "executor",
    "patch_applier",
    "provider_caller",
    "prompt_submitter",
    "live_workspace_operator",
    "autonomous_repair_agent",
    "dominion_operator",
    "production_certifier",
)
REQUIRED_EVIDENCE_TYPES: tuple[str, ...] = (
    "loop_decision_ref",
    "checkpoint_decision_ref",
    "safety_report_ref",
    "negative_gate_report_ref",
    "provider_prompt_boundary_report_ref",
    "restore_document_ref",
    "readiness_report_ref",
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
REQUIRED_RESTORE_SECTION_IDS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "repository_baseline_assumptions",
    "version_chain_summary",
    "current_implemented_modules",
    "current_test_files",
    "current_documentation_files",
    "capability_matrix",
    "safety_flag_canonical_values",
    "standalone_runtime_status",
    "verifier_subagent_boundary_summary",
    "evidence_requirement_summary",
    "context_isolation_summary",
    "verifier_result_quarantine_summary",
    "how_to_verify_this_state",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0407_handoff",
    "v041_smoke_run_status",
    "copy_paste_restore_prompt",
)
BASELINE_VERSIONS: tuple[str, ...] = (
    "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation",
    "v0.40.1 Sandbox Rehearsal Runner & Standalone Agent Readiness Clarification",
    "v0.40.2 Manual Two-Iteration Rehearsal & Human Checkpoint Enforcement",
    "v0.40.3 Negative Runtime Gate Regression & Denied Runtime Action Coverage",
    "v0.40.4 Human Checkpoint Hardening & Scope-Bound Approval Contract",
    "v0.40.5 Provider / Prompt Boundary Deepening & Integrated Restore Handoff",
    "v0.40.6 Verifier Subagent Boundary Deepening & Integrated Restore Handoff",
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
INTEGRATED_DOC_PATH = "docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening_restore.md"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0406_VERSION not in version:
        raise ValueError("version must include v0.40.6")


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
class VerifierEvidenceRequirement:
    requirement_id: str
    required_evidence_types: tuple[str, ...]
    provided_evidence_refs: dict[str, str]
    evidence_must_match: bool
    metadata_only: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("requirement_id", self.requirement_id)
        _validate_version(self.version)
        _validate_tuple("required_evidence_types", self.required_evidence_types)
        _validate_dict("provided_evidence_refs", self.provided_evidence_refs)
        _validate_dict("metadata", self.metadata)
        if not set(REQUIRED_EVIDENCE_TYPES).issubset(set(self.required_evidence_types)):
            raise ValueError("required evidence types must include v0.40.6 evidence refs")
        _validate_true(self, ("evidence_must_match", "metadata_only"))


@dataclass(frozen=True)
class VerifierEvidenceRequirementEvaluation:
    evaluation_id: str
    requirement_ref: str
    missing_evidence_types: tuple[str, ...]
    mismatched_evidence_types: tuple[str, ...]
    complete: bool
    eligible_for_verifier_draft: bool
    invocation_authority_granted: bool
    metadata_only: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("evaluation_id", self.evaluation_id)
        _require_non_blank("requirement_ref", self.requirement_ref)
        _validate_version(self.version)
        _validate_tuple("missing_evidence_types", self.missing_evidence_types)
        _validate_tuple("mismatched_evidence_types", self.mismatched_evidence_types)
        _validate_dict("metadata", self.metadata)
        if self.eligible_for_verifier_draft and not self.complete:
            raise ValueError("draft eligibility requires complete evidence")
        _validate_false(self, ("invocation_authority_granted",))
        _validate_true(self, ("metadata_only",))


@dataclass(frozen=True)
class VerifierRoleContract:
    contract_id: str
    verifier_role_kind: str
    role_description: str
    allowed_role: bool
    creates_subagent: bool
    invokes_subagent: bool
    grants_runtime_authority: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("contract_id", "verifier_role_kind", "role_description"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.verifier_role_kind in FORBIDDEN_VERIFIER_ROLES:
            raise ValueError("forbidden verifier role is not allowed")
        if self.verifier_role_kind not in ALLOWED_VERIFIER_ROLES:
            raise ValueError("verifier_role_kind must be an allowed review/evidence role")
        _validate_true(self, ("allowed_role",))
        _validate_false(self, ("creates_subagent", "invokes_subagent", "grants_runtime_authority"))


@dataclass(frozen=True)
class VerifierContextIsolationContract:
    contract_id: str
    parent_raw_transcript_shared: bool
    parent_hidden_context_shared: bool
    parent_credentials_shared: bool
    parent_runtime_authority_shared: bool
    summary_packet_required: bool
    structured_input_required: bool
    evidence_refs_required: bool
    child_context_isolated: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(
            self,
            (
                "parent_raw_transcript_shared",
                "parent_hidden_context_shared",
                "parent_credentials_shared",
                "parent_runtime_authority_shared",
            ),
        )
        _validate_true(self, ("summary_packet_required", "structured_input_required", "evidence_refs_required", "child_context_isolated"))


@dataclass(frozen=True)
class VerifierPermissionScope:
    scope_id: str
    read_only_metadata_scope: bool
    workspace_write_allowed: bool
    live_workspace_apply_allowed: bool
    shell_allowed: bool
    network_allowed: bool
    credential_access_allowed: bool
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    subagent_chaining_allowed: bool
    dominion_authority_allowed: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scope_id", self.scope_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("read_only_metadata_scope",))
        _validate_false(
            self,
            (
                "workspace_write_allowed",
                "live_workspace_apply_allowed",
                "shell_allowed",
                "network_allowed",
                "credential_access_allowed",
                "provider_invocation_allowed",
                "prompt_submission_allowed",
                "subagent_chaining_allowed",
                "dominion_authority_allowed",
            ),
        )


@dataclass(frozen=True)
class SubagentVerificationRequestDraft:
    request_id: str
    verifier_role_ref: str
    evidence_requirement_ref: str
    context_isolation_ref: str
    permission_scope_ref: str
    request_status: str
    metadata_only: bool
    draft_only: bool
    invocation_requested: bool
    invocation_allowed: bool
    subagent_invoked: bool
    child_session_created: bool
    parent_raw_transcript_shared: bool
    runtime_authority_granted: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("request_id", "verifier_role_ref", "evidence_requirement_ref", "context_isolation_ref", "permission_scope_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.request_status not in {status.value for status in VerifierRequestStatus}:
            raise ValueError("request_status must be a v0.40.6 verifier request status")
        _validate_true(self, ("metadata_only", "draft_only"))
        _validate_false(
            self,
            ("invocation_allowed", "subagent_invoked", "child_session_created", "parent_raw_transcript_shared", "runtime_authority_granted"),
        )


@dataclass(frozen=True)
class VerifierSubagentDispatchGatePolicy:
    policy_id: str
    deny_by_default: bool
    invocation_allowed: bool
    child_session_creation_allowed: bool
    parent_context_sharing_allowed: bool
    permission_grant_allowed: bool
    metadata_only: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("deny_by_default", "metadata_only"))
        _validate_false(self, ("invocation_allowed", "child_session_creation_allowed", "parent_context_sharing_allowed", "permission_grant_allowed"))


@dataclass(frozen=True)
class VerifierSubagentDispatchGateEvaluation:
    evaluation_id: str
    request_ref: str
    policy_ref: str
    blocked: bool
    subagent_invoked: bool
    child_session_created: bool
    parent_raw_transcript_shared: bool
    executed: bool
    metadata_only: bool
    decision_ref: str | None
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evaluation_id", "request_ref", "policy_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("blocked", "metadata_only"))
        _validate_false(self, ("subagent_invoked", "child_session_created", "parent_raw_transcript_shared", "executed"))


@dataclass(frozen=True)
class VerifierSubagentInvocationBlockedDecision:
    decision_id: str
    request_ref: str
    blocked: bool
    subagent_invoked: bool
    child_session_created: bool
    runtime_authority_granted: bool
    reason: str
    safe_alternative: str
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "request_ref", "reason", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("blocked",))
        _validate_false(self, ("subagent_invoked", "child_session_created", "runtime_authority_granted"))


@dataclass(frozen=True)
class VerifierParentContextBoundary:
    boundary_id: str
    summary_packet_only: bool
    parent_raw_transcript_shared: bool
    parent_hidden_context_shared: bool
    parent_credentials_shared: bool
    parent_runtime_authority_shared: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("summary_packet_only",))
        _validate_false(self, ("parent_raw_transcript_shared", "parent_hidden_context_shared", "parent_credentials_shared", "parent_runtime_authority_shared"))


@dataclass(frozen=True)
class VerifierReturnEnvelopeContract:
    contract_id: str
    summary_only_return: bool
    raw_child_transcript_return_allowed: bool
    evidence_refs_required: bool
    structured_result_required: bool
    human_review_required: bool
    direct_process_state_update_allowed: bool
    direct_memory_write_allowed: bool
    direct_runtime_decision_allowed: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("summary_only_return", "evidence_refs_required", "structured_result_required", "human_review_required"))
        _validate_false(self, ("raw_child_transcript_return_allowed", "direct_process_state_update_allowed", "direct_memory_write_allowed", "direct_runtime_decision_allowed"))


@dataclass(frozen=True)
class VerifierResultQuarantineContract:
    contract_id: str
    raw_verifier_result_trusted: bool
    direct_persistence_allowed: bool
    direct_process_state_update_allowed: bool
    direct_memory_write_allowed: bool
    direct_execution_allowed: bool
    requires_schema_validation: bool
    requires_human_review: bool
    requires_provenance: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("raw_verifier_result_trusted", "direct_persistence_allowed", "direct_process_state_update_allowed", "direct_memory_write_allowed", "direct_execution_allowed"))
        _validate_true(self, ("requires_schema_validation", "requires_human_review", "requires_provenance"))


@dataclass(frozen=True)
class VerifierResultQuarantineEnvelope:
    envelope_id: str
    contract_ref: str
    quarantined: bool
    validated: bool
    human_reviewed: bool
    eligible_for_persistence: bool
    eligible_for_process_state: bool
    eligible_for_memory: bool
    eligible_for_execution: bool
    metadata_only: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("envelope_id", self.envelope_id)
        _require_non_blank("contract_ref", self.contract_ref)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("quarantined", "metadata_only"))
        _validate_false(self, ("validated", "human_reviewed", "eligible_for_persistence", "eligible_for_process_state", "eligible_for_memory", "eligible_for_execution"))


@dataclass(frozen=True)
class VerifierSubagentAuthorityBoundary:
    boundary_id: str
    allows_subagent_invocation: bool
    allows_child_session_creation: bool
    allows_parent_raw_transcript_sharing: bool
    allows_workspace_write: bool
    allows_live_workspace_apply: bool
    allows_shell_execution: bool
    allows_network_access: bool
    allows_credential_access: bool
    allows_provider_invocation: bool
    allows_prompt_submission: bool
    allows_subagent_chaining: bool
    allows_runtime_execution: bool
    allows_standalone_default_personal_runtime: bool
    allows_production_certification: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(
            self,
            (
                "allows_subagent_invocation",
                "allows_child_session_creation",
                "allows_parent_raw_transcript_sharing",
                "allows_workspace_write",
                "allows_live_workspace_apply",
                "allows_shell_execution",
                "allows_network_access",
                "allows_credential_access",
                "allows_provider_invocation",
                "allows_prompt_submission",
                "allows_subagent_chaining",
                "allows_runtime_execution",
                "allows_standalone_default_personal_runtime",
                "allows_production_certification",
            ),
        )


@dataclass(frozen=True)
class VerifierSubagentFalseClaimRequest:
    claim_id: str
    claim_kind: str
    claim_text: str
    source: str
    evidence_refs: tuple[str, ...]
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("claim_id", "claim_kind", "claim_text", "source"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.claim_kind not in {item.value for item in VerifierSubagentFalseClaimKind}:
            raise ValueError("claim_kind must be a v0.40.6 false claim kind")


@dataclass(frozen=True)
class VerifierSubagentFalseClaimAudit:
    audit_id: str
    claim_id: str
    claim_kind: str
    claim_detected: bool
    claim_allowed: bool
    readiness_flag_modified: bool
    corrective_statement: str
    must_block_release_claim: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("audit_id", "claim_id", "claim_kind", "corrective_statement"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("claim_detected", "must_block_release_claim"))
        _validate_false(self, ("claim_allowed", "readiness_flag_modified"))


@dataclass(frozen=True)
class VerifierSubagentBoundaryAuditRecord:
    audit_id: str
    checked_role_contract: bool
    checked_evidence_requirement: bool
    checked_context_isolation: bool
    checked_permission_scope: bool
    checked_dispatch_gate: bool
    checked_result_quarantine: bool
    checked_false_claims_blocked: bool
    checked_integrated_restore_single_document: bool
    notes: tuple[str, ...]
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _validate_version(self.version)
        _validate_tuple("notes", self.notes)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("checked_role_contract", "checked_evidence_requirement", "checked_context_isolation", "checked_permission_scope", "checked_dispatch_gate", "checked_result_quarantine", "checked_false_claims_blocked", "checked_integrated_restore_single_document"))


@dataclass(frozen=True)
class VerifierSubagentBoundarySafetyReport:
    report_id: str
    safe_for_v0406_verifier_boundary: bool
    safe_for_subagent_invocation: bool
    safe_for_child_session_creation: bool
    safe_for_parent_raw_transcript_sharing: bool
    safe_for_subagent_permission_grant: bool
    safe_for_standalone_default_personal_runtime: bool
    production_certified: bool
    requires_v0407_rehearsal_evidence_matrix: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("safe_for_v0406_verifier_boundary", "requires_v0407_rehearsal_evidence_matrix"))
        _validate_false(self, ("safe_for_subagent_invocation", "safe_for_child_session_creation", "safe_for_parent_raw_transcript_sharing", "safe_for_subagent_permission_grant", "safe_for_standalone_default_personal_runtime", "production_certified"))


@dataclass(frozen=True)
class VerifierSubagentBoundaryReadinessReport:
    report_id: str
    verifier_subagent_boundary_deepening_defined: bool
    verifier_role_contract_ready: bool
    verifier_evidence_requirement_ready: bool
    verifier_context_isolation_contract_ready: bool
    subagent_verification_request_draft_ready: bool
    verifier_dispatch_gate_ready: bool
    verifier_result_quarantine_contract_ready: bool
    integrated_restore_document_ready: bool
    v0407_handoff_ready: bool
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
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("verifier_subagent_boundary_deepening_defined", "verifier_role_contract_ready", "verifier_evidence_requirement_ready", "verifier_context_isolation_contract_ready", "subagent_verification_request_draft_ready", "verifier_dispatch_gate_ready", "verifier_result_quarantine_contract_ready", "integrated_restore_document_ready", "v0407_handoff_ready"))
        _validate_false(self, REQUIRED_FALSE_FLAGS)


@dataclass(frozen=True)
class V0406IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("section_id", "title", "content_summary", "restore_value"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.section_id not in REQUIRED_RESTORE_SECTION_IDS:
            raise ValueError("section_id must be a required v0.40.6 integrated restore section")


@dataclass(frozen=True)
class V0406IntegratedRestoreContextSnapshot:
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
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("snapshot_id", "current_version", "current_track", "next_recommended_version", "next_recommended_focus"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("baseline_versions", "implemented_modules", "test_files", "docs", "open_capabilities", "closed_capabilities"):
            _validate_tuple(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if set(BASELINE_VERSIONS).difference(self.baseline_versions):
            raise ValueError("baseline_versions must include v0.40.0 through v0.40.6")
        if not set(OPEN_CAPABILITIES).issubset(set(self.open_capabilities)):
            raise ValueError("open_capabilities must include v0.40.6 openings")
        if not set(CLOSED_CAPABILITIES).issubset(set(self.closed_capabilities)):
            raise ValueError("closed_capabilities must include unsafe closed surfaces")


@dataclass(frozen=True)
class V0406IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0406IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0406IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    required_false_flags: tuple[str, ...]
    restore_prompt_summary: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("restore_packet_id", self.restore_packet_id)
        _require_non_blank("restore_prompt_summary", self.restore_prompt_summary)
        _validate_version(self.version)
        _validate_tuple("restore_sections", self.restore_sections)
        _validate_tuple("required_test_commands", self.required_test_commands)
        _validate_tuple("required_false_flags", self.required_false_flags)
        _validate_dict("metadata", self.metadata)
        if self.single_integrated_doc_path != INTEGRATED_DOC_PATH:
            raise ValueError("single_integrated_doc_path must match the v0.40.6 integrated doc path")
        _validate_false(self, ("separate_restore_doc_created",))
        if set(REQUIRED_RESTORE_SECTION_IDS) != {section.section_id for section in self.restore_sections}:
            raise ValueError("restore_sections must include every required integrated section")
        if set(REQUIRED_FALSE_FLAGS) != set(self.required_false_flags):
            raise ValueError("required_false_flags must match v0.40.6 unsafe false flags")


@dataclass(frozen=True)
class V0406IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("manifest_id", "integrated_doc_path"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.integrated_doc_path != INTEGRATED_DOC_PATH:
            raise ValueError("integrated_doc_path must be the single v0.40.6 document")
        _validate_true(self, ("integrated_doc_required", "copy_paste_restore_prompt_required"))
        _validate_false(self, ("separate_restore_doc_allowed", "separate_restore_doc_created"))
        if self.suitable_for_new_session_handoff and not self.required_sections_present:
            raise ValueError("new-session handoff requires every integrated section")


@dataclass(frozen=True)
class V0407RehearsalEvidenceMatrixHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0406: tuple[str, ...]
    risk_notes: tuple[str, ...]
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("recommended_focus", "required_inputs_from_v0406", "risk_notes"):
            _validate_tuple(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation" not in self.target_version:
            raise ValueError("target_version must target v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation")


@dataclass(frozen=True)
class V041SmokeRunAccelerationVerifierSignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    verifier_subagent_boundary_passed: bool
    blocking_runtime_gaps: tuple[str, ...]
    safety_conditions_for_acceleration: tuple[str, ...]
    recommendation: str
    version: str = V0406_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("signal_id", "conservative_target", "recommendation"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("blocking_runtime_gaps", self.blocking_runtime_gaps)
        _validate_tuple("safety_conditions_for_acceleration", self.safety_conditions_for_acceleration)
        _validate_dict("metadata", self.metadata)
        if self.conservative_target != "v0.41.6":
            raise ValueError("conservative_target must remain v0.41.6")
        if self.metadata.get("ready_for_standalone_default_personal_runtime") is True:
            raise ValueError("acceleration signal must not start standalone runtime")


def create_verifier_evidence_requirement(**overrides: Any) -> VerifierEvidenceRequirement:
    defaults = {
        "requirement_id": "verifier-evidence-requirement-v0406",
        "required_evidence_types": REQUIRED_EVIDENCE_TYPES,
        "provided_evidence_refs": {name: f"{name}-v0406" for name in REQUIRED_EVIDENCE_TYPES},
        "evidence_must_match": True,
        "metadata_only": True,
    }
    return VerifierEvidenceRequirement(**_with_overrides(defaults, overrides))


def evaluate_verifier_evidence_requirement(
    requirement: VerifierEvidenceRequirement | None = None,
    expected_evidence_refs: dict[str, str] | None = None,
    **overrides: Any,
) -> VerifierEvidenceRequirementEvaluation:
    requirement = requirement or create_verifier_evidence_requirement()
    expected_evidence_refs = expected_evidence_refs or {name: f"{name}-v0406" for name in REQUIRED_EVIDENCE_TYPES}
    missing = tuple(name for name in requirement.required_evidence_types if name not in requirement.provided_evidence_refs)
    mismatched = tuple(
        name
        for name, expected in expected_evidence_refs.items()
        if name in requirement.provided_evidence_refs and requirement.provided_evidence_refs[name] != expected
    )
    complete = not missing and not mismatched
    defaults = {
        "evaluation_id": "verifier-evidence-evaluation-v0406",
        "requirement_ref": requirement.requirement_id,
        "missing_evidence_types": missing,
        "mismatched_evidence_types": mismatched,
        "complete": complete,
        "eligible_for_verifier_draft": complete,
        "invocation_authority_granted": False,
        "metadata_only": True,
    }
    return VerifierEvidenceRequirementEvaluation(**_with_overrides(defaults, overrides))


def create_verifier_role_contract(**overrides: Any) -> VerifierRoleContract:
    defaults = {
        "contract_id": "verifier-role-contract-v0406",
        "verifier_role_kind": VerifierRoleKind.EVIDENCE_REVIEWER.value,
        "role_description": "Review supplied evidence refs without execution.",
        "allowed_role": True,
        "creates_subagent": False,
        "invokes_subagent": False,
        "grants_runtime_authority": False,
    }
    return VerifierRoleContract(**_with_overrides(defaults, overrides))


def create_verifier_context_isolation_contract(**overrides: Any) -> VerifierContextIsolationContract:
    defaults = {
        "contract_id": "verifier-context-isolation-v0406",
        "parent_raw_transcript_shared": False,
        "parent_hidden_context_shared": False,
        "parent_credentials_shared": False,
        "parent_runtime_authority_shared": False,
        "summary_packet_required": True,
        "structured_input_required": True,
        "evidence_refs_required": True,
        "child_context_isolated": True,
    }
    return VerifierContextIsolationContract(**_with_overrides(defaults, overrides))


def create_verifier_permission_scope(**overrides: Any) -> VerifierPermissionScope:
    defaults = {
        "scope_id": "verifier-permission-scope-v0406",
        "read_only_metadata_scope": True,
        "workspace_write_allowed": False,
        "live_workspace_apply_allowed": False,
        "shell_allowed": False,
        "network_allowed": False,
        "credential_access_allowed": False,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "subagent_chaining_allowed": False,
        "dominion_authority_allowed": False,
    }
    return VerifierPermissionScope(**_with_overrides(defaults, overrides))


def create_subagent_verification_request_draft(**overrides: Any) -> SubagentVerificationRequestDraft:
    defaults = {
        "request_id": "subagent-verification-request-draft-v0406",
        "verifier_role_ref": "verifier-role-contract-v0406",
        "evidence_requirement_ref": "verifier-evidence-requirement-v0406",
        "context_isolation_ref": "verifier-context-isolation-v0406",
        "permission_scope_ref": "verifier-permission-scope-v0406",
        "request_status": VerifierRequestStatus.EVIDENCE_ELIGIBLE_FOR_DRAFT.value,
        "metadata_only": True,
        "draft_only": True,
        "invocation_requested": True,
        "invocation_allowed": False,
        "subagent_invoked": False,
        "child_session_created": False,
        "parent_raw_transcript_shared": False,
        "runtime_authority_granted": False,
    }
    return SubagentVerificationRequestDraft(**_with_overrides(defaults, overrides))


def create_verifier_subagent_dispatch_gate_policy(**overrides: Any) -> VerifierSubagentDispatchGatePolicy:
    defaults = {
        "policy_id": "verifier-dispatch-gate-policy-v0406",
        "deny_by_default": True,
        "invocation_allowed": False,
        "child_session_creation_allowed": False,
        "parent_context_sharing_allowed": False,
        "permission_grant_allowed": False,
        "metadata_only": True,
    }
    return VerifierSubagentDispatchGatePolicy(**_with_overrides(defaults, overrides))


def create_verifier_subagent_invocation_blocked_decision(**overrides: Any) -> VerifierSubagentInvocationBlockedDecision:
    defaults = {
        "decision_id": "verifier-subagent-invocation-blocked-v0406",
        "request_ref": "subagent-verification-request-draft-v0406",
        "blocked": True,
        "subagent_invoked": False,
        "child_session_created": False,
        "runtime_authority_granted": False,
        "reason": "verifier_subagent_invocation_is_future_gated",
        "safe_alternative": "keep_request_as_draft",
    }
    return VerifierSubagentInvocationBlockedDecision(**_with_overrides(defaults, overrides))


def evaluate_verifier_subagent_dispatch_gate(
    request: SubagentVerificationRequestDraft | None = None,
    policy: VerifierSubagentDispatchGatePolicy | None = None,
    **overrides: Any,
) -> VerifierSubagentDispatchGateEvaluation:
    request = request or create_subagent_verification_request_draft()
    policy = policy or create_verifier_subagent_dispatch_gate_policy()
    decision = create_verifier_subagent_invocation_blocked_decision(request_ref=request.request_id)
    defaults = {
        "evaluation_id": "verifier-dispatch-gate-evaluation-v0406",
        "request_ref": request.request_id,
        "policy_ref": policy.policy_id,
        "blocked": True,
        "subagent_invoked": False,
        "child_session_created": False,
        "parent_raw_transcript_shared": False,
        "executed": False,
        "metadata_only": True,
        "decision_ref": decision.decision_id,
    }
    return VerifierSubagentDispatchGateEvaluation(**_with_overrides(defaults, overrides))


def create_verifier_parent_context_boundary(**overrides: Any) -> VerifierParentContextBoundary:
    defaults = {
        "boundary_id": "verifier-parent-context-boundary-v0406",
        "summary_packet_only": True,
        "parent_raw_transcript_shared": False,
        "parent_hidden_context_shared": False,
        "parent_credentials_shared": False,
        "parent_runtime_authority_shared": False,
    }
    return VerifierParentContextBoundary(**_with_overrides(defaults, overrides))


def create_verifier_return_envelope_contract(**overrides: Any) -> VerifierReturnEnvelopeContract:
    defaults = {
        "contract_id": "verifier-return-envelope-contract-v0406",
        "summary_only_return": True,
        "raw_child_transcript_return_allowed": False,
        "evidence_refs_required": True,
        "structured_result_required": True,
        "human_review_required": True,
        "direct_process_state_update_allowed": False,
        "direct_memory_write_allowed": False,
        "direct_runtime_decision_allowed": False,
    }
    return VerifierReturnEnvelopeContract(**_with_overrides(defaults, overrides))


def create_verifier_result_quarantine_contract(**overrides: Any) -> VerifierResultQuarantineContract:
    defaults = {
        "contract_id": "verifier-result-quarantine-contract-v0406",
        "raw_verifier_result_trusted": False,
        "direct_persistence_allowed": False,
        "direct_process_state_update_allowed": False,
        "direct_memory_write_allowed": False,
        "direct_execution_allowed": False,
        "requires_schema_validation": True,
        "requires_human_review": True,
        "requires_provenance": True,
    }
    return VerifierResultQuarantineContract(**_with_overrides(defaults, overrides))


def create_verifier_result_quarantine_envelope(**overrides: Any) -> VerifierResultQuarantineEnvelope:
    defaults = {
        "envelope_id": "verifier-result-quarantine-envelope-v0406",
        "contract_ref": "verifier-result-quarantine-contract-v0406",
        "quarantined": True,
        "validated": False,
        "human_reviewed": False,
        "eligible_for_persistence": False,
        "eligible_for_process_state": False,
        "eligible_for_memory": False,
        "eligible_for_execution": False,
        "metadata_only": True,
    }
    return VerifierResultQuarantineEnvelope(**_with_overrides(defaults, overrides))


def create_verifier_subagent_authority_boundary(**overrides: Any) -> VerifierSubagentAuthorityBoundary:
    defaults = {
        "boundary_id": "verifier-subagent-authority-boundary-v0406",
        "allows_subagent_invocation": False,
        "allows_child_session_creation": False,
        "allows_parent_raw_transcript_sharing": False,
        "allows_workspace_write": False,
        "allows_live_workspace_apply": False,
        "allows_shell_execution": False,
        "allows_network_access": False,
        "allows_credential_access": False,
        "allows_provider_invocation": False,
        "allows_prompt_submission": False,
        "allows_subagent_chaining": False,
        "allows_runtime_execution": False,
        "allows_standalone_default_personal_runtime": False,
        "allows_production_certification": False,
    }
    return VerifierSubagentAuthorityBoundary(**_with_overrides(defaults, overrides))


def audit_verifier_subagent_false_claim(
    claim_kind: str = VerifierSubagentFalseClaimKind.VERIFIER_SUBAGENT_INVOCATION_READY.value,
    **overrides: Any,
) -> VerifierSubagentFalseClaimAudit:
    request = VerifierSubagentFalseClaimRequest(
        claim_id=f"claim-{claim_kind}",
        claim_kind=claim_kind,
        claim_text=f"{claim_kind} is ready.",
        source="test_fixture",
        evidence_refs=("v0406",),
    )
    defaults = {
        "audit_id": f"audit-{claim_kind}",
        "claim_id": request.claim_id,
        "claim_kind": request.claim_kind,
        "claim_detected": True,
        "claim_allowed": False,
        "readiness_flag_modified": False,
        "corrective_statement": f"{claim_kind} remains blocked in v0.40.6.",
        "must_block_release_claim": True,
    }
    return VerifierSubagentFalseClaimAudit(**_with_overrides(defaults, overrides))


def create_verifier_subagent_boundary_audit_record(**overrides: Any) -> VerifierSubagentBoundaryAuditRecord:
    defaults = {
        "audit_id": "verifier-subagent-boundary-audit-v0406",
        "checked_role_contract": True,
        "checked_evidence_requirement": True,
        "checked_context_isolation": True,
        "checked_permission_scope": True,
        "checked_dispatch_gate": True,
        "checked_result_quarantine": True,
        "checked_false_claims_blocked": True,
        "checked_integrated_restore_single_document": True,
        "notes": ("verifier subagent surfaces remain draft-only and non-invoking",),
    }
    return VerifierSubagentBoundaryAuditRecord(**_with_overrides(defaults, overrides))


def create_verifier_subagent_boundary_safety_report(**overrides: Any) -> VerifierSubagentBoundarySafetyReport:
    defaults = {
        "report_id": "verifier-subagent-boundary-safety-v0406",
        "safe_for_v0406_verifier_boundary": True,
        "safe_for_subagent_invocation": False,
        "safe_for_child_session_creation": False,
        "safe_for_parent_raw_transcript_sharing": False,
        "safe_for_subagent_permission_grant": False,
        "safe_for_standalone_default_personal_runtime": False,
        "production_certified": False,
        "requires_v0407_rehearsal_evidence_matrix": True,
    }
    return VerifierSubagentBoundarySafetyReport(**_with_overrides(defaults, overrides))


def create_verifier_subagent_boundary_readiness_report(**overrides: Any) -> VerifierSubagentBoundaryReadinessReport:
    defaults = {
        "report_id": "verifier-subagent-boundary-readiness-v0406",
        "verifier_subagent_boundary_deepening_defined": True,
        "verifier_role_contract_ready": True,
        "verifier_evidence_requirement_ready": True,
        "verifier_context_isolation_contract_ready": True,
        "subagent_verification_request_draft_ready": True,
        "verifier_dispatch_gate_ready": True,
        "verifier_result_quarantine_contract_ready": True,
        "integrated_restore_document_ready": True,
        "v0407_handoff_ready": True,
        **{name: False for name in REQUIRED_FALSE_FLAGS},
    }
    return VerifierSubagentBoundaryReadinessReport(**_with_overrides(defaults, overrides))


def create_v0406_integrated_restore_sections() -> tuple[V0406IntegratedRestoreSection, ...]:
    return tuple(
        V0406IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for the v0.40.6 integrated restore document.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0406_integrated_restore_context_snapshot(**overrides: Any) -> V0406IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0406",
        "current_version": V0406_RELEASE_NAME,
        "current_track": V0406_TRACK_NAME,
        "baseline_versions": BASELINE_VERSIONS,
        "implemented_modules": (
            "repair_mission_loop_boundary",
            "repair_mission_loop_rehearsal",
            "repair_mission_loop_two_iteration",
            "repair_mission_loop_negative_gates",
            "repair_mission_loop_checkpoint_hardening",
            "repair_mission_loop_provider_prompt_boundary",
            "repair_mission_loop_verifier_subagent_boundary",
        ),
        "test_files": (
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
        "next_recommended_version": "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation",
        "next_recommended_focus": "Rehearsal evidence and boundary coverage without runtime expansion",
    }
    return V0406IntegratedRestoreContextSnapshot(**_with_overrides(defaults, overrides))


def create_v0406_integrated_restore_packet(**overrides: Any) -> V0406IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0406",
        "snapshot": create_v0406_integrated_restore_context_snapshot(),
        "restore_sections": create_v0406_integrated_restore_sections(),
        "required_test_commands": (
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
        "restore_prompt_summary": "Continue ChantaCore after v0.40.6 without opening verifier subagent runtime authority.",
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0406IntegratedRestorePacket(**_with_overrides(defaults, overrides))


def create_v0406_integrated_restore_document_manifest(**overrides: Any) -> V0406IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0406",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0406IntegratedRestoreDocumentManifest(**_with_overrides(defaults, overrides))


def create_v0407_rehearsal_evidence_matrix_handoff(**overrides: Any) -> V0407RehearsalEvidenceMatrixHandoff:
    defaults = {
        "handoff_id": "v0407-rehearsal-evidence-matrix-handoff",
        "target_version": "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation",
        "target_track": "Standalone-Agent Preparation Track: Rehearsal Evidence Matrix & Boundary Coverage",
        "recommended_focus": (
            "V040RehearsalEvidenceMatrix",
            "BoundaryCoverageRecord",
            "DeniedActionCoverageRecord",
            "CheckpointCoverageRecord",
            "ProviderPromptBoundaryCoverageRecord",
            "VerifierSubagentBoundaryCoverageRecord",
            "RestoreCoverageRecord",
            "no runtime expansion",
            "preparation for v0.40.8 CLI preview surface",
        ),
        "required_inputs_from_v0406": (
            "verifier_evidence_requirement",
            "verifier_context_isolation_contract",
            "verifier_dispatch_gate",
            "verifier_result_quarantine_contract",
            "integrated_restore_packet",
        ),
        "risk_notes": (
            "coverage consolidation must not become execution authority",
            "CLI preview preparation must not invoke subagents",
        ),
    }
    return V0407RehearsalEvidenceMatrixHandoff(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_verifier_signal(
    verifier_subagent_boundary_passed: bool = True,
    blocking_runtime_gaps: tuple[str, ...] = ("ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"),
    **overrides: Any,
) -> V041SmokeRunAccelerationVerifierSignal:
    if not verifier_subagent_boundary_passed:
        earliest = None
        recommendation = "do_not_accelerate"
    elif set(blocking_runtime_gaps) == {"ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"}:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    elif set(blocking_runtime_gaps).issubset({"CLI", "ProfileRuntime"}):
        earliest = "v0.41.5"
        recommendation = "possible_mild_acceleration"
    else:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    defaults = {
        "signal_id": "v041-smoke-run-verifier-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "verifier_subagent_boundary_passed": verifier_subagent_boundary_passed,
        "blocking_runtime_gaps": blocking_runtime_gaps,
        "safety_conditions_for_acceleration": (
            "verifier_request_draft_remains_non_invoking",
            "context_isolation_blocks_parent_raw_transcript",
            "dispatch_gate_blocks_child_session",
            "standalone_runtime_components_remain_future_gated",
        ),
        "recommendation": recommendation,
        "metadata": {"ready_for_standalone_default_personal_runtime": False},
    }
    return V041SmokeRunAccelerationVerifierSignal(**_with_overrides(defaults, overrides))


def verifier_request_draft_is_metadata_only(draft: SubagentVerificationRequestDraft) -> bool:
    return (
        draft.metadata_only
        and draft.draft_only
        and not draft.invocation_allowed
        and not draft.subagent_invoked
        and not draft.child_session_created
        and not draft.parent_raw_transcript_shared
        and not draft.runtime_authority_granted
    )


def verifier_dispatch_evaluation_is_blocked(evaluation: VerifierSubagentDispatchGateEvaluation) -> bool:
    return (
        evaluation.blocked
        and not evaluation.subagent_invoked
        and not evaluation.child_session_created
        and not evaluation.parent_raw_transcript_shared
        and not evaluation.executed
        and evaluation.metadata_only
    )


def verifier_readiness_preserves_no_unsafe_runtime(report: VerifierSubagentBoundaryReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0406IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def v041_verifier_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationVerifierSignal) -> bool:
    return signal.metadata.get("ready_for_standalone_default_personal_runtime") is False

