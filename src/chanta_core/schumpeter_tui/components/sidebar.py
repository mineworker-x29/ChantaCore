"""Sidebar component for Schumpeter v0.43.9."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from chanta_core.schumpeter_tui.state import V0439UIState


class V0439ComponentKind(StrEnum):
    SIDEBAR = "sidebar"
    HEADER = "header"
    CHAT_VIEW = "chat_view"
    INPUT_BOX = "input_box"
    STATUS_BAR = "status_bar"
    COMMAND_PALETTE = "command_palette"
    CODE_BLOCK = "code_block"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0439ComponentSpec:
    spec_id: str
    component_kind: str
    renders_from_ui_state_only: bool
    executes_runtime_action: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439ComponentRenderResult:
    result_id: str
    component_kind: str
    rendered_lines: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


def create_v0439_component_spec(component_kind: str = V0439ComponentKind.SIDEBAR.value, **overrides: Any) -> V0439ComponentSpec:
    defaults = {
        "spec_id": f"v0439-{component_kind}-component-spec",
        "component_kind": component_kind,
        "renders_from_ui_state_only": True,
        "executes_runtime_action": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439ComponentSpec(**defaults)


def _result(kind: str, lines: tuple[str, ...]) -> V0439ComponentRenderResult:
    return V0439ComponentRenderResult(
        result_id=f"v0439-{kind}-component-result",
        component_kind=kind,
        rendered_lines=lines,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        repo_search_used=False,
        workspace_read_opened=False,
        memory_mutated=False,
        production_certified=False,
    )


def render_v0439_sidebar(state: V0439UIState) -> V0439ComponentRenderResult:
    monitor = state.status_monitor
    lines = (
        state.product_name.upper(),
        state.subtitle,
        "",
        "PROJECT",
        f"path: {state.working_directory_label or 'unknown'}",
        f"mode: {state.mode_label}",
        "",
        "SESSION",
        f"profile: {state.profile_id}",
        f"provider: {state.provider_label}",
        "",
        "PI MONITOR",
        f"PI        {monitor.pi_status}",
        f"Provider  {monitor.provider_status}",
        f"Trace     {monitor.trace_status}",
        f"Evidence  {monitor.evidence_status}",
        f"Safety    {monitor.safety_status}",
        "",
        "COMMANDS",
        "workflows",
        "system",
    )
    return _result(V0439ComponentKind.SIDEBAR.value, lines)


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("create_v0439") or name.startswith("render_v0439")]
