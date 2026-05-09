from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.persona import PersonalRuntimeSmokeTestService
from chanta_core.pig.reports import PIGReportService
from chanta_core.traces.trace_service import TraceService


def test_personal_smoke_test_ocel_shape_and_pig_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "personal_smoke_test.sqlite")
    trace_service = TraceService(ocel_store=store)
    service = PersonalRuntimeSmokeTestService(trace_service=trace_service)
    scenario = service.create_scenario(
        scenario_name="sample_personal_assistant_smoke",
        scenario_type="mode_self_report",
    )
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="mode_self_report",
        input_prompt="Who are you?",
        expected_behavior="Report current mode.",
        required_claims=["research_mode"],
        expected_mode="research_mode",
    )
    service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={case.case_id: "research_mode"},
        observed_mode="research_mode",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    for object_type in [
        "personal_smoke_test_scenario",
        "personal_smoke_test_case",
        "personal_smoke_test_run",
        "personal_smoke_test_observation",
        "personal_smoke_test_assertion",
        "personal_smoke_test_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    assert {
        "personal_smoke_test_scenario_created",
        "personal_smoke_test_case_created",
        "personal_smoke_test_run_started",
        "personal_smoke_test_observation_recorded",
        "personal_smoke_test_assertion_recorded",
        "personal_smoke_test_result_recorded",
        "personal_smoke_test_run_completed",
    }.issubset(activities)

    report_service = PIGReportService(ocpx_loader=OCPXLoader(store=store))
    report = report_service.build_recent_report(limit=100)
    summary = report.report_attrs["persona_summary"]

    assert summary["personal_smoke_test_scenario_count"] == 1
    assert summary["personal_smoke_test_case_count"] == 1
    assert summary["personal_smoke_test_run_count"] == 1
    assert summary["personal_smoke_test_result_count"] == 1
    assert summary["personal_smoke_test_passed_count"] == 1
    assert summary["personal_smoke_test_by_scenario_type"]["mode_self_report"] == 1
    assert "Personal Smoke Test objects" in report.report_text
