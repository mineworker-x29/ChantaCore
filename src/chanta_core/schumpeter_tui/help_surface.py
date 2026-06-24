"""Schumpeter TUI help surface backed by the canonical command registry."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable, Sequence

from chanta_core.schumpeter_tui.command_registry import (
    V043111CommandCategory,
    V043111CommandSpec,
    create_v043111_command_registry,
    group_v043111_command_specs,
    list_v04310_shared_command_names,
)


class V04310HelpMode(StrEnum):
    OVERVIEW = "overview"
    COMMANDS = "commands"
    WORKFLOWS = "workflows"
    EVIDENCE = "evidence"
    GROUNDED = "grounded"
    NOTES = "notes"
    STATUS = "status"
    SAFETY = "safety"
    TUI = "tui"
    EXAMPLES = "examples"
    UNKNOWN = "unknown"


class V04310HelpCommandCategory(StrEnum):
    START = "Start"
    WORKFLOWS = "Workflows"
    ARTIFACTS = "Artifacts"
    NOTES = "Notes"
    EVIDENCE = "Evidence"
    GROUNDED_WORKFLOWS = "Grounded Workflows"
    STATUS_DIAGNOSTICS = "Status / Diagnostics"
    PILOT_RELEASE = "Pilot / Release"
    TUI = "TUI"
    SAFETY = "Safety"
    EXIT = "Exit"


class V04310CommandSideEffectLabel(StrEnum):
    DETERMINISTIC = "deterministic"
    READ_ONLY = "read-only"
    LOCAL_NOTE_WRITE = "local note write"
    DIAGNOSTIC = "diagnostic"
    DEBUG_ONLY = "debug-only"
    NOT_OPENED_YET = "not opened yet"


class V04310CommandProviderPolicyLabel(StrEnum):
    DETERMINISTIC = "deterministic"
    MAY_USE_PROVIDER = "may use provider"
    NON_PROVIDER = "non-provider"
    DEBUG_ONLY = "debug-only"
    NOT_OPENED_YET = "not opened yet"


@dataclass(frozen=True)
class V04310HelpTopic:
    topic_id: str
    mode: str
    title: str
    command: str
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpCommandSpec:
    command: str
    category: str
    short_description_ko: str
    long_description_ko: str
    usage: str
    example: str
    provider_invocation_policy: str
    side_effect_policy: str
    status: str
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpRenderPolicy:
    policy_id: str
    concise_default: bool
    grouped_details: bool
    human_facing_labels: bool
    raw_metadata_hidden: bool
    provider_invoked: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpRequest:
    request_id: str
    mode: str
    raw_text: str
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpSection:
    section_id: str
    title: str
    lines: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpExample:
    example_id: str
    text: str
    description_ko: str
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpResult:
    result_id: str
    mode: str
    rendered_text: str
    sections: tuple[V04310HelpSection, ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpRegistryConsistencyReport:
    report_id: str
    shared_registry_used: bool
    help_command_names: tuple[str, ...]
    palette_command_names: tuple[str, ...]
    missing_from_palette: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpNoisyOutputGuard:
    guard_id: str
    forbidden_strings: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    passed: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpSafetyReport:
    report_id: str
    help_surface_opened: bool
    workspace_read_opened: bool
    repo_search_opened: bool
    shell_execution_opened: bool
    git_execution_opened: bool
    file_edit_opened: bool
    provider_tool_calling_opened: bool
    function_calling_opened: bool
    subagent_opened: bool
    memory_mutation_opened: bool
    core_memory_write_opened: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpReadinessReport:
    report_id: str
    help_surface_ready: bool
    help_topics_ready: bool
    shared_registry_consistency_ready: bool
    golden_help_ready: bool
    ready_for_workspace_read: bool
    ready_for_repo_search: bool
    ready_for_shell_execution: bool
    ready_for_git_execution: bool
    ready_for_file_edit: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_subagent_invocation: bool
    ready_for_memory_mutation: bool
    ready_for_core_memory_write: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpGoldenCase:
    case_id: str
    command: str
    expected_contains: tuple[str, ...]
    forbidden_strings: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310HelpGoldenResult:
    result_id: str
    case: V04310HelpGoldenCase
    rendered_text: str
    passed: bool
    missing_expected: tuple[str, ...]
    forbidden_found: tuple[str, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04311VisualPolishHandoff:
    handoff_id: str
    target_version: str
    focus: tuple[str, ...]
    still_closed: tuple[str, ...]
    production_certified: bool


FORBIDDEN_HELP_STRINGS = (
    "ChantaGrowthKernel",
    "legacy Schumpeter",
    "safety:",
    "shell=false",
    "production_certified=false",
    "provider_invoked",
    "prompt_submitted",
    "base_url",
    "api_key",
    "secret",
    "Traceback",
    "No source text provided",
)

HELP_MODAL_FOOTER_HINT = "Esc 닫기  ·  q 닫기  ·  ↑/↓/PgUp/PgDn 스크롤"


def _help_specs() -> tuple[V043111CommandSpec, ...]:
    return create_v043111_command_registry()


def _section(title: str, lines: Iterable[str]) -> V04310HelpSection:
    section_id = title.lower().replace(" / ", "-").replace(" ", "-")
    return V04310HelpSection(f"v04310-help-section-{section_id}", title, tuple(lines), False)


def _render_sections(title: str, sections: Sequence[V04310HelpSection]) -> str:
    lines = [title, ""]
    for section in sections:
        lines.append(section.title)
        lines.extend(section.lines)
        lines.append("")
    lines.append(HELP_MODAL_FOOTER_HINT)
    return "\n".join(lines).rstrip()


def _format_spec(spec: V043111CommandSpec, detailed: bool = False) -> tuple[str, ...]:
    mode = ", ".join(dict.fromkeys((spec.provider_policy_label, spec.side_effect_label, spec.availability)))
    if not detailed:
        return (f"- {spec.command} - {spec.short_description_ko} ({spec.usage}) [{mode}]",)
    example = spec.examples[0] if spec.examples else spec.usage
    return (
        spec.usage,
        f"  {spec.long_description_ko}",
        f"  mode: {mode}",
        f"  example: {example}",
    )


def _specs_for_categories(categories: Sequence[str]) -> tuple[V043111CommandSpec, ...]:
    allowed = set(categories)
    return tuple(spec for spec in _help_specs() if spec.category in allowed)


def create_v04310_help_topic(mode: str = V04310HelpMode.OVERVIEW.value, **overrides: Any) -> V04310HelpTopic:
    titles = {
        V04310HelpMode.OVERVIEW.value: ("Schumpeter Help", "/help"),
        V04310HelpMode.COMMANDS.value: ("Schumpeter Commands", "/help commands"),
        V04310HelpMode.WORKFLOWS.value: ("Workflow Help", "/help workflows"),
        V04310HelpMode.EVIDENCE.value: ("Evidence Help", "/help evidence"),
        V04310HelpMode.GROUNDED.value: ("Grounded Workflow Help", "/help grounded"),
        V04310HelpMode.NOTES.value: ("Notes Help", "/help notes"),
        V04310HelpMode.STATUS.value: ("Status Help", "/help status"),
        V04310HelpMode.SAFETY.value: ("Safety Help", "/help safety"),
        V04310HelpMode.TUI.value: ("TUI Help", "/help tui"),
        V04310HelpMode.EXAMPLES.value: ("Examples", "/help examples"),
    }
    title, command = titles.get(mode, ("Unknown Help Topic", "/help"))
    defaults = {
        "topic_id": f"v04310-help-topic-{mode}",
        "mode": mode,
        "title": title,
        "command": command,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpTopic(**defaults)


def create_v04310_help_command_spec(
    command: str,
    category: str,
    short_description_ko: str,
    long_description_ko: str,
    usage: str,
    example: str,
    provider_invocation_policy: str = V04310CommandProviderPolicyLabel.DETERMINISTIC.value,
    side_effect_policy: str = V04310CommandSideEffectLabel.DETERMINISTIC.value,
    status: str = "available",
    **overrides: Any,
) -> V04310HelpCommandSpec:
    defaults = {
        "command": command,
        "category": category,
        "short_description_ko": short_description_ko,
        "long_description_ko": long_description_ko,
        "usage": usage,
        "example": example,
        "provider_invocation_policy": provider_invocation_policy,
        "side_effect_policy": side_effect_policy,
        "status": status,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpCommandSpec(**defaults)


def create_v04310_help_command_category(name: str, **overrides: Any) -> V04310HelpSection:
    defaults = {
        "section_id": f"v04310-help-category-{name.lower().replace(' ', '-')}",
        "title": name,
        "lines": (),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpSection(**defaults)


def create_v04310_help_render_policy(**overrides: Any) -> V04310HelpRenderPolicy:
    defaults = {
        "policy_id": "v04310-help-render-policy",
        "concise_default": True,
        "grouped_details": True,
        "human_facing_labels": True,
        "raw_metadata_hidden": True,
        "provider_invoked": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpRenderPolicy(**defaults)


def create_v04310_help_request(raw_text: str = "/help", **overrides: Any) -> V04310HelpRequest:
    topic = " ".join(raw_text.strip().split()[1:]).lower() if raw_text.strip().startswith("/help") else ""
    mode = {
        "": V04310HelpMode.OVERVIEW.value,
        "overview": V04310HelpMode.OVERVIEW.value,
        "commands": V04310HelpMode.COMMANDS.value,
        "workflows": V04310HelpMode.WORKFLOWS.value,
        "evidence": V04310HelpMode.EVIDENCE.value,
        "grounded": V04310HelpMode.GROUNDED.value,
        "notes": V04310HelpMode.NOTES.value,
        "status": V04310HelpMode.STATUS.value,
        "safety": V04310HelpMode.SAFETY.value,
        "tui": V04310HelpMode.TUI.value,
        "examples": V04310HelpMode.EXAMPLES.value,
    }.get(topic, V04310HelpMode.UNKNOWN.value)
    defaults = {
        "request_id": "v04310-help-request",
        "mode": mode,
        "raw_text": raw_text,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpRequest(**defaults)


def create_v04310_help_result(mode: str, rendered_text: str, sections: Sequence[V04310HelpSection] = (), **overrides: Any) -> V04310HelpResult:
    defaults = {
        "result_id": "v04310-help-result",
        "mode": mode,
        "rendered_text": rendered_text,
        "sections": tuple(sections),
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
    return V04310HelpResult(**defaults)


def render_v04310_help_overview() -> V04310HelpResult:
    sections = (
        _section(
            "소개",
            (
                "Schumpeter는 Process Intelligence-native 업무 보조 에이전트입니다.",
                "일반 문장을 입력하거나, slash command로 업무 흐름을 선택할 수 있습니다.",
            ),
        ),
        _section(
            "빠른 시작",
            (
                "- 그냥 입력하기: 오늘 작업을 요약해줘",
                "- 업무 요약: /summary <내용>",
                "- 다음 액션: /todo <내용>",
                "- 근거 검색: /recall <검색어>",
                "- 상태 확인: /status",
                "- 종료: /exit",
            ),
        ),
        _section(
            "자세히 보기",
            (
                "- /help commands",
                "- /help workflows",
                "- /help evidence",
                "- /help grounded",
                "- /help notes",
                "- /help status",
                "- /help safety",
                "- /help tui",
                "- /help examples",
            ),
        ),
    )
    return create_v04310_help_result(V04310HelpMode.OVERVIEW.value, _render_sections("Schumpeter Help", sections), sections)


def render_v04310_help_commands() -> V04310HelpResult:
    grouped = group_v043111_command_specs(_help_specs())
    sections: list[V04310HelpSection] = []
    for category in (category.value for category in V043111CommandCategory):
        specs = grouped.get(category, ())
        if specs:
            sections.append(_section(category, (line for spec in specs for line in _format_spec(spec))))
    exit_specs = tuple(spec for spec in _help_specs() if spec.command == "/exit")
    if exit_specs:
        sections.append(_section("Exit", (line for spec in exit_specs for line in _format_spec(spec))))
    return create_v04310_help_result(V04310HelpMode.COMMANDS.value, _render_sections("Schumpeter Commands", sections), sections)


def _topic_result(mode: str, title: str, categories: Sequence[str], detailed: bool = True) -> V04310HelpResult:
    grouped = group_v043111_command_specs(_specs_for_categories(categories))
    sections = tuple(
        _section(category, (line for spec in grouped.get(category, ()) for line in _format_spec(spec, detailed)))
        for category in categories
    )
    return create_v04310_help_result(mode, _render_sections(title, sections), sections)


def render_v04310_help_workflows() -> V04310HelpResult:
    return _topic_result(V04310HelpMode.WORKFLOWS.value, "Workflow Help", (V043111CommandCategory.WORKFLOWS.value,))


def render_v04310_help_evidence() -> V04310HelpResult:
    return _topic_result(V04310HelpMode.EVIDENCE.value, "Evidence Help", (V043111CommandCategory.EVIDENCE.value,))


def render_v04310_help_grounded() -> V04310HelpResult:
    return _topic_result(V04310HelpMode.GROUNDED.value, "Grounded Workflow Help", (V043111CommandCategory.GROUNDED_WORKFLOWS.value,))


def render_v04310_help_notes() -> V04310HelpResult:
    return _topic_result(V04310HelpMode.NOTES.value, "Notes Help", (V043111CommandCategory.NOTES.value,))


def render_v04310_help_status() -> V04310HelpResult:
    return _topic_result(
        V04310HelpMode.STATUS.value,
        "Status Help",
        (V043111CommandCategory.START_BASIC.value, V043111CommandCategory.STATUS_DIAGNOSTICS.value, V043111CommandCategory.PILOT_RELEASE.value),
    )


def render_v04310_help_safety() -> V04310HelpResult:
    sections = (
        _section(
            "현재 닫혀 있는 기능",
            (
                "- 저장소 직접 읽기",
                "- repo search",
                "- 셸/git 실행",
                "- 파일 수정/apply",
                "- provider tool/function calling",
                "- subagent 실행",
                "- 자동 메모리 승격",
                "- production certification",
            ),
        ),
        _section(
            "운영 원칙",
            (
                "이 기능들은 v0.44 이후 controlled design gate를 거쳐 단계적으로 열 수 있습니다.",
                "현재 TUI, help, palette, status refresh는 이 기능들을 실행하지 않습니다.",
            ),
        ),
    )
    return create_v04310_help_result(V04310HelpMode.SAFETY.value, _render_sections("Safety Help", sections), sections)


def render_v04310_help_tui() -> V04310HelpResult:
    sections = (
        _section(
            "TUI 사용법",
            (
                "- 일반 문장을 입력하면 Schumpeter가 대화형으로 답합니다.",
                "- / 로 시작하면 slash command를 사용할 수 있습니다.",
                "- / 는 가능한 환경에서 command suggestions를 엽니다.",
                "- Ctrl+P는 slash palette를 엽니다.",
                "- /help commands 로 전체 명령을 볼 수 있습니다.",
                "- /status 로 현재 PI/provider/trace/evidence/safety 상태를 확인합니다.",
                "- /exit 로 종료합니다.",
            ),
        ),
        _section("Snapshot", ("- chanta-cli tui snapshot --width 120", "- chanta-cli tui snapshot --plain")),
    )
    return create_v04310_help_result(V04310HelpMode.TUI.value, _render_sections("TUI Help", sections), sections)


def create_v04310_help_example(text: str, description_ko: str = "", **overrides: Any) -> V04310HelpExample:
    defaults = {
        "example_id": f"v04310-help-example-{abs(hash(text))}",
        "text": text,
        "description_ko": description_ko,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpExample(**defaults)


def render_v04310_help_examples() -> V04310HelpResult:
    examples = (
        create_v04310_help_example("오늘 회의 내용을 정리해줘", "일반 업무 정리"),
        create_v04310_help_example("오늘 작업을 요약해줘", "일반 대화 입력"),
        create_v04310_help_example("/summary 오늘 테스트 결과를 요약해줘", "업무 요약"),
        create_v04310_help_example("/todo 위 내용에서 다음 액션만 뽑아줘", "다음 액션"),
        create_v04310_help_example("/decision v0.44로 넘어갈지 판단해줘", "판단 정리"),
        create_v04310_help_example("/recall v0.43.10", "근거 recall"),
        create_v04310_help_example("/use-evidence v0.43.10", "근거 선택"),
        create_v04310_help_example("/grounded-summary 선택한 근거로 진행상황을 요약해줘", "근거 기반 요약"),
    )
    sections = (_section("Practical Examples", (f"- {example.text} : {example.description_ko}" for example in examples)),)
    return create_v04310_help_result(V04310HelpMode.EXAMPLES.value, _render_sections("Examples", sections), sections)


def _render_unknown(raw_text: str) -> V04310HelpResult:
    topics = "/help commands, /help workflows, /help evidence, /help grounded, /help notes, /help status, /help safety, /help tui, /help examples"
    text = f"Unknown help topic: {raw_text}\nAvailable topics: {topics}"
    return create_v04310_help_result(V04310HelpMode.UNKNOWN.value, text, ())


def render_v04310_help(request: V04310HelpRequest | str = "/help") -> V04310HelpResult:
    request = create_v04310_help_request(request) if isinstance(request, str) else request
    return {
        V04310HelpMode.OVERVIEW.value: render_v04310_help_overview,
        V04310HelpMode.COMMANDS.value: render_v04310_help_commands,
        V04310HelpMode.WORKFLOWS.value: render_v04310_help_workflows,
        V04310HelpMode.EVIDENCE.value: render_v04310_help_evidence,
        V04310HelpMode.GROUNDED.value: render_v04310_help_grounded,
        V04310HelpMode.NOTES.value: render_v04310_help_notes,
        V04310HelpMode.STATUS.value: render_v04310_help_status,
        V04310HelpMode.SAFETY.value: render_v04310_help_safety,
        V04310HelpMode.TUI.value: render_v04310_help_tui,
        V04310HelpMode.EXAMPLES.value: render_v04310_help_examples,
    }.get(request.mode, lambda: _render_unknown(request.raw_text))()


def label_v04310_command_side_effect(spec: V04310HelpCommandSpec | V043111CommandSpec) -> str:
    return getattr(spec, "side_effect_policy", getattr(spec, "side_effect_label", "deterministic"))


def label_v04310_command_provider_policy(spec: V04310HelpCommandSpec | V043111CommandSpec) -> str:
    return getattr(spec, "provider_invocation_policy", getattr(spec, "provider_policy_label", "deterministic"))


def create_v04310_help_registry_consistency_report(**overrides: Any) -> V04310HelpRegistryConsistencyReport:
    help_names = tuple(spec.command for spec in _help_specs())
    palette_names = list_v04310_shared_command_names("/")
    missing = tuple(name for name in help_names if name not in palette_names)
    defaults = {
        "report_id": "v04310-help-registry-consistency-report",
        "shared_registry_used": True,
        "help_command_names": help_names,
        "palette_command_names": palette_names,
        "missing_from_palette": missing,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpRegistryConsistencyReport(**defaults)


def check_v04310_help_noisy_output(text: str) -> V04310HelpNoisyOutputGuard:
    found = tuple(item for item in FORBIDDEN_HELP_STRINGS if item.lower() in text.lower())
    return V04310HelpNoisyOutputGuard("v04310-help-noisy-output-guard", FORBIDDEN_HELP_STRINGS, found, not found, False)


def create_v04310_help_safety_report(**overrides: Any) -> V04310HelpSafetyReport:
    defaults = {
        "report_id": "v04310-help-safety-report",
        "help_surface_opened": True,
        "workspace_read_opened": False,
        "repo_search_opened": False,
        "shell_execution_opened": False,
        "git_execution_opened": False,
        "file_edit_opened": False,
        "provider_tool_calling_opened": False,
        "function_calling_opened": False,
        "subagent_opened": False,
        "memory_mutation_opened": False,
        "core_memory_write_opened": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpSafetyReport(**defaults)


def create_v04310_help_readiness_report(**overrides: Any) -> V04310HelpReadinessReport:
    defaults = {
        "report_id": "v04310-help-readiness-report",
        "help_surface_ready": True,
        "help_topics_ready": True,
        "shared_registry_consistency_ready": True,
        "golden_help_ready": True,
        "ready_for_workspace_read": False,
        "ready_for_repo_search": False,
        "ready_for_shell_execution": False,
        "ready_for_git_execution": False,
        "ready_for_file_edit": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_subagent_invocation": False,
        "ready_for_memory_mutation": False,
        "ready_for_core_memory_write": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310HelpReadinessReport(**defaults)


def execute_v04310_help_golden_case(command: str = "/help") -> V04310HelpGoldenResult:
    expected = {
        "/help": ("Schumpeter Help", "Process Intelligence-native 업무 보조 에이전트", "빠른 시작", "/summary", "/todo", "/recall", "/status", "/exit", "/help commands", "/help examples"),
        "/help commands": ("Workflows", "Artifacts", "Notes", "Evidence", "Grounded Workflows", "Status / Diagnostics", "Pilot / Release", "TUI", "Safety"),
        "/help safety": ("현재 닫혀 있는 기능", "저장소 직접 읽기", "repo search", "셸/git 실행", "파일 수정/apply", "subagent", "production certification", "v0.44"),
        "/help examples": ("오늘 작업을 요약해줘", "/summary 오늘 테스트 결과를 요약해줘", "/todo", "/decision", "/recall", "/grounded-summary"),
    }.get(command, ())
    case = V04310HelpGoldenCase(f"v04310-help-golden-{command.replace(' ', '-')}", command, expected, FORBIDDEN_HELP_STRINGS, False)
    rendered = render_v04310_help(command).rendered_text
    missing = tuple(item for item in expected if item not in rendered)
    found = tuple(item for item in FORBIDDEN_HELP_STRINGS if item.lower() in rendered.lower())
    return V04310HelpGoldenResult("v04310-help-golden-result", case, rendered, not missing and not found, missing, found, False)


def create_v04311_visual_polish_handoff(**overrides: Any) -> V04311VisualPolishHandoff:
    defaults = {
        "handoff_id": "v04311-visual-polish-handoff",
        "target_version": "v0.43.11 Visual Polish",
        "focus": ("viewport layout", "full-screen redraw", "keyboard ergonomics", "help readability"),
        "still_closed": ("workspace read", "repo search", "shell/git", "file edit/apply", "provider tools/functions", "subagents", "persistent core memory persistence", "production certification"),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04311VisualPolishHandoff(**defaults)


__all__ = [name for name in globals() if name.startswith("V04310") or name.startswith("V04311") or name.startswith("create_v04310") or name.startswith("render_v04310") or name.startswith("label_v04310") or name.startswith("check_v04310") or name.startswith("execute_v04310") or name.startswith("FORBIDDEN")]
