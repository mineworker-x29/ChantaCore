from __future__ import annotations

from uuid import uuid4


def new_instruction_artifact_id() -> str:
    return f"instruction:{uuid4()}"


def new_project_rule_id() -> str:
    return f"project_rule:{uuid4()}"


def new_user_preference_id() -> str:
    return f"user_preference:{uuid4()}"
