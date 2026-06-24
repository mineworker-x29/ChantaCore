"""v0.43.8.2 slash command palette for the Schumpeter start session.

This module is a user-interface registry and completion surface only. It does
not execute commands, inspect repositories, call providers, or mutate memory.
"""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable, Sequence


V0438_COMMAND_PALETTE_VERSION = "v0.43.8.2"
V0438_COMMAND_PALETTE_RELEASE_NAME = "Slash Command Palette & Interactive Command Completion UX"


class V0438SlashCommandCategory(StrEnum):
    WORKFLOWS = "workflows"
    ARTIFACTS = "artifacts"
    NOTES = "notes"
    EVIDENCE = "evidence"
    GROUNDED_WORKFLOWS = "grounded_workflows"
    PILOT_RELEASE = "pilot_release"
    SYSTEM = "system"
    UNKNOWN = "unknown"


class V0438SlashCommandPaletteRenderMode(StrEnum):
    INTERACTIVE = "interactive"
    PLAIN = "plain"
    FALLBACK = "fallback"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0438SlashCommandSpec:
    command: str
    category: str
    description_ko: str
    usage_hint: str | None
    primary: bool
    read_only_registry_entry: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438SlashCommandRegistry:
    registry_id: str
    commands: tuple[V0438SlashCommandSpec, ...]
    deterministic: bool
    read_only: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438SlashCommandPalettePolicy:
    policy_id: str
    opens_on_slash: bool
    filters_as_user_types: bool
    inserts_without_execution: bool
    grouped_by_category: bool
    korean_descriptions: bool
    raw_metadata_hidden: bool
    plain_fallback_available: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438SlashCommandPaletteRequest:
    request_id: str
    prefix: str
    render_mode: str
    plain: bool
    max_items: int | None
    production_certified: bool


@dataclass(frozen=True)
class V0438SlashCommandPaletteResult:
    result_id: str
    request: V0438SlashCommandPaletteRequest
    commands: tuple[V0438SlashCommandSpec, ...]
    rendered_text: str
    grouped: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438SlashCommandCompletionItem:
    command: str
    insert_text: str
    display_text: str
    description_ko: str
    category: str
    executes_command: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438SlashCommandCompletionResult:
    result_id: str
    prefix: str
    items: tuple[V0438SlashCommandCompletionItem, ...]
    command_executed: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438InteractiveInputPolicy:
    policy_id: str
    prompt_toolkit_preferred: bool
    prompt_toolkit_optional: bool
    plain_mode_disables_interactive_palette: bool
    fallback_on_import_error: bool
    completion_executes_commands: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438PromptToolkitAvailability:
    availability_id: str
    available: bool
    import_name: str
    safe_optional_dependency: bool
    error: str | None
    production_certified: bool


@dataclass(frozen=True)
class V0438PlainInputFallbackPolicy:
    policy_id: str
    slash_enter_shows_palette: bool
    help_commands_shows_palette: bool
    plain_mode_supported: bool
    interactive_completion_required: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438CommandPaletteNoisyOutputGuard:
    guard_id: str
    forbidden_strings: tuple[str, ...]
    passed: bool
    forbidden_found: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V0438CommandPaletteSafetyReport:
    report_id: str
    command_palette_opened: bool
    provider_invocation_allowed: bool
    prompt_submission_allowed: bool
    shell_execution_allowed: bool
    git_execution_allowed: bool
    repo_search_allowed: bool
    workspace_read_allowed: bool
    file_edit_allowed: bool
    patch_apply_allowed: bool
    provider_tool_calling_allowed: bool
    function_calling_allowed: bool
    subagent_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438CommandPaletteReadinessReport:
    report_id: str
    command_registry_ready: bool
    grouped_palette_ready: bool
    completion_ready: bool
    plain_fallback_ready: bool
    start_lobby_hint_ready: bool
    safety_report_ready: bool
    ready_for_workspace_read: bool
    ready_for_repo_search: bool
    ready_for_shell_execution: bool
    ready_for_git_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_memory_mutation: bool
    ready_for_core_memory_write: bool
    production_certified: bool


@dataclass(frozen=True)
class V0438CommandPaletteGoldenCase:
    case_id: str
    prefix: str
    expected_commands: tuple[str, ...]
    forbidden_strings: tuple[str, ...]
    production_certified_allowed: bool


@dataclass(frozen=True)
class V0438CommandPaletteGoldenResult:
    result_id: str
    case: V0438CommandPaletteGoldenCase
    passed: bool
    rendered_text: str
    missing_expected: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    high_risk_flags_zero: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439OrV044Handoff:
    handoff_id: str
    recommendation: str
    reason: str
    required_before_next_track: tuple[str, ...]
    production_certified: bool


FORBIDDEN_PALETTE_STRINGS = (
    "safety:",
    "shell=false",
    "production_certified=false",
    "production_certified=True",
    "grounding:",
    "source:",
    "ChantaGrowthKernel",
    "legacy Schumpeter",
    "base_url=",
    "api_key",
    "secret",
)


def _new_id(prefix: str) -> str:
    return prefix


def create_v0438_slash_command_spec(
    command: str,
    category: str,
    description_ko: str,
    usage_hint: str | None = None,
    primary: bool = True,
    **overrides: Any,
) -> V0438SlashCommandSpec:
    defaults = {
        "command": command,
        "category": category,
        "description_ko": description_ko,
        "usage_hint": usage_hint,
        "primary": primary,
        "read_only_registry_entry": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438SlashCommandSpec(**defaults)


def _registry_specs() -> tuple[V0438SlashCommandSpec, ...]:
    data = (
        (V0438SlashCommandCategory.WORKFLOWS.value, (("/summary", "업무 요약 작성", "<내용>"), ("/todo", "TODO와 다음 액션 추출", "<내용>"), ("/memo", "업무 메모 작성", "<내용>"), ("/decision", "의사결정 brief 작성", "<내용>"), ("/handoff", "인수인계문 작성", "<내용>"), ("/clarify", "불명확한 점 확인", "<질문>"))),
        (V0438SlashCommandCategory.ARTIFACTS.value, (("/artifact last", "최근 artifact 보기", None), ("/revise", "최근 artifact 수정 요청", "<요청>"))),
        (V0438SlashCommandCategory.NOTES.value, (("/note", "로컬 업무 노트 남기기", "<내용>"), ("/notes", "로컬 노트 목록", None), ("/note last", "최근 노트 보기", None), ("/note from-artifact", "최근 artifact를 노트로 저장", None), ("/notes search", "로컬 노트 검색", "<검색어>"))),
        (V0438SlashCommandCategory.EVIDENCE.value, (("/recall", "로컬 근거 recall", "<검색어>"), ("/evidence", "로컬 근거 검색", "<검색어>"), ("/evidence sources", "근거 source 보기", None), ("/evidence last", "최근 근거 pack 보기", None), ("/evidence explain", "근거 검색 설명", None), ("/use-evidence", "근거 pack 선택", "<검색어>"), ("/evidence used", "사용 중인 근거 보기", None))),
        (V0438SlashCommandCategory.GROUNDED_WORKFLOWS.value, (("/grounded-summary", "근거 기반 요약", "<내용>"), ("/grounded-todo", "근거 기반 TODO", "<내용>"), ("/grounded-memo", "근거 기반 메모", "<내용>"), ("/grounded-decision", "근거 기반 의사결정", "<내용>"), ("/grounded-handoff", "근거 기반 인수인계", "<내용>"), ("/grounding-check", "grounding 점검", None))),
        (V0438SlashCommandCategory.PILOT_RELEASE.value, (("/pilot status", "pilot 상태", None), ("/pilot score", "pilot 점수", None), ("/pilot findings", "pilot findings", None), ("/pilot review", "pilot review", None), ("/pilot next", "다음 track 추천", None), ("/pilot report", "pilot report", None), ("/acceptance", "acceptance checklist", None), ("/workflow score", "workflow 점수", None), ("/polish status", "polish 상태", None), ("/polish findings", "polish findings", None), ("/polish report", "polish report", None), ("/pilot close", "pilot closure 평가", None), ("/v044 readiness", "v0.44 readiness", None), ("/v044 scope", "v0.44 scope", None), ("/v044 risks", "v0.44 risks", None), ("/v044 handoff", "v0.44 handoff", None))),
        (V0438SlashCommandCategory.SYSTEM.value, (("/help", "도움말", "commands"), ("/status", "상태 상세", None), ("/provider", "provider 상태 안내", None), ("/about", "Schumpeter 소개", None), ("/about --debug", "debug lineage 보기", None), ("/capabilities", "가능/불가 기능", None), ("/memory-boundary", "memory boundary", None), ("/context", "현재 context", None), ("/what-happened", "진단 요약", None), ("/report", "diagnostic bundle", None), ("/exit", "세션 종료", None))),
    )
    specs: list[V0438SlashCommandSpec] = []
    for category, entries in data:
        for command, description, usage in entries:
            specs.append(create_v0438_slash_command_spec(command, category, description, usage))
    return tuple(specs)


def create_v0438_slash_command_registry(**overrides: Any) -> V0438SlashCommandRegistry:
    defaults = {
        "registry_id": "v0438-slash-command-registry",
        "commands": _registry_specs(),
        "deterministic": True,
        "read_only": True,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438SlashCommandRegistry(**defaults)


def list_v0438_slash_commands(registry: V0438SlashCommandRegistry | None = None) -> tuple[V0438SlashCommandSpec, ...]:
    return (registry or create_v0438_slash_command_registry()).commands


def group_v0438_slash_commands(commands: Sequence[V0438SlashCommandSpec] | None = None) -> dict[str, tuple[V0438SlashCommandSpec, ...]]:
    grouped: dict[str, list[V0438SlashCommandSpec]] = {}
    for command in commands or list_v0438_slash_commands():
        grouped.setdefault(command.category, []).append(command)
    return {category: tuple(items) for category, items in grouped.items()}


def filter_v0438_slash_commands(prefix: str = "/", registry: V0438SlashCommandRegistry | None = None) -> tuple[V0438SlashCommandSpec, ...]:
    normalized = (prefix or "/").strip()
    if not normalized.startswith("/"):
        normalized = "/" + normalized
    commands = list_v0438_slash_commands(registry)
    if normalized == "/":
        return commands
    if normalized in {"/g", "/grounded"}:
        return tuple(command for command in commands if command.category == V0438SlashCommandCategory.GROUNDED_WORKFLOWS.value)
    if normalized == "/e":
        return tuple(command for command in commands if command.category == V0438SlashCommandCategory.EVIDENCE.value)
    return tuple(command for command in commands if command.command.startswith(normalized))


def create_v0438_completion_item(spec: V0438SlashCommandSpec, **overrides: Any) -> V0438SlashCommandCompletionItem:
    display = f"{spec.command} - {spec.description_ko}"
    defaults = {
        "command": spec.command,
        "insert_text": spec.command + (" " if spec.usage_hint else ""),
        "display_text": display,
        "description_ko": spec.description_ko,
        "category": spec.category,
        "executes_command": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438SlashCommandCompletionItem(**defaults)


def complete_v0438_slash_command(prefix: str = "/") -> V0438SlashCommandCompletionResult:
    items = tuple(create_v0438_completion_item(spec) for spec in filter_v0438_slash_commands(prefix))
    return V0438SlashCommandCompletionResult(
        result_id="v0438-slash-completion-result",
        prefix=prefix,
        items=items,
        command_executed=False,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        repo_search_used=False,
        workspace_read_opened=False,
        memory_mutated=False,
        production_certified=False,
    )


def _category_title(category: str) -> str:
    return {
        V0438SlashCommandCategory.WORKFLOWS.value: "Workflows",
        V0438SlashCommandCategory.ARTIFACTS.value: "Artifacts",
        V0438SlashCommandCategory.NOTES.value: "Notes",
        V0438SlashCommandCategory.EVIDENCE.value: "Evidence",
        V0438SlashCommandCategory.GROUNDED_WORKFLOWS.value: "Grounded Workflows",
        V0438SlashCommandCategory.PILOT_RELEASE.value: "Pilot / Release",
        V0438SlashCommandCategory.SYSTEM.value: "System",
    }.get(category, "Unknown")


def create_v0438_slash_command_palette_request(
    prefix: str = "/",
    render_mode: str = V0438SlashCommandPaletteRenderMode.PLAIN.value,
    plain: bool = True,
    max_items: int | None = None,
    **overrides: Any,
) -> V0438SlashCommandPaletteRequest:
    defaults = {
        "request_id": "v0438-slash-command-palette-request",
        "prefix": prefix,
        "render_mode": render_mode,
        "plain": plain,
        "max_items": max_items,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438SlashCommandPaletteRequest(**defaults)


def render_v0438_command_palette_plain(request: V0438SlashCommandPaletteRequest | None = None) -> str:
    request = request or create_v0438_slash_command_palette_request()
    commands = filter_v0438_slash_commands(request.prefix)
    if request.max_items is not None:
        commands = commands[: request.max_items]
    lines = ["Schumpeter command palette", "", "명령을 선택하거나 입력한 뒤 Enter를 눌러 실행합니다.", ""]
    for category, specs in group_v0438_slash_commands(commands).items():
        lines.append(_category_title(category))
        for spec in specs:
            usage = f" {spec.usage_hint}" if spec.usage_hint else ""
            lines.append(f"  {spec.command}{usage} - {spec.description_ko}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_v0438_command_palette(request: V0438SlashCommandPaletteRequest | None = None) -> V0438SlashCommandPaletteResult:
    request = request or create_v0438_slash_command_palette_request()
    commands = filter_v0438_slash_commands(request.prefix)
    if request.max_items is not None:
        commands = commands[: request.max_items]
    return V0438SlashCommandPaletteResult(
        result_id="v0438-slash-command-palette-result",
        request=request,
        commands=commands,
        rendered_text=render_v0438_command_palette_plain(request),
        grouped=True,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        repo_search_used=False,
        workspace_read_opened=False,
        memory_mutated=False,
        core_memory_written=False,
        production_certified=False,
    )


def detect_v0438_prompt_toolkit_availability() -> V0438PromptToolkitAvailability:
    try:
        available = importlib.util.find_spec("prompt_toolkit") is not None
    except Exception as exc:  # pragma: no cover - defensive optional dependency probe
        return V0438PromptToolkitAvailability("v0438-prompt-toolkit", False, "prompt_toolkit", True, str(exc), False)
    return V0438PromptToolkitAvailability("v0438-prompt-toolkit", available, "prompt_toolkit", True, None, False)


def create_v0438_interactive_input_policy(**overrides: Any) -> V0438InteractiveInputPolicy:
    defaults = {
        "policy_id": "v0438-interactive-input-policy",
        "prompt_toolkit_preferred": True,
        "prompt_toolkit_optional": True,
        "plain_mode_disables_interactive_palette": True,
        "fallback_on_import_error": True,
        "completion_executes_commands": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438InteractiveInputPolicy(**defaults)


def create_v0438_plain_input_fallback_policy(**overrides: Any) -> V0438PlainInputFallbackPolicy:
    defaults = {
        "policy_id": "v0438-plain-input-fallback-policy",
        "slash_enter_shows_palette": True,
        "help_commands_shows_palette": True,
        "plain_mode_supported": True,
        "interactive_completion_required": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438PlainInputFallbackPolicy(**defaults)


def create_v0438_command_palette_noisy_output_guard(text: str) -> V0438CommandPaletteNoisyOutputGuard:
    found = tuple(item for item in FORBIDDEN_PALETTE_STRINGS if item in text)
    return V0438CommandPaletteNoisyOutputGuard("v0438-command-palette-guard", FORBIDDEN_PALETTE_STRINGS, not found, found, False)


def create_v0438_command_palette_safety_report(**overrides: Any) -> V0438CommandPaletteSafetyReport:
    defaults = {
        "report_id": "v0438-command-palette-safety-report",
        "command_palette_opened": True,
        "provider_invocation_allowed": False,
        "prompt_submission_allowed": False,
        "shell_execution_allowed": False,
        "git_execution_allowed": False,
        "repo_search_allowed": False,
        "workspace_read_allowed": False,
        "file_edit_allowed": False,
        "patch_apply_allowed": False,
        "provider_tool_calling_allowed": False,
        "function_calling_allowed": False,
        "subagent_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438CommandPaletteSafetyReport(**defaults)


def create_v0438_command_palette_readiness_report(**overrides: Any) -> V0438CommandPaletteReadinessReport:
    defaults = {
        "report_id": "v0438-command-palette-readiness-report",
        "command_registry_ready": True,
        "grouped_palette_ready": True,
        "completion_ready": True,
        "plain_fallback_ready": True,
        "start_lobby_hint_ready": True,
        "safety_report_ready": True,
        "ready_for_workspace_read": False,
        "ready_for_repo_search": False,
        "ready_for_shell_execution": False,
        "ready_for_git_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0438CommandPaletteReadinessReport(**defaults)


def execute_v0438_command_palette_golden_case(case: V0438CommandPaletteGoldenCase) -> V0438CommandPaletteGoldenResult:
    result = render_v0438_command_palette(create_v0438_slash_command_palette_request(case.prefix))
    missing = tuple(item for item in case.expected_commands if item not in result.rendered_text)
    forbidden = tuple(item for item in case.forbidden_strings if item in result.rendered_text)
    high_risk_zero = not any((result.provider_invoked, result.prompt_submitted, result.shell_executed, result.repo_search_used, result.workspace_read_opened, result.memory_mutated))
    passed = not missing and not forbidden and high_risk_zero and result.production_certified is False
    return V0438CommandPaletteGoldenResult("v0438-command-palette-golden-result", case, passed, result.rendered_text, missing, forbidden, high_risk_zero, False)


def create_v0439_or_v044_handoff(**overrides: Any) -> V0439OrV044Handoff:
    defaults = {
        "handoff_id": "v0439-or-v044-command-palette-handoff",
        "recommendation": "retry_v0438_acceptance_or_continue_v0439",
        "reason": "Slash command palette is a UX surface only; v0.44 still depends on v0.43.7 and v0.43.8 acceptance.",
        "required_before_next_track": ("manual slash palette acceptance", "v0.43.7 golden transcripts", "start lobby clean rendering"),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439OrV044Handoff(**defaults)


def read_v0438_interactive_input(prompt_text: str = "> ", plain: bool = False) -> str:
    if plain or not detect_v0438_prompt_toolkit_availability().available:
        return input(prompt_text)
    try:
        from prompt_toolkit import prompt
        from prompt_toolkit.completion import Completer, Completion
    except Exception:
        return input(prompt_text)

    class SlashCompleter(Completer):
        def get_completions(self, document: Any, complete_event: Any) -> Iterable[Any]:
            text = document.text_before_cursor
            if not text.startswith("/"):
                return
            for item in complete_v0438_slash_command(text).items:
                yield Completion(item.insert_text, start_position=-len(text), display=item.command, display_meta=item.description_ko)

    return prompt(prompt_text, completer=SlashCompleter(), complete_while_typing=True)


__all__ = [
    name
    for name in globals()
    if name.startswith("V0438")
    or name.startswith("V0439")
    or name.startswith("create_v0438")
    or name.startswith("create_v0439")
    or name.startswith("list_v0438")
    or name.startswith("group_v0438")
    or name.startswith("filter_v0438")
    or name.startswith("render_v0438")
    or name.startswith("complete_v0438")
    or name.startswith("detect_v0438")
    or name.startswith("execute_v0438")
    or name.startswith("read_v0438")
    or name == "FORBIDDEN_PALETTE_STRINGS"
]
