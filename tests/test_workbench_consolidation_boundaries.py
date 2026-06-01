from __future__ import annotations

from pathlib import Path

from chanta_core.cli.main import main
from chanta_core.workspace_agent_workbench.consolidation import (
    WorkbenchConsolidationFindingService,
    WorkbenchConsolidationReportService,
)


def test_missing_sources_warn_without_memory_execution_or_raw_output() -> None:
    parts = WorkbenchConsolidationReportService().build_all_parts(
        v0260_available=False,
        v0261_available=False,
        v0262_available=False,
        v0263_available=False,
        v0264_available=False,
        v0265_available=False,
        v0266_available=False,
        v0267_available=False,
        v0268_available=False,
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.readiness_status == "warning"
    assert "missing_contract_report" in finding_types
    assert "missing_view_state_report" in finding_types
    assert "missing_trace_explorer_report" in finding_types
    assert "missing_provider_browser_report" in finding_types
    assert "missing_evidence_inspector_report" in finding_types
    assert "missing_approval_console_report" in finding_types
    assert "missing_dashboard_report" in finding_types
    assert "missing_command_surface_report" in finding_types
    assert "missing_snapshot_export_report" in finding_types
    assert report.ready_for_v0_28 is False
    assert report.memory_candidate_created is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.file_mutated is False
    assert report.patch_applied is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.raw_transcript_persisted is False
    assert report.raw_provider_output_inline is False
    assert report.raw_secret_output is False


def test_strict_missing_sources_blocks_readiness_without_creating_memory() -> None:
    report = WorkbenchConsolidationReportService().build_all_parts(
        strictness="strict",
        v0260_available=False,
    )["report"]

    assert report.readiness_status == "blocked"
    assert report.release_status == "blocked"
    assert report.ready_for_v0_27 is False
    assert report.ready_for_v0_28 is False
    assert report.memory_candidate_created is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.command_executed is False
    assert report.provider_invoked is False
    assert report.file_mutated is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False


def test_forbidden_attempt_findings_block_consolidation() -> None:
    service = WorkbenchConsolidationReportService()
    for finding_type in WorkbenchConsolidationFindingService.BLOCKED_FINDINGS:
        report = service.build_all_parts(extra_findings=[finding_type])["report"]
        finding_types = {finding.finding_type for finding in report.findings}

        assert report.readiness_status == "blocked"
        assert report.release_status == "blocked"
        assert report.ready_for_v0_27 is False
        assert finding_type in finding_types


def test_consolidation_cli_commands_are_readiness_only(capsys) -> None:
    commands = [
        ["workbench", "consolidate"],
        ["workbench", "release-manifest"],
        ["workbench", "readiness", "--target", "v0.27"],
        ["workbench", "coverage"],
        ["workbench", "safety-boundary"],
        ["workbench", "interaction-boundary"],
        ["workbench", "quality"],
        ["workbench", "trace-coverage"],
        ["workbench", "usability"],
        ["workbench", "feedback-loop"],
        ["workbench", "gaps"],
        ["workbench", "handoff", "--target", "v0.27"],
        ["workbench", "consolidation-report", "--report-id", "consolidation-report:test"],
    ]

    for command in commands:
        assert main(command) == 0
        output = capsys.readouterr().out
        assert "version=v0.26.9" in output
        assert "release_name=Workspace Agent Workbench Foundation v1" in output
        assert "ready_for_v0_27=true" in output
        assert "ready_for_v0_28=false" in output
        assert "memory_candidate_created=false" in output
        assert "memory_promoted=false" in output
        assert "persistent_memory_written=false" in output
        assert "persona_mutated=false" in output
        assert "command_executed=false" in output
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
        assert "external_provider_adapter_implemented=false" in output
        assert "vendor_adapter_implemented=false" in output
        assert "pm4py_runtime_dependency_added=false" in output
        assert "ocpa_runtime_dependency_added=false" in output
        assert "pig_memory_promoted=false" in output
        assert "pig_policy_mutated=false" in output
        assert "pig_executed=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "raw_transcript_persisted=false" in output
        assert "raw_provider_output_inline=false" in output
        assert "raw_secret_output=false" in output
        assert "llm_judge_used=false" in output


def test_v0269_changed_files_do_not_contain_forbidden_true_markers() -> None:
    root = Path(__file__).resolve().parents[1]
    paths = [
        root / "src" / "chanta_core" / "workspace_agent_workbench" / "consolidation.py",
        root / "tests" / "test_workbench_consolidation.py",
        root / "tests" / "test_workbench_consolidation_boundaries.py",
        root / "docs" / "versions" / "v0.26" / "v0.26.9_workspace_agent_workbench_consolidation.md",
    ]
    forbidden_names = [
        "memory_candidate_created",
        "memory_promoted",
        "persistent_memory_written",
        "persona_mutated",
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
        "external_provider_adapter_implemented",
        "external_agent_adapter_implemented",
        "vendor_adapter_implemented",
        "pm4py_runtime_dependency_added",
        "ocpa_runtime_dependency_added",
        "pig_memory_promoted",
        "pig_policy_mutated",
        "pig_executed",
        "schumpeter_split_introduced",
        "raw_transcript_persisted",
        "raw_provider_output_inline",
        "raw_secret_output",
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
