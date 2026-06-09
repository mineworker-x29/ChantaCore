from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .agentic_operation_cycle import (
    build_agentic_operation_input,
    build_agentic_operation_stage_refs_from_v036_artifacts,
    run_bounded_agentic_operation_cycle,
)
from .boundary import _require_non_blank, _validate_string_list
from .patch_apply_candidate import build_apply_candidate_envelope, build_human_approval_contract, validate_human_approval_contract
from .patch_apply_dry_run import build_dry_run_apply_simulation_result
from .patch_apply_engine import (
    build_sandbox_materialization_plan,
    build_sandbox_patch_apply_input,
    run_sandbox_patch_apply,
)
from .patch_apply_sandbox import build_sandbox_workspace_manifest, build_sandbox_workspace_plan
from .patch_apply_trace import (
    build_patch_apply_sandbox_trace_packet,
    build_trace_packet_from_agentic_operation_run_packet,
)
from .patch_apply_validation import (
    build_sandbox_post_apply_validation_input,
    build_sandbox_post_apply_validation_report,
    run_sandbox_post_apply_validation,
)


V0368_VERSION = "v0.36.8"
V0368_RELEASE_NAME = "v0.36.8 CLI Sandbox Apply & Agentic Task Surface"
DEFAULT_MAX_CLI_ARG_CHARS = 240
DEFAULT_MAX_RENDERED_OUTPUT_CHARS = 1600

SAFE_COMMAND_NAMES = {
    "sandbox-apply-help",
    "--help",
    "-h",
    "sandbox-apply-status",
    "sandbox-apply-dry-run-preview",
    "sandbox-apply-candidate-preview",
    "sandbox-approval-validate",
    "sandbox-workspace-preview",
    "sandbox-apply-preview",
    "sandbox-apply-run",
    "sandbox-validate",
    "sandbox-reconcile",
    "agentic-task-preview",
    "agentic-task-run-once",
    "sandbox-trace-preview",
    "sandbox-bundle-preview",
    "no-op",
}

DENIED_COMMAND_ALIASES = {
    "patch-apply-live",
    "apply-live",
    "write-live",
    "edit-live",
    "workspace-write",
    "code-edit",
    "git-apply",
    "apply-patch",
    "test-run",
    "pytest",
    "npm-test",
    "install",
    "npm",
    "pip",
    "shell",
    "bash",
    "powershell",
    "cmd",
    "run-opencode",
    "run-hermes",
    "run-openclaw",
    "run-claude-code",
    "run-codex",
    "dominion",
    "external-agent-loop",
    "infinite-loop",
    "recursive-agent",
    "agent-chain",
    "harness-execute",
    "auto-repair",
    "repair-loop",
    "retry-loop",
    "multi-cycle",
}

DEFAULT_PROHIBITED_ARG_PATTERNS = [
    ";",
    "|",
    "&&",
    "||",
    "$(",
    "`",
    ">",
    "<",
    "patch-apply-live",
    "apply-live",
    "write-live",
    "edit-live",
    "workspace-write",
    "code-edit",
    "git" + " apply",
    "git-apply",
    "apply_patch",
    "apply-patch",
    "test-run",
    "pytest",
    "npm-test",
    "install",
    "npm",
    "pip",
    "credential",
    "secret",
    "token",
    ".env",
    "id_rsa",
    "pem",
    "external-agent",
    "run-claude-code",
    "run-codex",
    "run-opencode",
    "run-hermes",
    "run-openclaw",
    "dominion",
    "infinite-loop",
    "recursive-agent",
    "agent-chain",
    "harness-execute",
    "auto-repair",
    "repair-loop",
    "retry-loop",
    "multi-cycle",
]

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_test_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_reference_execution",
    "ready_for_reference_import",
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
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_recursive_self_invocation",
    "ready_for_automatic_retry",
    "ready_for_automatic_repair",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ocel_file_write",
    "ready_for_jsonl_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_DECISION_ALLOWED_NAMES = (
    "live_workspace_write_allowed",
    "patch_application_allowed",
    "workspace_write_allowed",
    "code_edit_allowed",
    "apply_patch_allowed",
    "git_apply_allowed",
    "shell_execution_allowed",
    "subprocess_allowed",
    "command_execution_allowed",
    "test_execution_allowed",
    "dependency_install_allowed",
    "reference_execution_allowed",
    "reference_import_allowed",
    "external_agent_execution_allowed",
    "claude_code_invocation_allowed",
    "codex_cli_invocation_allowed",
    "dominion_runtime_allowed",
    "infinite_agent_loop_allowed",
    "automatic_retry_allowed",
    "automatic_repair_allowed",
    "multi_cycle_loop_allowed",
    "provider_invocation_allowed",
    "network_access_allowed",
    "credential_access_allowed",
    "secret_read_allowed",
    "persistent_trace_write_allowed",
    "ui_runtime_allowed",
)


class CLISandboxApplyCommandKind(StrEnum):
    SANDBOX_APPLY_HELP = "sandbox_apply_help"
    SANDBOX_APPLY_STATUS = "sandbox_apply_status"
    SANDBOX_APPLY_DRY_RUN_PREVIEW = "sandbox_apply_dry_run_preview"
    SANDBOX_APPLY_CANDIDATE_PREVIEW = "sandbox_apply_candidate_preview"
    SANDBOX_APPROVAL_VALIDATE = "sandbox_approval_validate"
    SANDBOX_WORKSPACE_PREVIEW = "sandbox_workspace_preview"
    SANDBOX_APPLY_PREVIEW = "sandbox_apply_preview"
    SANDBOX_APPLY_RUN = "sandbox_apply_run"
    SANDBOX_VALIDATE = "sandbox_validate"
    SANDBOX_RECONCILE = "sandbox_reconcile"
    AGENTIC_TASK_PREVIEW = "agentic_task_preview"
    AGENTIC_TASK_RUN_ONCE = "agentic_task_run_once"
    SANDBOX_TRACE_PREVIEW = "sandbox_trace_preview"
    SANDBOX_BUNDLE_PREVIEW = "sandbox_bundle_preview"
    LIVE_APPLY_DENIED = "live_apply_denied"
    LIVE_WRITE_DENIED = "live_write_denied"
    LIVE_EDIT_DENIED = "live_edit_denied"
    APPLY_PATCH_DENIED = "apply_patch_denied"
    GIT_APPLY_DENIED = "git_apply_denied"
    TEST_EXECUTION_DENIED = "test_execution_denied"
    DEPENDENCY_INSTALL_DENIED = "dependency_install_denied"
    SHELL_COMMAND_DENIED = "shell_command_denied"
    REFERENCE_EXECUTION_DENIED = "reference_execution_denied"
    EXTERNAL_AGENT_DENIED = "external_agent_denied"
    DOMINION_DENIED = "dominion_denied"
    AUTO_REPAIR_DENIED = "auto_repair_denied"
    MULTI_CYCLE_DENIED = "multi_cycle_denied"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLISandboxApplyCommandMode(StrEnum):
    HELP = "help"
    STATUS = "status"
    DRY_RUN_PREVIEW = "dry_run_preview"
    CANDIDATE_PREVIEW = "candidate_preview"
    APPROVAL_VALIDATE = "approval_validate"
    WORKSPACE_PREVIEW = "workspace_preview"
    SANDBOX_APPLY_PREVIEW = "sandbox_apply_preview"
    SANDBOX_APPLY_RUN = "sandbox_apply_run"
    VALIDATION = "validation"
    RECONCILIATION = "reconciliation"
    AGENTIC_TASK_PREVIEW = "agentic_task_preview"
    AGENTIC_TASK_RUN_ONCE = "agentic_task_run_once"
    TRACE_PREVIEW = "trace_preview"
    BUNDLE_PREVIEW = "bundle_preview"
    DENIED = "denied"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLISandboxApplyInputSourceKind(StrEnum):
    ARGV_LIST = "argv_list"
    PARSED_ARGS = "parsed_args"
    RUNTIME_CONTEXT = "runtime_context"
    SANDBOX_ROOT_ARG = "sandbox_root_arg"
    TASK_ARG = "task_arg"
    APPLY_CANDIDATE_REF = "apply_candidate_ref"
    HUMAN_APPROVAL_CONTRACT_REF = "human_approval_contract_ref"
    DRY_RUN_RESULT_REF = "dry_run_result_ref"
    SANDBOX_MANIFEST_REF = "sandbox_manifest_ref"
    SANDBOX_APPLY_RESULT_REF = "sandbox_apply_result_ref"
    POST_APPLY_VALIDATION_REPORT_REF = "post_apply_validation_report_ref"
    AGENTIC_OPERATION_RUN_PACKET_REF = "agentic_operation_run_packet_ref"
    TRACE_PACKET_REF = "trace_packet_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class CLISandboxApplySurfaceStatus(StrEnum):
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


class CLISandboxApplyDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_DRY_RUN_PREVIEW = "allow_dry_run_preview"
    ALLOW_CANDIDATE_PREVIEW = "allow_candidate_preview"
    ALLOW_APPROVAL_VALIDATE = "allow_approval_validate"
    ALLOW_WORKSPACE_PREVIEW = "allow_workspace_preview"
    ALLOW_SANDBOX_APPLY_PREVIEW = "allow_sandbox_apply_preview"
    ALLOW_SANDBOX_APPLY_RUN = "allow_sandbox_apply_run"
    ALLOW_SANDBOX_VALIDATE = "allow_sandbox_validate"
    ALLOW_SANDBOX_RECONCILE = "allow_sandbox_reconcile"
    ALLOW_AGENTIC_TASK_PREVIEW = "allow_agentic_task_preview"
    ALLOW_AGENTIC_TASK_RUN_ONCE = "allow_agentic_task_run_once"
    ALLOW_TRACE_PREVIEW = "allow_trace_preview"
    ALLOW_BUNDLE_PREVIEW = "allow_bundle_preview"
    DENY_LIVE_APPLY = "deny_live_apply"
    DENY_LIVE_WRITE_EDIT = "deny_live_write_edit"
    DENY_APPLY_PATCH = "deny_apply_patch"
    DENY_GIT_APPLY = "deny_git_apply"
    DENY_TEST_EXECUTION = "deny_test_execution"
    DENY_DEPENDENCY_INSTALL = "deny_dependency_install"
    DENY_SHELL_COMMAND = "deny_shell_command"
    DENY_REFERENCE_EXECUTION = "deny_reference_execution"
    DENY_EXTERNAL_AGENT_EXECUTION = "deny_external_agent_execution"
    DENY_DOMINION_RUNTIME = "deny_dominion_runtime"
    DENY_AUTO_REPAIR = "deny_auto_repair"
    DENY_MULTI_CYCLE = "deny_multi_cycle"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class CLISandboxApplyOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    STRUCTURED_ARTIFACT = "structured_artifact"
    DEBUG_SUMMARY = "debug_summary"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class CLISandboxApplyRiskKind(StrEnum):
    SHELL_INJECTION_RISK = "shell_injection_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    LIVE_PATCH_APPLY_RISK = "live_patch_apply_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    LIVE_CODE_EDIT_RISK = "live_code_edit_risk"
    SANDBOX_ESCAPE_RISK = "sandbox_escape_risk"
    PATH_TRAVERSAL_RISK = "path_traversal_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    REFERENCE_IMPORT_RISK = "reference_import_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    CLAUDE_CODE_INVOCATION_RISK = "claude_code_invocation_risk"
    CODEX_CLI_INVOCATION_RISK = "codex_cli_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    DIRECT_PROVIDER_INVOCATION_RISK = "direct_provider_invocation_risk"
    DIRECT_NETWORK_ACCESS_RISK = "direct_network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_READ_RISK = "secret_read_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    UI_RUNTIME_RISK = "ui_runtime_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class CLISandboxApplyReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_CONTRACT_READY = "cli_contract_ready"
    BOUNDED_CLI_SANDBOX_APPLY_SURFACE_READY = "bounded_cli_sandbox_apply_surface_ready"
    BOUNDED_PREVIEW_COMMAND_DISPATCH_READY = "bounded_preview_command_dispatch_ready"
    BOUNDED_SANDBOX_RUN_DISPATCH_READY = "bounded_sandbox_run_dispatch_ready"
    BOUNDED_AGENTIC_TASK_RUN_ONCE_READY = "bounded_agentic_task_run_once_ready"
    DESIGN_HANDOFF_READY_FOR_V0369 = "design_handoff_ready_for_v0369"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0368_VERSION not in version:
        raise ValueError("version must include v0.36.8")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.8")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _sanitize_text(value: Any, max_chars: int = DEFAULT_MAX_RENDERED_OUTPUT_CHARS) -> tuple[str, bool, bool]:
    text = str(value)
    redacted = text
    for token in ("secret", "credential", "api_key", "token", "password", "id_rsa", "pem"):
        for variant in (token, token.upper(), token.capitalize()):
            redacted = redacted.replace(variant, "[redacted]")
    truncated = len(redacted) > max_chars
    return redacted[:max_chars], redacted != text, truncated


def _bounded_json(value: Any) -> tuple[str, bool, bool]:
    return _sanitize_text(json.dumps(value, sort_keys=True, default=str), DEFAULT_MAX_RENDERED_OUTPUT_CHARS)


def _contains_prohibited_text(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyFlagSet:
    flag_set_id: str
    version: str
    cli_sandbox_apply_surface_constructed: bool
    cli_argument_parsing_enabled: bool
    bounded_preview_command_dispatch_enabled: bool
    bounded_sandbox_apply_dispatch_enabled: bool
    bounded_agentic_task_dispatch_enabled: bool
    denied_unsafe_command_handling_enabled: bool
    ready_for_v0369_patch_apply_sandbox_consolidation: bool
    ready_for_cli_sandbox_apply_surface: bool
    ready_for_bounded_cli_sandbox_apply_preview: bool
    ready_for_cli_apply_candidate_preview: bool
    ready_for_cli_dry_run_preview: bool
    ready_for_cli_sandbox_workspace_preview: bool
    ready_for_cli_sandbox_apply_run: bool
    ready_for_cli_sandbox_post_apply_validation: bool
    ready_for_cli_agentic_task_run_once: bool
    ready_for_cli_trace_preview: bool
    ready_for_sandbox_file_write: bool
    ready_for_sandbox_patch_apply: bool
    ready_for_execution: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
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
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_recursive_self_invocation: bool = False
    ready_for_automatic_retry: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_jsonl_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplySourceRef:
    source_ref_id: str
    source_kind: CLISandboxApplyInputSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        CLISandboxApplyInputSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyArgumentSpec:
    argument_spec_id: str
    name: str
    required: bool
    allowed_values: list[str]
    prohibited_values: list[str]
    allow_text_value: bool
    allow_ref_value: bool
    allow_json_value: bool
    max_value_chars: int
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("argument_spec_id", "name", "description"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("allowed_values", self.allowed_values)
        _validate_string_list("prohibited_values", self.prohibited_values)
        if self.max_value_chars < 0:
            raise ValueError("max_value_chars must be >= 0")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyCommandSpec:
    command_spec_id: str
    command_kind: CLISandboxApplyCommandKind | str
    command_mode: CLISandboxApplyCommandMode | str
    command_name: str
    description: str
    argument_specs: list[CLISandboxApplyArgumentSpec]
    allowed_output_formats: list[CLISandboxApplyOutputFormat | str]
    allowed_decisions: list[CLISandboxApplyDecisionKind | str]
    risk_kinds: list[CLISandboxApplyRiskKind | str]
    enabled: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("command_spec_id", "command_name", "description"):
            _require_non_blank(name, getattr(self, name))
        CLISandboxApplyCommandKind(self.command_kind)
        CLISandboxApplyCommandMode(self.command_mode)
        _validate_list("argument_specs", self.argument_specs)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLISandboxApplyOutputFormat)
        _validate_enum_list("allowed_decisions", self.allowed_decisions, CLISandboxApplyDecisionKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLISandboxApplyRiskKind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplySurfacePolicy:
    policy_id: str
    version: str
    allowed_command_kinds: list[CLISandboxApplyCommandKind | str]
    blocked_command_kinds: list[CLISandboxApplyCommandKind | str]
    allowed_output_formats: list[CLISandboxApplyOutputFormat | str]
    prohibited_arg_patterns: list[str]
    max_arg_chars: int
    allow_candidate_preview: bool
    allow_approval_validate: bool
    allow_dry_run_preview: bool
    allow_workspace_preview: bool
    allow_sandbox_apply_preview: bool
    allow_sandbox_apply_run: bool
    allow_sandbox_post_apply_validation: bool
    allow_agentic_task_preview: bool
    allow_agentic_task_run_once: bool
    allow_trace_preview: bool
    allow_sandbox_file_write: bool
    allow_sandbox_patch_apply: bool
    allow_live_workspace_write: bool = False
    allow_patch_application: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_test_execution: bool = False
    allow_shell: bool = False
    allow_subprocess: bool = False
    allow_command_execution: bool = False
    allow_dependency_install: bool = False
    allow_reference_execution: bool = False
    allow_reference_import: bool = False
    allow_external_agent_execution: bool = False
    allow_claude_code_invocation: bool = False
    allow_codex_cli_invocation: bool = False
    allow_dominion_runtime: bool = False
    allow_infinite_agent_loop: bool = False
    allow_automatic_retry: bool = False
    allow_automatic_repair: bool = False
    allow_multi_cycle_loop: bool = False
    allow_provider_invocation: bool = False
    allow_network_access: bool = False
    allow_credential_access: bool = False
    allow_secret_read: bool = False
    allow_persistent_trace_write: bool = False
    allow_ui_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_command_kinds", self.allowed_command_kinds, CLISandboxApplyCommandKind)
        _validate_enum_list("blocked_command_kinds", self.blocked_command_kinds, CLISandboxApplyCommandKind)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLISandboxApplyOutputFormat)
        _validate_string_list("prohibited_arg_patterns", self.prohibited_arg_patterns)
        if self.max_arg_chars < 0:
            raise ValueError("max_arg_chars must be >= 0")
        required_patterns = (";", "live", "git", "apply_patch", "test", "install", "credential", "external-agent", "dominion", "infinite-loop", "auto-repair", "multi-cycle")
        lowered = " ".join(pattern.lower() for pattern in self.prohibited_arg_patterns)
        for pattern in required_patterns:
            if pattern not in lowered:
                raise ValueError("prohibited_arg_patterns missing required unsafe pattern")
        _validate_false(
            self,
            (
                "allow_live_workspace_write",
                "allow_patch_application",
                "allow_workspace_write",
                "allow_code_edit",
                "allow_apply_patch",
                "allow_git_apply",
                "allow_test_execution",
                "allow_shell",
                "allow_subprocess",
                "allow_command_execution",
                "allow_dependency_install",
                "allow_reference_execution",
                "allow_reference_import",
                "allow_external_agent_execution",
                "allow_claude_code_invocation",
                "allow_codex_cli_invocation",
                "allow_dominion_runtime",
                "allow_infinite_agent_loop",
                "allow_automatic_retry",
                "allow_automatic_repair",
                "allow_multi_cycle_loop",
                "allow_provider_invocation",
                "allow_network_access",
                "allow_credential_access",
                "allow_secret_read",
                "allow_persistent_trace_write",
                "allow_ui_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplySurface:
    cli_surface_id: str
    version: str
    command_specs: list[CLISandboxApplyCommandSpec]
    policy: CLISandboxApplySurfacePolicy
    flags: CLISandboxApplyFlagSet
    status: CLISandboxApplySurfaceStatus | str
    readiness_level: CLISandboxApplyReadinessLevel | str
    summary: str
    ready_for_cli_sandbox_apply_surface: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("cli_surface_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("command_specs", self.command_specs)
        CLISandboxApplySurfaceStatus(self.status)
        CLISandboxApplyReadinessLevel(self.readiness_level)
        if not cli_sandbox_apply_flags_preserve_unsafe_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyInvocation:
    invocation_id: str
    argv: list[str]
    command_kind: CLISandboxApplyCommandKind | str
    command_mode: CLISandboxApplyCommandMode | str
    parsed_args: dict[str, Any]
    requested_output_format: CLISandboxApplyOutputFormat | str
    source_refs: list[CLISandboxApplySourceRef]
    invocation_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_id", self.invocation_id)
        _require_non_blank("invocation_summary", self.invocation_summary)
        _validate_string_list("argv", self.argv)
        CLISandboxApplyCommandKind(self.command_kind)
        CLISandboxApplyCommandMode(self.command_mode)
        CLISandboxApplyOutputFormat(self.requested_output_format)
        _validate_dict("parsed_args", self.parsed_args)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyInvocationDecision:
    decision_id: str
    invocation_id: str
    decision_kind: CLISandboxApplyDecisionKind | str
    reason: str
    risk_kinds: list[CLISandboxApplyRiskKind | str]
    allowed_command_kind: CLISandboxApplyCommandKind | str | None
    bounded_preview_allowed: bool
    sandbox_apply_run_allowed: bool
    sandbox_file_write_allowed: bool
    sandbox_patch_apply_allowed: bool
    live_workspace_write_allowed: bool = False
    patch_application_allowed: bool = False
    workspace_write_allowed: bool = False
    code_edit_allowed: bool = False
    apply_patch_allowed: bool = False
    git_apply_allowed: bool = False
    shell_execution_allowed: bool = False
    subprocess_allowed: bool = False
    command_execution_allowed: bool = False
    test_execution_allowed: bool = False
    dependency_install_allowed: bool = False
    reference_execution_allowed: bool = False
    reference_import_allowed: bool = False
    external_agent_execution_allowed: bool = False
    claude_code_invocation_allowed: bool = False
    codex_cli_invocation_allowed: bool = False
    dominion_runtime_allowed: bool = False
    infinite_agent_loop_allowed: bool = False
    automatic_retry_allowed: bool = False
    automatic_repair_allowed: bool = False
    multi_cycle_loop_allowed: bool = False
    provider_invocation_allowed: bool = False
    network_access_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    persistent_trace_write_allowed: bool = False
    ui_runtime_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "invocation_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        CLISandboxApplyDecisionKind(self.decision_kind)
        if self.allowed_command_kind is not None:
            CLISandboxApplyCommandKind(self.allowed_command_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLISandboxApplyRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_ALLOWED_NAMES)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyDeniedCommand:
    denied_command_id: str
    invocation_id: str | None
    decision_id: str | None
    command_kind: CLISandboxApplyCommandKind | str
    risk_kinds: list[CLISandboxApplyRiskKind | str]
    reason: str
    safe_alternatives: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("denied_command_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        CLISandboxApplyCommandKind(self.command_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLISandboxApplyRiskKind)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyRuntimeContext:
    runtime_context_id: str
    has_apply_candidate: bool
    has_human_approval_contract: bool
    has_dry_run_result: bool
    has_sandbox_workspace_manifest: bool
    has_sandbox_apply_result: bool
    has_post_apply_validation_report: bool
    has_agentic_operation_run_packet: bool
    has_patch_apply_trace_packet: bool
    sandbox_root_ref: str | None
    context_summary: str
    allows_sandbox_apply_run: bool
    allows_sandbox_file_write: bool
    allows_sandbox_patch_apply: bool
    allows_live_workspace_write: bool = False
    allows_patch_application: bool = False
    allows_workspace_write: bool = False
    allows_code_edit: bool = False
    allows_shell: bool = False
    allows_test_execution: bool = False
    allows_external_agent_execution: bool = False
    allows_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("runtime_context_id", "context_summary"):
            _require_non_blank(name, getattr(self, name))
        if any((self.allows_sandbox_apply_run, self.allows_sandbox_file_write, self.allows_sandbox_patch_apply)) and not self.sandbox_root_ref:
            raise ValueError("sandbox apply context requires explicit sandbox_root_ref")
        _validate_false(
            self,
            (
                "allows_live_workspace_write",
                "allows_patch_application",
                "allows_workspace_write",
                "allows_code_edit",
                "allows_shell",
                "allows_test_execution",
                "allows_external_agent_execution",
                "allows_dominion_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyCommandResult:
    command_result_id: str
    invocation_id: str
    decision_id: str
    command_kind: CLISandboxApplyCommandKind | str
    status: CLISandboxApplySurfaceStatus | str
    apply_candidate_ref: str | None
    dry_run_result_ref: str | None
    sandbox_manifest_ref: str | None
    sandbox_apply_result_ref: str | None
    post_apply_validation_report_ref: str | None
    agentic_operation_run_packet_ref: str | None
    trace_packet_ref: str | None
    structured_result: dict[str, Any]
    text_summary: str
    redacted: bool
    truncated: bool
    sandbox_write_performed: bool
    live_write_performed: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("command_result_id", "invocation_id", "decision_id", "text_summary"):
            _require_non_blank(name, getattr(self, name))
        CLISandboxApplyCommandKind(self.command_kind)
        CLISandboxApplySurfaceStatus(self.status)
        _validate_dict("structured_result", self.structured_result)
        _validate_false(self, ("live_write_performed", "ready_for_execution"))
        if self.sandbox_write_performed and CLISandboxApplyCommandKind(self.command_kind) != CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN:
            raise ValueError("sandbox_write_performed may be true only for sandbox_apply_run")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyRunOutput:
    run_output_id: str
    invocation_id: str
    command_result: CLISandboxApplyCommandResult | None
    denied_command: CLISandboxApplyDeniedCommand | None
    rendered_output: str
    output_format: CLISandboxApplyOutputFormat | str
    status: CLISandboxApplySurfaceStatus | str
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_output_id", "invocation_id", "rendered_output", "summary"):
            _require_non_blank(name, getattr(self, name))
        CLISandboxApplyOutputFormat(self.output_format)
        CLISandboxApplySurfaceStatus(self.status)
        if _sanitize_text(self.rendered_output)[0] != self.rendered_output:
            raise ValueError("rendered_output must be bounded and redacted")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyRunReport:
    run_report_id: str
    version: str
    run_output_id: str
    invocation_id: str
    status: CLISandboxApplySurfaceStatus | str
    bounded_preview_count: int
    sandbox_apply_run_count: int
    denied_command_count: int
    blocked_command_count: int
    summary: str
    sandbox_write_performed: bool
    live_write_performed: bool = False
    patch_application_performed: bool = False
    shell_execution_performed: bool = False
    test_execution_performed: bool = False
    external_agent_execution_performed: bool = False
    dominion_runtime_performed: bool = False
    persistent_trace_write_performed: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_report_id", "run_output_id", "invocation_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        CLISandboxApplySurfaceStatus(self.status)
        for name in ("bounded_preview_count", "sandbox_apply_run_count", "denied_command_count", "blocked_command_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(
            self,
            (
                "live_write_performed",
                "patch_application_performed",
                "shell_execution_performed",
                "test_execution_performed",
                "external_agent_execution_performed",
                "dominion_runtime_performed",
                "persistent_trace_write_performed",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyRunPreview:
    run_preview_id: str
    cli_surface_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_preview_id", "cli_surface_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_string_list("planned_steps", self.planned_steps)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_string_list("explicitly_not_performed", self.explicitly_not_performed)
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplyNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_live_workspace_write: bool
    no_live_code_edit: bool
    no_unrestricted_patch_application: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_shell_execution: bool
    no_subprocess_execution: bool
    no_command_execution: bool
    no_test_execution: bool
    no_dependency_install: bool
    no_reference_execution: bool
    no_reference_import: bool
    no_external_agent_execution: bool
    no_claude_code_invocation: bool
    no_codex_cli_invocation: bool
    no_dominion_runtime: bool
    no_infinite_agent_loop: bool
    no_automatic_repair: bool
    no_multi_cycle_loop: bool
    no_provider_invocation: bool
    no_network_access: bool
    no_credential_access: bool
    no_secret_read: bool
    no_autonomous_runtime: bool
    no_general_tool_execution: bool
    no_persistent_trace_write: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    no_sandbox_write: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name, value in self.__dict__.items():
            if name.startswith("no_") and name != "no_sandbox_write" and value is not True:
                raise ValueError(f"{name} must be True in v0.36.8")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0368ReadinessReport:
    readiness_report_id: str
    version: str
    release_name: str
    status: CLISandboxApplySurfaceStatus | str
    readiness_level: CLISandboxApplyReadinessLevel | str
    ready_for_v0369_patch_apply_sandbox_consolidation: bool
    ready_for_cli_sandbox_apply_surface: bool
    ready_for_bounded_cli_sandbox_apply_preview: bool
    ready_for_cli_apply_candidate_preview: bool
    ready_for_cli_dry_run_preview: bool
    ready_for_cli_sandbox_workspace_preview: bool
    ready_for_cli_sandbox_apply_run: bool
    ready_for_cli_sandbox_post_apply_validation: bool
    ready_for_cli_agentic_task_run_once: bool
    ready_for_cli_trace_preview: bool
    ready_for_sandbox_file_write: bool
    ready_for_sandbox_patch_apply: bool
    ready_for_execution: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
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
    ready_for_multi_cycle_agentic_loop: bool = False
    ready_for_recursive_self_invocation: bool = False
    ready_for_automatic_retry: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_jsonl_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    summary: str = "v0.36.8 CLI sandbox apply surface is bounded and not execution-ready"
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        CLISandboxApplySurfaceStatus(self.status)
        CLISandboxApplyReadinessLevel(self.readiness_level)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_cli_sandbox_apply_flags(**kwargs: Any) -> CLISandboxApplyFlagSet:
    return CLISandboxApplyFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "cli_sandbox_apply_flags:v0.36.8"),
        version=kwargs.pop("version", V0368_VERSION),
        cli_sandbox_apply_surface_constructed=kwargs.pop("cli_sandbox_apply_surface_constructed", True),
        cli_argument_parsing_enabled=kwargs.pop("cli_argument_parsing_enabled", True),
        bounded_preview_command_dispatch_enabled=kwargs.pop("bounded_preview_command_dispatch_enabled", True),
        bounded_sandbox_apply_dispatch_enabled=kwargs.pop("bounded_sandbox_apply_dispatch_enabled", True),
        bounded_agentic_task_dispatch_enabled=kwargs.pop("bounded_agentic_task_dispatch_enabled", True),
        denied_unsafe_command_handling_enabled=kwargs.pop("denied_unsafe_command_handling_enabled", True),
        ready_for_v0369_patch_apply_sandbox_consolidation=kwargs.pop("ready_for_v0369_patch_apply_sandbox_consolidation", True),
        ready_for_cli_sandbox_apply_surface=kwargs.pop("ready_for_cli_sandbox_apply_surface", True),
        ready_for_bounded_cli_sandbox_apply_preview=kwargs.pop("ready_for_bounded_cli_sandbox_apply_preview", True),
        ready_for_cli_apply_candidate_preview=kwargs.pop("ready_for_cli_apply_candidate_preview", True),
        ready_for_cli_dry_run_preview=kwargs.pop("ready_for_cli_dry_run_preview", True),
        ready_for_cli_sandbox_workspace_preview=kwargs.pop("ready_for_cli_sandbox_workspace_preview", True),
        ready_for_cli_sandbox_apply_run=kwargs.pop("ready_for_cli_sandbox_apply_run", True),
        ready_for_cli_sandbox_post_apply_validation=kwargs.pop("ready_for_cli_sandbox_post_apply_validation", True),
        ready_for_cli_agentic_task_run_once=kwargs.pop("ready_for_cli_agentic_task_run_once", True),
        ready_for_cli_trace_preview=kwargs.pop("ready_for_cli_trace_preview", True),
        ready_for_sandbox_file_write=kwargs.pop("ready_for_sandbox_file_write", True),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        **kwargs,
    )


def build_cli_sandbox_apply_source_ref(**kwargs: Any) -> CLISandboxApplySourceRef:
    return CLISandboxApplySourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "cli_sandbox_apply_source_ref:v0.36.8"),
        source_kind=kwargs.pop("source_kind", CLISandboxApplyInputSourceKind.TEST_FIXTURE),
        source_id=kwargs.pop("source_id", "source:v0.36.8"),
        source_summary=kwargs.pop("source_summary", "CLI sandbox apply source metadata; not shell/provider/live write"),
        evidence_refs=kwargs.pop("evidence_refs", []),
        **kwargs,
    )


def build_cli_sandbox_apply_argument_spec(**kwargs: Any) -> CLISandboxApplyArgumentSpec:
    return CLISandboxApplyArgumentSpec(
        argument_spec_id=kwargs.pop("argument_spec_id", "cli_sandbox_apply_argument_spec:v0.36.8"),
        name=kwargs.pop("name", "--sandbox-root"),
        required=kwargs.pop("required", False),
        allowed_values=kwargs.pop("allowed_values", []),
        prohibited_values=kwargs.pop("prohibited_values", DEFAULT_PROHIBITED_ARG_PATTERNS),
        allow_text_value=kwargs.pop("allow_text_value", True),
        allow_ref_value=kwargs.pop("allow_ref_value", True),
        allow_json_value=kwargs.pop("allow_json_value", False),
        max_value_chars=kwargs.pop("max_value_chars", DEFAULT_MAX_CLI_ARG_CHARS),
        description=kwargs.pop("description", "bounded CLI argument metadata; not execution"),
        **kwargs,
    )


def _decision_for_allowed_kind(kind: CLISandboxApplyCommandKind) -> CLISandboxApplyDecisionKind:
    mapping = {
        CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP: CLISandboxApplyDecisionKind.ALLOW_HELP,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS: CLISandboxApplyDecisionKind.ALLOW_STATUS,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_DRY_RUN_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_CANDIDATE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE: CLISandboxApplyDecisionKind.ALLOW_APPROVAL_VALIDATE,
        CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_WORKSPACE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_SANDBOX_APPLY_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN: CLISandboxApplyDecisionKind.ALLOW_SANDBOX_APPLY_RUN,
        CLISandboxApplyCommandKind.SANDBOX_VALIDATE: CLISandboxApplyDecisionKind.ALLOW_SANDBOX_VALIDATE,
        CLISandboxApplyCommandKind.SANDBOX_RECONCILE: CLISandboxApplyDecisionKind.ALLOW_SANDBOX_RECONCILE,
        CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_AGENTIC_TASK_PREVIEW,
        CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE: CLISandboxApplyDecisionKind.ALLOW_AGENTIC_TASK_RUN_ONCE,
        CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_TRACE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW: CLISandboxApplyDecisionKind.ALLOW_BUNDLE_PREVIEW,
        CLISandboxApplyCommandKind.NO_OP: CLISandboxApplyDecisionKind.NO_OP,
    }
    return mapping.get(kind, CLISandboxApplyDecisionKind.BLOCK)


def build_cli_sandbox_apply_command_spec(**kwargs: Any) -> CLISandboxApplyCommandSpec:
    kind = CLISandboxApplyCommandKind(kwargs.pop("command_kind", CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP))
    return CLISandboxApplyCommandSpec(
        command_spec_id=kwargs.pop("command_spec_id", f"cli_sandbox_apply_command_spec:v0.36.8:{kind.value}"),
        command_kind=kind,
        command_mode=kwargs.pop("command_mode", _mode_from_kind(kind)),
        command_name=kwargs.pop("command_name", kind.value.replace("_", "-")),
        description=kwargs.pop("description", "bounded CLI sandbox apply command spec; not OS command"),
        argument_specs=kwargs.pop("argument_specs", [build_cli_sandbox_apply_argument_spec()]),
        allowed_output_formats=kwargs.pop(
            "allowed_output_formats",
            [CLISandboxApplyOutputFormat.TEXT, CLISandboxApplyOutputFormat.JSON, CLISandboxApplyOutputFormat.MARKDOWN],
        ),
        allowed_decisions=kwargs.pop("allowed_decisions", [_decision_for_allowed_kind(kind)]),
        risk_kinds=kwargs.pop("risk_kinds", []),
        enabled=kwargs.pop("enabled", True),
        **kwargs,
    )


def default_cli_sandbox_apply_command_specs() -> list[CLISandboxApplyCommandSpec]:
    safe_kinds = [
        CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE,
        CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN,
        CLISandboxApplyCommandKind.SANDBOX_VALIDATE,
        CLISandboxApplyCommandKind.SANDBOX_RECONCILE,
        CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW,
        CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE,
        CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW,
        CLISandboxApplyCommandKind.NO_OP,
    ]
    denied_kinds = [
        CLISandboxApplyCommandKind.LIVE_APPLY_DENIED,
        CLISandboxApplyCommandKind.LIVE_WRITE_DENIED,
        CLISandboxApplyCommandKind.LIVE_EDIT_DENIED,
        CLISandboxApplyCommandKind.APPLY_PATCH_DENIED,
        CLISandboxApplyCommandKind.GIT_APPLY_DENIED,
        CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED,
        CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED,
        CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED,
        CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED,
        CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
        CLISandboxApplyCommandKind.DOMINION_DENIED,
        CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED,
        CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED,
    ]
    return [build_cli_sandbox_apply_command_spec(command_kind=kind, risk_kinds=_risks_for_denied_kind(kind) if kind in denied_kinds else []) for kind in safe_kinds + denied_kinds]


def build_cli_sandbox_apply_surface_policy(**kwargs: Any) -> CLISandboxApplySurfacePolicy:
    return CLISandboxApplySurfacePolicy(
        policy_id=kwargs.pop("policy_id", "cli_sandbox_apply_surface_policy:v0.36.8"),
        version=kwargs.pop("version", V0368_VERSION),
        allowed_command_kinds=kwargs.pop(
            "allowed_command_kinds",
            [
                CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP,
                CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS,
                CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW,
                CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW,
                CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE,
                CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW,
                CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW,
                CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN,
                CLISandboxApplyCommandKind.SANDBOX_VALIDATE,
                CLISandboxApplyCommandKind.SANDBOX_RECONCILE,
                CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW,
                CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE,
                CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW,
                CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW,
                CLISandboxApplyCommandKind.NO_OP,
            ],
        ),
        blocked_command_kinds=kwargs.pop(
            "blocked_command_kinds",
            [
                CLISandboxApplyCommandKind.LIVE_APPLY_DENIED,
                CLISandboxApplyCommandKind.LIVE_WRITE_DENIED,
                CLISandboxApplyCommandKind.LIVE_EDIT_DENIED,
                CLISandboxApplyCommandKind.APPLY_PATCH_DENIED,
                CLISandboxApplyCommandKind.GIT_APPLY_DENIED,
                CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED,
                CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED,
                CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED,
                CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED,
                CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
                CLISandboxApplyCommandKind.DOMINION_DENIED,
                CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED,
                CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED,
                CLISandboxApplyCommandKind.UNKNOWN,
            ],
        ),
        allowed_output_formats=kwargs.pop(
            "allowed_output_formats",
            [CLISandboxApplyOutputFormat.TEXT, CLISandboxApplyOutputFormat.MARKDOWN, CLISandboxApplyOutputFormat.JSON, CLISandboxApplyOutputFormat.STRUCTURED_ARTIFACT],
        ),
        prohibited_arg_patterns=kwargs.pop("prohibited_arg_patterns", DEFAULT_PROHIBITED_ARG_PATTERNS),
        max_arg_chars=kwargs.pop("max_arg_chars", DEFAULT_MAX_CLI_ARG_CHARS),
        allow_candidate_preview=kwargs.pop("allow_candidate_preview", True),
        allow_approval_validate=kwargs.pop("allow_approval_validate", True),
        allow_dry_run_preview=kwargs.pop("allow_dry_run_preview", True),
        allow_workspace_preview=kwargs.pop("allow_workspace_preview", True),
        allow_sandbox_apply_preview=kwargs.pop("allow_sandbox_apply_preview", True),
        allow_sandbox_apply_run=kwargs.pop("allow_sandbox_apply_run", True),
        allow_sandbox_post_apply_validation=kwargs.pop("allow_sandbox_post_apply_validation", True),
        allow_agentic_task_preview=kwargs.pop("allow_agentic_task_preview", True),
        allow_agentic_task_run_once=kwargs.pop("allow_agentic_task_run_once", True),
        allow_trace_preview=kwargs.pop("allow_trace_preview", True),
        allow_sandbox_file_write=kwargs.pop("allow_sandbox_file_write", True),
        allow_sandbox_patch_apply=kwargs.pop("allow_sandbox_patch_apply", True),
        **kwargs,
    )


def default_cli_sandbox_apply_surface_policy() -> CLISandboxApplySurfacePolicy:
    return build_cli_sandbox_apply_surface_policy()


def build_cli_sandbox_apply_surface(**kwargs: Any) -> CLISandboxApplySurface:
    return CLISandboxApplySurface(
        cli_surface_id=kwargs.pop("cli_surface_id", "cli_sandbox_apply_surface:v0.36.8"),
        version=kwargs.pop("version", V0368_VERSION),
        command_specs=kwargs.pop("command_specs", default_cli_sandbox_apply_command_specs()),
        policy=kwargs.pop("policy", default_cli_sandbox_apply_surface_policy()),
        flags=kwargs.pop("flags", build_cli_sandbox_apply_flags()),
        status=kwargs.pop("status", CLISandboxApplySurfaceStatus.INITIALIZED),
        readiness_level=kwargs.pop("readiness_level", CLISandboxApplyReadinessLevel.BOUNDED_CLI_SANDBOX_APPLY_SURFACE_READY),
        summary=kwargs.pop("summary", "bounded CLI sandbox apply and agentic task surface; not shell"),
        ready_for_cli_sandbox_apply_surface=kwargs.pop("ready_for_cli_sandbox_apply_surface", True),
        **kwargs,
    )


def build_default_cli_sandbox_apply_surface() -> CLISandboxApplySurface:
    return build_cli_sandbox_apply_surface()


def build_cli_sandbox_apply_invocation(**kwargs: Any) -> CLISandboxApplyInvocation:
    return CLISandboxApplyInvocation(
        invocation_id=kwargs.pop("invocation_id", "cli_sandbox_apply_invocation:v0.36.8"),
        argv=kwargs.pop("argv", ["sandbox-apply-help"]),
        command_kind=kwargs.pop("command_kind", CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP),
        command_mode=kwargs.pop("command_mode", CLISandboxApplyCommandMode.HELP),
        parsed_args=kwargs.pop("parsed_args", {}),
        requested_output_format=kwargs.pop("requested_output_format", CLISandboxApplyOutputFormat.TEXT),
        source_refs=kwargs.pop("source_refs", [build_cli_sandbox_apply_source_ref(source_kind=CLISandboxApplyInputSourceKind.ARGV_LIST)]),
        invocation_summary=kwargs.pop("invocation_summary", "bounded CLI sandbox apply invocation; not shell execution"),
        **kwargs,
    )


def build_cli_sandbox_apply_invocation_decision(**kwargs: Any) -> CLISandboxApplyInvocationDecision:
    return CLISandboxApplyInvocationDecision(
        decision_id=kwargs.pop("decision_id", "cli_sandbox_apply_decision:v0.36.8"),
        invocation_id=kwargs.pop("invocation_id", "cli_sandbox_apply_invocation:v0.36.8"),
        decision_kind=kwargs.pop("decision_kind", CLISandboxApplyDecisionKind.ALLOW_HELP),
        reason=kwargs.pop("reason", "bounded CLI command allowed without shell/live apply"),
        risk_kinds=kwargs.pop("risk_kinds", []),
        allowed_command_kind=kwargs.pop("allowed_command_kind", CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP),
        bounded_preview_allowed=kwargs.pop("bounded_preview_allowed", True),
        sandbox_apply_run_allowed=kwargs.pop("sandbox_apply_run_allowed", False),
        sandbox_file_write_allowed=kwargs.pop("sandbox_file_write_allowed", False),
        sandbox_patch_apply_allowed=kwargs.pop("sandbox_patch_apply_allowed", False),
        **kwargs,
    )


def build_cli_sandbox_apply_denied_command(**kwargs: Any) -> CLISandboxApplyDeniedCommand:
    return CLISandboxApplyDeniedCommand(
        denied_command_id=kwargs.pop("denied_command_id", "cli_sandbox_apply_denied:v0.36.8"),
        invocation_id=kwargs.pop("invocation_id", None),
        decision_id=kwargs.pop("decision_id", None),
        command_kind=kwargs.pop("command_kind", CLISandboxApplyCommandKind.UNKNOWN),
        risk_kinds=kwargs.pop("risk_kinds", [CLISandboxApplyRiskKind.UNKNOWN]),
        reason=kwargs.pop("reason", "command denied by v0.36.8 CLI sandbox apply surface"),
        safe_alternatives=kwargs.pop("safe_alternatives", ["sandbox-apply-help", "sandbox-apply-status", "sandbox-apply-preview"]),
        **kwargs,
    )


def build_cli_sandbox_apply_runtime_context(**kwargs: Any) -> CLISandboxApplyRuntimeContext:
    sandbox_root_ref = kwargs.pop("sandbox_root_ref", None)
    return CLISandboxApplyRuntimeContext(
        runtime_context_id=kwargs.pop("runtime_context_id", "cli_sandbox_apply_runtime_context:v0.36.8"),
        has_apply_candidate=kwargs.pop("has_apply_candidate", False),
        has_human_approval_contract=kwargs.pop("has_human_approval_contract", False),
        has_dry_run_result=kwargs.pop("has_dry_run_result", False),
        has_sandbox_workspace_manifest=kwargs.pop("has_sandbox_workspace_manifest", False),
        has_sandbox_apply_result=kwargs.pop("has_sandbox_apply_result", False),
        has_post_apply_validation_report=kwargs.pop("has_post_apply_validation_report", False),
        has_agentic_operation_run_packet=kwargs.pop("has_agentic_operation_run_packet", False),
        has_patch_apply_trace_packet=kwargs.pop("has_patch_apply_trace_packet", False),
        sandbox_root_ref=sandbox_root_ref,
        context_summary=kwargs.pop("context_summary", "bounded CLI runtime context; no credentials or shell access"),
        allows_sandbox_apply_run=kwargs.pop("allows_sandbox_apply_run", bool(sandbox_root_ref)),
        allows_sandbox_file_write=kwargs.pop("allows_sandbox_file_write", bool(sandbox_root_ref)),
        allows_sandbox_patch_apply=kwargs.pop("allows_sandbox_patch_apply", bool(sandbox_root_ref)),
        **kwargs,
    )


def build_cli_sandbox_apply_command_result(**kwargs: Any) -> CLISandboxApplyCommandResult:
    return CLISandboxApplyCommandResult(
        command_result_id=kwargs.pop("command_result_id", "cli_sandbox_apply_result:v0.36.8"),
        invocation_id=kwargs.pop("invocation_id", "cli_sandbox_apply_invocation:v0.36.8"),
        decision_id=kwargs.pop("decision_id", "cli_sandbox_apply_decision:v0.36.8"),
        command_kind=kwargs.pop("command_kind", CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP),
        status=kwargs.pop("status", CLISandboxApplySurfaceStatus.COMPLETED),
        apply_candidate_ref=kwargs.pop("apply_candidate_ref", None),
        dry_run_result_ref=kwargs.pop("dry_run_result_ref", None),
        sandbox_manifest_ref=kwargs.pop("sandbox_manifest_ref", None),
        sandbox_apply_result_ref=kwargs.pop("sandbox_apply_result_ref", None),
        post_apply_validation_report_ref=kwargs.pop("post_apply_validation_report_ref", None),
        agentic_operation_run_packet_ref=kwargs.pop("agentic_operation_run_packet_ref", None),
        trace_packet_ref=kwargs.pop("trace_packet_ref", None),
        structured_result=kwargs.pop("structured_result", {"ready_for_execution": False}),
        text_summary=kwargs.pop("text_summary", "bounded CLI sandbox apply result; not file write"),
        redacted=kwargs.pop("redacted", False),
        truncated=kwargs.pop("truncated", False),
        sandbox_write_performed=kwargs.pop("sandbox_write_performed", False),
        **kwargs,
    )


def build_cli_sandbox_apply_run_output(**kwargs: Any) -> CLISandboxApplyRunOutput:
    return CLISandboxApplyRunOutput(
        run_output_id=kwargs.pop("run_output_id", "cli_sandbox_apply_run_output:v0.36.8"),
        invocation_id=kwargs.pop("invocation_id", "cli_sandbox_apply_invocation:v0.36.8"),
        command_result=kwargs.pop("command_result", None),
        denied_command=kwargs.pop("denied_command", None),
        rendered_output=kwargs.pop("rendered_output", "bounded CLI sandbox apply output"),
        output_format=kwargs.pop("output_format", CLISandboxApplyOutputFormat.TEXT),
        status=kwargs.pop("status", CLISandboxApplySurfaceStatus.COMPLETED),
        summary=kwargs.pop("summary", "CLI sandbox apply output is returned in-memory; not file write"),
        **kwargs,
    )


def build_cli_sandbox_apply_run_report(**kwargs: Any) -> CLISandboxApplyRunReport:
    return CLISandboxApplyRunReport(
        run_report_id=kwargs.pop("run_report_id", "cli_sandbox_apply_run_report:v0.36.8"),
        version=kwargs.pop("version", V0368_VERSION),
        run_output_id=kwargs.pop("run_output_id", "cli_sandbox_apply_run_output:v0.36.8"),
        invocation_id=kwargs.pop("invocation_id", "cli_sandbox_apply_invocation:v0.36.8"),
        status=kwargs.pop("status", CLISandboxApplySurfaceStatus.COMPLETED),
        bounded_preview_count=kwargs.pop("bounded_preview_count", 1),
        sandbox_apply_run_count=kwargs.pop("sandbox_apply_run_count", 0),
        denied_command_count=kwargs.pop("denied_command_count", 0),
        blocked_command_count=kwargs.pop("blocked_command_count", 0),
        summary=kwargs.pop("summary", "CLI sandbox apply run report; not execution readiness"),
        sandbox_write_performed=kwargs.pop("sandbox_write_performed", False),
        **kwargs,
    )


def build_cli_sandbox_apply_run_preview(**kwargs: Any) -> CLISandboxApplyRunPreview:
    return CLISandboxApplyRunPreview(
        run_preview_id=kwargs.pop("run_preview_id", "cli_sandbox_apply_run_preview:v0.36.8"),
        cli_surface_id=kwargs.pop("cli_surface_id", "cli_sandbox_apply_surface:v0.36.8"),
        planned_steps=kwargs.pop("planned_steps", ["parse argv", "evaluate policy", "dispatch bounded helper", "return in-memory output"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["CLISandboxApplyInvocation", "CLISandboxApplyRunOutput"]),
        explicitly_not_performed=kwargs.pop(
            "explicitly_not_performed",
            ["shell execution", "live patch application", "test execution", "external agent execution", "trace persistence"],
        ),
        summary=kwargs.pop("summary", "bounded CLI sandbox apply run preview"),
        **kwargs,
    )


def build_cli_sandbox_apply_no_external_side_effect_guarantee(**kwargs: Any) -> CLISandboxApplyNoExternalSideEffectGuarantee:
    return CLISandboxApplyNoExternalSideEffectGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "cli_sandbox_apply_no_external_side_effect:v0.36.8"),
        version=kwargs.pop("version", V0368_VERSION),
        no_live_workspace_write=kwargs.pop("no_live_workspace_write", True),
        no_live_code_edit=kwargs.pop("no_live_code_edit", True),
        no_unrestricted_patch_application=kwargs.pop("no_unrestricted_patch_application", True),
        no_apply_patch=kwargs.pop("no_apply_patch", True),
        no_git_apply=kwargs.pop("no_git_apply", True),
        no_shell_execution=kwargs.pop("no_shell_execution", True),
        no_subprocess_execution=kwargs.pop("no_subprocess_execution", True),
        no_command_execution=kwargs.pop("no_command_execution", True),
        no_test_execution=kwargs.pop("no_test_execution", True),
        no_dependency_install=kwargs.pop("no_dependency_install", True),
        no_reference_execution=kwargs.pop("no_reference_execution", True),
        no_reference_import=kwargs.pop("no_reference_import", True),
        no_external_agent_execution=kwargs.pop("no_external_agent_execution", True),
        no_claude_code_invocation=kwargs.pop("no_claude_code_invocation", True),
        no_codex_cli_invocation=kwargs.pop("no_codex_cli_invocation", True),
        no_dominion_runtime=kwargs.pop("no_dominion_runtime", True),
        no_infinite_agent_loop=kwargs.pop("no_infinite_agent_loop", True),
        no_automatic_repair=kwargs.pop("no_automatic_repair", True),
        no_multi_cycle_loop=kwargs.pop("no_multi_cycle_loop", True),
        no_provider_invocation=kwargs.pop("no_provider_invocation", True),
        no_network_access=kwargs.pop("no_network_access", True),
        no_credential_access=kwargs.pop("no_credential_access", True),
        no_secret_read=kwargs.pop("no_secret_read", True),
        no_autonomous_runtime=kwargs.pop("no_autonomous_runtime", True),
        no_general_tool_execution=kwargs.pop("no_general_tool_execution", True),
        no_persistent_trace_write=kwargs.pop("no_persistent_trace_write", True),
        no_ui_runtime=kwargs.pop("no_ui_runtime", True),
        no_authority_grant=kwargs.pop("no_authority_grant", True),
        no_sandbox_write=kwargs.pop("no_sandbox_write", True),
        **kwargs,
    )


def build_v0368_readiness_report(**kwargs: Any) -> V0368ReadinessReport:
    return V0368ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0368_readiness_report"),
        version=kwargs.pop("version", V0368_VERSION),
        release_name=kwargs.pop("release_name", V0368_RELEASE_NAME),
        status=kwargs.pop("status", CLISandboxApplySurfaceStatus.COMPLETED),
        readiness_level=kwargs.pop("readiness_level", CLISandboxApplyReadinessLevel.BOUNDED_CLI_SANDBOX_APPLY_SURFACE_READY),
        ready_for_v0369_patch_apply_sandbox_consolidation=kwargs.pop("ready_for_v0369_patch_apply_sandbox_consolidation", True),
        ready_for_cli_sandbox_apply_surface=kwargs.pop("ready_for_cli_sandbox_apply_surface", True),
        ready_for_bounded_cli_sandbox_apply_preview=kwargs.pop("ready_for_bounded_cli_sandbox_apply_preview", True),
        ready_for_cli_apply_candidate_preview=kwargs.pop("ready_for_cli_apply_candidate_preview", True),
        ready_for_cli_dry_run_preview=kwargs.pop("ready_for_cli_dry_run_preview", True),
        ready_for_cli_sandbox_workspace_preview=kwargs.pop("ready_for_cli_sandbox_workspace_preview", True),
        ready_for_cli_sandbox_apply_run=kwargs.pop("ready_for_cli_sandbox_apply_run", True),
        ready_for_cli_sandbox_post_apply_validation=kwargs.pop("ready_for_cli_sandbox_post_apply_validation", True),
        ready_for_cli_agentic_task_run_once=kwargs.pop("ready_for_cli_agentic_task_run_once", True),
        ready_for_cli_trace_preview=kwargs.pop("ready_for_cli_trace_preview", True),
        ready_for_sandbox_file_write=kwargs.pop("ready_for_sandbox_file_write", True),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        **kwargs,
    )


def _mode_from_kind(kind: CLISandboxApplyCommandKind) -> CLISandboxApplyCommandMode:
    mapping = {
        CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP: CLISandboxApplyCommandMode.HELP,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS: CLISandboxApplyCommandMode.STATUS,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW: CLISandboxApplyCommandMode.DRY_RUN_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW: CLISandboxApplyCommandMode.CANDIDATE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE: CLISandboxApplyCommandMode.APPROVAL_VALIDATE,
        CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW: CLISandboxApplyCommandMode.WORKSPACE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW: CLISandboxApplyCommandMode.SANDBOX_APPLY_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN: CLISandboxApplyCommandMode.SANDBOX_APPLY_RUN,
        CLISandboxApplyCommandKind.SANDBOX_VALIDATE: CLISandboxApplyCommandMode.VALIDATION,
        CLISandboxApplyCommandKind.SANDBOX_RECONCILE: CLISandboxApplyCommandMode.RECONCILIATION,
        CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW: CLISandboxApplyCommandMode.AGENTIC_TASK_PREVIEW,
        CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE: CLISandboxApplyCommandMode.AGENTIC_TASK_RUN_ONCE,
        CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW: CLISandboxApplyCommandMode.TRACE_PREVIEW,
        CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW: CLISandboxApplyCommandMode.BUNDLE_PREVIEW,
        CLISandboxApplyCommandKind.NO_OP: CLISandboxApplyCommandMode.NO_OP,
    }
    if kind.value.endswith("_denied"):
        return CLISandboxApplyCommandMode.DENIED
    return mapping.get(kind, CLISandboxApplyCommandMode.UNKNOWN)


def _kind_from_command_token(token: str) -> CLISandboxApplyCommandKind:
    normalized = token.strip().lower()
    safe_map = {
        "sandbox-apply-help": CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP,
        "--help": CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP,
        "-h": CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP,
        "sandbox-apply-status": CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS,
        "sandbox-apply-dry-run-preview": CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW,
        "sandbox-apply-candidate-preview": CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW,
        "sandbox-approval-validate": CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE,
        "sandbox-workspace-preview": CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW,
        "sandbox-apply-preview": CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW,
        "sandbox-apply-run": CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN,
        "sandbox-validate": CLISandboxApplyCommandKind.SANDBOX_VALIDATE,
        "sandbox-reconcile": CLISandboxApplyCommandKind.SANDBOX_RECONCILE,
        "agentic-task-preview": CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW,
        "agentic-task-run-once": CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE,
        "sandbox-trace-preview": CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW,
        "sandbox-bundle-preview": CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW,
        "no-op": CLISandboxApplyCommandKind.NO_OP,
    }
    denied_map = {
        "patch-apply-live": CLISandboxApplyCommandKind.LIVE_APPLY_DENIED,
        "apply-live": CLISandboxApplyCommandKind.LIVE_APPLY_DENIED,
        "write-live": CLISandboxApplyCommandKind.LIVE_WRITE_DENIED,
        "edit-live": CLISandboxApplyCommandKind.LIVE_EDIT_DENIED,
        "workspace-write": CLISandboxApplyCommandKind.LIVE_WRITE_DENIED,
        "code-edit": CLISandboxApplyCommandKind.LIVE_EDIT_DENIED,
        "apply-patch": CLISandboxApplyCommandKind.APPLY_PATCH_DENIED,
        "git-apply": CLISandboxApplyCommandKind.GIT_APPLY_DENIED,
        "test-run": CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED,
        "pytest": CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED,
        "npm-test": CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED,
        "install": CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED,
        "npm": CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED,
        "pip": CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED,
        "shell": CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED,
        "bash": CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED,
        "powershell": CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED,
        "cmd": CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED,
        "run-opencode": CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED,
        "run-hermes": CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED,
        "run-openclaw": CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED,
        "run-claude-code": CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
        "run-codex": CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
        "external-agent-loop": CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
        "recursive-agent": CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
        "agent-chain": CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED,
        "harness-execute": CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED,
        "dominion": CLISandboxApplyCommandKind.DOMINION_DENIED,
        "infinite-loop": CLISandboxApplyCommandKind.DOMINION_DENIED,
        "auto-repair": CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED,
        "repair-loop": CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED,
        "retry-loop": CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED,
        "multi-cycle": CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED,
    }
    return safe_map.get(normalized) or denied_map.get(normalized) or CLISandboxApplyCommandKind.UNKNOWN


def _parse_option_pairs(tokens: list[str], max_arg_chars: int) -> dict[str, Any]:
    parsed: dict[str, Any] = {}
    index = 0
    while index < len(tokens):
        token = tokens[index][:max_arg_chars]
        if token.startswith("--"):
            key = "_".join(token[2:].split("-"))
            if index + 1 < len(tokens) and not tokens[index + 1].startswith("--"):
                parsed[key] = tokens[index + 1][:max_arg_chars]
                index += 2
            else:
                parsed[key] = True
                index += 1
        else:
            parsed.setdefault("positional", []).append(token)
            index += 1
    return parsed


def parse_cli_sandbox_apply_invocation(
    argv: list[str],
    surface: CLISandboxApplySurface | None = None,
) -> CLISandboxApplyInvocation:
    if not isinstance(argv, list) or not all(isinstance(arg, str) for arg in argv):
        raise TypeError("argv must be list[str]")
    active_surface = surface or build_default_cli_sandbox_apply_surface()
    safe_argv: list[str] = []
    input_redacted = False
    input_truncated = False
    for arg in argv:
        safe_arg, redacted, truncated = _sanitize_text(arg, active_surface.policy.max_arg_chars)
        safe_argv.append(safe_arg)
        input_redacted = input_redacted or redacted
        input_truncated = input_truncated or truncated
    tokens = list(safe_argv)
    if tokens and tokens[0] in {"sandbox", "sandbox-apply"}:
        tokens = tokens[1:]
    command_token = tokens[0] if tokens else "sandbox-apply-help"
    parsed_args = _parse_option_pairs(tokens[1:] if tokens else [], active_surface.policy.max_arg_chars)
    parsed_args["command_token"] = command_token
    requested_format = parsed_args.get("format", CLISandboxApplyOutputFormat.TEXT)
    try:
        output_format = CLISandboxApplyOutputFormat(requested_format)
    except ValueError:
        output_format = CLISandboxApplyOutputFormat.TEXT
    kind = _kind_from_command_token(command_token)
    return build_cli_sandbox_apply_invocation(
        invocation_id=f"cli_sandbox_apply_invocation:v0.36.8:{command_token.replace('-', '_') or 'help'}",
        argv=safe_argv,
        command_kind=kind,
        command_mode=_mode_from_kind(kind),
        parsed_args=parsed_args,
        requested_output_format=output_format,
        metadata={"passed_to_shell": False, "input_redacted": input_redacted, "input_truncated": input_truncated},
    )


def _risks_for_denied_kind(kind: CLISandboxApplyCommandKind) -> list[CLISandboxApplyRiskKind]:
    if kind == CLISandboxApplyCommandKind.LIVE_APPLY_DENIED:
        return [CLISandboxApplyRiskKind.LIVE_PATCH_APPLY_RISK]
    if kind == CLISandboxApplyCommandKind.LIVE_WRITE_DENIED:
        return [CLISandboxApplyRiskKind.LIVE_WORKSPACE_WRITE_RISK]
    if kind == CLISandboxApplyCommandKind.LIVE_EDIT_DENIED:
        return [CLISandboxApplyRiskKind.LIVE_CODE_EDIT_RISK]
    if kind == CLISandboxApplyCommandKind.APPLY_PATCH_DENIED:
        return [CLISandboxApplyRiskKind.APPLY_PATCH_RISK]
    if kind == CLISandboxApplyCommandKind.GIT_APPLY_DENIED:
        return [CLISandboxApplyRiskKind.GIT_APPLY_RISK]
    if kind == CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED:
        return [CLISandboxApplyRiskKind.TEST_EXECUTION_RISK]
    if kind == CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED:
        return [CLISandboxApplyRiskKind.DEPENDENCY_INSTALL_RISK]
    if kind == CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED:
        return [CLISandboxApplyRiskKind.SHELL_INJECTION_RISK, CLISandboxApplyRiskKind.COMMAND_EXECUTION_RISK]
    if kind == CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED:
        return [CLISandboxApplyRiskKind.REFERENCE_EXECUTION_RISK]
    if kind == CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED:
        return [CLISandboxApplyRiskKind.EXTERNAL_AGENT_EXECUTION_RISK]
    if kind == CLISandboxApplyCommandKind.DOMINION_DENIED:
        return [CLISandboxApplyRiskKind.DOMINION_RUNTIME_RISK, CLISandboxApplyRiskKind.INFINITE_AGENT_LOOP_RISK]
    if kind == CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED:
        return [CLISandboxApplyRiskKind.AUTOMATIC_REPAIR_RISK]
    if kind == CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED:
        return [CLISandboxApplyRiskKind.MULTI_CYCLE_LOOP_RISK]
    return [CLISandboxApplyRiskKind.UNKNOWN]


def _decision_for_denied_kind(kind: CLISandboxApplyCommandKind) -> CLISandboxApplyDecisionKind:
    mapping = {
        CLISandboxApplyCommandKind.LIVE_APPLY_DENIED: CLISandboxApplyDecisionKind.DENY_LIVE_APPLY,
        CLISandboxApplyCommandKind.LIVE_WRITE_DENIED: CLISandboxApplyDecisionKind.DENY_LIVE_WRITE_EDIT,
        CLISandboxApplyCommandKind.LIVE_EDIT_DENIED: CLISandboxApplyDecisionKind.DENY_LIVE_WRITE_EDIT,
        CLISandboxApplyCommandKind.APPLY_PATCH_DENIED: CLISandboxApplyDecisionKind.DENY_APPLY_PATCH,
        CLISandboxApplyCommandKind.GIT_APPLY_DENIED: CLISandboxApplyDecisionKind.DENY_GIT_APPLY,
        CLISandboxApplyCommandKind.TEST_EXECUTION_DENIED: CLISandboxApplyDecisionKind.DENY_TEST_EXECUTION,
        CLISandboxApplyCommandKind.DEPENDENCY_INSTALL_DENIED: CLISandboxApplyDecisionKind.DENY_DEPENDENCY_INSTALL,
        CLISandboxApplyCommandKind.SHELL_COMMAND_DENIED: CLISandboxApplyDecisionKind.DENY_SHELL_COMMAND,
        CLISandboxApplyCommandKind.REFERENCE_EXECUTION_DENIED: CLISandboxApplyDecisionKind.DENY_REFERENCE_EXECUTION,
        CLISandboxApplyCommandKind.EXTERNAL_AGENT_DENIED: CLISandboxApplyDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
        CLISandboxApplyCommandKind.DOMINION_DENIED: CLISandboxApplyDecisionKind.DENY_DOMINION_RUNTIME,
        CLISandboxApplyCommandKind.AUTO_REPAIR_DENIED: CLISandboxApplyDecisionKind.DENY_AUTO_REPAIR,
        CLISandboxApplyCommandKind.MULTI_CYCLE_DENIED: CLISandboxApplyDecisionKind.DENY_MULTI_CYCLE,
    }
    return mapping.get(kind, CLISandboxApplyDecisionKind.BLOCK)


def _unsafe_arg_risks(invocation: CLISandboxApplyInvocation, surface: CLISandboxApplySurface) -> list[CLISandboxApplyRiskKind]:
    joined = " ".join(invocation.argv).lower()
    risks: list[CLISandboxApplyRiskKind] = []
    if _contains_prohibited_text(joined, surface.policy.prohibited_arg_patterns):
        risks.append(CLISandboxApplyRiskKind.SHELL_INJECTION_RISK)
    risk_words = {
        "shell": CLISandboxApplyRiskKind.COMMAND_EXECUTION_RISK,
        "credential": CLISandboxApplyRiskKind.CREDENTIAL_ACCESS_RISK,
        "secret": CLISandboxApplyRiskKind.SECRET_READ_RISK,
        "token": CLISandboxApplyRiskKind.SECRET_READ_RISK,
        "opencode": CLISandboxApplyRiskKind.REFERENCE_EXECUTION_RISK,
        "hermes": CLISandboxApplyRiskKind.REFERENCE_EXECUTION_RISK,
        "openclaw": CLISandboxApplyRiskKind.REFERENCE_EXECUTION_RISK,
        "claude": CLISandboxApplyRiskKind.CLAUDE_CODE_INVOCATION_RISK,
        "codex": CLISandboxApplyRiskKind.CODEX_CLI_INVOCATION_RISK,
        "dominion": CLISandboxApplyRiskKind.DOMINION_RUNTIME_RISK,
        "auto-repair": CLISandboxApplyRiskKind.AUTOMATIC_REPAIR_RISK,
        "multi-cycle": CLISandboxApplyRiskKind.MULTI_CYCLE_LOOP_RISK,
    }
    for word, risk in risk_words.items():
        if word in joined:
            risks.append(risk)
    return list(dict.fromkeys(risks))


def evaluate_cli_sandbox_apply_invocation(
    invocation: CLISandboxApplyInvocation,
    surface: CLISandboxApplySurface,
    runtime_context: CLISandboxApplyRuntimeContext | None = None,
) -> CLISandboxApplyInvocationDecision:
    if not isinstance(invocation, CLISandboxApplyInvocation):
        raise TypeError("invocation must be CLISandboxApplyInvocation")
    if not isinstance(surface, CLISandboxApplySurface):
        raise TypeError("surface must be CLISandboxApplySurface")
    if runtime_context is not None and not isinstance(runtime_context, CLISandboxApplyRuntimeContext):
        raise TypeError("runtime_context must be CLISandboxApplyRuntimeContext")
    kind = CLISandboxApplyCommandKind(invocation.command_kind)
    if kind in surface.policy.blocked_command_kinds and kind != CLISandboxApplyCommandKind.UNKNOWN:
        return build_cli_sandbox_apply_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=_decision_for_denied_kind(kind),
            reason="unsafe CLI sandbox apply command denied without execution",
            risk_kinds=_risks_for_denied_kind(kind),
            allowed_command_kind=None,
            bounded_preview_allowed=False,
        )
    risks = _unsafe_arg_risks(invocation, surface)
    if invocation.metadata.get("input_redacted") or invocation.metadata.get("input_truncated"):
        risks.append(CLISandboxApplyRiskKind.UNBOUNDED_PAYLOAD_RISK if hasattr(CLISandboxApplyRiskKind, "UNBOUNDED_PAYLOAD_RISK") else CLISandboxApplyRiskKind.SECRET_READ_RISK)
    if kind == CLISandboxApplyCommandKind.UNKNOWN or risks:
        return build_cli_sandbox_apply_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=CLISandboxApplyDecisionKind.DENY_SHELL_COMMAND if risks else CLISandboxApplyDecisionKind.BLOCK,
            reason="unknown, shell-like, credential, external-agent, Dominion, or unsafe CLI input denied",
            risk_kinds=risks or [CLISandboxApplyRiskKind.UNKNOWN],
            allowed_command_kind=None,
            bounded_preview_allowed=False,
        )
    if kind not in surface.policy.allowed_command_kinds:
        return build_cli_sandbox_apply_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=CLISandboxApplyDecisionKind.DENY,
            reason="command is not enabled by v0.36.8 CLI policy",
            risk_kinds=[CLISandboxApplyRiskKind.UNKNOWN],
            allowed_command_kind=None,
            bounded_preview_allowed=False,
        )
    if kind == CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN:
        context_ok = (
            runtime_context is not None
            and runtime_context.sandbox_root_ref
            and runtime_context.allows_sandbox_apply_run
            and runtime_context.allows_sandbox_file_write
            and runtime_context.allows_sandbox_patch_apply
            and surface.policy.allow_sandbox_apply_run
            and surface.policy.allow_sandbox_file_write
            and surface.policy.allow_sandbox_patch_apply
        )
        if not context_ok:
            return build_cli_sandbox_apply_invocation_decision(
                decision_id=f"{invocation.invocation_id}:decision",
                invocation_id=invocation.invocation_id,
                decision_kind=CLISandboxApplyDecisionKind.REQUIRE_REVIEW,
                reason="sandbox-apply-run requires explicit validated sandbox root runtime context",
                risk_kinds=[CLISandboxApplyRiskKind.SANDBOX_ESCAPE_RISK],
                allowed_command_kind=None,
                bounded_preview_allowed=False,
            )
        return build_cli_sandbox_apply_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=CLISandboxApplyDecisionKind.ALLOW_SANDBOX_APPLY_RUN,
            reason="sandbox-apply-run allowed only through v0.36.4 sandbox helpers under explicit sandbox root",
            allowed_command_kind=kind,
            bounded_preview_allowed=False,
            sandbox_apply_run_allowed=True,
            sandbox_file_write_allowed=True,
            sandbox_patch_apply_allowed=True,
        )
    return build_cli_sandbox_apply_invocation_decision(
        decision_id=f"{invocation.invocation_id}:decision",
        invocation_id=invocation.invocation_id,
        decision_kind=_decision_for_allowed_kind(kind),
        reason="bounded CLI sandbox apply preview allowed; no shell/live apply/write/test execution",
        allowed_command_kind=kind,
        bounded_preview_allowed=kind != CLISandboxApplyCommandKind.NO_OP,
    )


def _context_value(runtime_context: CLISandboxApplyRuntimeContext | None, metadata_key: str, fallback: Any = None) -> Any:
    if runtime_context and metadata_key in runtime_context.metadata:
        return runtime_context.metadata[metadata_key]
    return fallback


def _command_result_for_allowed(
    invocation: CLISandboxApplyInvocation,
    decision: CLISandboxApplyInvocationDecision,
    runtime_context: CLISandboxApplyRuntimeContext | None,
) -> CLISandboxApplyCommandResult:
    kind = CLISandboxApplyCommandKind(invocation.command_kind)
    structured: dict[str, Any] = {
        "command": kind.value,
        "ready_for_execution": False,
        "live_workspace_write_allowed": False,
        "patch_application_allowed": False,
    }
    refs: dict[str, str | None] = {
        "apply_candidate_ref": None,
        "dry_run_result_ref": None,
        "sandbox_manifest_ref": None,
        "sandbox_apply_result_ref": None,
        "post_apply_validation_report_ref": None,
        "agentic_operation_run_packet_ref": None,
        "trace_packet_ref": None,
    }
    summary = "bounded CLI sandbox apply output"
    sandbox_write = False
    if kind in {CLISandboxApplyCommandKind.SANDBOX_APPLY_HELP, CLISandboxApplyCommandKind.SANDBOX_APPLY_STATUS}:
        structured["safe_commands"] = sorted(SAFE_COMMAND_NAMES)
        structured["denied_commands"] = sorted(DENIED_COMMAND_ALIASES)
        summary = "CLI sandbox apply surface status/help metadata only"
    if kind in {CLISandboxApplyCommandKind.SANDBOX_APPLY_CANDIDATE_PREVIEW, CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW}:
        candidate = build_apply_candidate_envelope()
        refs["apply_candidate_ref"] = _context_value(runtime_context, "apply_candidate_ref", candidate.candidate_id)
        structured["apply_candidate_id"] = refs["apply_candidate_ref"]
        summary = "apply candidate preview metadata only"
    if kind == CLISandboxApplyCommandKind.SANDBOX_APPROVAL_VALIDATE:
        contract = _context_value(runtime_context, "human_approval_contract", build_human_approval_contract())
        report = validate_human_approval_contract(contract)
        structured["human_approval_validation_successful"] = report.validation_successful
        summary = "human approval contract validation metadata only"
    if kind in {CLISandboxApplyCommandKind.SANDBOX_APPLY_DRY_RUN_PREVIEW, CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW}:
        dry_run = build_dry_run_apply_simulation_result()
        refs["dry_run_result_ref"] = _context_value(runtime_context, "dry_run_result_ref", dry_run.dry_run_result_id)
        structured["dry_run_result_id"] = refs["dry_run_result_ref"]
        summary = "dry-run patch apply simulation preview metadata only"
    if kind in {CLISandboxApplyCommandKind.SANDBOX_WORKSPACE_PREVIEW, CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW}:
        manifest = build_sandbox_workspace_manifest()
        refs["sandbox_manifest_ref"] = _context_value(runtime_context, "sandbox_manifest_ref", manifest.manifest_id)
        structured["sandbox_manifest_id"] = refs["sandbox_manifest_ref"]
        summary = "sandbox workspace manifest preview metadata only"
    if kind == CLISandboxApplyCommandKind.SANDBOX_APPLY_PREVIEW:
        apply_input = build_sandbox_patch_apply_input(sandbox_root_ref=_context_value(runtime_context, "sandbox_root_ref", "preview-sandbox-root"))
        refs["sandbox_apply_result_ref"] = apply_input.sandbox_apply_input_id
        structured["sandbox_apply_input_id"] = refs["sandbox_apply_result_ref"]
        summary = "sandbox apply preview metadata only; no write performed"
    if kind == CLISandboxApplyCommandKind.SANDBOX_APPLY_RUN:
        sandbox_root = runtime_context.sandbox_root_ref if runtime_context else None
        apply_input = _context_value(runtime_context, "sandbox_apply_input", None) or build_sandbox_patch_apply_input(sandbox_root_ref=str(sandbox_root))
        plan = _context_value(runtime_context, "materialization_plan", None) or build_sandbox_materialization_plan(sandbox_root_ref=str(sandbox_root))
        result = run_sandbox_patch_apply(apply_input, plan)
        refs["sandbox_apply_result_ref"] = result.sandbox_apply_result_id
        structured["sandbox_apply_result_id"] = result.sandbox_apply_result_id
        structured["files_written_count"] = result.files_written_count
        summary = "sandbox apply run completed through v0.36.4 sandbox helpers only"
        sandbox_write = bool(result.write_records)
    if kind in {CLISandboxApplyCommandKind.SANDBOX_VALIDATE, CLISandboxApplyCommandKind.SANDBOX_RECONCILE}:
        apply_result = _context_value(runtime_context, "sandbox_apply_result", None)
        if apply_result is not None and runtime_context and runtime_context.sandbox_root_ref:
            validation_input = build_sandbox_post_apply_validation_input(
                sandbox_apply_result_id=apply_result.sandbox_apply_result_id,
                sandbox_root_ref=runtime_context.sandbox_root_ref,
            )
            report = run_sandbox_post_apply_validation(validation_input, apply_result)
        else:
            report = build_sandbox_post_apply_validation_report()
        refs["post_apply_validation_report_ref"] = report.validation_report_id
        refs["sandbox_apply_result_ref"] = report.sandbox_apply_result_id
        structured["post_apply_validation_report_id"] = report.validation_report_id
        structured["validation_successful"] = report.validation_successful
        summary = "sandbox post-apply validation/reconciliation metadata only"
    if kind in {CLISandboxApplyCommandKind.AGENTIC_TASK_PREVIEW, CLISandboxApplyCommandKind.AGENTIC_TASK_RUN_ONCE}:
        report = _context_value(runtime_context, "post_apply_validation_report", build_sandbox_post_apply_validation_report())
        operation_input = build_agentic_operation_input_from_context(report)
        stage_refs = build_agentic_operation_stage_refs_from_v036_artifacts(post_apply_validation_report=report)
        packet = run_bounded_agentic_operation_cycle(operation_input, stage_refs, post_apply_validation_report=report)
        refs["agentic_operation_run_packet_ref"] = packet.run_packet_id
        structured["agentic_run_packet_id"] = packet.run_packet_id
        structured["single_cycle_only"] = packet.max_cycle_count == 1
        summary = "bounded agentic task run-once metadata; mandatory human handoff"
    if kind in {CLISandboxApplyCommandKind.SANDBOX_TRACE_PREVIEW, CLISandboxApplyCommandKind.SANDBOX_BUNDLE_PREVIEW}:
        run_packet = _context_value(runtime_context, "agentic_operation_run_packet", None)
        trace = build_trace_packet_from_agentic_operation_run_packet(run_packet) if run_packet is not None else build_patch_apply_sandbox_trace_packet()
        refs["trace_packet_ref"] = trace.trace_packet_id
        structured["trace_packet_id"] = trace.trace_packet_id
        structured["trace_persisted"] = False
        summary = "sandbox trace preview uses v0.36.7 returned packet only"
    if kind == CLISandboxApplyCommandKind.NO_OP:
        structured["no_op"] = True
        summary = "no-op completed without side effects"
    text, redacted, truncated = _bounded_json(structured)
    return build_cli_sandbox_apply_command_result(
        command_result_id=f"{invocation.invocation_id}:result",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=kind,
        status=CLISandboxApplySurfaceStatus.NO_OP if kind == CLISandboxApplyCommandKind.NO_OP else CLISandboxApplySurfaceStatus.COMPLETED,
        structured_result=structured,
        text_summary=summary,
        redacted=redacted,
        truncated=truncated,
        sandbox_write_performed=sandbox_write,
        metadata={"render_preview": text},
        **refs,
    )


def build_agentic_operation_input_from_context(post_apply_validation_report: Any) -> Any:
    return build_agentic_operation_input(
        post_apply_validation_report_id=getattr(post_apply_validation_report, "validation_report_id", None),
        sandbox_apply_result_id=getattr(post_apply_validation_report, "sandbox_apply_result_id", None),
        task_summary="bounded CLI agentic task run once; not autonomous runtime",
    )


def _run_output_from_denial(invocation: CLISandboxApplyInvocation, decision: CLISandboxApplyInvocationDecision) -> CLISandboxApplyRunOutput:
    denied = build_cli_sandbox_apply_denied_command(
        denied_command_id=f"{invocation.invocation_id}:denied",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=invocation.command_kind,
        risk_kinds=list(decision.risk_kinds),
        reason=decision.reason,
    )
    rendered, _, _ = _bounded_json(
        {
            "denied": denied.reason,
            "risk_kinds": [str(risk) for risk in denied.risk_kinds],
            "safe_alternatives": denied.safe_alternatives,
            "ready_for_execution": False,
        }
    )
    return build_cli_sandbox_apply_run_output(
        run_output_id=f"{invocation.invocation_id}:run_output",
        invocation_id=invocation.invocation_id,
        command_result=None,
        denied_command=denied,
        rendered_output=rendered,
        output_format=invocation.requested_output_format,
        status=CLISandboxApplySurfaceStatus.BLOCKED,
        summary="CLI sandbox apply command denied or blocked safely",
    )


def run_cli_sandbox_apply_command(
    invocation: CLISandboxApplyInvocation,
    surface: CLISandboxApplySurface,
    runtime_context: CLISandboxApplyRuntimeContext | None = None,
) -> CLISandboxApplyRunOutput:
    decision = evaluate_cli_sandbox_apply_invocation(invocation, surface, runtime_context)
    allowed_decisions = {
        CLISandboxApplyDecisionKind.ALLOW_HELP,
        CLISandboxApplyDecisionKind.ALLOW_STATUS,
        CLISandboxApplyDecisionKind.ALLOW_DRY_RUN_PREVIEW,
        CLISandboxApplyDecisionKind.ALLOW_CANDIDATE_PREVIEW,
        CLISandboxApplyDecisionKind.ALLOW_APPROVAL_VALIDATE,
        CLISandboxApplyDecisionKind.ALLOW_WORKSPACE_PREVIEW,
        CLISandboxApplyDecisionKind.ALLOW_SANDBOX_APPLY_PREVIEW,
        CLISandboxApplyDecisionKind.ALLOW_SANDBOX_APPLY_RUN,
        CLISandboxApplyDecisionKind.ALLOW_SANDBOX_VALIDATE,
        CLISandboxApplyDecisionKind.ALLOW_SANDBOX_RECONCILE,
        CLISandboxApplyDecisionKind.ALLOW_AGENTIC_TASK_PREVIEW,
        CLISandboxApplyDecisionKind.ALLOW_AGENTIC_TASK_RUN_ONCE,
        CLISandboxApplyDecisionKind.ALLOW_TRACE_PREVIEW,
        CLISandboxApplyDecisionKind.ALLOW_BUNDLE_PREVIEW,
        CLISandboxApplyDecisionKind.NO_OP,
    }
    if CLISandboxApplyDecisionKind(decision.decision_kind) not in allowed_decisions:
        return _run_output_from_denial(invocation, decision)
    result = _command_result_for_allowed(invocation, decision, runtime_context)
    pre_output = build_cli_sandbox_apply_run_output(
        run_output_id=f"{invocation.invocation_id}:run_output:pre_render",
        invocation_id=invocation.invocation_id,
        command_result=result,
        denied_command=None,
        rendered_output=result.metadata.get("render_preview", result.text_summary),
        output_format=invocation.requested_output_format,
        status=result.status,
        summary=result.text_summary,
    )
    rendered = render_cli_sandbox_apply_output(pre_output, invocation.requested_output_format)
    rendered, redacted, truncated = _sanitize_text(rendered, DEFAULT_MAX_RENDERED_OUTPUT_CHARS)
    safe_result = build_cli_sandbox_apply_command_result(
        **{**result.__dict__, "redacted": result.redacted or redacted, "truncated": result.truncated or truncated}
    )
    return build_cli_sandbox_apply_run_output(
        run_output_id=f"{invocation.invocation_id}:run_output",
        invocation_id=invocation.invocation_id,
        command_result=safe_result,
        denied_command=None,
        rendered_output=rendered,
        output_format=invocation.requested_output_format,
        status=result.status,
        summary=result.text_summary,
    )


def render_cli_sandbox_apply_output(
    output: CLISandboxApplyRunOutput,
    output_format: CLISandboxApplyOutputFormat | str | None = None,
) -> str:
    fmt = CLISandboxApplyOutputFormat(output_format or output.output_format)
    payload = {
        "status": str(output.status),
        "summary": output.summary,
        "ready_for_execution": output.ready_for_execution,
        "command_result": output.command_result.structured_result if output.command_result else None,
        "denied_command": output.denied_command.reason if output.denied_command else None,
    }
    if fmt == CLISandboxApplyOutputFormat.NO_OUTPUT:
        return "no output requested"
    if fmt in {CLISandboxApplyOutputFormat.JSON, CLISandboxApplyOutputFormat.STRUCTURED_ARTIFACT, CLISandboxApplyOutputFormat.DEBUG_SUMMARY}:
        return _bounded_json(payload)[0]
    if fmt == CLISandboxApplyOutputFormat.MARKDOWN:
        return _sanitize_text(f"**{payload['status']}**\n\n{payload['summary']}\n\n`ready_for_execution=False`")[0]
    return _sanitize_text(output.rendered_output or output.summary)[0]


def cli_sandbox_apply_flags_preserve_unsafe_false(flags: CLISandboxApplyFlagSet) -> bool:
    return isinstance(flags, CLISandboxApplyFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def cli_sandbox_apply_invocation_is_not_shell(invocation: CLISandboxApplyInvocation) -> bool:
    return isinstance(invocation.argv, list) and invocation.metadata.get("passed_to_shell") is not True


def cli_sandbox_apply_decision_blocks_live_apply(decision: CLISandboxApplyInvocationDecision) -> bool:
    return not any(
        getattr(decision, name)
        for name in (
            "live_workspace_write_allowed",
            "patch_application_allowed",
            "workspace_write_allowed",
            "code_edit_allowed",
            "apply_patch_allowed",
            "git_apply_allowed",
        )
    )


def cli_sandbox_apply_decision_blocks_external_agent(decision: CLISandboxApplyInvocationDecision) -> bool:
    return not any(
        getattr(decision, name)
        for name in (
            "external_agent_execution_allowed",
            "claude_code_invocation_allowed",
            "codex_cli_invocation_allowed",
            "dominion_runtime_allowed",
            "infinite_agent_loop_allowed",
            "automatic_repair_allowed",
            "multi_cycle_loop_allowed",
        )
    )


def cli_sandbox_apply_surface_is_not_shell(surface: CLISandboxApplySurface) -> bool:
    return (
        surface.ready_for_execution is False
        and surface.policy.allow_shell is False
        and surface.policy.allow_subprocess is False
        and surface.policy.allow_command_execution is False
    )


def v0368_readiness_report_is_not_execution_ready(report: V0368ReadinessReport) -> bool:
    return isinstance(report, V0368ReadinessReport) and all(getattr(report, name) is False for name in UNSAFE_FLAG_NAMES)
