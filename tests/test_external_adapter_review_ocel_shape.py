from chanta_core.external import ExternalAdapterReviewService, ExternalCapabilityImportService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_external_adapter_review_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_adapter_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    review_service = ExternalAdapterReviewService(trace_service=trace_service)
    descriptor, _, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={"name": "external_tool", "type": "tool", "risks": ["filesystem_write"]},
    )
    note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="medium",
        risk_categories=["filesystem_write"],
        message="Review.",
    )
    queue = review_service.create_review_queue(queue_name="external review")
    item = review_service.create_review_item(
        queue_id=queue.queue_id,
        candidate=candidate,
        risk_note_ids=[note.risk_note_id],
    )
    checklist = review_service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[note],
    )
    finding = review_service.record_finding(
        item_id=item.item_id,
        finding_type="risk",
        message="Risk.",
        severity="medium",
    )
    decision = review_service.record_decision(
        item=item,
        decision="approved_for_design",
        finding_ids=[finding.finding_id],
        checklist_id=checklist.checklist_id,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "external_adapter_review_queue_created",
        "external_adapter_review_item_created",
        "external_adapter_review_checklist_created",
        "external_adapter_review_finding_recorded",
        "external_adapter_review_decision_recorded",
        "external_adapter_review_decision_marked_non_activating",
    }.issubset(activities)
    assert store.fetch_objects_by_type("external_adapter_review_queue")
    assert store.fetch_objects_by_type("external_adapter_review_item")
    assert store.fetch_objects_by_type("external_adapter_review_checklist")
    assert store.fetch_objects_by_type("external_adapter_review_finding")
    assert store.fetch_objects_by_type("external_adapter_review_decision")
    assert store.fetch_object_object_relations_for_object(item.item_id)
    assert store.fetch_object_object_relations_for_object(checklist.checklist_id)
    assert store.fetch_object_object_relations_for_object(finding.finding_id)
    assert store.fetch_object_object_relations_for_object(decision.decision_id)
