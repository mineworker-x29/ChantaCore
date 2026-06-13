from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_verifier_subagent_boundary import (
    CLOSED_CAPABILITIES,
    FORBIDDEN_VERIFIER_ROLES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_RESTORE_SECTION_IDS,
    VerifierDispatchStatus,
    VerifierRequestStatus,
    VerifierRoleKind,
    VerifierSubagentBoundaryKind,
    VerifierSubagentFalseClaimKind,
    audit_verifier_subagent_false_claim,
    create_subagent_verification_request_draft,
    create_v0406_integrated_restore_context_snapshot,
    create_v0406_integrated_restore_document_manifest,
    create_v0406_integrated_restore_packet,
    create_v0407_rehearsal_evidence_matrix_handoff,
    create_v041_smoke_run_acceleration_verifier_signal,
    create_verifier_context_isolation_contract,
    create_verifier_evidence_requirement,
    create_verifier_parent_context_boundary,
    create_verifier_permission_scope,
    create_verifier_result_quarantine_contract,
    create_verifier_result_quarantine_envelope,
    create_verifier_return_envelope_contract,
    create_verifier_role_contract,
    create_verifier_subagent_authority_boundary,
    create_verifier_subagent_boundary_audit_record,
    create_verifier_subagent_boundary_readiness_report,
    create_verifier_subagent_boundary_safety_report,
    create_verifier_subagent_dispatch_gate_policy,
    create_verifier_subagent_invocation_blocked_decision,
    evaluate_verifier_evidence_requirement,
    evaluate_verifier_subagent_dispatch_gate,
    integrated_restore_packet_uses_single_doc,
    verifier_dispatch_evaluation_is_blocked,
    verifier_readiness_preserves_no_unsafe_runtime,
    verifier_request_draft_is_metadata_only,
    v041_verifier_signal_is_not_runtime_start,
)


def test_v0406_verifier_boundary_kinds_declared() -> None:
    assert {item.value for item in VerifierSubagentBoundaryKind} == {
        "verifier_request_draft",
        "verifier_role_contract",
        "verifier_evidence_requirement",
        "verifier_context_isolation",
        "verifier_permission_scope",
        "verifier_dispatch_gate",
        "verifier_result_quarantine",
    }


def test_v0406_verifier_role_kinds_declared() -> None:
    assert {item.value for item in VerifierRoleKind} == {
        "evidence_reviewer",
        "boundary_reviewer",
        "safety_invariant_reviewer",
        "restore_document_reviewer",
        "test_result_reviewer",
        "readiness_flag_reviewer",
    }


def test_v0406_request_status_and_dispatch_status_declared() -> None:
    assert "evidence_eligible_for_draft" in {item.value for item in VerifierRequestStatus}
    assert "blocked" in {item.value for item in VerifierDispatchStatus}


def test_v0406_verification_request_draft_is_metadata_only() -> None:
    draft = create_subagent_verification_request_draft()

    assert verifier_request_draft_is_metadata_only(draft)
    assert draft.invocation_requested is True
    with pytest.raises(ValueError):
        create_subagent_verification_request_draft(metadata_only=False)


def test_v0406_verification_request_draft_does_not_invoke_subagent() -> None:
    with pytest.raises(ValueError):
        create_subagent_verification_request_draft(subagent_invoked=True)


def test_v0406_verification_request_draft_does_not_create_child_session() -> None:
    with pytest.raises(ValueError):
        create_subagent_verification_request_draft(child_session_created=True)


@pytest.mark.parametrize("role", FORBIDDEN_VERIFIER_ROLES)
def test_v0406_verifier_role_contract_rejects_executor_roles(role: str) -> None:
    with pytest.raises(ValueError):
        create_verifier_role_contract(verifier_role_kind=role)


def test_v0406_evidence_requirement_blocks_missing_evidence() -> None:
    requirement = create_verifier_evidence_requirement(provided_evidence_refs={})
    evaluation = evaluate_verifier_evidence_requirement(requirement)

    assert evaluation.complete is False
    assert evaluation.eligible_for_verifier_draft is False


def test_v0406_evidence_requirement_blocks_mismatched_evidence() -> None:
    requirement = create_verifier_evidence_requirement(
        provided_evidence_refs={"loop_decision_ref": "wrong", **{k: f"{k}-v0406" for k in ("checkpoint_decision_ref", "safety_report_ref", "negative_gate_report_ref", "provider_prompt_boundary_report_ref", "restore_document_ref", "readiness_report_ref")}}
    )
    evaluation = evaluate_verifier_evidence_requirement(requirement)

    assert evaluation.complete is False
    assert evaluation.mismatched_evidence_types == ("loop_decision_ref",)


def test_v0406_evidence_requirement_can_mark_draft_eligible_without_invocation() -> None:
    evaluation = evaluate_verifier_evidence_requirement()

    assert evaluation.complete is True
    assert evaluation.eligible_for_verifier_draft is True
    assert evaluation.invocation_authority_granted is False


def test_v0406_context_isolation_blocks_parent_raw_transcript_sharing() -> None:
    contract = create_verifier_context_isolation_contract()

    assert contract.parent_raw_transcript_shared is False
    assert contract.child_context_isolated is True
    with pytest.raises(ValueError):
        create_verifier_context_isolation_contract(parent_raw_transcript_shared=True)


def test_v0406_context_isolation_blocks_parent_hidden_context_credentials_and_runtime_authority() -> None:
    contract = create_verifier_context_isolation_contract()

    assert contract.parent_hidden_context_shared is False
    assert contract.parent_credentials_shared is False
    assert contract.parent_runtime_authority_shared is False


def test_v0406_permission_scope_blocks_workspace_write_shell_network_credentials_provider_prompt_and_subagent_chaining() -> None:
    scope = create_verifier_permission_scope()

    assert scope.read_only_metadata_scope is True
    assert scope.workspace_write_allowed is False
    assert scope.shell_allowed is False
    assert scope.network_allowed is False
    assert scope.credential_access_allowed is False
    assert scope.provider_invocation_allowed is False
    assert scope.prompt_submission_allowed is False
    assert scope.subagent_chaining_allowed is False


def test_v0406_dispatch_gate_policy_is_deny_by_default() -> None:
    policy = create_verifier_subagent_dispatch_gate_policy()

    assert policy.deny_by_default is True
    assert policy.invocation_allowed is False
    assert policy.child_session_creation_allowed is False
    assert policy.parent_context_sharing_allowed is False
    assert policy.permission_grant_allowed is False


def test_v0406_dispatch_gate_blocks_subagent_invocation_child_session_and_parent_context_sharing() -> None:
    evaluation = evaluate_verifier_subagent_dispatch_gate()

    assert verifier_dispatch_evaluation_is_blocked(evaluation)
    assert evaluation.subagent_invoked is False
    assert evaluation.child_session_created is False
    assert evaluation.parent_raw_transcript_shared is False
    assert evaluation.executed is False


def test_v0406_invocation_blocked_decision_never_grants_runtime_authority() -> None:
    decision = create_verifier_subagent_invocation_blocked_decision()

    assert decision.blocked is True
    assert decision.subagent_invoked is False
    assert decision.child_session_created is False
    assert decision.runtime_authority_granted is False


def test_v0406_return_envelope_requires_summary_only_and_structured_result() -> None:
    contract = create_verifier_return_envelope_contract()

    assert contract.summary_only_return is True
    assert contract.structured_result_required is True
    assert contract.human_review_required is True


def test_v0406_return_envelope_blocks_raw_child_transcript_return() -> None:
    contract = create_verifier_return_envelope_contract()

    assert contract.raw_child_transcript_return_allowed is False
    assert contract.direct_process_state_update_allowed is False
    assert contract.direct_memory_write_allowed is False


def test_v0406_result_quarantine_contract_blocks_direct_persistence_process_state_memory_and_execution() -> None:
    contract = create_verifier_result_quarantine_contract()

    assert contract.raw_verifier_result_trusted is False
    assert contract.direct_persistence_allowed is False
    assert contract.direct_process_state_update_allowed is False
    assert contract.direct_memory_write_allowed is False
    assert contract.direct_execution_allowed is False
    assert contract.requires_schema_validation is True
    assert contract.requires_human_review is True
    assert contract.requires_provenance is True


def test_v0406_result_quarantine_envelope_is_metadata_only_and_not_eligible_for_execution() -> None:
    envelope = create_verifier_result_quarantine_envelope()

    assert envelope.quarantined is True
    assert envelope.metadata_only is True
    assert envelope.eligible_for_persistence is False
    assert envelope.eligible_for_process_state is False
    assert envelope.eligible_for_memory is False
    assert envelope.eligible_for_execution is False


def test_v0406_authority_boundary_blocks_all_subagent_runtime_authority() -> None:
    boundary = create_verifier_subagent_authority_boundary()

    assert boundary.allows_subagent_invocation is False
    assert boundary.allows_child_session_creation is False
    assert boundary.allows_parent_raw_transcript_sharing is False
    assert boundary.allows_workspace_write is False
    assert boundary.allows_live_workspace_apply is False
    assert boundary.allows_shell_execution is False
    assert boundary.allows_network_access is False
    assert boundary.allows_credential_access is False
    assert boundary.allows_provider_invocation is False
    assert boundary.allows_prompt_submission is False
    assert boundary.allows_subagent_chaining is False


def test_v0406_false_subagent_invocation_ready_claim_is_blocked() -> None:
    audit = audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.VERIFIER_SUBAGENT_INVOCATION_READY.value)

    assert audit.claim_allowed is False
    assert audit.readiness_flag_modified is False


def test_v0406_false_child_session_ready_claim_is_blocked() -> None:
    assert audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.VERIFIER_CHILD_SESSION_READY.value).claim_allowed is False


def test_v0406_false_parent_raw_transcript_sharing_claim_is_blocked() -> None:
    assert audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.PARENT_RAW_TRANSCRIPT_SHARING_READY.value).claim_allowed is False


def test_v0406_false_verifier_result_trusted_claim_is_blocked() -> None:
    assert audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.VERIFIER_RESULT_TRUSTED.value).claim_allowed is False


def test_v0406_false_subagent_chaining_standalone_and_production_claims_are_blocked() -> None:
    assert audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.SUBAGENT_CHAINING_READY.value).claim_allowed is False
    assert audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY.value).claim_allowed is False
    assert audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.PRODUCTION_CERTIFIED.value).claim_allowed is False


def test_v0406_audit_record_checks_role_evidence_context_dispatch_quarantine_and_false_claims() -> None:
    audit = create_verifier_subagent_boundary_audit_record()

    assert audit.checked_role_contract is True
    assert audit.checked_evidence_requirement is True
    assert audit.checked_context_isolation is True
    assert audit.checked_dispatch_gate is True
    assert audit.checked_result_quarantine is True
    assert audit.checked_false_claims_blocked is True


def test_v0406_safety_report_keeps_subagent_child_session_context_runtime_false() -> None:
    report = create_verifier_subagent_boundary_safety_report()

    assert report.safe_for_v0406_verifier_boundary is True
    assert report.safe_for_subagent_invocation is False
    assert report.safe_for_child_session_creation is False
    assert report.safe_for_parent_raw_transcript_sharing is False
    assert report.production_certified is False


def test_v0406_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_verifier_subagent_boundary_readiness_report()

    assert report.verifier_subagent_boundary_deepening_defined is True
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False
    assert verifier_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_verifier_subagent_boundary_readiness_report(ready_for_subagent_invocation=True)


def test_v0406_integrated_restore_snapshot_lists_version_chain_and_open_closed_capabilities() -> None:
    snapshot = create_v0406_integrated_restore_context_snapshot()

    assert len(snapshot.baseline_versions) == 7
    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)


def test_v0406_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = create_v0406_integrated_restore_packet()

    assert packet.single_integrated_doc_path == "docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening_restore.md"
    assert integrated_restore_packet_uses_single_doc(packet)


def test_v0406_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = create_v0406_integrated_restore_packet()

    assert packet.separate_restore_doc_created is False
    with pytest.raises(ValueError):
        create_v0406_integrated_restore_packet(separate_restore_doc_created=True)


def test_v0406_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0406_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.suitable_for_new_session_handoff is True


def test_v0406_integrated_document_exists_and_has_required_restore_sections() -> None:
    doc = Path(INTEGRATED_DOC_PATH)

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for heading in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Version Chain Summary",
        "v0.40.6 Verifier Subagent Boundary Summary",
        "Capability Matrix",
        "Safety Flag Canonical Values",
        "Withdrawal Conditions",
        "v0.40.7 Recommended Next Step",
    ):
        assert heading in text


def test_v0406_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "You are continuing ChantaCore after v0.40.6." in text
    assert "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation" in text


def test_v0406_no_separate_v0406_restore_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.6_restore_document.md").exists()


def test_v0406_no_separate_v0406_release_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening.md").exists()
    assert not Path("docs/versions/v0.40/v0.40.6_subagent_boundary_coverage.md").exists()


def test_v0406_v0407_handoff_targets_rehearsal_evidence_matrix() -> None:
    handoff = create_v0407_rehearsal_evidence_matrix_handoff()

    assert handoff.target_version == "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation"
    assert "V040RehearsalEvidenceMatrix" in handoff.recommended_focus


def test_v0406_v041_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_verifier_signal()

    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert v041_verifier_signal_is_not_runtime_start(signal)


def test_v0406_request_draft_to_evidence_requirement_to_dispatch_blocked_flow() -> None:
    evidence = evaluate_verifier_evidence_requirement()
    draft = create_subagent_verification_request_draft()
    evaluation = evaluate_verifier_subagent_dispatch_gate(draft)

    assert evidence.eligible_for_verifier_draft is True
    assert draft.subagent_invoked is False
    assert evaluation.blocked is True
    assert evaluation.subagent_invoked is False


def test_v0406_false_claims_do_not_modify_readiness_flags() -> None:
    audit = audit_verifier_subagent_false_claim(VerifierSubagentFalseClaimKind.VERIFIER_CHILD_SESSION_READY.value)
    readiness = create_verifier_subagent_boundary_readiness_report()

    assert audit.readiness_flag_modified is False
    assert readiness.ready_for_child_session_creation is False


def test_v0406_integrated_restore_doc_is_suitable_for_new_session_handoff() -> None:
    packet = create_v0406_integrated_restore_packet()
    manifest = create_v0406_integrated_restore_document_manifest()

    assert set(REQUIRED_RESTORE_SECTION_IDS) == {section.section_id for section in packet.restore_sections}
    assert manifest.suitable_for_new_session_handoff is True


def test_v0406_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/agent_runtime/repair_mission_loop_verifier_subagent_boundary.py").read_text(encoding="utf-8")
    forbidden_runtime_patterns = [
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
        r"api_key",
        r"\bsecret\b",
        r"invoke_subagent",
        r"run_subagent",
        r"create_child_session",
        r"spawn_agent",
    ]

    for pattern in forbidden_runtime_patterns:
        assert re.search(pattern, source) is None
    metadata_hits = [line for line in source.splitlines() if "credential" in line.lower() or "child_session" in line.lower()]
    assert metadata_hits
    assert all(
        (
            "credential" in line.lower()
            or "child_session_" in line.lower()
            or "child_session_created" in line.lower()
            or "child_session\"" in line.lower()
        )
        for line in metadata_hits
    )
