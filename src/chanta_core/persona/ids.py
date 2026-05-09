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


def new_persona_source_id() -> str:
    return f"persona_source:{uuid4()}"


def new_persona_source_manifest_id() -> str:
    return f"persona_source_manifest:{uuid4()}"


def new_persona_source_ingestion_candidate_id() -> str:
    return f"persona_source_ingestion_candidate:{uuid4()}"


def new_persona_source_validation_result_id() -> str:
    return f"persona_source_validation_result:{uuid4()}"


def new_persona_assimilation_draft_id() -> str:
    return f"persona_assimilation_draft:{uuid4()}"


def new_persona_projection_candidate_id() -> str:
    return f"persona_projection_candidate:{uuid4()}"


def new_persona_source_risk_note_id() -> str:
    return f"persona_source_risk_note:{uuid4()}"


def new_personal_directory_config_id() -> str:
    return f"personal_directory_config:{uuid4()}"


def new_personal_directory_manifest_id() -> str:
    return f"personal_directory_manifest:{uuid4()}"


def new_personal_overlay_load_request_id() -> str:
    return f"personal_overlay_load_request:{uuid4()}"


def new_personal_projection_ref_id() -> str:
    return f"personal_projection_ref:{uuid4()}"


def new_personal_overlay_load_result_id() -> str:
    return f"personal_overlay_load_result:{uuid4()}"


def new_personal_overlay_boundary_finding_id() -> str:
    return f"personal_overlay_boundary_finding:{uuid4()}"


def new_personal_core_profile_id() -> str:
    return f"personal_core_profile:{uuid4()}"


def new_personal_mode_profile_id() -> str:
    return f"personal_mode_profile:{uuid4()}"


def new_personal_mode_boundary_id() -> str:
    return f"personal_mode_boundary:{uuid4()}"


def new_personal_mode_capability_binding_id() -> str:
    return f"personal_mode_capability_binding:{uuid4()}"


def new_personal_mode_loadout_id() -> str:
    return f"personal_mode_loadout:{uuid4()}"


def new_personal_mode_loadout_draft_id() -> str:
    return f"personal_mode_loadout_draft:{uuid4()}"

