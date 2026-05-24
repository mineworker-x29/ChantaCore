from __future__ import annotations

import subprocess
import sys

from chanta_core.self_modification_safety import (
    LIFECYCLE_STATES,
    SELF_MODIFICATION_SEED_SKILL_IDS,
    SELF_MODIFICATION_SEED_SUBJECT_IDS,
    SELF_MODIFICATION_SAFETY_LAYER,
    SELF_MODIFICATION_SAFETY_VERSION,
    SelfModificationConformanceService,
    SelfModificationRegistryService,
    SelfModificationReportService,
)


def test_self_modification_safety_contract_builds() -> None:
    contract = SelfModificationRegistryService().build_contract()

    assert contract.version == SELF_MODIFICATION_SAFETY_VERSION
    assert contract.layer == SELF_MODIFICATION_SAFETY_LAYER
    assert contract.status == "contract_only"
    assert contract.pig_projection_required is True
    assert contract.ocpx_projection_required is True
    assert contract.workbench_visibility_required is True


def test_all_seed_subjects_and_skills_are_registered() -> None:
    registry = SelfModificationRegistryService()
    subjects = registry.list_subjects()

    assert [item.subject_id for item in subjects] == SELF_MODIFICATION_SEED_SUBJECT_IDS
    assert registry.list_seed_skill_ids() == SELF_MODIFICATION_SEED_SKILL_IDS
    for subject in subjects:
        assert subject.status == "contract_only"
        assert "stub" in subject.risk_notes
        assert "non_executable" in subject.risk_notes
        assert subject.ocel_object_types
        assert subject.ocel_event_types
        assert subject.ocel_relation_types


def test_risk_profile_disables_write_apply_execution_and_llm_paths() -> None:
    risk = SelfModificationRegistryService().build_contract().risk_profile

    assert risk.contract_only is True
    assert risk.file_write_enabled is False
    assert risk.apply_patch_enabled is False
    assert risk.shell_enabled is False
    assert risk.test_execution_enabled is False
    assert risk.lint_execution_enabled is False
    assert risk.network_enabled is False
    assert risk.mcp_enabled is False
    assert risk.plugin_enabled is False
    assert risk.external_harness_enabled is False
    assert risk.memory_mutation_enabled is False
    assert risk.persona_mutation_enabled is False
    assert risk.overlay_mutation_enabled is False
    assert risk.autonomous_apply_enabled is False
    assert risk.llm_patch_generation_enabled is False
    assert risk.llm_judge_enabled is False
    assert risk.dangerous_capability is False


def test_gate_contract_requires_all_safety_gates() -> None:
    gate = SelfModificationRegistryService().build_contract().gate_contract

    assert gate.requires_modification_request is True
    assert gate.requires_patch_candidate is True
    assert gate.requires_diff_preview is True
    assert gate.requires_static_safety_check is True
    assert gate.requires_dry_run_before_apply is True
    assert gate.requires_human_review_before_apply is True
    assert gate.requires_explicit_apply_gate is True
    assert gate.requires_rollback_plan is True
    assert gate.requires_post_apply_verification is True
    assert gate.deny_if_unreviewed is True
    assert gate.deny_if_no_rollback_plan is True
    assert gate.deny_if_no_dry_run is True
    assert gate.deny_if_private_boundary_risk is True
    assert gate.deny_if_patch_scope_exceeds_limit is True


def test_patch_policy_allows_only_bounded_text_patch_types() -> None:
    policy = SelfModificationRegistryService().build_contract().allowed_patch_policy

    assert {"text_replace", "insert_after", "append_block", "comment_only_change"} <= set(policy.allowed_patch_types)
    assert {
        "binary_patch",
        "broad_rewrite",
        "delete_file",
        "rename_file",
        "chmod_change",
        "dependency_install",
        "secret_file_change",
        "generated_file_mass_update",
    } <= set(policy.forbidden_patch_types)
    assert policy.max_files_per_patch == 1
    assert policy.max_hunks_per_file == 3
    assert policy.max_added_lines == 80
    assert policy.max_removed_lines == 80
    assert policy.requires_anchor_text is True
    assert policy.requires_workspace_path_policy is True
    assert policy.allows_binary_files is False
    assert policy.allows_secret_files is False
    assert policy.allows_private_paths is False


def test_lifecycle_policy_defines_future_apply_transition_without_execution() -> None:
    policy = SelfModificationRegistryService().build_contract().lifecycle_policy
    transitions = {(item["from"], item["to"]) for item in policy.transitions}

    assert set(LIFECYCLE_STATES) <= set(policy.states)
    assert ("requested", "candidate_created") in transitions
    assert ("candidate_created", "preview_created") in transitions
    assert ("preview_created", "safety_checked") in transitions
    assert ("safety_checked", "dry_run_checked") in transitions
    assert ("dry_run_checked", "pending_review") in transitions
    assert ("pending_review", "approved_for_apply") in transitions
    assert ("approved_for_apply", "apply_gate_opened") in transitions
    assert ("apply_gate_opened", "applied") in transitions
    assert ("applied", "post_apply_verified") in transitions
    assert ("post_apply_verified", "outcome_recorded") in transitions
    assert policy.mutation_transitions_executable is False


def test_conformance_and_reports_build() -> None:
    registry = SelfModificationRegistryService()
    conformance = SelfModificationConformanceService(registry)
    report_service = SelfModificationReportService(registry_service=registry, conformance_service=conformance)

    report = conformance.run_conformance()
    contract_report = report_service.build_contract_report()
    pig = report_service.build_pig_report()
    ocpx = report_service.build_ocpx_projection()

    assert report.passed is True
    assert contract_report.status == "contract_only"
    assert contract_report.review_status == "report_only"
    assert contract_report.canonical_promotion_enabled is False
    assert contract_report.promoted is False
    assert pig["version"] == "v0.22.0"
    assert pig["layer"] == "self_modification_safety"
    assert pig["status"] == "contract_only"
    assert pig["safety_boundary"]["file_write_enabled"] is False
    assert pig["safety_boundary"]["apply_patch_enabled"] is False
    assert pig["safety_boundary"]["autonomous_apply_enabled"] is False
    assert pig["safety_boundary"]["llm_patch_generation_enabled"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "self_modification_safety_contract_registered"
    assert "DeepSelfConsolidationState" in ocpx["source_read_models"]
    assert "SelfModificationSafetyContractState" in ocpx["target_read_models"]
    assert "SelfModificationLifecyclePolicyState" in ocpx["target_read_models"]
    assert "SelfModificationPatchPolicyState" in ocpx["target_read_models"]
    assert "SelfModificationGateContractState" in ocpx["target_read_models"]


def test_self_modification_cli_commands() -> None:
    commands = [
        "contract",
        "subjects",
        "conformance",
        "lifecycle",
        "patch-policy",
        "pig-report",
        "ocpx-projection",
    ]
    for command in commands:
        completed = subprocess.run(
            [sys.executable, "-m", "chanta_core.cli", "self-modification", command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "layer=self_modification_safety" in completed.stdout
        assert "file_write_enabled=false" in completed.stdout
        assert "apply_patch_enabled=false" in completed.stdout
        assert "no_file_mutation_occurred=true" in completed.stdout
        assert "raw_file_content_printed=False" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
