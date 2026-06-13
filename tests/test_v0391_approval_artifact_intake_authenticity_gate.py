import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairApprovalArtifact,
    RepairApprovalArtifactDecision,
    RepairApprovalArtifactDecisionKind,
    RepairApprovalArtifactFlagSet,
    RepairApprovalArtifactInput,
    RepairApprovalArtifactKind,
    RepairApprovalArtifactMode,
    RepairApprovalArtifactNoApplyGuarantee,
    RepairApprovalArtifactPolicy,
    RepairApprovalArtifactReadinessLevel,
    RepairApprovalArtifactRiskKind,
    RepairApprovalArtifactRunPreview,
    RepairApprovalArtifactSourceKind,
    RepairApprovalArtifactSourceRef,
    RepairApprovalArtifactStatus,
    RepairApprovalArtifactValidationFinding,
    RepairApprovalArtifactValidationReport,
    RepairApprovalAuthenticityAssessment,
    RepairApprovalAuthenticitySignalKind,
    RepairApprovalConfidenceLevel,
    RepairApprovalDisposition,
    RepairApprovalExpirationAssessment,
    RepairApprovalExpirationStatus,
    RepairApprovalPatchBindingAssessment,
    RepairApprovalProcessStateGate,
    RepairApprovalRiskAssessment,
    RepairApprovalScopeBinding,
    RepairApprovalScopeKind,
    V0391ReadinessReport,
    assess_repair_approval_authenticity,
    assess_repair_approval_expiration,
    assess_repair_approval_patch_binding,
    assess_repair_approval_risk,
    bind_repair_approval_scope,
    build_repair_approval_artifact,
    build_repair_approval_artifact_decision,
    build_repair_approval_artifact_flags,
    build_repair_approval_artifact_input,
    build_repair_approval_artifact_no_apply_guarantee,
    build_repair_approval_artifact_policy,
    build_repair_approval_artifact_run_preview,
    build_repair_approval_artifact_source_ref,
    build_repair_approval_artifact_validation_finding,
    build_repair_approval_artifact_validation_report,
    build_repair_approval_authenticity_assessment,
    build_repair_approval_expiration_assessment,
    build_repair_approval_patch_binding_assessment,
    build_repair_approval_process_state_gate,
    build_repair_approval_risk_assessment,
    build_repair_approval_scope_binding,
    build_v0391_readiness_report,
    create_repair_approval_process_state_gate,
    decide_repair_approval_artifact,
    default_repair_approval_artifact_policy,
    normalize_repair_approval_artifact_input,
    repair_approval_artifact_flags_preserve_no_apply,
    repair_approval_artifact_is_not_apply_permission,
    repair_approval_decision_is_not_apply_permission,
    repair_approval_policy_blocks_apply_and_execution,
    repair_approval_process_state_gate_is_not_runtime_authority,
    v0391_readiness_report_is_not_execution_ready,
)
from chanta_core.agent_runtime import repair_approval_artifact as approval_module


def test_all_v0391_enum_values_exist():
    assert {item.value for item in RepairApprovalArtifactMode} == {
        "approval_artifact_intake",
        "approval_artifact_schema_validation",
        "approval_artifact_authenticity_gate",
        "approval_scope_validation",
        "approval_expiration_validation",
        "approval_reviewer_identity_metadata",
        "approval_patch_envelope_binding",
        "approval_safety_report_binding",
        "approval_review_packet_binding",
        "approval_process_state_transition_gate",
        "future_sandbox_workspace_isolation_input",
        "future_sandbox_apply_precondition_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert {item.value for item in RepairApprovalArtifactSourceKind} == {
        "v0390_repair_apply_boundary",
        "v0389_handoff_packet",
        "v0389_consolidation_report",
        "v0386_human_review_packet",
        "v0386_approval_request_contract",
        "v0385_safety_report",
        "v0384_proposed_patch_envelope",
        "v0383_scope_plan",
        "manual_human_approval_note",
        "operator_supplied_approval_artifact",
        "test_fixture",
        "unknown",
    }
    assert {item.value for item in RepairApprovalArtifactStatus} == {
        "unknown",
        "draft",
        "received",
        "schema_validated",
        "authenticity_assessed",
        "scope_validated",
        "expiration_validated",
        "bound_to_review_packet",
        "bound_to_safety_report",
        "bound_to_patch_envelope",
        "process_state_gate_created",
        "ready_for_future_workspace_isolation",
        "ready_for_future_sandbox_apply_precondition",
        "blocked",
        "rejected",
        "expired",
        "review_required",
        "no_op",
        "safe_failed",
    }
    assert {item.value for item in RepairApprovalArtifactReadinessLevel} == {
        "not_ready",
        "approval_intake_ready",
        "schema_validation_ready",
        "authenticity_gate_ready",
        "scope_validation_ready",
        "expiration_validation_ready",
        "review_packet_binding_ready",
        "safety_report_binding_ready",
        "patch_envelope_binding_ready",
        "process_state_transition_gate_ready",
        "future_workspace_isolation_input_ready",
        "future_sandbox_apply_precondition_input_ready",
        "design_handoff_ready_for_v0392",
        "design_handoff_ready_for_v0393",
        "blocked",
        "future_track",
    }
    assert {item.value for item in RepairApprovalArtifactDecisionKind} == {
        "allow_approval_artifact_intake",
        "allow_schema_validation",
        "allow_authenticity_assessment",
        "allow_scope_validation",
        "allow_expiration_validation",
        "allow_review_packet_binding",
        "allow_safety_report_binding",
        "allow_patch_envelope_binding",
        "allow_process_state_transition_gate",
        "allow_future_workspace_isolation_input",
        "allow_future_sandbox_apply_precondition_input",
        "choose_do_nothing",
        "choose_human_review_required",
        "deny",
        "block",
        "reject_expired",
        "reject_scope_mismatch",
        "reject_missing_binding",
        "reject_unsafe_patch",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in RepairApprovalArtifactKind} == {
        "explicit_human_approval_text",
        "signed_text_metadata",
        "reviewer_attestation_metadata",
        "review_packet_attached_approval",
        "approval_request_response_metadata",
        "manual_operator_note",
        "test_fixture_approval",
        "invalid_artifact",
        "unknown",
    }
    assert {item.value for item in RepairApprovalScopeKind} == {
        "proposed_patch_envelope_scope",
        "proposed_file_change_scope",
        "proposed_hunk_scope",
        "safety_validated_patch_scope",
        "human_review_packet_scope",
        "sandbox_apply_future_scope",
        "live_apply_forbidden_scope",
        "unknown",
    }
    assert {item.value for item in RepairApprovalExpirationStatus} == {
        "not_evaluated",
        "fresh",
        "near_expiry",
        "expired",
        "missing_timestamp",
        "missing_expiration_policy",
        "invalid_timestamp",
        "unknown",
    }
    assert {item.value for item in RepairApprovalDisposition} == {
        "accepted_for_future_gate",
        "accepted_with_warnings",
        "review_required",
        "blocked",
        "rejected",
        "expired",
        "scope_mismatch",
        "do_nothing_preferred",
        "no_op",
        "unknown",
    }
    assert {item.value for item in RepairApprovalConfidenceLevel} == {
        "high",
        "medium",
        "low",
        "inconclusive",
        "unknown",
    }
    assert "approval_grant_confusion_risk" in {item.value for item in RepairApprovalArtifactRiskKind}
    assert "reviewer_id_present" in {item.value for item in RepairApprovalAuthenticitySignalKind}


def test_flags_allow_approval_gate_readiness_only():
    flags = build_repair_approval_artifact_flags()
    assert isinstance(flags, RepairApprovalArtifactFlagSet)
    for name in approval_module.SAFE_FLAG_NAMES:
        assert getattr(flags, name) is True
    for name in approval_module.UNSAFE_FLAG_NAMES:
        assert getattr(flags, name) is False
    assert repair_approval_artifact_flags_preserve_no_apply(flags)


@pytest.mark.parametrize(
    "unsafe_field",
    [
        "ready_for_execution",
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
        build_repair_approval_artifact_flags(**{unsafe_field: True})


def test_policy_allows_gate_metadata_and_blocks_runtime():
    policy = default_repair_approval_artifact_policy()
    assert isinstance(policy, RepairApprovalArtifactPolicy)
    assert policy.allow_approval_artifact_intake is True
    assert policy.allow_schema_validation is True
    assert policy.allow_authenticity_assessment is True
    assert policy.allow_scope_validation is True
    assert policy.allow_expiration_validation is True
    assert policy.allow_reviewer_identity_metadata is True
    assert policy.allow_patch_envelope_binding is True
    assert policy.allow_safety_report_binding is True
    assert policy.allow_review_packet_binding is True
    assert policy.allow_process_state_transition_gate is True
    assert policy.allow_future_workspace_isolation_input is True
    assert policy.allow_future_sandbox_apply_precondition_input is True
    assert policy.reject_live_apply_scope is True
    assert repair_approval_policy_blocks_apply_and_execution(policy)
    for name in approval_module.UNSAFE_POLICY_ALLOW_NAMES:
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_repair_approval_artifact_policy(**{name: True})


def test_input_and_artifact_are_metadata_not_approval_grant():
    source = build_repair_approval_artifact_source_ref()
    assert isinstance(source, RepairApprovalArtifactSourceRef)
    input_metadata = build_repair_approval_artifact_input(source_refs=[source])
    assert isinstance(input_metadata, RepairApprovalArtifactInput)
    for action in approval_module.PROHIBITED_RUNTIME_ACTIONS:
        assert action in input_metadata.prohibited_runtime_actions

    artifact = normalize_repair_approval_artifact_input(input_metadata)
    assert isinstance(artifact, RepairApprovalArtifact)
    assert artifact.human_approval_artifact_present is True
    assert artifact.approval_artifact_received is True
    assert artifact.approval_granted is False
    assert artifact.approval_captured_now is False
    assert artifact.apply_permission_granted is False
    assert artifact.sandbox_apply_allowed_now is False
    assert artifact.live_apply_allowed_now is False
    assert artifact.repair_execution_allowed_now is False
    assert artifact.bounded is True
    assert artifact.redacted is True
    assert repair_approval_artifact_is_not_apply_permission(artifact)

    with pytest.raises(ValueError):
        build_repair_approval_artifact(approval_granted=True)
    with pytest.raises(ValueError):
        build_repair_approval_artifact(apply_permission_granted=True)


def test_scope_authenticity_expiration_and_binding_assessments():
    artifact = build_repair_approval_artifact()
    scope = build_repair_approval_scope_binding()
    assert isinstance(scope, RepairApprovalScopeBinding)
    assert scope.sandbox_only_scope is True
    assert scope.scope_valid is True
    with pytest.raises(ValueError):
        build_repair_approval_scope_binding(live_apply_scope_requested=True, scope_valid=True)
    with pytest.raises(ValueError):
        build_repair_approval_scope_binding(sandbox_only_scope=False, scope_valid=True)

    authenticity = assess_repair_approval_authenticity(artifact)
    assert isinstance(authenticity, RepairApprovalAuthenticityAssessment)
    assert authenticity.external_identity_verified is False
    assert authenticity.cryptographic_signature_verified is False
    assert authenticity.authenticity_sufficient_for_future_gate is True

    weak = assess_repair_approval_authenticity(build_repair_approval_artifact(reviewer_id=None, approval_phrase_present=False))
    assert weak.authenticity_confidence == RepairApprovalConfidenceLevel.LOW
    assert weak.authenticity_sufficient_for_future_gate is False
    assert weak.missing_signals

    expiration = assess_repair_approval_expiration(artifact)
    assert isinstance(expiration, RepairApprovalExpirationAssessment)
    assert expiration.fresh_for_future_gate is True
    assert expiration.expired is False
    with pytest.raises(ValueError):
        build_repair_approval_expiration_assessment(expired=True, fresh_for_future_gate=True)

    expired = assess_repair_approval_expiration(artifact, expired=True)
    assert expired.expired is True
    assert expired.fresh_for_future_gate is False

    patch_binding = assess_repair_approval_patch_binding(artifact)
    assert isinstance(patch_binding, RepairApprovalPatchBindingAssessment)
    assert patch_binding.binding_consistent is True
    with pytest.raises(ValueError):
        build_repair_approval_patch_binding_assessment(patch_binding_present=False, binding_consistent=True)


def test_process_state_gate_risk_and_decision_do_not_grant_runtime_authority():
    artifact = build_repair_approval_artifact()
    scope = bind_repair_approval_scope(artifact)
    authenticity = assess_repair_approval_authenticity(artifact)
    expiration = assess_repair_approval_expiration(artifact)
    patch_binding = assess_repair_approval_patch_binding(artifact)
    gate = create_repair_approval_process_state_gate(artifact, authenticity, expiration, patch_binding, scope)
    assert isinstance(gate, RepairApprovalProcessStateGate)
    assert gate.gate_satisfied is True
    assert gate.future_workspace_isolation_eligible is True
    assert gate.future_sandbox_apply_precondition_satisfied is True
    assert gate.process_state_authority_granted is False
    assert gate.runtime_authority_granted is False
    assert repair_approval_process_state_gate_is_not_runtime_authority(gate)

    with pytest.raises(ValueError):
        build_repair_approval_process_state_gate(runtime_authority_granted=True)

    risk = assess_repair_approval_risk(artifact, authenticity, scope, expiration, patch_binding)
    assert isinstance(risk, RepairApprovalRiskAssessment)
    assert risk.blocks_future_sandbox_apply_precondition is False

    high_risk = build_repair_approval_risk_assessment(
        risk_kinds=[RepairApprovalArtifactRiskKind.APPLY_PERMISSION_CONFUSION_RISK],
        blocks_future_sandbox_apply_precondition=True,
        requires_human_review=True,
    )
    assert high_risk.requires_human_review is True

    with pytest.raises(ValueError):
        build_repair_approval_risk_assessment(
            risk_kinds=[RepairApprovalArtifactRiskKind.APPROVAL_GRANT_CONFUSION_RISK],
            blocks_future_sandbox_apply_precondition=False,
            requires_human_review=False,
        )

    decision = decide_repair_approval_artifact(artifact, gate, risk)
    assert isinstance(decision, RepairApprovalArtifactDecision)
    assert decision.ready_for_future_workspace_isolation_input is True
    assert decision.ready_for_future_sandbox_apply_precondition_input is True
    assert decision.approval_artifact_valid_for_future_gate is True
    for name in approval_module.UNSAFE_DECISION_NAMES:
        assert getattr(decision, name) is False
    assert repair_approval_decision_is_not_apply_permission(decision)

    with pytest.raises(ValueError):
        build_repair_approval_artifact_decision(sandbox_apply_allowed_now=True)


def test_validation_preview_guarantee_and_readiness_report():
    finding = build_repair_approval_artifact_validation_finding()
    assert isinstance(finding, RepairApprovalArtifactValidationFinding)
    assert finding.blocked is True

    validation = build_repair_approval_artifact_validation_report()
    assert isinstance(validation, RepairApprovalArtifactValidationReport)
    assert validation.artifact_intake_confirmed is True
    assert validation.schema_validation_confirmed is True
    assert validation.authenticity_assessment_confirmed is True
    assert validation.scope_validation_confirmed is True
    assert validation.freshness_validation_confirmed is True
    assert validation.no_approval_grant_confirmed is True
    assert validation.no_apply_confirmed is True
    assert validation.no_sandbox_workspace_creation_confirmed is True
    assert validation.no_patch_materialization_confirmed is True
    assert validation.no_patch_application_confirmed is True
    assert validation.no_test_execution_confirmed is True
    assert validation.no_self_prompt_execution_confirmed is True
    assert validation.no_subagent_invocation_confirmed is True
    assert validation.no_model_provider_confirmed is True
    assert validation.no_external_agent_confirmed is True
    assert validation.no_dominion_confirmed is True
    assert validation.no_production_certification_confirmed is True

    preview = build_repair_approval_artifact_run_preview()
    assert isinstance(preview, RepairApprovalArtifactRunPreview)
    assert preview.preview_only is True
    assert preview.ready_for_execution is False

    guarantee = build_repair_approval_artifact_no_apply_guarantee()
    assert isinstance(guarantee, RepairApprovalArtifactNoApplyGuarantee)
    for name, value in guarantee.__dict__.items():
        if name.startswith("no_"):
            assert value is True

    report = build_v0391_readiness_report()
    assert isinstance(report, V0391ReadinessReport)
    assert report.ready_for_v0392_sandbox_workspace_isolation is True
    assert report.ready_for_v0393_human_approved_patch_materialization_sandbox_apply is True
    assert report.ready_for_approval_artifact_intake is True
    assert report.approval_artifact_received is True
    assert report.approval_artifact_valid_for_future_gate is True
    assert report.future_sandbox_apply_precondition_satisfied is True
    for name in approval_module.UNSAFE_REPORT_NAMES:
        assert getattr(report, name) is False
    assert v0391_readiness_report_is_not_execution_ready(report)

    with pytest.raises(ValueError):
        build_v0391_readiness_report(sandbox_apply_enabled=True)
    with pytest.raises(ValueError):
        build_v0391_readiness_report(self_prompt_generation_enabled=True)
    with pytest.raises(ValueError):
        build_v0391_readiness_report(ready_for_execution=True)


def test_helpers_are_pure_metadata_helpers_without_runtime_patterns():
    source = inspect.getsource(approval_module)
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
        "apply_permission_granted=True",
        "apply_allowed=True",
        "sandbox_apply_allowed=True",
        "production_certified=True",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

