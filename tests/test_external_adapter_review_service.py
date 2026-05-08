from chanta_core.external import ExternalAdapterReviewService, ExternalCapabilityImportService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _flow(tmp_path):
    store = OCELStore(tmp_path / "external_adapter_review.sqlite")
    trace_service = TraceService(ocel_store=store)
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    review_service = ExternalAdapterReviewService(trace_service=trace_service)
    source = import_service.register_source(
        source_name="provided dict",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_file_writer",
            "type": "tool",
            "permissions": ["write_file", "shell"],
            "risks": ["filesystem_write", "shell_execution"],
        },
        source=source,
    )
    risk_note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=normalization.normalized_risk_categories,
        message="Review.",
    )
    return store, review_service, descriptor, candidate, risk_note


def test_external_adapter_review_service_records_flow(tmp_path) -> None:
    store, service, descriptor, candidate, risk_note = _flow(tmp_path)

    queue = service.create_review_queue(queue_name="external review")
    item = service.create_review_item(
        queue_id=queue.queue_id,
        candidate=candidate,
        risk_note_ids=[risk_note.risk_note_id],
    )
    assigned = service.assign_review_item(item=item, assigned_reviewer="reviewer", reason="manual")
    in_review = service.update_review_item_status(item=assigned, review_status="in_review", reason="start")
    checklist = service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[risk_note],
    )
    updated_checklist = service.update_checklist(checklist=checklist, status="completed", reason="verified")
    finding = service.record_finding(
        item_id=item.item_id,
        finding_type="risk",
        message="High-risk candidate.",
        severity="high",
        source_kind="risk_note",
        source_ref=risk_note.risk_note_id,
    )
    resolved = service.resolve_finding(finding=finding, status="resolved", reason="documented")
    decision = service.record_decision(
        item=item,
        decision="approved_for_design",
        decided_by="reviewer",
        decision_reason="Design only.",
        finding_ids=[finding.finding_id],
        checklist_id=updated_checklist.checklist_id,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "external_adapter_review_queue_created",
        "external_adapter_review_item_created",
        "external_adapter_review_item_assigned",
        "external_adapter_review_item_status_updated",
        "external_adapter_review_checklist_created",
        "external_adapter_review_checklist_updated",
        "external_adapter_review_finding_recorded",
        "external_adapter_review_finding_resolved",
        "external_adapter_review_decision_recorded",
        "external_adapter_review_decision_marked_non_activating",
    }.issubset(activities)
    assert in_review.review_status == "in_review"
    assert resolved.status == "resolved"
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
    assert decision.activation_allowed is False
    assert decision.runtime_registration_allowed is False
    assert decision.execution_enabled_after_decision is False


def test_approved_for_design_does_not_activate_candidate(tmp_path) -> None:
    _, service, _, candidate, risk_note = _flow(tmp_path)
    queue = service.create_review_queue(queue_name="external review")
    item = service.create_review_item(
        queue_id=queue.queue_id,
        candidate=candidate,
        risk_note_ids=[risk_note.risk_note_id],
    )

    decision = service.record_decision(item=item, decision="approved_for_design")

    assert decision.decision == "approved_for_design"
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
