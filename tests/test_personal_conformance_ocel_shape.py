from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.persona import PersonalConformanceService
from chanta_core.pig.reports import PIGReportService
from chanta_core.traces.trace_service import TraceService


def test_personal_conformance_ocel_shape_and_pig_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "personal_conformance.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = PersonalConformanceService(trace_service=trace_service)
    contract, _ = service.register_default_rules()
    run = service.start_run(contract_id=contract.contract_id, target_kind="manual")
    finding = service.record_finding(
        run_id=run.run_id,
        rule_type="canonical_import_disabled",
        status="passed",
        message="Dummy candidate remains staged.",
    )
    service.record_result(
        run_id=run.run_id,
        contract_id=contract.contract_id,
        findings=[finding],
    )
    service.complete_run(run)

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    for object_type in [
        "personal_conformance_contract",
        "personal_conformance_rule",
        "personal_conformance_run",
        "personal_conformance_finding",
        "personal_conformance_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    assert {
        "personal_conformance_contract_registered",
        "personal_conformance_rule_registered",
        "personal_conformance_run_started",
        "personal_conformance_finding_recorded",
        "personal_conformance_result_recorded",
        "personal_conformance_run_completed",
    }.issubset(activities)

    view = OCPXLoader(store=store).load_recent_view(limit=100)
    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))
    summary = PIGReportService._persona_summary(
        report_service.ocpx_engine.count_objects_by_type(view),
        report_service.ocpx_engine.count_events_by_activity(view),
        view,
    )
    assert summary["personal_conformance_contract_count"] == 1
    assert summary["personal_conformance_rule_count"] >= 18
    assert summary["personal_conformance_passed_count"] == 1
    assert summary["personal_conformance_by_rule_type"]["canonical_import_disabled"] == 1
