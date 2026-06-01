from __future__ import annotations

from pathlib import Path

from chanta_core.public_alpha_schumpeter_preparation import (
    CleanWorktreeReportService,
    ReleaseHygieneGateFindingService,
    ReleaseHygieneGateReportService,
    RuntimeArtifactTrackingReportService,
)


def test_dirty_and_unknown_worktree_do_not_pass_release_claim() -> None:
    unknown = CleanWorktreeReportService().build_report()
    dirty = CleanWorktreeReportService().build_report(worktree_status_known=True, clean_worktree=False)

    assert unknown.worktree_status == "unknown"
    assert unknown.blocks_release_claim is True
    assert dirty.worktree_status == "failed"
    assert dirty.blocks_release_claim is True


def test_tracked_runtime_artifact_blocks_release_claim() -> None:
    report = RuntimeArtifactTrackingReportService().build_report(
        tracked_artifact_refs=[{"object_type": "file", "object_id": "data/runtime.sqlite"}]
    )

    assert report.tracked_artifact_count == 1
    assert report.artifact_status == "failed"
    assert report.blocks_release_claim is True


def test_blocked_finding_catalog_contains_forbidden_gate_actions() -> None:
    assert {
        "auto_fix_attempted",
        "release_tag_creation_attempted",
        "package_publish_attempted",
        "provider_invocation_attempted",
        "command_execution_attempted",
        "schumpeter_split_attempted",
        "external_adapter_attempted",
        "llm_judge_detected",
    } <= ReleaseHygieneGateFindingService.BLOCKED_FINDINGS


def test_v0281_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "public_alpha_schumpeter_preparation.py",
        root / "src" / "chanta_core" / "cli" / "main.py",
        root / "tests" / "test_release_hygiene_repository_governance_gate.py",
        root / "tests" / "test_release_hygiene_repository_governance_gate_boundaries.py",
        root / "docs" / "versions" / "v0.28" / "v0.28.1_release_hygiene_repository_governance_blocking_gate.md",
    ]
    forbidden_names = [
        "auto_fix_performed",
        "license_created",
        "changelog_created",
        "release_tag_created",
        "package_published",
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
        "os" + ".system",
        "shell" + "=True",
        "eval" + "(",
    ]

    assert ReleaseHygieneGateReportService().build_report().auto_fix_performed is False
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert f"{name}=True" not in text
        for marker in forbidden_runtime_markers:
            assert marker not in text
