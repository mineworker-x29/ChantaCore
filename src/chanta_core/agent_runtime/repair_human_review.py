from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0386_VERSION = "v0.38.6"
V0386_RELEASE_NAME = "v0.38.6 Human Review Packet & Approval Request Contract"

SAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES = (
    "ready_for_v0387_bounded_repair_proposal_loop_trial",
    "ready_for_v0388_cli_repair_proposal_surface",
    "ready_for_v039_human_approved_sandbox_repair_apply",
    "ready_for_human_review_packet",
    "ready_for_approval_request_contract",
    "ready_for_review_checklist",
    "ready_for_review_questions",
    "ready_for_apply_precondition_metadata",
    "ready_for_review_evidence_summary",
    "ready_for_review_patch_summary",
    "ready_for_review_safety_summary",
    "ready_for_review_do_nothing_comparison",
    "ready_for_future_bounded_repair_proposal_loop_trial_input",
    "ready_for_future_cli_repair_proposal_surface_input",
    "ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input",
)

UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_human_approval_capture",
    "ready_for_approval_grant",
    "ready_for_apply_permission",
    "ready_for_review_packet_file_write",
    "ready_for_review_packet_external_send",
    "ready_for_ui_runtime",
    "ready_for_source_file_read",
    "ready_for_sandbox_source_read",
    "ready_for_live_workspace_read",
    "ready_for_unbounded_source_read",
    "ready_for_reference_source_read",
    "ready_for_secret_read",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
    "ready_for_patch_file_write",
    "ready_for_file_edit",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_applied_diff_generation",
    "ready_for_applied_code_hunk_generation",
    "ready_for_repair_execution",
    "ready_for_repair_apply",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_write",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_automatic_repair",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_repair_loop",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_model_provider_invocation",
    "ready_for_tool_execution",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_REPAIR_HUMAN_REVIEW_POLICY_ALLOW_NAMES = (
    "allow_human_approval_capture",
    "allow_approval_grant",
    "allow_apply_permission",
    "allow_review_packet_file_write",
    "allow_review_packet_external_send",
    "allow_ui_runtime",
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_source_file_write",
    "allow_patch_file_write",
    "allow_file_edit",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_repair_execution",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_APPROVAL_CONTRACT_STATE_NAMES = (
    "human_approval_present",
    "approval_granted",
    "approval_captured_now",
    "apply_allowed",
    "sandbox_apply_allowed",
    "live_apply_allowed",
    "patch_application_allowed",
    "repair_execution_allowed",
)

UNSAFE_REVIEW_PACKET_STATE_NAMES = (
    "human_approval_present",
    "approval_granted",
    "approval_captured_now",
    "apply_allowed",
    "sandbox_apply_allowed",
    "live_apply_allowed",
    "review_packet_written_to_file",
    "review_packet_sent_externally",
    "ui_runtime_invoked",
    "file_write_performed",
    "patch_file_written",
    "file_edit_performed",
    "patch_applied",
    "apply_patch_called",
    "git_apply_called",
    "tests_run",
    "repair_executed",
    "model_invocation_performed",
    "external_agent_invoked",
    "production_certified",
    "ready_for_execution",
)

UNSAFE_REVIEW_DECISION_NOW_NAMES = (
    "approval_capture_allowed_now",
    "approval_grant_allowed_now",
    "apply_permission_allowed_now",
    "file_write_allowed_now",
    "external_send_allowed_now",
    "ui_runtime_allowed_now",
    "patch_application_allowed_now",
    "repair_execution_allowed_now",
    "test_execution_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "production_certified",
)

REQUIRED_REPAIR_HUMAN_REVIEW_PROHIBITED_ACTIONS = (
    "approval_capture",
    "approval_grant",
    "apply_permission",
    "review_packet_file_write",
    "external_send",
    "ui_runtime",
    "source_read",
    "source_write",
    "patch_file_write",
    "file_edit",
    "patch_apply",
    "apply_patch",
    "git_apply",
    "repair_execution",
    "test_execution",
    "subprocess",
    "shell",
    "dependency_install",
    "network",
    "model_provider",
    "external_agent",
    "dominion",
)


class RepairHumanReviewMode(StrEnum):
    HUMAN_REVIEW_PACKET = "human_review_packet"
    APPROVAL_REQUEST_CONTRACT = "approval_request_contract"
    REVIEW_CHECKLIST = "review_checklist"
    REVIEW_QUESTIONS = "review_questions"
    APPLY_PRECONDITION_METADATA = "apply_precondition_metadata"
    REVIEW_EVIDENCE_SUMMARY = "review_evidence_summary"
    REVIEW_PATCH_SUMMARY = "review_patch_summary"
    REVIEW_SAFETY_SUMMARY = "review_safety_summary"
    DO_NOTHING_REVIEW_COMPARISON = "do_nothing_review_comparison"
    FUTURE_LOOP_TRIAL_INPUT = "future_loop_trial_input"
    FUTURE_CLI_SURFACE_INPUT = "future_cli_surface_input"
    FUTURE_V039_APPLY_CONTRACT_INPUT = "future_v039_apply_contract_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairHumanReviewSourceKind(StrEnum):
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0385_SAFETY_DECISION = "v0385_safety_decision"
    V0385_SAFETY_RISK_ASSESSMENT = "v0385_safety_risk_assessment"
    V0385_BOUNDARY_VIOLATION = "v0385_boundary_violation"
    V0385_UNSAFE_OPERATION_SIGNAL = "v0385_unsafe_operation_signal"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0384_PROPOSED_DIFF_METADATA = "v0384_proposed_diff_metadata"
    V0384_PROPOSED_CODE_HUNK = "v0384_proposed_code_hunk"
    V0384_PROPOSED_FILE_CHANGE = "v0384_proposed_file_change"
    V0383_REPAIR_SCOPE_PLAN = "v0383_repair_scope_plan"
    V0383_REPAIR_CHANGE_INTENT = "v0383_repair_change_intent"
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairHumanReviewStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    REVIEW_PACKET_CREATED = "review_packet_created"
    REVIEW_PACKET_CREATED_WITH_WARNINGS = "review_packet_created_with_warnings"
    APPROVAL_REQUEST_CONTRACT_CREATED = "approval_request_contract_created"
    CHECKLIST_CREATED = "checklist_created"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    UNSAFE_FOR_REVIEW = "unsafe_for_review"
    READY_FOR_FUTURE_LOOP_TRIAL = "ready_for_future_loop_trial"
    READY_FOR_FUTURE_CLI_SURFACE = "ready_for_future_cli_surface"
    FUTURE_V039_APPLY_CONTRACT_PREPARED = "future_v039_apply_contract_prepared"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairHumanReviewReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    REVIEW_PACKET_CONTRACT_READY = "review_packet_contract_ready"
    EVIDENCE_SUMMARY_READY = "evidence_summary_ready"
    PATCH_SUMMARY_READY = "patch_summary_ready"
    SAFETY_SUMMARY_READY = "safety_summary_ready"
    CHECKLIST_READY = "checklist_ready"
    APPROVAL_REQUEST_CONTRACT_READY = "approval_request_contract_ready"
    APPLY_PRECONDITION_METADATA_READY = "apply_precondition_metadata_ready"
    FUTURE_LOOP_TRIAL_INPUT_READY = "future_loop_trial_input_ready"
    FUTURE_CLI_SURFACE_INPUT_READY = "future_cli_surface_input_ready"
    FUTURE_V039_APPLY_CONTRACT_INPUT_READY = "future_v039_apply_contract_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0387 = "design_handoff_ready_for_v0387"
    DESIGN_HANDOFF_READY_FOR_V0388 = "design_handoff_ready_for_v0388"
    FUTURE_HANDOFF_READY_FOR_V039 = "future_handoff_ready_for_v039"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairHumanReviewDecisionKind(StrEnum):
    ALLOW_HUMAN_REVIEW_PACKET = "allow_human_review_packet"
    ALLOW_APPROVAL_REQUEST_CONTRACT = "allow_approval_request_contract"
    ALLOW_REVIEW_CHECKLIST = "allow_review_checklist"
    ALLOW_REVIEW_QUESTIONS = "allow_review_questions"
    ALLOW_APPLY_PRECONDITION_METADATA = "allow_apply_precondition_metadata"
    ALLOW_REVIEW_EVIDENCE_SUMMARY = "allow_review_evidence_summary"
    ALLOW_REVIEW_PATCH_SUMMARY = "allow_review_patch_summary"
    ALLOW_REVIEW_SAFETY_SUMMARY = "allow_review_safety_summary"
    ALLOW_DO_NOTHING_REVIEW_COMPARISON = "allow_do_nothing_review_comparison"
    ALLOW_FUTURE_LOOP_TRIAL_INPUT = "allow_future_loop_trial_input"
    ALLOW_FUTURE_CLI_SURFACE_INPUT = "allow_future_cli_surface_input"
    ALLOW_FUTURE_V039_APPLY_CONTRACT_INPUT = "allow_future_v039_apply_contract_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    UNSAFE_FOR_REVIEW = "unsafe_for_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairHumanReviewRiskKind(StrEnum):
    MISSING_SAFETY_REPORT_RISK = "missing_safety_report_risk"
    MISSING_PATCH_ENVELOPE_RISK = "missing_patch_envelope_risk"
    MISSING_EVIDENCE_SUMMARY_RISK = "missing_evidence_summary_risk"
    MISSING_DO_NOTHING_COMPARISON_RISK = "missing_do_nothing_comparison_risk"
    MISSING_HUMAN_REVIEW_REQUIREMENT_RISK = "missing_human_review_requirement_risk"
    UNSAFE_PATCH_IN_REVIEW_RISK = "unsafe_patch_in_review_risk"
    APPROVAL_CONFUSION_RISK = "approval_confusion_risk"
    APPLY_PERMISSION_CONFUSION_RISK = "apply_permission_confusion_risk"
    APPROVAL_CAPTURE_CONFUSION_RISK = "approval_capture_confusion_risk"
    REVIEW_PACKET_FILE_WRITE_RISK = "review_packet_file_write_risk"
    EXTERNAL_SEND_RISK = "external_send_risk"
    UI_RUNTIME_RISK = "ui_runtime_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    TEST_EXECUTION_CONFUSION_RISK = "test_execution_confusion_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairReviewPacketSectionKind(StrEnum):
    SUMMARY = "summary"
    EVIDENCE_SUMMARY = "evidence_summary"
    SOURCE_CONTEXT_SUMMARY = "source_context_summary"
    SCOPE_SUMMARY = "scope_summary"
    PROPOSED_PATCH_SUMMARY = "proposed_patch_summary"
    PROPOSED_DIFF_SUMMARY = "proposed_diff_summary"
    PROPOSED_HUNK_SUMMARY = "proposed_hunk_summary"
    SAFETY_SUMMARY = "safety_summary"
    RISK_SUMMARY = "risk_summary"
    DO_NOTHING_COMPARISON = "do_nothing_comparison"
    CHECKLIST = "checklist"
    REVIEW_QUESTIONS = "review_questions"
    APPROVAL_REQUEST_CONTRACT = "approval_request_contract"
    APPLY_PRECONDITIONS = "apply_preconditions"
    BLOCKED_ACTIONS = "blocked_actions"
    FUTURE_HANDOFF = "future_handoff"
    UNKNOWN = "unknown"


class RepairApprovalRequestKind(StrEnum):
    REQUEST_REVIEW_ONLY = "request_review_only"
    REQUEST_APPROVAL_FOR_FUTURE_SAFETY_VALIDATED_PROPOSAL = "request_approval_for_future_safety_validated_proposal"
    REQUEST_APPROVAL_FOR_FUTURE_V039_SANDBOX_APPLY = "request_approval_for_future_v039_sandbox_apply"
    REQUEST_REJECTION = "request_rejection"
    REQUEST_CHANGES = "request_changes"
    REQUEST_DO_NOTHING_CONFIRMATION = "request_do_nothing_confirmation"
    NO_APPROVAL_REQUEST = "no_approval_request"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class RepairReviewChecklistItemKind(StrEnum):
    VERIFY_EVIDENCE = "verify_evidence"
    VERIFY_SCOPE = "verify_scope"
    VERIFY_SOURCE_CONTEXT = "verify_source_context"
    VERIFY_PROPOSED_DIFF = "verify_proposed_diff"
    VERIFY_PROPOSED_HUNKS = "verify_proposed_hunks"
    VERIFY_SAFETY_REPORT = "verify_safety_report"
    VERIFY_NO_UNSAFE_OPERATIONS = "verify_no_unsafe_operations"
    VERIFY_DO_NOTHING_COMPARISON = "verify_do_nothing_comparison"
    VERIFY_HUMAN_REVIEW_REQUIRED = "verify_human_review_required"
    VERIFY_NO_APPLY_PERMISSION = "verify_no_apply_permission"
    VERIFY_NO_PRODUCTION_CERTIFICATION = "verify_no_production_certification"
    VERIFY_FUTURE_V039_PRECONDITIONS = "verify_future_v039_preconditions"
    UNKNOWN = "unknown"


class RepairReviewQuestionKind(StrEnum):
    SHOULD_REPAIR_BE_CONSIDERED = "should_repair_be_considered"
    IS_SCOPE_CORRECT = "is_scope_correct"
    IS_PROPOSED_CHANGE_REASONABLE = "is_proposed_change_reasonable"
    IS_RISK_ACCEPTABLE_FOR_FUTURE_REVIEW = "is_risk_acceptable_for_future_review"
    IS_DO_NOTHING_PREFERABLE = "is_do_nothing_preferable"
    SHOULD_REQUEST_CHANGES = "should_request_changes"
    SHOULD_REJECT = "should_reject"
    SHOULD_DEFER = "should_defer"
    SHOULD_PREPARE_FUTURE_V039_SANDBOX_APPLY_CONTRACT = "should_prepare_future_v039_sandbox_apply_contract"
    UNKNOWN = "unknown"


class RepairApplyPreconditionKind(StrEnum):
    HUMAN_APPROVAL_REQUIRED = "human_approval_required"
    SAFETY_VALIDATION_REQUIRED = "safety_validation_required"
    REVIEW_PACKET_REQUIRED = "review_packet_required"
    NO_BLOCKING_SAFETY_VIOLATION = "no_blocking_safety_violation"
    PROPOSED_PATCH_ENVELOPE_REQUIRED = "proposed_patch_envelope_required"
    DO_NOTHING_COMPARISON_REQUIRED = "do_nothing_comparison_required"
    SANDBOX_TARGET_REQUIRED = "sandbox_target_required"
    APPLY_SCOPE_MUST_BE_SANDBOX_ONLY = "apply_scope_must_be_sandbox_only"
    NO_LIVE_WORKSPACE_APPLY = "no_live_workspace_apply"
    NO_APPLY_PATCH_WITHOUT_FUTURE_GATE = "no_apply_patch_without_future_gate"
    NO_GIT_APPLY_WITHOUT_FUTURE_GATE = "no_git_apply_without_future_gate"
    RETEST_REQUIRED_AFTER_FUTURE_APPLY = "retest_required_after_future_apply"
    COLD_EVALUATION_REQUIRED_AFTER_FUTURE_APPLY = "cold_evaluation_required_after_future_apply"
    UNKNOWN = "unknown"


class RepairHumanReviewDisposition(StrEnum):
    REVIEW_PACKET_READY = "review_packet_ready"
    REVIEW_PACKET_READY_WITH_WARNINGS = "review_packet_ready_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    UNSAFE_FOR_REVIEW = "unsafe_for_review"
    NO_OP = "no_op"
    FUTURE_GATED = "future_gated"
    UNKNOWN = "unknown"


class RepairHumanReviewConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairHumanReviewDoNothingComparisonKind(StrEnum):
    DO_NOTHING_PREFERRED_DUE_TO_SAFETY = "do_nothing_preferred_due_to_safety"
    DO_NOTHING_PREFERRED_DUE_TO_EVIDENCE = "do_nothing_preferred_due_to_evidence"
    DO_NOTHING_COMPETITIVE = "do_nothing_competitive"
    REVIEW_PACKET_BETTER_THAN_DO_NOTHING = "review_packet_better_than_do_nothing"
    DO_NOTHING_REQUIRED_DUE_TO_BLOCKING_ISSUE = "do_nothing_required_due_to_blocking_issue"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
    UNKNOWN = "unknown"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0386_VERSION not in version:
        raise ValueError("version must include v0.38.6")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.6")


def _validate_true_fields(instance: Any, prefix: str = "no_") -> None:
    for name in instance.__dataclass_fields__:
        if name.startswith(prefix) and getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_metadata(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _attr(value: Any, name: str, default: Any = None) -> Any:
    if value is None:
        return default
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _bounded_text(value: str | None, limit: int) -> tuple[str, bool]:
    text = "" if value is None else str(value)
    if limit >= 0 and len(text) > limit:
        return text[:limit], True
    return text, False


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewFlagSet:
    flag_set_id: str
    version: str
    repair_human_review_layer_constructed: bool
    human_review_packet_available: bool
    approval_request_contract_available: bool
    review_checklist_available: bool
    review_questions_available: bool
    apply_precondition_metadata_available: bool
    review_evidence_summary_available: bool
    review_patch_summary_available: bool
    review_safety_summary_available: bool
    review_do_nothing_comparison_available: bool
    ready_for_v0387_bounded_repair_proposal_loop_trial: bool
    ready_for_v0388_cli_repair_proposal_surface: bool
    ready_for_v039_human_approved_sandbox_repair_apply: bool
    ready_for_human_review_packet: bool
    ready_for_approval_request_contract: bool
    ready_for_review_checklist: bool
    ready_for_review_questions: bool
    ready_for_apply_precondition_metadata: bool
    ready_for_review_evidence_summary: bool
    ready_for_review_patch_summary: bool
    ready_for_review_safety_summary: bool
    ready_for_review_do_nothing_comparison: bool
    ready_for_future_bounded_repair_proposal_loop_trial_input: bool
    ready_for_future_cli_repair_proposal_surface_input: bool
    ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_human_approval_capture: bool
    ready_for_approval_grant: bool
    ready_for_apply_permission: bool
    ready_for_review_packet_file_write: bool
    ready_for_review_packet_external_send: bool
    ready_for_ui_runtime: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_live_workspace_read: bool
    ready_for_unbounded_source_read: bool
    ready_for_reference_source_read: bool
    ready_for_secret_read: bool
    ready_for_source_file_write: bool
    ready_for_sandbox_source_write: bool
    ready_for_patch_file_write: bool
    ready_for_file_edit: bool
    ready_for_patch_application: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_applied_diff_generation: bool
    ready_for_applied_code_hunk_generation: bool
    ready_for_repair_execution: bool
    ready_for_repair_apply: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_live_workspace_write: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_automatic_repair: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_repair_loop: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_model_provider_invocation: bool
    ready_for_tool_execution: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_provider_invocation: bool
    ready_for_direct_network_access: bool
    ready_for_credential_access: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_independent_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewSourceRef:
    source_ref_id: str
    source_kind: RepairHumanReviewSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairHumanReviewSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewPolicy:
    review_policy_id: str
    version: str
    allowed_modes: list[RepairHumanReviewMode | str]
    required_sections: list[RepairReviewPacketSectionKind | str]
    required_checklist_items: list[RepairReviewChecklistItemKind | str]
    required_apply_preconditions: list[RepairApplyPreconditionKind | str]
    max_packet_chars: int
    max_section_chars: int
    max_checklist_items: int
    max_review_questions: int
    require_safety_report: bool
    require_patch_envelope: bool
    require_evidence_summary: bool
    require_do_nothing_comparison: bool
    require_no_approval_state: bool
    require_apply_preconditions: bool
    allow_human_review_packet: bool
    allow_approval_request_contract: bool
    allow_review_checklist: bool
    allow_review_questions: bool
    allow_apply_precondition_metadata: bool
    allow_future_loop_trial_input: bool
    allow_future_cli_surface_input: bool
    allow_future_v039_apply_contract_input: bool
    allow_human_approval_capture: bool
    allow_approval_grant: bool
    allow_apply_permission: bool
    allow_review_packet_file_write: bool
    allow_review_packet_external_send: bool
    allow_ui_runtime: bool
    allow_source_file_read: bool
    allow_sandbox_source_read: bool
    allow_source_file_write: bool
    allow_patch_file_write: bool
    allow_file_edit: bool
    allow_patch_application: bool
    allow_apply_patch: bool
    allow_git_apply: bool
    allow_repair_execution: bool
    allow_test_execution: bool
    allow_subprocess: bool
    allow_shell: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_model_provider_invocation: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_policy_id", self.review_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, RepairHumanReviewMode)
        _validate_enum_list("required_sections", self.required_sections, RepairReviewPacketSectionKind)
        _validate_enum_list("required_checklist_items", self.required_checklist_items, RepairReviewChecklistItemKind)
        _validate_enum_list("required_apply_preconditions", self.required_apply_preconditions, RepairApplyPreconditionKind)
        for name in ("max_packet_chars", "max_section_chars", "max_checklist_items", "max_review_questions"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(self, UNSAFE_REPAIR_HUMAN_REVIEW_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewInput:
    human_review_input_id: str
    version: str
    safety_report_id: str | None
    safety_decision_id: str | None
    proposed_patch_envelope_id: str | None
    scope_plan_id: str | None
    evidence_bundle_id: str | None
    requested_mode: RepairHumanReviewMode | str
    source_refs: list[RepairHumanReviewSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("human_review_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairHumanReviewMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        for action in REQUIRED_REPAIR_HUMAN_REVIEW_PROHIBITED_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairReviewEvidenceSummary:
    evidence_summary_id: str
    summary_text: str
    evidence_refs: list[str]
    missing_evidence_items: list[str]
    contradictory_evidence_items: list[str]
    confidence: RepairHumanReviewConfidenceLevel | str
    bounded: bool
    redacted: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_summary_id", "summary_text"):
            _require_non_blank(name, getattr(self, name))
        for list_name in ("evidence_refs", "missing_evidence_items", "contradictory_evidence_items"):
            _validate_string_list(list_name, getattr(self, list_name))
        RepairHumanReviewConfidenceLevel(self.confidence)
        if self.bounded is not True:
            raise ValueError("evidence summary must be bounded")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairReviewPatchSummary:
    patch_summary_id: str
    summary_text: str
    proposed_patch_envelope_id: str | None
    proposed_file_change_count: int
    proposed_hunk_count: int
    proposed_diff_count: int
    evidence_refs: list[str]
    confidence: RepairHumanReviewConfidenceLevel | str
    bounded: bool
    redacted: bool
    patch_applied: bool
    repair_executed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("patch_summary_id", "summary_text"):
            _require_non_blank(name, getattr(self, name))
        for name in ("proposed_file_change_count", "proposed_hunk_count", "proposed_diff_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_string_list("evidence_refs", self.evidence_refs)
        RepairHumanReviewConfidenceLevel(self.confidence)
        if self.bounded is not True:
            raise ValueError("patch summary must be bounded")
        if self.patch_applied is not False or self.repair_executed is not False:
            raise ValueError("patch summary is not apply or repair execution")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairReviewSafetySummary:
    safety_summary_id: str
    summary_text: str
    safety_report_id: str | None
    blocking_issue_count: int
    review_required_issue_count: int
    warning_count: int
    evidence_refs: list[str]
    confidence: RepairHumanReviewConfidenceLevel | str
    safe_for_review_packet: bool
    safe_for_future_loop_trial_input: bool
    apply_allowed: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_summary_id", "summary_text"):
            _require_non_blank(name, getattr(self, name))
        for name in ("blocking_issue_count", "review_required_issue_count", "warning_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_string_list("evidence_refs", self.evidence_refs)
        RepairHumanReviewConfidenceLevel(self.confidence)
        if self.apply_allowed is not False or self.production_certified is not False:
            raise ValueError("safety summary cannot allow apply or certify production")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairReviewChecklistItem:
    checklist_item_id: str
    item_kind: RepairReviewChecklistItemKind | str
    item_summary: str
    required: bool
    satisfied_by_metadata: bool
    evidence_refs: list[str]
    blocks_approval_request_if_missing: bool
    blocks_future_apply_if_missing: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("checklist_item_id", "item_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairReviewChecklistItemKind(self.item_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairReviewQuestion:
    review_question_id: str
    question_kind: RepairReviewQuestionKind | str
    question_text: str
    rationale: str
    evidence_refs: list[str]
    response_required_in_future: bool
    response_captured_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("review_question_id", "question_text", "rationale"):
            _require_non_blank(name, getattr(self, name))
        RepairReviewQuestionKind(self.question_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.response_captured_now is not False:
            raise ValueError("review questions do not capture responses in v0.38.6")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairApplyPrecondition:
    apply_precondition_id: str
    precondition_kind: RepairApplyPreconditionKind | str
    precondition_summary: str
    required_for_future_v039_apply: bool
    satisfied_now: bool
    grants_apply_permission: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("apply_precondition_id", "precondition_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairApplyPreconditionKind(self.precondition_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.grants_apply_permission is not False:
            raise ValueError("apply precondition is not apply permission")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewDoNothingComparison:
    do_nothing_review_comparison_id: str
    comparison_kind: RepairHumanReviewDoNothingComparisonKind | str
    comparison_summary: str
    evidence_refs: list[str]
    do_nothing_remains_valid: bool
    do_nothing_preferred: bool
    do_nothing_required: bool
    review_packet_outperforms_do_nothing: bool
    confidence: RepairHumanReviewConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("do_nothing_review_comparison_id", "comparison_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairHumanReviewDoNothingComparisonKind(self.comparison_kind)
        RepairHumanReviewConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.do_nothing_remains_valid is not True:
            raise ValueError("do-nothing comparison must remain valid")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairApprovalRequestContract:
    approval_request_contract_id: str
    version: str
    request_kind: RepairApprovalRequestKind | str
    request_summary: str
    requested_reviewer_action: str
    review_packet_id: str | None
    required_checklist_item_ids: list[str]
    required_precondition_ids: list[str]
    approval_scope_summary: str
    future_apply_scope_summary: str
    human_approval_present: bool
    approval_granted: bool
    approval_captured_now: bool
    apply_allowed: bool
    sandbox_apply_allowed: bool
    live_apply_allowed: bool
    patch_application_allowed: bool
    repair_execution_allowed: bool
    expires_without_future_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("approval_request_contract_id", "request_summary", "requested_reviewer_action", "approval_scope_summary", "future_apply_scope_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairApprovalRequestKind(self.request_kind)
        _validate_string_list("required_checklist_item_ids", self.required_checklist_item_ids)
        _validate_string_list("required_precondition_ids", self.required_precondition_ids)
        _validate_false(self, UNSAFE_APPROVAL_CONTRACT_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewPacket:
    human_review_packet_id: str
    version: str
    human_review_input_id: str
    status: RepairHumanReviewStatus | str
    readiness_level: RepairHumanReviewReadinessLevel | str
    disposition: RepairHumanReviewDisposition | str
    evidence_summary: RepairReviewEvidenceSummary
    patch_summary: RepairReviewPatchSummary
    safety_summary: RepairReviewSafetySummary
    checklist_items: list[RepairReviewChecklistItem]
    review_questions: list[RepairReviewQuestion]
    apply_preconditions: list[RepairApplyPrecondition]
    do_nothing_comparison: RepairHumanReviewDoNothingComparison
    approval_request_contract: RepairApprovalRequestContract
    source_refs: list[RepairHumanReviewSourceRef]
    packet_summary: str
    rendered_packet_preview: str
    bounded: bool
    redacted: bool
    ready_for_future_loop_trial_input: bool
    ready_for_future_cli_surface_input: bool
    ready_for_future_v039_apply_contract_input: bool
    human_approval_present: bool
    approval_granted: bool
    approval_captured_now: bool
    apply_allowed: bool
    sandbox_apply_allowed: bool
    live_apply_allowed: bool
    review_packet_written_to_file: bool
    review_packet_sent_externally: bool
    ui_runtime_invoked: bool
    file_write_performed: bool
    patch_file_written: bool
    file_edit_performed: bool
    patch_applied: bool
    apply_patch_called: bool
    git_apply_called: bool
    tests_run: bool
    repair_executed: bool
    model_invocation_performed: bool
    external_agent_invoked: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("human_review_packet_id", "human_review_input_id", "packet_summary", "rendered_packet_preview"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairHumanReviewStatus(self.status)
        RepairHumanReviewReadinessLevel(self.readiness_level)
        RepairHumanReviewDisposition(self.disposition)
        for list_name in ("checklist_items", "review_questions", "apply_preconditions", "source_refs"):
            _validate_list(list_name, getattr(self, list_name))
        if self.bounded is not True:
            raise ValueError("human review packet must be bounded")
        _validate_false(self, UNSAFE_REVIEW_PACKET_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewDecision:
    human_review_decision_id: str
    human_review_packet_id: str | None
    decision_kind: RepairHumanReviewDecisionKind | str
    disposition: RepairHumanReviewDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairHumanReviewConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_loop_trial_input: bool
    ready_for_future_cli_surface_input: bool
    ready_for_future_v039_apply_contract_input: bool
    approval_capture_allowed_now: bool
    approval_grant_allowed_now: bool
    apply_permission_allowed_now: bool
    file_write_allowed_now: bool
    external_send_allowed_now: bool
    ui_runtime_allowed_now: bool
    patch_application_allowed_now: bool
    repair_execution_allowed_now: bool
    test_execution_allowed_now: bool
    model_provider_invocation_allowed_now: bool
    external_agent_allowed_now: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("human_review_decision_id", "decision_summary", "rationale_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairHumanReviewDecisionKind(self.decision_kind)
        RepairHumanReviewDisposition(self.disposition)
        RepairHumanReviewConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_REVIEW_DECISION_NOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairHumanReviewRiskKind | str
    blocks_future_loop_trial: bool
    requires_human_review: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairHumanReviewRiskKind(self.risk_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewValidationReport:
    validation_report_id: str
    version: str
    human_review_packet_id: str
    findings: list[RepairHumanReviewValidationFinding]
    validation_summary: str
    packet_completeness_confirmed: bool
    review_checklist_confirmed: bool
    approval_request_contract_confirmed: bool
    do_nothing_comparison_confirmed: bool
    no_approval_capture_confirmed: bool
    no_apply_permission_confirmed: bool
    no_file_write_confirmed: bool
    no_external_send_confirmed: bool
    no_ui_runtime_confirmed: bool
    no_patch_apply_confirmed: bool
    no_repair_execution_confirmed: bool
    no_tests_confirmed: bool
    no_external_calls_confirmed: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "human_review_packet_id", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        for name in self.__dataclass_fields__:
            if name.endswith("_confirmed") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewReport:
    human_review_report_id: str
    version: str
    human_review_packet_id: str
    human_review_decision_id: str
    validation_report_id: str
    status: RepairHumanReviewStatus | str
    readiness_level: RepairHumanReviewReadinessLevel | str
    report_summary: str
    ready_for_future_loop_trial_input: bool
    ready_for_future_cli_surface_input: bool
    ready_for_future_v039_apply_contract_input: bool
    ready_for_execution: bool
    production_certified: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("human_review_report_id", "human_review_packet_id", "human_review_decision_id", "validation_report_id", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairHumanReviewStatus(self.status)
        RepairHumanReviewReadinessLevel(self.readiness_level)
        if self.ready_for_execution is not False or self.production_certified is not False:
            raise ValueError("human review report is not execution or production readiness")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewRunPreview:
    run_preview_id: str
    version: str
    requested_mode: RepairHumanReviewMode | str
    preview_summary: str
    will_capture_approval: bool
    will_grant_approval: bool
    will_allow_apply: bool
    will_write_files: bool
    will_send_externally: bool
    will_invoke_ui_runtime: bool
    will_apply_patch: bool
    will_execute_repair: bool
    will_run_tests: bool
    will_invoke_model_provider: bool
    will_invoke_external_agent: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairHumanReviewMode(self.requested_mode)
        for name in self.__dataclass_fields__:
            if name.startswith("will_") and getattr(self, name) is not False:
                raise ValueError(f"{name} must be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewNoApprovalGuarantee:
    guarantee_id: str
    version: str
    no_approval_capture: bool
    no_approval_grant: bool
    no_apply_permission: bool
    no_file_write: bool
    no_external_send: bool
    no_ui: bool
    no_patch_apply: bool
    no_repair: bool
    no_test: bool
    no_external_call: bool
    no_source_read: bool
    no_patch_file: bool
    no_subprocess: bool
    no_shell: bool
    no_network: bool
    no_model_provider: bool
    no_external_agent: bool
    no_dominion_runtime: bool
    guarantee_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "guarantee_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true_fields(self)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0386ReadinessReport:
    readiness_report_id: str
    version: str
    human_review_packet_id: str
    readiness_level: RepairHumanReviewReadinessLevel | str
    status: RepairHumanReviewStatus | str
    summary: str
    ready_for_v0387_bounded_repair_proposal_loop_trial: bool
    ready_for_v0388_cli_repair_proposal_surface: bool
    ready_for_v039_human_approved_sandbox_repair_apply: bool
    ready_for_human_review_packet: bool
    ready_for_approval_request_contract: bool
    ready_for_review_checklist: bool
    ready_for_review_questions: bool
    ready_for_apply_precondition_metadata: bool
    ready_for_review_evidence_summary: bool
    ready_for_review_patch_summary: bool
    ready_for_review_safety_summary: bool
    ready_for_review_do_nothing_comparison: bool
    ready_for_future_bounded_repair_proposal_loop_trial_input: bool
    ready_for_future_cli_repair_proposal_surface_input: bool
    ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input: bool
    evidence_refs: list[str]
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_human_approval_capture: bool
    ready_for_approval_grant: bool
    ready_for_apply_permission: bool
    ready_for_review_packet_file_write: bool
    ready_for_review_packet_external_send: bool
    ready_for_ui_runtime: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_live_workspace_read: bool
    ready_for_unbounded_source_read: bool
    ready_for_reference_source_read: bool
    ready_for_secret_read: bool
    ready_for_source_file_write: bool
    ready_for_sandbox_source_write: bool
    ready_for_patch_file_write: bool
    ready_for_file_edit: bool
    ready_for_patch_application: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_applied_diff_generation: bool
    ready_for_applied_code_hunk_generation: bool
    ready_for_repair_execution: bool
    ready_for_repair_apply: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_live_workspace_write: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_automatic_repair: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_repair_loop: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_model_provider_invocation: bool
    ready_for_tool_execution: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_provider_invocation: bool
    ready_for_direct_network_access: bool
    ready_for_credential_access: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_independent_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "human_review_packet_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairHumanReviewReadinessLevel(self.readiness_level)
        RepairHumanReviewStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES)
        _validate_metadata(self.metadata)


def build_repair_human_review_flags(**kwargs: Any) -> RepairHumanReviewFlagSet:
    return RepairHumanReviewFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_human_review_flags:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        repair_human_review_layer_constructed=kwargs.pop("repair_human_review_layer_constructed", True),
        human_review_packet_available=kwargs.pop("human_review_packet_available", True),
        approval_request_contract_available=kwargs.pop("approval_request_contract_available", True),
        review_checklist_available=kwargs.pop("review_checklist_available", True),
        review_questions_available=kwargs.pop("review_questions_available", True),
        apply_precondition_metadata_available=kwargs.pop("apply_precondition_metadata_available", True),
        review_evidence_summary_available=kwargs.pop("review_evidence_summary_available", True),
        review_patch_summary_available=kwargs.pop("review_patch_summary_available", True),
        review_safety_summary_available=kwargs.pop("review_safety_summary_available", True),
        review_do_nothing_comparison_available=kwargs.pop("review_do_nothing_comparison_available", True),
        ready_for_v0387_bounded_repair_proposal_loop_trial=kwargs.pop("ready_for_v0387_bounded_repair_proposal_loop_trial", True),
        ready_for_v0388_cli_repair_proposal_surface=kwargs.pop("ready_for_v0388_cli_repair_proposal_surface", True),
        ready_for_v039_human_approved_sandbox_repair_apply=kwargs.pop("ready_for_v039_human_approved_sandbox_repair_apply", True),
        ready_for_human_review_packet=kwargs.pop("ready_for_human_review_packet", True),
        ready_for_approval_request_contract=kwargs.pop("ready_for_approval_request_contract", True),
        ready_for_review_checklist=kwargs.pop("ready_for_review_checklist", True),
        ready_for_review_questions=kwargs.pop("ready_for_review_questions", True),
        ready_for_apply_precondition_metadata=kwargs.pop("ready_for_apply_precondition_metadata", True),
        ready_for_review_evidence_summary=kwargs.pop("ready_for_review_evidence_summary", True),
        ready_for_review_patch_summary=kwargs.pop("ready_for_review_patch_summary", True),
        ready_for_review_safety_summary=kwargs.pop("ready_for_review_safety_summary", True),
        ready_for_review_do_nothing_comparison=kwargs.pop("ready_for_review_do_nothing_comparison", True),
        ready_for_future_bounded_repair_proposal_loop_trial_input=kwargs.pop("ready_for_future_bounded_repair_proposal_loop_trial_input", True),
        ready_for_future_cli_repair_proposal_surface_input=kwargs.pop("ready_for_future_cli_repair_proposal_surface_input", True),
        ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input=kwargs.pop("ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input", True),
        metadata=kwargs.pop("metadata", {
            "digestion_first_policy_applied": True,
            "dominion_runtime_blocked": True,
            "external_agent_execution_blocked": True,
            "infinite_agent_loop_blocked": True,
            "recursive_self_invocation_blocked": True,
            "automatic_repair_loop_blocked": True,
            "repair_execution_blocked": True,
            "model_provider_invocation_blocked": True,
            "tool_execution_blocked": True,
            "bounded_repair_proposal_metadata_only": True,
            "human_review_packet_only": True,
            "approval_request_not_approval": True,
            "no_independent_autonomous_agent_runtime": True,
            "mandatory_human_review_before_any_apply": True,
        }),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES},
    )


def build_repair_human_review_source_ref(**kwargs: Any) -> RepairHumanReviewSourceRef:
    return RepairHumanReviewSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "repair_human_review_source_ref:v0.38.6"),
        source_kind=kwargs.pop("source_kind", RepairHumanReviewSourceKind.V0385_SAFETY_REPORT),
        source_id=kwargs.pop("source_id", "v0.38.5 safety report metadata"),
        source_summary=kwargs.pop("source_summary", "existing safety metadata consumed without file read"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_human_review_policy(**kwargs: Any) -> RepairHumanReviewPolicy:
    return RepairHumanReviewPolicy(
        review_policy_id=kwargs.pop("review_policy_id", "repair_human_review_policy:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [item for item in RepairHumanReviewMode if item != RepairHumanReviewMode.UNKNOWN]),
        required_sections=kwargs.pop("required_sections", [
            RepairReviewPacketSectionKind.EVIDENCE_SUMMARY,
            RepairReviewPacketSectionKind.PROPOSED_PATCH_SUMMARY,
            RepairReviewPacketSectionKind.SAFETY_SUMMARY,
            RepairReviewPacketSectionKind.DO_NOTHING_COMPARISON,
            RepairReviewPacketSectionKind.CHECKLIST,
            RepairReviewPacketSectionKind.APPROVAL_REQUEST_CONTRACT,
            RepairReviewPacketSectionKind.APPLY_PRECONDITIONS,
        ]),
        required_checklist_items=kwargs.pop("required_checklist_items", [
            RepairReviewChecklistItemKind.VERIFY_EVIDENCE,
            RepairReviewChecklistItemKind.VERIFY_SAFETY_REPORT,
            RepairReviewChecklistItemKind.VERIFY_DO_NOTHING_COMPARISON,
            RepairReviewChecklistItemKind.VERIFY_HUMAN_REVIEW_REQUIRED,
            RepairReviewChecklistItemKind.VERIFY_NO_APPLY_PERMISSION,
        ]),
        required_apply_preconditions=kwargs.pop("required_apply_preconditions", [
            RepairApplyPreconditionKind.HUMAN_APPROVAL_REQUIRED,
            RepairApplyPreconditionKind.SAFETY_VALIDATION_REQUIRED,
            RepairApplyPreconditionKind.REVIEW_PACKET_REQUIRED,
            RepairApplyPreconditionKind.NO_LIVE_WORKSPACE_APPLY,
            RepairApplyPreconditionKind.NO_APPLY_PATCH_WITHOUT_FUTURE_GATE,
            RepairApplyPreconditionKind.NO_GIT_APPLY_WITHOUT_FUTURE_GATE,
        ]),
        max_packet_chars=kwargs.pop("max_packet_chars", 16000),
        max_section_chars=kwargs.pop("max_section_chars", 2400),
        max_checklist_items=kwargs.pop("max_checklist_items", 20),
        max_review_questions=kwargs.pop("max_review_questions", 12),
        require_safety_report=kwargs.pop("require_safety_report", True),
        require_patch_envelope=kwargs.pop("require_patch_envelope", True),
        require_evidence_summary=kwargs.pop("require_evidence_summary", True),
        require_do_nothing_comparison=kwargs.pop("require_do_nothing_comparison", True),
        require_no_approval_state=kwargs.pop("require_no_approval_state", True),
        require_apply_preconditions=kwargs.pop("require_apply_preconditions", True),
        allow_human_review_packet=kwargs.pop("allow_human_review_packet", True),
        allow_approval_request_contract=kwargs.pop("allow_approval_request_contract", True),
        allow_review_checklist=kwargs.pop("allow_review_checklist", True),
        allow_review_questions=kwargs.pop("allow_review_questions", True),
        allow_apply_precondition_metadata=kwargs.pop("allow_apply_precondition_metadata", True),
        allow_future_loop_trial_input=kwargs.pop("allow_future_loop_trial_input", True),
        allow_future_cli_surface_input=kwargs.pop("allow_future_cli_surface_input", True),
        allow_future_v039_apply_contract_input=kwargs.pop("allow_future_v039_apply_contract_input", True),
        metadata=kwargs.pop("metadata", {"policy_is_not_approval_or_apply_permission": True}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_HUMAN_REVIEW_POLICY_ALLOW_NAMES},
    )


def default_repair_human_review_policy() -> RepairHumanReviewPolicy:
    return build_repair_human_review_policy()


def build_repair_human_review_input(**kwargs: Any) -> RepairHumanReviewInput:
    return RepairHumanReviewInput(
        human_review_input_id=kwargs.pop("human_review_input_id", "repair_human_review_input:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        safety_report_id=kwargs.pop("safety_report_id", "repair_proposal_safety_report:v0.38.5"),
        safety_decision_id=kwargs.pop("safety_decision_id", "repair_proposal_safety_decision:v0.38.5"),
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", None),
        requested_mode=kwargs.pop("requested_mode", RepairHumanReviewMode.HUMAN_REVIEW_PACKET),
        source_refs=kwargs.pop("source_refs", [build_repair_human_review_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(REQUIRED_REPAIR_HUMAN_REVIEW_PROHIBITED_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "human review packet request, not approval or apply request"),
        metadata=kwargs.pop("metadata", {"input_is_not_approval_or_apply_request": True}),
    )


def build_repair_review_evidence_summary(**kwargs: Any) -> RepairReviewEvidenceSummary:
    text, redacted = _bounded_text(kwargs.pop("summary_text", "review evidence summary metadata only"), kwargs.pop("limit", 2400))
    return RepairReviewEvidenceSummary(
        evidence_summary_id=kwargs.pop("evidence_summary_id", "repair_review_evidence_summary:v0.38.6"),
        summary_text=text,
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence metadata"]),
        missing_evidence_items=kwargs.pop("missing_evidence_items", []),
        contradictory_evidence_items=kwargs.pop("contradictory_evidence_items", []),
        confidence=kwargs.pop("confidence", RepairHumanReviewConfidenceLevel.MEDIUM),
        bounded=kwargs.pop("bounded", True),
        redacted=kwargs.pop("redacted", redacted),
        metadata=kwargs.pop("metadata", {"summary_is_not_proof": True}),
    )


def build_repair_review_patch_summary(**kwargs: Any) -> RepairReviewPatchSummary:
    text, redacted = _bounded_text(kwargs.pop("summary_text", "proposed patch metadata summary for review"), kwargs.pop("limit", 2400))
    return RepairReviewPatchSummary(
        patch_summary_id=kwargs.pop("patch_summary_id", "repair_review_patch_summary:v0.38.6"),
        summary_text=text,
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        proposed_file_change_count=kwargs.pop("proposed_file_change_count", 0),
        proposed_hunk_count=kwargs.pop("proposed_hunk_count", 0),
        proposed_diff_count=kwargs.pop("proposed_diff_count", 0),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.4 proposed patch metadata"]),
        confidence=kwargs.pop("confidence", RepairHumanReviewConfidenceLevel.MEDIUM),
        bounded=kwargs.pop("bounded", True),
        redacted=kwargs.pop("redacted", redacted),
        patch_applied=kwargs.pop("patch_applied", False),
        repair_executed=kwargs.pop("repair_executed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_review_safety_summary(**kwargs: Any) -> RepairReviewSafetySummary:
    return RepairReviewSafetySummary(
        safety_summary_id=kwargs.pop("safety_summary_id", "repair_review_safety_summary:v0.38.6"),
        summary_text=kwargs.pop("summary_text", "safety validation summary for human review"),
        safety_report_id=kwargs.pop("safety_report_id", "repair_proposal_safety_report:v0.38.5"),
        blocking_issue_count=kwargs.pop("blocking_issue_count", 0),
        review_required_issue_count=kwargs.pop("review_required_issue_count", 0),
        warning_count=kwargs.pop("warning_count", 0),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 safety report"]),
        confidence=kwargs.pop("confidence", RepairHumanReviewConfidenceLevel.MEDIUM),
        safe_for_review_packet=kwargs.pop("safe_for_review_packet", True),
        safe_for_future_loop_trial_input=kwargs.pop("safe_for_future_loop_trial_input", True),
        apply_allowed=kwargs.pop("apply_allowed", False),
        production_certified=kwargs.pop("production_certified", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_review_checklist_item(**kwargs: Any) -> RepairReviewChecklistItem:
    return RepairReviewChecklistItem(
        checklist_item_id=kwargs.pop("checklist_item_id", "repair_review_checklist_item:v0.38.6"),
        item_kind=kwargs.pop("item_kind", RepairReviewChecklistItemKind.VERIFY_NO_APPLY_PERMISSION),
        item_summary=kwargs.pop("item_summary", "verify review metadata grants no apply permission"),
        required=kwargs.pop("required", True),
        satisfied_by_metadata=kwargs.pop("satisfied_by_metadata", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 review checklist"]),
        blocks_approval_request_if_missing=kwargs.pop("blocks_approval_request_if_missing", True),
        blocks_future_apply_if_missing=kwargs.pop("blocks_future_apply_if_missing", True),
        metadata=kwargs.pop("metadata", {"checklist_item_is_not_approval": True}),
    )


def build_repair_review_question(**kwargs: Any) -> RepairReviewQuestion:
    return RepairReviewQuestion(
        review_question_id=kwargs.pop("review_question_id", "repair_review_question:v0.38.6"),
        question_kind=kwargs.pop("question_kind", RepairReviewQuestionKind.SHOULD_REPAIR_BE_CONSIDERED),
        question_text=kwargs.pop("question_text", "Should this repair proposal continue to future human review?"),
        rationale=kwargs.pop("rationale", "Question is metadata only and captures no response in v0.38.6"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 review question"]),
        response_required_in_future=kwargs.pop("response_required_in_future", True),
        response_captured_now=kwargs.pop("response_captured_now", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_apply_precondition(**kwargs: Any) -> RepairApplyPrecondition:
    return RepairApplyPrecondition(
        apply_precondition_id=kwargs.pop("apply_precondition_id", "repair_apply_precondition:v0.38.6"),
        precondition_kind=kwargs.pop("precondition_kind", RepairApplyPreconditionKind.HUMAN_APPROVAL_REQUIRED),
        precondition_summary=kwargs.pop("precondition_summary", "future apply requires human approval and future gate"),
        required_for_future_v039_apply=kwargs.pop("required_for_future_v039_apply", True),
        satisfied_now=kwargs.pop("satisfied_now", False),
        grants_apply_permission=kwargs.pop("grants_apply_permission", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 apply precondition metadata"]),
        metadata=kwargs.pop("metadata", {"precondition_is_not_apply_permission": True}),
    )


def build_repair_human_review_do_nothing_comparison(**kwargs: Any) -> RepairHumanReviewDoNothingComparison:
    return RepairHumanReviewDoNothingComparison(
        do_nothing_review_comparison_id=kwargs.pop("do_nothing_review_comparison_id", "repair_human_review_do_nothing:v0.38.6"),
        comparison_kind=kwargs.pop("comparison_kind", RepairHumanReviewDoNothingComparisonKind.DO_NOTHING_COMPETITIVE),
        comparison_summary=kwargs.pop("comparison_summary", "do-nothing remains valid for human review"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 do-nothing review comparison"]),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        do_nothing_preferred=kwargs.pop("do_nothing_preferred", False),
        do_nothing_required=kwargs.pop("do_nothing_required", False),
        review_packet_outperforms_do_nothing=kwargs.pop("review_packet_outperforms_do_nothing", True),
        confidence=kwargs.pop("confidence", RepairHumanReviewConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_approval_request_contract(**kwargs: Any) -> RepairApprovalRequestContract:
    return RepairApprovalRequestContract(
        approval_request_contract_id=kwargs.pop("approval_request_contract_id", "repair_approval_request_contract:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        request_kind=kwargs.pop("request_kind", RepairApprovalRequestKind.REQUEST_REVIEW_ONLY),
        request_summary=kwargs.pop("request_summary", "approval request contract requests future human review only"),
        requested_reviewer_action=kwargs.pop("requested_reviewer_action", "review metadata and decide in a future approved surface"),
        review_packet_id=kwargs.pop("review_packet_id", None),
        required_checklist_item_ids=kwargs.pop("required_checklist_item_ids", []),
        required_precondition_ids=kwargs.pop("required_precondition_ids", []),
        approval_scope_summary=kwargs.pop("approval_scope_summary", "approval is not captured or granted in v0.38.6"),
        future_apply_scope_summary=kwargs.pop("future_apply_scope_summary", "future apply requires v0.39 human-approved sandbox gate"),
        expires_without_future_review=kwargs.pop("expires_without_future_review", True),
        metadata=kwargs.pop("metadata", {"approval_request_contract_is_not_approval": True}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_APPROVAL_CONTRACT_STATE_NAMES},
    )


def build_repair_human_review_packet(**kwargs: Any) -> RepairHumanReviewPacket:
    evidence_summary = kwargs.pop("evidence_summary", build_repair_review_evidence_summary())
    patch_summary = kwargs.pop("patch_summary", build_repair_review_patch_summary())
    safety_summary = kwargs.pop("safety_summary", build_repair_review_safety_summary())
    checklist_items = kwargs.pop("checklist_items", [build_repair_review_checklist_item()])
    review_questions = kwargs.pop("review_questions", [build_repair_review_question()])
    apply_preconditions = kwargs.pop("apply_preconditions", [build_repair_apply_precondition()])
    do_nothing = kwargs.pop("do_nothing_comparison", build_repair_human_review_do_nothing_comparison())
    approval_contract = kwargs.pop("approval_request_contract", build_repair_approval_request_contract(
        required_checklist_item_ids=[item.checklist_item_id for item in checklist_items],
        required_precondition_ids=[item.apply_precondition_id for item in apply_preconditions],
    ))
    preview = kwargs.pop("rendered_packet_preview", None)
    if preview is None:
        preview = "\n".join((
            "v0.38.6 human review packet metadata only",
            evidence_summary.summary_text,
            patch_summary.summary_text,
            safety_summary.summary_text,
            do_nothing.comparison_summary,
            "approval not granted; apply not allowed",
        ))
    preview, preview_redacted = _bounded_text(preview, kwargs.pop("limit", 16000))
    return RepairHumanReviewPacket(
        human_review_packet_id=kwargs.pop("human_review_packet_id", "repair_human_review_packet:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        human_review_input_id=kwargs.pop("human_review_input_id", "repair_human_review_input:v0.38.6"),
        status=kwargs.pop("status", RepairHumanReviewStatus.REVIEW_PACKET_CREATED),
        readiness_level=kwargs.pop("readiness_level", RepairHumanReviewReadinessLevel.REVIEW_PACKET_CONTRACT_READY),
        disposition=kwargs.pop("disposition", RepairHumanReviewDisposition.REVIEW_PACKET_READY),
        evidence_summary=evidence_summary,
        patch_summary=patch_summary,
        safety_summary=safety_summary,
        checklist_items=checklist_items,
        review_questions=review_questions,
        apply_preconditions=apply_preconditions,
        do_nothing_comparison=do_nothing,
        approval_request_contract=approval_contract,
        source_refs=kwargs.pop("source_refs", []),
        packet_summary=kwargs.pop("packet_summary", "human review packet metadata assembled without approval or apply"),
        rendered_packet_preview=preview,
        bounded=kwargs.pop("bounded", True),
        redacted=kwargs.pop("redacted", preview_redacted),
        ready_for_future_loop_trial_input=kwargs.pop("ready_for_future_loop_trial_input", safety_summary.safe_for_future_loop_trial_input),
        ready_for_future_cli_surface_input=kwargs.pop("ready_for_future_cli_surface_input", True),
        ready_for_future_v039_apply_contract_input=kwargs.pop("ready_for_future_v039_apply_contract_input", True),
        metadata=kwargs.pop("metadata", {"in_memory_metadata_only": True}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REVIEW_PACKET_STATE_NAMES},
    )


def build_repair_human_review_decision(**kwargs: Any) -> RepairHumanReviewDecision:
    return RepairHumanReviewDecision(
        human_review_decision_id=kwargs.pop("human_review_decision_id", "repair_human_review_decision:v0.38.6"),
        human_review_packet_id=kwargs.pop("human_review_packet_id", "repair_human_review_packet:v0.38.6"),
        decision_kind=kwargs.pop("decision_kind", RepairHumanReviewDecisionKind.ALLOW_FUTURE_LOOP_TRIAL_INPUT),
        disposition=kwargs.pop("disposition", RepairHumanReviewDisposition.REVIEW_PACKET_READY),
        decision_summary=kwargs.pop("decision_summary", "human review packet is ready as metadata only"),
        rationale_summary=kwargs.pop("rationale_summary", "approval and apply remain blocked until future human gate"),
        confidence=kwargs.pop("confidence", RepairHumanReviewConfidenceLevel.MEDIUM),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 human review packet"]),
        ready_for_future_loop_trial_input=kwargs.pop("ready_for_future_loop_trial_input", True),
        ready_for_future_cli_surface_input=kwargs.pop("ready_for_future_cli_surface_input", True),
        ready_for_future_v039_apply_contract_input=kwargs.pop("ready_for_future_v039_apply_contract_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REVIEW_DECISION_NOW_NAMES},
    )


def build_repair_human_review_validation_finding(**kwargs: Any) -> RepairHumanReviewValidationFinding:
    return RepairHumanReviewValidationFinding(
        finding_id=kwargs.pop("finding_id", "repair_human_review_validation_finding:v0.38.6"),
        finding_summary=kwargs.pop("finding_summary", "human review packet preserves no approval and no apply"),
        risk_kind=kwargs.pop("risk_kind", RepairHumanReviewRiskKind.APPROVAL_CONFUSION_RISK),
        blocks_future_loop_trial=kwargs.pop("blocks_future_loop_trial", False),
        requires_human_review=kwargs.pop("requires_human_review", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 human review validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_human_review_validation_report(**kwargs: Any) -> RepairHumanReviewValidationReport:
    return RepairHumanReviewValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "repair_human_review_validation_report:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        human_review_packet_id=kwargs.pop("human_review_packet_id", "repair_human_review_packet:v0.38.6"),
        findings=kwargs.pop("findings", [build_repair_human_review_validation_finding()]),
        validation_summary=kwargs.pop("validation_summary", "human review validation confirms packet completeness and no approval/apply"),
        packet_completeness_confirmed=kwargs.pop("packet_completeness_confirmed", True),
        review_checklist_confirmed=kwargs.pop("review_checklist_confirmed", True),
        approval_request_contract_confirmed=kwargs.pop("approval_request_contract_confirmed", True),
        do_nothing_comparison_confirmed=kwargs.pop("do_nothing_comparison_confirmed", True),
        no_approval_capture_confirmed=kwargs.pop("no_approval_capture_confirmed", True),
        no_apply_permission_confirmed=kwargs.pop("no_apply_permission_confirmed", True),
        no_file_write_confirmed=kwargs.pop("no_file_write_confirmed", True),
        no_external_send_confirmed=kwargs.pop("no_external_send_confirmed", True),
        no_ui_runtime_confirmed=kwargs.pop("no_ui_runtime_confirmed", True),
        no_patch_apply_confirmed=kwargs.pop("no_patch_apply_confirmed", True),
        no_repair_execution_confirmed=kwargs.pop("no_repair_execution_confirmed", True),
        no_tests_confirmed=kwargs.pop("no_tests_confirmed", True),
        no_external_calls_confirmed=kwargs.pop("no_external_calls_confirmed", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_human_review_report(**kwargs: Any) -> RepairHumanReviewReport:
    packet = kwargs.pop("packet", None)
    decision = kwargs.pop("decision", None)
    validation = kwargs.pop("validation_report", None)
    return RepairHumanReviewReport(
        human_review_report_id=kwargs.pop("human_review_report_id", "repair_human_review_report:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        human_review_packet_id=kwargs.pop("human_review_packet_id", _attr(packet, "human_review_packet_id", "repair_human_review_packet:v0.38.6")),
        human_review_decision_id=kwargs.pop("human_review_decision_id", _attr(decision, "human_review_decision_id", "repair_human_review_decision:v0.38.6")),
        validation_report_id=kwargs.pop("validation_report_id", _attr(validation, "validation_report_id", "repair_human_review_validation_report:v0.38.6")),
        status=kwargs.pop("status", RepairHumanReviewStatus.READY_FOR_FUTURE_LOOP_TRIAL),
        readiness_level=kwargs.pop("readiness_level", RepairHumanReviewReadinessLevel.FUTURE_LOOP_TRIAL_INPUT_READY),
        report_summary=kwargs.pop("report_summary", "human review report metadata only"),
        ready_for_future_loop_trial_input=kwargs.pop("ready_for_future_loop_trial_input", _attr(packet, "ready_for_future_loop_trial_input", True)),
        ready_for_future_cli_surface_input=kwargs.pop("ready_for_future_cli_surface_input", _attr(packet, "ready_for_future_cli_surface_input", True)),
        ready_for_future_v039_apply_contract_input=kwargs.pop("ready_for_future_v039_apply_contract_input", _attr(packet, "ready_for_future_v039_apply_contract_input", True)),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", [_attr(packet, "human_review_packet_id", "v0.38.6 review packet")]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_human_review_run_preview(**kwargs: Any) -> RepairHumanReviewRunPreview:
    return RepairHumanReviewRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "repair_human_review_run_preview:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        requested_mode=kwargs.pop("requested_mode", RepairHumanReviewMode.HUMAN_REVIEW_PACKET),
        preview_summary=kwargs.pop("preview_summary", "review packet preview creates metadata only"),
        will_capture_approval=kwargs.pop("will_capture_approval", False),
        will_grant_approval=kwargs.pop("will_grant_approval", False),
        will_allow_apply=kwargs.pop("will_allow_apply", False),
        will_write_files=kwargs.pop("will_write_files", False),
        will_send_externally=kwargs.pop("will_send_externally", False),
        will_invoke_ui_runtime=kwargs.pop("will_invoke_ui_runtime", False),
        will_apply_patch=kwargs.pop("will_apply_patch", False),
        will_execute_repair=kwargs.pop("will_execute_repair", False),
        will_run_tests=kwargs.pop("will_run_tests", False),
        will_invoke_model_provider=kwargs.pop("will_invoke_model_provider", False),
        will_invoke_external_agent=kwargs.pop("will_invoke_external_agent", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_human_review_no_approval_guarantee(**kwargs: Any) -> RepairHumanReviewNoApprovalGuarantee:
    return RepairHumanReviewNoApprovalGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_human_review_no_approval_guarantee:v0.38.6"),
        version=kwargs.pop("version", V0386_VERSION),
        no_approval_capture=kwargs.pop("no_approval_capture", True),
        no_approval_grant=kwargs.pop("no_approval_grant", True),
        no_apply_permission=kwargs.pop("no_apply_permission", True),
        no_file_write=kwargs.pop("no_file_write", True),
        no_external_send=kwargs.pop("no_external_send", True),
        no_ui=kwargs.pop("no_ui", True),
        no_patch_apply=kwargs.pop("no_patch_apply", True),
        no_repair=kwargs.pop("no_repair", True),
        no_test=kwargs.pop("no_test", True),
        no_external_call=kwargs.pop("no_external_call", True),
        no_source_read=kwargs.pop("no_source_read", True),
        no_patch_file=kwargs.pop("no_patch_file", True),
        no_subprocess=kwargs.pop("no_subprocess", True),
        no_shell=kwargs.pop("no_shell", True),
        no_network=kwargs.pop("no_network", True),
        no_model_provider=kwargs.pop("no_model_provider", True),
        no_external_agent=kwargs.pop("no_external_agent", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        guarantee_summary=kwargs.pop("guarantee_summary", "v0.38.6 creates review metadata only and captures no approval"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v0386_readiness_report(**kwargs: Any) -> V0386ReadinessReport:
    return V0386ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0386_readiness_report"),
        version=kwargs.pop("version", V0386_VERSION),
        human_review_packet_id=kwargs.pop("human_review_packet_id", "repair_human_review_packet:v0.38.6"),
        readiness_level=kwargs.pop("readiness_level", RepairHumanReviewReadinessLevel.FUTURE_LOOP_TRIAL_INPUT_READY),
        status=kwargs.pop("status", RepairHumanReviewStatus.READY_FOR_FUTURE_LOOP_TRIAL),
        summary=kwargs.pop("summary", "v0.38.6 is ready for design-stage loop trial, CLI, and future v0.39 metadata handoff only"),
        ready_for_v0387_bounded_repair_proposal_loop_trial=kwargs.pop("ready_for_v0387_bounded_repair_proposal_loop_trial", True),
        ready_for_v0388_cli_repair_proposal_surface=kwargs.pop("ready_for_v0388_cli_repair_proposal_surface", True),
        ready_for_v039_human_approved_sandbox_repair_apply=kwargs.pop("ready_for_v039_human_approved_sandbox_repair_apply", True),
        ready_for_human_review_packet=kwargs.pop("ready_for_human_review_packet", True),
        ready_for_approval_request_contract=kwargs.pop("ready_for_approval_request_contract", True),
        ready_for_review_checklist=kwargs.pop("ready_for_review_checklist", True),
        ready_for_review_questions=kwargs.pop("ready_for_review_questions", True),
        ready_for_apply_precondition_metadata=kwargs.pop("ready_for_apply_precondition_metadata", True),
        ready_for_review_evidence_summary=kwargs.pop("ready_for_review_evidence_summary", True),
        ready_for_review_patch_summary=kwargs.pop("ready_for_review_patch_summary", True),
        ready_for_review_safety_summary=kwargs.pop("ready_for_review_safety_summary", True),
        ready_for_review_do_nothing_comparison=kwargs.pop("ready_for_review_do_nothing_comparison", True),
        ready_for_future_bounded_repair_proposal_loop_trial_input=kwargs.pop("ready_for_future_bounded_repair_proposal_loop_trial_input", True),
        ready_for_future_cli_repair_proposal_surface_input=kwargs.pop("ready_for_future_cli_repair_proposal_surface_input", True),
        ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input=kwargs.pop("ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.6 human review packet"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES},
    )


def build_repair_human_review_input_from_safety_report(safety_report: Any, proposed_patch_envelope: Any | None = None, scope_plan: Any | None = None, evidence_bundle: Any | None = None) -> RepairHumanReviewInput:
    return build_repair_human_review_input(
        safety_report_id=_attr(safety_report, "safety_report_id", None),
        safety_decision_id=_attr(_attr(safety_report, "safety_decision"), "safety_decision_id", None),
        proposed_patch_envelope_id=_attr(proposed_patch_envelope, "proposed_patch_envelope_id", None),
        scope_plan_id=_attr(scope_plan, "scope_plan_id", None),
        evidence_bundle_id=_attr(evidence_bundle, "evidence_bundle_id", None),
        source_refs=[build_repair_human_review_source_ref(
            source_id=_attr(safety_report, "safety_report_id", "v0.38.5 safety report"),
            evidence_refs=[_attr(safety_report, "safety_report_id", "v0.38.5 safety report")],
        )],
    )


def create_repair_review_evidence_summary(evidence_bundle: Any | None = None, safety_report: Any | None = None, policy: RepairHumanReviewPolicy | None = None) -> RepairReviewEvidenceSummary:
    policy = policy or default_repair_human_review_policy()
    refs = []
    if _attr(evidence_bundle, "evidence_bundle_id"):
        refs.append(_attr(evidence_bundle, "evidence_bundle_id"))
    if _attr(safety_report, "safety_report_id"):
        refs.append(_attr(safety_report, "safety_report_id"))
    text = f"Evidence summary for review packet. refs={', '.join(refs) if refs else 'metadata only'}"
    bounded, redacted = _bounded_text(text, policy.max_section_chars)
    return build_repair_review_evidence_summary(summary_text=bounded, evidence_refs=refs or ["review evidence metadata"], redacted=redacted)


def create_repair_review_patch_summary(proposed_patch_envelope: Any | None = None, policy: RepairHumanReviewPolicy | None = None) -> RepairReviewPatchSummary:
    policy = policy or default_repair_human_review_policy()
    changes = list(_attr(proposed_patch_envelope, "file_changes", []) or [])
    hunks = list(_attr(proposed_patch_envelope, "proposed_hunks", []) or [])
    diffs = list(_attr(proposed_patch_envelope, "proposed_diffs", []) or [])
    text = f"Proposed patch metadata summary: {len(changes)} file changes, {len(hunks)} hunks, {len(diffs)} diffs. Not applied."
    bounded, redacted = _bounded_text(text, policy.max_section_chars)
    return build_repair_review_patch_summary(
        summary_text=bounded,
        proposed_patch_envelope_id=_attr(proposed_patch_envelope, "proposed_patch_envelope_id", None),
        proposed_file_change_count=len(changes),
        proposed_hunk_count=len(hunks),
        proposed_diff_count=len(diffs),
        evidence_refs=[_attr(proposed_patch_envelope, "proposed_patch_envelope_id", "v0.38.4 proposed patch metadata")],
        redacted=redacted,
    )


def create_repair_review_safety_summary(safety_report: Any | None = None, policy: RepairHumanReviewPolicy | None = None) -> RepairReviewSafetySummary:
    policy = policy or default_repair_human_review_policy()
    boundary = list(_attr(safety_report, "boundary_violations", []) or [])
    signals = list(_attr(safety_report, "unsafe_operation_signals", []) or [])
    findings = list(_attr(safety_report, "static_findings", []) or [])
    blocking = len([item for item in boundary + signals if _attr(item, "blocked", False)])
    review_required = len([item for item in boundary + signals + findings if _attr(item, "requires_review", False)])
    safe_loop = bool(_attr(safety_report, "ready_for_future_loop_trial_input", False)) and blocking == 0
    text = f"Safety summary: {blocking} blocking issues, {review_required} review-required issues."
    bounded, _ = _bounded_text(text, policy.max_section_chars)
    return build_repair_review_safety_summary(
        summary_text=bounded,
        safety_report_id=_attr(safety_report, "safety_report_id", None),
        blocking_issue_count=blocking,
        review_required_issue_count=review_required,
        warning_count=max(0, len(findings) - blocking),
        evidence_refs=[_attr(safety_report, "safety_report_id", "v0.38.5 safety report")],
        safe_for_review_packet=True,
        safe_for_future_loop_trial_input=safe_loop,
    )


def create_repair_review_checklist(policy: RepairHumanReviewPolicy | None = None) -> list[RepairReviewChecklistItem]:
    policy = policy or default_repair_human_review_policy()
    return [
        build_repair_review_checklist_item(
            checklist_item_id=f"repair_review_checklist_item:{index}:{kind.value}:v0.38.6",
            item_kind=kind,
            item_summary=f"review checklist requires {kind.value}",
        )
        for index, kind in enumerate(policy.required_checklist_items[: policy.max_checklist_items], start=1)
    ]


def create_repair_review_questions(policy: RepairHumanReviewPolicy | None = None) -> list[RepairReviewQuestion]:
    policy = policy or default_repair_human_review_policy()
    kinds = [
        RepairReviewQuestionKind.SHOULD_REPAIR_BE_CONSIDERED,
        RepairReviewQuestionKind.IS_SCOPE_CORRECT,
        RepairReviewQuestionKind.IS_PROPOSED_CHANGE_REASONABLE,
        RepairReviewQuestionKind.IS_DO_NOTHING_PREFERABLE,
        RepairReviewQuestionKind.SHOULD_PREPARE_FUTURE_V039_SANDBOX_APPLY_CONTRACT,
    ]
    return [
        build_repair_review_question(
            review_question_id=f"repair_review_question:{index}:{kind.value}:v0.38.6",
            question_kind=kind,
            question_text=f"Reviewer question: {kind.value}?",
        )
        for index, kind in enumerate(kinds[: policy.max_review_questions], start=1)
    ]


def create_repair_apply_preconditions(policy: RepairHumanReviewPolicy | None = None) -> list[RepairApplyPrecondition]:
    policy = policy or default_repair_human_review_policy()
    return [
        build_repair_apply_precondition(
            apply_precondition_id=f"repair_apply_precondition:{index}:{kind.value}:v0.38.6",
            precondition_kind=kind,
            precondition_summary=f"future apply precondition metadata: {kind.value}",
        )
        for index, kind in enumerate(policy.required_apply_preconditions, start=1)
    ]


def compare_repair_review_packet_to_do_nothing(safety_summary: RepairReviewSafetySummary) -> RepairHumanReviewDoNothingComparison:
    if safety_summary.blocking_issue_count > 0:
        return build_repair_human_review_do_nothing_comparison(
            comparison_kind=RepairHumanReviewDoNothingComparisonKind.DO_NOTHING_REQUIRED_DUE_TO_BLOCKING_ISSUE,
            comparison_summary="do-nothing is required because blocking safety issues remain",
            do_nothing_preferred=True,
            do_nothing_required=True,
            review_packet_outperforms_do_nothing=False,
            confidence=RepairHumanReviewConfidenceLevel.HIGH,
        )
    if safety_summary.review_required_issue_count > 0:
        return build_repair_human_review_do_nothing_comparison(
            comparison_kind=RepairHumanReviewDoNothingComparisonKind.DO_NOTHING_COMPETITIVE,
            comparison_summary="do-nothing remains competitive because review-required issues remain",
            do_nothing_preferred=False,
            review_packet_outperforms_do_nothing=True,
            confidence=RepairHumanReviewConfidenceLevel.MEDIUM,
        )
    return build_repair_human_review_do_nothing_comparison(
        comparison_kind=RepairHumanReviewDoNothingComparisonKind.REVIEW_PACKET_BETTER_THAN_DO_NOTHING,
        comparison_summary="review packet is useful, while do-nothing remains valid",
    )


def create_repair_approval_request_contract(checklist_items: list[RepairReviewChecklistItem], apply_preconditions: list[RepairApplyPrecondition]) -> RepairApprovalRequestContract:
    return build_repair_approval_request_contract(
        required_checklist_item_ids=[item.checklist_item_id for item in checklist_items],
        required_precondition_ids=[item.apply_precondition_id for item in apply_preconditions],
    )


def create_repair_human_review_packet(
    human_review_input: RepairHumanReviewInput,
    safety_report: Any | None = None,
    proposed_patch_envelope: Any | None = None,
    scope_plan: Any | None = None,
    evidence_bundle: Any | None = None,
    policy: RepairHumanReviewPolicy | None = None,
) -> RepairHumanReviewPacket:
    policy = policy or default_repair_human_review_policy()
    evidence_summary = create_repair_review_evidence_summary(evidence_bundle, safety_report, policy)
    patch_summary = create_repair_review_patch_summary(proposed_patch_envelope, policy)
    safety_summary = create_repair_review_safety_summary(safety_report, policy)
    checklist = create_repair_review_checklist(policy)
    questions = create_repair_review_questions(policy)
    preconditions = create_repair_apply_preconditions(policy)
    do_nothing = compare_repair_review_packet_to_do_nothing(safety_summary)
    approval_contract = create_repair_approval_request_contract(checklist, preconditions)
    disposition = RepairHumanReviewDisposition.REVIEW_PACKET_READY
    status = RepairHumanReviewStatus.REVIEW_PACKET_CREATED
    if do_nothing.do_nothing_required:
        disposition = RepairHumanReviewDisposition.DO_NOTHING_PREFERRED
        status = RepairHumanReviewStatus.DO_NOTHING_PREFERRED
    elif safety_summary.review_required_issue_count:
        disposition = RepairHumanReviewDisposition.REVIEW_PACKET_READY_WITH_WARNINGS
        status = RepairHumanReviewStatus.REVIEW_PACKET_CREATED_WITH_WARNINGS
    return build_repair_human_review_packet(
        human_review_input_id=human_review_input.human_review_input_id,
        status=status,
        disposition=disposition,
        readiness_level=RepairHumanReviewReadinessLevel.FUTURE_LOOP_TRIAL_INPUT_READY if safety_summary.safe_for_future_loop_trial_input else RepairHumanReviewReadinessLevel.REVIEW_PACKET_CONTRACT_READY,
        evidence_summary=evidence_summary,
        patch_summary=patch_summary,
        safety_summary=safety_summary,
        checklist_items=checklist,
        review_questions=questions,
        apply_preconditions=preconditions,
        do_nothing_comparison=do_nothing,
        approval_request_contract=approval_contract,
        source_refs=human_review_input.source_refs,
        ready_for_future_loop_trial_input=safety_summary.safe_for_future_loop_trial_input and not do_nothing.do_nothing_required,
        ready_for_future_cli_surface_input=True,
        ready_for_future_v039_apply_contract_input=True,
        metadata={
            "scope_plan_id": _attr(scope_plan, "scope_plan_id", None),
            "approval_not_granted": True,
            "apply_not_allowed": True,
        },
    )


def decide_repair_human_review_readiness(packet: RepairHumanReviewPacket) -> RepairHumanReviewDecision:
    if packet.do_nothing_comparison.do_nothing_required:
        return build_repair_human_review_decision(
            human_review_packet_id=packet.human_review_packet_id,
            decision_kind=RepairHumanReviewDecisionKind.CHOOSE_DO_NOTHING,
            disposition=RepairHumanReviewDisposition.DO_NOTHING_PREFERRED,
            decision_summary="do-nothing is required by review packet metadata",
            rationale_summary="blocking issue remains and approval/apply are absent",
            ready_for_future_loop_trial_input=False,
            ready_for_future_cli_surface_input=True,
            ready_for_future_v039_apply_contract_input=False,
            confidence=RepairHumanReviewConfidenceLevel.HIGH,
            evidence_refs=[packet.human_review_packet_id],
        )
    return build_repair_human_review_decision(
        human_review_packet_id=packet.human_review_packet_id,
        ready_for_future_loop_trial_input=packet.ready_for_future_loop_trial_input,
        ready_for_future_cli_surface_input=packet.ready_for_future_cli_surface_input,
        ready_for_future_v039_apply_contract_input=packet.ready_for_future_v039_apply_contract_input,
        evidence_refs=[packet.human_review_packet_id],
    )


def validate_repair_human_review_packet(packet: RepairHumanReviewPacket) -> RepairHumanReviewValidationReport:
    return build_repair_human_review_validation_report(human_review_packet_id=packet.human_review_packet_id)


def repair_human_review_flags_preserve_no_approval(flags: RepairHumanReviewFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES)


def repair_human_review_policy_blocks_approval_and_apply(policy: RepairHumanReviewPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_REPAIR_HUMAN_REVIEW_POLICY_ALLOW_NAMES)


def repair_approval_request_contract_is_not_approval(contract: RepairApprovalRequestContract) -> bool:
    return all(getattr(contract, name) is False for name in UNSAFE_APPROVAL_CONTRACT_STATE_NAMES)


def repair_human_review_packet_is_not_apply_permission(packet: RepairHumanReviewPacket) -> bool:
    return all(getattr(packet, name) is False for name in UNSAFE_REVIEW_PACKET_STATE_NAMES)


def repair_human_review_decision_is_not_approval(decision: RepairHumanReviewDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_REVIEW_DECISION_NOW_NAMES)


def v0386_readiness_report_is_not_execution_ready(report: V0386ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPAIR_HUMAN_REVIEW_FLAG_NAMES if hasattr(report, name))
