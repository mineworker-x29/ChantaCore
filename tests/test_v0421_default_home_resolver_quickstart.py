from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_home_quickstart as v0421


def test_v0421_home_resolution_sources_declared() -> None:
    assert {item.value for item in v0421.V042HomeResolutionSource} == {
        "explicit_home_arg",
        "chantacore_home_env",
        "platform_default",
        "unresolved",
        "invalid",
    }


def test_v0421_home_resolution_status_values_declared() -> None:
    assert {item.value for item in v0421.V042HomeResolutionStatus} == {
        "resolved",
        "resolved_missing",
        "unresolved",
        "invalid",
        "blocked",
    }


def test_v0421_default_home_policy_uses_explicit_env_platform_order() -> None:
    policy = v0421.create_v042_default_home_policy()
    assert policy.resolution_order == ("explicit_home_arg", "chantacore_home_env", "platform_default")
    assert policy.env_var_name == "CHANTACORE_HOME"
    assert policy.explicit_home_supported is True
    assert policy.env_override_supported is True
    assert policy.platform_default_supported is True


def test_v0421_default_home_policy_disallows_silent_auto_create() -> None:
    policy = v0421.create_v042_default_home_policy()
    assert policy.silent_auto_create_allowed is False
    assert policy.quickstart_auto_create_allowed is True
    assert policy.init_auto_create_allowed is True


def test_v0421_windows_default_home_uses_localappdata_chantacore(tmp_path: Path) -> None:
    request = v0421.create_v042_home_resolution_request(
        env={"LOCALAPPDATA": str(tmp_path), "PATH": ""},
        platform="windows",
    )
    resolved = v0421.resolve_v042_home(request)
    assert resolved.home_path == str(tmp_path / "ChantaCore")
    assert resolved.source == "platform_default"


def test_v0421_resolve_home_prefers_explicit_home_over_env_and_platform(tmp_path: Path) -> None:
    explicit = tmp_path / "explicit"
    env_home = tmp_path / "env"
    request = v0421.create_v042_home_resolution_request(
        explicit_home=str(explicit),
        env={"CHANTACORE_HOME": str(env_home), "LOCALAPPDATA": str(tmp_path / "local")},
        platform="windows",
    )
    resolved = v0421.resolve_v042_home(request)
    assert resolved.home_path == str(explicit)
    assert resolved.source == "explicit_home_arg"


def test_v0421_resolve_home_uses_chantacore_home_env_when_no_explicit_home(tmp_path: Path) -> None:
    env_home = tmp_path / "env"
    request = v0421.create_v042_home_resolution_request(
        env={"CHANTACORE_HOME": str(env_home), "LOCALAPPDATA": str(tmp_path / "local")},
        platform="windows",
    )
    resolved = v0421.resolve_v042_home(request)
    assert resolved.home_path == str(env_home)
    assert resolved.source == "chantacore_home_env"


def test_v0421_resolve_home_uses_platform_default_when_no_explicit_or_env(tmp_path: Path) -> None:
    request = v0421.create_v042_home_resolution_request(
        env={"LOCALAPPDATA": str(tmp_path / "local")},
        platform="windows",
    )
    resolved = v0421.resolve_v042_home(request)
    assert resolved.home_path == str(tmp_path / "local" / "ChantaCore")
    assert resolved.source == "platform_default"


def test_v0421_home_resolver_does_not_create_directories(tmp_path: Path) -> None:
    home = tmp_path / "missing-home"
    request = v0421.create_v042_home_resolution_request(explicit_home=str(home), allow_create=True)
    resolved = v0421.resolve_v042_home(request)
    assert resolved.created_by_resolver is False
    assert resolved.exists is False
    assert not home.exists()


def test_v0421_home_validation_allows_quickstart_create_but_not_silent_readonly_create(tmp_path: Path) -> None:
    resolved = v0421.resolve_v042_home(v0421.create_v042_home_resolution_request(explicit_home=str(tmp_path / "home")))
    report = v0421.validate_v042_resolved_home(resolved, allow_create=True)
    assert report.valid_for_read_only_commands is False
    assert report.valid_for_quickstart is True
    assert report.silent_creation_required is False


def test_v0421_home_show_command_is_read_only_and_non_provider(tmp_path: Path) -> None:
    result = v0421.create_v042_home_show_command_result(
        v0421.create_v042_home_show_command_input(str(tmp_path), json_output=False)
    )
    assert result.mutated_filesystem is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False
    assert "ChantaCore home" in result.rendered_text


def test_v0421_home_status_command_is_read_only_and_reports_profile_state(tmp_path: Path) -> None:
    result = v0421.create_v042_home_status_command_result(v0421.create_v042_home_status_command_input(str(tmp_path)))
    assert result.mutated_filesystem is False
    assert result.provider_invoked is False
    assert result.profile_id == "default-personal"
    assert result.profile_exists is False
    assert result.profile_config_exists is False
    assert result.sessions_dir_exists is False
    assert result.traces_dir_exists is False


def test_v0421_command_home_adoption_records_existing_safe_commands() -> None:
    records = v0421.build_v042_command_home_adoption_records()
    names = {record.command_name for record in records}
    assert {
        "profile status",
        "provider doctor",
        "prompt preview",
        "session new",
        "session list",
        "run",
        "trace recent",
        "trace summary",
        "run-report last",
        "safety check-command",
    } <= names


def test_v0421_command_home_adoption_does_not_allow_readonly_commands_to_create_home() -> None:
    assert all(record.creates_home_when_missing is False for record in v0421.build_v042_command_home_adoption_records())


def test_v0421_quickstart_modes_declared() -> None:
    assert {item.value for item in v0421.V042QuickstartMode} == {"setup_only", "with_mock_run", "status_only", "unknown"}


def test_v0421_quickstart_plan_setup_only_does_not_call_real_provider_or_shell(tmp_path: Path) -> None:
    resolved = v0421.resolve_v042_home(v0421.create_v042_home_resolution_request(explicit_home=str(tmp_path / "home")))
    plan = v0421.create_v042_quickstart_plan(resolved)
    assert plan.will_run_mock_provider is False
    assert plan.will_call_real_provider is False
    assert plan.will_execute_shell is False
    assert plan.safe_to_execute is True


def test_v0421_quickstart_creates_default_personal_profile_when_missing(tmp_path: Path) -> None:
    home = tmp_path / "home"
    result = v0421.run_v042_quickstart(explicit_home=str(home))
    assert result.exit_code == 0
    assert (home / "profiles" / "default-personal" / "profile.json").exists()
    assert any(step.step_kind == "init_profile_if_missing" and step.mutated_filesystem for step in result.steps)


def test_v0421_quickstart_is_idempotent_and_does_not_overwrite_existing_files(tmp_path: Path) -> None:
    home = tmp_path / "home"
    first = v0421.run_v042_quickstart(explicit_home=str(home))
    profile_config = home / "profiles" / "default-personal" / "profile.json"
    before = profile_config.read_text(encoding="utf-8")
    second = v0421.run_v042_quickstart(explicit_home=str(home))
    after = profile_config.read_text(encoding="utf-8")
    assert first.exit_code == 0
    assert second.exit_code == 0
    assert before == after
    assert not any(step.step_kind == "init_profile_if_missing" and step.mutated_filesystem for step in second.steps)


def test_v0421_quickstart_provider_doctor_is_no_completion(tmp_path: Path) -> None:
    result = v0421.run_v042_quickstart(explicit_home=str(tmp_path / "home"))
    doctor_steps = [step for step in result.steps if step.step_kind == "provider_doctor_no_completion"]
    assert doctor_steps
    assert doctor_steps[0].status == "pass"
    assert "completion=false" in doctor_steps[0].message


def test_v0421_quickstart_with_mock_run_uses_mock_provider_only(tmp_path: Path) -> None:
    result = v0421.run_v042_quickstart(explicit_home=str(tmp_path / "home"), with_mock_run=True)
    assert result.mock_run_result is not None
    assert result.mock_run_result.attempted is True
    assert result.mock_run_result.provider_invoked is True
    assert result.mock_run_result.real_provider_invoked is False


def test_v0421_quickstart_with_mock_run_appends_session_and_trace(tmp_path: Path) -> None:
    home = tmp_path / "home"
    result = v0421.run_v042_quickstart(explicit_home=str(home), with_mock_run=True)
    assert result.mock_run_result is not None
    assert result.mock_run_result.session_id
    assert result.mock_run_result.run_id
    assert result.mock_run_result.trace_event_count and result.mock_run_result.trace_event_count >= 3
    assert (home / "profiles" / "default-personal" / "state" / "sessions").exists()
    assert (home / "profiles" / "default-personal" / "state" / "traces").exists()


def test_v0421_quickstart_with_mock_run_does_not_call_real_provider(tmp_path: Path) -> None:
    result = v0421.run_v042_quickstart(explicit_home=str(tmp_path / "home"), with_mock_run=True)
    assert result.mock_run_result is not None
    assert result.mock_run_result.real_provider_invoked is False
    assert result.real_provider_tested is False


def test_v0421_quickstart_next_actions_include_mock_run_provider_setup_trace_run_report_and_safety_check() -> None:
    actions = v0421.build_v042_quickstart_next_actions()
    text = "\n".join(action.command_text for action in actions)
    assert "run --profile default-personal --provider mock" in text
    assert "v0.42.2 Provider Setup UX" in text
    assert "trace recent" in text
    assert "run-report last" in text
    assert "safety check-command" in text


def test_v0421_quickstart_safety_report_keeps_provider_doctor_completion_tools_functions_shell_subagent_and_production_closed(tmp_path: Path) -> None:
    result = v0421.run_v042_quickstart(explicit_home=str(tmp_path / "home"))
    report = v0421.create_v042_quickstart_safety_report(result)
    assert report.provider_doctor_completion_closed is True
    assert report.real_provider_not_called_by_default is True
    assert report.tool_calling_closed is True
    assert report.function_calling_closed is True
    assert report.shell_closed is True
    assert report.subagent_closed is True
    assert report.production_certified is False


def test_v0421_readiness_report_sets_home_resolver_quickstart_flags_true() -> None:
    report = v0421.create_v0421_readiness_report()
    assert report.default_home_policy_ready is True
    assert report.home_resolver_ready is True
    assert report.chantacore_home_env_override_ready is True
    assert report.platform_default_home_ready is True
    assert report.home_show_command_ready is True
    assert report.home_status_command_ready is True
    assert report.existing_commands_can_omit_home is True
    assert report.quickstart_command_ready is True
    assert report.quickstart_setup_only_ready is True
    assert report.quickstart_mock_run_ready is True


def test_v0421_readiness_report_keeps_provider_setup_real_provider_wizard_high_risk_and_production_flags_false() -> None:
    report = v0421.create_v0421_readiness_report()
    assert report.ready_for_provider_setup_command is False
    assert report.ready_for_real_provider_wizard is False
    assert report.ready_for_provider_doctor_completion is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_read_only_skill_execution_as_actions is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.production_certified is False


def test_v0421_v0422_handoff_targets_provider_setup_ux() -> None:
    handoff = v0421.create_v0422_provider_setup_ux_handoff()
    assert handoff.target_version == "v0.42.2"
    assert handoff.title == "Provider Setup UX"
    assert "provider setup command" in handoff.recommended_focus
    assert "function_calling" in handoff.must_remain_closed
    assert handoff.production_certified is False


def test_v0421_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0421.create_v0421_integrated_restore_context_snapshot()
    assert "default_home_resolver" in snapshot.open_capabilities
    assert "quickstart_with_mock_run" in snapshot.open_capabilities
    assert "provider_setup_command" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0421_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0421.create_v0421_integrated_restore_packet()
    assert packet.single_integrated_doc_path == "docs/versions/v0.42/v0.42.1_default_home_resolver_quickstart_restore.md"


def test_v0421_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert v0421.create_v0421_integrated_restore_packet().separate_restore_doc_created is False


def test_v0421_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0421.create_v0421_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0421_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path("docs/versions/v0.42/v0.42.1_default_home_resolver_quickstart_restore.md").read_text(encoding="utf-8")
    for title in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Project Context for New Codex Session",
        "Home Resolution Policy",
        "Home Resolution Order",
        "Quickstart Setup-only Contract",
        "Quickstart Mock-run Contract",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert f"## {title}" in text


def test_v0421_integrated_document_contains_home_resolution_order_and_quickstart_examples() -> None:
    text = Path("docs/versions/v0.42/v0.42.1_default_home_resolver_quickstart_restore.md").read_text(encoding="utf-8")
    assert "explicit `--home`" in text
    assert "`CHANTACORE_HOME`" in text
    assert "%LOCALAPPDATA%\\\\ChantaCore" in text
    assert "chanta-cli quickstart --with-mock-run" in text


def test_v0421_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path("docs/versions/v0.42/v0.42.1_default_home_resolver_quickstart_restore.md").read_text(encoding="utf-8")
    assert "You are continuing ChantaCore after v0.42.1." in text
    assert "Next recommended version:" in text
    assert "v0.42.2 Provider Setup UX" in text


def test_v0421_no_separate_v0421_restore_document_created() -> None:
    assert not Path("docs/versions/v0.42/v0.42.1_restore_document.md").exists()


def test_v0421_no_separate_v0421_home_or_quickstart_document_created() -> None:
    assert not Path("docs/versions/v0.42/v0.42.1_default_home_resolver.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.1_quickstart.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.1_home_contract.md").exists()


def test_v0421_no_forbidden_runtime_call_patterns_except_existing_bounded_stores_and_mock_run_orchestration() -> None:
    checked = [
        Path("src/chanta_core/personal_runtime/default_personal_home_quickstart.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    forbidden = (
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
    for path in checked:
        text = path.read_text(encoding="utf-8")
        for item in forbidden:
            assert item not in text


def test_v0421_cli_home_show_uses_chantacore_home_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    monkeypatch.setenv("CHANTACORE_HOME", str(tmp_path / "env-home"))
    assert cli_main(["home", "show"]) == 0
    output = capsys.readouterr().out
    assert "chantacore_home_env" in output
    assert str(tmp_path / "env-home") in output


def test_v0421_cli_quickstart_setup_only_under_env_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "env-home"
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["quickstart"]) == 0
    assert (home / "profiles" / "default-personal" / "profile.json").exists()


def test_v0421_cli_run_omits_home_and_uses_chantacore_home_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "env-home"
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["quickstart"]) == 0
    assert cli_main(["run", "--profile", "default-personal", "--provider", "mock", "Summarize what ChantaCore is in three bullets."]) == 0


def test_v0421_cli_trace_recent_omits_home_and_uses_chantacore_home_env(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "env-home"
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["quickstart", "--with-mock-run"]) == 0
    assert cli_main(["trace", "recent", "--profile", "default-personal", "--limit", "10"]) == 0


def test_v0421_cli_quickstart_with_mock_run_then_run_report_last_works(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = tmp_path / "env-home"
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["quickstart", "--with-mock-run"]) == 0
    assert cli_main(["run-report", "last", "--profile", "default-personal"]) == 0


def test_v0421_cli_home_missing_readonly_command_suggests_quickstart_without_creating_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]) -> None:
    home = tmp_path / "missing"
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["trace", "recent", "--profile", "default-personal", "--limit", "10"]) == 1
    output = capsys.readouterr().out
    assert "quickstart" in output
    assert not home.exists()
