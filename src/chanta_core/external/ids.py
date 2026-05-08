from __future__ import annotations

from uuid import uuid4


def new_external_capability_source_id() -> str:
    return f"external_capability_source:{uuid4()}"


def new_external_capability_descriptor_id() -> str:
    return f"external_capability_descriptor:{uuid4()}"


def new_external_capability_import_batch_id() -> str:
    return f"external_capability_import_batch:{uuid4()}"


def new_external_capability_normalization_id() -> str:
    return f"external_capability_normalization:{uuid4()}"


def new_external_assimilation_candidate_id() -> str:
    return f"external_assimilation_candidate:{uuid4()}"


def new_external_capability_risk_note_id() -> str:
    return f"external_capability_risk_note:{uuid4()}"


def new_external_capability_registry_snapshot_id() -> str:
    return f"external_capability_registry_snapshot:{uuid4()}"


def new_external_adapter_review_queue_id() -> str:
    return f"external_adapter_review_queue:{uuid4()}"


def new_external_adapter_review_item_id() -> str:
    return f"external_adapter_review_item:{uuid4()}"


def new_external_adapter_review_checklist_id() -> str:
    return f"external_adapter_review_checklist:{uuid4()}"


def new_external_adapter_review_finding_id() -> str:
    return f"external_adapter_review_finding:{uuid4()}"


def new_external_adapter_review_decision_id() -> str:
    return f"external_adapter_review_decision:{uuid4()}"


def new_mcp_server_descriptor_id() -> str:
    return f"mcp_server_descriptor:{uuid4()}"


def new_mcp_tool_descriptor_id() -> str:
    return f"mcp_tool_descriptor:{uuid4()}"


def new_plugin_descriptor_id() -> str:
    return f"plugin_descriptor:{uuid4()}"


def new_plugin_entrypoint_descriptor_id() -> str:
    return f"plugin_entrypoint_descriptor:{uuid4()}"


def new_external_descriptor_skeleton_id() -> str:
    return f"external_descriptor_skeleton:{uuid4()}"


def new_external_descriptor_skeleton_validation_id() -> str:
    return f"external_descriptor_skeleton_validation:{uuid4()}"


def new_external_ocel_source_id() -> str:
    return f"external_ocel_source:{uuid4()}"


def new_external_ocel_payload_descriptor_id() -> str:
    return f"external_ocel_payload_descriptor:{uuid4()}"


def new_external_ocel_import_candidate_id() -> str:
    return f"external_ocel_import_candidate:{uuid4()}"


def new_external_ocel_validation_result_id() -> str:
    return f"external_ocel_validation_result:{uuid4()}"


def new_external_ocel_preview_snapshot_id() -> str:
    return f"external_ocel_preview_snapshot:{uuid4()}"


def new_external_ocel_import_risk_note_id() -> str:
    return f"external_ocel_import_risk_note:{uuid4()}"
