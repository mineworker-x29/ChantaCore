from __future__ import annotations

from pathlib import Path

from chanta_core.personal_runtime import default_personal_work_artifacts as v0431
from chanta_core.personal_runtime import default_personal_work_session as v0430


DOC_PATH = Path("docs/versions/v0.43/v0.43.1_business_flow_artifact_quality_restore.md")


def _sample_envelope(session_id: str = "session-test") -> v0431.V043BusinessArtifactEnvelope:
    artifact = v0431.create_v043_business_artifact(
        artifact_type="summary",
        session_id=session_id,
        sections=(
            v0431.create_v043_business_artifact_section("핵심 요약", "테스트를 진행했습니다.", "confirmed_from_user", "high", "explicit user content", False),
            v0431.create_v043_business_artifact_section("다음 액션", "결과를 검토합니다.", "next_action", "medium", "artifact", False),
            v0431.create_v043_business_artifact_section("불확실 / 확인 필요", "provider 품질은 실제 모델로 확인해야 합니다.", "unknown_needs_verification", "unknown", "quality check", True),
        ),
    )
    return v0431.remember_v043_business_artifact(v0431.create_v043_business_artifact_envelope(artifact))


def test_v0431_business_artifact_types_declared() -> None:
    assert {item.value for item in v0431.V043BusinessArtifactType} >= {
        "summary",
        "todo",
        "memo",
        "decision_brief",
        "handoff_note",
        "clarification_questions",
        "process_review",
        "issue_diagnosis",
        "unknown",
    }


def test_v0431_grounding_classes_declared() -> None:
    assert {item.value for item in v0431.V043GroundingClass} >= {
        "confirmed_from_user",
        "session_evidence",
        "data_based_interpretation",
        "likely_hypothesis",
        "assumption",
        "unknown_needs_verification",
        "next_action",
        "risk",
        "unknown",
    }


def test_v0431_artifact_sections_include_grounding_confidence_source_and_verification() -> None:
    section = v0431.create_v043_business_artifact_section("리스크", "확인 필요", "risk", "medium", "session", True)
    assert section.grounding_class == "risk"
    assert section.confidence == "medium"
    assert section.source_summary == "session"
    assert section.requires_verification is True


def test_v0431_business_artifact_tracks_provider_generated_grounded_assumptions_next_actions_and_production_false() -> None:
    artifact = _sample_envelope().artifact
    assert artifact.provider_generated is False
    assert artifact.grounded_in_session is True
    assert artifact.contains_unverified_assumption is True
    assert artifact.next_actions_present is True
    assert artifact.production_certified is False


def test_v0431_artifact_envelope_keeps_shell_subagent_workspace_memory_and_production_false() -> None:
    envelope = _sample_envelope()
    assert envelope.shell_executed is False
    assert envelope.subagent_invoked is False
    assert envelope.workspace_mutated is False
    assert envelope.memory_mutated is False
    assert envelope.production_certified is False


def test_v0431_context_selection_policy_prefers_explicit_content_and_blocks_arbitrary_file_read_and_repo_search() -> None:
    policy = v0431.create_v043_context_selection_policy(max_turns=200, max_chars=999999)
    assert policy.prefer_explicit_user_content is True
    assert policy.allow_arbitrary_file_read is False
    assert policy.allow_repo_search is False
    assert policy.max_turns <= 20
    assert policy.max_chars <= 12000


def test_v0431_session_context_pack_is_bounded_and_uses_no_shell_or_repo_search(tmp_path: Path) -> None:
    pack = v0431.build_v043_session_context_pack(home_path=str(tmp_path), session_id="session-test", explicit_user_content="오늘 테스트를 진행했습니다.")
    assert pack.bounded is True
    assert pack.arbitrary_file_read is False
    assert pack.repo_search_used is False
    assert pack.shell_executed is False
    assert {source.source_kind for source in pack.sources} >= {"explicit_user_content", "recent_session_turns", "last_run_report", "trace_summary"}


def test_v0431_quality_criteria_include_facts_assumptions_next_actions_risks_unknowns_korean_and_process_review() -> None:
    ids = {v0431.create_v043_business_artifact_quality_criterion(item).criterion_id for item in [
        "separates_facts_and_assumptions",
        "includes_next_actions_when_relevant",
        "includes_risks_when_relevant",
        "includes_unknowns_when_relevant",
        "uses_korean_polite_language",
        "process_reviewable",
    ]}
    assert ids == {
        "separates_facts_and_assumptions",
        "includes_next_actions_when_relevant",
        "includes_risks_when_relevant",
        "includes_unknowns_when_relevant",
        "uses_korean_polite_language",
        "process_reviewable",
    }


def test_v0431_summary_template_requires_context_key_changes_next_actions_unknowns() -> None:
    sections = set(v0431.build_v043_summary_artifact_template().required_sections)
    assert {"핵심 요약", "배경 / 맥락", "중요한 결정 또는 변화", "다음 액션", "불확실 / 확인 필요"} <= sections


def test_v0431_todo_template_requires_action_owner_due_dependency_priority_confidence() -> None:
    sections = set(v0431.build_v043_todo_artifact_template().required_sections)
    assert {"action", "owner", "due date", "dependency", "priority", "confidence / unknowns"} <= sections


def test_v0431_memo_template_requires_context_key_points_decisions_open_questions_next_actions() -> None:
    sections = set(v0431.build_v043_memo_artifact_template().required_sections)
    assert {"맥락", "주요 내용", "결정 사항", "미해결 질문", "다음 액션"} <= sections


def test_v0431_decision_template_requires_issue_options_evidence_tradeoffs_risks_recommendation_next_actions() -> None:
    sections = set(v0431.build_v043_decision_brief_artifact_template().required_sections)
    assert {"판단 대상", "선택지", "확인된 근거", "장단점 / tradeoff", "리스크", "권고안", "다음 액션"} <= sections


def test_v0431_handoff_template_requires_background_current_state_done_remaining_risks_next_action() -> None:
    sections = set(v0431.build_v043_handoff_artifact_template().required_sections)
    assert {"배경", "현재 상태", "지금까지 한 일", "남은 일", "리스크 / 주의사항", "다음 액션"} <= sections


def test_v0431_clarification_template_lists_missing_info_why_it_matters_and_questions() -> None:
    sections = set(v0431.build_v043_clarification_artifact_template().required_sections)
    assert {"missing information", "why it matters", "question to ask", "suggested default assumption"} <= sections


def test_v0431_what_happened_template_uses_trace_session_run_language() -> None:
    sections = set(v0431.build_v043_what_happened_artifact_template().required_sections)
    assert {"최근 실행된 흐름", "provider / mode", "run/session 상태", "trace/session/report state", "safety status"} <= sections


def test_v0431_artifact_last_is_read_only_and_non_provider() -> None:
    envelope = _sample_envelope("session-last")
    result = v0431.execute_v043_artifact_last(v0431.create_v043_artifact_last_request(session_id="session-last"))
    assert result.envelope == envelope
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.workspace_mutated is False
    assert result.memory_mutated is False


def test_v0431_revise_preserves_original_and_creates_new_version_without_file_edit_memory_mutation_or_workspace_mutation(tmp_path: Path) -> None:
    original = _sample_envelope("session-revise")
    result = v0431.execute_v043_revise_artifact(
        v0431.create_v043_revise_artifact_request(
            "더 간결하게 바꿔 주세요.",
            home_path=str(tmp_path),
            session_id="session-revise",
            provider="mock",
            previous_envelope=original,
        )
    )
    assert result.original_envelope == original
    assert result.revised_envelope is not None
    assert result.revised_envelope.version.previous_version_id == original.version.version_id
    assert result.preserved_original is True
    assert result.workspace_mutated is False
    assert result.memory_mutated is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False


def test_v0431_clarify_does_not_claim_unavailable_facts() -> None:
    result = v0431.execute_v043_clarify(v0431.create_v043_clarify_request(user_content="테스트 결과를 보고해야 합니다."))
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.questions
    assert "알 수 없음" in result.rendered_text or "확인" in result.rendered_text
    assert "file edited" not in result.rendered_text.lower()


def test_v0431_artifact_trace_record_is_pi_reviewable_and_high_risk_false() -> None:
    record = v0431.create_v043_business_artifact_trace_record(_sample_envelope().artifact, provider_invoked=True, prompt_submitted=True, response_parse_status="parsed")
    assert record.event_kind == "business_artifact_created"
    assert record.provider_invoked is True
    assert record.prompt_submitted is True
    assert record.response_parse_status == "parsed"
    assert record.shell_executed is False
    assert record.subagent_invoked is False
    assert record.workspace_mutated is False
    assert record.memory_mutated is False
    assert record.production_certified is False


def test_v0431_pi_review_record_requires_bounded_context_and_facts_assumptions_unknowns_separated() -> None:
    review = v0431.create_v043_business_artifact_pi_review_record(_sample_envelope().artifact)
    assert review.context_sources_bounded is True
    assert review.facts_assumptions_unknowns_separated is True
    assert review.high_risk_counts_zero is True


def test_v0431_business_flow_acceptance_report_marks_core_flows_ready() -> None:
    report = v0431.create_v043_business_flow_acceptance_report()
    assert report.summary_flow_ready is True
    assert report.todo_flow_ready is True
    assert report.memo_flow_ready is True
    assert report.decision_flow_ready is True
    assert report.handoff_flow_ready is True
    assert report.clarify_flow_ready is True
    assert report.artifact_last_ready is True
    assert report.revise_artifact_ready is True
    assert report.production_certified is False


def test_v0431_readiness_report_sets_artifact_context_quality_trace_pi_flags_true() -> None:
    report = v0431.create_v0431_readiness_report()
    assert report.work_artifact_model_ready is True
    assert report.session_context_pack_ready is True
    assert report.bounded_context_policy_ready is True
    assert report.artifact_quality_report_ready is True
    assert report.artifact_trace_record_ready is True
    assert report.artifact_pi_review_record_ready is True
    assert report.artifact_last_command_ready is True
    assert report.revise_command_ready is True
    assert report.clarify_command_ready is True


def test_v0431_readiness_report_keeps_shell_file_repo_tools_functions_subagent_agentloop_memory_and_production_false() -> None:
    report = v0431.create_v0431_readiness_report()
    assert report.ready_for_shell_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_autonomous_coding is False
    assert report.ready_for_memory_mutation is False
    assert report.production_certified is False


def test_v0431_v0432_handoff_targets_memory_boundary_and_local_note_discipline() -> None:
    handoff = v0431.create_v0432_work_session_memory_boundary_handoff()
    assert "v0.43.2 Work Session Memory Boundary" in handoff.target_version
    assert any("local session notes" in item for item in handoff.recommended_focus)
    assert any("CORE_MEMORY" in item for item in handoff.recommended_focus)
    assert handoff.production_certified is False


def test_v0431_integrated_document_exists_and_has_required_sections() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.0 Baseline Summary",
        "v0.43.1 Goal",
        "Business Artifact Model",
        "Session Context Pack",
        "Bounded Context Selection Policy",
        "Grounding Classes",
        "Artifact Quality Criteria",
        "Summary Flow Standard",
        "Todo Flow Standard",
        "Memo Flow Standard",
        "Decision Brief Standard",
        "Handoff Note Standard",
        "Clarification Flow",
        "What Happened Refinement",
        "Artifact Last / Revise Commands",
        "PI Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.2 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]:
        assert f"## {title}" in text


def test_v0431_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "ChantaCore v0.43.1 improves the quality of business work-session outputs." in text
    assert "Implement ChantaCore v0.43.2" in text


def test_v0431_no_separate_v0431_restore_artifact_or_user_guide_docs_created() -> None:
    docs = list(Path("docs/versions/v0.43").glob("*v0.43.1_*"))
    assert docs == [DOC_PATH]


def test_v0431_no_forbidden_runtime_call_patterns_except_existing_provider_run_and_bounded_session_trace_reads() -> None:
    scanned = [
        Path("src/chanta_core/personal_runtime/default_personal_work_artifacts.py"),
        Path("src/chanta_core/personal_runtime/default_personal_work_session.py"),
        Path("src/chanta_core/cli/main.py"),
    ]
    forbidden = [
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
    ]
    for path in scanned:
        text = path.read_text(encoding="utf-8")
        for pattern in forbidden:
            assert pattern not in text


def test_v0431_work_session_parses_and_executes_artifact_revise_clarify(tmp_path: Path) -> None:
    state = v0430.create_v043_work_session_state(home_path=str(tmp_path), provider="mock")
    summary = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/summary 오늘 테스트를 요약해줘"), state)
    assert summary.provider_invoked is True
    last = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/artifact last"), state)
    assert last.provider_invoked is False
    assert "업무 요약" in last.rendered_text
    revise = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/revise 더 간결하게"), state)
    assert revise.provider_invoked is True
    assert revise.workspace_mutated is False
    clarify = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/clarify"), state)
    assert clarify.provider_invoked is False
    assert "확인 질문" in clarify.rendered_text
