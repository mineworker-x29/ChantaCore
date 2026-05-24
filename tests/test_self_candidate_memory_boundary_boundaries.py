from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    CandidateMemoryBoundarySourceService,
    SelfCandidateMemoryBoundaryAwarenessService,
)


def test_candidate_memory_boundary_ocel_mapping_exists() -> None:
    for object_type in [
        "candidate_memory_boundary",
        "candidate_memory_boundary_snapshot",
        "candidate_memory_boundary_report",
        "candidate_memory_boundary_finding",
        "candidate_state_descriptor",
        "candidate_memory_boundary_source_ref",
        "memory_boundary_descriptor",
        "persona_overlay_boundary_descriptor",
        "promotion_boundary_descriptor",
        "materialization_boundary_descriptor",
        "candidate_ref",
        "memory_entry_ref",
        "persona_ref",
        "overlay_ref",
        "context_projection_item",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES

    for event_type in [
        "deep_self_candidate_memory_boundary_view_requested",
        "deep_self_candidate_memory_sources_collected",
        "deep_self_candidate_inventory_checked",
        "deep_self_promotion_boundary_checked",
        "deep_self_materialization_boundary_checked",
        "deep_self_memory_boundary_checked",
        "deep_self_persona_overlay_boundary_checked",
        "deep_self_candidate_memory_boundary_report_created",
        "deep_self_candidate_memory_boundary_warning_created",
        "deep_self_candidate_memory_boundary_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES

    for relation_type in [
        "checks_candidate_boundary",
        "checks_memory_boundary",
        "checks_promotion_boundary",
        "checks_materialization_boundary",
        "checks_persona_overlay_boundary",
        "candidate_derived_from_source",
        "candidate_has_evidence",
        "candidate_not_promoted",
        "candidate_not_materialized",
        "candidate_not_memory",
        "violates_promotion_boundary",
        "violates_materialization_boundary",
        "violates_memory_boundary",
        "violates_persona_overlay_boundary",
        "finds_candidate_memory_confusion",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_context_projection",
        "derived_from_trace_integrity",
        "derived_from_policy_gate",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES

    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_candidate_memory_boundary_docs_state_boundary_principles() -> None:
    text = Path("docs/versions/v0.21/v0.21.6_self_candidate_memory_boundary_awareness.md").read_text(encoding="utf-8")

    assert "Self-Candidate/Memory Boundary Awareness" in text
    assert "Candidate is not memory." in text
    assert "Report is not canonical truth." in text
    assert "Projection is not promotion." in text
    assert "Candidate creation is not materialization." in text


def test_candidate_memory_boundary_report_is_read_only_and_non_mutating() -> None:
    service = SelfCandidateMemoryBoundaryAwarenessService()
    report = service.truth_check()
    snapshot = service.last_snapshot

    assert snapshot is not None
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.boundary_summary["memory_write_enabled"] is False
    assert report.boundary_summary["memory_auto_promotion_enabled"] is False
    assert report.boundary_summary["persona_mutation_enabled"] is False
    assert report.boundary_summary["overlay_mutation_enabled"] is False


def test_unavailable_source_blocks_without_private_material_probe() -> None:
    service = SelfCandidateMemoryBoundaryAwarenessService(
        source_service=CandidateMemoryBoundarySourceService(source_available=False)
    )
    report = service.truth_check()

    assert report.status == "blocked"
    assert any(item.finding_type == "source_unavailable" for item in report.findings)


def test_runtime_implementation_does_not_call_promotion_mutation_or_materialization_operations() -> None:
    text = Path("src/chanta_core/deep_self_introspection/candidate_memory_boundary.py").read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "promote_candidate(",
        "promote_memory(",
        "create_memory_entry(",
        "update_memory(",
        "persona_update(",
        "overlay_update(",
        "materialize(",
        "create_todo(",
        "inject_context(",
        "modify_prompt(",
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
    for token in forbidden_call_tokens:
        assert token not in text
