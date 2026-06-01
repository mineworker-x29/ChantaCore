from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WorkbenchCommandSurfaceFindingService,
    WorkbenchCommandSurfaceReportService,
)


def test_missing_sources_warn_without_fabricating_execution_or_raw_data() -> None:
    parts = WorkbenchCommandSurfaceReportService().build_all_parts(
        view_state_available=False,
        command_surface_panel_available=False,
        dashboard_report_available=False,
        approval_console_available=False,
        evidence_inspector_available=False,
        provider_browser_available=False,
        trace_explorer_available=False,
        skill_registry_available=False,
        provider_registry_available=False,
        pig_guidance_available=False,
        user_intent_available=False,
        strictness="standard",
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert "missing_workbench_view_state" in finding_types
    assert "missing_command_surface_panel" in finding_types
    assert "missing_user_intent_ref" in finding_types
    assert report.command_surface_view_created is True
    assert report.do_nothing_candidates_created is True
    assert report.direct_command_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.file_mutated is False
    assert report.patch_applied is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.memory_promoted is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False


def test_strict_missing_mandatory_command_surface_sources_fails_without_execution() -> None:
    parts = WorkbenchCommandSurfaceReportService().build_all_parts(
        view_state_available=False,
        command_surface_panel_available=False,
        strictness="strict",
    )
    report = parts["report"]

    assert report.report_status == "failed"
    assert report.command_surface_view_created is True
    assert report.command_candidates_created is True
    assert report.do_nothing_candidates_created is True
    assert report.direct_command_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.file_mutated is False
    assert report.patch_applied is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.autonomous_loop_started is False
    assert report.approval_executed is False
    assert report.memory_promoted is False


def test_forbidden_attempt_findings_block_release() -> None:
    blocked_types = [
        "direct_command_execution_attempted",
        "provider_invocation_attempted",
        "local_command_execution_attempted",
        "file_mutation_attempted",
        "patch_application_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "route_rerun_attempted",
        "stage_rerun_attempted",
        "automatic_retry_attempted",
        "automatic_repair_attempted",
        "autonomous_loop_attempted",
        "approval_execution_attempted",
        "approval_token_execution_attempted",
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
        parts = WorkbenchCommandSurfaceReportService().build_all_parts(extra_findings=[finding_type])
        assert parts["report"].report_status == "blocked", finding_type
        assert finding_type in WorkbenchCommandSurfaceFindingService.BLOCKED_FINDINGS


def test_command_surface_cli_commands_are_record_only(capsys) -> None:
    commands = [
        ["workbench", "commands", "surface"],
        ["workbench", "commands", "candidates"],
        ["workbench", "commands", "do-nothing"],
        ["workbench", "commands", "skills"],
        ["workbench", "commands", "actions"],
        ["workbench", "commands", "routes"],
        ["workbench", "commands", "providers"],
        ["workbench", "commands", "file-edit-candidates"],
        ["workbench", "commands", "ask-candidates"],
        ["workbench", "commands", "snapshot-candidates"],
        ["workbench", "commands", "rationale"],
        ["workbench", "commands", "risk"],
        ["workbench", "commands", "pig-guidance"],
        ["workbench", "commands", "safety"],
        ["workbench", "commands", "approval-requirements"],
        ["workbench", "commands", "boundary-trace"],
        [
            "workbench",
            "commands",
            "decide",
            "--candidate-id",
            "candidate-1",
            "--decision",
            "choose_do_nothing",
        ],
        ["workbench", "commands", "history"],
        ["workbench", "commands", "audit"],
        ["workbench", "commands", "report", "--report-id", "report-1"],
    ]
    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.7" in output
        assert "direct_command_executed=false" in output
        assert "provider_invoked=false" in output
        assert "local_command_executed=false" in output
        assert "file_mutated=false" in output
        assert "patch_applied=false" in output
        assert "ask_executed=false" in output
        assert "final_response_emitted=false" in output
        assert "route_rerun_performed=false" in output
        assert "stage_rerun_performed=false" in output
        assert "automatic_retry_performed=false" in output
        assert "automatic_repair_performed=false" in output
        assert "autonomous_loop_started=false" in output
        assert "approval_executed=false" in output
        assert "approval_token_executed=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "persona_mutated=false" in output
        assert "external_provider_adapter_implemented=false" in output
        assert "vendor_adapter_implemented=false" in output
        assert "pig_memory_promoted=false" in output
        assert "pig_policy_mutated=false" in output
        assert "pig_executed=false" in output
        assert "raw_secret_output=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "llm_judge_used=false" in output


def test_changed_v0267_files_do_not_contain_forbidden_true_markers() -> None:
    paths = [
        Path("src/chanta_core/workspace_agent_workbench/command_surface.py"),
        Path("tests/test_workbench_command_surface.py"),
        Path("tests/test_workbench_command_surface_boundaries.py"),
        Path("docs/versions/v0.26/v0.26.7_workbench_command_surface.md"),
    ]
    forbidden_true_markers = [
        name + "=True"
        for name in [
            "direct_command_executed",
            "command_dispatched",
            "provider_invoked",
            "provider_invocation_performed",
            "local_command_executed",
            "bounded_local_command_executed",
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
            "approval_executed",
            "approval_token_executed",
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
