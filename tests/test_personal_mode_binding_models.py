from chanta_core.persona import (
    PersonalModeActivationRequest,
    PersonalModeActivationResult,
    PersonalModeSelection,
    PersonalRuntimeBinding,
    PersonalRuntimeCapabilityBinding,
)
from chanta_core.utility.time import utc_now_iso


def test_personal_mode_binding_models_to_dict() -> None:
    created_at = utc_now_iso()
    selection = PersonalModeSelection(
        selection_id="personal_mode_selection:test",
        core_profile_id="personal_core_profile:test",
        mode_profile_id="personal_mode_profile:test",
        loadout_id="personal_mode_loadout:test",
        selected_mode_name="research_mode",
        selected_mode_type="research_mode",
        selection_source="test",
        session_id="session:test",
        turn_id="turn:test",
        status="selected",
        private=False,
        created_at=created_at,
    )
    binding = PersonalRuntimeBinding(
        binding_id="personal_runtime_binding:test",
        selection_id=selection.selection_id,
        core_profile_id=selection.core_profile_id,
        mode_profile_id=selection.mode_profile_id,
        loadout_id=selection.loadout_id,
        runtime_kind="external_chat",
        runtime_path=None,
        context_ingress="manual_handoff",
        capability_profile_ref=None,
        status="bound",
        private=False,
        created_at=created_at,
    )
    capability = PersonalRuntimeCapabilityBinding(
        runtime_capability_binding_id="personal_runtime_capability_binding:test",
        runtime_binding_id=binding.binding_id,
        capability_name="provided_context_reasoning",
        capability_category="reasoning",
        availability="metadata_only",
        can_execute_now=False,
        requires_permission=False,
        requires_review=False,
        source_kind="runtime_profile",
        source_ref="capability_profile:test",
        created_at=created_at,
    )
    request = PersonalModeActivationRequest(
        request_id="personal_mode_activation_request:test",
        mode_profile_id=selection.mode_profile_id,
        loadout_id=selection.loadout_id,
        runtime_kind="external_chat",
        requested_by="test",
        session_id="session:test",
        turn_id="turn:test",
        reason="test activation",
        created_at=created_at,
    )
    result = PersonalModeActivationResult(
        result_id="personal_mode_activation_result:test",
        request_id=request.request_id,
        selection_id=selection.selection_id,
        runtime_binding_id=binding.binding_id,
        status="activated",
        activated=True,
        activation_scope="prompt_context_only",
        capability_boundary_summary="Runtime capability profile overrides personal/persona claims.",
        denied_reason=None,
        finding_ids=[],
        created_at=created_at,
    )

    assert selection.to_dict()["selected_mode_name"] == "research_mode"
    assert binding.to_dict()["context_ingress"] == "manual_handoff"
    assert capability.to_dict()["can_execute_now"] is False
    assert request.to_dict()["runtime_kind"] == "external_chat"
    assert result.to_dict()["activation_scope"] == "prompt_context_only"
