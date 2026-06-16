from __future__ import annotations

from pathlib import Path

from chanta_core.personal_runtime import default_personal_final_ux_acceptance as v04210


def test_v04210_acceptance_status_values_declared() -> None:
    assert {item.value for item in v04210.V04210AcceptanceStatus} == {
        "pass",
        "pass_with_notes",
        "warning",
        "fail",
        "not_tested",
        "blocked",
        "unknown",
    }
    assert {item.value for item in v04210.V04210AcceptanceSeverity} == {"low", "medium", "high", "blocker", "unknown"}


def test_v04210_acceptance_areas_declared() -> None:
    assert {item.value for item in v04210.V04210AcceptanceArea} >= {
        "default_run_output",
        "debug_run_output",
        "configured_provider",
        "mock_provider",
        "chat_output",
        "provider_status",
        "command_guide",
        "runtime_identity",
        "empty_response",
        "diagnostics",
        "process_intelligence_review",
        "safety_boundary",
        "unknown",
    }


def test_v04210_manual_acceptance_scenarios_cover_configured_mock_run_debug_chat_provider_commands_report_empty_identity_safety() -> None:
    scenarios = v04210.create_v04210_manual_acceptance_scenarios()
    ids = {scenario.scenario_id for scenario in scenarios}
    assert {
        "configured-provider-default-run",
        "configured-provider-debug-run",
        "mock-provider-default-run",
        "chat-configured-provider",
        "chat-mock-provider",
        "provider-status-connectivity",
        "command-guide",
        "report-bundle-copy-paste",
        "empty-response-handling",
        "runtime-identity-answer",
        "safety-boundary-check",
    } <= ids


def test_v04210_configured_provider_acceptance_requires_connectivity_actual_completion_identity_and_empty_response_safety() -> None:
    acceptance = v04210.create_v04210_configured_provider_acceptance(live_tested=True)
    assert acceptance.provider_config_required is True
    assert acceptance.connectivity_required is True
    assert acceptance.actual_completion_required is True
    assert acceptance.default_output_clean_required is True
    assert acceptance.runtime_identity_required is True
    assert acceptance.empty_response_must_not_complete_success is True
    assert acceptance.debug_output_available_required is True


def test_v04210_configured_provider_acceptance_not_full_pass_when_live_not_tested() -> None:
    acceptance = v04210.create_v04210_configured_provider_acceptance(live_tested=False)
    assert acceptance.status in {"not_tested", "pass_with_notes"}
    assert acceptance.status != "pass"
    assert acceptance.blocks_v043 is True


def test_v04210_mock_provider_acceptance_requires_run_chat_no_duplicate_and_debug() -> None:
    acceptance = v04210.create_v04210_mock_provider_acceptance()
    assert acceptance.mock_run_required is True
    assert acceptance.mock_chat_required is True
    assert acceptance.duplicate_output_absent_required is True
    assert acceptance.debug_available_required is True
    assert acceptance.status == "pass"


def test_v04210_run_ux_acceptance_requires_clean_default_and_debug_details() -> None:
    acceptance = v04210.create_v04210_run_ux_acceptance()
    assert acceptance.default_output_hides_raw_trace is True
    assert acceptance.default_output_shows_assistant_response is True
    assert acceptance.compact_footer_ok is True
    assert acceptance.debug_output_exposes_details is True
    assert acceptance.json_output_preserved is True
    assert acceptance.blocking_findings == ()


def test_v04210_debug_ux_acceptance_requires_run_session_provider_parse_and_safety_fields() -> None:
    acceptance = v04210.create_v04210_debug_ux_acceptance()
    assert acceptance.debug_flag_supported is True
    assert acceptance.run_id_visible is True
    assert acceptance.session_id_visible is True
    assert acceptance.provider_visible is True
    assert acceptance.parse_status_visible is True
    assert acceptance.safety_flags_visible is True


def test_v04210_chat_ux_acceptance_requires_clean_banner_grouped_help_status_provider_no_duplicate_and_safe_internal_commands() -> None:
    acceptance = v04210.create_v04210_chat_ux_acceptance()
    assert acceptance.clean_banner is True
    assert acceptance.grouped_help is True
    assert acceptance.readable_status is True
    assert acceptance.readable_provider_view is True
    assert acceptance.no_duplicate_response is True
    assert acceptance.internal_commands_safe is True


def test_v04210_provider_ux_acceptance_requires_readable_status_connectivity_next_action_secret_hiding() -> None:
    acceptance = v04210.create_v04210_provider_ux_acceptance()
    assert acceptance.status_readable is True
    assert acceptance.connectivity_readable is True
    assert acceptance.next_action_clear is True
    assert acceptance.secrets_hidden is True
    assert acceptance.mock_and_configured_readiness_clear is True


def test_v04210_command_guide_acceptance_requires_start_talk_provider_review_skills_diagnostics_safety_sections() -> None:
    acceptance = v04210.create_v04210_command_guide_acceptance()
    assert acceptance.guide_command_available is True
    assert set(acceptance.sections_present) >= {"Start", "Talk", "Provider", "Review", "Skills", "Diagnostics", "Safety"}
    assert acceptance.hides_internal_artifact_names is True
    assert acceptance.business_user_friendly is True


def test_v04210_runtime_identity_acceptance_disallows_base_model_identity_as_primary() -> None:
    acceptance = v04210.create_v04210_runtime_identity_acceptance()
    assert acceptance.base_model_identity_primary_allowed is False
    assert acceptance.business_agent_positioning is True
    assert "ChantaCore default-personal" in acceptance.primary_identity
    assert "provider" in acceptance.provider_identity_treatment


def test_v04210_empty_response_acceptance_disallows_completed_success() -> None:
    acceptance = v04210.create_v04210_empty_response_acceptance()
    assert acceptance.empty_response_must_fail_or_completed_empty is True
    assert acceptance.empty_response_completed_success_allowed is False
    assert acceptance.plain_language_guidance_required is True
    assert acceptance.run_report_parse_fields_required is True


def test_v04210_diagnostic_acceptance_requires_report_bundle_copy_paste_redaction_and_context() -> None:
    acceptance = v04210.create_v04210_diagnostic_acceptance()
    assert acceptance.report_bundle_available is True
    assert acceptance.copy_paste_available is True
    assert acceptance.redaction_required is True
    assert acceptance.includes_provider_run_trace_feedback_safety is True


def test_v04210_pi_review_availability_acceptance_requires_trace_run_report_history_feedback_and_process_evidence() -> None:
    acceptance = v04210.create_v04210_pi_review_availability_acceptance()
    assert acceptance.trace_timeline_available is True
    assert acceptance.run_report_available is True
    assert acceptance.run_history_available is True
    assert acceptance.report_bundle_available is True
    assert acceptance.feedback_available is True
    assert acceptance.process_evidence_preserved is True


def test_v04210_safety_boundary_acceptance_keeps_high_risk_closed_and_production_false() -> None:
    acceptance = v04210.create_v04210_safety_boundary_acceptance()
    assert acceptance.provider_doctor_completion_closed is True
    assert acceptance.provider_tool_calling_closed is True
    assert acceptance.function_calling_closed is True
    assert acceptance.shell_execution_closed is True
    assert acceptance.file_edit_closed is True
    assert acceptance.patch_apply_closed is True
    assert acceptance.arbitrary_file_read_closed is True
    assert acceptance.broad_scan_closed is True
    assert acceptance.repo_search_closed is True
    assert acceptance.subagent_closed is True
    assert acceptance.general_agent_loop_closed is True
    assert acceptance.dominion_closed is True
    assert acceptance.production_certified is False


def test_v04210_final_acceptance_report_sets_ready_for_v043_only_without_blockers() -> None:
    blocked = v04210.create_v04210_final_ux_acceptance_report(configured_live_tested=False)
    assert blocked.ready_for_v043 is False
    assert blocked.blocker_count >= 1
    ready = v04210.create_v04210_final_ux_acceptance_report(configured_live_tested=True)
    assert ready.ready_for_v043 is True
    assert ready.blocker_count == 0
    assert ready.production_certified is False


def test_v04210_pilot_gate_decision_can_choose_v043_or_v04211_based_on_findings() -> None:
    ready = v04210.create_v04210_pilot_gate_decision(v04210.create_v04210_final_ux_acceptance_report(configured_live_tested=True))
    assert ready.decision == "proceed_to_v043"
    assert ready.ready_for_v043 is True

    finding = v04210.create_v04210_final_ux_finding(deferred_to_v04211=True, blocks_v043=True)
    continue_report = v04210.create_v04210_final_ux_acceptance_report(
        configured_live_tested=True,
        findings=(finding,),
    )
    decision = v04210.create_v04210_pilot_gate_decision(continue_report)
    assert decision.decision in {"continue_v04211", "blocked"}
    assert decision.ready_for_v043 is False


def test_v04210_readiness_report_sets_acceptance_flags_true() -> None:
    report = v04210.create_v04210_readiness_report()
    assert report.final_business_ux_acceptance_ready is True
    assert report.configured_provider_acceptance_defined is True
    assert report.mock_provider_acceptance_defined is True
    assert report.run_ux_acceptance_ready is True
    assert report.chat_ux_acceptance_ready is True
    assert report.provider_ux_acceptance_ready is True
    assert report.command_guide_acceptance_ready is True
    assert report.runtime_identity_acceptance_ready is True
    assert report.empty_response_acceptance_ready is True
    assert report.diagnostic_acceptance_ready is True
    assert report.pi_review_availability_ready is True
    assert report.safety_boundary_acceptance_ready is True


def test_v04210_readiness_report_keeps_tools_functions_shell_subagent_agentloop_and_production_false() -> None:
    report = v04210.create_v04210_readiness_report()
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_dominion_runtime is False
    assert report.production_certified is False


def test_v04210_integrated_document_exists_and_has_required_sections() -> None:
    path = Path(v04210.INTEGRATED_DOC_PATH)
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for section in v04210.REQUIRED_V04210_DOC_SECTIONS:
        assert f"## {section}" in text


def test_v04210_integrated_document_contains_v04211_or_v043_decision_guidance_and_copy_paste_restore_prompt() -> None:
    text = Path(v04210.INTEGRATED_DOC_PATH).read_text(encoding="utf-8")
    assert "proceed to v0.43" in text.lower()
    assert "v0.42.11" in text
    assert "Copy-Paste Restore Prompt" in text


def test_v04210_no_separate_v04210_restore_acceptance_or_ux_documents_created() -> None:
    forbidden = (
        Path("docs/versions/v0.42/v0.42.10_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.10_acceptance.md"),
        Path("docs/versions/v0.42/v0.42.10_business_ux.md"),
        Path("docs/versions/v0.42/v0.42.10_final_ux.md"),
    )
    assert not any(path.exists() for path in forbidden)


def test_v04210_no_forbidden_runtime_call_patterns() -> None:
    paths = (
        Path("src/chanta_core/personal_runtime/default_personal_final_ux_acceptance.py"),
        Path("src/chanta_core/personal_runtime/default_personal_business_ux.py"),
        Path("src/chanta_core/cli/main.py"),
    )
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
        "requests",
        "httpx",
        "socket",
    )
    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert not any(pattern in text for pattern in forbidden), path
