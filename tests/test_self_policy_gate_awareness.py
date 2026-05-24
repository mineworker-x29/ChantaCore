import subprocess
import sys
from dataclasses import replace

from chanta_core.deep_self_introspection import (
    ExecutionEnvelopePolicyDescriptor,
    ExecutionGateDescriptor,
    MaterializationGateDescriptor,
    PermissionBoundaryDescriptor,
    PolicyGateTruthCheckService,
    PromotionGateDescriptor,
    ReviewPolicyDescriptor,
    SelfCapabilityRegistryAwarenessService,
    SelfPolicyGateAwarenessService,
)


def test_policy_gate_map_snapshot_builds() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    assert snapshot.snapshot_id
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.rules
    assert snapshot.review_policy.policy_id
    assert snapshot.permission_boundary.boundary_id
    assert snapshot.execution_gates
    assert snapshot.envelope_policy.policy_id
    assert snapshot.promotion_gate.gate_id
    assert snapshot.materialization_gate.gate_id
    assert snapshot.limitations


def test_review_policy_keeps_review_separate_from_execution() -> None:
    policy = SelfPolicyGateAwarenessService().view_policy_gate_map().review_policy
    assert policy.proposal_required is True
    assert policy.review_required is True
    assert "approved_for_explicit_invocation" in policy.allowed_review_decisions
    assert "rejected" in policy.allowed_review_decisions
    assert "revise_proposal" in policy.allowed_review_decisions
    assert "no_action" in policy.allowed_review_decisions
    assert "needs_more_input" in policy.allowed_review_decisions
    assert policy.approval_implies_execution is False
    assert policy.no_action_is_valid is True
    assert policy.needs_more_input_is_valid is True
    assert policy.reviewer_note_supported is True


def test_permission_boundary_denies_escalation_and_external_permissions() -> None:
    boundary = SelfPolicyGateAwarenessService().view_policy_gate_map().permission_boundary
    assert boundary.deny_by_default is True
    assert boundary.permission_grant_creation_allowed is False
    assert boundary.permission_escalation_allowed is False
    assert boundary.shell_permission_allowed is False
    assert boundary.network_permission_allowed is False
    assert boundary.mcp_permission_allowed is False
    assert boundary.plugin_permission_allowed is False
    assert boundary.external_harness_permission_allowed is False
    assert boundary.boundary_status == "ok"


def test_execution_gates_include_read_only_and_hard_blocks() -> None:
    gates = {gate.gate_type: gate for gate in SelfPolicyGateAwarenessService().view_policy_gate_map().execution_gates}
    assert gates["read_only"].enabled is True
    assert gates["read_only"].requires_envelope is True
    for gate_type in ["write", "shell", "network", "mcp", "plugin", "external_harness"]:
        assert gates[gate_type].enabled is False
        assert gates[gate_type].hard_blocked is True
        assert gates[gate_type].requires_envelope is True
        assert gates[gate_type].gate_status == "ok"


def test_envelope_policy_requires_redacted_envelopes() -> None:
    policy = SelfPolicyGateAwarenessService().view_policy_gate_map().envelope_policy
    assert policy.envelope_required is True
    assert policy.envelope_required_for_read_only is True
    assert policy.envelope_required_for_blocked_attempts is True
    assert policy.audit_visible is True
    assert policy.workbench_visible is True
    assert policy.ocel_visible is True
    assert policy.private_payload_redaction_required is True
    assert policy.raw_private_body_allowed is False
    assert policy.policy_status == "ok"


def test_promotion_and_materialization_gates_are_disabled() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    promotion = snapshot.promotion_gate
    assert promotion.candidate_promotion_enabled is False
    assert promotion.auto_promotion_allowed is False
    assert promotion.canonical_promotion_enabled is False
    assert promotion.memory_promotion_allowed is False
    assert promotion.persona_promotion_allowed is False
    assert promotion.overlay_promotion_allowed is False
    materialization = snapshot.materialization_gate
    assert materialization.materialization_enabled is False
    assert materialization.plan_materialization_allowed is False
    assert materialization.todo_materialization_allowed is False
    assert materialization.task_creation_allowed is False
    assert materialization.scheduler_registration_allowed is False
    assert materialization.file_write_materialization_allowed is False


def test_truth_check_passes_when_safe() -> None:
    report = SelfPolicyGateAwarenessService().truth_check()
    assert report.status == "passed"
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.gate_truth_summary["proposal_created != execution_allowed"] is True
    assert report.gate_truth_summary["review_approved != execution_performed"] is True
    assert report.gate_truth_summary["no_action is valid"] is True


def test_truth_check_fails_if_review_policy_allows_execution_or_removes_terminal_outcomes() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    bad_review = replace(
        snapshot.review_policy,
        approval_implies_execution=True,
        no_action_is_valid=False,
        needs_more_input_is_valid=False,
    )
    report = PolicyGateTruthCheckService().check_truth(replace(snapshot, review_policy=bad_review))
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "approval_implies_execution_violation" in finding_types
    assert "no_action_policy_missing" in finding_types
    assert "needs_more_input_policy_missing" in finding_types


def test_truth_check_fails_if_permission_boundary_allows_grants_or_escalation() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    bad_boundary = replace(
        snapshot.permission_boundary,
        permission_grant_creation_allowed=True,
        permission_escalation_allowed=True,
        shell_permission_allowed=True,
    )
    report = PolicyGateTruthCheckService().check_truth(replace(snapshot, permission_boundary=bad_boundary))
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "permission_grant_allowed_violation" in finding_types
    assert "permission_escalation_allowed_violation" in finding_types


def test_truth_check_fails_if_envelope_policy_is_missing_or_raw_private_payload_allowed() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    bad_envelope = replace(
        snapshot.envelope_policy,
        envelope_required=False,
        envelope_required_for_blocked_attempts=False,
        raw_private_body_allowed=True,
    )
    report = PolicyGateTruthCheckService().check_truth(replace(snapshot, envelope_policy=bad_envelope))
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "missing_execution_envelope_requirement" in finding_types
    assert "missing_blocked_attempt_envelope" in finding_types
    assert "raw_private_payload_allowed_violation" in finding_types


def test_truth_check_fails_if_dangerous_gate_is_enabled() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    gates = [replace(gate, enabled=True) if gate.gate_type in {"write", "shell", "network"} else gate for gate in snapshot.execution_gates]
    report = PolicyGateTruthCheckService().check_truth(replace(snapshot, execution_gates=gates))
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "write_gate_enabled_violation" in finding_types
    assert "shell_gate_enabled_violation" in finding_types
    assert "network_gate_enabled_violation" in finding_types


def test_truth_check_fails_if_promotion_or_materialization_enabled() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    report = PolicyGateTruthCheckService().check_truth(
        replace(
            snapshot,
            promotion_gate=replace(snapshot.promotion_gate, candidate_promotion_enabled=True),
            materialization_gate=replace(snapshot.materialization_gate, materialization_enabled=True),
        )
    )
    finding_types = {item.finding_type for item in report.findings}
    assert report.status == "failed"
    assert "promotion_gate_enabled_violation" in finding_types
    assert "materialization_gate_enabled_violation" in finding_types


def test_optional_policy_claim_exceeding_gate_truth_is_detected() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    report = PolicyGateTruthCheckService().check_truth(
        snapshot,
        optional_claims=[{"claim_type": "permission_grant_allowed", "claimed_allowed": True}],
    )
    assert report.status == "failed"
    assert report.unsafe_policy_claims_detected == 1
    assert any(item.finding_type == "policy_claim_exceeds_gate_truth" for item in report.findings)


def test_policy_skills_are_visible_as_read_only_and_remaining_seed_skills_stay_contract_only() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    records = {record.skill_id: record for record in snapshot.records}
    assert records["skill:deep_self_policy_gate_map"].status == "implemented"
    assert records["skill:deep_self_policy_gate_truth_check"].status == "implemented"
    assert records["skill:deep_self_capability_registry_view"].status == "implemented"
    assert records["skill:deep_self_capability_truth_check"].status == "implemented"
    assert records["skill:deep_self_runtime_boundary_view"].status == "implemented"
    assert records["skill:deep_self_runtime_boundary_truth_check"].status == "implemented"
    assert records["skill:deep_self_trace_integrity_check"].status == "implemented"
    assert records["skill:deep_self_context_projection_view"].status == "implemented"
    assert records["skill:deep_self_context_projection_gap_report"].status == "implemented"
    assert records["skill:deep_self_candidate_memory_boundary_report"].status == "implemented"
    assert records["skill:deep_self_promotion_boundary_check"].status == "implemented"
    assert records["skill:deep_self_claim_consistency_check"].status == "implemented"
    assert records["skill:deep_self_policy_gate_map"].read_only is True
    assert records["skill:deep_self_policy_gate_truth_check"].read_only is True


def test_no_review_decision_permission_grant_skill_invocation_or_envelope_execution_occurs() -> None:
    service = SelfPolicyGateAwarenessService()
    first = service.view_policy_gate_map().to_dict()
    second = service.view_policy_gate_map().to_dict()
    assert first["review_policy"] == second["review_policy"]
    assert first["permission_boundary"] == second["permission_boundary"]
    assert first["promotion_gate"] == second["promotion_gate"]
    assert first["materialization_gate"] == second["materialization_gate"]
    assert first["read_only"] is True
    assert first["mutation_performed"] is False


def test_pig_and_ocpx_projection_build() -> None:
    service = SelfPolicyGateAwarenessService()
    pig = service.build_pig_report()
    assert pig["version"] == "v0.21.3"
    assert pig["subject"] == "policy_gate"
    assert "proposal_created != execution_allowed" in pig["principles"]
    assert "review_approved != execution_performed" in pig["principles"]
    assert "no_action is valid" in pig["principles"]
    assert pig["permission_grant_creation_allowed"] is False
    assert "write" in pig["hard_blocked_gates"]
    assert "shell" in pig["hard_blocked_gates"]
    assert pig["promotion_enabled"] is False
    assert pig["materialization_enabled"] is False
    ocpx = service.build_ocpx_projection()
    assert ocpx["state"] == "self_policy_gate_awareness"
    assert "SelfCapabilityTruthState" in ocpx["source_read_models"]
    assert "SelfRuntimeBoundaryState" in ocpx["source_read_models"]
    assert "SelfPolicyGateState" in ocpx["target_read_models"]
    assert "SelfReviewPolicyState" in ocpx["target_read_models"]
    assert "SelfPermissionBoundaryState" in ocpx["target_read_models"]
    assert "SelfExecutionGateState" in ocpx["target_read_models"]
    assert "SelfEnvelopePolicyState" in ocpx["target_read_models"]
    assert "SelfPromotionGateState" in ocpx["target_read_models"]
    assert "SelfMaterializationGateState" in ocpx["target_read_models"]


def test_cli_policy_views_work() -> None:
    commands = [
        ["deep-self", "policy", "gate-map"],
        ["deep-self", "policy", "truth-check"],
        ["deep-self", "policy", "review"],
        ["deep-self", "policy", "permission-boundary"],
        ["deep-self", "policy", "execution-gates"],
        ["deep-self", "policy", "envelope"],
        ["deep-self", "policy", "promotion"],
        ["deep-self", "policy", "materialization"],
    ]
    for command in commands:
        result = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", *command],
            check=True,
            capture_output=True,
            text=True,
        )
        assert "Self-Policy/Gate Awareness" in result.stdout
        assert "proposal_created != execution_allowed=True" in result.stdout
        assert "review_approved != execution_performed=True" in result.stdout
        assert "no_action_is_valid=True" in result.stdout
        assert "needs_more_input_is_valid=True" in result.stdout
        assert "permission_grant_creation_allowed=False" in result.stdout
        assert "policy_mutated=False" in result.stdout
        assert "review_decision_created=False" in result.stdout
        assert "permission_grant_created=False" in result.stdout
        assert "raw_file_content_printed=False" in result.stdout
        assert "private_full_paths_printed=False" in result.stdout
        assert "raw_secrets_printed=False" in result.stdout


def test_descriptor_types_exported() -> None:
    assert ExecutionEnvelopePolicyDescriptor
    assert ExecutionGateDescriptor
    assert MaterializationGateDescriptor
    assert PermissionBoundaryDescriptor
    assert PromotionGateDescriptor
    assert ReviewPolicyDescriptor
