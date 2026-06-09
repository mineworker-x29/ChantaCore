from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0361_VERSION = "v0.36.1"
V0361_RELEASE_NAME = "v0.36.1 Apply Candidate & Human Approval Contract"
MAX_PREVIEW_CHARS = 240

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_dry_run_apply_simulation",
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


class PatchApplyCandidateKind(StrEnum):
    FROM_REVIEW_PACKET = "from_review_packet"
    FROM_DIFF_PROPOSAL = "from_diff_proposal"
    FROM_STRUCTURED_PATCH = "from_structured_patch"
    FROM_UNIFIED_DIFF = "from_unified_diff"
    FROM_RISK_ACCEPTED_REVIEW = "from_risk_accepted_review"
    FROM_MANUAL_OPERATOR_REQUEST = "from_manual_operator_request"
    BLOCKED_CANDIDATE = "blocked_candidate"
    NO_OP_CANDIDATE = "no_op_candidate"
    UNKNOWN = "unknown"


class PatchApplyCandidateSourceKind(StrEnum):
    V0360_APPLY_SANDBOX_BOUNDARY = "v0360_apply_sandbox_boundary"
    V0359_V036_HANDOFF_PACKET = "v0359_v036_handoff_packet"
    V0359_CONSOLIDATION_REPORT = "v0359_consolidation_report"
    V0358_CLI_PATCH_PROPOSAL_SURFACE = "v0358_cli_patch_proposal_surface"
    V0357_PATCH_PROPOSAL_TRACE_PACKET = "v0357_patch_proposal_trace_packet"
    V0356_PATCH_REVIEW_PACKET = "v0356_patch_review_packet"
    V0356_APPROVAL_GATE_METADATA = "v0356_approval_gate_metadata"
    V0356_REVIEW_DECISION_RECORD = "v0356_review_decision_record"
    V0355_PATCH_PROPOSAL_RISK_REPORT = "v0355_patch_proposal_risk_report"
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    V0354_STRUCTURED_PATCH_PROPOSAL = "v0354_structured_patch_proposal"
    V0354_UNIFIED_DIFF_PROPOSAL = "v0354_unified_diff_proposal"
    V0353_PATCH_PLAN = "v0353_patch_plan"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchApplyCandidateStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    CANDIDATE_CREATED = "candidate_created"
    CANDIDATE_VALIDATED = "candidate_validated"
    CANDIDATE_VALIDATED_WITH_GAPS = "candidate_validated_with_gaps"
    HUMAN_APPROVAL_ATTACHED = "human_approval_attached"
    HUMAN_APPROVAL_VALIDATED = "human_approval_validated"
    ELIGIBLE_FOR_FUTURE_DRY_RUN = "eligible_for_future_dry_run"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class PatchApplyCandidateReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CANDIDATE_CONTRACT_READY = "candidate_contract_ready"
    HUMAN_APPROVAL_CONTRACT_READY = "human_approval_contract_ready"
    APPROVAL_EVIDENCE_VALIDATED = "approval_evidence_validated"
    ELIGIBILITY_DECISION_READY = "eligibility_decision_ready"
    DESIGN_HANDOFF_READY_FOR_V0362 = "design_handoff_ready_for_v0362"
    DESIGN_HANDOFF_READY_FOR_V0363 = "design_handoff_ready_for_v0363"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchApplyCandidateDecisionKind(StrEnum):
    ALLOW_CANDIDATE_METADATA = "allow_candidate_metadata"
    ALLOW_HUMAN_APPROVAL_CONTRACT_METADATA = "allow_human_approval_contract_metadata"
    ALLOW_OPERATOR_APPROVAL_EVIDENCE_METADATA = "allow_operator_approval_evidence_metadata"
    ALLOW_FUTURE_DRY_RUN_INPUT = "allow_future_dry_run_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchApplyCandidateRiskKind(StrEnum):
    MISSING_REVIEW_PACKET_RISK = "missing_review_packet_risk"
    MISSING_DIFF_PROPOSAL_RISK = "missing_diff_proposal_risk"
    MISSING_RISK_REPORT_RISK = "missing_risk_report_risk"
    BLOCKED_RISK_REPORT_RISK = "blocked_risk_report_risk"
    HUMAN_APPROVAL_MISSING_RISK = "human_approval_missing_risk"
    HUMAN_APPROVAL_AMBIGUOUS_RISK = "human_approval_ambiguous_risk"
    MODEL_GENERATED_APPROVAL_RISK = "model_generated_approval_risk"
    REVIEW_METADATA_AS_APPLY_APPROVAL_RISK = "review_metadata_as_apply_approval_risk"
    FORGED_APPROVAL_RISK = "forged_approval_risk"
    STALE_APPROVAL_RISK = "stale_approval_risk"
    SCOPE_MISMATCH_RISK = "scope_mismatch_risk"
    DIFF_MISMATCH_RISK = "diff_mismatch_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    SANDBOX_ESCAPE_RISK = "sandbox_escape_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    UNKNOWN = "unknown"


class HumanApprovalSourceKind(StrEnum):
    OPERATOR_SUPPLIED_EXPLICIT_APPROVAL = "operator_supplied_explicit_approval"
    OPERATOR_SUPPLIED_REVIEW_RECORD = "operator_supplied_review_record"
    OPERATOR_SUPPLIED_CLI_METADATA = "operator_supplied_cli_metadata"
    HUMAN_REVIEW_PACKET_METADATA = "human_review_packet_metadata"
    MODEL_GENERATED_APPROVAL = "model_generated_approval"
    AUTOMATED_PLACEHOLDER = "automated_placeholder"
    INFERRED_APPROVAL = "inferred_approval"
    MISSING_APPROVAL = "missing_approval"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class HumanApprovalEvidenceKind(StrEnum):
    EXPLICIT_OPERATOR_CONFIRMATION = "explicit_operator_confirmation"
    REVIEWER_IDENTITY_REF = "reviewer_identity_ref"
    APPROVAL_TIMESTAMP = "approval_timestamp"
    APPROVED_CANDIDATE_REF = "approved_candidate_ref"
    APPROVED_DIFF_REF = "approved_diff_ref"
    APPROVED_SCOPE_REF = "approved_scope_ref"
    APPROVAL_STATEMENT = "approval_statement"
    APPROVAL_NONCE_OR_TICKET_REF = "approval_nonce_or_ticket_ref"
    REVIEW_PACKET_REF = "review_packet_ref"
    MODEL_GENERATED_STATEMENT = "model_generated_statement"
    AUTOMATED_PLACEHOLDER = "automated_placeholder"
    UNKNOWN = "unknown"


class HumanApprovalStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_SUPPLIED = "not_supplied"
    SUPPLIED = "supplied"
    VALIDATED = "validated"
    VALIDATED_WITH_WARNINGS = "validated_with_warnings"
    INVALID = "invalid"
    REJECTED = "rejected"
    STALE = "stale"
    AMBIGUOUS = "ambiguous"
    FUTURE_GATED = "future_gated"


class HumanApprovalValidationKind(StrEnum):
    OPERATOR_SOURCE_CHECK = "operator_source_check"
    MODEL_GENERATED_REJECTION_CHECK = "model_generated_rejection_check"
    REVIEW_METADATA_NOT_APPLY_CHECK = "review_metadata_not_apply_check"
    CANDIDATE_BINDING_CHECK = "candidate_binding_check"
    DIFF_BINDING_CHECK = "diff_binding_check"
    SCOPE_BINDING_CHECK = "scope_binding_check"
    TIMESTAMP_PRESENCE_CHECK = "timestamp_presence_check"
    AMBIGUITY_CHECK = "ambiguity_check"
    STALE_APPROVAL_CHECK = "stale_approval_check"
    NO_APPLY_PERMISSION_CHECK = "no_apply_permission_check"
    UNKNOWN = "unknown"


class ApplyEligibilityStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_ELIGIBLE = "not_eligible"
    ELIGIBLE_FOR_FUTURE_DRY_RUN = "eligible_for_future_dry_run"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class ApplyEligibilityDecisionKind(StrEnum):
    ELIGIBLE_FOR_FUTURE_DRY_RUN = "eligible_for_future_dry_run"
    BLOCK_MISSING_HUMAN_APPROVAL = "block_missing_human_approval"
    BLOCK_INVALID_HUMAN_APPROVAL = "block_invalid_human_approval"
    BLOCK_BLOCKED_RISK_REPORT = "block_blocked_risk_report"
    BLOCK_MISSING_DIFF = "block_missing_diff"
    BLOCK_SCOPE_MISMATCH = "block_scope_mismatch"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0361_VERSION not in version:
        raise ValueError("version must include v0.36.1")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.1")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True in v0.36.1")


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


def _operator_source(source_kind: HumanApprovalSourceKind | str) -> bool:
    return HumanApprovalSourceKind(source_kind) in {
        HumanApprovalSourceKind.OPERATOR_SUPPLIED_EXPLICIT_APPROVAL,
        HumanApprovalSourceKind.OPERATOR_SUPPLIED_REVIEW_RECORD,
        HumanApprovalSourceKind.OPERATOR_SUPPLIED_CLI_METADATA,
        HumanApprovalSourceKind.TEST_FIXTURE,
    }


@dataclass(frozen=True)
class ApplyCandidateFlagSet:
    flag_set_id: str
    version: str
    apply_candidate_layer_constructed: bool
    apply_candidate_envelope_available: bool
    human_approval_contract_available: bool
    human_approval_evidence_validation_available: bool
    apply_eligibility_decision_available: bool
    ready_for_v0362_dry_run_patch_apply_simulation: bool
    ready_for_v0363_sandbox_workspace_overlay_policy: bool
    ready_for_apply_candidate_envelope: bool
    ready_for_human_approval_contract: bool
    ready_for_human_approval_evidence_validation: bool
    ready_for_apply_eligibility_decision: bool
    ready_for_future_dry_run_apply_input: bool
    ready_for_execution: bool = False
    ready_for_dry_run_apply_simulation: bool = False
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
class ApplyCandidateSourceRef:
    source_ref_id: str
    source_kind: PatchApplyCandidateSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyCandidateSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class HumanApprovalEvidence:
    approval_evidence_id: str
    evidence_kind: HumanApprovalEvidenceKind | str
    source_kind: HumanApprovalSourceKind | str
    evidence_summary: str
    evidence_value_preview: str
    bound_candidate_id: str | None
    bound_diff_id: str | None
    bound_scope_id: str | None
    operator_supplied: bool
    model_generated: bool
    automated_placeholder: bool
    valid_for_apply_candidate: bool
    valid_for_patch_application: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("approval_evidence_id", "evidence_summary"):
            _require_non_blank(name, getattr(self, name))
        HumanApprovalEvidenceKind(self.evidence_kind)
        source_kind = HumanApprovalSourceKind(self.source_kind)
        if _bounded_preview(self.evidence_value_preview) != self.evidence_value_preview:
            raise ValueError("evidence_value_preview must be bounded and redacted")
        if source_kind in (HumanApprovalSourceKind.MODEL_GENERATED_APPROVAL, HumanApprovalSourceKind.AUTOMATED_PLACEHOLDER, HumanApprovalSourceKind.INFERRED_APPROVAL, HumanApprovalSourceKind.MISSING_APPROVAL, HumanApprovalSourceKind.HUMAN_REVIEW_PACKET_METADATA):
            if self.valid_for_apply_candidate:
                raise ValueError("invalid approval sources cannot validate apply candidate")
        if self.model_generated or self.automated_placeholder:
            if self.valid_for_apply_candidate:
                raise ValueError("model-generated or automated placeholder approval cannot validate")
        if self.valid_for_apply_candidate and (not self.operator_supplied or not _operator_source(source_kind)):
            raise ValueError("valid_for_apply_candidate requires operator supplied evidence")
        _validate_false(self, ("valid_for_patch_application",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class HumanApprovalContract:
    approval_contract_id: str
    version: str
    approval_status: HumanApprovalStatus | str
    approval_source_kind: HumanApprovalSourceKind | str
    approval_evidence_items: list[HumanApprovalEvidence]
    required_evidence_kinds: list[HumanApprovalEvidenceKind | str]
    candidate_binding_required: bool
    diff_binding_required: bool
    scope_binding_required: bool
    operator_supplied_approval_required: bool
    model_generated_approval_valid: bool
    review_metadata_counts_as_apply_approval: bool
    approval_valid_for_future_dry_run: bool
    approval_valid_for_patch_application: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("approval_contract_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        HumanApprovalStatus(self.approval_status)
        HumanApprovalSourceKind(self.approval_source_kind)
        _validate_list("approval_evidence_items", self.approval_evidence_items)
        _validate_enum_list("required_evidence_kinds", self.required_evidence_kinds, HumanApprovalEvidenceKind)
        if self.operator_supplied_approval_required is not True:
            raise ValueError("operator supplied approval should be required")
        _validate_false(self, ("model_generated_approval_valid", "review_metadata_counts_as_apply_approval", "approval_valid_for_patch_application"))
        if self.approval_valid_for_future_dry_run:
            if HumanApprovalStatus(self.approval_status) not in (HumanApprovalStatus.VALIDATED, HumanApprovalStatus.VALIDATED_WITH_WARNINGS):
                raise ValueError("future dry-run approval requires validated status")
            if not any(item.valid_for_apply_candidate for item in self.approval_evidence_items):
                raise ValueError("future dry-run approval requires operator evidence")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidatePolicy:
    apply_candidate_policy_id: str
    version: str
    require_review_packet: bool
    require_risk_report: bool
    require_diff_proposal: bool
    require_human_approval_contract: bool
    require_operator_supplied_approval: bool
    reject_model_generated_approval: bool
    reject_review_metadata_as_apply_approval: bool
    reject_automated_placeholder_approval: bool
    allow_future_dry_run_input: bool
    allow_dry_run_apply_simulation: bool = False
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
    allow_infinite_agent_loop: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("apply_candidate_policy_id", self.apply_candidate_policy_id)
        _validate_version(self.version)
        _validate_true(self, ("require_human_approval_contract", "require_operator_supplied_approval", "reject_model_generated_approval", "reject_review_metadata_as_apply_approval", "reject_automated_placeholder_approval"))
        _validate_false(self, ("allow_dry_run_apply_simulation", "allow_sandbox_patch_apply", "allow_sandbox_workspace_write", "allow_live_workspace_write", "allow_patch_application", "allow_workspace_write", "allow_code_edit", "allow_apply_patch", "allow_git_apply", "allow_test_execution", "allow_shell", "allow_dependency_install", "allow_external_agent_execution", "allow_dominion_runtime", "allow_infinite_agent_loop"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidateEnvelope:
    apply_candidate_id: str
    version: str
    candidate_kind: PatchApplyCandidateKind | str
    status: PatchApplyCandidateStatus | str
    readiness_level: PatchApplyCandidateReadinessLevel | str
    review_packet_id: str | None
    risk_report_id: str | None
    diff_envelope_id: str | None
    structured_patch_id: str | None
    unified_diff_id: str | None
    patch_plan_id: str | None
    scope_policy_id: str | None
    approval_contract: HumanApprovalContract
    source_refs: list[ApplyCandidateSourceRef]
    risk_kinds: list[PatchApplyCandidateRiskKind | str]
    summary: str
    gaps: list[str]
    eligible_for_future_dry_run: bool
    ready_for_dry_run_apply_simulation: bool = False
    ready_for_sandbox_patch_apply: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("apply_candidate_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchApplyCandidateKind(self.candidate_kind)
        PatchApplyCandidateStatus(self.status)
        PatchApplyCandidateReadinessLevel(self.readiness_level)
        _validate_list("source_refs", self.source_refs)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchApplyCandidateRiskKind)
        _validate_string_list("gaps", self.gaps)
        if self.eligible_for_future_dry_run:
            if not self.approval_contract.approval_valid_for_future_dry_run:
                raise ValueError("eligible_for_future_dry_run requires valid approval contract")
            if not self.diff_envelope_id:
                raise ValueError("eligible_for_future_dry_run requires diff_envelope_id")
            if PatchApplyCandidateRiskKind.BLOCKED_RISK_REPORT_RISK in [PatchApplyCandidateRiskKind(item) for item in self.risk_kinds]:
                raise ValueError("blocked risk report prevents eligibility")
        _validate_false(self, ("ready_for_dry_run_apply_simulation", "ready_for_sandbox_patch_apply", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidateValidationFinding:
    finding_id: str
    risk_kind: PatchApplyCandidateRiskKind | str
    decision_kind: PatchApplyCandidateDecisionKind | str
    summary: str
    blocks_future_dry_run: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        PatchApplyCandidateRiskKind(self.risk_kind)
        PatchApplyCandidateDecisionKind(self.decision_kind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidateValidationReport:
    validation_report_id: str
    candidate_id: str
    findings: list[ApplyCandidateValidationFinding]
    status: PatchApplyCandidateStatus | str
    summary: str
    certifies_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "candidate_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("findings", self.findings)
        PatchApplyCandidateStatus(self.status)
        _validate_false(self, ("certifies_patch_application",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class HumanApprovalValidationFinding:
    finding_id: str
    validation_kind: HumanApprovalValidationKind | str
    approval_status: HumanApprovalStatus | str
    summary: str
    blocks_future_dry_run: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        HumanApprovalValidationKind(self.validation_kind)
        HumanApprovalStatus(self.approval_status)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class HumanApprovalValidationReport:
    validation_report_id: str
    approval_contract_id: str
    findings: list[HumanApprovalValidationFinding]
    approval_status: HumanApprovalStatus | str
    summary: str
    approval_valid_for_future_dry_run: bool
    approval_valid_for_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "approval_contract_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("findings", self.findings)
        HumanApprovalStatus(self.approval_status)
        if self.approval_valid_for_future_dry_run and any(item.blocks_future_dry_run for item in self.findings):
            raise ValueError("blocking findings prevent future dry-run approval")
        _validate_false(self, ("approval_valid_for_patch_application",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyEligibilityDecision:
    eligibility_decision_id: str
    candidate_id: str
    eligibility_status: ApplyEligibilityStatus | str
    decision_kind: ApplyEligibilityDecisionKind | str
    reason: str
    eligible_for_future_dry_run: bool
    ready_for_apply: bool = False
    ready_for_dry_run_apply_simulation: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    risk_kinds: list[PatchApplyCandidateRiskKind | str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("eligibility_decision_id", "candidate_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        ApplyEligibilityStatus(self.eligibility_status)
        ApplyEligibilityDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchApplyCandidateRiskKind)
        _validate_false(self, ("ready_for_apply", "ready_for_dry_run_apply_simulation", "ready_for_patch_application", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidateReport:
    report_id: str
    candidate_id: str
    validation_report: ApplyCandidateValidationReport
    human_approval_report: HumanApprovalValidationReport
    eligibility_decision: ApplyEligibilityDecision
    summary: str
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "candidate_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidateRunPreview:
    run_preview_id: str
    candidate_id: str
    preview_summary: str
    ready_for_future_dry_run_input: bool
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "candidate_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ApplyCandidateNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_dry_run_apply_simulation: bool
    no_sandbox_workspace_creation: bool
    no_sandbox_patch_apply: bool
    no_sandbox_write: bool
    no_live_workspace_write: bool
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
class V0361ReadinessReport:
    report_id: str
    version: str
    release_name: str
    summary: str
    ready_for_v0362_dry_run_patch_apply_simulation: bool
    ready_for_v0363_sandbox_workspace_overlay_policy: bool
    ready_for_apply_candidate_envelope: bool
    ready_for_human_approval_contract: bool
    ready_for_human_approval_evidence_validation: bool
    ready_for_apply_eligibility_decision: bool
    ready_for_future_dry_run_apply_input: bool
    ready_for_execution: bool = False
    ready_for_dry_run_apply_simulation: bool = False
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


def build_apply_candidate_flags(flag_set_id: str = "apply_candidate_flags:v0.36.1", **kwargs: Any) -> ApplyCandidateFlagSet:
    return ApplyCandidateFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0361_VERSION),
        apply_candidate_layer_constructed=kwargs.pop("apply_candidate_layer_constructed", True),
        apply_candidate_envelope_available=kwargs.pop("apply_candidate_envelope_available", True),
        human_approval_contract_available=kwargs.pop("human_approval_contract_available", True),
        human_approval_evidence_validation_available=kwargs.pop("human_approval_evidence_validation_available", True),
        apply_eligibility_decision_available=kwargs.pop("apply_eligibility_decision_available", True),
        ready_for_v0362_dry_run_patch_apply_simulation=kwargs.pop("ready_for_v0362_dry_run_patch_apply_simulation", True),
        ready_for_v0363_sandbox_workspace_overlay_policy=kwargs.pop("ready_for_v0363_sandbox_workspace_overlay_policy", True),
        ready_for_apply_candidate_envelope=kwargs.pop("ready_for_apply_candidate_envelope", True),
        ready_for_human_approval_contract=kwargs.pop("ready_for_human_approval_contract", True),
        ready_for_human_approval_evidence_validation=kwargs.pop("ready_for_human_approval_evidence_validation", True),
        ready_for_apply_eligibility_decision=kwargs.pop("ready_for_apply_eligibility_decision", True),
        ready_for_future_dry_run_apply_input=kwargs.pop("ready_for_future_dry_run_apply_input", True),
        **kwargs,
    )


def build_apply_candidate_source_ref(source_ref_id: str = "apply_candidate_source:v0.36.1", **kwargs: Any) -> ApplyCandidateSourceRef:
    return ApplyCandidateSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchApplyCandidateSourceKind.V0356_PATCH_REVIEW_PACKET),
        source_id=kwargs.pop("source_id", "review_packet:test"),
        source_summary=kwargs.pop("source_summary", "supplied review/risk/diff metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.35.6", "v0.35.5", "v0.35.4"]),
        **kwargs,
    )


def build_human_approval_evidence(approval_evidence_id: str = "human_approval_evidence:v0.36.1", **kwargs: Any) -> HumanApprovalEvidence:
    preview = _bounded_preview(kwargs.pop("evidence_value_preview", "operator approved candidate for future dry-run"))
    source_kind = kwargs.pop("source_kind", HumanApprovalSourceKind.OPERATOR_SUPPLIED_EXPLICIT_APPROVAL)
    return HumanApprovalEvidence(
        approval_evidence_id=approval_evidence_id,
        evidence_kind=kwargs.pop("evidence_kind", HumanApprovalEvidenceKind.EXPLICIT_OPERATOR_CONFIRMATION),
        source_kind=source_kind,
        evidence_summary=kwargs.pop("evidence_summary", "operator supplied approval evidence"),
        evidence_value_preview=preview,
        bound_candidate_id=kwargs.pop("bound_candidate_id", "apply_candidate:v0.36.1"),
        bound_diff_id=kwargs.pop("bound_diff_id", "diff_envelope:test"),
        bound_scope_id=kwargs.pop("bound_scope_id", "scope_policy:test"),
        operator_supplied=kwargs.pop("operator_supplied", _operator_source(source_kind)),
        model_generated=kwargs.pop("model_generated", source_kind == HumanApprovalSourceKind.MODEL_GENERATED_APPROVAL),
        automated_placeholder=kwargs.pop("automated_placeholder", source_kind == HumanApprovalSourceKind.AUTOMATED_PLACEHOLDER),
        valid_for_apply_candidate=kwargs.pop("valid_for_apply_candidate", _operator_source(source_kind)),
        valid_for_patch_application=kwargs.pop("valid_for_patch_application", False),
        **kwargs,
    )


def build_human_approval_contract(approval_contract_id: str = "human_approval_contract:v0.36.1", approval_evidence_items: list[HumanApprovalEvidence] | None = None, **kwargs: Any) -> HumanApprovalContract:
    evidence_items = approval_evidence_items if approval_evidence_items is not None else kwargs.pop("approval_evidence_items", [build_human_approval_evidence()])
    valid_for_future = kwargs.pop("approval_valid_for_future_dry_run", any(item.valid_for_apply_candidate for item in evidence_items))
    return HumanApprovalContract(
        approval_contract_id=approval_contract_id,
        version=kwargs.pop("version", V0361_VERSION),
        approval_status=kwargs.pop("approval_status", HumanApprovalStatus.VALIDATED if valid_for_future else HumanApprovalStatus.NOT_SUPPLIED),
        approval_source_kind=kwargs.pop("approval_source_kind", evidence_items[0].source_kind if evidence_items else HumanApprovalSourceKind.MISSING_APPROVAL),
        approval_evidence_items=evidence_items,
        required_evidence_kinds=kwargs.pop("required_evidence_kinds", [HumanApprovalEvidenceKind.EXPLICIT_OPERATOR_CONFIRMATION, HumanApprovalEvidenceKind.APPROVED_DIFF_REF, HumanApprovalEvidenceKind.APPROVED_SCOPE_REF]),
        candidate_binding_required=kwargs.pop("candidate_binding_required", True),
        diff_binding_required=kwargs.pop("diff_binding_required", True),
        scope_binding_required=kwargs.pop("scope_binding_required", True),
        operator_supplied_approval_required=kwargs.pop("operator_supplied_approval_required", True),
        model_generated_approval_valid=kwargs.pop("model_generated_approval_valid", False),
        review_metadata_counts_as_apply_approval=kwargs.pop("review_metadata_counts_as_apply_approval", False),
        approval_valid_for_future_dry_run=valid_for_future,
        approval_valid_for_patch_application=kwargs.pop("approval_valid_for_patch_application", False),
        summary=kwargs.pop("summary", "Human approval contract metadata only; not apply permission."),
        **kwargs,
    )


def default_apply_candidate_policy(**kwargs: Any) -> ApplyCandidatePolicy:
    return build_apply_candidate_policy(**kwargs)


def build_apply_candidate_policy(apply_candidate_policy_id: str = "apply_candidate_policy:v0.36.1", **kwargs: Any) -> ApplyCandidatePolicy:
    return ApplyCandidatePolicy(
        apply_candidate_policy_id=apply_candidate_policy_id,
        version=kwargs.pop("version", V0361_VERSION),
        require_review_packet=kwargs.pop("require_review_packet", True),
        require_risk_report=kwargs.pop("require_risk_report", True),
        require_diff_proposal=kwargs.pop("require_diff_proposal", True),
        require_human_approval_contract=kwargs.pop("require_human_approval_contract", True),
        require_operator_supplied_approval=kwargs.pop("require_operator_supplied_approval", True),
        reject_model_generated_approval=kwargs.pop("reject_model_generated_approval", True),
        reject_review_metadata_as_apply_approval=kwargs.pop("reject_review_metadata_as_apply_approval", True),
        reject_automated_placeholder_approval=kwargs.pop("reject_automated_placeholder_approval", True),
        allow_future_dry_run_input=kwargs.pop("allow_future_dry_run_input", True),
        **kwargs,
    )


def build_apply_candidate_envelope(apply_candidate_id: str = "apply_candidate:v0.36.1", approval_contract: HumanApprovalContract | None = None, **kwargs: Any) -> ApplyCandidateEnvelope:
    contract = approval_contract or kwargs.pop("approval_contract", build_human_approval_contract())
    eligible = kwargs.pop("eligible_for_future_dry_run", contract.approval_valid_for_future_dry_run)
    return ApplyCandidateEnvelope(
        apply_candidate_id=apply_candidate_id,
        version=kwargs.pop("version", V0361_VERSION),
        candidate_kind=kwargs.pop("candidate_kind", PatchApplyCandidateKind.FROM_RISK_ACCEPTED_REVIEW),
        status=kwargs.pop("status", PatchApplyCandidateStatus.ELIGIBLE_FOR_FUTURE_DRY_RUN if eligible else PatchApplyCandidateStatus.REVIEW_REQUIRED),
        readiness_level=kwargs.pop("readiness_level", PatchApplyCandidateReadinessLevel.ELIGIBILITY_DECISION_READY),
        review_packet_id=kwargs.pop("review_packet_id", "review_packet:test"),
        risk_report_id=kwargs.pop("risk_report_id", "risk_report:test"),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:test"),
        structured_patch_id=kwargs.pop("structured_patch_id", "structured_patch:test"),
        unified_diff_id=kwargs.pop("unified_diff_id", "unified_diff:test"),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:test"),
        scope_policy_id=kwargs.pop("scope_policy_id", "scope_policy:test"),
        approval_contract=contract,
        source_refs=kwargs.pop("source_refs", [build_apply_candidate_source_ref()]),
        risk_kinds=kwargs.pop("risk_kinds", []),
        summary=kwargs.pop("summary", "Apply candidate metadata eligible for future dry-run only."),
        gaps=kwargs.pop("gaps", []),
        eligible_for_future_dry_run=eligible,
        **kwargs,
    )


def build_apply_candidate_validation_finding(finding_id: str = "candidate_finding:v0.36.1", **kwargs: Any) -> ApplyCandidateValidationFinding:
    return ApplyCandidateValidationFinding(
        finding_id=finding_id,
        risk_kind=kwargs.pop("risk_kind", PatchApplyCandidateRiskKind.UNKNOWN),
        decision_kind=kwargs.pop("decision_kind", PatchApplyCandidateDecisionKind.ALLOW_CANDIDATE_METADATA),
        summary=kwargs.pop("summary", "candidate metadata check"),
        blocks_future_dry_run=kwargs.pop("blocks_future_dry_run", False),
        **kwargs,
    )


def build_apply_candidate_validation_report(validation_report_id: str = "candidate_validation_report:v0.36.1", **kwargs: Any) -> ApplyCandidateValidationReport:
    return ApplyCandidateValidationReport(
        validation_report_id=validation_report_id,
        candidate_id=kwargs.pop("candidate_id", "apply_candidate:v0.36.1"),
        findings=kwargs.pop("findings", []),
        status=kwargs.pop("status", PatchApplyCandidateStatus.CANDIDATE_VALIDATED),
        summary=kwargs.pop("summary", "Candidate validation report; does not certify patch application."),
        certifies_patch_application=kwargs.pop("certifies_patch_application", False),
        **kwargs,
    )


def build_human_approval_validation_finding(finding_id: str = "approval_finding:v0.36.1", **kwargs: Any) -> HumanApprovalValidationFinding:
    return HumanApprovalValidationFinding(
        finding_id=finding_id,
        validation_kind=kwargs.pop("validation_kind", HumanApprovalValidationKind.NO_APPLY_PERMISSION_CHECK),
        approval_status=kwargs.pop("approval_status", HumanApprovalStatus.VALIDATED),
        summary=kwargs.pop("summary", "approval metadata validation"),
        blocks_future_dry_run=kwargs.pop("blocks_future_dry_run", False),
        **kwargs,
    )


def build_human_approval_validation_report(validation_report_id: str = "approval_validation_report:v0.36.1", **kwargs: Any) -> HumanApprovalValidationReport:
    return HumanApprovalValidationReport(
        validation_report_id=validation_report_id,
        approval_contract_id=kwargs.pop("approval_contract_id", "human_approval_contract:v0.36.1"),
        findings=kwargs.pop("findings", []),
        approval_status=kwargs.pop("approval_status", HumanApprovalStatus.VALIDATED),
        summary=kwargs.pop("summary", "Human approval validation report; not apply permission."),
        approval_valid_for_future_dry_run=kwargs.pop("approval_valid_for_future_dry_run", True),
        approval_valid_for_patch_application=kwargs.pop("approval_valid_for_patch_application", False),
        **kwargs,
    )


def build_apply_eligibility_decision(eligibility_decision_id: str = "apply_eligibility_decision:v0.36.1", **kwargs: Any) -> ApplyEligibilityDecision:
    eligible = kwargs.pop("eligible_for_future_dry_run", True)
    return ApplyEligibilityDecision(
        eligibility_decision_id=eligibility_decision_id,
        candidate_id=kwargs.pop("candidate_id", "apply_candidate:v0.36.1"),
        eligibility_status=kwargs.pop("eligibility_status", ApplyEligibilityStatus.ELIGIBLE_FOR_FUTURE_DRY_RUN if eligible else ApplyEligibilityStatus.NOT_ELIGIBLE),
        decision_kind=kwargs.pop("decision_kind", ApplyEligibilityDecisionKind.ELIGIBLE_FOR_FUTURE_DRY_RUN if eligible else ApplyEligibilityDecisionKind.REQUIRE_REVIEW),
        reason=kwargs.pop("reason", "Eligible for future dry-run metadata only." if eligible else "Not eligible for future dry-run."),
        eligible_for_future_dry_run=eligible,
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_apply_candidate_report(report_id: str = "apply_candidate_report:v0.36.1", **kwargs: Any) -> ApplyCandidateReport:
    return ApplyCandidateReport(
        report_id=report_id,
        candidate_id=kwargs.pop("candidate_id", "apply_candidate:v0.36.1"),
        validation_report=kwargs.pop("validation_report", build_apply_candidate_validation_report()),
        human_approval_report=kwargs.pop("human_approval_report", build_human_approval_validation_report()),
        eligibility_decision=kwargs.pop("eligibility_decision", build_apply_eligibility_decision()),
        summary=kwargs.pop("summary", "Apply candidate report only; no dry-run/apply/write."),
        **kwargs,
    )


def build_apply_candidate_run_preview(run_preview_id: str = "apply_candidate_run_preview:v0.36.1", **kwargs: Any) -> ApplyCandidateRunPreview:
    return ApplyCandidateRunPreview(
        run_preview_id=run_preview_id,
        candidate_id=kwargs.pop("candidate_id", "apply_candidate:v0.36.1"),
        preview_summary=kwargs.pop("preview_summary", "Future dry-run input preview only."),
        ready_for_future_dry_run_input=kwargs.pop("ready_for_future_dry_run_input", True),
        **kwargs,
    )


def build_apply_candidate_no_apply_guarantee(guarantee_id: str = "apply_candidate_no_apply_guarantee:v0.36.1", **kwargs: Any) -> ApplyCandidateNoApplyGuarantee:
    return ApplyCandidateNoApplyGuarantee(
        guarantee_id=guarantee_id,
        version=kwargs.pop("version", V0361_VERSION),
        no_dry_run_apply_simulation=kwargs.pop("no_dry_run_apply_simulation", True),
        no_sandbox_workspace_creation=kwargs.pop("no_sandbox_workspace_creation", True),
        no_sandbox_patch_apply=kwargs.pop("no_sandbox_patch_apply", True),
        no_sandbox_write=kwargs.pop("no_sandbox_write", True),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
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
        summary=kwargs.pop("summary", "v0.36.1 introduces no apply/write/execution authority."),
        **kwargs,
    )


def build_v0361_readiness_report(report_id: str = "v0361_readiness_report", **kwargs: Any) -> V0361ReadinessReport:
    return V0361ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0361_VERSION),
        release_name=kwargs.pop("release_name", V0361_RELEASE_NAME),
        summary=kwargs.pop("summary", "Apply candidate and human approval contract metadata ready; execution remains false."),
        ready_for_v0362_dry_run_patch_apply_simulation=kwargs.pop("ready_for_v0362_dry_run_patch_apply_simulation", True),
        ready_for_v0363_sandbox_workspace_overlay_policy=kwargs.pop("ready_for_v0363_sandbox_workspace_overlay_policy", True),
        ready_for_apply_candidate_envelope=kwargs.pop("ready_for_apply_candidate_envelope", True),
        ready_for_human_approval_contract=kwargs.pop("ready_for_human_approval_contract", True),
        ready_for_human_approval_evidence_validation=kwargs.pop("ready_for_human_approval_evidence_validation", True),
        ready_for_apply_eligibility_decision=kwargs.pop("ready_for_apply_eligibility_decision", True),
        ready_for_future_dry_run_apply_input=kwargs.pop("ready_for_future_dry_run_apply_input", True),
        evidence_refs=kwargs.pop("evidence_refs", ["docs/versions/v0.36/v0.36.1_apply_candidate_human_approval_contract.md"]),
        **kwargs,
    )


def build_apply_candidate_from_review_packet_metadata(
    review_packet_id: str | None = "review_packet:test",
    risk_report_id: str | None = "risk_report:test",
    diff_envelope_id: str | None = "diff_envelope:test",
    blocked_risk_report: bool = False,
    approval_contract: HumanApprovalContract | None = None,
    **kwargs: Any,
) -> ApplyCandidateEnvelope:
    risks: list[PatchApplyCandidateRiskKind] = []
    if review_packet_id is None:
        risks.append(PatchApplyCandidateRiskKind.MISSING_REVIEW_PACKET_RISK)
    if risk_report_id is None:
        risks.append(PatchApplyCandidateRiskKind.MISSING_RISK_REPORT_RISK)
    if diff_envelope_id is None:
        risks.append(PatchApplyCandidateRiskKind.MISSING_DIFF_PROPOSAL_RISK)
    if blocked_risk_report:
        risks.append(PatchApplyCandidateRiskKind.BLOCKED_RISK_REPORT_RISK)
    contract = approval_contract or build_human_approval_contract()
    eligible = not risks and contract.approval_valid_for_future_dry_run
    return build_apply_candidate_envelope(
        review_packet_id=review_packet_id,
        risk_report_id=risk_report_id,
        diff_envelope_id=diff_envelope_id,
        approval_contract=contract,
        eligible_for_future_dry_run=eligible,
        status=PatchApplyCandidateStatus.ELIGIBLE_FOR_FUTURE_DRY_RUN if eligible else PatchApplyCandidateStatus.BLOCKED,
        risk_kinds=risks,
        gaps=[risk.value for risk in risks],
        **kwargs,
    )


def validate_human_approval_contract(contract: HumanApprovalContract) -> HumanApprovalValidationReport:
    findings: list[HumanApprovalValidationFinding] = []
    if contract.review_metadata_counts_as_apply_approval:
        findings.append(build_human_approval_validation_finding(validation_kind=HumanApprovalValidationKind.REVIEW_METADATA_NOT_APPLY_CHECK, approval_status=HumanApprovalStatus.INVALID, blocks_future_dry_run=True))
    if contract.model_generated_approval_valid:
        findings.append(build_human_approval_validation_finding(validation_kind=HumanApprovalValidationKind.MODEL_GENERATED_REJECTION_CHECK, approval_status=HumanApprovalStatus.INVALID, blocks_future_dry_run=True))
    if not contract.approval_valid_for_future_dry_run:
        findings.append(build_human_approval_validation_finding(validation_kind=HumanApprovalValidationKind.OPERATOR_SOURCE_CHECK, approval_status=HumanApprovalStatus.NOT_SUPPLIED, blocks_future_dry_run=True))
    return build_human_approval_validation_report(
        approval_contract_id=contract.approval_contract_id,
        findings=findings,
        approval_status=HumanApprovalStatus.VALIDATED if not findings else HumanApprovalStatus.INVALID,
        approval_valid_for_future_dry_run=not findings,
    )


def validate_apply_candidate_envelope(envelope: ApplyCandidateEnvelope) -> ApplyCandidateValidationReport:
    findings = [
        build_apply_candidate_validation_finding(risk_kind=risk, decision_kind=PatchApplyCandidateDecisionKind.REQUIRE_REVIEW, summary=f"{risk} present", blocks_future_dry_run=True)
        for risk in envelope.risk_kinds
    ]
    return build_apply_candidate_validation_report(
        candidate_id=envelope.apply_candidate_id,
        findings=findings,
        status=PatchApplyCandidateStatus.CANDIDATE_VALIDATED if not findings else PatchApplyCandidateStatus.CANDIDATE_VALIDATED_WITH_GAPS,
    )


def decide_apply_candidate_eligibility(envelope: ApplyCandidateEnvelope) -> ApplyEligibilityDecision:
    if not envelope.approval_contract.approval_valid_for_future_dry_run:
        return build_apply_eligibility_decision(candidate_id=envelope.apply_candidate_id, eligible_for_future_dry_run=False, eligibility_status=ApplyEligibilityStatus.BLOCKED, decision_kind=ApplyEligibilityDecisionKind.BLOCK_INVALID_HUMAN_APPROVAL, reason="Human approval is missing or invalid.")
    risks = [PatchApplyCandidateRiskKind(item) for item in envelope.risk_kinds]
    if PatchApplyCandidateRiskKind.BLOCKED_RISK_REPORT_RISK in risks:
        return build_apply_eligibility_decision(candidate_id=envelope.apply_candidate_id, eligible_for_future_dry_run=False, eligibility_status=ApplyEligibilityStatus.BLOCKED, decision_kind=ApplyEligibilityDecisionKind.BLOCK_BLOCKED_RISK_REPORT, reason="Risk report blocks future dry-run.")
    if not envelope.diff_envelope_id:
        return build_apply_eligibility_decision(candidate_id=envelope.apply_candidate_id, eligible_for_future_dry_run=False, eligibility_status=ApplyEligibilityStatus.BLOCKED, decision_kind=ApplyEligibilityDecisionKind.BLOCK_MISSING_DIFF, reason="Diff proposal is missing.")
    return build_apply_eligibility_decision(candidate_id=envelope.apply_candidate_id, eligible_for_future_dry_run=True)


def apply_candidate_flags_preserve_no_apply(flags: ApplyCandidateFlagSet) -> bool:
    return isinstance(flags, ApplyCandidateFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def human_approval_contract_rejects_model_approval(contract: HumanApprovalContract) -> bool:
    return contract.model_generated_approval_valid is False and contract.review_metadata_counts_as_apply_approval is False and contract.approval_valid_for_patch_application is False


def human_approval_evidence_is_not_apply_permission(evidence: HumanApprovalEvidence) -> bool:
    return evidence.valid_for_patch_application is False


def apply_candidate_policy_blocks_apply(policy: ApplyCandidatePolicy) -> bool:
    return not any(getattr(policy, name) for name in ("allow_dry_run_apply_simulation", "allow_sandbox_patch_apply", "allow_sandbox_workspace_write", "allow_live_workspace_write", "allow_patch_application", "allow_workspace_write", "allow_code_edit", "allow_apply_patch", "allow_git_apply", "allow_test_execution", "allow_shell", "allow_dependency_install", "allow_external_agent_execution", "allow_dominion_runtime", "allow_infinite_agent_loop"))


def apply_candidate_envelope_is_not_apply(envelope: ApplyCandidateEnvelope) -> bool:
    return not any(getattr(envelope, name) for name in ("ready_for_dry_run_apply_simulation", "ready_for_sandbox_patch_apply", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))


def apply_eligibility_decision_is_not_apply_permission(decision: ApplyEligibilityDecision) -> bool:
    return not any(getattr(decision, name) for name in ("ready_for_apply", "ready_for_dry_run_apply_simulation", "ready_for_patch_application", "ready_for_execution"))


def v0361_readiness_report_is_not_execution_ready(report: V0361ReadinessReport) -> bool:
    return isinstance(report, V0361ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
