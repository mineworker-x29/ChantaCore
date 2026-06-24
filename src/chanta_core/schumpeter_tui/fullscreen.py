"""Full-screen Textual product surface for Schumpeter v0.43.11+."""

from __future__ import annotations

import importlib.util
from dataclasses import dataclass
from typing import Any

from chanta_core.schumpeter_tui.app_state import V04310TUIAppState, create_v04310_tui_app_state, create_v04310_transcript_message
from chanta_core.schumpeter_tui.command_registry import (
    extract_v043111_command_argument,
    find_v043111_command_spec,
)
from chanta_core.schumpeter_tui.display_width import truncate_to_display_width_v0439
from chanta_core.schumpeter_tui.help_surface import render_v04310_help
from chanta_core.schumpeter_tui.modals.help_modal import HelpModal, help_modal_text
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
from chanta_core.schumpeter_tui.turn_dispatch import apply_v04310_dispatch_result, dispatch_v04310_turn
from chanta_core.schumpeter_tui.widgets.slash_palette import (
    create_v043112_palette_state,
    insert_v043112_selected_command,
    move_v043112_palette_selection,
    palette_query_has_argument,
    render_v043112_palette_text,
)
from chanta_core.schumpeter_tui.widgets.pi_monitor import pi_monitor_text
from chanta_core.schumpeter_tui.widgets.session_panel import session_panel_text
from chanta_core.schumpeter_tui.widgets.status_bar import status_bar_text
from chanta_core.schumpeter_tui.widgets.message_view import message_card_style, message_label, render_v043117_card_text, sanitize_message_body


FORBIDDEN_V04311_DEFAULT_STRINGS = (
    "Structured TUI MVP is ready for preview",
    "Closed in this track",
    "ChantaGrowthKernel",
    "GrowthKernel",
    "legacy Schumpeter",
    "ChantaCore legacy core",
    "type: summary",
    "grounding:",
    "confidence:",
    "verification_required:",
    "source:",
    "shell=false",
    "subagent=false",
    "workspace_mutated=false",
    "memory_mutated=false",
    "production_certified=false",
    "production_" + "certified=True",
    "provider_invoked=",
    "prompt_submitted=",
    "base_url=",
    "api_key",
    "secret",
    "Traceback",
    "No source text provided",
)


@dataclass(frozen=True)
class V04311TextualDependencyStatus:
    available: bool
    dependency_declared: bool
    import_name: str
    actionable_message: str
    production_certified: bool


@dataclass(frozen=True)
class V04311EntrypointPolicy:
    default_start_launches_fullscreen_tui: bool
    tui_alias_launches_same_app: bool
    classic_fallback_available: bool
    plain_fallback_available: bool
    production_certified: bool


@dataclass(frozen=True)
class V04311VisualSnapshotResult:
    rendered_text: str
    width: int
    height: int
    layout_mode: str
    contains_sidebar: bool
    contains_chat: bool
    contains_input: bool
    contains_status_bar: bool
    contains_palette: bool
    contains_help_modal: bool
    contains_forbidden_default_strings: bool
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    repo_search_used: bool
    workspace_read_opened: bool
    memory_mutated: bool
    production_certified: bool


def detect_v04311_textual() -> V04311TextualDependencyStatus:
    available = importlib.util.find_spec("textual") is not None
    return V04311TextualDependencyStatus(
        available=available,
        dependency_declared=True,
        import_name="textual",
        actionable_message="Textual is required for full-screen mode. Run `py -m pip install -e .` or use `chanta-cli start --classic`.",
        production_certified=False,
    )


def create_v04311_entrypoint_policy(**overrides: Any) -> V04311EntrypointPolicy:
    defaults = {
        "default_start_launches_fullscreen_tui": True,
        "tui_alias_launches_same_app": True,
        "classic_fallback_available": True,
        "plain_fallback_available": True,
        "production_certified": False,
    }
    defaults.update(overrides)
    return V04311EntrypointPolicy(**defaults)


def _message_label(kind: str) -> str:
    return message_label(kind)


def _demo_v043117_app_state(app_state: V04310TUIAppState) -> V04310TUIAppState:
    transcript = (
        create_v04310_transcript_message("넌 누구야", "user"),
        create_v04310_transcript_message(
            "저는 Schumpeter입니다. PI-native Work Agent입니다.",
            "assistant",
        ),
        create_v04310_transcript_message("Provider: configured\nModel: qwen3.6-35b-a3b\nSafety: protected", "status"),
        create_v04310_transcript_message("핵심 요약: 메시지 카드 시각 계층을 점검했습니다.", "artifact"),
        create_v04310_transcript_message("recent turn: provider-backed\ntrace: active", "diagnostic"),
        create_v04310_transcript_message("저장소 읽기 닫힘. 다음: /v044 readiness", "error"),
    )
    return create_v04310_tui_app_state(app_state.runtime_snapshot, transcript)


def _render_v043117_transcript_lines(app_state: V04310TUIAppState, width: int, compact_spacing: bool = False) -> list[str]:
    card_width = max(30, min(width - 2, 88))
    lines: list[str] = []
    for message in app_state.transcript[-10:]:
        if message.kind == "system_notice":
            continue
        lines.extend(render_v043117_card_text(message.text, message.kind, width=card_width).splitlines())
        if not compact_spacing:
            lines.append("")
    return lines


def render_v04311_text_snapshot(
    width: int = 140,
    height: int = 42,
    app_state: V04310TUIAppState | None = None,
    include_palette: bool = False,
    include_help: bool = False,
    plain: bool = False,
    demo_conversation: bool = False,
    input_text: str | None = None,
) -> V04311VisualSnapshotResult:
    app_state = app_state or create_v04310_tui_app_state()
    if demo_conversation:
        app_state = _demo_v043117_app_state(app_state)
    mode = "narrow" if width < 90 else ("medium" if width < 120 else "wide")
    if plain:
        mode = "plain"
    lines: list[str] = []
    if demo_conversation:
        lines.extend(("Schumpeter demo conversation", ""))
    elif mode == "wide":
        provider_label = app_state.sidebar.provider_label
        provider_status_text = "ready" if provider_label == "configured" else provider_label
        lines.extend(
            (
                "SCHUMPETER                         | Welcome to Schumpeter",
                "PI-native Work Agent               | 오늘 어떤 업무를 진행할까요?",
                "PROJECT                            |",
                "ChantaCore                         |",
                "Work Session                       |",
                "SESSION                            |",
                f"{app_state.sidebar.profile_id:<34}|",
                f"provider: {provider_label:<24}|",
                "PI MONITOR                         |",
                "● PI       available               |",
                f"● Provider {provider_status_text:<21}|",
                "● Trace    active                  |",
                "○ Evidence none                    |",
                "● Safety   protected               |",
                "SHORTCUTS                          |",
                "/summary   /todo                   |",
                "/decision  /recall                 |",
                "/status    /help                   |",
                "",
            )
        )
    else:
        provider_status_text = "ready" if app_state.sidebar.provider_label == "configured" else app_state.sidebar.provider_label
        lines.extend((f"Schumpeter | default-personal | Provider {provider_status_text}", "PI ●  Trace ●  Evidence ○  Safety ●", ""))
    lines.append("Chat")
    transcript_lines = _render_v043117_transcript_lines(app_state, width, compact_spacing=demo_conversation and height <= 32)
    if include_palette:
        palette_line_budget = max(3, height - len(lines) - 5)
        palette_state = create_v043112_palette_state(
            input_text if input_text and input_text.startswith("/") else "/",
            max_visible_items=max(3, min(10, palette_line_budget - 2)),
        )
        palette_lines = render_v043112_palette_text(palette_state, width=width, compact=width < 90).splitlines()
        transcript_lines.extend(("", *palette_lines[:palette_line_budget]))
    if include_help:
        transcript_lines.extend(("", "Schumpeter Help", "Help", *render_v04310_help("/help").rendered_text.splitlines()[:18]))
    if demo_conversation:
        input_display = input_text or "Ask Schumpeter anything..."
        footer_lines = [
            "",
            "InputRegion",
            f"Input: {input_display}                         Ctrl+P  F1  /help",
            "",
            "StatusRegion",
            "PI   Provider   Trace   Evidence   Safety       default-personal       v0.43.11",
        ]
    else:
        input_display = input_text or "Ask Schumpeter anything..."
        footer_lines = [
            "",
            "InputRegion",
            "Input",
            f"{input_display}                                              Ctrl+P  F1  /help",
            "",
            "StatusRegion",
            "PI   Provider   Trace   Evidence   Safety       default-personal       v0.43.11",
        ]
    transcript_budget = max(0, height - len(lines) - len(footer_lines))
    if len(transcript_lines) > transcript_budget:
        if include_help or include_palette:
            transcript_lines = transcript_lines[:transcript_budget] if transcript_budget else []
        else:
            transcript_lines = transcript_lines[-transcript_budget:] if transcript_budget else []
    lines.extend(transcript_lines)
    lines.extend(footer_lines)
    clipped = "\n".join(truncate_to_display_width_v0439(line, width) for line in lines[:height])
    forbidden = any(item.lower() in clipped.lower() for item in FORBIDDEN_V04311_DEFAULT_STRINGS)
    return V04311VisualSnapshotResult(
        rendered_text=clipped,
        width=width,
        height=height,
        layout_mode=mode,
        contains_sidebar="PI MONITOR" in clipped or "Provider ready" in clipped,
        contains_chat="Chat" in clipped,
        contains_input=(input_text or "Ask Schumpeter anything") in clipped,
        contains_status_bar="v0.43.11" in clipped,
        contains_palette=include_palette and "Commands" in clipped,
        contains_help_modal=include_help and "Schumpeter Help" in clipped,
        contains_forbidden_default_strings=forbidden,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        repo_search_used=False,
        workspace_read_opened=False,
        memory_mutated=False,
        production_certified=False,
    )
    for message in app_state.transcript[-8:]:
        if message.kind == "system_notice":
            continue
        lines.append(_message_label(message.kind))
        lines.append(f"  {message.text.replace(chr(10), ' ')}")
    if include_palette:
        palette_line_budget = max(3, height - len(lines) - 5)
        palette_state = create_v043112_palette_state(
            "/",
            max_visible_items=max(3, min(10, palette_line_budget - 2)),
        )
        palette_lines = render_v043112_palette_text(palette_state, width=width, compact=width < 90).splitlines()
        lines.extend(("", *palette_lines[:palette_line_budget]))
    if include_help:
        lines.extend(("", "Help", *render_v04310_help("/help").rendered_text.splitlines()[:18]))
    lines.extend(
        (
            "",
            "Input",
            "Ask Schumpeter anything...                                              Ctrl+P  F1  /help",
            "● PI   ● Provider   ● Trace   ○ Evidence   ● Safety       default-personal       v0.43.11",
        )
    )
    clipped = "\n".join(truncate_to_display_width_v0439(line, width) for line in lines[:height])
    forbidden = any(item.lower() in clipped.lower() for item in FORBIDDEN_V04311_DEFAULT_STRINGS)
    return V04311VisualSnapshotResult(
        rendered_text=clipped,
        width=width,
        height=height,
        layout_mode=mode,
        contains_sidebar="PI MONITOR" in clipped or "Provider ready" in clipped,
        contains_chat="Chat" in clipped,
        contains_input="Ask Schumpeter anything" in clipped,
        contains_status_bar="v0.43.11" in clipped,
        contains_palette=include_palette and "Commands" in clipped,
        contains_help_modal=include_help and "Schumpeter Help" in clipped,
        contains_forbidden_default_strings=forbidden,
        provider_invoked=False,
        prompt_submitted=False,
        shell_executed=False,
        repo_search_used=False,
        workspace_read_opened=False,
        memory_mutated=False,
        production_certified=False,
    )


def create_v04311_textual_app(adapter: V04310RuntimeAdapter | None = None):
    status = detect_v04311_textual()
    if not status.available:
        return None

    from textual.app import App, ComposeResult
    from textual.binding import Binding
    from textual.containers import Container, Horizontal, Vertical, VerticalScroll
    from textual.widgets import Input, Static

    adapter = adapter or V04310RuntimeAdapter()

    class SchumpeterTextualApp(App):
        TITLE = "Schumpeter"
        SUB_TITLE = ""
        CSS_PATH = "styles/schumpeter.tcss"
        BINDINGS = [
            Binding("ctrl+c", "quit", "Exit"),
            Binding("ctrl+p", "toggle_palette", "Commands"),
            Binding("f1", "toggle_help", "Help"),
            Binding("escape", "close_overlays", "Close"),
        ]

        def __init__(self):
            super().__init__()
            self.adapter = adapter
            self.app_state = create_v04310_tui_app_state(self.adapter.collect_ui_snapshot())
            self.busy = False
            self.chat_plain = ""
            self.help_plain = ""
            self.about_plain = ""
            self.palette_plain = ""
            self.palette_state = create_v043112_palette_state("/", visible=False)
            self.palette_anchor = "above_input"
            self.input_visible_with_palette = True
            self.palette_selection_executed_command = False
            self.palette_suppressed_prefix = ""
            self.exit_requested = False
            self.help_modal_has_focus = False
            self.help_modal_traps_input = True
            self.help_modal_close_hint_visible = False
            self._input_value_before_help = ""
            self._restoring_input_for_help = False

        def compose(self) -> ComposeResult:
            with Vertical(id="app-root"):
                with Horizontal(id="main-body"):
                    with Vertical(id="sidebar"):
                        yield Static("SCHUMPETER\nPI-native Work Agent", id="brand-panel")
                        yield Static("PROJECT\nChantaCore\nWork Session", id="project-panel")
                        provider_label = self.app_state.sidebar.provider_label
                        provider_status_text = "ready" if provider_label == "configured" else provider_label
                        yield Static(session_panel_text(self.app_state.sidebar.profile_id, provider_label), id="session-panel")
                        yield Static(pi_monitor_text(provider_status_text), id="pi-monitor")
                        yield Static("SHORTCUTS\n/summary   /todo\n/decision  /recall\n/status    /help", id="shortcut-panel")
                    with Vertical(id="chat-panel"):
                        yield VerticalScroll(id="chat-view")
                with Vertical(id="palette-region", classes="hidden"):
                    yield Static("", id="slash-palette", classes="hidden")
                yield HelpModal("", id="help-modal", classes="overlay hidden")
                yield Static("", id="about-modal", classes="overlay hidden")
                with Vertical(id="input-region"):
                    yield Input(placeholder="Ask Schumpeter anything...", id="main-input")
                with Vertical(id="status-region"):
                    yield Static(status_bar_text(), id="status-bar")

        def on_mount(self) -> None:
            self._refresh_chat()

        def _refresh_chat(self) -> None:
            chat = self.query_one("#chat-view", VerticalScroll)
            chat.remove_children()
            plain_lines = ["Welcome to Schumpeter.", "일반 문장을 입력하거나 /help로 업무 명령을 확인하세요."]
            chat.mount(Static(plain_lines[0], classes="chat-welcome-title"))
            chat.mount(Static(plain_lines[1], classes="chat-welcome-subtitle"))
            for message in self.app_state.transcript:
                if message.kind == "system_notice":
                    continue
                style = message_card_style(message.kind)
                body = sanitize_message_body(message.text)
                bubble = Vertical(
                    Static(style.title, classes="speaker-label"),
                    Static(body, classes="message-body"),
                    classes=" ".join(style.css_classes),
                )
                row = Container(bubble, classes=f"message-row {style.kind}-row")
                chat.mount(row)
                plain_lines.extend((style.title, body, ""))
            self.chat_plain = "\n".join(plain_lines)

        def action_toggle_palette(self) -> None:
            if self._is_help_visible():
                return
            if self._is_palette_visible():
                self._hide_palette()
            else:
                input_bar = self.query_one("#main-input", Input)
                self._show_palette(input_bar.value or "/")

        def action_toggle_help(self) -> None:
            if self._is_help_visible():
                self._close_help_modal()
            else:
                self._open_help_modal("/help")

        def action_close_overlays(self) -> None:
            if self._is_help_visible():
                self._close_help_modal()
                return
            for selector in ("#slash-palette", "#help-modal", "#about-modal"):
                self.query_one(selector, Static).add_class("hidden")
            self.query_one("#palette-region", Vertical).add_class("hidden")
            self.query_one("#palette-region", Vertical).remove_class("open")
            self.palette_state = create_v043112_palette_state(self.palette_state.query, self.palette_state.selected_index, visible=False)

        def on_input_changed(self, event: Input.Changed) -> None:
            if self._is_help_visible():
                if not self._restoring_input_for_help and event.value != self._input_value_before_help:
                    self._restoring_input_for_help = True
                    event.input.value = self._input_value_before_help
                    self._restoring_input_for_help = False
                if self._is_palette_visible():
                    self._hide_palette()
                return
            if self.palette_suppressed_prefix:
                if event.value.startswith(self.palette_suppressed_prefix):
                    if self._is_palette_visible():
                        self._hide_palette()
                    return
                self.palette_suppressed_prefix = ""
            if event.value.startswith("/") and palette_query_has_argument(event.value):
                if self._is_palette_visible():
                    self._hide_palette()
            elif event.value.startswith("/"):
                self._show_palette(event.value)
            elif self._is_palette_visible():
                self._hide_palette()

        def _is_palette_visible(self) -> bool:
            return not self.query_one("#slash-palette", Static).has_class("hidden")

        def _is_help_visible(self) -> bool:
            return not self.query_one("#help-modal", HelpModal).has_class("hidden")

        def _open_help_modal(self, topic: str = "/help") -> None:
            if self._is_palette_visible():
                self._hide_palette()
            input_bar = self.query_one("#main-input", Input)
            self._input_value_before_help = input_bar.value
            input_bar.disabled = True
            self.help_plain = help_modal_text(topic)
            help_modal = self.query_one("#help-modal", HelpModal)
            help_modal.update(self.help_plain)
            help_modal.remove_class("hidden")
            help_modal.focus()
            self.help_modal_has_focus = True
            self.help_modal_close_hint_visible = "Esc 닫기" in self.help_plain and "q 닫기" in self.help_plain

        def _show_palette(self, query: str = "/") -> None:
            if self._is_help_visible():
                return
            self.palette_state = create_v043112_palette_state(query or "/", visible=True)
            self.palette_plain = render_v043112_palette_text(self.palette_state, width=max(50, self.size.width - 36), compact=self.size.width < 90)
            palette = self.query_one("#slash-palette", Static)
            palette.update(self.palette_plain)
            palette.remove_class("hidden")
            self.query_one("#palette-region", Vertical).remove_class("hidden")
            self.query_one("#palette-region", Vertical).add_class("open")
            self.input_visible_with_palette = True

        def _hide_palette(self) -> None:
            self.query_one("#slash-palette", Static).add_class("hidden")
            self.query_one("#palette-region", Vertical).add_class("hidden")
            self.query_one("#palette-region", Vertical).remove_class("open")
            self.palette_state = create_v043112_palette_state(self.palette_state.query, self.palette_state.selected_index, visible=False)

        def _close_help_modal(self) -> None:
            help_modal = self.query_one("#help-modal", HelpModal)
            help_modal.add_class("hidden")
            input_bar = self.query_one("#main-input", Input)
            input_bar.disabled = False
            self.help_modal_has_focus = False
            input_bar.focus()

        def _move_palette_selection(self, direction: int) -> None:
            self.palette_state, _result = move_v043112_palette_selection(self.palette_state, direction)
            self.palette_plain = render_v043112_palette_text(self.palette_state, width=max(50, self.size.width - 36), compact=self.size.width < 90)
            self.query_one("#slash-palette", Static).update(self.palette_plain)

        def _insert_palette_selection(self) -> None:
            result = insert_v043112_selected_command(self.palette_state)
            input_bar = self.query_one("#main-input", Input)
            input_bar.value = result.inserted_text
            input_bar.focus()
            self.palette_selection_executed_command = result.command_executed
            self.palette_suppressed_prefix = result.inserted_text
            self._hide_palette()

        def _input_is_complete_non_argument_command(self) -> bool:
            input_bar = self.query_one("#main-input", Input)
            raw = input_bar.value.strip()
            spec = find_v043111_command_spec(raw)
            if spec is None or spec.requires_argument:
                return False
            argument = extract_v043111_command_argument(raw, spec)
            return raw.lower() == spec.command.lower() and not argument

        def on_key(self, event) -> None:
            if self._is_help_visible():
                if event.key in {"escape", "q", "f1"}:
                    event.prevent_default()
                    event.stop()
                    self._close_help_modal()
                    return
                if event.key in {"up", "down", "pageup", "pagedown"}:
                    event.prevent_default()
                    event.stop()
                    return
                if event.key == "ctrl+c":
                    event.prevent_default()
                    event.stop()
                    self._close_help_modal()
                    return
                event.prevent_default()
                event.stop()
                return
            if not self._is_palette_visible():
                return
            if event.key == "enter" and self._input_is_complete_non_argument_command():
                self._hide_palette()
                return
            if event.key in {"down", "up", "tab", "enter", "escape"}:
                event.prevent_default()
                event.stop()
            if event.key == "down":
                self._move_palette_selection(1)
            elif event.key == "up":
                self._move_palette_selection(-1)
            elif event.key in {"tab", "enter"}:
                self._insert_palette_selection()
            elif event.key == "escape":
                self._hide_palette()

        def on_input_submitted(self, event: Input.Submitted) -> None:
            if self._is_help_visible():
                event.stop()
                return
            raw = event.value.strip()
            if not raw or self.busy:
                return
            if self._is_palette_visible():
                if self._input_is_complete_non_argument_command():
                    self._hide_palette()
                else:
                    self._insert_palette_selection()
                    return
            event.input.value = ""
            if raw == "/help" or raw.startswith("/help "):
                self._open_help_modal(raw)
                return
            if raw == "/about":
                self.about_plain = "Schumpeter\nProcess Intelligence-native Work Agent\n\nProduct surface: Schumpeter\nRuntime lineage: ChantaCore\nCLI compatibility: chanta-cli"
                self.query_one("#about-modal", Static).update(self.about_plain)
                self.query_one("#about-modal", Static).remove_class("hidden")
                return
            if raw in {"/exit", "/quit"}:
                self.exit_requested = True
                self.exit()
                return
            self.busy = True
            result = dispatch_v04310_turn(raw, self.adapter)
            self.app_state = apply_v04310_dispatch_result(self.app_state, result)
            self.busy = False
            self._refresh_chat()

    return SchumpeterTextualApp()


def run_v04311_fullscreen_tui() -> int:
    status = detect_v04311_textual()
    if not status.available:
        print(status.actionable_message)
        return 2
    app = create_v04311_textual_app()
    if app is None:
        print(status.actionable_message)
        return 2
    app.run()
    return 0


__all__ = [name for name in globals() if name.startswith("V04311") or name.startswith("FORBIDDEN") or name.startswith("detect_v04311") or name.startswith("create_v04311") or name.startswith("render_v04311") or name.startswith("run_v04311")]
