import inspect
import re

import chanta_core.agent_surface.intent_task as intent_task_module
from chanta_core.agent_surface import AgentIntentClassificationReportService


def test_agent_intent_task_source_has_no_execution_or_adapter_paths() -> None:
    source = inspect.getsource(intent_task_module)

    for forbidden in [
        "subprocess" + ".run",
        "subprocess" + ".Popen",
        "os" + ".system",
        "agent_ask_executed" + "=True",
        "agent_repl_started" + "=True",
        "agent_safety_gate_evaluated" + "=True",
        "agent_no_action_finalized" + "=True",
        "agent_clarification_finalized" + "=True",
        "agent_blocked_decision_finalized" + "=True",
        "tool_route_executed" + "=True",
        "agent_tool_route_plan_created" + "=True",
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


def test_intent_report_declares_all_future_stage_paths_disabled() -> None:
    report = AgentIntentClassificationReportService().build_report()

    assert report.ready_for_v0_25_3 is True
    assert report.ready_for_v0_26 is False
    assert report.intent_classified is True
    assert report.task_framed is True
    assert report.safety_gate_evaluated is False
    assert report.final_no_action_decision is False
    assert report.final_clarification_decision is False
    assert report.final_blocked_decision is False
    assert report.tool_route_created is False
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


def test_policy_descriptor_frame_and_candidate_are_intent_task_only() -> None:
    report = AgentIntentClassificationReportService().build_report()

    assert report.policy.deterministic_default is True
    assert report.policy.external_llm_classification_enabled is False
    assert report.policy.llm_safety_judge_enabled is False
    assert report.policy.safety_gate_enabled is False
    assert report.policy.tool_routing_enabled is False
    assert report.policy.provider_invocation_enabled is False
    assert report.policy.local_runtime_execution_enabled is False
    assert report.policy.final_no_action_decision_enabled is False
    assert report.policy.final_clarification_decision_enabled is False
    assert report.policy.final_blocked_decision_enabled is False
    assert report.intent_descriptor.requires_safety_gate_next is True
    assert report.intent_descriptor.final_no_action_decision is False
    assert report.intent_descriptor.final_blocked_decision is False
    assert report.intent_descriptor.final_clarification_decision is False
    assert report.task_frame.expected_next_stage == "v0.25.3 Safety / No-Action / Clarification Gate"
    assert report.task_frame.safety_gate_evaluated is False
    assert report.task_frame.tool_route_created is False
    assert report.task_frame.provider_invoked is False
    assert report.task_frame.local_command_executed is False
    assert report.task_frame_candidate.executes_now is False
    assert report.task_frame_candidate.routes_now is False
    assert report.task_frame_candidate.invokes_provider_now is False
    assert report.task_frame_candidate.mutates_state_now is False
