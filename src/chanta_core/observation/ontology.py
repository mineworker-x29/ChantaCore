ACTION_TYPES = [
    "observe_context",
    "load_context",
    "read_object",
    "search_object",
    "summarize_object",
    "classify_intent",
    "propose_action",
    "request_review",
    "decide_review",
    "invoke_skill",
    "invoke_tool",
    "request_permission",
    "decide_permission",
    "gate_action",
    "execute_action",
    "record_envelope",
    "verify_result",
    "record_outcome",
    "create_candidate",
    "delegate_task",
    "recover_failure",
    "emit_response",
    "unknown_action",
]

OBJECT_TYPES = [
    "agent_instance",
    "runtime",
    "environment",
    "workspace",
    "repository",
    "session",
    "turn",
    "message",
    "goal",
    "intent",
    "task",
    "skill",
    "tool",
    "file",
    "artifact",
    "permission_request",
    "permission_decision",
    "gate_decision",
    "execution_envelope",
    "summary",
    "candidate",
    "outcome",
    "error",
    "external_system",
    "unknown_object",
]

EFFECT_TYPES = [
    "no_effect",
    "read_only_observation",
    "state_candidate_created",
    "local_runtime_state_changed",
    "workspace_file_changed",
    "external_system_touched",
    "permission_requested",
    "permission_denied",
    "gate_blocked",
    "candidate_created",
    "unknown_side_effect",
]

RELATION_TYPES = [
    "followed_by",
    "responds_to",
    "uses",
    "reads",
    "searches",
    "summarizes",
    "invokes",
    "gates",
    "blocks",
    "allows",
    "produces",
    "derives_from",
    "verifies",
    "fails_on",
    "recovers_from",
    "delegates_to",
    "belongs_to",
    "caused_by",
    "depends_on",
    "contradicts",
    "unknown_relation",
]

CONFIDENCE_CLASSES = [
    "confirmed_observation",
    "derived_observation",
    "behavior_inference",
    "outcome_hypothesis",
    "unknown",
]


def default_ontology_specs() -> list[tuple[str, str, str, str | None]]:
    specs: list[tuple[str, str, str, str | None]] = []
    specs.extend(("action_type", value, f"Canonical action type: {value}.", None) for value in ACTION_TYPES)
    specs.extend(("object_type", value, f"Canonical observed object type: {value}.", None) for value in OBJECT_TYPES)
    specs.extend(("effect_type", value, f"Canonical effect type: {value}.", None) for value in EFFECT_TYPES)
    specs.extend(("relation_type", value, f"Canonical relation type: {value}.", None) for value in RELATION_TYPES)
    specs.extend(("confidence_class", value, f"Canonical confidence class: {value}.", None) for value in CONFIDENCE_CLASSES)
    return specs
