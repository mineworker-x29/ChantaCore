from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    SelfPolicyGateAwarenessService,
)


def test_ocel_mapping_contains_policy_gate_awareness_types() -> None:
    for object_type in [
        "policy_gate_map",
        "policy_gate_rule",
        "review_policy",
        "proposal_policy",
        "permission_boundary",
        "read_only_gate",
        "execution_gate",
        "execution_envelope_policy",
        "promotion_gate",
        "materialization_gate",
        "hard_block_rule",
        "candidate_only_policy",
        "no_action_policy",
        "needs_more_input_policy",
        "policy_gate_snapshot",
        "policy_gate_truth_report",
        "policy_gate_finding",
        "capability_record",
        "runtime_boundary_snapshot",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES
    for event_type in [
        "deep_self_policy_gate_map_requested",
        "deep_self_policy_gate_sources_collected",
        "deep_self_policy_gate_map_created",
        "deep_self_policy_gate_truth_check_requested",
        "deep_self_policy_gate_truth_report_created",
        "deep_self_policy_gate_warning_created",
        "deep_self_policy_gate_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES
    for relation_type in [
        "views_policy_gate",
        "maps_policy",
        "maps_gate",
        "requires_review",
        "requires_permission_boundary",
        "requires_execution_envelope",
        "blocks_capability",
        "allows_read_only_invocation",
        "denies_execution",
        "separates_review_from_execution",
        "prevents_promotion",
        "prevents_materialization",
        "supports_no_action",
        "supports_needs_more_input",
        "verified_by_policy_gate",
        "contradicts_policy_claim",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
        "derived_from_deep_self_contract",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES
    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_policy_gate_awareness_is_read_only_and_non_mutating() -> None:
    snapshot = SelfPolicyGateAwarenessService().view_policy_gate_map()
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert snapshot.permission_boundary.permission_grant_creation_allowed is False
    assert snapshot.permission_boundary.permission_escalation_allowed is False
    assert snapshot.promotion_gate.candidate_promotion_enabled is False
    assert snapshot.materialization_gate.materialization_enabled is False
    assert all(gate.enabled is False for gate in snapshot.execution_gates if gate.gate_type != "read_only")


def test_docs_define_policy_gate_awareness_boundary() -> None:
    text = Path("docs/versions/v0.21/v0.21.3_self_policy_gate_awareness.md").read_text(encoding="utf-8")
    assert "Self-Policy/Gate Awareness" in text
    assert "Policy awareness is not policy mutation." in text
    assert "Gate awareness is not permission grant." in text
    assert "Review approval is not execution permission." in text
    assert "No-action is a valid policy outcome." in text
    assert "v0.21.4 Self-Trace Integrity Awareness" in text


def test_runtime_files_do_not_contain_policy_mutation_or_execution_calls() -> None:
    runtime_files = [
        Path("src/chanta_core/deep_self_introspection/policy_gate.py"),
    ]
    forbidden_calls = [
        "accept_proposal(",
        "reject_proposal(",
        "create_review_decision(",
        "invoke_skill(",
        "execute_envelope(",
        "apply_patch(",
        "write_file(",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "mutates_policy=True",
        "mutates_capability_registry=True",
        "memory_auto_promotion",
        "persona_auto_promotion",
        "overlay_auto_mutation",
        "canonical_promotion_enabled=True",
        "promoted=True",
        "materialized=True",
        "execution_enabled=True",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    text = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)
    for item in forbidden_calls:
        assert item not in text
