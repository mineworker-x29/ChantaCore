from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_diff_proposal import DiffProposalEnvelope
from .patch_risk import PatchProposalRiskReport, PatchRiskDecisionKind, PatchRiskScanDecision


V0356_VERSION = "v0.35.6"
V0356_RELEASE_NAME = "v0.35.6 Human Review Packet & Approval Gate Metadata"
DEFAULT_V0356_DOC_PATH = "docs/versions/v0.35/v0.35.6_human_review_packet_approval_gate_metadata.md"
DEFAULT_V0355_RISK_DOC_REF = "docs/versions/v0.35/v0.35.5_patch_risk_conformance_scanner.md"
DEFAULT_V0354_DIFF_DOC_REF = "docs/versions/v0.35/v0.35.4_diff_proposal_envelope.md"
DEFAULT_V0353_PLAN_DOC_REF = "docs/versions/v0.35/v0.35.3_reference_informed_patch_plan_change_set_graph.md"
DEFAULT_V0352_CONTEXT_DOC_REF = "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"
DEFAULT_MAX_REVIEW_PREVIEW_CHARS = 1200

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

UNSAFE_PATCH_REVIEW_FLAG_NAMES = (
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


class PatchReviewPacketMode(StrEnum):
    RISK_REPORT_ONLY = "risk_report_only"
    DIFF_AND_RISK_REVIEW = "diff_and_risk_review"
    FULL_PATCH_PROPOSAL_REVIEW = "full_patch_proposal_review"
    METADATA_ONLY_REVIEW = "metadata_only_review"
    BLOCKED = "blocked"
    NEEDS_REVISION = "needs_revision"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchReviewSourceKind(StrEnum):
    V0355_PATCH_PROPOSAL_RISK_REPORT = "v0355_patch_proposal_risk_report"
    V0355_PATCH_RISK_SCAN_DECISION = "v0355_patch_risk_scan_decision"
    V0354_DIFF_PROPOSAL_ENVELOPE = "v0354_diff_proposal_envelope"
    V0354_UNIFIED_DIFF_PROPOSAL = "v0354_unified_diff_proposal"
    V0354_STRUCTURED_PATCH_PROPOSAL = "v0354_structured_patch_proposal"
    V0353_PATCH_PLAN = "v0353_patch_plan"
    V0352_CONTEXT_SNAPSHOT = "v0352_context_snapshot"
    V0351_PATCH_INTENT_SCOPE_BUNDLE = "v0351_patch_intent_scope_bundle"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    REVIEWER_METADATA = "reviewer_metadata"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchReviewPacketStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    REVIEW_PACKET_CREATED = "review_packet_created"
    CHECKLIST_CREATED = "checklist_created"
    APPROVAL_GATE_METADATA_CREATED = "approval_gate_metadata_created"
    PENDING_HUMAN_REVIEW = "pending_human_review"
    APPROVED_FOR_REVIEW = "approved_for_review"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    BLOCKED = "blocked"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class PatchReviewReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    REVIEW_CONTRACT_READY = "review_contract_ready"
    REVIEW_PACKET_READY = "review_packet_ready"
    CHECKLIST_READY = "checklist_ready"
    APPROVAL_GATE_METADATA_READY = "approval_gate_metadata_ready"
    DESIGN_HANDOFF_READY_FOR_V0357 = "design_handoff_ready_for_v0357"
    DESIGN_HANDOFF_READY_FOR_V0358 = "design_handoff_ready_for_v0358"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchReviewDecisionKind(StrEnum):
    READY_FOR_HUMAN_REVIEW = "ready_for_human_review"
    APPROVED_FOR_REVIEW = "approved_for_review"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    BLOCKED_BY_RISK = "blocked_by_risk"
    BLOCKED_BY_SCOPE = "blocked_by_scope"
    BLOCKED_BY_MISSING_ARTIFACT = "blocked_by_missing_artifact"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchReviewRiskKind(StrEnum):
    MISSING_RISK_REPORT = "missing_risk_report"
    BLOCKING_RISK_PRESENT = "blocking_risk_present"
    UNRESOLVED_REVIEW_ITEM = "unresolved_review_item"
    MISSING_DIFF_PROPOSAL = "missing_diff_proposal"
    MISSING_PATCH_PLAN = "missing_patch_plan"
    MISSING_CONTEXT_SNAPSHOT = "missing_context_snapshot"
    SCOPE_VIOLATION_PRESENT = "scope_violation_present"
    SAFETY_REGRESSION_PRESENT = "safety_regression_present"
    SECRET_OR_CREDENTIAL_RISK = "secret_or_credential_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class PatchReviewChecklistItemKind(StrEnum):
    VERIFY_SCOPE_ALIGNMENT = "verify_scope_alignment"
    VERIFY_INTENT_ALIGNMENT = "verify_intent_alignment"
    VERIFY_CONTEXT_EVIDENCE = "verify_context_evidence"
    VERIFY_DIFF_SHAPE = "verify_diff_shape"
    VERIFY_RISK_REPORT = "verify_risk_report"
    VERIFY_NO_SECRET_EXPOSURE = "verify_no_secret_exposure"
    VERIFY_NO_PROVIDER_NETWORK_OPENING = "verify_no_provider_network_opening"
    VERIFY_NO_SHELL_COMMAND = "verify_no_shell_command"
    VERIFY_NO_WRITE_APPLY_RUNTIME = "verify_no_write_apply_runtime"
    VERIFY_NO_REFERENCE_EXECUTION = "verify_no_reference_execution"
    VERIFY_TESTS_PLANNED_BUT_NOT_RUN = "verify_tests_planned_but_not_run"
    VERIFY_DOCS_PLANNED_BUT_NOT_WRITTEN = "verify_docs_planned_but_not_written"
    VERIFY_HUMAN_DECISION_NEEDED = "verify_human_decision_needed"
    VERIFY_FUTURE_APPLY_SANDBOX_REQUIRED = "verify_future_apply_sandbox_required"
    UNKNOWN = "unknown"


class PatchReviewOutcomeKind(StrEnum):
    PENDING = "pending"
    ACCEPTABLE_FOR_HUMAN_REVIEW = "acceptable_for_human_review"
    APPROVED_FOR_REVIEW = "approved_for_review"
    REJECTED = "rejected"
    NEEDS_REVISION = "needs_revision"
    BLOCKED = "blocked"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchApprovalGateKind(StrEnum):
    NO_APPLY_GATE = "no_apply_gate"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    APPROVAL_METADATA_ONLY = "approval_metadata_only"
    FUTURE_HUMAN_APPROVED_APPLY_SANDBOX = "future_human_approved_apply_sandbox"
    BLOCKED_GATE = "blocked_gate"
    NO_OP_GATE = "no_op_gate"
    UNKNOWN = "unknown"


class PatchReviewerRoleKind(StrEnum):
    HUMAN_REVIEWER = "human_reviewer"
    OWNER = "owner"
    MAINTAINER = "maintainer"
    SAFETY_REVIEWER = "safety_reviewer"
    DOMAIN_REVIEWER = "domain_reviewer"
    AUTOMATED_PLACEHOLDER = "automated_placeholder"
    UNKNOWN = "unknown"


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0356_VERSION not in value:
        raise ValueError("version must include v0.35.6")


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


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.6")


def _bounded(value: str, limit: int = DEFAULT_MAX_REVIEW_PREVIEW_CHARS, marker: str = "\n[truncated by v0.35.6 review boundary]") -> tuple[str, bool]:
    if limit < 0:
        raise ValueError("limit must be >= 0")
    if len(value) <= limit:
        return value, False
    if limit <= len(marker):
        return value[:limit], True
    return value[: limit - len(marker)] + marker, True


@dataclass(frozen=True)
class PatchReviewFlagSet:
    flag_set_id: str
    version: str
    patch_review_layer_constructed: bool
    human_review_packet_available: bool
    review_checklist_available: bool
    approval_gate_metadata_available: bool
    reviewer_decision_placeholder_available: bool
    ready_for_v0357_patch_proposal_ocel_trace_packet: bool
    ready_for_v0358_cli_patch_proposal_surface: bool
    ready_for_human_review_packet: bool
    ready_for_review_checklist: bool
    ready_for_approval_gate_metadata: bool
    ready_for_reviewer_decision_placeholder: bool
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
        _validate_false(self, UNSAFE_PATCH_REVIEW_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewSourceRef:
    source_ref_id: str
    source_kind: PatchReviewSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PatchReviewSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewPolicy:
    review_policy_id: str
    version: str
    allowed_modes: list[PatchReviewPacketMode | str]
    blocked_modes: list[PatchReviewPacketMode | str]
    required_checklist_items: list[PatchReviewChecklistItemKind | str]
    blocked_risk_kinds: list[PatchReviewRiskKind | str]
    require_risk_report: bool
    require_diff_proposal: bool
    require_patch_plan: bool
    require_context_snapshot: bool
    require_no_blocking_risks: bool
    require_human_review: bool
    allow_approved_for_review: bool
    allow_approved_for_apply: bool = False
    allow_patch_application: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_policy_id", self.review_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, PatchReviewPacketMode)
        _validate_enum_list("blocked_modes", self.blocked_modes, PatchReviewPacketMode)
        _validate_enum_list("required_checklist_items", self.required_checklist_items, PatchReviewChecklistItemKind)
        _validate_enum_list("blocked_risk_kinds", self.blocked_risk_kinds, PatchReviewRiskKind)
        for name in ("allow_approved_for_apply", "allow_patch_application", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_shell", "allow_dependency_install"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.6")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewInput:
    review_input_id: str
    version: str
    proposal_risk_report_id: str | None
    risk_scan_decision_id: str | None
    diff_envelope_id: str | None
    unified_diff_id: str | None
    structured_patch_id: str | None
    patch_plan_id: str | None
    context_snapshot_id: str | None
    intent_scope_bundle_id: str | None
    requested_mode: PatchReviewPacketMode | str
    task_summary: str
    source_refs: list[PatchReviewSourceRef]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_input_id", self.review_input_id)
        _validate_version(self.version)
        for name in ("proposal_risk_report_id", "risk_scan_decision_id", "diff_envelope_id", "unified_diff_id", "structured_patch_id", "patch_plan_id", "context_snapshot_id", "intent_scope_bundle_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        PatchReviewPacketMode(self.requested_mode)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"patch_application", "workspace_write", "code_edit", "shell_execution", "test_execution", "dependency_install", "reference_execution", "provider_invocation", "direct_network_access", "credential_access"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include unsafe runtime actions")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewChecklistItem:
    checklist_item_id: str
    item_kind: PatchReviewChecklistItemKind | str
    item_summary: str
    evidence_ref: str | None
    required: bool
    satisfied: bool
    blocked: bool
    requires_human_attention: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("checklist_item_id", self.checklist_item_id)
        PatchReviewChecklistItemKind(self.item_kind)
        _require_non_blank("item_summary", self.item_summary)
        if self.evidence_ref is not None:
            _require_non_blank("evidence_ref", self.evidence_ref)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewChecklist:
    checklist_id: str
    version: str
    checklist_items: list[PatchReviewChecklistItem]
    required_item_count: int
    satisfied_item_count: int
    blocked_item_count: int
    human_attention_count: int
    summary: str
    ready_for_human_review: bool
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("checklist_id", self.checklist_id)
        _validate_version(self.version)
        _validate_list("checklist_items", self.checklist_items)
        for name in ("required_item_count", "satisfied_item_count", "blocked_item_count", "human_attention_count"):
            _validate_non_negative(name, getattr(self, name))
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewArtifactSummary:
    artifact_summary_id: str
    artifact_kind: str
    artifact_id: str | None
    artifact_summary: str
    bounded_preview: str
    redacted: bool
    truncated: bool
    risk_kinds: list[PatchReviewRiskKind | str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("artifact_summary_id", self.artifact_summary_id)
        _require_non_blank("artifact_kind", self.artifact_kind)
        if self.artifact_id is not None:
            _require_non_blank("artifact_id", self.artifact_id)
        _require_non_blank("artifact_summary", self.artifact_summary)
        if len(self.bounded_preview) > DEFAULT_MAX_REVIEW_PREVIEW_CHARS:
            raise ValueError("bounded_preview must be bounded")
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchReviewRiskKind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewRiskSummary:
    review_risk_summary_id: str
    proposal_risk_report_id: str | None
    risk_summary: str
    blocking_risk_count: int
    review_required_count: int
    acceptable_for_review: bool
    approved_for_apply: bool
    risk_kinds: list[PatchReviewRiskKind | str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_risk_summary_id", self.review_risk_summary_id)
        if self.proposal_risk_report_id is not None:
            _require_non_blank("proposal_risk_report_id", self.proposal_risk_report_id)
        _require_non_blank("risk_summary", self.risk_summary)
        _validate_non_negative("blocking_risk_count", self.blocking_risk_count)
        _validate_non_negative("review_required_count", self.review_required_count)
        if self.approved_for_apply is not False:
            raise ValueError("approved_for_apply must always be False")
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchReviewRiskKind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchApprovalGateMetadata:
    approval_gate_id: str
    version: str
    gate_kind: PatchApprovalGateKind | str
    gate_summary: str
    requires_human_reviewer: bool
    allows_review_approval_metadata: bool
    allows_apply_permission: bool = False
    allows_workspace_write: bool = False
    allows_code_edit: bool = False
    applies_patch: bool = False
    future_apply_sandbox_required: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("approval_gate_id", self.approval_gate_id)
        _validate_version(self.version)
        PatchApprovalGateKind(self.gate_kind)
        _require_non_blank("gate_summary", self.gate_summary)
        _validate_false(self, ("allows_apply_permission", "allows_workspace_write", "allows_code_edit", "applies_patch"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewerDecisionPlaceholder:
    reviewer_decision_placeholder_id: str
    reviewer_role: PatchReviewerRoleKind | str
    expected_decision_kind: PatchReviewDecisionKind | str
    placeholder_summary: str
    required: bool
    filled: bool
    decision_record_id: str | None
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("reviewer_decision_placeholder_id", self.reviewer_decision_placeholder_id)
        PatchReviewerRoleKind(self.reviewer_role)
        PatchReviewDecisionKind(self.expected_decision_kind)
        _require_non_blank("placeholder_summary", self.placeholder_summary)
        if self.decision_record_id is not None:
            _require_non_blank("decision_record_id", self.decision_record_id)
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewDecisionRecord:
    review_decision_record_id: str
    reviewer_role: PatchReviewerRoleKind | str
    decision_kind: PatchReviewDecisionKind | str
    outcome_kind: PatchReviewOutcomeKind | str
    decision_summary: str
    rationale: str
    approved_for_review: bool
    approved_for_apply: bool = False
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_decision_record_id", self.review_decision_record_id)
        PatchReviewerRoleKind(self.reviewer_role)
        PatchReviewDecisionKind(self.decision_kind)
        PatchReviewOutcomeKind(self.outcome_kind)
        _require_non_blank("decision_summary", self.decision_summary)
        _require_non_blank("rationale", self.rationale)
        if self.approved_for_apply is not False:
            raise ValueError("approved_for_apply must always be False")
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewPacket:
    review_packet_id: str
    version: str
    review_input_id: str
    mode: PatchReviewPacketMode | str
    status: PatchReviewPacketStatus | str
    readiness_level: PatchReviewReadinessLevel | str
    artifact_summaries: list[PatchReviewArtifactSummary]
    risk_summary: PatchReviewRiskSummary
    checklist: PatchReviewChecklist
    approval_gate_metadata: PatchApprovalGateMetadata
    reviewer_decision_placeholders: list[PatchReviewerDecisionPlaceholder]
    decision_records: list[PatchReviewDecisionRecord]
    source_refs: list[PatchReviewSourceRef]
    summary: str
    gaps: list[str]
    ready_for_v0357_patch_proposal_ocel_trace_packet: bool
    ready_for_v0358_cli_patch_proposal_surface: bool
    ready_for_human_review: bool
    approved_for_review: bool
    approved_for_apply: bool = False
    ready_for_apply: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("review_packet_id", "review_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchReviewPacketMode(self.mode)
        status = PatchReviewPacketStatus(self.status)
        PatchReviewReadinessLevel(self.readiness_level)
        for name in ("artifact_summaries", "reviewer_decision_placeholders", "decision_records", "source_refs"):
            _validate_list(name, getattr(self, name))
        _validate_string_list("gaps", self.gaps)
        if self.approved_for_apply is not False:
            raise ValueError("approved_for_apply must always be False")
        _validate_false(self, ("ready_for_apply", "ready_for_execution"))
        if status == PatchReviewPacketStatus.BLOCKED and self.approved_for_review:
            raise ValueError("blocked review packets cannot be approved_for_review")
        if self.risk_summary.blocking_risk_count > 0 and self.approved_for_review:
            raise ValueError("review packets with blocking risks cannot be approved_for_review")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewValidationFinding:
    finding_id: str
    decision_kind: PatchReviewDecisionKind | str
    risk_kinds: list[PatchReviewRiskKind | str]
    finding_summary: str
    evidence_preview: str
    blocks_validation: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        PatchReviewDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchReviewRiskKind)
        _require_non_blank("finding_summary", self.finding_summary)
        if len(self.evidence_preview) > DEFAULT_MAX_REVIEW_PREVIEW_CHARS:
            raise ValueError("evidence_preview must be bounded")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewValidationReport:
    validation_report_id: str
    version: str
    review_packet_id: str | None
    findings: list[PatchReviewValidationFinding]
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
        if self.review_packet_id is not None:
            _require_non_blank("review_packet_id", self.review_packet_id)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewReadinessReport:
    readiness_report_id: str
    version: str
    review_packet_id: str
    summary: str
    ready_for_human_review_packet: bool
    ready_for_review_checklist: bool
    ready_for_approval_gate_metadata: bool
    ready_for_reviewer_decision_placeholder: bool
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "review_packet_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewReport:
    review_report_id: str
    version: str
    review_packet_id: str
    summary: str
    review_packet_ready: bool
    checklist_ready: bool
    approval_gate_metadata_ready: bool
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("review_report_id", "review_packet_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, ("ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReviewRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_apply_permission_guarantee: bool = True
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
class PatchReviewNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_apply_permission: bool = True
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
class V0356ReadinessReport:
    report_id: str
    version: str
    review_packet_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0357_patch_proposal_ocel_trace_packet: bool = True
    ready_for_v0358_cli_patch_proposal_surface: bool = True
    ready_for_human_review_packet: bool = True
    ready_for_review_checklist: bool = True
    ready_for_approval_gate_metadata: bool = True
    ready_for_reviewer_decision_placeholder: bool = True
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
        if self.review_packet_id is not None:
            _require_non_blank("review_packet_id", self.review_packet_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_PATCH_REVIEW_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_patch_review_flags(flag_set_id: str = "patch_review_flags:v0.35.6", **kwargs: Any) -> PatchReviewFlagSet:
    return PatchReviewFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0356_VERSION),
        patch_review_layer_constructed=kwargs.pop("patch_review_layer_constructed", True),
        human_review_packet_available=kwargs.pop("human_review_packet_available", True),
        review_checklist_available=kwargs.pop("review_checklist_available", True),
        approval_gate_metadata_available=kwargs.pop("approval_gate_metadata_available", True),
        reviewer_decision_placeholder_available=kwargs.pop("reviewer_decision_placeholder_available", True),
        ready_for_v0357_patch_proposal_ocel_trace_packet=kwargs.pop("ready_for_v0357_patch_proposal_ocel_trace_packet", True),
        ready_for_v0358_cli_patch_proposal_surface=kwargs.pop("ready_for_v0358_cli_patch_proposal_surface", True),
        ready_for_human_review_packet=kwargs.pop("ready_for_human_review_packet", True),
        ready_for_review_checklist=kwargs.pop("ready_for_review_checklist", True),
        ready_for_approval_gate_metadata=kwargs.pop("ready_for_approval_gate_metadata", True),
        ready_for_reviewer_decision_placeholder=kwargs.pop("ready_for_reviewer_decision_placeholder", True),
        ready_for_patch_review_packet_input=kwargs.pop("ready_for_patch_review_packet_input", True),
        **kwargs,
    )


def build_patch_review_source_ref(source_ref_id: str = "patch_review_source:v0.35.6", **kwargs: Any) -> PatchReviewSourceRef:
    return PatchReviewSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchReviewSourceKind.V0355_PATCH_PROPOSAL_RISK_REPORT),
        source_id=kwargs.pop("source_id", "proposal_risk_report:v0.35.5"),
        source_summary=kwargs.pop("source_summary", "Supplied v0.35.5 patch proposal risk report metadata."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0355_RISK_DOC_REF]),
        **kwargs,
    )


def build_patch_review_policy(review_policy_id: str = "patch_review_policy:v0.35.6", **kwargs: Any) -> PatchReviewPolicy:
    return PatchReviewPolicy(
        review_policy_id=review_policy_id,
        version=kwargs.pop("version", V0356_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [PatchReviewPacketMode.RISK_REPORT_ONLY, PatchReviewPacketMode.DIFF_AND_RISK_REVIEW, PatchReviewPacketMode.FULL_PATCH_PROPOSAL_REVIEW, PatchReviewPacketMode.METADATA_ONLY_REVIEW]),
        blocked_modes=kwargs.pop("blocked_modes", [PatchReviewPacketMode.UNKNOWN]),
        required_checklist_items=kwargs.pop("required_checklist_items", [PatchReviewChecklistItemKind.VERIFY_RISK_REPORT, PatchReviewChecklistItemKind.VERIFY_NO_WRITE_APPLY_RUNTIME, PatchReviewChecklistItemKind.VERIFY_HUMAN_DECISION_NEEDED, PatchReviewChecklistItemKind.VERIFY_FUTURE_APPLY_SANDBOX_REQUIRED]),
        blocked_risk_kinds=kwargs.pop("blocked_risk_kinds", [PatchReviewRiskKind.BLOCKING_RISK_PRESENT, PatchReviewRiskKind.SCOPE_VIOLATION_PRESENT, PatchReviewRiskKind.SAFETY_REGRESSION_PRESENT, PatchReviewRiskKind.PATCH_APPLY_RISK, PatchReviewRiskKind.WORKSPACE_WRITE_RISK, PatchReviewRiskKind.AUTHORITY_GRANT_RISK]),
        require_risk_report=kwargs.pop("require_risk_report", True),
        require_diff_proposal=kwargs.pop("require_diff_proposal", True),
        require_patch_plan=kwargs.pop("require_patch_plan", True),
        require_context_snapshot=kwargs.pop("require_context_snapshot", True),
        require_no_blocking_risks=kwargs.pop("require_no_blocking_risks", True),
        require_human_review=kwargs.pop("require_human_review", True),
        allow_approved_for_review=kwargs.pop("allow_approved_for_review", True),
        **kwargs,
    )


def default_patch_review_policy() -> PatchReviewPolicy:
    return build_patch_review_policy()


def build_patch_review_input(review_input_id: str = "patch_review_input:v0.35.6", **kwargs: Any) -> PatchReviewInput:
    return PatchReviewInput(
        review_input_id=review_input_id,
        version=kwargs.pop("version", V0356_VERSION),
        proposal_risk_report_id=kwargs.pop("proposal_risk_report_id", "proposal_risk_report:v0.35.5"),
        risk_scan_decision_id=kwargs.pop("risk_scan_decision_id", "patch_risk_decision:v0.35.5"),
        diff_envelope_id=kwargs.pop("diff_envelope_id", "diff_envelope:v0.35.4"),
        unified_diff_id=kwargs.pop("unified_diff_id", "unified_diff:v0.35.4"),
        structured_patch_id=kwargs.pop("structured_patch_id", "structured_patch:v0.35.4"),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        intent_scope_bundle_id=kwargs.pop("intent_scope_bundle_id", "intent_scope_bundle:v0.35.1"),
        requested_mode=kwargs.pop("requested_mode", PatchReviewPacketMode.FULL_PATCH_PROPOSAL_REVIEW),
        task_summary=kwargs.pop("task_summary", "Create human review packet metadata from supplied risk and diff artifacts."),
        source_refs=kwargs.pop("source_refs", [build_patch_review_source_ref()]),
        **kwargs,
    )


def build_patch_review_checklist_item(checklist_item_id: str = "review_checklist_item:v0.35.6:risk", **kwargs: Any) -> PatchReviewChecklistItem:
    return PatchReviewChecklistItem(
        checklist_item_id=checklist_item_id,
        item_kind=kwargs.pop("item_kind", PatchReviewChecklistItemKind.VERIFY_RISK_REPORT),
        item_summary=kwargs.pop("item_summary", "Reviewer must verify risk report before any future apply sandbox."),
        evidence_ref=kwargs.pop("evidence_ref", DEFAULT_V0355_RISK_DOC_REF),
        required=kwargs.pop("required", True),
        satisfied=kwargs.pop("satisfied", False),
        blocked=kwargs.pop("blocked", False),
        requires_human_attention=kwargs.pop("requires_human_attention", True),
        **kwargs,
    )


def build_patch_review_checklist(checklist_id: str = "review_checklist:v0.35.6", **kwargs: Any) -> PatchReviewChecklist:
    items = kwargs.pop("checklist_items", [build_patch_review_checklist_item(), build_patch_review_checklist_item("review_checklist_item:v0.35.6:no_apply", item_kind=PatchReviewChecklistItemKind.VERIFY_NO_WRITE_APPLY_RUNTIME, item_summary="Reviewer must verify no write/apply runtime is present.")])
    return PatchReviewChecklist(
        checklist_id=checklist_id,
        version=kwargs.pop("version", V0356_VERSION),
        checklist_items=items,
        required_item_count=kwargs.pop("required_item_count", sum(1 for item in items if item.required)),
        satisfied_item_count=kwargs.pop("satisfied_item_count", sum(1 for item in items if item.satisfied)),
        blocked_item_count=kwargs.pop("blocked_item_count", sum(1 for item in items if item.blocked)),
        human_attention_count=kwargs.pop("human_attention_count", sum(1 for item in items if item.requires_human_attention)),
        summary=kwargs.pop("summary", "Checklist is human review metadata, not enforcement execution."),
        ready_for_human_review=kwargs.pop("ready_for_human_review", True),
        **kwargs,
    )


def build_patch_review_artifact_summary(artifact_summary_id: str = "review_artifact:v0.35.6:risk", **kwargs: Any) -> PatchReviewArtifactSummary:
    preview, truncated = _bounded(kwargs.pop("bounded_preview", "Review artifact summary preview."))
    return PatchReviewArtifactSummary(
        artifact_summary_id=artifact_summary_id,
        artifact_kind=kwargs.pop("artifact_kind", "PatchProposalRiskReport"),
        artifact_id=kwargs.pop("artifact_id", "proposal_risk_report:v0.35.5"),
        artifact_summary=kwargs.pop("artifact_summary", "Risk report is summarized as review input metadata."),
        bounded_preview=preview,
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", truncated),
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_patch_review_risk_summary(review_risk_summary_id: str = "review_risk_summary:v0.35.6", **kwargs: Any) -> PatchReviewRiskSummary:
    return PatchReviewRiskSummary(
        review_risk_summary_id=review_risk_summary_id,
        proposal_risk_report_id=kwargs.pop("proposal_risk_report_id", "proposal_risk_report:v0.35.5"),
        risk_summary=kwargs.pop("risk_summary", "Risk report permits human review metadata only."),
        blocking_risk_count=kwargs.pop("blocking_risk_count", 0),
        review_required_count=kwargs.pop("review_required_count", 0),
        acceptable_for_review=kwargs.pop("acceptable_for_review", True),
        approved_for_apply=kwargs.pop("approved_for_apply", False),
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_patch_approval_gate_metadata(approval_gate_id: str = "approval_gate:v0.35.6", **kwargs: Any) -> PatchApprovalGateMetadata:
    return PatchApprovalGateMetadata(
        approval_gate_id=approval_gate_id,
        version=kwargs.pop("version", V0356_VERSION),
        gate_kind=kwargs.pop("gate_kind", PatchApprovalGateKind.NO_APPLY_GATE),
        gate_summary=kwargs.pop("gate_summary", "Approval gate metadata does not grant apply permission."),
        requires_human_reviewer=kwargs.pop("requires_human_reviewer", True),
        allows_review_approval_metadata=kwargs.pop("allows_review_approval_metadata", True),
        future_apply_sandbox_required=kwargs.pop("future_apply_sandbox_required", True),
        **kwargs,
    )


def build_patch_reviewer_decision_placeholder(reviewer_decision_placeholder_id: str = "reviewer_placeholder:v0.35.6", **kwargs: Any) -> PatchReviewerDecisionPlaceholder:
    return PatchReviewerDecisionPlaceholder(
        reviewer_decision_placeholder_id=reviewer_decision_placeholder_id,
        reviewer_role=kwargs.pop("reviewer_role", PatchReviewerRoleKind.HUMAN_REVIEWER),
        expected_decision_kind=kwargs.pop("expected_decision_kind", PatchReviewDecisionKind.READY_FOR_HUMAN_REVIEW),
        placeholder_summary=kwargs.pop("placeholder_summary", "Human reviewer decision placeholder is metadata only."),
        required=kwargs.pop("required", True),
        filled=kwargs.pop("filled", False),
        decision_record_id=kwargs.pop("decision_record_id", None),
        **kwargs,
    )


def build_patch_review_decision_record(review_decision_record_id: str = "review_decision:v0.35.6", **kwargs: Any) -> PatchReviewDecisionRecord:
    return PatchReviewDecisionRecord(
        review_decision_record_id=review_decision_record_id,
        reviewer_role=kwargs.pop("reviewer_role", PatchReviewerRoleKind.HUMAN_REVIEWER),
        decision_kind=kwargs.pop("decision_kind", PatchReviewDecisionKind.APPROVED_FOR_REVIEW),
        outcome_kind=kwargs.pop("outcome_kind", PatchReviewOutcomeKind.APPROVED_FOR_REVIEW),
        decision_summary=kwargs.pop("decision_summary", "Approved for review metadata only."),
        rationale=kwargs.pop("rationale", "Approval for review does not approve apply."),
        approved_for_review=kwargs.pop("approved_for_review", True),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0356_DOC_PATH]),
        **kwargs,
    )


def build_patch_review_packet(review_packet_id: str = "review_packet:v0.35.6", **kwargs: Any) -> PatchReviewPacket:
    risk_summary = kwargs.pop("risk_summary", build_patch_review_risk_summary())
    blocked = risk_summary.blocking_risk_count > 0
    return PatchReviewPacket(
        review_packet_id=review_packet_id,
        version=kwargs.pop("version", V0356_VERSION),
        review_input_id=kwargs.pop("review_input_id", "patch_review_input:v0.35.6"),
        mode=kwargs.pop("mode", PatchReviewPacketMode.FULL_PATCH_PROPOSAL_REVIEW if not blocked else PatchReviewPacketMode.BLOCKED),
        status=kwargs.pop("status", PatchReviewPacketStatus.PENDING_HUMAN_REVIEW if not blocked else PatchReviewPacketStatus.BLOCKED),
        readiness_level=kwargs.pop("readiness_level", PatchReviewReadinessLevel.REVIEW_PACKET_READY if not blocked else PatchReviewReadinessLevel.BLOCKED),
        artifact_summaries=kwargs.pop("artifact_summaries", [build_patch_review_artifact_summary()]),
        risk_summary=risk_summary,
        checklist=kwargs.pop("checklist", build_patch_review_checklist()),
        approval_gate_metadata=kwargs.pop("approval_gate_metadata", build_patch_approval_gate_metadata()),
        reviewer_decision_placeholders=kwargs.pop("reviewer_decision_placeholders", [build_patch_reviewer_decision_placeholder()]),
        decision_records=kwargs.pop("decision_records", []),
        source_refs=kwargs.pop("source_refs", [build_patch_review_source_ref()]),
        summary=kwargs.pop("summary", "Human review packet is review metadata, not apply permission."),
        gaps=kwargs.pop("gaps", []),
        ready_for_v0357_patch_proposal_ocel_trace_packet=kwargs.pop("ready_for_v0357_patch_proposal_ocel_trace_packet", True),
        ready_for_v0358_cli_patch_proposal_surface=kwargs.pop("ready_for_v0358_cli_patch_proposal_surface", True),
        ready_for_human_review=kwargs.pop("ready_for_human_review", not blocked),
        approved_for_review=kwargs.pop("approved_for_review", False),
        **kwargs,
    )


def build_patch_review_input_from_risk_report(risk_report: PatchProposalRiskReport | None = None, **kwargs: Any) -> PatchReviewInput:
    if risk_report is None:
        return build_patch_review_input(
            proposal_risk_report_id=None,
            requested_mode=PatchReviewPacketMode.BLOCKED,
            task_summary="Review input is blocked because risk report metadata is missing.",
            metadata={"gap": "missing_risk_report"},
            **kwargs,
        )
    return build_patch_review_input(proposal_risk_report_id=risk_report.proposal_risk_report_id, source_refs=[build_patch_review_source_ref(source_id=risk_report.proposal_risk_report_id)], **kwargs)


def build_patch_review_checklist_from_risk_report(risk_report: PatchProposalRiskReport | None = None) -> PatchReviewChecklist:
    if risk_report is None:
        return build_patch_review_checklist(checklist_items=[build_patch_review_checklist_item(blocked=True, item_summary="Risk report is missing and blocks review approval metadata.")], ready_for_human_review=False)
    blocked = risk_report.blocked
    items = [
        build_patch_review_checklist_item(satisfied=not blocked, blocked=blocked, item_summary="Risk report must be acceptable for human review."),
        build_patch_review_checklist_item("review_checklist_item:v0.35.6:no_apply", item_kind=PatchReviewChecklistItemKind.VERIFY_NO_WRITE_APPLY_RUNTIME, satisfied=True, item_summary="Verify review metadata does not grant apply permission."),
    ]
    return build_patch_review_checklist(checklist_items=items, ready_for_human_review=not blocked)


def build_patch_review_packet_from_risk_and_diff(risk_report: PatchProposalRiskReport | None = None, diff_envelope: DiffProposalEnvelope | None = None, **kwargs: Any) -> PatchReviewPacket:
    if risk_report is None:
        risk_summary = build_patch_review_risk_summary(proposal_risk_report_id=None, risk_summary="Missing risk report blocks human review packet.", blocking_risk_count=1, review_required_count=1, acceptable_for_review=False, risk_kinds=[PatchReviewRiskKind.MISSING_RISK_REPORT])
        return build_patch_review_packet(risk_summary=risk_summary, checklist=build_patch_review_checklist_from_risk_report(None), gaps=["missing risk report"], status=PatchReviewPacketStatus.BLOCKED, mode=PatchReviewPacketMode.BLOCKED, ready_for_human_review=False, **kwargs)
    risk_kinds: list[PatchReviewRiskKind] = []
    if risk_report.blocked:
        risk_kinds.append(PatchReviewRiskKind.BLOCKING_RISK_PRESENT)
    if risk_report.safety_regression_report.blocked:
        risk_kinds.append(PatchReviewRiskKind.SAFETY_REGRESSION_PRESENT)
    if risk_report.scope_violation_report.blocked:
        risk_kinds.append(PatchReviewRiskKind.SCOPE_VIOLATION_PRESENT)
    missing_diff = diff_envelope is None
    if missing_diff:
        risk_kinds.append(PatchReviewRiskKind.MISSING_DIFF_PROPOSAL)
    blocked = risk_report.blocked
    requires_revision = missing_diff and not blocked
    ready_for_human_review = risk_report.acceptable_for_review and not blocked and not missing_diff
    risk_summary = build_patch_review_risk_summary(
        proposal_risk_report_id=risk_report.proposal_risk_report_id,
        risk_summary=risk_report.summary,
        blocking_risk_count=1 if blocked else 0,
        review_required_count=1 if risk_report.requires_review or missing_diff else 0,
        acceptable_for_review=ready_for_human_review,
        risk_kinds=risk_kinds,
    )
    artifacts = [build_patch_review_artifact_summary(artifact_id=risk_report.proposal_risk_report_id, artifact_summary=risk_report.summary)]
    if diff_envelope is not None:
        artifacts.append(build_patch_review_artifact_summary("review_artifact:v0.35.6:diff", artifact_kind="DiffProposalEnvelope", artifact_id=diff_envelope.diff_envelope_id, artifact_summary=diff_envelope.summary, bounded_preview=diff_envelope.summary))
    return build_patch_review_packet(
        risk_summary=risk_summary,
        artifact_summaries=artifacts,
        checklist=build_patch_review_checklist_from_risk_report(risk_report),
        status=PatchReviewPacketStatus.BLOCKED if blocked else PatchReviewPacketStatus.NEEDS_REVISION if requires_revision else PatchReviewPacketStatus.PENDING_HUMAN_REVIEW,
        mode=PatchReviewPacketMode.BLOCKED if blocked else PatchReviewPacketMode.NEEDS_REVISION if requires_revision else PatchReviewPacketMode.FULL_PATCH_PROPOSAL_REVIEW,
        gaps=["missing diff proposal"] if missing_diff else [],
        ready_for_human_review=ready_for_human_review,
        **kwargs,
    )


def build_patch_review_validation_finding(finding_id: str = "review_validation:v0.35.6:ok", **kwargs: Any) -> PatchReviewValidationFinding:
    return PatchReviewValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchReviewDecisionKind.READY_FOR_HUMAN_REVIEW),
        risk_kinds=kwargs.pop("risk_kinds", []),
        finding_summary=kwargs.pop("finding_summary", "Review packet does not certify apply/write/execution."),
        evidence_preview=kwargs.pop("evidence_preview", "review metadata"),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_review_validation_report(validation_report_id: str = "review_validation_report:v0.35.6", **kwargs: Any) -> PatchReviewValidationReport:
    findings = kwargs.pop("findings", [build_patch_review_validation_finding()])
    return PatchReviewValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0356_VERSION),
        review_packet_id=kwargs.pop("review_packet_id", "review_packet:v0.35.6"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Review validation does not certify apply/write/execution."),
        **kwargs,
    )


def build_patch_review_readiness_report(readiness_report_id: str = "review_readiness:v0.35.6", **kwargs: Any) -> PatchReviewReadinessReport:
    return PatchReviewReadinessReport(
        readiness_report_id=readiness_report_id,
        version=kwargs.pop("version", V0356_VERSION),
        review_packet_id=kwargs.pop("review_packet_id", "review_packet:v0.35.6"),
        summary=kwargs.pop("summary", "Review packet artifacts are ready for human review metadata only."),
        ready_for_human_review_packet=kwargs.pop("ready_for_human_review_packet", True),
        ready_for_review_checklist=kwargs.pop("ready_for_review_checklist", True),
        ready_for_approval_gate_metadata=kwargs.pop("ready_for_approval_gate_metadata", True),
        ready_for_reviewer_decision_placeholder=kwargs.pop("ready_for_reviewer_decision_placeholder", True),
        **kwargs,
    )


def build_patch_review_report(review_report_id: str = "review_report:v0.35.6", **kwargs: Any) -> PatchReviewReport:
    return PatchReviewReport(
        review_report_id=review_report_id,
        version=kwargs.pop("version", V0356_VERSION),
        review_packet_id=kwargs.pop("review_packet_id", "review_packet:v0.35.6"),
        summary=kwargs.pop("summary", "Human review packet is ready as review metadata only."),
        review_packet_ready=kwargs.pop("review_packet_ready", True),
        checklist_ready=kwargs.pop("checklist_ready", True),
        approval_gate_metadata_ready=kwargs.pop("approval_gate_metadata_ready", True),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0356_DOC_PATH, DEFAULT_V0355_RISK_DOC_REF]),
        **kwargs,
    )


def build_patch_review_run_preview(run_preview_id: str = "review_run_preview:v0.35.6", **kwargs: Any) -> PatchReviewRunPreview:
    return PatchReviewRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["summarize supplied risk metadata", "build checklist", "build no-apply gate metadata", "build reviewer placeholder"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["PatchReviewPacket", "PatchReviewChecklist", "PatchApprovalGateMetadata"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["apply approval", "patch application", "workspace write", "code edit", "apply_patch", "git apply", "test execution", "shell execution"]),
        **kwargs,
    )


def build_patch_review_no_apply_guarantee(guarantee_id: str = "review_no_apply:v0.35.6", **kwargs: Any) -> PatchReviewNoApplyGuarantee:
    return PatchReviewNoApplyGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0356_VERSION), **kwargs)


def build_v0356_readiness_report(report_id: str = "readiness:v0.35.6", **kwargs: Any) -> V0356ReadinessReport:
    return V0356ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0356_VERSION),
        review_packet_id=kwargs.pop("review_packet_id", "review_packet:v0.35.6"),
        summary=kwargs.pop("summary", "v0.35.6 is ready for v0.35.7/v0.35.8 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["PatchReviewPacket", "PatchReviewChecklist", "PatchApprovalGateMetadata", "PatchReviewerDecisionPlaceholder"]),
        blocked_items=kwargs.pop("blocked_items", ["apply approval", "patch application", "workspace write", "code edit", "apply_patch", "git apply", "test execution", "shell execution"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.7 Patch Proposal OCEL Trace Packet", "v0.35.8 CLI Patch Proposal Surface"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0356_DOC_PATH, DEFAULT_V0355_RISK_DOC_REF, DEFAULT_V0354_DIFF_DOC_REF, DEFAULT_V0353_PLAN_DOC_REF, DEFAULT_V0352_CONTEXT_DOC_REF, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any apply approval/apply/write/edit/test/shell/reference execution path is introduced."]),
        **kwargs,
    )


def validate_patch_review_packet(packet: PatchReviewPacket) -> PatchReviewValidationReport:
    findings: list[PatchReviewValidationFinding] = []
    if not patch_review_packet_is_not_apply_permission(packet):
        findings.append(build_patch_review_validation_finding("review_validation:v0.35.6:apply", decision_kind=PatchReviewDecisionKind.BLOCKED_BY_RISK, risk_kinds=[PatchReviewRiskKind.PATCH_APPLY_RISK], finding_summary="Review packet cannot grant apply permission.", evidence_preview="apply permission readiness", blocks_validation=True))
    if packet.risk_summary.blocking_risk_count > 0 and packet.approved_for_review:
        findings.append(build_patch_review_validation_finding("review_validation:v0.35.6:blocking_risk", decision_kind=PatchReviewDecisionKind.BLOCKED_BY_RISK, risk_kinds=[PatchReviewRiskKind.BLOCKING_RISK_PRESENT], finding_summary="Blocked risk report cannot be approved for review.", evidence_preview="blocking risk present", blocks_validation=True))
    if not findings:
        findings.append(build_patch_review_validation_finding())
    return build_patch_review_validation_report(review_packet_id=packet.review_packet_id, findings=findings)


def patch_review_flags_preserve_no_apply(flags: PatchReviewFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_REVIEW_FLAG_NAMES) and flags.production_certified is False


def patch_review_policy_blocks_apply(policy: PatchReviewPolicy) -> bool:
    return (
        policy.allow_approved_for_apply is False
        and policy.allow_patch_application is False
        and policy.allow_workspace_write is False
        and policy.allow_code_edit is False
        and policy.allow_test_execution is False
        and policy.allow_shell is False
        and policy.allow_dependency_install is False
    )


def patch_approval_gate_metadata_is_not_apply_permission(gate: PatchApprovalGateMetadata) -> bool:
    return gate.allows_apply_permission is False and gate.allows_workspace_write is False and gate.allows_code_edit is False and gate.applies_patch is False


def patch_review_decision_record_is_not_apply_permission(record: PatchReviewDecisionRecord) -> bool:
    return record.approved_for_apply is False and record.ready_for_apply is False and record.ready_for_execution is False


def patch_review_packet_is_not_apply_permission(packet: PatchReviewPacket) -> bool:
    return packet.approved_for_apply is False and packet.ready_for_apply is False and packet.ready_for_execution is False and patch_approval_gate_metadata_is_not_apply_permission(packet.approval_gate_metadata)


def v0356_readiness_report_is_not_execution_ready(report: V0356ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_PATCH_REVIEW_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
