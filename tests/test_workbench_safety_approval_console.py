from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_SAFETY_APPROVAL_EFFECT_TYPES,
    WORKBENCH_SAFETY_APPROVAL_EVENT_TYPES,
    WORKBENCH_SAFETY_APPROVAL_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_SAFETY_APPROVAL_FUTURE_SKILL_IDS,
    WORKBENCH_SAFETY_APPROVAL_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_SAFETY_APPROVAL_OBJECT_TYPES,
    WORKBENCH_SAFETY_APPROVAL_RELATION_TYPES,
    WORKBENCH_SAFETY_APPROVAL_VERSION,
    WorkbenchActionRiskSummary,
    WorkbenchApprovalAuditTrail,
    WorkbenchApprovalCandidate,
    WorkbenchApprovalCandidateEvidenceBundle,
    WorkbenchApprovalConsoleFinding,
    WorkbenchApprovalConsolePrerequisiteSourceService,
    WorkbenchApprovalConsoleReport,
    WorkbenchApprovalConsoleReportService,
    WorkbenchApprovalConsoleView,
    WorkbenchApprovalDecision,
    WorkbenchApprovalDecisionRecord,
    WorkbenchApprovalExpiry,
    WorkbenchApprovalHumanInterventionPoint,
    WorkbenchApprovalRequirement,
    WorkbenchApprovalScope,
    WorkbenchApprovalToken,
    WorkbenchDeferralDecisionRecord,
    WorkbenchManualReviewRecord,
    WorkbenchPIGGuidanceAttachment,
    WorkbenchRejectionDecisionRecord,
    WorkbenchSafetyApprovalPolicy,
    WorkbenchSafetyApprovalRequest,
    WorkbenchSafetyGateSourceView,
    WorkbenchSafetyGateView,
    WorkbenchSafetyRationaleConsoleView,
)


def _parts() -> dict:
    return WorkbenchApprovalConsoleReportService().build_all_parts()


def test_safety_approval_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], WorkbenchSafetyApprovalPolicy)
    assert isinstance(parts["request"], WorkbenchSafetyApprovalRequest)
    assert isinstance(parts["source_view"], WorkbenchSafetyGateSourceView)
    assert isinstance(parts["safety_gate_view"], WorkbenchSafetyGateView)
    assert isinstance(parts["safety_rationale_console_view"], WorkbenchSafetyRationaleConsoleView)
    assert isinstance(parts["approval_console_view"], WorkbenchApprovalConsoleView)
    assert isinstance(parts["approval_requirements"][0], WorkbenchApprovalRequirement)
    assert isinstance(parts["approval_candidates"][0], WorkbenchApprovalCandidate)
    assert isinstance(parts["approval_evidence_bundle"], WorkbenchApprovalCandidateEvidenceBundle)
    assert isinstance(parts["risk_summary"], WorkbenchActionRiskSummary)
    assert isinstance(parts["approval_scope"], WorkbenchApprovalScope)
    assert isinstance(parts["approval_expiry"], WorkbenchApprovalExpiry)
    assert isinstance(parts["approval_token"], WorkbenchApprovalToken)
    assert isinstance(parts["approval_decisions"][0], WorkbenchApprovalDecision)
    assert isinstance(parts["approval_decision_records"][0], WorkbenchApprovalDecisionRecord)
    assert isinstance(parts["rejection_records"][0], WorkbenchRejectionDecisionRecord)
    assert isinstance(parts["deferral_records"][0], WorkbenchDeferralDecisionRecord)
    assert isinstance(parts["manual_review_records"][0], WorkbenchManualReviewRecord)
    assert isinstance(parts["pig_guidance_attachments"][0], WorkbenchPIGGuidanceAttachment)
    assert isinstance(parts["human_intervention_points"][0], WorkbenchApprovalHumanInterventionPoint)
    assert isinstance(parts["approval_audit_trail"], WorkbenchApprovalAuditTrail)
    assert isinstance(parts["findings"][0], WorkbenchApprovalConsoleFinding)
    assert isinstance(parts["report"], WorkbenchApprovalConsoleReport)


def test_policy_sources_and_skills_are_record_only() -> None:
    parts = _parts()
    sources = WorkbenchApprovalConsolePrerequisiteSourceService().load_sources()
    policy = parts["policy"]

    assert WORKBENCH_SAFETY_APPROVAL_VERSION == "v0.26.5"
    assert WORKBENCH_SAFETY_APPROVAL_IMPLEMENTED_SKILL_IDS == [
        "skill:workbench_safety_gate_view",
        "skill:workbench_approval_console_view",
    ]
    assert "skill:workbench_command_surface_use" in WORKBENCH_SAFETY_APPROVAL_FUTURE_SKILL_IDS
    assert "skill:memory_candidate_create" not in WORKBENCH_SAFETY_APPROVAL_FUTURE_SKILL_IDS
    assert sources["view_state"] is not None
    assert sources["safety_gate_panel"].panel_type == "safety_gate_view"
    assert sources["approval_console_panel"].panel_type == "approval_console"
    assert sources["safety_gate"] is not None
    assert sources["evidence_inspector"] is not None
    assert policy.safety_gate_view_enabled is True
    assert policy.approval_console_enabled is True
    assert policy.approval_candidate_enabled is True
    assert policy.approval_decision_record_enabled is True
    assert policy.rejection_decision_record_enabled is True
    assert policy.deferral_decision_record_enabled is True
    assert policy.manual_review_record_enabled is True
    assert policy.human_intervention_point_enabled is True
    assert policy.actual_ui_rendering_enabled is False
    assert policy.approval_execution_enabled is False
    assert policy.approval_token_execution_enabled is False
    assert policy.auto_approval_enabled is False
    assert policy.command_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.route_rerun_enabled is False
    assert policy.stage_rerun_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_adapter_enabled is False
    assert policy.approval_requires_user_intent_ref is True
    assert policy.approval_requires_policy_ref is True
    assert policy.approval_requires_evidence_refs is True
    assert policy.approval_requires_risk_summary is True
    assert policy.approval_requires_scope is True
    assert policy.approval_requires_expiry is True
    assert policy.approval_requires_ocel_visibility is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_is_not_policy_mutation is True
    assert policy.pig_guidance_is_not_execution is True


def test_safety_gate_candidate_scope_expiry_and_token_are_non_executing() -> None:
    parts = _parts()
    source = parts["source_view"]
    safety_view = parts["safety_gate_view"]
    candidate = parts["approval_candidates"][0]
    bundle = parts["approval_evidence_bundle"]
    risk = parts["risk_summary"]
    scope = parts["approval_scope"]
    expiry = parts["approval_expiry"]
    token = parts["approval_token"]

    assert source.source_status in {"complete", "partial", "missing", "blocked"}
    assert source.raw_provider_output_included is False
    assert source.raw_transcript_included is False
    assert source.raw_secret_included is False
    assert safety_view.rationale_refs
    assert safety_view.policy_refs
    assert safety_view.user_intent_refs
    assert safety_view.safety_policy_mutated_now is False
    assert safety_view.execution_triggered_now is False
    assert candidate.candidate_type in {
        "route_approval",
        "provider_invocation_approval",
        "local_runtime_approval",
        "file_edit_approval",
        "command_candidate_approval",
        "risk_acceptance",
        "manual_review",
        "unknown",
    }
    assert candidate.user_intent_refs
    assert candidate.policy_refs
    assert candidate.approval_requirements
    assert candidate.approval_decision_required is True
    assert candidate.executable_now is False
    assert candidate.execution_triggered_now is False
    assert bundle.evidence_count >= 1
    assert bundle.raw_provider_output_included is False
    assert bundle.raw_transcript_included is False
    assert bundle.raw_secret_included is False
    assert risk.risk_level in {"none", "low", "medium", "high", "blocked", "unknown"}
    assert risk.human_review_required is True
    assert scope.max_use_count == 1
    assert scope.scope_grants_execution_now is False
    assert expiry.expired_now is False
    assert token.token_is_command is False
    assert token.token_executes_now is False
    assert token.token_grants_unbounded_execution is False


def test_decision_records_manual_review_pig_intervention_and_audit_do_not_execute() -> None:
    parts = _parts()
    decision = parts["approval_decisions"][0]
    decision_record = parts["approval_decision_records"][0]
    rejection = parts["rejection_records"][0]
    deferral = parts["deferral_records"][0]
    manual = parts["manual_review_records"][0]
    pig = parts["pig_guidance_attachments"][0]
    intervention = parts["human_intervention_points"][0]
    audit = parts["approval_audit_trail"]

    assert decision.decision_type in {
        "approve",
        "reject",
        "defer",
        "request_clarification",
        "request_more_evidence",
        "revoke",
        "expire",
        "unknown",
    }
    assert decision.creates_execution is False
    assert decision.provider_invoked_now is False
    assert decision.local_command_executed_now is False
    assert decision_record.ocel_visible is True
    assert decision_record.execution_triggered is False
    assert rejection.execution_triggered is False
    assert deferral.execution_triggered is False
    assert manual.execution_triggered is False
    assert pig.pig_guidance_is_memory is False
    assert pig.pig_guidance_mutates_policy is False
    assert pig.pig_guidance_executes is False
    assert intervention.ocel_visible is True
    assert intervention.execution_triggered_now is False
    assert audit.audit_event_count >= 1
    assert audit.raw_secret_included is False
    assert audit.raw_provider_output_included is False


def test_report_flags_ocel_pig_ocpx_and_cli_outputs(capsys) -> None:
    service = WorkbenchApprovalConsoleReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status in {"passed", "warning", "failed", "blocked"}
    assert report.ready_for_v0_26_6 is True
    assert report.ready_for_v0_27 is False
    assert report.safety_gate_view_created is True
    assert report.approval_console_view_created is True
    assert report.approval_candidates_created is True
    assert report.approval_decisions_recorded is True
    assert report.rejection_decisions_recorded is True
    assert report.deferral_decisions_recorded is True
    assert report.manual_review_records_created is True
    assert report.human_intervention_points_created is True
    assert report.audit_trail_created is True
    for field_name in [
        "approval_executed",
        "approval_token_executed",
        "auto_approval_performed",
        "command_executed",
        "provider_invoked",
        "route_rerun_performed",
        "stage_rerun_performed",
        "ask_executed",
        "final_response_emitted",
        "local_command_executed",
        "command_rerun_performed",
        "automatic_repair_performed",
        "memory_promoted",
        "persistent_memory_written",
        "persona_mutated",
        "pig_memory_promoted",
        "pig_policy_mutated",
        "pig_executed",
        "schumpeter_split_introduced",
        "credential_exposed",
        "raw_secret_output",
        "raw_provider_output_inline",
        "raw_transcript_persisted",
        "llm_judge_used",
    ]:
        assert getattr(report, field_name) is False
    assert report.next_required_step == "v0.26.6 Run Dashboard / Session Monitor"
    for object_type in [
        "workbench_safety_approval_policy",
        "workbench_approval_candidate",
        "workbench_approval_console_report",
    ]:
        assert object_type in WORKBENCH_SAFETY_APPROVAL_OBJECT_TYPES
    assert "workbench_approval_decision_recorded" in WORKBENCH_SAFETY_APPROVAL_EVENT_TYPES
    assert "records_approval_decision" in WORKBENCH_SAFETY_APPROVAL_RELATION_TYPES
    assert "workbench_approval_candidate_created" in WORKBENCH_SAFETY_APPROVAL_EFFECT_TYPES
    assert "approval_executed" in WORKBENCH_SAFETY_APPROVAL_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.5"
    assert pig["subject"] == "safety_gate_approval_console"
    assert pig["safety_boundary"]["approval_executed"] is False
    assert pig["safety_boundary"]["pig_executed"] is False
    assert ocpx["state"] == "workbench_safety_gate_approval_console_created"
    assert "WorkbenchApprovalConsoleViewState" in ocpx["target_read_models"]
    assert "WorkbenchApprovalAuditTrailState" in ocpx["target_read_models"]

    assert main(["workbench", "approval", "decide", "--candidate-id", "candidate-1", "--decision", "approve"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.5" in output
    assert "approval_console_view_created=true" in output
    assert "decision_record_created=true" in output
    assert "approval_executed=false" in output
    assert "approval_token_executed=false" in output
    assert "auto_approval_performed=false" in output
    assert "command_executed=false" in output
    assert "provider_invoked=false" in output
    assert "ready_for_v0_26_6=true" in output
    assert "ready_for_v0_27=false" in output
