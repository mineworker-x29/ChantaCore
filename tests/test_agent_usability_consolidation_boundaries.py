from __future__ import annotations

from pathlib import Path

from chanta_core.agent_surface import (
    AGENT_USABILITY_FORBIDDEN_EFFECT_TYPES,
    AgentSurfaceSafetyBoundaryReportService,
    AgentUsabilityConsolidationReportService,
)


def test_missing_required_subject_blocks_v026_readiness() -> None:
    parts = AgentUsabilityConsolidationReportService().build_all_parts(missing_subjects={"agent_trace_telemetry"})

    report = parts["report"]
    readiness = parts["v026_readiness_report"]
    manifest = parts["release_manifest"]

    assert readiness.ready_for_v0_26 is False
    assert "agent_trace_telemetry" in readiness.blockers
    assert report.readiness_status == "blocked"
    assert report.release_status == "blocked"
    assert report.ready_for_v0_26 is False
    assert manifest.release_status == "blocked"
    assert any(finding.finding_type == "missing_v0_25_subject" for finding in report.findings)


def test_dangerous_safety_counts_block_release() -> None:
    service = AgentSurfaceSafetyBoundaryReportService()
    safety = service.build_safety_boundary_report(dangerous_overrides={"direct_subprocess_count": 1})
    parts = AgentUsabilityConsolidationReportService().build_all_parts(dangerous_overrides={"direct_subprocess_count": 1})

    assert safety.status == "blocked"
    assert safety.direct_subprocess_count == 1
    assert parts["report"].readiness_status == "blocked"
    assert parts["report"].release_status == "blocked"
    assert parts["v026_readiness_report"].ready_for_v0_26 is False
    assert any(finding.finding_type == "unsafe_surface_boundary" for finding in parts["findings"])


def test_trace_telemetry_missing_blocks_handoff() -> None:
    parts = AgentUsabilityConsolidationReportService().build_all_parts(trace_available=False)

    assert parts["trace_telemetry_coverage_report"].coverage_status == "blocked"
    assert parts["v026_readiness_report"].ready_for_v0_26 is False
    assert parts["workbench_handoff_packet"].handoff_status == "blocked"
    assert any(finding.finding_type == "missing_trace_telemetry" for finding in parts["findings"])


def test_attempt_flags_create_blocking_findings_without_setting_execution_flags() -> None:
    parts = AgentUsabilityConsolidationReportService().build_all_parts(
        attempt_flags={
            "direct_provider_bypass_detected": True,
            "workspace_workbench_premature": True,
            "llm_judge_detected": True,
        }
    )
    report = parts["report"]
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.readiness_status == "blocked"
    assert report.new_ask_executed is False
    assert report.new_repl_turn_executed is False
    assert report.new_final_response_emitted is False
    assert report.new_provider_invocation_performed is False
    assert report.new_local_command_executed is False
    assert report.direct_provider_invocation is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.command_rerun_performed is False
    assert report.workspace_workbench_implemented is False
    assert report.memory_promoted is False
    assert report.raw_transcript_persisted is False
    assert report.llm_judge_used is False
    assert {"direct_provider_bypass_detected", "workspace_workbench_premature", "llm_judge_detected"} <= finding_types


def test_forbidden_effects_are_not_emitted_by_ocpx_effects() -> None:
    ocpx = AgentUsabilityConsolidationReportService().build_ocpx_projection()

    assert set(ocpx["effect_types"]).isdisjoint(AGENT_USABILITY_FORBIDDEN_EFFECT_TYPES)
    assert "read_only_observation" in ocpx["effect_types"]
    assert "agent_usability_consolidation_created" in ocpx["effect_types"]
    assert "agent_v026_readiness_created" in ocpx["effect_types"]
    assert "agent_workbench_handoff_packet_created" in ocpx["effect_types"]


def test_v0259_source_does_not_include_forbidden_runtime_calls_or_true_markers() -> None:
    source_paths = [
        Path("src/chanta_core/agent_surface/usability_consolidation.py"),
        Path("tests/test_agent_usability_consolidation.py"),
    ]
    combined = "\n".join(path.read_text(encoding="utf-8") for path in source_paths)
    forbidden_literals = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "final_response_emitted" + "=True",
        "provider_invocation_performed" + "=True",
        "direct_file_access_performed" + "=True",
        "direct_subprocess_performed" + "=True",
        "direct_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
        "autonomous_optimization_performed" + "=True",
        "workspace_workbench_implemented" + "=True",
        "memory_promoted" + "=True",
        "persistent_memory_written" + "=True",
        "persona_mutated" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "raw_transcript_persisted" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "raw_provider_output_inline" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
        "ex" + "ec(",
        "ev" + "al(",
    ]
    for literal in forbidden_literals:
        assert literal not in combined


def test_reference_architecture_mentions_are_policy_only() -> None:
    docs = Path("docs/versions/v0.25/v0.25.9_general_agent_usability_consolidation.md")
    if not docs.exists():
        return
    text = docs.read_text(encoding="utf-8")
    normalized = " ".join(text.split())

    assert "OpenCode / OpenClaw / Hermes remain reference architectures only" in normalized
    assert "runtime dependency" in normalized
    assert "Do not add runtime dependency" in normalized
