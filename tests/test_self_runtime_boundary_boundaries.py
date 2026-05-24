from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    SelfRuntimeBoundaryAwarenessService,
)


def test_ocel_mapping_contains_runtime_boundary_awareness_types() -> None:
    for object_type in [
        "runtime_boundary",
        "runtime_profile",
        "runtime_mode",
        "runtime_track_state",
        "workspace_boundary",
        "private_boundary",
        "canonical_store_policy",
        "execution_boundary",
        "runtime_boundary_snapshot",
        "runtime_boundary_truth_report",
        "runtime_boundary_finding",
        "capability_record",
        "capability_registry_snapshot",
        "deep_self_introspection_subject",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES
    for event_type in [
        "deep_self_runtime_boundary_view_requested",
        "deep_self_runtime_boundary_sources_collected",
        "deep_self_runtime_boundary_snapshot_created",
        "deep_self_runtime_boundary_truth_check_requested",
        "deep_self_runtime_boundary_truth_report_created",
        "deep_self_runtime_boundary_warning_created",
        "deep_self_runtime_boundary_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES
    for relation_type in [
        "views_runtime_boundary",
        "uses_profile",
        "declares_runtime_mode",
        "enables_track",
        "disables_track",
        "constrains_capability",
        "protects_private_boundary",
        "defines_workspace_scope",
        "confirms_canonical_store",
        "requires_execution_boundary",
        "contradicts_runtime_claim",
        "verified_by_runtime_boundary",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_capability_truth",
        "derived_from_deep_self_contract",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES
    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES
    assert "state_candidate_created" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_runtime_boundary_awareness_is_read_only_and_non_mutating() -> None:
    snapshot = SelfRuntimeBoundaryAwarenessService().view_runtime_boundary()
    boundary = snapshot.execution_boundary
    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert boundary.write_enabled is False
    assert boundary.shell_enabled is False
    assert boundary.network_enabled is False
    assert boundary.mcp_enabled is False
    assert boundary.plugin_enabled is False
    assert boundary.external_harness_enabled is False
    assert boundary.memory_mutation_enabled is False
    assert boundary.persona_mutation_enabled is False
    assert boundary.overlay_mutation_enabled is False


def test_docs_define_runtime_boundary_awareness_boundary() -> None:
    text = Path("docs/versions/v0.21/v0.21.2_self_runtime_boundary_awareness.md").read_text(encoding="utf-8")
    assert "Self-Runtime Boundary Awareness" in text
    assert "Runtime boundary awareness is not runtime probing." in text
    assert "Runtime boundary truth > persona claim." in text
    assert "Runtime boundary view is read-only." in text
    assert "v0.21.3 Self-Policy/Gate Awareness" in text


def test_runtime_files_do_not_contain_probe_or_activation_calls() -> None:
    runtime_files = [
        Path("src/chanta_core/deep_self_introspection/runtime_boundary.py"),
    ]
    forbidden = [
        "subprocess",
        "os.system",
        "os.environ",
        "getenv",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "credential",
        "api_key",
        "token",
        "provider_probe",
        "permission_grant",
        "grants_permission=True",
        "enable_skill",
        "capability_enable",
        "mutates_policy=True",
        "mutates_capability_registry=True",
        "apply_patch",
        "write_file",
        "memory_auto_promotion",
        "persona_auto_promotion",
        "overlay_auto_mutation",
        "canonical_promotion_enabled=True",
        "promoted=True",
        "materialized=True",
        "execution_enabled=True",
        "llm",
        "openai",
        "anthropic",
        "completion",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    text = "\n".join(path.read_text(encoding="utf-8").lower() for path in runtime_files)
    for item in forbidden:
        assert item.lower() not in text
