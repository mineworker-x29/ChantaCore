from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .sandbox_test_feedback import (
    SandboxDoNothingSignalKind,
    SandboxEvidenceStrength,
    SandboxFeedbackConfidenceLevel,
    SandboxRootCauseHypothesisKind,
    SandboxSuggestedNextActionKind,
    SandboxTestFeedbackReport,
)


V0375_VERSION = "v0.37.5"
V0375_RELEASE_NAME = "v0.37.5 Repair Suggestion Metadata, No Auto-Repair"


UNSAFE_REPAIR_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_pytest_execution",
    "ready_for_npm_test_execution",
    "ready_for_unittest_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_repair_patch_proposal",
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_vera_codex_trial_execution",
    "ready_for_cold_agent_performance_evaluation",
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

UNSAFE_REPAIR_POLICY_ALLOW_NAMES = (
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_repair_patch_proposal",
    "allow_repair_diff_generation",
    "allow_code_hunk_generation",
    "allow_automatic_repair",
    "allow_repair_execution",
    "allow_vera_codex_trial_execution",
    "allow_cold_performance_evaluation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_metadata(value: dict[str, Any]) -> None:
    _validate_dict("metadata", value)


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0375_VERSION not in version:
        raise ValueError("version must include v0.37.5")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.5")


def _validate_true(name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{name} must be True")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _limit_text(text: str, limit: int) -> str:
    _validate_non_negative("limit", limit)
    return text[:limit]


class SandboxRepairSuggestionMode(StrEnum):
    METADATA_ONLY_SUGGESTION = "metadata_only_suggestion"
    EVIDENCE_BASED_REPAIR_HINT = "evidence_based_repair_hint"
    SCOPE_ONLY_REPAIR_HINT = "scope_only_repair_hint"
    HUMAN_REVIEW_REPAIR_HINT = "human_review_repair_hint"
    DO_NOTHING_COMPARISON_HINT = "do_nothing_comparison_hint"
    FUTURE_REPAIR_PROPOSAL_INPUT = "future_repair_proposal_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class SandboxRepairSuggestionSourceKind(StrEnum):
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0374_FAILURE_DIAGNOSIS_REPORT = "v0374_failure_diagnosis_report"
    V0374_ROOT_CAUSE_HYPOTHESIS = "v0374_root_cause_hypothesis"
    V0374_SUGGESTED_NEXT_ACTION = "v0374_suggested_next_action"
    V0374_DO_NOTHING_SIGNAL = "v0374_do_nothing_signal"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    V0373_FAILURE_CLASSIFICATION = "v0373_failure_classification"
    V0372_TEST_EXECUTION_RESULT = "v0372_test_execution_result"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    MANUAL_OPERATOR_INPUT = "manual_operator_input"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class SandboxRepairSuggestionStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    SUGGESTION_CREATED = "suggestion_created"
    SUGGESTION_CREATED_WITH_WARNINGS = "suggestion_created_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class SandboxRepairSuggestionReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SUGGESTION_CONTRACT_READY = "suggestion_contract_ready"
    REPAIR_SCOPE_METADATA_READY = "repair_scope_metadata_ready"
    REPAIR_RISK_ASSESSMENT_READY = "repair_risk_assessment_ready"
    HUMAN_REVIEW_REQUIREMENT_READY = "human_review_requirement_ready"
    FUTURE_REPAIR_PROPOSAL_INPUT_READY = "future_repair_proposal_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0376 = "design_handoff_ready_for_v0376"
    DESIGN_HANDOFF_READY_FOR_V0377 = "design_handoff_ready_for_v0377"
    DESIGN_HANDOFF_READY_FOR_V0378 = "design_handoff_ready_for_v0378"
    FUTURE_HANDOFF_READY_FOR_V038 = "future_handoff_ready_for_v038"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class SandboxRepairSuggestionDecisionKind(StrEnum):
    ALLOW_REPAIR_SUGGESTION_METADATA = "allow_repair_suggestion_metadata"
    ALLOW_REPAIR_SCOPE_METADATA = "allow_repair_scope_metadata"
    ALLOW_REPAIR_RISK_ASSESSMENT = "allow_repair_risk_assessment"
    ALLOW_HUMAN_REVIEW_REQUIREMENT = "allow_human_review_requirement"
    ALLOW_DO_NOTHING_COMPARISON = "allow_do_nothing_comparison"
    ALLOW_FUTURE_REPAIR_PROPOSAL_INPUT = "allow_future_repair_proposal_input"
    ALLOW_FUTURE_VERA_CODEX_TRIAL_INPUT = "allow_future_vera_codex_trial_input"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class SandboxRepairSuggestionRiskKind(StrEnum):
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    OVERCONFIDENT_REPAIR_SUGGESTION_RISK = "overconfident_repair_suggestion_risk"
    REPAIR_PATCH_CONFUSION_RISK = "repair_patch_confusion_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DEPENDENCY_INSTALL_CONFUSION_RISK = "dependency_install_confusion_risk"
    TIMEOUT_RETRY_CONFUSION_RISK = "timeout_retry_confusion_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    HUMAN_REVIEW_OMISSION_RISK = "human_review_omission_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class SandboxRepairSuggestionKind(StrEnum):
    NO_REPAIR_NEEDED = "no_repair_needed"
    INVESTIGATE_ONLY = "investigate_only"
    UPDATE_TEST_EXPECTATION_FUTURE_GATE = "update_test_expectation_future_gate"
    REVISE_IMPLEMENTATION_FUTURE_GATE = "revise_implementation_future_gate"
    ADJUST_IMPORT_PATH_FUTURE_GATE = "adjust_import_path_future_gate"
    INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL = "inspect_missing_dependency_without_install"
    INSPECT_TIMEOUT_OR_PERFORMANCE_FUTURE_GATE = "inspect_timeout_or_performance_future_gate"
    UPDATE_ALLOWLIST_FUTURE_GATE = "update_allowlist_future_gate"
    BLOCK_DUE_TO_INSUFFICIENT_EVIDENCE = "block_due_to_insufficient_evidence"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    UNKNOWN = "unknown"


class SandboxRepairScopeKind(StrEnum):
    NO_SCOPE = "no_scope"
    TEST_SCOPE = "test_scope"
    IMPLEMENTATION_SCOPE = "implementation_scope"
    IMPORT_PATH_SCOPE = "import_path_scope"
    CONFIGURATION_SCOPE = "configuration_scope"
    ALLOWLIST_POLICY_SCOPE = "allowlist_policy_scope"
    SANDBOX_ENVIRONMENT_SCOPE = "sandbox_environment_scope"
    DOCUMENTATION_SCOPE = "documentation_scope"
    UNKNOWN_SCOPE = "unknown_scope"


class SandboxRepairActionKind(StrEnum):
    NO_ACTION = "no_action"
    DO_NOTHING = "do_nothing"
    REQUEST_HUMAN_REVIEW = "request_human_review"
    PREPARE_FUTURE_REPAIR_PROPOSAL_INPUT = "prepare_future_repair_proposal_input"
    INSPECT_EVIDENCE = "inspect_evidence"
    INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL = "inspect_missing_dependency_without_install"
    INSPECT_TIMEOUT_WITHOUT_RETRY = "inspect_timeout_without_retry"
    SUGGEST_TEST_EXPECTATION_REVIEW = "suggest_test_expectation_review"
    SUGGEST_IMPLEMENTATION_REVIEW = "suggest_implementation_review"
    SUGGEST_ALLOWLIST_REVIEW = "suggest_allowlist_review"
    BLOCK_AND_INVESTIGATE = "block_and_investigate"
    UNKNOWN = "unknown"


class SandboxRepairEvidenceKind(StrEnum):
    FEEDBACK_REPORT_REF = "feedback_report_ref"
    DIAGNOSIS_REPORT_REF = "diagnosis_report_ref"
    ROOT_CAUSE_HYPOTHESIS_REF = "root_cause_hypothesis_ref"
    TEST_RESULT_ENVELOPE_REF = "test_result_envelope_ref"
    FAILURE_CLASSIFICATION_REF = "failure_classification_ref"
    OUTCOME_CLASSIFICATION_REF = "outcome_classification_ref"
    EVIDENCE_SNIPPET_REF = "evidence_snippet_ref"
    DO_NOTHING_SIGNAL_REF = "do_nothing_signal_ref"
    HUMAN_OPERATOR_NOTE = "human_operator_note"
    UNKNOWN = "unknown"


class SandboxRepairUrgency(StrEnum):
    NONE = "none"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class SandboxRepairConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class SandboxRepairReviewRequirementKind(StrEnum):
    NO_REVIEW_REQUIRED_FOR_NO_OP = "no_review_required_for_no_op"
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    HUMAN_REVIEW_REQUIRED_DUE_TO_RISK = "human_review_required_due_to_risk"
    HUMAN_REVIEW_REQUIRED_DUE_TO_LOW_CONFIDENCE = "human_review_required_due_to_low_confidence"
    HUMAN_REVIEW_REQUIRED_BEFORE_FUTURE_REPAIR_PROPOSAL = "human_review_required_before_future_repair_proposal"
    HUMAN_REVIEW_REQUIRED_BEFORE_ANY_APPLY = "human_review_required_before_any_apply"
    UNKNOWN = "unknown"


class SandboxRepairDoNothingComparisonKind(StrEnum):
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    DO_NOTHING_COMPETITIVE = "do_nothing_competitive"
    DO_NOTHING_INFERIOR = "do_nothing_inferior"
    DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE = "do_nothing_required_due_to_insufficient_evidence"
    DO_NOTHING_REQUIRED_DUE_TO_RISK = "do_nothing_required_due_to_risk"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SandboxRepairSuggestionFlagSet:
    flag_set_id: str
    version: str
    repair_suggestion_layer_constructed: bool
    repair_suggestion_metadata_available: bool
    repair_scope_metadata_available: bool
    repair_risk_assessment_available: bool
    repair_human_review_requirement_available: bool
    do_nothing_repair_comparison_available: bool
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_v0378_cli_test_runner_agent_evaluation_surface: bool
    ready_for_v038_bounded_repair_proposal_loop: bool
    ready_for_repair_suggestion_metadata: bool
    ready_for_repair_scope_metadata: bool
    ready_for_repair_risk_assessment: bool
    ready_for_repair_human_review_requirement: bool
    ready_for_do_nothing_repair_comparison: bool
    ready_for_future_repair_proposal_input: bool
    ready_for_future_vera_codex_trial_input: bool
    ready_for_future_cold_evaluation_input: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_pytest_execution: bool
    ready_for_npm_test_execution: bool
    ready_for_unittest_execution: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_automatic_repair: bool
    ready_for_repair_execution: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_vera_codex_trial_execution: bool
    ready_for_cold_agent_performance_evaluation: bool
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
        for name in UNSAFE_REPAIR_FLAG_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionSourceRef:
    source_ref_id: str
    source_kind: SandboxRepairSuggestionSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionPolicy:
    repair_policy_id: str
    version: str
    allowed_modes: list[SandboxRepairSuggestionMode | str]
    max_suggestions: int
    max_evidence_refs: int
    max_summary_chars: int
    require_feedback_report: bool
    require_evidence_refs: bool
    require_confidence_level: bool
    require_risk_assessment: bool
    require_human_review_requirement: bool
    require_do_nothing_comparison: bool
    allow_repair_suggestion_metadata: bool
    allow_scope_metadata: bool
    allow_risk_assessment: bool
    allow_human_review_requirement: bool
    allow_future_repair_proposal_input: bool
    allow_test_execution: bool
    allow_subprocess: bool
    allow_shell: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_repair_patch_proposal: bool
    allow_repair_diff_generation: bool
    allow_code_hunk_generation: bool
    allow_automatic_repair: bool
    allow_repair_execution: bool
    allow_vera_codex_trial_execution: bool
    allow_cold_performance_evaluation: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_policy_id", self.repair_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_modes", self.allowed_modes)
        for name in ("max_suggestions", "max_evidence_refs", "max_summary_chars"):
            _validate_non_negative(name, getattr(self, name))
        for name in (
            "require_feedback_report",
            "require_evidence_refs",
            "require_confidence_level",
            "require_risk_assessment",
            "require_human_review_requirement",
            "require_do_nothing_comparison",
        ):
            _validate_true(name, getattr(self, name))
        for name in UNSAFE_REPAIR_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionInput:
    repair_input_id: str
    version: str
    feedback_report_id: str | None
    diagnosis_report_id: str | None
    result_envelope_id: str | None
    requested_mode: SandboxRepairSuggestionMode | str
    source_refs: list[SandboxRepairSuggestionSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_input_id", self.repair_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"patch proposal", "diff generation", "code edit", "apply", "test execution", "subprocess", "shell", "install", "network", "repair execution", "external agent", "Dominion"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include v0.37.5 unsafe actions")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairEvidenceRef:
    repair_evidence_id: str
    evidence_kind: SandboxRepairEvidenceKind | str
    source_id: str | None
    evidence_summary: str
    evidence_strength: str
    confidence: SandboxRepairConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_evidence_id", self.repair_evidence_id)
        _require_non_blank("evidence_summary", self.evidence_summary)
        _require_non_blank("evidence_strength", self.evidence_strength)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairScope:
    repair_scope_id: str
    scope_kind: SandboxRepairScopeKind | str
    scope_summary: str
    candidate_paths: list[str]
    candidate_symbols: list[str]
    scope_confidence: SandboxRepairConfidenceLevel | str
    edit_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_scope_id", self.repair_scope_id)
        _require_non_blank("scope_summary", self.scope_summary)
        _validate_string_list("candidate_paths", self.candidate_paths)
        _validate_string_list("candidate_symbols", self.candidate_symbols)
        _validate_false("edit_allowed", self.edit_allowed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairRiskAssessment:
    risk_assessment_id: str
    risk_kinds: list[SandboxRepairSuggestionRiskKind | str]
    severity: str
    risk_summary: str
    requires_human_review: bool
    blocks_future_repair_proposal: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_assessment_id", self.risk_assessment_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("risk_summary", self.risk_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        if self.severity in ("high", "critical", "blocked") and not self.requires_human_review:
            raise ValueError("high repair suggestion risk requires human review")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairDoNothingComparison:
    do_nothing_comparison_id: str
    comparison_kind: SandboxRepairDoNothingComparisonKind | str
    comparison_summary: str
    evidence_refs: list[str]
    do_nothing_remains_valid: bool
    repair_suggestion_outperforms_do_nothing: bool
    scoring_performed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("do_nothing_comparison_id", self.do_nothing_comparison_id)
        _require_non_blank("comparison_summary", self.comparison_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false("scoring_performed", self.scoring_performed)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairHumanReviewRequirement:
    review_requirement_id: str
    requirement_kind: SandboxRepairReviewRequirementKind | str
    requirement_summary: str
    required_before_future_repair_proposal: bool
    required_before_any_apply: bool
    human_approval_present: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("review_requirement_id", self.review_requirement_id)
        _require_non_blank("requirement_summary", self.requirement_summary)
        _validate_false("human_approval_present", self.human_approval_present)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestedAction:
    repair_action_id: str
    action_kind: SandboxRepairActionKind | str
    action_summary: str
    rationale: str
    evidence_refs: list[SandboxRepairEvidenceRef]
    future_gated: bool
    executes_now: bool
    generates_patch: bool
    edits_code: bool
    applies_patch: bool
    runs_tests: bool
    installs_dependency: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_action_id", self.repair_action_id)
        _require_non_blank("action_summary", self.action_summary)
        _require_non_blank("rationale", self.rationale)
        _validate_list("evidence_refs", self.evidence_refs)
        for name in ("executes_now", "generates_patch", "edits_code", "applies_patch", "runs_tests", "installs_dependency"):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionEnvelope:
    repair_suggestion_id: str
    version: str
    repair_input_id: str
    status: SandboxRepairSuggestionStatus | str
    readiness_level: SandboxRepairSuggestionReadinessLevel | str
    suggestion_kind: SandboxRepairSuggestionKind | str
    scope: SandboxRepairScope
    evidence_refs: list[SandboxRepairEvidenceRef]
    risk_assessment: SandboxRepairRiskAssessment
    do_nothing_comparison: SandboxRepairDoNothingComparison
    human_review_requirement: SandboxRepairHumanReviewRequirement
    suggested_actions: list[SandboxRepairSuggestedAction]
    source_refs: list[SandboxRepairSuggestionSourceRef]
    suggestion_summary: str
    urgency: SandboxRepairUrgency | str
    confidence: SandboxRepairConfidenceLevel | str
    eligible_for_future_repair_proposal: bool
    eligible_for_future_vera_codex_trial: bool
    eligible_for_future_cold_evaluation: bool
    repair_patch_proposal_created: bool
    repair_diff_generated: bool
    code_hunk_generated: bool
    repair_executed: bool
    tests_rerun: bool
    dependency_install_allowed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("repair_suggestion_id", self.repair_suggestion_id)
        _validate_version(self.version)
        _require_non_blank("repair_input_id", self.repair_input_id)
        _require_non_blank("suggestion_summary", self.suggestion_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_list("suggested_actions", self.suggested_actions)
        _validate_list("source_refs", self.source_refs)
        for name in (
            "repair_patch_proposal_created",
            "repair_diff_generated",
            "code_hunk_generated",
            "repair_executed",
            "tests_rerun",
            "dependency_install_allowed",
            "production_certified",
            "ready_for_execution",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionDecision:
    decision_id: str
    repair_input_id: str
    decision_kind: SandboxRepairSuggestionDecisionKind | str
    status: SandboxRepairSuggestionStatus | str
    risk_kinds: list[SandboxRepairSuggestionRiskKind | str]
    decision_summary: str
    repair_suggestion_metadata_allowed: bool
    repair_scope_metadata_allowed: bool
    repair_risk_assessment_allowed: bool
    human_review_requirement_allowed: bool
    do_nothing_comparison_allowed: bool
    future_repair_proposal_input_allowed: bool
    future_vera_codex_trial_input_allowed: bool
    patch_proposal_allowed: bool
    diff_generation_allowed: bool
    code_hunk_generation_allowed: bool
    file_edit_allowed: bool
    patch_apply_allowed: bool
    test_execution_allowed: bool
    subprocess_allowed: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_allowed: bool
    repair_execution_allowed: bool
    vera_codex_trial_execution_allowed: bool
    external_agent_allowed: bool
    dominion_runtime_allowed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("repair_input_id", self.repair_input_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        for name in (
            "patch_proposal_allowed",
            "diff_generation_allowed",
            "code_hunk_generation_allowed",
            "file_edit_allowed",
            "patch_apply_allowed",
            "test_execution_allowed",
            "subprocess_allowed",
            "shell_allowed",
            "dependency_install_allowed",
            "network_allowed",
            "repair_execution_allowed",
            "vera_codex_trial_execution_allowed",
            "external_agent_allowed",
            "dominion_runtime_allowed",
        ):
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionValidationFinding:
    finding_id: str
    risk_kind: SandboxRepairSuggestionRiskKind | str
    severity: str
    message: str
    blocks_suggestion: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("severity", self.severity)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionValidationReport:
    validation_report_id: str
    version: str
    repair_suggestion_id: str
    findings: list[SandboxRepairSuggestionValidationFinding]
    evidence_refs_confirmed: bool
    confidence_confirmed: bool
    do_nothing_comparison_confirmed: bool
    human_review_requirement_confirmed: bool
    no_patch_diff_hunk_confirmed: bool
    no_repair_execution_confirmed: bool
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("repair_suggestion_id", self.repair_suggestion_id)
        _require_non_blank("summary", self.summary)
        _validate_list("findings", self.findings)
        for name in (
            "evidence_refs_confirmed",
            "confidence_confirmed",
            "do_nothing_comparison_confirmed",
            "human_review_requirement_confirmed",
            "no_patch_diff_hunk_confirmed",
            "no_repair_execution_confirmed",
        ):
            _validate_true(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionReport:
    report_id: str
    version: str
    repair_suggestion: SandboxRepairSuggestionEnvelope
    validation_report: SandboxRepairSuggestionValidationReport
    report_summary: str
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _require_non_blank("report_summary", self.report_summary)
        _validate_false("production_certified", self.production_certified)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionRunPreview:
    run_preview_id: str
    version: str
    repair_input_id: str
    preview_summary: str
    ready_for_repair_suggestion_metadata: bool
    ready_for_repair_patch_proposal: bool
    ready_for_test_execution: bool
    ready_for_repair_execution: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("repair_input_id", self.repair_input_id)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_false("ready_for_repair_patch_proposal", self.ready_for_repair_patch_proposal)
        _validate_false("ready_for_test_execution", self.ready_for_test_execution)
        _validate_false("ready_for_repair_execution", self.ready_for_repair_execution)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class SandboxRepairSuggestionNoAutoRepairGuarantee:
    guarantee_id: str
    version: str
    no_repair_patch_proposal: bool
    no_unified_diff: bool
    no_code_hunk_generation: bool
    no_file_edit: bool
    no_patch_application: bool
    no_apply_patch_call: bool
    no_git_apply_call: bool
    no_test_execution: bool
    no_controlled_test_subprocess: bool
    no_shell_execution: bool
    no_subprocess_execution: bool
    no_command_execution: bool
    no_dependency_install: bool
    no_network_access: bool
    no_automatic_repair: bool
    no_repair_execution: bool
    no_retry_loop: bool
    no_multi_cycle_loop: bool
    no_vera_codex_trial_execution: bool
    no_cold_performance_evaluation_execution: bool
    no_provider_invocation: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    no_persistent_trace_write: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        for name in self.__dataclass_fields__:
            if name.startswith("no_"):
                _validate_true(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class V0375ReadinessReport:
    readiness_report_id: str
    version: str
    readiness_level: SandboxRepairSuggestionReadinessLevel | str
    status: SandboxRepairSuggestionStatus | str
    summary: str
    ready_for_v0376_vera_codex_one_shot_agent_trial: bool
    ready_for_v0377_cold_agent_performance_evaluation: bool
    ready_for_v0378_cli_test_runner_agent_evaluation_surface: bool
    ready_for_v038_bounded_repair_proposal_loop: bool
    ready_for_repair_suggestion_metadata: bool
    ready_for_repair_scope_metadata: bool
    ready_for_repair_risk_assessment: bool
    ready_for_repair_human_review_requirement: bool
    ready_for_do_nothing_repair_comparison: bool
    ready_for_future_repair_proposal_input: bool
    ready_for_future_vera_codex_trial_input: bool
    ready_for_future_cold_evaluation_input: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_automatic_repair: bool
    ready_for_repair_execution: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_vera_codex_trial_execution: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        for name in (
            "ready_for_execution",
            "ready_for_test_execution",
            "ready_for_controlled_test_subprocess",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_repair_patch_proposal",
            "ready_for_repair_diff_generation",
            "ready_for_code_hunk_generation",
            "ready_for_automatic_repair",
            "ready_for_repair_execution",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_vera_codex_trial_execution",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        ):
            _validate_false(name, getattr(self, name))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


def build_sandbox_repair_suggestion_flags(**kwargs: Any) -> SandboxRepairSuggestionFlagSet:
    return SandboxRepairSuggestionFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_repair_suggestion_flags:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        repair_suggestion_layer_constructed=kwargs.pop("repair_suggestion_layer_constructed", True),
        repair_suggestion_metadata_available=kwargs.pop("repair_suggestion_metadata_available", True),
        repair_scope_metadata_available=kwargs.pop("repair_scope_metadata_available", True),
        repair_risk_assessment_available=kwargs.pop("repair_risk_assessment_available", True),
        repair_human_review_requirement_available=kwargs.pop("repair_human_review_requirement_available", True),
        do_nothing_repair_comparison_available=kwargs.pop("do_nothing_repair_comparison_available", True),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_v0378_cli_test_runner_agent_evaluation_surface=kwargs.pop("ready_for_v0378_cli_test_runner_agent_evaluation_surface", True),
        ready_for_v038_bounded_repair_proposal_loop=kwargs.pop("ready_for_v038_bounded_repair_proposal_loop", True),
        ready_for_repair_suggestion_metadata=kwargs.pop("ready_for_repair_suggestion_metadata", True),
        ready_for_repair_scope_metadata=kwargs.pop("ready_for_repair_scope_metadata", True),
        ready_for_repair_risk_assessment=kwargs.pop("ready_for_repair_risk_assessment", True),
        ready_for_repair_human_review_requirement=kwargs.pop("ready_for_repair_human_review_requirement", True),
        ready_for_do_nothing_repair_comparison=kwargs.pop("ready_for_do_nothing_repair_comparison", True),
        ready_for_future_repair_proposal_input=kwargs.pop("ready_for_future_repair_proposal_input", True),
        ready_for_future_vera_codex_trial_input=kwargs.pop("ready_for_future_vera_codex_trial_input", True),
        ready_for_future_cold_evaluation_input=kwargs.pop("ready_for_future_cold_evaluation_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_FLAG_NAMES},
    )


def build_sandbox_repair_suggestion_source_ref(**kwargs: Any) -> SandboxRepairSuggestionSourceRef:
    return SandboxRepairSuggestionSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "sandbox_repair_suggestion_source:v0.37.5"),
        source_kind=kwargs.pop("source_kind", SandboxRepairSuggestionSourceKind.V0374_TEST_FEEDBACK_REPORT),
        source_id=kwargs.pop("source_id", "sandbox_test_feedback_report:v0.37.4"),
        source_summary=kwargs.pop("source_summary", "supplied feedback report metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.4 feedback report"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_policy(**kwargs: Any) -> SandboxRepairSuggestionPolicy:
    return SandboxRepairSuggestionPolicy(
        repair_policy_id=kwargs.pop("repair_policy_id", "sandbox_repair_suggestion_policy:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            SandboxRepairSuggestionMode.METADATA_ONLY_SUGGESTION,
            SandboxRepairSuggestionMode.EVIDENCE_BASED_REPAIR_HINT,
            SandboxRepairSuggestionMode.SCOPE_ONLY_REPAIR_HINT,
            SandboxRepairSuggestionMode.HUMAN_REVIEW_REPAIR_HINT,
            SandboxRepairSuggestionMode.DO_NOTHING_COMPARISON_HINT,
            SandboxRepairSuggestionMode.FUTURE_REPAIR_PROPOSAL_INPUT,
        ]),
        max_suggestions=kwargs.pop("max_suggestions", 10),
        max_evidence_refs=kwargs.pop("max_evidence_refs", 20),
        max_summary_chars=kwargs.pop("max_summary_chars", 1000),
        require_feedback_report=kwargs.pop("require_feedback_report", True),
        require_evidence_refs=kwargs.pop("require_evidence_refs", True),
        require_confidence_level=kwargs.pop("require_confidence_level", True),
        require_risk_assessment=kwargs.pop("require_risk_assessment", True),
        require_human_review_requirement=kwargs.pop("require_human_review_requirement", True),
        require_do_nothing_comparison=kwargs.pop("require_do_nothing_comparison", True),
        allow_repair_suggestion_metadata=kwargs.pop("allow_repair_suggestion_metadata", True),
        allow_scope_metadata=kwargs.pop("allow_scope_metadata", True),
        allow_risk_assessment=kwargs.pop("allow_risk_assessment", True),
        allow_human_review_requirement=kwargs.pop("allow_human_review_requirement", True),
        allow_future_repair_proposal_input=kwargs.pop("allow_future_repair_proposal_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_POLICY_ALLOW_NAMES},
    )


def build_sandbox_repair_suggestion_input(**kwargs: Any) -> SandboxRepairSuggestionInput:
    return SandboxRepairSuggestionInput(
        repair_input_id=kwargs.pop("repair_input_id", "sandbox_repair_suggestion_input:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        feedback_report_id=kwargs.pop("feedback_report_id", "sandbox_test_feedback_report:v0.37.4"),
        diagnosis_report_id=kwargs.pop("diagnosis_report_id", "sandbox_failure_diagnosis_report:v0.37.4"),
        result_envelope_id=kwargs.pop("result_envelope_id", None),
        requested_mode=kwargs.pop("requested_mode", SandboxRepairSuggestionMode.METADATA_ONLY_SUGGESTION),
        source_refs=kwargs.pop("source_refs", [build_sandbox_repair_suggestion_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["patch proposal", "diff generation", "code edit", "apply", "test execution", "subprocess", "shell", "install", "network", "repair execution", "external agent", "Dominion"]),
        task_summary=kwargs.pop("task_summary", "repair suggestion metadata request"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_evidence_ref(**kwargs: Any) -> SandboxRepairEvidenceRef:
    return SandboxRepairEvidenceRef(
        repair_evidence_id=kwargs.pop("repair_evidence_id", "sandbox_repair_evidence:v0.37.5"),
        evidence_kind=kwargs.pop("evidence_kind", SandboxRepairEvidenceKind.FEEDBACK_REPORT_REF),
        source_id=kwargs.pop("source_id", "sandbox_test_feedback_report:v0.37.4"),
        evidence_summary=kwargs.pop("evidence_summary", "repair evidence metadata"),
        evidence_strength=kwargs.pop("evidence_strength", "moderate"),
        confidence=kwargs.pop("confidence", SandboxRepairConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_scope(**kwargs: Any) -> SandboxRepairScope:
    return SandboxRepairScope(
        repair_scope_id=kwargs.pop("repair_scope_id", "sandbox_repair_scope:v0.37.5"),
        scope_kind=kwargs.pop("scope_kind", SandboxRepairScopeKind.UNKNOWN_SCOPE),
        scope_summary=kwargs.pop("scope_summary", "repair scope metadata only"),
        candidate_paths=kwargs.pop("candidate_paths", []),
        candidate_symbols=kwargs.pop("candidate_symbols", []),
        scope_confidence=kwargs.pop("scope_confidence", SandboxRepairConfidenceLevel.INCONCLUSIVE),
        edit_allowed=kwargs.pop("edit_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_risk_assessment(**kwargs: Any) -> SandboxRepairRiskAssessment:
    return SandboxRepairRiskAssessment(
        risk_assessment_id=kwargs.pop("risk_assessment_id", "sandbox_repair_risk:v0.37.5"),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxRepairSuggestionRiskKind.REPAIR_PATCH_CONFUSION_RISK]),
        severity=kwargs.pop("severity", "medium"),
        risk_summary=kwargs.pop("risk_summary", "repair suggestion risk metadata"),
        requires_human_review=kwargs.pop("requires_human_review", True),
        blocks_future_repair_proposal=kwargs.pop("blocks_future_repair_proposal", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_do_nothing_comparison(**kwargs: Any) -> SandboxRepairDoNothingComparison:
    return SandboxRepairDoNothingComparison(
        do_nothing_comparison_id=kwargs.pop("do_nothing_comparison_id", "sandbox_repair_do_nothing:v0.37.5"),
        comparison_kind=kwargs.pop("comparison_kind", SandboxRepairDoNothingComparisonKind.DO_NOTHING_COMPETITIVE),
        comparison_summary=kwargs.pop("comparison_summary", "do-nothing repair comparison metadata"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        repair_suggestion_outperforms_do_nothing=kwargs.pop("repair_suggestion_outperforms_do_nothing", False),
        scoring_performed=kwargs.pop("scoring_performed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_human_review_requirement(**kwargs: Any) -> SandboxRepairHumanReviewRequirement:
    return SandboxRepairHumanReviewRequirement(
        review_requirement_id=kwargs.pop("review_requirement_id", "sandbox_repair_review:v0.37.5"),
        requirement_kind=kwargs.pop("requirement_kind", SandboxRepairReviewRequirementKind.HUMAN_REVIEW_REQUIRED_BEFORE_FUTURE_REPAIR_PROPOSAL),
        requirement_summary=kwargs.pop("requirement_summary", "human review required; not approval"),
        required_before_future_repair_proposal=kwargs.pop("required_before_future_repair_proposal", True),
        required_before_any_apply=kwargs.pop("required_before_any_apply", True),
        human_approval_present=kwargs.pop("human_approval_present", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggested_action(**kwargs: Any) -> SandboxRepairSuggestedAction:
    return SandboxRepairSuggestedAction(
        repair_action_id=kwargs.pop("repair_action_id", "sandbox_repair_action:v0.37.5"),
        action_kind=kwargs.pop("action_kind", SandboxRepairActionKind.REQUEST_HUMAN_REVIEW),
        action_summary=kwargs.pop("action_summary", "repair suggested action metadata only"),
        rationale=kwargs.pop("rationale", "no repair executes in v0.37.5"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        future_gated=kwargs.pop("future_gated", True),
        executes_now=kwargs.pop("executes_now", False),
        generates_patch=kwargs.pop("generates_patch", False),
        edits_code=kwargs.pop("edits_code", False),
        applies_patch=kwargs.pop("applies_patch", False),
        runs_tests=kwargs.pop("runs_tests", False),
        installs_dependency=kwargs.pop("installs_dependency", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_envelope(**kwargs: Any) -> SandboxRepairSuggestionEnvelope:
    evidence_refs = kwargs.pop("evidence_refs", [build_sandbox_repair_evidence_ref()])
    return SandboxRepairSuggestionEnvelope(
        repair_suggestion_id=kwargs.pop("repair_suggestion_id", "sandbox_repair_suggestion:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        repair_input_id=kwargs.pop("repair_input_id", "sandbox_repair_suggestion_input:v0.37.5"),
        status=kwargs.pop("status", SandboxRepairSuggestionStatus.SUGGESTION_CREATED),
        readiness_level=kwargs.pop("readiness_level", SandboxRepairSuggestionReadinessLevel.FUTURE_REPAIR_PROPOSAL_INPUT_READY),
        suggestion_kind=kwargs.pop("suggestion_kind", SandboxRepairSuggestionKind.HUMAN_REVIEW_REQUIRED),
        scope=kwargs.pop("scope", build_sandbox_repair_scope()),
        evidence_refs=evidence_refs,
        risk_assessment=kwargs.pop("risk_assessment", build_sandbox_repair_risk_assessment()),
        do_nothing_comparison=kwargs.pop("do_nothing_comparison", build_sandbox_repair_do_nothing_comparison(evidence_refs=[e.repair_evidence_id for e in evidence_refs])),
        human_review_requirement=kwargs.pop("human_review_requirement", build_sandbox_repair_human_review_requirement()),
        suggested_actions=kwargs.pop("suggested_actions", [build_sandbox_repair_suggested_action(evidence_refs=evidence_refs)]),
        source_refs=kwargs.pop("source_refs", [build_sandbox_repair_suggestion_source_ref()]),
        suggestion_summary=kwargs.pop("suggestion_summary", "repair suggestion metadata only; no patch proposal"),
        urgency=kwargs.pop("urgency", SandboxRepairUrgency.MEDIUM),
        confidence=kwargs.pop("confidence", SandboxRepairConfidenceLevel.MEDIUM),
        eligible_for_future_repair_proposal=kwargs.pop("eligible_for_future_repair_proposal", True),
        eligible_for_future_vera_codex_trial=kwargs.pop("eligible_for_future_vera_codex_trial", True),
        eligible_for_future_cold_evaluation=kwargs.pop("eligible_for_future_cold_evaluation", True),
        repair_patch_proposal_created=kwargs.pop("repair_patch_proposal_created", False),
        repair_diff_generated=kwargs.pop("repair_diff_generated", False),
        code_hunk_generated=kwargs.pop("code_hunk_generated", False),
        repair_executed=kwargs.pop("repair_executed", False),
        tests_rerun=kwargs.pop("tests_rerun", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        production_certified=kwargs.pop("production_certified", False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_decision(**kwargs: Any) -> SandboxRepairSuggestionDecision:
    return SandboxRepairSuggestionDecision(
        decision_id=kwargs.pop("decision_id", "sandbox_repair_suggestion_decision:v0.37.5"),
        repair_input_id=kwargs.pop("repair_input_id", "sandbox_repair_suggestion_input:v0.37.5"),
        decision_kind=kwargs.pop("decision_kind", SandboxRepairSuggestionDecisionKind.ALLOW_REPAIR_SUGGESTION_METADATA),
        status=kwargs.pop("status", SandboxRepairSuggestionStatus.SUGGESTION_CREATED),
        risk_kinds=kwargs.pop("risk_kinds", [SandboxRepairSuggestionRiskKind.REPAIR_PATCH_CONFUSION_RISK]),
        decision_summary=kwargs.pop("decision_summary", "repair suggestion metadata allowed; repair execution blocked"),
        repair_suggestion_metadata_allowed=kwargs.pop("repair_suggestion_metadata_allowed", True),
        repair_scope_metadata_allowed=kwargs.pop("repair_scope_metadata_allowed", True),
        repair_risk_assessment_allowed=kwargs.pop("repair_risk_assessment_allowed", True),
        human_review_requirement_allowed=kwargs.pop("human_review_requirement_allowed", True),
        do_nothing_comparison_allowed=kwargs.pop("do_nothing_comparison_allowed", True),
        future_repair_proposal_input_allowed=kwargs.pop("future_repair_proposal_input_allowed", True),
        future_vera_codex_trial_input_allowed=kwargs.pop("future_vera_codex_trial_input_allowed", True),
        patch_proposal_allowed=kwargs.pop("patch_proposal_allowed", False),
        diff_generation_allowed=kwargs.pop("diff_generation_allowed", False),
        code_hunk_generation_allowed=kwargs.pop("code_hunk_generation_allowed", False),
        file_edit_allowed=kwargs.pop("file_edit_allowed", False),
        patch_apply_allowed=kwargs.pop("patch_apply_allowed", False),
        test_execution_allowed=kwargs.pop("test_execution_allowed", False),
        subprocess_allowed=kwargs.pop("subprocess_allowed", False),
        shell_allowed=kwargs.pop("shell_allowed", False),
        dependency_install_allowed=kwargs.pop("dependency_install_allowed", False),
        network_allowed=kwargs.pop("network_allowed", False),
        repair_execution_allowed=kwargs.pop("repair_execution_allowed", False),
        vera_codex_trial_execution_allowed=kwargs.pop("vera_codex_trial_execution_allowed", False),
        external_agent_allowed=kwargs.pop("external_agent_allowed", False),
        dominion_runtime_allowed=kwargs.pop("dominion_runtime_allowed", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.5 repair suggestion decision"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_validation_finding(**kwargs: Any) -> SandboxRepairSuggestionValidationFinding:
    return SandboxRepairSuggestionValidationFinding(
        finding_id=kwargs.pop("finding_id", "sandbox_repair_validation_finding:v0.37.5"),
        risk_kind=kwargs.pop("risk_kind", SandboxRepairSuggestionRiskKind.UNKNOWN),
        severity=kwargs.pop("severity", "info"),
        message=kwargs.pop("message", "repair suggestion validation finding"),
        blocks_suggestion=kwargs.pop("blocks_suggestion", False),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_validation_report(**kwargs: Any) -> SandboxRepairSuggestionValidationReport:
    return SandboxRepairSuggestionValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "sandbox_repair_validation_report:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        repair_suggestion_id=kwargs.pop("repair_suggestion_id", "sandbox_repair_suggestion:v0.37.5"),
        findings=kwargs.pop("findings", []),
        evidence_refs_confirmed=kwargs.pop("evidence_refs_confirmed", True),
        confidence_confirmed=kwargs.pop("confidence_confirmed", True),
        do_nothing_comparison_confirmed=kwargs.pop("do_nothing_comparison_confirmed", True),
        human_review_requirement_confirmed=kwargs.pop("human_review_requirement_confirmed", True),
        no_patch_diff_hunk_confirmed=kwargs.pop("no_patch_diff_hunk_confirmed", True),
        no_repair_execution_confirmed=kwargs.pop("no_repair_execution_confirmed", True),
        summary=kwargs.pop("summary", "repair suggestion validation confirms no patch/diff/hunk or repair execution"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.5 validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_report(**kwargs: Any) -> SandboxRepairSuggestionReport:
    envelope = kwargs.pop("repair_suggestion", build_sandbox_repair_suggestion_envelope())
    return SandboxRepairSuggestionReport(
        report_id=kwargs.pop("report_id", "sandbox_repair_suggestion_report:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        repair_suggestion=envelope,
        validation_report=kwargs.pop("validation_report", build_sandbox_repair_suggestion_validation_report(repair_suggestion_id=envelope.repair_suggestion_id)),
        report_summary=kwargs.pop("report_summary", "repair suggestion report metadata only"),
        production_certified=kwargs.pop("production_certified", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_run_preview(**kwargs: Any) -> SandboxRepairSuggestionRunPreview:
    return SandboxRepairSuggestionRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "sandbox_repair_run_preview:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        repair_input_id=kwargs.pop("repair_input_id", "sandbox_repair_suggestion_input:v0.37.5"),
        preview_summary=kwargs.pop("preview_summary", "repair suggestion preview only"),
        ready_for_repair_suggestion_metadata=kwargs.pop("ready_for_repair_suggestion_metadata", True),
        ready_for_repair_patch_proposal=kwargs.pop("ready_for_repair_patch_proposal", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_repair_execution=kwargs.pop("ready_for_repair_execution", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.5 preview"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_repair_suggestion_no_auto_repair_guarantee(**kwargs: Any) -> SandboxRepairSuggestionNoAutoRepairGuarantee:
    no_names = tuple(name for name in SandboxRepairSuggestionNoAutoRepairGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return SandboxRepairSuggestionNoAutoRepairGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "sandbox_repair_no_auto_repair_guarantee:v0.37.5"),
        version=kwargs.pop("version", V0375_VERSION),
        summary=kwargs.pop("summary", "v0.37.5 emits repair suggestion metadata only and performs no repair"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v0375_readiness_report(**kwargs: Any) -> V0375ReadinessReport:
    return V0375ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0375_readiness_report"),
        version=kwargs.pop("version", V0375_VERSION),
        readiness_level=kwargs.pop("readiness_level", SandboxRepairSuggestionReadinessLevel.FUTURE_REPAIR_PROPOSAL_INPUT_READY),
        status=kwargs.pop("status", SandboxRepairSuggestionStatus.SUGGESTION_CREATED),
        summary=kwargs.pop("summary", "v0.37.5 repair suggestion metadata ready; repair execution remains false"),
        ready_for_v0376_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_v0376_vera_codex_one_shot_agent_trial", True),
        ready_for_v0377_cold_agent_performance_evaluation=kwargs.pop("ready_for_v0377_cold_agent_performance_evaluation", True),
        ready_for_v0378_cli_test_runner_agent_evaluation_surface=kwargs.pop("ready_for_v0378_cli_test_runner_agent_evaluation_surface", True),
        ready_for_v038_bounded_repair_proposal_loop=kwargs.pop("ready_for_v038_bounded_repair_proposal_loop", True),
        ready_for_repair_suggestion_metadata=kwargs.pop("ready_for_repair_suggestion_metadata", True),
        ready_for_repair_scope_metadata=kwargs.pop("ready_for_repair_scope_metadata", True),
        ready_for_repair_risk_assessment=kwargs.pop("ready_for_repair_risk_assessment", True),
        ready_for_repair_human_review_requirement=kwargs.pop("ready_for_repair_human_review_requirement", True),
        ready_for_do_nothing_repair_comparison=kwargs.pop("ready_for_do_nothing_repair_comparison", True),
        ready_for_future_repair_proposal_input=kwargs.pop("ready_for_future_repair_proposal_input", True),
        ready_for_future_vera_codex_trial_input=kwargs.pop("ready_for_future_vera_codex_trial_input", True),
        ready_for_future_cold_evaluation_input=kwargs.pop("ready_for_future_cold_evaluation_input", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_controlled_test_subprocess=kwargs.pop("ready_for_controlled_test_subprocess", False),
        ready_for_shell_execution=kwargs.pop("ready_for_shell_execution", False),
        ready_for_subprocess_execution=kwargs.pop("ready_for_subprocess_execution", False),
        ready_for_command_execution=kwargs.pop("ready_for_command_execution", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        ready_for_repair_patch_proposal=kwargs.pop("ready_for_repair_patch_proposal", False),
        ready_for_repair_diff_generation=kwargs.pop("ready_for_repair_diff_generation", False),
        ready_for_code_hunk_generation=kwargs.pop("ready_for_code_hunk_generation", False),
        ready_for_automatic_repair=kwargs.pop("ready_for_automatic_repair", False),
        ready_for_repair_execution=kwargs.pop("ready_for_repair_execution", False),
        ready_for_multi_cycle_agentic_loop=kwargs.pop("ready_for_multi_cycle_agentic_loop", False),
        ready_for_vera_codex_trial_execution=kwargs.pop("ready_for_vera_codex_trial_execution", False),
        ready_for_cold_agent_performance_evaluation=kwargs.pop("ready_for_cold_agent_performance_evaluation", False),
        ready_for_external_agent_execution=kwargs.pop("ready_for_external_agent_execution", False),
        ready_for_dominion_runtime=kwargs.pop("ready_for_dominion_runtime", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.5 repair suggestion"]),
        metadata=kwargs.pop("metadata", {}),
    )


def default_sandbox_repair_suggestion_policy(**kwargs: Any) -> SandboxRepairSuggestionPolicy:
    return build_sandbox_repair_suggestion_policy(**kwargs)


def build_repair_suggestion_input_from_feedback_report(
    feedback_report: SandboxTestFeedbackReport,
    **kwargs: Any,
) -> SandboxRepairSuggestionInput:
    return build_sandbox_repair_suggestion_input(
        feedback_report_id=feedback_report.feedback_report_id,
        diagnosis_report_id=feedback_report.diagnosis_report.diagnosis_report_id,
        source_refs=[build_sandbox_repair_suggestion_source_ref(
            source_id=feedback_report.feedback_report_id,
            evidence_refs=[feedback_report.feedback_report_id, feedback_report.diagnosis_report.diagnosis_report_id],
        )],
        **kwargs,
    )


def derive_repair_evidence_refs_from_feedback(
    feedback_report: SandboxTestFeedbackReport,
    policy: SandboxRepairSuggestionPolicy | None = None,
) -> list[SandboxRepairEvidenceRef]:
    policy = policy or default_sandbox_repair_suggestion_policy()
    refs = [
        build_sandbox_repair_evidence_ref(
            repair_evidence_id="sandbox_repair_evidence:feedback:v0.37.5",
            evidence_kind=SandboxRepairEvidenceKind.FEEDBACK_REPORT_REF,
            source_id=feedback_report.feedback_report_id,
            evidence_summary="feedback report metadata",
        ),
        build_sandbox_repair_evidence_ref(
            repair_evidence_id="sandbox_repair_evidence:diagnosis:v0.37.5",
            evidence_kind=SandboxRepairEvidenceKind.DIAGNOSIS_REPORT_REF,
            source_id=feedback_report.diagnosis_report.diagnosis_report_id,
            evidence_summary="diagnosis report metadata",
        ),
        build_sandbox_repair_evidence_ref(
            repair_evidence_id="sandbox_repair_evidence:do_nothing:v0.37.5",
            evidence_kind=SandboxRepairEvidenceKind.DO_NOTHING_SIGNAL_REF,
            source_id=feedback_report.do_nothing_signal.do_nothing_signal_id,
            evidence_summary="do-nothing signal metadata",
        ),
    ]
    for index, hypothesis in enumerate(feedback_report.diagnosis_report.hypotheses[: policy.max_evidence_refs]):
        refs.append(build_sandbox_repair_evidence_ref(
            repair_evidence_id=f"sandbox_repair_evidence:hypothesis:{index}:v0.37.5",
            evidence_kind=SandboxRepairEvidenceKind.ROOT_CAUSE_HYPOTHESIS_REF,
            source_id=hypothesis.hypothesis_id,
            evidence_summary=_limit_text(hypothesis.hypothesis_summary, policy.max_summary_chars),
            evidence_strength=_enum_value(hypothesis.evidence_strength),
            confidence=_confidence_from_feedback(hypothesis.confidence),
        ))
    return refs[: policy.max_evidence_refs]


def _confidence_from_feedback(confidence: Any) -> SandboxRepairConfidenceLevel:
    value = _enum_value(confidence)
    mapping = {
        SandboxFeedbackConfidenceLevel.HIGH.value: SandboxRepairConfidenceLevel.HIGH,
        SandboxFeedbackConfidenceLevel.MEDIUM.value: SandboxRepairConfidenceLevel.MEDIUM,
        SandboxFeedbackConfidenceLevel.LOW.value: SandboxRepairConfidenceLevel.LOW,
        SandboxFeedbackConfidenceLevel.INCONCLUSIVE.value: SandboxRepairConfidenceLevel.INCONCLUSIVE,
    }
    return mapping.get(value, SandboxRepairConfidenceLevel.UNKNOWN)


def derive_repair_scope_from_feedback(feedback_report: SandboxTestFeedbackReport) -> SandboxRepairScope:
    hypotheses = feedback_report.diagnosis_report.hypotheses
    kinds = {_enum_value(h.hypothesis_kind) for h in hypotheses}
    if SandboxRootCauseHypothesisKind.IMPLEMENTATION_BUG_LIKELY.value in kinds:
        scope_kind = SandboxRepairScopeKind.IMPLEMENTATION_SCOPE
    elif SandboxRootCauseHypothesisKind.IMPORT_PATH_ISSUE_LIKELY.value in kinds:
        scope_kind = SandboxRepairScopeKind.IMPORT_PATH_SCOPE
    elif SandboxRootCauseHypothesisKind.MISSING_DEPENDENCY_LIKELY.value in kinds:
        scope_kind = SandboxRepairScopeKind.CONFIGURATION_SCOPE
    elif SandboxRootCauseHypothesisKind.COMMAND_POLICY_BLOCK_LIKELY.value in kinds:
        scope_kind = SandboxRepairScopeKind.ALLOWLIST_POLICY_SCOPE
    elif SandboxRootCauseHypothesisKind.TIMEOUT_OR_PERFORMANCE_ISSUE_LIKELY.value in kinds:
        scope_kind = SandboxRepairScopeKind.SANDBOX_ENVIRONMENT_SCOPE
    elif SandboxRootCauseHypothesisKind.NO_ROOT_CAUSE_IDENTIFIED.value in kinds:
        scope_kind = SandboxRepairScopeKind.NO_SCOPE
    else:
        scope_kind = SandboxRepairScopeKind.UNKNOWN_SCOPE
    return build_sandbox_repair_scope(
        scope_kind=scope_kind,
        scope_summary=f"{scope_kind.value}; metadata only, edit permission not granted",
        scope_confidence=SandboxRepairConfidenceLevel.MEDIUM if scope_kind != SandboxRepairScopeKind.UNKNOWN_SCOPE else SandboxRepairConfidenceLevel.INCONCLUSIVE,
    )


def assess_repair_suggestion_risk(feedback_report: SandboxTestFeedbackReport) -> SandboxRepairRiskAssessment:
    risk_kinds: list[SandboxRepairSuggestionRiskKind] = [
        SandboxRepairSuggestionRiskKind.REPAIR_PATCH_CONFUSION_RISK,
        SandboxRepairSuggestionRiskKind.REPAIR_EXECUTION_CONFUSION_RISK,
    ]
    severity = "medium"
    blocks = False
    if feedback_report.diagnosis_report.inconclusive:
        risk_kinds.append(SandboxRepairSuggestionRiskKind.INSUFFICIENT_EVIDENCE_RISK)
        severity = "high"
        blocks = True
    action_values = {_enum_value(action.action_kind) for action in feedback_report.suggested_actions}
    if SandboxSuggestedNextActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL.value in action_values:
        risk_kinds.append(SandboxRepairSuggestionRiskKind.DEPENDENCY_INSTALL_CONFUSION_RISK)
    if SandboxSuggestedNextActionKind.RERUN_TEST_FUTURE_GATE.value in action_values:
        risk_kinds.append(SandboxRepairSuggestionRiskKind.TIMEOUT_RETRY_CONFUSION_RISK)
    if not feedback_report.do_nothing_signal.do_nothing_remains_valid:
        risk_kinds.append(SandboxRepairSuggestionRiskKind.DO_NOTHING_OMISSION_RISK)
    return build_sandbox_repair_risk_assessment(
        risk_kinds=risk_kinds,
        severity=severity,
        risk_summary="repair suggestion risk assessment; human review required",
        requires_human_review=True,
        blocks_future_repair_proposal=blocks,
    )


def compare_repair_suggestion_to_do_nothing(
    feedback_report: SandboxTestFeedbackReport,
    risk_assessment: SandboxRepairRiskAssessment,
    evidence_refs: list[SandboxRepairEvidenceRef],
) -> SandboxRepairDoNothingComparison:
    evidence_ids = [e.repair_evidence_id for e in evidence_refs]
    if risk_assessment.blocks_future_repair_proposal:
        return build_sandbox_repair_do_nothing_comparison(
            comparison_kind=SandboxRepairDoNothingComparisonKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_EVIDENCE,
            comparison_summary="do nothing required because evidence is insufficient or repair risk is high",
            evidence_refs=evidence_ids,
            repair_suggestion_outperforms_do_nothing=False,
        )
    if feedback_report.diagnosis_report.inconclusive:
        return build_sandbox_repair_do_nothing_comparison(
            comparison_kind=SandboxRepairDoNothingComparisonKind.DO_NOTHING_PREFERRED,
            comparison_summary="do nothing preferred while diagnosis remains inconclusive",
            evidence_refs=evidence_ids,
            repair_suggestion_outperforms_do_nothing=False,
        )
    return build_sandbox_repair_do_nothing_comparison(
        comparison_kind=SandboxRepairDoNothingComparisonKind.DO_NOTHING_COMPETITIVE,
        comparison_summary="do nothing remains valid comparator; future-gated metadata may be useful",
        evidence_refs=evidence_ids,
        repair_suggestion_outperforms_do_nothing=False,
    )


def derive_human_review_requirement_for_repair(
    risk_assessment: SandboxRepairRiskAssessment,
    confidence: SandboxRepairConfidenceLevel | str,
) -> SandboxRepairHumanReviewRequirement:
    if risk_assessment.blocks_future_repair_proposal or risk_assessment.severity in ("high", "critical", "blocked"):
        kind = SandboxRepairReviewRequirementKind.HUMAN_REVIEW_REQUIRED_DUE_TO_RISK
    elif _enum_value(confidence) in (SandboxRepairConfidenceLevel.LOW.value, SandboxRepairConfidenceLevel.INCONCLUSIVE.value, SandboxRepairConfidenceLevel.UNKNOWN.value):
        kind = SandboxRepairReviewRequirementKind.HUMAN_REVIEW_REQUIRED_DUE_TO_LOW_CONFIDENCE
    else:
        kind = SandboxRepairReviewRequirementKind.HUMAN_REVIEW_REQUIRED_BEFORE_FUTURE_REPAIR_PROPOSAL
    return build_sandbox_repair_human_review_requirement(
        requirement_kind=kind,
        requirement_summary=f"{kind.value}; requirement is not approval",
    )


def _suggestion_kind_from_feedback(feedback_report: SandboxTestFeedbackReport, risk: SandboxRepairRiskAssessment) -> SandboxRepairSuggestionKind:
    if risk.blocks_future_repair_proposal:
        return SandboxRepairSuggestionKind.BLOCK_DUE_TO_INSUFFICIENT_EVIDENCE
    action_values = {_enum_value(action.action_kind) for action in feedback_report.suggested_actions}
    if SandboxSuggestedNextActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL.value in action_values:
        return SandboxRepairSuggestionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL
    if SandboxSuggestedNextActionKind.RERUN_TEST_FUTURE_GATE.value in action_values:
        return SandboxRepairSuggestionKind.INSPECT_TIMEOUT_OR_PERFORMANCE_FUTURE_GATE
    if SandboxSuggestedNextActionKind.CREATE_REPAIR_SUGGESTION_FUTURE_GATE.value in action_values:
        return SandboxRepairSuggestionKind.REVISE_IMPLEMENTATION_FUTURE_GATE
    if SandboxSuggestedNextActionKind.DO_NOTHING.value in action_values:
        return SandboxRepairSuggestionKind.DO_NOTHING_PREFERRED
    return SandboxRepairSuggestionKind.HUMAN_REVIEW_REQUIRED


def generate_sandbox_repair_suggested_actions(
    suggestion_kind: SandboxRepairSuggestionKind | str,
    evidence_refs: list[SandboxRepairEvidenceRef],
    risk_assessment: SandboxRepairRiskAssessment,
) -> list[SandboxRepairSuggestedAction]:
    kind = _enum_value(suggestion_kind)
    evidence = evidence_refs
    actions = [build_sandbox_repair_suggested_action(
        repair_action_id="sandbox_repair_action:human_review:v0.37.5",
        action_kind=SandboxRepairActionKind.REQUEST_HUMAN_REVIEW,
        action_summary="request human review before any future repair proposal",
        rationale="human review requirement is not approval",
        evidence_refs=evidence,
    )]
    if risk_assessment.blocks_future_repair_proposal or kind == SandboxRepairSuggestionKind.BLOCK_DUE_TO_INSUFFICIENT_EVIDENCE.value:
        actions.insert(0, build_sandbox_repair_suggested_action(
            repair_action_id="sandbox_repair_action:do_nothing:v0.37.5",
            action_kind=SandboxRepairActionKind.DO_NOTHING,
            action_summary="do nothing remains preferred because evidence is insufficient or risk is high",
            rationale="weak evidence must not generate repair proposal input",
            evidence_refs=evidence,
            future_gated=False,
        ))
    elif kind == SandboxRepairSuggestionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL.value:
        actions.append(build_sandbox_repair_suggested_action(
            repair_action_id="sandbox_repair_action:missing_dependency:v0.37.5",
            action_kind=SandboxRepairActionKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL,
            action_summary="inspect missing dependency metadata without installing dependencies",
            rationale="missing dependency does not grant install permission",
            evidence_refs=evidence,
        ))
    elif kind == SandboxRepairSuggestionKind.INSPECT_TIMEOUT_OR_PERFORMANCE_FUTURE_GATE.value:
        actions.append(build_sandbox_repair_suggested_action(
            repair_action_id="sandbox_repair_action:timeout:v0.37.5",
            action_kind=SandboxRepairActionKind.INSPECT_TIMEOUT_WITHOUT_RETRY,
            action_summary="inspect timeout metadata without retrying tests",
            rationale="timeout does not grant retry permission",
            evidence_refs=evidence,
        ))
    else:
        actions.append(build_sandbox_repair_suggested_action(
            repair_action_id="sandbox_repair_action:future_input:v0.37.5",
            action_kind=SandboxRepairActionKind.PREPARE_FUTURE_REPAIR_PROPOSAL_INPUT,
            action_summary="prepare future repair proposal input metadata only",
            rationale="future proposal generation belongs to a later gated track",
            evidence_refs=evidence,
        ))
    return actions


def create_sandbox_repair_suggestion_envelope_from_feedback(
    feedback_report: SandboxTestFeedbackReport,
    policy: SandboxRepairSuggestionPolicy | None = None,
) -> SandboxRepairSuggestionEnvelope:
    policy = policy or default_sandbox_repair_suggestion_policy()
    repair_input = build_repair_suggestion_input_from_feedback_report(feedback_report)
    evidence = derive_repair_evidence_refs_from_feedback(feedback_report, policy)
    scope = derive_repair_scope_from_feedback(feedback_report)
    risk = assess_repair_suggestion_risk(feedback_report)
    comparison = compare_repair_suggestion_to_do_nothing(feedback_report, risk, evidence)
    confidence = SandboxRepairConfidenceLevel.INCONCLUSIVE if risk.blocks_future_repair_proposal else SandboxRepairConfidenceLevel.MEDIUM
    review = derive_human_review_requirement_for_repair(risk, confidence)
    suggestion_kind = _suggestion_kind_from_feedback(feedback_report, risk)
    actions = generate_sandbox_repair_suggested_actions(suggestion_kind, evidence, risk)
    eligible_for_future_repair = not risk.blocks_future_repair_proposal
    return build_sandbox_repair_suggestion_envelope(
        repair_input_id=repair_input.repair_input_id,
        suggestion_kind=suggestion_kind,
        scope=scope,
        evidence_refs=evidence,
        risk_assessment=risk,
        do_nothing_comparison=comparison,
        human_review_requirement=review,
        suggested_actions=actions,
        source_refs=repair_input.source_refs,
        suggestion_summary="repair suggestion metadata created from supplied v0.37.4 feedback only",
        urgency=SandboxRepairUrgency.BLOCKED if risk.blocks_future_repair_proposal else SandboxRepairUrgency.MEDIUM,
        confidence=confidence,
        eligible_for_future_repair_proposal=eligible_for_future_repair,
    )


def validate_sandbox_repair_suggestion_envelope(envelope: SandboxRepairSuggestionEnvelope) -> SandboxRepairSuggestionValidationReport:
    findings: list[SandboxRepairSuggestionValidationFinding] = []
    if envelope.repair_patch_proposal_created or envelope.repair_diff_generated or envelope.code_hunk_generated:
        findings.append(build_sandbox_repair_suggestion_validation_finding(
            risk_kind=SandboxRepairSuggestionRiskKind.REPAIR_PATCH_CONFUSION_RISK,
            severity="blocked",
            message="patch/diff/hunk generation is not allowed",
            blocks_suggestion=True,
        ))
    if envelope.repair_executed or envelope.ready_for_execution:
        findings.append(build_sandbox_repair_suggestion_validation_finding(
            risk_kind=SandboxRepairSuggestionRiskKind.REPAIR_EXECUTION_CONFUSION_RISK,
            severity="blocked",
            message="repair execution is not allowed",
            blocks_suggestion=True,
        ))
    return build_sandbox_repair_suggestion_validation_report(
        repair_suggestion_id=envelope.repair_suggestion_id,
        findings=findings,
        summary="repair suggestion validation report",
    )


def sandbox_repair_suggestion_flags_preserve_no_repair(flags: SandboxRepairSuggestionFlagSet) -> bool:
    return isinstance(flags, SandboxRepairSuggestionFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_REPAIR_FLAG_NAMES)


def sandbox_repair_suggestion_policy_blocks_repair_execution(policy: SandboxRepairSuggestionPolicy) -> bool:
    return isinstance(policy, SandboxRepairSuggestionPolicy) and all(getattr(policy, name) is False for name in UNSAFE_REPAIR_POLICY_ALLOW_NAMES)


def sandbox_repair_scope_is_not_edit_permission(scope: SandboxRepairScope) -> bool:
    return isinstance(scope, SandboxRepairScope) and scope.edit_allowed is False


def sandbox_repair_action_is_not_execution(action: SandboxRepairSuggestedAction) -> bool:
    return isinstance(action, SandboxRepairSuggestedAction) and not action.executes_now and not action.generates_patch and not action.edits_code and not action.applies_patch and not action.runs_tests and not action.installs_dependency


def sandbox_repair_envelope_is_not_patch_proposal(envelope: SandboxRepairSuggestionEnvelope) -> bool:
    return (
        isinstance(envelope, SandboxRepairSuggestionEnvelope)
        and envelope.repair_patch_proposal_created is False
        and envelope.repair_diff_generated is False
        and envelope.code_hunk_generated is False
        and envelope.repair_executed is False
        and envelope.ready_for_execution is False
    )


def v0375_readiness_report_is_not_execution_ready(report: V0375ReadinessReport) -> bool:
    if not isinstance(report, V0375ReadinessReport):
        return False
    return all(
        getattr(report, name) is False
        for name in (
            "ready_for_execution",
            "ready_for_test_execution",
            "ready_for_controlled_test_subprocess",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
            "ready_for_repair_patch_proposal",
            "ready_for_repair_diff_generation",
            "ready_for_code_hunk_generation",
            "ready_for_automatic_repair",
            "ready_for_repair_execution",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_vera_codex_trial_execution",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_external_agent_execution",
            "ready_for_dominion_runtime",
            "production_certified",
        )
    )
