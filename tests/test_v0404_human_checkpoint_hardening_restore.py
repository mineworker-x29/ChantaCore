from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_checkpoint_hardening import (
    FORBIDDEN_ACTION_CLASSES,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_RESTORE_SECTION_IDS,
    CheckpointDecisionKind,
    CheckpointScopeKind,
    CheckpointApprovalValidationInput,
    create_checkpoint_approval_authority_boundary,
    create_checkpoint_approval_scope,
    create_checkpoint_artifact_binding,
    create_checkpoint_expiry_record,
    create_checkpoint_freshness_policy,
    create_checkpoint_hardening_audit_record,
    create_checkpoint_hardening_readiness_report,
    create_checkpoint_hardening_safety_report,
    create_checkpoint_revocation_record,
    create_scope_bound_checkpoint_decision,
    create_v0404_restore_context_snapshot,
    create_v0404_restore_document_manifest,
    create_v0404_restore_packet,
    create_v0405_provider_prompt_boundary_handoff,
    create_v041_smoke_run_acceleration_checkpoint_signal,
    evaluate_checkpoint_freshness,
    restore_packet_is_suitable_for_new_session_handoff,
    scope_bound_decision_preserves_no_authority,
    validate_scope_bound_checkpoint_decision,
    v041_checkpoint_signal_is_not_runtime_start,
)


EXPECTED_ARTIFACTS = ("iteration-state-v0404", "safety-report-v0404", "negative-gate-v0404")


def _validation_input(**overrides):
    decision = overrides.pop("decision", create_scope_bound_checkpoint_decision())
    freshness = overrides.pop("freshness_evaluation", evaluate_checkpoint_freshness())
    defaults = {
        "validation_id": "validation-v0404-test",
        "decision": decision,
        "freshness_evaluation": freshness,
        "expected_loop_id": "loop-v0404",
        "expected_iteration_index": 1,
        "expected_checkpoint_request_id": "checkpoint-request-v0404",
        "expected_artifact_refs": EXPECTED_ARTIFACTS,
        "negative_gate_report_ref": "negative-gate-v0404",
    }
    defaults.update(overrides)
    return CheckpointApprovalValidationInput(**defaults)


def test_v0404_scope_kind_declares_required_scopes() -> None:
    assert {item.value for item in CheckpointScopeKind} == {
        "loop",
        "mission",
        "iteration",
        "checkpoint_request",
        "checkpoint_decision",
        "sandbox_rehearsal",
        "manual_two_iteration_rehearsal",
        "negative_gate_regression",
        "artifact_set",
        "restore_packet",
    }


def test_v0404_decision_kind_declares_required_decisions() -> None:
    assert {item.value for item in CheckpointDecisionKind} == {
        "approve_scoped_rehearsal",
        "request_more_evidence",
        "stop",
        "do_nothing",
        "reject",
        "revoke",
        "expire",
    }


def test_v0404_approval_scope_rejects_broad_future_authority() -> None:
    with pytest.raises(ValueError):
        create_checkpoint_approval_scope(broad_future_authority_allowed=True)


@pytest.mark.parametrize("action_class", FORBIDDEN_ACTION_CLASSES)
def test_v0404_approval_scope_rejects_forbidden_action_classes(action_class: str) -> None:
    with pytest.raises(ValueError):
        create_checkpoint_approval_scope(approved_action_class=action_class)


def test_v0404_artifact_binding_is_required() -> None:
    binding = create_checkpoint_artifact_binding()

    assert binding.artifact_binding_required is True
    with pytest.raises(ValueError):
        create_checkpoint_artifact_binding(artifact_binding_required=False)
    with pytest.raises(ValueError):
        create_checkpoint_artifact_binding(bound_artifact_refs=())


def test_v0404_freshness_policy_marks_iteration_mismatch_stale() -> None:
    evaluation = evaluate_checkpoint_freshness(current_iteration_index=2)

    assert evaluation.fresh is False
    assert evaluation.stale_reason == "iteration_mismatch"


def test_v0404_freshness_policy_marks_artifact_mismatch_stale() -> None:
    evaluation = evaluate_checkpoint_freshness(current_artifact_refs=("changed-artifact",))

    assert evaluation.fresh is False
    assert evaluation.stale_reason == "artifact_mismatch"


def test_v0404_freshness_policy_marks_revoked_decision_stale() -> None:
    evaluation = evaluate_checkpoint_freshness(revoked=True)

    assert evaluation.fresh is False
    assert evaluation.stale_reason == "revoked"


def test_v0404_freshness_policy_marks_policy_version_change_stale() -> None:
    evaluation = evaluate_checkpoint_freshness(policy_version_changed=True)

    assert evaluation.fresh is False
    assert evaluation.stale_reason == "policy_version_changed"


def test_v0404_scope_bound_decision_never_grants_runtime_authority() -> None:
    decision = create_scope_bound_checkpoint_decision()

    assert scope_bound_decision_preserves_no_authority(decision)
    with pytest.raises(ValueError):
        create_scope_bound_checkpoint_decision(approval_grants_runtime_authority=True)


def test_v0404_validation_rejects_missing_artifact_binding() -> None:
    binding = create_checkpoint_artifact_binding(bound_artifact_refs=("iteration-state-v0404",))
    decision = create_scope_bound_checkpoint_decision(artifact_binding=binding)
    result = validate_scope_bound_checkpoint_decision(_validation_input(decision=decision))

    assert result.valid is False
    assert result.artifact_binding_valid is False


def test_v0404_validation_rejects_stale_checkpoint() -> None:
    result = validate_scope_bound_checkpoint_decision(
        _validation_input(freshness_evaluation=evaluate_checkpoint_freshness(revoked=True))
    )

    assert result.valid is False
    assert result.freshness_valid is False


def test_v0404_validation_rejects_scope_mismatch() -> None:
    result = validate_scope_bound_checkpoint_decision(_validation_input(expected_loop_id="other-loop"))

    assert result.valid is False
    assert result.scope_valid is False


def test_v0404_validation_rejects_negative_gate_incompatible_decision() -> None:
    result = validate_scope_bound_checkpoint_decision(_validation_input(negative_gate_report_ref=None))

    assert result.valid is False
    assert result.negative_gate_compatible is False


def test_v0404_validation_allows_only_valid_scoped_manual_rehearsal_candidate() -> None:
    result = validate_scope_bound_checkpoint_decision(_validation_input())

    assert result.valid is True
    assert result.safe_to_construct_second_iteration_candidate is True
    assert result.safe_to_execute_runtime_action is False


def test_v0404_validation_never_allows_runtime_execution() -> None:
    result = validate_scope_bound_checkpoint_decision(_validation_input())

    assert result.runtime_authority_granted is False
    assert result.safe_to_execute_runtime_action is False


def test_v0404_authority_boundary_blocks_live_model_prompt_subagent_autonomy_dominion_and_certification() -> None:
    boundary = create_checkpoint_approval_authority_boundary()

    assert boundary.allows_manual_rehearsal_candidate is True
    assert boundary.allows_live_workspace_mutation is False
    assert boundary.allows_model_invocation is False
    assert boundary.allows_prompt_submission is False
    assert boundary.allows_subagent_invocation is False
    assert boundary.allows_autonomous_continuation is False
    assert boundary.allows_dominion_runtime is False
    assert boundary.allows_production_certification is False


def test_v0404_revocation_record_invalidates_checkpoint() -> None:
    revocation = create_checkpoint_revocation_record()
    evaluation = evaluate_checkpoint_freshness(revoked=revocation.revoked)

    assert revocation.revoked is True
    assert evaluation.fresh is False


def test_v0404_expiry_record_invalidates_checkpoint() -> None:
    expiry = create_checkpoint_expiry_record()
    evaluation = evaluate_checkpoint_freshness(policy_version_changed=expiry.expired)

    assert expiry.expired is True
    assert evaluation.fresh is False


def test_v0404_audit_record_checks_scope_binding_freshness_and_no_authority() -> None:
    audit = create_checkpoint_hardening_audit_record()

    assert audit.checked_scope_bound_approval is True
    assert audit.checked_artifact_binding is True
    assert audit.checked_freshness_policy is True
    assert audit.checked_runtime_authority_not_granted is True


def test_v0404_safety_report_keeps_runtime_and_standalone_false() -> None:
    report = create_checkpoint_hardening_safety_report()

    assert report.safe_for_v0404_checkpoint_hardening is True
    assert report.safe_for_runtime_execution is False
    assert report.safe_for_standalone_default_personal_runtime is False
    assert report.production_certified is False


def test_v0404_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_checkpoint_hardening_readiness_report()

    assert report.human_checkpoint_hardening_defined is True
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False
    with pytest.raises(ValueError):
        create_checkpoint_hardening_readiness_report(ready_for_execution=True)


def test_v0404_restore_context_snapshot_lists_version_chain() -> None:
    snapshot = create_v0404_restore_context_snapshot()

    assert len(snapshot.baseline_versions) == 5
    assert any("v0.40.4" in version for version in snapshot.baseline_versions)
    assert "standalone_default_personal_runtime" in snapshot.closed_capabilities


def test_v0404_restore_packet_lists_required_false_flags() -> None:
    packet = create_v0404_restore_packet()

    assert set(packet.required_false_flags) == set(REQUIRED_FALSE_FLAGS)
    assert {section.section_id for section in packet.restore_sections} == set(REQUIRED_RESTORE_SECTION_IDS)


def test_v0404_restore_document_manifest_requires_copy_paste_restore_prompt() -> None:
    manifest = create_v0404_restore_document_manifest()

    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True
    with pytest.raises(ValueError):
        create_v0404_restore_document_manifest(required_sections_present=False, suitable_for_new_session_handoff=True)


def test_v0404_restore_document_exists_and_has_required_sections() -> None:
    doc = Path("docs/versions/v0.40/v0.40.4_restore_document.md")
    assert doc.exists()
    text = doc.read_text(encoding="utf-8")

    for section in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Version Chain Summary",
        "Capability Matrix",
        "Safety Flag Canonical Values",
        "Copy-Paste Restore Prompt for Future GPT/Codex Session",
    ):
        assert section in text


def test_v0404_restore_document_contains_current_baseline_and_next_handoff() -> None:
    text = Path("docs/versions/v0.40/v0.40.4_restore_document.md").read_text(encoding="utf-8")

    assert "ChantaCore v0.40.4 is a standalone-agent preparation release" in text
    assert "v0.40.5 Provider / Prompt Boundary Deepening" in text
    assert "Standalone Default Personal runtime remains closed." in text


def test_v0404_v0405_handoff_targets_provider_prompt_boundary() -> None:
    handoff = create_v0405_provider_prompt_boundary_handoff()

    assert handoff.target_version == "v0.40.5 Provider / Prompt Boundary Deepening"
    assert "ProviderBoundaryGate hardening" in handoff.recommended_focus
    assert "no prompt submission" in handoff.recommended_focus


def test_v0404_v041_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_checkpoint_signal()

    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert v041_checkpoint_signal_is_not_runtime_start(signal)


def test_v0404_broad_approval_cannot_override_negative_gate() -> None:
    with pytest.raises(ValueError):
        create_checkpoint_approval_scope(
            approved_action_class="model_provider_invocation",
            broad_future_authority_allowed=True,
        )


def test_v0404_scoped_approval_cannot_authorize_model_prompt_or_subagent() -> None:
    decision = create_scope_bound_checkpoint_decision()

    assert decision.approval_grants_model_invocation_authority is False
    assert decision.approval_grants_prompt_submission_authority is False
    assert decision.approval_grants_subagent_invocation_authority is False


def test_v0404_stale_checkpoint_cannot_construct_second_iteration_candidate() -> None:
    result = validate_scope_bound_checkpoint_decision(
        _validation_input(freshness_evaluation=evaluate_checkpoint_freshness(current_iteration_index=2))
    )

    assert result.valid is False
    assert result.safe_to_construct_second_iteration_candidate is False


def test_v0404_valid_scoped_checkpoint_can_only_construct_manual_rehearsal_candidate() -> None:
    result = validate_scope_bound_checkpoint_decision(_validation_input())
    boundary = create_checkpoint_approval_authority_boundary(result)

    assert result.safe_to_construct_second_iteration_candidate is True
    assert boundary.allows_manual_rehearsal_candidate is True
    assert boundary.allows_runtime_execution is False


def test_v0404_restore_packet_is_suitable_for_new_session_handoff() -> None:
    packet = create_v0404_restore_packet()
    manifest = create_v0404_restore_document_manifest()

    assert restore_packet_is_suitable_for_new_session_handoff(packet, manifest)


def test_v0404_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/agent_runtime/repair_mission_loop_checkpoint_hardening.py").read_text(encoding="utf-8")
    forbidden = [
        r"\bsubprocess\b",
        r"shell=True",
        r"os\.system",
        r"\beval\(",
        r"\bexec\(",
        r"\brequests\b",
        r"\bhttpx\b",
        r"\burllib\b",
        r"\bsocket\b",
        r"\bopenai\b",
        r"\banthropic\b",
        r"\bollama\b",
        r"\blmstudio\b",
        r"apply_patch",
        r"git apply",
        r"git worktree",
    ]

    for pattern in forbidden:
        assert re.search(pattern, source) is None

