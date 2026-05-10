from chanta_core.ocel.store import OCELStore
from chanta_core.persona.personal_conformance import PersonalConformanceResult
from chanta_core.persona.personal_mode_binding import PersonalModeBindingService
from chanta_core.persona.personal_mode_loadout import PersonalModeLoadoutService
from chanta_core.persona.personal_overlay import PersonalOverlayLoadResult
from chanta_core.persona.personal_prompt_activation import PersonalPromptActivationService
from chanta_core.persona.personal_smoke_test import PersonalSmokeTestResult


def _loadout_and_binding(trace_store):
    loadouts = PersonalModeLoadoutService(ocel_store=trace_store)
    bindings = PersonalModeBindingService(ocel_store=trace_store)
    core = loadouts.register_core_profile(
        profile_name="public_safe_profile",
        profile_type="test",
        identity_statement="Public-safe identity summary.",
        private=True,
    )
    mode = loadouts.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="public_safe_mode",
        mode_type="test",
        role_statement="Operate within public-safe test boundaries.",
        limitation_summary="No ambient capabilities.",
        private=True,
    )
    boundary = loadouts.register_mode_boundary(
        mode_profile_id=mode.mode_profile_id,
        boundary_type="capability_boundary",
        boundary_text="Capability truth overrides personal claims.",
        severity="high",
    )
    loadout = loadouts.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=[boundary],
        private=True,
    )
    selection = bindings.select_mode(
        mode_profile=mode,
        loadout=loadout,
        selection_source="test",
    )
    runtime_binding = bindings.bind_runtime(
        selection=selection,
        runtime_kind="local_runtime",
    )
    capability = bindings.register_runtime_capability_binding(
        runtime_binding_id=runtime_binding.binding_id,
        capability_name="workspace_read",
        capability_category="workspace",
        availability="requires_explicit_skill",
        can_execute_now=False,
        requires_permission=True,
    )
    return loadout, selection, runtime_binding, [capability]


def test_env_absent_skips_missing_config(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    service = PersonalPromptActivationService(
        ocel_store=OCELStore(tmp_path / "activation.sqlite")
    )

    result = service.activate_for_prompt_context()

    assert result.status == "missing_config"
    assert result.activation_scope == "none"
    assert result.attached_block_ids == []


def test_explicit_loadout_attaches_prompt_context_only(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout, selection, runtime_binding, capabilities = _loadout_and_binding(store)
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(
        explicit_loadout=loadout,
        explicit_selection=selection,
        explicit_runtime_binding=runtime_binding,
        explicit_capability_bindings=capabilities,
        runtime_kind="local_runtime",
    )
    rendered = service.render_activation_blocks(result=result)

    assert result.status == "attached"
    assert result.activation_scope == "prompt_context_only"
    assert result.result_attrs["capability_grants_created"] is False
    assert result.result_attrs["tool_execution_used"] is False
    assert "Runtime capability profile overrides personal/persona claims." in rendered
    assert "This binding does not grant new runtime capabilities." in rendered


def test_overlay_projection_block_excludes_source_body(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout, _, _, _ = _loadout_and_binding(store)
    overlay = PersonalOverlayLoadResult(
        result_id="personal_overlay_load_result:test",
        request_id="personal_overlay_load_request:test",
        manifest_id="personal_directory_manifest:test",
        loaded_projection_ref_ids=["personal_projection_ref:test"],
        rendered_blocks=[
            {
                "projection_ref_id": "personal_projection_ref:test",
                "projection_name": "core",
                "projection_kind": "core_projection",
                "content": "public-safe overlay projection",
            }
        ],
        total_chars=30,
        truncated=False,
        denied=False,
        finding_ids=[],
        created_at="2026-01-01T00:00:00Z",
        result_attrs={"source_bodies_loaded": False},
    )
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(
        explicit_loadout=loadout,
        explicit_overlay_load_result=overlay,
    )
    rendered = service.render_activation_blocks(result=result)

    assert "public-safe overlay projection" in rendered
    assert "source body" not in rendered


def test_unsafe_overlay_denies_attachment(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout, _, _, _ = _loadout_and_binding(store)
    overlay = PersonalOverlayLoadResult(
        result_id="personal_overlay_load_result:denied",
        request_id="personal_overlay_load_request:test",
        manifest_id="personal_directory_manifest:test",
        loaded_projection_ref_ids=[],
        rendered_blocks=[],
        total_chars=0,
        truncated=False,
        denied=True,
        finding_ids=["personal_overlay_boundary_finding:test"],
        created_at="2026-01-01T00:00:00Z",
    )
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(
        explicit_loadout=loadout,
        explicit_overlay_load_result=overlay,
    )

    assert result.status == "denied"
    assert result.activation_scope == "none"


def test_require_conformance_or_smoke_pass_denies(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout, _, _, _ = _loadout_and_binding(store)
    conformance = PersonalConformanceResult(
        result_id="personal_conformance_result:test",
        run_id="personal_conformance_run:test",
        contract_id="personal_conformance_contract:test",
        status="failed",
        score=0.0,
        confidence=1.0,
        passed_finding_ids=[],
        failed_finding_ids=["finding:test"],
        warning_finding_ids=[],
        skipped_finding_ids=[],
        reason=None,
        created_at="2026-01-01T00:00:00Z",
    )
    smoke = PersonalSmokeTestResult(
        result_id="personal_smoke_test_result:test",
        run_id="personal_smoke_test_run:test",
        status="failed",
        score=0.0,
        confidence=1.0,
        passed_assertion_ids=[],
        failed_assertion_ids=["assertion:test"],
        warning_assertion_ids=[],
        skipped_assertion_ids=[],
        reason=None,
        created_at="2026-01-01T00:00:00Z",
    )
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(
        explicit_loadout=loadout,
        conformance_result=conformance,
        smoke_result=smoke,
        require_conformance_pass=True,
        require_smoke_pass=True,
    )

    assert result.status == "denied"
    assert len(result.finding_ids) == 2


def test_max_chars_truncation(monkeypatch, tmp_path) -> None:
    monkeypatch.delenv("CHANTA_PERSONAL_DIRECTORY_ROOT", raising=False)
    store = OCELStore(tmp_path / "activation.sqlite")
    loadout, _, _, _ = _loadout_and_binding(store)
    service = PersonalPromptActivationService(ocel_store=store)

    result = service.activate_for_prompt_context(explicit_loadout=loadout, max_chars=40)

    assert result.truncated is True
    assert result.total_chars <= 40
