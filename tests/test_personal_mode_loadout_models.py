from chanta_core.persona import (
    PersonalCoreProfile,
    PersonalModeBoundary,
    PersonalModeCapabilityBinding,
    PersonalModeLoadout,
    PersonalModeLoadoutDraft,
    PersonalModeProfile,
)
from chanta_core.utility.time import utc_now_iso


def test_personal_mode_loadout_models_to_dict() -> None:
    created_at = utc_now_iso()
    core = PersonalCoreProfile(
        core_profile_id="personal_core_profile:test",
        profile_name="dummy_personal_profile",
        profile_type="assistant",
        description="Dummy profile.",
        identity_statement="A public-safe sample assistant profile.",
        continuity_statement="Use supplied context only.",
        status="active",
        private=False,
        created_at=created_at,
        updated_at=created_at,
    )
    mode = PersonalModeProfile(
        mode_profile_id="personal_mode_profile:test",
        core_profile_id=core.core_profile_id,
        mode_name="research_mode",
        mode_type="research_mode",
        role_statement="Analyze provided documents.",
        operating_context="Provided context only.",
        capability_summary="Can reason over supplied text.",
        limitation_summary="Cannot claim local file access without a binding.",
        status="active",
        private=False,
        created_at=created_at,
        updated_at=created_at,
    )
    boundary = PersonalModeBoundary(
        boundary_id="personal_mode_boundary:test",
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Use runtime capability profile as truth.",
        severity="high",
        required=True,
        status="active",
        created_at=created_at,
    )
    binding = PersonalModeCapabilityBinding(
        binding_id="personal_mode_capability_binding:test",
        mode_profile_id=mode.mode_profile_id,
        capability_name="document_analysis",
        capability_category="reasoning",
        availability="metadata_only",
        can_execute_now=False,
        requires_permission=False,
        requires_review=True,
        source_kind="runtime_profile",
        source_ref="capability_surface:test",
        created_at=created_at,
    )
    loadout = PersonalModeLoadout(
        loadout_id="personal_mode_loadout:test",
        core_profile_id=core.core_profile_id,
        mode_profile_id=mode.mode_profile_id,
        loadout_name="research_mode_loadout",
        identity_block="Identity",
        role_block="Role",
        capability_boundary_block="Runtime capability profile overrides personal/persona claims.",
        safety_boundary_block="Safety",
        privacy_boundary_block="Privacy",
        projection_ref_ids=[],
        source_candidate_ids=[],
        capability_binding_ids=[binding.binding_id],
        total_chars=10,
        truncated=False,
        private=False,
        created_at=created_at,
    )
    draft = PersonalModeLoadoutDraft(
        draft_id="personal_mode_loadout_draft:test",
        core_profile_id=core.core_profile_id,
        mode_profile_id=mode.mode_profile_id,
        draft_name="research_draft",
        projected_blocks=[{"kind": "identity", "content": "Identity"}],
        source_refs=[],
        unresolved_questions=[],
        review_status="pending_review",
        private=False,
        canonical_activation_enabled=False,
        created_at=created_at,
    )

    assert core.to_dict()["profile_type"] == "assistant"
    assert mode.to_dict()["mode_type"] == "research_mode"
    assert boundary.to_dict()["required"] is True
    assert binding.to_dict()["can_execute_now"] is False
    assert loadout.to_dict()["capability_binding_ids"] == [binding.binding_id]
    assert draft.to_dict()["canonical_activation_enabled"] is False
