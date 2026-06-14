from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_chat_shell as v0424
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart


def _prepared_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    result = run_v042_quickstart(explicit_home=str(home), with_mock_run=True)
    assert result.exit_code == 0
    return home


def test_v0424_chat_shell_modes_declared() -> None:
    assert {item.value for item in v0424.V042ChatShellMode} == {"interactive", "scripted_test", "dry_run", "unknown"}


def test_v0424_chat_shell_status_values_declared() -> None:
    assert {item.value for item in v0424.V042ChatShellStatus} == {
        "started",
        "waiting_for_input",
        "turn_completed",
        "internal_command_completed",
        "denied",
        "exited",
        "failed",
        "blocked",
    }


def test_v0424_chat_shell_input_kinds_declared() -> None:
    assert {item.value for item in v0424.V042ChatShellInputKind} == {
        "user_message",
        "internal_command",
        "empty",
        "exit",
        "unsafe_command_like_text",
        "unknown",
    }


def test_v0424_internal_command_kinds_declared() -> None:
    assert {item.value for item in v0424.V042ChatShellInternalCommandKind} == {
        "help",
        "exit",
        "quit",
        "status",
        "provider",
        "history",
        "trace",
        "run_last",
        "session",
        "handoff",
        "safety",
        "unknown",
    }


def test_v0424_chat_shell_loop_policy_is_ui_loop_not_agent_loop() -> None:
    policy = v0424.create_v042_chat_shell_loop_policy()
    assert policy.ui_loop_allowed is True
    assert policy.agent_loop_allowed is False
    assert policy.one_run_per_user_message is True
    assert policy.internal_commands_call_provider is False


def test_v0424_chat_shell_loop_policy_disallows_autonomous_continuation_retry_shell_subagent_tools_functions_and_production() -> None:
    policy = v0424.create_v042_chat_shell_loop_policy()
    assert policy.autonomous_continuation_allowed is False
    assert policy.retry_loop_allowed is False
    assert policy.shell_execution_allowed is False
    assert policy.subagent_allowed is False
    assert policy.tool_calling_allowed is False
    assert policy.function_calling_allowed is False
    assert policy.production_certified is False


def test_v0424_chat_shell_config_uses_default_home_resolver_and_allows_mock_provider() -> None:
    config = v0424.create_v042_chat_shell_config(provider_mode="mock", max_turns=1000)
    assert config.use_default_home_resolver is True
    assert config.internal_commands_enabled is True
    assert config.allow_mock_provider is True
    assert config.max_turns == 200


def test_v0424_chat_shell_internal_commands_never_call_provider_or_submit_prompt() -> None:
    state = v0424.create_v042_chat_shell_session_state(resolved_home_path="C:/tmp/home")
    for raw in ["/help", "/status", "/provider", "/history", "/trace", "/session", "/handoff", "/safety", "/exit"]:
        command = v0424.parse_v042_chat_shell_internal_command(raw)
        assert command.provider_call_allowed is False
        assert command.prompt_submission_allowed is False
        assert command.mutates_filesystem is False
        if raw not in {"/provider", "/history", "/trace", "/session"}:
            result = v0424.create_v042_chat_shell_internal_command_result(command, state)
            assert result.provider_invoked is False
            assert result.prompt_submitted is False
            assert result.shell_executed is False
            assert result.subagent_invoked is False
            assert result.production_certified is False


def test_v0424_help_view_lists_expected_internal_commands_and_safety_statement() -> None:
    view = v0424.create_v042_chat_shell_help_view()
    for command in ["/help", "/exit", "/status", "/provider", "/history", "/trace", "/run last", "/session", "/handoff", "/safety"]:
        assert command in view.commands
        assert command in view.rendered_text
    assert "Shell commands are not executed" in view.safety_statement


def test_v0424_status_view_includes_profile_home_session_provider_and_closed_capabilities() -> None:
    state = v0424.create_v042_chat_shell_session_state(resolved_home_path="C:/tmp/home", session_id="session-1", provider_mode="mock")
    view = v0424.create_v042_chat_shell_status_view(state)
    assert "default-personal" in view.rendered_text
    assert "C:/tmp/home" in view.rendered_text
    assert "session-1" in view.rendered_text
    assert "mock" in view.rendered_text
    assert "closed" in view.rendered_text
    assert view.high_risk_capabilities_closed is True


def test_v0424_provider_view_does_not_call_provider_or_reveal_secrets(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    state = v0424.create_v042_chat_shell_session_state(resolved_home_path=str(home))
    view = v0424.create_v042_chat_shell_provider_view(state)
    assert view.provider_invoked is False
    assert view.secret_values_redacted is True
    assert "secrets: redacted" in view.rendered_text


def test_v0424_history_view_uses_run_history_without_provider_call(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    state = v0424.create_v042_chat_shell_session_state(resolved_home_path=str(home))
    view = v0424.create_v042_chat_shell_history_view(state)
    assert view.provider_invoked is False
    assert "Run History" in view.rendered_text


def test_v0424_trace_view_uses_trace_timeline_without_mutation(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    state = v0424.create_v042_chat_shell_session_state(resolved_home_path=str(home))
    view = v0424.create_v042_chat_shell_trace_view(state)
    assert view.provider_invoked is False
    assert view.mutated_filesystem is False
    assert "Trace Timeline" in view.rendered_text


def test_v0424_session_view_marks_provider_text_untrusted(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock")
    state = v0424.create_v042_chat_shell_session_state(
        resolved_home_path=str(home),
        session_id=result.summary.session_id,
        provider_mode="mock",
        turn_count=1,
        run_ids=result.summary.run_ids,
    )
    view = v0424.create_v042_chat_shell_session_view(state)
    assert view.provider_invoked is False
    assert view.provider_text_untrusted is True
    assert "trusted_execution=false" in view.rendered_text


def test_v0424_user_message_executes_existing_single_turn_run_once(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["Summarize what ChantaCore is in three bullets.", "/exit"], home_path=str(home), provider="mock")
    assert result.summary.user_message_count == 1
    assert result.summary.run_count == 1
    assert len(result.turn_results) == 1
    assert result.turn_results[0].run_id is not None
    assert result.turn_results[0].provider_invoked is True
    assert result.turn_results[0].prompt_submitted is True


def test_v0424_user_message_result_keeps_shell_skill_subagent_autonomous_retry_and_production_false(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock")
    turn = result.turn_results[0]
    assert turn.shell_executed is False
    assert turn.skill_executed is False
    assert turn.subagent_invoked is False
    assert turn.autonomous_continuation_started is False
    assert turn.retry_loop_started is False
    assert turn.production_certified is False


def test_v0424_run_invocation_record_marks_scoped_single_turn_and_no_tools_or_functions(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    turn = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock").turn_results[0]
    record = v0424.create_v042_chat_shell_run_invocation_record(turn, "hello", 1, "mock")
    assert record.invoked_existing_run_path is True
    assert record.scoped_single_turn is True
    assert record.tool_calling_used is False
    assert record.function_calling_used is False
    assert record.shell_executed is False
    assert record.subagent_invoked is False


def test_v0424_exit_and_quit_commands_exit_gracefully(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    assert v0424.run_v042_chat_shell_scripted(["/exit"], home_path=str(home)).exited is True
    assert v0424.run_v042_chat_shell_scripted(["/quit"], home_path=str(home)).exited is True


def test_v0424_unsafe_command_like_input_is_denied_or_warned_without_execution(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["Remove-Item -Recurse -Force C:\\", "/exit"], home_path=str(home), provider="mock")
    assert result.turn_results[0].status == "denied"
    assert result.turn_results[0].provider_invoked is False
    assert result.turn_results[0].prompt_submitted is False
    assert result.turn_results[0].shell_executed is False
    assert result.summary.denial_count >= 1


def test_v0424_chat_summary_counts_runs_internal_commands_and_zero_high_risk_counts(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    summary = v0424.run_v042_chat_shell_scripted(["/help", "hello", "/exit"], home_path=str(home), provider="mock").summary
    assert summary.total_inputs == 3
    assert summary.user_message_count == 1
    assert summary.internal_command_count == 2
    assert summary.run_count == 1
    assert summary.shell_execution_count == 0
    assert summary.skill_execution_count == 0
    assert summary.subagent_invocation_count == 0
    assert summary.production_certification_count == 0


def test_v0424_debug_handoff_contains_session_run_safety_context_and_no_secrets(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock")
    state = v0424.create_v042_chat_shell_session_state(
        resolved_home_path=str(home),
        session_id=result.summary.session_id,
        provider_mode="mock",
        turn_count=1,
        run_ids=result.summary.run_ids,
    )
    handoff = v0424.create_v042_chat_shell_debug_handoff(state)
    assert result.summary.session_id in handoff.concise_text
    assert result.summary.run_ids[0] in handoff.concise_text
    assert "shell=0" in handoff.concise_text
    assert handoff.includes_secret_values is False
    assert handoff.suitable_for_gpt_or_codex is True


def test_v0424_render_policy_marks_provider_text_untrusted_and_redacts_secrets() -> None:
    policy = v0424.create_v042_chat_shell_render_policy()
    assert policy.mark_provider_text_untrusted is True
    assert policy.redact_secrets is True
    assert policy.show_run_id_after_turn is True


def test_v0424_safety_report_opens_ui_loop_but_keeps_agent_loop_retry_tools_functions_shell_subagent_and_production_closed() -> None:
    report = v0424.create_v042_chat_shell_safety_report()
    assert report.ui_loop_opened is True
    assert report.agent_loop_opened is False
    assert report.autonomous_continuation_allowed is False
    assert report.retry_loop_allowed is False
    assert report.provider_tool_calling_allowed is False
    assert report.function_calling_allowed is False
    assert report.shell_execution_allowed is False
    assert report.subagent_invocation_allowed is False
    assert report.production_certified is False


def test_v0424_scripted_run_helper_processes_help_message_exit_without_subprocess(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["/help", "hello", "/exit"], home_path=str(home), provider="mock")
    assert result.inputs_processed == 3
    assert result.exited is True
    assert any("Chat Help" in output for output in result.outputs)
    assert result.shell_executed is False
    assert result.subagent_invoked is False


def test_v0424_scripted_run_helper_with_mock_message_creates_one_run_and_exits(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock")
    assert result.summary.run_count == 1
    assert result.provider_invoked_count == 1
    assert result.prompt_submitted_count == 1
    assert result.production_certified is False


def test_v0424_readiness_report_sets_chat_manual_ui_flags_true() -> None:
    report = v0424.create_v0424_readiness_report()
    assert report.chat_command_ready is True
    assert report.manual_ui_loop_ready is True
    assert report.one_run_per_user_message_ready is True
    assert report.internal_help_command_ready is True
    assert report.internal_exit_command_ready is True
    assert report.internal_status_command_ready is True
    assert report.chat_shell_scripted_test_helper_ready is True
    assert report.integrated_restore_document_ready is True


def test_v0424_readiness_report_keeps_agentloop_retry_skill_shell_subagent_and_production_flags_false() -> None:
    report = v0424.create_v0424_readiness_report()
    assert report.ready_for_autonomous_agent_loop is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_multi_step_agent_loop is False
    assert report.ready_for_retry_loop is False
    assert report.ready_for_read_only_skill_execution_as_actions is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.production_certified is False


def test_v0424_v0425_handoff_targets_bounded_read_only_skill_execution() -> None:
    handoff = v0424.create_v0425_bounded_read_only_skill_execution_handoff()
    assert "Bounded Read-only Skill Execution" in handoff.target_version
    assert "shell_execution" in handoff.must_not_open
    assert handoff.production_certified is False


def test_v0424_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0424.create_v0424_integrated_restore_context_snapshot()
    assert snapshot.current_version == "v0.42.4 Interactive Manual Chat Shell"
    assert "chat_command" in snapshot.open_capabilities
    assert "manual_ui_loop" in snapshot.open_capabilities
    assert "autonomous_agent_loop" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0424_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0424.create_v0424_integrated_restore_packet()
    assert packet.single_integrated_doc_path == "docs/versions/v0.42/v0.42.4_interactive_manual_chat_shell_restore.md"


def test_v0424_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0424.create_v0424_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0424_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0424.create_v0424_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0424_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path("docs/versions/v0.42/v0.42.4_interactive_manual_chat_shell_restore.md").read_text(encoding="utf-8")
    for section in v0424.REQUIRED_V0424_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0424_integrated_document_contains_chat_shell_examples_and_copy_paste_restore_prompt() -> None:
    text = Path("docs/versions/v0.42/v0.42.4_interactive_manual_chat_shell_restore.md").read_text(encoding="utf-8")
    assert "chanta-cli chat" in text
    assert "/help" in text
    assert "/exit" in text
    assert "You are continuing ChantaCore after v0.42.4." in text


def test_v0424_no_separate_v0424_restore_or_chat_documents_created() -> None:
    forbidden = [
        Path("docs/versions/v0.42/v0.42.4_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.4_interactive_chat_shell.md"),
        Path("docs/versions/v0.42/v0.42.4_manual_chat_contract.md"),
        Path("docs/versions/v0.42/v0.42.4_chat_user_guide.md"),
    ]
    assert all(not path.exists() for path in forbidden)


def test_v0424_no_forbidden_runtime_call_patterns_except_existing_single_turn_run_and_bounded_reads() -> None:
    files = [
        Path("src/chanta_core/personal_runtime/default_personal_chat_shell.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    forbidden = [
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "openai",
        "anthropic",
        "ollama",
        "lmstudio",
        "apply_patch",
        "git apply",
        "git worktree",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "pytest",
        "unittest",
    ]
    for path in files:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text
        assert "invoke_subagent(" not in text


def test_v0424_cli_quickstart_with_mock_run_then_chat_scripted_two_messages(tmp_path: Path) -> None:
    home = tmp_path / "home"
    assert cli_main(["quickstart", "--home", str(home), "--with-mock-run"]) == 0
    result = v0424.run_v042_chat_shell_scripted(["hello", "again", "/exit"], home_path=str(home), provider="mock")
    assert result.summary.user_message_count == 2
    assert result.summary.run_count == 2


def test_v0424_cli_chat_scripted_help_status_provider_history_trace_exit(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["/help", "/status", "/provider", "/history", "/trace", "/exit"], home_path=str(home), provider="mock")
    assert result.summary.internal_command_count == 6
    assert all(item.provider_invoked is False for item in result.internal_command_results)
    assert all(item.prompt_submitted is False for item in result.internal_command_results)


def test_v0424_cli_chat_user_message_then_run_history_shows_new_run(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["hello", "/exit"], home_path=str(home), provider="mock")
    assert result.summary.run_ids
    history = v0424.create_v042_chat_shell_history_view(
        v0424.create_v042_chat_shell_session_state(resolved_home_path=str(home), session_id=result.summary.session_id)
    )
    assert result.summary.run_ids[0] in history.rendered_text


def test_v0424_cli_chat_unsafe_shell_like_input_never_executes(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0424.run_v042_chat_shell_scripted(["Remove-Item -Recurse -Force C:\\", "/exit"], home_path=str(home), provider="mock")
    assert result.shell_executed is False
    assert result.provider_invoked_count == 0
    assert result.summary.denial_count >= 1


def test_v0424_cli_chat_json_startup_summary(tmp_path: Path, capsys) -> None:
    home = _prepared_home(tmp_path)
    assert cli_main(["chat", "--home", str(home), "--provider", "mock", "--json"]) == 0
    output = capsys.readouterr().out
    assert '"provider_mode": "mock"' in output
