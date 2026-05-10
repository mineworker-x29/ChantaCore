from chanta_core.persona.history_adapter import (
    personal_cli_command_results_to_history_entries,
    personal_runtime_diagnostics_to_history_entries,
    personal_runtime_status_snapshots_to_history_entries,
)
from chanta_core.persona.personal_runtime_surface import (
    PersonalCLICommandResult,
    PersonalRuntimeDiagnostic,
    PersonalRuntimeStatusSnapshot,
)


def test_personal_runtime_surface_history_entries() -> None:
    created_at = "2026-01-01T00:00:00Z"
    snapshot = PersonalRuntimeStatusSnapshot(
        status_id="personal_runtime_status_snapshot:test",
        config_view_id="personal_runtime_config_view:test",
        manifest_id=None,
        personal_directory_configured=False,
        source_root_present=False,
        overlay_dir_present=False,
        profiles_dir_present=False,
        mode_loadouts_dir_present=False,
        validation_dir_present=False,
        letters_dir_excluded=False,
        messages_dir_excluded=False,
        archive_dir_excluded=False,
        available_projection_count=0,
        available_profile_count=0,
        available_loadout_count=0,
        conformance_status="not_run",
        smoke_status="not_run",
        created_at=created_at,
    )
    diagnostic = PersonalRuntimeDiagnostic(
        diagnostic_id="personal_runtime_diagnostic:test",
        command_name="personal validate",
        status="failed",
        severity="medium",
        message="Personal Directory is not configured.",
        recommendation=None,
        created_at=created_at,
    )
    result = PersonalCLICommandResult(
        result_id="personal_cli_command_result:test",
        command_name="personal validate",
        exit_code=1,
        status="failed",
        summary="not run",
        diagnostic_ids=[diagnostic.diagnostic_id],
        status_snapshot_id=snapshot.status_id,
        conformance_result_ids=[],
        smoke_result_ids=[],
        created_at=created_at,
    )

    snapshot_entry = personal_runtime_status_snapshots_to_history_entries([snapshot])[0]
    diagnostic_entry = personal_runtime_diagnostics_to_history_entries([diagnostic])[0]
    result_entry = personal_cli_command_results_to_history_entries([result])[0]

    assert snapshot_entry.source == "personal_runtime_surface"
    assert diagnostic_entry.priority >= 70
    assert result_entry.priority == 85
    assert "personal_cli_command_result" in {ref["ref_type"] for ref in result_entry.refs}
