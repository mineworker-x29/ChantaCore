from __future__ import annotations

from uuid import uuid4


def new_session_id() -> str:
    return f"session:{uuid4()}"


def new_conversation_turn_id() -> str:
    return f"conversation_turn:{uuid4()}"


def new_session_message_id() -> str:
    return f"message:{uuid4()}"


def new_session_context_snapshot_id() -> str:
    return f"session_context_snapshot:{uuid4()}"


def new_session_resume_id() -> str:
    return f"session_resume:{uuid4()}"


def new_session_fork_id() -> str:
    return f"session_fork:{uuid4()}"


def new_session_context_policy_id() -> str:
    return f"session_context_policy:{uuid4()}"


def new_session_context_projection_id() -> str:
    return f"session_context_projection:{uuid4()}"


def new_session_prompt_render_id() -> str:
    return f"session_prompt_render:{uuid4()}"
