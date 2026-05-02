from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.ocpx.models import OCPXProcessView
from tests.test_ocel_store import make_record


def test_ocpx_loader_reads_ocel_store(tmp_path) -> None:
    store = OCELStore(tmp_path / "test.sqlite")
    store.append_record(make_record())

    loader = OCPXLoader(store=store)
    view = loader.load_recent_view(limit=20)
    engine = OCPXEngine()
    summary = engine.summarize_view(view)

    assert isinstance(view, OCPXProcessView)
    assert len(view.events) >= 1
    assert summary["event_count"] >= 1
