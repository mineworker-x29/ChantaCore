from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .agent_performance_evaluation import create_cold_agent_evaluation_report
from .boundary import _require_non_blank
from .vera_codex_trial import run_vera_codex_one_shot_trial


V0378_VERSION = "v0.37.8"
V0378_RELEASE_NAME = "v0.37.8 CLI Test Runner & Agent Evaluation Surface"


UNSAFE_CLI_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_uncontrolled_subprocess",
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

UNSAFE_CLI_POLICY_ALLOW_NAMES = (
    "allow_direct_subprocess",
    "allow_shell",
    "allow_arbitrary_command",
    "allow_dependency_install",
    "allow_network_access",
    "allow_live_workspace_write",
    "allow_patch_application",
    "allow_workspace_write",
    "allow_code_edit",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_repair_patch_proposal",
    "allow_repair_execution",
    "allow_automatic_repair",
    "allow_retry_loop",
    "allow_multi_cycle_loop",
    "allow_model_provider_invocation",
    "allow_tool_execution",
    "allow_external_agent_execution",
    "allow_claude_code_invocation",
    "allow_codex_cli_invocation",
    "allow_dominion_runtime",
    "allow_persistent_trace_write",
    "allow_ui_runtime",
)

UNSAFE_DECISION_ALLOW_NAMES = (
    "direct_subprocess_allowed",
    "shell_execution_allowed",
    "command_execution_allowed",
    "dependency_install_allowed",
    "network_access_allowed",
    "live_workspace_write_allowed",
    "patch_application_allowed",
    "code_edit_allowed",
    "apply_patch_allowed",
    "git_apply_allowed",
    "repair_patch_proposal_allowed",
    "repair_execution_allowed",
    "automatic_repair_allowed",
    "retry_loop_allowed",
    "multi_cycle_loop_allowed",
    "model_provider_invocation_allowed",
    "tool_execution_allowed",
    "external_agent_execution_allowed",
    "claude_code_invocation_allowed",
    "codex_cli_invocation_allowed",
    "dominion_runtime_allowed",
    "persistent_trace_write_allowed",
    "production_certification_allowed",
)

PROHIBITED_RUNTIME_ACTIONS = (
    "shell",
    "subprocess",
    "command execution",
    "dependency install",
    "network",
    "live workspace write",
    "patch application",
    "apply_patch",
    "git apply",
    "repair",
    "model provider invocation",
    "tool execution",
    "external agent",
    "Dominion",
    "persistent trace",
)

PROHIBITED_ARG_PATTERNS = (
    ";",
    "&&",
    "||",
    "|",
    "`",
    "$(",
    ">",
    "<",
    "shell",
    "bash",
    "powershell",
    "cmd",
    "python",
    "pytest",
    "unittest",
    "npm",
    "pnpm",
    "yarn",
    "pip",
    "poetry",
    "install",
    "network",
    "curl",
    "wget",
    "git apply",
    "apply_patch",
    "apply-patch",
    "live-write",
    "live-apply",
    "code-edit",
    "repair",
    "auto-repair",
    "retry-loop",
    "multi-cycle",
    "provider-call",
    "run-codex",
    "run-claude-code",
    "run-opencode",
    "run-hermes",
    "run-openclaw",
    "external-agent",
    "dominion",
    "infinite-loop",
    "recursive-agent",
)


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_metadata(value: dict[str, Any]) -> None:
    _validate_dict("metadata", value)
    for key in value:
        lowered = str(key).lower()
        if any(marker in lowered for marker in ("secret", "credential", "api_key", "token", ".env")):
            raise ValueError("metadata must not contain credential-like keys")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0378_VERSION not in version:
        raise ValueError("version must include v0.37.8")


def _validate_false(name: str, value: bool) -> None:
    if value is not False:
        raise ValueError(f"{name} must remain False in v0.37.8")


def _validate_true(name: str, value: bool) -> None:
    if value is not True:
        raise ValueError(f"{name} must be True")


def _enum_value(value: Any) -> str:
    return value.value if isinstance(value, StrEnum) else str(value)


def _limit_text(text: Any, limit: int = 1200) -> tuple[str, bool]:
    rendered = str(text)
    if len(rendered) <= limit:
        return rendered, False
    return rendered[:limit], True


def _canonical_command(value: str) -> str:
    return value.strip().lower().replace("_", "-")


def _contains_prohibited_pattern(tokens: list[str], patterns: list[str] | None = None) -> bool:
    joined = " ".join(str(token).lower() for token in tokens)
    return any(pattern.lower() in joined for pattern in (patterns or list(PROHIBITED_ARG_PATTERNS)))


class CLITestRunnerCommandKind(StrEnum):
    TEST_RUN_HELP = "test_run_help"
    TEST_RUN_STATUS = "test_run_status"
    TEST_INVOCATION_PREVIEW = "test_invocation_preview"
    TEST_RUN_SANDBOX = "test_run_sandbox"
    TEST_RESULT_SUMMARY = "test_result_summary"
    FEEDBACK_REPORT = "feedback_report"
    REPAIR_SUGGESTION_PREVIEW = "repair_suggestion_preview"
    VERA_TRIAL_PREVIEW = "vera_trial_preview"
    VERA_TRIAL_RUN_ONCE = "vera_trial_run_once"
    COLD_SCORECARD = "cold_scorecard"
    EVALUATION_BUNDLE_PREVIEW = "evaluation_bundle_preview"
    DENIED_SHELL = "denied_shell"
    DENIED_DIRECT_PYTEST = "denied_direct_pytest"
    DENIED_DIRECT_UNITTEST = "denied_direct_unittest"
    DENIED_PACKAGE_SCRIPT = "denied_package_script"
    DENIED_DEPENDENCY_INSTALL = "denied_dependency_install"
    DENIED_NETWORK_COMMAND = "denied_network_command"
    DENIED_LIVE_WORKSPACE_COMMAND = "denied_live_workspace_command"
    DENIED_APPLY_PATCH = "denied_apply_patch"
    DENIED_GIT_APPLY = "denied_git_apply"
    DENIED_REPAIR_EXECUTION = "denied_repair_execution"
    DENIED_EXTERNAL_AGENT = "denied_external_agent"
    DENIED_MODEL_PROVIDER = "denied_model_provider"
    DENIED_DOMINION = "denied_dominion"
    DENIED_MULTI_CYCLE = "denied_multi_cycle"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLITestRunnerCommandMode(StrEnum):
    HELP = "help"
    STATUS = "status"
    INVOCATION_PREVIEW = "invocation_preview"
    SANDBOX_TEST_RUN = "sandbox_test_run"
    RESULT_SUMMARY = "result_summary"
    FEEDBACK_REPORT = "feedback_report"
    REPAIR_SUGGESTION_PREVIEW = "repair_suggestion_preview"
    VERA_TRIAL_PREVIEW = "vera_trial_preview"
    VERA_TRIAL_RUN_ONCE = "vera_trial_run_once"
    COLD_SCORECARD = "cold_scorecard"
    EVALUATION_BUNDLE_PREVIEW = "evaluation_bundle_preview"
    DENIED = "denied"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLITestRunnerInputSourceKind(StrEnum):
    ARGV_LIST = "argv_list"
    PARSED_ARGS = "parsed_args"
    RUNTIME_CONTEXT = "runtime_context"
    SANDBOX_ROOT_ARG = "sandbox_root_arg"
    INVOCATION_CONTRACT_REF = "invocation_contract_ref"
    TEST_EXECUTION_RESULT_REF = "test_execution_result_ref"
    TEST_RESULT_ENVELOPE_REF = "test_result_envelope_ref"
    FEEDBACK_REPORT_REF = "feedback_report_ref"
    REPAIR_SUGGESTION_REF = "repair_suggestion_ref"
    VERA_TRIAL_PACKET_REF = "vera_trial_packet_ref"
    COLD_EVALUATION_REPORT_REF = "cold_evaluation_report_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class CLITestRunnerSurfaceStatus(StrEnum):
    UNKNOWN = "unknown"
    INITIALIZED = "initialized"
    PARSED = "parsed"
    DECISION_READY = "decision_ready"
    ALLOWED = "allowed"
    DENIED = "denied"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"
    FUTURE_GATED = "future_gated"


class CLITestRunnerDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_INVOCATION_PREVIEW = "allow_invocation_preview"
    ALLOW_SANDBOX_TEST_RUN = "allow_sandbox_test_run"
    ALLOW_RESULT_SUMMARY = "allow_result_summary"
    ALLOW_FEEDBACK_REPORT = "allow_feedback_report"
    ALLOW_REPAIR_SUGGESTION_PREVIEW = "allow_repair_suggestion_preview"
    ALLOW_VERA_TRIAL_PREVIEW = "allow_vera_trial_preview"
    ALLOW_VERA_TRIAL_RUN_ONCE = "allow_vera_trial_run_once"
    ALLOW_COLD_SCORECARD = "allow_cold_scorecard"
    ALLOW_EVALUATION_BUNDLE_PREVIEW = "allow_evaluation_bundle_preview"
    DENY_SHELL = "deny_shell"
    DENY_DIRECT_PYTEST = "deny_direct_pytest"
    DENY_DIRECT_UNITTEST = "deny_direct_unittest"
    DENY_PACKAGE_SCRIPT = "deny_package_script"
    DENY_DEPENDENCY_INSTALL = "deny_dependency_install"
    DENY_NETWORK = "deny_network"
    DENY_LIVE_WORKSPACE = "deny_live_workspace"
    DENY_APPLY_PATCH = "deny_apply_patch"
    DENY_GIT_APPLY = "deny_git_apply"
    DENY_REPAIR_EXECUTION = "deny_repair_execution"
    DENY_EXTERNAL_AGENT = "deny_external_agent"
    DENY_MODEL_PROVIDER = "deny_model_provider"
    DENY_DOMINION = "deny_dominion"
    DENY_MULTI_CYCLE = "deny_multi_cycle"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class CLITestRunnerOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    STRUCTURED_ARTIFACT = "structured_artifact"
    DEBUG_SUMMARY = "debug_summary"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class CLITestRunnerRiskKind(StrEnum):
    SHELL_INJECTION_RISK = "shell_injection_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    DIRECT_PYTEST_RISK = "direct_pytest_risk"
    PACKAGE_SCRIPT_RISK = "package_script_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    LIVE_CODE_EDIT_RISK = "live_code_edit_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    REPAIR_EXECUTION_RISK = "repair_execution_risk"
    REPAIR_PATCH_GENERATION_RISK = "repair_patch_generation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    CODEX_CLI_INVOCATION_RISK = "codex_cli_invocation_risk"
    CLAUDE_CODE_INVOCATION_RISK = "claude_code_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DIRECT_PROVIDER_INVOCATION_RISK = "direct_provider_invocation_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_READ_RISK = "secret_read_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class CLITestRunnerReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_CONTRACT_READY = "cli_contract_ready"
    BOUNDED_CLI_TEST_RUNNER_SURFACE_READY = "bounded_cli_test_runner_surface_ready"
    BOUNDED_PREVIEW_DISPATCH_READY = "bounded_preview_dispatch_ready"
    BOUNDED_SANDBOX_TEST_RUN_DISPATCH_READY = "bounded_sandbox_test_run_dispatch_ready"
    BOUNDED_AGENT_EVALUATION_DISPATCH_READY = "bounded_agent_evaluation_dispatch_ready"
    DESIGN_HANDOFF_READY_FOR_V0379 = "design_handoff_ready_for_v0379"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


SAFE_COMMAND_MAP: dict[str, tuple[CLITestRunnerCommandKind, CLITestRunnerCommandMode, CLITestRunnerDecisionKind]] = {
    "test-run-help": (CLITestRunnerCommandKind.TEST_RUN_HELP, CLITestRunnerCommandMode.HELP, CLITestRunnerDecisionKind.ALLOW_HELP),
    "help": (CLITestRunnerCommandKind.TEST_RUN_HELP, CLITestRunnerCommandMode.HELP, CLITestRunnerDecisionKind.ALLOW_HELP),
    "test-run-status": (CLITestRunnerCommandKind.TEST_RUN_STATUS, CLITestRunnerCommandMode.STATUS, CLITestRunnerDecisionKind.ALLOW_STATUS),
    "status": (CLITestRunnerCommandKind.TEST_RUN_STATUS, CLITestRunnerCommandMode.STATUS, CLITestRunnerDecisionKind.ALLOW_STATUS),
    "test-invocation-preview": (CLITestRunnerCommandKind.TEST_INVOCATION_PREVIEW, CLITestRunnerCommandMode.INVOCATION_PREVIEW, CLITestRunnerDecisionKind.ALLOW_INVOCATION_PREVIEW),
    "test-run-sandbox": (CLITestRunnerCommandKind.TEST_RUN_SANDBOX, CLITestRunnerCommandMode.SANDBOX_TEST_RUN, CLITestRunnerDecisionKind.ALLOW_SANDBOX_TEST_RUN),
    "test-result-summary": (CLITestRunnerCommandKind.TEST_RESULT_SUMMARY, CLITestRunnerCommandMode.RESULT_SUMMARY, CLITestRunnerDecisionKind.ALLOW_RESULT_SUMMARY),
    "feedback-report": (CLITestRunnerCommandKind.FEEDBACK_REPORT, CLITestRunnerCommandMode.FEEDBACK_REPORT, CLITestRunnerDecisionKind.ALLOW_FEEDBACK_REPORT),
    "repair-suggestion-preview": (CLITestRunnerCommandKind.REPAIR_SUGGESTION_PREVIEW, CLITestRunnerCommandMode.REPAIR_SUGGESTION_PREVIEW, CLITestRunnerDecisionKind.ALLOW_REPAIR_SUGGESTION_PREVIEW),
    "vera-trial-preview": (CLITestRunnerCommandKind.VERA_TRIAL_PREVIEW, CLITestRunnerCommandMode.VERA_TRIAL_PREVIEW, CLITestRunnerDecisionKind.ALLOW_VERA_TRIAL_PREVIEW),
    "vera-trial-run-once": (CLITestRunnerCommandKind.VERA_TRIAL_RUN_ONCE, CLITestRunnerCommandMode.VERA_TRIAL_RUN_ONCE, CLITestRunnerDecisionKind.ALLOW_VERA_TRIAL_RUN_ONCE),
    "cold-scorecard": (CLITestRunnerCommandKind.COLD_SCORECARD, CLITestRunnerCommandMode.COLD_SCORECARD, CLITestRunnerDecisionKind.ALLOW_COLD_SCORECARD),
    "evaluation-bundle-preview": (CLITestRunnerCommandKind.EVALUATION_BUNDLE_PREVIEW, CLITestRunnerCommandMode.EVALUATION_BUNDLE_PREVIEW, CLITestRunnerDecisionKind.ALLOW_EVALUATION_BUNDLE_PREVIEW),
    "no-op": (CLITestRunnerCommandKind.NO_OP, CLITestRunnerCommandMode.NO_OP, CLITestRunnerDecisionKind.NO_OP),
}

DENIED_COMMAND_MAP: dict[str, tuple[CLITestRunnerCommandKind, CLITestRunnerDecisionKind, CLITestRunnerRiskKind]] = {
    "shell": (CLITestRunnerCommandKind.DENIED_SHELL, CLITestRunnerDecisionKind.DENY_SHELL, CLITestRunnerRiskKind.SHELL_INJECTION_RISK),
    "bash": (CLITestRunnerCommandKind.DENIED_SHELL, CLITestRunnerDecisionKind.DENY_SHELL, CLITestRunnerRiskKind.SHELL_INJECTION_RISK),
    "powershell": (CLITestRunnerCommandKind.DENIED_SHELL, CLITestRunnerDecisionKind.DENY_SHELL, CLITestRunnerRiskKind.SHELL_INJECTION_RISK),
    "cmd": (CLITestRunnerCommandKind.DENIED_SHELL, CLITestRunnerDecisionKind.DENY_SHELL, CLITestRunnerRiskKind.SHELL_INJECTION_RISK),
    "python": (CLITestRunnerCommandKind.DENIED_SHELL, CLITestRunnerDecisionKind.DENY_SHELL, CLITestRunnerRiskKind.COMMAND_EXECUTION_RISK),
    "pytest": (CLITestRunnerCommandKind.DENIED_DIRECT_PYTEST, CLITestRunnerDecisionKind.DENY_DIRECT_PYTEST, CLITestRunnerRiskKind.DIRECT_PYTEST_RISK),
    "unittest": (CLITestRunnerCommandKind.DENIED_DIRECT_UNITTEST, CLITestRunnerDecisionKind.DENY_DIRECT_UNITTEST, CLITestRunnerRiskKind.DIRECT_PYTEST_RISK),
    "npm": (CLITestRunnerCommandKind.DENIED_PACKAGE_SCRIPT, CLITestRunnerDecisionKind.DENY_PACKAGE_SCRIPT, CLITestRunnerRiskKind.PACKAGE_SCRIPT_RISK),
    "npm-test": (CLITestRunnerCommandKind.DENIED_PACKAGE_SCRIPT, CLITestRunnerDecisionKind.DENY_PACKAGE_SCRIPT, CLITestRunnerRiskKind.PACKAGE_SCRIPT_RISK),
    "pnpm": (CLITestRunnerCommandKind.DENIED_PACKAGE_SCRIPT, CLITestRunnerDecisionKind.DENY_PACKAGE_SCRIPT, CLITestRunnerRiskKind.PACKAGE_SCRIPT_RISK),
    "yarn": (CLITestRunnerCommandKind.DENIED_PACKAGE_SCRIPT, CLITestRunnerDecisionKind.DENY_PACKAGE_SCRIPT, CLITestRunnerRiskKind.PACKAGE_SCRIPT_RISK),
    "pip": (CLITestRunnerCommandKind.DENIED_DEPENDENCY_INSTALL, CLITestRunnerDecisionKind.DENY_DEPENDENCY_INSTALL, CLITestRunnerRiskKind.DEPENDENCY_INSTALL_RISK),
    "poetry": (CLITestRunnerCommandKind.DENIED_DEPENDENCY_INSTALL, CLITestRunnerDecisionKind.DENY_DEPENDENCY_INSTALL, CLITestRunnerRiskKind.DEPENDENCY_INSTALL_RISK),
    "install": (CLITestRunnerCommandKind.DENIED_DEPENDENCY_INSTALL, CLITestRunnerDecisionKind.DENY_DEPENDENCY_INSTALL, CLITestRunnerRiskKind.DEPENDENCY_INSTALL_RISK),
    "dependency-install": (CLITestRunnerCommandKind.DENIED_DEPENDENCY_INSTALL, CLITestRunnerDecisionKind.DENY_DEPENDENCY_INSTALL, CLITestRunnerRiskKind.DEPENDENCY_INSTALL_RISK),
    "network": (CLITestRunnerCommandKind.DENIED_NETWORK_COMMAND, CLITestRunnerDecisionKind.DENY_NETWORK, CLITestRunnerRiskKind.NETWORK_ACCESS_RISK),
    "curl": (CLITestRunnerCommandKind.DENIED_NETWORK_COMMAND, CLITestRunnerDecisionKind.DENY_NETWORK, CLITestRunnerRiskKind.NETWORK_ACCESS_RISK),
    "wget": (CLITestRunnerCommandKind.DENIED_NETWORK_COMMAND, CLITestRunnerDecisionKind.DENY_NETWORK, CLITestRunnerRiskKind.NETWORK_ACCESS_RISK),
    "git": (CLITestRunnerCommandKind.DENIED_GIT_APPLY, CLITestRunnerDecisionKind.DENY_GIT_APPLY, CLITestRunnerRiskKind.GIT_APPLY_RISK),
    "git-apply": (CLITestRunnerCommandKind.DENIED_GIT_APPLY, CLITestRunnerDecisionKind.DENY_GIT_APPLY, CLITestRunnerRiskKind.GIT_APPLY_RISK),
    "apply-patch": (CLITestRunnerCommandKind.DENIED_APPLY_PATCH, CLITestRunnerDecisionKind.DENY_APPLY_PATCH, CLITestRunnerRiskKind.APPLY_PATCH_RISK),
    "apply_patch": (CLITestRunnerCommandKind.DENIED_APPLY_PATCH, CLITestRunnerDecisionKind.DENY_APPLY_PATCH, CLITestRunnerRiskKind.APPLY_PATCH_RISK),
    "live-test": (CLITestRunnerCommandKind.DENIED_LIVE_WORKSPACE_COMMAND, CLITestRunnerDecisionKind.DENY_LIVE_WORKSPACE, CLITestRunnerRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "live-apply": (CLITestRunnerCommandKind.DENIED_LIVE_WORKSPACE_COMMAND, CLITestRunnerDecisionKind.DENY_LIVE_WORKSPACE, CLITestRunnerRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "live-write": (CLITestRunnerCommandKind.DENIED_LIVE_WORKSPACE_COMMAND, CLITestRunnerDecisionKind.DENY_LIVE_WORKSPACE, CLITestRunnerRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "edit-live": (CLITestRunnerCommandKind.DENIED_LIVE_WORKSPACE_COMMAND, CLITestRunnerDecisionKind.DENY_LIVE_WORKSPACE, CLITestRunnerRiskKind.LIVE_CODE_EDIT_RISK),
    "workspace-write": (CLITestRunnerCommandKind.DENIED_LIVE_WORKSPACE_COMMAND, CLITestRunnerDecisionKind.DENY_LIVE_WORKSPACE, CLITestRunnerRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "code-edit": (CLITestRunnerCommandKind.DENIED_LIVE_WORKSPACE_COMMAND, CLITestRunnerDecisionKind.DENY_LIVE_WORKSPACE, CLITestRunnerRiskKind.LIVE_CODE_EDIT_RISK),
    "repair": (CLITestRunnerCommandKind.DENIED_REPAIR_EXECUTION, CLITestRunnerDecisionKind.DENY_REPAIR_EXECUTION, CLITestRunnerRiskKind.REPAIR_EXECUTION_RISK),
    "auto-repair": (CLITestRunnerCommandKind.DENIED_REPAIR_EXECUTION, CLITestRunnerDecisionKind.DENY_REPAIR_EXECUTION, CLITestRunnerRiskKind.AUTOMATIC_REPAIR_RISK),
    "repair-loop": (CLITestRunnerCommandKind.DENIED_MULTI_CYCLE, CLITestRunnerDecisionKind.DENY_MULTI_CYCLE, CLITestRunnerRiskKind.MULTI_CYCLE_LOOP_RISK),
    "retry-loop": (CLITestRunnerCommandKind.DENIED_MULTI_CYCLE, CLITestRunnerDecisionKind.DENY_MULTI_CYCLE, CLITestRunnerRiskKind.MULTI_CYCLE_LOOP_RISK),
    "multi-cycle": (CLITestRunnerCommandKind.DENIED_MULTI_CYCLE, CLITestRunnerDecisionKind.DENY_MULTI_CYCLE, CLITestRunnerRiskKind.MULTI_CYCLE_LOOP_RISK),
    "run-codex": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.CODEX_CLI_INVOCATION_RISK),
    "run-claude-code": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.CLAUDE_CODE_INVOCATION_RISK),
    "run-opencode": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "run-hermes": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "run-openclaw": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "external-agent": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "external-agent-loop": (CLITestRunnerCommandKind.DENIED_EXTERNAL_AGENT, CLITestRunnerDecisionKind.DENY_EXTERNAL_AGENT, CLITestRunnerRiskKind.INFINITE_AGENT_LOOP_RISK),
    "dominion": (CLITestRunnerCommandKind.DENIED_DOMINION, CLITestRunnerDecisionKind.DENY_DOMINION, CLITestRunnerRiskKind.DOMINION_RUNTIME_RISK),
    "infinite-loop": (CLITestRunnerCommandKind.DENIED_MULTI_CYCLE, CLITestRunnerDecisionKind.DENY_MULTI_CYCLE, CLITestRunnerRiskKind.INFINITE_AGENT_LOOP_RISK),
    "recursive-agent": (CLITestRunnerCommandKind.DENIED_MULTI_CYCLE, CLITestRunnerDecisionKind.DENY_MULTI_CYCLE, CLITestRunnerRiskKind.INFINITE_AGENT_LOOP_RISK),
    "provider-call": (CLITestRunnerCommandKind.DENIED_MODEL_PROVIDER, CLITestRunnerDecisionKind.DENY_MODEL_PROVIDER, CLITestRunnerRiskKind.MODEL_PROVIDER_INVOCATION_RISK),
}


@dataclass(frozen=True)
class CLITestRunnerFlagSet:
    flag_set_id: str = "cli-test-runner-flags:v0378"
    version: str = V0378_VERSION
    cli_test_runner_surface_constructed: bool = True
    cli_argument_parsing_enabled: bool = True
    bounded_preview_dispatch_enabled: bool = True
    bounded_sandbox_test_dispatch_enabled: bool = True
    bounded_agent_evaluation_dispatch_enabled: bool = True
    denied_unsafe_command_handling_enabled: bool = True
    ready_for_v0379_controlled_sandbox_test_runner_consolidation: bool = True
    ready_for_cli_test_runner_surface: bool = True
    ready_for_cli_test_invocation_preview: bool = True
    ready_for_cli_sandbox_test_run: bool = True
    ready_for_cli_test_result_summary: bool = True
    ready_for_cli_feedback_report: bool = True
    ready_for_cli_repair_suggestion_preview: bool = True
    ready_for_cli_vera_trial_preview: bool = True
    ready_for_cli_vera_trial_run_once: bool = True
    ready_for_cli_cold_scorecard: bool = True
    ready_for_cli_evaluation_bundle_preview: bool = True
    ready_for_cli_controlled_test_execution_dispatch: bool = True
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_uncontrolled_subprocess: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_repair_patch_proposal: bool = False
    ready_for_repair_diff_generation: bool = False
    ready_for_code_hunk_generation: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_execution: bool = False
    ready_for_repair_loop: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
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
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
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
        _validate_metadata(self.metadata)
        for name in UNSAFE_CLI_FLAG_NAMES:
            _validate_false(name, getattr(self, name))


@dataclass(frozen=True)
class CLITestRunnerSourceRef:
    source_ref_id: str
    source_kind: CLITestRunnerInputSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerArgumentSpec:
    argument_spec_id: str
    name: str
    required: bool = False
    allowed_values: list[str] = field(default_factory=list)
    prohibited_values: list[str] = field(default_factory=list)
    allowed_patterns: list[str] = field(default_factory=list)
    prohibited_patterns: list[str] = field(default_factory=lambda: list(PROHIBITED_ARG_PATTERNS))
    allow_text_value: bool = True
    allow_ref_value: bool = True
    allow_json_value: bool = False
    max_value_chars: int = 400
    description: str = "bounded CLI argument metadata"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("argument_spec_id", self.argument_spec_id)
        _require_non_blank("name", self.name)
        _require_non_blank("description", self.description)
        for name in ("allowed_values", "prohibited_values", "allowed_patterns", "prohibited_patterns"):
            _validate_list(name, getattr(self, name))
        if self.max_value_chars < 0:
            raise ValueError("max_value_chars must be >= 0")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerCommandSpec:
    command_spec_id: str
    command_kind: CLITestRunnerCommandKind | str
    command_mode: CLITestRunnerCommandMode | str
    command_name: str
    description: str
    argument_specs: list[CLITestRunnerArgumentSpec] = field(default_factory=list)
    allowed_output_formats: list[CLITestRunnerOutputFormat | str] = field(default_factory=lambda: [CLITestRunnerOutputFormat.TEXT, CLITestRunnerOutputFormat.JSON])
    allowed_decisions: list[CLITestRunnerDecisionKind | str] = field(default_factory=list)
    risk_kinds: list[CLITestRunnerRiskKind | str] = field(default_factory=list)
    dispatch_target: str | None = None
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        _require_non_blank("command_name", self.command_name)
        _require_non_blank("description", self.description)
        for name in ("argument_specs", "allowed_output_formats", "allowed_decisions", "risk_kinds"):
            _validate_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerSurfacePolicy:
    policy_id: str = "cli-test-runner-policy:v0378"
    version: str = V0378_VERSION
    allowed_command_kinds: list[CLITestRunnerCommandKind | str] = field(default_factory=list)
    blocked_command_kinds: list[CLITestRunnerCommandKind | str] = field(default_factory=list)
    allowed_output_formats: list[CLITestRunnerOutputFormat | str] = field(default_factory=lambda: [CLITestRunnerOutputFormat.TEXT, CLITestRunnerOutputFormat.MARKDOWN, CLITestRunnerOutputFormat.JSON, CLITestRunnerOutputFormat.STRUCTURED_ARTIFACT])
    prohibited_arg_patterns: list[str] = field(default_factory=lambda: list(PROHIBITED_ARG_PATTERNS))
    max_arg_chars: int = 400
    allow_help: bool = True
    allow_status: bool = True
    allow_invocation_preview: bool = True
    allow_sandbox_test_run: bool = True
    allow_result_summary: bool = True
    allow_feedback_report: bool = True
    allow_repair_suggestion_preview: bool = True
    allow_vera_trial_preview: bool = True
    allow_vera_trial_run_once: bool = True
    allow_cold_scorecard: bool = True
    allow_evaluation_bundle_preview: bool = True
    allow_controlled_test_execution_dispatch: bool = True
    allow_direct_subprocess: bool = False
    allow_shell: bool = False
    allow_arbitrary_command: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_repair_patch_proposal: bool = False
    allow_repair_execution: bool = False
    allow_automatic_repair: bool = False
    allow_retry_loop: bool = False
    allow_multi_cycle_loop: bool = False
    allow_model_provider_invocation: bool = False
    allow_tool_execution: bool = False
    allow_external_agent_execution: bool = False
    allow_claude_code_invocation: bool = False
    allow_codex_cli_invocation: bool = False
    allow_dominion_runtime: bool = False
    allow_persistent_trace_write: bool = False
    allow_ui_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        for name in ("allowed_command_kinds", "blocked_command_kinds", "allowed_output_formats", "prohibited_arg_patterns"):
            _validate_list(name, getattr(self, name))
        if self.max_arg_chars < 0:
            raise ValueError("max_arg_chars must be >= 0")
        missing = [pattern for pattern in ("shell", "pytest", "install", "network", "apply_patch", "git apply", "repair", "provider-call", "dominion") if pattern not in self.prohibited_arg_patterns]
        if missing:
            raise ValueError("prohibited_arg_patterns must include core unsafe CLI patterns")
        for name in UNSAFE_CLI_POLICY_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerSurface:
    cli_surface_id: str = "cli-test-runner-surface:v0378"
    version: str = V0378_VERSION
    command_specs: list[CLITestRunnerCommandSpec] = field(default_factory=list)
    policy: CLITestRunnerSurfacePolicy = field(default_factory=lambda: CLITestRunnerSurfacePolicy())
    flags: CLITestRunnerFlagSet = field(default_factory=lambda: CLITestRunnerFlagSet())
    status: CLITestRunnerSurfaceStatus | str = CLITestRunnerSurfaceStatus.INITIALIZED
    readiness_level: CLITestRunnerReadinessLevel | str = CLITestRunnerReadinessLevel.BOUNDED_CLI_TEST_RUNNER_SURFACE_READY
    summary: str = "bounded CLI test runner and agent evaluation surface metadata"
    ready_for_cli_test_runner_surface: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_surface_id", self.cli_surface_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        _validate_list("command_specs", self.command_specs)
        if not cli_test_runner_flags_preserve_unsafe_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        _validate_false("ready_for_execution", self.ready_for_execution)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerRuntimeContext:
    runtime_context_id: str = "cli-runtime-context:v0378"
    has_invocation_contract: bool = False
    has_test_execution_result: bool = False
    has_test_result_envelope: bool = False
    has_feedback_report: bool = False
    has_repair_suggestion: bool = False
    has_vera_trial_packet: bool = False
    has_cold_evaluation_report: bool = False
    sandbox_root_ref: str | None = None
    context_summary: str = "bounded in-memory CLI runtime context"
    allows_controlled_test_execution_dispatch: bool = False
    allows_result_summary: bool = False
    allows_feedback_report: bool = False
    allows_repair_suggestion_preview: bool = False
    allows_vera_trial_run_once: bool = False
    allows_cold_scorecard: bool = False
    allows_direct_subprocess: bool = False
    allows_shell: bool = False
    allows_dependency_install: bool = False
    allows_network_access: bool = False
    allows_live_workspace_write: bool = False
    allows_repair_execution: bool = False
    allows_model_provider_invocation: bool = False
    allows_external_agent_execution: bool = False
    allows_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("runtime_context_id", self.runtime_context_id)
        _require_non_blank("context_summary", self.context_summary)
        if self.allows_controlled_test_execution_dispatch and not (self.has_invocation_contract and self.sandbox_root_ref):
            raise ValueError("controlled dispatch requires invocation contract and sandbox root ref")
        for name in (
            "allows_direct_subprocess",
            "allows_shell",
            "allows_dependency_install",
            "allows_network_access",
            "allows_live_workspace_write",
            "allows_repair_execution",
            "allows_model_provider_invocation",
            "allows_external_agent_execution",
            "allows_dominion_runtime",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerInvocation:
    invocation_id: str
    argv: list[str]
    command_kind: CLITestRunnerCommandKind | str
    command_mode: CLITestRunnerCommandMode | str
    parsed_args: dict[str, Any] = field(default_factory=dict)
    requested_output_format: CLITestRunnerOutputFormat | str = CLITestRunnerOutputFormat.TEXT
    source_refs: list[CLITestRunnerSourceRef] = field(default_factory=list)
    invocation_summary: str = "bounded CLI invocation metadata"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("invocation_summary", self.invocation_summary)
        _validate_list("argv", self.argv)
        _validate_dict("parsed_args", self.parsed_args)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerInvocationDecision:
    decision_id: str
    invocation_id: str
    decision_kind: CLITestRunnerDecisionKind | str
    reason: str
    risk_kinds: list[CLITestRunnerRiskKind | str] = field(default_factory=list)
    allowed_command_kind: CLITestRunnerCommandKind | str | None = None
    bounded_preview_allowed: bool = False
    controlled_test_execution_dispatch_allowed: bool = False
    result_summary_allowed: bool = False
    feedback_report_allowed: bool = False
    repair_suggestion_preview_allowed: bool = False
    vera_trial_run_once_allowed: bool = False
    cold_scorecard_allowed: bool = False
    direct_subprocess_allowed: bool = False
    shell_execution_allowed: bool = False
    command_execution_allowed: bool = False
    dependency_install_allowed: bool = False
    network_access_allowed: bool = False
    live_workspace_write_allowed: bool = False
    patch_application_allowed: bool = False
    code_edit_allowed: bool = False
    apply_patch_allowed: bool = False
    git_apply_allowed: bool = False
    repair_patch_proposal_allowed: bool = False
    repair_execution_allowed: bool = False
    automatic_repair_allowed: bool = False
    retry_loop_allowed: bool = False
    multi_cycle_loop_allowed: bool = False
    model_provider_invocation_allowed: bool = False
    tool_execution_allowed: bool = False
    external_agent_execution_allowed: bool = False
    claude_code_invocation_allowed: bool = False
    codex_cli_invocation_allowed: bool = False
    dominion_runtime_allowed: bool = False
    persistent_trace_write_allowed: bool = False
    production_certification_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("reason", self.reason)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_list("evidence_refs", self.evidence_refs)
        for name in UNSAFE_DECISION_ALLOW_NAMES:
            _validate_false(name, getattr(self, name))
        if self.controlled_test_execution_dispatch_allowed and _enum_value(self.allowed_command_kind) != CLITestRunnerCommandKind.TEST_RUN_SANDBOX.value:
            raise ValueError("controlled dispatch is allowed only for test_run_sandbox")
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerDeniedCommand:
    denied_command_id: str
    invocation_id: str | None
    decision_id: str | None
    command_kind: CLITestRunnerCommandKind | str
    risk_kinds: list[CLITestRunnerRiskKind | str]
    reason: str
    safe_alternatives: list[str] = field(default_factory=lambda: ["test-run-help", "test-invocation-preview", "no-op"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_command_id", self.denied_command_id)
        _require_non_blank("reason", self.reason)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerCommandResult:
    command_result_id: str
    invocation_id: str
    decision_id: str
    command_kind: CLITestRunnerCommandKind | str
    status: CLITestRunnerSurfaceStatus | str
    invocation_contract_ref: str | None = None
    test_execution_result_ref: str | None = None
    result_envelope_ref: str | None = None
    feedback_report_ref: str | None = None
    repair_suggestion_ref: str | None = None
    vera_trial_packet_ref: str | None = None
    cold_evaluation_report_ref: str | None = None
    structured_result: dict[str, Any] = field(default_factory=dict)
    text_summary: str = "bounded CLI command result"
    redacted: bool = True
    truncated: bool = False
    controlled_test_execution_dispatched: bool = False
    direct_subprocess_used: bool = False
    shell_used: bool = False
    dependency_install_performed: bool = False
    network_access_allowed: bool = False
    live_write_performed: bool = False
    repair_performed: bool = False
    model_invocation_performed: bool = False
    external_agent_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_result_id", self.command_result_id)
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("text_summary", self.text_summary)
        _validate_dict("structured_result", self.structured_result)
        if self.controlled_test_execution_dispatched and _enum_value(self.command_kind) != CLITestRunnerCommandKind.TEST_RUN_SANDBOX.value:
            raise ValueError("controlled dispatch result is allowed only for test_run_sandbox")
        for name in (
            "direct_subprocess_used",
            "shell_used",
            "dependency_install_performed",
            "network_access_allowed",
            "live_write_performed",
            "repair_performed",
            "model_invocation_performed",
            "external_agent_invoked",
            "production_certified",
            "ready_for_execution",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerRunOutput:
    run_output_id: str
    invocation_id: str
    command_result: CLITestRunnerCommandResult | None
    denied_command: CLITestRunnerDeniedCommand | None
    rendered_output: str
    output_format: CLITestRunnerOutputFormat | str
    status: CLITestRunnerSurfaceStatus | str
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_output_id", self.run_output_id)
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("rendered_output", self.rendered_output)
        _require_non_blank("summary", self.summary)
        _validate_false("ready_for_execution", self.ready_for_execution)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerRunReport:
    run_report_id: str = "cli-run-report:v0378"
    version: str = V0378_VERSION
    invocation_id: str = "invocation:v0378"
    run_output: CLITestRunnerRunOutput | None = None
    status: CLITestRunnerSurfaceStatus | str = CLITestRunnerSurfaceStatus.COMPLETED
    summary: str = "bounded CLI run report"
    controlled_test_execution_dispatched: bool = False
    direct_subprocess_used: bool = False
    shell_used: bool = False
    dependency_install_performed: bool = False
    network_access_allowed: bool = False
    live_write_performed: bool = False
    repair_performed: bool = False
    model_invocation_performed: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    persistent_trace_written: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_report_id", self.run_report_id)
        _validate_version(self.version)
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("summary", self.summary)
        for name in (
            "direct_subprocess_used",
            "shell_used",
            "dependency_install_performed",
            "network_access_allowed",
            "live_write_performed",
            "repair_performed",
            "model_invocation_performed",
            "external_agent_invoked",
            "dominion_runtime_invoked",
            "persistent_trace_written",
            "production_certified",
            "ready_for_execution",
        ):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerRunPreview:
    run_preview_id: str = "cli-run-preview:v0378"
    version: str = V0378_VERSION
    command_kind: CLITestRunnerCommandKind | str = CLITestRunnerCommandKind.TEST_RUN_HELP
    preview_summary: str = "bounded CLI preview metadata"
    safe_to_render_in_memory: bool = True
    will_write_files: bool = False
    will_use_shell: bool = False
    will_use_direct_subprocess: bool = False
    will_invoke_provider: bool = False
    will_invoke_external_agent: bool = False
    will_apply_patch: bool = False
    will_execute_repair: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_true("safe_to_render_in_memory", self.safe_to_render_in_memory)
        for name in ("will_write_files", "will_use_shell", "will_use_direct_subprocess", "will_invoke_provider", "will_invoke_external_agent", "will_apply_patch", "will_execute_repair"):
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class CLITestRunnerNoUnsafeSideEffectGuarantee:
    guarantee_id: str = "cli-no-unsafe-side-effect-guarantee:v0378"
    version: str = V0378_VERSION
    no_shell_execution: bool = True
    no_direct_subprocess: bool = True
    no_uncontrolled_subprocess: bool = True
    no_arbitrary_command_execution: bool = True
    no_dependency_install: bool = True
    no_network_access: bool = True
    no_live_workspace_write: bool = True
    no_live_code_edit: bool = True
    no_patch_application: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_repair_patch_generation: bool = True
    no_automatic_repair: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_model_provider_invocation: bool = True
    no_tool_execution: bool = True
    no_external_agent_execution: bool = True
    no_dominion_runtime: bool = True
    no_persistent_trace_write: bool = True
    no_ui_runtime: bool = True
    no_authority_grant: bool = True
    no_controlled_test_dispatch: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name, value in self.__dict__.items():
            if name.startswith("no_") and name != "no_controlled_test_dispatch":
                _validate_true(name, value)
        _validate_metadata(self.metadata)


@dataclass(frozen=True)
class V0378ReadinessReport:
    readiness_report_id: str = "readiness:v0378-cli-test-runner-surface"
    version: str = V0378_VERSION
    release_name: str = V0378_RELEASE_NAME
    readiness_level: CLITestRunnerReadinessLevel | str = CLITestRunnerReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0379
    ready_for_v0379_controlled_sandbox_test_runner_consolidation: bool = True
    ready_for_cli_test_runner_surface: bool = True
    ready_for_cli_test_invocation_preview: bool = True
    ready_for_cli_sandbox_test_run: bool = True
    ready_for_cli_test_result_summary: bool = True
    ready_for_cli_feedback_report: bool = True
    ready_for_cli_repair_suggestion_preview: bool = True
    ready_for_cli_vera_trial_preview: bool = True
    ready_for_cli_vera_trial_run_once: bool = True
    ready_for_cli_cold_scorecard: bool = True
    ready_for_cli_evaluation_bundle_preview: bool = True
    ready_for_cli_controlled_test_execution_dispatch: bool = True
    ready_for_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_uncontrolled_subprocess: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_repair_patch_proposal: bool = False
    ready_for_repair_diff_generation: bool = False
    ready_for_code_hunk_generation: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_execution: bool = False
    ready_for_repair_loop: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_agentic_loop: bool = False
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
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    summary: str = "v0.37.8 is ready for v0.37.9 design handoff only"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("summary", self.summary)
        for name in UNSAFE_CLI_FLAG_NAMES:
            _validate_false(name, getattr(self, name))
        _validate_metadata(self.metadata)


def build_cli_test_runner_flags(**overrides: Any) -> CLITestRunnerFlagSet:
    return CLITestRunnerFlagSet(**overrides)


def build_cli_test_runner_source_ref(**overrides: Any) -> CLITestRunnerSourceRef:
    defaults = {
        "source_ref_id": "cli-source:argv",
        "source_kind": CLITestRunnerInputSourceKind.ARGV_LIST,
        "source_id": "argv",
        "source_summary": "bounded argv list supplied by caller",
    }
    defaults.update(overrides)
    return CLITestRunnerSourceRef(**defaults)


def build_cli_test_runner_argument_spec(**overrides: Any) -> CLITestRunnerArgumentSpec:
    defaults = {"argument_spec_id": "cli-arg:format", "name": "--format", "description": "bounded output format selector"}
    defaults.update(overrides)
    return CLITestRunnerArgumentSpec(**defaults)


def build_cli_test_runner_command_spec(**overrides: Any) -> CLITestRunnerCommandSpec:
    defaults = {
        "command_spec_id": "cli-command:test-run-help",
        "command_kind": CLITestRunnerCommandKind.TEST_RUN_HELP,
        "command_mode": CLITestRunnerCommandMode.HELP,
        "command_name": "test-run-help",
        "description": "bounded help command; not shell execution",
        "allowed_decisions": [CLITestRunnerDecisionKind.ALLOW_HELP],
    }
    defaults.update(overrides)
    return CLITestRunnerCommandSpec(**defaults)


def build_cli_test_runner_surface_policy(**overrides: Any) -> CLITestRunnerSurfacePolicy:
    if "allowed_command_kinds" not in overrides:
        overrides["allowed_command_kinds"] = [kind for kind, _, _ in SAFE_COMMAND_MAP.values()]
    if "blocked_command_kinds" not in overrides:
        overrides["blocked_command_kinds"] = [kind for kind, _, _ in DENIED_COMMAND_MAP.values()]
    return CLITestRunnerSurfacePolicy(**overrides)


def build_cli_test_runner_surface(**overrides: Any) -> CLITestRunnerSurface:
    if "command_specs" not in overrides:
        overrides["command_specs"] = default_cli_test_runner_command_specs()
    if "policy" not in overrides:
        overrides["policy"] = default_cli_test_runner_surface_policy()
    if "flags" not in overrides:
        overrides["flags"] = build_cli_test_runner_flags()
    return CLITestRunnerSurface(**overrides)


def build_cli_test_runner_runtime_context(**overrides: Any) -> CLITestRunnerRuntimeContext:
    return CLITestRunnerRuntimeContext(**overrides)


def build_cli_test_runner_invocation(**overrides: Any) -> CLITestRunnerInvocation:
    defaults = {
        "invocation_id": "cli-invocation:v0378",
        "argv": ["test-run-help"],
        "command_kind": CLITestRunnerCommandKind.TEST_RUN_HELP,
        "command_mode": CLITestRunnerCommandMode.HELP,
    }
    defaults.update(overrides)
    return CLITestRunnerInvocation(**defaults)


def build_cli_test_runner_invocation_decision(**overrides: Any) -> CLITestRunnerInvocationDecision:
    defaults = {
        "decision_id": "cli-decision:v0378",
        "invocation_id": "cli-invocation:v0378",
        "decision_kind": CLITestRunnerDecisionKind.ALLOW_HELP,
        "reason": "bounded help command allowed",
        "allowed_command_kind": CLITestRunnerCommandKind.TEST_RUN_HELP,
        "bounded_preview_allowed": True,
    }
    defaults.update(overrides)
    return CLITestRunnerInvocationDecision(**defaults)


def build_cli_test_runner_denied_command(**overrides: Any) -> CLITestRunnerDeniedCommand:
    defaults = {
        "denied_command_id": "cli-denied:v0378",
        "invocation_id": None,
        "decision_id": None,
        "command_kind": CLITestRunnerCommandKind.UNKNOWN,
        "risk_kinds": [CLITestRunnerRiskKind.COMMAND_EXECUTION_RISK],
        "reason": "command denied by v0.37.8 CLI surface policy",
    }
    defaults.update(overrides)
    return CLITestRunnerDeniedCommand(**defaults)


def build_cli_test_runner_command_result(**overrides: Any) -> CLITestRunnerCommandResult:
    defaults = {
        "command_result_id": "cli-command-result:v0378",
        "invocation_id": "cli-invocation:v0378",
        "decision_id": "cli-decision:v0378",
        "command_kind": CLITestRunnerCommandKind.TEST_RUN_HELP,
        "status": CLITestRunnerSurfaceStatus.COMPLETED,
        "structured_result": {"release": V0378_RELEASE_NAME},
        "text_summary": "bounded CLI command completed in memory",
    }
    defaults.update(overrides)
    return CLITestRunnerCommandResult(**defaults)


def build_cli_test_runner_run_output(**overrides: Any) -> CLITestRunnerRunOutput:
    defaults = {
        "run_output_id": "cli-run-output:v0378",
        "invocation_id": "cli-invocation:v0378",
        "command_result": build_cli_test_runner_command_result(),
        "denied_command": None,
        "rendered_output": "bounded CLI output",
        "output_format": CLITestRunnerOutputFormat.TEXT,
        "status": CLITestRunnerSurfaceStatus.COMPLETED,
        "summary": "bounded in-memory CLI output",
    }
    defaults.update(overrides)
    return CLITestRunnerRunOutput(**defaults)


def build_cli_test_runner_run_report(**overrides: Any) -> CLITestRunnerRunReport:
    return CLITestRunnerRunReport(**overrides)


def build_cli_test_runner_run_preview(**overrides: Any) -> CLITestRunnerRunPreview:
    return CLITestRunnerRunPreview(**overrides)


def build_cli_test_runner_no_unsafe_side_effect_guarantee(**overrides: Any) -> CLITestRunnerNoUnsafeSideEffectGuarantee:
    return CLITestRunnerNoUnsafeSideEffectGuarantee(**overrides)


def build_v0378_readiness_report(**overrides: Any) -> V0378ReadinessReport:
    return V0378ReadinessReport(**overrides)


def default_cli_test_runner_command_specs() -> list[CLITestRunnerCommandSpec]:
    specs: list[CLITestRunnerCommandSpec] = []
    arg_spec = build_cli_test_runner_argument_spec()
    for command_name, (kind, mode, decision) in SAFE_COMMAND_MAP.items():
        specs.append(build_cli_test_runner_command_spec(
            command_spec_id=f"cli-command:{command_name}",
            command_kind=kind,
            command_mode=mode,
            command_name=command_name,
            description=f"{command_name} is a bounded v0.37 CLI surface command, not an OS command",
            argument_specs=[arg_spec],
            allowed_decisions=[decision],
            risk_kinds=[],
            dispatch_target=_dispatch_target_for_kind(kind),
            enabled=True,
        ))
    for command_name, (kind, decision, risk) in DENIED_COMMAND_MAP.items():
        specs.append(build_cli_test_runner_command_spec(
            command_spec_id=f"cli-denied-command:{command_name}",
            command_kind=kind,
            command_mode=CLITestRunnerCommandMode.DENIED,
            command_name=command_name,
            description=f"{command_name} is explicitly denied by v0.37.8",
            argument_specs=[],
            allowed_decisions=[decision],
            risk_kinds=[risk],
            dispatch_target=None,
            enabled=True,
        ))
    return specs


def default_cli_test_runner_surface_policy() -> CLITestRunnerSurfacePolicy:
    return build_cli_test_runner_surface_policy()


def build_default_cli_test_runner_surface() -> CLITestRunnerSurface:
    return build_cli_test_runner_surface()


def _dispatch_target_for_kind(kind: CLITestRunnerCommandKind | str) -> str | None:
    value = _enum_value(kind)
    return {
        CLITestRunnerCommandKind.TEST_RUN_SANDBOX.value: "v0372_controlled_sandbox_test_execution_helper_boundary",
        CLITestRunnerCommandKind.TEST_RESULT_SUMMARY.value: "v0373_test_result_envelope_helper_boundary",
        CLITestRunnerCommandKind.FEEDBACK_REPORT.value: "v0374_feedback_report_helper_boundary",
        CLITestRunnerCommandKind.REPAIR_SUGGESTION_PREVIEW.value: "v0375_repair_suggestion_metadata_helper_boundary",
        CLITestRunnerCommandKind.VERA_TRIAL_RUN_ONCE.value: "v0376_vera_codex_one_shot_trial_helper_boundary",
        CLITestRunnerCommandKind.COLD_SCORECARD.value: "v0377_cold_agent_evaluation_helper_boundary",
    }.get(value)


def parse_cli_test_runner_invocation(argv: list[str], surface: CLITestRunnerSurface | None = None) -> CLITestRunnerInvocation:
    surface = surface or build_default_cli_test_runner_surface()
    if not isinstance(argv, list):
        raise ValueError("argv must be a list")
    bounded_argv = [str(arg)[: surface.policy.max_arg_chars] for arg in argv]
    if not bounded_argv:
        command = "no-op"
    else:
        command = _canonical_command(bounded_argv[0])
    parsed: dict[str, Any] = {}
    output_format: CLITestRunnerOutputFormat | str = CLITestRunnerOutputFormat.TEXT
    remaining = bounded_argv[1:]
    index = 0
    while index < len(remaining):
        token = remaining[index]
        if token == "--format" and index + 1 < len(remaining):
            candidate = remaining[index + 1].strip().lower()
            output_format = candidate if candidate in {item.value for item in CLITestRunnerOutputFormat} else CLITestRunnerOutputFormat.TEXT
            parsed["format"] = output_format
            index += 2
            continue
        if token.startswith("--") and index + 1 < len(remaining) and not remaining[index + 1].startswith("--"):
            parsed[token[2:].replace("-", "_")] = remaining[index + 1]
            index += 2
            continue
        parsed.setdefault("args", []).append(token)
        index += 1
    if command in SAFE_COMMAND_MAP:
        kind, mode, _ = SAFE_COMMAND_MAP[command]
    elif command in DENIED_COMMAND_MAP:
        kind, _, _ = DENIED_COMMAND_MAP[command]
        mode = CLITestRunnerCommandMode.DENIED
    else:
        kind = CLITestRunnerCommandKind.UNKNOWN
        mode = CLITestRunnerCommandMode.UNKNOWN
    return build_cli_test_runner_invocation(
        invocation_id=f"cli-invocation:{command or 'no-op'}",
        argv=bounded_argv,
        command_kind=kind,
        command_mode=mode,
        parsed_args=parsed,
        requested_output_format=output_format,
        source_refs=[build_cli_test_runner_source_ref()],
        invocation_summary=f"parsed bounded CLI argv for {command}",
        metadata={"argv_not_passed_to_shell": True, "argv_not_passed_to_subprocess": True, "raw_arg_count": len(argv)},
    )


def evaluate_cli_test_runner_invocation(
    invocation: CLITestRunnerInvocation,
    surface: CLITestRunnerSurface | None,
    runtime_context: CLITestRunnerRuntimeContext | None = None,
) -> CLITestRunnerInvocationDecision:
    surface = surface or build_default_cli_test_runner_surface()
    runtime_context = runtime_context or build_cli_test_runner_runtime_context()
    command_value = _enum_value(invocation.command_kind)
    if command_value == CLITestRunnerCommandKind.UNKNOWN.value:
        return _deny_decision(invocation, CLITestRunnerDecisionKind.DENY, CLITestRunnerRiskKind.COMMAND_EXECUTION_RISK, "unknown CLI command denied by default")
    if command_value.startswith("denied_"):
        canonical = _canonical_command(invocation.argv[0]) if invocation.argv else "unknown"
        _, decision, risk = DENIED_COMMAND_MAP.get(canonical, (CLITestRunnerCommandKind.UNKNOWN, CLITestRunnerDecisionKind.DENY, CLITestRunnerRiskKind.UNKNOWN))
        return _deny_decision(invocation, decision, risk, "unsafe CLI command denied without execution")
    if _contains_prohibited_pattern(invocation.argv[1:], surface.policy.prohibited_arg_patterns):
        return _deny_decision(invocation, CLITestRunnerDecisionKind.DENY, CLITestRunnerRiskKind.SHELL_INJECTION_RISK, "unsafe CLI argument pattern denied")
    safe_command = _safe_command_name_from_kind(invocation.command_kind)
    if not safe_command:
        return _deny_decision(invocation, CLITestRunnerDecisionKind.BLOCK, CLITestRunnerRiskKind.COMMAND_EXECUTION_RISK, "command is not part of safe command set")
    _, _, decision_kind = SAFE_COMMAND_MAP[safe_command]
    if command_value == CLITestRunnerCommandKind.TEST_RUN_SANDBOX.value:
        allowed = (
            surface.policy.allow_sandbox_test_run
            and surface.policy.allow_controlled_test_execution_dispatch
            and runtime_context.allows_controlled_test_execution_dispatch
            and runtime_context.has_invocation_contract
            and bool(runtime_context.sandbox_root_ref)
        )
        if not allowed:
            return _deny_decision(invocation, CLITestRunnerDecisionKind.REQUIRE_REVIEW, CLITestRunnerRiskKind.COMMAND_EXECUTION_RISK, "test-run-sandbox requires v0.37.2 contract and sandbox root context")
        return build_cli_test_runner_invocation_decision(
            decision_id=f"cli-decision:{safe_command}",
            invocation_id=invocation.invocation_id,
            decision_kind=decision_kind,
            reason="test-run-sandbox allowed only as v0.37.2 controlled helper boundary dispatch",
            allowed_command_kind=invocation.command_kind,
            controlled_test_execution_dispatch_allowed=True,
            evidence_refs=["v0372_controlled_helper_boundary"],
        )
    return build_cli_test_runner_invocation_decision(
        decision_id=f"cli-decision:{safe_command}",
        invocation_id=invocation.invocation_id,
        decision_kind=decision_kind,
        reason="bounded safe CLI metadata command allowed",
        allowed_command_kind=invocation.command_kind,
        bounded_preview_allowed=command_value in {
            CLITestRunnerCommandKind.TEST_RUN_HELP.value,
            CLITestRunnerCommandKind.TEST_RUN_STATUS.value,
            CLITestRunnerCommandKind.TEST_INVOCATION_PREVIEW.value,
            CLITestRunnerCommandKind.VERA_TRIAL_PREVIEW.value,
            CLITestRunnerCommandKind.EVALUATION_BUNDLE_PREVIEW.value,
            CLITestRunnerCommandKind.NO_OP.value,
        },
        result_summary_allowed=command_value == CLITestRunnerCommandKind.TEST_RESULT_SUMMARY.value,
        feedback_report_allowed=command_value == CLITestRunnerCommandKind.FEEDBACK_REPORT.value,
        repair_suggestion_preview_allowed=command_value == CLITestRunnerCommandKind.REPAIR_SUGGESTION_PREVIEW.value,
        vera_trial_run_once_allowed=command_value == CLITestRunnerCommandKind.VERA_TRIAL_RUN_ONCE.value,
        cold_scorecard_allowed=command_value == CLITestRunnerCommandKind.COLD_SCORECARD.value,
        evidence_refs=["v0378_cli_surface_policy"],
    )


def _deny_decision(
    invocation: CLITestRunnerInvocation,
    decision_kind: CLITestRunnerDecisionKind,
    risk_kind: CLITestRunnerRiskKind,
    reason: str,
) -> CLITestRunnerInvocationDecision:
    return build_cli_test_runner_invocation_decision(
        decision_id=f"cli-decision:denied:{invocation.invocation_id}",
        invocation_id=invocation.invocation_id,
        decision_kind=decision_kind,
        reason=reason,
        risk_kinds=[risk_kind],
        allowed_command_kind=None,
    )


def _safe_command_name_from_kind(kind: CLITestRunnerCommandKind | str) -> str | None:
    value = _enum_value(kind)
    for command, (candidate, _, _) in SAFE_COMMAND_MAP.items():
        if candidate.value == value:
            return command
    return None


def run_cli_test_runner_command(
    invocation: CLITestRunnerInvocation,
    surface: CLITestRunnerSurface | None = None,
    runtime_context: CLITestRunnerRuntimeContext | None = None,
) -> CLITestRunnerRunOutput:
    surface = surface or build_default_cli_test_runner_surface()
    runtime_context = runtime_context or build_cli_test_runner_runtime_context()
    decision = evaluate_cli_test_runner_invocation(invocation, surface, runtime_context)
    if _enum_value(decision.decision_kind).startswith("deny") or _enum_value(decision.decision_kind) in {CLITestRunnerDecisionKind.BLOCK.value, CLITestRunnerDecisionKind.REQUIRE_REVIEW.value, CLITestRunnerDecisionKind.UNKNOWN.value}:
        denied = build_cli_test_runner_denied_command(
            denied_command_id=f"cli-denied:{invocation.invocation_id}",
            invocation_id=invocation.invocation_id,
            decision_id=decision.decision_id,
            command_kind=invocation.command_kind,
            risk_kinds=decision.risk_kinds or [CLITestRunnerRiskKind.COMMAND_EXECUTION_RISK],
            reason=decision.reason,
        )
        rendered = render_cli_test_runner_output(denied, invocation.requested_output_format)
        return build_cli_test_runner_run_output(
            run_output_id=f"cli-output:denied:{invocation.invocation_id}",
            invocation_id=invocation.invocation_id,
            command_result=None,
            denied_command=denied,
            rendered_output=rendered,
            output_format=invocation.requested_output_format,
            status=CLITestRunnerSurfaceStatus.DENIED,
            summary="CLI command denied safely without execution",
        )
    structured, summary, refs, dispatched = _run_safe_command_metadata(invocation, decision, runtime_context)
    rendered_summary, truncated = _limit_text(summary)
    result = build_cli_test_runner_command_result(
        command_result_id=f"cli-result:{invocation.invocation_id}",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=invocation.command_kind,
        status=CLITestRunnerSurfaceStatus.COMPLETED,
        invocation_contract_ref=refs.get("invocation_contract_ref"),
        test_execution_result_ref=refs.get("test_execution_result_ref"),
        result_envelope_ref=refs.get("result_envelope_ref"),
        feedback_report_ref=refs.get("feedback_report_ref"),
        repair_suggestion_ref=refs.get("repair_suggestion_ref"),
        vera_trial_packet_ref=refs.get("vera_trial_packet_ref"),
        cold_evaluation_report_ref=refs.get("cold_evaluation_report_ref"),
        structured_result=structured,
        text_summary=rendered_summary,
        truncated=truncated,
        controlled_test_execution_dispatched=dispatched,
        metadata={"bounded_in_memory_output": True},
    )
    rendered = render_cli_test_runner_output(result, invocation.requested_output_format)
    return build_cli_test_runner_run_output(
        run_output_id=f"cli-output:{invocation.invocation_id}",
        invocation_id=invocation.invocation_id,
        command_result=result,
        denied_command=None,
        rendered_output=rendered,
        output_format=invocation.requested_output_format,
        status=CLITestRunnerSurfaceStatus.COMPLETED,
        summary="CLI command returned bounded in-memory output",
    )


def _run_safe_command_metadata(
    invocation: CLITestRunnerInvocation,
    decision: CLITestRunnerInvocationDecision,
    runtime_context: CLITestRunnerRuntimeContext,
) -> tuple[dict[str, Any], str, dict[str, str], bool]:
    command = _enum_value(invocation.command_kind)
    refs: dict[str, str] = {}
    if command == CLITestRunnerCommandKind.TEST_RUN_HELP.value:
        return {"safe_commands": list(SAFE_COMMAND_MAP), "denied_commands": list(DENIED_COMMAND_MAP)}, "v0.37.8 bounded CLI help; not shell execution", refs, False
    if command == CLITestRunnerCommandKind.TEST_RUN_STATUS.value:
        return {"surface": V0378_RELEASE_NAME, "ready_for_execution": False}, "CLI surface initialized; unsafe runtime remains blocked", refs, False
    if command == CLITestRunnerCommandKind.TEST_INVOCATION_PREVIEW.value:
        return {"argv": invocation.argv, "parsed_args": invocation.parsed_args, "argv_not_passed_to_shell": True}, "test invocation preview only", refs, False
    if command == CLITestRunnerCommandKind.TEST_RUN_SANDBOX.value:
        refs["invocation_contract_ref"] = str(runtime_context.metadata.get("invocation_contract_ref", "v0372:invocation-contract"))
        refs["test_execution_result_ref"] = str(runtime_context.metadata.get("test_execution_result_ref", "v0372:controlled-execution-result"))
        return {"dispatch_target": "v0.37.2 controlled sandbox helper boundary", "direct_subprocess_used_by_v0378": False}, "test-run-sandbox dispatched only through v0.37.2 helper boundary metadata", refs, True
    if command == CLITestRunnerCommandKind.TEST_RESULT_SUMMARY.value:
        refs["result_envelope_ref"] = str(runtime_context.metadata.get("result_envelope_ref", "v0373:result-envelope"))
        return {"has_test_result_envelope": runtime_context.has_test_result_envelope, "summary_source": "v0.37.3 metadata"}, "test result summary produced from supplied metadata only", refs, False
    if command == CLITestRunnerCommandKind.FEEDBACK_REPORT.value:
        refs["feedback_report_ref"] = str(runtime_context.metadata.get("feedback_report_ref", "v0374:feedback-report"))
        return {"has_feedback_report": runtime_context.has_feedback_report, "summary_source": "v0.37.4 metadata"}, "feedback report output produced from supplied metadata only", refs, False
    if command == CLITestRunnerCommandKind.REPAIR_SUGGESTION_PREVIEW.value:
        refs["repair_suggestion_ref"] = str(runtime_context.metadata.get("repair_suggestion_ref", "v0375:repair-suggestion"))
        return {"has_repair_suggestion": runtime_context.has_repair_suggestion, "patch_generated": False, "diff_generated": False, "hunk_generated": False}, "repair suggestion preview contains no patch/diff/hunk", refs, False
    if command == CLITestRunnerCommandKind.VERA_TRIAL_PREVIEW.value:
        return {"trial_count": 1, "max_cycle_count": 1, "model_provider_invocation_allowed": False}, "Vera trial preview is one-shot metadata only", refs, False
    if command == CLITestRunnerCommandKind.VERA_TRIAL_RUN_ONCE.value:
        packet = runtime_context.metadata.get("vera_trial_packet") or run_vera_codex_one_shot_trial(
            repair_suggestion=runtime_context.metadata.get("repair_suggestion"),
            feedback_report=runtime_context.metadata.get("feedback_report"),
            result_envelope=runtime_context.metadata.get("result_envelope"),
        )
        refs["vera_trial_packet_ref"] = getattr(packet, "trial_packet_id", "v0376:vera-trial-packet")
        return {"trial_packet_id": refs["vera_trial_packet_ref"], "trial_count": getattr(packet, "trial_count", 1), "max_cycle_count": getattr(packet, "max_cycle_count", 1), "model_invocation_performed": False}, "Vera one-shot trial metadata produced through v0.37.6 helper", refs, False
    if command == CLITestRunnerCommandKind.COLD_SCORECARD.value:
        report = runtime_context.metadata.get("cold_evaluation_report") or create_cold_agent_evaluation_report(
            trial_packet=runtime_context.metadata.get("vera_trial_packet"),
            repair_suggestion=runtime_context.metadata.get("repair_suggestion"),
            feedback_report=runtime_context.metadata.get("feedback_report"),
            result_envelope=runtime_context.metadata.get("result_envelope"),
        )
        refs["cold_evaluation_report_ref"] = getattr(report, "evaluation_report_id", "v0377:cold-evaluation-report")
        return {"cold_evaluation_report_id": refs["cold_evaluation_report_ref"], "production_certified": False, "ready_for_execution": False}, "cold scorecard metadata produced through v0.37.7 helper", refs, False
    if command == CLITestRunnerCommandKind.EVALUATION_BUNDLE_PREVIEW.value:
        return {"has_vera_trial_packet": runtime_context.has_vera_trial_packet, "has_cold_evaluation_report": runtime_context.has_cold_evaluation_report}, "evaluation bundle preview aggregates supplied metadata only", refs, False
    return {"no_op": True}, "no-op command returned safe in-memory output", refs, False


def render_cli_test_runner_output(output: Any, output_format: CLITestRunnerOutputFormat | str) -> str:
    fmt = _enum_value(output_format)
    if isinstance(output, CLITestRunnerDeniedCommand):
        base = {"status": "denied", "reason": output.reason, "safe_alternatives": output.safe_alternatives}
    elif isinstance(output, CLITestRunnerCommandResult):
        base = {"status": _enum_value(output.status), "summary": output.text_summary, "structured_result": output.structured_result}
    elif isinstance(output, CLITestRunnerRunOutput):
        base = {"status": _enum_value(output.status), "summary": output.summary, "rendered_output": output.rendered_output}
    else:
        base = {"summary": str(output)}
    if fmt == CLITestRunnerOutputFormat.NO_OUTPUT.value:
        return "no output requested"
    if fmt == CLITestRunnerOutputFormat.MARKDOWN.value:
        return f"**CLI Output**\n\n- status: {base.get('status', 'unknown')}\n- summary: {base.get('summary') or base.get('reason')}"
    if fmt in (CLITestRunnerOutputFormat.JSON.value, CLITestRunnerOutputFormat.STRUCTURED_ARTIFACT.value, CLITestRunnerOutputFormat.DEBUG_SUMMARY.value):
        return str(base)
    return str(base.get("summary") or base.get("reason") or base)


def cli_test_runner_flags_preserve_unsafe_false(flags: CLITestRunnerFlagSet) -> bool:
    return isinstance(flags, CLITestRunnerFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_CLI_FLAG_NAMES)


def cli_test_runner_invocation_is_not_shell(invocation: CLITestRunnerInvocation) -> bool:
    return isinstance(invocation, CLITestRunnerInvocation) and invocation.metadata.get("argv_not_passed_to_shell") is True


def cli_test_runner_decision_blocks_shell_and_live_runtime(decision: CLITestRunnerInvocationDecision) -> bool:
    return isinstance(decision, CLITestRunnerInvocationDecision) and all(
        getattr(decision, name) is False
        for name in (
            "shell_execution_allowed",
            "direct_subprocess_allowed",
            "command_execution_allowed",
            "dependency_install_allowed",
            "network_access_allowed",
            "live_workspace_write_allowed",
            "patch_application_allowed",
            "code_edit_allowed",
            "apply_patch_allowed",
            "git_apply_allowed",
            "repair_execution_allowed",
        )
    )


def cli_test_runner_decision_blocks_external_agent(decision: CLITestRunnerInvocationDecision) -> bool:
    return isinstance(decision, CLITestRunnerInvocationDecision) and not decision.external_agent_execution_allowed and not decision.claude_code_invocation_allowed and not decision.codex_cli_invocation_allowed and not decision.dominion_runtime_allowed


def cli_test_runner_surface_is_not_shell(surface: CLITestRunnerSurface) -> bool:
    return isinstance(surface, CLITestRunnerSurface) and not surface.ready_for_execution and not surface.policy.allow_shell and not surface.policy.allow_direct_subprocess


def v0378_readiness_report_is_not_execution_ready(report: V0378ReadinessReport) -> bool:
    return isinstance(report, V0378ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_CLI_FLAG_NAMES)
