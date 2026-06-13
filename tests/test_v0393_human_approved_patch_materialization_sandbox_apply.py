import inspect

import pytest

from chanta_core.agent_runtime import (
    RepairSandboxApplyAudit,
    RepairSandboxApplyDecision,
    RepairSandboxApplyDecisionKind,
    RepairSandboxApplyDisposition,
    RepairSandboxApplyFailureKind,
    RepairSandboxApplyFlagSet,
    RepairSandboxApplyInput,
    RepairSandboxApplyMode,
    RepairSandboxApplyOperation,
    RepairSandboxApplyOperationKind,
    RepairSandboxApplyPolicy,
    RepairSandboxApplyPreflight,
    RepairSandboxApplyReadinessLevel,
    RepairSandboxApplyResult,
    RepairSandboxApplyRiskKind,
    RepairSandboxApplyRunPreview,
    RepairSandboxApplySandboxOnlyGuarantee,
    RepairSandboxApplySourceKind,
    RepairSandboxApplySourceRef,
    RepairSandboxApplyStatus,
    RepairSandboxApplyTarget,
    RepairSandboxApplyTargetKind,
    RepairSandboxApplyTransaction,
    RepairSandboxApplyValidationFinding,
    RepairSandboxApplyValidationReport,
    RepairSandboxPatchMaterialization,
    RepairSandboxPatchMaterializationKind,
    V0393ReadinessReport,
    apply_sandbox_text_replacements,
    audit_sandbox_apply_result,
    build_repair_sandbox_apply_audit,
    build_repair_sandbox_apply_decision,
    build_repair_sandbox_apply_flags,
    build_repair_sandbox_apply_input,
    build_repair_sandbox_apply_operation,
    build_repair_sandbox_apply_policy,
    build_repair_sandbox_apply_preflight,
    build_repair_sandbox_apply_result,
    build_repair_sandbox_apply_run_preview,
    build_repair_sandbox_apply_sandbox_only_guarantee,
    build_repair_sandbox_apply_source_ref,
    build_repair_sandbox_apply_target,
    build_repair_sandbox_apply_transaction,
    build_repair_sandbox_apply_validation_finding,
    build_repair_sandbox_apply_validation_report,
    build_repair_sandbox_patch_materialization,
    build_v0393_readiness_report,
    create_sandbox_apply_operations,
    create_sandbox_apply_preflight,
    decide_repair_sandbox_apply,
    default_repair_sandbox_apply_policy,
    materialize_patch_from_proposed_hunks,
    repair_sandbox_apply_flags_preserve_no_live_execution,
    repair_sandbox_apply_policy_blocks_live_apply_and_runtime,
    sandbox_apply_result_is_not_test_or_repair_execution,
    sandbox_apply_target_is_not_live_target,
    sandbox_patch_materialization_is_not_patch_file_export,
    v0393_readiness_report_is_not_general_execution_ready,
    validate_sandbox_apply_target,
)
from chanta_core.agent_runtime import repair_sandbox_apply as sandbox_module


UNSAFE_FLAG_FIELDS = [
    "ready_for_execution",
    "ready_for_git_worktree_creation",
    "ready_for_filesystem_scan",
    "ready_for_live_workspace_read",
    "ready_for_live_workspace_apply",
    "ready_for_patch_file_write",
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


def test_all_v0393_enum_values_exist():
    assert {item.value for item in RepairSandboxApplyMode} == {
        "human_approved_patch_materialization",
        "sandbox_apply_preflight",
        "sandbox_apply_plan",
        "sandbox_text_replacement_apply",
        "sandbox_apply_transaction",
        "sandbox_apply_result",
        "sandbox_apply_audit",
        "rollback_discard_metadata",
        "future_post_apply_retest_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert {item.value for item in RepairSandboxApplySourceKind} == {
        "v0392_workspace_isolation_decision",
        "v0392_workspace_descriptor",
        "v0392_target_binding",
        "v0392_live_boundary_check",
        "v0391_approval_artifact_decision",
        "v0391_approval_process_state_gate",
        "v0391_approval_artifact",
        "v0390_repair_apply_boundary",
        "v0384_proposed_patch_envelope",
        "v0384_proposed_diff_metadata",
        "v0384_proposed_code_hunk",
        "v0385_safety_report",
        "v0386_human_review_packet",
        "supplied_sandbox_root",
        "supplied_sandbox_target_file",
        "test_fixture",
        "unknown",
    }
    assert {item.value for item in RepairSandboxApplyStatus} == {
        "unknown",
        "draft",
        "input_validated",
        "preflight_completed",
        "patch_materialized",
        "apply_plan_created",
        "apply_transaction_created",
        "sandbox_apply_completed",
        "sandbox_apply_completed_with_warnings",
        "sandbox_apply_blocked",
        "sandbox_apply_failed",
        "rollback_in_memory_completed",
        "ready_for_future_post_apply_retest",
        "blocked",
        "rejected",
        "review_required",
        "no_op",
        "safe_failed",
    }
    assert {item.value for item in RepairSandboxApplyReadinessLevel} == {
        "not_ready",
        "approval_gate_ready",
        "workspace_isolation_ready",
        "patch_materialization_ready",
        "sandbox_apply_preflight_ready",
        "sandbox_apply_plan_ready",
        "sandbox_apply_transaction_ready",
        "sandbox_apply_result_ready",
        "future_post_apply_retest_input_ready",
        "design_handoff_ready_for_v0394",
        "blocked",
        "future_track",
    }
    assert {item.value for item in RepairSandboxApplyDecisionKind} == {
        "allow_patch_materialization",
        "allow_sandbox_apply_preflight",
        "allow_sandbox_apply_plan",
        "allow_sandbox_text_replacement_apply",
        "allow_sandbox_apply_transaction",
        "allow_sandbox_apply_result",
        "allow_future_post_apply_retest_input",
        "choose_do_nothing",
        "choose_human_review_required",
        "deny",
        "block",
        "reject_missing_approval_gate",
        "reject_invalid_workspace",
        "reject_live_workspace_target",
        "reject_reference_corpus_target",
        "reject_secret_target",
        "reject_path_escape",
        "reject_symlink_target",
        "reject_binary_target",
        "reject_original_text_mismatch",
        "reject_unapproved_patch",
        "reject_unsafe_patch",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert {item.value for item in RepairSandboxPatchMaterializationKind} == {
        "structured_hunk_text_replacement",
        "bounded_unified_diff_metadata_render",
        "in_memory_patch_materialization",
        "rejected_patch_file_export",
        "unsupported",
        "unknown",
    }
    assert {item.value for item in RepairSandboxApplyOperationKind} == {
        "exact_text_replace",
        "insert_after_anchor",
        "insert_before_anchor",
        "delete_exact_text",
        "no_op",
        "unsupported",
        "unknown",
    }
    assert {item.value for item in RepairSandboxApplyTargetKind} == {
        "sandbox_text_file",
        "sandbox_test_file",
        "sandbox_config_file",
        "live_workspace_file",
        "reference_corpus_file",
        "secret_or_credential_file",
        "binary_file",
        "unknown",
    }
    assert {item.value for item in RepairSandboxApplyDisposition} == {
        "sandbox_apply_completed",
        "sandbox_apply_completed_with_warnings",
        "blocked",
        "rejected",
        "review_required",
        "do_nothing_preferred",
        "no_op",
        "failed",
        "unknown",
    }
    assert {item.value for item in RepairSandboxApplyFailureKind} == {
        "missing_approval_gate",
        "invalid_workspace",
        "target_outside_sandbox",
        "live_workspace_target",
        "reference_corpus_target",
        "secret_target",
        "symlink_target",
        "binary_target",
        "original_text_not_found",
        "original_text_ambiguous",
        "write_failed",
        "rollback_failed",
        "unsupported_operation",
        "unsafe_patch",
        "unknown",
    }
    assert "apply_patch_confusion_risk" in {item.value for item in RepairSandboxApplyRiskKind}


def test_required_models_construct():
    assert isinstance(build_repair_sandbox_apply_source_ref(), RepairSandboxApplySourceRef)
    assert isinstance(build_repair_sandbox_apply_policy(), RepairSandboxApplyPolicy)
    assert isinstance(build_repair_sandbox_apply_input(), RepairSandboxApplyInput)
    assert isinstance(build_repair_sandbox_patch_materialization(), RepairSandboxPatchMaterialization)
    assert isinstance(build_repair_sandbox_apply_target(), RepairSandboxApplyTarget)
    assert isinstance(build_repair_sandbox_apply_preflight(), RepairSandboxApplyPreflight)
    assert isinstance(build_repair_sandbox_apply_operation(), RepairSandboxApplyOperation)
    assert isinstance(build_repair_sandbox_apply_transaction(), RepairSandboxApplyTransaction)
    assert isinstance(build_repair_sandbox_apply_result(), RepairSandboxApplyResult)
    assert isinstance(build_repair_sandbox_apply_audit(), RepairSandboxApplyAudit)
    assert isinstance(build_repair_sandbox_apply_decision(), RepairSandboxApplyDecision)
    assert isinstance(build_repair_sandbox_apply_validation_finding(), RepairSandboxApplyValidationFinding)
    assert isinstance(build_repair_sandbox_apply_validation_report(), RepairSandboxApplyValidationReport)
    assert isinstance(build_repair_sandbox_apply_run_preview(), RepairSandboxApplyRunPreview)
    assert isinstance(build_v0393_readiness_report(), V0393ReadinessReport)


def test_flag_set_allows_sandbox_apply_and_blocks_runtime():
    flags = build_repair_sandbox_apply_flags()
    assert isinstance(flags, RepairSandboxApplyFlagSet)
    assert flags.sandbox_apply_layer_constructed is True
    assert flags.sandbox_patch_materialization_available is True
    assert flags.ready_for_bounded_sandbox_target_read is True
    assert flags.ready_for_bounded_sandbox_target_write is True
    assert flags.ready_for_sandbox_patch_materialization is True
    assert flags.ready_for_sandbox_repair_apply is True
    assert flags.ready_for_future_post_apply_retest_input is True
    assert repair_sandbox_apply_flags_preserve_no_live_execution(flags) is True
    for field_name in UNSAFE_FLAG_FIELDS:
        assert getattr(flags, field_name) is False


@pytest.mark.parametrize("field_name", UNSAFE_FLAG_FIELDS)
def test_flags_reject_unsafe_true_values(field_name):
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_flags(**{field_name: True})


def test_policy_allows_sandbox_only_apply_and_blocks_runtime():
    policy = default_repair_sandbox_apply_policy(max_file_changes=0, max_hunks=0, max_file_bytes=0)
    assert policy.allow_in_memory_patch_materialization is True
    assert policy.allow_bounded_sandbox_target_read is True
    assert policy.allow_bounded_sandbox_target_write is True
    assert policy.allow_sandbox_text_replacement_apply is True
    assert policy.allow_sandbox_apply_transaction is True
    assert policy.allow_future_post_apply_retest_input is True
    assert policy.require_approval_decision is True
    assert policy.require_workspace_isolation_decision is True
    assert policy.require_safety_report is True
    assert policy.require_proposed_patch_envelope is True
    assert policy.require_exact_original_text_match is True
    assert policy.require_sandbox_root_containment is True
    assert policy.reject_live_workspace_targets is True
    assert policy.reject_reference_targets is True
    assert policy.reject_secret_targets is True
    assert policy.reject_symlink_targets is True
    assert policy.reject_binary_targets is True
    assert repair_sandbox_apply_policy_blocks_live_apply_and_runtime(policy) is True


@pytest.mark.parametrize("field_name", sandbox_module.UNSAFE_POLICY_ALLOW_NAMES)
def test_policy_rejects_unsafe_allow_values(field_name):
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_policy(**{field_name: True})


def test_sandbox_apply_input_is_not_live_apply_request():
    apply_input = build_repair_sandbox_apply_input()
    assert apply_input.requested_mode == RepairSandboxApplyMode.SANDBOX_TEXT_REPLACEMENT_APPLY
    for action in sandbox_module.PROHIBITED_RUNTIME_ACTIONS:
        assert action in apply_input.prohibited_runtime_actions


def test_patch_materialization_is_in_memory_only():
    materialization = materialize_patch_from_proposed_hunks(
        "patch-envelope-1",
        [{"target_relative_path": "src/example.py", "original_text": "old", "replacement_text": "new"}],
    )
    assert materialization.in_memory_only is True
    assert materialization.patch_file_written is False
    assert materialization.patch_file_path is None
    assert sandbox_patch_materialization_is_not_patch_file_export(materialization) is True
    with pytest.raises(ValueError):
        build_repair_sandbox_patch_materialization(patch_file_written=True)


def test_apply_target_accepts_sandbox_contained_relative_path(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    target = validate_sandbox_apply_target(str(sandbox_root), "src/example.py")
    assert target.inside_sandbox_root is True
    assert target.eligible_for_sandbox_apply is True
    assert sandbox_apply_target_is_not_live_target(target) is True


@pytest.mark.parametrize(
    ("target_path", "target_kind", "flag_name"),
    [
        ("live/ChantaCore/file.py", RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE, "live_workspace_like"),
        ("references/OpenCode/file.py", RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE, "reference_corpus_like"),
        ("secrets/token.txt", RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE, "secret_path_like"),
        ("../escape.py", RepairSandboxApplyTargetKind.SANDBOX_TEXT_FILE, "path_traversal_like"),
        ("image.png", RepairSandboxApplyTargetKind.BINARY_FILE, "binary_target"),
    ],
)
def test_apply_target_rejects_unsafe_targets(tmp_path, target_path, target_kind, flag_name):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    target = validate_sandbox_apply_target(str(sandbox_root), target_path, target_kind)
    assert getattr(target, flag_name) is True
    assert target.eligible_for_sandbox_apply is False


def test_apply_target_rejects_symlink_target(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("outside", encoding="utf-8")
    link = sandbox_root / "link.txt"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlink creation is unavailable on this platform")
    target = validate_sandbox_apply_target(str(sandbox_root), "link.txt")
    assert target.symlink_target is True
    assert target.eligible_for_sandbox_apply is False


def test_preflight_fails_on_missing_gates_or_ineligible_targets(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    good_target = validate_sandbox_apply_target(str(sandbox_root), "good.txt")
    bad_target = validate_sandbox_apply_target(str(sandbox_root), "../bad.txt")
    assert build_repair_sandbox_apply_preflight(approval_gate_valid=False).preflight_passed is False
    assert build_repair_sandbox_apply_preflight(workspace_isolation_valid=False).preflight_passed is False
    assert build_repair_sandbox_apply_preflight(targets=[good_target]).preflight_passed is True
    assert build_repair_sandbox_apply_preflight(targets=[bad_target]).preflight_passed is False


def test_operation_requires_exact_match_and_rejects_invalid_applied_state():
    target = build_repair_sandbox_apply_target()
    operation = build_repair_sandbox_apply_operation(target=target)
    assert operation.exact_match_required is True
    assert operation.applied is False
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_operation(target=target, exact_match_required=False)
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_operation(target=target, ambiguous_match_found=True, applied=True)


def test_apply_sandbox_text_replacements_changes_only_sandbox_target_file(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    target_file = sandbox_root / "example.txt"
    target_file.write_text("alpha before omega", encoding="utf-8")
    outside_file = tmp_path / "outside.txt"
    outside_file.write_text("before", encoding="utf-8")
    apply_input = build_repair_sandbox_apply_input(sandbox_root_ref=str(sandbox_root))
    operations = create_sandbox_apply_operations(
        str(sandbox_root),
        [{"target_relative_path": "example.txt", "original_text": "before", "replacement_text": "after"}],
    )
    transaction, result, applied_ops = apply_sandbox_text_replacements(apply_input, operations)
    assert transaction.max_cycle_count == 1
    assert transaction.apply_attempt_count <= 1
    assert transaction.sandbox_only is True
    assert transaction.live_workspace_touched is False
    assert transaction.tests_run is False
    assert result.sandbox_apply_completed is True
    assert result.ready_for_future_post_apply_retest_input is True
    assert result.tests_run is False
    assert result.repair_executed is False
    assert result.self_prompt_generated is False
    assert result.self_prompt_executed is False
    assert result.subagent_invoked is False
    assert result.model_invoked is False
    assert result.external_agent_invoked is False
    assert result.dominion_runtime_invoked is False
    assert target_file.read_text(encoding="utf-8") == "alpha after omega"
    assert outside_file.read_text(encoding="utf-8") == "before"
    assert applied_ops[0].applied is True


def test_apply_sandbox_text_replacements_fails_on_missing_or_ambiguous_text(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    target_file = sandbox_root / "example.txt"
    target_file.write_text("before before", encoding="utf-8")
    apply_input = build_repair_sandbox_apply_input(sandbox_root_ref=str(sandbox_root))
    ambiguous_ops = create_sandbox_apply_operations(
        str(sandbox_root),
        [{"target_relative_path": "example.txt", "original_text": "before", "replacement_text": "after"}],
    )
    _, ambiguous_result, ambiguous_operation_results = apply_sandbox_text_replacements(apply_input, ambiguous_ops)
    assert ambiguous_result.sandbox_apply_completed is False
    assert RepairSandboxApplyFailureKind.ORIGINAL_TEXT_AMBIGUOUS in ambiguous_result.failure_kinds
    assert ambiguous_operation_results[0].failed is True
    assert target_file.read_text(encoding="utf-8") == "before before"

    missing_ops = create_sandbox_apply_operations(
        str(sandbox_root),
        [{"target_relative_path": "example.txt", "original_text": "missing", "replacement_text": "after"}],
    )
    _, missing_result, _ = apply_sandbox_text_replacements(apply_input, missing_ops)
    assert missing_result.sandbox_apply_completed is False
    assert RepairSandboxApplyFailureKind.ORIGINAL_TEXT_NOT_FOUND in missing_result.failure_kinds


def test_apply_helper_cannot_touch_path_outside_sandbox_root(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    outside = tmp_path / "outside.txt"
    outside.write_text("before", encoding="utf-8")
    apply_input = build_repair_sandbox_apply_input(sandbox_root_ref=str(sandbox_root))
    operations = create_sandbox_apply_operations(
        str(sandbox_root),
        [{"target_relative_path": "../outside.txt", "original_text": "before", "replacement_text": "after"}],
    )
    _, result, _ = apply_sandbox_text_replacements(apply_input, operations)
    assert result.sandbox_apply_completed is False
    assert outside.read_text(encoding="utf-8") == "before"


def test_audit_confirms_no_live_runtime_or_tests():
    audit = build_repair_sandbox_apply_audit()
    assert audit.approval_gate_confirmed is True
    assert audit.workspace_isolation_confirmed is True
    assert audit.sandbox_root_containment_confirmed is True
    assert audit.live_workspace_exclusion_confirmed is True
    assert audit.exact_text_match_confirmed is True
    assert audit.no_patch_file_export_confirmed is True
    assert audit.no_apply_patch_confirmed is True
    assert audit.no_git_apply_confirmed is True
    assert audit.no_shell_confirmed is True
    assert audit.no_subprocess_confirmed is True
    assert audit.no_test_execution_confirmed is True
    assert audit.no_self_prompt_execution_confirmed is True
    assert audit.no_subagent_invocation_confirmed is True
    assert audit.no_model_invocation_confirmed is True
    assert audit.no_external_agent_confirmed is True
    assert audit.no_dominion_runtime_confirmed is True
    assert audit.no_production_certification_confirmed is True


def test_decision_allows_sandbox_only_apply_and_blocks_runtime():
    decision = decide_repair_sandbox_apply(build_repair_sandbox_apply_result())
    assert decision.patch_materialization_allowed_now is True
    assert decision.sandbox_target_read_allowed_now is True
    assert decision.sandbox_target_write_allowed_now is True
    assert decision.sandbox_apply_allowed_now is True
    for field_name in sandbox_module.UNSAFE_DECISION_NAMES:
        assert getattr(decision, field_name) is False
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_decision(live_apply_allowed_now=True)


def test_readiness_report_sandbox_enabled_but_general_execution_false():
    report = build_v0393_readiness_report()
    assert report.sandbox_apply_completed is True
    assert report.patch_materialization_enabled is True
    assert report.bounded_sandbox_target_read_enabled is True
    assert report.bounded_sandbox_target_write_enabled is True
    assert report.sandbox_apply_enabled is True
    assert report.ready_for_future_post_apply_retest_input is True
    assert v0393_readiness_report_is_not_general_execution_ready(report) is True
    for field_name in sandbox_module.UNSAFE_REPORT_NAMES:
        assert getattr(report, field_name) is False
    with pytest.raises(ValueError):
        build_v0393_readiness_report(live_apply_enabled=True)
    with pytest.raises(ValueError):
        build_v0393_readiness_report(test_execution_enabled=True)
    with pytest.raises(ValueError):
        build_v0393_readiness_report(ready_for_execution=True)


def test_sandbox_only_guarantee_all_true():
    guarantee = build_repair_sandbox_apply_sandbox_only_guarantee()
    assert isinstance(guarantee, RepairSandboxApplySandboxOnlyGuarantee)
    for field_name, value in vars(guarantee).items():
        if field_name.startswith("no_"):
            assert value is True


def test_result_cannot_claim_test_or_repair_execution():
    assert sandbox_apply_result_is_not_test_or_repair_execution(build_repair_sandbox_apply_result()) is True
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_result(tests_run=True)
    with pytest.raises(ValueError):
        build_repair_sandbox_apply_result(repair_executed=True)


def test_validation_report_confirms_sandbox_only_boundary():
    report = build_repair_sandbox_apply_validation_report()
    assert report.confirms_approval_gate is True
    assert report.confirms_workspace_isolation is True
    assert report.confirms_target_containment is True
    assert report.confirms_exact_match is True
    assert report.confirms_sandbox_only_apply is True
    assert report.confirms_no_live_apply is True
    assert report.confirms_no_patch_file_export is True
    assert report.confirms_no_apply_patch is True
    assert report.confirms_no_git_apply is True
    assert report.confirms_no_shell_subprocess is True
    assert report.confirms_no_test_execution is True
    assert report.confirms_no_self_prompt_execution is True
    assert report.confirms_no_subagent_invocation is True
    assert report.confirms_no_model_provider is True
    assert report.confirms_no_external_agent is True
    assert report.confirms_no_dominion is True
    assert report.confirms_no_production_certification is True


def test_module_does_not_contain_forbidden_runtime_invocation_patterns():
    source = inspect.getsource(sandbox_module)
    forbidden_patterns = [
        "os.walk",
        "rglob(",
        "glob(",
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
