from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    ProposedCodeHunkPosture,
    ProposedDiffPosture,
    ProposedPatchEnvelopePosture,
    RepairDoNothingPosture,
    RepairEvidenceBoundaryPolicy,
    RepairFutureApplyBoundaryPolicy,
    RepairHumanReviewBoundaryPolicy,
    RepairHumanReviewPosture,
    RepairPatchMetadataBoundaryPolicy,
    RepairProposalAllowedSurface,
    RepairProposalBoundary,
    RepairProposalBoundaryPolicy,
    RepairProposalCapabilityKind,
    RepairProposalDecisionKind,
    RepairProposalDeniedAction,
    RepairProposalFlagSet,
    RepairProposalGateEvaluation,
    RepairProposalNoExecutionGuarantee,
    RepairProposalPermissionDecision,
    RepairProposalPermissionRequest,
    RepairProposalPosture,
    RepairProposalProhibitedSurface,
    RepairProposalReadinessLevel,
    RepairProposalRiskKind,
    RepairProposalRiskRegister,
    RepairProposalSourceKind,
    RepairProposalSourceRef,
    RepairProposalStatus,
    RepairProposalSurfaceKind,
    RepairProposalTrackKind,
    RepairSafetyValidationBoundaryPolicy,
    RepairScopePlanningBoundaryPolicy,
    RepairSourceContextBoundaryPolicy,
    RepairSourceContextPosture,
    V0380ReadinessReport,
    V038RoadmapOverview,
    build_repair_evidence_boundary_policy,
    build_repair_future_apply_boundary_policy,
    build_repair_human_review_boundary_policy,
    build_repair_patch_metadata_boundary_policy,
    build_repair_proposal_allowed_surface,
    build_repair_proposal_boundary,
    build_repair_proposal_boundary_policy,
    build_repair_proposal_denied_action,
    build_repair_proposal_flags,
    build_repair_proposal_gate_evaluation,
    build_repair_proposal_no_execution_guarantee,
    build_repair_proposal_permission_decision,
    build_repair_proposal_permission_request,
    build_repair_proposal_prohibited_surface,
    build_repair_proposal_risk_register,
    build_repair_proposal_source_ref,
    build_repair_safety_validation_boundary_policy,
    build_repair_scope_planning_boundary_policy,
    build_repair_source_context_boundary_policy,
    build_v0380_readiness_report,
    build_v038_roadmap_overview,
    repair_future_apply_policy_blocks_apply,
    repair_human_review_policy_is_not_approval,
    repair_patch_metadata_policy_blocks_generation,
    repair_proposal_boundary_is_not_generation,
    repair_proposal_flags_preserve_no_execution,
    repair_proposal_permission_decision_is_not_generation,
    repair_proposal_policy_blocks_generation_and_execution,
    v0380_readiness_report_is_not_execution_ready,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0381_repair_proposal_evidence_contract",
    "ready_for_v0382_read_only_sandbox_source_context",
    "ready_for_v0383_repair_scope_planner_change_intent",
    "ready_for_v0384_proposed_diff_code_hunk_metadata",
    "ready_for_v0385_repair_proposal_safety_validation",
    "ready_for_v0386_human_review_packet",
    "ready_for_v0387_bounded_repair_proposal_loop_trial",
    "ready_for_v0388_cli_repair_proposal_surface",
    "ready_for_bounded_repair_proposal_boundary",
    "ready_for_repair_proposal_policy_boundary",
    "ready_for_repair_evidence_contract_boundary",
    "ready_for_read_only_sandbox_source_context_boundary",
    "ready_for_repair_scope_planning_boundary",
    "ready_for_change_intent_boundary",
    "ready_for_proposed_diff_metadata_boundary",
    "ready_for_proposed_code_hunk_metadata_boundary",
    "ready_for_proposed_patch_envelope_boundary",
    "ready_for_repair_safety_validation_boundary",
    "ready_for_repair_human_review_boundary",
    "ready_for_do_nothing_repair_comparison_boundary",
    "ready_for_future_sandbox_repair_apply_input_boundary",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES
    ]


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairProposalTrackKind} == {
        "boundary_foundation",
        "repair_proposal_evidence_contract",
        "read_only_sandbox_source_context",
        "repair_scope_planner_change_intent",
        "proposed_diff_code_hunk_metadata",
        "repair_proposal_safety_validation",
        "human_review_packet",
        "bounded_repair_proposal_loop_trial",
        "cli_repair_proposal_surface",
        "consolidation",
        "unknown",
    }
    assert "proposed_diff_metadata" in {item.value for item in RepairProposalSurfaceKind}
    assert "generate_proposed_diff" in {item.value for item in RepairProposalCapabilityKind}
    assert "source_read_scope_risk" in {item.value for item in RepairProposalRiskKind}
    assert "allow_boundary_definition" in {item.value for item in RepairProposalDecisionKind}
    assert "boundary_ready" in {item.value for item in RepairProposalStatus}
    assert "bounded_repair_proposal_boundary_ready" in {item.value for item in RepairProposalReadinessLevel}
    assert "boundary_only" in {item.value for item in RepairProposalPosture}
    assert "no_diff_generation" in {item.value for item in ProposedDiffPosture}
    assert "no_hunk_generation" in {item.value for item in ProposedCodeHunkPosture}
    assert "no_patch_envelope_generation" in {item.value for item in ProposedPatchEnvelopePosture}
    assert "no_source_read" in {item.value for item in RepairSourceContextPosture}
    assert "human_review_required_boundary" in {item.value for item in RepairHumanReviewPosture}
    assert "do_nothing_boundary_defined" in {item.value for item in RepairDoNothingPosture}
    assert "v0379_test_runner_consolidation" in {item.value for item in RepairProposalSourceKind}


def test_required_models_are_exported():
    for model in (
        RepairProposalFlagSet,
        RepairProposalSourceRef,
        RepairProposalBoundaryPolicy,
        RepairEvidenceBoundaryPolicy,
        RepairSourceContextBoundaryPolicy,
        RepairScopePlanningBoundaryPolicy,
        RepairPatchMetadataBoundaryPolicy,
        RepairSafetyValidationBoundaryPolicy,
        RepairHumanReviewBoundaryPolicy,
        RepairFutureApplyBoundaryPolicy,
        RepairProposalAllowedSurface,
        RepairProposalProhibitedSurface,
        RepairProposalBoundary,
        RepairProposalPermissionRequest,
        RepairProposalPermissionDecision,
        RepairProposalDeniedAction,
        RepairProposalGateEvaluation,
        RepairProposalRiskRegister,
        RepairProposalNoExecutionGuarantee,
        V038RoadmapOverview,
        V0380ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_boundary_readiness_and_preserve_no_execution():
    flags = build_repair_proposal_flags()
    assert flags.repair_proposal_boundary_constructed
    assert flags.repair_proposal_policy_defined
    assert flags.repair_evidence_contract_boundary_defined
    assert flags.read_only_source_context_boundary_defined
    assert flags.repair_scope_planning_boundary_defined
    assert flags.change_intent_boundary_defined
    assert flags.proposed_diff_metadata_boundary_defined
    assert flags.proposed_code_hunk_metadata_boundary_defined
    assert flags.proposed_patch_envelope_boundary_defined
    assert flags.repair_safety_validation_boundary_defined
    assert flags.repair_human_review_boundary_defined
    assert flags.do_nothing_repair_comparison_boundary_defined
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    assert repair_proposal_flags_preserve_no_execution(flags)
    for name in _unsafe_flag_names(RepairProposalFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize(
    "field_name",
    _unsafe_flag_names(RepairProposalFlagSet) + ["production_certified"],
)
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_proposal_flags(**{field_name: True})


def test_source_ref_is_not_source_read_or_generation():
    source = build_repair_proposal_source_ref()
    assert source.source_kind == RepairProposalSourceKind.V0379_TEST_RUNNER_CONSOLIDATION
    assert source.evidence_refs


def test_boundary_policy_allows_future_gates_but_blocks_generation_and_execution():
    policy = build_repair_proposal_boundary_policy()
    assert policy.allow_boundary_definition
    assert policy.allow_evidence_contract_future_gate
    assert policy.allow_read_only_source_context_future_gate
    assert policy.allow_proposed_diff_metadata_future_gate
    assert policy.allow_proposed_code_hunk_metadata_future_gate
    assert policy.allow_future_sandbox_repair_apply_input_boundary
    assert repair_proposal_policy_blocks_generation_and_execution(policy)
    for name in (
        "allow_source_file_read",
        "allow_sandbox_source_read",
        "allow_repair_proposal_generation",
        "allow_proposed_diff_generation",
        "allow_proposed_code_hunk_generation",
        "allow_proposed_patch_envelope_generation",
        "allow_repair_patch_proposal",
        "allow_repair_execution",
        "allow_repair_apply",
        "allow_sandbox_repair_apply",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_automatic_repair",
        "allow_test_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_dependency_install",
        "allow_network_access",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_repair_proposal_boundary_policy(**{name: True})


def test_subpolicies_are_future_gated_and_not_executable():
    subpolicies = (
        build_repair_evidence_boundary_policy(),
        build_repair_source_context_boundary_policy(),
        build_repair_scope_planning_boundary_policy(),
        build_repair_patch_metadata_boundary_policy(),
        build_repair_safety_validation_boundary_policy(),
        build_repair_human_review_boundary_policy(),
        build_repair_future_apply_boundary_policy(),
    )
    assert all(policy.future_gated for policy in subpolicies)
    for policy in subpolicies:
        assert policy.executable_in_v0380 is False
        assert policy.allows_file_read is False
        assert policy.allows_file_write is False
        assert policy.allows_diff_generation is False
        assert policy.allows_hunk_generation is False
        assert policy.allows_patch_generation is False
        assert policy.allows_patch_apply is False
        assert policy.allows_repair_execution is False
    assert repair_patch_metadata_policy_blocks_generation(subpolicies[3])
    assert repair_human_review_policy_is_not_approval(subpolicies[5])
    assert repair_future_apply_policy_blocks_apply(subpolicies[6])
    with pytest.raises(ValueError):
        build_repair_patch_metadata_boundary_policy(allows_diff_generation=True)
    with pytest.raises(ValueError):
        build_repair_human_review_boundary_policy(executable_in_v0380=True)
    with pytest.raises(ValueError):
        build_repair_future_apply_boundary_policy(allows_patch_apply=True)


def test_allowed_and_prohibited_surfaces():
    allowed = build_repair_proposal_allowed_surface()
    assert allowed.allowed_only_for_design_stage
    for name in (
        "executable_in_v0380",
        "reads_source",
        "generates_diff",
        "generates_hunk",
        "generates_patch_envelope",
        "writes_file",
        "applies_patch",
        "executes_repair",
    ):
        assert getattr(allowed, name) is False
        with pytest.raises(ValueError):
            build_repair_proposal_allowed_surface(**{name: True})
    prohibited = build_repair_proposal_prohibited_surface()
    assert prohibited.blocks_proposal_generation
    assert prohibited.blocks_repair_execution
    assert prohibited.blocks_runtime_readiness
    with pytest.raises(ValueError):
        build_repair_proposal_prohibited_surface(blocks_runtime_readiness=False)


def test_boundary_is_not_proposal_generation():
    boundary = build_repair_proposal_boundary()
    assert repair_proposal_boundary_is_not_generation(boundary)
    assert boundary.ready_for_v0381_repair_proposal_evidence_contract
    assert boundary.ready_for_v0382_read_only_sandbox_source_context
    assert boundary.ready_for_v0384_proposed_diff_code_hunk_metadata
    assert boundary.ready_for_bounded_repair_proposal_boundary
    assert boundary.ready_for_repair_human_review_boundary
    assert boundary.ready_for_do_nothing_repair_comparison_boundary
    with pytest.raises(ValueError):
        build_repair_proposal_boundary(ready_for_repair_proposal_generation=True)
    with pytest.raises(ValueError):
        build_repair_proposal_boundary(ready_for_proposed_diff_generation=True)


def test_permission_decision_never_allows_generation_or_runtime():
    request = build_repair_proposal_permission_request()
    decision = build_repair_proposal_permission_decision(request_id=request.request_id)
    denied = build_repair_proposal_denied_action()
    gate = build_repair_proposal_gate_evaluation(request=request, decision=decision, denied_action=denied)
    assert repair_proposal_permission_decision_is_not_generation(decision)
    assert gate.ready_for_execution is False
    for name in (
        "source_file_read_allowed",
        "sandbox_source_read_allowed",
        "repair_proposal_generation_allowed",
        "proposed_diff_generation_allowed",
        "proposed_code_hunk_generation_allowed",
        "proposed_patch_envelope_generation_allowed",
        "file_write_allowed",
        "patch_apply_allowed",
        "repair_execution_allowed",
        "test_execution_allowed",
        "subprocess_allowed",
        "shell_allowed",
        "dependency_install_allowed",
        "network_access_allowed",
        "model_provider_invocation_allowed",
        "external_agent_execution_allowed",
        "dominion_runtime_allowed",
    ):
        assert getattr(decision, name) is False
        with pytest.raises(ValueError):
            build_repair_proposal_permission_decision(**{name: True})


def test_risk_register_no_execution_guarantee_roadmap_and_readiness():
    risk = build_repair_proposal_risk_register()
    guarantee = build_repair_proposal_no_execution_guarantee()
    roadmap = build_v038_roadmap_overview()
    report = build_v0380_readiness_report()
    required_risks = {
        RepairProposalRiskKind.REPAIR_EXECUTION_CONFUSION_RISK,
        RepairProposalRiskKind.PATCH_PROPOSAL_CONFUSION_RISK,
        RepairProposalRiskKind.SOURCE_READ_SCOPE_RISK,
        RepairProposalRiskKind.INSUFFICIENT_EVIDENCE_RISK,
        RepairProposalRiskKind.DO_NOTHING_OMISSION_RISK,
        RepairProposalRiskKind.HUMAN_REVIEW_OMISSION_RISK,
        RepairProposalRiskKind.AUTOMATIC_REPAIR_RISK,
        RepairProposalRiskKind.RETRY_LOOP_RISK,
        RepairProposalRiskKind.MULTI_CYCLE_LOOP_RISK,
        RepairProposalRiskKind.MODEL_PROVIDER_INVOCATION_RISK,
        RepairProposalRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
        RepairProposalRiskKind.DOMINION_RUNTIME_RISK,
    }
    assert required_risks.issubset({RepairProposalRiskKind(item) for item in risk.risk_kinds})
    for field in fields(RepairProposalNoExecutionGuarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    for index in range(10):
        assert any(f"v0.38.{index}" in item for item in roadmap.roadmap_items)
    assert v0380_readiness_report_is_not_execution_ready(report)
    assert report.ready_for_v0381_repair_proposal_evidence_contract
    assert report.ready_for_bounded_repair_proposal_boundary
    for name in _unsafe_flag_names(V0380ReadinessReport) + ["production_certified"]:
        assert getattr(report, name) is False
        with pytest.raises(ValueError):
            build_v0380_readiness_report(**{name: True})


def test_helpers_do_not_contain_runtime_execution_patterns():
    import chanta_core.agent_runtime.repair_proposal_boundary as module

    source = inspect.getsource(module)
    forbidden = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.read_text",
        "Path.read_bytes",
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
        "apply_patch(",
    ]
    for pattern in forbidden:
        assert pattern not in source
