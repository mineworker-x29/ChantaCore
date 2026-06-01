from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench import (
    WorkbenchApprovalConsoleFindingService,
    WorkbenchApprovalConsoleReportService,
)


def test_missing_sources_warn_without_fabricating_execution_or_raw_data() -> None:
    parts = WorkbenchApprovalConsoleReportService().build_all_parts(
        view_state_available=False,
        safety_gate_panel_available=False,
        approval_console_panel_available=False,
        safety_gate_available=False,
        evidence_inspector_available=False,
        pig_guidance_available=False,
        strictness="standard",
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert "missing_workbench_view_state" in finding_types
    assert "missing_safety_gate_panel" in finding_types
    assert "missing_approval_console_panel" in finding_types
    assert "missing_safety_gate_report" in finding_types
    assert "missing_evidence_inspector_report" in finding_types
    assert report.approval_executed is False
    assert report.approval_token_executed is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False


def test_strict_missing_mandatory_refs_fails_but_does_not_execute() -> None:
    parts = WorkbenchApprovalConsoleReportService().build_all_parts(
        safety_gate_available=False,
        evidence_inspector_available=False,
        strictness="strict",
    )
    report = parts["report"]

    assert report.report_status == "failed"
    assert report.safety_gate_view_created is True
    assert report.approval_console_view_created is True
    assert report.approval_executed is False
    assert report.auto_approval_performed is False
    assert report.command_executed is False
    assert report.route_rerun_performed is False
    assert report.local_command_executed is False
    assert report.memory_promoted is False
    assert report.persona_mutated is False


def test_forbidden_attempt_findings_block_release() -> None:
    blocked_types = [
        "approval_execution_attempted",
        "approval_token_execution_attempted",
        "auto_approval_attempted",
        "command_execution_attempted",
        "provider_invocation_attempted",
        "route_rerun_attempted",
        "stage_rerun_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "automatic_repair_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_adapter_detected",
        "vendor_adapter_detected",
        "schumpeter_split_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_detected",
        "raw_transcript_persistence_detected",
        "llm_judge_detected",
    ]
    for finding_type in blocked_types:
        parts = WorkbenchApprovalConsoleReportService().build_all_parts(extra_findings=[finding_type])
        assert parts["report"].report_status == "blocked", finding_type
        assert finding_type in WorkbenchApprovalConsoleFindingService.BLOCKED_FINDINGS


def test_approve_reject_defer_cli_commands_record_only(capsys) -> None:
    for decision in ["approve", "reject", "defer"]:
        assert main(
            [
                "workbench",
                "approval",
                "decide",
                "--candidate-id",
                "candidate-1",
                "--decision",
                decision,
            ]
        ) == 0
        output = capsys.readouterr().out
        assert f"decision_type={decision}" in output
        assert "decision_record_created=true" in output
        assert "decision_creates_execution=false" in output
        assert "approval_executed=false" in output
        assert "command_executed=false" in output
        assert "provider_invoked=false" in output
        assert "local_command_executed=false" in output


def test_changed_v0265_files_do_not_contain_forbidden_true_markers() -> None:
    paths = [
        Path("src/chanta_core/workspace_agent_workbench/safety_approval.py"),
        Path("tests/test_workbench_safety_approval_console.py"),
        Path("tests/test_workbench_safety_approval_console_boundaries.py"),
        Path("docs/versions/v0.26/v0.26.5_safety_gate_approval_console.md"),
    ]
    forbidden_true_markers = [
        name + "=True"
        for name in [
            "approval_executed",
            "approval_token_executed",
            "auto_approval_performed",
            "command_executed",
            "provider_invoked",
            "provider_invocation_performed",
            "route_rerun_performed",
            "stage_rerun_performed",
            "agent_ask_executed",
            "final_response_emitted",
            "local_command_executed",
            "command_rerun_performed",
            "automatic_repair_performed",
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
