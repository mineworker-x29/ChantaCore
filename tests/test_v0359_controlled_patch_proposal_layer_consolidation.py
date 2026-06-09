import inspect

import pytest

from chanta_core.agent_runtime.patch_proposal_consolidation import (
    CLIPatchProposalSurfaceCoverage,
    ControlledPatchProposalAuditTrail,
    ControlledPatchProposalCapabilityMatrix,
    ControlledPatchProposalConsolidationReadinessLevel,
    ControlledPatchProposalConsolidationStatus,
    ControlledPatchProposalReleaseFlagSet,
    ControlledPatchProposalStageCoverage,
    DigestionDominionConsolidationRecord,
    ExternalAgentControlPatternConsolidationRecord,
    PatchBoundaryCoverage,
    PatchContextCoverage,
    PatchIntentScopeCoverage,
    PatchPlanCoverage,
    PatchProposalTraceCoverage,
    PatchReviewCoverage,
    PatchRiskCoverage,
    ReferenceDigestCoverage,
    V035ConsolidationReport,
    V036HandoffPacket,
    build_cli_patch_proposal_surface_coverage,
    build_controlled_patch_proposal_audit_trail,
    build_controlled_patch_proposal_boundary_register,
    build_controlled_patch_proposal_capability_matrix,
    build_controlled_patch_proposal_gap_register,
    build_controlled_patch_proposal_release_flags,
    build_controlled_patch_proposal_release_manifest,
    build_controlled_patch_proposal_risk_register,
    build_controlled_patch_proposal_snapshot,
    build_controlled_patch_proposal_stage_coverage,
    build_diff_proposal_coverage,
    build_digestion_dominion_consolidation_record,
    build_external_agent_control_pattern_consolidation_record,
    build_patch_boundary_coverage,
    build_patch_context_coverage,
    build_patch_intent_scope_coverage,
    build_patch_plan_coverage,
    build_patch_proposal_trace_coverage,
    build_patch_review_coverage,
    build_patch_risk_coverage,
    build_reference_digest_coverage,
    build_v035_consolidation_report,
    build_v036_handoff_packet,
    controlled_patch_proposal_audit_confirms_no_unsafe_runtime,
    controlled_patch_proposal_capability_matrix_is_not_permission_grant,
    controlled_patch_proposal_flags_preserve_no_apply,
    controlled_patch_proposal_snapshot_is_not_runtime_expansion,
    digestion_dominion_consolidation_record_is_not_runtime,
    external_agent_control_pattern_record_is_not_execution,
    v035_consolidation_report_is_not_runtime_ready,
    v036_handoff_packet_is_design_stage_only,
)
import chanta_core.agent_runtime.patch_proposal_consolidation as consolidation


def test_consolidation_taxonomies_are_complete():
    assert {item.value for item in ControlledPatchProposalConsolidationStatus} == {
        "unknown",
        "not_started",
        "in_progress",
        "consolidated",
        "consolidated_with_gaps",
        "blocked",
        "future_track",
        "no_op",
    }
    assert {item.value for item in ControlledPatchProposalConsolidationReadinessLevel} == {
        "not_ready",
        "contract_ready",
        "controlled_patch_proposal_layer_ready",
        "patch_proposal_artifact_ready",
        "review_packet_ready",
        "cli_patch_surface_ready",
        "handoff_ready_for_v036",
        "blocked",
        "future_track",
    }


def test_release_flags_allow_controlled_readiness_only():
    flags = build_controlled_patch_proposal_release_flags()

    assert isinstance(flags, ControlledPatchProposalReleaseFlagSet)
    assert flags.controlled_patch_proposal_layer_v1_ready is True
    assert flags.ready_for_v036_handoff is True
    assert flags.ready_for_patch_intent_scope_policy is True
    assert flags.ready_for_readonly_patch_context_collection is True
    assert flags.ready_for_reference_informed_patch_plan is True
    assert flags.ready_for_diff_proposal_artifact is True
    assert flags.ready_for_patch_risk_conformance_scan is True
    assert flags.ready_for_human_review_packet is True
    assert flags.ready_for_patch_proposal_trace_packet_creation is True
    assert flags.ready_for_cli_patch_proposal_surface is True
    assert flags.production_certified is False
    assert all(level in flags.future_track_levels for level in ("D4", "D5", "D6", "D7", "D8", "D9"))
    assert controlled_patch_proposal_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_kwarg",
    [
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_external_agent_execution",
        "ready_for_claude_code_invocation",
        "ready_for_codex_cli_invocation",
        "ready_for_dominion_runtime",
        "ready_for_infinite_agent_loop",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_persistent_trace_write",
        "ready_for_external_trace_sink",
        "ready_for_ui_runtime",
        "production_certified",
    ],
)
def test_release_flags_reject_unsafe_true(unsafe_kwarg):
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_release_flags(**{unsafe_kwarg: True})


def test_release_flags_reject_invalid_dominion_level_metadata():
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_release_flags(max_grantable_level="D4")
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_release_flags(future_track_levels=["D4", "D5"])


def test_snapshot_includes_all_v035_versions_and_is_not_runtime_expansion():
    snapshot = build_controlled_patch_proposal_snapshot()

    assert snapshot.release_name == "Controlled Patch Proposal Layer v1"
    for version in [f"v0.35.{index}" for index in range(9)]:
        assert version in snapshot.included_versions
    assert snapshot.consolidation_status == ControlledPatchProposalConsolidationStatus.CONSOLIDATED
    assert controlled_patch_proposal_snapshot_is_not_runtime_expansion(snapshot)

    with pytest.raises(ValueError):
        build_controlled_patch_proposal_snapshot(included_versions=["v0.35.1"])


def test_capability_matrix_lists_enabled_and_prohibited_surfaces():
    matrix = build_controlled_patch_proposal_capability_matrix()

    assert isinstance(matrix, ControlledPatchProposalCapabilityMatrix)
    assert "diff proposal envelope artifacts" in matrix.enabled_controlled_capabilities
    assert "CLI patch proposal preview surface" in matrix.enabled_controlled_capabilities
    for prohibited in (
        "patch application",
        "workspace write",
        "code edit",
        "apply_patch runtime call",
        "git apply runtime call",
        "test execution",
        "shell execution",
        "subprocess execution",
        "dependency install",
        "reference execution",
        "reference import",
        "external agent execution",
        "Claude Code invocation",
        "Codex CLI invocation",
        "Dominion runtime",
        "infinite agent loop",
        "provider invocation",
        "direct network access",
        "credential access",
        "secret read",
        "persistent trace write",
        "UI runtime",
    ):
        assert prohibited in matrix.prohibited_capabilities
    assert controlled_patch_proposal_capability_matrix_is_not_permission_grant(matrix)

    with pytest.raises(ValueError):
        build_controlled_patch_proposal_capability_matrix(prohibited_capabilities=["patch application"])


def test_coverage_models_cover_all_v035_stages_and_blocking_gaps_block_complete_coverage():
    coverages = [
        build_patch_boundary_coverage(),
        build_reference_digest_coverage(),
        build_patch_intent_scope_coverage(),
        build_patch_context_coverage(),
        build_patch_plan_coverage(),
        build_diff_proposal_coverage(),
        build_patch_risk_coverage(),
        build_patch_review_coverage(),
        build_patch_proposal_trace_coverage(),
        build_cli_patch_proposal_surface_coverage(),
    ]

    assert all(isinstance(item, ControlledPatchProposalStageCoverage) for item in coverages)
    assert isinstance(coverages[0], PatchBoundaryCoverage)
    assert isinstance(coverages[1], ReferenceDigestCoverage)
    assert isinstance(coverages[2], PatchIntentScopeCoverage)
    assert isinstance(coverages[3], PatchContextCoverage)
    assert isinstance(coverages[4], PatchPlanCoverage)
    assert isinstance(coverages[6], PatchRiskCoverage)
    assert isinstance(coverages[7], PatchReviewCoverage)
    assert isinstance(coverages[8], PatchProposalTraceCoverage)
    assert isinstance(coverages[9], CLIPatchProposalSurfaceCoverage)

    blocked = build_controlled_patch_proposal_stage_coverage(
        coverage_complete=False,
        blocking_gaps=["missing fixture"],
    )
    assert blocked.coverage_complete is False

    with pytest.raises(ValueError):
        build_controlled_patch_proposal_stage_coverage(
            coverage_complete=True,
            blocking_gaps=["cannot be complete"],
        )


def test_boundary_risk_and_gap_registers_keep_unsafe_surfaces_prohibited():
    boundary = build_controlled_patch_proposal_boundary_register()
    risk = build_controlled_patch_proposal_risk_register()
    gap = build_controlled_patch_proposal_gap_register()

    for prohibited in ("patch_apply", "workspace_write", "code_edit", "apply_patch", "git_apply", "shell", "subprocess", "external_agent_execution", "dominion_runtime", "authority_grant"):
        assert prohibited in boundary.prohibited_boundaries
    for surface in ("patch_application", "workspace_write", "code_edit", "apply_patch", "git_apply", "test_execution", "shell_execution", "subprocess_execution", "command_execution", "dependency_install", "reference_execution", "reference_import", "external_agent_execution", "dominion_runtime", "infinite_agent_loop", "provider_invocation", "direct_network_access", "credential_access", "secret_read", "persistent_trace_write", "UI_runtime", "external_control", "authority_grant", "D4_D9_grant"):
        assert surface in risk.prohibited_runtime_surfaces
    for future_item in ("human-approved patch apply sandbox", "dry-run apply simulation", "rollback plan", "controlled test runner", "persistent trace store", "UI runtime", "external harness adapter", "Dominion runtime gated review"):
        assert future_item in gap.future_track_items

    with pytest.raises(ValueError):
        build_controlled_patch_proposal_boundary_register(prohibited_boundaries=["patch_apply"])
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_risk_register(prohibited_runtime_surfaces=["patch_application"])
    with pytest.raises(ValueError):
        build_controlled_patch_proposal_gap_register(future_track_items=["human-approved patch apply sandbox"])


def test_manifest_and_audit_are_metadata_not_production_release():
    manifest = build_controlled_patch_proposal_release_manifest()
    audit = build_controlled_patch_proposal_audit_trail()

    for version in [f"v0.35.{index}" for index in range(9)]:
        assert version in manifest.included_versions
    assert manifest.release_flags.production_certified is False
    assert isinstance(audit, ControlledPatchProposalAuditTrail)
    assert audit.no_patch_application_confirmed is True
    assert audit.no_workspace_write_confirmed is True
    assert audit.no_code_edit_confirmed is True
    assert audit.no_apply_patch_confirmed is True
    assert audit.no_git_apply_confirmed is True
    assert audit.no_test_execution_confirmed is True
    assert audit.no_shell_execution_confirmed is True
    assert audit.no_external_agent_execution_confirmed is True
    assert audit.no_dominion_runtime_confirmed is True
    assert audit.no_persistent_trace_write_confirmed is True
    assert audit.unsafe_readiness_flags_false_confirmed is True
    assert controlled_patch_proposal_audit_confirms_no_unsafe_runtime(audit)

    with pytest.raises(ValueError):
        build_controlled_patch_proposal_audit_trail(no_patch_application_confirmed=False)


def test_digestion_dominion_and_external_agent_records_are_metadata_only():
    digestion = build_digestion_dominion_consolidation_record()
    external = build_external_agent_control_pattern_consolidation_record()

    assert isinstance(digestion, DigestionDominionConsolidationRecord)
    assert digestion.digestion_first_policy_confirmed is True
    assert digestion.dominion_fallback_future_gated is True
    assert digestion.external_agent_execution_blocked is True
    assert digestion.dominion_runtime_blocked is True
    assert digestion.infinite_loop_blocked is True
    assert digestion_dominion_consolidation_record_is_not_runtime(digestion)

    assert isinstance(external, ExternalAgentControlPatternConsolidationRecord)
    assert "codex_to_claude_code_loop" in external.observed_pattern_kinds
    assert external.execution_allowed is False
    assert external.dominion_runtime_allowed is False
    assert external.infinite_loop_allowed is False
    assert external_agent_control_pattern_record_is_not_execution(external)

    with pytest.raises(ValueError):
        build_digestion_dominion_consolidation_record(dominion_runtime_blocked=False)
    with pytest.raises(ValueError):
        build_external_agent_control_pattern_consolidation_record(execution_allowed=True)


def test_v036_handoff_is_design_stage_only():
    handoff = build_v036_handoff_packet()

    assert isinstance(handoff, V036HandoffPacket)
    assert "v0.35.9" in handoff.source_version
    assert "v0.36" in handoff.target_version_track
    assert "Human-approved Patch Apply Sandbox" in handoff.recommended_next_track
    assert handoff.ready_for_v036 is True
    assert handoff.ready_for_execution is False
    assert handoff.ready_for_patch_application is False
    assert handoff.ready_for_workspace_write is False
    assert handoff.ready_for_code_edit is False
    assert handoff.ready_for_apply_patch is False
    assert handoff.ready_for_git_apply is False
    assert "dry-run apply simulation" in " ".join(handoff.dry_run_apply_simulation_items)
    assert handoff.rollback_plan_items
    assert v036_handoff_packet_is_design_stage_only(handoff)

    with pytest.raises(ValueError):
        build_v036_handoff_packet(source_version="v0.35.8")
    with pytest.raises(ValueError):
        build_v036_handoff_packet(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v036_handoff_packet(ready_for_patch_application=True)


def test_v035_consolidation_report_keeps_runtime_readiness_false():
    report = build_v035_consolidation_report()

    assert isinstance(report, V035ConsolidationReport)
    assert report.ready_for_v036 is True
    assert report.ready_for_controlled_patch_proposal_layer_v1 is True
    assert report.ready_for_diff_proposal_artifact is True
    assert report.ready_for_human_review_packet is True
    assert report.ready_for_patch_proposal_trace_packet_creation is True
    assert report.ready_for_cli_patch_proposal_surface is True
    assert report.ready_for_execution is False
    assert report.ready_for_patch_application is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_code_edit is False
    assert report.ready_for_apply_patch is False
    assert report.ready_for_git_apply is False
    assert report.ready_for_test_execution is False
    assert report.ready_for_shell_execution is False
    assert report.ready_for_external_agent_execution is False
    assert report.ready_for_dominion_runtime is False
    assert report.ready_for_persistent_trace_write is False
    assert report.production_certified is False
    assert v035_consolidation_report_is_not_runtime_ready(report)

    with pytest.raises(ValueError):
        build_v035_consolidation_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v035_consolidation_report(ready_for_patch_application=True)


def test_module_exports_safe_consolidation_names():
    from chanta_core.agent_runtime import (
        ControlledPatchProposalSnapshot,
        build_v035_consolidation_report,
    )

    snapshot = build_controlled_patch_proposal_snapshot()
    report = build_v035_consolidation_report()
    assert isinstance(snapshot, ControlledPatchProposalSnapshot)
    assert report.ready_for_execution is False


def test_runtime_forbidden_patterns_are_absent_from_implementation_helpers():
    source = inspect.getsource(consolidation)

    forbidden_runtime_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system(",
        "shell=True",
        "from pathlib",
        "Path(",
        ".read_text(",
        ".read_bytes(",
        ".write_text(",
        ".write_bytes(",
        " open(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
        "logging.",
        "json.dump(",
        "sqlite",
    ]

    for pattern in forbidden_runtime_patterns:
        assert pattern not in source
