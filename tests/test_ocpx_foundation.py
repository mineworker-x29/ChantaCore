from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.context import PIGContext
from chanta_core.pig.feedback import PIGFeedbackService
from tests.test_ocel_store import make_record


def test_ocpx_loader_reads_ocel_store(tmp_path) -> None:
    store = OCELStore(tmp_path / "test.sqlite")
    store.append_record(make_record())

    loader = OCPXLoader(store=store)
    view = loader.load_recent_view(limit=20)
    engine = OCPXEngine()
    summary = engine.summarize_view(view)

    assert PIGContext is not None
    assert PIGFeedbackService is not None
    assert isinstance(view, OCPXProcessView)
    assert len(view.events) >= 1
    assert view.events[0].event_activity
    assert isinstance(engine.activity_sequence(view), list)
    assert engine.count_events_by_activity(view)
    assert engine.count_objects_by_type(view)
    assert engine.compute_relation_coverage(view)["events_total"] >= 1
    assert engine.compute_basic_variant(view)["event_count"] >= 1
    assert engine.compute_basic_performance(view)["event_count"] >= 1
    assert engine.summarize_for_pig_context(view)["performance_summary"]
    assert summary["event_count"] >= 1
