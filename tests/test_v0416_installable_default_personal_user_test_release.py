from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_user_test_release as v0416
from chanta_core.personal_runtime.default_personal_trace_report import (
    create_last_run_report,
    create_last_run_report_request,
    create_trace_recent_request,
    create_trace_summary_request,
    read_trace_recent,
    summarize_trace_events,
)


def _values(enum_cls: type) -> set[str]:
    return {item.value for item in enum_cls}


def test_v0416_release_mode_values_declared() -> None:
    assert {
        "deterministic_mock_acceptance",
        "configured_provider_acceptance",
        "documentation_only",
        "unsupported",
    } <= _values(v0416.V0416ReleaseMode)


def test_v0416_user_test_command_kinds_declared() -> None:
    assert {
        "pip_editable_install",
        "cli_version",
        "cli_doctor",
        "init_default_personal",
        "profile_status",
        "provider_doctor_no_completion",
        "run_mock_provider",
        "run_configured_provider",
        "trace_recent",
        "trace_summary",
        "run_report_last",
        "safety_check_command",
        "unsupported_command_denial",
        "release_status",
        "unknown",
    } <= _values(v0416.V0416UserTestCommandKind)


def test_v0416_user_test_command_status_values_declared() -> None:
    assert {
        "pass",
        "pass_with_notes",
        "fail",
        "skipped",
        "not_applicable",
        "manual_only",
        "future_gated",
        "denied",
    } <= _values(v0416.V0416UserTestCommandStatus)


def test_v0416_install_check_requires_chanta_cli_and_editable_install_command_but_does_not_run_pip() -> None:
    check = v0416.create_v0416_install_check()
    assert check.cli_name == "chanta-cli"
    assert check.expected_console_script == "chanta-cli"
    assert check.editable_install_command == "py -m pip install -e ."
    assert check.manual_install_required is True
    assert "does not run pip" in check.message


def test_v0416_cli_entrypoint_check_covers_version_doctor_run_trace_and_safety_commands() -> None:
    check = v0416.create_v0416_cli_entrypoint_check()
    assert check.entrypoint_ready is True
    assert check.version_command_expected == "chanta-cli --version"
    assert check.doctor_command_expected == "chanta-cli doctor"
    assert "run" in check.run_command_expected
    assert "trace recent" in check.trace_recent_command_expected
    assert "safety check-command" in check.safety_check_command_expected


def test_v0416_command_acceptance_criterion_lists_required_mock_flow_commands() -> None:
    matrix = v0416.create_v0416_command_acceptance_matrix()
    required = {criterion.command_kind for criterion in matrix.criteria if criterion.required_for_mock_flow}
    assert {
        "pip_editable_install",
        "cli_version",
        "cli_doctor",
        "init_default_personal",
        "profile_status",
        "provider_doctor_no_completion",
        "run_mock_provider",
        "trace_recent",
        "trace_summary",
        "run_report_last",
        "safety_check_command",
        "unsupported_command_denial",
    } <= required


def test_v0416_command_acceptance_result_keeps_shell_subagent_and_production_false() -> None:
    criterion = v0416.create_v0416_command_acceptance_criterion("cli_version", "chanta-cli --version")
    result = v0416.create_v0416_command_acceptance_result(criterion)
    assert result.shell_executed is False
    assert result.workspace_mutated_outside_allowed_store is False
    assert result.subagent_invoked is False
    assert result.production_certified is False


def test_v0416_command_acceptance_matrix_requires_mock_flow_and_unsafe_denial() -> None:
    matrix = v0416.create_v0416_command_acceptance_matrix()
    assert matrix.required_mock_flow_passed is True
    assert matrix.configured_provider_flow_supported is True
    assert matrix.unsafe_command_denial_passed is True
    assert matrix.all_required_commands_present is True


def test_v0416_user_test_flow_defines_deterministic_mock_flow_as_required_and_ci_safe() -> None:
    flow = v0416.create_v0416_user_test_flow("deterministic_mock")
    assert flow.required_for_release is True
    assert flow.safe_for_ci is True
    assert flow.requires_external_provider is False
    kinds = {step.command_kind for step in flow.steps}
    assert {"init_default_personal", "profile_status", "provider_doctor_no_completion", "run_mock_provider", "trace_recent", "trace_summary", "run_report_last", "safety_check_command"} <= kinds


def test_v0416_user_test_flow_defines_configured_provider_flow_as_supported_but_not_ci_required() -> None:
    flow = v0416.create_v0416_user_test_flow("configured_provider")
    assert flow.required_for_release is False
    assert flow.safe_for_ci is False
    assert flow.requires_external_provider is True
    assert any(step.command_kind == "run_configured_provider" for step in flow.steps)


def test_v0416_mock_provider_acceptance_requires_no_network_session_trace_and_run_report() -> None:
    acceptance = v0416.create_v0416_mock_provider_acceptance()
    assert acceptance.mock_provider_required is True
    assert acceptance.no_network_required is True
    assert acceptance.session_append_required is True
    assert acceptance.trace_required is True
    assert acceptance.run_report_required is True
    assert acceptance.mock_run_expected_response_prefix == "Mock provider response:"


def test_v0416_configured_provider_acceptance_allows_completion_only_in_run() -> None:
    acceptance = v0416.create_v0416_configured_provider_acceptance()
    assert acceptance.configured_provider_supported is True
    assert acceptance.configured_provider_required_for_ci is False
    assert acceptance.provider_doctor_no_completion_required is True
    assert acceptance.completion_allowed_only_in_run is True
    assert acceptance.tool_calling_allowed is False
    assert acceptance.function_calling_allowed is False
    assert acceptance.secret_redaction_required is True


def test_v0416_provider_acceptance_policy_keeps_doctor_completion_tools_and_functions_closed() -> None:
    policy = v0416.create_v0416_provider_acceptance_policy()
    assert policy.provider_doctor_completion_allowed is False
    assert policy.unscoped_prompt_submission_allowed is False
    assert policy.provider_tool_calling_allowed is False
    assert policy.function_calling_allowed is False
    assert policy.remote_provider_allowed_only_for_run is True


def test_v0416_trace_acceptance_requires_run_provider_session_and_denial_events() -> None:
    acceptance = v0416.create_v0416_trace_acceptance()
    assert acceptance.trace_recent_required is True
    assert acceptance.trace_summary_required is True
    assert acceptance.trace_contains_run_event_required is True
    assert acceptance.trace_contains_provider_text_call_event_required is True
    assert acceptance.trace_contains_session_turn_append_event_required is True
    assert acceptance.trace_contains_denial_event_required is True
    assert acceptance.trace_is_append_only is True


def test_v0416_run_report_acceptance_requires_last_mock_run_without_provider_call() -> None:
    acceptance = v0416.create_v0416_run_report_acceptance()
    assert acceptance.run_report_last_required is True
    assert acceptance.must_find_last_mock_run is True
    assert acceptance.must_include_session_id is True
    assert acceptance.must_include_assistant_response_preview is True
    assert acceptance.must_not_call_provider is True


def test_v0416_denial_acceptance_blocks_remove_item_recurse_force_and_never_executes() -> None:
    acceptance = v0416.create_v0416_denial_acceptance()
    assert "Remove-Item -Recurse -Force C:\\" in acceptance.dangerous_command_example
    assert acceptance.must_block is True
    assert acceptance.must_not_execute is True
    assert acceptance.denial_trace_required is True


def test_v0416_safety_boundary_report_keeps_all_high_risk_capabilities_closed() -> None:
    report = v0416.create_v0416_safety_boundary_report()
    for name, value in report.__dict__.items():
        if name.endswith("_closed"):
            assert value is True
    assert report.production_certified is False


def test_v0416_closed_capability_matrix_contains_required_closed_capabilities() -> None:
    matrix = v0416.create_v0416_closed_capability_matrix()
    names = {capability.name for capability in matrix.capabilities}
    assert set(v0416.REQUIRED_CLOSED_CAPABILITIES) <= names
    assert matrix.all_required_closed is True
    assert matrix.production_certified is False


def test_v0416_release_readiness_report_can_be_true_only_when_mock_trace_report_denial_and_closed_matrix_pass() -> None:
    report = v0416.create_v0416_release_readiness_report()
    assert report.ready_for_final_user_test_release is True
    failed = v0416.create_v0416_release_readiness_report(
        trace_acceptance=v0416.create_v0416_trace_acceptance(passed=False)
    )
    assert failed.ready_for_final_user_test_release is False


def test_v0416_release_readiness_report_keeps_production_certified_false() -> None:
    report = v0416.create_v0416_release_readiness_report()
    assert report.production_certified is False
    assert report.next_recommended_version == "v0.42.0"


def test_v0416_known_limitations_include_no_tool_calling_no_shell_no_subagent_no_production_certification() -> None:
    titles = {item.title for item in v0416.create_v0416_release_readiness_report().known_limitations}
    assert {
        "no provider tool calling",
        "no shell/edit/apply",
        "no subagents",
        "no production certification",
        "real provider requires user configuration",
    } <= titles


def test_v0416_user_guide_sections_include_install_doctor_init_provider_run_trace_safety_troubleshooting() -> None:
    section_ids = {section.section_id for section in v0416.create_v0416_user_guide_sections()}
    assert {
        "install",
        "doctor",
        "init",
        "profile-status",
        "provider-doctor",
        "mock-provider-run",
        "configured-provider-run",
        "trace-recent",
        "trace-summary",
        "run-report-last",
        "safety-denial-test",
        "known-limitations",
        "troubleshooting",
        "what-v0416-is-not",
    } <= section_ids


def test_v0416_troubleshooting_items_include_chanta_cli_not_found_profile_missing_provider_not_configured_trace_empty() -> None:
    symptoms = {item.symptom for item in v0416.create_v0416_troubleshooting_items()}
    assert {
        "chanta-cli not found",
        "profile missing",
        "provider not configured",
        "run fails with provider unavailable",
        "trace recent empty",
        "safety check-command does not emit denial trace",
        "permission/path problem on Windows",
    } <= symptoms


def test_v0416_v042_handoff_targets_v0420_and_blocks_shell_edit_apply_subagent_dominion_without_new_gate() -> None:
    handoff = v0416.create_v0416_v042_handoff()
    assert handoff.next_version == "v0.42.0"
    assert any("provider configuration UX" in item for item in handoff.recommended_focus)
    assert "shell/edit/apply" in handoff.must_not_open_without_new_gate
    assert "subagents" in handoff.must_not_open_without_new_gate
    assert "Dominion runtime" in handoff.must_not_open_without_new_gate


def test_v0416_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0416.create_v0416_integrated_restore_context_snapshot()
    assert snapshot.current_version == "v0.41.6 Installable Default Personal User Test Release"
    assert "installable_chanta_cli_user_test_flow" in snapshot.open_capabilities
    assert "final_user_test_release_readiness" in snapshot.open_capabilities
    assert "production_certification" in snapshot.closed_capabilities
    assert "provider_doctor_completion" in snapshot.closed_capabilities


def test_v0416_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0416.create_v0416_integrated_restore_packet()
    assert packet.single_integrated_doc_path == v0416.INTEGRATED_DOC_PATH


def test_v0416_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0416.create_v0416_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0416_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0416.create_v0416_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0416_integrated_document_exists_and_has_required_restore_sections() -> None:
    doc = Path(v0416.INTEGRATED_DOC_PATH)
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for section in v0416.REQUIRED_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0416_integrated_document_contains_windows_user_guide_commands() -> None:
    text = Path(v0416.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "Set-Location D:\\ChantaResearchGroup\\ChantaCore" in text
    assert "py -m pip install -e ." in text
    assert "chanta-cli run --profile default-personal --provider mock" in text
    assert "chanta-cli safety check-command --profile default-personal" in text


def test_v0416_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(v0416.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "You are continuing ChantaCore after v0.41.6." in text
    assert "ChantaCore has completed the v0.41 Default Personal Runtime Opening Track." in text
    assert "Next recommended version:" in text
    assert "v0.42.0." in text


def test_v0416_no_separate_v0416_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.6_restore_document.md").exists()


def test_v0416_no_separate_v0416_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.6_installable_default_personal_user_test_release.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.6_user_test_guide.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.6_release_manifest.md").exists()


def test_v0416_full_mock_user_flow_with_cli_helpers_if_available(tmp_path: Path, capsys) -> None:
    assert cli_main(["--version"]) == 0
    assert cli_main(["doctor"]) == 0
    assert cli_main(["init", "default-personal", "--home", str(tmp_path)]) == 0
    assert cli_main(["profile", "status", "--profile", "default-personal", "--home", str(tmp_path)]) == 0
    assert cli_main(["provider", "doctor", "--profile", "default-personal", "--home", str(tmp_path), "--no-completion"]) == 0
    assert cli_main(["run", "--profile", "default-personal", "--home", str(tmp_path), "--provider", "mock", "Summarize what ChantaCore is in three bullets."]) == 0
    assert cli_main(["trace", "recent", "--profile", "default-personal", "--home", str(tmp_path), "--limit", "10"]) == 0
    assert cli_main(["trace", "summary", "--profile", "default-personal", "--home", str(tmp_path)]) == 0
    assert cli_main(["run-report", "last", "--profile", "default-personal", "--home", str(tmp_path)]) == 0
    assert cli_main(["safety", "check-command", "--profile", "default-personal", "--home", str(tmp_path), "--command", "Remove-Item -Recurse -Force C:\\"]) == 1
    output = capsys.readouterr().out
    assert "Mock provider response" in output
    assert "unsafe_command" in output


def test_v0416_mock_run_then_trace_recent_then_run_report_then_safety_denial_flow(tmp_path: Path) -> None:
    cli_main(["init", "default-personal", "--home", str(tmp_path)])
    cli_main(["run", "--profile", "default-personal", "--home", str(tmp_path), "--provider", "mock", "Summarize status."])
    cli_main(["safety", "check-command", "--profile", "default-personal", "--home", str(tmp_path), "--command", "Remove-Item -Recurse -Force C:\\"])
    recent = read_trace_recent(create_trace_recent_request("default-personal", str(tmp_path), 20))
    kinds = {event.event_kind for event in recent.events}
    assert "run_completed" in kinds
    assert "provider_text_call_completed" in kinds
    assert "session_turns_appended" in kinds
    assert "unsafe_command_denied" in kinds
    report = create_last_run_report(create_last_run_report_request("default-personal", str(tmp_path)))
    assert report.found is True
    assert report.provider_invoked is True
    summary = summarize_trace_events(create_trace_summary_request("default-personal", str(tmp_path)))
    assert summary.denial_count == 1


def test_v0416_unsupported_apply_shell_subagent_dominion_commands_do_not_execute(tmp_path: Path) -> None:
    for command in ("apply", "shell", "invoke-subagent", "dominion", "production-certify"):
        assert cli_main([command, "--profile", "default-personal", "--home", str(tmp_path)]) == 1
    summary = summarize_trace_events(create_trace_summary_request("default-personal", str(tmp_path)))
    assert summary.denial_count == 5
    assert summary.shell_execution_count == 0
    assert summary.subagent_invocation_count == 0
    assert summary.production_certification_count == 0


def test_v0416_no_forbidden_runtime_call_patterns_except_existing_scoped_provider_run_and_bounded_stores() -> None:
    paths = [
        Path("src/chanta_core/personal_runtime/default_personal_user_test_release.py"),
        Path("src/chanta_core/personal_runtime/default_personal_trace_report.py"),
        Path("src/chanta_core/personal_runtime/default_personal_run.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    sources = {path: path.read_text(encoding="utf-8").lower() for path in paths}
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
    for path, source in sources.items():
        for token in forbidden:
            assert token not in source, f"{token} found in {path}"
    assert "openai" not in sources[Path("src/chanta_core/personal_runtime/default_personal_user_test_release.py")]


def test_v0416_main_full_mock_flow_under_tmp_home(tmp_path: Path) -> None:
    assert cli_main(["init", "default-personal", "--home", str(tmp_path)]) == 0
    assert cli_main(["run", "--profile", "default-personal", "--home", str(tmp_path), "--provider", "mock", "Summarize."]) == 0
    assert cli_main(["run-report", "last", "--profile", "default-personal", "--home", str(tmp_path)]) == 0


def test_v0416_main_doctor_after_init_reports_profile_ready(tmp_path: Path, capsys) -> None:
    cli_main(["init", "default-personal", "--home", str(tmp_path)])
    assert cli_main(["profile", "status", "--profile", "default-personal", "--home", str(tmp_path)]) == 0
    assert "profile_exists" in capsys.readouterr().out


def test_v0416_main_provider_doctor_no_completion_before_run(tmp_path: Path, capsys) -> None:
    assert cli_main(["provider", "doctor", "--profile", "default-personal", "--home", str(tmp_path), "--no-completion"]) == 0
    output = capsys.readouterr().out
    assert '"provider_invoked_completion": false' in output
    assert '"prompt_submitted": false' in output


def test_v0416_main_trace_recent_after_mock_run_contains_run_completed(tmp_path: Path) -> None:
    cli_main(["run", "--profile", "default-personal", "--home", str(tmp_path), "--provider", "mock", "Summarize."])
    recent = read_trace_recent(create_trace_recent_request("default-personal", str(tmp_path), 10))
    assert any(event.event_kind == "run_completed" for event in recent.events)


def test_v0416_main_safety_check_command_after_mock_run_contains_denial_event(tmp_path: Path) -> None:
    cli_main(["run", "--profile", "default-personal", "--home", str(tmp_path), "--provider", "mock", "Summarize."])
    cli_main(["safety", "check-command", "--profile", "default-personal", "--home", str(tmp_path), "--command", "Remove-Item -Recurse -Force C:\\"])
    recent = read_trace_recent(create_trace_recent_request("default-personal", str(tmp_path), 20))
    assert any(event.event_kind == "unsafe_command_denied" for event in recent.events)


def test_v0416_configured_provider_flow_is_skipped_without_provider_config() -> None:
    flow = v0416.create_v0416_user_test_flow("configured_provider")
    assert flow.required_for_release is False
    assert flow.requires_external_provider is True
    assert all(step.manual_only for step in flow.steps)
