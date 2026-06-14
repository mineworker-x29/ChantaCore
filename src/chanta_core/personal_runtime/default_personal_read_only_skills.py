"""v0.42.5 bounded read-only skill execution support.

This module opens only a narrow execution gate for bounded metadata/report
skills. Skill execution does not call providers, submit prompts, execute shell,
read arbitrary paths, mutate session/memory/workspace state, invoke subagents,
or certify production.
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

from chanta_core.personal_runtime.default_personal_chat_shell import main as _v0424_main
from chanta_core.personal_runtime.default_personal_cli_bootstrap import (
    PROFILE_ID,
    DefaultPersonalProfileStatusCommandInput,
    run_profile_status_command,
)
from chanta_core.personal_runtime.default_personal_home_quickstart import (
    create_v042_home_resolution_request,
    create_v042_home_status_command_input,
    create_v042_home_status_command_result,
    resolve_v042_home,
)
from chanta_core.personal_runtime.default_personal_provider_setup import (
    create_v042_provider_config_show_request,
    create_v042_provider_config_show_result,
    create_v042_provider_status_report,
    create_v042_provider_status_request,
)
from chanta_core.personal_runtime.default_personal_trace_history import (
    create_v042_run_history_request,
    create_v042_run_history_result,
    create_v042_session_show_request,
    create_v042_session_show_result,
    create_v042_trace_timeline_request,
    create_v042_trace_timeline_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    RuntimeObjectKind,
    append_runtime_event,
    create_last_run_report,
    create_last_run_report_request,
    create_runtime_event,
    create_runtime_object_ref,
    create_trace_store_config,
    create_trace_summary_request,
    summarize_trace_events,
)


V0425_VERSION = "v0.42.5"
V0425_RELEASE_NAME = "v0.42.5 Bounded Read-only Skill Execution"
V042_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.5_bounded_read_only_skill_execution_restore.md"


class V042SkillExecutionGateStatus(StrEnum):
    OPEN_FOR_BOUNDED_READ_ONLY = "open_for_bounded_read_only"
    CLOSED = "closed"
    DENIED = "denied"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class V042SkillCapabilityClass(StrEnum):
    METADATA_READ = "metadata_read"
    STATUS_READ = "status_read"
    TRACE_READ = "trace_read"
    RUN_READ = "run_read"
    SESSION_READ = "session_read"
    CONFIG_READ = "config_read"
    SAFETY_READ = "safety_read"
    PROVIDER_READ_NO_CALL = "provider_read_no_call"
    FILE_READ_ARBITRARY = "file_read_arbitrary"
    FILE_WRITE = "file_write"
    SHELL = "shell"
    PROVIDER_CALL = "provider_call"
    PROMPT_SUBMIT = "prompt_submit"
    FUNCTION_CALL = "function_call"
    TOOL_CALL = "tool_call"
    SUBAGENT = "subagent"
    MEMORY_WRITE = "memory_write"
    UNKNOWN = "unknown"


class V042SkillMutabilityClass(StrEnum):
    READ_ONLY = "read_only"
    TRACE_APPEND_ONLY = "trace_append_only"
    MUTATING = "mutating"
    DESTRUCTIVE = "destructive"
    UNKNOWN = "unknown"


class V042SkillBoundaryClass(StrEnum):
    BOUNDED_HOME = "bounded_home"
    BOUNDED_PROFILE = "bounded_profile"
    BOUNDED_TRACE_STORE = "bounded_trace_store"
    BOUNDED_SESSION_STORE = "bounded_session_store"
    BOUNDED_CONFIG = "bounded_config"
    ARBITRARY_PATH = "arbitrary_path"
    NETWORK = "network"
    SHELL = "shell"
    UNKNOWN = "unknown"


class V042SkillExecutionStatus(StrEnum):
    COMPLETED = "completed"
    DENIED = "denied"
    BLOCKED = "blocked"
    FAILED = "failed"
    SKIPPED = "skipped"
    DRY_RUN = "dry_run"


class V042SkillRiskLevel(StrEnum):
    LOW = "low"
    MODERATE = "moderate"
    HIGH = "high"
    FORBIDDEN = "forbidden"
    UNKNOWN = "unknown"


class V042SkillDenialReason(StrEnum):
    UNKNOWN_SKILL = "unknown_skill"
    EXECUTION_NOT_ALLOWED = "execution_not_allowed"
    FORBIDDEN_CAPABILITY = "forbidden_capability"
    INVALID_ARGS = "invalid_args"
    ARBITRARY_PATH_BLOCKED = "arbitrary_path_blocked"
    PROVIDER_CALL_BLOCKED = "provider_call_blocked"
    PROMPT_SUBMISSION_BLOCKED = "prompt_submission_blocked"
    SHELL_BLOCKED = "shell_blocked"
    SUBAGENT_BLOCKED = "subagent_blocked"
    MUTATION_BLOCKED = "mutation_blocked"
    OUTSIDE_HOME_BLOCKED = "outside_home_blocked"
    PRODUCTION_CERTIFICATION_BLOCKED = "production_certification_blocked"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042ReadOnlySkillDefinition:
    skill_id: str
    display_name: str
    description: str
    capability_class: str
    mutability_class: str
    boundary_class: str
    risk_level: str
    execution_allowed: bool
    requires_provider_call: bool
    submits_prompt: bool
    executes_shell: bool
    mutates_workspace: bool
    mutates_memory: bool
    mutates_session: bool
    appends_trace_event: bool
    allows_arbitrary_path: bool
    allows_network: bool
    max_limit: int | None
    safe_alternative: str | None


@dataclass(frozen=True)
class V042ReadOnlySkillRegistry:
    registry_id: str
    skills: tuple[V042ReadOnlySkillDefinition, ...]
    executable_skill_ids: tuple[str, ...]
    denied_skill_ids: tuple[str, ...]
    execution_gate_status: str
    provider_calls_allowed: bool
    prompt_submission_allowed: bool
    shell_execution_allowed: bool
    subagent_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillInputSchema:
    schema_id: str
    skill_id: str
    allowed_args: tuple[str, ...]
    required_args: tuple[str, ...]
    max_limit: int | None
    arbitrary_path_allowed: bool
    raw_shell_text_allowed: bool
    provider_prompt_allowed: bool


@dataclass(frozen=True)
class V042SkillExecutionRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    skill_id: str
    args: dict[str, object]
    display_format: str
    trace_execution: bool


@dataclass(frozen=True)
class V042SkillExecutionPlan:
    plan_id: str
    request: V042SkillExecutionRequest
    skill_definition: V042ReadOnlySkillDefinition | None
    input_schema: V042SkillInputSchema | None
    resolved_home_path: str | None
    gate_status: str
    safe_to_execute: bool
    denial_reason: str | None
    will_call_provider: bool
    will_submit_prompt: bool
    will_execute_shell: bool
    will_invoke_subagent: bool
    will_mutate_workspace: bool
    will_mutate_memory: bool
    will_mutate_session: bool
    will_append_trace: bool
    outside_home_paths: tuple[str, ...]


@dataclass(frozen=True)
class V042SkillExecutionTraceRecord:
    trace_record_id: str
    event_kind: str
    skill_id: str
    profile_id: str
    status: str
    message: str
    object_refs: tuple[dict[str, object], ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    session_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillExecutionResult:
    result_id: str
    request_id: str
    skill_id: str
    status: str
    rendered_text: str
    data: dict[str, object]
    trace_record: V042SkillExecutionTraceRecord | None
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    skill_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    memory_mutated: bool
    session_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillDenialResult:
    denial_id: str
    skill_id: str
    reason: str
    message: str
    safe_alternative: str
    trace_record: V042SkillExecutionTraceRecord | None
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillListRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    include_denied: bool
    display_format: str


@dataclass(frozen=True)
class V042SkillListResult:
    result_id: str
    skills: tuple[V042ReadOnlySkillDefinition, ...]
    executable_count: int
    denied_count: int
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillInspectRequest:
    request_id: str
    profile_id: str
    home_path: str | None
    skill_id: str
    display_format: str


@dataclass(frozen=True)
class V042SkillInspectResult:
    result_id: str
    skill_definition: V042ReadOnlySkillDefinition | None
    input_schema: V042SkillInputSchema | None
    found: bool
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillRunCommandInput:
    skill_id: str
    profile_id: str
    home_path: str | None
    args: dict[str, object]
    display_format: str
    trace_execution: bool


@dataclass(frozen=True)
class V042SkillRunCommandResult:
    result_id: str
    skill_id: str
    status: str
    execution_result: V042SkillExecutionResult | None
    denial_result: V042SkillDenialResult | None
    rendered_text: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillOutputRenderPolicy:
    policy_id: str
    default_format: str
    json_available: bool
    max_preview_chars: int
    redact_secrets: bool
    include_process_relevance: bool
    include_safety_flags: bool
    include_trace_reference: bool


@dataclass(frozen=True)
class V042SkillSafetyReport:
    report_id: str
    bounded_read_only_skill_execution_opened: bool
    provider_calls_allowed: bool
    prompt_submission_allowed: bool
    shell_execution_allowed: bool
    function_calling_allowed: bool
    tool_calling_allowed: bool
    subagent_invocation_allowed: bool
    arbitrary_path_read_allowed: bool
    workspace_mutation_allowed: bool
    memory_mutation_allowed: bool
    session_mutation_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillPIReviewRecord:
    review_id: str
    skill_id: str
    event_kind: str
    object_kind: str
    process_instance_id: str | None
    evidence_summary: str
    reconstructable_as_process_event: bool
    input_bounded: bool
    output_bounded: bool
    high_risk_counts_zero: bool


@dataclass(frozen=True)
class V042SkillEvidenceView:
    view_id: str
    skill_id: str
    execution_status: str
    trace_event_kind: str | None
    evidence_summary: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    workspace_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V042SkillClosedCapabilityMatrix:
    matrix_id: str
    shell_execution_closed: bool
    file_write_closed: bool
    file_read_arbitrary_closed: bool
    provider_call_closed_for_skills: bool
    prompt_submission_closed_for_skills: bool
    function_calling_closed: bool
    tool_calling_closed: bool
    subagent_closed: bool
    memory_write_closed: bool
    broad_scan_closed: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ChatSkillCommandPolicy:
    policy_id: str
    chat_skill_command_supported: bool
    allowed_skill_ids: tuple[str, ...]
    arbitrary_args_allowed: bool
    provider_call_allowed: bool
    prompt_submission_allowed: bool
    shell_allowed: bool
    subagent_allowed: bool


@dataclass(frozen=True)
class V0425ReadinessReport:
    bounded_read_only_skill_execution_ready: bool
    skill_list_command_ready: bool
    skill_inspect_command_ready: bool
    skill_run_command_ready: bool
    executable_safe_skill_subset_ready: bool
    unsafe_skill_denial_ready: bool
    skill_execution_trace_evidence_ready: bool
    skill_pi_review_record_ready: bool
    skill_output_render_policy_ready: bool
    skill_safety_report_ready: bool
    integrated_restore_document_ready: bool
    v0426_handoff_ready: bool
    chat_skill_command_ready: bool
    ready_for_shell_execution: bool
    ready_for_file_write: bool
    ready_for_arbitrary_file_read: bool
    ready_for_broad_filesystem_scan: bool
    ready_for_repo_search: bool
    ready_for_provider_call_from_skills: bool
    ready_for_prompt_submission_from_skills: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_subagent_invocation: bool
    ready_for_child_session_creation: bool
    ready_for_memory_write: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0426DiagnosticBundleFeedbackHandoff:
    target_version: str
    title: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0425IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0425IntegratedRestoreContextSnapshot:
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]


@dataclass(frozen=True)
class V0425IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0425IntegratedRestoreContextSnapshot
    sections: tuple[V0425IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0425IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    suitable_for_new_session_handoff: bool
    required_sections: tuple[str, ...]


EXECUTABLE_SKILL_IDS: tuple[str, ...] = (
    "profile_status",
    "home_status",
    "provider_status",
    "provider_config_show",
    "trace_summary",
    "trace_timeline",
    "run_report_last",
    "run_history",
    "session_show",
    "safety_summary",
    "config_view",
)

DENIED_SKILL_IDS: tuple[str, ...] = (
    "shell_command",
    "file_write",
    "file_read_arbitrary",
    "repo_search",
    "docs_reference_search",
    "code_edit",
    "patch_apply",
    "test_run",
    "provider_completion",
    "provider_tool_call",
    "function_call",
    "subagent_delegate",
    "memory_write",
    "broad_config_scan",
)

SKILL_CAPABILITY_MAP: dict[str, tuple[str, str]] = {
    "profile_status": (V042SkillCapabilityClass.STATUS_READ.value, V042SkillBoundaryClass.BOUNDED_PROFILE.value),
    "home_status": (V042SkillCapabilityClass.STATUS_READ.value, V042SkillBoundaryClass.BOUNDED_HOME.value),
    "provider_status": (V042SkillCapabilityClass.PROVIDER_READ_NO_CALL.value, V042SkillBoundaryClass.BOUNDED_CONFIG.value),
    "provider_config_show": (V042SkillCapabilityClass.CONFIG_READ.value, V042SkillBoundaryClass.BOUNDED_CONFIG.value),
    "trace_summary": (V042SkillCapabilityClass.TRACE_READ.value, V042SkillBoundaryClass.BOUNDED_TRACE_STORE.value),
    "trace_timeline": (V042SkillCapabilityClass.TRACE_READ.value, V042SkillBoundaryClass.BOUNDED_TRACE_STORE.value),
    "run_report_last": (V042SkillCapabilityClass.RUN_READ.value, V042SkillBoundaryClass.BOUNDED_TRACE_STORE.value),
    "run_history": (V042SkillCapabilityClass.RUN_READ.value, V042SkillBoundaryClass.BOUNDED_TRACE_STORE.value),
    "session_show": (V042SkillCapabilityClass.SESSION_READ.value, V042SkillBoundaryClass.BOUNDED_SESSION_STORE.value),
    "safety_summary": (V042SkillCapabilityClass.SAFETY_READ.value, V042SkillBoundaryClass.BOUNDED_TRACE_STORE.value),
    "config_view": (V042SkillCapabilityClass.CONFIG_READ.value, V042SkillBoundaryClass.BOUNDED_CONFIG.value),
}


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


def _resolve_home(home_path: str | None, command_name: str) -> str | None:
    resolved = resolve_v042_home(
        create_v042_home_resolution_request(
            explicit_home=home_path,
            command_name=command_name,
            allow_create=False,
            cwd=os.getcwd(),
        )
    )
    return resolved.home_path if resolved.safe_to_use else None


def _bounded_int(value: object, default: int, maximum: int) -> int:
    try:
        return max(1, min(int(value), maximum))
    except (TypeError, ValueError):
        return default


def _looks_like_path_argument(key: str, value: object) -> bool:
    lowered = key.lower()
    if lowered in {"path", "file", "filename", "directory", "root"}:
        return True
    if not isinstance(value, str):
        return False
    return value.startswith(("/", "\\")) or ".." in Path(value).parts or ":" in value


def create_v042_read_only_skill_definition(skill_id: str, **overrides: Any) -> V042ReadOnlySkillDefinition:
    if skill_id in EXECUTABLE_SKILL_IDS:
        capability, boundary = SKILL_CAPABILITY_MAP[skill_id]
        defaults = {
            "skill_id": skill_id,
            "display_name": skill_id.replace("_", " ").title(),
            "description": f"Bounded read-only {skill_id.replace('_', ' ')} report skill.",
            "capability_class": capability,
            "mutability_class": V042SkillMutabilityClass.TRACE_APPEND_ONLY.value,
            "boundary_class": boundary,
            "risk_level": V042SkillRiskLevel.LOW.value,
            "execution_allowed": True,
            "requires_provider_call": False,
            "submits_prompt": False,
            "executes_shell": False,
            "mutates_workspace": False,
            "mutates_memory": False,
            "mutates_session": False,
            "appends_trace_event": True,
            "allows_arbitrary_path": False,
            "allows_network": False,
            "max_limit": 200 if skill_id in {"trace_timeline", "run_history"} else 50 if skill_id == "session_show" else None,
            "safe_alternative": None,
        }
        return V042ReadOnlySkillDefinition(**_merge(defaults, overrides))

    capability = {
        "shell_command": V042SkillCapabilityClass.SHELL.value,
        "file_write": V042SkillCapabilityClass.FILE_WRITE.value,
        "file_read_arbitrary": V042SkillCapabilityClass.FILE_READ_ARBITRARY.value,
        "repo_search": V042SkillCapabilityClass.FILE_READ_ARBITRARY.value,
        "docs_reference_search": V042SkillCapabilityClass.FILE_READ_ARBITRARY.value,
        "provider_completion": V042SkillCapabilityClass.PROVIDER_CALL.value,
        "provider_tool_call": V042SkillCapabilityClass.TOOL_CALL.value,
        "function_call": V042SkillCapabilityClass.FUNCTION_CALL.value,
        "subagent_delegate": V042SkillCapabilityClass.SUBAGENT.value,
        "memory_write": V042SkillCapabilityClass.MEMORY_WRITE.value,
    }.get(skill_id, V042SkillCapabilityClass.UNKNOWN.value)
    defaults = {
        "skill_id": skill_id,
        "display_name": skill_id.replace("_", " ").title(),
        "description": "Non-executable v0.42.5 skill; capability remains denied.",
        "capability_class": capability,
        "mutability_class": V042SkillMutabilityClass.DESTRUCTIVE.value
        if skill_id in {"file_write", "code_edit", "patch_apply"}
        else V042SkillMutabilityClass.MUTATING.value,
        "boundary_class": V042SkillBoundaryClass.SHELL.value
        if skill_id == "shell_command"
        else V042SkillBoundaryClass.ARBITRARY_PATH.value
        if skill_id in {"file_read_arbitrary", "repo_search", "docs_reference_search", "broad_config_scan"}
        else V042SkillBoundaryClass.UNKNOWN.value,
        "risk_level": V042SkillRiskLevel.FORBIDDEN.value,
        "execution_allowed": False,
        "requires_provider_call": skill_id in {"provider_completion", "provider_tool_call"},
        "submits_prompt": skill_id in {"provider_completion", "provider_tool_call", "function_call"},
        "executes_shell": skill_id == "shell_command",
        "mutates_workspace": skill_id in {"file_write", "code_edit", "patch_apply", "test_run"},
        "mutates_memory": skill_id == "memory_write",
        "mutates_session": False,
        "appends_trace_event": False,
        "allows_arbitrary_path": skill_id in {"file_read_arbitrary", "repo_search", "docs_reference_search", "broad_config_scan"},
        "allows_network": skill_id in {"provider_completion", "provider_tool_call"},
        "max_limit": None,
        "safe_alternative": "Use a bounded read-only metadata/report skill such as profile_status, trace_summary, or run_history.",
    }
    return V042ReadOnlySkillDefinition(**_merge(defaults, overrides))


def build_v042_read_only_skill_registry(**overrides: Any) -> V042ReadOnlySkillRegistry:
    skills = tuple(create_v042_read_only_skill_definition(skill_id) for skill_id in (*EXECUTABLE_SKILL_IDS, *DENIED_SKILL_IDS))
    defaults = {
        "registry_id": "v0425-read-only-skill-registry",
        "skills": skills,
        "executable_skill_ids": EXECUTABLE_SKILL_IDS,
        "denied_skill_ids": DENIED_SKILL_IDS,
        "execution_gate_status": V042SkillExecutionGateStatus.OPEN_FOR_BOUNDED_READ_ONLY.value,
        "provider_calls_allowed": False,
        "prompt_submission_allowed": False,
        "shell_execution_allowed": False,
        "subagent_allowed": False,
        "production_certified": False,
    }
    return V042ReadOnlySkillRegistry(**_merge(defaults, overrides))


def create_v042_skill_input_schema(skill_id: str, **overrides: Any) -> V042SkillInputSchema:
    allowed_args: tuple[str, ...] = ()
    max_limit: int | None = None
    if skill_id in {"trace_timeline", "run_history"}:
        allowed_args = ("limit",)
        max_limit = 200
    elif skill_id == "session_show":
        allowed_args = ("target", "session_id", "max_turns")
        max_limit = 50
    defaults = {
        "schema_id": f"v0425-skill-input-schema-{skill_id}",
        "skill_id": skill_id,
        "allowed_args": allowed_args,
        "required_args": (),
        "max_limit": max_limit,
        "arbitrary_path_allowed": False,
        "raw_shell_text_allowed": False,
        "provider_prompt_allowed": False,
    }
    return V042SkillInputSchema(**_merge(defaults, overrides))


def create_v042_skill_execution_request(
    skill_id: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    args: Mapping[str, object] | None = None,
    display_format: str = "text",
    trace_execution: bool = True,
    **overrides: Any,
) -> V042SkillExecutionRequest:
    defaults = {
        "request_id": "v0425-skill-execution-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "skill_id": skill_id,
        "args": dict(args or {}),
        "display_format": display_format,
        "trace_execution": bool(trace_execution),
    }
    return V042SkillExecutionRequest(**_merge(defaults, overrides))


def _definition_by_id(registry: V042ReadOnlySkillRegistry, skill_id: str) -> V042ReadOnlySkillDefinition | None:
    return next((skill for skill in registry.skills if skill.skill_id == skill_id), None)


def validate_v042_skill_execution_request(
    request: V042SkillExecutionRequest,
    registry: V042ReadOnlySkillRegistry | None = None,
) -> str | None:
    actual_registry = registry or build_v042_read_only_skill_registry()
    definition = _definition_by_id(actual_registry, request.skill_id)
    if definition is None:
        return V042SkillDenialReason.UNKNOWN_SKILL.value
    if not definition.execution_allowed:
        return V042SkillDenialReason.EXECUTION_NOT_ALLOWED.value
    schema = create_v042_skill_input_schema(request.skill_id)
    unknown_args = set(request.args) - set(schema.allowed_args)
    if unknown_args:
        return V042SkillDenialReason.INVALID_ARGS.value
    if any(_looks_like_path_argument(key, value) for key, value in request.args.items()):
        return V042SkillDenialReason.ARBITRARY_PATH_BLOCKED.value
    if "limit" in request.args and _bounded_int(request.args["limit"], 10, schema.max_limit or 10) != int(request.args["limit"]):
        return V042SkillDenialReason.INVALID_ARGS.value
    if "max_turns" in request.args and _bounded_int(request.args["max_turns"], 10, schema.max_limit or 10) != int(request.args["max_turns"]):
        return V042SkillDenialReason.INVALID_ARGS.value
    if request.skill_id == "session_show":
        target = str(request.args.get("target", "last"))
        if target not in {"last", "session_id"}:
            return V042SkillDenialReason.INVALID_ARGS.value
        if target == "session_id" and not request.args.get("session_id"):
            return V042SkillDenialReason.INVALID_ARGS.value
    return None


def create_v042_skill_execution_plan(request: V042SkillExecutionRequest, **overrides: Any) -> V042SkillExecutionPlan:
    registry = build_v042_read_only_skill_registry()
    definition = _definition_by_id(registry, request.skill_id)
    schema = create_v042_skill_input_schema(request.skill_id) if definition else None
    home = _resolve_home(request.home_path, "skill run")
    denial_reason = validate_v042_skill_execution_request(request, registry)
    if home is None:
        denial_reason = denial_reason or V042SkillDenialReason.OUTSIDE_HOME_BLOCKED.value
    safe = definition is not None and denial_reason is None and bool(home)
    defaults = {
        "plan_id": "v0425-skill-execution-plan",
        "request": request,
        "skill_definition": definition,
        "input_schema": schema,
        "resolved_home_path": home,
        "gate_status": V042SkillExecutionGateStatus.OPEN_FOR_BOUNDED_READ_ONLY.value if safe else V042SkillExecutionGateStatus.DENIED.value,
        "safe_to_execute": safe,
        "denial_reason": denial_reason,
        "will_call_provider": False,
        "will_submit_prompt": False,
        "will_execute_shell": False,
        "will_invoke_subagent": False,
        "will_mutate_workspace": False,
        "will_mutate_memory": False,
        "will_mutate_session": False,
        "will_append_trace": bool(safe and request.trace_execution),
        "outside_home_paths": (),
    }
    return V042SkillExecutionPlan(**_merge(defaults, overrides))


def create_v042_skill_execution_trace_record(
    skill_id: str,
    profile_id: str = PROFILE_ID,
    status: str = V042SkillExecutionStatus.COMPLETED.value,
    event_kind: str = "read_only_skill_executed",
    message: str | None = None,
    **overrides: Any,
) -> V042SkillExecutionTraceRecord:
    defaults = {
        "trace_record_id": f"v0425-skill-trace-{skill_id}",
        "event_kind": event_kind,
        "skill_id": skill_id,
        "profile_id": profile_id,
        "status": status,
        "message": message or f"Bounded read-only skill {skill_id} {status}.",
        "object_refs": ({"object_kind": "skill", "object_id": skill_id, "bounded": True},),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "session_mutated": False,
        "production_certified": False,
    }
    return V042SkillExecutionTraceRecord(**_merge(defaults, overrides))


def _append_skill_trace_event(
    plan: V042SkillExecutionPlan,
    trace_record: V042SkillExecutionTraceRecord | None,
    *,
    skill_executed: bool,
) -> None:
    if not trace_record or not plan.resolved_home_path:
        return
    event = create_runtime_event(
        trace_record.event_kind,
        trace_record.status,
        profile_id=plan.request.profile_id,
        command_name="skill run",
        objects=(
            create_runtime_object_ref(
                plan.request.skill_id,
                RuntimeObjectKind.SKILL.value,
                display_name=plan.request.skill_id,
                metadata={"bounded": True, "read_only": True},
            ),
        ),
        message=trace_record.message,
        metadata={"skill_id": plan.request.skill_id, "bounded_read_only": True},
        provider_invoked=False,
        prompt_submitted=False,
        skill_executed=skill_executed,
        shell_executed=False,
        workspace_mutated=False,
        subagent_invoked=False,
        production_certified=False,
    )
    append_runtime_event(event, create_trace_store_config(plan.request.profile_id, plan.resolved_home_path))


def _data_dict(value: Any) -> dict[str, object]:
    ready = _json_ready(value)
    return ready if isinstance(ready, dict) else {"value": ready}


def _render_skill_output(skill_id: str, rendered_text: str, status: str) -> str:
    return "\n".join(
        (
            f"ChantaCore skill run: {skill_id}",
            f"status: {status}",
            "provider_invoked: false",
            "prompt_submitted: false",
            "shell_executed: false",
            rendered_text,
        )
    )


def _execute_skill_payload(plan: V042SkillExecutionPlan) -> tuple[str, dict[str, object]]:
    request = plan.request
    home = plan.resolved_home_path or ""
    if request.skill_id == "profile_status":
        result = run_profile_status_command(DefaultPersonalProfileStatusCommandInput(request.profile_id, home))
        rendered = "\n".join(
            (
                "ChantaCore profile status",
                f"profile: {result.profile_id}",
                f"home: {result.home_path}",
                f"status: {result.status}",
                f"profile_exists: {str(result.profile_exists).lower()}",
                f"message: {result.message}",
            )
        )
        return rendered, _data_dict(result)
    if request.skill_id == "home_status":
        result = create_v042_home_status_command_result(create_v042_home_status_command_input(home, request.profile_id))
        return result.rendered_text, _data_dict(result)
    if request.skill_id == "provider_status":
        result = create_v042_provider_status_report(create_v042_provider_status_request(home, request.profile_id))
        return result.rendered_text, _data_dict(result)
    if request.skill_id == "provider_config_show":
        result = create_v042_provider_config_show_result(create_v042_provider_config_show_request(home, request.profile_id))
        return result.rendered_text, _data_dict(result)
    if request.skill_id == "trace_summary":
        result = summarize_trace_events(create_trace_summary_request(request.profile_id, home))
        return _render_json(result), _data_dict(result)
    if request.skill_id == "trace_timeline":
        limit = _bounded_int(request.args.get("limit", 10), 10, 200)
        result = create_v042_trace_timeline_result(create_v042_trace_timeline_request(request.profile_id, home, limit))
        return result.rendered_text, _data_dict(result)
    if request.skill_id == "run_report_last":
        result = create_last_run_report(create_last_run_report_request(request.profile_id, home))
        return _render_json(result), _data_dict(result)
    if request.skill_id == "run_history":
        limit = _bounded_int(request.args.get("limit", 10), 10, 200)
        result = create_v042_run_history_result(create_v042_run_history_request(request.profile_id, home, limit))
        return result.rendered_text, _data_dict(result)
    if request.skill_id == "session_show":
        target = str(request.args.get("target", "last"))
        session_id = request.args.get("session_id")
        max_turns = _bounded_int(request.args.get("max_turns", 10), 10, 50)
        result = create_v042_session_show_result(
            create_v042_session_show_request(
                request.profile_id,
                home,
                target,
                str(session_id) if session_id else None,
                "text",
                True,
                max_turns,
            )
        )
        return result.rendered_text, _data_dict(result)
    if request.skill_id == "safety_summary":
        summary = summarize_trace_events(create_trace_summary_request(request.profile_id, home))
        data = {
            "shell_execution_count": summary.shell_execution_count,
            "skill_execution_count": summary.skill_execution_count,
            "subagent_invocation_count": summary.subagent_invocation_count,
            "production_certification_count": summary.production_certification_count,
            "provider_tool_calling_count": 0,
            "function_calling_count": 0,
            "safe_for_v0425_review": summary.shell_execution_count == 0 and summary.subagent_invocation_count == 0 and summary.production_certification_count == 0,
        }
        rendered = "\n".join(f"{key}: {value}" for key, value in data.items())
        return rendered, data
    if request.skill_id == "config_view":
        provider = create_v042_provider_config_show_result(create_v042_provider_config_show_request(home, request.profile_id))
        profile_path = Path(home) / "profiles" / request.profile_id / "profile.json"
        data = {
            "profile_config_path": str(profile_path),
            "profile_config_present": profile_path.exists(),
            "provider_config_path": provider.config_path,
            "provider_config_present": provider.config_present,
            "provider_config_redacted": provider.redacted_config,
            "secret_values_redacted": True,
        }
        rendered = "\n".join(
            (
                "ChantaCore bounded config view",
                f"profile_config_present: {str(data['profile_config_present']).lower()}",
                f"provider_config_present: {str(data['provider_config_present']).lower()}",
                "secret_values_redacted: true",
            )
        )
        return rendered, data
    return "Skill is not executable in v0.42.5.", {}


def create_v042_skill_execution_result(
    plan: V042SkillExecutionPlan,
    rendered_text: str,
    data: Mapping[str, object] | None = None,
    **overrides: Any,
) -> V042SkillExecutionResult:
    trace_record = create_v042_skill_execution_trace_record(plan.request.skill_id, plan.request.profile_id) if plan.request.trace_execution else None
    _append_skill_trace_event(plan, trace_record, skill_executed=True)
    defaults = {
        "result_id": "v0425-skill-execution-result",
        "request_id": plan.request.request_id,
        "skill_id": plan.request.skill_id,
        "status": V042SkillExecutionStatus.COMPLETED.value,
        "rendered_text": rendered_text,
        "data": dict(data or {}),
        "trace_record": trace_record,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "skill_executed": True,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "memory_mutated": False,
        "session_mutated": False,
        "production_certified": False,
    }
    return V042SkillExecutionResult(**_merge(defaults, overrides))


def create_v042_skill_denial_result(plan: V042SkillExecutionPlan, **overrides: Any) -> V042SkillDenialResult:
    definition = plan.skill_definition
    reason = plan.denial_reason or V042SkillDenialReason.UNKNOWN.value
    trace_record = create_v042_skill_execution_trace_record(
        plan.request.skill_id,
        plan.request.profile_id,
        status=V042SkillExecutionStatus.DENIED.value,
        event_kind="read_only_skill_denied",
        message=f"Read-only skill request denied: {reason}.",
    ) if plan.request.trace_execution else None
    _append_skill_trace_event(plan, trace_record, skill_executed=False)
    defaults = {
        "denial_id": f"v0425-skill-denial-{plan.request.skill_id}",
        "skill_id": plan.request.skill_id,
        "reason": reason,
        "message": f"Skill '{plan.request.skill_id}' is denied by the v0.42.5 bounded read-only gate.",
        "safe_alternative": (definition.safe_alternative if definition and definition.safe_alternative else "Use skill list to choose a bounded read-only skill."),
        "trace_record": trace_record,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V042SkillDenialResult(**_merge(defaults, overrides))


def execute_v042_read_only_skill(plan: V042SkillExecutionPlan) -> V042SkillExecutionResult | V042SkillDenialResult:
    if not plan.safe_to_execute:
        return create_v042_skill_denial_result(plan)
    rendered, data = _execute_skill_payload(plan)
    output = _render_skill_output(plan.request.skill_id, rendered, V042SkillExecutionStatus.COMPLETED.value)
    if plan.request.display_format == "json":
        output = _render_json({"skill_id": plan.request.skill_id, "status": V042SkillExecutionStatus.COMPLETED.value, "data": data})
    return create_v042_skill_execution_result(plan, output, data)


def create_v042_skill_list_request(
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    include_denied: bool = True,
    display_format: str = "text",
    **overrides: Any,
) -> V042SkillListRequest:
    defaults = {
        "request_id": "v0425-skill-list-request",
        "profile_id": profile_id,
        "home_path": home_path,
        "include_denied": include_denied,
        "display_format": display_format,
    }
    return V042SkillListRequest(**_merge(defaults, overrides))


def _render_skill_list(skills: Sequence[V042ReadOnlySkillDefinition]) -> str:
    lines = ["ChantaCore bounded read-only skills"]
    for skill in skills:
        status = "executable" if skill.execution_allowed else "denied"
        lines.append(f"- {skill.skill_id}: {status}; {skill.capability_class}; {skill.boundary_class}")
    lines.append("skill execution never calls providers, submits prompts, executes shell, invokes subagents, or certifies production.")
    return "\n".join(lines)


def create_v042_skill_list_result(request: V042SkillListRequest, **overrides: Any) -> V042SkillListResult:
    registry = build_v042_read_only_skill_registry()
    skills = registry.skills if request.include_denied else tuple(skill for skill in registry.skills if skill.execution_allowed)
    defaults = {
        "result_id": "v0425-skill-list-result",
        "skills": skills,
        "executable_count": len(registry.executable_skill_ids),
        "denied_count": len(registry.denied_skill_ids),
        "rendered_text": _render_json(skills) if request.display_format == "json" else _render_skill_list(skills),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V042SkillListResult(**_merge(defaults, overrides))


def create_v042_skill_inspect_request(
    skill_id: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    display_format: str = "text",
    **overrides: Any,
) -> V042SkillInspectRequest:
    defaults = {"request_id": "v0425-skill-inspect-request", "profile_id": profile_id, "home_path": home_path, "skill_id": skill_id, "display_format": display_format}
    return V042SkillInspectRequest(**_merge(defaults, overrides))


def _render_skill_inspect(definition: V042ReadOnlySkillDefinition | None, schema: V042SkillInputSchema | None) -> str:
    if definition is None:
        return "Skill not found."
    return "\n".join(
        (
            f"ChantaCore skill inspect: {definition.skill_id}",
            f"execution_allowed: {str(definition.execution_allowed).lower()}",
            f"risk_level: {definition.risk_level}",
            f"capability_class: {definition.capability_class}",
            f"boundary_class: {definition.boundary_class}",
            f"allowed_args: {', '.join(schema.allowed_args) if schema else '-'}",
            f"safe_alternative: {definition.safe_alternative or '-'}",
            "provider_call: false",
            "prompt_submission: false",
            "shell_execution: false",
        )
    )


def create_v042_skill_inspect_result(request: V042SkillInspectRequest, **overrides: Any) -> V042SkillInspectResult:
    registry = build_v042_read_only_skill_registry()
    definition = _definition_by_id(registry, request.skill_id)
    schema = create_v042_skill_input_schema(request.skill_id) if definition else None
    rendered = _render_json({"skill_definition": definition, "input_schema": schema}) if request.display_format == "json" else _render_skill_inspect(definition, schema)
    defaults = {
        "result_id": "v0425-skill-inspect-result",
        "skill_definition": definition,
        "input_schema": schema,
        "found": definition is not None,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "production_certified": False,
    }
    return V042SkillInspectResult(**_merge(defaults, overrides))


def create_v042_skill_run_command_input(
    skill_id: str,
    profile_id: str = PROFILE_ID,
    home_path: str | None = None,
    args: Mapping[str, object] | None = None,
    display_format: str = "text",
    trace_execution: bool = True,
    **overrides: Any,
) -> V042SkillRunCommandInput:
    defaults = {"skill_id": skill_id, "profile_id": profile_id, "home_path": home_path, "args": dict(args or {}), "display_format": display_format, "trace_execution": bool(trace_execution)}
    return V042SkillRunCommandInput(**_merge(defaults, overrides))


def create_v042_skill_run_command_result(command_input: V042SkillRunCommandInput, **overrides: Any) -> V042SkillRunCommandResult:
    request = create_v042_skill_execution_request(
        command_input.skill_id,
        command_input.profile_id,
        command_input.home_path,
        command_input.args,
        command_input.display_format,
        command_input.trace_execution,
    )
    plan = create_v042_skill_execution_plan(request)
    outcome = execute_v042_read_only_skill(plan)
    execution = outcome if isinstance(outcome, V042SkillExecutionResult) else None
    denial = outcome if isinstance(outcome, V042SkillDenialResult) else None
    status = execution.status if execution else V042SkillExecutionStatus.DENIED.value
    rendered = execution.rendered_text if execution else _render_json(denial) if command_input.display_format == "json" else "\n".join((denial.message, f"reason: {denial.reason}", f"safe_alternative: {denial.safe_alternative}", "shell_executed: false"))
    defaults = {
        "result_id": "v0425-skill-run-command-result",
        "skill_id": command_input.skill_id,
        "status": status,
        "execution_result": execution,
        "denial_result": denial,
        "rendered_text": rendered,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V042SkillRunCommandResult(**_merge(defaults, overrides))


def create_v042_skill_output_render_policy(**overrides: Any) -> V042SkillOutputRenderPolicy:
    defaults = {
        "policy_id": "v0425-skill-output-render-policy",
        "default_format": "text",
        "json_available": True,
        "max_preview_chars": 400,
        "redact_secrets": True,
        "include_process_relevance": True,
        "include_safety_flags": True,
        "include_trace_reference": True,
    }
    return V042SkillOutputRenderPolicy(**_merge(defaults, overrides))


def create_v042_skill_safety_report(**overrides: Any) -> V042SkillSafetyReport:
    defaults = {
        "report_id": "v0425-skill-safety-report",
        "bounded_read_only_skill_execution_opened": True,
        "provider_calls_allowed": False,
        "prompt_submission_allowed": False,
        "shell_execution_allowed": False,
        "function_calling_allowed": False,
        "tool_calling_allowed": False,
        "subagent_invocation_allowed": False,
        "arbitrary_path_read_allowed": False,
        "workspace_mutation_allowed": False,
        "memory_mutation_allowed": False,
        "session_mutation_allowed": False,
        "production_certified": False,
    }
    return V042SkillSafetyReport(**_merge(defaults, overrides))


def create_v042_skill_pi_review_record(skill_id: str, event_kind: str = "read_only_skill_executed", **overrides: Any) -> V042SkillPIReviewRecord:
    defaults = {
        "review_id": f"v0425-skill-pi-review-{skill_id}",
        "skill_id": skill_id,
        "event_kind": event_kind,
        "object_kind": "skill",
        "process_instance_id": f"skill:{skill_id}",
        "evidence_summary": "Bounded read-only skill execution is reconstructable as a process event.",
        "reconstructable_as_process_event": True,
        "input_bounded": True,
        "output_bounded": True,
        "high_risk_counts_zero": True,
    }
    return V042SkillPIReviewRecord(**_merge(defaults, overrides))


def create_v042_skill_evidence_view(
    result: V042SkillExecutionResult | V042SkillDenialResult,
    **overrides: Any,
) -> V042SkillEvidenceView:
    trace_record = result.trace_record
    status = result.status if isinstance(result, V042SkillExecutionResult) else V042SkillExecutionStatus.DENIED.value
    defaults = {
        "view_id": f"v0425-skill-evidence-{result.skill_id}",
        "skill_id": result.skill_id,
        "execution_status": status,
        "trace_event_kind": trace_record.event_kind if trace_record else None,
        "evidence_summary": f"Skill {result.skill_id} status={status}; provider/prompt/shell/subagent/workspace mutation all false.",
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "subagent_invoked": False,
        "workspace_mutated": False,
        "production_certified": False,
    }
    return V042SkillEvidenceView(**_merge(defaults, overrides))


def create_v042_skill_closed_capability_matrix(**overrides: Any) -> V042SkillClosedCapabilityMatrix:
    defaults = {
        "matrix_id": "v0425-skill-closed-capability-matrix",
        "shell_execution_closed": True,
        "file_write_closed": True,
        "file_read_arbitrary_closed": True,
        "provider_call_closed_for_skills": True,
        "prompt_submission_closed_for_skills": True,
        "function_calling_closed": True,
        "tool_calling_closed": True,
        "subagent_closed": True,
        "memory_write_closed": True,
        "broad_scan_closed": True,
        "production_certified": False,
    }
    return V042SkillClosedCapabilityMatrix(**_merge(defaults, overrides))


def create_v042_chat_skill_command_policy(**overrides: Any) -> V042ChatSkillCommandPolicy:
    defaults = {
        "policy_id": "v0425-chat-skill-command-policy",
        "chat_skill_command_supported": False,
        "allowed_skill_ids": EXECUTABLE_SKILL_IDS,
        "arbitrary_args_allowed": False,
        "provider_call_allowed": False,
        "prompt_submission_allowed": False,
        "shell_allowed": False,
        "subagent_allowed": False,
    }
    return V042ChatSkillCommandPolicy(**_merge(defaults, overrides))


def create_v0425_readiness_report(**overrides: Any) -> V0425ReadinessReport:
    defaults = {
        "bounded_read_only_skill_execution_ready": True,
        "skill_list_command_ready": True,
        "skill_inspect_command_ready": True,
        "skill_run_command_ready": True,
        "executable_safe_skill_subset_ready": True,
        "unsafe_skill_denial_ready": True,
        "skill_execution_trace_evidence_ready": True,
        "skill_pi_review_record_ready": True,
        "skill_output_render_policy_ready": True,
        "skill_safety_report_ready": True,
        "integrated_restore_document_ready": True,
        "v0426_handoff_ready": True,
        "chat_skill_command_ready": False,
        "ready_for_shell_execution": False,
        "ready_for_file_write": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_broad_filesystem_scan": False,
        "ready_for_repo_search": False,
        "ready_for_provider_call_from_skills": False,
        "ready_for_prompt_submission_from_skills": False,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_subagent_invocation": False,
        "ready_for_child_session_creation": False,
        "ready_for_memory_write": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0425ReadinessReport(**_merge(defaults, overrides))


def create_v0426_diagnostic_bundle_feedback_handoff(**overrides: Any) -> V0426DiagnosticBundleFeedbackHandoff:
    defaults = {
        "target_version": "v0.42.6 Diagnostic Bundle & User Feedback Loop",
        "title": "Diagnostic Bundle & User Feedback Loop",
        "recommended_focus": (
            "chanta-cli report bundle",
            "chanta-cli feedback note",
            "collect version, home/profile/provider status, last run, run history, trace summary, skill execution summary, denial summary, closed capabilities, known limitations",
            "redact secrets",
            "produce copy-paste GPT/Codex handoff text",
        ),
        "must_not_open": ("shell_execution", "file_edit", "patch_apply", "provider_tool_calling", "function_calling", "subagent_invocation", "autonomous_agent_loop", "production_certification"),
        "production_certified": False,
    }
    return V0426DiagnosticBundleFeedbackHandoff(**_merge(defaults, overrides))


REQUIRED_V0425_RESTORE_SECTIONS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "project_context_for_new_codex_session",
    "v0416_user_test_baseline",
    "v0420_ux_baseline_summary",
    "v0421_home_quickstart_summary",
    "v0422_provider_setup_summary",
    "v0423_trace_history_summary",
    "v0424_chat_shell_summary",
    "bounded_read_only_skill_execution_summary",
    "skill_execution_gate_contract",
    "executable_skill_subset",
    "denied_skill_subset",
    "skill_input_schema_contract",
    "skill_run_command_contract",
    "skill_trace_evidence_contract",
    "skill_denial_contract",
    "skill_pi_review_contract",
    "skill_safety_boundary",
    "chat_skill_command_policy",
    "runtime_opening_status",
    "still_closed_capabilities",
    "required_test_commands",
    "expected_test_interpretation",
    "withdrawal_conditions",
    "v0426_handoff",
    "copy_paste_restore_prompt",
)


def create_v0425_integrated_restore_context_snapshot(**overrides: Any) -> V0425IntegratedRestoreContextSnapshot:
    defaults = {
        "current_version": "v0.42.5 Bounded Read-only Skill Execution",
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
            "v0.42.3 Human-readable Trace / Run History",
            "v0.42.4 Interactive Manual Chat Shell",
            "v0.42.5 Bounded Read-only Skill Execution",
        ),
        "open_capabilities": (
            "bounded_read_only_skill_execution_gate",
            "skill_list_command",
            "skill_inspect_command",
            "skill_run_command",
            "profile_status_skill_execution",
            "home_status_skill_execution",
            "provider_status_skill_execution",
            "provider_config_show_skill_execution",
            "trace_summary_skill_execution",
            "trace_timeline_skill_execution",
            "run_report_last_skill_execution",
            "run_history_skill_execution",
            "session_show_skill_execution",
            "safety_summary_skill_execution",
            "config_view_skill_execution",
            "unsafe_skill_denial",
            "skill_execution_trace_evidence",
            "skill_pi_review_record",
            "skill_safety_report",
            "integrated_restore_document",
        ),
        "closed_capabilities": (
            "shell_execution",
            "file_write",
            "arbitrary_file_read",
            "broad_filesystem_scan",
            "repo_search",
            "provider_call_from_skills",
            "prompt_submission_from_skills",
            "provider_doctor_completion",
            "provider_tool_calling",
            "function_calling",
            "general_agent_loop",
            "multi_step_agent_loop",
            "subagent_invocation",
            "child_session_creation",
            "memory_write",
            "autonomous_retry_loop",
            "dominion_runtime",
            "production_certification",
        ),
    }
    return V0425IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0425_integrated_restore_packet(**overrides: Any) -> V0425IntegratedRestorePacket:
    sections = tuple(V0425IntegratedRestoreSection(section, section.replace("_", " ").title(), True) for section in REQUIRED_V0425_RESTORE_SECTIONS)
    defaults = {
        "packet_id": "v0425-integrated-restore-packet",
        "context_snapshot": create_v0425_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0425IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0425_integrated_restore_document_manifest(**overrides: Any) -> V0425IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0425-integrated-restore-document-manifest",
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "suitable_for_new_session_handoff": True,
        "required_sections": REQUIRED_V0425_RESTORE_SECTIONS,
    }
    return V0425IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _handle_skill_list(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli skill list")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--include-denied", action="store_true", default=True)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    result = create_v042_skill_list_result(create_v042_skill_list_request(parsed.profile, parsed.home, parsed.include_denied, "json" if parsed.json else "text"))
    print(result.rendered_text)
    return 0


def _handle_skill_inspect(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli skill inspect")
    parser.add_argument("skill_id")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    result = create_v042_skill_inspect_result(create_v042_skill_inspect_request(parsed.skill_id, parsed.profile, parsed.home, "json" if parsed.json else "text"))
    print(result.rendered_text)
    return 0 if result.found else 1


def _handle_skill_run(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli skill run")
    parser.add_argument("skill_id")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--target", choices=["last", "session_id"])
    parser.add_argument("--session-id")
    parser.add_argument("--max-turns", type=int)
    parser.add_argument("--no-trace", action="store_true")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    skill_args: dict[str, object] = {}
    if parsed.limit is not None:
        skill_args["limit"] = parsed.limit
    if parsed.target is not None:
        skill_args["target"] = parsed.target
    if parsed.session_id is not None:
        skill_args["session_id"] = parsed.session_id
    if parsed.max_turns is not None:
        skill_args["max_turns"] = parsed.max_turns
    result = create_v042_skill_run_command_result(
        create_v042_skill_run_command_input(
            parsed.skill_id,
            parsed.profile,
            parsed.home,
            skill_args,
            "json" if parsed.json else "text",
            not parsed.no_trace,
        )
    )
    print(result.rendered_text)
    return 0 if result.execution_result else 1


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0425_VERSION}; {V0425_RELEASE_NAME})")
        return 0
    if len(args) >= 2 and args[0] == "skill" and args[1] == "list":
        return _handle_skill_list(args[2:])
    if len(args) >= 2 and args[0] == "skill" and args[1] == "inspect":
        return _handle_skill_inspect(args[2:])
    if len(args) >= 2 and args[0] == "skill" and args[1] == "run":
        return _handle_skill_run(args[2:])
    return _v0424_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V042")
    or name.startswith("create_v042")
    or name.startswith("build_v042")
    or name.startswith("execute_v042")
    or name.startswith("validate_v042")
    or name == "main"
]
