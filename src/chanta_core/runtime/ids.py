from __future__ import annotations

from uuid import uuid4


def _new_id(prefix: str) -> str:
    return f"{prefix}:{uuid4()}"


def new_personal_runtime_workbench_snapshot_id() -> str:
    return _new_id("personal_runtime_workbench_snapshot")


def new_personal_runtime_workbench_panel_id() -> str:
    return _new_id("personal_runtime_workbench_panel")


def new_personal_runtime_workbench_pending_item_id() -> str:
    return _new_id("personal_runtime_workbench_pending_item")


def new_personal_runtime_workbench_recent_activity_id() -> str:
    return _new_id("personal_runtime_workbench_recent_activity")


def new_personal_runtime_workbench_finding_id() -> str:
    return _new_id("personal_runtime_workbench_finding")


def new_personal_runtime_workbench_result_id() -> str:
    return _new_id("personal_runtime_workbench_result")
