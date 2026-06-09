from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0388_VERSION = "v0.38.8"
V0388_RELEASE_NAME = "v0.38.8 CLI Repair Proposal Surface"

SAFE_REPAIR_CLI_COMMAND_NAMES = (
    "repair-proposal-help",
    "repair-proposal-status",
    "repair-boundary-preview",
    "repair-evidence-preview",
    "repair-source-context-preview",
    "repair-scope-preview",
    "repair-patch-metadata-preview",
    "repair-safety-preview",
    "repair-review-packet-preview",
    "repair-loop-packet-preview",
    "repair-proposal-bundle-preview",
    "repair-do-nothing-preview",
    "repair-handoff-preview",
    "repair-no-op",
)

DENIED_REPAIR_CLI_COMMAND_NAMES = (
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
    "cargo",
    "go",
    "make",
    "install",
    "dependency-install",
    "network",
    "curl",
    "wget",
    "git",
    "git-apply",
    "git apply",
    "apply-patch",
    "apply_patch",
    "repair-apply",
    "apply-repair",
    "sandbox-repair-apply",
    "live-apply",
    "live-write",
    "edit-live",
    "write-file",
    "write-patch-file",
    "export-file",
    "send-review",
    "send-email",
    "webhook",
    "run-tests",
    "rerun-tests",
    "auto-repair",
    "repair-loop",
    "retry-loop",
    "multi-cycle-loop",
    "run-codex",
    "run-claude-code",
    "run-opencode",
    "run-hermes",
    "run-openclaw",
    "external-agent",
    "provider-call",
    "model-call",
    "dominion",
    "infinite-loop",
    "recursive-agent",
    "approve",
    "grant-approval",
    "capture-approval",
    "approve-apply",
    "unknown",
)

SAFE_REPAIR_CLI_FLAG_NAMES = (
    "ready_for_v0389_bounded_repair_proposal_loop_consolidation",
    "ready_for_v039_human_approved_sandbox_repair_apply",
    "ready_for_cli_repair_proposal_surface",
    "ready_for_cli_command_registry",
    "ready_for_cli_argument_parsing",
    "ready_for_cli_help_command",
    "ready_for_cli_status_command",
    "ready_for_cli_boundary_preview",
    "ready_for_cli_evidence_preview",
    "ready_for_cli_source_context_preview",
    "ready_for_cli_scope_preview",
    "ready_for_cli_patch_metadata_preview",
    "ready_for_cli_safety_preview",
    "ready_for_cli_human_review_packet_preview",
    "ready_for_cli_loop_packet_preview",
    "ready_for_cli_bundle_preview",
    "ready_for_cli_do_nothing_preview",
    "ready_for_cli_handoff_preview",
    "ready_for_future_v0389_consolidation_input",
    "ready_for_future_v039_apply_handoff_metadata",
)

UNSAFE_REPAIR_CLI_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_cli_shell",
    "ready_for_cli_subprocess",
    "ready_for_arbitrary_command_execution",
    "ready_for_command_execution",
    "ready_for_cli_apply",
    "ready_for_cli_test_execution",
    "ready_for_cli_repair_execution",
    "ready_for_cli_approval_capture",
    "ready_for_cli_file_export",
    "ready_for_cli_external_send",
    "ready_for_ui_runtime",
    "ready_for_autonomous_loop_runtime",
    "ready_for_multi_cycle_loop",
    "ready_for_retry_loop",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
    "ready_for_human_approval_capture",
    "ready_for_approval_grant",
    "ready_for_apply_permission",
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

UNSAFE_REPAIR_CLI_POLICY_ALLOW_NAMES = (
    "allow_file_export",
    "allow_external_send",
    "allow_ui_runtime",
    "allow_shell",
    "allow_subprocess",
    "allow_arbitrary_command_execution",
    "allow_dependency_install",
    "allow_network_access",
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
    "allow_new_patch_generation",
    "allow_approval_capture",
    "allow_approval_grant",
    "allow_apply_permission",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_REPAIR_CLI_DECISION_NAMES = (
    "file_export_allowed",
    "external_send_allowed",
    "ui_runtime_allowed",
    "shell_allowed",
    "subprocess_allowed",
    "command_execution_allowed",
    "source_read_allowed",
    "source_write_allowed",
    "new_patch_generation_allowed",
    "patch_application_allowed",
    "apply_patch_allowed",
    "git_apply_allowed",
    "repair_execution_allowed",
    "test_execution_allowed",
    "approval_capture_allowed",
    "approval_grant_allowed",
    "apply_permission_allowed",
    "model_provider_invocation_allowed",
    "external_agent_allowed",
    "dominion_runtime_allowed",
    "production_certified",
)

UNSAFE_REPAIR_CLI_RESULT_NAMES = (
    "file_export_performed",
    "external_send_performed",
    "ui_runtime_invoked",
    "shell_used",
    "subprocess_used",
    "command_executed",
    "source_read_performed_by_v0388",
    "new_patch_metadata_generated_by_v0388",
    "file_write_performed",
    "patch_file_written",
    "file_edit_performed",
    "patch_applied",
    "apply_patch_called",
    "git_apply_called",
    "tests_run",
    "repair_executed",
    "approval_captured",
    "approval_granted",
    "apply_permission_granted",
    "model_invocation_performed",
    "external_agent_invoked",
    "dominion_runtime_invoked",
    "production_certified",
    "ready_for_execution",
)


class RepairCLISurfaceMode(StrEnum):
    CLI_REPAIR_PROPOSAL_SURFACE = "cli_repair_proposal_surface"
    CLI_COMMAND_REGISTRY = "cli_command_registry"
    CLI_ARGUMENT_PARSING = "cli_argument_parsing"
    CLI_HELP = "cli_help"
    CLI_STATUS = "cli_status"
    CLI_PREVIEW = "cli_preview"
    CLI_BUNDLE_PREVIEW = "cli_bundle_preview"
    CLI_HANDOFF_PREVIEW = "cli_handoff_preview"
    DENIED = "denied"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class RepairCLISourceKind(StrEnum):
    V0387_LOOP_PACKET = "v0387_loop_packet"
    V0387_LOOP_REPORT = "v0387_loop_report"
    V0386_HUMAN_REVIEW_PACKET = "v0386_human_review_packet"
    V0386_APPROVAL_REQUEST_CONTRACT = "v0386_approval_request_contract"
    V0385_SAFETY_REPORT = "v0385_safety_report"
    V0384_PROPOSED_PATCH_ENVELOPE = "v0384_proposed_patch_envelope"
    V0384_PROPOSED_DIFF_METADATA = "v0384_proposed_diff_metadata"
    V0384_PROPOSED_CODE_HUNK = "v0384_proposed_code_hunk"
    V0383_REPAIR_SCOPE_PLAN = "v0383_repair_scope_plan"
    V0382_SOURCE_CONTEXT_SNAPSHOT = "v0382_source_context_snapshot"
    V0381_EVIDENCE_BUNDLE = "v0381_evidence_bundle"
    V0380_REPAIR_PROPOSAL_BOUNDARY = "v0380_repair_proposal_boundary"
    V0379_TEST_RUNNER_CONSOLIDATION = "v0379_test_runner_consolidation"
    CLI_ARGV = "cli_argv"
    PARSED_ARGS = "parsed_args"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RepairCLIStatus(StrEnum):
    UNKNOWN = "unknown"
    INITIALIZED = "initialized"
    PARSED = "parsed"
    DECISION_READY = "decision_ready"
    ALLOWED_PREVIEW = "allowed_preview"
    DENIED = "denied"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    COMPLETED_WITH_WARNINGS = "completed_with_warnings"
    SAFE_FAILED = "safe_failed"
    NO_OP = "no_op"
    FUTURE_GATED = "future_gated"


class RepairCLIReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_CONTRACT_READY = "cli_contract_ready"
    COMMAND_REGISTRY_READY = "command_registry_ready"
    ARGUMENT_PARSING_READY = "argument_parsing_ready"
    PREVIEW_SURFACE_READY = "preview_surface_ready"
    BUNDLE_PREVIEW_READY = "bundle_preview_ready"
    HANDOFF_PREVIEW_READY = "handoff_preview_ready"
    DESIGN_HANDOFF_READY_FOR_V0389 = "design_handoff_ready_for_v0389"
    FUTURE_HANDOFF_READY_FOR_V039 = "future_handoff_ready_for_v039"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairCLICommandKind(StrEnum):
    REPAIR_PROPOSAL_HELP = "repair_proposal_help"
    REPAIR_PROPOSAL_STATUS = "repair_proposal_status"
    REPAIR_BOUNDARY_PREVIEW = "repair_boundary_preview"
    REPAIR_EVIDENCE_PREVIEW = "repair_evidence_preview"
    REPAIR_SOURCE_CONTEXT_PREVIEW = "repair_source_context_preview"
    REPAIR_SCOPE_PREVIEW = "repair_scope_preview"
    REPAIR_PATCH_METADATA_PREVIEW = "repair_patch_metadata_preview"
    REPAIR_SAFETY_PREVIEW = "repair_safety_preview"
    REPAIR_REVIEW_PACKET_PREVIEW = "repair_review_packet_preview"
    REPAIR_LOOP_PACKET_PREVIEW = "repair_loop_packet_preview"
    REPAIR_PROPOSAL_BUNDLE_PREVIEW = "repair_proposal_bundle_preview"
    REPAIR_DO_NOTHING_PREVIEW = "repair_do_nothing_preview"
    REPAIR_HANDOFF_PREVIEW = "repair_handoff_preview"
    REPAIR_NO_OP = "repair_no_op"
    DENIED_SHELL = "denied_shell"
    DENIED_SUBPROCESS = "denied_subprocess"
    DENIED_DIRECT_PYTHON = "denied_direct_python"
    DENIED_DIRECT_PYTEST = "denied_direct_pytest"
    DENIED_PACKAGE_MANAGER = "denied_package_manager"
    DENIED_DEPENDENCY_INSTALL = "denied_dependency_install"
    DENIED_NETWORK = "denied_network"
    DENIED_FILE_WRITE = "denied_file_write"
    DENIED_PATCH_FILE_WRITE = "denied_patch_file_write"
    DENIED_LIVE_WRITE = "denied_live_write"
    DENIED_PATCH_APPLY = "denied_patch_apply"
    DENIED_APPLY_PATCH = "denied_apply_patch"
    DENIED_GIT_APPLY = "denied_git_apply"
    DENIED_REPAIR_APPLY = "denied_repair_apply"
    DENIED_REPAIR_EXECUTION = "denied_repair_execution"
    DENIED_AUTO_REPAIR = "denied_auto_repair"
    DENIED_RETRY_LOOP = "denied_retry_loop"
    DENIED_MULTI_CYCLE_LOOP = "denied_multi_cycle_loop"
    DENIED_APPROVAL_CAPTURE = "denied_approval_capture"
    DENIED_APPROVAL_GRANT = "denied_approval_grant"
    DENIED_MODEL_PROVIDER = "denied_model_provider"
    DENIED_EXTERNAL_AGENT = "denied_external_agent"
    DENIED_DOMINION = "denied_dominion"
    DENIED_UI_RUNTIME = "denied_ui_runtime"
    DENIED_EXTERNAL_SEND = "denied_external_send"
    UNKNOWN = "unknown"


class RepairCLIDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_BOUNDARY_PREVIEW = "allow_boundary_preview"
    ALLOW_EVIDENCE_PREVIEW = "allow_evidence_preview"
    ALLOW_SOURCE_CONTEXT_PREVIEW = "allow_source_context_preview"
    ALLOW_SCOPE_PREVIEW = "allow_scope_preview"
    ALLOW_PATCH_METADATA_PREVIEW = "allow_patch_metadata_preview"
    ALLOW_SAFETY_PREVIEW = "allow_safety_preview"
    ALLOW_REVIEW_PACKET_PREVIEW = "allow_review_packet_preview"
    ALLOW_LOOP_PACKET_PREVIEW = "allow_loop_packet_preview"
    ALLOW_BUNDLE_PREVIEW = "allow_bundle_preview"
    ALLOW_DO_NOTHING_PREVIEW = "allow_do_nothing_preview"
    ALLOW_HANDOFF_PREVIEW = "allow_handoff_preview"
    DENY_SHELL = "deny_shell"
    DENY_SUBPROCESS = "deny_subprocess"
    DENY_DIRECT_PYTHON = "deny_direct_python"
    DENY_DIRECT_PYTEST = "deny_direct_pytest"
    DENY_PACKAGE_MANAGER = "deny_package_manager"
    DENY_DEPENDENCY_INSTALL = "deny_dependency_install"
    DENY_NETWORK = "deny_network"
    DENY_FILE_WRITE = "deny_file_write"
    DENY_PATCH_FILE_WRITE = "deny_patch_file_write"
    DENY_PATCH_APPLY = "deny_patch_apply"
    DENY_REPAIR_APPLY = "deny_repair_apply"
    DENY_REPAIR_EXECUTION = "deny_repair_execution"
    DENY_APPROVAL_CAPTURE = "deny_approval_capture"
    DENY_APPROVAL_GRANT = "deny_approval_grant"
    DENY_MODEL_PROVIDER = "deny_model_provider"
    DENY_EXTERNAL_AGENT = "deny_external_agent"
    DENY_DOMINION = "deny_dominion"
    DENY_UI_RUNTIME = "deny_ui_runtime"
    DENY_EXTERNAL_SEND = "deny_external_send"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairCLIRiskKind(StrEnum):
    CLI_SHELL_CONFUSION_RISK = "cli_shell_confusion_risk"
    ARBITRARY_COMMAND_EXECUTION_RISK = "arbitrary_command_execution_risk"
    SUBPROCESS_EXECUTION_RISK = "subprocess_execution_risk"
    RAW_PYTHON_EXECUTION_RISK = "raw_python_execution_risk"
    RAW_PYTEST_EXECUTION_RISK = "raw_pytest_execution_risk"
    PACKAGE_MANAGER_RISK = "package_manager_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    FILE_WRITE_RISK = "file_write_risk"
    PATCH_FILE_WRITE_RISK = "patch_file_write_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    REPAIR_EXECUTION_RISK = "repair_execution_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    APPROVAL_CAPTURE_RISK = "approval_capture_risk"
    APPROVAL_GRANT_RISK = "approval_grant_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    UI_RUNTIME_RISK = "ui_runtime_risk"
    EXTERNAL_SEND_RISK = "external_send_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairCLIOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    STRUCTURED_ARTIFACT = "structured_artifact"
    COMPACT = "compact"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class RepairCLICommandDisposition(StrEnum):
    ALLOWED_PREVIEW = "allowed_preview"
    DENIED = "denied"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    FUTURE_GATED = "future_gated"
    UNKNOWN = "unknown"


SAFE_COMMAND_KIND_BY_NAME = {
    "repair-proposal-help": RepairCLICommandKind.REPAIR_PROPOSAL_HELP,
    "repair-proposal-status": RepairCLICommandKind.REPAIR_PROPOSAL_STATUS,
    "repair-boundary-preview": RepairCLICommandKind.REPAIR_BOUNDARY_PREVIEW,
    "repair-evidence-preview": RepairCLICommandKind.REPAIR_EVIDENCE_PREVIEW,
    "repair-source-context-preview": RepairCLICommandKind.REPAIR_SOURCE_CONTEXT_PREVIEW,
    "repair-scope-preview": RepairCLICommandKind.REPAIR_SCOPE_PREVIEW,
    "repair-patch-metadata-preview": RepairCLICommandKind.REPAIR_PATCH_METADATA_PREVIEW,
    "repair-safety-preview": RepairCLICommandKind.REPAIR_SAFETY_PREVIEW,
    "repair-review-packet-preview": RepairCLICommandKind.REPAIR_REVIEW_PACKET_PREVIEW,
    "repair-loop-packet-preview": RepairCLICommandKind.REPAIR_LOOP_PACKET_PREVIEW,
    "repair-proposal-bundle-preview": RepairCLICommandKind.REPAIR_PROPOSAL_BUNDLE_PREVIEW,
    "repair-do-nothing-preview": RepairCLICommandKind.REPAIR_DO_NOTHING_PREVIEW,
    "repair-handoff-preview": RepairCLICommandKind.REPAIR_HANDOFF_PREVIEW,
    "repair-no-op": RepairCLICommandKind.REPAIR_NO_OP,
}

ALLOW_DECISION_BY_COMMAND_KIND = {
    RepairCLICommandKind.REPAIR_PROPOSAL_HELP: RepairCLIDecisionKind.ALLOW_HELP,
    RepairCLICommandKind.REPAIR_PROPOSAL_STATUS: RepairCLIDecisionKind.ALLOW_STATUS,
    RepairCLICommandKind.REPAIR_BOUNDARY_PREVIEW: RepairCLIDecisionKind.ALLOW_BOUNDARY_PREVIEW,
    RepairCLICommandKind.REPAIR_EVIDENCE_PREVIEW: RepairCLIDecisionKind.ALLOW_EVIDENCE_PREVIEW,
    RepairCLICommandKind.REPAIR_SOURCE_CONTEXT_PREVIEW: RepairCLIDecisionKind.ALLOW_SOURCE_CONTEXT_PREVIEW,
    RepairCLICommandKind.REPAIR_SCOPE_PREVIEW: RepairCLIDecisionKind.ALLOW_SCOPE_PREVIEW,
    RepairCLICommandKind.REPAIR_PATCH_METADATA_PREVIEW: RepairCLIDecisionKind.ALLOW_PATCH_METADATA_PREVIEW,
    RepairCLICommandKind.REPAIR_SAFETY_PREVIEW: RepairCLIDecisionKind.ALLOW_SAFETY_PREVIEW,
    RepairCLICommandKind.REPAIR_REVIEW_PACKET_PREVIEW: RepairCLIDecisionKind.ALLOW_REVIEW_PACKET_PREVIEW,
    RepairCLICommandKind.REPAIR_LOOP_PACKET_PREVIEW: RepairCLIDecisionKind.ALLOW_LOOP_PACKET_PREVIEW,
    RepairCLICommandKind.REPAIR_PROPOSAL_BUNDLE_PREVIEW: RepairCLIDecisionKind.ALLOW_BUNDLE_PREVIEW,
    RepairCLICommandKind.REPAIR_DO_NOTHING_PREVIEW: RepairCLIDecisionKind.ALLOW_DO_NOTHING_PREVIEW,
    RepairCLICommandKind.REPAIR_HANDOFF_PREVIEW: RepairCLIDecisionKind.ALLOW_HANDOFF_PREVIEW,
    RepairCLICommandKind.REPAIR_NO_OP: RepairCLIDecisionKind.NO_OP,
}

DENIED_COMMAND_METADATA = {
    "shell": (RepairCLICommandKind.DENIED_SHELL, RepairCLIDecisionKind.DENY_SHELL, RepairCLIRiskKind.CLI_SHELL_CONFUSION_RISK),
    "bash": (RepairCLICommandKind.DENIED_SHELL, RepairCLIDecisionKind.DENY_SHELL, RepairCLIRiskKind.CLI_SHELL_CONFUSION_RISK),
    "powershell": (RepairCLICommandKind.DENIED_SHELL, RepairCLIDecisionKind.DENY_SHELL, RepairCLIRiskKind.CLI_SHELL_CONFUSION_RISK),
    "cmd": (RepairCLICommandKind.DENIED_SHELL, RepairCLIDecisionKind.DENY_SHELL, RepairCLIRiskKind.CLI_SHELL_CONFUSION_RISK),
    "python": (RepairCLICommandKind.DENIED_DIRECT_PYTHON, RepairCLIDecisionKind.DENY_DIRECT_PYTHON, RepairCLIRiskKind.RAW_PYTHON_EXECUTION_RISK),
    "pytest": (RepairCLICommandKind.DENIED_DIRECT_PYTEST, RepairCLIDecisionKind.DENY_DIRECT_PYTEST, RepairCLIRiskKind.RAW_PYTEST_EXECUTION_RISK),
    "unittest": (RepairCLICommandKind.DENIED_DIRECT_PYTEST, RepairCLIDecisionKind.DENY_DIRECT_PYTEST, RepairCLIRiskKind.RAW_PYTEST_EXECUTION_RISK),
    "npm": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "pnpm": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "yarn": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "pip": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "poetry": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "cargo": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "go": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "make": (RepairCLICommandKind.DENIED_PACKAGE_MANAGER, RepairCLIDecisionKind.DENY_PACKAGE_MANAGER, RepairCLIRiskKind.PACKAGE_MANAGER_RISK),
    "install": (RepairCLICommandKind.DENIED_DEPENDENCY_INSTALL, RepairCLIDecisionKind.DENY_DEPENDENCY_INSTALL, RepairCLIRiskKind.DEPENDENCY_INSTALL_RISK),
    "dependency-install": (RepairCLICommandKind.DENIED_DEPENDENCY_INSTALL, RepairCLIDecisionKind.DENY_DEPENDENCY_INSTALL, RepairCLIRiskKind.DEPENDENCY_INSTALL_RISK),
    "network": (RepairCLICommandKind.DENIED_NETWORK, RepairCLIDecisionKind.DENY_NETWORK, RepairCLIRiskKind.NETWORK_ACCESS_RISK),
    "curl": (RepairCLICommandKind.DENIED_NETWORK, RepairCLIDecisionKind.DENY_NETWORK, RepairCLIRiskKind.NETWORK_ACCESS_RISK),
    "wget": (RepairCLICommandKind.DENIED_NETWORK, RepairCLIDecisionKind.DENY_NETWORK, RepairCLIRiskKind.NETWORK_ACCESS_RISK),
    "git": (RepairCLICommandKind.DENIED_GIT_APPLY, RepairCLIDecisionKind.DENY_PATCH_APPLY, RepairCLIRiskKind.GIT_APPLY_RISK),
    "git-apply": (RepairCLICommandKind.DENIED_GIT_APPLY, RepairCLIDecisionKind.DENY_PATCH_APPLY, RepairCLIRiskKind.GIT_APPLY_RISK),
    "git apply": (RepairCLICommandKind.DENIED_GIT_APPLY, RepairCLIDecisionKind.DENY_PATCH_APPLY, RepairCLIRiskKind.GIT_APPLY_RISK),
    "apply-patch": (RepairCLICommandKind.DENIED_APPLY_PATCH, RepairCLIDecisionKind.DENY_PATCH_APPLY, RepairCLIRiskKind.APPLY_PATCH_RISK),
    "apply_patch": (RepairCLICommandKind.DENIED_APPLY_PATCH, RepairCLIDecisionKind.DENY_PATCH_APPLY, RepairCLIRiskKind.APPLY_PATCH_RISK),
    "repair-apply": (RepairCLICommandKind.DENIED_REPAIR_APPLY, RepairCLIDecisionKind.DENY_REPAIR_APPLY, RepairCLIRiskKind.REPAIR_EXECUTION_RISK),
    "apply-repair": (RepairCLICommandKind.DENIED_REPAIR_APPLY, RepairCLIDecisionKind.DENY_REPAIR_APPLY, RepairCLIRiskKind.REPAIR_EXECUTION_RISK),
    "sandbox-repair-apply": (RepairCLICommandKind.DENIED_REPAIR_APPLY, RepairCLIDecisionKind.DENY_REPAIR_APPLY, RepairCLIRiskKind.REPAIR_EXECUTION_RISK),
    "live-apply": (RepairCLICommandKind.DENIED_LIVE_WRITE, RepairCLIDecisionKind.DENY_FILE_WRITE, RepairCLIRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "live-write": (RepairCLICommandKind.DENIED_LIVE_WRITE, RepairCLIDecisionKind.DENY_FILE_WRITE, RepairCLIRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "edit-live": (RepairCLICommandKind.DENIED_LIVE_WRITE, RepairCLIDecisionKind.DENY_FILE_WRITE, RepairCLIRiskKind.LIVE_WORKSPACE_WRITE_RISK),
    "write-file": (RepairCLICommandKind.DENIED_FILE_WRITE, RepairCLIDecisionKind.DENY_FILE_WRITE, RepairCLIRiskKind.FILE_WRITE_RISK),
    "write-patch-file": (RepairCLICommandKind.DENIED_PATCH_FILE_WRITE, RepairCLIDecisionKind.DENY_PATCH_FILE_WRITE, RepairCLIRiskKind.PATCH_FILE_WRITE_RISK),
    "export-file": (RepairCLICommandKind.DENIED_FILE_WRITE, RepairCLIDecisionKind.DENY_FILE_WRITE, RepairCLIRiskKind.FILE_WRITE_RISK),
    "send-review": (RepairCLICommandKind.DENIED_EXTERNAL_SEND, RepairCLIDecisionKind.DENY_EXTERNAL_SEND, RepairCLIRiskKind.EXTERNAL_SEND_RISK),
    "send-email": (RepairCLICommandKind.DENIED_EXTERNAL_SEND, RepairCLIDecisionKind.DENY_EXTERNAL_SEND, RepairCLIRiskKind.EXTERNAL_SEND_RISK),
    "webhook": (RepairCLICommandKind.DENIED_EXTERNAL_SEND, RepairCLIDecisionKind.DENY_EXTERNAL_SEND, RepairCLIRiskKind.EXTERNAL_SEND_RISK),
    "run-tests": (RepairCLICommandKind.DENIED_DIRECT_PYTEST, RepairCLIDecisionKind.DENY_DIRECT_PYTEST, RepairCLIRiskKind.RAW_PYTEST_EXECUTION_RISK),
    "rerun-tests": (RepairCLICommandKind.DENIED_DIRECT_PYTEST, RepairCLIDecisionKind.DENY_DIRECT_PYTEST, RepairCLIRiskKind.RAW_PYTEST_EXECUTION_RISK),
    "auto-repair": (RepairCLICommandKind.DENIED_AUTO_REPAIR, RepairCLIDecisionKind.DENY_REPAIR_EXECUTION, RepairCLIRiskKind.AUTOMATIC_REPAIR_RISK),
    "repair-loop": (RepairCLICommandKind.DENIED_MULTI_CYCLE_LOOP, RepairCLIDecisionKind.DENY_REPAIR_EXECUTION, RepairCLIRiskKind.MULTI_CYCLE_LOOP_RISK),
    "retry-loop": (RepairCLICommandKind.DENIED_RETRY_LOOP, RepairCLIDecisionKind.DENY_REPAIR_EXECUTION, RepairCLIRiskKind.RETRY_LOOP_RISK),
    "multi-cycle-loop": (RepairCLICommandKind.DENIED_MULTI_CYCLE_LOOP, RepairCLIDecisionKind.DENY_REPAIR_EXECUTION, RepairCLIRiskKind.MULTI_CYCLE_LOOP_RISK),
    "run-codex": (RepairCLICommandKind.DENIED_EXTERNAL_AGENT, RepairCLIDecisionKind.DENY_EXTERNAL_AGENT, RepairCLIRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "run-claude-code": (RepairCLICommandKind.DENIED_EXTERNAL_AGENT, RepairCLIDecisionKind.DENY_EXTERNAL_AGENT, RepairCLIRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "run-opencode": (RepairCLICommandKind.DENIED_EXTERNAL_AGENT, RepairCLIDecisionKind.DENY_EXTERNAL_AGENT, RepairCLIRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "run-hermes": (RepairCLICommandKind.DENIED_EXTERNAL_AGENT, RepairCLIDecisionKind.DENY_EXTERNAL_AGENT, RepairCLIRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "run-openclaw": (RepairCLICommandKind.DENIED_EXTERNAL_AGENT, RepairCLIDecisionKind.DENY_EXTERNAL_AGENT, RepairCLIRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "external-agent": (RepairCLICommandKind.DENIED_EXTERNAL_AGENT, RepairCLIDecisionKind.DENY_EXTERNAL_AGENT, RepairCLIRiskKind.EXTERNAL_AGENT_EXECUTION_RISK),
    "provider-call": (RepairCLICommandKind.DENIED_MODEL_PROVIDER, RepairCLIDecisionKind.DENY_MODEL_PROVIDER, RepairCLIRiskKind.MODEL_PROVIDER_INVOCATION_RISK),
    "model-call": (RepairCLICommandKind.DENIED_MODEL_PROVIDER, RepairCLIDecisionKind.DENY_MODEL_PROVIDER, RepairCLIRiskKind.MODEL_PROVIDER_INVOCATION_RISK),
    "dominion": (RepairCLICommandKind.DENIED_DOMINION, RepairCLIDecisionKind.DENY_DOMINION, RepairCLIRiskKind.DOMINION_RUNTIME_RISK),
    "infinite-loop": (RepairCLICommandKind.DENIED_DOMINION, RepairCLIDecisionKind.DENY_DOMINION, RepairCLIRiskKind.DOMINION_RUNTIME_RISK),
    "recursive-agent": (RepairCLICommandKind.DENIED_DOMINION, RepairCLIDecisionKind.DENY_DOMINION, RepairCLIRiskKind.DOMINION_RUNTIME_RISK),
    "approve": (RepairCLICommandKind.DENIED_APPROVAL_GRANT, RepairCLIDecisionKind.DENY_APPROVAL_GRANT, RepairCLIRiskKind.APPROVAL_GRANT_RISK),
    "grant-approval": (RepairCLICommandKind.DENIED_APPROVAL_GRANT, RepairCLIDecisionKind.DENY_APPROVAL_GRANT, RepairCLIRiskKind.APPROVAL_GRANT_RISK),
    "capture-approval": (RepairCLICommandKind.DENIED_APPROVAL_CAPTURE, RepairCLIDecisionKind.DENY_APPROVAL_CAPTURE, RepairCLIRiskKind.APPROVAL_CAPTURE_RISK),
    "approve-apply": (RepairCLICommandKind.DENIED_APPROVAL_GRANT, RepairCLIDecisionKind.DENY_APPROVAL_GRANT, RepairCLIRiskKind.APPROVAL_GRANT_RISK),
    "unknown": (RepairCLICommandKind.UNKNOWN, RepairCLIDecisionKind.DENY, RepairCLIRiskKind.UNKNOWN),
}


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0388_VERSION not in version:
        raise ValueError("version must include v0.38.8")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name):
            raise ValueError(f"{name} must remain False for {V0388_VERSION}")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if not getattr(instance, name):
            raise ValueError(f"{name} must remain True for {V0388_VERSION}")


def _bounded_text(value: Any, limit: int = 1200) -> str:
    text = str(value)
    return text if len(text) <= limit else text[: limit - 15] + "...[truncated]"


def _normalize_command_name(argv: list[str]) -> str:
    if not argv:
        return "repair-no-op"
    first = str(argv[0]).strip().lower()
    if first == "git" and len(argv) > 1 and str(argv[1]).strip().lower() == "apply":
        return "git apply"
    return first or "unknown"


@dataclass(frozen=True, kw_only=True)
class RepairCLIFlagSet:
    flag_set_id: str
    version: str
    repair_cli_surface_layer_constructed: bool = True
    cli_command_registry_available: bool = True
    cli_argument_parsing_available: bool = True
    cli_preview_output_available: bool = True
    cli_denied_command_handling_available: bool = True
    cli_bundle_preview_available: bool = True
    cli_handoff_preview_available: bool = True
    ready_for_v0389_bounded_repair_proposal_loop_consolidation: bool = True
    ready_for_v039_human_approved_sandbox_repair_apply: bool = True
    ready_for_cli_repair_proposal_surface: bool = True
    ready_for_cli_command_registry: bool = True
    ready_for_cli_argument_parsing: bool = True
    ready_for_cli_help_command: bool = True
    ready_for_cli_status_command: bool = True
    ready_for_cli_boundary_preview: bool = True
    ready_for_cli_evidence_preview: bool = True
    ready_for_cli_source_context_preview: bool = True
    ready_for_cli_scope_preview: bool = True
    ready_for_cli_patch_metadata_preview: bool = True
    ready_for_cli_safety_preview: bool = True
    ready_for_cli_human_review_packet_preview: bool = True
    ready_for_cli_loop_packet_preview: bool = True
    ready_for_cli_bundle_preview: bool = True
    ready_for_cli_do_nothing_preview: bool = True
    ready_for_cli_handoff_preview: bool = True
    ready_for_future_v0389_consolidation_input: bool = True
    ready_for_future_v039_apply_handoff_metadata: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_cli_shell: bool = False
    ready_for_cli_subprocess: bool = False
    ready_for_arbitrary_command_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_cli_apply: bool = False
    ready_for_cli_test_execution: bool = False
    ready_for_cli_repair_execution: bool = False
    ready_for_cli_approval_capture: bool = False
    ready_for_cli_file_export: bool = False
    ready_for_cli_external_send: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_retry_loop: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_execution: bool = False
    ready_for_human_approval_capture: bool = False
    ready_for_approval_grant: bool = False
    ready_for_apply_permission: bool = False
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
        _validate_false(self, UNSAFE_REPAIR_CLI_FLAG_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairCLISourceRef:
    source_ref_id: str
    source_kind: RepairCLISourceKind | str
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
class RepairCLIArgumentSpec:
    argument_spec_id: str
    name: str
    required: bool = False
    allowed_values: list[str] = field(default_factory=list)
    prohibited_values: list[str] = field(default_factory=list)
    allowed_patterns: list[str] = field(default_factory=list)
    prohibited_patterns: list[str] = field(default_factory=list)
    allow_text_value: bool = True
    allow_ref_value: bool = True
    allow_json_value: bool = False
    max_value_chars: int = 200
    description: str = "Bounded CLI metadata argument."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("argument_spec_id", self.argument_spec_id)
        _require_non_blank("name", self.name)
        _require_non_blank("description", self.description)
        _validate_string_list("allowed_values", self.allowed_values)
        _validate_string_list("prohibited_values", self.prohibited_values)
        _validate_string_list("allowed_patterns", self.allowed_patterns)
        _validate_string_list("prohibited_patterns", self.prohibited_patterns)
        if self.max_value_chars < 0:
            raise ValueError("max_value_chars must be >= 0")


@dataclass(frozen=True, kw_only=True)
class RepairCLICommandSpec:
    command_spec_id: str
    command_kind: RepairCLICommandKind | str
    command_name: str
    description: str
    argument_specs: list[RepairCLIArgumentSpec] = field(default_factory=list)
    allowed_output_formats: list[RepairCLIOutputFormat | str] = field(default_factory=list)
    allowed_decisions: list[RepairCLIDecisionKind | str] = field(default_factory=list)
    risk_kinds: list[RepairCLIRiskKind | str] = field(default_factory=list)
    dispatch_target: str | None = None
    enabled: bool = True
    preview_only: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        _require_non_blank("command_name", self.command_name)
        _require_non_blank("description", self.description)
        _validate_list("argument_specs", self.argument_specs)
        _validate_list("allowed_output_formats", self.allowed_output_formats)
        _validate_list("allowed_decisions", self.allowed_decisions)
        _validate_list("risk_kinds", self.risk_kinds)
        if self.command_name in SAFE_REPAIR_CLI_COMMAND_NAMES and not self.preview_only:
            raise ValueError("safe CLI command specs must be preview_only")


@dataclass(frozen=True, kw_only=True)
class RepairCLISurfacePolicy:
    cli_policy_id: str
    version: str
    allowed_command_kinds: list[RepairCLICommandKind | str]
    blocked_command_kinds: list[RepairCLICommandKind | str]
    allowed_output_formats: list[RepairCLIOutputFormat | str]
    prohibited_arg_patterns: list[str] = field(default_factory=list)
    max_arg_chars: int = 200
    max_output_chars: int = 4000
    allow_help: bool = True
    allow_status: bool = True
    allow_boundary_preview: bool = True
    allow_evidence_preview: bool = True
    allow_source_context_preview: bool = True
    allow_scope_preview: bool = True
    allow_patch_metadata_preview: bool = True
    allow_safety_preview: bool = True
    allow_review_packet_preview: bool = True
    allow_loop_packet_preview: bool = True
    allow_bundle_preview: bool = True
    allow_do_nothing_preview: bool = True
    allow_handoff_preview: bool = True
    allow_file_export: bool = False
    allow_external_send: bool = False
    allow_ui_runtime: bool = False
    allow_shell: bool = False
    allow_subprocess: bool = False
    allow_arbitrary_command_execution: bool = False
    allow_dependency_install: bool = False
    allow_network_access: bool = False
    allow_source_file_read: bool = False
    allow_sandbox_source_read: bool = False
    allow_source_file_write: bool = False
    allow_patch_file_write: bool = False
    allow_file_edit: bool = False
    allow_patch_application: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_repair_execution: bool = False
    allow_test_execution: bool = False
    allow_new_patch_generation: bool = False
    allow_approval_capture: bool = False
    allow_approval_grant: bool = False
    allow_apply_permission: bool = False
    allow_model_provider_invocation: bool = False
    allow_external_agent_execution: bool = False
    allow_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_policy_id", self.cli_policy_id)
        _validate_version(self.version)
        _validate_list("allowed_command_kinds", self.allowed_command_kinds)
        _validate_list("blocked_command_kinds", self.blocked_command_kinds)
        _validate_list("allowed_output_formats", self.allowed_output_formats)
        _validate_string_list("prohibited_arg_patterns", self.prohibited_arg_patterns)
        if self.max_arg_chars < 0 or self.max_output_chars < 0:
            raise ValueError("CLI bounds must be >= 0")
        _validate_false(self, UNSAFE_REPAIR_CLI_POLICY_ALLOW_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairCLISurface:
    cli_surface_id: str
    version: str
    release_name: str
    command_specs: list[RepairCLICommandSpec]
    policy: RepairCLISurfacePolicy
    flags: RepairCLIFlagSet
    status: RepairCLIStatus | str
    readiness_level: RepairCLIReadinessLevel | str
    summary: str
    ready_for_cli_repair_proposal_surface: bool = True
    ready_for_future_v0389_consolidation_input: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_surface_id", self.cli_surface_id)
        _validate_version(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("summary", self.summary)
        _validate_list("command_specs", self.command_specs)
        if self.ready_for_execution:
            raise ValueError("ready_for_execution must remain False")


@dataclass(frozen=True, kw_only=True)
class RepairCLIInvocation:
    cli_invocation_id: str
    version: str
    argv: list[str]
    command_kind: RepairCLICommandKind | str
    parsed_args: dict[str, Any]
    requested_output_format: RepairCLIOutputFormat | str
    source_refs: list[RepairCLISourceRef] = field(default_factory=list)
    invocation_summary: str = "CLI argv parsed into bounded metadata only."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_invocation_id", self.cli_invocation_id)
        _validate_version(self.version)
        _validate_string_list("argv", self.argv)
        _validate_dict("parsed_args", self.parsed_args)
        _validate_list("source_refs", self.source_refs)
        _require_non_blank("invocation_summary", self.invocation_summary)


@dataclass(frozen=True, kw_only=True)
class RepairCLIInvocationDecision:
    cli_decision_id: str
    cli_invocation_id: str
    decision_kind: RepairCLIDecisionKind | str
    disposition: RepairCLICommandDisposition | str
    decision_summary: str
    risk_kinds: list[RepairCLIRiskKind | str] = field(default_factory=list)
    allowed_command_kind: RepairCLICommandKind | str | None = None
    preview_allowed: bool = False
    file_export_allowed: bool = False
    external_send_allowed: bool = False
    ui_runtime_allowed: bool = False
    shell_allowed: bool = False
    subprocess_allowed: bool = False
    command_execution_allowed: bool = False
    source_read_allowed: bool = False
    source_write_allowed: bool = False
    new_patch_generation_allowed: bool = False
    patch_application_allowed: bool = False
    apply_patch_allowed: bool = False
    git_apply_allowed: bool = False
    repair_execution_allowed: bool = False
    test_execution_allowed: bool = False
    approval_capture_allowed: bool = False
    approval_grant_allowed: bool = False
    apply_permission_allowed: bool = False
    model_provider_invocation_allowed: bool = False
    external_agent_allowed: bool = False
    dominion_runtime_allowed: bool = False
    production_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_decision_id", self.cli_decision_id)
        _require_non_blank("cli_invocation_id", self.cli_invocation_id)
        _require_non_blank("decision_summary", self.decision_summary)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_REPAIR_CLI_DECISION_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairCLIDeniedCommand:
    denied_command_id: str
    cli_invocation_id: str | None
    command_kind: RepairCLICommandKind | str
    risk_kinds: list[RepairCLIRiskKind | str]
    reason: str
    safe_alternatives: list[str] = field(default_factory=lambda: ["repair-proposal-help", "repair-proposal-status"])
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_command_id", self.denied_command_id)
        _require_non_blank("reason", self.reason)
        _validate_list("risk_kinds", self.risk_kinds)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True, kw_only=True)
class RepairCLICommandResult:
    cli_command_result_id: str
    cli_invocation_id: str
    cli_decision_id: str
    command_kind: RepairCLICommandKind | str
    status: RepairCLIStatus | str
    structured_result: dict[str, Any]
    rendered_preview: str
    output_format: RepairCLIOutputFormat | str
    redacted: bool = True
    truncated: bool = False
    preview_only: bool = True
    file_export_performed: bool = False
    external_send_performed: bool = False
    ui_runtime_invoked: bool = False
    shell_used: bool = False
    subprocess_used: bool = False
    command_executed: bool = False
    source_read_performed_by_v0388: bool = False
    new_patch_metadata_generated_by_v0388: bool = False
    file_write_performed: bool = False
    patch_file_written: bool = False
    file_edit_performed: bool = False
    patch_applied: bool = False
    apply_patch_called: bool = False
    git_apply_called: bool = False
    tests_run: bool = False
    repair_executed: bool = False
    approval_captured: bool = False
    approval_granted: bool = False
    apply_permission_granted: bool = False
    model_invocation_performed: bool = False
    external_agent_invoked: bool = False
    dominion_runtime_invoked: bool = False
    production_certified: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_command_result_id", self.cli_command_result_id)
        _require_non_blank("cli_invocation_id", self.cli_invocation_id)
        _require_non_blank("cli_decision_id", self.cli_decision_id)
        _validate_dict("structured_result", self.structured_result)
        _require_non_blank("rendered_preview", self.rendered_preview)
        if not self.preview_only:
            raise ValueError("CLI command result must remain preview_only")
        _validate_false(self, UNSAFE_REPAIR_CLI_RESULT_NAMES)


@dataclass(frozen=True, kw_only=True)
class RepairCLIOutput:
    cli_output_id: str
    version: str
    cli_invocation_id: str
    command_result: RepairCLICommandResult | None
    denied_command: RepairCLIDeniedCommand | None
    rendered_output: str
    output_format: RepairCLIOutputFormat | str
    status: RepairCLIStatus | str
    output_summary: str
    bounded: bool = True
    redacted: bool = True
    truncated: bool = False
    written_to_file: bool = False
    sent_externally: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_output_id", self.cli_output_id)
        _validate_version(self.version)
        _require_non_blank("cli_invocation_id", self.cli_invocation_id)
        _require_non_blank("rendered_output", self.rendered_output)
        _require_non_blank("output_summary", self.output_summary)
        if not self.bounded:
            raise ValueError("bounded must be True")
        _validate_false(self, ("written_to_file", "sent_externally", "ready_for_execution"))


@dataclass(frozen=True, kw_only=True)
class RepairCLIReport:
    cli_report_id: str
    version: str
    report_summary: str
    output: RepairCLIOutput | None = None
    ready_for_future_v0389_consolidation_input: bool = True
    ready_for_future_v039_apply_handoff_metadata: bool = True
    ready_for_execution: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_report_id", self.cli_report_id)
        _validate_version(self.version)
        _require_non_blank("report_summary", self.report_summary)
        _validate_false(self, ("ready_for_execution", "production_certified"))


@dataclass(frozen=True, kw_only=True)
class RepairCLIRunPreview:
    cli_run_preview_id: str
    version: str
    preview_summary: str
    would_execute_shell: bool = False
    would_use_subprocess: bool = False
    would_export_file: bool = False
    would_apply_patch: bool = False
    would_run_tests: bool = False
    would_invoke_external_systems: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_run_preview_id", self.cli_run_preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_false(
            self,
            (
                "would_execute_shell",
                "would_use_subprocess",
                "would_export_file",
                "would_apply_patch",
                "would_run_tests",
                "would_invoke_external_systems",
            ),
        )


@dataclass(frozen=True, kw_only=True)
class RepairCLINoRuntimeGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_shell: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_file_export: bool = True
    no_external_send: bool = True
    no_ui: bool = True
    no_source_read: bool = True
    no_new_patch_generation: bool = True
    no_apply: bool = True
    no_approval: bool = True
    no_repair: bool = True
    no_test: bool = True
    no_model: bool = True
    no_external_agent: bool = True
    no_dominion: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_true(
            self,
            (
                "no_shell",
                "no_subprocess",
                "no_command_execution",
                "no_file_export",
                "no_external_send",
                "no_ui",
                "no_source_read",
                "no_new_patch_generation",
                "no_apply",
                "no_approval",
                "no_repair",
                "no_test",
                "no_model",
                "no_external_agent",
                "no_dominion",
            ),
        )


@dataclass(frozen=True, kw_only=True)
class V0388ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    flags: RepairCLIFlagSet
    no_runtime_guarantee: RepairCLINoRuntimeGuarantee
    readiness_summary: str
    ready_for_v0389_bounded_repair_proposal_loop_consolidation: bool = True
    ready_for_v039_human_approved_sandbox_repair_apply: bool = True
    ready_for_cli_repair_proposal_surface: bool = True
    ready_for_execution: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("readiness_report_id", self.readiness_report_id)
        _validate_version(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("readiness_summary", self.readiness_summary)
        _validate_false(self, ("ready_for_execution", "production_certified"))


def build_repair_cli_flags(**kwargs: Any) -> RepairCLIFlagSet:
    defaults = {
        "flag_set_id": "v0388-cli-flags",
        "version": V0388_VERSION,
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
            "bounded_repair_proposal_cli_surface_only": True,
            "no_shell_execution": True,
            "no_arbitrary_command_execution": True,
            "no_independent_autonomous_agent_runtime": True,
            "mandatory_human_handoff_before_any_apply": True,
        },
    }
    defaults.update(kwargs)
    return RepairCLIFlagSet(**defaults)


def build_repair_cli_source_ref(**kwargs: Any) -> RepairCLISourceRef:
    defaults = {
        "source_ref_id": "v0388-cli-source-ref",
        "source_kind": RepairCLISourceKind.TEST_FIXTURE,
        "source_id": "fixture-source",
        "source_summary": "Existing metadata source reference for in-memory CLI preview.",
        "evidence_refs": [],
    }
    defaults.update(kwargs)
    return RepairCLISourceRef(**defaults)


def build_repair_cli_argument_spec(**kwargs: Any) -> RepairCLIArgumentSpec:
    defaults = {"argument_spec_id": "v0388-cli-arg", "name": "format", "description": "Bounded output format selector."}
    defaults.update(kwargs)
    return RepairCLIArgumentSpec(**defaults)


def build_repair_cli_command_spec(**kwargs: Any) -> RepairCLICommandSpec:
    defaults = {
        "command_spec_id": "v0388-cli-command-spec",
        "command_kind": RepairCLICommandKind.REPAIR_PROPOSAL_HELP,
        "command_name": "repair-proposal-help",
        "description": "Render repair proposal CLI help in memory.",
        "argument_specs": [build_repair_cli_argument_spec()],
        "allowed_output_formats": [RepairCLIOutputFormat.TEXT, RepairCLIOutputFormat.MARKDOWN, RepairCLIOutputFormat.JSON],
        "allowed_decisions": [RepairCLIDecisionKind.ALLOW_HELP],
        "risk_kinds": [],
        "dispatch_target": "render_repair_cli_help",
        "preview_only": True,
    }
    defaults.update(kwargs)
    return RepairCLICommandSpec(**defaults)


def build_repair_cli_surface_policy(**kwargs: Any) -> RepairCLISurfacePolicy:
    defaults = {
        "cli_policy_id": "v0388-cli-policy",
        "version": V0388_VERSION,
        "allowed_command_kinds": list(SAFE_COMMAND_KIND_BY_NAME.values()),
        "blocked_command_kinds": [metadata[0] for metadata in DENIED_COMMAND_METADATA.values()],
        "allowed_output_formats": [
            RepairCLIOutputFormat.TEXT,
            RepairCLIOutputFormat.MARKDOWN,
            RepairCLIOutputFormat.JSON,
            RepairCLIOutputFormat.STRUCTURED_ARTIFACT,
            RepairCLIOutputFormat.COMPACT,
        ],
        "prohibited_arg_patterns": list(DENIED_REPAIR_CLI_COMMAND_NAMES),
        "metadata": {"policy_is_preview_only": True},
    }
    defaults.update(kwargs)
    return RepairCLISurfacePolicy(**defaults)


def build_repair_cli_surface(**kwargs: Any) -> RepairCLISurface:
    defaults = {
        "cli_surface_id": "v0388-cli-surface",
        "version": V0388_VERSION,
        "release_name": V0388_RELEASE_NAME,
        "command_specs": default_repair_cli_command_specs(),
        "policy": default_repair_cli_surface_policy(),
        "flags": build_repair_cli_flags(),
        "status": RepairCLIStatus.INITIALIZED,
        "readiness_level": RepairCLIReadinessLevel.PREVIEW_SURFACE_READY,
        "summary": "Bounded CLI repair proposal surface for in-memory metadata previews only.",
    }
    defaults.update(kwargs)
    return RepairCLISurface(**defaults)


def build_repair_cli_invocation(**kwargs: Any) -> RepairCLIInvocation:
    defaults = {
        "cli_invocation_id": "v0388-cli-invocation",
        "version": V0388_VERSION,
        "argv": ["repair-proposal-help"],
        "command_kind": RepairCLICommandKind.REPAIR_PROPOSAL_HELP,
        "parsed_args": {"command": "repair-proposal-help", "args": []},
        "requested_output_format": RepairCLIOutputFormat.TEXT,
    }
    defaults.update(kwargs)
    return RepairCLIInvocation(**defaults)


def build_repair_cli_invocation_decision(**kwargs: Any) -> RepairCLIInvocationDecision:
    defaults = {
        "cli_decision_id": "v0388-cli-decision",
        "cli_invocation_id": "v0388-cli-invocation",
        "decision_kind": RepairCLIDecisionKind.ALLOW_HELP,
        "disposition": RepairCLICommandDisposition.ALLOWED_PREVIEW,
        "decision_summary": "Allowed in-memory CLI preview only.",
        "allowed_command_kind": RepairCLICommandKind.REPAIR_PROPOSAL_HELP,
        "preview_allowed": True,
    }
    defaults.update(kwargs)
    return RepairCLIInvocationDecision(**defaults)


def build_repair_cli_denied_command(**kwargs: Any) -> RepairCLIDeniedCommand:
    defaults = {
        "denied_command_id": "v0388-denied-command",
        "cli_invocation_id": None,
        "command_kind": RepairCLICommandKind.UNKNOWN,
        "risk_kinds": [RepairCLIRiskKind.UNKNOWN],
        "reason": "Command denied by bounded repair CLI policy.",
    }
    defaults.update(kwargs)
    return RepairCLIDeniedCommand(**defaults)


def build_repair_cli_command_result(**kwargs: Any) -> RepairCLICommandResult:
    defaults = {
        "cli_command_result_id": "v0388-cli-command-result",
        "cli_invocation_id": "v0388-cli-invocation",
        "cli_decision_id": "v0388-cli-decision",
        "command_kind": RepairCLICommandKind.REPAIR_PROPOSAL_HELP,
        "status": RepairCLIStatus.COMPLETED,
        "structured_result": {"preview_only": True},
        "rendered_preview": "Repair proposal CLI preview.",
        "output_format": RepairCLIOutputFormat.TEXT,
    }
    defaults.update(kwargs)
    return RepairCLICommandResult(**defaults)


def build_repair_cli_output(**kwargs: Any) -> RepairCLIOutput:
    defaults = {
        "cli_output_id": "v0388-cli-output",
        "version": V0388_VERSION,
        "cli_invocation_id": "v0388-cli-invocation",
        "command_result": None,
        "denied_command": None,
        "rendered_output": "Repair CLI output preview.",
        "output_format": RepairCLIOutputFormat.TEXT,
        "status": RepairCLIStatus.COMPLETED,
        "output_summary": "In-memory bounded CLI output.",
    }
    defaults.update(kwargs)
    return RepairCLIOutput(**defaults)


def build_repair_cli_report(**kwargs: Any) -> RepairCLIReport:
    defaults = {
        "cli_report_id": "v0388-cli-report",
        "version": V0388_VERSION,
        "report_summary": "CLI repair proposal surface report metadata; no execution readiness.",
    }
    defaults.update(kwargs)
    return RepairCLIReport(**defaults)


def build_repair_cli_run_preview(**kwargs: Any) -> RepairCLIRunPreview:
    defaults = {
        "cli_run_preview_id": "v0388-cli-run-preview",
        "version": V0388_VERSION,
        "preview_summary": "CLI parser/render preview only; no shell or subprocess use.",
    }
    defaults.update(kwargs)
    return RepairCLIRunPreview(**defaults)


def build_repair_cli_no_runtime_guarantee(**kwargs: Any) -> RepairCLINoRuntimeGuarantee:
    defaults = {
        "guarantee_id": "v0388-cli-no-runtime-guarantee",
        "version": V0388_VERSION,
        "guarantee_summary": "No shell, subprocess, command execution, export, send, source read, apply, repair, test, model, external agent, or Dominion runtime.",
    }
    defaults.update(kwargs)
    return RepairCLINoRuntimeGuarantee(**defaults)


def build_v0388_readiness_report(**kwargs: Any) -> V0388ReadinessReport:
    defaults = {
        "readiness_report_id": "v0388-readiness-report",
        "version": V0388_VERSION,
        "release_name": V0388_RELEASE_NAME,
        "flags": build_repair_cli_flags(),
        "no_runtime_guarantee": build_repair_cli_no_runtime_guarantee(),
        "readiness_summary": "v0.38.8 CLI repair proposal surface is ready for v0.38.9 handoff metadata only.",
    }
    defaults.update(kwargs)
    return V0388ReadinessReport(**defaults)


def default_repair_cli_command_specs() -> list[RepairCLICommandSpec]:
    specs: list[RepairCLICommandSpec] = []
    for command_name, command_kind in SAFE_COMMAND_KIND_BY_NAME.items():
        decision = ALLOW_DECISION_BY_COMMAND_KIND[command_kind]
        specs.append(
            build_repair_cli_command_spec(
                command_spec_id=f"v0388-spec-{command_name}",
                command_kind=command_kind,
                command_name=command_name,
                description=f"Preview {command_name} metadata in memory.",
                allowed_decisions=[decision],
                dispatch_target=f"render:{command_kind.value}",
                preview_only=True,
            )
        )
    for command_name, metadata in DENIED_COMMAND_METADATA.items():
        command_kind, decision_kind, risk_kind = metadata
        specs.append(
            build_repair_cli_command_spec(
                command_spec_id=f"v0388-denied-spec-{command_name.replace(' ', '-')}",
                command_kind=command_kind,
                command_name=command_name,
                description=f"Deny unsafe repair CLI command: {command_name}.",
                allowed_decisions=[decision_kind],
                risk_kinds=[risk_kind],
                dispatch_target="deny:static-policy",
                preview_only=False,
            )
        )
    return specs


def default_repair_cli_surface_policy() -> RepairCLISurfacePolicy:
    return build_repair_cli_surface_policy()


def build_default_repair_cli_surface() -> RepairCLISurface:
    return build_repair_cli_surface()


def parse_repair_cli_invocation(argv: list[str], surface: RepairCLISurface | None = None) -> RepairCLIInvocation:
    _validate_string_list("argv", argv)
    policy = surface.policy if surface else default_repair_cli_surface_policy()
    bounded_argv = [arg[: policy.max_arg_chars] for arg in argv]
    command_name = _normalize_command_name(bounded_argv)
    command_kind = SAFE_COMMAND_KIND_BY_NAME.get(command_name)
    if command_kind is None:
        command_kind = DENIED_COMMAND_METADATA.get(command_name, DENIED_COMMAND_METADATA["unknown"])[0]
    output_format = RepairCLIOutputFormat.TEXT
    for index, arg in enumerate(bounded_argv):
        if arg.startswith("--format="):
            value = arg.split("=", 1)[1].replace("-", "_")
            output_format = RepairCLIOutputFormat(value) if value in {item.value for item in RepairCLIOutputFormat} else RepairCLIOutputFormat.UNKNOWN
        elif arg == "--format" and index + 1 < len(bounded_argv):
            value = bounded_argv[index + 1].replace("-", "_")
            output_format = RepairCLIOutputFormat(value) if value in {item.value for item in RepairCLIOutputFormat} else RepairCLIOutputFormat.UNKNOWN
    return build_repair_cli_invocation(
        cli_invocation_id="v0388-cli-invocation:" + command_name.replace(" ", "-"),
        argv=bounded_argv,
        command_kind=command_kind,
        parsed_args={"command": command_name, "args": bounded_argv[1:], "argv_recorded_as_metadata_only": True},
        requested_output_format=output_format,
        metadata={"argv_not_passed_to_shell_or_subprocess": True},
    )


def evaluate_repair_cli_invocation(
    invocation: RepairCLIInvocation,
    surface: RepairCLISurface,
    artifact_context: dict[str, Any] | None = None,
) -> RepairCLIInvocationDecision:
    command_kind = RepairCLICommandKind(str(invocation.command_kind))
    if command_kind in SAFE_COMMAND_KIND_BY_NAME.values():
        decision_kind = ALLOW_DECISION_BY_COMMAND_KIND[command_kind]
        return build_repair_cli_invocation_decision(
            cli_decision_id="v0388-cli-decision:" + command_kind.value,
            cli_invocation_id=invocation.cli_invocation_id,
            decision_kind=decision_kind,
            disposition=RepairCLICommandDisposition.ALLOWED_PREVIEW
            if command_kind != RepairCLICommandKind.REPAIR_NO_OP
            else RepairCLICommandDisposition.NO_OP,
            decision_summary="Safe command allowed for bounded in-memory preview only.",
            allowed_command_kind=command_kind,
            preview_allowed=command_kind != RepairCLICommandKind.REPAIR_NO_OP,
            metadata={"artifact_context_supplied": bool(artifact_context)},
        )
    command_name = invocation.parsed_args.get("command", "unknown")
    denied = DENIED_COMMAND_METADATA.get(str(command_name), DENIED_COMMAND_METADATA["unknown"])
    return build_repair_cli_invocation_decision(
        cli_decision_id="v0388-cli-decision-denied:" + str(command_name).replace(" ", "-"),
        cli_invocation_id=invocation.cli_invocation_id,
        decision_kind=denied[1],
        disposition=RepairCLICommandDisposition.DENIED,
        decision_summary="Unsafe or unknown command denied by repair CLI surface policy.",
        risk_kinds=[denied[2]],
        allowed_command_kind=None,
        preview_allowed=False,
    )


def run_repair_cli_command(
    invocation: RepairCLIInvocation,
    surface: RepairCLISurface,
    artifact_context: dict[str, Any] | None = None,
) -> RepairCLIOutput:
    decision = evaluate_repair_cli_invocation(invocation, surface, artifact_context)
    output_format = RepairCLIOutputFormat(str(invocation.requested_output_format))
    if decision.disposition == RepairCLICommandDisposition.DENIED:
        denied = build_repair_cli_denied_command(
            denied_command_id="v0388-denied:" + invocation.cli_invocation_id,
            cli_invocation_id=invocation.cli_invocation_id,
            command_kind=invocation.command_kind,
            risk_kinds=decision.risk_kinds,
            reason=decision.decision_summary,
        )
        rendered = f"DENIED: {denied.reason}. Safe alternatives: {', '.join(denied.safe_alternatives)}"
        return build_repair_cli_output(
            cli_output_id="v0388-cli-output-denied:" + invocation.cli_invocation_id,
            cli_invocation_id=invocation.cli_invocation_id,
            command_result=None,
            denied_command=denied,
            rendered_output=rendered,
            output_format=output_format,
            status=RepairCLIStatus.DENIED,
            output_summary="Unsafe command denied; no remediation executed.",
        )
    rendered = (
        render_repair_cli_help(surface, output_format)
        if decision.decision_kind == RepairCLIDecisionKind.ALLOW_HELP
        else render_repair_cli_status(surface, output_format)
        if decision.decision_kind == RepairCLIDecisionKind.ALLOW_STATUS
        else render_repair_cli_preview(RepairCLICommandKind(str(invocation.command_kind)), artifact_context or {}, output_format)
    )
    structured = {
        "command_kind": str(invocation.command_kind),
        "preview_only": True,
        "artifact_context_keys": sorted((artifact_context or {}).keys()),
        "future_v0389_consolidation_input": True,
        "future_v039_handoff_metadata": True,
    }
    result = build_repair_cli_command_result(
        cli_command_result_id="v0388-cli-result:" + invocation.cli_invocation_id,
        cli_invocation_id=invocation.cli_invocation_id,
        cli_decision_id=decision.cli_decision_id,
        command_kind=invocation.command_kind,
        status=RepairCLIStatus.COMPLETED,
        structured_result=structured,
        rendered_preview=rendered,
        output_format=output_format,
    )
    return build_repair_cli_output(
        cli_output_id="v0388-cli-output:" + invocation.cli_invocation_id,
        cli_invocation_id=invocation.cli_invocation_id,
        command_result=result,
        denied_command=None,
        rendered_output=rendered,
        output_format=output_format,
        status=RepairCLIStatus.COMPLETED,
        output_summary="Safe command rendered as bounded in-memory preview.",
    )


def render_repair_cli_preview(
    command_kind: RepairCLICommandKind | str,
    artifact_context: dict[str, Any] | None,
    output_format: RepairCLIOutputFormat | str,
) -> str:
    context = artifact_context or {}
    key_map = {
        RepairCLICommandKind.REPAIR_BOUNDARY_PREVIEW: "boundary",
        RepairCLICommandKind.REPAIR_EVIDENCE_PREVIEW: "evidence",
        RepairCLICommandKind.REPAIR_SOURCE_CONTEXT_PREVIEW: "source_context",
        RepairCLICommandKind.REPAIR_SCOPE_PREVIEW: "scope",
        RepairCLICommandKind.REPAIR_PATCH_METADATA_PREVIEW: "patch_metadata",
        RepairCLICommandKind.REPAIR_SAFETY_PREVIEW: "safety",
        RepairCLICommandKind.REPAIR_REVIEW_PACKET_PREVIEW: "review_packet",
        RepairCLICommandKind.REPAIR_LOOP_PACKET_PREVIEW: "loop_packet",
        RepairCLICommandKind.REPAIR_DO_NOTHING_PREVIEW: "do_nothing",
    }
    kind = RepairCLICommandKind(str(command_kind))
    if kind == RepairCLICommandKind.REPAIR_PROPOSAL_BUNDLE_PREVIEW:
        return _bounded_text(create_repair_cli_bundle_preview(context, output_format))
    if kind == RepairCLICommandKind.REPAIR_HANDOFF_PREVIEW:
        return _bounded_text(create_repair_cli_handoff_preview(context, output_format))
    if kind == RepairCLICommandKind.REPAIR_NO_OP:
        return "No-op command acknowledged. Do-nothing remains available."
    selected_key = key_map.get(kind, "summary")
    preview_value = context.get(selected_key, f"{selected_key} metadata not supplied")
    return _bounded_text(f"{kind.value}: {preview_value}. Preview only; no file export, apply, test, repair, or execution.")


def render_repair_cli_status(surface: RepairCLISurface, output_format: RepairCLIOutputFormat | str) -> str:
    return _bounded_text(
        {
            "surface": surface.cli_surface_id,
            "status": str(surface.status),
            "ready_for_cli_repair_proposal_surface": surface.ready_for_cli_repair_proposal_surface,
            "ready_for_execution": surface.ready_for_execution,
            "safe_command_count": len([spec for spec in surface.command_specs if spec.command_name in SAFE_REPAIR_CLI_COMMAND_NAMES]),
        }
    )


def render_repair_cli_help(surface: RepairCLISurface, output_format: RepairCLIOutputFormat | str) -> str:
    safe_commands = [spec.command_name for spec in surface.command_specs if spec.command_name in SAFE_REPAIR_CLI_COMMAND_NAMES]
    return "Safe repair proposal preview commands: " + ", ".join(safe_commands)


def create_repair_cli_bundle_preview(
    artifact_context: dict[str, Any] | None,
    output_format: RepairCLIOutputFormat | str,
) -> dict[str, Any]:
    context = artifact_context or {}
    keys = (
        "boundary",
        "evidence",
        "source_context",
        "scope",
        "patch_metadata",
        "safety",
        "review_packet",
        "loop_packet",
        "do_nothing",
    )
    return {
        "preview_only": True,
        "in_memory_only": True,
        "present_artifacts": [key for key in keys if key in context],
        "missing_artifacts": [key for key in keys if key not in context],
        "output_format": str(output_format),
    }


def create_repair_cli_handoff_preview(
    artifact_context: dict[str, Any] | None,
    output_format: RepairCLIOutputFormat | str,
) -> dict[str, Any]:
    return {
        "preview_only": True,
        "future_v0389_consolidation_input": True,
        "future_v039_apply_handoff_metadata": True,
        "apply_permission": False,
        "human_handoff_required": True,
        "output_format": str(output_format),
    }


def repair_cli_flags_preserve_no_runtime(flags: RepairCLIFlagSet) -> bool:
    return all(not getattr(flags, name) for name in UNSAFE_REPAIR_CLI_FLAG_NAMES)


def repair_cli_policy_blocks_runtime(policy: RepairCLISurfacePolicy) -> bool:
    return all(not getattr(policy, name) for name in UNSAFE_REPAIR_CLI_POLICY_ALLOW_NAMES)


def repair_cli_invocation_is_not_shell(invocation: RepairCLIInvocation) -> bool:
    return bool(invocation.metadata.get("argv_not_passed_to_shell_or_subprocess", True))


def repair_cli_decision_is_preview_only(decision: RepairCLIInvocationDecision) -> bool:
    return all(not getattr(decision, name) for name in UNSAFE_REPAIR_CLI_DECISION_NAMES)


def repair_cli_command_result_is_not_runtime(result: RepairCLICommandResult) -> bool:
    return result.preview_only and all(not getattr(result, name) for name in UNSAFE_REPAIR_CLI_RESULT_NAMES)


def repair_cli_output_is_in_memory_only(output: RepairCLIOutput) -> bool:
    return output.bounded and not output.written_to_file and not output.sent_externally and not output.ready_for_execution


def v0388_readiness_report_is_not_execution_ready(report: V0388ReadinessReport) -> bool:
    return (
        not report.ready_for_execution
        and not report.production_certified
        and repair_cli_flags_preserve_no_runtime(report.flags)
    )
