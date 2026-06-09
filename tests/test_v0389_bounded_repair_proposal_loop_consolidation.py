import inspect

import pytest

from chanta_core.agent_runtime import (
    DigestionDominionRepairConsolidationRecord,
    RepairCLISurfaceConsolidationRecord,
    RepairCLISurfaceCoverage,
    RepairEvidenceConsolidationRecord,
    RepairHumanReviewConsolidationRecord,
    RepairHumanReviewCoverage,
    RepairLoopTrialConsolidationRecord,
    RepairLoopTrialCoverage,
    RepairPatchMetadataConsolidationRecord,
    RepairPatchMetadataCoverage,
    RepairProposalAuditTrail,
    RepairProposalBoundaryCoverage,
    RepairProposalBoundaryRegister,
    RepairProposalCapabilityMatrix,
    RepairProposalConsolidationReadinessLevel,
    RepairProposalConsolidationStatus,
    RepairProposalEvidenceCoverage,
    RepairProposalGapRegister,
    RepairProposalLoopSnapshot,
    RepairProposalReleaseFlagSet,
    RepairProposalReleaseManifest,
    RepairProposalStageCoverage,
    RepairSafetyValidationConsolidationRecord,
    RepairSafetyValidationCoverage,
    RepairScopePlanningConsolidationRecord,
    RepairScopePlanningCoverage,
    RepairSourceContextConsolidationRecord,
    RepairSourceContextCoverage,
    V038ConsolidationReport,
    V039HandoffPacket,
    build_digestion_dominion_repair_consolidation_record,
    build_repair_cli_surface_consolidation_record,
    build_repair_cli_surface_coverage,
    build_repair_evidence_consolidation_record,
    build_repair_human_review_consolidation_record,
    build_repair_human_review_coverage,
    build_repair_loop_trial_consolidation_record,
    build_repair_loop_trial_coverage,
    build_repair_patch_metadata_consolidation_record,
    build_repair_patch_metadata_coverage,
    build_repair_proposal_audit_trail,
    build_repair_proposal_boundary_coverage,
    build_repair_proposal_boundary_register,
    build_repair_proposal_capability_matrix,
    build_repair_proposal_evidence_coverage,
    build_repair_proposal_gap_register,
    build_repair_proposal_loop_snapshot,
    build_repair_proposal_release_flags,
    build_repair_proposal_release_manifest,
    build_repair_proposal_stage_coverage,
    build_repair_safety_validation_consolidation_record,
    build_repair_safety_validation_coverage,
    build_repair_scope_planning_consolidation_record,
    build_repair_scope_planning_coverage,
    build_repair_source_context_consolidation_record,
    build_repair_source_context_coverage,
    build_v038_consolidation_report,
    build_v039_handoff_packet,
    repair_proposal_audit_confirms_no_runtime,
    repair_proposal_capability_matrix_is_not_permission_grant,
    repair_proposal_release_flags_preserve_no_runtime,
    repair_proposal_snapshot_is_not_runtime,
    repair_stage_consolidation_record_is_not_runtime,
    v038_consolidation_report_is_not_execution_ready,
    v039_handoff_packet_is_future_track_only,
)
from chanta_core.agent_runtime import repair_proposal_consolidation as consolidation_module


EXPECTED_STATUS_VALUES = {
    "unknown",
    "not_started",
    "in_progress",
    "consolidated",
    "consolidated_with_gaps",
    "blocked",
    "future_track",
    "no_op",
}

EXPECTED_READINESS_VALUES = {
    "not_ready",
    "boundary_ready",
    "evidence_source_scope_ready",
    "patch_metadata_ready",
    "safety_review_ready",
    "loop_cli_surface_ready",
    "bounded_repair_proposal_loop_v1_ready",
    "handoff_ready_for_v039",
    "blocked",
    "future_track",
}

EXPECTED_INCLUDED_VERSIONS = {
    "v0.38.0",
    "v0.38.1",
    "v0.38.2",
    "v0.38.3",
    "v0.38.4",
    "v0.38.5",
    "v0.38.6",
    "v0.38.7",
    "v0.38.8",
}

SAFE_RELEASE_TRUE_FIELDS = {
    "bounded_repair_proposal_loop_v1_ready",
    "ready_for_v039_handoff",
    "ready_for_v039_human_approved_sandbox_repair_apply_contract_input",
    "ready_for_repair_proposal_boundary",
    "ready_for_repair_evidence_contract",
    "ready_for_repair_evidence_bundle",
    "ready_for_repair_evidence_assessment",
    "ready_for_read_only_sandbox_source_context",
    "ready_for_validated_read_only_sandbox_source_read",
    "ready_for_source_context_snapshot",
    "ready_for_bounded_source_excerpt",
    "ready_for_repair_scope_planning",
    "ready_for_repair_change_intent_model",
    "ready_for_affected_file_candidates",
    "ready_for_affected_symbol_candidates",
    "ready_for_proposed_diff_metadata",
    "ready_for_proposed_code_hunk_metadata",
    "ready_for_proposed_patch_envelope_metadata",
    "ready_for_repair_proposal_safety_validation",
    "ready_for_static_patch_metadata_validation",
    "ready_for_boundary_violation_scan",
    "ready_for_unsafe_operation_detection",
    "ready_for_human_review_packet",
    "ready_for_approval_request_contract",
    "ready_for_review_checklist",
    "ready_for_apply_precondition_metadata",
    "ready_for_one_shot_repair_proposal_loop_trial",
    "ready_for_one_shot_loop_packet",
    "ready_for_loop_artifact_bundle",
    "ready_for_loop_step_records",
    "ready_for_loop_stop_condition",
    "ready_for_cli_repair_proposal_surface",
    "ready_for_cli_command_registry",
    "ready_for_cli_argument_parsing",
    "ready_for_cli_preview",
}


def _unsafe_release_fields():
    flags = build_repair_proposal_release_flags()
    return [
        name
        for name, value in flags.__dict__.items()
        if isinstance(value, bool) and name not in SAFE_RELEASE_TRUE_FIELDS
    ]


def test_consolidation_taxonomies_include_required_values():
    assert {item.value for item in RepairProposalConsolidationStatus} == EXPECTED_STATUS_VALUES
    assert {item.value for item in RepairProposalConsolidationReadinessLevel} == EXPECTED_READINESS_VALUES


def test_release_flags_allow_bounded_metadata_readiness_only():
    flags = build_repair_proposal_release_flags()
    assert isinstance(flags, RepairProposalReleaseFlagSet)
    assert flags.version == "v0.38.9"
    assert flags.bounded_repair_proposal_loop_v1_ready is True
    assert flags.ready_for_v039_handoff is True
    assert flags.ready_for_v039_human_approved_sandbox_repair_apply_contract_input is True
    assert {"D4", "D5", "D6", "D7", "D8", "D9"}.issubset(set(flags.future_track_levels))
    assert flags.production_certified is False
    assert flags.max_grantable_level is None
    assert repair_proposal_release_flags_preserve_no_runtime(flags)
    for field_name in _unsafe_release_fields():
        assert getattr(flags, field_name) is False


@pytest.mark.parametrize(
    "unsafe_field",
    [
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_repair_execution",
        "ready_for_sandbox_repair_apply",
        "ready_for_human_approval_capture",
        "ready_for_approval_grant",
        "ready_for_apply_permission",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_model_provider_invocation",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_release_flags_reject_unsafe_true_values(unsafe_field):
    with pytest.raises(ValueError):
        build_repair_proposal_release_flags(**{unsafe_field: True})


def test_loop_snapshot_includes_all_v038_versions_and_is_not_runtime():
    snapshot = build_repair_proposal_loop_snapshot()
    assert isinstance(snapshot, RepairProposalLoopSnapshot)
    assert set(snapshot.included_versions).issuperset(EXPECTED_INCLUDED_VERSIONS)
    assert snapshot.release_name == "Bounded Repair Proposal Loop v1"
    assert "repair_execution" in snapshot.prohibited_capabilities
    assert repair_proposal_snapshot_is_not_runtime(snapshot)

    with pytest.raises(ValueError):
        build_repair_proposal_loop_snapshot(included_versions=["v0.38.8"])


def test_capability_matrix_records_enabled_and_prohibited_capabilities():
    matrix = build_repair_proposal_capability_matrix()
    assert isinstance(matrix, RepairProposalCapabilityMatrix)
    assert "proposed_diff_metadata" in matrix.enabled_capabilities
    for prohibited in [
        "live_workspace_read",
        "unbounded_source_read",
        "source_write",
        "patch_file_write",
        "file_edit",
        "patch_application",
        "human_approval_capture",
        "repair_execution",
        "test_execution",
        "shell_execution",
        "subprocess_execution",
        "dependency_install",
        "network_access",
        "model_provider_invocation",
        "external_agent_execution",
        "dominion_runtime",
        "production_certification",
    ]:
        assert prohibited in matrix.prohibited_capabilities
    assert repair_proposal_capability_matrix_is_not_permission_grant(matrix)


def test_coverage_records_exist_for_all_v038_stages():
    builders_and_types = [
        (build_repair_proposal_stage_coverage, RepairProposalStageCoverage),
        (build_repair_proposal_boundary_coverage, RepairProposalBoundaryCoverage),
        (build_repair_proposal_evidence_coverage, RepairProposalEvidenceCoverage),
        (build_repair_source_context_coverage, RepairSourceContextCoverage),
        (build_repair_scope_planning_coverage, RepairScopePlanningCoverage),
        (build_repair_patch_metadata_coverage, RepairPatchMetadataCoverage),
        (build_repair_safety_validation_coverage, RepairSafetyValidationCoverage),
        (build_repair_human_review_coverage, RepairHumanReviewCoverage),
        (build_repair_loop_trial_coverage, RepairLoopTrialCoverage),
        (build_repair_cli_surface_coverage, RepairCLISurfaceCoverage),
    ]
    for builder, expected_type in builders_and_types:
        coverage = builder()
        assert isinstance(coverage, expected_type)
        assert coverage.coverage_complete is True
        assert "production certification" not in " ".join(coverage.coverage_notes).lower()

    with pytest.raises(ValueError):
        build_repair_proposal_stage_coverage(coverage_complete=True, blocking_gaps=["missing safety coverage"])


def test_boundary_risk_and_gap_registers_include_unsafe_surfaces_and_v039_items():
    boundary = build_repair_proposal_boundary_register()
    assert isinstance(boundary, RepairProposalBoundaryRegister)
    for item in ["live_read", "source_write", "patch_application", "apply_patch", "git_apply", "approval_capture", "repair_execution", "test_execution", "shell_execution", "subprocess_execution", "network_access", "model_provider_invocation", "external_agent_execution", "dominion_runtime", "authority_grant"]:
        assert item in boundary.prohibited_boundaries

    risk = consolidation_module.build_repair_proposal_risk_register()
    assert isinstance(risk, consolidation_module.RepairProposalRiskRegister)
    for item in ["source_write", "patch_apply", "repair_execution", "approval_capture", "test_execution", "shell", "subprocess", "install", "network", "model", "external_agent", "Dominion"]:
        assert item in risk.prohibited_runtime_surfaces

    gap = build_repair_proposal_gap_register()
    assert isinstance(gap, RepairProposalGapRegister)
    for item in [
        "human-approved sandbox apply boundary",
        "approval artifact validation",
        "sandbox-only patch application",
        "controlled re-test",
        "before/after comparison",
        "cold repair evaluation",
        "rollback/discard metadata",
    ]:
        assert item in gap.recommended_v039_items
    for item in ["live apply gate", "persistent trace store", "UI runtime", "external harness adapter", "Dominion runtime gated review"]:
        assert item in gap.future_track_items


def test_release_manifest_is_not_production_release():
    manifest = build_repair_proposal_release_manifest()
    assert isinstance(manifest, RepairProposalReleaseManifest)
    assert set(manifest.included_versions).issuperset(EXPECTED_INCLUDED_VERSIONS)
    assert manifest.release_name == "Bounded Repair Proposal Loop v1"
    assert repair_proposal_release_flags_preserve_no_runtime(manifest.release_flags)


def test_audit_trail_requires_all_no_runtime_confirmations_true():
    audit = build_repair_proposal_audit_trail()
    assert isinstance(audit, RepairProposalAuditTrail)
    assert audit.bounded_sandbox_source_read_scoped_to_v0382_confirmed is True
    assert audit.no_patch_application_confirmed is True
    assert audit.no_approval_capture_confirmed is True
    assert audit.no_test_execution_confirmed is True
    assert audit.one_shot_loop_only_confirmed is True
    assert audit.cli_preview_only_confirmed is True
    assert repair_proposal_audit_confirms_no_runtime(audit)

    with pytest.raises(ValueError):
        build_repair_proposal_audit_trail(no_patch_application_confirmed=False)


def test_stage_consolidation_records_exist_and_are_not_runtime_permissions():
    builders_and_types = [
        (build_repair_evidence_consolidation_record, RepairEvidenceConsolidationRecord),
        (build_repair_source_context_consolidation_record, RepairSourceContextConsolidationRecord),
        (build_repair_scope_planning_consolidation_record, RepairScopePlanningConsolidationRecord),
        (build_repair_patch_metadata_consolidation_record, RepairPatchMetadataConsolidationRecord),
        (build_repair_safety_validation_consolidation_record, RepairSafetyValidationConsolidationRecord),
        (build_repair_human_review_consolidation_record, RepairHumanReviewConsolidationRecord),
        (build_repair_loop_trial_consolidation_record, RepairLoopTrialConsolidationRecord),
        (build_repair_cli_surface_consolidation_record, RepairCLISurfaceConsolidationRecord),
        (build_digestion_dominion_repair_consolidation_record, DigestionDominionRepairConsolidationRecord),
    ]
    for builder, expected_type in builders_and_types:
        record = builder()
        assert isinstance(record, expected_type)
        assert repair_stage_consolidation_record_is_not_runtime(record)
        assert "repair_execution" in record.blocked_capabilities

    with pytest.raises(ValueError):
        build_repair_evidence_consolidation_record(confirmation_booleans={"no_runtime_permission_granted": False})


def test_v039_handoff_packet_is_future_track_metadata_only():
    handoff = build_v039_handoff_packet()
    assert isinstance(handoff, V039HandoffPacket)
    assert "v0.38.9" in handoff.source_version
    assert "v0.39" in handoff.target_version_track
    assert "Human-approved Sandbox Repair Apply & Re-test Loop" in handoff.recommended_next_track
    assert handoff.ready_for_v039 is True
    assert handoff.ready_for_execution is False
    assert handoff.ready_for_apply_permission is False
    assert handoff.ready_for_sandbox_repair_apply is False
    assert handoff.ready_for_patch_application is False
    assert handoff.ready_for_test_execution is False
    assert handoff.ready_for_shell_execution is False
    assert handoff.ready_for_network_access is False
    assert handoff.ready_for_model_provider_invocation is False
    assert handoff.ready_for_external_agent_execution is False
    assert handoff.ready_for_dominion_runtime is False
    assert v039_handoff_packet_is_future_track_only(handoff)
    for item in ["approval artifact validation", "sandbox-only patch application contract", "controlled re-test", "before/after result comparison", "cold repair improvement evaluation", "rollback metadata"]:
        assert item in " ".join(
            handoff.approval_artifact_validation_items
            + handoff.sandbox_patch_application_contract_items
            + handoff.post_apply_test_items
            + handoff.before_after_comparison_items
            + handoff.cold_repair_evaluation_items
            + handoff.rollback_discard_items
        )

    with pytest.raises(ValueError):
        build_v039_handoff_packet(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v039_handoff_packet(ready_for_apply_permission=True)
    with pytest.raises(ValueError):
        build_v039_handoff_packet(ready_for_sandbox_repair_apply=True)


def test_v038_consolidation_report_is_not_execution_ready():
    report = build_v038_consolidation_report()
    assert isinstance(report, V038ConsolidationReport)
    assert report.ready_for_bounded_repair_proposal_loop_v1 is True
    assert report.ready_for_repair_proposal_boundary is True
    assert report.ready_for_repair_evidence_contract is True
    assert report.ready_for_read_only_sandbox_source_context is True
    assert report.ready_for_repair_scope_planning is True
    assert report.ready_for_proposed_diff_metadata is True
    assert report.ready_for_proposed_code_hunk_metadata is True
    assert report.ready_for_proposed_patch_envelope_metadata is True
    assert report.ready_for_repair_proposal_safety_validation is True
    assert report.ready_for_human_review_packet is True
    assert report.ready_for_approval_request_contract is True
    assert report.ready_for_one_shot_repair_proposal_loop_trial is True
    assert report.ready_for_cli_repair_proposal_surface is True
    assert report.ready_for_execution is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_apply_patch is False
    assert report.ready_for_git_apply is False
    assert report.ready_for_repair_execution is False
    assert report.ready_for_test_execution is False
    assert report.ready_for_human_approval_capture is False
    assert report.ready_for_approval_grant is False
    assert report.ready_for_apply_permission is False
    assert report.ready_for_model_provider_invocation is False
    assert report.ready_for_external_agent_execution is False
    assert report.ready_for_dominion_runtime is False
    assert report.production_certified is False
    assert v038_consolidation_report_is_not_execution_ready(report)

    with pytest.raises(ValueError):
        build_v038_consolidation_report(ready_for_repair_execution=True)


def test_helpers_are_pure_and_do_not_contain_runtime_patterns():
    source = inspect.getsource(consolidation_module)
    forbidden_patterns = [
        "Path.read_text",
        "Path.read_bytes",
        "open(",
        "write_text",
        "write_bytes",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "approval_granted=True",
        "production_certified=True",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source
