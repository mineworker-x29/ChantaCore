from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench.snapshot_export import (
    WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES,
    WORKBENCH_SNAPSHOT_EXPORT_EVENT_TYPES,
    WORKBENCH_SNAPSHOT_EXPORT_FORBIDDEN_EFFECT_TYPES,
    WORKBENCH_SNAPSHOT_EXPORT_FUTURE_SKILL_IDS,
    WORKBENCH_SNAPSHOT_EXPORT_IMPLEMENTED_SKILL_IDS,
    WORKBENCH_SNAPSHOT_EXPORT_OBJECT_TYPES,
    WORKBENCH_SNAPSHOT_EXPORT_RELATION_TYPES,
    WORKBENCH_SNAPSHOT_EXPORT_VERSION,
    WorkbenchActionCandidateExportRef,
    WorkbenchApprovalDecisionExportRef,
    WorkbenchCommandCandidateExportRef,
    WorkbenchDecisionPointExportRef,
    WorkbenchEventQualityReport,
    WorkbenchExportBoundaryDescriptor,
    WorkbenchFailureCauseExportRef,
    WorkbenchHumanInterventionExportRef,
    WorkbenchOCELExportManifest,
    WorkbenchOCELExportPackage,
    WorkbenchOCELExportPolicy,
    WorkbenchPIGGuidanceExportRef,
    WorkbenchProviderRationaleExportRef,
    WorkbenchReproducibilityPacket,
    WorkbenchRouteRationaleExportRef,
    WorkbenchSafetyRationaleExportRef,
    WorkbenchSkillCandidateExportRef,
    WorkbenchSnapshot,
    WorkbenchSnapshotExportFinding,
    WorkbenchSnapshotExportReport,
    WorkbenchSnapshotExportReportService,
    WorkbenchSnapshotManifest,
    WorkbenchSnapshotPolicy,
    WorkbenchSnapshotRedactionPolicy,
    WorkbenchSnapshotRedactionReport,
    WorkbenchSnapshotRefBundle,
    WorkbenchSnapshotRequest,
    WorkbenchSnapshotSelection,
    WorkbenchSnapshotSelectionPolicy,
    WorkbenchSnapshotSourceView,
    WorkbenchTraceCoverageReport,
)


def _parts() -> dict:
    return WorkbenchSnapshotExportReportService().build_all_parts()


def test_snapshot_export_models_build() -> None:
    parts = _parts()

    assert isinstance(parts["snapshot_policy"], WorkbenchSnapshotPolicy)
    assert isinstance(parts["request"], WorkbenchSnapshotRequest)
    assert isinstance(parts["source_view"], WorkbenchSnapshotSourceView)
    assert isinstance(parts["selection_policy"], WorkbenchSnapshotSelectionPolicy)
    assert isinstance(parts["selection"], WorkbenchSnapshotSelection)
    assert isinstance(parts["snapshot"], WorkbenchSnapshot)
    assert isinstance(parts["snapshot_manifest"], WorkbenchSnapshotManifest)
    assert isinstance(parts["ref_bundle"], WorkbenchSnapshotRefBundle)
    assert isinstance(parts["ref_bundle"].decision_point_export_refs[0], WorkbenchDecisionPointExportRef)
    assert isinstance(parts["ref_bundle"].skill_candidate_export_refs[0], WorkbenchSkillCandidateExportRef)
    assert isinstance(parts["ref_bundle"].action_candidate_export_refs[0], WorkbenchActionCandidateExportRef)
    assert isinstance(parts["ref_bundle"].route_rationale_export_refs[0], WorkbenchRouteRationaleExportRef)
    assert isinstance(parts["ref_bundle"].provider_rationale_export_refs[0], WorkbenchProviderRationaleExportRef)
    assert isinstance(parts["ref_bundle"].safety_rationale_export_refs[0], WorkbenchSafetyRationaleExportRef)
    assert isinstance(parts["ref_bundle"].pig_guidance_export_refs[0], WorkbenchPIGGuidanceExportRef)
    assert isinstance(parts["ref_bundle"].human_intervention_export_refs[0], WorkbenchHumanInterventionExportRef)
    assert isinstance(parts["ref_bundle"].approval_decision_export_refs[0], WorkbenchApprovalDecisionExportRef)
    assert isinstance(parts["ref_bundle"].failure_cause_export_refs[0], WorkbenchFailureCauseExportRef)
    assert isinstance(parts["ref_bundle"].command_candidate_export_refs[0], WorkbenchCommandCandidateExportRef)
    assert isinstance(parts["ocel_export_policy"], WorkbenchOCELExportPolicy)
    assert isinstance(parts["ocel_export_package"], WorkbenchOCELExportPackage)
    assert isinstance(parts["ocel_export_manifest"], WorkbenchOCELExportManifest)
    assert isinstance(parts["event_quality_report"], WorkbenchEventQualityReport)
    assert isinstance(parts["trace_coverage_report"], WorkbenchTraceCoverageReport)
    assert isinstance(parts["redaction_policy"], WorkbenchSnapshotRedactionPolicy)
    assert isinstance(parts["redaction_report"], WorkbenchSnapshotRedactionReport)
    assert isinstance(parts["reproducibility_packet"], WorkbenchReproducibilityPacket)
    assert isinstance(parts["export_boundary_descriptor"], WorkbenchExportBoundaryDescriptor)
    assert isinstance(parts["findings"][0], WorkbenchSnapshotExportFinding)
    assert isinstance(parts["report"], WorkbenchSnapshotExportReport)


def test_policy_source_and_selection_are_refs_only() -> None:
    parts = _parts()
    policy = parts["snapshot_policy"]
    source = parts["source_view"]
    selection_policy = parts["selection_policy"]
    selection = parts["selection"]

    assert WORKBENCH_SNAPSHOT_EXPORT_VERSION == "v0.26.8"
    assert WORKBENCH_SNAPSHOT_EXPORT_IMPLEMENTED_SKILL_IDS == [
        "skill:workbench_snapshot_create",
        "skill:workbench_ocel_export_create",
    ]
    assert WORKBENCH_SNAPSHOT_EXPORT_FUTURE_SKILL_IDS == ["skill:workbench_consolidation_view"]
    assert policy.snapshot_enabled is True
    assert policy.ocel_export_enabled is True
    assert policy.reproducibility_packet_enabled is True
    assert policy.event_quality_report_enabled is True
    assert policy.trace_coverage_report_enabled is True
    assert policy.redaction_report_enabled is True
    assert policy.memory_promotion_enabled is False
    assert policy.persistent_memory_write_enabled is False
    assert policy.memory_candidate_extraction_enabled is False
    assert policy.persona_mutation_enabled is False
    assert policy.external_sync_enabled is False
    assert policy.external_adapter_enabled is False
    assert policy.pm4py_runtime_dependency_enabled is False
    assert policy.ocpa_runtime_dependency_enabled is False
    assert policy.command_execution_enabled is False
    assert policy.provider_invocation_enabled is False
    assert policy.local_runtime_execution_enabled is False
    assert policy.file_mutation_enabled is False
    assert policy.ask_execution_enabled is False
    assert policy.response_emission_enabled is False
    assert policy.route_rerun_enabled is False
    assert policy.stage_rerun_enabled is False
    assert policy.automatic_retry_enabled is False
    assert policy.automatic_repair_enabled is False
    assert policy.autonomous_loop_enabled is False
    assert policy.refs_only_by_default is True
    assert policy.raw_transcript_export_forbidden is True
    assert policy.raw_provider_output_export_forbidden is True
    assert policy.raw_secret_export_forbidden is True
    assert policy.credential_export_forbidden is True
    assert policy.private_full_path_export_forbidden is True
    assert policy.pig_guidance_is_not_memory is True
    assert policy.pig_guidance_is_not_policy_mutation is True
    assert policy.pig_guidance_is_not_execution is True
    assert source.workbench_report_refs
    assert source.command_candidate_refs
    assert source.decision_point_refs
    assert source.skill_candidate_refs
    assert source.action_candidate_refs
    assert source.route_rationale_refs
    assert source.provider_rationale_refs
    assert source.safety_rationale_refs
    assert source.pig_guidance_refs
    assert source.human_intervention_refs
    assert source.approval_decision_refs
    assert source.failure_cause_refs
    assert source.trace_refs
    assert source.raw_provider_output_included is False
    assert source.raw_transcript_included is False
    assert source.raw_secret_included is False
    assert source.private_full_path_included is False
    assert selection_policy.selection_is_not_memory_candidate is True
    assert selection_policy.selection_is_not_memory_promotion is True
    assert selection_policy.refs_only_selection_required is True
    assert selection.selected_refs
    assert selection.memory_candidate_created is False
    assert selection.memory_promoted is False
    assert selection.raw_content_selected is False


def test_snapshot_manifest_ref_bundle_and_export_refs_are_safe() -> None:
    parts = _parts()
    snapshot = parts["snapshot"]
    manifest = parts["snapshot_manifest"]
    bundle = parts["ref_bundle"]

    assert snapshot.refs_only is True
    assert snapshot.memory_promoted is False
    assert snapshot.persistent_memory_written is False
    assert snapshot.raw_transcript_included is False
    assert snapshot.raw_provider_output_included is False
    assert snapshot.raw_secret_included is False
    assert snapshot.credential_included is False
    assert snapshot.private_full_path_included is False
    assert manifest.included_report_refs
    assert manifest.included_trace_refs
    assert manifest.included_decision_point_refs
    assert manifest.included_candidate_refs
    assert manifest.included_approval_refs
    assert manifest.included_failure_refs
    assert manifest.included_pig_guidance_refs
    assert "raw_transcripts" in manifest.excluded_raw_data_categories
    assert "raw_provider_outputs" in manifest.excluded_raw_data_categories
    assert "raw_secrets" in manifest.excluded_raw_data_categories
    assert "credentials" in manifest.excluded_raw_data_categories
    assert "private_full_paths" in manifest.excluded_raw_data_categories
    assert manifest.is_memory_index is False
    assert bundle.ref_count > 0
    assert bundle.raw_content_included is False

    assert bundle.skill_candidate_export_refs[0].skill_executed_now is False
    assert bundle.action_candidate_export_refs[0].action_executed_now is False
    assert bundle.route_rationale_export_refs[0].route_executed_now is False
    provider = bundle.provider_rationale_export_refs[0]
    assert provider.provider_invoked_now is False
    assert provider.raw_provider_output_included is False
    assert bundle.safety_rationale_export_refs[0].safety_policy_mutated_now is False
    pig = bundle.pig_guidance_export_refs[0]
    assert pig.pig_guidance_is_memory is False
    assert pig.pig_guidance_mutates_policy is False
    assert pig.pig_guidance_executes is False
    assert bundle.human_intervention_export_refs[0].execution_triggered_now is False
    assert bundle.approval_decision_export_refs[0].execution_triggered is False
    assert bundle.failure_cause_export_refs[0].automatic_repair_enabled is False
    assert bundle.failure_cause_export_refs[0].auto_retry_enabled is False
    assert bundle.command_candidate_export_refs[0].command_executed_now is False


def test_ocel_export_quality_coverage_redaction_reproducibility_boundary() -> None:
    parts = _parts()
    export_policy = parts["ocel_export_policy"]
    package = parts["ocel_export_package"]
    quality = parts["event_quality_report"]
    coverage = parts["trace_coverage_report"]
    redaction_policy = parts["redaction_policy"]
    redaction = parts["redaction_report"]
    reproducibility = parts["reproducibility_packet"]
    boundary = parts["export_boundary_descriptor"]

    assert export_policy.export_refs_only is True
    assert export_policy.mutate_original_artifacts is False
    assert export_policy.external_sync_enabled is False
    assert export_policy.external_adapter_enabled is False
    assert export_policy.raw_transcript_export_forbidden is True
    assert export_policy.raw_provider_output_export_forbidden is True
    assert export_policy.raw_secret_export_forbidden is True
    assert export_policy.credential_export_forbidden is True
    assert export_policy.private_full_path_export_forbidden is True
    assert export_policy.pm4py_runtime_dependency_enabled is False
    assert export_policy.ocpa_runtime_dependency_enabled is False
    assert package.object_type_refs
    assert package.event_type_refs
    assert package.relation_type_refs
    assert package.effect_type_refs
    assert package.refs_only is True
    assert package.external_sync_performed is False
    assert package.raw_transcript_exported is False
    assert package.raw_provider_output_exported is False
    assert package.raw_secret_exported is False
    assert package.credential_exported is False
    assert quality.decision_point_coverage is not None
    assert quality.automatic_optimization_performed is False
    assert coverage.trace_ref_count >= 1
    assert coverage.command_trace_coverage is True
    assert redaction_policy.redact_raw_transcripts is True
    assert redaction_policy.redact_raw_provider_outputs is True
    assert redaction_policy.redact_raw_secrets is True
    assert redaction_policy.redact_credentials is True
    assert redaction_policy.redact_private_full_paths is True
    assert redaction.redacted_raw_transcript_count >= 1
    assert redaction.redacted_raw_provider_output_count >= 1
    assert redaction.redacted_raw_secret_count >= 1
    assert redaction.redacted_credential_count >= 1
    assert redaction.redacted_private_path_count >= 1
    assert redaction.preserved_ref_count >= 1
    assert reproducibility.rerun_permission_granted is False
    assert reproducibility.rerun_performed is False
    assert reproducibility.provider_invoked is False
    assert reproducibility.command_executed is False
    assert boundary.external_adapter_invoked is False
    assert boundary.pm4py_runtime_dependency_used is False
    assert boundary.ocpa_runtime_dependency_used is False


def test_report_ocel_pig_ocpx_and_cli_outputs(capsys) -> None:
    service = WorkbenchSnapshotExportReportService()
    parts = _parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_26_9 is True
    assert report.ready_for_v0_27 is False
    assert report.snapshot_created is True
    assert report.snapshot_manifest_created is True
    assert report.ref_bundle_created is True
    assert report.ocel_export_package_created is True
    assert report.ocel_export_manifest_created is True
    assert report.event_quality_report_created is True
    assert report.trace_coverage_report_created is True
    assert report.redaction_report_created is True
    assert report.reproducibility_packet_created is True
    assert report.export_boundary_descriptor_created is True
    assert report.memory_candidate_created is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.raw_transcript_exported is False
    assert report.raw_provider_output_exported is False
    assert report.raw_secret_exported is False
    assert report.credential_exported is False
    assert report.private_full_path_exported is False
    assert report.external_sync_performed is False
    assert report.pm4py_runtime_dependency_added is False
    assert report.ocpa_runtime_dependency_added is False
    assert report.command_executed is False
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
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.schumpeter_split_introduced is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.26.9 Workspace Agent Workbench Consolidation"
    assert "workbench_snapshot" in WORKBENCH_SNAPSHOT_EXPORT_OBJECT_TYPES
    assert "workbench_snapshot_created" in WORKBENCH_SNAPSHOT_EXPORT_EVENT_TYPES
    assert "creates_workbench_snapshot" in WORKBENCH_SNAPSHOT_EXPORT_RELATION_TYPES
    assert "workbench_snapshot_created" in WORKBENCH_SNAPSHOT_EXPORT_EFFECT_TYPES
    assert "memory_promoted" in WORKBENCH_SNAPSHOT_EXPORT_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.26.8"
    assert pig["subject"] == "workbench_snapshot_ocel_export"
    assert pig["safety_boundary"]["memory_promoted"] is False
    assert ocpx["state"] == "workbench_snapshot_ocel_export_created"
    assert "WorkbenchSnapshotState" in ocpx["target_read_models"]
    assert "WorkbenchExportBoundaryDescriptorState" in ocpx["target_read_models"]

    assert main(["workbench", "snapshot", "create"]) == 0
    output = capsys.readouterr().out
    assert "version=v0.26.8" in output
    assert "snapshot_created=true" in output
    assert "ready_for_v0_26_9=true" in output
    assert "ready_for_v0_27=false" in output
    assert "memory_promoted=false" in output
    assert "raw_transcript_exported=false" in output
    assert "raw_provider_output_exported=false" in output
    assert "external_sync_performed=false" in output
    assert "pm4py_runtime_dependency_added=false" in output
    assert "ocpa_runtime_dependency_added=false" in output
    assert "command_executed=false" in output
    assert "provider_invoked=false" in output
    assert "llm_judge_used=false" in output
