from chanta_core.ocel.store import OCELStore
from chanta_core.persona import PersonalOverlayLoaderService
from chanta_core.traces.trace_service import TraceService


def _write(path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_personal_overlay_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    root = tmp_path / "dummy_personal_directory"
    _write(root / "overlay" / "core.md", "projection")
    store = OCELStore(tmp_path / "personal_overlay.sqlite")
    service = PersonalOverlayLoaderService(trace_service=TraceService(ocel_store=store))
    config = service.register_config(directory_name="dummy", directory_root=root)
    manifest = service.load_manifest(config)
    findings = service.check_overlay_boundaries(manifest, public_repo_root=tmp_path / "public_repo")
    refs = service.register_projection_refs(manifest)
    service.load_projection_for_prompt(
        manifest=manifest,
        projection_refs=refs,
        boundary_findings=findings,
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}

    for object_type in [
        "personal_directory_config",
        "personal_directory_manifest",
        "personal_projection_ref",
        "personal_overlay_load_request",
        "personal_overlay_load_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    assert {
        "personal_directory_config_registered",
        "personal_directory_manifest_loaded",
        "personal_overlay_boundary_checked",
        "personal_projection_ref_registered",
        "personal_overlay_load_requested",
        "personal_overlay_load_completed",
        "personal_projection_attached_to_prompt",
    }.issubset(activities)





