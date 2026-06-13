"""v0.41.0 Default Personal profile runtime foundation.

This module defines metadata, config-read, status, restore, and handoff records
for the first Default Personal profile runtime foundation. It does not create
profile files, start CLI commands, submit prompts, call providers, start an
AgentLoop, execute skills, create child sessions, or mutate the filesystem.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any


V0410_VERSION = "v0.41.0"
V0410_RELEASE_NAME = "v0.41.0 Default Personal Profile Runtime Foundation"
V0410_TRACK_NAME = "v0.41 Default Personal Runtime Opening Track"
PROFILE_ID = "default-personal"
INTEGRATED_DOC_PATH = "docs/versions/v0.41/v0.41.0_default_personal_profile_runtime_restore.md"
V0409_RESTORE_DOC_PATH = (
    "docs/versions/v0.40/"
    "v0.40.9_controlled_mission_loop_preparation_consolidation_v041_handoff_restore.md"
)


class DefaultPersonalProfileKind(StrEnum):
    DEFAULT_PERSONAL = "default_personal"
    CUSTOM_PERSONAL = "custom_personal"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class DefaultPersonalProfileStatus(StrEnum):
    UNKNOWN = "unknown"
    MISSING = "missing"
    PARTIAL = "partial"
    LOADED_METADATA_ONLY = "loaded_metadata_only"
    LOADED_WITH_GAPS = "loaded_with_gaps"
    LOAD_BLOCKED = "load_blocked"
    READY_FOR_V0411_CLI_BOOTSTRAP = "ready_for_v0411_cli_bootstrap"
    INVALID = "invalid"


OPEN_CAPABILITIES: tuple[str, ...] = (
    "default_personal_profile_runtime_foundation",
    "personal_runtime_root_model",
    "default_personal_profile_config",
    "profile_status_report",
    "profile_safety_posture",
    "restore_context_ref",
    "v040_compatibility_gate",
    "v0411_handoff",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "cli_entrypoint_bootstrap",
    "profile_init_command",
    "prompt_assembly",
    "session_store",
    "provider_text_only_invocation",
    "read_only_skill_registry",
    "read_only_skill_execution",
    "minimal_agent_loop",
    "trace_emission",
    "user_test_release",
    "file_write",
    "file_edit",
    "patch_apply",
    "shell_execution",
    "test_execution",
    "subagent_invocation",
    "child_session_creation",
    "autonomous_loop",
    "retry_loop",
    "dominion_runtime",
    "production_certification",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_cli_entrypoint",
    "ready_for_profile_init",
    "ready_for_prompt_assembly",
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
    "v0409_handoff_summary",
    "v041_master_design_summary",
    "default_personal_profile_runtime_summary",
    "profile_config_contract",
    "personal_runtime_root_contract",
    "identity_files_contract",
    "policy_files_contract",
    "profile_status_report_contract",
    "profile_safety_posture_contract",
    "restore_context_ref_summary",
    "v040_compatibility_gate_summary",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0411_handoff",
    "v0416_user_test_target",
    "copy_paste_restore_prompt",
)
V0416_TARGET_COMMANDS: tuple[str, ...] = (
    "py -m pip install -e .",
    "chanta-cli --version",
    "chanta-cli doctor",
    'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"',
    "chanta-cli profile status --profile default-personal",
    "chanta-cli provider doctor --profile default-personal --no-completion",
    'chanta-cli run --profile default-personal "Summarize what ChantaCore is in three bullets."',
    "chanta-cli trace recent --profile default-personal --limit 10",
    'chanta-cli safety check-command --profile default-personal --command "Remove-Item -Recurse -Force C:\\"',
)


@dataclass(frozen=True)
class PersonalRuntimeRoot:
    root_id: str
    root_path: str
    profile_home_path: str
    created_by_init: bool
    exists: bool
    writable_checked: bool
    writable: bool | None
    metadata_only: bool


@dataclass(frozen=True)
class DefaultPersonalProfilePaths:
    paths_id: str
    profile_id: str
    profile_home_path: str
    soul_path: str
    role_path: str
    domain_path: str
    policy_path: str
    provider_config_path: str
    session_store_path: str
    trace_store_path: str
    restore_context_path: str | None
    all_paths_metadata_only: bool


@dataclass(frozen=True)
class DefaultPersonalProfileConfig:
    profile_id: str
    profile_kind: str
    display_name: str
    personal_root_ref: str
    profile_home_path: str
    soul_path: str | None
    role_path: str | None
    domain_path: str | None
    policy_path: str | None
    core_memory_path: str | None
    restore_context_path: str | None
    safety_boundary_ref: str | None
    provider_config_path: str | None
    session_store_path: str | None
    trace_store_path: str | None
    profile_is_sandbox: bool
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    agent_loop_allowed: bool
    skill_execution_allowed: bool
    workspace_mutation_allowed: bool
    shell_execution_allowed: bool
    subagent_invocation_allowed: bool
    production_certified: bool
    metadata: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class DefaultPersonalIdentityFiles:
    identity_id: str
    profile_id: str
    soul_path: str | None
    role_path: str | None
    domain_path: str | None
    core_memory_path: str | None
    soul_exists: bool
    role_exists: bool
    domain_exists: bool
    core_memory_exists: bool
    missing_identity_items: tuple[str, ...]


@dataclass(frozen=True)
class DefaultPersonalPolicyFiles:
    policy_id: str
    profile_id: str
    policy_path: str | None
    safety_boundary_ref: str | None
    restore_context_ref: str | None
    policy_exists: bool
    safety_boundary_loaded: bool
    restore_context_loaded: bool
    unsafe_capabilities_closed: bool
    missing_policy_items: tuple[str, ...]


@dataclass(frozen=True)
class RestoreContextRef:
    restore_ref_id: str
    source_version: str
    restore_doc_path: str
    restore_doc_expected: bool
    restore_doc_present: bool
    copy_paste_restore_prompt_expected: bool
    copy_paste_restore_prompt_present: bool
    suitable_for_profile_runtime: bool


@dataclass(frozen=True)
class V040CompatibilityGate:
    gate_id: str
    source_version: str
    v0409_restore_ref: str | None
    unsafe_flags_false_confirmed: bool
    standalone_runtime_was_closed: bool
    provider_runtime_was_closed: bool
    prompt_submission_was_closed: bool
    subagent_runtime_was_closed: bool
    live_apply_was_closed: bool
    compatible_for_v0410_profile_runtime: bool
    compatible_for_v041_runtime_execution: bool


@dataclass(frozen=True)
class DefaultPersonalRuntimeState:
    state_id: str
    profile_id: str
    profile_loaded: bool
    config_valid: bool
    identity_files_status: DefaultPersonalIdentityFiles
    policy_files_status: DefaultPersonalPolicyFiles
    restore_context_ref: RestoreContextRef | None
    v040_compatibility_gate: V040CompatibilityGate
    runtime_opened: bool
    provider_ready: bool
    prompt_assembly_ready: bool
    session_store_ready: bool
    agent_loop_ready: bool
    skill_registry_ready: bool
    trace_emission_ready: bool
    user_test_ready: bool
    blocking_gaps: tuple[str, ...]
    non_blocking_gaps: tuple[str, ...]


@dataclass(frozen=True)
class DefaultPersonalProfileLoadRequest:
    request_id: str
    profile_id: str
    personal_root_path: str | None
    profile_home_path: str | None
    allow_filesystem_read: bool
    allow_filesystem_write: bool
    allow_profile_creation: bool
    metadata_only: bool


@dataclass(frozen=True)
class DefaultPersonalProfileMissingItem:
    item_id: str
    profile_id: str
    item_kind: str
    path: str | None
    severity: str
    blocks_v0410: bool
    blocks_v0411: bool
    blocks_v0416_user_test: bool
    recommendation: str


@dataclass(frozen=True)
class DefaultPersonalProfileValidationFinding:
    finding_id: str
    severity: str
    field_name: str
    message: str
    recommendation: str
    blocks_runtime: bool


@dataclass(frozen=True)
class DefaultPersonalProfileValidationReport:
    report_id: str
    profile_id: str
    valid_for_v0410: bool
    valid_for_runtime_execution: bool
    findings: tuple[DefaultPersonalProfileValidationFinding, ...]
    missing_items: tuple[DefaultPersonalProfileMissingItem, ...]
    unsafe_authority_detected: bool


@dataclass(frozen=True)
class DefaultPersonalProfileStatusReport:
    report_id: str
    profile_id: str
    status: str
    summary: str
    profile_home_path: str
    root_exists: bool
    profile_config_present: bool
    identity_files_present: bool
    policy_files_present: bool
    restore_context_present: bool
    unsafe_capabilities_closed: bool
    runtime_opened: bool
    blocking_gaps: tuple[str, ...]
    non_blocking_gaps: tuple[str, ...]
    next_recommended_version: str
    next_recommended_action: str


@dataclass(frozen=True)
class DefaultPersonalProfileLoadResult:
    result_id: str
    request_id: str
    profile_id: str
    loaded: bool
    config: DefaultPersonalProfileConfig | None
    runtime_state: DefaultPersonalRuntimeState
    status_report: DefaultPersonalProfileStatusReport
    validation_report: DefaultPersonalProfileValidationReport
    created_files: bool
    mutated_filesystem: bool
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool


@dataclass(frozen=True)
class DefaultPersonalProfileSafetyPosture:
    posture_id: str
    profile_id: str
    profile_is_sandbox: bool
    deny_first: bool
    write_allowed: bool
    shell_allowed: bool
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    agent_loop_allowed: bool
    skill_execution_allowed: bool
    subagent_invocation_allowed: bool
    autonomous_loop_allowed: bool
    dominion_allowed: bool
    production_certified: bool
    safety_summary: str


@dataclass(frozen=True)
class V041RuntimeOpeningStatus:
    status_id: str
    current_version: str
    profile_runtime_opened: bool
    cli_entrypoint_opened: bool
    profile_init_opened: bool
    prompt_assembly_opened: bool
    session_store_opened: bool
    provider_text_invocation_opened: bool
    read_only_skill_registry_opened: bool
    agent_loop_opened: bool
    trace_emission_opened: bool
    user_test_release_ready: bool


@dataclass(frozen=True)
class V0410ReadinessReport:
    report_id: str
    default_personal_profile_runtime_defined: bool
    personal_runtime_root_model_ready: bool
    default_personal_profile_config_ready: bool
    profile_status_report_ready: bool
    profile_safety_posture_ready: bool
    restore_context_ref_ready: bool
    v040_compatibility_gate_ready: bool
    v0411_handoff_ready: bool
    integrated_restore_document_ready: bool
    ready_for_cli_entrypoint: bool
    ready_for_profile_init: bool
    ready_for_prompt_assembly: bool
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
class V0411InstallableCLIBootstrapHandoff:
    handoff_id: str
    target_version: str
    fixed_cli_command_name: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0416UserTestTarget:
    target_id: str
    target_version: str
    design_only: bool
    commands: tuple[str, ...]
    user_test_release_ready: bool


@dataclass(frozen=True)
class V0410IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0410IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0410IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0410IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0410IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0410IntegratedRestoreDocumentManifest:
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


def _path_exists(path: str | None, allow_filesystem_read: bool = True) -> bool:
    return bool(path and allow_filesystem_read and Path(path).exists())


def _profile_home(root_path: str | None, profile_home_path: str | None) -> str:
    if profile_home_path:
        return profile_home_path
    base = root_path or "$LOCALAPPDATA/ChantaCore"
    return f"{base}/profiles/default-personal"


def create_personal_runtime_root(
    root_path: str | None = None,
    profile_home_path: str | None = None,
    check_exists: bool = False,
    **overrides: Any,
) -> PersonalRuntimeRoot:
    root = root_path or "$LOCALAPPDATA/ChantaCore"
    home = _profile_home(root, profile_home_path)
    defaults = {
        "root_id": "personal-runtime-root-default",
        "root_path": root,
        "profile_home_path": home,
        "created_by_init": False,
        "exists": _path_exists(root, check_exists),
        "writable_checked": False,
        "writable": None,
        "metadata_only": True,
    }
    return PersonalRuntimeRoot(**_merge(defaults, overrides))


def create_default_personal_profile_paths(
    profile_home_path: str | None = None,
    restore_context_path: str | None = V0409_RESTORE_DOC_PATH,
    **overrides: Any,
) -> DefaultPersonalProfilePaths:
    home = _profile_home(None, profile_home_path)
    defaults = {
        "paths_id": "default-personal-profile-paths",
        "profile_id": PROFILE_ID,
        "profile_home_path": home,
        "soul_path": f"{home}/identity/soul.md",
        "role_path": f"{home}/identity/role.md",
        "domain_path": f"{home}/identity/domain.md",
        "policy_path": f"{home}/policy/safety.md",
        "provider_config_path": f"{home}/providers/provider.toml",
        "session_store_path": f"{home}/sessions",
        "trace_store_path": f"{home}/traces",
        "restore_context_path": restore_context_path,
        "all_paths_metadata_only": True,
    }
    return DefaultPersonalProfilePaths(**_merge(defaults, overrides))


def create_default_personal_profile_config(
    profile_home_path: str | None = None,
    **overrides: Any,
) -> DefaultPersonalProfileConfig:
    paths = create_default_personal_profile_paths(profile_home_path)
    defaults = {
        "profile_id": PROFILE_ID,
        "profile_kind": DefaultPersonalProfileKind.DEFAULT_PERSONAL.value,
        "display_name": "Default Personal",
        "personal_root_ref": "personal-runtime-root-default",
        "profile_home_path": paths.profile_home_path,
        "soul_path": paths.soul_path,
        "role_path": paths.role_path,
        "domain_path": paths.domain_path,
        "policy_path": paths.policy_path,
        "core_memory_path": f"{paths.profile_home_path}/identity/core_memory.md",
        "restore_context_path": paths.restore_context_path,
        "safety_boundary_ref": "v0.40.9-safety-closure",
        "provider_config_path": paths.provider_config_path,
        "session_store_path": paths.session_store_path,
        "trace_store_path": paths.trace_store_path,
        "profile_is_sandbox": False,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "agent_loop_allowed": False,
        "skill_execution_allowed": False,
        "workspace_mutation_allowed": False,
        "shell_execution_allowed": False,
        "subagent_invocation_allowed": False,
        "production_certified": False,
        "metadata": {"runtime_foundation_only": True, "fixed_cli_command_name": "chanta-cli"},
    }
    return DefaultPersonalProfileConfig(**_merge(defaults, overrides))


def create_default_personal_identity_files(
    config: DefaultPersonalProfileConfig | None = None,
    allow_filesystem_read: bool = True,
    **overrides: Any,
) -> DefaultPersonalIdentityFiles:
    config = config or create_default_personal_profile_config()
    checks = {
        "soul": _path_exists(config.soul_path, allow_filesystem_read),
        "role": _path_exists(config.role_path, allow_filesystem_read),
        "domain": _path_exists(config.domain_path, allow_filesystem_read),
        "core_memory": _path_exists(config.core_memory_path, allow_filesystem_read),
    }
    missing = tuple(name for name, exists in checks.items() if not exists)
    defaults = {
        "identity_id": "default-personal-identity-files",
        "profile_id": config.profile_id,
        "soul_path": config.soul_path,
        "role_path": config.role_path,
        "domain_path": config.domain_path,
        "core_memory_path": config.core_memory_path,
        "soul_exists": checks["soul"],
        "role_exists": checks["role"],
        "domain_exists": checks["domain"],
        "core_memory_exists": checks["core_memory"],
        "missing_identity_items": missing,
    }
    return DefaultPersonalIdentityFiles(**_merge(defaults, overrides))


def create_restore_context_ref(
    restore_doc_path: str = V0409_RESTORE_DOC_PATH,
    allow_filesystem_read: bool = True,
    **overrides: Any,
) -> RestoreContextRef:
    present = _path_exists(restore_doc_path, allow_filesystem_read)
    prompt_present = False
    if present and allow_filesystem_read:
        text = Path(restore_doc_path).read_text(encoding="utf-8")
        prompt_present = "You are continuing ChantaCore after v0.40.9." in text
    defaults = {
        "restore_ref_id": "v0409-restore-context-ref",
        "source_version": "v0.40.9",
        "restore_doc_path": restore_doc_path,
        "restore_doc_expected": True,
        "restore_doc_present": present,
        "copy_paste_restore_prompt_expected": True,
        "copy_paste_restore_prompt_present": prompt_present,
        "suitable_for_profile_runtime": present and prompt_present,
    }
    return RestoreContextRef(**_merge(defaults, overrides))


def create_default_personal_policy_files(
    config: DefaultPersonalProfileConfig | None = None,
    restore_context_ref: RestoreContextRef | None = None,
    allow_filesystem_read: bool = True,
    **overrides: Any,
) -> DefaultPersonalPolicyFiles:
    config = config or create_default_personal_profile_config()
    restore_context_ref = restore_context_ref or create_restore_context_ref(
        config.restore_context_path or V0409_RESTORE_DOC_PATH,
        allow_filesystem_read=allow_filesystem_read,
    )
    policy_exists = _path_exists(config.policy_path, allow_filesystem_read)
    safety_loaded = bool(config.safety_boundary_ref)
    missing = tuple(
        item
        for item, present in (
            ("policy", policy_exists),
            ("safety_boundary", safety_loaded),
            ("restore_context", restore_context_ref.restore_doc_present),
        )
        if not present
    )
    defaults = {
        "policy_id": "default-personal-policy-files",
        "profile_id": config.profile_id,
        "policy_path": config.policy_path,
        "safety_boundary_ref": config.safety_boundary_ref,
        "restore_context_ref": restore_context_ref.restore_ref_id,
        "policy_exists": policy_exists,
        "safety_boundary_loaded": safety_loaded,
        "restore_context_loaded": restore_context_ref.restore_doc_present,
        "unsafe_capabilities_closed": True,
        "missing_policy_items": missing,
    }
    return DefaultPersonalPolicyFiles(**_merge(defaults, overrides))


def create_v040_compatibility_gate(
    restore_ref: RestoreContextRef | None = None,
    **overrides: Any,
) -> V040CompatibilityGate:
    restore_ref = restore_ref or create_restore_context_ref()
    defaults = {
        "gate_id": "v040-compatibility-gate-v0410",
        "source_version": "v0.40.9",
        "v0409_restore_ref": restore_ref.restore_ref_id,
        "unsafe_flags_false_confirmed": True,
        "standalone_runtime_was_closed": True,
        "provider_runtime_was_closed": True,
        "prompt_submission_was_closed": True,
        "subagent_runtime_was_closed": True,
        "live_apply_was_closed": True,
        "compatible_for_v0410_profile_runtime": True,
        "compatible_for_v041_runtime_execution": False,
    }
    return V040CompatibilityGate(**_merge(defaults, overrides))


def create_default_personal_runtime_state(
    config: DefaultPersonalProfileConfig | None = None,
    allow_filesystem_read: bool = True,
    **overrides: Any,
) -> DefaultPersonalRuntimeState:
    config = config or create_default_personal_profile_config()
    restore_ref = create_restore_context_ref(config.restore_context_path or V0409_RESTORE_DOC_PATH, allow_filesystem_read)
    identity = create_default_personal_identity_files(config, allow_filesystem_read)
    policy = create_default_personal_policy_files(config, restore_ref, allow_filesystem_read)
    compatibility = create_v040_compatibility_gate(restore_ref)
    blocking = tuple(
        item
        for item in (
            "missing_identity_files" if identity.missing_identity_items else "",
            "missing_policy_files" if policy.missing_policy_items else "",
            "provider_text_invocation_not_open",
            "prompt_assembly_not_open",
            "agent_loop_not_open",
            "read_only_skill_registry_not_open",
            "trace_emission_not_open",
            "user_test_release_not_ready",
        )
        if item
    )
    defaults = {
        "state_id": "default-personal-runtime-state-v0410",
        "profile_id": config.profile_id,
        "profile_loaded": True,
        "config_valid": True,
        "identity_files_status": identity,
        "policy_files_status": policy,
        "restore_context_ref": restore_ref,
        "v040_compatibility_gate": compatibility,
        "runtime_opened": False,
        "provider_ready": False,
        "prompt_assembly_ready": False,
        "session_store_ready": False,
        "agent_loop_ready": False,
        "skill_registry_ready": False,
        "trace_emission_ready": False,
        "user_test_ready": False,
        "blocking_gaps": blocking,
        "non_blocking_gaps": ("profile files may be absent until v0.41.1 init",),
    }
    return DefaultPersonalRuntimeState(**_merge(defaults, overrides))


def create_default_personal_profile_status(
    state: DefaultPersonalRuntimeState | None = None,
) -> str:
    state = state or create_default_personal_runtime_state()
    if not state.profile_loaded:
        return DefaultPersonalProfileStatus.MISSING.value
    if state.blocking_gaps:
        return DefaultPersonalProfileStatus.LOADED_WITH_GAPS.value
    return DefaultPersonalProfileStatus.READY_FOR_V0411_CLI_BOOTSTRAP.value


def create_default_personal_profile_status_report(
    root: PersonalRuntimeRoot | None = None,
    config: DefaultPersonalProfileConfig | None = None,
    state: DefaultPersonalRuntimeState | None = None,
    **overrides: Any,
) -> DefaultPersonalProfileStatusReport:
    config = config or create_default_personal_profile_config()
    root = root or create_personal_runtime_root(profile_home_path=config.profile_home_path)
    state = state or create_default_personal_runtime_state(config)
    identity_present = not state.identity_files_status.missing_identity_items
    policy_present = not state.policy_files_status.missing_policy_items
    defaults = {
        "report_id": "default-personal-profile-status-report-v0410",
        "profile_id": config.profile_id,
        "status": create_default_personal_profile_status(state),
        "summary": "Default Personal profile foundation is loaded as metadata/config-read with runtime gaps.",
        "profile_home_path": config.profile_home_path,
        "root_exists": root.exists,
        "profile_config_present": True,
        "identity_files_present": identity_present,
        "policy_files_present": policy_present,
        "restore_context_present": bool(state.restore_context_ref and state.restore_context_ref.restore_doc_present),
        "unsafe_capabilities_closed": True,
        "runtime_opened": False,
        "blocking_gaps": state.blocking_gaps,
        "non_blocking_gaps": state.non_blocking_gaps,
        "next_recommended_version": "v0.41.1",
        "next_recommended_action": "Implement installable CLI bootstrap, doctor, and idempotent profile init command.",
    }
    return DefaultPersonalProfileStatusReport(**_merge(defaults, overrides))


def create_default_personal_profile_safety_posture(**overrides: Any) -> DefaultPersonalProfileSafetyPosture:
    defaults = {
        "posture_id": "default-personal-safety-posture-v0410",
        "profile_id": PROFILE_ID,
        "profile_is_sandbox": False,
        "deny_first": True,
        "write_allowed": False,
        "shell_allowed": False,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "agent_loop_allowed": False,
        "skill_execution_allowed": False,
        "subagent_invocation_allowed": False,
        "autonomous_loop_allowed": False,
        "dominion_allowed": False,
        "production_certified": False,
        "safety_summary": "Default Personal profile is deny-first and not a sandbox or execution authority.",
    }
    return DefaultPersonalProfileSafetyPosture(**_merge(defaults, overrides))


def _missing_item(item_kind: str, path: str | None, severity: str, blocks_v0411: bool = True) -> DefaultPersonalProfileMissingItem:
    return DefaultPersonalProfileMissingItem(
        item_id=f"missing-{item_kind}",
        profile_id=PROFILE_ID,
        item_kind=item_kind,
        path=path,
        severity=severity,
        blocks_v0410=False,
        blocks_v0411=blocks_v0411,
        blocks_v0416_user_test=True,
        recommendation=f"Define {item_kind} during v0.41.1 or later scoped runtime work.",
    )


def validate_default_personal_profile_config(
    config: DefaultPersonalProfileConfig | None = None,
    identity_files: DefaultPersonalIdentityFiles | None = None,
    policy_files: DefaultPersonalPolicyFiles | None = None,
    **overrides: Any,
) -> DefaultPersonalProfileValidationReport:
    config = config or create_default_personal_profile_config()
    identity_files = identity_files or create_default_personal_identity_files(config)
    policy_files = policy_files or create_default_personal_policy_files(config)
    findings: list[DefaultPersonalProfileValidationFinding] = []
    unsafe = any(
        (
            config.provider_invocation_allowed,
            config.prompt_submission_allowed,
            config.agent_loop_allowed,
            config.skill_execution_allowed,
            config.workspace_mutation_allowed,
            config.shell_execution_allowed,
            config.subagent_invocation_allowed,
            config.production_certified,
        )
    )
    if config.profile_is_sandbox:
        findings.append(
            DefaultPersonalProfileValidationFinding(
                finding_id="profile-sandbox-claim",
                severity="blocking",
                field_name="profile_is_sandbox",
                message="Default Personal profile is not an OS-level sandbox.",
                recommendation="Keep profile_is_sandbox false.",
                blocks_runtime=True,
            )
        )
    if unsafe:
        findings.append(
            DefaultPersonalProfileValidationFinding(
                finding_id="unsafe-authority-detected",
                severity="blocking",
                field_name="runtime_authority",
                message="Unsafe runtime authority was requested in v0.41.0.",
                recommendation="Keep all action/runtime flags false.",
                blocks_runtime=True,
            )
        )
    missing = tuple(
        _missing_item(item, getattr(config, f"{item}_path", None), "warning")
        for item in identity_files.missing_identity_items
    ) + tuple(_missing_item(item, None, "blocking") for item in policy_files.missing_policy_items)
    defaults = {
        "report_id": "default-personal-validation-report-v0410",
        "profile_id": config.profile_id,
        "valid_for_v0410": not unsafe,
        "valid_for_runtime_execution": False,
        "findings": tuple(findings),
        "missing_items": missing,
        "unsafe_authority_detected": unsafe,
    }
    return DefaultPersonalProfileValidationReport(**_merge(defaults, overrides))


def create_default_personal_profile_load_request(**overrides: Any) -> DefaultPersonalProfileLoadRequest:
    defaults = {
        "request_id": "default-personal-load-request-v0410",
        "profile_id": PROFILE_ID,
        "personal_root_path": None,
        "profile_home_path": None,
        "allow_filesystem_read": True,
        "allow_filesystem_write": False,
        "allow_profile_creation": False,
        "metadata_only": True,
    }
    return DefaultPersonalProfileLoadRequest(**_merge(defaults, overrides))


def load_default_personal_profile(
    request: DefaultPersonalProfileLoadRequest | None = None,
    **overrides: Any,
) -> DefaultPersonalProfileLoadResult:
    request = request or create_default_personal_profile_load_request()
    if request.allow_filesystem_write or request.allow_profile_creation:
        raise ValueError("v0.41.0 profile loading cannot write or create profile files")
    root = create_personal_runtime_root(
        request.personal_root_path,
        request.profile_home_path,
        check_exists=request.allow_filesystem_read,
    )
    config = create_default_personal_profile_config(root.profile_home_path)
    state = create_default_personal_runtime_state(config, request.allow_filesystem_read)
    validation = validate_default_personal_profile_config(
        config,
        state.identity_files_status,
        state.policy_files_status,
    )
    status = create_default_personal_profile_status_report(root, config, state)
    defaults = {
        "result_id": "default-personal-load-result-v0410",
        "request_id": request.request_id,
        "profile_id": request.profile_id,
        "loaded": True,
        "config": config,
        "runtime_state": state,
        "status_report": status,
        "validation_report": validation,
        "created_files": False,
        "mutated_filesystem": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "agent_loop_started": False,
    }
    return DefaultPersonalProfileLoadResult(**_merge(defaults, overrides))


def create_v041_runtime_opening_status(**overrides: Any) -> V041RuntimeOpeningStatus:
    defaults = {
        "status_id": "v041-runtime-opening-status-v0410",
        "current_version": V0410_RELEASE_NAME,
        "profile_runtime_opened": True,
        "cli_entrypoint_opened": False,
        "profile_init_opened": False,
        "prompt_assembly_opened": False,
        "session_store_opened": False,
        "provider_text_invocation_opened": False,
        "read_only_skill_registry_opened": False,
        "agent_loop_opened": False,
        "trace_emission_opened": False,
        "user_test_release_ready": False,
    }
    return V041RuntimeOpeningStatus(**_merge(defaults, overrides))


def create_v0410_readiness_report(**overrides: Any) -> V0410ReadinessReport:
    defaults = {
        "report_id": "v0410-readiness-report",
        "default_personal_profile_runtime_defined": True,
        "personal_runtime_root_model_ready": True,
        "default_personal_profile_config_ready": True,
        "profile_status_report_ready": True,
        "profile_safety_posture_ready": True,
        "restore_context_ref_ready": True,
        "v040_compatibility_gate_ready": True,
        "v0411_handoff_ready": True,
        "integrated_restore_document_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return V0410ReadinessReport(**_merge(defaults, overrides))


def create_v0411_installable_cli_bootstrap_handoff(**overrides: Any) -> V0411InstallableCLIBootstrapHandoff:
    defaults = {
        "handoff_id": "v0411-installable-cli-bootstrap-handoff",
        "target_version": "v0.41.1 Installable CLI Bootstrap & Doctor",
        "fixed_cli_command_name": "chanta-cli",
        "recommended_focus": (
            "stabilize chanta-cli entrypoint",
            "expose chanta-cli --version",
            "expose chanta-cli doctor",
            "expose chanta-cli init default-personal",
            "expose chanta-cli profile status",
            "define idempotent profile init",
            "no provider call",
            "no run/ask",
            "no AgentLoop",
            "no skill execution",
            "no unsafe commands",
        ),
        "still_closed": CLOSED_CAPABILITIES,
    }
    return V0411InstallableCLIBootstrapHandoff(**_merge(defaults, overrides))


def create_v0416_user_test_target(**overrides: Any) -> V0416UserTestTarget:
    defaults = {
        "target_id": "v0416-user-test-target",
        "target_version": "v0.41.6 Installable User-Test Release",
        "design_only": True,
        "commands": V0416_TARGET_COMMANDS,
        "user_test_release_ready": False,
    }
    return V0416UserTestTarget(**_merge(defaults, overrides))


def create_v0410_integrated_restore_sections() -> tuple[V0410IntegratedRestoreSection, ...]:
    return tuple(
        V0410IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.41.0 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0410_integrated_restore_context_snapshot(**overrides: Any) -> V0410IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0410",
        "current_version": V0410_RELEASE_NAME,
        "current_track": V0410_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            V0410_RELEASE_NAME,
        ),
        "open_capabilities": OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "next_recommended_version": "v0.41.1 Installable CLI Bootstrap & Doctor",
    }
    return V0410IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0410_integrated_restore_packet(**overrides: Any) -> V0410IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0410",
        "snapshot": create_v0410_integrated_restore_context_snapshot(),
        "restore_sections": create_v0410_integrated_restore_sections(),
        "required_test_commands": (
            "tests/test_v0410_default_personal_profile_runtime.py",
            "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
        ),
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0410IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0410_integrated_restore_document_manifest(**overrides: Any) -> V0410IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0410",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0410IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def default_profile_config_preserves_no_runtime_authority(config: DefaultPersonalProfileConfig) -> bool:
    return (
        not config.profile_is_sandbox
        and not config.provider_invocation_allowed
        and not config.prompt_submission_allowed
        and not config.agent_loop_allowed
        and not config.skill_execution_allowed
        and not config.workspace_mutation_allowed
        and not config.shell_execution_allowed
        and not config.subagent_invocation_allowed
        and not config.production_certified
    )


def profile_load_result_preserves_no_side_effects(result: DefaultPersonalProfileLoadResult) -> bool:
    return (
        not result.created_files
        and not result.mutated_filesystem
        and not result.provider_invoked
        and not result.prompt_submitted
        and not result.agent_loop_started
    )


def profile_safety_posture_preserves_denial(posture: DefaultPersonalProfileSafetyPosture) -> bool:
    return (
        not posture.profile_is_sandbox
        and posture.deny_first
        and not posture.write_allowed
        and not posture.shell_allowed
        and not posture.provider_invocation_allowed
        and not posture.prompt_submission_allowed
        and not posture.agent_loop_allowed
        and not posture.skill_execution_allowed
        and not posture.subagent_invocation_allowed
        and not posture.autonomous_loop_allowed
        and not posture.dominion_allowed
        and not posture.production_certified
    )


def v040_compatibility_gate_blocks_runtime_execution(gate: V040CompatibilityGate) -> bool:
    return gate.compatible_for_v0410_profile_runtime and not gate.compatible_for_v041_runtime_execution


def v0410_readiness_preserves_closed_runtime(report: V0410ReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0410IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


__all__ = [
    "CLOSED_CAPABILITIES",
    "INTEGRATED_DOC_PATH",
    "OPEN_CAPABILITIES",
    "PROFILE_ID",
    "REQUIRED_FALSE_FLAGS",
    "REQUIRED_RESTORE_SECTION_IDS",
    "V0409_RESTORE_DOC_PATH",
    "V0410_RELEASE_NAME",
    "V0410_TRACK_NAME",
    "V0410_VERSION",
    "V0416_TARGET_COMMANDS",
    "DefaultPersonalIdentityFiles",
    "DefaultPersonalPolicyFiles",
    "DefaultPersonalProfileConfig",
    "DefaultPersonalProfileKind",
    "DefaultPersonalProfileLoadRequest",
    "DefaultPersonalProfileLoadResult",
    "DefaultPersonalProfileMissingItem",
    "DefaultPersonalProfilePaths",
    "DefaultPersonalProfileSafetyPosture",
    "DefaultPersonalProfileStatus",
    "DefaultPersonalProfileStatusReport",
    "DefaultPersonalProfileValidationFinding",
    "DefaultPersonalProfileValidationReport",
    "DefaultPersonalRuntimeState",
    "PersonalRuntimeRoot",
    "RestoreContextRef",
    "V040CompatibilityGate",
    "V0410IntegratedRestoreContextSnapshot",
    "V0410IntegratedRestoreDocumentManifest",
    "V0410IntegratedRestorePacket",
    "V0410IntegratedRestoreSection",
    "V0410ReadinessReport",
    "V0411InstallableCLIBootstrapHandoff",
    "V0416UserTestTarget",
    "V041RuntimeOpeningStatus",
    "create_default_personal_identity_files",
    "create_default_personal_policy_files",
    "create_default_personal_profile_config",
    "create_default_personal_profile_load_request",
    "create_default_personal_profile_paths",
    "create_default_personal_profile_safety_posture",
    "create_default_personal_profile_status",
    "create_default_personal_profile_status_report",
    "create_default_personal_runtime_state",
    "create_personal_runtime_root",
    "create_restore_context_ref",
    "create_v040_compatibility_gate",
    "create_v0410_integrated_restore_context_snapshot",
    "create_v0410_integrated_restore_document_manifest",
    "create_v0410_integrated_restore_packet",
    "create_v0410_integrated_restore_sections",
    "create_v0410_readiness_report",
    "create_v0411_installable_cli_bootstrap_handoff",
    "create_v0416_user_test_target",
    "create_v041_runtime_opening_status",
    "default_profile_config_preserves_no_runtime_authority",
    "integrated_restore_packet_uses_single_doc",
    "load_default_personal_profile",
    "profile_load_result_preserves_no_side_effects",
    "profile_safety_posture_preserves_denial",
    "v040_compatibility_gate_blocks_runtime_execution",
    "v0410_readiness_preserves_closed_runtime",
    "validate_default_personal_profile_config",
]
