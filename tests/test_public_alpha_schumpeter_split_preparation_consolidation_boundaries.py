from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    V028ConsolidationFindingService,
    V028ConsolidationReportService,
)


def test_v0289_blocked_finding_types_cover_consolidation_drift() -> None:
    blocked = V028ConsolidationFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "public_alpha_release_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "official_release_artifact_attempted",
        "production_runtime_attempted",
        "schumpeter_private_runtime_attempted",
        "company_wrapper_attempted",
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


def test_v0289_report_forbidden_flags_remain_false() -> None:
    report = V028ConsolidationReportService().build_report()

    forbidden_flags = [
        "ready_for_external_adapter_implementation",
        "ready_for_provider_invocation",
        "ready_for_command_execution",
        "public_alpha_release_implemented",
        "package_published",
        "package_uploaded",
        "release_tag_created",
        "official_release_artifact_created",
        "production_runtime_implemented",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
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
    assert report.ready_for_v0_29 is True
    assert report.ready_for_v0_29_contract is True
    assert report.public_alpha_release_ready is False
    assert report.public_alpha_release_claim_allowed is False
    assert report.release_manifest.public_alpha_release_implemented is False
    assert report.external_adapter_contract_handoff_packet.refs_only is True
    assert report.external_adapter_contract_handoff_packet.implementation_performed_now is False
    assert report.audit_trail.raw_content_included is False


def test_v0289_changed_files_do_not_encode_forbidden_true_flags_or_execution_calls() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_public_alpha_schumpeter_split_preparation_consolidation.py",
        root / "tests" / "test_public_alpha_schumpeter_split_preparation_consolidation_boundaries.py",
        root
        / "docs"
        / "versions"
        / "v0.28"
        / "v0.28.9_public_alpha_schumpeter_split_preparation_consolidation.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "public_alpha_release_implemented",
        "package_published",
        "package_uploaded",
        "release_tag_created",
        "official_release_artifact_created",
        "production_runtime_implemented",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
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
