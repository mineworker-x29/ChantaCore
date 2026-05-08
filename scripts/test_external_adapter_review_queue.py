from pathlib import Path

from chanta_core.external import ExternalAdapterReviewService, ExternalCapabilityImportService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def main() -> None:
    db_path = Path(".pytest-tmp") / "external_adapter_review_queue_script.sqlite"
    trace_service = TraceService(ocel_store=OCELStore(db_path))
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    review_service = ExternalAdapterReviewService(trace_service=trace_service)

    source = import_service.register_source(
        source_name="provided descriptor",
        source_type="provided_dict",
        trust_level="untrusted",
    )
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={
            "name": "external_file_writer",
            "type": "tool",
            "description": "External descriptor imported as metadata only.",
            "permissions": ["write_file", "shell"],
            "risks": ["filesystem_write", "shell_execution"],
            "entrypoint": "external.module:run",
        },
        source=source,
    )
    risk_note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=normalization.normalized_risk_categories,
        message="Review required before design approval.",
    )
    queue = review_service.create_review_queue(queue_name="external adapter review")
    item = review_service.create_review_item(
        queue_id=queue.queue_id,
        candidate=candidate,
        risk_note_ids=[risk_note.risk_note_id],
        priority=80,
    )
    checklist = review_service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[risk_note],
    )
    finding = review_service.record_finding(
        item_id=item.item_id,
        finding_type="risk",
        message="High-risk external adapter candidate requires review.",
        severity="high",
        source_kind="risk_note",
        source_ref=risk_note.risk_note_id,
    )
    decision = review_service.record_decision(
        item=item,
        decision="approved_for_design",
        decided_by="script",
        decision_reason="Design-only approval record.",
        finding_ids=[finding.finding_id],
        checklist_id=checklist.checklist_id,
    )

    print(f"queue_id={queue.queue_id}")
    print(f"item_id={item.item_id} status={item.review_status}")
    print(f"checklist_id={checklist.checklist_id} status={checklist.status}")
    print(f"finding_id={finding.finding_id} severity={finding.severity}")
    print(f"decision_id={decision.decision_id} decision={decision.decision}")
    assert candidate.execution_enabled is False
    assert candidate.activation_status == "disabled"
    assert decision.activation_allowed is False
    assert decision.runtime_registration_allowed is False
    assert decision.execution_enabled_after_decision is False


if __name__ == "__main__":
    main()
