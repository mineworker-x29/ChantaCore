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


def new_shell_command_intent_id() -> str:
    return f"shell_command_intent:{uuid4()}"


def new_network_access_intent_id() -> str:
    return f"network_access_intent:{uuid4()}"


def new_shell_network_risk_assessment_id() -> str:
    return f"shell_network_risk_assessment:{uuid4()}"


def new_shell_network_pre_sandbox_decision_id() -> str:
    return f"shell_network_pre_sandbox_decision:{uuid4()}"


def new_shell_network_risk_violation_id() -> str:
    return f"shell_network_risk_violation:{uuid4()}"
