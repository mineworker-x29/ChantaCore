from chanta_core.persona import (
    PersonalModeBindingService,
    PersonalModeLoadoutService,
)


def _loadout():
    loadout_service = PersonalModeLoadoutService()
    core = loadout_service.register_core_profile(
        profile_name="sample_personal_assistant",
        profile_type="assistant",
        identity_statement="A public-safe assistant profile.",
    )
    mode = loadout_service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="research_mode",
        mode_type="research_mode",
        role_statement="Analyze provided documents.",
        limitation_summary="No local access is claimed without runtime capability evidence.",
    )
    boundary = loadout_service.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Runtime capability profile is authoritative.",
        severity="high",
    )
    loadout = loadout_service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
    )
    return core, mode, loadout


def test_select_mode_and_bind_external_chat_defaults_to_manual_handoff() -> None:
    _, mode, loadout = _loadout()
    service = PersonalModeBindingService()

    selection = service.select_mode(
        mode_profile=mode,
        loadout=loadout,
        selection_source="test",
        session_id="session:test",
    )
    runtime_binding = service.bind_runtime(
        selection=selection,
        runtime_kind="external_chat",
    )

    assert selection.selected_mode_name == "research_mode"
    assert runtime_binding.context_ingress == "manual_handoff"
    assert runtime_binding.binding_attrs["runtime_executed"] is False
    assert runtime_binding.binding_attrs["capability_grants_created"] is False


def test_bind_local_runtime_defaults_to_local_runtime_context() -> None:
    _, mode, loadout = _loadout()
    service = PersonalModeBindingService()
    selection = service.select_mode(mode_profile=mode, loadout=loadout)

    runtime_binding = service.bind_runtime(
        selection=selection,
        runtime_kind="local_runtime",
    )

    assert runtime_binding.context_ingress == "local_runtime_context"
    assert runtime_binding.binding_attrs["active_tool_routing_enabled"] is False


def test_runtime_capability_binding_and_render_block_do_not_grant_capabilities() -> None:
    _, mode, loadout = _loadout()
    service = PersonalModeBindingService()
    selection = service.select_mode(mode_profile=mode, loadout=loadout)
    runtime_binding = service.bind_runtime(selection=selection, runtime_kind="local_runtime")
    capability = service.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="workspace_read",
        capability_category="workspace",
        availability="available_via_explicit_skill",
        can_execute_now=False,
        requires_permission=True,
        source_kind="runtime_profile",
        source_ref="capability_profile:test",
    )
    block = service.render_runtime_binding_block(
        selection=selection,
        runtime_binding=runtime_binding,
        capability_bindings=[capability],
    )

    assert capability.binding_attrs["capability_grant_created"] is False
    assert "This binding does not grant new runtime capabilities." in block
    assert "requires_permission=True" in block


def test_activation_is_prompt_context_only() -> None:
    _, mode, loadout = _loadout()
    service = PersonalModeBindingService()
    request = service.create_activation_request(
        mode_profile_id=mode.mode_profile_id,
        loadout_id=loadout.loadout_id,
        runtime_kind="external_chat",
        requested_by="test",
    )

    result = service.activate_mode_for_prompt_context(
        request=request,
        mode_profile=mode,
        loadout=loadout,
        runtime_kind="external_chat",
    )

    assert result.status == "activated"
    assert result.activated is True
    assert result.activation_scope == "prompt_context_only"
    assert result.result_attrs["runtime_mutated"] is False
    assert result.result_attrs["capability_grants_created"] is False


def test_active_runtime_request_is_denied() -> None:
    _, mode, loadout = _loadout()
    service = PersonalModeBindingService()
    request = service.create_activation_request(
        mode_profile_id=mode.mode_profile_id,
        loadout_id=loadout.loadout_id,
        runtime_kind="local_runtime",
        request_attrs={"active_runtime_requested": True},
    )

    result = service.activate_mode_for_prompt_context(
        request=request,
        mode_profile=mode,
        loadout=loadout,
        runtime_kind="local_runtime",
    )

    assert result.status == "denied"
    assert result.activated is False
    assert result.activation_scope == "none"
    assert result.denied_reason == "Active runtime mode switching is not implemented."
