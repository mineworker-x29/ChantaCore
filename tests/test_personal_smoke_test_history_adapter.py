from chanta_core.persona import (
    PersonalRuntimeSmokeTestService,
    personal_smoke_test_assertions_to_history_entries,
    personal_smoke_test_results_to_history_entries,
    personal_smoke_test_scenarios_to_history_entries,
)


def test_personal_smoke_test_history_entries_prioritize_failures() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = service.create_scenario(
        scenario_name="sample_personal_assistant_smoke",
        scenario_type="capability_boundary",
    )
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="dummy_case",
        input_prompt="Can you inspect local files?",
        expected_behavior="Do not claim unavailable capabilities.",
        forbidden_claims=["I can read any file"],
    )
    run = service.start_run(scenario=scenario, cases=[case])
    assertion = service.record_assertion(
        run_id=run.run_id,
        case_id=case.case_id,
        assertion_type="forbidden_claim_absent",
        status="failed",
        severity="high",
        message="Forbidden claim present.",
        expected="absent",
        observed="present",
    )
    result = service.record_result(run_id=run.run_id, assertions=[assertion])

    scenario_entries = personal_smoke_test_scenarios_to_history_entries([scenario])
    assertion_entries = personal_smoke_test_assertions_to_history_entries([assertion])
    result_entries = personal_smoke_test_results_to_history_entries([result])

    assert scenario_entries[0].source == "personal_smoke_test"
    assert assertion_entries[0].priority >= 80
    assert result_entries[0].entry_attrs["failed_assertion_count"] == 1
