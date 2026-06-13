from __future__ import annotations

import pytest

from chanta_core.agent_runtime.repair_self_prompting import (
    RepairAgentToSubagentPromptDraft,
    RepairHumanHandoffPrompt,
    RepairNextActionCandidate,
    RepairNextActionDecision,
    RepairNextActionDraft,
    RepairNextActionKind,
    RepairPromptDraftConfidenceLevel,
    RepairPromptDraftDisposition,
    RepairPromptSafetyAssessment,
    RepairSelfPromptDraft,
    RepairSelfPromptDraftKind,
    RepairSelfPromptingDecision,
    RepairSelfPromptingDecisionKind,
    RepairSelfPromptingDraftOnlyGuarantee,
    RepairSelfPromptingDraftPacket,
    RepairSelfPromptingFlagSet,
    RepairSelfPromptingInput,
    RepairSelfPromptingLoopContext,
    RepairSelfPromptingMode,
    RepairSelfPromptingPolicy,
    RepairSelfPromptingReadinessLevel,
    RepairSelfPromptingReport,
    RepairSelfPromptingRiskKind,
    RepairSelfPromptingSourceKind,
    RepairSelfPromptingSourceRef,
    RepairSelfPromptingStatus,
    RepairSubagentPromptDraftKind,
    RepairSubagentVerificationRequestDraft,
    V0397ReadinessReport,
    assess_repair_prompt_safety,
    build_repair_agent_to_subagent_prompt_draft,
    build_repair_human_handoff_prompt,
    build_repair_next_action_candidate,
    build_repair_next_action_decision,
    build_repair_next_action_draft,
    build_repair_prompt_safety_assessment,
    build_repair_self_prompt_draft,
    build_repair_self_prompting_decision,
    build_repair_self_prompting_draft_only_guarantee,
    build_repair_self_prompting_draft_packet,
    build_repair_self_prompting_flags,
    build_repair_self_prompting_input,
    build_repair_self_prompting_loop_context,
    build_repair_self_prompting_policy,
    build_repair_self_prompting_report,
    build_repair_self_prompting_source_ref,
    build_repair_self_prompting_validation_report,
    build_repair_subagent_verification_request_draft,
    build_v0397_readiness_report,
    create_repair_human_handoff_prompt,
    create_repair_next_action_candidates,
    create_repair_self_prompting_draft_packet,
    create_repair_self_prompting_loop_context,
    create_repair_self_prompting_report,
    decide_repair_next_action,
    decide_repair_self_prompting,
    default_repair_self_prompting_policy,
    draft_repair_agent_to_subagent_prompt,
    draft_repair_next_action,
    draft_repair_self_prompt,
    draft_repair_subagent_verification_request,
    repair_self_prompt_draft_is_not_execution,
    repair_self_prompting_flags_preserve_no_execution,
    repair_self_prompting_packet_is_draft_only,
    repair_self_prompting_policy_blocks_execution,
    repair_subagent_prompt_draft_is_not_invocation,
    v0397_readiness_report_is_not_execution_ready,
)


def test_v0397_enum_values() -> None:
    assert [item.value for item in RepairSelfPromptingMode] == [
        "self_prompting_next_action_draft",
        "process_state_driven_next_action_candidate",
        "process_state_driven_next_action_decision",
        "self_prompt_draft_generation",
        "agent_to_subagent_prompt_draft",
        "subagent_verification_request_draft",
        "prompt_safety_assessment",
        "human_handoff_prompt",
        "future_cli_loop_state_surface_input",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in RepairSelfPromptingSourceKind] == [
        "v0396_process_state_reconstruction_report",
        "v0396_mission_state_projection",
        "v0396_pig_diagnostic_input_context",
        "v0396_ocpx_state_projection",
        "v0396_process_state_decision",
        "v0395_outcome_comparison_report",
        "v0395_effectiveness_assessment",
        "v0395_regression_signal",
        "v0395_do_nothing_comparison",
        "v0394_post_apply_retest_result",
        "v0393_sandbox_apply_result",
        "v0392_workspace_isolation_decision",
        "v0391_approval_process_state_gate",
        "manual_operator_note",
        "test_fixture",
        "unknown",
    ]
    assert "draft_packet_created" in {item.value for item in RepairSelfPromptingStatus}
    assert "design_handoff_ready_for_v0398" in {item.value for item in RepairSelfPromptingReadinessLevel}
    assert "reject_model_provider_request" in {item.value for item in RepairSelfPromptingDecisionKind}
    assert "prompt_injection_risk" in {item.value for item in RepairSelfPromptingRiskKind}
    assert "human_review" in {item.value for item in RepairNextActionKind}
    assert "mission_continuation_prompt_draft" in {item.value for item in RepairSelfPromptDraftKind}
    assert "verifier_subagent_prompt_draft" in {item.value for item in RepairSubagentPromptDraftKind}
    assert "draft_created" in {item.value for item in RepairPromptDraftDisposition}
    assert "medium" in {item.value for item in RepairPromptDraftConfidenceLevel}


def test_flags_allow_draft_metadata_and_future_cli_input_only() -> None:
    flags = build_repair_self_prompting_flags()

    assert isinstance(flags, RepairSelfPromptingFlagSet)
    assert flags.self_prompting_layer_constructed is True
    assert flags.self_prompting_mission_loop_context_available is True
    assert flags.process_state_driven_next_action_candidate_available is True
    assert flags.process_state_driven_next_action_decision_available is True
    assert flags.self_prompt_draft_available is True
    assert flags.agent_to_subagent_prompt_draft_available is True
    assert flags.subagent_verification_request_draft_available is True
    assert flags.prompt_safety_assessment_available is True
    assert flags.human_handoff_prompt_available is True
    assert flags.future_cli_loop_state_surface_input_available is True
    assert flags.ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface is True
    assert flags.ready_for_self_prompt_draft_generation is True
    assert flags.ready_for_agent_to_subagent_prompt_draft_generation is True
    assert flags.ready_for_prompt_safety_assessment is True
    assert repair_self_prompting_flags_preserve_no_execution(flags)

    assert flags.ready_for_execution is False
    assert flags.ready_for_prompt_submission_to_model is False
    assert flags.ready_for_model_provider_invocation is False
    assert flags.ready_for_self_prompt_runtime_generation is False
    assert flags.ready_for_self_prompt_execution is False
    assert flags.ready_for_next_action_execution is False
    assert flags.ready_for_subagent_invocation is False
    assert flags.ready_for_external_agent_execution is False
    assert flags.ready_for_autonomous_loop_runtime is False
    assert flags.ready_for_retry_loop is False
    assert flags.ready_for_multi_cycle_loop is False
    assert flags.ready_for_repair_execution is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_dominion_runtime is False
    assert flags.production_certified is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_model_provider_invocation",
        "ready_for_prompt_submission_to_model",
        "ready_for_self_prompt_runtime_generation",
        "ready_for_self_prompt_execution",
        "ready_for_self_prompt_auto_execution",
        "ready_for_next_action_execution",
        "ready_for_next_action_auto_execution",
        "ready_for_agent_to_subagent_prompt_runtime_generation",
        "ready_for_subagent_invocation",
        "ready_for_subagent_auto_invocation",
        "ready_for_external_agent_execution",
        "ready_for_claude_code_invocation",
        "ready_for_codex_cli_invocation",
        "ready_for_autonomous_loop_runtime",
        "ready_for_retry_loop",
        "ready_for_multi_cycle_loop",
        "ready_for_repair_execution",
        "ready_for_test_execution",
        "ready_for_patch_application",
        "ready_for_persistent_trace_write",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_self_prompting_flags(**{field_name: True})


def test_policy_allows_drafts_and_blocks_execution_surfaces() -> None:
    policy = default_repair_self_prompting_policy()

    assert isinstance(policy, RepairSelfPromptingPolicy)
    assert policy.allow_loop_context is True
    assert policy.allow_next_action_candidate_generation is True
    assert policy.allow_next_action_decision is True
    assert policy.allow_self_prompt_draft_generation is True
    assert policy.allow_agent_to_subagent_prompt_draft_generation is True
    assert policy.allow_subagent_verification_request_draft_generation is True
    assert policy.allow_prompt_safety_assessment is True
    assert policy.allow_human_handoff_prompt is True
    assert policy.allow_future_cli_loop_state_surface_input is True
    assert policy.require_human_handoff is True
    assert policy.require_draft_only is True
    assert repair_self_prompting_policy_blocks_execution(policy)

    assert policy.allow_prompt_submission_to_model is False
    assert policy.allow_model_provider_invocation is False
    assert policy.allow_self_prompt_execution is False
    assert policy.allow_next_action_execution is False
    assert policy.allow_subagent_invocation is False
    assert policy.allow_external_agent_execution is False
    assert policy.allow_autonomous_loop_runtime is False
    assert policy.allow_retry_loop is False
    assert policy.allow_multi_cycle_loop is False
    assert policy.allow_repair_execution is False
    assert policy.allow_test_execution is False
    assert policy.allow_patch_application is False
    assert policy.allow_pig_recommendation_execution is False
    assert policy.allow_trace_persistence is False
    assert policy.allow_dominion_runtime is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_prompt_submission_to_model",
        "allow_model_provider_invocation",
        "allow_self_prompt_execution",
        "allow_next_action_execution",
        "allow_subagent_invocation",
        "allow_external_agent_execution",
        "allow_autonomous_loop_runtime",
        "allow_retry_loop",
        "allow_multi_cycle_loop",
        "allow_repair_execution",
        "allow_test_execution",
        "allow_patch_application",
        "allow_pig_recommendation_execution",
        "allow_trace_persistence",
        "allow_subprocess",
        "allow_shell",
        "allow_network_access",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_execution_allow(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_self_prompting_policy(**{field_name: True})


def test_input_and_source_refs_are_draft_request_metadata_only() -> None:
    source_ref = build_repair_self_prompting_source_ref()
    self_prompting_input = build_repair_self_prompting_input(source_refs=[source_ref])

    assert isinstance(source_ref, RepairSelfPromptingSourceRef)
    assert isinstance(self_prompting_input, RepairSelfPromptingInput)
    for action in [
        "prompt_submission",
        "model_provider_invocation",
        "prompt_execution",
        "next_action_execution",
        "subagent_invocation",
        "external_agent",
        "autonomous_loop",
        "retry_loop",
        "multi_cycle_loop",
        "repair_execution",
        "test_execution",
        "patch_application",
        "pig_execution",
        "trace_persistence",
        "Dominion",
    ]:
        assert action in self_prompting_input.prohibited_runtime_actions


def test_loop_context_candidate_and_decision_are_single_iteration_drafts() -> None:
    context = build_repair_self_prompting_loop_context()
    candidate = build_repair_next_action_candidate()
    decision = build_repair_next_action_decision()

    assert isinstance(context, RepairSelfPromptingLoopContext)
    assert context.canonical_name == "Self-Prompting Mission Loop"
    assert context.human_handoff_required is True
    assert context.max_iteration_count == 1
    assert context.current_iteration_index == 0
    assert context.autonomous_continuation_allowed is False
    assert context.retry_loop_allowed is False
    assert context.multi_cycle_loop_allowed is False

    assert isinstance(candidate, RepairNextActionCandidate)
    assert candidate.requires_human_review is True
    assert candidate.draft_only is True
    assert candidate.executable_now is False
    assert candidate.runtime_authority_granted is False

    assert isinstance(decision, RepairNextActionDecision)
    assert decision.human_handoff_required is True
    assert decision.do_nothing_considered is True
    assert decision.execution_allowed is False
    assert decision.auto_continue_allowed is False
    assert decision.subagent_invocation_allowed is False
    assert decision.model_invocation_allowed is False


def test_draft_artifacts_never_execute_or_invoke() -> None:
    next_action = build_repair_next_action_draft()
    self_prompt = build_repair_self_prompt_draft()
    subagent_prompt = build_repair_agent_to_subagent_prompt_draft()
    verification = build_repair_subagent_verification_request_draft()
    safety = build_repair_prompt_safety_assessment()
    handoff = build_repair_human_handoff_prompt()

    assert isinstance(next_action, RepairNextActionDraft)
    assert next_action.bounded is True
    assert next_action.redacted is True
    assert next_action.draft_only is True
    assert next_action.execution_allowed is False
    assert next_action.sent_to_model is False
    assert next_action.sent_to_tool is False
    assert next_action.sent_to_subagent is False

    assert isinstance(self_prompt, RepairSelfPromptDraft)
    assert self_prompt.bounded is True
    assert self_prompt.redacted is True
    assert self_prompt.draft_only is True
    assert self_prompt.submitted_to_model is False
    assert self_prompt.executed is False
    assert repair_self_prompt_draft_is_not_execution(self_prompt)

    assert isinstance(subagent_prompt, RepairAgentToSubagentPromptDraft)
    assert subagent_prompt.draft_only is True
    assert subagent_prompt.subagent_invoked is False
    assert subagent_prompt.external_agent_invoked is False
    assert subagent_prompt.model_invoked is False
    assert repair_subagent_prompt_draft_is_not_invocation(subagent_prompt)

    assert isinstance(verification, RepairSubagentVerificationRequestDraft)
    assert verification.bounded is True
    assert verification.draft_only is True
    assert verification.subagent_invocation_allowed is False
    assert verification.sent_to_subagent is False

    assert isinstance(safety, RepairPromptSafetyAssessment)
    assert safety.blocks_prompt_execution is True
    assert safety.blocks_model_invocation is True
    assert safety.blocks_subagent_invocation is True
    assert safety.blocks_auto_continue is True
    assert safety.requires_human_review is True
    assert safety.safe_as_draft is True
    assert safety.safe_to_execute is False

    assert isinstance(handoff, RepairHumanHandoffPrompt)
    assert handoff.human_action_required is True
    assert handoff.auto_continue_allowed is False


@pytest.mark.parametrize(
    ("builder", "field_name"),
    [
        (build_repair_self_prompt_draft, "submitted_to_model"),
        (build_repair_self_prompt_draft, "executed"),
        (build_repair_agent_to_subagent_prompt_draft, "subagent_invoked"),
        (build_repair_agent_to_subagent_prompt_draft, "model_invoked"),
        (build_repair_subagent_verification_request_draft, "sent_to_subagent"),
        (build_repair_prompt_safety_assessment, "safe_to_execute"),
    ],
)
def test_draft_artifacts_reject_runtime_flags(builder, field_name: str) -> None:
    with pytest.raises(ValueError):
        builder(**{field_name: True})


def test_draft_packet_decision_report_and_readiness_preserve_no_execution() -> None:
    packet = build_repair_self_prompting_draft_packet()
    decision = build_repair_self_prompting_decision()
    report = build_repair_self_prompting_report(draft_packet=packet, decision=decision)
    readiness = build_v0397_readiness_report(self_prompting_report=report)

    assert isinstance(packet, RepairSelfPromptingDraftPacket)
    assert packet.ready_for_future_cli_loop_state_surface_input is True
    assert packet.draft_only is True
    assert repair_self_prompting_packet_is_draft_only(packet)
    assert packet.submitted_to_model is False
    assert packet.prompt_executed is False
    assert packet.next_action_executed is False
    assert packet.subagent_invoked is False
    assert packet.external_agent_invoked is False
    assert packet.model_invoked is False
    assert packet.autonomous_loop_continued is False
    assert packet.retry_loop_started is False
    assert packet.multi_cycle_loop_started is False
    assert packet.repair_executed is False
    assert packet.tests_run is False
    assert packet.patch_applied is False
    assert packet.trace_persisted is False
    assert packet.dominion_runtime_invoked is False
    assert packet.production_certified is False
    assert packet.ready_for_execution is False

    assert isinstance(decision, RepairSelfPromptingDecision)
    assert decision.ready_for_future_cli_loop_state_surface_input is True
    assert decision.draft_generation_allowed_now is True
    assert decision.prompt_execution_allowed_now is False
    assert decision.next_action_execution_allowed_now is False
    assert decision.model_provider_invocation_allowed_now is False
    assert decision.subagent_invocation_allowed_now is False
    assert decision.external_agent_allowed_now is False
    assert decision.autonomous_loop_allowed_now is False
    assert decision.retry_loop_allowed_now is False
    assert decision.multi_cycle_loop_allowed_now is False
    assert decision.repair_execution_allowed_now is False
    assert decision.test_execution_allowed_now is False
    assert decision.patch_application_allowed_now is False
    assert decision.trace_persistence_allowed_now is False
    assert decision.dominion_runtime_allowed_now is False
    assert decision.production_certified is False

    assert isinstance(report, RepairSelfPromptingReport)
    assert report.ready_for_future_cli_loop_state_surface_input is True
    assert report.draft_generation_completed is True
    assert report.prompt_submitted_to_model is False
    assert report.prompt_executed is False
    assert report.next_action_executed is False
    assert report.subagent_invoked is False
    assert report.model_invoked is False
    assert report.external_agent_invoked is False
    assert report.autonomous_loop_continued is False
    assert report.repair_executed is False
    assert report.tests_run is False
    assert report.patch_applied is False
    assert report.trace_persisted is False
    assert report.dominion_runtime_invoked is False
    assert report.production_certified is False
    assert report.ready_for_execution is False

    assert isinstance(readiness, V0397ReadinessReport)
    assert readiness.ready_for_v0398_cli_sandbox_repair_apply_retest_loop_state_surface is True
    assert readiness.ready_for_self_prompting_next_action_draft_contract is True
    assert readiness.ready_for_self_prompt_draft_generation is True
    assert readiness.prompt_submission_enabled is False
    assert readiness.prompt_execution_enabled is False
    assert readiness.model_invocation_enabled is False
    assert readiness.subagent_invocation_enabled is False
    assert readiness.external_agent_enabled is False
    assert readiness.autonomous_loop_enabled is False
    assert readiness.retry_loop_enabled is False
    assert readiness.multi_cycle_loop_enabled is False
    assert readiness.repair_execution_enabled is False
    assert readiness.test_execution_enabled is False
    assert readiness.patch_application_enabled is False
    assert readiness.trace_persistence_enabled is False
    assert readiness.dominion_runtime_enabled is False
    assert readiness.production_certified is False
    assert readiness.ready_for_execution is False
    assert v0397_readiness_report_is_not_execution_ready(readiness)


@pytest.mark.parametrize(
    ("builder", "field_name"),
    [
        (build_repair_self_prompting_draft_packet, "autonomous_loop_continued"),
        (build_repair_self_prompting_draft_packet, "repair_executed"),
        (build_repair_self_prompting_draft_packet, "ready_for_execution"),
        (build_repair_self_prompting_report, "prompt_submitted_to_model"),
        (build_repair_self_prompting_report, "ready_for_execution"),
        (build_v0397_readiness_report, "prompt_execution_enabled"),
        (build_v0397_readiness_report, "model_invocation_enabled"),
        (build_v0397_readiness_report, "ready_for_execution"),
    ],
)
def test_packet_report_readiness_reject_runtime_flags(builder, field_name: str) -> None:
    with pytest.raises(ValueError):
        builder(**{field_name: True})


def test_validation_and_draft_only_guarantee_confirm_no_runtime() -> None:
    validation = build_repair_self_prompting_validation_report()
    guarantee = build_repair_self_prompting_draft_only_guarantee()

    assert validation.draft_only_confirmed is True
    assert validation.no_model_invocation_confirmed is True
    assert validation.no_prompt_submission_confirmed is True
    assert validation.no_prompt_execution_confirmed is True
    assert validation.no_next_action_execution_confirmed is True
    assert validation.no_subagent_invocation_confirmed is True
    assert validation.no_external_agent_confirmed is True
    assert validation.no_autonomous_loop_confirmed is True
    assert validation.no_retry_loop_confirmed is True
    assert validation.no_multi_cycle_loop_confirmed is True
    assert validation.no_repair_execution_confirmed is True
    assert validation.no_test_execution_confirmed is True
    assert validation.no_patch_application_confirmed is True
    assert validation.no_trace_persistence_confirmed is True
    assert validation.no_pig_execution_confirmed is True
    assert validation.no_dominion_runtime_confirmed is True
    assert validation.no_production_certification_confirmed is True

    assert isinstance(guarantee, RepairSelfPromptingDraftOnlyGuarantee)
    assert guarantee.no_prompt_submission_to_model is True
    assert guarantee.no_model_invocation is True
    assert guarantee.no_prompt_execution is True
    assert guarantee.no_self_prompt_auto_execution is True
    assert guarantee.no_next_action_execution is True
    assert guarantee.no_subagent_invocation is True
    assert guarantee.no_external_agent is True
    assert guarantee.no_tool_execution is True
    assert guarantee.no_autonomous_loop is True
    assert guarantee.no_retry_loop is True
    assert guarantee.no_multi_cycle_loop is True
    assert guarantee.no_repair_execution is True
    assert guarantee.no_test_execution is True
    assert guarantee.no_patch_application is True
    assert guarantee.no_trace_persistence is True
    assert guarantee.no_pig_execution is True
    assert guarantee.no_dominion_runtime is True
    assert guarantee.no_production_certification is True


def test_pure_helper_pipeline_creates_bounded_drafts_without_execution() -> None:
    self_prompting_input = build_repair_self_prompting_input()
    context = create_repair_self_prompting_loop_context(self_prompting_input)
    candidates = create_repair_next_action_candidates(context)
    decision = decide_repair_next_action(candidates)
    next_action_draft = draft_repair_next_action(decision, max_chars=120)
    self_prompt_draft = draft_repair_self_prompt(context, max_chars=120)
    subagent_prompt = draft_repair_agent_to_subagent_prompt(context, max_chars=120)
    verification_request = draft_repair_subagent_verification_request(subagent_prompt)
    safety = assess_repair_prompt_safety([self_prompt_draft.self_prompt_draft_id, subagent_prompt.subagent_prompt_draft_id])
    handoff = create_repair_human_handoff_prompt([next_action_draft.next_action_draft_id, self_prompt_draft.self_prompt_draft_id])
    packet = create_repair_self_prompting_draft_packet(self_prompting_input)
    report = create_repair_self_prompting_report(self_prompting_input)

    assert len(candidates) == 3
    assert len(next_action_draft.action_request_text) <= 120
    assert len(self_prompt_draft.prompt_text) <= 120
    assert len(subagent_prompt.prompt_text) <= 120
    assert verification_request.sent_to_subagent is False
    assert safety.safe_to_execute is False
    assert handoff.auto_continue_allowed is False
    assert repair_self_prompting_packet_is_draft_only(packet)
    assert report.prompt_submitted_to_model is False
    assert report.ready_for_execution is False
    assert decide_repair_self_prompting(packet).draft_generation_allowed_now is True
