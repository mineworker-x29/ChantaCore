from pathlib import Path
import json

from chanta_core.personal_runtime.default_personal_run import (
    create_minimal_single_turn_run_result,
    create_provider_text_response,
    create_run_command_result,
)
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_last_run_report,
    create_last_run_report_request,
)
from chanta_core.schumpeter_tui.app_state import create_v04310_tui_app_state
from chanta_core.schumpeter_tui.runtime_adapter import V04310RuntimeAdapter
from chanta_core.schumpeter_tui.turn_dispatch import apply_v04310_dispatch_result, dispatch_v04310_turn
from chanta_core.schumpeter_tui.widgets.slash_palette import create_v043112_palette_state, render_v043112_palette_text


FALLBACK_FORBIDDEN = (
    "일반 대화로 이해했습니다",
    "업무 산출물이 필요하면",
)


class FakeRunService:
    def __init__(self, text: str = "1+1은 2입니다.", status: str = "success", error_class: str | None = None):
        self.text = text
        self.status = status
        self.error_class = error_class
        self.calls = []

    def __call__(self, command_input):
        self.calls.append(command_input)
        response = None
        if self.status == "success":
            response = create_provider_text_response(
                text=self.text,
                response_parse_status="parsed",
                response_extracted_from_field="choices[0].message.content",
                response_content_length=len(self.text),
                provider_model="fake-provider-model",
                runtime_identity_included=True,
                empty_response_detected=False,
            )
        run_result = create_minimal_single_turn_run_result(
            status=self.status,
            assistant_text=self.text,
            provider_response=response,
            provider_invoked=True,
            prompt_submitted=True,
            shell_executed=False,
            subagent_invoked=False,
            workspace_mutated=False,
            production_certified=False,
            session_id=command_input.session_id or "session-test",
        )
        if self.status != "success":
            run_result = create_minimal_single_turn_run_result(
                status=self.status,
                assistant_text="provider failed",
                provider_response=create_provider_text_response(
                    status=self.status,
                    text="",
                    error_class=self.error_class or self.status,
                    response_parse_status="error",
                    empty_response_detected=True,
                ),
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
            trace_emitted=False,
            production_certified=False,
        )


def _adapter(tmp_path: Path | None = None, service: FakeRunService | None = None, emit_trace: bool = False):
    if tmp_path:
        _write_provider_config(tmp_path)
    return V04310RuntimeAdapter(
        home_path=str(tmp_path) if tmp_path else None,
        provider="configured",
        run_service=service or FakeRunService(),
        emit_run_report_trace=emit_trace,
    )


def _write_provider_config(home: Path) -> None:
    path = home / "profiles" / "default-personal" / "profile" / "PROVIDER.json"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            {
                "provider_id": "configured-provider",
                "provider_kind": "local_openai_compatible",
                "mode": "text_only",
                "base_url": "http://localhost:1234/v1",
                "model": "fake-provider-model",
                "completion_allowed_in_run": True,
                "tool_calling_allowed": False,
                "function_calling_allowed": False,
                "metadata": {"preset_kind": "local_openai_compatible"},
            },
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


def test_tui_general_chat_routes_to_runtime_adapter_provider_path(tmp_path):
    service = FakeRunService()
    result = _adapter(tmp_path, service).submit_user_input("오늘 작업 계획을 정리해줘")
    assert result.route_kind == "general_chat"
    assert service.calls


def test_tui_general_chat_does_not_use_generic_fallback_when_provider_configured(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1은?")
    assert not any(text in result.rendered_text for text in FALLBACK_FORBIDDEN)


def test_tui_general_chat_1_plus_1_gets_provider_response_with_fake_provider(tmp_path):
    result = _adapter(tmp_path, FakeRunService("1+1은 2입니다.")).submit_user_input("1+1은?")
    assert "1+1은 2입니다." in result.rendered_text


def test_tui_general_chat_appends_user_and_assistant_messages(tmp_path):
    adapter = _adapter(tmp_path, FakeRunService("1+1은 2입니다."))
    dispatch = dispatch_v04310_turn("1+1은?", adapter)
    state = apply_v04310_dispatch_result(create_v04310_tui_app_state(), dispatch)
    assert state.transcript[-2].kind == "user"
    assert state.transcript[-1].kind == "assistant"
    assert "1+1은 2입니다." in state.transcript[-1].text


def test_tui_general_chat_result_message_kind_assistant(tmp_path):
    result = _adapter(tmp_path).submit_user_input("간단히 설명해줘")
    assert result.message_kind == "assistant"


def test_tui_general_chat_result_provider_invoked_true_when_provider_used(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1은?")
    assert result.provider_invoked is True


def test_tui_general_chat_result_prompt_submitted_true_when_provider_used(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1은?")
    assert result.prompt_submitted is True


def test_tui_general_chat_preserves_shell_repo_workspace_subagent_memory_false(tmp_path):
    result = _adapter(tmp_path).submit_user_input("오늘 작업 계획을 정리해줘")
    assert result.shell_executed is False
    assert result.git_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.tool_calling_used is False
    assert result.function_calling_used is False
    assert result.subagent_invoked is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False


def test_tui_general_chat_uses_existing_run_service_not_direct_provider_client(tmp_path):
    service = FakeRunService("provider path used")
    result = _adapter(tmp_path, service).submit_user_input("이 내용을 어떻게 판단하면 좋을까?")
    assert len(service.calls) == 1
    assert service.calls[0].user_input == "이 내용을 어떻게 판단하면 좋을까?"
    assert "provider path used" in result.rendered_text


def test_tui_general_chat_provider_error_renders_clean_error_card(tmp_path):
    result = _adapter(tmp_path, FakeRunService(status="provider_unavailable", error_class="provider_unavailable")).submit_user_input("1+1은?")
    assert result.message_kind == "error"
    assert result.route_kind == "provider_error"
    assert "Provider unavailable" in result.rendered_text
    assert "Traceback" not in result.rendered_text


def test_tui_general_chat_provider_unavailable_suggests_provider_connectivity(tmp_path):
    result = _adapter(tmp_path, FakeRunService(status="provider_unavailable", error_class="provider_unavailable")).submit_user_input("1+1은?")
    assert "/provider" in result.rendered_text
    assert "chanta-cli provider connectivity" in result.rendered_text


def test_tui_general_chat_does_not_show_raw_metadata_by_default(tmp_path):
    result = _adapter(tmp_path).submit_user_input("1+1은?")
    forbidden = ("provider_invoked=", "prompt_submitted=", "response_parse_status=", "production_certified=false", "base_url", "api_key")
    assert not any(item in result.rendered_text for item in forbidden)


def test_tui_identity_question_may_remain_deterministic(tmp_path):
    service = FakeRunService()
    result = _adapter(tmp_path, service).submit_user_input("넌 누구야")
    assert result.route_kind == "identity_question"
    assert result.provider_invoked is False
    assert not service.calls


def test_tui_capability_question_may_remain_deterministic(tmp_path):
    service = FakeRunService()
    result = _adapter(tmp_path, service).submit_user_input("너가 할 줄 아는게 뭐야")
    assert result.route_kind == "capability_question"
    assert result.provider_invoked is False
    assert not service.calls


def test_tui_repository_status_request_remains_boundary_answer_without_repo_read(tmp_path):
    service = FakeRunService()
    result = _adapter(tmp_path, service).submit_user_input("지금 ChantaCore 저장소 상태도 점검해줘")
    assert result.route_kind == "repository_status_request"
    assert result.workspace_read_opened is False
    assert result.repo_search_used is False
    assert not service.calls


def test_slash_commands_still_route_to_command_dispatcher(tmp_path):
    service = FakeRunService()
    result = _adapter(tmp_path, service).execute_slash_command("/status")
    assert result.route_kind == "slash_command"
    assert result.message_kind == "status"
    assert result.provider_invoked is False
    assert not service.calls


def test_help_palette_status_sidebar_do_not_call_provider(tmp_path):
    service = FakeRunService()
    adapter = _adapter(tmp_path, service)
    adapter.collect_ui_snapshot()
    adapter.execute_slash_command("/help")
    adapter.execute_slash_command("/status")
    render_v043112_palette_text(create_v043112_palette_state("/"))
    assert not service.calls


def test_provider_call_happens_only_on_user_submit_provider_eligible_text(tmp_path):
    service = FakeRunService()
    adapter = _adapter(tmp_path, service)
    adapter.collect_ui_snapshot()
    render_v043112_palette_text(create_v043112_palette_state("/s"))
    assert not service.calls
    adapter.submit_user_input("간단히 설명해줘")
    assert len(service.calls) == 1


def test_run_report_contract_for_tui_general_chat_has_response_preview(tmp_path):
    service = FakeRunService("1+1은 2입니다.")
    result = _adapter(tmp_path, service, emit_trace=True).submit_user_input("1+1은?")
    report = create_last_run_report(create_last_run_report_request("default-personal", str(tmp_path)))
    assert result.run_id
    assert report.found is True
    assert report.provider_invoked is True
    assert report.prompt_submitted is True
    assert report.assistant_response_preview
    assert report.response_parse_status == "parsed"


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
