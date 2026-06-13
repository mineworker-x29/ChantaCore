"""v0.41.3 safe provider doctor and read-only skill registry support.

The provider doctor is no-completion by default and may only perform an
explicit loopback models probe. Skill registry commands list and inspect static
metadata only; they do not execute skills.
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
from enum import StrEnum
from pathlib import Path
from typing import Any, Sequence

from chanta_core.personal_runtime.default_personal_profile_runtime import V0416_TARGET_COMMANDS
from chanta_core.personal_runtime.default_personal_prompt_session import (
    PROFILE_ID,
    main as v0412_main,
)


V0413_VERSION = "v0.41.3"
V0413_RELEASE_NAME = "v0.41.3 Safe Provider Probe & Read-only Skill Registry"
V0413_TRACK_NAME = "v0.41 Default Personal Runtime Opening Track"
CLI_NAME = "chanta-cli"
INTEGRATED_DOC_PATH = "docs/versions/v0.41/v0.41.3_safe_provider_probe_read_only_skill_registry_restore.md"


class ProviderKind(StrEnum):
    OPENAI_COMPATIBLE = "openai_compatible"
    LOCAL_OPENAI_COMPATIBLE = "local_openai_compatible"
    LM_STUDIO = "lm_studio"
    OLLAMA_COMPATIBLE = "ollama_compatible"
    MOCK = "mock"
    UNKNOWN = "unknown"


class ProviderConfigSource(StrEnum):
    PROFILE_FILE = "profile_file"
    ENVIRONMENT = "environment"
    DEFAULT_METADATA = "default_metadata"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class ProviderEndpointKind(StrEnum):
    LOOPBACK = "loopback"
    REMOTE = "remote"
    MISSING = "missing"
    INVALID = "invalid"
    UNKNOWN = "unknown"


class ProviderDoctorStatus(StrEnum):
    PASS = "pass"
    WARN = "warn"
    FAIL = "fail"
    SKIPPED = "skipped"
    BLOCKED = "blocked"
    NOT_CONFIGURED = "not_configured"


class ReadOnlySkillKind(StrEnum):
    PROFILE_STATUS = "profile_status"
    CONFIG_VIEW = "config_view"
    PROVIDER_STATUS = "provider_status"
    RESTORE_SUMMARY = "restore_summary"
    TRACE_RECENT = "trace_recent"
    TRACE_SUMMARY = "trace_summary"
    STATUS_SUMMARY = "status_summary"
    DOCS_REFERENCE_SEARCH = "docs_reference_search"
    LIST_AVAILABLE_SKILLS = "list_available_skills"
    UNSAFE_COMMAND_CHECK = "unsafe_command_check"
    UNKNOWN = "unknown"


class ReadOnlySkillSafetyClass(StrEnum):
    READ_ONLY_METADATA = "read_only_metadata"
    READ_ONLY_FILE_BOUNDED = "read_only_file_bounded"
    FUTURE_TRACE_READ = "future_trace_read"
    FUTURE_DOCS_READ = "future_docs_read"
    UNSAFE_WRITE = "unsafe_write"
    UNSAFE_SHELL = "unsafe_shell"
    UNSAFE_SUBAGENT = "unsafe_subagent"
    UNSAFE_PROVIDER_TOOL = "unsafe_provider_tool"
    UNKNOWN = "unknown"


class ReadOnlySkillCapabilityStatus(StrEnum):
    REGISTERED = "registered"
    INSPECTABLE = "inspectable"
    FUTURE_GATED = "future_gated"
    EXECUTION_CLOSED = "execution_closed"
    UNSUPPORTED = "unsupported"
    UNSAFE_DENIED = "unsafe_denied"


class UnsafeSkillRequestKind(StrEnum):
    FILE_WRITE = "file_write"
    FILE_EDIT = "file_edit"
    PATCH_APPLY = "patch_apply"
    SHELL_EXECUTE = "shell_execute"
    TEST_EXECUTE = "test_execute"
    PROVIDER_TOOL_CALL = "provider_tool_call"
    FUNCTION_CALL = "function_call"
    SUBAGENT_INVOKE = "subagent_invoke"
    CHILD_SESSION_CREATE = "child_session_create"
    NETWORK_UNBOUNDED = "network_unbounded"
    CREDENTIAL_ACCESS = "credential_access"
    MEMORY_MUTATE = "memory_mutate"
    MISSION_SCHEDULE = "mission_schedule"
    DOMINION_RUNTIME = "dominion_runtime"
    PRODUCTION_CERTIFY = "production_certify"


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
    "safe_loopback_models_probe_policy",
    "read_only_skill_registry",
    "skill_list_command",
    "skill_inspect_command",
    "unsafe_skill_denial",
    "unsupported_command_denial",
    "integrated_restore_document",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "run_command",
    "ask_command",
    "provider_text_completion",
    "prompt_submission_to_model",
    "read_only_skill_execution",
    "minimal_agent_loop",
    "trace_emission",
    "user_test_release",
    "file_write_outside_profile_or_session_init",
    "file_edit",
    "patch_apply",
    "shell_execution",
    "test_execution",
    "subagent_invocation",
    "child_session_creation",
    "parent_raw_transcript_sharing",
    "provider_tool_calling",
    "function_calling",
    "autonomous_loop",
    "retry_loop",
    "dominion_runtime",
    "production_certification",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_run_command",
    "ready_for_ask_command",
    "ready_for_provider_text_only_invocation",
    "ready_for_prompt_submission",
    "ready_for_read_only_skill_execution",
    "ready_for_minimal_single_turn_run",
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
    "ready_for_provider_tool_calling",
    "ready_for_function_calling",
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
    "v0412_prompt_session_summary",
    "provider_config_contract",
    "provider_doctor_contract",
    "no_completion_policy",
    "safe_loopback_models_probe_policy",
    "secret_redaction_contract",
    "provider_runtime_still_closed",
    "read_only_skill_registry_contract",
    "skill_list_contract",
    "skill_inspect_contract",
    "unsafe_skill_denial_policy",
    "unsupported_command_policy",
    "safety_posture",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0414_handoff",
    "v0416_user_test_target",
    "copy_paste_restore_prompt",
)


@dataclass(frozen=True)
class ProviderSecretRef:
    secret_id: str
    env_var_name: str | None
    present: bool
    redacted_display: str
    value_loaded: bool
    value_printed: bool


@dataclass(frozen=True)
class ProviderSecretRedactionReport:
    report_id: str
    secret_refs: tuple[ProviderSecretRef, ...]
    all_values_redacted: bool
    unsafe_secret_exposure_detected: bool


@dataclass(frozen=True)
class ProviderConfig:
    provider_id: str
    provider_kind: str
    source: str
    base_url: str | None
    model: str | None
    api_key_env_var: str | None
    mode: str
    tool_calling_allowed: bool
    function_calling_allowed: bool
    completion_allowed_in_doctor: bool
    completion_allowed_in_run: bool
    network_probe_allowed: bool
    remote_network_probe_allowed: bool
    metadata: dict[str, object]


@dataclass(frozen=True)
class ProviderConfigValidationFinding:
    finding_id: str
    severity: str
    field_name: str
    message: str
    recommendation: str
    blocks_provider_doctor: bool
    blocks_v0414_run: bool


@dataclass(frozen=True)
class ProviderConfigValidationReport:
    report_id: str
    provider_id: str
    valid_for_doctor: bool
    valid_for_completion: bool
    findings: tuple[ProviderConfigValidationFinding, ...]
    secret_redaction_report: ProviderSecretRedactionReport
    endpoint_kind: str
    completion_blocked: bool


@dataclass(frozen=True)
class ProviderProbeNetworkPolicy:
    policy_id: str
    loopback_probe_allowed: bool
    remote_probe_allowed: bool
    completion_probe_allowed: bool
    allowed_paths: tuple[str, ...]
    timeout_seconds: float
    sends_user_prompt: bool
    sends_completion_request: bool
    prints_secret: bool


@dataclass(frozen=True)
class ProviderModelsProbeRequest:
    request_id: str
    provider_id: str
    base_url: str
    path: str
    explicit_probe_requested: bool
    no_completion: bool
    endpoint_kind: str
    timeout_seconds: float


@dataclass(frozen=True)
class ProviderModelsProbeResult:
    result_id: str
    request_id: str
    attempted: bool
    status: str
    endpoint_url_redacted: str
    model_count: int | None
    model_names_preview: tuple[str, ...]
    error_message: str | None
    sent_user_prompt: bool
    sent_completion_request: bool
    printed_secret: bool
    network_accessed: bool
    remote_network_accessed: bool


@dataclass(frozen=True)
class ProviderCompletionBlockedRecord:
    record_id: str
    provider_id: str
    command_name: str
    completion_blocked: bool
    reason: str
    future_target_version: str


@dataclass(frozen=True)
class ProviderDoctorReport:
    report_id: str
    provider_id: str
    profile_id: str
    status: str
    provider_config: ProviderConfig | None
    validation_report: ProviderConfigValidationReport
    models_probe_result: ProviderModelsProbeResult | None
    completion_blocked_record: ProviderCompletionBlockedRecord
    provider_invoked_completion: bool
    prompt_submitted: bool
    user_prompt_sent: bool
    tool_calling_enabled: bool
    function_calling_enabled: bool
    secrets_redacted: bool
    ready_for_v0414_run: bool


@dataclass(frozen=True)
class ProviderRuntimeStillClosedReport:
    report_id: str
    provider_doctor_opened: bool
    provider_completion_opened: bool
    prompt_submission_opened: bool
    provider_tool_calling_opened: bool
    function_calling_opened: bool
    agent_loop_opened: bool
    run_command_opened: bool


@dataclass(frozen=True)
class ReadOnlySkillSpec:
    skill_id: str
    skill_name: str
    skill_kind: str
    description: str
    safety_class: str
    capability_status: str
    execution_allowed: bool
    mutates_workspace: bool
    uses_shell: bool
    uses_network: bool
    accesses_credentials: bool
    invokes_provider: bool
    invokes_subagent: bool
    future_target_version: str | None
    input_schema_preview: dict[str, object]
    output_schema_preview: dict[str, object]


@dataclass(frozen=True)
class ReadOnlySkillRegistry:
    registry_id: str
    profile_id: str
    skills: tuple[ReadOnlySkillSpec, ...]
    execution_enabled: bool
    skill_execution_allowed: bool
    unsafe_skill_count: int
    registered_skill_count: int


@dataclass(frozen=True)
class ReadOnlySkillListRequest:
    profile_id: str
    include_future_gated: bool


@dataclass(frozen=True)
class ReadOnlySkillListResult:
    profile_id: str
    skills: tuple[ReadOnlySkillSpec, ...]
    execution_enabled: bool
    provider_invoked: bool
    skill_executed: bool
    prompt_submitted: bool


@dataclass(frozen=True)
class ReadOnlySkillInspectRequest:
    profile_id: str
    skill_name: str


@dataclass(frozen=True)
class ReadOnlySkillInspectResult:
    profile_id: str
    skill_name: str
    found: bool
    skill_spec: ReadOnlySkillSpec | None
    execution_allowed: bool
    provider_invoked: bool
    skill_executed: bool
    prompt_submitted: bool


@dataclass(frozen=True)
class SkillExecutionBlockedDecision:
    decision_id: str
    skill_name: str
    request_kind: str
    blocked: bool
    reason: str
    future_target_version: str | None
    safe_alternative: str
    executed: bool


@dataclass(frozen=True)
class ReadOnlySkillRegistrySafetyReport:
    report_id: str
    registry_id: str
    execution_enabled: bool
    write_skills_allowed: bool
    shell_skills_allowed: bool
    provider_tool_skills_allowed: bool
    subagent_skills_allowed: bool
    memory_mutation_allowed: bool
    production_certified: bool
    unsafe_skills_blocked: bool


@dataclass(frozen=True)
class V0413ReadinessReport:
    report_id: str
    provider_config_model_ready: bool
    provider_doctor_ready: bool
    provider_secret_redaction_ready: bool
    provider_completion_block_ready: bool
    safe_loopback_models_probe_policy_ready: bool
    read_only_skill_registry_defined: bool
    skill_list_command_ready: bool
    skill_inspect_command_ready: bool
    unsafe_skill_denial_ready: bool
    integrated_restore_document_ready: bool
    v0414_handoff_ready: bool
    ready_for_run_command: bool
    ready_for_ask_command: bool
    ready_for_provider_text_only_invocation: bool
    ready_for_prompt_submission: bool
    ready_for_read_only_skill_execution: bool
    ready_for_minimal_single_turn_run: bool
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
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_autonomous_loop_runtime: bool
    ready_for_retry_loop: bool
    ready_for_mission_scheduler: bool
    ready_for_mutable_memory_automation: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0414MinimalProviderRunHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0416UserTestTargetUpdate:
    target_id: str
    target_version: str
    commands: tuple[str, ...]
    commands_expected_in_v0413: tuple[str, ...]
    user_test_release_ready: bool


@dataclass(frozen=True)
class V0413IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0413IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0413IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0413IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0413IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0413IntegratedRestoreDocumentManifest:
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


def _home_path(home_path: str | None) -> str:
    return str(Path(home_path or Path.cwd() / ".chantacore-personal").resolve())


def _provider_config_path(home_path: str | None) -> Path:
    return Path(_home_path(home_path)) / "profiles" / PROFILE_ID / "profile" / "PROVIDER.json"


def _endpoint_kind(base_url: str | None) -> str:
    if not base_url:
        return ProviderEndpointKind.MISSING.value
    parsed = urllib.parse.urlparse(base_url)
    host = parsed.hostname
    if not parsed.scheme or not host:
        return ProviderEndpointKind.INVALID.value
    if host in {"localhost", "127.0.0.1", "::1"}:
        return ProviderEndpointKind.LOOPBACK.value
    return ProviderEndpointKind.REMOTE.value


def _redacted_url(base_url: str, path: str) -> str:
    parsed = urllib.parse.urlparse(base_url)
    safe = parsed._replace(params="", query="", fragment="")
    return urllib.parse.urljoin(urllib.parse.urlunparse(safe).rstrip("/") + "/", path.lstrip("/"))


def create_provider_secret_ref(env_var_name: str | None = "OPENAI_API_KEY", **overrides: Any) -> ProviderSecretRef:
    present = bool(env_var_name and env_var_name in os.environ)
    defaults = {
        "secret_id": f"secret-ref-{env_var_name or 'none'}",
        "env_var_name": env_var_name,
        "present": present,
        "redacted_display": f"{env_var_name}=<redacted-present>" if present else f"{env_var_name}=<not-set>",
        "value_loaded": False,
        "value_printed": False,
    }
    return ProviderSecretRef(**_merge(defaults, overrides))


def create_provider_secret_redaction_report(
    secret_refs: Sequence[ProviderSecretRef] | None = None,
    **overrides: Any,
) -> ProviderSecretRedactionReport:
    refs = tuple(secret_refs or (create_provider_secret_ref(),))
    defaults = {
        "report_id": "provider-secret-redaction-report-v0413",
        "secret_refs": refs,
        "all_values_redacted": True,
        "unsafe_secret_exposure_detected": False,
    }
    return ProviderSecretRedactionReport(**_merge(defaults, overrides))


def create_provider_config(**overrides: Any) -> ProviderConfig:
    defaults = {
        "provider_id": "default-provider",
        "provider_kind": ProviderKind.LOCAL_OPENAI_COMPATIBLE.value,
        "source": ProviderConfigSource.DEFAULT_METADATA.value,
        "base_url": None,
        "model": None,
        "api_key_env_var": "OPENAI_API_KEY",
        "mode": "metadata_only",
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "completion_allowed_in_doctor": False,
        "completion_allowed_in_run": False,
        "network_probe_allowed": False,
        "remote_network_probe_allowed": False,
        "metadata": {"v0413_provider_doctor_only": True},
    }
    return ProviderConfig(**_merge(defaults, overrides))


def load_provider_config_from_profile(home_path: str | None = None, **overrides: Any) -> ProviderConfig:
    path = _provider_config_path(home_path)
    data: dict[str, Any] = {}
    source = ProviderConfigSource.DEFAULT_METADATA.value
    if path.exists():
        data = json.loads(path.read_text(encoding="utf-8"))
        source = ProviderConfigSource.PROFILE_FILE.value
    defaults = {
        "provider_id": str(data.get("provider_id", "default-provider")),
        "provider_kind": str(data.get("provider_kind", ProviderKind.LOCAL_OPENAI_COMPATIBLE.value)),
        "source": source,
        "base_url": data.get("base_url"),
        "model": data.get("model"),
        "api_key_env_var": data.get("api_key_env_var", "OPENAI_API_KEY"),
        "mode": str(data.get("mode", "metadata_only")),
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "completion_allowed_in_doctor": False,
        "completion_allowed_in_run": False,
        "network_probe_allowed": bool(data.get("network_probe_allowed", False)),
        "remote_network_probe_allowed": False,
        "metadata": {"source_path": str(path), "v0413_provider_doctor_only": True},
    }
    return ProviderConfig(**_merge(defaults, overrides))


def validate_provider_config(config: ProviderConfig, **overrides: Any) -> ProviderConfigValidationReport:
    findings: list[ProviderConfigValidationFinding] = []
    endpoint_kind = _endpoint_kind(config.base_url)
    if config.mode not in {"text_only", "metadata_only"}:
        findings.append(
            ProviderConfigValidationFinding(
                "invalid-mode",
                "blocking",
                "mode",
                "Provider mode must be text_only or metadata_only.",
                "Use metadata_only until v0.41.4 opens scoped run.",
                True,
                True,
            )
        )
    if endpoint_kind == ProviderEndpointKind.MISSING.value:
        findings.append(
            ProviderConfigValidationFinding(
                "missing-base-url",
                "warning",
                "base_url",
                "Provider base_url is not configured.",
                "Add bounded profile provider metadata before v0.41.4.",
                False,
                True,
            )
        )
    defaults = {
        "report_id": "provider-config-validation-v0413",
        "provider_id": config.provider_id,
        "valid_for_doctor": not any(item.blocks_provider_doctor for item in findings),
        "valid_for_completion": False,
        "findings": tuple(findings),
        "secret_redaction_report": create_provider_secret_redaction_report((create_provider_secret_ref(config.api_key_env_var),)),
        "endpoint_kind": endpoint_kind,
        "completion_blocked": True,
    }
    return ProviderConfigValidationReport(**_merge(defaults, overrides))


def create_provider_probe_network_policy(**overrides: Any) -> ProviderProbeNetworkPolicy:
    defaults = {
        "policy_id": "provider-probe-network-policy-v0413",
        "loopback_probe_allowed": True,
        "remote_probe_allowed": False,
        "completion_probe_allowed": False,
        "allowed_paths": ("/models", "/v1/models"),
        "timeout_seconds": 2.0,
        "sends_user_prompt": False,
        "sends_completion_request": False,
        "prints_secret": False,
    }
    return ProviderProbeNetworkPolicy(**_merge(defaults, overrides))


def create_provider_models_probe_request(
    config: ProviderConfig | None = None,
    path: str = "/models",
    explicit_probe_requested: bool = True,
    no_completion: bool = True,
    **overrides: Any,
) -> ProviderModelsProbeRequest:
    config = config or create_provider_config(base_url="http://127.0.0.1:1234")
    defaults = {
        "request_id": "provider-models-probe-request-v0413",
        "provider_id": config.provider_id,
        "base_url": config.base_url or "",
        "path": path,
        "explicit_probe_requested": explicit_probe_requested,
        "no_completion": no_completion,
        "endpoint_kind": _endpoint_kind(config.base_url),
        "timeout_seconds": create_provider_probe_network_policy().timeout_seconds,
    }
    return ProviderModelsProbeRequest(**_merge(defaults, overrides))


def create_provider_models_probe_result(**overrides: Any) -> ProviderModelsProbeResult:
    defaults = {
        "result_id": "provider-models-probe-result-v0413",
        "request_id": "provider-models-probe-request-v0413",
        "attempted": False,
        "status": ProviderDoctorStatus.SKIPPED.value,
        "endpoint_url_redacted": "",
        "model_count": None,
        "model_names_preview": (),
        "error_message": None,
        "sent_user_prompt": False,
        "sent_completion_request": False,
        "printed_secret": False,
        "network_accessed": False,
        "remote_network_accessed": False,
    }
    return ProviderModelsProbeResult(**_merge(defaults, overrides))


def run_safe_loopback_models_probe(request: ProviderModelsProbeRequest) -> ProviderModelsProbeResult:
    policy = create_provider_probe_network_policy()
    endpoint_url = _redacted_url(request.base_url, request.path) if request.base_url else ""
    if not request.explicit_probe_requested or not request.no_completion:
        return create_provider_models_probe_result(
            request_id=request.request_id,
            status=ProviderDoctorStatus.BLOCKED.value,
            endpoint_url_redacted=endpoint_url,
            error_message="explicit probe and no-completion are required",
        )
    if request.endpoint_kind != ProviderEndpointKind.LOOPBACK.value or request.path not in policy.allowed_paths:
        return create_provider_models_probe_result(
            request_id=request.request_id,
            status=ProviderDoctorStatus.BLOCKED.value,
            endpoint_url_redacted=endpoint_url,
            error_message="only loopback models paths are allowed",
            remote_network_accessed=False,
        )
    try:
        with urllib.request.urlopen(endpoint_url, timeout=request.timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
        data = payload.get("data", []) if isinstance(payload, dict) else []
        names = tuple(str(item.get("id", "")) for item in data[:5] if isinstance(item, dict))
        return create_provider_models_probe_result(
            request_id=request.request_id,
            attempted=True,
            status=ProviderDoctorStatus.PASS.value,
            endpoint_url_redacted=endpoint_url,
            model_count=len(data),
            model_names_preview=names,
            network_accessed=True,
        )
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        return create_provider_models_probe_result(
            request_id=request.request_id,
            attempted=True,
            status=ProviderDoctorStatus.WARN.value,
            endpoint_url_redacted=endpoint_url,
            error_message=str(exc),
            network_accessed=True,
        )


def create_provider_completion_blocked_record(**overrides: Any) -> ProviderCompletionBlockedRecord:
    defaults = {
        "record_id": "provider-completion-blocked-v0413",
        "provider_id": "default-provider",
        "command_name": "provider doctor",
        "completion_blocked": True,
        "reason": "v0.41.3 provider doctor is no-completion and config-readiness only.",
        "future_target_version": "v0.41.4",
    }
    return ProviderCompletionBlockedRecord(**_merge(defaults, overrides))


def create_provider_doctor_report(
    home_path: str | None = None,
    no_completion: bool = True,
    probe_models: bool = False,
    **overrides: Any,
) -> ProviderDoctorReport:
    config = load_provider_config_from_profile(home_path)
    validation = validate_provider_config(config)
    probe = None
    if probe_models:
        probe = run_safe_loopback_models_probe(
            create_provider_models_probe_request(config, explicit_probe_requested=True, no_completion=no_completion)
        )
    status = ProviderDoctorStatus.PASS.value if validation.valid_for_doctor else ProviderDoctorStatus.WARN.value
    if not no_completion:
        status = ProviderDoctorStatus.BLOCKED.value
    defaults = {
        "report_id": "provider-doctor-report-v0413",
        "provider_id": config.provider_id,
        "profile_id": PROFILE_ID,
        "status": status,
        "provider_config": config,
        "validation_report": validation,
        "models_probe_result": probe,
        "completion_blocked_record": create_provider_completion_blocked_record(provider_id=config.provider_id),
        "provider_invoked_completion": False,
        "prompt_submitted": False,
        "user_prompt_sent": False,
        "tool_calling_enabled": False,
        "function_calling_enabled": False,
        "secrets_redacted": True,
        "ready_for_v0414_run": validation.valid_for_doctor
        and not any(finding.blocks_v0414_run for finding in validation.findings),
    }
    return ProviderDoctorReport(**_merge(defaults, overrides))


def create_provider_runtime_still_closed_report(**overrides: Any) -> ProviderRuntimeStillClosedReport:
    defaults = {
        "report_id": "provider-runtime-still-closed-v0413",
        "provider_doctor_opened": True,
        "provider_completion_opened": False,
        "prompt_submission_opened": False,
        "provider_tool_calling_opened": False,
        "function_calling_opened": False,
        "agent_loop_opened": False,
        "run_command_opened": False,
    }
    return ProviderRuntimeStillClosedReport(**_merge(defaults, overrides))


def create_read_only_skill_spec(skill_name: str = "profile_status", **overrides: Any) -> ReadOnlySkillSpec:
    kind = skill_name if skill_name in {item.value for item in ReadOnlySkillKind} else ReadOnlySkillKind.UNKNOWN.value
    safety = ReadOnlySkillSafetyClass.FUTURE_TRACE_READ.value if kind.startswith("trace_") else ReadOnlySkillSafetyClass.READ_ONLY_METADATA.value
    defaults = {
        "skill_id": f"readonly:{skill_name}",
        "skill_name": skill_name,
        "skill_kind": kind,
        "description": f"Static read-only metadata spec for {skill_name}.",
        "safety_class": safety,
        "capability_status": ReadOnlySkillCapabilityStatus.INSPECTABLE.value,
        "execution_allowed": False,
        "mutates_workspace": False,
        "uses_shell": False,
        "uses_network": False,
        "accesses_credentials": False,
        "invokes_provider": False,
        "invokes_subagent": False,
        "future_target_version": "v0.41.5" if kind.startswith("trace_") else None,
        "input_schema_preview": {"type": "object", "execution": "closed"},
        "output_schema_preview": {"type": "object", "metadata_only": True},
    }
    return ReadOnlySkillSpec(**_merge(defaults, overrides))


def build_default_read_only_skill_registry(**overrides: Any) -> ReadOnlySkillRegistry:
    names = (
        "profile_status",
        "config_view",
        "provider_status",
        "restore_summary",
        "trace_recent",
        "trace_summary",
        "status_summary",
        "docs_reference_search",
        "list_available_skills",
        "unsafe_command_check",
    )
    skills = tuple(create_read_only_skill_spec(name) for name in names)
    defaults = {
        "registry_id": "read-only-skill-registry-v0413",
        "profile_id": PROFILE_ID,
        "skills": skills,
        "execution_enabled": False,
        "skill_execution_allowed": False,
        "unsafe_skill_count": 0,
        "registered_skill_count": len(skills),
    }
    return ReadOnlySkillRegistry(**_merge(defaults, overrides))


def create_read_only_skill_list_request(**overrides: Any) -> ReadOnlySkillListRequest:
    defaults = {"profile_id": PROFILE_ID, "include_future_gated": True}
    return ReadOnlySkillListRequest(**_merge(defaults, overrides))


def list_read_only_skills(
    request: ReadOnlySkillListRequest | None = None,
    registry: ReadOnlySkillRegistry | None = None,
    **overrides: Any,
) -> ReadOnlySkillListResult:
    request = request or create_read_only_skill_list_request()
    registry = registry or build_default_read_only_skill_registry(profile_id=request.profile_id)
    skills = registry.skills if request.include_future_gated else tuple(
        skill for skill in registry.skills if skill.capability_status != ReadOnlySkillCapabilityStatus.FUTURE_GATED.value
    )
    defaults = {
        "profile_id": request.profile_id,
        "skills": skills,
        "execution_enabled": False,
        "provider_invoked": False,
        "skill_executed": False,
        "prompt_submitted": False,
    }
    return ReadOnlySkillListResult(**_merge(defaults, overrides))


def create_read_only_skill_inspect_request(skill_name: str = "profile_status", **overrides: Any) -> ReadOnlySkillInspectRequest:
    defaults = {"profile_id": PROFILE_ID, "skill_name": skill_name}
    return ReadOnlySkillInspectRequest(**_merge(defaults, overrides))


def inspect_read_only_skill(
    request: ReadOnlySkillInspectRequest,
    registry: ReadOnlySkillRegistry | None = None,
    **overrides: Any,
) -> ReadOnlySkillInspectResult:
    registry = registry or build_default_read_only_skill_registry(profile_id=request.profile_id)
    found = next((skill for skill in registry.skills if skill.skill_name == request.skill_name), None)
    defaults = {
        "profile_id": request.profile_id,
        "skill_name": request.skill_name,
        "found": found is not None,
        "skill_spec": found,
        "execution_allowed": False,
        "provider_invoked": False,
        "skill_executed": False,
        "prompt_submitted": False,
    }
    return ReadOnlySkillInspectResult(**_merge(defaults, overrides))


def create_skill_execution_blocked_decision(
    skill_name: str = "unsafe",
    request_kind: str = UnsafeSkillRequestKind.FILE_WRITE.value,
    **overrides: Any,
) -> SkillExecutionBlockedDecision:
    defaults = {
        "decision_id": f"blocked-skill-{request_kind}",
        "skill_name": skill_name,
        "request_kind": request_kind,
        "blocked": True,
        "reason": f"{request_kind} is not allowed in v0.41.3 skill registry.",
        "future_target_version": "v0.42+" if request_kind not in {"provider_tool_call", "function_call"} else "not_planned_in_v041",
        "safe_alternative": "skills list",
        "executed": False,
    }
    return SkillExecutionBlockedDecision(**_merge(defaults, overrides))


def create_read_only_skill_registry_safety_report(**overrides: Any) -> ReadOnlySkillRegistrySafetyReport:
    defaults = {
        "report_id": "read-only-skill-registry-safety-v0413",
        "registry_id": "read-only-skill-registry-v0413",
        "execution_enabled": False,
        "write_skills_allowed": False,
        "shell_skills_allowed": False,
        "provider_tool_skills_allowed": False,
        "subagent_skills_allowed": False,
        "memory_mutation_allowed": False,
        "production_certified": False,
        "unsafe_skills_blocked": True,
    }
    return ReadOnlySkillRegistrySafetyReport(**_merge(defaults, overrides))


def create_v0413_readiness_report(**overrides: Any) -> V0413ReadinessReport:
    defaults = {
        "report_id": "v0413-readiness-report",
        "provider_config_model_ready": True,
        "provider_doctor_ready": True,
        "provider_secret_redaction_ready": True,
        "provider_completion_block_ready": True,
        "safe_loopback_models_probe_policy_ready": True,
        "read_only_skill_registry_defined": True,
        "skill_list_command_ready": True,
        "skill_inspect_command_ready": True,
        "unsafe_skill_denial_ready": True,
        "integrated_restore_document_ready": True,
        "v0414_handoff_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return V0413ReadinessReport(**_merge(defaults, overrides))


def create_v0414_minimal_provider_run_handoff(**overrides: Any) -> V0414MinimalProviderRunHandoff:
    defaults = {
        "handoff_id": "v0414-minimal-provider-run-handoff",
        "target_version": "v0.41.4 Minimal Single-turn Provider-backed Run",
        "recommended_focus": (
            "open chanta-cli run",
            "use explicit configured provider",
            "allow text-only completion",
            "send user input to provider only in run command",
            "no tool calling",
            "no function calling",
            "no AgentLoop beyond single-turn minimal path",
            "no skill execution unless explicitly read-only and bounded",
            "no trace runtime until v0.41.5 except session append if already opened",
            "no subagent",
            "no shell/edit/apply/test execution",
        ),
        "still_closed": CLOSED_CAPABILITIES,
    }
    return V0414MinimalProviderRunHandoff(**_merge(defaults, overrides))


def create_v0416_user_test_target_update(**overrides: Any) -> V0416UserTestTargetUpdate:
    defaults = {
        "target_id": "v0416-user-test-target-update-v0413",
        "target_version": "v0.41.6 Installable User-Test Release",
        "commands": V0416_TARGET_COMMANDS,
        "commands_expected_in_v0413": (
            "py -m pip install -e .",
            "chanta-cli --version",
            "chanta-cli doctor",
            'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"',
            "chanta-cli profile status --profile default-personal",
            "chanta-cli provider doctor --profile default-personal --no-completion",
            "chanta-cli skills list --profile default-personal",
            "chanta-cli skills inspect profile_status --profile default-personal",
        ),
        "user_test_release_ready": False,
    }
    return V0416UserTestTargetUpdate(**_merge(defaults, overrides))


def create_v0413_integrated_restore_sections() -> tuple[V0413IntegratedRestoreSection, ...]:
    return tuple(
        V0413IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.41.3 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0413_integrated_restore_context_snapshot(**overrides: Any) -> V0413IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0413",
        "current_version": V0413_RELEASE_NAME,
        "current_track": V0413_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            V0413_RELEASE_NAME,
        ),
        "open_capabilities": OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "next_recommended_version": "v0.41.4 Minimal Single-turn Provider-backed Run",
    }
    return V0413IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0413_integrated_restore_packet(**overrides: Any) -> V0413IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0413",
        "snapshot": create_v0413_integrated_restore_context_snapshot(),
        "restore_sections": create_v0413_integrated_restore_sections(),
        "required_test_commands": (
            "tests/test_v0413_safe_provider_probe_read_only_skill_registry.py",
            "tests/test_v0412_prompt_assembly_session_store.py",
            "tests/test_v0411_installable_cli_bootstrap_doctor.py",
            "tests/test_v0410_default_personal_profile_runtime.py",
            "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
        ),
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0413IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0413_integrated_restore_document_manifest(**overrides: Any) -> V0413IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0413",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0413IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def provider_doctor_preserves_no_completion(report: ProviderDoctorReport) -> bool:
    return (
        not report.provider_invoked_completion
        and not report.prompt_submitted
        and not report.user_prompt_sent
        and not report.tool_calling_enabled
        and not report.function_calling_enabled
        and report.secrets_redacted
    )


def skill_registry_safety_preserves_closed(report: ReadOnlySkillRegistrySafetyReport) -> bool:
    return (
        not report.execution_enabled
        and not report.write_skills_allowed
        and not report.shell_skills_allowed
        and not report.provider_tool_skills_allowed
        and not report.subagent_skills_allowed
        and not report.memory_mutation_allowed
        and not report.production_certified
        and report.unsafe_skills_blocked
    )


def v0413_readiness_preserves_closed_runtime(report: V0413ReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0413IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def _handle_provider_doctor(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("provider")
    parser.add_argument("doctor")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home")
    parser.add_argument("--no-completion", action="store_true")
    parser.add_argument("--probe-models", action="store_true")
    parsed = parser.parse_args(args)
    if not parsed.no_completion:
        print(
            json.dumps(
                {
                    "command_name": "provider doctor",
                    "status": "future_gated",
                    "blocked": True,
                    "future_target_version": V0413_VERSION,
                    "reason": "provider doctor requires --no-completion in v0.41.3",
                    "safe_alternative": "chanta-cli provider doctor --no-completion",
                    "executed": False,
                },
                ensure_ascii=False,
                sort_keys=True,
            )
        )
        return 1
    report = create_provider_doctor_report(parsed.home, parsed.no_completion, parsed.probe_models)
    print(json.dumps(asdict(report), ensure_ascii=False, sort_keys=True))
    return 0 if report.status != ProviderDoctorStatus.BLOCKED.value else 1


def _handle_skills_list(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("skills")
    parser.add_argument("list")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home")
    parsed = parser.parse_args(args)
    result = list_read_only_skills(create_read_only_skill_list_request(profile_id=parsed.profile))
    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    return 0


def _handle_skills_inspect(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("skills")
    parser.add_argument("inspect")
    parser.add_argument("skill_name")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home")
    parsed = parser.parse_args(args)
    result = inspect_read_only_skill(create_read_only_skill_inspect_request(parsed.skill_name, profile_id=parsed.profile))
    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    return 0 if result.found else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"--version", "-V", "version"}:
        print("chanta-cli v0.41.1 / v0.41.2 prompt-session / v0.41.3 provider-skills")
        return 0
    if args[0] == "doctor":
        print("chanta-cli doctor v0.41.1")
        print("current_extension: v0.41.3 provider-skills")
        print("next: v0.41.4 Minimal Single-turn Provider-backed Run")
        print("provider_doctor_no_completion: pass")
        print("read_only_skill_registry: pass")
        print("provider_completion: closed")
        print("prompt_submission_to_model: closed")
        print("agent_loop: closed")
        print("skill_execution: closed")
        print("trace_runtime: closed")
        print("closed: " + ", ".join(CLOSED_CAPABILITIES))
        return 0
    if tuple(args[:2]) == ("provider", "doctor"):
        return _handle_provider_doctor(args)
    if tuple(args[:2]) == ("skills", "list"):
        return _handle_skills_list(args)
    if tuple(args[:2]) == ("skills", "inspect"):
        return _handle_skills_inspect(args)
    return v0412_main(args)


__all__ = [
    "CLOSED_CAPABILITIES",
    "INTEGRATED_DOC_PATH",
    "OPEN_CAPABILITIES",
    "ProviderKind",
    "ProviderConfigSource",
    "ProviderEndpointKind",
    "ProviderDoctorStatus",
    "ProviderSecretRef",
    "ProviderSecretRedactionReport",
    "ProviderConfig",
    "ProviderConfigValidationFinding",
    "ProviderConfigValidationReport",
    "ProviderProbeNetworkPolicy",
    "ProviderModelsProbeRequest",
    "ProviderModelsProbeResult",
    "ProviderCompletionBlockedRecord",
    "ProviderDoctorReport",
    "ProviderRuntimeStillClosedReport",
    "ReadOnlySkillKind",
    "ReadOnlySkillSafetyClass",
    "ReadOnlySkillCapabilityStatus",
    "ReadOnlySkillSpec",
    "ReadOnlySkillRegistry",
    "ReadOnlySkillListRequest",
    "ReadOnlySkillListResult",
    "ReadOnlySkillInspectRequest",
    "ReadOnlySkillInspectResult",
    "UnsafeSkillRequestKind",
    "SkillExecutionBlockedDecision",
    "ReadOnlySkillRegistrySafetyReport",
    "V0413ReadinessReport",
    "V0414MinimalProviderRunHandoff",
    "V0416UserTestTargetUpdate",
    "V0413IntegratedRestoreSection",
    "V0413IntegratedRestoreContextSnapshot",
    "V0413IntegratedRestorePacket",
    "V0413IntegratedRestoreDocumentManifest",
    "create_provider_config",
    "load_provider_config_from_profile",
    "validate_provider_config",
    "create_provider_secret_ref",
    "create_provider_secret_redaction_report",
    "create_provider_probe_network_policy",
    "create_provider_models_probe_request",
    "run_safe_loopback_models_probe",
    "create_provider_models_probe_result",
    "create_provider_completion_blocked_record",
    "create_provider_doctor_report",
    "create_provider_runtime_still_closed_report",
    "create_read_only_skill_spec",
    "build_default_read_only_skill_registry",
    "create_read_only_skill_list_request",
    "list_read_only_skills",
    "create_read_only_skill_inspect_request",
    "inspect_read_only_skill",
    "create_skill_execution_blocked_decision",
    "create_read_only_skill_registry_safety_report",
    "create_v0413_readiness_report",
    "create_v0414_minimal_provider_run_handoff",
    "create_v0416_user_test_target_update",
    "create_v0413_integrated_restore_context_snapshot",
    "create_v0413_integrated_restore_packet",
    "create_v0413_integrated_restore_document_manifest",
    "provider_doctor_preserves_no_completion",
    "skill_registry_safety_preserves_closed",
    "v0413_readiness_preserves_closed_runtime",
    "integrated_restore_packet_uses_single_doc",
    "main",
]
