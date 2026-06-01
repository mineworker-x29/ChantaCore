from __future__ import annotations

from pathlib import Path

from chanta_core.workspace_agent_workbench import (
    WorkbenchEvidenceInspectorFindingService,
    WorkbenchEvidenceInspectorReportService,
)


def test_missing_optional_sources_create_warnings_without_fabricating_raw_data() -> None:
    parts = WorkbenchEvidenceInspectorReportService().build_all_parts(
        view_state_available=False,
        evidence_inspector_panel_available=False,
        response_assembly_available=False,
        safety_gate_available=False,
        routing_available=False,
        provider_browser_available=False,
        pig_guidance_available=False,
        strictness="standard",
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "warning"
    assert "missing_workbench_view_state" in finding_types
    assert "missing_evidence_inspector_panel" in finding_types
    assert "missing_response_assembly_report" in finding_types
    assert "missing_evidence_bundle" in finding_types
    assert "missing_safety_gate_report" in finding_types
    assert "missing_route_report" in finding_types
    assert "missing_pig_guidance_refs" in finding_types
    assert report.source_view.raw_provider_output_included is False
    assert report.source_view.raw_transcript_included is False
    assert report.source_view.raw_secret_included is False
    assert report.raw_provider_output_inline is False
    assert report.raw_transcript_persisted is False
    assert report.raw_secret_output is False


def test_strict_missing_core_sources_fail_but_do_not_execute() -> None:
    parts = WorkbenchEvidenceInspectorReportService().build_all_parts(
        response_assembly_available=False,
        evidence_bundle_available=False,
        strictness="strict",
    )
    report = parts["report"]

    assert report.report_status == "failed"
    assert report.evidence_inspector_view_created is True
    assert report.response_rewritten is False
    assert report.provider_invoked is False
    assert report.route_rerun_performed is False
    assert report.approval_executed is False
    assert report.local_command_executed is False
    assert report.memory_promoted is False
    assert report.persona_mutated is False


def test_forbidden_attempt_findings_block_release() -> None:
    blocked_types = [
        "raw_provider_output_inline_attempted",
        "raw_transcript_inline_attempted",
        "raw_secret_inline_attempted",
        "response_rewrite_attempted",
        "factuality_llm_judge_detected",
        "safety_llm_judge_detected",
        "decision_mutation_attempted",
        "safety_policy_mutation_attempted",
        "pig_guidance_as_memory_detected",
        "pig_policy_mutation_detected",
        "pig_execution_detected",
        "provider_invocation_attempted",
        "route_rerun_attempted",
        "stage_rerun_attempted",
        "approval_execution_attempted",
        "ask_execution_attempted",
        "final_response_emission_attempted",
        "local_command_execution_attempted",
        "direct_file_access_attempted",
        "direct_subprocess_attempted",
        "command_rerun_attempted",
        "automatic_repair_attempted",
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
        parts = WorkbenchEvidenceInspectorReportService().build_all_parts(extra_findings=[finding_type])
        assert parts["report"].report_status == "blocked", finding_type
        assert finding_type in WorkbenchEvidenceInspectorFindingService.BLOCKED_FINDINGS


def test_attempt_flags_block_without_setting_success_flags_true() -> None:
    parts = WorkbenchEvidenceInspectorReportService().build_all_parts(
        attempt_flags={
            "provider_invocation_attempted": True,
            "approval_execution_attempted": True,
            "response_rewrite_attempted": True,
        }
    )
    report = parts["report"]

    assert report.report_status == "blocked"
    assert report.provider_invoked is False
    assert report.approval_executed is False
    assert report.response_rewritten is False
    assert report.factuality_llm_judge_used is False
    assert report.local_command_executed is False


def test_changed_v0264_files_do_not_contain_forbidden_true_markers() -> None:
    paths = [
        Path("src/chanta_core/workspace_agent_workbench/evidence_inspector.py"),
        Path("tests/test_workbench_evidence_report_inspector.py"),
        Path("tests/test_workbench_evidence_report_inspector_boundaries.py"),
        Path("docs/versions/v0.26/v0.26.4_evidence_report_inspector.md"),
    ]
    forbidden_true_markers = [
        name + "=True"
        for name in [
            "response_rewritten",
            "response_regenerated",
            "factuality_llm_judge_used",
            "safety_llm_judge_used",
            "provider_invoked",
            "provider_test_run_performed",
            "route_rerun_performed",
            "stage_rerun_performed",
            "approval_executed",
            "agent_ask_executed",
            "final_response_emitted",
            "local_command_executed",
            "command_rerun_performed",
            "automatic_repair_performed",
            "memory_candidate_created",
            "memory_continuity_implemented",
            "memory_promoted",
            "persistent_memory_written",
            "persona_mutated",
            "external_provider_adapter_implemented",
            "external_agent_adapter_implemented",
            "vendor_adapter_implemented",
            "pig_memory_promoted",
            "pig_policy_mutated",
            "pig_executed",
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
        assert "chat" + ".completions" not in text
