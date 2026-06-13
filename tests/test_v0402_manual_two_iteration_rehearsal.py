from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_rehearsal import create_sandbox_rehearsal_input
from chanta_core.agent_runtime.repair_mission_loop_two_iteration import (
    CHECKPOINT_DECISIONS,
    V0403_NEGATIVE_CASES,
    ManualIterationStateRef,
    create_checkpoint_decision,
    create_checkpoint_request_after_iteration_zero,
    create_manual_two_iteration_input,
    create_manual_two_iteration_plan,
    create_manual_two_iteration_readiness_report,
    create_manual_two_iteration_safety_report,
    create_no_autonomous_continuation_guarantee,
    create_standalone_runtime_still_closed_record,
    create_v0403_negative_runtime_gate_handoff,
    create_v041_smoke_run_acceleration_signal,
    evaluate_second_iteration_eligibility,
    manual_iteration_state_ref_is_not_execution_permission,
    manual_two_iteration_readiness_preserves_no_unsafe_runtime,
    manual_two_iteration_result_preserves_safety,
    run_manual_two_iteration_rehearsal,
    second_iteration_eligibility_is_not_runtime_authority,
    smoke_run_acceleration_signal_is_not_runtime_start,
    standalone_runtime_still_closed,
)


def _sandbox_input(tmp_path: Path, name: str, before: str = "before", after: str = "after"):
    sandbox = tmp_path / name
    sandbox.mkdir()
    target = sandbox / "example.txt"
    target.write_text(f"alpha {before} omega", encoding="utf-8")
    return create_sandbox_rehearsal_input(
        rehearsal_id=f"{name}-rehearsal",
        loop_id="v0402-loop",
        sandbox_root_ref=str(sandbox),
        target_relative_path="example.txt",
        original_text=before,
        replacement_text=after,
    ), target


def test_v0402_input_caps_max_iterations_at_two() -> None:
    rehearsal_input = create_manual_two_iteration_input()

    assert rehearsal_input.max_iterations == 2
    with pytest.raises(ValueError):
        create_manual_two_iteration_input(max_iterations=3)


def test_v0402_input_requires_manual_mode() -> None:
    rehearsal_input = create_manual_two_iteration_input()

    assert rehearsal_input.manual_mode_required is True
    assert rehearsal_input.autonomous_continuation_requested is False
    with pytest.raises(ValueError):
        create_manual_two_iteration_input(manual_mode_required=False)
    with pytest.raises(ValueError):
        create_manual_two_iteration_input(autonomous_continuation_requested=True)


def test_v0402_checkpoint_request_is_required_after_iteration_zero() -> None:
    request = create_checkpoint_request_after_iteration_zero()

    assert request.after_iteration_index == 0
    assert request.required is True
    assert request.default_decision == "stop"
    assert set(CHECKPOINT_DECISIONS).issubset(request.decision_options)
    assert request.approval_grants_runtime_authority is False


def test_v0402_checkpoint_approval_does_not_grant_runtime_authority() -> None:
    decision = create_checkpoint_decision()

    assert decision.decision == "approve_second_iteration_rehearsal"
    assert decision.approved_iteration_index == 1
    assert decision.approved_rehearsal_only is True
    assert decision.approval_grants_runtime_authority is False
    with pytest.raises(ValueError):
        create_checkpoint_decision(approval_grants_runtime_authority=True)


def test_v0402_missing_checkpoint_blocks_second_iteration() -> None:
    eligibility = evaluate_second_iteration_eligibility(None)

    assert eligibility.eligible is False
    assert eligibility.reason == "human_checkpoint_missing"
    assert eligibility.checkpoint_required is True
    assert eligibility.checkpoint_present is False


@pytest.mark.parametrize("decision_kind", ["stop", "do_nothing", "request_more_evidence", "reject"])
def test_v0402_non_approval_decisions_block_second_iteration(decision_kind: str) -> None:
    decision = create_checkpoint_decision(decision=decision_kind)
    eligibility = evaluate_second_iteration_eligibility(decision)

    assert eligibility.eligible is False
    assert eligibility.reason == decision_kind
    assert eligibility.checkpoint_present is True
    assert eligibility.runtime_authority_granted is False


def test_v0402_stop_decision_blocks_second_iteration() -> None:
    assert evaluate_second_iteration_eligibility(create_checkpoint_decision(decision="stop")).eligible is False


def test_v0402_do_nothing_decision_blocks_second_iteration() -> None:
    assert evaluate_second_iteration_eligibility(create_checkpoint_decision(decision="do_nothing")).eligible is False


def test_v0402_request_more_evidence_blocks_second_iteration() -> None:
    assert evaluate_second_iteration_eligibility(create_checkpoint_decision(decision="request_more_evidence")).eligible is False


def test_v0402_approval_allows_only_manual_bounded_second_rehearsal() -> None:
    decision = create_checkpoint_decision(decision="approve_second_iteration_rehearsal")
    eligibility = evaluate_second_iteration_eligibility(decision)

    assert eligibility.eligible is True
    assert eligibility.reason == "approved_manual_bounded_rehearsal"
    assert eligibility.manual_only is True
    assert eligibility.runtime_authority_granted is False


def test_v0402_second_iteration_eligibility_is_not_execution_permission() -> None:
    state_ref = ManualIterationStateRef(
        state_ref_id="state-ref-1",
        loop_id="v0402-loop",
        iteration_index=1,
        eligible_for_next_iteration=True,
        execution_permission_granted=False,
    )
    eligibility = evaluate_second_iteration_eligibility(create_checkpoint_decision())

    assert manual_iteration_state_ref_is_not_execution_permission(state_ref)
    assert second_iteration_eligibility_is_not_runtime_authority(eligibility)


def test_v0402_plan_disallows_autonomous_continuation() -> None:
    plan = create_manual_two_iteration_plan()

    assert plan.max_iterations == 2
    assert plan.manual_only is True
    assert plan.autonomous_continuation_allowed is False
    with pytest.raises(ValueError):
        create_manual_two_iteration_plan(autonomous_continuation_allowed=True)


def test_v0402_result_enforces_max_two_iteration_cap(tmp_path: Path) -> None:
    first_input, _ = _sandbox_input(tmp_path, "iteration0")
    plan, result, _, _ = run_manual_two_iteration_rehearsal(
        create_manual_two_iteration_input(),
        first_input,
        checkpoint_decision=None,
    )

    assert plan.max_iterations == 2
    assert result.max_iteration_cap_enforced is True
    assert result.iteration_zero_attempted is True
    assert result.iteration_one_attempted is False


def test_v0402_result_records_no_live_workspace_model_prompt_or_subagent(tmp_path: Path) -> None:
    first_input, live_file = _sandbox_input(tmp_path, "iteration0")
    result_tuple = run_manual_two_iteration_rehearsal(create_manual_two_iteration_input(), first_input)
    result = result_tuple[1]

    assert manual_two_iteration_result_preserves_safety(result)
    assert result.live_workspace_mutated is False
    assert result.model_invoked is False
    assert result.prompt_submitted is False
    assert result.subagent_invoked is False
    assert live_file.read_text(encoding="utf-8") == "alpha after omega"


def test_v0402_audit_record_checks_checkpoint_and_no_autonomy(tmp_path: Path) -> None:
    first_input, _ = _sandbox_input(tmp_path, "iteration0")
    _, _, audit, _ = run_manual_two_iteration_rehearsal(create_manual_two_iteration_input(), first_input)

    assert audit.checked_max_two_iterations is True
    assert audit.checked_checkpoint_between_iterations is True
    assert audit.checked_no_autonomous_continuation is True
    assert audit.checked_no_runtime_authority_grant is True
    assert audit.checked_standalone_runtime_not_opened is True


def test_v0402_safety_report_blocks_autonomous_live_model_prompt_subagent_and_standalone() -> None:
    report = create_manual_two_iteration_safety_report()

    assert report.safe_for_v0402_manual_rehearsal is True
    assert report.safe_for_autonomous_loop is False
    assert report.safe_for_live_apply is False
    assert report.safe_for_model_invocation is False
    assert report.safe_for_prompt_submission is False
    assert report.safe_for_subagent_invocation is False
    assert report.safe_for_standalone_default_personal_runtime is False
    assert report.requires_v0403_negative_gate_regression is True


def test_v0402_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_manual_two_iteration_readiness_report()

    assert report.manual_two_iteration_rehearsal_defined is True
    assert report.human_checkpoint_between_iterations_required is True
    assert report.second_iteration_eligibility_gate_ready is True
    assert report.max_two_iteration_cap_ready is True
    assert report.no_autonomous_continuation_guarantee_ready is True
    assert manual_two_iteration_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_manual_two_iteration_readiness_report(ready_for_autonomous_loop_runtime=True)
    with pytest.raises(ValueError):
        create_manual_two_iteration_readiness_report(production_certified=True)


def test_v0402_no_autonomous_continuation_guarantee_blocks_retry_and_unbounded_loop() -> None:
    guarantee = create_no_autonomous_continuation_guarantee()

    assert guarantee.autonomous_continuation_allowed is False
    assert guarantee.automatic_second_iteration_allowed is False
    assert guarantee.unbounded_loop_allowed is False
    assert guarantee.retry_loop_allowed is False
    assert guarantee.human_checkpoint_required is True


def test_v0402_standalone_runtime_still_closed_record_all_false() -> None:
    record = create_standalone_runtime_still_closed_record()

    assert standalone_runtime_still_closed(record)
    assert record.first_smoke_run_conservative_target == "v0.41.6"
    with pytest.raises(ValueError):
        create_standalone_runtime_still_closed_record(agent_loop_opened=True)


def test_v0402_smoke_run_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_signal(manual_two_iteration_rehearsal_passed=True)

    assert smoke_run_acceleration_signal_is_not_runtime_start(signal)
    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert signal.recommendation == "keep_conservative_target"
    assert "ChatService" in signal.blocking_runtime_gaps


def test_v0402_v0403_handoff_includes_required_negative_cases() -> None:
    handoff = create_v0403_negative_runtime_gate_handoff()

    assert handoff.target_version == "v0.40.3"
    assert set(V0403_NEGATIVE_CASES).issubset(handoff.required_negative_cases)


def test_v0402_manual_two_iteration_flow_stops_without_checkpoint(tmp_path: Path) -> None:
    first_input, first_target = _sandbox_input(tmp_path, "iteration0")
    second_input, second_target = _sandbox_input(tmp_path, "iteration1")
    plan, result, _, _ = run_manual_two_iteration_rehearsal(
        create_manual_two_iteration_input(iteration_one_input_ref=second_input.rehearsal_id),
        first_input,
        iteration_one_input=second_input,
        checkpoint_decision=None,
    )

    assert result.checkpoint_requested is True
    assert result.checkpoint_present is False
    assert result.second_iteration_eligible is False
    assert result.stopped_after_iteration_zero is True
    assert result.iteration_one_attempted is False
    assert plan.iteration_one_rehearsal_ref is None
    assert first_target.read_text(encoding="utf-8") == "alpha after omega"
    assert second_target.read_text(encoding="utf-8") == "alpha before omega"


def test_v0402_manual_two_iteration_flow_allows_second_candidate_with_explicit_checkpoint(tmp_path: Path) -> None:
    first_input, first_target = _sandbox_input(tmp_path, "iteration0")
    second_input, second_target = _sandbox_input(tmp_path, "iteration1")
    decision = create_checkpoint_decision()
    plan, result, _, _ = run_manual_two_iteration_rehearsal(
        create_manual_two_iteration_input(
            iteration_one_input_ref=second_input.rehearsal_id,
            checkpoint_decision_ref=decision.checkpoint_decision_id,
        ),
        first_input,
        iteration_one_input=second_input,
        checkpoint_decision=decision,
    )

    assert result.checkpoint_present is True
    assert result.second_iteration_eligible is True
    assert result.iteration_one_attempted is True
    assert result.iteration_one_succeeded is True
    assert plan.iteration_one_rehearsal_ref == "iteration1-rehearsal-result"
    assert first_target.read_text(encoding="utf-8") == "alpha after omega"
    assert second_target.read_text(encoding="utf-8") == "alpha after omega"


def test_v0402_manual_two_iteration_flow_never_auto_continues(tmp_path: Path) -> None:
    first_input, _ = _sandbox_input(tmp_path, "iteration0")
    _, result, _, _ = run_manual_two_iteration_rehearsal(create_manual_two_iteration_input(), first_input)

    assert result.autonomous_continuation_used is False
    assert result.runtime_authority_granted is False


def test_v0402_no_forbidden_runtime_call_patterns() -> None:
    implementation = Path("src/chanta_core/agent_runtime/repair_mission_loop_two_iteration.py")
    source = implementation.read_text(encoding="utf-8")
    lower_source = source.lower()
    actual_runtime_patterns = [
        "import subprocess",
        "subprocess.",
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

    for pattern in actual_runtime_patterns:
        assert pattern not in lower_source
    assert re.search(r"(?<!no_)shell\s*=\s*True", source) is None
