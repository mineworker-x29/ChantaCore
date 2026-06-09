from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairProposalLoopArtifactBundle,
    RepairProposalLoopBoundaryAudit,
    RepairProposalLoopConfidenceLevel,
    RepairProposalLoopDecision,
    RepairProposalLoopDecisionKind,
    RepairProposalLoopDisposition,
    RepairProposalLoopDoNothingComparison,
    RepairProposalLoopDoNothingComparisonKind,
    RepairProposalLoopFlagSet,
    RepairProposalLoopInput,
    RepairProposalLoopMode,
    RepairProposalLoopNoExecutionGuarantee,
    RepairProposalLoopOutcomeKind,
    RepairProposalLoopPacket,
    RepairProposalLoopPolicy,
    RepairProposalLoopReadinessLevel,
    RepairProposalLoopReport,
    RepairProposalLoopRiskKind,
    RepairProposalLoopRunPreview,
    RepairProposalLoopSourceKind,
    RepairProposalLoopSourceRef,
    RepairProposalLoopStatus,
    RepairProposalLoopStepKind,
    RepairProposalLoopStepRecord,
    RepairProposalLoopStepStatus,
    RepairProposalLoopStopCondition,
    RepairProposalLoopStopReasonKind,
    RepairProposalLoopValidationFinding,
    RepairProposalLoopValidationReport,
    V0387ReadinessReport,
    audit_repair_proposal_loop_boundaries,
    build_repair_proposal_loop_artifact_bundle,
    build_repair_proposal_loop_boundary_audit,
    build_repair_proposal_loop_decision,
    build_repair_proposal_loop_do_nothing_comparison,
    build_repair_proposal_loop_flags,
    build_repair_proposal_loop_input,
    build_repair_proposal_loop_input_from_human_review_packet,
    build_repair_proposal_loop_no_execution_guarantee,
    build_repair_proposal_loop_packet,
    build_repair_proposal_loop_policy,
    build_repair_proposal_loop_report,
    build_repair_proposal_loop_run_preview,
    build_repair_proposal_loop_source_ref,
    build_repair_proposal_loop_step_record,
    build_repair_proposal_loop_stop_condition,
    build_repair_proposal_loop_validation_finding,
    build_repair_proposal_loop_validation_report,
    build_v0387_readiness_report,
    collect_repair_proposal_loop_artifacts,
    compare_repair_proposal_loop_to_do_nothing,
    create_repair_proposal_loop_packet,
    create_repair_proposal_loop_step_records,
    create_repair_proposal_loop_stop_condition,
    decide_repair_proposal_loop,
    default_repair_proposal_loop_policy,
    repair_proposal_loop_decision_is_not_apply_permission,
    repair_proposal_loop_flags_preserve_no_execution,
    repair_proposal_loop_packet_is_not_execution,
    repair_proposal_loop_policy_blocks_runtime,
    repair_proposal_loop_policy_is_one_shot_only,
    v0387_readiness_report_is_not_execution_ready,
    validate_repair_proposal_loop_packet,
)
import chanta_core.agent_runtime.repair_proposal_loop_trial as loop_module


SAFE_FLAG_NAMES = {
    "ready_for_v0388_cli_repair_proposal_surface",
    "ready_for_v0389_bounded_repair_proposal_loop_consolidation",
    "ready_for_v039_human_approved_sandbox_repair_apply",
    "ready_for_bounded_repair_proposal_loop_trial",
    "ready_for_one_shot_loop_packet",
    "ready_for_loop_artifact_bundle",
    "ready_for_loop_step_records",
    "ready_for_loop_boundary_audit",
    "ready_for_loop_stop_condition",
    "ready_for_loop_do_nothing_comparison",
    "ready_for_loop_decision",
    "ready_for_loop_human_handoff",
    "ready_for_future_cli_repair_proposal_surface_input",
    "ready_for_future_v0389_consolidation_input",
    "ready_for_future_v039_apply_handoff_metadata",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if (field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES)
        or field.name == "production_certified"
    ]


def _complete_bundle():
    return build_repair_proposal_loop_artifact_bundle(
        evidence_bundle_id="evidence",
        source_context_snapshot_id="source-context",
        scope_plan_id="scope-plan",
        proposed_patch_envelope_id="patch-envelope",
        safety_report_id="safety-report",
        human_review_packet_id="review-packet",
        approval_request_contract_id="approval-contract",
    )


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairProposalLoopMode} == {
        "one_shot_loop_trial",
        "loop_artifact_bundle",
        "loop_step_records",
        "loop_boundary_audit",
        "loop_stop_condition",
        "loop_do_nothing_comparison",
        "loop_decision",
        "future_cli_surface_input",
        "future_consolidation_input",
        "future_v039_handoff_metadata",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0386_human_review_packet" in {item.value for item in RepairProposalLoopSourceKind}
    assert "stopped_after_one_cycle" in {item.value for item in RepairProposalLoopStatus}
    assert "future_consolidation_input_ready" in {item.value for item in RepairProposalLoopReadinessLevel}
    assert "allow_future_v039_handoff_metadata" in {item.value for item in RepairProposalLoopDecisionKind}
    assert "multi_cycle_loop_risk" in {item.value for item in RepairProposalLoopRiskKind}
    assert "human_handoff_step" in {item.value for item in RepairProposalLoopStepKind}
    assert "completed_as_metadata" in {item.value for item in RepairProposalLoopStepStatus}
    assert "stopped_for_human_handoff" in {item.value for item in RepairProposalLoopStopReasonKind}
    assert "future_v039_handoff_metadata_ready" in {item.value for item in RepairProposalLoopOutcomeKind}
    assert "trial_ready" in {item.value for item in RepairProposalLoopDisposition}
    assert "inconclusive" in {item.value for item in RepairProposalLoopConfidenceLevel}
    assert "do_nothing_preferred_due_to_missing_artifact" in {
        item.value for item in RepairProposalLoopDoNothingComparisonKind
    }


def test_required_models_are_exported():
    for model in (
        RepairProposalLoopFlagSet,
        RepairProposalLoopSourceRef,
        RepairProposalLoopPolicy,
        RepairProposalLoopInput,
        RepairProposalLoopArtifactBundle,
        RepairProposalLoopStepRecord,
        RepairProposalLoopBoundaryAudit,
        RepairProposalLoopStopCondition,
        RepairProposalLoopDoNothingComparison,
        RepairProposalLoopDecision,
        RepairProposalLoopPacket,
        RepairProposalLoopValidationFinding,
        RepairProposalLoopValidationReport,
        RepairProposalLoopReport,
        RepairProposalLoopRunPreview,
        RepairProposalLoopNoExecutionGuarantee,
        V0387ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_loop_metadata_readiness_and_preserve_no_execution():
    flags = build_repair_proposal_loop_flags()
    assert flags.repair_proposal_loop_trial_layer_constructed
    assert flags.one_shot_loop_trial_available
    assert flags.loop_artifact_bundle_available
    assert flags.loop_step_records_available
    assert flags.loop_boundary_audit_available
    assert flags.loop_stop_condition_available
    assert flags.loop_do_nothing_comparison_available
    assert flags.loop_decision_available
    assert flags.loop_human_handoff_available
    for name in SAFE_FLAG_NAMES:
        assert getattr(flags, name)
    for name in _unsafe_flag_names(RepairProposalLoopFlagSet):
        assert not getattr(flags, name)
    assert repair_proposal_loop_flags_preserve_no_execution(flags)
    assert flags.metadata["mandatory_stop_after_one_cycle"]


@pytest.mark.parametrize("flag_name", _unsafe_flag_names(RepairProposalLoopFlagSet))
def test_flags_reject_unsafe_readiness(flag_name):
    with pytest.raises(ValueError):
        build_repair_proposal_loop_flags(**{flag_name: True})


def test_policy_is_one_shot_only_and_blocks_runtime():
    policy = default_repair_proposal_loop_policy()
    assert policy.max_cycle_count == 1
    assert policy.max_retry_count == 0
    assert policy.require_evidence_bundle
    assert policy.require_source_context_snapshot
    assert policy.require_scope_plan
    assert policy.require_patch_envelope
    assert policy.require_safety_report
    assert policy.require_human_review_packet
    assert policy.require_do_nothing_comparison
    assert policy.require_stop_reason
    assert policy.require_human_handoff
    assert policy.allow_one_shot_loop_packet
    assert policy.allow_loop_artifact_bundle
    assert policy.allow_loop_step_records
    assert policy.allow_loop_boundary_audit
    assert policy.allow_loop_stop_condition
    assert policy.allow_future_cli_surface_input
    assert policy.allow_future_consolidation_input
    assert policy.allow_future_v039_handoff_metadata
    assert repair_proposal_loop_policy_is_one_shot_only(policy)
    assert repair_proposal_loop_policy_blocks_runtime(policy)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_cycle_count": 2},
        {"max_retry_count": 1},
        {"allow_autonomous_loop_runtime": True},
        {"allow_multi_cycle_loop": True},
        {"allow_retry_loop": True},
        {"allow_automatic_repair": True},
        {"allow_human_approval_capture": True},
        {"allow_approval_grant": True},
        {"allow_apply_permission": True},
        {"allow_source_file_read": True},
        {"allow_new_proposed_diff_generation": True},
        {"allow_new_proposed_code_hunk_generation": True},
        {"allow_new_proposed_patch_envelope_generation": True},
        {"allow_test_execution": True},
        {"allow_shell": True},
        {"allow_model_provider_invocation": True},
        {"allow_external_agent_execution": True},
        {"allow_dominion_runtime": True},
    ],
)
def test_policy_rejects_runtime_or_unbounded_loop_permissions(kwargs):
    with pytest.raises(ValueError):
        build_repair_proposal_loop_policy(**kwargs)


def test_loop_input_is_packet_request_not_execution_request():
    input_model = build_repair_proposal_loop_input()
    assert input_model.requested_mode == RepairProposalLoopMode.ONE_SHOT_LOOP_TRIAL
    for required in (
        "autonomous_loop",
        "multi_cycle_loop",
        "retry_loop",
        "approval_capture",
        "approval_grant",
        "apply_permission",
        "source_read",
        "new_patch_generation",
        "patch_apply",
        "apply_patch",
        "git_apply",
        "repair_execution",
        "test_execution",
        "subprocess",
        "shell",
        "dependency_install",
        "network",
        "model_provider",
        "external_agent",
        "dominion",
    ):
        assert required in input_model.prohibited_runtime_actions


def test_source_ref_is_metadata_only():
    source_ref = build_repair_proposal_loop_source_ref()
    assert source_ref.source_summary
    assert source_ref.evidence_refs == []


def test_artifact_bundle_completeness_tracks_required_existing_artifacts():
    missing = build_repair_proposal_loop_artifact_bundle()
    assert not missing.complete_for_one_shot_trial
    assert "evidence_bundle_id" in missing.missing_artifacts

    complete = _complete_bundle()
    assert complete.complete_for_one_shot_trial
    assert complete.complete_for_future_cli_surface
    assert complete.complete_for_future_v039_handoff_metadata
    assert complete.missing_artifacts == []

    with pytest.raises(ValueError):
        build_repair_proposal_loop_artifact_bundle(complete_for_one_shot_trial=True)


def test_step_records_are_metadata_only_and_reject_runtime_flags():
    record = build_repair_proposal_loop_step_record(completed_as_metadata=True)
    assert record.completed_as_metadata
    for name in (
        "executed_runtime_action",
        "performed_source_read",
        "generated_new_patch_metadata",
        "wrote_file",
        "applied_patch",
        "ran_tests",
        "invoked_model",
        "invoked_external_agent",
    ):
        assert not getattr(record, name)
        with pytest.raises(ValueError):
            build_repair_proposal_loop_step_record(**{name: True})


def test_create_step_records_marks_missing_and_present_artifacts():
    missing_bundle = build_repair_proposal_loop_artifact_bundle()
    missing_steps = create_repair_proposal_loop_step_records(missing_bundle)
    assert any(step.step_status == RepairProposalLoopStepStatus.ARTIFACT_MISSING for step in missing_steps)

    complete_steps = create_repair_proposal_loop_step_records(_complete_bundle())
    assert all(
        step.step_status == RepairProposalLoopStepStatus.COMPLETED_AS_METADATA for step in complete_steps
    )


def test_boundary_audit_confirms_no_runtime_surfaces():
    audit = build_repair_proposal_loop_boundary_audit()
    assert audit.approval_absent_confirmed
    assert audit.no_apply_permission_confirmed
    assert audit.no_source_read_confirmed
    assert audit.no_new_patch_generation_confirmed
    assert audit.no_file_write_confirmed
    assert audit.no_patch_apply_confirmed
    assert audit.no_repair_execution_confirmed
    assert audit.no_test_execution_confirmed
    assert audit.no_model_invocation_confirmed
    assert audit.no_external_agent_confirmed
    assert audit.no_dominion_runtime_confirmed
    assert audit.no_production_certification_confirmed

    missing_audit = audit_repair_proposal_loop_boundaries(
        create_repair_proposal_loop_step_records(build_repair_proposal_loop_artifact_bundle())
    )
    assert RepairProposalLoopRiskKind.MISSING_EVIDENCE_BUNDLE_RISK in missing_audit.risk_kinds


def test_stop_condition_enforces_single_cycle_retry_zero_and_handoff():
    stop = create_repair_proposal_loop_stop_condition()
    assert stop.cycle_count_at_stop <= 1
    assert stop.retry_count_at_stop == 0
    assert stop.human_handoff_required
    assert stop.approval_absent
    assert stop.apply_not_allowed
    assert stop.repair_not_executed
    assert stop.tests_not_run

    for kwargs in (
        {"cycle_count_at_stop": 2},
        {"retry_count_at_stop": 1},
        {"human_handoff_required": False},
        {"approval_absent": False},
        {"apply_not_allowed": False},
        {"repair_not_executed": False},
        {"tests_not_run": False},
    ):
        with pytest.raises(ValueError):
            build_repair_proposal_loop_stop_condition(**kwargs)


def test_do_nothing_comparison_is_always_represented():
    missing_bundle = build_repair_proposal_loop_artifact_bundle()
    missing_audit = audit_repair_proposal_loop_boundaries(create_repair_proposal_loop_step_records(missing_bundle))
    comparison = compare_repair_proposal_loop_to_do_nothing(missing_bundle, missing_audit)
    assert comparison.do_nothing_remains_valid
    assert comparison.do_nothing_preferred
    assert comparison.do_nothing_required
    assert not comparison.loop_packet_outperforms_do_nothing

    complete_bundle = _complete_bundle()
    complete_audit = audit_repair_proposal_loop_boundaries(create_repair_proposal_loop_step_records(complete_bundle))
    complete_comparison = compare_repair_proposal_loop_to_do_nothing(complete_bundle, complete_audit)
    assert complete_comparison.do_nothing_remains_valid


def test_loop_decision_allows_future_metadata_only_and_blocks_runtime_now():
    decision = build_repair_proposal_loop_decision()
    assert decision.ready_for_future_cli_surface_input
    assert decision.ready_for_future_consolidation_input
    assert decision.ready_for_future_v039_handoff_metadata
    assert repair_proposal_loop_decision_is_not_apply_permission(decision)
    for name in (
        "autonomous_loop_allowed_now",
        "retry_allowed_now",
        "multi_cycle_allowed_now",
        "approval_capture_allowed_now",
        "approval_grant_allowed_now",
        "apply_permission_allowed_now",
        "source_read_allowed_now",
        "new_patch_generation_allowed_now",
        "file_write_allowed_now",
        "patch_application_allowed_now",
        "repair_execution_allowed_now",
        "test_execution_allowed_now",
        "model_provider_invocation_allowed_now",
        "external_agent_allowed_now",
        "production_certified",
    ):
        assert not getattr(decision, name)
        with pytest.raises(ValueError):
            build_repair_proposal_loop_decision(**{name: True})


def test_decide_loop_blocks_future_metadata_when_required_artifacts_missing():
    bundle = build_repair_proposal_loop_artifact_bundle()
    audit = audit_repair_proposal_loop_boundaries(create_repair_proposal_loop_step_records(bundle))
    comparison = compare_repair_proposal_loop_to_do_nothing(bundle, audit)
    decision = decide_repair_proposal_loop(bundle, audit, comparison)
    assert decision.decision_kind == RepairProposalLoopDecisionKind.MISSING_REQUIRED_ARTIFACT
    assert not decision.ready_for_future_cli_surface_input
    assert not decision.ready_for_future_consolidation_input
    assert not decision.ready_for_future_v039_handoff_metadata


def test_loop_packet_is_bounded_one_shot_and_not_execution():
    packet = build_repair_proposal_loop_packet()
    assert packet.max_cycle_count == 1
    assert packet.actual_cycle_count <= 1
    assert packet.retry_count == 0
    assert packet.bounded
    assert packet.human_handoff_required
    assert not packet.human_approval_present
    assert not packet.approval_granted
    assert not packet.approval_captured_now
    assert not packet.apply_allowed
    assert not packet.sandbox_apply_allowed
    assert not packet.live_apply_allowed
    for name in (
        "autonomous_loop_started",
        "retry_performed",
        "multi_cycle_performed",
        "source_read_performed_by_v0387",
        "new_patch_metadata_generated_by_v0387",
        "file_write_performed",
        "patch_file_written",
        "file_edit_performed",
        "patch_applied",
        "apply_patch_called",
        "git_apply_called",
        "tests_run",
        "repair_executed",
        "model_invocation_performed",
        "external_agent_invoked",
        "dominion_runtime_invoked",
        "production_certified",
        "ready_for_execution",
    ):
        assert not getattr(packet, name)
    assert repair_proposal_loop_packet_is_not_execution(packet)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"max_cycle_count": 2},
        {"actual_cycle_count": 2},
        {"retry_count": 1},
        {"bounded": False},
        {"human_handoff_required": False},
        {"human_approval_present": True},
        {"approval_granted": True},
        {"apply_allowed": True},
        {"repair_executed": True},
        {"tests_run": True},
    ],
)
def test_loop_packet_rejects_execution_or_unbounded_state(kwargs):
    with pytest.raises(ValueError):
        build_repair_proposal_loop_packet(**kwargs)


def test_create_loop_packet_from_existing_metadata_ids_only():
    packet = create_repair_proposal_loop_packet(
        human_review_packet={"human_review_packet_id": "review-packet"},
        approval_request_contract={"approval_request_contract_id": "approval-contract"},
        safety_report={"safety_report_id": "safety-report"},
        proposed_patch_envelope={"proposed_patch_envelope_id": "patch-envelope"},
        scope_plan={"scope_plan_id": "scope-plan"},
        source_context_snapshot={"source_context_snapshot_id": "source-context"},
        evidence_bundle={"evidence_bundle_id": "evidence"},
    )
    assert packet.artifact_bundle.complete_for_one_shot_trial
    assert packet.stop_condition.cycle_count_at_stop == 1
    assert packet.stop_condition.retry_count_at_stop == 0
    assert packet.ready_for_future_cli_surface_input
    assert packet.ready_for_future_consolidation_input
    assert packet.ready_for_future_v039_handoff_metadata
    assert "No autonomous loop" in packet.rendered_packet_preview


def test_loop_input_from_human_review_packet_uses_existing_supplied_ids():
    input_model = build_repair_proposal_loop_input_from_human_review_packet(
        {"human_review_packet_id": "review-packet"},
        approval_request_contract={"approval_request_contract_id": "approval-contract"},
        safety_report={"safety_report_id": "safety-report"},
        proposed_patch_envelope={"proposed_patch_envelope_id": "patch-envelope"},
        scope_plan={"scope_plan_id": "scope-plan"},
        source_context_snapshot={"source_context_snapshot_id": "source-context"},
        evidence_bundle={"evidence_bundle_id": "evidence"},
    )
    assert input_model.human_review_packet_id == "review-packet"
    assert input_model.approval_request_contract_id == "approval-contract"
    assert input_model.safety_report_id == "safety-report"
    assert input_model.proposed_patch_envelope_id == "patch-envelope"
    assert input_model.scope_plan_id == "scope-plan"
    assert input_model.source_context_snapshot_id == "source-context"
    assert input_model.evidence_bundle_id == "evidence"


def test_validation_report_and_loop_report_preserve_no_execution():
    packet = build_repair_proposal_loop_packet()
    validation = validate_repair_proposal_loop_packet(packet)
    assert validation.findings == []
    assert validation.confirms_one_shot_only
    assert validation.confirms_max_cycle_one
    assert validation.confirms_retry_zero
    assert validation.confirms_stop_condition
    assert validation.confirms_human_handoff
    assert validation.confirms_no_approval
    assert validation.confirms_no_apply
    assert validation.confirms_no_source_read
    assert validation.confirms_no_new_patch_generation
    assert validation.confirms_no_file_write
    assert validation.confirms_no_external_send
    assert validation.confirms_no_ui_runtime
    assert validation.confirms_no_patch_apply
    assert validation.confirms_no_repair_execution
    assert validation.confirms_no_tests
    assert validation.confirms_no_external_calls

    report = build_repair_proposal_loop_report(validation_report=validation)
    assert report.ready_for_future_cli_surface_input
    assert report.ready_for_future_consolidation_input
    assert report.ready_for_future_v039_handoff_metadata
    assert not report.ready_for_execution
    assert not report.production_certified


def test_no_execution_guarantee_and_readiness_report_unsafe_flags_false():
    guarantee = build_repair_proposal_loop_no_execution_guarantee()
    assert guarantee.no_autonomous_loop
    assert guarantee.no_retry
    assert guarantee.no_multi_cycle
    assert guarantee.no_approval
    assert guarantee.no_apply
    assert guarantee.no_source_read
    assert guarantee.no_new_patch_generation
    assert guarantee.no_file_write
    assert guarantee.no_external_send
    assert guarantee.no_ui
    assert guarantee.no_patch_apply
    assert guarantee.no_repair
    assert guarantee.no_test
    assert guarantee.no_external_call

    readiness = build_v0387_readiness_report(no_execution_guarantee=guarantee)
    assert readiness.ready_for_v0388_cli_repair_proposal_surface
    assert readiness.ready_for_v0389_bounded_repair_proposal_loop_consolidation
    assert readiness.ready_for_v039_human_approved_sandbox_repair_apply
    assert readiness.ready_for_bounded_repair_proposal_loop_trial
    assert v0387_readiness_report_is_not_execution_ready(readiness)


def test_run_preview_is_metadata_preview_only():
    preview = build_repair_proposal_loop_run_preview()
    assert preview.max_cycle_count == 1
    assert preview.retry_count == 0
    assert not preview.would_start_autonomous_loop
    assert not preview.would_apply_patch
    assert not preview.would_run_tests
    assert not preview.would_invoke_external_systems


def test_builder_helpers_exist_and_preserve_boundaries():
    helpers = (
        build_repair_proposal_loop_flags,
        build_repair_proposal_loop_source_ref,
        build_repair_proposal_loop_policy,
        build_repair_proposal_loop_input,
        build_repair_proposal_loop_artifact_bundle,
        build_repair_proposal_loop_step_record,
        build_repair_proposal_loop_boundary_audit,
        build_repair_proposal_loop_stop_condition,
        build_repair_proposal_loop_do_nothing_comparison,
        build_repair_proposal_loop_decision,
        build_repair_proposal_loop_packet,
        build_repair_proposal_loop_validation_finding,
        build_repair_proposal_loop_validation_report,
        build_repair_proposal_loop_report,
        build_repair_proposal_loop_run_preview,
        build_repair_proposal_loop_no_execution_guarantee,
        build_v0387_readiness_report,
        default_repair_proposal_loop_policy,
        build_repair_proposal_loop_input_from_human_review_packet,
        collect_repair_proposal_loop_artifacts,
        create_repair_proposal_loop_step_records,
        audit_repair_proposal_loop_boundaries,
        create_repair_proposal_loop_stop_condition,
        compare_repair_proposal_loop_to_do_nothing,
        decide_repair_proposal_loop,
        create_repair_proposal_loop_packet,
        validate_repair_proposal_loop_packet,
        repair_proposal_loop_flags_preserve_no_execution,
        repair_proposal_loop_policy_is_one_shot_only,
        repair_proposal_loop_policy_blocks_runtime,
        repair_proposal_loop_packet_is_not_execution,
        repair_proposal_loop_decision_is_not_apply_permission,
        v0387_readiness_report_is_not_execution_ready,
    )
    assert all(callable(helper) for helper in helpers)


def test_implementation_does_not_contain_runtime_action_calls():
    source = inspect.getsource(loop_module)
    forbidden_fragments = (
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
        "apply_patch(",
        "approval_granted=True",
        "human_approval_present=True",
        "approval_captured_now=True",
        "apply_allowed=True",
        "sandbox_apply_allowed=True",
    )
    for forbidden in forbidden_fragments:
        assert forbidden not in source
