import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairWorkspaceCollisionPreventionPlan,
    RepairWorkspaceDescriptor,
    RepairWorkspaceDisposition,
    RepairWorkspaceIsolationDecision,
    RepairWorkspaceIsolationDecisionKind,
    RepairWorkspaceIsolationFlagSet,
    RepairWorkspaceIsolationInput,
    RepairWorkspaceIsolationMode,
    RepairWorkspaceIsolationNoMutationGuarantee,
    RepairWorkspaceIsolationPolicy,
    RepairWorkspaceIsolationReadinessLevel,
    RepairWorkspaceIsolationRiskAssessment,
    RepairWorkspaceIsolationRiskKind,
    RepairWorkspaceIsolationRunPreview,
    RepairWorkspaceIsolationSourceKind,
    RepairWorkspaceIsolationSourceRef,
    RepairWorkspaceIsolationStatus,
    RepairWorkspaceIsolationStrategyKind,
    RepairWorkspaceIsolationValidationFinding,
    RepairWorkspaceIsolationValidationReport,
    RepairWorkspaceKind,
    RepairWorkspaceLiveBoundaryCheck,
    RepairWorkspaceRootRefValidation,
    RepairWorkspaceTargetBinding,
    RepairWorkspaceTrustLevel,
    V0392ReadinessReport,
    assess_repair_workspace_isolation_risk,
    bind_repair_workspace_target,
    build_repair_workspace_collision_prevention_plan,
    build_repair_workspace_descriptor,
    build_repair_workspace_isolation_decision,
    build_repair_workspace_isolation_flags,
    build_repair_workspace_isolation_input,
    build_repair_workspace_isolation_no_mutation_guarantee,
    build_repair_workspace_isolation_policy,
    build_repair_workspace_isolation_risk_assessment,
    build_repair_workspace_isolation_run_preview,
    build_repair_workspace_isolation_source_ref,
    build_repair_workspace_isolation_validation_finding,
    build_repair_workspace_isolation_validation_report,
    build_repair_workspace_live_boundary_check,
    build_repair_workspace_root_ref_validation,
    build_repair_workspace_target_binding,
    build_v0392_readiness_report,
    check_repair_workspace_live_boundaries,
    classify_repair_workspace_descriptor,
    create_repair_workspace_collision_prevention_plan,
    decide_repair_workspace_isolation,
    default_repair_workspace_isolation_policy,
    repair_workspace_decision_is_not_apply_permission,
    repair_workspace_descriptor_is_metadata_only,
    repair_workspace_isolation_flags_preserve_no_mutation,
    repair_workspace_policy_blocks_creation_apply_and_execution,
    repair_workspace_root_ref_validation_does_not_read_files,
    v0392_readiness_report_is_not_execution_ready,
    validate_repair_workspace_root_ref_metadata,
)
from chanta_core.agent_runtime import repair_workspace_isolation as workspace_module


UNSAFE_FLAG_FIELDS = [
    "ready_for_execution",
    "ready_for_sandbox_repair_workspace_creation",
    "ready_for_git_worktree_creation",
    "ready_for_git_checkout",
    "ready_for_branch_creation",
    "ready_for_filesystem_scan",
    "ready_for_source_file_read",
    "ready_for_sandbox_source_read",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
    "ready_for_sandbox_patch_materialization",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_apply",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_post_apply_controlled_retest",
    "ready_for_repair_test_execution",
    "ready_for_self_prompt_generation",
    "ready_for_self_prompt_auto_execution",
    "ready_for_agent_to_subagent_prompt_generation",
    "ready_for_subagent_auto_invocation",
    "ready_for_external_agent_execution",
    "ready_for_model_provider_invocation",
    "ready_for_autonomous_loop_runtime",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_repair_execution",
    "ready_for_test_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_network_access",
    "ready_for_dominion_runtime",
    "production_certified",
]


def test_all_v0392_enum_values_exist():
    assert {item.value for item in RepairWorkspaceIsolationMode} == {
        "sandbox_repair_workspace_isolation_contract",
        "workspace_descriptor_metadata",
        "workspace_root_ref_metadata",
        "workspace_classification_metadata",
        "apply_target_isolation_metadata",
        "collision_prevention_metadata",
        "live_workspace_exclusion_metadata",
        "reference_corpus_exclusion_metadata",
        "secret_path_exclusion_metadata",
        "future_patch_materialization_input",
        "future_sandbox_apply_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert {item.value for item in RepairWorkspaceIsolationSourceKind} == {
        "v0391_approval_artifact_decision",
        "v0391_approval_process_state_gate",
        "v0391_readiness_report",
        "v0390_repair_apply_boundary",
        "v0389_handoff_packet",
        "v0389_consolidation_report",
        "v0386_human_review_packet",
        "v0385_safety_report",
        "v0384_proposed_patch_envelope",
        "supplied_workspace_root_ref",
        "supplied_workspace_descriptor",
        "manual_operator_note",
        "test_fixture",
        "unknown",
    }
    assert {item.value for item in RepairWorkspaceIsolationStatus} == {
        "unknown",
        "draft",
        "input_validated",
        "workspace_descriptor_created",
        "workspace_classified",
        "isolation_contract_created",
        "collision_prevention_defined",
        "live_workspace_excluded",
        "reference_corpus_excluded",
        "secret_paths_excluded",
        "apply_target_bound",
        "ready_for_future_patch_materialization",
        "ready_for_future_sandbox_apply",
        "blocked",
        "rejected",
        "review_required",
        "no_op",
        "safe_failed",
    }
    assert {item.value for item in RepairWorkspaceIsolationReadinessLevel} == {
        "not_ready",
        "workspace_descriptor_ready",
        "workspace_root_ref_ready",
        "workspace_classification_ready",
        "isolation_contract_ready",
        "collision_prevention_ready",
        "apply_target_isolation_ready",
        "live_workspace_exclusion_ready",
        "future_patch_materialization_input_ready",
        "future_sandbox_apply_input_ready",
        "design_handoff_ready_for_v0393",
        "blocked",
        "future_track",
    }
    assert {item.value for item in RepairWorkspaceIsolationDecisionKind} == {
        "allow_workspace_descriptor",
        "allow_workspace_root_ref_metadata",
        "allow_workspace_classification",
        "allow_isolation_contract",
        "allow_collision_prevention_metadata",
        "allow_live_workspace_exclusion",
        "allow_reference_corpus_exclusion",
        "allow_secret_path_exclusion",
        "allow_apply_target_isolation",
        "allow_future_patch_materialization_input",
        "allow_future_sandbox_apply_input",
        "choose_do_nothing",
        "choose_human_review_required",
        "deny",
        "block",
        "reject_live_workspace",
        "reject_reference_corpus",
        "reject_secret_path",
        "reject_missing_approval_gate",
        "reject_scope_mismatch",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in RepairWorkspaceKind} == {
        "declared_sandbox_workspace",
        "sandbox_worktree_like_workspace",
        "sandbox_copy_workspace",
        "sandbox_temp_workspace",
        "sandbox_container_mount_ref",
        "live_workspace",
        "reference_corpus",
        "secret_or_credential_area",
        "unknown",
    }
    assert {item.value for item in RepairWorkspaceIsolationStrategyKind} == {
        "metadata_only_declared_sandbox",
        "worktree_like_isolation_metadata",
        "branch_like_isolation_metadata",
        "copy_like_isolation_metadata",
        "container_mount_like_metadata",
        "manual_operator_supplied_sandbox",
        "no_isolation",
        "invalid",
        "unknown",
    }
    assert {item.value for item in RepairWorkspaceTrustLevel} == {
        "trusted_sandbox_candidate",
        "review_required",
        "untrusted",
        "rejected_live_workspace",
        "rejected_reference_corpus",
        "rejected_secret_area",
        "unknown",
    }
    assert {item.value for item in RepairWorkspaceDisposition} == {
        "accepted_for_future_patch_materialization",
        "accepted_for_future_sandbox_apply",
        "accepted_with_warnings",
        "review_required",
        "blocked",
        "rejected",
        "do_nothing_preferred",
        "no_op",
        "unknown",
    }
    assert "workspace_not_declared_sandbox_risk" in {item.value for item in RepairWorkspaceIsolationRiskKind}


def test_required_models_construct():
    assert isinstance(build_repair_workspace_isolation_source_ref(), RepairWorkspaceIsolationSourceRef)
    assert isinstance(build_repair_workspace_isolation_policy(), RepairWorkspaceIsolationPolicy)
    assert isinstance(build_repair_workspace_isolation_input(), RepairWorkspaceIsolationInput)
    assert isinstance(build_repair_workspace_descriptor(), RepairWorkspaceDescriptor)
    assert isinstance(build_repair_workspace_root_ref_validation(), RepairWorkspaceRootRefValidation)
    assert isinstance(build_repair_workspace_collision_prevention_plan(), RepairWorkspaceCollisionPreventionPlan)
    assert isinstance(build_repair_workspace_target_binding(), RepairWorkspaceTargetBinding)
    assert isinstance(build_repair_workspace_live_boundary_check(), RepairWorkspaceLiveBoundaryCheck)
    assert isinstance(build_repair_workspace_isolation_risk_assessment(), RepairWorkspaceIsolationRiskAssessment)
    assert isinstance(build_repair_workspace_isolation_decision(), RepairWorkspaceIsolationDecision)
    assert isinstance(build_repair_workspace_isolation_validation_finding(), RepairWorkspaceIsolationValidationFinding)
    assert isinstance(build_repair_workspace_isolation_validation_report(), RepairWorkspaceIsolationValidationReport)
    assert isinstance(build_repair_workspace_isolation_run_preview(), RepairWorkspaceIsolationRunPreview)
    assert isinstance(build_v0392_readiness_report(), V0392ReadinessReport)


def test_flag_set_allows_metadata_and_blocks_runtime():
    flags = build_repair_workspace_isolation_flags()
    assert isinstance(flags, RepairWorkspaceIsolationFlagSet)
    assert flags.workspace_isolation_layer_constructed is True
    assert flags.workspace_descriptor_available is True
    assert flags.workspace_root_ref_metadata_available is True
    assert flags.workspace_classification_available is True
    assert flags.ready_for_v0393_human_approved_patch_materialization_sandbox_apply is True
    assert flags.ready_for_future_patch_materialization_input is True
    assert flags.ready_for_future_sandbox_apply_input is True
    assert repair_workspace_isolation_flags_preserve_no_mutation(flags) is True
    for field_name in UNSAFE_FLAG_FIELDS:
        assert getattr(flags, field_name) is False


@pytest.mark.parametrize("field_name", UNSAFE_FLAG_FIELDS)
def test_flags_reject_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_repair_workspace_isolation_flags(**{field_name: True})


def test_policy_allows_metadata_only_and_blocks_creation_apply_execution():
    policy = default_repair_workspace_isolation_policy()
    assert policy.allow_workspace_descriptor_metadata is True
    assert policy.allow_workspace_root_ref_metadata is True
    assert policy.allow_workspace_classification_metadata is True
    assert policy.allow_isolation_contract_metadata is True
    assert policy.allow_collision_prevention_metadata is True
    assert policy.allow_apply_target_isolation_metadata is True
    assert policy.allow_future_patch_materialization_input is True
    assert policy.allow_future_sandbox_apply_input is True
    assert policy.require_approval_process_state_gate is True
    assert policy.require_sandbox_only_workspace is True
    assert policy.require_live_workspace_exclusion is True
    assert policy.require_reference_corpus_exclusion is True
    assert policy.require_secret_path_exclusion is True
    assert repair_workspace_policy_blocks_creation_apply_and_execution(policy) is True


@pytest.mark.parametrize("field_name", workspace_module.UNSAFE_POLICY_ALLOW_NAMES)
def test_policy_rejects_unsafe_allow_values(field_name):
    with pytest.raises(ValueError):
        build_repair_workspace_isolation_policy(**{field_name: True})


def test_workspace_input_is_metadata_only_and_lists_prohibited_actions():
    workspace_input = build_repair_workspace_isolation_input()
    for action in workspace_module.PROHIBITED_RUNTIME_ACTIONS:
        assert action in workspace_input.prohibited_runtime_actions
    assert workspace_input.workspace_root_ref == "sandbox/repair/v0392/workspace-candidate"
    assert workspace_input.requested_mode == RepairWorkspaceIsolationMode.SANDBOX_REPAIR_WORKSPACE_ISOLATION_CONTRACT


def test_workspace_descriptor_accepts_declared_sandbox_metadata():
    descriptor = classify_repair_workspace_descriptor(build_repair_workspace_isolation_input())
    assert descriptor.declared_sandbox is True
    assert descriptor.declared_live_workspace is False
    assert descriptor.declared_reference_corpus is False
    assert descriptor.declared_secret_area is False
    assert descriptor.trust_level == RepairWorkspaceTrustLevel.TRUSTED_SANDBOX_CANDIDATE
    assert repair_workspace_descriptor_is_metadata_only(descriptor) is True


@pytest.mark.parametrize(
    ("workspace_kind", "root_ref", "expected_trust"),
    [
        (RepairWorkspaceKind.LIVE_WORKSPACE, "live/ChantaCore", RepairWorkspaceTrustLevel.REJECTED_LIVE_WORKSPACE),
        (RepairWorkspaceKind.REFERENCE_CORPUS, "references/OpenCode", RepairWorkspaceTrustLevel.REJECTED_REFERENCE_CORPUS),
        (RepairWorkspaceKind.SECRET_OR_CREDENTIAL_AREA, "sandbox/.env/token", RepairWorkspaceTrustLevel.REJECTED_SECRET_AREA),
    ],
)
def test_workspace_descriptor_rejects_or_review_gates_unsafe_areas(workspace_kind, root_ref, expected_trust):
    descriptor = classify_repair_workspace_descriptor(
        build_repair_workspace_isolation_input(workspace_kind=workspace_kind, workspace_root_ref=root_ref)
    )
    assert descriptor.trust_level == expected_trust
    assert descriptor.declared_sandbox is False


def test_descriptor_cannot_accept_live_workspace_as_trusted_future_input():
    with pytest.raises(ValueError):
        build_repair_workspace_descriptor(declared_live_workspace=True, trust_level=RepairWorkspaceTrustLevel.TRUSTED_SANDBOX_CANDIDATE)


def test_root_ref_validation_is_metadata_only_and_accepts_sandbox_ref():
    validation = validate_repair_workspace_root_ref_metadata(build_repair_workspace_descriptor())
    assert validation.normalized_root_ref == "sandbox/repair/v0392/workspace-candidate"
    assert validation.valid_for_future_patch_materialization_input is True
    assert validation.valid_for_future_sandbox_apply_input is True
    assert validation.metadata["filesystem_read_performed"] is False
    assert repair_workspace_root_ref_validation_does_not_read_files(validation) is True


@pytest.mark.parametrize(
    ("root_ref", "flag_name"),
    [
        ("sandbox/../live", "parent_traversal_like"),
        ("references/OpenCode/sample", "reference_corpus_like"),
        ("sandbox/secrets/token", "secret_path_like"),
        ("D:/ChantaResearchGroup/ChantaCore", "live_workspace_like"),
    ],
)
def test_root_ref_validation_rejects_risky_refs(root_ref, flag_name):
    validation = build_repair_workspace_root_ref_validation(workspace_root_ref=root_ref)
    assert getattr(validation, flag_name) is True
    assert validation.valid_for_future_patch_materialization_input is False
    assert validation.valid_for_future_sandbox_apply_input is False


def test_collision_prevention_plan_blocks_collision_without_runtime_actions():
    plan = create_repair_workspace_collision_prevention_plan(build_repair_workspace_descriptor())
    assert plan.parallel_agent_collision_blocked is True
    assert plan.shared_live_workspace_write_blocked is True
    assert plan.branch_collision_risk_mitigated is True
    assert plan.git_worktree_execution_performed is False
    assert plan.branch_creation_performed is False
    assert plan.workspace_creation_performed is False


def test_target_binding_binds_metadata_and_rejects_live_scope():
    descriptor = build_repair_workspace_descriptor()
    binding = bind_repair_workspace_target(descriptor)
    assert binding.target_bound_to_approved_patch is True
    assert binding.target_bound_to_safety_report is True
    assert binding.target_bound_to_human_review_packet is True
    assert binding.target_scope_sandbox_only is True
    assert binding.binding_valid_for_future_materialization is True
    assert binding.binding_valid_for_future_sandbox_apply is True
    with pytest.raises(ValueError):
        build_repair_workspace_target_binding(
            target_scope_live_apply=True,
            binding_valid_for_future_materialization=True,
            binding_valid_for_future_sandbox_apply=True,
        )


def test_live_boundary_check_requires_all_exclusions():
    check = check_repair_workspace_live_boundaries(build_repair_workspace_descriptor())
    assert check.live_workspace_excluded is True
    assert check.live_workspace_read_blocked is True
    assert check.live_workspace_write_blocked is True
    assert check.live_workspace_apply_blocked is True
    assert check.reference_corpus_excluded is True
    assert check.secret_paths_excluded is True
    with pytest.raises(ValueError):
        build_repair_workspace_live_boundary_check(live_workspace_read_blocked=False)


def test_risk_assessment_blocks_high_risk_workspace_confusion():
    descriptor = classify_repair_workspace_descriptor(
        build_repair_workspace_isolation_input(workspace_kind=RepairWorkspaceKind.LIVE_WORKSPACE, workspace_root_ref="live/ChantaCore")
    )
    root_validation = validate_repair_workspace_root_ref_metadata(descriptor)
    target_binding = bind_repair_workspace_target(descriptor)
    risk = assess_repair_workspace_isolation_risk(descriptor, root_validation, target_binding)
    assert risk.blocks_future_patch_materialization_input is True
    assert risk.blocks_future_sandbox_apply_input is True
    assert risk.requires_human_review is True
    assert risk.do_nothing_recommended is True
    with pytest.raises(ValueError):
        build_repair_workspace_isolation_risk_assessment(
            risk_kinds=[RepairWorkspaceIsolationRiskKind.LIVE_WORKSPACE_CONFUSION_RISK],
            blocks_future_sandbox_apply_input=False,
            requires_human_review=False,
        )


def test_decision_future_readiness_metadata_and_runtime_false():
    report = build_v0392_readiness_report()
    decision = report.decision
    assert decision.ready_for_future_patch_materialization_input is True
    assert decision.ready_for_future_sandbox_apply_input is True
    assert repair_workspace_decision_is_not_apply_permission(decision) is True
    for field_name in workspace_module.UNSAFE_DECISION_NAMES:
        assert getattr(decision, field_name) is False
    with pytest.raises(ValueError):
        build_repair_workspace_isolation_decision(sandbox_apply_allowed_now=True)


def test_readiness_report_future_readiness_and_runtime_false():
    report = build_v0392_readiness_report()
    assert report.ready_for_v0393_human_approved_patch_materialization_sandbox_apply is True
    assert report.ready_for_workspace_descriptor_metadata is True
    assert report.ready_for_workspace_root_ref_metadata is True
    assert report.ready_for_workspace_classification_metadata is True
    assert report.ready_for_sandbox_repair_workspace_isolation_contract is True
    assert report.ready_for_collision_prevention_metadata is True
    assert report.ready_for_apply_target_isolation_metadata is True
    assert report.ready_for_live_workspace_exclusion_metadata is True
    assert report.ready_for_future_patch_materialization_input is True
    assert report.ready_for_future_sandbox_apply_input is True
    assert v0392_readiness_report_is_not_execution_ready(report) is True
    for field_name in workspace_module.UNSAFE_REPORT_NAMES:
        assert getattr(report, field_name) is False
    with pytest.raises(ValueError):
        build_v0392_readiness_report(sandbox_apply_enabled=True)
    with pytest.raises(ValueError):
        build_v0392_readiness_report(patch_materialization_enabled=True)
    with pytest.raises(ValueError):
        build_v0392_readiness_report(ready_for_execution=True)


def test_no_mutation_guarantee_all_true():
    guarantee = build_repair_workspace_isolation_no_mutation_guarantee()
    assert isinstance(guarantee, RepairWorkspaceIsolationNoMutationGuarantee)
    for field_name, value in vars(guarantee).items():
        if field_name.startswith("no_"):
            assert value is True


def test_validation_report_confirms_metadata_only_no_runtime():
    report = build_repair_workspace_isolation_validation_report()
    assert report.confirms_metadata_only_workspace_isolation_contract is True
    assert report.confirms_no_workspace_creation is True
    assert report.confirms_no_git_worktree is True
    assert report.confirms_no_branch_creation is True
    assert report.confirms_no_source_read is True
    assert report.confirms_no_filesystem_scan is True
    assert report.confirms_no_file_write is True
    assert report.confirms_no_patch_materialization is True
    assert report.confirms_no_patch_application is True
    assert report.confirms_no_test_execution is True
    assert report.confirms_no_self_prompt_execution is True
    assert report.confirms_no_subagent_invocation is True
    assert report.confirms_no_model_provider is True
    assert report.confirms_no_external_agent is True
    assert report.confirms_no_dominion is True
    assert report.confirms_no_production_certification is True


def test_helper_pipeline_blocks_unsafe_inputs():
    workspace_input = build_repair_workspace_isolation_input(
        workspace_kind=RepairWorkspaceKind.REFERENCE_CORPUS,
        workspace_root_ref="references/Hermes/sample",
    )
    descriptor = classify_repair_workspace_descriptor(workspace_input)
    root_validation = validate_repair_workspace_root_ref_metadata(descriptor)
    target_binding = bind_repair_workspace_target(descriptor)
    risk = assess_repair_workspace_isolation_risk(descriptor, root_validation, target_binding)
    decision = decide_repair_workspace_isolation(descriptor, root_validation, target_binding, risk)
    assert decision.ready_for_future_patch_materialization_input is False
    assert decision.ready_for_future_sandbox_apply_input is False
    assert repair_workspace_decision_is_not_apply_permission(decision) is True


def test_helpers_do_not_expose_runtime_side_effect_patterns():
    source = inspect.getsource(workspace_module)
    forbidden_patterns = [
        "Path.exists",
        "Path.read_text",
        "Path.read_bytes",
        "Path.write_text",
        "Path.write_bytes",
        "os.walk",
        "rglob",
        "glob(",
        "mkdir(",
        "git worktree",
        "git checkout",
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "apply_patch(",
        "git apply",
        "requests",
        "httpx",
        "urllib",
        "aiohttp",
        "socket",
        "ready_for_execution=True",
        "production_certified=True",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source
