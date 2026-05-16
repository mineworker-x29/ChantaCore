from pathlib import Path

from chanta_core.self_awareness import (
    SELF_AWARENESS_OCEL_EVENT_TYPES,
    SELF_AWARENESS_OCEL_OBJECT_TYPES,
    SELF_AWARENESS_OCEL_RELATION_TYPES,
    SelfAwarenessWorkbenchRequest,
    SelfAwarenessWorkbenchService,
)


def test_workbench_does_not_mutate_or_execute() -> None:
    snapshot = SelfAwarenessWorkbenchService().build_snapshot(SelfAwarenessWorkbenchRequest())

    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.safety_boundary.write_enabled_count == 0
    assert snapshot.safety_boundary.shell_enabled_count == 0
    assert snapshot.safety_boundary.network_enabled_count == 0
    assert snapshot.safety_boundary.mcp_enabled_count == 0
    assert snapshot.safety_boundary.plugin_enabled_count == 0
    assert snapshot.safety_boundary.external_harness_enabled_count == 0
    assert snapshot.safety_boundary.memory_mutation_enabled_count == 0
    assert snapshot.safety_boundary.persona_mutation_enabled_count == 0
    assert snapshot.safety_boundary.overlay_mutation_enabled_count == 0
    assert snapshot.candidate_queue.promoted_count == 0
    assert snapshot.candidate_queue.materialized_count == 0


def test_workbench_ocel_mapping_contains_read_model_types() -> None:
    for object_type in [
        "self_awareness_workbench_snapshot",
        "self_awareness_coverage_row",
        "self_awareness_safety_boundary_status",
        "self_awareness_candidate_queue_view",
        "self_awareness_verification_queue_view",
        "self_awareness_envelope_view",
        "self_awareness_workbench_finding",
        "pig_report",
        "ocpx_projection",
        "execution_envelope",
    ]:
        assert object_type in SELF_AWARENESS_OCEL_OBJECT_TYPES
    for event_type in [
        "self_awareness_workbench_requested",
        "self_awareness_workbench_snapshot_created",
        "self_awareness_registry_viewed",
        "self_awareness_coverage_viewed",
        "self_awareness_candidates_viewed",
        "self_awareness_verification_viewed",
        "self_awareness_audit_viewed",
        "self_awareness_risks_viewed",
        "self_awareness_pig_status_viewed",
        "self_awareness_ocpx_status_viewed",
        "self_awareness_workbench_warning_created",
        "self_awareness_workbench_violation_detected",
    ]:
        assert event_type in SELF_AWARENESS_OCEL_EVENT_TYPES
    for relation_type in [
        "views_registry",
        "views_coverage",
        "views_candidate_queue",
        "views_verification_queue",
        "views_envelope",
        "views_pig_report",
        "views_ocpx_projection",
        "detects_finding",
        "summarizes_boundary",
        "recorded_in_envelope",
        "derived_from_request",
    ]:
        assert relation_type in SELF_AWARENESS_OCEL_RELATION_TYPES


def test_workbench_runtime_file_avoids_forbidden_calls() -> None:
    text = Path("src/chanta_core/self_awareness/workbench.py").read_text(encoding="utf-8")
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
    for negative_or_counter in [
        "promoted_count",
        "materialized_count",
        "read_only",
        "mutation_performed",
    ]:
        assert negative_or_counter in text


def test_workbench_docs_state_boundaries() -> None:
    text = Path("docs/versions/v0.20/v0.20.8_self_awareness_workbench.md").read_text(encoding="utf-8")

    assert "Self-Awareness Workbench" in text
    assert "자각 워크벤치" in text
    assert "Self-awareness is not self-modification." in text
    assert "Workbench is not execution." in text
    assert "Workbench is not approval." in text
    assert "Workbench is not promotion." in text
    assert "v0.20.9 Self-Awareness Consolidation" in text
