"""v0.40.5 provider / prompt boundary deepening metadata.

This layer separates prompt dispatch candidates from prompt submission and
provider invocation. It also defines provider output quarantine and one
integrated release/restore/handoff packet. It does not submit prompts, invoke
providers, create clients, use network, open standalone runtime, or certify
production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank
from .repair_mission_loop_boundary import (
    DeniedRuntimeActionMetadata,
    LoopDecisionRecord,
    PromptSubmissionBoundary,
    ProviderBoundaryGate,
    V040ReadinessReport,
)
from .repair_mission_loop_checkpoint_hardening import (
    V0404RestoreContextSnapshot,
    V0404RestorePacket,
)
from .repair_mission_loop_negative_gates import (
    NegativeRuntimeGateDecision,
    NegativeRuntimeGateReadinessReport,
    NegativeRuntimeRequest,
    RuntimeFalseClaimDetection,
)


V0405_VERSION = "v0.40.5"
V0405_RELEASE_NAME = "v0.40.5 Provider / Prompt Boundary Deepening & Integrated Restore Handoff"
V0405_TRACK_NAME = (
    "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + "
    "Sandbox Rehearsal + Manual Checkpoint Gate + Negative Runtime Gate "
    "Regression + Scope-Bound Human Approval + Provider / Prompt Boundary Deepening"
)


class PromptBoundaryKind(StrEnum):
    PROMPT_DRAFT = "prompt_draft"
    PROMPT_DISPATCH_CANDIDATE = "prompt_dispatch_candidate"
    PROMPT_SUBMISSION_GATE = "prompt_submission_gate"
    PROMPT_SUBMISSION_BLOCKED_DECISION = "prompt_submission_blocked_decision"


class ProviderBoundaryKind(StrEnum):
    PROVIDER_REFERENCE = "provider_reference"
    MODEL_REFERENCE = "model_reference"
    PROVIDER_INVOCATION_GATE = "provider_invocation_gate"
    PROVIDER_INVOCATION_BLOCKED_DECISION = "provider_invocation_blocked_decision"
    PROVIDER_OUTPUT_QUARANTINE_CONTRACT = "provider_output_quarantine_contract"
    PROVIDER_OUTPUT_QUARANTINE_ENVELOPE = "provider_output_quarantine_envelope"


class PromptDispatchStatus(StrEnum):
    DRAFT = "draft"
    CANDIDATE_CREATED = "candidate_created"
    SUBMISSION_BLOCKED = "submission_blocked"
    NO_OP = "no_op"


class ProviderInvocationStatus(StrEnum):
    REFERENCE_ONLY = "reference_only"
    INVOCATION_BLOCKED = "invocation_blocked"
    QUARANTINE_REQUIRED = "quarantine_required"
    NO_OP = "no_op"


class ProviderPromptFalseClaimKind(StrEnum):
    PROMPT_SUBMISSION_READY = "prompt_submission_ready"
    MODEL_PROVIDER_INVOCATION_READY = "model_provider_invocation_ready"
    PROVIDER_OUTPUT_TRUSTED = "provider_output_trusted"
    PROVIDER_OUTPUT_DIRECT_PERSISTENCE_READY = "provider_output_direct_persistence_ready"
    PROVIDER_OUTPUT_DIRECT_EXECUTION_READY = "provider_output_direct_execution_ready"
    CREDENTIAL_ACCESS_READY = "credential_access_ready"
    NETWORK_ACCESS_READY = "network_access_ready"
    STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY = "standalone_default_personal_runtime_ready"
    PRODUCTION_CERTIFIED = "production_certified"


ALLOWED_DECISION_KINDS: tuple[str, ...] = (
    "block",
    "stop",
    "do_nothing",
    "request_human_checkpoint",
    "defer_to_future_gate",
)

REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_live_workspace_apply",
    "ready_for_prompt_submission_to_model",
    "ready_for_model_provider_invocation",
    "ready_for_subagent_invocation",
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
    "provider_prompt_boundary_summary",
    "quarantine_contract_summary",
    "how_to_verify_this_state",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0406_handoff",
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
    "integrated_restore_document",
)

CLOSED_CAPABILITIES: tuple[str, ...] = (
    "standalone_default_personal_runtime",
    "actual_prompt_submission",
    "actual_model_provider_invocation",
    "actual_subagent_invocation",
    "live_workspace_apply",
    "autonomous_loop_runtime",
    "automatic_repair_loop",
    "retry_loop",
    "network_access",
    "credential_access",
    "dominion_runtime",
    "production_certification",
)

INTEGRATED_DOC_PATH = "docs/versions/v0.40/v0.40.5_provider_prompt_boundary_deepening_restore.md"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0405_VERSION not in version:
        raise ValueError("version must include v0.40.5")


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
class PromptDispatchCandidate:
    candidate_id: str
    prompt_draft_ref: str
    provider_ref: str | None
    model_ref: str | None
    dispatch_status: str
    metadata_only: bool
    submitted_to_model: bool
    provider_invoked: bool
    network_used: bool
    credential_accessed: bool
    runtime_authority_granted: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("prompt_draft_ref", self.prompt_draft_ref)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.dispatch_status not in {item.value for item in PromptDispatchStatus}:
            raise ValueError("dispatch_status must be a v0.40.5 prompt dispatch status")
        _validate_true(self, ("metadata_only",))
        _validate_false(
            self,
            (
                "submitted_to_model",
                "provider_invoked",
                "network_used",
                "credential_accessed",
                "runtime_authority_granted",
            ),
        )


@dataclass(frozen=True)
class PromptSubmissionGatePolicy:
    policy_id: str
    deny_by_default: bool
    submission_allowed: bool
    human_checkpoint_required: bool
    metadata_only: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("deny_by_default", "human_checkpoint_required", "metadata_only"))
        _validate_false(self, ("submission_allowed",))


@dataclass(frozen=True)
class PromptSubmissionGateEvaluation:
    evaluation_id: str
    candidate_ref: str
    policy_ref: str
    blocked: bool
    submitted_to_model: bool
    executed: bool
    metadata_only: bool
    decision_ref: str | None
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evaluation_id", "candidate_ref", "policy_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("blocked", "metadata_only"))
        _validate_false(self, ("submitted_to_model", "executed"))


@dataclass(frozen=True)
class ProviderInvocationGatePolicy:
    policy_id: str
    deny_by_default: bool
    invocation_allowed: bool
    network_allowed: bool
    credential_access_allowed: bool
    client_creation_allowed: bool
    metadata_only: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("deny_by_default", "metadata_only"))
        _validate_false(
            self,
            (
                "invocation_allowed",
                "network_allowed",
                "credential_access_allowed",
                "client_creation_allowed",
            ),
        )


@dataclass(frozen=True)
class ProviderInvocationGateEvaluation:
    evaluation_id: str
    candidate_ref: str
    policy_ref: str
    blocked: bool
    provider_invoked: bool
    network_used: bool
    credential_accessed: bool
    client_created: bool
    executed: bool
    metadata_only: bool
    decision_ref: str | None
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evaluation_id", "candidate_ref", "policy_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("blocked", "metadata_only"))
        _validate_false(
            self,
            ("provider_invoked", "network_used", "credential_accessed", "client_created", "executed"),
        )


@dataclass(frozen=True)
class PromptProviderBoundaryDecision:
    decision_id: str
    candidate_ref: str
    decision_kind: str
    reason: str
    safe_alternative: str
    prompt_submission_allowed: bool
    provider_invocation_allowed: bool
    runtime_authority_granted: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "candidate_ref", "decision_kind", "reason", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.decision_kind not in ALLOWED_DECISION_KINDS:
            raise ValueError("decision_kind must be a v0.40.5 allowed decision")
        _validate_false(
            self,
            ("prompt_submission_allowed", "provider_invocation_allowed", "runtime_authority_granted"),
        )


@dataclass(frozen=True)
class PromptDispatchBlockedDecision:
    decision_id: str
    candidate_ref: str
    blocked: bool
    prompt_submission_allowed: bool
    submitted_to_model: bool
    reason: str
    safe_alternative: str
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "candidate_ref", "reason", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("blocked",))
        _validate_false(self, ("prompt_submission_allowed", "submitted_to_model"))


@dataclass(frozen=True)
class ProviderInvocationBlockedDecision:
    decision_id: str
    candidate_ref: str
    blocked: bool
    provider_invocation_allowed: bool
    provider_invoked: bool
    network_allowed: bool
    credential_access_allowed: bool
    client_creation_allowed: bool
    reason: str
    safe_alternative: str
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "candidate_ref", "reason", "safe_alternative"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("blocked",))
        _validate_false(
            self,
            (
                "provider_invocation_allowed",
                "provider_invoked",
                "network_allowed",
                "credential_access_allowed",
                "client_creation_allowed",
            ),
        )


@dataclass(frozen=True)
class ProviderOutputQuarantineContract:
    contract_id: str
    provider_ref: str | None
    model_ref: str | None
    raw_provider_output_trusted: bool
    direct_persistence_allowed: bool
    direct_execution_allowed: bool
    requires_redaction: bool
    requires_schema_validation: bool
    requires_human_review: bool
    requires_provenance: bool
    eligible_for_process_state_only_after_validation: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("raw_provider_output_trusted", "direct_persistence_allowed", "direct_execution_allowed"))
        _validate_true(
            self,
            (
                "requires_redaction",
                "requires_schema_validation",
                "requires_human_review",
                "requires_provenance",
                "eligible_for_process_state_only_after_validation",
            ),
        )


@dataclass(frozen=True)
class ProviderOutputQuarantineEnvelope:
    envelope_id: str
    contract_ref: str
    output_ref: str | None
    quarantined: bool
    validated: bool
    redacted: bool
    human_reviewed: bool
    eligible_for_persistence: bool
    eligible_for_execution: bool
    metadata_only: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("envelope_id", self.envelope_id)
        _require_non_blank("contract_ref", self.contract_ref)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("quarantined", "metadata_only"))
        _validate_false(
            self,
            ("validated", "redacted", "human_reviewed", "eligible_for_persistence", "eligible_for_execution"),
        )


@dataclass(frozen=True)
class ProviderPromptAuthorityBoundary:
    boundary_id: str
    allows_prompt_submission: bool
    allows_provider_invocation: bool
    allows_network_access: bool
    allows_credential_access: bool
    allows_client_creation: bool
    allows_direct_provider_output_persistence: bool
    allows_direct_provider_output_execution: bool
    allows_runtime_execution: bool
    allows_standalone_default_personal_runtime: bool
    allows_production_certification: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(
            self,
            (
                "allows_prompt_submission",
                "allows_provider_invocation",
                "allows_network_access",
                "allows_credential_access",
                "allows_client_creation",
                "allows_direct_provider_output_persistence",
                "allows_direct_provider_output_execution",
                "allows_runtime_execution",
                "allows_standalone_default_personal_runtime",
                "allows_production_certification",
            ),
        )


@dataclass(frozen=True)
class ProviderPromptFalseClaimRequest:
    claim_id: str
    claim_kind: str
    claim_text: str
    source: str
    evidence_refs: tuple[str, ...]
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("claim_id", "claim_kind", "claim_text", "source"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.claim_kind not in {item.value for item in ProviderPromptFalseClaimKind}:
            raise ValueError("claim_kind must be a v0.40.5 false claim kind")


@dataclass(frozen=True)
class ProviderPromptFalseClaimAudit:
    audit_id: str
    claim_id: str
    claim_kind: str
    claim_detected: bool
    claim_allowed: bool
    readiness_flag_modified: bool
    corrective_statement: str
    must_block_release_claim: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("audit_id", "claim_id", "claim_kind", "corrective_statement"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("claim_detected", "must_block_release_claim"))
        _validate_false(self, ("claim_allowed", "readiness_flag_modified"))


@dataclass(frozen=True)
class ProviderPromptBoundaryAuditRecord:
    audit_id: str
    checked_prompt_dispatch_candidate_metadata_only: bool
    checked_prompt_submission_blocked: bool
    checked_provider_invocation_blocked: bool
    checked_network_blocked: bool
    checked_credential_access_blocked: bool
    checked_client_creation_blocked: bool
    checked_quarantine_required: bool
    checked_false_claims_blocked: bool
    checked_integrated_restore_single_document: bool
    notes: tuple[str, ...]
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _validate_version(self.version)
        _validate_tuple("notes", self.notes)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "checked_prompt_dispatch_candidate_metadata_only",
                "checked_prompt_submission_blocked",
                "checked_provider_invocation_blocked",
                "checked_network_blocked",
                "checked_credential_access_blocked",
                "checked_client_creation_blocked",
                "checked_quarantine_required",
                "checked_false_claims_blocked",
                "checked_integrated_restore_single_document",
            ),
        )


@dataclass(frozen=True)
class ProviderPromptBoundarySafetyReport:
    report_id: str
    safe_for_v0405_provider_prompt_boundary: bool
    safe_for_prompt_submission: bool
    safe_for_provider_invocation: bool
    safe_for_network_access: bool
    safe_for_credential_access: bool
    safe_for_client_creation: bool
    safe_for_direct_output_persistence: bool
    safe_for_direct_output_execution: bool
    safe_for_standalone_default_personal_runtime: bool
    production_certified: bool
    requires_v0406_verifier_subagent_boundary: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("safe_for_v0405_provider_prompt_boundary", "requires_v0406_verifier_subagent_boundary"))
        _validate_false(
            self,
            (
                "safe_for_prompt_submission",
                "safe_for_provider_invocation",
                "safe_for_network_access",
                "safe_for_credential_access",
                "safe_for_client_creation",
                "safe_for_direct_output_persistence",
                "safe_for_direct_output_execution",
                "safe_for_standalone_default_personal_runtime",
                "production_certified",
            ),
        )


@dataclass(frozen=True)
class ProviderPromptBoundaryReadinessReport:
    report_id: str
    provider_prompt_boundary_deepening_defined: bool
    prompt_dispatch_candidate_ready: bool
    prompt_submission_gate_ready: bool
    provider_invocation_gate_ready: bool
    provider_output_quarantine_contract_ready: bool
    integrated_restore_document_ready: bool
    v0406_handoff_ready: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_live_workspace_apply: bool
    ready_for_prompt_submission_to_model: bool
    ready_for_model_provider_invocation: bool
    ready_for_subagent_invocation: bool
    ready_for_external_agent_execution: bool
    ready_for_autonomous_loop_runtime: bool
    ready_for_automatic_repair: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_loop: bool
    ready_for_standalone_default_personal_runtime: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "provider_prompt_boundary_deepening_defined",
                "prompt_dispatch_candidate_ready",
                "prompt_submission_gate_ready",
                "provider_invocation_gate_ready",
                "provider_output_quarantine_contract_ready",
                "integrated_restore_document_ready",
                "v0406_handoff_ready",
            ),
        )
        _validate_false(self, REQUIRED_FALSE_FLAGS)


@dataclass(frozen=True)
class V0405IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("section_id", "title", "content_summary", "restore_value"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.section_id not in REQUIRED_RESTORE_SECTION_IDS:
            raise ValueError("section_id must be a required v0.40.5 integrated restore section")


@dataclass(frozen=True)
class V0405IntegratedRestoreContextSnapshot:
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
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("snapshot_id", "current_version", "current_track", "next_recommended_version", "next_recommended_focus"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("baseline_versions", "implemented_modules", "test_files", "docs", "open_capabilities", "closed_capabilities"):
            _validate_tuple(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if set(BASELINE_VERSIONS).difference(self.baseline_versions):
            raise ValueError("baseline_versions must include v0.40.0 through v0.40.5")
        if not set(OPEN_CAPABILITIES).issubset(set(self.open_capabilities)):
            raise ValueError("open_capabilities must include v0.40.5 provider/prompt openings")
        if not set(CLOSED_CAPABILITIES).issubset(set(self.closed_capabilities)):
            raise ValueError("closed_capabilities must include unsafe closed surfaces")


@dataclass(frozen=True)
class V0405IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0405IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0405IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    required_false_flags: tuple[str, ...]
    restore_prompt_summary: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool
    version: str = V0405_VERSION
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
            raise ValueError("single_integrated_doc_path must match the v0.40.5 integrated doc path")
        _validate_false(self, ("separate_restore_doc_created",))
        if set(REQUIRED_RESTORE_SECTION_IDS) != {section.section_id for section in self.restore_sections}:
            raise ValueError("restore_sections must include every required integrated section")
        if set(REQUIRED_FALSE_FLAGS) != set(self.required_false_flags):
            raise ValueError("required_false_flags must match v0.40.5 unsafe false flags")


@dataclass(frozen=True)
class V0405IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("manifest_id", "integrated_doc_path"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.integrated_doc_path != INTEGRATED_DOC_PATH:
            raise ValueError("integrated_doc_path must be the single v0.40.5 document")
        _validate_true(self, ("integrated_doc_required", "copy_paste_restore_prompt_required"))
        _validate_false(self, ("separate_restore_doc_allowed", "separate_restore_doc_created"))
        if self.suitable_for_new_session_handoff and not self.required_sections_present:
            raise ValueError("new-session handoff requires every integrated section")


@dataclass(frozen=True)
class V0406VerifierSubagentBoundaryHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0405: tuple[str, ...]
    risk_notes: tuple[str, ...]
    version: str = V0405_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("recommended_focus", "required_inputs_from_v0405", "risk_notes"):
            _validate_tuple(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if "v0.40.6 Verifier Subagent Boundary Deepening" not in self.target_version:
            raise ValueError("target_version must target v0.40.6 Verifier Subagent Boundary Deepening")


@dataclass(frozen=True)
class V041SmokeRunAccelerationProviderPromptSignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    provider_prompt_boundary_passed: bool
    blocking_runtime_gaps: tuple[str, ...]
    safety_conditions_for_acceleration: tuple[str, ...]
    recommendation: str
    version: str = V0405_VERSION
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


def create_prompt_dispatch_candidate(**overrides: Any) -> PromptDispatchCandidate:
    defaults = {
        "candidate_id": "prompt-dispatch-candidate-v0405",
        "prompt_draft_ref": "prompt-draft-v0405",
        "provider_ref": "provider-ref-metadata-only",
        "model_ref": "model-ref-metadata-only",
        "dispatch_status": PromptDispatchStatus.CANDIDATE_CREATED.value,
        "metadata_only": True,
        "submitted_to_model": False,
        "provider_invoked": False,
        "network_used": False,
        "credential_accessed": False,
        "runtime_authority_granted": False,
    }
    return PromptDispatchCandidate(**_with_overrides(defaults, overrides))


def create_prompt_submission_gate_policy(**overrides: Any) -> PromptSubmissionGatePolicy:
    defaults = {
        "policy_id": "prompt-submission-policy-v0405",
        "deny_by_default": True,
        "submission_allowed": False,
        "human_checkpoint_required": True,
        "metadata_only": True,
    }
    return PromptSubmissionGatePolicy(**_with_overrides(defaults, overrides))


def create_prompt_dispatch_blocked_decision(**overrides: Any) -> PromptDispatchBlockedDecision:
    defaults = {
        "decision_id": "prompt-dispatch-blocked-v0405",
        "candidate_ref": "prompt-dispatch-candidate-v0405",
        "blocked": True,
        "prompt_submission_allowed": False,
        "submitted_to_model": False,
        "reason": "prompt_submission_is_future_gated",
        "safe_alternative": "create_draft",
    }
    return PromptDispatchBlockedDecision(**_with_overrides(defaults, overrides))


def evaluate_prompt_submission_gate(
    candidate: PromptDispatchCandidate | None = None,
    policy: PromptSubmissionGatePolicy | None = None,
    **overrides: Any,
) -> PromptSubmissionGateEvaluation:
    candidate = candidate or create_prompt_dispatch_candidate()
    policy = policy or create_prompt_submission_gate_policy()
    decision = create_prompt_dispatch_blocked_decision(candidate_ref=candidate.candidate_id)
    defaults = {
        "evaluation_id": "prompt-submission-evaluation-v0405",
        "candidate_ref": candidate.candidate_id,
        "policy_ref": policy.policy_id,
        "blocked": True,
        "submitted_to_model": False,
        "executed": False,
        "metadata_only": True,
        "decision_ref": decision.decision_id,
    }
    return PromptSubmissionGateEvaluation(**_with_overrides(defaults, overrides))


def create_provider_invocation_gate_policy(**overrides: Any) -> ProviderInvocationGatePolicy:
    defaults = {
        "policy_id": "provider-invocation-policy-v0405",
        "deny_by_default": True,
        "invocation_allowed": False,
        "network_allowed": False,
        "credential_access_allowed": False,
        "client_creation_allowed": False,
        "metadata_only": True,
    }
    return ProviderInvocationGatePolicy(**_with_overrides(defaults, overrides))


def create_provider_invocation_blocked_decision(**overrides: Any) -> ProviderInvocationBlockedDecision:
    defaults = {
        "decision_id": "provider-invocation-blocked-v0405",
        "candidate_ref": "prompt-dispatch-candidate-v0405",
        "blocked": True,
        "provider_invocation_allowed": False,
        "provider_invoked": False,
        "network_allowed": False,
        "credential_access_allowed": False,
        "client_creation_allowed": False,
        "reason": "provider_invocation_is_future_gated",
        "safe_alternative": "defer_to_future_gate",
    }
    return ProviderInvocationBlockedDecision(**_with_overrides(defaults, overrides))


def evaluate_provider_invocation_gate(
    candidate: PromptDispatchCandidate | None = None,
    policy: ProviderInvocationGatePolicy | None = None,
    **overrides: Any,
) -> ProviderInvocationGateEvaluation:
    candidate = candidate or create_prompt_dispatch_candidate()
    policy = policy or create_provider_invocation_gate_policy()
    decision = create_provider_invocation_blocked_decision(candidate_ref=candidate.candidate_id)
    defaults = {
        "evaluation_id": "provider-invocation-evaluation-v0405",
        "candidate_ref": candidate.candidate_id,
        "policy_ref": policy.policy_id,
        "blocked": True,
        "provider_invoked": False,
        "network_used": False,
        "credential_accessed": False,
        "client_created": False,
        "executed": False,
        "metadata_only": True,
        "decision_ref": decision.decision_id,
    }
    return ProviderInvocationGateEvaluation(**_with_overrides(defaults, overrides))


def create_provider_output_quarantine_contract(**overrides: Any) -> ProviderOutputQuarantineContract:
    defaults = {
        "contract_id": "provider-output-quarantine-contract-v0405",
        "provider_ref": "provider-ref-metadata-only",
        "model_ref": "model-ref-metadata-only",
        "raw_provider_output_trusted": False,
        "direct_persistence_allowed": False,
        "direct_execution_allowed": False,
        "requires_redaction": True,
        "requires_schema_validation": True,
        "requires_human_review": True,
        "requires_provenance": True,
        "eligible_for_process_state_only_after_validation": True,
    }
    return ProviderOutputQuarantineContract(**_with_overrides(defaults, overrides))


def create_provider_output_quarantine_envelope(**overrides: Any) -> ProviderOutputQuarantineEnvelope:
    defaults = {
        "envelope_id": "provider-output-quarantine-envelope-v0405",
        "contract_ref": "provider-output-quarantine-contract-v0405",
        "output_ref": None,
        "quarantined": True,
        "validated": False,
        "redacted": False,
        "human_reviewed": False,
        "eligible_for_persistence": False,
        "eligible_for_execution": False,
        "metadata_only": True,
    }
    return ProviderOutputQuarantineEnvelope(**_with_overrides(defaults, overrides))


def create_provider_prompt_authority_boundary(**overrides: Any) -> ProviderPromptAuthorityBoundary:
    defaults = {
        "boundary_id": "provider-prompt-authority-boundary-v0405",
        "allows_prompt_submission": False,
        "allows_provider_invocation": False,
        "allows_network_access": False,
        "allows_credential_access": False,
        "allows_client_creation": False,
        "allows_direct_provider_output_persistence": False,
        "allows_direct_provider_output_execution": False,
        "allows_runtime_execution": False,
        "allows_standalone_default_personal_runtime": False,
        "allows_production_certification": False,
    }
    return ProviderPromptAuthorityBoundary(**_with_overrides(defaults, overrides))


def create_prompt_provider_boundary_decision(**overrides: Any) -> PromptProviderBoundaryDecision:
    defaults = {
        "decision_id": "provider-prompt-boundary-decision-v0405",
        "candidate_ref": "prompt-dispatch-candidate-v0405",
        "decision_kind": "block",
        "reason": "prompt_submission_and_provider_invocation_are_future_gated",
        "safe_alternative": "create_draft",
        "prompt_submission_allowed": False,
        "provider_invocation_allowed": False,
        "runtime_authority_granted": False,
    }
    return PromptProviderBoundaryDecision(**_with_overrides(defaults, overrides))


def audit_provider_prompt_false_claim(
    claim_kind: str = ProviderPromptFalseClaimKind.PROMPT_SUBMISSION_READY.value,
    **overrides: Any,
) -> ProviderPromptFalseClaimAudit:
    request = ProviderPromptFalseClaimRequest(
        claim_id=f"claim-{claim_kind}",
        claim_kind=claim_kind,
        claim_text=f"{claim_kind} is ready.",
        source="test_fixture",
        evidence_refs=("v0405",),
    )
    defaults = {
        "audit_id": f"audit-{claim_kind}",
        "claim_id": request.claim_id,
        "claim_kind": request.claim_kind,
        "claim_detected": True,
        "claim_allowed": False,
        "readiness_flag_modified": False,
        "corrective_statement": f"{claim_kind} remains blocked in v0.40.5.",
        "must_block_release_claim": True,
    }
    return ProviderPromptFalseClaimAudit(**_with_overrides(defaults, overrides))


def create_provider_prompt_boundary_audit_record(**overrides: Any) -> ProviderPromptBoundaryAuditRecord:
    defaults = {
        "audit_id": "provider-prompt-boundary-audit-v0405",
        "checked_prompt_dispatch_candidate_metadata_only": True,
        "checked_prompt_submission_blocked": True,
        "checked_provider_invocation_blocked": True,
        "checked_network_blocked": True,
        "checked_credential_access_blocked": True,
        "checked_client_creation_blocked": True,
        "checked_quarantine_required": True,
        "checked_false_claims_blocked": True,
        "checked_integrated_restore_single_document": True,
        "notes": ("provider and prompt surfaces remain metadata-gated",),
    }
    return ProviderPromptBoundaryAuditRecord(**_with_overrides(defaults, overrides))


def create_provider_prompt_boundary_safety_report(**overrides: Any) -> ProviderPromptBoundarySafetyReport:
    defaults = {
        "report_id": "provider-prompt-boundary-safety-v0405",
        "safe_for_v0405_provider_prompt_boundary": True,
        "safe_for_prompt_submission": False,
        "safe_for_provider_invocation": False,
        "safe_for_network_access": False,
        "safe_for_credential_access": False,
        "safe_for_client_creation": False,
        "safe_for_direct_output_persistence": False,
        "safe_for_direct_output_execution": False,
        "safe_for_standalone_default_personal_runtime": False,
        "production_certified": False,
        "requires_v0406_verifier_subagent_boundary": True,
    }
    return ProviderPromptBoundarySafetyReport(**_with_overrides(defaults, overrides))


def create_provider_prompt_boundary_readiness_report(**overrides: Any) -> ProviderPromptBoundaryReadinessReport:
    defaults = {
        "report_id": "provider-prompt-boundary-readiness-v0405",
        "provider_prompt_boundary_deepening_defined": True,
        "prompt_dispatch_candidate_ready": True,
        "prompt_submission_gate_ready": True,
        "provider_invocation_gate_ready": True,
        "provider_output_quarantine_contract_ready": True,
        "integrated_restore_document_ready": True,
        "v0406_handoff_ready": True,
        **{name: False for name in REQUIRED_FALSE_FLAGS},
    }
    return ProviderPromptBoundaryReadinessReport(**_with_overrides(defaults, overrides))


def create_v0405_integrated_restore_sections() -> tuple[V0405IntegratedRestoreSection, ...]:
    return tuple(
        V0405IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for the v0.40.5 integrated restore document.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0405_integrated_restore_context_snapshot(**overrides: Any) -> V0405IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0405",
        "current_version": V0405_RELEASE_NAME,
        "current_track": V0405_TRACK_NAME,
        "baseline_versions": BASELINE_VERSIONS,
        "implemented_modules": (
            "repair_mission_loop_boundary",
            "repair_mission_loop_rehearsal",
            "repair_mission_loop_two_iteration",
            "repair_mission_loop_negative_gates",
            "repair_mission_loop_checkpoint_hardening",
            "repair_mission_loop_provider_prompt_boundary",
        ),
        "test_files": (
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
        "next_recommended_version": "v0.40.6 Verifier Subagent Boundary Deepening",
        "next_recommended_focus": "Verifier subagent boundary hardening without invocation",
    }
    return V0405IntegratedRestoreContextSnapshot(**_with_overrides(defaults, overrides))


def create_v0405_integrated_restore_packet(**overrides: Any) -> V0405IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0405",
        "snapshot": create_v0405_integrated_restore_context_snapshot(),
        "restore_sections": create_v0405_integrated_restore_sections(),
        "required_test_commands": (
            r"py -m pytest tests\test_v0405_provider_prompt_boundary_deepening_restore.py",
            r"py -m pytest tests\test_v0404_human_checkpoint_hardening_restore.py",
            r"py -m pytest tests\test_v0403_negative_runtime_gate_regression.py",
            r"py -m pytest tests\test_v0402_manual_two_iteration_rehearsal.py",
            r"py -m pytest tests\test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",
            r"py -m pytest tests\test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
            r"py -m pytest tests\test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        ),
        "required_false_flags": REQUIRED_FALSE_FLAGS,
        "restore_prompt_summary": "Continue ChantaCore after v0.40.5 without opening provider or prompt runtime authority.",
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0405IntegratedRestorePacket(**_with_overrides(defaults, overrides))


def create_v0405_integrated_restore_document_manifest(**overrides: Any) -> V0405IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0405",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0405IntegratedRestoreDocumentManifest(**_with_overrides(defaults, overrides))


def create_v0406_verifier_subagent_boundary_handoff(**overrides: Any) -> V0406VerifierSubagentBoundaryHandoff:
    defaults = {
        "handoff_id": "v0406-verifier-subagent-boundary-handoff",
        "target_version": "v0.40.6 Verifier Subagent Boundary Deepening",
        "target_track": "Standalone-Agent Preparation Track: Verifier Subagent Boundary Deepening",
        "recommended_focus": (
            "VerifierSubagentBoundary hardening",
            "VerifierRoleContract",
            "VerifierEvidenceRequirement",
            "VerifierContextIsolationContract",
            "SubagentVerificationRequestDraft remains draft-only",
            "no actual subagent invocation",
            "no parent raw transcript sharing",
        ),
        "required_inputs_from_v0405": (
            "prompt_submission_gate",
            "provider_invocation_gate",
            "provider_output_quarantine_contract",
            "integrated_restore_packet",
        ),
        "risk_notes": (
            "verifier request drafts must remain non-invoking",
            "provider/prompt gates must not be bypassed by verifier handoff",
        ),
    }
    return V0406VerifierSubagentBoundaryHandoff(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_provider_prompt_signal(
    provider_prompt_boundary_passed: bool = True,
    blocking_runtime_gaps: tuple[str, ...] = ("ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"),
    **overrides: Any,
) -> V041SmokeRunAccelerationProviderPromptSignal:
    if not provider_prompt_boundary_passed:
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
        "signal_id": "v041-smoke-run-provider-prompt-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "provider_prompt_boundary_passed": provider_prompt_boundary_passed,
        "blocking_runtime_gaps": blocking_runtime_gaps,
        "safety_conditions_for_acceleration": (
            "prompt_submission_gate_remains_blocked",
            "provider_invocation_gate_remains_blocked",
            "provider_output_quarantine_required",
            "standalone_runtime_components_remain_future_gated",
        ),
        "recommendation": recommendation,
        "metadata": {"ready_for_standalone_default_personal_runtime": False},
    }
    return V041SmokeRunAccelerationProviderPromptSignal(**_with_overrides(defaults, overrides))


def provider_prompt_readiness_preserves_no_unsafe_runtime(report: ProviderPromptBoundaryReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in REQUIRED_FALSE_FLAGS)


def prompt_dispatch_candidate_is_metadata_only(candidate: PromptDispatchCandidate) -> bool:
    return (
        candidate.metadata_only
        and not candidate.submitted_to_model
        and not candidate.provider_invoked
        and not candidate.network_used
        and not candidate.credential_accessed
        and not candidate.runtime_authority_granted
    )


def provider_invocation_evaluation_is_blocked(evaluation: ProviderInvocationGateEvaluation) -> bool:
    return (
        evaluation.blocked
        and not evaluation.provider_invoked
        and not evaluation.network_used
        and not evaluation.credential_accessed
        and not evaluation.client_created
        and not evaluation.executed
    )


def integrated_restore_packet_uses_single_doc(packet: V0405IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def v041_provider_prompt_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationProviderPromptSignal) -> bool:
    return signal.metadata.get("ready_for_standalone_default_personal_runtime") is False
