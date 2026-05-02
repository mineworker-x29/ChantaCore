from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.builder import PIGBuilder
from chanta_core.pig.service import PIGService
from tests.test_ocel_store import make_record


def test_pig_foundation_builds_outputs(tmp_path) -> None:
    store = OCELStore(tmp_path / "test.sqlite")
    store.append_record(make_record())

    loader = OCPXLoader(store=store)
    view = loader.load_recent_view(limit=20)
    graph = PIGBuilder().build_from_ocpx_view(view)
    service_result = PIGService(loader=loader).analyze_recent(limit=20)

    assert graph.nodes
    assert PIGBuilder is not None
    assert PIGService is not None
    assert "event_count" in service_result["guide"]
    assert isinstance(service_result["diagnostics"], list)
    assert isinstance(service_result["recommendations"], list)
