from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    SchumpeterSplitDecisionFindingService,
    SchumpeterSplitDecisionReportService,
)


def test_schumpeter_blocked_findings_catalog_contains_forbidden_actions() -> None:
    assert {
        "actual_split_attempted",
        "company_wrapper_attempted",
        "private_repo_creation_attempted",
        "merge_into_public_core_attempted",
        "references_runtime_dependency_attempted",
        "references_code_copy_attempted",
        "file_move_attempted",
        "destructive_redaction_attempted",
        "external_adapter_attempted",
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
    } <= SchumpeterSplitDecisionFindingService.BLOCKED_FINDINGS


def test_schumpeter_forbidden_action_flags_remain_false() -> None:
    report = SchumpeterSplitDecisionReportService().build_report()

    assert report.ready_for_v0_28_5 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.actual_split_implemented is False
    assert report.company_wrapper_implemented is False
    assert report.private_repo_created is False
    assert report.merge_into_public_core_performed is False
    assert report.references_runtime_dependency_added is False
    assert report.references_code_copied is False
    assert report.file_moved is False
    assert report.destructive_redaction_performed is False
    assert report.external_adapter_implemented is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.runtime_continuity_injected is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.secret_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.PIG_execution_authority_enabled is False
    assert report.llm_judge_used is False


def test_v0284_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_schumpeter_split_decision_framework.py",
        root / "tests" / "test_schumpeter_split_decision_framework_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.4_schumpeter_split_decision_framework.md",
    ]
    forbidden_names = [
        "actual_split_implemented",
        "schumpeter_split_implemented",
        "company_wrapper_implemented",
        "private_repo_created",
        "merge_into_public_core_performed",
        "references_runtime_dependency_added",
        "references_code_copied",
        "file_moved",
        "destructive_redaction_performed",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
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
