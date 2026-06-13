"""v0.40.4 scope-bound human checkpoint hardening metadata.

This layer narrows human checkpoint approval to a declared loop, iteration,
rehearsal, artifact set, and freshness policy. It creates restore metadata for
future handoff. It does not execute runtime actions, invoke providers, submit
prompts, invoke subagents, mutate live workspace, open standalone runtime, or
certify production readiness.
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
    LoopDecisionRecord,
    MissionLoopEnvelope,
    V040ReadinessReport,
)
from .repair_mission_loop_negative_gates import (
    DeniedRuntimeActionCoverageMatrix,
    NegativeRuntimeGateDecision,
    NegativeRuntimeGateEvaluation,
    NegativeRuntimeGateReadinessReport,
    ProductionCertificationFalseClaimAudit,
    StandaloneRuntimeFalseClaimAudit,
    V041SmokeRunAccelerationSafetySignal,
)
from .repair_mission_loop_rehearsal import (
    DefaultPersonalAccelerationAssessment,
    DefaultPersonalStandaloneGapRegister,
    SandboxRehearsalResult,
    SandboxRehearsalSafetyReport,
    StandaloneAgentRuntimeStatus,
)
from .repair_mission_loop_two_iteration import (
    ManualIterationCheckpointDecision,
    ManualIterationCheckpointRequest,
    ManualTwoIterationReadinessReport,
    ManualTwoIterationSafetyReport,
    NoAutonomousContinuationGuarantee,
    SecondIterationEligibilityDecision,
    StandaloneRuntimeStillClosedRecord,
    V041SmokeRunAccelerationSignal,
)


V0404_VERSION = "v0.40.4"
V0404_RELEASE_NAME = "v0.40.4 Human Checkpoint Hardening & Scope-Bound Approval Contract"
V0404_TRACK_NAME = (
    "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + "
    "Sandbox Rehearsal + Manual Checkpoint Gate + Negative Runtime Gate "
    "Regression + Scope-Bound Human Approval"
)


class CheckpointScopeKind(StrEnum):
    LOOP = "loop"
    MISSION = "mission"
    ITERATION = "iteration"
    CHECKPOINT_REQUEST = "checkpoint_request"
    CHECKPOINT_DECISION = "checkpoint_decision"
    SANDBOX_REHEARSAL = "sandbox_rehearsal"
    MANUAL_TWO_ITERATION_REHEARSAL = "manual_two_iteration_rehearsal"
    NEGATIVE_GATE_REGRESSION = "negative_gate_regression"
    ARTIFACT_SET = "artifact_set"
    RESTORE_PACKET = "restore_packet"


class CheckpointDecisionKind(StrEnum):
    APPROVE_SCOPED_REHEARSAL = "approve_scoped_rehearsal"
    REQUEST_MORE_EVIDENCE = "request_more_evidence"
    STOP = "stop"
    DO_NOTHING = "do_nothing"
    REJECT = "reject"
    REVOKE = "revoke"
    EXPIRE = "expire"


ALLOWED_ACTION_CLASSES: tuple[str, ...] = (
    "manual_second_iteration_rehearsal",
    "request_more_evidence",
    "stop",
    "do_nothing",
    "reject",
    "restore_context_only",
)

FORBIDDEN_ACTION_CLASSES: tuple[str, ...] = (
    "model_provider_invocation",
    "prompt_submission",
    "subagent_invocation",
    "live_workspace_apply",
    "autonomous_loop",
    "retry_loop",
    "dominion_runtime",
    "production_certification",
)

REQUIRED_RESTORE_SECTION_IDS: tuple[str, ...] = (
    "restore_purpose",
    "current_baseline",
    "version_chain",
    "implemented_artifacts",
    "files_added_modified",
    "safety_flags",
    "runtime_boundaries",
    "standalone_runtime_status",
    "test_commands",
    "known_limitations",
    "withdrawal_conditions",
    "v0405_handoff",
    "v041_smoke_run_status",
    "copy_paste_restore_prompt",
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

BASELINE_VERSIONS: tuple[str, ...] = (
    "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation",
    "v0.40.1 Sandbox Rehearsal Runner & Standalone Agent Readiness Clarification",
    "v0.40.2 Manual Two-Iteration Rehearsal & Human Checkpoint Enforcement",
    "v0.40.3 Negative Runtime Gate Regression & Denied Runtime Action Coverage",
    "v0.40.4 Human Checkpoint Hardening & Scope-Bound Approval Contract",
)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0404_VERSION not in version:
        raise ValueError("version must include v0.40.4")


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
class CheckpointApprovalScope:
    scope_id: str
    loop_id: str
    mission_id: str | None
    iteration_index: int
    checkpoint_request_id: str
    approved_rehearsal_id: str | None
    approved_action_class: str
    artifact_refs: tuple[str, ...]
    scope_kinds: tuple[str, ...]
    broad_future_authority_allowed: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_id", "loop_id", "checkpoint_request_id", "approved_action_class"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("artifact_refs", self.artifact_refs)
        _validate_tuple("scope_kinds", self.scope_kinds)
        _validate_dict("metadata", self.metadata)
        if self.iteration_index < 0:
            raise ValueError("iteration_index must be >= 0")
        if self.approved_action_class in FORBIDDEN_ACTION_CLASSES:
            raise ValueError("approved_action_class is forbidden in v0.40.4")
        if self.approved_action_class not in ALLOWED_ACTION_CLASSES:
            raise ValueError("approved_action_class must be a v0.40.4 allowed class")
        required = {
            CheckpointScopeKind.LOOP.value,
            CheckpointScopeKind.ITERATION.value,
            CheckpointScopeKind.CHECKPOINT_REQUEST.value,
            CheckpointScopeKind.ARTIFACT_SET.value,
        }
        if not required.issubset(set(self.scope_kinds)):
            raise ValueError("scope_kinds must bind loop, iteration, checkpoint request, and artifact set")
        _validate_false(self, ("broad_future_authority_allowed",))


@dataclass(frozen=True)
class CheckpointArtifactBinding:
    binding_id: str
    checkpoint_request_ref: str
    checkpoint_decision_ref: str
    loop_ref: str
    iteration_state_ref: str | None
    rehearsal_result_ref: str | None
    safety_report_ref: str | None
    negative_gate_report_ref: str | None
    restore_packet_ref: str | None
    bound_artifact_refs: tuple[str, ...]
    artifact_binding_required: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("binding_id", "checkpoint_request_ref", "checkpoint_decision_ref", "loop_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("bound_artifact_refs", self.bound_artifact_refs)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("artifact_binding_required",))
        if not self.bound_artifact_refs:
            raise ValueError("bound_artifact_refs must not be empty")


@dataclass(frozen=True)
class CheckpointFreshnessPolicy:
    policy_id: str
    valid_for_loop_id: str
    valid_for_iteration_index: int
    valid_for_checkpoint_request_id: str
    stale_if_iteration_changed: bool
    stale_if_artifacts_changed: bool
    stale_if_policy_version_changed: bool
    stale_if_revoked: bool
    max_age_marker: str | None
    freshness_required: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("policy_id", "valid_for_loop_id", "valid_for_checkpoint_request_id"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.valid_for_iteration_index < 0:
            raise ValueError("valid_for_iteration_index must be >= 0")
        _validate_true(
            self,
            (
                "stale_if_iteration_changed",
                "stale_if_artifacts_changed",
                "stale_if_policy_version_changed",
                "stale_if_revoked",
                "freshness_required",
            ),
        )


@dataclass(frozen=True)
class CheckpointFreshnessEvaluation:
    evaluation_id: str
    policy_id: str
    checkpoint_decision_ref: str
    current_loop_id: str
    current_iteration_index: int
    current_artifact_refs: tuple[str, ...]
    revoked: bool
    policy_version_changed: bool
    fresh: bool
    stale_reason: str | None
    expected_loop_id: str | None = None
    expected_iteration_index: int | None = None
    expected_artifact_refs: tuple[str, ...] = ()
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evaluation_id", "policy_id", "checkpoint_decision_ref", "current_loop_id"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("current_artifact_refs", self.current_artifact_refs)
        _validate_tuple("expected_artifact_refs", self.expected_artifact_refs)
        _validate_dict("metadata", self.metadata)
        if self.current_iteration_index < 0:
            raise ValueError("current_iteration_index must be >= 0")
        if self.fresh and self.stale_reason is not None:
            raise ValueError("fresh evaluation cannot carry a stale reason")
        if not self.fresh:
            _require_non_blank("stale_reason", self.stale_reason)


@dataclass(frozen=True)
class ScopeBoundCheckpointDecision:
    decision_id: str
    checkpoint_request_id: str
    loop_id: str
    mission_id: str | None
    iteration_index: int
    decision_kind: str
    approval_scope: CheckpointApprovalScope
    artifact_binding: CheckpointArtifactBinding
    freshness_policy_ref: str
    reviewed_evidence_refs: tuple[str, ...]
    approval_grants_runtime_authority: bool
    approval_grants_live_workspace_authority: bool
    approval_grants_model_invocation_authority: bool
    approval_grants_prompt_submission_authority: bool
    approval_grants_subagent_invocation_authority: bool
    approval_grants_autonomous_continuation_authority: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "checkpoint_request_id", "loop_id", "decision_kind", "freshness_policy_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("reviewed_evidence_refs", self.reviewed_evidence_refs)
        _validate_dict("metadata", self.metadata)
        if self.decision_kind not in {item.value for item in CheckpointDecisionKind}:
            raise ValueError("decision_kind must be a v0.40.4 checkpoint decision")
        if self.iteration_index != self.approval_scope.iteration_index:
            raise ValueError("decision iteration must match approval scope")
        if self.loop_id != self.approval_scope.loop_id:
            raise ValueError("decision loop must match approval scope")
        if self.checkpoint_request_id != self.approval_scope.checkpoint_request_id:
            raise ValueError("decision request must match approval scope")
        _validate_false(
            self,
            (
                "approval_grants_runtime_authority",
                "approval_grants_live_workspace_authority",
                "approval_grants_model_invocation_authority",
                "approval_grants_prompt_submission_authority",
                "approval_grants_subagent_invocation_authority",
                "approval_grants_autonomous_continuation_authority",
            ),
        )


@dataclass(frozen=True)
class CheckpointApprovalValidationInput:
    validation_id: str
    decision: ScopeBoundCheckpointDecision
    freshness_evaluation: CheckpointFreshnessEvaluation
    expected_loop_id: str
    expected_iteration_index: int
    expected_checkpoint_request_id: str
    expected_artifact_refs: tuple[str, ...]
    negative_gate_report_ref: str | None
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_id", "expected_loop_id", "expected_checkpoint_request_id"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_tuple("expected_artifact_refs", self.expected_artifact_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class CheckpointApprovalValidationResult:
    result_id: str
    validation_id: str
    valid: bool
    reason: str
    scope_valid: bool
    artifact_binding_valid: bool
    freshness_valid: bool
    negative_gate_compatible: bool
    runtime_authority_granted: bool
    safe_to_construct_second_iteration_candidate: bool
    safe_to_execute_runtime_action: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("result_id", "validation_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, ("runtime_authority_granted", "safe_to_execute_runtime_action"))
        should_be_valid = (
            self.scope_valid
            and self.artifact_binding_valid
            and self.freshness_valid
            and self.negative_gate_compatible
            and not self.runtime_authority_granted
        )
        if self.valid != should_be_valid:
            raise ValueError("valid must match scope, binding, freshness, gate, and authority checks")
        if self.safe_to_construct_second_iteration_candidate and not self.valid:
            raise ValueError("manual second iteration candidate requires a valid approval")


@dataclass(frozen=True)
class CheckpointApprovalAuthorityBoundary:
    boundary_id: str
    checkpoint_decision_ref: str
    allows_manual_rehearsal_candidate: bool
    allows_runtime_execution: bool
    allows_live_workspace_mutation: bool
    allows_model_invocation: bool
    allows_prompt_submission: bool
    allows_subagent_invocation: bool
    allows_external_agent_execution: bool
    allows_autonomous_continuation: bool
    allows_retry_loop: bool
    allows_dominion_runtime: bool
    allows_production_certification: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_id", self.boundary_id)
        _require_non_blank("checkpoint_decision_ref", self.checkpoint_decision_ref)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(
            self,
            (
                "allows_runtime_execution",
                "allows_live_workspace_mutation",
                "allows_model_invocation",
                "allows_prompt_submission",
                "allows_subagent_invocation",
                "allows_external_agent_execution",
                "allows_autonomous_continuation",
                "allows_retry_loop",
                "allows_dominion_runtime",
                "allows_production_certification",
            ),
        )


@dataclass(frozen=True)
class CheckpointRevocationRecord:
    revocation_id: str
    checkpoint_decision_ref: str
    revoked: bool
    revocation_reason: str
    revoked_by_ref: str | None
    revocation_evidence_refs: tuple[str, ...]
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("revocation_id", self.revocation_id)
        _require_non_blank("checkpoint_decision_ref", self.checkpoint_decision_ref)
        _require_non_blank("revocation_reason", self.revocation_reason)
        _validate_version(self.version)
        _validate_tuple("revocation_evidence_refs", self.revocation_evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class CheckpointExpiryRecord:
    expiry_id: str
    checkpoint_decision_ref: str
    expired: bool
    expiry_reason: str
    expiry_evidence_refs: tuple[str, ...]
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("expiry_id", self.expiry_id)
        _require_non_blank("checkpoint_decision_ref", self.checkpoint_decision_ref)
        _require_non_blank("expiry_reason", self.expiry_reason)
        _validate_version(self.version)
        _validate_tuple("expiry_evidence_refs", self.expiry_evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class CheckpointHardeningAuditRecord:
    audit_id: str
    checked_scope_bound_approval: bool
    checked_artifact_binding: bool
    checked_freshness_policy: bool
    checked_revocation_and_expiry: bool
    checked_broad_approval_rejected: bool
    checked_stale_approval_rejected: bool
    checked_mismatched_artifact_rejected: bool
    checked_negative_gate_compatibility: bool
    checked_runtime_authority_not_granted: bool
    checked_standalone_runtime_not_opened: bool
    notes: tuple[str, ...]
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_id", self.audit_id)
        _validate_version(self.version)
        _validate_tuple("notes", self.notes)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "checked_scope_bound_approval",
                "checked_artifact_binding",
                "checked_freshness_policy",
                "checked_revocation_and_expiry",
                "checked_broad_approval_rejected",
                "checked_stale_approval_rejected",
                "checked_mismatched_artifact_rejected",
                "checked_negative_gate_compatibility",
                "checked_runtime_authority_not_granted",
                "checked_standalone_runtime_not_opened",
            ),
        )


@dataclass(frozen=True)
class CheckpointHardeningSafetyReport:
    report_id: str
    safe_for_v0404_checkpoint_hardening: bool
    safe_to_construct_manual_second_iteration_candidate: bool
    safe_for_runtime_execution: bool
    safe_for_live_workspace_apply: bool
    safe_for_model_invocation: bool
    safe_for_prompt_submission: bool
    safe_for_subagent_invocation: bool
    safe_for_autonomous_loop: bool
    safe_for_standalone_default_personal_runtime: bool
    safe_for_dominion_runtime: bool
    production_certified: bool
    requires_v0405_provider_prompt_boundary: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("safe_for_v0404_checkpoint_hardening", "requires_v0405_provider_prompt_boundary"))
        _validate_false(
            self,
            (
                "safe_for_runtime_execution",
                "safe_for_live_workspace_apply",
                "safe_for_model_invocation",
                "safe_for_prompt_submission",
                "safe_for_subagent_invocation",
                "safe_for_autonomous_loop",
                "safe_for_standalone_default_personal_runtime",
                "safe_for_dominion_runtime",
                "production_certified",
            ),
        )


@dataclass(frozen=True)
class CheckpointHardeningReadinessReport:
    report_id: str
    human_checkpoint_hardening_defined: bool
    scope_bound_approval_contract_ready: bool
    checkpoint_artifact_binding_ready: bool
    checkpoint_freshness_policy_ready: bool
    checkpoint_revocation_expiry_metadata_ready: bool
    restore_document_ready: bool
    v0405_handoff_ready: bool
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
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(
            self,
            (
                "human_checkpoint_hardening_defined",
                "scope_bound_approval_contract_ready",
                "checkpoint_artifact_binding_ready",
                "checkpoint_freshness_policy_ready",
                "checkpoint_revocation_expiry_metadata_ready",
                "restore_document_ready",
                "v0405_handoff_ready",
            ),
        )
        _validate_false(self, REQUIRED_FALSE_FLAGS)


@dataclass(frozen=True)
class RestoreDocumentSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("section_id", "title", "content_summary", "restore_value"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        if self.section_id not in REQUIRED_RESTORE_SECTION_IDS:
            raise ValueError("section_id must be a required v0.40.4 restore section")


@dataclass(frozen=True)
class V0404RestoreContextSnapshot:
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
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("snapshot_id", "current_version", "current_track", "next_recommended_version", "next_recommended_focus"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("baseline_versions", "implemented_modules", "test_files", "docs", "open_capabilities", "closed_capabilities"):
            _validate_tuple(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        missing_versions = set(BASELINE_VERSIONS).difference(self.baseline_versions)
        if missing_versions:
            raise ValueError(f"missing baseline versions: {sorted(missing_versions)}")
        required_closed = {
            "standalone_default_personal_runtime",
            "model_provider_invocation",
            "prompt_submission",
            "subagent_invocation",
            "live_workspace_apply",
            "autonomous_loop_runtime",
            "retry_loop",
            "dominion_runtime",
            "production_certification",
        }
        if not required_closed.issubset(set(self.closed_capabilities)):
            raise ValueError("closed_capabilities must include unsafe closed surfaces")


@dataclass(frozen=True)
class V0404RestorePacket:
    restore_packet_id: str
    snapshot: V0404RestoreContextSnapshot
    restore_sections: tuple[RestoreDocumentSection, ...]
    required_test_commands: tuple[str, ...]
    required_false_flags: tuple[str, ...]
    restore_prompt_summary: str
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("restore_packet_id", self.restore_packet_id)
        _require_non_blank("restore_prompt_summary", self.restore_prompt_summary)
        _validate_version(self.version)
        _validate_tuple("restore_sections", self.restore_sections)
        _validate_tuple("required_test_commands", self.required_test_commands)
        _validate_tuple("required_false_flags", self.required_false_flags)
        _validate_dict("metadata", self.metadata)
        section_ids = {section.section_id for section in self.restore_sections}
        missing = set(REQUIRED_RESTORE_SECTION_IDS).difference(section_ids)
        if missing:
            raise ValueError(f"missing restore sections: {sorted(missing)}")
        if set(self.required_false_flags) != set(REQUIRED_FALSE_FLAGS):
            raise ValueError("required_false_flags must match v0.40.4 canonical false flags")


@dataclass(frozen=True)
class V0404RestoreDocumentManifest:
    manifest_id: str
    restore_doc_path: str
    restore_doc_required: bool
    restore_packet_ref: str
    required_sections_present: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("manifest_id", "restore_doc_path", "restore_packet_ref"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_true(self, ("restore_doc_required", "copy_paste_restore_prompt_required"))
        if self.suitable_for_new_session_handoff and not self.required_sections_present:
            raise ValueError("new-session handoff requires all restore sections")


@dataclass(frozen=True)
class V0405ProviderPromptBoundaryHandoff:
    handoff_id: str
    target_version: str
    target_track: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0404: tuple[str, ...]
    risk_notes: tuple[str, ...]
    version: str = V0404_VERSION
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "target_version", "target_track"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("recommended_focus", "required_inputs_from_v0404", "risk_notes"):
            _validate_tuple(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if "v0.40.5 Provider / Prompt Boundary Deepening" not in self.target_version:
            raise ValueError("target_version must target v0.40.5 Provider / Prompt Boundary Deepening")


@dataclass(frozen=True)
class V041SmokeRunAccelerationCheckpointSignal:
    signal_id: str
    conservative_target: str
    earliest_candidate_target: str | None
    checkpoint_hardening_passed: bool
    blocking_runtime_gaps: tuple[str, ...]
    safety_conditions_for_acceleration: tuple[str, ...]
    recommendation: str
    version: str = V0404_VERSION
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


def create_checkpoint_approval_scope(**overrides: Any) -> CheckpointApprovalScope:
    defaults = {
        "scope_id": "scope-v0404",
        "loop_id": "loop-v0404",
        "mission_id": "mission-v0404",
        "iteration_index": 1,
        "checkpoint_request_id": "checkpoint-request-v0404",
        "approved_rehearsal_id": "rehearsal-v0404",
        "approved_action_class": "manual_second_iteration_rehearsal",
        "artifact_refs": ("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404"),
        "scope_kinds": (
            CheckpointScopeKind.LOOP.value,
            CheckpointScopeKind.MISSION.value,
            CheckpointScopeKind.ITERATION.value,
            CheckpointScopeKind.CHECKPOINT_REQUEST.value,
            CheckpointScopeKind.SANDBOX_REHEARSAL.value,
            CheckpointScopeKind.ARTIFACT_SET.value,
        ),
        "broad_future_authority_allowed": False,
    }
    return CheckpointApprovalScope(**_with_overrides(defaults, overrides))


def create_checkpoint_artifact_binding(**overrides: Any) -> CheckpointArtifactBinding:
    defaults = {
        "binding_id": "binding-v0404",
        "checkpoint_request_ref": "checkpoint-request-v0404",
        "checkpoint_decision_ref": "checkpoint-decision-v0404",
        "loop_ref": "loop-v0404",
        "iteration_state_ref": "iteration-state-v0404",
        "rehearsal_result_ref": "rehearsal-result-v0404",
        "safety_report_ref": "safety-report-v0404",
        "negative_gate_report_ref": "negative-gate-v0404",
        "restore_packet_ref": None,
        "bound_artifact_refs": ("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404"),
        "artifact_binding_required": True,
    }
    return CheckpointArtifactBinding(**_with_overrides(defaults, overrides))


def create_checkpoint_freshness_policy(**overrides: Any) -> CheckpointFreshnessPolicy:
    defaults = {
        "policy_id": "freshness-policy-v0404",
        "valid_for_loop_id": "loop-v0404",
        "valid_for_iteration_index": 1,
        "valid_for_checkpoint_request_id": "checkpoint-request-v0404",
        "stale_if_iteration_changed": True,
        "stale_if_artifacts_changed": True,
        "stale_if_policy_version_changed": True,
        "stale_if_revoked": True,
        "max_age_marker": "single-checkpoint-window",
        "freshness_required": True,
    }
    return CheckpointFreshnessPolicy(**_with_overrides(defaults, overrides))


def evaluate_checkpoint_freshness(
    policy: CheckpointFreshnessPolicy | None = None,
    *,
    checkpoint_decision_ref: str = "checkpoint-decision-v0404",
    current_loop_id: str = "loop-v0404",
    current_iteration_index: int = 1,
    current_artifact_refs: tuple[str, ...] = ("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404"),
    expected_artifact_refs: tuple[str, ...] = ("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404"),
    revoked: bool = False,
    policy_version_changed: bool = False,
    **overrides: Any,
) -> CheckpointFreshnessEvaluation:
    policy = policy or create_checkpoint_freshness_policy()
    fresh = True
    stale_reason: str | None = None
    if current_loop_id != policy.valid_for_loop_id:
        fresh = False
        stale_reason = "loop_mismatch"
    elif policy.stale_if_iteration_changed and current_iteration_index != policy.valid_for_iteration_index:
        fresh = False
        stale_reason = "iteration_mismatch"
    elif policy.stale_if_artifacts_changed and set(current_artifact_refs) != set(expected_artifact_refs):
        fresh = False
        stale_reason = "artifact_mismatch"
    elif policy.stale_if_revoked and revoked:
        fresh = False
        stale_reason = "revoked"
    elif policy.stale_if_policy_version_changed and policy_version_changed:
        fresh = False
        stale_reason = "policy_version_changed"
    defaults = {
        "evaluation_id": "freshness-evaluation-v0404",
        "policy_id": policy.policy_id,
        "checkpoint_decision_ref": checkpoint_decision_ref,
        "current_loop_id": current_loop_id,
        "current_iteration_index": current_iteration_index,
        "current_artifact_refs": current_artifact_refs,
        "revoked": revoked,
        "policy_version_changed": policy_version_changed,
        "fresh": fresh,
        "stale_reason": stale_reason,
        "expected_loop_id": policy.valid_for_loop_id,
        "expected_iteration_index": policy.valid_for_iteration_index,
        "expected_artifact_refs": expected_artifact_refs,
    }
    return CheckpointFreshnessEvaluation(**_with_overrides(defaults, overrides))


def create_scope_bound_checkpoint_decision(**overrides: Any) -> ScopeBoundCheckpointDecision:
    scope = overrides.pop("approval_scope", create_checkpoint_approval_scope())
    binding = overrides.pop("artifact_binding", create_checkpoint_artifact_binding())
    defaults = {
        "decision_id": "checkpoint-decision-v0404",
        "checkpoint_request_id": scope.checkpoint_request_id,
        "loop_id": scope.loop_id,
        "mission_id": scope.mission_id,
        "iteration_index": scope.iteration_index,
        "decision_kind": CheckpointDecisionKind.APPROVE_SCOPED_REHEARSAL.value,
        "approval_scope": scope,
        "artifact_binding": binding,
        "freshness_policy_ref": "freshness-policy-v0404",
        "reviewed_evidence_refs": scope.artifact_refs,
        "approval_grants_runtime_authority": False,
        "approval_grants_live_workspace_authority": False,
        "approval_grants_model_invocation_authority": False,
        "approval_grants_prompt_submission_authority": False,
        "approval_grants_subagent_invocation_authority": False,
        "approval_grants_autonomous_continuation_authority": False,
    }
    return ScopeBoundCheckpointDecision(**_with_overrides(defaults, overrides))


def validate_checkpoint_approval_scope(
    scope: CheckpointApprovalScope,
    *,
    expected_loop_id: str,
    expected_iteration_index: int,
    expected_checkpoint_request_id: str,
    expected_artifact_refs: tuple[str, ...],
) -> bool:
    return (
        scope.loop_id == expected_loop_id
        and scope.iteration_index == expected_iteration_index
        and scope.checkpoint_request_id == expected_checkpoint_request_id
        and set(expected_artifact_refs).issubset(set(scope.artifact_refs))
        and scope.approved_action_class in ALLOWED_ACTION_CLASSES
        and scope.approved_action_class not in FORBIDDEN_ACTION_CLASSES
        and scope.broad_future_authority_allowed is False
    )


def validate_checkpoint_artifact_binding(
    binding: CheckpointArtifactBinding,
    *,
    expected_checkpoint_request_id: str,
    expected_artifact_refs: tuple[str, ...],
    negative_gate_report_ref: str | None,
) -> bool:
    if not binding.artifact_binding_required:
        return False
    if binding.checkpoint_request_ref != expected_checkpoint_request_id:
        return False
    if not set(expected_artifact_refs).issubset(set(binding.bound_artifact_refs)):
        return False
    if negative_gate_report_ref and binding.negative_gate_report_ref != negative_gate_report_ref:
        return False
    return True


def validate_scope_bound_checkpoint_decision(validation_input: CheckpointApprovalValidationInput, **overrides: Any) -> CheckpointApprovalValidationResult:
    decision = validation_input.decision
    scope_valid = validate_checkpoint_approval_scope(
        decision.approval_scope,
        expected_loop_id=validation_input.expected_loop_id,
        expected_iteration_index=validation_input.expected_iteration_index,
        expected_checkpoint_request_id=validation_input.expected_checkpoint_request_id,
        expected_artifact_refs=validation_input.expected_artifact_refs,
    )
    artifact_binding_valid = validate_checkpoint_artifact_binding(
        decision.artifact_binding,
        expected_checkpoint_request_id=validation_input.expected_checkpoint_request_id,
        expected_artifact_refs=validation_input.expected_artifact_refs,
        negative_gate_report_ref=validation_input.negative_gate_report_ref,
    )
    freshness_valid = validation_input.freshness_evaluation.fresh
    negative_gate_compatible = (
        validation_input.negative_gate_report_ref is not None
        and decision.decision_kind == CheckpointDecisionKind.APPROVE_SCOPED_REHEARSAL.value
        and decision.approval_scope.approved_action_class == "manual_second_iteration_rehearsal"
    )
    runtime_authority_granted = any(
        (
            decision.approval_grants_runtime_authority,
            decision.approval_grants_live_workspace_authority,
            decision.approval_grants_model_invocation_authority,
            decision.approval_grants_prompt_submission_authority,
            decision.approval_grants_subagent_invocation_authority,
            decision.approval_grants_autonomous_continuation_authority,
        )
    )
    valid = scope_valid and artifact_binding_valid and freshness_valid and negative_gate_compatible and not runtime_authority_granted
    safe_candidate = (
        valid
        and decision.decision_kind == CheckpointDecisionKind.APPROVE_SCOPED_REHEARSAL.value
        and decision.approval_scope.approved_action_class == "manual_second_iteration_rehearsal"
    )
    reason = "valid_scoped_manual_rehearsal_candidate" if valid else "invalid_checkpoint_approval"
    defaults = {
        "result_id": "validation-result-v0404",
        "validation_id": validation_input.validation_id,
        "valid": valid,
        "reason": reason,
        "scope_valid": scope_valid,
        "artifact_binding_valid": artifact_binding_valid,
        "freshness_valid": freshness_valid,
        "negative_gate_compatible": negative_gate_compatible,
        "runtime_authority_granted": False,
        "safe_to_construct_second_iteration_candidate": safe_candidate,
        "safe_to_execute_runtime_action": False,
    }
    return CheckpointApprovalValidationResult(**_with_overrides(defaults, overrides))


def create_checkpoint_approval_authority_boundary(
    validation_result: CheckpointApprovalValidationResult | None = None,
    checkpoint_decision_ref: str = "checkpoint-decision-v0404",
    **overrides: Any,
) -> CheckpointApprovalAuthorityBoundary:
    validation_result = validation_result or validate_scope_bound_checkpoint_decision(
        CheckpointApprovalValidationInput(
            validation_id="validation-v0404",
            decision=create_scope_bound_checkpoint_decision(),
            freshness_evaluation=evaluate_checkpoint_freshness(),
            expected_loop_id="loop-v0404",
            expected_iteration_index=1,
            expected_checkpoint_request_id="checkpoint-request-v0404",
            expected_artifact_refs=("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404"),
            negative_gate_report_ref="negative-gate-v0404",
        )
    )
    defaults = {
        "boundary_id": "authority-boundary-v0404",
        "checkpoint_decision_ref": checkpoint_decision_ref,
        "allows_manual_rehearsal_candidate": validation_result.safe_to_construct_second_iteration_candidate,
        "allows_runtime_execution": False,
        "allows_live_workspace_mutation": False,
        "allows_model_invocation": False,
        "allows_prompt_submission": False,
        "allows_subagent_invocation": False,
        "allows_external_agent_execution": False,
        "allows_autonomous_continuation": False,
        "allows_retry_loop": False,
        "allows_dominion_runtime": False,
        "allows_production_certification": False,
    }
    return CheckpointApprovalAuthorityBoundary(**_with_overrides(defaults, overrides))


def create_checkpoint_revocation_record(**overrides: Any) -> CheckpointRevocationRecord:
    defaults = {
        "revocation_id": "revocation-v0404",
        "checkpoint_decision_ref": "checkpoint-decision-v0404",
        "revoked": True,
        "revocation_reason": "human_checkpoint_revoked",
        "revoked_by_ref": "human-operator",
        "revocation_evidence_refs": ("revocation-note-v0404",),
    }
    return CheckpointRevocationRecord(**_with_overrides(defaults, overrides))


def create_checkpoint_expiry_record(**overrides: Any) -> CheckpointExpiryRecord:
    defaults = {
        "expiry_id": "expiry-v0404",
        "checkpoint_decision_ref": "checkpoint-decision-v0404",
        "expired": True,
        "expiry_reason": "freshness_window_expired",
        "expiry_evidence_refs": ("expiry-note-v0404",),
    }
    return CheckpointExpiryRecord(**_with_overrides(defaults, overrides))


def create_checkpoint_hardening_audit_record(**overrides: Any) -> CheckpointHardeningAuditRecord:
    defaults = {
        "audit_id": "checkpoint-hardening-audit-v0404",
        "checked_scope_bound_approval": True,
        "checked_artifact_binding": True,
        "checked_freshness_policy": True,
        "checked_revocation_and_expiry": True,
        "checked_broad_approval_rejected": True,
        "checked_stale_approval_rejected": True,
        "checked_mismatched_artifact_rejected": True,
        "checked_negative_gate_compatibility": True,
        "checked_runtime_authority_not_granted": True,
        "checked_standalone_runtime_not_opened": True,
        "notes": ("approval remains scope-bound metadata",),
    }
    return CheckpointHardeningAuditRecord(**_with_overrides(defaults, overrides))


def create_checkpoint_hardening_safety_report(
    validation_result: CheckpointApprovalValidationResult | None = None,
    **overrides: Any,
) -> CheckpointHardeningSafetyReport:
    validation_result = validation_result or validate_scope_bound_checkpoint_decision(
        CheckpointApprovalValidationInput(
            validation_id="validation-v0404",
            decision=create_scope_bound_checkpoint_decision(),
            freshness_evaluation=evaluate_checkpoint_freshness(),
            expected_loop_id="loop-v0404",
            expected_iteration_index=1,
            expected_checkpoint_request_id="checkpoint-request-v0404",
            expected_artifact_refs=("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404"),
            negative_gate_report_ref="negative-gate-v0404",
        )
    )
    defaults = {
        "report_id": "checkpoint-hardening-safety-v0404",
        "safe_for_v0404_checkpoint_hardening": validation_result.valid,
        "safe_to_construct_manual_second_iteration_candidate": validation_result.safe_to_construct_second_iteration_candidate,
        "safe_for_runtime_execution": False,
        "safe_for_live_workspace_apply": False,
        "safe_for_model_invocation": False,
        "safe_for_prompt_submission": False,
        "safe_for_subagent_invocation": False,
        "safe_for_autonomous_loop": False,
        "safe_for_standalone_default_personal_runtime": False,
        "safe_for_dominion_runtime": False,
        "production_certified": False,
        "requires_v0405_provider_prompt_boundary": True,
    }
    return CheckpointHardeningSafetyReport(**_with_overrides(defaults, overrides))


def create_checkpoint_hardening_readiness_report(**overrides: Any) -> CheckpointHardeningReadinessReport:
    defaults = {
        "report_id": "checkpoint-hardening-readiness-v0404",
        "human_checkpoint_hardening_defined": True,
        "scope_bound_approval_contract_ready": True,
        "checkpoint_artifact_binding_ready": True,
        "checkpoint_freshness_policy_ready": True,
        "checkpoint_revocation_expiry_metadata_ready": True,
        "restore_document_ready": True,
        "v0405_handoff_ready": True,
        **{name: False for name in REQUIRED_FALSE_FLAGS},
    }
    return CheckpointHardeningReadinessReport(**_with_overrides(defaults, overrides))


def create_restore_document_sections() -> tuple[RestoreDocumentSection, ...]:
    titles = {
        "restore_purpose": "Restore Purpose",
        "current_baseline": "Current Baseline",
        "version_chain": "Version Chain Summary",
        "implemented_artifacts": "Implemented Artifacts",
        "files_added_modified": "Files Added / Modified",
        "safety_flags": "Safety Flag Canonical Values",
        "runtime_boundaries": "Runtime Boundaries",
        "standalone_runtime_status": "Standalone Default Personal Runtime Status",
        "test_commands": "Required Test Commands",
        "known_limitations": "Known Limitations",
        "withdrawal_conditions": "Withdrawal Conditions",
        "v0405_handoff": "v0.40.5 Handoff",
        "v041_smoke_run_status": "v0.41 Smoke Run Status",
        "copy_paste_restore_prompt": "Copy-Paste Restore Prompt",
    }
    return tuple(
        RestoreDocumentSection(
            section_id=section_id,
            title=titles[section_id],
            required=True,
            content_summary=f"{titles[section_id]} is required for v0.40.4 restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0404_restore_context_snapshot(**overrides: Any) -> V0404RestoreContextSnapshot:
    defaults = {
        "snapshot_id": "restore-snapshot-v0404",
        "current_version": V0404_RELEASE_NAME,
        "current_track": V0404_TRACK_NAME,
        "baseline_versions": BASELINE_VERSIONS,
        "implemented_modules": (
            "repair_mission_loop_boundary",
            "repair_mission_loop_rehearsal",
            "repair_mission_loop_two_iteration",
            "repair_mission_loop_negative_gates",
            "repair_mission_loop_checkpoint_hardening",
        ),
        "test_files": (
            "tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
            "tests/test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",
            "tests/test_v0402_manual_two_iteration_rehearsal.py",
            "tests/test_v0403_negative_runtime_gate_regression.py",
            "tests/test_v0404_human_checkpoint_hardening_restore.py",
        ),
        "docs": (
            "docs/versions/v0.40/v0.40.4_human_checkpoint_hardening.md",
            "docs/versions/v0.40/v0.40.4_scope_bound_approval_contract.md",
            "docs/versions/v0.40/v0.40.4_restore_document.md",
        ),
        "open_capabilities": (
            "scope_bound_checkpoint_approval",
            "checkpoint_freshness_metadata",
            "checkpoint_artifact_binding",
            "checkpoint_revocation_expiry_metadata",
            "restore_packet",
        ),
        "closed_capabilities": (
            "standalone_default_personal_runtime",
            "model_provider_invocation",
            "prompt_submission",
            "subagent_invocation",
            "live_workspace_apply",
            "autonomous_loop_runtime",
            "retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
        "next_recommended_version": "v0.40.5 Provider / Prompt Boundary Deepening",
        "next_recommended_focus": "Provider and prompt boundary deepening without invocation or submission",
    }
    return V0404RestoreContextSnapshot(**_with_overrides(defaults, overrides))


def create_v0404_restore_packet(**overrides: Any) -> V0404RestorePacket:
    defaults = {
        "restore_packet_id": "restore-packet-v0404",
        "snapshot": create_v0404_restore_context_snapshot(),
        "restore_sections": create_restore_document_sections(),
        "required_test_commands": (
            r"py -m pytest tests\test_v0404_human_checkpoint_hardening_restore.py",
            r"py -m pytest tests\test_v0403_negative_runtime_gate_regression.py",
            r"py -m pytest tests\test_v0402_manual_two_iteration_rehearsal.py",
            r"py -m pytest tests\test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",
            r"py -m pytest tests\test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
            r"py -m pytest tests\test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        ),
        "required_false_flags": REQUIRED_FALSE_FLAGS,
        "restore_prompt_summary": "Continue ChantaCore after v0.40.4 without opening unsafe runtime authority.",
    }
    return V0404RestorePacket(**_with_overrides(defaults, overrides))


def create_v0404_restore_document_manifest(**overrides: Any) -> V0404RestoreDocumentManifest:
    defaults = {
        "manifest_id": "restore-document-manifest-v0404",
        "restore_doc_path": "docs/versions/v0.40/v0.40.4_restore_document.md",
        "restore_doc_required": True,
        "restore_packet_ref": "restore-packet-v0404",
        "required_sections_present": True,
        "copy_paste_restore_prompt_required": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0404RestoreDocumentManifest(**_with_overrides(defaults, overrides))


def create_v0405_provider_prompt_boundary_handoff(**overrides: Any) -> V0405ProviderPromptBoundaryHandoff:
    defaults = {
        "handoff_id": "v0405-provider-prompt-boundary-handoff",
        "target_version": "v0.40.5 Provider / Prompt Boundary Deepening",
        "target_track": "Standalone-Agent Preparation Track: Provider / Prompt Boundary Deepening",
        "recommended_focus": (
            "ProviderBoundaryGate hardening",
            "PromptSubmissionBoundary hardening",
            "ProviderOutputQuarantineContract",
            "PromptDispatchCandidate",
            "PromptDispatchBlockedDecision",
            "no provider invocation",
            "no prompt submission",
        ),
        "required_inputs_from_v0404": (
            "scope_bound_checkpoint_decision",
            "checkpoint_freshness_policy",
            "checkpoint_artifact_binding",
            "negative_gate_compatibility",
            "restore_packet",
        ),
        "risk_notes": (
            "checkpoint approval must not become provider invocation authority",
            "prompt dispatch candidates must remain blocked until future gate",
        ),
    }
    return V0405ProviderPromptBoundaryHandoff(**_with_overrides(defaults, overrides))


def create_v041_smoke_run_acceleration_checkpoint_signal(
    checkpoint_hardening_passed: bool = True,
    blocking_runtime_gaps: tuple[str, ...] = ("ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"),
    **overrides: Any,
) -> V041SmokeRunAccelerationCheckpointSignal:
    if not checkpoint_hardening_passed:
        earliest = None
        recommendation = "do_not_accelerate"
    elif set(blocking_runtime_gaps) == {"ChatService", "CLI", "ProfileRuntime", "AgentLoop", "SkillExecutor"}:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    elif set(blocking_runtime_gaps).issubset({"CLI", "ProfileRuntime"}):
        earliest = "v0.41.5"
        recommendation = "possible_mild_acceleration"
    elif "SkillRegistry" in blocking_runtime_gaps and "AgentLoop" not in blocking_runtime_gaps:
        earliest = "v0.41.4"
        recommendation = "possible_acceleration_after_v0413"
    else:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    defaults = {
        "signal_id": "v041-smoke-run-checkpoint-signal",
        "conservative_target": "v0.41.6",
        "earliest_candidate_target": earliest,
        "checkpoint_hardening_passed": checkpoint_hardening_passed,
        "blocking_runtime_gaps": blocking_runtime_gaps,
        "safety_conditions_for_acceleration": (
            "scope_bound_checkpoint_approval_passes",
            "negative_runtime_gate_regression_remains_blocked",
            "standalone_runtime_components_remain_explicitly_gated",
        ),
        "recommendation": recommendation,
        "metadata": {"ready_for_standalone_default_personal_runtime": False},
    }
    return V041SmokeRunAccelerationCheckpointSignal(**_with_overrides(defaults, overrides))


def checkpoint_hardening_readiness_preserves_no_unsafe_runtime(report: CheckpointHardeningReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in REQUIRED_FALSE_FLAGS)


def scope_bound_decision_preserves_no_authority(decision: ScopeBoundCheckpointDecision) -> bool:
    return not any(
        (
            decision.approval_grants_runtime_authority,
            decision.approval_grants_live_workspace_authority,
            decision.approval_grants_model_invocation_authority,
            decision.approval_grants_prompt_submission_authority,
            decision.approval_grants_subagent_invocation_authority,
            decision.approval_grants_autonomous_continuation_authority,
        )
    )


def checkpoint_validation_never_allows_runtime_execution(result: CheckpointApprovalValidationResult) -> bool:
    return result.runtime_authority_granted is False and result.safe_to_execute_runtime_action is False


def restore_packet_is_suitable_for_new_session_handoff(packet: V0404RestorePacket, manifest: V0404RestoreDocumentManifest | None = None) -> bool:
    section_ids = {section.section_id for section in packet.restore_sections}
    manifest_ok = True if manifest is None else manifest.suitable_for_new_session_handoff
    return (
        set(REQUIRED_RESTORE_SECTION_IDS).issubset(section_ids)
        and set(packet.required_false_flags) == set(REQUIRED_FALSE_FLAGS)
        and bool(packet.restore_prompt_summary)
        and manifest_ok
    )


def v041_checkpoint_signal_is_not_runtime_start(signal: V041SmokeRunAccelerationCheckpointSignal) -> bool:
    return signal.metadata.get("ready_for_standalone_default_personal_runtime") is False

