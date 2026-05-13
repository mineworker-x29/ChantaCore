from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.workbench import PersonalRuntimeWorkbenchService


def test_personal_runtime_workbench_ocel_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "workbench_ocel.sqlite")
    service = PersonalRuntimeWorkbenchService(ocel_store=store)

    snapshot = service.build_snapshot()
    service.record_result(snapshot=snapshot, command_name="status")

    object_types = {row["object_type"] for row in store.fetch_objects_by_type("personal_runtime_workbench_snapshot")}
    events = {row["event_activity"] for row in store.fetch_recent_events(limit=20)}
    relations = store.fetch_object_object_relations_for_object(snapshot.snapshot_id)

    assert "personal_runtime_workbench_snapshot" in object_types
    assert "personal_runtime_workbench_snapshot_created" in events
    assert "personal_runtime_workbench_result_recorded" in events
    assert relations
