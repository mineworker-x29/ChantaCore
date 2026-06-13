from __future__ import annotations

import re
from pathlib import Path

import pytest

from chanta_core.agent_runtime.repair_mission_loop_provider_prompt_boundary import (
    CLOSED_CAPABILITIES,
    INTEGRATED_DOC_PATH,
    OPEN_CAPABILITIES,
    REQUIRED_FALSE_FLAGS,
    REQUIRED_RESTORE_SECTION_IDS,
    ProviderBoundaryKind,
    ProviderInvocationStatus,
    ProviderPromptFalseClaimKind,
    PromptBoundaryKind,
    PromptDispatchStatus,
    audit_provider_prompt_false_claim,
    create_prompt_dispatch_blocked_decision,
    create_prompt_dispatch_candidate,
    create_prompt_provider_boundary_decision,
    create_prompt_submission_gate_policy,
    create_provider_invocation_blocked_decision,
    create_provider_invocation_gate_policy,
    create_provider_output_quarantine_contract,
    create_provider_output_quarantine_envelope,
    create_provider_prompt_authority_boundary,
    create_provider_prompt_boundary_audit_record,
    create_provider_prompt_boundary_readiness_report,
    create_provider_prompt_boundary_safety_report,
    create_v0405_integrated_restore_context_snapshot,
    create_v0405_integrated_restore_document_manifest,
    create_v0405_integrated_restore_packet,
    create_v0406_verifier_subagent_boundary_handoff,
    create_v041_smoke_run_acceleration_provider_prompt_signal,
    evaluate_prompt_submission_gate,
    evaluate_provider_invocation_gate,
    integrated_restore_packet_uses_single_doc,
    prompt_dispatch_candidate_is_metadata_only,
    provider_invocation_evaluation_is_blocked,
    provider_prompt_readiness_preserves_no_unsafe_runtime,
    v041_provider_prompt_signal_is_not_runtime_start,
)


def test_v0405_prompt_boundary_kinds_declared() -> None:
    assert {item.value for item in PromptBoundaryKind} == {
        "prompt_draft",
        "prompt_dispatch_candidate",
        "prompt_submission_gate",
        "prompt_submission_blocked_decision",
    }


def test_v0405_provider_boundary_kinds_declared() -> None:
    assert {item.value for item in ProviderBoundaryKind} == {
        "provider_reference",
        "model_reference",
        "provider_invocation_gate",
        "provider_invocation_blocked_decision",
        "provider_output_quarantine_contract",
        "provider_output_quarantine_envelope",
    }


def test_v0405_prompt_dispatch_candidate_is_metadata_only() -> None:
    candidate = create_prompt_dispatch_candidate()

    assert candidate.dispatch_status == PromptDispatchStatus.CANDIDATE_CREATED.value
    assert prompt_dispatch_candidate_is_metadata_only(candidate)
    with pytest.raises(ValueError):
        create_prompt_dispatch_candidate(metadata_only=False)


def test_v0405_prompt_dispatch_candidate_does_not_submit_to_model() -> None:
    assert create_prompt_dispatch_candidate().submitted_to_model is False
    with pytest.raises(ValueError):
        create_prompt_dispatch_candidate(submitted_to_model=True)


def test_v0405_prompt_dispatch_candidate_does_not_invoke_provider() -> None:
    assert create_prompt_dispatch_candidate().provider_invoked is False
    with pytest.raises(ValueError):
        create_prompt_dispatch_candidate(provider_invoked=True)


def test_v0405_prompt_submission_policy_is_deny_by_default() -> None:
    policy = create_prompt_submission_gate_policy()

    assert policy.deny_by_default is True
    assert policy.submission_allowed is False
    assert policy.human_checkpoint_required is True
    with pytest.raises(ValueError):
        create_prompt_submission_gate_policy(submission_allowed=True)


def test_v0405_prompt_submission_gate_blocks_submission() -> None:
    evaluation = evaluate_prompt_submission_gate()

    assert evaluation.blocked is True
    assert evaluation.submitted_to_model is False
    assert evaluation.executed is False


def test_v0405_provider_invocation_policy_is_deny_by_default() -> None:
    policy = create_provider_invocation_gate_policy()

    assert policy.deny_by_default is True
    assert policy.invocation_allowed is False
    assert policy.network_allowed is False
    assert policy.credential_access_allowed is False
    assert policy.client_creation_allowed is False


def test_v0405_provider_invocation_gate_blocks_invocation_network_credentials_and_client_creation() -> None:
    evaluation = evaluate_provider_invocation_gate()

    assert evaluation.blocked is True
    assert evaluation.provider_invoked is False
    assert evaluation.network_used is False
    assert evaluation.credential_accessed is False
    assert evaluation.client_created is False
    assert evaluation.executed is False
    assert provider_invocation_evaluation_is_blocked(evaluation)


def test_v0405_prompt_provider_decision_never_grants_runtime_authority() -> None:
    decision = create_prompt_provider_boundary_decision()

    assert decision.prompt_submission_allowed is False
    assert decision.provider_invocation_allowed is False
    assert decision.runtime_authority_granted is False
    with pytest.raises(ValueError):
        create_prompt_provider_boundary_decision(runtime_authority_granted=True)


def test_v0405_prompt_dispatch_blocked_decision_blocks_submission() -> None:
    decision = create_prompt_dispatch_blocked_decision()

    assert decision.blocked is True
    assert decision.prompt_submission_allowed is False
    assert decision.submitted_to_model is False


def test_v0405_provider_invocation_blocked_decision_blocks_provider_network_credentials_and_client() -> None:
    decision = create_provider_invocation_blocked_decision()

    assert decision.blocked is True
    assert decision.provider_invoked is False
    assert decision.network_allowed is False
    assert decision.credential_access_allowed is False
    assert decision.client_creation_allowed is False


def test_v0405_provider_output_quarantine_contract_requires_redaction_schema_validation_human_review_and_provenance() -> None:
    contract = create_provider_output_quarantine_contract()

    assert contract.raw_provider_output_trusted is False
    assert contract.direct_persistence_allowed is False
    assert contract.direct_execution_allowed is False
    assert contract.requires_redaction is True
    assert contract.requires_schema_validation is True
    assert contract.requires_human_review is True
    assert contract.requires_provenance is True
    assert contract.eligible_for_process_state_only_after_validation is True


def test_v0405_quarantine_envelope_blocks_direct_persistence_and_execution() -> None:
    envelope = create_provider_output_quarantine_envelope()

    assert envelope.quarantined is True
    assert envelope.validated is False
    assert envelope.redacted is False
    assert envelope.eligible_for_persistence is False
    assert envelope.eligible_for_execution is False
    assert envelope.metadata_only is True


def test_v0405_authority_boundary_blocks_all_provider_prompt_runtime_authority() -> None:
    boundary = create_provider_prompt_authority_boundary()

    assert boundary.allows_prompt_submission is False
    assert boundary.allows_provider_invocation is False
    assert boundary.allows_network_access is False
    assert boundary.allows_credential_access is False
    assert boundary.allows_client_creation is False
    assert boundary.allows_direct_provider_output_persistence is False
    assert boundary.allows_direct_provider_output_execution is False
    assert boundary.allows_runtime_execution is False
    assert boundary.allows_standalone_default_personal_runtime is False
    assert boundary.allows_production_certification is False


def test_v0405_false_prompt_submission_ready_claim_is_blocked() -> None:
    audit = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.PROMPT_SUBMISSION_READY.value)

    assert audit.claim_allowed is False
    assert audit.readiness_flag_modified is False


def test_v0405_false_provider_invocation_ready_claim_is_blocked() -> None:
    audit = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.MODEL_PROVIDER_INVOCATION_READY.value)

    assert audit.claim_allowed is False


def test_v0405_false_provider_output_trusted_claim_is_blocked() -> None:
    audit = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.PROVIDER_OUTPUT_TRUSTED.value)

    assert audit.claim_allowed is False


def test_v0405_false_network_credential_access_claims_are_blocked() -> None:
    network_audit = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.NETWORK_ACCESS_READY.value)
    credential_audit = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.CREDENTIAL_ACCESS_READY.value)

    assert network_audit.claim_allowed is False
    assert credential_audit.claim_allowed is False


def test_v0405_false_standalone_and_production_claims_are_blocked() -> None:
    standalone = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.STANDALONE_DEFAULT_PERSONAL_RUNTIME_READY.value)
    production = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.PRODUCTION_CERTIFIED.value)

    assert standalone.claim_allowed is False
    assert production.claim_allowed is False


def test_v0405_audit_record_checks_prompt_provider_network_credential_client_and_quarantine() -> None:
    audit = create_provider_prompt_boundary_audit_record()

    assert audit.checked_prompt_dispatch_candidate_metadata_only is True
    assert audit.checked_prompt_submission_blocked is True
    assert audit.checked_provider_invocation_blocked is True
    assert audit.checked_network_blocked is True
    assert audit.checked_credential_access_blocked is True
    assert audit.checked_client_creation_blocked is True
    assert audit.checked_quarantine_required is True


def test_v0405_safety_report_keeps_prompt_provider_network_credential_runtime_false() -> None:
    report = create_provider_prompt_boundary_safety_report()

    assert report.safe_for_v0405_provider_prompt_boundary is True
    assert report.safe_for_prompt_submission is False
    assert report.safe_for_provider_invocation is False
    assert report.safe_for_network_access is False
    assert report.safe_for_credential_access is False
    assert report.safe_for_client_creation is False
    assert report.production_certified is False


def test_v0405_readiness_report_keeps_unsafe_flags_false() -> None:
    report = create_provider_prompt_boundary_readiness_report()

    assert report.provider_prompt_boundary_deepening_defined is True
    for flag in REQUIRED_FALSE_FLAGS:
        assert getattr(report, flag) is False
    assert provider_prompt_readiness_preserves_no_unsafe_runtime(report)
    with pytest.raises(ValueError):
        create_provider_prompt_boundary_readiness_report(ready_for_prompt_submission_to_model=True)


def test_v0405_integrated_restore_snapshot_lists_version_chain_and_open_closed_capabilities() -> None:
    snapshot = create_v0405_integrated_restore_context_snapshot()

    assert len(snapshot.baseline_versions) == 6
    assert set(OPEN_CAPABILITIES).issubset(snapshot.open_capabilities)
    assert set(CLOSED_CAPABILITIES).issubset(snapshot.closed_capabilities)


def test_v0405_restore_packet_uses_single_integrated_doc_path() -> None:
    packet = create_v0405_integrated_restore_packet()

    assert packet.single_integrated_doc_path == INTEGRATED_DOC_PATH
    assert integrated_restore_packet_uses_single_doc(packet)


def test_v0405_restore_packet_marks_separate_restore_doc_created_false() -> None:
    packet = create_v0405_integrated_restore_packet()

    assert packet.separate_restore_doc_created is False
    with pytest.raises(ValueError):
        create_v0405_integrated_restore_packet(separate_restore_doc_created=True)


def test_v0405_integrated_restore_manifest_disallows_separate_restore_doc() -> None:
    manifest = create_v0405_integrated_restore_document_manifest()

    assert manifest.integrated_doc_required is True
    assert manifest.separate_restore_doc_allowed is False
    assert manifest.separate_restore_doc_created is False
    assert manifest.copy_paste_restore_prompt_required is True
    assert manifest.suitable_for_new_session_handoff is True


def test_v0405_integrated_document_exists_and_has_required_restore_sections() -> None:
    doc = Path(INTEGRATED_DOC_PATH)

    assert doc.exists()
    text = doc.read_text(encoding="utf-8")
    for heading in (
        "Restore Purpose",
        "One-Screen Restore Summary",
        "Current Version and Track Identity",
        "Version Chain Summary",
        "v0.40.5 Provider / Prompt Boundary Summary",
        "Capability Matrix",
        "Safety Flag Canonical Values",
        "Withdrawal Conditions",
        "v0.40.6 Recommended Next Step",
    ):
        assert heading in text


def test_v0405_integrated_document_contains_copy_paste_restore_prompt() -> None:
    text = Path(INTEGRATED_DOC_PATH).read_text(encoding="utf-8")

    assert "Copy-Paste Restore Prompt for Future GPT/Codex Session" in text
    assert "You are continuing ChantaCore after v0.40.5." in text
    assert "v0.40.6 Verifier Subagent Boundary Deepening" in text


def test_v0405_no_separate_v0405_restore_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.5_restore_document.md").exists()


def test_v0405_no_separate_v0405_release_document_created() -> None:
    assert not Path("docs/versions/v0.40/v0.40.5_provider_prompt_boundary_deepening.md").exists()
    assert not Path("docs/versions/v0.40/v0.40.5_denied_provider_prompt_coverage.md").exists()


def test_v0405_v0406_handoff_targets_verifier_subagent_boundary() -> None:
    handoff = create_v0406_verifier_subagent_boundary_handoff()

    assert handoff.target_version == "v0.40.6 Verifier Subagent Boundary Deepening"
    assert "VerifierSubagentBoundary hardening" in handoff.recommended_focus
    assert "no actual subagent invocation" in handoff.recommended_focus


def test_v0405_v041_acceleration_signal_is_non_authoritative() -> None:
    signal = create_v041_smoke_run_acceleration_provider_prompt_signal()

    assert signal.conservative_target == "v0.41.6"
    assert signal.earliest_candidate_target == "v0.41.6"
    assert v041_provider_prompt_signal_is_not_runtime_start(signal)


def test_v0405_prompt_candidate_to_submission_gate_to_blocked_decision_flow() -> None:
    candidate = create_prompt_dispatch_candidate()
    evaluation = evaluate_prompt_submission_gate(candidate)
    decision = create_prompt_dispatch_blocked_decision(candidate_ref=candidate.candidate_id)

    assert candidate.metadata_only is True
    assert evaluation.blocked is True
    assert decision.blocked is True
    assert decision.submitted_to_model is False


def test_v0405_provider_reference_to_invocation_gate_to_quarantine_contract_flow() -> None:
    candidate = create_prompt_dispatch_candidate()
    evaluation = evaluate_provider_invocation_gate(candidate)
    contract = create_provider_output_quarantine_contract(provider_ref=candidate.provider_ref, model_ref=candidate.model_ref)

    assert evaluation.provider_invoked is False
    assert evaluation.network_used is False
    assert contract.raw_provider_output_trusted is False
    assert contract.direct_execution_allowed is False


def test_v0405_false_claims_do_not_modify_readiness_flags() -> None:
    audit = audit_provider_prompt_false_claim(ProviderPromptFalseClaimKind.MODEL_PROVIDER_INVOCATION_READY.value)
    readiness = create_provider_prompt_boundary_readiness_report()

    assert audit.readiness_flag_modified is False
    assert readiness.ready_for_model_provider_invocation is False


def test_v0405_integrated_restore_doc_is_suitable_for_new_session_handoff() -> None:
    packet = create_v0405_integrated_restore_packet()
    manifest = create_v0405_integrated_restore_document_manifest()

    assert set(REQUIRED_RESTORE_SECTION_IDS) == {section.section_id for section in packet.restore_sections}
    assert manifest.suitable_for_new_session_handoff is True


def test_v0405_no_forbidden_runtime_call_patterns() -> None:
    source = Path("src/chanta_core/agent_runtime/repair_mission_loop_provider_prompt_boundary.py").read_text(encoding="utf-8")
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
    ]

    for pattern in forbidden_runtime_patterns:
        assert re.search(pattern, source) is None
    credential_hits = [line for line in source.splitlines() if "credential" in line.lower()]
    assert credential_hits
    assert all("credential_access" in line.lower() or "credential_" in line.lower() for line in credential_hits)

