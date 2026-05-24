from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    SelfContextProjectionAwarenessService,
)


def test_context_projection_ocel_mapping_exists() -> None:
    for object_type in [
        "context_projection",
        "context_projection_snapshot",
        "context_projection_source_ref",
        "context_projection_item",
        "context_projection_budget",
        "context_projection_freshness",
        "context_projection_gap",
        "context_projection_risk_finding",
        "context_projection_truth_report",
        "ocpx_read_model_ref",
        "pig_report_ref",
        "workbench_snapshot_ref",
        "candidate_ref",
        "verification_report_ref",
        "execution_envelope",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES

    for event_type in [
        "deep_self_context_projection_view_requested",
        "deep_self_context_projection_sources_collected",
        "deep_self_context_projection_items_built",
        "deep_self_context_projection_budget_checked",
        "deep_self_context_projection_freshness_checked",
        "deep_self_context_projection_gap_detected",
        "deep_self_context_projection_truth_check_requested",
        "deep_self_context_projection_truth_report_created",
        "deep_self_context_projection_warning_created",
        "deep_self_context_projection_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES

    for relation_type in [
        "views_context_projection",
        "projects_object",
        "projects_event",
        "projects_report",
        "projects_candidate",
        "omits_source",
        "compacts_source",
        "summarizes_source",
        "marks_stale_source",
        "derived_from_ocpx_read_model",
        "derived_from_pig_report",
        "derived_from_workbench_snapshot",
        "contradicts_capability_truth",
        "contradicts_runtime_boundary",
        "contradicts_policy_gate",
        "contradicts_trace_integrity",
        "finds_projection_gap",
        "verified_by_context_projection",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_trace_integrity",
        "derived_from_policy_gate",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES

    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_context_projection_docs_state_boundary_principles() -> None:
    text = Path("docs/versions/v0.21/v0.21.5_self_context_projection_awareness.md").read_text(encoding="utf-8")

    assert "Self-Context Projection Awareness" in text
    assert "Context projection awareness is not context injection." in text
    assert "Projection view is not canonical truth." in text
    assert "Raw transcript is not process-state." in text
    assert "Candidate-only must not appear as canonical memory." in text


def test_context_projection_report_is_read_only_and_non_mutating() -> None:
    service = SelfContextProjectionAwarenessService()
    report = service.truth_check()
    snapshot = service.last_snapshot

    assert snapshot is not None
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.projection_truth_summary["context_injection_performed"] is False
    assert report.projection_truth_summary["memory_promotion_performed"] is False
    assert report.projection_truth_summary["raw_transcript_is_process_state"] is False


def test_runtime_implementation_does_not_call_projection_mutation_or_external_operations() -> None:
    text = Path("src/chanta_core/deep_self_introspection/context_projection.py").read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "inject_context(",
        "modify_prompt(",
        "promote_memory(",
        "memory_auto_promotion(",
        "candidate_promotion(",
        "run_compaction(",
        "compact_conversation(",
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
