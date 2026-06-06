from __future__ import annotations

from pathlib import Path

from chanta_core.credential_secret_network_boundary import (
    CredentialNetworkBoundaryFindingService,
    CredentialNetworkBoundaryReportService,
)


def test_v0294_blocked_finding_types_cover_boundary_drift() -> None:
    blocked = CredentialNetworkBoundaryFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "credential_value_detected",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "env_file_creation_attempted",
        "secret_retrieval_attempted",
        "secret_materialization_attempted",
        "network_call_attempted",
        "provider_sdk_invocation_attempted",
        "provider_invocation_attempted",
        "outbound_request_attempted",
        "webhook_attempted",
        "websocket_attempted",
        "command_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
        "live_adapter_implementation_attempted",
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
        "raw_payload_logging_detected",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    ]:
        assert finding_type in blocked


def test_v0294_report_forbidden_flags_remain_false() -> None:
    report = CredentialNetworkBoundaryReportService().build_report()

    forbidden_flags = [
        "ready_for_provider_invocation",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_command_execution",
        "credential_value_present",
        "credential_stored",
        "credential_logged",
        "env_file_created",
        "secret_retrieved",
        "secret_materialized",
        "provider_sdk_invoked",
        "provider_invoked",
        "network_called",
        "outbound_request_sent",
        "command_executed",
        "live_adapter_implemented",
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
        "raw_payload_logged",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in forbidden_flags)
    assert report.ready_for_v0_29_5 is True
    assert report.ready_for_invocation_candidate is True
    assert report.ready_for_dry_run_plan is True
    assert report.policy.no_credential_value_default is True
    assert report.policy.no_network_default is True
    assert report.credential_network_gate.no_credential_value_present is True
    assert report.credential_network_gate.no_network_call is True
    assert report.credential_network_gate.no_provider_sdk_invocation is True


def test_v0294_changed_files_do_not_encode_forbidden_true_flags_or_execution_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "credential_secret_network_boundary.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_credential_secret_network_boundary.py",
        root / "tests" / "test_credential_secret_network_boundary_boundaries.py",
        root / "docs" / "versions" / "v0.29" / "v0.29.4_credential_secret_network_boundary.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "credential_value_present",
        "credential_stored",
        "credential_logged",
        "env_file_created",
        "secret_retrieved",
        "secret_materialized",
        "provider_sdk_invoked",
        "provider_invoked",
        "network_called",
        "outbound_request_sent",
        "webhook_called",
        "websocket_connected",
        "command_executed",
        "shell_execution_surface_created",
        "subprocess_expansion_added",
        "live_adapter_implemented",
        "external_provider_adapter_implemented",
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
        "raw_payload_logged",
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
    assert "open" + "ai" not in combined
    assert "anth" + "ropic" not in combined
    assert "comple" + "tion" not in combined
    assert "chat" + "." + "comple" + "tions" not in combined
    assert "llm_judge" + true_literal not in combined
    assert "llm_judge_used" + true_literal not in combined
    assert "eval" + "(" not in combined
