from __future__ import annotations

from pathlib import Path

from chanta_core.agent_surface import AgentTraceTelemetryReportService
from chanta_core.agent_surface.trace_telemetry import AGENT_TRACE_FORBIDDEN_EFFECT_TYPES


SOURCE_FILES = [
    Path("src/chanta_core/agent_surface/trace_telemetry.py"),
    Path("docs/versions/v0.25/v0.25.8_agent_trace_usability_telemetry.md"),
]


def _source() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_FILES)


def test_trace_telemetry_source_has_no_direct_execution_or_persistence_markers() -> None:
    source = _source()
    forbidden_exact = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "exec" + "(",
        "eval" + "(",
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "agent_repl_turn_executed" + "=True",
        "final_response_emitted" + "=True",
        "provider_invocation_performed" + "=True",
        "provider_invoked" + "=True",
        "direct_file_read_performed" + "=True",
        "direct_file_access_performed" + "=True",
        "direct_repository_search_performed" + "=True",
        "direct_process_inspection_performed" + "=True",
        "direct_subprocess_performed" + "=True",
        "direct_local_command_executed" + "=True",
        "local_command_executed" + "=True",
        "bounded_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
        "background_telemetry_daemon_started" + "=True",
        "continuous_watcher_started" + "=True",
        "autonomous_optimization_loop_started" + "=True",
        "autonomous_optimization_performed" + "=True",
        "workspace_workbench_implemented" + "=True",
        "memory_candidate_created" + "=True",
        "memory_continuity_implemented" + "=True",
        "memory_promoted" + "=True",
        "persistent_memory_written" + "=True",
        "persona_mutated" + "=True",
        "file_write_performed" + "=True",
        "file_edit_performed" + "=True",
        "file_delete_performed" + "=True",
        "patch_applied" + "=True",
        "automatic_repair_performed" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "external_provider_invoked" + "=True",
        "external_agent_runtime_touched" + "=True",
        "opencode_runtime_dependency_allowed" + "=True",
        "openclaw_runtime_dependency_allowed" + "=True",
        "hermes_runtime_dependency_allowed" + "=True",
        "raw_user_secret_persisted" + "=True",
        "raw_transcript_persisted" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "raw_provider_output_inline" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
    ]

    for marker in forbidden_exact:
        assert marker not in source


def test_trace_telemetry_forbidden_effects_are_not_emitted() -> None:
    ocpx = AgentTraceTelemetryReportService().build_ocpx_projection()

    for forbidden_effect in AGENT_TRACE_FORBIDDEN_EFFECT_TYPES:
        assert forbidden_effect not in ocpx["effect_types"]
    assert "agent_surface_trace_recorded" in ocpx["effect_types"]
    assert "agent_turn_ocel_projected" in ocpx["effect_types"]
    assert "agent_usability_telemetry_created" in ocpx["effect_types"]


def test_attempted_forbidden_trace_actions_create_blocking_findings() -> None:
    report = AgentTraceTelemetryReportService().build_report(
        ask_report_id="ask-report:test",
        attempt_flags={
            "raw_transcript_persistence_attempted": True,
            "raw_provider_output_persistence_attempted": True,
            "raw_secret_persistence_attempted": True,
            "telemetry_background_daemon_attempted": True,
            "continuous_watcher_attempted": True,
            "autonomous_optimization_attempted": True,
            "ask_execution_attempted": True,
            "repl_execution_attempted": True,
            "provider_invocation_attempted": True,
            "local_command_execution_attempted": True,
            "direct_file_access_attempted": True,
            "direct_subprocess_attempted": True,
            "command_rerun_attempted": True,
            "memory_promotion_attempted": True,
            "persistent_memory_write_attempted": True,
            "persona_mutation_attempted": True,
            "workspace_workbench_attempted": True,
            "external_provider_adapter_detected": True,
            "external_agent_adapter_detected": True,
            "opencode_runtime_dependency_detected": True,
            "openclaw_runtime_dependency_detected": True,
            "hermes_runtime_dependency_detected": True,
            "schumpeter_split_detected": True,
            "credential_exposure_detected": True,
            "raw_secret_output_detected": True,
            "raw_provider_output_inline_detected": True,
            "llm_judge_detected": True,
        },
    )
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "blocked"
    assert "raw_transcript_persistence_attempted" in finding_types
    assert "raw_provider_output_persistence_attempted" in finding_types
    assert "raw_secret_persistence_attempted" in finding_types
    assert "telemetry_background_daemon_attempted" in finding_types
    assert "continuous_watcher_attempted" in finding_types
    assert "autonomous_optimization_attempted" in finding_types
    assert "ask_execution_attempted" in finding_types
    assert "repl_execution_attempted" in finding_types
    assert "provider_invocation_attempted" in finding_types
    assert "local_command_execution_attempted" in finding_types
    assert "direct_file_access_attempted" in finding_types
    assert "direct_subprocess_attempted" in finding_types
    assert "command_rerun_attempted" in finding_types
    assert "memory_promotion_attempted" in finding_types
    assert "persistent_memory_write_attempted" in finding_types
    assert "persona_mutation_attempted" in finding_types
    assert "workspace_workbench_attempted" in finding_types
    assert "external_provider_adapter_detected" in finding_types
    assert "external_agent_adapter_detected" in finding_types
    assert "opencode_runtime_dependency_detected" in finding_types
    assert "openclaw_runtime_dependency_detected" in finding_types
    assert "hermes_runtime_dependency_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types
    assert "credential_exposure_detected" in finding_types
    assert "raw_secret_output_detected" in finding_types
    assert "raw_provider_output_inline_detected" in finding_types
    assert "llm_judge_detected" in finding_types
    assert report.ask_executed is False
    assert report.final_response_emitted is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.background_collection_started is False
    assert report.autonomous_optimization_performed is False
    assert report.workspace_workbench_implemented is False
    assert report.raw_transcript_persisted is False


def test_trace_text_sanitization_reuses_agent_surface_redaction() -> None:
    module = __import__("chanta_core.agent_surface.trace_telemetry", fromlist=["_sanitize_text"])
    sanitized = module._sanitize_text(r"Trace D:\private\secret.txt token=abc123")

    assert "[private-path]" in sanitized
    assert "token=[redacted]" in sanitized
    assert "abc123" not in sanitized
