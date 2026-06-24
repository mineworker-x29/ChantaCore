from pathlib import Path

from chanta_core.personal_runtime import default_personal_conversation_router as r
from chanta_core.personal_runtime.default_personal_work_session import (
    create_v043_work_session_state,
    execute_v043_work_session_input,
    parse_v043_work_session_command,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.7_default_conversation_router_minimal_output_restore.md"
SCAN_PATHS = (
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_conversation_router.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_artifacts.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_business_ux.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_chat_shell.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_pilot_closure.py",
    ROOT / "src" / "chanta_core" / "cli" / "main.py",
)


def _assert_clean_default(answer: r.V0437RenderedConversationAnswer) -> None:
    assert answer.contains_type_label is False
    assert answer.contains_raw_grounding_metadata is False
    assert answer.contains_raw_confidence_metadata is False
    assert answer.contains_raw_verification_metadata is False
    assert answer.contains_raw_source_metadata is False
    assert answer.contains_raw_safety_footer is False
    assert answer.contains_duplicate_headings is False
    assert answer.contains_empty_unknown_sections is False
    assert answer.provider_invoked is False
    assert answer.prompt_submitted is False
    assert answer.shell_executed is False
    assert answer.repo_search_used is False
    assert answer.workspace_read_opened is False
    assert answer.memory_mutated is False
    assert answer.core_memory_written is False
    assert answer.production_certified is False


def _assert_no_default_forbidden(text: str) -> None:
    found = r.check_v0437_forbidden_strings(text).forbidden_found
    assert found == ()


def _golden_case(case_id: str) -> r.V0437GoldenTranscriptResult:
    cases = {
        "identity": r.create_v0437_golden_transcript_case(
            "identity",
            "넌 누구야",
            "identity_question",
            "MinimalConversationRenderer",
            ("ChantaCore default-personal", "업무 보조 에이전트"),
            r.DEFAULT_MINIMAL_FORBIDDEN_STRINGS,
        ),
        "capabilities": r.create_v0437_golden_transcript_case(
            "capabilities",
            "무엇을 할 수 있어?",
            "capability_question",
            "MinimalConversationRenderer",
            ("업무 정리", "요약", "TODO", "로컬 노트", "근거 조회"),
            r.DEFAULT_MINIMAL_FORBIDDEN_STRINGS,
        ),
        "runtime_status_repository_basis": r.create_v0437_golden_transcript_case(
            "runtime-status-repository-basis",
            "지금 너의 상태를 체크해봐. 저장소 기준.",
            "repository_status_request",
            "StatusRenderer",
            ("v0.43", "저장소 파일", "직접 읽", "v0.44 Controlled Workspace Read"),
            r.DEFAULT_MINIMAL_FORBIDDEN_STRINGS,
        ),
        "repository_status": r.create_v0437_golden_transcript_case(
            "repository-status",
            "지금 ChantaCore 저장소 상태도 점검해줘",
            "repository_status_request",
            "StatusRenderer",
            ("v0.43", "저장소 파일", "git 상태", "확인하지 않습니다", "현재 가능한 점검"),
            r.DEFAULT_MINIMAL_FORBIDDEN_STRINGS,
        ),
        "summary": r.create_v0437_golden_transcript_case(
            "summary",
            "/summary 오늘 v0.43.7 UX repair를 테스트하고 있어.",
            "explicit_artifact_command",
            "ArtifactRenderer",
            ("업무 요약", "핵심 요약", "다음 액션"),
            r.DEFAULT_ARTIFACT_FORBIDDEN_STRINGS,
        ),
        "artifact_last": r.create_v0437_golden_transcript_case(
            "artifact-last",
            "/artifact last",
            "explicit_artifact_command",
            "ArtifactRenderer",
            ("업무 요약", "핵심 요약"),
            r.DEFAULT_ARTIFACT_FORBIDDEN_STRINGS,
        ),
        "what_happened": r.create_v0437_golden_transcript_case(
            "what-happened",
            "/what-happened",
            "debug_or_report_command",
            "DiagnosticRenderer",
            ("진단",),
            (),
        ),
        "v044_readiness": r.create_v0437_golden_transcript_case(
            "v044-readiness",
            "/v044 readiness",
            "pilot_command",
            "StatusRenderer",
            ("v0.44", "Controlled Workspace Read", "v0.43.7 UX repair", "workspace read remains closed"),
            ("workspace read opened", "production_certified=True"),
        ),
    }
    return r.execute_v0437_golden_transcript_case(cases[case_id])


def test_v0437_intent_kinds_declared():
    assert {item.value for item in r.V0437ConversationIntentKind} >= {
        "identity_question",
        "capability_question",
        "runtime_status_question",
        "repository_status_request",
        "general_chat",
        "explicit_artifact_command",
        "evidence_command",
        "grounded_command",
        "pilot_command",
        "debug_or_report_command",
        "unknown",
    }


def test_v0437_router_policy_plain_text_does_not_default_to_summary_artifact():
    policy = r.create_v0437_conversation_router_policy()
    assert policy.plain_text_defaults_to_summary_artifact is False
    assert policy.explicit_slash_required_for_artifact_mode is True
    assert policy.identity_question_uses_minimal_answer is True
    assert policy.repository_status_request_uses_boundary_answer is True
    assert policy.debug_metadata_hidden_by_default is True
    assert policy.safety_footer_hidden_by_default is True
    assert policy.v044_blocked_until_golden_transcripts_pass is True
    assert policy.production_certified is False


def test_v0437_classifies_identity_question():
    assert r.classify_v0437_conversation_intent("넌 누구야") == "identity_question"
    assert r.classify_v0437_conversation_intent("ChantaCore가 뭐야") == "identity_question"


def test_v0437_classifies_capability_question():
    assert r.classify_v0437_conversation_intent("무엇을 할 수 있어?") == "capability_question"
    assert r.classify_v0437_conversation_intent("지금 가능한 기능 알려줘") == "capability_question"


def test_v0437_classifies_runtime_status_question():
    assert r.classify_v0437_conversation_intent("지금 너의 상태를 체크해봐") == "runtime_status_question"
    assert r.classify_v0437_conversation_intent("provider 상태는?") == "runtime_status_question"


def test_v0437_classifies_repository_status_request():
    assert r.classify_v0437_conversation_intent("지금 ChantaCore 저장소 상태도 점검해줘") == "repository_status_request"
    assert r.classify_v0437_conversation_intent("git 상태 봐줘") == "repository_status_request"


def test_v0437_classifies_general_chat_without_artifact_mode():
    assert r.classify_v0437_conversation_intent("오늘은 회의가 길었어") == "general_chat"
    decision = r.create_v0437_route_decision("오늘은 회의가 길었어")
    assert decision.routed_to_minimal_renderer is True
    assert decision.routed_to_artifact_renderer is False


def test_v0437_classifies_explicit_summary_command_as_artifact():
    assert r.classify_v0437_conversation_intent("/summary 오늘 일") == "explicit_artifact_command"
    assert r.classify_v0437_conversation_intent("오늘 일을 요약해줘") == "explicit_artifact_command"


def test_v0437_classifies_evidence_grounded_pilot_and_debug_commands():
    assert r.classify_v0437_conversation_intent("/recall v0.43.7") == "evidence_command"
    assert r.classify_v0437_conversation_intent("/grounded-summary v0.43.7") == "grounded_command"
    assert r.classify_v0437_conversation_intent("/pilot score") == "pilot_command"
    assert r.classify_v0437_conversation_intent("/what-happened") == "debug_or_report_command"


def test_v0437_route_decision_identity_uses_minimal_not_artifact_renderer():
    decision = r.create_v0437_route_decision("넌 누구야")
    assert decision.intent_kind == "identity_question"
    assert decision.routed_to_minimal_renderer is True
    assert decision.routed_to_artifact_renderer is False
    assert decision.production_certified is False


def test_v0437_route_decision_repository_status_never_requires_shell_repo_or_workspace_read():
    decision = r.create_v0437_route_decision("지금 ChantaCore 저장소 상태도 점검해줘")
    assert decision.intent_kind == "repository_status_request"
    assert decision.routed_to_artifact_renderer is False
    assert decision.shell_required is False
    assert decision.repo_search_required is False
    assert decision.workspace_read_required is False


def test_v0437_identity_answer_minimal_no_type_no_grounding_no_source_no_safety_no_duplicate_heading():
    answer = r.render_v0437_identity_answer()
    _assert_clean_default(answer)
    assert "ChantaCore default-personal" in answer.rendered_text
    assert "업무 보조 에이전트" in answer.rendered_text
    assert "저장소 직접 읽기" in answer.rendered_text
    _assert_no_default_forbidden(answer.rendered_text)


def test_v0437_capability_answer_minimal_and_lists_closed_capabilities_briefly():
    answer = r.render_v0437_capability_answer()
    _assert_clean_default(answer)
    for expected in ("업무 정리", "요약", "TODO", "로컬 노트", "근거 조회"):
        assert expected in answer.rendered_text
    for closed in ("저장소 직접 읽기", "repo search", "셸 실행", "파일 수정"):
        assert closed in answer.rendered_text
    _assert_no_default_forbidden(answer.rendered_text)


def test_v0437_runtime_status_answer_does_not_become_summary_artifact():
    answer = r.render_v0437_runtime_status_answer()
    _assert_clean_default(answer)
    assert answer.renderer_kind == "StatusRenderer"
    assert "v0.43" in answer.rendered_text
    assert "업무 요약" not in answer.rendered_text


def test_v0437_repository_status_answer_does_not_claim_repo_inspection():
    answer = r.render_v0437_repository_status_answer()
    _assert_clean_default(answer)
    assert "git 상태를 확인했습니다" not in answer.rendered_text
    assert "저장소를 확인했습니다" not in answer.rendered_text
    assert answer.contains_false_repo_inspection_claim is False


def test_v0437_repository_status_answer_mentions_v044_controlled_workspace_read():
    answer = r.render_v0437_repository_status_answer()
    assert "v0.44 Controlled Workspace Read" in answer.rendered_text
    assert "현재 가능한 점검" in answer.rendered_text


def test_v0437_repository_status_answer_no_shell_git_suggestion_by_default():
    policy = r.create_v0437_repository_status_response_policy()
    answer = r.render_v0437_repository_status_answer()
    assert policy.suggest_git_shell_execution is False
    assert "git status" not in answer.rendered_text.lower()
    assert "실행해" not in answer.rendered_text
    assert answer.shell_executed is False
    assert answer.repo_search_used is False


def test_v0437_minimal_renderer_hides_type_grounding_confidence_verification_source_safety_and_unknown_sections():
    dirty = "\n".join(
        (
            "업무 요약",
            "type: summary",
            "## 핵심 요약",
            "내용",
            "grounding: x",
            "confidence: medium",
            "verification_required: false",
            "source: y",
            "safety: shell=false",
            "## 배경 / 맥락",
            "알 수 없음",
        )
    )
    answer = r.render_v0437_artifact_default(dirty)
    assert "type:" not in answer.rendered_text
    assert "grounding:" not in answer.rendered_text
    assert "confidence:" not in answer.rendered_text
    assert "verification_required:" not in answer.rendered_text
    assert "source:" not in answer.rendered_text
    assert "safety:" not in answer.rendered_text
    assert "## 배경 / 맥락" not in answer.rendered_text


def test_v0437_duplicate_heading_suppression_removes_repeated_core_summary_heading():
    text = r.suppress_v0437_duplicate_headings("## 핵심 요약\n\n## 핵심 요약\n내용")
    assert text.count("## 핵심 요약") == 1


def test_v0437_duplicate_heading_suppression_removes_duplicate_artifact_title():
    text = r.suppress_v0437_duplicate_headings("업무 요약\n업무 요약\n## 핵심 요약\n내용")
    assert text.count("업무 요약") == 1


def test_v0437_unknown_section_suppression_removes_empty_unknown_blocks():
    text = r.suppress_v0437_unknown_sections("## 배경 / 맥락\n알 수 없음\n\n## 다음 액션\n테스트")
    assert "## 배경 / 맥락" not in text
    assert "알 수 없음" not in text
    assert "## 다음 액션" in text


def test_v0437_safety_footer_hidden_by_default():
    policy = r.create_v0437_safety_footer_policy()
    answer = r.render_v0437_artifact_default("내용\nsafety: shell=false; production_certified=false")
    assert policy.raw_safety_footer_hidden_by_default is True
    assert policy.raw_shell_false_footer_allowed_in_default is False
    assert "safety:" not in answer.rendered_text
    assert "shell=false" not in answer.rendered_text


def test_v0437_artifact_renderer_still_allows_explicit_summary():
    command = parse_v043_work_session_command("/summary 오늘 v0.43.7 UX repair를 테스트하고 있어.")
    answer = r.render_v0437_artifact_default("업무 요약\n\n## 핵심 요약\n오늘 테스트 중입니다.\n\n## 다음 액션\n* golden transcript 확인")
    assert command.command_kind == "summary"
    assert answer.intent_kind == "explicit_artifact_command"
    assert answer.renderer_kind == "ArtifactRenderer"
    assert "업무 요약" in answer.rendered_text


def test_v0437_artifact_renderer_hides_raw_metadata_by_default():
    answer = r.render_v0437_artifact_default(
        "업무 요약\ntype: summary\n## 핵심 요약\n내용\ngrounding: x\nconfidence: y\nverification_required: false\nsource: z\nsafety: shell=false"
    )
    assert "type:" not in answer.rendered_text
    assert "grounding:" not in answer.rendered_text
    assert "confidence:" not in answer.rendered_text
    assert "verification_required:" not in answer.rendered_text
    assert "source:" not in answer.rendered_text
    assert "safety:" not in answer.rendered_text


def test_v0437_artifact_renderer_suppresses_empty_unknown_sections_by_default():
    answer = r.render_v0437_artifact_default("업무 요약\n\n## 배경 / 맥락\n알 수 없음\n\n## 핵심 요약\n내용")
    assert "## 배경 / 맥락" not in answer.rendered_text
    assert "알 수 없음" not in answer.rendered_text
    assert "## 핵심 요약" in answer.rendered_text


def test_v0437_debug_policy_allows_metadata_only_in_debug():
    policy = r.create_v0437_debug_disclosure_policy()
    debug = r.render_v0437_artifact_debug("업무 요약\n\n## 핵심 요약\n내용")
    default = r.render_v0437_artifact_default("업무 요약\n\n## 핵심 요약\n내용")
    assert policy.debug_metadata_hidden_by_default is True
    assert policy.grounding_visible_in_debug is True
    assert "grounding:" in debug.rendered_text
    assert "grounding:" not in default.rendered_text


def test_v0437_what_happened_uses_diagnostic_renderer_not_artifact_renderer():
    decision = r.create_v0437_route_decision("/what-happened")
    assert decision.intent_kind == "debug_or_report_command"
    assert decision.routed_to_diagnostic_renderer is True
    assert decision.routed_to_artifact_renderer is False


def test_v0437_v044_readiness_says_ux_repair_required_and_workspace_read_closed():
    state = create_v043_work_session_state(session_id="v0437-v044-readiness")
    result = execute_v043_work_session_input("/v044 readiness", state)
    assert "v0.43.7 UX repair gate" in result.rendered_text
    assert "golden transcripts pass" in result.rendered_text
    assert "workspace read remains closed in v0.43.7" in result.rendered_text


def test_v0437_golden_transcript_identity_passes():
    result = _golden_case("identity")
    assert result.passed is True


def test_v0437_golden_transcript_capabilities_passes():
    result = _golden_case("capabilities")
    assert result.passed is True


def test_v0437_golden_transcript_runtime_status_repository_basis_passes():
    result = _golden_case("runtime_status_repository_basis")
    assert result.passed is True


def test_v0437_golden_transcript_repository_status_passes():
    result = _golden_case("repository_status")
    assert result.passed is True


def test_v0437_golden_transcript_summary_passes():
    result = _golden_case("summary")
    assert result.passed is True


def test_v0437_golden_transcript_artifact_last_passes():
    result = _golden_case("artifact_last")
    assert result.passed is True


def test_v0437_golden_transcript_what_happened_passes():
    result = _golden_case("what_happened")
    assert result.passed is True


def test_v0437_golden_transcript_v044_readiness_passes():
    result = _golden_case("v044_readiness")
    assert result.passed is True


def test_v0437_forbidden_strings_absent_from_default_identity_output():
    _assert_no_default_forbidden(r.render_v0437_identity_answer().rendered_text)


def test_v0437_forbidden_strings_absent_from_default_repository_status_output():
    _assert_no_default_forbidden(r.render_v0437_repository_status_answer().rendered_text)


def test_v0437_forbidden_strings_absent_from_default_artifact_output_except_allowed_title():
    answer = r.render_v0437_artifact_default(
        "업무 요약\ntype: summary\n\n## 핵심 요약\n내용\n\n## 배경 / 맥락\n알 수 없음\nsafety: shell=false"
    )
    found = r.check_v0437_forbidden_strings(answer.rendered_text, r.DEFAULT_ARTIFACT_FORBIDDEN_STRINGS).forbidden_found
    assert found == ()
    assert "업무 요약" in answer.rendered_text


def test_v0437_v044_gate_recheck_fails_when_identity_output_dirty():
    assert r.create_v0437_v044_gate_recheck(identity_output_clean=False).ready_for_v044_design is False


def test_v0437_v044_gate_recheck_fails_when_repository_output_dirty():
    assert r.create_v0437_v044_gate_recheck(repository_status_output_clean=False).ready_for_v044_design is False


def test_v0437_v044_gate_recheck_fails_when_plain_text_routes_to_summary():
    assert r.create_v0437_v044_gate_recheck(plain_text_not_summary_artifact=False).ready_for_v044_design is False


def test_v0437_v044_gate_recheck_passes_only_when_all_golden_transcripts_pass():
    assert r.create_v0437_v044_gate_recheck(golden_transcripts_pass=False).ready_for_v044_design is False
    assert r.create_v0437_v044_gate_recheck().ready_for_v044_design is True


def test_v0437_readiness_report_sets_router_renderer_golden_transcript_flags_true():
    report = r.create_v0437_readiness_report()
    assert report.conversation_router_ready is True
    assert report.minimal_renderer_ready is True
    assert report.artifact_renderer_boundary_ready is True
    assert report.debug_disclosure_policy_ready is True
    assert report.golden_transcript_tests_ready is True
    assert report.v044_gate_recheck_ready is True
    assert report.integrated_restore_document_ready is True


def test_v0437_readiness_report_keeps_workspace_read_repo_shell_git_edit_tools_functions_subagent_memory_core_and_production_false():
    report = r.create_v0437_readiness_report()
    assert report.ready_for_workspace_read is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_workspace_search is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_git_status_execution is False
    assert report.ready_for_file_edit is False
    assert report.ready_for_patch_apply is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_autonomous_coding is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_v0437_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in r.REQUIRED_V0437_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0437_integrated_document_contains_golden_transcripts_and_copy_paste_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Golden Transcript Acceptance" in text
    assert "넌 누구야" in text
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text


def test_v0437_no_separate_v0437_restore_debug_or_user_guide_docs_created():
    docs = sorted((ROOT / "docs" / "versions" / "v0.43").glob("*v0.43.7*"))
    assert docs == [DOC_PATH]


def test_v0437_no_forbidden_runtime_call_patterns():
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


def test_v0437_no_broad_glob_rglob_oswalk_repo_scan_or_arbitrary_path_read():
    execution_patterns = ("['git', 'status']", '["git", "status"]', "git.exe status", "repo scan", "arbitrary path read")
    for path in SCAN_PATHS:
        text = path.read_text(encoding="utf-8")
        assert "os.walk" not in text
        assert ".rglob(" not in text
        assert "Path.rglob" not in text
        for pattern in execution_patterns:
            assert pattern not in text
