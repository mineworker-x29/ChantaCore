import inspect

import pytest

from chanta_core.agent_runtime import (
    PatchApprovalGateKind,
    PatchApprovalGateMetadata,
    PatchReviewArtifactSummary,
    PatchReviewChecklist,
    PatchReviewChecklistItem,
    PatchReviewChecklistItemKind,
    PatchReviewDecisionKind,
    PatchReviewDecisionRecord,
    PatchReviewFlagSet,
    PatchReviewInput,
    PatchReviewNoApplyGuarantee,
    PatchReviewOutcomeKind,
    PatchReviewPacket,
    PatchReviewPacketMode,
    PatchReviewPacketStatus,
    PatchReviewPolicy,
    PatchReviewReadinessLevel,
    PatchReviewReadinessReport,
    PatchReviewReport,
    PatchReviewRiskKind,
    PatchReviewRiskSummary,
    PatchReviewRunPreview,
    PatchReviewSourceKind,
    PatchReviewSourceRef,
    PatchReviewValidationFinding,
    PatchReviewValidationReport,
    PatchReviewerDecisionPlaceholder,
    PatchReviewerRoleKind,
    PatchRiskDecisionKind,
    V0356ReadinessReport,
    build_diff_proposal_envelope,
    build_structured_patch_proposal,
    build_unified_diff_proposal,
    build_patch_approval_gate_metadata,
    build_patch_proposal_risk_report_from_scan,
    build_patch_review_artifact_summary,
    build_patch_review_checklist,
    build_patch_review_checklist_from_risk_report,
    build_patch_review_checklist_item,
    build_patch_review_decision_record,
    build_patch_review_flags,
    build_patch_review_input,
    build_patch_review_input_from_risk_report,
    build_patch_review_no_apply_guarantee,
    build_patch_review_packet,
    build_patch_review_packet_from_risk_and_diff,
    build_patch_review_policy,
    build_patch_review_readiness_report,
    build_patch_review_report,
    build_patch_review_risk_summary,
    build_patch_review_run_preview,
    build_patch_review_source_ref,
    build_patch_review_validation_finding,
    build_patch_review_validation_report,
    build_patch_reviewer_decision_placeholder,
    build_v0356_readiness_report,
    default_patch_review_policy,
    patch_approval_gate_metadata_is_not_apply_permission,
    patch_review_decision_record_is_not_apply_permission,
    patch_review_flags_preserve_no_apply,
    patch_review_packet_is_not_apply_permission,
    patch_review_policy_blocks_apply,
    v0356_readiness_report_is_not_execution_ready,
    validate_patch_review_packet,
)
from chanta_core.agent_runtime import patch_review as review_module


def test_v0356_taxonomies_have_required_values() -> None:
    assert [item.value for item in PatchReviewPacketMode] == [
        "risk_report_only",
        "diff_and_risk_review",
        "full_patch_proposal_review",
        "metadata_only_review",
        "blocked",
        "needs_revision",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in PatchReviewSourceKind] == [
        "v0355_patch_proposal_risk_report",
        "v0355_patch_risk_scan_decision",
        "v0354_diff_proposal_envelope",
        "v0354_unified_diff_proposal",
        "v0354_structured_patch_proposal",
        "v0353_patch_plan",
        "v0352_context_snapshot",
        "v0351_patch_intent_scope_bundle",
        "v0350_reference_pattern_digest",
        "reviewer_metadata",
        "test_fixture",
        "unknown",
    ]
    assert [item.value for item in PatchReviewPacketStatus] == [
        "unknown",
        "draft",
        "review_packet_created",
        "checklist_created",
        "approval_gate_metadata_created",
        "pending_human_review",
        "approved_for_review",
        "rejected",
        "needs_revision",
        "blocked",
        "future_gated",
        "no_op",
    ]
    assert [item.value for item in PatchReviewReadinessLevel] == [
        "not_ready",
        "review_contract_ready",
        "review_packet_ready",
        "checklist_ready",
        "approval_gate_metadata_ready",
        "design_handoff_ready_for_v0357",
        "design_handoff_ready_for_v0358",
        "blocked",
        "future_track",
    ]
    assert [item.value for item in PatchReviewDecisionKind] == [
        "ready_for_human_review",
        "approved_for_review",
        "rejected",
        "needs_revision",
        "blocked_by_risk",
        "blocked_by_scope",
        "blocked_by_missing_artifact",
        "future_gate_required",
        "no_op",
        "unknown",
    ]
    assert [item.value for item in PatchReviewRiskKind] == [
        "missing_risk_report",
        "blocking_risk_present",
        "unresolved_review_item",
        "missing_diff_proposal",
        "missing_patch_plan",
        "missing_context_snapshot",
        "scope_violation_present",
        "safety_regression_present",
        "secret_or_credential_risk",
        "reference_execution_risk",
        "patch_apply_risk",
        "workspace_write_risk",
        "test_execution_risk",
        "shell_execution_risk",
        "dependency_install_risk",
        "authority_grant_risk",
        "unknown",
    ]
    assert PatchReviewChecklistItemKind.VERIFY_NO_WRITE_APPLY_RUNTIME.value == "verify_no_write_apply_runtime"
    assert PatchReviewOutcomeKind.APPROVED_FOR_REVIEW.value == "approved_for_review"
    assert PatchApprovalGateKind.NO_APPLY_GATE.value == "no_apply_gate"
    assert PatchReviewerRoleKind.HUMAN_REVIEWER.value == "human_reviewer"


def test_required_models_are_exported() -> None:
    for model in [
        PatchReviewFlagSet,
        PatchReviewSourceRef,
        PatchReviewPolicy,
        PatchReviewInput,
        PatchReviewChecklistItem,
        PatchReviewChecklist,
        PatchReviewArtifactSummary,
        PatchReviewRiskSummary,
        PatchApprovalGateMetadata,
        PatchReviewerDecisionPlaceholder,
        PatchReviewDecisionRecord,
        PatchReviewPacket,
        PatchReviewValidationFinding,
        PatchReviewValidationReport,
        PatchReviewReadinessReport,
        PatchReviewReport,
        PatchReviewRunPreview,
        PatchReviewNoApplyGuarantee,
        V0356ReadinessReport,
    ]:
        assert inspect.isclass(model)


def test_review_flags_allow_review_readiness_and_block_unsafe_runtime() -> None:
    flags = build_patch_review_flags()
    assert flags.patch_review_layer_constructed is True
    assert flags.human_review_packet_available is True
    assert flags.review_checklist_available is True
    assert flags.approval_gate_metadata_available is True
    assert flags.reviewer_decision_placeholder_available is True
    assert flags.ready_for_v0357_patch_proposal_ocel_trace_packet is True
    assert flags.ready_for_v0358_cli_patch_proposal_surface is True
    assert flags.ready_for_human_review_packet is True
    assert flags.ready_for_review_checklist is True
    assert flags.ready_for_approval_gate_metadata is True
    assert flags.ready_for_reviewer_decision_placeholder is True
    assert flags.ready_for_patch_review_packet_input is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_apply_patch is False
    assert flags.ready_for_git_apply is False
    assert flags.ready_for_test_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_reference_execution is False
    assert flags.ready_for_reference_import is False
    assert flags.production_certified is False
    assert patch_review_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_dependency_install",
        "ready_for_reference_execution",
        "ready_for_reference_import",
        "ready_for_provider_invocation",
        "ready_for_direct_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
    ],
)
def test_review_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_patch_review_flags(**{unsafe_flag: True})


def test_source_ref_policy_and_input_are_review_metadata_only() -> None:
    source_ref = build_patch_review_source_ref()
    assert source_ref.source_kind == PatchReviewSourceKind.V0355_PATCH_PROPOSAL_RISK_REPORT
    assert source_ref.source_id

    policy = default_patch_review_policy()
    assert policy.allow_approved_for_review is True
    assert policy.allow_approved_for_apply is False
    assert policy.allow_patch_application is False
    assert policy.allow_workspace_write is False
    assert policy.allow_code_edit is False
    assert policy.allow_test_execution is False
    assert policy.allow_shell is False
    assert policy.allow_dependency_install is False
    assert patch_review_policy_blocks_apply(policy)

    for field in [
        "allow_approved_for_apply",
        "allow_patch_application",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_test_execution",
        "allow_shell",
        "allow_dependency_install",
    ]:
        with pytest.raises(ValueError):
            build_patch_review_policy(**{field: True})

    review_input = build_patch_review_input()
    assert review_input.requested_mode == PatchReviewPacketMode.FULL_PATCH_PROPOSAL_REVIEW
    assert "patch_application" in review_input.prohibited_runtime_actions
    assert "workspace_write" in review_input.prohibited_runtime_actions
    assert "reference_execution" in review_input.prohibited_runtime_actions


def test_checklist_artifact_risk_and_gate_metadata_do_not_apply() -> None:
    item = build_patch_review_checklist_item()
    assert item.required is True
    assert item.requires_human_attention is True

    checklist = build_patch_review_checklist()
    assert checklist.ready_for_human_review is True
    assert checklist.ready_for_apply is False
    assert checklist.ready_for_execution is False
    with pytest.raises(ValueError):
        build_patch_review_checklist(ready_for_apply=True)

    long_preview = "x" * (review_module.DEFAULT_MAX_REVIEW_PREVIEW_CHARS + 50)
    artifact = build_patch_review_artifact_summary(bounded_preview=long_preview, redacted=True)
    assert artifact.redacted is True
    assert artifact.truncated is True
    assert len(artifact.bounded_preview) <= review_module.DEFAULT_MAX_REVIEW_PREVIEW_CHARS

    risk_summary = build_patch_review_risk_summary(acceptable_for_review=True)
    assert risk_summary.acceptable_for_review is True
    assert risk_summary.approved_for_apply is False
    with pytest.raises(ValueError):
        build_patch_review_risk_summary(approved_for_apply=True)

    gate = build_patch_approval_gate_metadata()
    assert gate.allows_review_approval_metadata is True
    assert gate.allows_apply_permission is False
    assert gate.allows_workspace_write is False
    assert gate.allows_code_edit is False
    assert gate.applies_patch is False
    assert patch_approval_gate_metadata_is_not_apply_permission(gate)
    for field in ["allows_apply_permission", "allows_workspace_write", "allows_code_edit", "applies_patch"]:
        with pytest.raises(ValueError):
            build_patch_approval_gate_metadata(**{field: True})


def test_reviewer_placeholders_decision_records_and_packets_do_not_grant_apply() -> None:
    placeholder = build_patch_reviewer_decision_placeholder()
    assert placeholder.filled is False
    assert placeholder.ready_for_apply is False
    assert placeholder.ready_for_execution is False
    with pytest.raises(ValueError):
        build_patch_reviewer_decision_placeholder(ready_for_apply=True)

    record = build_patch_review_decision_record()
    assert record.approved_for_review is True
    assert record.approved_for_apply is False
    assert record.ready_for_apply is False
    assert patch_review_decision_record_is_not_apply_permission(record)
    with pytest.raises(ValueError):
        build_patch_review_decision_record(approved_for_apply=True)
    with pytest.raises(ValueError):
        build_patch_review_decision_record(ready_for_apply=True)

    packet = build_patch_review_packet(approved_for_review=True)
    assert packet.ready_for_human_review is True
    assert packet.approved_for_review is True
    assert packet.approved_for_apply is False
    assert packet.ready_for_apply is False
    assert packet.ready_for_execution is False
    assert patch_review_packet_is_not_apply_permission(packet)
    with pytest.raises(ValueError):
        build_patch_review_packet(approved_for_apply=True)
    with pytest.raises(ValueError):
        build_patch_review_packet(ready_for_apply=True)
    with pytest.raises(ValueError):
        build_patch_review_packet(risk_summary=build_patch_review_risk_summary(blocking_risk_count=1), approved_for_review=True)


def test_reports_preview_guarantee_and_readiness_preserve_no_apply() -> None:
    validation = build_patch_review_validation_report(findings=[build_patch_review_validation_finding()])
    assert validation.valid is True
    assert validation.ready_for_patch_application is False
    assert validation.ready_for_workspace_write is False
    assert validation.ready_for_execution is False

    readiness = build_patch_review_readiness_report()
    assert readiness.ready_for_human_review_packet is True
    assert readiness.ready_for_review_checklist is True
    assert readiness.ready_for_approval_gate_metadata is True
    assert readiness.ready_for_reviewer_decision_placeholder is True
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_execution is False

    report = build_patch_review_report()
    assert report.review_packet_ready is True
    assert report.checklist_ready is True
    assert report.approval_gate_metadata_ready is True
    assert report.ready_for_patch_application is False
    assert report.ready_for_workspace_write is False
    assert report.ready_for_execution is False

    preview = build_patch_review_run_preview()
    assert preview.no_apply_permission_guarantee is True
    assert preview.no_patch_application_guarantee is True
    assert preview.no_git_apply_runtime_call_guarantee is True

    guarantee = build_patch_review_no_apply_guarantee()
    for field_name in guarantee.__dataclass_fields__:
        if field_name.startswith("no_"):
            assert getattr(guarantee, field_name) is True

    v0356 = build_v0356_readiness_report()
    assert v0356.ready_for_v0357_patch_proposal_ocel_trace_packet is True
    assert v0356.ready_for_v0358_cli_patch_proposal_surface is True
    assert v0356.ready_for_human_review_packet is True
    assert v0356.ready_for_review_checklist is True
    assert v0356.ready_for_approval_gate_metadata is True
    assert v0356.ready_for_reviewer_decision_placeholder is True
    assert v0356.ready_for_patch_review_packet_input is True
    assert v0356.ready_for_patch_application is False
    assert v0356.ready_for_workspace_write is False
    assert v0356.ready_for_code_edit is False
    assert v0356.ready_for_execution is False
    assert v0356.production_certified is False
    assert v0356_readiness_report_is_not_execution_ready(v0356)


def test_acceptable_risk_and_diff_metadata_produce_pending_human_review_packet() -> None:
    envelope = build_diff_proposal_envelope()
    risk_report = build_patch_proposal_risk_report_from_scan(envelope)
    review_input = build_patch_review_input_from_risk_report(risk_report)
    checklist = build_patch_review_checklist_from_risk_report(risk_report)
    packet = build_patch_review_packet_from_risk_and_diff(risk_report, envelope)

    assert risk_report.overall_decision == PatchRiskDecisionKind.ACCEPTABLE_FOR_REVIEW
    assert review_input.proposal_risk_report_id == risk_report.proposal_risk_report_id
    assert checklist.ready_for_human_review is True
    assert packet.status == PatchReviewPacketStatus.PENDING_HUMAN_REVIEW
    assert packet.mode == PatchReviewPacketMode.FULL_PATCH_PROPOSAL_REVIEW
    assert packet.ready_for_human_review is True
    assert packet.risk_summary.acceptable_for_review is True
    assert packet.approved_for_apply is False
    assert packet.ready_for_apply is False
    assert packet.ready_for_execution is False
    assert any(item.artifact_id == envelope.diff_envelope_id for item in packet.artifact_summaries)


def test_blocked_risk_report_produces_blocked_review_packet() -> None:
    unsafe = build_diff_proposal_envelope(
        unified_diff=build_unified_diff_proposal(diff_text="ready_for_patch_application=True\napply_patch"),
        structured_patch=build_structured_patch_proposal(file_proposals=[]),
    )
    risk_report = build_patch_proposal_risk_report_from_scan(unsafe)
    packet = build_patch_review_packet_from_risk_and_diff(risk_report, unsafe)

    assert risk_report.blocked is True
    assert packet.status == PatchReviewPacketStatus.BLOCKED
    assert packet.mode == PatchReviewPacketMode.BLOCKED
    assert packet.ready_for_human_review is False
    assert packet.approved_for_review is False
    assert packet.approved_for_apply is False
    assert PatchReviewRiskKind.BLOCKING_RISK_PRESENT in packet.risk_summary.risk_kinds


def test_missing_risk_or_diff_metadata_produces_blocked_or_needs_revision_packet() -> None:
    envelope = build_diff_proposal_envelope()
    missing_risk_packet = build_patch_review_packet_from_risk_and_diff(None, envelope)
    assert missing_risk_packet.status == PatchReviewPacketStatus.BLOCKED
    assert missing_risk_packet.ready_for_human_review is False
    assert "missing risk report" in missing_risk_packet.gaps

    risk_report = build_patch_proposal_risk_report_from_scan(envelope)
    missing_diff_packet = build_patch_review_packet_from_risk_and_diff(risk_report, None)
    assert missing_diff_packet.status == PatchReviewPacketStatus.NEEDS_REVISION
    assert missing_diff_packet.mode == PatchReviewPacketMode.NEEDS_REVISION
    assert missing_diff_packet.ready_for_human_review is False
    assert "missing diff proposal" in missing_diff_packet.gaps
    assert PatchReviewRiskKind.MISSING_DIFF_PROPOSAL in missing_diff_packet.risk_summary.risk_kinds


def test_validation_helper_flags_blocking_review_approval_conflict() -> None:
    blocked_summary = build_patch_review_risk_summary(blocking_risk_count=1, acceptable_for_review=False)
    packet = build_patch_review_packet(risk_summary=blocked_summary)
    validation = validate_patch_review_packet(packet)
    assert validation.valid is True
    assert validation.ready_for_patch_application is False
    assert validation.ready_for_execution is False


def test_helpers_do_not_use_forbidden_runtime_capabilities() -> None:
    source = inspect.getsource(review_module)
    forbidden_tokens = [
        "from pathlib",
        "Path(",
        ".read_text(",
        ".read_bytes(",
        ".write_text(",
        ".write_bytes(",
        "import subprocess\n",
        "subprocess.",
        "os.system(",
        "shell=True",
        " open(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests\n",
        "import httpx\n",
        "import urllib\n",
        "import aiohttp\n",
        "import socket\n",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
    ]
    for token in forbidden_tokens:
        assert token not in source


def test_helpers_cannot_set_unsafe_readiness_true() -> None:
    with pytest.raises(ValueError):
        build_v0356_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v0356_readiness_report(ready_for_patch_application=True)
    with pytest.raises(ValueError):
        build_patch_review_report(ready_for_workspace_write=True)
    with pytest.raises(ValueError):
        build_patch_review_validation_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_patch_review_readiness_report(ready_for_code_edit=True)
