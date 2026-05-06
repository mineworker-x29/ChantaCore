from chanta_core.verification import VerificationResult, verification_results_to_history_entries


def test_verification_results_to_history_entries_refs_and_priority() -> None:
    failed = VerificationResult(
        result_id="verification_result:failed",
        run_id="verification_run:1",
        contract_id="verification_contract:1",
        target_id="verification_target:1",
        status="failed",
        confidence=0.3,
        reason="missing supplied evidence",
        evidence_ids=["verification_evidence:1"],
        created_at="2026-05-06T00:00:00Z",
    )
    passed = VerificationResult(
        result_id="verification_result:passed",
        run_id="verification_run:1",
        contract_id="verification_contract:1",
        target_id="verification_target:1",
        status="passed",
        confidence=0.9,
        reason="evidence supplied",
        evidence_ids=["verification_evidence:2"],
        created_at="2026-05-06T00:00:01Z",
    )

    entries = verification_results_to_history_entries([failed, passed])

    assert entries[0].source == "verification"
    assert entries[0].role == "context"
    assert entries[0].priority > entries[1].priority
    ref = entries[0].refs[0]
    assert ref["result_id"] == failed.result_id
    assert ref["run_id"] == failed.run_id
    assert ref["contract_id"] == failed.contract_id
    assert ref["target_id"] == failed.target_id
    assert ref["evidence_ids"] == failed.evidence_ids
