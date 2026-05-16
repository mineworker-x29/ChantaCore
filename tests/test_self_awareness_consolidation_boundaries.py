from pathlib import Path

from chanta_core.self_awareness import (
    SELF_AWARENESS_OCEL_EVENT_TYPES,
    SELF_AWARENESS_OCEL_OBJECT_TYPES,
    SELF_AWARENESS_OCEL_RELATION_TYPES,
    SelfAwarenessConsolidationService,
)


def test_consolidation_does_not_add_execution_or_capability_expansion() -> None:
    service = SelfAwarenessConsolidationService()
    report = service.consolidate()

    assert report.readiness_status == "warning"
    assert service.last_safety_report.write_enabled_count == 0
    assert service.last_safety_report.shell_enabled_count == 0
    assert service.last_safety_report.network_enabled_count == 0
    assert service.last_safety_report.mcp_enabled_count == 0
    assert service.last_safety_report.plugin_enabled_count == 0
    assert service.last_safety_report.external_harness_enabled_count == 0
    assert service.last_safety_report.memory_mutation_enabled_count == 0
    assert service.last_safety_report.persona_mutation_enabled_count == 0
    assert service.last_safety_report.overlay_mutation_enabled_count == 0
    assert service.last_candidate_inventory.promoted_count == 0
    assert service.last_candidate_inventory.materialized_count == 0
    assert service.last_candidate_inventory.execution_enabled_count == 0


def test_consolidation_ocel_mapping_contains_release_types() -> None:
    for object_type in [
        "self_awareness_ecosystem_snapshot",
        "self_awareness_ecosystem_component",
        "self_awareness_capability_map",
        "self_awareness_capability_map_entry",
        "self_awareness_coverage_matrix",
        "self_awareness_coverage_matrix_row",
        "self_awareness_safety_boundary_report",
        "self_awareness_candidate_inventory",
        "self_awareness_verification_summary",
        "self_awareness_gap_register",
        "self_awareness_gap",
        "self_awareness_release_manifest",
        "self_awareness_consolidation_report",
        "self_awareness_workbench_snapshot",
        "execution_envelope",
    ]:
        assert object_type in SELF_AWARENESS_OCEL_OBJECT_TYPES
    for event_type in [
        "self_awareness_consolidation_requested",
        "self_awareness_ecosystem_snapshot_created",
        "self_awareness_capability_map_created",
        "self_awareness_coverage_matrix_created",
        "self_awareness_safety_boundary_report_created",
        "self_awareness_candidate_inventory_created",
        "self_awareness_verification_summary_created",
        "self_awareness_gap_register_created",
        "self_awareness_release_manifest_created",
        "self_awareness_consolidation_report_created",
        "self_awareness_release_ready",
        "self_awareness_release_warning",
        "self_awareness_release_blocked",
    ]:
        assert event_type in SELF_AWARENESS_OCEL_EVENT_TYPES
    for relation_type in [
        "summarizes_component",
        "maps_capability",
        "checks_coverage",
        "checks_safety_boundary",
        "counts_candidates",
        "summarizes_verification",
        "registers_gap",
        "declares_release_manifest",
        "produces_consolidation_report",
        "recommends_next_track",
        "blocks_release",
        "recorded_in_envelope",
        "derived_from_request",
    ]:
        assert relation_type in SELF_AWARENESS_OCEL_RELATION_TYPES


def test_consolidation_runtime_file_avoids_forbidden_calls() -> None:
    text = Path("src/chanta_core/self_awareness/consolidation.py").read_text(encoding="utf-8")
    for forbidden in [
        "apply_patch",
        "write_file",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "exec(",
        "eval(",
        "promoted=True",
        "canonical_promotion_enabled=True",
        "materialized=True",
        "execution_enabled=True",
    ]:
        assert forbidden not in text


def test_consolidation_docs_state_identity_and_boundaries() -> None:
    text = Path("docs/versions/v0.20/v0.20.9_self_awareness_consolidation.md").read_text(encoding="utf-8")

    assert "Self-Awareness Consolidation" in text
    assert "자각 계층 통합 정리" in text
    assert "Self-awareness is not self-modification." in text
    assert "release readiness" in text
    assert "safety closure" in text
    assert "gap registration" in text
    assert "does not add new perception" in text
    assert "Self-Awareness Foundation v1" in text
