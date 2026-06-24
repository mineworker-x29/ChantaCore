"""Canonical Schumpeter TUI slash command registry.

The registry is display metadata only. It is used by help, the slash palette,
completion, and the TUI dispatcher, and it does not execute commands.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any, Iterable


class V043111CommandAvailability(StrEnum):
    AVAILABLE = "available"
    PREVIEW = "preview"
    DEBUG_ONLY = "debug_only"
    NOT_OPENED = "not_opened"


class V043111RendererKind(StrEnum):
    MESSAGE = "message"
    ARTIFACT = "artifact"
    DIAGNOSTIC = "diagnostic"
    STATUS = "status"
    ERROR = "error"
    MODAL = "modal"


class V043111CommandCategory(StrEnum):
    START_BASIC = "Start / Basic"
    WORKFLOWS = "Workflows"
    ARTIFACTS = "Artifacts"
    NOTES = "Notes"
    EVIDENCE = "Evidence"
    GROUNDED_WORKFLOWS = "Grounded Workflows"
    STATUS_DIAGNOSTICS = "Status / Diagnostics"
    PILOT_RELEASE = "Pilot / Release"
    TUI = "TUI"
    SAFETY = "Safety"


@dataclass(frozen=True)
class V043111CommandSpec:
    command: str
    aliases: tuple[str, ...]
    category: str
    short_description_ko: str
    long_description_ko: str
    usage: str
    examples: tuple[str, ...]
    provider_policy_label: str
    side_effect_label: str
    availability: str
    handler_id: str
    requires_argument: bool
    renderer_kind: str
    opens_provider: bool
    opens_workspace_read: bool
    opens_repo_search: bool
    opens_shell: bool
    mutates_memory: bool
    production_certified: bool = False


@dataclass(frozen=True)
class V0439CommandRegistryReuseReport:
    report_id: str
    source_registry: str
    deterministic: bool
    commands: tuple[str, ...]
    command_executed: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


def _spec(
    command: str,
    category: str,
    short: str,
    long: str,
    usage: str,
    examples: Iterable[str],
    handler_id: str,
    renderer_kind: str,
    *,
    aliases: Iterable[str] = (),
    provider: str = "deterministic",
    side_effect: str = "deterministic",
    availability: str = V043111CommandAvailability.AVAILABLE.value,
    requires_argument: bool = False,
    opens_provider: bool = False,
    opens_workspace_read: bool = False,
    opens_repo_search: bool = False,
    opens_shell: bool = False,
    mutates_memory: bool = False,
) -> V043111CommandSpec:
    return V043111CommandSpec(
        command=command,
        aliases=tuple(aliases),
        category=category,
        short_description_ko=short,
        long_description_ko=long,
        usage=usage,
        examples=tuple(examples),
        provider_policy_label=provider,
        side_effect_label=side_effect,
        availability=availability,
        handler_id=handler_id,
        requires_argument=requires_argument,
        renderer_kind=renderer_kind,
        opens_provider=opens_provider,
        opens_workspace_read=opens_workspace_read,
        opens_repo_search=opens_repo_search,
        opens_shell=opens_shell,
        mutates_memory=mutates_memory,
    )


def create_v043111_command_registry() -> tuple[V043111CommandSpec, ...]:
    C = V043111CommandCategory
    R = V043111RendererKind
    A = V043111CommandAvailability
    return (
        _spec("/help", C.START_BASIC.value, "도움말을 봅니다.", "Schumpeter 사용법과 상세 도움말 주제를 엽니다.", "/help [topic]", ("/help commands",), "help", R.MODAL.value, aliases=("/?",)),
        _spec("/help commands", C.START_BASIC.value, "전체 명령을 봅니다.", "등록된 slash command를 category별로 봅니다.", "/help commands", ("/help commands",), "help_commands", R.MODAL.value),
        _spec("/exit", C.START_BASIC.value, "TUI를 종료합니다.", "현재 Schumpeter TUI 세션을 종료합니다.", "/exit", ("/exit",), "exit", R.MESSAGE.value, aliases=("/quit",)),
        _spec("/about", C.START_BASIC.value, "제품 정보를 봅니다.", "Schumpeter 제품 표면과 ChantaCore runtime lineage를 확인합니다.", "/about", ("/about",), "about", R.MODAL.value),
        _spec("/status", C.START_BASIC.value, "간단한 상태를 봅니다.", "PI/provider/trace/evidence/safety 상태를 간결하게 봅니다.", "/status", ("/status",), "status", R.STATUS.value, side_effect="diagnostic"),
        _spec("/status --debug", C.START_BASIC.value, "상세 상태를 봅니다.", "닫힌 capability matrix를 포함한 debug 상태를 봅니다.", "/status --debug", ("/status --debug",), "status_debug", R.STATUS.value, side_effect="debug-only", availability=A.DEBUG_ONLY.value),
        _spec("/capabilities", C.START_BASIC.value, "가능한 일을 봅니다.", "현재 열려 있는 업무 기능과 닫힌 경계를 설명합니다.", "/capabilities", ("/capabilities",), "capabilities", R.STATUS.value),
        _spec("/summary", C.WORKFLOWS.value, "업무 요약을 만듭니다.", "입력 내용을 핵심 요약과 다음 액션으로 정리합니다.", "/summary <내용>", ("/summary 오늘 테스트 결과를 요약해줘",), "workflow_summary", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/todo", C.WORKFLOWS.value, "다음 액션을 뽑습니다.", "입력 내용에서 TODO와 미확정 요소를 추출합니다.", "/todo <내용>", ("/todo 위 내용에서 다음 액션만 뽑아줘",), "workflow_todo", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/memo", C.WORKFLOWS.value, "업무 메모를 만듭니다.", "회의나 업무 내용을 읽기 쉬운 메모로 정리합니다.", "/memo <내용>", ("/memo 오늘 회의 내용을 정리해줘",), "workflow_memo", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/decision", C.WORKFLOWS.value, "의사결정 brief를 만듭니다.", "선택지, 근거, tradeoff, 결론을 정리합니다.", "/decision <질문>", ("/decision v0.44로 넘어갈지 판단해줘",), "workflow_decision", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/handoff", C.WORKFLOWS.value, "인수인계문을 만듭니다.", "다음 세션으로 넘길 배경, 진행 상태, 위험, 액션을 정리합니다.", "/handoff <내용>", ("/handoff 오늘 진행상황을 넘겨줘",), "workflow_handoff", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/clarify", C.WORKFLOWS.value, "확인 질문을 만듭니다.", "불명확한 요구사항에서 확인해야 할 질문을 뽑습니다.", "/clarify <내용>", ("/clarify 이 요구사항에서 확인할 점",), "workflow_clarify", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/artifact last", C.ARTIFACTS.value, "최근 artifact를 봅니다.", "최근 생성한 업무 산출물을 봅니다.", "/artifact last", ("/artifact last",), "artifact_last", R.ARTIFACT.value),
        _spec("/artifact last --debug", C.ARTIFACTS.value, "최근 artifact debug를 봅니다.", "명시 debug 표면에서 artifact metadata를 확인합니다.", "/artifact last --debug", ("/artifact last --debug",), "artifact_last_debug", R.ARTIFACT.value, side_effect="debug-only", availability=A.DEBUG_ONLY.value),
        _spec("/revise", C.ARTIFACTS.value, "최근 artifact를 수정합니다.", "최근 artifact를 기반으로 수정 요청을 적용합니다.", "/revise <요청>", ("/revise 더 짧게 정리해줘",), "revise", R.ARTIFACT.value, provider="may use provider", requires_argument=True, opens_provider=True),
        _spec("/note", C.NOTES.value, "local work note를 남깁니다.", "현재 세션의 local note로 기록합니다.", "/note <내용>", ("/note 오늘 TUI 테스트 진행",), "note", R.STATUS.value, side_effect="local note write", requires_argument=True),
        _spec("/notes", C.NOTES.value, "local note 목록을 봅니다.", "현재 profile의 bounded local note 목록을 봅니다.", "/notes", ("/notes",), "notes", R.STATUS.value, side_effect="read-only"),
        _spec("/note last", C.NOTES.value, "최근 note를 봅니다.", "마지막 local work note를 봅니다.", "/note last", ("/note last",), "note_last", R.STATUS.value, side_effect="read-only"),
        _spec("/note from-artifact", C.NOTES.value, "artifact를 note로 저장합니다.", "최근 artifact를 local note로 전환합니다.", "/note from-artifact", ("/note from-artifact",), "note_from_artifact", R.STATUS.value, side_effect="local note write"),
        _spec("/notes search", C.NOTES.value, "note를 검색합니다.", "local note 안에서만 검색합니다.", "/notes search <검색어>", ("/notes search TUI",), "notes_search", R.STATUS.value, side_effect="read-only", requires_argument=True),
        _spec("/memory-boundary", C.NOTES.value, "메모리 경계를 봅니다.", "local note와 persistent memory의 경계를 설명합니다.", "/memory-boundary", ("/memory-boundary",), "memory_boundary", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/context", C.NOTES.value, "현재 context를 봅니다.", "현재 TUI가 표시 가능한 bounded context를 봅니다.", "/context", ("/context",), "context", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/recall", C.EVIDENCE.value, "근거를 찾습니다.", "local Schumpeter evidence store 안에서 관련 근거를 찾습니다.", "/recall <검색어>", ("/recall v0.43.10",), "recall", R.DIAGNOSTIC.value, side_effect="read-only", requires_argument=True),
        _spec("/evidence", C.EVIDENCE.value, "근거 검색을 수행합니다.", "선택 가능한 evidence pack을 찾습니다.", "/evidence <검색어>", ("/evidence TUI",), "evidence", R.DIAGNOSTIC.value, side_effect="read-only", requires_argument=True),
        _spec("/evidence sources", C.EVIDENCE.value, "근거 출처를 봅니다.", "현재 evidence surface의 출처 목록을 봅니다.", "/evidence sources", ("/evidence sources",), "evidence_sources", R.DIAGNOSTIC.value, side_effect="read-only"),
        _spec("/evidence last", C.EVIDENCE.value, "최근 evidence pack을 봅니다.", "마지막 evidence 결과를 확인합니다.", "/evidence last", ("/evidence last",), "evidence_last", R.DIAGNOSTIC.value, side_effect="read-only"),
        _spec("/evidence explain", C.EVIDENCE.value, "근거 사용법을 설명합니다.", "evidence 흐름과 제약을 설명합니다.", "/evidence explain", ("/evidence explain",), "evidence_explain", R.DIAGNOSTIC.value, side_effect="read-only"),
        _spec("/use-evidence", C.EVIDENCE.value, "evidence pack을 선택합니다.", "검색된 evidence를 현재 작업 근거로 선택합니다.", "/use-evidence <검색어>", ("/use-evidence v0.43.10",), "use_evidence", R.DIAGNOSTIC.value, side_effect="read-only", requires_argument=True),
        _spec("/use-evidence last", C.EVIDENCE.value, "최근 evidence를 선택합니다.", "마지막 evidence pack을 현재 근거로 선택합니다.", "/use-evidence last", ("/use-evidence last",), "use_evidence_last", R.DIAGNOSTIC.value, side_effect="read-only"),
        _spec("/evidence used", C.EVIDENCE.value, "사용 중인 근거를 봅니다.", "현재 선택된 evidence 상태를 확인합니다.", "/evidence used", ("/evidence used",), "evidence_used", R.DIAGNOSTIC.value, side_effect="read-only"),
        _spec("/grounded-summary", C.GROUNDED_WORKFLOWS.value, "근거 기반 요약을 만듭니다.", "선택된 evidence를 바탕으로 요약합니다.", "/grounded-summary <내용>", ("/grounded-summary 선택한 근거로 진행상황을 요약해줘",), "grounded_summary", R.ARTIFACT.value, provider="may use provider", side_effect="read-only", requires_argument=True, opens_provider=True),
        _spec("/grounded-todo", C.GROUNDED_WORKFLOWS.value, "근거 기반 TODO를 만듭니다.", "선택된 evidence에서 다음 액션을 뽑습니다.", "/grounded-todo <내용>", ("/grounded-todo 다음 액션",), "grounded_todo", R.ARTIFACT.value, provider="may use provider", side_effect="read-only", requires_argument=True, opens_provider=True),
        _spec("/grounded-memo", C.GROUNDED_WORKFLOWS.value, "근거 기반 메모를 만듭니다.", "근거를 반영한 업무 메모를 만듭니다.", "/grounded-memo <내용>", ("/grounded-memo 회의 메모",), "grounded_memo", R.ARTIFACT.value, provider="may use provider", side_effect="read-only", requires_argument=True, opens_provider=True),
        _spec("/grounded-decision", C.GROUNDED_WORKFLOWS.value, "근거 기반 판단을 정리합니다.", "근거 기반 decision brief를 만듭니다.", "/grounded-decision <질문>", ("/grounded-decision 진행 여부",), "grounded_decision", R.ARTIFACT.value, provider="may use provider", side_effect="read-only", requires_argument=True, opens_provider=True),
        _spec("/grounded-handoff", C.GROUNDED_WORKFLOWS.value, "근거 기반 handoff를 만듭니다.", "근거를 포함한 인수인계문을 작성합니다.", "/grounded-handoff <내용>", ("/grounded-handoff 다음 세션에 넘길 내용",), "grounded_handoff", R.ARTIFACT.value, provider="may use provider", side_effect="read-only", requires_argument=True, opens_provider=True),
        _spec("/grounding-check", C.GROUNDED_WORKFLOWS.value, "grounding 상태를 점검합니다.", "산출물이 evidence와 연결되는지 확인합니다.", "/grounding-check", ("/grounding-check",), "grounding_check", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/provider", C.STATUS_DIAGNOSTICS.value, "provider 상태를 봅니다.", "provider 설정 상태를 사용자용으로 확인합니다.", "/provider", ("/provider",), "provider", R.STATUS.value, side_effect="diagnostic"),
        _spec("/what-happened", C.STATUS_DIAGNOSTICS.value, "진행 상황을 진단합니다.", "현재 세션에서 무슨 일이 있었는지 요약합니다.", "/what-happened", ("/what-happened",), "what_happened", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/report", C.STATUS_DIAGNOSTICS.value, "진단 report를 봅니다.", "명시적인 report surface를 엽니다.", "/report", ("/report",), "report", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/trace", C.STATUS_DIAGNOSTICS.value, "trace 안내를 봅니다.", "TUI에서 가능한 trace/status 표면을 안내합니다.", "/trace", ("/trace",), "trace", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/run-report", C.STATUS_DIAGNOSTICS.value, "run report 안내를 봅니다.", "run-report 표면을 안내합니다.", "/run-report", ("/run-report",), "run_report", R.DIAGNOSTIC.value, side_effect="diagnostic"),
        _spec("/pilot status", C.PILOT_RELEASE.value, "pilot 상태를 봅니다.", "v0.43 pilot 상태를 확인합니다.", "/pilot status", ("/pilot status",), "pilot_status", R.DIAGNOSTIC.value),
        _spec("/pilot score", C.PILOT_RELEASE.value, "pilot 점수를 봅니다.", "v0.43 pilot score를 확인합니다.", "/pilot score", ("/pilot score",), "pilot_score", R.DIAGNOSTIC.value),
        _spec("/pilot findings", C.PILOT_RELEASE.value, "pilot findings를 봅니다.", "pilot review findings를 확인합니다.", "/pilot findings", ("/pilot findings",), "pilot_findings", R.DIAGNOSTIC.value),
        _spec("/pilot review", C.PILOT_RELEASE.value, "pilot review를 봅니다.", "pilot review surface를 엽니다.", "/pilot review", ("/pilot review",), "pilot_review", R.DIAGNOSTIC.value),
        _spec("/pilot next", C.PILOT_RELEASE.value, "다음 track을 봅니다.", "다음 권장 track을 확인합니다.", "/pilot next", ("/pilot next",), "pilot_next", R.DIAGNOSTIC.value),
        _spec("/pilot report", C.PILOT_RELEASE.value, "pilot report를 봅니다.", "pilot report surface를 엽니다.", "/pilot report", ("/pilot report",), "pilot_report", R.DIAGNOSTIC.value),
        _spec("/acceptance", C.PILOT_RELEASE.value, "acceptance를 봅니다.", "acceptance checklist를 확인합니다.", "/acceptance", ("/acceptance",), "acceptance", R.STATUS.value),
        _spec("/workflow score", C.PILOT_RELEASE.value, "workflow 점수를 봅니다.", "workflow score를 확인합니다.", "/workflow score", ("/workflow score",), "workflow_score", R.STATUS.value),
        _spec("/polish status", C.PILOT_RELEASE.value, "polish 상태를 봅니다.", "pilot polish 상태를 확인합니다.", "/polish status", ("/polish status",), "polish_status", R.DIAGNOSTIC.value),
        _spec("/polish findings", C.PILOT_RELEASE.value, "polish findings를 봅니다.", "polish findings를 확인합니다.", "/polish findings", ("/polish findings",), "polish_findings", R.DIAGNOSTIC.value),
        _spec("/polish report", C.PILOT_RELEASE.value, "polish report를 봅니다.", "polish report surface를 엽니다.", "/polish report", ("/polish report",), "polish_report", R.DIAGNOSTIC.value),
        _spec("/pilot close", C.PILOT_RELEASE.value, "pilot closure를 봅니다.", "pilot closure 평가를 확인합니다.", "/pilot close", ("/pilot close",), "pilot_close", R.DIAGNOSTIC.value),
        _spec("/v044 readiness", C.STATUS_DIAGNOSTICS.value, "v0.44 준비도를 봅니다.", "v0.44 gate readiness를 확인합니다.", "/v044 readiness", ("/v044 readiness",), "v044_readiness", R.STATUS.value, side_effect="diagnostic"),
        _spec("/v044 scope", C.PILOT_RELEASE.value, "v0.44 scope를 봅니다.", "v0.44 controlled workspace read scope를 확인합니다.", "/v044 scope", ("/v044 scope",), "v044_scope", R.DIAGNOSTIC.value),
        _spec("/v044 risks", C.PILOT_RELEASE.value, "v0.44 risks를 봅니다.", "v0.44 진입 위험을 확인합니다.", "/v044 risks", ("/v044 risks",), "v044_risks", R.DIAGNOSTIC.value),
        _spec("/v044 handoff", C.PILOT_RELEASE.value, "v0.44 handoff를 봅니다.", "v0.44 handoff를 확인합니다.", "/v044 handoff", ("/v044 handoff",), "v044_handoff", R.DIAGNOSTIC.value),
        _spec("/help tui", C.TUI.value, "TUI 사용법을 봅니다.", "입력, palette, modal, snapshot 사용법을 봅니다.", "/help tui", ("/help tui",), "help_tui", R.MODAL.value),
        _spec("/help examples", C.TUI.value, "예시를 봅니다.", "실제 업무 입력 예시를 봅니다.", "/help examples", ("/help examples",), "help_examples", R.MODAL.value),
        _spec("/lobby", C.TUI.value, "lobby를 명시적으로 봅니다.", "시작 안내를 다시 보고 싶을 때 사용합니다.", "/lobby", ("/lobby",), "lobby", R.STATUS.value),
        _spec("/refresh", C.TUI.value, "화면을 새로고칩니다.", "TUI chrome을 명시적으로 새로고칩니다.", "/refresh", ("/refresh",), "refresh", R.STATUS.value, availability=A.PREVIEW.value),
        _spec("/clear", C.TUI.value, "현재 transcript를 정리합니다.", "화면 transcript를 정리하는 preview 명령입니다.", "/clear", ("/clear",), "clear", R.STATUS.value, availability=A.PREVIEW.value),
        _spec("/help safety", C.SAFETY.value, "닫힌 기능을 봅니다.", "현재 닫힌 고위험 capability를 사용자 언어로 설명합니다.", "/help safety", ("/help safety",), "help_safety", R.MODAL.value),
    )


def list_v043111_command_specs(prefix: str = "/", max_items: int | None = None) -> tuple[V043111CommandSpec, ...]:
    specs = create_v043111_command_registry()
    normalized = " ".join(prefix.strip().split()).lower() if prefix else "/"
    if normalized in {"", "/"}:
        result = specs
    elif normalized == "/s":
        matches = tuple(spec for spec in specs if spec.command.startswith(normalized) or any(alias.startswith(normalized) for alias in spec.aliases))
        result = tuple(sorted(matches, key=lambda spec: (0 if spec.command == "/summary" else 1, spec.command)))
    elif normalized in {"/sta", "/stat", "/status"}:
        result = tuple(spec for spec in specs if spec.command.startswith("/status") or spec.category == V043111CommandCategory.STATUS_DIAGNOSTICS.value)
    elif normalized.startswith("/grounded"):
        result = tuple(spec for spec in specs if spec.command.startswith(normalized) or spec.category == V043111CommandCategory.GROUNDED_WORKFLOWS.value)
    elif normalized.startswith("/help"):
        result = tuple(spec for spec in specs if spec.command.startswith(normalized) or spec.command.startswith("/help"))
    else:
        result = tuple(
            spec
            for spec in specs
            if spec.command.startswith(normalized) or any(alias.startswith(normalized) for alias in spec.aliases)
        )
    return result[:max_items] if max_items is not None else result


def list_v043111_command_names(prefix: str = "/", max_items: int | None = None) -> tuple[str, ...]:
    return tuple(spec.command for spec in list_v043111_command_specs(prefix, max_items))


def find_v043111_command_spec(input_text: str) -> V043111CommandSpec | None:
    normalized = " ".join(input_text.strip().split()).lower()
    if not normalized.startswith("/"):
        return None
    all_specs = sorted(create_v043111_command_registry(), key=lambda spec: len(spec.command), reverse=True)
    for spec in all_specs:
        command = spec.command.lower()
        candidates = (command, *(alias.lower() for alias in spec.aliases))
        for candidate in candidates:
            if normalized == candidate or normalized.startswith(candidate + " "):
                return spec
    return None


def extract_v043111_command_argument(input_text: str, spec: V043111CommandSpec) -> str:
    normalized_command = spec.command
    raw = input_text.strip()
    if raw.lower().startswith(normalized_command.lower()):
        return raw[len(normalized_command) :].strip()
    for alias in spec.aliases:
        if raw.lower().startswith(alias.lower()):
            return raw[len(alias) :].strip()
    return ""


def render_v043111_usage_text(spec: V043111CommandSpec) -> str:
    example = spec.examples[0] if spec.examples else spec.usage
    return "\n".join(("Usage", spec.usage, "", "예:", f"  {example}"))


def group_v043111_command_specs(specs: Iterable[V043111CommandSpec] | None = None) -> dict[str, tuple[V043111CommandSpec, ...]]:
    grouped: dict[str, list[V043111CommandSpec]] = {}
    for spec in specs or create_v043111_command_registry():
        grouped.setdefault(spec.category, []).append(spec)
    return {key: tuple(value) for key, value in grouped.items()}


def render_v043111_palette_text(prefix: str = "/", max_items: int = 200) -> str:
    specs = list_v043111_command_specs(prefix, max_items)
    grouped = group_v043111_command_specs(specs)
    lines = ["Commands"]
    for category in (category.value for category in V043111CommandCategory):
        items = grouped.get(category, ())
        if not items:
            continue
        lines.append(category)
        for index, spec in enumerate(items):
            marker = ">" if len(lines) == 2 and index == 0 else " "
            label = f" [{spec.availability}]" if spec.availability != V043111CommandAvailability.AVAILABLE.value else ""
            lines.append(f"{marker} {spec.usage:<26} {spec.short_description_ko}{label}")
    return "\n".join(lines)


def list_v0439_palette_commands(prefix: str = "/", max_items: int | None = None) -> tuple[str, ...]:
    return list_v043111_command_names(prefix, max_items)


def list_v04310_shared_command_names(prefix: str = "/", max_items: int | None = None) -> tuple[str, ...]:
    return list_v043111_command_names(prefix, max_items)


def create_v0439_command_registry_reuse_report(prefix: str = "/", max_items: int | None = None, **overrides: Any) -> V0439CommandRegistryReuseReport:
    defaults = {
        "report_id": "v0439-command-registry-reuse-report",
        "source_registry": "v0.43.8.2 slash command registry",
        "deterministic": True,
        "commands": list_v043111_command_names(prefix, max_items),
        "command_executed": False,
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439CommandRegistryReuseReport(**defaults)


__all__ = [
    "V043111CommandAvailability",
    "V043111RendererKind",
    "V043111CommandCategory",
    "V043111CommandSpec",
    "V0439CommandRegistryReuseReport",
    "create_v043111_command_registry",
    "list_v043111_command_specs",
    "list_v043111_command_names",
    "find_v043111_command_spec",
    "extract_v043111_command_argument",
    "render_v043111_usage_text",
    "group_v043111_command_specs",
    "render_v043111_palette_text",
    "list_v0439_palette_commands",
    "list_v04310_shared_command_names",
    "create_v0439_command_registry_reuse_report",
]
