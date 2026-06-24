from pathlib import Path

from chanta_core.personal_runtime import default_personal_schumpeter_lobby as lobby
from chanta_core.personal_runtime import default_personal_work_session as work


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.8_schumpeter_rebrand_start_lobby_restore.md"
SCAN_PATHS = (
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_schumpeter_lobby.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_conversation_router.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_chat_shell.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_pilot_closure.py",
    ROOT / "src" / "chanta_core" / "cli" / "main.py",
)


def _assert_clean_lobby(result: lobby.V0438StartLobbyRenderResult) -> None:
    assert result.contains_schumpeter_brand is True
    assert result.contains_internal_lineage_default is False
    assert result.contains_chantagrowthkernel is False
    assert result.contains_legacy_schumpeter is False
    assert result.contains_raw_debug_metadata is False
    assert result.contains_raw_safety_footer is False
    assert result.contains_provider_secret is False
    assert result.contains_base_url is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False
    assert lobby.check_v0438_forbidden_brand_leaks(result.rendered_text).passed is True
    assert lobby.check_v0438_forbidden_metadata_leaks(result.rendered_text).passed is True


def _case(case_id: str) -> lobby.V0438StartLobbyGoldenTranscriptResult:
    cases = {
        "full": lobby.create_v0438_start_lobby_golden_transcript_case(
            "full",
            width=120,
            expected_contains=(
                "Schumpeter",
                "Process Intelligence-native Work Agent",
                "Ask anything",
                "오늘 작업을 요약해줘",
                "default-personal",
                "Work Session",
                "/help",
                "/status",
                "/exit",
                "PI",
                "Provider",
                "Trace",
                "Evidence",
                "Safety",
                "v0.43.8",
            ),
        ),
        "compact": lobby.create_v0438_start_lobby_golden_transcript_case(
            "compact",
            width=70,
            expected_contains=("Schumpeter", "PI-native Work Agent", "Ask anything", "Profile", "Provider", "Mode", "/help", "/status", "/exit", "PI=", "Provider=", "Trace=", "Safety="),
        ),
        "plain": lobby.create_v0438_start_lobby_golden_transcript_case(
            "plain",
            render_mode="plain",
            width=120,
            force_plain=True,
            expected_contains=("Schumpeter", "Process Intelligence-native Work Agent", "Ask anything", "default-personal", "Business Work Session", "PI=", "Provider=", "Trace=", "Evidence=", "Safety="),
        ),
        "no_logo": lobby.create_v0438_start_lobby_golden_transcript_case(
            "no-logo",
            render_mode="no_logo",
            width=120,
            force_no_logo=True,
            expected_contains=("Schumpeter", "Ask anything", "/help", "/status", "/exit"),
        ),
    }
    return lobby.execute_v0438_start_lobby_golden_transcript_case(cases[case_id])


def test_v0438_product_brand_policy_sets_schumpeter_as_default_ui_name():
    policy = lobby.create_v0438_product_brand_policy()
    assert policy.product_name == "Schumpeter"
    assert policy.default_ui_name == "Schumpeter"
    assert policy.internal_lineage_name == "ChantaCore"
    assert policy.cli_compatibility_name == "chanta-cli"
    assert policy.default_ui_mentions_internal_lineage is False
    assert policy.about_may_mention_internal_lineage is True
    assert policy.production_certified is False


def test_v0438_rebrand_boundary_policy_keeps_package_cli_module_profile_trace_rename_closed():
    policy = lobby.create_v0438_rebrand_boundary_policy()
    assert policy.ui_rebrand_enabled is True
    assert policy.package_rename_allowed is False
    assert policy.cli_rename_allowed is False
    assert policy.module_rename_allowed is False
    assert policy.profile_path_rename_allowed is False
    assert policy.trace_path_rename_allowed is False
    assert policy.compatibility_preserved is True


def test_v0438_legacy_name_deprecation_policy_hides_legacy_schumpeter_and_chantagrowthkernel_from_default_ui():
    policy = lobby.create_v0438_legacy_name_deprecation_policy()
    assert policy.legacy_schumpeter_is_current_runtime is False
    assert policy.legacy_schumpeter_default_ui_visible is False
    assert "stoploss-agent" in policy.legacy_schumpeter_target
    assert policy.chantagrowthkernel_active_dependency is False
    assert policy.chantagrowthkernel_default_ui_visible is False


def test_v0438_terminal_capability_profile_selects_full_compact_plain_and_no_logo_modes():
    assert lobby.create_v0438_terminal_capability_profile(width=120).recommended_render_mode == "full"
    assert lobby.create_v0438_terminal_capability_profile(width=70).recommended_render_mode == "compact"
    assert lobby.create_v0438_terminal_capability_profile(width=120, force_plain=True).recommended_render_mode == "plain"
    assert lobby.create_v0438_terminal_capability_profile(width=120, force_no_logo=True).recommended_render_mode == "no_logo"


def test_v0438_layout_policy_shows_lobby_elements_and_hides_debug_metadata():
    policy = lobby.create_v0438_start_lobby_layout_policy()
    assert policy.center_logo is True
    assert policy.show_product_name is True
    assert policy.show_input_card is True
    assert policy.show_profile_provider_mode_row is True
    assert policy.show_pi_status_bar is True
    assert policy.show_debug_metadata_by_default is False
    assert policy.show_raw_safety_footer_by_default is False
    assert policy.show_internal_lineage_by_default is False


def test_v0438_status_tokens_declared_for_pi_provider_trace_evidence_safety():
    names = {token.name for token in lobby.create_v0438_start_lobby_status_bar().tokens}
    assert names == {"PI", "Provider", "Trace", "Evidence", "Safety"}


def test_v0438_status_bar_contains_compact_pi_provider_trace_evidence_safety():
    bar = lobby.create_v0438_start_lobby_status_bar()
    for expected in ("PI", "Provider", "Trace", "Evidence", "Safety", "v0.43.8"):
        assert expected in bar.rendered_text


def test_v0438_status_bar_does_not_invoke_provider_prompt_shell_repo_workspace_or_memory():
    bar = lobby.create_v0438_start_lobby_status_bar()
    assert bar.contains_raw_debug_metadata is False
    assert bar.contains_raw_safety_footer is False
    assert bar.provider_invoked is False
    assert bar.prompt_submitted is False
    assert bar.shell_executed is False
    assert bar.repo_search_used is False
    assert bar.workspace_read_opened is False
    assert bar.production_certified is False


def test_v0438_default_start_lobby_contains_schumpeter_brand_and_business_work_session():
    result = lobby.render_v0438_start_lobby(width=120)
    _assert_clean_lobby(result)
    assert "Schumpeter" in result.rendered_text
    assert "Work Session" in result.rendered_text


def test_v0438_default_start_lobby_contains_command_hints():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    assert "/help" in text
    assert "/status" in text
    assert "/exit" in text


def test_v0438_default_start_lobby_contains_pi_status_bar():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    for expected in ("PI", "Provider", "Trace", "Evidence", "Safety"):
        assert expected in text


def test_v0438_default_start_lobby_hides_chantacore_lineage_by_default():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    assert "Internal implementation lineage" not in text
    assert "ChantaCore legacy core" not in text


def test_v0438_default_start_lobby_hides_chantagrowthkernel_and_legacy_schumpeter():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    assert lobby.check_v0438_forbidden_brand_leaks(text).passed is True


def test_v0438_default_start_lobby_hides_closed_track_raw_safety_and_debug_metadata():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    for forbidden in ("Closed in this track", "safety:", "shell=false", "production_certified=false", "grounding:", "source:"):
        assert forbidden not in text


def test_v0438_default_start_lobby_hides_provider_base_url_secrets_and_raw_config_paths():
    text = lobby.render_v0438_start_lobby(width=120).rendered_text
    assert "base_url=" not in text
    assert "api_key" not in text
    assert "secret" not in text.lower()
    assert ".chantacore" not in text.lower()


def test_v0438_compact_lobby_renders_under_narrow_width():
    result = lobby.render_v0438_start_lobby(width=70)
    _assert_clean_lobby(result)
    assert result.render_mode == "compact"
    assert "Profile:" in result.rendered_text
    assert "PI=" in result.rendered_text


def test_v0438_plain_lobby_has_no_unicode_box_dependency():
    result = lobby.render_v0438_start_lobby(width=120, force_plain=True)
    _assert_clean_lobby(result)
    assert result.render_mode == "plain"
    assert "╭" not in result.rendered_text
    assert "─" not in result.rendered_text
    assert "PI=" in result.rendered_text


def test_v0438_no_logo_lobby_disables_large_logo_but_keeps_brand_and_hints():
    result = lobby.render_v0438_start_lobby(width=120, force_no_logo=True)
    _assert_clean_lobby(result)
    assert result.render_mode == "no_logo"
    assert "Schumpeter" in result.rendered_text
    assert "/help" in result.rendered_text


def test_v0438_about_default_explains_schumpeter_and_chantacore_lineage_cleanly():
    about = lobby.render_v0438_about_card()
    assert "Schumpeter" in about.rendered_text
    assert "Process Intelligence-native Work Agent" in about.rendered_text
    assert "internal implementation lineage: ChantaCore" in about.rendered_text
    assert "CLI compatibility: chanta-cli" in about.rendered_text
    assert about.production_certified is False


def test_v0438_about_default_does_not_show_legacy_or_growthkernel_history_by_default():
    about = lobby.render_v0438_about_card()
    assert about.contains_legacy_history_default is False
    assert about.contains_chantagrowthkernel_default is False
    assert "legacy Schumpeter" not in about.rendered_text
    assert "ChantaGrowthKernel" not in about.rendered_text


def test_v0438_about_debug_may_show_lineage_but_not_secrets_or_production_certification():
    about = lobby.render_v0438_about_card_debug()
    assert "version: v0.43.8" in about.rendered_text
    assert "chanta_core.personal_runtime" in about.rendered_text
    assert about.contains_secret is False
    assert "production_certified=True" not in about.rendered_text
    assert about.production_certified is False


def test_v0438_noisy_output_guard_flags_forbidden_brand_leaks():
    check = lobby.check_v0438_forbidden_brand_leaks("ChantaGrowthKernel and legacy Schumpeter")
    assert check.passed is False
    assert "ChantaGrowthKernel" in check.forbidden_found
    assert "legacy Schumpeter" in check.forbidden_found


def test_v0438_noisy_output_guard_flags_forbidden_metadata_leaks():
    check = lobby.check_v0438_forbidden_metadata_leaks("safety: shell=false base_url=http://example")
    assert check.passed is False
    assert "safety:" in check.forbidden_found
    assert "shell=false" in check.forbidden_found
    assert "base_url=" in check.forbidden_found


def test_v0438_start_lobby_golden_default_full_passes():
    assert _case("full").passed is True


def test_v0438_start_lobby_golden_compact_passes():
    assert _case("compact").passed is True


def test_v0438_start_lobby_golden_plain_passes():
    result = _case("plain")
    assert result.passed is True
    assert "╭" not in result.rendered_text


def test_v0438_start_lobby_golden_no_logo_passes():
    assert _case("no_logo").passed is True


def test_v0438_about_golden_default_passes():
    about = lobby.render_v0438_about_card()
    assert about.contains_schumpeter_brand is True
    assert about.contains_internal_lineage is True
    assert about.contains_raw_safety_footer is False
    assert about.contains_secret is False


def test_v0438_about_golden_debug_passes():
    about = lobby.render_v0438_about_card_debug()
    assert about.debug is True
    assert "version: v0.43.8" in about.rendered_text
    assert about.contains_secret is False
    assert about.production_certified is False


def test_v0438_status_detail_separation_passes():
    start = lobby.render_v0438_start_lobby(width=120).rendered_text
    status = lobby.render_v0438_status_detail()
    assert "PI: ok - process evidence surfaces are available." not in start
    assert "PI: ok - process evidence surfaces are available." in status
    assert "Safety:" in status


def test_v0438_v044_gate_recheck_requires_v0437_and_v0438_acceptance():
    assert lobby.create_v0438_v044_gate_recheck().ready_for_v044_design is True
    assert lobby.create_v0438_v044_gate_recheck(v0437_golden_transcripts_passed=False).ready_for_v044_design is False


def test_v0438_v044_gate_recheck_fails_if_start_lobby_noisy():
    assert lobby.create_v0438_v044_gate_recheck(start_lobby_clean=False).ready_for_v044_design is False


def test_v0438_v044_gate_recheck_fails_if_legacy_names_visible_by_default():
    assert lobby.create_v0438_v044_gate_recheck(default_ui_legacy_names_hidden=False).ready_for_v044_design is False


def test_v0438_readiness_report_sets_brand_lobby_status_about_guard_flags_true():
    report = lobby.create_v0438_readiness_report()
    assert report.schumpeter_brand_policy_ready is True
    assert report.rebrand_boundary_policy_ready is True
    assert report.start_lobby_renderer_ready is True
    assert report.pi_status_bar_ready is True
    assert report.about_card_ready is True
    assert report.noisy_output_guard_ready is True
    assert report.start_lobby_golden_transcripts_ready is True
    assert report.v044_gate_recheck_ready is True


def test_v0438_readiness_report_keeps_workspace_read_file_repo_shell_git_edit_tools_functions_subagent_memory_core_cli_package_rename_and_production_false():
    report = lobby.create_v0438_readiness_report()
    assert report.ready_for_workspace_read is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_workspace_search is False
    assert report.ready_for_git_status_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.ready_for_cli_rename is False
    assert report.ready_for_package_rename is False
    assert report.production_certified is False


def test_v0438_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in lobby.REQUIRED_V0438_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0438_integrated_document_contains_schumpeter_rebrand_policy_start_lobby_golden_transcripts_and_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Schumpeter product branding" in text
    assert "Start Lobby UI Contract" in text
    assert "Golden Start Lobby Acceptance" in text
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text


def test_v0438_no_separate_v0438_brand_lobby_about_docs_created():
    docs = sorted((ROOT / "docs" / "versions" / "v0.43").glob("*v0.43.8*"))
    assert docs == [DOC_PATH]


def test_v0438_no_forbidden_runtime_call_patterns():
    forbidden = (
        "subprocess",
        "shell=True",
        "os.system",
        "eval(",
        "exec(",
        "apply_patch",
        "git apply",
        "git worktree",
        "invoke_subagent",
        "run_subagent",
        "create_child_session",
        "spawn_agent",
        "os.walk",
        "Path.rglob",
        ".rglob(",
        "glob(",
    )
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text, f"{pattern} found in {path}"


def test_v0438_no_repo_scan_shell_git_workspace_read_or_provider_completion_in_lobby():
    text = (ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_schumpeter_lobby.py").read_text(encoding="utf-8")
    for pattern in ("repo scan", "arbitrary path read", "provider completion", "workspace_read_opened=True"):
        assert pattern not in text
    result = lobby.render_v0438_start_lobby(width=120)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.repo_search_used is False
    assert result.workspace_read_opened is False


def test_v0438_work_session_start_uses_schumpeter_lobby_and_about_status_commands(tmp_path):
    result = work.start_v043_work_session(work.create_v043_work_session_start_request(home_path=str(tmp_path), provider="mock"))
    assert "Schumpeter" in result.rendered_text
    assert "Closed in this track" not in result.rendered_text
    state = result.state
    about = work.execute_v043_work_session_input("/about", state)
    status = work.execute_v043_work_session_input("/status", state)
    assert "internal implementation lineage: ChantaCore" in about.rendered_text
    assert "Schumpeter status" in status.rendered_text


def test_v0438_work_session_v044_readiness_mentions_v0437_and_v0438_gates(tmp_path):
    state = work.start_v043_work_session(work.create_v043_work_session_start_request(home_path=str(tmp_path))).state
    result = work.execute_v043_work_session_input("/v044 readiness", state)
    assert "v0.43.7 UX repair gate" in result.rendered_text
    assert "v0.43.8 start lobby gate" in result.rendered_text
    assert "Controlled Workspace Read Design & Scope Contract" in result.rendered_text
    assert "workspace read remains closed in v0.43.8" in result.rendered_text
