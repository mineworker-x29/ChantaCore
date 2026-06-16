from __future__ import annotations

import json
from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_chat_shell as v0424
from chanta_core.personal_runtime import default_personal_provider_connectivity as v0427
from chanta_core.personal_runtime import default_personal_run as v0414
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart
from chanta_core.personal_runtime.default_personal_provider_setup import (
    create_v042_provider_status_report,
    create_v042_provider_status_request,
)


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


def _setup_local_provider(home: Path, model: str = "local-model") -> None:
    assert cli_main(["provider", "setup", "local-openai", "--home", str(home), "--base-url", "http://localhost:1234/v1", "--model", model]) == 0


def _trace_text(home: Path) -> str:
    path = home / "profiles" / "default-personal" / "state" / "traces" / "events.jsonl"
    return path.read_text(encoding="utf-8")


def test_v0427_run_help_shows_usage_and_does_not_require_home_or_prompt(capsys) -> None:
    assert cli_main(["run", "--help"]) == 0
    output = capsys.readouterr().out
    assert "usage: chanta-cli run" in output
    assert "--provider" in output
    assert "--profile" in output
    assert "--home" in output
    assert "prompt" in output
    assert "invalid_config" not in output


def test_v0427_configured_provider_run_uses_traced_v0415_path_not_old_v0414_path(tmp_path: Path, monkeypatch, capsys) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)

    def fake_urlopen(request, timeout):  # noqa: ANN001
        assert request.full_url.endswith("/chat/completions")
        return _FakeResponse({"choices": [{"message": {"content": "configured response"}}]})

    monkeypatch.setattr(v0414.urllib.request, "urlopen", fake_urlopen)
    assert cli_main(["run", "--home", str(home), "--provider", "configured", "--timeout", "60", "hello"]) == 0
    output = capsys.readouterr().out
    assert "[v0.41.5 traced single-turn text-only run]" in output
    assert "trace runtime emitted bounded append-only events in v0.41.5" in output
    assert "trace runtime remains closed until v0.41.5" not in output
    trace = _trace_text(home)
    assert "provider_text_call_started" in trace
    assert "provider_text_call_completed" in trace
    assert "run_completed" in trace


def test_v0427_configured_provider_timeout_returns_structured_error_class_and_next_actions(tmp_path: Path, monkeypatch, capsys) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)

    def fake_urlopen(request, timeout):  # noqa: ANN001
        raise TimeoutError("timed out")

    monkeypatch.setattr(v0414.urllib.request, "urlopen", fake_urlopen)
    assert cli_main(["run", "--home", str(home), "--provider", "configured", "--timeout", "120", "hello"]) == 1
    output = capsys.readouterr().out
    assert "Configured provider run failed." in output
    assert "trace runtime remains closed until v0.41.5" not in output
    assert "run chanta-cli provider connectivity" in output
    assert "try a smaller model" in output
    assert cli_main(["run-report", "last", "--home", str(home)]) == 0
    report_output = capsys.readouterr().out
    assert "provider_timeout" in report_output
    assert '"provider_invoked": true' in report_output
    assert '"prompt_submitted": true' in report_output
    assert '"shell_executed": false' in report_output


def test_v0427_configured_provider_timeout_appends_failure_trace_without_shell_subagent_or_production(tmp_path: Path, monkeypatch) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)

    def fake_urlopen(request, timeout):  # noqa: ANN001
        raise TimeoutError("timed out")

    monkeypatch.setattr(v0414.urllib.request, "urlopen", fake_urlopen)
    assert cli_main(["run", "--home", str(home), "--provider", "configured", "--timeout", "2", "hello"]) == 1
    trace = _trace_text(home)
    assert "provider_text_call_failed" in trace
    assert "run_failed" in trace
    assert "provider_timeout" in trace
    latest_run_segment = trace.rsplit("run_failed", 1)[0]
    assert "assistant_response_recorded" not in latest_run_segment.split("run_started")[-1]
    assert '"shell_executed": false' in trace
    assert '"subagent_invoked": false' in trace
    assert '"production_certified": false' in trace


def test_v0427_provider_connectivity_probe_uses_models_endpoint_only_no_completion(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)
    seen_urls: list[str] = []

    def fake_urlopen(request, timeout):  # noqa: ANN001
        seen_urls.append(request.full_url)
        return _FakeResponse({"data": [{"id": "local-model"}]})

    result = v0427.probe_v0427_provider_connectivity(v0427.create_v0427_provider_connectivity_request(str(home)), urlopen=fake_urlopen)
    assert result.error_class == "none"
    assert result.configured_model_found is True
    assert seen_urls == ["http://localhost:1234/v1/models"]
    assert "chat/completions" not in "\n".join(seen_urls)
    assert result.completion_endpoint_called is False
    assert result.prompt_submitted is False


def test_v0427_provider_connectivity_reports_model_found_when_configured_model_in_models_list(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home, "qwen-local")
    result = v0427.probe_v0427_provider_connectivity(
        v0427.create_v0427_provider_connectivity_request(str(home)),
        urlopen=lambda request, timeout: _FakeResponse({"data": [{"id": "qwen-local"}, {"id": "other"}]}),
    )
    assert result.models_endpoint_reachable is True
    assert result.model_list_available is True
    assert result.configured_model_found is True
    assert "qwen-local" in result.available_model_ids


def test_v0427_provider_connectivity_reports_model_not_found_with_available_model_ids(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home, "missing-model")
    result = v0427.probe_v0427_provider_connectivity(
        v0427.create_v0427_provider_connectivity_request(str(home)),
        urlopen=lambda request, timeout: _FakeResponse({"data": [{"id": "available-model"}]}),
    )
    assert result.error_class == "model_not_found"
    assert result.configured_model_found is False
    assert result.available_model_ids == ("available-model",)


def test_v0427_provider_connectivity_classifies_endpoint_unreachable_or_timeout(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)

    def fake_urlopen(request, timeout):  # noqa: ANN001
        raise TimeoutError("timed out")

    result = v0427.probe_v0427_provider_connectivity(v0427.create_v0427_provider_connectivity_request(str(home)), urlopen=fake_urlopen)
    assert result.error_class == "models_endpoint_timeout"
    assert result.endpoint_reachable is False
    assert result.provider_invoked is False


def test_v0427_provider_status_distinguishes_mock_available_from_configured_provider_ready(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)
    report = create_v042_provider_status_report(create_v042_provider_status_request(str(home)))
    assert report.mock_provider_available is True
    assert report.active_provider_config_present is True
    assert report.configured_provider_run_ready is True
    assert "mock_provider_available: true" in report.rendered_text
    assert "configured_provider_connectivity: unknown" in report.rendered_text


def test_v0427_provider_status_never_prints_secrets(tmp_path: Path, monkeypatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "raw-secret")
    assert cli_main(["provider", "setup", "local-openai", "--home", str(home), "--base-url", "http://localhost:1234/v1", "--model", "local-model", "--api-key-env", "OPENAI_API_KEY"]) == 0
    report = create_v042_provider_status_report(create_v042_provider_status_request(str(home)))
    assert "raw-secret" not in report.rendered_text
    assert "OPENAI_API_KEY" in report.rendered_text


def test_v0427_run_timeout_option_is_supported_or_documented(capsys) -> None:
    assert cli_main(["run", "--help"]) == 0
    assert "--timeout" in capsys.readouterr().out


def test_v0427_chat_timeout_option_is_supported_or_documented(capsys) -> None:
    assert cli_main(["chat", "--help"]) == 0
    assert "--timeout" in capsys.readouterr().out


def test_v0427_chat_mock_response_printed_once(tmp_path: Path, capsys) -> None:
    home = _prepared_home(tmp_path)
    capsys.readouterr()
    result = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock")
    captured = capsys.readouterr().out
    joined = "\n".join(result.outputs)
    assert captured.count("Mock provider response") == 0
    assert joined.count("Mock provider response") == 1


def test_v0427_chat_status_updates_turn_count_latest_run_id_and_run_ids_after_message(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["hello", "/status", "/exit"], home_path=str(home), provider="mock")
    status_text = result.internal_command_results[0].rendered_text
    assert result.summary.turn_count if hasattr(result.summary, "turn_count") else result.summary.run_count == 1
    assert result.summary.run_ids
    assert "turn_count: 1" in status_text
    assert f"latest_run_id: {result.summary.run_ids[0]}" in status_text


def test_v0427_chat_provider_view_shows_configured_provider_guidance_without_calling_provider(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    _setup_local_provider(home)
    state = v0424.create_v042_chat_shell_session_state(resolved_home_path=str(home), provider_mode="configured")
    view = v0424.create_v042_chat_shell_provider_view(state)
    assert view.provider_invoked is False
    assert "mock_provider_available: true" in view.rendered_text
    assert "configured_provider_next_action" in view.rendered_text
    assert "secret" not in view.rendered_text.lower() or "redacted" in view.rendered_text.lower()


def test_v0427_chat_internal_commands_do_not_call_provider_or_submit_prompt(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["/status", "/provider", "/exit"], home_path=str(home), provider="mock")
    assert all(item.provider_invoked is False for item in result.internal_command_results)
    assert all(item.prompt_submitted is False for item in result.internal_command_results)


def test_v0427_safety_boundaries_remain_closed() -> None:
    report = v0427.create_v0427_stabilization_safety_report()
    assert report.provider_doctor_completion_opened is False
    assert report.provider_tool_calling_opened is False
    assert report.function_calling_opened is False
    assert report.shell_execution_opened is False
    assert report.subagent_invocation_opened is False
    assert report.general_agent_loop_opened is False
    assert report.retry_loop_opened is False
    assert report.production_certified is False


def test_v0427_integrated_document_exists_and_has_required_sections() -> None:
    text = Path("docs/versions/v0.42/v0.42.7_provider_connectivity_chat_ux_stabilization_restore.md").read_text(encoding="utf-8")
    for section in [
        "Restore Purpose",
        "Observed User-Test Issues",
        "Run Help Fix",
        "Configured Provider Traced Path",
        "Provider Connectivity Probe Contract",
        "Timeout and Error Classification",
        "Provider Status Semantics",
        "Chat UX Stabilization",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Command Checks",
        "v0.43 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]:
        assert f"## {section}" in text


def test_v0427_no_separate_restore_provider_or_chat_docs_created() -> None:
    forbidden = [
        Path("docs/versions/v0.42/v0.42.7_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.7_provider_connectivity.md"),
        Path("docs/versions/v0.42/v0.42.7_chat_ux_stabilization.md"),
        Path("docs/versions/v0.42/v0.42.7_provider_chat_user_guide.md"),
    ]
    assert all(not item.exists() for item in forbidden)


def test_v0427_no_forbidden_runtime_call_patterns_except_bounded_models_probe_and_existing_run_provider_call() -> None:
    files = [
        Path("src/chanta_core/personal_runtime/default_personal_provider_connectivity.py"),
        Path("src/chanta_core/personal_runtime/default_personal_run.py"),
        Path("src/chanta_core/personal_runtime/default_personal_chat_shell.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    forbidden = ["subprocess", "shell=True", "os.system", "eval(", "exec(", "apply_patch", "git apply", "git worktree", "run_subagent", "create_child_session", "spawn_agent"]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text
        assert "tools" not in text.lower() or "tool_calling" in text or "tools=false" in text or "provider tools" in text.lower()
