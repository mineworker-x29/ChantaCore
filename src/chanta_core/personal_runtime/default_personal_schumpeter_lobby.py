"""v0.43.8 Schumpeter product surface and start lobby.

This module renders a clean start lobby and product/about cards. It does not
open workspace read, repository search, shell or git execution, file mutation,
provider tools/functions, subagents, memory mutation, CLI/package rename, or
production certification.
"""

from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any, Mapping, Sequence


V0438_VERSION = "v0.43.8"
V0438_RELEASE_NAME = "Schumpeter Rebrand Surface & Start Lobby UX"
ANSI_ESCAPE_PATTERN = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")


class V0438ProductBrandName(StrEnum):
    SCHUMPETER = "Schumpeter"
    CHANTACORE = "ChantaCore"


class V0438StartLobbyRenderMode(StrEnum):
    FULL = "full"
    COMPACT = "compact"
    PLAIN = "plain"
    NO_LOGO = "no_logo"
    UNKNOWN = "unknown"


class V0438StatusValue(StrEnum):
    OK = "ok"
    WARN = "warn"
    OFF = "off"
    NONE = "none"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0438ProductBrandPolicy:
    policy_id: str
    product_name: str
    subtitle: str
    default_ui_name: str
    internal_lineage_name: str
    cli_compatibility_name: str
    default_ui_mentions_internal_lineage: bool
    about_may_mention_internal_lineage: bool
    debug_may_mention_internal_lineage: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438RebrandBoundaryPolicy:
    policy_id: str
    ui_rebrand_enabled: bool
    package_rename_allowed: bool
    cli_rename_allowed: bool
    module_rename_allowed: bool
    profile_path_rename_allowed: bool
    trace_path_rename_allowed: bool
    docs_default_to_schumpeter: bool
    compatibility_preserved: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438LegacyNameDeprecationPolicy:
    policy_id: str
    legacy_schumpeter_is_current_runtime: bool
    legacy_schumpeter_default_ui_visible: bool
    legacy_schumpeter_target: str
    chantagrowthkernel_active_dependency: bool
    chantagrowthkernel_default_ui_visible: bool
    migration_note_allowed_in_docs: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438TerminalCapabilityProfile:
    profile_id: str
    width: int
    height: int | None
    supports_unicode: bool
    supports_color: bool
    force_plain: bool
    force_no_logo: bool
    recommended_render_mode: str


@dataclass(frozen=True)
class V0438StartLobbyLayoutPolicy:
    policy_id: str
    center_logo: bool
    show_product_name: bool
    show_subtitle: bool
    show_input_card: bool
    show_profile_provider_mode_row: bool
    show_command_hints: bool
    show_pi_status_bar: bool
    show_debug_metadata_by_default: bool
    show_raw_safety_footer_by_default: bool
    show_internal_lineage_by_default: bool
    min_width_for_full: int
    min_width_for_card: int
    production_certified: bool


@dataclass(frozen=True)
class V0438StartLobbyStatusToken:
    token_id: str
    name: str
    status: str
    icon: str
    plain_label: str
    tooltip: str | None
    detail_command: str | None


@dataclass(frozen=True)
class V0438PIStatusIndicator:
    token: V0438StartLobbyStatusToken


@dataclass(frozen=True)
class V0438ProviderStatusIndicator:
    token: V0438StartLobbyStatusToken


@dataclass(frozen=True)
class V0438TraceStatusIndicator:
    token: V0438StartLobbyStatusToken


@dataclass(frozen=True)
class V0438EvidenceStatusIndicator:
    token: V0438StartLobbyStatusToken


@dataclass(frozen=True)
class V0438SafetyStatusIndicator:
    token: V0438StartLobbyStatusToken


@dataclass(frozen=True)
class V0438StartLobbyStatusBar:
    bar_id: str
    working_directory_label: str | None
    tokens: tuple[V0438StartLobbyStatusToken, ...]
    version_label: str
    rendered_text: str
    contains_raw_debug_metadata: bool
    contains_raw_safety_footer: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438StartLobbyCommandHint:
    hint_id: str
    command: str
    label: str
    visible_on_start: bool


@dataclass(frozen=True)
class V0438StartLobbyCommandGroup:
    group_id: str
    title: str
    commands: tuple[str, ...]
    visible_in_help: bool


@dataclass(frozen=True)
class V0438StartLobbyCard:
    card_id: str
    product_name: str
    subtitle: str
    placeholder: str
    profile_label: str
    provider_label: str
    mode_label: str
    command_hints: tuple[V0438StartLobbyCommandHint, ...]
    status_bar: V0438StartLobbyStatusBar
    rendered_text: str


@dataclass(frozen=True)
class V0438StartLobbyRenderRequest:
    request_id: str
    profile_id: str
    provider_label: str | None
    mode_label: str
    working_directory_label: str | None
    terminal_width: int | None
    force_plain: bool
    force_no_color: bool
    force_no_logo: bool
    debug: bool


@dataclass(frozen=True)
class V0438StartLobbyRenderResult:
    result_id: str
    render_mode: str
    rendered_text: str
    contains_schumpeter_brand: bool
    contains_internal_lineage_default: bool
    contains_chantagrowthkernel: bool
    contains_legacy_schumpeter: bool
    contains_raw_debug_metadata: bool
    contains_raw_safety_footer: bool
    contains_provider_secret: bool
    contains_base_url: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438AboutCardPolicy:
    policy_id: str
    show_product_name: bool
    show_internal_lineage: bool
    show_cli_compatibility: bool
    show_legacy_deprecation_note: bool
    show_chantagrowthkernel_drop_note: bool
    show_raw_debug_metadata: bool
    show_raw_safety_footer: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438AboutCardResult:
    result_id: str
    rendered_text: str
    debug: bool
    contains_schumpeter_brand: bool
    contains_internal_lineage: bool
    contains_legacy_history_default: bool
    contains_chantagrowthkernel_default: bool
    contains_raw_safety_footer: bool
    contains_secret: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438NoisyOutputGuard:
    guard_id: str
    forbidden_default_strings: tuple[str, ...]
    forbidden_brand_leaks: tuple[str, ...]
    forbidden_metadata_leaks: tuple[str, ...]
    applies_to_start_lobby: bool
    applies_to_about_default: bool
    applies_to_status_bar: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438ForbiddenBrandLeakCheck:
    check_id: str
    text: str
    forbidden_found: tuple[str, ...]
    passed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438ForbiddenMetadataLeakCheck:
    check_id: str
    text: str
    forbidden_found: tuple[str, ...]
    passed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438StartLobbyGoldenTranscriptCase:
    case_id: str
    render_mode: str
    width: int | None
    force_plain: bool
    force_no_logo: bool
    expected_contains: tuple[str, ...]
    forbidden_strings: tuple[str, ...]
    production_certified_allowed: bool


@dataclass(frozen=True)
class V0438StartLobbyGoldenTranscriptResult:
    result_id: str
    case: V0438StartLobbyGoldenTranscriptCase
    passed: bool
    rendered_text: str
    missing_expected: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    high_risk_flags_zero: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438V044GateRecheck:
    recheck_id: str
    v0437_golden_transcripts_required: bool
    v0437_golden_transcripts_passed: bool
    start_lobby_clean: bool
    schumpeter_brand_visible: bool
    default_ui_legacy_names_hidden: bool
    default_ui_debug_metadata_hidden: bool
    pi_status_bar_present: bool
    status_detail_available: bool
    high_risk_capabilities_closed: bool
    ready_for_v044_design: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438ReadinessReport:
    report_id: str
    schumpeter_brand_policy_ready: bool
    rebrand_boundary_policy_ready: bool
    start_lobby_renderer_ready: bool
    terminal_layout_fallback_ready: bool
    pi_status_bar_ready: bool
    about_card_ready: bool
    noisy_output_guard_ready: bool
    start_lobby_golden_transcripts_ready: bool
    v044_gate_recheck_ready: bool
    integrated_restore_document_ready: bool
    ready_for_v044_design: bool
    ready_for_workspace_read: bool
    ready_for_arbitrary_file_read: bool
    ready_for_repo_search: bool
    ready_for_workspace_search: bool
    ready_for_git_status_execution: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_autonomous_coding: bool
    ready_for_memory_mutation: bool
    ready_for_core_memory_write: bool
    ready_for_cli_rename: bool
    ready_for_package_rename: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439NamingAuditHandoff:
    handoff_id: str
    target_version: str
    reason: str
    required_checks: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0440ControlledWorkspaceReadDesignHandoff:
    handoff_id: str
    target_version: str
    objective: str
    allowed_scope: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0438IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    product_name: str
    internal_lineage_name: str
    cli_compatibility_name: str
    integrated_doc_path: str
    production_certified: bool


@dataclass(frozen=True)
class V0438IntegratedRestorePacket:
    packet_id: str
    snapshot: V0438IntegratedRestoreContextSnapshot
    required_sections: tuple[str, ...]
    copy_paste_prompt: str
    production_certified: bool


@dataclass(frozen=True)
class V0438IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_brand_doc_allowed: bool
    separate_lobby_doc_allowed: bool
    separate_about_doc_allowed: bool
    separate_docs_created: bool
    required_sections_present: bool
    production_certified: bool


FORBIDDEN_DEFAULT_STRINGS = (
    "ChantaGrowthKernel",
    "GrowthKernel",
    "legacy Schumpeter",
    "ChantaCore legacy core",
    "Closed in this track",
    "safety:",
    "shell=false",
    "subagent=false",
    "workspace_mutated=false",
    "memory_mutated=false",
    "production_certified=false",
    "production_certified=True",
    "grounding:",
    "source:",
    "trace runtime emitted",
    "base_url=",
    "api_key",
    "secret",
)
FORBIDDEN_BRAND_LEAKS = ("ChantaGrowthKernel", "GrowthKernel", "legacy Schumpeter", "ChantaCore legacy core")
FORBIDDEN_METADATA_LEAKS = (
    "safety:",
    "shell=false",
    "subagent=false",
    "workspace_mutated=false",
    "memory_mutated=false",
    "production_certified=false",
    "production_certified=True",
    "grounding:",
    "source:",
    "base_url=",
    "api_key",
    "secret",
)
REQUIRED_V0438_RESTORE_SECTIONS = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "v0.43.7 Baseline Requirement",
    "User Rebrand Decision",
    "Product Naming Policy",
    "Legacy Name Deprecation Policy",
    "Schumpeter Start Lobby Concept",
    "OpenCode-inspired Layout Pattern",
    "Terminal Render Modes",
    "Start Lobby UI Contract",
    "PI Status Bar Contract",
    "Provider/Profile/Mode Display Contract",
    "About Card Contract",
    "Metadata / Safety Disclosure Policy",
    "Golden Start Lobby Acceptance",
    "Forbidden Output Strings",
    "v0.44 Gate Recheck",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Acceptance Commands",
    "Withdrawal Conditions",
    "v0.43.9 or v0.44 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    data = dict(defaults)
    data.update(overrides)
    return data


def _new_id(prefix: str) -> str:
    return f"{prefix}-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def strip_ansi_for_width(text: str) -> str:
    return ANSI_ESCAPE_PATTERN.sub("", str(text))


def display_width(text: str) -> int:
    width = 0
    for char in strip_ansi_for_width(text):
        if char == "\t":
            width += 4
            continue
        category = unicodedata.category(char)
        if category.startswith("C") and char not in {"\n", "\r"}:
            continue
        if unicodedata.combining(char):
            continue
        width += 2 if unicodedata.east_asian_width(char) in {"F", "W"} else 1
    return width


def truncate_to_display_width(text: str, width: int) -> str:
    target = max(0, int(width))
    output: list[str] = []
    used = 0
    for char in strip_ansi_for_width(text):
        char_width = display_width(char)
        if used + char_width > target:
            break
        output.append(char)
        used += char_width
    return "".join(output)


def pad_to_display_width(text: str, width: int) -> str:
    target = max(0, int(width))
    truncated = truncate_to_display_width(text, target)
    return truncated + (" " * max(0, target - display_width(truncated)))


def render_box_line(text: str, width: int) -> str:
    total = max(4, int(width))
    return "│" + pad_to_display_width(text, total - 2) + "│"


def _center(text: str, width: int) -> str:
    target = max(int(width), display_width(text))
    left = max(0, (target - display_width(text)) // 2)
    return (" " * left) + text


def _clean_provider_label(provider_label: str | None) -> str:
    value = (provider_label or "configured").strip().lower()
    if value in {"mock", "test"}:
        return "mock"
    if value in {"qwen", "qwen-local", "qwen local", "local"}:
        return "Qwen Local"
    if value in {"configured", "auto", "configured provider"}:
        return "configured provider"
    if not value or value in {"none", "not configured"}:
        return "provider not configured"
    if "key" in value or "base_url" in value or "http://" in value or "https://" in value:
        return "configured provider"
    return provider_label or "configured provider"


def _short_provider_label(provider_label: str | None) -> str:
    provider = _clean_provider_label(provider_label)
    if "configured provider" in provider:
        return "configured"
    return {
        "configured provider": "configured",
        "provider not configured": "not configured",
        "local provider": "local",
    }.get(provider, truncate_to_display_width(provider, 16))


def _short_mode_label(mode_label: str) -> str:
    return mode_label


def _icon(status: str) -> str:
    return {
        V0438StatusValue.OK.value: "●",
        V0438StatusValue.WARN.value: "◐",
        V0438StatusValue.OFF.value: "○",
        V0438StatusValue.NONE.value: "○",
        V0438StatusValue.UNKNOWN.value: "?",
    }.get(status, "?")


def _plain_label(name: str, status: str) -> str:
    return f"{name}={status}"


def _contains_any(text: str, values: Sequence[str]) -> tuple[str, ...]:
    lowered = text.lower()
    found: list[str] = []
    for value in values:
        if value and value.lower() in lowered:
            found.append(value)
    return tuple(found)


def create_v0438_product_brand_policy(**overrides: Any) -> V0438ProductBrandPolicy:
    defaults = {
        "policy_id": "v0438-product-brand-policy",
        "product_name": "Schumpeter",
        "subtitle": "Process Intelligence-native Work Agent",
        "default_ui_name": "Schumpeter",
        "internal_lineage_name": "ChantaCore",
        "cli_compatibility_name": "chanta-cli",
        "default_ui_mentions_internal_lineage": False,
        "about_may_mention_internal_lineage": True,
        "debug_may_mention_internal_lineage": True,
        "production_certified": False,
    }
    return V0438ProductBrandPolicy(**_merge(defaults, overrides))


def create_v0438_rebrand_boundary_policy(**overrides: Any) -> V0438RebrandBoundaryPolicy:
    defaults = {
        "policy_id": "v0438-rebrand-boundary-policy",
        "ui_rebrand_enabled": True,
        "package_rename_allowed": False,
        "cli_rename_allowed": False,
        "module_rename_allowed": False,
        "profile_path_rename_allowed": False,
        "trace_path_rename_allowed": False,
        "docs_default_to_schumpeter": True,
        "compatibility_preserved": True,
        "production_certified": False,
    }
    return V0438RebrandBoundaryPolicy(**_merge(defaults, overrides))


def create_v0438_legacy_name_deprecation_policy(**overrides: Any) -> V0438LegacyNameDeprecationPolicy:
    defaults = {
        "policy_id": "v0438-legacy-name-deprecation-policy",
        "legacy_schumpeter_is_current_runtime": False,
        "legacy_schumpeter_default_ui_visible": False,
        "legacy_schumpeter_target": "reserved for the stoploss-agent subagent-system lineage",
        "chantagrowthkernel_active_dependency": False,
        "chantagrowthkernel_default_ui_visible": False,
        "migration_note_allowed_in_docs": True,
        "production_certified": False,
    }
    return V0438LegacyNameDeprecationPolicy(**_merge(defaults, overrides))


def create_v0438_terminal_capability_profile(
    width: int = 100,
    height: int | None = None,
    supports_unicode: bool = True,
    supports_color: bool = True,
    force_plain: bool = False,
    force_no_logo: bool = False,
    **overrides: Any,
) -> V0438TerminalCapabilityProfile:
    if force_plain:
        mode = V0438StartLobbyRenderMode.PLAIN.value
    elif force_no_logo:
        mode = V0438StartLobbyRenderMode.NO_LOGO.value
    elif int(width) < 90:
        mode = V0438StartLobbyRenderMode.COMPACT.value
    else:
        mode = V0438StartLobbyRenderMode.FULL.value
    defaults = {
        "profile_id": "v0438-terminal-capability-profile",
        "width": int(width),
        "height": height,
        "supports_unicode": bool(supports_unicode),
        "supports_color": bool(supports_color),
        "force_plain": bool(force_plain),
        "force_no_logo": bool(force_no_logo),
        "recommended_render_mode": mode,
    }
    return V0438TerminalCapabilityProfile(**_merge(defaults, overrides))


def detect_v0438_terminal_capability_profile(
    terminal_width: int | None = None,
    force_plain: bool = False,
    force_no_color: bool = False,
    force_no_logo: bool = False,
    **overrides: Any,
) -> V0438TerminalCapabilityProfile:
    width = int(terminal_width or 100)
    return create_v0438_terminal_capability_profile(
        width=width,
        supports_unicode=not force_plain,
        supports_color=not force_no_color and not force_plain,
        force_plain=force_plain,
        force_no_logo=force_no_logo,
        **overrides,
    )


def create_v0438_start_lobby_layout_policy(**overrides: Any) -> V0438StartLobbyLayoutPolicy:
    defaults = {
        "policy_id": "v0438-start-lobby-layout-policy",
        "center_logo": True,
        "show_product_name": True,
        "show_subtitle": True,
        "show_input_card": True,
        "show_profile_provider_mode_row": True,
        "show_command_hints": True,
        "show_pi_status_bar": True,
        "show_debug_metadata_by_default": False,
        "show_raw_safety_footer_by_default": False,
        "show_internal_lineage_by_default": False,
        "min_width_for_full": 90,
        "min_width_for_card": 70,
        "production_certified": False,
    }
    return V0438StartLobbyLayoutPolicy(**_merge(defaults, overrides))


def create_v0438_status_indicator(
    name: str,
    status: str = V0438StatusValue.OK.value,
    tooltip: str | None = None,
    detail_command: str | None = "/status",
    **overrides: Any,
) -> V0438StartLobbyStatusToken:
    defaults = {
        "token_id": f"v0438-status-{name.lower()}",
        "name": name,
        "status": status,
        "icon": _icon(status),
        "plain_label": _plain_label(name, status),
        "tooltip": tooltip,
        "detail_command": detail_command,
    }
    return V0438StartLobbyStatusToken(**_merge(defaults, overrides))


def create_v0438_pi_status_indicator(status: str = "ok", **overrides: Any) -> V0438PIStatusIndicator:
    return V0438PIStatusIndicator(create_v0438_status_indicator("PI", status, "Process Intelligence evidence surface", "/status", **overrides))


def create_v0438_provider_status_indicator(status: str = "ok", **overrides: Any) -> V0438ProviderStatusIndicator:
    return V0438ProviderStatusIndicator(create_v0438_status_indicator("Provider", status, "Provider setup summary", "/provider", **overrides))


def create_v0438_trace_status_indicator(status: str = "ok", **overrides: Any) -> V0438TraceStatusIndicator:
    return V0438TraceStatusIndicator(create_v0438_status_indicator("Trace", status, "Trace and run report availability", "/what-happened", **overrides))


def create_v0438_evidence_status_indicator(status: str = "none", **overrides: Any) -> V0438EvidenceStatusIndicator:
    return V0438EvidenceStatusIndicator(create_v0438_status_indicator("Evidence", status, "Active evidence pack state", "/evidence last", **overrides))


def create_v0438_safety_status_indicator(status: str = "ok", **overrides: Any) -> V0438SafetyStatusIndicator:
    return V0438SafetyStatusIndicator(create_v0438_status_indicator("Safety", status, "Closed high-risk capability summary", "/status", **overrides))


def _default_tokens() -> tuple[V0438StartLobbyStatusToken, ...]:
    return (
        create_v0438_pi_status_indicator().token,
        create_v0438_provider_status_indicator().token,
        create_v0438_trace_status_indicator().token,
        create_v0438_evidence_status_indicator().token,
        create_v0438_safety_status_indicator().token,
    )


def create_v0438_start_lobby_status_bar(
    working_directory_label: str | None = None,
    tokens: Sequence[V0438StartLobbyStatusToken] | None = None,
    version_label: str = V0438_VERSION,
    plain: bool = False,
    **overrides: Any,
) -> V0438StartLobbyStatusBar:
    token_tuple = tuple(tokens or _default_tokens())
    if plain:
        status = " ".join(token.plain_label for token in token_tuple)
        rendered = f"{status} {version_label}"
    else:
        status = "  ".join(f"{token.icon} {token.name}" for token in token_tuple)
        prefix = f"{working_directory_label}   " if working_directory_label else ""
        rendered = f"{prefix}{status}   {version_label}"
    defaults = {
        "bar_id": _new_id("v0438-start-lobby-status-bar"),
        "working_directory_label": working_directory_label,
        "tokens": token_tuple,
        "version_label": version_label,
        "rendered_text": rendered,
        "contains_raw_debug_metadata": False,
        "contains_raw_safety_footer": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    return V0438StartLobbyStatusBar(**_merge(defaults, overrides))


def create_v0438_start_lobby_command_hint(command: str = "/help", label: str = "commands", visible_on_start: bool = True, **overrides: Any) -> V0438StartLobbyCommandHint:
    defaults = {
        "hint_id": f"v0438-command-hint-{command.strip('/').replace(' ', '-')}",
        "command": command,
        "label": label,
        "visible_on_start": bool(visible_on_start),
    }
    return V0438StartLobbyCommandHint(**_merge(defaults, overrides))


def create_v0438_start_lobby_command_group(title: str = "Workflows", commands: Sequence[str] = ("/summary", "/todo", "/memo"), **overrides: Any) -> V0438StartLobbyCommandGroup:
    defaults = {
        "group_id": f"v0438-command-group-{title.lower().replace(' ', '-')}",
        "title": title,
        "commands": tuple(commands),
        "visible_in_help": True,
    }
    return V0438StartLobbyCommandGroup(**_merge(defaults, overrides))


def _default_hints() -> tuple[V0438StartLobbyCommandHint, ...]:
    return (
        create_v0438_start_lobby_command_hint("/help", "commands"),
        create_v0438_start_lobby_command_hint("/status", "status"),
        create_v0438_start_lobby_command_hint("/exit", "exit"),
    )


def create_v0438_start_lobby_render_request(
    profile_id: str = "default-personal",
    provider_label: str | None = None,
    mode_label: str = "Business Work Session",
    working_directory_label: str | None = None,
    terminal_width: int | None = None,
    force_plain: bool = False,
    force_no_color: bool = False,
    force_no_logo: bool = False,
    debug: bool = False,
    **overrides: Any,
) -> V0438StartLobbyRenderRequest:
    defaults = {
        "request_id": _new_id("v0438-start-lobby-render-request"),
        "profile_id": profile_id,
        "provider_label": provider_label,
        "mode_label": mode_label,
        "working_directory_label": working_directory_label,
        "terminal_width": terminal_width,
        "force_plain": bool(force_plain),
        "force_no_color": bool(force_no_color),
        "force_no_logo": bool(force_no_logo),
        "debug": bool(debug),
    }
    return V0438StartLobbyRenderRequest(**_merge(defaults, overrides))


def _command_hint_text(hints: Sequence[V0438StartLobbyCommandHint], separator: str = "     ") -> str:
    return separator.join(hint.command if hint.label in {"status", "exit"} else f"{hint.command} {hint.label}" for hint in hints if hint.visible_on_start)


def create_v0438_start_lobby_card(
    profile_label: str = "default-personal",
    provider_label: str = "configured provider",
    mode_label: str = "Business Work Session",
    status_bar: V0438StartLobbyStatusBar | None = None,
    **overrides: Any,
) -> V0438StartLobbyCard:
    brand = create_v0438_product_brand_policy()
    hints = _default_hints()
    status = status_bar or create_v0438_start_lobby_status_bar()
    rendered = "\n".join(
        (
            brand.product_name,
            brand.subtitle,
            "Ask anything...",
            '"오늘 작업을 요약해줘"',
            f"{profile_label} | {provider_label} | {mode_label}",
            _command_hint_text(hints),
            status.rendered_text,
        )
    )
    defaults = {
        "card_id": _new_id("v0438-start-lobby-card"),
        "product_name": brand.product_name,
        "subtitle": brand.subtitle,
        "placeholder": 'Ask anything...\n"오늘 작업을 요약해줘"',
        "profile_label": profile_label,
        "provider_label": provider_label,
        "mode_label": mode_label,
        "command_hints": hints,
        "status_bar": status,
        "rendered_text": rendered,
    }
    return V0438StartLobbyCard(**_merge(defaults, overrides))


def render_v0438_start_lobby_plain(request: V0438StartLobbyRenderRequest) -> str:
    provider = _short_provider_label(request.provider_label)
    status = create_v0438_start_lobby_status_bar(request.working_directory_label, plain=True).rendered_text
    return "\n".join(
        (
            "Schumpeter",
            "Process Intelligence-native Work Agent",
            "",
            "Ask anything...",
            '"오늘 작업을 요약해줘"',
            "",
            f"{request.profile_id} | {provider} | {request.mode_label}",
            "",
            "/help commands | /status | /exit",
            "",
            status,
        )
    )


def render_v0438_start_lobby_compact(request: V0438StartLobbyRenderRequest) -> str:
    provider = _short_provider_label(request.provider_label)
    status = create_v0438_start_lobby_status_bar(request.working_directory_label, plain=True).rendered_text
    return "\n".join(
        (
            "Schumpeter",
            "PI-native Work Agent",
            "",
            "Ask anything...",
            '"오늘 작업을 요약해줘"',
            "",
            f"Profile: {request.profile_id}",
            f"Provider: {provider}",
            f"Mode: {_short_mode_label(request.mode_label)}",
            "",
            "/help commands   /status   /exit",
            status.replace(" ", " | "),
        )
    )


def render_v0438_start_lobby_no_logo(request: V0438StartLobbyRenderRequest) -> str:
    provider = _short_provider_label(request.provider_label)
    status = create_v0438_start_lobby_status_bar(request.working_directory_label, plain=True).rendered_text
    return "\n".join(
        (
            "Schumpeter",
            "Ask anything...",
            '"오늘 작업을 요약해줘"',
            f"{request.profile_id} | {provider} | {_short_mode_label(request.mode_label)}",
            "/help commands   /status   /exit",
            status,
        )
    )


def _render_full_lobby(request: V0438StartLobbyRenderRequest) -> str:
    width = max(90, min(int(request.terminal_width or 100), 140))
    provider = _short_provider_label(request.provider_label)
    title = _center("Schumpeter", width)
    subtitle = _center("Process Intelligence-native Work Agent", width)
    card_width = min(64, max(52, width - 24))
    left = max(0, (width - card_width) // 2)
    pad = " " * left
    row = f"{request.profile_id}   {provider}   {_short_mode_label(request.mode_label)}"
    korean_placeholder = '  "오늘 작업을 요약해줘"'
    box = "\n".join(
        (
            f"{pad}╭" + "─" * (card_width - 2) + "╮",
            f"{pad}{render_box_line('  Ask anything...', card_width)}",
            f"{pad}{render_box_line(korean_placeholder, card_width)}",
            f"{pad}{render_box_line('', card_width)}",
            f"{pad}{render_box_line('  ' + row, card_width)}",
            f"{pad}╰" + "─" * (card_width - 2) + "╯",
        )
    )
    hints = _center("/help commands     /status     /exit", width)
    status_bar = create_v0438_start_lobby_status_bar(request.working_directory_label).rendered_text
    return "\n".join((title, "", subtitle, "", "", box, "", hints, "", "", status_bar))


def create_v0438_start_lobby_render_result(render_mode: str, rendered_text: str, **overrides: Any) -> V0438StartLobbyRenderResult:
    brand_leaks = check_v0438_forbidden_brand_leaks(rendered_text).forbidden_found
    metadata_leaks = check_v0438_forbidden_metadata_leaks(rendered_text).forbidden_found
    defaults = {
        "result_id": _new_id("v0438-start-lobby-render-result"),
        "render_mode": render_mode,
        "rendered_text": rendered_text,
        "contains_schumpeter_brand": "Schumpeter" in rendered_text,
        "contains_internal_lineage_default": "Internal implementation lineage" in rendered_text or "internal implementation lineage" in rendered_text,
        "contains_chantagrowthkernel": "ChantaGrowthKernel" in rendered_text or "GrowthKernel" in rendered_text,
        "contains_legacy_schumpeter": "legacy Schumpeter" in rendered_text,
        "contains_raw_debug_metadata": bool(metadata_leaks),
        "contains_raw_safety_footer": "safety:" in rendered_text,
        "contains_provider_secret": "api_key" in rendered_text.lower() or "secret" in rendered_text.lower(),
        "contains_base_url": "base_url=" in rendered_text.lower(),
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    merged = _merge(defaults, overrides)
    if brand_leaks:
        merged["contains_chantagrowthkernel"] = any(item in {"ChantaGrowthKernel", "GrowthKernel"} for item in brand_leaks)
        merged["contains_legacy_schumpeter"] = "legacy Schumpeter" in brand_leaks
    return V0438StartLobbyRenderResult(**merged)


def render_v0438_start_lobby(
    request: V0438StartLobbyRenderRequest | None = None,
    width: int | None = None,
    force_plain: bool = False,
    force_no_logo: bool = False,
    **overrides: Any,
) -> V0438StartLobbyRenderResult:
    request = request or create_v0438_start_lobby_render_request(terminal_width=width, force_plain=force_plain, force_no_logo=force_no_logo, **overrides)
    profile = detect_v0438_terminal_capability_profile(request.terminal_width, request.force_plain, request.force_no_color, request.force_no_logo)
    mode = profile.recommended_render_mode
    if mode == V0438StartLobbyRenderMode.PLAIN.value:
        text = render_v0438_start_lobby_plain(request)
    elif mode == V0438StartLobbyRenderMode.COMPACT.value:
        text = render_v0438_start_lobby_compact(request)
    elif mode == V0438StartLobbyRenderMode.NO_LOGO.value:
        text = render_v0438_start_lobby_no_logo(request)
    else:
        text = _render_full_lobby(request)
    return create_v0438_start_lobby_render_result(mode, text)


def create_v0438_about_card_policy(debug: bool = False, migration_history: bool = False, **overrides: Any) -> V0438AboutCardPolicy:
    defaults = {
        "policy_id": "v0438-about-card-policy",
        "show_product_name": True,
        "show_internal_lineage": True,
        "show_cli_compatibility": True,
        "show_legacy_deprecation_note": bool(debug and migration_history),
        "show_chantagrowthkernel_drop_note": bool(debug and migration_history),
        "show_raw_debug_metadata": bool(debug),
        "show_raw_safety_footer": False,
        "production_certified": False,
    }
    return V0438AboutCardPolicy(**_merge(defaults, overrides))


def render_v0438_about_card(debug: bool = False, migration_history: bool = False, **overrides: Any) -> V0438AboutCardResult:
    policy = create_v0438_about_card_policy(debug=debug, migration_history=migration_history)
    lines = [
        "Schumpeter",
        "",
        "Schumpeter is a Process Intelligence-native Work Agent.",
        "",
        "Product surface:",
        "- name: Schumpeter",
        "- mode: Business Work Session",
        "",
        "Runtime lineage:",
        "- internal implementation lineage: ChantaCore",
        "- CLI compatibility: chanta-cli",
        "",
        "Current boundary:",
        "- workspace read: not open yet",
        "- repo search: not open yet",
        "- shell/edit/apply: not open",
    ]
    if debug:
        lines.extend(
            (
                "",
                "Debug:",
                f"- version: {V0438_VERSION}",
                "- package/module lineage: chanta_core.personal_runtime",
                "- profile path compatibility: unchanged",
                "- trace path compatibility: unchanged",
            )
        )
    if policy.show_legacy_deprecation_note:
        lines.append("- deprecated legacy Schumpeter concept: reserved for stoploss-agent subagent-system lineage")
    if policy.show_chantagrowthkernel_drop_note:
        lines.append("- ChantaGrowthKernel: dropped, not an active dependency")
    text = "\n".join(lines)
    defaults = {
        "result_id": _new_id("v0438-about-card-result"),
        "rendered_text": text,
        "debug": bool(debug),
        "contains_schumpeter_brand": "Schumpeter" in text,
        "contains_internal_lineage": "ChantaCore" in text,
        "contains_legacy_history_default": (not debug) and "legacy Schumpeter" in text,
        "contains_chantagrowthkernel_default": (not debug) and "ChantaGrowthKernel" in text,
        "contains_raw_safety_footer": "safety:" in text,
        "contains_secret": "secret" in text.lower() or "api_key" in text.lower(),
        "production_certified": False,
    }
    return V0438AboutCardResult(**_merge(defaults, overrides))


def render_v0438_about_card_debug(**overrides: Any) -> V0438AboutCardResult:
    return render_v0438_about_card(debug=True, **overrides)


def create_v0438_noisy_output_guard(**overrides: Any) -> V0438NoisyOutputGuard:
    defaults = {
        "guard_id": "v0438-noisy-output-guard",
        "forbidden_default_strings": FORBIDDEN_DEFAULT_STRINGS,
        "forbidden_brand_leaks": FORBIDDEN_BRAND_LEAKS,
        "forbidden_metadata_leaks": FORBIDDEN_METADATA_LEAKS,
        "applies_to_start_lobby": True,
        "applies_to_about_default": True,
        "applies_to_status_bar": True,
        "production_certified": False,
    }
    return V0438NoisyOutputGuard(**_merge(defaults, overrides))


def check_v0438_forbidden_brand_leaks(text: str, **overrides: Any) -> V0438ForbiddenBrandLeakCheck:
    found = _contains_any(text, FORBIDDEN_BRAND_LEAKS)
    defaults = {
        "check_id": _new_id("v0438-forbidden-brand-leak-check"),
        "text": text,
        "forbidden_found": found,
        "passed": not found,
        "production_certified": False,
    }
    return V0438ForbiddenBrandLeakCheck(**_merge(defaults, overrides))


def check_v0438_forbidden_metadata_leaks(text: str, **overrides: Any) -> V0438ForbiddenMetadataLeakCheck:
    found = _contains_any(text, FORBIDDEN_METADATA_LEAKS)
    defaults = {
        "check_id": _new_id("v0438-forbidden-metadata-leak-check"),
        "text": text,
        "forbidden_found": found,
        "passed": not found,
        "production_certified": False,
    }
    return V0438ForbiddenMetadataLeakCheck(**_merge(defaults, overrides))


def create_v0438_start_lobby_golden_transcript_case(
    case_id: str = "default-full",
    render_mode: str = V0438StartLobbyRenderMode.FULL.value,
    width: int | None = 120,
    force_plain: bool = False,
    force_no_logo: bool = False,
    expected_contains: Sequence[str] = ("Schumpeter", "Ask anything", "/help", "/status", "/exit"),
    forbidden_strings: Sequence[str] = FORBIDDEN_DEFAULT_STRINGS,
    production_certified_allowed: bool = False,
    **overrides: Any,
) -> V0438StartLobbyGoldenTranscriptCase:
    defaults = {
        "case_id": case_id,
        "render_mode": render_mode,
        "width": width,
        "force_plain": bool(force_plain),
        "force_no_logo": bool(force_no_logo),
        "expected_contains": tuple(expected_contains),
        "forbidden_strings": tuple(forbidden_strings),
        "production_certified_allowed": bool(production_certified_allowed),
    }
    return V0438StartLobbyGoldenTranscriptCase(**_merge(defaults, overrides))


def create_v0438_start_lobby_golden_transcript_result(
    case: V0438StartLobbyGoldenTranscriptCase,
    result: V0438StartLobbyRenderResult,
    **overrides: Any,
) -> V0438StartLobbyGoldenTranscriptResult:
    missing = tuple(item for item in case.expected_contains if item not in result.rendered_text)
    forbidden = tuple(item for item in case.forbidden_strings if item and item in result.rendered_text)
    high_risk_zero = not (
        result.provider_invoked
        or result.prompt_submitted
        or result.shell_executed
        or result.repo_search_used
        or result.workspace_read_opened
        or result.memory_mutated
        or result.core_memory_written
    )
    passed = not missing and not forbidden and high_risk_zero and not result.production_certified
    defaults = {
        "result_id": _new_id("v0438-start-lobby-golden-transcript-result"),
        "case": case,
        "passed": passed,
        "rendered_text": result.rendered_text,
        "missing_expected": missing,
        "forbidden_found": forbidden,
        "high_risk_flags_zero": high_risk_zero,
        "production_certified": False,
    }
    return V0438StartLobbyGoldenTranscriptResult(**_merge(defaults, overrides))


def execute_v0438_start_lobby_golden_transcript_case(case: V0438StartLobbyGoldenTranscriptCase, **overrides: Any) -> V0438StartLobbyGoldenTranscriptResult:
    result = render_v0438_start_lobby(width=case.width, force_plain=case.force_plain, force_no_logo=case.force_no_logo)
    return create_v0438_start_lobby_golden_transcript_result(case, result, **overrides)


def create_v0438_v044_gate_recheck(**overrides: Any) -> V0438V044GateRecheck:
    defaults = {
        "recheck_id": _new_id("v0438-v044-gate-recheck"),
        "v0437_golden_transcripts_required": True,
        "v0437_golden_transcripts_passed": True,
        "start_lobby_clean": True,
        "schumpeter_brand_visible": True,
        "default_ui_legacy_names_hidden": True,
        "default_ui_debug_metadata_hidden": True,
        "pi_status_bar_present": True,
        "status_detail_available": True,
        "high_risk_capabilities_closed": True,
        "ready_for_v044_design": True,
        "production_certified": False,
    }
    data = _merge(defaults, overrides)
    ready = all(
        (
            data["v0437_golden_transcripts_passed"],
            data["start_lobby_clean"],
            data["schumpeter_brand_visible"],
            data["default_ui_legacy_names_hidden"],
            data["default_ui_debug_metadata_hidden"],
            data["pi_status_bar_present"],
            data["status_detail_available"],
            data["high_risk_capabilities_closed"],
        )
    )
    data["ready_for_v044_design"] = ready
    return V0438V044GateRecheck(**data)


def create_v0438_readiness_report(**overrides: Any) -> V0438ReadinessReport:
    gate = create_v0438_v044_gate_recheck()
    defaults = {
        "report_id": _new_id("v0438-readiness-report"),
        "schumpeter_brand_policy_ready": True,
        "rebrand_boundary_policy_ready": True,
        "start_lobby_renderer_ready": True,
        "terminal_layout_fallback_ready": True,
        "pi_status_bar_ready": True,
        "about_card_ready": True,
        "noisy_output_guard_ready": True,
        "start_lobby_golden_transcripts_ready": True,
        "v044_gate_recheck_ready": True,
        "integrated_restore_document_ready": True,
        "ready_for_v044_design": gate.ready_for_v044_design,
        "ready_for_workspace_read": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_repo_search": False,
        "ready_for_workspace_search": False,
        "ready_for_git_status_execution": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_autonomous_coding": False,
        "ready_for_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "ready_for_cli_rename": False,
        "ready_for_package_rename": False,
        "production_certified": False,
    }
    return V0438ReadinessReport(**_merge(defaults, overrides))


def create_v0439_naming_audit_handoff(**overrides: Any) -> V0439NamingAuditHandoff:
    defaults = {
        "handoff_id": "v0439-naming-audit-handoff",
        "target_version": "v0.43.9 Naming Audit",
        "reason": "Use if more old naming leaks are found after the Schumpeter surface patch.",
        "required_checks": ("default UI naming", "docs naming", "about/debug lineage", "legacy/dropped name leaks"),
        "production_certified": False,
    }
    return V0439NamingAuditHandoff(**_merge(defaults, overrides))


def create_v0440_controlled_workspace_read_design_handoff(**overrides: Any) -> V0440ControlledWorkspaceReadDesignHandoff:
    defaults = {
        "handoff_id": "v0440-controlled-workspace-read-design-handoff",
        "target_version": "v0.44.0 Controlled Workspace Read Design & Scope Contract",
        "objective": "Design the read-only workspace scope contract after v0.43.7 and v0.43.8 UX gates pass.",
        "allowed_scope": ("design", "spec", "scope contract", "safety gates", "risk register", "tests"),
        "closed_capabilities": ("workspace read implementation", "repo search", "shell", "edit/apply", "subagents", "production certification"),
        "production_certified": False,
    }
    return V0440ControlledWorkspaceReadDesignHandoff(**_merge(defaults, overrides))


def create_v0438_integrated_restore_context_snapshot(**overrides: Any) -> V0438IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0438-integrated-restore-context",
        "current_version": V0438_VERSION,
        "product_name": "Schumpeter",
        "internal_lineage_name": "ChantaCore",
        "cli_compatibility_name": "chanta-cli",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.8_schumpeter_rebrand_start_lobby_restore.md",
        "production_certified": False,
    }
    return V0438IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0438_integrated_restore_packet(**overrides: Any) -> V0438IntegratedRestorePacket:
    defaults = {
        "packet_id": "v0438-integrated-restore-packet",
        "snapshot": create_v0438_integrated_restore_context_snapshot(),
        "required_sections": REQUIRED_V0438_RESTORE_SECTIONS,
        "copy_paste_prompt": "Restore Schumpeter v0.43.8 start lobby and keep v0.43.7 golden transcript rules intact.",
        "production_certified": False,
    }
    return V0438IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0438_integrated_restore_document_manifest(**overrides: Any) -> V0438IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "v0438-integrated-restore-document-manifest",
        "integrated_doc_path": "docs/versions/v0.43/v0.43.8_schumpeter_rebrand_start_lobby_restore.md",
        "integrated_doc_required": True,
        "separate_brand_doc_allowed": False,
        "separate_lobby_doc_allowed": False,
        "separate_about_doc_allowed": False,
        "separate_docs_created": False,
        "required_sections_present": True,
        "production_certified": False,
    }
    return V0438IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def render_v0438_status_detail() -> str:
    return "\n".join(
        (
            "Schumpeter status",
            "",
            "PI: ok - process evidence surfaces are available.",
            "Provider: ok - provider configuration status surface is available.",
            "Trace: ok - trace/run-report surfaces remain available.",
            "Evidence: none - no active evidence pack is required for the lobby.",
            "Safety: ok - workspace read, repo search, shell, edit/apply, subagents, memory mutation, and production certification remain closed.",
        )
    )


__all__ = [
    name
    for name in globals()
    if name.startswith("V0438")
    or name.startswith("V0439")
    or name.startswith("V0440")
    or name.startswith("create_v0438")
    or name.startswith("create_v0439")
    or name.startswith("create_v0440")
    or name.startswith("render_v0438")
    or name.startswith("detect_v0438")
    or name.startswith("check_v0438")
    or name.startswith("execute_v0438")
    or name
    in {
        "FORBIDDEN_DEFAULT_STRINGS",
        "REQUIRED_V0438_RESTORE_SECTIONS",
        "strip_ansi_for_width",
        "display_width",
        "pad_to_display_width",
        "truncate_to_display_width",
        "render_box_line",
    }
]
