from uuid import uuid4


def new_tool_descriptor_id() -> str:
    return f"tool_descriptor:{uuid4()}"


def new_tool_registry_snapshot_id() -> str:
    return f"tool_registry_snapshot:{uuid4()}"


def new_tool_policy_note_id() -> str:
    return f"tool_policy_note:{uuid4()}"


def new_tool_risk_annotation_id() -> str:
    return f"tool_risk_annotation:{uuid4()}"

