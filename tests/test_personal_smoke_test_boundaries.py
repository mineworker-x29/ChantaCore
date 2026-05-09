from pathlib import Path

from chanta_core.persona import PersonalRuntimeSmokeTestService


def test_personal_smoke_test_public_files_do_not_contain_forbidden_terms() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "persona" / "personal_smoke_test.py",
        root / "tests" / "test_personal_smoke_test_models.py",
        root / "tests" / "test_personal_smoke_test_service.py",
        root / "tests" / "test_personal_smoke_test_history_adapter.py",
        root / "tests" / "test_personal_smoke_test_ocel_shape.py",
        root / "tests" / "test_personal_smoke_test_boundaries.py",
        root / "docs" / "chanta_core_v0_16_5_restore.md",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in paths)

    forbidden_fragments = [
        "message_to_" + "future",
        "complete_" + "text",
        "complete_" + "json",
        "Tool" + "Dispatcher",
        "dis" + "patch",
        "sub" + "process",
        "req" + "uests",
        "ht" + "tpx",
        "so" + "cket",
        "connect_" + "mcp",
        "load_" + "plugin",
        "apply_" + "grant",
        "js" + "onl",
    ]

    assert not any(fragment in text for fragment in forbidden_fragments)
    assert "AgentRuntime" + " mode switch" not in text


def test_smoke_test_service_does_not_use_runtime_execution_flags() -> None:
    service = PersonalRuntimeSmokeTestService()
    scenario = service.create_scenario(
        scenario_name="sample_personal_assistant_smoke",
        scenario_type="runtime_binding_boundary",
    )
    case = service.create_case(
        scenario_id=scenario.scenario_id,
        case_name="no_runtime_execution",
        input_prompt="What can you do?",
        expected_behavior="Static output only.",
    )

    result = service.run_cases_against_static_outputs(
        scenario=scenario,
        cases=[case],
        outputs_by_case_id={case.case_id: "Static output only."},
    )

    assert result.result_attrs["model_call_used"] is False
    assert result.result_attrs["tool_execution_used"] is False
    assert result.result_attrs["runtime_activation_used"] is False
    assert result.result_attrs["permission_grants_created"] is False
