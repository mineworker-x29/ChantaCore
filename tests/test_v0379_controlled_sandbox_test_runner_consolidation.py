from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    CLITestRunnerSurfaceConsolidationRecord,
    CLITestRunnerSurfaceCoverage,
    ColdAgentEvaluationCoverage,
    ColdEvaluationConsolidationRecord,
    ControlledTestExecutionConsolidationRecord,
    DigestionDominionTestRunnerConsolidationRecord,
    SandboxRepairSuggestionCoverage,
    SandboxTestBoundaryCoverage,
    SandboxTestCommandPolicyCoverage,
    SandboxTestExecutionEngineCoverage,
    SandboxTestFeedbackCoverage,
    SandboxTestResultEnvelopeCoverage,
    SandboxTestRunnerAuditTrail,
    SandboxTestRunnerBoundaryRegister,
    SandboxTestRunnerCapabilityMatrix,
    SandboxTestRunnerConsolidationRiskRegister,
    SandboxTestRunnerConsolidationReadinessLevel,
    SandboxTestRunnerConsolidationStatus,
    SandboxTestRunnerEvaluationSnapshot,
    SandboxTestRunnerGapRegister,
    SandboxTestRunnerReleaseFlagSet,
    SandboxTestRunnerReleaseManifest,
    SandboxTestRunnerStageCoverage,
    V037ConsolidationReport,
    V038HandoffPacket,
    VeraCodexTrialConsolidationRecord,
    VeraCodexTrialCoverage,
    build_cli_test_runner_surface_consolidation_record,
    build_cli_test_runner_surface_coverage,
    build_cold_agent_evaluation_coverage,
    build_cold_evaluation_consolidation_record,
    build_controlled_test_execution_consolidation_record,
    build_digestion_dominion_test_runner_consolidation_record,
    build_sandbox_repair_suggestion_coverage,
    build_sandbox_test_boundary_coverage,
    build_sandbox_test_command_policy_coverage,
    build_sandbox_test_execution_engine_coverage,
    build_sandbox_test_feedback_coverage,
    build_sandbox_test_result_envelope_coverage,
    build_sandbox_test_runner_audit_trail,
    build_sandbox_test_runner_boundary_register,
    build_sandbox_test_runner_capability_matrix,
    build_sandbox_test_runner_consolidation_risk_register,
    build_sandbox_test_runner_evaluation_snapshot,
    build_sandbox_test_runner_gap_register,
    build_sandbox_test_runner_release_flags,
    build_sandbox_test_runner_release_manifest,
    build_sandbox_test_runner_stage_coverage,
    build_v037_consolidation_report,
    build_v038_handoff_packet,
    build_vera_codex_trial_consolidation_record,
    build_vera_codex_trial_coverage,
    cli_test_runner_surface_consolidation_record_is_not_shell,
    cold_evaluation_consolidation_record_is_not_production_certification,
    controlled_test_execution_consolidation_record_is_scoped,
    digestion_dominion_test_runner_record_is_not_runtime,
    sandbox_test_runner_audit_confirms_no_unsafe_runtime,
    sandbox_test_runner_capability_matrix_is_not_permission_grant,
    sandbox_test_runner_flags_preserve_no_unsafe_runtime,
    sandbox_test_runner_snapshot_is_not_production_runtime,
    v037_consolidation_report_is_not_runtime_ready,
    v038_handoff_packet_is_design_stage_only,
    vera_codex_trial_consolidation_record_is_not_autonomous_runtime,
)


V037_VERSIONS = {f"v0.37.{index}" for index in range(9)}

SAFE_FLAG_NAMES = {
    "ready_for_v038_handoff",
    "ready_for_test_runner_boundary",
    "ready_for_controlled_test_command_policy",
    "ready_for_test_invocation_contract",
    "ready_for_controlled_sandbox_test_execution",
    "ready_for_controlled_test_subprocess_via_v0372",
    "ready_for_bounded_test_output_capture",
    "ready_for_test_result_envelope",
    "ready_for_test_output_classifier",
    "ready_for_test_feedback_report",
    "ready_for_failure_diagnosis_report",
    "ready_for_repair_suggestion_metadata",
    "ready_for_repair_scope_metadata",
    "ready_for_future_repair_proposal_input",
    "ready_for_vera_codex_one_shot_agent_trial",
    "ready_for_vera_codex_evidence_bundle",
    "ready_for_vera_codex_decision_trace",
    "ready_for_cold_agent_performance_evaluation",
    "ready_for_cold_agent_scorecard",
    "ready_for_do_nothing_comparison",
    "ready_for_cli_test_runner_surface",
    "ready_for_cli_sandbox_test_run",
    "ready_for_cli_vera_trial_run_once",
    "ready_for_cli_cold_scorecard",
}

SAFE_REPORT_READY_NAMES = {
    "ready_for_v038",
    "ready_for_controlled_sandbox_test_runner_v1",
    "ready_for_controlled_test_command_policy",
    "ready_for_controlled_sandbox_test_execution",
    "ready_for_test_result_envelope",
    "ready_for_test_feedback_report",
    "ready_for_repair_suggestion_metadata",
    "ready_for_vera_codex_one_shot_agent_trial",
    "ready_for_cold_agent_performance_evaluation",
    "ready_for_cli_test_runner_surface",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES
    ]


def _unsafe_report_ready_names():
    return [
        field.name
        for field in fields(V037ConsolidationReport)
        if field.name.startswith("ready_for_") and field.name not in SAFE_REPORT_READY_NAMES
    ]


def test_status_and_readiness_taxonomies():
    assert {item.value for item in SandboxTestRunnerConsolidationStatus} == {
        "unknown",
        "not_started",
        "in_progress",
        "consolidated",
        "consolidated_with_gaps",
        "blocked",
        "future_track",
        "no_op",
    }
    assert {item.value for item in SandboxTestRunnerConsolidationReadinessLevel} == {
        "not_ready",
        "contract_ready",
        "controlled_sandbox_test_runner_ready",
        "test_result_feedback_pipeline_ready",
        "vera_codex_evaluation_ready",
        "cli_surface_ready",
        "handoff_ready_for_v038",
        "blocked",
        "future_track",
    }


def test_required_models_are_exported():
    for model in (
        SandboxTestRunnerReleaseFlagSet,
        SandboxTestRunnerEvaluationSnapshot,
        SandboxTestRunnerCapabilityMatrix,
        SandboxTestRunnerStageCoverage,
        SandboxTestBoundaryCoverage,
        SandboxTestCommandPolicyCoverage,
        SandboxTestExecutionEngineCoverage,
        SandboxTestResultEnvelopeCoverage,
        SandboxTestFeedbackCoverage,
        SandboxRepairSuggestionCoverage,
        VeraCodexTrialCoverage,
        ColdAgentEvaluationCoverage,
        CLITestRunnerSurfaceCoverage,
        SandboxTestRunnerBoundaryRegister,
        SandboxTestRunnerConsolidationRiskRegister,
        SandboxTestRunnerGapRegister,
        SandboxTestRunnerReleaseManifest,
        SandboxTestRunnerAuditTrail,
        ControlledTestExecutionConsolidationRecord,
        VeraCodexTrialConsolidationRecord,
        ColdEvaluationConsolidationRecord,
        CLITestRunnerSurfaceConsolidationRecord,
        DigestionDominionTestRunnerConsolidationRecord,
        V038HandoffPacket,
        V037ConsolidationReport,
    ):
        assert model is not None


def test_release_flags_allow_bounded_v037_readiness_and_preserve_unsafe_false():
    flags = build_sandbox_test_runner_release_flags()
    assert flags.controlled_sandbox_test_runner_v1_ready
    assert flags.ready_for_v038_handoff
    assert flags.ready_for_controlled_test_command_policy
    assert flags.ready_for_controlled_sandbox_test_execution
    assert flags.ready_for_controlled_test_subprocess_via_v0372
    assert flags.ready_for_test_result_envelope
    assert flags.ready_for_test_feedback_report
    assert flags.ready_for_repair_suggestion_metadata
    assert flags.ready_for_vera_codex_one_shot_agent_trial
    assert flags.ready_for_cold_agent_performance_evaluation
    assert flags.ready_for_cli_test_runner_surface
    assert sandbox_test_runner_flags_preserve_no_unsafe_runtime(flags)
    assert flags.production_certified is False
    for name in _unsafe_flag_names(SandboxTestRunnerReleaseFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False
    for level in ("D4", "D5", "D6", "D7", "D8", "D9"):
        assert any(item.startswith(level) for item in flags.future_track_levels)


@pytest.mark.parametrize(
    "field_name",
    _unsafe_flag_names(SandboxTestRunnerReleaseFlagSet) + ["production_certified"],
)
def test_release_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_sandbox_test_runner_release_flags(**{field_name: True})


def test_release_flags_reject_invalid_dominion_grant_metadata():
    with pytest.raises(ValueError):
        build_sandbox_test_runner_release_flags(max_grantable_level="D4_WRITE")
    with pytest.raises(ValueError):
        build_sandbox_test_runner_release_flags(future_track_levels=["D4", "D5"])


def test_snapshot_includes_v0370_through_v0378_and_is_not_runtime_expansion():
    snapshot = build_sandbox_test_runner_evaluation_snapshot()
    assert V037_VERSIONS.issubset(set(snapshot.included_versions))
    assert "Controlled Sandbox Test Runner & Vera-Codex Agent Evaluation v1" in snapshot.release_name
    assert sandbox_test_runner_snapshot_is_not_production_runtime(snapshot)
    assert "repair_patch_proposal" in snapshot.prohibited_capabilities
    with pytest.raises(ValueError):
        build_sandbox_test_runner_evaluation_snapshot(included_versions=["v0.37.8"])


def test_capability_matrix_lists_enabled_and_prohibited_capabilities():
    matrix = build_sandbox_test_runner_capability_matrix()
    joined_enabled = " ".join(matrix.enabled_test_runner_capabilities + matrix.enabled_agent_evaluation_capabilities).lower()
    for enabled in (
        "controlled sandbox test execution",
        "test result envelope",
        "test feedback report",
        "repair suggestion metadata",
        "one-shot trial",
        "cold agent",
        "scorecard",
        "cli",
    ):
        assert enabled in joined_enabled
    for prohibited in (
        "arbitrary_shell",
        "direct_subprocess",
        "uncontrolled_subprocess",
        "raw_pytest",
        "package_script",
        "dependency_install",
        "network_access",
        "live_workspace_write",
        "patch_application",
        "apply_patch",
        "git_apply",
        "repair_patch_proposal",
        "repair_diff_generation",
        "code_hunk_generation",
        "automatic_repair",
        "model_provider_invocation",
        "tool_execution",
        "external_agent_execution",
        "claude_code_invocation",
        "codex_cli_invocation",
        "Dominion_runtime",
        "persistent_trace_write",
        "UI_runtime",
        "authority_grant",
        "production_certification",
    ):
        assert prohibited in matrix.prohibited_capabilities
    assert sandbox_test_runner_capability_matrix_is_not_permission_grant(matrix)


def test_coverage_builders_and_blocking_gap_rule():
    builders = (
        build_sandbox_test_runner_stage_coverage,
        build_sandbox_test_boundary_coverage,
        build_sandbox_test_command_policy_coverage,
        build_sandbox_test_execution_engine_coverage,
        build_sandbox_test_result_envelope_coverage,
        build_sandbox_test_feedback_coverage,
        build_sandbox_repair_suggestion_coverage,
        build_vera_codex_trial_coverage,
        build_cold_agent_evaluation_coverage,
        build_cli_test_runner_surface_coverage,
    )
    coverages = [builder() for builder in builders]
    assert all(coverage.coverage_complete for coverage in coverages)
    assert {coverage.stage_version for coverage in coverages} >= {"v0.37.0", "v0.37.8"}
    with pytest.raises(ValueError):
        build_sandbox_test_runner_stage_coverage(coverage_complete=True, blocking_gaps=["missing boundary"])
    incomplete = build_sandbox_test_runner_stage_coverage(coverage_complete=False, blocking_gaps=["missing test"])
    assert incomplete.coverage_complete is False


def test_boundary_risk_and_gap_registers():
    boundary = build_sandbox_test_runner_boundary_register()
    risk = build_sandbox_test_runner_consolidation_risk_register()
    gap = build_sandbox_test_runner_gap_register()
    for unsafe in (
        "arbitrary_shell",
        "direct_subprocess",
        "uncontrolled_subprocess",
        "raw_pytest",
        "dependency_install",
        "network_access",
        "live_workspace_write",
        "apply_patch",
        "git_apply",
        "repair_patch_proposal",
        "automatic_repair",
        "model_provider_invocation",
        "external_agent_execution",
        "dominion_runtime",
        "authority_grant",
    ):
        assert unsafe in boundary.prohibited_boundaries
    for unsafe in ("shell", "direct_subprocess", "dependency_install", "network_access", "live_write", "repair_patch_proposal", "model_invocation", "tool_execution", "external_agent", "Dominion"):
        assert unsafe in risk.prohibited_runtime_surfaces
    for item in (
        "bounded repair proposal boundary",
        "repair proposal evidence contract",
        "proposed diff metadata",
        "code hunk proposal metadata",
        "no apply by default",
        "human approval before apply",
        "sandbox-only proposal validation",
        "do-nothing comparison",
        "cold evaluation feedback integration",
    ):
        assert item in gap.recommended_v038_items
    for item in ("bounded repair proposal loop", "sandbox repair apply gate", "persistent trace store", "UI runtime", "external harness adapter", "Dominion runtime gated review"):
        assert item in gap.future_track_items


def test_release_manifest_and_audit_trail():
    manifest = build_sandbox_test_runner_release_manifest()
    audit = build_sandbox_test_runner_audit_trail()
    assert V037_VERSIONS.issubset(set(manifest.included_versions))
    assert manifest.release_flags.production_certified is False
    assert sandbox_test_runner_audit_confirms_no_unsafe_runtime(audit)
    assert audit.controlled_subprocess_scoped_to_v0372_confirmed
    assert audit.do_nothing_comparison_required_confirmed
    assert audit.human_handoff_required_confirmed
    assert audit.evidence_bounded_scorecard_confirmed
    with pytest.raises(ValueError):
        build_sandbox_test_runner_audit_trail(no_shell_execution_confirmed=False)


def test_controlled_vera_cold_cli_and_digestion_records_are_bounded():
    controlled = build_controlled_test_execution_consolidation_record()
    vera = build_vera_codex_trial_consolidation_record()
    cold = build_cold_evaluation_consolidation_record()
    cli = build_cli_test_runner_surface_consolidation_record()
    digestion = build_digestion_dominion_test_runner_consolidation_record()
    assert controlled_test_execution_consolidation_record_is_scoped(controlled)
    assert controlled.structured_argv_confirmed
    assert controlled.shell_false_confirmed
    assert controlled.direct_subprocess_blocked
    assert controlled.dependency_install_blocked
    assert controlled.network_access_blocked
    assert vera_codex_trial_consolidation_record_is_not_autonomous_runtime(vera)
    assert vera.one_shot_trial_confirmed
    assert vera.no_model_invocation_confirmed
    assert vera.no_chain_of_thought_output_confirmed
    assert cold_evaluation_consolidation_record_is_not_production_certification(cold)
    assert cold.pass_requires_evidence_confirmed
    assert cold.production_certification_blocked
    assert cli_test_runner_surface_consolidation_record_is_not_shell(cli)
    assert cli.argv_not_shell_confirmed
    assert cli.raw_pytest_blocked
    assert digestion_dominion_test_runner_record_is_not_runtime(digestion)
    assert digestion.digestion_first_policy_confirmed
    assert digestion.dominion_fallback_future_gated
    with pytest.raises(ValueError):
        build_controlled_test_execution_consolidation_record(direct_subprocess_blocked=False)
    with pytest.raises(ValueError):
        build_vera_codex_trial_consolidation_record(no_model_invocation_confirmed=False)
    with pytest.raises(ValueError):
        build_cold_evaluation_consolidation_record(production_certification_blocked=False)
    with pytest.raises(ValueError):
        build_cli_test_runner_surface_consolidation_record(argv_not_shell_confirmed=False)
    with pytest.raises(ValueError):
        build_digestion_dominion_test_runner_consolidation_record(dominion_runtime_blocked=False)


def test_v038_handoff_packet_is_design_stage_only():
    packet = build_v038_handoff_packet()
    assert "v0.37.9" in packet.source_version
    assert "v0.38" in packet.target_version_track
    assert "Bounded Repair Proposal Loop" in packet.recommended_next_track
    assert packet.ready_for_v038
    assert packet.ready_for_execution is False
    assert packet.ready_for_repair_patch_proposal is False
    assert packet.ready_for_repair_execution is False
    assert packet.ready_for_patch_application is False
    assert packet.ready_for_live_workspace_write is False
    assert packet.ready_for_shell_execution is False
    assert packet.ready_for_dependency_install is False
    assert packet.ready_for_network_access is False
    assert "bounded repair proposal boundary" in packet.repair_proposal_boundary_items
    assert "repair proposal evidence contract" in packet.repair_evidence_contract_items
    assert "proposed diff metadata" in packet.proposed_diff_metadata_items
    assert "code hunk proposal metadata" in packet.code_hunk_proposal_metadata_items
    assert "no apply by default" in packet.no_apply_by_default_items
    assert "human approval before apply" in packet.human_approval_before_apply_items
    assert "sandbox-only proposal validation" in packet.sandbox_only_proposal_validation_items
    assert "do-nothing comparison" in packet.do_nothing_comparison_items
    assert "cold evaluation feedback integration" in packet.cold_evaluation_feedback_items
    assert v038_handoff_packet_is_design_stage_only(packet)
    with pytest.raises(ValueError):
        build_v038_handoff_packet(ready_for_repair_patch_proposal=True)
    with pytest.raises(ValueError):
        build_v038_handoff_packet(ready_for_execution=True)


def test_v037_consolidation_report_is_not_runtime_ready():
    report = build_v037_consolidation_report()
    assert report.ready_for_v038
    assert report.ready_for_controlled_sandbox_test_runner_v1
    assert report.ready_for_controlled_test_command_policy
    assert report.ready_for_controlled_sandbox_test_execution
    assert report.ready_for_test_result_envelope
    assert report.ready_for_test_feedback_report
    assert report.ready_for_repair_suggestion_metadata
    assert report.ready_for_vera_codex_one_shot_agent_trial
    assert report.ready_for_cold_agent_performance_evaluation
    assert report.ready_for_cli_test_runner_surface
    assert v037_consolidation_report_is_not_runtime_ready(report)
    assert report.production_certified is False
    for name in _unsafe_report_ready_names() + ["production_certified"]:
        assert getattr(report, name) is False
    with pytest.raises(ValueError):
        build_v037_consolidation_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v037_consolidation_report(ready_for_shell_execution=True)
    with pytest.raises(ValueError):
        build_v037_consolidation_report(production_certified=True)


def test_helpers_do_not_contain_runtime_execution_patterns():
    import chanta_core.agent_runtime.sandbox_test_consolidation as module

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
