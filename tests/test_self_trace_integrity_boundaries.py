from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    SelfTraceIntegrityAwarenessService,
    TraceIntegritySourceService,
)


def test_trace_integrity_ocel_mapping_exists() -> None:
    for object_type in [
        "trace_integrity_request",
        "trace_integrity_snapshot",
        "trace_integrity_report",
        "trace_integrity_finding",
        "trace_element_ref",
        "envelope_ocel_link_check",
        "event_object_coverage_check",
        "object_relation_integrity_check",
        "candidate_lineage_check",
        "process_chain_integrity_check",
        "ocel_event_ref",
        "ocel_object_ref",
        "ocel_relation_ref",
        "execution_envelope_ref",
        "candidate_ref",
        "process_instance_ref",
        "skill_contract",
        "capability_record",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES

    for event_type in [
        "deep_self_trace_integrity_check_requested",
        "deep_self_trace_sources_collected",
        "deep_self_envelope_ocel_links_checked",
        "deep_self_event_object_coverage_checked",
        "deep_self_object_relation_integrity_checked",
        "deep_self_candidate_lineage_checked",
        "deep_self_process_chain_integrity_checked",
        "deep_self_trace_integrity_report_created",
        "deep_self_trace_integrity_warning_created",
        "deep_self_trace_integrity_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES

    for relation_type in [
        "checks_trace_integrity",
        "checks_envelope_link",
        "checks_event_object_coverage",
        "checks_object_relation_integrity",
        "checks_candidate_lineage",
        "checks_process_chain",
        "links_envelope_to_event",
        "finds_trace_gap",
        "finds_dangling_relation",
        "finds_orphan_event",
        "finds_orphan_object",
        "supports_trace_finding",
        "verified_by_trace_integrity",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_policy_gate",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
        "derived_from_deep_self_contract",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES

    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_trace_integrity_report_is_read_only_and_non_mutating() -> None:
    service = SelfTraceIntegrityAwarenessService(
        source_service=TraceIntegritySourceService(events=[], objects=[], relations=[], envelopes=[], candidates=[])
    )
    report = service.check_trace_integrity()
    snapshot = service.last_snapshot

    assert snapshot is not None
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert report.review_status == "report_only"
    assert report.canonical_promotion_enabled is False
    assert report.promoted is False
    assert report.integrity_summary["no_repair_performed"] is True


def test_trace_integrity_docs_state_boundary_principles() -> None:
    text = Path("docs/versions/v0.21/v0.21.4_self_trace_integrity_awareness.md").read_text(encoding="utf-8")

    assert "Trace integrity awareness is not trace repair." in text
    assert "Missing trace is a finding, not implicit backfill." in text
    assert "OCEL remains canonical." in text


def test_runtime_implementation_does_not_call_repair_or_mutation_operations() -> None:
    text = Path("src/chanta_core/deep_self_introspection/trace_integrity.py").read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "repair_trace(",
        "backfill(",
        "replay_event(",
        "reemit_event(",
        "rewrite_event(",
        "mutate_ocel(",
        "update_relation(",
        "delete_relation(",
        "create_missing_relation(",
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
