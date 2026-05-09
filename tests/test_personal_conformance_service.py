from dataclasses import replace

from chanta_core.persona import (
    PersonalModeBindingService,
    PersonalModeLoadoutService,
    PersonalOverlayLoaderService,
    PersonaSourceStagedImportService,
)
from chanta_core.persona.personal_conformance import PersonalConformanceService


def _source_candidate():
    source_service = PersonaSourceStagedImportService()
    source = source_service.register_source_from_text(
        source_name="profile.md",
        text="# Identity\n- public-safe dummy assistant",
        source_ref="source/identity/profile.md",
        media_type="text/markdown",
    )
    manifest = source_service.create_manifest(
        manifest_name="dummy",
        source_root="source",
        sources=[source],
    )
    candidate = source_service.create_ingestion_candidate(manifest=manifest, sources=[source])
    return source, candidate


def _mode_loadout(private: bool = True):
    service = PersonalModeLoadoutService()
    core = service.register_core_profile(
        profile_name="sample_personal_assistant",
        profile_type="assistant",
        identity_statement="A public-safe assistant profile.",
        private=private,
    )
    mode = service.register_mode_profile(
        core_profile_id=core.core_profile_id,
        mode_name="research_mode",
        mode_type="research_mode",
        role_statement="Analyze provided context.",
        private=private,
    )
    boundaries = [
        service.register_mode_boundary(
            mode_profile_id=mode.mode_profile_id,
            boundary_type="capability_boundary",
            boundary_text="Runtime capability profile is authoritative.",
        ),
        service.register_mode_boundary(
            mode_profile_id=mode.mode_profile_id,
            boundary_type="privacy_boundary",
            boundary_text="Do not expose local personal directory content.",
        ),
    ]
    loadout = service.create_mode_loadout(
        core_profile=core,
        mode_profile=mode,
        boundaries=boundaries,
        private=private,
    )
    return core, mode, boundaries, loadout


def test_default_rules_are_registered() -> None:
    service = PersonalConformanceService()
    contract, rules = service.register_default_rules()
    rule_types = {rule.rule_type for rule in rules}

    assert contract.contract_type == "personal_overlay_boundary"
    assert "canonical_import_disabled" in rule_types
    assert "runtime_binding_non_executing" in rule_types
    assert "no_" + "json" + "l_personal_store" in rule_types
    assert len(rules) >= 18


def test_good_source_candidate_passes_and_enabled_candidate_fails() -> None:
    source, candidate = _source_candidate()
    service = PersonalConformanceService()

    _, good_result, good_findings = service.evaluate_personal_source_conformance(
        candidate=candidate,
        sources=[source],
    )
    bad_candidate = replace(candidate, **{"canonical_import_enabled": True})
    _, bad_result, bad_findings = service.evaluate_personal_source_conformance(
        candidate=bad_candidate,
        sources=[source],
    )

    assert good_result.status == "passed"
    assert any(finding.rule_type == "canonical_import_disabled" for finding in good_findings)
    assert bad_result.status == "failed"
    assert any(
        finding.rule_type == "canonical_import_disabled" and finding.status == "failed"
        for finding in bad_findings
    )


def test_overlay_projection_from_source_fails_and_overlay_projection_passes(tmp_path) -> None:
    root = tmp_path / "personal_directory"
    (root / "overlay").mkdir(parents=True)
    (root / "overlay" / "core.md").write_text("safe projection", encoding="utf-8")
    overlay_service = PersonalOverlayLoaderService()
    config = overlay_service.register_config(directory_name="dummy", directory_root=root)
    manifest = overlay_service.load_manifest(config)
    safe_ref = overlay_service.register_projection_refs(manifest)
    _, safe_result, safe_findings = PersonalConformanceService().evaluate_personal_overlay_conformance(
        manifest=manifest,
        projection_refs=safe_ref,
    )
    source_ref = replace(
        safe_ref[0],
        projection_path=str(root / "source" / "identity.md"),
        safe_for_prompt=True,
    ) if safe_ref else None

    conformance = PersonalConformanceService()
    _, result, findings = conformance.evaluate_personal_overlay_conformance(
        manifest=manifest,
        projection_refs=[source_ref] if source_ref else [],
    )

    assert safe_result.status == "passed"
    assert all(finding.status == "passed" for finding in safe_findings)
    assert result.status in {"failed", "needs_review"}
    assert any(
        finding.rule_type == "source_body_not_prompt_block" and finding.status == "failed"
        for finding in findings
    )


def test_mode_loadout_and_runtime_binding_conformance() -> None:
    _, mode, boundaries, loadout = _mode_loadout()
    conformance = PersonalConformanceService()

    _, loadout_result, _ = conformance.evaluate_personal_mode_loadout_conformance(
        loadout=loadout,
        mode_boundaries=boundaries,
    )

    binding_service = PersonalModeBindingService()
    selection = binding_service.select_mode(mode_profile=mode, loadout=loadout)
    runtime_binding = binding_service.bind_runtime(selection=selection, runtime_kind="local_runtime")
    request = binding_service.create_activation_request(
        mode_profile_id=mode.mode_profile_id,
        loadout_id=loadout.loadout_id,
        runtime_kind="local_runtime",
    )
    activation = binding_service.activate_mode_for_prompt_context(
        request=request,
        mode_profile=mode,
        loadout=loadout,
        runtime_kind="local_runtime",
    )
    _, binding_result, _ = conformance.evaluate_personal_runtime_binding_conformance(
        runtime_binding=runtime_binding,
        activation_result=activation,
    )

    assert loadout_result.status == "passed"
    assert binding_result.status == "passed"
    assert activation.activation_scope in {"prompt_context_only", "runtime_binding_only"}


def test_public_repo_privacy_scan_uses_supplied_dummy_patterns_only() -> None:
    service = PersonalConformanceService()

    _, result, findings = service.evaluate_public_repo_privacy_conformance(
        public_artifacts=[
            {"ref": "safe.md", "text": "ordinary public-safe text"},
            {"ref": "bad.md", "text": "contains DUMMY_FORBIDDEN_TOKEN"},
            {"ref": "store.md", "text": "personal " + "json" + "l store marker"},
        ],
        forbidden_patterns=["DUMMY_FORBIDDEN_TOKEN"],
    )

    assert result.status == "failed"
    assert any(finding.rule_type == "private_content_not_in_public_artifacts" for finding in findings)
    assert any(finding.rule_type == "no_" + "json" + "l_personal_store" for finding in findings)
