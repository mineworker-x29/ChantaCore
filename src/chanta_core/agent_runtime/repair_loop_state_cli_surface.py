"""v0.39.8 CLI loop-state preview surface metadata.

This module creates CLI-facing preview metadata only. It does not execute shell
commands, start subprocesses, apply patches, run re-tests, submit prompts,
invoke models or subagents, export files, persist traces, execute repair, run
loops, start Dominion runtime, or certify production readiness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0398_VERSION = "v0.39.8"
V0398_RELEASE_NAME = "v0.39.8 CLI Sandbox Repair Apply / Re-test / Loop-State Surface"
V039_TRACK_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop with PI-native Self-Prompting Mission Loop Boundary"

PROHIBITED_RUNTIME_ACTIONS = [
    "apply_execution",
    "retest_execution",
    "prompt_submission",
    "model_invocation",
    "subagent_invocation",
    "external_agent",
    "shell",
    "subprocess",
    "arbitrary_command",
    "file_export",
    "external_send",
    "trace_persistence",
    "Dominion",
]


class RepairCLILoopSurfaceMode(StrEnum):
    CLI_LOOP_STATE_SURFACE = "cli_loop_state_surface"
    CLI_HELP_SURFACE = "cli_help_surface"
    CLI_STATUS_SURFACE = "cli_status_surface"
    CLI_APPROVAL_PREVIEW = "cli_approval_preview"
    CLI_WORKSPACE_PREVIEW = "cli_workspace_preview"
    CLI_SANDBOX_APPLY_PREVIEW = "cli_sandbox_apply_preview"
    CLI_POST_APPLY_RETEST_PREVIEW = "cli_post_apply_retest_preview"
    CLI_OUTCOME_COMPARISON_PREVIEW = "cli_outcome_comparison_preview"
    CLI_PROCESS_STATE_PREVIEW = "cli_process_state_preview"
    CLI_SELF_PROMPT_DRAFT_PREVIEW = "cli_self_prompt_draft_preview"
    CLI_SUBAGENT_PROMPT_DRAFT_PREVIEW = "cli_subagent_prompt_draft_preview"
    CLI_HUMAN_HANDOFF_PREVIEW = "cli_human_handoff_preview"
    CLI_LOOP_BUNDLE_PREVIEW = "cli_loop_bundle_preview"
    CLI_BLOCKED_ACTIONS_PREVIEW = "cli_blocked_actions_preview"
    CLI_READINESS_PREVIEW = "cli_readiness_preview"
    CLI_CONSOLIDATION_HANDOFF_PREVIEW = "cli_consolidation_handoff_preview"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceSourceKind(StrEnum):
    V0397_SELF_PROMPTING_DRAFT_PACKET = "v0397_self_prompting_draft_packet"
    V0397_HUMAN_HANDOFF_PROMPT = "v0397_human_handoff_prompt"
    V0397_PROMPT_SAFETY_ASSESSMENT = "v0397_prompt_safety_assessment"
    V0397_READINESS_REPORT = "v0397_readiness_report"
    V0396_PROCESS_STATE_RECONSTRUCTION_REPORT = "v0396_process_state_reconstruction_report"
    V0396_MISSION_STATE_PROJECTION = "v0396_mission_state_projection"
    V0396_PIG_DIAGNOSTIC_INPUT_CONTEXT = "v0396_pig_diagnostic_input_context"
    V0395_OUTCOME_COMPARISON_REPORT = "v0395_outcome_comparison_report"
    V0395_EFFECTIVENESS_ASSESSMENT = "v0395_effectiveness_assessment"
    V0395_REGRESSION_SIGNAL = "v0395_regression_signal"
    V0394_POST_APPLY_RETEST_RESULT = "v0394_post_apply_retest_result"
    V0394_POST_APPLY_RETEST_RUN_RECORD = "v0394_post_apply_retest_run_record"
    V0394_OUTPUT_CAPTURE = "v0394_output_capture"
    V0393_SANDBOX_APPLY_RESULT = "v0393_sandbox_apply_result"
    V0393_SANDBOX_APPLY_TRANSACTION = "v0393_sandbox_apply_transaction"
    V0393_SANDBOX_APPLY_AUDIT = "v0393_sandbox_apply_audit"
    V0392_WORKSPACE_DESCRIPTOR = "v0392_workspace_descriptor"
    V0392_WORKSPACE_ISOLATION_DECISION = "v0392_workspace_isolation_decision"
    V0391_APPROVAL_ARTIFACT_DECISION = "v0391_approval_artifact_decision"
    V0391_APPROVAL_PROCESS_STATE_GATE = "v0391_approval_process_state_gate"
    CLI_ARGV = "cli_argv"
    PARSED_CLI_ARGS = "parsed_cli_args"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    SURFACE_CREATED = "surface_created"
    INVOCATION_PARSED = "invocation_parsed"
    COMMAND_CLASSIFIED = "command_classified"
    COMMAND_ALLOWED_FOR_PREVIEW = "command_allowed_for_preview"
    COMMAND_DENIED = "command_denied"
    VIEW_RENDERED = "view_rendered"
    BUNDLE_CREATED = "bundle_created"
    HANDOFF_CREATED = "handoff_created"
    READINESS_CREATED = "readiness_created"
    READY_FOR_V0399_CONSOLIDATION = "ready_for_v0399_consolidation"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairCLILoopSurfaceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_SURFACE_READY = "cli_surface_ready"
    CLI_COMMAND_REGISTRY_READY = "cli_command_registry_ready"
    CLI_INVOCATION_PARSER_READY = "cli_invocation_parser_ready"
    CLI_PREVIEW_RENDERER_READY = "cli_preview_renderer_ready"
    CLI_LOOP_BUNDLE_READY = "cli_loop_bundle_ready"
    CLI_HANDOFF_SURFACE_READY = "cli_handoff_surface_ready"
    CLI_BLOCKED_ACTION_SURFACE_READY = "cli_blocked_action_surface_ready"
    FUTURE_V0399_CONSOLIDATION_INPUT_READY = "future_v0399_consolidation_input_ready"
    DESIGN_HANDOFF_READY_FOR_V0399 = "design_handoff_ready_for_v0399"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairCLILoopSurfaceCommandKind(StrEnum):
    HELP = "help"
    STATUS = "status"
    APPROVAL_PREVIEW = "approval_preview"
    WORKSPACE_PREVIEW = "workspace_preview"
    SANDBOX_APPLY_PREVIEW = "sandbox_apply_preview"
    POST_APPLY_RETEST_PREVIEW = "post_apply_retest_preview"
    OUTCOME_COMPARISON_PREVIEW = "outcome_comparison_preview"
    PROCESS_STATE_PREVIEW = "process_state_preview"
    SELF_PROMPT_DRAFT_PREVIEW = "self_prompt_draft_preview"
    SUBAGENT_PROMPT_DRAFT_PREVIEW = "subagent_prompt_draft_preview"
    HUMAN_HANDOFF_PREVIEW = "human_handoff_preview"
    LOOP_BUNDLE_PREVIEW = "loop_bundle_preview"
    BLOCKED_ACTIONS_PREVIEW = "blocked_actions_preview"
    READINESS_PREVIEW = "readiness_preview"
    CONSOLIDATION_HANDOFF_PREVIEW = "consolidation_handoff_preview"
    NO_OP = "no_op"
    DENIED_APPLY = "denied_apply"
    DENIED_RETEST = "denied_retest"
    DENIED_RUN_TESTS = "denied_run_tests"
    DENIED_LIVE_APPLY = "denied_live_apply"
    DENIED_APPLY_PATCH = "denied_apply_patch"
    DENIED_GIT_APPLY = "denied_git_apply"
    DENIED_PROMPT_SUBMIT = "denied_prompt_submit"
    DENIED_MODEL_CALL = "denied_model_call"
    DENIED_NEXT_ACTION_EXECUTE = "denied_next_action_execute"
    DENIED_SUBAGENT_INVOKE = "denied_subagent_invoke"
    DENIED_EXTERNAL_AGENT = "denied_external_agent"
    DENIED_AUTO_CONTINUE = "denied_auto_continue"
    DENIED_RETRY_LOOP = "denied_retry_loop"
    DENIED_MULTI_CYCLE_LOOP = "denied_multi_cycle_loop"
    DENIED_REPAIR_EXECUTE = "denied_repair_execute"
    DENIED_SHELL = "denied_shell"
    DENIED_SUBPROCESS = "denied_subprocess"
    DENIED_ARBITRARY_COMMAND = "denied_arbitrary_command"
    DENIED_DEPENDENCY_INSTALL = "denied_dependency_install"
    DENIED_NETWORK = "denied_network"
    DENIED_FILE_EXPORT = "denied_file_export"
    DENIED_EXTERNAL_SEND = "denied_external_send"
    DENIED_TRACE_PERSIST = "denied_trace_persist"
    DENIED_OCEL_WRITE = "denied_ocel_write"
    DENIED_OCPX_PERSIST = "denied_ocpx_persist"
    DENIED_PIG_EXECUTE = "denied_pig_execute"
    DENIED_DOMINION = "denied_dominion"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_APPROVAL_PREVIEW = "allow_approval_preview"
    ALLOW_WORKSPACE_PREVIEW = "allow_workspace_preview"
    ALLOW_SANDBOX_APPLY_PREVIEW = "allow_sandbox_apply_preview"
    ALLOW_POST_APPLY_RETEST_PREVIEW = "allow_post_apply_retest_preview"
    ALLOW_OUTCOME_COMPARISON_PREVIEW = "allow_outcome_comparison_preview"
    ALLOW_PROCESS_STATE_PREVIEW = "allow_process_state_preview"
    ALLOW_SELF_PROMPT_DRAFT_PREVIEW = "allow_self_prompt_draft_preview"
    ALLOW_SUBAGENT_PROMPT_DRAFT_PREVIEW = "allow_subagent_prompt_draft_preview"
    ALLOW_HUMAN_HANDOFF_PREVIEW = "allow_human_handoff_preview"
    ALLOW_LOOP_BUNDLE_PREVIEW = "allow_loop_bundle_preview"
    ALLOW_BLOCKED_ACTIONS_PREVIEW = "allow_blocked_actions_preview"
    ALLOW_READINESS_PREVIEW = "allow_readiness_preview"
    ALLOW_CONSOLIDATION_HANDOFF_PREVIEW = "allow_consolidation_handoff_preview"
    CHOOSE_NO_OP = "choose_no_op"
    DENY_APPLY = "deny_apply"
    DENY_RETEST = "deny_retest"
    DENY_TEST_EXECUTION = "deny_test_execution"
    DENY_LIVE_APPLY = "deny_live_apply"
    DENY_PROMPT_SUBMIT = "deny_prompt_submit"
    DENY_MODEL_CALL = "deny_model_call"
    DENY_SUBAGENT_INVOCATION = "deny_subagent_invocation"
    DENY_EXTERNAL_AGENT = "deny_external_agent"
    DENY_AUTO_CONTINUE = "deny_auto_continue"
    DENY_SHELL = "deny_shell"
    DENY_SUBPROCESS = "deny_subprocess"
    DENY_ARBITRARY_COMMAND = "deny_arbitrary_command"
    DENY_FILE_EXPORT = "deny_file_export"
    DENY_EXTERNAL_SEND = "deny_external_send"
    DENY_TRACE_PERSISTENCE = "deny_trace_persistence"
    DENY_DOMINION = "deny_dominion"
    BLOCK = "block"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceRiskKind(StrEnum):
    CLI_EXECUTION_CONFUSION_RISK = "cli_execution_confusion_risk"
    APPLY_EXECUTION_CONFUSION_RISK = "apply_execution_confusion_risk"
    RETEST_EXECUTION_CONFUSION_RISK = "retest_execution_confusion_risk"
    PROMPT_EXECUTION_CONFUSION_RISK = "prompt_execution_confusion_risk"
    MODEL_INVOCATION_CONFUSION_RISK = "model_invocation_confusion_risk"
    SUBAGENT_INVOCATION_CONFUSION_RISK = "subagent_invocation_confusion_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    AUTONOMOUS_LOOP_RUNTIME_RISK = "autonomous_loop_runtime_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    ARBITRARY_COMMAND_EXECUTION_RISK = "arbitrary_command_execution_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    RAW_SUBPROCESS_EXECUTION_RISK = "raw_subprocess_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    FILE_EXPORT_RISK = "file_export_risk"
    EXTERNAL_SEND_RISK = "external_send_risk"
    TRACE_PERSISTENCE_RISK = "trace_persistence_risk"
    OCEL_WRITE_RISK = "ocel_write_risk"
    OCPX_PERSISTENCE_RISK = "ocpx_persistence_risk"
    PIG_EXECUTION_RISK = "pig_execution_risk"
    REPAIR_EXECUTION_RISK = "repair_execution_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceViewKind(StrEnum):
    HELP_VIEW = "help_view"
    STATUS_VIEW = "status_view"
    APPROVAL_VIEW = "approval_view"
    WORKSPACE_VIEW = "workspace_view"
    SANDBOX_APPLY_VIEW = "sandbox_apply_view"
    POST_APPLY_RETEST_VIEW = "post_apply_retest_view"
    OUTCOME_COMPARISON_VIEW = "outcome_comparison_view"
    PROCESS_STATE_VIEW = "process_state_view"
    SELF_PROMPT_DRAFT_VIEW = "self_prompt_draft_view"
    SUBAGENT_PROMPT_DRAFT_VIEW = "subagent_prompt_draft_view"
    HUMAN_HANDOFF_VIEW = "human_handoff_view"
    LOOP_BUNDLE_VIEW = "loop_bundle_view"
    BLOCKED_ACTIONS_VIEW = "blocked_actions_view"
    READINESS_VIEW = "readiness_view"
    CONSOLIDATION_HANDOFF_VIEW = "consolidation_handoff_view"
    DENIED_COMMAND_VIEW = "denied_command_view"
    NO_OP_VIEW = "no_op_view"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON_LIKE = "json_like"
    COMPACT = "compact"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class RepairCLILoopSurfaceDisposition(StrEnum):
    PREVIEW_RENDERED = "preview_rendered"
    PREVIEW_RENDERED_WITH_WARNINGS = "preview_rendered_with_warnings"
    COMMAND_DENIED = "command_denied"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    FAILED = "failed"
    UNKNOWN = "unknown"


SAFE_COMMAND_KINDS = [
    RepairCLILoopSurfaceCommandKind.HELP,
    RepairCLILoopSurfaceCommandKind.STATUS,
    RepairCLILoopSurfaceCommandKind.APPROVAL_PREVIEW,
    RepairCLILoopSurfaceCommandKind.WORKSPACE_PREVIEW,
    RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW,
    RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW,
    RepairCLILoopSurfaceCommandKind.OUTCOME_COMPARISON_PREVIEW,
    RepairCLILoopSurfaceCommandKind.PROCESS_STATE_PREVIEW,
    RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW,
    RepairCLILoopSurfaceCommandKind.SUBAGENT_PROMPT_DRAFT_PREVIEW,
    RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW,
    RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW,
    RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW,
    RepairCLILoopSurfaceCommandKind.READINESS_PREVIEW,
    RepairCLILoopSurfaceCommandKind.CONSOLIDATION_HANDOFF_PREVIEW,
    RepairCLILoopSurfaceCommandKind.NO_OP,
]

DENIED_COMMAND_KINDS = [
    RepairCLILoopSurfaceCommandKind.DENIED_APPLY,
    RepairCLILoopSurfaceCommandKind.DENIED_RETEST,
    RepairCLILoopSurfaceCommandKind.DENIED_RUN_TESTS,
    RepairCLILoopSurfaceCommandKind.DENIED_LIVE_APPLY,
    RepairCLILoopSurfaceCommandKind.DENIED_APPLY_PATCH,
    RepairCLILoopSurfaceCommandKind.DENIED_GIT_APPLY,
    RepairCLILoopSurfaceCommandKind.DENIED_PROMPT_SUBMIT,
    RepairCLILoopSurfaceCommandKind.DENIED_MODEL_CALL,
    RepairCLILoopSurfaceCommandKind.DENIED_NEXT_ACTION_EXECUTE,
    RepairCLILoopSurfaceCommandKind.DENIED_SUBAGENT_INVOKE,
    RepairCLILoopSurfaceCommandKind.DENIED_EXTERNAL_AGENT,
    RepairCLILoopSurfaceCommandKind.DENIED_AUTO_CONTINUE,
    RepairCLILoopSurfaceCommandKind.DENIED_RETRY_LOOP,
    RepairCLILoopSurfaceCommandKind.DENIED_MULTI_CYCLE_LOOP,
    RepairCLILoopSurfaceCommandKind.DENIED_REPAIR_EXECUTE,
    RepairCLILoopSurfaceCommandKind.DENIED_SHELL,
    RepairCLILoopSurfaceCommandKind.DENIED_SUBPROCESS,
    RepairCLILoopSurfaceCommandKind.DENIED_ARBITRARY_COMMAND,
    RepairCLILoopSurfaceCommandKind.DENIED_DEPENDENCY_INSTALL,
    RepairCLILoopSurfaceCommandKind.DENIED_NETWORK,
    RepairCLILoopSurfaceCommandKind.DENIED_FILE_EXPORT,
    RepairCLILoopSurfaceCommandKind.DENIED_EXTERNAL_SEND,
    RepairCLILoopSurfaceCommandKind.DENIED_TRACE_PERSIST,
    RepairCLILoopSurfaceCommandKind.DENIED_OCEL_WRITE,
    RepairCLILoopSurfaceCommandKind.DENIED_OCPX_PERSIST,
    RepairCLILoopSurfaceCommandKind.DENIED_PIG_EXECUTE,
    RepairCLILoopSurfaceCommandKind.DENIED_DOMINION,
    RepairCLILoopSurfaceCommandKind.UNKNOWN,
]

COMMAND_TO_VIEW = {
    RepairCLILoopSurfaceCommandKind.HELP: RepairCLILoopSurfaceViewKind.HELP_VIEW,
    RepairCLILoopSurfaceCommandKind.STATUS: RepairCLILoopSurfaceViewKind.STATUS_VIEW,
    RepairCLILoopSurfaceCommandKind.APPROVAL_PREVIEW: RepairCLILoopSurfaceViewKind.APPROVAL_VIEW,
    RepairCLILoopSurfaceCommandKind.WORKSPACE_PREVIEW: RepairCLILoopSurfaceViewKind.WORKSPACE_VIEW,
    RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW: RepairCLILoopSurfaceViewKind.SANDBOX_APPLY_VIEW,
    RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW: RepairCLILoopSurfaceViewKind.POST_APPLY_RETEST_VIEW,
    RepairCLILoopSurfaceCommandKind.OUTCOME_COMPARISON_PREVIEW: RepairCLILoopSurfaceViewKind.OUTCOME_COMPARISON_VIEW,
    RepairCLILoopSurfaceCommandKind.PROCESS_STATE_PREVIEW: RepairCLILoopSurfaceViewKind.PROCESS_STATE_VIEW,
    RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW: RepairCLILoopSurfaceViewKind.SELF_PROMPT_DRAFT_VIEW,
    RepairCLILoopSurfaceCommandKind.SUBAGENT_PROMPT_DRAFT_PREVIEW: RepairCLILoopSurfaceViewKind.SUBAGENT_PROMPT_DRAFT_VIEW,
    RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW: RepairCLILoopSurfaceViewKind.HUMAN_HANDOFF_VIEW,
    RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW: RepairCLILoopSurfaceViewKind.LOOP_BUNDLE_VIEW,
    RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW: RepairCLILoopSurfaceViewKind.BLOCKED_ACTIONS_VIEW,
    RepairCLILoopSurfaceCommandKind.READINESS_PREVIEW: RepairCLILoopSurfaceViewKind.READINESS_VIEW,
    RepairCLILoopSurfaceCommandKind.CONSOLIDATION_HANDOFF_PREVIEW: RepairCLILoopSurfaceViewKind.CONSOLIDATION_HANDOFF_VIEW,
    RepairCLILoopSurfaceCommandKind.NO_OP: RepairCLILoopSurfaceViewKind.NO_OP_VIEW,
}

COMMAND_TO_DECISION = {
    RepairCLILoopSurfaceCommandKind.HELP: RepairCLILoopSurfaceDecisionKind.ALLOW_HELP,
    RepairCLILoopSurfaceCommandKind.STATUS: RepairCLILoopSurfaceDecisionKind.ALLOW_STATUS,
    RepairCLILoopSurfaceCommandKind.APPROVAL_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_APPROVAL_PREVIEW,
    RepairCLILoopSurfaceCommandKind.WORKSPACE_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_WORKSPACE_PREVIEW,
    RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_SANDBOX_APPLY_PREVIEW,
    RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_POST_APPLY_RETEST_PREVIEW,
    RepairCLILoopSurfaceCommandKind.OUTCOME_COMPARISON_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_OUTCOME_COMPARISON_PREVIEW,
    RepairCLILoopSurfaceCommandKind.PROCESS_STATE_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_PROCESS_STATE_PREVIEW,
    RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_SELF_PROMPT_DRAFT_PREVIEW,
    RepairCLILoopSurfaceCommandKind.SUBAGENT_PROMPT_DRAFT_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_SUBAGENT_PROMPT_DRAFT_PREVIEW,
    RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_HUMAN_HANDOFF_PREVIEW,
    RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_LOOP_BUNDLE_PREVIEW,
    RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_BLOCKED_ACTIONS_PREVIEW,
    RepairCLILoopSurfaceCommandKind.READINESS_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_READINESS_PREVIEW,
    RepairCLILoopSurfaceCommandKind.CONSOLIDATION_HANDOFF_PREVIEW: RepairCLILoopSurfaceDecisionKind.ALLOW_CONSOLIDATION_HANDOFF_PREVIEW,
    RepairCLILoopSurfaceCommandKind.NO_OP: RepairCLILoopSurfaceDecisionKind.CHOOSE_NO_OP,
}

UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_cli_runtime_execution",
    "ready_for_cli_apply_execution",
    "ready_for_cli_retest_execution",
    "ready_for_cli_prompt_submission",
    "ready_for_cli_model_invocation",
    "ready_for_cli_subagent_invocation",
    "ready_for_cli_external_agent_execution",
    "ready_for_cli_auto_continue",
    "ready_for_cli_retry_loop",
    "ready_for_cli_multi_cycle_loop",
    "ready_for_cli_shell_execution",
    "ready_for_cli_subprocess_execution",
    "ready_for_cli_arbitrary_command_execution",
    "ready_for_cli_dependency_install",
    "ready_for_cli_network_access",
    "ready_for_cli_file_export",
    "ready_for_cli_external_send",
    "ready_for_prompt_submission_to_model",
    "ready_for_model_provider_invocation",
    "ready_for_self_prompt_execution",
    "ready_for_next_action_execution",
    "ready_for_subagent_invocation",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_opencode_invocation",
    "ready_for_hermes_invocation",
    "ready_for_openclaw_invocation",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_repair_execution",
    "ready_for_test_execution",
    "ready_for_controlled_retest_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_arbitrary_command_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_tool_execution",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_rollback_execution",
    "ready_for_ocel_event_write",
    "ready_for_ocel_file_write",
    "ready_for_ocpx_state_persistence",
    "ready_for_pig_recommendation_execution",
    "ready_for_pig_runtime_authority",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
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
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
]

UNSAFE_POLICY_NAMES = [
    "allow_cli_runtime_execution",
    "allow_cli_apply_execution",
    "allow_cli_retest_execution",
    "allow_cli_prompt_submission",
    "allow_cli_model_invocation",
    "allow_cli_subagent_invocation",
    "allow_cli_external_agent_execution",
    "allow_cli_auto_continue",
    "allow_cli_retry_loop",
    "allow_cli_multi_cycle_loop",
    "allow_cli_shell",
    "allow_cli_subprocess",
    "allow_cli_arbitrary_command",
    "allow_cli_dependency_install",
    "allow_cli_network_access",
    "allow_cli_file_export",
    "allow_cli_external_send",
    "allow_trace_persistence",
    "allow_ocel_write",
    "allow_ocpx_persistence",
    "allow_pig_execution",
    "allow_dominion_runtime",
]

UNSAFE_DECISION_NAMES = [
    "runtime_execution_allowed",
    "apply_execution_allowed",
    "retest_execution_allowed",
    "prompt_submission_allowed",
    "model_invocation_allowed",
    "subagent_invocation_allowed",
    "external_agent_allowed",
    "auto_continue_allowed",
    "retry_loop_allowed",
    "multi_cycle_loop_allowed",
    "shell_allowed",
    "subprocess_allowed",
    "arbitrary_command_allowed",
    "file_export_allowed",
    "external_send_allowed",
    "trace_persistence_allowed",
    "dominion_runtime_allowed",
    "production_certified",
]

UNSAFE_RESULT_NAMES = [
    "runtime_executed",
    "apply_executed",
    "retest_executed",
    "prompt_submitted",
    "model_invoked",
    "subagent_invoked",
    "external_agent_invoked",
    "auto_continued",
    "shell_used",
    "subprocess_used",
    "arbitrary_command_executed",
    "file_written",
    "file_exported",
    "sent_externally",
    "trace_persisted",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_REPORT_NAMES = [
    "runtime_executed",
    "apply_executed",
    "retest_executed",
    "prompt_executed",
    "model_invoked",
    "subagent_invoked",
    "external_agent_invoked",
    "autonomous_loop_continued",
    "trace_persisted",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
]

UNSAFE_READINESS_NAMES = [
    "cli_runtime_execution_enabled",
    "cli_apply_execution_enabled",
    "cli_retest_execution_enabled",
    "cli_prompt_submission_enabled",
    "cli_model_invocation_enabled",
    "cli_subagent_invocation_enabled",
    "cli_external_agent_enabled",
    "cli_auto_continue_enabled",
    "shell_enabled",
    "subprocess_enabled",
    "arbitrary_command_enabled",
    "file_export_enabled",
    "external_send_enabled",
    "trace_persistence_enabled",
    "dominion_runtime_enabled",
    "production_certified",
    "ready_for_execution",
]


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    values = defaults.copy()
    values.update(overrides)
    return values


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0398_VERSION not in version:
        raise ValueError("version must include v0.39.8")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.8")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


def _bounded(text: str, limit: int = 4000) -> tuple[str, bool]:
    if len(text) <= limit:
        return text, False
    suffix = "...[truncated]"
    if limit <= len(suffix):
        return text[:limit], True
    return f"{text[: limit - len(suffix)]}{suffix}", True


@dataclass(frozen=True)
class RepairCLILoopSurfaceFlagSet:
    flag_set_id: str
    version: str
    cli_loop_surface_layer_constructed: bool = True
    cli_command_registry_available: bool = True
    cli_invocation_parser_available: bool = True
    cli_preview_renderer_available: bool = True
    cli_loop_bundle_preview_available: bool = True
    cli_human_handoff_preview_available: bool = True
    cli_blocked_action_surface_available: bool = True
    cli_readiness_surface_available: bool = True
    future_v0399_consolidation_input_available: bool = True
    ready_for_v0399_consolidation: bool = True
    ready_for_cli_loop_state_surface: bool = True
    ready_for_cli_command_registry: bool = True
    ready_for_cli_invocation_parser: bool = True
    ready_for_cli_preview_renderer: bool = True
    ready_for_cli_approval_preview: bool = True
    ready_for_cli_workspace_preview: bool = True
    ready_for_cli_sandbox_apply_preview: bool = True
    ready_for_cli_post_apply_retest_preview: bool = True
    ready_for_cli_outcome_comparison_preview: bool = True
    ready_for_cli_process_state_preview: bool = True
    ready_for_cli_self_prompt_draft_preview: bool = True
    ready_for_cli_subagent_prompt_draft_preview: bool = True
    ready_for_cli_human_handoff_preview: bool = True
    ready_for_cli_loop_bundle_preview: bool = True
    ready_for_cli_blocked_actions_preview: bool = True
    ready_for_cli_readiness_preview: bool = True
    ready_for_future_v0399_consolidation_input: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_cli_runtime_execution: bool = False
    ready_for_cli_apply_execution: bool = False
    ready_for_cli_retest_execution: bool = False
    ready_for_cli_prompt_submission: bool = False
    ready_for_cli_model_invocation: bool = False
    ready_for_cli_subagent_invocation: bool = False
    ready_for_cli_external_agent_execution: bool = False
    ready_for_cli_auto_continue: bool = False
    ready_for_cli_retry_loop: bool = False
    ready_for_cli_multi_cycle_loop: bool = False
    ready_for_cli_shell_execution: bool = False
    ready_for_cli_subprocess_execution: bool = False
    ready_for_cli_arbitrary_command_execution: bool = False
    ready_for_cli_dependency_install: bool = False
    ready_for_cli_network_access: bool = False
    ready_for_cli_file_export: bool = False
    ready_for_cli_external_send: bool = False
    ready_for_prompt_submission_to_model: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_self_prompt_execution: bool = False
    ready_for_next_action_execution: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_opencode_invocation: bool = False
    ready_for_hermes_invocation: bool = False
    ready_for_openclaw_invocation: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_repair_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_retest_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_arbitrary_command_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_tool_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_rollback_execution: bool = False
    ready_for_ocel_event_write: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_ocpx_state_persistence: bool = False
    ready_for_pig_recommendation_execution: bool = False
    ready_for_pig_runtime_authority: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
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
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_dict("metadata", self.metadata)
        _validate_false(self, UNSAFE_FLAG_NAMES)


@dataclass(frozen=True)
class RepairCLILoopSurfaceSourceRef:
    source_ref_id: str
    source_kind: RepairCLILoopSurfaceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopCommandSpec:
    command_spec_id: str
    version: str
    command_kind: RepairCLILoopSurfaceCommandKind | str
    command_name: str
    aliases: list[str]
    description: str
    view_kind: RepairCLILoopSurfaceViewKind | str
    output_formats: list[RepairCLILoopSurfaceOutputFormat | str]
    preview_only: bool
    enabled: bool
    denied_by_default: bool
    risk_kinds: list[RepairCLILoopSurfaceRiskKind | str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["command_spec_id", "version", "command_name", "description"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["aliases", "output_formats", "risk_kinds"]:
            _validate_list(name, getattr(self, name))
        if self.preview_only is not True:
            raise ValueError("command specs are preview-only metadata in v0.39.8")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfacePolicy:
    policy_id: str
    version: str
    allowed_command_kinds: list[RepairCLILoopSurfaceCommandKind | str]
    denied_command_kinds: list[RepairCLILoopSurfaceCommandKind | str]
    allowed_view_kinds: list[RepairCLILoopSurfaceViewKind | str]
    allowed_output_formats: list[RepairCLILoopSurfaceOutputFormat | str]
    prohibited_argv_fragments: list[str]
    max_argv_items: int = 16
    max_arg_chars: int = 120
    max_render_chars: int = 4000
    require_preview_only: bool = True
    require_bounded_output: bool = True
    require_no_file_write: bool = True
    require_no_external_send: bool = True
    require_human_handoff: bool = True
    allow_help: bool = True
    allow_status: bool = True
    allow_preview_views: bool = True
    allow_loop_bundle_preview: bool = True
    allow_blocked_actions_preview: bool = True
    allow_readiness_preview: bool = True
    allow_future_v0399_consolidation_input: bool = True
    allow_cli_runtime_execution: bool = False
    allow_cli_apply_execution: bool = False
    allow_cli_retest_execution: bool = False
    allow_cli_prompt_submission: bool = False
    allow_cli_model_invocation: bool = False
    allow_cli_subagent_invocation: bool = False
    allow_cli_external_agent_execution: bool = False
    allow_cli_auto_continue: bool = False
    allow_cli_retry_loop: bool = False
    allow_cli_multi_cycle_loop: bool = False
    allow_cli_shell: bool = False
    allow_cli_subprocess: bool = False
    allow_cli_arbitrary_command: bool = False
    allow_cli_dependency_install: bool = False
    allow_cli_network_access: bool = False
    allow_cli_file_export: bool = False
    allow_cli_external_send: bool = False
    allow_trace_persistence: bool = False
    allow_ocel_write: bool = False
    allow_ocpx_persistence: bool = False
    allow_pig_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        for name in ["allowed_command_kinds", "denied_command_kinds", "allowed_view_kinds", "allowed_output_formats", "prohibited_argv_fragments"]:
            _validate_list(name, getattr(self, name))
        if self.max_argv_items <= 0 or self.max_arg_chars <= 0 or self.max_render_chars <= 0:
            raise ValueError("numeric limits must be > 0")
        _validate_true(self, ["require_preview_only", "require_bounded_output", "require_no_file_write", "require_no_external_send", "require_human_handoff"])
        _validate_false(self, UNSAFE_POLICY_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceInput:
    cli_surface_input_id: str
    version: str
    argv: list[str]
    requested_command: str | None
    artifact_context: dict[str, Any]
    source_refs: list[RepairCLILoopSurfaceSourceRef]
    prohibited_runtime_actions: list[str]
    task_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_surface_input_id", self.cli_surface_input_id)
        _validate_version(self.version)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("argv", self.argv)
        _validate_dict("artifact_context", self.artifact_context)
        _validate_list("source_refs", self.source_refs)
        _validate_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        for action in PROHIBITED_RUNTIME_ACTIONS:
            if action not in self.prohibited_runtime_actions:
                raise ValueError(f"prohibited_runtime_actions must include {action}")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopInvocation:
    invocation_id: str
    version: str
    argv: list[str]
    command_kind: RepairCLILoopSurfaceCommandKind | str
    output_format: RepairCLILoopSurfaceOutputFormat | str
    parsed_args: dict[str, Any]
    invocation_summary: str
    shell_used: bool = False
    subprocess_used: bool = False
    arbitrary_command_executed: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_id", self.invocation_id)
        _validate_version(self.version)
        _require_non_blank("invocation_summary", self.invocation_summary)
        _validate_list("argv", self.argv)
        _validate_dict("parsed_args", self.parsed_args)
        _validate_false(self, ["shell_used", "subprocess_used", "arbitrary_command_executed"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceDecision:
    cli_decision_id: str
    version: str
    invocation_id: str
    decision_kind: RepairCLILoopSurfaceDecisionKind | str
    status: RepairCLILoopSurfaceStatus | str
    disposition: RepairCLILoopSurfaceDisposition | str
    decision_summary: str
    risk_kinds: list[RepairCLILoopSurfaceRiskKind | str]
    evidence_refs: list[str]
    preview_allowed: bool
    runtime_execution_allowed: bool = False
    apply_execution_allowed: bool = False
    retest_execution_allowed: bool = False
    prompt_submission_allowed: bool = False
    model_invocation_allowed: bool = False
    subagent_invocation_allowed: bool = False
    external_agent_allowed: bool = False
    auto_continue_allowed: bool = False
    retry_loop_allowed: bool = False
    multi_cycle_loop_allowed: bool = False
    shell_allowed: bool = False
    subprocess_allowed: bool = False
    arbitrary_command_allowed: bool = False
    file_export_allowed: bool = False
    external_send_allowed: bool = False
    trace_persistence_allowed: bool = False
    dominion_runtime_allowed: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["cli_decision_id", "version", "invocation_id", "decision_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLIDeniedLoopCommand:
    denied_command_id: str
    version: str
    invocation_id: str | None
    command_kind: RepairCLILoopSurfaceCommandKind | str
    denied_summary: str
    reason: str
    risk_kinds: list[RepairCLILoopSurfaceRiskKind | str]
    safe_alternatives: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["denied_command_id", "version", "denied_summary", "reason"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["risk_kinds", "safe_alternatives", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopRenderedView:
    rendered_view_id: str
    version: str
    view_kind: RepairCLILoopSurfaceViewKind | str
    output_format: RepairCLILoopSurfaceOutputFormat | str
    title: str
    rendered_text: str
    structured_payload: dict[str, Any]
    bounded: bool
    redacted: bool
    truncated: bool
    written_to_file: bool = False
    sent_externally: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["rendered_view_id", "version", "title", "rendered_text"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_dict("structured_payload", self.structured_payload)
        _validate_true(self, ["bounded", "redacted"])
        _validate_false(self, ["written_to_file", "sent_externally"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopBundleView:
    bundle_view_id: str
    version: str
    approval_summary: str
    workspace_summary: str
    sandbox_apply_summary: str
    retest_summary: str
    outcome_comparison_summary: str
    process_state_summary: str
    self_prompt_summary: str
    human_handoff_summary: str
    blocked_actions_summary: str
    ready_for_v0399_consolidation_input: bool
    bundle_complete: bool
    bundle_warnings: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in [
            "bundle_view_id",
            "version",
            "approval_summary",
            "workspace_summary",
            "sandbox_apply_summary",
            "retest_summary",
            "outcome_comparison_summary",
            "process_state_summary",
            "self_prompt_summary",
            "human_handoff_summary",
            "blocked_actions_summary",
        ]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("bundle_warnings", self.bundle_warnings)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopHandoffPacket:
    handoff_packet_id: str
    version: str
    handoff_title: str
    handoff_summary: str
    human_decision_points: list[str]
    safe_next_steps: list[str]
    blocked_runtime_actions: list[str]
    artifact_refs: list[str]
    ready_for_v0399_consolidation_input: bool
    human_action_required: bool
    auto_continue_allowed: bool = False
    sent_externally: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["handoff_packet_id", "version", "handoff_title", "handoff_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["human_decision_points", "safe_next_steps", "blocked_runtime_actions", "artifact_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_true(self, ["human_action_required"])
        _validate_false(self, ["auto_continue_allowed", "sent_externally"])
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceResult:
    result_id: str
    version: str
    invocation_id: str
    decision_id: str
    command_kind: RepairCLILoopSurfaceCommandKind | str
    rendered_view: RepairCLILoopRenderedView | None
    denied_command: RepairCLIDeniedLoopCommand | None
    bundle_view: RepairCLILoopBundleView | None
    handoff_packet: RepairCLILoopHandoffPacket | None
    status: RepairCLILoopSurfaceStatus | str
    disposition: RepairCLILoopSurfaceDisposition | str
    result_summary: str
    preview_rendered: bool
    command_denied: bool
    runtime_executed: bool = False
    apply_executed: bool = False
    retest_executed: bool = False
    prompt_submitted: bool = False
    model_invoked: bool = False
    subagent_invoked: bool = False
    external_agent_invoked: bool = False
    auto_continued: bool = False
    shell_used: bool = False
    subprocess_used: bool = False
    arbitrary_command_executed: bool = False
    file_written: bool = False
    file_exported: bool = False
    sent_externally: bool = False
    trace_persisted: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["result_id", "version", "invocation_id", "decision_id", "result_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, UNSAFE_RESULT_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceReport:
    cli_surface_report_id: str
    version: str
    cli_surface_input_id: str
    invocation: RepairCLILoopInvocation
    decision: RepairCLILoopSurfaceDecision
    result: RepairCLILoopSurfaceResult
    report_summary: str
    ready_for_v0399_consolidation_input: bool
    surface_completed: bool
    preview_only: bool
    runtime_executed: bool = False
    apply_executed: bool = False
    retest_executed: bool = False
    prompt_executed: bool = False
    model_invoked: bool = False
    subagent_invoked: bool = False
    external_agent_invoked: bool = False
    autonomous_loop_continued: bool = False
    trace_persisted: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["cli_surface_report_id", "version", "cli_surface_input_id", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, ["preview_only"])
        _validate_false(self, UNSAFE_REPORT_NAMES)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V0398ReadinessReport:
    report_id: str
    version: str
    release_name: str
    track_name: str
    cli_surface_report: RepairCLILoopSurfaceReport | None
    decision: RepairCLILoopSurfaceDecision
    flags: RepairCLILoopSurfaceFlagSet
    source_refs: list[RepairCLILoopSurfaceSourceRef]
    report_summary: str
    ready_for_v0399_consolidation: bool
    ready_for_cli_loop_state_surface: bool
    ready_for_cli_command_registry: bool
    ready_for_cli_invocation_parser: bool
    ready_for_cli_preview_renderer: bool
    ready_for_cli_loop_bundle_preview: bool
    ready_for_cli_human_handoff_preview: bool
    ready_for_future_v0399_consolidation_input: bool
    surface_completed: bool
    preview_only: bool
    cli_runtime_execution_enabled: bool = False
    cli_apply_execution_enabled: bool = False
    cli_retest_execution_enabled: bool = False
    cli_prompt_submission_enabled: bool = False
    cli_model_invocation_enabled: bool = False
    cli_subagent_invocation_enabled: bool = False
    cli_external_agent_enabled: bool = False
    cli_auto_continue_enabled: bool = False
    shell_enabled: bool = False
    subprocess_enabled: bool = False
    arbitrary_command_enabled: bool = False
    file_export_enabled: bool = False
    external_send_enabled: bool = False
    trace_persistence_enabled: bool = False
    dominion_runtime_enabled: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["report_id", "version", "release_name", "track_name", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, ["preview_only"])
        _validate_list("source_refs", self.source_refs)
        _validate_false(self, UNSAFE_READINESS_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceValidationFinding:
    finding_id: str
    finding_summary: str
    risk_kind: RepairCLILoopSurfaceRiskKind | str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairCLILoopSurfaceValidationFinding]
    preview_only_confirmed: bool
    no_apply_execution_confirmed: bool
    no_retest_execution_confirmed: bool
    no_prompt_submission_confirmed: bool
    no_model_invocation_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_external_agent_confirmed: bool
    no_shell_confirmed: bool
    no_subprocess_confirmed: bool
    no_arbitrary_command_confirmed: bool
    no_file_export_confirmed: bool
    no_external_send_confirmed: bool
    no_trace_persistence_confirmed: bool
    no_pig_execution_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_production_certification_confirmed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("findings", self.findings)
        _validate_true(
            self,
            [
                "preview_only_confirmed",
                "no_apply_execution_confirmed",
                "no_retest_execution_confirmed",
                "no_prompt_submission_confirmed",
                "no_model_invocation_confirmed",
                "no_subagent_invocation_confirmed",
                "no_external_agent_confirmed",
                "no_shell_confirmed",
                "no_subprocess_confirmed",
                "no_arbitrary_command_confirmed",
                "no_file_export_confirmed",
                "no_external_send_confirmed",
                "no_trace_persistence_confirmed",
                "no_pig_execution_confirmed",
                "no_dominion_runtime_confirmed",
                "no_production_certification_confirmed",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfaceRunPreview:
    preview_id: str
    version: str
    preview_summary: str
    planned_preview_steps: list[str]
    preview_only: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_id", self.preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("planned_preview_steps", self.planned_preview_steps)
        if self.preview_only is not True or self.ready_for_execution is not False:
            raise ValueError("run preview must remain preview-only and not execution-ready")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairCLILoopSurfacePreviewOnlyGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_cli_runtime_execution: bool = True
    no_cli_apply_execution: bool = True
    no_cli_retest_execution: bool = True
    no_prompt_submission: bool = True
    no_model_invocation: bool = True
    no_prompt_execution: bool = True
    no_next_action_execution: bool = True
    no_subagent_invocation: bool = True
    no_external_agent: bool = True
    no_shell: bool = True
    no_subprocess: bool = True
    no_arbitrary_command: bool = True
    no_dependency_install: bool = True
    no_network_access: bool = True
    no_file_export: bool = True
    no_external_send: bool = True
    no_trace_persistence: bool = True
    no_ocel_write: bool = True
    no_ocpx_persistence: bool = True
    no_pig_execution: bool = True
    no_autonomous_loop: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_repair_execution: bool = True
    no_dominion_runtime: bool = True
    no_production_certification: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_true(
            self,
            [
                "no_cli_runtime_execution",
                "no_cli_apply_execution",
                "no_cli_retest_execution",
                "no_prompt_submission",
                "no_model_invocation",
                "no_prompt_execution",
                "no_next_action_execution",
                "no_subagent_invocation",
                "no_external_agent",
                "no_shell",
                "no_subprocess",
                "no_arbitrary_command",
                "no_dependency_install",
                "no_network_access",
                "no_file_export",
                "no_external_send",
                "no_trace_persistence",
                "no_ocel_write",
                "no_ocpx_persistence",
                "no_pig_execution",
                "no_autonomous_loop",
                "no_retry_loop",
                "no_multi_cycle_loop",
                "no_repair_execution",
                "no_dominion_runtime",
                "no_production_certification",
            ],
        )
        _validate_dict("metadata", self.metadata)


def build_repair_cli_loop_surface_flags(**overrides: Any) -> RepairCLILoopSurfaceFlagSet:
    return RepairCLILoopSurfaceFlagSet(**_with_overrides({"flag_set_id": "v0398-cli-surface-flags", "version": V0398_VERSION}, overrides))


def build_repair_cli_loop_surface_source_ref(**overrides: Any) -> RepairCLILoopSurfaceSourceRef:
    defaults = {
        "source_ref_id": "v0398-source-ref",
        "source_kind": RepairCLILoopSurfaceSourceKind.V0397_SELF_PROMPTING_DRAFT_PACKET,
        "source_id": "v0397-draft-packet",
        "source_summary": "Supplied self-prompting draft packet metadata for CLI preview.",
        "evidence_refs": ["v0397-draft-packet"],
    }
    return RepairCLILoopSurfaceSourceRef(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_command_spec(**overrides: Any) -> RepairCLILoopCommandSpec:
    defaults = {
        "command_spec_id": "v0398-command-status",
        "version": V0398_VERSION,
        "command_kind": RepairCLILoopSurfaceCommandKind.STATUS,
        "command_name": "status",
        "aliases": ["st"],
        "description": "Render CLI loop-state status preview metadata.",
        "view_kind": RepairCLILoopSurfaceViewKind.STATUS_VIEW,
        "output_formats": [RepairCLILoopSurfaceOutputFormat.TEXT, RepairCLILoopSurfaceOutputFormat.MARKDOWN, RepairCLILoopSurfaceOutputFormat.JSON_LIKE],
        "preview_only": True,
        "enabled": True,
        "denied_by_default": False,
        "risk_kinds": [],
    }
    return RepairCLILoopCommandSpec(**_with_overrides(defaults, overrides))


def _safe_spec(command_kind: RepairCLILoopSurfaceCommandKind, command_name: str, view_kind: RepairCLILoopSurfaceViewKind, aliases: list[str] | None = None) -> RepairCLILoopCommandSpec:
    return build_repair_cli_loop_command_spec(
        command_spec_id=f"v0398-command-{command_kind.value}",
        command_kind=command_kind,
        command_name=command_name,
        aliases=aliases or [],
        description=f"Render {command_kind.value} preview metadata.",
        view_kind=view_kind,
    )


def _denied_spec(command_kind: RepairCLILoopSurfaceCommandKind, command_name: str, risks: list[RepairCLILoopSurfaceRiskKind]) -> RepairCLILoopCommandSpec:
    return build_repair_cli_loop_command_spec(
        command_spec_id=f"v0398-command-{command_kind.value}",
        command_kind=command_kind,
        command_name=command_name,
        aliases=[],
        description=f"Classify {command_name} as a denied runtime command.",
        view_kind=RepairCLILoopSurfaceViewKind.DENIED_COMMAND_VIEW,
        enabled=True,
        denied_by_default=True,
        risk_kinds=risks,
    )


def default_repair_cli_loop_command_specs() -> list[RepairCLILoopCommandSpec]:
    specs = [
        _safe_spec(kind, kind.value, COMMAND_TO_VIEW[kind])
        for kind in SAFE_COMMAND_KINDS
        if kind in COMMAND_TO_VIEW
    ]
    denied = [
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_APPLY, "apply", [RepairCLILoopSurfaceRiskKind.APPLY_EXECUTION_CONFUSION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_RETEST, "retest", [RepairCLILoopSurfaceRiskKind.RETEST_EXECUTION_CONFUSION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_RUN_TESTS, "test", [RepairCLILoopSurfaceRiskKind.RETEST_EXECUTION_CONFUSION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_PROMPT_SUBMIT, "prompt-submit", [RepairCLILoopSurfaceRiskKind.PROMPT_EXECUTION_CONFUSION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_MODEL_CALL, "model", [RepairCLILoopSurfaceRiskKind.MODEL_INVOCATION_CONFUSION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_SUBAGENT_INVOKE, "subagent", [RepairCLILoopSurfaceRiskKind.SUBAGENT_INVOCATION_CONFUSION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_AUTO_CONTINUE, "auto-continue", [RepairCLILoopSurfaceRiskKind.AUTONOMOUS_LOOP_RUNTIME_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_SHELL, "shell", [RepairCLILoopSurfaceRiskKind.SHELL_EXECUTION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_SUBPROCESS, "subprocess", [RepairCLILoopSurfaceRiskKind.RAW_SUBPROCESS_EXECUTION_RISK]),
        _denied_spec(RepairCLILoopSurfaceCommandKind.DENIED_FILE_EXPORT, "export", [RepairCLILoopSurfaceRiskKind.FILE_EXPORT_RISK]),
    ]
    return specs + denied


def default_repair_cli_loop_surface_policy(**overrides: Any) -> RepairCLILoopSurfacePolicy:
    defaults = {
        "policy_id": "v0398-cli-surface-policy",
        "version": V0398_VERSION,
        "allowed_command_kinds": SAFE_COMMAND_KINDS.copy(),
        "denied_command_kinds": DENIED_COMMAND_KINDS.copy(),
        "allowed_view_kinds": [item for item in RepairCLILoopSurfaceViewKind],
        "allowed_output_formats": [item for item in RepairCLILoopSurfaceOutputFormat],
        "prohibited_argv_fragments": ["apply", "retest", "test", "shell", "subprocess", "export", "send", "model", "subagent"],
    }
    return RepairCLILoopSurfacePolicy(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_surface_policy(**overrides: Any) -> RepairCLILoopSurfacePolicy:
    return default_repair_cli_loop_surface_policy(**overrides)


def build_repair_cli_loop_surface_input(**overrides: Any) -> RepairCLILoopSurfaceInput:
    defaults = {
        "cli_surface_input_id": "v0398-cli-surface-input",
        "version": V0398_VERSION,
        "argv": ["status"],
        "requested_command": "status",
        "artifact_context": {
            "approval_summary": "Approval gate metadata available.",
            "workspace_summary": "Workspace isolation metadata available.",
            "sandbox_apply_summary": "Sandbox apply result metadata available.",
            "retest_summary": "Post-apply re-test metadata available.",
            "outcome_comparison_summary": "Outcome comparison metadata available.",
            "process_state_summary": "Process-state reconstruction metadata available.",
            "self_prompt_summary": "Self-prompt draft metadata available.",
            "human_handoff_summary": "Human handoff remains mandatory.",
        },
        "source_refs": [build_repair_cli_loop_surface_source_ref()],
        "prohibited_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "task_summary": "Render preview-only CLI loop-state surface metadata.",
    }
    return RepairCLILoopSurfaceInput(**_with_overrides(defaults, overrides))


def classify_repair_cli_loop_command(argv: list[str]) -> RepairCLILoopSurfaceCommandKind:
    if not argv:
        return RepairCLILoopSurfaceCommandKind.STATUS
    command = str(argv[0]).strip().lower().replace("-", "_")
    aliases = {
        "help": RepairCLILoopSurfaceCommandKind.HELP,
        "--help": RepairCLILoopSurfaceCommandKind.HELP,
        "-h": RepairCLILoopSurfaceCommandKind.HELP,
        "status": RepairCLILoopSurfaceCommandKind.STATUS,
        "st": RepairCLILoopSurfaceCommandKind.STATUS,
        "approval": RepairCLILoopSurfaceCommandKind.APPROVAL_PREVIEW,
        "approval_preview": RepairCLILoopSurfaceCommandKind.APPROVAL_PREVIEW,
        "workspace": RepairCLILoopSurfaceCommandKind.WORKSPACE_PREVIEW,
        "workspace_preview": RepairCLILoopSurfaceCommandKind.WORKSPACE_PREVIEW,
        "sandbox_apply_preview": RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW,
        "apply_preview": RepairCLILoopSurfaceCommandKind.SANDBOX_APPLY_PREVIEW,
        "retest_preview": RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW,
        "post_apply_retest_preview": RepairCLILoopSurfaceCommandKind.POST_APPLY_RETEST_PREVIEW,
        "comparison": RepairCLILoopSurfaceCommandKind.OUTCOME_COMPARISON_PREVIEW,
        "outcome_comparison_preview": RepairCLILoopSurfaceCommandKind.OUTCOME_COMPARISON_PREVIEW,
        "process_state": RepairCLILoopSurfaceCommandKind.PROCESS_STATE_PREVIEW,
        "process_state_preview": RepairCLILoopSurfaceCommandKind.PROCESS_STATE_PREVIEW,
        "self_prompt": RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW,
        "self_prompt_draft_preview": RepairCLILoopSurfaceCommandKind.SELF_PROMPT_DRAFT_PREVIEW,
        "subagent_prompt": RepairCLILoopSurfaceCommandKind.SUBAGENT_PROMPT_DRAFT_PREVIEW,
        "subagent_prompt_draft_preview": RepairCLILoopSurfaceCommandKind.SUBAGENT_PROMPT_DRAFT_PREVIEW,
        "handoff": RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW,
        "human_handoff_preview": RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW,
        "bundle": RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW,
        "loop_bundle_preview": RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW,
        "blocked": RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW,
        "blocked_actions_preview": RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW,
        "readiness": RepairCLILoopSurfaceCommandKind.READINESS_PREVIEW,
        "consolidation": RepairCLILoopSurfaceCommandKind.CONSOLIDATION_HANDOFF_PREVIEW,
        "consolidation_handoff_preview": RepairCLILoopSurfaceCommandKind.CONSOLIDATION_HANDOFF_PREVIEW,
        "noop": RepairCLILoopSurfaceCommandKind.NO_OP,
        "no_op": RepairCLILoopSurfaceCommandKind.NO_OP,
        "apply": RepairCLILoopSurfaceCommandKind.DENIED_APPLY,
        "retest": RepairCLILoopSurfaceCommandKind.DENIED_RETEST,
        "test": RepairCLILoopSurfaceCommandKind.DENIED_RUN_TESTS,
        "run_tests": RepairCLILoopSurfaceCommandKind.DENIED_RUN_TESTS,
        "live_apply": RepairCLILoopSurfaceCommandKind.DENIED_LIVE_APPLY,
        "apply_patch": RepairCLILoopSurfaceCommandKind.DENIED_APPLY_PATCH,
        "git_apply": RepairCLILoopSurfaceCommandKind.DENIED_GIT_APPLY,
        "prompt_submit": RepairCLILoopSurfaceCommandKind.DENIED_PROMPT_SUBMIT,
        "model": RepairCLILoopSurfaceCommandKind.DENIED_MODEL_CALL,
        "model_call": RepairCLILoopSurfaceCommandKind.DENIED_MODEL_CALL,
        "next_action_execute": RepairCLILoopSurfaceCommandKind.DENIED_NEXT_ACTION_EXECUTE,
        "subagent": RepairCLILoopSurfaceCommandKind.DENIED_SUBAGENT_INVOKE,
        "external_agent": RepairCLILoopSurfaceCommandKind.DENIED_EXTERNAL_AGENT,
        "auto_continue": RepairCLILoopSurfaceCommandKind.DENIED_AUTO_CONTINUE,
        "retry": RepairCLILoopSurfaceCommandKind.DENIED_RETRY_LOOP,
        "multi_cycle": RepairCLILoopSurfaceCommandKind.DENIED_MULTI_CYCLE_LOOP,
        "repair": RepairCLILoopSurfaceCommandKind.DENIED_REPAIR_EXECUTE,
        "shell": RepairCLILoopSurfaceCommandKind.DENIED_SHELL,
        "subprocess": RepairCLILoopSurfaceCommandKind.DENIED_SUBPROCESS,
        "cmd": RepairCLILoopSurfaceCommandKind.DENIED_ARBITRARY_COMMAND,
        "install": RepairCLILoopSurfaceCommandKind.DENIED_DEPENDENCY_INSTALL,
        "network": RepairCLILoopSurfaceCommandKind.DENIED_NETWORK,
        "export": RepairCLILoopSurfaceCommandKind.DENIED_FILE_EXPORT,
        "send": RepairCLILoopSurfaceCommandKind.DENIED_EXTERNAL_SEND,
        "trace": RepairCLILoopSurfaceCommandKind.DENIED_TRACE_PERSIST,
        "ocel": RepairCLILoopSurfaceCommandKind.DENIED_OCEL_WRITE,
        "ocpx": RepairCLILoopSurfaceCommandKind.DENIED_OCPX_PERSIST,
        "pig": RepairCLILoopSurfaceCommandKind.DENIED_PIG_EXECUTE,
        "dominion": RepairCLILoopSurfaceCommandKind.DENIED_DOMINION,
    }
    return aliases.get(command, RepairCLILoopSurfaceCommandKind.UNKNOWN)


def build_repair_cli_loop_invocation(**overrides: Any) -> RepairCLILoopInvocation:
    argv = overrides.pop("argv", ["status"])
    command_kind = overrides.pop("command_kind", classify_repair_cli_loop_command(argv))
    defaults = {
        "invocation_id": "v0398-cli-invocation",
        "version": V0398_VERSION,
        "argv": argv,
        "command_kind": command_kind,
        "output_format": RepairCLILoopSurfaceOutputFormat.TEXT,
        "parsed_args": {"command": argv[0] if argv else "status", "argv_count": len(argv)},
        "invocation_summary": "CLI-like argv parsed into preview metadata only.",
    }
    return RepairCLILoopInvocation(**_with_overrides(defaults, overrides))


def parse_repair_cli_loop_invocation(cli_input: RepairCLILoopSurfaceInput) -> RepairCLILoopInvocation:
    argv = cli_input.argv[:16]
    bounded_argv = [str(item)[:120] for item in argv]
    return build_repair_cli_loop_invocation(argv=bounded_argv)


def _risk_for_command(command_kind: RepairCLILoopSurfaceCommandKind | str) -> list[RepairCLILoopSurfaceRiskKind]:
    value = command_kind.value if isinstance(command_kind, RepairCLILoopSurfaceCommandKind) else str(command_kind)
    if "apply" in value:
        return [RepairCLILoopSurfaceRiskKind.APPLY_EXECUTION_CONFUSION_RISK]
    if "retest" in value or "test" in value:
        return [RepairCLILoopSurfaceRiskKind.RETEST_EXECUTION_CONFUSION_RISK]
    if "prompt" in value:
        return [RepairCLILoopSurfaceRiskKind.PROMPT_EXECUTION_CONFUSION_RISK]
    if "model" in value:
        return [RepairCLILoopSurfaceRiskKind.MODEL_INVOCATION_CONFUSION_RISK]
    if "subagent" in value:
        return [RepairCLILoopSurfaceRiskKind.SUBAGENT_INVOCATION_CONFUSION_RISK]
    if "shell" in value:
        return [RepairCLILoopSurfaceRiskKind.SHELL_EXECUTION_RISK]
    if "subprocess" in value:
        return [RepairCLILoopSurfaceRiskKind.RAW_SUBPROCESS_EXECUTION_RISK]
    if "export" in value:
        return [RepairCLILoopSurfaceRiskKind.FILE_EXPORT_RISK]
    if "dominion" in value:
        return [RepairCLILoopSurfaceRiskKind.DOMINION_RUNTIME_RISK]
    return [RepairCLILoopSurfaceRiskKind.CLI_EXECUTION_CONFUSION_RISK]


def build_repair_cli_loop_surface_decision(**overrides: Any) -> RepairCLILoopSurfaceDecision:
    command_kind = overrides.pop("command_kind", RepairCLILoopSurfaceCommandKind.STATUS)
    preview_allowed = command_kind in SAFE_COMMAND_KINDS
    defaults = {
        "cli_decision_id": "v0398-cli-decision",
        "version": V0398_VERSION,
        "invocation_id": "v0398-cli-invocation",
        "decision_kind": COMMAND_TO_DECISION.get(command_kind, RepairCLILoopSurfaceDecisionKind.DENY_ARBITRARY_COMMAND),
        "status": RepairCLILoopSurfaceStatus.COMMAND_ALLOWED_FOR_PREVIEW if preview_allowed else RepairCLILoopSurfaceStatus.COMMAND_DENIED,
        "disposition": RepairCLILoopSurfaceDisposition.PREVIEW_RENDERED if preview_allowed else RepairCLILoopSurfaceDisposition.COMMAND_DENIED,
        "decision_summary": "CLI command is allowed for preview only." if preview_allowed else "CLI command is denied as runtime/action request.",
        "risk_kinds": [] if preview_allowed else _risk_for_command(command_kind),
        "evidence_refs": ["v0398-cli-invocation"],
        "preview_allowed": preview_allowed,
    }
    return RepairCLILoopSurfaceDecision(**_with_overrides(defaults, overrides))


def decide_repair_cli_loop_surface(invocation: RepairCLILoopInvocation) -> RepairCLILoopSurfaceDecision:
    return build_repair_cli_loop_surface_decision(invocation_id=invocation.invocation_id, command_kind=invocation.command_kind)


def build_repair_cli_denied_loop_command(**overrides: Any) -> RepairCLIDeniedLoopCommand:
    defaults = {
        "denied_command_id": "v0398-denied-command",
        "version": V0398_VERSION,
        "invocation_id": "v0398-cli-invocation",
        "command_kind": RepairCLILoopSurfaceCommandKind.DENIED_APPLY,
        "denied_summary": "Runtime command denied by CLI preview surface.",
        "reason": "v0.39.8 only renders preview metadata and grants no execution authority.",
        "risk_kinds": [RepairCLILoopSurfaceRiskKind.CLI_EXECUTION_CONFUSION_RISK],
        "safe_alternatives": ["status", "loop_bundle_preview", "blocked_actions_preview", "human_handoff_preview"],
        "evidence_refs": ["v0398-cli-invocation"],
    }
    return RepairCLIDeniedLoopCommand(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_rendered_view(**overrides: Any) -> RepairCLILoopRenderedView:
    text = overrides.pop("rendered_text", "v0.39.8 CLI preview surface: metadata only; no runtime action executed.")
    max_chars = overrides.pop("max_chars", 4000)
    bounded_text, truncated = _bounded(text, max_chars)
    defaults = {
        "rendered_view_id": "v0398-rendered-view",
        "version": V0398_VERSION,
        "view_kind": RepairCLILoopSurfaceViewKind.STATUS_VIEW,
        "output_format": RepairCLILoopSurfaceOutputFormat.TEXT,
        "title": "CLI Loop-State Surface Preview",
        "rendered_text": bounded_text,
        "structured_payload": {"preview_only": True, "ready_for_execution": False},
        "bounded": True,
        "redacted": True,
        "truncated": truncated,
    }
    return RepairCLILoopRenderedView(**_with_overrides(defaults, overrides))


def render_repair_cli_loop_help(*, max_chars: int = 4000) -> RepairCLILoopRenderedView:
    commands = ", ".join(kind.value for kind in SAFE_COMMAND_KINDS)
    return build_repair_cli_loop_rendered_view(
        view_kind=RepairCLILoopSurfaceViewKind.HELP_VIEW,
        title="CLI Preview Help",
        rendered_text=f"Preview-only commands: {commands}. Runtime commands are denied.",
        max_chars=max_chars,
    )


def render_repair_cli_loop_status(*, max_chars: int = 4000) -> RepairCLILoopRenderedView:
    return build_repair_cli_loop_rendered_view(
        view_kind=RepairCLILoopSurfaceViewKind.STATUS_VIEW,
        title="CLI Preview Status",
        rendered_text="v0.39.8 CLI loop-state surface is preview-only and ready for v0.39.9 design-stage handoff.",
        max_chars=max_chars,
    )


def render_repair_cli_blocked_actions(*, max_chars: int = 4000) -> RepairCLILoopRenderedView:
    return build_repair_cli_loop_rendered_view(
        view_kind=RepairCLILoopSurfaceViewKind.BLOCKED_ACTIONS_VIEW,
        title="Blocked Runtime Actions",
        rendered_text="Blocked: apply, re-test, prompt submission, model call, subagent invocation, shell, subprocess, export, send, trace persistence, Dominion.",
        structured_payload={"blocked_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy()},
        max_chars=max_chars,
    )


def render_repair_cli_loop_view(command_kind: RepairCLILoopSurfaceCommandKind | str, artifact_context: dict[str, Any] | None = None, *, max_chars: int = 4000) -> RepairCLILoopRenderedView:
    kind = command_kind if isinstance(command_kind, RepairCLILoopSurfaceCommandKind) else RepairCLILoopSurfaceCommandKind(str(command_kind))
    context = artifact_context or {}
    if kind == RepairCLILoopSurfaceCommandKind.HELP:
        return render_repair_cli_loop_help(max_chars=max_chars)
    if kind == RepairCLILoopSurfaceCommandKind.STATUS:
        return render_repair_cli_loop_status(max_chars=max_chars)
    if kind == RepairCLILoopSurfaceCommandKind.BLOCKED_ACTIONS_PREVIEW:
        return render_repair_cli_blocked_actions(max_chars=max_chars)
    view_kind = COMMAND_TO_VIEW.get(kind, RepairCLILoopSurfaceViewKind.UNKNOWN)
    label = kind.value.replace("_", " ")
    text = f"{label}: preview metadata only. Human handoff remains mandatory."
    payload = {"command_kind": kind.value, "artifact_context_keys": sorted(context.keys()), "preview_only": True}
    return build_repair_cli_loop_rendered_view(
        view_kind=view_kind,
        title=f"{label.title()}",
        rendered_text=text,
        structured_payload=payload,
        max_chars=max_chars,
    )


def build_repair_cli_loop_bundle_view(**overrides: Any) -> RepairCLILoopBundleView:
    defaults = {
        "bundle_view_id": "v0398-loop-bundle",
        "version": V0398_VERSION,
        "approval_summary": "Approval artifact and process-state gate metadata are available.",
        "workspace_summary": "Workspace isolation metadata is available.",
        "sandbox_apply_summary": "Sandbox apply result metadata is available for preview only.",
        "retest_summary": "Post-apply re-test metadata is available for preview only.",
        "outcome_comparison_summary": "Outcome comparison metadata is available.",
        "process_state_summary": "Process-state reconstruction metadata is available.",
        "self_prompt_summary": "Self-prompt and subagent prompt drafts are available as drafts only.",
        "human_handoff_summary": "Human handoff remains mandatory.",
        "blocked_actions_summary": "Runtime apply, re-test, prompt, model, subagent, shell, export, persistence, and Dominion actions are blocked.",
        "ready_for_v0399_consolidation_input": True,
        "bundle_complete": True,
        "bundle_warnings": [],
    }
    return RepairCLILoopBundleView(**_with_overrides(defaults, overrides))


def create_repair_cli_loop_bundle_view(artifact_context: dict[str, Any] | None = None) -> RepairCLILoopBundleView:
    context = artifact_context or {}
    return build_repair_cli_loop_bundle_view(
        approval_summary=str(context.get("approval_summary", "Approval artifact preview metadata available.")),
        workspace_summary=str(context.get("workspace_summary", "Workspace preview metadata available.")),
        sandbox_apply_summary=str(context.get("sandbox_apply_summary", "Sandbox apply preview metadata available.")),
        retest_summary=str(context.get("retest_summary", "Re-test preview metadata available.")),
        outcome_comparison_summary=str(context.get("outcome_comparison_summary", "Outcome comparison preview metadata available.")),
        process_state_summary=str(context.get("process_state_summary", "Process-state preview metadata available.")),
        self_prompt_summary=str(context.get("self_prompt_summary", "Self-prompt draft preview metadata available.")),
        human_handoff_summary=str(context.get("human_handoff_summary", "Human handoff preview metadata available.")),
    )


def build_repair_cli_loop_handoff_packet(**overrides: Any) -> RepairCLILoopHandoffPacket:
    defaults = {
        "handoff_packet_id": "v0398-handoff-packet",
        "version": V0398_VERSION,
        "handoff_title": "CLI preview human handoff",
        "handoff_summary": "Human review is required; no CLI runtime action has executed.",
        "human_decision_points": ["Review repair loop bundle", "Choose do nothing or future consolidation", "Do not treat preview as approval capture"],
        "safe_next_steps": ["status", "loop_bundle_preview", "blocked_actions_preview", "consolidation_handoff_preview"],
        "blocked_runtime_actions": PROHIBITED_RUNTIME_ACTIONS.copy(),
        "artifact_refs": ["v0397-draft-packet", "v0396-process-state-report", "v0395-outcome-comparison-report"],
        "ready_for_v0399_consolidation_input": True,
        "human_action_required": True,
    }
    return RepairCLILoopHandoffPacket(**_with_overrides(defaults, overrides))


def create_repair_cli_loop_handoff_packet(artifact_refs: list[str] | None = None) -> RepairCLILoopHandoffPacket:
    return build_repair_cli_loop_handoff_packet(artifact_refs=artifact_refs or ["v0397-draft-packet"])


def build_repair_cli_loop_surface_result(**overrides: Any) -> RepairCLILoopSurfaceResult:
    command_kind = overrides.pop("command_kind", RepairCLILoopSurfaceCommandKind.STATUS)
    preview = command_kind in SAFE_COMMAND_KINDS
    rendered_view = overrides.pop("rendered_view", render_repair_cli_loop_view(command_kind) if preview else None)
    denied_command = overrides.pop("denied_command", None if preview else build_repair_cli_denied_loop_command(command_kind=command_kind))
    bundle = overrides.pop("bundle_view", create_repair_cli_loop_bundle_view() if command_kind == RepairCLILoopSurfaceCommandKind.LOOP_BUNDLE_PREVIEW else None)
    handoff = overrides.pop("handoff_packet", create_repair_cli_loop_handoff_packet() if command_kind == RepairCLILoopSurfaceCommandKind.HUMAN_HANDOFF_PREVIEW else None)
    defaults = {
        "result_id": "v0398-cli-result",
        "version": V0398_VERSION,
        "invocation_id": "v0398-cli-invocation",
        "decision_id": "v0398-cli-decision",
        "command_kind": command_kind,
        "rendered_view": rendered_view,
        "denied_command": denied_command,
        "bundle_view": bundle,
        "handoff_packet": handoff,
        "status": RepairCLILoopSurfaceStatus.VIEW_RENDERED if preview else RepairCLILoopSurfaceStatus.COMMAND_DENIED,
        "disposition": RepairCLILoopSurfaceDisposition.PREVIEW_RENDERED if preview else RepairCLILoopSurfaceDisposition.COMMAND_DENIED,
        "result_summary": "CLI preview rendered without runtime execution." if preview else "CLI command denied without runtime execution.",
        "preview_rendered": preview,
        "command_denied": not preview,
    }
    return RepairCLILoopSurfaceResult(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_surface_report(**overrides: Any) -> RepairCLILoopSurfaceReport:
    cli_input = overrides.pop("cli_surface_input", build_repair_cli_loop_surface_input())
    invocation = overrides.pop("invocation", parse_repair_cli_loop_invocation(cli_input))
    decision = overrides.pop("decision", decide_repair_cli_loop_surface(invocation))
    result = overrides.pop("result", build_repair_cli_loop_surface_result(invocation_id=invocation.invocation_id, decision_id=decision.cli_decision_id, command_kind=invocation.command_kind))
    defaults = {
        "cli_surface_report_id": "v0398-cli-surface-report",
        "version": V0398_VERSION,
        "cli_surface_input_id": cli_input.cli_surface_input_id,
        "invocation": invocation,
        "decision": decision,
        "result": result,
        "report_summary": "v0.39.8 CLI loop-state surface completed as preview-only metadata.",
        "ready_for_v0399_consolidation_input": True,
        "surface_completed": True,
        "preview_only": True,
        "evidence_refs": ["v0398-cli-result"],
    }
    return RepairCLILoopSurfaceReport(**_with_overrides(defaults, overrides))


def run_repair_cli_loop_surface_preview(cli_input: RepairCLILoopSurfaceInput) -> RepairCLILoopSurfaceReport:
    return build_repair_cli_loop_surface_report(cli_surface_input=cli_input)


def create_repair_cli_loop_surface_report(cli_input: RepairCLILoopSurfaceInput) -> RepairCLILoopSurfaceReport:
    return run_repair_cli_loop_surface_preview(cli_input)


def build_repair_cli_loop_surface_validation_finding(**overrides: Any) -> RepairCLILoopSurfaceValidationFinding:
    defaults = {
        "finding_id": "v0398-validation-finding",
        "finding_summary": "CLI surface remains preview-only.",
        "risk_kind": RepairCLILoopSurfaceRiskKind.CLI_EXECUTION_CONFUSION_RISK,
        "blocked": False,
    }
    return RepairCLILoopSurfaceValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_surface_validation_report(**overrides: Any) -> RepairCLILoopSurfaceValidationReport:
    defaults = {
        "validation_report_id": "v0398-validation-report",
        "version": V0398_VERSION,
        "validation_summary": "Validation confirms CLI preview-only behavior and no runtime/export/persistence authority.",
        "findings": [build_repair_cli_loop_surface_validation_finding()],
        "preview_only_confirmed": True,
        "no_apply_execution_confirmed": True,
        "no_retest_execution_confirmed": True,
        "no_prompt_submission_confirmed": True,
        "no_model_invocation_confirmed": True,
        "no_subagent_invocation_confirmed": True,
        "no_external_agent_confirmed": True,
        "no_shell_confirmed": True,
        "no_subprocess_confirmed": True,
        "no_arbitrary_command_confirmed": True,
        "no_file_export_confirmed": True,
        "no_external_send_confirmed": True,
        "no_trace_persistence_confirmed": True,
        "no_pig_execution_confirmed": True,
        "no_dominion_runtime_confirmed": True,
        "no_production_certification_confirmed": True,
    }
    return RepairCLILoopSurfaceValidationReport(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_surface_run_preview(**overrides: Any) -> RepairCLILoopSurfaceRunPreview:
    defaults = {
        "preview_id": "v0398-run-preview",
        "version": V0398_VERSION,
        "preview_summary": "Preview lists CLI surface metadata steps only.",
        "planned_preview_steps": ["CLIInvocation", "CLIDecision", "RenderedView", "LoopBundleView", "HandoffPacket"],
    }
    return RepairCLILoopSurfaceRunPreview(**_with_overrides(defaults, overrides))


def build_repair_cli_loop_surface_preview_only_guarantee(**overrides: Any) -> RepairCLILoopSurfacePreviewOnlyGuarantee:
    defaults = {
        "guarantee_id": "v0398-preview-only-guarantee",
        "version": V0398_VERSION,
        "guarantee_summary": "v0.39.8 renders CLI preview metadata only and blocks runtime/export/persistence.",
    }
    return RepairCLILoopSurfacePreviewOnlyGuarantee(**_with_overrides(defaults, overrides))


def build_v0398_readiness_report(**overrides: Any) -> V0398ReadinessReport:
    report = overrides.pop("cli_surface_report", build_repair_cli_loop_surface_report())
    defaults = {
        "report_id": "v0398-readiness-report",
        "version": V0398_VERSION,
        "release_name": V0398_RELEASE_NAME,
        "track_name": V039_TRACK_NAME,
        "cli_surface_report": report,
        "decision": report.decision,
        "flags": build_repair_cli_loop_surface_flags(),
        "source_refs": [build_repair_cli_loop_surface_source_ref()],
        "report_summary": "v0.39.8 CLI preview surface is ready for v0.39.9 design-stage handoff only.",
        "ready_for_v0399_consolidation": True,
        "ready_for_cli_loop_state_surface": True,
        "ready_for_cli_command_registry": True,
        "ready_for_cli_invocation_parser": True,
        "ready_for_cli_preview_renderer": True,
        "ready_for_cli_loop_bundle_preview": True,
        "ready_for_cli_human_handoff_preview": True,
        "ready_for_future_v0399_consolidation_input": True,
        "surface_completed": True,
        "preview_only": True,
    }
    return V0398ReadinessReport(**_with_overrides(defaults, overrides))


def repair_cli_loop_surface_flags_preserve_no_execution(flags: RepairCLILoopSurfaceFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_cli_loop_surface_policy_blocks_runtime(policy: RepairCLILoopSurfacePolicy) -> bool:
    return all(getattr(policy, name) is False for name in UNSAFE_POLICY_NAMES)


def repair_cli_loop_invocation_is_not_shell(invocation: RepairCLILoopInvocation) -> bool:
    return invocation.shell_used is False and invocation.subprocess_used is False and invocation.arbitrary_command_executed is False


def repair_cli_loop_decision_is_preview_only(decision: RepairCLILoopSurfaceDecision) -> bool:
    return all(getattr(decision, name) is False for name in UNSAFE_DECISION_NAMES)


def repair_cli_loop_result_is_not_runtime(result: RepairCLILoopSurfaceResult) -> bool:
    return all(getattr(result, name) is False for name in UNSAFE_RESULT_NAMES)


def repair_cli_loop_report_is_preview_only(report: RepairCLILoopSurfaceReport) -> bool:
    return report.preview_only is True and all(getattr(report, name) is False for name in UNSAFE_REPORT_NAMES)


def v0398_readiness_report_is_not_execution_ready(report: V0398ReadinessReport) -> bool:
    return report.preview_only is True and all(getattr(report, name) is False for name in UNSAFE_READINESS_NAMES) and repair_cli_loop_surface_flags_preserve_no_execution(report.flags)
