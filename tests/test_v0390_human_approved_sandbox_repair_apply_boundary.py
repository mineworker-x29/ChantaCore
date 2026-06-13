import inspect

import pytest

from chanta_core.agent_runtime import (
    AgentToSubagentPromptBoundary,
    HumanApprovedSandboxRepairApplyBoundary,
    ProcessStateDrivenNextActionBoundary,
    RepairApplyBoundaryDecision,
    RepairApplyBoundaryDecisionKind,
    RepairApplyBoundaryFlagSet,
    RepairApplyBoundaryKind,
    RepairApplyBoundaryMode,
    RepairApplyBoundaryNoExecutionGuarantee,
    RepairApplyBoundaryPolicy,
    RepairApplyBoundaryReadinessLevel,
    RepairApplyBoundaryRiskKind,
    RepairApplyBoundaryRunPreview,
    RepairApplyBoundarySourceKind,
    RepairApplyBoundarySourceRef,
    RepairApplyBoundaryStatus,
    RepairApplyBoundaryValidationFinding,
    RepairApplyBoundaryValidationReport,
    SelfPromptingMissionLoopBoundary,
    SelfPromptingMissionLoopBoundaryKind,
    V0390ReadinessReport,
    build_agent_to_subagent_prompt_boundary,
    build_human_approved_sandbox_repair_apply_boundary,
    build_process_state_driven_next_action_boundary,
    build_repair_apply_boundary_decision,
    build_repair_apply_boundary_flags,
    build_repair_apply_boundary_no_execution_guarantee,
    build_repair_apply_boundary_policy,
    build_repair_apply_boundary_run_preview,
    build_repair_apply_boundary_source_ref,
    build_repair_apply_boundary_validation_finding,
    build_repair_apply_boundary_validation_report,
    build_self_prompting_mission_loop_boundary,
    build_v0390_readiness_report,
    default_repair_apply_boundary_policy,
    next_action_boundary_is_not_next_action_execution,
    repair_apply_boundary_flags_preserve_no_execution,
    repair_apply_boundary_policy_blocks_apply_and_execution,
    self_prompting_boundary_is_not_self_execution,
    subagent_prompt_boundary_is_not_invocation,
    v0390_readiness_report_is_not_execution_ready,
)
from chanta_core.agent_runtime import repair_apply_boundary as boundary_module


EXPECTED_MODE_VALUES = {
    "human_approved_sandbox_repair_apply_boundary",
    "approval_artifact_boundary",
    "sandbox_workspace_isolation_boundary",
    "sandbox_patch_materialization_boundary",
    "sandbox_repair_apply_boundary",
    "post_apply_controlled_retest_boundary",
    "before_after_repair_comparison_boundary",
    "pi_native_repair_process_state_boundary",
    "self_prompting_mission_loop_boundary",
    "process_state_driven_next_action_boundary",
    "agent_to_subagent_prompt_boundary",
    "human_handoff_prompt_boundary",
    "future_v039_stage_gate",
    "blocked",
    "no_op",
    "unknown",
}

EXPECTED_SOURCE_KIND_VALUES = {
    "v0389_consolidation_report",
    "v0389_release_manifest",
    "v0389_handoff_packet",
    "v0388_cli_surface_report",
    "v0387_loop_packet",
    "v0386_human_review_packet",
    "v0385_safety_report",
    "v0384_proposed_patch_envelope",
    "v0383_scope_plan",
    "v0382_source_context_snapshot",
    "v0381_evidence_bundle",
    "v0380_boundary",
    "loop_engineering_note",
    "pi_native_design_note",
    "manual_operator_note",
    "test_fixture",
    "unknown",
}

EXPECTED_STATUS_VALUES = {
    "unknown",
    "draft",
    "boundary_defined",
    "boundary_defined_with_warnings",
    "ready_for_v0391_approval_artifact_intake",
    "ready_for_v0392_sandbox_workspace_isolation",
    "ready_for_v0393_sandbox_patch_materialization",
    "ready_for_v0394_post_apply_retest",
    "ready_for_v0395_before_after_comparison",
    "ready_for_v0396_process_state_reconstruction",
    "ready_for_v0397_self_prompting_draft",
    "ready_for_v0398_cli_surface",
    "ready_for_v0399_consolidation",
    "blocked",
    "review_required",
    "no_op",
    "safe_failed",
}

EXPECTED_READINESS_VALUES = {
    "not_ready",
    "apply_boundary_ready",
    "approval_boundary_ready",
    "sandbox_isolation_boundary_ready",
    "patch_materialization_boundary_ready",
    "sandbox_apply_boundary_ready",
    "retest_boundary_ready",
    "outcome_comparison_boundary_ready",
    "pi_process_state_boundary_ready",
    "self_prompting_loop_boundary_ready",
    "next_action_draft_boundary_ready",
    "subagent_prompt_boundary_ready",
    "human_handoff_boundary_ready",
    "v039_track_boundary_ready",
    "blocked",
    "future_track",
}

EXPECTED_DECISION_VALUES = {
    "allow_boundary_definition",
    "allow_approval_artifact_boundary",
    "allow_sandbox_workspace_isolation_boundary",
    "allow_sandbox_patch_materialization_boundary",
    "allow_sandbox_apply_boundary",
    "allow_post_apply_retest_boundary",
    "allow_before_after_comparison_boundary",
    "allow_pi_process_state_boundary",
    "allow_self_prompting_loop_boundary",
    "allow_next_action_draft_boundary",
    "allow_agent_to_subagent_prompt_boundary",
    "allow_human_handoff_boundary",
    "allow_future_v039_stage_gate",
    "choose_do_nothing",
    "choose_human_review_required",
    "deny",
    "block",
    "no_op",
    "require_review",
    "future_gate_required",
    "unknown",
}

EXPECTED_RISK_VALUES = {
    "approval_confusion_risk",
    "apply_permission_confusion_risk",
    "sandbox_live_confusion_risk",
    "self_prompt_execution_confusion_risk",
    "next_action_auto_execution_risk",
    "subagent_auto_invocation_risk",
    "autonomous_loop_runtime_risk",
    "retry_loop_risk",
    "multi_cycle_loop_risk",
    "automatic_repair_risk",
    "test_execution_confusion_risk",
    "process_state_correctness_overclaim_risk",
    "pig_recommendation_authority_confusion_risk",
    "live_workspace_apply_risk",
    "live_workspace_write_risk",
    "patch_application_risk",
    "apply_patch_risk",
    "git_apply_risk",
    "external_agent_execution_risk",
    "model_provider_invocation_risk",
    "dominion_runtime_risk",
    "production_certification_confusion_risk",
    "token_cost_loop_explosion_risk",
    "cognitive_surrender_risk",
    "unknown",
}

EXPECTED_BOUNDARY_KIND_VALUES = {
    "human_approved_sandbox_apply",
    "approval_artifact_intake",
    "approval_scope_validation",
    "sandbox_workspace_isolation",
    "sandbox_patch_materialization",
    "sandbox_repair_apply",
    "post_apply_controlled_retest",
    "before_after_repair_outcome_comparison",
    "repair_effectiveness_assessment",
    "repair_process_state_projection",
    "ocel_style_repair_event_envelope",
    "ocpx_style_repair_state_reconstruction",
    "pig_repair_diagnostic_recommendation",
    "self_prompting_mission_loop",
    "process_state_driven_next_action_draft",
    "agent_to_subagent_prompt_draft",
    "human_handoff_prompt",
    "no_autonomous_continuation",
    "no_live_apply",
    "unknown",
}

EXPECTED_SELF_PROMPTING_KIND_VALUES = {
    "mission_objective_ref",
    "process_state_projection",
    "trace_history_ref",
    "verification_contract_ref",
    "policy_boundary_ref",
    "pig_recommendation_ref",
    "next_action_decision_boundary",
    "prompt_draft_boundary",
    "action_request_draft_boundary",
    "subagent_verification_prompt_draft_boundary",
    "human_handoff_boundary",
    "no_self_execution_boundary",
    "no_subagent_invocation_boundary",
    "no_autonomous_continuation_boundary",
    "unknown",
}

SAFE_FLAG_TRUE_FIELDS = set(boundary_module.BOUNDARY_FLAG_NAMES)


def _unsafe_flag_fields():
    flags = build_repair_apply_boundary_flags()
    return [
        name
        for name, value in flags.__dict__.items()
        if isinstance(value, bool) and name not in SAFE_FLAG_TRUE_FIELDS
    ]


def test_all_v0390_enum_values_exist():
    assert {item.value for item in RepairApplyBoundaryMode} == EXPECTED_MODE_VALUES
    assert {item.value for item in RepairApplyBoundarySourceKind} == EXPECTED_SOURCE_KIND_VALUES
    assert {item.value for item in RepairApplyBoundaryStatus} == EXPECTED_STATUS_VALUES
    assert {item.value for item in RepairApplyBoundaryReadinessLevel} == EXPECTED_READINESS_VALUES
    assert {item.value for item in RepairApplyBoundaryDecisionKind} == EXPECTED_DECISION_VALUES
    assert {item.value for item in RepairApplyBoundaryRiskKind} == EXPECTED_RISK_VALUES
    assert {item.value for item in RepairApplyBoundaryKind} == EXPECTED_BOUNDARY_KIND_VALUES
    assert {item.value for item in SelfPromptingMissionLoopBoundaryKind} == EXPECTED_SELF_PROMPTING_KIND_VALUES


def test_repair_apply_boundary_flags_allow_boundary_and_future_stage_only():
    flags = build_repair_apply_boundary_flags()
    assert isinstance(flags, RepairApplyBoundaryFlagSet)
    assert flags.v039_boundary_layer_constructed is True
    assert flags.ready_for_v0391_approval_artifact_intake is True
    assert flags.ready_for_v0399_consolidation is True
    assert flags.ready_for_human_approved_sandbox_repair_apply_boundary is True
    assert flags.ready_for_self_prompting_mission_loop_boundary is True
    assert repair_apply_boundary_flags_preserve_no_execution(flags)
    for field_name in _unsafe_flag_fields():
        assert getattr(flags, field_name) is False


@pytest.mark.parametrize(
    "unsafe_field",
    [
        "ready_for_execution",
        "ready_for_approval_artifact_intake",
        "ready_for_human_approval_capture",
        "ready_for_approval_grant",
        "ready_for_apply_permission",
        "ready_for_sandbox_repair_workspace_creation",
        "ready_for_sandbox_patch_materialization",
        "ready_for_sandbox_repair_apply",
        "ready_for_live_workspace_apply",
        "ready_for_patch_file_write",
        "ready_for_file_edit",
        "ready_for_patch_application",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_post_apply_controlled_retest",
        "ready_for_repair_test_execution",
        "ready_for_self_prompt_generation",
        "ready_for_self_prompt_auto_execution",
        "ready_for_next_action_auto_execution",
        "ready_for_agent_to_subagent_prompt_generation",
        "ready_for_subagent_auto_invocation",
        "ready_for_external_agent_execution",
        "ready_for_model_provider_invocation",
        "ready_for_autonomous_loop_runtime",
        "ready_for_retry_loop",
        "ready_for_multi_cycle_loop",
        "ready_for_repair_execution",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_network_access",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true_values(unsafe_field):
    with pytest.raises(ValueError):
        build_repair_apply_boundary_flags(**{unsafe_field: True})


def test_source_ref_is_metadata_only():
    source_ref = build_repair_apply_boundary_source_ref()
    assert isinstance(source_ref, RepairApplyBoundarySourceRef)
    assert source_ref.source_kind == RepairApplyBoundarySourceKind.V0389_HANDOFF_PACKET
    assert source_ref.evidence_refs


def test_policy_allows_boundary_definitions_and_blocks_runtime():
    policy = default_repair_apply_boundary_policy()
    assert isinstance(policy, RepairApplyBoundaryPolicy)
    assert policy.allow_boundary_definition is True
    assert policy.allow_future_stage_gate_metadata is True
    assert policy.allow_approval_artifact_intake_boundary is True
    assert policy.allow_sandbox_workspace_isolation_boundary is True
    assert policy.allow_sandbox_patch_materialization_boundary is True
    assert policy.allow_sandbox_apply_boundary is True
    assert policy.allow_post_apply_retest_boundary is True
    assert policy.allow_before_after_comparison_boundary is True
    assert policy.allow_process_state_boundary is True
    assert policy.allow_self_prompting_boundary is True
    assert policy.allow_next_action_draft_boundary is True
    assert policy.allow_agent_to_subagent_prompt_boundary is True
    assert policy.allow_human_handoff_boundary is True
    assert policy.require_human_approval_for_future_apply is True
    assert policy.require_sandbox_only_for_future_apply is True
    assert policy.require_no_live_apply is True
    assert policy.require_self_prompting_no_execution_boundary is True
    assert policy.require_subagent_no_invocation_boundary is True
    assert policy.require_human_handoff_boundary is True
    assert repair_apply_boundary_policy_blocks_apply_and_execution(policy)

    for field_name in boundary_module.UNSAFE_POLICY_ALLOW_NAMES:
        assert getattr(policy, field_name) is False
        with pytest.raises(ValueError):
            build_repair_apply_boundary_policy(**{field_name: True})


def test_human_approved_sandbox_boundary_is_boundary_only():
    boundary = build_human_approved_sandbox_repair_apply_boundary()
    assert isinstance(boundary, HumanApprovedSandboxRepairApplyBoundary)
    assert boundary.required_human_approval_future_gate is True
    assert boundary.sandbox_only_future_gate is True
    assert boundary.live_workspace_apply_blocked is True
    assert boundary.approval_capture_blocked_in_v0390 is True
    assert boundary.apply_execution_blocked_in_v0390 is True
    assert boundary.test_execution_blocked_in_v0390 is True
    assert boundary.repair_execution_blocked_in_v0390 is True
    assert boundary.future_v0391_gate_open is True
    assert boundary.future_v0392_gate_open is True
    assert boundary.future_v0393_gate_open is True

    with pytest.raises(ValueError):
        build_human_approved_sandbox_repair_apply_boundary(apply_execution_blocked_in_v0390=False)


def test_self_prompting_mission_loop_boundary_uses_pi_native_terms_and_blocks_execution():
    boundary = build_self_prompting_mission_loop_boundary()
    assert isinstance(boundary, SelfPromptingMissionLoopBoundary)
    assert boundary.canonical_name == "Self-Prompting Mission Loop"
    assert "Loop Engineering as top-level ChantaCore concept" in boundary.rejected_external_terms
    for term in [
        "Self-Prompting Mission Loop",
        "PI-native Mission Execution Loop",
        "Process-State-Driven Self-Prompting",
        "Agent-to-Subagent Prompting Cycle",
    ]:
        assert term in boundary.accepted_internal_terms
    assert boundary.process_state_required is True
    assert boundary.mission_objective_required is True
    assert boundary.verification_contract_required is True
    assert boundary.policy_boundary_required is True
    assert boundary.human_handoff_required is True
    assert boundary.self_prompt_generation_blocked_in_v0390 is True
    assert boundary.self_prompt_auto_execution_blocked is True
    assert boundary.next_action_auto_execution_blocked is True
    assert boundary.subagent_prompt_generation_blocked_in_v0390 is True
    assert boundary.subagent_auto_invocation_blocked is True
    assert boundary.autonomous_continuation_blocked is True
    assert boundary.model_provider_invocation_blocked is True
    assert boundary.external_agent_execution_blocked is True
    assert self_prompting_boundary_is_not_self_execution(boundary)

    with pytest.raises(ValueError):
        build_self_prompting_mission_loop_boundary(canonical_name="Loop Engineering")


def test_next_action_and_subagent_boundaries_are_not_execution_or_invocation():
    next_action = build_process_state_driven_next_action_boundary()
    assert isinstance(next_action, ProcessStateDrivenNextActionBoundary)
    assert next_action.oc_el_style_event_envelope_future_gate is True
    assert next_action.ocpx_state_reconstruction_future_gate is True
    assert next_action.pig_recommendation_future_gate is True
    assert next_action.next_action_draft_future_gate is True
    assert next_action.execution_blocked is True
    assert next_action_boundary_is_not_next_action_execution(next_action)

    subagent = build_agent_to_subagent_prompt_boundary()
    assert isinstance(subagent, AgentToSubagentPromptBoundary)
    assert subagent.future_prompt_draft_allowed is True
    assert subagent.future_verification_prompt_draft_allowed is True
    assert subagent.subagent_invocation_allowed_now is False
    assert subagent.external_agent_invocation_allowed_now is False
    assert subagent.model_provider_invocation_allowed_now is False
    assert subagent.automatic_dispatch_allowed_now is False
    assert subagent.human_handoff_required is True
    assert subagent_prompt_boundary_is_not_invocation(subagent)

    with pytest.raises(ValueError):
        build_agent_to_subagent_prompt_boundary(subagent_invocation_allowed_now=True)


def test_boundary_decision_allows_future_readiness_but_no_runtime_now():
    decision = build_repair_apply_boundary_decision()
    assert isinstance(decision, RepairApplyBoundaryDecision)
    assert decision.ready_for_v0391 is True
    assert decision.ready_for_v0399 is True
    for field_name in boundary_module.UNSAFE_DECISION_NAMES:
        assert getattr(decision, field_name) is False

    with pytest.raises(ValueError):
        build_repair_apply_boundary_decision(apply_allowed_now=True)


def test_validation_report_run_preview_and_no_execution_guarantee():
    finding = build_repair_apply_boundary_validation_finding()
    assert isinstance(finding, RepairApplyBoundaryValidationFinding)
    assert finding.blocked is True

    report = build_repair_apply_boundary_validation_report()
    assert isinstance(report, RepairApplyBoundaryValidationReport)
    assert report.boundary_only_confirmed is True
    assert report.no_approval_capture_confirmed is True
    assert report.no_apply_confirmed is True
    assert report.no_test_execution_confirmed is True
    assert report.no_self_prompt_execution_confirmed is True
    assert report.no_subagent_invocation_confirmed is True
    assert report.no_external_agent_confirmed is True
    assert report.no_model_provider_confirmed is True
    assert report.no_repair_execution_confirmed is True
    assert report.no_dominion_confirmed is True
    assert report.no_production_certification_confirmed is True

    preview = build_repair_apply_boundary_run_preview()
    assert isinstance(preview, RepairApplyBoundaryRunPreview)
    assert preview.preview_only is True
    assert preview.ready_for_execution is False

    guarantee = build_repair_apply_boundary_no_execution_guarantee()
    assert isinstance(guarantee, RepairApplyBoundaryNoExecutionGuarantee)
    for name, value in guarantee.__dict__.items():
        if name.startswith("no_"):
            assert value is True


def test_v0390_readiness_report_future_ready_but_not_execution_ready():
    report = build_v0390_readiness_report()
    assert isinstance(report, V0390ReadinessReport)
    assert report.ready_for_v039_track is True
    assert report.ready_for_v0391_approval_artifact_intake is True
    assert report.ready_for_v0392_sandbox_workspace_isolation is True
    assert report.ready_for_v0393_sandbox_patch_materialization_apply is True
    assert report.ready_for_v0394_post_apply_retest is True
    assert report.ready_for_v0395_before_after_comparison is True
    assert report.ready_for_v0396_pi_process_state_reconstruction is True
    assert report.ready_for_v0397_self_prompting_next_action_draft is True
    assert report.ready_for_v0398_cli_surface is True
    assert report.ready_for_v0399_consolidation is True
    for field_name in boundary_module.UNSAFE_REPORT_NAMES:
        assert getattr(report, field_name) is False
    assert v0390_readiness_report_is_not_execution_ready(report)

    with pytest.raises(ValueError):
        build_v0390_readiness_report(apply_enabled=True)
    with pytest.raises(ValueError):
        build_v0390_readiness_report(self_prompt_generation_enabled=True)
    with pytest.raises(ValueError):
        build_v0390_readiness_report(subagent_invocation_enabled=True)
    with pytest.raises(ValueError):
        build_v0390_readiness_report(ready_for_execution=True)


def test_helpers_are_pure_boundary_helpers_without_runtime_patterns():
    source = inspect.getsource(boundary_module)
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
        "human_approval_present=True",
        "apply_allowed=True",
        "sandbox_apply_allowed=True",
        "production_certified=True",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

