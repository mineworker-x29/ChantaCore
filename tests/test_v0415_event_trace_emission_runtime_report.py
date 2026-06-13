from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path

import pytest

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_trace_report as v0415


def _values(enum_cls: type) -> set[str]:
    return {item.value for item in enum_cls}


def test_v0415_runtime_event_kinds_declared() -> None:
    assert {
        "runtime_started",
        "cli_command_received",
        "cli_command_completed",
        "doctor_check_started",
        "doctor_check_completed",
        "profile_init_requested",
        "profile_initialized",
        "profile_loaded",
        "profile_status_viewed",
        "prompt_preview_requested",
        "prompt_preview_rendered",
        "session_created",
        "session_list_viewed",
        "provider_doctor_started",
        "provider_doctor_completed",
        "provider_models_probe_started",
        "provider_models_probe_completed",
        "skill_registry_loaded",
        "skill_list_viewed",
        "skill_inspect_viewed",
        "skill_gate_checked",
        "skill_invocation_denied",
        "run_started",
        "prompt_assembled",
        "user_input_received",
        "provider_text_call_started",
        "provider_text_call_completed",
        "session_turns_appended",
        "assistant_response_recorded",
        "run_completed",
        "run_failed",
        "unsafe_command_checked",
        "unsafe_command_denied",
        "trace_recent_viewed",
        "trace_summary_generated",
        "run_report_generated",
        "unsupported_command_denied",
        "runtime_error_recorded",
    } <= _values(v0415.RuntimeEventKind)


def test_v0415_runtime_event_status_values_declared() -> None:
    assert {"started", "completed", "failed", "skipped", "denied", "blocked", "warning", "info"} <= _values(
        v0415.RuntimeEventStatus
    )


def test_v0415_runtime_object_kinds_declared() -> None:
    assert {
        "profile",
        "session",
        "run",
        "prompt_bundle",
        "provider_config",
        "provider_request",
        "provider_response",
        "skill",
        "command",
        "trace_store",
        "denial",
        "safety_gate",
        "restore_context",
        "runtime_report",
        "ocel_projection_candidate",
    } <= _values(v0415.RuntimeObjectKind)


def test_v0415_runtime_object_ref_redacts_secrets() -> None:
    ref = v0415.create_runtime_object_ref(
        "provider",
        "provider_config",
        metadata={"api_key": "secret-value", "normal": "visible"},
    )
    assert ref.metadata["api_key"] == "<redacted>"
    assert "secret-value" not in str(asdict(ref))


def test_v0415_runtime_event_keeps_shell_workspace_subagent_production_false() -> None:
    event = v0415.create_runtime_event("trace_recent_viewed", "completed")
    assert event.shell_executed is False
    assert event.workspace_mutated is False
    assert event.subagent_invoked is False
    assert event.production_certified is False
    assert event.skill_executed is False


def test_v0415_runtime_event_allows_provider_invoked_only_for_run_provider_events() -> None:
    provider_event = v0415.create_runtime_event("provider_text_call_started", "started")
    other_event = v0415.create_runtime_event("trace_summary_generated", "completed")
    assert provider_event.provider_invoked is True
    assert provider_event.prompt_submitted is True
    assert other_event.provider_invoked is False
    assert other_event.prompt_submitted is False


def test_v0415_event_envelope_is_append_only_and_redacted() -> None:
    envelope = v0415.create_runtime_event_envelope(
        v0415.create_runtime_event("runtime_started", "started")
    )
    assert envelope.append_only is True
    assert envelope.redacted is True
    assert envelope.source_version == "v0.41.5"


def test_v0415_trace_store_config_is_bounded_to_home_and_append_only(tmp_path: Path) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    assert config.append_only is True
    assert config.overwrite_allowed is False
    assert config.bounded_to_home is True
    assert Path(config.events_jsonl_path).is_relative_to(tmp_path.resolve())


def test_v0415_trace_append_policy_disallows_overwrite_and_outside_home() -> None:
    policy = v0415.create_trace_append_policy()
    assert policy.append_allowed is True
    assert policy.overwrite_allowed is False
    assert policy.write_outside_home_allowed is False
    assert policy.recursive_trace_view_events_allowed is False
    assert policy.redact_secrets is True


def test_v0415_append_runtime_event_writes_jsonl_under_tmp_home(tmp_path: Path) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    event = v0415.create_runtime_event("runtime_started", "started")
    result = v0415.append_runtime_event(event, config)
    assert result.success is True
    assert result.event_count == 1
    assert Path(config.events_jsonl_path).exists()
    assert Path(config.events_jsonl_path).read_text(encoding="utf-8").count("\n") == 1


def test_v0415_append_runtime_event_does_not_overwrite_existing_trace(tmp_path: Path) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    v0415.append_runtime_event(v0415.create_runtime_event("runtime_started", "started"), config)
    v0415.append_runtime_event(v0415.create_runtime_event("cli_command_completed", "completed"), config)
    assert Path(config.events_jsonl_path).read_text(encoding="utf-8").count("\n") == 2


def test_v0415_trace_recent_reads_bounded_events_without_provider_prompt_skill_shell_or_subagent(
    tmp_path: Path,
) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    for index in range(5):
        v0415.append_runtime_event(
            v0415.create_runtime_event("cli_command_completed", "completed", metadata={"index": index}),
            config,
        )
    result = v0415.read_trace_recent(
        v0415.create_trace_recent_request("default-personal", str(tmp_path), limit=2)
    )
    assert result.event_count == 2
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.skill_executed is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False


def test_v0415_trace_summary_counts_event_status_command_denial_provider_and_unsafe_counts(
    tmp_path: Path,
) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    events = (
        v0415.create_runtime_event("run_started", "started", run_id="run-1", command_name="run"),
        v0415.create_runtime_event("provider_text_call_completed", "completed", run_id="run-1", command_name="run"),
        v0415.create_runtime_event("unsafe_command_denied", "denied", command_name="safety check-command"),
    )
    v0415.append_runtime_events(events, config)
    result = v0415.summarize_trace_events(
        v0415.create_trace_summary_request("default-personal", str(tmp_path))
    )
    assert result.total_events == 3
    assert result.by_event_kind["provider_text_call_completed"] == 1
    assert result.by_status["denied"] == 1
    assert result.by_command_name["run"] == 2
    assert result.run_count == 1
    assert result.denial_count == 1
    assert result.provider_call_count == 1


def test_v0415_trace_summary_keeps_skill_shell_subagent_production_counts_zero(tmp_path: Path) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    v0415.append_runtime_event(v0415.create_runtime_event("trace_summary_generated", "completed"), config)
    result = v0415.summarize_trace_events(
        v0415.create_trace_summary_request("default-personal", str(tmp_path))
    )
    assert result.skill_execution_count == 0
    assert result.shell_execution_count == 0
    assert result.subagent_invocation_count == 0
    assert result.production_certification_count == 0


def test_v0415_last_run_report_finds_latest_run_after_mock_run(tmp_path: Path) -> None:
    exit_code = cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "Summarize status.",
        ]
    )
    assert exit_code == 0
    report = v0415.create_last_run_report(
        v0415.create_last_run_report_request("default-personal", str(tmp_path))
    )
    assert report.found is True
    assert report.run_id is not None
    assert report.session_id is not None
    assert report.provider_invoked is True
    assert report.prompt_submitted is True
    assert "Mock provider response" in (report.assistant_response_preview or "")


def test_v0415_last_run_report_keeps_skill_shell_subagent_production_false(tmp_path: Path) -> None:
    cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "Summarize status.",
        ]
    )
    report = v0415.create_last_run_report(
        v0415.create_last_run_report_request("default-personal", str(tmp_path))
    )
    assert report.skill_executed is False
    assert report.shell_executed is False
    assert report.subagent_invoked is False
    assert report.production_certified is False


def test_v0415_command_trace_envelope_wraps_command_start_and_complete_events() -> None:
    started = v0415.create_runtime_event("cli_command_received", "started", command_name="doctor")
    completed = v0415.create_runtime_event("cli_command_completed", "completed", command_name="doctor")
    append_result = v0415.create_trace_append_result(2, appended_paths=("events.jsonl",))
    envelope = v0415.create_runtime_command_trace_envelope(
        "doctor",
        started_event=started,
        completed_event=completed,
        trace_append_result=append_result,
    )
    result = v0415.create_runtime_command_trace_result("doctor", (started, completed), append_result, True)
    assert envelope.started_event == started
    assert envelope.completed_event == completed
    assert result.event_kinds_emitted == ("cli_command_received", "cli_command_completed")
    assert result.trace_written is True


def test_v0415_denial_kind_values_declared() -> None:
    assert {
        "unsupported_command",
        "unsafe_command",
        "unsafe_skill",
        "unsafe_runtime_escalation",
        "shell_execution",
        "file_write",
        "file_edit",
        "patch_apply",
        "test_execution",
        "provider_tool_call",
        "function_call",
        "subagent_invocation",
        "child_session_creation",
        "credential_access",
        "dominion_runtime",
        "production_certification",
    } <= _values(v0415.DenialKind)


def test_v0415_denial_event_record_is_blocked_and_not_executed() -> None:
    record = v0415.create_denial_event_record("unsafe_command", "safety check-command", "Remove-Item x")
    assert record.blocked is True
    assert record.executed is False


def test_v0415_safety_check_command_never_executes_command_text(tmp_path: Path) -> None:
    command_input = v0415.create_safety_check_command_input(
        "default-personal", str(tmp_path), "Remove-Item -Recurse -Force C:\\"
    )
    decision = v0415.check_unsafe_command(command_input)
    assert decision.executed is False
    assert decision.blocked is True


def test_v0415_safety_check_command_denies_remove_recurse_force(tmp_path: Path) -> None:
    result_code = cli_main(
        [
            "safety",
            "check-command",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--command",
            "Remove-Item -Recurse -Force C:\\",
        ]
    )
    assert result_code == 1
    summary = v0415.summarize_trace_events(
        v0415.create_trace_summary_request("default-personal", str(tmp_path))
    )
    assert summary.denial_count == 1
    assert summary.by_event_kind["unsafe_command_denied"] == 1


def test_v0415_safety_check_command_appends_denial_event(tmp_path: Path) -> None:
    cli_main(
        [
            "safety",
            "check-command",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--command",
            "production-certify",
        ]
    )
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    assert Path(config.denials_jsonl_path).exists()
    assert "unsafe_command_denied" in Path(config.denials_jsonl_path).read_text(encoding="utf-8")


def test_v0415_unsafe_command_patterns_declared() -> None:
    names = {pattern.pattern_name for pattern in v0415.build_unsafe_command_patterns()}
    assert {
        "remove_recursive_force",
        "shell_execution",
        "file_write",
        "file_edit",
        "patch_apply",
        "test_execution",
        "credential_access",
        "network_unbounded",
        "subagent_invoke",
        "dominion_runtime",
        "production_certify",
    } <= names


def test_v0415_trace_validation_detects_invalid_or_unsafe_events(tmp_path: Path) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    unsafe_event = v0415.create_runtime_event(
        "runtime_error_recorded",
        "failed",
        shell_executed=True,
    )
    v0415.append_runtime_event(unsafe_event, config)
    report = v0415.validate_trace_store("default-personal", str(tmp_path))
    assert report.valid is False
    assert report.unsafe_runtime_event_detected is True
    assert report.production_certification_detected is False


def test_v0415_ocel_projection_candidate_is_metadata_only_and_export_not_performed() -> None:
    event = v0415.create_runtime_event("run_completed", "completed", run_id="run-1", session_id="session-1")
    candidate = v0415.create_ocel_projection_candidate("default-personal", (event,))
    assert candidate.export_performed is False
    assert candidate.suitable_for_future_ocel_export is True
    assert {ref.object_type for ref in candidate.object_refs} >= {"profile", "session", "run"}


def test_v0415_readiness_report_sets_trace_and_report_ready_but_keeps_user_release_and_unsafe_flags_false() -> None:
    report = v0415.create_v0415_readiness_report()
    assert report.runtime_event_model_ready is True
    assert report.trace_recent_command_ready is True
    assert report.trace_summary_command_ready is True
    assert report.run_report_last_command_ready is True
    assert report.safety_check_command_ready is True
    assert report.ready_for_final_user_test_release is False
    assert report.ready_for_provider_doctor_completion is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_read_only_skill_execution is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.production_certified is False


def test_v0415_v0416_handoff_targets_installable_user_test_release() -> None:
    handoff = v0415.create_v0416_installable_user_test_release_handoff()
    assert handoff.target_version == "v0.41.6"
    assert "Installable Default Personal User Test Release" in handoff.title


def test_v0415_v0416_user_test_target_preserves_required_commands() -> None:
    target = v0415.create_v0416_user_test_target_update()
    assert "chanta-cli trace recent --profile default-personal --limit 10" in target.required_commands
    assert any("safety check-command" in command for command in target.required_commands)
    assert target.certification_claimed_in_v0415 is False


def test_v0415_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0415.create_v0415_integrated_restore_context_snapshot()
    assert "trace_recent_command" in snapshot.open_capabilities
    assert "run_report_last_command" in snapshot.open_capabilities
    assert "final_user_test_release_certification" in snapshot.closed_capabilities
    assert "provider_doctor_completion" in snapshot.closed_capabilities


def test_v0415_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0415.create_v0415_integrated_restore_packet()
    assert packet.single_integrated_doc_path == v0415.INTEGRATED_DOC_PATH


def test_v0415_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0415.create_v0415_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0415_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0415.create_v0415_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0415_integrated_document_exists_and_has_required_restore_sections() -> None:
    doc = Path(v0415.INTEGRATED_DOC_PATH)
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for section in v0415.REQUIRED_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0415_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(v0415.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "You are continuing ChantaCore after v0.41.5." in text
    assert "Next recommended version:" in text
    assert "v0.41.6 Installable Default Personal User Test Release" in text


def test_v0415_no_separate_v0415_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.5_restore_document.md").exists()


def test_v0415_no_separate_v0415_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.5_event_trace_emission.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.5_runtime_report.md").exists()


def test_v0415_unsupported_apply_shell_subagent_dominion_commands_do_not_execute(tmp_path: Path) -> None:
    for command in ("apply", "shell", "invoke-subagent", "dominion", "production-certify"):
        exit_code = cli_main([command, "--profile", "default-personal", "--home", str(tmp_path)])
        assert exit_code == 1
    summary = v0415.summarize_trace_events(
        v0415.create_trace_summary_request("default-personal", str(tmp_path))
    )
    assert summary.denial_count == 5
    assert summary.shell_execution_count == 0
    assert summary.subagent_invocation_count == 0
    assert summary.production_certification_count == 0


def test_v0415_no_forbidden_runtime_call_patterns_except_bounded_trace_store_and_existing_provider_run() -> None:
    scan_paths = [
        Path("src/chanta_core/personal_runtime/default_personal_trace_report.py"),
        Path("src/chanta_core/personal_runtime/default_personal_run.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    source_by_path = {path: path.read_text(encoding="utf-8").lower() for path in scan_paths}
    forbidden = (
        "subprocess",
        "shell=true",
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
        "unittest",
    )
    for path, source in source_by_path.items():
        for token in forbidden:
            assert token not in source, f"{token} found in {path}"
    assert "openai" not in source_by_path[Path("src/chanta_core/personal_runtime/default_personal_trace_report.py")]


def test_v0415_main_mock_run_then_trace_recent_shows_run_events(tmp_path: Path) -> None:
    cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "Summarize status.",
        ]
    )
    result = v0415.read_trace_recent(
        v0415.create_trace_recent_request("default-personal", str(tmp_path), limit=10)
    )
    kinds = [event.event_kind for event in result.events]
    assert "run_started" in kinds
    assert "run_completed" in kinds


def test_v0415_main_mock_run_then_trace_summary_counts_run_completed(tmp_path: Path) -> None:
    cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "Summarize status.",
        ]
    )
    result = v0415.summarize_trace_events(
        v0415.create_trace_summary_request("default-personal", str(tmp_path))
    )
    assert result.by_event_kind["run_completed"] == 1


def test_v0415_main_mock_run_then_run_report_last_summarizes_response(tmp_path: Path) -> None:
    cli_main(
        [
            "run",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--provider",
            "mock",
            "Summarize status.",
        ]
    )
    report = v0415.create_last_run_report(
        v0415.create_last_run_report_request("default-personal", str(tmp_path))
    )
    assert report.found is True
    assert "Mock provider response" in (report.assistant_response_preview or "")


def test_v0415_main_safety_check_command_denies_dangerous_command_and_trace_recent_shows_denial(
    tmp_path: Path,
) -> None:
    cli_main(
        [
            "safety",
            "check-command",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--command",
            "Remove-Item -Recurse -Force C:\\",
        ]
    )
    result = v0415.read_trace_recent(
        v0415.create_trace_recent_request("default-personal", str(tmp_path), limit=5)
    )
    assert result.events[-1].event_kind == "unsafe_command_denied"
    assert result.events[-1].shell_executed is False


def test_v0415_trace_recent_does_not_create_recursive_trace_noise_by_default(tmp_path: Path) -> None:
    config = v0415.create_trace_store_config("default-personal", str(tmp_path))
    v0415.append_runtime_event(v0415.create_runtime_event("runtime_started", "started"), config)
    before = Path(config.events_jsonl_path).read_text(encoding="utf-8").count("\n")
    cli_main(
        [
            "trace",
            "recent",
            "--profile",
            "default-personal",
            "--home",
            str(tmp_path),
            "--limit",
            "10",
        ]
    )
    after = Path(config.events_jsonl_path).read_text(encoding="utf-8").count("\n")
    assert after == before
