import pytest

from chanta_core.persona import (
    PersonalConformanceContract,
    PersonalConformanceFinding,
    PersonalConformanceResult,
    PersonalConformanceRule,
    PersonalConformanceRun,
)
from chanta_core.persona.errors import PersonalConformanceError
from chanta_core.utility.time import utc_now_iso


def test_personal_conformance_models_to_dict() -> None:
    created_at = utc_now_iso()
    contract = PersonalConformanceContract(
        contract_id="personal_conformance_contract:test",
        contract_name="default_personal_conformance",
        contract_type="privacy_boundary",
        description="Public-safe structural contract.",
        status="active",
        severity="high",
        created_at=created_at,
        updated_at=created_at,
    )
    rule = PersonalConformanceRule(
        rule_id="personal_conformance_rule:test",
        contract_id=contract.contract_id,
        rule_type="canonical_import_disabled",
        description="Canonical import remains disabled.",
        required=True,
        severity="high",
        expected_value="False",
        status="active",
    )
    run = PersonalConformanceRun(
        run_id="personal_conformance_run:test",
        contract_id=contract.contract_id,
        target_kind="persona_source_candidate",
        target_ref="candidate:test",
        status="started",
        started_at=created_at,
        completed_at=None,
    )
    finding = PersonalConformanceFinding(
        finding_id="personal_conformance_finding:test",
        run_id=run.run_id,
        rule_id=rule.rule_id,
        rule_type=rule.rule_type,
        status="passed",
        severity="high",
        message="Rule passed.",
        subject_type="persona_source_candidate",
        subject_ref="candidate:test",
        evidence_refs=[{"kind": "dummy"}],
        created_at=created_at,
    )
    result = PersonalConformanceResult(
        result_id="personal_conformance_result:test",
        run_id=run.run_id,
        contract_id=contract.contract_id,
        status="passed",
        score=1.0,
        confidence=1.0,
        passed_finding_ids=[finding.finding_id],
        failed_finding_ids=[],
        warning_finding_ids=[],
        skipped_finding_ids=[],
        reason=None,
        created_at=created_at,
    )

    assert contract.to_dict()["contract_type"] == "privacy_boundary"
    assert rule.to_dict()["rule_type"] == "canonical_import_disabled"
    assert run.to_dict()["target_kind"] == "persona_source_candidate"
    assert finding.to_dict()["evidence_refs"] == [{"kind": "dummy"}]
    assert result.to_dict()["score"] == 1.0


def test_personal_conformance_result_rejects_out_of_range_score() -> None:
    with pytest.raises(PersonalConformanceError):
        PersonalConformanceResult(
            result_id="personal_conformance_result:test",
            run_id="personal_conformance_run:test",
            contract_id="personal_conformance_contract:test",
            status="error",
            score=1.2,
            confidence=1.0,
            passed_finding_ids=[],
            failed_finding_ids=[],
            warning_finding_ids=[],
            skipped_finding_ids=[],
            reason="bad score",
            created_at=utc_now_iso(),
        )
