from __future__ import annotations

from pathlib import Path

from chanta_core.personal_runtime import default_personal_memory_boundary as v0432
from chanta_core.personal_runtime import default_personal_work_artifacts as v0431
from chanta_core.personal_runtime import default_personal_work_session as v0430


DOC_PATH = Path("docs/versions/v0.43/v0.43.2_work_session_memory_boundary_restore.md")


def _sample_artifact(session_id: str = "session-note") -> v0431.V043BusinessArtifactEnvelope:
    artifact = v0431.create_v043_business_artifact(
        artifact_type="summary",
        session_id=session_id,
        sections=(
            v0431.create_v043_business_artifact_section("핵심 요약", "v0.43.2는 memory와 local note를 분리합니다.", "confirmed_from_user", "high", "test", False),
            v0431.create_v043_business_artifact_section("다음 액션", "bounded note 테스트를 실행합니다.", "next_action", "medium", "test", False),
            v0431.create_v043_business_artifact_section("불확실 / 확인 필요", "실제 provider 품질은 별도 확인이 필요합니다.", "unknown_needs_verification", "unknown", "test", True),
        ),
    )
    return v0431.remember_v043_business_artifact(v0431.create_v043_business_artifact_envelope(artifact))


def test_v0432_memory_boundary_classes_declared() -> None:
    assert {item.value for item in v0432.V043MemoryBoundaryClass} >= {
        "session_context",
        "business_artifact",
        "local_work_note",
        "feedback_record",
        "memory_candidate",
        "persistent_memory",
        "profile_config",
        "provider_config",
        "workspace_file",
        "unknown",
    }


def test_v0432_memory_mutation_status_values_declared() -> None:
    assert {item.value for item in v0432.V043MemoryMutationStatus} >= {
        "open_for_bounded_local_note",
        "open_for_memory_candidate_only",
        "closed_for_persistent_memory",
        "closed_for_core_memory",
        "denied",
        "blocked",
        "unknown",
    }


def test_v0432_local_note_status_values_declared() -> None:
    assert {item.value for item in v0432.V043LocalNoteStatus} >= {"recorded", "redacted", "rejected", "listed", "shown", "searched", "not_found", "failed", "unknown"}


def test_v0432_local_note_categories_declared() -> None:
    assert {item.value for item in v0432.V043LocalNoteCategory} >= {"work", "meeting", "decision", "handoff", "process_review", "issue", "idea", "reminder", "unknown"}


def test_v0432_memory_candidate_status_values_declared() -> None:
    assert {item.value for item in v0432.V043MemoryCandidateStatus} >= {"proposed", "recorded_as_candidate", "rejected", "not_promoted", "promoted_not_allowed", "unknown"}


def test_v0432_memory_boundary_policy_distinguishes_session_artifact_note_feedback_candidate_and_persistent_memory() -> None:
    policy = v0432.create_v043_memory_boundary_policy()
    assert policy.session_context_is_memory is False
    assert policy.business_artifact_is_memory is False
    assert policy.local_note_is_persistent_memory is False
    assert policy.feedback_is_memory is False
    assert policy.memory_candidate_is_persistent_memory is False


def test_v0432_memory_boundary_policy_disallows_core_memory_profile_provider_workspace_arbitrary_read_repo_search_and_production() -> None:
    policy = v0432.create_v043_memory_boundary_policy()
    assert policy.automatic_core_memory_write_allowed is False
    assert policy.explicit_core_memory_write_allowed is False
    assert policy.profile_config_write_allowed is False
    assert policy.provider_config_write_allowed is False
    assert policy.workspace_write_allowed is False
    assert policy.arbitrary_file_read_allowed is False
    assert policy.repo_search_allowed is False
    assert policy.production_certified is False


def test_v0432_local_work_note_store_policy_is_bounded_append_only_and_not_core_memory() -> None:
    policy = v0432.create_v043_local_work_note_store_policy()
    assert policy.relative_store_path == "profiles/default-personal/state/work_notes/notes.jsonl"
    assert policy.bounded_to_home is True
    assert policy.append_only is True
    assert policy.writes_core_memory is False
    assert policy.writes_workspace is False
    assert policy.stores_secret_values is False


def test_v0432_memory_candidate_store_policy_is_bounded_append_only_and_no_auto_promote() -> None:
    policy = v0432.create_v043_memory_candidate_store_policy()
    assert policy.relative_store_path == "profiles/default-personal/state/work_notes/memory_candidates.jsonl"
    assert policy.bounded_to_home is True
    assert policy.append_only is True
    assert policy.auto_promote_allowed is False
    assert policy.core_memory_write_allowed is False
    assert policy.requires_future_gate_for_promotion is True


def test_v0432_local_work_note_record_redacts_secrets_and_sets_all_high_risk_flags_false() -> None:
    request = v0432.create_v043_local_work_note_request("token=abc123 password=hunter2 sk-1234567890abcdef")
    record = v0432.create_v043_local_work_note_record(request)
    assert "[REDACTED]" in record.note_text_redacted
    assert record.raw_secret_value_persisted is False
    assert record.provider_invoked is False
    assert record.prompt_submitted is False
    assert record.shell_executed is False
    assert record.subagent_invoked is False
    assert record.core_memory_written is False
    assert record.workspace_mutated is False
    assert record.production_certified is False


def test_v0432_local_work_note_append_writes_only_bounded_note_store(tmp_path: Path) -> None:
    result = v0432.append_v043_local_work_note(v0432.create_v043_local_work_note_request("v0.43.2 local note", home_path=str(tmp_path), session_id="s1"))
    assert result.appended is True
    assert result.rejected is False
    assert result.outside_home_paths == ()
    assert result.overwritten_files == ()
    assert result.core_memory_written is False
    assert result.workspace_mutated is False
    assert Path(result.store_path).is_file()
    assert Path(result.store_path).resolve().is_relative_to(tmp_path.resolve())


def test_v0432_local_work_note_list_is_read_only(tmp_path: Path) -> None:
    v0432.append_v043_local_work_note(v0432.create_v043_local_work_note_request("list note", home_path=str(tmp_path)))
    result = v0432.list_v043_local_work_notes(v0432.create_v043_local_work_note_list_request(home_path=str(tmp_path)))
    assert result.count == 1
    assert result.filesystem_written is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False


def test_v0432_local_work_note_show_last_is_read_only(tmp_path: Path) -> None:
    append = v0432.append_v043_local_work_note(v0432.create_v043_local_work_note_request("show last note", home_path=str(tmp_path)))
    result = v0432.show_v043_local_work_note(v0432.create_v043_local_work_note_show_request(home_path=str(tmp_path), target="last"))
    assert result.found is True
    assert result.record == append.note_record
    assert result.filesystem_written is False
    assert result.provider_invoked is False
    assert result.shell_executed is False


def test_v0432_local_work_note_search_only_searches_local_note_store_no_broad_scan_or_repo_search(tmp_path: Path) -> None:
    v0432.append_v043_local_work_note(v0432.create_v043_local_work_note_request("memory boundary note", home_path=str(tmp_path)))
    result = v0432.search_v043_local_work_notes(v0432.create_v043_local_work_note_search_request("memory", home_path=str(tmp_path)))
    assert result.count == 1
    assert result.searched_only_local_note_store is True
    assert result.broad_filesystem_scan_used is False
    assert result.repo_search_used is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False


def test_v0432_note_from_artifact_preserves_artifact_and_does_not_write_memory_or_workspace(tmp_path: Path) -> None:
    artifact = _sample_artifact("session-artifact-note")
    result = v0432.create_v043_note_from_artifact(v0432.create_v043_note_from_artifact_request(home_path=str(tmp_path)), "session-artifact-note", artifact)
    assert result.source_artifact_found is True
    assert result.source_artifact_id == artifact.artifact.artifact_id
    assert result.note_append_result is not None
    assert result.core_memory_written is False
    assert result.workspace_mutated is False
    assert result.provider_invoked is False
    assert artifact.artifact.title == "업무 요약"


def test_v0432_memory_candidate_record_never_promotes_to_persistent_memory() -> None:
    record = v0432.create_v043_memory_candidate_record(v0432.create_v043_memory_candidate_request("remember candidate", "might be useful"))
    assert record.promoted_to_persistent_memory is False
    assert record.core_memory_written is False
    assert record.raw_secret_value_persisted is False
    assert record.production_certified is False


def test_v0432_memory_candidate_append_does_not_write_core_memory(tmp_path: Path) -> None:
    result = v0432.append_v043_memory_candidate(v0432.create_v043_memory_candidate_request("candidate", "reason", home_path=str(tmp_path)))
    assert result.appended is True
    assert result.rejected is False
    assert result.core_memory_written is False
    assert result.production_certified is False
    assert result.outside_home_paths == ()


def test_v0432_memory_boundary_status_explains_persistent_memory_closed_and_no_provider_prompt_shell() -> None:
    result = v0432.create_v043_memory_boundary_status_result()
    assert "persistent memory: closed" in result.rendered_text
    assert "CORE_MEMORY write" in result.rendered_text
    assert result.persistent_memory_write_allowed is False
    assert result.automatic_memory_mutation_allowed is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False


def test_v0432_context_boundary_status_shows_available_context_and_blocks_arbitrary_files_repo_search(tmp_path: Path) -> None:
    result = v0432.create_v043_context_boundary_result(v0432.create_v043_context_boundary_request(home_path=str(tmp_path), session_id="s1"))
    assert result.session_context_available is True
    assert result.arbitrary_files_available is False
    assert result.repo_search_available is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert "arbitrary files: unavailable" in result.rendered_text
    assert "repo search: unavailable" in result.rendered_text


def test_v0432_local_note_trace_record_is_pi_reviewable_and_high_risk_false() -> None:
    record = v0432.create_v043_local_note_trace_record(note_id="note-1", session_id="s1")
    assert record.event_kind == "local_work_note_recorded"
    assert record.note_id == "note-1"
    assert record.provider_invoked is False
    assert record.prompt_submitted is False
    assert record.shell_executed is False
    assert record.subagent_invoked is False
    assert record.core_memory_written is False
    assert record.workspace_mutated is False
    assert record.production_certified is False


def test_v0432_memory_boundary_pi_review_record_requires_persistent_memory_untouched() -> None:
    record = v0432.create_v043_memory_boundary_pi_review_record()
    assert record.reconstructable_as_process_event is True
    assert record.bounded_store_used is True
    assert record.persistent_memory_untouched is True
    assert record.high_risk_counts_zero is True


def test_v0432_memory_boundary_safety_report_opens_notes_and_candidates_but_keeps_memory_workspace_file_repo_shell_subagent_closed() -> None:
    report = v0432.create_v043_memory_boundary_safety_report()
    assert report.local_note_store_opened is True
    assert report.memory_candidate_store_opened is True
    assert report.persistent_memory_write_allowed is False
    assert report.automatic_memory_mutation_allowed is False
    assert report.core_memory_write_allowed is False
    assert report.workspace_write_allowed is False
    assert report.arbitrary_file_read_allowed is False
    assert report.repo_search_allowed is False
    assert report.shell_execution_allowed is False
    assert report.subagent_allowed is False
    assert report.production_certified is False


def test_v0432_readiness_report_sets_note_boundary_flags_true() -> None:
    report = v0432.create_v0432_readiness_report()
    assert report.memory_boundary_policy_ready is True
    assert report.local_work_note_store_ready is True
    assert report.memory_candidate_store_ready is True
    assert report.note_command_ready is True
    assert report.notes_list_show_search_ready is True
    assert report.note_from_artifact_ready is True
    assert report.memory_boundary_status_ready is True
    assert report.context_boundary_status_ready is True
    assert report.local_note_trace_record_ready is True


def test_v0432_readiness_report_keeps_persistent_memory_core_profile_provider_workspace_arbitrary_read_repo_shell_subagent_agentloop_and_production_false() -> None:
    report = v0432.create_v0432_readiness_report()
    assert report.ready_for_persistent_memory_write is False
    assert report.ready_for_automatic_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.ready_for_profile_config_write is False
    assert report.ready_for_provider_config_write is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_arbitrary_file_read is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_autonomous_coding is False
    assert report.production_certified is False


def test_v0432_v0433_handoff_targets_bounded_retrieval_and_local_evidence_search() -> None:
    handoff = v0432.create_v0433_work_session_retrieval_handoff()
    assert "v0.43.3 Work Session Retrieval" in handoff.target_version
    assert any("bounded retrieval" in item for item in handoff.recommended_focus)
    assert any("no repo search" in item for item in handoff.recommended_focus)
    assert handoff.production_certified is False


def test_v0432_integrated_document_exists_and_has_required_sections() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    for title in [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.1 Baseline Summary",
        "v0.43.2 Goal",
        "Memory Boundary Model",
        "Session Context vs Persistent Memory",
        "Business Artifacts vs Local Notes",
        "Feedback vs Memory",
        "Memory Candidates",
        "Local Work Note Store",
        "Memory Candidate Store",
        "Note Commands",
        "Memory Boundary Command",
        "Context Boundary Command",
        "Process Intelligence Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.3 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]:
        assert f"## {title}" in text


def test_v0432_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "ChantaCore v0.43.2 implements Work Session Memory Boundary & Local Note Discipline." in text
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "Implement ChantaCore v0.43.3" in text


def test_v0432_no_separate_v0432_restore_memory_note_or_user_guide_docs_created() -> None:
    docs = list(Path("docs/versions/v0.43").glob("*v0.43.2*"))
    assert docs == [DOC_PATH]


def test_v0432_no_forbidden_runtime_call_patterns_except_bounded_note_candidate_append_and_bounded_reads() -> None:
    scanned = [
        Path("src/chanta_core/personal_runtime/default_personal_memory_boundary.py"),
        Path("src/chanta_core/personal_runtime/default_personal_work_session.py"),
        Path("src/chanta_core/personal_runtime/default_personal_work_artifacts.py"),
        Path("src/chanta_core/personal_runtime/default_personal_chat_shell.py"),
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


def test_v0432_work_session_slash_note_commands_memory_boundary_and_context(tmp_path: Path) -> None:
    state = v0430.create_v043_work_session_state(home_path=str(tmp_path), provider="mock")
    boundary = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/memory-boundary"), state)
    assert boundary.provider_invoked is False
    assert "Memory Boundary" in boundary.rendered_text
    context = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/context"), state)
    assert context.provider_invoked is False
    assert "arbitrary files: unavailable" in context.rendered_text
    note = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/note 오늘 테스트에서 memory와 local note를 분리함"), state)
    assert note.provider_invoked is False
    assert note.workspace_mutated is False
    notes = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/notes"), state)
    assert "memory와 local note" in notes.rendered_text
    last = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/note last"), state)
    assert "memory와 local note" in last.rendered_text
    summary = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/summary 오늘 테스트 내용을 요약해줘"), state)
    assert summary.provider_invoked is True
    from_artifact = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/note from-artifact"), state)
    assert from_artifact.provider_invoked is False
    search = v0430.execute_v043_work_session_command(v0430.parse_v043_work_session_command("/notes search memory"), state)
    assert "memory" in search.rendered_text
