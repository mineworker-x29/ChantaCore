from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench.snapshot_export import (
    WorkbenchSnapshotExportFindingService,
    WorkbenchSnapshotExportReportService,
)


def test_missing_sources_warn_without_memory_or_raw_export() -> None:
    parts = WorkbenchSnapshotExportReportService().build_all_parts(
        view_state_available=False,
        snapshot_export_panel_available=False,
        command_surface_available=False,
        dashboard_available=False,
        trace_explorer_available=False,
        pig_guidance_available=False,
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert "missing_workbench_view_state" in finding_types
    assert "missing_snapshot_export_panel" in finding_types
    assert "missing_command_surface_report" in finding_types
    assert "missing_dashboard_report" in finding_types
    assert "missing_trace_report" in finding_types
    assert report.snapshot_created is True
    assert report.ocel_export_package_created is True
    assert report.memory_candidate_created is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.raw_transcript_exported is False
    assert report.raw_provider_output_exported is False
    assert report.raw_secret_exported is False
    assert report.external_sync_performed is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.llm_judge_used is False


def test_strict_missing_mandatory_sources_fails_without_export_or_execution() -> None:
    parts = WorkbenchSnapshotExportReportService().build_all_parts(
        strictness="strict",
        view_state_available=False,
        snapshot_export_panel_available=False,
    )
    report = parts["report"]

    assert report.report_status == "failed"
    assert report.ready_for_v0_26_9 is False
    assert report.ready_for_v0_27 is False
    assert report.memory_candidate_created is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.raw_transcript_exported is False
    assert report.raw_provider_output_exported is False
    assert report.raw_secret_exported is False
    assert report.credential_exported is False
    assert report.private_full_path_exported is False
    assert report.external_sync_performed is False
    assert report.pm4py_runtime_dependency_added is False
    assert report.ocpa_runtime_dependency_added is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.file_mutated is False
    assert report.patch_applied is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.autonomous_loop_started is False


def test_forbidden_attempt_findings_block_snapshot_export() -> None:
    service = WorkbenchSnapshotExportReportService()
    for finding_type in WorkbenchSnapshotExportFindingService.BLOCKED_FINDINGS:
        report = service.build_all_parts(extra_findings=[finding_type])["report"]
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.report_status == "blocked"
        assert report.ready_for_v0_26_9 is False
        assert finding_type in finding_types


def test_snapshot_and_export_cli_commands_are_record_only(capsys) -> None:
    commands = [
        ["workbench", "snapshot", "create"],
        ["workbench", "snapshot", "selection"],
        ["workbench", "snapshot", "manifest"],
        ["workbench", "snapshot", "refs"],
        ["workbench", "snapshot", "redaction"],
        ["workbench", "snapshot", "reproducibility"],
        ["workbench", "snapshot", "report", "--report-id", "snapshot-report:test"],
        ["workbench", "export", "ocel"],
        ["workbench", "export", "manifest"],
        ["workbench", "export", "quality"],
        ["workbench", "export", "trace-coverage"],
        ["workbench", "export", "boundary"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.8" in output
        assert "ready_for_v0_26_9=true" in output
        assert "ready_for_v0_27=false" in output
        assert "memory_candidate_created=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "raw_transcript_exported=false" in output
        assert "raw_provider_output_exported=false" in output
        assert "raw_secret_exported=false" in output
        assert "credential_exported=false" in output
        assert "private_full_path_exported=false" in output
        assert "external_sync_performed=false" in output
        assert "pm4py_runtime_dependency_added=false" in output
        assert "ocpa_runtime_dependency_added=false" in output
        assert "command_executed=false" in output
        assert "provider_invoked=false" in output
        assert "local_command_executed=false" in output
        assert "file_mutated=false" in output
        assert "patch_applied=false" in output
        assert "ask_executed=false" in output
        assert "final_response_emitted=false" in output
        assert "automatic_retry_performed=false" in output
        assert "automatic_repair_performed=false" in output
        assert "autonomous_loop_started=false" in output
        assert "pig_memory_promoted=false" in output
        assert "pig_policy_mutated=false" in output
        assert "pig_executed=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "llm_judge_used=false" in output


def test_v0268_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "workspace_agent_workbench" / "snapshot_export.py",
        root / "tests" / "test_workbench_snapshot_ocel_export.py",
        root / "tests" / "test_workbench_snapshot_ocel_export_boundaries.py",
        root / "docs" / "versions" / "v0.26" / "v0.26.8_workbench_snapshot_ocel_export.md",
    ]
    forbidden_names = [
        "memory_candidate_created",
        "memory_promoted",
        "persistent_memory_written",
        "persona_mutated",
        "raw_transcript_exported",
        "raw_provider_output_exported",
        "raw_secret_exported",
        "credential_exported",
        "private_full_path_exported",
        "external_sync_performed",
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "vendor_adapter_implemented",
        "pm4py_runtime_dependency_added",
        "ocpa_runtime_dependency_added",
        "command_executed",
        "provider_invoked",
        "local_command_executed",
        "file_mutated",
        "patch_applied",
        "file_written",
        "file_edited",
        "file_deleted",
        "agent_ask_executed",
        "agent_repl_started",
        "final_response_emitted",
        "route_rerun_performed",
        "stage_rerun_performed",
        "automatic_retry_performed",
        "automatic_repair_performed",
        "autonomous_loop_started",
        "pig_memory_promoted",
        "pig_policy_mutated",
        "pig_executed",
        "schumpeter_split_introduced",
    ]
    forbidden_runtime_markers = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "exec" + "(",
        "eval" + "(",
        "import " + "pm4py",
        "from " + "pm4py",
        "import " + "ocpa",
        "from " + "ocpa",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        for name in forbidden_names:
            assert f"{name}=True" not in text
        for marker in forbidden_runtime_markers:
            assert marker not in text
