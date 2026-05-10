from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.persona.personal_runtime_surface import PersonalRuntimeSurfaceService
from chanta_core.pig.reports import PIGReportService


def _dummy_personal_directory(root: Path) -> None:
    for name in ["source", "overlay", "profiles", "mode_loadouts", "validation"]:
        (root / name).mkdir(parents=True, exist_ok=True)
    (root / "overlay" / "core.md").write_text("public-safe overlay", encoding="utf-8")
    (root / "profiles" / "profile.md").write_text("public-safe profile", encoding="utf-8")
    (root / "mode_loadouts" / "mode.md").write_text("public-safe mode", encoding="utf-8")


def test_personal_runtime_surface_records_ocel_objects_events_and_relations(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    store = OCELStore(tmp_path / "surface.sqlite")
    service = PersonalRuntimeSurfaceService(ocel_store=store)

    result = service.run_personal_status()

    assert result.status in {"passed", "needs_review"}
    object_types = {
        item["object_type"]
        for object_type in [
            "personal_runtime_config_view",
            "personal_runtime_status_snapshot",
            "personal_runtime_health_check",
            "personal_cli_command_result",
        ]
        for item in store.fetch_objects_by_type(object_type)
    }
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    relations = store.fetch_object_object_relations_for_object(result.result_id)

    assert "personal_runtime_config_view" in object_types
    assert "personal_runtime_status_snapshot" in object_types
    assert "personal_runtime_health_check" in object_types
    assert "personal_cli_command_result" in object_types
    assert "personal_runtime_config_view_created" in events
    assert "personal_runtime_status_snapshot_created" in events
    assert "personal_runtime_health_check_recorded" in events
    assert "personal_cli_command_completed" in events
    assert any(item["qualifier"] == "references_status_snapshot" for item in relations)


def test_personal_runtime_surface_pig_summary_counts(monkeypatch, tmp_path) -> None:
    personal_root = tmp_path / "personal"
    _dummy_personal_directory(personal_root)
    monkeypatch.setenv("CHANTA_PERSONAL_DIRECTORY_ROOT", str(personal_root))
    store = OCELStore(tmp_path / "surface.sqlite")
    service = PersonalRuntimeSurfaceService(ocel_store=store)

    service.run_personal_validate()
    service.run_personal_smoke()
    objects = []
    object_type_counts = {}
    for object_type in [
        "personal_runtime_config_view",
        "personal_runtime_status_snapshot",
        "personal_runtime_health_check",
        "personal_runtime_diagnostic",
        "personal_cli_command_result",
    ]:
        rows = store.fetch_objects_by_type(object_type)
        object_type_counts[object_type] = len(rows)
        objects.extend(
            type(
                "Obj",
                (),
                {
                    "object_id": row["object_id"],
                    "object_type": row["object_type"],
                    "object_attrs": row["object_attrs"],
                },
            )()
            for row in rows
        )
    event_activity_counts = {}
    for event in store.fetch_recent_events(limit=200):
        activity = event["event_activity"]
        event_activity_counts[activity] = event_activity_counts.get(activity, 0) + 1
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=objects,
    )

    summary = PIGReportService._persona_summary(object_type_counts, event_activity_counts, view)

    assert summary["personal_runtime_config_view_count"] >= 2
    assert summary["personal_runtime_status_snapshot_count"] >= 2
    assert summary["personal_cli_validate_run_count"] == 1
    assert summary["personal_cli_smoke_run_count"] == 1
