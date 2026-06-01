from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    PackagingFindingService,
    PackagingReadinessReportService,
)


def test_packaging_blocked_findings_catalog_contains_forbidden_actions() -> None:
    assert {
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "official_release_artifact_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "schumpeter_split_attempted",
        "external_adapter_attempted",
        "auto_fix_attempted",
        "llm_judge_detected",
    } <= PackagingFindingService.BLOCKED_FINDINGS


def test_packaging_forbidden_action_flags_remain_false() -> None:
    report = PackagingReadinessReportService().build_report()

    assert report.ready_for_public_alpha_release_claim is False
    assert report.public_alpha_ready is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.official_release_artifact_created is False
    assert report.auto_fix_performed is False
    assert report.schumpeter_split_implemented is False
    assert report.external_adapter_implemented is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.llm_judge_used is False


def test_v0282_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_packaging_distribution_type_boundary.py",
        root / "tests" / "test_packaging_distribution_type_boundary_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.2_packaging_distribution_type_boundary.md",
    ]
    forbidden_names = [
        "package_published",
        "package_uploaded",
        "release_tag_created",
        "official_release_artifact_created",
        "public_alpha_release_implemented",
        "schumpeter_split_implemented",
        "company_wrapper_implemented",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "provider_invoked",
        "command_executed",
        "runtime_continuity_injected",
        "references_schumpeter_runtime_dependency_added",
        "references_schumpeter_code_copied",
        "company_private_material_exposed",
        "credential_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "PIG_execution_authority_enabled",
    ]
    forbidden_runtime_markers = [
        "tw" + "ine",
        "git" + " tag",
        "os" + ".system",
        "shell" + "=True",
        "eval" + "(",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert f"{name}=True" not in text
        for marker in forbidden_runtime_markers:
            assert marker not in text
