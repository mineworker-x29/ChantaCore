from __future__ import annotations

from uuid import uuid4


def new_session_id() -> str:
    return f"session:{uuid4()}"


def new_conversation_turn_id() -> str:
    return f"conversation_turn:{uuid4()}"


def new_session_message_id() -> str:
    return f"message:{uuid4()}"
