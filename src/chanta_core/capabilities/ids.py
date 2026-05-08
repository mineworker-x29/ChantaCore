from __future__ import annotations

from uuid import uuid4


def new_capability_request_intent_id() -> str:
    return f"capability_request_intent:{uuid4()}"


def new_capability_requirement_id() -> str:
    return f"capability_requirement:{uuid4()}"


def new_capability_decision_id() -> str:
    return f"capability_decision:{uuid4()}"


def new_capability_decision_surface_id() -> str:
    return f"capability_decision_surface:{uuid4()}"


def new_capability_decision_evidence_id() -> str:
    return f"capability_decision_evidence:{uuid4()}"
