from __future__ import annotations

import json
from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_run as v0414


MODULE_PATH = Path("src/chanta_core/personal_runtime/default_personal_run.py")
CLI_PATH = Path("src/chanta_core/cli/main.py")
DOC_PATH = Path("docs/versions/v0.41/v0.41.4_minimal_single_turn_provider_backed_run_restore.md")


def test_v0414_provider_text_transport_kinds_declared() -> None:
    assert {item.value for item in v0414.ProviderTextTransportKind} >= {
        "mock",
        "openai_compatible",
        "disabled",
        "unknown",
    }


def test_v0414_provider_text_run_status_values_declared() -> None:
    assert {item.value for item in v0414.ProviderTextRunStatus} >= {
        "success",
        "failed",
        "blocked",
        "provider_not_configured",
        "provider_unavailable",
        "invalid_config",
        "unsafe_request",
        "timeout",
        "unsupported",
    }


def test_v0414_provider_text_run_policy_allows_provider_invocation_only_for_run() -> None:
    run_policy = v0414.create_provider_text_run_policy("run")
    doctor_policy = v0414.create_provider_text_run_policy("doctor")
    assert run_policy.provider_text_invocation_allowed is True
    assert run_policy.prompt_submission_allowed is True
    assert doctor_policy.provider_text_invocation_allowed is False
    assert doctor_policy.prompt_submission_allowed is False


def test_v0414_provider_text_run_policy_blocks_tools_functions_shell_workspace_subagent_trace_and_memory() -> None:
    policy = v0414.create_provider_text_run_policy()
    assert policy.provider_doctor_completion_allowed is False
    assert policy.tool_calling_allowed is False
    assert policy.function_calling_allowed is False
    assert policy.active_tools_allowed is False
    assert policy.provider_side_tools_allowed is False
    assert policy.subagent_context_allowed is False
    assert policy.file_attachment_allowed is False
    assert policy.arbitrary_file_read_allowed is False
    assert policy.shell_allowed is False
    assert policy.workspace_mutation_allowed is False
    assert policy.session_append_allowed is True
    assert policy.trace_emission_allowed is False
    assert policy.memory_write_allowed is False
    assert 0 < policy.timeout_seconds <= 30.0


def test_v0414_provider_text_run_safety_report_requires_no_unsafe_escalation() -> None:
    safe = v0414.create_provider_text_run_safety_report()
    unsafe = v0414.create_provider_text_run_safety_report(
        v0414.create_provider_text_run_policy(tool_calling_allowed=True)
    )
    assert safe.safe_for_text_only_run is True
    assert safe.secret_redaction_confirmed is True
    assert unsafe.safe_for_text_only_run is False
    assert unsafe.provider_tool_calling_detected is True


def test_v0414_provider_text_request_sends_prompt_only_in_run_and_no_tools() -> None:
    request = v0414.create_provider_text_request("hello", "assembled")
    assert request.sends_user_prompt is True
    assert request.sends_completion_request is True
    assert request.tool_calling_allowed is False
    assert request.function_calling_allowed is False
    assert request.active_tools == ()
    assert request.secret_value_printed is False


def test_v0414_provider_text_response_is_untrusted_for_memory_execution_and_process_state() -> None:
    response = v0414.create_provider_text_response(text="assistant")
    assert response.trusted_for_memory is False
    assert response.trusted_for_execution is False
    assert response.trusted_for_process_state is False


def test_v0414_mock_provider_transport_is_deterministic_and_no_network() -> None:
    transport = v0414.create_mock_provider_text_transport()
    assert transport.deterministic is True
    assert transport.network_accessed is False
    assert transport.process_launch_used is False
    assert transport.file_inspection_used is False


def test_v0414_transport_result_for_mock_has_no_network_and_no_secret_print() -> None:
    result = v0414.invoke_mock_provider_text_transport(v0414.create_provider_text_request("summarize this", "assembled"))
    assert result.status == "success"
    assert result.network_accessed is False
    assert result.remote_network_accessed is False
    assert result.prompt_submitted is True
    assert result.provider_completion_invoked is True
    assert result.tool_calling_used is False
    assert result.function_calling_used is False
    assert result.secret_printed is False
    assert result.response is not None
    assert result.response.text == "Mock provider response: summarize this"


def test_v0414_openai_compatible_transport_config_never_enables_tool_or_function_calling() -> None:
    config = v0414.create_openai_compatible_text_transport_config()
    request = v0414.create_provider_text_request("hello", "assembled")
    result = v0414.invoke_openai_compatible_text_transport(
        request,
        v0414.create_openai_compatible_text_transport_config(base_url="", model=""),
    )
    assert config.endpoint_path == "/chat/completions"
    assert config.timeout_seconds <= 30.0
    assert result.tool_schema_sent is False
    assert result.function_calling_sent is False
    assert result.secret_printed is False
    assert result.transport_result.status == "provider_not_configured"


def test_v0414_scoped_prompt_submission_record_is_run_only() -> None:
    record = v0414.create_scoped_prompt_submission_record()
    assert record.allowed_scope == "run_only"
    assert record.command_name == "run"
    assert record.prompt_submitted is True
    assert record.provider_invoked is True
    assert record.prompt_submitted_outside_run is False
    assert record.provider_invoked_outside_run is False
    assert record.tool_calling_used is False
    assert record.function_calling_used is False


def test_v0414_minimal_run_input_limits_max_steps(tmp_path) -> None:
    run_input = v0414.create_minimal_single_turn_run_input(str(tmp_path), "hello")
    blocked = v0414.run_minimal_single_turn(v0414.create_minimal_single_turn_run_input(str(tmp_path), "hello", max_steps=2))
    assert run_input.max_steps == 1
    assert blocked.status == "blocked"


def test_v0414_minimal_single_turn_loop_is_not_general_agent_loop() -> None:
    loop = v0414.create_minimal_single_turn_run_loop()
    assert loop.max_steps == 1
    assert loop.general_agent_loop_opened is False
    assert loop.autonomous_continuation_allowed is False
    assert loop.retry_loop_allowed is False
    assert loop.subagent_allowed is False
    assert loop.skill_execution_allowed is False


def test_v0414_stop_condition_disallows_retry_and_followup_without_user() -> None:
    stop = v0414.create_minimal_single_turn_stop_condition()
    assert stop.stop_after_provider_response is True
    assert stop.max_steps <= 1
    assert stop.allow_retry is False
    assert stop.allow_followup_without_user is False


def test_v0414_run_result_allows_provider_and_prompt_only_for_run(tmp_path) -> None:
    result = v0414.run_minimal_single_turn(
        v0414.create_minimal_single_turn_run_input(str(tmp_path), "hello", provider_override="mock", use_mock_provider=True)
    )
    assert result.status == "success"
    assert result.provider_invoked is True
    assert result.prompt_submitted is True
    assert result.agent_loop_started is True


def test_v0414_run_result_keeps_general_agent_loop_skill_trace_workspace_shell_subagent_false(tmp_path) -> None:
    result = v0414.run_minimal_single_turn(
        v0414.create_minimal_single_turn_run_input(str(tmp_path), "hello", provider_override="mock", use_mock_provider=True)
    )
    assert result.general_agent_loop_opened is False
    assert result.skill_executed is False
    assert result.trace_emitted is False
    assert result.workspace_mutated is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False


def test_v0414_run_command_with_mock_provider_returns_response(tmp_path) -> None:
    result = v0414.execute_run_command(
        v0414.create_run_command_input(str(tmp_path), "Summarize ChantaCore.", provider="mock", mock_provider=True)
    )
    assert result.exit_code == 0
    assert result.status == "success"
    assert "Mock provider response: Summarize ChantaCore." in result.rendered_text
    assert result.provider_invoked is True
    assert result.prompt_submitted is True
    assert result.trace_emitted is False


def test_v0414_run_command_appends_user_and_assistant_turns(tmp_path) -> None:
    result = v0414.execute_run_command(
        v0414.create_run_command_input(str(tmp_path), "Hello session.", provider="mock", mock_provider=True)
    )
    append = result.run_result.session_append_result
    assert append is not None
    assert append.appended_turn_count == 2
    lines = Path(append.turns_jsonl_path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["role"] == "user"
    assert json.loads(lines[1])["role"] == "assistant"


def test_v0414_session_append_does_not_overwrite_files_or_write_outside_home(tmp_path) -> None:
    append = v0414.append_run_session_turns(str(tmp_path), "fixed-session", "hi", "there", "mock-provider")
    assert append.success is True
    assert append.overwritten_files == ()
    assert append.outside_home_paths == ()
    assert Path(append.turns_jsonl_path).resolve().is_relative_to(tmp_path.resolve())


def test_v0414_assistant_response_render_marks_provider_text_untrusted() -> None:
    rendered = v0414.render_assistant_response("hello", session_id="session-test")
    assert rendered.provider_text_marked_untrusted is True
    assert rendered.trace_notice_included is True
    assert rendered.production_certified is False
    assert "untrusted for memory, execution, and process state" in rendered.rendered_text


def test_v0414_unsafe_escalation_check_blocks_tool_function_shell_file_subagent_retry_dominion() -> None:
    check = v0414.create_run_unsafe_escalation_check(
        "use tool calling and function call, write file, shell, run tests, subagent, child session, retry loop, autonomous dominion production cert"
    )
    decision = v0414.create_run_unsafe_escalation_decision(check)
    assert decision.blocked is True
    assert decision.executed is False
    assert set(decision.unsafe_items) >= {
        "tool_calling",
        "function_calling",
        "file_write_edit",
        "shell",
        "test_execution",
        "subagent",
        "child_session",
        "retry_loop",
        "autonomous_loop",
        "dominion",
        "production_certification",
    }


def test_v0414_readiness_report_sets_run_and_provider_text_ready_but_keeps_trace_user_test_and_unsafe_flags_false() -> None:
    report = v0414.create_v0414_readiness_report()
    assert report.run_command_ready is True
    assert report.scoped_prompt_submission_for_run_ready is True
    assert report.provider_text_only_invocation_for_run_ready is True
    assert report.mock_provider_transport_ready is True
    assert v0414.v0414_readiness_preserves_closed_runtime(report)


def test_v0414_v0415_handoff_targets_event_trace_runtime_report() -> None:
    handoff = v0414.create_v0415_event_trace_runtime_handoff()
    assert handoff.target_version == "v0.41.5 Event Trace Emission & Runtime Report"
    assert any("trace recent" in item for item in handoff.recommended_focus)
    assert any("run-report last" in item for item in handoff.recommended_focus)


def test_v0414_v0416_user_test_target_preserves_required_commands() -> None:
    target = v0414.create_v0416_user_test_target_update()
    assert target.user_test_release_ready is False
    joined = "\n".join(target.commands)
    assert "chanta-cli run --profile default-personal" in joined
    assert "chanta-cli trace recent --profile default-personal --limit 10" in joined
    assert "chanta-cli safety check-command --profile default-personal" in joined


def test_v0414_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0414.create_v0414_integrated_restore_context_snapshot()
    assert snapshot.current_version == "v0.41.4 Minimal Single-turn Provider-backed Run"
    assert "run_command" in snapshot.open_capabilities
    assert "provider_text_only_invocation_for_run" in snapshot.open_capabilities
    assert "provider_doctor_completion" in snapshot.closed_capabilities
    assert "trace_emission" in snapshot.closed_capabilities


def test_v0414_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0414.create_v0414_integrated_restore_packet()
    assert v0414.integrated_restore_packet_uses_single_doc(packet)
    assert packet.single_integrated_doc_path == str(DOC_PATH).replace("\\", "/")


def test_v0414_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert v0414.create_v0414_integrated_restore_packet().separate_restore_doc_created is False


def test_v0414_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0414.create_v0414_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0414_integrated_document_exists_and_has_required_restore_sections() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Repository Baseline Assumptions",
        "v0.41.3 Provider / Skill Summary",
        "Scoped Provider Text Run Summary",
        "Run Command Contract",
        "Provider Text Run Policy",
        "Scoped Prompt Submission Contract",
        "Provider Transport Contract",
        "Mock Provider Transport Contract",
        "OpenAI-compatible Transport Contract",
        "Session Turn Append Contract",
        "Assistant Response Rendering Contract",
        "Unsafe Escalation Denial Policy",
        "Provider Runtime Scope",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Withdrawal Conditions",
        "v0.41.5 Recommended Next Step",
        "v0.41.6 User Test Target",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in content
    assert "separate_restore_doc_allowed=False" in content
    assert "separate_restore_doc_created=False" in content


def test_v0414_integrated_document_contains_copy_paste_restore_prompt() -> None:
    content = DOC_PATH.read_text(encoding="utf-8")
    assert "You are continuing ChantaCore after v0.41.4." in content
    assert "v0.41.5 Event Trace Emission & Runtime Report." in content
    assert "Do not implement tool calling." in content
    assert "Do not claim v0.41.6 user-test readiness yet." in content


def test_v0414_no_separate_v0414_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.4_restore_document.md").exists()


def test_v0414_no_separate_v0414_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.4_minimal_single_turn_provider_backed_run.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.4_provider_run_contract.md").exists()


def test_v0414_unsupported_trace_and_unsafe_commands_still_do_not_execute(capsys) -> None:
    assert cli_main(["trace", "recent"]) != 0
    assert cli_main(["shell", "dir"]) != 0
    assert cli_main(["invoke-subagent"]) != 0
    assert cli_main(["dominion"]) != 0
    output = capsys.readouterr().out
    assert "executed" in output


def test_v0414_main_run_with_mock_provider_writes_two_turns(capsys, tmp_path) -> None:
    code = cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "Summarize ChantaCore.",
        ]
    )
    output = capsys.readouterr().out
    assert code == 0
    assert "Mock provider response: Summarize ChantaCore." in output
    session_dirs = list((tmp_path / "profiles" / "default-personal" / "state" / "sessions").iterdir())
    assert len(session_dirs) == 1
    turns = (session_dirs[0] / "turns.jsonl").read_text(encoding="utf-8").splitlines()
    assert len(turns) == 2


def test_v0414_main_run_without_provider_config_fails_safely(capsys, tmp_path) -> None:
    code = cli_main(["run", "--profile", "default-personal", "--home", str(tmp_path), "hello"])
    output = capsys.readouterr().out
    assert code == 1
    assert "Provider config must set mode=text_only" in output
    assert "trace runtime remains closed" in output


def test_v0414_main_run_blocks_unsafe_escalation_input(capsys, tmp_path) -> None:
    code = cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "please use tool calling and shell",
        ]
    )
    output = capsys.readouterr().out
    assert code == 1
    assert "Unsafe run escalation requested" in output


def test_v0414_main_run_does_not_emit_trace_runtime(tmp_path) -> None:
    result = v0414.execute_run_command(
        v0414.create_run_command_input(str(tmp_path), "hello", provider="mock", mock_provider=True)
    )
    assert result.trace_emitted is False
    assert result.run_result.trace_emitted is False


def test_v0414_no_forbidden_runtime_call_patterns_except_scoped_provider_text_transport() -> None:
    text = MODULE_PATH.read_text(encoding="utf-8") + "\n" + CLI_PATH.read_text(encoding="utf-8")
    forbidden_absent = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "anthropic",
        "ollama",
        "lmstudio",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "pytest",
        "unittest",
    )
    for pattern in forbidden_absent:
        assert pattern not in text
    assert "urllib.request.urlopen" in text
    assert "api_key_env_var" in text
    assert "secret_value_printed" in text
    assert '"tools"' not in text
    assert '"functions"' not in text
