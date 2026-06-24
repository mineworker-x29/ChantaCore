"""Bounded RuntimeAdapter contract for Schumpeter TUI snapshots and preview."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable


@dataclass(frozen=True)
class V0439RuntimeAdapterPolicy:
    policy_id: str
    provider_completion_allowed: bool
    prompt_submission_allowed: bool
    shell_execution_allowed: bool
    git_execution_allowed: bool
    repo_search_allowed: bool
    workspace_read_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    unavailable_sources_return_unknown: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439RuntimeSnapshot:
    snapshot_id: str
    product_name: str
    profile_id: str
    provider_label: str
    mode_label: str
    working_directory_label: str | None
    project_label: str | None
    session_label: str | None
    pi_status: str
    provider_status: str
    trace_status: str
    evidence_status: str
    safety_status: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    git_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


@dataclass(frozen=True)
class V043115TUIProviderContext:
    profile_id: str
    home_path: str
    provider_mode: str
    configured_provider_available: bool
    provider_label: str
    configured_model: str | None
    provider_status_source: str
    provider_resolution_error: str | None
    timeout_seconds: float | None
    uses_same_resolver_as_cli_run: bool
    provider_invoked: bool
    prompt_submitted: bool
    production_certified: bool


def create_v0439_runtime_adapter_policy(**overrides: Any) -> V0439RuntimeAdapterPolicy:
    defaults = {
        "policy_id": "v0439-runtime-adapter-policy",
        "provider_completion_allowed": False,
        "prompt_submission_allowed": False,
        "shell_execution_allowed": False,
        "git_execution_allowed": False,
        "repo_search_allowed": False,
        "workspace_read_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "unavailable_sources_return_unknown": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439RuntimeAdapterPolicy(**defaults)


def create_v0439_runtime_snapshot(**overrides: Any) -> V0439RuntimeSnapshot:
    defaults = {
        "snapshot_id": "v0439-runtime-snapshot",
        "product_name": "Schumpeter",
        "profile_id": "default-personal",
        "provider_label": "configured",
        "mode_label": "Work Session",
        "working_directory_label": "D:\\...\\ChantaCore",
        "project_label": "Schumpeter v0.43",
        "session_label": "structured TUI contract",
        "pi_status": "ok",
        "provider_status": "ok",
        "trace_status": "active",
        "evidence_status": "none",
        "safety_status": "closed",
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "git_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439RuntimeSnapshot(**defaults)


def collect_v0439_runtime_snapshot(**overrides: Any) -> V0439RuntimeSnapshot:
    policy = create_v0439_runtime_adapter_policy()
    fallback = "unknown" if policy.unavailable_sources_return_unknown else None
    defaults: dict[str, Any] = {
        "project_label": overrides.pop("project_label", "Schumpeter v0.43"),
        "session_label": overrides.pop("session_label", "structured TUI contract"),
        "working_directory_label": overrides.pop("working_directory_label", "D:\\...\\ChantaCore"),
    }
    for key in ("pi_status", "provider_status", "trace_status", "evidence_status", "safety_status"):
        if key not in overrides:
            defaults[key] = {
                "pi_status": "ok",
                "provider_status": "ok",
                "trace_status": "active",
                "evidence_status": "none",
                "safety_status": "closed",
            }.get(key, fallback)
    defaults.update(overrides)
    return create_v0439_runtime_snapshot(**defaults)


@dataclass(frozen=True)
class V04310RuntimeAdapterPolicy:
    policy_id: str
    render_collect_snapshot_side_effect_free: bool
    component_direct_runtime_access_allowed: bool
    provider_completion_from_rendering_allowed: bool
    prompt_submission_from_rendering_allowed: bool
    shell_execution_allowed: bool
    git_execution_allowed: bool
    repo_search_allowed: bool
    workspace_read_allowed: bool
    memory_mutation_allowed: bool
    core_memory_write_allowed: bool
    production_certified: bool


@dataclass(frozen=True)
class V04310RuntimeSnapshot:
    snapshot_id: str
    product_name: str
    profile_id: str
    provider_label: str
    mode_label: str
    working_directory_label: str | None
    session_label: str | None
    pi_status: str
    provider_status: str
    trace_status: str
    evidence_status: str
    safety_status: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    git_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    core_memory_written: bool
    production_certified: bool


def create_v04310_runtime_adapter_policy(**overrides: Any) -> V04310RuntimeAdapterPolicy:
    defaults = {
        "policy_id": "v04310-runtime-adapter-policy",
        "render_collect_snapshot_side_effect_free": True,
        "component_direct_runtime_access_allowed": False,
        "provider_completion_from_rendering_allowed": False,
        "prompt_submission_from_rendering_allowed": False,
        "shell_execution_allowed": False,
        "git_execution_allowed": False,
        "repo_search_allowed": False,
        "workspace_read_allowed": False,
        "memory_mutation_allowed": False,
        "core_memory_write_allowed": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310RuntimeAdapterPolicy(**defaults)


def create_v04310_runtime_snapshot(**overrides: Any) -> V04310RuntimeSnapshot:
    defaults = {
        "snapshot_id": "v04310-runtime-snapshot",
        "product_name": "Schumpeter",
        "profile_id": "default-personal",
        "provider_label": "configured",
        "mode_label": "Work Session",
        "working_directory_label": "D:\\...\\ChantaCore",
        "session_label": "structured TUI MVP",
        "pi_status": "ok",
        "provider_status": "ok",
        "trace_status": "active",
        "evidence_status": "none",
        "safety_status": "closed",
        "provider_invoked": False,
        "prompt_submitted": False,
        "shell_executed": False,
        "git_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated": False,
        "core_memory_written": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310RuntimeSnapshot(**defaults)


def collect_v04310_runtime_snapshot(**overrides: Any) -> V04310RuntimeSnapshot:
    return create_v04310_runtime_snapshot(**overrides)


def create_v043115_tui_provider_context(
    profile_id: str = "default-personal",
    home_path: str | None = None,
    provider: str | None = None,
    timeout_seconds: float | None = 120,
    **overrides: Any,
) -> V043115TUIProviderContext:
    from chanta_core.personal_runtime.default_personal_home_quickstart import (
        create_v042_home_resolution_request,
        resolve_v042_home,
    )
    from chanta_core.personal_runtime.default_personal_provider_setup import (
        create_v042_provider_status_report,
        create_v042_provider_status_request,
    )

    resolved = resolve_v042_home(
        create_v042_home_resolution_request(
            explicit_home=home_path,
            command_name="run",
            allow_create=False,
        )
    )
    resolved_home = resolved.home_path or ""
    report = create_v042_provider_status_report(
        create_v042_provider_status_request(resolved_home, profile_id)
    )
    requested = (provider or "auto").strip().lower()
    configured_available = bool(report.ready_for_configured_provider_run)
    if requested in {"configured", "mock"}:
        provider_mode = requested
    elif configured_available:
        provider_mode = "configured"
    else:
        provider_mode = "unavailable"
    label = "configured" if provider_mode == "configured" and configured_available else provider_mode
    error = None
    if not resolved.safe_to_use:
        error = resolved.message
    elif provider_mode == "configured" and not configured_available:
        error = report.next_action
    defaults = {
        "profile_id": profile_id,
        "home_path": resolved_home,
        "provider_mode": provider_mode,
        "configured_provider_available": configured_available,
        "provider_label": label,
        "configured_model": report.model,
        "provider_status_source": "v042_home_resolver_and_provider_status",
        "provider_resolution_error": error,
        "timeout_seconds": timeout_seconds,
        "uses_same_resolver_as_cli_run": True,
        "provider_invoked": False,
        "prompt_submitted": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V043115TUIProviderContext(**defaults)


def _render_v04310_product_surface_text(text: str) -> str:
    return text.replace(
        "저는 ChantaCore default-personal runtime에서 동작하는 업무 보조 에이전트입니다.",
        "저는 Schumpeter입니다. Process Intelligence-native Work Agent로서 업무 세션을 돕습니다.",
    ).replace(
        "ChantaCore default-personal runtime",
        "Schumpeter",
    ).replace(
        "ChantaCore default-personal",
        "Schumpeter",
    ).replace(
        "base_url",
        "provider endpoint",
    ).replace(
        "api_key",
        "provider credential",
    ).replace(
        "현재는 저장소 직접 읽기, 파일 수정, 셸 실행, repo search는 열려 있지 않습니다.",
        "Safety: protected.",
    ).replace(
        "workspace read, repo search, shell, edit/apply, subagents, memory mutation, and production certification remain closed",
        "high-risk actions closed",
    )


def _v043102_command_payload(input_text: str) -> str:
    from chanta_core.schumpeter_tui.command_registry import extract_v043111_command_argument, find_v043111_command_spec

    spec = find_v043111_command_spec(input_text)
    if spec is not None:
        return extract_v043111_command_argument(input_text, spec)
    parts = input_text.strip().split(maxsplit=1)
    return parts[1].strip() if len(parts) > 1 else ""


def _render_v043102_help() -> str:
    from chanta_core.schumpeter_tui.help_surface import render_v04310_help

    return render_v04310_help("/help").rendered_text


def _render_v043102_status() -> str:
    return "\n".join(
        (
            "Schumpeter status",
            "PI: ok",
            "Provider: configured",
            "Trace: active",
            "Evidence: none",
            "Safety: protected",
        )
    )


def _render_v043102_status_debug() -> str:
    return "\n".join(
        (
            "Schumpeter debug status",
            "Closed capability matrix:",
            "- workspace read: closed",
            "- repo search: closed",
            "- shell/git: closed",
            "- edit/apply: closed",
            "- subagents: closed",
            "- memory mutation: closed",
            "- production certification: false",
        )
    )


def _render_v043102_artifact(input_text: str) -> str:
    payload = _v043102_command_payload(input_text)
    heading = "TUI artifact"
    command = input_text.strip().split(maxsplit=1)[0].lower()
    if command == "/summary":
        heading = "Summary"
    elif command == "/todo":
        heading = "TODO"
    elif command == "/memo":
        heading = "Memo"
    elif command == "/decision":
        heading = "Decision"
    elif command == "/handoff":
        heading = "Handoff"
    return "\n".join(
        (
            heading,
            f"- {payload}",
        )
    )


def _render_v043102_diagnostic() -> str:
    return "\n".join(
        (
            "TUI diagnostic",
            "- Command routed through the Schumpeter TUI diagnostic surface.",
            "- Static chrome was not redrawn for this turn.",
            "- Rendering stayed display-only.",
        )
    )


def _render_v043102_diagnostic_debug() -> str:
    return "\n".join(
        (
            "TUI diagnostic debug",
            "- route: diagnostic",
            "- provider invoked by rendering: false",
            "- shell/git from rendering: false",
            "- repo/workspace read from rendering: false",
            "- memory mutation from rendering: false",
        )
    )


def _render_v043102_lobby() -> str:
    return "\n".join(
        (
            "Lobby",
            "Schumpeter",
            "Process Intelligence-native Work Agent",
            "Use /help for commands, /status for concise status, and /exit to leave.",
        )
    )


def _render_v043102_routed_command(input_text: str, renderer_kind: str) -> str:
    if renderer_kind == "help":
        from chanta_core.schumpeter_tui.help_surface import render_v04310_help

        return render_v04310_help(input_text).rendered_text
    if renderer_kind == "status":
        return _render_v043102_status()
    if renderer_kind == "debug_status":
        return _render_v043102_status_debug()
    if renderer_kind == "artifact":
        return _render_v043102_artifact(input_text)
    if renderer_kind == "diagnostic":
        return _render_v043102_diagnostic()
    if renderer_kind == "debug_diagnostic":
        return _render_v043102_diagnostic_debug()
    if renderer_kind == "lobby":
        return _render_v043102_lobby()
    if renderer_kind == "message" and input_text.strip().lower() in {"/exit", "/quit"}:
        return "Schumpeter session closed."
    return ""


def _render_v043111_usage_error(input_text: str) -> str:
    from chanta_core.schumpeter_tui.command_registry import find_v043111_command_spec, render_v043111_usage_text

    spec = find_v043111_command_spec(input_text)
    if spec is None:
        return "Usage\n/help commands\n\n예:\n  /help commands"
    return render_v043111_usage_text(spec)


def _render_v043111_unavailable(spec_command: str) -> str:
    return "\n".join(
        (
            "Unavailable",
            f"{spec_command} 명령은 현재 TUI 모드에서 아직 열리지 않았습니다.",
            "현재 사용 가능한 표면은 /help commands, /status, /what-happened 입니다.",
        )
    )


def _render_v043111_trace_guidance() -> str:
    return "\n".join(
        (
            "Trace guidance",
            "현재 TUI는 OCEL/log 파일을 직접 읽지 않습니다.",
            "사용 가능한 진단 표면:",
            "- /what-happened",
            "- /trace",
            "- /run-report",
            "- /status",
        )
    )


def _render_v043111_repository_boundary() -> str:
    return "\n".join(
        (
            "Repository boundary",
            "현재 TUI는 저장소 파일이나 git 상태를 직접 검사하지 않습니다.",
            "저장소 직접 읽기는 v0.44 Controlled Workspace Read gate 이후 별도 설계로 열어야 합니다.",
            "현재 가능한 점검: /status, /what-happened, /trace, /run-report",
        )
    )


def _render_v043111_capability_answer() -> str:
    return "\n".join(
        (
            "Schumpeter capabilities",
            "- 업무 요약, TODO, 메모, 의사결정, 인수인계 산출물 작성",
            "- local note와 evidence 표면 안내",
            "- PI/provider/trace/evidence/safety 상태 확인",
            "- v0.44 readiness와 handoff 점검",
            "닫힌 기능: 저장소 직접 읽기, repo search, shell/git, file edit/apply, subagent, persistent memory promotion",
        )
    )


def _new_v043114_run_id() -> str:
    return f"tui-run-{datetime.now(UTC).strftime('%Y%m%d%H%M%S%f')}"


def _preview_v043114(text: str | None, limit: int = 160) -> str | None:
    if text is None:
        return None
    normalized = " ".join(text.split())
    return normalized if len(normalized) <= limit else normalized[: limit - 3] + "..."


def _render_v043114_provider_error(error_class: str | None = None, status_was_configured: bool = False) -> str:
    detail = f" ({error_class})" if error_class else ""
    if status_was_configured:
        return "\n".join(
            (
                "Provider unavailable",
                "The configured provider was available in status, but the run failed during invocation.",
                "",
                "Try:",
                "- /provider",
                "- chanta-cli provider connectivity",
            )
        )
    return "\n".join(
        (
            "Provider unavailable",
            f"Schumpeter could not reach the configured provider{detail}.",
            "",
            "Try:",
            "- /provider",
            "- chanta-cli provider connectivity",
        )
    )


def _looks_like_v043114_identity_question(text: str) -> bool:
    lowered = text.strip().lower()
    return any(token in lowered for token in ("넌 누구", "너는 누구", "정체", "who are you", "what are you"))


def _render_v043114_identity_answer() -> str:
    return "\n".join(
        (
            "저는 Schumpeter입니다.",
            "Process Intelligence-native Work Agent로서 업무 대화, 산출물 작성, 상태/근거 확인을 돕습니다.",
            "내부 구현 lineage는 ChantaCore이지만 기본 제품 표면은 Schumpeter입니다.",
        )
    )


def _emit_v043114_run_report_trace(profile_id: str, home_path: str, run_id: str, command_input: Any, result: Any) -> None:
    from chanta_core.personal_runtime.default_personal_trace_report import (
        _run_events_from_result,
        append_runtime_events,
        create_trace_store_config,
    )

    config = create_trace_store_config(profile_id, home_path)
    append_runtime_events(_run_events_from_result(run_id, command_input, result), config)


def _render_v043111_registered_command_response(input_text: str, spec: Any) -> tuple[str, str, str]:
    command = spec.command
    argument = _v043102_command_payload(input_text)
    if command == "/about":
        return (
            "about",
            "status",
            "Schumpeter\nProcess Intelligence-native Work Agent\n\nProduct surface: Schumpeter\nRuntime lineage: ChantaCore\nCLI compatibility: chanta-cli",
        )
    if command == "/capabilities":
        return ("capability_question", "status", _render_v043111_capability_answer())
    if command in {"/trace", "/run-report"}:
        return ("trace_or_evidence_status_request", "diagnostic", _render_v043111_trace_guidance())
    if command == "/provider":
        return ("provider_status", "status", "Provider\nProvider: configured\nSafety: protected")
    if command.startswith("/v044"):
        return (
            "release_status",
            "status",
            "v0.44 gate\n현재 v0.44는 Controlled Workspace Read 설계 gate 이후 검토해야 합니다.\nSafety: protected",
        )
    if command in {"/recall", "/evidence", "/evidence sources", "/evidence last", "/evidence explain", "/use-evidence", "/use-evidence last", "/evidence used"}:
        query = f"\nQuery: {argument}" if argument else ""
        return (
            "evidence_guidance",
            "diagnostic",
            f"Evidence guidance{query}\n현재 TUI는 evidence/status 표면을 안내합니다.\n상세 확인: /evidence explain, /what-happened, /status",
        )
    if command.startswith("/grounded-") or command == "/grounding-check":
        return (
            "grounded_guidance",
            "diagnostic" if command == "/grounding-check" else "artifact",
            f"Grounded workflow\n{argument or '선택된 evidence가 필요합니다. 먼저 /use-evidence <검색어>를 실행하세요.'}",
        )
    if spec.renderer_kind == "artifact":
        return ("slash_command", "artifact", _render_v043102_artifact(input_text))
    if spec.renderer_kind == "status":
        return (
            "slash_command",
            "status",
            f"{command}\n{spec.long_description_ko}\nmode: {spec.provider_policy_label}, {spec.side_effect_label}",
        )
    if spec.renderer_kind == "diagnostic":
        return (
            "slash_command",
            "diagnostic",
            f"{command}\n{spec.long_description_ko}\nmode: {spec.provider_policy_label}, {spec.side_effect_label}",
        )
    return ("slash_command", "status", f"{command}\n{spec.long_description_ko}")


def _classify_v043111_natural_language(text: str) -> tuple[str, str, str] | None:
    lowered = text.strip().lower()
    if _looks_like_v043114_identity_question(text):
        return ("identity_question", "assistant", _render_v043114_identity_answer())
    capability_tokens = ("할 줄", "뭘 할", "무엇을 할", "가능한", "capabilit")
    trace_tokens = ("ocel", "로그", "log", "trace", "run-report", "실행 기록")
    repository_tokens = ("저장소", "repository", "repo", "git")
    if any(token in lowered for token in capability_tokens):
        return ("capability_question", "status", _render_v043111_capability_answer())
    if any(token in lowered for token in trace_tokens) and any(token in lowered for token in ("확인", "봐", "보여", "점검", "check", "확인해")):
        return ("trace_or_evidence_status_request", "diagnostic", _render_v043111_trace_guidance())
    if any(token in lowered for token in repository_tokens) and any(token in lowered for token in ("상태", "확인", "점검", "check")):
        return ("repository_status_request", "status", _render_v043111_repository_boundary())
    return None


class V04310RuntimeAdapter:
    """Bounded bridge between the TUI preview and existing work-session logic."""

    def __init__(
        self,
        profile_id: str = "default-personal",
        home_path: str | None = None,
        provider: str | None = None,
        run_service: Callable[[Any], Any] | None = None,
        emit_run_report_trace: bool = True,
        timeout_seconds: float | None = 120,
    ):
        self.profile_id = profile_id
        self.home_path = home_path
        self.provider = provider
        self.timeout_seconds = timeout_seconds
        self.run_service = run_service
        self.emit_run_report_trace = emit_run_report_trace
        self.provider_context = create_v043115_tui_provider_context(profile_id, home_path, provider, timeout_seconds)
        self.closed = False
        from chanta_core.personal_runtime.default_personal_work_session import create_v043_work_session_state

        self.work_state = create_v043_work_session_state(
            profile_id=self.provider_context.profile_id,
            home_path=self.provider_context.home_path,
            provider=self.provider_context.provider_mode,
        )

    def collect_ui_snapshot(self) -> V04310RuntimeSnapshot:
        return collect_v04310_runtime_snapshot(
            profile_id=self.work_state.profile_id,
            provider_label=self.provider_context.provider_label,
            session_label=self.work_state.session_id,
        )

    def render_provider_status_card(self) -> str:
        context = self.provider_context
        status = "configured" if context.configured_provider_available else "unavailable"
        model = context.configured_model or "unknown"
        return "\n".join(
            (
                "Provider",
                f"Status: {status}",
                f"Mode: {context.provider_mode}",
                f"Model: {model}",
                f"Home: {context.home_path}",
                "Resolver: CLI run",
                "Safety: protected",
            )
        )

    def _submit_provider_backed_general_chat(self, text: str):
        from chanta_core.personal_runtime.default_personal_run import RunCommandInput, execute_run_command
        from chanta_core.schumpeter_tui.app_state import create_v04310_tui_turn_result

        context = self.provider_context
        if context.provider_mode == "unavailable" or (context.provider_mode == "configured" and not context.configured_provider_available):
            return create_v04310_tui_turn_result(
                input_text=text,
                route_kind="provider_error",
                rendered_text=_render_v043114_provider_error("configured_provider_unavailable"),
                message_kind="error",
                provider_invoked=False,
                prompt_submitted=False,
                shell_executed=False,
                git_executed=False,
                repo_search_used=False,
                workspace_read_opened=False,
                tool_calling_used=False,
                function_calling_used=False,
                subagent_invoked=False,
                memory_mutated=False,
                core_memory_written=False,
            )
        provider_mode = context.provider_mode
        command_input = RunCommandInput(
            profile_id=context.profile_id,
            home_path=context.home_path,
            user_input=text,
            session_id=self.work_state.session_id,
            provider=provider_mode,
            mock_provider=provider_mode == "mock",
            timeout_seconds=context.timeout_seconds,
        )
        run_service = self.run_service or execute_run_command
        try:
            result = run_service(command_input)
        except Exception:
            return create_v04310_tui_turn_result(
                input_text=text,
                route_kind="provider_error",
                rendered_text=_render_v043114_provider_error("runtime_exception"),
                message_kind="error",
                provider_invoked=False,
                prompt_submitted=False,
                shell_executed=False,
                git_executed=False,
                repo_search_used=False,
                workspace_read_opened=False,
                tool_calling_used=False,
                function_calling_used=False,
                subagent_invoked=False,
                memory_mutated=False,
                core_memory_written=False,
            )

        run_result = result.run_result
        provider_response = run_result.provider_response
        run_id = _new_v043114_run_id()
        if self.emit_run_report_trace:
            try:
                _emit_v043114_run_report_trace(context.profile_id, context.home_path, run_id, command_input, result)
            except Exception:
                pass
        response_parse_status = provider_response.response_parse_status if provider_response else None
        response_error_class = provider_response.error_class if provider_response else None
        provider_model = provider_response.provider_model if provider_response else None
        assistant_text = provider_response.text if provider_response and provider_response.text.strip() else run_result.assistant_text
        if result.status != "success" or not assistant_text.strip():
            error_class = response_error_class or result.status or "provider_error"
            status_was_configured = context.configured_provider_available and error_class in {"provider_not_configured", "provider_unavailable"}
            return create_v04310_tui_turn_result(
                input_text=text,
                route_kind="provider_error",
                rendered_text=_render_v043114_provider_error(error_class, status_was_configured=status_was_configured),
                message_kind="error",
                run_id=run_id,
                session_id=run_result.session_id,
                response_parse_status=response_parse_status,
                response_error_class=error_class,
                provider_model=provider_model,
                assistant_response_preview=_preview_v043114(assistant_text),
                provider_invoked=result.provider_invoked,
                prompt_submitted=result.prompt_submitted,
                shell_executed=run_result.shell_executed,
                git_executed=False,
                repo_search_used=False,
                workspace_read_opened=False,
                tool_calling_used=False,
                function_calling_used=False,
                subagent_invoked=run_result.subagent_invoked,
                memory_mutated=False,
                core_memory_written=False,
            )
        return create_v04310_tui_turn_result(
            input_text=text,
            route_kind="general_chat",
            rendered_text=assistant_text.strip(),
            message_kind="assistant",
            run_id=run_id,
            session_id=run_result.session_id,
            response_parse_status=response_parse_status,
            response_error_class=response_error_class,
            provider_model=provider_model,
            assistant_response_preview=_preview_v043114(assistant_text),
            provider_invoked=result.provider_invoked,
            prompt_submitted=result.prompt_submitted,
            shell_executed=run_result.shell_executed,
            git_executed=False,
            repo_search_used=False,
            workspace_read_opened=False,
            tool_calling_used=False,
            function_calling_used=False,
            subagent_invoked=run_result.subagent_invoked,
            memory_mutated=False,
            core_memory_written=False,
        )

    def submit_user_input(self, text: str):
        from chanta_core.schumpeter_tui.app_state import create_v04310_tui_turn_result
        from chanta_core.schumpeter_tui.command_registry import (
            V043111CommandAvailability,
            extract_v043111_command_argument,
            find_v043111_command_spec,
        )
        from chanta_core.schumpeter_tui.turn_dispatch import resolve_v043102_tui_command_route

        natural_route = _classify_v043111_natural_language(text)
        if natural_route is not None:
            route_kind, message_kind, rendered_text = natural_route
            return create_v04310_tui_turn_result(
                input_text=text,
                route_kind=route_kind,
                rendered_text=rendered_text,
                message_kind=message_kind,
                provider_invoked=False,
                prompt_submitted=False,
                shell_executed=False,
                git_executed=False,
                repo_search_used=False,
                workspace_read_opened=False,
                memory_mutated=False,
                core_memory_written=False,
            )

        spec = find_v043111_command_spec(text)
        if spec is not None:
            argument = extract_v043111_command_argument(text, spec)
            if spec.requires_argument and not argument:
                return create_v04310_tui_turn_result(
                    input_text=text,
                    route_kind="usage_error",
                    rendered_text=_render_v043111_usage_error(text),
                    message_kind="error",
                    provider_invoked=False,
                    prompt_submitted=False,
                    shell_executed=False,
                    git_executed=False,
                    repo_search_used=False,
                    workspace_read_opened=False,
                    memory_mutated=False,
                    core_memory_written=False,
                )
            if spec.availability in {V043111CommandAvailability.NOT_OPENED.value, V043111CommandAvailability.PREVIEW.value}:
                return create_v04310_tui_turn_result(
                    input_text=text,
                    route_kind="not_opened",
                    rendered_text=_render_v043111_unavailable(spec.command),
                    message_kind="error",
                    provider_invoked=False,
                    prompt_submitted=False,
                    shell_executed=False,
                    git_executed=False,
                    repo_search_used=False,
                    workspace_read_opened=False,
                    memory_mutated=False,
                    core_memory_written=False,
                )
            if spec.command == "/provider":
                return create_v04310_tui_turn_result(
                    input_text=text,
                    route_kind="provider_status",
                    rendered_text=self.render_provider_status_card(),
                    message_kind="status",
                    provider_invoked=False,
                    prompt_submitted=False,
                    shell_executed=False,
                    git_executed=False,
                    repo_search_used=False,
                    workspace_read_opened=False,
                    memory_mutated=False,
                    core_memory_written=False,
                )

        route_spec = resolve_v043102_tui_command_route(text)
        if route_spec is not None:
            if route_spec.route_kind == "exit":
                self.closed = True
            return create_v04310_tui_turn_result(
                input_text=text,
                route_kind=route_spec.route_kind,
                rendered_text=_render_v043102_routed_command(text, route_spec.renderer_kind),
                message_kind=route_spec.message_kind,
                provider_invoked=False,
                prompt_submitted=False,
                shell_executed=False,
                git_executed=False,
                repo_search_used=False,
                workspace_read_opened=False,
                memory_mutated=False,
                core_memory_written=False,
            )

        if spec is not None:
            route_kind, message_kind, rendered_text = _render_v043111_registered_command_response(text, spec)
            return create_v04310_tui_turn_result(
                input_text=text,
                route_kind=route_kind,
                rendered_text=rendered_text,
                message_kind=message_kind,
                provider_invoked=False,
                prompt_submitted=False,
                shell_executed=False,
                git_executed=False,
                repo_search_used=False,
                workspace_read_opened=False,
                memory_mutated=False,
                core_memory_written=False,
            )

        return self._submit_provider_backed_general_chat(text)

    def execute_slash_command(self, command_text: str):
        return self.submit_user_input(command_text)

    def get_command_registry(self):
        from chanta_core.schumpeter_tui.command_registry import create_v0439_command_registry_reuse_report

        return create_v0439_command_registry_reuse_report("/")

    def close(self) -> None:
        self.closed = True


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("V04310") or name.startswith("create_v043") or name.startswith("collect_v043")]
