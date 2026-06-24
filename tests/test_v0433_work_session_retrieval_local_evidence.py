from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.personal_runtime.default_personal_local_evidence_retrieval import (
    V043EvidenceMatchStrategy,
    V043EvidenceRetrievalMode,
    V043EvidenceSourceKind,
    V043EvidenceSourceStatus,
    create_v043_evidence_boundary_policy,
    create_v043_evidence_explain_request,
    create_v043_evidence_item,
    create_v043_evidence_last_request,
    create_v043_evidence_pack,
    create_v043_evidence_pack_summary,
    create_v043_evidence_query,
    create_v043_evidence_retrieval_pi_review_record,
    create_v043_evidence_retrieval_safety_report,
    create_v043_evidence_retrieval_trace_record,
    create_v043_evidence_search_request,
    create_v043_evidence_source_disclosure,
    create_v043_evidence_source_policy,
    create_v043_evidence_sources_request,
    create_v043_recall_request,
    create_v0433_integrated_restore_document_manifest,
    create_v0433_readiness_report,
    create_v0434_evidence_grounded_workflow_handoff,
    execute_v043_evidence_explain,
    execute_v043_evidence_last,
    execute_v043_evidence_sources,
    execute_v043_recall,
    resolve_v043_evidence_source_descriptors,
    score_v043_evidence_item,
    search_v043_local_evidence,
)
from chanta_core.personal_runtime.default_personal_memory_boundary import (
    append_v043_local_work_note,
    append_v043_memory_candidate,
    create_v043_local_work_note_request,
    create_v043_memory_candidate_request,
)
from chanta_core.personal_runtime.default_personal_work_session import (
    V043WorkSessionCommandKind,
    create_v043_work_session_state,
    execute_v043_work_session_command,
    parse_v043_work_session_command,
)


DOC_PATH = Path("docs/versions/v0.43/v0.43.3_work_session_retrieval_local_evidence_restore.md")
MODULE_PATH = Path("src/chanta_core/personal_runtime/default_personal_local_evidence_retrieval.py")


def _seed_evidence(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    append_v043_local_work_note(
        create_v043_local_work_note_request(
            "v0.43.3 local evidence retrieval pilot note",
            home_path=str(home),
            session_id="session-test",
        )
    )
    append_v043_memory_candidate(
        create_v043_memory_candidate_request(
            "retrieval should remain local bounded evidence",
            "candidate for later explicit memory gate only",
            home_path=str(home),
            session_id="session-test",
        )
    )
    return home


def test_v0433_evidence_source_kinds_declared_without_general_filesystem_or_repo_as_allowed_source():
    values = {item.value for item in V043EvidenceSourceKind}
    assert {
        "local_work_note",
        "memory_candidate",
        "business_artifact",
        "feedback_record",
        "trace_summary",
        "run_report",
        "session_summary",
        "current_session",
        "unknown",
    } <= values
    assert "general_filesystem" not in values
    assert "repo" not in values
    assert "workspace" not in values


def test_v0433_evidence_source_status_values_declared():
    assert {"available", "unavailable", "empty", "unreadable", "skipped_by_policy", "failed", "unknown"} <= {item.value for item in V043EvidenceSourceStatus}


def test_v0433_evidence_retrieval_modes_declared():
    assert {"deterministic_local", "provider_synthesis_disabled", "source_disclosure", "last_result", "explain", "unknown"} <= {item.value for item in V043EvidenceRetrievalMode}


def test_v0433_evidence_match_strategies_declared():
    assert {"substring", "token_overlap", "exact_id", "source_kind_filter", "timestamp_hint", "none", "unknown"} <= {item.value for item in V043EvidenceMatchStrategy}


def test_v0433_evidence_boundary_policy_allows_deterministic_local_but_blocks_provider_prompt_file_repo_workspace_external_shell_memory_and_production():
    policy = create_v043_evidence_boundary_policy()
    assert policy.deterministic_by_default is True
    assert policy.provider_invocation_allowed_by_default is False
    assert policy.prompt_submission_allowed_by_default is False
    assert policy.arbitrary_file_search_allowed is False
    assert policy.repo_search_allowed is False
    assert policy.workspace_search_allowed is False
    assert policy.broad_filesystem_scan_allowed is False
    assert policy.external_search_allowed is False
    assert policy.shell_execution_allowed is False
    assert policy.memory_mutation_allowed is False
    assert policy.core_memory_write_allowed is False
    assert policy.production_certified is False


def test_v0433_evidence_source_policy_is_bounded_read_only_no_append_and_redacted():
    policy = create_v043_evidence_source_policy("local_work_note")
    assert policy.bounded_to_home is True
    assert policy.read_only is True
    assert policy.append_allowed is False
    assert policy.search_allowed is True
    assert policy.secrets_redacted is True
    assert policy.max_records <= 100
    assert policy.max_chars_per_record <= 4000


def test_v0433_source_descriptors_are_bounded_read_only_and_allow_unavailable_sources(tmp_path: Path):
    descriptors = resolve_v043_evidence_source_descriptors(home_path=str(tmp_path / "empty"))
    assert descriptors
    assert all(descriptor.bounded_to_home for descriptor in descriptors)
    assert all(descriptor.read_only for descriptor in descriptors)
    assert any(descriptor.status == "unavailable" for descriptor in descriptors)


def test_v0433_search_request_requires_non_empty_query_and_bounded_limit():
    request = create_v043_evidence_search_request(" retrieval ", limit=999)
    assert request.query_text == "retrieval"
    assert request.limit <= 25
    with pytest.raises(ValueError):
        create_v043_evidence_search_request(" ")


def test_v0433_evidence_query_normalizes_query_and_tokens():
    query = create_v043_evidence_query(create_v043_evidence_search_request("  Local Retrieval  "))
    assert query.normalized_query == "local retrieval"
    assert query.tokens == ("local", "retrieval")
    assert query.match_strategy == "substring"


def test_v0433_evidence_item_sets_bounded_source_and_all_high_risk_flags_false():
    item = create_v043_evidence_item("local_work_note", "retrieval")
    assert item.bounded_source is True
    assert item.provider_invoked is False
    assert item.prompt_submitted is False
    assert item.arbitrary_file_read is False
    assert item.repo_search_used is False
    assert item.shell_executed is False
    assert item.production_certified is False


def test_v0433_scoring_supports_substring_and_token_overlap():
    item = create_v043_evidence_item("local_work_note", "bounded local evidence retrieval")
    substring_query = create_v043_evidence_query(create_v043_evidence_search_request("local evidence"))
    score, terms, strategy = score_v043_evidence_item(item, substring_query)
    assert score == 1.0
    assert strategy == "substring"
    overlap_query = create_v043_evidence_query(create_v043_evidence_search_request("retrieval missing"))
    score, terms, strategy = score_v043_evidence_item(item, overlap_query)
    assert 0 < score < 1
    assert terms == ("retrieval",)
    assert strategy == "token_overlap"


def test_v0433_local_evidence_search_reads_only_allowed_sources(tmp_path: Path):
    home = _seed_evidence(tmp_path)
    result = search_v043_local_evidence(create_v043_evidence_search_request("retrieval", home_path=str(home)))
    source_kinds = {match.item.source_kind for match in result.matches}
    assert {"local_work_note", "memory_candidate"} <= source_kinds
    assert all(match.item.bounded_source for match in result.matches)


def test_v0433_local_evidence_search_does_not_use_broad_filesystem_scan_or_repo_search(tmp_path: Path):
    home = _seed_evidence(tmp_path)
    result = search_v043_local_evidence(create_v043_evidence_search_request("retrieval", home_path=str(home)))
    assert result.arbitrary_file_search_used is False
    assert result.repo_search_used is False
    assert result.workspace_search_used is False
    assert result.broad_filesystem_scan_used is False
    assert result.shell_executed is False


def test_v0433_search_result_discloses_searched_and_skipped_sources(tmp_path: Path):
    home = _seed_evidence(tmp_path)
    result = search_v043_local_evidence(create_v043_evidence_search_request("retrieval", home_path=str(home)))
    assert result.searched_sources
    assert result.skipped_sources
    assert "not searched: arbitrary files" in result.rendered_text


def test_v0433_search_result_high_risk_flags_false(tmp_path: Path):
    home = _seed_evidence(tmp_path)
    result = search_v043_local_evidence(create_v043_evidence_search_request("retrieval", home_path=str(home)))
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False


def test_v0433_evidence_pack_is_bounded_and_non_provider():
    pack = create_v043_evidence_pack("retrieval")
    assert pack.bounded is True
    assert pack.provider_invoked is False
    assert pack.prompt_submitted is False
    assert pack.production_certified is False
    summary = create_v043_evidence_pack_summary(pack)
    assert summary.pack_id == pack.pack_id


def test_v0433_evidence_source_disclosure_lists_not_searched_arbitrary_files_repo_external_web_and_shell():
    disclosure = create_v043_evidence_source_disclosure()
    text = " ".join(disclosure.explicitly_not_searched)
    assert "arbitrary files" in text
    assert "repo" in text
    assert "external web" in text
    assert "shell output" in text
    assert disclosure.arbitrary_files_searched is False
    assert disclosure.repo_searched is False
    assert disclosure.external_web_searched is False
    assert disclosure.shell_used is False
    assert disclosure.memory_mutated is False


def test_v0433_recall_result_is_user_friendly_non_provider_and_has_next_actions(tmp_path: Path):
    home = _seed_evidence(tmp_path)
    result = execute_v043_recall(create_v043_recall_request("retrieval", home_path=str(home)))
    assert "검색어" in result.rendered_text
    assert result.next_actions
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.production_certified is False


def test_v0433_evidence_sources_result_marks_arbitrary_files_repo_external_unavailable(tmp_path: Path):
    result = execute_v043_evidence_sources(create_v043_evidence_sources_request(home_path=str(tmp_path)))
    assert result.arbitrary_files_available is False
    assert result.repo_search_available is False
    assert result.external_search_available is False
    assert result.provider_invoked is False
    assert "arbitrary files: unavailable" in result.rendered_text


def test_v0433_evidence_last_is_read_only_non_provider_and_no_filesystem_write(tmp_path: Path):
    request = create_v043_evidence_last_request(home_path=str(tmp_path))
    result = execute_v043_evidence_last(request)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.filesystem_written is False
    assert result.production_certified is False


def test_v0433_evidence_explain_describes_deterministic_local_search_and_closed_boundaries():
    result = execute_v043_evidence_explain(create_v043_evidence_explain_request())
    assert result.deterministic_local_search is True
    assert result.arbitrary_file_search_allowed is False
    assert result.repo_search_allowed is False
    assert result.external_search_allowed is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.memory_mutation_allowed is False
    assert "deterministic local" in result.rendered_text


def test_v0433_retrieval_trace_record_is_pi_reviewable_and_high_risk_false():
    record = create_v043_evidence_retrieval_trace_record("retrieval", 2, ("local_work_note",))
    assert record.event_kind == "local_evidence_retrieved"
    assert record.provider_invoked is False
    assert record.prompt_submitted is False
    assert record.arbitrary_file_search_used is False
    assert record.repo_search_used is False
    assert record.shell_executed is False
    assert record.memory_mutated is False
    assert record.production_certified is False


def test_v0433_retrieval_pi_review_record_requires_bounded_sources_only_and_high_risk_zero():
    record = create_v043_evidence_retrieval_pi_review_record("retrieval-1", "retrieval", ("local_work_note",))
    assert record.reconstructable_as_process_event is True
    assert record.bounded_sources_only is True
    assert record.high_risk_counts_zero is True


def test_v0433_retrieval_safety_report_opens_bounded_local_evidence_search_but_keeps_dangerous_fields_false():
    report = create_v043_evidence_retrieval_safety_report()
    assert report.bounded_local_evidence_search_opened is True
    assert report.arbitrary_file_search_allowed is False
    assert report.repo_search_allowed is False
    assert report.workspace_search_allowed is False
    assert report.broad_filesystem_scan_allowed is False
    assert report.external_search_allowed is False
    assert report.shell_execution_allowed is False
    assert report.provider_invocation_by_default_allowed is False
    assert report.prompt_submission_by_default_allowed is False
    assert report.memory_mutation_allowed is False
    assert report.core_memory_write_allowed is False
    assert report.production_certified is False


def test_v0433_readiness_report_sets_retrieval_flags_true():
    report = create_v0433_readiness_report()
    assert report.evidence_boundary_policy_ready is True
    assert report.evidence_source_policy_ready is True
    assert report.evidence_source_disclosure_ready is True
    assert report.deterministic_local_search_ready is True
    assert report.recall_command_ready is True
    assert report.evidence_command_ready is True
    assert report.evidence_sources_ready is True
    assert report.evidence_last_ready is True
    assert report.evidence_explain_ready is True
    assert report.retrieval_trace_record_ready is True
    assert report.retrieval_pi_review_ready is True
    assert report.integrated_restore_document_ready is True
    assert report.v0434_handoff_ready is True


def test_v0433_readiness_report_keeps_file_repo_workspace_external_shell_tools_functions_subagent_agentloop_memory_core_and_production_false():
    report = create_v0433_readiness_report()
    assert report.ready_for_arbitrary_file_search is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_workspace_search is False
    assert report.ready_for_broad_filesystem_scan is False
    assert report.ready_for_external_search is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_provider_tool_calling is False
    assert report.ready_for_function_calling is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_general_agent_loop is False
    assert report.ready_for_autonomous_coding is False
    assert report.ready_for_memory_mutation is False
    assert report.ready_for_core_memory_write is False
    assert report.production_certified is False


def test_v0433_v0434_handoff_targets_evidence_grounded_workflow_synthesis_with_explicit_provider_use_only():
    handoff = create_v0434_evidence_grounded_workflow_handoff()
    assert handoff.target_version.startswith("v0.43.4 Evidence-Grounded Business Flow Synthesis")
    assert any("explicitly use a retrieved evidence pack" in item for item in handoff.recommended_focus)
    assert any("provider-backed synthesis only when the user explicitly requests it" in item for item in handoff.recommended_focus)
    assert handoff.production_certified is False


def test_v0433_work_session_commands_parse_and_execute_retrieval(tmp_path: Path):
    home = _seed_evidence(tmp_path)
    state = create_v043_work_session_state(home_path=str(home))
    assert parse_v043_work_session_command("/recall retrieval").command_kind == V043WorkSessionCommandKind.RECALL.value
    assert parse_v043_work_session_command("/evidence retrieval").command_kind == V043WorkSessionCommandKind.EVIDENCE.value
    assert parse_v043_work_session_command("/evidence sources").command_kind == V043WorkSessionCommandKind.EVIDENCE_SOURCES.value
    assert parse_v043_work_session_command("/evidence last").command_kind == V043WorkSessionCommandKind.EVIDENCE_LAST.value
    assert parse_v043_work_session_command("/evidence explain").command_kind == V043WorkSessionCommandKind.EVIDENCE_EXPLAIN.value
    result = execute_v043_work_session_command(parse_v043_work_session_command("/recall retrieval"), state)
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.memory_mutated is False
    assert "검색어" in result.rendered_text


def test_v0433_integrated_document_exists_and_has_required_sections():
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    sections = [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.2 Baseline Summary",
        "v0.43.3 Goal",
        "Local Evidence Retrieval Concept",
        "Allowed Evidence Sources",
        "Disallowed Search Sources",
        "Evidence Boundary Policy",
        "Evidence Source Policy",
        "Retrieval Commands",
        "Recall Result Format",
        "Evidence Source Disclosure",
        "Evidence Pack",
        "Retrieval Trace Record",
        "PI Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.4 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]
    for section in sections:
        assert section in text
    manifest = create_v0433_integrated_restore_document_manifest()
    assert manifest.integrated_doc_path == str(DOC_PATH).replace("/", "\\") or manifest.integrated_doc_path == str(DOC_PATH).replace("\\", "/")
    assert manifest.separate_restore_doc_allowed is False


def test_v0433_integrated_document_contains_copy_paste_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "Restore v0.43.3" in text


def test_v0433_no_separate_v0433_restore_retrieval_evidence_or_user_guide_docs_created():
    docs = [path.name for path in Path("docs/versions/v0.43").iterdir() if path.is_file() and "v0.43.3" in path.name]
    assert docs == ["v0.43.3_work_session_retrieval_local_evidence_restore.md"]


def test_v0433_no_forbidden_runtime_call_patterns_except_bounded_known_store_reads():
    source = MODULE_PATH.read_text(encoding="utf-8")
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
        ".rglob(",
        "glob(",
    )
    for pattern in forbidden:
        assert pattern not in source
