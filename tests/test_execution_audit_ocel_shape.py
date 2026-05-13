from chanta_core.execution.audit import ExecutionAuditService
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from tests.test_execution_audit_service import build_store


def test_execution_audit_ocel_objects_and_events(tmp_path) -> None:
    store, first, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)

    service.show_envelope(first.envelope_id)

    assert store.fetch_objects_by_type("execution_audit_query")
    assert store.fetch_objects_by_type("execution_audit_filter")
    assert store.fetch_objects_by_type("execution_audit_record_view")
    assert store.fetch_objects_by_type("execution_audit_result")
    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert "execution_audit_query_requested" in activities
    assert "execution_audit_record_view_created" in activities
    assert "execution_audit_result_recorded" in activities


def test_execution_audit_pig_counts(tmp_path) -> None:
    store, first, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)
    service.show_envelope(first.envelope_id)
    service.show_envelope("execution_envelope:missing")

    objects = []
    for object_type in [
        "execution_audit_query",
        "execution_audit_filter",
        "execution_audit_record_view",
        "execution_audit_result",
        "execution_audit_finding",
    ]:
        for row in store.fetch_objects_by_type(object_type):
            objects.append(
                OCPXObjectView(
                    object_id=row["object_id"],
                    object_type=row["object_type"],
                    object_attrs=row["object_attrs"],
                )
            )
    summary = PIGReportService._skill_usage_summary(
        OCPXProcessView(view_id="view:test", source="test", session_id=None, events=[], objects=objects)
    )

    assert summary["execution_audit_query_count"] == 2
    assert summary["execution_audit_result_count"] == 2
    assert summary["execution_audit_not_found_count"] == 1
    assert summary["execution_audit_by_query_type"]["show"] == 2
