from chanta_core.runtime.workbench import (
    PersonalRuntimeWorkbenchFinding,
    PersonalRuntimeWorkbenchPanel,
    PersonalRuntimeWorkbenchPendingItem,
    PersonalRuntimeWorkbenchRecentActivity,
    PersonalRuntimeWorkbenchResult,
    PersonalRuntimeWorkbenchSnapshot,
)
from chanta_core.utility.time import utc_now_iso


def test_personal_runtime_workbench_models_to_dict() -> None:
    now = utc_now_iso()
    snapshot = PersonalRuntimeWorkbenchSnapshot(
        "personal_runtime_workbench_snapshot:test",
        False,
        None,
        None,
        None,
        "inactive",
        "not_run",
        "not_run",
        1,
        2,
        3,
        4,
        5,
        6,
        7,
        now,
    )
    panel = PersonalRuntimeWorkbenchPanel("personal_runtime_workbench_panel:test", snapshot.snapshot_id, "status", "Status", "ok", 1, "summary", now)
    pending = PersonalRuntimeWorkbenchPendingItem("personal_runtime_workbench_pending_item:test", snapshot.snapshot_id, "skill_invocation_proposal", "ref", "Pending", "pending_review", "medium", "reason", now)
    recent = PersonalRuntimeWorkbenchRecentActivity("personal_runtime_workbench_recent_activity:test", snapshot.snapshot_id, "execution_envelope", "ref", "Recent", "blocked", True, False, "skill:read_workspace_text_file", now)
    finding = PersonalRuntimeWorkbenchFinding("personal_runtime_workbench_finding:test", snapshot.snapshot_id, "missing_personal_directory", "warning", "medium", "message", None, now)
    result = PersonalRuntimeWorkbenchResult("personal_runtime_workbench_result:test", snapshot.snapshot_id, "status", "needs_review", [panel.panel_id], [pending.pending_item_id], [recent.activity_id], [finding.finding_id], "summary", now)

    assert snapshot.to_dict()["snapshot_id"] == snapshot.snapshot_id
    assert panel.to_dict()["panel_type"] == "status"
    assert pending.to_dict()["status"] == "pending_review"
    assert recent.to_dict()["blocked"] is True
    assert finding.to_dict()["finding_type"] == "missing_personal_directory"
    assert result.to_dict()["command_name"] == "status"
