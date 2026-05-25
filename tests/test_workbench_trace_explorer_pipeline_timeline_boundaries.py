from __future__ import annotations

from pathlib import Path

from chanta_core.workspace_agent_workbench import (
    WORKBENCH_TRACE_EXPLORER_EFFECT_TYPES,
    WORKBENCH_TRACE_EXPLORER_FORBIDDEN_EFFECT_TYPES,
    WorkbenchTraceExplorerReportService,
)


def test_missing_view_state_blocks_without_execution_or_raw_data() -> None:
    parts = WorkbenchTraceExplorerReportService().build_all_parts(view_state_available=False)
    report = parts["report"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert report.report_status == "blocked"
    assert report.ready_for_v0_26_3 is False
    assert "missing_workbench_view_state" in finding_types
    assert "missing_trace_explorer_panel" in finding_types
    assert "missing_pipeline_timeline_panel" in finding_types
    assert report.actual_ui_rendered is False
    assert report.panel_rendered is False
    assert report.trace_mutated is False
    assert report.stage_rerun_performed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.memory_promoted is False
    assert report.external_provider_adapter_implemented is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False


def test_missing_surface_trace_blocks_without_fabricated_trace_data() -> None:
    parts = WorkbenchTraceExplorerReportService().build_all_parts(trace_available=False)
    report = parts["report"]
    source_view = parts["source_view"]
    timeline = parts["timeline"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert source_view.source_status == "blocked"
    assert timeline.timeline_status == "blocked"
    assert report.report_status == "blocked"
    assert report.ready_for_v0_26_3 is False
    assert "missing_surface_trace" in finding_types
    assert "missing_ocel_projection" in finding_types
    assert "missing_stage_trace" in finding_types
    assert "missing_decision_trace" in finding_types
    assert report.stage_nodes_created is False
    assert report.decision_nodes_created is False
    assert report.trace_mutated is False
    assert report.stage_rerun_performed is False
    assert report.provider_invoked is False
    assert report.raw_transcript_persisted is False


def test_optional_route_provider_response_missing_warns_but_preserves_readiness() -> None:
    parts = WorkbenchTraceExplorerReportService().build_all_parts(
        route_trace_available=False,
        provider_trace_available=False,
        response_trace_available=False,
    )
    report = parts["report"]
    source_view = parts["source_view"]
    timeline = parts["timeline"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert source_view.source_status == "partial"
    assert timeline.timeline_status == "partial"
    assert report.report_status == "warning"
    assert report.ready_for_v0_26_3 is True
    assert "missing_route_trace" in finding_types
    assert "missing_provider_trace" in finding_types
    assert "missing_response_trace" in finding_types
    assert "partial_trace_source" in finding_types
    assert report.stage_nodes_created is True
    assert report.decision_nodes_created is True
    assert report.provider_invoked is False
    assert report.final_response_emitted is False
    assert report.local_command_executed is False
    assert report.memory_promoted is False


def test_dangerous_attempt_findings_block_trace_explorer_report() -> None:
    blocked_attempts = [
        "raw_transcript_inline_attempted",
        "raw_provider_output_inline_attempted",
        "raw_secret_inline_attempted",
        "trace_mutation_attempted",
        "stage_rerun_attempted",
        "route_rerun_attempted",
        "provider_invocation_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
        "external_adapter_detected",
        "schumpeter_split_detected",
        "opencode_runtime_dependency_detected",
        "openclaw_runtime_dependency_detected",
        "hermes_runtime_dependency_detected",
        "credential_exposure_detected",
        "raw_secret_output_detected",
        "raw_provider_output_detected",
        "raw_transcript_persistence_detected",
        "llm_" + "judge_detected",
    ]
    for finding_type in blocked_attempts:
        parts = WorkbenchTraceExplorerReportService().build_all_parts(attempt_flags={finding_type: True})
        report = parts["report"]
        finding_types = {finding.finding_type for finding in parts["findings"]}
        assert report.report_status == "blocked"
        assert report.ready_for_v0_26_3 is False
        assert finding_type in finding_types
        assert report.actual_ui_rendered is False
        assert report.panel_rendered is False
        assert report.trace_mutated is False
        assert report.stage_rerun_performed is False
        assert report.route_rerun_performed is False
        assert report.provider_invoked is False
        assert report.local_command_executed is False
        assert report.memory_promoted is False
        assert report.external_provider_adapter_implemented is False
        assert report.raw_secret_output is False
        assert report.llm_judge_used is False


def test_forbidden_effects_are_declared_but_not_emitted() -> None:
    parts = WorkbenchTraceExplorerReportService().build_all_parts()
    ocpx = parts["ocpx_projection"]

    assert set(ocpx["effect_types"]) == set(WORKBENCH_TRACE_EXPLORER_EFFECT_TYPES)
    assert not set(ocpx["effect_types"]).intersection(WORKBENCH_TRACE_EXPLORER_FORBIDDEN_EFFECT_TYPES)


def test_source_files_do_not_add_forbidden_runtime_patterns() -> None:
    checked_files = [
        Path("src/chanta_core/workspace_agent_workbench/trace_explorer.py"),
        Path("src/chanta_core/workspace_agent_workbench/__init__.py"),
        Path("src/chanta_core/cli/main.py"),
        Path("docs/versions/v0.26/v0.26.2_trace_explorer_pipeline_timeline.md"),
        Path("tests/test_workbench_trace_explorer_pipeline_timeline.py"),
    ]
    forbidden_literals = [
        "Re" + "act",
        "V" + "ue",
        "Fast" + "API",
        "Fla" + "sk",
        "server_started" + "=True",
        "workbench_ui_implemented" + "=True",
        "workbench_panel_rendered" + "=True",
        "actual_ui_rendered" + "=True",
        "panel_rendered" + "=True",
        "stage_rerun_performed" + "=True",
        "route_rerun_performed" + "=True",
        "provider_browser_implemented" + "=True",
        "evidence_inspector_implemented" + "=True",
        "approval_console_implemented" + "=True",
        "run_dashboard_implemented" + "=True",
        "command_surface_implemented" + "=True",
        "snapshot_export_implemented" + "=True",
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "final_response_emitted" + "=True",
        "provider_invocation_performed" + "=True",
        "provider_invoked" + "=True",
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
        "schumpeter_split_introduced" + "=True",
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


def test_reference_architectures_and_vendor_terms_are_policy_only() -> None:
    doc_text = Path("docs/versions/v0.26/v0.26.2_trace_explorer_pipeline_timeline.md").read_text(encoding="utf-8")
    module_text = Path("src/chanta_core/workspace_agent_workbench/trace_explorer.py").read_text(encoding="utf-8")

    assert "reference architectures only" in doc_text
    assert "runtime dependency" in doc_text
    assert "opencode_runtime_dependency_detected" in module_text
    assert "openclaw_runtime_dependency_detected" in module_text
    assert "hermes_runtime_dependency_detected" in module_text
    assert "import opencode" not in module_text.lower()
    assert "import openclaw" not in module_text.lower()
    assert "import hermes" not in module_text.lower()
    vendors = ["A" + "360", "Automation " + "Anywhere", "Br" + "ity", "Ui" + "Path", "Power " + "Automate"]
    for vendor in vendors:
        assert vendor not in module_text
