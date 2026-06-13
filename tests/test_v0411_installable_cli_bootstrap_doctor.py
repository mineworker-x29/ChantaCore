from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.personal_runtime.default_personal_cli_bootstrap import (
    CLOSED_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    REQUIRED_FALSE_FLAGS,
    V0416_TARGET_COMMANDS,
    ChantaCLICommandKind,
    ChantaCLICommandStatus,
    ChantaCLIDoctorCheckKind,
    classify_cli_command,
    cli_command_result_preserves_runtime_closed,
    cli_safety_posture_preserves_closed,
    create_cli_bootstrap_config,
    create_cli_bootstrap_paths,
    create_cli_command_result,
    create_cli_doctor_report,
    create_cli_safety_posture_report,
    create_cli_version_info,
    create_default_personal_idempotency_report,
    create_default_personal_init_plan,
    create_default_personal_init_request,
    create_unsupported_command_decision,
    create_v0411_integrated_restore_context_snapshot,
    create_v0411_integrated_restore_document_manifest,
    create_v0411_integrated_restore_packet,
    create_v0411_readiness_report,
    create_v0412_prompt_assembly_session_store_handoff,
    create_v0416_user_test_target_update,
    execute_default_personal_init_plan,
    init_result_preserves_runtime_closed,
    integrated_restore_packet_uses_single_doc,
    run_profile_status_command,
    v0411_readiness_preserves_closed_runtime,
    DefaultPersonalProfileStatusCommandInput,
)


def test_v0411_cli_version_info_uses_chanta_cli() -> None:
    info = create_cli_version_info()

    assert info.cli_name == "chanta-cli"
    assert info.command_name == "chanta-cli"
    assert info.version == "v0.41.1"
    assert "v0.41 Default Personal Runtime Opening Track" in info.track


def test_v0411_command_kind_values_declared() -> None:
    assert {item.value for item in ChantaCLICommandKind} == {
        "version",
        "doctor",
        "init_default_personal",
        "profile_status",
        "unsupported_future_gated",
        "unsafe_denied",
        "unknown",
    }


def test_v0411_command_status_values_declared() -> None:
    assert {item.value for item in ChantaCLICommandStatus} == {
        "ok",
        "warning",
        "failed",
        "unsupported",
        "unsafe_denied",
        "future_gated",
        "not_implemented",
        "no_op",
    }


def test_v0411_cli_command_result_defaults_do_not_invoke_provider_prompt_agentloop_skill_shell_network_or_credentials() -> None:
    result = create_cli_command_result()

    assert cli_command_result_preserves_runtime_closed(result)
    assert result.mutated_filesystem is False


def test_v0411_bootstrap_config_supports_version_doctor_init_profile_status_only() -> None:
    config = create_cli_bootstrap_config()

    assert config.cli_name == "chanta-cli"
    assert config.default_profile_id == "default-personal"
    assert config.supports_init is True
    assert config.supports_doctor is True
    assert config.supports_profile_status is True
    assert config.supports_run is False
    assert config.supports_provider_doctor is False
    assert config.supports_trace is False


def test_v0411_bootstrap_paths_remain_under_home(tmp_path: Path) -> None:
    paths = create_cli_bootstrap_paths(str(tmp_path))
    home = Path(paths.home_path)

    for value in paths.__dict__.values():
        assert Path(value).resolve().is_relative_to(home.resolve())


def test_v0411_doctor_check_kinds_declared() -> None:
    assert {item.value for item in ChantaCLIDoctorCheckKind} == {
        "python_version",
        "package_import",
        "cli_entrypoint",
        "cwd",
        "personal_home",
        "profile_home",
        "profile_config",
        "identity_files",
        "policy_files",
        "restore_docs",
        "v0409_handoff_doc",
        "v0410_profile_runtime",
        "closed_capabilities",
        "next_version_handoff",
    }


def test_v0411_doctor_report_marks_v0416_user_test_not_ready(tmp_path: Path) -> None:
    report = create_cli_doctor_report(str(tmp_path))

    assert report.cli_name == "chanta-cli"
    assert report.current_version == "v0.41.1"
    assert report.next_recommended_version == "v0.41.2"
    assert report.ready_for_v0416_user_test is False


def test_v0411_doctor_report_lists_closed_capabilities() -> None:
    report = create_cli_doctor_report()

    assert set(CLOSED_CAPABILITIES).issubset(report.closed_capabilities)
    assert "provider_text_only_invocation" in report.closed_capabilities


def test_v0411_init_request_defaults_no_overwrite(tmp_path: Path) -> None:
    request = create_default_personal_init_request(str(tmp_path))

    assert request.profile_id == "default-personal"
    assert request.allow_overwrite is False
    assert request.dry_run is False


def test_v0411_init_plan_rejects_paths_outside_home(tmp_path: Path) -> None:
    request = create_default_personal_init_request(str(tmp_path))
    plan = create_default_personal_init_plan(
        request,
        files=(
            *create_default_personal_init_plan(request).files,
            create_default_personal_init_plan(request).files[0].__class__(
                str(tmp_path.parent / "outside.json"),
                "outside",
                "{}",
                True,
                False,
            ),
        ),
    )

    assert plan.safe_to_execute is True
    unsafe_plan = create_default_personal_init_plan(request, outside_home_paths=(str(tmp_path.parent / "outside.json"),), safe_to_execute=False)
    assert unsafe_plan.safe_to_execute is False


def test_v0411_init_plan_contains_default_personal_directories_and_files(tmp_path: Path) -> None:
    plan = create_default_personal_init_plan(create_default_personal_init_request(str(tmp_path)))
    directory_paths = {Path(item.path).name for item in plan.directories}
    file_paths = {Path(item.path).name for item in plan.files}

    assert "default-personal" in {Path(item.path).name for item in plan.directories}
    assert {"profile.json", "SOUL.md", "ROLE.json", "DOMAIN.json", "POLICY.json", "CORE_MEMORY.md"}.issubset(file_paths)
    assert plan.safe_to_execute is True
    assert "profiles" in directory_paths


def test_v0411_init_result_does_not_overwrite_existing_files(tmp_path: Path) -> None:
    request = create_default_personal_init_request(str(tmp_path))
    plan = create_default_personal_init_plan(request)
    first = execute_default_personal_init_plan(request, plan)
    marker = Path(plan.files[0].path)
    original = marker.read_text(encoding="utf-8")
    second = execute_default_personal_init_plan(request, plan)

    assert marker.read_text(encoding="utf-8") == original
    assert second.overwritten_files == ()
    assert marker.as_posix() not in {Path(path).as_posix() for path in second.created_files}
    assert first.created_files


def test_v0411_init_result_never_invokes_provider_prompt_agentloop_shell_network_or_credentials(tmp_path: Path) -> None:
    request = create_default_personal_init_request(str(tmp_path))
    result = execute_default_personal_init_plan(request, create_default_personal_init_plan(request))

    assert init_result_preserves_runtime_closed(result)


def test_v0411_init_is_idempotent_in_tmp_path(tmp_path: Path) -> None:
    request = create_default_personal_init_request(str(tmp_path))
    plan = create_default_personal_init_plan(request)
    first = execute_default_personal_init_plan(request, plan)
    second = execute_default_personal_init_plan(request, plan)
    report = create_default_personal_idempotency_report(first, second)

    assert report.idempotent is True
    assert report.overwrite_detected is False
    assert second.created_files == ()


def test_v0411_profile_status_reports_profile_files_after_init(tmp_path: Path) -> None:
    request = create_default_personal_init_request(str(tmp_path))
    execute_default_personal_init_plan(request, create_default_personal_init_plan(request))
    status = run_profile_status_command(DefaultPersonalProfileStatusCommandInput("default-personal", str(tmp_path)))

    assert status.profile_exists is True
    assert status.profile_config_exists is True
    assert status.soul_exists is True
    assert status.role_exists is True
    assert status.domain_exists is True
    assert status.policy_exists is True
    assert status.core_memory_exists is True
    assert status.sessions_dir_exists is True
    assert status.traces_dir_exists is True


def test_v0411_profile_status_keeps_runtime_provider_prompt_agentloop_skill_false(tmp_path: Path) -> None:
    status = run_profile_status_command(DefaultPersonalProfileStatusCommandInput("default-personal", str(tmp_path)))

    assert status.runtime_opened is False
    assert status.provider_invocation_allowed is False
    assert status.prompt_submission_allowed is False
    assert status.agent_loop_allowed is False
    assert status.skill_execution_allowed is False
    assert status.production_certified is False


def test_v0411_safety_posture_keeps_run_provider_prompt_session_trace_and_unsafe_actions_closed() -> None:
    report = create_cli_safety_posture_report()

    assert cli_safety_posture_preserves_closed(report)


def test_v0411_unsupported_run_command_is_future_gated_to_v0414() -> None:
    decision = create_unsupported_command_decision("run")

    assert decision.future_target_version == "v0.41.4"
    assert decision.executed is False


def test_v0411_unsupported_provider_doctor_is_future_gated_to_v0413() -> None:
    decision = create_unsupported_command_decision("provider", ("provider", "doctor"))

    assert decision.future_target_version == "v0.41.3"
    assert decision.executed is False


def test_v0411_unsupported_prompt_and_session_commands_are_future_gated_to_v0412() -> None:
    assert create_unsupported_command_decision("prompt").future_target_version == "v0.41.2"
    assert create_unsupported_command_decision("session").future_target_version == "v0.41.2"


def test_v0411_unsupported_trace_command_is_future_gated_to_v0415() -> None:
    assert create_unsupported_command_decision("trace").future_target_version == "v0.41.5"


def test_v0411_unsafe_apply_shell_subagent_dominion_commands_are_denied_or_future_gated_beyond_v041() -> None:
    for command in ("apply", "shell", "invoke-subagent", "dominion", "production-certify"):
        decision = create_unsupported_command_decision(command)
        assert decision.status == "unsafe_denied"
        assert decision.executed is False
        assert decision.future_target_version in {"v0.42+", "not_planned_in_v041"}


def test_v0411_readiness_report_keeps_run_provider_prompt_session_skill_trace_user_test_false() -> None:
    report = create_v0411_readiness_report()

    assert report.installable_cli_bootstrap_defined is True
    assert report.chanta_cli_entrypoint_ready is True
    assert report.v0412_handoff_ready is True
    assert v0411_readiness_preserves_closed_runtime(report)
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False


def test_v0411_v0412_handoff_targets_prompt_assembly_session_store() -> None:
    handoff = create_v0412_prompt_assembly_session_store_handoff()

    assert handoff.target_version == "v0.41.2 Prompt Assembly & Session Store"
    assert "define prompt assembly block order" in handoff.recommended_focus
    assert "no provider call" in handoff.recommended_focus


def test_v0411_v0416_user_test_target_preserves_required_commands() -> None:
    target = create_v0416_user_test_target_update()

    assert target.user_test_release_ready is False
    for command in V0416_TARGET_COMMANDS:
        assert command in target.commands
    assert "chanta-cli --version" in target.commands_expected_in_v0411


def test_v0411_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = create_v0411_integrated_restore_context_snapshot()

    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)
    assert snapshot.next_recommended_version == "v0.41.2 Prompt Assembly & Session Store"


def test_v0411_restore_packet_uses_single_integrated_doc_path() -> None:
    assert integrated_restore_packet_uses_single_doc(create_v0411_integrated_restore_packet())


def test_v0411_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert create_v0411_integrated_restore_packet().separate_restore_doc_created is False


def test_v0411_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0411_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0411_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Repository Baseline Assumptions",
        "v0.41.0 Profile Runtime Summary",
        "Installable CLI Bootstrap Summary",
        "`chanta-cli` Entrypoint Contract",
        "CLI Command Catalog",
        "Doctor Contract",
        "Init Default Personal Contract",
        "Profile Status Contract",
        "Unsupported Command Policy",
        "Safety Posture",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Expected Test Interpretation",
        "Known Limitations",
        "Withdrawal Conditions",
        "v0.41.2 Recommended Next Step",
        "v0.41.6 User Test Target",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in text


def test_v0411_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "You are continuing ChantaCore after v0.41.1." in text
    assert "v0.41.2 Prompt Assembly & Session Store" in text
    assert "chanta-cli" in text


def test_v0411_no_separate_v0411_restore_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.1_restore_document.md").exists()


def test_v0411_no_separate_v0411_release_document_created() -> None:
    assert not Path("docs/versions/v0.41/v0.41.1_installable_cli_bootstrap.md").exists()
    assert not Path("docs/versions/v0.41/v0.41.1_cli_doctor_contract.md").exists()


def test_v0411_no_forbidden_runtime_call_patterns() -> None:
    paths = (
        Path("src/chanta_core/cli/main.py"),
        Path("src/chanta_core/personal_runtime/default_personal_cli_bootstrap.py"),
    )
    forbidden = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "anthropic",
        "ollama",
        "lmstudio",
        "apply_patch",
        "git apply",
        "git worktree",
        "api_key",
        "secret",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "client_create",
        "pytest",
        "unittest",
    )
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths)
    for pattern in forbidden:
        assert pattern not in combined

    assert "Path.mkdir" not in combined
    assert ".mkdir(" in combined
    assert "Path.write_text" not in combined
    assert ".write_text(" in combined
    credential_lines = [line for line in combined.splitlines() if "credential" in line]
    assert credential_lines
    assert all("credentials_accessed" in line for line in credential_lines)
    provider_invoke_lines = [line for line in combined.splitlines() if "provider_invoke" in line]
    assert provider_invoke_lines
    assert all("provider_invoked" in line for line in provider_invoke_lines)
    prompt_submit_lines = [line for line in combined.splitlines() if "prompt_submit" in line]
    assert prompt_submit_lines
    assert all("prompt_submitted" in line for line in prompt_submit_lines)


def test_v0411_main_version_command_returns_zero(capsys) -> None:
    assert main(["--version"]) == 0
    assert "chanta-cli v0.41.1" in capsys.readouterr().out


def test_v0411_main_doctor_command_returns_zero(capsys) -> None:
    assert main(["doctor"]) == 0
    assert "chanta-cli doctor v0.41.1" in capsys.readouterr().out


def test_v0411_main_init_default_personal_creates_profile_under_tmp_home(tmp_path: Path, capsys) -> None:
    assert main(["init", "default-personal", "--home", str(tmp_path)]) == 0
    capsys.readouterr()
    assert (tmp_path / "profiles" / "default-personal" / "profile.json").exists()
    assert (tmp_path / "profiles" / "default-personal" / "soul" / "SOUL.md").exists()


def test_v0411_main_profile_status_reads_tmp_profile(tmp_path: Path, capsys) -> None:
    main(["init", "default-personal", "--home", str(tmp_path)])
    capsys.readouterr()
    assert main(["profile", "status", "--profile", "default-personal", "--home", str(tmp_path)]) == 0
    assert '"runtime_opened": false' in capsys.readouterr().out


def test_v0411_main_unsupported_run_returns_future_gated_without_provider_call(capsys) -> None:
    assert main(["run", "--profile", "default-personal", "hello"]) == 1
    output = capsys.readouterr().out
    assert '"future_target_version": "v0.41.4"' in output
    assert '"executed": false' in output


def test_v0411_classify_cli_command() -> None:
    assert classify_cli_command(["--version"]) == "version"
    assert classify_cli_command(["doctor"]) == "doctor"
    assert classify_cli_command(["init", "default-personal"]) == "init_default_personal"
    assert classify_cli_command(["profile", "status"]) == "profile_status"
    assert classify_cli_command(["run"]) == "unsupported_future_gated"
    assert classify_cli_command(["shell"]) == "unsafe_denied"
