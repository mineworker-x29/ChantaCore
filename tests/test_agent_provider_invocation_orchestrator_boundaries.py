from __future__ import annotations

from pathlib import Path

from chanta_core.agent_surface import AgentProviderInvocationReportService
from chanta_core.agent_surface.provider_invocation import AGENT_PROVIDER_INVOCATION_FORBIDDEN_EFFECT_TYPES


SOURCE_FILES = [
    Path("src/chanta_core/agent_surface/provider_invocation.py"),
    Path("docs/versions/v0.25/v0.25.5_internal_provider_invocation_orchestrator.md"),
]


def _source() -> str:
    return "\n".join(path.read_text(encoding="utf-8") for path in SOURCE_FILES)


def test_provider_invocation_source_has_no_direct_execution_bypass_markers() -> None:
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
        "response_assembled" + "=True",
        "final_response_emitted" + "=True",
        "direct_file_read_performed" + "=True",
        "direct_file_access_performed" + "=True",
        "direct_repository_search_performed" + "=True",
        "direct_process_inspection_performed" + "=True",
        "direct_subprocess_performed" + "=True",
        "direct_subprocess_called" + "=True",
        "direct_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
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
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "raw_provider_output_inline" + "=True",
        "workspace_workbench_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
    ]

    for marker in forbidden_exact:
        assert marker not in source


def test_provider_invocation_forbidden_effects_are_not_emitted() -> None:
    service = AgentProviderInvocationReportService()
    ocpx = service.build_ocpx_projection()

    for forbidden_effect in AGENT_PROVIDER_INVOCATION_FORBIDDEN_EFFECT_TYPES:
        assert forbidden_effect not in ocpx["effect_types"]
    assert "read_only_observation" in ocpx["effect_types"]
    assert "internal_provider_invoked" in ocpx["effect_types"]
    assert "agent_provider_evidence_seed_created" in ocpx["effect_types"]


def test_attempted_forbidden_actions_create_blocking_findings() -> None:
    service = AgentProviderInvocationReportService()
    report = service.build_report(
        "Explain the project structure",
        attempt_flags={
            "direct_file_access_attempted": True,
            "direct_repository_search_attempted": True,
            "direct_process_inspection_attempted": True,
            "direct_subprocess_attempted": True,
            "direct_local_command_execution_attempted": True,
            "command_rerun_attempted": True,
            "final_response_assembly_attempted_too_early": True,
            "ask_execution_attempted_too_early": True,
            "repl_execution_attempted_too_early": True,
            "memory_promotion_attempted": True,
            "persona_mutation_attempted": True,
            "external_provider_adapter_detected": True,
            "external_agent_adapter_detected": True,
            "opencode_runtime_dependency_detected": True,
            "openclaw_runtime_dependency_detected": True,
            "hermes_runtime_dependency_detected": True,
            "schumpeter_split_detected": True,
            "growthkernel_dependency_detected": True,
            "credential_exposure_detected": True,
            "raw_secret_output_detected": True,
            "llm_judge_detected": True,
        },
    )
    finding_types = {finding.finding_type for finding in report.findings}

    assert report.report_status == "blocked"
    assert "direct_file_access_attempted" in finding_types
    assert "direct_subprocess_attempted" in finding_types
    assert "direct_local_command_execution_attempted" in finding_types
    assert "final_response_assembly_attempted_too_early" in finding_types
    assert "ask_execution_attempted_too_early" in finding_types
    assert "repl_execution_attempted_too_early" in finding_types
    assert "external_provider_adapter_detected" in finding_types
    assert "opencode_runtime_dependency_detected" in finding_types
    assert "openclaw_runtime_dependency_detected" in finding_types
    assert "hermes_runtime_dependency_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "credential_exposure_detected" in finding_types
    assert "raw_secret_output_detected" in finding_types
    assert "llm_judge_detected" in finding_types
    assert report.provider_invoked is True
    assert report.final_response_assembled is False
    assert report.direct_file_access_performed is False
    assert report.direct_subprocess_performed is False
    assert report.direct_local_command_executed is False
    assert report.external_provider_invoked is False
    assert report.memory_promoted is False
    assert report.persona_mutated is False


def test_missing_provider_boundary_blocks_dispatch() -> None:
    step = AgentProviderInvocationReportService().build_report("Explain the project structure").invocation_plan.steps[0]
    step.provider_type = "unknown"
    step.boundary_checks = []
    dispatch = __import__(
        "chanta_core.agent_surface.provider_invocation",
        fromlist=["AgentProviderDispatchService"],
    ).AgentProviderDispatchService().dispatch_internal_provider(step)

    assert dispatch.dispatch_status == "blocked"
    assert dispatch.internal_provider_invoked is False
    assert dispatch.external_provider_invoked is False
