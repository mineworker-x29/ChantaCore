import pytest

from chanta_core.verification import (
    VerificationContract,
    VerificationEvidence,
    VerificationRequirement,
    VerificationResult,
    VerificationRun,
    VerificationTarget,
    hash_content,
    new_verification_contract_id,
    new_verification_evidence_id,
    new_verification_requirement_id,
    new_verification_result_id,
    new_verification_run_id,
    new_verification_target_id,
    preview_text,
)
from chanta_core.verification.errors import VerificationResultError


NOW = "2026-05-06T00:00:00Z"


def test_verification_models_to_dict_and_helpers() -> None:
    contract = VerificationContract(
        contract_id="verification_contract:1",
        contract_name="Contract",
        contract_type="file_existence",
        description="Check supplied evidence.",
        status="active",
        subject_type="file",
        required_evidence_kinds=["manual_note"],
        pass_criteria={"ok": True},
        fail_criteria={"ok": False},
        severity="low",
        created_at=NOW,
        updated_at=NOW,
        contract_attrs={"a": 1},
    )
    target = VerificationTarget(
        target_id="verification_target:1",
        target_type="file",
        target_ref="README.md",
        target_label="README",
        status="active",
        created_at=NOW,
    )
    requirement = VerificationRequirement(
        requirement_id="verification_requirement:1",
        contract_id=contract.contract_id,
        requirement_type="must_exist",
        description="must exist",
        required=True,
        evidence_kind="manual_note",
        priority=1,
        status="active",
    )
    run = VerificationRun(
        run_id="verification_run:1",
        contract_id=contract.contract_id,
        target_ids=[target.target_id],
        status="running",
        started_at=NOW,
        completed_at=None,
        session_id="session:1",
        turn_id="conversation_turn:1",
        process_instance_id="process_instance:1",
    )
    evidence = VerificationEvidence(
        evidence_id="verification_evidence:1",
        run_id=run.run_id,
        target_id=target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="manual evidence",
        content_preview="manual evidence",
        content_hash=hash_content("manual evidence"),
        confidence=0.8,
        collected_at=NOW,
    )
    result = VerificationResult(
        result_id="verification_result:1",
        run_id=run.run_id,
        contract_id=contract.contract_id,
        target_id=target.target_id,
        status="passed",
        confidence=0.8,
        reason="evidence supplied",
        evidence_ids=[evidence.evidence_id],
        created_at=NOW,
    )

    assert contract.to_dict()["contract_type"] == "file_existence"
    assert target.to_dict()["target_ref"] == "README.md"
    assert requirement.to_dict()["contract_id"] == contract.contract_id
    assert run.to_dict()["target_ids"] == [target.target_id]
    assert evidence.to_dict()["content_hash"] == hash_content("manual evidence")
    assert result.to_dict()["evidence_ids"] == [evidence.evidence_id]
    assert hash_content("same") == hash_content("same")
    assert preview_text("abcdef", max_chars=3).endswith("...[preview truncated]...")
    assert new_verification_contract_id().startswith("verification_contract:")
    assert new_verification_target_id().startswith("verification_target:")
    assert new_verification_requirement_id().startswith("verification_requirement:")
    assert new_verification_run_id().startswith("verification_run:")
    assert new_verification_evidence_id().startswith("verification_evidence:")
    assert new_verification_result_id().startswith("verification_result:")


def test_passed_and_failed_results_require_evidence() -> None:
    with pytest.raises(VerificationResultError):
        VerificationResult(
            result_id="verification_result:no-evidence",
            run_id=None,
            contract_id="verification_contract:1",
            target_id=None,
            status="passed",
            confidence=None,
            reason=None,
            evidence_ids=[],
            created_at=NOW,
        )

    result = VerificationResult(
        result_id="verification_result:inconclusive",
        run_id=None,
        contract_id="verification_contract:1",
        target_id=None,
        status="inconclusive",
        confidence=None,
        reason=None,
        evidence_ids=[],
        created_at=NOW,
    )
    assert result.status == "inconclusive"
