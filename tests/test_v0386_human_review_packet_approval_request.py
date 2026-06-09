from dataclasses import fields
import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairApplyPrecondition,
    RepairApplyPreconditionKind,
    RepairApprovalRequestContract,
    RepairApprovalRequestKind,
    RepairHumanReviewConfidenceLevel,
    RepairHumanReviewDecision,
    RepairHumanReviewDecisionKind,
    RepairHumanReviewDisposition,
    RepairHumanReviewDoNothingComparison,
    RepairHumanReviewDoNothingComparisonKind,
    RepairHumanReviewFlagSet,
    RepairHumanReviewInput,
    RepairHumanReviewMode,
    RepairHumanReviewNoApprovalGuarantee,
    RepairHumanReviewPacket,
    RepairHumanReviewPolicy,
    RepairHumanReviewReadinessLevel,
    RepairHumanReviewReport,
    RepairHumanReviewRiskKind,
    RepairHumanReviewRunPreview,
    RepairHumanReviewSourceKind,
    RepairHumanReviewSourceRef,
    RepairHumanReviewStatus,
    RepairHumanReviewValidationFinding,
    RepairHumanReviewValidationReport,
    RepairProposalSafetyStatus,
    RepairReviewChecklistItem,
    RepairReviewChecklistItemKind,
    RepairReviewEvidenceSummary,
    RepairReviewPacketSectionKind,
    RepairReviewPatchSummary,
    RepairReviewQuestion,
    RepairReviewQuestionKind,
    RepairReviewSafetySummary,
    V0386ReadinessReport,
    build_proposed_change_evidence_map,
    build_proposed_change_rationale,
    build_proposed_code_hunk,
    build_proposed_diff_metadata,
    build_proposed_file_change,
    build_proposed_patch_do_nothing_comparison,
    build_proposed_patch_envelope,
    build_proposed_patch_review_requirement,
    build_repair_apply_precondition,
    build_repair_approval_request_contract,
    build_repair_human_review_decision,
    build_repair_human_review_do_nothing_comparison,
    build_repair_human_review_flags,
    build_repair_human_review_input,
    build_repair_human_review_input_from_safety_report,
    build_repair_human_review_no_approval_guarantee,
    build_repair_human_review_packet,
    build_repair_human_review_policy,
    build_repair_human_review_report,
    build_repair_human_review_run_preview,
    build_repair_human_review_source_ref,
    build_repair_human_review_validation_finding,
    build_repair_human_review_validation_report,
    build_repair_proposal_safety_report,
    build_repair_review_checklist_item,
    build_repair_review_evidence_summary,
    build_repair_review_patch_summary,
    build_repair_review_question,
    build_repair_review_safety_summary,
    build_v0386_readiness_report,
    compare_repair_review_packet_to_do_nothing,
    create_repair_apply_preconditions,
    create_repair_approval_request_contract,
    create_repair_human_review_packet,
    create_repair_review_checklist,
    create_repair_review_evidence_summary,
    create_repair_review_patch_summary,
    create_repair_review_questions,
    create_repair_review_safety_summary,
    decide_repair_human_review_readiness,
    default_repair_human_review_policy,
    repair_approval_request_contract_is_not_approval,
    repair_human_review_decision_is_not_approval,
    repair_human_review_flags_preserve_no_approval,
    repair_human_review_packet_is_not_apply_permission,
    repair_human_review_policy_blocks_approval_and_apply,
    v0386_readiness_report_is_not_execution_ready,
    validate_repair_human_review_packet,
)
import chanta_core.agent_runtime.repair_human_review as review_module


SAFE_FLAG_NAMES = {
    "ready_for_v0387_bounded_repair_proposal_loop_trial",
    "ready_for_v0388_cli_repair_proposal_surface",
    "ready_for_v039_human_approved_sandbox_repair_apply",
    "ready_for_human_review_packet",
    "ready_for_approval_request_contract",
    "ready_for_review_checklist",
    "ready_for_review_questions",
    "ready_for_apply_precondition_metadata",
    "ready_for_review_evidence_summary",
    "ready_for_review_patch_summary",
    "ready_for_review_safety_summary",
    "ready_for_review_do_nothing_comparison",
    "ready_for_future_bounded_repair_proposal_loop_trial_input",
    "ready_for_future_cli_repair_proposal_surface_input",
    "ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if (field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES)
        or field.name == "production_certified"
    ]


def _patch_envelope():
    evidence_map = build_proposed_change_evidence_map()
    rationale = build_proposed_change_rationale(evidence_map_id=evidence_map.change_evidence_map_id)
    hunk = build_proposed_code_hunk(target_relative_path="src/pkg/module.py")
    diff = build_proposed_diff_metadata(
        target_relative_path="src/pkg/module.py",
        hunk_ids=[hunk.proposed_hunk_id],
        evidence_map_id=evidence_map.change_evidence_map_id,
    )
    file_change = build_proposed_file_change(
        target_relative_path="src/pkg/module.py",
        proposed_hunks=[hunk],
        proposed_diff=diff,
        rationale=rationale,
        evidence_map=evidence_map,
    )
    return build_proposed_patch_envelope(
        file_changes=[file_change],
        proposed_diffs=[diff],
        proposed_hunks=[hunk],
        evidence_map=evidence_map,
        rationale=rationale,
        review_requirement=build_proposed_patch_review_requirement(),
        do_nothing_comparison=build_proposed_patch_do_nothing_comparison(),
        source_refs=[],
    )


def _safety_report(blocked=False):
    return build_repair_proposal_safety_report(
        status=RepairProposalSafetyStatus.REVIEW_REQUIRED if blocked else RepairProposalSafetyStatus.VALIDATION_COMPLETED,
        ready_for_future_loop_trial_input=not blocked,
    )


def test_taxonomies_have_required_values():
    assert {item.value for item in RepairHumanReviewMode} == {
        "human_review_packet",
        "approval_request_contract",
        "review_checklist",
        "review_questions",
        "apply_precondition_metadata",
        "review_evidence_summary",
        "review_patch_summary",
        "review_safety_summary",
        "do_nothing_review_comparison",
        "future_loop_trial_input",
        "future_cli_surface_input",
        "future_v039_apply_contract_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0385_safety_report" in {item.value for item in RepairHumanReviewSourceKind}
    assert "approval_request_contract_created" in {item.value for item in RepairHumanReviewStatus}
    assert "future_v039_apply_contract_input_ready" in {item.value for item in RepairHumanReviewReadinessLevel}
    assert "allow_future_v039_apply_contract_input" in {item.value for item in RepairHumanReviewDecisionKind}
    assert "approval_confusion_risk" in {item.value for item in RepairHumanReviewRiskKind}
    assert "approval_request_contract" in {item.value for item in RepairReviewPacketSectionKind}
    assert "request_approval_for_future_v039_sandbox_apply" in {item.value for item in RepairApprovalRequestKind}
    assert "verify_no_apply_permission" in {item.value for item in RepairReviewChecklistItemKind}
    assert "should_prepare_future_v039_sandbox_apply_contract" in {item.value for item in RepairReviewQuestionKind}
    assert "human_approval_required" in {item.value for item in RepairApplyPreconditionKind}
    assert "review_packet_ready" in {item.value for item in RepairHumanReviewDisposition}
    assert "inconclusive" in {item.value for item in RepairHumanReviewConfidenceLevel}
    assert "do_nothing_required_due_to_blocking_issue" in {item.value for item in RepairHumanReviewDoNothingComparisonKind}


def test_required_models_are_exported():
    for model in (
        RepairHumanReviewFlagSet,
        RepairHumanReviewSourceRef,
        RepairHumanReviewPolicy,
        RepairHumanReviewInput,
        RepairReviewEvidenceSummary,
        RepairReviewPatchSummary,
        RepairReviewSafetySummary,
        RepairReviewChecklistItem,
        RepairReviewQuestion,
        RepairApplyPrecondition,
        RepairHumanReviewDoNothingComparison,
        RepairApprovalRequestContract,
        RepairHumanReviewPacket,
        RepairHumanReviewDecision,
        RepairHumanReviewValidationFinding,
        RepairHumanReviewValidationReport,
        RepairHumanReviewReport,
        RepairHumanReviewRunPreview,
        RepairHumanReviewNoApprovalGuarantee,
        V0386ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_review_metadata_readiness_and_preserve_no_approval():
    flags = build_repair_human_review_flags()
    assert flags.repair_human_review_layer_constructed
    assert flags.human_review_packet_available
    assert flags.approval_request_contract_available
    assert flags.review_checklist_available
    assert flags.review_questions_available
    assert flags.apply_precondition_metadata_available
    assert flags.ready_for_v0387_bounded_repair_proposal_loop_trial
    assert flags.ready_for_v0388_cli_repair_proposal_surface
    assert flags.ready_for_v039_human_approved_sandbox_repair_apply
    assert flags.ready_for_human_review_packet
    assert flags.ready_for_approval_request_contract
    assert flags.ready_for_future_v039_human_approved_sandbox_repair_apply_contract_input
    assert repair_human_review_flags_preserve_no_approval(flags)
    assert flags.metadata["approval_request_not_approval"] is True
    for field_name in _unsafe_flag_names(RepairHumanReviewFlagSet):
        assert getattr(flags, field_name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(RepairHumanReviewFlagSet))
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_human_review_flags(**{field_name: True})


def test_policy_allows_review_contract_and_blocks_approval_apply_runtime():
    policy = build_repair_human_review_policy()
    assert policy.allow_human_review_packet
    assert policy.allow_approval_request_contract
    assert policy.allow_review_checklist
    assert policy.allow_review_questions
    assert policy.allow_apply_precondition_metadata
    assert policy.allow_future_loop_trial_input
    assert policy.allow_future_cli_surface_input
    assert policy.allow_future_v039_apply_contract_input
    assert repair_human_review_policy_blocks_approval_and_apply(policy)
    for field in fields(RepairHumanReviewPolicy):
        if field.name.startswith("allow_") and field.name not in {
            "allow_human_review_packet",
            "allow_approval_request_contract",
            "allow_review_checklist",
            "allow_review_questions",
            "allow_apply_precondition_metadata",
            "allow_future_loop_trial_input",
            "allow_future_cli_surface_input",
            "allow_future_v039_apply_contract_input",
        }:
            assert getattr(policy, field.name) is False


@pytest.mark.parametrize(
    "field_name",
    [
        "allow_human_approval_capture",
        "allow_approval_grant",
        "allow_apply_permission",
        "allow_review_packet_file_write",
        "allow_review_packet_external_send",
        "allow_ui_runtime",
        "allow_source_file_read",
        "allow_patch_file_write",
        "allow_file_edit",
        "allow_patch_application",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_repair_execution",
        "allow_test_execution",
        "allow_subprocess",
        "allow_shell",
        "allow_dependency_install",
        "allow_network_access",
        "allow_model_provider_invocation",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_unsafe_allow_true(field_name):
    with pytest.raises(ValueError):
        build_repair_human_review_policy(**{field_name: True})


def test_human_review_input_is_not_approval_or_apply_request():
    review_input = build_repair_human_review_input()
    for action in (
        "approval_capture",
        "approval_grant",
        "apply_permission",
        "review_packet_file_write",
        "external_send",
        "ui_runtime",
        "source_read",
        "patch_file_write",
        "file_edit",
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
        assert action in review_input.prohibited_runtime_actions
    with pytest.raises(ValueError):
        build_repair_human_review_input(prohibited_runtime_actions=["approval_capture"])


def test_summaries_checklist_questions_and_preconditions_preserve_boundaries():
    evidence = build_repair_review_evidence_summary(summary_text="evidence " * 1000, limit=100)
    assert evidence.bounded
    assert evidence.redacted
    patch = build_repair_review_patch_summary(patch_applied=False, repair_executed=False)
    assert patch.patch_applied is False
    assert patch.repair_executed is False
    with pytest.raises(ValueError):
        build_repair_review_patch_summary(patch_applied=True)
    safety = build_repair_review_safety_summary()
    assert safety.apply_allowed is False
    assert safety.production_certified is False
    with pytest.raises(ValueError):
        build_repair_review_safety_summary(apply_allowed=True)
    checklist = build_repair_review_checklist_item()
    assert checklist.metadata["checklist_item_is_not_approval"] is True
    question = build_repair_review_question()
    assert question.response_captured_now is False
    with pytest.raises(ValueError):
        build_repair_review_question(response_captured_now=True)
    precondition = build_repair_apply_precondition()
    assert precondition.grants_apply_permission is False
    with pytest.raises(ValueError):
        build_repair_apply_precondition(grants_apply_permission=True)


def test_do_nothing_review_comparison_is_represented():
    comparison = build_repair_human_review_do_nothing_comparison()
    assert comparison.do_nothing_remains_valid
    safety = build_repair_review_safety_summary(blocking_issue_count=1, safe_for_future_loop_trial_input=False)
    blocking = compare_repair_review_packet_to_do_nothing(safety)
    assert blocking.do_nothing_required
    assert blocking.review_packet_outperforms_do_nothing is False


def test_approval_request_contract_is_not_approval():
    contract = build_repair_approval_request_contract()
    assert contract.human_approval_present is False
    assert contract.approval_granted is False
    assert contract.approval_captured_now is False
    assert contract.apply_allowed is False
    assert contract.sandbox_apply_allowed is False
    assert contract.live_apply_allowed is False
    assert contract.patch_application_allowed is False
    assert contract.repair_execution_allowed is False
    assert repair_approval_request_contract_is_not_approval(contract)
    for field_name in (
        "human_approval_present",
        "approval_granted",
        "approval_captured_now",
        "apply_allowed",
        "sandbox_apply_allowed",
        "live_apply_allowed",
        "patch_application_allowed",
        "repair_execution_allowed",
    ):
        with pytest.raises(ValueError):
            build_repair_approval_request_contract(**{field_name: True})


def test_human_review_packet_is_in_memory_metadata_not_apply_permission():
    packet = build_repair_human_review_packet()
    assert packet.bounded
    assert packet.rendered_packet_preview
    assert packet.ready_for_future_loop_trial_input
    assert packet.ready_for_future_cli_surface_input
    assert packet.ready_for_future_v039_apply_contract_input
    assert packet.human_approval_present is False
    assert packet.approval_granted is False
    assert packet.approval_captured_now is False
    assert packet.apply_allowed is False
    assert packet.sandbox_apply_allowed is False
    assert packet.live_apply_allowed is False
    assert packet.review_packet_written_to_file is False
    assert packet.review_packet_sent_externally is False
    assert packet.ui_runtime_invoked is False
    assert packet.patch_applied is False
    assert packet.apply_patch_called is False
    assert packet.git_apply_called is False
    assert packet.tests_run is False
    assert packet.repair_executed is False
    assert packet.model_invocation_performed is False
    assert packet.external_agent_invoked is False
    assert packet.production_certified is False
    assert packet.ready_for_execution is False
    assert repair_human_review_packet_is_not_apply_permission(packet)


@pytest.mark.parametrize(
    "field_name",
    [
        "human_approval_present",
        "approval_granted",
        "approval_captured_now",
        "apply_allowed",
        "sandbox_apply_allowed",
        "live_apply_allowed",
        "review_packet_written_to_file",
        "review_packet_sent_externally",
        "ui_runtime_invoked",
        "patch_applied",
        "apply_patch_called",
        "git_apply_called",
        "tests_run",
        "repair_executed",
        "production_certified",
        "ready_for_execution",
    ],
)
def test_human_review_packet_rejects_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_repair_human_review_packet(**{field_name: True})


def test_human_review_decision_never_allows_approval_or_apply_now():
    decision = build_repair_human_review_decision()
    assert decision.ready_for_future_loop_trial_input
    assert decision.ready_for_future_cli_surface_input
    assert decision.ready_for_future_v039_apply_contract_input
    assert repair_human_review_decision_is_not_approval(decision)
    for field_name in (
        "approval_capture_allowed_now",
        "approval_grant_allowed_now",
        "apply_permission_allowed_now",
        "file_write_allowed_now",
        "external_send_allowed_now",
        "ui_runtime_allowed_now",
        "patch_application_allowed_now",
        "repair_execution_allowed_now",
        "test_execution_allowed_now",
        "model_provider_invocation_allowed_now",
        "external_agent_allowed_now",
        "production_certified",
    ):
        with pytest.raises(ValueError):
            build_repair_human_review_decision(**{field_name: True})


def test_helpers_create_review_packet_from_safety_and_patch_metadata():
    safety_report = _safety_report()
    envelope = _patch_envelope()
    review_input = build_repair_human_review_input_from_safety_report(safety_report, envelope)
    packet = create_repair_human_review_packet(review_input, safety_report, envelope)
    assert packet.evidence_summary
    assert packet.patch_summary.proposed_hunk_count == 1
    assert packet.safety_summary.apply_allowed is False
    assert packet.checklist_items
    assert packet.review_questions
    assert packet.apply_preconditions
    assert packet.approval_request_contract.approval_granted is False
    decision = decide_repair_human_review_readiness(packet)
    assert repair_human_review_decision_is_not_approval(decision)


def test_validation_report_report_preview_guarantee_and_readiness():
    packet = build_repair_human_review_packet()
    validation = validate_repair_human_review_packet(packet)
    assert validation.packet_completeness_confirmed
    assert validation.review_checklist_confirmed
    assert validation.approval_request_contract_confirmed
    assert validation.do_nothing_comparison_confirmed
    assert validation.no_approval_capture_confirmed
    assert validation.no_apply_permission_confirmed
    assert validation.no_file_write_confirmed
    assert validation.no_external_send_confirmed
    assert validation.no_ui_runtime_confirmed
    assert validation.no_patch_apply_confirmed
    assert validation.no_repair_execution_confirmed
    assert validation.no_tests_confirmed
    assert validation.no_external_calls_confirmed
    assert validation.ready_for_execution is False
    decision = decide_repair_human_review_readiness(packet)
    report = build_repair_human_review_report(packet=packet, decision=decision, validation_report=validation)
    assert report.ready_for_future_loop_trial_input
    assert report.ready_for_future_cli_surface_input
    assert report.ready_for_future_v039_apply_contract_input
    assert report.ready_for_execution is False
    assert report.production_certified is False
    preview = build_repair_human_review_run_preview()
    assert preview.will_capture_approval is False
    assert preview.will_allow_apply is False
    guarantee = build_repair_human_review_no_approval_guarantee()
    assert guarantee.no_approval_capture
    assert guarantee.no_approval_grant
    assert guarantee.no_apply_permission
    assert guarantee.no_file_write
    assert guarantee.no_external_send
    assert guarantee.no_ui
    assert guarantee.no_patch_apply
    assert guarantee.no_repair
    assert guarantee.no_test
    assert guarantee.no_external_call
    readiness = build_v0386_readiness_report()
    assert readiness.ready_for_v0387_bounded_repair_proposal_loop_trial
    assert readiness.ready_for_v0388_cli_repair_proposal_surface
    assert readiness.ready_for_v039_human_approved_sandbox_repair_apply
    assert v0386_readiness_report_is_not_execution_ready(readiness)


def test_helpers_do_not_contain_forbidden_runtime_patterns():
    source = inspect.getsource(review_module)
    forbidden = [
        "Path.read_text",
        "Path.read_bytes",
        "open(",
        "write_text",
        "write_bytes",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "eval(",
        "exec(",
        "apply_patch(",
        "approval_granted=True",
        "human_approval_present=True",
        "approval_captured_now=True",
        "apply_allowed=True",
        "sandbox_apply_allowed=True",
    ]
    for pattern in forbidden:
        assert pattern not in source

