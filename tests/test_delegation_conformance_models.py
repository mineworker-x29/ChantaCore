import pytest

from chanta_core.delegation.conformance import (
    DelegationConformanceContract,
    DelegationConformanceResult,
    DelegationConformanceRule,
    DelegationConformanceRun,
    DelegationConformanceFinding,
)
from chanta_core.delegation.ids import (
    new_delegation_conformance_contract_id,
    new_delegation_conformance_finding_id,
    new_delegation_conformance_result_id,
    new_delegation_conformance_rule_id,
    new_delegation_conformance_run_id,
)
from chanta_core.utility.time import utc_now_iso


def test_delegation_conformance_ids_use_expected_prefixes() -> None:
    assert new_delegation_conformance_contract_id().startswith("delegation_conformance_contract:")
    assert new_delegation_conformance_rule_id().startswith("delegation_conformance_rule:")
    assert new_delegation_conformance_run_id().startswith("delegation_conformance_run:")
    assert new_delegation_conformance_finding_id().startswith("delegation_conformance_finding:")
    assert new_delegation_conformance_result_id().startswith("delegation_conformance_result:")


def test_delegation_conformance_models_to_dict() -> None:
    now = utc_now_iso()
    contract = DelegationConformanceContract(
        contract_id="delegation_conformance_contract:1",
        contract_name="Default",
        contract_type="delegation_structure",
        description="Check structure.",
        status="active",
        severity="high",
        created_at=now,
        updated_at=now,
        contract_attrs={"default": True},
    )
    rule = DelegationConformanceRule(
        rule_id="delegation_conformance_rule:1",
        contract_id=contract.contract_id,
        rule_type="packet_exists",
        description="Packet exists.",
        required=True,
        severity="critical",
        expected_value="true",
        status="active",
        rule_attrs={},
    )
    run = DelegationConformanceRun(
        run_id="delegation_conformance_run:1",
        contract_id=contract.contract_id,
        packet_id="delegation_packet:1",
        delegated_run_id="delegated_process_run:1",
        sidechain_context_id="sidechain_context:1",
        return_envelope_id="sidechain_return_envelope:1",
        status="started",
        started_at=now,
        completed_at=None,
        run_attrs={},
    )
    finding = DelegationConformanceFinding(
        finding_id="delegation_conformance_finding:1",
        run_id=run.run_id,
        rule_id=rule.rule_id,
        rule_type=rule.rule_type,
        status="passed",
        severity="critical",
        message="Packet exists.",
        subject_type="delegation_packet",
        subject_ref="delegation_packet:1",
        evidence_refs=[{"ref_id": "delegation_packet:1"}],
        created_at=now,
        finding_attrs={},
    )
    result = DelegationConformanceResult(
        result_id="delegation_conformance_result:1",
        run_id=run.run_id,
        contract_id=contract.contract_id,
        status="passed",
        score=1.0,
        confidence=1.0,
        passed_finding_ids=[finding.finding_id],
        failed_finding_ids=[],
        warning_finding_ids=[],
        skipped_finding_ids=[],
        reason="All passed.",
        created_at=now,
        result_attrs={},
    )

    assert contract.to_dict()["contract_type"] == "delegation_structure"
    assert rule.to_dict()["rule_type"] == "packet_exists"
    assert run.to_dict()["packet_id"] == "delegation_packet:1"
    assert finding.to_dict()["status"] == "passed"
    assert result.to_dict()["score"] == 1.0


def test_delegation_conformance_result_validates_probability_fields() -> None:
    with pytest.raises(ValueError):
        DelegationConformanceResult(
            result_id="delegation_conformance_result:bad",
            run_id="delegation_conformance_run:bad",
            contract_id="delegation_conformance_contract:bad",
            status="passed",
            score=1.5,
            confidence=1.0,
            passed_finding_ids=[],
            failed_finding_ids=[],
            warning_finding_ids=[],
            skipped_finding_ids=[],
            reason=None,
            created_at=utc_now_iso(),
            result_attrs={},
        )
