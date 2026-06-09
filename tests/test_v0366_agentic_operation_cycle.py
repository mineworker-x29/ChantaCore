from pathlib import Path

import pytest

from chanta_core.agent_runtime.agentic_operation_cycle import (
    AgenticOperationDecisionKind,
    AgenticOperationHandoffKind,
    AgenticOperationMode,
    AgenticOperationReadinessLevel,
    AgenticOperationRiskKind,
    AgenticOperationRuntimeKind,
    AgenticOperationSafetyCheckKind,
    AgenticOperationSourceKind,
    AgenticOperationStatus,
    AgenticOperationStepKind,
    AgenticOperationStepStatus,
    AgenticOperationStopReasonKind,
    V0366ReadinessReport,
    agentic_operation_flags_preserve_no_autonomy,
    agentic_operation_policy_blocks_autonomy,
    agentic_operation_result_is_not_production_certification,
    agentic_operation_run_packet_is_single_cycle,
    agentic_operation_stop_reason_prevents_continuation,
    build_agentic_operation_decision,
    build_agentic_operation_flags,
    build_agentic_operation_input,
    build_agentic_operation_input_from_post_apply_validation,
    build_agentic_operation_intent,
    build_agentic_operation_no_autonomy_guarantee,
    build_agentic_operation_policy,
    build_agentic_operation_report,
    build_agentic_operation_result,
    build_agentic_operation_run_packet,
    build_agentic_operation_run_preview,
    build_agentic_operation_safety_finding,
    build_agentic_operation_safety_report,
    build_agentic_operation_source_ref,
    build_agentic_operation_stage_artifact_ref,
    build_agentic_operation_stage_refs_from_v036_artifacts,
    build_agentic_operation_step_record,
    build_agentic_operation_step_sequence,
    build_agentic_operation_stop_reason,
    build_agentic_operation_validation_finding,
    build_agentic_operation_validation_report,
    build_agentic_safety_report_from_stage_refs,
    build_agentic_step_sequence_from_stage_refs,
    build_v0366_readiness_report,
    decide_agentic_operation,
    default_agentic_operation_policy,
    run_bounded_agentic_operation_cycle,
    v0366_readiness_report_is_not_execution_ready,
    validate_agentic_operation_run_packet,
)
from chanta_core.agent_runtime.patch_apply_validation import build_sandbox_post_apply_validation_report


def _present_stage_refs():
    return build_agentic_operation_stage_refs_from_v036_artifacts(
        apply_candidate_id="candidate-1",
        human_approval_contract_id="approval-1",
        dry_run_result_id="dry-run-1",
        sandbox_manifest_id="manifest-1",
        sandbox_apply_result_id="apply-1",
        post_apply_validation_report_id="validation-1",
    )


def test_v0366_taxonomies_have_expected_values():
    assert [item.value for item in AgenticOperationMode] == [
        "metadata_only_cycle",
        "supplied_artifact_cycle",
        "bounded_function_task_cycle",
        "sandbox_apply_validation_cycle",
        "human_handoff_cycle",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert "v0365_post_apply_validation_report" in [item.value for item in AgenticOperationSourceKind]
    assert "cycle_completed" in [item.value for item in AgenticOperationStatus]
    assert "human_handoff_ready" in [item.value for item in AgenticOperationReadinessLevel]
    assert "allow_future_trace_input" in [item.value for item in AgenticOperationDecisionKind]
    assert "multi_cycle_loop_risk" in [item.value for item in AgenticOperationRiskKind]
    assert "verify_post_apply_validation" in [item.value for item in AgenticOperationStepKind]
    assert "failed_safe" in [item.value for item in AgenticOperationStepStatus]
    assert "stopped_no_retry_allowed" in [item.value for item in AgenticOperationStopReasonKind]
    assert "independent_autonomous_agent" in [item.value for item in AgenticOperationRuntimeKind]
    assert "human_handoff_required" in [item.value for item in AgenticOperationHandoffKind]
    assert "no_model_invocation_check" in [item.value for item in AgenticOperationSafetyCheckKind]


def test_flags_allow_bounded_cycle_readiness_but_block_unsafe_readiness():
    flags = build_agentic_operation_flags()
    assert flags.agentic_operation_cycle_constructed is True
    assert flags.ready_for_bounded_agentic_task_operation_cycle is True
    assert flags.ready_for_agentic_function_task_execution is True
    assert flags.ready_for_single_cycle_operation_packet is True
    assert flags.ready_for_agentic_step_recording is True
    assert flags.ready_for_agentic_operation_safety_report is True
    assert flags.ready_for_human_handoff_after_cycle is True
    assert flags.ready_for_future_trace_input is True
    assert flags.ready_for_v0367_patch_apply_sandbox_ocel_trace_packet is True
    assert flags.ready_for_v0368_cli_sandbox_apply_agentic_surface is True
    assert agentic_operation_flags_preserve_no_autonomy(flags)


@pytest.mark.parametrize(
    "field",
    [
        "ready_for_execution",
        "ready_for_independent_agent_runtime",
        "ready_for_autonomous_agent_runtime",
        "ready_for_multi_cycle_agentic_loop",
        "ready_for_recursive_self_invocation",
        "ready_for_automatic_retry",
        "ready_for_automatic_repair",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
    ],
)
def test_flags_reject_unsafe_true_values(field):
    with pytest.raises(ValueError):
        build_agentic_operation_flags(**{field: True})


def test_policy_allows_bounded_single_cycle_only_and_blocks_autonomy():
    policy = default_agentic_operation_policy()
    assert policy.max_cycle_count == 1
    assert policy.allow_bounded_function_task is True
    assert policy.allow_single_cycle_operation is True
    assert policy.allow_metadata_only_operation is True
    assert policy.require_human_handoff_after_cycle is True
    assert agentic_operation_policy_blocks_autonomy(policy)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_cycle_count": 2},
        {"allow_automatic_retry": True},
        {"allow_automatic_repair": True},
        {"allow_multi_cycle_loop": True},
        {"allow_recursive_self_invocation": True},
        {"allow_independent_agent_runtime": True},
        {"allow_external_agent_orchestration": True},
        {"allow_dominion_runtime": True},
        {"allow_model_invocation": True},
        {"allow_general_tool_execution": True},
        {"allow_live_workspace_write": True},
        {"allow_patch_application": True},
        {"allow_test_execution": True},
        {"allow_shell": True},
    ],
)
def test_policy_rejects_autonomy_and_runtime_permissions(kwargs):
    with pytest.raises(ValueError):
        build_agentic_operation_policy(**kwargs)


def test_source_ref_input_and_intent_are_bounded_task_metadata():
    source_ref = build_agentic_operation_source_ref(source_kind=AgenticOperationSourceKind.MANUAL_OPERATOR_TASK)
    operation_input = build_agentic_operation_input(source_refs=[source_ref])
    intent = build_agentic_operation_intent()
    assert operation_input.requested_mode == AgenticOperationMode.SANDBOX_APPLY_VALIDATION_CYCLE
    assert "automatic_retry" in operation_input.prohibited_runtime_actions
    assert "dominion_runtime" in operation_input.prohibited_runtime_actions
    assert intent.single_cycle_only is True
    assert intent.human_handoff_required is True
    assert intent.automatic_retry_allowed is False
    assert intent.automatic_repair_allowed is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"single_cycle_only": False},
        {"human_handoff_required": False},
        {"automatic_retry_allowed": True},
        {"automatic_repair_allowed": True},
        {"runtime_kind": AgenticOperationRuntimeKind.INDEPENDENT_AUTONOMOUS_AGENT},
    ],
)
def test_intent_rejects_autonomy(kwargs):
    with pytest.raises(ValueError):
        build_agentic_operation_intent(**kwargs)


def test_missing_required_stage_artifact_blocks_or_requires_review():
    missing = build_agentic_operation_stage_artifact_ref(
        artifact_id=None,
        present=False,
        required=True,
        valid_for_cycle=True,
    )
    assert missing.valid_for_cycle is False
    sequence = build_agentic_step_sequence_from_stage_refs([missing])
    assert sequence.blocked is True
    assert sequence.step_records[0].blocked is True
    assert sequence.step_records[0].step_status == AgenticOperationStepStatus.BLOCKED


def test_step_record_never_executes_external_tool_shell_test_live_write_or_repair():
    step = build_agentic_operation_step_record()
    assert step.executed_external_tool is False
    assert step.executed_shell is False
    assert step.executed_test is False
    assert step.wrote_live_workspace is False
    assert step.performed_repair is False
    for field in ("executed_external_tool", "executed_shell", "executed_test", "wrote_live_workspace", "performed_repair"):
        with pytest.raises(ValueError):
            build_agentic_operation_step_record(**{field: True})


def test_step_sequence_actual_count_must_stay_within_max():
    sequence = build_agentic_operation_step_sequence()
    assert sequence.actual_step_count <= sequence.max_step_count
    with pytest.raises(ValueError):
        build_agentic_operation_step_sequence(actual_step_count=13, max_step_count=12)


def test_safety_report_and_stop_reason_preserve_no_execution_or_continuation():
    safety_report = build_agentic_operation_safety_report()
    stop_reason = build_agentic_operation_stop_reason()
    assert safety_report.ready_for_execution is False
    assert agentic_operation_stop_reason_prevents_continuation(stop_reason)
    for field in ("allows_continuation", "allows_retry", "allows_repair"):
        with pytest.raises(ValueError):
            build_agentic_operation_stop_reason(**{field: True})


def test_operation_result_and_run_packet_are_single_cycle_not_production_or_execution():
    result = build_agentic_operation_result()
    packet = build_agentic_operation_run_packet(result=result)
    assert result.completed_single_cycle is True
    assert result.human_handoff_required is True
    assert agentic_operation_result_is_not_production_certification(result)
    assert agentic_operation_run_packet_is_single_cycle(packet)
    assert validate_agentic_operation_run_packet(packet).validation_successful is True


@pytest.mark.parametrize(
    "kwargs",
    [
        {"production_certified": True},
        {"ready_for_execution": True},
        {"ready_for_independent_agent_runtime": True},
        {"ready_for_multi_cycle_agentic_loop": True},
        {"ready_for_live_workspace_write": True},
        {"ready_for_patch_application": True},
        {"ready_for_test_execution": True},
        {"ready_for_shell_execution": True},
    ],
)
def test_operation_result_rejects_unsafe_readiness(kwargs):
    with pytest.raises(ValueError):
        build_agentic_operation_result(**kwargs)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_cycle_count": 2},
        {"cycle_count": 2},
        {"automatic_retry_allowed": True},
        {"automatic_repair_allowed": True},
        {"human_handoff_required": False},
        {"ready_for_execution": True},
    ],
)
def test_run_packet_rejects_retry_repair_continuation_or_execution(kwargs):
    with pytest.raises(ValueError):
        build_agentic_operation_run_packet(**kwargs)


def test_fake_successful_post_apply_validation_produces_completed_single_cycle_packet():
    validation_report = build_sandbox_post_apply_validation_report()
    operation_input = build_agentic_operation_input_from_post_apply_validation(validation_report)
    stage_refs = _present_stage_refs()
    packet = run_bounded_agentic_operation_cycle(operation_input, stage_refs, validation_report)
    assert packet.result.completed_successfully is True
    assert packet.result.status == AgenticOperationStatus.CYCLE_COMPLETED
    assert packet.result.stop_reason.stop_reason_kind == AgenticOperationStopReasonKind.COMPLETED_SINGLE_CYCLE
    assert packet.human_handoff_required is True
    assert packet.automatic_retry_allowed is False
    assert packet.automatic_repair_allowed is False


def test_failed_post_apply_validation_produces_review_required_packet():
    validation_report = build_sandbox_post_apply_validation_report(validation_successful=False)
    operation_input = build_agentic_operation_input_from_post_apply_validation(validation_report)
    packet = run_bounded_agentic_operation_cycle(operation_input, _present_stage_refs(), validation_report)
    assert packet.result.completed_successfully is False
    assert packet.result.status == AgenticOperationStatus.REVIEW_REQUIRED
    assert packet.result.stop_reason.stop_reason_kind == AgenticOperationStopReasonKind.BLOCKED_BY_FAILED_VALIDATION
    assert packet.result.ready_for_future_trace_input is False


def test_blocking_safety_finding_blocks_operation():
    validation_report = build_sandbox_post_apply_validation_report()
    operation_input = build_agentic_operation_input_from_post_apply_validation(validation_report)
    finding = build_agentic_operation_safety_finding()
    packet = run_bounded_agentic_operation_cycle(operation_input, _present_stage_refs(), validation_report, safety_findings=[finding])
    assert packet.result.completed_successfully is False
    assert packet.result.status == AgenticOperationStatus.REVIEW_REQUIRED
    assert packet.result.stop_reason.stop_reason_kind == AgenticOperationStopReasonKind.BLOCKED_BY_SAFETY_REPORT


def test_missing_stage_artifact_blocks_operation():
    validation_report = build_sandbox_post_apply_validation_report()
    operation_input = build_agentic_operation_input_from_post_apply_validation(validation_report)
    stage_refs = _present_stage_refs()
    stage_refs[0] = build_agentic_operation_stage_artifact_ref(
        stage_artifact_ref_id="missing-candidate",
        stage_name="apply_candidate",
        artifact_id=None,
        artifact_summary="missing candidate",
        required=True,
        present=False,
        valid_for_cycle=True,
    )
    packet = run_bounded_agentic_operation_cycle(operation_input, stage_refs, validation_report)
    assert packet.result.completed_successfully is False
    assert packet.result.status == AgenticOperationStatus.BLOCKED
    assert packet.result.stop_reason.stop_reason_kind == AgenticOperationStopReasonKind.BLOCKED_BY_MISSING_ARTIFACT


def test_decision_validation_report_operation_report_preview_and_guarantee():
    decision = build_agentic_operation_decision()
    validation_finding = build_agentic_operation_validation_finding()
    validation_report = build_agentic_operation_validation_report(findings=[validation_finding])
    operation_report = build_agentic_operation_report(validation_report=validation_report)
    preview = build_agentic_operation_run_preview()
    guarantee = build_agentic_operation_no_autonomy_guarantee()
    assert decision.allow_autonomous_runtime is False
    assert decision.allow_multi_cycle_loop is False
    assert validation_report.confirms_single_cycle_limit is True
    assert operation_report.production_certified is False
    assert preview.ready_for_bounded_agentic_task_operation_cycle is True
    assert guarantee.no_independent_autonomous_agent_runtime is True
    assert guarantee.mandatory_human_handoff_after_cycle is True


@pytest.mark.parametrize(
    "field",
    [
        "allow_autonomous_runtime",
        "allow_multi_cycle_loop",
        "allow_automatic_retry",
        "allow_automatic_repair",
        "allow_shell",
        "allow_test_execution",
        "allow_live_workspace_write",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_decision_rejects_unsafe_permissions(field):
    with pytest.raises(ValueError):
        build_agentic_operation_decision(**{field: True})


def test_v0366_readiness_report_unsafe_flags_false():
    report = build_v0366_readiness_report()
    assert isinstance(report, V0366ReadinessReport)
    assert report.ready_for_bounded_agentic_task_operation_cycle is True
    assert report.ready_for_v0367_patch_apply_sandbox_ocel_trace_packet is True
    assert report.ready_for_v0368_cli_sandbox_apply_agentic_surface is True
    assert report.ready_for_execution is False
    assert report.ready_for_independent_agent_runtime is False
    assert report.ready_for_multi_cycle_agentic_loop is False
    assert report.ready_for_automatic_retry is False
    assert report.ready_for_automatic_repair is False
    assert report.ready_for_dominion_runtime is False
    assert v0366_readiness_report_is_not_execution_ready(report)


def test_agentic_operation_module_has_no_runtime_execution_or_file_write_calls():
    source = Path("src/chanta_core/agent_runtime/agentic_operation_cycle.py").read_text(encoding="utf-8")
    assert ".write_text(" not in source
    assert ".write_bytes(" not in source
    assert ".open(\"w\"" not in source
    assert "subprocess.run" not in source
    assert "os.system" not in source
    assert "shell=True" not in source
    assert "git apply" not in source
    assert "apply_patch(" not in source
    assert "pytest.main" not in source
    assert "while " not in source
