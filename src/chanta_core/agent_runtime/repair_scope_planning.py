from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0383_VERSION = "v0.38.3"
V0383_RELEASE_NAME = "v0.38.3 Repair Scope Planner & Change Intent Model"

SAFE_SCOPE_FLAG_NAMES = (
    "ready_for_v0384_proposed_diff_code_hunk_metadata",
    "ready_for_v0385_repair_proposal_safety_validation",
    "ready_for_repair_scope_planner",
    "ready_for_change_intent_model",
    "ready_for_affected_file_candidates",
    "ready_for_affected_symbol_candidates",
    "ready_for_scope_evidence_map",
    "ready_for_scope_risk_assessment",
    "ready_for_do_nothing_scope_comparison",
    "ready_for_future_proposed_diff_metadata_input",
    "ready_for_future_proposed_code_hunk_metadata_input",
)

UNSAFE_SCOPE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_source_file_read",
    "ready_for_sandbox_source_read",
    "ready_for_live_workspace_read",
    "ready_for_unbounded_source_read",
    "ready_for_reference_source_read",
    "ready_for_secret_read",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
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

UNSAFE_SCOPE_POLICY_ALLOW_NAMES = (
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_live_workspace_read",
    "allow_source_file_write",
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

UNSAFE_CANDIDATE_NAMES = (
    "edit_allowed",
    "proposal_generation_allowed",
    "diff_generation_allowed",
    "hunk_generation_allowed",
    "repair_execution_allowed",
)

UNSAFE_INTENT_NOW_NAMES = (
    "source_read_allowed_now",
    "edit_allowed_now",
    "proposal_generation_allowed_now",
    "diff_generation_allowed_now",
    "hunk_generation_allowed_now",
    "patch_envelope_generation_allowed_now",
    "repair_execution_allowed_now",
)

UNSAFE_PLAN_STATE_NAMES = (
    "source_read_performed_by_v0383",
    "proposal_generated",
    "diff_generated",
    "hunk_generated",
    "patch_envelope_generated",
    "file_edit_performed",
    "repair_executed",
    "production_certified",
    "ready_for_execution",
)

UNSAFE_SCOPE_DECISION_NOW_NAMES = (
    "source_read_allowed_now",
    "proposal_generation_allowed_now",
    "diff_generation_allowed_now",
    "hunk_generation_allowed_now",
    "patch_envelope_generation_allowed_now",
    "repair_execution_allowed_now",
)

REQUIRED_SCOPE_PROHIBITED_ACTIONS = (
    "source_read",
    "source_write",
    "proposal_generation",
    "diff_generation",
    "hunk_generation",
    "patch_envelope_generation",
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


class RepairScopePlanningMode(StrEnum):
    REPAIR_SCOPE_PLAN = "repair_scope_plan"
    CHANGE_INTENT_MODEL = "change_intent_model"
    AFFECTED_FILE_CANDIDATES = "affected_file_candidates"
    AFFECTED_SYMBOL_CANDIDATES = "affected_symbol_candidates"
    SCOPE_EVIDENCE_MAP = "scope_evidence_map"
    SCOPE_RISK_ASSESSMENT = "scope_risk_assessment"
    DO_NOTHING_SCOPE_COMPARISON = "do_nothing_scope_comparison"
    FUTURE_PATCH_METADATA_INPUT = "future_patch_metadata_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairScopePlanningSourceKind(StrEnum):
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0382_SOURCE_CONTEXT_ASSESSMENT = "v0382_source_context_assessment"
    V0382_SOURCE_EXCERPT = "v0382_source_excerpt"
    V0382_SYMBOL_CONTEXT_HINT = "v0382_symbol_context_hint"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0381_EVIDENCE_ASSESSMENT = "v0381_evidence_assessment"
    V0381_ELIGIBILITY_DECISION = "v0381_eligibility_decision"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    V0375_REPAIR_SUGGESTION_ENVELOPE = "v0375_repair_suggestion_envelope"
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0374_FAILURE_DIAGNOSIS_REPORT = "v0374_failure_diagnosis_report"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairScopePlanningStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    CANDIDATES_CREATED = "candidates_created"
    CHANGE_INTENT_CREATED = "change_intent_created"
    SCOPE_PLAN_CREATED = "scope_plan_created"
    SCOPE_PLAN_CREATED_WITH_WARNINGS = "scope_plan_created_with_warnings"
    READY_FOR_FUTURE_PATCH_METADATA = "ready_for_future_patch_metadata"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    INSUFFICIENT_SCOPE_CONTEXT = "insufficient_scope_context"
    NO_REPAIR_NEEDED = "no_repair_needed"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairScopePlanningReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SCOPE_PLANNING_CONTRACT_READY = "scope_planning_contract_ready"
    AFFECTED_FILE_CANDIDATE_READY = "affected_file_candidate_ready"
    AFFECTED_SYMBOL_CANDIDATE_READY = "affected_symbol_candidate_ready"
    SCOPE_EVIDENCE_MAP_READY = "scope_evidence_map_ready"
    CHANGE_INTENT_READY = "change_intent_ready"
    REPAIR_SCOPE_PLAN_READY = "repair_scope_plan_ready"
    DO_NOTHING_SCOPE_COMPARISON_READY = "do_nothing_scope_comparison_ready"
    FUTURE_PATCH_METADATA_INPUT_READY = "future_patch_metadata_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0384 = "design_handoff_ready_for_v0384"
    DESIGN_HANDOFF_READY_FOR_V0385 = "design_handoff_ready_for_v0385"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairScopePlanningDecisionKind(StrEnum):
    ALLOW_SCOPE_PLANNING = "allow_scope_planning"
    ALLOW_AFFECTED_FILE_CANDIDATES = "allow_affected_file_candidates"
    ALLOW_AFFECTED_SYMBOL_CANDIDATES = "allow_affected_symbol_candidates"
    ALLOW_SCOPE_EVIDENCE_MAP = "allow_scope_evidence_map"
    ALLOW_CHANGE_INTENT_MODEL = "allow_change_intent_model"
    ALLOW_SCOPE_RISK_ASSESSMENT = "allow_scope_risk_assessment"
    ALLOW_DO_NOTHING_SCOPE_COMPARISON = "allow_do_nothing_scope_comparison"
    ALLOW_FUTURE_PATCH_METADATA_INPUT = "allow_future_patch_metadata_input"
    CHOOSE_NO_REPAIR_NEEDED = "choose_no_repair_needed"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW = "choose_human_review"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairScopePlanningRiskKind(StrEnum):
    MISSING_SOURCE_CONTEXT_RISK = "missing_source_context_risk"
    INSUFFICIENT_SOURCE_CONTEXT_RISK = "insufficient_source_context_risk"
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    CONTRADICTORY_EVIDENCE_RISK = "contradictory_evidence_risk"
    WRONG_SCOPE_RISK = "wrong_scope_risk"
    OVERBROAD_SCOPE_RISK = "overbroad_scope_risk"
    UNDERBROAD_SCOPE_RISK = "underbroad_scope_risk"
    TEST_REWRITE_OVERREACH_RISK = "test_rewrite_overreach_risk"
    IMPLEMENTATION_CHANGE_OVERREACH_RISK = "implementation_change_overreach_risk"
    IMPORT_PATH_MISCLASSIFICATION_RISK = "import_path_misclassification_risk"
    DEPENDENCY_INSTALL_CONFUSION_RISK = "dependency_install_confusion_risk"
    TIMEOUT_RETRY_CONFUSION_RISK = "timeout_retry_confusion_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    HUMAN_REVIEW_OMISSION_RISK = "human_review_omission_risk"
    DIFF_GENERATION_CONFUSION_RISK = "diff_generation_confusion_risk"
    CODE_HUNK_GENERATION_CONFUSION_RISK = "code_hunk_generation_confusion_risk"
    EDIT_PERMISSION_CONFUSION_RISK = "edit_permission_confusion_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairScopeKind(StrEnum):
    NO_SCOPE = "no_scope"
    IMPLEMENTATION_SCOPE = "implementation_scope"
    TEST_SCOPE = "test_scope"
    IMPORT_PATH_SCOPE = "import_path_scope"
    CONFIGURATION_SCOPE = "configuration_scope"
    ALLOWLIST_POLICY_SCOPE = "allowlist_policy_scope"
    SANDBOX_ENVIRONMENT_SCOPE = "sandbox_environment_scope"
    DOCUMENTATION_SCOPE = "documentation_scope"
    DEPENDENCY_INSPECTION_SCOPE = "dependency_inspection_scope"
    PERFORMANCE_INVESTIGATION_SCOPE = "performance_investigation_scope"
    AMBIGUOUS_SCOPE = "ambiguous_scope"
    UNKNOWN_SCOPE = "unknown_scope"


class RepairChangeIntentKind(StrEnum):
    NO_CHANGE_NEEDED = "no_change_needed"
    ALIGN_IMPLEMENTATION_WITH_TEST = "align_implementation_with_test"
    REVIEW_TEST_EXPECTATION_FUTURE_GATE = "review_test_expectation_future_gate"
    ADJUST_IMPORT_PATH_FUTURE_GATE = "adjust_import_path_future_gate"
    INSPECT_CONFIGURATION_FUTURE_GATE = "inspect_configuration_future_gate"
    INSPECT_ALLOWLIST_POLICY_FUTURE_GATE = "inspect_allowlist_policy_future_gate"
    INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL = "inspect_missing_dependency_without_install"
    INSPECT_TIMEOUT_WITHOUT_RETRY = "inspect_timeout_without_retry"
    REDUCE_RUNTIME_ERROR_FUTURE_GATE = "reduce_runtime_error_future_gate"
    CLARIFY_DOCUMENTATION_FUTURE_GATE = "clarify_documentation_future_gate"
    HUMAN_REVIEW_ONLY = "human_review_only"
    DO_NOTHING = "do_nothing"
    UNKNOWN = "unknown"


class RepairAffectedArtifactKind(StrEnum):
    SOURCE_FILE = "source_file"
    TEST_FILE = "test_file"
    IMPORT_BLOCK = "import_block"
    FUNCTION_SYMBOL = "function_symbol"
    CLASS_SYMBOL = "class_symbol"
    CONFIG_FILE = "config_file"
    CONFIG_KEY = "config_key"
    ALLOWLIST_POLICY = "allowlist_policy"
    DOCUMENTATION_SECTION = "documentation_section"
    SANDBOX_ENVIRONMENT = "sandbox_environment"
    UNKNOWN = "unknown"


class RepairScopeDisposition(StrEnum):
    SELECTED_PRIMARY_SCOPE = "selected_primary_scope"
    CANDIDATE_SCOPE = "candidate_scope"
    REJECTED_SCOPE = "rejected_scope"
    BLOCKED_SCOPE = "blocked_scope"
    REVIEW_REQUIRED_SCOPE = "review_required_scope"
    DO_NOTHING_SCOPE = "do_nothing_scope"
    NO_SCOPE = "no_scope"
    UNKNOWN = "unknown"


class RepairScopeConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairScopeEvidenceKind(StrEnum):
    SOURCE_CONTEXT_SNAPSHOT_REF = "source_context_snapshot_ref"
    SOURCE_EXCERPT_REF = "source_excerpt_ref"
    SYMBOL_CONTEXT_HINT_REF = "symbol_context_hint_ref"
    EVIDENCE_BUNDLE_REF = "evidence_bundle_ref"
    COLD_SCORECARD_REF = "cold_scorecard_ref"
    REPAIR_SUGGESTION_REF = "repair_suggestion_ref"
    FEEDBACK_REPORT_REF = "feedback_report_ref"
    FAILURE_DIAGNOSIS_REF = "failure_diagnosis_ref"
    TEST_RESULT_REF = "test_result_ref"
    HUMAN_OPERATOR_NOTE = "human_operator_note"
    DO_NOTHING_REF = "do_nothing_ref"
    MISSING_EVIDENCE = "missing_evidence"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    UNKNOWN = "unknown"


class RepairScopeDoNothingComparisonKind(StrEnum):
    DO_NOTHING_PREFERRED_DUE_TO_NO_REPAIR_NEEDED = "do_nothing_preferred_due_to_no_repair_needed"
    DO_NOTHING_PREFERRED_DUE_TO_INSUFFICIENT_CONTEXT = "do_nothing_preferred_due_to_insufficient_context"
    DO_NOTHING_PREFERRED_DUE_TO_HIGH_SCOPE_RISK = "do_nothing_preferred_due_to_high_scope_risk"
    DO_NOTHING_COMPETITIVE_DUE_TO_LOW_CONFIDENCE = "do_nothing_competitive_due_to_low_confidence"
    SCOPE_PLAN_BETTER_THAN_DO_NOTHING = "scope_plan_better_than_do_nothing"
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
    if V0383_VERSION not in version:
        raise ValueError("version must include v0.38.3")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.3")


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


def _attr(value: Any, name: str, default: Any = None) -> Any:
    if value is None:
        return default
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _text_from_inputs(*items: Any) -> str:
    parts: list[str] = []
    for item in items:
        if item is None:
            continue
        for name in (
            "task_summary",
            "snapshot_summary",
            "assessment_summary",
            "evidence_summary",
            "decision_summary",
            "rationale_summary",
            "excerpt_summary",
            "hint_summary",
            "metadata",
        ):
            value = _attr(item, name)
            if value:
                parts.append(str(value))
    return " ".join(parts).lower()


def _scope_from_path(path: str) -> tuple[RepairAffectedArtifactKind, RepairScopeKind]:
    lowered = path.lower()
    if "test" in lowered:
        return RepairAffectedArtifactKind.TEST_FILE, RepairScopeKind.TEST_SCOPE
    if lowered.endswith((".md", ".rst", ".txt")):
        return RepairAffectedArtifactKind.DOCUMENTATION_SECTION, RepairScopeKind.DOCUMENTATION_SCOPE
    if lowered.endswith((".toml", ".yaml", ".yml", ".json", ".ini", ".cfg")):
        return RepairAffectedArtifactKind.CONFIG_FILE, RepairScopeKind.CONFIGURATION_SCOPE
    return RepairAffectedArtifactKind.SOURCE_FILE, RepairScopeKind.IMPLEMENTATION_SCOPE


def _intent_for_text(text: str, default_scope: RepairScopeKind) -> tuple[RepairChangeIntentKind, RepairScopeKind, bool, bool]:
    if "no repair" in text or "passed" in text or "no failure" in text:
        return RepairChangeIntentKind.NO_CHANGE_NEEDED, RepairScopeKind.NO_SCOPE, False, False
    if "dependency" in text or "module not found" in text or "modulenotfound" in text:
        return RepairChangeIntentKind.INSPECT_MISSING_DEPENDENCY_WITHOUT_INSTALL, RepairScopeKind.DEPENDENCY_INSPECTION_SCOPE, False, True
    if "timeout" in text or "performance" in text:
        return RepairChangeIntentKind.INSPECT_TIMEOUT_WITHOUT_RETRY, RepairScopeKind.PERFORMANCE_INVESTIGATION_SCOPE, False, True
    if "import" in text:
        return RepairChangeIntentKind.ADJUST_IMPORT_PATH_FUTURE_GATE, RepairScopeKind.IMPORT_PATH_SCOPE, True, True
    if "assert" in text or "expect" in text or "mismatch" in text:
        return RepairChangeIntentKind.REVIEW_TEST_EXPECTATION_FUTURE_GATE, default_scope, True, True
    if default_scope == RepairScopeKind.DOCUMENTATION_SCOPE:
        return RepairChangeIntentKind.CLARIFY_DOCUMENTATION_FUTURE_GATE, default_scope, True, True
    if default_scope == RepairScopeKind.CONFIGURATION_SCOPE:
        return RepairChangeIntentKind.INSPECT_CONFIGURATION_FUTURE_GATE, default_scope, True, True
    return RepairChangeIntentKind.ALIGN_IMPLEMENTATION_WITH_TEST, default_scope, True, False


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningFlagSet:
    flag_set_id: str
    version: str
    repair_scope_planning_layer_constructed: bool
    repair_scope_planner_available: bool
    change_intent_model_available: bool
    affected_file_candidates_available: bool
    affected_symbol_candidates_available: bool
    scope_evidence_map_available: bool
    scope_risk_assessment_available: bool
    do_nothing_scope_comparison_available: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_v0385_repair_proposal_safety_validation: bool
    ready_for_repair_scope_planner: bool
    ready_for_change_intent_model: bool
    ready_for_affected_file_candidates: bool
    ready_for_affected_symbol_candidates: bool
    ready_for_scope_evidence_map: bool
    ready_for_scope_risk_assessment: bool
    ready_for_do_nothing_scope_comparison: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_live_workspace_read: bool
    ready_for_unbounded_source_read: bool
    ready_for_reference_source_read: bool
    ready_for_secret_read: bool
    ready_for_source_file_write: bool
    ready_for_sandbox_source_write: bool
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
        _validate_false(self, UNSAFE_SCOPE_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningSourceRef:
    source_ref_id: str
    source_kind: RepairScopePlanningSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairScopePlanningSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningPolicy:
    scope_policy_id: str
    version: str
    allowed_modes: list[RepairScopePlanningMode | str]
    allowed_scope_kinds: list[RepairScopeKind | str]
    allowed_change_intents: list[RepairChangeIntentKind | str]
    max_file_candidates: int
    max_symbol_candidates: int
    max_change_intents: int
    require_source_context_snapshot: bool
    require_evidence_bundle: bool
    require_do_nothing_comparison: bool
    require_human_review_marker: bool
    allow_scope_planning: bool
    allow_affected_file_candidates: bool
    allow_affected_symbol_candidates: bool
    allow_scope_evidence_map: bool
    allow_change_intent_model: bool
    allow_scope_risk_assessment: bool
    allow_do_nothing_scope_comparison: bool
    allow_future_patch_metadata_input: bool
    allow_source_file_read: bool
    allow_sandbox_source_read: bool
    allow_live_workspace_read: bool
    allow_source_file_write: bool
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
        _require_non_blank("scope_policy_id", self.scope_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, RepairScopePlanningMode)
        _validate_enum_list("allowed_scope_kinds", self.allowed_scope_kinds, RepairScopeKind)
        _validate_enum_list("allowed_change_intents", self.allowed_change_intents, RepairChangeIntentKind)
        for name in ("max_file_candidates", "max_symbol_candidates", "max_change_intents"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(self, UNSAFE_SCOPE_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningInput:
    scope_input_id: str
    version: str
    source_context_snapshot_id: str | None
    source_context_assessment_id: str | None
    evidence_bundle_id: str | None
    eligibility_decision_id: str | None
    repair_suggestion_id: str | None
    feedback_report_id: str | None
    requested_mode: RepairScopePlanningMode | str
    source_refs: list[RepairScopePlanningSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairScopePlanningMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [item for item in REQUIRED_SCOPE_PROHIBITED_ACTIONS if item not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError("prohibited_runtime_actions must include all unsafe surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairAffectedFileCandidate:
    affected_file_candidate_id: str
    normalized_relative_path: str
    artifact_kind: RepairAffectedArtifactKind | str
    scope_kind: RepairScopeKind | str
    disposition: RepairScopeDisposition | str
    rationale: str
    evidence_refs: list[str]
    confidence: RepairScopeConfidenceLevel | str
    source_read_performed_by_v0383: bool
    edit_allowed: bool
    proposal_generation_allowed: bool
    diff_generation_allowed: bool
    hunk_generation_allowed: bool
    repair_execution_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("affected_file_candidate_id", "normalized_relative_path", "rationale"):
            _require_non_blank(name, getattr(self, name))
        RepairAffectedArtifactKind(self.artifact_kind)
        RepairScopeKind(self.scope_kind)
        RepairScopeDisposition(self.disposition)
        RepairScopeConfidenceLevel(self.confidence)
        if self.source_read_performed_by_v0383 is not False:
            raise ValueError("source_read_performed_by_v0383 must always be False")
        _validate_false(self, UNSAFE_CANDIDATE_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairAffectedSymbolCandidate:
    affected_symbol_candidate_id: str
    symbol_name: str | None
    normalized_relative_path: str
    artifact_kind: RepairAffectedArtifactKind | str
    scope_kind: RepairScopeKind | str
    disposition: RepairScopeDisposition | str
    rationale: str
    evidence_refs: list[str]
    confidence: RepairScopeConfidenceLevel | str
    imported_or_executed_source: bool
    edit_allowed: bool
    proposal_generation_allowed: bool
    diff_generation_allowed: bool
    hunk_generation_allowed: bool
    repair_execution_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("affected_symbol_candidate_id", "normalized_relative_path", "rationale"):
            _require_non_blank(name, getattr(self, name))
        RepairAffectedArtifactKind(self.artifact_kind)
        RepairScopeKind(self.scope_kind)
        RepairScopeDisposition(self.disposition)
        RepairScopeConfidenceLevel(self.confidence)
        if self.imported_or_executed_source is not False:
            raise ValueError("affected symbol candidate must not import or execute source")
        _validate_false(self, UNSAFE_CANDIDATE_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopeEvidenceMap:
    scope_evidence_map_id: str
    evidence_kinds: list[RepairScopeEvidenceKind | str]
    file_candidate_ids: list[str]
    symbol_candidate_ids: list[str]
    supporting_evidence_refs: list[str]
    contradictory_evidence_refs: list[str]
    missing_evidence_items: list[str]
    map_summary: str
    confidence: RepairScopeConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_evidence_map_id", "map_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_enum_list("evidence_kinds", self.evidence_kinds, RepairScopeEvidenceKind)
        for list_name in ("file_candidate_ids", "symbol_candidate_ids", "supporting_evidence_refs", "contradictory_evidence_refs", "missing_evidence_items"):
            _validate_string_list(list_name, getattr(self, list_name))
        confidence = RepairScopeConfidenceLevel(self.confidence)
        if (self.missing_evidence_items or self.contradictory_evidence_refs) and confidence == RepairScopeConfidenceLevel.HIGH:
            raise ValueError("missing or contradictory scope evidence cannot produce high confidence")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopeRiskAssessment:
    scope_risk_assessment_id: str
    risk_kinds: list[RepairScopePlanningRiskKind | str]
    risk_summary: str
    severity: str
    requires_human_review: bool
    blocks_future_patch_metadata: bool
    do_nothing_recommended: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_risk_assessment_id", "risk_summary", "severity"):
            _require_non_blank(name, getattr(self, name))
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairScopePlanningRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.severity.lower() in {"high", "critical"} and not (self.requires_human_review or self.blocks_future_patch_metadata):
            raise ValueError("high scope risk must require review or block future patch metadata")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairChangeIntent:
    change_intent_id: str
    intent_kind: RepairChangeIntentKind | str
    scope_kind: RepairScopeKind | str
    intent_summary: str
    rationale: str
    affected_file_candidate_ids: list[str]
    affected_symbol_candidate_ids: list[str]
    evidence_refs: list[str]
    confidence: RepairScopeConfidenceLevel | str
    future_patch_metadata_input_eligible: bool
    source_read_allowed_now: bool
    edit_allowed_now: bool
    proposal_generation_allowed_now: bool
    diff_generation_allowed_now: bool
    hunk_generation_allowed_now: bool
    patch_envelope_generation_allowed_now: bool
    repair_execution_allowed_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("change_intent_id", "intent_summary", "rationale"):
            _require_non_blank(name, getattr(self, name))
        intent = RepairChangeIntentKind(self.intent_kind)
        RepairScopeKind(self.scope_kind)
        RepairScopeConfidenceLevel(self.confidence)
        for list_name in ("affected_file_candidate_ids", "affected_symbol_candidate_ids", "evidence_refs"):
            _validate_string_list(list_name, getattr(self, list_name))
        if self.future_patch_metadata_input_eligible and intent in (
            RepairChangeIntentKind.NO_CHANGE_NEEDED,
            RepairChangeIntentKind.DO_NOTHING,
            RepairChangeIntentKind.HUMAN_REVIEW_ONLY,
            RepairChangeIntentKind.UNKNOWN,
        ):
            raise ValueError("do-nothing or review-only intent cannot be eligible for future patch metadata")
        _validate_false(self, UNSAFE_INTENT_NOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopeDoNothingComparison:
    do_nothing_scope_comparison_id: str
    comparison_kind: RepairScopeDoNothingComparisonKind | str
    comparison_summary: str
    evidence_refs: list[str]
    do_nothing_remains_valid: bool
    do_nothing_preferred: bool
    do_nothing_required: bool
    scope_plan_outperforms_do_nothing: bool
    confidence: RepairScopeConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("do_nothing_scope_comparison_id", "comparison_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairScopeDoNothingComparisonKind(self.comparison_kind)
        RepairScopeConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.do_nothing_remains_valid is not True:
            raise ValueError("do_nothing_remains_valid must remain True")
        if (self.do_nothing_preferred or self.do_nothing_required) and self.scope_plan_outperforms_do_nothing:
            raise ValueError("preferred or required do-nothing cannot be outperformed by scope plan")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlan:
    scope_plan_id: str
    version: str
    scope_input_id: str
    primary_scope_kind: RepairScopeKind | str
    primary_change_intent_id: str | None
    affected_file_candidates: list[RepairAffectedFileCandidate]
    affected_symbol_candidates: list[RepairAffectedSymbolCandidate]
    evidence_map: RepairScopeEvidenceMap
    risk_assessment: RepairScopeRiskAssessment
    change_intents: list[RepairChangeIntent]
    do_nothing_comparison: RepairScopeDoNothingComparison
    source_refs: list[RepairScopePlanningSourceRef]
    plan_summary: str
    ready_for_future_patch_metadata_input: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    source_read_performed_by_v0383: bool
    proposal_generated: bool
    diff_generated: bool
    hunk_generated: bool
    patch_envelope_generated: bool
    file_edit_performed: bool
    repair_executed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_plan_id", "scope_input_id", "plan_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairScopeKind(self.primary_scope_kind)
        for list_name in ("affected_file_candidates", "affected_symbol_candidates", "change_intents", "source_refs"):
            _validate_list(list_name, getattr(self, list_name))
        if not isinstance(self.evidence_map, RepairScopeEvidenceMap):
            raise TypeError("evidence_map must be RepairScopeEvidenceMap")
        if not isinstance(self.risk_assessment, RepairScopeRiskAssessment):
            raise TypeError("risk_assessment must be RepairScopeRiskAssessment")
        if not isinstance(self.do_nothing_comparison, RepairScopeDoNothingComparison):
            raise TypeError("do_nothing_comparison must be RepairScopeDoNothingComparison")
        if self.ready_for_future_patch_metadata_input:
            supported = any(intent.future_patch_metadata_input_eligible for intent in self.change_intents)
            if not supported or self.risk_assessment.blocks_future_patch_metadata or self.do_nothing_comparison.do_nothing_preferred or self.do_nothing_comparison.do_nothing_required:
                raise ValueError("future patch metadata readiness requires supported intent, acceptable risk, and non-preferred do-nothing")
        if self.ready_for_future_proposed_diff_metadata_input and not self.ready_for_future_patch_metadata_input:
            raise ValueError("future proposed diff metadata input requires future patch metadata input")
        if self.ready_for_future_proposed_code_hunk_metadata_input and not self.ready_for_future_patch_metadata_input:
            raise ValueError("future proposed code hunk metadata input requires future patch metadata input")
        _validate_false(self, UNSAFE_PLAN_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningDecision:
    scope_decision_id: str
    scope_plan_id: str | None
    decision_kind: RepairScopePlanningDecisionKind | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairScopeConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_patch_metadata_input: bool
    source_read_allowed_now: bool
    proposal_generation_allowed_now: bool
    diff_generation_allowed_now: bool
    hunk_generation_allowed_now: bool
    patch_envelope_generation_allowed_now: bool
    repair_execution_allowed_now: bool
    human_review_required: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_decision_id", "decision_summary", "rationale_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairScopePlanningDecisionKind(self.decision_kind)
        RepairScopeConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_SCOPE_DECISION_NOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairScopePlanningRiskKind | str
    decision_kind: RepairScopePlanningDecisionKind | str
    blocks_future_patch_metadata: bool
    requires_human_review: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairScopePlanningRiskKind(self.risk_kind)
        RepairScopePlanningDecisionKind(self.decision_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningValidationReport:
    validation_report_id: str
    version: str
    scope_plan_id: str
    findings: list[RepairScopePlanningValidationFinding]
    validation_summary: str
    metadata_only_scope_planning_confirmed: bool
    no_source_read_confirmed: bool
    no_source_write_confirmed: bool
    no_proposal_generation_confirmed: bool
    no_diff_generation_confirmed: bool
    no_hunk_generation_confirmed: bool
    no_patch_envelope_generation_confirmed: bool
    no_edit_confirmed: bool
    no_repair_execution_confirmed: bool
    do_nothing_comparison_confirmed: bool
    human_review_when_needed_confirmed: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "scope_plan_id", "validation_summary"):
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
class RepairScopePlanningReport:
    scope_report_id: str
    version: str
    scope_plan_id: str
    scope_decision_id: str
    validation_report_id: str
    readiness_level: RepairScopePlanningReadinessLevel | str
    status: RepairScopePlanningStatus | str
    report_summary: str
    ready_for_future_patch_metadata_input: bool
    ready_for_execution: bool
    production_certified: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("scope_report_id", "scope_plan_id", "scope_decision_id", "validation_report_id", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairScopePlanningReadinessLevel(self.readiness_level)
        RepairScopePlanningStatus(self.status)
        if self.ready_for_execution is not False or self.production_certified is not False:
            raise ValueError("scope planning report is not execution or production readiness")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningRunPreview:
    run_preview_id: str
    version: str
    requested_mode: RepairScopePlanningMode | str
    preview_summary: str
    will_read_source: bool
    will_write_files: bool
    will_generate_proposal: bool
    will_generate_diff: bool
    will_generate_hunks: bool
    will_generate_patch_envelope: bool
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
        RepairScopePlanningMode(self.requested_mode)
        for name in self.__dataclass_fields__:
            if name.startswith("will_") and getattr(self, name) is not False:
                raise ValueError(f"{name} must be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningNoGenerationGuarantee:
    guarantee_id: str
    version: str
    no_source_read: bool
    no_source_write: bool
    no_repair_proposal_generation: bool
    no_proposed_diff_generation: bool
    no_proposed_code_hunk_generation: bool
    no_proposed_patch_envelope_generation: bool
    no_file_edit: bool
    no_patch_application: bool
    no_repair_execution: bool
    no_test_execution: bool
    no_subprocess_execution: bool
    no_shell_execution: bool
    no_model_provider_invocation: bool
    no_external_agent_execution: bool
    no_dominion_runtime: bool
    guarantee_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_version(self.version)
        _validate_true(self)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0383ReadinessReport:
    readiness_report_id: str
    version: str
    scope_plan_id: str
    readiness_level: RepairScopePlanningReadinessLevel | str
    status: RepairScopePlanningStatus | str
    summary: str
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_v0385_repair_proposal_safety_validation: bool
    ready_for_repair_scope_planner: bool
    ready_for_change_intent_model: bool
    ready_for_affected_file_candidates: bool
    ready_for_affected_symbol_candidates: bool
    ready_for_scope_evidence_map: bool
    ready_for_scope_risk_assessment: bool
    ready_for_do_nothing_scope_comparison: bool
    ready_for_future_proposed_diff_metadata_input: bool
    ready_for_future_proposed_code_hunk_metadata_input: bool
    ready_for_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_live_workspace_read: bool
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
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "scope_plan_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairScopePlanningReadinessLevel(self.readiness_level)
        RepairScopePlanningStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, tuple(name for name in UNSAFE_SCOPE_FLAG_NAMES if hasattr(self, name)))
        _validate_metadata(self.metadata)


def build_repair_scope_planning_flags(**kwargs: Any) -> RepairScopePlanningFlagSet:
    safe_defaults = {
        "repair_scope_planning_layer_constructed": True,
        "repair_scope_planner_available": True,
        "change_intent_model_available": True,
        "affected_file_candidates_available": True,
        "affected_symbol_candidates_available": True,
        "scope_evidence_map_available": True,
        "scope_risk_assessment_available": True,
        "do_nothing_scope_comparison_available": True,
        **{name: True for name in SAFE_SCOPE_FLAG_NAMES},
    }
    return RepairScopePlanningFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_scope_planning_flags:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_SCOPE_FLAG_NAMES},
    )


def build_repair_scope_planning_source_ref(**kwargs: Any) -> RepairScopePlanningSourceRef:
    source_kind = kwargs.pop("source_kind", RepairScopePlanningSourceKind.V0382_SOURCE_CONTEXT_SNAPSHOT)
    return RepairScopePlanningSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", f"repair_scope_planning_source_ref:{str(source_kind)}"),
        source_kind=source_kind,
        source_id=kwargs.pop("source_id", "repair-source-context-snapshot"),
        source_summary=kwargs.pop("source_summary", "scope planning metadata source reference only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 source context metadata"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_scope_planning_policy(**kwargs: Any) -> RepairScopePlanningPolicy:
    return RepairScopePlanningPolicy(
        scope_policy_id=kwargs.pop("scope_policy_id", "repair_scope_planning_policy:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            RepairScopePlanningMode.REPAIR_SCOPE_PLAN,
            RepairScopePlanningMode.CHANGE_INTENT_MODEL,
            RepairScopePlanningMode.AFFECTED_FILE_CANDIDATES,
            RepairScopePlanningMode.AFFECTED_SYMBOL_CANDIDATES,
            RepairScopePlanningMode.SCOPE_EVIDENCE_MAP,
            RepairScopePlanningMode.SCOPE_RISK_ASSESSMENT,
            RepairScopePlanningMode.DO_NOTHING_SCOPE_COMPARISON,
            RepairScopePlanningMode.FUTURE_PATCH_METADATA_INPUT,
        ]),
        allowed_scope_kinds=kwargs.pop("allowed_scope_kinds", [item for item in RepairScopeKind]),
        allowed_change_intents=kwargs.pop("allowed_change_intents", [item for item in RepairChangeIntentKind]),
        max_file_candidates=kwargs.pop("max_file_candidates", 8),
        max_symbol_candidates=kwargs.pop("max_symbol_candidates", 12),
        max_change_intents=kwargs.pop("max_change_intents", 4),
        require_source_context_snapshot=kwargs.pop("require_source_context_snapshot", True),
        require_evidence_bundle=kwargs.pop("require_evidence_bundle", True),
        require_do_nothing_comparison=kwargs.pop("require_do_nothing_comparison", True),
        require_human_review_marker=kwargs.pop("require_human_review_marker", True),
        allow_scope_planning=kwargs.pop("allow_scope_planning", True),
        allow_affected_file_candidates=kwargs.pop("allow_affected_file_candidates", True),
        allow_affected_symbol_candidates=kwargs.pop("allow_affected_symbol_candidates", True),
        allow_scope_evidence_map=kwargs.pop("allow_scope_evidence_map", True),
        allow_change_intent_model=kwargs.pop("allow_change_intent_model", True),
        allow_scope_risk_assessment=kwargs.pop("allow_scope_risk_assessment", True),
        allow_do_nothing_scope_comparison=kwargs.pop("allow_do_nothing_scope_comparison", True),
        allow_future_patch_metadata_input=kwargs.pop("allow_future_patch_metadata_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SCOPE_POLICY_ALLOW_NAMES},
    )


def default_repair_scope_planning_policy(**kwargs: Any) -> RepairScopePlanningPolicy:
    return build_repair_scope_planning_policy(**kwargs)


def build_repair_scope_planning_input(**kwargs: Any) -> RepairScopePlanningInput:
    return RepairScopePlanningInput(
        scope_input_id=kwargs.pop("scope_input_id", "repair_scope_planning_input:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"),
        source_context_assessment_id=kwargs.pop("source_context_assessment_id", "repair_source_context_assessment:v0.38.2"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"),
        eligibility_decision_id=kwargs.pop("eligibility_decision_id", "repair_proposal_eligibility_decision:v0.38.1"),
        repair_suggestion_id=kwargs.pop("repair_suggestion_id", None),
        feedback_report_id=kwargs.pop("feedback_report_id", None),
        requested_mode=kwargs.pop("requested_mode", RepairScopePlanningMode.REPAIR_SCOPE_PLAN),
        source_refs=kwargs.pop("source_refs", [build_repair_scope_planning_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(REQUIRED_SCOPE_PROHIBITED_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "scope planning request metadata only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_affected_file_candidate(**kwargs: Any) -> RepairAffectedFileCandidate:
    path = kwargs.pop("normalized_relative_path", "pkg/module.py")
    artifact_kind, scope_kind = _scope_from_path(path)
    return RepairAffectedFileCandidate(
        affected_file_candidate_id=kwargs.pop("affected_file_candidate_id", f"repair_affected_file_candidate:{path}"),
        normalized_relative_path=path,
        artifact_kind=kwargs.pop("artifact_kind", artifact_kind),
        scope_kind=kwargs.pop("scope_kind", scope_kind),
        disposition=kwargs.pop("disposition", RepairScopeDisposition.CANDIDATE_SCOPE),
        rationale=kwargs.pop("rationale", "affected file candidate derived from supplied source context metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 source context snapshot"]),
        confidence=kwargs.pop("confidence", RepairScopeConfidenceLevel.MEDIUM),
        source_read_performed_by_v0383=kwargs.pop("source_read_performed_by_v0383", False),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_CANDIDATE_NAMES},
    )


def build_repair_affected_symbol_candidate(**kwargs: Any) -> RepairAffectedSymbolCandidate:
    symbol_name = kwargs.pop("symbol_name", "target_function")
    path = kwargs.pop("normalized_relative_path", "pkg/module.py")
    artifact_kind = RepairAffectedArtifactKind.CLASS_SYMBOL if symbol_name and symbol_name[:1].isupper() else RepairAffectedArtifactKind.FUNCTION_SYMBOL
    return RepairAffectedSymbolCandidate(
        affected_symbol_candidate_id=kwargs.pop("affected_symbol_candidate_id", f"repair_affected_symbol_candidate:{path}:{symbol_name or 'unknown'}"),
        symbol_name=symbol_name,
        normalized_relative_path=path,
        artifact_kind=kwargs.pop("artifact_kind", artifact_kind),
        scope_kind=kwargs.pop("scope_kind", RepairScopeKind.IMPLEMENTATION_SCOPE),
        disposition=kwargs.pop("disposition", RepairScopeDisposition.CANDIDATE_SCOPE),
        rationale=kwargs.pop("rationale", "affected symbol candidate derived from supplied symbol context metadata"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 symbol context hint"]),
        confidence=kwargs.pop("confidence", RepairScopeConfidenceLevel.MEDIUM),
        imported_or_executed_source=kwargs.pop("imported_or_executed_source", False),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_CANDIDATE_NAMES},
    )


def build_repair_scope_evidence_map(**kwargs: Any) -> RepairScopeEvidenceMap:
    return RepairScopeEvidenceMap(
        scope_evidence_map_id=kwargs.pop("scope_evidence_map_id", "repair_scope_evidence_map:v0.38.3"),
        evidence_kinds=kwargs.pop("evidence_kinds", [
            RepairScopeEvidenceKind.SOURCE_CONTEXT_SNAPSHOT_REF,
            RepairScopeEvidenceKind.EVIDENCE_BUNDLE_REF,
        ]),
        file_candidate_ids=kwargs.pop("file_candidate_ids", ["repair_affected_file_candidate:pkg/module.py"]),
        symbol_candidate_ids=kwargs.pop("symbol_candidate_ids", []),
        supporting_evidence_refs=kwargs.pop("supporting_evidence_refs", ["v0.38.2 source context snapshot"]),
        contradictory_evidence_refs=kwargs.pop("contradictory_evidence_refs", []),
        missing_evidence_items=kwargs.pop("missing_evidence_items", []),
        map_summary=kwargs.pop("map_summary", "scope evidence map metadata only"),
        confidence=kwargs.pop("confidence", RepairScopeConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_scope_risk_assessment(**kwargs: Any) -> RepairScopeRiskAssessment:
    return RepairScopeRiskAssessment(
        scope_risk_assessment_id=kwargs.pop("scope_risk_assessment_id", "repair_scope_risk_assessment:v0.38.3"),
        risk_kinds=kwargs.pop("risk_kinds", [
            RepairScopePlanningRiskKind.DIFF_GENERATION_CONFUSION_RISK,
            RepairScopePlanningRiskKind.EDIT_PERMISSION_CONFUSION_RISK,
        ]),
        risk_summary=kwargs.pop("risk_summary", "scope plan is metadata only and requires future gates"),
        severity=kwargs.pop("severity", "medium"),
        requires_human_review=kwargs.pop("requires_human_review", True),
        blocks_future_patch_metadata=kwargs.pop("blocks_future_patch_metadata", False),
        do_nothing_recommended=kwargs.pop("do_nothing_recommended", False),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.3 scope risk assessment"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_change_intent(**kwargs: Any) -> RepairChangeIntent:
    return RepairChangeIntent(
        change_intent_id=kwargs.pop("change_intent_id", "repair_change_intent:v0.38.3"),
        intent_kind=kwargs.pop("intent_kind", RepairChangeIntentKind.ALIGN_IMPLEMENTATION_WITH_TEST),
        scope_kind=kwargs.pop("scope_kind", RepairScopeKind.IMPLEMENTATION_SCOPE),
        intent_summary=kwargs.pop("intent_summary", "future-gated change intent metadata only"),
        rationale=kwargs.pop("rationale", "intent is derived from supplied evidence and source context metadata"),
        affected_file_candidate_ids=kwargs.pop("affected_file_candidate_ids", ["repair_affected_file_candidate:pkg/module.py"]),
        affected_symbol_candidate_ids=kwargs.pop("affected_symbol_candidate_ids", []),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 source context snapshot"]),
        confidence=kwargs.pop("confidence", RepairScopeConfidenceLevel.MEDIUM),
        future_patch_metadata_input_eligible=kwargs.pop("future_patch_metadata_input_eligible", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_INTENT_NOW_NAMES},
    )


def build_repair_scope_do_nothing_comparison(**kwargs: Any) -> RepairScopeDoNothingComparison:
    return RepairScopeDoNothingComparison(
        do_nothing_scope_comparison_id=kwargs.pop("do_nothing_scope_comparison_id", "repair_scope_do_nothing_comparison:v0.38.3"),
        comparison_kind=kwargs.pop("comparison_kind", RepairScopeDoNothingComparisonKind.SCOPE_PLAN_BETTER_THAN_DO_NOTHING),
        comparison_summary=kwargs.pop("comparison_summary", "do-nothing remains valid but scope plan may support future metadata input"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.1 do-nothing evidence", "v0.38.2 source context"]),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        do_nothing_preferred=kwargs.pop("do_nothing_preferred", False),
        do_nothing_required=kwargs.pop("do_nothing_required", False),
        scope_plan_outperforms_do_nothing=kwargs.pop("scope_plan_outperforms_do_nothing", True),
        confidence=kwargs.pop("confidence", RepairScopeConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_scope_plan(**kwargs: Any) -> RepairScopePlan:
    intents = kwargs.pop("change_intents", [build_repair_change_intent()])
    risk = kwargs.pop("risk_assessment", build_repair_scope_risk_assessment())
    comparison = kwargs.pop("do_nothing_comparison", build_repair_scope_do_nothing_comparison())
    ready = kwargs.pop(
        "ready_for_future_patch_metadata_input",
        any(intent.future_patch_metadata_input_eligible for intent in intents)
        and not risk.blocks_future_patch_metadata
        and not comparison.do_nothing_preferred
        and not comparison.do_nothing_required,
    )
    return RepairScopePlan(
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        scope_input_id=kwargs.pop("scope_input_id", "repair_scope_planning_input:v0.38.3"),
        primary_scope_kind=kwargs.pop("primary_scope_kind", RepairScopeKind.IMPLEMENTATION_SCOPE),
        primary_change_intent_id=kwargs.pop("primary_change_intent_id", intents[0].change_intent_id if intents else None),
        affected_file_candidates=kwargs.pop("affected_file_candidates", [build_repair_affected_file_candidate()]),
        affected_symbol_candidates=kwargs.pop("affected_symbol_candidates", []),
        evidence_map=kwargs.pop("evidence_map", build_repair_scope_evidence_map()),
        risk_assessment=risk,
        change_intents=intents,
        do_nothing_comparison=comparison,
        source_refs=kwargs.pop("source_refs", [build_repair_scope_planning_source_ref()]),
        plan_summary=kwargs.pop("plan_summary", "repair scope plan metadata only"),
        ready_for_future_patch_metadata_input=ready,
        ready_for_future_proposed_diff_metadata_input=kwargs.pop("ready_for_future_proposed_diff_metadata_input", ready),
        ready_for_future_proposed_code_hunk_metadata_input=kwargs.pop("ready_for_future_proposed_code_hunk_metadata_input", ready),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_PLAN_STATE_NAMES},
    )


def build_repair_scope_planning_decision(**kwargs: Any) -> RepairScopePlanningDecision:
    return RepairScopePlanningDecision(
        scope_decision_id=kwargs.pop("scope_decision_id", "repair_scope_planning_decision:v0.38.3"),
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        decision_kind=kwargs.pop("decision_kind", RepairScopePlanningDecisionKind.ALLOW_FUTURE_PATCH_METADATA_INPUT),
        decision_summary=kwargs.pop("decision_summary", "future patch metadata input is eligible as metadata only"),
        rationale_summary=kwargs.pop("rationale_summary", "scope plan supports future-gated metadata but grants no generation or execution permission"),
        confidence=kwargs.pop("confidence", RepairScopeConfidenceLevel.MEDIUM),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.3 scope plan"]),
        ready_for_future_patch_metadata_input=kwargs.pop("ready_for_future_patch_metadata_input", True),
        human_review_required=kwargs.pop("human_review_required", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SCOPE_DECISION_NOW_NAMES},
    )


def build_repair_scope_planning_input_from_source_context(
    source_context_snapshot: Any,
    evidence_bundle: Any | None = None,
    **kwargs: Any,
) -> RepairScopePlanningInput:
    return build_repair_scope_planning_input(
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", _attr(source_context_snapshot, "source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2")),
        source_context_assessment_id=kwargs.pop("source_context_assessment_id", _attr(_attr(source_context_snapshot, "context_assessment"), "context_assessment_id")),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", _attr(evidence_bundle, "evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1")),
        task_summary=kwargs.pop("task_summary", _attr(source_context_snapshot, "snapshot_summary", "scope planning request from source context metadata")),
        source_refs=kwargs.pop("source_refs", [
            build_repair_scope_planning_source_ref(
                source_kind=RepairScopePlanningSourceKind.V0382_SOURCE_CONTEXT_SNAPSHOT,
                source_id=_attr(source_context_snapshot, "source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"),
                source_summary="v0.38.2 source context snapshot metadata",
            )
        ]),
        **kwargs,
    )


def derive_affected_file_candidates_from_source_context(
    source_context_snapshot: Any,
    policy: RepairScopePlanningPolicy | None = None,
) -> list[RepairAffectedFileCandidate]:
    policy = policy or default_repair_scope_planning_policy()
    file_snapshots = list(_attr(source_context_snapshot, "file_snapshots", []) or [])
    excerpts = list(_attr(source_context_snapshot, "source_excerpts", []) or [])
    paths: list[tuple[str, str]] = []
    for snapshot in file_snapshots:
        path = _attr(snapshot, "normalized_relative_path")
        if path:
            paths.append((str(path), _attr(snapshot, "file_snapshot_id", "v0.38.2 file snapshot")))
    for excerpt in excerpts:
        path = _attr(excerpt, "normalized_relative_path")
        if path and not any(existing == path for existing, _ in paths):
            paths.append((str(path), _attr(excerpt, "source_excerpt_id", "v0.38.2 source excerpt")))
    candidates: list[RepairAffectedFileCandidate] = []
    for index, (path, evidence_ref) in enumerate(paths[: policy.max_file_candidates], start=1):
        artifact_kind, scope_kind = _scope_from_path(path)
        candidates.append(build_repair_affected_file_candidate(
            affected_file_candidate_id=f"repair_affected_file_candidate:{index}:{path}",
            normalized_relative_path=path,
            artifact_kind=artifact_kind,
            scope_kind=scope_kind,
            evidence_refs=[evidence_ref],
        ))
    return candidates


def derive_affected_symbol_candidates_from_source_context(
    source_context_snapshot: Any,
    policy: RepairScopePlanningPolicy | None = None,
) -> list[RepairAffectedSymbolCandidate]:
    policy = policy or default_repair_scope_planning_policy()
    hints = list(_attr(source_context_snapshot, "symbol_context_hints", []) or [])
    candidates: list[RepairAffectedSymbolCandidate] = []
    for index, hint in enumerate(hints[: policy.max_symbol_candidates], start=1):
        symbol_name = _attr(hint, "symbol_name")
        path = _attr(hint, "normalized_relative_path", "unknown")
        artifact_kind = RepairAffectedArtifactKind.CLASS_SYMBOL if symbol_name and str(symbol_name)[:1].isupper() else RepairAffectedArtifactKind.FUNCTION_SYMBOL
        candidates.append(build_repair_affected_symbol_candidate(
            affected_symbol_candidate_id=f"repair_affected_symbol_candidate:{index}:{path}:{symbol_name or 'unknown'}",
            symbol_name=symbol_name,
            normalized_relative_path=str(path),
            artifact_kind=artifact_kind,
            scope_kind=_scope_from_path(str(path))[1],
            evidence_refs=[_attr(hint, "symbol_context_hint_id", "v0.38.2 symbol context hint")],
        ))
    return candidates


def build_scope_evidence_map_from_context_and_evidence(
    file_candidates: list[RepairAffectedFileCandidate],
    symbol_candidates: list[RepairAffectedSymbolCandidate],
    source_context_snapshot: Any | None = None,
    evidence_bundle: Any | None = None,
) -> RepairScopeEvidenceMap:
    supporting = [_attr(source_context_snapshot, "source_context_snapshot_id", "v0.38.2 source context snapshot")]
    if evidence_bundle is not None:
        supporting.append(_attr(evidence_bundle, "evidence_bundle_id", "v0.38.1 evidence bundle"))
    missing = [] if file_candidates else ["affected file candidate"]
    return build_repair_scope_evidence_map(
        file_candidate_ids=[candidate.affected_file_candidate_id for candidate in file_candidates],
        symbol_candidate_ids=[candidate.affected_symbol_candidate_id for candidate in symbol_candidates],
        supporting_evidence_refs=supporting,
        missing_evidence_items=missing,
        confidence=RepairScopeConfidenceLevel.LOW if missing else RepairScopeConfidenceLevel.MEDIUM,
    )


def assess_repair_scope_risk(
    evidence_map: RepairScopeEvidenceMap,
    task_summary: str = "",
) -> RepairScopeRiskAssessment:
    lowered = task_summary.lower()
    risks: list[RepairScopePlanningRiskKind | str] = [
        RepairScopePlanningRiskKind.DIFF_GENERATION_CONFUSION_RISK,
        RepairScopePlanningRiskKind.EDIT_PERMISSION_CONFUSION_RISK,
        RepairScopePlanningRiskKind.HUMAN_REVIEW_OMISSION_RISK,
    ]
    severity = "medium"
    blocks = False
    do_nothing = False
    if evidence_map.missing_evidence_items:
        risks.append(RepairScopePlanningRiskKind.INSUFFICIENT_SOURCE_CONTEXT_RISK)
        severity = "high"
        blocks = True
        do_nothing = True
    if evidence_map.contradictory_evidence_refs:
        risks.append(RepairScopePlanningRiskKind.CONTRADICTORY_EVIDENCE_RISK)
        severity = "high"
        blocks = True
        do_nothing = True
    if "dependency" in lowered or "module not found" in lowered:
        risks.append(RepairScopePlanningRiskKind.DEPENDENCY_INSTALL_CONFUSION_RISK)
    if "timeout" in lowered or "retry" in lowered:
        risks.append(RepairScopePlanningRiskKind.TIMEOUT_RETRY_CONFUSION_RISK)
    return build_repair_scope_risk_assessment(
        risk_kinds=risks,
        severity=severity,
        blocks_future_patch_metadata=blocks,
        do_nothing_recommended=do_nothing,
        risk_summary="scope risk assessment blocks unsafe generation and execution confusion",
    )


def derive_repair_change_intents(
    scope_input: RepairScopePlanningInput,
    file_candidates: list[RepairAffectedFileCandidate],
    symbol_candidates: list[RepairAffectedSymbolCandidate],
    evidence_map: RepairScopeEvidenceMap,
    risk_assessment: RepairScopeRiskAssessment,
    policy: RepairScopePlanningPolicy | None = None,
) -> list[RepairChangeIntent]:
    policy = policy or default_repair_scope_planning_policy()
    text = _text_from_inputs(scope_input, evidence_map, risk_assessment)
    default_scope = file_candidates[0].scope_kind if file_candidates else RepairScopeKind.AMBIGUOUS_SCOPE
    intent_kind, scope_kind, future_eligible, review = _intent_for_text(text, RepairScopeKind(default_scope))
    if risk_assessment.blocks_future_patch_metadata:
        future_eligible = False
        review = True
    if intent_kind == RepairChangeIntentKind.NO_CHANGE_NEEDED:
        return [build_repair_change_intent(
            change_intent_id="repair_change_intent:no_change_needed:v0.38.3",
            intent_kind=RepairChangeIntentKind.NO_CHANGE_NEEDED,
            scope_kind=RepairScopeKind.NO_SCOPE,
            intent_summary="no change needed based on supplied metadata",
            rationale="do-nothing is preferred when metadata indicates no repair needed",
            affected_file_candidate_ids=[],
            affected_symbol_candidate_ids=[],
            evidence_refs=evidence_map.supporting_evidence_refs,
            confidence=RepairScopeConfidenceLevel.MEDIUM,
            future_patch_metadata_input_eligible=False,
        )]
    return [build_repair_change_intent(
        change_intent_id=f"repair_change_intent:{intent_kind.value}:v0.38.3",
        intent_kind=intent_kind,
        scope_kind=scope_kind,
        intent_summary=f"{intent_kind.value} metadata only",
        rationale="intent is future-gated and grants no code modification permission",
        affected_file_candidate_ids=[candidate.affected_file_candidate_id for candidate in file_candidates],
        affected_symbol_candidate_ids=[candidate.affected_symbol_candidate_id for candidate in symbol_candidates],
        evidence_refs=evidence_map.supporting_evidence_refs,
        confidence=RepairScopeConfidenceLevel.LOW if review else RepairScopeConfidenceLevel.MEDIUM,
        future_patch_metadata_input_eligible=future_eligible,
    )][: policy.max_change_intents]


def compare_scope_plan_to_do_nothing(
    risk_assessment: RepairScopeRiskAssessment,
    change_intents: list[RepairChangeIntent],
    evidence_refs: list[str] | None = None,
) -> RepairScopeDoNothingComparison:
    refs = evidence_refs or ["v0.38.3 scope planning"]
    if risk_assessment.blocks_future_patch_metadata or risk_assessment.do_nothing_recommended:
        return build_repair_scope_do_nothing_comparison(
            comparison_kind=RepairScopeDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_HIGH_SCOPE_RISK,
            comparison_summary="do-nothing is preferred because scope risk blocks future patch metadata",
            evidence_refs=refs,
            do_nothing_preferred=True,
            do_nothing_required=False,
            scope_plan_outperforms_do_nothing=False,
            confidence=RepairScopeConfidenceLevel.MEDIUM,
        )
    if not any(intent.future_patch_metadata_input_eligible for intent in change_intents):
        return build_repair_scope_do_nothing_comparison(
            comparison_kind=RepairScopeDoNothingComparisonKind.DO_NOTHING_COMPETITIVE_DUE_TO_LOW_CONFIDENCE,
            comparison_summary="do-nothing remains competitive because no future patch metadata intent is eligible",
            evidence_refs=refs,
            do_nothing_preferred=True,
            do_nothing_required=False,
            scope_plan_outperforms_do_nothing=False,
            confidence=RepairScopeConfidenceLevel.LOW,
        )
    return build_repair_scope_do_nothing_comparison(evidence_refs=refs)


def create_repair_scope_plan(
    scope_input: RepairScopePlanningInput,
    source_context_snapshot: Any,
    evidence_bundle: Any | None = None,
    policy: RepairScopePlanningPolicy | None = None,
) -> RepairScopePlan:
    policy = policy or default_repair_scope_planning_policy()
    files = derive_affected_file_candidates_from_source_context(source_context_snapshot, policy)
    symbols = derive_affected_symbol_candidates_from_source_context(source_context_snapshot, policy)
    evidence_map = build_scope_evidence_map_from_context_and_evidence(files, symbols, source_context_snapshot, evidence_bundle)
    risk = assess_repair_scope_risk(evidence_map, scope_input.task_summary)
    intents = derive_repair_change_intents(scope_input, files, symbols, evidence_map, risk, policy)
    comparison = compare_scope_plan_to_do_nothing(risk, intents, evidence_map.supporting_evidence_refs)
    ready = any(intent.future_patch_metadata_input_eligible for intent in intents) and not risk.blocks_future_patch_metadata and not comparison.do_nothing_preferred
    primary_scope = intents[0].scope_kind if intents else RepairScopeKind.AMBIGUOUS_SCOPE
    return build_repair_scope_plan(
        scope_input_id=scope_input.scope_input_id,
        primary_scope_kind=primary_scope,
        primary_change_intent_id=intents[0].change_intent_id if intents else None,
        affected_file_candidates=files,
        affected_symbol_candidates=symbols,
        evidence_map=evidence_map,
        risk_assessment=risk,
        change_intents=intents,
        do_nothing_comparison=comparison,
        source_refs=scope_input.source_refs,
        ready_for_future_patch_metadata_input=ready,
        ready_for_future_proposed_diff_metadata_input=ready,
        ready_for_future_proposed_code_hunk_metadata_input=ready,
    )


def decide_repair_scope_planning(plan: RepairScopePlan) -> RepairScopePlanningDecision:
    if plan.do_nothing_comparison.do_nothing_preferred or plan.do_nothing_comparison.do_nothing_required:
        return build_repair_scope_planning_decision(
            scope_plan_id=plan.scope_plan_id,
            decision_kind=RepairScopePlanningDecisionKind.CHOOSE_DO_NOTHING,
            decision_summary="do-nothing is preferred for this scope plan",
            rationale_summary="do-nothing comparison or risk assessment blocks future patch metadata",
            ready_for_future_patch_metadata_input=False,
            confidence=RepairScopeConfidenceLevel.LOW,
            evidence_refs=[plan.scope_plan_id],
        )
    if plan.ready_for_future_patch_metadata_input:
        return build_repair_scope_planning_decision(scope_plan_id=plan.scope_plan_id, evidence_refs=[plan.scope_plan_id])
    return build_repair_scope_planning_decision(
        scope_plan_id=plan.scope_plan_id,
        decision_kind=RepairScopePlanningDecisionKind.REQUIRE_REVIEW,
        decision_summary="scope plan requires human review before future patch metadata input",
        rationale_summary="scope plan is not sufficient for future patch metadata input",
        ready_for_future_patch_metadata_input=False,
        confidence=RepairScopeConfidenceLevel.LOW,
        evidence_refs=[plan.scope_plan_id],
    )


def build_repair_scope_planning_validation_finding(**kwargs: Any) -> RepairScopePlanningValidationFinding:
    return RepairScopePlanningValidationFinding(
        finding_id=kwargs.pop("finding_id", "repair_scope_planning_validation_finding:v0.38.3"),
        finding_summary=kwargs.pop("finding_summary", "scope planning preserves no generation or execution permission"),
        risk_kind=kwargs.pop("risk_kind", RepairScopePlanningRiskKind.DIFF_GENERATION_CONFUSION_RISK),
        decision_kind=kwargs.pop("decision_kind", RepairScopePlanningDecisionKind.ALLOW_SCOPE_PLANNING),
        blocks_future_patch_metadata=kwargs.pop("blocks_future_patch_metadata", False),
        requires_human_review=kwargs.pop("requires_human_review", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.3 scope validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_scope_planning_validation_report(**kwargs: Any) -> RepairScopePlanningValidationReport:
    return RepairScopePlanningValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "repair_scope_planning_validation_report:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        findings=kwargs.pop("findings", [build_repair_scope_planning_validation_finding()]),
        validation_summary=kwargs.pop("validation_summary", "scope planning validation confirms metadata-only posture"),
        metadata_only_scope_planning_confirmed=kwargs.pop("metadata_only_scope_planning_confirmed", True),
        no_source_read_confirmed=kwargs.pop("no_source_read_confirmed", True),
        no_source_write_confirmed=kwargs.pop("no_source_write_confirmed", True),
        no_proposal_generation_confirmed=kwargs.pop("no_proposal_generation_confirmed", True),
        no_diff_generation_confirmed=kwargs.pop("no_diff_generation_confirmed", True),
        no_hunk_generation_confirmed=kwargs.pop("no_hunk_generation_confirmed", True),
        no_patch_envelope_generation_confirmed=kwargs.pop("no_patch_envelope_generation_confirmed", True),
        no_edit_confirmed=kwargs.pop("no_edit_confirmed", True),
        no_repair_execution_confirmed=kwargs.pop("no_repair_execution_confirmed", True),
        do_nothing_comparison_confirmed=kwargs.pop("do_nothing_comparison_confirmed", True),
        human_review_when_needed_confirmed=kwargs.pop("human_review_when_needed_confirmed", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def validate_repair_scope_plan(plan: RepairScopePlan) -> RepairScopePlanningValidationReport:
    return build_repair_scope_planning_validation_report(scope_plan_id=plan.scope_plan_id)


def build_repair_scope_planning_report(**kwargs: Any) -> RepairScopePlanningReport:
    plan = kwargs.pop("plan", None)
    decision = kwargs.pop("decision", None)
    validation_report = kwargs.pop("validation_report", None)
    ready = kwargs.pop("ready_for_future_patch_metadata_input", plan.ready_for_future_patch_metadata_input if plan else True)
    return RepairScopePlanningReport(
        scope_report_id=kwargs.pop("scope_report_id", "repair_scope_planning_report:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        scope_plan_id=kwargs.pop("scope_plan_id", plan.scope_plan_id if plan else "repair_scope_plan:v0.38.3"),
        scope_decision_id=kwargs.pop("scope_decision_id", decision.scope_decision_id if decision else "repair_scope_planning_decision:v0.38.3"),
        validation_report_id=kwargs.pop("validation_report_id", validation_report.validation_report_id if validation_report else "repair_scope_planning_validation_report:v0.38.3"),
        readiness_level=kwargs.pop("readiness_level", RepairScopePlanningReadinessLevel.FUTURE_PATCH_METADATA_INPUT_READY if ready else RepairScopePlanningReadinessLevel.REPAIR_SCOPE_PLAN_READY),
        status=kwargs.pop("status", RepairScopePlanningStatus.READY_FOR_FUTURE_PATCH_METADATA if ready else RepairScopePlanningStatus.REVIEW_REQUIRED),
        report_summary=kwargs.pop("report_summary", "repair scope planning report metadata only"),
        ready_for_future_patch_metadata_input=ready,
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", [plan.scope_plan_id if plan else "v0.38.3 scope plan"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_scope_planning_run_preview(**kwargs: Any) -> RepairScopePlanningRunPreview:
    return RepairScopePlanningRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "repair_scope_planning_run_preview:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        requested_mode=kwargs.pop("requested_mode", RepairScopePlanningMode.REPAIR_SCOPE_PLAN),
        preview_summary=kwargs.pop("preview_summary", "scope planning preview performs metadata derivation only"),
        will_read_source=kwargs.pop("will_read_source", False),
        will_write_files=kwargs.pop("will_write_files", False),
        will_generate_proposal=kwargs.pop("will_generate_proposal", False),
        will_generate_diff=kwargs.pop("will_generate_diff", False),
        will_generate_hunks=kwargs.pop("will_generate_hunks", False),
        will_generate_patch_envelope=kwargs.pop("will_generate_patch_envelope", False),
        will_apply_patch=kwargs.pop("will_apply_patch", False),
        will_execute_repair=kwargs.pop("will_execute_repair", False),
        will_run_tests=kwargs.pop("will_run_tests", False),
        will_invoke_model_provider=kwargs.pop("will_invoke_model_provider", False),
        will_invoke_external_agent=kwargs.pop("will_invoke_external_agent", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_scope_planning_no_generation_guarantee(**kwargs: Any) -> RepairScopePlanningNoGenerationGuarantee:
    return RepairScopePlanningNoGenerationGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_scope_planning_no_generation_guarantee:v0.38.3"),
        version=kwargs.pop("version", V0383_VERSION),
        no_source_read=kwargs.pop("no_source_read", True),
        no_source_write=kwargs.pop("no_source_write", True),
        no_repair_proposal_generation=kwargs.pop("no_repair_proposal_generation", True),
        no_proposed_diff_generation=kwargs.pop("no_proposed_diff_generation", True),
        no_proposed_code_hunk_generation=kwargs.pop("no_proposed_code_hunk_generation", True),
        no_proposed_patch_envelope_generation=kwargs.pop("no_proposed_patch_envelope_generation", True),
        no_file_edit=kwargs.pop("no_file_edit", True),
        no_patch_application=kwargs.pop("no_patch_application", True),
        no_repair_execution=kwargs.pop("no_repair_execution", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_subprocess_execution=kwargs.pop("no_subprocess_execution", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_model_provider_invocation=kwargs.pop("no_model_provider_invocation", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        guarantee_summary=kwargs.pop("guarantee_summary", "v0.38.3 scope planning creates no proposal, diff, hunk, patch, edit, or execution"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v0383_readiness_report(**kwargs: Any) -> V0383ReadinessReport:
    return V0383ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0383_readiness_report"),
        version=kwargs.pop("version", V0383_VERSION),
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        readiness_level=kwargs.pop("readiness_level", RepairScopePlanningReadinessLevel.FUTURE_PATCH_METADATA_INPUT_READY),
        status=kwargs.pop("status", RepairScopePlanningStatus.READY_FOR_FUTURE_PATCH_METADATA),
        summary=kwargs.pop("summary", "v0.38.3 scope planning is ready for design-stage v0.38.4 handoff only"),
        ready_for_v0384_proposed_diff_code_hunk_metadata=kwargs.pop("ready_for_v0384_proposed_diff_code_hunk_metadata", True),
        ready_for_v0385_repair_proposal_safety_validation=kwargs.pop("ready_for_v0385_repair_proposal_safety_validation", True),
        ready_for_repair_scope_planner=kwargs.pop("ready_for_repair_scope_planner", True),
        ready_for_change_intent_model=kwargs.pop("ready_for_change_intent_model", True),
        ready_for_affected_file_candidates=kwargs.pop("ready_for_affected_file_candidates", True),
        ready_for_affected_symbol_candidates=kwargs.pop("ready_for_affected_symbol_candidates", True),
        ready_for_scope_evidence_map=kwargs.pop("ready_for_scope_evidence_map", True),
        ready_for_scope_risk_assessment=kwargs.pop("ready_for_scope_risk_assessment", True),
        ready_for_do_nothing_scope_comparison=kwargs.pop("ready_for_do_nothing_scope_comparison", True),
        ready_for_future_proposed_diff_metadata_input=kwargs.pop("ready_for_future_proposed_diff_metadata_input", True),
        ready_for_future_proposed_code_hunk_metadata_input=kwargs.pop("ready_for_future_proposed_code_hunk_metadata_input", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.3 scope plan"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SCOPE_FLAG_NAMES if hasattr(V0383ReadinessReport, name) or name in V0383ReadinessReport.__dataclass_fields__},
    )


def repair_scope_planning_flags_preserve_no_generation(flags: RepairScopePlanningFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_SCOPE_FLAG_NAMES)


def repair_scope_policy_blocks_generation_and_execution(policy: RepairScopePlanningPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_SCOPE_POLICY_ALLOW_NAMES)


def repair_scope_plan_is_not_proposal(plan: RepairScopePlan) -> bool:
    return all(getattr(plan, name) is False for name in UNSAFE_PLAN_STATE_NAMES)


def repair_change_intent_is_not_code_modification(intent: RepairChangeIntent) -> bool:
    return all(getattr(intent, name) is False for name in UNSAFE_INTENT_NOW_NAMES)


def repair_scope_decision_is_not_generation_permission(decision: RepairScopePlanningDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_SCOPE_DECISION_NOW_NAMES)


def v0383_readiness_report_is_not_execution_ready(report: V0383ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_SCOPE_FLAG_NAMES if hasattr(report, name))
