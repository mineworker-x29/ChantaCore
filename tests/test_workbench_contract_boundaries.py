from __future__ import annotations

from pathlib import Path

from chanta_core.workspace_agent_workbench import (
    WORKBENCH_CONTRACT_EFFECT_TYPES,
    WORKBENCH_CONTRACT_FORBIDDEN_EFFECT_TYPES,
    WorkbenchContractReportService,
)


def test_missing_v0259_release_is_warning_not_execution() -> None:
    parts = WorkbenchContractReportService().build_all_parts(v0259_available=False)
    report = parts["report"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert report.report_status == "warning"
    assert report.ready_for_v0_26_1 is True
    assert "missing_v0259_release" in finding_types
    assert report.ask_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.raw_transcript_persisted is False


def test_dangerous_attempt_findings_block_contract_report() -> None:
    blocked_attempts = [
        "workbench_ui_implemented_too_early",
        "trace_explorer_implemented_too_early",
        "provider_browser_implemented_too_early",
        "evidence_inspector_implemented_too_early",
        "approval_console_implemented_too_early",
        "run_dashboard_implemented_too_early",
        "command_surface_implemented_too_early",
        "snapshot_export_implemented_too_early",
        "ask_execution_attempted",
        "provider_invocation_attempted",
        "direct_execution_attempted",
        "memory_promotion_attempted",
        "external_adapter_detected",
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
    for finding_type in blocked_attempts:
        parts = WorkbenchContractReportService().build_all_parts(attempt_flags={finding_type: True})
        report = parts["report"]
        finding_types = {finding.finding_type for finding in parts["findings"]}
        assert report.report_status == "blocked"
        assert report.ready_for_v0_26_1 is False
        assert finding_type in finding_types
        assert report.actual_ui_implemented is False
        assert report.provider_invoked is False
        assert report.memory_promoted is False
        assert report.external_provider_adapter_implemented is False
        assert report.raw_secret_output is False
        assert report.llm_judge_used is False


def test_forbidden_effects_are_declared_but_not_emitted() -> None:
    parts = WorkbenchContractReportService().build_all_parts()
    ocpx = parts["ocpx_projection"]

    assert set(ocpx["effect_types"]) == set(WORKBENCH_CONTRACT_EFFECT_TYPES)
    assert not set(ocpx["effect_types"]).intersection(WORKBENCH_CONTRACT_FORBIDDEN_EFFECT_TYPES)


def test_source_files_do_not_add_forbidden_runtime_patterns() -> None:
    checked_files = [
        Path("src/chanta_core/workspace_agent_workbench/contract.py"),
        Path("src/chanta_core/workspace_agent_workbench/__init__.py"),
        Path("src/chanta_core/cli/main.py"),
        Path("docs/versions/v0.26/v0.26.0_workspace_agent_workbench_contract.md"),
        Path("tests/test_workbench_contract.py"),
    ]
    forbidden_literals = [
        "Fast" + "API",
        "Fla" + "sk",
        "server_started" + "=True",
        "workbench_ui_implemented" + "=True",
        "workbench_panel_rendered" + "=True",
        "trace_explorer_implemented" + "=True",
        "provider_browser_implemented" + "=True",
        "evidence_inspector_implemented" + "=True",
        "approval_console_implemented" + "=True",
        "run_dashboard_implemented" + "=True",
        "command_surface_implemented" + "=True",
        "snapshot_export_implemented" + "=True",
        "agent_ask_executed" + "=True",
        "final_response_emitted" + "=True",
        "provider_invocation_performed" + "=True",
        "local_command_executed" + "=True",
        "direct_provider_invocation" + "=True",
        "direct_file_access_performed" + "=True",
        "direct_subprocess_performed" + "=True",
        "command_rerun_performed" + "=True",
        "autonomous_loop_started" + "=True",
        "background_execution_started" + "=True",
        "memory_candidate_created" + "=True",
        "memory_continuity_implemented" + "=True",
        "memory_promoted" + "=True",
        "persistent_memory_written" + "=True",
        "persona_mutated" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "raw_transcript_persisted" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "raw_provider_output_inline" + "=True",
        "growthkernel_dependency_required" + "=True",
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "chat" + ".com" + "pletions",
        "exec" + "(",
        "eval" + "(",
    ]
    for path in checked_files:
        text = path.read_text(encoding="utf-8")
        for forbidden in forbidden_literals:
            assert forbidden not in text


def test_reference_architectures_are_policy_only() -> None:
    doc_text = Path("docs/versions/v0.26/v0.26.0_workspace_agent_workbench_contract.md").read_text(encoding="utf-8")
    module_text = Path("src/chanta_core/workspace_agent_workbench/contract.py").read_text(encoding="utf-8")

    assert "reference architectures only" in doc_text
    assert "runtime dependency" in doc_text
    assert "opencode_runtime_dependency_detected" in module_text
    assert "openclaw_runtime_dependency_detected" in module_text
    assert "hermes_runtime_dependency_detected" in module_text
    assert "import opencode" not in module_text.lower()
    assert "import openclaw" not in module_text.lower()
    assert "import hermes" not in module_text.lower()
