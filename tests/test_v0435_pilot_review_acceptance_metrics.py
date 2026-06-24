from pathlib import Path

from chanta_core.personal_runtime import default_personal_pilot_review as p
from chanta_core.personal_runtime.default_personal_work_artifacts import (
    create_v043_business_artifact,
    create_v043_business_artifact_envelope,
    remember_v043_business_artifact,
)
from chanta_core.personal_runtime.default_personal_work_session import (
    V043WorkSessionCommandKind,
    create_v043_work_session_state,
    execute_v043_work_session_command,
    parse_v043_work_session_command,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.5_pilot_review_acceptance_metrics_restore.md"
SCAN_PATHS = (
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_pilot_review.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_grounded_synthesis.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_local_evidence_retrieval.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_artifacts.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_memory_boundary.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_chat_shell.py",
    ROOT / "src" / "chanta_core" / "cli" / "main.py",
)


def test_v0435_pilot_metric_dimensions_declared():
    assert {item.value for item in p.V043PilotMetricDimension} >= {
        "work_session_usability",
        "business_artifact_usefulness",
        "evidence_retrieval_quality",
        "grounded_synthesis_quality",
        "process_intelligence_reviewability",
        "safety_boundary_integrity",
        "v044_controlled_workspace_read_readiness",
        "unknown",
    }


def test_v0435_pilot_metric_labels_declared():
    assert {item.value for item in p.V043PilotMetricLabel} == {
        "excellent",
        "good",
        "acceptable",
        "weak",
        "blocked",
        "unknown",
    }


def test_v0435_pilot_gate_decision_kinds_declared():
    assert {item.value for item in p.V043PilotGateDecisionKind} >= {
        "continue_v043_polish",
        "proceed_to_v044_design",
        "blocked_by_safety",
        "blocked_by_usability",
        "blocked_by_missing_evidence",
        "unknown",
    }


def test_v0435_finding_areas_and_severities_declared():
    assert {item.value for item in p.V043PilotFindingArea} >= {
        "ux",
        "command_surface",
        "work_session",
        "artifact_quality",
        "evidence_retrieval",
        "grounded_synthesis",
        "process_intelligence",
        "safety",
        "v044_readiness",
        "provider",
        "unknown",
    }
    assert {item.value for item in p.V043PilotFindingSeverity} == {
        "info",
        "low",
        "medium",
        "high",
        "blocker",
        "unknown",
    }


def test_v0435_metric_score_between_zero_and_one_and_label_thresholds():
    assert p.label_v043_pilot_score(0.85) == "excellent"
    assert p.label_v043_pilot_score(0.70) == "good"
    assert p.label_v043_pilot_score(0.55) == "acceptable"
    assert p.label_v043_pilot_score(0.35) == "weak"
    assert p.label_v043_pilot_score(0.34) == "blocked"
    metric = p.create_v043_pilot_metric(score=5.0, blocking=True)
    assert metric.score == 1.0
    assert metric.label == "weak"


def test_v0435_metric_score_ready_for_v044_only_without_blockers_and_with_safety_acceptable():
    safety = p.create_v043_pilot_metric(p.V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value, score=0.55)
    score = p.create_v043_pilot_metric_score((safety,))
    assert score.ready_for_v044_design is True
    blocked = p.create_v043_pilot_metric("work_session_usability", score=0.2, blocking=True)
    blocked_score = p.create_v043_pilot_metric_score((safety, blocked))
    assert blocked_score.ready_for_v044_design is False


def test_v0435_pilot_evidence_summary_uses_bounded_sources_only_and_no_provider_prompt_file_repo_shell_memory_or_production():
    result = p.create_v043_pilot_evidence_summary()
    assert result.bounded_sources_only is True
    assert result.provider_invoked_for_review is False
    assert result.prompt_submitted_for_review is False
    assert result.arbitrary_file_search_used is False
    assert result.repo_search_used is False
    assert result.shell_executed is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_v0435_work_session_usability_review_tracks_start_commands_chat_debug_friction_and_score():
    review = p.create_v043_work_session_usability_review(user_friction_count=2)
    assert review.start_flow_clear
    assert review.command_discoverability_clear
    assert review.chat_output_clean
    assert review.default_debug_separation_clear
    assert review.user_friction_count == 2
    assert 0 <= review.score <= 1


def test_v0435_business_artifact_usefulness_review_tracks_summary_todo_memo_decision_handoff_facts_next_actions():
    review = p.create_v043_business_artifact_usefulness_review()
    assert review.summary_useful and review.todo_actionable and review.memo_readable
    assert review.decision_brief_useful and review.handoff_useful
    assert review.facts_assumptions_unknowns_separated
    assert review.next_actions_clear


def test_v0435_evidence_retrieval_review_tracks_source_disclosure_recall_bounded_sources_no_result_ranking_and_searched_not_searched():
    review = p.create_v043_evidence_retrieval_usefulness_review()
    assert review.source_disclosure_clear
    assert review.recall_useful
    assert review.bounded_sources_only
    assert review.no_result_guidance_clear
    assert review.ranking_understandable
    assert review.searched_not_searched_clear


def test_v0435_grounded_synthesis_review_tracks_evidence_pack_citations_unsupported_claims_grounding_check_evidence_used_and_no_invented_ids():
    review = p.create_v043_grounded_synthesis_usefulness_review()
    assert review.evidence_pack_linked
    assert review.evidence_ids_cited
    assert review.unsupported_claims_marked
    assert review.grounding_check_available
    assert review.evidence_used_view_available
    assert review.invented_evidence_ids_detected is False


def test_v0435_pi_reviewability_review_tracks_trace_artifact_evidence_feedback_lineage_and_high_risk_zero():
    review = p.create_v043_pi_reviewability_review()
    assert review.trace_run_session_linked
    assert review.artifact_lineage_preserved
    assert review.evidence_lineage_preserved
    assert review.feedback_linked
    assert review.reconstructable_process_events
    assert review.high_risk_counts_zero


def test_v0435_safety_boundary_review_keeps_shell_file_search_repo_tools_functions_subagent_memory_closed_and_production_false():
    review = p.create_v043_safety_boundary_review()
    assert review.shell_closed
    assert review.file_edit_apply_closed
    assert review.arbitrary_file_search_closed
    assert review.repo_search_closed
    assert review.provider_tool_function_closed
    assert review.subagent_closed
    assert review.memory_mutation_closed
    assert review.production_certified is False


def test_v0435_v044_readiness_review_recommends_controlled_workspace_read_design_only_not_edit_apply_shell_test():
    review = p.create_v043_v044_readiness_review()
    assert review.user_value_for_workspace_read_clear
    assert review.read_only_boundary_required
    assert review.allowlist_scope_model_required
    assert review.write_apply_shell_test_remain_closed
    assert "Controlled Workspace Read Design" in review.recommended_v044_scope
    assert "read-only" in review.recommended_v044_scope
    assert "edit/apply/shell/test" in review.recommended_v044_scope


def test_v0435_acceptance_checklist_blocks_next_track_on_blockers_and_production_false():
    item = p.create_v043_pilot_acceptance_checklist_item(status="blocker", blocks_next_track=True)
    checklist = p.create_v043_pilot_acceptance_checklist((item,))
    assert checklist.blocker_count == 1
    assert checklist.ready_for_v044_design is False
    assert checklist.production_certified is False


def test_v0435_pilot_status_result_is_non_provider_non_prompt_and_production_false():
    result = p.execute_v043_pilot_status(p.create_v043_pilot_status_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.production_certified is False
    assert "/pilot review" in result.rendered_text


def test_v0435_pilot_review_result_is_deterministic_no_provider_no_prompt_no_file_repo_shell_memory():
    result = p.execute_v043_pilot_review(p.create_v043_pilot_review_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.arbitrary_file_search_used is False
    assert result.repo_search_used is False
    assert result.shell_executed is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_v0435_pilot_score_result_is_non_provider_and_production_false():
    result = p.execute_v043_pilot_score(p.create_v043_pilot_score_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.production_certified is False
    assert result.metric_score.metrics


def test_v0435_pilot_findings_result_counts_blockers_and_warnings_without_provider():
    result = p.execute_v043_pilot_findings(p.create_v043_pilot_findings_request())
    assert result.blocker_count >= 0
    assert result.warning_count >= 0
    assert result.provider_invoked is False
    assert result.prompt_submitted is False


def test_v0435_pilot_next_result_recommends_v0436_or_v044_based_on_findings():
    safety = p.create_v043_pilot_metric(p.V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value, score=1.0)
    weak = p.create_v043_pilot_metric(p.V043PilotMetricDimension.WORK_SESSION_USABILITY.value, score=0.35)
    v0436 = p.create_v043_pilot_next_result(metric_score=p.create_v043_pilot_metric_score((safety, weak)))
    assert "v0.43.6" in v0436.recommended_next_track
    good = p.create_v043_pilot_next_result(metric_score=p.create_v043_pilot_metric_score((safety,)))
    assert "v0.44" in good.recommended_next_track


def test_v0435_pilot_report_result_includes_summary_metrics_findings_checklist_safety_v044_and_high_risk_false():
    result = p.execute_v043_pilot_report(p.create_v043_pilot_report_request())
    assert result.one_screen_summary
    assert result.metric_score.metrics
    assert result.findings
    assert result.acceptance_checklist.production_certified is False
    assert result.safety_review.production_certified is False
    assert result.v044_readiness_review.write_apply_shell_test_remain_closed
    assert "high_risk" in result.rendered_text


def test_v0435_workflow_score_result_scores_latest_workflow_without_provider():
    session_id = "v0435-workflow-score-session"
    envelope = create_v043_business_artifact_envelope(create_v043_business_artifact(session_id=session_id))
    remember_v043_business_artifact(envelope)
    result = p.execute_v043_workflow_score(p.create_v043_workflow_score_request(session_id=session_id))
    assert result.found is True
    assert result.target_kind == "business_artifact"
    assert result.overall_score > 0
    assert result.provider_invoked is False
    assert result.prompt_submitted is False


def test_v0435_pilot_review_trace_record_is_pi_reviewable_and_high_risk_false():
    record = p.create_v043_pilot_review_trace_record()
    assert record.event_kind == "pilot_review_completed"
    assert record.provider_invoked is False
    assert record.prompt_submitted is False
    assert record.arbitrary_file_search_used is False
    assert record.repo_search_used is False
    assert record.shell_executed is False
    assert record.memory_mutated is False
    assert record.production_certified is False


def test_v0435_pilot_pi_review_record_preserves_metric_feedback_safety_lineage():
    record = p.create_v043_pilot_pi_review_record()
    assert record.reconstructable_as_process_event
    assert record.metric_lineage_preserved
    assert record.feedback_lineage_preserved
    assert record.safety_lineage_preserved
    assert record.bounded_sources_only
    assert record.high_risk_counts_zero


def test_v0435_pilot_review_safety_report_opens_deterministic_review_but_keeps_dangerous_fields_false():
    report = p.create_v043_pilot_review_safety_report()
    assert report.pilot_review_opened
    assert report.deterministic_review_by_default
    assert report.provider_invocation_allowed_by_default is False
    assert report.prompt_submission_allowed_by_default is False
    assert report.arbitrary_file_search_allowed is False
    assert report.repo_search_allowed is False
    assert report.workspace_search_allowed is False
    assert report.external_search_allowed is False
    assert report.shell_execution_allowed is False
    assert report.provider_tool_calling_allowed is False
    assert report.function_calling_allowed is False
    assert report.subagent_allowed is False
    assert report.memory_mutation_allowed is False
    assert report.core_memory_write_allowed is False
    assert report.production_certified is False


def test_v0435_readiness_report_sets_pilot_review_flags_true():
    report = p.create_v0435_readiness_report()
    assert report.pilot_metric_model_ready
    assert report.pilot_status_ready
    assert report.pilot_review_ready
    assert report.pilot_score_ready
    assert report.pilot_findings_ready
    assert report.pilot_next_ready
    assert report.pilot_report_ready
    assert report.acceptance_checklist_ready
    assert report.workflow_score_ready


def test_v0435_readiness_report_keeps_file_repo_workspace_external_shell_edit_apply_tools_functions_subagent_agentloop_memory_core_and_production_false():
    report = p.create_v0435_readiness_report()
    assert report.ready_for_arbitrary_file_search is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_workspace_search is False
    assert report.ready_for_external_search is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_v0435_handoff_recommends_v0436_if_weak_or_v044_if_acceptable_and_safe():
    safety = p.create_v043_pilot_metric(p.V043PilotMetricDimension.SAFETY_BOUNDARY_INTEGRITY.value, score=1.0)
    weak = p.create_v043_pilot_metric(p.V043PilotMetricDimension.WORK_SESSION_USABILITY.value, score=0.2)
    v0436 = p.create_v0436_polish_or_v044_controlled_workspace_read_handoff(p.create_v043_pilot_metric_score((safety, weak)))
    assert "v0.43.6" in v0436.target_version
    v044 = p.create_v0436_polish_or_v044_controlled_workspace_read_handoff(p.create_v043_pilot_metric_score((safety,)))
    assert "v0.44" in v044.target_version
    assert any("read-only" in item for item in v044.recommended_focus)
    assert "shell execution" in v044.must_not_open


def test_v0435_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in p.REQUIRED_V0435_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0435_integrated_document_contains_copy_paste_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "ChantaCore v0.43.5 implements Pilot Review & Work Session Acceptance Metrics." in text


def test_v0435_no_separate_v0435_restore_pilot_metrics_or_user_guide_docs_created():
    docs = sorted((ROOT / "docs" / "versions" / "v0.43").glob("*v0.43.5*"))
    assert docs == [DOC_PATH]


def test_v0435_no_forbidden_runtime_call_patterns_except_bounded_existing_evidence_reads():
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


def test_v0435_work_session_slash_commands_are_registered_and_deterministic():
    state = create_v043_work_session_state(session_id="v0435-slash-session")
    expected = {
        "/pilot status": V043WorkSessionCommandKind.PILOT_STATUS.value,
        "/pilot review": V043WorkSessionCommandKind.PILOT_REVIEW.value,
        "/pilot score": V043WorkSessionCommandKind.PILOT_SCORE.value,
        "/pilot findings": V043WorkSessionCommandKind.PILOT_FINDINGS.value,
        "/pilot next": V043WorkSessionCommandKind.PILOT_NEXT.value,
        "/pilot report": V043WorkSessionCommandKind.PILOT_REPORT.value,
        "/acceptance": V043WorkSessionCommandKind.ACCEPTANCE.value,
        "/workflow score": V043WorkSessionCommandKind.WORKFLOW_SCORE.value,
    }
    for raw, kind in expected.items():
        command = parse_v043_work_session_command(raw)
        assert command.command_kind == kind
        assert command.provider_backed is False
        assert command.deterministic is True
        result = execute_v043_work_session_command(command, state)
        assert result.provider_invoked is False
        assert result.prompt_submitted is False
        assert result.production_certified is False
