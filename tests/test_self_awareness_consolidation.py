from chanta_core.cli.main import main
from chanta_core.self_awareness import (
    SelfAwarenessCandidateInventory,
    SelfAwarenessCapabilityMapService,
    SelfAwarenessConsolidationService,
    SelfAwarenessCoverageMatrixService,
    SelfAwarenessGapRegisterService,
    SelfAwarenessReleaseManifestService,
    SelfAwarenessSafetyBoundaryReport,
    SelfAwarenessVerificationSummary,
)
from chanta_core.self_awareness.consolidation import INCLUDED_VERSIONS
from chanta_core.self_awareness.reports import SelfAwarenessReportService


def _service() -> SelfAwarenessConsolidationService:
    service = SelfAwarenessConsolidationService()
    service.consolidate()
    return service


def test_ecosystem_snapshot_and_capability_map_build() -> None:
    service = _service()
    snapshot = service.last_ecosystem_snapshot
    capability_map = service.last_capability_map

    assert snapshot is not None
    assert snapshot.layer == "self_awareness"
    versions = {item.version_introduced for item in snapshot.components}
    for version in [f"v0.20.{index}" for index in range(9)]:
        assert version in versions
    assert snapshot.status == "warning"
    assert snapshot.limitations

    assert capability_map is not None
    skill_ids = {item.skill_id for item in capability_map.capabilities}
    for skill_id in [
        "skill:self_awareness_workspace_inventory",
        "skill:self_awareness_path_verify",
        "skill:self_awareness_text_read",
        "skill:self_awareness_workspace_search",
        "skill:self_awareness_markdown_structure",
        "skill:self_awareness_python_symbols",
        "skill:self_awareness_project_structure",
        "skill:self_awareness_surface_verify",
        "skill:self_awareness_plan_candidate",
        "skill:self_awareness_todo_candidate",
    ]:
        assert skill_id in skill_ids
    by_skill = {item.skill_id: item for item in capability_map.capabilities}
    for skill_id in [
        "skill:self_awareness_config_surface",
        "skill:self_awareness_test_surface",
        "skill:self_awareness_capability_registry",
        "skill:self_awareness_runtime_boundary",
    ]:
        assert by_skill[skill_id].status == "contract_only"
        assert by_skill[skill_id].ocel_visible is True
        assert by_skill[skill_id].pig_visible is True
        assert by_skill[skill_id].ocpx_visible is True
        assert by_skill[skill_id].workbench_visible is True


def test_coverage_matrix_safety_candidate_and_verification_artifacts() -> None:
    service = _service()
    matrix = service.last_coverage_matrix
    safety = service.last_safety_report
    inventory = service.last_candidate_inventory
    verification = service.last_verification_summary

    assert matrix is not None
    assert matrix.coverage_status in {"complete", "partial", "blocked"}
    assert matrix.rows
    for row in matrix.rows:
        assert hasattr(row, "has_model")
        assert hasattr(row, "has_service")
        assert hasattr(row, "has_cli")
        assert hasattr(row, "has_tests")
        assert hasattr(row, "has_ocel_mapping")
        assert hasattr(row, "has_pig_projection")
        assert hasattr(row, "has_ocpx_projection")
        assert hasattr(row, "has_workbench_visibility")
        assert hasattr(row, "has_boundary_tests")

    assert safety is not None
    assert safety.write_enabled_count == 0
    assert safety.shell_enabled_count == 0
    assert safety.network_enabled_count == 0
    assert safety.mcp_enabled_count == 0
    assert safety.plugin_enabled_count == 0
    assert safety.external_harness_enabled_count == 0
    assert safety.memory_mutation_enabled_count == 0
    assert safety.persona_mutation_enabled_count == 0
    assert safety.overlay_mutation_enabled_count == 0
    assert safety.canonical_promotion_enabled_count == 0
    assert safety.materialized_count == 0
    assert safety.dangerous_capability_count == 0
    assert safety.private_boundary_violation_count == 0
    assert safety.raw_secret_exposure_count == 0
    assert safety.status == "passed"

    assert inventory is not None
    assert inventory.promoted_count == 0
    assert inventory.materialized_count == 0
    assert inventory.execution_enabled_count == 0
    assert inventory.status == "ok"
    for field in [
        "summary_candidate_count",
        "project_structure_candidate_count",
        "verification_report_count",
        "plan_candidate_count",
        "todo_candidate_count",
        "no_action_candidate_count",
        "needs_more_input_candidate_count",
        "pending_review_count",
    ]:
        assert hasattr(inventory, field)

    assert verification is not None
    assert verification.status in {"passed", "warning", "failed"}
    assert verification.unresolved_finding_count == 0


def test_gap_register_release_manifest_and_consolidation_report() -> None:
    service = _service()
    gaps = service.last_gap_register
    manifest = service.last_release_manifest
    report = service.last_report

    assert gaps is not None
    required = {
        "config_surface_not_implemented",
        "test_surface_not_implemented",
        "capability_registry_not_implemented",
        "runtime_boundary_not_implemented",
        "write_edit_safety_not_started",
        "shell_execution_safety_not_started",
        "network_mcp_plugin_safety_not_started",
        "external_adapter_implementation_not_started",
        "mission_loop_not_started",
        "growth_kernel_bridge_not_started",
    }
    by_title = {item.title: item for item in gaps.gaps}
    assert required <= set(by_title)
    assert gaps.blocker_count == 0
    assert gaps.future_track_count >= len(required)
    for title in required:
        assert by_title[title].severity == "future_track"
        assert by_title[title].recommended_track
        assert by_title[title].withdrawal_condition

    assert manifest is not None
    assert manifest.release_version == "v0.20.9"
    assert manifest.release_name == "Self-Awareness Foundation v1"
    assert manifest.included_versions == INCLUDED_VERSIONS
    assert {"write", "shell", "network", "MCP", "plugin", "external_harness"} <= set(manifest.excluded_capabilities)
    assert "Self-Modification Safety" in manifest.future_tracks
    assert "Self-Execution Safety" in manifest.future_tracks
    assert "External Contact Safety" in manifest.future_tracks
    assert "External Adapter Implementation" in manifest.future_tracks
    assert "Mission Loop / Self-Directed Operation" in manifest.future_tracks
    assert "GrowthKernel Bridge" in manifest.future_tracks
    assert manifest.release_status == "releasable_with_warnings"

    assert report is not None
    assert report.readiness_status == "warning"
    assert report.readiness_rationale
    assert report.next_track_recommendations
    assert report.withdrawal_conditions
    assert report.validity_horizon


def test_blocking_rules_for_safety_and_candidate_inventory() -> None:
    safety = SelfAwarenessSafetyBoundaryReport(
        report_id="safety:block",
        version="v0.20.9",
        write_enabled_count=0,
        shell_enabled_count=0,
        network_enabled_count=0,
        mcp_enabled_count=0,
        plugin_enabled_count=0,
        external_harness_enabled_count=0,
        memory_mutation_enabled_count=0,
        persona_mutation_enabled_count=0,
        overlay_mutation_enabled_count=0,
        canonical_promotion_enabled_count=0,
        materialized_count=0,
        dangerous_capability_count=1,
        private_boundary_violation_count=0,
        raw_secret_exposure_count=0,
        status="failed",
    )
    gaps = SelfAwarenessGapRegisterService().build_gap_register(safety_report=safety)
    capability_map = SelfAwarenessCapabilityMapService().build_capability_map()
    manifest = SelfAwarenessReleaseManifestService().build_release_manifest(
        capability_map=capability_map,
        safety_report=safety,
        gap_register=gaps,
    )
    assert gaps.blocker_count == 1
    assert manifest.release_status == "blocked"

    inventory = SelfAwarenessCandidateInventory(
        inventory_id="candidate_inventory:bad",
        summary_candidate_count=0,
        project_structure_candidate_count=0,
        verification_report_count=0,
        plan_candidate_count=0,
        todo_candidate_count=0,
        no_action_candidate_count=0,
        needs_more_input_candidate_count=0,
        pending_review_count=0,
        promoted_count=1,
        materialized_count=0,
        execution_enabled_count=0,
        recent_refs=[],
        status="violation",
    )
    assert inventory.status == "violation"


def test_cli_consolidation_commands(capsys) -> None:
    for args in [
        ["self-awareness", "consolidate"],
        ["self-awareness", "release-manifest"],
        ["self-awareness", "gap-register"],
        ["self-awareness", "safety-report"],
        ["self-awareness", "capability-map"],
        ["self-awareness", "coverage-matrix"],
    ]:
        assert main(args) == 0
        output = capsys.readouterr().out
        assert "Self-Awareness Consolidation" in output
        assert "release_status=" in output
        assert "readiness_status=" in output
        assert "dangerous_capability_count=0" in output
        assert "promoted_count=0" in output
        assert "materialized_count=0" in output
        assert "next_track_recommendations=" in output
        assert "no_execution_promotion_materialization_occurred=true" in output
        assert "ChantaResearchGroup" + "_Members" not in output
        assert "raw_file_content_printed=false" in output
        assert "raw_secrets_printed=false" in output


def test_pig_and_ocpx_consolidation_coverage() -> None:
    reports = SelfAwarenessReportService()
    pig = reports.build_pig_report()
    ocpx = reports.build_ocpx_projection()

    assert pig["version"] == "0.20.9"
    assert pig["consolidation"] == "implemented_release_closure"
    assert pig["read_only_self_awareness_v1"] == "warning"
    assert pig["self_modification"] == "not_started"
    assert pig["self_execution"] == "not_started"
    assert pig["external_contact"] == "not_started"
    assert pig["growth_bridge"] == "not_started"
    assert ocpx["state"] == "self_awareness_foundation_v1_consolidated"
    assert ocpx["release_version"] == "v0.20.9"
    assert "consolidation_report" in ocpx["candidate_types"]
    assert "read_only_observation" in ocpx["effect_types"]
    assert "state_candidate_created" in ocpx["effect_types"]
    assert ocpx["release_status"] == "releasable_with_warnings"
