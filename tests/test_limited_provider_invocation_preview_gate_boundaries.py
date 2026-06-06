from __future__ import annotations

from pathlib import Path

from chanta_core.limited_provider_invocation_preview_gate import (
    LimitedProviderInvocationPreviewReportService,
    LimitedPreviewFindingService,
)


def test_blocked_finding_catalog_covers_v0298_withdrawal_conditions() -> None:
    blocked = LimitedPreviewFindingService.BLOCKED_FINDINGS

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
        "live_adapter_implementation_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "live_provider_certification_attempted",
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
    }
    assert expected <= blocked


def test_report_never_marks_preview_execution_or_runtime_readiness() -> None:
    report = LimitedProviderInvocationPreviewReportService().build_report()

    assert report.ready_for_v0_29_9 is True
    assert report.ready_for_v029_consolidation is True
    assert report.ready_for_preview_execution_now is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_command_execution is False
    assert report.preview_gate.ready_for_preview_execution_now is False
    assert report.preview_gate.ready_for_provider_invocation is False
    assert report.preview_gate.ready_for_network_access is False
    assert report.preview_gate.ready_for_credential_access is False
    assert report.preview_gate.ready_for_command_execution is False
    assert report.preview_execution_performed is False
    assert report.provider_registered is False
    assert report.provider_invoked is False
    assert report.provider_sdk_invoked is False
    assert report.network_called is False
    assert report.outbound_request_sent is False
    assert report.credential_accessed is False
    assert report.credential_stored is False
    assert report.credential_logged is False
    assert report.secret_retrieved is False
    assert report.secret_materialized is False
    assert report.command_executed is False
    assert report.external_side_effect_performed is False
    assert report.file_mutated is False
    assert report.rollback_executed is False
    assert report.automatic_retry_performed is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.live_provider_certified is False
    assert report.live_adapter_implemented is False
    assert report.RPA_adapter_implemented is False
    assert report.A360_adapter_implemented is False
    assert report.Brity_adapter_implemented is False
    assert report.UiPath_adapter_implemented is False
    assert report.external_dominion_implemented is False
    assert report.schumpeter_private_runtime_used is False
    assert report.actual_user_data_used is False
    assert report.actual_company_data_used is False
    assert report.private_material_exposed is False
    assert report.raw_provider_output_persisted is False
    assert report.raw_payload_logged is False
    assert report.references_runtime_dependency_added is False
    assert report.references_code_copied is False
    assert report.PIG_execution_authority_enabled is False
    assert report.llm_judge_used is False


def test_v0298_changed_files_do_not_add_forbidden_runtime_surfaces() -> None:
    root = Path(__file__).resolve().parents[1]
    changed_files = [
        root / "src" / "chanta_core" / "limited_provider_invocation_preview_gate.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "docs" / "versions" / "v0.29" / "v0.29.8_limited_provider_invocation_preview_gate.md",
        root / "tests" / "test_limited_provider_invocation_preview_gate.py",
        root / "tests" / "test_limited_provider_invocation_preview_gate_boundaries.py",
    ]
    content = "\n".join(path.read_text(encoding="utf-8") for path in changed_files)

    forbidden_literals = [
        "preview_execution_performed" + "=True",
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
