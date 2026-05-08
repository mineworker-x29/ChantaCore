from chanta_core.delegation.conformance import DelegationConformanceFinding, DelegationConformanceResult
from chanta_core.delegation.history_adapter import (
    delegation_conformance_findings_to_history_entries,
    delegation_conformance_results_to_history_entries,
)
from chanta_core.utility.time import utc_now_iso


def test_delegation_conformance_history_adapter_converts_findings_and_results() -> None:
    finding = DelegationConformanceFinding(
        finding_id="delegation_conformance_finding:history",
        run_id="delegation_conformance_run:history",
        rule_id="delegation_conformance_rule:history",
        rule_type="packet_exists",
        status="failed",
        severity="critical",
        message="Packet missing.",
        subject_type="delegation_packet",
        subject_ref="delegation_packet:history",
        evidence_refs=[{"ref_id": "delegation_packet:history"}],
        created_at=utc_now_iso(),
        finding_attrs={},
    )
    result = DelegationConformanceResult(
        result_id="delegation_conformance_result:history",
        run_id=finding.run_id,
        contract_id="delegation_conformance_contract:history",
        status="needs_review",
        score=0.5,
        confidence=0.5,
        passed_finding_ids=[],
        failed_finding_ids=[finding.finding_id],
        warning_finding_ids=[],
        skipped_finding_ids=[],
        reason="Review required.",
        created_at=utc_now_iso(),
        result_attrs={},
    )

    finding_entry = delegation_conformance_findings_to_history_entries([finding])[0]
    result_entry = delegation_conformance_results_to_history_entries([result])[0]

    assert finding_entry.source == "delegation_conformance"
    assert result_entry.source == "delegation_conformance"
    assert finding_entry.refs[0]["finding_id"] == finding.finding_id
    assert finding_entry.refs[0]["rule_id"] == finding.rule_id
    assert finding_entry.refs[0]["subject_ref"] == finding.subject_ref
    assert result_entry.refs[0]["result_id"] == result.result_id
    assert result_entry.refs[0]["contract_id"] == result.contract_id
    assert finding_entry.priority >= 90
    assert result_entry.priority >= 80
