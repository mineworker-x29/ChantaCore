from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    SelfCapabilityRegistryAwarenessService,
)


def test_ocel_mapping_contains_capability_registry_awareness_types() -> None:
    for object_type in [
        "capability_registry",
        "capability_record",
        "capability_registry_snapshot",
        "capability_truth_report",
        "capability_truth_finding",
        "capability_risk_profile_view",
        "capability_gate_view",
        "capability_observability_view",
        "skill_contract",
        "deep_self_introspection_subject",
        "self_awareness_capability",
        "external_candidate_capability",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES
    for event_type in [
        "deep_self_capability_registry_view_requested",
        "deep_self_capability_registry_snapshot_created",
        "deep_self_capability_risk_view_created",
        "deep_self_capability_gate_view_created",
        "deep_self_capability_observability_view_created",
        "deep_self_capability_truth_check_requested",
        "deep_self_capability_truth_report_created",
        "deep_self_capability_truth_warning_created",
        "deep_self_capability_truth_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES
    for relation_type in [
        "views_capability_registry",
        "contains_capability",
        "describes_skill_contract",
        "has_risk_view",
        "has_gate_view",
        "has_observability_view",
        "checks_capability_truth",
        "finds_capability_issue",
        "contradicts_claim",
        "verified_by_registry",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_deep_self_contract",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES
    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_capability_awareness_is_read_only_and_non_enabling() -> None:
    snapshot = SelfCapabilityRegistryAwarenessService().view_registry()
    assert snapshot.execution_enabled_count == 0
    assert snapshot.materialization_enabled_count == 0
    assert snapshot.canonical_promotion_enabled_count == 0
    assert snapshot.dangerous_capability_count == 0
    assert all(view.permission_grant_allowed is False for view in snapshot.gate_views)


def test_docs_define_capability_truth_boundary() -> None:
    text = Path("docs/versions/v0.21/v0.21.1_self_capability_registry_awareness.md").read_text(encoding="utf-8")
    assert "Self-Capability Registry Awareness" in text
    assert "Capability truth > persona claim." in text
    assert "Capability awareness is not capability enablement." in text
    assert "Registry view is read-only." in text
    assert "v0.21.2 Self-Runtime Boundary Awareness" in text


def test_runtime_files_do_not_contain_activation_calls() -> None:
    runtime_files = [
        Path("src/chanta_core/deep_self_introspection/capability_registry.py"),
    ]
    forbidden = [
        "enable_skill(",
        "capability_enable(",
        "permission_grant(",
        "grants_permission=True",
        "apply_patch(",
        "write_file(",
        "os.system",
        "mcp.connect",
        "plugin.load",
        "mutates_capability_registry=True",
        "mutates_policy=True",
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
    for token in forbidden:
        assert token not in text
