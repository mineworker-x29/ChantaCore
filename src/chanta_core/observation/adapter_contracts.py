from __future__ import annotations

ADAPTER_CONTRACT_SPECS = [
    ("ChantaCoreOCELAdapter", "chantacore", "chantacore", ["json", "ocel_like"], True),
    ("GenericJSONLTranscriptAdapter", "generic_jsonl", "generic", ["jsonl", "generic_jsonl"], True),
    ("SchumpeterAgentEventAdapter", "schumpeter_agent", "agent_event", ["jsonl"], False),
    ("OpenCodeToolLifecycleAdapter", "opencode", "tool_lifecycle", ["jsonl", "tool_lifecycle"], False),
    ("ClaudeCodeTranscriptAdapter", "claude_code", "transcript", ["json", "transcript"], False),
    ("CodexTaskLogAdapter", "codex_task_log", "task_log", ["jsonl", "task_log"], False),
    ("OpenClawGatewayLogAdapter", "openclaw_gateway", "gateway_log", ["jsonl", "gateway_log"], False),
    ("HermesMissionLogAdapter", "hermes_mission", "mission_log", ["json", "mission_log"], False),
]

GENERIC_JSONL_RULE_SPECS = [
    ("role=user", "role=user", "user_message_observed", "observe_context", ["message"], "no_effect"),
    ("role=assistant", "role=assistant", "assistant_message_observed", "emit_response", ["message"], "no_effect"),
    ("tool_call", "tool|tool_call|name", "tool_call_observed", "invoke_tool", ["tool"], "unknown_side_effect"),
    ("tool_result", "tool_result|result|output", "tool_result_observed", "record_outcome", ["outcome"], "no_effect"),
    ("error", "error", "error_observed", "record_outcome", ["error"], "no_effect"),
]

CHANTACORE_OCEL_RULE_SPECS = [
    ("explicit_skill_invocation", "explicit_skill_invocation", "skill_invocation_observed", "invoke_skill", ["skill"], "unknown_side_effect"),
    ("skill_execution_gate_result", "skill_execution_gate_result", "gate_observed", "gate_action", ["gate_decision"], "gate_blocked"),
    ("execution_envelope", "execution_envelope", "outcome_observed", "record_envelope", ["execution_envelope"], "no_effect"),
    ("workspace_read_summary_result", "workspace_read_summary_result", "summary_observed", "summarize_object", ["summary"], "read_only_observation"),
    ("execution_result_promotion_candidate", "execution_result_promotion_candidate", "outcome_observed", "create_candidate", ["candidate"], "candidate_created"),
]

STUB_RULE_SPECS = [
    ("SchumpeterAgentEventAdapter", "user_message", "user_message_observed", "observe_context"),
    ("SchumpeterAgentEventAdapter", "assistant_response", "assistant_message_observed", "emit_response"),
    ("SchumpeterAgentEventAdapter", "skill_selected", "skill_invocation_observed", "invoke_skill"),
    ("SchumpeterAgentEventAdapter", "tool_invoked", "tool_call_observed", "invoke_tool"),
    ("SchumpeterAgentEventAdapter", "task_failed", "error_observed", "record_outcome"),
    ("OpenCodeToolLifecycleAdapter", "tool_lifecycle", "tool_call_observed", "invoke_tool"),
    ("ClaudeCodeTranscriptAdapter", "transcript_message", "assistant_message_observed", "emit_response"),
    ("CodexTaskLogAdapter", "task_log_event", "outcome_observed", "record_outcome"),
    ("OpenClawGatewayLogAdapter", "gateway_log_event", "tool_call_observed", "invoke_tool"),
    ("HermesMissionLogAdapter", "mission_log_event", "outcome_observed", "record_outcome"),
]
