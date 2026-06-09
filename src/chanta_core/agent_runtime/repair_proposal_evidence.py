from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0381_VERSION = "v0.38.1"
V0381_RELEASE_NAME = "v0.38.1 Repair Proposal Evidence Contract"

UNSAFE_EVIDENCE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_source_file_read",
    "ready_for_sandbox_source_read",
    "ready_for_repair_proposal_generation",
    "ready_for_proposed_diff_generation",
    "ready_for_proposed_code_hunk_generation",
    "ready_for_proposed_patch_envelope_generation",
    "ready_for_repair_patch_proposal",
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_repair_execution",
    "ready_for_repair_apply",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
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
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_EVIDENCE_POLICY_ALLOW_NAMES = (
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_repair_proposal_generation",
    "allow_proposed_diff_generation",
    "allow_proposed_code_hunk_generation",
    "allow_proposed_patch_envelope_generation",
    "allow_repair_patch_proposal",
    "allow_repair_execution",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_ELIGIBILITY_NOW_NAMES = (
    "source_read_allowed_now",
    "proposal_generation_allowed_now",
    "diff_generation_allowed_now",
    "hunk_generation_allowed_now",
    "patch_envelope_generation_allowed_now",
    "repair_execution_allowed_now",
)

UNSAFE_CONTRACT_NOW_NAMES = (
    "allows_source_read_now",
    "allows_proposal_generation_now",
    "allows_diff_generation_now",
    "allows_hunk_generation_now",
    "allows_patch_envelope_generation_now",
    "allows_repair_execution_now",
)

UNSAFE_BUNDLE_STATE_NAMES = (
    "source_read_performed",
    "proposal_generated",
    "diff_generated",
    "hunk_generated",
    "patch_envelope_generated",
    "repair_executed",
    "production_certified",
    "ready_for_execution",
)

REQUIRED_PROHIBITED_RUNTIME_ACTIONS = (
    "source_read",
    "proposal_generation",
    "diff_generation",
    "hunk_generation",
    "file_write",
    "patch_apply",
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

STRENGTH_ORDER = {
    "missing": 0,
    "contradictory": 0,
    "unknown": 0,
    "insufficient": 1,
    "weak": 2,
    "adequate": 3,
    "strong": 4,
}


class RepairProposalEvidenceMode(StrEnum):
    EVIDENCE_CONTRACT = "evidence_contract"
    EVIDENCE_BUNDLE = "evidence_bundle"
    EVIDENCE_ASSESSMENT = "evidence_assessment"
    ELIGIBILITY_DECISION = "eligibility_decision"
    DO_NOTHING_EVIDENCE = "do_nothing_evidence"
    FUTURE_SOURCE_CONTEXT_INPUT = "future_source_context_input"
    FUTURE_SCOPE_PLANNING_INPUT = "future_scope_planning_input"
    FUTURE_PATCH_METADATA_INPUT = "future_patch_metadata_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairProposalEvidenceSourceKind(StrEnum):
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0379_TEST_RUNNER_CONSOLIDATION = "v0379_test_runner_consolidation"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    V0377_COLD_AGENT_SCORECARD = "v0377_cold_agent_scorecard"
    V0377_COLD_AGENT_VERDICT = "v0377_cold_agent_verdict"
    V0376_VERA_CODEX_TRIAL_PACKET = "v0376_vera_codex_trial_packet"
    V0375_REPAIR_SUGGESTION_ENVELOPE = "v0375_repair_suggestion_envelope"
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0374_FAILURE_DIAGNOSIS_REPORT = "v0374_failure_diagnosis_report"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    V0373_OUTCOME_CLASSIFICATION = "v0373_outcome_classification"
    V0373_FAILURE_CLASSIFICATION = "v0373_failure_classification"
    V0372_TEST_EXECUTION_RESULT = "v0372_test_execution_result"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairProposalEvidenceStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    CONTRACT_CREATED = "contract_created"
    BUNDLE_CREATED = "bundle_created"
    ASSESSED = "assessed"
    ELIGIBLE_FOR_FUTURE_SOURCE_CONTEXT = "eligible_for_future_source_context"
    ELIGIBLE_FOR_FUTURE_SCOPE_PLANNING = "eligible_for_future_scope_planning"
    ELIGIBLE_FOR_FUTURE_PATCH_METADATA = "eligible_for_future_patch_metadata"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    NO_REPAIR_NEEDED = "no_repair_needed"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairProposalEvidenceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    EVIDENCE_CONTRACT_READY = "evidence_contract_ready"
    EVIDENCE_BUNDLE_READY = "evidence_bundle_ready"
    EVIDENCE_ASSESSMENT_READY = "evidence_assessment_ready"
    ELIGIBILITY_DECISION_READY = "eligibility_decision_ready"
    DO_NOTHING_EVIDENCE_READY = "do_nothing_evidence_ready"
    FUTURE_SOURCE_CONTEXT_INPUT_READY = "future_source_context_input_ready"
    FUTURE_SCOPE_PLANNING_INPUT_READY = "future_scope_planning_input_ready"
    FUTURE_PATCH_METADATA_INPUT_READY = "future_patch_metadata_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0382 = "design_handoff_ready_for_v0382"
    DESIGN_HANDOFF_READY_FOR_V0383 = "design_handoff_ready_for_v0383"
    DESIGN_HANDOFF_READY_FOR_V0384 = "design_handoff_ready_for_v0384"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairProposalEvidenceDecisionKind(StrEnum):
    ALLOW_EVIDENCE_CONTRACT = "allow_evidence_contract"
    ALLOW_EVIDENCE_BUNDLE = "allow_evidence_bundle"
    ALLOW_EVIDENCE_ASSESSMENT = "allow_evidence_assessment"
    ALLOW_ELIGIBILITY_DECISION = "allow_eligibility_decision"
    ALLOW_DO_NOTHING_EVIDENCE = "allow_do_nothing_evidence"
    ALLOW_FUTURE_SOURCE_CONTEXT_INPUT = "allow_future_source_context_input"
    ALLOW_FUTURE_SCOPE_PLANNING_INPUT = "allow_future_scope_planning_input"
    ALLOW_FUTURE_PATCH_METADATA_INPUT = "allow_future_patch_metadata_input"
    CHOOSE_NO_REPAIR_NEEDED = "choose_no_repair_needed"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW = "choose_human_review"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    INSUFFICIENT_EVIDENCE = "insufficient_evidence"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairProposalEvidenceRiskKind(StrEnum):
    MISSING_BOUNDARY_RISK = "missing_boundary_risk"
    MISSING_TEST_RESULT_RISK = "missing_test_result_risk"
    MISSING_FEEDBACK_RISK = "missing_feedback_risk"
    MISSING_REPAIR_SUGGESTION_RISK = "missing_repair_suggestion_risk"
    MISSING_COLD_SCORECARD_RISK = "missing_cold_scorecard_risk"
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    CONTRADICTORY_EVIDENCE_RISK = "contradictory_evidence_risk"
    OVERCONFIDENT_ELIGIBILITY_RISK = "overconfident_eligibility_risk"
    FAILED_TEST_REPORTED_AS_SUCCESS_RISK = "failed_test_reported_as_success_risk"
    INCONCLUSIVE_REPORTED_AS_SUCCESS_RISK = "inconclusive_reported_as_success_risk"
    PASSED_TEST_REPAIR_OVERREACH_RISK = "passed_test_repair_overreach_risk"
    MISSING_DEPENDENCY_INSTALL_CONFUSION_RISK = "missing_dependency_install_confusion_risk"
    TIMEOUT_RETRY_CONFUSION_RISK = "timeout_retry_confusion_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    HUMAN_REVIEW_OMISSION_RISK = "human_review_omission_risk"
    SOURCE_READ_CONFUSION_RISK = "source_read_confusion_risk"
    REPAIR_PROPOSAL_GENERATION_CONFUSION_RISK = "repair_proposal_generation_confusion_risk"
    DIFF_GENERATION_CONFUSION_RISK = "diff_generation_confusion_risk"
    HUNK_GENERATION_CONFUSION_RISK = "hunk_generation_confusion_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairProposalEvidenceItemKind(StrEnum):
    BOUNDARY_EVIDENCE = "boundary_evidence"
    COLD_SCORECARD_EVIDENCE = "cold_scorecard_evidence"
    COLD_VERDICT_EVIDENCE = "cold_verdict_evidence"
    VERA_TRIAL_EVIDENCE = "vera_trial_evidence"
    REPAIR_SUGGESTION_EVIDENCE = "repair_suggestion_evidence"
    FEEDBACK_REPORT_EVIDENCE = "feedback_report_evidence"
    FAILURE_DIAGNOSIS_EVIDENCE = "failure_diagnosis_evidence"
    TEST_RESULT_ENVELOPE_EVIDENCE = "test_result_envelope_evidence"
    TEST_EXECUTION_EVIDENCE = "test_execution_evidence"
    PATCH_APPLY_SANDBOX_EVIDENCE = "patch_apply_sandbox_evidence"
    DO_NOTHING_EVIDENCE = "do_nothing_evidence"
    HUMAN_OPERATOR_NOTE = "human_operator_note"
    MISSING_EVIDENCE = "missing_evidence"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    UNKNOWN = "unknown"


class RepairProposalEvidenceStrength(StrEnum):
    STRONG = "strong"
    ADEQUATE = "adequate"
    WEAK = "weak"
    INSUFFICIENT = "insufficient"
    CONTRADICTORY = "contradictory"
    MISSING = "missing"
    UNKNOWN = "unknown"


class RepairProposalEvidenceConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairProposalEligibilityKind(StrEnum):
    ELIGIBLE_FOR_FUTURE_SOURCE_CONTEXT = "eligible_for_future_source_context"
    ELIGIBLE_FOR_FUTURE_SCOPE_PLANNING = "eligible_for_future_scope_planning"
    ELIGIBLE_FOR_FUTURE_PATCH_METADATA = "eligible_for_future_patch_metadata"
    ELIGIBLE_FOR_HUMAN_REVIEW_ONLY = "eligible_for_human_review_only"
    NO_REPAIR_NEEDED = "no_repair_needed"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    BLOCKED_BY_INSUFFICIENT_EVIDENCE = "blocked_by_insufficient_evidence"
    BLOCKED_BY_CONTRADICTORY_EVIDENCE = "blocked_by_contradictory_evidence"
    BLOCKED_BY_SAFETY_BOUNDARY = "blocked_by_safety_boundary"
    BLOCKED_BY_NO_BOUNDARY = "blocked_by_no_boundary"
    UNKNOWN = "unknown"


class RepairProposalEvidenceGapKind(StrEnum):
    MISSING_BOUNDARY = "missing_boundary"
    MISSING_TEST_RESULT = "missing_test_result"
    MISSING_FEEDBACK_REPORT = "missing_feedback_report"
    MISSING_FAILURE_DIAGNOSIS = "missing_failure_diagnosis"
    MISSING_REPAIR_SUGGESTION = "missing_repair_suggestion"
    MISSING_COLD_SCORECARD = "missing_cold_scorecard"
    MISSING_DO_NOTHING_COMPARISON = "missing_do_nothing_comparison"
    MISSING_HUMAN_REVIEW_CONTEXT = "missing_human_review_context"
    MISSING_FAILURE_EVIDENCE = "missing_failure_evidence"
    CONTRADICTORY_FAILURE_EVIDENCE = "contradictory_failure_evidence"
    INCONCLUSIVE_RESULT = "inconclusive_result"
    UNKNOWN = "unknown"


class RepairProposalEvidenceUseKind(StrEnum):
    SUPPORTS_FUTURE_SOURCE_CONTEXT = "supports_future_source_context"
    SUPPORTS_FUTURE_SCOPE_PLANNING = "supports_future_scope_planning"
    SUPPORTS_FUTURE_PATCH_METADATA = "supports_future_patch_metadata"
    SUPPORTS_NO_REPAIR_NEEDED = "supports_no_repair_needed"
    SUPPORTS_DO_NOTHING = "supports_do_nothing"
    SUPPORTS_HUMAN_REVIEW = "supports_human_review"
    BLOCKS_FUTURE_PROPOSAL_PATH = "blocks_future_proposal_path"
    UNKNOWN = "unknown"


class RepairProposalDoNothingEvidenceKind(StrEnum):
    DO_NOTHING_REQUIRED_DUE_TO_MISSING_EVIDENCE = "do_nothing_required_due_to_missing_evidence"
    DO_NOTHING_REQUIRED_DUE_TO_CONTRADICTION = "do_nothing_required_due_to_contradiction"
    DO_NOTHING_PREFERRED_DUE_TO_PASSED_TESTS = "do_nothing_preferred_due_to_passed_tests"
    DO_NOTHING_COMPETITIVE_DUE_TO_LOW_CONFIDENCE = "do_nothing_competitive_due_to_low_confidence"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
    DO_NOTHING_NOT_PREFERRED_BUT_STILL_VALID = "do_nothing_not_preferred_but_still_valid"
    UNKNOWN = "unknown"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0381_VERSION not in version:
        raise ValueError("version must include v0.38.1")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.1")


def _validate_true(instance: Any, prefix: str = "no_") -> None:
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


def _strength_at_least(value: RepairProposalEvidenceStrength | str, minimum: RepairProposalEvidenceStrength | str) -> bool:
    return STRENGTH_ORDER[str(RepairProposalEvidenceStrength(value))] >= STRENGTH_ORDER[str(RepairProposalEvidenceStrength(minimum))]


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceFlagSet:
    flag_set_id: str
    version: str
    repair_proposal_evidence_layer_constructed: bool
    repair_proposal_evidence_contract_available: bool
    repair_proposal_evidence_bundle_available: bool
    repair_proposal_evidence_assessment_available: bool
    repair_proposal_eligibility_decision_available: bool
    repair_proposal_evidence_gap_register_available: bool
    repair_proposal_do_nothing_evidence_available: bool
    ready_for_v0382_read_only_sandbox_source_context: bool
    ready_for_v0383_repair_scope_planner_change_intent: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_repair_proposal_evidence_contract: bool
    ready_for_repair_proposal_evidence_bundle: bool
    ready_for_repair_proposal_evidence_assessment: bool
    ready_for_repair_proposal_eligibility_decision: bool
    ready_for_repair_proposal_evidence_gap_register: bool
    ready_for_repair_proposal_do_nothing_evidence: bool
    ready_for_future_read_only_sandbox_source_context_input: bool
    ready_for_future_repair_scope_planning_input: bool
    ready_for_future_change_intent_input: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_proposed_code_hunk_generation: bool
    ready_for_proposed_patch_envelope_generation: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_repair_execution: bool
    ready_for_repair_apply: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
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
    ready_for_secret_read: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_independent_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_ui_runtime: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_EVIDENCE_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceSourceRef:
    source_ref_id: str
    source_kind: RepairProposalEvidenceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalEvidenceSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidencePolicy:
    evidence_policy_id: str
    version: str
    allowed_modes: list[RepairProposalEvidenceMode | str]
    required_source_kinds: list[RepairProposalEvidenceSourceKind | str]
    min_strength_for_future_source_context: RepairProposalEvidenceStrength | str
    min_strength_for_future_scope_planning: RepairProposalEvidenceStrength | str
    min_strength_for_future_patch_metadata: RepairProposalEvidenceStrength | str
    require_v0380_boundary: bool
    require_test_result_evidence: bool
    require_feedback_evidence: bool
    require_do_nothing_evidence: bool
    require_human_review_marker: bool
    reject_failed_as_success: bool
    reject_inconclusive_as_success: bool
    reject_missing_dependency_install: bool
    reject_timeout_retry: bool
    allow_evidence_contract: bool
    allow_evidence_bundle: bool
    allow_evidence_assessment: bool
    allow_eligibility_decision: bool
    allow_future_source_context_input: bool
    allow_future_scope_planning_input: bool
    allow_future_patch_metadata_input: bool
    allow_source_file_read: bool
    allow_sandbox_source_read: bool
    allow_repair_proposal_generation: bool
    allow_proposed_diff_generation: bool
    allow_proposed_code_hunk_generation: bool
    allow_proposed_patch_envelope_generation: bool
    allow_repair_patch_proposal: bool
    allow_repair_execution: bool
    allow_patch_application: bool
    allow_apply_patch: bool
    allow_git_apply: bool
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
        _require_non_blank("evidence_policy_id", self.evidence_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, RepairProposalEvidenceMode)
        _validate_enum_list("required_source_kinds", self.required_source_kinds, RepairProposalEvidenceSourceKind)
        RepairProposalEvidenceStrength(self.min_strength_for_future_source_context)
        RepairProposalEvidenceStrength(self.min_strength_for_future_scope_planning)
        RepairProposalEvidenceStrength(self.min_strength_for_future_patch_metadata)
        _validate_false(self, UNSAFE_EVIDENCE_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceInput:
    evidence_input_id: str
    version: str
    boundary_id: str | None
    cold_evaluation_report_id: str | None
    repair_suggestion_id: str | None
    feedback_report_id: str | None
    failure_diagnosis_report_id: str | None
    test_result_envelope_id: str | None
    test_execution_result_id: str | None
    requested_mode: RepairProposalEvidenceMode | str
    source_refs: list[RepairProposalEvidenceSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalEvidenceMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [item for item in REQUIRED_PROHIBITED_RUNTIME_ACTIONS if item not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError("prohibited_runtime_actions must include all unsafe surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceItem:
    evidence_item_id: str
    evidence_kind: RepairProposalEvidenceItemKind | str
    source_ref_id: str | None
    evidence_summary: str
    evidence_strength: RepairProposalEvidenceStrength | str
    confidence: RepairProposalEvidenceConfidenceLevel | str
    evidence_use: RepairProposalEvidenceUseKind | str
    required: bool
    present: bool
    contradictory: bool
    redacted: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_item_id", "evidence_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalEvidenceItemKind(self.evidence_kind)
        RepairProposalEvidenceStrength(self.evidence_strength)
        RepairProposalEvidenceConfidenceLevel(self.confidence)
        RepairProposalEvidenceUseKind(self.evidence_use)
        if self.contradictory and self.confidence == RepairProposalEvidenceConfidenceLevel.HIGH:
            raise ValueError("contradictory evidence cannot be high confidence")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceGap:
    evidence_gap_id: str
    gap_kind: RepairProposalEvidenceGapKind | str
    gap_summary: str
    missing_source_kinds: list[RepairProposalEvidenceSourceKind | str]
    blocks_future_source_context: bool
    blocks_future_scope_planning: bool
    blocks_future_patch_metadata: bool
    requires_human_review: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_gap_id", "gap_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalEvidenceGapKind(self.gap_kind)
        _validate_enum_list("missing_source_kinds", self.missing_source_kinds, RepairProposalEvidenceSourceKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if (
            self.blocks_future_source_context
            or self.blocks_future_scope_planning
            or self.blocks_future_patch_metadata
        ) and not self.requires_human_review:
            raise ValueError("blocking gaps must require human review")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceAssessment:
    evidence_assessment_id: str
    overall_strength: RepairProposalEvidenceStrength | str
    confidence: RepairProposalEvidenceConfidenceLevel | str
    evidence_items: list[RepairProposalEvidenceItem]
    evidence_gaps: list[RepairProposalEvidenceGap]
    assessment_summary: str
    sufficient_for_future_source_context: bool
    sufficient_for_future_scope_planning: bool
    sufficient_for_future_patch_metadata: bool
    insufficient_evidence: bool
    contradictory_evidence: bool
    human_review_required: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_assessment_id", "assessment_summary"):
            _require_non_blank(name, getattr(self, name))
        strength = RepairProposalEvidenceStrength(self.overall_strength)
        confidence = RepairProposalEvidenceConfidenceLevel(self.confidence)
        _validate_list("evidence_items", self.evidence_items)
        _validate_list("evidence_gaps", self.evidence_gaps)
        if (self.insufficient_evidence or self.contradictory_evidence) and (
            self.sufficient_for_future_source_context
            or self.sufficient_for_future_scope_planning
            or self.sufficient_for_future_patch_metadata
        ):
            raise ValueError("sufficient flags must be False for insufficient or contradictory evidence")
        if confidence == RepairProposalEvidenceConfidenceLevel.HIGH and strength not in (
            RepairProposalEvidenceStrength.STRONG,
            RepairProposalEvidenceStrength.ADEQUATE,
        ):
            raise ValueError("high confidence requires adequate or strong evidence")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalDoNothingEvidence:
    do_nothing_evidence_id: str
    do_nothing_kind: RepairProposalDoNothingEvidenceKind | str
    evidence_summary: str
    evidence_refs: list[str]
    do_nothing_remains_valid: bool
    do_nothing_preferred: bool
    do_nothing_required: bool
    confidence: RepairProposalEvidenceConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("do_nothing_evidence_id", "evidence_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalDoNothingEvidenceKind(self.do_nothing_kind)
        RepairProposalEvidenceConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.do_nothing_remains_valid is not True:
            raise ValueError("do_nothing_remains_valid must remain True in v0.38.1")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEligibilityDecision:
    eligibility_decision_id: str
    eligibility_kind: RepairProposalEligibilityKind | str
    decision_kind: RepairProposalEvidenceDecisionKind | str
    decision_summary: str
    rationale_summary: str
    evidence_assessment_id: str
    do_nothing_evidence_id: str
    confidence: RepairProposalEvidenceConfidenceLevel | str
    evidence_refs: list[str]
    eligible_for_future_source_context: bool
    eligible_for_future_scope_planning: bool
    eligible_for_future_patch_metadata: bool
    source_read_allowed_now: bool
    proposal_generation_allowed_now: bool
    diff_generation_allowed_now: bool
    hunk_generation_allowed_now: bool
    patch_envelope_generation_allowed_now: bool
    repair_execution_allowed_now: bool
    human_review_required: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "eligibility_decision_id",
            "decision_summary",
            "rationale_summary",
            "evidence_assessment_id",
            "do_nothing_evidence_id",
        ):
            _require_non_blank(name, getattr(self, name))
        RepairProposalEligibilityKind(self.eligibility_kind)
        RepairProposalEvidenceDecisionKind(self.decision_kind)
        RepairProposalEvidenceConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_ELIGIBILITY_NOW_NAMES)
        if self.eligibility_kind in (
            RepairProposalEligibilityKind.BLOCKED_BY_INSUFFICIENT_EVIDENCE,
            RepairProposalEligibilityKind.BLOCKED_BY_CONTRADICTORY_EVIDENCE,
            RepairProposalEligibilityKind.BLOCKED_BY_SAFETY_BOUNDARY,
            RepairProposalEligibilityKind.BLOCKED_BY_NO_BOUNDARY,
            RepairProposalEligibilityKind.NO_REPAIR_NEEDED,
            RepairProposalEligibilityKind.DO_NOTHING_PREFERRED,
        ) and (
            self.eligible_for_future_source_context
            or self.eligible_for_future_scope_planning
            or self.eligible_for_future_patch_metadata
        ):
            raise ValueError("blocked/no-repair/do-nothing eligibility cannot enable future proposal inputs")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceContract:
    evidence_contract_id: str
    version: str
    evidence_input_id: str
    policy: RepairProposalEvidencePolicy
    required_evidence_kinds: list[RepairProposalEvidenceItemKind | str]
    optional_evidence_kinds: list[RepairProposalEvidenceItemKind | str]
    accepted_source_kinds: list[RepairProposalEvidenceSourceKind | str]
    rejected_source_kinds: list[RepairProposalEvidenceSourceKind | str]
    contract_summary: str
    requires_boundary: bool
    requires_test_result: bool
    requires_feedback_or_diagnosis: bool
    requires_do_nothing_evidence: bool
    requires_human_review_marker: bool
    allows_source_read_now: bool
    allows_proposal_generation_now: bool
    allows_diff_generation_now: bool
    allows_hunk_generation_now: bool
    allows_patch_envelope_generation_now: bool
    allows_repair_execution_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_contract_id", "evidence_input_id", "contract_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if not isinstance(self.policy, RepairProposalEvidencePolicy):
            raise TypeError("policy must be RepairProposalEvidencePolicy")
        _validate_enum_list("required_evidence_kinds", self.required_evidence_kinds, RepairProposalEvidenceItemKind)
        _validate_enum_list("optional_evidence_kinds", self.optional_evidence_kinds, RepairProposalEvidenceItemKind)
        _validate_enum_list("accepted_source_kinds", self.accepted_source_kinds, RepairProposalEvidenceSourceKind)
        _validate_enum_list("rejected_source_kinds", self.rejected_source_kinds, RepairProposalEvidenceSourceKind)
        _validate_false(self, UNSAFE_CONTRACT_NOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceBundle:
    evidence_bundle_id: str
    version: str
    evidence_contract_id: str
    evidence_items: list[RepairProposalEvidenceItem]
    evidence_gaps: list[RepairProposalEvidenceGap]
    do_nothing_evidence: RepairProposalDoNothingEvidence
    evidence_assessment: RepairProposalEvidenceAssessment
    eligibility_decision: RepairProposalEligibilityDecision
    source_refs: list[RepairProposalEvidenceSourceRef]
    bundle_summary: str
    ready_for_future_source_context_input: bool
    ready_for_future_scope_planning_input: bool
    ready_for_future_patch_metadata_input: bool
    source_read_performed: bool
    proposal_generated: bool
    diff_generated: bool
    hunk_generated: bool
    patch_envelope_generated: bool
    repair_executed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_bundle_id", "evidence_contract_id", "bundle_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("evidence_items", self.evidence_items)
        _validate_list("evidence_gaps", self.evidence_gaps)
        if not isinstance(self.do_nothing_evidence, RepairProposalDoNothingEvidence):
            raise TypeError("do_nothing_evidence must be RepairProposalDoNothingEvidence")
        if not isinstance(self.evidence_assessment, RepairProposalEvidenceAssessment):
            raise TypeError("evidence_assessment must be RepairProposalEvidenceAssessment")
        if not isinstance(self.eligibility_decision, RepairProposalEligibilityDecision):
            raise TypeError("eligibility_decision must be RepairProposalEligibilityDecision")
        _validate_list("source_refs", self.source_refs)
        if self.ready_for_future_source_context_input and not self.eligibility_decision.eligible_for_future_source_context:
            raise ValueError("future source context readiness requires eligibility decision")
        if self.ready_for_future_scope_planning_input and not self.eligibility_decision.eligible_for_future_scope_planning:
            raise ValueError("future scope planning readiness requires eligibility decision")
        if self.ready_for_future_patch_metadata_input and not self.eligibility_decision.eligible_for_future_patch_metadata:
            raise ValueError("future patch metadata readiness requires eligibility decision")
        _validate_false(self, UNSAFE_BUNDLE_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairProposalEvidenceRiskKind | str
    decision_kind: RepairProposalEvidenceDecisionKind | str
    blocks_future_source_context: bool
    blocks_future_scope_planning: bool
    blocks_future_patch_metadata: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalEvidenceRiskKind(self.risk_kind)
        RepairProposalEvidenceDecisionKind(self.decision_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceValidationReport:
    validation_report_id: str
    version: str
    evidence_bundle_id: str
    findings: list[RepairProposalEvidenceValidationFinding]
    validation_summary: str
    evidence_contract_confirmed: bool
    evidence_gaps_confirmed: bool
    do_nothing_evidence_confirmed: bool
    no_source_read_confirmed: bool
    no_proposal_generation_confirmed: bool
    no_diff_generation_confirmed: bool
    no_hunk_generation_confirmed: bool
    no_patch_envelope_generation_confirmed: bool
    no_repair_execution_confirmed: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "evidence_bundle_id", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        for name in (
            "evidence_contract_confirmed",
            "evidence_gaps_confirmed",
            "do_nothing_evidence_confirmed",
            "no_source_read_confirmed",
            "no_proposal_generation_confirmed",
            "no_diff_generation_confirmed",
            "no_hunk_generation_confirmed",
            "no_patch_envelope_generation_confirmed",
            "no_repair_execution_confirmed",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceReport:
    evidence_report_id: str
    version: str
    evidence_bundle_id: str
    validation_report_id: str
    readiness_level: RepairProposalEvidenceReadinessLevel | str
    status: RepairProposalEvidenceStatus | str
    report_summary: str
    ready_for_future_source_context_input: bool
    ready_for_future_scope_planning_input: bool
    ready_for_future_patch_metadata_input: bool
    ready_for_execution: bool
    production_certified: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("evidence_report_id", "evidence_bundle_id", "validation_report_id", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalEvidenceReadinessLevel(self.readiness_level)
        RepairProposalEvidenceStatus(self.status)
        if self.ready_for_execution is not False or self.production_certified is not False:
            raise ValueError("evidence report is not execution or production readiness")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceRunPreview:
    run_preview_id: str
    version: str
    requested_mode: RepairProposalEvidenceMode | str
    preview_summary: str
    would_create_contract: bool
    would_create_bundle: bool
    would_assess_evidence: bool
    would_decide_eligibility: bool
    would_read_source: bool
    would_generate_proposal: bool
    would_generate_diff: bool
    would_generate_hunk: bool
    would_execute_repair: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "preview_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalEvidenceMode(self.requested_mode)
        for name in ("would_read_source", "would_generate_proposal", "would_generate_diff", "would_generate_hunk", "would_execute_repair"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalEvidenceNoGenerationGuarantee:
    guarantee_id: str
    version: str
    no_source_file_read: bool
    no_sandbox_source_read: bool
    no_repair_proposal_generation: bool
    no_proposed_diff_generation: bool
    no_proposed_code_hunk_generation: bool
    no_proposed_patch_envelope_generation: bool
    no_repair_patch_proposal: bool
    no_file_write: bool
    no_file_edit: bool
    no_patch_application: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_repair_execution: bool
    no_automatic_repair: bool
    no_repair_loop: bool
    no_retry_loop: bool
    no_multi_cycle_repair_loop: bool
    no_test_execution: bool
    no_subprocess_execution: bool
    no_shell_execution: bool
    no_command_execution: bool
    no_dependency_install: bool
    no_network_access: bool
    no_model_provider_invocation: bool
    no_tool_execution: bool
    no_external_agent_execution: bool
    no_claude_code_invocation: bool
    no_codex_cli_invocation: bool
    no_dominion_runtime: bool
    no_provider_invocation: bool
    no_credential_access: bool
    no_secret_read: bool
    no_autonomous_agent_runtime: bool
    no_general_tool_execution: bool
    no_persistent_trace_write: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0381ReadinessReport:
    readiness_report_id: str
    version: str
    evidence_contract_id: str
    evidence_bundle_id: str
    readiness_level: RepairProposalEvidenceReadinessLevel | str
    status: RepairProposalEvidenceStatus | str
    summary: str
    evidence_refs: list[str]
    repair_proposal_evidence_layer_constructed: bool
    ready_for_v0382_read_only_sandbox_source_context: bool
    ready_for_v0383_repair_scope_planner_change_intent: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_repair_proposal_evidence_contract: bool
    ready_for_repair_proposal_evidence_bundle: bool
    ready_for_repair_proposal_evidence_assessment: bool
    ready_for_repair_proposal_eligibility_decision: bool
    ready_for_repair_proposal_evidence_gap_register: bool
    ready_for_repair_proposal_do_nothing_evidence: bool
    ready_for_future_read_only_sandbox_source_context_input: bool
    ready_for_future_repair_scope_planning_input: bool
    ready_for_future_change_intent_input: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_proposed_code_hunk_generation: bool
    ready_for_proposed_patch_envelope_generation: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_execution: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_patch_application: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_automatic_repair: bool
    ready_for_test_execution: bool
    ready_for_shell_execution: bool
    ready_for_model_provider_invocation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "evidence_contract_id", "evidence_bundle_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalEvidenceReadinessLevel(self.readiness_level)
        RepairProposalEvidenceStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, tuple(name for name in UNSAFE_EVIDENCE_FLAG_NAMES if hasattr(self, name)))
        _validate_metadata(self.metadata)


def build_repair_proposal_evidence_flags(**kwargs: Any) -> RepairProposalEvidenceFlagSet:
    safe_defaults = {
        "repair_proposal_evidence_layer_constructed": True,
        "repair_proposal_evidence_contract_available": True,
        "repair_proposal_evidence_bundle_available": True,
        "repair_proposal_evidence_assessment_available": True,
        "repair_proposal_eligibility_decision_available": True,
        "repair_proposal_evidence_gap_register_available": True,
        "repair_proposal_do_nothing_evidence_available": True,
        "ready_for_v0382_read_only_sandbox_source_context": True,
        "ready_for_v0383_repair_scope_planner_change_intent": True,
        "ready_for_v0384_proposed_diff_code_hunk_metadata": True,
        "ready_for_repair_proposal_evidence_contract": True,
        "ready_for_repair_proposal_evidence_bundle": True,
        "ready_for_repair_proposal_evidence_assessment": True,
        "ready_for_repair_proposal_eligibility_decision": True,
        "ready_for_repair_proposal_evidence_gap_register": True,
        "ready_for_repair_proposal_do_nothing_evidence": True,
        "ready_for_future_read_only_sandbox_source_context_input": True,
        "ready_for_future_repair_scope_planning_input": True,
        "ready_for_future_change_intent_input": True,
        "ready_for_future_proposed_diff_metadata_input": True,
        "ready_for_future_proposed_code_hunk_metadata_input": True,
    }
    return RepairProposalEvidenceFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_proposal_evidence_flags:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_EVIDENCE_FLAG_NAMES},
    )


def build_repair_proposal_evidence_source_ref(**kwargs: Any) -> RepairProposalEvidenceSourceRef:
    source_kind = kwargs.pop("source_kind", RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY)
    return RepairProposalEvidenceSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", f"evidence_source_ref:{str(source_kind)}"),
        source_kind=source_kind,
        source_id=kwargs.pop("source_id", "v0.38.0-boundary"),
        source_summary=kwargs.pop("source_summary", "static metadata source reference only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.0 boundary"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_evidence_policy(**kwargs: Any) -> RepairProposalEvidencePolicy:
    return RepairProposalEvidencePolicy(
        evidence_policy_id=kwargs.pop("evidence_policy_id", "repair_proposal_evidence_policy:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            RepairProposalEvidenceMode.EVIDENCE_CONTRACT,
            RepairProposalEvidenceMode.EVIDENCE_BUNDLE,
            RepairProposalEvidenceMode.EVIDENCE_ASSESSMENT,
            RepairProposalEvidenceMode.ELIGIBILITY_DECISION,
            RepairProposalEvidenceMode.DO_NOTHING_EVIDENCE,
            RepairProposalEvidenceMode.FUTURE_SOURCE_CONTEXT_INPUT,
            RepairProposalEvidenceMode.FUTURE_SCOPE_PLANNING_INPUT,
            RepairProposalEvidenceMode.FUTURE_PATCH_METADATA_INPUT,
        ]),
        required_source_kinds=kwargs.pop("required_source_kinds", [
            RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY,
            RepairProposalEvidenceSourceKind.V0373_TEST_RESULT_ENVELOPE,
            RepairProposalEvidenceSourceKind.V0374_TEST_FEEDBACK_REPORT,
        ]),
        min_strength_for_future_source_context=kwargs.pop("min_strength_for_future_source_context", RepairProposalEvidenceStrength.ADEQUATE),
        min_strength_for_future_scope_planning=kwargs.pop("min_strength_for_future_scope_planning", RepairProposalEvidenceStrength.ADEQUATE),
        min_strength_for_future_patch_metadata=kwargs.pop("min_strength_for_future_patch_metadata", RepairProposalEvidenceStrength.STRONG),
        require_v0380_boundary=kwargs.pop("require_v0380_boundary", True),
        require_test_result_evidence=kwargs.pop("require_test_result_evidence", True),
        require_feedback_evidence=kwargs.pop("require_feedback_evidence", True),
        require_do_nothing_evidence=kwargs.pop("require_do_nothing_evidence", True),
        require_human_review_marker=kwargs.pop("require_human_review_marker", True),
        reject_failed_as_success=kwargs.pop("reject_failed_as_success", True),
        reject_inconclusive_as_success=kwargs.pop("reject_inconclusive_as_success", True),
        reject_missing_dependency_install=kwargs.pop("reject_missing_dependency_install", True),
        reject_timeout_retry=kwargs.pop("reject_timeout_retry", True),
        allow_evidence_contract=kwargs.pop("allow_evidence_contract", True),
        allow_evidence_bundle=kwargs.pop("allow_evidence_bundle", True),
        allow_evidence_assessment=kwargs.pop("allow_evidence_assessment", True),
        allow_eligibility_decision=kwargs.pop("allow_eligibility_decision", True),
        allow_future_source_context_input=kwargs.pop("allow_future_source_context_input", True),
        allow_future_scope_planning_input=kwargs.pop("allow_future_scope_planning_input", True),
        allow_future_patch_metadata_input=kwargs.pop("allow_future_patch_metadata_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_EVIDENCE_POLICY_ALLOW_NAMES},
    )


def default_repair_proposal_evidence_policy(**kwargs: Any) -> RepairProposalEvidencePolicy:
    return build_repair_proposal_evidence_policy(**kwargs)


def build_repair_proposal_evidence_input(**kwargs: Any) -> RepairProposalEvidenceInput:
    return RepairProposalEvidenceInput(
        evidence_input_id=kwargs.pop("evidence_input_id", "repair_proposal_evidence_input:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        boundary_id=kwargs.pop("boundary_id", "repair_proposal_boundary:v0.38.0"),
        cold_evaluation_report_id=kwargs.pop("cold_evaluation_report_id", "cold_agent_evaluation_report:v0.37.7"),
        repair_suggestion_id=kwargs.pop("repair_suggestion_id", "repair_suggestion_envelope:v0.37.5"),
        feedback_report_id=kwargs.pop("feedback_report_id", "test_feedback_report:v0.37.4"),
        failure_diagnosis_report_id=kwargs.pop("failure_diagnosis_report_id", "failure_diagnosis_report:v0.37.4"),
        test_result_envelope_id=kwargs.pop("test_result_envelope_id", "test_result_envelope:v0.37.3"),
        test_execution_result_id=kwargs.pop("test_execution_result_id", "test_execution_result:v0.37.2"),
        requested_mode=kwargs.pop("requested_mode", RepairProposalEvidenceMode.EVIDENCE_CONTRACT),
        source_refs=kwargs.pop("source_refs", [
            build_repair_proposal_evidence_source_ref(source_kind=RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY),
            build_repair_proposal_evidence_source_ref(source_kind=RepairProposalEvidenceSourceKind.V0373_TEST_RESULT_ENVELOPE, source_id="test-result-envelope"),
            build_repair_proposal_evidence_source_ref(source_kind=RepairProposalEvidenceSourceKind.V0374_TEST_FEEDBACK_REPORT, source_id="feedback-report"),
            build_repair_proposal_evidence_source_ref(source_kind=RepairProposalEvidenceSourceKind.V0375_REPAIR_SUGGESTION_ENVELOPE, source_id="repair-suggestion"),
            build_repair_proposal_evidence_source_ref(source_kind=RepairProposalEvidenceSourceKind.V0377_COLD_AGENT_SCORECARD, source_id="cold-scorecard"),
        ]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(REQUIRED_PROHIBITED_RUNTIME_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "repair proposal evidence contract request only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_evidence_input_from_v037_artifacts(**kwargs: Any) -> RepairProposalEvidenceInput:
    return build_repair_proposal_evidence_input(**kwargs)


def build_repair_proposal_evidence_item(**kwargs: Any) -> RepairProposalEvidenceItem:
    return RepairProposalEvidenceItem(
        evidence_item_id=kwargs.pop("evidence_item_id", "repair_proposal_evidence_item:v0.38.1"),
        evidence_kind=kwargs.pop("evidence_kind", RepairProposalEvidenceItemKind.TEST_RESULT_ENVELOPE_EVIDENCE),
        source_ref_id=kwargs.pop("source_ref_id", "evidence_source_ref:v0373_test_result_envelope"),
        evidence_summary=kwargs.pop("evidence_summary", "failed test result metadata supports future repair analysis"),
        evidence_strength=kwargs.pop("evidence_strength", RepairProposalEvidenceStrength.ADEQUATE),
        confidence=kwargs.pop("confidence", RepairProposalEvidenceConfidenceLevel.MEDIUM),
        evidence_use=kwargs.pop("evidence_use", RepairProposalEvidenceUseKind.SUPPORTS_FUTURE_SOURCE_CONTEXT),
        required=kwargs.pop("required", True),
        present=kwargs.pop("present", True),
        contradictory=kwargs.pop("contradictory", False),
        redacted=kwargs.pop("redacted", True),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_evidence_gap(**kwargs: Any) -> RepairProposalEvidenceGap:
    return RepairProposalEvidenceGap(
        evidence_gap_id=kwargs.pop("evidence_gap_id", "repair_proposal_evidence_gap:v0.38.1"),
        gap_kind=kwargs.pop("gap_kind", RepairProposalEvidenceGapKind.MISSING_TEST_RESULT),
        gap_summary=kwargs.pop("gap_summary", "required evidence is missing"),
        missing_source_kinds=kwargs.pop("missing_source_kinds", [RepairProposalEvidenceSourceKind.V0373_TEST_RESULT_ENVELOPE]),
        blocks_future_source_context=kwargs.pop("blocks_future_source_context", True),
        blocks_future_scope_planning=kwargs.pop("blocks_future_scope_planning", True),
        blocks_future_patch_metadata=kwargs.pop("blocks_future_patch_metadata", True),
        requires_human_review=kwargs.pop("requires_human_review", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence policy"]),
        metadata=kwargs.pop("metadata", {}),
    )


def collect_repair_proposal_evidence_items(
    evidence_input: RepairProposalEvidenceInput,
    policy: RepairProposalEvidencePolicy | None = None,
) -> list[RepairProposalEvidenceItem]:
    policy = policy or default_repair_proposal_evidence_policy()
    source_to_item = {
        RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY: RepairProposalEvidenceItemKind.BOUNDARY_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0377_COLD_AGENT_EVALUATION_REPORT: RepairProposalEvidenceItemKind.COLD_SCORECARD_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0377_COLD_AGENT_SCORECARD: RepairProposalEvidenceItemKind.COLD_SCORECARD_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0377_COLD_AGENT_VERDICT: RepairProposalEvidenceItemKind.COLD_VERDICT_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0376_VERA_CODEX_TRIAL_PACKET: RepairProposalEvidenceItemKind.VERA_TRIAL_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0375_REPAIR_SUGGESTION_ENVELOPE: RepairProposalEvidenceItemKind.REPAIR_SUGGESTION_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0374_TEST_FEEDBACK_REPORT: RepairProposalEvidenceItemKind.FEEDBACK_REPORT_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0374_FAILURE_DIAGNOSIS_REPORT: RepairProposalEvidenceItemKind.FAILURE_DIAGNOSIS_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0373_TEST_RESULT_ENVELOPE: RepairProposalEvidenceItemKind.TEST_RESULT_ENVELOPE_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0372_TEST_EXECUTION_RESULT: RepairProposalEvidenceItemKind.TEST_EXECUTION_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION: RepairProposalEvidenceItemKind.PATCH_APPLY_SANDBOX_EVIDENCE,
    }
    items: list[RepairProposalEvidenceItem] = []
    required_sources = {RepairProposalEvidenceSourceKind(item) for item in policy.required_source_kinds}
    for source in evidence_input.source_refs:
        source_kind = RepairProposalEvidenceSourceKind(source.source_kind)
        if source_kind in source_to_item:
            items.append(build_repair_proposal_evidence_item(
                evidence_item_id=f"evidence_item:{source.source_ref_id}",
                evidence_kind=source_to_item[source_kind],
                source_ref_id=source.source_ref_id,
                evidence_summary=source.source_summary,
                required=source_kind in required_sources,
                evidence_strength=RepairProposalEvidenceStrength.ADEQUATE,
                confidence=RepairProposalEvidenceConfidenceLevel.MEDIUM,
            ))
    return items


def identify_repair_proposal_evidence_gaps(
    evidence_items: list[RepairProposalEvidenceItem],
    policy: RepairProposalEvidencePolicy | None = None,
) -> list[RepairProposalEvidenceGap]:
    policy = policy or default_repair_proposal_evidence_policy()
    gaps: list[RepairProposalEvidenceGap] = []
    kind_to_gap = {
        RepairProposalEvidenceItemKind.BOUNDARY_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_BOUNDARY,
        RepairProposalEvidenceItemKind.TEST_RESULT_ENVELOPE_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_TEST_RESULT,
        RepairProposalEvidenceItemKind.FEEDBACK_REPORT_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_FEEDBACK_REPORT,
        RepairProposalEvidenceItemKind.FAILURE_DIAGNOSIS_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_FAILURE_DIAGNOSIS,
        RepairProposalEvidenceItemKind.REPAIR_SUGGESTION_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_REPAIR_SUGGESTION,
        RepairProposalEvidenceItemKind.COLD_SCORECARD_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_COLD_SCORECARD,
        RepairProposalEvidenceItemKind.DO_NOTHING_EVIDENCE: RepairProposalEvidenceGapKind.MISSING_DO_NOTHING_COMPARISON,
    }
    source_to_item = {
        RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY: RepairProposalEvidenceItemKind.BOUNDARY_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0373_TEST_RESULT_ENVELOPE: RepairProposalEvidenceItemKind.TEST_RESULT_ENVELOPE_EVIDENCE,
        RepairProposalEvidenceSourceKind.V0374_TEST_FEEDBACK_REPORT: RepairProposalEvidenceItemKind.FEEDBACK_REPORT_EVIDENCE,
    }
    present_kinds = {RepairProposalEvidenceItemKind(item.evidence_kind) for item in evidence_items if item.present}
    for item in evidence_items:
        if item.contradictory:
            gaps.append(build_repair_proposal_evidence_gap(
                evidence_gap_id=f"contradictory_gap:{item.evidence_item_id}",
                gap_kind=RepairProposalEvidenceGapKind.CONTRADICTORY_FAILURE_EVIDENCE,
                gap_summary="contradictory evidence requires review",
                missing_source_kinds=[],
            ))
        if item.required and not item.present:
            kind = RepairProposalEvidenceItemKind(item.evidence_kind)
            gaps.append(build_repair_proposal_evidence_gap(
                evidence_gap_id=f"missing_gap:{item.evidence_item_id}",
                gap_kind=kind_to_gap.get(kind, RepairProposalEvidenceGapKind.MISSING_FAILURE_EVIDENCE),
                gap_summary="required evidence item is not present",
                missing_source_kinds=[],
            ))
    for source_kind in policy.required_source_kinds:
        item_kind = source_to_item.get(RepairProposalEvidenceSourceKind(source_kind))
        if item_kind is not None and item_kind not in present_kinds:
            gaps.append(build_repair_proposal_evidence_gap(
                evidence_gap_id=f"missing_source_gap:{str(source_kind)}",
                gap_kind=kind_to_gap[item_kind],
                gap_summary="required source kind has no evidence item",
                missing_source_kinds=[RepairProposalEvidenceSourceKind(source_kind)],
            ))
    return gaps


def build_repair_proposal_evidence_assessment(**kwargs: Any) -> RepairProposalEvidenceAssessment:
    evidence_items = kwargs.pop("evidence_items", [build_repair_proposal_evidence_item()])
    evidence_gaps = kwargs.pop("evidence_gaps", [])
    insufficient = kwargs.pop("insufficient_evidence", bool(evidence_gaps))
    contradictory = kwargs.pop("contradictory_evidence", any(
        RepairProposalEvidenceGapKind(gap.gap_kind) == RepairProposalEvidenceGapKind.CONTRADICTORY_FAILURE_EVIDENCE
        for gap in evidence_gaps
    ))
    sufficient_default = not insufficient and not contradictory
    return RepairProposalEvidenceAssessment(
        evidence_assessment_id=kwargs.pop("evidence_assessment_id", "repair_proposal_evidence_assessment:v0.38.1"),
        overall_strength=kwargs.pop("overall_strength", RepairProposalEvidenceStrength.ADEQUATE if sufficient_default else RepairProposalEvidenceStrength.INSUFFICIENT),
        confidence=kwargs.pop("confidence", RepairProposalEvidenceConfidenceLevel.MEDIUM if sufficient_default else RepairProposalEvidenceConfidenceLevel.LOW),
        evidence_items=evidence_items,
        evidence_gaps=evidence_gaps,
        assessment_summary=kwargs.pop("assessment_summary", "evidence assessment metadata only"),
        sufficient_for_future_source_context=kwargs.pop("sufficient_for_future_source_context", sufficient_default),
        sufficient_for_future_scope_planning=kwargs.pop("sufficient_for_future_scope_planning", sufficient_default),
        sufficient_for_future_patch_metadata=kwargs.pop("sufficient_for_future_patch_metadata", sufficient_default),
        insufficient_evidence=insufficient,
        contradictory_evidence=contradictory,
        human_review_required=kwargs.pop("human_review_required", True),
        metadata=kwargs.pop("metadata", {}),
    )


def assess_repair_proposal_evidence(
    evidence_items: list[RepairProposalEvidenceItem],
    evidence_gaps: list[RepairProposalEvidenceGap],
    policy: RepairProposalEvidencePolicy | None = None,
) -> RepairProposalEvidenceAssessment:
    policy = policy or default_repair_proposal_evidence_policy()
    insufficient = bool(evidence_gaps) or any(item.required and not item.present for item in evidence_items)
    contradictory = any(item.contradictory for item in evidence_items) or any(
        RepairProposalEvidenceGapKind(gap.gap_kind) == RepairProposalEvidenceGapKind.CONTRADICTORY_FAILURE_EVIDENCE
        for gap in evidence_gaps
    )
    present_strengths = [RepairProposalEvidenceStrength(item.evidence_strength) for item in evidence_items if item.present and not item.contradictory]
    overall_strength = RepairProposalEvidenceStrength.INSUFFICIENT
    if contradictory:
        overall_strength = RepairProposalEvidenceStrength.CONTRADICTORY
    elif present_strengths:
        min_score = min(STRENGTH_ORDER[str(strength)] for strength in present_strengths)
        overall_strength = RepairProposalEvidenceStrength.ADEQUATE if min_score >= STRENGTH_ORDER["adequate"] else RepairProposalEvidenceStrength.WEAK
    source_ok = not insufficient and not contradictory and _strength_at_least(overall_strength, policy.min_strength_for_future_source_context)
    scope_ok = not insufficient and not contradictory and _strength_at_least(overall_strength, policy.min_strength_for_future_scope_planning)
    patch_ok = not insufficient and not contradictory and _strength_at_least(overall_strength, policy.min_strength_for_future_patch_metadata)
    return build_repair_proposal_evidence_assessment(
        evidence_items=evidence_items,
        evidence_gaps=evidence_gaps,
        overall_strength=overall_strength,
        confidence=RepairProposalEvidenceConfidenceLevel.MEDIUM if source_ok or scope_ok or patch_ok else RepairProposalEvidenceConfidenceLevel.LOW,
        sufficient_for_future_source_context=source_ok,
        sufficient_for_future_scope_planning=scope_ok,
        sufficient_for_future_patch_metadata=patch_ok,
        insufficient_evidence=insufficient,
        contradictory_evidence=contradictory,
        human_review_required=True,
    )


def build_repair_proposal_do_nothing_evidence(**kwargs: Any) -> RepairProposalDoNothingEvidence:
    return RepairProposalDoNothingEvidence(
        do_nothing_evidence_id=kwargs.pop("do_nothing_evidence_id", "repair_proposal_do_nothing_evidence:v0.38.1"),
        do_nothing_kind=kwargs.pop("do_nothing_kind", RepairProposalDoNothingEvidenceKind.DO_NOTHING_NOT_PREFERRED_BUT_STILL_VALID),
        evidence_summary=kwargs.pop("evidence_summary", "do-nothing alternative remains represented"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 do-nothing evidence"]),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        do_nothing_preferred=kwargs.pop("do_nothing_preferred", False),
        do_nothing_required=kwargs.pop("do_nothing_required", False),
        confidence=kwargs.pop("confidence", RepairProposalEvidenceConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def create_repair_proposal_do_nothing_evidence(
    assessment: RepairProposalEvidenceAssessment | None = None,
    *,
    passed_or_no_failure: bool = False,
) -> RepairProposalDoNothingEvidence:
    if passed_or_no_failure:
        return build_repair_proposal_do_nothing_evidence(
            do_nothing_kind=RepairProposalDoNothingEvidenceKind.DO_NOTHING_PREFERRED_DUE_TO_PASSED_TESTS,
            evidence_summary="passed or no-failure evidence makes do-nothing preferred",
            do_nothing_preferred=True,
            confidence=RepairProposalEvidenceConfidenceLevel.HIGH,
        )
    if assessment is not None and assessment.contradictory_evidence:
        return build_repair_proposal_do_nothing_evidence(
            do_nothing_kind=RepairProposalDoNothingEvidenceKind.DO_NOTHING_REQUIRED_DUE_TO_CONTRADICTION,
            evidence_summary="contradictory evidence requires do-nothing until review",
            do_nothing_required=True,
            confidence=RepairProposalEvidenceConfidenceLevel.MEDIUM,
        )
    if assessment is not None and assessment.insufficient_evidence:
        return build_repair_proposal_do_nothing_evidence(
            do_nothing_kind=RepairProposalDoNothingEvidenceKind.DO_NOTHING_REQUIRED_DUE_TO_MISSING_EVIDENCE,
            evidence_summary="missing evidence requires do-nothing until evidence is complete",
            do_nothing_required=True,
            confidence=RepairProposalEvidenceConfidenceLevel.MEDIUM,
        )
    return build_repair_proposal_do_nothing_evidence()


def build_repair_proposal_eligibility_decision(**kwargs: Any) -> RepairProposalEligibilityDecision:
    return RepairProposalEligibilityDecision(
        eligibility_decision_id=kwargs.pop("eligibility_decision_id", "repair_proposal_eligibility_decision:v0.38.1"),
        eligibility_kind=kwargs.pop("eligibility_kind", RepairProposalEligibilityKind.ELIGIBLE_FOR_FUTURE_SOURCE_CONTEXT),
        decision_kind=kwargs.pop("decision_kind", RepairProposalEvidenceDecisionKind.ALLOW_FUTURE_SOURCE_CONTEXT_INPUT),
        decision_summary=kwargs.pop("decision_summary", "future source context input may proceed as metadata only"),
        rationale_summary=kwargs.pop("rationale_summary", "evidence is sufficient for future-gated input; no source read now"),
        evidence_assessment_id=kwargs.pop("evidence_assessment_id", "repair_proposal_evidence_assessment:v0.38.1"),
        do_nothing_evidence_id=kwargs.pop("do_nothing_evidence_id", "repair_proposal_do_nothing_evidence:v0.38.1"),
        confidence=kwargs.pop("confidence", RepairProposalEvidenceConfidenceLevel.MEDIUM),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence assessment"]),
        eligible_for_future_source_context=kwargs.pop("eligible_for_future_source_context", True),
        eligible_for_future_scope_planning=kwargs.pop("eligible_for_future_scope_planning", True),
        eligible_for_future_patch_metadata=kwargs.pop("eligible_for_future_patch_metadata", False),
        human_review_required=kwargs.pop("human_review_required", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_ELIGIBILITY_NOW_NAMES},
    )


def decide_repair_proposal_eligibility(
    assessment: RepairProposalEvidenceAssessment,
    do_nothing_evidence: RepairProposalDoNothingEvidence,
) -> RepairProposalEligibilityDecision:
    if do_nothing_evidence.do_nothing_preferred:
        return build_repair_proposal_eligibility_decision(
            eligibility_kind=RepairProposalEligibilityKind.DO_NOTHING_PREFERRED,
            decision_kind=RepairProposalEvidenceDecisionKind.CHOOSE_DO_NOTHING,
            decision_summary="do-nothing is preferred by passed or no-failure evidence",
            rationale_summary="no repair path should proceed without failure evidence",
            evidence_assessment_id=assessment.evidence_assessment_id,
            do_nothing_evidence_id=do_nothing_evidence.do_nothing_evidence_id,
            eligible_for_future_source_context=False,
            eligible_for_future_scope_planning=False,
            eligible_for_future_patch_metadata=False,
            confidence=do_nothing_evidence.confidence,
        )
    if assessment.contradictory_evidence:
        return build_repair_proposal_eligibility_decision(
            eligibility_kind=RepairProposalEligibilityKind.BLOCKED_BY_CONTRADICTORY_EVIDENCE,
            decision_kind=RepairProposalEvidenceDecisionKind.CONTRADICTORY_EVIDENCE,
            decision_summary="contradictory evidence blocks future proposal inputs",
            rationale_summary="review is required before future source context or patch metadata input",
            evidence_assessment_id=assessment.evidence_assessment_id,
            do_nothing_evidence_id=do_nothing_evidence.do_nothing_evidence_id,
            eligible_for_future_source_context=False,
            eligible_for_future_scope_planning=False,
            eligible_for_future_patch_metadata=False,
            confidence=RepairProposalEvidenceConfidenceLevel.LOW,
        )
    if assessment.insufficient_evidence:
        return build_repair_proposal_eligibility_decision(
            eligibility_kind=RepairProposalEligibilityKind.BLOCKED_BY_INSUFFICIENT_EVIDENCE,
            decision_kind=RepairProposalEvidenceDecisionKind.INSUFFICIENT_EVIDENCE,
            decision_summary="insufficient evidence blocks future proposal inputs",
            rationale_summary="required evidence gaps must be addressed before future-gated inputs",
            evidence_assessment_id=assessment.evidence_assessment_id,
            do_nothing_evidence_id=do_nothing_evidence.do_nothing_evidence_id,
            eligible_for_future_source_context=False,
            eligible_for_future_scope_planning=False,
            eligible_for_future_patch_metadata=False,
            confidence=RepairProposalEvidenceConfidenceLevel.LOW,
        )
    return build_repair_proposal_eligibility_decision(
        evidence_assessment_id=assessment.evidence_assessment_id,
        do_nothing_evidence_id=do_nothing_evidence.do_nothing_evidence_id,
        eligible_for_future_source_context=assessment.sufficient_for_future_source_context,
        eligible_for_future_scope_planning=assessment.sufficient_for_future_scope_planning,
        eligible_for_future_patch_metadata=assessment.sufficient_for_future_patch_metadata,
        confidence=assessment.confidence,
    )


def build_repair_proposal_evidence_contract(**kwargs: Any) -> RepairProposalEvidenceContract:
    return RepairProposalEvidenceContract(
        evidence_contract_id=kwargs.pop("evidence_contract_id", "repair_proposal_evidence_contract:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        evidence_input_id=kwargs.pop("evidence_input_id", "repair_proposal_evidence_input:v0.38.1"),
        policy=kwargs.pop("policy", default_repair_proposal_evidence_policy()),
        required_evidence_kinds=kwargs.pop("required_evidence_kinds", [
            RepairProposalEvidenceItemKind.BOUNDARY_EVIDENCE,
            RepairProposalEvidenceItemKind.TEST_RESULT_ENVELOPE_EVIDENCE,
            RepairProposalEvidenceItemKind.FEEDBACK_REPORT_EVIDENCE,
            RepairProposalEvidenceItemKind.DO_NOTHING_EVIDENCE,
        ]),
        optional_evidence_kinds=kwargs.pop("optional_evidence_kinds", [
            RepairProposalEvidenceItemKind.FAILURE_DIAGNOSIS_EVIDENCE,
            RepairProposalEvidenceItemKind.REPAIR_SUGGESTION_EVIDENCE,
            RepairProposalEvidenceItemKind.COLD_SCORECARD_EVIDENCE,
            RepairProposalEvidenceItemKind.VERA_TRIAL_EVIDENCE,
        ]),
        accepted_source_kinds=kwargs.pop("accepted_source_kinds", [
            RepairProposalEvidenceSourceKind.V0380_REPAIR_PROPOSAL_BOUNDARY,
            RepairProposalEvidenceSourceKind.V0379_TEST_RUNNER_CONSOLIDATION,
            RepairProposalEvidenceSourceKind.V0377_COLD_AGENT_EVALUATION_REPORT,
            RepairProposalEvidenceSourceKind.V0377_COLD_AGENT_SCORECARD,
            RepairProposalEvidenceSourceKind.V0376_VERA_CODEX_TRIAL_PACKET,
            RepairProposalEvidenceSourceKind.V0375_REPAIR_SUGGESTION_ENVELOPE,
            RepairProposalEvidenceSourceKind.V0374_TEST_FEEDBACK_REPORT,
            RepairProposalEvidenceSourceKind.V0374_FAILURE_DIAGNOSIS_REPORT,
            RepairProposalEvidenceSourceKind.V0373_TEST_RESULT_ENVELOPE,
            RepairProposalEvidenceSourceKind.V0372_TEST_EXECUTION_RESULT,
        ]),
        rejected_source_kinds=kwargs.pop("rejected_source_kinds", [RepairProposalEvidenceSourceKind.UNKNOWN]),
        contract_summary=kwargs.pop("contract_summary", "repair proposal evidence contract metadata only"),
        requires_boundary=kwargs.pop("requires_boundary", True),
        requires_test_result=kwargs.pop("requires_test_result", True),
        requires_feedback_or_diagnosis=kwargs.pop("requires_feedback_or_diagnosis", True),
        requires_do_nothing_evidence=kwargs.pop("requires_do_nothing_evidence", True),
        requires_human_review_marker=kwargs.pop("requires_human_review_marker", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_CONTRACT_NOW_NAMES},
    )


def create_repair_proposal_evidence_contract(
    evidence_input: RepairProposalEvidenceInput,
    policy: RepairProposalEvidencePolicy | None = None,
) -> RepairProposalEvidenceContract:
    return build_repair_proposal_evidence_contract(
        evidence_input_id=evidence_input.evidence_input_id,
        policy=policy or default_repair_proposal_evidence_policy(),
    )


def build_repair_proposal_evidence_bundle(**kwargs: Any) -> RepairProposalEvidenceBundle:
    assessment = kwargs.pop("evidence_assessment", build_repair_proposal_evidence_assessment())
    do_nothing = kwargs.pop("do_nothing_evidence", create_repair_proposal_do_nothing_evidence(assessment))
    decision = kwargs.pop("eligibility_decision", decide_repair_proposal_eligibility(assessment, do_nothing))
    return RepairProposalEvidenceBundle(
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        evidence_contract_id=kwargs.pop("evidence_contract_id", "repair_proposal_evidence_contract:v0.38.1"),
        evidence_items=kwargs.pop("evidence_items", assessment.evidence_items),
        evidence_gaps=kwargs.pop("evidence_gaps", assessment.evidence_gaps),
        do_nothing_evidence=do_nothing,
        evidence_assessment=assessment,
        eligibility_decision=decision,
        source_refs=kwargs.pop("source_refs", [build_repair_proposal_evidence_source_ref()]),
        bundle_summary=kwargs.pop("bundle_summary", "repair proposal evidence bundle metadata only"),
        ready_for_future_source_context_input=kwargs.pop("ready_for_future_source_context_input", decision.eligible_for_future_source_context),
        ready_for_future_scope_planning_input=kwargs.pop("ready_for_future_scope_planning_input", decision.eligible_for_future_scope_planning),
        ready_for_future_patch_metadata_input=kwargs.pop("ready_for_future_patch_metadata_input", decision.eligible_for_future_patch_metadata),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_BUNDLE_STATE_NAMES},
    )


def create_repair_proposal_evidence_bundle(
    evidence_input: RepairProposalEvidenceInput,
    policy: RepairProposalEvidencePolicy | None = None,
) -> RepairProposalEvidenceBundle:
    policy = policy or default_repair_proposal_evidence_policy()
    contract = create_repair_proposal_evidence_contract(evidence_input, policy)
    items = collect_repair_proposal_evidence_items(evidence_input, policy)
    do_nothing_item = build_repair_proposal_evidence_item(
        evidence_item_id="evidence_item:do_nothing:v0.38.1",
        evidence_kind=RepairProposalEvidenceItemKind.DO_NOTHING_EVIDENCE,
        source_ref_id=None,
        evidence_summary="do-nothing comparison is represented",
        required=True,
        present=True,
        evidence_use=RepairProposalEvidenceUseKind.SUPPORTS_DO_NOTHING,
    )
    items = [*items, do_nothing_item]
    gaps = identify_repair_proposal_evidence_gaps(items, policy)
    assessment = assess_repair_proposal_evidence(items, gaps, policy)
    do_nothing = create_repair_proposal_do_nothing_evidence(assessment)
    decision = decide_repair_proposal_eligibility(assessment, do_nothing)
    return build_repair_proposal_evidence_bundle(
        evidence_contract_id=contract.evidence_contract_id,
        evidence_items=items,
        evidence_gaps=gaps,
        do_nothing_evidence=do_nothing,
        evidence_assessment=assessment,
        eligibility_decision=decision,
        source_refs=evidence_input.source_refs,
    )


def build_repair_proposal_evidence_validation_finding(**kwargs: Any) -> RepairProposalEvidenceValidationFinding:
    return RepairProposalEvidenceValidationFinding(
        finding_id=kwargs.pop("finding_id", "repair_proposal_evidence_validation_finding:v0.38.1"),
        finding_summary=kwargs.pop("finding_summary", "evidence bundle preserves no generation"),
        risk_kind=kwargs.pop("risk_kind", RepairProposalEvidenceRiskKind.REPAIR_PROPOSAL_GENERATION_CONFUSION_RISK),
        decision_kind=kwargs.pop("decision_kind", RepairProposalEvidenceDecisionKind.ALLOW_EVIDENCE_BUNDLE),
        blocks_future_source_context=kwargs.pop("blocks_future_source_context", False),
        blocks_future_scope_planning=kwargs.pop("blocks_future_scope_planning", False),
        blocks_future_patch_metadata=kwargs.pop("blocks_future_patch_metadata", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_evidence_validation_report(**kwargs: Any) -> RepairProposalEvidenceValidationReport:
    return RepairProposalEvidenceValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "repair_proposal_evidence_validation_report:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"),
        findings=kwargs.pop("findings", [build_repair_proposal_evidence_validation_finding()]),
        validation_summary=kwargs.pop("validation_summary", "evidence validation report confirms metadata-only posture"),
        evidence_contract_confirmed=kwargs.pop("evidence_contract_confirmed", True),
        evidence_gaps_confirmed=kwargs.pop("evidence_gaps_confirmed", True),
        do_nothing_evidence_confirmed=kwargs.pop("do_nothing_evidence_confirmed", True),
        no_source_read_confirmed=kwargs.pop("no_source_read_confirmed", True),
        no_proposal_generation_confirmed=kwargs.pop("no_proposal_generation_confirmed", True),
        no_diff_generation_confirmed=kwargs.pop("no_diff_generation_confirmed", True),
        no_hunk_generation_confirmed=kwargs.pop("no_hunk_generation_confirmed", True),
        no_patch_envelope_generation_confirmed=kwargs.pop("no_patch_envelope_generation_confirmed", True),
        no_repair_execution_confirmed=kwargs.pop("no_repair_execution_confirmed", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def validate_repair_proposal_evidence_bundle(bundle: RepairProposalEvidenceBundle) -> RepairProposalEvidenceValidationReport:
    return build_repair_proposal_evidence_validation_report(
        evidence_bundle_id=bundle.evidence_bundle_id,
        findings=[build_repair_proposal_evidence_validation_finding()],
    )


def build_repair_proposal_evidence_report(**kwargs: Any) -> RepairProposalEvidenceReport:
    bundle = kwargs.pop("bundle", None)
    validation_report = kwargs.pop("validation_report", None)
    return RepairProposalEvidenceReport(
        evidence_report_id=kwargs.pop("evidence_report_id", "repair_proposal_evidence_report:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", bundle.evidence_bundle_id if bundle else "repair_proposal_evidence_bundle:v0.38.1"),
        validation_report_id=kwargs.pop("validation_report_id", validation_report.validation_report_id if validation_report else "repair_proposal_evidence_validation_report:v0.38.1"),
        readiness_level=kwargs.pop("readiness_level", RepairProposalEvidenceReadinessLevel.EVIDENCE_BUNDLE_READY),
        status=kwargs.pop("status", RepairProposalEvidenceStatus.BUNDLE_CREATED),
        report_summary=kwargs.pop("report_summary", "repair proposal evidence report metadata only"),
        ready_for_future_source_context_input=kwargs.pop("ready_for_future_source_context_input", bundle.ready_for_future_source_context_input if bundle else True),
        ready_for_future_scope_planning_input=kwargs.pop("ready_for_future_scope_planning_input", bundle.ready_for_future_scope_planning_input if bundle else True),
        ready_for_future_patch_metadata_input=kwargs.pop("ready_for_future_patch_metadata_input", bundle.ready_for_future_patch_metadata_input if bundle else False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 evidence bundle"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_evidence_run_preview(**kwargs: Any) -> RepairProposalEvidenceRunPreview:
    return RepairProposalEvidenceRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "repair_proposal_evidence_run_preview:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        requested_mode=kwargs.pop("requested_mode", RepairProposalEvidenceMode.EVIDENCE_BUNDLE),
        preview_summary=kwargs.pop("preview_summary", "would create evidence metadata only"),
        would_create_contract=kwargs.pop("would_create_contract", True),
        would_create_bundle=kwargs.pop("would_create_bundle", True),
        would_assess_evidence=kwargs.pop("would_assess_evidence", True),
        would_decide_eligibility=kwargs.pop("would_decide_eligibility", True),
        would_read_source=kwargs.pop("would_read_source", False),
        would_generate_proposal=kwargs.pop("would_generate_proposal", False),
        would_generate_diff=kwargs.pop("would_generate_diff", False),
        would_generate_hunk=kwargs.pop("would_generate_hunk", False),
        would_execute_repair=kwargs.pop("would_execute_repair", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_evidence_no_generation_guarantee(**kwargs: Any) -> RepairProposalEvidenceNoGenerationGuarantee:
    no_names = tuple(name for name in RepairProposalEvidenceNoGenerationGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return RepairProposalEvidenceNoGenerationGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_proposal_evidence_no_generation_guarantee:v0.38.1"),
        version=kwargs.pop("version", V0381_VERSION),
        summary=kwargs.pop("summary", "v0.38.1 creates evidence metadata only"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0381_readiness_report(**kwargs: Any) -> V0381ReadinessReport:
    safe_defaults = {
        "repair_proposal_evidence_layer_constructed": True,
        "ready_for_v0382_read_only_sandbox_source_context": True,
        "ready_for_v0383_repair_scope_planner_change_intent": True,
        "ready_for_v0384_proposed_diff_code_hunk_metadata": True,
        "ready_for_repair_proposal_evidence_contract": True,
        "ready_for_repair_proposal_evidence_bundle": True,
        "ready_for_repair_proposal_evidence_assessment": True,
        "ready_for_repair_proposal_eligibility_decision": True,
        "ready_for_repair_proposal_evidence_gap_register": True,
        "ready_for_repair_proposal_do_nothing_evidence": True,
        "ready_for_future_read_only_sandbox_source_context_input": True,
        "ready_for_future_repair_scope_planning_input": True,
        "ready_for_future_change_intent_input": True,
        "ready_for_future_proposed_diff_metadata_input": True,
        "ready_for_future_proposed_code_hunk_metadata_input": True,
    }
    return V0381ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0381_readiness_report"),
        version=kwargs.pop("version", V0381_VERSION),
        evidence_contract_id=kwargs.pop("evidence_contract_id", "repair_proposal_evidence_contract:v0.38.1"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"),
        readiness_level=kwargs.pop("readiness_level", RepairProposalEvidenceReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0382),
        status=kwargs.pop("status", RepairProposalEvidenceStatus.BUNDLE_CREATED),
        summary=kwargs.pop("summary", "v0.38.1 evidence contract ready; source read, generation, and execution remain false"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.0 boundary", "v0.37.9 consolidation"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_EVIDENCE_FLAG_NAMES if name in V0381ReadinessReport.__dataclass_fields__},
    )


def repair_proposal_evidence_flags_preserve_no_generation(flags: RepairProposalEvidenceFlagSet) -> bool:
    return isinstance(flags, RepairProposalEvidenceFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_EVIDENCE_FLAG_NAMES)


def repair_proposal_evidence_policy_blocks_generation(policy: RepairProposalEvidencePolicy) -> bool:
    return isinstance(policy, RepairProposalEvidencePolicy) and all(getattr(policy, name) is False for name in UNSAFE_EVIDENCE_POLICY_ALLOW_NAMES)


def repair_proposal_evidence_bundle_is_not_proposal(bundle: RepairProposalEvidenceBundle) -> bool:
    return isinstance(bundle, RepairProposalEvidenceBundle) and all(getattr(bundle, name) is False for name in UNSAFE_BUNDLE_STATE_NAMES)


def repair_proposal_eligibility_is_not_permission(decision: RepairProposalEligibilityDecision) -> bool:
    return isinstance(decision, RepairProposalEligibilityDecision) and all(getattr(decision, name) is False for name in UNSAFE_ELIGIBILITY_NOW_NAMES)


def v0381_readiness_report_is_not_execution_ready(report: V0381ReadinessReport) -> bool:
    return isinstance(report, V0381ReadinessReport) and all(
        getattr(report, name) is False for name in UNSAFE_EVIDENCE_FLAG_NAMES if hasattr(report, name)
    )
