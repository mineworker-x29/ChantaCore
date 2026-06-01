from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    PublicPrivateBoundaryFindingService,
    PublicPrivateBoundaryReportService,
)


def test_public_private_blocked_findings_catalog_contains_forbidden_actions() -> None:
    assert {
        "destructive_redaction_attempted",
        "source_file_deletion_attempted",
        "file_move_attempted",
        "repo_split_attempted",
        "schumpeter_split_attempted",
        "external_adapter_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "runtime_continuity_injection_attempted",
        "llm_judge_detected",
    } <= PublicPrivateBoundaryFindingService.BLOCKED_FINDINGS


def test_public_private_forbidden_action_flags_remain_false() -> None:
    report = PublicPrivateBoundaryReportService().build_report()

    assert report.ready_for_v0_28_4 is True
    assert report.destructive_redaction_performed is False
    assert report.source_file_deleted is False
    assert report.file_moved is False
    assert report.repo_split_performed is False
    assert report.schumpeter_split_implemented is False
    assert report.company_wrapper_implemented is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.external_adapter_implemented is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.runtime_continuity_injected is False
    assert report.references_runtime_dependency_added is False
    assert report.references_code_copied is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.secret_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.llm_judge_used is False


def test_v0283_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_public_private_boundary_redaction_reference_policy.py",
        root / "tests" / "test_public_private_boundary_redaction_reference_policy_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.3_public_private_boundary_redaction_reference_policy.md",
    ]
    forbidden_names = [
        "destructive_redaction_performed",
        "source_file_deleted",
        "file_moved",
        "repo_split_performed",
        "schumpeter_split_implemented",
        "company_wrapper_implemented",
        "package_published",
        "release_tag_created",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "provider_invoked",
        "command_executed",
        "runtime_continuity_injected",
        "references_runtime_dependency_added",
        "references_code_copied",
        "company_private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "PIG_execution_authority_enabled",
    ]
    forbidden_runtime_markers = [
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
