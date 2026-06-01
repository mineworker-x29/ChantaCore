from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    AlphaReadinessValidationFindingService,
    AlphaReadinessValidationReportService,
)


def test_v0288_blocked_finding_types_cover_validation_and_preflight_drift() -> None:
    blocked = AlphaReadinessValidationFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "public_alpha_release_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "external_adapter_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "network_call_attempted",
        "command_execution_attempted",
        "external_dominion_attempted",
        "RPA_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "schumpeter_private_runtime_attempted",
        "credential_creation_attempted",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "private_material_exposure_detected",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "raw_trace_detected",
        "raw_transcript_detected",
        "raw_provider_output_detected",
        "runtime_continuity_injection_attempted",
        "autonomous_memory_execution_attempted",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    ]:
        assert finding_type in blocked


def test_v0288_report_forbidden_flags_remain_false() -> None:
    report = AlphaReadinessValidationReportService().build_report()

    forbidden_flags = [
        "ready_for_provider_invocation",
        "ready_for_command_execution",
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "official_release_artifact_created",
        "external_adapter_implemented",
        "provider_registered",
        "provider_invoked",
        "network_called",
        "command_executed",
        "external_dominion_implemented",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "schumpeter_private_runtime_used",
        "credential_created",
        "credential_exposed",
        "secret_exposed",
        "private_material_exposed",
        "actual_user_data_used",
        "actual_company_data_used",
        "raw_trace_used",
        "raw_transcript_used",
        "raw_provider_output_used",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in forbidden_flags)
    assert report.ready_for_v0_28_9 is True
    assert report.ready_for_v0_29_contract is True
    assert report.ready_for_public_alpha_release is False
    assert report.ready_for_public_alpha_release_claim is False
    assert report.external_adapter_preflight_report.ready_for_provider_invocation is False
    assert report.external_adapter_preflight_report.ready_for_command_execution is False
    assert report.handoff_packet.refs_only is True
    assert report.handoff_packet.implementation_performed_now is False


def test_v0288_changed_files_do_not_encode_forbidden_true_flags_or_execution_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_alpha_readiness_validation_external_adapter_preflight_gate.py",
        root
        / "tests"
        / "test_alpha_readiness_validation_external_adapter_preflight_gate_boundaries.py",
        root
        / "docs"
        / "versions"
        / "v0.28"
        / "v0.28.8_alpha_readiness_validation_external_adapter_preflight_gate.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "public_alpha_release_implemented",
        "package_published",
        "package_uploaded",
        "release_tag_created",
        "official_release_artifact_created",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "provider_registered",
        "provider_invoked",
        "network_called",
        "command_executed",
        "external_dominion_implemented",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
        "private_config_created",
        "credential_created",
        "credential_exposed",
        "secret_exposed",
        "private_material_exposed",
        "actual_user_data_used",
        "actual_company_data_used",
        "raw_trace_used",
        "raw_transcript_used",
        "raw_provider_output_used",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
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
    assert "eval" + "(" not in combined
