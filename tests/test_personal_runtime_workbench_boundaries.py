from pathlib import Path

from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService


def test_personal_runtime_workbench_boundaries_have_no_forbidden_behavior() -> None:
    source = "\n".join(
        path.read_text(encoding="utf-8")
        for path in [
            Path("src/chanta_core/runtime/workbench.py"),
            Path("src/chanta_core/runtime/history_adapter.py"),
            Path("docs/chanta_core_v0_18_5_restore.md"),
        ]
    )
    forbidden = [
        "invoke_explicit_" + "skill(",
        "gate_explicit_" + "invocation(",
        "bridge_reviewed_" + "proposal(",
        "approve_review_" + "automatically",
        "promote_to_" + "memory",
        "update_" + "persona",
        "update_" + "overlay",
        "create_permission_" + "grant",
        "complete_" + "text",
        "complete_" + "json",
        "sub" + "process",
        "os." + "system",
        "re" + "quests",
        "ht" + "tpx",
        "sock" + "et",
        "connect_" + "mcp",
        "load_" + "plugin",
        "write_" + "text",
        "op" + "en(",
        "js" + "onl",
    ]

    for token in forbidden:
        assert token not in source


def test_personal_runtime_workbench_pig_counts_visible() -> None:
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView("personal_runtime_workbench_snapshot:test", "personal_runtime_workbench_snapshot", {}),
            OCPXObjectView("personal_runtime_workbench_panel:test", "personal_runtime_workbench_panel", {}),
            OCPXObjectView("personal_runtime_workbench_pending_item:test", "personal_runtime_workbench_pending_item", {"status": "pending_review", "item_type": "promotion_candidate"}),
            OCPXObjectView("personal_runtime_workbench_recent_activity:test", "personal_runtime_workbench_recent_activity", {"blocked": True, "failed": True}),
            OCPXObjectView("personal_runtime_workbench_result:test", "personal_runtime_workbench_result", {"command_name": "status"}),
        ],
    )

    summary = PIGReportService._personal_runtime_workbench_summary({}, {}, view)

    assert summary["personal_runtime_workbench_snapshot_count"] == 1
    assert summary["personal_runtime_workbench_pending_review_count"] == 1
    assert summary["personal_runtime_workbench_blocked_activity_count"] == 1
    assert summary["personal_runtime_workbench_candidate_count"] == 1
    assert summary["personal_runtime_workbench_by_command"] == {"status": 1}
