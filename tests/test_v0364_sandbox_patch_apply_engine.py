import inspect

import pytest

from chanta_core.agent_runtime import (
    SandboxFileWriteKind,
    SandboxFileWriteStatus,
    SandboxMaterializationStatus,
    SandboxPatchApplyDecisionKind,
    SandboxPatchApplyMode,
    SandboxPatchApplyReadinessLevel,
    SandboxPatchApplyRiskKind,
    SandboxPatchApplySourceKind,
    SandboxPatchApplyStatus,
    SandboxPatchEngineStatus,
    SandboxPatchEngineStrategy,
    build_dry_run_apply_input,
    build_dry_run_source_image,
    build_sandbox_file_materialization_plan,
    build_sandbox_file_write_operation,
    build_sandbox_file_write_record,
    build_sandbox_manifest_from_dry_run_result,
    build_sandbox_materialization_plan,
    build_sandbox_materialization_plan_from_manifest,
    build_sandbox_overlay_entry,
    build_sandbox_patch_apply_decision,
    build_sandbox_patch_apply_flags,
    build_sandbox_patch_apply_input,
    build_sandbox_patch_apply_input_from_manifest,
    build_sandbox_patch_apply_no_live_write_guarantee,
    build_sandbox_patch_apply_policy,
    build_sandbox_patch_apply_report,
    build_sandbox_patch_apply_result,
    build_sandbox_patch_apply_run_preview,
    build_sandbox_patch_apply_source_ref,
    build_sandbox_patch_apply_validation_report,
    build_sandbox_patch_engine_file_result,
    build_sandbox_patch_engine_operation,
    build_sandbox_workspace_input_from_dry_run_result,
    build_v0364_readiness_report,
    default_sandbox_patch_apply_policy,
    run_dry_run_apply_simulation,
    run_sandbox_patch_apply,
    sandbox_file_write_record_is_sandbox_only,
    sandbox_patch_apply_decision_is_not_live_apply_permission,
    sandbox_patch_apply_flags_preserve_no_live_write,
    sandbox_patch_apply_policy_blocks_live_write,
    sandbox_patch_apply_result_is_not_live_apply,
    v0364_readiness_report_is_not_execution_ready,
    validate_sandbox_apply_path_containment,
    validate_sandbox_patch_apply_result,
    write_sandbox_file_under_policy,
)
import chanta_core.agent_runtime.patch_apply_engine as engine


SIMPLE_DIFF = """--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,3 @@
 alpha
-beta
+BETA
 gamma
"""


def values(enum_cls):
    return {item.value for item in enum_cls}


def successful_manifest(tmp_path):
    dry_input = build_dry_run_apply_input()
    source_image = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\n")
    result = run_dry_run_apply_simulation(dry_input, SIMPLE_DIFF, [source_image])
    workspace_input = build_sandbox_workspace_input_from_dry_run_result(
        result,
        requested_sandbox_root_ref=str(tmp_path),
    )
    return build_sandbox_manifest_from_dry_run_result(result, workspace_input=workspace_input)


def test_taxonomies_are_complete():
    assert values(SandboxPatchApplyMode) == {
        "materialize_from_dry_run_result",
        "materialize_from_overlay_manifest",
        "sandbox_apply_structured_patch",
        "sandbox_apply_unified_diff_after_dry_run",
        "metadata_only",
        "blocked",
        "no_op",
        "unknown",
    }
    assert values(SandboxPatchApplySourceKind) == {
        "v0363_sandbox_workspace_manifest",
        "v0363_sandbox_workspace_plan",
        "v0363_sandbox_workspace_policy",
        "v0362_dry_run_apply_simulation_result",
        "v0362_simulated_file_result",
        "v0362_simulated_file_delta",
        "v0361_apply_candidate_envelope",
        "v0361_human_approval_contract",
        "test_fixture",
        "unknown",
    }
    assert values(SandboxPatchApplyStatus) == {
        "unknown",
        "draft",
        "input_validated",
        "materialization_planned",
        "sandbox_materialized",
        "sandbox_apply_completed",
        "sandbox_apply_completed_with_warnings",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
        "safe_failed",
    }
    assert values(SandboxPatchApplyReadinessLevel) == {
        "not_ready",
        "sandbox_apply_contract_ready",
        "sandbox_materialization_ready",
        "sandbox_file_write_ready",
        "sandbox_apply_result_ready",
        "design_handoff_ready_for_v0365",
        "design_handoff_ready_for_v0366",
        "blocked",
        "future_track",
    }
    assert values(SandboxPatchApplyDecisionKind) == {
        "allow_sandbox_materialization",
        "allow_sandbox_file_write",
        "allow_sandbox_patch_apply",
        "allow_future_post_apply_validation_input",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert values(SandboxPatchApplyRiskKind) == {
        "live_workspace_write_risk",
        "sandbox_escape_risk",
        "symlink_escape_risk",
        "outside_root_write_risk",
        "path_traversal_risk",
        "absolute_path_risk",
        "reference_root_write_risk",
        "secret_path_risk",
        "credential_path_risk",
        "binary_target_risk",
        "unresolved_dry_run_conflict_risk",
        "stale_manifest_risk",
        "partial_apply_risk",
        "write_record_missing_risk",
        "patch_apply_confusion_risk",
        "apply_patch_risk",
        "git_apply_risk",
        "shell_execution_risk",
        "test_execution_risk",
        "external_agent_execution_risk",
        "dominion_runtime_risk",
        "unknown",
    }
    assert values(SandboxMaterializationStatus) == {
        "unknown",
        "not_materialized",
        "planned",
        "materialized",
        "materialized_with_warnings",
        "blocked",
        "skipped",
        "safe_failed",
    }
    assert values(SandboxFileWriteKind) == {
        "create_sandbox_file",
        "overwrite_sandbox_file",
        "update_sandbox_file",
        "create_sandbox_directory",
        "write_sandbox_manifest_copy",
        "blocked_live_write",
        "blocked_reference_write",
        "blocked_outside_root_write",
        "no_op",
        "unknown",
    }
    assert values(SandboxFileWriteStatus) == {
        "unknown",
        "planned",
        "written",
        "skipped",
        "blocked",
        "failed_safe",
        "no_op",
    }
    assert values(SandboxPatchEngineStrategy) == {
        "write_simulated_after_content",
        "apply_structured_patch_in_memory_then_write_sandbox",
        "apply_unified_diff_in_memory_then_write_sandbox",
        "materialize_overlay_entries",
        "metadata_only",
        "blocked",
        "unknown",
    }
    assert values(SandboxPatchEngineStatus) == {
        "unknown",
        "initialized",
        "validated",
        "applied_to_sandbox",
        "applied_to_sandbox_with_warnings",
        "blocked",
        "safe_failed",
        "no_op",
    }


def test_flags_allow_sandbox_readiness_but_preserve_no_live_write():
    flags = build_sandbox_patch_apply_flags()

    assert flags.sandbox_patch_apply_engine_constructed is True
    assert flags.sandbox_materialization_available is True
    assert flags.sandbox_file_write_available is True
    assert flags.sandbox_patch_apply_available is True
    assert flags.ready_for_sandbox_workspace_materialization is True
    assert flags.ready_for_sandbox_workspace_write is True
    assert flags.ready_for_sandbox_patch_apply is True
    assert flags.ready_for_v0365_sandbox_post_apply_validation is True
    assert flags.ready_for_v0366_bounded_agentic_task_operation_cycle is True
    assert sandbox_patch_apply_flags_preserve_no_live_write(flags)


@pytest.mark.parametrize(
    "flag_name",
    [
        "ready_for_execution",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
        "ready_for_external_agent_execution",
        "ready_for_dominion_runtime",
        "ready_for_independent_agent_runtime",
        "ready_for_multi_cycle_agentic_loop",
        "production_certified",
    ],
)
def test_flags_reject_unsafe_live_readiness(flag_name):
    with pytest.raises(ValueError):
        build_sandbox_patch_apply_flags(**{flag_name: True})


def test_source_ref_policy_and_input_are_sandbox_only():
    source_ref = build_sandbox_patch_apply_source_ref()
    policy = default_sandbox_patch_apply_policy()
    apply_input = build_sandbox_patch_apply_input()

    assert source_ref.source_kind == SandboxPatchApplySourceKind.V0363_SANDBOX_WORKSPACE_MANIFEST
    assert policy.allow_sandbox_directory_creation is True
    assert policy.allow_sandbox_file_write is True
    assert policy.allow_sandbox_patch_apply is True
    assert policy.allow_partial_safe_apply is False
    assert sandbox_patch_apply_policy_blocks_live_write(policy)
    assert "live_write" in apply_input.prohibited_runtime_actions
    assert "apply_patch" in apply_input.prohibited_runtime_actions
    assert "git_apply" in apply_input.prohibited_runtime_actions
    assert "shell" in apply_input.prohibited_runtime_actions


@pytest.mark.parametrize(
    "allow_name",
    [
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_workspace_write",
        "allow_code_edit",
        "allow_apply_patch",
        "allow_git_apply",
        "allow_test_execution",
        "allow_shell",
        "allow_dependency_install",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_policy_rejects_live_or_external_allow_flags(allow_name):
    with pytest.raises(ValueError):
        build_sandbox_patch_apply_policy(**{allow_name: True})


def test_materialization_write_and_result_artifacts_are_not_live_apply():
    materialization_plan = build_sandbox_materialization_plan()
    file_plan = build_sandbox_file_materialization_plan()
    operation = build_sandbox_file_write_operation()
    record = build_sandbox_file_write_record()
    engine_operation = build_sandbox_patch_engine_operation()
    file_result = build_sandbox_patch_engine_file_result()
    apply_result = build_sandbox_patch_apply_result()

    assert materialization_plan.ready_for_materialization is True
    assert materialization_plan.ready_for_live_write is False
    assert materialization_plan.ready_for_execution is False
    assert file_plan.ready_for_sandbox_write is True
    assert file_plan.ready_for_live_write is False
    assert operation.live_write is False
    assert record.live_write is False
    assert record.wrote_outside_sandbox is False
    assert sandbox_file_write_record_is_sandbox_only(record)
    assert engine_operation.used_apply_patch is False
    assert engine_operation.used_git_apply is False
    assert engine_operation.used_shell is False
    assert file_result.sandbox_write_successful is True
    assert file_result.live_write is False
    assert file_result.ready_for_live_apply is False
    assert apply_result.sandbox_apply_successful is True
    assert apply_result.live_write_performed is False
    assert apply_result.used_apply_patch is False
    assert apply_result.used_git_apply is False
    assert apply_result.used_shell is False
    assert apply_result.ready_for_live_workspace_write is False
    assert apply_result.ready_for_patch_application is False
    assert sandbox_patch_apply_result_is_not_live_apply(apply_result)

    with pytest.raises(ValueError):
        build_sandbox_file_write_record(live_write=True)
    with pytest.raises(ValueError):
        build_sandbox_patch_engine_operation(used_apply_patch=True)
    with pytest.raises(ValueError):
        build_sandbox_patch_apply_result(live_write_performed=True)
    with pytest.raises(ValueError):
        build_sandbox_patch_apply_result(ready_for_patch_application=True)


def test_tmp_path_sandbox_root_materialization_writes_under_root_only(tmp_path):
    manifest = successful_manifest(tmp_path)
    apply_input = build_sandbox_patch_apply_input_from_manifest(manifest, sandbox_root_ref=str(tmp_path))
    plan = build_sandbox_materialization_plan_from_manifest(manifest, apply_input)
    result = run_sandbox_patch_apply(apply_input, plan)

    target = tmp_path / "src" / "example.py"
    assert result.sandbox_apply_successful is True
    assert target.exists()
    assert target.read_text(encoding="utf-8") == "alpha\nBETA\ngamma"
    assert result.files_written_count == 1
    assert result.live_write_performed is False
    assert result.ready_for_patch_application is False
    assert sandbox_patch_apply_result_is_not_live_apply(result)
    assert all(str(tmp_path) in record.sandbox_root_ref for record in result.write_records)


@pytest.mark.parametrize(
    "target_path",
    [
        "../escape.py",
        "C:/outside/escape.py",
        "references/OpenCode/file.py",
        "workspace/src/example.py",
        "src/.env",
        "src/token.txt",
        "assets/logo.png",
    ],
)
def test_unsafe_target_paths_block_before_write(tmp_path, target_path):
    operation = build_sandbox_file_write_operation(
        sandbox_root_ref=str(tmp_path),
        sandbox_path_ref=target_path,
    )
    with pytest.raises(ValueError):
        write_sandbox_file_under_policy(operation)


def test_symlink_escape_is_blocked_when_supported(tmp_path):
    outside = tmp_path / "outside"
    outside.mkdir()
    symlink_path = tmp_path / "link"
    try:
        symlink_path.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlink creation unavailable in this environment")

    operation = build_sandbox_file_write_operation(
        sandbox_root_ref=str(tmp_path),
        sandbox_path_ref="link/escape.py",
    )
    with pytest.raises(ValueError):
        write_sandbox_file_under_policy(operation)


def test_fail_closed_partial_apply_default(tmp_path):
    plan = build_sandbox_materialization_plan(
        sandbox_root_ref=str(tmp_path),
        file_plans=[
            build_sandbox_file_materialization_plan(
                sandbox_path_ref="src/example.py",
                blocked=True,
                block_reason="blocked plan should fail closed",
            )
        ],
    )
    apply_input = build_sandbox_patch_apply_input(sandbox_root_ref=str(tmp_path))
    result = run_sandbox_patch_apply(apply_input, plan)

    assert result.sandbox_apply_successful is False
    assert result.status == SandboxPatchApplyStatus.BLOCKED
    assert not (tmp_path / "src" / "example.py").exists()


def test_decision_validation_report_preview_guarantee_and_readiness():
    decision = build_sandbox_patch_apply_decision()
    apply_result = build_sandbox_patch_apply_result()
    validation = validate_sandbox_patch_apply_result(apply_result)
    report = build_sandbox_patch_apply_report(apply_result=apply_result, validation_report=validation, decision=decision)
    preview = build_sandbox_patch_apply_run_preview()
    guarantee = build_sandbox_patch_apply_no_live_write_guarantee()
    readiness = build_v0364_readiness_report()

    assert sandbox_patch_apply_decision_is_not_live_apply_permission(decision)
    assert validation.verified_no_live_write is True
    assert validation.verified_no_outside_sandbox_write is True
    assert validation.verified_no_apply_patch is True
    assert validation.verified_no_git_apply is True
    assert validation.verified_no_shell is True
    assert report.sandbox_apply_successful is True
    assert report.ready_for_execution is False
    assert preview.ready_for_sandbox_patch_apply is True
    assert preview.ready_for_execution is False
    assert guarantee.no_sandbox_write is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_") and name != "no_sandbox_write")
    assert readiness.ready_for_sandbox_patch_apply is True
    assert readiness.ready_for_execution is False
    assert v0364_readiness_report_is_not_execution_ready(readiness)

    with pytest.raises(ValueError):
        build_sandbox_patch_apply_decision(allow_git_apply=True)
    with pytest.raises(ValueError):
        build_sandbox_patch_apply_validation_report(verified_no_shell=False)
    with pytest.raises(ValueError):
        build_sandbox_patch_apply_no_live_write_guarantee(no_live_workspace_write=False)
    with pytest.raises(ValueError):
        build_v0364_readiness_report(ready_for_execution=True)


def test_module_exports_import_cleanly_from_agent_runtime():
    from chanta_core.agent_runtime import (  # noqa: PLC0415
        SandboxPatchApplyResult,
        SandboxPatchApplyPolicy,
        V0364ReadinessReport,
    )

    assert SandboxPatchApplyResult is not None
    assert SandboxPatchApplyPolicy is not None
    assert V0364ReadinessReport is not None


def test_sandbox_apply_helpers_do_not_use_external_patch_or_shell_tools():
    source = inspect.getsource(engine)

    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "git apply",
        "apply_patch(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "os.environ",
        "eval(",
        "exec(",
        "importlib",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source
