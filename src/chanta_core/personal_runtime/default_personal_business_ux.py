"""v0.42.9 business-agent UX polish for default-personal runtime.

This layer changes default presentation, not runtime authority. Trace,
run-report, diagnostic bundle, JSON, and debug paths remain available while
ordinary output is kept calm and business-user-facing.
"""

from __future__ import annotations

import argparse
import contextlib
import io
import json
import sys
from dataclasses import asdict, dataclass, is_dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence

from chanta_core.personal_runtime.default_personal_home_quickstart import (
    PROFILE_ID,
    create_v042_home_resolution_request,
    resolve_v042_home,
)
from chanta_core.personal_runtime.default_personal_provider_response import main as _v0428_main
from chanta_core.personal_runtime.default_personal_provider_setup import (
    V042ProviderStatusReport,
    create_v042_provider_status_report,
    create_v042_provider_status_request,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    LastRunReportResult,
    create_last_run_report,
    create_last_run_report_request,
)


V0429_VERSION = "v0.42.9"
V0429_RELEASE_NAME = "v0.42.9 Business Agent UX Polish & Operation Readiness Freeze"
V0429_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.9_business_agent_ux_polish_restore.md"


class V042BusinessUXMode(StrEnum):
    DEFAULT = "default"
    DEBUG = "debug"
    VERBOSE = "verbose"
    JSON = "json"
    COMPACT = "compact"
    UNKNOWN = "unknown"


class V042BusinessOutputAudience(StrEnum):
    BUSINESS_USER = "business_user"
    OPERATOR = "operator"
    DEVELOPER = "developer"
    PROCESS_INTELLIGENCE_REVIEWER = "process_intelligence_reviewer"
    UNKNOWN = "unknown"


class V042BusinessOutputVerbosity(StrEnum):
    CLEAN = "clean"
    NORMAL = "normal"
    DETAILED = "detailed"
    DEBUG = "debug"
    JSON = "json"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V042BusinessRunRenderPolicy:
    policy_id: str
    default_audience: str
    default_verbosity: str
    show_internal_trace_banner_by_default: bool
    show_provider_untrusted_warning_by_default: bool
    show_run_id_by_default: bool
    show_session_id_by_default: bool
    show_parse_status_by_default: bool
    show_debug_fields_only_with_debug: bool
    preserve_json_output: bool
    preserve_debug_output: bool


@dataclass(frozen=True)
class V042BusinessRunRenderResult:
    result_id: str
    mode: str
    assistant_text: str | None
    rendered_text: str
    run_id: str | None
    session_id: str | None
    debug_fields_hidden: bool
    response_parse_status: str | None
    error_class: str | None
    provider_text_untrusted: bool
    production_certified: bool


@dataclass(frozen=True)
class V042BusinessChatRenderPolicy:
    policy_id: str
    prompt_label: str
    show_provider_in_prompt: bool
    show_turn_count_in_prompt: bool
    show_session_in_banner: bool
    show_provider_in_banner: bool
    group_help_by_purpose: bool
    show_debug_in_default_chat: bool
    provider_text_untrusted_disclosed_in_status: bool
    preserve_debug_commands: bool


@dataclass(frozen=True)
class V042BusinessChatBanner:
    banner_id: str
    title: str
    profile_id: str
    provider_label: str
    session_id: str
    help_hint: str
    exit_hint: str
    rendered_text: str


@dataclass(frozen=True)
class V042BusinessChatHelpView:
    help_id: str
    sections: tuple[dict[str, object], ...]
    rendered_text: str
    includes_developer_jargon: bool
    includes_shell_safety_statement: bool


@dataclass(frozen=True)
class V042BusinessProviderStatusView:
    view_id: str
    status_label: str
    provider_mode_label: str
    model_label: str | None
    endpoint_label: str | None
    mock_provider_available: bool
    configured_provider_ready: bool
    next_action: str
    rendered_text: str
    secrets_visible: bool
    production_certified: bool


@dataclass(frozen=True)
class V042BusinessEmptyResponseView:
    view_id: str
    title: str
    explanation: str
    likely_causes: tuple[str, ...]
    next_actions: tuple[str, ...]
    debug_reference: str
    rendered_text: str
    blames_user: bool
    exposes_raw_trace_by_default: bool


@dataclass(frozen=True)
class V042BusinessCommandGuideItem:
    command: str
    purpose: str


@dataclass(frozen=True)
class V042BusinessCommandGuideSection:
    title: str
    items: tuple[V042BusinessCommandGuideItem, ...]


@dataclass(frozen=True)
class V042BusinessCommandGuide:
    guide_id: str
    sections: tuple[V042BusinessCommandGuideSection, ...]
    rendered_text: str
    includes_core_workflow: bool
    hides_internal_artifact_names: bool
    production_certified: bool


@dataclass(frozen=True)
class V042RuntimeIdentityAnswerPolicy:
    policy_id: str
    runtime_identity: str
    primary_identity_answer: str
    provider_identity_treatment: str
    default_language: str
    business_agent_positioning: str
    base_model_identity_primary_allowed: bool


@dataclass(frozen=True)
class V042UserFacingErrorCard:
    card_id: str
    title: str
    plain_language_summary: str
    likely_causes: tuple[str, ...]
    next_actions: tuple[str, ...]
    debug_command: str
    rendered_text: str
    includes_stack_trace_by_default: bool


@dataclass(frozen=True)
class V042DebugDisclosurePolicy:
    policy_id: str
    debug_flag: str
    verbose_flag: str
    json_flag: str
    internal_fields_hidden_by_default: bool
    internal_fields_available_on_debug: bool
    trace_available_via_trace_commands: bool
    report_available_via_report_bundle: bool


@dataclass(frozen=True)
class V042OperationReadinessCheck:
    check_id: str
    title: str
    status: str
    user_value: str
    failure_mode: str
    verification_command: str


@dataclass(frozen=True)
class V042OperationReadinessReport:
    report_id: str
    checks: tuple[V042OperationReadinessCheck, ...]
    pass_count: int
    warning_count: int
    fail_count: int
    ready_for_v043_pilot: bool
    production_certified: bool


@dataclass(frozen=True)
class V042UXPolishFinding:
    finding_id: str
    area: str
    severity: str
    description: str
    user_impact: str
    fixed_in_v0429: bool
    deferred_to_v04210: bool
    next_action: str


@dataclass(frozen=True)
class V042UXPolishReport:
    report_id: str
    findings: tuple[V042UXPolishFinding, ...]
    fixed_count: int
    deferred_count: int
    ready_for_v043: bool
    recommends_v04210: bool


@dataclass(frozen=True)
class V0429ReadinessReport:
    business_run_output_ready: bool
    business_chat_output_ready: bool
    grouped_help_ready: bool
    command_guide_ready: bool
    provider_status_view_ready: bool
    empty_response_view_ready: bool
    runtime_identity_policy_ready: bool
    debug_disclosure_policy_ready: bool
    operation_readiness_report_ready: bool
    integrated_restore_document_ready: bool
    ready_for_v043_user_operation_pilot: bool
    recommends_v04210_final_polish: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_arbitrary_file_read: bool
    ready_for_broad_filesystem_scan: bool
    ready_for_repo_search: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V04210FinalUXPolishHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    must_not_open: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0429IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0429IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    integrated_doc_path: str


@dataclass(frozen=True)
class V0429IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0429IntegratedRestoreContextSnapshot
    sections: tuple[V0429IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0429IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool


REQUIRED_V0429_DOC_SECTIONS: tuple[str, ...] = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Project Context for New Codex Session",
    "User UX Direction",
    "Business Agent UX Principles",
    "Default vs Debug Output Policy",
    "Run Output Polish",
    "Chat Output Polish",
    "Provider Status Polish",
    "Empty Response User Guidance",
    "Command Guide",
    "Runtime Identity Answer Policy",
    "Operation Readiness Report",
    "UX Polish Findings",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Acceptance Commands",
    "Withdrawal Conditions",
    "v0.42.10 or v0.43 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)

V0429_CLOSED_CAPABILITIES: tuple[str, ...] = (
    "provider_doctor_completion",
    "provider_tool_calling",
    "function_calling",
    "shell_execution",
    "file_edit",
    "patch_apply",
    "arbitrary_file_read",
    "broad_filesystem_scan",
    "repo_search",
    "subagent_invocation",
    "general_agent_loop",
    "multi_step_agent_loop",
    "autonomous_retry_loop",
    "dominion_runtime",
    "production_certification",
)


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_ready(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


def _render_json(value: Any) -> str:
    return json.dumps(_json_ready(value), ensure_ascii=False, indent=2, sort_keys=True)


def _resolve_home(home_path: str | None, command_name: str) -> str:
    resolved = resolve_v042_home(create_v042_home_resolution_request(explicit_home=home_path, command_name=command_name))
    return resolved.home_path if resolved.safe_to_use else ""


def _extract_option(args: Sequence[str], name: str) -> str | None:
    items = list(args)
    if name in items:
        index = items.index(name)
        if index + 1 < len(items):
            return items[index + 1]
    return None


def _strip_debug_flags(args: Sequence[str]) -> tuple[list[str], bool, bool]:
    cleaned: list[str] = []
    debug = False
    verbose = False
    for item in args:
        if item == "--debug":
            debug = True
        elif item == "--verbose":
            verbose = True
        else:
            cleaned.append(item)
    return cleaned, debug, verbose


def _assistant_text_from_legacy_output(text: str) -> str:
    hidden_prefixes = (
        "[v0.41.",
        "profile:",
        "session:",
        "trace runtime",
        "provider text is untrusted",
        "run_id:",
        "session_id:",
        "provider_text_untrusted:",
        "response_parse_status:",
        "error_class:",
        "response_error_class:",
    )
    lines = [line for line in text.splitlines() if not line.strip().startswith(hidden_prefixes)]
    return "\n".join(lines).strip()


def create_v042_business_run_render_policy(**overrides: Any) -> V042BusinessRunRenderPolicy:
    defaults = {
        "policy_id": "v0429-business-run-render-policy",
        "default_audience": V042BusinessOutputAudience.BUSINESS_USER.value,
        "default_verbosity": V042BusinessOutputVerbosity.CLEAN.value,
        "show_internal_trace_banner_by_default": False,
        "show_provider_untrusted_warning_by_default": False,
        "show_run_id_by_default": True,
        "show_session_id_by_default": True,
        "show_parse_status_by_default": False,
        "show_debug_fields_only_with_debug": True,
        "preserve_json_output": True,
        "preserve_debug_output": True,
    }
    return V042BusinessRunRenderPolicy(**_merge(defaults, overrides))


def render_v042_business_run_output(
    assistant_text: str | None = "Mock provider response.",
    run_id: str | None = "run-test",
    session_id: str | None = "session-test",
    mode: str = V042BusinessUXMode.DEFAULT.value,
    response_parse_status: str | None = None,
    error_class: str | None = None,
    trace_event_count: int | None = None,
    provider_text_untrusted: bool = True,
    **overrides: Any,
) -> V042BusinessRunRenderResult:
    policy = create_v042_business_run_render_policy()
    debug = mode in {V042BusinessUXMode.DEBUG.value, V042BusinessUXMode.VERBOSE.value}
    if debug:
        rendered = "\n".join(
            (
                "ChantaCore Run Debug",
                f"run_id: {run_id or '-'}",
                f"session_id: {session_id or '-'}",
                f"response_parse_status: {response_parse_status or '-'}",
                f"response_error_class: {error_class or '-'}",
                f"trace_event_count: {trace_event_count if trace_event_count is not None else '-'}",
                f"provider_text_untrusted: {str(provider_text_untrusted).lower()}",
                "shell_executed: false",
                "subagent_invoked: false",
                "production_certified: false",
                "",
                assistant_text or "",
            )
        )
        hidden = False
    else:
        empty_classes = {"provider_empty_response", "response_parse_empty", "provider_reasoning_without_final"}
        if error_class in empty_classes:
            rendered = create_v042_business_empty_response_view().rendered_text
        elif error_class and error_class != "none":
            lines = [
                "Configured provider run failed.",
                f"error_class: {error_class}",
                "",
                "Next:",
                "- run chanta-cli provider connectivity",
                "- inspect chanta-cli run-report last",
                "- try chanta-cli run --timeout 180",
                "- check local provider/model settings",
                "- try a smaller model",
            ]
            footer = []
            if run_id:
                footer.append(f"run: {run_id}")
            if session_id:
                footer.append(f"session: {session_id}")
            if footer:
                lines.extend(["", *footer])
            rendered = "\n".join(lines)
        else:
            parts = ["ChantaCore", "", assistant_text or ""]
            footer: list[str] = []
            if policy.show_run_id_by_default and run_id:
                footer.append(f"run: {run_id}")
            if policy.show_session_id_by_default and session_id:
                footer.append(f"session: {session_id}")
            if footer:
                parts.extend(["", *footer])
            rendered = "\n".join(parts).strip()
        hidden = True
    defaults = {
        "result_id": "v0429-business-run-render-result",
        "mode": mode,
        "assistant_text": assistant_text,
        "rendered_text": rendered,
        "run_id": run_id,
        "session_id": session_id,
        "debug_fields_hidden": hidden,
        "response_parse_status": response_parse_status,
        "error_class": error_class,
        "provider_text_untrusted": provider_text_untrusted,
        "production_certified": False,
    }
    return V042BusinessRunRenderResult(**_merge(defaults, overrides))


def create_v042_business_chat_render_policy(**overrides: Any) -> V042BusinessChatRenderPolicy:
    defaults = {
        "policy_id": "v0429-business-chat-render-policy",
        "prompt_label": "ChantaCore>",
        "show_provider_in_prompt": False,
        "show_turn_count_in_prompt": False,
        "show_session_in_banner": True,
        "show_provider_in_banner": True,
        "group_help_by_purpose": True,
        "show_debug_in_default_chat": False,
        "provider_text_untrusted_disclosed_in_status": True,
        "preserve_debug_commands": True,
    }
    return V042BusinessChatRenderPolicy(**_merge(defaults, overrides))


def create_v042_business_chat_banner(
    profile_id: str = PROFILE_ID,
    provider_label: str = "mock",
    session_id: str = "session-test",
    **overrides: Any,
) -> V042BusinessChatBanner:
    rendered = "\n".join(
        (
            "ChantaCore Agent",
            f"Profile: {profile_id}",
            f"Provider: {provider_label}",
            f"Session: {session_id}",
            "Type /help for commands. Type /exit to leave.",
        )
    )
    defaults = {
        "banner_id": "v0429-business-chat-banner",
        "title": "ChantaCore Agent",
        "profile_id": profile_id,
        "provider_label": provider_label,
        "session_id": session_id,
        "help_hint": "Type /help for commands.",
        "exit_hint": "Type /exit to leave.",
        "rendered_text": rendered,
    }
    return V042BusinessChatBanner(**_merge(defaults, overrides))


def _help_sections() -> tuple[dict[str, object], ...]:
    return (
        {"title": "Conversation", "commands": ("type any message", "/exit", "/quit")},
        {"title": "Status", "commands": ("/status", "/provider", "/session")},
        {"title": "Review", "commands": ("/history", "/trace", "/run last", "/handoff")},
        {"title": "Safety", "commands": ("/safety",)},
        {"title": "Skills", "commands": ("/skill <skill_id>",)},
    )


def create_v042_business_chat_help_view(**overrides: Any) -> V042BusinessChatHelpView:
    sections = _help_sections()
    lines = ["ChantaCore Help"]
    for section in sections:
        lines.append("")
        lines.append(str(section["title"]))
        lines.extend(f"- {command}" for command in section["commands"])
    lines.append("")
    lines.append("Safety: shell, file edit, subagents, tools, and production certification remain closed.")
    defaults = {
        "help_id": "v0429-business-chat-help",
        "sections": sections,
        "rendered_text": "\n".join(lines),
        "includes_developer_jargon": False,
        "includes_shell_safety_statement": True,
    }
    return V042BusinessChatHelpView(**_merge(defaults, overrides))


def create_v042_business_provider_status_view(
    report: V042ProviderStatusReport | None = None,
    **overrides: Any,
) -> V042BusinessProviderStatusView:
    if report is None:
        report = create_v042_provider_status_report(create_v042_provider_status_request(None))
    if not report.config_present:
        status = "Not configured"
        mode = "not configured"
        next_action = "Run chanta-cli provider setup mock or chanta-cli provider setup local-openai ..."
    elif report.ready_for_configured_provider_run:
        status = "Ready"
        mode = "configured local OpenAI-compatible" if "openai" in str(report.provider_kind) else str(report.mode or "configured")
        next_action = 'Run chanta-cli run --provider configured "..."'
    else:
        status = "Needs attention"
        mode = str(report.mode or report.provider_kind or "configured")
        next_action = report.next_action
    rendered = "\n".join(
        (
            "Provider",
            f"Status: {status}",
            f"Mode: {mode}",
            f"Model: {report.model or '(none)'}",
            f"Endpoint: {report.configured_provider_connectivity}",
            f"Mock provider: {'available' if report.mock_provider_available else 'unavailable'}",
            f"Next: {next_action}",
        )
    )
    defaults = {
        "view_id": "v0429-business-provider-status-view",
        "status_label": status,
        "provider_mode_label": mode,
        "model_label": report.model,
        "endpoint_label": report.configured_provider_connectivity,
        "mock_provider_available": report.mock_provider_available,
        "configured_provider_ready": report.ready_for_configured_provider_run,
        "next_action": next_action,
        "rendered_text": rendered,
        "secrets_visible": False,
        "production_certified": False,
    }
    return V042BusinessProviderStatusView(**_merge(defaults, overrides))


def create_v042_business_empty_response_view(**overrides: Any) -> V042BusinessEmptyResponseView:
    likely = (
        "local model returned reasoning tokens but no final content",
        "LM Studio chat template needs adjustment",
        "max_tokens may be too small",
        "model may need more time or a smaller prompt",
    )
    actions = (
        "try --timeout 180",
        "increase max_tokens if supported",
        "check LM Studio model/template settings",
        "run chanta-cli provider connectivity",
        "inspect chanta-cli run-report last",
    )
    lines = [
        "ChantaCore could not find a final answer in the provider response.",
        "Configured provider returned no final assistant content.",
        "",
        "Likely causes:",
        *[f"- {item}" for item in likely],
        "",
        "Next:",
        *[f"- {item}" for item in actions],
        "",
        "Debug fields are available in chanta-cli run-report last.",
    ]
    defaults = {
        "view_id": "v0429-business-empty-response-view",
        "title": "ChantaCore could not find a final answer in the provider response.",
        "explanation": "The provider call returned no usable final assistant content.",
        "likely_causes": likely,
        "next_actions": actions,
        "debug_reference": "chanta-cli run-report last",
        "rendered_text": "\n".join(lines),
        "blames_user": False,
        "exposes_raw_trace_by_default": False,
    }
    return V042BusinessEmptyResponseView(**_merge(defaults, overrides))


def create_v042_business_command_guide(**overrides: Any) -> V042BusinessCommandGuide:
    sections = (
        V042BusinessCommandGuideSection("Start", (V042BusinessCommandGuideItem("chanta-cli quickstart", "Prepare default-personal runtime."), V042BusinessCommandGuideItem("chanta-cli chat", "Start a work session."))),
        V042BusinessCommandGuideSection("Talk", (V042BusinessCommandGuideItem('chanta-cli run "..."', "Ask one question."), V042BusinessCommandGuideItem("chanta-cli chat", "Continue manually in chat."))),
        V042BusinessCommandGuideSection("Provider", (V042BusinessCommandGuideItem("chanta-cli provider status", "Show provider readiness."), V042BusinessCommandGuideItem("chanta-cli provider connectivity", "Check local model metadata."), V042BusinessCommandGuideItem("chanta-cli provider setup local-openai ...", "Configure local OpenAI-compatible provider."))),
        V042BusinessCommandGuideSection("Review", (V042BusinessCommandGuideItem("chanta-cli trace timeline", "Review recent runtime evidence."), V042BusinessCommandGuideItem("chanta-cli run-report last", "Inspect latest run details."), V042BusinessCommandGuideItem("chanta-cli run show last", "Show latest run process view."), V042BusinessCommandGuideItem("chanta-cli session show last", "Show latest session."))),
        V042BusinessCommandGuideSection("Skills", (V042BusinessCommandGuideItem("chanta-cli skill list", "List bounded skills."), V042BusinessCommandGuideItem("chanta-cli skill run trace_summary", "Run a read-only review skill."))),
        V042BusinessCommandGuideSection("Diagnostics", (V042BusinessCommandGuideItem("chanta-cli report bundle --copy-paste", "Create a support bundle."), V042BusinessCommandGuideItem('chanta-cli feedback note "..."', "Record operator feedback."))),
        V042BusinessCommandGuideSection("Safety", (V042BusinessCommandGuideItem('chanta-cli safety check-command --command "..."', "Check dangerous command text without executing it."),)),
    )
    lines = ["ChantaCore Commands"]
    for section in sections:
        lines.append("")
        lines.append(section.title)
        lines.extend(f"- {item.command} - {item.purpose}" for item in section.items)
    defaults = {
        "guide_id": "v0429-business-command-guide",
        "sections": sections,
        "rendered_text": "\n".join(lines),
        "includes_core_workflow": True,
        "hides_internal_artifact_names": True,
        "production_certified": False,
    }
    return V042BusinessCommandGuide(**_merge(defaults, overrides))


def create_v042_runtime_identity_answer_policy(**overrides: Any) -> V042RuntimeIdentityAnswerPolicy:
    answer = (
        "저는 ChantaCore default-personal runtime에서 동작하는 업무 보조 에이전트입니다. "
        "현재 응답 생성에는 로컬 OpenAI-compatible provider가 사용되고 있으며, provider 모델은 구현 세부사항입니다."
    )
    defaults = {
        "policy_id": "v0429-runtime-identity-answer-policy",
        "runtime_identity": "ChantaCore default-personal runtime",
        "primary_identity_answer": (
            "\uc800\ub294 ChantaCore default-personal runtime\uc5d0\uc11c \ub3d9\uc791\ud558\ub294 "
            "\uc5c5\ubb34 \ubcf4\uc870 \uc5d0\uc774\uc804\ud2b8\uc785\ub2c8\ub2e4. "
            "\ud604\uc7ac \uc751\ub2f5 \uc0dd\uc131\uc5d0\ub294 \ub85c\uceec OpenAI-compatible provider\uac00 "
            "\uc0ac\uc6a9\ub418\uace0 \uc788\uc73c\uba70, provider \ubaa8\ub378\uc740 "
            "\uad6c\ud604 \uc138\ubd80\uc0ac\ud56d\uc785\ub2c8\ub2e4."
        ),
        "provider_identity_treatment": "provider model is implementation detail",
        "default_language": "Korean polite language",
        "business_agent_positioning": "work/business assistant",
        "base_model_identity_primary_allowed": False,
    }
    return V042RuntimeIdentityAnswerPolicy(**_merge(defaults, overrides))


def create_v042_user_facing_error_card(**overrides: Any) -> V042UserFacingErrorCard:
    view = create_v042_business_empty_response_view()
    defaults = {
        "card_id": "v0429-user-facing-error-card",
        "title": view.title,
        "plain_language_summary": view.explanation,
        "likely_causes": view.likely_causes,
        "next_actions": view.next_actions,
        "debug_command": view.debug_reference,
        "rendered_text": view.rendered_text,
        "includes_stack_trace_by_default": False,
    }
    return V042UserFacingErrorCard(**_merge(defaults, overrides))


def create_v042_debug_disclosure_policy(**overrides: Any) -> V042DebugDisclosurePolicy:
    defaults = {
        "policy_id": "v0429-debug-disclosure-policy",
        "debug_flag": "--debug",
        "verbose_flag": "--verbose",
        "json_flag": "--json",
        "internal_fields_hidden_by_default": True,
        "internal_fields_available_on_debug": True,
        "trace_available_via_trace_commands": True,
        "report_available_via_report_bundle": True,
    }
    return V042DebugDisclosurePolicy(**_merge(defaults, overrides))


def create_v042_operation_readiness_check(
    check_id: str,
    title: str,
    status: str = "pass",
    user_value: str = "Ready for operator use.",
    failure_mode: str = "Needs manual verification.",
    verification_command: str = "chanta-cli commands",
    **overrides: Any,
) -> V042OperationReadinessCheck:
    defaults = {
        "check_id": check_id,
        "title": title,
        "status": status,
        "user_value": user_value,
        "failure_mode": failure_mode,
        "verification_command": verification_command,
    }
    return V042OperationReadinessCheck(**_merge(defaults, overrides))


def _readiness_checks() -> tuple[V042OperationReadinessCheck, ...]:
    return (
        create_v042_operation_readiness_check("quickstart", "quickstart works", verification_command="chanta-cli quickstart"),
        create_v042_operation_readiness_check("provider-connectivity", "provider connectivity works", verification_command="chanta-cli provider connectivity"),
        create_v042_operation_readiness_check("configured-run", "configured run handles content or empty response correctly", verification_command='chanta-cli run --provider configured "넌 누구야?"'),
        create_v042_operation_readiness_check("chat-start", "chat starts cleanly", verification_command="chanta-cli chat"),
        create_v042_operation_readiness_check("chat-help", "chat help is grouped", verification_command="/help"),
        create_v042_operation_readiness_check("run-output", "run output is business-friendly", verification_command='chanta-cli run "..."'),
        create_v042_operation_readiness_check("debug-details", "debug details remain available", verification_command='chanta-cli run --debug "..."'),
        create_v042_operation_readiness_check("trace-timeline", "trace timeline available", verification_command="chanta-cli trace timeline"),
        create_v042_operation_readiness_check("report-bundle", "report bundle available", verification_command="chanta-cli report bundle --copy-paste"),
        create_v042_operation_readiness_check("feedback-note", "feedback note available", verification_command='chanta-cli feedback note "..."'),
        create_v042_operation_readiness_check("unsafe-closed", "unsafe capabilities closed", verification_command='chanta-cli safety check-command --command "rm -rf ."'),
    )


def create_v042_operation_readiness_report(**overrides: Any) -> V042OperationReadinessReport:
    checks = _readiness_checks()
    pass_count = sum(1 for check in checks if check.status == "pass")
    warning_count = sum(1 for check in checks if check.status == "warning")
    fail_count = sum(1 for check in checks if check.status == "fail")
    defaults = {
        "report_id": "v0429-operation-readiness-report",
        "checks": checks,
        "pass_count": pass_count,
        "warning_count": warning_count,
        "fail_count": fail_count,
        "ready_for_v043_pilot": fail_count == 0,
        "production_certified": False,
    }
    return V042OperationReadinessReport(**_merge(defaults, overrides))


def create_v042_ux_polish_finding(
    finding_id: str = "run-output",
    area: str = "run_output",
    severity: str = "medium",
    description: str = "Default output exposed raw runtime details.",
    user_impact: str = "Business users saw developer-console text.",
    fixed_in_v0429: bool = True,
    deferred_to_v04210: bool = False,
    next_action: str = "Use clean default renderer; keep debug details behind --debug.",
    **overrides: Any,
) -> V042UXPolishFinding:
    defaults = {
        "finding_id": finding_id,
        "area": area,
        "severity": severity,
        "description": description,
        "user_impact": user_impact,
        "fixed_in_v0429": fixed_in_v0429,
        "deferred_to_v04210": deferred_to_v04210,
        "next_action": next_action,
    }
    return V042UXPolishFinding(**_merge(defaults, overrides))


def create_v042_ux_polish_report(**overrides: Any) -> V042UXPolishReport:
    findings = (
        create_v042_ux_polish_finding("run-output", "run_output"),
        create_v042_ux_polish_finding("chat-output", "chat_output", description="Chat startup and help were too flat.", user_impact="User had to parse internal command lists."),
        create_v042_ux_polish_finding("provider-status", "provider_status", description="Provider status was raw-field oriented.", user_impact="Readiness was harder to see."),
        create_v042_ux_polish_finding("v04210-manual-acceptance", "command_surface", "low", "Final live-provider polish may remain.", "Manual operation may reveal wording rough edges.", False, True, "Use v0.42.10 only if manual acceptance still feels rough."),
    )
    fixed_count = sum(1 for item in findings if item.fixed_in_v0429)
    deferred_count = sum(1 for item in findings if item.deferred_to_v04210)
    defaults = {
        "report_id": "v0429-ux-polish-report",
        "findings": findings,
        "fixed_count": fixed_count,
        "deferred_count": deferred_count,
        "ready_for_v043": deferred_count == 0,
        "recommends_v04210": deferred_count > 0,
    }
    return V042UXPolishReport(**_merge(defaults, overrides))


def create_v0429_readiness_report(**overrides: Any) -> V0429ReadinessReport:
    defaults = {
        "business_run_output_ready": True,
        "business_chat_output_ready": True,
        "grouped_help_ready": True,
        "command_guide_ready": True,
        "provider_status_view_ready": True,
        "empty_response_view_ready": True,
        "runtime_identity_policy_ready": True,
        "debug_disclosure_policy_ready": True,
        "operation_readiness_report_ready": True,
        "integrated_restore_document_ready": True,
        "ready_for_v043_user_operation_pilot": True,
        "recommends_v04210_final_polish": True,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_broad_filesystem_scan": False,
        "ready_for_repo_search": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0429ReadinessReport(**_merge(defaults, overrides))


def create_v04210_final_ux_polish_handoff(**overrides: Any) -> V04210FinalUXPolishHandoff:
    defaults = {
        "handoff_id": "v04210-final-ux-polish-handoff",
        "target_version": "v0.42.10 Final Business UX Acceptance",
        "recommended_focus": (
            "polish any remaining rough default output",
            "finalize start/chat/run command guidance",
            "ensure business-agent language",
            "final manual acceptance checklist",
            "no new high-risk capabilities",
        ),
        "must_not_open": V0429_CLOSED_CAPABILITIES,
        "production_certified": False,
    }
    return V04210FinalUXPolishHandoff(**_merge(defaults, overrides))


def create_v0429_integrated_restore_context_snapshot(**overrides: Any) -> V0429IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0429-integrated-restore-context-snapshot",
        "current_version": V0429_RELEASE_NAME,
        "current_track": V0429_TRACK_NAME,
        "open_capabilities": (
            "clean_default_run_output",
            "clean_default_chat_output",
            "grouped_chat_help",
            "business_provider_status_view",
            "empty_response_user_guidance",
            "command_guide",
            "runtime_identity_answer_policy",
            "debug_disclosure_policy",
            "operation_readiness_report",
            "ux_polish_report",
            "v04210_or_v043_handoff",
            "integrated_restore_document",
        ),
        "closed_capabilities": V0429_CLOSED_CAPABILITIES,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
    }
    return V0429IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0429_integrated_restore_packet(**overrides: Any) -> V0429IntegratedRestorePacket:
    sections = tuple(V0429IntegratedRestoreSection(section.lower().replace(" ", "_").replace("-", "_"), section, True) for section in REQUIRED_V0429_DOC_SECTIONS)
    defaults = {
        "packet_id": "v0429-integrated-restore-packet",
        "context_snapshot": create_v0429_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0429IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0429_integrated_restore_document_manifest(**overrides: Any) -> V0429IntegratedRestoreDocumentManifest:
    path = Path(INTEGRATED_DOC_PATH)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required_present = bool(text) and all(f"## {section}" in text for section in REQUIRED_V0429_DOC_SECTIONS)
    forbidden = [
        Path("docs/versions/v0.42/v0.42.9_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.9_business_ux.md"),
        Path("docs/versions/v0.42/v0.42.9_chat_ux.md"),
        Path("docs/versions/v0.42/v0.42.9_help_text.md"),
    ]
    defaults = {
        "manifest_id": "v0429-integrated-restore-document-manifest",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": any(item.exists() for item in forbidden),
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": required_present,
    }
    return V0429IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _run_report_for_args(args: Sequence[str]) -> LastRunReportResult | None:
    home = _extract_option(args, "--home") or _resolve_home(None, "run-report last")
    if not home:
        return None
    profile = _extract_option(args, "--profile") or PROFILE_ID
    return create_last_run_report(create_last_run_report_request(profile, home))


def _handle_business_run(args: Sequence[str]) -> int:
    if len(args) >= 2 and args[1] in {"show", "history"}:
        return _v0428_main(args)
    if "--json" in args:
        return _v0428_main(args)
    if "--help" in args or "-h" in args:
        parser = argparse.ArgumentParser(prog="chanta-cli run", description="Ask ChantaCore one question.")
        parser.add_argument("--profile", default=PROFILE_ID, help="profile id")
        parser.add_argument("--home", help="ChantaCore home path")
        parser.add_argument("--session", help="session id")
        parser.add_argument("--provider", choices=["mock", "configured"], default=None, help="provider mode")
        parser.add_argument("--timeout", type=float, help="configured provider timeout seconds")
        parser.add_argument("--debug", action="store_true", help="show run/session/trace/provider details")
        parser.add_argument("--verbose", action="store_true", help="show debug-style details")
        parser.add_argument("prompt", nargs="?", help="question or work request")
        parser.print_help()
        return 0
    cleaned, debug, verbose = _strip_debug_flags(args)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        exit_code = _v0428_main(cleaned)
    legacy_output = buffer.getvalue().strip()
    if debug or verbose:
        print(legacy_output)
        report = _run_report_for_args(cleaned)
        if report:
            print("")
            print(render_v042_business_run_output(_assistant_text_from_legacy_output(legacy_output), report.run_id, report.session_id, V042BusinessUXMode.DEBUG.value, report.response_parse_status, report.response_error_class, report.trace_event_count).rendered_text)
        return exit_code
    report = _run_report_for_args(cleaned)
    assistant_text = _assistant_text_from_legacy_output(legacy_output)
    error_class = report.response_error_class if report else None
    if exit_code != 0 and not error_class:
        error_class = "provider_timeout" if "provider_timeout" in assistant_text else "unknown_provider_error"
    if report and report.empty_response_detected:
        error_class = report.response_error_class or "provider_empty_response"
        assistant_text = None
    rendered = render_v042_business_run_output(
        assistant_text,
        report.run_id if report else None,
        report.session_id if report else None,
        V042BusinessUXMode.DEFAULT.value,
        report.response_parse_status if report else None,
        error_class,
        report.trace_event_count if report else None,
    )
    print(rendered.rendered_text)
    return exit_code


def _handle_provider_status(args: Sequence[str]) -> int:
    if "--json" in args:
        return _v0428_main(["provider", "status", *args])
    parser = argparse.ArgumentParser(prog="chanta-cli provider status")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parsed = parser.parse_args(list(args))
    report = create_v042_provider_status_report(create_v042_provider_status_request(parsed.home, parsed.profile))
    print(create_v042_business_provider_status_view(report).rendered_text)
    return 0 if report.resolved_home_path else 1


def _handle_commands(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli commands")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    guide = create_v042_business_command_guide()
    print(_render_json(guide) if parsed.json else guide.rendered_text)
    return 0


def _handle_whoami(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli whoami")
    parser.add_argument("--json", action="store_true")
    parsed = parser.parse_args(list(args))
    policy = create_v042_runtime_identity_answer_policy()
    print(_render_json(policy) if parsed.json else policy.primary_identity_answer)
    return 0


def _handle_status(args: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(prog="chanta-cli status")
    parser.add_argument("--home")
    parser.add_argument("--profile", default=PROFILE_ID)
    parsed = parser.parse_args(list(args))
    provider = create_v042_business_provider_status_view(create_v042_provider_status_report(create_v042_provider_status_request(parsed.home, parsed.profile)))
    readiness = create_v042_operation_readiness_report()
    print("\n".join(("ChantaCore Status", f"Profile: {parsed.profile}", f"Provider: {provider.status_label}", f"Operation readiness: {readiness.pass_count} pass, {readiness.warning_count} warnings, {readiness.fail_count} failures", "Next: chanta-cli commands")))
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0429_VERSION}; {V0429_RELEASE_NAME})")
        return 0
    if args and args[0] == "commands":
        return _handle_commands(args[1:])
    if args and args[0] == "whoami":
        return _handle_whoami(args[1:])
    if args and args[0] == "status":
        return _handle_status(args[1:])
    if args and args[0] == "run":
        return _handle_business_run(args)
    if len(args) >= 2 and args[0] == "provider" and args[1] == "status":
        return _handle_provider_status(args[2:])
    return _v0428_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V042")
    or name.startswith("create_v042")
    or name.startswith("render_v042")
    or name == "main"
]
