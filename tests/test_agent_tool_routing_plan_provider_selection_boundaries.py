from __future__ import annotations

import inspect

import chanta_core.agent_surface.tool_routing as tool_routing
from chanta_core.agent_surface import (
    AGENT_TOOL_ROUTING_FORBIDDEN_EFFECT_TYPES,
    AgentToolRoutingReportService,
)


def test_tool_routing_source_does_not_add_execution_or_provider_calls() -> None:
    source = inspect.getsource(tool_routing)
    forbidden_fragments = [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "shell" + "=True",
        "exec" + "(",
        "eval" + "(",
        "chat" + ".completions",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in source


def test_tool_routing_source_does_not_set_forbidden_true_markers() -> None:
    source = inspect.getsource(tool_routing)
    forbidden_true_markers = [
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "tool_route_executed" + "=True",
        "route_step_executed" + "=True",
        "provider_selection_executed" + "=True",
        "provider_execution_performed" + "=True",
        "provider_invocation_performed" + "=True",
        "provider_invocation_enabled" + "=True",
        "local_command_executed" + "=True",
        "local_runtime_execution_enabled" + "=True",
        "bounded_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
        "response_assembled" + "=True",
        "memory_candidate_created" + "=True",
        "memory_continuity_implemented" + "=True",
        "memory_promoted" + "=True",
        "persistent_memory_written" + "=True",
        "persona_mutated" + "=True",
        "external_provider_adapter_implemented" + "=True",
        "external_agent_adapter_implemented" + "=True",
        "raw_user_secret_persisted" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "workspace_workbench_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
    ]

    for marker in forbidden_true_markers:
        assert marker not in source


def test_tool_routing_forbidden_effects_are_not_emitted_effects() -> None:
    emitted = set(tool_routing.AGENT_TOOL_ROUTING_EFFECT_TYPES)
    forbidden = set(AGENT_TOOL_ROUTING_FORBIDDEN_EFFECT_TYPES)

    assert emitted.isdisjoint(forbidden)
    assert "tool_route_executed" not in emitted
    assert "provider_invoked" not in emitted
    assert "local_command_executed" not in emitted
    assert "agent_response_assembled" not in emitted
    assert "memory_promoted" not in emitted
    assert "credential_exposed" not in emitted
    assert "raw_secret_output" not in emitted


def test_attempt_flags_block_without_executing() -> None:
    report = AgentToolRoutingReportService().build_report(
        "Explain the project structure",
        attempt_flags={
            "route_execution_attempted": True,
            "provider_invocation_attempted": True,
            "local_command_execution_attempted": True,
            "response_assembly_attempted_too_early": True,
            "memory_promotion_attempted": True,
            "llm_judge_detected": True,
        },
    )

    assert report.report_status == "blocked"
    assert report.tool_route_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.response_assembled is False
    assert report.memory_promoted is False
    assert report.llm_judge_used is False


def test_reference_architecture_mentions_do_not_create_runtime_dependency() -> None:
    source = inspect.getsource(tool_routing)

    assert "import opencode" not in source.lower()
    assert "import openclaw" not in source.lower()
    assert "import hermes" not in source.lower()
    assert "runtime_dependency_allowed" not in source


def test_vendor_specific_runtime_logic_not_added_to_tool_routing() -> None:
    source = inspect.getsource(tool_routing).lower()

    for vendor in ["a360", "automation anywhere", "brity", "uipath", "power automate"]:
        assert vendor not in source
