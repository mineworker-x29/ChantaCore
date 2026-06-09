from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_context import build_patch_context_snapshot
from .patch_diff_proposal import build_diff_proposal_envelope
from .patch_intent import build_patch_intent_scope_bundle
from .patch_ocel_trace import build_patch_proposal_trace_packet
from .patch_plan import build_patch_plan
from .patch_review import build_patch_review_packet
from .patch_risk import build_patch_proposal_risk_report


V0358_VERSION = "v0.35.8"
V0358_RELEASE_NAME = "v0.35.8 CLI Patch Proposal Surface"
DEFAULT_MAX_CLI_ARG_CHARS = 240
DEFAULT_MAX_RENDERED_OUTPUT_CHARS = 1200

SAFE_COMMAND_NAMES = {
    "patch-help",
    "--help",
    "-h",
    "patch-status",
    "patch-dry-run",
    "patch-intent-preview",
    "patch-scope-preview",
    "patch-context-preview",
    "patch-plan-preview",
    "patch-diff-preview",
    "patch-risk",
    "patch-review",
    "patch-trace-preview",
    "patch-bundle-preview",
    "no-op",
}

DENIED_COMMAND_ALIASES = {
    "patch-apply",
    "apply",
    "write",
    "edit",
    "git-apply",
    "apply-patch",
    "test-run",
    "pytest",
    "install",
    "npm",
    "pip",
    "shell",
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
    "patch-apply",
    "git apply",
    "apply_patch",
    "apply-patch",
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
]

UNSAFE_CLI_PATCH_PROPOSAL_FLAG_NAMES = (
    "ready_for_execution",
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
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

UNSAFE_DECISION_ALLOWED_NAMES = (
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
    "provider_invocation_allowed",
    "network_access_allowed",
    "credential_access_allowed",
    "secret_read_allowed",
    "persistent_trace_write_allowed",
    "ui_runtime_allowed",
)


class CLIPatchProposalCommandKind(StrEnum):
    PATCH_HELP = "patch_help"
    PATCH_STATUS = "patch_status"
    PATCH_DRY_RUN = "patch_dry_run"
    PATCH_INTENT_PREVIEW = "patch_intent_preview"
    PATCH_SCOPE_PREVIEW = "patch_scope_preview"
    PATCH_CONTEXT_PREVIEW = "patch_context_preview"
    PATCH_PLAN_PREVIEW = "patch_plan_preview"
    PATCH_DIFF_PREVIEW = "patch_diff_preview"
    PATCH_RISK = "patch_risk"
    PATCH_REVIEW = "patch_review"
    PATCH_TRACE_PREVIEW = "patch_trace_preview"
    PATCH_BUNDLE_PREVIEW = "patch_bundle_preview"
    PATCH_APPLY_DENIED = "patch_apply_denied"
    PATCH_WRITE_DENIED = "patch_write_denied"
    PATCH_EDIT_DENIED = "patch_edit_denied"
    PATCH_TEST_DENIED = "patch_test_denied"
    PATCH_INSTALL_DENIED = "patch_install_denied"
    EXTERNAL_AGENT_DENIED = "external_agent_denied"
    DOMINION_DENIED = "dominion_denied"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLIPatchProposalCommandMode(StrEnum):
    HELP = "help"
    STATUS = "status"
    DRY_RUN = "dry_run"
    INTENT_PREVIEW = "intent_preview"
    SCOPE_PREVIEW = "scope_preview"
    CONTEXT_PREVIEW = "context_preview"
    PLAN_PREVIEW = "plan_preview"
    DIFF_PREVIEW = "diff_preview"
    RISK_PREVIEW = "risk_preview"
    REVIEW_PREVIEW = "review_preview"
    TRACE_PREVIEW = "trace_preview"
    BUNDLE_PREVIEW = "bundle_preview"
    DENIED = "denied"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class CLIPatchProposalInputSourceKind(StrEnum):
    ARGV_LIST = "argv_list"
    PARSED_ARGS = "parsed_args"
    RUNTIME_CONTEXT = "runtime_context"
    INTENT_TEXT_ARG = "intent_text_arg"
    SCOPE_ARG = "scope_arg"
    TASK_ARG = "task_arg"
    PATCH_INTENT_REF = "patch_intent_ref"
    PATCH_CONTEXT_SNAPSHOT_REF = "patch_context_snapshot_ref"
    PATCH_PLAN_REF = "patch_plan_ref"
    DIFF_ENVELOPE_REF = "diff_envelope_ref"
    RISK_REPORT_REF = "risk_report_ref"
    REVIEW_PACKET_REF = "review_packet_ref"
    TRACE_PACKET_REF = "trace_packet_ref"
    REFERENCE_DIGEST_REF = "reference_digest_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class CLIPatchProposalSurfaceStatus(StrEnum):
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


class CLIPatchProposalDecisionKind(StrEnum):
    ALLOW_HELP = "allow_help"
    ALLOW_STATUS = "allow_status"
    ALLOW_DRY_RUN = "allow_dry_run"
    ALLOW_INTENT_PREVIEW = "allow_intent_preview"
    ALLOW_SCOPE_PREVIEW = "allow_scope_preview"
    ALLOW_CONTEXT_PREVIEW = "allow_context_preview"
    ALLOW_PLAN_PREVIEW = "allow_plan_preview"
    ALLOW_DIFF_PREVIEW = "allow_diff_preview"
    ALLOW_RISK_PREVIEW = "allow_risk_preview"
    ALLOW_REVIEW_PREVIEW = "allow_review_preview"
    ALLOW_TRACE_PREVIEW = "allow_trace_preview"
    ALLOW_BUNDLE_PREVIEW = "allow_bundle_preview"
    DENY_PATCH_APPLY = "deny_patch_apply"
    DENY_WRITE_EDIT = "deny_write_edit"
    DENY_TEST_EXECUTION = "deny_test_execution"
    DENY_DEPENDENCY_INSTALL = "deny_dependency_install"
    DENY_SHELL_COMMAND = "deny_shell_command"
    DENY_REFERENCE_EXECUTION = "deny_reference_execution"
    DENY_EXTERNAL_AGENT_EXECUTION = "deny_external_agent_execution"
    DENY_DOMINION_RUNTIME = "deny_dominion_runtime"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class CLIPatchProposalOutputFormat(StrEnum):
    TEXT = "text"
    MARKDOWN = "markdown"
    JSON = "json"
    STRUCTURED_ARTIFACT = "structured_artifact"
    DEBUG_SUMMARY = "debug_summary"
    NO_OUTPUT = "no_output"
    UNKNOWN = "unknown"


class CLIPatchProposalRiskKind(StrEnum):
    SHELL_INJECTION_RISK = "shell_injection_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    REFERENCE_IMPORT_RISK = "reference_import_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    CLAUDE_CODE_INVOCATION_RISK = "claude_code_invocation_risk"
    CODEX_CLI_INVOCATION_RISK = "codex_cli_invocation_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    INFINITE_AGENT_LOOP_RISK = "infinite_agent_loop_risk"
    DIRECT_PROVIDER_INVOCATION_RISK = "direct_provider_invocation_risk"
    DIRECT_NETWORK_ACCESS_RISK = "direct_network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_READ_RISK = "secret_read_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    UI_RUNTIME_RISK = "ui_runtime_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class CLIPatchProposalReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CLI_CONTRACT_READY = "cli_contract_ready"
    BOUNDED_CLI_PATCH_PROPOSAL_SURFACE_READY = "bounded_cli_patch_proposal_surface_ready"
    BOUNDED_PREVIEW_COMMAND_DISPATCH_READY = "bounded_preview_command_dispatch_ready"
    DESIGN_HANDOFF_READY_FOR_V0359 = "design_handoff_ready_for_v0359"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0358_VERSION not in version:
        raise ValueError("version must include v0.35.8")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    _validate_list(name, values)
    for value in values:
        enum_type(value)


def _validate_non_negative(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.8")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret", "credential", "api_key", "token")):
            raise ValueError("metadata keys must not request credentials or secrets")


def _contains_prohibited_text(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _bounded_text(value: Any, max_chars: int = DEFAULT_MAX_RENDERED_OUTPUT_CHARS) -> tuple[str, bool, bool]:
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str)
    redacted = _contains_prohibited_text(text, ["secret", "token", "credential", "api_key", "id_rsa", ".env", "private key"])
    if redacted:
        text = "[redacted]"
    truncated = len(text) > max_chars
    if truncated:
        marker = "...[truncated]"
        text = text[: max(max_chars - len(marker), 0)] + marker
    return text, redacted, truncated


def _command_mode_for_kind(command_kind: CLIPatchProposalCommandKind | str) -> CLIPatchProposalCommandMode:
    kind = CLIPatchProposalCommandKind(command_kind)
    mapping = {
        CLIPatchProposalCommandKind.PATCH_HELP: CLIPatchProposalCommandMode.HELP,
        CLIPatchProposalCommandKind.PATCH_STATUS: CLIPatchProposalCommandMode.STATUS,
        CLIPatchProposalCommandKind.PATCH_DRY_RUN: CLIPatchProposalCommandMode.DRY_RUN,
        CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW: CLIPatchProposalCommandMode.INTENT_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW: CLIPatchProposalCommandMode.SCOPE_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW: CLIPatchProposalCommandMode.CONTEXT_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW: CLIPatchProposalCommandMode.PLAN_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW: CLIPatchProposalCommandMode.DIFF_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_RISK: CLIPatchProposalCommandMode.RISK_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_REVIEW: CLIPatchProposalCommandMode.REVIEW_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW: CLIPatchProposalCommandMode.TRACE_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW: CLIPatchProposalCommandMode.BUNDLE_PREVIEW,
        CLIPatchProposalCommandKind.NO_OP: CLIPatchProposalCommandMode.NO_OP,
    }
    if kind in {
        CLIPatchProposalCommandKind.PATCH_APPLY_DENIED,
        CLIPatchProposalCommandKind.PATCH_WRITE_DENIED,
        CLIPatchProposalCommandKind.PATCH_EDIT_DENIED,
        CLIPatchProposalCommandKind.PATCH_TEST_DENIED,
        CLIPatchProposalCommandKind.PATCH_INSTALL_DENIED,
        CLIPatchProposalCommandKind.EXTERNAL_AGENT_DENIED,
        CLIPatchProposalCommandKind.DOMINION_DENIED,
    }:
        return CLIPatchProposalCommandMode.DENIED
    return mapping.get(kind, CLIPatchProposalCommandMode.UNKNOWN)


def _decision_for_allowed_kind(command_kind: CLIPatchProposalCommandKind | str) -> CLIPatchProposalDecisionKind:
    kind = CLIPatchProposalCommandKind(command_kind)
    return {
        CLIPatchProposalCommandKind.PATCH_HELP: CLIPatchProposalDecisionKind.ALLOW_HELP,
        CLIPatchProposalCommandKind.PATCH_STATUS: CLIPatchProposalDecisionKind.ALLOW_STATUS,
        CLIPatchProposalCommandKind.PATCH_DRY_RUN: CLIPatchProposalDecisionKind.ALLOW_DRY_RUN,
        CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_INTENT_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_SCOPE_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_CONTEXT_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_PLAN_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_DIFF_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_RISK: CLIPatchProposalDecisionKind.ALLOW_RISK_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_REVIEW: CLIPatchProposalDecisionKind.ALLOW_REVIEW_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_TRACE_PREVIEW,
        CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW: CLIPatchProposalDecisionKind.ALLOW_BUNDLE_PREVIEW,
        CLIPatchProposalCommandKind.NO_OP: CLIPatchProposalDecisionKind.NO_OP,
    }.get(kind, CLIPatchProposalDecisionKind.BLOCK)


def _kind_from_command_token(command_token: str) -> CLIPatchProposalCommandKind:
    token = command_token.lower()
    if token in {"patch-help", "--help", "-h"}:
        return CLIPatchProposalCommandKind.PATCH_HELP
    if token == "patch-status":
        return CLIPatchProposalCommandKind.PATCH_STATUS
    if token == "patch-dry-run":
        return CLIPatchProposalCommandKind.PATCH_DRY_RUN
    if token == "patch-intent-preview":
        return CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW
    if token == "patch-scope-preview":
        return CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW
    if token == "patch-context-preview":
        return CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW
    if token == "patch-plan-preview":
        return CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW
    if token == "patch-diff-preview":
        return CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW
    if token == "patch-risk":
        return CLIPatchProposalCommandKind.PATCH_RISK
    if token == "patch-review":
        return CLIPatchProposalCommandKind.PATCH_REVIEW
    if token == "patch-trace-preview":
        return CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW
    if token == "patch-bundle-preview":
        return CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW
    if token in {"patch-apply", "apply", "git-apply", "apply-patch"}:
        return CLIPatchProposalCommandKind.PATCH_APPLY_DENIED
    if token == "write":
        return CLIPatchProposalCommandKind.PATCH_WRITE_DENIED
    if token == "edit":
        return CLIPatchProposalCommandKind.PATCH_EDIT_DENIED
    if token in {"test-run", "pytest"}:
        return CLIPatchProposalCommandKind.PATCH_TEST_DENIED
    if token in {"install", "npm", "pip"}:
        return CLIPatchProposalCommandKind.PATCH_INSTALL_DENIED
    if token in {"run-opencode", "run-hermes", "run-openclaw", "run-claude-code", "run-codex", "external-agent-loop", "recursive-agent", "agent-chain", "harness-execute"}:
        return CLIPatchProposalCommandKind.EXTERNAL_AGENT_DENIED
    if token in {"dominion", "infinite-loop"}:
        return CLIPatchProposalCommandKind.DOMINION_DENIED
    if token == "no-op":
        return CLIPatchProposalCommandKind.NO_OP
    return CLIPatchProposalCommandKind.UNKNOWN


@dataclass(frozen=True)
class CLIPatchProposalFlagSet:
    flag_set_id: str
    version: str
    cli_patch_proposal_surface_constructed: bool
    cli_argument_parsing_enabled: bool
    bounded_preview_command_dispatch_enabled: bool
    denied_unsafe_command_handling_enabled: bool
    ready_for_v0359_consolidation: bool
    ready_for_cli_patch_proposal_surface: bool
    ready_for_bounded_cli_patch_proposal_preview: bool
    ready_for_cli_patch_intent_preview: bool
    ready_for_cli_patch_context_preview: bool
    ready_for_cli_patch_plan_preview: bool
    ready_for_cli_diff_proposal_preview: bool
    ready_for_cli_patch_risk_preview: bool
    ready_for_cli_patch_review_preview: bool
    ready_for_cli_patch_trace_preview: bool
    ready_for_execution: bool = False
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
        _validate_false(self, UNSAFE_CLI_PATCH_PROPOSAL_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalSourceRef:
    source_ref_id: str
    source_kind: CLIPatchProposalInputSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        CLIPatchProposalInputSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalArgumentSpec:
    argument_spec_id: str
    name: str
    required: bool = False
    allowed_values: list[str] = field(default_factory=list)
    prohibited_values: list[str] = field(default_factory=list)
    allow_text_value: bool = True
    allow_ref_value: bool = True
    allow_json_value: bool = False
    max_value_chars: int = DEFAULT_MAX_CLI_ARG_CHARS
    description: str = "Bounded CLI patch proposal argument."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("argument_spec_id", self.argument_spec_id)
        _require_non_blank("name", self.name)
        _validate_string_list("allowed_values", self.allowed_values)
        _validate_string_list("prohibited_values", self.prohibited_values)
        _validate_non_negative("max_value_chars", self.max_value_chars)
        _require_non_blank("description", self.description)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalCommandSpec:
    command_spec_id: str
    command_kind: CLIPatchProposalCommandKind | str
    command_mode: CLIPatchProposalCommandMode | str
    command_name: str
    description: str
    argument_specs: list[CLIPatchProposalArgumentSpec] = field(default_factory=list)
    allowed_output_formats: list[CLIPatchProposalOutputFormat | str] = field(default_factory=lambda: [CLIPatchProposalOutputFormat.TEXT, CLIPatchProposalOutputFormat.JSON, CLIPatchProposalOutputFormat.MARKDOWN])
    allowed_decisions: list[CLIPatchProposalDecisionKind | str] = field(default_factory=list)
    risk_kinds: list[CLIPatchProposalRiskKind | str] = field(default_factory=list)
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("command_spec_id", self.command_spec_id)
        kind = CLIPatchProposalCommandKind(self.command_kind)
        CLIPatchProposalCommandMode(self.command_mode)
        _require_non_blank("command_name", self.command_name)
        _require_non_blank("description", self.description)
        _validate_list("argument_specs", self.argument_specs)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLIPatchProposalOutputFormat)
        _validate_enum_list("allowed_decisions", self.allowed_decisions, CLIPatchProposalDecisionKind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIPatchProposalRiskKind)
        if self.enabled and kind in {CLIPatchProposalCommandKind.UNKNOWN}:
            raise ValueError("unknown command spec cannot be enabled")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalSurfacePolicy:
    policy_id: str
    version: str
    allowed_command_kinds: list[CLIPatchProposalCommandKind | str]
    blocked_command_kinds: list[CLIPatchProposalCommandKind | str]
    allowed_output_formats: list[CLIPatchProposalOutputFormat | str]
    prohibited_arg_patterns: list[str]
    max_arg_chars: int
    allow_patch_intent_preview: bool = True
    allow_patch_context_preview: bool = True
    allow_patch_plan_preview: bool = True
    allow_diff_proposal_preview: bool = True
    allow_patch_risk_preview: bool = True
    allow_patch_review_preview: bool = True
    allow_patch_trace_preview: bool = True
    allow_shell: bool = False
    allow_subprocess: bool = False
    allow_command_execution: bool = False
    allow_patch_application: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_apply_patch: bool = False
    allow_git_apply: bool = False
    allow_test_execution: bool = False
    allow_dependency_install: bool = False
    allow_reference_execution: bool = False
    allow_reference_import: bool = False
    allow_external_agent_execution: bool = False
    allow_claude_code_invocation: bool = False
    allow_codex_cli_invocation: bool = False
    allow_dominion_runtime: bool = False
    allow_infinite_agent_loop: bool = False
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
        _validate_enum_list("allowed_command_kinds", self.allowed_command_kinds, CLIPatchProposalCommandKind)
        _validate_enum_list("blocked_command_kinds", self.blocked_command_kinds, CLIPatchProposalCommandKind)
        _validate_enum_list("allowed_output_formats", self.allowed_output_formats, CLIPatchProposalOutputFormat)
        _validate_string_list("prohibited_arg_patterns", self.prohibited_arg_patterns)
        lowered = {pattern.lower() for pattern in self.prohibited_arg_patterns}
        for required in (";", "|", "apply_patch", "git apply", "credential", "secret", "external-agent", "dominion", "infinite-loop"):
            if required not in lowered:
                raise ValueError("prohibited_arg_patterns missing required v0.35.8 pattern")
        _validate_non_negative("max_arg_chars", self.max_arg_chars)
        _validate_false(
            self,
            (
                "allow_shell",
                "allow_subprocess",
                "allow_command_execution",
                "allow_patch_application",
                "allow_workspace_write",
                "allow_code_edit",
                "allow_apply_patch",
                "allow_git_apply",
                "allow_test_execution",
                "allow_dependency_install",
                "allow_reference_execution",
                "allow_reference_import",
                "allow_external_agent_execution",
                "allow_claude_code_invocation",
                "allow_codex_cli_invocation",
                "allow_dominion_runtime",
                "allow_infinite_agent_loop",
                "allow_provider_invocation",
                "allow_network_access",
                "allow_credential_access",
                "allow_secret_read",
                "allow_persistent_trace_write",
                "allow_ui_runtime",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalSurface:
    cli_surface_id: str
    version: str
    command_specs: list[CLIPatchProposalCommandSpec]
    policy: CLIPatchProposalSurfacePolicy
    flags: CLIPatchProposalFlagSet
    status: CLIPatchProposalSurfaceStatus | str
    readiness_level: CLIPatchProposalReadinessLevel | str
    summary: str
    ready_for_cli_patch_proposal_surface: bool
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("cli_surface_id", self.cli_surface_id)
        _validate_version(self.version)
        _validate_list("command_specs", self.command_specs)
        if not isinstance(self.policy, CLIPatchProposalSurfacePolicy):
            raise TypeError("policy must be CLIPatchProposalSurfacePolicy")
        if not cli_patch_proposal_flags_preserve_unsafe_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        CLIPatchProposalSurfaceStatus(self.status)
        CLIPatchProposalReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.35.8")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalInvocation:
    invocation_id: str
    argv: list[str]
    command_kind: CLIPatchProposalCommandKind | str
    command_mode: CLIPatchProposalCommandMode | str
    parsed_args: dict[str, Any]
    requested_output_format: CLIPatchProposalOutputFormat | str
    source_refs: list[CLIPatchProposalSourceRef]
    invocation_summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("invocation_id", self.invocation_id)
        _validate_list("argv", self.argv)
        if not all(isinstance(arg, str) for arg in self.argv):
            raise TypeError("argv must be list[str]")
        CLIPatchProposalCommandKind(self.command_kind)
        CLIPatchProposalCommandMode(self.command_mode)
        _validate_dict("parsed_args", self.parsed_args)
        CLIPatchProposalOutputFormat(self.requested_output_format)
        _validate_list("source_refs", self.source_refs)
        _require_non_blank("invocation_summary", self.invocation_summary)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalInvocationDecision:
    decision_id: str
    invocation_id: str
    decision_kind: CLIPatchProposalDecisionKind | str
    reason: str
    risk_kinds: list[CLIPatchProposalRiskKind | str] = field(default_factory=list)
    allowed_command_kind: CLIPatchProposalCommandKind | str | None = None
    bounded_preview_allowed: bool = False
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
    provider_invocation_allowed: bool = False
    network_access_allowed: bool = False
    credential_access_allowed: bool = False
    secret_read_allowed: bool = False
    persistent_trace_write_allowed: bool = False
    ui_runtime_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("invocation_id", self.invocation_id)
        CLIPatchProposalDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIPatchProposalRiskKind)
        if self.allowed_command_kind is not None:
            CLIPatchProposalCommandKind(self.allowed_command_kind)
        _validate_false(self, UNSAFE_DECISION_ALLOWED_NAMES)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalDeniedCommand:
    denied_command_id: str
    invocation_id: str | None
    decision_id: str | None
    command_kind: CLIPatchProposalCommandKind | str
    risk_kinds: list[CLIPatchProposalRiskKind | str]
    reason: str
    safe_alternatives: list[str] = field(default_factory=lambda: ["patch-help", "patch-dry-run", "patch-bundle-preview"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("denied_command_id", self.denied_command_id)
        if self.invocation_id is not None:
            _require_non_blank("invocation_id", self.invocation_id)
        if self.decision_id is not None:
            _require_non_blank("decision_id", self.decision_id)
        CLIPatchProposalCommandKind(self.command_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, CLIPatchProposalRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalRuntimeContext:
    runtime_context_id: str
    has_patch_intent_artifacts: bool = False
    has_patch_context_snapshot: bool = False
    has_patch_plan: bool = False
    has_diff_envelope: bool = False
    has_risk_report: bool = False
    has_review_packet: bool = False
    has_trace_packet: bool = False
    has_reference_digest: bool = False
    context_summary: str = "In-memory CLI patch proposal runtime context metadata."
    allows_patch_application: bool = False
    allows_workspace_write: bool = False
    allows_code_edit: bool = False
    allows_shell: bool = False
    allows_external_agent_execution: bool = False
    allows_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("runtime_context_id", self.runtime_context_id)
        _require_non_blank("context_summary", self.context_summary)
        _validate_false(self, ("allows_patch_application", "allows_workspace_write", "allows_code_edit", "allows_shell", "allows_external_agent_execution", "allows_dominion_runtime"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalCommandResult:
    command_result_id: str
    invocation_id: str
    decision_id: str
    command_kind: CLIPatchProposalCommandKind | str
    status: CLIPatchProposalSurfaceStatus | str
    patch_intent_ref: str | None = None
    patch_context_snapshot_ref: str | None = None
    patch_plan_ref: str | None = None
    diff_envelope_ref: str | None = None
    risk_report_ref: str | None = None
    review_packet_ref: str | None = None
    trace_packet_ref: str | None = None
    structured_result: dict[str, Any] = field(default_factory=dict)
    text_summary: str = "Bounded CLI patch proposal command result."
    redacted: bool = False
    truncated: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("command_result_id", "invocation_id", "decision_id", "text_summary"):
            _require_non_blank(name, getattr(self, name))
        CLIPatchProposalCommandKind(self.command_kind)
        CLIPatchProposalSurfaceStatus(self.status)
        _validate_dict("structured_result", self.structured_result)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.35.8")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalRunOutput:
    run_output_id: str
    invocation_id: str
    command_result: CLIPatchProposalCommandResult | None
    denied_command: CLIPatchProposalDeniedCommand | None
    rendered_output: str
    output_format: CLIPatchProposalOutputFormat | str
    status: CLIPatchProposalSurfaceStatus | str
    summary: str
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_output_id", "invocation_id", "rendered_output", "summary"):
            _require_non_blank(name, getattr(self, name))
        if self.command_result is not None and not isinstance(self.command_result, CLIPatchProposalCommandResult):
            raise TypeError("command_result must be CLIPatchProposalCommandResult")
        if self.denied_command is not None and not isinstance(self.denied_command, CLIPatchProposalDeniedCommand):
            raise TypeError("denied_command must be CLIPatchProposalDeniedCommand")
        CLIPatchProposalOutputFormat(self.output_format)
        CLIPatchProposalSurfaceStatus(self.status)
        if len(self.rendered_output) > DEFAULT_MAX_RENDERED_OUTPUT_CHARS:
            raise ValueError("rendered_output must be bounded")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.35.8")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalRunReport:
    run_report_id: str
    version: str
    run_output_id: str
    invocation_id: str
    status: CLIPatchProposalSurfaceStatus | str
    bounded_preview_count: int
    denied_command_count: int
    blocked_command_count: int
    summary: str
    ready_for_cli_patch_proposal_surface: bool = True
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_shell_execution: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_persistent_trace_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("run_report_id", "run_output_id", "invocation_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        CLIPatchProposalSurfaceStatus(self.status)
        for name in ("bounded_preview_count", "denied_command_count", "blocked_command_count"):
            _validate_non_negative(name, getattr(self, name))
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_shell_execution", "ready_for_external_agent_execution", "ready_for_dominion_runtime", "ready_for_persistent_trace_write"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalRunPreview:
    run_preview_id: str
    cli_surface_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_shell_execution_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_external_agent_execution_guarantee: bool = True
    no_dominion_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        _require_non_blank("cli_surface_id", self.cli_surface_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class CLIPatchProposalNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_shell_execution: bool = True
    no_subprocess_execution: bool = True
    no_command_execution: bool = True
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_test_execution: bool = True
    no_dependency_install: bool = True
    no_reference_execution: bool = True
    no_reference_import: bool = True
    no_external_agent_execution: bool = True
    no_claude_code_invocation: bool = True
    no_codex_cli_invocation: bool = True
    no_dominion_runtime: bool = True
    no_infinite_agent_loop: bool = True
    no_provider_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_persistent_trace_write: bool = True
    no_ui_runtime: bool = True
    no_authority_grant: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0358ReadinessReport:
    report_id: str
    version: str
    summary: str = "v0.35.8 CLI Patch Proposal Surface readiness; not execution readiness."
    readiness_level: CLIPatchProposalReadinessLevel | str = CLIPatchProposalReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0359
    ready_for_v0359_consolidation: bool = True
    ready_for_cli_patch_proposal_surface: bool = True
    ready_for_bounded_cli_patch_proposal_preview: bool = True
    ready_for_cli_patch_intent_preview: bool = True
    ready_for_cli_patch_context_preview: bool = True
    ready_for_cli_patch_plan_preview: bool = True
    ready_for_cli_diff_proposal_preview: bool = True
    ready_for_cli_patch_risk_preview: bool = True
    ready_for_cli_patch_review_preview: bool = True
    ready_for_cli_patch_trace_preview: bool = True
    ready_for_execution: bool = False
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
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    completed_items: list[str] = field(default_factory=lambda: ["CLI patch proposal surface", "bounded preview dispatch", "unsafe command denial"])
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=lambda: ["v0.35.9 consolidation"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        _require_non_blank("summary", self.summary)
        CLIPatchProposalReadinessLevel(self.readiness_level)
        _validate_false(self, UNSAFE_CLI_PATCH_PROPOSAL_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata_safe(self.metadata)


def build_cli_patch_proposal_flags(flag_set_id: str = "cli_patch_proposal_flags:v0.35.8", **kwargs: Any) -> CLIPatchProposalFlagSet:
    return CLIPatchProposalFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0358_VERSION),
        cli_patch_proposal_surface_constructed=kwargs.pop("cli_patch_proposal_surface_constructed", True),
        cli_argument_parsing_enabled=kwargs.pop("cli_argument_parsing_enabled", True),
        bounded_preview_command_dispatch_enabled=kwargs.pop("bounded_preview_command_dispatch_enabled", True),
        denied_unsafe_command_handling_enabled=kwargs.pop("denied_unsafe_command_handling_enabled", True),
        ready_for_v0359_consolidation=kwargs.pop("ready_for_v0359_consolidation", True),
        ready_for_cli_patch_proposal_surface=kwargs.pop("ready_for_cli_patch_proposal_surface", True),
        ready_for_bounded_cli_patch_proposal_preview=kwargs.pop("ready_for_bounded_cli_patch_proposal_preview", True),
        ready_for_cli_patch_intent_preview=kwargs.pop("ready_for_cli_patch_intent_preview", True),
        ready_for_cli_patch_context_preview=kwargs.pop("ready_for_cli_patch_context_preview", True),
        ready_for_cli_patch_plan_preview=kwargs.pop("ready_for_cli_patch_plan_preview", True),
        ready_for_cli_diff_proposal_preview=kwargs.pop("ready_for_cli_diff_proposal_preview", True),
        ready_for_cli_patch_risk_preview=kwargs.pop("ready_for_cli_patch_risk_preview", True),
        ready_for_cli_patch_review_preview=kwargs.pop("ready_for_cli_patch_review_preview", True),
        ready_for_cli_patch_trace_preview=kwargs.pop("ready_for_cli_patch_trace_preview", True),
        **kwargs,
    )


def build_cli_patch_proposal_source_ref(source_ref_id: str = "cli_patch_source:v0.35.8", **kwargs: Any) -> CLIPatchProposalSourceRef:
    return CLIPatchProposalSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", CLIPatchProposalInputSourceKind.TEST_FIXTURE),
        source_id=kwargs.pop("source_id", "test_fixture"),
        source_summary=kwargs.pop("source_summary", "In-memory CLI patch proposal source metadata."),
        **kwargs,
    )


def build_cli_patch_proposal_argument_spec(argument_spec_id: str = "cli_patch_argument:v0.35.8", name: str = "--task", **kwargs: Any) -> CLIPatchProposalArgumentSpec:
    return CLIPatchProposalArgumentSpec(argument_spec_id=argument_spec_id, name=name, **kwargs)


def build_cli_patch_proposal_command_spec(command_spec_id: str = "cli_patch_command:v0.35.8", command_kind: CLIPatchProposalCommandKind | str = CLIPatchProposalCommandKind.PATCH_HELP, command_name: str = "patch-help", **kwargs: Any) -> CLIPatchProposalCommandSpec:
    kind = CLIPatchProposalCommandKind(command_kind)
    return CLIPatchProposalCommandSpec(
        command_spec_id=command_spec_id,
        command_kind=kind,
        command_mode=kwargs.pop("command_mode", _command_mode_for_kind(kind)),
        command_name=command_name,
        description=kwargs.pop("description", f"Bounded CLI patch proposal command: {command_name}"),
        **kwargs,
    )


def default_cli_patch_proposal_command_specs() -> list[CLIPatchProposalCommandSpec]:
    specs: list[CLIPatchProposalCommandSpec] = []
    command_names = [
        ("patch-help", CLIPatchProposalCommandKind.PATCH_HELP),
        ("patch-status", CLIPatchProposalCommandKind.PATCH_STATUS),
        ("patch-dry-run", CLIPatchProposalCommandKind.PATCH_DRY_RUN),
        ("patch-intent-preview", CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW),
        ("patch-scope-preview", CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW),
        ("patch-context-preview", CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW),
        ("patch-plan-preview", CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW),
        ("patch-diff-preview", CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW),
        ("patch-risk", CLIPatchProposalCommandKind.PATCH_RISK),
        ("patch-review", CLIPatchProposalCommandKind.PATCH_REVIEW),
        ("patch-trace-preview", CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW),
        ("patch-bundle-preview", CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW),
        ("no-op", CLIPatchProposalCommandKind.NO_OP),
    ]
    for command_name, kind in command_names:
        specs.append(
            build_cli_patch_proposal_command_spec(
                command_spec_id=f"cli_patch_command:{kind.value}:v0.35.8",
                command_kind=kind,
                command_name=command_name,
                allowed_decisions=[_decision_for_allowed_kind(kind)],
            )
        )
    for denied_name in sorted(DENIED_COMMAND_ALIASES):
        kind = _kind_from_command_token(denied_name)
        if kind == CLIPatchProposalCommandKind.UNKNOWN:
            continue
        specs.append(
            build_cli_patch_proposal_command_spec(
                command_spec_id=f"cli_patch_command:{denied_name}:denied:v0.35.8",
                command_kind=kind,
                command_name=denied_name,
                command_mode=CLIPatchProposalCommandMode.DENIED,
                allowed_decisions=[
                    CLIPatchProposalDecisionKind.DENY_PATCH_APPLY,
                    CLIPatchProposalDecisionKind.DENY_WRITE_EDIT,
                    CLIPatchProposalDecisionKind.DENY_TEST_EXECUTION,
                    CLIPatchProposalDecisionKind.DENY_DEPENDENCY_INSTALL,
                    CLIPatchProposalDecisionKind.DENY_REFERENCE_EXECUTION,
                    CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION,
                    CLIPatchProposalDecisionKind.DENY_DOMINION_RUNTIME,
                    CLIPatchProposalDecisionKind.DENY_SHELL_COMMAND,
                ],
                enabled=True,
            )
        )
    return specs


def default_cli_patch_proposal_surface_policy() -> CLIPatchProposalSurfacePolicy:
    return build_cli_patch_proposal_surface_policy(
        allowed_command_kinds=[
            CLIPatchProposalCommandKind.PATCH_HELP,
            CLIPatchProposalCommandKind.PATCH_STATUS,
            CLIPatchProposalCommandKind.PATCH_DRY_RUN,
            CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW,
            CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW,
            CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW,
            CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW,
            CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW,
            CLIPatchProposalCommandKind.PATCH_RISK,
            CLIPatchProposalCommandKind.PATCH_REVIEW,
            CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW,
            CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW,
            CLIPatchProposalCommandKind.NO_OP,
        ],
        blocked_command_kinds=[
            CLIPatchProposalCommandKind.UNKNOWN,
            CLIPatchProposalCommandKind.PATCH_APPLY_DENIED,
            CLIPatchProposalCommandKind.PATCH_WRITE_DENIED,
            CLIPatchProposalCommandKind.PATCH_EDIT_DENIED,
            CLIPatchProposalCommandKind.PATCH_TEST_DENIED,
            CLIPatchProposalCommandKind.PATCH_INSTALL_DENIED,
            CLIPatchProposalCommandKind.EXTERNAL_AGENT_DENIED,
            CLIPatchProposalCommandKind.DOMINION_DENIED,
        ],
    )


def build_cli_patch_proposal_surface_policy(policy_id: str = "cli_patch_policy:v0.35.8", **kwargs: Any) -> CLIPatchProposalSurfacePolicy:
    return CLIPatchProposalSurfacePolicy(
        policy_id=policy_id,
        version=kwargs.pop("version", V0358_VERSION),
        allowed_command_kinds=kwargs.pop("allowed_command_kinds", [CLIPatchProposalCommandKind.PATCH_HELP]),
        blocked_command_kinds=kwargs.pop("blocked_command_kinds", [CLIPatchProposalCommandKind.UNKNOWN]),
        allowed_output_formats=kwargs.pop("allowed_output_formats", [CLIPatchProposalOutputFormat.TEXT, CLIPatchProposalOutputFormat.MARKDOWN, CLIPatchProposalOutputFormat.JSON, CLIPatchProposalOutputFormat.STRUCTURED_ARTIFACT, CLIPatchProposalOutputFormat.DEBUG_SUMMARY]),
        prohibited_arg_patterns=kwargs.pop("prohibited_arg_patterns", list(DEFAULT_PROHIBITED_ARG_PATTERNS)),
        max_arg_chars=kwargs.pop("max_arg_chars", DEFAULT_MAX_CLI_ARG_CHARS),
        **kwargs,
    )


def build_cli_patch_proposal_surface(cli_surface_id: str = "cli_patch_surface:v0.35.8", **kwargs: Any) -> CLIPatchProposalSurface:
    return CLIPatchProposalSurface(
        cli_surface_id=cli_surface_id,
        version=kwargs.pop("version", V0358_VERSION),
        command_specs=kwargs.pop("command_specs", default_cli_patch_proposal_command_specs()),
        policy=kwargs.pop("policy", default_cli_patch_proposal_surface_policy()),
        flags=kwargs.pop("flags", build_cli_patch_proposal_flags()),
        status=kwargs.pop("status", CLIPatchProposalSurfaceStatus.INITIALIZED),
        readiness_level=kwargs.pop("readiness_level", CLIPatchProposalReadinessLevel.BOUNDED_CLI_PATCH_PROPOSAL_SURFACE_READY),
        summary=kwargs.pop("summary", "v0.35.8 bounded CLI patch proposal surface; not shell."),
        ready_for_cli_patch_proposal_surface=kwargs.pop("ready_for_cli_patch_proposal_surface", True),
        **kwargs,
    )


def build_default_cli_patch_proposal_surface() -> CLIPatchProposalSurface:
    return build_cli_patch_proposal_surface()


def build_cli_patch_proposal_invocation(invocation_id: str = "cli_patch_invocation:v0.35.8", **kwargs: Any) -> CLIPatchProposalInvocation:
    kind = CLIPatchProposalCommandKind(kwargs.pop("command_kind", CLIPatchProposalCommandKind.PATCH_HELP))
    return CLIPatchProposalInvocation(
        invocation_id=invocation_id,
        argv=kwargs.pop("argv", ["patch-help"]),
        command_kind=kind,
        command_mode=kwargs.pop("command_mode", _command_mode_for_kind(kind)),
        parsed_args=kwargs.pop("parsed_args", {}),
        requested_output_format=kwargs.pop("requested_output_format", CLIPatchProposalOutputFormat.TEXT),
        source_refs=kwargs.pop("source_refs", [build_cli_patch_proposal_source_ref(source_kind=CLIPatchProposalInputSourceKind.ARGV_LIST, source_id="argv", source_summary="CLI argv parsed in memory; not shell.")]),
        invocation_summary=kwargs.pop("invocation_summary", "Parsed CLI patch proposal invocation; not shell execution."),
        **kwargs,
    )


def build_cli_patch_proposal_invocation_decision(decision_id: str = "cli_patch_decision:v0.35.8", **kwargs: Any) -> CLIPatchProposalInvocationDecision:
    return CLIPatchProposalInvocationDecision(
        decision_id=decision_id,
        invocation_id=kwargs.pop("invocation_id", "cli_patch_invocation:v0.35.8"),
        decision_kind=kwargs.pop("decision_kind", CLIPatchProposalDecisionKind.ALLOW_HELP),
        reason=kwargs.pop("reason", "Bounded CLI patch proposal preview decision."),
        **kwargs,
    )


def build_cli_patch_proposal_denied_command(denied_command_id: str = "cli_patch_denied:v0.35.8", **kwargs: Any) -> CLIPatchProposalDeniedCommand:
    return CLIPatchProposalDeniedCommand(
        denied_command_id=denied_command_id,
        invocation_id=kwargs.pop("invocation_id", None),
        decision_id=kwargs.pop("decision_id", None),
        command_kind=kwargs.pop("command_kind", CLIPatchProposalCommandKind.UNKNOWN),
        risk_kinds=kwargs.pop("risk_kinds", [CLIPatchProposalRiskKind.UNKNOWN]),
        reason=kwargs.pop("reason", "Command denied by v0.35.8 CLI patch proposal surface."),
        **kwargs,
    )


def build_cli_patch_proposal_runtime_context(runtime_context_id: str = "cli_patch_runtime_context:v0.35.8", **kwargs: Any) -> CLIPatchProposalRuntimeContext:
    return CLIPatchProposalRuntimeContext(runtime_context_id=runtime_context_id, **kwargs)


def build_cli_patch_proposal_command_result(command_result_id: str = "cli_patch_result:v0.35.8", **kwargs: Any) -> CLIPatchProposalCommandResult:
    return CLIPatchProposalCommandResult(
        command_result_id=command_result_id,
        invocation_id=kwargs.pop("invocation_id", "cli_patch_invocation:v0.35.8"),
        decision_id=kwargs.pop("decision_id", "cli_patch_decision:v0.35.8"),
        command_kind=kwargs.pop("command_kind", CLIPatchProposalCommandKind.PATCH_HELP),
        status=kwargs.pop("status", CLIPatchProposalSurfaceStatus.COMPLETED),
        **kwargs,
    )


def build_cli_patch_proposal_run_output(run_output_id: str = "cli_patch_run_output:v0.35.8", **kwargs: Any) -> CLIPatchProposalRunOutput:
    return CLIPatchProposalRunOutput(
        run_output_id=run_output_id,
        invocation_id=kwargs.pop("invocation_id", "cli_patch_invocation:v0.35.8"),
        command_result=kwargs.pop("command_result", None),
        denied_command=kwargs.pop("denied_command", None),
        rendered_output=kwargs.pop("rendered_output", "Bounded CLI patch proposal output."),
        output_format=kwargs.pop("output_format", CLIPatchProposalOutputFormat.TEXT),
        status=kwargs.pop("status", CLIPatchProposalSurfaceStatus.COMPLETED),
        summary=kwargs.pop("summary", "Bounded CLI patch proposal output; not file write."),
        **kwargs,
    )


def build_cli_patch_proposal_run_report(run_report_id: str = "cli_patch_run_report:v0.35.8", **kwargs: Any) -> CLIPatchProposalRunReport:
    return CLIPatchProposalRunReport(
        run_report_id=run_report_id,
        version=kwargs.pop("version", V0358_VERSION),
        run_output_id=kwargs.pop("run_output_id", "cli_patch_run_output:v0.35.8"),
        invocation_id=kwargs.pop("invocation_id", "cli_patch_invocation:v0.35.8"),
        status=kwargs.pop("status", CLIPatchProposalSurfaceStatus.COMPLETED),
        bounded_preview_count=kwargs.pop("bounded_preview_count", 1),
        denied_command_count=kwargs.pop("denied_command_count", 0),
        blocked_command_count=kwargs.pop("blocked_command_count", 0),
        summary=kwargs.pop("summary", "CLI patch proposal run report; not execution."),
        **kwargs,
    )


def build_cli_patch_proposal_run_preview(run_preview_id: str = "cli_patch_run_preview:v0.35.8", **kwargs: Any) -> CLIPatchProposalRunPreview:
    return CLIPatchProposalRunPreview(
        run_preview_id=run_preview_id,
        cli_surface_id=kwargs.pop("cli_surface_id", "cli_patch_surface:v0.35.8"),
        planned_steps=kwargs.pop("planned_steps", ["parse argv", "evaluate policy", "return bounded preview"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["CLIPatchProposalInvocation", "CLIPatchProposalRunOutput"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["shell execution", "patch application", "file write", "external agent execution"]),
        **kwargs,
    )


def build_cli_patch_proposal_no_external_side_effect_guarantee(guarantee_id: str = "cli_patch_no_external_side_effect:v0.35.8", **kwargs: Any) -> CLIPatchProposalNoExternalSideEffectGuarantee:
    return CLIPatchProposalNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0358_VERSION), **kwargs)


def build_v0358_readiness_report(report_id: str = "v0358_readiness_report", **kwargs: Any) -> V0358ReadinessReport:
    return V0358ReadinessReport(report_id=report_id, version=kwargs.pop("version", V0358_VERSION), **kwargs)


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


def parse_cli_patch_proposal_invocation(argv: list[str], surface: CLIPatchProposalSurface | None = None) -> CLIPatchProposalInvocation:
    if not isinstance(argv, list) or not all(isinstance(arg, str) for arg in argv):
        raise TypeError("argv must be list[str]")
    active_surface = surface or build_default_cli_patch_proposal_surface()
    safe_argv = [arg[: active_surface.policy.max_arg_chars] for arg in argv]
    tokens = list(safe_argv)
    if tokens and tokens[0] in {"patch", "patch-proposal"}:
        tokens = tokens[1:]
    command_token = tokens[0] if tokens else "patch-help"
    parsed_args = _parse_option_pairs(tokens[1:] if tokens else [], active_surface.policy.max_arg_chars)
    parsed_args["command_token"] = command_token
    requested_format = parsed_args.get("format", CLIPatchProposalOutputFormat.TEXT)
    try:
        output_format = CLIPatchProposalOutputFormat(requested_format)
    except ValueError:
        output_format = CLIPatchProposalOutputFormat.TEXT
    return build_cli_patch_proposal_invocation(
        invocation_id=f"cli_patch_invocation:v0.35.8:{command_token.replace('-', '_') or 'patch_help'}",
        argv=safe_argv,
        command_kind=_kind_from_command_token(command_token),
        parsed_args=parsed_args,
        requested_output_format=output_format,
    )


def _risks_for_denied_kind(kind: CLIPatchProposalCommandKind) -> list[CLIPatchProposalRiskKind]:
    if kind == CLIPatchProposalCommandKind.PATCH_APPLY_DENIED:
        return [CLIPatchProposalRiskKind.PATCH_APPLY_RISK]
    if kind in {CLIPatchProposalCommandKind.PATCH_WRITE_DENIED, CLIPatchProposalCommandKind.PATCH_EDIT_DENIED}:
        return [CLIPatchProposalRiskKind.WORKSPACE_WRITE_RISK, CLIPatchProposalRiskKind.CODE_EDIT_RISK]
    if kind == CLIPatchProposalCommandKind.PATCH_TEST_DENIED:
        return [CLIPatchProposalRiskKind.TEST_EXECUTION_RISK]
    if kind == CLIPatchProposalCommandKind.PATCH_INSTALL_DENIED:
        return [CLIPatchProposalRiskKind.DEPENDENCY_INSTALL_RISK]
    if kind == CLIPatchProposalCommandKind.EXTERNAL_AGENT_DENIED:
        return [CLIPatchProposalRiskKind.EXTERNAL_AGENT_EXECUTION_RISK]
    if kind == CLIPatchProposalCommandKind.DOMINION_DENIED:
        return [CLIPatchProposalRiskKind.DOMINION_RUNTIME_RISK, CLIPatchProposalRiskKind.INFINITE_AGENT_LOOP_RISK]
    return [CLIPatchProposalRiskKind.UNKNOWN]


def _decision_for_denied_kind(kind: CLIPatchProposalCommandKind) -> CLIPatchProposalDecisionKind:
    if kind == CLIPatchProposalCommandKind.PATCH_APPLY_DENIED:
        return CLIPatchProposalDecisionKind.DENY_PATCH_APPLY
    if kind in {CLIPatchProposalCommandKind.PATCH_WRITE_DENIED, CLIPatchProposalCommandKind.PATCH_EDIT_DENIED}:
        return CLIPatchProposalDecisionKind.DENY_WRITE_EDIT
    if kind == CLIPatchProposalCommandKind.PATCH_TEST_DENIED:
        return CLIPatchProposalDecisionKind.DENY_TEST_EXECUTION
    if kind == CLIPatchProposalCommandKind.PATCH_INSTALL_DENIED:
        return CLIPatchProposalDecisionKind.DENY_DEPENDENCY_INSTALL
    if kind == CLIPatchProposalCommandKind.EXTERNAL_AGENT_DENIED:
        return CLIPatchProposalDecisionKind.DENY_EXTERNAL_AGENT_EXECUTION
    if kind == CLIPatchProposalCommandKind.DOMINION_DENIED:
        return CLIPatchProposalDecisionKind.DENY_DOMINION_RUNTIME
    return CLIPatchProposalDecisionKind.BLOCK


def _unsafe_arg_risks(invocation: CLIPatchProposalInvocation, surface: CLIPatchProposalSurface) -> list[CLIPatchProposalRiskKind]:
    joined = " ".join(invocation.argv).lower()
    risks: list[CLIPatchProposalRiskKind] = []
    if _contains_prohibited_text(joined, surface.policy.prohibited_arg_patterns):
        risks.append(CLIPatchProposalRiskKind.SHELL_INJECTION_RISK)
    risk_words = {
        "shell": CLIPatchProposalRiskKind.COMMAND_EXECUTION_RISK,
        "provider": CLIPatchProposalRiskKind.DIRECT_PROVIDER_INVOCATION_RISK,
        "network": CLIPatchProposalRiskKind.DIRECT_NETWORK_ACCESS_RISK,
        "credential": CLIPatchProposalRiskKind.CREDENTIAL_ACCESS_RISK,
        "secret": CLIPatchProposalRiskKind.SECRET_READ_RISK,
        "token": CLIPatchProposalRiskKind.SECRET_READ_RISK,
        "opencode": CLIPatchProposalRiskKind.REFERENCE_EXECUTION_RISK,
        "hermes": CLIPatchProposalRiskKind.REFERENCE_EXECUTION_RISK,
        "openclaw": CLIPatchProposalRiskKind.REFERENCE_EXECUTION_RISK,
        "claude": CLIPatchProposalRiskKind.CLAUDE_CODE_INVOCATION_RISK,
        "codex": CLIPatchProposalRiskKind.CODEX_CLI_INVOCATION_RISK,
        "dominion": CLIPatchProposalRiskKind.DOMINION_RUNTIME_RISK,
        "infinite-loop": CLIPatchProposalRiskKind.INFINITE_AGENT_LOOP_RISK,
    }
    for word, risk in risk_words.items():
        if word in joined:
            risks.append(risk)
    for arg in invocation.argv:
        if len(arg) > surface.policy.max_arg_chars:
            risks.append(CLIPatchProposalRiskKind.SHELL_INJECTION_RISK)
    return list(dict.fromkeys(risks))


def evaluate_cli_patch_proposal_invocation(invocation: CLIPatchProposalInvocation, surface: CLIPatchProposalSurface, runtime_context: CLIPatchProposalRuntimeContext | None = None) -> CLIPatchProposalInvocationDecision:
    if not isinstance(invocation, CLIPatchProposalInvocation):
        raise TypeError("invocation must be CLIPatchProposalInvocation")
    if not isinstance(surface, CLIPatchProposalSurface):
        raise TypeError("surface must be CLIPatchProposalSurface")
    if runtime_context is not None and not isinstance(runtime_context, CLIPatchProposalRuntimeContext):
        raise TypeError("runtime_context must be CLIPatchProposalRuntimeContext")
    kind = CLIPatchProposalCommandKind(invocation.command_kind)
    if kind in surface.policy.blocked_command_kinds and kind != CLIPatchProposalCommandKind.UNKNOWN:
        return build_cli_patch_proposal_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=_decision_for_denied_kind(kind),
            reason="Unsafe CLI patch proposal command denied without execution.",
            risk_kinds=_risks_for_denied_kind(kind),
            allowed_command_kind=None,
        )
    risks = _unsafe_arg_risks(invocation, surface)
    if kind == CLIPatchProposalCommandKind.UNKNOWN or risks:
        decision_kind = CLIPatchProposalDecisionKind.DENY_SHELL_COMMAND if risks else CLIPatchProposalDecisionKind.BLOCK
        return build_cli_patch_proposal_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=decision_kind,
            reason="Unknown, shell-like, reference, external-agent, Dominion, credential, or otherwise unsafe CLI command was denied.",
            risk_kinds=risks or [CLIPatchProposalRiskKind.UNKNOWN],
            allowed_command_kind=None,
        )
    if kind not in surface.policy.allowed_command_kinds:
        return build_cli_patch_proposal_invocation_decision(
            decision_id=f"{invocation.invocation_id}:decision",
            invocation_id=invocation.invocation_id,
            decision_kind=CLIPatchProposalDecisionKind.DENY,
            reason="Command is not enabled by v0.35.8 CLI patch proposal policy.",
            risk_kinds=[CLIPatchProposalRiskKind.UNKNOWN],
            allowed_command_kind=None,
        )
    decision_kind = _decision_for_allowed_kind(kind)
    return build_cli_patch_proposal_invocation_decision(
        decision_id=f"{invocation.invocation_id}:decision",
        invocation_id=invocation.invocation_id,
        decision_kind=decision_kind,
        reason="Bounded in-memory CLI patch proposal preview allowed; no shell/apply/write execution.",
        allowed_command_kind=kind,
        bounded_preview_allowed=kind != CLIPatchProposalCommandKind.NO_OP,
    )


def _context_ref(runtime_context: CLIPatchProposalRuntimeContext | None, metadata_key: str, fallback: str) -> str:
    if runtime_context and isinstance(runtime_context.metadata.get(metadata_key), str):
        return runtime_context.metadata[metadata_key]
    return fallback


def _preview_result_for_kind(invocation: CLIPatchProposalInvocation, decision: CLIPatchProposalInvocationDecision, runtime_context: CLIPatchProposalRuntimeContext | None) -> CLIPatchProposalCommandResult:
    kind = CLIPatchProposalCommandKind(invocation.command_kind)
    structured: dict[str, Any] = {
        "command": kind.value,
        "bounded_preview": True,
        "ready_for_execution": False,
        "patch_application_allowed": False,
    }
    refs: dict[str, str | None] = {
        "patch_intent_ref": None,
        "patch_context_snapshot_ref": None,
        "patch_plan_ref": None,
        "diff_envelope_ref": None,
        "risk_report_ref": None,
        "review_packet_ref": None,
        "trace_packet_ref": None,
    }
    summary = "Bounded CLI patch proposal preview."
    if kind in {CLIPatchProposalCommandKind.PATCH_HELP, CLIPatchProposalCommandKind.PATCH_STATUS, CLIPatchProposalCommandKind.PATCH_DRY_RUN}:
        structured["safe_commands"] = sorted(SAFE_COMMAND_NAMES)
        structured["denied_commands"] = sorted(DENIED_COMMAND_ALIASES)
        summary = "CLI patch proposal surface status/help/dry-run metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_INTENT_PREVIEW, CLIPatchProposalCommandKind.PATCH_SCOPE_PREVIEW, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        bundle = build_patch_intent_scope_bundle()
        refs["patch_intent_ref"] = _context_ref(runtime_context, "patch_intent_ref", bundle.bundle_id)
        structured["intent_scope_bundle_id"] = refs["patch_intent_ref"]
        summary = "Patch intent/scope preview metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_CONTEXT_PREVIEW, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        snapshot = build_patch_context_snapshot()
        refs["patch_context_snapshot_ref"] = _context_ref(runtime_context, "patch_context_snapshot_ref", snapshot.context_snapshot_id)
        structured["context_snapshot_id"] = refs["patch_context_snapshot_ref"]
        summary = "Patch context snapshot preview metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_PLAN_PREVIEW, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        plan = build_patch_plan()
        refs["patch_plan_ref"] = _context_ref(runtime_context, "patch_plan_ref", plan.patch_plan_id)
        structured["patch_plan_id"] = refs["patch_plan_ref"]
        summary = "Patch plan preview metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_DIFF_PREVIEW, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        envelope = build_diff_proposal_envelope()
        refs["diff_envelope_ref"] = _context_ref(runtime_context, "diff_envelope_ref", envelope.diff_envelope_id)
        structured["diff_envelope_id"] = refs["diff_envelope_ref"]
        summary = "Diff proposal envelope preview metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_RISK, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        risk = build_patch_proposal_risk_report()
        refs["risk_report_ref"] = _context_ref(runtime_context, "risk_report_ref", risk.proposal_risk_report_id)
        structured["risk_report_id"] = refs["risk_report_ref"]
        summary = "Patch risk report preview metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_REVIEW, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        review = build_patch_review_packet()
        refs["review_packet_ref"] = _context_ref(runtime_context, "review_packet_ref", review.review_packet_id)
        structured["review_packet_id"] = refs["review_packet_ref"]
        summary = "Patch review packet preview metadata only."
    if kind in {CLIPatchProposalCommandKind.PATCH_TRACE_PREVIEW, CLIPatchProposalCommandKind.PATCH_BUNDLE_PREVIEW}:
        trace = build_patch_proposal_trace_packet()
        refs["trace_packet_ref"] = _context_ref(runtime_context, "trace_packet_ref", trace.trace_packet_id)
        structured["trace_packet_id"] = refs["trace_packet_ref"]
        summary = "Patch proposal trace packet preview metadata only; no trace persistence."
    if kind == CLIPatchProposalCommandKind.NO_OP:
        structured["no_op"] = True
        summary = "No-op command completed without side effects."
    text, redacted, truncated = _bounded_text(structured)
    return build_cli_patch_proposal_command_result(
        command_result_id=f"{invocation.invocation_id}:result",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=kind,
        status=CLIPatchProposalSurfaceStatus.NO_OP if kind == CLIPatchProposalCommandKind.NO_OP else CLIPatchProposalSurfaceStatus.COMPLETED,
        structured_result=structured,
        text_summary=summary,
        redacted=redacted,
        truncated=truncated,
        **refs,
        metadata={"render_preview": text},
    )


def _run_output_from_denial(invocation: CLIPatchProposalInvocation, decision: CLIPatchProposalInvocationDecision) -> CLIPatchProposalRunOutput:
    denied = build_cli_patch_proposal_denied_command(
        denied_command_id=f"{invocation.invocation_id}:denied",
        invocation_id=invocation.invocation_id,
        decision_id=decision.decision_id,
        command_kind=invocation.command_kind,
        risk_kinds=list(decision.risk_kinds),
        reason=decision.reason,
    )
    rendered, _, _ = _bounded_text({"denied": denied.reason, "risk_kinds": [str(risk) for risk in denied.risk_kinds], "safe_alternatives": denied.safe_alternatives})
    return build_cli_patch_proposal_run_output(
        run_output_id=f"{invocation.invocation_id}:run_output",
        invocation_id=invocation.invocation_id,
        command_result=None,
        denied_command=denied,
        rendered_output=rendered,
        output_format=invocation.requested_output_format,
        status=CLIPatchProposalSurfaceStatus.BLOCKED,
        summary="CLI patch proposal command denied or blocked safely.",
    )


def run_cli_patch_proposal_command(invocation: CLIPatchProposalInvocation, surface: CLIPatchProposalSurface, runtime_context: CLIPatchProposalRuntimeContext | None = None) -> CLIPatchProposalRunOutput:
    decision = evaluate_cli_patch_proposal_invocation(invocation, surface, runtime_context)
    if CLIPatchProposalDecisionKind(decision.decision_kind) not in {
        CLIPatchProposalDecisionKind.ALLOW_HELP,
        CLIPatchProposalDecisionKind.ALLOW_STATUS,
        CLIPatchProposalDecisionKind.ALLOW_DRY_RUN,
        CLIPatchProposalDecisionKind.ALLOW_INTENT_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_SCOPE_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_CONTEXT_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_PLAN_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_DIFF_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_RISK_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_REVIEW_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_TRACE_PREVIEW,
        CLIPatchProposalDecisionKind.ALLOW_BUNDLE_PREVIEW,
        CLIPatchProposalDecisionKind.NO_OP,
    }:
        return _run_output_from_denial(invocation, decision)
    result = _preview_result_for_kind(invocation, decision, runtime_context)
    rendered = render_cli_patch_proposal_output(
        build_cli_patch_proposal_run_output(
            run_output_id=f"{invocation.invocation_id}:run_output:pre_render",
            invocation_id=invocation.invocation_id,
            command_result=result,
            denied_command=None,
            rendered_output=result.metadata.get("render_preview", result.text_summary),
            output_format=invocation.requested_output_format,
            status=result.status,
            summary=result.text_summary,
        ),
        invocation.requested_output_format,
    )
    rendered, redacted, truncated = _bounded_text(rendered)
    safe_result = build_cli_patch_proposal_command_result(**{**result.__dict__, "redacted": result.redacted or redacted, "truncated": result.truncated or truncated})
    return build_cli_patch_proposal_run_output(
        run_output_id=f"{invocation.invocation_id}:run_output",
        invocation_id=invocation.invocation_id,
        command_result=safe_result,
        denied_command=None,
        rendered_output=rendered,
        output_format=invocation.requested_output_format,
        status=result.status,
        summary=result.text_summary,
    )


def render_cli_patch_proposal_output(output: CLIPatchProposalRunOutput, output_format: CLIPatchProposalOutputFormat | str | None = None) -> str:
    fmt = CLIPatchProposalOutputFormat(output_format or output.output_format)
    payload = {
        "status": str(output.status),
        "summary": output.summary,
        "ready_for_execution": output.ready_for_execution,
        "command_result": output.command_result.structured_result if output.command_result else None,
        "denied_command": output.denied_command.reason if output.denied_command else None,
    }
    if fmt == CLIPatchProposalOutputFormat.NO_OUTPUT:
        return "no output requested"
    if fmt in {CLIPatchProposalOutputFormat.JSON, CLIPatchProposalOutputFormat.STRUCTURED_ARTIFACT, CLIPatchProposalOutputFormat.DEBUG_SUMMARY}:
        return _bounded_text(payload)[0]
    if fmt == CLIPatchProposalOutputFormat.MARKDOWN:
        return _bounded_text(f"**{payload['status']}**\n\n{payload['summary']}\n\n`ready_for_execution=False`")[0]
    return _bounded_text(output.rendered_output or output.summary)[0]


def cli_patch_proposal_flags_preserve_unsafe_false(flags: CLIPatchProposalFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_CLI_PATCH_PROPOSAL_FLAG_NAMES)


def cli_patch_proposal_invocation_is_not_shell(invocation: CLIPatchProposalInvocation) -> bool:
    return isinstance(invocation.argv, list) and invocation.metadata.get("passed_to_shell") is not True


def cli_patch_proposal_decision_blocks_apply(decision: CLIPatchProposalInvocationDecision) -> bool:
    return not any(getattr(decision, name) for name in ("patch_application_allowed", "workspace_write_allowed", "code_edit_allowed", "apply_patch_allowed", "git_apply_allowed"))


def cli_patch_proposal_decision_blocks_external_agent(decision: CLIPatchProposalInvocationDecision) -> bool:
    return not any(getattr(decision, name) for name in ("external_agent_execution_allowed", "claude_code_invocation_allowed", "codex_cli_invocation_allowed", "dominion_runtime_allowed", "infinite_agent_loop_allowed"))


def cli_patch_proposal_surface_is_not_shell(surface: CLIPatchProposalSurface) -> bool:
    return surface.ready_for_execution is False and surface.policy.allow_shell is False and surface.policy.allow_subprocess is False and surface.policy.allow_command_execution is False


def v0358_readiness_report_is_not_execution_ready(report: V0358ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_CLI_PATCH_PROPOSAL_FLAG_NAMES)
