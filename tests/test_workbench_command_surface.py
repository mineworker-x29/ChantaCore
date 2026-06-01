from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES,
    WORKBENCH_COMMAND_SURFACE_EVENT_TYPES,
    WORKBENCH_COMMAND_SURFACE_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_COMMAND_SURFACE_FUTURE_SKILL_IDS,
    WORKBENCH_COMMAND_SURFACE_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_COMMAND_SURFACE_OBJECT_TYPES,
    WORKBENCH_COMMAND_SURFACE_RELATION_TYPES,
    WORKBENCH_COMMAND_SURFACE_VERSION,
    WorkbenchActionCandidate,
    WorkbenchAskPipelineCandidate,
    WorkbenchCommandApprovalRequirement,
    WorkbenchCommandAuditTrail,
    WorkbenchCommandBoundaryTrace,
    WorkbenchCommandCandidate,
    WorkbenchCommandCandidateRationale,
    WorkbenchCommandDecision,
    WorkbenchCommandDecisionRecord,
    WorkbenchCommandEvidenceBundle,
    WorkbenchCommandExecutionEnvelope,
    WorkbenchCommandHistoryEntry,
    WorkbenchCommandPIGGuidanceView,
    WorkbenchCommandRequest,
    WorkbenchCommandResult,
    WorkbenchCommandRiskSummary,
    WorkbenchCommandSafetyFindingView,
    WorkbenchCommandSourceView,
    WorkbenchCommandSurfaceFinding,
    WorkbenchCommandSurfacePolicy,
    WorkbenchCommandSurfaceReport,
    WorkbenchCommandSurfaceReportService,
    WorkbenchCommandSurfaceRequest,
    WorkbenchCommandSurfaceView,
    WorkbenchCommandTypePolicy,
    WorkbenchDoNothingCandidate,
    WorkbenchFileEditCandidate,
    WorkbenchProviderCandidateRef,
    WorkbenchRouteCandidate,
    WorkbenchSkillCandidate,
    WorkbenchSnapshotRequestCandidate,
)


def _parts() -> dict:
    return WorkbenchCommandSurfaceReportService().build_all_parts()


def test_command_surface_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], WorkbenchCommandSurfacePolicy)
    assert isinstance(parts["request"], WorkbenchCommandSurfaceRequest)
    assert isinstance(parts["source_view"], WorkbenchCommandSourceView)
    assert isinstance(parts["command_surface_view"], WorkbenchCommandSurfaceView)
    assert isinstance(parts["command_type_policy"], WorkbenchCommandTypePolicy)
    assert isinstance(parts["command_requests"][0], WorkbenchCommandRequest)
    assert isinstance(parts["command_candidates"][0], WorkbenchCommandCandidate)
    assert isinstance(parts["do_nothing_candidates"][0], WorkbenchDoNothingCandidate)
    assert isinstance(parts["skill_candidates"][0], WorkbenchSkillCandidate)
    assert isinstance(parts["action_candidates"][0], WorkbenchActionCandidate)
    assert isinstance(parts["route_candidates"][0], WorkbenchRouteCandidate)
    assert isinstance(parts["provider_candidate_refs"][0], WorkbenchProviderCandidateRef)
    assert isinstance(parts["file_edit_candidates"][0], WorkbenchFileEditCandidate)
    assert isinstance(parts["ask_pipeline_candidates"][0], WorkbenchAskPipelineCandidate)
    assert isinstance(parts["snapshot_request_candidates"][0], WorkbenchSnapshotRequestCandidate)
    assert isinstance(parts["rationale"], WorkbenchCommandCandidateRationale)
    assert isinstance(parts["evidence_bundle"], WorkbenchCommandEvidenceBundle)
    assert isinstance(parts["risk_summary"], WorkbenchCommandRiskSummary)
    assert isinstance(parts["pig_guidance_view"], WorkbenchCommandPIGGuidanceView)
    assert isinstance(parts["safety_finding_view"], WorkbenchCommandSafetyFindingView)
    assert isinstance(parts["approval_requirement"], WorkbenchCommandApprovalRequirement)
    assert isinstance(parts["boundary_trace"], WorkbenchCommandBoundaryTrace)
    assert isinstance(parts["command_decisions"][0], WorkbenchCommandDecision)
    assert isinstance(parts["command_decision_records"][0], WorkbenchCommandDecisionRecord)
    assert isinstance(parts["execution_envelope"], WorkbenchCommandExecutionEnvelope)
    assert isinstance(parts["command_results"][0], WorkbenchCommandResult)
    assert isinstance(parts["command_history"][0], WorkbenchCommandHistoryEntry)
    assert isinstance(parts["audit_trail"], WorkbenchCommandAuditTrail)
    assert isinstance(parts["findings"][0], WorkbenchCommandSurfaceFinding)
    assert isinstance(parts["report"], WorkbenchCommandSurfaceReport)


def test_policy_skills_and_source_view_are_command_candidate_only() -> None:
    parts = _parts()
    policy = parts["policy"]
    source = parts["source_view"]
    type_policy = parts["command_type_policy"]

    assert WORKBENCH_COMMAND_SURFACE_VERSION == "v0.26.7"
    assert WORKBENCH_COMMAND_SURFACE_IMPLEMENTED_SKILL_IDS == ["skill:workbench_command_surface_use"]
    assert "skill:workbench_snapshot_create" in WORKBENCH_COMMAND_SURFACE_FUTURE_SKILL_IDS
    assert "skill:memory_candidate_create" not in WORKBENCH_COMMAND_SURFACE_FUTURE_SKILL_IDS
    assert policy.command_surface_enabled is True
    assert policy.command_candidate_enabled is True
    assert policy.skill_candidate_enabled is True
    assert policy.action_candidate_enabled is True
    assert policy.route_candidate_enabled is True
    assert policy.provider_candidate_enabled is True
    assert policy.ask_pipeline_candidate_enabled is True
    assert policy.file_edit_candidate_enabled is True
    assert policy.snapshot_request_candidate_enabled is True
    assert policy.do_nothing_candidate_enabled is True
    assert policy.command_decision_record_enabled is True
    assert policy.direct_command_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.file_mutation_enabled is False
    assert policy.patch_application_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.route_rerun_enabled is False
    assert policy.stage_rerun_enabled is False
    assert policy.automatic_retry_enabled is False
    assert policy.automatic_repair_enabled is False
    assert policy.autonomous_loop_enabled is False
    assert policy.approval_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_adapter_enabled is False
    assert policy.command_requires_evidence_refs is True
    assert policy.command_requires_risk_summary is True
    assert policy.command_requires_boundary_trace is True
    assert policy.risky_command_requires_approval_requirement is True
    assert policy.do_nothing_alternative_required is True
    assert policy.refs_only_by_default is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_transcript_inline_forbidden is True
    assert policy.raw_secret_inline_forbidden is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_is_not_policy_mutation is True
    assert policy.pig_guidance_is_not_execution is True
    assert type_policy.default_to_candidate_only is True
    assert type_policy.do_nothing_required is True
    assert "do_nothing" in type_policy.allowed_candidate_types
    assert source.dashboard_report_refs
    assert source.approval_report_refs
    assert source.evidence_report_refs
    assert source.provider_report_refs
    assert source.trace_report_refs
    assert source.skill_registry_refs
    assert source.provider_registry_refs
    assert source.pig_guidance_refs
    assert source.user_intent_refs
    assert source.raw_provider_output_included is False
    assert source.raw_transcript_included is False
    assert source.raw_secret_included is False


def test_command_candidates_and_sub_candidates_do_not_execute() -> None:
    parts = _parts()
    candidate = parts["command_candidates"][0]
    do_nothing = parts["do_nothing_candidates"][0]
    skill = parts["skill_candidates"][0]
    action = parts["action_candidates"][0]
    route = parts["route_candidates"][0]
    provider = parts["provider_candidate_refs"][0]
    file_edit = parts["file_edit_candidates"][0]
    ask = parts["ask_pipeline_candidates"][0]
    snapshot = parts["snapshot_request_candidates"][0]

    assert candidate.candidate_status in {"proposed", "ready_for_review", "incomplete", "rejected", "deferred", "blocked"}
    assert candidate.executable_now is False
    assert candidate.executed_now is False
    assert candidate.evidence_bundle.evidence_refs
    assert candidate.risk_summary.approval_required is True
    assert candidate.boundary_trace.execution_performed_now is False
    assert do_nothing.execution_triggered is False
    assert do_nothing.selected_now is False
    assert skill.skill_executed_now is False
    assert action.action_executed_now is False
    assert action.file_mutated_now is False
    assert action.provider_invoked_now is False
    assert route.route_executed_now is False
    assert route.route_rerun_now is False
    assert provider.provider_invoked_now is False
    assert provider.provider_test_run_performed is False
    assert file_edit.file_mutated_now is False
    assert file_edit.patch_applied_now is False
    assert ask.ask_executed_now is False
    assert ask.final_response_emitted_now is False
    assert snapshot.snapshot_created_now is False
    assert snapshot.ocel_export_created_now is False


def test_rationale_evidence_risk_pig_safety_approval_boundary_are_refs_only() -> None:
    parts = _parts()
    rationale = parts["rationale"]
    evidence = parts["evidence_bundle"]
    risk = parts["risk_summary"]
    pig = parts["pig_guidance_view"]
    safety = parts["safety_finding_view"]
    approval = parts["approval_requirement"]
    boundary = parts["boundary_trace"]

    assert rationale.evidence_refs
    assert evidence.evidence_status == "complete"
    assert evidence.raw_provider_output_included is False
    assert evidence.raw_transcript_included is False
    assert evidence.raw_secret_included is False
    assert risk.risk_level in {"none", "low", "medium", "high", "blocked", "unknown"}
    assert pig.pig_guidance_is_memory is False
    assert pig.pig_guidance_mutates_policy is False
    assert pig.pig_guidance_executes is False
    assert safety.safety_policy_mutated_now is False
    assert approval.approval_required is True
    assert approval.approval_execution_performed is False
    assert boundary.boundary_bypassed is False
    assert boundary.execution_performed_now is False
    assert "v0.26_workbench_view_only" in boundary.required_boundaries


def test_decision_envelope_result_history_audit_and_report_are_non_executing() -> None:
    parts = _parts()
    decision = parts["command_decisions"][0]
    record = parts["command_decision_records"][0]
    envelope = parts["execution_envelope"]
    result = parts["command_results"][0]
    history = parts["command_history"][0]
    audit = parts["audit_trail"]
    report = parts["report"]

    assert decision.decision_type in {
        "approve_candidate",
        "reject_candidate",
        "defer_candidate",
        "request_more_evidence",
        "request_clarification",
        "choose_do_nothing",
        "mark_inspection_only",
        "unknown",
    }
    assert decision.creates_execution is False
    assert record.ocel_visible is True
    assert record.execution_triggered is False
    assert envelope.dispatch_deferred is True
    assert envelope.dispatch_performed_now is False
    assert envelope.provider_invoked_now is False
    assert envelope.local_command_executed_now is False
    assert envelope.file_mutated_now is False
    assert envelope.ask_executed_now is False
    assert envelope.final_response_emitted_now is False
    assert result.external_execution_result is False
    assert result.provider_invocation_result is False
    assert result.local_command_result is False
    assert result.file_mutation_result is False
    assert history.sanitized is True
    assert history.raw_secret_included is False
    assert history.raw_provider_output_included is False
    assert history.raw_transcript_included is False
    assert audit.raw_secret_included is False
    assert audit.raw_provider_output_included is False
    assert audit.raw_transcript_included is False
    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_26_8 is True
    assert report.ready_for_v0_27 is False
    assert report.command_surface_view_created is True
    assert report.command_candidates_created is True
    assert report.do_nothing_candidates_created is True
    assert report.command_decisions_recorded is True
    assert report.command_history_created is True
    assert report.audit_trail_created is True
    assert report.direct_command_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.file_mutated is False
    assert report.patch_applied is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.route_rerun_performed is False
    assert report.stage_rerun_performed is False
    assert report.automatic_retry_performed is False
    assert report.automatic_repair_performed is False
    assert report.autonomous_loop_started is False
    assert report.approval_executed is False
    assert report.approval_token_executed is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.schumpeter_split_introduced is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.26.8 Workbench Snapshot / OCEL Export"


def test_ocel_pig_ocpx_and_cli_outputs(capsys) -> None:
    service = WorkbenchCommandSurfaceReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "workbench_command_candidate" in WORKBENCH_COMMAND_SURFACE_OBJECT_TYPES
    assert "workbench_command_candidate_created" in WORKBENCH_COMMAND_SURFACE_EVENT_TYPES
    assert "creates_command_candidate" in WORKBENCH_COMMAND_SURFACE_RELATION_TYPES
    assert "workbench_command_candidate_created" in WORKBENCH_COMMAND_SURFACE_EFFECT_TYPES
    assert "direct_command_executed" in WORKBENCH_COMMAND_SURFACE_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.7"
    assert pig["subject"] == "workbench_command_surface"
    assert pig["safety_boundary"]["direct_command_executed"] is False
    assert pig["safety_boundary"]["pig_executed"] is False
    assert ocpx["state"] == "workbench_command_surface_created"
    assert "WorkbenchCommandSurfaceViewState" in ocpx["target_read_models"]
    assert "WorkbenchCommandAuditTrailState" in ocpx["target_read_models"]

    assert main(["workbench", "commands", "surface"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.7" in output
    assert "command_surface_view_created=true" in output
    assert "ready_for_v0_26_8=true" in output
    assert "ready_for_v0_27=false" in output
    assert "direct_command_executed=false" in output
    assert "provider_invoked=false" in output
    assert "file_mutated=false" in output
    assert "patch_applied=false" in output
    assert "ask_executed=false" in output
    assert "final_response_emitted=false" in output
    assert "memory_promoted=false" in output
    assert "raw_provider_output_inline=false" in output
    assert "raw_transcript_persisted=false" in output
    assert "llm_judge_used=false" in output
