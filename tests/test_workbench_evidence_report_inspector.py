from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WORKBENCH_EVIDENCE_INSPECTOR_EFFECT_TYPES,
    WORKBENCH_EVIDENCE_INSPECTOR_EVENT_TYPES,
    WORKBENCH_EVIDENCE_INSPECTOR_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_EVIDENCE_INSPECTOR_FUTURE_SKILL_IDS,
    WORKBENCH_EVIDENCE_INSPECTOR_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_EVIDENCE_INSPECTOR_OBJECT_TYPES,
    WORKBENCH_EVIDENCE_INSPECTOR_RELATION_TYPES,
    WORKBENCH_EVIDENCE_INSPECTOR_VERSION,
    WorkbenchActionCandidateEvidenceView,
    WorkbenchClaimInspectorView,
    WorkbenchClaimSupportInspectorView,
    WorkbenchDecisionEvidenceView,
    WorkbenchEvidenceBundleView,
    WorkbenchEvidenceFilterState,
    WorkbenchEvidenceInspectionPolicy,
    WorkbenchEvidenceInspectionSummary,
    WorkbenchEvidenceInspectorFinding,
    WorkbenchEvidenceInspectorPolicy,
    WorkbenchEvidenceInspectorPrerequisiteSourceService,
    WorkbenchEvidenceInspectorReport,
    WorkbenchEvidenceInspectorReportService,
    WorkbenchEvidenceInspectorRequest,
    WorkbenchEvidenceInspectorView,
    WorkbenchEvidenceItemView,
    WorkbenchEvidenceSelectionView,
    WorkbenchEvidenceSourceView,
    WorkbenchFailureCauseView,
    WorkbenchLimitationInspectorView,
    WorkbenchPIGGuidanceInspectorView,
    WorkbenchProviderSelectionEvidenceView,
    WorkbenchReportInspectorView,
    WorkbenchRouteSelectionEvidenceView,
    WorkbenchSafetyRationaleView,
    WorkbenchSkillSelectionEvidenceView,
    WorkbenchUncertaintyInspectorView,
    WorkbenchUnsupportedClaimView,
)


def _parts() -> dict:
    return WorkbenchEvidenceInspectorReportService().build_all_parts()


def test_evidence_inspector_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["policy"], WorkbenchEvidenceInspectorPolicy)
    assert isinstance(parts["request"], WorkbenchEvidenceInspectorRequest)
    assert isinstance(parts["source_view"], WorkbenchEvidenceSourceView)
    assert isinstance(parts["evidence_inspector_view"], WorkbenchEvidenceInspectorView)
    assert isinstance(parts["report_inspector_view"], WorkbenchReportInspectorView)
    assert isinstance(parts["evidence_bundle_view"], WorkbenchEvidenceBundleView)
    assert isinstance(parts["evidence_item_views"][0], WorkbenchEvidenceItemView)
    assert isinstance(parts["claim_views"][0], WorkbenchClaimInspectorView)
    assert isinstance(parts["claim_support_views"][0], WorkbenchClaimSupportInspectorView)
    assert isinstance(parts["decision_evidence_views"][0], WorkbenchDecisionEvidenceView)
    assert isinstance(parts["skill_selection_evidence_views"][0], WorkbenchSkillSelectionEvidenceView)
    assert isinstance(parts["action_candidate_evidence_views"][0], WorkbenchActionCandidateEvidenceView)
    assert isinstance(parts["route_selection_evidence_views"][0], WorkbenchRouteSelectionEvidenceView)
    assert isinstance(parts["provider_selection_evidence_views"][0], WorkbenchProviderSelectionEvidenceView)
    assert isinstance(parts["safety_rationale_views"][0], WorkbenchSafetyRationaleView)
    assert isinstance(parts["pig_guidance_views"][0], WorkbenchPIGGuidanceInspectorView)
    assert isinstance(parts["failure_cause_views"][0], WorkbenchFailureCauseView)
    assert isinstance(parts["unsupported_claim_views"][0], WorkbenchUnsupportedClaimView)
    assert isinstance(parts["uncertainty_views"][0], WorkbenchUncertaintyInspectorView)
    assert isinstance(parts["limitation_views"][0], WorkbenchLimitationInspectorView)
    assert isinstance(parts["filter_state"], WorkbenchEvidenceFilterState)
    assert isinstance(parts["selection_view"], WorkbenchEvidenceSelectionView)
    assert isinstance(parts["inspection_policy"], WorkbenchEvidenceInspectionPolicy)
    assert isinstance(parts["inspection_summary"], WorkbenchEvidenceInspectionSummary)
    assert isinstance(parts["findings"][0], WorkbenchEvidenceInspectorFinding)
    assert isinstance(parts["report"], WorkbenchEvidenceInspectorReport)


def test_sources_skills_and_policy_are_evidence_report_inspector_only() -> None:
    parts = _parts()
    sources = WorkbenchEvidenceInspectorPrerequisiteSourceService().load_sources()
    policy = parts["policy"]

    assert WORKBENCH_EVIDENCE_INSPECTOR_VERSION == "v0.26.4"
    assert WORKBENCH_EVIDENCE_INSPECTOR_IMPLEMENTED_SKILL_IDS == ["skill:workbench_evidence_inspector_view"]
    assert "skill:workbench_approval_console_view" in WORKBENCH_EVIDENCE_INSPECTOR_FUTURE_SKILL_IDS
    assert "skill:workbench_command_surface_use" in WORKBENCH_EVIDENCE_INSPECTOR_FUTURE_SKILL_IDS
    assert sources["view_state"] is not None
    assert sources["panel"].panel_type == "evidence_inspector"
    assert sources["response_assembly"] is not None
    assert sources["response_assembly"]["evidence_bundle"] is not None
    assert sources["safety_gate"] is not None
    assert sources["routing"] is not None
    assert sources["provider_browser"] is not None
    assert policy.evidence_inspector_enabled is True
    assert policy.report_inspector_enabled is True
    assert policy.decision_evidence_enabled is True
    assert policy.skill_selection_evidence_enabled is True
    assert policy.action_candidate_evidence_enabled is True
    assert policy.route_selection_evidence_enabled is True
    assert policy.provider_selection_evidence_enabled is True
    assert policy.safety_rationale_view_enabled is True
    assert policy.pig_guidance_inspection_enabled is True
    assert policy.failure_cause_view_enabled is True
    assert policy.unsupported_claim_view_enabled is True
    assert policy.uncertainty_limitation_view_enabled is True
    assert policy.actual_ui_rendering_enabled is False
    assert policy.response_rewrite_enabled is False
    assert policy.factuality_llm_judge_enabled is False
    assert policy.safety_llm_judge_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.route_rerun_enabled is False
    assert policy.stage_rerun_enabled is False
    assert policy.approval_execution_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_adapter_enabled is False
    assert policy.refs_only_by_default is True
    assert policy.raw_provider_output_inline_forbidden is True
    assert policy.raw_transcript_inline_forbidden is True
    assert policy.raw_secret_inline_forbidden is True
    assert policy.credential_inline_forbidden is True
    assert policy.private_path_sanitization_required is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_is_not_policy_mutation is True
    assert policy.pig_guidance_is_not_execution is True
    assert policy.ocel_visible is True


def test_source_evidence_claim_and_support_views_are_refs_only() -> None:
    parts = _parts()
    source = parts["source_view"]
    bundle = parts["evidence_bundle_view"]
    evidence = parts["evidence_item_views"][0]
    claim = parts["claim_views"][0]
    support = parts["claim_support_views"][0]

    assert source.response_assembly_report_ref is not None
    assert source.evidence_bundle_ref is not None
    assert source.claim_refs
    assert source.claim_support_refs
    assert source.safety_gate_refs
    assert source.routing_refs
    assert source.provider_selection_refs
    assert source.provider_result_refs
    assert source.pig_guidance_refs
    assert source.failure_cause_refs
    assert source.raw_provider_output_included is False
    assert source.raw_transcript_included is False
    assert source.raw_secret_included is False
    assert source.private_full_path_included is False
    assert bundle.evidence_count >= 1
    assert bundle.provider_evidence_count >= 0
    assert bundle.policy_evidence_count >= 0
    assert bundle.uncertainty_evidence_count >= 0
    assert bundle.unsupported_evidence_count >= 0
    assert bundle.raw_provider_output_included is False
    assert bundle.raw_secret_included is False
    assert evidence.sanitized_summary
    assert evidence.supports_claim_refs
    assert evidence.confidence in {"low", "medium", "high", "unknown"}
    assert evidence.raw_content_included is False
    assert evidence.raw_provider_output_included is False
    assert evidence.raw_secret_included is False
    assert claim.claim_type
    assert claim.confidence in {"low", "medium", "high", "unknown"}
    assert claim.support_status in {"supported", "weakly_supported", "unsupported", "not_required", "unknown"}
    assert claim.raw_claim_content_included is False
    assert support.support_status in {"supported", "weakly_supported", "unsupported", "not_required", "unknown"}


def test_decision_skill_action_route_provider_safety_and_pig_views_are_non_executing() -> None:
    parts = _parts()

    for item in parts["decision_evidence_views"]:
        assert item.decision_type in {
            "intent_classification",
            "safety_gate",
            "no_action",
            "clarification",
            "needs_more_input",
            "blocked",
            "deferred",
            "allow_route",
            "route_selection",
            "provider_selection",
            "provider_invocation",
            "response_assembly",
            "emission",
            "unknown",
        }
        assert item.deterministic is True
        assert item.decision_mutated_now is False
        assert item.llm_judge_used is False
    for item in parts["skill_selection_evidence_views"]:
        assert item.skill_id == "skill:workbench_evidence_inspector_view"
        assert item.selected is True
        assert item.skill_executed_now is False
    for item in parts["action_candidate_evidence_views"]:
        assert item.evidence_bound is True
        assert item.action_executed_now is False
        assert item.approval_created_now is False
    for item in parts["route_selection_evidence_views"]:
        assert item.route_ref is not None
        assert item.route_rerun_now is False
    for item in parts["provider_selection_evidence_views"]:
        assert item.provider_id
        assert item.provider_invoked_now is False
        assert item.provider_test_run_performed is False
    for item in parts["safety_rationale_views"]:
        assert item.safety_gate_report_ref is not None
        assert item.safety_policy_mutated_now is False
    for item in parts["pig_guidance_views"]:
        assert item.guidance_summary
        assert item.pig_guidance_is_memory is False
        assert item.pig_guidance_mutates_policy is False
        assert item.pig_guidance_executes is False


def test_failure_unsupported_uncertainty_limitation_filter_selection_and_report_boundaries() -> None:
    parts = _parts()
    report = parts["report"]

    for item in parts["failure_cause_views"]:
        assert item.failure_category in {
            "missing_input",
            "safety_block",
            "provider_unavailable",
            "provider_warning",
            "provider_failed",
            "evidence_missing",
            "unsupported_claim",
            "boundary_violation",
            "route_failed",
            "response_assembly_failed",
            "unknown",
        }
        assert item.auto_rerun_enabled is False
        assert item.automatic_repair_enabled is False
    for item in parts["unsupported_claim_views"]:
        assert item.auto_corrected is False
        assert item.response_rewritten is False
    for item in parts["uncertainty_views"]:
        assert item.converted_to_certainty_now is False
    for item in parts["limitation_views"]:
        assert item.treated_as_failure is False
    assert parts["filter_state"].data_deleted is False
    assert parts["filter_state"].access_policy_mutated is False
    assert parts["selection_view"].selection_is_approval is False
    assert parts["selection_view"].selection_executes_now is False
    assert parts["selection_view"].raw_content_included is False
    assert parts["selection_view"].raw_secret_included is False
    assert parts["inspection_summary"].raw_provider_output_included is False
    assert parts["inspection_summary"].raw_transcript_included is False
    assert parts["inspection_summary"].raw_secret_included is False
    assert report.report_status in {"passed", "warning", "failed", "blocked"}
    assert report.ready_for_v0_26_5 is True
    assert report.ready_for_v0_27 is False
    assert report.actual_ui_rendered is False
    assert report.response_rewritten is False
    assert report.factuality_llm_judge_used is False
    assert report.decision_mutated is False
    assert report.safety_policy_mutated is False
    assert report.provider_invoked is False
    assert report.provider_test_run_performed is False
    assert report.route_rerun_performed is False
    assert report.stage_rerun_performed is False
    assert report.approval_executed is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.local_command_executed is False
    assert report.command_rerun_performed is False
    assert report.automatic_repair_performed is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.pm4py_runtime_dependency_added is False
    assert report.ocpa_runtime_dependency_added is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.26.5 Safety Gate / Approval Console"


def test_ocel_pig_ocpx_and_cli_outputs(capsys) -> None:
    service = WorkbenchEvidenceInspectorReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    for object_type in [
        "workbench_evidence_inspector_policy",
        "workbench_evidence_inspector_report",
        "workbench_claim_inspector_view",
        "workbench_pig_guidance_inspector_view",
    ]:
        assert object_type in WORKBENCH_EVIDENCE_INSPECTOR_OBJECT_TYPES
    for event_type in [
        "workbench_evidence_inspector_requested",
        "workbench_evidence_inspector_view_created",
        "workbench_evidence_inspector_report_created",
    ]:
        assert event_type in WORKBENCH_EVIDENCE_INSPECTOR_EVENT_TYPES
    for relation_type in [
        "uses_response_assembly_report",
        "creates_evidence_source_view",
        "not_response_rewritten",
        "not_provider_invoked",
    ]:
        assert relation_type in WORKBENCH_EVIDENCE_INSPECTOR_RELATION_TYPES
    assert "read_only_observation" in WORKBENCH_EVIDENCE_INSPECTOR_EFFECT_TYPES
    assert "workbench_evidence_inspector_created" in WORKBENCH_EVIDENCE_INSPECTOR_EFFECT_TYPES
    assert "provider_invoked" in WORKBENCH_EVIDENCE_INSPECTOR_FORBIDDEN_EFFECT_TYPES
    assert "response_rewritten" in WORKBENCH_EVIDENCE_INSPECTOR_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.4"
    assert pig["layer"] == "workspace_agent_workbench"
    assert pig["subject"] == "evidence_report_inspector"
    assert pig["safety_boundary"]["provider_invoked"] is False
    assert pig["safety_boundary"]["pig_executed"] is False
    assert ocpx["state"] == "workbench_evidence_report_inspector_created"
    assert "WorkbenchEvidenceInspectorViewState" in ocpx["target_read_models"]
    assert "WorkbenchUnsupportedClaimState" in ocpx["target_read_models"]

    assert main(["workbench", "evidence", "view"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.4" in output
    assert "evidence_inspector_view_created=true" in output
    assert "ready_for_v0_26_5=true" in output
    assert "ready_for_v0_27=false" in output
    assert "response_rewritten=false" in output
    assert "factuality_llm_judge_used=false" in output
    assert "provider_invoked=false" in output
    assert "route_rerun_performed=false" in output
    assert "approval_executed=false" in output
    assert "raw_provider_output_inline=false" in output
    assert "raw_transcript_persisted=false" in output
