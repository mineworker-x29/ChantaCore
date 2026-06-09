from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    ApplyCandidateCoverage,
    BoundedAgenticOperationConsolidationRecord,
    BoundedAgenticOperationCoverage,
    CLISandboxApplySurfaceCoverage,
    DigestionDominionSandboxConsolidationRecord,
    DryRunApplyCoverage,
    ExternalAgentControlSandboxConsolidationRecord,
    PatchApplyBoundaryCoverage,
    PatchApplySandboxAuditTrail,
    PatchApplySandboxBoundaryRegister,
    PatchApplySandboxCapabilityMatrix,
    PatchApplySandboxConsolidationReadinessLevel,
    PatchApplySandboxConsolidationStatus,
    PatchApplySandboxGapRegister,
    PatchApplySandboxReleaseFlagSet,
    PatchApplySandboxReleaseManifest,
    PatchApplySandboxRiskRegister,
    PatchApplySandboxSnapshot,
    PatchApplySandboxStageCoverage,
    PatchApplyTraceCoverage,
    SandboxPatchApplyCoverage,
    SandboxPostApplyValidationCoverage,
    SandboxWorkspaceCoverage,
    V036ConsolidationReport,
    V037HandoffPacket,
    bounded_agentic_consolidation_record_is_not_autonomous_runtime,
    build_apply_candidate_coverage,
    build_bounded_agentic_operation_consolidation_record,
    build_bounded_agentic_operation_coverage,
    build_cli_sandbox_apply_surface_coverage,
    build_digestion_dominion_sandbox_consolidation_record,
    build_dry_run_apply_coverage,
    build_external_agent_control_sandbox_consolidation_record,
    build_patch_apply_boundary_coverage,
    build_patch_apply_sandbox_audit_trail,
    build_patch_apply_sandbox_boundary_register,
    build_patch_apply_sandbox_capability_matrix,
    build_patch_apply_sandbox_gap_register,
    build_patch_apply_sandbox_release_flags,
    build_patch_apply_sandbox_release_manifest,
    build_patch_apply_sandbox_risk_register,
    build_patch_apply_sandbox_snapshot,
    build_patch_apply_sandbox_stage_coverage,
    build_patch_apply_trace_coverage,
    build_sandbox_patch_apply_coverage,
    build_sandbox_post_apply_validation_coverage,
    build_sandbox_workspace_coverage,
    build_v036_consolidation_report,
    build_v037_handoff_packet,
    digestion_dominion_sandbox_record_is_not_runtime,
    external_agent_control_sandbox_record_is_not_execution,
    patch_apply_sandbox_audit_confirms_no_unsafe_runtime,
    patch_apply_sandbox_capability_matrix_is_not_permission_grant,
    patch_apply_sandbox_flags_preserve_no_live_apply,
    patch_apply_sandbox_snapshot_is_not_live_runtime,
    v036_consolidation_report_is_not_runtime_ready,
    v037_handoff_packet_is_design_stage_only,
)


V036_VERSIONS = {f"v0.36.{index}" for index in range(9)}


SAFE_FLAG_NAMES = {
    "ready_for_v037_handoff",
    "ready_for_apply_sandbox_boundary",
    "ready_for_apply_candidate_human_approval_contract",
    "ready_for_human_approval_evidence_validation",
    "ready_for_dry_run_apply_simulation",
    "ready_for_dry_run_hunk_alignment",
    "ready_for_sandbox_workspace_policy",
    "ready_for_sandbox_workspace_manifest",
    "ready_for_sandbox_workspace_materialization",
    "ready_for_sandbox_workspace_write",
    "ready_for_sandbox_patch_apply",
    "ready_for_sandbox_patch_apply_result",
    "ready_for_sandbox_post_apply_validation",
    "ready_for_sandbox_reconciliation_report",
    "ready_for_sandbox_safety_regression_scan",
    "ready_for_sandbox_scope_validation",
    "ready_for_bounded_agentic_task_operation_cycle",
    "ready_for_agentic_function_task_execution",
    "ready_for_single_cycle_operation_packet",
    "ready_for_human_handoff_after_cycle",
    "ready_for_patch_apply_sandbox_trace_packet_creation",
    "ready_for_bounded_patch_apply_ocel_trace_emission",
    "ready_for_cli_sandbox_apply_surface",
    "ready_for_cli_sandbox_apply_run",
    "ready_for_cli_agentic_task_run_once",
}


def _unsafe_flag_names(cls):
    return [field.name for field in fields(cls) if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES]


def test_status_and_readiness_taxonomies():
    assert {item.value for item in PatchApplySandboxConsolidationStatus} == {
        "unknown",
        "not_started",
        "in_progress",
        "consolidated",
        "consolidated_with_gaps",
        "blocked",
        "future_track",
        "no_op",
    }
    assert {item.value for item in PatchApplySandboxConsolidationReadinessLevel} == {
        "not_ready",
        "contract_ready",
        "human_approved_patch_apply_sandbox_ready",
        "sandbox_apply_workflow_ready",
        "bounded_agentic_task_ready",
        "cli_sandbox_apply_surface_ready",
        "handoff_ready_for_v037",
        "blocked",
        "future_track",
    }


def test_required_models_are_exported():
    for model in (
        PatchApplySandboxReleaseFlagSet,
        PatchApplySandboxSnapshot,
        PatchApplySandboxCapabilityMatrix,
        PatchApplySandboxStageCoverage,
        PatchApplyBoundaryCoverage,
        ApplyCandidateCoverage,
        DryRunApplyCoverage,
        SandboxWorkspaceCoverage,
        SandboxPatchApplyCoverage,
        SandboxPostApplyValidationCoverage,
        BoundedAgenticOperationCoverage,
        PatchApplyTraceCoverage,
        CLISandboxApplySurfaceCoverage,
        PatchApplySandboxBoundaryRegister,
        PatchApplySandboxRiskRegister,
        PatchApplySandboxGapRegister,
        PatchApplySandboxReleaseManifest,
        PatchApplySandboxAuditTrail,
        BoundedAgenticOperationConsolidationRecord,
        DigestionDominionSandboxConsolidationRecord,
        ExternalAgentControlSandboxConsolidationRecord,
        V037HandoffPacket,
        V036ConsolidationReport,
    ):
        assert model is not None


def test_release_flags_allow_sandbox_readiness_and_preserve_unsafe_false():
    flags = build_patch_apply_sandbox_release_flags()
    assert flags.human_approved_patch_apply_sandbox_v1_ready
    assert flags.ready_for_v037_handoff
    assert flags.ready_for_apply_candidate_human_approval_contract
    assert flags.ready_for_dry_run_apply_simulation
    assert flags.ready_for_sandbox_workspace_policy
    assert flags.ready_for_sandbox_workspace_materialization
    assert flags.ready_for_sandbox_workspace_write
    assert flags.ready_for_sandbox_patch_apply
    assert flags.ready_for_sandbox_post_apply_validation
    assert flags.ready_for_bounded_agentic_task_operation_cycle
    assert flags.ready_for_patch_apply_sandbox_trace_packet_creation
    assert flags.ready_for_cli_sandbox_apply_surface
    assert flags.ready_for_cli_sandbox_apply_run
    assert patch_apply_sandbox_flags_preserve_no_live_apply(flags)
    assert flags.production_certified is False
    for name in _unsafe_flag_names(PatchApplySandboxReleaseFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False
    assert flags.max_grantable_level == "D3_SIMULATE"
    for level in ("D4", "D5", "D6", "D7", "D8", "D9"):
        assert any(item.startswith(level) for item in flags.future_track_levels)


@pytest.mark.parametrize(
    "field_name",
    _unsafe_flag_names(PatchApplySandboxReleaseFlagSet) + ["production_certified"],
)
def test_release_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_release_flags(**{field_name: True})


def test_snapshot_includes_v0360_through_v0368_and_is_not_runtime_expansion():
    snapshot = build_patch_apply_sandbox_snapshot()
    assert V036_VERSIONS.issubset(set(snapshot.included_versions))
    assert "Human-approved Patch Apply Sandbox v1" in snapshot.release_name
    assert patch_apply_sandbox_snapshot_is_not_live_runtime(snapshot)
    assert "live_workspace_write" in snapshot.prohibited_capabilities
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_snapshot(included_versions=["v0.36.8"])


def test_capability_matrix_lists_enabled_and_prohibited_capabilities():
    matrix = build_patch_apply_sandbox_capability_matrix()
    joined_enabled = " ".join(matrix.enabled_sandbox_capabilities).lower()
    assert "sandbox patch apply" in joined_enabled
    assert "sandbox file write" in joined_enabled
    assert "single-cycle run packet" in " ".join(matrix.enabled_bounded_capabilities).lower()
    for prohibited in (
        "live_workspace_write",
        "live_code_edit",
        "unrestricted_patch_application",
        "apply_patch",
        "git_apply",
        "test_execution",
        "shell_execution",
        "dependency_install",
        "reference_execution",
        "reference_import",
        "external_agent_execution",
        "dominion_runtime",
        "provider_invocation",
        "direct_network_access",
        "credential_access",
        "persistent_trace_write",
        "UI_runtime",
        "authority_grant",
    ):
        assert prohibited in matrix.prohibited_capabilities
    assert patch_apply_sandbox_capability_matrix_is_not_permission_grant(matrix)


def test_coverage_builders_and_blocking_gap_rule():
    builders = (
        build_patch_apply_sandbox_stage_coverage,
        build_patch_apply_boundary_coverage,
        build_apply_candidate_coverage,
        build_dry_run_apply_coverage,
        build_sandbox_workspace_coverage,
        build_sandbox_patch_apply_coverage,
        build_sandbox_post_apply_validation_coverage,
        build_bounded_agentic_operation_coverage,
        build_patch_apply_trace_coverage,
        build_cli_sandbox_apply_surface_coverage,
    )
    coverages = [builder() for builder in builders]
    assert all(coverage.coverage_complete for coverage in coverages)
    assert {coverage.stage_version for coverage in coverages} >= {"v0.36.0", "v0.36.8"}
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_stage_coverage(coverage_complete=True, blocking_gaps=["missing boundary"])
    incomplete = build_patch_apply_sandbox_stage_coverage(coverage_complete=False, blocking_gaps=["missing test"])
    assert incomplete.coverage_complete is False


def test_boundary_risk_and_gap_registers():
    boundary = build_patch_apply_sandbox_boundary_register()
    risk = build_patch_apply_sandbox_risk_register()
    gap = build_patch_apply_sandbox_gap_register()
    for unsafe in ("live_workspace_write", "apply_patch", "git_apply", "test_execution", "external_agent_execution", "dominion_runtime", "authority_grant"):
        assert unsafe in boundary.prohibited_boundaries
    for unsafe in ("live_workspace_write", "shell_execution", "subprocess_execution", "command_execution", "D4_D9_grant"):
        assert unsafe in risk.prohibited_runtime_surfaces
    for item in ("controlled sandbox test runner boundary", "allowlisted test command policy", "timeout", "bounded output", "no network", "no dependency install by default", "test result envelope", "feedback report", "repair suggestion metadata only", "human checkpoint"):
        assert item in gap.recommended_v037_items
    assert "bounded repair loop" in gap.future_track_items


def test_release_manifest_and_audit_trail():
    manifest = build_patch_apply_sandbox_release_manifest()
    audit = build_patch_apply_sandbox_audit_trail()
    assert V036_VERSIONS.issubset(set(manifest.included_versions))
    assert manifest.release_flags.production_certified is False
    assert patch_apply_sandbox_audit_confirms_no_unsafe_runtime(audit)
    assert audit.sandbox_write_scoped_to_validated_root_confirmed
    assert audit.single_cycle_agentic_task_confirmed
    assert audit.human_handoff_required_confirmed
    with pytest.raises(ValueError):
        build_patch_apply_sandbox_audit_trail(no_shell_execution_confirmed=False)


def test_bounded_agentic_digestion_and_external_agent_records_are_not_runtime():
    agentic = build_bounded_agentic_operation_consolidation_record()
    digestion = build_digestion_dominion_sandbox_consolidation_record()
    external = build_external_agent_control_sandbox_consolidation_record()
    assert bounded_agentic_consolidation_record_is_not_autonomous_runtime(agentic)
    assert digestion_dominion_sandbox_record_is_not_runtime(digestion)
    assert external_agent_control_sandbox_record_is_not_execution(external)
    assert agentic.single_cycle_only_confirmed
    assert agentic.automatic_repair_blocked
    assert digestion.digestion_first_policy_confirmed
    assert digestion.dominion_fallback_future_gated
    assert external.execution_allowed is False
    assert external.dominion_runtime_allowed is False
    with pytest.raises(ValueError):
        build_external_agent_control_sandbox_consolidation_record(execution_allowed=True)


def test_v037_handoff_packet_is_design_stage_only():
    packet = build_v037_handoff_packet()
    assert "v0.36.9" in packet.source_version
    assert "v0.37" in packet.target_version_track
    assert "Controlled Sandbox Test Runner & Feedback Loop" in packet.recommended_next_track
    assert packet.ready_for_v037
    assert packet.ready_for_execution is False
    assert packet.ready_for_test_execution is False
    assert packet.ready_for_live_workspace_write is False
    assert packet.ready_for_patch_application is False
    assert packet.ready_for_shell_execution is False
    assert packet.ready_for_dependency_install is False
    assert "allowlisted test command policy" in packet.allowlisted_test_command_policy_items
    assert "timeout" in packet.timeout_and_resource_limit_items
    assert "bounded output" in packet.bounded_output_items
    assert "no network" in packet.no_network_items
    assert "no dependency install by default" in packet.no_dependency_install_by_default_items
    assert "feedback report" in packet.feedback_report_items
    assert "human checkpoint before repair loop" in packet.human_checkpoint_items
    assert v037_handoff_packet_is_design_stage_only(packet)
    with pytest.raises(ValueError):
        build_v037_handoff_packet(ready_for_test_execution=True)


def test_v036_consolidation_report_is_not_runtime_ready():
    report = build_v036_consolidation_report()
    assert report.ready_for_v037
    assert report.ready_for_human_approved_patch_apply_sandbox_v1
    assert report.ready_for_apply_candidate_human_approval_contract
    assert report.ready_for_dry_run_apply_simulation
    assert report.ready_for_sandbox_workspace_policy
    assert report.ready_for_sandbox_patch_apply
    assert report.ready_for_sandbox_post_apply_validation
    assert report.ready_for_bounded_agentic_task_operation_cycle
    assert report.ready_for_patch_apply_sandbox_trace_packet_creation
    assert report.ready_for_cli_sandbox_apply_surface
    assert v036_consolidation_report_is_not_runtime_ready(report)
    assert report.production_certified is False
    for name in (
        "ready_for_execution",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "ready_for_persistent_trace_write",
    ):
        assert getattr(report, name) is False
    with pytest.raises(ValueError):
        build_v036_consolidation_report(ready_for_execution=True)


def test_helpers_do_not_contain_runtime_execution_patterns():
    import chanta_core.agent_runtime.patch_apply_consolidation as module

    source = inspect.getsource(module)
    forbidden = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.write_text",
        "Path.write_bytes",
        "open(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
    ]
    for pattern in forbidden:
        assert pattern not in source
    assert "apply_patch(" not in source
    assert "git apply" not in source
