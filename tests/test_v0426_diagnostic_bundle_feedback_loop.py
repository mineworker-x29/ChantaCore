from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_diagnostics_feedback as v0426
from chanta_core.personal_runtime.default_personal_home_quickstart import run_v042_quickstart


FAKE_SECRET_NOTE = "Do not store this fake key OPENAI_API_KEY=sk-test-secret-value"


def _prepared_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    result = run_v042_quickstart(explicit_home=str(home), with_mock_run=True)
    assert result.exit_code == 0
    return home


def test_v0426_diagnostic_bundle_modes_declared() -> None:
    assert {item.value for item in v0426.V042DiagnosticBundleMode} == {"standard", "copy_paste", "markdown", "json", "brief", "unknown"}


def test_v0426_diagnostic_bundle_status_values_declared() -> None:
    assert {item.value for item in v0426.V042DiagnosticBundleStatus} == {"completed", "completed_with_warnings", "failed", "blocked", "skipped", "unknown"}


def test_v0426_diagnostic_bundle_source_kinds_declared() -> None:
    assert {item.value for item in v0426.V042DiagnosticBundleSourceKind} == {
        "version",
        "home_status",
        "profile_status",
        "provider_status",
        "provider_config_redacted",
        "last_run_report",
        "run_history",
        "trace_summary",
        "trace_timeline_summary",
        "session_show_last",
        "skill_list_summary",
        "skill_execution_summary",
        "denial_summary",
        "safety_count_summary",
        "feedback_summary",
        "latest_feedback_notes",
        "known_limitations",
        "closed_capability_snapshot",
        "v042_track_closure",
        "next_action",
        "unknown",
    }


def test_v0426_diagnostic_bundle_section_kinds_declared() -> None:
    assert {item.value for item in v0426.V042DiagnosticBundleSectionKind} == {
        "header",
        "environment",
        "runtime_status",
        "provider",
        "run",
        "trace",
        "session",
        "skills",
        "denials",
        "feedback",
        "safety",
        "limitations",
        "closed_capabilities",
        "process_intelligence_review",
        "next_steps",
        "copy_paste_handoff",
        "unknown",
    }


def test_v0426_diagnostic_bundle_formats_declared() -> None:
    assert {item.value for item in v0426.V042DiagnosticBundleFormat} == {"text", "markdown", "json", "compact_text", "unknown"}


def test_v0426_diagnostic_redaction_policy_redacts_secrets_tokens_env_values_and_preserves_safe_context() -> None:
    policy = v0426.create_v042_diagnostic_redaction_policy()
    assert policy.redact_secrets is True
    assert policy.redact_api_keys is True
    assert policy.redact_tokens is True
    assert policy.redact_env_values is True
    assert policy.preserve_safe_path_context is True
    assert policy.replacement_text == "<redacted>"
    redacted, changed = v0426._redact_text(FAKE_SECRET_NOTE)
    assert changed is True
    assert "sk-test-secret-value" not in redacted
    assert "<redacted>" in redacted


def test_v0426_diagnostic_bundle_request_has_bounded_limits_and_no_file_write_by_default() -> None:
    request = v0426.create_v042_diagnostic_bundle_request(max_runs=9999, max_trace_items=9999, max_feedback_items=9999)
    assert request.max_runs == 100
    assert request.max_trace_items == 200
    assert request.max_feedback_items == 100
    assert request.home_path is None
    result = v0426.create_v042_diagnostic_safety_report()
    assert result.report_bundle_writes_files_by_default is False


def test_v0426_diagnostic_bundle_sources_never_invoke_provider_submit_prompt_shell_subagent_or_production(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    sources = v0426.collect_v042_diagnostic_bundle_sources(v0426.create_v042_diagnostic_bundle_request(home_path=str(home)))
    assert {source.source_kind for source in sources} >= {
        "version",
        "home_status",
        "profile_status",
        "provider_status",
        "provider_config_redacted",
        "last_run_report",
        "run_history",
        "trace_summary",
        "trace_timeline_summary",
        "session_show_last",
        "skill_list_summary",
        "skill_execution_summary",
        "denial_summary",
        "safety_count_summary",
        "feedback_summary",
        "latest_feedback_notes",
        "known_limitations",
        "closed_capability_snapshot",
        "v042_track_closure",
        "next_action",
    }
    for source in sources:
        assert source.provider_invoked is False
        assert source.prompt_submitted is False
        assert source.shell_executed is False
        assert source.subagent_invoked is False
        assert source.production_certified is False


def test_v0426_diagnostic_bundle_sections_include_process_intelligence_relevance(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0426.create_v042_diagnostic_bundle_result(v0426.create_v042_diagnostic_bundle_request(home_path=str(home)))
    assert result.sections
    assert all(section.process_intelligence_relevance for section in result.sections)


def test_v0426_diagnostic_bundle_result_contains_required_sources_and_no_provider_prompt_shell_or_file_write(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0426.create_v042_diagnostic_bundle_result(v0426.create_v042_diagnostic_bundle_request(home_path=str(home)))
    assert result.status == "completed"
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.filesystem_written is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False
    source_kinds = {source.source_kind for source in result.sources}
    assert "feedback_summary" in source_kinds
    assert "closed_capability_snapshot" in source_kinds


def test_v0426_copy_paste_text_contains_debug_context_no_secrets_and_is_bounded(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    v0426.append_v042_feedback_note(v0426.create_v042_feedback_note_request(FAKE_SECRET_NOTE, home_path=str(home), category="safety", severity="high"))
    result = v0426.create_v042_diagnostic_bundle_result(v0426.create_v042_diagnostic_bundle_request(home_path=str(home), copy_paste=True))
    assert "ChantaCore" in result.copy_paste_text
    assert "sk-test-secret-value" not in result.copy_paste_text
    assert result.pi_review_packet.evidence_handoff_ready is True
    copy = v0426.create_v042_diagnostic_copy_paste_text(result.sections)
    assert copy.includes_secret_values is False
    assert copy.includes_required_debug_context is True
    assert copy.suitable_for_gpt_or_codex is True
    assert copy.max_length_bounded is True


def test_v0426_diagnostic_safety_report_keeps_provider_prompt_file_write_shell_subagent_arbitrary_read_scan_upload_and_production_false() -> None:
    report = v0426.create_v042_diagnostic_safety_report()
    assert report.report_bundle_calls_provider is False
    assert report.report_bundle_submits_prompt is False
    assert report.report_bundle_writes_files_by_default is False
    assert report.report_bundle_executes_shell is False
    assert report.report_bundle_invokes_subagent is False
    assert report.report_bundle_reads_arbitrary_paths is False
    assert report.report_bundle_scans_filesystem is False
    assert report.report_bundle_uploads_external is False
    assert report.secrets_redacted is True
    assert report.production_certified is False


def test_v0426_diagnostic_pi_review_packet_contains_run_provider_denial_skill_feedback_and_safety_context(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0426.create_v042_diagnostic_bundle_result(v0426.create_v042_diagnostic_bundle_request(home_path=str(home)))
    packet = result.pi_review_packet
    assert packet.run_count_summary
    assert packet.provider_count_summary
    assert packet.denial_summary
    assert packet.skill_summary
    assert packet.feedback_summary
    assert packet.safety_summary
    assert packet.process_instance_review_ready is True
    assert packet.evidence_handoff_ready is True
    assert packet.high_risk_counts_zero is True


def test_v0426_feedback_categories_declared() -> None:
    assert {item.value for item in v0426.V042FeedbackCategory} == {"ux", "bug", "provider", "trace", "skill", "safety", "process_intelligence", "docs", "performance", "idea", "unknown"}


def test_v0426_feedback_severities_declared() -> None:
    assert {item.value for item in v0426.V042FeedbackSeverity} == {"low", "medium", "high", "blocker", "unknown"}


def test_v0426_feedback_status_values_declared() -> None:
    assert {item.value for item in v0426.V042FeedbackStatus} == {"recorded", "redacted", "rejected", "listed", "summarized", "failed", "unknown"}


def test_v0426_feedback_redaction_policy_redacts_secret_like_values_before_persistence() -> None:
    policy = v0426.create_v042_feedback_redaction_policy()
    assert policy.redact_secret_like_values_before_persistence is True
    assert policy.replacement_text == "<redacted>"
    assert "sk-test-secret-value" not in v0426.redact_v042_feedback_note_text(FAKE_SECRET_NOTE, policy)


def test_v0426_feedback_store_policy_is_bounded_append_only_and_does_not_write_core_memory_profile_provider_session_or_workspace() -> None:
    policy = v0426.create_v042_feedback_store_policy()
    assert policy.relative_store_path == "profiles/default-personal/state/feedback/feedback.jsonl"
    assert policy.bounded_to_home is True
    assert policy.append_only is True
    assert policy.writes_core_memory is False
    assert policy.writes_profile_config is False
    assert policy.writes_provider_config is False
    assert policy.writes_session_store is False
    assert policy.writes_workspace is False
    assert policy.stores_secret_values is False


def test_v0426_feedback_note_record_persists_redacted_text_and_no_raw_secret_values() -> None:
    record = v0426.create_v042_feedback_note_record(v0426.create_v042_feedback_note_request(FAKE_SECRET_NOTE, category="safety", severity="high"))
    assert "sk-test-secret-value" not in record.note_text_redacted
    assert record.raw_secret_value_persisted is False
    assert record.provider_invoked is False
    assert record.prompt_submitted is False
    assert record.shell_executed is False
    assert record.subagent_invoked is False
    assert record.production_certified is False


def test_v0426_feedback_append_result_writes_only_bounded_feedback_store_and_no_outside_home_paths(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    result = v0426.append_v042_feedback_note(v0426.create_v042_feedback_note_request("provider setup UX is clear", home_path=str(home), category="ux"))
    assert result.appended is True
    assert result.rejected is False
    assert result.outside_home_paths == ()
    assert result.overwritten_files == ()
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False
    assert str(home) in result.store_path
    assert Path(result.store_path).exists()


def test_v0426_feedback_list_result_is_read_only(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    v0426.append_v042_feedback_note(v0426.create_v042_feedback_note_request("note", home_path=str(home), category="ux"))
    result = v0426.create_v042_feedback_list_result(v0426.create_v042_feedback_list_request(home_path=str(home)))
    assert result.count == 1
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.filesystem_written is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False


def test_v0426_feedback_show_last_result_is_read_only(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    v0426.append_v042_feedback_note(v0426.create_v042_feedback_note_request("note", home_path=str(home), category="ux"))
    result = v0426.create_v042_feedback_show_result(v0426.create_v042_feedback_show_request(home_path=str(home)))
    assert result.found is True
    assert result.filesystem_written is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False


def test_v0426_feedback_summary_counts_category_severity_pi_and_safety_feedback(tmp_path: Path) -> None:
    home = _prepared_home(tmp_path)
    v0426.append_v042_feedback_note(v0426.create_v042_feedback_note_request("pi note", home_path=str(home), category="process_intelligence", severity="medium"))
    v0426.append_v042_feedback_note(v0426.create_v042_feedback_note_request("safety note", home_path=str(home), category="safety", severity="high"))
    summary = v0426.create_v042_feedback_list_summary(str(home))
    assert summary.total_feedback_count == 2
    assert summary.by_category["process_intelligence"] == 1
    assert summary.by_category["safety"] == 1
    assert summary.high_count == 1
    assert summary.process_intelligence_feedback_count == 1
    assert summary.safety_feedback_count == 1


def test_v0426_feedback_loop_safety_report_keeps_provider_prompt_shell_subagent_memory_workspace_and_production_false() -> None:
    report = v0426.create_v042_feedback_loop_safety_report()
    assert report.feedback_writes_bounded_store is True
    assert report.feedback_writes_core_memory is False
    assert report.feedback_writes_profile_config is False
    assert report.feedback_writes_provider_config is False
    assert report.feedback_writes_session_store is False
    assert report.feedback_writes_workspace is False
    assert report.feedback_calls_provider is False
    assert report.feedback_submits_prompt is False
    assert report.feedback_executes_shell is False
    assert report.feedback_invokes_subagent is False
    assert report.feedback_stores_secret_values is False
    assert report.production_certified is False


def test_v0426_known_limitations_include_provider_manual_setup_prod_false_agentloop_closed_shell_closed_feedback_not_issue_fixing_and_bundle_not_upload() -> None:
    text = "\n".join(item.title + " " + item.description for item in v0426.build_v042_known_limitations())
    assert "manual environment setup" in text
    assert "Production certification remains false" in text
    assert "General AgentLoop remains closed" in text
    assert "Shell/edit/apply/subagent remain closed" in text
    assert "Broad filesystem/repo search remains closed" in text
    assert "not automatic issue fixing" in text
    assert "not external upload" in text
    assert "not production release" in text


def test_v0426_closed_capability_snapshot_keeps_all_high_risk_capabilities_closed() -> None:
    snapshot = v0426.create_v042_closed_capability_snapshot()
    assert snapshot.shell_execution_closed is True
    assert snapshot.file_edit_closed is True
    assert snapshot.patch_apply_closed is True
    assert snapshot.arbitrary_file_read_closed is True
    assert snapshot.broad_scan_closed is True
    assert snapshot.provider_tool_calling_closed is True
    assert snapshot.function_calling_closed is True
    assert snapshot.provider_doctor_completion_closed is True
    assert snapshot.subagent_closed is True
    assert snapshot.general_agent_loop_closed is True
    assert snapshot.autonomous_loop_closed is True
    assert snapshot.memory_mutation_closed is True
    assert snapshot.dominion_closed is True
    assert snapshot.production_certified is False


def test_v0426_ux_hardening_track_closure_assessment_marks_v043_user_operation_pilot_ready_but_production_false() -> None:
    assessment = v0426.create_v042_ux_hardening_track_closure_assessment()
    assert "Default Personal Runtime UX Hardening" in assessment.track_name
    assert "v0.42.6" in assessment.versions_completed
    assert assessment.user_operability_improved is True
    assert assessment.installable_runtime_baseline is True
    assert assessment.default_home_ready is True
    assert assessment.provider_setup_ux_ready is True
    assert assessment.trace_history_ux_ready is True
    assert assessment.manual_chat_ready is True
    assert assessment.bounded_skill_execution_ready is True
    assert assessment.diagnostic_bundle_ready is True
    assert assessment.feedback_loop_ready is True
    assert assessment.high_risk_capabilities_deferred is True
    assert assessment.ready_for_v043_user_operation_pilot is True
    assert assessment.production_certified is False


def test_v0426_readiness_report_sets_diagnostic_feedback_and_v043_handoff_flags_true() -> None:
    report = v0426.create_v0426_readiness_report()
    assert report.diagnostic_bundle_command_ready is True
    assert report.diagnostic_copy_paste_ready is True
    assert report.diagnostic_redaction_ready is True
    assert report.diagnostic_pi_review_packet_ready is True
    assert report.feedback_note_command_ready is True
    assert report.feedback_list_command_ready is True
    assert report.feedback_show_command_ready is True
    assert report.feedback_summary_command_ready is True
    assert report.feedback_store_ready is True
    assert report.feedback_redaction_ready is True
    assert report.known_limitations_ready is True
    assert report.closed_capability_snapshot_ready is True
    assert report.v042_track_closure_assessment_ready is True
    assert report.integrated_restore_document_ready is True
    assert report.v043_handoff_ready is True


def test_v0426_readiness_report_keeps_upload_network_issue_fix_shell_edit_patch_arbitrary_read_scan_repo_provider_tools_functions_agentloop_subagent_memory_and_production_flags_false() -> None:
    report = v0426.create_v0426_readiness_report()
    assert report.ready_for_external_upload is False
    assert report.ready_for_network_submission is False
    assert report.ready_for_automatic_issue_creation is False
    assert report.ready_for_automatic_code_fixing is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_broad_filesystem_scan is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_provider_doctor_completion is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_multi_step_agent_loop is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_child_session_creation is False
    assert report.ready_for_memory_write is False
    assert report.production_certified is False


def test_v0426_v043_handoff_targets_user_operation_pilot_and_process_intelligence_review_loop() -> None:
    handoff = v0426.create_v043_user_operation_pilot_handoff()
    assert handoff.target_version == "v0.43.0 User Operation Pilot & Process Intelligence Review Loop"
    assert any("diagnostic bundles" in item for item in handoff.recommended_focus)
    assert handoff.production_certified is False


def test_v0426_integrated_restore_snapshot_lists_open_and_closed_capabilities() -> None:
    snapshot = v0426.create_v0426_integrated_restore_context_snapshot()
    assert "report_bundle_command" in snapshot.open_capabilities
    assert "feedback_note_command" in snapshot.open_capabilities
    assert "external_upload" in snapshot.closed_capabilities
    assert "shell_execution" in snapshot.closed_capabilities
    assert "production_certification" in snapshot.closed_capabilities


def test_v0426_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = v0426.create_v0426_integrated_restore_packet()
    assert packet.single_integrated_doc_path == "docs/versions/v0.42/v0.42.6_diagnostic_bundle_feedback_loop_restore.md"


def test_v0426_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = v0426.create_v0426_integrated_restore_packet()
    assert packet.separate_restore_doc_created is False


def test_v0426_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = v0426.create_v0426_integrated_restore_document_manifest()
    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0426_integrated_document_exists_and_has_required_restore_sections() -> None:
    path = Path("docs/versions/v0.42/v0.42.6_diagnostic_bundle_feedback_loop_restore.md")
    assert path.exists()
    text = path.read_text(encoding="utf-8")
    for heading in [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Project Context for New Codex Session",
        "v0.41.6 User Test Baseline",
        "v0.42.0 UX Baseline Summary",
        "v0.42.1 Home / Quickstart Summary",
        "v0.42.2 Provider Setup Summary",
        "v0.42.3 Trace / Run History Summary",
        "v0.42.4 Chat Shell Summary",
        "v0.42.5 Skill Execution Summary",
        "Diagnostic Bundle Summary",
        "Diagnostic Bundle Contract",
        "Diagnostic Redaction Contract",
        "Diagnostic PI Review Packet",
        "Feedback Loop Summary",
        "Feedback Store Contract",
        "Feedback Redaction Contract",
        "Feedback Commands",
        "Known Limitations",
        "Closed Capability Snapshot",
        "v0.42 Track Closure Assessment",
        "Runtime Opening Status",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Expected Test Interpretation",
        "Withdrawal Conditions",
        "v0.43 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]:
        assert f"## {heading}" in text


def test_v0426_integrated_document_contains_report_feedback_examples_and_copy_paste_restore_prompt() -> None:
    text = Path("docs/versions/v0.42/v0.42.6_diagnostic_bundle_feedback_loop_restore.md").read_text(encoding="utf-8")
    assert "chanta-cli report bundle" in text
    assert "chanta-cli report bundle --copy-paste" in text
    assert "chanta-cli feedback note" in text
    assert "chanta-cli feedback show last" in text
    assert "You are continuing ChantaCore after v0.42.6." in text


def test_v0426_no_separate_v0426_restore_diagnostic_or_feedback_documents_created() -> None:
    forbidden = [
        "docs/versions/v0.42/v0.42.6_restore_document.md",
        "docs/versions/v0.42/v0.42.6_diagnostic_bundle.md",
        "docs/versions/v0.42/v0.42.6_feedback_loop.md",
        "docs/versions/v0.42/v0.42.6_report_bundle_user_guide.md",
    ]
    for path in forbidden:
        assert not Path(path).exists()


def test_v0426_no_forbidden_runtime_call_patterns_except_bounded_feedback_append_and_bounded_reads() -> None:
    combined = Path("src/chanta_core/personal_runtime/default_personal_diagnostics_feedback.py").read_text(encoding="utf-8")
    combined += "\n" + Path("src/chanta_core/cli/main.py").read_text(encoding="utf-8")
    for forbidden in [
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
        "invoke_subagent(",
        "run_subagent(",
        "create_child_session(",
        "spawn_agent(",
        "pytest",
        "unittest",
        "requests",
        "httpx",
        "socket",
    ]:
        assert forbidden not in combined


def test_v0426_cli_feedback_note_then_list_show_summary_and_bundle_redacts_fake_secret(tmp_path: Path, monkeypatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["feedback", "note", "trace timeline is readable", "--category", "process_intelligence", "--severity", "medium"]) == 0
    assert cli_main(["feedback", "list"]) == 0
    assert cli_main(["feedback", "show", "last"]) == 0
    assert cli_main(["feedback", "summary"]) == 0
    assert cli_main(["feedback", "note", FAKE_SECRET_NOTE, "--category", "safety", "--severity", "high"]) == 0
    assert cli_main(["report", "bundle", "--copy-paste"]) == 0
    store_text = Path(home, "profiles", "default-personal", "state", "feedback", "feedback.jsonl").read_text(encoding="utf-8")
    assert "sk-test-secret-value" not in store_text
    bundle = v0426.create_v042_diagnostic_bundle_result(v0426.create_v042_diagnostic_bundle_request(home_path=str(home), copy_paste=True))
    assert "sk-test-secret-value" not in bundle.rendered_text


def test_v0426_cli_report_bundle_formats(tmp_path: Path, monkeypatch) -> None:
    home = _prepared_home(tmp_path)
    monkeypatch.setenv("CHANTACORE_HOME", str(home))
    assert cli_main(["report", "bundle"]) == 0
    assert cli_main(["report", "bundle", "--copy-paste"]) == 0
    assert cli_main(["report", "bundle", "--format", "markdown"]) == 0
    assert cli_main(["report", "bundle", "--format", "json"]) == 0
