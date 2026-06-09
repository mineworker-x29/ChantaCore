from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0387_VERSION = "v0.38.7"
V0387_RELEASE_NAME = "v0.38.7 Bounded Repair Proposal Loop Trial"

SAFE_REPAIR_PROPOSAL_LOOP_FLAG_NAMES = (
    "ready_for_v0388_cli_repair_proposal_surface",
    "ready_for_v0389_bounded_repair_proposal_loop_consolidation",
    "ready_for_v039_human_approved_sandbox_repair_apply",
    "ready_for_bounded_repair_proposal_loop_trial",
    "ready_for_one_shot_loop_packet",
    "ready_for_loop_artifact_bundle",
    "ready_for_loop_step_records",
    "ready_for_loop_boundary_audit",
    "ready_for_loop_stop_condition",
    "ready_for_loop_do_nothing_comparison",
    "ready_for_loop_decision",
    "ready_for_loop_human_handoff",
    "ready_for_future_cli_repair_proposal_surface_input",
    "ready_for_future_v0389_consolidation_input",
    "ready_for_future_v039_apply_handoff_metadata",
)

UNSAFE_REPAIR_PROPOSAL_LOOP_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_autonomous_loop_runtime",
    "ready_for_multi_cycle_loop",
    "ready_for_retry_loop",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
    "ready_for_human_approval_capture",
    "ready_for_approval_grant",
    "ready_for_apply_permission",
    "ready_for_loop_packet_file_write",
    "ready_for_loop_packet_external_send",
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
    "ready_for_new_proposed_diff_generation",
    "ready_for_new_proposed_code_hunk_generation",
    "ready_for_new_proposed_patch_envelope_generation",
    "ready_for_repair_apply",
    "ready_for_sandbox_repair_apply",
    "ready_for_repair_loop",
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

UNSAFE_REPAIR_PROPOSAL_LOOP_POLICY_ALLOW_NAMES = (
    "allow_autonomous_loop_runtime",
    "allow_multi_cycle_loop",
    "allow_retry_loop",
    "allow_automatic_repair",
    "allow_human_approval_capture",
    "allow_approval_grant",
    "allow_apply_permission",
    "allow_loop_packet_file_write",
    "allow_loop_packet_external_send",
    "allow_ui_runtime",
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_source_file_write",
    "allow_patch_file_write",
    "allow_new_proposed_diff_generation",
    "allow_new_proposed_code_hunk_generation",
    "allow_new_proposed_patch_envelope_generation",
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

UNSAFE_LOOP_STEP_STATE_NAMES = (
    "executed_runtime_action",
    "performed_source_read",
    "generated_new_patch_metadata",
    "wrote_file",
    "applied_patch",
    "ran_tests",
    "invoked_model",
    "invoked_external_agent",
)

UNSAFE_LOOP_DECISION_NOW_NAMES = (
    "autonomous_loop_allowed_now",
    "retry_allowed_now",
    "multi_cycle_allowed_now",
    "approval_capture_allowed_now",
    "approval_grant_allowed_now",
    "apply_permission_allowed_now",
    "source_read_allowed_now",
    "new_patch_generation_allowed_now",
    "file_write_allowed_now",
    "patch_application_allowed_now",
    "repair_execution_allowed_now",
    "test_execution_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
    "production_certified",
)

UNSAFE_LOOP_PACKET_STATE_NAMES = (
    "human_approval_present",
    "approval_granted",
    "approval_captured_now",
    "apply_allowed",
    "sandbox_apply_allowed",
    "live_apply_allowed",
    "autonomous_loop_started",
    "retry_performed",
    "multi_cycle_performed",
    "source_read_performed_by_v0387",
    "new_patch_metadata_generated_by_v0387",
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
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
)

REQUIRED_REPAIR_PROPOSAL_LOOP_PROHIBITED_ACTIONS = (
    "autonomous_loop",
    "multi_cycle_loop",
    "retry_loop",
    "approval_capture",
    "approval_grant",
    "apply_permission",
    "source_read",
    "new_patch_generation",
    "file_write",
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

REQUIRED_LOOP_ARTIFACT_KEYS = (
    "evidence_bundle_id",
    "source_context_snapshot_id",
    "scope_plan_id",
    "proposed_patch_envelope_id",
    "safety_report_id",
    "human_review_packet_id",
    "approval_request_contract_id",
)


class RepairProposalLoopMode(StrEnum):
    ONE_SHOT_LOOP_TRIAL = "one_shot_loop_trial"
    LOOP_ARTIFACT_BUNDLE = "loop_artifact_bundle"
    LOOP_STEP_RECORDS = "loop_step_records"
    LOOP_BOUNDARY_AUDIT = "loop_boundary_audit"
    LOOP_STOP_CONDITION = "loop_stop_condition"
    LOOP_DO_NOTHING_COMPARISON = "loop_do_nothing_comparison"
    LOOP_DECISION = "loop_decision"
    FUTURE_CLI_SURFACE_INPUT = "future_cli_surface_input"
    FUTURE_CONSOLIDATION_INPUT = "future_consolidation_input"
    FUTURE_V039_HANDOFF_METADATA = "future_v039_handoff_metadata"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairProposalLoopSourceKind(StrEnum):
    V0386_HUMAN_REVIEW_PACKET = "v0386_human_review_packet"
    V0386_APPROVAL_REQUEST_CONTRACT = "v0386_approval_request_contract"
    V0386_HUMAN_REVIEW_DECISION = "v0386_human_review_decision"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0385_SAFETY_DECISION = "v0385_safety_decision"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0384_PROPOSED_DIFF_METADATA = "v0384_proposed_diff_metadata"
    V0384_PROPOSED_CODE_HUNK = "v0384_proposed_code_hunk"
    V0383_REPAIR_SCOPE_PLAN = "v0383_repair_scope_plan"
    V0383_REPAIR_CHANGE_INTENT = "v0383_repair_change_intent"
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0381_ELIGIBILITY_DECISION = "v0381_eligibility_decision"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairProposalLoopStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    ARTIFACT_BUNDLE_CREATED = "artifact_bundle_created"
    STEP_RECORDS_CREATED = "step_records_created"
    ONE_SHOT_LOOP_PACKET_CREATED = "one_shot_loop_packet_created"
    ONE_SHOT_LOOP_PACKET_CREATED_WITH_WARNINGS = "one_shot_loop_packet_created_with_warnings"
    STOPPED_AFTER_ONE_CYCLE = "stopped_after_one_cycle"
    HUMAN_HANDOFF_REQUIRED = "human_handoff_required"
    READY_FOR_FUTURE_CLI_SURFACE = "ready_for_future_cli_surface"
    READY_FOR_FUTURE_CONSOLIDATION = "ready_for_future_consolidation"
    FUTURE_V039_HANDOFF_PREPARED = "future_v039_handoff_prepared"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairProposalLoopReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    LOOP_TRIAL_CONTRACT_READY = "loop_trial_contract_ready"
    ARTIFACT_BUNDLE_READY = "artifact_bundle_ready"
    STEP_RECORDS_READY = "step_records_ready"
    BOUNDARY_AUDIT_READY = "boundary_audit_ready"
    STOP_CONDITION_READY = "stop_condition_ready"
    DO_NOTHING_LOOP_COMPARISON_READY = "do_nothing_loop_comparison_ready"
    ONE_SHOT_LOOP_PACKET_READY = "one_shot_loop_packet_ready"
    FUTURE_CLI_SURFACE_INPUT_READY = "future_cli_surface_input_ready"
    FUTURE_CONSOLIDATION_INPUT_READY = "future_consolidation_input_ready"
    FUTURE_V039_HANDOFF_METADATA_READY = "future_v039_handoff_metadata_ready"
    DESIGN_HANDOFF_READY_FOR_V0388 = "design_handoff_ready_for_v0388"
    DESIGN_HANDOFF_READY_FOR_V0389 = "design_handoff_ready_for_v0389"
    FUTURE_HANDOFF_READY_FOR_V039 = "future_handoff_ready_for_v039"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairProposalLoopDecisionKind(StrEnum):
    ALLOW_ONE_SHOT_LOOP_PACKET = "allow_one_shot_loop_packet"
    ALLOW_ARTIFACT_BUNDLE = "allow_artifact_bundle"
    ALLOW_STEP_RECORDS = "allow_step_records"
    ALLOW_BOUNDARY_AUDIT = "allow_boundary_audit"
    ALLOW_STOP_CONDITION = "allow_stop_condition"
    ALLOW_DO_NOTHING_COMPARISON = "allow_do_nothing_comparison"
    ALLOW_FUTURE_CLI_SURFACE_INPUT = "allow_future_cli_surface_input"
    ALLOW_FUTURE_CONSOLIDATION_INPUT = "allow_future_consolidation_input"
    ALLOW_FUTURE_V039_HANDOFF_METADATA = "allow_future_v039_handoff_metadata"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW_REQUIRED = "choose_human_review_required"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    MISSING_REQUIRED_ARTIFACT = "missing_required_artifact"
    SAFETY_BLOCKED = "safety_blocked"
    APPROVAL_ABSENT = "approval_absent"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairProposalLoopRiskKind(StrEnum):
    MISSING_HUMAN_REVIEW_PACKET_RISK = "missing_human_review_packet_risk"
    MISSING_SAFETY_REPORT_RISK = "missing_safety_report_risk"
    MISSING_PATCH_ENVELOPE_RISK = "missing_patch_envelope_risk"
    MISSING_SCOPE_PLAN_RISK = "missing_scope_plan_risk"
    MISSING_SOURCE_CONTEXT_RISK = "missing_source_context_risk"
    MISSING_EVIDENCE_BUNDLE_RISK = "missing_evidence_bundle_risk"
    MISSING_STOP_REASON_RISK = "missing_stop_reason_risk"
    MISSING_DO_NOTHING_COMPARISON_RISK = "missing_do_nothing_comparison_risk"
    APPROVAL_CONFUSION_RISK = "approval_confusion_risk"
    APPLY_PERMISSION_CONFUSION_RISK = "apply_permission_confusion_risk"
    LOOP_EXECUTION_CONFUSION_RISK = "loop_execution_confusion_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    TEST_EXECUTION_CONFUSION_RISK = "test_execution_confusion_risk"
    NEW_SOURCE_READ_CONFUSION_RISK = "new_source_read_confusion_risk"
    NEW_PATCH_GENERATION_CONFUSION_RISK = "new_patch_generation_confusion_risk"
    FILE_WRITE_RISK = "file_write_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    EXTERNAL_SEND_RISK = "external_send_risk"
    UI_RUNTIME_RISK = "ui_runtime_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairProposalLoopStepKind(StrEnum):
    EVIDENCE_CONTRACT_STEP = "evidence_contract_step"
    SOURCE_CONTEXT_STEP = "source_context_step"
    SCOPE_PLANNING_STEP = "scope_planning_step"
    PATCH_METADATA_STEP = "patch_metadata_step"
    SAFETY_VALIDATION_STEP = "safety_validation_step"
    HUMAN_REVIEW_PACKET_STEP = "human_review_packet_step"
    DO_NOTHING_COMPARISON_STEP = "do_nothing_comparison_step"
    STOP_CONDITION_STEP = "stop_condition_step"
    HUMAN_HANDOFF_STEP = "human_handoff_step"
    FUTURE_CLI_SURFACE_HANDOFF_STEP = "future_cli_surface_handoff_step"
    FUTURE_CONSOLIDATION_HANDOFF_STEP = "future_consolidation_handoff_step"
    FUTURE_V039_HANDOFF_STEP = "future_v039_handoff_step"
    UNKNOWN = "unknown"


class RepairProposalLoopStepStatus(StrEnum):
    NOT_STARTED = "not_started"
    ARTIFACT_PRESENT = "artifact_present"
    ARTIFACT_MISSING = "artifact_missing"
    ARTIFACT_INVALID = "artifact_invalid"
    COMPLETED_AS_METADATA = "completed_as_metadata"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    SKIPPED = "skipped"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairProposalLoopStopReasonKind(StrEnum):
    STOPPED_AFTER_ONE_CYCLE = "stopped_after_one_cycle"
    STOPPED_FOR_HUMAN_HANDOFF = "stopped_for_human_handoff"
    STOPPED_DUE_TO_MISSING_ARTIFACT = "stopped_due_to_missing_artifact"
    STOPPED_DUE_TO_SAFETY_BLOCK = "stopped_due_to_safety_block"
    STOPPED_DUE_TO_DO_NOTHING_PREFERRED = "stopped_due_to_do_nothing_preferred"
    STOPPED_DUE_TO_NO_APPROVAL = "stopped_due_to_no_approval"
    STOPPED_DUE_TO_POLICY = "stopped_due_to_policy"
    STOPPED_DUE_TO_FUTURE_GATE = "stopped_due_to_future_gate"
    STOPPED_DUE_TO_REVIEW_REQUIRED = "stopped_due_to_review_required"
    UNKNOWN = "unknown"


class RepairProposalLoopOutcomeKind(StrEnum):
    ONE_SHOT_PACKET_READY = "one_shot_packet_ready"
    ONE_SHOT_PACKET_READY_WITH_WARNINGS = "one_shot_packet_ready_with_warnings"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    FUTURE_CLI_SURFACE_READY = "future_cli_surface_ready"
    FUTURE_CONSOLIDATION_READY = "future_consolidation_ready"
    FUTURE_V039_HANDOFF_METADATA_READY = "future_v039_handoff_metadata_ready"
    UNKNOWN = "unknown"


class RepairProposalLoopDisposition(StrEnum):
    TRIAL_READY = "trial_ready"
    TRIAL_READY_WITH_WARNINGS = "trial_ready_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    FUTURE_GATED = "future_gated"
    UNKNOWN = "unknown"


class RepairProposalLoopConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairProposalLoopDoNothingComparisonKind(StrEnum):
    DO_NOTHING_PREFERRED_DUE_TO_SAFETY = "do_nothing_preferred_due_to_safety"
    DO_NOTHING_PREFERRED_DUE_TO_REVIEW_GAP = "do_nothing_preferred_due_to_review_gap"
    DO_NOTHING_PREFERRED_DUE_TO_MISSING_ARTIFACT = "do_nothing_preferred_due_to_missing_artifact"
    DO_NOTHING_COMPETITIVE = "do_nothing_competitive"
    LOOP_PACKET_BETTER_THAN_DO_NOTHING = "loop_packet_better_than_do_nothing"
    DO_NOTHING_REQUIRED_DUE_TO_BLOCKING_ISSUE = "do_nothing_required_due_to_blocking_issue"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
    UNKNOWN = "unknown"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0387_VERSION not in version:
        raise ValueError("version must include v0.38.7")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name):
            raise ValueError(f"{name} must remain False for {V0387_VERSION}")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if not getattr(instance, name):
            raise ValueError(f"{name} must remain True for {V0387_VERSION}")


def _source_id_from(value: Any, fallback: str | None = None) -> str | None:
    if value is None:
        return fallback
    if isinstance(value, str):
        return value or fallback
    if isinstance(value, dict):
        for key in (
            "id",
            "source_id",
            "artifact_id",
            "human_review_packet_id",
            "approval_request_contract_id",
            "safety_report_id",
            "proposed_patch_envelope_id",
            "scope_plan_id",
            "source_context_snapshot_id",
            "evidence_bundle_id",
        ):
            found = value.get(key)
            if found:
                return str(found)
        return fallback
    candidate_names = (
        "human_review_packet_id",
        "approval_request_contract_id",
        "safety_report_id",
        "proposed_patch_envelope_id",
        "scope_plan_id",
        "source_context_snapshot_id",
        "evidence_bundle_id",
        "repair_proposal_evidence_bundle_id",
        "repair_scope_plan_id",
        "repair_source_context_snapshot_id",
    )
    for name in candidate_names:
        found = getattr(value, name, None)
        if found:
            return str(found)
    return fallback


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopFlagSet:
    flag_set_id: str
    version: str
    repair_proposal_loop_trial_layer_constructed: bool = True
    one_shot_loop_trial_available: bool = True
    loop_artifact_bundle_available: bool = True
    loop_step_records_available: bool = True
    loop_boundary_audit_available: bool = True
    loop_stop_condition_available: bool = True
    loop_do_nothing_comparison_available: bool = True
    loop_decision_available: bool = True
    loop_human_handoff_available: bool = True
    ready_for_v0388_cli_repair_proposal_surface: bool = True
    ready_for_v0389_bounded_repair_proposal_loop_consolidation: bool = True
    ready_for_v039_human_approved_sandbox_repair_apply: bool = True
    ready_for_bounded_repair_proposal_loop_trial: bool = True
    ready_for_one_shot_loop_packet: bool = True
    ready_for_loop_artifact_bundle: bool = True
    ready_for_loop_step_records: bool = True
    ready_for_loop_boundary_audit: bool = True
    ready_for_loop_stop_condition: bool = True
    ready_for_loop_do_nothing_comparison: bool = True
    ready_for_loop_decision: bool = True
    ready_for_loop_human_handoff: bool = True
    ready_for_future_cli_repair_proposal_surface_input: bool = True
    ready_for_future_v0389_consolidation_input: bool = True
    ready_for_future_v039_apply_handoff_metadata: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_retry_loop: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_execution: bool = False
    ready_for_human_approval_capture: bool = False
    ready_for_approval_grant: bool = False
    ready_for_apply_permission: bool = False
    ready_for_loop_packet_file_write: bool = False
    ready_for_loop_packet_external_send: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_source_file_read: bool = False
    ready_for_sandbox_source_read: bool = False
    ready_for_live_workspace_read: bool = False
    ready_for_unbounded_source_read: bool = False
    ready_for_reference_source_read: bool = False
    ready_for_secret_read: bool = False
    ready_for_source_file_write: bool = False
    ready_for_sandbox_source_write: bool = False
    ready_for_patch_file_write: bool = False
    ready_for_file_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_applied_diff_generation: bool = False
    ready_for_applied_code_hunk_generation: bool = False
    ready_for_new_proposed_diff_generation: bool = False
    ready_for_new_proposed_code_hunk_generation: bool = False
    ready_for_new_proposed_patch_envelope_generation: bool = False
    ready_for_repair_apply: bool = False
    ready_for_sandbox_repair_apply: bool = False
    ready_for_repair_loop: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_tool_execution: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_REPAIR_PROPOSAL_LOOP_FLAG_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopSourceRef:
    source_ref_id: str
    source_kind: RepairProposalLoopSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopPolicy:
    loop_policy_id: str
    version: str
    allowed_modes: list[RepairProposalLoopMode | str]
    required_step_kinds: list[RepairProposalLoopStepKind | str]
    required_stop_reasons: list[RepairProposalLoopStopReasonKind | str]
    max_cycle_count: int = 1
    max_retry_count: int = 0
    require_evidence_bundle: bool = True
    require_source_context_snapshot: bool = True
    require_scope_plan: bool = True
    require_patch_envelope: bool = True
    require_safety_report: bool = True
    require_human_review_packet: bool = True
    require_do_nothing_comparison: bool = True
    require_stop_reason: bool = True
    require_human_handoff: bool = True
    allow_one_shot_loop_packet: bool = True
    allow_loop_artifact_bundle: bool = True
    allow_loop_step_records: bool = True
    allow_loop_boundary_audit: bool = True
    allow_loop_stop_condition: bool = True
    allow_loop_do_nothing_comparison: bool = True
    allow_future_cli_surface_input: bool = True
    allow_future_consolidation_input: bool = True
    allow_future_v039_handoff_metadata: bool = True
    allow_autonomous_loop_runtime: bool = False
    allow_multi_cycle_loop: bool = False
    allow_retry_loop: bool = False
    allow_automatic_repair: bool = False
    allow_human_approval_capture: bool = False
    allow_approval_grant: bool = False
    allow_apply_permission: bool = False
    allow_loop_packet_file_write: bool = False
    allow_loop_packet_external_send: bool = False
    allow_ui_runtime: bool = False
    allow_source_file_read: bool = False
    allow_sandbox_source_read: bool = False
    allow_source_file_write: bool = False
    allow_patch_file_write: bool = False
    allow_new_proposed_diff_generation: bool = False
    allow_new_proposed_code_hunk_generation: bool = False
    allow_new_proposed_patch_envelope_generation: bool = False
    allow_file_edit: bool = False
    allow_patch_application: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_repair_execution: bool = False
    allow_test_execution: bool = False
    allow_subprocess: bool = False
    allow_shell: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_model_provider_invocation: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_policy_id", self.loop_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        _validate_list("required_step_kinds", self.required_step_kinds)
        _validate_list("required_stop_reasons", self.required_stop_reasons)
        if self.max_cycle_count != 1:
            raise ValueError("max_cycle_count must be exactly 1")
        if self.max_retry_count != 0:
            raise ValueError("max_retry_count must be exactly 0")
        _validate_false(self, UNSAFE_REPAIR_PROPOSAL_LOOP_POLICY_ALLOW_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopInput:
    loop_input_id: str
    version: str
    human_review_packet_id: str | None = None
    approval_request_contract_id: str | None = None
    safety_report_id: str | None = None
    proposed_patch_envelope_id: str | None = None
    scope_plan_id: str | None = None
    source_context_snapshot_id: str | None = None
    evidence_bundle_id: str | None = None
    requested_mode: RepairProposalLoopMode | str = RepairProposalLoopMode.ONE_SHOT_LOOP_TRIAL
    source_refs: list[RepairProposalLoopSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(
        default_factory=lambda: list(REQUIRED_REPAIR_PROPOSAL_LOOP_PROHIBITED_ACTIONS)
    )
    task_summary: str = "Create bounded one-shot repair proposal loop trial packet metadata."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_input_id", self.loop_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = set(REQUIRED_REPAIR_PROPOSAL_LOOP_PROHIBITED_ACTIONS) - set(self.prohibited_runtime_actions)
        if missing:
            raise ValueError(f"prohibited_runtime_actions missing required actions: {sorted(missing)}")


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopArtifactBundle:
    artifact_bundle_id: str
    version: str
    evidence_bundle_id: str | None = None
    source_context_snapshot_id: str | None = None
    scope_plan_id: str | None = None
    proposed_patch_envelope_id: str | None = None
    safety_report_id: str | None = None
    human_review_packet_id: str | None = None
    approval_request_contract_id: str | None = None
    present_artifacts: list[str] = field(default_factory=list)
    missing_artifacts: list[str] = field(default_factory=list)
    invalid_artifacts: list[str] = field(default_factory=list)
    bundle_summary: str = "Existing repair proposal artifacts assembled for one-shot loop trial metadata."
    complete_for_one_shot_trial: bool = False
    complete_for_future_cli_surface: bool = False
    complete_for_future_v039_handoff_metadata: bool = False
    source_refs: list[RepairProposalLoopSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("artifact_bundle_id", self.artifact_bundle_id)
        _validate_version(self.version)
        _require_non_blank("bundle_summary", self.bundle_summary)
        _validate_string_list("present_artifacts", self.present_artifacts)
        _validate_string_list("missing_artifacts", self.missing_artifacts)
        _validate_string_list("invalid_artifacts", self.invalid_artifacts)
        _validate_list("source_refs", self.source_refs)
        has_gaps = bool(self.missing_artifacts or self.invalid_artifacts)
        if has_gaps and (
            self.complete_for_one_shot_trial
            or self.complete_for_future_cli_surface
            or self.complete_for_future_v039_handoff_metadata
        ):
            raise ValueError("complete flags must remain False when required artifacts are missing or invalid")


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopStepRecord:
    loop_step_id: str
    step_kind: RepairProposalLoopStepKind | str
    step_status: RepairProposalLoopStepStatus | str
    artifact_ref_id: str | None = None
    step_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    completed_as_metadata: bool = True
    executed_runtime_action: bool = False
    performed_source_read: bool = False
    generated_new_patch_metadata: bool = False
    wrote_file: bool = False
    applied_patch: bool = False
    ran_tests: bool = False
    invoked_model: bool = False
    invoked_external_agent: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_step_id", self.loop_step_id)
        _require_non_blank("step_summary", self.step_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_LOOP_STEP_STATE_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopBoundaryAudit:
    boundary_audit_id: str
    version: str
    audit_summary: str
    checked_step_ids: list[str] = field(default_factory=list)
    risk_kinds: list[RepairProposalLoopRiskKind | str] = field(default_factory=list)
    approval_absent_confirmed: bool = True
    no_apply_permission_confirmed: bool = True
    no_source_read_confirmed: bool = True
    no_new_patch_generation_confirmed: bool = True
    no_file_write_confirmed: bool = True
    no_patch_apply_confirmed: bool = True
    no_repair_execution_confirmed: bool = True
    no_test_execution_confirmed: bool = True
    no_model_invocation_confirmed: bool = True
    no_external_agent_confirmed: bool = True
    no_dominion_runtime_confirmed: bool = True
    no_production_certification_confirmed: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_audit_id", self.boundary_audit_id)
        _validate_version(self.version)
        _require_non_blank("audit_summary", self.audit_summary)
        _validate_string_list("checked_step_ids", self.checked_step_ids)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_true(
            self,
            (
                "approval_absent_confirmed",
                "no_apply_permission_confirmed",
                "no_source_read_confirmed",
                "no_new_patch_generation_confirmed",
                "no_file_write_confirmed",
                "no_patch_apply_confirmed",
                "no_repair_execution_confirmed",
                "no_test_execution_confirmed",
                "no_model_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ),
        )


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopStopCondition:
    stop_condition_id: str
    stop_reason_kind: RepairProposalLoopStopReasonKind | str
    stop_summary: str
    cycle_count_at_stop: int = 1
    retry_count_at_stop: int = 0
    human_handoff_required: bool = True
    approval_absent: bool = True
    apply_not_allowed: bool = True
    repair_not_executed: bool = True
    tests_not_run: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("stop_condition_id", self.stop_condition_id)
        _require_non_blank("stop_summary", self.stop_summary)
        _validate_non_negative("cycle_count_at_stop", self.cycle_count_at_stop)
        _validate_non_negative("retry_count_at_stop", self.retry_count_at_stop)
        if self.cycle_count_at_stop > 1:
            raise ValueError("cycle_count_at_stop must be <= 1")
        if self.retry_count_at_stop != 0:
            raise ValueError("retry_count_at_stop must be 0")
        _validate_true(
            self,
            (
                "human_handoff_required",
                "approval_absent",
                "apply_not_allowed",
                "repair_not_executed",
                "tests_not_run",
            ),
        )
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopDoNothingComparison:
    loop_do_nothing_comparison_id: str
    comparison_kind: RepairProposalLoopDoNothingComparisonKind | str
    comparison_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    do_nothing_remains_valid: bool = True
    do_nothing_preferred: bool = False
    do_nothing_required: bool = False
    loop_packet_outperforms_do_nothing: bool = False
    confidence: RepairProposalLoopConfidenceLevel | str = RepairProposalLoopConfidenceLevel.MEDIUM
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_do_nothing_comparison_id", self.loop_do_nothing_comparison_id)
        _require_non_blank("comparison_summary", self.comparison_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopDecision:
    loop_decision_id: str
    decision_kind: RepairProposalLoopDecisionKind | str
    disposition: RepairProposalLoopDisposition | str
    outcome_kind: RepairProposalLoopOutcomeKind | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairProposalLoopConfidenceLevel | str = RepairProposalLoopConfidenceLevel.MEDIUM
    evidence_refs: list[str] = field(default_factory=list)
    ready_for_future_cli_surface_input: bool = False
    ready_for_future_consolidation_input: bool = False
    ready_for_future_v039_handoff_metadata: bool = False
    autonomous_loop_allowed_now: bool = False
    retry_allowed_now: bool = False
    multi_cycle_allowed_now: bool = False
    approval_capture_allowed_now: bool = False
    approval_grant_allowed_now: bool = False
    apply_permission_allowed_now: bool = False
    source_read_allowed_now: bool = False
    new_patch_generation_allowed_now: bool = False
    file_write_allowed_now: bool = False
    patch_application_allowed_now: bool = False
    repair_execution_allowed_now: bool = False
    test_execution_allowed_now: bool = False
    model_provider_invocation_allowed_now: bool = False
    external_agent_allowed_now: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_decision_id", self.loop_decision_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _require_non_blank("rationale_summary", self.rationale_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_LOOP_DECISION_NOW_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopPacket:
    loop_packet_id: str
    version: str
    loop_input_id: str
    status: RepairProposalLoopStatus | str
    readiness_level: RepairProposalLoopReadinessLevel | str
    disposition: RepairProposalLoopDisposition | str
    outcome_kind: RepairProposalLoopOutcomeKind | str
    artifact_bundle: RepairProposalLoopArtifactBundle
    step_records: list[RepairProposalLoopStepRecord]
    boundary_audit: RepairProposalLoopBoundaryAudit
    stop_condition: RepairProposalLoopStopCondition
    do_nothing_comparison: RepairProposalLoopDoNothingComparison
    loop_decision: RepairProposalLoopDecision
    source_refs: list[RepairProposalLoopSourceRef] = field(default_factory=list)
    packet_summary: str = "Bounded one-shot repair proposal loop trial packet metadata."
    rendered_packet_preview: str = "One-shot loop packet preview; metadata only."
    max_cycle_count: int = 1
    actual_cycle_count: int = 1
    retry_count: int = 0
    bounded: bool = True
    redacted: bool = True
    ready_for_future_cli_surface_input: bool = False
    ready_for_future_consolidation_input: bool = False
    ready_for_future_v039_handoff_metadata: bool = False
    human_handoff_required: bool = True
    human_approval_present: bool = False
    approval_granted: bool = False
    approval_captured_now: bool = False
    apply_allowed: bool = False
    sandbox_apply_allowed: bool = False
    live_apply_allowed: bool = False
    autonomous_loop_started: bool = False
    retry_performed: bool = False
    multi_cycle_performed: bool = False
    source_read_performed_by_v0387: bool = False
    new_patch_metadata_generated_by_v0387: bool = False
    file_write_performed: bool = False
    patch_file_written: bool = False
    file_edit_performed: bool = False
    patch_applied: bool = False
    apply_patch_called: bool = False
    git_apply_called: bool = False
    tests_run: bool = False
    repair_executed: bool = False
    model_invocation_performed: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_packet_id", self.loop_packet_id)
        _validate_version(self.version)
        _require_non_blank("loop_input_id", self.loop_input_id)
        _require_non_blank("packet_summary", self.packet_summary)
        _require_non_blank("rendered_packet_preview", self.rendered_packet_preview)
        _validate_list("step_records", self.step_records)
        _validate_list("source_refs", self.source_refs)
        if self.max_cycle_count != 1:
            raise ValueError("max_cycle_count must be 1")
        if self.actual_cycle_count > 1:
            raise ValueError("actual_cycle_count must be <= 1")
        if self.retry_count != 0:
            raise ValueError("retry_count must be 0")
        if not self.bounded:
            raise ValueError("bounded must be True")
        if not self.human_handoff_required:
            raise ValueError("human_handoff_required must be True")
        _validate_false(self, UNSAFE_LOOP_PACKET_STATE_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopValidationFinding:
    validation_finding_id: str
    finding_summary: str
    severity: RepairProposalLoopDisposition | str = RepairProposalLoopDisposition.REVIEW_REQUIRED
    evidence_refs: list[str] = field(default_factory=list)
    blocks_loop_packet: bool = False
    blocks_future_cli_surface_input: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_finding_id", self.validation_finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopValidationReport:
    validation_report_id: str
    version: str
    report_summary: str
    findings: list[RepairProposalLoopValidationFinding] = field(default_factory=list)
    confirms_one_shot_only: bool = True
    confirms_max_cycle_one: bool = True
    confirms_retry_zero: bool = True
    confirms_stop_condition: bool = True
    confirms_human_handoff: bool = True
    confirms_no_approval: bool = True
    confirms_no_apply: bool = True
    confirms_no_source_read: bool = True
    confirms_no_new_patch_generation: bool = True
    confirms_no_file_write: bool = True
    confirms_no_external_send: bool = True
    confirms_no_ui_runtime: bool = True
    confirms_no_patch_apply: bool = True
    confirms_no_repair_execution: bool = True
    confirms_no_tests: bool = True
    confirms_no_external_calls: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("report_summary", self.report_summary)
        _validate_list("findings", self.findings)
        _validate_true(
            self,
            (
                "confirms_one_shot_only",
                "confirms_max_cycle_one",
                "confirms_retry_zero",
                "confirms_stop_condition",
                "confirms_human_handoff",
                "confirms_no_approval",
                "confirms_no_apply",
                "confirms_no_source_read",
                "confirms_no_new_patch_generation",
                "confirms_no_file_write",
                "confirms_no_external_send",
                "confirms_no_ui_runtime",
                "confirms_no_patch_apply",
                "confirms_no_repair_execution",
                "confirms_no_tests",
                "confirms_no_external_calls",
            ),
        )


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopReport:
    loop_report_id: str
    version: str
    loop_packet_id: str
    report_summary: str
    validation_report: RepairProposalLoopValidationReport
    ready_for_future_cli_surface_input: bool = False
    ready_for_future_consolidation_input: bool = False
    ready_for_future_v039_handoff_metadata: bool = False
    ready_for_execution: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("loop_report_id", self.loop_report_id)
        _validate_version(self.version)
        _require_non_blank("loop_packet_id", self.loop_packet_id)
        _require_non_blank("report_summary", self.report_summary)
        if self.ready_for_execution:
            raise ValueError("ready_for_execution must remain False")
        if self.production_certified:
            raise ValueError("production_certified must remain False")


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopRunPreview:
    run_preview_id: str
    version: str
    preview_summary: str
    max_cycle_count: int = 1
    retry_count: int = 0
    would_start_autonomous_loop: bool = False
    would_apply_patch: bool = False
    would_run_tests: bool = False
    would_invoke_external_systems: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        if self.max_cycle_count != 1:
            raise ValueError("max_cycle_count must be 1")
        if self.retry_count != 0:
            raise ValueError("retry_count must be 0")
        _validate_false(
            self,
            (
                "would_start_autonomous_loop",
                "would_apply_patch",
                "would_run_tests",
                "would_invoke_external_systems",
            ),
        )


@dataclass(frozen=True, kw_only=True)
class RepairProposalLoopNoExecutionGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_autonomous_loop: bool = True
    no_retry: bool = True
    no_multi_cycle: bool = True
    no_approval: bool = True
    no_apply: bool = True
    no_source_read: bool = True
    no_new_patch_generation: bool = True
    no_file_write: bool = True
    no_external_send: bool = True
    no_ui: bool = True
    no_patch_apply: bool = True
    no_repair: bool = True
    no_test: bool = True
    no_external_call: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_true(
            self,
            (
                "no_autonomous_loop",
                "no_retry",
                "no_multi_cycle",
                "no_approval",
                "no_apply",
                "no_source_read",
                "no_new_patch_generation",
                "no_file_write",
                "no_external_send",
                "no_ui",
                "no_patch_apply",
                "no_repair",
                "no_test",
                "no_external_call",
            ),
        )


@dataclass(frozen=True, kw_only=True)
class V0387ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str = V0387_RELEASE_NAME
    flags: RepairProposalLoopFlagSet
    no_execution_guarantee: RepairProposalLoopNoExecutionGuarantee
    readiness_summary: str = "v0.38.7 one-shot loop trial metadata is ready for v0.38.8/v0.38.9 handoff metadata."
    ready_for_v0388_cli_repair_proposal_surface: bool = True
    ready_for_v0389_bounded_repair_proposal_loop_consolidation: bool = True
    ready_for_v039_human_approved_sandbox_repair_apply: bool = True
    ready_for_bounded_repair_proposal_loop_trial: bool = True
    ready_for_execution: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("readiness_summary", self.readiness_summary)
        if self.ready_for_execution:
            raise ValueError("ready_for_execution must remain False")
        if self.production_certified:
            raise ValueError("production_certified must remain False")


def build_repair_proposal_loop_flags(**kwargs: Any) -> RepairProposalLoopFlagSet:
    defaults = {
        "flag_set_id": "v0387-loop-flags",
        "version": V0387_VERSION,
        "metadata": {
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
            "one_shot_loop_trial_only": True,
            "no_independent_autonomous_agent_runtime": True,
            "mandatory_stop_after_one_cycle": True,
            "mandatory_human_handoff_before_any_apply": True,
        },
    }
    defaults.update(kwargs)
    return RepairProposalLoopFlagSet(**defaults)


def build_repair_proposal_loop_source_ref(**kwargs: Any) -> RepairProposalLoopSourceRef:
    defaults = {
        "source_ref_id": "v0387-source-ref",
        "source_kind": RepairProposalLoopSourceKind.TEST_FIXTURE,
        "source_id": "fixture-source",
        "source_summary": "Existing metadata source reference; no file read or execution.",
        "evidence_refs": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopSourceRef(**defaults)


def build_repair_proposal_loop_policy(**kwargs: Any) -> RepairProposalLoopPolicy:
    defaults = {
        "loop_policy_id": "v0387-loop-policy",
        "version": V0387_VERSION,
        "allowed_modes": [
            RepairProposalLoopMode.ONE_SHOT_LOOP_TRIAL,
            RepairProposalLoopMode.LOOP_ARTIFACT_BUNDLE,
            RepairProposalLoopMode.LOOP_STEP_RECORDS,
            RepairProposalLoopMode.LOOP_BOUNDARY_AUDIT,
            RepairProposalLoopMode.LOOP_STOP_CONDITION,
            RepairProposalLoopMode.LOOP_DO_NOTHING_COMPARISON,
            RepairProposalLoopMode.LOOP_DECISION,
            RepairProposalLoopMode.FUTURE_CLI_SURFACE_INPUT,
            RepairProposalLoopMode.FUTURE_CONSOLIDATION_INPUT,
            RepairProposalLoopMode.FUTURE_V039_HANDOFF_METADATA,
        ],
        "required_step_kinds": [
            RepairProposalLoopStepKind.EVIDENCE_CONTRACT_STEP,
            RepairProposalLoopStepKind.SOURCE_CONTEXT_STEP,
            RepairProposalLoopStepKind.SCOPE_PLANNING_STEP,
            RepairProposalLoopStepKind.PATCH_METADATA_STEP,
            RepairProposalLoopStepKind.SAFETY_VALIDATION_STEP,
            RepairProposalLoopStepKind.HUMAN_REVIEW_PACKET_STEP,
            RepairProposalLoopStepKind.DO_NOTHING_COMPARISON_STEP,
            RepairProposalLoopStepKind.STOP_CONDITION_STEP,
            RepairProposalLoopStepKind.HUMAN_HANDOFF_STEP,
        ],
        "required_stop_reasons": [
            RepairProposalLoopStopReasonKind.STOPPED_AFTER_ONE_CYCLE,
            RepairProposalLoopStopReasonKind.STOPPED_FOR_HUMAN_HANDOFF,
        ],
        "metadata": {
            "policy_is_metadata_only": True,
            "max_cycle_count_required": 1,
            "max_retry_count_required": 0,
        },
    }
    defaults.update(kwargs)
    return RepairProposalLoopPolicy(**defaults)


def build_repair_proposal_loop_input(**kwargs: Any) -> RepairProposalLoopInput:
    defaults = {
        "loop_input_id": "v0387-loop-input",
        "version": V0387_VERSION,
        "requested_mode": RepairProposalLoopMode.ONE_SHOT_LOOP_TRIAL,
    }
    defaults.update(kwargs)
    return RepairProposalLoopInput(**defaults)


def build_repair_proposal_loop_artifact_bundle(**kwargs: Any) -> RepairProposalLoopArtifactBundle:
    ids = {key: kwargs.get(key) for key in REQUIRED_LOOP_ARTIFACT_KEYS}
    present = [key for key, value in ids.items() if value]
    missing = [key for key, value in ids.items() if not value]
    complete = not missing and not kwargs.get("invalid_artifacts")
    defaults = {
        "artifact_bundle_id": "v0387-artifact-bundle",
        "version": V0387_VERSION,
        "present_artifacts": present,
        "missing_artifacts": missing,
        "invalid_artifacts": [],
        "complete_for_one_shot_trial": complete,
        "complete_for_future_cli_surface": complete,
        "complete_for_future_v039_handoff_metadata": complete,
    }
    defaults.update(kwargs)
    return RepairProposalLoopArtifactBundle(**defaults)


def build_repair_proposal_loop_step_record(**kwargs: Any) -> RepairProposalLoopStepRecord:
    defaults = {
        "loop_step_id": "v0387-loop-step",
        "step_kind": RepairProposalLoopStepKind.EVIDENCE_CONTRACT_STEP,
        "step_status": RepairProposalLoopStepStatus.COMPLETED_AS_METADATA,
        "step_summary": "Loop step recorded as metadata only; no step execution performed.",
        "evidence_refs": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopStepRecord(**defaults)


def build_repair_proposal_loop_boundary_audit(**kwargs: Any) -> RepairProposalLoopBoundaryAudit:
    defaults = {
        "boundary_audit_id": "v0387-boundary-audit",
        "version": V0387_VERSION,
        "audit_summary": "Boundary audit confirms one-shot metadata-only loop packet posture.",
        "checked_step_ids": [],
        "risk_kinds": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopBoundaryAudit(**defaults)


def build_repair_proposal_loop_stop_condition(**kwargs: Any) -> RepairProposalLoopStopCondition:
    defaults = {
        "stop_condition_id": "v0387-stop-condition",
        "stop_reason_kind": RepairProposalLoopStopReasonKind.STOPPED_AFTER_ONE_CYCLE,
        "stop_summary": "Stopped after one metadata cycle with mandatory human handoff.",
        "cycle_count_at_stop": 1,
        "retry_count_at_stop": 0,
        "evidence_refs": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopStopCondition(**defaults)


def build_repair_proposal_loop_do_nothing_comparison(**kwargs: Any) -> RepairProposalLoopDoNothingComparison:
    defaults = {
        "loop_do_nothing_comparison_id": "v0387-do-nothing-comparison",
        "comparison_kind": RepairProposalLoopDoNothingComparisonKind.DO_NOTHING_COMPETITIVE,
        "comparison_summary": "Do-nothing remains valid while one-shot loop packet awaits human handoff.",
        "evidence_refs": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopDoNothingComparison(**defaults)


def build_repair_proposal_loop_decision(**kwargs: Any) -> RepairProposalLoopDecision:
    defaults = {
        "loop_decision_id": "v0387-loop-decision",
        "decision_kind": RepairProposalLoopDecisionKind.ALLOW_ONE_SHOT_LOOP_PACKET,
        "disposition": RepairProposalLoopDisposition.TRIAL_READY,
        "outcome_kind": RepairProposalLoopOutcomeKind.ONE_SHOT_PACKET_READY,
        "decision_summary": "Allow one-shot loop packet metadata and future handoff metadata only.",
        "rationale_summary": "Required artifacts and boundary confirmations support metadata handoff without execution.",
        "evidence_refs": [],
        "ready_for_future_cli_surface_input": True,
        "ready_for_future_consolidation_input": True,
        "ready_for_future_v039_handoff_metadata": True,
    }
    defaults.update(kwargs)
    return RepairProposalLoopDecision(**defaults)


def build_repair_proposal_loop_packet(**kwargs: Any) -> RepairProposalLoopPacket:
    bundle = kwargs.get("artifact_bundle") or build_repair_proposal_loop_artifact_bundle(
        evidence_bundle_id="evidence",
        source_context_snapshot_id="source-context",
        scope_plan_id="scope-plan",
        proposed_patch_envelope_id="patch-envelope",
        safety_report_id="safety-report",
        human_review_packet_id="review-packet",
        approval_request_contract_id="approval-contract",
    )
    steps = kwargs.get("step_records") or create_repair_proposal_loop_step_records(bundle)
    audit = kwargs.get("boundary_audit") or audit_repair_proposal_loop_boundaries(steps)
    stop = kwargs.get("stop_condition") or create_repair_proposal_loop_stop_condition()
    comparison = kwargs.get("do_nothing_comparison") or compare_repair_proposal_loop_to_do_nothing(bundle, audit)
    decision = kwargs.get("loop_decision") or decide_repair_proposal_loop(bundle, audit, comparison)
    defaults = {
        "loop_packet_id": "v0387-loop-packet",
        "version": V0387_VERSION,
        "loop_input_id": "v0387-loop-input",
        "status": RepairProposalLoopStatus.ONE_SHOT_LOOP_PACKET_CREATED,
        "readiness_level": RepairProposalLoopReadinessLevel.ONE_SHOT_LOOP_PACKET_READY,
        "disposition": decision.disposition,
        "outcome_kind": decision.outcome_kind,
        "artifact_bundle": bundle,
        "step_records": steps,
        "boundary_audit": audit,
        "stop_condition": stop,
        "do_nothing_comparison": comparison,
        "loop_decision": decision,
        "rendered_packet_preview": _render_loop_packet_preview(bundle, steps, stop, comparison, decision),
        "ready_for_future_cli_surface_input": decision.ready_for_future_cli_surface_input,
        "ready_for_future_consolidation_input": decision.ready_for_future_consolidation_input,
        "ready_for_future_v039_handoff_metadata": decision.ready_for_future_v039_handoff_metadata,
    }
    defaults.update(kwargs)
    return RepairProposalLoopPacket(**defaults)


def build_repair_proposal_loop_validation_finding(**kwargs: Any) -> RepairProposalLoopValidationFinding:
    defaults = {
        "validation_finding_id": "v0387-validation-finding",
        "finding_summary": "Loop packet validation finding metadata.",
        "evidence_refs": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopValidationFinding(**defaults)


def build_repair_proposal_loop_validation_report(**kwargs: Any) -> RepairProposalLoopValidationReport:
    defaults = {
        "validation_report_id": "v0387-validation-report",
        "version": V0387_VERSION,
        "report_summary": "Validation confirms one-shot loop packet boundaries and no execution posture.",
        "findings": [],
    }
    defaults.update(kwargs)
    return RepairProposalLoopValidationReport(**defaults)


def build_repair_proposal_loop_report(**kwargs: Any) -> RepairProposalLoopReport:
    validation_report = kwargs.get("validation_report") or build_repair_proposal_loop_validation_report()
    defaults = {
        "loop_report_id": "v0387-loop-report",
        "version": V0387_VERSION,
        "loop_packet_id": "v0387-loop-packet",
        "report_summary": "One-shot loop trial report metadata; no execution readiness.",
        "validation_report": validation_report,
        "ready_for_future_cli_surface_input": True,
        "ready_for_future_consolidation_input": True,
        "ready_for_future_v039_handoff_metadata": True,
    }
    defaults.update(kwargs)
    return RepairProposalLoopReport(**defaults)


def build_repair_proposal_loop_run_preview(**kwargs: Any) -> RepairProposalLoopRunPreview:
    defaults = {
        "run_preview_id": "v0387-run-preview",
        "version": V0387_VERSION,
        "preview_summary": "Preview describes one-shot metadata packet construction only.",
    }
    defaults.update(kwargs)
    return RepairProposalLoopRunPreview(**defaults)


def build_repair_proposal_loop_no_execution_guarantee(**kwargs: Any) -> RepairProposalLoopNoExecutionGuarantee:
    defaults = {
        "guarantee_id": "v0387-no-execution-guarantee",
        "version": V0387_VERSION,
        "guarantee_summary": "No autonomous loop, retry, apply, source read, test, repair, or external call is enabled.",
    }
    defaults.update(kwargs)
    return RepairProposalLoopNoExecutionGuarantee(**defaults)


def build_v0387_readiness_report(**kwargs: Any) -> V0387ReadinessReport:
    defaults = {
        "readiness_report_id": "v0387-readiness-report",
        "version": V0387_VERSION,
        "flags": build_repair_proposal_loop_flags(),
        "no_execution_guarantee": build_repair_proposal_loop_no_execution_guarantee(),
    }
    defaults.update(kwargs)
    return V0387ReadinessReport(**defaults)


def default_repair_proposal_loop_policy() -> RepairProposalLoopPolicy:
    return build_repair_proposal_loop_policy()


def build_repair_proposal_loop_input_from_human_review_packet(
    human_review_packet: Any,
    *,
    approval_request_contract: Any | None = None,
    safety_report: Any | None = None,
    proposed_patch_envelope: Any | None = None,
    scope_plan: Any | None = None,
    source_context_snapshot: Any | None = None,
    evidence_bundle: Any | None = None,
    source_refs: list[RepairProposalLoopSourceRef] | None = None,
    **kwargs: Any,
) -> RepairProposalLoopInput:
    defaults = {
        "loop_input_id": "v0387-loop-input-from-human-review",
        "version": V0387_VERSION,
        "human_review_packet_id": _source_id_from(human_review_packet),
        "approval_request_contract_id": _source_id_from(approval_request_contract),
        "safety_report_id": _source_id_from(safety_report),
        "proposed_patch_envelope_id": _source_id_from(proposed_patch_envelope),
        "scope_plan_id": _source_id_from(scope_plan),
        "source_context_snapshot_id": _source_id_from(source_context_snapshot),
        "evidence_bundle_id": _source_id_from(evidence_bundle),
        "source_refs": source_refs or [],
        "task_summary": "Assemble existing human review and prior repair metadata into one-shot loop packet input.",
    }
    defaults.update(kwargs)
    return build_repair_proposal_loop_input(**defaults)


def collect_repair_proposal_loop_artifacts(
    *,
    human_review_packet: Any | None = None,
    approval_request_contract: Any | None = None,
    safety_report: Any | None = None,
    proposed_patch_envelope: Any | None = None,
    scope_plan: Any | None = None,
    source_context_snapshot: Any | None = None,
    evidence_bundle: Any | None = None,
    source_refs: list[RepairProposalLoopSourceRef] | None = None,
    **kwargs: Any,
) -> RepairProposalLoopArtifactBundle:
    ids = {
        "human_review_packet_id": _source_id_from(human_review_packet, kwargs.get("human_review_packet_id")),
        "approval_request_contract_id": _source_id_from(
            approval_request_contract, kwargs.get("approval_request_contract_id")
        ),
        "safety_report_id": _source_id_from(safety_report, kwargs.get("safety_report_id")),
        "proposed_patch_envelope_id": _source_id_from(
            proposed_patch_envelope, kwargs.get("proposed_patch_envelope_id")
        ),
        "scope_plan_id": _source_id_from(scope_plan, kwargs.get("scope_plan_id")),
        "source_context_snapshot_id": _source_id_from(
            source_context_snapshot, kwargs.get("source_context_snapshot_id")
        ),
        "evidence_bundle_id": _source_id_from(evidence_bundle, kwargs.get("evidence_bundle_id")),
    }
    present = [key for key in REQUIRED_LOOP_ARTIFACT_KEYS if ids.get(key)]
    missing = [key for key in REQUIRED_LOOP_ARTIFACT_KEYS if not ids.get(key)]
    complete = not missing
    return build_repair_proposal_loop_artifact_bundle(
        artifact_bundle_id=kwargs.get("artifact_bundle_id", "v0387-collected-artifact-bundle"),
        version=kwargs.get("version", V0387_VERSION),
        present_artifacts=present,
        missing_artifacts=missing,
        invalid_artifacts=kwargs.get("invalid_artifacts", []),
        bundle_summary=kwargs.get(
            "bundle_summary",
            "Existing v0.38.1-v0.38.6 metadata artifacts collected for one-shot loop trial.",
        ),
        complete_for_one_shot_trial=complete,
        complete_for_future_cli_surface=complete,
        complete_for_future_v039_handoff_metadata=complete,
        source_refs=source_refs or kwargs.get("source_refs", []),
        **ids,
    )


def create_repair_proposal_loop_step_records(
    artifact_bundle: RepairProposalLoopArtifactBundle,
) -> list[RepairProposalLoopStepRecord]:
    artifact_for_step = {
        RepairProposalLoopStepKind.EVIDENCE_CONTRACT_STEP: artifact_bundle.evidence_bundle_id,
        RepairProposalLoopStepKind.SOURCE_CONTEXT_STEP: artifact_bundle.source_context_snapshot_id,
        RepairProposalLoopStepKind.SCOPE_PLANNING_STEP: artifact_bundle.scope_plan_id,
        RepairProposalLoopStepKind.PATCH_METADATA_STEP: artifact_bundle.proposed_patch_envelope_id,
        RepairProposalLoopStepKind.SAFETY_VALIDATION_STEP: artifact_bundle.safety_report_id,
        RepairProposalLoopStepKind.HUMAN_REVIEW_PACKET_STEP: artifact_bundle.human_review_packet_id,
        RepairProposalLoopStepKind.DO_NOTHING_COMPARISON_STEP: "do-nothing-represented",
        RepairProposalLoopStepKind.STOP_CONDITION_STEP: "stop-required",
        RepairProposalLoopStepKind.HUMAN_HANDOFF_STEP: "human-handoff-required",
    }
    records: list[RepairProposalLoopStepRecord] = []
    for index, (step_kind, artifact_id) in enumerate(artifact_for_step.items(), start=1):
        present = bool(artifact_id)
        records.append(
            build_repair_proposal_loop_step_record(
                loop_step_id=f"v0387-step-{index:02d}-{step_kind.value}",
                step_kind=step_kind,
                step_status=(
                    RepairProposalLoopStepStatus.COMPLETED_AS_METADATA
                    if present
                    else RepairProposalLoopStepStatus.ARTIFACT_MISSING
                ),
                artifact_ref_id=artifact_id,
                completed_as_metadata=present,
                step_summary=(
                    f"{step_kind.value} recorded from existing metadata."
                    if present
                    else f"{step_kind.value} missing required existing metadata."
                ),
                evidence_refs=[artifact_id] if artifact_id else [],
            )
        )
    return records


def audit_repair_proposal_loop_boundaries(
    step_records: list[RepairProposalLoopStepRecord],
) -> RepairProposalLoopBoundaryAudit:
    _validate_list("step_records", step_records)
    missing = [
        record.step_kind
        for record in step_records
        if record.step_status == RepairProposalLoopStepStatus.ARTIFACT_MISSING
        or str(record.step_status) == RepairProposalLoopStepStatus.ARTIFACT_MISSING.value
    ]
    risks: list[RepairProposalLoopRiskKind | str] = []
    risk_by_step = {
        RepairProposalLoopStepKind.EVIDENCE_CONTRACT_STEP: RepairProposalLoopRiskKind.MISSING_EVIDENCE_BUNDLE_RISK,
        RepairProposalLoopStepKind.SOURCE_CONTEXT_STEP: RepairProposalLoopRiskKind.MISSING_SOURCE_CONTEXT_RISK,
        RepairProposalLoopStepKind.SCOPE_PLANNING_STEP: RepairProposalLoopRiskKind.MISSING_SCOPE_PLAN_RISK,
        RepairProposalLoopStepKind.PATCH_METADATA_STEP: RepairProposalLoopRiskKind.MISSING_PATCH_ENVELOPE_RISK,
        RepairProposalLoopStepKind.SAFETY_VALIDATION_STEP: RepairProposalLoopRiskKind.MISSING_SAFETY_REPORT_RISK,
        RepairProposalLoopStepKind.HUMAN_REVIEW_PACKET_STEP: RepairProposalLoopRiskKind.MISSING_HUMAN_REVIEW_PACKET_RISK,
    }
    for step_kind in missing:
        normalized = RepairProposalLoopStepKind(str(step_kind))
        risk = risk_by_step.get(normalized)
        if risk and risk not in risks:
            risks.append(risk)
    return build_repair_proposal_loop_boundary_audit(
        checked_step_ids=[record.loop_step_id for record in step_records],
        risk_kinds=risks,
        audit_summary=(
            "Boundary audit confirms no runtime actions; required artifact gaps require review."
            if risks
            else "Boundary audit confirms no runtime actions and no missing required artifacts."
        ),
    )


def create_repair_proposal_loop_stop_condition(
    *,
    stop_reason_kind: RepairProposalLoopStopReasonKind | str = RepairProposalLoopStopReasonKind.STOPPED_AFTER_ONE_CYCLE,
    **kwargs: Any,
) -> RepairProposalLoopStopCondition:
    return build_repair_proposal_loop_stop_condition(stop_reason_kind=stop_reason_kind, **kwargs)


def compare_repair_proposal_loop_to_do_nothing(
    artifact_bundle: RepairProposalLoopArtifactBundle,
    boundary_audit: RepairProposalLoopBoundaryAudit,
) -> RepairProposalLoopDoNothingComparison:
    if artifact_bundle.missing_artifacts:
        return build_repair_proposal_loop_do_nothing_comparison(
            comparison_kind=RepairProposalLoopDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_MISSING_ARTIFACT,
            comparison_summary="Do-nothing is preferred because required one-shot loop artifacts are missing.",
            do_nothing_preferred=True,
            do_nothing_required=True,
            loop_packet_outperforms_do_nothing=False,
            confidence=RepairProposalLoopConfidenceLevel.HIGH,
            evidence_refs=artifact_bundle.missing_artifacts,
        )
    if boundary_audit.risk_kinds:
        return build_repair_proposal_loop_do_nothing_comparison(
            comparison_kind=RepairProposalLoopDoNothingComparisonKind.DO_NOTHING_COMPETITIVE,
            comparison_summary="Do-nothing remains competitive because loop boundary risks require review.",
            do_nothing_preferred=False,
            do_nothing_required=False,
            loop_packet_outperforms_do_nothing=False,
            confidence=RepairProposalLoopConfidenceLevel.MEDIUM,
        )
    return build_repair_proposal_loop_do_nothing_comparison(
        comparison_kind=RepairProposalLoopDoNothingComparisonKind.LOOP_PACKET_BETTER_THAN_DO_NOTHING,
        comparison_summary="One-shot loop packet metadata is review-ready while do-nothing remains valid.",
        do_nothing_preferred=False,
        do_nothing_required=False,
        loop_packet_outperforms_do_nothing=True,
        confidence=RepairProposalLoopConfidenceLevel.MEDIUM,
    )


def decide_repair_proposal_loop(
    artifact_bundle: RepairProposalLoopArtifactBundle,
    boundary_audit: RepairProposalLoopBoundaryAudit,
    do_nothing_comparison: RepairProposalLoopDoNothingComparison,
) -> RepairProposalLoopDecision:
    if artifact_bundle.missing_artifacts or artifact_bundle.invalid_artifacts:
        return build_repair_proposal_loop_decision(
            decision_kind=RepairProposalLoopDecisionKind.MISSING_REQUIRED_ARTIFACT,
            disposition=RepairProposalLoopDisposition.REVIEW_REQUIRED,
            outcome_kind=RepairProposalLoopOutcomeKind.HUMAN_REVIEW_REQUIRED,
            decision_summary="One-shot loop packet requires human review because required artifacts are missing.",
            rationale_summary="v0.38.7 does not generate missing artifacts or read source to fill gaps.",
            ready_for_future_cli_surface_input=False,
            ready_for_future_consolidation_input=False,
            ready_for_future_v039_handoff_metadata=False,
            confidence=RepairProposalLoopConfidenceLevel.HIGH,
            evidence_refs=artifact_bundle.missing_artifacts + artifact_bundle.invalid_artifacts,
        )
    if do_nothing_comparison.do_nothing_required:
        return build_repair_proposal_loop_decision(
            decision_kind=RepairProposalLoopDecisionKind.CHOOSE_DO_NOTHING,
            disposition=RepairProposalLoopDisposition.DO_NOTHING_PREFERRED,
            outcome_kind=RepairProposalLoopOutcomeKind.DO_NOTHING_PREFERRED,
            decision_summary="Do-nothing is selected for loop trial metadata due to blocking comparison.",
            rationale_summary="Do-nothing remains mandatory when blocking issues are present.",
            ready_for_future_cli_surface_input=True,
            ready_for_future_consolidation_input=True,
            ready_for_future_v039_handoff_metadata=False,
        )
    return build_repair_proposal_loop_decision(
        decision_kind=RepairProposalLoopDecisionKind.ALLOW_ONE_SHOT_LOOP_PACKET,
        disposition=(
            RepairProposalLoopDisposition.TRIAL_READY_WITH_WARNINGS
            if boundary_audit.risk_kinds
            else RepairProposalLoopDisposition.TRIAL_READY
        ),
        outcome_kind=(
            RepairProposalLoopOutcomeKind.ONE_SHOT_PACKET_READY_WITH_WARNINGS
            if boundary_audit.risk_kinds
            else RepairProposalLoopOutcomeKind.ONE_SHOT_PACKET_READY
        ),
        decision_summary="One-shot loop packet metadata may be prepared for future CLI/consolidation handoff.",
        rationale_summary="Existing artifacts are present and boundary audit confirms no execution permissions.",
    )


def create_repair_proposal_loop_packet(
    *,
    human_review_packet: Any | None = None,
    approval_request_contract: Any | None = None,
    safety_report: Any | None = None,
    proposed_patch_envelope: Any | None = None,
    scope_plan: Any | None = None,
    source_context_snapshot: Any | None = None,
    evidence_bundle: Any | None = None,
    loop_input: RepairProposalLoopInput | None = None,
    source_refs: list[RepairProposalLoopSourceRef] | None = None,
    **kwargs: Any,
) -> RepairProposalLoopPacket:
    bundle = collect_repair_proposal_loop_artifacts(
        human_review_packet=human_review_packet,
        approval_request_contract=approval_request_contract,
        safety_report=safety_report,
        proposed_patch_envelope=proposed_patch_envelope,
        scope_plan=scope_plan,
        source_context_snapshot=source_context_snapshot,
        evidence_bundle=evidence_bundle,
        source_refs=source_refs,
    )
    step_records = create_repair_proposal_loop_step_records(bundle)
    boundary_audit = audit_repair_proposal_loop_boundaries(step_records)
    stop_reason = (
        RepairProposalLoopStopReasonKind.STOPPED_DUE_TO_MISSING_ARTIFACT
        if bundle.missing_artifacts
        else RepairProposalLoopStopReasonKind.STOPPED_AFTER_ONE_CYCLE
    )
    stop_condition = create_repair_proposal_loop_stop_condition(stop_reason_kind=stop_reason)
    do_nothing_comparison = compare_repair_proposal_loop_to_do_nothing(bundle, boundary_audit)
    loop_decision = decide_repair_proposal_loop(bundle, boundary_audit, do_nothing_comparison)
    status = (
        RepairProposalLoopStatus.ONE_SHOT_LOOP_PACKET_CREATED_WITH_WARNINGS
        if boundary_audit.risk_kinds or bundle.missing_artifacts
        else RepairProposalLoopStatus.ONE_SHOT_LOOP_PACKET_CREATED
    )
    readiness = (
        RepairProposalLoopReadinessLevel.ONE_SHOT_LOOP_PACKET_READY
        if not bundle.missing_artifacts
        else RepairProposalLoopReadinessLevel.BLOCKED
    )
    defaults = {
        "loop_packet_id": "v0387-created-loop-packet",
        "version": V0387_VERSION,
        "loop_input_id": loop_input.loop_input_id if loop_input else "v0387-loop-input",
        "status": status,
        "readiness_level": readiness,
        "disposition": loop_decision.disposition,
        "outcome_kind": loop_decision.outcome_kind,
        "artifact_bundle": bundle,
        "step_records": step_records,
        "boundary_audit": boundary_audit,
        "stop_condition": stop_condition,
        "do_nothing_comparison": do_nothing_comparison,
        "loop_decision": loop_decision,
        "source_refs": source_refs or [],
        "rendered_packet_preview": _render_loop_packet_preview(
            bundle, step_records, stop_condition, do_nothing_comparison, loop_decision
        ),
        "ready_for_future_cli_surface_input": loop_decision.ready_for_future_cli_surface_input,
        "ready_for_future_consolidation_input": loop_decision.ready_for_future_consolidation_input,
        "ready_for_future_v039_handoff_metadata": loop_decision.ready_for_future_v039_handoff_metadata,
    }
    defaults.update(kwargs)
    return build_repair_proposal_loop_packet(**defaults)


def validate_repair_proposal_loop_packet(
    packet: RepairProposalLoopPacket,
) -> RepairProposalLoopValidationReport:
    findings: list[RepairProposalLoopValidationFinding] = []
    if packet.max_cycle_count != 1 or packet.actual_cycle_count > 1:
        findings.append(
            build_repair_proposal_loop_validation_finding(
                validation_finding_id="v0387-cycle-count-finding",
                finding_summary="Loop packet violates one-shot cycle constraint.",
                blocks_loop_packet=True,
            )
        )
    if packet.retry_count != 0:
        findings.append(
            build_repair_proposal_loop_validation_finding(
                validation_finding_id="v0387-retry-count-finding",
                finding_summary="Loop packet violates retry-zero constraint.",
                blocks_loop_packet=True,
            )
        )
    if packet.artifact_bundle.missing_artifacts:
        findings.append(
            build_repair_proposal_loop_validation_finding(
                validation_finding_id="v0387-missing-artifact-finding",
                finding_summary="Loop packet is missing required prior-stage artifacts.",
                evidence_refs=packet.artifact_bundle.missing_artifacts,
                blocks_loop_packet=True,
            )
        )
    return build_repair_proposal_loop_validation_report(findings=findings)


def repair_proposal_loop_flags_preserve_no_execution(flags: RepairProposalLoopFlagSet) -> bool:
    return all(not getattr(flags, name) for name in UNSAFE_REPAIR_PROPOSAL_LOOP_FLAG_NAMES)


def repair_proposal_loop_policy_is_one_shot_only(policy: RepairProposalLoopPolicy) -> bool:
    return policy.max_cycle_count == 1 and policy.max_retry_count == 0


def repair_proposal_loop_policy_blocks_runtime(policy: RepairProposalLoopPolicy) -> bool:
    return all(not getattr(policy, name) for name in UNSAFE_REPAIR_PROPOSAL_LOOP_POLICY_ALLOW_NAMES)


def repair_proposal_loop_packet_is_not_execution(packet: RepairProposalLoopPacket) -> bool:
    return (
        packet.max_cycle_count == 1
        and packet.actual_cycle_count <= 1
        and packet.retry_count == 0
        and packet.human_handoff_required
        and all(not getattr(packet, name) for name in UNSAFE_LOOP_PACKET_STATE_NAMES)
    )


def repair_proposal_loop_decision_is_not_apply_permission(decision: RepairProposalLoopDecision) -> bool:
    return all(not getattr(decision, name) for name in UNSAFE_LOOP_DECISION_NOW_NAMES)


def v0387_readiness_report_is_not_execution_ready(report: V0387ReadinessReport) -> bool:
    return (
        not report.ready_for_execution
        and not report.production_certified
        and repair_proposal_loop_flags_preserve_no_execution(report.flags)
    )


def _render_loop_packet_preview(
    bundle: RepairProposalLoopArtifactBundle,
    step_records: list[RepairProposalLoopStepRecord],
    stop_condition: RepairProposalLoopStopCondition,
    do_nothing_comparison: RepairProposalLoopDoNothingComparison,
    decision: RepairProposalLoopDecision,
) -> str:
    step_values = ", ".join(str(record.step_kind) for record in step_records[:9])
    return (
        f"{V0387_RELEASE_NAME}: one-shot metadata packet. "
        f"present={len(bundle.present_artifacts)} missing={len(bundle.missing_artifacts)}. "
        f"steps={step_values}. stop={stop_condition.stop_reason_kind}. "
        f"do_nothing={do_nothing_comparison.comparison_kind}. decision={decision.decision_kind}. "
        "No autonomous loop, retry, approval, apply, source read, new patch generation, test, repair, or external call."
    )
