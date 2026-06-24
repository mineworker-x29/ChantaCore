"""Deterministic fake RuntimeAdapter for v0.43.11 UI tests."""

from __future__ import annotations

from dataclasses import dataclass

from chanta_core.schumpeter_tui.app_state import create_v04310_tui_turn_result
from chanta_core.schumpeter_tui.runtime_adapter import collect_v04310_runtime_snapshot


@dataclass
class V04311FakeRuntimeCounters:
    provider_completion_count: int = 0
    prompt_submission_count: int = 0
    shell_execution_count: int = 0
    repo_workspace_read_count: int = 0
    memory_mutation_count: int = 0


class V04311FakeRuntimeAdapter:
    def __init__(self):
        self.counters = V04311FakeRuntimeCounters()
        self.closed = False

    def collect_ui_snapshot(self):
        return collect_v04310_runtime_snapshot(
            provider_label="ready",
            pi_status="available",
            provider_status="ready",
            trace_status="active",
            evidence_status="none",
            safety_status="protected",
        )

    def submit_user_input(self, text: str):
        if text.strip().startswith("/"):
            return self.execute_slash_command(text)
        return create_v04310_tui_turn_result(
            input_text=text,
            route_kind="conversation",
            rendered_text="테스트 결과를 기준으로 핵심 사항과 다음 액션을 정리합니다.",
            message_kind="assistant",
            provider_invoked=True,
            prompt_submitted=True,
        )

    def execute_slash_command(self, command_text: str):
        raw = command_text.strip()
        if raw == "/exit":
            self.closed = True
            return create_v04310_tui_turn_result(input_text=raw, route_kind="exit", rendered_text="Schumpeter session closed.", message_kind="assistant")
        if raw.startswith("/summary"):
            return create_v04310_tui_turn_result(input_text=raw, route_kind="slash_command", rendered_text="핵심 내용\n- 테스트 완료\n- 다음 액션 정리", message_kind="artifact")
        if raw.startswith("/status"):
            return create_v04310_tui_turn_result(input_text=raw, route_kind="slash_command", rendered_text="Schumpeter status\nSafety: protected", message_kind="status")
        if raw.startswith("/what-happened"):
            return create_v04310_tui_turn_result(input_text=raw, route_kind="slash_command", rendered_text="TUI diagnostic\n- Rendering stayed display-only.", message_kind="diagnostic")
        if "workspace" in raw.lower():
            return create_v04310_tui_turn_result(input_text=raw, route_kind="slash_command", rendered_text="Workspace read is unavailable in this TUI.", message_kind="error")
        return create_v04310_tui_turn_result(input_text=raw, route_kind="slash_command", rendered_text="Command handled.", message_kind="status")

    def get_command_registry(self):
        return ("/summary", "/todo", "/decision", "/recall", "/status", "/help", "/exit")

    def close(self) -> None:
        self.closed = True


__all__ = ["V04311FakeRuntimeAdapter", "V04311FakeRuntimeCounters"]
