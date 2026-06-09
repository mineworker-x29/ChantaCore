from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0384_VERSION = "v0.38.4"
V0384_RELEASE_NAME = "v0.38.4 Proposed Diff / Code Hunk Metadata Generation"

SAFE_PATCH_METADATA_FLAG_NAMES = (
    "ready_for_v0385_repair_proposal_safety_validation",
    "ready_for_v0386_human_review_packet",
    "ready_for_repair_patch_metadata_generation",
    "ready_for_proposed_diff_metadata_generation",
    "ready_for_proposed_code_hunk_metadata_generation",
    "ready_for_proposed_patch_envelope_metadata_generation",
    "ready_for_proposed_file_change_metadata",
    "ready_for_change_rationale_metadata",
    "ready_for_patch_evidence_map",
    "ready_for_patch_do_nothing_comparison",
    "ready_for_patch_review_requirement",
    "ready_for_future_repair_proposal_safety_validation_input",
    "ready_for_future_human_review_packet_input",
)

UNSAFE_PATCH_METADATA_FLAG_NAMES = (
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
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_PATCH_METADATA_POLICY_ALLOW_NAMES = (
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_live_workspace_read",
    "allow_source_file_write",
    "allow_sandbox_source_write",
    "allow_patch_file_write",
    "allow_file_edit",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_repair_execution",
    "allow_automatic_repair",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_HUNK_STATE_NAMES = (
    "source_read_performed_by_v0384",
    "write_performed",
    "edit_applied",
    "patch_applied",
    "repair_executed",
)

UNSAFE_DIFF_STATE_NAMES = (
    "written_to_file",
    "applied",
    "repair_executed",
)

UNSAFE_FILE_CHANGE_STATE_NAMES = (
    "creates_new_file",
    "deletes_file",
    "renames_file",
    "changes_permissions",
    "writes_file",
    "applies_patch",
    "repair_executed",
)

UNSAFE_ENVELOPE_STATE_NAMES = (
    "source_read_performed_by_v0384",
    "file_write_performed",
    "patch_file_written",
    "file_edit_performed",
    "patch_applied",
    "apply_patch_called",
    "git_apply_called",
    "tests_run",
    "repair_executed",
    "production_certified",
    "ready_for_execution",
)

UNSAFE_PATCH_DECISION_NOW_NAMES = (
    "source_read_allowed_now",
    "write_allowed_now",
    "patch_file_write_allowed_now",
    "edit_allowed_now",
    "apply_allowed_now",
    "apply_patch_allowed_now",
    "git_apply_allowed_now",
    "repair_execution_allowed_now",
    "test_execution_allowed_now",
    "model_provider_invocation_allowed_now",
    "external_agent_allowed_now",
)

REQUIRED_PATCH_METADATA_PROHIBITED_ACTIONS = (
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

UNSAFE_OPERATION_TOKENS = (
    "install",
    "pip ",
    "npm ",
    "retry loop",
    "while true",
    "subprocess",
    "shell",
    "os system",
    "network",
    "requests",
    "httpx",
    "socket",
    "model provider",
    "external agent",
    "dominion",
    "credential",
    "secret",
    "token",
    "delete file",
    "rename file",
    "chmod",
    "permission",
    "binary",
)


class RepairPatchMetadataMode(StrEnum):
    PROPOSED_DIFF_METADATA = "proposed_diff_metadata"
    PROPOSED_CODE_HUNK_METADATA = "proposed_code_hunk_metadata"
    PROPOSED_FILE_CHANGE_METADATA = "proposed_file_change_metadata"
    PROPOSED_PATCH_ENVELOPE_METADATA = "proposed_patch_envelope_metadata"
    CHANGE_RATIONALE_METADATA = "change_rationale_metadata"
    PATCH_EVIDENCE_MAP = "patch_evidence_map"
    DO_NOTHING_PATCH_COMPARISON = "do_nothing_patch_comparison"
    FUTURE_SAFETY_VALIDATION_INPUT = "future_safety_validation_input"
    FUTURE_HUMAN_REVIEW_PACKET_INPUT = "future_human_review_packet_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairPatchMetadataSourceKind(StrEnum):
    V0383_REPAIR_SCOPE_PLAN = "v0383_repair_scope_plan"
    V0383_REPAIR_CHANGE_INTENT = "v0383_repair_change_intent"
    V0383_AFFECTED_FILE_CANDIDATE = "v0383_affected_file_candidate"
    V0383_AFFECTED_SYMBOL_CANDIDATE = "v0383_affected_symbol_candidate"
    V0383_SCOPE_EVIDENCE_MAP = "v0383_scope_evidence_map"
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0382_SOURCE_EXCERPT = "v0382_source_excerpt"
    V0382_SYMBOL_CONTEXT_HINT = "v0382_symbol_context_hint"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0381_ELIGIBILITY_DECISION = "v0381_eligibility_decision"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    V0375_REPAIR_SUGGESTION_ENVELOPE = "v0375_repair_suggestion_envelope"
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairPatchMetadataStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    DIFF_METADATA_CREATED = "diff_metadata_created"
    HUNK_METADATA_CREATED = "hunk_metadata_created"
    PATCH_ENVELOPE_CREATED = "patch_envelope_created"
    PATCH_ENVELOPE_CREATED_WITH_WARNINGS = "patch_envelope_created_with_warnings"
    READY_FOR_FUTURE_SAFETY_VALIDATION = "ready_for_future_safety_validation"
    READY_FOR_FUTURE_HUMAN_REVIEW_PACKET = "ready_for_future_human_review_packet"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    INSUFFICIENT_SCOPE = "insufficient_scope"
    INSUFFICIENT_SOURCE_CONTEXT = "insufficient_source_context"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairPatchMetadataReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    PATCH_METADATA_CONTRACT_READY = "patch_metadata_contract_ready"
    PROPOSED_DIFF_METADATA_READY = "proposed_diff_metadata_ready"
    PROPOSED_CODE_HUNK_METADATA_READY = "proposed_code_hunk_metadata_ready"
    PROPOSED_FILE_CHANGE_METADATA_READY = "proposed_file_change_metadata_ready"
    PROPOSED_PATCH_ENVELOPE_METADATA_READY = "proposed_patch_envelope_metadata_ready"
    PATCH_EVIDENCE_MAP_READY = "patch_evidence_map_ready"
    PATCH_DO_NOTHING_COMPARISON_READY = "patch_do_nothing_comparison_ready"
    FUTURE_SAFETY_VALIDATION_INPUT_READY = "future_safety_validation_input_ready"
    FUTURE_HUMAN_REVIEW_PACKET_INPUT_READY = "future_human_review_packet_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0385 = "design_handoff_ready_for_v0385"
    DESIGN_HANDOFF_READY_FOR_V0386 = "design_handoff_ready_for_v0386"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairPatchMetadataDecisionKind(StrEnum):
    ALLOW_PROPOSED_DIFF_METADATA = "allow_proposed_diff_metadata"
    ALLOW_PROPOSED_CODE_HUNK_METADATA = "allow_proposed_code_hunk_metadata"
    ALLOW_PROPOSED_FILE_CHANGE_METADATA = "allow_proposed_file_change_metadata"
    ALLOW_PROPOSED_PATCH_ENVELOPE_METADATA = "allow_proposed_patch_envelope_metadata"
    ALLOW_CHANGE_RATIONALE_METADATA = "allow_change_rationale_metadata"
    ALLOW_PATCH_EVIDENCE_MAP = "allow_patch_evidence_map"
    ALLOW_DO_NOTHING_PATCH_COMPARISON = "allow_do_nothing_patch_comparison"
    ALLOW_FUTURE_SAFETY_VALIDATION_INPUT = "allow_future_safety_validation_input"
    ALLOW_FUTURE_HUMAN_REVIEW_PACKET_INPUT = "allow_future_human_review_packet_input"
    CHOOSE_NO_PATCH_NEEDED = "choose_no_patch_needed"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW = "choose_human_review"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    INSUFFICIENT_SCOPE = "insufficient_scope"
    INSUFFICIENT_SOURCE_CONTEXT = "insufficient_source_context"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairPatchMetadataRiskKind(StrEnum):
    MISSING_SCOPE_PLAN_RISK = "missing_scope_plan_risk"
    MISSING_CHANGE_INTENT_RISK = "missing_change_intent_risk"
    MISSING_SOURCE_CONTEXT_RISK = "missing_source_context_risk"
    INSUFFICIENT_SOURCE_CONTEXT_RISK = "insufficient_source_context_risk"
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    CONTRADICTORY_EVIDENCE_RISK = "contradictory_evidence_risk"
    WRONG_SCOPE_RISK = "wrong_scope_risk"
    OVERBROAD_PATCH_RISK = "overbroad_patch_risk"
    UNDERBROAD_PATCH_RISK = "underbroad_patch_risk"
    UNSAFE_OPERATION_RISK = "unsafe_operation_risk"
    FILE_DELETION_RISK = "file_deletion_risk"
    FILE_RENAME_RISK = "file_rename_risk"
    BINARY_CHANGE_RISK = "binary_change_risk"
    PERMISSION_CHANGE_RISK = "permission_change_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_CALL_RISK = "network_call_risk"
    SUBPROCESS_SHELL_ADDITION_RISK = "subprocess_shell_addition_risk"
    MODEL_PROVIDER_CALL_RISK = "model_provider_call_risk"
    EXTERNAL_AGENT_CALL_RISK = "external_agent_call_risk"
    CREDENTIAL_SECRET_READ_RISK = "credential_secret_read_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    HUMAN_REVIEW_OMISSION_RISK = "human_review_omission_risk"
    APPLIED_PATCH_CONFUSION_RISK = "applied_patch_confusion_risk"
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class ProposedPatchArtifactKind(StrEnum):
    PROPOSED_PATCH_ENVELOPE = "proposed_patch_envelope"
    PROPOSED_FILE_CHANGE = "proposed_file_change"
    PROPOSED_DIFF_METADATA = "proposed_diff_metadata"
    PROPOSED_CODE_HUNK = "proposed_code_hunk"
    PROPOSED_CHANGE_RATIONALE = "proposed_change_rationale"
    PROPOSED_EVIDENCE_MAP = "proposed_evidence_map"
    PROPOSED_REVIEW_NOTE = "proposed_review_note"
    NO_PATCH_ARTIFACT = "no_patch_artifact"
    UNKNOWN = "unknown"


class ProposedDiffFormatKind(StrEnum):
    UNIFIED_DIFF_LIKE_METADATA = "unified_diff_like_metadata"
    STRUCTURED_DIFF_METADATA = "structured_diff_metadata"
    TEXT_REPLACEMENT_METADATA = "text_replacement_metadata"
    INSERT_METADATA = "insert_metadata"
    DELETE_METADATA = "delete_metadata"
    NO_DIFF = "no_diff"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


class ProposedCodeHunkKind(StrEnum):
    REPLACE_BOUNDED_TEXT = "replace_bounded_text"
    INSERT_BOUNDED_TEXT = "insert_bounded_text"
    REMOVE_BOUNDED_TEXT = "remove_bounded_text"
    IMPORT_PATH_ADJUSTMENT = "import_path_adjustment"
    CONFIG_VALUE_ADJUSTMENT = "config_value_adjustment"
    TEST_EXPECTATION_REVIEW_NOTE = "test_expectation_review_note"
    DOCUMENTATION_CLARIFICATION = "documentation_clarification"
    NO_HUNK = "no_hunk"
    UNSUPPORTED = "unsupported"
    UNKNOWN = "unknown"


class ProposedChangeOperationKind(StrEnum):
    NO_CHANGE = "no_change"
    PROPOSE_REPLACE = "propose_replace"
    PROPOSE_INSERT = "propose_insert"
    PROPOSE_REMOVE = "propose_remove"
    PROPOSE_IMPORT_ADJUSTMENT = "propose_import_adjustment"
    PROPOSE_CONFIG_ADJUSTMENT = "propose_config_adjustment"
    PROPOSE_TEST_REVIEW = "propose_test_review"
    PROPOSE_DOCUMENTATION_UPDATE = "propose_documentation_update"
    BLOCKED_OPERATION = "blocked_operation"
    UNSUPPORTED_OPERATION = "unsupported_operation"
    UNKNOWN = "unknown"


class ProposedPatchDisposition(StrEnum):
    PROPOSED = "proposed"
    PROPOSED_WITH_WARNINGS = "proposed_with_warnings"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_PATCH_NEEDED = "no_patch_needed"
    INSUFFICIENT_CONTEXT = "insufficient_context"
    UNSAFE_OPERATION_BLOCKED = "unsafe_operation_blocked"
    UNKNOWN = "unknown"


class ProposedPatchConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class ProposedPatchReviewRequirementKind(StrEnum):
    HUMAN_REVIEW_REQUIRED = "human_review_required"
    HUMAN_REVIEW_REQUIRED_DUE_TO_RISK = "human_review_required_due_to_risk"
    HUMAN_REVIEW_REQUIRED_DUE_TO_LOW_CONFIDENCE = "human_review_required_due_to_low_confidence"
    HUMAN_REVIEW_REQUIRED_BEFORE_SAFETY_VALIDATION = "human_review_required_before_safety_validation"
    HUMAN_REVIEW_REQUIRED_BEFORE_ANY_APPLY = "human_review_required_before_any_apply"
    NO_REVIEW_REQUIRED_FOR_NO_OP = "no_review_required_for_no_op"
    UNKNOWN = "unknown"


class ProposedPatchDoNothingComparisonKind(StrEnum):
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    DO_NOTHING_COMPETITIVE = "do_nothing_competitive"
    PATCH_METADATA_BETTER_THAN_DO_NOTHING = "patch_metadata_better_than_do_nothing"
    DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_CONTEXT = "do_nothing_required_due_to_insufficient_context"
    DO_NOTHING_REQUIRED_DUE_TO_HIGH_RISK = "do_nothing_required_due_to_high_risk"
    DO_NOTHING_NOT_EVALUABLE_YET = "do_nothing_not_evaluable_yet"
    UNKNOWN = "unknown"


class ProposedPatchEvidenceKind(StrEnum):
    SCOPE_PLAN_REF = "scope_plan_ref"
    CHANGE_INTENT_REF = "change_intent_ref"
    AFFECTED_FILE_REF = "affected_file_ref"
    AFFECTED_SYMBOL_REF = "affected_symbol_ref"
    SOURCE_EXCERPT_REF = "source_excerpt_ref"
    SOURCE_CONTEXT_SNAPSHOT_REF = "source_context_snapshot_ref"
    EVIDENCE_BUNDLE_REF = "evidence_bundle_ref"
    COLD_SCORECARD_REF = "cold_scorecard_ref"
    REPAIR_SUGGESTION_REF = "repair_suggestion_ref"
    FEEDBACK_REPORT_REF = "feedback_report_ref"
    TEST_RESULT_REF = "test_result_ref"
    HUMAN_OPERATOR_NOTE = "human_operator_note"
    DO_NOTHING_REF = "do_nothing_ref"
    MISSING_EVIDENCE = "missing_evidence"
    CONTRADICTORY_EVIDENCE = "contradictory_evidence"
    UNKNOWN = "unknown"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0384_VERSION not in version:
        raise ValueError("version must include v0.38.4")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.4")


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


def _bounded_text(value: str, limit: int) -> tuple[str, bool]:
    if limit >= 0 and len(value) > limit:
        return value[:limit], True
    return value, False


def _text_from_inputs(*items: Any) -> str:
    parts: list[str] = []
    for item in items:
        if item is None:
            continue
        for name in (
            "task_summary",
            "plan_summary",
            "intent_summary",
            "rationale",
            "snapshot_summary",
            "excerpt_summary",
            "comparison_summary",
            "metadata",
        ):
            value = _attr(item, name)
            if value:
                parts.append(str(value))
    return " ".join(parts).lower()


def _detect_unsafe_tokens(*texts: str) -> list[RepairPatchMetadataRiskKind]:
    lowered = " ".join(texts).lower()
    risks: list[RepairPatchMetadataRiskKind] = []
    if "install" in lowered or "pip " in lowered or "npm " in lowered:
        risks.append(RepairPatchMetadataRiskKind.DEPENDENCY_INSTALL_RISK)
    if "retry loop" in lowered or "while true" in lowered:
        risks.append(RepairPatchMetadataRiskKind.UNSAFE_OPERATION_RISK)
    if "subprocess" in lowered or "shell" in lowered or "os system" in lowered:
        risks.append(RepairPatchMetadataRiskKind.SUBPROCESS_SHELL_ADDITION_RISK)
    if "network" in lowered or "requests" in lowered or "httpx" in lowered or "socket" in lowered:
        risks.append(RepairPatchMetadataRiskKind.NETWORK_CALL_RISK)
    if "model provider" in lowered:
        risks.append(RepairPatchMetadataRiskKind.MODEL_PROVIDER_CALL_RISK)
    if "external agent" in lowered:
        risks.append(RepairPatchMetadataRiskKind.EXTERNAL_AGENT_CALL_RISK)
    if "dominion" in lowered:
        risks.append(RepairPatchMetadataRiskKind.DOMINION_RUNTIME_RISK)
    if "credential" in lowered or "secret" in lowered or "token" in lowered:
        risks.append(RepairPatchMetadataRiskKind.CREDENTIAL_SECRET_READ_RISK)
    if "delete file" in lowered:
        risks.append(RepairPatchMetadataRiskKind.FILE_DELETION_RISK)
    if "rename file" in lowered:
        risks.append(RepairPatchMetadataRiskKind.FILE_RENAME_RISK)
    if "chmod" in lowered or "permission" in lowered:
        risks.append(RepairPatchMetadataRiskKind.PERMISSION_CHANGE_RISK)
    if "binary" in lowered:
        risks.append(RepairPatchMetadataRiskKind.BINARY_CHANGE_RISK)
    return risks


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataFlagSet:
    flag_set_id: str
    version: str
    repair_patch_metadata_layer_constructed: bool
    proposed_diff_metadata_available: bool
    proposed_code_hunk_metadata_available: bool
    proposed_file_change_metadata_available: bool
    proposed_patch_envelope_metadata_available: bool
    proposed_change_rationale_available: bool
    proposed_change_evidence_map_available: bool
    proposed_patch_do_nothing_comparison_available: bool
    proposed_patch_review_requirement_available: bool
    ready_for_v0385_repair_proposal_safety_validation: bool
    ready_for_v0386_human_review_packet: bool
    ready_for_repair_patch_metadata_generation: bool
    ready_for_proposed_diff_metadata_generation: bool
    ready_for_proposed_code_hunk_metadata_generation: bool
    ready_for_proposed_patch_envelope_metadata_generation: bool
    ready_for_proposed_file_change_metadata: bool
    ready_for_change_rationale_metadata: bool
    ready_for_patch_evidence_map: bool
    ready_for_patch_do_nothing_comparison: bool
    ready_for_patch_review_requirement: bool
    ready_for_future_repair_proposal_safety_validation_input: bool
    ready_for_future_human_review_packet_input: bool
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
    ready_for_ui_runtime: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_PATCH_METADATA_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataSourceRef:
    source_ref_id: str
    source_kind: RepairPatchMetadataSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairPatchMetadataSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataPolicy:
    patch_metadata_policy_id: str
    version: str
    allowed_modes: list[RepairPatchMetadataMode | str]
    allowed_diff_formats: list[ProposedDiffFormatKind | str]
    allowed_hunk_kinds: list[ProposedCodeHunkKind | str]
    allowed_operations: list[ProposedChangeOperationKind | str]
    prohibited_risk_kinds: list[RepairPatchMetadataRiskKind | str]
    max_file_changes: int
    max_hunks: int
    max_diff_text_chars: int
    max_hunk_text_chars: int
    max_total_patch_metadata_chars: int
    require_scope_plan: bool
    require_change_intent: bool
    require_source_context_snapshot: bool
    require_evidence_bundle: bool
    require_do_nothing_comparison: bool
    require_human_review_requirement: bool
    allow_proposed_diff_metadata: bool
    allow_proposed_code_hunk_metadata: bool
    allow_proposed_file_change_metadata: bool
    allow_proposed_patch_envelope_metadata: bool
    allow_change_rationale_metadata: bool
    allow_patch_evidence_map: bool
    allow_future_safety_validation_input: bool
    allow_future_human_review_packet_input: bool
    allow_source_file_read: bool
    allow_sandbox_source_read: bool
    allow_live_workspace_read: bool
    allow_source_file_write: bool
    allow_sandbox_source_write: bool
    allow_patch_file_write: bool
    allow_file_edit: bool
    allow_patch_application: bool
    allow_apply_patch: bool
    allow_git_apply: bool
    allow_repair_execution: bool
    allow_automatic_repair: bool
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
        _require_non_blank("patch_metadata_policy_id", self.patch_metadata_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, RepairPatchMetadataMode)
        _validate_enum_list("allowed_diff_formats", self.allowed_diff_formats, ProposedDiffFormatKind)
        _validate_enum_list("allowed_hunk_kinds", self.allowed_hunk_kinds, ProposedCodeHunkKind)
        _validate_enum_list("allowed_operations", self.allowed_operations, ProposedChangeOperationKind)
        _validate_enum_list("prohibited_risk_kinds", self.prohibited_risk_kinds, RepairPatchMetadataRiskKind)
        for name in ("max_file_changes", "max_hunks", "max_diff_text_chars", "max_hunk_text_chars", "max_total_patch_metadata_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(self, UNSAFE_PATCH_METADATA_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataInput:
    patch_metadata_input_id: str
    version: str
    scope_plan_id: str | None
    primary_change_intent_id: str | None
    source_context_snapshot_id: str | None
    evidence_bundle_id: str | None
    requested_mode: RepairPatchMetadataMode | str
    source_refs: list[RepairPatchMetadataSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("patch_metadata_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairPatchMetadataMode(self.requested_mode)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        missing = [item for item in REQUIRED_PATCH_METADATA_PROHIBITED_ACTIONS if item not in self.prohibited_runtime_actions]
        if missing:
            raise ValueError("prohibited_runtime_actions must include all unsafe patch metadata surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedChangeEvidenceMap:
    change_evidence_map_id: str
    evidence_kinds: list[ProposedPatchEvidenceKind | str]
    supporting_evidence_refs: list[str]
    contradictory_evidence_refs: list[str]
    missing_evidence_items: list[str]
    scope_plan_refs: list[str]
    source_excerpt_refs: list[str]
    map_summary: str
    confidence: ProposedPatchConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("change_evidence_map_id", "map_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_enum_list("evidence_kinds", self.evidence_kinds, ProposedPatchEvidenceKind)
        for list_name in ("supporting_evidence_refs", "contradictory_evidence_refs", "missing_evidence_items", "scope_plan_refs", "source_excerpt_refs"):
            _validate_string_list(list_name, getattr(self, list_name))
        confidence = ProposedPatchConfidenceLevel(self.confidence)
        if (self.contradictory_evidence_refs or self.missing_evidence_items) and confidence == ProposedPatchConfidenceLevel.HIGH:
            raise ValueError("missing or contradictory evidence cannot produce high patch metadata confidence")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedChangeRationale:
    change_rationale_id: str
    rationale_summary: str
    intent_kind: str
    scope_kind: str
    evidence_map_id: str
    human_review_required: bool
    confidence: ProposedPatchConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("change_rationale_id", "rationale_summary", "evidence_map_id"):
            _require_non_blank(name, getattr(self, name))
        _require_non_blank("intent_kind", self.intent_kind)
        _require_non_blank("scope_kind", self.scope_kind)
        ProposedPatchConfidenceLevel(self.confidence)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedCodeHunk:
    proposed_hunk_id: str
    hunk_kind: ProposedCodeHunkKind | str
    operation_kind: ProposedChangeOperationKind | str
    target_relative_path: str
    target_excerpt_id: str | None
    original_text: str
    proposed_text: str
    hunk_summary: str
    start_line: int | None
    end_line: int | None
    evidence_refs: list[str]
    confidence: ProposedPatchConfidenceLevel | str
    bounded: bool
    redacted: bool
    generated_from_source_context: bool
    source_read_performed_by_v0384: bool
    write_performed: bool
    edit_applied: bool
    patch_applied: bool
    repair_executed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("proposed_hunk_id", "target_relative_path", "hunk_summary"):
            _require_non_blank(name, getattr(self, name))
        ProposedCodeHunkKind(self.hunk_kind)
        operation = ProposedChangeOperationKind(self.operation_kind)
        ProposedPatchConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.bounded is not True:
            raise ValueError("proposed code hunk text must be bounded")
        if operation in (ProposedChangeOperationKind.BLOCKED_OPERATION, ProposedChangeOperationKind.UNSUPPORTED_OPERATION) and self.confidence == ProposedPatchConfidenceLevel.HIGH:
            raise ValueError("blocked or unsupported operation cannot be high confidence")
        _validate_false(self, UNSAFE_HUNK_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedDiffMetadata:
    proposed_diff_id: str
    diff_format: ProposedDiffFormatKind | str
    target_relative_path: str
    proposed_diff_text: str
    diff_summary: str
    hunk_ids: list[str]
    evidence_map_id: str
    confidence: ProposedPatchConfidenceLevel | str
    bounded: bool
    redacted: bool
    in_memory_only: bool
    written_to_file: bool
    applied: bool
    repair_executed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("proposed_diff_id", "target_relative_path", "diff_summary", "evidence_map_id"):
            _require_non_blank(name, getattr(self, name))
        ProposedDiffFormatKind(self.diff_format)
        ProposedPatchConfidenceLevel(self.confidence)
        _validate_string_list("hunk_ids", self.hunk_ids)
        if self.bounded is not True or self.in_memory_only is not True:
            raise ValueError("proposed diff metadata must be bounded and in-memory only")
        _validate_false(self, UNSAFE_DIFF_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedFileChange:
    proposed_file_change_id: str
    target_relative_path: str
    artifact_kind: ProposedPatchArtifactKind | str
    disposition: ProposedPatchDisposition | str
    operation_kinds: list[ProposedChangeOperationKind | str]
    proposed_hunks: list[ProposedCodeHunk]
    proposed_diff: ProposedDiffMetadata | None
    rationale: ProposedChangeRationale
    evidence_map: ProposedChangeEvidenceMap
    file_change_summary: str
    confidence: ProposedPatchConfidenceLevel | str
    creates_new_file: bool
    deletes_file: bool
    renames_file: bool
    changes_permissions: bool
    writes_file: bool
    applies_patch: bool
    repair_executed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("proposed_file_change_id", "target_relative_path", "file_change_summary"):
            _require_non_blank(name, getattr(self, name))
        ProposedPatchArtifactKind(self.artifact_kind)
        ProposedPatchDisposition(self.disposition)
        _validate_enum_list("operation_kinds", self.operation_kinds, ProposedChangeOperationKind)
        _validate_list("proposed_hunks", self.proposed_hunks)
        if self.proposed_diff is not None and not isinstance(self.proposed_diff, ProposedDiffMetadata):
            raise TypeError("proposed_diff must be ProposedDiffMetadata or None")
        if not isinstance(self.rationale, ProposedChangeRationale):
            raise TypeError("rationale must be ProposedChangeRationale")
        if not isinstance(self.evidence_map, ProposedChangeEvidenceMap):
            raise TypeError("evidence_map must be ProposedChangeEvidenceMap")
        ProposedPatchConfidenceLevel(self.confidence)
        _validate_false(self, UNSAFE_FILE_CHANGE_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedPatchReviewRequirement:
    review_requirement_id: str
    requirement_kind: ProposedPatchReviewRequirementKind | str
    requirement_summary: str
    required_before_safety_validation: bool
    required_before_human_review_packet: bool
    required_before_any_apply: bool
    human_approval_present: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("review_requirement_id", "requirement_summary"):
            _require_non_blank(name, getattr(self, name))
        ProposedPatchReviewRequirementKind(self.requirement_kind)
        if self.human_approval_present is not False:
            raise ValueError("human_approval_present must always be False in v0.38.4")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedPatchDoNothingComparison:
    do_nothing_patch_comparison_id: str
    comparison_kind: ProposedPatchDoNothingComparisonKind | str
    comparison_summary: str
    evidence_refs: list[str]
    do_nothing_remains_valid: bool
    do_nothing_preferred: bool
    do_nothing_required: bool
    patch_metadata_outperforms_do_nothing: bool
    confidence: ProposedPatchConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("do_nothing_patch_comparison_id", "comparison_summary"):
            _require_non_blank(name, getattr(self, name))
        ProposedPatchDoNothingComparisonKind(self.comparison_kind)
        ProposedPatchConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.do_nothing_remains_valid is not True:
            raise ValueError("do_nothing_remains_valid must remain True")
        if (self.do_nothing_preferred or self.do_nothing_required) and self.patch_metadata_outperforms_do_nothing:
            raise ValueError("preferred or required do-nothing cannot be outperformed by patch metadata")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ProposedPatchEnvelope:
    proposed_patch_envelope_id: str
    version: str
    patch_metadata_input_id: str
    status: RepairPatchMetadataStatus | str
    readiness_level: RepairPatchMetadataReadinessLevel | str
    disposition: ProposedPatchDisposition | str
    file_changes: list[ProposedFileChange]
    proposed_diffs: list[ProposedDiffMetadata]
    proposed_hunks: list[ProposedCodeHunk]
    evidence_map: ProposedChangeEvidenceMap
    rationale: ProposedChangeRationale
    review_requirement: ProposedPatchReviewRequirement
    do_nothing_comparison: ProposedPatchDoNothingComparison
    source_refs: list[RepairPatchMetadataSourceRef]
    envelope_summary: str
    confidence: ProposedPatchConfidenceLevel | str
    ready_for_future_safety_validation_input: bool
    ready_for_future_human_review_packet_input: bool
    source_read_performed_by_v0384: bool
    file_write_performed: bool
    patch_file_written: bool
    file_edit_performed: bool
    patch_applied: bool
    apply_patch_called: bool
    git_apply_called: bool
    tests_run: bool
    repair_executed: bool
    production_certified: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("proposed_patch_envelope_id", "patch_metadata_input_id", "envelope_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairPatchMetadataStatus(self.status)
        RepairPatchMetadataReadinessLevel(self.readiness_level)
        disposition = ProposedPatchDisposition(self.disposition)
        ProposedPatchConfidenceLevel(self.confidence)
        for list_name in ("file_changes", "proposed_diffs", "proposed_hunks", "source_refs"):
            _validate_list(list_name, getattr(self, list_name))
        if not isinstance(self.evidence_map, ProposedChangeEvidenceMap):
            raise TypeError("evidence_map must be ProposedChangeEvidenceMap")
        if not isinstance(self.rationale, ProposedChangeRationale):
            raise TypeError("rationale must be ProposedChangeRationale")
        if not isinstance(self.review_requirement, ProposedPatchReviewRequirement):
            raise TypeError("review_requirement must be ProposedPatchReviewRequirement")
        if not isinstance(self.do_nothing_comparison, ProposedPatchDoNothingComparison):
            raise TypeError("do_nothing_comparison must be ProposedPatchDoNothingComparison")
        if (self.ready_for_future_safety_validation_input or self.ready_for_future_human_review_packet_input) and disposition in (
            ProposedPatchDisposition.BLOCKED,
            ProposedPatchDisposition.DO_NOTHING_PREFERRED,
            ProposedPatchDisposition.NO_PATCH_NEEDED,
            ProposedPatchDisposition.INSUFFICIENT_CONTEXT,
            ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED,
        ):
            raise ValueError("blocked or do-nothing dispositions cannot be ready for future inputs")
        if self.do_nothing_comparison.do_nothing_preferred and disposition not in (
            ProposedPatchDisposition.REVIEW_REQUIRED,
            ProposedPatchDisposition.DO_NOTHING_PREFERRED,
            ProposedPatchDisposition.BLOCKED,
            ProposedPatchDisposition.INSUFFICIENT_CONTEXT,
            ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED,
        ):
            raise ValueError("do-nothing preferred must block or review-gate patch envelope")
        _validate_false(self, UNSAFE_ENVELOPE_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataDecision:
    patch_metadata_decision_id: str
    proposed_patch_envelope_id: str | None
    decision_kind: RepairPatchMetadataDecisionKind | str
    decision_summary: str
    rationale_summary: str
    confidence: ProposedPatchConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_safety_validation_input: bool
    ready_for_future_human_review_packet_input: bool
    source_read_allowed_now: bool
    write_allowed_now: bool
    patch_file_write_allowed_now: bool
    edit_allowed_now: bool
    apply_allowed_now: bool
    apply_patch_allowed_now: bool
    git_apply_allowed_now: bool
    repair_execution_allowed_now: bool
    test_execution_allowed_now: bool
    model_provider_invocation_allowed_now: bool
    external_agent_allowed_now: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("patch_metadata_decision_id", "decision_summary", "rationale_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairPatchMetadataDecisionKind(self.decision_kind)
        ProposedPatchConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_PATCH_DECISION_NOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairPatchMetadataRiskKind | str
    decision_kind: RepairPatchMetadataDecisionKind | str
    blocks_future_safety_validation: bool
    requires_human_review: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairPatchMetadataRiskKind(self.risk_kind)
        RepairPatchMetadataDecisionKind(self.decision_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataValidationReport:
    validation_report_id: str
    version: str
    proposed_patch_envelope_id: str
    findings: list[RepairPatchMetadataValidationFinding]
    validation_summary: str
    metadata_only_proposal_confirmed: bool
    bounded_diff_text_confirmed: bool
    no_file_write_confirmed: bool
    no_patch_file_write_confirmed: bool
    no_edit_confirmed: bool
    no_apply_confirmed: bool
    no_repair_confirmed: bool
    no_tests_confirmed: bool
    do_nothing_comparison_confirmed: bool
    human_review_requirement_confirmed: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "proposed_patch_envelope_id", "validation_summary"):
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
class RepairPatchMetadataReport:
    patch_metadata_report_id: str
    version: str
    proposed_patch_envelope_id: str
    patch_metadata_decision_id: str
    validation_report_id: str
    readiness_level: RepairPatchMetadataReadinessLevel | str
    status: RepairPatchMetadataStatus | str
    report_summary: str
    ready_for_future_safety_validation_input: bool
    ready_for_future_human_review_packet_input: bool
    ready_for_execution: bool
    production_certified: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("patch_metadata_report_id", "proposed_patch_envelope_id", "patch_metadata_decision_id", "validation_report_id", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairPatchMetadataReadinessLevel(self.readiness_level)
        RepairPatchMetadataStatus(self.status)
        if self.ready_for_execution is not False or self.production_certified is not False:
            raise ValueError("patch metadata report is not execution or production readiness")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataRunPreview:
    run_preview_id: str
    version: str
    requested_mode: RepairPatchMetadataMode | str
    preview_summary: str
    will_read_source: bool
    will_write_files: bool
    will_write_patch_files: bool
    will_edit_files: bool
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
        RepairPatchMetadataMode(self.requested_mode)
        for name in self.__dataclass_fields__:
            if name.startswith("will_") and getattr(self, name) is not False:
                raise ValueError(f"{name} must be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_write: bool
    no_patch_file: bool
    no_edit: bool
    no_apply: bool
    no_repair: bool
    no_test: bool
    no_source_read: bool
    no_subprocess: bool
    no_shell: bool
    no_network: bool
    no_model_provider: bool
    no_external_agent: bool
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
class V0384ReadinessReport:
    readiness_report_id: str
    version: str
    proposed_patch_envelope_id: str
    readiness_level: RepairPatchMetadataReadinessLevel | str
    status: RepairPatchMetadataStatus | str
    summary: str
    ready_for_v0385_repair_proposal_safety_validation: bool
    ready_for_v0386_human_review_packet: bool
    ready_for_repair_patch_metadata_generation: bool
    ready_for_proposed_diff_metadata_generation: bool
    ready_for_proposed_code_hunk_metadata_generation: bool
    ready_for_proposed_patch_envelope_metadata_generation: bool
    ready_for_proposed_file_change_metadata: bool
    ready_for_change_rationale_metadata: bool
    ready_for_patch_evidence_map: bool
    ready_for_patch_do_nothing_comparison: bool
    ready_for_patch_review_requirement: bool
    ready_for_future_repair_proposal_safety_validation_input: bool
    ready_for_future_human_review_packet_input: bool
    ready_for_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_live_workspace_read: bool
    ready_for_source_file_write: bool
    ready_for_sandbox_source_write: bool
    ready_for_patch_file_write: bool
    ready_for_file_edit: bool
    ready_for_patch_application: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_repair_execution: bool
    ready_for_sandbox_repair_apply: bool
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
        for name in ("readiness_report_id", "proposed_patch_envelope_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairPatchMetadataReadinessLevel(self.readiness_level)
        RepairPatchMetadataStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, tuple(name for name in UNSAFE_PATCH_METADATA_FLAG_NAMES if hasattr(self, name)))
        _validate_metadata(self.metadata)


def build_repair_patch_metadata_flags(**kwargs: Any) -> RepairPatchMetadataFlagSet:
    safe_defaults = {
        "repair_patch_metadata_layer_constructed": True,
        "proposed_diff_metadata_available": True,
        "proposed_code_hunk_metadata_available": True,
        "proposed_file_change_metadata_available": True,
        "proposed_patch_envelope_metadata_available": True,
        "proposed_change_rationale_available": True,
        "proposed_change_evidence_map_available": True,
        "proposed_patch_do_nothing_comparison_available": True,
        "proposed_patch_review_requirement_available": True,
        **{name: True for name in SAFE_PATCH_METADATA_FLAG_NAMES},
    }
    return RepairPatchMetadataFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_patch_metadata_flags:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_PATCH_METADATA_FLAG_NAMES},
    )


def build_repair_patch_metadata_source_ref(**kwargs: Any) -> RepairPatchMetadataSourceRef:
    source_kind = kwargs.pop("source_kind", RepairPatchMetadataSourceKind.V0383_REPAIR_SCOPE_PLAN)
    return RepairPatchMetadataSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", f"repair_patch_metadata_source_ref:{str(source_kind)}"),
        source_kind=source_kind,
        source_id=kwargs.pop("source_id", "repair_scope_plan:v0.38.3"),
        source_summary=kwargs.pop("source_summary", "patch metadata source reference only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.3 scope plan"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_patch_metadata_policy(**kwargs: Any) -> RepairPatchMetadataPolicy:
    return RepairPatchMetadataPolicy(
        patch_metadata_policy_id=kwargs.pop("patch_metadata_policy_id", "repair_patch_metadata_policy:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [
            RepairPatchMetadataMode.PROPOSED_DIFF_METADATA,
            RepairPatchMetadataMode.PROPOSED_CODE_HUNK_METADATA,
            RepairPatchMetadataMode.PROPOSED_FILE_CHANGE_METADATA,
            RepairPatchMetadataMode.PROPOSED_PATCH_ENVELOPE_METADATA,
            RepairPatchMetadataMode.CHANGE_RATIONALE_METADATA,
            RepairPatchMetadataMode.PATCH_EVIDENCE_MAP,
            RepairPatchMetadataMode.DO_NOTHING_PATCH_COMPARISON,
            RepairPatchMetadataMode.FUTURE_SAFETY_VALIDATION_INPUT,
            RepairPatchMetadataMode.FUTURE_HUMAN_REVIEW_PACKET_INPUT,
        ]),
        allowed_diff_formats=kwargs.pop("allowed_diff_formats", [
            ProposedDiffFormatKind.UNIFIED_DIFF_LIKE_METADATA,
            ProposedDiffFormatKind.STRUCTURED_DIFF_METADATA,
            ProposedDiffFormatKind.TEXT_REPLACEMENT_METADATA,
            ProposedDiffFormatKind.INSERT_METADATA,
            ProposedDiffFormatKind.DELETE_METADATA,
        ]),
        allowed_hunk_kinds=kwargs.pop("allowed_hunk_kinds", [
            ProposedCodeHunkKind.REPLACE_BOUNDED_TEXT,
            ProposedCodeHunkKind.INSERT_BOUNDED_TEXT,
            ProposedCodeHunkKind.REMOVE_BOUNDED_TEXT,
            ProposedCodeHunkKind.IMPORT_PATH_ADJUSTMENT,
            ProposedCodeHunkKind.CONFIG_VALUE_ADJUSTMENT,
            ProposedCodeHunkKind.TEST_EXPECTATION_REVIEW_NOTE,
            ProposedCodeHunkKind.DOCUMENTATION_CLARIFICATION,
        ]),
        allowed_operations=kwargs.pop("allowed_operations", [
            ProposedChangeOperationKind.PROPOSE_REPLACE,
            ProposedChangeOperationKind.PROPOSE_INSERT,
            ProposedChangeOperationKind.PROPOSE_REMOVE,
            ProposedChangeOperationKind.PROPOSE_IMPORT_ADJUSTMENT,
            ProposedChangeOperationKind.PROPOSE_CONFIG_ADJUSTMENT,
            ProposedChangeOperationKind.PROPOSE_TEST_REVIEW,
            ProposedChangeOperationKind.PROPOSE_DOCUMENTATION_UPDATE,
        ]),
        prohibited_risk_kinds=kwargs.pop("prohibited_risk_kinds", [
            RepairPatchMetadataRiskKind.FILE_DELETION_RISK,
            RepairPatchMetadataRiskKind.FILE_RENAME_RISK,
            RepairPatchMetadataRiskKind.BINARY_CHANGE_RISK,
            RepairPatchMetadataRiskKind.PERMISSION_CHANGE_RISK,
            RepairPatchMetadataRiskKind.DEPENDENCY_INSTALL_RISK,
            RepairPatchMetadataRiskKind.NETWORK_CALL_RISK,
            RepairPatchMetadataRiskKind.SUBPROCESS_SHELL_ADDITION_RISK,
            RepairPatchMetadataRiskKind.MODEL_PROVIDER_CALL_RISK,
            RepairPatchMetadataRiskKind.EXTERNAL_AGENT_CALL_RISK,
            RepairPatchMetadataRiskKind.CREDENTIAL_SECRET_READ_RISK,
            RepairPatchMetadataRiskKind.DOMINION_RUNTIME_RISK,
        ]),
        max_file_changes=kwargs.pop("max_file_changes", 4),
        max_hunks=kwargs.pop("max_hunks", 8),
        max_diff_text_chars=kwargs.pop("max_diff_text_chars", 4000),
        max_hunk_text_chars=kwargs.pop("max_hunk_text_chars", 1200),
        max_total_patch_metadata_chars=kwargs.pop("max_total_patch_metadata_chars", 12000),
        require_scope_plan=kwargs.pop("require_scope_plan", True),
        require_change_intent=kwargs.pop("require_change_intent", True),
        require_source_context_snapshot=kwargs.pop("require_source_context_snapshot", True),
        require_evidence_bundle=kwargs.pop("require_evidence_bundle", True),
        require_do_nothing_comparison=kwargs.pop("require_do_nothing_comparison", True),
        require_human_review_requirement=kwargs.pop("require_human_review_requirement", True),
        allow_proposed_diff_metadata=kwargs.pop("allow_proposed_diff_metadata", True),
        allow_proposed_code_hunk_metadata=kwargs.pop("allow_proposed_code_hunk_metadata", True),
        allow_proposed_file_change_metadata=kwargs.pop("allow_proposed_file_change_metadata", True),
        allow_proposed_patch_envelope_metadata=kwargs.pop("allow_proposed_patch_envelope_metadata", True),
        allow_change_rationale_metadata=kwargs.pop("allow_change_rationale_metadata", True),
        allow_patch_evidence_map=kwargs.pop("allow_patch_evidence_map", True),
        allow_future_safety_validation_input=kwargs.pop("allow_future_safety_validation_input", True),
        allow_future_human_review_packet_input=kwargs.pop("allow_future_human_review_packet_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_PATCH_METADATA_POLICY_ALLOW_NAMES},
    )


def default_repair_patch_metadata_policy(**kwargs: Any) -> RepairPatchMetadataPolicy:
    return build_repair_patch_metadata_policy(**kwargs)


def build_repair_patch_metadata_input(**kwargs: Any) -> RepairPatchMetadataInput:
    return RepairPatchMetadataInput(
        patch_metadata_input_id=kwargs.pop("patch_metadata_input_id", "repair_patch_metadata_input:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        primary_change_intent_id=kwargs.pop("primary_change_intent_id", "repair_change_intent:v0.38.3"),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"),
        requested_mode=kwargs.pop("requested_mode", RepairPatchMetadataMode.PROPOSED_PATCH_ENVELOPE_METADATA),
        source_refs=kwargs.pop("source_refs", [build_repair_patch_metadata_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(REQUIRED_PATCH_METADATA_PROHIBITED_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "proposed patch metadata request only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_proposed_change_evidence_map(**kwargs: Any) -> ProposedChangeEvidenceMap:
    return ProposedChangeEvidenceMap(
        change_evidence_map_id=kwargs.pop("change_evidence_map_id", "proposed_change_evidence_map:v0.38.4"),
        evidence_kinds=kwargs.pop("evidence_kinds", [
            ProposedPatchEvidenceKind.SCOPE_PLAN_REF,
            ProposedPatchEvidenceKind.CHANGE_INTENT_REF,
            ProposedPatchEvidenceKind.SOURCE_CONTEXT_SNAPSHOT_REF,
            ProposedPatchEvidenceKind.EVIDENCE_BUNDLE_REF,
        ]),
        supporting_evidence_refs=kwargs.pop("supporting_evidence_refs", ["v0.38.3 scope plan"]),
        contradictory_evidence_refs=kwargs.pop("contradictory_evidence_refs", []),
        missing_evidence_items=kwargs.pop("missing_evidence_items", []),
        scope_plan_refs=kwargs.pop("scope_plan_refs", ["repair_scope_plan:v0.38.3"]),
        source_excerpt_refs=kwargs.pop("source_excerpt_refs", ["repair_source_excerpt:v0.38.2"]),
        map_summary=kwargs.pop("map_summary", "proposed change evidence map metadata only"),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_proposed_change_rationale(**kwargs: Any) -> ProposedChangeRationale:
    return ProposedChangeRationale(
        change_rationale_id=kwargs.pop("change_rationale_id", "proposed_change_rationale:v0.38.4"),
        rationale_summary=kwargs.pop("rationale_summary", "change rationale is review metadata, not proof of correctness"),
        intent_kind=kwargs.pop("intent_kind", "align_implementation_with_test"),
        scope_kind=kwargs.pop("scope_kind", "implementation_scope"),
        evidence_map_id=kwargs.pop("evidence_map_id", "proposed_change_evidence_map:v0.38.4"),
        human_review_required=kwargs.pop("human_review_required", True),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_proposed_code_hunk(**kwargs: Any) -> ProposedCodeHunk:
    original_text, original_truncated = _bounded_text(kwargs.pop("original_text", "return 1"), kwargs.pop("max_original_chars", 1200))
    proposed_text, proposed_truncated = _bounded_text(kwargs.pop("proposed_text", "return expected_value"), kwargs.pop("max_proposed_chars", 1200))
    return ProposedCodeHunk(
        proposed_hunk_id=kwargs.pop("proposed_hunk_id", "proposed_code_hunk:v0.38.4"),
        hunk_kind=kwargs.pop("hunk_kind", ProposedCodeHunkKind.REPLACE_BOUNDED_TEXT),
        operation_kind=kwargs.pop("operation_kind", ProposedChangeOperationKind.PROPOSE_REPLACE),
        target_relative_path=kwargs.pop("target_relative_path", "pkg/module.py"),
        target_excerpt_id=kwargs.pop("target_excerpt_id", "repair_source_excerpt:v0.38.2"),
        original_text=original_text,
        proposed_text=proposed_text,
        hunk_summary=kwargs.pop("hunk_summary", "bounded proposed code hunk metadata only"),
        start_line=kwargs.pop("start_line", None),
        end_line=kwargs.pop("end_line", None),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.2 source excerpt", "v0.38.3 scope plan"]),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        bounded=kwargs.pop("bounded", True),
        redacted=kwargs.pop("redacted", original_truncated or proposed_truncated),
        generated_from_source_context=kwargs.pop("generated_from_source_context", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_HUNK_STATE_NAMES},
    )


def build_proposed_diff_metadata(**kwargs: Any) -> ProposedDiffMetadata:
    hunk_ids = kwargs.pop("hunk_ids", ["proposed_code_hunk:v0.38.4"])
    text = kwargs.pop("proposed_diff_text", "--- proposed/pkg/module.py\n+++ proposed/pkg/module.py\n@@ metadata only @@\n-return 1\n+return expected_value\n")
    bounded_text, truncated = _bounded_text(text, kwargs.pop("max_diff_text_chars", 4000))
    return ProposedDiffMetadata(
        proposed_diff_id=kwargs.pop("proposed_diff_id", "proposed_diff_metadata:v0.38.4"),
        diff_format=kwargs.pop("diff_format", ProposedDiffFormatKind.UNIFIED_DIFF_LIKE_METADATA),
        target_relative_path=kwargs.pop("target_relative_path", "pkg/module.py"),
        proposed_diff_text=bounded_text,
        diff_summary=kwargs.pop("diff_summary", "bounded in-memory proposed diff metadata only"),
        hunk_ids=hunk_ids,
        evidence_map_id=kwargs.pop("evidence_map_id", "proposed_change_evidence_map:v0.38.4"),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        bounded=kwargs.pop("bounded", True),
        redacted=kwargs.pop("redacted", truncated),
        in_memory_only=kwargs.pop("in_memory_only", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_DIFF_STATE_NAMES},
    )


def build_proposed_file_change(**kwargs: Any) -> ProposedFileChange:
    evidence_map = kwargs.pop("evidence_map", build_proposed_change_evidence_map())
    rationale = kwargs.pop("rationale", build_proposed_change_rationale(evidence_map_id=evidence_map.change_evidence_map_id))
    hunks = kwargs.pop("proposed_hunks", [build_proposed_code_hunk(evidence_refs=evidence_map.supporting_evidence_refs)])
    diff = kwargs.pop("proposed_diff", build_proposed_diff_metadata(
        hunk_ids=[hunk.proposed_hunk_id for hunk in hunks],
        evidence_map_id=evidence_map.change_evidence_map_id,
    ))
    return ProposedFileChange(
        proposed_file_change_id=kwargs.pop("proposed_file_change_id", "proposed_file_change:v0.38.4"),
        target_relative_path=kwargs.pop("target_relative_path", hunks[0].target_relative_path if hunks else "pkg/module.py"),
        artifact_kind=kwargs.pop("artifact_kind", ProposedPatchArtifactKind.PROPOSED_FILE_CHANGE),
        disposition=kwargs.pop("disposition", ProposedPatchDisposition.PROPOSED_WITH_WARNINGS),
        operation_kinds=kwargs.pop("operation_kinds", [hunk.operation_kind for hunk in hunks]),
        proposed_hunks=hunks,
        proposed_diff=diff,
        rationale=rationale,
        evidence_map=evidence_map,
        file_change_summary=kwargs.pop("file_change_summary", "proposed file change metadata only"),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_FILE_CHANGE_STATE_NAMES},
    )


def build_proposed_patch_review_requirement(**kwargs: Any) -> ProposedPatchReviewRequirement:
    return ProposedPatchReviewRequirement(
        review_requirement_id=kwargs.pop("review_requirement_id", "proposed_patch_review_requirement:v0.38.4"),
        requirement_kind=kwargs.pop("requirement_kind", ProposedPatchReviewRequirementKind.HUMAN_REVIEW_REQUIRED_BEFORE_ANY_APPLY),
        requirement_summary=kwargs.pop("requirement_summary", "human review is mandatory before any future apply"),
        required_before_safety_validation=kwargs.pop("required_before_safety_validation", True),
        required_before_human_review_packet=kwargs.pop("required_before_human_review_packet", True),
        required_before_any_apply=kwargs.pop("required_before_any_apply", True),
        human_approval_present=kwargs.pop("human_approval_present", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_proposed_patch_do_nothing_comparison(**kwargs: Any) -> ProposedPatchDoNothingComparison:
    return ProposedPatchDoNothingComparison(
        do_nothing_patch_comparison_id=kwargs.pop("do_nothing_patch_comparison_id", "proposed_patch_do_nothing_comparison:v0.38.4"),
        comparison_kind=kwargs.pop("comparison_kind", ProposedPatchDoNothingComparisonKind.PATCH_METADATA_BETTER_THAN_DO_NOTHING),
        comparison_summary=kwargs.pop("comparison_summary", "do-nothing remains valid while patch metadata is reviewable"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.3 do-nothing scope comparison"]),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        do_nothing_preferred=kwargs.pop("do_nothing_preferred", False),
        do_nothing_required=kwargs.pop("do_nothing_required", False),
        patch_metadata_outperforms_do_nothing=kwargs.pop("patch_metadata_outperforms_do_nothing", True),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_proposed_patch_envelope(**kwargs: Any) -> ProposedPatchEnvelope:
    evidence_map = kwargs.pop("evidence_map", build_proposed_change_evidence_map())
    rationale = kwargs.pop("rationale", build_proposed_change_rationale(evidence_map_id=evidence_map.change_evidence_map_id))
    hunks = kwargs.pop("proposed_hunks", [build_proposed_code_hunk(evidence_refs=evidence_map.supporting_evidence_refs)])
    diffs = kwargs.pop("proposed_diffs", [build_proposed_diff_metadata(
        hunk_ids=[hunk.proposed_hunk_id for hunk in hunks],
        evidence_map_id=evidence_map.change_evidence_map_id,
    )])
    changes = kwargs.pop("file_changes", [build_proposed_file_change(
        evidence_map=evidence_map,
        rationale=rationale,
        proposed_hunks=hunks,
        proposed_diff=diffs[0] if diffs else None,
    )])
    do_nothing = kwargs.pop("do_nothing_comparison", build_proposed_patch_do_nothing_comparison())
    disposition = kwargs.pop("disposition", ProposedPatchDisposition.PROPOSED_WITH_WARNINGS)
    ready = kwargs.pop("ready_for_future_safety_validation_input", disposition not in (
        ProposedPatchDisposition.BLOCKED,
        ProposedPatchDisposition.DO_NOTHING_PREFERRED,
        ProposedPatchDisposition.NO_PATCH_NEEDED,
        ProposedPatchDisposition.INSUFFICIENT_CONTEXT,
        ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED,
    ))
    return ProposedPatchEnvelope(
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        patch_metadata_input_id=kwargs.pop("patch_metadata_input_id", "repair_patch_metadata_input:v0.38.4"),
        status=kwargs.pop("status", RepairPatchMetadataStatus.PATCH_ENVELOPE_CREATED_WITH_WARNINGS),
        readiness_level=kwargs.pop("readiness_level", RepairPatchMetadataReadinessLevel.FUTURE_SAFETY_VALIDATION_INPUT_READY if ready else RepairPatchMetadataReadinessLevel.PROPOSED_PATCH_ENVELOPE_METADATA_READY),
        disposition=disposition,
        file_changes=changes,
        proposed_diffs=diffs,
        proposed_hunks=hunks,
        evidence_map=evidence_map,
        rationale=rationale,
        review_requirement=kwargs.pop("review_requirement", build_proposed_patch_review_requirement()),
        do_nothing_comparison=do_nothing,
        source_refs=kwargs.pop("source_refs", [build_repair_patch_metadata_source_ref()]),
        envelope_summary=kwargs.pop("envelope_summary", "proposed patch envelope metadata only"),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        ready_for_future_safety_validation_input=ready,
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", ready),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_ENVELOPE_STATE_NAMES},
    )


def build_repair_patch_metadata_decision(**kwargs: Any) -> RepairPatchMetadataDecision:
    return RepairPatchMetadataDecision(
        patch_metadata_decision_id=kwargs.pop("patch_metadata_decision_id", "repair_patch_metadata_decision:v0.38.4"),
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        decision_kind=kwargs.pop("decision_kind", RepairPatchMetadataDecisionKind.ALLOW_FUTURE_SAFETY_VALIDATION_INPUT),
        decision_summary=kwargs.pop("decision_summary", "future safety validation input is allowed as metadata only"),
        rationale_summary=kwargs.pop("rationale_summary", "decision grants no read, write, apply, test, repair, model, or external-agent permission"),
        confidence=kwargs.pop("confidence", ProposedPatchConfidenceLevel.MEDIUM),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.4 proposed patch envelope"]),
        ready_for_future_safety_validation_input=kwargs.pop("ready_for_future_safety_validation_input", True),
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_PATCH_DECISION_NOW_NAMES},
    )


def build_repair_patch_metadata_input_from_scope_plan(
    scope_plan: Any,
    source_context_snapshot: Any | None = None,
    evidence_bundle: Any | None = None,
    **kwargs: Any,
) -> RepairPatchMetadataInput:
    return build_repair_patch_metadata_input(
        scope_plan_id=kwargs.pop("scope_plan_id", _attr(scope_plan, "scope_plan_id", "repair_scope_plan:v0.38.3")),
        primary_change_intent_id=kwargs.pop("primary_change_intent_id", _attr(scope_plan, "primary_change_intent_id", "repair_change_intent:v0.38.3")),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", _attr(source_context_snapshot, "source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2")),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", _attr(evidence_bundle, "evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1")),
        task_summary=kwargs.pop("task_summary", _attr(scope_plan, "plan_summary", "patch metadata input from scope plan")),
        source_refs=kwargs.pop("source_refs", [
            build_repair_patch_metadata_source_ref(
                source_kind=RepairPatchMetadataSourceKind.V0383_REPAIR_SCOPE_PLAN,
                source_id=_attr(scope_plan, "scope_plan_id", "repair_scope_plan:v0.38.3"),
                source_summary="v0.38.3 scope plan metadata",
            )
        ]),
        **kwargs,
    )


def create_proposed_change_evidence_map_from_scope(
    scope_plan: Any | None,
    source_context_snapshot: Any | None = None,
    evidence_bundle: Any | None = None,
) -> ProposedChangeEvidenceMap:
    supporting: list[str] = []
    missing: list[str] = []
    if scope_plan is None:
        missing.append("scope plan")
    else:
        supporting.append(_attr(scope_plan, "scope_plan_id", "repair_scope_plan:v0.38.3"))
    if source_context_snapshot is None:
        missing.append("source context snapshot")
    else:
        supporting.append(_attr(source_context_snapshot, "source_context_snapshot_id", "repair_source_context_snapshot:v0.38.2"))
    if evidence_bundle is not None:
        supporting.append(_attr(evidence_bundle, "evidence_bundle_id", "repair_proposal_evidence_bundle:v0.38.1"))
    excerpts = [
        str(_attr(excerpt, "source_excerpt_id"))
        for excerpt in (_attr(source_context_snapshot, "source_excerpts", []) or [])
        if _attr(excerpt, "source_excerpt_id")
    ]
    return build_proposed_change_evidence_map(
        supporting_evidence_refs=supporting or ["v0.38.4 patch metadata input"],
        missing_evidence_items=missing,
        scope_plan_refs=[] if scope_plan is None else [_attr(scope_plan, "scope_plan_id", "repair_scope_plan:v0.38.3")],
        source_excerpt_refs=excerpts,
        confidence=ProposedPatchConfidenceLevel.LOW if missing else ProposedPatchConfidenceLevel.MEDIUM,
    )


def create_proposed_change_rationale_from_intent(
    change_intent: Any | None,
    evidence_map: ProposedChangeEvidenceMap,
) -> ProposedChangeRationale:
    return build_proposed_change_rationale(
        intent_kind=str(_attr(change_intent, "intent_kind", "unknown")),
        scope_kind=str(_attr(change_intent, "scope_kind", "unknown_scope")),
        rationale_summary=str(_attr(change_intent, "rationale", "change rationale requires human review and is not proof")),
        evidence_map_id=evidence_map.change_evidence_map_id,
        confidence=evidence_map.confidence,
    )


def _operation_from_intent(change_intent: Any | None) -> tuple[ProposedCodeHunkKind, ProposedChangeOperationKind]:
    text = _text_from_inputs(change_intent)
    if "missing_dependency_without_install" in text or "dependency" in text:
        return ProposedCodeHunkKind.NO_HUNK, ProposedChangeOperationKind.BLOCKED_OPERATION
    if "timeout_without_retry" in text or "timeout" in text:
        return ProposedCodeHunkKind.NO_HUNK, ProposedChangeOperationKind.BLOCKED_OPERATION
    if "import" in text:
        return ProposedCodeHunkKind.IMPORT_PATH_ADJUSTMENT, ProposedChangeOperationKind.PROPOSE_IMPORT_ADJUSTMENT
    if "config" in text:
        return ProposedCodeHunkKind.CONFIG_VALUE_ADJUSTMENT, ProposedChangeOperationKind.PROPOSE_CONFIG_ADJUSTMENT
    if "test_expectation" in text or "test expectation" in text:
        return ProposedCodeHunkKind.TEST_EXPECTATION_REVIEW_NOTE, ProposedChangeOperationKind.PROPOSE_TEST_REVIEW
    if "documentation" in text:
        return ProposedCodeHunkKind.DOCUMENTATION_CLARIFICATION, ProposedChangeOperationKind.PROPOSE_DOCUMENTATION_UPDATE
    return ProposedCodeHunkKind.REPLACE_BOUNDED_TEXT, ProposedChangeOperationKind.PROPOSE_REPLACE


def create_proposed_code_hunks_from_scope_context(
    scope_plan: Any,
    source_context_snapshot: Any,
    policy: RepairPatchMetadataPolicy | None = None,
) -> list[ProposedCodeHunk]:
    policy = policy or default_repair_patch_metadata_policy()
    change_intents = list(_attr(scope_plan, "change_intents", []) or [])
    change_intent = change_intents[0] if change_intents else None
    hunk_kind, operation = _operation_from_intent(change_intent)
    if operation == ProposedChangeOperationKind.BLOCKED_OPERATION:
        return []
    excerpts = list(_attr(source_context_snapshot, "source_excerpts", []) or [])
    hunks: list[ProposedCodeHunk] = []
    for index, excerpt in enumerate(excerpts[: policy.max_hunks], start=1):
        original = str(_attr(excerpt, "excerpt_text", ""))
        if not original:
            continue
        proposed = original
        if operation == ProposedChangeOperationKind.PROPOSE_IMPORT_ADJUSTMENT:
            proposed = original.replace("from .", "from ")
        elif operation == ProposedChangeOperationKind.PROPOSE_TEST_REVIEW:
            proposed = original + "\n# review test expectation before any future change"
        elif operation == ProposedChangeOperationKind.PROPOSE_DOCUMENTATION_UPDATE:
            proposed = original + "\n\nClarification proposed for human review."
        else:
            proposed = original + "\n# proposed metadata-only replacement requires review"
        original, original_truncated = _bounded_text(original, policy.max_hunk_text_chars)
        proposed, proposed_truncated = _bounded_text(proposed, policy.max_hunk_text_chars)
        path = str(_attr(excerpt, "normalized_relative_path", "unknown"))
        hunks.append(build_proposed_code_hunk(
            proposed_hunk_id=f"proposed_code_hunk:{index}:{path}:v0.38.4",
            hunk_kind=hunk_kind,
            operation_kind=operation,
            target_relative_path=path,
            target_excerpt_id=_attr(excerpt, "source_excerpt_id"),
            original_text=original,
            proposed_text=proposed,
            hunk_summary="proposed code hunk metadata generated from supplied source excerpt metadata",
            evidence_refs=[_attr(excerpt, "source_excerpt_id", "v0.38.2 source excerpt"), _attr(scope_plan, "scope_plan_id", "v0.38.3 scope plan")],
            bounded=True,
            redacted=bool(_attr(excerpt, "redacted", False) or original_truncated or proposed_truncated),
        ))
    return hunks


def create_proposed_diff_metadata_from_hunks(
    hunks: list[ProposedCodeHunk],
    evidence_map: ProposedChangeEvidenceMap,
    policy: RepairPatchMetadataPolicy | None = None,
) -> list[ProposedDiffMetadata]:
    policy = policy or default_repair_patch_metadata_policy()
    diffs: list[ProposedDiffMetadata] = []
    for index, hunk in enumerate(hunks, start=1):
        diff_text = (
            f"--- proposed/{hunk.target_relative_path}\n"
            f"+++ proposed/{hunk.target_relative_path}\n"
            "@@ metadata only @@\n"
            f"-{hunk.original_text}\n"
            f"+{hunk.proposed_text}\n"
        )
        bounded, truncated = _bounded_text(diff_text, policy.max_diff_text_chars)
        diffs.append(build_proposed_diff_metadata(
            proposed_diff_id=f"proposed_diff_metadata:{index}:{hunk.target_relative_path}:v0.38.4",
            target_relative_path=hunk.target_relative_path,
            proposed_diff_text=bounded,
            hunk_ids=[hunk.proposed_hunk_id],
            evidence_map_id=evidence_map.change_evidence_map_id,
            redacted=hunk.redacted or truncated,
            confidence=hunk.confidence,
        ))
    return diffs


def create_proposed_file_changes(
    hunks: list[ProposedCodeHunk],
    diffs: list[ProposedDiffMetadata],
    evidence_map: ProposedChangeEvidenceMap,
    rationale: ProposedChangeRationale,
) -> list[ProposedFileChange]:
    changes: list[ProposedFileChange] = []
    for index, hunk in enumerate(hunks, start=1):
        diff = next((item for item in diffs if hunk.proposed_hunk_id in item.hunk_ids), None)
        changes.append(build_proposed_file_change(
            proposed_file_change_id=f"proposed_file_change:{index}:{hunk.target_relative_path}:v0.38.4",
            target_relative_path=hunk.target_relative_path,
            operation_kinds=[hunk.operation_kind],
            proposed_hunks=[hunk],
            proposed_diff=diff,
            rationale=rationale,
            evidence_map=evidence_map,
        ))
    return changes


def compare_proposed_patch_to_do_nothing(
    evidence_map: ProposedChangeEvidenceMap,
    risks: list[RepairPatchMetadataRiskKind] | None = None,
) -> ProposedPatchDoNothingComparison:
    risk_items = risks or []
    if evidence_map.missing_evidence_items:
        return build_proposed_patch_do_nothing_comparison(
            comparison_kind=ProposedPatchDoNothingComparisonKind.DO_NOTHING_REQUIRED_DUE_TO_INSUFFICIENT_CONTEXT,
            comparison_summary="do-nothing is required because patch metadata lacks required context",
            evidence_refs=evidence_map.supporting_evidence_refs,
            do_nothing_preferred=True,
            do_nothing_required=True,
            patch_metadata_outperforms_do_nothing=False,
            confidence=ProposedPatchConfidenceLevel.MEDIUM,
        )
    if risk_items:
        return build_proposed_patch_do_nothing_comparison(
            comparison_kind=ProposedPatchDoNothingComparisonKind.DO_NOTHING_REQUIRED_DUE_TO_HIGH_RISK,
            comparison_summary="do-nothing is required because unsafe patch metadata risk is present",
            evidence_refs=evidence_map.supporting_evidence_refs,
            do_nothing_preferred=True,
            do_nothing_required=True,
            patch_metadata_outperforms_do_nothing=False,
            confidence=ProposedPatchConfidenceLevel.MEDIUM,
        )
    return build_proposed_patch_do_nothing_comparison(evidence_refs=evidence_map.supporting_evidence_refs)


def create_proposed_patch_review_requirement(
    risks: list[RepairPatchMetadataRiskKind] | None = None,
    low_confidence: bool = False,
) -> ProposedPatchReviewRequirement:
    if risks:
        return build_proposed_patch_review_requirement(
            requirement_kind=ProposedPatchReviewRequirementKind.HUMAN_REVIEW_REQUIRED_DUE_TO_RISK,
            requirement_summary="human review is required because proposed patch metadata has risk",
        )
    if low_confidence:
        return build_proposed_patch_review_requirement(
            requirement_kind=ProposedPatchReviewRequirementKind.HUMAN_REVIEW_REQUIRED_DUE_TO_LOW_CONFIDENCE,
            requirement_summary="human review is required because proposed patch metadata confidence is low",
        )
    return build_proposed_patch_review_requirement()


def create_proposed_patch_envelope(
    patch_input: RepairPatchMetadataInput,
    scope_plan: Any | None,
    source_context_snapshot: Any | None,
    evidence_bundle: Any | None = None,
    policy: RepairPatchMetadataPolicy | None = None,
) -> ProposedPatchEnvelope:
    policy = policy or default_repair_patch_metadata_policy()
    evidence_map = create_proposed_change_evidence_map_from_scope(scope_plan, source_context_snapshot, evidence_bundle)
    change_intents = list(_attr(scope_plan, "change_intents", []) or [])
    change_intent = change_intents[0] if change_intents else None
    rationale = create_proposed_change_rationale_from_intent(change_intent, evidence_map)
    text = _text_from_inputs(patch_input, scope_plan, change_intent, source_context_snapshot)
    risks = _detect_unsafe_tokens(text)
    if any(risk in policy.prohibited_risk_kinds for risk in risks):
        hunks: list[ProposedCodeHunk] = []
    else:
        hunks = create_proposed_code_hunks_from_scope_context(scope_plan, source_context_snapshot, policy) if scope_plan and source_context_snapshot else []
    diffs = create_proposed_diff_metadata_from_hunks(hunks, evidence_map, policy)
    changes = create_proposed_file_changes(hunks, diffs, evidence_map, rationale)
    do_nothing = compare_proposed_patch_to_do_nothing(evidence_map, risks)
    review = create_proposed_patch_review_requirement(risks, evidence_map.confidence in (ProposedPatchConfidenceLevel.LOW, ProposedPatchConfidenceLevel.INCONCLUSIVE, ProposedPatchConfidenceLevel.UNKNOWN))
    blocked = bool(evidence_map.missing_evidence_items or risks or do_nothing.do_nothing_required)
    disposition = ProposedPatchDisposition.PROPOSED_WITH_WARNINGS
    if evidence_map.missing_evidence_items:
        disposition = ProposedPatchDisposition.INSUFFICIENT_CONTEXT
    elif risks:
        disposition = ProposedPatchDisposition.UNSAFE_OPERATION_BLOCKED
    elif do_nothing.do_nothing_preferred:
        disposition = ProposedPatchDisposition.REVIEW_REQUIRED
    ready = not blocked
    return build_proposed_patch_envelope(
        patch_metadata_input_id=patch_input.patch_metadata_input_id,
        disposition=disposition,
        status=RepairPatchMetadataStatus.PATCH_ENVELOPE_CREATED_WITH_WARNINGS if ready else RepairPatchMetadataStatus.REVIEW_REQUIRED,
        readiness_level=RepairPatchMetadataReadinessLevel.FUTURE_SAFETY_VALIDATION_INPUT_READY if ready else RepairPatchMetadataReadinessLevel.PROPOSED_PATCH_ENVELOPE_METADATA_READY,
        file_changes=changes,
        proposed_diffs=diffs,
        proposed_hunks=hunks,
        evidence_map=evidence_map,
        rationale=rationale,
        review_requirement=review,
        do_nothing_comparison=do_nothing,
        source_refs=patch_input.source_refs,
        ready_for_future_safety_validation_input=ready,
        ready_for_future_human_review_packet_input=ready,
        confidence=evidence_map.confidence,
    )


def decide_repair_patch_metadata(envelope: ProposedPatchEnvelope) -> RepairPatchMetadataDecision:
    if envelope.do_nothing_comparison.do_nothing_preferred or envelope.disposition in (
        ProposedPatchDisposition.DO_NOTHING_PREFERRED,
        ProposedPatchDisposition.NO_PATCH_NEEDED,
    ):
        return build_repair_patch_metadata_decision(
            proposed_patch_envelope_id=envelope.proposed_patch_envelope_id,
            decision_kind=RepairPatchMetadataDecisionKind.CHOOSE_DO_NOTHING,
            decision_summary="do-nothing is preferred for this proposed patch metadata",
            rationale_summary="do-nothing comparison blocks or review-gates future safety input",
            ready_for_future_safety_validation_input=False,
            ready_for_future_human_review_packet_input=False,
            confidence=ProposedPatchConfidenceLevel.LOW,
            evidence_refs=[envelope.proposed_patch_envelope_id],
        )
    if envelope.ready_for_future_safety_validation_input:
        return build_repair_patch_metadata_decision(
            proposed_patch_envelope_id=envelope.proposed_patch_envelope_id,
            evidence_refs=[envelope.proposed_patch_envelope_id],
        )
    return build_repair_patch_metadata_decision(
        proposed_patch_envelope_id=envelope.proposed_patch_envelope_id,
        decision_kind=RepairPatchMetadataDecisionKind.REQUIRE_REVIEW,
        decision_summary="proposed patch metadata requires human review",
        rationale_summary="future safety or human review packet input is not yet sufficiently supported",
        ready_for_future_safety_validation_input=False,
        ready_for_future_human_review_packet_input=False,
        confidence=ProposedPatchConfidenceLevel.LOW,
        evidence_refs=[envelope.proposed_patch_envelope_id],
    )


def build_repair_patch_metadata_validation_finding(**kwargs: Any) -> RepairPatchMetadataValidationFinding:
    return RepairPatchMetadataValidationFinding(
        finding_id=kwargs.pop("finding_id", "repair_patch_metadata_validation_finding:v0.38.4"),
        finding_summary=kwargs.pop("finding_summary", "proposed patch metadata preserves no apply or repair permission"),
        risk_kind=kwargs.pop("risk_kind", RepairPatchMetadataRiskKind.APPLIED_PATCH_CONFUSION_RISK),
        decision_kind=kwargs.pop("decision_kind", RepairPatchMetadataDecisionKind.ALLOW_PROPOSED_PATCH_ENVELOPE_METADATA),
        blocks_future_safety_validation=kwargs.pop("blocks_future_safety_validation", False),
        requires_human_review=kwargs.pop("requires_human_review", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.4 patch metadata validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_patch_metadata_validation_report(**kwargs: Any) -> RepairPatchMetadataValidationReport:
    return RepairPatchMetadataValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "repair_patch_metadata_validation_report:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        findings=kwargs.pop("findings", [build_repair_patch_metadata_validation_finding()]),
        validation_summary=kwargs.pop("validation_summary", "patch metadata validation confirms no apply, no write, no repair"),
        metadata_only_proposal_confirmed=kwargs.pop("metadata_only_proposal_confirmed", True),
        bounded_diff_text_confirmed=kwargs.pop("bounded_diff_text_confirmed", True),
        no_file_write_confirmed=kwargs.pop("no_file_write_confirmed", True),
        no_patch_file_write_confirmed=kwargs.pop("no_patch_file_write_confirmed", True),
        no_edit_confirmed=kwargs.pop("no_edit_confirmed", True),
        no_apply_confirmed=kwargs.pop("no_apply_confirmed", True),
        no_repair_confirmed=kwargs.pop("no_repair_confirmed", True),
        no_tests_confirmed=kwargs.pop("no_tests_confirmed", True),
        do_nothing_comparison_confirmed=kwargs.pop("do_nothing_comparison_confirmed", True),
        human_review_requirement_confirmed=kwargs.pop("human_review_requirement_confirmed", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def validate_proposed_patch_envelope(envelope: ProposedPatchEnvelope) -> RepairPatchMetadataValidationReport:
    return build_repair_patch_metadata_validation_report(proposed_patch_envelope_id=envelope.proposed_patch_envelope_id)


def build_repair_patch_metadata_report(**kwargs: Any) -> RepairPatchMetadataReport:
    envelope = kwargs.pop("envelope", None)
    decision = kwargs.pop("decision", None)
    validation_report = kwargs.pop("validation_report", None)
    ready = kwargs.pop("ready_for_future_safety_validation_input", envelope.ready_for_future_safety_validation_input if envelope else True)
    return RepairPatchMetadataReport(
        patch_metadata_report_id=kwargs.pop("patch_metadata_report_id", "repair_patch_metadata_report:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", envelope.proposed_patch_envelope_id if envelope else "proposed_patch_envelope:v0.38.4"),
        patch_metadata_decision_id=kwargs.pop("patch_metadata_decision_id", decision.patch_metadata_decision_id if decision else "repair_patch_metadata_decision:v0.38.4"),
        validation_report_id=kwargs.pop("validation_report_id", validation_report.validation_report_id if validation_report else "repair_patch_metadata_validation_report:v0.38.4"),
        readiness_level=kwargs.pop("readiness_level", RepairPatchMetadataReadinessLevel.FUTURE_SAFETY_VALIDATION_INPUT_READY if ready else RepairPatchMetadataReadinessLevel.PROPOSED_PATCH_ENVELOPE_METADATA_READY),
        status=kwargs.pop("status", RepairPatchMetadataStatus.READY_FOR_FUTURE_SAFETY_VALIDATION if ready else RepairPatchMetadataStatus.REVIEW_REQUIRED),
        report_summary=kwargs.pop("report_summary", "repair patch metadata report metadata only"),
        ready_for_future_safety_validation_input=ready,
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", envelope.ready_for_future_human_review_packet_input if envelope else True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        production_certified=kwargs.pop("production_certified", False),
        evidence_refs=kwargs.pop("evidence_refs", [envelope.proposed_patch_envelope_id if envelope else "v0.38.4 proposed patch envelope"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_patch_metadata_run_preview(**kwargs: Any) -> RepairPatchMetadataRunPreview:
    return RepairPatchMetadataRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "repair_patch_metadata_run_preview:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        requested_mode=kwargs.pop("requested_mode", RepairPatchMetadataMode.PROPOSED_PATCH_ENVELOPE_METADATA),
        preview_summary=kwargs.pop("preview_summary", "patch metadata preview creates in-memory metadata only"),
        will_read_source=kwargs.pop("will_read_source", False),
        will_write_files=kwargs.pop("will_write_files", False),
        will_write_patch_files=kwargs.pop("will_write_patch_files", False),
        will_edit_files=kwargs.pop("will_edit_files", False),
        will_apply_patch=kwargs.pop("will_apply_patch", False),
        will_execute_repair=kwargs.pop("will_execute_repair", False),
        will_run_tests=kwargs.pop("will_run_tests", False),
        will_invoke_model_provider=kwargs.pop("will_invoke_model_provider", False),
        will_invoke_external_agent=kwargs.pop("will_invoke_external_agent", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_patch_metadata_no_apply_guarantee(**kwargs: Any) -> RepairPatchMetadataNoApplyGuarantee:
    return RepairPatchMetadataNoApplyGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_patch_metadata_no_apply_guarantee:v0.38.4"),
        version=kwargs.pop("version", V0384_VERSION),
        no_write=kwargs.pop("no_write", True),
        no_patch_file=kwargs.pop("no_patch_file", True),
        no_edit=kwargs.pop("no_edit", True),
        no_apply=kwargs.pop("no_apply", True),
        no_repair=kwargs.pop("no_repair", True),
        no_test=kwargs.pop("no_test", True),
        no_source_read=kwargs.pop("no_source_read", True),
        no_subprocess=kwargs.pop("no_subprocess", True),
        no_shell=kwargs.pop("no_shell", True),
        no_network=kwargs.pop("no_network", True),
        no_model_provider=kwargs.pop("no_model_provider", True),
        no_external_agent=kwargs.pop("no_external_agent", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        guarantee_summary=kwargs.pop("guarantee_summary", "v0.38.4 creates metadata only and applies nothing"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v0384_readiness_report(**kwargs: Any) -> V0384ReadinessReport:
    return V0384ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0384_readiness_report"),
        version=kwargs.pop("version", V0384_VERSION),
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        readiness_level=kwargs.pop("readiness_level", RepairPatchMetadataReadinessLevel.FUTURE_SAFETY_VALIDATION_INPUT_READY),
        status=kwargs.pop("status", RepairPatchMetadataStatus.READY_FOR_FUTURE_SAFETY_VALIDATION),
        summary=kwargs.pop("summary", "v0.38.4 is ready for design-stage safety validation and human review packet input only"),
        ready_for_v0385_repair_proposal_safety_validation=kwargs.pop("ready_for_v0385_repair_proposal_safety_validation", True),
        ready_for_v0386_human_review_packet=kwargs.pop("ready_for_v0386_human_review_packet", True),
        ready_for_repair_patch_metadata_generation=kwargs.pop("ready_for_repair_patch_metadata_generation", True),
        ready_for_proposed_diff_metadata_generation=kwargs.pop("ready_for_proposed_diff_metadata_generation", True),
        ready_for_proposed_code_hunk_metadata_generation=kwargs.pop("ready_for_proposed_code_hunk_metadata_generation", True),
        ready_for_proposed_patch_envelope_metadata_generation=kwargs.pop("ready_for_proposed_patch_envelope_metadata_generation", True),
        ready_for_proposed_file_change_metadata=kwargs.pop("ready_for_proposed_file_change_metadata", True),
        ready_for_change_rationale_metadata=kwargs.pop("ready_for_change_rationale_metadata", True),
        ready_for_patch_evidence_map=kwargs.pop("ready_for_patch_evidence_map", True),
        ready_for_patch_do_nothing_comparison=kwargs.pop("ready_for_patch_do_nothing_comparison", True),
        ready_for_patch_review_requirement=kwargs.pop("ready_for_patch_review_requirement", True),
        ready_for_future_repair_proposal_safety_validation_input=kwargs.pop("ready_for_future_repair_proposal_safety_validation_input", True),
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.4 proposed patch envelope"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_PATCH_METADATA_FLAG_NAMES if name in V0384ReadinessReport.__dataclass_fields__},
    )


def repair_patch_metadata_flags_preserve_no_apply(flags: RepairPatchMetadataFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_METADATA_FLAG_NAMES)


def repair_patch_metadata_policy_blocks_apply_and_repair(policy: RepairPatchMetadataPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_PATCH_METADATA_POLICY_ALLOW_NAMES)


def proposed_code_hunk_is_not_edit(hunk: ProposedCodeHunk) -> bool:
    return all(getattr(hunk, name) is False for name in UNSAFE_HUNK_STATE_NAMES)


def proposed_diff_metadata_is_not_applied_diff(diff: ProposedDiffMetadata) -> bool:
    return diff.in_memory_only is True and all(getattr(diff, name) is False for name in UNSAFE_DIFF_STATE_NAMES)


def proposed_patch_envelope_is_not_patch_application(envelope: ProposedPatchEnvelope) -> bool:
    return all(getattr(envelope, name) is False for name in UNSAFE_ENVELOPE_STATE_NAMES)


def repair_patch_metadata_decision_is_not_apply_permission(decision: RepairPatchMetadataDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_PATCH_DECISION_NOW_NAMES)


def v0384_readiness_report_is_not_execution_ready(report: V0384ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_PATCH_METADATA_FLAG_NAMES if hasattr(report, name))
