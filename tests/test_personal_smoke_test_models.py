import pytest

from chanta_core.persona import (
    PersonalSmokeTestAssertion,
    PersonalSmokeTestCase,
    PersonalSmokeTestObservation,
    PersonalSmokeTestResult,
    PersonalSmokeTestRun,
    PersonalSmokeTestScenario,
)
from chanta_core.persona.errors import PersonalSmokeTestError
from chanta_core.utility.time import utc_now_iso


def test_personal_smoke_test_models_to_dict() -> None:
    created_at = utc_now_iso()
    scenario = PersonalSmokeTestScenario(
        scenario_id="personal_smoke_test_scenario:test",
        scenario_name="sample_personal_assistant_smoke",
        scenario_type="mode_self_report",
        description="Public-safe smoke scenario.",
        target_mode_profile_id="personal_mode_profile:test",
        target_loadout_id="personal_mode_loadout:test",
        target_runtime_binding_id="personal_runtime_binding:test",
        status="active",
        private=False,
        created_at=created_at,
    )
    case = PersonalSmokeTestCase(
        case_id="personal_smoke_test_case:test",
        scenario_id=scenario.scenario_id,
        case_name="mode_self_report",
        input_prompt="Who are you?",
        expected_behavior="Report mode and boundary.",
        forbidden_claims=["direct repository access"],
        required_claims=["research_mode"],
        expected_mode="research_mode",
        expected_runtime_kind="external_chat",
        created_at=created_at,
    )
    run = PersonalSmokeTestRun(
        run_id="personal_smoke_test_run:test",
        scenario_id=scenario.scenario_id,
        case_ids=[case.case_id],
        status="started",
        started_at=created_at,
        completed_at=None,
    )
    observation = PersonalSmokeTestObservation(
        observation_id="personal_smoke_test_observation:test",
        run_id=run.run_id,
        case_id=case.case_id,
        observed_output="research_mode with role boundary",
        observed_blocks=[{"kind": "loadout", "chars": 10}],
        observed_mode="research_mode",
        observed_runtime_kind="external_chat",
        observed_capabilities=[{"capability_name": "local_tests", "availability": "not_implemented"}],
        created_at=created_at,
    )
    assertion = PersonalSmokeTestAssertion(
        assertion_id="personal_smoke_test_assertion:test",
        run_id=run.run_id,
        case_id=case.case_id,
        assertion_type="required_claim_present",
        status="passed",
        severity="high",
        message="Required claim present.",
        expected="research_mode",
        observed=observation.observed_output,
        created_at=created_at,
    )
    result = PersonalSmokeTestResult(
        result_id="personal_smoke_test_result:test",
        run_id=run.run_id,
        status="passed",
        score=1.0,
        confidence=1.0,
        passed_assertion_ids=[assertion.assertion_id],
        failed_assertion_ids=[],
        warning_assertion_ids=[],
        skipped_assertion_ids=[],
        reason=None,
        created_at=created_at,
    )

    assert scenario.to_dict()["scenario_type"] == "mode_self_report"
    assert case.to_dict()["required_claims"] == ["research_mode"]
    assert run.to_dict()["case_ids"] == [case.case_id]
    assert observation.to_dict()["observed_mode"] == "research_mode"
    assert assertion.to_dict()["status"] == "passed"
    assert result.to_dict()["score"] == 1.0


def test_personal_smoke_test_result_rejects_out_of_range_score() -> None:
    with pytest.raises(PersonalSmokeTestError):
        PersonalSmokeTestResult(
            result_id="personal_smoke_test_result:test",
            run_id="personal_smoke_test_run:test",
            status="error",
            score=1.2,
            confidence=1.0,
            passed_assertion_ids=[],
            failed_assertion_ids=[],
            warning_assertion_ids=[],
            skipped_assertion_ids=[],
            reason="bad score",
            created_at=utc_now_iso(),
        )
