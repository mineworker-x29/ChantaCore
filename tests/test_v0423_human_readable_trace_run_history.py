from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_trace_history as v0423
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart


def _prepared_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    result = run_v042_quickstart(explicit_home=str(home), with_mock_run=True)
    assert result.exit_code == 0
    return home


def _run_history(home: Path) -> v0423.V042RunHistoryResult:
    return v0423.create_v042_run_history_result(v0423.create_v042_run_history_request(home_path=str(home)))


def _latest_run_id(home: Path) -> str:
    history = _run_history(home)
    assert history.runs
    return history.runs[0].run_id


def _latest_session_id(home: Path) -> str:
    history = _run_history(home)
    assert history.runs
    assert history.runs[0].session_id is not None
    return history.runs[0].session_id


def test_v0423_trace_history_display_modes_declared() -> None:
    assert {item.value for item in v0423.V042TraceHistoryDisplayMode} == {
        "timeline",
        "run_history",
        "run_show",
        "session_show",
        "debug_handoff",
        "json",
        "unknown",
    }


def test_v0423_human_readable_formats_declared() -> None:
    assert {item.value for item in v0423.V042HumanReadableFormat} == {
        "text",
        "compact_text",
        "markdown",
        "json",
        "unknown",
    }


def test_v0423_trace_timeline_item_kinds_declared() -> None:
    assert {item.value for item in v0423.V042TraceTimelineItemKind} == {
        "command",
        "profile",
        "provider",
        "prompt",
        "run",
        "session",
        "assistant_response",
        "denial",
        "safety",
        "trace",
        "unknown",
    }


def test_v0423_trace_timeline_status_values_declared() -> None:
    assert {item.value for item in v0423.V042TraceTimelineStatus} == {
        "completed",
        "started",
        "info",
        "denied",
        "failed",
        "warning",
        "skipped",
        "unknown",
    }


def test_v0423_timeline_item_keeps_shell_subagent_and_production_false() -> None:
    item = v0423.create_v042_trace_timeline_item(
        {
            "event_kind": "run_completed",
            "status": "completed",
            "created_at": "2026-06-14T00:00:00Z",
            "message": "run completed",
            "run_id": "run-1",
        },
        0,
    )
    assert item.shell_executed is False
    assert item.subagent_invoked is False
    assert item.production_certified is False


def test_v0423_trace_timeline_request_is_bounded_and_read_only() -> None:
    request = v0423.create_v042_trace_timeline_request(limit=10000)
    assert request.limit == 200
    assert request.home_path is None
    assert request.display_format == "text"


def test_v0423_trace_timeline_result_does_not_invoke_provider_submit_prompt_or_mutate_files(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0423.create_v042_trace_timeline_result(v0423.create_v042_trace_timeline_request(home_path=str(home)))
    assert result.event_count > 0
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.mutated_filesystem is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False


def test_v0423_provider_call_count_semantics_distinguishes_events_from_transactions(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    events = v0423.load_v042_trace_events(str(home))
    semantics = v0423.create_v042_provider_call_count_semantics(events)
    assert semantics.provider_call_event_count == 2
    assert semantics.provider_call_transaction_count == 1
    assert "provider_text_call_started" in semantics.explanation
    assert "provider_text_call_completed" in semantics.explanation


def test_v0423_run_lifecycle_status_values_declared() -> None:
    assert {item.value for item in v0423.V042RunLifecycleStatus} == {"completed", "started", "failed", "incomplete", "unknown"}


def test_v0423_run_history_item_groups_run_and_session_and_keeps_safety_counts_zero(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    item = _run_history(home).runs[0]
    assert item.run_id
    assert item.session_id
    assert item.mock_provider is True
    assert item.provider_call_transaction_count == 1
    assert item.session_turns_appended is True
    assert item.trace_event_count >= 8
    assert item.shell_executed is False
    assert item.subagent_invoked is False
    assert item.production_certified is False


def test_v0423_run_history_result_is_read_only(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = _run_history(home)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.mutated_filesystem is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False


def test_v0423_run_process_instance_view_contains_expected_v0415_lifecycle_steps(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    run_id = _latest_run_id(home)
    events = [event for event in v0423.load_v042_trace_events(str(home)) if event.get("run_id") == run_id]
    view = v0423.build_v042_run_process_instance_view(str(home), "default-personal", run_id, events)
    kinds = [step.event_kind for step in view.steps]
    assert kinds == [
        "run_started",
        "user_input_received",
        "prompt_assembled",
        "provider_text_call_started",
        "provider_text_call_completed",
        "session_turns_appended",
        "assistant_response_recorded",
        "run_completed",
    ]


def test_v0423_run_process_instance_view_marks_successful_mock_run_reconstructable(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    run_id = _latest_run_id(home)
    events = [event for event in v0423.load_v042_trace_events(str(home)) if event.get("run_id") == run_id]
    view = v0423.build_v042_run_process_instance_view(str(home), "default-personal", run_id, events)
    assert view.process_instance_reconstructable is True
    assert view.lifecycle_status == "completed"
    assert view.provider_call_event_count == 2
    assert view.provider_call_transaction_count == 1
    assert view.safety_summary.safe_for_v0423_review is True


def test_v0423_run_show_last_returns_process_instance_without_provider_call(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0423.create_v042_run_show_result(v0423.create_v042_run_show_request(home_path=str(home), target="last"))
    assert result.found is True
    assert result.process_instance_view is not None
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.mutated_filesystem is False
    assert "Run Process Instance" in result.rendered_text


def test_v0423_run_show_by_id_returns_selected_run_without_provider_call(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    run_id = _latest_run_id(home)
    result = v0423.create_v042_run_show_result(
        v0423.create_v042_run_show_request(home_path=str(home), target="run_id", run_id=run_id)
    )
    assert result.found is True
    assert result.process_instance_view is not None
    assert result.process_instance_view.run_id == run_id
    assert result.provider_invoked is False
    assert result.mutated_filesystem is False


def test_v0423_session_show_last_returns_session_runs_and_turn_previews_without_provider_call(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0423.create_v042_session_show_result(v0423.create_v042_session_show_request(home_path=str(home), target="last"))
    assert result.found is True
    assert result.session_id
    assert result.run_links
    assert result.turn_previews
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.mutated_filesystem is False
    assert "Session" in result.rendered_text


def test_v0423_session_turn_preview_marks_provider_generated_text_untrusted() -> None:
    preview = v0423.build_v042_session_turn_preview(
        {"turn_id": "turn-1", "role": "assistant", "content": "hello", "provider_generated": True}
    )
    assert preview.provider_generated is True
    assert preview.trusted_for_memory is False
    assert preview.trusted_for_execution is False


def test_v0423_denial_evidence_view_proves_non_execution_from_denial_events() -> None:
    view = v0423.create_v042_denial_evidence_view(
        [
            {
                "event_kind": "unsafe_command_denied",
                "command_name": "safety check-command",
                "message": "Denied Remove-Item",
                "metadata": {"command": "Remove-Item -Recurse -Force C:\\", "matched_patterns": ["Remove-Item"]},
                "shell_executed": False,
            }
        ]
    )
    assert view.denial_count == 1
    assert view.denied_commands == ("Remove-Item -Recurse -Force C:\\",)
    assert view.matched_patterns == ("Remove-Item",)
    assert view.proves_non_execution is True


def test_v0423_safety_count_summary_marks_review_safe_when_shell_subagent_production_zero() -> None:
    summary = v0423.create_v042_safety_count_summary(
        [
            {"event_kind": "unsafe_command_denied", "shell_executed": False},
            {"event_kind": "run_completed", "shell_executed": False, "subagent_invoked": False, "production_certified": False},
        ]
    )
    assert summary.unsafe_denial_count == 1
    assert summary.shell_execution_count == 0
    assert summary.subagent_invocation_count == 0
    assert summary.production_certification_count == 0
    assert summary.safe_for_v0423_review is True


def test_v0423_debug_handoff_text_contains_run_session_safety_context_and_no_secrets() -> None:
    summary = v0423.create_v042_safety_count_summary([])
    handoff = v0423.create_v042_debug_handoff_text(
        profile_id="default-personal",
        home_path="C:/tmp/chanta",
        run_id="run-1",
        session_id="session-1",
        provider_mode="mock",
        safety_summary=summary,
        provider_call_event_count=2,
        provider_call_transaction_count=1,
    )
    assert "run_id: run-1" in handoff.concise_text
    assert "session_id: session-1" in handoff.concise_text
    assert "provider_call_transaction_count: 1" in handoff.concise_text
    assert handoff.includes_secret_values is False
    assert handoff.suitable_for_gpt_or_codex is True


def test_v0423_human_readable_render_policy_keeps_json_available_and_mutate_on_read_false() -> None:
    policy = v0423.create_v042_human_readable_render_policy()
    assert policy.default_format == "text"
    assert policy.json_still_available is True
    assert policy.redact_secrets is True
    assert policy.include_process_relevance is True
    assert policy.include_safety_counts is True
    assert policy.mutate_on_read is False


def test_v0423_trace_history_safety_report_says_trace_commands_do_not_call_provider_or_mutate_files() -> None:
    report = v0423.create_v042_trace_history_safety_report()
    assert report.trace_commands_call_provider is False
    assert report.trace_commands_submit_prompt is False
    assert report.trace_commands_mutate_filesystem is False
    assert report.trace_commands_execute_shell is False
    assert report.trace_commands_invoke_subagent is False
    assert report.trace_commands_certify_production is False
    assert report.raw_secrets_redacted is True
    assert report.provider_text_remains_untrusted is True


def test_v0423_readiness_report_sets_trace_history_flags_true() -> None:
    report = v0423.create_v0423_readiness_report()
    assert report.trace_timeline_command_ready is True
    assert report.run_history_command_ready is True
    assert report.run_show_last_command_ready is True
    assert report.run_show_by_id_command_ready is True
    assert report.session_show_last_command_ready is True
    assert report.session_show_by_id_command_ready is True
    assert report.provider_call_count_semantics_ready is True
    assert report.process_instance_view_ready is True
    assert report.denial_evidence_view_ready is True
    assert report.safety_count_summary_ready is True
    assert report.debug_handoff_text_ready is True
    assert report.integrated_restore_document_ready is True
    assert report.v0424_handoff_ready is True


def test_v0423_readiness_report_keeps_chat_skill_agentloop_shell_subagent_and_production_flags_false() -> None:
    report = v0423.create_v0423_readiness_report()
    assert report.ready_for_interactive_chat_shell is False
    assert report.ready_for_read_only_skill_execution_as_actions is False
    assert report.ready_for_provider_doctor_completion is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.production_certified is False


def test_v0423_v0424_handoff_targets_interactive_manual_chat_shell() -> None:
    handoff = v0423.create_v0424_interactive_manual_chat_shell_handoff()
    assert "Interactive Manual Chat Shell" in handoff.target_version
    assert "shell_execution" in handoff.must_not_open
    assert "subagent_invocation" in handoff.must_not_open
    assert "autonomous_continuation" in handoff.must_not_open
    assert handoff.production_certified is False


def test_v0423_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0423.create_v0423_integrated_restore_context_snapshot()
    assert snapshot.current_version == "v0.42.3 Human-readable Trace / Run History"
    assert "trace_timeline_command" in snapshot.open_capabilities
    assert "run_process_instance_view" in snapshot.open_capabilities
    assert "interactive_chat_shell" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0423_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0423.create_v0423_integrated_restore_packet()
    assert packet.single_integrated_doc_path == "docs/versions/v0.42/v0.42.3_human_readable_trace_run_history_restore.md"


def test_v0423_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0423.create_v0423_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0423_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0423.create_v0423_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0423_integrated_document_exists_and_has_required_restore_sections() -> None:
    path = Path("docs/versions/v0.42/v0.42.3_human_readable_trace_run_history_restore.md")
    text = path.read_text(encoding="utf-8")
    required_sections = [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Project Context for New Codex Session",
        "v0.41.6 User Test Baseline",
        "v0.42.0 UX Baseline Summary",
        "v0.42.1 Home / Quickstart Summary",
        "v0.42.2 Provider Setup Summary",
        "Human-readable Trace Summary",
        "Trace Timeline Contract",
        "Run History Contract",
        "Run Show Contract",
        "Session Show Contract",
        "Provider Call Count Semantics",
        "Process Instance View Contract",
        "Denial Evidence Contract",
        "Safety Count Summary Contract",
        "Debug Handoff Text Contract",
        "Trace History Safety Boundary",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Expected Test Interpretation",
        "Withdrawal Conditions",
        "v0.42.4 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]
    for section in required_sections:
        assert f"## {section}" in text


def test_v0423_integrated_document_contains_trace_timeline_run_history_examples_and_copy_paste_restore_prompt() -> None:
    path = Path("docs/versions/v0.42/v0.42.3_human_readable_trace_run_history_restore.md")
    text = path.read_text(encoding="utf-8")
    assert "chanta-cli trace timeline" in text
    assert "chanta-cli run history" in text
    assert "chanta-cli run show last" in text
    assert "chanta-cli session show last" in text
    assert "You are continuing ChantaCore after v0.42.3." in text


def test_v0423_no_separate_v0423_restore_trace_or_run_history_documents_created() -> None:
    forbidden = [
        Path("docs/versions/v0.42/v0.42.3_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.3_human_readable_trace.md"),
        Path("docs/versions/v0.42/v0.42.3_run_history.md"),
        Path("docs/versions/v0.42/v0.42.3_trace_timeline_contract.md"),
    ]
    assert all(not path.exists() for path in forbidden)


def test_v0423_no_forbidden_runtime_call_patterns_except_reading_bounded_trace_and_session_files() -> None:
    files = [
        Path("src/chanta_core/personal_runtime/default_personal_trace_history.py"),
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


def test_v0423_cli_quickstart_with_mock_run_then_trace_timeline_outputs_human_text(tmp_path: Path, capsys) -> None:
    home = tmp_path / "cli-home"
    assert cli_main(["quickstart", "--home", str(home), "--with-mock-run"]) == 0
    assert cli_main(["trace", "timeline", "--home", str(home)]) == 0
    output = capsys.readouterr().out
    assert "Trace Timeline" in output
    assert "provider_call_event_count" in output


def test_v0423_cli_quickstart_with_mock_run_then_run_history_outputs_one_run(tmp_path: Path, capsys) -> None:
    home = tmp_path / "cli-home"
    assert cli_main(["quickstart", "--home", str(home), "--with-mock-run"]) == 0
    assert cli_main(["run", "history", "--home", str(home)]) == 0
    output = capsys.readouterr().out
    assert "Run History" in output
    assert "mock=true" in output


def test_v0423_cli_run_show_last_outputs_process_instance_steps(tmp_path: Path, capsys) -> None:
    home = tmp_path / "cli-home"
    assert cli_main(["quickstart", "--home", str(home), "--with-mock-run"]) == 0
    assert cli_main(["run", "show", "last", "--home", str(home)]) == 0
    output = capsys.readouterr().out
    assert "Run Process Instance" in output
    assert "provider_text_call_completed" in output


def test_v0423_cli_session_show_last_outputs_turn_preview(tmp_path: Path, capsys) -> None:
    home = tmp_path / "cli-home"
    assert cli_main(["quickstart", "--home", str(home), "--with-mock-run"]) == 0
    assert cli_main(["session", "show", "last", "--home", str(home)]) == 0
    output = capsys.readouterr().out
    assert "Session" in output
    assert "assistant" in output


def test_v0423_cli_safety_denial_then_trace_timeline_shows_denial(tmp_path: Path, capsys) -> None:
    home = tmp_path / "cli-home"
    assert cli_main(["quickstart", "--home", str(home), "--with-mock-run"]) == 0
    assert cli_main(["safety", "check-command", "--home", str(home), "--command", "Remove-Item -Recurse -Force C:\\"]) == 1
    assert cli_main(["trace", "timeline", "--home", str(home), "--limit", "20"]) == 0
    output = capsys.readouterr().out
    assert "denial" in output.lower()
    assert "Remove-Item" in output


def test_v0423_cli_run_show_does_not_emit_recursive_trace_event(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    before = len(v0423.load_v042_trace_events(str(home)))
    run_id = _latest_run_id(home)
    assert cli_main(["run", "show", "--home", str(home), "--run-id", run_id]) == 0
    after = len(v0423.load_v042_trace_events(str(home)))
    assert after == before
