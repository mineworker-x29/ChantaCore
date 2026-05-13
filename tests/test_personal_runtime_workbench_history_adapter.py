from chanta_core.runtime.history_adapter import (
    personal_runtime_workbench_findings_to_history_entries,
    personal_runtime_workbench_pending_items_to_history_entries,
    personal_runtime_workbench_recent_activities_to_history_entries,
    personal_runtime_workbench_results_to_history_entries,
    personal_runtime_workbench_snapshots_to_history_entries,
)
from chanta_core.ocel.store import OCELStore
from chanta_core.runtime.workbench import PersonalRuntimeWorkbenchService


def test_personal_runtime_workbench_history_entries(tmp_path) -> None:
    service = PersonalRuntimeWorkbenchService(ocel_store=OCELStore(tmp_path / "history.sqlite"))
    snapshot = service.build_snapshot()
    result = service.record_result(snapshot=snapshot, command_name="status")

    assert personal_runtime_workbench_snapshots_to_history_entries([snapshot])[0].source == "personal_runtime_workbench"
    assert personal_runtime_workbench_results_to_history_entries([result])[0].source == "personal_runtime_workbench"
    assert personal_runtime_workbench_pending_items_to_history_entries(service.last_pending_items) == []
    assert personal_runtime_workbench_recent_activities_to_history_entries(service.last_recent_activities) == []
    assert personal_runtime_workbench_findings_to_history_entries(service.last_findings)[0].source == "personal_runtime_workbench"
