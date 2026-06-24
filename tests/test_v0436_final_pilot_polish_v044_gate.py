from pathlib import Path

from chanta_core.personal_runtime import default_personal_pilot_closure as c
from chanta_core.personal_runtime.default_personal_work_session import (
    V043WorkSessionCommandKind,
    create_v043_work_session_state,
    execute_v043_work_session_command,
    parse_v043_work_session_command,
)


ROOT = Path(__file__).resolve().parents[1]
DOC_PATH = ROOT / "docs" / "versions" / "v0.43" / "v0.43.6_final_pilot_polish_v044_gate_restore.md"
SCAN_PATHS = (
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_pilot_closure.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_pilot_review.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_work_session.py",
    ROOT / "src" / "chanta_core" / "personal_runtime" / "default_personal_chat_shell.py",
    ROOT / "src" / "chanta_core" / "cli" / "main.py",
)


def test_v0436_polish_status_values_declared():
    assert {item.value for item in c.V0436PolishStatus} == {"open", "fixed", "deferred", "accepted", "blocked", "unknown"}


def test_v0436_polish_finding_areas_severities_and_statuses_declared():
    assert {item.value for item in c.V0436PolishFindingArea} >= {
        "command_surface",
        "chat_ux",
        "run_ux",
        "provider_ux",
        "work_flow",
        "artifact_quality",
        "evidence_retrieval",
        "grounded_synthesis",
        "pilot_review",
        "safety",
        "v044_gate",
        "documentation",
        "unknown",
    }
    assert {item.value for item in c.V0436PolishFindingSeverity} == {"info", "low", "medium", "high", "blocker", "unknown"}
    assert {item.value for item in c.V0436PolishFindingStatus} == {
        "open",
        "fixed_in_v0436",
        "deferred_to_v0437",
        "accepted_for_v044",
        "blocks_v044",
        "unknown",
    }


def test_v0436_polish_finding_tracks_blocks_fixed_and_deferred():
    finding = c.create_v0436_polish_finding(status="deferred_to_v0437", fixed_in_v0436=False, deferred_reason="non-blocking")
    assert finding.blocks_v044 is False
    assert finding.fixed_in_v0436 is False
    assert finding.deferred_reason == "non-blocking"
    blocker = c.create_v0436_polish_finding(status="blocks_v044")
    assert blocker.blocks_v044 is True


def test_v0436_command_surface_audit_item_keeps_high_risk_capability_false():
    item = c.create_v0436_command_surface_audit_item(high_risk_capability_opened=True)
    assert item.high_risk_capability_opened is False


def test_v0436_command_surface_audit_requires_no_high_risk_commands_for_v044_ready():
    audit = c.create_v0436_command_surface_audit()
    categories = {item.category for item in audit.items}
    assert categories >= {"start", "work_flow", "artifact", "notes", "evidence", "grounded", "pilot", "diagnostics", "safety", "v044_gate"}
    assert audit.high_risk_commands == ()
    assert audit.ready_for_v044 is True


def test_v0436_business_ux_final_acceptance_tracks_start_chat_workflow_artifact_evidence_grounded_pilot_debug():
    acceptance = c.create_v0436_business_ux_final_acceptance()
    assert acceptance.start_flow_accepted
    assert acceptance.chat_ux_accepted
    assert acceptance.work_flow_accepted
    assert acceptance.artifact_ux_accepted
    assert acceptance.evidence_ux_accepted
    assert acceptance.grounded_ux_accepted
    assert acceptance.pilot_review_accepted
    assert acceptance.default_debug_separation_accepted
    assert acceptance.overall_accepted


def test_v0436_pilot_closure_criteria_include_work_session_artifacts_notes_evidence_grounded_metrics_pi_safety_production_and_v044_gate():
    report = c.create_v0436_pilot_closure_report()
    ids = {item.criterion_id for item in report.criteria}
    assert ids >= {
        "business_work_session_usable",
        "core_workflow_commands_available",
        "artifacts_useful",
        "local_notes_safe",
        "local_evidence_retrieval_safe",
        "grounded_synthesis_traceable",
        "pilot_metrics_available",
        "process_intelligence_reviewable",
        "safety_boundary_intact",
        "production_certification_not_claimed",
        "v044_gate_defined",
    }


def test_v0436_pilot_closure_report_allows_closure_only_without_blockers_and_with_safety_intact():
    report = c.create_v0436_pilot_closure_report()
    assert report.blocker_count == 0
    assert report.v043_closure_allowed is True
    assert report.recommends_v044_design is True
    blocking = c.create_v0436_pilot_closure_criterion("safety_boundary_intact", status="fail", blocks_closure=True)
    blocked_report = c.create_v0436_pilot_closure_report(criteria=(blocking,))
    assert blocked_report.v043_closure_allowed is False
    assert blocked_report.production_certified is False


def test_v0436_pilot_closure_decision_can_close_v043_or_continue_v0437():
    decision = c.create_v0436_pilot_closure_decision()
    assert decision.decision == "close_v043_proceed_v044_design"
    assert decision.close_v043 is True
    assert decision.proceed_to_v044_design is True
    blocking = c.create_v0436_pilot_closure_criterion("business_work_session_usable", status="fail", blocks_closure=True)
    report = c.create_v0436_pilot_closure_report(criteria=(blocking,))
    blocked = c.create_v0436_pilot_closure_decision(report)
    assert blocked.decision in {"continue_v0437_polish", "blocked_by_safety"}
    assert blocked.production_certified is False


def test_v0436_v044_gate_decision_values_declared():
    assert {item.value for item in c.V0436V044GateDecisionKind} == {
        "proceed_to_v044_controlled_workspace_read_design",
        "continue_v0437_polish",
        "blocked_by_safety",
        "blocked_by_unclear_scope",
        "unknown",
    }


def test_v0436_v044_scope_is_design_only_in_v0436_and_does_not_open_workspace_read():
    scope = c.create_v0436_v044_controlled_workspace_read_scope()
    assert scope.design_only_in_v0436
    assert scope.controlled_workspace_read_may_open_in_v044
    assert scope.write_allowed is False
    assert scope.edit_apply_allowed is False
    assert scope.shell_allowed is False
    assert scope.test_execution_allowed is False
    assert scope.repo_wide_search_allowed is False
    assert scope.subagent_allowed is False
    assert scope.production_certified is False


def test_v0436_v044_scope_requires_workspace_root_allowlist_path_validation_budgets_filters_redaction_trace_disclosure_and_denial():
    scope = c.create_v0436_v044_controlled_workspace_read_scope()
    assert set(scope.required_scope_elements) >= set(c.REQUIRED_SCOPE_ELEMENTS)


def test_v0436_v044_safety_gates_include_path_traversal_inside_root_budget_filter_redaction_no_shell_no_edit_no_test_no_scan_trace_disclosure():
    report = c.create_v0436_v044_readiness_report()
    gate_ids = {gate.gate_id for gate in report.safety_gates}
    assert gate_ids >= set(c.REQUIRED_SAFETY_GATES)
    assert all(gate.required and gate.blocks_workspace_read for gate in report.safety_gates)


def test_v0436_v044_risk_register_includes_path_traversal_secret_leakage_broad_scan_repo_overread_prompt_leakage_context_expansion_read_edit_confusion_shell_pressure_memory_pollution_audit_gap():
    register = c.create_v0436_v044_risk_register()
    assert {risk.risk_id for risk in register.risks} >= set(c.REQUIRED_RISKS)
    assert register.mitigations_defined
    assert register.safe_to_design_v044


def test_v0436_v044_readiness_report_recommends_controlled_workspace_read_design_and_forbids_edit_apply_shell_test_subagent_production():
    report = c.create_v0436_v044_readiness_report()
    assert "Controlled Workspace Read Design" in report.recommended_v0440_title
    forbidden = " ".join(report.forbidden_in_v0440)
    for word in ("edit", "apply", "shell", "test", "subagent", "production"):
        assert word in forbidden
    assert report.production_certified is False


def test_v0436_v044_scope_proposal_targets_v0440_controlled_workspace_read_design():
    proposal = c.create_v0436_v044_scope_proposal()
    assert proposal.recommended_next_version == c.V0440_RECOMMENDED_TITLE
    assert "design/spec/contract only" in proposal.allowed_scope
    assert "workspace read" in proposal.forbidden_scope


def test_v0436_v044_handoff_packet_includes_closure_summary_objective_scope_closed_capabilities_safety_gates_risks_tests_and_prompt():
    packet = c.create_v0436_v044_handoff_packet()
    assert packet.v043_closure_summary
    assert packet.v044_objective
    assert packet.allowed_scope
    assert packet.closed_capabilities
    assert packet.safety_gates
    assert packet.risk_summary
    assert packet.required_tests
    assert packet.copy_paste_prompt
    assert packet.production_certified is False


def test_v0436_polish_status_result_is_non_provider_non_prompt_and_production_false():
    result = c.execute_v0436_polish_status(c.create_v0436_polish_status_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.production_certified is False
    assert result.v043_can_close is True


def test_v0436_polish_report_result_is_non_provider_no_file_repo_shell_memory_and_production_false():
    result = c.execute_v0436_polish_report(c.create_v0436_polish_report_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.arbitrary_file_search_used is False
    assert result.repo_search_used is False
    assert result.shell_executed is False
    assert result.memory_mutated is False
    assert result.production_certified is False


def test_v0436_pilot_close_result_is_non_provider_and_production_false():
    result = c.execute_v0436_pilot_close(c.create_v0436_pilot_close_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.production_certified is False
    assert result.closure_decision.close_v043 is True


def test_v0436_v044_readiness_result_does_not_open_workspace_read():
    result = c.execute_v0436_v044_readiness(c.create_v0436_v044_readiness_request())
    assert result.workspace_read_opened is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False


def test_v0436_v044_scope_result_does_not_open_workspace_read():
    result = c.execute_v0436_v044_scope(c.create_v0436_v044_scope_request())
    assert result.workspace_read_opened is False
    assert result.provider_invoked is False
    assert result.prompt_submitted is False


def test_v0436_v044_risks_result_is_non_provider_and_production_false():
    result = c.execute_v0436_v044_risks(c.create_v0436_v044_risks_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.production_certified is False
    assert result.risk_register.risks


def test_v0436_v044_handoff_result_is_non_provider_does_not_open_workspace_read_and_production_false():
    result = c.execute_v0436_v044_handoff(c.create_v0436_v044_handoff_request())
    assert result.provider_invoked is False
    assert result.prompt_submitted is False
    assert result.workspace_read_opened is False
    assert result.production_certified is False


def test_v0436_pilot_closure_trace_record_high_risk_false_and_workspace_read_not_opened():
    record = c.create_v0436_pilot_closure_trace_record()
    assert record.event_kind == "pilot_closure_evaluated"
    assert record.provider_invoked is False
    assert record.prompt_submitted is False
    assert record.arbitrary_file_search_used is False
    assert record.repo_search_used is False
    assert record.workspace_read_opened is False
    assert record.shell_executed is False
    assert record.memory_mutated is False
    assert record.production_certified is False


def test_v0436_pilot_closure_pi_review_record_preserves_closure_safety_and_v044_gate_lineage():
    record = c.create_v0436_pilot_closure_pi_review_record()
    assert record.reconstructable_as_process_event
    assert record.closure_criteria_lineage_preserved
    assert record.safety_lineage_preserved
    assert record.v044_gate_lineage_preserved
    assert record.high_risk_counts_zero


def test_v0436_pilot_closure_safety_report_opens_polish_and_gate_but_keeps_workspace_read_file_repo_shell_edit_tools_functions_subagent_memory_core_false():
    report = c.create_v0436_pilot_closure_safety_report()
    assert report.final_pilot_polish_opened
    assert report.v044_design_gate_opened
    assert report.workspace_read_opened is False
    assert report.arbitrary_file_search_allowed is False
    assert report.repo_search_allowed is False
    assert report.workspace_search_allowed is False
    assert report.shell_execution_allowed is False
    assert report.file_edit_allowed is False
    assert report.patch_apply_allowed is False
    assert report.provider_tool_calling_allowed is False
    assert report.function_calling_allowed is False
    assert report.subagent_allowed is False
    assert report.memory_mutation_allowed is False
    assert report.core_memory_write_allowed is False
    assert report.production_certified is False


def test_v0436_readiness_report_sets_final_polish_and_v044_gate_flags_true():
    report = c.create_v0436_readiness_report()
    assert report.final_pilot_polish_ready
    assert report.command_surface_audit_ready
    assert report.business_ux_final_acceptance_ready
    assert report.pilot_closure_report_ready
    assert report.pilot_closure_decision_ready
    assert report.v044_readiness_report_ready
    assert report.v044_scope_proposal_ready
    assert report.v044_risk_register_ready
    assert report.v044_handoff_packet_ready
    assert report.ready_to_close_v043
    assert report.ready_for_v044_design


def test_v0436_readiness_report_keeps_workspace_read_file_repo_shell_edit_apply_tools_functions_subagent_agentloop_memory_core_and_production_false():
    report = c.create_v0436_readiness_report()
    assert report.ready_for_workspace_read_in_v0436 is False
    assert report.ready_for_arbitrary_file_search is False
    assert report.ready_for_repo_search is False
    assert report.ready_for_workspace_search is False
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


def test_v0436_v0440_handoff_targets_design_scope_contract_only():
    handoff = c.create_v0440_controlled_workspace_read_design_handoff()
    assert handoff.target_version == c.V0440_RECOMMENDED_TITLE
    assert "design only first" in handoff.recommended_focus
    assert "workspace read" in handoff.must_not_open
    assert handoff.production_certified is False


def test_v0436_integrated_document_exists_and_has_required_sections():
    text = DOC_PATH.read_text(encoding="utf-8")
    for section in c.REQUIRED_V0436_RESTORE_SECTIONS:
        assert f"## {section}" in text


def test_v0436_integrated_document_contains_copy_paste_restore_prompt():
    text = DOC_PATH.read_text(encoding="utf-8")
    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "ChantaCore v0.43.6 closes the Business Work Session Pilot with final polish and a v0.44 Controlled Workspace Read gate." in text


def test_v0436_no_separate_v0436_restore_polish_v044_or_user_guide_docs_created():
    docs = sorted((ROOT / "docs" / "versions" / "v0.43").glob("*v0.43.6*"))
    assert docs == [DOC_PATH]


def test_v0436_no_forbidden_runtime_call_patterns_except_bounded_existing_review_reads():
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


def test_v0436_work_session_slash_commands_are_registered_and_deterministic():
    state = create_v043_work_session_state(session_id="v0436-slash-session")
    expected = {
        "/polish status": V043WorkSessionCommandKind.POLISH_STATUS.value,
        "/polish findings": V043WorkSessionCommandKind.POLISH_FINDINGS.value,
        "/polish report": V043WorkSessionCommandKind.POLISH_REPORT.value,
        "/pilot close": V043WorkSessionCommandKind.PILOT_CLOSE.value,
        "/v044 readiness": V043WorkSessionCommandKind.V044_READINESS.value,
        "/v044 scope": V043WorkSessionCommandKind.V044_SCOPE.value,
        "/v044 risks": V043WorkSessionCommandKind.V044_RISKS.value,
        "/v044 handoff": V043WorkSessionCommandKind.V044_HANDOFF.value,
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
