"""v0.42.1 Default Home Resolver & Quickstart support.

This module opens only usability surfaces for the default-personal runtime:
home resolution, home inspection, omitted-home adoption, and bounded
quickstart orchestration. It does not open provider setup, provider doctor
completion, tool calling, function calling, shell execution, subagents,
Dominion runtime, or production certification.
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

from chanta_core.personal_runtime.default_personal_cli_bootstrap import (
    PROFILE_ID,
    DefaultPersonalProfileStatusCommandInput,
    create_cli_bootstrap_paths,
    create_default_personal_init_plan,
    create_default_personal_init_request,
    execute_default_personal_init_plan,
    run_profile_status_command,
)
from chanta_core.personal_runtime.default_personal_provider_skills import (
    create_provider_doctor_report,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_last_run_report,
    create_last_run_report_request,
    create_trace_summary_request,
    summarize_trace_events,
)
from chanta_core.personal_runtime.default_personal_user_test_release import (
    main as _v0416_main,
)


V0421_VERSION = "v0.42.1"
V0421_RELEASE_NAME = "v0.42.1 Default Home Resolver & Quickstart"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
CHANTACORE_HOME_ENV = "CHANTACORE_HOME"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.1_default_home_resolver_quickstart_restore.md"


class V042HomeResolutionSource(StrEnum):
    EXPLICIT_HOME_ARG = "explicit_home_arg"
    CHANTACORE_HOME_ENV = "chantacore_home_env"
    PLATFORM_DEFAULT = "platform_default"
    UNRESOLVED = "unresolved"
    INVALID = "invalid"


class V042HomeResolutionStatus(StrEnum):
    RESOLVED = "resolved"
    RESOLVED_MISSING = "resolved_missing"
    UNRESOLVED = "unresolved"
    INVALID = "invalid"
    BLOCKED = "blocked"


class V042DefaultHomePlatform(StrEnum):
    WINDOWS = "windows"
    MACOS = "macos"
    LINUX = "linux"
    UNKNOWN = "unknown"


class V042QuickstartMode(StrEnum):
    SETUP_ONLY = "setup_only"
    WITH_MOCK_RUN = "with_mock_run"
    STATUS_ONLY = "status_only"
    UNKNOWN = "unknown"


class V042QuickstartStepKind(StrEnum):
    RESOLVE_HOME = "resolve_home"
    VALIDATE_HOME = "validate_home"
    INIT_PROFILE_IF_MISSING = "init_profile_if_missing"
    PROFILE_STATUS = "profile_status"
    PROVIDER_DOCTOR_NO_COMPLETION = "provider_doctor_no_completion"
    MOCK_RUN = "mock_run"
    TRACE_RECENT = "trace_recent"
    RUN_REPORT_LAST = "run_report_last"
    SAFETY_BOUNDARY_SUMMARY = "safety_boundary_summary"
    NEXT_ACTIONS = "next_actions"
    COMPLETED = "completed"


class V042QuickstartStepStatus(StrEnum):
    PASS = "pass"
    PASS_WITH_NOTES = "pass_with_notes"
    SKIPPED = "skipped"
    FAILED = "failed"
    BLOCKED = "blocked"


@dataclass(frozen=True)
class V042DefaultHomePolicy:
    policy_id: str
    resolution_order: tuple[str, ...]
    windows_default_template: str
    macos_default_template: str
    linux_default_template: str
    env_var_name: str
    explicit_home_supported: bool
    env_override_supported: bool
    platform_default_supported: bool
    silent_auto_create_allowed: bool
    quickstart_auto_create_allowed: bool
    init_auto_create_allowed: bool


@dataclass(frozen=True)
class V042HomeResolutionRequest:
    request_id: str
    explicit_home: str | None
    env: dict[str, str]
    platform: str | None
    cwd: str | None
    command_name: str
    allow_create: bool


@dataclass(frozen=True)
class V042ResolvedHome:
    resolved_id: str
    home_path: str | None
    source: str
    status: str
    platform: str
    exists: bool
    profile_exists: bool
    created_by_resolver: bool
    safe_to_use: bool
    message: str


@dataclass(frozen=True)
class V042HomeValidationFinding:
    finding_id: str
    severity: str
    field_name: str
    message: str
    recommendation: str
    blocks_command: bool
    blocks_quickstart: bool


@dataclass(frozen=True)
class V042HomeValidationReport:
    report_id: str
    resolved_home: V042ResolvedHome
    valid_for_read_only_commands: bool
    valid_for_quickstart: bool
    findings: tuple[V042HomeValidationFinding, ...]
    outside_allowed_location_detected: bool
    silent_creation_required: bool


@dataclass(frozen=True)
class V042HomeShowCommandInput:
    explicit_home: str | None
    command_name: str
    json_output: bool


@dataclass(frozen=True)
class V042HomeShowCommandResult:
    result_id: str
    resolved_home: V042ResolvedHome
    validation_report: V042HomeValidationReport
    rendered_text: str
    exit_code: int
    mutated_filesystem: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042HomeStatusCommandInput:
    explicit_home: str | None
    profile_id: str
    json_output: bool


@dataclass(frozen=True)
class V042HomeStatusCommandResult:
    result_id: str
    resolved_home: V042ResolvedHome
    profile_id: str
    profile_exists: bool
    profile_config_exists: bool
    sessions_dir_exists: bool
    traces_dir_exists: bool
    provider_config_exists: bool
    recommended_next_action: str
    rendered_text: str
    exit_code: int
    mutated_filesystem: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042CommandHomeAdoptionRecord:
    record_id: str
    command_name: str
    previously_required_explicit_home: bool
    now_supports_omitted_home: bool
    resolver_used: bool
    creates_home_when_missing: bool
    behavior_when_home_missing: str
    target_user_value: str


@dataclass(frozen=True)
class V042QuickstartStep:
    step_id: str
    order_index: int
    step_kind: str
    status: str
    message: str
    command_equivalent: str | None
    mutated_filesystem: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042QuickstartPlan:
    plan_id: str
    mode: str
    profile_id: str
    resolved_home: V042ResolvedHome
    steps: tuple[V042QuickstartStep, ...]
    will_create_profile_if_missing: bool
    will_run_mock_provider: bool
    will_call_real_provider: bool
    will_execute_shell: bool
    safe_to_execute: bool


@dataclass(frozen=True)
class V042QuickstartMockRunPolicy:
    policy_id: str
    mock_run_allowed: bool
    real_provider_allowed: bool
    provider_doctor_completion_allowed: bool
    tool_calling_allowed: bool
    function_calling_allowed: bool
    shell_allowed: bool
    subagent_allowed: bool
    prompt_text: str


@dataclass(frozen=True)
class V042QuickstartMockRunResult:
    result_id: str
    attempted: bool
    status: str
    session_id: str | None
    run_id: str | None
    assistant_response_preview: str | None
    trace_event_count: int | None
    provider_invoked: bool
    prompt_submitted: bool
    real_provider_invoked: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042QuickstartNextAction:
    action_id: str
    title: str
    command_text: str
    purpose: str
    priority: str


@dataclass(frozen=True)
class V042QuickstartResult:
    result_id: str
    mode: str
    profile_id: str
    resolved_home: V042ResolvedHome
    steps: tuple[V042QuickstartStep, ...]
    mock_run_result: V042QuickstartMockRunResult | None
    next_actions: tuple[V042QuickstartNextAction, ...]
    rendered_text: str
    exit_code: int
    ready_for_basic_user_testing: bool
    provider_setup_completed: bool
    real_provider_tested: bool
    production_certified: bool


@dataclass(frozen=True)
class V042QuickstartSafetyReport:
    report_id: str
    quickstart_result: V042QuickstartResult
    provider_doctor_completion_closed: bool
    real_provider_not_called_by_default: bool
    tool_calling_closed: bool
    function_calling_closed: bool
    shell_closed: bool
    subagent_closed: bool
    file_edit_closed: bool
    patch_apply_closed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0421ReadinessReport:
    default_home_policy_ready: bool
    home_resolver_ready: bool
    chantacore_home_env_override_ready: bool
    platform_default_home_ready: bool
    home_show_command_ready: bool
    home_status_command_ready: bool
    existing_commands_can_omit_home: bool
    quickstart_command_ready: bool
    quickstart_setup_only_ready: bool
    quickstart_mock_run_ready: bool
    quickstart_safety_report_ready: bool
    integrated_restore_document_ready: bool
    v0422_handoff_ready: bool
    ready_for_provider_setup_command: bool
    ready_for_real_provider_wizard: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
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
class V0422ProviderSetupUXHandoff:
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_remain_closed: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0421IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0421IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0421IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0421IntegratedRestoreContextSnapshot
    sections: tuple[V0421IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0421IntegratedRestoreDocumentManifest:
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


def _normal_path(path: str | Path) -> str:
    return str(Path(path).expanduser())


def _profile_config_path(home_path: str, profile_id: str = PROFILE_ID) -> Path:
    return Path(home_path) / "profiles" / profile_id / "profile.json"


def _default_windows_home(env: Mapping[str, str]) -> str | None:
    local_app_data = env.get("LOCALAPPDATA")
    if local_app_data:
        return str(Path(local_app_data) / "ChantaCore")
    user_profile = env.get("USERPROFILE")
    if user_profile:
        return str(Path(user_profile) / "AppData" / "Local" / "ChantaCore")
    try:
        return str(Path.home() / "AppData" / "Local" / "ChantaCore")
    except RuntimeError:
        return None


def _default_home_for_platform(platform: str, env: Mapping[str, str], cwd: str | None) -> str | None:
    if platform == V042DefaultHomePlatform.WINDOWS.value:
        return _default_windows_home(env)
    if platform == V042DefaultHomePlatform.MACOS.value:
        home = env.get("HOME")
        return str(Path(home) / "Library" / "Application Support" / "ChantaCore") if home else None
    if platform == V042DefaultHomePlatform.LINUX.value:
        xdg = env.get("XDG_DATA_HOME")
        if xdg:
            return str(Path(xdg) / "ChantaCore")
        home = env.get("HOME")
        return str(Path(home) / ".local" / "share" / "ChantaCore") if home else None
    if cwd:
        return str(Path(cwd) / ".chantacore")
    return None


def _is_obviously_unsafe_home(home_path: str | None) -> bool:
    if not home_path:
        return True
    path = Path(home_path)
    text = str(path).strip()
    if not text:
        return True
    if text in {"/", "\\", ".", ".."}:
        return True
    resolved = path.resolve(strict=False)
    anchor = Path(resolved.anchor) if resolved.anchor else None
    return bool(anchor and resolved == anchor)


def create_v042_default_home_policy(**overrides: Any) -> V042DefaultHomePolicy:
    defaults = {
        "policy_id": "v0421-default-home-policy",
        "resolution_order": (
            V042HomeResolutionSource.EXPLICIT_HOME_ARG.value,
            V042HomeResolutionSource.CHANTACORE_HOME_ENV.value,
            V042HomeResolutionSource.PLATFORM_DEFAULT.value,
        ),
        "windows_default_template": "%LOCALAPPDATA%\\ChantaCore",
        "macos_default_template": "$HOME/Library/Application Support/ChantaCore",
        "linux_default_template": "${XDG_DATA_HOME:-$HOME/.local/share}/ChantaCore",
        "env_var_name": CHANTACORE_HOME_ENV,
        "explicit_home_supported": True,
        "env_override_supported": True,
        "platform_default_supported": True,
        "silent_auto_create_allowed": False,
        "quickstart_auto_create_allowed": True,
        "init_auto_create_allowed": True,
    }
    return V042DefaultHomePolicy(**_merge(defaults, overrides))


def detect_v042_platform(platform: str | None = None) -> str:
    value = (platform or sys.platform or "").lower()
    if value.startswith("win") or os.name == "nt" and platform is None:
        return V042DefaultHomePlatform.WINDOWS.value
    if value == "darwin" or value.startswith("mac"):
        return V042DefaultHomePlatform.MACOS.value
    if value.startswith("linux"):
        return V042DefaultHomePlatform.LINUX.value
    return V042DefaultHomePlatform.UNKNOWN.value


def create_v042_home_resolution_request(
    explicit_home: str | None = None,
    env: Mapping[str, str] | None = None,
    platform: str | None = None,
    cwd: str | None = None,
    command_name: str = "home show",
    allow_create: bool = False,
    **overrides: Any,
) -> V042HomeResolutionRequest:
    defaults = {
        "request_id": "v0421-home-resolution-request",
        "explicit_home": explicit_home,
        "env": dict(os.environ if env is None else env),
        "platform": platform,
        "cwd": cwd,
        "command_name": command_name,
        "allow_create": bool(allow_create),
    }
    return V042HomeResolutionRequest(**_merge(defaults, overrides))


def resolve_v042_home(request: V042HomeResolutionRequest, **overrides: Any) -> V042ResolvedHome:
    platform = detect_v042_platform(request.platform)
    source = V042HomeResolutionSource.UNRESOLVED.value
    path: str | None = None
    if request.explicit_home:
        path = request.explicit_home
        source = V042HomeResolutionSource.EXPLICIT_HOME_ARG.value
    elif request.env.get(CHANTACORE_HOME_ENV):
        path = request.env[CHANTACORE_HOME_ENV]
        source = V042HomeResolutionSource.CHANTACORE_HOME_ENV.value
    else:
        path = _default_home_for_platform(platform, request.env, request.cwd)
        source = V042HomeResolutionSource.PLATFORM_DEFAULT.value if path else V042HomeResolutionSource.UNRESOLVED.value

    home_path = _normal_path(path) if path else None
    safe = not _is_obviously_unsafe_home(home_path)
    exists = bool(home_path and Path(home_path).exists())
    profile_exists = bool(home_path and _profile_config_path(home_path).exists())
    if not home_path:
        status = V042HomeResolutionStatus.UNRESOLVED.value
        message = "No ChantaCore home could be resolved."
    elif not safe:
        status = V042HomeResolutionStatus.BLOCKED.value
        source = V042HomeResolutionSource.INVALID.value
        message = "Resolved home is blocked because it is empty or root-like."
    elif exists:
        status = V042HomeResolutionStatus.RESOLVED.value
        message = f"Resolved ChantaCore home from {source}."
    else:
        status = V042HomeResolutionStatus.RESOLVED_MISSING.value
        message = f"Resolved ChantaCore home from {source}, but it does not exist yet."

    defaults = {
        "resolved_id": "v0421-resolved-home",
        "home_path": home_path,
        "source": source,
        "status": status,
        "platform": platform,
        "exists": exists,
        "profile_exists": profile_exists,
        "created_by_resolver": False,
        "safe_to_use": safe,
        "message": message,
    }
    return V042ResolvedHome(**_merge(defaults, overrides))


def validate_v042_resolved_home(
    resolved_home: V042ResolvedHome,
    allow_create: bool = False,
    **overrides: Any,
) -> V042HomeValidationReport:
    findings: list[V042HomeValidationFinding] = []
    if not resolved_home.home_path or not resolved_home.safe_to_use:
        findings.append(
            V042HomeValidationFinding(
                "home-blocking-path",
                "blocking",
                "home_path",
                "Home path is unresolved or blocked.",
                "Pass --home, set CHANTACORE_HOME, or run quickstart with a valid platform default.",
                True,
                True,
            )
        )
    elif not resolved_home.exists:
        findings.append(
            V042HomeValidationFinding(
                "home-missing",
                "warning",
                "home_path",
                "Resolved home does not exist.",
                "Run chanta-cli quickstart or chanta-cli init default-personal.",
                True,
                False,
            )
        )
    elif not resolved_home.profile_exists:
        findings.append(
            V042HomeValidationFinding(
                "profile-missing",
                "warning",
                "profile",
                "default-personal profile is missing.",
                "Run chanta-cli quickstart.",
                False,
                False,
            )
        )
    valid_for_read_only = bool(resolved_home.home_path and resolved_home.safe_to_use and resolved_home.exists)
    valid_for_quickstart = bool(resolved_home.home_path and resolved_home.safe_to_use)
    defaults = {
        "report_id": "v0421-home-validation-report",
        "resolved_home": resolved_home,
        "valid_for_read_only_commands": valid_for_read_only,
        "valid_for_quickstart": valid_for_quickstart,
        "findings": tuple(findings),
        "outside_allowed_location_detected": False,
        "silent_creation_required": False,
    }
    return V042HomeValidationReport(**_merge(defaults, overrides))


def create_v042_home_validation_report(
    resolved_home: V042ResolvedHome,
    allow_create: bool = False,
    **overrides: Any,
) -> V042HomeValidationReport:
    return validate_v042_resolved_home(resolved_home, allow_create=allow_create, **overrides)


def create_v042_home_show_command_input(
    explicit_home: str | None = None,
    command_name: str = "home show",
    json_output: bool = False,
    **overrides: Any,
) -> V042HomeShowCommandInput:
    defaults = {"explicit_home": explicit_home, "command_name": command_name, "json_output": json_output}
    return V042HomeShowCommandInput(**_merge(defaults, overrides))


def _render_home_show(result: V042ResolvedHome, validation: V042HomeValidationReport) -> str:
    return "\n".join(
        (
            "ChantaCore home",
            f"  path: {result.home_path or '(unresolved)'}",
            f"  source: {result.source}",
            f"  status: {result.status}",
            f"  exists: {str(result.exists).lower()}",
            f"  profile_exists: {str(result.profile_exists).lower()}",
            f"  safe_to_use: {str(result.safe_to_use).lower()}",
            f"  next: {'ready' if validation.valid_for_read_only_commands else 'run chanta-cli quickstart or pass --home'}",
        )
    )


def create_v042_home_show_command_result(
    command_input: V042HomeShowCommandInput,
    env: Mapping[str, str] | None = None,
    platform: str | None = None,
    cwd: str | None = None,
    **overrides: Any,
) -> V042HomeShowCommandResult:
    request = create_v042_home_resolution_request(
        explicit_home=command_input.explicit_home,
        env=env,
        platform=platform,
        cwd=cwd,
        command_name=command_input.command_name,
        allow_create=False,
    )
    resolved = resolve_v042_home(request)
    validation = validate_v042_resolved_home(resolved, allow_create=False)
    rendered = _render_json({"resolved_home": resolved, "validation_report": validation}) if command_input.json_output else _render_home_show(resolved, validation)
    defaults = {
        "result_id": "v0421-home-show-result",
        "resolved_home": resolved,
        "validation_report": validation,
        "rendered_text": rendered,
        "exit_code": 0 if resolved.home_path and resolved.safe_to_use else 1,
        "mutated_filesystem": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042HomeShowCommandResult(**_merge(defaults, overrides))


def create_v042_home_status_command_input(
    explicit_home: str | None = None,
    profile_id: str = PROFILE_ID,
    json_output: bool = False,
    **overrides: Any,
) -> V042HomeStatusCommandInput:
    defaults = {"explicit_home": explicit_home, "profile_id": profile_id, "json_output": json_output}
    return V042HomeStatusCommandInput(**_merge(defaults, overrides))


def _provider_config_path(home_path: str, profile_id: str = PROFILE_ID) -> Path:
    return Path(home_path) / "profiles" / profile_id / "provider.json"


def _render_home_status(result: V042HomeStatusCommandResult) -> str:
    return "\n".join(
        (
            "ChantaCore home status",
            f"  path: {result.resolved_home.home_path or '(unresolved)'}",
            f"  source: {result.resolved_home.source}",
            f"  profile: {result.profile_id}",
            f"  profile_exists: {str(result.profile_exists).lower()}",
            f"  profile_config_exists: {str(result.profile_config_exists).lower()}",
            f"  sessions_dir_exists: {str(result.sessions_dir_exists).lower()}",
            f"  traces_dir_exists: {str(result.traces_dir_exists).lower()}",
            f"  provider_config_exists: {str(result.provider_config_exists).lower()}",
            f"  next: {result.recommended_next_action}",
        )
    )


def create_v042_home_status_command_result(
    command_input: V042HomeStatusCommandInput,
    env: Mapping[str, str] | None = None,
    platform: str | None = None,
    cwd: str | None = None,
    **overrides: Any,
) -> V042HomeStatusCommandResult:
    request = create_v042_home_resolution_request(
        explicit_home=command_input.explicit_home,
        env=env,
        platform=platform,
        cwd=cwd,
        command_name="home status",
        allow_create=False,
    )
    resolved = resolve_v042_home(request)
    home = resolved.home_path
    paths = create_cli_bootstrap_paths(home) if home else None
    profile_exists = bool(paths and Path(paths.default_profile_dir).exists())
    profile_config_exists = bool(paths and Path(paths.profile_config_path).exists())
    sessions_dir_exists = bool(paths and Path(paths.sessions_dir).exists())
    traces_dir_exists = bool(paths and Path(paths.traces_dir).exists())
    provider_config_exists = bool(home and _provider_config_path(home, command_input.profile_id).exists())
    if not home or not resolved.safe_to_use:
        next_action = "pass --home, set CHANTACORE_HOME, or run quickstart with a valid platform default"
        exit_code = 1
    elif not resolved.exists or not profile_config_exists:
        next_action = "run chanta-cli quickstart"
        exit_code = 1
    else:
        next_action = "run chanta-cli provider doctor --profile default-personal --no-completion"
        exit_code = 0
    defaults = {
        "result_id": "v0421-home-status-result",
        "resolved_home": resolved,
        "profile_id": command_input.profile_id,
        "profile_exists": profile_exists,
        "profile_config_exists": profile_config_exists,
        "sessions_dir_exists": sessions_dir_exists,
        "traces_dir_exists": traces_dir_exists,
        "provider_config_exists": provider_config_exists,
        "recommended_next_action": next_action,
        "rendered_text": "",
        "exit_code": exit_code,
        "mutated_filesystem": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    result = V042HomeStatusCommandResult(**_merge(defaults, overrides))
    rendered = _render_json(result) if command_input.json_output else _render_home_status(result)
    return replace(result, rendered_text=rendered)


def create_v042_command_home_adoption_record(command_name: str, **overrides: Any) -> V042CommandHomeAdoptionRecord:
    defaults = {
        "record_id": f"v0421-home-adoption-{command_name.replace(' ', '-')}",
        "command_name": command_name,
        "previously_required_explicit_home": True,
        "now_supports_omitted_home": True,
        "resolver_used": True,
        "creates_home_when_missing": False,
        "behavior_when_home_missing": "block with quickstart/init guidance; do not silently create home",
        "target_user_value": "User can omit --home after quickstart or when CHANTACORE_HOME/default home is prepared.",
    }
    return V042CommandHomeAdoptionRecord(**_merge(defaults, overrides))


def build_v042_command_home_adoption_records() -> tuple[V042CommandHomeAdoptionRecord, ...]:
    return tuple(
        create_v042_command_home_adoption_record(name)
        for name in (
            "profile status",
            "provider doctor",
            "prompt preview",
            "session new",
            "session list",
            "run",
            "trace recent",
            "trace summary",
            "run-report last",
            "safety check-command",
        )
    )


def create_v042_quickstart_step(
    order_index: int,
    step_kind: str,
    status: str,
    message: str,
    command_equivalent: str | None = None,
    mutated_filesystem: bool = False,
    provider_invoked: bool = False,
    prompt_submitted: bool = False,
    **overrides: Any,
) -> V042QuickstartStep:
    defaults = {
        "step_id": f"v0421-quickstart-step-{order_index:02d}-{step_kind}",
        "order_index": order_index,
        "step_kind": step_kind,
        "status": status,
        "message": message,
        "command_equivalent": command_equivalent,
        "mutated_filesystem": mutated_filesystem,
        "provider_invoked": provider_invoked,
        "prompt_submitted": prompt_submitted,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042QuickstartStep(**_merge(defaults, overrides))


def create_v042_quickstart_plan(
    resolved_home: V042ResolvedHome,
    mode: str = V042QuickstartMode.SETUP_ONLY.value,
    profile_id: str = PROFILE_ID,
    validation_report: V042HomeValidationReport | None = None,
    **overrides: Any,
) -> V042QuickstartPlan:
    validation = validation_report or validate_v042_resolved_home(resolved_home, allow_create=True)
    will_run_mock = mode == V042QuickstartMode.WITH_MOCK_RUN.value
    steps = (
        create_v042_quickstart_step(1, V042QuickstartStepKind.RESOLVE_HOME.value, V042QuickstartStepStatus.PASS.value, resolved_home.message),
        create_v042_quickstart_step(
            2,
            V042QuickstartStepKind.VALIDATE_HOME.value,
            V042QuickstartStepStatus.PASS.value if validation.valid_for_quickstart else V042QuickstartStepStatus.BLOCKED.value,
            "Home is valid for quickstart." if validation.valid_for_quickstart else "Home is not valid for quickstart.",
        ),
        create_v042_quickstart_step(3, V042QuickstartStepKind.INIT_PROFILE_IF_MISSING.value, V042QuickstartStepStatus.SKIPPED.value, "Planned if profile is missing."),
        create_v042_quickstart_step(4, V042QuickstartStepKind.PROFILE_STATUS.value, V042QuickstartStepStatus.SKIPPED.value, "Planned after init check."),
        create_v042_quickstart_step(5, V042QuickstartStepKind.PROVIDER_DOCTOR_NO_COMPLETION.value, V042QuickstartStepStatus.SKIPPED.value, "Planned no-completion provider doctor."),
    ) + (
        (create_v042_quickstart_step(6, V042QuickstartStepKind.MOCK_RUN.value, V042QuickstartStepStatus.SKIPPED.value, "Planned mock-provider run."),)
        if will_run_mock
        else ()
    )
    defaults = {
        "plan_id": "v0421-quickstart-plan",
        "mode": mode,
        "profile_id": profile_id,
        "resolved_home": resolved_home,
        "steps": steps,
        "will_create_profile_if_missing": not resolved_home.profile_exists,
        "will_run_mock_provider": will_run_mock,
        "will_call_real_provider": False,
        "will_execute_shell": False,
        "safe_to_execute": validation.valid_for_quickstart,
    }
    return V042QuickstartPlan(**_merge(defaults, overrides))


def create_v042_quickstart_mock_run_policy(**overrides: Any) -> V042QuickstartMockRunPolicy:
    defaults = {
        "policy_id": "v0421-quickstart-mock-run-policy",
        "mock_run_allowed": True,
        "real_provider_allowed": False,
        "provider_doctor_completion_allowed": False,
        "tool_calling_allowed": False,
        "function_calling_allowed": False,
        "shell_allowed": False,
        "subagent_allowed": False,
        "prompt_text": "Summarize what ChantaCore is in three bullets.",
    }
    return V042QuickstartMockRunPolicy(**_merge(defaults, overrides))


def create_v042_quickstart_mock_run_result(**overrides: Any) -> V042QuickstartMockRunResult:
    defaults = {
        "result_id": "v0421-quickstart-mock-run-result",
        "attempted": False,
        "status": V042QuickstartStepStatus.SKIPPED.value,
        "session_id": None,
        "run_id": None,
        "assistant_response_preview": None,
        "trace_event_count": None,
        "provider_invoked": False,
        "prompt_submitted": False,
        "real_provider_invoked": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042QuickstartMockRunResult(**_merge(defaults, overrides))


def create_v042_quickstart_next_action(action_id: str, title: str, command_text: str, purpose: str, priority: str = "normal") -> V042QuickstartNextAction:
    return V042QuickstartNextAction(action_id, title, command_text, purpose, priority)


def build_v042_quickstart_next_actions() -> tuple[V042QuickstartNextAction, ...]:
    return (
        create_v042_quickstart_next_action("mock-run", "Run with mock provider", 'chanta-cli run --profile default-personal --provider mock "Summarize what ChantaCore is in three bullets."', "Verify the default-personal run path without real provider access.", "high"),
        create_v042_quickstart_next_action("provider-setup-v0422", "Provider setup target", "v0.42.2 Provider Setup UX", "Configure real providers in a later gated UX track.", "normal"),
        create_v042_quickstart_next_action("trace-recent", "Review trace recent", "chanta-cli trace recent --profile default-personal --limit 10", "Inspect recent runtime events.", "normal"),
        create_v042_quickstart_next_action("run-report-last", "Review last run", "chanta-cli run-report last --profile default-personal", "Inspect the latest run report.", "normal"),
        create_v042_quickstart_next_action("safety-check", "Run denial check", 'chanta-cli safety check-command --profile default-personal --command "Remove-Item -Recurse -Force C:\\"', "Confirm unsafe command denial remains visible.", "normal"),
        create_v042_quickstart_next_action("provider-setup-note", "v0.42.2 note", "Do not use provider setup until v0.42.2.", "Provider setup wizard remains closed in v0.42.1.", "low"),
    )


def _run_bounded_profile_init(home_path: str) -> tuple[bool, str]:
    request = create_default_personal_init_request(home_path)
    plan = create_default_personal_init_plan(request)
    result = execute_default_personal_init_plan(request, plan)
    mutated = bool(result.created_directories or result.created_files)
    return mutated, f"init status={result.status}; created_files={len(result.created_files)}; skipped_files={len(result.skipped_files)}"


def _run_mock_provider_flow(home_path: str, profile_id: str, policy: V042QuickstartMockRunPolicy) -> V042QuickstartMockRunResult:
    exit_code = _v0416_main([
        "run",
        "--profile",
        profile_id,
        "--home",
        home_path,
        "--provider",
        "mock",
        policy.prompt_text,
    ])
    report = create_last_run_report(create_last_run_report_request(profile_id=profile_id, home_path=home_path))
    summary = summarize_trace_events(create_trace_summary_request(profile_id=profile_id, home_path=home_path))
    return create_v042_quickstart_mock_run_result(
        attempted=True,
        status=V042QuickstartStepStatus.PASS.value if exit_code == 0 and report.found else V042QuickstartStepStatus.FAILED.value,
        session_id=report.session_id,
        run_id=report.run_id,
        assistant_response_preview=report.assistant_response_preview,
        trace_event_count=summary.total_events,
        provider_invoked=report.provider_invoked,
        prompt_submitted=report.prompt_submitted,
        real_provider_invoked=False,
    )


def create_v042_quickstart_result(
    mode: str,
    profile_id: str,
    resolved_home: V042ResolvedHome,
    steps: tuple[V042QuickstartStep, ...],
    mock_run_result: V042QuickstartMockRunResult | None,
    next_actions: tuple[V042QuickstartNextAction, ...],
    rendered_text: str,
    exit_code: int,
    ready_for_basic_user_testing: bool,
    **overrides: Any,
) -> V042QuickstartResult:
    defaults = {
        "result_id": "v0421-quickstart-result",
        "mode": mode,
        "profile_id": profile_id,
        "resolved_home": resolved_home,
        "steps": steps,
        "mock_run_result": mock_run_result,
        "next_actions": next_actions,
        "rendered_text": rendered_text,
        "exit_code": exit_code,
        "ready_for_basic_user_testing": ready_for_basic_user_testing,
        "provider_setup_completed": False,
        "real_provider_tested": False,
        "production_certified": False,
    }
    return V042QuickstartResult(**_merge(defaults, overrides))


def _render_quickstart(result: V042QuickstartResult) -> str:
    lines = [
        "ChantaCore quickstart",
        f"  mode: {result.mode}",
        f"  home: {result.resolved_home.home_path}",
        f"  source: {result.resolved_home.source}",
        f"  profile: {result.profile_id}",
        f"  ready_for_basic_user_testing: {str(result.ready_for_basic_user_testing).lower()}",
        "  steps:",
    ]
    lines.extend(f"    - {step.step_kind}: {step.status} ({step.message})" for step in result.steps)
    if result.mock_run_result:
        lines.extend(
            (
                "  mock_run:",
                f"    status: {result.mock_run_result.status}",
                f"    run_id: {result.mock_run_result.run_id}",
                f"    session_id: {result.mock_run_result.session_id}",
                f"    provider_text_untrusted: true",
            )
        )
    lines.append("  next_actions:")
    lines.extend(f"    - {action.command_text}" for action in result.next_actions)
    lines.append("  closed: real_provider_default=false, provider_doctor_completion=false, shell=false, subagent=false, production_certified=false")
    return "\n".join(lines)


def run_v042_quickstart(
    explicit_home: str | None = None,
    env: Mapping[str, str] | None = None,
    platform: str | None = None,
    cwd: str | None = None,
    profile_id: str = PROFILE_ID,
    with_mock_run: bool = False,
    json_output: bool = False,
) -> V042QuickstartResult:
    mode = V042QuickstartMode.WITH_MOCK_RUN.value if with_mock_run else V042QuickstartMode.SETUP_ONLY.value
    request = create_v042_home_resolution_request(explicit_home, env, platform, cwd, "quickstart", allow_create=True)
    resolved = resolve_v042_home(request)
    validation = validate_v042_resolved_home(resolved, allow_create=True)
    plan = create_v042_quickstart_plan(resolved, mode=mode, profile_id=profile_id, validation_report=validation)
    steps: list[V042QuickstartStep] = list(plan.steps[:2])
    if not plan.safe_to_execute or not resolved.home_path:
        steps.append(create_v042_quickstart_step(3, V042QuickstartStepKind.COMPLETED.value, V042QuickstartStepStatus.BLOCKED.value, "Quickstart blocked before filesystem mutation."))
        result = create_v042_quickstart_result(mode, profile_id, resolved, tuple(steps), None, build_v042_quickstart_next_actions(), "", 1, False)
        return replace(result, rendered_text=_render_json(result) if json_output else _render_quickstart(result))

    profile_was_missing = not _profile_config_path(resolved.home_path, profile_id).exists()
    mutated = False
    init_message = "default-personal profile already exists."
    if profile_was_missing:
        mutated, init_message = _run_bounded_profile_init(resolved.home_path)
    steps.append(
        create_v042_quickstart_step(
            3,
            V042QuickstartStepKind.INIT_PROFILE_IF_MISSING.value,
            V042QuickstartStepStatus.PASS.value,
            init_message,
            "chanta-cli init default-personal",
            mutated_filesystem=mutated,
        )
    )

    status = run_profile_status_command(DefaultPersonalProfileStatusCommandInput(profile_id=profile_id, home_path=resolved.home_path))
    steps.append(
        create_v042_quickstart_step(
            4,
            V042QuickstartStepKind.PROFILE_STATUS.value,
            V042QuickstartStepStatus.PASS.value if status.profile_config_exists else V042QuickstartStepStatus.FAILED.value,
            status.message,
            "chanta-cli profile status --profile default-personal",
        )
    )
    provider_report = create_provider_doctor_report(resolved.home_path, no_completion=True, probe_models=False)
    steps.append(
        create_v042_quickstart_step(
            5,
            V042QuickstartStepKind.PROVIDER_DOCTOR_NO_COMPLETION.value,
            V042QuickstartStepStatus.PASS.value if not provider_report.provider_invoked_completion else V042QuickstartStepStatus.FAILED.value,
            f"provider doctor status={provider_report.status}; completion=false",
            "chanta-cli provider doctor --profile default-personal --no-completion",
        )
    )

    mock_result: V042QuickstartMockRunResult | None = None
    if with_mock_run:
        policy = create_v042_quickstart_mock_run_policy()
        mock_result = _run_mock_provider_flow(resolved.home_path, profile_id, policy)
        steps.append(
            create_v042_quickstart_step(
                6,
                V042QuickstartStepKind.MOCK_RUN.value,
                mock_result.status,
                "mock provider run completed through existing v0.41.6 run path." if mock_result.status == V042QuickstartStepStatus.PASS.value else "mock provider run failed.",
                'chanta-cli run --profile default-personal --provider mock "Summarize what ChantaCore is in three bullets."',
                mutated_filesystem=True,
                provider_invoked=mock_result.provider_invoked,
                prompt_submitted=mock_result.prompt_submitted,
            )
        )
        steps.append(create_v042_quickstart_step(7, V042QuickstartStepKind.RUN_REPORT_LAST.value, V042QuickstartStepStatus.PASS.value, "run-report last is available after mock run.", "chanta-cli run-report last --profile default-personal"))
        steps.append(create_v042_quickstart_step(8, V042QuickstartStepKind.TRACE_RECENT.value, V042QuickstartStepStatus.PASS.value, "trace recent is available after mock run.", "chanta-cli trace recent --profile default-personal --limit 10"))

    steps.append(create_v042_quickstart_step(90, V042QuickstartStepKind.SAFETY_BOUNDARY_SUMMARY.value, V042QuickstartStepStatus.PASS.value, "Real provider default, provider doctor completion, tools, functions, shell, subagent, and production remain closed."))
    steps.append(create_v042_quickstart_step(99, V042QuickstartStepKind.NEXT_ACTIONS.value, V042QuickstartStepStatus.PASS.value, "Next user-facing commands are available."))
    ready = bool(status.profile_config_exists and not provider_report.provider_invoked_completion)
    if with_mock_run:
        ready = ready and bool(mock_result and mock_result.status == V042QuickstartStepStatus.PASS.value)
    result = create_v042_quickstart_result(mode, profile_id, resolved, tuple(steps), mock_result, build_v042_quickstart_next_actions(), "", 0 if ready else 1, ready)
    rendered = _render_json(result) if json_output else _render_quickstart(result)
    return replace(result, rendered_text=rendered)


def create_v042_quickstart_safety_report(quickstart_result: V042QuickstartResult, **overrides: Any) -> V042QuickstartSafetyReport:
    defaults = {
        "report_id": "v0421-quickstart-safety-report",
        "quickstart_result": quickstart_result,
        "provider_doctor_completion_closed": True,
        "real_provider_not_called_by_default": True,
        "tool_calling_closed": True,
        "function_calling_closed": True,
        "shell_closed": True,
        "subagent_closed": True,
        "file_edit_closed": True,
        "patch_apply_closed": True,
        "production_certified": False,
    }
    return V042QuickstartSafetyReport(**_merge(defaults, overrides))


def create_v0421_readiness_report(**overrides: Any) -> V0421ReadinessReport:
    defaults = {
        "default_home_policy_ready": True,
        "home_resolver_ready": True,
        "chantacore_home_env_override_ready": True,
        "platform_default_home_ready": True,
        "home_show_command_ready": True,
        "home_status_command_ready": True,
        "existing_commands_can_omit_home": True,
        "quickstart_command_ready": True,
        "quickstart_setup_only_ready": True,
        "quickstart_mock_run_ready": True,
        "quickstart_safety_report_ready": True,
        "integrated_restore_document_ready": True,
        "v0422_handoff_ready": True,
        "ready_for_provider_setup_command": False,
        "ready_for_real_provider_wizard": False,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
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
    return V0421ReadinessReport(**_merge(defaults, overrides))


def create_v0422_provider_setup_ux_handoff(**overrides: Any) -> V0422ProviderSetupUXHandoff:
    defaults = {
        "target_version": "v0.42.2",
        "title": "Provider Setup UX",
        "recommended_focus": (
            "provider setup command",
            "provider status command",
            "mock/local OpenAI-compatible provider profiles",
            "base_url/model configuration",
            "secrets remain env-var references only",
            "provider doctor remains no-completion",
            "real provider completion remains allowed only in run",
        ),
        "must_remain_closed": (
            "provider_tool_calling",
            "function_calling",
            "shell_execution",
            "file_edit",
            "patch_apply",
            "subagent_invocation",
            "general_agent_loop",
            "production_certification",
        ),
        "production_certified": False,
    }
    return V0422ProviderSetupUXHandoff(**_merge(defaults, overrides))


def create_v0421_integrated_restore_context_snapshot(**overrides: Any) -> V0421IntegratedRestoreContextSnapshot:
    defaults = {
        "current_version": "v0.42.1 Default Home Resolver & Quickstart",
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
        ),
        "open_capabilities": (
            "default_home_resolver",
            "explicit_home_resolution",
            "CHANTACORE_HOME_env_resolution",
            "platform_default_home_resolution",
            "home_show_command",
            "home_status_command",
            "existing_command_home_omission_support",
            "quickstart_command",
            "quickstart_setup_only",
            "quickstart_with_mock_run",
            "quickstart_next_actions",
            "quickstart_safety_report",
            "integrated_restore_document",
        ),
        "closed_capabilities": (
            "provider_setup_command",
            "real_provider_wizard",
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
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
    return V0421IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


REQUIRED_V0421_RESTORE_SECTIONS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "project_context_for_new_codex_session",
    "v0416_user_test_baseline",
    "v0420_ux_baseline_summary",
    "default_home_resolver_summary",
    "home_resolution_policy",
    "home_resolution_order",
    "chantacore_home_env_override",
    "platform_default_home",
    "home_show_contract",
    "home_status_contract",
    "command_home_adoption_contract",
    "quickstart_summary",
    "quickstart_setup_only_contract",
    "quickstart_mock_run_contract",
    "quickstart_safety_boundary",
    "user_facing_examples",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "withdrawal_conditions",
    "v0422_handoff",
    "copy_paste_restore_prompt",
)


def create_v0421_integrated_restore_packet(**overrides: Any) -> V0421IntegratedRestorePacket:
    sections = tuple(V0421IntegratedRestoreSection(section_id, section_id.replace("_", " ").title(), True) for section_id in REQUIRED_V0421_RESTORE_SECTIONS)
    defaults = {
        "packet_id": "v0421-integrated-restore-packet",
        "context_snapshot": create_v0421_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0421IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0421_integrated_restore_document_manifest(**overrides: Any) -> V0421IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0421-integrated-restore-document-manifest",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "suitable_for_new_session_handoff": True,
        "required_sections": REQUIRED_V0421_RESTORE_SECTIONS,
    }
    return V0421IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _extract_option(args: Sequence[str], option: str) -> str | None:
    if option not in args:
        return None
    index = list(args).index(option)
    if index + 1 >= len(args):
        return None
    return args[index + 1]


def _has_option(args: Sequence[str], option: str) -> bool:
    return option in args


def _has_explicit_default_personal_profile(args: Sequence[str]) -> bool:
    return _extract_option(args, "--profile") == PROFILE_ID


def _inject_home(args: Sequence[str], home_path: str) -> list[str]:
    out = list(args)
    if not out:
        return out
    if out[0] in {"profile", "provider", "prompt", "session", "trace", "safety"} and len(out) >= 2:
        return out[:2] + ["--home", home_path] + out[2:]
    if out[0] == "run-report" and len(out) >= 2:
        return out[:2] + ["--home", home_path] + out[2:]
    if out[0] == "init" and len(out) >= 2:
        return out[:2] + ["--home", home_path] + out[2:]
    if out[0] == "run":
        return out[:1] + ["--home", home_path] + out[1:]
    return out + ["--home", home_path]


def _adopts_omitted_home(args: Sequence[str]) -> bool:
    if not args or "--home" in args:
        return False
    first = args[0]
    second = args[1] if len(args) > 1 else ""
    if first == "init" and second == "default-personal":
        return True
    if not _has_explicit_default_personal_profile(args):
        return False
    if first == "run" and _extract_option(args, "--provider") is None:
        return False
    return (
        first == "run"
        or (first, second)
        in {
            ("profile", "status"),
            ("provider", "doctor"),
            ("prompt", "preview"),
            ("session", "new"),
            ("session", "list"),
            ("trace", "recent"),
            ("trace", "summary"),
            ("run-report", "last"),
            ("safety", "check-command"),
        }
    )


def _command_name(args: Sequence[str]) -> str:
    if not args:
        return ""
    if args[0] == "run":
        return "run"
    if len(args) >= 2:
        return f"{args[0]} {args[1]}"
    return args[0]


def _resolve_for_cli(args: Sequence[str], allow_create: bool) -> V042ResolvedHome:
    request = create_v042_home_resolution_request(
        explicit_home=None,
        command_name=_command_name(args),
        allow_create=allow_create,
        cwd=os.getcwd(),
    )
    return resolve_v042_home(request)


def _print_missing_home(resolved: V042ResolvedHome) -> None:
    print(
        "\n".join(
            (
                "ChantaCore home is not ready.",
                f"resolved_home: {resolved.home_path or '(unresolved)'}",
                f"source: {resolved.source}",
                f"status: {resolved.status}",
                "next: run chanta-cli quickstart, pass --home, or set CHANTACORE_HOME.",
            )
        )
    )


def _handle_home(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli home")
    subparsers = parser.add_subparsers(dest="command", required=True)
    show = subparsers.add_parser("show")
    show.add_argument("--home")
    show.add_argument("--json", action="store_true")
    status = subparsers.add_parser("status")
    status.add_argument("--home")
    status.add_argument("--profile", default=PROFILE_ID)
    status.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    if parsed.command == "show":
        result = create_v042_home_show_command_result(create_v042_home_show_command_input(parsed.home, "home show", parsed.json), cwd=os.getcwd())
    else:
        result = create_v042_home_status_command_result(create_v042_home_status_command_input(parsed.home, parsed.profile, parsed.json), cwd=os.getcwd())
    print(result.rendered_text)
    return result.exit_code


def _handle_quickstart(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli quickstart")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--with-mock-run", action="store_true")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    result = run_v042_quickstart(
        explicit_home=parsed.home,
        profile_id=parsed.profile,
        with_mock_run=parsed.with_mock_run,
        json_output=parsed.json,
        cwd=os.getcwd(),
    )
    print(result.rendered_text)
    return result.exit_code


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        return _v0416_main(args)
    if args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0421_VERSION}; {V0421_RELEASE_NAME})")
        return 0
    if args[0] == "home":
        return _handle_home(args[1:])
    if args[0] == "quickstart":
        return _handle_quickstart(args[1:])
    if _adopts_omitted_home(args):
        allow_create = args[0] == "init"
        resolved = _resolve_for_cli(args, allow_create=allow_create)
        if not resolved.home_path or not resolved.safe_to_use:
            _print_missing_home(resolved)
            return 1
        if not allow_create and not resolved.exists:
            _print_missing_home(resolved)
            return 1
        return _v0416_main(_inject_home(args, resolved.home_path))
    return _v0416_main(args)


__all__ = [
    "V042HomeResolutionSource",
    "V042HomeResolutionStatus",
    "V042DefaultHomePlatform",
    "V042DefaultHomePolicy",
    "V042HomeResolutionRequest",
    "V042ResolvedHome",
    "V042HomeValidationFinding",
    "V042HomeValidationReport",
    "V042HomeShowCommandInput",
    "V042HomeShowCommandResult",
    "V042HomeStatusCommandInput",
    "V042HomeStatusCommandResult",
    "V042CommandHomeAdoptionRecord",
    "V042QuickstartMode",
    "V042QuickstartStepKind",
    "V042QuickstartStepStatus",
    "V042QuickstartStep",
    "V042QuickstartPlan",
    "V042QuickstartMockRunPolicy",
    "V042QuickstartMockRunResult",
    "V042QuickstartNextAction",
    "V042QuickstartResult",
    "V042QuickstartSafetyReport",
    "V0421ReadinessReport",
    "V0422ProviderSetupUXHandoff",
    "V0421IntegratedRestoreSection",
    "V0421IntegratedRestoreContextSnapshot",
    "V0421IntegratedRestorePacket",
    "V0421IntegratedRestoreDocumentManifest",
    "create_v042_default_home_policy",
    "detect_v042_platform",
    "create_v042_home_resolution_request",
    "resolve_v042_home",
    "validate_v042_resolved_home",
    "create_v042_home_validation_report",
    "create_v042_home_show_command_input",
    "create_v042_home_show_command_result",
    "create_v042_home_status_command_input",
    "create_v042_home_status_command_result",
    "create_v042_command_home_adoption_record",
    "build_v042_command_home_adoption_records",
    "create_v042_quickstart_step",
    "create_v042_quickstart_plan",
    "create_v042_quickstart_mock_run_policy",
    "create_v042_quickstart_mock_run_result",
    "create_v042_quickstart_next_action",
    "run_v042_quickstart",
    "create_v042_quickstart_result",
    "create_v042_quickstart_safety_report",
    "create_v0421_readiness_report",
    "create_v0422_provider_setup_ux_handoff",
    "create_v0421_integrated_restore_context_snapshot",
    "create_v0421_integrated_restore_packet",
    "create_v0421_integrated_restore_document_manifest",
    "main",
]
