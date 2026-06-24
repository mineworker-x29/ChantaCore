"""Transcript and loop state for v0.43.10.1 interaction repair."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from chanta_core.schumpeter_tui.app_state import V04310TranscriptMessage


@dataclass(frozen=True)
class V04310TranscriptState:
    state_id: str
    messages: tuple[V04310TranscriptMessage, ...]
    production_certified: bool


@dataclass(frozen=True)
class V04310InteractiveLoopState:
    state_id: str
    transcript_messages: tuple[V04310TranscriptMessage, ...]
    prompt_visible: bool
    exit_requested: bool
    header_rendered_once: bool
    last_input: str | None
    last_route_kind: str | None
    repeated_static_chrome_count: int
    provider_invoked_by_rendering: bool
    prompt_submitted_by_rendering: bool
    shell_executed: bool
    git_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated_by_rendering: bool
    production_certified: bool


def create_v04310_transcript_state(
    messages: Sequence[V04310TranscriptMessage] = (),
    **overrides: Any,
) -> V04310TranscriptState:
    defaults = {
        "state_id": "v04310-transcript-state",
        "messages": tuple(messages),
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310TranscriptState(**defaults)


def create_v04310_interactive_loop_state(
    transcript_messages: Sequence[V04310TranscriptMessage] = (),
    last_input: str | None = None,
    last_route_kind: str | None = None,
    **overrides: Any,
) -> V04310InteractiveLoopState:
    defaults = {
        "state_id": "v04310-interactive-loop-state",
        "transcript_messages": tuple(transcript_messages),
        "prompt_visible": True,
        "exit_requested": False,
        "header_rendered_once": False,
        "last_input": last_input,
        "last_route_kind": last_route_kind,
        "repeated_static_chrome_count": 0,
        "provider_invoked_by_rendering": False,
        "prompt_submitted_by_rendering": False,
        "shell_executed": False,
        "git_executed": False,
        "repo_search_used": False,
        "workspace_read_opened": False,
        "memory_mutated_by_rendering": False,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04310InteractiveLoopState(**defaults)


__all__ = [name for name in globals() if name.startswith("V04310") or name.startswith("create_v04310")]
