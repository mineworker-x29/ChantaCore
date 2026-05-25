import inspect
import re

import chanta_core.agent_surface.contract as agent_surface_module
from chanta_core.agent_surface import AgentSurfaceContractReportService


def test_agent_surface_contract_source_has_no_execution_or_adapter_paths() -> None:
    source = inspect.getsource(agent_surface_module)

    for forbidden in [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "ask_enabled_v0_25_0" + "=True",
        "repl_enabled_v0_25_0" + "=True",
        "tool_route_executed" + "=True",
        "tool_route_execution_enabled" + "=True",
        "provider_invocation_performed" + "=True",
        "provider_invocation_enabled" + "=True",
        "local_command_executed" + "=True",
        "local_runtime_execution_enabled" + "=True",
        "bounded_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "opencode_runtime_dependency_allowed" + "=True",
        "openclaw_runtime_dependency_allowed" + "=True",
        "hermes_runtime_dependency_allowed" + "=True",
        "memory_continuity_implemented" + "=True",
        "memory_promoted" + "=True",
        "persona_mutated" + "=True",
        "workspace_workbench_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "open" + "ai",
        "anth" + "ropic",
        "chat" + ".compl" + "etions",
        "eval" + "(",
    ]:
        assert forbidden not in source
    assert re.search(r"(?<![A-Za-z0-9_])shell" + r"=True", source) is None


def test_report_declares_all_executable_agent_surface_paths_disabled() -> None:
    report = AgentSurfaceContractReportService().build_report()

    assert report.ready_for_v0_25_1 is True
    assert report.ready_for_v0_26 is False
    assert report.agent_ask_enabled is False
    assert report.agent_repl_enabled is False
    assert report.tool_route_execution_enabled is False
    assert report.provider_invocation_enabled is False
    assert report.local_runtime_execution_enabled is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.memory_continuity_implemented is False
    assert report.workspace_workbench_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_routing_and_reference_boundaries_are_contract_only() -> None:
    contract = AgentSurfaceContractReportService().build_report().contract
    routing = contract.routing_boundary
    reference = contract.reference_architecture_policy

    assert routing.route_plan_enabled_v0_25_0 is False
    assert routing.provider_invocation_enabled_v0_25_0 is False
    assert routing.local_runtime_execution_enabled_v0_25_0 is False
    assert routing.ask_enabled_v0_25_0 is False
    assert routing.repl_enabled_v0_25_0 is False
    assert reference.direct_implementation_strategy is True
    assert reference.opencode_reference_allowed is True
    assert reference.openclaw_reference_allowed is True
    assert reference.hermes_reference_allowed is True
    assert reference.opencode_runtime_dependency_allowed is False
    assert reference.openclaw_runtime_dependency_allowed is False
    assert reference.hermes_runtime_dependency_allowed is False


def test_dangerous_agent_surface_safety_counts_are_zero() -> None:
    safety = AgentSurfaceContractReportService().build_report().contract.safety_boundary

    assert safety.agent_ask_execution_count == 0
    assert safety.agent_repl_execution_count == 0
    assert safety.tool_route_execution_count == 0
    assert safety.provider_invocation_count == 0
    assert safety.local_command_execution_count == 0
    assert safety.command_rerun_count == 0
    assert safety.unrestricted_shell_count == 0
    assert safety.arbitrary_subprocess_count == 0
    assert safety.external_provider_call_count == 0
    assert safety.external_agent_runtime_touch_count == 0
    assert safety.memory_promotion_count == 0
    assert safety.persona_mutation_count == 0
    assert safety.file_mutation_count == 0
    assert safety.credential_exposure_count == 0
    assert safety.raw_secret_output_count == 0
    assert safety.llm_judge_for_safety_count == 0
    assert safety.schumpeter_split_count == 0
