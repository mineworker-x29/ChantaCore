from __future__ import annotations

from uuid import uuid4


def new_permission_scope_id() -> str:
    return f"permission_scope:{uuid4()}"


def new_permission_request_id() -> str:
    return f"permission_request:{uuid4()}"


def new_permission_decision_id() -> str:
    return f"permission_decision:{uuid4()}"


def new_permission_grant_id() -> str:
    return f"permission_grant:{uuid4()}"


def new_permission_denial_id() -> str:
    return f"permission_denial:{uuid4()}"


def new_permission_policy_note_id() -> str:
    return f"permission_policy_note:{uuid4()}"


def new_session_permission_context_id() -> str:
    return f"session_permission_context:{uuid4()}"


def new_session_permission_snapshot_id() -> str:
    return f"session_permission_snapshot:{uuid4()}"


def new_session_permission_resolution_id() -> str:
    return f"session_permission_resolution:{uuid4()}"
