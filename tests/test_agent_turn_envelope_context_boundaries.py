import inspect
import re

import chanta_core.agent_surface.turn_context as turn_context_module
from chanta_core.agent_surface import AgentTurnReportService


def test_agent_turn_context_source_has_no_execution_or_adapter_paths() -> None:
    source = inspect.getsource(turn_context_module)

    for forbidden in [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "agent_intent_classified" + "=True",
        "agent_task_framed" + "=True",
        "agent_safety_gate_evaluated" + "=True",
        "tool_route_executed" + "=True",
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
        "opencode_runtime_dependency_allowed" + "=True",
        "openclaw_runtime_dependency_allowed" + "=True",
        "hermes_runtime_dependency_allowed" + "=True",
        "raw_user_secret_persisted" + "=True",
        "credential_exposed" + "=True",
        "raw_secret_output" + "=True",
        "workspace_workbench_implemented" + "=True",
        "schumpeter_split_introduced" + "=True",
        "growthkernel_dependency_required" + "=True",
        "open" + "ai",
        "anth" + "ropic",
        "chat" + ".compl" + "etions",
        "eval" + "(",
    ]:
        assert forbidden not in source
    assert re.search(r"(?<![A-Za-z0-9_])shell" + r"=True", source) is None


def test_agent_turn_report_declares_all_premature_paths_disabled() -> None:
    report = AgentTurnReportService().build_report()

    assert report.ready_for_v0_25_2 is True
    assert report.ready_for_v0_26 is False
    assert report.intent_classified is False
    assert report.task_framed is False
    assert report.safety_gate_evaluated is False
    assert report.tool_route_executed is False
    assert report.provider_invoked is False
    assert report.local_command_executed is False
    assert report.ask_executed is False
    assert report.repl_started is False
    assert report.memory_promoted is False
    assert report.persistent_memory_written is False
    assert report.persona_mutated is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_policy_context_trace_and_envelope_boundaries_are_context_only() -> None:
    report = AgentTurnReportService().build_report()

    assert report.policy.envelope_only is True
    assert report.policy.intent_classification_enabled is False
    assert report.policy.safety_gate_enabled is False
    assert report.policy.tool_routing_enabled is False
    assert report.policy.provider_invocation_enabled is False
    assert report.policy.local_runtime_execution_enabled is False
    assert report.policy.memory_promotion_enabled is False
    assert report.policy.persistent_memory_write_enabled is False
    assert report.session.persistent_memory_session is False
    assert report.context_view.persistent_memory_used is False
    assert report.context_view.memory_promoted is False
    assert report.envelope.expected_next_stage == "v0.25.2 Intent Classification & Task Framing"
    assert report.trace.ocel_visible is True
    assert report.trace.raw_secret_in_trace is False
