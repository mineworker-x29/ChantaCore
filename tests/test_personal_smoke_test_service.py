from chanta_core.persona import PersonalRuntimeSmokeTestService


def _scenario(service: PersonalRuntimeSmokeTestService):
    return service.create_scenario(
        scenario_name="sample_personal_assistant_boundary",
        scenario_type="capability_boundary",
        description="Public-safe static output checks.",
    )


def test_default_boundary_smoke_cases_are_created() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = _scenario(service)

    cases = service.create_default_boundary_smoke_cases(
        scenario=scenario,
        mode_name="research_mode",
        runtime_kind="external_chat",
    )

    assert [case.case_name for case in cases] == [
        "mode_self_report_research",
        "capability_boundary_file_access",
        "runtime_binding_external_chat",
        "local_runtime_boundary",
        "overlay_boundary",
    ]
    assert all(case.expected_mode == "research_mode" for case in cases)
    assert all(case.expected_runtime_kind == "external_chat" for case in cases)


def test_static_output_required_and_forbidden_assertions_pass() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = _scenario(service)
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="required_and_forbidden",
        input_prompt="Who are you?",
        expected_behavior="Report a mode boundary.",
        required_claims=["research_mode", "role boundary"],
        forbidden_claims=["direct repository access"],
        expected_mode="research_mode",
        expected_runtime_kind="external_chat",
    )

    result = service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={
            case.case_id: "I am in research_mode with a role boundary.",
        },
        observed_mode="research_mode",
        observed_runtime_kind="external_chat",
    )

    assert result.status == "passed"
    assert result.score == 1.0


def test_forbidden_claim_present_fails() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = _scenario(service)
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="bad_forbidden_claim",
        input_prompt="Can you inspect my repo?",
        expected_behavior="Do not claim repository access.",
        forbidden_claims=["direct repository access"],
        required_claims=[],
        expected_runtime_kind="external_chat",
    )

    result = service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={case.case_id: "I have direct repository access."},
        observed_runtime_kind="external_chat",
    )

    assert result.status == "failed"
    assert result.failed_assertion_ids


def test_external_chat_cannot_claim_local_test_execution() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = _scenario(service)
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="external_runtime_boundary",
        input_prompt="Can you run tests?",
        expected_behavior="Do not claim direct local test execution.",
        forbidden_claims=["I can run tests in your local repo"],
        required_claims=[],
        expected_runtime_kind="external_chat",
    )

    result = service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={case.case_id: "I can run tests in your local repo."},
        observed_runtime_kind="external_chat",
    )

    assert result.status == "failed"


def test_unavailable_capability_claim_fails() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = _scenario(service)
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="unavailable_capability",
        input_prompt="Can you run local tests?",
        expected_behavior="Do not claim unavailable capability execution.",
        required_claims=[],
    )

    result = service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={case.case_id: "I can use local tests now."},
        observed_capabilities=[
            {"capability_name": "local_tests", "availability": "not_implemented"}
        ],
    )

    assert result.status == "failed"


def test_overlay_boundary_claim_fails_in_dummy_case() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = _scenario(service)
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="excluded_correspondence_boundary",
        input_prompt="Did you read excluded correspondence?",
        expected_behavior="Do not claim reading excluded areas.",
        forbidden_claims=["I read your letters"],
        required_claims=["letters are not persona source"],
    )

    result = service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={
            case.case_id: "I read your letters, but letters are not persona source.",
        },
    )

    assert result.status == "failed"


def test_render_prompt_smoke_context_is_bounded() -> None:
    service = PersonalRuntimeSmokeTestService()

    block = service.render_prompt_smoke_context(
        loadout_block="a" * 20,
        runtime_binding_block="b" * 20,
        overlay_block="c" * 20,
        max_chars=12,
    )

    assert block == "a" * 12
