import inspect

import pytest

from chanta_core.agent_runtime import (
    ApplyEligibilityDecisionKind,
    ApplyEligibilityStatus,
    HumanApprovalEvidenceKind,
    HumanApprovalSourceKind,
    HumanApprovalStatus,
    HumanApprovalValidationKind,
    PatchApplyCandidateDecisionKind,
    PatchApplyCandidateKind,
    PatchApplyCandidateReadinessLevel,
    PatchApplyCandidateRiskKind,
    PatchApplyCandidateSourceKind,
    PatchApplyCandidateStatus,
    apply_candidate_envelope_is_not_apply,
    apply_candidate_flags_preserve_no_apply,
    apply_candidate_policy_blocks_apply,
    apply_eligibility_decision_is_not_apply_permission,
    build_apply_candidate_envelope,
    build_apply_candidate_flags,
    build_apply_candidate_from_review_packet_metadata,
    build_apply_candidate_no_apply_guarantee,
    build_apply_candidate_policy,
    build_apply_candidate_report,
    build_apply_candidate_run_preview,
    build_apply_candidate_source_ref,
    build_apply_candidate_validation_finding,
    build_apply_candidate_validation_report,
    build_apply_eligibility_decision,
    build_human_approval_contract,
    build_human_approval_evidence,
    build_human_approval_validation_finding,
    build_human_approval_validation_report,
    build_v0361_readiness_report,
    decide_apply_candidate_eligibility,
    default_apply_candidate_policy,
    human_approval_contract_rejects_model_approval,
    human_approval_evidence_is_not_apply_permission,
    validate_apply_candidate_envelope,
    validate_human_approval_contract,
    v0361_readiness_report_is_not_execution_ready,
)
import chanta_core.agent_runtime.patch_apply_candidate as pac


def values(enum_cls):
    return {item.value for item in enum_cls}


def test_taxonomies_are_complete():
    assert values(PatchApplyCandidateKind) == {
        "from_review_packet",
        "from_diff_proposal",
        "from_structured_patch",
        "from_unified_diff",
        "from_risk_accepted_review",
        "from_manual_operator_request",
        "blocked_candidate",
        "no_op_candidate",
        "unknown",
    }
    assert values(PatchApplyCandidateSourceKind) == {
        "v0360_apply_sandbox_boundary",
        "v0359_v036_handoff_packet",
        "v0359_consolidation_report",
        "v0358_cli_patch_proposal_surface",
        "v0357_patch_proposal_trace_packet",
        "v0356_patch_review_packet",
        "v0356_approval_gate_metadata",
        "v0356_review_decision_record",
        "v0355_patch_proposal_risk_report",
        "v0354_diff_proposal_envelope",
        "v0354_structured_patch_proposal",
        "v0354_unified_diff_proposal",
        "v0353_patch_plan",
        "manual_operator_input",
        "test_fixture",
        "unknown",
    }
    assert values(PatchApplyCandidateStatus) == {
        "unknown",
        "draft",
        "candidate_created",
        "candidate_validated",
        "candidate_validated_with_gaps",
        "human_approval_attached",
        "human_approval_validated",
        "eligible_for_future_dry_run",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
    }
    assert values(PatchApplyCandidateReadinessLevel) == {
        "not_ready",
        "candidate_contract_ready",
        "human_approval_contract_ready",
        "approval_evidence_validated",
        "eligibility_decision_ready",
        "design_handoff_ready_for_v0362",
        "design_handoff_ready_for_v0363",
        "blocked",
        "future_track",
    }
    assert values(PatchApplyCandidateDecisionKind) == {
        "allow_candidate_metadata",
        "allow_human_approval_contract_metadata",
        "allow_operator_approval_evidence_metadata",
        "allow_future_dry_run_input",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert values(PatchApplyCandidateRiskKind) == {
        "missing_review_packet_risk",
        "missing_diff_proposal_risk",
        "missing_risk_report_risk",
        "blocked_risk_report_risk",
        "human_approval_missing_risk",
        "human_approval_ambiguous_risk",
        "model_generated_approval_risk",
        "review_metadata_as_apply_approval_risk",
        "forged_approval_risk",
        "stale_approval_risk",
        "scope_mismatch_risk",
        "diff_mismatch_risk",
        "patch_apply_risk",
        "live_workspace_write_risk",
        "sandbox_escape_risk",
        "shell_execution_risk",
        "test_execution_risk",
        "dependency_install_risk",
        "external_agent_execution_risk",
        "dominion_runtime_risk",
        "infinite_agent_loop_risk",
        "unknown",
    }
    assert values(HumanApprovalSourceKind) == {
        "operator_supplied_explicit_approval",
        "operator_supplied_review_record",
        "operator_supplied_cli_metadata",
        "human_review_packet_metadata",
        "model_generated_approval",
        "automated_placeholder",
        "inferred_approval",
        "missing_approval",
        "test_fixture",
        "unknown",
    }
    assert values(HumanApprovalEvidenceKind) == {
        "explicit_operator_confirmation",
        "reviewer_identity_ref",
        "approval_timestamp",
        "approved_candidate_ref",
        "approved_diff_ref",
        "approved_scope_ref",
        "approval_statement",
        "approval_nonce_or_ticket_ref",
        "review_packet_ref",
        "model_generated_statement",
        "automated_placeholder",
        "unknown",
    }
    assert values(HumanApprovalStatus) == {
        "unknown",
        "not_supplied",
        "supplied",
        "validated",
        "validated_with_warnings",
        "invalid",
        "rejected",
        "stale",
        "ambiguous",
        "future_gated",
    }
    assert values(HumanApprovalValidationKind) == {
        "operator_source_check",
        "model_generated_rejection_check",
        "review_metadata_not_apply_check",
        "candidate_binding_check",
        "diff_binding_check",
        "scope_binding_check",
        "timestamp_presence_check",
        "ambiguity_check",
        "stale_approval_check",
        "no_apply_permission_check",
        "unknown",
    }
    assert values(ApplyEligibilityStatus) == {
        "unknown",
        "not_eligible",
        "eligible_for_future_dry_run",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
    }
    assert values(ApplyEligibilityDecisionKind) == {
        "eligible_for_future_dry_run",
        "block_missing_human_approval",
        "block_invalid_human_approval",
        "block_blocked_risk_report",
        "block_missing_diff",
        "block_scope_mismatch",
        "require_review",
        "future_gate_required",
        "no_op",
        "unknown",
    }


def test_flags_allow_candidate_handoff_but_preserve_no_apply():
    flags = build_apply_candidate_flags()

    assert flags.apply_candidate_layer_constructed is True
    assert flags.apply_candidate_envelope_available is True
    assert flags.human_approval_contract_available is True
    assert flags.human_approval_evidence_validation_available is True
    assert flags.apply_eligibility_decision_available is True
    assert flags.ready_for_v0362_dry_run_patch_apply_simulation is True
    assert flags.ready_for_v0363_sandbox_workspace_overlay_policy is True
    assert flags.ready_for_future_dry_run_apply_input is True
    assert apply_candidate_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "flag_name",
    [
        "ready_for_execution",
        "ready_for_dry_run_apply_simulation",
        "ready_for_sandbox_patch_apply",
        "ready_for_sandbox_workspace_write",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "ready_for_independent_agent_runtime",
        "ready_for_multi_cycle_agentic_loop",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_readiness(flag_name):
    with pytest.raises(ValueError):
        build_apply_candidate_flags(**{flag_name: True})


def test_source_ref_is_metadata_only():
    source_ref = build_apply_candidate_source_ref()

    assert source_ref.source_kind == PatchApplyCandidateSourceKind.V0356_PATCH_REVIEW_PACKET
    assert source_ref.evidence_refs == ["v0.35.6", "v0.35.5", "v0.35.4"]


def test_operator_human_approval_evidence_can_validate_future_candidate_only():
    evidence = build_human_approval_evidence(
        evidence_value_preview=("operator approved; secret token hidden " * 20),
    )

    assert evidence.operator_supplied is True
    assert evidence.valid_for_apply_candidate is True
    assert human_approval_evidence_is_not_apply_permission(evidence)
    assert len(evidence.evidence_value_preview) <= 240
    assert "secret" not in evidence.evidence_value_preview
    assert "token" not in evidence.evidence_value_preview


@pytest.mark.parametrize(
    "source_kind,kwargs",
    [
        (HumanApprovalSourceKind.MODEL_GENERATED_APPROVAL, {"operator_supplied": False, "model_generated": True}),
        (HumanApprovalSourceKind.AUTOMATED_PLACEHOLDER, {"operator_supplied": False, "automated_placeholder": True}),
        (HumanApprovalSourceKind.HUMAN_REVIEW_PACKET_METADATA, {"operator_supplied": False}),
    ],
)
def test_invalid_approval_sources_cannot_validate_candidate(source_kind, kwargs):
    with pytest.raises(ValueError):
        build_human_approval_evidence(
            source_kind=source_kind,
            valid_for_apply_candidate=True,
            **kwargs,
        )


def test_approval_evidence_cannot_be_valid_for_patch_application():
    with pytest.raises(ValueError):
        build_human_approval_evidence(valid_for_patch_application=True)


def test_human_approval_contract_rejects_model_generated_and_review_metadata_approval():
    contract = build_human_approval_contract()

    assert contract.approval_valid_for_future_dry_run is True
    assert contract.approval_valid_for_patch_application is False
    assert human_approval_contract_rejects_model_approval(contract)

    with pytest.raises(ValueError):
        build_human_approval_contract(model_generated_approval_valid=True)
    with pytest.raises(ValueError):
        build_human_approval_contract(review_metadata_counts_as_apply_approval=True)
    with pytest.raises(ValueError):
        build_human_approval_contract(approval_valid_for_patch_application=True)


def test_human_approval_validation_blocks_missing_or_invalid_operator_evidence():
    invalid_evidence = build_human_approval_evidence(
        source_kind=HumanApprovalSourceKind.MODEL_GENERATED_APPROVAL,
        operator_supplied=False,
        model_generated=True,
        valid_for_apply_candidate=False,
    )
    contract = build_human_approval_contract(
        approval_evidence_items=[invalid_evidence],
        approval_valid_for_future_dry_run=False,
    )

    report = validate_human_approval_contract(contract)

    assert report.approval_status == HumanApprovalStatus.INVALID
    assert report.approval_valid_for_future_dry_run is False
    assert report.approval_valid_for_patch_application is False
    assert any(item.blocks_future_dry_run for item in report.findings)


def test_apply_candidate_policy_blocks_runtime_apply_surfaces():
    policy = default_apply_candidate_policy()

    assert policy.require_review_packet is True
    assert policy.require_risk_report is True
    assert policy.require_diff_proposal is True
    assert policy.require_operator_supplied_approval is True
    assert policy.reject_model_generated_approval is True
    assert policy.reject_review_metadata_as_apply_approval is True
    assert policy.reject_automated_placeholder_approval is True
    assert policy.allow_future_dry_run_input is True
    assert apply_candidate_policy_blocks_apply(policy)


@pytest.mark.parametrize(
    "allow_name",
    [
        "allow_dry_run_apply_simulation",
        "allow_sandbox_patch_apply",
        "allow_sandbox_workspace_write",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_shell",
        "allow_dependency_install",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
        "allow_infinite_agent_loop",
    ],
)
def test_apply_candidate_policy_rejects_unsafe_allow_flags(allow_name):
    with pytest.raises(ValueError):
        build_apply_candidate_policy(**{allow_name: True})


def test_apply_candidate_envelope_can_be_future_dry_run_input_only():
    envelope = build_apply_candidate_envelope()

    assert envelope.eligible_for_future_dry_run is True
    assert envelope.ready_for_dry_run_apply_simulation is False
    assert envelope.ready_for_sandbox_patch_apply is False
    assert envelope.ready_for_patch_application is False
    assert envelope.ready_for_workspace_write is False
    assert envelope.ready_for_code_edit is False
    assert envelope.ready_for_execution is False
    assert apply_candidate_envelope_is_not_apply(envelope)


def test_apply_candidate_envelope_rejects_apply_readiness_or_blocked_risk_eligibility():
    with pytest.raises(ValueError):
        build_apply_candidate_envelope(ready_for_patch_application=True)

    with pytest.raises(ValueError):
        build_apply_candidate_envelope(
            risk_kinds=[PatchApplyCandidateRiskKind.BLOCKED_RISK_REPORT_RISK],
        )

    blocked = build_apply_candidate_envelope(
        eligible_for_future_dry_run=False,
        status=PatchApplyCandidateStatus.BLOCKED,
        risk_kinds=[PatchApplyCandidateRiskKind.BLOCKED_RISK_REPORT_RISK],
    )
    assert blocked.eligible_for_future_dry_run is False
    assert apply_candidate_envelope_is_not_apply(blocked)


def test_validation_reports_do_not_certify_patch_application():
    finding = build_apply_candidate_validation_finding(
        risk_kind=PatchApplyCandidateRiskKind.MISSING_DIFF_PROPOSAL_RISK,
        decision_kind=PatchApplyCandidateDecisionKind.REQUIRE_REVIEW,
        blocks_future_dry_run=True,
    )
    report = build_apply_candidate_validation_report(
        findings=[finding],
        status=PatchApplyCandidateStatus.CANDIDATE_VALIDATED_WITH_GAPS,
    )

    assert report.certifies_patch_application is False
    with pytest.raises(ValueError):
        build_apply_candidate_validation_report(certifies_patch_application=True)

    approval_finding = build_human_approval_validation_finding(
        validation_kind=HumanApprovalValidationKind.REVIEW_METADATA_NOT_APPLY_CHECK,
        approval_status=HumanApprovalStatus.INVALID,
        blocks_future_dry_run=True,
    )
    approval_report = build_human_approval_validation_report(
        findings=[approval_finding],
        approval_status=HumanApprovalStatus.INVALID,
        approval_valid_for_future_dry_run=False,
    )
    assert approval_report.approval_valid_for_patch_application is False


def test_eligibility_decision_is_never_apply_permission():
    decision = build_apply_eligibility_decision()

    assert decision.eligible_for_future_dry_run is True
    assert decision.ready_for_apply is False
    assert decision.ready_for_dry_run_apply_simulation is False
    assert decision.ready_for_patch_application is False
    assert decision.ready_for_execution is False
    assert apply_eligibility_decision_is_not_apply_permission(decision)

    with pytest.raises(ValueError):
        build_apply_eligibility_decision(ready_for_apply=True)


def test_review_risk_diff_metadata_can_create_candidate_without_reading_or_applying():
    envelope = build_apply_candidate_from_review_packet_metadata(
        review_packet_id="review:v0356",
        risk_report_id="risk:v0355",
        diff_envelope_id="diff:v0354",
    )
    decision = decide_apply_candidate_eligibility(envelope)

    assert envelope.review_packet_id == "review:v0356"
    assert envelope.risk_report_id == "risk:v0355"
    assert envelope.diff_envelope_id == "diff:v0354"
    assert envelope.eligible_for_future_dry_run is True
    assert decision.decision_kind == ApplyEligibilityDecisionKind.ELIGIBLE_FOR_FUTURE_DRY_RUN
    assert apply_eligibility_decision_is_not_apply_permission(decision)


def test_blocked_risk_report_blocks_candidate_eligibility():
    envelope = build_apply_candidate_from_review_packet_metadata(blocked_risk_report=True)
    decision = decide_apply_candidate_eligibility(envelope)

    assert envelope.eligible_for_future_dry_run is False
    assert decision.eligibility_status == ApplyEligibilityStatus.BLOCKED
    assert decision.decision_kind == ApplyEligibilityDecisionKind.BLOCK_BLOCKED_RISK_REPORT
    assert decision.ready_for_apply is False


def test_missing_approval_or_missing_diff_blocks_eligibility():
    invalid_evidence = build_human_approval_evidence(
        source_kind=HumanApprovalSourceKind.MISSING_APPROVAL,
        operator_supplied=False,
        valid_for_apply_candidate=False,
    )
    invalid_contract = build_human_approval_contract(
        approval_evidence_items=[invalid_evidence],
        approval_valid_for_future_dry_run=False,
    )
    missing_approval = build_apply_candidate_envelope(
        approval_contract=invalid_contract,
        eligible_for_future_dry_run=False,
    )

    approval_decision = decide_apply_candidate_eligibility(missing_approval)
    assert approval_decision.decision_kind == ApplyEligibilityDecisionKind.BLOCK_INVALID_HUMAN_APPROVAL

    missing_diff = build_apply_candidate_envelope(
        diff_envelope_id=None,
        eligible_for_future_dry_run=False,
    )
    diff_decision = decide_apply_candidate_eligibility(missing_diff)
    assert diff_decision.decision_kind == ApplyEligibilityDecisionKind.BLOCK_MISSING_DIFF


def test_candidate_reports_previews_guarantee_and_readiness_preserve_no_apply():
    envelope = build_apply_candidate_envelope()
    validation_report = validate_apply_candidate_envelope(envelope)
    approval_report = validate_human_approval_contract(envelope.approval_contract)
    decision = decide_apply_candidate_eligibility(envelope)
    report = build_apply_candidate_report(
        validation_report=validation_report,
        human_approval_report=approval_report,
        eligibility_decision=decision,
    )
    preview = build_apply_candidate_run_preview()
    guarantee = build_apply_candidate_no_apply_guarantee()
    readiness = build_v0361_readiness_report()

    assert report.ready_for_execution is False
    assert report.ready_for_patch_application is False
    assert preview.ready_for_future_dry_run_input is True
    assert preview.ready_for_execution is False
    assert preview.ready_for_patch_application is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert v0361_readiness_report_is_not_execution_ready(readiness)
    assert readiness.ready_for_v0362_dry_run_patch_apply_simulation is True
    assert readiness.ready_for_v0363_sandbox_workspace_overlay_policy is True

    with pytest.raises(ValueError):
        build_apply_candidate_no_apply_guarantee(no_patch_application=False)
    with pytest.raises(ValueError):
        build_v0361_readiness_report(ready_for_execution=True)


def test_module_exports_import_cleanly_from_agent_runtime():
    from chanta_core.agent_runtime import (  # noqa: PLC0415
        ApplyCandidateEnvelope,
        HumanApprovalContract,
        V0361ReadinessReport,
    )

    assert ApplyCandidateEnvelope is not None
    assert HumanApprovalContract is not None
    assert V0361ReadinessReport is not None


def test_patch_apply_candidate_helpers_do_not_contain_runtime_execution_patterns():
    source = inspect.getsource(pac)

    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.write_text",
        "Path.write_bytes",
        ".write_text(",
        ".write_bytes(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

