from __future__ import annotations

from pathlib import Path

from chanta_core.deep_self_introspection import (
    DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    DeepSelfContradictionRegisterView,
    DeepSelfCoverageRow,
    DeepSelfFindingsView,
    DeepSelfOCELCoverageView,
    DeepSelfPigOCPXStatusView,
    DeepSelfSafetyBoundaryStatus,
    DeepSelfSubjectStatusView,
    DeepSelfWorkbenchFinding,
    DeepSelfWorkbenchRequest,
    DeepSelfWorkbenchService,
    DeepSelfWorkbenchSnapshot,
)


RUNTIME_FILE = Path("src/chanta_core/deep_self_introspection/workbench.py")
DOC_FILE = Path("docs/versions/v0.21/v0.21.8_deep_self_introspection_workbench.md")


def test_workbench_model_types_are_exported() -> None:
    assert DeepSelfWorkbenchRequest
    assert DeepSelfCoverageRow
    assert DeepSelfSubjectStatusView
    assert DeepSelfSafetyBoundaryStatus
    assert DeepSelfFindingsView
    assert DeepSelfContradictionRegisterView
    assert DeepSelfOCELCoverageView
    assert DeepSelfPigOCPXStatusView
    assert DeepSelfWorkbenchFinding
    assert DeepSelfWorkbenchSnapshot


def test_docs_define_workbench_identity_and_non_goals() -> None:
    content = DOC_FILE.read_text(encoding="utf-8")

    assert "Deep Self-Introspection Workbench" in content
    assert "심층 자기 관조 워크벤치" in content
    assert "Workbench is not correction" in content
    assert "Workbench is not approval" in content
    assert "Workbench is not promotion" in content
    assert "Workbench is not execution" in content
    assert "Workbench is an OCEL-native read model" in content
    assert "v0.21.9 Deep Self-Introspection Consolidation" in content


def test_ocel_mapping_includes_workbench_types() -> None:
    for object_type in [
        "deep_self_workbench_snapshot",
        "deep_self_coverage_row",
        "deep_self_subject_status_view",
        "deep_self_safety_boundary_status",
        "deep_self_findings_view",
        "deep_self_contradiction_register_view",
        "deep_self_ocel_coverage_view",
        "deep_self_pig_ocpx_status_view",
        "deep_self_workbench_finding",
        "capability_truth_report",
        "runtime_boundary_truth_report",
        "policy_gate_truth_report",
        "trace_integrity_report",
        "context_projection_truth_report",
        "candidate_memory_boundary_report",
        "claim_consistency_report",
        "contradiction_register",
        "execution_envelope",
    ]:
        assert object_type in DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES
    for event_type in [
        "deep_self_workbench_requested",
        "deep_self_workbench_snapshot_created",
        "deep_self_capability_truth_viewed",
        "deep_self_runtime_boundary_viewed",
        "deep_self_policy_gate_viewed",
        "deep_self_trace_integrity_viewed",
        "deep_self_context_projection_viewed",
        "deep_self_candidate_memory_boundary_viewed",
        "deep_self_claim_consistency_viewed",
        "deep_self_contradictions_viewed",
        "deep_self_findings_viewed",
        "deep_self_safety_boundary_viewed",
        "deep_self_ocel_coverage_viewed",
        "deep_self_pig_ocpx_status_viewed",
        "deep_self_workbench_warning_created",
        "deep_self_workbench_violation_detected",
    ]:
        assert event_type in DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES
    for relation_type in [
        "views_capability_truth",
        "views_runtime_boundary",
        "views_policy_gate",
        "views_trace_integrity",
        "views_context_projection",
        "views_candidate_memory_boundary",
        "views_claim_consistency",
        "views_contradiction_register",
        "views_findings",
        "views_safety_boundary",
        "views_ocel_coverage",
        "views_pig_ocpx_status",
        "detects_workbench_finding",
        "summarizes_deep_self_subject",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_claim_consistency",
        "derived_from_candidate_memory_boundary",
        "derived_from_context_projection",
        "derived_from_trace_integrity",
        "derived_from_policy_gate",
        "derived_from_runtime_boundary",
        "derived_from_capability_truth",
    ]:
        assert relation_type in DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES
    assert "read_only_observation" in DEEP_SELF_INTROSPECTION_EFFECT_TYPES


def test_workbench_output_is_sanitized_and_non_mutating() -> None:
    service = DeepSelfWorkbenchService()
    snapshot = service.build_snapshot()
    output = service.render_cli(snapshot)

    assert snapshot.read_only is True
    assert snapshot.mutation_performed is False
    assert "No correction performed." in output
    assert "No approval performed." in output
    assert "No promotion performed." in output
    assert "No execution performed." in output
    assert "No contradiction resolution performed." in output
    assert "raw_memory_persona_private_material_printed=False" in output
    assert "private_full_paths_printed=False" in output
    assert "raw_file_content_printed=False" in output
    assert "raw_secrets_printed=False" in output


def test_runtime_implementation_does_not_add_forbidden_calls() -> None:
    content = RUNTIME_FILE.read_text(encoding="utf-8")
    forbidden_call_tokens = [
        "correct_finding(",
        "auto_correct(",
        "resolve_contradiction(",
        "acknowledge_contradiction(",
        "approve(",
        "promote(",
        "promote_candidate(",
        "promote_memory(",
        "memory_write(",
        "create_memory_entry(",
        "update_memory(",
        "persona_update(",
        "overlay_update(",
        "materialize(",
        "create_todo(",
        "task_queue(",
        "scheduler(",
        "inject_context(",
        "modify_prompt(",
        "system_prompt(",
        "prompt_mutation(",
        "repair_trace(",
        "backfill(",
        "rewrite_claim(",
        "modify_response(",
        "apply_patch(",
        "write_file(",
        "subprocess",
        "os.system",
        "requests",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    for token in forbidden_call_tokens:
        assert token not in content


def test_jsonl_is_not_canonical_store() -> None:
    service = DeepSelfWorkbenchService()
    assert service.build_ocpx_projection()["canonical_store"] == "ocel"
    assert "jsonl" not in RUNTIME_FILE.read_text(encoding="utf-8").lower()
