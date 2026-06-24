from __future__ import annotations

import io
from contextlib import redirect_stdout
from pathlib import Path

from chanta_core.cli.main import main as cli_main
from chanta_core.personal_runtime import default_personal_work_session as v0430


DOC_PATH = Path("docs/versions/v0.43/v0.43.0_business_work_session_pilot_restore.md")


def _state(tmp_path: Path) -> v0430.V043WorkSessionState:
    return v0430.create_v043_work_session_state(home_path=str(tmp_path), provider="mock")


def test_v0430_track_identity_declares_business_work_session_pilot_not_codex_like_coding() -> None:
    identity = v0430.create_v043_track_identity()
    assert identity.version == "v0.43.0"
    assert "Business Work Session Pilot" in identity.track_name
    assert identity.opens_codex_like_coding_capabilities is False
    assert identity.opens_business_work_session_pilot is True
    assert identity.production_certified is False


def test_v0430_work_session_modes_declared() -> None:
    assert {item.value for item in v0430.V043WorkSessionMode} >= {
        "general",
        "work_summary",
        "meeting_memo",
        "decision_brief",
        "todo_extraction",
        "handoff_note",
        "process_review",
        "issue_diagnosis",
        "unknown",
    }


def test_v0430_work_flow_kinds_declared() -> None:
    assert {item.value for item in v0430.V043WorkFlowKind} >= {
        "summary",
        "todo",
        "memo",
        "decision",
        "handoff",
        "what_happened",
        "capabilities",
        "feedback",
        "report",
        "unknown",
    }


def test_v0430_work_session_status_values_declared() -> None:
    assert {item.value for item in v0430.V043WorkSessionStatus} >= {
        "started",
        "active",
        "command_completed",
        "provider_run_completed",
        "provider_run_failed",
        "deterministic_result_completed",
        "exited",
        "failed",
        "blocked",
    }


def test_v0430_start_result_is_clean_non_provider_non_prompt_and_non_shell(tmp_path: Path) -> None:
    result = v0430.start_v043_work_session(v0430.create_v043_work_session_start_request(home_path=str(tmp_path)))
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False
    assert result.state.production_certified is False


def test_v0430_start_screen_contains_business_commands_and_no_raw_debug_banner(tmp_path: Path) -> None:
    result = v0430.start_v043_work_session(v0430.create_v043_work_session_start_request(home_path=str(tmp_path)))
    text = result.rendered_text
    assert "Schumpeter" in text
    assert "Business Work Session" in text
    for command in ["/help", "/status", "/exit"]:
        assert command in text
    assert "trace runtime" not in text
    assert "run_id:" not in text
    assert "stack trace" not in text.lower()


def test_v0430_command_kinds_include_new_summary_todo_memo_decision_handoff_what_happened_capabilities_feedback_report() -> None:
    values = {item.value for item in v0430.V043WorkSessionCommandKind}
    assert {
        "new",
        "summary",
        "todo",
        "memo",
        "decision",
        "handoff",
        "what_happened",
        "capabilities",
        "feedback",
        "report",
    } <= values


def test_v0430_capability_map_lists_can_do_and_cannot_do_yet_honestly() -> None:
    capability_map = v0430.create_v043_capability_map()
    assert capability_map.honest is True
    assert capability_map.production_certified is False
    assert {item.label for item in capability_map.can_do} >= {"summary", "memo", "todo extraction", "decision brief", "handoff note"}
    assert capability_map.cannot_do_yet
    assert "아직 못 하는 일" in capability_map.rendered_text


def test_v0430_capability_map_keeps_shell_file_edit_repo_search_subagent_autonomous_coding_closed() -> None:
    cannot = " ".join(item.label for item in v0430.create_v043_capability_map().cannot_do_yet)
    for label in ["shell execution", "file edit/apply", "arbitrary file read", "repo search", "subagents", "autonomous coding", "production automation"]:
        assert label in cannot


def test_v0430_business_flow_templates_exist_for_summary_todo_memo_decision_handoff_issue_diagnosis() -> None:
    for flow in ["summary", "todo", "memo", "decision", "handoff", "issue_diagnosis"]:
        template = v0430.create_v043_business_flow_prompt_template(flow)
        assert template.flow_kind == flow
        assert template.output_structure


def test_v0430_business_flow_templates_use_korean_polite_language_and_forbid_unavailable_claims() -> None:
    template = v0430.create_v043_business_flow_prompt_template("decision")
    assert template.korean_polite_language is True
    forbidden = set(template.forbidden_claims)
    assert {"file access", "shell execution", "external action", "production automation"} <= forbidden


def test_v0430_summary_flow_invokes_existing_single_turn_run_without_shell_subagent_or_tools(tmp_path: Path) -> None:
    request = v0430.create_v043_business_flow_request(
        "summary",
        "오늘 오전 ChantaCore 테스트를 진행했고 결과를 정리해야 합니다.",
        home_path=str(tmp_path),
        provider="mock",
    )
    result = v0430.execute_v043_business_flow(request)
    assert result.provider_invoked is True
    assert result.prompt_submitted is True
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.production_certified is False
    assert result.status == "provider_run_completed"


def test_v0430_todo_flow_outputs_action_owner_due_dependency_unknowns_structure() -> None:
    template = v0430.create_v043_business_flow_prompt_template("todo")
    assert set(template.output_structure) >= {"action", "owner", "due date", "dependency", "confidence / unknowns"}


def test_v0430_memo_flow_outputs_context_key_points_decisions_open_questions_next_actions() -> None:
    template = v0430.create_v043_business_flow_prompt_template("memo")
    assert set(template.output_structure) >= {"context", "key points", "decisions", "open questions", "next actions"}


def test_v0430_decision_flow_outputs_issue_options_evidence_tradeoffs_decision_risks_next_actions() -> None:
    template = v0430.create_v043_business_flow_prompt_template("decision")
    assert set(template.output_structure) >= {"issue", "options", "evidence", "tradeoffs", "decision", "risks", "next actions"}


def test_v0430_handoff_flow_outputs_background_current_state_done_remaining_risks_next_action() -> None:
    template = v0430.create_v043_business_flow_prompt_template("handoff")
    assert set(template.output_structure) >= {"background", "current state", "what was done", "remaining work", "risks", "next action"}


def test_v0430_what_happened_uses_trace_run_session_without_provider_by_default(tmp_path: Path) -> None:
    result = v0430.create_v043_what_happened_result(v0430.create_v043_what_happened_request(home_path=str(tmp_path), session_id="session-test"))
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.subagent_invoked is False
    assert result.trace_summary_used is True
    assert result.run_history_used is True
    assert result.session_used is True
    assert "provider 호출: 이 설명 명령에서는 호출하지 않았습니다" in result.rendered_text


def test_v0430_feedback_command_routes_to_bounded_feedback_loop(tmp_path: Path) -> None:
    state = _state(tmp_path)
    command = v0430.parse_v043_work_session_command("/feedback start UX는 업무 세션처럼 느껴지는지 테스트 중")
    result = v0430.execute_v043_work_session_command(command, state)
    assert command.mutates_feedback_store is True
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.workspace_mutated is False
    assert result.memory_mutated is False
    assert "feedback recorded" in result.rendered_text


def test_v0430_report_command_routes_to_diagnostic_bundle_or_safe_guidance(tmp_path: Path) -> None:
    result = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/report"), _state(tmp_path))
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert "chanta-cli report bundle --copy-paste" in result.rendered_text


def test_v0430_work_session_trace_record_is_pi_reviewable() -> None:
    record = v0430.create_v043_work_session_trace_record(work_session_id="ws-1", flow_kind="summary", run_id="run-1", session_id="session-1", provider_invoked=True, prompt_submitted=True)
    assert record.work_session_id == "ws-1"
    assert record.flow_kind == "summary"
    assert record.run_id == "run-1"
    assert record.session_id == "session-1"
    assert record.shell_executed is False
    assert record.subagent_invoked is False
    assert record.production_certified is False


def test_v0430_work_session_safety_report_opens_business_session_but_keeps_codex_like_capabilities_closed() -> None:
    report = v0430.create_v043_work_session_safety_report()
    assert report.business_work_session_opened is True
    assert report.codex_like_coding_capabilities_opened is False
    assert report.shell_execution_allowed is False
    assert report.file_edit_allowed is False
    assert report.patch_apply_allowed is False
    assert report.provider_tool_calling_allowed is False
    assert report.function_calling_allowed is False
    assert report.production_certified is False


def test_v0430_pilot_readiness_report_sets_business_session_flags_true() -> None:
    report = v0430.create_v043_pilot_readiness_report()
    assert report.business_work_session_start_ready is True
    assert report.work_session_command_surface_ready is True
    assert report.business_flow_templates_ready is True
    assert report.capability_map_ready is True
    assert report.what_happened_ready is True
    assert report.feedback_command_ready is True
    assert report.report_command_ready is True
    assert report.pi_review_contract_ready is True


def test_v0430_pilot_readiness_report_keeps_shell_file_repo_tools_functions_subagent_agentloop_and_production_false() -> None:
    report = v0430.create_v043_pilot_readiness_report()
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
    assert report.production_certified is False


def test_v0430_integrated_document_exists_and_has_required_sections() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.42 Closure Summary",
        "v0.43 Track Goal",
        "Business Work Session Concept",
        "Start Command Contract",
        "Work Session Command Surface",
        "Business Flow Prompt Templates",
        "Capability Map",
        "What Happened Contract",
        "Feedback / Report Integration",
        "Process Intelligence Review Contract",
        "Safety Boundary",
        "Pilot Feedback Criteria",
        "Still-Closed Capabilities",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.1 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]:
        assert f"## {title}" in text


def test_v0430_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "Implement ChantaCore v0.43.1" in text


def test_v0430_no_separate_v0430_restore_work_session_or_user_guide_docs_created() -> None:
    docs = list(Path("docs/versions/v0.43").glob("*v0.43.0*"))
    assert docs == [DOC_PATH]


def test_v0430_no_forbidden_runtime_call_patterns_except_existing_provider_run_feedback_and_report_helpers() -> None:
    scanned = [
        Path("src/chanta_core/personal_runtime/default_personal_work_session.py"),
        Path("src/chanta_core/cli/main.py"),
        Path("src/chanta_core/personal_runtime/default_personal_chat_shell.py"),
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


def test_v0430_cli_start_exists_and_prints_business_entrypoint(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setenv("CHANTACORE_HOME", str(tmp_path))
    output = io.StringIO()
    with redirect_stdout(output):
        code = cli_main(["start", "--once", "/capabilities"])
    text = output.getvalue()
    assert code == 0
    assert "Schumpeter" in text
    assert "/help" in text
    assert "/status" in text
    assert "지금 할 수 있는 일" in text
