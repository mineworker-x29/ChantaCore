from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    AlphaRuntimeProfileFindingService,
    AlphaRuntimeProfileReportService,
)


def test_v0286_blocked_finding_types_cover_forbidden_runtime_drift() -> None:
    blocked = AlphaRuntimeProfileFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "production_runtime_attempted",
        "public_alpha_release_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "schumpeter_private_runtime_attempted",
        "external_adapter_attempted",
        "RPA_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "network_call_attempted",
        "runtime_continuity_injection_attempted",
        "autonomous_memory_execution_attempted",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "raw_trace_detected",
        "raw_transcript_detected",
        "raw_provider_output_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    ]:
        assert finding_type in blocked


def test_v0286_report_forbidden_flags_remain_false() -> None:
    report = AlphaRuntimeProfileReportService().build_report()

    forbidden_flags = [
        "production_runtime_implemented",
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "official_release_artifact_created",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
        "external_adapter_implemented",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "provider_invoked",
        "command_executed",
        "network_called",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
        "actual_user_data_used",
        "actual_company_data_used",
        "raw_trace_used",
        "raw_transcript_used",
        "raw_provider_output_used",
        "credential_exposed",
        "secret_exposed",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in forbidden_flags)
    assert report.operator_handoff_packet.refs_only is True
    assert report.operator_handoff_packet.implementation_performed_now is False
    assert report.smoke_input_bundle.synthetic_only is True


def test_v0286_changed_files_do_not_encode_forbidden_true_flags_or_execution_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_public_alpha_runtime_profile_smoke_demo_flow.py",
        root / "tests" / "test_public_alpha_runtime_profile_smoke_demo_flow_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.6_public_alpha_runtime_profile_smoke_demo_flow.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "production_runtime_implemented",
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "official_release_artifact_created",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "provider_invoked",
        "command_executed",
        "network_called",
        "file_mutated",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
        "actual_user_data_used",
        "actual_company_data_used",
        "raw_trace_used",
        "raw_transcript_used",
        "raw_provider_output_used",
        "credential_exposed",
        "secret_exposed",
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
