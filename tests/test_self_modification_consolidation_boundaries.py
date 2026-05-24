from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    SelfModificationConsolidationService,
)


def test_consolidation_ocel_mapping_entries_exist() -> None:
    for object_type in [
        "self_modification_ecosystem_snapshot",
        "self_modification_subject_component",
        "self_modification_capability_map",
        "self_modification_capability_map_entry",
        "self_modification_coverage_matrix",
        "self_modification_coverage_matrix_row",
        "self_modification_safety_boundary_report",
        "self_modification_pipeline_summary",
        "self_modification_authorization_summary",
        "self_modification_change_summary",
        "self_modification_outcome_summary",
        "self_modification_gap_register",
        "self_modification_gap",
        "self_modification_release_manifest",
        "self_modification_consolidation_report",
    ]:
        assert object_type in SELF_MODIFICATION_OCEL_OBJECT_TYPES
    for event_type in [
        "self_modification_consolidation_requested",
        "self_modification_ecosystem_snapshot_created",
        "self_modification_capability_map_created",
        "self_modification_coverage_matrix_created",
        "self_modification_safety_boundary_report_created",
        "self_modification_pipeline_summary_created",
        "self_modification_authorization_summary_created",
        "self_modification_change_summary_created",
        "self_modification_outcome_summary_created",
        "self_modification_gap_register_created",
        "self_modification_release_manifest_created",
        "self_modification_consolidation_report_created",
        "self_modification_release_ready",
        "self_modification_release_warning",
        "self_modification_release_blocked",
    ]:
        assert event_type in SELF_MODIFICATION_OCEL_EVENT_TYPES
    for relation_type in [
        "summarizes_self_modification_subject",
        "maps_self_modification_capability",
        "checks_self_modification_coverage",
        "checks_self_modification_safety_boundary",
        "summarizes_self_modification_pipeline",
        "summarizes_self_modification_authorizations",
        "summarizes_self_modification_changes",
        "summarizes_self_modification_outcomes",
        "registers_self_modification_gap",
        "declares_self_modification_release_manifest",
        "produces_self_modification_consolidation_report",
        "recommends_next_track",
        "blocks_self_modification_release",
        "derived_from_self_modification_workbench",
    ]:
        assert relation_type in SELF_MODIFICATION_OCEL_RELATION_TYPES


def test_consolidation_projection_uses_only_allowed_effects() -> None:
    projection = SelfModificationConsolidationService().build_ocpx_projection()

    assert projection["effect_types"] == ["read_only_observation", "state_candidate_created"]
    assert "workspace_file_changed" not in projection["effect_types"]
    assert "outcome_recorded" not in projection["effect_types"]
    assert "gate_state_created" not in projection["effect_types"]


def test_consolidation_runtime_has_no_mutation_execution_or_llm_judge() -> None:
    source = Path("src/chanta_core/self_modification_safety/consolidation.py").read_text(encoding="utf-8")
    forbidden = [
        "apply_patch(",
        "write_file",
        "pathlib.Path.write_text",
        "pathlib.Path.write_bytes",
        "shutil.move",
        "os.remove",
        "chmod",
        "subprocess",
        "os.system",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "outcome_recorded=True",
        "authorization_consumed=True",
        "rollback_executed=True",
        "shell_executed=True",
        "test_lint_executed=True",
        "file_write_performed=True",
        "mutation_performed=True",
        "additional_file_write_performed=True",
        "exec(",
        "eval(",
    ]

    for token in forbidden:
        assert token not in source

