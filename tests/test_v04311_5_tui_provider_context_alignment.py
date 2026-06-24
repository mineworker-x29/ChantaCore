import json
from pathlib import Path

from chanta_core.personal_runtime.default_personal_run import (
    create_minimal_single_turn_run_result,
    create_provider_text_response,
    create_run_command_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_last_run_report,
    create_last_run_report_request,
)
from chanta_core.schumpeter_tui.runtime_adapter import (
    V04310RuntimeAdapter,
    create_v043115_tui_provider_context,
)
from chanta_core.schumpeter_tui.widgets.slash_palette import create_v043112_palette_state, render_v043112_palette_text


class FakeExistingRunService:
    def __init__(self, text: str = "1+1은 2입니다.", status: str = "success", error_class: str | None = None):
        self.text = text
        self.status = status
        self.error_class = error_class
        self.calls = []

    def __call__(self, command_input):
        self.calls.append(command_input)
        response = create_provider_text_response(
            status=self.status,
            text=self.text if self.status == "success" else "",
            error_class=self.error_class,
            response_parse_status="parsed" if self.status == "success" else "error",
            response_extracted_from_field="choices[0].message.content" if self.status == "success" else None,
            response_content_length=len(self.text) if self.status == "success" else 0,
            provider_model="fake-provider-model",
            runtime_identity_included=True,
            empty_response_detected=self.status != "success",
        )
        run_result = create_minimal_single_turn_run_result(
            status=self.status,
            assistant_text=self.text if self.status == "success" else "provider failed",
            provider_response=response,
            provider_invoked=True,
            prompt_submitted=True,
            shell_executed=False,
            subagent_invoked=False,
            workspace_mutated=False,
            production_certified=False,
            session_id=command_input.session_id or "session-test",
        )
        return create_run_command_result(
            status=self.status,
            exit_code=0 if self.status == "success" else 1,
            run_result=run_result,
            provider_invoked=True,
            prompt_submitted=True,
            production_certified=False,
        )


def _write_provider_config(home: Path, model: str = "fake-provider-model") -> None:
    path = home / "profiles" / "default-personal" / "profile" / "PROVIDER.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "provider_id": "configured-provider",
                "provider_kind": "local_openai_compatible",
                "mode": "text_only",
                "base_url": "http://localhost:1234/v1",
                "model": model,
                "completion_allowed_in_run": True,
                "tool_calling_allowed": False,
                "function_calling_allowed": False,
                "metadata": {"preset_kind": "local_openai_compatible"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def _adapter(home: Path, service: FakeExistingRunService | None = None, provider: str | None = None, emit_trace: bool = False):
    _write_provider_config(home)
    return V04310RuntimeAdapter(
        home_path=str(home),
        provider=provider,
        run_service=service or FakeExistingRunService(),
        emit_run_report_trace=emit_trace,
    )


def test_tui_provider_context_uses_same_home_profile_provider_as_cli_run(tmp_path):
    _write_provider_config(tmp_path)
    context = create_v043115_tui_provider_context(home_path=str(tmp_path), provider="configured")
    assert context.home_path == str(tmp_path)
    assert context.profile_id == "default-personal"
    assert context.provider_mode == "configured"
    assert context.uses_same_resolver_as_cli_run is True


def test_tui_provider_context_resolves_default_personal_profile(tmp_path):
    _write_provider_config(tmp_path)
    context = create_v043115_tui_provider_context(home_path=str(tmp_path))
    assert context.profile_id == "default-personal"


def test_tui_provider_context_resolves_chantacore_home_env(tmp_path, monkeypatch):
    _write_provider_config(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(tmp_path))
    context = create_v043115_tui_provider_context()
    assert context.home_path == str(tmp_path)


def test_tui_provider_auto_resolves_to_configured_when_configured_available(tmp_path):
    _write_provider_config(tmp_path)
    context = create_v043115_tui_provider_context(home_path=str(tmp_path), provider=None)
    assert context.provider_mode == "configured"
    assert context.configured_provider_available is True


def test_tui_sidebar_provider_status_not_fake(tmp_path):
    _write_provider_config(tmp_path, model="real-status-model")
    adapter = V04310RuntimeAdapter(home_path=str(tmp_path), provider=None, run_service=FakeExistingRunService(), emit_run_report_trace=False)
    assert adapter.provider_context.configured_model == "real-status-model"
    assert adapter.provider_context.provider_status_source == "v042_home_resolver_and_provider_status"


def test_tui_provider_status_and_dispatch_consistent(tmp_path):
    adapter = _adapter(tmp_path)
    status = adapter.execute_slash_command("/provider")
    result = adapter.submit_user_input("1+1이 뭐야?")
    assert "Status: configured" in status.rendered_text
    assert result.route_kind == "general_chat"
    assert "provider_not_configured" not in result.rendered_text


def test_tui_general_chat_does_not_return_provider_not_configured_when_configured_available(tmp_path):
    service = FakeExistingRunService(status="provider_not_configured", error_class="provider_not_configured")
    result = _adapter(tmp_path, service).submit_user_input("1+1이 뭐야?")
    assert "provider_not_configured" not in result.rendered_text
    assert "configured provider was available" in result.rendered_text


def test_tui_general_chat_calls_existing_run_service(tmp_path):
    service = FakeExistingRunService()
    result = _adapter(tmp_path, service).submit_user_input("오늘 작업 계획을 3줄로 정리해줘")
    assert len(service.calls) == 1
    assert service.calls[0].home_path == str(tmp_path)
    assert service.calls[0].profile_id == "default-personal"
    assert service.calls[0].provider == "configured"
    assert result.provider_invoked is True


def test_tui_general_chat_does_not_create_direct_http_provider_client():
    text = Path("src/chanta_core/schumpeter_tui/runtime_adapter.py").read_text(encoding="utf-8")
    forbidden = ("requ" + "ests", "ht" + "tpx", "url" + "lib", "so" + "cket", "Open" + "AI(")
    assert not any(item in text for item in forbidden)


def test_tui_general_chat_1_plus_1_uses_fake_existing_run_service_and_returns_answer(tmp_path):
    result = _adapter(tmp_path, FakeExistingRunService("1+1은 2입니다.")).submit_user_input("1+1이 뭐야?")
    assert result.rendered_text == "1+1은 2입니다."


def test_tui_general_chat_result_contains_run_id_and_session_id_when_available(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1이 뭐야?")
    assert result.run_id
    assert result.session_id


def test_tui_general_chat_result_provider_invoked_true_prompt_submitted_true(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1이 뭐야?")
    assert result.provider_invoked is True
    assert result.prompt_submitted is True


def test_tui_general_chat_result_shell_repo_workspace_subagent_memory_false(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1이 뭐야?")
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.subagent_invoked is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False


def test_tui_provider_unavailable_error_is_clean_and_actionable(tmp_path):
    adapter = V04310RuntimeAdapter(home_path=str(tmp_path), provider="configured", run_service=FakeExistingRunService(), emit_run_report_trace=False)
    result = adapter.submit_user_input("1+1이 뭐야?")
    assert result.message_kind == "error"
    assert "Provider unavailable" in result.rendered_text
    assert "/provider" in result.rendered_text
    assert "chanta-cli provider connectivity" in result.rendered_text


def test_tui_provider_unavailable_does_not_show_raw_stack_trace(tmp_path):
    adapter = V04310RuntimeAdapter(home_path=str(tmp_path), provider="configured", run_service=FakeExistingRunService(), emit_run_report_trace=False)
    result = adapter.submit_user_input("1+1이 뭐야?")
    assert "Traceback" not in result.rendered_text


def test_tui_provider_error_preserves_status_consistency_message(tmp_path):
    result = _adapter(tmp_path, FakeExistingRunService(status="provider_not_configured", error_class="provider_not_configured")).submit_user_input("1+1이 뭐야?")
    assert "configured provider was available" in result.rendered_text


def test_help_status_sidebar_palette_do_not_call_provider(tmp_path):
    service = FakeExistingRunService()
    adapter = _adapter(tmp_path, service)
    adapter.collect_ui_snapshot()
    adapter.execute_slash_command("/provider")
    adapter.execute_slash_command("/status")
    render_v043112_palette_text(create_v043112_palette_state("/"))
    assert not service.calls


def test_provider_status_card_uses_same_resolver_as_dispatch(tmp_path):
    adapter = _adapter(tmp_path)
    status = adapter.execute_slash_command("/provider").rendered_text
    adapter.submit_user_input("1+1이 뭐야?")
    assert f"Home: {tmp_path}" in status


def test_run_report_contract_after_tui_provider_backed_turn(tmp_path):
    adapter = _adapter(tmp_path, FakeExistingRunService("1+1은 2입니다."), emit_trace=True)
    adapter.submit_user_input("1+1이 뭐야?")
    report = create_last_run_report(create_last_run_report_request("default-personal", str(tmp_path)))
    assert report.found is True
    assert report.provider_invoked is True
    assert report.prompt_submitted is True
    assert report.assistant_response_preview


def test_no_forbidden_runtime_call_patterns():
    text = Path("src/chanta_core/schumpeter_tui/runtime_adapter.py").read_text(encoding="utf-8")
    forbidden = (
        "requ" + "ests",
        "ht" + "tpx",
        "url" + "lib",
        "so" + "cket",
        "sub" + "process",
        "shell" + "=True",
        "os." + "system",
        "ev" + "al(",
        "ex" + "ec(",
        "Path." + "rglob",
        "os." + "walk",
        "CORE_MEMORY",
    )
    assert not any(item in text for item in forbidden)
