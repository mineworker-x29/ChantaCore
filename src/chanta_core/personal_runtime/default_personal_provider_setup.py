"""v0.42.2 Provider Setup UX support.

This module configures provider metadata only. Provider setup/status/config-show
do not call providers, submit prompts, enable tools/functions, execute shell, or
certify production. Provider completion remains available only through the
existing run path.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass, is_dataclass, replace
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import PROFILE_ID
from chanta_core.personal_runtime.default_personal_home_quickstart import (
    create_v042_home_resolution_request,
    main as _v0421_main,
    resolve_v042_home,
)


V0422_VERSION = "v0.42.2"
V0422_RELEASE_NAME = "v0.42.2 Provider Setup UX"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.2_provider_setup_ux_restore.md"


class V042ProviderSetupMode(StrEnum):
    MOCK = "mock"
    LOCAL_OPENAI_COMPATIBLE = "local_openai_compatible"
    OPENAI_COMPATIBLE = "openai_compatible"
    STATUS_ONLY = "status_only"
    DRY_RUN = "dry_run"
    UNKNOWN = "unknown"


class V042ProviderSetupStatus(StrEnum):
    PASS = "pass"
    PASS_WITH_NOTES = "pass_with_notes"
    FAILED = "failed"
    BLOCKED = "blocked"
    CONFLICT = "conflict"
    DRY_RUN = "dry_run"
    NOT_CONFIGURED = "not_configured"
    INVALID = "invalid"


class V042ProviderProfileKind(StrEnum):
    DEFAULT_PERSONAL = "default_personal"
    TEST_FIXTURE = "test_fixture"
    CUSTOM_PERSONAL = "custom_personal"
    UNKNOWN = "unknown"


class V042ProviderPresetKind(StrEnum):
    MOCK = "mock"
    LOCAL_OPENAI_COMPATIBLE = "local_openai_compatible"
    LM_STUDIO_COMPATIBLE = "lm_studio_compatible"
    OPENAI_COMPATIBLE = "openai_compatible"
    UNKNOWN = "unknown"


class V042ProviderConfigFormat(StrEnum):
    JSON = "json"
    EXISTING_PROFILE_FORMAT = "existing_profile_format"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042ProviderConfigPathPolicy:
    policy_id: str
    profile_id: str
    config_filename: str
    relative_config_path: str
    bounded_to_home: bool
    write_outside_home_allowed: bool
    overwrite_existing_allowed: bool
    create_if_missing_allowed: bool
    stores_secret_values: bool


@dataclass(frozen=True)
class V042ProviderPreset:
    preset_id: str
    preset_kind: str
    display_name: str
    description: str
    provider_kind: str
    mode: str
    default_base_url: str | None
    requires_base_url: bool
    requires_model: bool
    requires_api_key_env: bool
    default_api_key_env_var: str | None
    tool_calling_allowed: bool
    function_calling_allowed: bool
    completion_allowed_in_doctor: bool
    completion_allowed_in_run: bool
    setup_calls_provider: bool
    status_calls_provider: bool


@dataclass(frozen=True)
class V042ProviderPresetRegistry:
    registry_id: str
    presets: tuple[V042ProviderPreset, ...]
    default_preset_kind: str
    supports_mock: bool
    supports_local_openai_compatible: bool
    supports_tool_calling: bool
    supports_function_calling: bool


@dataclass(frozen=True)
class V042ProviderConfigDraft:
    draft_id: str
    profile_id: str
    preset_kind: str
    provider_id: str
    provider_kind: str
    mode: str
    base_url: str | None
    model: str | None
    api_key_env_var: str | None
    tool_calling_allowed: bool
    function_calling_allowed: bool
    completion_allowed_in_doctor: bool
    completion_allowed_in_run: bool
    source: str
    metadata: dict[str, object]


@dataclass(frozen=True)
class V042ProviderConfigValidationFinding:
    finding_id: str
    severity: str
    field_name: str
    message: str
    recommendation: str
    blocks_setup: bool
    blocks_run_readiness: bool


@dataclass(frozen=True)
class V042ProviderConfigValidationReport:
    report_id: str
    draft_id: str
    valid_for_setup: bool
    valid_for_run_readiness: bool
    findings: tuple[V042ProviderConfigValidationFinding, ...]
    secret_values_detected: bool
    unsafe_capability_detected: bool


@dataclass(frozen=True)
class V042ProviderEnvSecretPolicy:
    policy_id: str
    stores_secret_values: bool
    stores_env_var_name_only: bool
    default_env_var_name: str | None
    checks_presence_without_loading_value: bool
    prints_secret_value: bool
    redacted_display_format: str


@dataclass(frozen=True)
class V042ProviderConfigWritePolicy:
    policy_id: str
    bounded_to_home: bool
    create_if_missing_allowed: bool
    overwrite_existing_allowed: bool
    replace_flag_supported: bool
    write_outside_home_allowed: bool
    backup_before_replace_required: bool
    dry_run_supported: bool


@dataclass(frozen=True)
class V042ProviderSetupRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    setup_mode: str
    preset_kind: str
    base_url: str | None
    model: str | None
    api_key_env_var: str | None
    dry_run: bool
    replace_existing: bool
    json_output: bool


@dataclass(frozen=True)
class V042ProviderSetupPlan:
    plan_id: str
    request: V042ProviderSetupRequest
    resolved_home_path: str
    config_path: str
    config_draft: V042ProviderConfigDraft
    validation_report: V042ProviderConfigValidationReport
    write_policy: V042ProviderConfigWritePolicy
    existing_config_present: bool
    existing_config_conflict: bool
    safe_to_execute: bool
    will_call_provider: bool
    will_print_secret: bool
    will_overwrite: bool
    outside_home_paths: tuple[str, ...]


@dataclass(frozen=True)
class V042ProviderConfigWriteResult:
    result_id: str
    config_path: str
    created: bool
    skipped_existing_identical: bool
    blocked_conflict: bool
    overwritten: bool
    dry_run: bool
    outside_home_paths: tuple[str, ...]
    wrote_secret_value: bool
    success: bool
    message: str


@dataclass(frozen=True)
class V042ProviderRunReadinessReport:
    report_id: str
    provider_kind: str
    provider_config_present: bool
    base_url_present: bool
    model_present: bool
    api_key_env_var_name_present: bool
    api_key_env_present: bool | None
    mock_run_ready: bool
    configured_provider_run_ready: bool
    provider_doctor_ready: bool
    completion_allowed_only_in_run: bool
    blocking_gaps: tuple[str, ...]
    next_action: str


@dataclass(frozen=True)
class V042ProviderSetupResult:
    result_id: str
    request_id: str
    profile_id: str
    resolved_home_path: str
    status: str
    config_path: str
    config_draft: V042ProviderConfigDraft
    validation_report: V042ProviderConfigValidationReport
    write_result: V042ProviderConfigWriteResult
    run_readiness_report: V042ProviderRunReadinessReport
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    real_provider_called: bool
    tool_calling_enabled: bool
    function_calling_enabled: bool
    secret_printed: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ProviderStatusRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    json_output: bool


@dataclass(frozen=True)
class V042ProviderStatusReport:
    report_id: str
    profile_id: str
    resolved_home_path: str
    config_path: str
    config_present: bool
    provider_id: str | None
    provider_kind: str | None
    mode: str | None
    base_url_display: str | None
    model: str | None
    api_key_env_var: str | None
    api_key_env_present: bool | None
    secret_redacted: bool
    ready_for_mock_run: bool
    ready_for_configured_provider_run: bool
    provider_doctor_no_completion_available: bool
    provider_doctor_completion_allowed: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    next_action: str
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ProviderConfigShowRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    json_output: bool
    include_sensitive: bool


@dataclass(frozen=True)
class V042ProviderConfigShowResult:
    result_id: str
    config_present: bool
    config_path: str
    redacted_config: dict[str, object]
    rendered_text: str
    secret_values_redacted: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ProviderDoctorUXInterpretation:
    interpretation_id: str
    provider_status_report: V042ProviderStatusReport
    doctor_status: str
    doctor_means_completion_ready: bool
    doctor_sends_completion: bool
    user_explanation: str
    next_recommended_command: str


@dataclass(frozen=True)
class V042ProviderTroubleshootingItem:
    item_id: str
    symptom: str
    likely_cause: str
    check_command: str
    recommended_fix: str
    target_command: str


@dataclass(frozen=True)
class V042ProviderUserGuideCommand:
    command_id: str
    order_index: int
    command_text: str
    purpose: str
    expected_output_summary: str
    safety_note: str


@dataclass(frozen=True)
class V042ProviderUserGuideSection:
    section_id: str
    title: str
    commands: tuple[V042ProviderUserGuideCommand, ...]
    notes: str


@dataclass(frozen=True)
class V042ProviderUXSafetyReport:
    report_id: str
    provider_setup_calls_provider: bool
    provider_status_calls_provider: bool
    provider_doctor_completion_closed: bool
    tool_calling_closed: bool
    function_calling_closed: bool
    shell_closed: bool
    subagent_closed: bool
    file_edit_closed: bool
    patch_apply_closed: bool
    stores_secret_values: bool
    prints_secret_values: bool
    production_certified: bool


@dataclass(frozen=True)
class V0422ReadinessReport:
    provider_preset_registry_ready: bool
    provider_setup_mock_ready: bool
    provider_setup_local_openai_ready: bool
    provider_status_command_ready: bool
    provider_config_show_command_ready: bool
    provider_setup_dry_run_ready: bool
    provider_config_write_ready: bool
    provider_secret_redaction_ready: bool
    provider_run_readiness_report_ready: bool
    provider_troubleshooting_ready: bool
    integrated_restore_document_ready: bool
    v0423_handoff_ready: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_provider_setup_real_network_call: bool
    ready_for_real_provider_wizard_that_calls_completion: bool
    ready_for_read_only_skill_execution_as_actions: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_subagent_invocation: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0423TraceHistoryUXHandoff:
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0422IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0422IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0422IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0422IntegratedRestoreContextSnapshot
    sections: tuple[V0422IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0422IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_ready(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, list):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


def _render_json(value: Any) -> str:
    return json.dumps(_json_ready(value), indent=2, sort_keys=True)


def _provider_config_relative_path(profile_id: str = PROFILE_ID) -> str:
    return f"profiles/{profile_id}/profile/PROVIDER.json"


def _provider_config_path(home_path: str, profile_id: str = PROFILE_ID) -> Path:
    return Path(home_path) / "profiles" / profile_id / "profile" / "PROVIDER.json"


def _profile_root(home_path: str, profile_id: str = PROFILE_ID) -> Path:
    return Path(home_path) / "profiles" / profile_id


def _is_under(path: Path, root: Path) -> bool:
    try:
        path.resolve(strict=False).relative_to(root.resolve(strict=False))
        return True
    except ValueError:
        return False


def _load_json(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))


def _draft_payload(draft: V042ProviderConfigDraft) -> dict[str, object]:
    return {
        "provider_id": draft.provider_id,
        "provider_kind": draft.provider_kind,
        "mode": draft.mode,
        "base_url": draft.base_url,
        "model": draft.model,
        "api_key_env_var": draft.api_key_env_var,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "completion_allowed_in_doctor": False,
        "completion_allowed_in_run": draft.completion_allowed_in_run,
        "network_probe_allowed": False,
        "remote_network_probe_allowed": False,
        "metadata": draft.metadata,
    }


def _redacted_config(data: Mapping[str, Any] | None) -> dict[str, object]:
    if not data:
        return {}
    redacted = dict(data)
    redacted.pop("api_key", None)
    redacted.pop("secret", None)
    redacted["secret_values"] = "<redacted>"
    return redacted


def create_v042_provider_config_path_policy(profile_id: str = PROFILE_ID, **overrides: Any) -> V042ProviderConfigPathPolicy:
    defaults = {
        "policy_id": "v0422-provider-config-path-policy",
        "profile_id": profile_id,
        "config_filename": "PROVIDER.json",
        "relative_config_path": _provider_config_relative_path(profile_id),
        "bounded_to_home": True,
        "write_outside_home_allowed": False,
        "overwrite_existing_allowed": False,
        "create_if_missing_allowed": True,
        "stores_secret_values": False,
    }
    return V042ProviderConfigPathPolicy(**_merge(defaults, overrides))


def create_v042_provider_preset(preset_kind: str = V042ProviderPresetKind.MOCK.value, **overrides: Any) -> V042ProviderPreset:
    if preset_kind == V042ProviderPresetKind.MOCK.value:
        defaults = {
            "preset_id": "v0422-provider-preset-mock",
            "preset_kind": V042ProviderPresetKind.MOCK.value,
            "display_name": "Mock provider",
            "description": "Deterministic local mock provider for default-personal testing.",
            "provider_kind": "mock",
            "mode": "mock",
            "default_base_url": None,
            "requires_base_url": False,
            "requires_model": False,
            "requires_api_key_env": False,
            "default_api_key_env_var": None,
            "tool_calling_allowed": False,
            "function_calling_allowed": False,
            "completion_allowed_in_doctor": False,
            "completion_allowed_in_run": True,
            "setup_calls_provider": False,
            "status_calls_provider": False,
        }
    else:
        defaults = {
            "preset_id": f"v0422-provider-preset-{preset_kind}",
            "preset_kind": preset_kind,
            "display_name": "Local OpenAI-compatible provider",
            "description": "Local text-only OpenAI-compatible endpoint metadata.",
            "provider_kind": "local_openai_compatible",
            "mode": "text_only",
            "default_base_url": "http://localhost:1234/v1",
            "requires_base_url": True,
            "requires_model": True,
            "requires_api_key_env": False,
            "default_api_key_env_var": None,
            "tool_calling_allowed": False,
            "function_calling_allowed": False,
            "completion_allowed_in_doctor": False,
            "completion_allowed_in_run": True,
            "setup_calls_provider": False,
            "status_calls_provider": False,
        }
        if preset_kind == V042ProviderPresetKind.LM_STUDIO_COMPATIBLE.value:
            defaults["display_name"] = "LM Studio compatible provider"
            defaults["provider_kind"] = "local_openai_compatible"
    return V042ProviderPreset(**_merge(defaults, overrides))


def build_v042_provider_preset_registry(**overrides: Any) -> V042ProviderPresetRegistry:
    presets = (
        create_v042_provider_preset(V042ProviderPresetKind.MOCK.value),
        create_v042_provider_preset(V042ProviderPresetKind.LOCAL_OPENAI_COMPATIBLE.value),
        create_v042_provider_preset(V042ProviderPresetKind.LM_STUDIO_COMPATIBLE.value),
    )
    defaults = {
        "registry_id": "v0422-provider-preset-registry",
        "presets": presets,
        "default_preset_kind": V042ProviderPresetKind.MOCK.value,
        "supports_mock": True,
        "supports_local_openai_compatible": True,
        "supports_tool_calling": False,
        "supports_function_calling": False,
    }
    return V042ProviderPresetRegistry(**_merge(defaults, overrides))


def create_v042_provider_config_draft(
    preset_kind: str = V042ProviderPresetKind.MOCK.value,
    profile_id: str = PROFILE_ID,
    base_url: str | None = None,
    model: str | None = None,
    api_key_env_var: str | None = None,
    **overrides: Any,
) -> V042ProviderConfigDraft:
    preset = create_v042_provider_preset(preset_kind)
    defaults = {
        "draft_id": "v0422-provider-config-draft",
        "profile_id": profile_id,
        "preset_kind": preset.preset_kind,
        "provider_id": "default-provider",
        "provider_kind": preset.provider_kind,
        "mode": preset.mode,
        "base_url": base_url,
        "model": model,
        "api_key_env_var": api_key_env_var,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "completion_allowed_in_doctor": False,
        "completion_allowed_in_run": bool(preset.completion_allowed_in_run),
        "source": "v0.42.2 provider setup UX",
        "metadata": {
            "config_format": V042ProviderConfigFormat.JSON.value,
            "preset_kind": preset.preset_kind,
            "stores_secret_values": False,
            "setup_calls_provider": False,
        },
    }
    return V042ProviderConfigDraft(**_merge(defaults, overrides))


def validate_v042_provider_config_draft(draft: V042ProviderConfigDraft, **overrides: Any) -> V042ProviderConfigValidationReport:
    findings: list[V042ProviderConfigValidationFinding] = []
    if draft.tool_calling_allowed or draft.function_calling_allowed or draft.completion_allowed_in_doctor:
        findings.append(
            V042ProviderConfigValidationFinding(
                "unsafe-provider-capability",
                "blocking",
                "capabilities",
                "Provider setup cannot enable doctor completion, tool calling, or function calling.",
                "Keep provider setup metadata-only and text-only.",
                True,
                True,
            )
        )
    if draft.preset_kind in {V042ProviderPresetKind.LOCAL_OPENAI_COMPATIBLE.value, V042ProviderPresetKind.LM_STUDIO_COMPATIBLE.value, V042ProviderPresetKind.OPENAI_COMPATIBLE.value}:
        if not draft.base_url:
            findings.append(
                V042ProviderConfigValidationFinding("missing-base-url", "blocking", "base_url", "base_url is required.", "Pass --base-url.", True, True)
            )
        if not draft.model:
            findings.append(
                V042ProviderConfigValidationFinding("missing-model", "blocking", "model", "model is required.", "Pass --model.", True, True)
            )
    secret_detected = False
    for value in (draft.api_key_env_var,):
        if value and ("sk-" in value.lower() or "secret" in value.lower() and value.upper() != value):
            secret_detected = True
            findings.append(
                V042ProviderConfigValidationFinding("secret-value-detected", "blocking", "api_key_env_var", "Potential secret value detected.", "Store only the environment variable name.", True, True)
            )
    unsafe = any(item.finding_id == "unsafe-provider-capability" for item in findings)
    defaults = {
        "report_id": "v0422-provider-config-validation-report",
        "draft_id": draft.draft_id,
        "valid_for_setup": not any(item.blocks_setup for item in findings),
        "valid_for_run_readiness": not any(item.blocks_run_readiness for item in findings),
        "findings": tuple(findings),
        "secret_values_detected": secret_detected,
        "unsafe_capability_detected": unsafe,
    }
    return V042ProviderConfigValidationReport(**_merge(defaults, overrides))


def create_v042_provider_env_secret_policy(default_env_var_name: str | None = "OPENAI_API_KEY", **overrides: Any) -> V042ProviderEnvSecretPolicy:
    defaults = {
        "policy_id": "v0422-provider-env-secret-policy",
        "stores_secret_values": False,
        "stores_env_var_name_only": True,
        "default_env_var_name": default_env_var_name,
        "checks_presence_without_loading_value": True,
        "prints_secret_value": False,
        "redacted_display_format": "{env_var}=<redacted-present|not-set>",
    }
    return V042ProviderEnvSecretPolicy(**_merge(defaults, overrides))


def create_v042_provider_config_write_policy(**overrides: Any) -> V042ProviderConfigWritePolicy:
    defaults = {
        "policy_id": "v0422-provider-config-write-policy",
        "bounded_to_home": True,
        "create_if_missing_allowed": True,
        "overwrite_existing_allowed": False,
        "replace_flag_supported": False,
        "write_outside_home_allowed": False,
        "backup_before_replace_required": False,
        "dry_run_supported": True,
    }
    return V042ProviderConfigWritePolicy(**_merge(defaults, overrides))


def create_v042_provider_setup_request(
    setup_mode: str = V042ProviderSetupMode.MOCK.value,
    home_path: str | None = None,
    profile_id: str = PROFILE_ID,
    preset_kind: str | None = None,
    base_url: str | None = None,
    model: str | None = None,
    api_key_env_var: str | None = None,
    dry_run: bool = False,
    replace_existing: bool = False,
    json_output: bool = False,
    **overrides: Any,
) -> V042ProviderSetupRequest:
    resolved_preset = preset_kind or (V042ProviderPresetKind.MOCK.value if setup_mode == V042ProviderSetupMode.MOCK.value else V042ProviderPresetKind.LOCAL_OPENAI_COMPATIBLE.value)
    defaults = {
        "request_id": "v0422-provider-setup-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "setup_mode": setup_mode,
        "preset_kind": resolved_preset,
        "base_url": base_url,
        "model": model,
        "api_key_env_var": api_key_env_var,
        "dry_run": dry_run,
        "replace_existing": replace_existing,
        "json_output": json_output,
    }
    return V042ProviderSetupRequest(**_merge(defaults, overrides))


def _resolve_home_path(home_path: str | None, command_name: str) -> str | None:
    resolved = resolve_v042_home(create_v042_home_resolution_request(explicit_home=home_path, command_name=command_name, allow_create=False, cwd=os.getcwd()))
    return resolved.home_path if resolved.safe_to_use else None


def create_v042_provider_setup_plan(request: V042ProviderSetupRequest, **overrides: Any) -> V042ProviderSetupPlan:
    home = _resolve_home_path(request.home_path, "provider setup") or ""
    config_path = _provider_config_path(home, request.profile_id) if home else Path("")
    draft = create_v042_provider_config_draft(request.preset_kind, request.profile_id, request.base_url, request.model, request.api_key_env_var)
    validation = validate_v042_provider_config_draft(draft)
    write_policy = create_v042_provider_config_write_policy()
    home_root = Path(home)
    outside = () if home and _is_under(config_path, home_root) else (str(config_path),)
    existing = _load_json(config_path) if config_path else None
    existing_present = existing is not None
    desired = _draft_payload(draft)
    conflict = bool(existing_present and existing != desired)
    profile_exists = bool(home and _profile_root(home, request.profile_id).exists())
    safe = bool(
        home
        and profile_exists
        and validation.valid_for_setup
        and not outside
        and not (conflict and not request.replace_existing)
        and not request.replace_existing
    )
    defaults = {
        "plan_id": "v0422-provider-setup-plan",
        "request": request,
        "resolved_home_path": home,
        "config_path": str(config_path),
        "config_draft": draft,
        "validation_report": validation,
        "write_policy": write_policy,
        "existing_config_present": existing_present,
        "existing_config_conflict": conflict,
        "safe_to_execute": safe,
        "will_call_provider": False,
        "will_print_secret": False,
        "will_overwrite": False,
        "outside_home_paths": tuple(outside),
    }
    return V042ProviderSetupPlan(**_merge(defaults, overrides))


def create_v042_provider_config_write_result(**overrides: Any) -> V042ProviderConfigWriteResult:
    defaults = {
        "result_id": "v0422-provider-config-write-result",
        "config_path": "",
        "created": False,
        "skipped_existing_identical": False,
        "blocked_conflict": False,
        "overwritten": False,
        "dry_run": False,
        "outside_home_paths": (),
        "wrote_secret_value": False,
        "success": False,
        "message": "not executed",
    }
    return V042ProviderConfigWriteResult(**_merge(defaults, overrides))


def execute_v042_provider_setup_plan(plan: V042ProviderSetupPlan) -> V042ProviderConfigWriteResult:
    payload = _draft_payload(plan.config_draft)
    path = Path(plan.config_path)
    if plan.request.dry_run:
        return create_v042_provider_config_write_result(
            config_path=plan.config_path,
            dry_run=True,
            success=plan.validation_report.valid_for_setup and not plan.outside_home_paths,
            message="dry run; provider config was not written",
        )
    if plan.outside_home_paths:
        return create_v042_provider_config_write_result(config_path=plan.config_path, outside_home_paths=plan.outside_home_paths, message="blocked outside home")
    if not plan.validation_report.valid_for_setup:
        return create_v042_provider_config_write_result(config_path=plan.config_path, message="blocked invalid provider config")
    existing = _load_json(path)
    if existing is not None:
        if existing == payload:
            return create_v042_provider_config_write_result(config_path=plan.config_path, skipped_existing_identical=True, success=True, message="existing provider config is identical")
        return create_v042_provider_config_write_result(config_path=plan.config_path, blocked_conflict=True, success=False, message="existing provider config differs; replacement is deferred")
    if not plan.safe_to_execute:
        return create_v042_provider_config_write_result(config_path=plan.config_path, message="blocked; run quickstart first or fix validation findings")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return create_v042_provider_config_write_result(config_path=plan.config_path, created=True, success=True, message="provider config written")


def create_v042_provider_run_readiness_report(
    draft: V042ProviderConfigDraft | None = None,
    config_present: bool = False,
    env: Mapping[str, str] | None = None,
    **overrides: Any,
) -> V042ProviderRunReadinessReport:
    env_map = os.environ if env is None else env
    provider_kind = draft.provider_kind if draft else "not_configured"
    base_url_present = bool(draft and draft.base_url)
    model_present = bool(draft and draft.model)
    api_name_present = bool(draft and draft.api_key_env_var)
    api_present = bool(draft.api_key_env_var in env_map) if draft and draft.api_key_env_var else None
    mock_ready = provider_kind == "mock" or not config_present
    configured_ready = bool(config_present and provider_kind != "mock" and base_url_present and model_present and (api_present is not False))
    gaps: list[str] = []
    if config_present and provider_kind != "mock":
        if not base_url_present:
            gaps.append("base_url_missing")
        if not model_present:
            gaps.append("model_missing")
        if api_present is False:
            gaps.append(f"{draft.api_key_env_var}_not_set")
    next_action = (
        "run chanta-cli run --profile default-personal --provider mock"
        if mock_ready and not configured_ready
        else "run chanta-cli provider doctor --profile default-personal --no-completion"
        if configured_ready
        else "run chanta-cli provider setup local-openai --base-url ... --model ..."
    )
    defaults = {
        "report_id": "v0422-provider-run-readiness-report",
        "provider_kind": provider_kind,
        "provider_config_present": config_present,
        "base_url_present": base_url_present,
        "model_present": model_present,
        "api_key_env_var_name_present": api_name_present,
        "api_key_env_present": api_present,
        "mock_run_ready": mock_ready,
        "configured_provider_run_ready": configured_ready,
        "provider_doctor_ready": bool(draft is None or provider_kind in {"mock", "local_openai_compatible", "openai_compatible"}),
        "completion_allowed_only_in_run": True,
        "blocking_gaps": tuple(gaps),
        "next_action": next_action,
    }
    return V042ProviderRunReadinessReport(**_merge(defaults, overrides))


def create_v042_provider_setup_result(plan: V042ProviderSetupPlan, write_result: V042ProviderConfigWriteResult | None = None, **overrides: Any) -> V042ProviderSetupResult:
    result = write_result or execute_v042_provider_setup_plan(plan)
    if plan.request.dry_run:
        status = V042ProviderSetupStatus.DRY_RUN.value
    elif result.blocked_conflict:
        status = V042ProviderSetupStatus.CONFLICT.value
    elif result.success:
        status = V042ProviderSetupStatus.PASS.value
    elif not plan.validation_report.valid_for_setup:
        status = V042ProviderSetupStatus.INVALID.value
    else:
        status = V042ProviderSetupStatus.BLOCKED.value
    readiness = create_v042_provider_run_readiness_report(plan.config_draft, config_present=result.success or plan.existing_config_present)
    defaults = {
        "result_id": "v0422-provider-setup-result",
        "request_id": plan.request.request_id,
        "profile_id": plan.request.profile_id,
        "resolved_home_path": plan.resolved_home_path,
        "status": status,
        "config_path": plan.config_path,
        "config_draft": plan.config_draft,
        "validation_report": plan.validation_report,
        "write_result": result,
        "run_readiness_report": readiness,
        "rendered_text": "",
        "provider_invoked": False,
        "prompt_submitted": False,
        "real_provider_called": False,
        "tool_calling_enabled": False,
        "function_calling_enabled": False,
        "secret_printed": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    setup_result = V042ProviderSetupResult(**_merge(defaults, overrides))
    return replace(setup_result, rendered_text=_render_provider_setup(setup_result) if not plan.request.json_output else _render_json(setup_result))


def create_v042_provider_status_request(home_path: str | None = None, profile_id: str = PROFILE_ID, json_output: bool = False, **overrides: Any) -> V042ProviderStatusRequest:
    defaults = {"request_id": "v0422-provider-status-request", "profile_id": profile_id, "home_path": home_path, "json_output": json_output}
    return V042ProviderStatusRequest(**_merge(defaults, overrides))


def _draft_from_config(data: Mapping[str, Any], profile_id: str = PROFILE_ID) -> V042ProviderConfigDraft:
    return create_v042_provider_config_draft(
        preset_kind=str(data.get("metadata", {}).get("preset_kind", data.get("provider_kind", V042ProviderPresetKind.LOCAL_OPENAI_COMPATIBLE.value))),
        profile_id=profile_id,
        base_url=data.get("base_url"),
        model=data.get("model"),
        api_key_env_var=data.get("api_key_env_var"),
        provider_id=str(data.get("provider_id", "default-provider")),
        provider_kind=str(data.get("provider_kind", "local_openai_compatible")),
        mode=str(data.get("mode", "text_only")),
        completion_allowed_in_run=bool(data.get("completion_allowed_in_run", True)),
    )


def create_v042_provider_status_report(request: V042ProviderStatusRequest, env: Mapping[str, str] | None = None, **overrides: Any) -> V042ProviderStatusReport:
    home = _resolve_home_path(request.home_path, "provider status") or ""
    config_path = _provider_config_path(home, request.profile_id) if home else Path("")
    data = _load_json(config_path) if config_path else None
    draft = _draft_from_config(data, request.profile_id) if data else None
    readiness = create_v042_provider_run_readiness_report(draft, config_present=bool(data), env=env)
    api_env = draft.api_key_env_var if draft else None
    api_present = bool(api_env in (os.environ if env is None else env)) if api_env else None
    next_action = readiness.next_action if data else "run chanta-cli provider setup mock or provider setup local-openai"
    defaults = {
        "report_id": "v0422-provider-status-report",
        "profile_id": request.profile_id,
        "resolved_home_path": home,
        "config_path": str(config_path),
        "config_present": bool(data),
        "provider_id": draft.provider_id if draft else None,
        "provider_kind": draft.provider_kind if draft else None,
        "mode": draft.mode if draft else None,
        "base_url_display": draft.base_url if draft and draft.base_url else None,
        "model": draft.model if draft else None,
        "api_key_env_var": api_env,
        "api_key_env_present": api_present,
        "secret_redacted": True,
        "ready_for_mock_run": readiness.mock_run_ready,
        "ready_for_configured_provider_run": readiness.configured_provider_run_ready,
        "provider_doctor_no_completion_available": True,
        "provider_doctor_completion_allowed": False,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "next_action": next_action,
        "rendered_text": "",
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    report = V042ProviderStatusReport(**_merge(defaults, overrides))
    return replace(report, rendered_text=_render_json(report) if request.json_output else _render_provider_status(report))


def create_v042_provider_config_show_request(
    home_path: str | None = None,
    profile_id: str = PROFILE_ID,
    json_output: bool = False,
    include_sensitive: bool = False,
    **overrides: Any,
) -> V042ProviderConfigShowRequest:
    defaults = {"request_id": "v0422-provider-config-show-request", "profile_id": profile_id, "home_path": home_path, "json_output": json_output, "include_sensitive": include_sensitive}
    return V042ProviderConfigShowRequest(**_merge(defaults, overrides))


def create_v042_provider_config_show_result(request: V042ProviderConfigShowRequest, **overrides: Any) -> V042ProviderConfigShowResult:
    home = _resolve_home_path(request.home_path, "provider config show") or ""
    config_path = _provider_config_path(home, request.profile_id) if home else Path("")
    data = _load_json(config_path) if config_path else None
    redacted = _redacted_config(data)
    defaults = {
        "result_id": "v0422-provider-config-show-result",
        "config_present": bool(data),
        "config_path": str(config_path),
        "redacted_config": redacted,
        "rendered_text": "",
        "secret_values_redacted": True,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    result = V042ProviderConfigShowResult(**_merge(defaults, overrides))
    return replace(result, rendered_text=_render_json(result if request.json_output else redacted) if request.json_output else _render_provider_config_show(result))


def create_v042_provider_doctor_ux_interpretation(status_report: V042ProviderStatusReport, doctor_status: str = "pass", **overrides: Any) -> V042ProviderDoctorUXInterpretation:
    defaults = {
        "interpretation_id": "v0422-provider-doctor-ux-interpretation",
        "provider_status_report": status_report,
        "doctor_status": doctor_status,
        "doctor_means_completion_ready": False,
        "doctor_sends_completion": False,
        "user_explanation": "provider doctor is a no-completion metadata/readiness check. Run readiness is reported separately.",
        "next_recommended_command": status_report.next_action,
    }
    return V042ProviderDoctorUXInterpretation(**_merge(defaults, overrides))


def create_v042_provider_troubleshooting_item(item_id: str, symptom: str, likely_cause: str, check_command: str, recommended_fix: str, target_command: str) -> V042ProviderTroubleshootingItem:
    return V042ProviderTroubleshootingItem(item_id, symptom, likely_cause, check_command, recommended_fix, target_command)


def build_v042_provider_troubleshooting_items() -> tuple[V042ProviderTroubleshootingItem, ...]:
    return (
        create_v042_provider_troubleshooting_item("missing-config", "Provider config missing", "provider setup has not been run", "chanta-cli provider status", "run provider setup mock or local-openai", "chanta-cli provider setup mock"),
        create_v042_provider_troubleshooting_item("missing-base-url", "base_url missing", "local provider metadata incomplete", "chanta-cli provider config show", "pass --base-url", "chanta-cli provider setup local-openai --base-url http://localhost:1234/v1 --model local-model"),
        create_v042_provider_troubleshooting_item("missing-model", "model missing", "local provider metadata incomplete", "chanta-cli provider config show", "pass --model", "chanta-cli provider setup local-openai --base-url http://localhost:1234/v1 --model local-model"),
        create_v042_provider_troubleshooting_item("openai-api-key-not-set", "OPENAI_API_KEY not set", "env var name is configured but absent", "chanta-cli provider status", "set the env var without storing it in config", "set OPENAI_API_KEY in the shell"),
        create_v042_provider_troubleshooting_item("lm-studio-server-not-running", "LM Studio server not running", "local server may be stopped", "chanta-cli provider doctor --profile default-personal --no-completion", "start LM Studio server", "chanta-cli provider setup local-openai --base-url http://localhost:1234/v1 --model local-model"),
        create_v042_provider_troubleshooting_item("mock-intentional", "Using mock provider intentionally", "mock setup selected", "chanta-cli provider status", "continue with mock run", "chanta-cli run --profile default-personal --provider mock \"Summarize what ChantaCore is in three bullets.\""),
        create_v042_provider_troubleshooting_item("doctor-passes-run-fails", "Provider doctor passes but run fails", "doctor does not send completion", "chanta-cli run-report last --profile default-personal", "check run readiness and provider server", "chanta-cli provider status"),
        create_v042_provider_troubleshooting_item("configured-provider-not-required", "Configured provider flow not required for mock testing", "mock flow is deterministic", "chanta-cli provider status", "use mock provider for local acceptance", "chanta-cli provider setup mock"),
    )


def create_v042_provider_user_guide_command(command_id: str, order_index: int, command_text: str, purpose: str, expected_output_summary: str, safety_note: str) -> V042ProviderUserGuideCommand:
    return V042ProviderUserGuideCommand(command_id, order_index, command_text, purpose, expected_output_summary, safety_note)


def create_v042_provider_user_guide_section(section_id: str, title: str, commands: tuple[V042ProviderUserGuideCommand, ...], notes: str) -> V042ProviderUserGuideSection:
    return V042ProviderUserGuideSection(section_id, title, commands, notes)


def build_v042_provider_user_guide_sections() -> tuple[V042ProviderUserGuideSection, ...]:
    commands = {
        "status": create_v042_provider_user_guide_command("provider-status", 1, "chanta-cli provider status", "Show provider state.", "Config presence and readiness.", "No provider call."),
        "setup-mock": create_v042_provider_user_guide_command("provider-setup-mock", 2, "chanta-cli provider setup mock", "Write mock config.", "Bounded config write.", "No real provider call."),
        "setup-local-dry": create_v042_provider_user_guide_command("provider-setup-local-dry-run", 3, "chanta-cli provider setup local-openai --base-url http://localhost:1234/v1 --model local-model --dry-run", "Preview local config.", "Dry-run report.", "No file write."),
        "setup-local": create_v042_provider_user_guide_command("provider-setup-local", 4, "chanta-cli provider setup local-openai --base-url http://localhost:1234/v1 --model local-model", "Write local config.", "Bounded config write.", "No provider call."),
        "config-show": create_v042_provider_user_guide_command("provider-config-show", 5, "chanta-cli provider config show", "Show redacted config.", "Redacted JSON.", "No secret value printed."),
        "doctor": create_v042_provider_user_guide_command("provider-doctor", 6, "chanta-cli provider doctor --profile default-personal --no-completion", "Check no-completion readiness.", "Doctor report.", "No completion."),
        "run-mock": create_v042_provider_user_guide_command("run-mock", 7, "chanta-cli run --profile default-personal --provider mock \"Summarize what ChantaCore is in three bullets.\"", "Run mock provider.", "Mock response and trace.", "Mock only."),
        "run-configured": create_v042_provider_user_guide_command("run-configured", 8, "chanta-cli run --profile default-personal \"Summarize what ChantaCore is in three bullets.\"", "Run configured provider.", "Text-only run.", "Completion only in run."),
    }
    return (
        create_v042_provider_user_guide_section("current-provider-status", "Current Provider Status", (commands["status"],), "Start here."),
        create_v042_provider_user_guide_section("mock-provider-setup", "Mock Provider Setup", (commands["setup-mock"], commands["run-mock"]), "Mock is deterministic."),
        create_v042_provider_user_guide_section("local-openai-compatible-provider-setup", "Local OpenAI-compatible Provider Setup", (commands["setup-local-dry"], commands["setup-local"], commands["config-show"]), "Setup writes metadata only."),
        create_v042_provider_user_guide_section("provider-doctor", "Provider Doctor", (commands["doctor"],), "Doctor remains no-completion."),
        create_v042_provider_user_guide_section("running-with-mock-provider", "Running with Mock Provider", (commands["run-mock"],), "Mock remains available."),
        create_v042_provider_user_guide_section("running-with-configured-provider", "Running with Configured Provider", (commands["run-configured"],), "Real completion is only in run."),
        create_v042_provider_user_guide_section("troubleshooting", "Troubleshooting", (commands["status"], commands["config-show"]), "Use status and redacted config."),
        create_v042_provider_user_guide_section("what-provider-setup-does-not-do", "What Provider Setup Does Not Do", (), "No provider call, no completion, no tools, no functions, no shell."),
    )


def create_v042_provider_ux_safety_report(**overrides: Any) -> V042ProviderUXSafetyReport:
    defaults = {
        "report_id": "v0422-provider-ux-safety-report",
        "provider_setup_calls_provider": False,
        "provider_status_calls_provider": False,
        "provider_doctor_completion_closed": True,
        "tool_calling_closed": True,
        "function_calling_closed": True,
        "shell_closed": True,
        "subagent_closed": True,
        "file_edit_closed": True,
        "patch_apply_closed": True,
        "stores_secret_values": False,
        "prints_secret_values": False,
        "production_certified": False,
    }
    return V042ProviderUXSafetyReport(**_merge(defaults, overrides))


def create_v0422_readiness_report(**overrides: Any) -> V0422ReadinessReport:
    defaults = {
        "provider_preset_registry_ready": True,
        "provider_setup_mock_ready": True,
        "provider_setup_local_openai_ready": True,
        "provider_status_command_ready": True,
        "provider_config_show_command_ready": True,
        "provider_setup_dry_run_ready": True,
        "provider_config_write_ready": True,
        "provider_secret_redaction_ready": True,
        "provider_run_readiness_report_ready": True,
        "provider_troubleshooting_ready": True,
        "integrated_restore_document_ready": True,
        "v0423_handoff_ready": True,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_provider_setup_real_network_call": False,
        "ready_for_real_provider_wizard_that_calls_completion": False,
        "ready_for_read_only_skill_execution_as_actions": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_subagent_invocation": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0422ReadinessReport(**_merge(defaults, overrides))


def create_v0423_trace_history_ux_handoff(**overrides: Any) -> V0423TraceHistoryUXHandoff:
    defaults = {
        "target_version": "v0.42.3",
        "title": "Human-readable Trace / Run History",
        "recommended_focus": (
            "human-readable trace timeline",
            "run history",
            "run show last",
            "session show last",
            "clarify provider_call_event_count vs provider_call_transaction_count",
            "preserve JSON trace availability",
        ),
        "must_not_open": ("shell_execution", "file_edit", "patch_apply", "subagent_invocation", "general_agent_loop", "new_provider_power", "production_certification"),
        "production_certified": False,
    }
    return V0423TraceHistoryUXHandoff(**_merge(defaults, overrides))


REQUIRED_V0422_RESTORE_SECTIONS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "project_context_for_new_codex_session",
    "v0416_user_test_baseline",
    "v0420_ux_baseline_summary",
    "v0421_home_quickstart_summary",
    "provider_setup_ux_summary",
    "provider_preset_registry",
    "provider_config_contract",
    "provider_setup_mock_contract",
    "provider_setup_local_openai_contract",
    "provider_status_contract",
    "provider_config_show_contract",
    "provider_secret_policy",
    "provider_run_readiness_contract",
    "provider_doctor_ux_interpretation",
    "provider_troubleshooting",
    "provider_user_guide",
    "provider_ux_safety_boundary",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "withdrawal_conditions",
    "v0423_handoff",
    "copy_paste_restore_prompt",
)


def create_v0422_integrated_restore_context_snapshot(**overrides: Any) -> V0422IntegratedRestoreContextSnapshot:
    defaults = {
        "current_version": "v0.42.2 Provider Setup UX",
        "current_track": V042_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            "v0.41.2 Prompt Assembly & Session Store",
            "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
            "v0.41.4 Minimal Single-turn Provider-backed Run",
            "v0.41.5 Event Trace Emission & Runtime Report",
            "v0.41.6 Installable Default Personal User Test Release",
            "v0.42.0 Default Personal Runtime UX Baseline & User Journey Contract",
            "v0.42.1 Default Home Resolver & Quickstart",
            "v0.42.2 Provider Setup UX",
        ),
        "open_capabilities": (
            "provider_preset_registry",
            "provider_setup_mock",
            "provider_setup_local_openai",
            "provider_setup_dry_run",
            "provider_config_write_under_profile_home",
            "provider_status_command",
            "provider_config_show_command",
            "provider_run_readiness_report",
            "provider_secret_redaction",
            "provider_troubleshooting",
            "provider_user_guide",
            "provider_ux_safety_report",
            "integrated_restore_document",
        ),
        "closed_capabilities": (
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
            "provider_setup_real_network_call",
            "real_provider_wizard_that_calls_completion",
            "read_only_skill_execution_as_actions",
            "general_agent_loop",
            "multi_step_agent_loop",
            "shell_execution",
            "file_edit",
            "patch_apply",
            "test_execution_through_cli",
            "subagent_invocation",
            "child_session_creation",
            "autonomous_retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
    }
    return V0422IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0422_integrated_restore_packet(**overrides: Any) -> V0422IntegratedRestorePacket:
    sections = tuple(V0422IntegratedRestoreSection(section_id, section_id.replace("_", " ").title(), True) for section_id in REQUIRED_V0422_RESTORE_SECTIONS)
    defaults = {
        "packet_id": "v0422-integrated-restore-packet",
        "context_snapshot": create_v0422_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0422IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0422_integrated_restore_document_manifest(**overrides: Any) -> V0422IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0422-integrated-restore-document-manifest",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "suitable_for_new_session_handoff": True,
        "required_sections": REQUIRED_V0422_RESTORE_SECTIONS,
    }
    return V0422IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _render_provider_setup(result: V042ProviderSetupResult) -> str:
    return "\n".join(
        (
            "ChantaCore provider setup",
            f"  status: {result.status}",
            f"  profile: {result.profile_id}",
            f"  config_path: {result.config_path}",
            f"  provider_kind: {result.config_draft.provider_kind}",
            f"  mode: {result.config_draft.mode}",
            f"  base_url: {result.config_draft.base_url or '(none)'}",
            f"  model: {result.config_draft.model or '(none)'}",
            f"  api_key_env_var: {result.config_draft.api_key_env_var or '(none)'}",
            f"  write: {result.write_result.message}",
            f"  next: {result.run_readiness_report.next_action}",
            "  closed: setup_provider_call=false, doctor_completion=false, tools=false, functions=false, shell=false, subagent=false, production_certified=false",
        )
    )


def _render_provider_status(report: V042ProviderStatusReport) -> str:
    return "\n".join(
        (
            "ChantaCore provider status",
            f"  config_present: {str(report.config_present).lower()}",
            f"  config_path: {report.config_path}",
            f"  provider_kind: {report.provider_kind or '(not configured)'}",
            f"  mode: {report.mode or '(not configured)'}",
            f"  base_url: {report.base_url_display or '(none)'}",
            f"  model: {report.model or '(none)'}",
            f"  api_key_env_var: {report.api_key_env_var or '(none)'}",
            f"  api_key_env_present: {report.api_key_env_present}",
            f"  ready_for_mock_run: {str(report.ready_for_mock_run).lower()}",
            f"  ready_for_configured_provider_run: {str(report.ready_for_configured_provider_run).lower()}",
            f"  provider_doctor_no_completion_available: {str(report.provider_doctor_no_completion_available).lower()}",
            f"  next: {report.next_action}",
        )
    )


def _render_provider_config_show(result: V042ProviderConfigShowResult) -> str:
    if not result.config_present:
        return f"ChantaCore provider config\n  config_present: false\n  config_path: {result.config_path}\n  next: chanta-cli provider setup mock"
    return "ChantaCore provider config\n" + _render_json(result.redacted_config)


def _handle_provider_setup(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli provider setup")
    parser.add_argument("preset", choices=("mock", "local-openai"))
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--base-url")
    parser.add_argument("--model")
    parser.add_argument("--api-key-env")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    if parsed.preset == "mock":
        request = create_v042_provider_setup_request(V042ProviderSetupMode.MOCK.value, parsed.home, parsed.profile, dry_run=parsed.dry_run, json_output=parsed.json)
    else:
        request = create_v042_provider_setup_request(
            V042ProviderSetupMode.LOCAL_OPENAI_COMPATIBLE.value,
            parsed.home,
            parsed.profile,
            preset_kind=V042ProviderPresetKind.LOCAL_OPENAI_COMPATIBLE.value,
            base_url=parsed.base_url,
            model=parsed.model,
            api_key_env_var=parsed.api_key_env,
            dry_run=parsed.dry_run,
            json_output=parsed.json,
        )
    result = create_v042_provider_setup_result(create_v042_provider_setup_plan(request))
    print(result.rendered_text)
    return 0 if result.status in {V042ProviderSetupStatus.PASS.value, V042ProviderSetupStatus.DRY_RUN.value} else 1


def _handle_provider_status(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli provider status")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    report = create_v042_provider_status_report(create_v042_provider_status_request(parsed.home, parsed.profile, parsed.json))
    print(report.rendered_text)
    return 0 if report.resolved_home_path else 1


def _handle_provider_config(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli provider config")
    sub = parser.add_subparsers(dest="command", required=True)
    show = sub.add_parser("show")
    show.add_argument("--home")
    show.add_argument("--profile", default=PROFILE_ID)
    show.add_argument("--json", action="store_true")
    show.add_argument("--include-sensitive", action="store_true")
    parsed = parser.parse_args(list(args))
    result = create_v042_provider_config_show_result(create_v042_provider_config_show_request(parsed.home, parsed.profile, parsed.json, parsed.include_sensitive))
    print(result.rendered_text)
    return 0 if result.config_path else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0422_VERSION}; {V0422_RELEASE_NAME})")
        return 0
    if len(args) >= 2 and args[0] == "provider" and args[1] == "setup":
        return _handle_provider_setup(args[2:])
    if len(args) >= 2 and args[0] == "provider" and args[1] == "status":
        return _handle_provider_status(args[2:])
    if len(args) >= 2 and args[0] == "provider" and args[1] == "config":
        return _handle_provider_config(args[2:])
    return _v0421_main(args)


__all__ = [name for name in globals() if name.startswith("V042") or name.startswith("create_v042") or name.startswith("build_v042") or name == "execute_v042_provider_setup_plan" or name == "main"]
