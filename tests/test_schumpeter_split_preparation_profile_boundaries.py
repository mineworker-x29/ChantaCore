from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    SchumpeterPreparationFindingService,
    SchumpeterPreparationReportService,
)


def test_v0285_blocked_finding_types_cover_forbidden_implementation_drift() -> None:
    blocked = SchumpeterPreparationFindingService.BLOCKED_FINDINGS

    for finding_type in [
        "actual_split_attempted",
        "company_wrapper_attempted",
        "private_repo_creation_attempted",
        "private_config_creation_attempted",
        "credential_creation_attempted",
        "endpoint_creation_attempted",
        "provider_adapter_creation_attempted",
        "RPA_adapter_creation_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "references_runtime_dependency_attempted",
        "references_code_copy_attempted",
        "file_move_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "runtime_continuity_injection_attempted",
        "company_private_material_exposure_detected",
        "credential_exposure_detected",
        "secret_exposure_detected",
        "raw_trace_exposure_detected",
        "raw_transcript_exposure_detected",
        "raw_provider_output_exposure_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    ]:
        assert finding_type in blocked


def test_v0285_report_forbidden_flags_remain_false() -> None:
    report = SchumpeterPreparationReportService().build_report()

    forbidden_flags = [
        "actual_split_implemented",
        "company_wrapper_implemented",
        "private_repo_created",
        "private_config_created",
        "credential_created",
        "endpoint_created",
        "provider_adapter_created",
        "RPA_adapter_created",
        "A360_adapter_created",
        "Brity_adapter_created",
        "UiPath_adapter_created",
        "references_runtime_dependency_added",
        "references_code_copied",
        "file_moved",
        "package_published",
        "release_tag_created",
        "provider_invoked",
        "command_executed",
        "runtime_continuity_injected",
        "company_private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]
    assert all(getattr(report, flag) is False for flag in forbidden_flags)
    assert report.handoff_packet.refs_only is True
    assert report.overlay_manifest_preview.preview_is_not_file_creation is True
    assert report.overlay_manifest_preview.manifest_file_created_now is False
    assert report.overlay_manifest_preview.private_config_created_now is False


def test_v0285_changed_files_do_not_encode_forbidden_true_flags() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_schumpeter_split_preparation_profile.py",
        root / "tests" / "test_schumpeter_split_preparation_profile_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.5_schumpeter_split_preparation_profile.md",
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in paths if path.exists())

    forbidden_names = [
        "actual_split_implemented",
        "schumpeter_split_implemented",
        "company_wrapper_implemented",
        "private_repo_created",
        "private_config_created",
        "credential_created",
        "endpoint_created",
        "provider_adapter_created",
        "RPA_adapter_created",
        "A360_adapter_created",
        "Brity_adapter_created",
        "UiPath_adapter_created",
        "references_runtime_dependency_added",
        "references_code_copied",
        "file_moved",
        "package_published",
        "release_tag_created",
        "provider_invoked",
        "command_executed",
        "runtime_continuity_injected",
        "company_private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "PIG_execution_authority_enabled",
    ]
    true_literal = "".join(["=", "True"])
    assert all(name + true_literal not in combined for name in forbidden_names)
    assert ".".join(["os", "system"]) not in combined
    assert "shell" + true_literal not in combined
    assert "eval" + "(" not in combined
