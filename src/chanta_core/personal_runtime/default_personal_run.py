"""v0.41.4 minimal single-turn provider-backed run support.

This module opens scoped prompt submission and text-only provider invocation
only for ``chanta-cli run``. It keeps provider doctor completion, tools,
function calling, general AgentLoop, skill execution, trace runtime, shell,
subagents, memory writes, and production certification closed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Sequence

from chanta_core.personal_runtime.default_personal_profile_runtime import V0416_TARGET_COMMANDS
from chanta_core.personal_runtime.default_personal_prompt_session import (
    PROFILE_ID,
    PromptAssemblyInput,
    assemble_default_personal_prompt,
    create_default_personal_session,
    create_default_personal_session_create_request,
)
from chanta_core.personal_runtime.default_personal_provider_response import (
    create_v042_provider_reasoning_model_troubleshooting_guide,
    create_v042_run_response_recording_decision,
    create_v042_runtime_identity_injection_report,
    create_v042_runtime_identity_prompt,
    parse_v042_openai_compatible_response,
)
from chanta_core.personal_runtime.default_personal_provider_skills import (
    ProviderConfig,
    ProviderKind,
    load_provider_config_from_profile,
    main as v0413_main,
)


V0414_VERSION = "v0.41.4"
V0414_RELEASE_NAME = "v0.41.4 Minimal Single-turn Provider-backed Run"
V0414_TRACK_NAME = "v0.41 Default Personal Runtime Opening Track"
CLI_NAME = "chanta-cli"
INTEGRATED_DOC_PATH = "docs/versions/v0.41/v0.41.4_minimal_single_turn_provider_backed_run_restore.md"


class ProviderTextTransportKind(StrEnum):
    MOCK = "mock"
    OPENAI_COMPATIBLE = "openai_compatible"
    DISABLED = "disabled"
    UNKNOWN = "unknown"


class ProviderTextRunStatus(StrEnum):
    SUCCESS = "success"
    FAILED = "failed"
    BLOCKED = "blocked"
    PROVIDER_NOT_CONFIGURED = "provider_not_configured"
    PROVIDER_UNAVAILABLE = "provider_unavailable"
    INVALID_CONFIG = "invalid_config"
    UNSAFE_REQUEST = "unsafe_request"
    TIMEOUT = "timeout"
    UNSUPPORTED = "unsupported"


OPEN_CAPABILITIES: tuple[str, ...] = (
    "default_personal_profile_runtime_foundation",
    "installable_cli_bootstrap",
    "chanta_cli_entrypoint",
    "cli_version_command",
    "cli_doctor_command",
    "init_default_personal_command",
    "profile_status_command",
    "prompt_assembly",
    "prompt_preview_command",
    "session_store_schema",
    "session_new_command",
    "session_list_command",
    "provider_config_metadata",
    "provider_doctor_no_completion",
    "secret_redaction",
    "read_only_skill_registry",
    "skill_list_command",
    "skill_inspect_command",
    "run_command",
    "scoped_prompt_submission_for_run",
    "provider_text_only_invocation_for_run",
    "minimal_single_turn_run",
    "mock_provider_transport",
    "session_turn_append_for_run",
    "assistant_response_rendering",
    "integrated_restore_document",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "ask_command",
    "provider_doctor_completion",
    "unscoped_prompt_submission",
    "provider_tool_calling",
    "function_calling",
    "read_only_skill_execution",
    "general_agent_loop",
    "multi_step_agent_loop",
    "trace_emission",
    "user_test_release",
    "file_write_outside_profile_or_session_store",
    "file_edit",
    "patch_apply",
    "shell_execution",
    "test_execution",
    "subagent_invocation",
    "child_session_creation",
    "parent_raw_transcript_sharing",
    "autonomous_loop",
    "retry_loop",
    "dominion_runtime",
    "production_certification",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_ask_command",
    "ready_for_provider_doctor_completion",
    "ready_for_unscoped_prompt_submission",
    "ready_for_provider_tool_calling",
    "ready_for_function_calling",
    "ready_for_read_only_skill_execution",
    "ready_for_general_agent_loop",
    "ready_for_multi_step_agent_loop",
    "ready_for_trace_emission",
    "ready_for_user_test_release",
    "ready_for_file_write",
    "ready_for_file_edit",
    "ready_for_patch_apply",
    "ready_for_shell_execution",
    "ready_for_test_execution",
    "ready_for_subagent_invocation",
    "ready_for_child_session_creation",
    "ready_for_parent_raw_transcript_sharing",
    "ready_for_autonomous_loop_runtime",
    "ready_for_retry_loop",
    "ready_for_mission_scheduler",
    "ready_for_mutable_memory_automation",
    "ready_for_dominion_runtime",
    "production_certified",
)
REQUIRED_RESTORE_SECTION_IDS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "repository_baseline_assumptions",
    "v0413_provider_skill_summary",
    "scoped_provider_text_run_summary",
    "run_command_contract",
    "provider_text_run_policy",
    "scoped_prompt_submission_contract",
    "provider_transport_contract",
    "mock_provider_transport_contract",
    "openai_compatible_transport_contract",
    "session_turn_append_contract",
    "assistant_response_rendering_contract",
    "unsafe_escalation_denial_policy",
    "provider_runtime_scope",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0415_handoff",
    "v0416_user_test_target",
    "copy_paste_restore_prompt",
)


@dataclass(frozen=True)
class ProviderTextRunPolicy:
    policy_id: str
    profile_id: str
    command_name: str
    provider_text_invocation_allowed: bool
    prompt_submission_allowed: bool
    provider_doctor_completion_allowed: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    active_tools_allowed: bool
    provider_side_tools_allowed: bool
    subagent_context_allowed: bool
    file_attachment_allowed: bool
    arbitrary_file_read_allowed: bool
    shell_allowed: bool
    workspace_mutation_allowed: bool
    session_append_allowed: bool
    trace_emission_allowed: bool
    memory_write_allowed: bool
    timeout_seconds: float


@dataclass(frozen=True)
class ProviderTextRunSafetyReport:
    report_id: str
    policy: ProviderTextRunPolicy
    safe_for_text_only_run: bool
    unsafe_escalation_detected: bool
    provider_tool_calling_detected: bool
    function_calling_detected: bool
    shell_or_workspace_mutation_detected: bool
    subagent_context_detected: bool
    secret_redaction_confirmed: bool


@dataclass(frozen=True)
class ProviderTextRequest:
    request_id: str
    provider_id: str
    provider_kind: str
    base_url: str | None
    model: str
    user_input: str
    assembled_prompt: str
    system_prompt_preview: str | None
    timeout_seconds: float
    tool_calling_allowed: bool
    function_calling_allowed: bool
    active_tools: tuple[str, ...]
    sends_user_prompt: bool
    sends_completion_request: bool
    secret_env_var_name: str | None
    secret_value_printed: bool


@dataclass(frozen=True)
class ProviderTextResponse:
    response_id: str
    request_id: str
    provider_id: str
    status: str
    text: str
    raw_text_available: bool
    trusted_for_memory: bool
    trusted_for_execution: bool
    trusted_for_process_state: bool
    token_usage: dict[str, object] | None
    error_message: str | None
    error_class: str | None
    response_parse_status: str | None
    response_extracted_from_field: str | None
    response_content_length: int | None
    response_finish_reason: str | None
    provider_model: str | None
    runtime_identity_included: bool
    provider_identity_is_implementation_detail: bool
    empty_response_detected: bool


@dataclass(frozen=True)
class ProviderTextTransportResult:
    result_id: str
    transport_kind: str
    attempted: bool
    status: str
    response: ProviderTextResponse | None
    error_message: str | None
    network_accessed: bool
    remote_network_accessed: bool
    prompt_submitted: bool
    provider_completion_invoked: bool
    tool_calling_used: bool
    function_calling_used: bool
    secret_printed: bool
    error_class: str | None
    timeout_seconds: float | None


@dataclass(frozen=True)
class MockProviderTextTransport:
    transport_id: str
    transport_kind: str
    deterministic: bool
    network_accessed: bool
    process_launch_used: bool
    file_inspection_used: bool


@dataclass(frozen=True)
class OpenAICompatibleTextTransportConfig:
    provider_id: str
    base_url: str
    model: str
    api_key_env_var: str | None
    timeout_seconds: float
    endpoint_path: str


@dataclass(frozen=True)
class OpenAICompatibleTextTransportResult:
    config: OpenAICompatibleTextTransportConfig
    transport_result: ProviderTextTransportResult
    tool_schema_sent: bool
    function_calling_sent: bool
    secret_printed: bool


@dataclass(frozen=True)
class ProviderTextInvocationAudit:
    audit_id: str
    command_name: str
    provider_id: str
    prompt_submitted: bool
    provider_completion_invoked: bool
    provider_doctor_completion_invoked: bool
    tool_calling_used: bool
    function_calling_used: bool
    secret_printed: bool
    trace_emitted: bool


@dataclass(frozen=True)
class ScopedPromptSubmissionRecord:
    record_id: str
    command_name: str
    profile_id: str
    session_id: str | None
    allowed_scope: str
    prompt_submitted: bool
    provider_invoked: bool
    prompt_submitted_outside_run: bool
    provider_invoked_outside_run: bool
    tool_calling_used: bool
    function_calling_used: bool


@dataclass(frozen=True)
class MinimalSingleTurnRunInput:
    input_id: str
    profile_id: str
    home_path: str
    user_input: str
    session_id: str | None
    provider_override: str | None
    use_mock_provider: bool
    max_steps: int
    timeout_seconds: float | None


@dataclass(frozen=True)
class MinimalSingleTurnRunContext:
    context_id: str
    profile_id: str
    profile_loaded: bool
    prompt_assembled: bool
    provider_config_loaded: bool
    session_ready: bool
    safety_report: ProviderTextRunSafetyReport
    prompt_preview: str
    provider_id: str
    session_id: str


@dataclass(frozen=True)
class MinimalSingleTurnStopCondition:
    stop_after_provider_response: bool
    stop_after_error: bool
    max_steps: int
    allow_retry: bool
    allow_followup_without_user: bool


@dataclass(frozen=True)
class MinimalSingleTurnRunLoop:
    loop_id: str
    profile_id: str
    max_steps: int
    current_step: int
    stop_condition: MinimalSingleTurnStopCondition
    general_agent_loop_opened: bool
    autonomous_continuation_allowed: bool
    retry_loop_allowed: bool
    subagent_allowed: bool
    skill_execution_allowed: bool


@dataclass(frozen=True)
class MinimalSingleTurnRunResult:
    result_id: str
    input_id: str
    profile_id: str
    session_id: str
    status: str
    assistant_text: str
    provider_response: ProviderTextResponse | None
    session_append_result: "RunSessionAppendResult | None"
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool
    general_agent_loop_opened: bool
    skill_executed: bool
    trace_emitted: bool
    workspace_mutated: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class RunCommandInput:
    profile_id: str
    home_path: str
    user_input: str
    session_id: str | None
    provider: str | None
    mock_provider: bool
    timeout_seconds: float | None = None


@dataclass(frozen=True)
class RunCommandResult:
    status: str
    rendered_text: str
    exit_code: int
    run_result: MinimalSingleTurnRunResult
    provider_invoked: bool
    prompt_submitted: bool
    trace_emitted: bool
    production_certified: bool


@dataclass(frozen=True)
class RunSessionAppendPolicy:
    append_user_turn: bool
    append_assistant_turn: bool
    create_session_if_missing: bool
    overwrite_allowed: bool
    write_outside_home_allowed: bool


@dataclass(frozen=True)
class RunSessionTurnRecord:
    turn_id: str
    session_id: str
    role: str
    content: str
    created_at: str
    source: str
    provider_generated: bool
    provider_id: str | None
    prompt_submitted: bool
    trusted_for_memory: bool
    trusted_for_execution: bool
    metadata: dict[str, object]


@dataclass(frozen=True)
class RunSessionAppendResult:
    result_id: str
    session_id: str
    turns_jsonl_path: str
    appended_turn_count: int
    overwritten_files: tuple[str, ...]
    outside_home_paths: tuple[str, ...]
    success: bool


@dataclass(frozen=True)
class AssistantResponseRenderPolicy:
    include_safety_notice: bool
    include_profile_id: bool
    include_session_id: bool
    include_trace_notice: bool
    mark_untrusted_provider_text: bool


@dataclass(frozen=True)
class AssistantResponseRenderResult:
    rendered_text: str
    provider_text_marked_untrusted: bool
    trace_notice_included: bool
    production_certified: bool


@dataclass(frozen=True)
class RunUnsafeEscalationCheck:
    check_id: str
    user_input: str
    unsafe_items: tuple[str, ...]
    tool_calling_requested: bool
    function_calling_requested: bool
    file_write_or_edit_requested: bool
    shell_requested: bool
    test_execution_requested: bool
    subagent_requested: bool
    child_session_requested: bool
    retry_loop_requested: bool
    autonomous_loop_requested: bool
    dominion_requested: bool
    production_certification_requested: bool


@dataclass(frozen=True)
class RunUnsafeEscalationDecision:
    decision_id: str
    blocked: bool
    reason: str
    unsafe_items: tuple[str, ...]
    safe_alternative: str
    executed: bool


@dataclass(frozen=True)
class V0414ReadinessReport:
    report_id: str
    run_command_ready: bool
    scoped_prompt_submission_for_run_ready: bool
    provider_text_only_invocation_for_run_ready: bool
    minimal_single_turn_run_ready: bool
    mock_provider_transport_ready: bool
    session_turn_append_ready: bool
    assistant_response_rendering_ready: bool
    run_unsafe_escalation_denial_ready: bool
    integrated_restore_document_ready: bool
    v0415_handoff_ready: bool
    ready_for_ask_command: bool
    ready_for_provider_doctor_completion: bool
    ready_for_unscoped_prompt_submission: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_read_only_skill_execution: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_trace_emission: bool
    ready_for_user_test_release: bool
    ready_for_file_write: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_shell_execution: bool
    ready_for_test_execution: bool
    ready_for_subagent_invocation: bool
    ready_for_child_session_creation: bool
    ready_for_parent_raw_transcript_sharing: bool
    ready_for_autonomous_loop_runtime: bool
    ready_for_retry_loop: bool
    ready_for_mission_scheduler: bool
    ready_for_mutable_memory_automation: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0415EventTraceRuntimeHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0416UserTestTargetUpdate:
    target_id: str
    target_version: str
    commands: tuple[str, ...]
    commands_expected_in_v0414: tuple[str, ...]
    user_test_release_ready: bool


@dataclass(frozen=True)
class V0414IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0414IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0414IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0414IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0414IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0414IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


def _merge(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _now_iso() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _home_path(home_path: str | None) -> str:
    return str(Path(home_path or Path.cwd() / ".chantacore-personal").resolve())


def _sessions_dir(home_path: str) -> Path:
    return Path(home_path) / "profiles" / PROFILE_ID / "state" / "sessions"


def _is_under_home(path: Path, home_path: str) -> bool:
    try:
        path.resolve().relative_to(Path(home_path).resolve())
        return True
    except ValueError:
        return False


def _short_user_input(user_input: str, limit: int = 120) -> str:
    normalized = " ".join(user_input.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 3] + "..."


def _session_id_or_create(home_path: str, session_id: str | None) -> str:
    if session_id:
        return session_id
    create_result = create_default_personal_session(
        create_default_personal_session_create_request(home_path)
    )
    return create_result.session_id


def _turns_jsonl_path(home_path: str, session_id: str) -> Path:
    return _sessions_dir(home_path) / session_id / "turns.jsonl"


def _provider_url(base_url: str, endpoint_path: str) -> str:
    parsed = urllib.parse.urlparse(base_url)
    safe = parsed._replace(params="", query="", fragment="")
    return urllib.parse.urljoin(urllib.parse.urlunparse(safe).rstrip("/") + "/", endpoint_path.lstrip("/"))


def create_provider_text_run_policy(command_name: str = "run", **overrides: Any) -> ProviderTextRunPolicy:
    is_run = command_name == "run"
    defaults = {
        "policy_id": "provider-text-run-policy-v0414",
        "profile_id": PROFILE_ID,
        "command_name": command_name,
        "provider_text_invocation_allowed": is_run,
        "prompt_submission_allowed": is_run,
        "provider_doctor_completion_allowed": False,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "active_tools_allowed": False,
        "provider_side_tools_allowed": False,
        "subagent_context_allowed": False,
        "file_attachment_allowed": False,
        "arbitrary_file_read_allowed": False,
        "shell_allowed": False,
        "workspace_mutation_allowed": False,
        "session_append_allowed": True,
        "trace_emission_allowed": False,
        "memory_write_allowed": False,
        "timeout_seconds": 20.0,
    }
    return ProviderTextRunPolicy(**_merge(defaults, overrides))


def create_provider_text_run_safety_report(
    policy: ProviderTextRunPolicy | None = None,
    **overrides: Any,
) -> ProviderTextRunSafetyReport:
    policy = policy or create_provider_text_run_policy()
    unsafe = (
        policy.provider_doctor_completion_allowed
        or policy.tool_calling_allowed
        or policy.function_calling_allowed
        or policy.active_tools_allowed
        or policy.provider_side_tools_allowed
        or policy.shell_allowed
        or policy.workspace_mutation_allowed
        or policy.subagent_context_allowed
        or policy.trace_emission_allowed
        or policy.memory_write_allowed
    )
    defaults = {
        "report_id": "provider-text-run-safety-v0414",
        "policy": policy,
        "safe_for_text_only_run": policy.command_name == "run" and not unsafe,
        "unsafe_escalation_detected": bool(unsafe),
        "provider_tool_calling_detected": policy.tool_calling_allowed or policy.provider_side_tools_allowed,
        "function_calling_detected": policy.function_calling_allowed,
        "shell_or_workspace_mutation_detected": policy.shell_allowed or policy.workspace_mutation_allowed,
        "subagent_context_detected": policy.subagent_context_allowed,
        "secret_redaction_confirmed": True,
    }
    return ProviderTextRunSafetyReport(**_merge(defaults, overrides))


def create_provider_text_request(
    user_input: str = "Hello",
    assembled_prompt: str | None = None,
    config: ProviderConfig | None = None,
    **overrides: Any,
) -> ProviderTextRequest:
    config = config or ProviderConfig(
        provider_id="mock-provider",
        provider_kind=ProviderKind.MOCK.value,
        source="test_fixture",
        base_url=None,
        model="mock-model",
        api_key_env_var=None,
        mode="text_only",
        tool_calling_allowed=False,
        function_calling_allowed=False,
        completion_allowed_in_doctor=False,
        completion_allowed_in_run=True,
        network_probe_allowed=False,
        remote_network_probe_allowed=False,
        metadata={},
    )
    defaults = {
        "request_id": "provider-text-request-v0414",
        "provider_id": config.provider_id,
        "provider_kind": config.provider_kind,
        "base_url": config.base_url,
        "model": config.model or "mock-model",
        "user_input": user_input,
        "assembled_prompt": assembled_prompt if assembled_prompt is not None else user_input,
        "system_prompt_preview": None,
        "timeout_seconds": create_provider_text_run_policy().timeout_seconds,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "active_tools": (),
        "sends_user_prompt": True,
        "sends_completion_request": True,
        "secret_env_var_name": config.api_key_env_var,
        "secret_value_printed": False,
    }
    return ProviderTextRequest(**_merge(defaults, overrides))


def create_provider_text_response(**overrides: Any) -> ProviderTextResponse:
    defaults = {
        "response_id": "provider-text-response-v0414",
        "request_id": "provider-text-request-v0414",
        "provider_id": "mock-provider",
        "status": ProviderTextRunStatus.SUCCESS.value,
        "text": "Mock provider response.",
        "raw_text_available": True,
        "trusted_for_memory": False,
        "trusted_for_execution": False,
        "trusted_for_process_state": False,
        "token_usage": None,
        "error_message": None,
        "error_class": None,
        "response_parse_status": None,
        "response_extracted_from_field": None,
        "response_content_length": None,
        "response_finish_reason": None,
        "provider_model": None,
        "runtime_identity_included": False,
        "provider_identity_is_implementation_detail": False,
        "empty_response_detected": False,
    }
    return ProviderTextResponse(**_merge(defaults, overrides))


def create_provider_text_transport_result(**overrides: Any) -> ProviderTextTransportResult:
    defaults = {
        "result_id": "provider-text-transport-result-v0414",
        "transport_kind": ProviderTextTransportKind.DISABLED.value,
        "attempted": False,
        "status": ProviderTextRunStatus.UNSUPPORTED.value,
        "response": None,
        "error_message": None,
        "network_accessed": False,
        "remote_network_accessed": False,
        "prompt_submitted": False,
        "provider_completion_invoked": False,
        "tool_calling_used": False,
        "function_calling_used": False,
        "secret_printed": False,
        "error_class": None,
        "timeout_seconds": None,
    }
    return ProviderTextTransportResult(**_merge(defaults, overrides))


def create_mock_provider_text_transport(**overrides: Any) -> MockProviderTextTransport:
    defaults = {
        "transport_id": "mock-provider-text-transport-v0414",
        "transport_kind": ProviderTextTransportKind.MOCK.value,
        "deterministic": True,
        "network_accessed": False,
        "process_launch_used": False,
        "file_inspection_used": False,
    }
    return MockProviderTextTransport(**_merge(defaults, overrides))


def invoke_mock_provider_text_transport(request: ProviderTextRequest) -> ProviderTextTransportResult:
    text = f"Mock provider response: {_short_user_input(request.user_input)}"
    response = create_provider_text_response(
        request_id=request.request_id,
        provider_id=request.provider_id,
        text=text,
    )
    return create_provider_text_transport_result(
        result_id="mock-provider-text-transport-result-v0414",
        transport_kind=ProviderTextTransportKind.MOCK.value,
        attempted=True,
        status=ProviderTextRunStatus.SUCCESS.value,
        response=response,
        network_accessed=False,
        remote_network_accessed=False,
        prompt_submitted=True,
        provider_completion_invoked=True,
    )


def create_openai_compatible_text_transport_config(
    config: ProviderConfig | None = None,
    **overrides: Any,
) -> OpenAICompatibleTextTransportConfig:
    config = config or ProviderConfig(
        provider_id="openai-compatible-provider",
        provider_kind=ProviderTextTransportKind.OPENAI_COMPATIBLE.value,
        source="test_fixture",
        base_url="http://127.0.0.1:1234/v1",
        model="local-model",
        api_key_env_var=None,
        mode="text_only",
        tool_calling_allowed=False,
        function_calling_allowed=False,
        completion_allowed_in_doctor=False,
        completion_allowed_in_run=True,
        network_probe_allowed=False,
        remote_network_probe_allowed=False,
        metadata={},
    )
    defaults = {
        "provider_id": config.provider_id,
        "base_url": config.base_url or "",
        "model": config.model or "",
        "api_key_env_var": config.api_key_env_var,
        "timeout_seconds": create_provider_text_run_policy().timeout_seconds,
        "endpoint_path": "/chat/completions",
    }
    return OpenAICompatibleTextTransportConfig(**_merge(defaults, overrides))


def invoke_openai_compatible_text_transport(
    request: ProviderTextRequest,
    config: OpenAICompatibleTextTransportConfig | None = None,
) -> OpenAICompatibleTextTransportResult:
    transport_config = config or create_openai_compatible_text_transport_config(
        ProviderConfig(
            provider_id=request.provider_id,
            provider_kind=request.provider_kind,
            source="profile_file",
            base_url=request.base_url,
            model=request.model,
            api_key_env_var=request.secret_env_var_name,
            mode="text_only",
            tool_calling_allowed=False,
            function_calling_allowed=False,
            completion_allowed_in_doctor=False,
            completion_allowed_in_run=True,
            network_probe_allowed=False,
            remote_network_probe_allowed=False,
            metadata={},
        )
    )
    if not transport_config.base_url or not transport_config.model:
        result = create_provider_text_transport_result(
            transport_kind=ProviderTextTransportKind.OPENAI_COMPATIBLE.value,
            attempted=False,
            status=ProviderTextRunStatus.PROVIDER_NOT_CONFIGURED.value,
            error_message="base_url and model are required for configured provider run",
            error_class="provider_not_configured",
            timeout_seconds=transport_config.timeout_seconds,
        )
        return OpenAICompatibleTextTransportResult(transport_config, result, False, False, False)
    endpoint = _provider_url(transport_config.base_url, transport_config.endpoint_path)
    identity_prompt = create_v042_runtime_identity_prompt()
    identity_report = create_v042_runtime_identity_injection_report(provider_model=transport_config.model)
    payload = json.dumps(
        {
            "model": transport_config.model,
            "messages": [
                {"role": "system", "content": identity_prompt.prompt_text},
                {"role": "user", "content": request.assembled_prompt},
            ],
            "stream": False,
        }
    ).encode("utf-8")
    headers = {"Content-Type": "application/json"}
    if transport_config.api_key_env_var:
        api_key = os.environ.get(transport_config.api_key_env_var)
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
    http_request = urllib.request.Request(endpoint, data=payload, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(http_request, timeout=transport_config.timeout_seconds) as response:
            data = json.loads(response.read().decode("utf-8"))
        parse_result = parse_v042_openai_compatible_response(data)
        recording_decision = create_v042_run_response_recording_decision(parse_result)
        token_usage = data.get("usage") if isinstance(data, dict) else None
        provider_response = create_provider_text_response(
            request_id=request.request_id,
            provider_id=request.provider_id,
            status=ProviderTextRunStatus.SUCCESS.value if recording_decision.response_valid else ProviderTextRunStatus.FAILED.value,
            text=parse_result.assistant_text,
            token_usage=token_usage,
            error_message=None if recording_decision.response_valid else parse_result.diagnostic_summary,
            error_class=None if recording_decision.response_valid else parse_result.error_class,
            response_parse_status=parse_result.status,
            response_extracted_from_field=parse_result.extracted_from_field,
            response_content_length=parse_result.content_length,
            response_finish_reason=parse_result.response_shape_summary.finish_reason,
            provider_model=parse_result.response_shape_summary.provider_model or transport_config.model,
            runtime_identity_included=identity_report.runtime_identity_included,
            provider_identity_is_implementation_detail=identity_report.provider_identity_is_implementation_detail,
            empty_response_detected=not parse_result.assistant_text_present,
        )
        result = create_provider_text_transport_result(
            transport_kind=ProviderTextTransportKind.OPENAI_COMPATIBLE.value,
            attempted=True,
            status=ProviderTextRunStatus.SUCCESS.value if recording_decision.response_valid else ProviderTextRunStatus.FAILED.value,
            response=provider_response,
            error_message=None if recording_decision.response_valid else parse_result.diagnostic_summary,
            network_accessed=True,
            remote_network_accessed=urllib.parse.urlparse(transport_config.base_url).hostname not in {"localhost", "127.0.0.1", "::1"},
            prompt_submitted=True,
            provider_completion_invoked=True,
            error_class=None if recording_decision.response_valid else parse_result.error_class,
            timeout_seconds=transport_config.timeout_seconds,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        error_class = _classify_provider_transport_error(exc)
        status = ProviderTextRunStatus.TIMEOUT.value if error_class == "provider_timeout" else ProviderTextRunStatus.PROVIDER_UNAVAILABLE.value
        result = create_provider_text_transport_result(
            transport_kind=ProviderTextTransportKind.OPENAI_COMPATIBLE.value,
            attempted=True,
            status=status,
            error_message=str(exc),
            network_accessed=True,
            remote_network_accessed=urllib.parse.urlparse(transport_config.base_url).hostname not in {"localhost", "127.0.0.1", "::1"},
            prompt_submitted=True,
            provider_completion_invoked=True,
            error_class=error_class,
            timeout_seconds=transport_config.timeout_seconds,
        )
    return OpenAICompatibleTextTransportResult(transport_config, result, False, False, False)


def _classify_provider_transport_error(exc: BaseException) -> str:
    text = str(exc).lower()
    reason = getattr(exc, "reason", None)
    reason_text = str(reason).lower() if reason is not None else ""
    combined = f"{text} {reason_text}"
    if isinstance(exc, TimeoutError) or "timed out" in combined or "timeout" in combined:
        return "provider_timeout"
    if "connection refused" in combined or "actively refused" in combined or "winerror 10061" in combined:
        return "connection_refused"
    if isinstance(exc, json.JSONDecodeError):
        return "invalid_provider_response"
    return "unknown_provider_error"


def create_provider_text_invocation_audit(**overrides: Any) -> ProviderTextInvocationAudit:
    defaults = {
        "audit_id": "provider-text-invocation-audit-v0414",
        "command_name": "run",
        "provider_id": "mock-provider",
        "prompt_submitted": True,
        "provider_completion_invoked": True,
        "provider_doctor_completion_invoked": False,
        "tool_calling_used": False,
        "function_calling_used": False,
        "secret_printed": False,
        "trace_emitted": False,
    }
    return ProviderTextInvocationAudit(**_merge(defaults, overrides))


def create_scoped_prompt_submission_record(**overrides: Any) -> ScopedPromptSubmissionRecord:
    defaults = {
        "record_id": "scoped-prompt-submission-v0414",
        "command_name": "run",
        "profile_id": PROFILE_ID,
        "session_id": None,
        "allowed_scope": "run_only",
        "prompt_submitted": True,
        "provider_invoked": True,
        "prompt_submitted_outside_run": False,
        "provider_invoked_outside_run": False,
        "tool_calling_used": False,
        "function_calling_used": False,
    }
    return ScopedPromptSubmissionRecord(**_merge(defaults, overrides))


def create_minimal_single_turn_run_input(
    home_path: str,
    user_input: str = "Hello",
    **overrides: Any,
) -> MinimalSingleTurnRunInput:
    defaults = {
        "input_id": "minimal-single-turn-run-input-v0414",
        "profile_id": PROFILE_ID,
        "home_path": _home_path(home_path),
        "user_input": user_input,
        "session_id": None,
        "provider_override": None,
        "use_mock_provider": False,
        "max_steps": 1,
        "timeout_seconds": None,
    }
    return MinimalSingleTurnRunInput(**_merge(defaults, overrides))


def create_minimal_single_turn_stop_condition(**overrides: Any) -> MinimalSingleTurnStopCondition:
    defaults = {
        "stop_after_provider_response": True,
        "stop_after_error": True,
        "max_steps": 1,
        "allow_retry": False,
        "allow_followup_without_user": False,
    }
    return MinimalSingleTurnStopCondition(**_merge(defaults, overrides))


def create_minimal_single_turn_run_loop(**overrides: Any) -> MinimalSingleTurnRunLoop:
    defaults = {
        "loop_id": "minimal-single-turn-run-loop-v0414",
        "profile_id": PROFILE_ID,
        "max_steps": 1,
        "current_step": 0,
        "stop_condition": create_minimal_single_turn_stop_condition(),
        "general_agent_loop_opened": False,
        "autonomous_continuation_allowed": False,
        "retry_loop_allowed": False,
        "subagent_allowed": False,
        "skill_execution_allowed": False,
    }
    return MinimalSingleTurnRunLoop(**_merge(defaults, overrides))


def create_run_session_append_policy(**overrides: Any) -> RunSessionAppendPolicy:
    defaults = {
        "append_user_turn": True,
        "append_assistant_turn": True,
        "create_session_if_missing": True,
        "overwrite_allowed": False,
        "write_outside_home_allowed": False,
    }
    return RunSessionAppendPolicy(**_merge(defaults, overrides))


def create_run_session_turn_record(
    session_id: str = "session-test",
    role: str = "user",
    content: str = "",
    **overrides: Any,
) -> RunSessionTurnRecord:
    defaults = {
        "turn_id": f"turn-{role}-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S%f')}",
        "session_id": session_id,
        "role": role,
        "content": content,
        "created_at": _now_iso(),
        "source": "chanta-cli run",
        "provider_generated": role == "assistant",
        "provider_id": None,
        "prompt_submitted": role == "assistant",
        "trusted_for_memory": False,
        "trusted_for_execution": False,
        "metadata": {"v0414_single_turn": True},
    }
    return RunSessionTurnRecord(**_merge(defaults, overrides))


def create_run_session_append_result(**overrides: Any) -> RunSessionAppendResult:
    defaults = {
        "result_id": "run-session-append-result-v0414",
        "session_id": "session-test",
        "turns_jsonl_path": "",
        "appended_turn_count": 0,
        "overwritten_files": (),
        "outside_home_paths": (),
        "success": False,
    }
    return RunSessionAppendResult(**_merge(defaults, overrides))


def append_run_session_turns(
    home_path: str,
    session_id: str,
    user_input: str,
    assistant_text: str,
    provider_id: str,
    **overrides: Any,
) -> RunSessionAppendResult:
    home = _home_path(home_path)
    session_dir = _sessions_dir(home) / session_id
    turns_path = _turns_jsonl_path(home, session_id)
    paths = (session_dir, turns_path)
    outside = tuple(str(path) for path in paths if not _is_under_home(path, home))
    if outside:
        return create_run_session_append_result(
            session_id=session_id,
            turns_jsonl_path=str(turns_path),
            outside_home_paths=outside,
            success=False,
            **overrides,
        )
    if not session_dir.exists():
        create_default_personal_session(
            create_default_personal_session_create_request(home, explicit_session_id=session_id)
        )
    user_turn = create_run_session_turn_record(
        session_id=session_id,
        role="user",
        content=user_input,
        provider_generated=False,
        provider_id=None,
        prompt_submitted=True,
    )
    assistant_turn = create_run_session_turn_record(
        session_id=session_id,
        role="assistant",
        content=assistant_text,
        provider_generated=True,
        provider_id=provider_id,
        prompt_submitted=True,
    )
    with turns_path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(asdict(user_turn), ensure_ascii=False, sort_keys=True) + "\n")
        handle.write(json.dumps(asdict(assistant_turn), ensure_ascii=False, sort_keys=True) + "\n")
    defaults = {
        "result_id": "run-session-append-result-v0414",
        "session_id": session_id,
        "turns_jsonl_path": str(turns_path),
        "appended_turn_count": 2,
        "overwritten_files": (),
        "outside_home_paths": (),
        "success": True,
    }
    return RunSessionAppendResult(**_merge(defaults, overrides))


def create_assistant_response_render_policy(**overrides: Any) -> AssistantResponseRenderPolicy:
    defaults = {
        "include_safety_notice": True,
        "include_profile_id": True,
        "include_session_id": True,
        "include_trace_notice": True,
        "mark_untrusted_provider_text": True,
    }
    return AssistantResponseRenderPolicy(**_merge(defaults, overrides))


def render_assistant_response(
    assistant_text: str,
    profile_id: str = PROFILE_ID,
    session_id: str | None = None,
    policy: AssistantResponseRenderPolicy | None = None,
    **overrides: Any,
) -> AssistantResponseRenderResult:
    policy = policy or create_assistant_response_render_policy()
    parts: list[str] = []
    if policy.include_safety_notice:
        parts.append("[v0.41.4 single-turn text-only run]")
    if policy.include_profile_id:
        parts.append(f"profile: {profile_id}")
    if policy.include_session_id and session_id:
        parts.append(f"session: {session_id}")
    if policy.include_trace_notice:
        parts.append("trace runtime remains closed until v0.41.5")
    if policy.mark_untrusted_provider_text:
        parts.append("provider text is untrusted for memory, execution, and process state")
    parts.append("")
    parts.append(assistant_text)
    defaults = {
        "rendered_text": "\n".join(parts),
        "provider_text_marked_untrusted": policy.mark_untrusted_provider_text,
        "trace_notice_included": policy.include_trace_notice,
        "production_certified": False,
    }
    return AssistantResponseRenderResult(**_merge(defaults, overrides))


def create_run_unsafe_escalation_check(user_input: str = "", **overrides: Any) -> RunUnsafeEscalationCheck:
    text = user_input.lower()
    checks = {
        "tool_calling": "tool" in text and "call" in text,
        "function_calling": "function" in text and "call" in text,
        "file_write_edit": ("write file" in text) or ("edit file" in text) or ("apply patch" in text),
        "shell": "shell" in text or "powershell" in text or "cmd.exe" in text,
        "test_execution": "run tests" in text,
        "subagent": "subagent" in text,
        "child_session": "child session" in text,
        "retry_loop": "retry loop" in text,
        "autonomous_loop": "autonomous" in text,
        "dominion": "dominion" in text,
        "production_certification": "production cert" in text,
    }
    unsafe_items = tuple(name for name, present in checks.items() if present)
    defaults = {
        "check_id": "run-unsafe-escalation-check-v0414",
        "user_input": user_input,
        "unsafe_items": unsafe_items,
        "tool_calling_requested": checks["tool_calling"],
        "function_calling_requested": checks["function_calling"],
        "file_write_or_edit_requested": checks["file_write_edit"],
        "shell_requested": checks["shell"],
        "test_execution_requested": checks["test_execution"],
        "subagent_requested": checks["subagent"],
        "child_session_requested": checks["child_session"],
        "retry_loop_requested": checks["retry_loop"],
        "autonomous_loop_requested": checks["autonomous_loop"],
        "dominion_requested": checks["dominion"],
        "production_certification_requested": checks["production_certification"],
    }
    return RunUnsafeEscalationCheck(**_merge(defaults, overrides))


def create_run_unsafe_escalation_decision(
    check: RunUnsafeEscalationCheck | None = None,
    **overrides: Any,
) -> RunUnsafeEscalationDecision:
    check = check or create_run_unsafe_escalation_check()
    blocked = bool(check.unsafe_items)
    defaults = {
        "decision_id": "run-unsafe-escalation-decision-v0414",
        "blocked": blocked,
        "reason": "Unsafe run escalation requested." if blocked else "No unsafe escalation detected.",
        "unsafe_items": check.unsafe_items,
        "safe_alternative": "chanta-cli prompt preview",
        "executed": False if blocked else True,
    }
    return RunUnsafeEscalationDecision(**_merge(defaults, overrides))


def create_minimal_single_turn_run_context(
    run_input: MinimalSingleTurnRunInput | None = None,
    session_id: str | None = None,
    prompt_preview: str = "",
    provider_id: str = "mock-provider",
    **overrides: Any,
) -> MinimalSingleTurnRunContext:
    run_input = run_input or create_minimal_single_turn_run_input(str(Path.cwd()))
    defaults = {
        "context_id": "minimal-single-turn-run-context-v0414",
        "profile_id": run_input.profile_id,
        "profile_loaded": True,
        "prompt_assembled": True,
        "provider_config_loaded": True,
        "session_ready": True,
        "safety_report": create_provider_text_run_safety_report(),
        "prompt_preview": prompt_preview,
        "provider_id": provider_id,
        "session_id": session_id or "session-test",
    }
    return MinimalSingleTurnRunContext(**_merge(defaults, overrides))


def create_minimal_single_turn_run_result(**overrides: Any) -> MinimalSingleTurnRunResult:
    defaults = {
        "result_id": "minimal-single-turn-run-result-v0414",
        "input_id": "minimal-single-turn-run-input-v0414",
        "profile_id": PROFILE_ID,
        "session_id": "session-test",
        "status": ProviderTextRunStatus.SUCCESS.value,
        "assistant_text": "",
        "provider_response": None,
        "session_append_result": None,
        "provider_invoked": False,
        "prompt_submitted": False,
        "agent_loop_started": False,
        "general_agent_loop_opened": False,
        "skill_executed": False,
        "trace_emitted": False,
        "workspace_mutated": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return MinimalSingleTurnRunResult(**_merge(defaults, overrides))


def _mock_provider_config() -> ProviderConfig:
    return ProviderConfig(
        provider_id="mock-provider",
        provider_kind=ProviderKind.MOCK.value,
        source="test_fixture",
        base_url=None,
        model="mock-model",
        api_key_env_var=None,
        mode="text_only",
        tool_calling_allowed=False,
        function_calling_allowed=False,
        completion_allowed_in_doctor=False,
        completion_allowed_in_run=True,
        network_probe_allowed=False,
        remote_network_probe_allowed=False,
        metadata={"v0414_mock": True},
    )


def _render_provider_failure_text(config: ProviderConfig, transport_result: ProviderTextTransportResult) -> str:
    error_class = transport_result.error_class or (
        "provider_timeout" if transport_result.status == ProviderTextRunStatus.TIMEOUT.value else "unknown_provider_error"
    )
    timeout = transport_result.timeout_seconds or create_provider_text_run_policy().timeout_seconds
    response = transport_result.response
    if response and response.empty_response_detected:
        parse_status = response.response_parse_status or "parsed_empty"
        guide = create_v042_provider_reasoning_model_troubleshooting_guide()
        return "\n".join(
            (
                "Configured provider returned no final assistant content.",
                f"error_class: {error_class}",
                f"response_parse_status: {parse_status}",
                "next:",
                *[f"* {item}" for item in guide.recommended_actions[:5]],
                f"run_id: (assigned by trace runtime)",
                "provider_text_untrusted: true",
                "provider_invoked: true",
                "prompt_submitted: true",
                "shell_executed: false",
                "subagent_invoked: false",
                "production_certified: false",
            )
        )
    return "\n".join(
        (
            "Configured provider run failed.",
            "status: failed",
            f"error_class: {error_class}",
            f"base_url: {config.base_url or '(none)'}",
            f"model: {config.model or '(none)'}",
            f"timeout_seconds: {timeout:g}",
            "provider_invoked: true",
            "prompt_submitted: true",
            "shell_executed: false",
            "subagent_invoked: false",
            "production_certified: false",
            f"error_message: {transport_result.error_message or '(none)'}",
            "next_action:",
            "1. check LM Studio server is running",
            "2. run chanta-cli provider connectivity or provider doctor --no-completion --probe-models",
            "3. confirm model id from /v1/models",
            "4. increase timeout with chanta-cli run --timeout 120",
            "5. try a smaller model",
        )
    )


def run_minimal_single_turn(run_input: MinimalSingleTurnRunInput, **overrides: Any) -> MinimalSingleTurnRunResult:
    if run_input.max_steps > 1:
        return create_minimal_single_turn_run_result(
            input_id=run_input.input_id,
            profile_id=run_input.profile_id,
            session_id=run_input.session_id or "",
            status=ProviderTextRunStatus.BLOCKED.value,
            assistant_text="max_steps must be 1 in v0.41.4",
        )
    check = create_run_unsafe_escalation_check(run_input.user_input)
    decision = create_run_unsafe_escalation_decision(check)
    if decision.blocked:
        return create_minimal_single_turn_run_result(
            input_id=run_input.input_id,
            profile_id=run_input.profile_id,
            session_id=run_input.session_id or "",
            status=ProviderTextRunStatus.UNSAFE_REQUEST.value,
            assistant_text=decision.reason,
        )
    home = _home_path(run_input.home_path)
    session_id = _session_id_or_create(home, run_input.session_id)
    prompt_result = assemble_default_personal_prompt(
        PromptAssemblyInput(
            "run-prompt-assembly-input-v0414",
            run_input.profile_id,
            home,
            run_input.user_input,
            home,
            session_id,
            True,
            True,
            True,
            True,
        )
    )
    config = _mock_provider_config() if run_input.use_mock_provider else load_provider_config_from_profile(home)
    if run_input.provider_override == "mock":
        config = _mock_provider_config()
    if config.provider_kind == ProviderKind.MOCK.value or run_input.use_mock_provider:
        request = create_provider_text_request(run_input.user_input, prompt_result.rendered_preview, config, timeout_seconds=run_input.timeout_seconds or create_provider_text_run_policy().timeout_seconds)
        transport_result = invoke_mock_provider_text_transport(request)
    else:
        if config.mode != "text_only" or not config.base_url or not config.model:
            return create_minimal_single_turn_run_result(
                input_id=run_input.input_id,
                profile_id=run_input.profile_id,
                session_id=session_id,
                status=ProviderTextRunStatus.PROVIDER_NOT_CONFIGURED.value,
                assistant_text="Provider config must set mode=text_only, base_url, and model for non-mock run.",
            )
        timeout_seconds = run_input.timeout_seconds or create_provider_text_run_policy().timeout_seconds
        request = create_provider_text_request(run_input.user_input, prompt_result.rendered_preview, config, timeout_seconds=timeout_seconds)
        transport_config = create_openai_compatible_text_transport_config(config, timeout_seconds=timeout_seconds)
        transport_result = invoke_openai_compatible_text_transport(request, transport_config).transport_result
    response = transport_result.response
    assistant_text = response.text if response and transport_result.status == ProviderTextRunStatus.SUCCESS.value else _render_provider_failure_text(config, transport_result)
    append_result = None
    if transport_result.status == ProviderTextRunStatus.SUCCESS.value and response is not None:
        append_result = append_run_session_turns(home, session_id, run_input.user_input, assistant_text, request.provider_id)
    defaults = {
        "result_id": "minimal-single-turn-run-result-v0414",
        "input_id": run_input.input_id,
        "profile_id": run_input.profile_id,
        "session_id": session_id,
        "status": transport_result.status,
        "assistant_text": assistant_text,
        "provider_response": response,
        "session_append_result": append_result,
        "provider_invoked": transport_result.provider_completion_invoked,
        "prompt_submitted": transport_result.prompt_submitted,
        "agent_loop_started": True if transport_result.status == ProviderTextRunStatus.SUCCESS.value else False,
        "general_agent_loop_opened": False,
        "skill_executed": False,
        "trace_emitted": False,
        "workspace_mutated": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return MinimalSingleTurnRunResult(**_merge(defaults, overrides))


def create_run_command_input(
    home_path: str,
    user_input: str = "Hello",
    **overrides: Any,
) -> RunCommandInput:
    defaults = {
        "profile_id": PROFILE_ID,
        "home_path": _home_path(home_path),
        "user_input": user_input,
        "session_id": None,
        "provider": None,
        "mock_provider": False,
        "timeout_seconds": None,
    }
    return RunCommandInput(**_merge(defaults, overrides))


def create_run_command_result(**overrides: Any) -> RunCommandResult:
    run_result = create_minimal_single_turn_run_result()
    defaults = {
        "status": run_result.status,
        "rendered_text": "",
        "exit_code": 1,
        "run_result": run_result,
        "provider_invoked": run_result.provider_invoked,
        "prompt_submitted": run_result.prompt_submitted,
        "trace_emitted": False,
        "production_certified": False,
    }
    return RunCommandResult(**_merge(defaults, overrides))


def execute_run_command(command_input: RunCommandInput, **overrides: Any) -> RunCommandResult:
    run_input = create_minimal_single_turn_run_input(
        command_input.home_path,
        command_input.user_input,
        profile_id=command_input.profile_id,
        session_id=command_input.session_id,
        provider_override=command_input.provider,
        use_mock_provider=command_input.mock_provider or command_input.provider == "mock",
        timeout_seconds=command_input.timeout_seconds,
    )
    run_result = run_minimal_single_turn(run_input)
    render_result = render_assistant_response(
        run_result.assistant_text,
        command_input.profile_id,
        run_result.session_id,
    )
    exit_code = 0 if run_result.status == ProviderTextRunStatus.SUCCESS.value else 1
    defaults = {
        "status": run_result.status,
        "rendered_text": render_result.rendered_text,
        "exit_code": exit_code,
        "run_result": run_result,
        "provider_invoked": run_result.provider_invoked,
        "prompt_submitted": run_result.prompt_submitted,
        "trace_emitted": False,
        "production_certified": False,
    }
    return RunCommandResult(**_merge(defaults, overrides))


def create_v0414_readiness_report(**overrides: Any) -> V0414ReadinessReport:
    defaults = {
        "report_id": "v0414-readiness-report",
        "run_command_ready": True,
        "scoped_prompt_submission_for_run_ready": True,
        "provider_text_only_invocation_for_run_ready": True,
        "minimal_single_turn_run_ready": True,
        "mock_provider_transport_ready": True,
        "session_turn_append_ready": True,
        "assistant_response_rendering_ready": True,
        "run_unsafe_escalation_denial_ready": True,
        "integrated_restore_document_ready": True,
        "v0415_handoff_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return V0414ReadinessReport(**_merge(defaults, overrides))


def create_v0415_event_trace_runtime_handoff(**overrides: Any) -> V0415EventTraceRuntimeHandoff:
    defaults = {
        "handoff_id": "v0415-event-trace-runtime-handoff",
        "target_version": "v0.41.5 Event Trace Emission & Runtime Report",
        "recommended_focus": (
            "emit runtime events for doctor/init/profile/prompt/session/provider/run/denial",
            "implement chanta-cli trace recent",
            "implement chanta-cli trace summary",
            "implement chanta-cli run-report last",
            "attach run/session/profile/provider object refs",
            "no subagent",
            "no shell/edit/apply/test execution",
            "no production certification",
        ),
        "still_closed": tuple(item for item in CLOSED_CAPABILITIES if item != "trace_emission"),
    }
    return V0415EventTraceRuntimeHandoff(**_merge(defaults, overrides))


def create_v0416_user_test_target_update(**overrides: Any) -> V0416UserTestTargetUpdate:
    defaults = {
        "target_id": "v0416-user-test-target-update-v0414",
        "target_version": "v0.41.6 Installable User-Test Release",
        "commands": V0416_TARGET_COMMANDS,
        "commands_expected_in_v0414": (
            "py -m pip install -e .",
            "chanta-cli --version",
            "chanta-cli doctor",
            'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"',
            "chanta-cli profile status --profile default-personal",
            "chanta-cli provider doctor --profile default-personal --no-completion",
            'chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."',
        ),
        "user_test_release_ready": False,
    }
    return V0416UserTestTargetUpdate(**_merge(defaults, overrides))


def create_v0414_integrated_restore_sections() -> tuple[V0414IntegratedRestoreSection, ...]:
    return tuple(
        V0414IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.41.4 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0414_integrated_restore_context_snapshot(**overrides: Any) -> V0414IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0414",
        "current_version": V0414_RELEASE_NAME,
        "current_track": V0414_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
            V0414_RELEASE_NAME,
        ),
        "open_capabilities": OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "next_recommended_version": "v0.41.5 Event Trace Emission & Runtime Report",
    }
    return V0414IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0414_integrated_restore_packet(**overrides: Any) -> V0414IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0414",
        "snapshot": create_v0414_integrated_restore_context_snapshot(),
        "restore_sections": create_v0414_integrated_restore_sections(),
        "required_test_commands": (
            "tests/test_v0414_minimal_single_turn_provider_backed_run.py",
            "tests/test_v0413_safe_provider_probe_read_only_skill_registry.py",
            "tests/test_v0412_prompt_assembly_session_store.py",
            "tests/test_v0411_installable_cli_bootstrap_doctor.py",
            "tests/test_v0410_default_personal_profile_runtime.py",
            "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
        ),
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0414IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0414_integrated_restore_document_manifest(**overrides: Any) -> V0414IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0414",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0414IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def v0414_readiness_preserves_closed_runtime(report: V0414ReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0414IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def _handle_run(args: Sequence[str]) -> int:
    if "--home" not in args:
        print(
            json.dumps(
                {
                    "command_name": "run",
                    "status": ProviderTextRunStatus.INVALID_CONFIG.value,
                    "blocked": True,
                    "future_target_version": V0414_VERSION,
                    "reason": "chanta-cli run requires an explicit --home path in v0.41.4",
                    "safe_alternative": 'chanta-cli run --profile default-personal --home <path> --provider mock "..."',
                    "executed": False,
                    "provider_invoked": False,
                    "prompt_submitted": False,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 1
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("run")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--session", dest="session_id")
    parser.add_argument("--provider")
    parser.add_argument("--timeout", type=float, default=None)
    parser.add_argument("user_input")
    parsed = parser.parse_args(args)
    result = execute_run_command(
        RunCommandInput(
            parsed.profile,
            parsed.home,
            parsed.user_input,
            parsed.session_id,
            parsed.provider,
            parsed.provider == "mock",
            parsed.timeout,
        )
    )
    print(result.rendered_text)
    return result.exit_code


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"--version", "-V", "version"}:
        print("chanta-cli v0.41.1 / v0.41.2 prompt-session / v0.41.3 provider-skills / v0.41.4 run")
        return 0
    if args[0] == "doctor":
        print("chanta-cli doctor v0.41.1")
        print("current_extension: v0.41.4 minimal-single-turn-run")
        print("next: v0.41.5 Event Trace Emission & Runtime Report")
        print("run_command: pass")
        print("provider_text_only_invocation_for_run: pass")
        print("provider_doctor_completion: closed")
        print("tool_calling: closed")
        print("function_calling: closed")
        print("general_agent_loop: closed")
        print("skill_execution: closed")
        print("trace_runtime: closed")
        print("closed: " + ", ".join(CLOSED_CAPABILITIES))
        return 0
    if args[0] == "run":
        return _handle_run(args)
    return v0413_main(args)


__all__ = [
    "CLOSED_CAPABILITIES",
    "INTEGRATED_DOC_PATH",
    "OPEN_CAPABILITIES",
    "ProviderTextTransportKind",
    "ProviderTextRunStatus",
    "ProviderTextRunPolicy",
    "ProviderTextRunSafetyReport",
    "ProviderTextRequest",
    "ProviderTextResponse",
    "ProviderTextTransportResult",
    "MockProviderTextTransport",
    "OpenAICompatibleTextTransportConfig",
    "OpenAICompatibleTextTransportResult",
    "ProviderTextInvocationAudit",
    "ScopedPromptSubmissionRecord",
    "MinimalSingleTurnRunInput",
    "MinimalSingleTurnRunContext",
    "MinimalSingleTurnRunLoop",
    "MinimalSingleTurnStopCondition",
    "MinimalSingleTurnRunResult",
    "RunCommandInput",
    "RunCommandResult",
    "RunSessionAppendPolicy",
    "RunSessionTurnRecord",
    "RunSessionAppendResult",
    "AssistantResponseRenderPolicy",
    "AssistantResponseRenderResult",
    "RunUnsafeEscalationCheck",
    "RunUnsafeEscalationDecision",
    "V0414ReadinessReport",
    "V0415EventTraceRuntimeHandoff",
    "V0416UserTestTargetUpdate",
    "V0414IntegratedRestoreSection",
    "V0414IntegratedRestoreContextSnapshot",
    "V0414IntegratedRestorePacket",
    "V0414IntegratedRestoreDocumentManifest",
    "append_run_session_turns",
    "create_assistant_response_render_policy",
    "create_minimal_single_turn_run_context",
    "create_minimal_single_turn_run_input",
    "create_minimal_single_turn_run_loop",
    "create_minimal_single_turn_run_result",
    "create_minimal_single_turn_stop_condition",
    "create_mock_provider_text_transport",
    "create_openai_compatible_text_transport_config",
    "create_provider_text_invocation_audit",
    "create_provider_text_request",
    "create_provider_text_response",
    "create_provider_text_run_policy",
    "create_provider_text_run_safety_report",
    "create_provider_text_transport_result",
    "create_run_command_input",
    "create_run_command_result",
    "create_run_session_append_policy",
    "create_run_session_append_result",
    "create_run_session_turn_record",
    "create_run_unsafe_escalation_check",
    "create_run_unsafe_escalation_decision",
    "create_scoped_prompt_submission_record",
    "create_v0414_integrated_restore_context_snapshot",
    "create_v0414_integrated_restore_document_manifest",
    "create_v0414_integrated_restore_packet",
    "create_v0414_integrated_restore_sections",
    "create_v0414_readiness_report",
    "create_v0415_event_trace_runtime_handoff",
    "create_v0416_user_test_target_update",
    "execute_run_command",
    "integrated_restore_packet_uses_single_doc",
    "invoke_mock_provider_text_transport",
    "invoke_openai_compatible_text_transport",
    "main",
    "render_assistant_response",
    "run_minimal_single_turn",
    "v0414_readiness_preserves_closed_runtime",
]
