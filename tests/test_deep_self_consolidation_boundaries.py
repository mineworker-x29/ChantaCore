from __future__ import annotations

from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_MAPPING,
    DeepSelfConsolidationService,
    DeepSelfIntrospectionCapabilityMap,
    DeepSelfIntrospectionCapabilityMapEntry,
    DeepSelfIntrospectionConsolidationReport,
    DeepSelfIntrospectionContradictionSummary,
    DeepSelfIntrospectionCoverageMatrix,
    DeepSelfIntrospectionCoverageMatrixRow,
    DeepSelfIntrospectionEcosystemSnapshot,
    DeepSelfIntrospectionFindingsSummary,
    DeepSelfIntrospectionGap,
    DeepSelfIntrospectionGapRegister,
    DeepSelfIntrospectionReleaseManifest,
    DeepSelfIntrospectionSafetyBoundaryReport,
    DeepSelfIntrospectionSubjectComponent,
)


def test_consolidation_models_are_exported() -> None:
    exported = [
        DeepSelfIntrospectionEcosystemSnapshot,
        DeepSelfIntrospectionSubjectComponent,
        DeepSelfIntrospectionCapabilityMap,
        DeepSelfIntrospectionCapabilityMapEntry,
        DeepSelfIntrospectionCoverageMatrix,
        DeepSelfIntrospectionCoverageMatrixRow,
        DeepSelfIntrospectionSafetyBoundaryReport,
        DeepSelfIntrospectionFindingsSummary,
        DeepSelfIntrospectionContradictionSummary,
        DeepSelfIntrospectionGapRegister,
        DeepSelfIntrospectionGap,
        DeepSelfIntrospectionReleaseManifest,
        DeepSelfIntrospectionConsolidationReport,
    ]
    assert all(item is not None for item in exported)


def test_docs_define_identity_and_non_goals() -> None:
    doc = Path("docs/versions/v0.21/v0.21.9_deep_self_introspection_consolidation.md").read_text(encoding="utf-8")

    assert "Deep Self-Introspection Consolidation" in doc
    assert "심층 자기 관조 통합 정리" in doc
    assert "OCEL-native Deep Self-Introspection Foundation v1" in doc
    assert "consolidation is not new capability expansion" in doc.lower()
    assert "consolidation is not correction" in doc.lower()
    assert "consolidation is not promotion" in doc.lower()
    assert "consolidation is not execution" in doc.lower()
    assert "v0.22.x Self-Modification Safety" in doc


def test_ocel_mapping_includes_consolidation_types() -> None:
    object_types = {
        "deep_self_ecosystem_snapshot",
        "deep_self_subject_component",
        "deep_self_capability_map",
        "deep_self_capability_map_entry",
        "deep_self_coverage_matrix",
        "deep_self_coverage_matrix_row",
        "deep_self_safety_boundary_report",
        "deep_self_findings_summary",
        "deep_self_contradiction_summary",
        "deep_self_gap_register",
        "deep_self_gap",
        "deep_self_release_manifest",
        "deep_self_consolidation_report",
        "deep_self_workbench_snapshot",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    }
    event_types = {
        "deep_self_consolidation_requested",
        "deep_self_ecosystem_snapshot_created",
        "deep_self_capability_map_created",
        "deep_self_coverage_matrix_created",
        "deep_self_safety_boundary_report_created",
        "deep_self_findings_summary_created",
        "deep_self_contradiction_summary_created",
        "deep_self_gap_register_created",
        "deep_self_release_manifest_created",
        "deep_self_consolidation_report_created",
        "deep_self_release_ready",
        "deep_self_release_warning",
        "deep_self_release_blocked",
    }
    relation_types = {
        "summarizes_deep_self_subject",
        "maps_deep_self_capability",
        "checks_deep_self_coverage",
        "checks_deep_self_safety_boundary",
        "summarizes_deep_self_findings",
        "summarizes_deep_self_contradictions",
        "registers_deep_self_gap",
        "declares_deep_self_release_manifest",
        "produces_deep_self_consolidation_report",
        "recommends_next_track",
        "blocks_deep_self_release",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_deep_self_workbench",
        "derived_from_claim_consistency",
        "derived_from_candidate_memory_boundary",
        "derived_from_context_projection",
        "derived_from_trace_integrity",
        "derived_from_policy_gate",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
    }

    assert object_types <= set(DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES)
    assert event_types <= set(DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES)
    assert relation_types <= set(DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES)
    assert {"read_only_observation", "state_candidate_created"} <= set(DEEP_SELF_INTROSPECTION_EFFECT_TYPES)
    assert "deep_self_consolidation_report" in DEEP_SELF_INTROSPECTION_OCEL_MAPPING.object_types


def test_consolidation_has_no_new_action_side_effects() -> None:
    service = DeepSelfConsolidationService()
    report = service.consolidate()
    safety = service.last_safety_report
    manifest = service.last_release_manifest

    assert safety is not None
    assert manifest is not None
    assert safety.mutation_enabled_count == 0
    assert safety.correction_enabled_count == 0
    assert safety.memory_promotion_enabled_count == 0
    assert safety.candidate_promotion_enabled_count == 0
    assert safety.materialization_enabled_count == 0
    assert safety.shell_enabled_count == 0
    assert safety.network_enabled_count == 0
    assert safety.mcp_enabled_count == 0
    assert safety.plugin_enabled_count == 0
    assert safety.external_harness_enabled_count == 0
    assert safety.llm_judge_enabled_count == 0
    assert safety.dangerous_capability_count == 0
    assert safety.private_boundary_violation_count == 0
    assert safety.raw_secret_exposure_count == 0
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert {"correction", "promotion", "mutation", "execution", "LLM judge"} <= set(manifest.excluded_capabilities)


def test_consolidation_cli_output_is_sanitized() -> None:
    service = DeepSelfConsolidationService()
    service.consolidate()
    rendered = service.render_cli("consolidate")

    assert "private_full_paths_printed=False" in rendered
    assert "raw_prompt_body_printed=False" in rendered
    assert "raw_transcript_printed=False" in rendered
    assert "raw_memory_persona_private_material_printed=False" in rendered
    assert "raw_file_content_printed=False" in rendered
    assert "raw_secrets_printed=False" in rendered


def test_consolidation_runtime_does_not_call_forbidden_operations() -> None:
    runtime = Path("src/chanta_core/deep_self_introspection/consolidation.py").read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "correct_finding(",
        "auto_correct(",
        "resolve_contradiction(",
        "acknowledge_contradiction(",
        "approve(",
        "promote(",
        "promote_candidate(",
        "promote_memory(",
        "memory_write(",
        "create_memory_entry(",
        "update_memory(",
        "persona_update(",
        "overlay_update(",
        "materialize(",
        "create_todo(",
        "task_queue(",
        "scheduler(",
        "inject_context(",
        "modify_prompt(",
        "system_prompt(",
        "prompt_mutation(",
        "repair_trace(",
        "backfill(",
        "rewrite_claim(",
        "modify_response(",
        "apply_patch(",
        "write_file(",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    assert [token for token in forbidden_call_tokens if token in runtime] == []
    assert "jsonl" not in runtime.lower()
