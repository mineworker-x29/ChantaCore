from __future__ import annotations

from pathlib import Path

from chanta_core.mock_adapter_harness_no_network_default import (
    MockAdapterHarnessFindingService,
    MockAdapterHarnessReportService,
)


def test_v0292_blocked_finding_types_cover_mock_harness_drift() -> None:
    blocked = MockAdapterHarnessFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "live_adapter_implementation_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "env_file_creation_attempted",
        "command_execution_attempted",
        "shell_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
        "rpa_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "external_dominion_attempted",
        "schumpeter_private_runtime_attempted",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "private_material_exposure_detected",
        "raw_provider_output_persistence_detected",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    ]:
        assert finding_type in blocked


def test_v0292_report_forbidden_flags_remain_false() -> None:
    report = MockAdapterHarnessReportService().build_report()

    forbidden_flags = [
        "ready_for_live_adapter_implementation",
        "ready_for_provider_registration",
        "ready_for_provider_invocation",
        "ready_for_network_access",
        "ready_for_command_execution",
        "live_adapter_implemented",
        "provider_registered",
        "provider_invoked",
        "provider_sdk_invoked",
        "network_called",
        "command_executed",
        "credential_stored",
        "credential_logged",
        "env_file_created",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "external_dominion_implemented",
        "schumpeter_private_runtime_used",
        "actual_user_data_used",
        "actual_company_data_used",
        "private_material_exposed",
        "raw_provider_output_persisted",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in forbidden_flags)
    assert report.ready_for_v0_29_3 is True
    assert report.ready_for_permission_safety_gate is True
    assert report.policy.no_network_default_required is True
    assert report.mock_harness_gate.no_network_boundary_passed is True
    assert report.mock_harness_gate.provider_sdk_isolation_passed is True
    assert report.mock_harness_gate.credential_free_mock_passed is True


def test_v0292_changed_files_do_not_encode_forbidden_true_flags_or_execution_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "mock_adapter_harness_no_network_default.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_mock_adapter_harness_no_network_default.py",
        root / "tests" / "test_mock_adapter_harness_no_network_default_boundaries.py",
        root / "docs" / "versions" / "v0.29" / "v0.29.2_mock_adapter_harness_no_network_default.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "live_adapter_implemented",
        "external_provider_adapter_implemented",
        "provider_registered",
        "provider_invoked",
        "provider_sdk_invoked",
        "network_called",
        "credential_stored",
        "credential_logged",
        "env_file_created",
        "command_executed",
        "shell_execution_surface_created",
        "subprocess_expansion_added",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "external_dominion_implemented",
        "schumpeter_private_runtime_used",
        "actual_user_data_used",
        "actual_company_data_used",
        "private_material_exposed",
        "raw_provider_output_persisted",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
    ]
    true_literal = "".join(["=", "True"])
    assert all(name + true_literal not in combined for name in forbidden_names)
    assert ".".join(["os", "system"]) not in combined
    assert "shell" + true_literal not in combined
    assert "subprocess" + "." + "run" not in combined
    assert "subprocess" + "." + "Popen" not in combined
    assert "request" + "s" + "." not in combined
    assert "url" + "lib" not in combined
    assert "htt" + "px" not in combined
    assert "llm_judge" + true_literal not in combined
    assert "llm_judge_used" + true_literal not in combined
    assert "eval" + "(" not in combined
