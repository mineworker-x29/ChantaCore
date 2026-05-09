from chanta_core.persona import (
    PersonalConformanceService,
    personal_conformance_findings_to_history_entries,
    personal_conformance_results_to_history_entries,
)


def test_personal_conformance_history_entries_prioritize_failures() -> None:
    service = PersonalConformanceService()
    contract, _ = service.register_default_rules()
    run = service.start_run(
        contract_id=contract.contract_id,
        target_kind="manual",
        target_ref="dummy",
    )
    finding = service.record_finding(
        run_id=run.run_id,
        rule_type="runtime_binding_non_executing",
        status="failed",
        message="Dummy non-executing check failed.",
        subject_type="personal_runtime_binding",
        subject_ref="binding:test",
    )
    result = service.record_result(
        run_id=run.run_id,
        contract_id=contract.contract_id,
        findings=[finding],
    )

    finding_entries = personal_conformance_findings_to_history_entries([finding])
    result_entries = personal_conformance_results_to_history_entries([result])

    assert finding_entries[0].source == "personal_conformance"
    assert finding_entries[0].priority >= 80
    assert result_entries[0].source == "personal_conformance"
    assert result_entries[0].entry_attrs["failed_finding_count"] == 1
