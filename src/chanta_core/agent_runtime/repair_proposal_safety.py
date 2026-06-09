from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .repair_patch_metadata import ProposedPatchArtifactKind


V0385_VERSION = "v0.38.5"
V0385_RELEASE_NAME = "v0.38.5 Repair Proposal Safety & Static Validation"

SAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES = (
    "ready_for_v0386_human_review_packet",
    "ready_for_v0387_bounded_repair_proposal_loop_trial",
    "ready_for_repair_proposal_safety_validation",
    "ready_for_static_patch_metadata_validation",
    "ready_for_patch_target_validation",
    "ready_for_patch_content_validation",
    "ready_for_boundary_violation_scan",
    "ready_for_unsafe_operation_detection",
    "ready_for_repair_safety_risk_assessment",
    "ready_for_repair_safety_do_nothing_comparison",
    "ready_for_repair_safety_decision",
    "ready_for_future_human_review_packet_input",
    "ready_for_future_bounded_repair_proposal_loop_trial_input",
)

UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES = (
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

UNSAFE_REPAIR_PROPOSAL_SAFETY_POLICY_ALLOW_NAMES = (
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
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_TARGET_VALIDATION_STATE_NAMES = (
    "source_read_performed",
    "write_allowed",
    "apply_allowed",
    "repair_execution_allowed",
)

UNSAFE_SAFETY_DECISION_NOW_NAMES = (
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
    "production_certified",
)

UNSAFE_SAFETY_REPORT_STATE_NAMES = (
    "source_read_performed_by_v0385",
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

REQUIRED_REPAIR_PROPOSAL_SAFETY_PROHIBITED_ACTIONS = (
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

CRITICAL_RISK_KINDS = (
    "absolute_path_target_risk",
    "parent_traversal_target_risk",
    "reference_target_risk",
    "secret_target_risk",
    "dependency_install_risk",
    "package_manager_risk",
    "network_call_risk",
    "subprocess_shell_risk",
    "eval_exec_risk",
    "dynamic_import_risk",
    "file_write_risk",
    "patch_apply_call_risk",
    "git_apply_call_risk",
    "model_provider_call_risk",
    "external_agent_call_risk",
    "credential_secret_read_risk",
    "dominion_runtime_risk",
    "automatic_repair_risk",
    "retry_loop_risk",
    "multi_cycle_loop_risk",
)


class RepairProposalSafetyMode(StrEnum):
    STATIC_VALIDATION = "static_validation"
    TARGET_VALIDATION = "target_validation"
    CONTENT_VALIDATION = "content_validation"
    BOUNDARY_VIOLATION_SCAN = "boundary_violation_scan"
    UNSAFE_OPERATION_DETECTION = "unsafe_operation_detection"
    SAFETY_RISK_ASSESSMENT = "safety_risk_assessment"
    DO_NOTHING_SAFETY_COMPARISON = "do_nothing_safety_comparison"
    FUTURE_HUMAN_REVIEW_PACKET_INPUT = "future_human_review_packet_input"
    FUTURE_LOOP_TRIAL_INPUT = "future_loop_trial_input"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairProposalSafetySourceKind(StrEnum):
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0384_PROPOSED_DIFF_METADATA = "v0384_proposed_diff_metadata"
    V0384_PROPOSED_CODE_HUNK = "v0384_proposed_code_hunk"
    V0384_PROPOSED_FILE_CHANGE = "v0384_proposed_file_change"
    V0384_PROPOSED_CHANGE_RATIONALE = "v0384_proposed_change_rationale"
    V0384_PROPOSED_CHANGE_EVIDENCE_MAP = "v0384_proposed_change_evidence_map"
    V0383_REPAIR_SCOPE_PLAN = "v0383_repair_scope_plan"
    V0383_REPAIR_CHANGE_INTENT = "v0383_repair_change_intent"
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairProposalSafetyStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INPUT_VALIDATED = "input_validated"
    VALIDATION_COMPLETED = "validation_completed"
    VALIDATION_COMPLETED_WITH_WARNINGS = "validation_completed_with_warnings"
    VALIDATION_BLOCKED = "validation_blocked"
    UNSAFE_OPERATION_DETECTED = "unsafe_operation_detected"
    BOUNDARY_VIOLATION_DETECTED = "boundary_violation_detected"
    READY_FOR_FUTURE_HUMAN_REVIEW_PACKET = "ready_for_future_human_review_packet"
    READY_FOR_FUTURE_LOOP_TRIAL = "ready_for_future_loop_trial"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairProposalSafetyReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    SAFETY_CONTRACT_READY = "safety_contract_ready"
    TARGET_VALIDATION_READY = "target_validation_ready"
    CONTENT_VALIDATION_READY = "content_validation_ready"
    BOUNDARY_VIOLATION_SCAN_READY = "boundary_violation_scan_ready"
    UNSAFE_OPERATION_DETECTION_READY = "unsafe_operation_detection_ready"
    SAFETY_RISK_ASSESSMENT_READY = "safety_risk_assessment_ready"
    DO_NOTHING_SAFETY_COMPARISON_READY = "do_nothing_safety_comparison_ready"
    FUTURE_HUMAN_REVIEW_PACKET_INPUT_READY = "future_human_review_packet_input_ready"
    FUTURE_LOOP_TRIAL_INPUT_READY = "future_loop_trial_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0386 = "design_handoff_ready_for_v0386"
    DESIGN_HANDOFF_READY_FOR_V0387 = "design_handoff_ready_for_v0387"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairProposalSafetyDecisionKind(StrEnum):
    ALLOW_STATIC_VALIDATION = "allow_static_validation"
    ALLOW_TARGET_VALIDATION = "allow_target_validation"
    ALLOW_CONTENT_VALIDATION = "allow_content_validation"
    ALLOW_BOUNDARY_VIOLATION_SCAN = "allow_boundary_violation_scan"
    ALLOW_UNSAFE_OPERATION_DETECTION = "allow_unsafe_operation_detection"
    ALLOW_SAFETY_RISK_ASSESSMENT = "allow_safety_risk_assessment"
    ALLOW_DO_NOTHING_SAFETY_COMPARISON = "allow_do_nothing_safety_comparison"
    ALLOW_FUTURE_HUMAN_REVIEW_PACKET_INPUT = "allow_future_human_review_packet_input"
    ALLOW_FUTURE_LOOP_TRIAL_INPUT = "allow_future_loop_trial_input"
    CHOOSE_DO_NOTHING = "choose_do_nothing"
    CHOOSE_HUMAN_REVIEW = "choose_human_review"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    UNSAFE_OPERATION_BLOCKED = "unsafe_operation_blocked"
    BOUNDARY_VIOLATION_BLOCKED = "boundary_violation_blocked"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairProposalSafetyRiskKind(StrEnum):
    MISSING_PATCH_ENVELOPE_RISK = "missing_patch_envelope_risk"
    MISSING_DIFF_METADATA_RISK = "missing_diff_metadata_risk"
    MISSING_HUNK_METADATA_RISK = "missing_hunk_metadata_risk"
    MISSING_SCOPE_PLAN_RISK = "missing_scope_plan_risk"
    MISSING_EVIDENCE_MAP_RISK = "missing_evidence_map_risk"
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    OVERBROAD_PATCH_RISK = "overbroad_patch_risk"
    WRONG_TARGET_PATH_RISK = "wrong_target_path_risk"
    ABSOLUTE_PATH_TARGET_RISK = "absolute_path_target_risk"
    PARENT_TRAVERSAL_TARGET_RISK = "parent_traversal_target_risk"
    REFERENCE_TARGET_RISK = "reference_target_risk"
    SECRET_TARGET_RISK = "secret_target_risk"
    FILE_DELETION_RISK = "file_deletion_risk"
    FILE_RENAME_RISK = "file_rename_risk"
    PERMISSION_CHANGE_RISK = "permission_change_risk"
    BINARY_CHANGE_RISK = "binary_change_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    PACKAGE_MANAGER_RISK = "package_manager_risk"
    NETWORK_CALL_RISK = "network_call_risk"
    SUBPROCESS_SHELL_RISK = "subprocess_shell_risk"
    EVAL_EXEC_RISK = "eval_exec_risk"
    DYNAMIC_IMPORT_RISK = "dynamic_import_risk"
    FILE_WRITE_RISK = "file_write_risk"
    PATCH_APPLY_CALL_RISK = "patch_apply_call_risk"
    GIT_APPLY_CALL_RISK = "git_apply_call_risk"
    MODEL_PROVIDER_CALL_RISK = "model_provider_call_risk"
    EXTERNAL_AGENT_CALL_RISK = "external_agent_call_risk"
    CREDENTIAL_SECRET_READ_RISK = "credential_secret_read_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    HUMAN_REVIEW_OMISSION_RISK = "human_review_omission_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairProposalStaticRuleKind(StrEnum):
    REQUIRE_PATCH_ENVELOPE = "require_patch_envelope"
    REQUIRE_SCOPE_PLAN = "require_scope_plan"
    REQUIRE_EVIDENCE_MAP = "require_evidence_map"
    REQUIRE_DO_NOTHING_COMPARISON = "require_do_nothing_comparison"
    REQUIRE_HUMAN_REVIEW_REQUIREMENT = "require_human_review_requirement"
    PROHIBIT_ABSOLUTE_TARGET_PATH = "prohibit_absolute_target_path"
    PROHIBIT_PARENT_TRAVERSAL_TARGET = "prohibit_parent_traversal_target"
    PROHIBIT_REFERENCE_TARGET = "prohibit_reference_target"
    PROHIBIT_SECRET_TARGET = "prohibit_secret_target"
    PROHIBIT_FILE_DELETE = "prohibit_file_delete"
    PROHIBIT_FILE_RENAME = "prohibit_file_rename"
    PROHIBIT_PERMISSION_CHANGE = "prohibit_permission_change"
    PROHIBIT_BINARY_CHANGE = "prohibit_binary_change"
    PROHIBIT_DEPENDENCY_INSTALL = "prohibit_dependency_install"
    PROHIBIT_PACKAGE_MANAGER_COMMAND = "prohibit_package_manager_command"
    PROHIBIT_NETWORK_CALL = "prohibit_network_call"
    PROHIBIT_SUBPROCESS_SHELL = "prohibit_subprocess_shell"
    PROHIBIT_EVAL_EXEC = "prohibit_eval_exec"
    PROHIBIT_DYNAMIC_IMPORT = "prohibit_dynamic_import"
    PROHIBIT_FILE_WRITE = "prohibit_file_write"
    PROHIBIT_PATCH_APPLY_CALL = "prohibit_patch_apply_call"
    PROHIBIT_GIT_APPLY_CALL = "prohibit_git_apply_call"
    PROHIBIT_MODEL_PROVIDER_CALL = "prohibit_model_provider_call"
    PROHIBIT_EXTERNAL_AGENT_CALL = "prohibit_external_agent_call"
    PROHIBIT_CREDENTIAL_SECRET_READ = "prohibit_credential_secret_read"
    PROHIBIT_DOMINION_RUNTIME = "prohibit_dominion_runtime"
    PROHIBIT_AUTO_REPAIR_LOOP = "prohibit_auto_repair_loop"
    PROHIBIT_RETRY_LOOP = "prohibit_retry_loop"
    PROHIBIT_MULTI_CYCLE_LOOP = "prohibit_multi_cycle_loop"
    UNKNOWN = "unknown"


class RepairProposalStaticCheckKind(StrEnum):
    METADATA_PRESENCE_CHECK = "metadata_presence_check"
    TARGET_PATH_CHECK = "target_path_check"
    PROPOSED_TEXT_PATTERN_CHECK = "proposed_text_pattern_check"
    OPERATION_KIND_CHECK = "operation_kind_check"
    EVIDENCE_MAPPING_CHECK = "evidence_mapping_check"
    DO_NOTHING_CHECK = "do_nothing_check"
    HUMAN_REVIEW_CHECK = "human_review_check"
    BOUNDARY_CHECK = "boundary_check"
    RISK_CHECK = "risk_check"
    UNKNOWN = "unknown"


class RepairProposalBoundaryViolationKind(StrEnum):
    NO_VIOLATION = "no_violation"
    MISSING_REQUIRED_METADATA = "missing_required_metadata"
    ABSOLUTE_TARGET_PATH = "absolute_target_path"
    PARENT_TRAVERSAL_TARGET = "parent_traversal_target"
    REFERENCE_TARGET = "reference_target"
    SECRET_TARGET = "secret_target"
    UNSAFE_OPERATION = "unsafe_operation"
    UNSAFE_DEPENDENCY_INSTALL = "unsafe_dependency_install"
    UNSAFE_NETWORK_CALL = "unsafe_network_call"
    UNSAFE_SUBPROCESS_SHELL = "unsafe_subprocess_shell"
    UNSAFE_MODEL_PROVIDER_CALL = "unsafe_model_provider_call"
    UNSAFE_EXTERNAL_AGENT_CALL = "unsafe_external_agent_call"
    UNSAFE_DOMINION_RUNTIME = "unsafe_dominion_runtime"
    UNSAFE_PATCH_APPLY_CALL = "unsafe_patch_apply_call"
    UNSAFE_FILE_WRITE = "unsafe_file_write"
    MISSING_DO_NOTHING_COMPARISON = "missing_do_nothing_comparison"
    MISSING_HUMAN_REVIEW_REQUIREMENT = "missing_human_review_requirement"
    PRODUCTION_CERTIFICATION_OVERCLAIM = "production_certification_overclaim"
    UNKNOWN = "unknown"


class RepairProposalUnsafeOperationKind(StrEnum):
    NO_UNSAFE_OPERATION = "no_unsafe_operation"
    DEPENDENCY_INSTALL = "dependency_install"
    PACKAGE_MANAGER_COMMAND = "package_manager_command"
    NETWORK_CALL = "network_call"
    SUBPROCESS_SHELL = "subprocess_shell"
    EVAL_EXEC = "eval_exec"
    DYNAMIC_IMPORT = "dynamic_import"
    FILE_WRITE = "file_write"
    PATCH_APPLY = "patch_apply"
    GIT_APPLY = "git_apply"
    MODEL_PROVIDER_CALL = "model_provider_call"
    EXTERNAL_AGENT_CALL = "external_agent_call"
    CREDENTIAL_SECRET_READ = "credential_secret_read"
    DOMINION_RUNTIME = "dominion_runtime"
    AUTOMATIC_REPAIR_LOOP = "automatic_repair_loop"
    RETRY_LOOP = "retry_loop"
    MULTI_CYCLE_LOOP = "multi_cycle_loop"
    FILE_DELETE = "file_delete"
    FILE_RENAME = "file_rename"
    PERMISSION_CHANGE = "permission_change"
    BINARY_CHANGE = "binary_change"
    UNKNOWN = "unknown"


class RepairProposalSafetySeverity(StrEnum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class RepairProposalSafetyConfidenceLevel(StrEnum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairProposalSafetyDisposition(StrEnum):
    SAFETY_PASS = "safety_pass"
    SAFETY_PASS_WITH_WARNINGS = "safety_pass_with_warnings"
    REVIEW_REQUIRED = "review_required"
    BLOCKED = "blocked"
    DO_NOTHING_PREFERRED = "do_nothing_preferred"
    NO_OP = "no_op"
    INCONCLUSIVE = "inconclusive"
    UNKNOWN = "unknown"


class RepairProposalSafetyDoNothingComparisonKind(StrEnum):
    DO_NOTHING_PREFERRED_DUE_TO_SAFETY_RISK = "do_nothing_preferred_due_to_safety_risk"
    DO_NOTHING_PREFERRED_DUE_TO_INSUFFICIENT_METADATA = "do_nothing_preferred_due_to_insufficient_metadata"
    DO_NOTHING_COMPETITIVE_DUE_TO_WARNINGS = "do_nothing_competitive_due_to_warnings"
    PATCH_METADATA_SAFE_BUT_DO_NOTHING_VALID = "patch_metadata_safe_but_do_nothing_valid"
    PATCH_METADATA_SAFER_THAN_DO_NOTHING = "patch_metadata_safer_than_do_nothing"
    DO_NOTHING_REQUIRED_DUE_TO_BLOCKING_VIOLATION = "do_nothing_required_due_to_blocking_violation"
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
    if V0385_VERSION not in version:
        raise ValueError("version must include v0.38.5")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.5")


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


def _collect_patch_text(*items: Any, limit: int = 12000) -> str:
    parts: list[str] = []
    for item in items:
        if item is None:
            continue
        if isinstance(item, str):
            parts.append(item)
            continue
        for name in (
            "proposed_diff_text",
            "original_text",
            "proposed_text",
            "file_change_summary",
            "rationale_summary",
            "envelope_summary",
            "comparison_summary",
            "task_summary",
            "metadata",
        ):
            value = _attr(item, name)
            if value:
                parts.append(str(value))
        for list_name in ("proposed_diffs", "proposed_hunks", "file_changes", "static_findings"):
            for nested in list(_attr(item, list_name, []) or []):
                parts.append(_collect_patch_text(nested, limit=limit))
    return " ".join(parts)[:limit]


def _target_path_risk_and_violation(path: str) -> tuple[list[RepairProposalSafetyRiskKind], list[RepairProposalBoundaryViolationKind]]:
    lowered = path.replace("\\", "/").lower()
    parts = [part for part in lowered.split("/") if part]
    risks: list[RepairProposalSafetyRiskKind] = []
    violations: list[RepairProposalBoundaryViolationKind] = []
    if lowered.startswith("/") or lowered.startswith("\\") or (len(path) > 1 and path[1] == ":"):
        risks.append(RepairProposalSafetyRiskKind.ABSOLUTE_PATH_TARGET_RISK)
        violations.append(RepairProposalBoundaryViolationKind.ABSOLUTE_TARGET_PATH)
    if ".." in parts:
        risks.append(RepairProposalSafetyRiskKind.PARENT_TRAVERSAL_TARGET_RISK)
        violations.append(RepairProposalBoundaryViolationKind.PARENT_TRAVERSAL_TARGET)
    if any(fragment in lowered for fragment in ("references/opencode", "references/hermes", "references/openclaw")):
        risks.append(RepairProposalSafetyRiskKind.REFERENCE_TARGET_RISK)
        violations.append(RepairProposalBoundaryViolationKind.REFERENCE_TARGET)
    if any(fragment in lowered for fragment in (".env", "secret", "credential", "token", "api_key", "apikey")):
        risks.append(RepairProposalSafetyRiskKind.SECRET_TARGET_RISK)
        violations.append(RepairProposalBoundaryViolationKind.SECRET_TARGET)
    return risks, violations


UNSAFE_OPERATION_SPECS = (
    (RepairProposalUnsafeOperationKind.DEPENDENCY_INSTALL, RepairProposalSafetyRiskKind.DEPENDENCY_INSTALL_RISK, ("dependency install", "pip install", "poetry add", "npm install", "yarn add", "pnpm add")),
    (RepairProposalUnsafeOperationKind.PACKAGE_MANAGER_COMMAND, RepairProposalSafetyRiskKind.PACKAGE_MANAGER_RISK, ("package manager", "pip ", "npm ", "pnpm ", "yarn ", "poetry ")),
    (RepairProposalUnsafeOperationKind.NETWORK_CALL, RepairProposalSafetyRiskKind.NETWORK_CALL_RISK, ("network call", "requests", "httpx", "socket", "urllib", "aiohttp", "http://", "https://")),
    (RepairProposalUnsafeOperationKind.SUBPROCESS_SHELL, RepairProposalSafetyRiskKind.SUBPROCESS_SHELL_RISK, ("subprocess", "shell command", "powershell", "cmd.exe", "bash", "os system")),
    (RepairProposalUnsafeOperationKind.EVAL_EXEC, RepairProposalSafetyRiskKind.EVAL_EXEC_RISK, ("eval call", "exec call")),
    (RepairProposalUnsafeOperationKind.DYNAMIC_IMPORT, RepairProposalSafetyRiskKind.DYNAMIC_IMPORT_RISK, ("dynamic import", "importlib", "__import__")),
    (RepairProposalUnsafeOperationKind.FILE_WRITE, RepairProposalSafetyRiskKind.FILE_WRITE_RISK, ("file write", "write file", "write text", "write bytes", ".write")),
    (RepairProposalUnsafeOperationKind.PATCH_APPLY, RepairProposalSafetyRiskKind.PATCH_APPLY_CALL_RISK, ("patch apply", "apply patch", "apply_patch", "patch_applied")),
    (RepairProposalUnsafeOperationKind.GIT_APPLY, RepairProposalSafetyRiskKind.GIT_APPLY_CALL_RISK, ("git_apply", "git-apply")),
    (RepairProposalUnsafeOperationKind.MODEL_PROVIDER_CALL, RepairProposalSafetyRiskKind.MODEL_PROVIDER_CALL_RISK, ("model provider", "openai", "anthropic", "claude")),
    (RepairProposalUnsafeOperationKind.EXTERNAL_AGENT_CALL, RepairProposalSafetyRiskKind.EXTERNAL_AGENT_CALL_RISK, ("external agent", "codex cli", "claude code")),
    (RepairProposalUnsafeOperationKind.CREDENTIAL_SECRET_READ, RepairProposalSafetyRiskKind.CREDENTIAL_SECRET_READ_RISK, ("credential", "secret", "token", "api key", ".env")),
    (RepairProposalUnsafeOperationKind.DOMINION_RUNTIME, RepairProposalSafetyRiskKind.DOMINION_RUNTIME_RISK, ("dominion",)),
    (RepairProposalUnsafeOperationKind.AUTOMATIC_REPAIR_LOOP, RepairProposalSafetyRiskKind.AUTOMATIC_REPAIR_RISK, ("automatic repair",)),
    (RepairProposalUnsafeOperationKind.RETRY_LOOP, RepairProposalSafetyRiskKind.RETRY_LOOP_RISK, ("retry loop", "while true")),
    (RepairProposalUnsafeOperationKind.MULTI_CYCLE_LOOP, RepairProposalSafetyRiskKind.MULTI_CYCLE_LOOP_RISK, ("multi cycle", "multi-cycle")),
    (RepairProposalUnsafeOperationKind.FILE_DELETE, RepairProposalSafetyRiskKind.FILE_DELETION_RISK, ("delete file", "remove file")),
    (RepairProposalUnsafeOperationKind.FILE_RENAME, RepairProposalSafetyRiskKind.FILE_RENAME_RISK, ("rename file", "move file")),
    (RepairProposalUnsafeOperationKind.PERMISSION_CHANGE, RepairProposalSafetyRiskKind.PERMISSION_CHANGE_RISK, ("chmod", "chown", "permission change")),
    (RepairProposalUnsafeOperationKind.BINARY_CHANGE, RepairProposalSafetyRiskKind.BINARY_CHANGE_RISK, ("binary",)),
)

UNSAFE_TO_BOUNDARY = {
    RepairProposalUnsafeOperationKind.DEPENDENCY_INSTALL: RepairProposalBoundaryViolationKind.UNSAFE_DEPENDENCY_INSTALL,
    RepairProposalUnsafeOperationKind.NETWORK_CALL: RepairProposalBoundaryViolationKind.UNSAFE_NETWORK_CALL,
    RepairProposalUnsafeOperationKind.SUBPROCESS_SHELL: RepairProposalBoundaryViolationKind.UNSAFE_SUBPROCESS_SHELL,
    RepairProposalUnsafeOperationKind.MODEL_PROVIDER_CALL: RepairProposalBoundaryViolationKind.UNSAFE_MODEL_PROVIDER_CALL,
    RepairProposalUnsafeOperationKind.EXTERNAL_AGENT_CALL: RepairProposalBoundaryViolationKind.UNSAFE_EXTERNAL_AGENT_CALL,
    RepairProposalUnsafeOperationKind.DOMINION_RUNTIME: RepairProposalBoundaryViolationKind.UNSAFE_DOMINION_RUNTIME,
    RepairProposalUnsafeOperationKind.PATCH_APPLY: RepairProposalBoundaryViolationKind.UNSAFE_PATCH_APPLY_CALL,
    RepairProposalUnsafeOperationKind.GIT_APPLY: RepairProposalBoundaryViolationKind.UNSAFE_PATCH_APPLY_CALL,
    RepairProposalUnsafeOperationKind.FILE_WRITE: RepairProposalBoundaryViolationKind.UNSAFE_FILE_WRITE,
}


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyFlagSet:
    flag_set_id: str
    version: str
    repair_proposal_safety_layer_constructed: bool
    static_patch_metadata_validation_available: bool
    patch_target_validation_available: bool
    patch_content_validation_available: bool
    boundary_violation_scan_available: bool
    unsafe_operation_detection_available: bool
    repair_safety_risk_assessment_available: bool
    repair_safety_do_nothing_comparison_available: bool
    repair_safety_decision_available: bool
    ready_for_v0386_human_review_packet: bool
    ready_for_v0387_bounded_repair_proposal_loop_trial: bool
    ready_for_repair_proposal_safety_validation: bool
    ready_for_static_patch_metadata_validation: bool
    ready_for_patch_target_validation: bool
    ready_for_patch_content_validation: bool
    ready_for_boundary_violation_scan: bool
    ready_for_unsafe_operation_detection: bool
    ready_for_repair_safety_risk_assessment: bool
    ready_for_repair_safety_do_nothing_comparison: bool
    ready_for_repair_safety_decision: bool
    ready_for_future_human_review_packet_input: bool
    ready_for_future_bounded_repair_proposal_loop_trial_input: bool
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
        _validate_false(self, UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetySourceRef:
    source_ref_id: str
    source_kind: RepairProposalSafetySourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSafetySourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyPolicy:
    safety_policy_id: str
    version: str
    allowed_modes: list[RepairProposalSafetyMode | str]
    required_rule_kinds: list[RepairProposalStaticRuleKind | str]
    critical_risk_kinds: list[RepairProposalSafetyRiskKind | str]
    prohibited_unsafe_operations: list[RepairProposalUnsafeOperationKind | str]
    max_findings: int
    max_scan_text_chars: int
    max_report_chars: int
    require_patch_envelope: bool
    require_target_validation: bool
    require_content_validation: bool
    require_do_nothing_comparison: bool
    require_human_review_requirement: bool
    block_on_critical: bool
    block_on_boundary_violation: bool
    allow_static_validation: bool
    allow_target_validation: bool
    allow_content_validation: bool
    allow_boundary_violation_scan: bool
    allow_unsafe_operation_detection: bool
    allow_safety_risk_assessment: bool
    allow_do_nothing_safety_comparison: bool
    allow_future_human_review_packet_input: bool
    allow_future_loop_trial_input: bool
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
        _require_non_blank("safety_policy_id", self.safety_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_modes", self.allowed_modes, RepairProposalSafetyMode)
        _validate_enum_list("required_rule_kinds", self.required_rule_kinds, RepairProposalStaticRuleKind)
        _validate_enum_list("critical_risk_kinds", self.critical_risk_kinds, RepairProposalSafetyRiskKind)
        _validate_enum_list("prohibited_unsafe_operations", self.prohibited_unsafe_operations, RepairProposalUnsafeOperationKind)
        for name in ("max_findings", "max_scan_text_chars", "max_report_chars"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(self, UNSAFE_REPAIR_PROPOSAL_SAFETY_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyInput:
    safety_input_id: str
    version: str
    proposed_patch_envelope_id: str | None
    proposed_diff_ids: list[str]
    proposed_hunk_ids: list[str]
    proposed_file_change_ids: list[str]
    scope_plan_id: str | None
    evidence_bundle_id: str | None
    requested_mode: RepairProposalSafetyMode | str
    source_refs: list[RepairProposalSafetySourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_input_id", "task_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalSafetyMode(self.requested_mode)
        for list_name in ("proposed_diff_ids", "proposed_hunk_ids", "proposed_file_change_ids", "source_refs", "prohibited_runtime_actions"):
            _validate_list(list_name, getattr(self, list_name))
        for action in REQUIRED_REPAIR_PROPOSAL_SAFETY_PROHIBITED_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalStaticValidationRule:
    static_rule_id: str
    rule_kind: RepairProposalStaticRuleKind | str
    check_kind: RepairProposalStaticCheckKind | str
    rule_summary: str
    severity: RepairProposalSafetySeverity | str
    enabled: bool
    blocks_on_failure: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("static_rule_id", "rule_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalStaticRuleKind(self.rule_kind)
        RepairProposalStaticCheckKind(self.check_kind)
        RepairProposalSafetySeverity(self.severity)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalStaticValidationFinding:
    static_finding_id: str
    rule_kind: RepairProposalStaticRuleKind | str
    check_kind: RepairProposalStaticCheckKind | str
    severity: RepairProposalSafetySeverity | str
    finding_summary: str
    evidence_preview: str
    evidence_refs: list[str]
    passed: bool
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("static_finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalStaticRuleKind(self.rule_kind)
        RepairProposalStaticCheckKind(self.check_kind)
        severity = RepairProposalSafetySeverity(self.severity)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if len(self.evidence_preview) > 400:
            raise ValueError("evidence_preview must be bounded")
        if severity in (RepairProposalSafetySeverity.HIGH, RepairProposalSafetySeverity.CRITICAL, RepairProposalSafetySeverity.BLOCKED) and not (self.blocked or self.requires_review):
            raise ValueError("high severity static findings must block or require review")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalBoundaryViolation:
    boundary_violation_id: str
    violation_kind: RepairProposalBoundaryViolationKind | str
    severity: RepairProposalSafetySeverity | str
    violation_summary: str
    target_ref: str | None
    evidence_refs: list[str]
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("boundary_violation_id", "violation_summary"):
            _require_non_blank(name, getattr(self, name))
        violation = RepairProposalBoundaryViolationKind(self.violation_kind)
        severity = RepairProposalSafetySeverity(self.severity)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if violation == RepairProposalBoundaryViolationKind.NO_VIOLATION and (self.blocked or self.requires_review):
            raise ValueError("no_violation must not block")
        if violation != RepairProposalBoundaryViolationKind.NO_VIOLATION and severity in (
            RepairProposalSafetySeverity.HIGH,
            RepairProposalSafetySeverity.CRITICAL,
            RepairProposalSafetySeverity.BLOCKED,
        ) and not (self.blocked or self.requires_review):
            raise ValueError("serious boundary violations must block or require review")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalUnsafeOperationSignal:
    unsafe_signal_id: str
    unsafe_operation_kind: RepairProposalUnsafeOperationKind | str
    severity: RepairProposalSafetySeverity | str
    signal_summary: str
    matched_pattern: str | None
    evidence_preview: str
    evidence_refs: list[str]
    blocked: bool
    requires_review: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("unsafe_signal_id", "signal_summary"):
            _require_non_blank(name, getattr(self, name))
        unsafe_kind = RepairProposalUnsafeOperationKind(self.unsafe_operation_kind)
        RepairProposalSafetySeverity(self.severity)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.matched_pattern is not None and len(self.matched_pattern) > 120:
            raise ValueError("matched_pattern must be bounded")
        if len(self.evidence_preview) > 400:
            raise ValueError("evidence_preview must be bounded")
        if unsafe_kind != RepairProposalUnsafeOperationKind.NO_UNSAFE_OPERATION and not (self.blocked or self.requires_review):
            raise ValueError("unsafe operation signals must block or require review")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalTargetValidation:
    target_validation_id: str
    target_relative_path: str
    valid_target: bool
    normalized_relative_path: str | None
    violation_kinds: list[RepairProposalBoundaryViolationKind | str]
    risk_kinds: list[RepairProposalSafetyRiskKind | str]
    validation_summary: str
    evidence_refs: list[str]
    source_read_performed: bool
    write_allowed: bool
    apply_allowed: bool
    repair_execution_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("target_validation_id", "target_relative_path", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_enum_list("violation_kinds", self.violation_kinds, RepairProposalBoundaryViolationKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairProposalSafetyRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.valid_target and any(kind != RepairProposalBoundaryViolationKind.NO_VIOLATION for kind in self.violation_kinds):
            raise ValueError("target with boundary violation cannot be valid")
        _validate_false(self, UNSAFE_TARGET_VALIDATION_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalContentValidation:
    content_validation_id: str
    validated_artifact_id: str
    artifact_kind: ProposedPatchArtifactKind | str
    static_findings: list[RepairProposalStaticValidationFinding]
    boundary_violations: list[RepairProposalBoundaryViolation]
    unsafe_operation_signals: list[RepairProposalUnsafeOperationSignal]
    validation_summary: str
    safe_for_future_human_review_packet: bool
    safe_for_future_loop_trial: bool
    blocked: bool
    requires_review: bool
    executed_content: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("content_validation_id", "validated_artifact_id", "validation_summary"):
            _require_non_blank(name, getattr(self, name))
        ProposedPatchArtifactKind(self.artifact_kind)
        for list_name in ("static_findings", "boundary_violations", "unsafe_operation_signals"):
            _validate_list(list_name, getattr(self, list_name))
        if self.executed_content is not False:
            raise ValueError("content validation must not execute content")
        if self.blocked and (self.safe_for_future_human_review_packet or self.safe_for_future_loop_trial):
            raise ValueError("blocked content validation cannot be safe for future inputs")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyRiskAssessment:
    safety_risk_assessment_id: str
    risk_kinds: list[RepairProposalSafetyRiskKind | str]
    severity: RepairProposalSafetySeverity | str
    risk_summary: str
    boundary_violation_ids: list[str]
    unsafe_signal_ids: list[str]
    finding_ids: list[str]
    blocks_future_human_review_packet: bool
    blocks_future_loop_trial: bool
    requires_human_review: bool
    do_nothing_recommended: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_risk_assessment_id", "risk_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairProposalSafetyRiskKind)
        severity = RepairProposalSafetySeverity(self.severity)
        for list_name in ("boundary_violation_ids", "unsafe_signal_ids", "finding_ids"):
            _validate_string_list(list_name, getattr(self, list_name))
        if severity in (RepairProposalSafetySeverity.CRITICAL, RepairProposalSafetySeverity.BLOCKED) and not self.blocks_future_loop_trial:
            raise ValueError("critical safety risk must block future loop trial")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyDoNothingComparison:
    do_nothing_safety_comparison_id: str
    comparison_kind: RepairProposalSafetyDoNothingComparisonKind | str
    comparison_summary: str
    evidence_refs: list[str]
    do_nothing_remains_valid: bool
    do_nothing_preferred: bool
    do_nothing_required: bool
    proposal_safe_enough_to_review: bool
    confidence: RepairProposalSafetyConfidenceLevel | str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("do_nothing_safety_comparison_id", "comparison_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSafetyDoNothingComparisonKind(self.comparison_kind)
        RepairProposalSafetyConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.do_nothing_remains_valid is not True:
            raise ValueError("do_nothing_remains_valid must remain True")
        if self.do_nothing_required and self.proposal_safe_enough_to_review:
            raise ValueError("required do-nothing cannot mark proposal safe enough to review")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyDecision:
    safety_decision_id: str
    decision_kind: RepairProposalSafetyDecisionKind | str
    disposition: RepairProposalSafetyDisposition | str
    decision_summary: str
    rationale_summary: str
    confidence: RepairProposalSafetyConfidenceLevel | str
    evidence_refs: list[str]
    ready_for_future_human_review_packet_input: bool
    ready_for_future_loop_trial_input: bool
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
    production_certified: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("safety_decision_id", "decision_summary", "rationale_summary"):
            _require_non_blank(name, getattr(self, name))
        decision = RepairProposalSafetyDecisionKind(self.decision_kind)
        disposition = RepairProposalSafetyDisposition(self.disposition)
        RepairProposalSafetyConfidenceLevel(self.confidence)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if self.ready_for_future_loop_trial_input and disposition in (
            RepairProposalSafetyDisposition.BLOCKED,
            RepairProposalSafetyDisposition.DO_NOTHING_PREFERRED,
            RepairProposalSafetyDisposition.INCONCLUSIVE,
        ):
            raise ValueError("blocked or do-nothing decisions cannot be ready for loop trial input")
        if decision == RepairProposalSafetyDecisionKind.UNKNOWN:
            raise ValueError("unknown safety decision must not be constructed as allowing readiness")
        _validate_false(self, UNSAFE_SAFETY_DECISION_NOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyReport:
    safety_report_id: str
    version: str
    safety_input_id: str
    status: RepairProposalSafetyStatus | str
    readiness_level: RepairProposalSafetyReadinessLevel | str
    target_validations: list[RepairProposalTargetValidation]
    content_validations: list[RepairProposalContentValidation]
    static_findings: list[RepairProposalStaticValidationFinding]
    boundary_violations: list[RepairProposalBoundaryViolation]
    unsafe_operation_signals: list[RepairProposalUnsafeOperationSignal]
    risk_assessment: RepairProposalSafetyRiskAssessment
    do_nothing_comparison: RepairProposalSafetyDoNothingComparison
    safety_decision: RepairProposalSafetyDecision
    source_refs: list[RepairProposalSafetySourceRef]
    report_summary: str
    ready_for_future_human_review_packet_input: bool
    ready_for_future_loop_trial_input: bool
    source_read_performed_by_v0385: bool
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
        for name in ("safety_report_id", "safety_input_id", "report_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalSafetyStatus(self.status)
        RepairProposalSafetyReadinessLevel(self.readiness_level)
        for list_name in ("target_validations", "content_validations", "static_findings", "boundary_violations", "unsafe_operation_signals", "source_refs"):
            _validate_list(list_name, getattr(self, list_name))
        if not isinstance(self.risk_assessment, RepairProposalSafetyRiskAssessment):
            raise TypeError("risk_assessment must be RepairProposalSafetyRiskAssessment")
        if not isinstance(self.do_nothing_comparison, RepairProposalSafetyDoNothingComparison):
            raise TypeError("do_nothing_comparison must be RepairProposalSafetyDoNothingComparison")
        if not isinstance(self.safety_decision, RepairProposalSafetyDecision):
            raise TypeError("safety_decision must be RepairProposalSafetyDecision")
        if self.ready_for_future_loop_trial_input and self.risk_assessment.blocks_future_loop_trial:
            raise ValueError("blocked risk assessment cannot be ready for future loop trial input")
        if self.ready_for_future_human_review_packet_input and self.risk_assessment.blocks_future_human_review_packet:
            raise ValueError("blocked risk assessment cannot be ready for future human review packet input")
        _validate_false(self, UNSAFE_SAFETY_REPORT_STATE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyValidationFinding:
    finding_id: str
    finding_summary: str
    severity: RepairProposalSafetySeverity | str
    blocks_future_human_review_packet: bool
    blocks_future_loop_trial: bool
    requires_human_review: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("finding_id", "finding_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSafetySeverity(self.severity)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyValidationReport:
    validation_report_id: str
    version: str
    safety_report_id: str
    findings: list[RepairProposalSafetyValidationFinding]
    validation_summary: str
    static_validation_confirmed: bool
    no_source_read_confirmed: bool
    no_file_write_confirmed: bool
    no_patch_file_write_confirmed: bool
    no_edit_confirmed: bool
    no_apply_confirmed: bool
    no_repair_confirmed: bool
    no_tests_confirmed: bool
    no_external_calls_confirmed: bool
    do_nothing_comparison_confirmed: bool
    human_review_requirement_confirmed: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("validation_report_id", "safety_report_id", "validation_summary"):
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
class RepairProposalSafetyRunPreview:
    run_preview_id: str
    version: str
    requested_mode: RepairProposalSafetyMode | str
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
        RepairProposalSafetyMode(self.requested_mode)
        for name in self.__dataclass_fields__:
            if name.startswith("will_") and getattr(self, name) is not False:
                raise ValueError(f"{name} must be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSafetyNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_source_read: bool
    no_write: bool
    no_patch_file: bool
    no_edit: bool
    no_apply: bool
    no_repair: bool
    no_test: bool
    no_external_call: bool
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
class V0385ReadinessReport:
    readiness_report_id: str
    version: str
    safety_report_id: str
    readiness_level: RepairProposalSafetyReadinessLevel | str
    status: RepairProposalSafetyStatus | str
    summary: str
    ready_for_v0386_human_review_packet: bool
    ready_for_v0387_bounded_repair_proposal_loop_trial: bool
    ready_for_repair_proposal_safety_validation: bool
    ready_for_static_patch_metadata_validation: bool
    ready_for_patch_target_validation: bool
    ready_for_patch_content_validation: bool
    ready_for_boundary_violation_scan: bool
    ready_for_unsafe_operation_detection: bool
    ready_for_repair_safety_risk_assessment: bool
    ready_for_repair_safety_do_nothing_comparison: bool
    ready_for_repair_safety_decision: bool
    ready_for_future_human_review_packet_input: bool
    ready_for_future_bounded_repair_proposal_loop_trial_input: bool
    evidence_refs: list[str]
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
        for name in ("readiness_report_id", "safety_report_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalSafetyReadinessLevel(self.readiness_level)
        RepairProposalSafetyStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES)
        _validate_metadata(self.metadata)


def build_repair_proposal_safety_flags(**kwargs: Any) -> RepairProposalSafetyFlagSet:
    return RepairProposalSafetyFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_proposal_safety_flags:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        repair_proposal_safety_layer_constructed=kwargs.pop("repair_proposal_safety_layer_constructed", True),
        static_patch_metadata_validation_available=kwargs.pop("static_patch_metadata_validation_available", True),
        patch_target_validation_available=kwargs.pop("patch_target_validation_available", True),
        patch_content_validation_available=kwargs.pop("patch_content_validation_available", True),
        boundary_violation_scan_available=kwargs.pop("boundary_violation_scan_available", True),
        unsafe_operation_detection_available=kwargs.pop("unsafe_operation_detection_available", True),
        repair_safety_risk_assessment_available=kwargs.pop("repair_safety_risk_assessment_available", True),
        repair_safety_do_nothing_comparison_available=kwargs.pop("repair_safety_do_nothing_comparison_available", True),
        repair_safety_decision_available=kwargs.pop("repair_safety_decision_available", True),
        ready_for_v0386_human_review_packet=kwargs.pop("ready_for_v0386_human_review_packet", True),
        ready_for_v0387_bounded_repair_proposal_loop_trial=kwargs.pop("ready_for_v0387_bounded_repair_proposal_loop_trial", True),
        ready_for_repair_proposal_safety_validation=kwargs.pop("ready_for_repair_proposal_safety_validation", True),
        ready_for_static_patch_metadata_validation=kwargs.pop("ready_for_static_patch_metadata_validation", True),
        ready_for_patch_target_validation=kwargs.pop("ready_for_patch_target_validation", True),
        ready_for_patch_content_validation=kwargs.pop("ready_for_patch_content_validation", True),
        ready_for_boundary_violation_scan=kwargs.pop("ready_for_boundary_violation_scan", True),
        ready_for_unsafe_operation_detection=kwargs.pop("ready_for_unsafe_operation_detection", True),
        ready_for_repair_safety_risk_assessment=kwargs.pop("ready_for_repair_safety_risk_assessment", True),
        ready_for_repair_safety_do_nothing_comparison=kwargs.pop("ready_for_repair_safety_do_nothing_comparison", True),
        ready_for_repair_safety_decision=kwargs.pop("ready_for_repair_safety_decision", True),
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", True),
        ready_for_future_bounded_repair_proposal_loop_trial_input=kwargs.pop("ready_for_future_bounded_repair_proposal_loop_trial_input", True),
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
            "static_validation_only": True,
            "no_independent_autonomous_agent_runtime": True,
            "mandatory_human_review_before_any_apply": True,
        }),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES},
    )


def build_repair_proposal_safety_source_ref(**kwargs: Any) -> RepairProposalSafetySourceRef:
    return RepairProposalSafetySourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "repair_proposal_safety_source_ref:v0.38.5"),
        source_kind=kwargs.pop("source_kind", RepairProposalSafetySourceKind.V0384_PROPOSED_PATCH_ENVELOPE),
        source_id=kwargs.pop("source_id", "v0.38.4 proposed patch envelope metadata"),
        source_summary=kwargs.pop("source_summary", "existing proposed patch metadata consumed without source read"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_safety_policy(**kwargs: Any) -> RepairProposalSafetyPolicy:
    return RepairProposalSafetyPolicy(
        safety_policy_id=kwargs.pop("safety_policy_id", "repair_proposal_safety_policy:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        allowed_modes=kwargs.pop("allowed_modes", [item for item in RepairProposalSafetyMode if item not in (RepairProposalSafetyMode.UNKNOWN,)]),
        required_rule_kinds=kwargs.pop("required_rule_kinds", [
            RepairProposalStaticRuleKind.REQUIRE_PATCH_ENVELOPE,
            RepairProposalStaticRuleKind.REQUIRE_DO_NOTHING_COMPARISON,
            RepairProposalStaticRuleKind.REQUIRE_HUMAN_REVIEW_REQUIREMENT,
            RepairProposalStaticRuleKind.PROHIBIT_ABSOLUTE_TARGET_PATH,
            RepairProposalStaticRuleKind.PROHIBIT_PARENT_TRAVERSAL_TARGET,
            RepairProposalStaticRuleKind.PROHIBIT_REFERENCE_TARGET,
            RepairProposalStaticRuleKind.PROHIBIT_SECRET_TARGET,
            RepairProposalStaticRuleKind.PROHIBIT_DEPENDENCY_INSTALL,
            RepairProposalStaticRuleKind.PROHIBIT_NETWORK_CALL,
            RepairProposalStaticRuleKind.PROHIBIT_SUBPROCESS_SHELL,
            RepairProposalStaticRuleKind.PROHIBIT_MODEL_PROVIDER_CALL,
            RepairProposalStaticRuleKind.PROHIBIT_EXTERNAL_AGENT_CALL,
            RepairProposalStaticRuleKind.PROHIBIT_DOMINION_RUNTIME,
        ]),
        critical_risk_kinds=kwargs.pop("critical_risk_kinds", [RepairProposalSafetyRiskKind(item) for item in CRITICAL_RISK_KINDS]),
        prohibited_unsafe_operations=kwargs.pop("prohibited_unsafe_operations", [item for item in RepairProposalUnsafeOperationKind if item not in (RepairProposalUnsafeOperationKind.NO_UNSAFE_OPERATION, RepairProposalUnsafeOperationKind.UNKNOWN)]),
        max_findings=kwargs.pop("max_findings", 50),
        max_scan_text_chars=kwargs.pop("max_scan_text_chars", 12000),
        max_report_chars=kwargs.pop("max_report_chars", 12000),
        require_patch_envelope=kwargs.pop("require_patch_envelope", True),
        require_target_validation=kwargs.pop("require_target_validation", True),
        require_content_validation=kwargs.pop("require_content_validation", True),
        require_do_nothing_comparison=kwargs.pop("require_do_nothing_comparison", True),
        require_human_review_requirement=kwargs.pop("require_human_review_requirement", True),
        block_on_critical=kwargs.pop("block_on_critical", True),
        block_on_boundary_violation=kwargs.pop("block_on_boundary_violation", True),
        allow_static_validation=kwargs.pop("allow_static_validation", True),
        allow_target_validation=kwargs.pop("allow_target_validation", True),
        allow_content_validation=kwargs.pop("allow_content_validation", True),
        allow_boundary_violation_scan=kwargs.pop("allow_boundary_violation_scan", True),
        allow_unsafe_operation_detection=kwargs.pop("allow_unsafe_operation_detection", True),
        allow_safety_risk_assessment=kwargs.pop("allow_safety_risk_assessment", True),
        allow_do_nothing_safety_comparison=kwargs.pop("allow_do_nothing_safety_comparison", True),
        allow_future_human_review_packet_input=kwargs.pop("allow_future_human_review_packet_input", True),
        allow_future_loop_trial_input=kwargs.pop("allow_future_loop_trial_input", True),
        metadata=kwargs.pop("metadata", {"policy_is_not_apply_or_repair_permission": True}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_PROPOSAL_SAFETY_POLICY_ALLOW_NAMES},
    )


def default_repair_proposal_safety_policy() -> RepairProposalSafetyPolicy:
    return build_repair_proposal_safety_policy()


def build_repair_proposal_safety_input(**kwargs: Any) -> RepairProposalSafetyInput:
    return RepairProposalSafetyInput(
        safety_input_id=kwargs.pop("safety_input_id", "repair_proposal_safety_input:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        proposed_patch_envelope_id=kwargs.pop("proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        proposed_diff_ids=kwargs.pop("proposed_diff_ids", []),
        proposed_hunk_ids=kwargs.pop("proposed_hunk_ids", []),
        proposed_file_change_ids=kwargs.pop("proposed_file_change_ids", []),
        scope_plan_id=kwargs.pop("scope_plan_id", "repair_scope_plan:v0.38.3"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", None),
        requested_mode=kwargs.pop("requested_mode", RepairProposalSafetyMode.STATIC_VALIDATION),
        source_refs=kwargs.pop("source_refs", [build_repair_proposal_safety_source_ref()]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", list(REQUIRED_REPAIR_PROPOSAL_SAFETY_PROHIBITED_ACTIONS)),
        task_summary=kwargs.pop("task_summary", "safety validation request for proposed patch metadata only"),
        metadata=kwargs.pop("metadata", {"input_is_not_apply_request": True}),
    )


def build_repair_proposal_static_validation_rule(**kwargs: Any) -> RepairProposalStaticValidationRule:
    return RepairProposalStaticValidationRule(
        static_rule_id=kwargs.pop("static_rule_id", "repair_proposal_static_rule:v0.38.5"),
        rule_kind=kwargs.pop("rule_kind", RepairProposalStaticRuleKind.REQUIRE_PATCH_ENVELOPE),
        check_kind=kwargs.pop("check_kind", RepairProposalStaticCheckKind.METADATA_PRESENCE_CHECK),
        rule_summary=kwargs.pop("rule_summary", "static validation rule inspects metadata only"),
        severity=kwargs.pop("severity", RepairProposalSafetySeverity.HIGH),
        enabled=kwargs.pop("enabled", True),
        blocks_on_failure=kwargs.pop("blocks_on_failure", True),
        metadata=kwargs.pop("metadata", {"does_not_execute_proposed_code": True}),
    )


def build_repair_proposal_static_validation_finding(**kwargs: Any) -> RepairProposalStaticValidationFinding:
    return RepairProposalStaticValidationFinding(
        static_finding_id=kwargs.pop("static_finding_id", "repair_proposal_static_finding:v0.38.5"),
        rule_kind=kwargs.pop("rule_kind", RepairProposalStaticRuleKind.REQUIRE_PATCH_ENVELOPE),
        check_kind=kwargs.pop("check_kind", RepairProposalStaticCheckKind.METADATA_PRESENCE_CHECK),
        severity=kwargs.pop("severity", RepairProposalSafetySeverity.INFO),
        finding_summary=kwargs.pop("finding_summary", "static validation metadata finding"),
        evidence_preview=kwargs.pop("evidence_preview", "bounded metadata preview"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 static validation"]),
        passed=kwargs.pop("passed", True),
        blocked=kwargs.pop("blocked", False),
        requires_review=kwargs.pop("requires_review", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_boundary_violation(**kwargs: Any) -> RepairProposalBoundaryViolation:
    violation_kind = kwargs.pop("violation_kind", RepairProposalBoundaryViolationKind.NO_VIOLATION)
    blocked = kwargs.pop("blocked", violation_kind != RepairProposalBoundaryViolationKind.NO_VIOLATION)
    return RepairProposalBoundaryViolation(
        boundary_violation_id=kwargs.pop("boundary_violation_id", "repair_proposal_boundary_violation:v0.38.5"),
        violation_kind=violation_kind,
        severity=kwargs.pop("severity", RepairProposalSafetySeverity.CRITICAL if blocked else RepairProposalSafetySeverity.INFO),
        violation_summary=kwargs.pop("violation_summary", "repair proposal boundary validation metadata"),
        target_ref=kwargs.pop("target_ref", None),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 boundary scan"]),
        blocked=blocked,
        requires_review=kwargs.pop("requires_review", blocked),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_unsafe_operation_signal(**kwargs: Any) -> RepairProposalUnsafeOperationSignal:
    unsafe_kind = kwargs.pop("unsafe_operation_kind", RepairProposalUnsafeOperationKind.NO_UNSAFE_OPERATION)
    blocked = kwargs.pop("blocked", unsafe_kind != RepairProposalUnsafeOperationKind.NO_UNSAFE_OPERATION)
    preview, _ = _bounded_text(kwargs.pop("evidence_preview", "bounded unsafe operation metadata preview"), 400)
    matched, _ = _bounded_text(kwargs.pop("matched_pattern", None), 120)
    return RepairProposalUnsafeOperationSignal(
        unsafe_signal_id=kwargs.pop("unsafe_signal_id", "repair_proposal_unsafe_signal:v0.38.5"),
        unsafe_operation_kind=unsafe_kind,
        severity=kwargs.pop("severity", RepairProposalSafetySeverity.CRITICAL if blocked else RepairProposalSafetySeverity.INFO),
        signal_summary=kwargs.pop("signal_summary", "unsafe operation signal derived from proposed metadata text"),
        matched_pattern=matched if matched else None,
        evidence_preview=preview,
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 unsafe operation scan"]),
        blocked=blocked,
        requires_review=kwargs.pop("requires_review", blocked),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_target_validation(**kwargs: Any) -> RepairProposalTargetValidation:
    return RepairProposalTargetValidation(
        target_validation_id=kwargs.pop("target_validation_id", "repair_proposal_target_validation:v0.38.5"),
        target_relative_path=kwargs.pop("target_relative_path", "src/example.py"),
        valid_target=kwargs.pop("valid_target", True),
        normalized_relative_path=kwargs.pop("normalized_relative_path", kwargs.get("target_relative_path", "src/example.py")),
        violation_kinds=kwargs.pop("violation_kinds", [RepairProposalBoundaryViolationKind.NO_VIOLATION]),
        risk_kinds=kwargs.pop("risk_kinds", []),
        validation_summary=kwargs.pop("validation_summary", "target path validation uses metadata only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 target validation"]),
        source_read_performed=kwargs.pop("source_read_performed", False),
        write_allowed=kwargs.pop("write_allowed", False),
        apply_allowed=kwargs.pop("apply_allowed", False),
        repair_execution_allowed=kwargs.pop("repair_execution_allowed", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_content_validation(**kwargs: Any) -> RepairProposalContentValidation:
    blocked = kwargs.pop("blocked", False)
    return RepairProposalContentValidation(
        content_validation_id=kwargs.pop("content_validation_id", "repair_proposal_content_validation:v0.38.5"),
        validated_artifact_id=kwargs.pop("validated_artifact_id", "proposed_patch_envelope:v0.38.4"),
        artifact_kind=kwargs.pop("artifact_kind", ProposedPatchArtifactKind.PROPOSED_PATCH_ENVELOPE),
        static_findings=kwargs.pop("static_findings", []),
        boundary_violations=kwargs.pop("boundary_violations", []),
        unsafe_operation_signals=kwargs.pop("unsafe_operation_signals", []),
        validation_summary=kwargs.pop("validation_summary", "content validation scans bounded in-memory metadata only"),
        safe_for_future_human_review_packet=kwargs.pop("safe_for_future_human_review_packet", not blocked),
        safe_for_future_loop_trial=kwargs.pop("safe_for_future_loop_trial", not blocked),
        blocked=blocked,
        requires_review=kwargs.pop("requires_review", blocked),
        executed_content=kwargs.pop("executed_content", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_safety_risk_assessment(**kwargs: Any) -> RepairProposalSafetyRiskAssessment:
    risk_kinds = kwargs.pop("risk_kinds", [])
    critical = any(str(risk) in {str(item) for item in CRITICAL_RISK_KINDS} or RepairProposalSafetyRiskKind(risk).value in CRITICAL_RISK_KINDS for risk in risk_kinds)
    return RepairProposalSafetyRiskAssessment(
        safety_risk_assessment_id=kwargs.pop("safety_risk_assessment_id", "repair_proposal_safety_risk_assessment:v0.38.5"),
        risk_kinds=risk_kinds,
        severity=kwargs.pop("severity", RepairProposalSafetySeverity.CRITICAL if critical else (RepairProposalSafetySeverity.LOW if risk_kinds else RepairProposalSafetySeverity.INFO)),
        risk_summary=kwargs.pop("risk_summary", "repair proposal safety risk assessment metadata"),
        boundary_violation_ids=kwargs.pop("boundary_violation_ids", []),
        unsafe_signal_ids=kwargs.pop("unsafe_signal_ids", []),
        finding_ids=kwargs.pop("finding_ids", []),
        blocks_future_human_review_packet=kwargs.pop("blocks_future_human_review_packet", False),
        blocks_future_loop_trial=kwargs.pop("blocks_future_loop_trial", critical),
        requires_human_review=kwargs.pop("requires_human_review", bool(risk_kinds)),
        do_nothing_recommended=kwargs.pop("do_nothing_recommended", bool(risk_kinds)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_safety_do_nothing_comparison(**kwargs: Any) -> RepairProposalSafetyDoNothingComparison:
    return RepairProposalSafetyDoNothingComparison(
        do_nothing_safety_comparison_id=kwargs.pop("do_nothing_safety_comparison_id", "repair_proposal_safety_do_nothing:v0.38.5"),
        comparison_kind=kwargs.pop("comparison_kind", RepairProposalSafetyDoNothingComparisonKind.PATCH_METADATA_SAFE_BUT_DO_NOTHING_VALID),
        comparison_summary=kwargs.pop("comparison_summary", "do-nothing remains valid during safety validation"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 do-nothing safety comparison"]),
        do_nothing_remains_valid=kwargs.pop("do_nothing_remains_valid", True),
        do_nothing_preferred=kwargs.pop("do_nothing_preferred", False),
        do_nothing_required=kwargs.pop("do_nothing_required", False),
        proposal_safe_enough_to_review=kwargs.pop("proposal_safe_enough_to_review", True),
        confidence=kwargs.pop("confidence", RepairProposalSafetyConfidenceLevel.MEDIUM),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_safety_decision(**kwargs: Any) -> RepairProposalSafetyDecision:
    return RepairProposalSafetyDecision(
        safety_decision_id=kwargs.pop("safety_decision_id", "repair_proposal_safety_decision:v0.38.5"),
        decision_kind=kwargs.pop("decision_kind", RepairProposalSafetyDecisionKind.ALLOW_FUTURE_HUMAN_REVIEW_PACKET_INPUT),
        disposition=kwargs.pop("disposition", RepairProposalSafetyDisposition.SAFETY_PASS),
        decision_summary=kwargs.pop("decision_summary", "safety decision allows future review input only"),
        rationale_summary=kwargs.pop("rationale_summary", "static validation is not apply, test, repair, or correctness proof"),
        confidence=kwargs.pop("confidence", RepairProposalSafetyConfidenceLevel.MEDIUM),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 safety decision"]),
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", True),
        ready_for_future_loop_trial_input=kwargs.pop("ready_for_future_loop_trial_input", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SAFETY_DECISION_NOW_NAMES},
    )


def build_repair_proposal_safety_report(**kwargs: Any) -> RepairProposalSafetyReport:
    risk = kwargs.pop("risk_assessment", build_repair_proposal_safety_risk_assessment())
    do_nothing = kwargs.pop("do_nothing_comparison", build_repair_proposal_safety_do_nothing_comparison())
    decision = kwargs.pop("safety_decision", build_repair_proposal_safety_decision(
        ready_for_future_human_review_packet_input=not risk.blocks_future_human_review_packet,
        ready_for_future_loop_trial_input=not risk.blocks_future_loop_trial,
    ))
    return RepairProposalSafetyReport(
        safety_report_id=kwargs.pop("safety_report_id", "repair_proposal_safety_report:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        safety_input_id=kwargs.pop("safety_input_id", "repair_proposal_safety_input:v0.38.5"),
        status=kwargs.pop("status", RepairProposalSafetyStatus.VALIDATION_COMPLETED if not risk.risk_kinds else RepairProposalSafetyStatus.REVIEW_REQUIRED),
        readiness_level=kwargs.pop("readiness_level", RepairProposalSafetyReadinessLevel.FUTURE_HUMAN_REVIEW_PACKET_INPUT_READY if decision.ready_for_future_human_review_packet_input else RepairProposalSafetyReadinessLevel.SAFETY_RISK_ASSESSMENT_READY),
        target_validations=kwargs.pop("target_validations", []),
        content_validations=kwargs.pop("content_validations", []),
        static_findings=kwargs.pop("static_findings", []),
        boundary_violations=kwargs.pop("boundary_violations", []),
        unsafe_operation_signals=kwargs.pop("unsafe_operation_signals", []),
        risk_assessment=risk,
        do_nothing_comparison=do_nothing,
        safety_decision=decision,
        source_refs=kwargs.pop("source_refs", []),
        report_summary=kwargs.pop("report_summary", "repair proposal safety report metadata only"),
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", decision.ready_for_future_human_review_packet_input),
        ready_for_future_loop_trial_input=kwargs.pop("ready_for_future_loop_trial_input", decision.ready_for_future_loop_trial_input),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SAFETY_REPORT_STATE_NAMES},
    )


def build_repair_proposal_safety_validation_finding(**kwargs: Any) -> RepairProposalSafetyValidationFinding:
    return RepairProposalSafetyValidationFinding(
        finding_id=kwargs.pop("finding_id", "repair_proposal_safety_validation_finding:v0.38.5"),
        finding_summary=kwargs.pop("finding_summary", "safety validation confirms metadata-only no-apply boundary"),
        severity=kwargs.pop("severity", RepairProposalSafetySeverity.INFO),
        blocks_future_human_review_packet=kwargs.pop("blocks_future_human_review_packet", False),
        blocks_future_loop_trial=kwargs.pop("blocks_future_loop_trial", False),
        requires_human_review=kwargs.pop("requires_human_review", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 safety validation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_safety_validation_report(**kwargs: Any) -> RepairProposalSafetyValidationReport:
    return RepairProposalSafetyValidationReport(
        validation_report_id=kwargs.pop("validation_report_id", "repair_proposal_safety_validation_report:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        safety_report_id=kwargs.pop("safety_report_id", "repair_proposal_safety_report:v0.38.5"),
        findings=kwargs.pop("findings", [build_repair_proposal_safety_validation_finding()]),
        validation_summary=kwargs.pop("validation_summary", "safety validation report confirms static metadata-only validation"),
        static_validation_confirmed=kwargs.pop("static_validation_confirmed", True),
        no_source_read_confirmed=kwargs.pop("no_source_read_confirmed", True),
        no_file_write_confirmed=kwargs.pop("no_file_write_confirmed", True),
        no_patch_file_write_confirmed=kwargs.pop("no_patch_file_write_confirmed", True),
        no_edit_confirmed=kwargs.pop("no_edit_confirmed", True),
        no_apply_confirmed=kwargs.pop("no_apply_confirmed", True),
        no_repair_confirmed=kwargs.pop("no_repair_confirmed", True),
        no_tests_confirmed=kwargs.pop("no_tests_confirmed", True),
        no_external_calls_confirmed=kwargs.pop("no_external_calls_confirmed", True),
        do_nothing_comparison_confirmed=kwargs.pop("do_nothing_comparison_confirmed", True),
        human_review_requirement_confirmed=kwargs.pop("human_review_requirement_confirmed", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_safety_run_preview(**kwargs: Any) -> RepairProposalSafetyRunPreview:
    return RepairProposalSafetyRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "repair_proposal_safety_run_preview:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        requested_mode=kwargs.pop("requested_mode", RepairProposalSafetyMode.STATIC_VALIDATION),
        preview_summary=kwargs.pop("preview_summary", "safety validation preview scans metadata only"),
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


def build_repair_proposal_safety_no_apply_guarantee(**kwargs: Any) -> RepairProposalSafetyNoApplyGuarantee:
    return RepairProposalSafetyNoApplyGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_proposal_safety_no_apply_guarantee:v0.38.5"),
        version=kwargs.pop("version", V0385_VERSION),
        no_source_read=kwargs.pop("no_source_read", True),
        no_write=kwargs.pop("no_write", True),
        no_patch_file=kwargs.pop("no_patch_file", True),
        no_edit=kwargs.pop("no_edit", True),
        no_apply=kwargs.pop("no_apply", True),
        no_repair=kwargs.pop("no_repair", True),
        no_test=kwargs.pop("no_test", True),
        no_external_call=kwargs.pop("no_external_call", True),
        no_subprocess=kwargs.pop("no_subprocess", True),
        no_shell=kwargs.pop("no_shell", True),
        no_network=kwargs.pop("no_network", True),
        no_model_provider=kwargs.pop("no_model_provider", True),
        no_external_agent=kwargs.pop("no_external_agent", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        guarantee_summary=kwargs.pop("guarantee_summary", "v0.38.5 validates metadata only and grants no apply permission"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v0385_readiness_report(**kwargs: Any) -> V0385ReadinessReport:
    return V0385ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0385_readiness_report"),
        version=kwargs.pop("version", V0385_VERSION),
        safety_report_id=kwargs.pop("safety_report_id", "repair_proposal_safety_report:v0.38.5"),
        readiness_level=kwargs.pop("readiness_level", RepairProposalSafetyReadinessLevel.FUTURE_HUMAN_REVIEW_PACKET_INPUT_READY),
        status=kwargs.pop("status", RepairProposalSafetyStatus.READY_FOR_FUTURE_HUMAN_REVIEW_PACKET),
        summary=kwargs.pop("summary", "v0.38.5 is ready for design-stage human review packet and loop trial input only"),
        ready_for_v0386_human_review_packet=kwargs.pop("ready_for_v0386_human_review_packet", True),
        ready_for_v0387_bounded_repair_proposal_loop_trial=kwargs.pop("ready_for_v0387_bounded_repair_proposal_loop_trial", True),
        ready_for_repair_proposal_safety_validation=kwargs.pop("ready_for_repair_proposal_safety_validation", True),
        ready_for_static_patch_metadata_validation=kwargs.pop("ready_for_static_patch_metadata_validation", True),
        ready_for_patch_target_validation=kwargs.pop("ready_for_patch_target_validation", True),
        ready_for_patch_content_validation=kwargs.pop("ready_for_patch_content_validation", True),
        ready_for_boundary_violation_scan=kwargs.pop("ready_for_boundary_violation_scan", True),
        ready_for_unsafe_operation_detection=kwargs.pop("ready_for_unsafe_operation_detection", True),
        ready_for_repair_safety_risk_assessment=kwargs.pop("ready_for_repair_safety_risk_assessment", True),
        ready_for_repair_safety_do_nothing_comparison=kwargs.pop("ready_for_repair_safety_do_nothing_comparison", True),
        ready_for_repair_safety_decision=kwargs.pop("ready_for_repair_safety_decision", True),
        ready_for_future_human_review_packet_input=kwargs.pop("ready_for_future_human_review_packet_input", True),
        ready_for_future_bounded_repair_proposal_loop_trial_input=kwargs.pop("ready_for_future_bounded_repair_proposal_loop_trial_input", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.5 safety report"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES},
    )


def build_repair_proposal_safety_input_from_patch_envelope(envelope: Any, scope_plan: Any | None = None, evidence_bundle: Any | None = None) -> RepairProposalSafetyInput:
    return build_repair_proposal_safety_input(
        proposed_patch_envelope_id=_attr(envelope, "proposed_patch_envelope_id", None),
        proposed_diff_ids=[_attr(diff, "proposed_diff_id", "unknown") for diff in list(_attr(envelope, "proposed_diffs", []) or [])],
        proposed_hunk_ids=[_attr(hunk, "proposed_hunk_id", "unknown") for hunk in list(_attr(envelope, "proposed_hunks", []) or [])],
        proposed_file_change_ids=[_attr(change, "proposed_file_change_id", "unknown") for change in list(_attr(envelope, "file_changes", []) or [])],
        scope_plan_id=_attr(scope_plan, "scope_plan_id", _attr(envelope, "metadata", {}).get("scope_plan_id") if isinstance(_attr(envelope, "metadata", {}), dict) else None),
        evidence_bundle_id=_attr(evidence_bundle, "evidence_bundle_id", None),
        source_refs=[build_repair_proposal_safety_source_ref(
            source_id=_attr(envelope, "proposed_patch_envelope_id", "v0.38.4 proposed patch envelope"),
            evidence_refs=[_attr(envelope, "proposed_patch_envelope_id", "v0.38.4 proposed patch envelope")],
        )],
    )


def validate_repair_proposal_targets(target_paths: list[str], policy: RepairProposalSafetyPolicy | None = None) -> list[RepairProposalTargetValidation]:
    policy = policy or default_repair_proposal_safety_policy()
    results: list[RepairProposalTargetValidation] = []
    for index, path in enumerate(target_paths, start=1):
        risks, violations = _target_path_risk_and_violation(path)
        valid = not risks
        results.append(build_repair_proposal_target_validation(
            target_validation_id=f"repair_proposal_target_validation:{index}:v0.38.5",
            target_relative_path=path,
            normalized_relative_path=path.replace("\\", "/") if valid else None,
            valid_target=valid,
            violation_kinds=violations or [RepairProposalBoundaryViolationKind.NO_VIOLATION],
            risk_kinds=risks,
            validation_summary="target path is valid metadata target" if valid else "target path violates safety boundary",
            evidence_refs=[path],
        ))
        if len(results) >= policy.max_findings:
            break
    return results


def scan_proposed_patch_text_for_unsafe_operations(texts: str | list[str], policy: RepairProposalSafetyPolicy | None = None) -> list[RepairProposalUnsafeOperationSignal]:
    policy = policy or default_repair_proposal_safety_policy()
    text = texts if isinstance(texts, str) else " ".join(str(item) for item in texts)
    bounded, _ = _bounded_text(text, policy.max_scan_text_chars)
    lowered = bounded.lower()
    signals: list[RepairProposalUnsafeOperationSignal] = []
    for operation_kind, _risk_kind, tokens in UNSAFE_OPERATION_SPECS:
        for token in tokens:
            if token in lowered:
                signals.append(build_repair_proposal_unsafe_operation_signal(
                    unsafe_signal_id=f"repair_proposal_unsafe_signal:{operation_kind.value}:v0.38.5",
                    unsafe_operation_kind=operation_kind,
                    matched_pattern=token,
                    evidence_preview=bounded,
                    evidence_refs=["proposed patch metadata text"],
                ))
                break
        if len(signals) >= policy.max_findings:
            break
    return signals


def validate_repair_proposal_content(envelope: Any, policy: RepairProposalSafetyPolicy | None = None) -> RepairProposalContentValidation:
    policy = policy or default_repair_proposal_safety_policy()
    text = _collect_patch_text(envelope, limit=policy.max_scan_text_chars)
    signals = scan_proposed_patch_text_for_unsafe_operations(text, policy)
    violations = [
        build_repair_proposal_boundary_violation(
            boundary_violation_id=f"repair_proposal_boundary_violation:{index}:v0.38.5",
            violation_kind=UNSAFE_TO_BOUNDARY.get(RepairProposalUnsafeOperationKind(signal.unsafe_operation_kind), RepairProposalBoundaryViolationKind.UNSAFE_OPERATION),
            target_ref=_attr(envelope, "proposed_patch_envelope_id", None),
            evidence_refs=signal.evidence_refs,
        )
        for index, signal in enumerate(signals, start=1)
    ]
    findings = [
        build_repair_proposal_static_validation_finding(
            static_finding_id=f"repair_proposal_static_finding:{index}:v0.38.5",
            rule_kind=RepairProposalStaticRuleKind.PROHIBIT_DEPENDENCY_INSTALL if RepairProposalUnsafeOperationKind(signal.unsafe_operation_kind) == RepairProposalUnsafeOperationKind.DEPENDENCY_INSTALL else RepairProposalStaticRuleKind.PROHIBIT_NETWORK_CALL,
            check_kind=RepairProposalStaticCheckKind.PROPOSED_TEXT_PATTERN_CHECK,
            severity=RepairProposalSafetySeverity.CRITICAL,
            finding_summary=f"unsafe operation detected: {signal.unsafe_operation_kind}",
            evidence_preview=signal.evidence_preview,
            evidence_refs=signal.evidence_refs,
            passed=False,
            blocked=True,
            requires_review=True,
        )
        for index, signal in enumerate(signals, start=1)
    ]
    blocked = bool(signals or violations)
    return build_repair_proposal_content_validation(
        validated_artifact_id=_attr(envelope, "proposed_patch_envelope_id", "proposed_patch_envelope:v0.38.4"),
        static_findings=findings,
        boundary_violations=violations,
        unsafe_operation_signals=signals,
        blocked=blocked,
        safe_for_future_human_review_packet=not blocked,
        safe_for_future_loop_trial=not blocked,
        requires_review=blocked,
    )


def assess_repair_proposal_safety_risk(
    target_validations: list[RepairProposalTargetValidation],
    content_validations: list[RepairProposalContentValidation],
    policy: RepairProposalSafetyPolicy | None = None,
) -> RepairProposalSafetyRiskAssessment:
    policy = policy or default_repair_proposal_safety_policy()
    risks: list[RepairProposalSafetyRiskKind] = []
    boundary_ids: list[str] = []
    unsafe_ids: list[str] = []
    finding_ids: list[str] = []
    for target in target_validations:
        risks.extend(RepairProposalSafetyRiskKind(item) for item in target.risk_kinds)
    for content in content_validations:
        boundary_ids.extend(violation.boundary_violation_id for violation in content.boundary_violations)
        unsafe_ids.extend(signal.unsafe_signal_id for signal in content.unsafe_operation_signals)
        finding_ids.extend(finding.static_finding_id for finding in content.static_findings)
        for signal in content.unsafe_operation_signals:
            signal_kind = RepairProposalUnsafeOperationKind(signal.unsafe_operation_kind)
            for operation_kind, risk_kind, _tokens in UNSAFE_OPERATION_SPECS:
                if signal_kind == operation_kind:
                    risks.append(risk_kind)
    unique_risks = list(dict.fromkeys(risks))
    critical = any(risk in policy.critical_risk_kinds for risk in unique_risks)
    return build_repair_proposal_safety_risk_assessment(
        risk_kinds=unique_risks,
        severity=RepairProposalSafetySeverity.CRITICAL if critical else (RepairProposalSafetySeverity.LOW if unique_risks else RepairProposalSafetySeverity.INFO),
        boundary_violation_ids=boundary_ids,
        unsafe_signal_ids=unsafe_ids,
        finding_ids=finding_ids,
        blocks_future_loop_trial=critical,
        requires_human_review=bool(unique_risks),
        do_nothing_recommended=bool(unique_risks),
    )


def compare_repair_proposal_safety_to_do_nothing(risk_assessment: RepairProposalSafetyRiskAssessment) -> RepairProposalSafetyDoNothingComparison:
    if risk_assessment.blocks_future_loop_trial:
        return build_repair_proposal_safety_do_nothing_comparison(
            comparison_kind=RepairProposalSafetyDoNothingComparisonKind.DO_NOTHING_REQUIRED_DUE_TO_BLOCKING_VIOLATION,
            comparison_summary="do-nothing is required because a blocking safety violation is present",
            do_nothing_preferred=True,
            do_nothing_required=True,
            proposal_safe_enough_to_review=False,
            confidence=RepairProposalSafetyConfidenceLevel.HIGH,
            evidence_refs=risk_assessment.boundary_violation_ids + risk_assessment.unsafe_signal_ids,
        )
    if risk_assessment.risk_kinds:
        return build_repair_proposal_safety_do_nothing_comparison(
            comparison_kind=RepairProposalSafetyDoNothingComparisonKind.DO_NOTHING_PREFERRED_DUE_TO_SAFETY_RISK,
            comparison_summary="do-nothing is preferred or competitive because safety risk remains",
            do_nothing_preferred=True,
            do_nothing_required=False,
            proposal_safe_enough_to_review=True,
            confidence=RepairProposalSafetyConfidenceLevel.MEDIUM,
            evidence_refs=risk_assessment.finding_ids,
        )
    return build_repair_proposal_safety_do_nothing_comparison()


def decide_repair_proposal_safety(
    risk_assessment: RepairProposalSafetyRiskAssessment,
    do_nothing_comparison: RepairProposalSafetyDoNothingComparison,
) -> RepairProposalSafetyDecision:
    if do_nothing_comparison.do_nothing_required or risk_assessment.blocks_future_loop_trial:
        return build_repair_proposal_safety_decision(
            decision_kind=RepairProposalSafetyDecisionKind.BOUNDARY_VIOLATION_BLOCKED,
            disposition=RepairProposalSafetyDisposition.BLOCKED,
            decision_summary="safety validation blocks future loop trial input",
            rationale_summary="critical boundary or unsafe operation risk remains in proposed metadata",
            ready_for_future_human_review_packet_input=not risk_assessment.blocks_future_human_review_packet,
            ready_for_future_loop_trial_input=False,
            confidence=RepairProposalSafetyConfidenceLevel.HIGH,
            evidence_refs=risk_assessment.boundary_violation_ids + risk_assessment.unsafe_signal_ids,
        )
    if do_nothing_comparison.do_nothing_preferred:
        return build_repair_proposal_safety_decision(
            decision_kind=RepairProposalSafetyDecisionKind.REQUIRE_REVIEW,
            disposition=RepairProposalSafetyDisposition.REVIEW_REQUIRED,
            decision_summary="safety validation requires human review before any future handoff",
            rationale_summary="do-nothing remains preferred or competitive due to warnings",
            ready_for_future_human_review_packet_input=True,
            ready_for_future_loop_trial_input=False,
            confidence=RepairProposalSafetyConfidenceLevel.MEDIUM,
            evidence_refs=risk_assessment.finding_ids,
        )
    return build_repair_proposal_safety_decision()


def create_repair_proposal_safety_report(
    safety_input: RepairProposalSafetyInput,
    proposed_patch_envelope: Any | None,
    policy: RepairProposalSafetyPolicy | None = None,
) -> RepairProposalSafetyReport:
    policy = policy or default_repair_proposal_safety_policy()
    if proposed_patch_envelope is None:
        missing_finding = build_repair_proposal_static_validation_finding(
            rule_kind=RepairProposalStaticRuleKind.REQUIRE_PATCH_ENVELOPE,
            severity=RepairProposalSafetySeverity.CRITICAL,
            finding_summary="patch envelope metadata is missing",
            passed=False,
            blocked=True,
            requires_review=True,
        )
        risk = build_repair_proposal_safety_risk_assessment(
            risk_kinds=[RepairProposalSafetyRiskKind.MISSING_PATCH_ENVELOPE_RISK],
            severity=RepairProposalSafetySeverity.CRITICAL,
            finding_ids=[missing_finding.static_finding_id],
            blocks_future_loop_trial=True,
            requires_human_review=True,
            do_nothing_recommended=True,
        )
        do_nothing = compare_repair_proposal_safety_to_do_nothing(risk)
        decision = decide_repair_proposal_safety(risk, do_nothing)
        return build_repair_proposal_safety_report(
            safety_input_id=safety_input.safety_input_id,
            status=RepairProposalSafetyStatus.VALIDATION_BLOCKED,
            readiness_level=RepairProposalSafetyReadinessLevel.BLOCKED,
            static_findings=[missing_finding],
            risk_assessment=risk,
            do_nothing_comparison=do_nothing,
            safety_decision=decision,
            source_refs=safety_input.source_refs,
            ready_for_future_human_review_packet_input=decision.ready_for_future_human_review_packet_input,
            ready_for_future_loop_trial_input=False,
        )
    paths = [
        str(_attr(change, "target_relative_path", "unknown"))
        for change in list(_attr(proposed_patch_envelope, "file_changes", []) or [])
    ] or [
        str(_attr(diff, "target_relative_path", "unknown"))
        for diff in list(_attr(proposed_patch_envelope, "proposed_diffs", []) or [])
    ]
    target_validations = validate_repair_proposal_targets(paths or ["unknown"], policy)
    content_validation = validate_repair_proposal_content(proposed_patch_envelope, policy)
    risk = assess_repair_proposal_safety_risk(target_validations, [content_validation], policy)
    do_nothing = compare_repair_proposal_safety_to_do_nothing(risk)
    decision = decide_repair_proposal_safety(risk, do_nothing)
    status = RepairProposalSafetyStatus.VALIDATION_COMPLETED if not risk.risk_kinds else RepairProposalSafetyStatus.REVIEW_REQUIRED
    if any(not target.valid_target for target in target_validations):
        status = RepairProposalSafetyStatus.BOUNDARY_VIOLATION_DETECTED
    if content_validation.unsafe_operation_signals:
        status = RepairProposalSafetyStatus.UNSAFE_OPERATION_DETECTED
    return build_repair_proposal_safety_report(
        safety_input_id=safety_input.safety_input_id,
        status=status,
        readiness_level=RepairProposalSafetyReadinessLevel.FUTURE_HUMAN_REVIEW_PACKET_INPUT_READY if decision.ready_for_future_human_review_packet_input else RepairProposalSafetyReadinessLevel.SAFETY_RISK_ASSESSMENT_READY,
        target_validations=target_validations,
        content_validations=[content_validation],
        static_findings=content_validation.static_findings,
        boundary_violations=[violation for validation in [content_validation] for violation in validation.boundary_violations],
        unsafe_operation_signals=content_validation.unsafe_operation_signals,
        risk_assessment=risk,
        do_nothing_comparison=do_nothing,
        safety_decision=decision,
        source_refs=safety_input.source_refs,
        ready_for_future_human_review_packet_input=decision.ready_for_future_human_review_packet_input,
        ready_for_future_loop_trial_input=decision.ready_for_future_loop_trial_input,
    )


def validate_repair_proposal_safety_report(report: RepairProposalSafetyReport) -> RepairProposalSafetyValidationReport:
    return build_repair_proposal_safety_validation_report(safety_report_id=report.safety_report_id)


def repair_proposal_safety_flags_preserve_no_apply(flags: RepairProposalSafetyFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES)


def repair_proposal_safety_policy_blocks_runtime(policy: RepairProposalSafetyPolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_REPAIR_PROPOSAL_SAFETY_POLICY_ALLOW_NAMES)


def repair_proposal_target_validation_is_metadata_only(result: RepairProposalTargetValidation) -> bool:
    return all(getattr(result, name) is False for name in UNSAFE_TARGET_VALIDATION_STATE_NAMES)


def repair_proposal_content_validation_does_not_execute_content(result: RepairProposalContentValidation) -> bool:
    return result.executed_content is False


def repair_proposal_safety_decision_is_not_apply_permission(decision: RepairProposalSafetyDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_SAFETY_DECISION_NOW_NAMES)


def repair_proposal_safety_report_is_not_apply_permission(report: RepairProposalSafetyReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_SAFETY_REPORT_STATE_NAMES)


def v0385_readiness_report_is_not_execution_ready(report: V0385ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPAIR_PROPOSAL_SAFETY_FLAG_NAMES if hasattr(report, name))
