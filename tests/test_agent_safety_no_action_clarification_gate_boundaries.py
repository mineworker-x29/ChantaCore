from __future__ import annotations

import inspect

import chanta_core.agent_surface.safety_gate as safety_gate
from chanta_core.agent_surface import (
    AGENT_SAFETY_GATE_FORBIDDEN_EFFECT_TYPES,
    AgentSafetyGateReportService,
)


def test_safety_gate_source_does_not_add_execution_or_routing_calls() -> None:
    source = inspect.getsource(safety_gate)
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


def test_safety_gate_source_does_not_set_forbidden_true_markers() -> None:
    source = inspect.getsource(safety_gate)
    forbidden_true_markers = [
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "tool_route_executed" + "=True",
        "agent_tool_route_plan_created" + "=True",
        "provider_selection_performed" + "=True",
        "provider_invocation_performed" + "=True",
        "provider_invocation_enabled" + "=True",
        "local_command_executed" + "=True",
        "local_runtime_execution_enabled" + "=True",
        "bounded_local_command_executed" + "=True",
        "command_rerun_performed" + "=True",
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


def test_safety_gate_forbidden_effects_are_not_emitted_effects() -> None:
    emitted = set(safety_gate.AGENT_SAFETY_GATE_EFFECT_TYPES)
    forbidden = set(AGENT_SAFETY_GATE_FORBIDDEN_EFFECT_TYPES)

    assert emitted.isdisjoint(forbidden)
    assert "agent_tool_route_plan_created" not in emitted
    assert "provider_invoked" not in emitted
    assert "local_command_executed" not in emitted
    assert "memory_promoted" not in emitted
    assert "credential_exposed" not in emitted
    assert "raw_secret_output" not in emitted


def test_attempt_flags_block_without_executing() -> None:
    report = AgentSafetyGateReportService().build_report(
        "Explain the project structure",
        attempt_flags={
            "provider_invocation_attempted": True,
            "tool_routing_attempted": True,
            "local_command_execution_attempted": True,
            "memory_promotion_attempted": True,
            "llm_judge_detected": True,
        },
    )

    assert report.report_status == "blocked"
    assert report.final_blocked_decision is True
    assert report.tool_route_created is False
    assert report.tool_route_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.memory_promoted is False
    assert report.llm_judge_used is False


def test_reference_architecture_mentions_do_not_create_runtime_dependency() -> None:
    source = inspect.getsource(safety_gate)

    assert "import opencode" not in source.lower()
    assert "import openclaw" not in source.lower()
    assert "import hermes" not in source.lower()
    assert "runtime_dependency_allowed" not in source


def test_vendor_specific_runtime_logic_not_added_to_safety_gate() -> None:
    source = inspect.getsource(safety_gate).lower()

    for vendor in ["a360", "automation anywhere", "brity", "uipath", "power automate"]:
        assert vendor not in source
