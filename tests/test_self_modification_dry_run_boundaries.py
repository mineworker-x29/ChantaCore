from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_EFFECT_TYPES,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    PatchDryRunCheckRequest,
    PatchDryRunReportService,
    PatchDryRunSourceService,
    SelfModificationDryRunService,
)


DOC_FILE = Path("docs/versions/v0.22/v0.22.4_patch_dry_run_applicability_check.md")


def test_v0_22_4_restore_grade_doc_exists_and_states_boundaries() -> None:
    text = DOC_FILE.read_text(encoding="utf-8")
    assert "Patch Dry-run / Applicability Check" in text
    assert "패치 Dry-run·적용가능성 검사" in text
    assert "Patch dry-run is an in-memory applicability check." in text
    assert "Patch dry-run is not file mutation." in text
    assert "Patch dry-run pass is not review approval." in text
    assert "Patch dry-run pass is not apply permission." in text
    assert "v0.22.5 Human Review & Apply Gate" in text
    assert "Restore procedure" in text
    assert "Withdrawal Conditions" in text
    assert "Validity Horizon" in text


def test_dry_run_report_boundary_flags_are_disabled() -> None:
    result = SelfModificationDryRunService(
        report_service=PatchDryRunReportService(
            source_service=PatchDryRunSourceService(allow_synthetic=True)
        )
    ).check_applicability(PatchDryRunCheckRequest())
    report = result.report

    assert report.safe_to_apply is False
    assert report.file_write_enabled is False
    assert report.apply_patch_enabled is False
    assert report.file_write_performed is False
    assert report.patch_applied is False
    assert report.workspace_file_changed_emitted is False
    assert report.shell_executed is False
    assert report.test_lint_executed is False
    assert all(item.file_write_performed is False for item in report.operation_results)
    assert all(item.workspace_file_changed_emitted is False for item in report.operation_results)
    assert all(snapshot.raw_content_emitted is False for snapshot in report.target_snapshots)


def test_dry_run_ocel_mapping_has_no_workspace_file_changed_effect() -> None:
    for object_type in [
        "patch_dry_run_check_request",
        "patch_dry_run_engine_policy",
        "patch_dry_run_target_snapshot",
        "patch_anchor_applicability_check",
        "patch_dry_run_conflict",
        "patch_dry_run_operation_result",
        "patch_applicability_finding",
        "patch_dry_run_report",
        "patch_dry_run_no_action_candidate",
        "patch_dry_run_needs_more_input_candidate",
        "patch_static_safety_report",
        "patch_draft",
        "diff_preview",
        "patch_candidate",
        "modification_request",
        "workspace_file",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    for event_type in [
        "self_modification_dry_run_requested",
        "self_modification_dry_run_sources_collected",
        "self_modification_target_snapshot_collected",
        "self_modification_anchor_applicability_checked",
        "self_modification_operation_simulated_in_memory",
        "self_modification_conflicts_detected",
        "self_modification_dry_run_report_created",
        "self_modification_dry_run_warning_created",
        "self_modification_dry_run_failed",
        "self_modification_dry_run_blocked",
    ]:
        assert event_type in SELF_MODIFICATION_OCEL_EVENT_TYPES
    for relation_type in [
        "checks_patch_applicability",
        "uses_static_safety_report",
        "uses_patch_draft",
        "uses_diff_preview",
        "uses_target_snapshot",
        "checks_anchor_applicability",
        "simulates_operation_in_memory",
        "detects_dry_run_conflict",
        "produces_dry_run_report",
        "eligible_for_human_review",
        "not_safe_to_apply",
        "requires_human_review",
        "requires_apply_gate",
        "requires_rollback_plan",
        "requires_post_apply_verification",
        "not_applied_to_workspace",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_static_safety_report",
        "derived_from_patch_draft",
        "derived_from_diff_preview",
        "derived_from_patch_candidate",
    ]:
        assert relation_type in SELF_MODIFICATION_OCEL_RELATION_TYPES
    assert {"read_only_observation", "state_candidate_created"} <= set(SELF_MODIFICATION_EFFECT_TYPES)
    assert "workspace_file_changed" in SELF_MODIFICATION_EFFECT_TYPES


def test_dry_run_runtime_source_contains_no_forbidden_execution_imports() -> None:
    text = Path("src/chanta_core/self_modification_safety/dry_run.py").read_text(encoding="utf-8")
    forbidden = [
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "Path.write_text",
        "Path.write_bytes",
        "shutil.move",
        "os.remove",
        "chmod",
        "safe_to_apply=True",
        "file_write_performed=True",
        "workspace_file_changed_emitted=True",
        "shell_executed=True",
        "test_lint_executed=True",
    ]
    for token in forbidden:
        assert token not in text
