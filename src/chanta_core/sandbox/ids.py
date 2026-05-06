from __future__ import annotations

from uuid import uuid4


def new_workspace_root_id() -> str:
    return f"workspace_root:{uuid4()}"


def new_workspace_write_boundary_id() -> str:
    return f"workspace_write_boundary:{uuid4()}"


def new_workspace_write_intent_id() -> str:
    return f"workspace_write_intent:{uuid4()}"


def new_workspace_write_sandbox_decision_id() -> str:
    return f"workspace_write_sandbox_decision:{uuid4()}"


def new_workspace_write_sandbox_violation_id() -> str:
    return f"workspace_write_sandbox_violation:{uuid4()}"
