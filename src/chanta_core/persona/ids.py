from __future__ import annotations

from uuid import uuid4


def new_soul_identity_id() -> str:
    return f"soul_identity:{uuid4()}"


def new_persona_profile_id() -> str:
    return f"persona_profile:{uuid4()}"


def new_persona_instruction_artifact_id() -> str:
    return f"persona_instruction_artifact:{uuid4()}"


def new_agent_role_binding_id() -> str:
    return f"agent_role_binding:{uuid4()}"


def new_persona_loadout_id() -> str:
    return f"persona_loadout:{uuid4()}"


def new_persona_projection_id() -> str:
    return f"persona_projection:{uuid4()}"
