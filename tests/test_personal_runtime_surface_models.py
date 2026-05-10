from chanta_core.persona.personal_runtime_surface import (
    PersonalCLICommandResult,
    PersonalRuntimeConfigView,
    PersonalRuntimeDiagnostic,
    PersonalRuntimeHealthCheck,
    PersonalRuntimeStatusSnapshot,
)


def test_personal_runtime_surface_models_to_dict() -> None:
    config = PersonalRuntimeConfigView(
        config_view_id="personal_runtime_config_view:test",
        personal_directory_configured=True,
        directory_root_redacted="<redacted:root:123>",
        config_source="env:CHANTA_PERSONAL_DIRECTORY_ROOT",
        env_key_used="CHANTA_PERSONAL_DIRECTORY_ROOT",
        created_at="2026-01-01T00:00:00Z",
        config_attrs={"path_redacted": True},
    )
    status = PersonalRuntimeStatusSnapshot(
        status_id="personal_runtime_status_snapshot:test",
        config_view_id=config.config_view_id,
        manifest_id="personal_directory_manifest:test",
        personal_directory_configured=True,
        source_root_present=True,
        overlay_dir_present=True,
        profiles_dir_present=True,
        mode_loadouts_dir_present=True,
        validation_dir_present=True,
        letters_dir_excluded=True,
        messages_dir_excluded=True,
        archive_dir_excluded=True,
        available_projection_count=1,
        available_profile_count=1,
        available_loadout_count=1,
        conformance_status="not_run",
        smoke_status="not_run",
        created_at=config.created_at,
        status_attrs={"source_bodies_printed": False},
    )
    health = PersonalRuntimeHealthCheck(
        health_check_id="personal_runtime_health_check:test",
        status_id=status.status_id,
        check_type="config_present",
        status="passed",
        severity="low",
        message="checked",
        created_at=config.created_at,
    )
    diagnostic = PersonalRuntimeDiagnostic(
        diagnostic_id="personal_runtime_diagnostic:test",
        command_name="personal status",
        status="passed",
        severity="low",
        message="checked",
        recommendation=None,
        created_at=config.created_at,
    )
    result = PersonalCLICommandResult(
        result_id="personal_cli_command_result:test",
        command_name="personal status",
        exit_code=0,
        status="passed",
        summary="ok",
        diagnostic_ids=[diagnostic.diagnostic_id],
        status_snapshot_id=status.status_id,
        conformance_result_ids=[],
        smoke_result_ids=[],
        created_at=config.created_at,
    )

    assert config.to_dict()["config_view_id"].startswith("personal_runtime_config_view:")
    assert status.to_dict()["letters_dir_excluded"] is True
    assert health.to_dict()["check_type"] == "config_present"
    assert diagnostic.to_dict()["recommendation"] is None
    assert result.to_dict()["diagnostic_ids"] == [diagnostic.diagnostic_id]
