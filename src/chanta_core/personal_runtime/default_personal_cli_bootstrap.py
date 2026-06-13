"""v0.41.1 installable chanta-cli bootstrap and doctor support.

The only bounded write path is explicit ``init default-personal`` profile
bootstrap under the selected home path. All provider, prompt, AgentLoop, skill,
trace, shell, network, subagent, and production surfaces remain closed.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from dataclasses import asdict, dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Sequence

from chanta_core.personal_runtime.default_personal_profile_runtime import (
    V0416_TARGET_COMMANDS,
    create_default_personal_profile_safety_posture,
)


V0411_VERSION = "v0.41.1"
V0411_RELEASE_NAME = "v0.41.1 Installable CLI Bootstrap & Doctor"
V0411_TRACK_NAME = "v0.41 Default Personal Runtime Opening Track"
CLI_NAME = "chanta-cli"
PROFILE_ID = "default-personal"
INTEGRATED_DOC_PATH = "docs/versions/v0.41/v0.41.1_installable_cli_bootstrap_doctor_restore.md"
V0410_RESTORE_DOC_PATH = "docs/versions/v0.41/v0.41.0_default_personal_profile_runtime_restore.md"
V0409_RESTORE_DOC_PATH = (
    "docs/versions/v0.40/"
    "v0.40.9_controlled_mission_loop_preparation_consolidation_v041_handoff_restore.md"
)


class ChantaCLICommandKind(StrEnum):
    VERSION = "version"
    DOCTOR = "doctor"
    INIT_DEFAULT_PERSONAL = "init_default_personal"
    PROFILE_STATUS = "profile_status"
    UNSUPPORTED_FUTURE_GATED = "unsupported_future_gated"
    UNSAFE_DENIED = "unsafe_denied"
    UNKNOWN = "unknown"


class ChantaCLICommandStatus(StrEnum):
    OK = "ok"
    WARNING = "warning"
    FAILED = "failed"
    UNSUPPORTED = "unsupported"
    UNSAFE_DENIED = "unsafe_denied"
    FUTURE_GATED = "future_gated"
    NOT_IMPLEMENTED = "not_implemented"
    NO_OP = "no_op"


class ChantaCLIDoctorCheckKind(StrEnum):
    PYTHON_VERSION = "python_version"
    PACKAGE_IMPORT = "package_import"
    CLI_ENTRYPOINT = "cli_entrypoint"
    CWD = "cwd"
    PERSONAL_HOME = "personal_home"
    PROFILE_HOME = "profile_home"
    PROFILE_CONFIG = "profile_config"
    IDENTITY_FILES = "identity_files"
    POLICY_FILES = "policy_files"
    RESTORE_DOCS = "restore_docs"
    V0409_HANDOFF_DOC = "v0409_handoff_doc"
    V0410_PROFILE_RUNTIME = "v0410_profile_runtime"
    CLOSED_CAPABILITIES = "closed_capabilities"
    NEXT_VERSION_HANDOFF = "next_version_handoff"


OPEN_CAPABILITIES: tuple[str, ...] = (
    "default_personal_profile_runtime_foundation",
    "installable_cli_bootstrap",
    "chanta_cli_entrypoint",
    "cli_version_command",
    "cli_doctor_command",
    "init_default_personal_command",
    "profile_status_command",
    "unsupported_command_denial",
    "integrated_restore_document",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "run_command",
    "ask_command",
    "provider_doctor",
    "prompt_preview",
    "session_store",
    "provider_text_only_invocation",
    "read_only_skill_registry",
    "read_only_skill_execution",
    "minimal_agent_loop",
    "trace_emission",
    "user_test_release",
    "file_write_outside_profile_init",
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
    "ready_for_run_command",
    "ready_for_ask_command",
    "ready_for_provider_doctor",
    "ready_for_prompt_preview",
    "ready_for_session_store",
    "ready_for_provider_text_only_invocation",
    "ready_for_read_only_skill_registry",
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
    "v0410_profile_runtime_summary",
    "installable_cli_bootstrap_summary",
    "chanta_cli_entrypoint_contract",
    "cli_command_catalog",
    "doctor_contract",
    "init_default_personal_contract",
    "profile_status_contract",
    "unsupported_command_policy",
    "safety_posture",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0412_handoff",
    "v0416_user_test_target",
    "copy_paste_restore_prompt",
)
FUTURE_GATED_COMMANDS: tuple[str, ...] = (
    "run",
    "ask",
    "provider",
    "prompt",
    "session",
    "skills",
    "trace",
    "apply",
    "edit",
    "write",
    "shell",
    "test",
    "retest",
    "invoke-subagent",
    "auto",
    "retry-loop",
    "dominion",
    "production-certify",
)


@dataclass(frozen=True)
class ChantaCLIVersionInfo:
    package_name: str
    cli_name: str
    version: str
    track: str
    command_name: str


@dataclass(frozen=True)
class ChantaCLICommandResult:
    result_id: str
    command_kind: str
    status: str
    message: str
    exit_code: int
    rendered_text: str
    mutated_filesystem: bool
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool
    skill_executed: bool
    shell_executed: bool
    network_accessed: bool
    credentials_accessed: bool
    created_child_session: bool
    invoked_subagent: bool
    production_certified: bool


@dataclass(frozen=True)
class ChantaCLIUnsupportedCommandDecision:
    command_name: str
    requested_args: tuple[str, ...]
    status: str
    blocked: bool
    future_target_version: str | None
    reason: str
    safe_alternative: str
    executed: bool


@dataclass(frozen=True)
class ChantaCLIBootstrapConfig:
    cli_name: str
    default_profile_id: str
    default_home_env_var: str
    default_home_path_hint: str
    supports_init: bool
    supports_doctor: bool
    supports_profile_status: bool
    supports_run: bool
    supports_provider_doctor: bool
    supports_trace: bool


@dataclass(frozen=True)
class ChantaCLIBootstrapPaths:
    home_path: str
    profiles_dir: str
    default_profile_dir: str
    profile_config_path: str
    soul_path: str
    role_path: str
    domain_path: str
    policy_path: str
    core_memory_path: str
    sessions_dir: str
    traces_dir: str
    runtime_dir: str


@dataclass(frozen=True)
class ChantaCLIDoctorCheckResult:
    check_id: str
    check_kind: str
    status: str
    message: str
    details: dict[str, object]
    blocks_v0411: bool
    blocks_v0416: bool


@dataclass(frozen=True)
class ChantaCLIDoctorReport:
    report_id: str
    cli_name: str
    current_version: str
    profile_id: str
    home_path: str | None
    checks: tuple[ChantaCLIDoctorCheckResult, ...]
    closed_capabilities: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    next_recommended_version: str
    ready_for_v0411: bool
    ready_for_v0416_user_test: bool


@dataclass(frozen=True)
class DefaultPersonalInitRequest:
    request_id: str
    profile_id: str
    home_path: str
    allow_overwrite: bool
    dry_run: bool


@dataclass(frozen=True)
class DefaultPersonalInitFileSpec:
    path: str
    description: str
    default_content: str
    create_if_missing: bool
    overwrite_existing: bool


@dataclass(frozen=True)
class DefaultPersonalInitDirectorySpec:
    path: str
    description: str
    create_if_missing: bool


@dataclass(frozen=True)
class DefaultPersonalInitPlan:
    plan_id: str
    profile_id: str
    home_path: str
    directories: tuple[DefaultPersonalInitDirectorySpec, ...]
    files: tuple[DefaultPersonalInitFileSpec, ...]
    safe_to_execute: bool
    outside_home_paths: tuple[str, ...]


@dataclass(frozen=True)
class DefaultPersonalInitResult:
    result_id: str
    request_id: str
    profile_id: str
    home_path: str
    status: str
    created_directories: tuple[str, ...]
    existing_directories: tuple[str, ...]
    created_files: tuple[str, ...]
    existing_files: tuple[str, ...]
    skipped_files: tuple[str, ...]
    overwritten_files: tuple[str, ...]
    outside_home_paths: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool
    shell_executed: bool
    network_accessed: bool
    credentials_accessed: bool


@dataclass(frozen=True)
class DefaultPersonalInitIdempotencyReport:
    report_id: str
    first_run_result: DefaultPersonalInitResult | None
    second_run_result: DefaultPersonalInitResult | None
    idempotent: bool
    overwrite_detected: bool
    unsafe_path_detected: bool


@dataclass(frozen=True)
class DefaultPersonalProfileStatusCommandInput:
    profile_id: str
    home_path: str | None


@dataclass(frozen=True)
class DefaultPersonalProfileStatusCommandResult:
    profile_id: str
    home_path: str
    profile_exists: bool
    profile_config_exists: bool
    soul_exists: bool
    role_exists: bool
    domain_exists: bool
    policy_exists: bool
    core_memory_exists: bool
    sessions_dir_exists: bool
    traces_dir_exists: bool
    status: str
    message: str
    runtime_opened: bool
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    agent_loop_allowed: bool
    skill_execution_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class ChantaCLISafetyPostureReport:
    report_id: str
    cli_name: str
    deny_first: bool
    run_allowed: bool
    provider_doctor_allowed: bool
    prompt_preview_allowed: bool
    session_store_allowed: bool
    trace_allowed: bool
    apply_allowed: bool
    edit_allowed: bool
    shell_allowed: bool
    test_execution_allowed: bool
    subagent_allowed: bool
    dominion_allowed: bool
    production_certified: bool
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0411ReadinessReport:
    report_id: str
    installable_cli_bootstrap_defined: bool
    chanta_cli_entrypoint_ready: bool
    cli_version_ready: bool
    cli_doctor_ready: bool
    default_personal_init_ready: bool
    profile_status_command_ready: bool
    unsupported_command_denial_ready: bool
    integrated_restore_document_ready: bool
    v0412_handoff_ready: bool
    ready_for_run_command: bool
    ready_for_ask_command: bool
    ready_for_provider_doctor: bool
    ready_for_prompt_preview: bool
    ready_for_session_store: bool
    ready_for_provider_text_only_invocation: bool
    ready_for_read_only_skill_registry: bool
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
class V0412PromptAssemblySessionStoreHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0416UserTestTargetUpdate:
    target_id: str
    target_version: str
    commands: tuple[str, ...]
    commands_expected_in_v0411: tuple[str, ...]
    user_test_release_ready: bool


@dataclass(frozen=True)
class V0411IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0411IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0411IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0411IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0411IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0411IntegratedRestoreDocumentManifest:
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


def _is_under_home(path: str, home_path: str) -> bool:
    try:
        Path(path).resolve().relative_to(Path(home_path).resolve())
        return True
    except ValueError:
        return False


def _default_file_content(description: str) -> str:
    return f"# {description}\n\nCreated by chanta-cli v0.41.1 default-personal bootstrap.\n"


def create_cli_version_info(**overrides: Any) -> ChantaCLIVersionInfo:
    defaults = {
        "package_name": "chanta-core",
        "cli_name": CLI_NAME,
        "version": V0411_VERSION,
        "track": V0411_TRACK_NAME,
        "command_name": CLI_NAME,
    }
    return ChantaCLIVersionInfo(**_merge(defaults, overrides))


def classify_cli_command(args: Sequence[str]) -> str:
    if not args or args[0] in {"--version", "-V", "version"}:
        return ChantaCLICommandKind.VERSION.value
    if args[0] == "doctor":
        return ChantaCLICommandKind.DOCTOR.value
    if tuple(args[:2]) == ("init", PROFILE_ID):
        return ChantaCLICommandKind.INIT_DEFAULT_PERSONAL.value
    if tuple(args[:2]) == ("profile", "status"):
        return ChantaCLICommandKind.PROFILE_STATUS.value
    if args[0] in FUTURE_GATED_COMMANDS:
        unsafe = args[0] in {"apply", "edit", "write", "shell", "test", "retest", "invoke-subagent", "auto", "retry-loop", "dominion", "production-certify"}
        return ChantaCLICommandKind.UNSAFE_DENIED.value if unsafe else ChantaCLICommandKind.UNSUPPORTED_FUTURE_GATED.value
    return ChantaCLICommandKind.UNKNOWN.value


def create_cli_command_result(**overrides: Any) -> ChantaCLICommandResult:
    defaults = {
        "result_id": "chanta-cli-result",
        "command_kind": ChantaCLICommandKind.VERSION.value,
        "status": ChantaCLICommandStatus.OK.value,
        "message": "ok",
        "exit_code": 0,
        "rendered_text": "ok",
        "mutated_filesystem": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "agent_loop_started": False,
        "skill_executed": False,
        "shell_executed": False,
        "network_accessed": False,
        "credentials_accessed": False,
        "created_child_session": False,
        "invoked_subagent": False,
        "production_certified": False,
    }
    return ChantaCLICommandResult(**_merge(defaults, overrides))


def create_unsupported_command_decision(
    command_name: str,
    requested_args: Sequence[str] = (),
    **overrides: Any,
) -> ChantaCLIUnsupportedCommandDecision:
    if command_name in {"run", "ask"}:
        target = "v0.41.4"
        status = ChantaCLICommandStatus.FUTURE_GATED.value
    elif command_name == "provider":
        target = "v0.41.3"
        status = ChantaCLICommandStatus.FUTURE_GATED.value
    elif command_name in {"prompt", "session"}:
        target = "v0.41.2"
        status = ChantaCLICommandStatus.FUTURE_GATED.value
    elif command_name == "trace":
        target = "v0.41.5"
        status = ChantaCLICommandStatus.FUTURE_GATED.value
    elif command_name == "skills":
        target = "v0.41.3"
        status = ChantaCLICommandStatus.FUTURE_GATED.value
    elif command_name in {"apply", "edit", "write", "shell", "test", "retest", "invoke-subagent", "auto", "retry-loop", "dominion", "production-certify"}:
        target = "not_planned_in_v041" if command_name in {"dominion", "production-certify"} else "v0.42+"
        status = ChantaCLICommandStatus.UNSAFE_DENIED.value
    else:
        target = None
        status = ChantaCLICommandStatus.UNSUPPORTED.value
    defaults = {
        "command_name": command_name,
        "requested_args": tuple(requested_args),
        "status": status,
        "blocked": True,
        "future_target_version": target,
        "reason": f"{command_name} is not opened in v0.41.1.",
        "safe_alternative": "chanta-cli doctor",
        "executed": False,
    }
    return ChantaCLIUnsupportedCommandDecision(**_merge(defaults, overrides))


def create_cli_bootstrap_config(**overrides: Any) -> ChantaCLIBootstrapConfig:
    defaults = {
        "cli_name": CLI_NAME,
        "default_profile_id": PROFILE_ID,
        "default_home_env_var": "LOCALAPPDATA",
        "default_home_path_hint": "$env:LOCALAPPDATA/ChantaCore",
        "supports_init": True,
        "supports_doctor": True,
        "supports_profile_status": True,
        "supports_run": False,
        "supports_provider_doctor": False,
        "supports_trace": False,
    }
    return ChantaCLIBootstrapConfig(**_merge(defaults, overrides))


def create_cli_bootstrap_paths(home_path: str | None = None, **overrides: Any) -> ChantaCLIBootstrapPaths:
    home = _home_path(home_path)
    profile_dir = str(Path(home) / "profiles" / PROFILE_ID)
    defaults = {
        "home_path": home,
        "profiles_dir": str(Path(home) / "profiles"),
        "default_profile_dir": profile_dir,
        "profile_config_path": str(Path(profile_dir) / "profile.json"),
        "soul_path": str(Path(profile_dir) / "soul" / "SOUL.md"),
        "role_path": str(Path(profile_dir) / "profile" / "ROLE.json"),
        "domain_path": str(Path(profile_dir) / "profile" / "DOMAIN.json"),
        "policy_path": str(Path(profile_dir) / "profile" / "POLICY.json"),
        "core_memory_path": str(Path(profile_dir) / "memory" / "CORE_MEMORY.md"),
        "sessions_dir": str(Path(profile_dir) / "state" / "sessions"),
        "traces_dir": str(Path(profile_dir) / "state" / "traces"),
        "runtime_dir": str(Path(profile_dir) / "runtime"),
    }
    return ChantaCLIBootstrapPaths(**_merge(defaults, overrides))


def _path_details(path: str) -> dict[str, object]:
    p = Path(path)
    return {"path": path, "exists": p.exists(), "is_dir": p.is_dir()}


def run_cli_doctor_checks(home_path: str | None = None) -> tuple[ChantaCLIDoctorCheckResult, ...]:
    paths = create_cli_bootstrap_paths(home_path)
    try:
        importlib.import_module("chanta_core")
        package_status = "pass"
        package_message = "chanta_core import ok"
    except Exception as exc:  # pragma: no cover - defensive metadata path
        package_status = "fail"
        package_message = f"chanta_core import failed: {exc}"
    checks = (
        ChantaCLIDoctorCheckResult(
            "doctor-python-version",
            ChantaCLIDoctorCheckKind.PYTHON_VERSION.value,
            "pass" if sys.version_info >= (3, 11) else "fail",
            sys.version.split()[0],
            {"major": sys.version_info.major, "minor": sys.version_info.minor},
            False,
            sys.version_info < (3, 11),
        ),
        ChantaCLIDoctorCheckResult(
            "doctor-package-import",
            ChantaCLIDoctorCheckKind.PACKAGE_IMPORT.value,
            package_status,
            package_message,
            {},
            package_status == "fail",
            package_status == "fail",
        ),
        ChantaCLIDoctorCheckResult(
            "doctor-cli-entrypoint",
            ChantaCLIDoctorCheckKind.CLI_ENTRYPOINT.value,
            "pass",
            "chanta-cli entrypoint is wired to chanta_core.cli.main:main",
            {"cli_name": CLI_NAME},
            False,
            False,
        ),
        ChantaCLIDoctorCheckResult("doctor-cwd", ChantaCLIDoctorCheckKind.CWD.value, "advisory", str(Path.cwd()), {}, False, False),
        ChantaCLIDoctorCheckResult("doctor-home", ChantaCLIDoctorCheckKind.PERSONAL_HOME.value, "advisory", paths.home_path, _path_details(paths.home_path), False, False),
        ChantaCLIDoctorCheckResult("doctor-profile-home", ChantaCLIDoctorCheckKind.PROFILE_HOME.value, "advisory", paths.default_profile_dir, _path_details(paths.default_profile_dir), False, False),
        ChantaCLIDoctorCheckResult("doctor-profile-config", ChantaCLIDoctorCheckKind.PROFILE_CONFIG.value, "pass" if Path(paths.profile_config_path).exists() else "warn", paths.profile_config_path, _path_details(paths.profile_config_path), False, True),
        ChantaCLIDoctorCheckResult("doctor-identity", ChantaCLIDoctorCheckKind.IDENTITY_FILES.value, "pass" if all(Path(p).exists() for p in (paths.soul_path, paths.role_path, paths.domain_path, paths.core_memory_path)) else "warn", "identity placeholders checked", {}, False, True),
        ChantaCLIDoctorCheckResult("doctor-policy", ChantaCLIDoctorCheckKind.POLICY_FILES.value, "pass" if Path(paths.policy_path).exists() else "warn", paths.policy_path, _path_details(paths.policy_path), False, True),
        ChantaCLIDoctorCheckResult("doctor-restore-docs", ChantaCLIDoctorCheckKind.RESTORE_DOCS.value, "pass" if Path(V0410_RESTORE_DOC_PATH).exists() else "warn", V0410_RESTORE_DOC_PATH, _path_details(V0410_RESTORE_DOC_PATH), False, False),
        ChantaCLIDoctorCheckResult("doctor-v0409", ChantaCLIDoctorCheckKind.V0409_HANDOFF_DOC.value, "pass" if Path(V0409_RESTORE_DOC_PATH).exists() else "warn", V0409_RESTORE_DOC_PATH, _path_details(V0409_RESTORE_DOC_PATH), False, False),
        ChantaCLIDoctorCheckResult("doctor-v0410", ChantaCLIDoctorCheckKind.V0410_PROFILE_RUNTIME.value, "pass", "v0.41.0 profile runtime import available", {}, False, False),
        ChantaCLIDoctorCheckResult("doctor-closed", ChantaCLIDoctorCheckKind.CLOSED_CAPABILITIES.value, "pass", "unsafe capabilities remain closed", {"closed": CLOSED_CAPABILITIES}, False, False),
        ChantaCLIDoctorCheckResult("doctor-handoff", ChantaCLIDoctorCheckKind.NEXT_VERSION_HANDOFF.value, "pass", "v0.41.2 Prompt Assembly & Session Store", {}, False, False),
    )
    return checks


def create_cli_doctor_report(home_path: str | None = None, **overrides: Any) -> ChantaCLIDoctorReport:
    checks = run_cli_doctor_checks(home_path)
    defaults = {
        "report_id": "chanta-cli-doctor-v0411",
        "cli_name": CLI_NAME,
        "current_version": V0411_VERSION,
        "profile_id": PROFILE_ID,
        "home_path": _home_path(home_path) if home_path else None,
        "checks": checks,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "open_capabilities": OPEN_CAPABILITIES,
        "next_recommended_version": "v0.41.2",
        "ready_for_v0411": not any(check.blocks_v0411 for check in checks),
        "ready_for_v0416_user_test": False,
    }
    return ChantaCLIDoctorReport(**_merge(defaults, overrides))


def create_default_personal_init_request(
    home_path: str,
    dry_run: bool = False,
    **overrides: Any,
) -> DefaultPersonalInitRequest:
    defaults = {
        "request_id": "default-personal-init-request-v0411",
        "profile_id": PROFILE_ID,
        "home_path": _home_path(home_path),
        "allow_overwrite": False,
        "dry_run": dry_run,
    }
    return DefaultPersonalInitRequest(**_merge(defaults, overrides))


def create_default_personal_init_plan(
    request: DefaultPersonalInitRequest,
    **overrides: Any,
) -> DefaultPersonalInitPlan:
    if request.profile_id != PROFILE_ID:
        raise ValueError("v0.41.1 init supports only default-personal")
    paths = create_cli_bootstrap_paths(request.home_path)
    directories = tuple(
        DefaultPersonalInitDirectorySpec(path, description, True)
        for path, description in (
            (paths.home_path, "Personal runtime home"),
            (paths.profiles_dir, "Profiles directory"),
            (paths.default_profile_dir, "Default Personal profile directory"),
            (str(Path(paths.soul_path).parent), "Soul directory"),
            (str(Path(paths.role_path).parent), "Profile metadata directory"),
            (str(Path(paths.core_memory_path).parent), "Memory directory"),
            (paths.sessions_dir, "Sessions directory"),
            (paths.traces_dir, "Traces directory"),
            (paths.runtime_dir, "Runtime cache directory"),
        )
    )
    profile_payload = json.dumps(
        {
            "profile_id": PROFILE_ID,
            "profile_kind": "default_personal",
            "display_name": "Default Personal",
            "provider_invocation_allowed": False,
            "prompt_submission_allowed": False,
            "agent_loop_allowed": False,
            "skill_execution_allowed": False,
            "production_certified": False,
        },
        indent=2,
        sort_keys=True,
    )
    files = (
        DefaultPersonalInitFileSpec(paths.profile_config_path, "Default Personal profile config", profile_payload + "\n", True, False),
        DefaultPersonalInitFileSpec(paths.soul_path, "Default Personal soul placeholder", _default_file_content("SOUL placeholder"), True, False),
        DefaultPersonalInitFileSpec(paths.role_path, "Default Personal role placeholder", '{"role": "default_personal", "runtime_authority": false}\n', True, False),
        DefaultPersonalInitFileSpec(paths.domain_path, "Default Personal domain placeholder", '{"domain": "default", "provider_invocation_allowed": false}\n', True, False),
        DefaultPersonalInitFileSpec(paths.policy_path, "Default Personal policy placeholder", '{"deny_first": true, "production_certified": false}\n', True, False),
        DefaultPersonalInitFileSpec(paths.core_memory_path, "Default Personal core memory placeholder", _default_file_content("CORE_MEMORY placeholder"), True, False),
    )
    outside = tuple(
        path
        for path in [*(directory.path for directory in directories), *(file.path for file in files)]
        if not _is_under_home(path, paths.home_path)
    )
    defaults = {
        "plan_id": "default-personal-init-plan-v0411",
        "profile_id": request.profile_id,
        "home_path": paths.home_path,
        "directories": directories,
        "files": files,
        "safe_to_execute": not outside,
        "outside_home_paths": outside,
    }
    return DefaultPersonalInitPlan(**_merge(defaults, overrides))


def create_default_personal_init_result(
    request: DefaultPersonalInitRequest,
    plan: DefaultPersonalInitPlan,
    **overrides: Any,
) -> DefaultPersonalInitResult:
    defaults = {
        "result_id": "default-personal-init-result-v0411",
        "request_id": request.request_id,
        "profile_id": request.profile_id,
        "home_path": request.home_path,
        "status": ChantaCLICommandStatus.NO_OP.value if request.dry_run else ChantaCLICommandStatus.OK.value,
        "created_directories": (),
        "existing_directories": (),
        "created_files": (),
        "existing_files": (),
        "skipped_files": (),
        "overwritten_files": (),
        "outside_home_paths": plan.outside_home_paths,
        "provider_invoked": False,
        "prompt_submitted": False,
        "agent_loop_started": False,
        "shell_executed": False,
        "network_accessed": False,
        "credentials_accessed": False,
    }
    return DefaultPersonalInitResult(**_merge(defaults, overrides))


def execute_default_personal_init_plan(request: DefaultPersonalInitRequest, plan: DefaultPersonalInitPlan) -> DefaultPersonalInitResult:
    if not plan.safe_to_execute:
        return create_default_personal_init_result(request, plan, status=ChantaCLICommandStatus.UNSAFE_DENIED.value)
    if request.allow_overwrite:
        raise ValueError("v0.41.1 init does not support overwrite")
    created_dirs: list[str] = []
    existing_dirs: list[str] = []
    created_files: list[str] = []
    existing_files: list[str] = []
    skipped_files: list[str] = []
    if not request.dry_run:
        for directory in plan.directories:
            path = Path(directory.path)
            if path.exists():
                existing_dirs.append(directory.path)
            elif directory.create_if_missing:
                path.mkdir(parents=True, exist_ok=True)
                created_dirs.append(directory.path)
        for file_spec in plan.files:
            path = Path(file_spec.path)
            if path.exists():
                existing_files.append(file_spec.path)
                skipped_files.append(file_spec.path)
            elif file_spec.create_if_missing:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(file_spec.default_content, encoding="utf-8")
                created_files.append(file_spec.path)
    return create_default_personal_init_result(
        request,
        plan,
        created_directories=tuple(created_dirs),
        existing_directories=tuple(existing_dirs),
        created_files=tuple(created_files),
        existing_files=tuple(existing_files),
        skipped_files=tuple(skipped_files),
    )


def create_default_personal_idempotency_report(
    first_run_result: DefaultPersonalInitResult | None,
    second_run_result: DefaultPersonalInitResult | None,
    **overrides: Any,
) -> DefaultPersonalInitIdempotencyReport:
    defaults = {
        "report_id": "default-personal-init-idempotency-v0411",
        "first_run_result": first_run_result,
        "second_run_result": second_run_result,
        "idempotent": bool(second_run_result and not second_run_result.created_files and not second_run_result.overwritten_files),
        "overwrite_detected": bool(
            (first_run_result and first_run_result.overwritten_files)
            or (second_run_result and second_run_result.overwritten_files)
        ),
        "unsafe_path_detected": bool(
            (first_run_result and first_run_result.outside_home_paths)
            or (second_run_result and second_run_result.outside_home_paths)
        ),
    }
    return DefaultPersonalInitIdempotencyReport(**_merge(defaults, overrides))


def run_profile_status_command(
    command_input: "DefaultPersonalProfileStatusCommandInput",
    **overrides: Any,
) -> DefaultPersonalProfileStatusCommandResult:
    if command_input.profile_id != PROFILE_ID:
        raise ValueError("v0.41.1 profile status supports only default-personal")
    paths = create_cli_bootstrap_paths(command_input.home_path)
    profile_exists = Path(paths.default_profile_dir).exists()
    config_exists = Path(paths.profile_config_path).exists()
    result_status = "ready_for_v0412" if profile_exists and config_exists else "missing_or_partial"
    defaults = {
        "profile_id": command_input.profile_id,
        "home_path": paths.home_path,
        "profile_exists": profile_exists,
        "profile_config_exists": config_exists,
        "soul_exists": Path(paths.soul_path).exists(),
        "role_exists": Path(paths.role_path).exists(),
        "domain_exists": Path(paths.domain_path).exists(),
        "policy_exists": Path(paths.policy_path).exists(),
        "core_memory_exists": Path(paths.core_memory_path).exists(),
        "sessions_dir_exists": Path(paths.sessions_dir).exists(),
        "traces_dir_exists": Path(paths.traces_dir).exists(),
        "status": result_status,
        "message": f"default-personal profile status: {result_status}",
        "runtime_opened": False,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "agent_loop_allowed": False,
        "skill_execution_allowed": False,
        "production_certified": False,
    }
    return DefaultPersonalProfileStatusCommandResult(**_merge(defaults, overrides))


def create_cli_safety_posture_report(**overrides: Any) -> ChantaCLISafetyPostureReport:
    create_default_personal_profile_safety_posture()
    defaults = {
        "report_id": "chanta-cli-safety-posture-v0411",
        "cli_name": CLI_NAME,
        "deny_first": True,
        "run_allowed": False,
        "provider_doctor_allowed": False,
        "prompt_preview_allowed": False,
        "session_store_allowed": False,
        "trace_allowed": False,
        "apply_allowed": False,
        "edit_allowed": False,
        "shell_allowed": False,
        "test_execution_allowed": False,
        "subagent_allowed": False,
        "dominion_allowed": False,
        "production_certified": False,
        "closed_capabilities": CLOSED_CAPABILITIES,
    }
    return ChantaCLISafetyPostureReport(**_merge(defaults, overrides))


def create_v0411_readiness_report(**overrides: Any) -> V0411ReadinessReport:
    defaults = {
        "report_id": "v0411-readiness-report",
        "installable_cli_bootstrap_defined": True,
        "chanta_cli_entrypoint_ready": True,
        "cli_version_ready": True,
        "cli_doctor_ready": True,
        "default_personal_init_ready": True,
        "profile_status_command_ready": True,
        "unsupported_command_denial_ready": True,
        "integrated_restore_document_ready": True,
        "v0412_handoff_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return V0411ReadinessReport(**_merge(defaults, overrides))


def create_v0412_prompt_assembly_session_store_handoff(**overrides: Any) -> V0412PromptAssemblySessionStoreHandoff:
    defaults = {
        "handoff_id": "v0412-prompt-assembly-session-store-handoff",
        "target_version": "v0.41.2 Prompt Assembly & Session Store",
        "recommended_focus": (
            "define prompt assembly block order",
            "define safety invariant block",
            "define Soul/Role/Domain source loading",
            "define prompt preview command",
            "define append-only session transcript schema",
            "define session new/list",
            "no provider call",
            "no AgentLoop",
            "no skill execution",
            "no trace emission runtime beyond metadata planning",
        ),
        "still_closed": CLOSED_CAPABILITIES,
    }
    return V0412PromptAssemblySessionStoreHandoff(**_merge(defaults, overrides))


def create_v0416_user_test_target_update(**overrides: Any) -> V0416UserTestTargetUpdate:
    defaults = {
        "target_id": "v0416-user-test-target-update-v0411",
        "target_version": "v0.41.6 Installable User-Test Release",
        "commands": V0416_TARGET_COMMANDS,
        "commands_expected_in_v0411": (
            "py -m pip install -e .",
            "chanta-cli --version",
            "chanta-cli doctor",
            'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"',
            "chanta-cli profile status --profile default-personal",
        ),
        "user_test_release_ready": False,
    }
    return V0416UserTestTargetUpdate(**_merge(defaults, overrides))


def create_v0411_integrated_restore_sections() -> tuple[V0411IntegratedRestoreSection, ...]:
    return tuple(
        V0411IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.41.1 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0411_integrated_restore_context_snapshot(**overrides: Any) -> V0411IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0411",
        "current_version": V0411_RELEASE_NAME,
        "current_track": V0411_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            V0411_RELEASE_NAME,
        ),
        "open_capabilities": OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "next_recommended_version": "v0.41.2 Prompt Assembly & Session Store",
    }
    return V0411IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0411_integrated_restore_packet(**overrides: Any) -> V0411IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0411",
        "snapshot": create_v0411_integrated_restore_context_snapshot(),
        "restore_sections": create_v0411_integrated_restore_sections(),
        "required_test_commands": (
            "tests/test_v0411_installable_cli_bootstrap_doctor.py",
            "tests/test_v0410_default_personal_profile_runtime.py",
            "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
        ),
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0411IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0411_integrated_restore_document_manifest(**overrides: Any) -> V0411IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0411",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0411IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def cli_command_result_preserves_runtime_closed(result: ChantaCLICommandResult) -> bool:
    return (
        not result.provider_invoked
        and not result.prompt_submitted
        and not result.agent_loop_started
        and not result.skill_executed
        and not result.shell_executed
        and not result.network_accessed
        and not result.credentials_accessed
        and not result.created_child_session
        and not result.invoked_subagent
        and not result.production_certified
    )


def init_result_preserves_runtime_closed(result: DefaultPersonalInitResult) -> bool:
    return (
        not result.overwritten_files
        and not result.provider_invoked
        and not result.prompt_submitted
        and not result.agent_loop_started
        and not result.shell_executed
        and not result.network_accessed
        and not result.credentials_accessed
    )


def cli_safety_posture_preserves_closed(report: ChantaCLISafetyPostureReport) -> bool:
    return (
        report.deny_first
        and not report.run_allowed
        and not report.provider_doctor_allowed
        and not report.prompt_preview_allowed
        and not report.session_store_allowed
        and not report.trace_allowed
        and not report.apply_allowed
        and not report.edit_allowed
        and not report.shell_allowed
        and not report.test_execution_allowed
        and not report.subagent_allowed
        and not report.dominion_allowed
        and not report.production_certified
    )


def v0411_readiness_preserves_closed_runtime(report: V0411ReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0411IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def render_doctor_report(report: ChantaCLIDoctorReport) -> str:
    lines = [f"{report.cli_name} doctor {report.current_version}", f"next: {report.next_recommended_version}"]
    lines.extend(f"{check.check_kind}: {check.status} - {check.message}" for check in report.checks)
    lines.append("closed: " + ", ".join(report.closed_capabilities))
    return "\n".join(lines)


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    kind = classify_cli_command(args)
    if kind == ChantaCLICommandKind.VERSION.value:
        info = create_cli_version_info()
        print(f"{info.command_name} {info.version}")
        return 0
    if kind == ChantaCLICommandKind.DOCTOR.value:
        parser = argparse.ArgumentParser(prog=CLI_NAME)
        parser.add_argument("doctor")
        parser.add_argument("--home")
        parsed = parser.parse_args(args)
        print(render_doctor_report(create_cli_doctor_report(parsed.home)))
        return 0
    if kind == ChantaCLICommandKind.INIT_DEFAULT_PERSONAL.value:
        parser = argparse.ArgumentParser(prog=CLI_NAME)
        parser.add_argument("init")
        parser.add_argument("profile_id")
        parser.add_argument("--home", required=True)
        parser.add_argument("--dry-run", action="store_true")
        parsed = parser.parse_args(args)
        request = create_default_personal_init_request(parsed.home, dry_run=parsed.dry_run)
        plan = create_default_personal_init_plan(request)
        result = execute_default_personal_init_plan(request, plan)
        print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
        return 0 if result.status in {ChantaCLICommandStatus.OK.value, ChantaCLICommandStatus.NO_OP.value} else 2
    if kind == ChantaCLICommandKind.PROFILE_STATUS.value:
        parser = argparse.ArgumentParser(prog=CLI_NAME)
        parser.add_argument("profile")
        parser.add_argument("status")
        parser.add_argument("--profile", default=PROFILE_ID)
        parser.add_argument("--home")
        parsed = parser.parse_args(args)
        result = run_profile_status_command(DefaultPersonalProfileStatusCommandInput(parsed.profile, parsed.home))
        print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
        return 0
    command = args[0] if args else "unknown"
    decision = create_unsupported_command_decision(command, args)
    print(json.dumps(asdict(decision), ensure_ascii=False, sort_keys=True))
    return 2 if decision.status == ChantaCLICommandStatus.UNSAFE_DENIED.value else 1


__all__ = [
    "CLI_NAME",
    "CLOSED_CAPABILITIES",
    "FUTURE_GATED_COMMANDS",
    "INTEGRATED_DOC_PATH",
    "OPEN_CAPABILITIES",
    "PROFILE_ID",
    "REQUIRED_FALSE_FLAGS",
    "REQUIRED_RESTORE_SECTION_IDS",
    "V0411_RELEASE_NAME",
    "V0411_TRACK_NAME",
    "V0411_VERSION",
    "ChantaCLIBootstrapConfig",
    "ChantaCLIBootstrapPaths",
    "ChantaCLICommandKind",
    "ChantaCLICommandResult",
    "ChantaCLICommandStatus",
    "ChantaCLIDoctorCheckKind",
    "ChantaCLIDoctorCheckResult",
    "ChantaCLIDoctorReport",
    "ChantaCLISafetyPostureReport",
    "ChantaCLIUnsupportedCommandDecision",
    "ChantaCLIVersionInfo",
    "DefaultPersonalInitDirectorySpec",
    "DefaultPersonalInitFileSpec",
    "DefaultPersonalInitIdempotencyReport",
    "DefaultPersonalInitPlan",
    "DefaultPersonalInitRequest",
    "DefaultPersonalInitResult",
    "DefaultPersonalProfileStatusCommandInput",
    "DefaultPersonalProfileStatusCommandResult",
    "V0411IntegratedRestoreContextSnapshot",
    "V0411IntegratedRestoreDocumentManifest",
    "V0411IntegratedRestorePacket",
    "V0411IntegratedRestoreSection",
    "V0411ReadinessReport",
    "V0412PromptAssemblySessionStoreHandoff",
    "V0416UserTestTargetUpdate",
    "classify_cli_command",
    "cli_command_result_preserves_runtime_closed",
    "cli_safety_posture_preserves_closed",
    "create_cli_bootstrap_config",
    "create_cli_bootstrap_paths",
    "create_cli_command_result",
    "create_cli_doctor_report",
    "create_cli_safety_posture_report",
    "create_cli_version_info",
    "create_default_personal_idempotency_report",
    "create_default_personal_init_plan",
    "create_default_personal_init_request",
    "create_default_personal_init_result",
    "create_unsupported_command_decision",
    "create_v0411_integrated_restore_context_snapshot",
    "create_v0411_integrated_restore_document_manifest",
    "create_v0411_integrated_restore_packet",
    "create_v0411_integrated_restore_sections",
    "create_v0411_readiness_report",
    "create_v0412_prompt_assembly_session_store_handoff",
    "create_v0416_user_test_target_update",
    "execute_default_personal_init_plan",
    "init_result_preserves_runtime_closed",
    "integrated_restore_packet_uses_single_doc",
    "main",
    "render_doctor_report",
    "run_cli_doctor_checks",
    "run_profile_status_command",
    "v0411_readiness_preserves_closed_runtime",
]
