from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.feedback import PIGFeedbackService
from tests.test_ocel_store import make_record


def test_pig_feedback_service_builds_recent_context(tmp_path) -> None:
    store = OCELStore(tmp_path / "pig_feedback.sqlite")
    store.append_record(make_record())
    service = PIGFeedbackService(ocpx_loader=OCPXLoader(store=store))

    context = service.build_recent_context(limit=20)

    assert context.source == "pig"
    assert context.scope == "recent"
    assert isinstance(context.activity_sequence, list)
    assert context.relation_coverage["events_total"] >= 1
    assert context.basic_variant["event_count"] >= 1
    assert context.performance_summary["event_count"] >= 1
    assert "Process Intelligence Context" in context.context_text
    assert "Relation coverage" in context.context_text
