from chanta_core.external import (
    ExternalAdapterReviewService,
    ExternalCapabilityImportService,
    external_adapter_review_decisions_to_history_entries,
    external_adapter_review_findings_to_history_entries,
    external_adapter_review_items_to_history_entries,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_external_adapter_review_history_entries_include_refs(tmp_path) -> None:
    trace_service = TraceService(ocel_store=OCELStore(tmp_path / "external_adapter_history.sqlite"))
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    review_service = ExternalAdapterReviewService(trace_service=trace_service)
    descriptor, _, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={"name": "external_tool", "type": "tool", "risks": ["filesystem_write"]},
    )
    note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=["filesystem_write"],
        message="Review.",
    )
    queue = review_service.create_review_queue(queue_name="external review")
    item = review_service.create_review_item(queue_id=queue.queue_id, candidate=candidate)
    finding = review_service.record_finding(
        item_id=item.item_id,
        finding_type="risk",
        message="Critical risk.",
        severity="critical",
        source_kind="risk_note",
        source_ref=note.risk_note_id,
    )
    decision = review_service.record_decision(
        item=item,
        decision="needs_more_info",
        finding_ids=[finding.finding_id],
    )

    item_entry = external_adapter_review_items_to_history_entries([item])[0]
    finding_entry = external_adapter_review_findings_to_history_entries([finding])[0]
    decision_entry = external_adapter_review_decisions_to_history_entries([decision])[0]

    assert item_entry.source == "external_adapter_review"
    assert item_entry.refs[0]["queue_id"] == queue.queue_id
    assert item_entry.refs[0]["candidate_id"] == candidate.candidate_id
    assert finding_entry.source == "external_adapter_review"
    assert finding_entry.priority >= 90
    assert finding_entry.refs[0]["finding_id"] == finding.finding_id
    assert decision_entry.source == "external_adapter_review"
    assert decision_entry.refs[0]["decision_id"] == decision.decision_id
    assert decision_entry.refs[0]["finding_ids"] == [finding.finding_id]
