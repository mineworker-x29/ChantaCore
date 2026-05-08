from chanta_core.external import ExternalAdapterReviewService, ExternalCapabilityImportService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def _objects(tmp_path):
    trace_service = TraceService(ocel_store=OCELStore(tmp_path / "external_adapter_checklist.sqlite"))
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
    item = review_service.create_review_item(queue_id=queue.queue_id, candidate=candidate)
    return review_service, descriptor, candidate, note, item


def test_disabled_candidate_completes_default_checks(tmp_path) -> None:
    service, descriptor, candidate, note, item = _objects(tmp_path)

    checklist = service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[note],
    )

    assert "candidate_disabled" in checklist.completed_checks
    assert "execution_disabled" in checklist.completed_checks
    assert "risk_notes_reviewed" in checklist.completed_checks
    assert "no_runtime_activation" in checklist.completed_checks
    assert checklist.failed_checks == []
    assert checklist.status == "completed"


def test_execution_enabled_candidate_fails_check_without_mutation(tmp_path) -> None:
    service, descriptor, candidate, note, item = _objects(tmp_path)
    object.__setattr__(candidate, "execution_enabled", True)

    checklist = service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[note],
    )

    assert "execution_disabled" in checklist.failed_checks
    assert candidate.execution_enabled is True


def test_missing_descriptor_fields_fail_descriptor_checks(tmp_path) -> None:
    service, descriptor, candidate, note, item = _objects(tmp_path)
    object.__setattr__(descriptor, "capability_name", "")
    object.__setattr__(descriptor, "capability_type", "")

    checklist = service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[note],
    )

    assert "descriptor_has_name" in checklist.failed_checks
    assert "descriptor_has_type" in checklist.failed_checks
    assert checklist.status == "needs_review"


def test_absent_risk_notes_fail_reviewed_check(tmp_path) -> None:
    service, descriptor, candidate, _, item = _objects(tmp_path)

    checklist = service.build_default_checklist_for_candidate(
        item=item,
        candidate=candidate,
        descriptor=descriptor,
        risk_notes=[],
    )

    assert "risk_notes_reviewed" in checklist.failed_checks
    assert "permissions_declared_or_empty" in checklist.completed_checks
