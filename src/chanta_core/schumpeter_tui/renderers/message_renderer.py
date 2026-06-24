"""Message renderer boundary for normal chat messages."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any

from chanta_core.schumpeter_tui.state import V0439DisplayMessage, V0439DisplayMessageKind
from chanta_core.schumpeter_tui.widgets.message_view import render_v043117_card_text


class V0439RendererKind(StrEnum):
    MESSAGE = "message"
    ARTIFACT = "artifact"
    DIAGNOSTIC = "diagnostic"
    STATUS = "status"
    ERROR = "error"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class V0439RendererPolicy:
    policy_id: str
    default_hides_raw_metadata: bool
    debug_requires_explicit_surface: bool
    renderer_executes_runtime_actions: bool
    production_certified: bool


@dataclass(frozen=True)
class V0439RendererBoundary:
    boundary_id: str
    renderer_kind: str
    input_kind: str
    shows_raw_metadata_by_default: bool
    shows_debug_metadata_only_when_explicit: bool
    executes_runtime_action: bool
    provider_invoked: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    production_certified: bool


def create_v0439_renderer_policy(**overrides: Any) -> V0439RendererPolicy:
    defaults = {
        "policy_id": "v0439-renderer-policy",
        "default_hides_raw_metadata": True,
        "debug_requires_explicit_surface": True,
        "renderer_executes_runtime_actions": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439RendererPolicy(**defaults)


def create_v0439_renderer_boundary(
    renderer_kind: str = V0439RendererKind.MESSAGE.value,
    input_kind: str = V0439DisplayMessageKind.ASSISTANT.value,
    **overrides: Any,
) -> V0439RendererBoundary:
    defaults = {
        "boundary_id": f"v0439-{renderer_kind}-renderer-boundary",
        "renderer_kind": renderer_kind,
        "input_kind": input_kind,
        "shows_raw_metadata_by_default": False,
        "shows_debug_metadata_only_when_explicit": True,
        "executes_runtime_action": False,
        "provider_invoked": False,
        "shell_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V0439RendererBoundary(**defaults)


def render_v0439_message(message: V0439DisplayMessage, width: int = 78) -> str:
    return render_v043117_card_text(message.text, kind=message.kind, width=width)


__all__ = [name for name in globals() if name.startswith("V0439") or name.startswith("create_v0439") or name.startswith("render_v0439")]
