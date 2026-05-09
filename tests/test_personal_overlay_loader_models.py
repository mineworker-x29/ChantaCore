from chanta_core.persona import (
    PersonalOverlayBoundaryFinding,
    PersonalDirectoryConfig,
    PersonalOverlayLoadRequest,
    PersonalOverlayLoadResult,
    PersonalDirectoryManifest,
    PersonalProjectionRef,
)
from chanta_core.utility.time import utc_now_iso


def test_personal_overlay_models_to_dict() -> None:
    created_at = utc_now_iso()
    config = PersonalDirectoryConfig(
        config_id="personal_directory_config:test",
        directory_name="dummy",
        directory_root="DUMMY_ROOT",
        config_source="explicit_input",
        private=True,
        status="registered",
        created_at=created_at,
        config_attrs={"root_hash": "abc"},
    )
    manifest = PersonalDirectoryManifest(
        manifest_id="personal_directory_manifest:test",
        config_id=config.config_id,
        directory_root="DUMMY_ROOT",
        source_root="DUMMY_ROOT/source",
        overlay_dir="DUMMY_ROOT/overlay",
        profiles_dir="DUMMY_ROOT/profiles",
        mode_loadouts_dir="DUMMY_ROOT/mode_loadouts",
        validation_dir="DUMMY_ROOT/validation",
        source_manifest_ref=None,
        available_projection_refs=[{"name": "core", "kind": "core_projection"}],
        available_profile_refs=[{"name": "default", "kind": "profile_projection"}],
        available_loadout_refs=[{"name": "mode", "kind": "mode_loadout"}],
        excluded_roots=["DUMMY_ROOT/letters"],
        created_at=created_at,
        manifest_attrs={},
    )
    request = PersonalOverlayLoadRequest(
        request_id="personal_overlay_load_request:test",
        manifest_id=manifest.manifest_id,
        requested_projection=None,
        requested_profile=None,
        requested_mode="mode",
        session_id="session:test",
        turn_id="turn:test",
        created_at=created_at,
    )
    ref = PersonalProjectionRef(
        projection_ref_id="personal_projection_ref:test",
        manifest_id=manifest.manifest_id,
        projection_name="mode",
        projection_path="DUMMY_ROOT/mode_loadouts/mode.md",
        projection_kind="mode_loadout",
        content_hash="hash",
        content_preview="preview",
        total_chars=7,
        private=True,
        safe_for_prompt=True,
        created_at=created_at,
    )
    result = PersonalOverlayLoadResult(
        result_id="personal_overlay_load_result:test",
        request_id=request.request_id,
        manifest_id=manifest.manifest_id,
        loaded_projection_ref_ids=[ref.projection_ref_id],
        rendered_blocks=[{"content": "preview", "projection_ref_id": ref.projection_ref_id}],
        total_chars=7,
        truncated=False,
        denied=False,
        finding_ids=[],
        created_at=created_at,
    )
    finding = PersonalOverlayBoundaryFinding(
        finding_id="personal_overlay_boundary_finding:test",
        manifest_id=manifest.manifest_id,
        request_id=request.request_id,
        finding_type="dummy",
        status="passed",
        severity="info",
        message="Checked.",
        subject_ref="dummy:hash",
        created_at=created_at,
    )

    assert config.to_dict()["private"] is True
    assert manifest.to_dict()["available_projection_refs"][0]["name"] == "core"
    assert request.to_dict()["requested_mode"] == "mode"
    assert ref.to_dict()["safe_for_prompt"] is True
    assert result.to_dict()["denied"] is False
    assert finding.to_dict()["status"] == "passed"

