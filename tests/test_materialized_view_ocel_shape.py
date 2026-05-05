from chanta_core.materialized_views import (
    MaterializedViewInputSnapshot,
    MaterializedViewService,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_refresh_default_views_records_materialized_view_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "materialized_views.sqlite")
    service = MaterializedViewService(
        trace_service=TraceService(ocel_store=store),
        root=tmp_path / "views",
    )

    service.refresh_default_views(MaterializedViewInputSnapshot())

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    view_objects = store.fetch_objects_by_type("materialized_view")

    assert "materialized_view_refresh_started" in activities
    assert "materialized_view_rendered" in activities
    assert "materialized_view_written" in activities
    assert "materialized_view_refresh_completed" in activities
    assert view_objects
    assert all(item["object_attrs"].get("canonical") is False for item in view_objects)
