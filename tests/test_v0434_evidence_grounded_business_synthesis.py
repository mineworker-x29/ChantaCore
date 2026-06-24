from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.personal_runtime.default_personal_grounded_synthesis import (
    V043ClaimGroundingStatus,
    V043EvidenceUseStatus,
    V043GroundedSynthesisMode,
    V043GroundedWorkflowKind,
    build_v043_grounded_decision_template,
    build_v043_grounded_handoff_template,
    build_v043_grounded_memo_template,
    build_v043_grounded_synthesis_prompt,
    build_v043_grounded_summary_template,
    build_v043_grounded_todo_template,
    create_v043_active_evidence_pack_state,
    create_v043_evidence_backed_claim,
    create_v043_evidence_citation,
    create_v043_evidence_usage_trace_record,
    create_v043_evidence_use_policy,
    create_v043_evidence_used_request,
    create_v043_grounded_artifact,
    create_v043_grounded_artifact_envelope,
    create_v043_grounded_synthesis_pi_review_record,
    create_v043_grounded_synthesis_request,
    create_v043_grounded_synthesis_safety_report,
    create_v043_grounded_synthesis_result,
    create_v043_grounding_check_request,
    create_v043_grounding_verification_criterion,
    create_v043_grounding_verification_report,
    create_v043_unsupported_claim,
    create_v043_use_evidence_request,
    create_v0434_integrated_restore_document_manifest,
    create_v0434_readiness_report,
    create_v0435_pilot_review_and_workflow_acceptance_handoff,
    evaluate_v043_grounding,
    execute_v043_evidence_used,
    execute_v043_grounded_synthesis,
    execute_v043_grounding_check,
    execute_v043_use_evidence,
)
from chanta_core.personal_runtime.default_personal_memory_boundary import (
    append_v043_local_work_note,
    create_v043_local_work_note_request,
)
from chanta_core.personal_runtime.default_personal_work_session import (
    V043WorkSessionCommandKind,
    create_v043_work_session_state,
    execute_v043_work_session_command,
    parse_v043_work_session_command,
)


DOC_PATH = Path("docs/versions/v0.43/v0.43.4_evidence_grounded_business_synthesis_restore.md")
MODULE_PATH = Path("src/chanta_core/personal_runtime/default_personal_grounded_synthesis.py")


def _seed_home(tmp_path: Path) -> Path:
    home = tmp_path / "home"
    append_v043_local_work_note(
        create_v043_local_work_note_request(
            "v0.43.4 grounded synthesis uses local evidence citations",
            home_path=str(home),
            session_id="session-grounded",
        )
    )
    return home


def _active_pack(tmp_path: Path, session_id: str = "session-grounded"):
    home = _seed_home(tmp_path)
    result = execute_v043_use_evidence(create_v043_use_evidence_request("v0.43.4", home_path=str(home), session_id=session_id))
    return home, result


def test_v0434_grounded_synthesis_modes_declared():
    assert {"explicit_grounded_synthesis", "evidence_selection_only", "deterministic_grounding_check", "evidence_used_view", "provider_synthesis", "unknown"} <= {item.value for item in V043GroundedSynthesisMode}


def test_v0434_grounded_workflow_kinds_declared():
    assert {"grounded_summary", "grounded_todo", "grounded_memo", "grounded_decision", "grounded_handoff", "grounding_check", "evidence_used", "unknown"} <= {item.value for item in V043GroundedWorkflowKind}


def test_v0434_evidence_use_status_values_declared():
    assert {"active", "selected", "unavailable", "empty", "expired", "not_found", "blocked_by_policy", "unknown"} <= {item.value for item in V043EvidenceUseStatus}


def test_v0434_claim_grounding_status_values_declared():
    assert {"evidence_backed", "partially_supported", "unsupported_assumption", "unknown_needs_verification", "contradicted_by_evidence", "not_checked", "unknown"} <= {item.value for item in V043ClaimGroundingStatus}


def test_v0434_evidence_use_policy_requires_explicit_provider_synthesis_and_blocks_file_repo_workspace_external_shell_tools_functions_subagent_memory_core_and_production():
    policy = create_v043_evidence_use_policy()
    assert policy.requires_explicit_user_command_for_provider_synthesis is True
    assert policy.active_evidence_pack_required_for_synthesis is True
    assert policy.allow_query_to_create_evidence_pack is True
    assert policy.cite_evidence_ids_required is True
    assert policy.unsupported_claims_must_be_marked is True
    assert policy.arbitrary_file_search_allowed is False
    assert policy.repo_search_allowed is False
    assert policy.workspace_search_allowed is False
    assert policy.external_search_allowed is False
    assert policy.shell_execution_allowed is False
    assert policy.tool_calling_allowed is False
    assert policy.function_calling_allowed is False
    assert policy.subagent_allowed is False
    assert policy.memory_mutation_allowed is False
    assert policy.core_memory_write_allowed is False
    assert policy.production_certified is False


def test_v0434_evidence_citation_requires_bounded_source():
    citation = create_v043_evidence_citation("item-1", "local_work_note", "note-1", "snippet")
    assert citation.bounded_source is True
    assert citation.evidence_item_id == "item-1"


def test_v0434_evidence_backed_claim_requires_citation_for_evidence_backed_status():
    no_citation = create_v043_evidence_backed_claim("claim", (), "evidence_backed")
    assert no_citation.grounding_status != "evidence_backed"
    citation = create_v043_evidence_citation("item-1")
    backed = create_v043_evidence_backed_claim("claim", (citation,), "evidence_backed")
    assert backed.grounding_status == "evidence_backed"
    assert backed.citations


def test_v0434_unsupported_claim_requires_user_verification():
    claim = create_v043_unsupported_claim("unsupported")
    assert claim.requires_user_verification is True
    assert claim.suggested_label


def test_v0434_active_evidence_pack_state_selection_is_non_provider_non_prompt_and_high_risk_false(tmp_path: Path):
    home, use = _active_pack(tmp_path)
    state = use.active_state
    assert state.evidence_pack_id
    assert state.provider_invoked is False
    assert state.prompt_submitted is False
    assert state.arbitrary_file_search_used is False
    assert state.repo_search_used is False
    assert state.shell_executed is False
    assert state.memory_mutated is False
    assert state.production_certified is False


def test_v0434_use_evidence_request_requires_query_or_use_last_and_bounded_limit():
    request = create_v043_use_evidence_request("query", limit=999)
    assert request.limit <= 10
    with pytest.raises(ValueError):
        create_v043_use_evidence_request(None, use_last=False)
    assert create_v043_use_evidence_request(None, use_last=True).use_last is True


def test_v0434_use_evidence_result_selects_pack_without_provider_prompt_file_repo_shell_or_memory(tmp_path: Path):
    home, result = _active_pack(tmp_path)
    assert result.active_state.evidence_pack_id
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.arbitrary_file_search_used is False
    assert result.repo_search_used is False
    assert result.shell_executed is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_v0434_grounded_synthesis_request_requires_workflow_instruction_and_evidence_pack_or_query(tmp_path: Path):
    with pytest.raises(ValueError):
        create_v043_grounded_synthesis_request("grounded_summary", "", session_id="new-session")
    with pytest.raises(ValueError):
        create_v043_grounded_synthesis_request("grounded_summary", "instruction", session_id="new-session")
    request = create_v043_grounded_synthesis_request("grounded_summary", "instruction", query_text="v0.43.4")
    assert request.workflow_kind == "grounded_summary"


def test_v0434_grounded_synthesis_prompt_includes_runtime_identity_evidence_grounding_citation_unsupported_claim_and_forbidden_capability_instructions(tmp_path: Path):
    home, use = _active_pack(tmp_path)
    request = create_v043_grounded_synthesis_request("grounded_summary", "요약", home_path=str(home), session_id="session-grounded", provider="mock")
    prompt = build_v043_grounded_synthesis_prompt(request)
    assert prompt.runtime_identity_included is True
    assert prompt.evidence_grounding_instruction_included is True
    assert prompt.citation_instruction_included is True
    assert prompt.unsupported_claim_instruction_included is True
    assert prompt.forbidden_capability_claims_included is True
    assert "Do not invent evidence ids" in prompt.prompt_text
    assert "Do not claim arbitrary file access" in prompt.prompt_text


def test_v0434_grounded_synthesis_prompt_excludes_arbitrary_file_repo_and_shell_content(tmp_path: Path):
    home, use = _active_pack(tmp_path)
    request = create_v043_grounded_synthesis_request("grounded_summary", "요약", home_path=str(home), session_id="session-grounded", provider="mock")
    prompt = build_v043_grounded_synthesis_prompt(request)
    assert prompt.arbitrary_file_content_included is False
    assert prompt.repo_content_included is False
    assert prompt.shell_output_included is False


def test_v0434_grounded_synthesis_result_invokes_provider_only_for_explicit_grounded_commands_and_keeps_tools_functions_shell_subagent_memory_core_false(tmp_path: Path):
    home, use = _active_pack(tmp_path)
    request = create_v043_grounded_synthesis_request("grounded_summary", "근거로 요약", home_path=str(home), session_id="session-grounded", provider="mock")
    result = execute_v043_grounded_synthesis(request)
    assert result.provider_invoked is True
    assert result.prompt_submitted is True
    assert result.arbitrary_file_search_used is False
    assert result.repo_search_used is False
    assert result.shell_executed is False
    assert result.tool_calling_used is False
    assert result.function_calling_used is False
    assert result.subagent_invoked is False
    assert result.memory_mutated is False
    assert result.core_memory_written is False
    assert result.production_certified is False
    assert result.used_evidence_item_ids == use.active_state.selected_evidence_item_ids


def test_v0434_grounded_artifact_tracks_evidence_pack_used_items_unsupported_claims_and_production_false():
    unsupported = create_v043_unsupported_claim("unknown")
    section = create_v043_grounded_artifact().sections[0]
    section = type(section)(section.section_id, section.title, section.content, section.claims, (unsupported,), ("item-1",), True)
    artifact = create_v043_grounded_artifact("grounded_summary", "pack-1", ("item-1",), sections=(section,))
    assert artifact.evidence_pack_id == "pack-1"
    assert artifact.used_evidence_item_ids == ("item-1",)
    assert artifact.unsupported_claim_count == 1
    assert artifact.provider_generated is True
    assert artifact.evidence_grounded is True
    assert artifact.production_certified is False


def test_v0434_grounded_templates_exist_for_summary_todo_memo_decision_handoff():
    templates = (
        build_v043_grounded_summary_template(),
        build_v043_grounded_todo_template(),
        build_v043_grounded_memo_template(),
        build_v043_grounded_decision_template(),
        build_v043_grounded_handoff_template(),
    )
    assert {template.workflow_kind for template in templates} == {"grounded_summary", "grounded_todo", "grounded_memo", "grounded_decision", "grounded_handoff"}


def test_v0434_grounded_templates_require_local_evidence_citation_format_and_no_invented_evidence_ids():
    template = build_v043_grounded_decision_template()
    assert "[EVID:<evidence_item_id>]" in template.citation_format
    assert "[NOTE:<note_id>]" in template.citation_format
    assert "invented evidence ids" in template.forbidden_claims
    assert "web citations" in template.forbidden_claims


def test_v0434_grounding_verification_criteria_include_citations_unsupported_claims_no_file_repo_shell_tools_memory_source_disclosure_and_process_review():
    criteria = {
        "cites_evidence_ids",
        "unsupported_claims_marked",
        "no_arbitrary_file_search",
        "no_repo_search",
        "no_shell",
        "no_tool_or_function_calling",
        "no_memory_mutation",
        "no_core_memory_write",
        "source_disclosure_preserved",
        "process_reviewable",
    }
    created = {create_v043_grounding_verification_criterion(item).criterion_id for item in criteria}
    assert created == criteria


def test_v0434_grounding_verification_report_counts_citations_and_unsupported_claims():
    artifact = create_v043_grounded_artifact("grounded_summary", "pack-1", ("item-1", "item-2"))
    report = create_v043_grounding_verification_report(artifact)
    assert report.citation_count == 2
    assert report.unsupported_claim_count == 0
    assert report.passed is True
    empty = evaluate_v043_grounding(create_v043_grounded_artifact("grounded_summary", None, ()))
    assert "has_evidence_pack" in empty.missing_required_criteria
    assert "cites_evidence_ids" in empty.missing_required_criteria


def test_v0434_evidence_used_result_is_read_only_non_provider_and_no_filesystem_write(tmp_path: Path):
    home, use = _active_pack(tmp_path)
    result = execute_v043_evidence_used(create_v043_evidence_used_request(home_path=str(home), session_id="session-grounded"))
    assert result.found is True
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.filesystem_written is False
    assert result.production_certified is False


def test_v0434_grounding_check_is_deterministic_non_provider_by_default(tmp_path: Path):
    home, use = _active_pack(tmp_path)
    synthesis = create_v043_grounded_synthesis_result("grounded_summary", "text", "session-grounded", use.active_state.evidence_pack_id, use.active_state.selected_evidence_item_ids)
    create_v043_grounded_artifact_envelope(synthesis)
    result = execute_v043_grounding_check(create_v043_grounding_check_request(home_path=str(home), session_id="session-grounded"))
    assert result.found is True
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.shell_executed is False
    assert result.production_certified is False


def test_v0434_evidence_usage_trace_record_preserves_lineage_and_high_risk_false():
    record = create_v043_evidence_usage_trace_record("pack-1", ("item-1",), "grounded_summary", "run-1", "session-1")
    assert record.event_kind == "evidence_used_for_grounded_synthesis"
    assert record.evidence_pack_id == "pack-1"
    assert record.used_evidence_item_ids == ("item-1",)
    assert record.arbitrary_file_search_used is False
    assert record.repo_search_used is False
    assert record.shell_executed is False
    assert record.tool_calling_used is False
    assert record.function_calling_used is False
    assert record.subagent_invoked is False
    assert record.memory_mutated is False
    assert record.production_certified is False


def test_v0434_grounded_synthesis_pi_review_record_requires_evidence_lineage_citation_policy_bounded_sources_and_high_risk_zero():
    record = create_v043_grounded_synthesis_pi_review_record("synth-1", "pack-1", "grounded_summary")
    assert record.reconstructable_as_process_event is True
    assert record.evidence_lineage_preserved is True
    assert record.citation_policy_applied is True
    assert record.unsupported_claims_marked is True
    assert record.bounded_sources_only is True
    assert record.high_risk_counts_zero is True


def test_v0434_safety_report_opens_explicit_grounded_provider_synthesis_but_keeps_dangerous_fields_false():
    report = create_v043_grounded_synthesis_safety_report()
    assert report.explicit_grounded_provider_synthesis_opened is True
    assert report.provider_invocation_requires_explicit_command is True
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


def test_v0434_readiness_report_sets_grounded_synthesis_flags_true():
    report = create_v0434_readiness_report()
    assert report.evidence_use_policy_ready is True
    assert report.active_evidence_pack_ready is True
    assert report.grounded_synthesis_prompt_ready is True
    assert report.grounded_summary_ready is True
    assert report.grounded_todo_ready is True
    assert report.grounded_memo_ready is True
    assert report.grounded_decision_ready is True
    assert report.grounded_handoff_ready is True
    assert report.grounding_verification_ready is True
    assert report.evidence_used_view_ready is True
    assert report.evidence_usage_trace_ready is True
    assert report.grounded_synthesis_pi_review_ready is True
    assert report.integrated_restore_document_ready is True
    assert report.v0435_handoff_ready is True


def test_v0434_readiness_report_keeps_file_repo_workspace_external_shell_tools_functions_subagent_agentloop_memory_core_and_production_false():
    report = create_v0434_readiness_report()
    assert report.ready_for_arbitrary_file_search is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_workspace_search is False
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


def test_v0434_v0435_handoff_targets_pilot_review_and_work_session_acceptance_metrics():
    handoff = create_v0435_pilot_review_and_workflow_acceptance_handoff()
    assert handoff.target_version.startswith("v0.43.5 Pilot Review & Work Session Acceptance Metrics")
    assert any("evaluate actual pilot sessions" in item for item in handoff.recommended_focus)
    assert any("score evidence-grounded outputs" in item for item in handoff.recommended_focus)
    assert handoff.production_certified is False


def test_v0434_work_session_commands_parse_and_execute_grounded_flow(tmp_path: Path):
    home = _seed_home(tmp_path)
    state = create_v043_work_session_state(home_path=str(home), provider="mock")
    assert parse_v043_work_session_command("/use-evidence v0.43.4").command_kind == V043WorkSessionCommandKind.USE_EVIDENCE.value
    assert parse_v043_work_session_command("/use-evidence last").command_kind == V043WorkSessionCommandKind.USE_EVIDENCE_LAST.value
    assert parse_v043_work_session_command("/grounded-summary 요약").command_kind == V043WorkSessionCommandKind.GROUNDED_SUMMARY.value
    assert parse_v043_work_session_command("/grounded-decision 판단").command_kind == V043WorkSessionCommandKind.GROUNDED_DECISION.value
    assert parse_v043_work_session_command("/grounding-check").command_kind == V043WorkSessionCommandKind.GROUNDING_CHECK.value
    assert parse_v043_work_session_command("/evidence used").command_kind == V043WorkSessionCommandKind.EVIDENCE_USED.value
    select = execute_v043_work_session_command(parse_v043_work_session_command("/use-evidence v0.43.4"), state)
    assert select.provider_invoked is False
    grounded = execute_v043_work_session_command(parse_v043_work_session_command("/grounded-summary 근거로 요약"), state)
    assert grounded.provider_invoked is True
    assert grounded.prompt_submitted is True
    assert grounded.shell_executed is False
    assert grounded.memory_mutated is False
    used = execute_v043_work_session_command(parse_v043_work_session_command("/evidence used"), state)
    assert used.provider_invoked is False
    assert "used_evidence_item_ids" in used.rendered_text


def test_v0434_integrated_document_exists_and_has_required_sections():
    assert DOC_PATH.exists()
    text = DOC_PATH.read_text(encoding="utf-8")
    sections = [
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "v0.43.3 Baseline Summary",
        "v0.43.4 Goal",
        "Evidence-Grounded Synthesis Concept",
        "Evidence Use Policy",
        "Active Evidence Pack",
        "Grounded Synthesis Commands",
        "Grounded Prompt Contract",
        "Evidence Citation Format",
        "Unsupported Claim Policy",
        "Grounded Artifact Model",
        "Grounding Verification",
        "Evidence Used View",
        "Evidence Usage Trace Record",
        "PI Review Contract",
        "Safety Boundary",
        "Required Test Commands",
        "Manual Pilot Commands",
        "Withdrawal Conditions",
        "v0.43.5 Recommended Next Step",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ]
    for section in sections:
        assert section in text
    manifest = create_v0434_integrated_restore_document_manifest()
    assert manifest.integrated_doc_path.endswith("v0.43.4_evidence_grounded_business_synthesis_restore.md")
    assert manifest.separate_restore_doc_allowed is False


def test_v0434_integrated_document_contains_copy_paste_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "Restore v0.43.4" in text


def test_v0434_no_separate_v0434_restore_grounded_evidence_or_user_guide_docs_created():
    docs = [path.name for path in Path("docs/versions/v0.43").iterdir() if path.is_file() and "v0.43.4" in path.name]
    assert docs == ["v0.43.4_evidence_grounded_business_synthesis_restore.md"]


def test_v0434_no_forbidden_runtime_call_patterns_except_existing_provider_run_for_explicit_grounded_synthesis():
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
