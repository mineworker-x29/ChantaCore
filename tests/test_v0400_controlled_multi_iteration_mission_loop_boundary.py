from __future__ import annotations

from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_boundary import (
    DeniedRuntimeActionMetadata,
    HumanCheckpointGate,
    IterationState,
    IterationStatus,
    LoopDecisionKind,
    LoopDecisionRecord,
    MissionLoopEnvelope,
    PromptSubmissionBoundary,
    ProviderBoundaryGate,
    RuntimeActionType,
    SafeAlternative,
    SimulatedMultiIterationLoopPacket,
    StopConditionContract,
    VerifierSubagentBoundary,
    V040ReadinessReport,
    create_default_mission_loop_envelope,
    create_denied_runtime_action,
    create_initial_iteration_state,
    create_prompt_submission_boundary,
    create_provider_boundary_gate,
    create_v040_readiness_report,
    create_verifier_subagent_boundary,
    evaluate_loop_budget,
    evaluate_stop_conditions,
    iteration_state_is_not_execution_permission,
    prompt_submission_boundary_is_not_submission,
    provider_boundary_gate_is_not_invocation,
    require_human_checkpoint_for_second_iteration,
    simulated_packet_is_dry_run_only,
    simulate_multi_iteration_loop_dry_run,
    verifier_subagent_boundary_is_not_invocation,
    v040_readiness_report_preserves_no_execution,
)


def test_v0400_envelope_defaults_to_dry_run_only() -> None:
    envelope = create_default_mission_loop_envelope()

    assert isinstance(envelope, MissionLoopEnvelope)
    assert envelope.current_iteration_index == 0
    assert envelope.max_iteration_count == 1
    assert envelope.human_checkpoint_required is True
    assert envelope.dry_run_only is True
    assert envelope.sandbox_rehearsal_allowed is False
    assert envelope.production_certified is False


def test_v0400_envelope_disallows_autonomous_continuation() -> None:
    envelope = create_default_mission_loop_envelope()

    assert envelope.autonomous_continuation_allowed is False
    with pytest.raises(ValueError):
        create_default_mission_loop_envelope(autonomous_continuation_allowed=True)
    with pytest.raises(ValueError):
        create_default_mission_loop_envelope(sandbox_rehearsal_allowed=True)


def test_v0400_iteration_state_is_metadata_only() -> None:
    state = create_initial_iteration_state()

    assert isinstance(state, IterationState)
    assert state.iteration_index == 0
    assert state.input_refs
    assert state.status == IterationStatus.DRAFTED.value
    assert state.grants_execution_permission is False


def test_v0400_eligible_for_next_iteration_is_not_execution_permission() -> None:
    state = create_initial_iteration_state(status=IterationStatus.ELIGIBLE_FOR_NEXT_ITERATION.value)

    assert state.status == "eligible_for_next_iteration"
    assert iteration_state_is_not_execution_permission(state)


def test_v0400_stop_condition_blocks_model_invocation_without_gate() -> None:
    contract = evaluate_stop_conditions(
        active_stop_signals=("model_invocation_without_gate",),
        unsafe_runtime_requested=True,
    )

    assert isinstance(contract, StopConditionContract)
    assert contract.decision_if_triggered == LoopDecisionKind.BLOCK.value
    assert "model_invocation_without_gate" in contract.active_stop_signals


def test_v0400_stop_condition_blocks_prompt_submission_without_gate() -> None:
    contract = evaluate_stop_conditions(
        active_stop_signals=("prompt_submission_without_gate",),
        unsafe_runtime_requested=True,
    )

    assert contract.decision_if_triggered == LoopDecisionKind.BLOCK.value
    assert "prompt_submission_without_gate" in contract.active_stop_signals


def test_v0400_stop_condition_blocks_subagent_invocation_without_gate() -> None:
    contract = evaluate_stop_conditions(
        active_stop_signals=("subagent_invocation_without_gate",),
        unsafe_runtime_requested=True,
    )

    assert contract.decision_if_triggered == LoopDecisionKind.BLOCK.value
    assert "subagent_invocation_without_gate" in contract.active_stop_signals


def test_v0400_stop_condition_blocks_live_workspace_apply() -> None:
    contract = evaluate_stop_conditions(
        active_stop_signals=("live_workspace_apply_requested",),
        unsafe_runtime_requested=True,
    )

    assert contract.decision_if_triggered == LoopDecisionKind.BLOCK.value
    assert "live_workspace_apply_requested" in contract.active_stop_signals


def test_v0400_stop_condition_contract_requires_all_signals() -> None:
    with pytest.raises(ValueError):
        StopConditionContract(
            contract_id="bad-stop-contract",
            loop_id="v0400-loop",
            stop_signals=("budget_exhausted",),
        )


def test_v0400_budget_unknown_is_not_unlimited() -> None:
    gate = evaluate_loop_budget()

    assert gate.max_estimated_tokens is None
    assert gate.unknown_token_budget_requires_checkpoint is True
    assert gate.budget_status == "checkpoint_required"
    with pytest.raises(ValueError):
        evaluate_loop_budget(
            max_estimated_tokens=None,
            budget_status="unlimited",
            unknown_token_budget_requires_checkpoint=True,
        )


def test_v0400_human_checkpoint_required_before_second_iteration() -> None:
    second_iteration = IterationState(
        loop_id="v0400-loop",
        iteration_index=1,
        status=IterationStatus.CHECKPOINT_REQUIRED.value,
    )
    checkpoint = require_human_checkpoint_for_second_iteration(second_iteration)

    assert isinstance(checkpoint, HumanCheckpointGate)
    assert checkpoint.iteration_index == 1
    assert checkpoint.required is True
    assert checkpoint.default_decision == LoopDecisionKind.STOP.value


def test_v0400_checkpoint_approval_does_not_grant_runtime_authority() -> None:
    checkpoint = require_human_checkpoint_for_second_iteration()

    assert checkpoint.approval_grants_runtime_authority is False
    with pytest.raises(ValueError):
        require_human_checkpoint_for_second_iteration(approval_grants_runtime_authority=True)


def test_v0400_provider_boundary_is_not_invocation() -> None:
    gate = create_provider_boundary_gate(invocation_requested=True)

    assert isinstance(gate, ProviderBoundaryGate)
    assert gate.invocation_requested is True
    assert gate.invocation_allowed is False
    assert gate.dispatch_mode == "metadata_only"
    assert provider_boundary_gate_is_not_invocation(gate)
    with pytest.raises(ValueError):
        create_provider_boundary_gate(invocation_allowed=True)


def test_v0400_prompt_submission_boundary_is_not_submission() -> None:
    boundary = create_prompt_submission_boundary(submission_requested=True)

    assert isinstance(boundary, PromptSubmissionBoundary)
    assert boundary.submission_requested is True
    assert boundary.submission_allowed is False
    assert boundary.submitted_to_model is False
    assert boundary.human_checkpoint_required is True
    assert prompt_submission_boundary_is_not_submission(boundary)
    with pytest.raises(ValueError):
        create_prompt_submission_boundary(submitted_to_model=True)


def test_v0400_verifier_boundary_is_not_subagent_invocation() -> None:
    boundary = create_verifier_subagent_boundary(invocation_requested=True)

    assert isinstance(boundary, VerifierSubagentBoundary)
    assert boundary.invocation_requested is True
    assert boundary.invocation_allowed is False
    assert boundary.subagent_invoked is False
    assert boundary.parent_context_shared is False
    assert verifier_subagent_boundary_is_not_invocation(boundary)
    with pytest.raises(ValueError):
        create_verifier_subagent_boundary(subagent_invoked=True)


def test_v0400_denied_runtime_action_records_safe_alternative() -> None:
    denied = create_denied_runtime_action(
        requested_action_type=RuntimeActionType.AUTOMATIC_REPAIR.value,
        suggested_safe_alternative=SafeAlternative.STOP.value,
    )

    assert isinstance(denied, DeniedRuntimeActionMetadata)
    assert denied.requested_action_type == "automatic_repair"
    assert denied.suggested_safe_alternative == "stop"
    with pytest.raises(ValueError):
        create_denied_runtime_action(suggested_safe_alternative="run_it")


def test_v0400_do_nothing_is_valid_loop_decision() -> None:
    decision = LoopDecisionRecord(
        decision_id="v0400-do-nothing-decision",
        loop_id="v0400-loop",
        iteration_index=0,
        decision_kind=LoopDecisionKind.DO_NOTHING.value,
        reason="No safe continuation is required.",
        requires_human_checkpoint=True,
        grants_runtime_authority=False,
        safe_alternative=SafeAlternative.DO_NOTHING.value,
        evidence_refs=("stop-condition",),
    )

    assert decision.decision_kind == "do_nothing"
    assert decision.grants_runtime_authority is False


def test_v0400_simulated_packet_does_not_execute_or_mutate() -> None:
    packet = simulate_multi_iteration_loop_dry_run()

    assert isinstance(packet, SimulatedMultiIterationLoopPacket)
    assert len(packet.iteration_states) == 2
    assert packet.loop_decision.decision_kind == LoopDecisionKind.REQUEST_HUMAN_CHECKPOINT.value
    assert packet.executed is False
    assert packet.mutated_files is False
    assert packet.invoked_model is False
    assert packet.invoked_subagent is False
    assert simulated_packet_is_dry_run_only(packet)
    with pytest.raises(ValueError):
        SimulatedMultiIterationLoopPacket(
            packet_id="bad-packet",
            loop_envelope=create_default_mission_loop_envelope(),
            iteration_states=(create_initial_iteration_state(),),
            loop_decision=packet.loop_decision,
            executed=True,
        )


def test_v0400_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_v040_readiness_report()

    assert isinstance(report, V040ReadinessReport)
    assert report.controlled_multi_iteration_boundary_defined is True
    assert report.dry_run_simulation_ready is True
    assert report.negative_runtime_gate_test_ready is True
    assert report.default_personal_user_guide_ready is True
    assert v040_readiness_report_preserves_no_execution(report)
    assert report.ready_for_execution is False
    assert report.ready_for_model_provider_invocation is False
    assert report.ready_for_prompt_submission_to_model is False
    assert report.ready_for_subagent_invocation is False
    assert report.ready_for_autonomous_loop_runtime is False
    assert report.ready_for_retry_loop is False
    assert report.ready_for_dominion_runtime is False
    assert report.production_certified is False
    with pytest.raises(ValueError):
        create_v040_readiness_report(ready_for_execution=True)


def test_v0400_default_personal_user_guide_exists() -> None:
    guide = Path("docs/versions/v0.40/v0.40.0_default_personal_user_guide.md")

    assert guide.exists()
    text = guide.read_text(encoding="utf-8")
    assert "Default Personal" in text
    assert "do_nothing" in text
    assert "HumanCheckpointGate" in text
    assert "v0.40.1" in text


def test_v0400_no_forbidden_runtime_call_patterns() -> None:
    implementation = Path("src/chanta_core/agent_runtime/repair_mission_loop_boundary.py")
    source = implementation.read_text(encoding="utf-8").lower()

    forbidden_patterns = [
        "subprocess",
        "shell=true",
        "os.system",
        "eval(",
        "exec(",
        "requests",
        "httpx",
        "urllib",
        "socket",
        "openai",
        "anthropic",
        "ollama",
        "lmstudio",
        "codex",
        "claude",
        "apply_patch",
        "git apply",
        "git worktree",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source
