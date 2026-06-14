from __future__ import annotations

import json
from pathlib import Path

import pytest

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_provider_setup as v0422
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart


def _prepared_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    result = run_v042_quickstart(explicit_home=str(home))
    assert result.exit_code == 0
    return home


def _provider_path(home: Path) -> Path:
    return home / "profiles" / "default-personal" / "profile" / "PROVIDER.json"


def test_v0422_provider_setup_modes_declared() -> None:
    assert {item.value for item in v0422.V042ProviderSetupMode} == {
        "mock",
        "local_openai_compatible",
        "openai_compatible",
        "status_only",
        "dry_run",
        "unknown",
    }


def test_v0422_provider_setup_status_values_declared() -> None:
    assert {item.value for item in v0422.V042ProviderSetupStatus} == {
        "pass",
        "pass_with_notes",
        "failed",
        "blocked",
        "conflict",
        "dry_run",
        "not_configured",
        "invalid",
    }


def test_v0422_provider_profile_kinds_declared() -> None:
    assert {item.value for item in v0422.V042ProviderProfileKind} == {"default_personal", "test_fixture", "custom_personal", "unknown"}


def test_v0422_provider_preset_kinds_declared() -> None:
    assert {item.value for item in v0422.V042ProviderPresetKind} == {
        "mock",
        "local_openai_compatible",
        "lm_studio_compatible",
        "openai_compatible",
        "unknown",
    }


def test_v0422_provider_config_path_policy_bounds_provider_json_under_home_and_stores_no_secrets() -> None:
    policy = v0422.create_v042_provider_config_path_policy()
    assert policy.config_filename == "PROVIDER.json"
    assert policy.relative_config_path == "profiles/default-personal/profile/PROVIDER.json"
    assert policy.bounded_to_home is True
    assert policy.write_outside_home_allowed is False
    assert policy.overwrite_existing_allowed is False
    assert policy.create_if_missing_allowed is True
    assert policy.stores_secret_values is False


def test_v0422_provider_preset_registry_supports_mock_and_local_openai_but_no_tool_or_function_calling() -> None:
    registry = v0422.build_v042_provider_preset_registry()
    assert registry.supports_mock is True
    assert registry.supports_local_openai_compatible is True
    assert registry.supports_tool_calling is False
    assert registry.supports_function_calling is False


def test_v0422_mock_provider_preset_requires_no_base_url_model_or_api_key() -> None:
    preset = v0422.create_v042_provider_preset("mock")
    assert preset.requires_base_url is False
    assert preset.requires_model is False
    assert preset.requires_api_key_env is False
    assert preset.setup_calls_provider is False
    assert preset.status_calls_provider is False


def test_v0422_local_openai_preset_requires_base_url_and_model() -> None:
    preset = v0422.create_v042_provider_preset("local_openai_compatible")
    assert preset.requires_base_url is True
    assert preset.requires_model is True
    assert preset.setup_calls_provider is False
    assert preset.status_calls_provider is False


def test_v0422_provider_config_draft_never_enables_tool_or_function_calling() -> None:
    draft = v0422.create_v042_provider_config_draft("local_openai_compatible", base_url="http://localhost:1234/v1", model="local-model")
    assert draft.tool_calling_allowed is False
    assert draft.function_calling_allowed is False


def test_v0422_provider_config_draft_never_allows_completion_in_doctor() -> None:
    draft = v0422.create_v042_provider_config_draft("local_openai_compatible", base_url="http://localhost:1234/v1", model="local-model")
    assert draft.completion_allowed_in_doctor is False
    assert draft.completion_allowed_in_run is True


def test_v0422_provider_config_validation_rejects_missing_local_base_url_or_model() -> None:
    draft = v0422.create_v042_provider_config_draft("local_openai_compatible", base_url=None, model=None)
    report = v0422.validate_v042_provider_config_draft(draft)
    assert report.valid_for_setup is False
    ids = {item.finding_id for item in report.findings}
    assert {"missing-base-url", "missing-model"} <= ids


def test_v0422_provider_env_secret_policy_stores_env_var_name_only_and_never_prints_value() -> None:
    policy = v0422.create_v042_provider_env_secret_policy()
    assert policy.stores_secret_values is False
    assert policy.stores_env_var_name_only is True
    assert policy.checks_presence_without_loading_value is True
    assert policy.prints_secret_value is False


def test_v0422_provider_setup_plan_never_calls_provider_or_prints_secret(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    request = v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock")
    plan = v0422.create_v042_provider_setup_plan(request)
    assert plan.will_call_provider is False
    assert plan.will_print_secret is False
    assert plan.will_overwrite is False


def test_v0422_provider_setup_plan_blocks_outside_home_config_path(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    request = v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock")
    plan = v0422.create_v042_provider_setup_plan(request, config_path=str(tmp_path.parent / "outside" / "PROVIDER.json"), outside_home_paths=(str(tmp_path.parent / "outside"),), safe_to_execute=False)
    assert plan.safe_to_execute is False
    assert plan.outside_home_paths


def test_v0422_provider_setup_dry_run_does_not_write_file(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    request = v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock", dry_run=True)
    result = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    assert result.status == "dry_run"
    assert result.write_result.dry_run is True
    assert not _provider_path(home).exists()


def test_v0422_provider_setup_mock_writes_bounded_provider_config_when_missing(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    request = v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock")
    result = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    assert result.status == "pass"
    assert result.write_result.created is True
    data = json.loads(_provider_path(home).read_text(encoding="utf-8"))
    assert data["provider_kind"] == "mock"
    assert "api_key" not in data


def test_v0422_provider_setup_local_openai_writes_bounded_provider_config_when_valid(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    request = v0422.create_v042_provider_setup_request(
        setup_mode="local_openai_compatible",
        preset_kind="local_openai_compatible",
        home_path=str(home),
        base_url="http://localhost:1234/v1",
        model="local-model",
        api_key_env_var="OPENAI_API_KEY",
    )
    result = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    assert result.status == "pass"
    data = json.loads(_provider_path(home).read_text(encoding="utf-8"))
    assert data["provider_kind"] == "local_openai_compatible"
    assert data["base_url"] == "http://localhost:1234/v1"
    assert data["model"] == "local-model"
    assert data["api_key_env_var"] == "OPENAI_API_KEY"


def test_v0422_provider_setup_is_idempotent_for_identical_existing_config(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    request = v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock")
    first = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    second = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    assert first.status == "pass"
    assert second.status == "pass"
    assert second.write_result.skipped_existing_identical is True


def test_v0422_provider_setup_blocks_conflicting_existing_config_without_replace(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    mock_request = v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock")
    assert v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(mock_request)).status == "pass"
    local_request = v0422.create_v042_provider_setup_request(
        setup_mode="local_openai_compatible",
        preset_kind="local_openai_compatible",
        home_path=str(home),
        base_url="http://localhost:1234/v1",
        model="local-model",
    )
    result = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(local_request))
    assert result.status == "conflict"
    assert result.write_result.blocked_conflict is True


def test_v0422_provider_setup_result_never_invokes_provider_prompt_shell_subagent_or_production(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(v0422.create_v042_provider_setup_request(home_path=str(home), setup_mode="mock")))
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.real_provider_called is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False


def test_v0422_provider_status_reports_config_and_redacts_secret(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "not-to-print")
    request = v0422.create_v042_provider_setup_request("local_openai_compatible", str(home), preset_kind="local_openai_compatible", base_url="http://localhost:1234/v1", model="local-model", api_key_env_var="OPENAI_API_KEY")
    v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    report = v0422.create_v042_provider_status_report(v0422.create_v042_provider_status_request(str(home)))
    assert report.config_present is True
    assert report.api_key_env_var == "OPENAI_API_KEY"
    assert report.api_key_env_present is True
    assert report.secret_redacted is True
    assert "not-to-print" not in report.rendered_text


def test_v0422_provider_config_show_returns_redacted_config_only(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("OPENAI_API_KEY", "actual-secret")
    request = v0422.create_v042_provider_setup_request("local_openai_compatible", str(home), preset_kind="local_openai_compatible", base_url="http://localhost:1234/v1", model="local-model", api_key_env_var="OPENAI_API_KEY")
    v0422.create_v042_provider_setup_result(v0422.create_v042_provider_setup_plan(request))
    result = v0422.create_v042_provider_config_show_result(v0422.create_v042_provider_config_show_request(str(home)))
    assert result.config_present is True
    assert result.secret_values_redacted is True
    assert "actual-secret" not in result.rendered_text
    assert result.provider_invoked is False


def test_v0422_provider_run_readiness_distinguishes_mock_ready_from_configured_provider_ready() -> None:
    mock = v0422.create_v042_provider_run_readiness_report(v0422.create_v042_provider_config_draft("mock"), True)
    local = v0422.create_v042_provider_run_readiness_report(v0422.create_v042_provider_config_draft("local_openai_compatible", base_url="http://localhost:1234/v1", model="local-model"), True)
    assert mock.mock_run_ready is True
    assert mock.configured_provider_run_ready is False
    assert local.configured_provider_run_ready is True


def test_v0422_provider_doctor_ux_interpretation_says_no_completion(tmp_path: Path) -> None:
    report = v0422.create_v042_provider_status_report(v0422.create_v042_provider_status_request(str(_prepared_home(tmp_path))))
    interpretation = v0422.create_v042_provider_doctor_ux_interpretation(report)
    assert interpretation.doctor_means_completion_ready is False
    assert interpretation.doctor_sends_completion is False
    assert "no-completion" in interpretation.user_explanation


def test_v0422_provider_troubleshooting_items_include_missing_config_base_url_model_api_key_lm_studio_and_doctor_passes_but_run_fails() -> None:
    text = "\n".join(item.item_id for item in v0422.build_v042_provider_troubleshooting_items())
    assert "missing-config" in text
    assert "missing-base-url" in text
    assert "missing-model" in text
    assert "openai-api-key-not-set" in text
    assert "lm-studio-server-not-running" in text
    assert "doctor-passes-run-fails" in text


def test_v0422_provider_user_guide_sections_cover_status_mock_local_openai_doctor_run_and_troubleshooting() -> None:
    titles = {section.title for section in v0422.build_v042_provider_user_guide_sections()}
    assert {
        "Current Provider Status",
        "Mock Provider Setup",
        "Local OpenAI-compatible Provider Setup",
        "Provider Doctor",
        "Running with Mock Provider",
        "Running with Configured Provider",
        "Troubleshooting",
        "What Provider Setup Does Not Do",
    } <= titles


def test_v0422_provider_ux_safety_report_keeps_setup_status_no_provider_call_and_closes_tools_functions_shell_subagent_and_production() -> None:
    report = v0422.create_v042_provider_ux_safety_report()
    assert report.provider_setup_calls_provider is False
    assert report.provider_status_calls_provider is False
    assert report.provider_doctor_completion_closed is True
    assert report.tool_calling_closed is True
    assert report.function_calling_closed is True
    assert report.shell_closed is True
    assert report.subagent_closed is True
    assert report.production_certified is False


def test_v0422_readiness_report_sets_provider_setup_ux_flags_true() -> None:
    report = v0422.create_v0422_readiness_report()
    assert report.provider_preset_registry_ready is True
    assert report.provider_setup_mock_ready is True
    assert report.provider_setup_local_openai_ready is True
    assert report.provider_status_command_ready is True
    assert report.provider_config_show_command_ready is True
    assert report.provider_setup_dry_run_ready is True


def test_v0422_readiness_report_keeps_provider_doctor_completion_tool_function_shell_subagent_and_production_flags_false() -> None:
    report = v0422.create_v0422_readiness_report()
    assert report.ready_for_provider_doctor_completion is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.production_certified is False


def test_v0422_v0423_handoff_targets_human_readable_trace_and_run_history() -> None:
    handoff = v0422.create_v0423_trace_history_ux_handoff()
    assert handoff.target_version == "v0.42.3"
    assert "run history" in handoff.recommended_focus
    assert "shell_execution" in handoff.must_not_open


def test_v0422_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0422.create_v0422_integrated_restore_context_snapshot()
    assert "provider_preset_registry" in snapshot.open_capabilities
    assert "provider_config_show_command" in snapshot.open_capabilities
    assert "provider_doctor_completion" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0422_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0422.create_v0422_integrated_restore_packet()
    assert packet.single_integrated_doc_path == "docs/versions/v0.42/v0.42.2_provider_setup_ux_restore.md"


def test_v0422_restore_packet_marks_separate_restore_doc_created_false() -> None:
    assert v0422.create_v0422_integrated_restore_packet().separate_restore_doc_created is False


def test_v0422_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0422.create_v0422_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True


def test_v0422_integrated_document_exists_and_has_required_restore_sections() -> None:
    text = Path("docs/versions/v0.42/v0.42.2_provider_setup_ux_restore.md").read_text(encoding="utf-8")
    for title in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Provider Setup UX Summary",
        "Provider Preset Registry",
        "Provider Config Contract",
        "Provider Status Contract",
        "Provider UX Safety Boundary",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert f"## {title}" in text


def test_v0422_integrated_document_contains_provider_setup_examples_and_copy_paste_restore_prompt() -> None:
    text = Path("docs/versions/v0.42/v0.42.2_provider_setup_ux_restore.md").read_text(encoding="utf-8")
    assert "chanta-cli provider setup mock" in text
    assert "chanta-cli provider setup local-openai" in text
    assert "You are continuing ChantaCore after v0.42.2." in text
    assert "v0.42.3 Human-readable Trace / Run History" in text


def test_v0422_no_separate_v0422_restore_provider_setup_or_user_guide_documents_created() -> None:
    assert not Path("docs/versions/v0.42/v0.42.2_restore_document.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.2_provider_setup.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.2_provider_config_contract.md").exists()
    assert not Path("docs/versions/v0.42/v0.42.2_provider_user_guide.md").exists()


def test_v0422_no_forbidden_runtime_call_patterns_except_bounded_provider_config_write() -> None:
    text = Path("src/chanta_core/personal_runtime/default_personal_provider_setup.py").read_text(encoding="utf-8")
    for forbidden in (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "anthropic",
        "ollama",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "pytest",
        "unittest",
    ):
        assert forbidden not in text


def test_v0422_cli_provider_status_uses_default_home_resolver(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["provider", "status"]) == 0


def test_v0422_cli_provider_setup_mock_then_status_then_config_show(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["provider", "setup", "mock"]) == 0
    assert cli_main(["provider", "status"]) == 0
    assert cli_main(["provider", "config", "show"]) == 0


def test_v0422_cli_provider_setup_local_openai_dry_run_does_not_write(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["provider", "setup", "local-openai", "--base-url", "http://localhost:1234/v1", "--model", "local-model", "--dry-run"]) == 0
    assert not _provider_path(home).exists()


def test_v0422_cli_provider_setup_local_openai_then_provider_doctor_no_completion(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["provider", "setup", "local-openai", "--base-url", "http://localhost:1234/v1", "--model", "local-model"]) == 0
    assert cli_main(["provider", "doctor", "--profile", "default-personal", "--no-completion"]) == 0


def test_v0422_cli_provider_setup_does_not_call_real_provider(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["provider", "setup", "mock"]) == 0
    report = v0422.create_v042_provider_status_report(v0422.create_v042_provider_status_request(str(home)))
    assert report.provider_invoked is False
    assert report.prompt_submitted is False


def test_v0422_cli_run_with_mock_after_provider_setup_still_works(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["provider", "setup", "mock"]) == 0
    assert cli_main(["run", "--profile", "default-personal", "--provider", "mock", "Summarize what ChantaCore is in three bullets."]) == 0
