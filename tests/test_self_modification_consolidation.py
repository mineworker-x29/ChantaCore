from __future__ import annotations

import subprocess
import sys
from types import SimpleNamespace

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_FOUNDATION_RELEASE_NAME,
    SelfModificationConsolidationService,
    SelfModificationWorkbenchService,
    SelfModificationWorkbenchSourceService,
)

from tests.test_self_modification_workbench import _workbench_service


def _consolidation_service(tmp_path, *, include_post_apply: bool = True) -> SelfModificationConsolidationService:
    return SelfModificationConsolidationService(
        workbench_service=_workbench_service(tmp_path, include_post_apply=include_post_apply)
    )


def test_self_modification_consolidation_report_builds(tmp_path) -> None:
    report = _consolidation_service(tmp_path).build_report()

    assert report.ecosystem_snapshot.track == "self_modification_safety"
    assert report.ecosystem_snapshot.release_name == SELF_MODIFICATION_FOUNDATION_RELEASE_NAME
    assert report.release_manifest.release_version == "v0.22.9"
    assert report.release_manifest.release_name == SELF_MODIFICATION_FOUNDATION_RELEASE_NAME
    assert report.review_status == "report_only"
    assert report.mutation_performed is False
    assert report.additional_file_write_performed is False
    assert report.rollback_executed is False
    assert report.shell_executed is False
    assert report.test_lint_executed is False
    assert report.llm_judge_used is False


def test_ecosystem_snapshot_includes_v0_22_subjects(tmp_path) -> None:
    report = _consolidation_service(tmp_path).build_report()
    versions = {item.version_introduced for item in report.ecosystem_snapshot.subject_components}
    subjects = {item.subject_id for item in report.ecosystem_snapshot.subject_components}

    for version in [f"v0.22.{index}" for index in range(0, 9)]:
        assert version in versions
    assert "subject:self_modification_safety_contract" in subjects
    assert "subject:self_modification_workbench" in subjects


def test_capability_map_and_coverage_matrix_cover_required_columns(tmp_path) -> None:
    report = _consolidation_service(tmp_path).build_report()
    capabilities = {item.capability_id for item in report.capability_map.entries}

    for capability in [
        "contract",
        "request_candidate",
        "draft_diff_preview",
        "static_safety",
        "dry_run",
        "human_review_apply_gate",
        "bounded_apply",
        "post_apply_verification_outcome",
        "workbench",
        "consolidation",
    ]:
        assert capability in capabilities
    required_columns = set(report.coverage_matrix.required_columns)
    assert "has_contract" in required_columns
    assert "has_model" in required_columns
    assert "has_service" in required_columns
    assert "has_cli" in required_columns
    assert "has_tests" in required_columns
    assert "has_boundary_tests" in required_columns
    assert "has_ocel_mapping" in required_columns
    assert "has_pig_projection" in required_columns
    assert "has_ocpx_projection" in required_columns
    assert "has_workbench_visibility" in required_columns
    assert "latest_artifact_available" in required_columns


def test_safety_report_allows_traced_bounded_write_and_blocks_unverified_apply(tmp_path) -> None:
    clean_report = _consolidation_service(tmp_path).build_report()
    assert clean_report.safety_boundary_report.bounded_file_write_count == 1
    assert clean_report.safety_boundary_report.unauthorized_write_count == 0
    assert clean_report.safety_boundary_report.workspace_file_changed_without_transaction_count == 0
    assert clean_report.safety_boundary_report.safety_status == "ok"

    blocked_report = _consolidation_service(tmp_path, include_post_apply=False).build_report()
    assert blocked_report.safety_boundary_report.unverified_apply_count == 1
    assert blocked_report.safety_boundary_report.missing_outcome_count == 1
    assert blocked_report.readiness_status == "blocked"


def test_safety_report_blocks_unauthorized_write_and_authorization_reuse() -> None:
    service = SelfModificationConsolidationService(
        workbench_service=SelfModificationWorkbenchService(
            source_service=SelfModificationWorkbenchSourceService(
                authorizations=[
                    SimpleNamespace(
                        authorization_id="apply_gate_authorization:reused",
                        apply_gate_id="apply_gate_state:test",
                        patch_candidate_id="patch_candidate:test",
                        authorized_for_stage="bounded_patch_apply",
                        authorized_next_version="v0.22.6",
                        single_use=True,
                        consumed=True,
                        expired=False,
                        patch_applied=False,
                    )
                ],
                events=[{"event_id": "workspace_file_changed:test", "event_type": "workspace_file_changed"}],
            )
        )
    )

    report = service.build_report()

    assert report.safety_boundary_report.workspace_file_changed_without_transaction_count == 1
    assert report.safety_boundary_report.consumed_authorization_reuse_count == 1
    assert report.readiness_status == "blocked"


def test_pipeline_authorization_change_and_outcome_summaries(tmp_path) -> None:
    report = _consolidation_service(tmp_path).build_report()

    assert report.pipeline_summary.bounded_apply_count == 1
    assert report.pipeline_summary.post_apply_verification_count == 1
    assert report.pipeline_summary.outcome_count == 1
    assert report.pipeline_summary.completed_pipeline_count == 1
    assert report.authorization_summary.consumed_count == 1
    assert report.change_summary.changed_file_count == 1
    assert report.change_summary.verified_change_count == 1
    assert report.outcome_summary.applied_verified_count == 1
    assert report.outcome_summary.missing_outcome_count == 0


def test_gap_register_and_release_manifest_define_future_boundaries(tmp_path) -> None:
    report = _consolidation_service(tmp_path).build_report()
    gap_ids = {item.gap_id for item in report.gap_register.gaps}

    for gap_id in [
        "local_runtime_provider_not_started",
        "test_lint_execution_safety_not_started",
        "rollback_execution_safety_not_started",
        "multi_file_apply_safety_not_started",
        "external_adapter_safety_not_started",
        "autonomous_repair_loop_not_started",
        "memory_promotion_after_modification_not_started",
        "semantic_code_review_not_started",
        "performance_regression_check_not_started",
        "security_scan_execution_not_started",
    ]:
        assert gap_id in gap_ids
    assert all(not item.current_release_blocker for item in report.gap_register.gaps)
    assert "v0.22.0" in report.release_manifest.included_versions
    assert "v0.22.9" in report.release_manifest.included_versions
    assert "test/lint/shell execution" in report.release_manifest.excluded_capabilities
    assert "rollback execution" in report.release_manifest.excluded_capabilities
    assert "LLM judge" in report.release_manifest.excluded_capabilities
    assert "v0.24.x Local Runtime Provider" in report.release_manifest.future_tracks


def test_pig_and_ocpx_reports_use_v0_22_9() -> None:
    service = SelfModificationConsolidationService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.22.9"
    assert pig["subject"] == "consolidation"
    assert pig["release_name"] == SELF_MODIFICATION_FOUNDATION_RELEASE_NAME
    assert pig["coverage"]["consolidation"] == "implemented"
    assert pig["mutation_performed"] is False
    assert pig["additional_file_write_performed"] is False
    assert pig["rollback_executed"] is False
    assert pig["shell_executed"] is False
    assert pig["test_lint_executed"] is False
    assert pig["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_safety_foundation_v1_consolidated"
    assert ocpx["release_version"] == "v0.22.9"
    assert "SelfModificationReleaseState" in ocpx["target_read_models"]
    assert ocpx["effect_types"] == ["read_only_observation", "state_candidate_created"]


def test_consolidation_cli_commands_are_sanitized() -> None:
    for command in [
        "consolidate",
        "release-manifest",
        "gap-register",
        "safety-report",
        "pipeline-summary",
        "authorization-summary",
        "change-summary",
        "outcome-summary",
    ]:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "self-modification", command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "release_status=" in completed.stdout
        assert "readiness_status=" in completed.stdout
        assert "read_only_consolidation=true" in completed.stdout
        assert "mutation_performed=false" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
