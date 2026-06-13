from __future__ import annotations

import pytest

from chanta_core.agent_runtime.repair_outcome_comparison import (
    RepairEffectivenessKind,
    RepairFailureDeltaKind,
    RepairOutcomeComparisonDecision,
    RepairOutcomeComparisonDecisionKind,
    RepairOutcomeComparisonFlagSet,
    RepairOutcomeComparisonInput,
    RepairOutcomeComparisonMode,
    RepairOutcomeComparisonNoExecutionGuarantee,
    RepairOutcomeComparisonPolicy,
    RepairOutcomeComparisonReport,
    RepairOutcomeComparisonSourceKind,
    RepairOutcomeComparisonStatus,
    RepairOutcomeConfidenceLevel,
    RepairOutcomeDoNothingComparisonKind,
    RepairRegressionSignalKind,
    RepairTestOutcomeDeltaKind,
    RepairTestOutcomeKind,
    RepairTestOutcomeSnapshot,
    V0395ReadinessReport,
    assess_repair_effectiveness,
    assess_repair_failure_delta,
    audit_repair_outcome_comparison,
    build_repair_before_after_outcome_pair,
    build_repair_effectiveness_assessment,
    build_repair_outcome_comparison_flags,
    build_repair_outcome_comparison_input,
    build_repair_outcome_comparison_no_execution_guarantee,
    build_repair_outcome_comparison_policy,
    build_repair_outcome_comparison_report,
    build_repair_test_outcome_snapshot,
    build_v0395_readiness_report,
    compare_repair_outcome_to_do_nothing,
    compare_repair_test_outcomes,
    create_repair_outcome_comparison_report,
    create_repair_test_outcome_snapshot_from_result_metadata,
    default_repair_outcome_comparison_policy,
    detect_repair_regression_signals,
    pair_before_after_repair_outcomes,
    repair_effectiveness_assessment_is_not_correctness_proof,
    repair_outcome_comparison_flags_preserve_no_execution,
    repair_outcome_comparison_policy_blocks_runtime,
    repair_outcome_comparison_report_is_not_execution,
    v0395_readiness_report_is_not_execution_ready,
)


def test_v0395_enum_values() -> None:
    assert [item.value for item in RepairOutcomeComparisonMode] == [
        "before_after_repair_outcome_comparison",
        "before_after_test_pairing",
        "test_outcome_delta_analysis",
        "failure_delta_assessment",
        "regression_signal_detection",
        "residual_failure_assessment",
        "repair_effectiveness_assessment",
        "do_nothing_after_apply_comparison",
        "future_process_state_reconstruction_input",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in RepairOutcomeComparisonSourceKind] == [
        "v0394_post_apply_retest_result",
        "v0394_post_apply_retest_run_record",
        "v0394_post_apply_output_capture",
        "v0394_post_apply_retest_audit",
        "v0394_readiness_report",
        "v0393_sandbox_apply_result",
        "v0393_sandbox_apply_transaction",
        "v0393_sandbox_apply_audit",
        "v0373_before_test_result_envelope",
        "v0374_before_test_feedback_report",
        "v0374_failure_diagnosis_report",
        "v0381_repair_evidence_bundle",
        "v0384_proposed_patch_envelope",
        "v0385_safety_report",
        "supplied_before_test_result",
        "supplied_after_test_result",
        "manual_operator_note",
        "test_fixture",
        "unknown",
    ]
    assert "comparison_completed" in {item.value for item in RepairOutcomeComparisonStatus}
    assert "fail_to_pass" in {item.value for item in RepairTestOutcomeDeltaKind}
    assert "failure_resolved" in {item.value for item in RepairFailureDeltaKind}
    assert "new_failed_test" in {item.value for item in RepairRegressionSignalKind}
    assert "effective_candidate" in {item.value for item in RepairEffectivenessKind}
    assert "high" in {item.value for item in RepairOutcomeConfidenceLevel}
    assert "repair_outperforms_do_nothing" in {item.value for item in RepairOutcomeDoNothingComparisonKind}
    assert [item.value for item in RepairTestOutcomeKind] == [
        "passed",
        "failed",
        "error",
        "timed_out",
        "skipped",
        "blocked",
        "runner_unavailable",
        "inconclusive",
        "no_result",
        "unknown",
    ]


def test_flags_allow_comparison_only() -> None:
    flags = build_repair_outcome_comparison_flags()

    assert isinstance(flags, RepairOutcomeComparisonFlagSet)
    assert flags.ready_for_before_after_repair_comparison is True
    assert flags.ready_for_test_outcome_delta_analysis is True
    assert flags.ready_for_failure_delta_assessment is True
    assert flags.ready_for_regression_signal_detection is True
    assert flags.ready_for_residual_failure_assessment is True
    assert flags.ready_for_repair_effectiveness_assessment is True
    assert flags.ready_for_do_nothing_after_apply_comparison is True
    assert flags.ready_for_future_process_state_reconstruction_input is True
    assert flags.ready_for_v0396_pi_native_repair_process_state_reconstruction is True
    assert repair_outcome_comparison_flags_preserve_no_execution(flags)

    assert flags.ready_for_execution is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_controlled_retest_execution is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_repair_process_state_projection is False
    assert flags.production_certified is False


@pytest.mark.parametrize(
    "field_name",
    [
        "ready_for_execution",
        "ready_for_test_execution",
        "ready_for_controlled_retest_execution",
        "ready_for_controlled_test_subprocess",
        "ready_for_arbitrary_command_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_patch_application",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_repair_process_state_projection",
        "ready_for_ocel_event_write",
        "ready_for_ocpx_state_persistence",
        "ready_for_pig_recommendation_execution",
        "ready_for_self_prompt_generation",
        "ready_for_self_prompt_auto_execution",
        "ready_for_agent_to_subagent_prompt_generation",
        "ready_for_subagent_auto_invocation",
        "ready_for_external_agent_execution",
        "ready_for_model_provider_invocation",
        "ready_for_autonomous_loop_runtime",
        "ready_for_retry_loop",
        "ready_for_multi_cycle_loop",
        "ready_for_repair_execution",
        "ready_for_dominion_runtime",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_outcome_comparison_flags(**{field_name: True})


def test_policy_allows_comparison_and_blocks_runtime() -> None:
    policy = default_repair_outcome_comparison_policy()

    assert isinstance(policy, RepairOutcomeComparisonPolicy)
    assert policy.allow_before_after_pairing is True
    assert policy.allow_test_outcome_delta_analysis is True
    assert policy.allow_failure_delta_assessment is True
    assert policy.allow_regression_signal_detection is True
    assert policy.allow_residual_failure_assessment is True
    assert policy.allow_repair_effectiveness_assessment is True
    assert policy.allow_do_nothing_after_apply_comparison is True
    assert policy.allow_future_process_state_reconstruction_input is True
    assert policy.require_do_nothing_comparison is True
    assert repair_outcome_comparison_policy_blocks_runtime(policy)

    assert policy.allow_test_execution is False
    assert policy.allow_controlled_retest_execution is False
    assert policy.allow_shell is False
    assert policy.allow_raw_subprocess is False
    assert policy.allow_patch_application is False
    assert policy.allow_rollback_execution is False
    assert policy.allow_process_state_reconstruction is False
    assert policy.allow_dominion_runtime is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_test_execution",
        "allow_controlled_retest_execution",
        "allow_arbitrary_command_execution",
        "allow_shell",
        "allow_raw_subprocess",
        "allow_dependency_install",
        "allow_network_access",
        "allow_patch_materialization",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_rollback_execution",
        "allow_repair_execution",
        "allow_process_state_reconstruction",
        "allow_ocel_event_write",
        "allow_ocpx_state_persistence",
        "allow_pig_recommendation_execution",
        "allow_self_prompt_generation",
        "allow_subagent_auto_invocation",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_unsafe_runtime_allow(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_outcome_comparison_policy(**{field_name: True})


def test_input_is_metadata_only_comparison_request() -> None:
    comparison_input = build_repair_outcome_comparison_input()

    assert isinstance(comparison_input, RepairOutcomeComparisonInput)
    for action in [
        "test_execution",
        "controlled_runner_invocation",
        "shell",
        "subprocess",
        "command_execution",
        "apply_patch",
        "git_apply",
        "rollback_execution",
        "repair_execution",
        "self_prompt_execution",
        "subagent_invocation",
        "model_provider",
        "external_agent",
        "Dominion",
    ]:
        assert action in comparison_input.prohibited_runtime_actions


def test_outcome_snapshot_is_bounded_redacted_metadata() -> None:
    snapshot = create_repair_test_outcome_snapshot_from_result_metadata(
        {
            "result_id": "before",
            "outcome_kind": RepairTestOutcomeKind.FAILED,
            "selected_test_refs": ["t::a"],
            "failed_test_refs": ["t::a"],
            "output_preview": "abcdef",
        },
        phase_label="before",
        max_output_preview_chars=3,
    )

    assert isinstance(snapshot, RepairTestOutcomeSnapshot)
    assert snapshot.output_preview == "abc...[truncated]"
    assert snapshot.bounded is True
    assert snapshot.redacted is True


def test_before_after_pair_complete_and_comparable_rules() -> None:
    before = build_repair_test_outcome_snapshot(phase_label="before", outcome_kind=RepairTestOutcomeKind.FAILED)
    after = build_repair_test_outcome_snapshot(phase_label="after", outcome_kind=RepairTestOutcomeKind.PASSED)
    pair = pair_before_after_repair_outcomes(before, after)

    assert pair.pair_complete is True
    assert pair.pair_comparable is True
    assert pair.scope_changed is False

    incomplete = pair_before_after_repair_outcomes(None, after)
    assert incomplete.pair_complete is False
    assert incomplete.pair_comparable is False

    changed = pair_before_after_repair_outcomes(
        before,
        build_repair_test_outcome_snapshot(selected_test_refs=["t::other"], passed_test_refs=["t::other"]),
    )
    assert changed.scope_changed is True
    assert changed.pair_comparable is False


@pytest.mark.parametrize(
    ("before_kind", "after_kind", "expected", "improved", "worsened"),
    [
        (RepairTestOutcomeKind.FAILED, RepairTestOutcomeKind.PASSED, RepairTestOutcomeDeltaKind.FAIL_TO_PASS, True, False),
        (RepairTestOutcomeKind.PASSED, RepairTestOutcomeKind.FAILED, RepairTestOutcomeDeltaKind.PASS_TO_FAIL, False, True),
        (RepairTestOutcomeKind.FAILED, RepairTestOutcomeKind.FAILED, RepairTestOutcomeDeltaKind.FAIL_TO_FAIL, False, False),
        (RepairTestOutcomeKind.PASSED, RepairTestOutcomeKind.PASSED, RepairTestOutcomeDeltaKind.PASS_TO_PASS, False, False),
    ],
)
def test_outcome_delta_kinds(before_kind: RepairTestOutcomeKind, after_kind: RepairTestOutcomeKind, expected: RepairTestOutcomeDeltaKind, improved: bool, worsened: bool) -> None:
    before = build_repair_test_outcome_snapshot(
        phase_label="before",
        outcome_kind=before_kind,
        passed_test_refs=["t::a"] if before_kind == RepairTestOutcomeKind.PASSED else [],
        failed_test_refs=["t::a"] if before_kind == RepairTestOutcomeKind.FAILED else [],
    )
    after = build_repair_test_outcome_snapshot(
        phase_label="after",
        outcome_kind=after_kind,
        passed_test_refs=["t::a"] if after_kind == RepairTestOutcomeKind.PASSED else [],
        failed_test_refs=["t::a"] if after_kind == RepairTestOutcomeKind.FAILED else [],
    )
    delta = compare_repair_test_outcomes(pair_before_after_repair_outcomes(before, after))

    assert delta.delta_kind == expected
    assert delta.improved is improved
    assert delta.worsened is worsened


def test_failure_delta_resolved_residual_and_new() -> None:
    before = build_repair_test_outcome_snapshot(
        phase_label="before",
        outcome_kind=RepairTestOutcomeKind.FAILED,
        selected_test_refs=["t::a", "t::b", "t::c"],
        passed_test_refs=[],
        failed_test_refs=["t::a", "t::b"],
    )
    after = build_repair_test_outcome_snapshot(
        phase_label="after",
        outcome_kind=RepairTestOutcomeKind.FAILED,
        selected_test_refs=["t::a", "t::b", "t::c"],
        passed_test_refs=["t::a"],
        failed_test_refs=["t::b", "t::c"],
    )
    failure_delta = assess_repair_failure_delta(pair_before_after_repair_outcomes(before, after))

    assert RepairFailureDeltaKind.FAILURE_RESOLVED in failure_delta.failure_delta_kinds
    assert RepairFailureDeltaKind.RESIDUAL_FAILURE_PRESENT in failure_delta.failure_delta_kinds
    assert RepairFailureDeltaKind.NEW_FAILURE_INTRODUCED in failure_delta.failure_delta_kinds
    assert failure_delta.resolved_failure_refs == ["t::a"]
    assert failure_delta.residual_failure_refs == ["t::b"]
    assert failure_delta.new_failure_refs == ["t::c"]


def test_regression_signal_detects_new_failures_and_no_regression_is_not_certification() -> None:
    before = build_repair_test_outcome_snapshot(phase_label="before", outcome_kind=RepairTestOutcomeKind.PASSED)
    after = build_repair_test_outcome_snapshot(phase_label="after", outcome_kind=RepairTestOutcomeKind.FAILED, passed_test_refs=[], failed_test_refs=["tests/test_target.py::test_case"])
    pair = pair_before_after_repair_outcomes(before, after)
    failure_delta = assess_repair_failure_delta(pair)
    signal = detect_repair_regression_signals(pair, failure_delta)

    assert RepairRegressionSignalKind.NEW_FAILED_TEST in signal.signal_kinds
    assert signal.regression_detected is True
    assert signal.new_failure_detected is True

    clean_signal = detect_repair_regression_signals(build_repair_before_after_outcome_pair())
    assert RepairRegressionSignalKind.NO_REGRESSION_DETECTED in clean_signal.signal_kinds
    report = build_v0395_readiness_report()
    assert report.production_certified is False


def test_effectiveness_assessment_variants_are_not_correctness_proof() -> None:
    effective = build_repair_effectiveness_assessment(effectiveness_kind=RepairEffectivenessKind.EFFECTIVE_CANDIDATE)
    partial = build_repair_effectiveness_assessment(
        effectiveness_kind=RepairEffectivenessKind.PARTIALLY_EFFECTIVE_CANDIDATE,
        effective_candidate=False,
        partially_effective_candidate=True,
    )
    ineffective = build_repair_effectiveness_assessment(
        effectiveness_kind=RepairEffectivenessKind.INEFFECTIVE_CANDIDATE,
        effective_candidate=False,
        ineffective_candidate=True,
    )
    regressive = build_repair_effectiveness_assessment(
        effectiveness_kind=RepairEffectivenessKind.REGRESSIVE_CANDIDATE,
        effective_candidate=False,
        regressive_candidate=True,
    )

    for assessment in [effective, partial, ineffective, regressive]:
        assert repair_effectiveness_assessment_is_not_correctness_proof(assessment)
        assert assessment.correctness_proven is False
        assert assessment.production_certified is False
        assert assessment.human_review_required is True

    with pytest.raises(ValueError):
        build_repair_effectiveness_assessment(correctness_proven=True)


def test_do_nothing_comparison_is_always_represented() -> None:
    effectiveness = build_repair_effectiveness_assessment()
    comparison = compare_repair_outcome_to_do_nothing(effectiveness)

    assert comparison.do_nothing_remains_valid is True
    assert comparison.comparison_kind == RepairOutcomeDoNothingComparisonKind.REPAIR_OUTPERFORMS_DO_NOTHING


def test_audit_decision_report_and_readiness_block_runtime() -> None:
    comparison_input = build_repair_outcome_comparison_input()
    audit = audit_repair_outcome_comparison(comparison_input)
    report = create_repair_outcome_comparison_report(
        comparison_input,
        build_repair_test_outcome_snapshot(phase_label="before", outcome_kind=RepairTestOutcomeKind.FAILED, passed_test_refs=[], failed_test_refs=["tests/test_target.py::test_case"]),
        build_repair_test_outcome_snapshot(phase_label="after", outcome_kind=RepairTestOutcomeKind.PASSED),
    )
    readiness = build_v0395_readiness_report(comparison_report=report)

    assert audit.no_test_execution_confirmed is True
    assert audit.no_controlled_runner_invocation_confirmed is True
    assert audit.no_patch_application_confirmed is True
    assert audit.no_rollback_execution_confirmed is True
    assert audit.no_repair_execution_confirmed is True
    assert audit.no_process_state_reconstruction_confirmed is True
    assert audit.no_self_prompt_execution_confirmed is True
    assert audit.no_subagent_invocation_confirmed is True
    assert audit.no_model_invocation_confirmed is True
    assert audit.no_external_agent_confirmed is True
    assert audit.no_dominion_runtime_confirmed is True
    assert audit.no_production_certification_confirmed is True

    assert isinstance(report, RepairOutcomeComparisonReport)
    assert report.comparison_completed is True
    assert report.correctness_proven is False
    assert report.production_certified is False
    assert report.tests_run_by_v0395 is False
    assert report.patches_applied_by_v0395 is False
    assert report.rollback_executed_by_v0395 is False
    assert report.repair_executed_by_v0395 is False
    assert report.ready_for_execution is False
    assert repair_outcome_comparison_report_is_not_execution(report)

    assert isinstance(report.decision, RepairOutcomeComparisonDecision)
    assert report.decision.ready_for_future_process_state_reconstruction_input is True
    assert report.decision.test_execution_allowed_now is False
    assert report.decision.controlled_retest_allowed_now is False
    assert report.decision.patch_apply_allowed_now is False
    assert report.decision.rollback_execution_allowed_now is False
    assert report.decision.process_state_reconstruction_allowed_now is False
    assert report.decision.production_certified is False

    assert isinstance(readiness, V0395ReadinessReport)
    assert readiness.ready_for_v0396_pi_native_repair_process_state_reconstruction is True
    assert readiness.ready_for_future_process_state_reconstruction_input is True
    assert readiness.tests_run_enabled is False
    assert readiness.controlled_retest_enabled is False
    assert readiness.patch_apply_enabled is False
    assert readiness.rollback_execution_enabled is False
    assert readiness.repair_execution_enabled is False
    assert readiness.process_state_reconstruction_enabled is False
    assert readiness.production_certified is False
    assert readiness.ready_for_execution is False
    assert v0395_readiness_report_is_not_execution_ready(readiness)


@pytest.mark.parametrize(
    "field_name",
    [
        "tests_run_by_v0395",
        "correctness_proven",
        "production_certified",
        "patches_applied_by_v0395",
        "rollback_executed_by_v0395",
        "repair_executed_by_v0395",
        "ready_for_execution",
    ],
)
def test_comparison_report_rejects_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_repair_outcome_comparison_report(**{field_name: True})


@pytest.mark.parametrize(
    "field_name",
    ["process_state_reconstruction_allowed_now", "test_execution_allowed_now", "patch_apply_allowed_now", "production_certified"],
)
def test_decision_rejects_runtime_allowed_now(field_name: str) -> None:
    with pytest.raises(ValueError):
        from chanta_core.agent_runtime.repair_outcome_comparison import build_repair_outcome_comparison_decision

        build_repair_outcome_comparison_decision(**{field_name: True})


@pytest.mark.parametrize(
    "field_name",
    ["process_state_reconstruction_enabled", "ready_for_execution", "tests_run_enabled", "patch_apply_enabled"],
)
def test_readiness_report_rejects_unsafe_true(field_name: str) -> None:
    with pytest.raises(ValueError):
        build_v0395_readiness_report(**{field_name: True})


def test_no_execution_guarantee_all_required_no_flags_true() -> None:
    guarantee = build_repair_outcome_comparison_no_execution_guarantee()

    assert isinstance(guarantee, RepairOutcomeComparisonNoExecutionGuarantee)
    assert guarantee.no_test_execution is True
    assert guarantee.no_controlled_runner_invocation is True
    assert guarantee.no_arbitrary_command is True
    assert guarantee.no_shell is True
    assert guarantee.no_subprocess is True
    assert guarantee.no_patch_application is True
    assert guarantee.no_apply_patch is True
    assert guarantee.no_git_apply is True
    assert guarantee.no_rollback_execution is True
    assert guarantee.no_repair_execution is True
    assert guarantee.no_process_state_reconstruction is True
    assert guarantee.no_ocel_event_write is True
    assert guarantee.no_ocpx_persistence is True
    assert guarantee.no_pig_execution is True
    assert guarantee.no_self_prompt_generation is True
    assert guarantee.no_self_prompt_execution is True
    assert guarantee.no_next_action_execution is True
    assert guarantee.no_subagent_invocation is True
    assert guarantee.no_model_invocation is True
    assert guarantee.no_external_agent is True
    assert guarantee.no_autonomous_loop is True
    assert guarantee.no_retry_loop is True
    assert guarantee.no_multi_cycle_loop is True
    assert guarantee.no_dominion_runtime is True
    assert guarantee.no_production_certification is True
