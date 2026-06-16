from __future__ import annotations

import json
from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_provider_response as v0428
from chanta_core.personal_runtime import default_personal_run as v0414
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart


class _FakeResponse:
    def __init__(self, payload: dict[str, object]) -> None:
        self.payload = payload

    def __enter__(self) -> "_FakeResponse":
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode("utf-8")


def _prepared_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    result = run_v042_quickstart(explicit_home=str(home), with_mock_run=True)
    assert result.exit_code == 0
    return home


def _setup_local_provider(home: Path, model: str = "qwen3.6-35b-a3b") -> None:
    assert cli_main(["provider", "setup", "local-openai", "--home", str(home), "--base-url", "http://localhost:1234/v1", "--model", model]) == 0


def _trace_text(home: Path) -> str:
    path = home / "profiles" / "default-personal" / "state" / "traces" / "events.jsonl"
    return path.read_text(encoding="utf-8")


def test_v0428_response_parse_status_values_declared() -> None:
    values = {item.value for item in v0428.V042ProviderResponseParseStatus}
    assert {
        "parsed",
        "parsed_empty",
        "missing_choices",
        "missing_message",
        "missing_content",
        "provider_reasoning_without_final",
        "invalid_response_shape",
        "parse_error",
        "timeout",
        "connection_error",
        "unknown",
    }.issubset(values)


def test_v0428_response_error_classes_declared() -> None:
    values = {item.value for item in v0428.V042ProviderResponseErrorClass}
    assert {
        "none",
        "provider_empty_response",
        "response_parse_empty",
        "response_parse_error",
        "provider_reasoning_without_final",
        "provider_invalid_response",
        "provider_timeout",
        "provider_connection_error",
        "model_not_found",
        "unknown_provider_error",
    }.issubset(values)


def test_v0428_response_shape_summary_detects_choices_message_content_usage_and_model() -> None:
    summary = v0428.summarize_v042_provider_response_shape(
        {"model": "qwen", "choices": [{"message": {"content": "안녕하세요"}, "finish_reason": "stop"}], "usage": {"prompt_tokens": 1, "completion_tokens": 2, "total_tokens": 3}}
    )
    assert summary.has_choices is True
    assert summary.choices_count == 1
    assert summary.has_message is True
    assert summary.has_message_content is True
    assert summary.provider_model == "qwen"
    assert summary.finish_reason == "stop"
    assert summary.total_tokens == 3


def test_v0428_parser_extracts_choices_message_content() -> None:
    result = v0428.parse_v042_openai_compatible_response({"choices": [{"message": {"content": "final"}}]})
    assert result.status == "parsed"
    assert result.error_class == "none"
    assert result.assistant_text == "final"
    assert result.extracted_from_field == "choices[0].message.content"


def test_v0428_parser_extracts_choices_text_fallback() -> None:
    result = v0428.parse_v042_openai_compatible_response({"choices": [{"text": "legacy text"}]})
    assert result.status == "parsed"
    assert result.assistant_text == "legacy text"
    assert result.extracted_from_field == "choices[0].text"


def test_v0428_parser_detects_missing_choices() -> None:
    result = v0428.parse_v042_openai_compatible_response({"model": "qwen"})
    assert result.status == "missing_choices"
    assert result.error_class == "provider_invalid_response"


def test_v0428_parser_detects_missing_message() -> None:
    result = v0428.parse_v042_openai_compatible_response({"choices": [{"finish_reason": "stop"}]})
    assert result.status == "missing_message"
    assert result.assistant_text_present is False


def test_v0428_parser_detects_missing_content() -> None:
    result = v0428.parse_v042_openai_compatible_response({"choices": [{"message": {"role": "assistant"}}]})
    assert result.status == "missing_content"
    assert result.error_class == "response_parse_empty"


def test_v0428_parser_detects_empty_content_as_failure() -> None:
    result = v0428.parse_v042_openai_compatible_response({"choices": [{"message": {"content": "   "}}]})
    assert result.status == "parsed_empty"
    assert result.error_class == "provider_empty_response"
    assert result.assistant_text_present is False


def test_v0428_parser_detects_reasoning_without_final_as_not_success() -> None:
    result = v0428.parse_v042_openai_compatible_response({"choices": [{"message": {"reasoning_content": "thinking"}}]})
    assert result.status == "provider_reasoning_without_final"
    assert result.error_class == "provider_reasoning_without_final"
    assert result.reasoning_content_detected is True
    assert result.assistant_text_present is False


def test_v0428_empty_response_decision_does_not_mark_run_completed() -> None:
    decision = v0428.create_v042_provider_empty_response_decision()
    assert decision.empty_response_detected is True
    assert decision.mark_run_completed is False
    assert decision.status == "failed"


def test_v0428_empty_response_decision_does_not_append_normal_assistant_turn() -> None:
    decision = v0428.create_v042_provider_empty_response_decision()
    assert decision.append_normal_assistant_turn is False
    assert decision.record_assistant_response_success is False


def test_v0428_runtime_identity_prompt_declares_chantacore_default_personal_identity() -> None:
    prompt = v0428.create_v042_runtime_identity_prompt()
    assert "ChantaCore Default Personal Runtime" in prompt.prompt_text
    assert "default-personal" in prompt.prompt_text
    assert "Korean polite language" in prompt.prompt_text
    assert prompt.included_in_configured_provider_run is True


def test_v0428_runtime_identity_prompt_treats_provider_identity_as_implementation_detail() -> None:
    prompt = v0428.create_v042_runtime_identity_prompt()
    assert "provider identity is an implementation detail" in prompt.prompt_text
    assert "underlying base model" in prompt.prompt_text


def test_v0428_runtime_identity_injection_report_marks_identity_included_for_configured_provider() -> None:
    report = v0428.create_v042_runtime_identity_injection_report(provider_model="qwen")
    assert report.prompt_assembled is True
    assert report.runtime_identity_included is True
    assert report.provider_model == "qwen"
    assert report.provider_identity_is_implementation_detail is True


def test_v0428_provider_identity_separation_disallows_base_model_identity_as_primary() -> None:
    report = v0428.create_v042_provider_identity_separation_report("qwen")
    assert report.base_model_identity_allowed_as_primary is False
    assert report.provider_identity_allowed_as_implementation_detail is True
    assert "ChantaCore" in report.expected_identity_answer_policy


def test_v0428_run_response_recording_policy_requires_non_empty_assistant_text_for_success() -> None:
    policy = v0428.create_v042_run_response_recording_policy()
    assert policy.require_non_empty_assistant_text_for_success is True
    assert policy.append_empty_assistant_turn_as_success is False


def test_v0428_run_response_recording_decision_marks_empty_response_failed() -> None:
    decision = v0428.create_v042_run_response_recording_decision()
    assert decision.response_valid is False
    assert decision.run_status == "failed"
    assert decision.should_append_assistant_turn is False


def test_v0428_run_report_response_fields_include_parse_status_error_class_content_length_runtime_identity() -> None:
    result = v0428.parse_v042_openai_compatible_response({"model": "qwen", "choices": [{"message": {"content": "ok"}}]})
    fields = v0428.create_v042_run_report_response_fields(result)
    assert fields.response_parse_status == "parsed"
    assert fields.response_error_class == "none"
    assert fields.response_content_length == 2
    assert fields.runtime_identity_included is True


def test_v0428_response_parse_trace_record_has_high_risk_flags_false() -> None:
    record = v0428.create_v042_response_parse_trace_record()
    assert record.event_kind == "provider_text_response_parsed"
    assert record.shell_executed is False
    assert record.subagent_invoked is False
    assert record.production_certified is False


def test_v0428_configured_run_empty_response_report_has_next_actions_and_no_shell_subagent_or_production() -> None:
    report = v0428.create_v042_configured_run_failure_report(provider_model="qwen")
    assert report.error_class in {"provider_empty_response", "response_parse_empty", "provider_reasoning_without_final"}
    assert report.next_actions
    assert report.shell_executed is False
    assert report.subagent_invoked is False
    assert report.production_certified is False


def test_v0428_command_surface_policy_preserves_direct_run_and_prioritizes_help() -> None:
    policy = v0428.create_v042_command_surface_stabilization_policy()
    assert policy.preserve_direct_run_command is True
    assert policy.help_priority_over_validation is True
    assert policy.unrecognized_show_args_redirected is True


def test_v0428_run_help_shows_usage_and_does_not_return_invalid_config(capsys) -> None:
    assert cli_main(["run", "--help"]) == 0
    output = capsys.readouterr().out
    assert "usage: chanta-cli run" in output
    assert "invalid_config" not in output


def test_v0428_run_show_last_no_longer_unrecognized_or_provides_clear_redirect(tmp_path: Path, capsys) -> None:
    home = _prepared_home(tmp_path)
    assert cli_main(["run", "show", "last", "--home", str(home)]) in {0, 1}
    output = capsys.readouterr().out
    assert "unrecognized arguments" not in output
    assert "ChantaCore Run" in output or "run-report last" in output


def test_v0428_direct_run_still_works_for_mock_provider(tmp_path: Path, capsys) -> None:
    home = _prepared_home(tmp_path)
    assert cli_main(["run", "--home", str(home), "--provider", "mock", "hi"]) == 0
    output = capsys.readouterr().out
    assert "Mock provider response" in output


def test_v0428_reasoning_model_troubleshooting_mentions_completion_tokens_without_content_max_tokens_final_answer_lm_studio_template() -> None:
    guide = v0428.create_v042_provider_reasoning_model_troubleshooting_guide()
    text = " ".join(guide.symptoms + guide.recommended_actions + guide.likely_causes)
    assert "completion tokens" in text
    assert "message.content" in text
    assert "max_tokens" in text
    assert "final answer" in text
    assert "LM Studio" in text


def test_v0428_readiness_report_sets_parser_identity_command_surface_flags_true() -> None:
    report = v0428.create_v0428_readiness_report()
    assert report.provider_response_parser_ready is True
    assert report.runtime_identity_prompt_ready is True
    assert report.command_surface_stabilization_ready is True


def test_v0428_readiness_report_keeps_tools_functions_shell_subagent_agentloop_and_production_false() -> None:
    report = v0428.create_v0428_readiness_report()
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.production_certified is False


def test_v0428_configured_empty_response_is_failed_and_not_appended(tmp_path: Path, monkeypatch, capsys) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)

    def fake_urlopen(request, timeout):  # noqa: ANN001
        return _FakeResponse({"model": "qwen3.6-35b-a3b", "choices": [{"message": {"content": ""}, "finish_reason": "stop"}], "usage": {"completion_tokens": 255}})

    monkeypatch.setattr(v0414.urllib.request, "urlopen", fake_urlopen)
    assert cli_main(["run", "--home", str(home), "--provider", "configured", "--timeout", "120", "넌 누구야?"]) == 1
    output = capsys.readouterr().out
    assert "Configured provider returned no final assistant content." in output
    assert "Debug fields are available in chanta-cli run-report last." in output
    assert cli_main(["run-report", "last", "--home", str(home)]) == 0
    report_output = capsys.readouterr().out
    assert '"response_parse_status": "parsed_empty"' in report_output
    assert "assistant_response_recorded" not in _trace_text(home).split("run_started")[-1]
    assert "provider_text_response_empty" in _trace_text(home)
    assert "run_failed" in _trace_text(home)


def test_v0428_configured_run_payload_includes_runtime_identity_prompt(tmp_path: Path, monkeypatch) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)
    seen_payloads: list[dict[str, object]] = []

    def fake_urlopen(request, timeout):  # noqa: ANN001
        seen_payloads.append(json.loads(request.data.decode("utf-8")))
        return _FakeResponse({"model": "qwen3.6-35b-a3b", "choices": [{"message": {"content": "저는 ChantaCore default-personal runtime에서 동작하는 대화형 assistant입니다."}}]})

    monkeypatch.setattr(v0414.urllib.request, "urlopen", fake_urlopen)
    assert cli_main(["run", "--home", str(home), "--provider", "configured", "넌 누구야?"]) == 0
    messages = seen_payloads[-1]["messages"]
    assert isinstance(messages, list)
    assert messages[0]["role"] == "system"
    assert "ChantaCore Default Personal Runtime" in messages[0]["content"]
    assert "provider identity is an implementation detail" in messages[0]["content"]


def test_v0428_run_report_includes_response_parse_fields_after_empty_response(tmp_path: Path, monkeypatch, capsys) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)

    def fake_urlopen(request, timeout):  # noqa: ANN001
        return _FakeResponse({"model": "qwen3.6-35b-a3b", "choices": [{"message": {"content": ""}, "finish_reason": "stop"}]})

    monkeypatch.setattr(v0414.urllib.request, "urlopen", fake_urlopen)
    assert cli_main(["run", "--home", str(home), "--provider", "configured", "넌 누구야?"]) == 1
    capsys.readouterr()
    assert cli_main(["run-report", "last", "--home", str(home)]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["status"] == "failed"
    assert report["assistant_response_preview"] == ""
    assert report["response_parse_status"] == "parsed_empty"
    assert report["response_error_class"] == "provider_empty_response"
    assert report["empty_response_detected"] is True


def test_v0428_integrated_document_exists_and_has_required_sections() -> None:
    text = Path(v0428.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    for section in v0428.REQUIRED_V0428_DOC_SECTIONS:
        assert f"## {section}" in text


def test_v0428_integrated_document_contains_user_observed_failure_and_copy_paste_restore_prompt() -> None:
    text = Path(v0428.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert 'assistant_response_preview=""' in text
    assert "status=\"completed\"" in text
    assert "Copy-Paste Restore Prompt" in text


def test_v0428_no_separate_v0428_restore_provider_identity_or_command_docs_created() -> None:
    forbidden = [
        Path("docs/versions/v0.42/v0.42.8_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.8_provider_response.md"),
        Path("docs/versions/v0.42/v0.42.8_runtime_identity.md"),
        Path("docs/versions/v0.42/v0.42.8_command_surface.md"),
    ]
    assert all(not item.exists() for item in forbidden)


def test_v0428_no_forbidden_runtime_call_patterns_except_existing_provider_run_and_bounded_response_parsing() -> None:
    files = [
        Path("src/chanta_core/personal_runtime/default_personal_provider_response.py"),
        Path("src/chanta_core/personal_runtime/default_personal_run.py"),
        Path("src/chanta_core/personal_runtime/default_personal_trace_report.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    forbidden = ["subprocess", "shell=True", "os.system", "eval(", "exec(", "apply_patch", "git apply", "run_subagent", "create_child_session", "spawn_agent"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text
    run_text = Path("src/chanta_core/personal_runtime/default_personal_run.py").read_text(encoding="utf-8")
    assert "chat/completions" in run_text
    assert '"tools"' not in run_text
