from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WorkbenchRunDashboardFindingService,
    WorkbenchRunDashboardReportService,
)


def test_missing_sources_warn_without_fabricating_monitoring_execution_or_raw_data() -> None:
    parts = WorkbenchRunDashboardReportService().build_all_parts(
        view_state_available=False,
        run_dashboard_panel_available=False,
        session_monitor_panel_available=False,
        ask_repl_available=False,
        trace_telemetry_available=False,
        approval_console_available=False,
        evidence_inspector_available=False,
        provider_browser_available=False,
        pig_guidance_available=False,
        strictness="standard",
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert "missing_workbench_view_state" in finding_types
    assert "missing_run_dashboard_panel" in finding_types
    assert "missing_session_monitor_panel" in finding_types
    assert "missing_ask_repl_report" in finding_types
    assert "missing_pipeline_run" in finding_types
    assert "missing_trace_telemetry_report" in finding_types
    assert "missing_session_refs" in finding_types
    assert report.background_monitor_started is False
    assert report.continuous_watcher_started is False
    assert report.auto_refresh_execution_started is False
    assert report.rerun_performed is False
    assert report.automatic_retry_performed is False
    assert report.automatic_repair_performed is False
    assert report.command_executed is False
    assert report.approval_executed is False
    assert report.provider_invoked is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False


def test_strict_missing_mandatory_view_sources_fails_but_does_not_execute() -> None:
    parts = WorkbenchRunDashboardReportService().build_all_parts(
        view_state_available=False,
        run_dashboard_panel_available=False,
        session_monitor_panel_available=False,
        strictness="strict",
    )
    report = parts["report"]

    assert report.report_status == "failed"
    assert report.run_dashboard_view_created is True
    assert report.session_monitor_view_created is True
    assert report.background_monitor_started is False
    assert report.rerun_performed is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.ask_executed is False
    assert report.memory_continuity_enabled is False
    assert report.memory_promoted is False
    assert report.persona_mutated is False


def test_forbidden_attempt_findings_block_release() -> None:
    blocked_types = [
        "background_monitor_attempted",
        "continuous_watcher_attempted",
        "auto_refresh_execution_attempted",
        "rerun_attempted",
        "automatic_retry_attempted",
        "automatic_repair_attempted",
        "autonomous_optimization_attempted",
        "command_execution_attempted",
        "approval_execution_attempted",
        "provider_invocation_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "memory_continuity_attempted",
        "memory_promotion_attempted",
        "persistent_memory_write_attempted",
        "persona_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "external_adapter_detected",
        "vendor_adapter_detected",
        "schumpeter_split_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_detected",
        "raw_transcript_persistence_detected",
        "llm_judge_detected",
    ]
    for finding_type in blocked_types:
        parts = WorkbenchRunDashboardReportService().build_all_parts(extra_findings=[finding_type])
        assert parts["report"].report_status == "blocked", finding_type
        assert finding_type in WorkbenchRunDashboardFindingService.BLOCKED_FINDINGS


def test_dashboard_and_session_cli_commands_are_view_only(capsys) -> None:
    commands = [
        ["workbench", "dashboard", "view"],
        ["workbench", "dashboard", "runs"],
        ["workbench", "dashboard", "pipeline-status"],
        ["workbench", "dashboard", "providers"],
        ["workbench", "dashboard", "responses"],
        ["workbench", "dashboard", "safety"],
        ["workbench", "dashboard", "approvals"],
        ["workbench", "dashboard", "failures"],
        ["workbench", "dashboard", "warnings"],
        ["workbench", "dashboard", "metrics"],
        ["workbench", "dashboard", "report", "--report-id", "report-1"],
        ["workbench", "sessions", "monitor"],
        ["workbench", "sessions", "cards"],
        ["workbench", "sessions", "trace-summary"],
        ["workbench", "sessions", "pig-guidance"],
        ["workbench", "sessions", "patterns"],
        ["workbench", "sessions", "context-refs"],
    ]
    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.6" in output
        assert "background_monitor_started=false" in output
        assert "continuous_watcher_started=false" in output
        assert "rerun_performed=false" in output
        assert "automatic_repair_performed=false" in output
        assert "command_executed=false" in output
        assert "provider_invoked=false" in output
        assert "memory_promoted=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output


def test_changed_v0266_files_do_not_contain_forbidden_true_markers() -> None:
    paths = [
        Path("src/chanta_core/workspace_agent_workbench/run_dashboard.py"),
        Path("tests/test_workbench_run_dashboard_session_monitor.py"),
        Path("tests/test_workbench_run_dashboard_session_monitor_boundaries.py"),
        Path("docs/versions/v0.26/v0.26.6_run_dashboard_session_monitor.md"),
    ]
    forbidden_true_markers = [
        name + "=True"
        for name in [
            "background_monitor_started",
            "continuous_watcher_started",
            "auto_refresh_execution_started",
            "rerun_performed",
            "automatic_retry_performed",
            "automatic_repair_performed",
            "autonomous_optimization_performed",
            "command_executed",
            "approval_executed",
            "provider_invoked",
            "agent_ask_executed",
            "final_response_emitted",
            "local_command_executed",
            "memory_continuity_enabled",
            "memory_promoted",
            "persistent_memory_written",
            "persona_mutated",
            "pig_memory_promoted",
            "pig_policy_mutated",
            "pig_executed",
            "external_provider_adapter_implemented",
            "vendor_adapter_implemented",
            "schumpeter_split_introduced",
            "raw_transcript_persisted",
            "credential_exposed",
            "raw_secret_output",
            "raw_provider_output_inline",
        ]
    ]
    for path in paths:
        text = path.read_text(encoding="utf-8")
        for marker in forbidden_true_markers:
            assert marker not in text
        assert "subprocess" + ".run" not in text
        assert "subprocess" + ".Popen" not in text
        assert "os" + ".system" not in text
        assert "shell" + "=True" not in text
        assert "chat" + "." + "com" + "pletions" not in text
