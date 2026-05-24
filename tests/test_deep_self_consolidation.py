from __future__ import annotations

import subprocess
import sys

from chanta_core.deep_self_introspection import (
    CONSOLIDATION_RELEASE_NAME,
    CONSOLIDATION_VERSION,
    DeepSelfConsolidationService,
    DeepSelfCoverageMatrixService,
    DeepSelfIntrospectionCoverageMatrixRow,
    DeepSelfSafetyBoundaryReportService,
)
from chanta_core.deep_self_introspection.consolidation import FUTURE_GAP_DEFINITIONS, FUTURE_TRACKS
from chanta_core.deep_self_introspection.workbench import DeepSelfSafetyBoundaryStatus


def test_deep_self_ecosystem_snapshot_builds() -> None:
    service = DeepSelfConsolidationService()
    report = service.consolidate()
    snapshot = service.last_ecosystem_snapshot

    assert snapshot is not None
    assert snapshot.track == "deep_self_introspection"
    assert snapshot.version == CONSOLIDATION_VERSION
    assert snapshot.release_name == CONSOLIDATION_RELEASE_NAME
    assert report.ecosystem_snapshot_id == snapshot.snapshot_id
    assert {item.version_introduced for item in snapshot.subjects} >= {f"v0.21.{index}" for index in range(9)}
    assert snapshot.limitations


def test_capability_map_includes_all_v021_subjects() -> None:
    service = DeepSelfConsolidationService()
    service.consolidate()
    capability_map = service.last_capability_map

    assert capability_map is not None
    subjects = {item.subject_id for item in capability_map.entries}
    assert {
        "deep_self_contract",
        "capability_truth",
        "runtime_boundary",
        "policy_gate",
        "trace_integrity",
        "context_projection",
        "candidate_memory_boundary",
        "claim_consistency",
        "workbench",
    } <= subjects
    for entry in capability_map.entries:
        assert entry.source_read_models
        assert entry.target_read_models
        assert entry.ocel_visible is True
        assert entry.pig_visible is True
        assert entry.ocpx_visible is True
        assert entry.workbench_visible is True


def test_coverage_matrix_required_columns_and_missing_coverage() -> None:
    service = DeepSelfConsolidationService()
    service.consolidate()
    matrix = service.last_coverage_matrix

    assert matrix is not None
    assert matrix.coverage_status == "complete"
    row = matrix.rows[0]
    assert hasattr(row, "has_contract")
    assert hasattr(row, "has_model")
    assert hasattr(row, "has_service")
    assert hasattr(row, "has_cli")
    assert hasattr(row, "has_tests")
    assert hasattr(row, "has_boundary_tests")
    assert hasattr(row, "has_ocel_mapping")
    assert hasattr(row, "has_pig_projection")
    assert hasattr(row, "has_ocpx_projection")
    assert hasattr(row, "has_workbench_visibility")
    assert hasattr(row, "latest_report_available")

    broken = DeepSelfCoverageMatrixService().build_coverage_matrix()
    broken_row = DeepSelfIntrospectionCoverageMatrixRow(
        subject_id=broken.rows[0].subject_id,
        has_contract=False,
        has_model=True,
        has_service=True,
        has_cli=True,
        has_tests=True,
        has_boundary_tests=True,
        has_ocel_mapping=True,
        has_pig_projection=True,
        has_ocpx_projection=True,
        has_workbench_visibility=True,
        latest_report_available=True,
        coverage_notes=[],
    )
    broken = type(broken)(
        matrix_id=broken.matrix_id,
        rows=[broken_row, *broken.rows[1:]],
        coverage_status="blocked",
        missing_required_coverage_count=1,
        optional_gap_count=0,
    )
    assert broken.coverage_status == "blocked"
    assert broken.missing_required_coverage_count == 1


def test_safety_report_zero_counts_and_blocking_counts() -> None:
    service = DeepSelfSafetyBoundaryReportService()
    report = service.build_safety_report()
    assert report.status == "passed"
    assert report.mutation_enabled_count == 0
    assert report.correction_enabled_count == 0
    assert report.materialization_enabled_count == 0
    assert report.llm_judge_enabled_count == 0

    unsafe = DeepSelfSafetyBoundaryStatus(
        mutation_enabled_count=1,
        permission_grant_enabled_count=0,
        policy_mutation_enabled_count=0,
        registry_mutation_enabled_count=0,
        trace_repair_enabled_count=1,
        context_injection_enabled_count=0,
        memory_promotion_enabled_count=0,
        candidate_promotion_enabled_count=0,
        materialization_enabled_count=0,
        shell_enabled_count=0,
        network_enabled_count=0,
        mcp_enabled_count=0,
        plugin_enabled_count=0,
        external_harness_enabled_count=0,
        llm_judge_enabled_count=1,
        dangerous_capability_count=0,
        status="violation",
    )
    unsafe_report = service.build_safety_report(unsafe)
    assert unsafe_report.status == "failed"
    assert unsafe_report.mutation_enabled_count == 1
    assert unsafe_report.trace_repair_enabled_count == 1
    assert unsafe_report.llm_judge_enabled_count == 1


def test_findings_contradictions_and_gap_register_build() -> None:
    service = DeepSelfConsolidationService()
    service.consolidate()

    findings = service.last_findings_summary
    contradictions = service.last_contradiction_summary
    gaps = service.last_gap_register

    assert findings is not None
    assert contradictions is not None
    assert gaps is not None
    assert findings.total_findings >= findings.open_findings
    assert isinstance(findings.by_subject, dict)
    assert contradictions.open_count >= 0
    expected_gap_ids = {item[0] for item in FUTURE_GAP_DEFINITIONS}
    actual_gap_ids = {item.gap_id for item in gaps.gaps}
    assert expected_gap_ids <= actual_gap_ids
    assert gaps.blocker_count == 0
    assert gaps.future_track_count == len(FUTURE_GAP_DEFINITIONS)
    assert all(item.recommended_track for item in gaps.gaps)
    assert all(item.withdrawal_condition for item in gaps.gaps)


def test_release_manifest_and_readiness() -> None:
    service = DeepSelfConsolidationService()
    report = service.consolidate()
    manifest = service.last_release_manifest

    assert manifest is not None
    assert manifest.release_version == "v0.21.9"
    assert manifest.release_name == CONSOLIDATION_RELEASE_NAME
    assert {f"v0.21.{index}" for index in range(10)} <= set(manifest.included_versions)
    assert {"correction", "promotion", "mutation", "execution", "LLM judge", "external harness"} <= set(manifest.excluded_capabilities)
    assert set(FUTURE_TRACKS) <= set(manifest.future_tracks)
    assert manifest.release_status in {"releasable", "releasable_with_warnings", "blocked"}
    assert report.readiness_status in {"ready", "warning", "blocked"}
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.withdrawal_conditions
    assert report.validity_horizon


def test_pig_and_ocpx_projection_builds() -> None:
    service = DeepSelfConsolidationService()
    service.consolidate()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.21.9"
    assert pig["subject"] == "consolidation"
    assert pig["release_name"] == CONSOLIDATION_RELEASE_NAME
    assert pig["coverage"]["workbench"] == "implemented"
    assert pig["safety_boundary"]["mutation_enabled"] is False
    assert pig["safety_boundary"]["correction_enabled"] is False
    assert pig["safety_boundary"]["promotion_enabled"] is False
    assert pig["safety_boundary"]["materialization_enabled"] is False
    assert pig["safety_boundary"]["execution_enabled"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "deep_self_introspection_foundation_v1_consolidated"
    assert ocpx["release_version"] == "v0.21.9"
    assert "DeepSelfReleaseState" in ocpx["target_read_models"]
    assert "DeepSelfReadinessState" in ocpx["target_read_models"]


def test_deep_self_consolidation_cli_commands() -> None:
    commands = [
        "consolidate",
        "release-manifest",
        "gap-register",
        "safety-report",
        "capability-map",
        "coverage-matrix",
        "findings-summary",
        "contradiction-summary",
    ]
    for command in commands:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "deep-self", command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "release_status=" in completed.stdout
        assert "readiness_status=" in completed.stdout
        assert "No correction performed." in completed.stdout
        assert "No promotion performed." in completed.stdout
        assert "No mutation performed." in completed.stdout
        assert "No execution performed." in completed.stdout
        assert "raw_prompt_body_printed=False" in completed.stdout
        assert "raw_transcript_printed=False" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
