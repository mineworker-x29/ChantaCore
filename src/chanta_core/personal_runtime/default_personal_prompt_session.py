"""v0.41.2 prompt assembly preview and bounded session store support.

This module opens deterministic prompt preview and session new/list metadata
only. It does not submit prompts, call providers, start AgentLoop, execute
skills, emit trace runtime, or mutate files outside the selected profile home.
"""

from __future__ import annotations

import argparse
import json
import sys
import uuid
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from enum import StrEnum
from pathlib import Path
from typing import Any, Sequence

from chanta_core.personal_runtime.default_personal_cli_bootstrap import (
    CLI_NAME,
    PROFILE_ID,
    V0416_TARGET_COMMANDS,
    create_unsupported_command_decision,
    main as v0411_main,
)


V0412_VERSION = "v0.41.2"
V0412_RELEASE_NAME = "v0.41.2 Prompt Assembly & Session Store"
V0412_TRACK_NAME = "v0.41 Default Personal Runtime Opening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.41/v0.41.2_prompt_assembly_session_store_restore.md"
V0411_RESTORE_DOC_PATH = "docs/versions/v0.41/v0.41.1_installable_cli_bootstrap_doctor_restore.md"
V0410_RESTORE_DOC_PATH = "docs/versions/v0.41/v0.41.0_default_personal_profile_runtime_restore.md"
V0409_RESTORE_DOC_PATH = (
    "docs/versions/v0.40/"
    "v0.40.9_controlled_mission_loop_preparation_consolidation_v041_handoff_restore.md"
)


class PromptBlockKind(StrEnum):
    SAFETY_INVARIANT = "safety_invariant"
    SOUL = "soul"
    PROFILE_ROLE = "profile_role"
    DOMAIN_INSTRUCTION = "domain_instruction"
    PROJECT_INSTRUCTION = "project_instruction"
    READ_ONLY_SKILL_POLICY = "read_only_skill_policy"
    RESTORE_SUMMARY = "restore_summary"
    SESSION_CONTEXT = "session_context"
    USER_INPUT = "user_input"
    DIAGNOSTIC_NOTE = "diagnostic_note"
    MISSING_SOURCE_NOTICE = "missing_source_notice"


class PromptSourceKind(StrEnum):
    BUILT_IN_SAFETY = "built_in_safety"
    PROFILE_SOUL_FILE = "profile_soul_file"
    PROFILE_ROLE_FILE = "profile_role_file"
    PROFILE_DOMAIN_FILE = "profile_domain_file"
    PROFILE_POLICY_FILE = "profile_policy_file"
    PROJECT_AGENTS_FILE = "project_agents_file"
    PROJECT_INSTRUCTION_FILE = "project_instruction_file"
    RESTORE_DOCUMENT = "restore_document"
    SESSION_STORE = "session_store"
    USER_INPUT = "user_input"
    GENERATED_METADATA = "generated_metadata"


class PromptAssemblyStatus(StrEnum):
    ASSEMBLED = "assembled"
    ASSEMBLED_WITH_WARNINGS = "assembled_with_warnings"
    BLOCKED = "blocked"
    MISSING_REQUIRED_SOURCE = "missing_required_source"
    INVALID_INPUT = "invalid_input"
    PREVIEW_ONLY = "preview_only"


PROMPT_BLOCK_ORDER: tuple[str, ...] = (
    PromptBlockKind.SAFETY_INVARIANT.value,
    PromptBlockKind.SOUL.value,
    PromptBlockKind.PROFILE_ROLE.value,
    PromptBlockKind.DOMAIN_INSTRUCTION.value,
    PromptBlockKind.PROJECT_INSTRUCTION.value,
    PromptBlockKind.READ_ONLY_SKILL_POLICY.value,
    PromptBlockKind.RESTORE_SUMMARY.value,
    PromptBlockKind.SESSION_CONTEXT.value,
    PromptBlockKind.USER_INPUT.value,
)
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
    "unsupported_command_denial",
    "integrated_restore_document",
)
CLOSED_CAPABILITIES: tuple[str, ...] = (
    "run_command",
    "ask_command",
    "provider_doctor",
    "provider_text_only_invocation",
    "read_only_skill_registry",
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
    "autonomous_loop",
    "retry_loop",
    "dominion_runtime",
    "production_certification",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_run_command",
    "ready_for_ask_command",
    "ready_for_provider_doctor",
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
    "v0411_cli_bootstrap_summary",
    "prompt_assembly_summary",
    "prompt_block_order_contract",
    "safety_invariant_block_contract",
    "soul_role_domain_binding_contract",
    "project_instruction_contract",
    "read_only_skill_policy_block_contract",
    "restore_summary_block_contract",
    "session_context_block_contract",
    "prompt_preview_contract",
    "session_store_contract",
    "session_new_contract",
    "session_list_contract",
    "unsupported_command_policy",
    "safety_posture",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0413_handoff",
    "v0416_user_test_target",
    "copy_paste_restore_prompt",
)


@dataclass(frozen=True)
class PromptAssemblyPolicy:
    policy_id: str
    profile_id: str
    safety_invariant_required: bool
    soul_required: bool
    role_required: bool
    domain_required: bool
    project_context_allowed: bool
    restore_summary_allowed: bool
    session_context_allowed: bool
    max_block_chars: int
    max_total_chars: int
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    agent_loop_allowed: bool
    skill_execution_allowed: bool
    metadata_only: bool


@dataclass(frozen=True)
class PromptSourceProvenance:
    provenance_id: str
    source_kind: str
    source_path: str | None
    source_present: bool
    source_read: bool
    truncated: bool
    chars_loaded: int
    warning: str | None


@dataclass(frozen=True)
class PromptBlock:
    block_id: str
    block_kind: str
    title: str
    content: str
    provenance: PromptSourceProvenance
    required: bool
    present: bool
    truncated: bool
    order_index: int


@dataclass(frozen=True)
class SafetyInvariantBlock:
    block: PromptBlock
    provider_invocation_closed: bool
    prompt_submission_closed: bool
    agent_loop_closed: bool
    skill_execution_closed: bool
    preview_not_model_response: bool


@dataclass(frozen=True)
class SoulRoleDomainBinding:
    binding_id: str
    profile_id: str
    soul_block: PromptBlock
    role_block: PromptBlock
    domain_block: PromptBlock
    missing_identity_items: tuple[str, ...]
    usable_for_preview: bool
    usable_for_provider_run: bool


@dataclass(frozen=True)
class ProjectInstructionRef:
    ref_id: str
    project_root: str
    candidate_paths: tuple[str, ...]
    loaded_paths: tuple[str, ...]
    missing_paths: tuple[str, ...]
    project_context_allowed: bool
    prompt_injection_warning: bool


@dataclass(frozen=True)
class ReadOnlySkillPolicyBlock:
    block: PromptBlock
    skill_execution_allowed: bool
    file_write_allowed: bool
    shell_execution_allowed: bool
    provider_tool_calling_allowed: bool


@dataclass(frozen=True)
class RestoreSummaryBlock:
    block: PromptBlock
    restore_docs_present: tuple[str, ...]
    grants_runtime_authority: bool


@dataclass(frozen=True)
class SessionContextBlock:
    block: PromptBlock
    session_id: str | None
    prior_turn_count: int
    provider_output_present: bool


@dataclass(frozen=True)
class PromptAssemblyInput:
    input_id: str
    profile_id: str
    home_path: str | None
    user_input: str
    project_root: str | None
    session_id: str | None
    include_project_context: bool
    include_restore_summary: bool
    include_session_context: bool
    metadata_only: bool


@dataclass(frozen=True)
class PromptAssemblyResult:
    result_id: str
    input_id: str
    profile_id: str
    status: str
    blocks: tuple[PromptBlock, ...]
    rendered_preview: str
    warnings: tuple[str, ...]
    missing_sources: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool
    skill_executed: bool
    session_written: bool


@dataclass(frozen=True)
class PromptPreviewCommandInput:
    profile_id: str
    home_path: str | None
    user_input: str
    project_root: str | None
    session_id: str | None


@dataclass(frozen=True)
class PromptPreviewCommandResult:
    status: str
    rendered_preview: str
    warnings: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    session_written: bool


@dataclass(frozen=True)
class DefaultPersonalSessionId:
    session_id: str
    explicit: bool


@dataclass(frozen=True)
class DefaultPersonalSessionRecord:
    session_id: str
    profile_id: str
    created_at: str
    title: str | None
    status: str
    session_dir: str
    session_json_path: str
    turns_jsonl_path: str
    events_jsonl_path: str
    provider_invoked: bool
    agent_loop_started: bool
    production_certified: bool


@dataclass(frozen=True)
class DefaultPersonalSessionStoreConfig:
    profile_id: str
    home_path: str
    sessions_dir: str
    allow_create: bool
    allow_append_turns: bool
    allow_overwrite: bool
    metadata_only: bool


@dataclass(frozen=True)
class DefaultPersonalSessionCreateRequest:
    profile_id: str
    home_path: str
    title: str | None
    explicit_session_id: str | None
    dry_run: bool


@dataclass(frozen=True)
class DefaultPersonalSessionCreateResult:
    result_id: str
    profile_id: str
    session_id: str
    session_record: DefaultPersonalSessionRecord | None
    created_directories: tuple[str, ...]
    created_files: tuple[str, ...]
    existing_files: tuple[str, ...]
    overwritten_files: tuple[str, ...]
    outside_home_paths: tuple[str, ...]
    status: str
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool
    skill_executed: bool
    shell_executed: bool
    network_accessed: bool
    credentials_accessed: bool


@dataclass(frozen=True)
class DefaultPersonalSessionListRequest:
    profile_id: str
    home_path: str
    limit: int | None


@dataclass(frozen=True)
class DefaultPersonalSessionListResult:
    profile_id: str
    home_path: str
    sessions: tuple[DefaultPersonalSessionRecord, ...]
    status: str
    warning: str | None
    provider_invoked: bool
    prompt_submitted: bool
    agent_loop_started: bool


@dataclass(frozen=True)
class DefaultPersonalSessionTurnRecord:
    turn_id: str
    session_id: str
    role: str
    content: str
    created_at: str
    source: str
    provider_generated: bool
    metadata: dict[str, object]


@dataclass(frozen=True)
class DefaultPersonalSessionStoreSafetyReport:
    report_id: str
    profile_id: str
    bounded_to_home: bool
    overwrite_allowed: bool
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    agent_loop_allowed: bool
    shell_execution_allowed: bool
    network_access_allowed: bool
    credential_access_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0412ReadinessReport:
    report_id: str
    prompt_assembly_defined: bool
    prompt_preview_command_ready: bool
    prompt_block_order_ready: bool
    safety_invariant_block_ready: bool
    soul_role_domain_binding_ready: bool
    restore_summary_block_ready: bool
    session_store_schema_ready: bool
    session_new_command_ready: bool
    session_list_command_ready: bool
    integrated_restore_document_ready: bool
    v0413_handoff_ready: bool
    ready_for_run_command: bool
    ready_for_ask_command: bool
    ready_for_provider_doctor: bool
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
class V0413ProviderProbeSkillRegistryHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0416UserTestTargetUpdate:
    target_id: str
    target_version: str
    commands: tuple[str, ...]
    commands_expected_in_v0412: tuple[str, ...]
    user_test_release_ready: bool


@dataclass(frozen=True)
class V0412IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0412IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0412IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0412IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0412IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0412IntegratedRestoreDocumentManifest:
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


def _profile_dir(home_path: str) -> Path:
    return Path(home_path) / "profiles" / PROFILE_ID


def _sessions_dir(home_path: str) -> Path:
    return _profile_dir(home_path) / "state" / "sessions"


def _is_under_home(path: Path, home_path: str) -> bool:
    try:
        path.resolve().relative_to(Path(home_path).resolve())
        return True
    except ValueError:
        return False


def _bounded_read(path: Path, max_chars: int) -> tuple[str, PromptSourceProvenance]:
    if not path.exists():
        return "", create_prompt_source_provenance(
            source_path=str(path),
            source_present=False,
            source_read=False,
            warning="source missing",
        )
    text = path.read_text(encoding="utf-8")
    truncated = len(text) > max_chars
    loaded = text[:max_chars]
    return loaded, create_prompt_source_provenance(
        source_path=str(path),
        source_present=True,
        source_read=True,
        truncated=truncated,
        chars_loaded=len(loaded),
        warning="source truncated" if truncated else None,
    )


def _session_record_from_dir(session_dir: Path, profile_id: str) -> DefaultPersonalSessionRecord | None:
    session_json = session_dir / "session.json"
    if not session_json.exists():
        return None
    data = json.loads(session_json.read_text(encoding="utf-8"))
    return create_default_personal_session_record(
        session_id=str(data.get("session_id", session_dir.name)),
        profile_id=profile_id,
        created_at=str(data.get("created_at", "")),
        title=data.get("title"),
        status=str(data.get("status", "created")),
        session_dir=str(session_dir),
        session_json_path=str(session_json),
        turns_jsonl_path=str(session_dir / "turns.jsonl"),
        events_jsonl_path=str(session_dir / "events.jsonl"),
    )


def create_prompt_assembly_policy(**overrides: Any) -> PromptAssemblyPolicy:
    defaults = {
        "policy_id": "prompt-assembly-policy-v0412",
        "profile_id": PROFILE_ID,
        "safety_invariant_required": True,
        "soul_required": False,
        "role_required": False,
        "domain_required": False,
        "project_context_allowed": True,
        "restore_summary_allowed": True,
        "session_context_allowed": True,
        "max_block_chars": 4000,
        "max_total_chars": 12000,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "agent_loop_allowed": False,
        "skill_execution_allowed": False,
        "metadata_only": True,
    }
    return PromptAssemblyPolicy(**_merge(defaults, overrides))


def create_prompt_source_provenance(**overrides: Any) -> PromptSourceProvenance:
    defaults = {
        "provenance_id": "prompt-source-generated-v0412",
        "source_kind": PromptSourceKind.GENERATED_METADATA.value,
        "source_path": None,
        "source_present": True,
        "source_read": False,
        "truncated": False,
        "chars_loaded": 0,
        "warning": None,
    }
    return PromptSourceProvenance(**_merge(defaults, overrides))


def create_prompt_block(**overrides: Any) -> PromptBlock:
    defaults = {
        "block_id": "prompt-block-v0412",
        "block_kind": PromptBlockKind.DIAGNOSTIC_NOTE.value,
        "title": "Diagnostic Note",
        "content": "",
        "provenance": create_prompt_source_provenance(),
        "required": False,
        "present": True,
        "truncated": False,
        "order_index": 0,
    }
    return PromptBlock(**_merge(defaults, overrides))


def create_safety_invariant_block(**overrides: Any) -> SafetyInvariantBlock:
    content = (
        "v0.41.2 is preview/session only. Provider invocation is closed. "
        "Prompt submission to model is closed. AgentLoop is closed. Skill "
        "execution is closed. File write/edit is closed except bounded session "
        "creation. Shell, test, subagent, autonomous loop, and Dominion are "
        "closed. This output is a deterministic prompt preview, not a model response."
    )
    block = create_prompt_block(
        block_id="safety-invariant-block-v0412",
        block_kind=PromptBlockKind.SAFETY_INVARIANT.value,
        title="Safety Invariant",
        content=content,
        provenance=create_prompt_source_provenance(
            provenance_id="built-in-safety-v0412",
            source_kind=PromptSourceKind.BUILT_IN_SAFETY.value,
        ),
        required=True,
        present=True,
        order_index=0,
    )
    defaults = {
        "block": block,
        "provider_invocation_closed": True,
        "prompt_submission_closed": True,
        "agent_loop_closed": True,
        "skill_execution_closed": True,
        "preview_not_model_response": True,
    }
    return SafetyInvariantBlock(**_merge(defaults, overrides))


def _identity_block(
    home_path: str | None,
    filename: str,
    source_kind: str,
    block_kind: str,
    title: str,
    order_index: int,
    max_chars: int,
) -> PromptBlock:
    home = _home_path(home_path)
    path = _profile_dir(home) / ("soul" if filename == "SOUL.md" else "profile") / filename
    content, provenance = _bounded_read(path, max_chars)
    if not content:
        content = f"{title} source is missing."
    provenance = create_prompt_source_provenance(
        **{**asdict(provenance), "source_kind": source_kind, "provenance_id": f"{block_kind}-provenance-v0412"}
    )
    return create_prompt_block(
        block_id=f"{block_kind}-block-v0412",
        block_kind=block_kind,
        title=title,
        content=content,
        provenance=provenance,
        required=False,
        present=provenance.source_present,
        truncated=provenance.truncated,
        order_index=order_index,
    )


def create_soul_role_domain_binding(
    home_path: str | None = None,
    policy: PromptAssemblyPolicy | None = None,
    **overrides: Any,
) -> SoulRoleDomainBinding:
    policy = policy or create_prompt_assembly_policy()
    soul = _identity_block(
        home_path,
        "SOUL.md",
        PromptSourceKind.PROFILE_SOUL_FILE.value,
        PromptBlockKind.SOUL.value,
        "Soul",
        1,
        policy.max_block_chars,
    )
    role = _identity_block(
        home_path,
        "ROLE.json",
        PromptSourceKind.PROFILE_ROLE_FILE.value,
        PromptBlockKind.PROFILE_ROLE.value,
        "Profile Role",
        2,
        policy.max_block_chars,
    )
    domain = _identity_block(
        home_path,
        "DOMAIN.json",
        PromptSourceKind.PROFILE_DOMAIN_FILE.value,
        PromptBlockKind.DOMAIN_INSTRUCTION.value,
        "Domain Instruction",
        3,
        policy.max_block_chars,
    )
    missing = tuple(block.block_kind for block in (soul, role, domain) if not block.present)
    defaults = {
        "binding_id": "soul-role-domain-binding-v0412",
        "profile_id": PROFILE_ID,
        "soul_block": soul,
        "role_block": role,
        "domain_block": domain,
        "missing_identity_items": missing,
        "usable_for_preview": True,
        "usable_for_provider_run": False,
    }
    return SoulRoleDomainBinding(**_merge(defaults, overrides))


def create_project_instruction_ref(
    project_root: str | None = None,
    include_project_context: bool = True,
    max_chars: int = 4000,
    **overrides: Any,
) -> ProjectInstructionRef:
    root = str(Path(project_root or Path.cwd()).resolve())
    candidates = (str(Path(root) / "AGENTS.md"), str(Path(root) / "README.md"))
    loaded: list[str] = []
    missing: list[str] = []
    if include_project_context:
        for candidate in candidates:
            path = Path(candidate)
            if path.exists():
                path.read_text(encoding="utf-8")[:max_chars]
                loaded.append(candidate)
            else:
                missing.append(candidate)
    else:
        missing.extend(candidates)
    defaults = {
        "ref_id": "project-instruction-ref-v0412",
        "project_root": root,
        "candidate_paths": candidates,
        "loaded_paths": tuple(loaded),
        "missing_paths": tuple(missing),
        "project_context_allowed": include_project_context,
        "prompt_injection_warning": True,
    }
    return ProjectInstructionRef(**_merge(defaults, overrides))


def create_project_instruction_block(
    project_root: str | None = None,
    include_project_context: bool = True,
    policy: PromptAssemblyPolicy | None = None,
) -> tuple[ProjectInstructionRef, PromptBlock]:
    policy = policy or create_prompt_assembly_policy()
    ref = create_project_instruction_ref(project_root, include_project_context, policy.max_block_chars)
    contents: list[str] = []
    for loaded in ref.loaded_paths:
        text, _ = _bounded_read(Path(loaded), policy.max_block_chars)
        contents.append(f"Source: {loaded}\n{text}")
    content = "\n\n".join(contents) if contents else "No project instruction source loaded."
    block = create_prompt_block(
        block_id="project-instruction-block-v0412",
        block_kind=PromptBlockKind.PROJECT_INSTRUCTION.value,
        title="Project Instruction",
        content=content,
        provenance=create_prompt_source_provenance(
            provenance_id="project-instruction-provenance-v0412",
            source_kind=PromptSourceKind.PROJECT_INSTRUCTION_FILE.value,
            source_path=ref.loaded_paths[0] if ref.loaded_paths else None,
            source_present=bool(ref.loaded_paths),
            source_read=bool(ref.loaded_paths),
            chars_loaded=len(content),
            warning="lower priority than safety invariant",
        ),
        required=False,
        present=bool(ref.loaded_paths),
        order_index=4,
    )
    return ref, block


def create_read_only_skill_policy_block(**overrides: Any) -> ReadOnlySkillPolicyBlock:
    content = (
        "Future read-only skill policy metadata only. v0.41.2 does not execute "
        "skills, write files, edit files, apply patches, execute shell commands, "
        "execute tests, invoke subagents, or perform provider tool calling."
    )
    block = create_prompt_block(
        block_id="read-only-skill-policy-block-v0412",
        block_kind=PromptBlockKind.READ_ONLY_SKILL_POLICY.value,
        title="Read-only Skill Policy",
        content=content,
        provenance=create_prompt_source_provenance(
            provenance_id="read-only-skill-policy-provenance-v0412",
            source_kind=PromptSourceKind.GENERATED_METADATA.value,
        ),
        order_index=5,
    )
    defaults = {
        "block": block,
        "skill_execution_allowed": False,
        "file_write_allowed": False,
        "shell_execution_allowed": False,
        "provider_tool_calling_allowed": False,
    }
    return ReadOnlySkillPolicyBlock(**_merge(defaults, overrides))


def create_restore_summary_block(**overrides: Any) -> RestoreSummaryBlock:
    paths = (V0409_RESTORE_DOC_PATH, V0410_RESTORE_DOC_PATH, V0411_RESTORE_DOC_PATH)
    present = tuple(path for path in paths if Path(path).exists())
    content = (
        "Restore context references v0.40.9, v0.41.0, and v0.41.1 when present. "
        "Restore documents are context only and do not grant runtime authority."
    )
    if present:
        content += "\nPresent restore docs:\n" + "\n".join(f"- {path}" for path in present)
    block = create_prompt_block(
        block_id="restore-summary-block-v0412",
        block_kind=PromptBlockKind.RESTORE_SUMMARY.value,
        title="Restore Summary",
        content=content,
        provenance=create_prompt_source_provenance(
            provenance_id="restore-summary-provenance-v0412",
            source_kind=PromptSourceKind.RESTORE_DOCUMENT.value,
            source_present=bool(present),
            source_read=False,
            chars_loaded=len(content),
        ),
        order_index=6,
    )
    defaults = {"block": block, "restore_docs_present": present, "grants_runtime_authority": False}
    return RestoreSummaryBlock(**_merge(defaults, overrides))


def create_session_context_block(
    home_path: str | None = None,
    session_id: str | None = None,
    **overrides: Any,
) -> SessionContextBlock:
    prior_turn_count = 0
    created_at = "not_loaded"
    if session_id:
        session_dir = _sessions_dir(_home_path(home_path)) / session_id
        session_json = session_dir / "session.json"
        turns = session_dir / "turns.jsonl"
        if session_json.exists():
            data = json.loads(session_json.read_text(encoding="utf-8"))
            created_at = str(data.get("created_at", created_at))
        if turns.exists():
            prior_turn_count = sum(1 for line in turns.read_text(encoding="utf-8").splitlines() if line.strip())
    content = (
        f"session_id: {session_id or 'none'}\n"
        f"created_at: {created_at}\n"
        f"profile_id: {PROFILE_ID}\n"
        f"prior_turn_count: {prior_turn_count}\n"
        "model_response: none\nprovider_output: none"
    )
    block = create_prompt_block(
        block_id="session-context-block-v0412",
        block_kind=PromptBlockKind.SESSION_CONTEXT.value,
        title="Session Context",
        content=content,
        provenance=create_prompt_source_provenance(
            provenance_id="session-context-provenance-v0412",
            source_kind=PromptSourceKind.SESSION_STORE.value,
            source_path=str(_sessions_dir(_home_path(home_path)) / session_id) if session_id else None,
            source_present=bool(session_id),
            source_read=bool(session_id),
            chars_loaded=len(content),
        ),
        order_index=7,
    )
    defaults = {
        "block": block,
        "session_id": session_id,
        "prior_turn_count": prior_turn_count,
        "provider_output_present": False,
    }
    return SessionContextBlock(**_merge(defaults, overrides))


def assemble_default_personal_prompt(
    assembly_input: PromptAssemblyInput,
    policy: PromptAssemblyPolicy | None = None,
) -> PromptAssemblyResult:
    policy = policy or create_prompt_assembly_policy(profile_id=assembly_input.profile_id)
    warnings: list[str] = []
    missing: list[str] = []
    if not assembly_input.user_input.strip():
        warnings.append("user input is empty")
    safety = create_safety_invariant_block().block
    binding = create_soul_role_domain_binding(assembly_input.home_path, policy)
    missing.extend(binding.missing_identity_items)
    if binding.missing_identity_items:
        warnings.append("identity sources missing; preview continues with warnings")
    _, project_block = create_project_instruction_block(
        assembly_input.project_root,
        assembly_input.include_project_context,
        policy,
    )
    skill_policy = create_read_only_skill_policy_block().block
    restore = create_restore_summary_block().block if assembly_input.include_restore_summary else create_prompt_block(
        block_id="restore-summary-block-v0412",
        block_kind=PromptBlockKind.RESTORE_SUMMARY.value,
        title="Restore Summary",
        content="Restore summary omitted by request.",
        order_index=6,
    )
    session = create_session_context_block(assembly_input.home_path, assembly_input.session_id).block if assembly_input.include_session_context else create_prompt_block(
        block_id="session-context-block-v0412",
        block_kind=PromptBlockKind.SESSION_CONTEXT.value,
        title="Session Context",
        content="Session context omitted by request.",
        order_index=7,
    )
    user = create_prompt_block(
        block_id="user-input-block-v0412",
        block_kind=PromptBlockKind.USER_INPUT.value,
        title="User Input",
        content=assembly_input.user_input,
        provenance=create_prompt_source_provenance(
            provenance_id="user-input-provenance-v0412",
            source_kind=PromptSourceKind.USER_INPUT.value,
            chars_loaded=len(assembly_input.user_input),
        ),
        required=True,
        present=bool(assembly_input.user_input),
        order_index=8,
    )
    blocks = (
        safety,
        binding.soul_block,
        binding.role_block,
        binding.domain_block,
        project_block,
        skill_policy,
        restore,
        session,
        user,
    )
    rendered = "PROMPT PREVIEW ONLY - NOT A MODEL RESPONSE\n\n" + "\n\n".join(
        f"## {block.title}\n{block.content}" for block in sorted(blocks, key=lambda item: item.order_index)
    )
    if len(rendered) > policy.max_total_chars:
        rendered = rendered[: policy.max_total_chars]
        warnings.append("prompt preview truncated to max_total_chars")
    status = PromptAssemblyStatus.ASSEMBLED_WITH_WARNINGS.value if warnings else PromptAssemblyStatus.ASSEMBLED.value
    return PromptAssemblyResult(
        result_id="prompt-assembly-result-v0412",
        input_id=assembly_input.input_id,
        profile_id=assembly_input.profile_id,
        status=status,
        blocks=blocks,
        rendered_preview=rendered,
        warnings=tuple(warnings),
        missing_sources=tuple(missing),
        provider_invoked=False,
        prompt_submitted=False,
        agent_loop_started=False,
        skill_executed=False,
        session_written=False,
    )


def create_prompt_preview_command_input(**overrides: Any) -> PromptPreviewCommandInput:
    defaults = {
        "profile_id": PROFILE_ID,
        "home_path": None,
        "user_input": "",
        "project_root": None,
        "session_id": None,
    }
    return PromptPreviewCommandInput(**_merge(defaults, overrides))


def create_prompt_preview_command_result(command_input: PromptPreviewCommandInput, **overrides: Any) -> PromptPreviewCommandResult:
    assembly_input = PromptAssemblyInput(
        input_id="prompt-preview-command-input-v0412",
        profile_id=command_input.profile_id,
        home_path=command_input.home_path,
        user_input=command_input.user_input,
        project_root=command_input.project_root,
        session_id=command_input.session_id,
        include_project_context=True,
        include_restore_summary=True,
        include_session_context=True,
        metadata_only=True,
    )
    result = assemble_default_personal_prompt(assembly_input)
    defaults = {
        "status": result.status,
        "rendered_preview": result.rendered_preview,
        "warnings": result.warnings,
        "provider_invoked": False,
        "prompt_submitted": False,
        "session_written": False,
    }
    return PromptPreviewCommandResult(**_merge(defaults, overrides))


def create_default_personal_session_store_config(home_path: str | None = None, **overrides: Any) -> DefaultPersonalSessionStoreConfig:
    home = _home_path(home_path)
    defaults = {
        "profile_id": PROFILE_ID,
        "home_path": home,
        "sessions_dir": str(_sessions_dir(home)),
        "allow_create": True,
        "allow_append_turns": False,
        "allow_overwrite": False,
        "metadata_only": False,
    }
    return DefaultPersonalSessionStoreConfig(**_merge(defaults, overrides))


def create_default_personal_session_id(explicit_session_id: str | None = None, **overrides: Any) -> DefaultPersonalSessionId:
    defaults = {
        "session_id": explicit_session_id or f"session-{datetime.now(UTC).strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}",
        "explicit": explicit_session_id is not None,
    }
    return DefaultPersonalSessionId(**_merge(defaults, overrides))


def create_default_personal_session_record(
    session_id: str,
    home_path: str | None = None,
    **overrides: Any,
) -> DefaultPersonalSessionRecord:
    home = _home_path(home_path)
    session_dir = _sessions_dir(home) / session_id
    defaults = {
        "session_id": session_id,
        "profile_id": PROFILE_ID,
        "created_at": _now_iso(),
        "title": None,
        "status": "created",
        "session_dir": str(session_dir),
        "session_json_path": str(session_dir / "session.json"),
        "turns_jsonl_path": str(session_dir / "turns.jsonl"),
        "events_jsonl_path": str(session_dir / "events.jsonl"),
        "provider_invoked": False,
        "agent_loop_started": False,
        "production_certified": False,
    }
    return DefaultPersonalSessionRecord(**_merge(defaults, overrides))


def create_default_personal_session_create_request(home_path: str, **overrides: Any) -> DefaultPersonalSessionCreateRequest:
    defaults = {
        "profile_id": PROFILE_ID,
        "home_path": _home_path(home_path),
        "title": None,
        "explicit_session_id": None,
        "dry_run": False,
    }
    return DefaultPersonalSessionCreateRequest(**_merge(defaults, overrides))


def create_default_personal_session(
    request: DefaultPersonalSessionCreateRequest,
    **overrides: Any,
) -> DefaultPersonalSessionCreateResult:
    session_id = create_default_personal_session_id(request.explicit_session_id).session_id
    record = create_default_personal_session_record(session_id, request.home_path, title=request.title)
    paths = (Path(record.session_dir), Path(record.session_json_path), Path(record.turns_jsonl_path), Path(record.events_jsonl_path))
    outside = tuple(str(path) for path in paths if not _is_under_home(path, request.home_path))
    created_dirs: list[str] = []
    created_files: list[str] = []
    existing_files: list[str] = []
    status = "ok"
    if outside:
        status = "unsafe_denied"
        record_for_result: DefaultPersonalSessionRecord | None = None
    else:
        record_for_result = record
        if not request.dry_run:
            session_dir = Path(record.session_dir)
            if not session_dir.exists():
                session_dir.mkdir(parents=True, exist_ok=True)
                created_dirs.append(record.session_dir)
            payload = json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n"
            for path, content in (
                (Path(record.session_json_path), payload),
                (Path(record.turns_jsonl_path), ""),
                (Path(record.events_jsonl_path), json.dumps({"event": "session_created", "session_id": session_id}, sort_keys=True) + "\n"),
            ):
                if path.exists():
                    existing_files.append(str(path))
                else:
                    path.write_text(content, encoding="utf-8")
                    created_files.append(str(path))
    defaults = {
        "result_id": "default-personal-session-create-result-v0412",
        "profile_id": request.profile_id,
        "session_id": session_id,
        "session_record": record_for_result,
        "created_directories": tuple(created_dirs),
        "created_files": tuple(created_files),
        "existing_files": tuple(existing_files),
        "overwritten_files": (),
        "outside_home_paths": outside,
        "status": status,
        "provider_invoked": False,
        "prompt_submitted": False,
        "agent_loop_started": False,
        "skill_executed": False,
        "shell_executed": False,
        "network_accessed": False,
        "credentials_accessed": False,
    }
    return DefaultPersonalSessionCreateResult(**_merge(defaults, overrides))


def create_default_personal_session_list_request(home_path: str, **overrides: Any) -> DefaultPersonalSessionListRequest:
    defaults = {"profile_id": PROFILE_ID, "home_path": _home_path(home_path), "limit": None}
    return DefaultPersonalSessionListRequest(**_merge(defaults, overrides))


def list_default_personal_sessions(request: DefaultPersonalSessionListRequest, **overrides: Any) -> DefaultPersonalSessionListResult:
    sessions_dir = _sessions_dir(request.home_path)
    records: list[DefaultPersonalSessionRecord] = []
    warning = None
    if sessions_dir.exists():
        for child in sorted(path for path in sessions_dir.iterdir() if path.is_dir()):
            record = _session_record_from_dir(child, request.profile_id)
            if record:
                records.append(record)
                if request.limit is not None and len(records) >= request.limit:
                    break
    else:
        warning = "sessions directory missing"
    defaults = {
        "profile_id": request.profile_id,
        "home_path": request.home_path,
        "sessions": tuple(records),
        "status": "ok" if warning is None else "warning",
        "warning": warning,
        "provider_invoked": False,
        "prompt_submitted": False,
        "agent_loop_started": False,
    }
    return DefaultPersonalSessionListResult(**_merge(defaults, overrides))


def create_default_personal_session_store_safety_report(**overrides: Any) -> DefaultPersonalSessionStoreSafetyReport:
    defaults = {
        "report_id": "default-personal-session-store-safety-v0412",
        "profile_id": PROFILE_ID,
        "bounded_to_home": True,
        "overwrite_allowed": False,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "agent_loop_allowed": False,
        "shell_execution_allowed": False,
        "network_access_allowed": False,
        "credential_access_allowed": False,
        "production_certified": False,
    }
    return DefaultPersonalSessionStoreSafetyReport(**_merge(defaults, overrides))


def create_v0412_readiness_report(**overrides: Any) -> V0412ReadinessReport:
    defaults = {
        "report_id": "v0412-readiness-report",
        "prompt_assembly_defined": True,
        "prompt_preview_command_ready": True,
        "prompt_block_order_ready": True,
        "safety_invariant_block_ready": True,
        "soul_role_domain_binding_ready": True,
        "restore_summary_block_ready": True,
        "session_store_schema_ready": True,
        "session_new_command_ready": True,
        "session_list_command_ready": True,
        "integrated_restore_document_ready": True,
        "v0413_handoff_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return V0412ReadinessReport(**_merge(defaults, overrides))


def create_v0413_provider_probe_skill_registry_handoff(**overrides: Any) -> V0413ProviderProbeSkillRegistryHandoff:
    defaults = {
        "handoff_id": "v0413-provider-probe-skill-registry-handoff",
        "target_version": "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
        "recommended_focus": (
            "provider config loading",
            "provider doctor --no-completion",
            "redaction of sensitive provider config values",
            "optional loopback /models probe",
            "provider completion still closed in provider doctor",
            "static read-only skill registry",
            "read-only skill inspection",
            "unsafe skill denial",
            "no run/ask",
            "no AgentLoop",
            "no provider text completion yet",
        ),
        "still_closed": CLOSED_CAPABILITIES,
    }
    return V0413ProviderProbeSkillRegistryHandoff(**_merge(defaults, overrides))


def create_v0416_user_test_target_update(**overrides: Any) -> V0416UserTestTargetUpdate:
    defaults = {
        "target_id": "v0416-user-test-target-update-v0412",
        "target_version": "v0.41.6 Installable User-Test Release",
        "commands": V0416_TARGET_COMMANDS,
        "commands_expected_in_v0412": (
            "py -m pip install -e .",
            "chanta-cli --version",
            "chanta-cli doctor",
            'chanta-cli init default-personal --home "$env:LOCALAPPDATA\\ChantaCore"',
            "chanta-cli profile status --profile default-personal",
            'chanta-cli prompt preview --profile default-personal "Summarize current ChantaCore status."',
            "chanta-cli session new --profile default-personal",
            "chanta-cli session list --profile default-personal",
        ),
        "user_test_release_ready": False,
    }
    return V0416UserTestTargetUpdate(**_merge(defaults, overrides))


def create_v0412_integrated_restore_sections() -> tuple[V0412IntegratedRestoreSection, ...]:
    return tuple(
        V0412IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.41.2 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0412_integrated_restore_context_snapshot(**overrides: Any) -> V0412IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0412",
        "current_version": V0412_RELEASE_NAME,
        "current_track": V0412_TRACK_NAME,
        "baseline_versions": (
            "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
            "v0.41.0 Default Personal Profile Runtime Foundation",
            "v0.41.1 Installable CLI Bootstrap & Doctor",
            V0412_RELEASE_NAME,
        ),
        "open_capabilities": OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "next_recommended_version": "v0.41.3 Safe Provider Probe & Read-only Skill Registry",
    }
    return V0412IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0412_integrated_restore_packet(**overrides: Any) -> V0412IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0412",
        "snapshot": create_v0412_integrated_restore_context_snapshot(),
        "restore_sections": create_v0412_integrated_restore_sections(),
        "required_test_commands": (
            "tests/test_v0412_prompt_assembly_session_store.py",
            "tests/test_v0411_installable_cli_bootstrap_doctor.py",
            "tests/test_v0410_default_personal_profile_runtime.py",
            "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
        ),
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0412IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0412_integrated_restore_document_manifest(**overrides: Any) -> V0412IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0412",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0412IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def prompt_assembly_result_preserves_preview_only(result: PromptAssemblyResult) -> bool:
    return (
        not result.provider_invoked
        and not result.prompt_submitted
        and not result.agent_loop_started
        and not result.skill_executed
        and not result.session_written
    )


def session_create_result_preserves_runtime_closed(result: DefaultPersonalSessionCreateResult) -> bool:
    return (
        not result.overwritten_files
        and not result.outside_home_paths
        and not result.provider_invoked
        and not result.prompt_submitted
        and not result.agent_loop_started
        and not result.skill_executed
        and not result.shell_executed
        and not result.network_accessed
        and not result.credentials_accessed
    )


def session_safety_report_preserves_closed(report: DefaultPersonalSessionStoreSafetyReport) -> bool:
    return (
        report.bounded_to_home
        and not report.overwrite_allowed
        and not report.provider_invocation_allowed
        and not report.prompt_submission_allowed
        and not report.agent_loop_allowed
        and not report.shell_execution_allowed
        and not report.network_access_allowed
        and not report.credential_access_allowed
        and not report.production_certified
    )


def v0412_readiness_preserves_closed_runtime(report: V0412ReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0412IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


def _handle_prompt_preview(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("prompt")
    parser.add_argument("preview")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home")
    parser.add_argument("--project-root")
    parser.add_argument("--session-id")
    parser.add_argument("user_input")
    parsed = parser.parse_args(args)
    result = create_prompt_preview_command_result(
        PromptPreviewCommandInput(parsed.profile, parsed.home, parsed.user_input, parsed.project_root, parsed.session_id)
    )
    print(result.rendered_preview)
    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")
    return 0


def _handle_session_new(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("session")
    parser.add_argument("new")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--title")
    parser.add_argument("--session-id")
    parsed = parser.parse_args(args)
    request = create_default_personal_session_create_request(
        parsed.home,
        profile_id=parsed.profile,
        title=parsed.title,
        explicit_session_id=parsed.session_id,
    )
    result = create_default_personal_session(request)
    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    return 0 if result.status == "ok" else 2


def _handle_session_list(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog=CLI_NAME)
    parser.add_argument("session")
    parser.add_argument("list")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--home", required=True)
    parser.add_argument("--limit", type=int)
    parsed = parser.parse_args(args)
    result = list_default_personal_sessions(
        create_default_personal_session_list_request(parsed.home, profile_id=parsed.profile, limit=parsed.limit)
    )
    print(json.dumps(asdict(result), ensure_ascii=False, sort_keys=True))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in {"--version", "-V", "version"}:
        print("chanta-cli v0.41.1 / v0.41.2 prompt-session")
        return 0
    if args[0] == "doctor":
        print("chanta-cli doctor v0.41.1 / v0.41.2")
        print("next: v0.41.3 Safe Provider Probe & Read-only Skill Registry")
        print("prompt_preview: pass - deterministic local preview is available")
        print("session_store: pass - bounded session new/list are available")
        print("provider_invocation: closed")
        print("prompt_submission_to_model: closed")
        print("agent_loop: closed")
        print("skill_execution: closed")
        print("trace_runtime: closed")
        print("closed: " + ", ".join(CLOSED_CAPABILITIES))
        return 0
    if tuple(args[:2]) == ("prompt", "preview"):
        return _handle_prompt_preview(args)
    if tuple(args[:2]) == ("session", "new"):
        return _handle_session_new(args)
    if tuple(args[:2]) == ("session", "list"):
        return _handle_session_list(args)
    return v0411_main(args)


__all__ = [
    "CLOSED_CAPABILITIES",
    "INTEGRATED_DOC_PATH",
    "OPEN_CAPABILITIES",
    "PROFILE_ID",
    "PROMPT_BLOCK_ORDER",
    "PromptAssemblyInput",
    "PromptAssemblyPolicy",
    "PromptAssemblyResult",
    "PromptAssemblyStatus",
    "PromptBlock",
    "PromptBlockKind",
    "PromptPreviewCommandInput",
    "PromptPreviewCommandResult",
    "PromptSourceKind",
    "PromptSourceProvenance",
    "ProjectInstructionRef",
    "ReadOnlySkillPolicyBlock",
    "REQUIRED_FALSE_FLAGS",
    "REQUIRED_RESTORE_SECTION_IDS",
    "RestoreSummaryBlock",
    "SafetyInvariantBlock",
    "SessionContextBlock",
    "SoulRoleDomainBinding",
    "DefaultPersonalSessionCreateRequest",
    "DefaultPersonalSessionCreateResult",
    "DefaultPersonalSessionId",
    "DefaultPersonalSessionListRequest",
    "DefaultPersonalSessionListResult",
    "DefaultPersonalSessionRecord",
    "DefaultPersonalSessionStoreConfig",
    "DefaultPersonalSessionStoreSafetyReport",
    "DefaultPersonalSessionTurnRecord",
    "V0412IntegratedRestoreContextSnapshot",
    "V0412IntegratedRestoreDocumentManifest",
    "V0412IntegratedRestorePacket",
    "V0412IntegratedRestoreSection",
    "V0412ReadinessReport",
    "V0413ProviderProbeSkillRegistryHandoff",
    "V0416UserTestTargetUpdate",
    "assemble_default_personal_prompt",
    "create_default_personal_session",
    "create_default_personal_session_create_request",
    "create_default_personal_session_id",
    "create_default_personal_session_list_request",
    "create_default_personal_session_record",
    "create_default_personal_session_store_config",
    "create_default_personal_session_store_safety_report",
    "create_prompt_assembly_policy",
    "create_prompt_block",
    "create_prompt_preview_command_input",
    "create_prompt_preview_command_result",
    "create_prompt_source_provenance",
    "create_project_instruction_ref",
    "create_read_only_skill_policy_block",
    "create_restore_summary_block",
    "create_safety_invariant_block",
    "create_session_context_block",
    "create_soul_role_domain_binding",
    "create_v0412_integrated_restore_context_snapshot",
    "create_v0412_integrated_restore_document_manifest",
    "create_v0412_integrated_restore_packet",
    "create_v0412_integrated_restore_sections",
    "create_v0412_readiness_report",
    "create_v0413_provider_probe_skill_registry_handoff",
    "create_v0416_user_test_target_update",
    "integrated_restore_packet_uses_single_doc",
    "list_default_personal_sessions",
    "main",
    "prompt_assembly_result_preserves_preview_only",
    "session_create_result_preserves_runtime_closed",
    "session_safety_report_preserves_closed",
    "v0412_readiness_preserves_closed_runtime",
]
