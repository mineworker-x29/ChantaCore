from __future__ import annotations

from pathlib import Path

from chanta_core.workspace_agent_workbench import (
    WORKBENCH_PROVIDER_BROWSER_EFFECT_TYPES,
    WORKBENCH_PROVIDER_BROWSER_FORBIDDEN_EFFECT_TYPES,
    WorkbenchProviderBrowserReportService,
)


def test_missing_view_state_blocks_without_invocation_or_raw_data() -> None:
    parts = WorkbenchProviderBrowserReportService().build_all_parts(view_state_available=False)
    report = parts["report"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert report.report_status == "blocked"
    assert report.ready_for_v0_26_4 is False
    assert "missing_workbench_view_state" in finding_types
    assert "missing_provider_browser_panel" in finding_types
    assert report.provider_invoked is False
    assert report.provider_test_run_performed is False
    assert report.provider_boundary_bypassed is False
    assert report.external_provider_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.local_command_executed is False
    assert report.memory_promoted is False
    assert report.raw_secret_output is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False


def test_missing_registry_or_capability_surface_fails_without_fabricated_provider_data() -> None:
    parts = WorkbenchProviderBrowserReportService().build_all_parts(
        provider_registry_available=False,
        capability_surface_available=False,
    )
    report = parts["report"]
    source = parts["source_view"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert source.source_status == "partial"
    assert source.provider_count == 0
    assert source.capability_count == 0
    assert parts["provider_cards"] == []
    assert parts["capability_cards"] == []
    assert report.report_status == "failed"
    assert report.ready_for_v0_26_4 is False
    assert "missing_provider_registry" in finding_types
    assert "missing_capability_surface" in finding_types
    assert report.provider_invoked is False
    assert report.provider_test_run_performed is False
    assert report.external_provider_adapter_implemented is False
    assert report.vendor_adapter_implemented is False
    assert report.raw_provider_output_inline is False


def test_optional_routing_and_pig_guidance_missing_warns_but_stays_view_only() -> None:
    parts = WorkbenchProviderBrowserReportService().build_all_parts(
        routing_available=False,
        pig_guidance_available=False,
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in parts["findings"]}

    assert report.report_status == "warning"
    assert report.ready_for_v0_26_4 is True
    assert report.provider_cards_created is True
    assert report.capability_cards_created is True
    assert report.selection_rationale_views_created is False
    assert report.pig_guidance_views_created is False
    assert "missing_route_report" in finding_types
    assert "missing_provider_selection" in finding_types
    assert report.provider_invoked is False
    assert report.provider_test_run_performed is False
    assert report.pig_memory_promoted is False
    assert report.pig_policy_mutated is False
    assert report.pig_executed is False


def test_dangerous_attempt_findings_block_provider_browser_report() -> None:
    blocked_attempts = [
        "external_adapter_detected",
        "vendor_adapter_detected",
        "pm4py_runtime_dependency_detected",
        "ocpa_runtime_dependency_detected",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "provider_test_run_attempted",
        "provider_boundary_bypass_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "automatic_repair_attempted",
        "memory_promotion_attempted",
        "persona_mutation_attempted",
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
        parts = WorkbenchProviderBrowserReportService().build_all_parts(attempt_flags={finding_type: True})
        report = parts["report"]
        finding_types = {finding.finding_type for finding in parts["findings"]}
        assert report.report_status == "blocked"
        assert report.ready_for_v0_26_4 is False
        assert finding_type in finding_types
        assert report.actual_ui_rendered is False
        assert report.panel_rendered is False
        assert report.provider_invoked is False
        assert report.provider_test_run_performed is False
        assert report.provider_boundary_bypassed is False
        assert report.external_provider_adapter_implemented is False
        assert report.vendor_adapter_implemented is False
        assert report.pig_memory_promoted is False
        assert report.pig_policy_mutated is False
        assert report.pig_executed is False
        assert report.local_command_executed is False
        assert report.memory_promoted is False
        assert report.raw_secret_output is False
        assert report.raw_provider_output_inline is False
        assert report.llm_judge_used is False


def test_forbidden_effects_are_declared_but_not_emitted() -> None:
    parts = WorkbenchProviderBrowserReportService().build_all_parts()
    ocpx = parts["ocpx_projection"]

    assert set(ocpx["effect_types"]) == set(WORKBENCH_PROVIDER_BROWSER_EFFECT_TYPES)
    assert not set(ocpx["effect_types"]).intersection(WORKBENCH_PROVIDER_BROWSER_FORBIDDEN_EFFECT_TYPES)


def test_source_files_do_not_add_forbidden_runtime_patterns() -> None:
    checked_files = [
        Path("src/chanta_core/workspace_agent_workbench/provider_browser.py"),
        Path("src/chanta_core/workspace_agent_workbench/__init__.py"),
        Path("src/chanta_core/cli/main.py"),
        Path("docs/versions/v0.26/v0.26.3_provider_capability_browser.md"),
        Path("tests/test_workbench_provider_capability_browser.py"),
    ]
    forbidden_literals = [
        "Re" + "act",
        "V" + "ue",
        "Fast" + "API",
        "Fla" + "sk",
        "server_started" + "=True",
        "provider_invocation_performed" + "=True",
        "provider_invoked" + "=True",
        "provider_test_run_performed" + "=True",
        "provider_boundary_bypassed" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "vendor_adapter_implemented" + "=True",
        "pm4py_runtime_dependency_added" + "=True",
        "ocpa_runtime_dependency_added" + "=True",
        "pig_memory_promoted" + "=True",
        "pig_policy_mutated" + "=True",
        "pig_executed" + "=True",
        "automatic_repair_performed" + "=True",
        "command_rerun_performed" + "=True",
        "autonomous_loop_started" + "=True",
        "background_execution_started" + "=True",
        "memory_candidate_created" + "=True",
        "memory_continuity_implemented" + "=True",
        "memory_promoted" + "=True",
        "persistent_memory_written" + "=True",
        "persona_mutated" + "=True",
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


def test_reference_vendor_and_process_mining_terms_are_policy_only() -> None:
    doc_text = Path("docs/versions/v0.26/v0.26.3_provider_capability_browser.md").read_text(encoding="utf-8")
    module_text = Path("src/chanta_core/workspace_agent_workbench/provider_browser.py").read_text(encoding="utf-8")

    assert "reference architectures only" in doc_text
    assert "runtime dependencies" in doc_text
    assert "opencode_runtime_dependency_detected" in module_text
    assert "openclaw_runtime_dependency_detected" in module_text
    assert "hermes_runtime_dependency_detected" in module_text
    assert "import opencode" not in module_text.lower()
    assert "import openclaw" not in module_text.lower()
    assert "import hermes" not in module_text.lower()
    for vendor in ["A" + "360", "Automation " + "Anywhere", "Br" + "ity", "Ui" + "Path", "Power " + "Automate"]:
        assert vendor not in module_text
    assert "import pm4" + "py" not in module_text
    assert "import oc" + "pa" not in module_text
