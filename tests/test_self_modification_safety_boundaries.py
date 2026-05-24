from __future__ import annotations

from pathlib import Path

from chanta_core.self_modification_safety import (
    SELF_MODIFICATION_EFFECT_TYPES,
    SELF_MODIFICATION_OCEL_EVENT_TYPES,
    SELF_MODIFICATION_OCEL_MAPPING,
    SELF_MODIFICATION_OCEL_OBJECT_TYPES,
    SELF_MODIFICATION_OCEL_RELATION_TYPES,
    SelfModificationAllowedPatchPolicy,
    SelfModificationContractReport,
    SelfModificationGateContract,
    SelfModificationLifecyclePolicy,
    SelfModificationObservabilityContract,
    SelfModificationRiskProfile,
    SelfModificationSafetyContract,
    SelfModificationSubject,
)


def test_self_modification_models_are_exported() -> None:
    exported = [
        SelfModificationSafetyContract,
        SelfModificationSubject,
        SelfModificationRiskProfile,
        SelfModificationGateContract,
        SelfModificationObservabilityContract,
        SelfModificationAllowedPatchPolicy,
        SelfModificationLifecyclePolicy,
        SelfModificationContractReport,
    ]
    assert all(item is not None for item in exported)


def test_docs_define_self_modification_safety_boundary() -> None:
    text = Path("docs/versions/v0.22/v0.22.0_self_modification_safety_contract.md").read_text(encoding="utf-8")

    assert "OCEL-native Self-Modification Safety Contract" in text
    assert "OCEL-native 자기수정 안전 계약" in text
    assert "Self-modification safety is not self-modification." in text
    assert "Patch candidate is not patch apply." in text
    assert "Diff preview is not file mutation." in text
    assert "Apply requires explicit apply gate." in text
    assert "Rollback plan is required before mutation." in text
    assert "Post-apply verification is mandatory after mutation." in text
    assert "v0.22.1 Self-Modification Request & Patch Candidate" in text


def test_ocel_mapping_skeleton_exists() -> None:
    object_types = {
        "self_modification_safety_layer",
        "self_modification_safety_contract",
        "self_modification_subject",
        "self_modification_skill_contract",
        "self_modification_risk_profile",
        "self_modification_gate_contract",
        "self_modification_observability_contract",
        "self_modification_allowed_patch_policy",
        "self_modification_lifecycle_policy",
        "self_modification_contract_report",
        "modification_request_subject",
        "patch_candidate_subject",
        "diff_preview_subject",
        "patch_static_safety_subject",
        "patch_dry_run_subject",
        "modification_review_gate_subject",
        "patch_apply_gate_subject",
        "rollback_plan_subject",
        "post_apply_verification_subject",
        "modification_outcome_subject",
        "deep_self_consolidation_report",
        "capability_truth_report",
        "runtime_boundary_truth_report",
        "policy_gate_truth_report",
        "trace_integrity_report",
        "candidate_memory_boundary_report",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    }
    event_types = {
        "self_modification_safety_layer_registered",
        "self_modification_safety_contract_registered",
        "self_modification_subject_registered",
        "self_modification_contract_checked",
        "self_modification_conformance_report_created",
        "self_modification_pig_report_created",
        "self_modification_ocpx_projection_created",
    }
    relation_types = {
        "declares_modification_subject",
        "maps_subject_to_ocel_object",
        "maps_subject_to_ocel_event",
        "maps_subject_to_ocel_relation",
        "requires_modification_request",
        "requires_patch_candidate",
        "requires_diff_preview",
        "requires_safety_check",
        "requires_dry_run",
        "requires_human_review",
        "requires_apply_gate",
        "requires_rollback_plan",
        "requires_post_apply_verification",
        "derived_from_deep_self_consolidation",
        "constrained_by_capability_truth",
        "constrained_by_runtime_boundary",
        "constrained_by_policy_gate",
        "constrained_by_trace_integrity",
        "recorded_in_envelope",
        "visible_in_workbench",
    }

    assert object_types <= set(SELF_MODIFICATION_OCEL_OBJECT_TYPES)
    assert event_types <= set(SELF_MODIFICATION_OCEL_EVENT_TYPES)
    assert relation_types <= set(SELF_MODIFICATION_OCEL_RELATION_TYPES)
    assert {"read_only_observation", "state_candidate_created"} <= set(SELF_MODIFICATION_EFFECT_TYPES)
    assert "workspace_file_changed" in SELF_MODIFICATION_EFFECT_TYPES
    assert "self_modification_safety_contract" in SELF_MODIFICATION_OCEL_MAPPING.object_types


def test_runtime_does_not_call_forbidden_write_or_execution_operations() -> None:
    runtime_files = [
        Path("src/chanta_core/self_modification_safety/models.py"),
        Path("src/chanta_core/self_modification_safety/mapping.py"),
        Path("src/chanta_core/self_modification_safety/registry.py"),
        Path("src/chanta_core/self_modification_safety/conformance.py"),
        Path("src/chanta_core/self_modification_safety/reports.py"),
    ]
    runtime = "\n".join(path.read_text(encoding="utf-8") for path in runtime_files)
    forbidden_call_tokens = [
        "open(",
        "pathlib.Path.write_text",
        "pathlib.Path.write_bytes",
        "shutil.move",
        "os.remove",
        "unlink(",
        "rename(",
        "chmod(",
        "subprocess",
        "os.system",
        "pytest",
        "ruff",
        "mypy",
        "requests(",
        "httpx",
        "mcp.connect",
        "plugin.load",
        "generate_patch(",
        "patch_apply(",
        "openai",
        "anthropic",
        "chat.completions",
        "exec(",
        "eval(",
    ]
    assert [token for token in forbidden_call_tokens if token in runtime] == []
    assert "file_write_enabled=True" not in runtime
    assert "apply_patch_enabled=True" not in runtime
    assert "execution_enabled=True" not in runtime
    assert "dangerous_capability=True" not in runtime
    assert "jsonl" not in runtime.lower()
