from chanta_core.persona import PersonalModeLoadoutService


def _core(service: PersonalModeLoadoutService):
    return service.register_core_profile(
        profile_name="dummy_personal_profile",
        profile_type="assistant",
        identity_statement="A public-safe assistant identity for tests.",
        continuity_statement="Use only supplied context.",
    )


def test_service_creates_core_mode_boundaries_bindings_and_loadout() -> None:
    service = PersonalModeLoadoutService()
    core = _core(service)
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="research_mode",
        mode_type="research_mode",
        role_statement="Analyze provided documents.",
        capability_summary="Can reason over provided material.",
        limitation_summary="Cannot claim filesystem access unless explicitly bound.",
    )
    boundaries = [
        service.register_mode_boundary(
            mode_profile_id=mode.mode_profile_id,
            boundary_type="capability_boundary",
            boundary_text="Runtime capability profile is authoritative.",
            severity="high",
        ),
        service.register_mode_boundary(
            mode_profile_id=mode.mode_profile_id,
            boundary_type="privacy_boundary",
            boundary_text="Do not expose local personal directory contents.",
            severity="high",
        ),
    ]
    binding = service.register_capability_binding(
        mode_profile_id=mode.mode_profile_id,
        capability_name="document_reasoning",
        capability_category="reasoning",
        availability="metadata_only",
        can_execute_now=False,
        requires_review=True,
    )
    loadout = service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=boundaries,
        capability_bindings=[binding],
    )
    rendered = service.render_mode_loadout_block(loadout=loadout)

    assert loadout.core_profile_id == core.core_profile_id
    assert loadout.mode_profile_id == mode.mode_profile_id
    assert binding.binding_id in loadout.capability_binding_ids
    assert "Runtime capability profile overrides personal/persona claims." in rendered
    assert "metadata_only" in loadout.capability_boundary_block
    assert loadout.loadout_attrs["runtime_mode_selection_enabled"] is False
    assert loadout.loadout_attrs["capability_grants_created"] is False


def test_service_creates_pending_draft_without_activation() -> None:
    service = PersonalModeLoadoutService()
    core = _core(service)
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="writing_mode",
        mode_type="writing_mode",
        role_statement="Draft text from provided requirements.",
    )

    draft = service.create_mode_loadout_draft(
        core_profile=core,
        mode_profile=mode,
        projected_blocks=[{"kind": "role", "content": "Draft text."}],
        source_refs=[{"kind": "projection_ref", "id": "personal_projection_ref:dummy"}],
        unresolved_questions=["Which output format is required?"],
    )

    assert draft.review_status == "pending_review"
    assert draft.canonical_activation_enabled is False
    assert draft.draft_attrs["runtime_activation_enabled"] is False


def test_multi_mode_loadout_set_uses_generic_specs() -> None:
    service = PersonalModeLoadoutService()
    core = _core(service)

    loadouts = service.create_multi_mode_loadout_set(
        core_profile=core,
        mode_specs=[
            {
                "mode_name": "research_mode",
                "mode_type": "research_mode",
                "role_statement": "Analyze provided documents.",
                "boundaries": [
                    {
                        "boundary_type": "capability_boundary",
                        "boundary_text": "Do not claim filesystem access.",
                    }
                ],
                "capability_bindings": [
                    {
                        "capability_name": "document_reasoning",
                        "capability_category": "reasoning",
                        "availability": "metadata_only",
                    }
                ],
            },
            {
                "mode_name": "coding_mode",
                "mode_type": "coding_mode",
                "role_statement": "Reason about code supplied in the prompt.",
                "boundaries": [
                    {
                        "boundary_type": "runtime_boundary",
                        "boundary_text": "Runtime execution depends on actual bindings.",
                    }
                ],
                "capability_bindings": [
                    {
                        "capability_name": "local_execution",
                        "capability_category": "runtime",
                        "availability": "not_implemented",
                    }
                ],
            },
        ],
    )

    assert [loadout.loadout_name for loadout in loadouts] == [
        "dummy_personal_profile:research_mode",
        "dummy_personal_profile:coding_mode",
    ]
    assert loadouts[0].capability_boundary_block != loadouts[1].capability_boundary_block
