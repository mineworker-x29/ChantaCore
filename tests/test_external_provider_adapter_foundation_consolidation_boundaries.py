from __future__ import annotations

from pathlib import Path

from chanta_core.external_provider_adapter_foundation_consolidation import (
    V029ConsolidationFindingService,
    V029ConsolidationReportService,
)


def test_blocked_finding_catalog_covers_v0299_withdrawal_conditions() -> None:
    blocked = V029ConsolidationFindingService.BLOCKED_FINDINGS

    expected = {
        "provider_invocation_attempted",
        "provider_registration_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "outbound_request_attempted",
        "credential_access_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "secret_retrieval_attempted",
        "secret_materialization_attempted",
        "command_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
        "external_side_effect_attempted",
        "file_mutation_attempted",
        "rollback_execution_attempted",
        "automatic_retry_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "live_provider_certification_attempted",
        "live_adapter_implementation_attempted",
        "RPA_adapter_attempted",
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
    }
    assert expected <= blocked


def test_consolidation_report_never_marks_runtime_readiness() -> None:
    report = V029ConsolidationReportService().build_report()

    assert report.external_provider_adapter_foundation_ready is True
    assert report.ready_for_v030 is True
    assert report.ready_for_v030_contract is True
    assert report.provider_invocation_runtime_ready is False
    assert report.limited_preview_execution_ready_now is False
    assert report.live_adapter_runtime_ready is False
    assert report.external_agent_dominion_runtime_ready is False
    assert report.adapter_readiness_report.provider_invocation_runtime_ready is False
    assert report.adapter_readiness_report.limited_preview_execution_ready_now is False
    assert report.adapter_readiness_report.live_adapter_runtime_ready is False
    assert report.v030_readiness_report.ready_for_external_agent_dominion_runtime is False
    assert report.v030_readiness_report.ready_for_external_agent_execution is False
    assert report.external_agent_dominion_handoff_packet.refs_only is True
    assert report.external_agent_dominion_handoff_packet.implementation_performed_now is False
    assert report.release_manifest.provider_invocation_enabled is False
    assert report.release_manifest.network_access_enabled is False
    assert report.release_manifest.credential_access_enabled is False
    assert report.release_manifest.command_execution_enabled is False


def test_v0299_changed_files_do_not_add_forbidden_runtime_surfaces() -> None:
    root = Path(__file__).resolve().parents[1]
    changed_files = [
        root / "src" / "chanta_core" / "external_provider_adapter_foundation_consolidation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "docs" / "versions" / "v0.29" / "v0.29.9_external_provider_adapter_foundation_consolidation.md",
        root / "tests" / "test_external_provider_adapter_foundation_consolidation.py",
        root / "tests" / "test_external_provider_adapter_foundation_consolidation_boundaries.py",
    ]
    content = "\n".join(path.read_text(encoding="utf-8") for path in changed_files)

    forbidden_literals = [
        "provider_registered" + "=True",
        "provider_invoked" + "=True",
        "provider_sdk_invoked" + "=True",
        "network_called" + "=True",
        "outbound_request_sent" + "=True",
        "credential_accessed" + "=True",
        "credential_stored" + "=True",
        "credential_logged" + "=True",
        "secret_retrieved" + "=True",
        "secret_materialized" + "=True",
        "command_executed" + "=True",
        "shell_execution_surface_created" + "=True",
        "subprocess_expansion_added" + "=True",
        "external_side_effect_performed" + "=True",
        "file_mutated" + "=True",
        "rollback_executed" + "=True",
        "automatic_retry_performed" + "=True",
        "package_published" + "=True",
        "package_uploaded" + "=True",
        "release_tag_created" + "=True",
        "official_release_artifact_created" + "=True",
        "live_provider_certified" + "=True",
        "live_adapter_implemented" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "RPA_adapter_implemented" + "=True",
        "A360_adapter_implemented" + "=True",
        "Brity_adapter_implemented" + "=True",
        "UiPath_adapter_implemented" + "=True",
        "external_dominion_implemented" + "=True",
        "schumpeter_private_runtime_used" + "=True",
        "actual_user_data_used" + "=True",
        "actual_company_data_used" + "=True",
        "private_material_exposed" + "=True",
        "raw_provider_output_persisted" + "=True",
        "raw_payload_logged" + "=True",
        "references_runtime_dependency_added" + "=True",
        "references_code_copied" + "=True",
        "PIG_execution_authority_enabled" + "=True",
        "os" + ".system",
        "shell" + "=True",
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "requests" + ".",
        "url" + "lib",
        "htt" + "px",
        "open" + "ai",
        "anth" + "ropic",
        "chat" + ".comp" + "letions",
        "llm" + "_judge=True",
        "ev" + "al(",
    ]
    for forbidden in forbidden_literals:
        assert forbidden not in content
