from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    AlphaDocumentationFindingService,
    AlphaDocumentationReadinessReportService,
)


def test_v0287_blocked_finding_types_cover_documentation_drift() -> None:
    blocked = AlphaDocumentationFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "production_runtime_overclaim_detected",
        "public_alpha_release_overclaim_detected",
        "provider_invocation_overclaim_detected",
        "command_execution_expansion_overclaim_detected",
        "external_adapter_overclaim_detected",
        "schumpeter_runtime_overclaim_detected",
        "private_material_exposure_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "raw_trace_exposure_detected",
        "raw_transcript_exposure_detected",
        "raw_provider_output_exposure_detected",
        "actual_user_data_example_detected",
        "actual_company_data_example_detected",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "network_call_attempted",
        "runtime_continuity_injection_attempted",
        "external_adapter_attempted",
        "RPA_adapter_attempted",
        "llm_judge_detected",
    ]:
        assert finding_type in blocked


def test_v0287_report_forbidden_flags_remain_false() -> None:
    report = AlphaDocumentationReadinessReportService().build_report()

    forbidden_flags = [
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "production_runtime_claimed",
        "provider_invocation_documented_as_enabled",
        "command_execution_expansion_documented_as_enabled",
        "external_adapter_documented_as_enabled",
        "RPA_adapter_documented_as_enabled",
        "schumpeter_private_runtime_documented_as_enabled",
        "actual_user_data_used",
        "actual_company_data_used",
        "private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "provider_invoked",
        "command_executed",
        "network_called",
        "runtime_continuity_injected",
        "external_adapter_implemented",
        "references_runtime_dependency_added",
        "references_code_copied",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in forbidden_flags)
    assert report.handoff_packet.refs_only is True
    assert report.handoff_packet.implementation_performed_now is False
    assert report.example_pack_manifest.contains_private_data is False
    assert report.synthetic_example_bundle.synthetic_only is True


def test_v0287_changed_files_do_not_encode_forbidden_true_flags_or_execution_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_alpha_documentation_onboarding_example_pack.py",
        root / "tests" / "test_alpha_documentation_onboarding_example_pack_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.7_alpha_documentation_onboarding_example_pack.md",
        root / "docs" / "QUICKSTART.md",
        root / "docs" / "ARCHITECTURE.md",
        root / "docs" / "SAFETY_BOUNDARIES.md",
        root / "docs" / "PUBLIC_PRIVATE_BOUNDARY.md",
        root / "docs" / "WORKBENCH_FOUNDATION.md",
        root / "docs" / "MEMORY_FOUNDATION.md",
        root / "docs" / "PUBLIC_ALPHA_RUNTIME_PROFILE.md",
        root / "docs" / "SMOKE_DEMO_FLOW.md",
        root / "docs" / "CLI_REFERENCE.md",
        root / "docs" / "EXAMPLES.md",
        root / "docs" / "SCHUMPETER_PREPARATION.md",
        root / "docs" / "EXTERNAL_ADAPTER_FUTURE_TRACK.md",
        root / "docs" / "ONBOARDING_CHECKLIST.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "official_release_artifact_created",
        "production_runtime_claimed",
        "provider_invocation_documented_as_enabled",
        "command_execution_expansion_documented_as_enabled",
        "external_adapter_documented_as_enabled",
        "RPA_adapter_documented_as_enabled",
        "schumpeter_private_runtime_documented_as_enabled",
        "actual_user_data_used",
        "actual_company_data_used",
        "private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "provider_invoked",
        "command_executed",
        "network_called",
        "runtime_continuity_injected",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "references_runtime_dependency_added",
        "references_code_copied",
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
