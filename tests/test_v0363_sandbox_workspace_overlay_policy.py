import inspect

import pytest

from chanta_core.agent_runtime import (
    OverlayMaterializationMode,
    OverlayWriteMode,
    SandboxEscapeKind,
    SandboxPathDecisionKind,
    SandboxPathRole,
    SandboxPathStatus,
    SandboxWorkspaceDecisionKind,
    SandboxWorkspaceMode,
    SandboxWorkspaceReadinessLevel,
    SandboxWorkspaceRiskKind,
    SandboxWorkspaceSourceKind,
    SandboxWorkspaceStatus,
    build_dry_run_apply_input,
    build_dry_run_apply_simulation_result,
    build_dry_run_conflict,
    build_dry_run_source_image,
    build_sandbox_file_map_entry,
    build_sandbox_live_write_block,
    build_sandbox_manifest_from_dry_run_result,
    build_sandbox_overlay_entry,
    build_sandbox_overlay_policy,
    build_sandbox_path_ref,
    build_sandbox_root_policy,
    build_sandbox_workspace_flags,
    build_sandbox_workspace_gate_decision,
    build_sandbox_workspace_input,
    build_sandbox_workspace_input_from_dry_run_result,
    build_sandbox_workspace_manifest,
    build_sandbox_workspace_no_live_write_guarantee,
    build_sandbox_workspace_plan,
    build_sandbox_workspace_policy,
    build_sandbox_workspace_report,
    build_sandbox_workspace_run_preview,
    build_sandbox_workspace_source_ref,
    build_sandbox_workspace_validation_report,
    build_v0363_readiness_report,
    classify_sandbox_path_ref,
    default_sandbox_workspace_policy,
    normalize_sandbox_relative_path_ref,
    run_dry_run_apply_simulation,
    sandbox_live_write_block_blocks_live_write,
    sandbox_overlay_policy_blocks_materialization,
    sandbox_root_policy_blocks_live_write,
    sandbox_workspace_flags_preserve_no_write,
    sandbox_workspace_manifest_is_not_materialized,
    v0363_readiness_report_is_not_execution_ready,
    validate_sandbox_workspace_manifest,
)
import chanta_core.agent_runtime.patch_apply_sandbox as sandbox


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


def successful_dry_run_result():
    dry_input = build_dry_run_apply_input()
    source_image = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\n")
    return run_dry_run_apply_simulation(dry_input, SIMPLE_DIFF, [source_image])


def test_taxonomies_are_complete():
    assert values(SandboxWorkspaceMode) == {
        "manifest_only",
        "overlay_policy_only",
        "in_memory_overlay_plan",
        "future_materialization_input",
        "blocked",
        "no_op",
        "unknown",
    }
    assert values(SandboxWorkspaceSourceKind) == {
        "v0362_dry_run_apply_simulation_result",
        "v0362_simulated_file_result",
        "v0362_simulated_file_delta",
        "v0361_apply_candidate_envelope",
        "v0361_human_approval_contract",
        "v0360_patch_apply_sandbox_boundary",
        "v0354_diff_proposal_envelope",
        "manual_operator_input",
        "test_fixture",
        "unknown",
    }
    assert values(SandboxWorkspaceStatus) == {
        "unknown",
        "draft",
        "policy_created",
        "manifest_created",
        "manifest_validated",
        "manifest_validated_with_gaps",
        "future_materialization_ready",
        "blocked",
        "review_required",
        "future_gated",
        "no_op",
        "safe_failed",
    }
    assert values(SandboxWorkspaceReadinessLevel) == {
        "not_ready",
        "sandbox_policy_ready",
        "overlay_policy_ready",
        "manifest_ready",
        "file_map_ready",
        "live_write_block_ready",
        "design_handoff_ready_for_v0364",
        "design_handoff_ready_for_v0365",
        "blocked",
        "future_track",
    }
    assert values(SandboxWorkspaceDecisionKind) == {
        "allow_manifest_metadata",
        "allow_overlay_policy_metadata",
        "allow_file_map_metadata",
        "allow_future_materialization_input",
        "deny",
        "block",
        "no_op",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert values(SandboxWorkspaceRiskKind) == {
        "live_workspace_write_risk",
        "sandbox_workspace_write_confusion_risk",
        "sandbox_escape_risk",
        "symlink_escape_risk",
        "outside_root_write_risk",
        "path_traversal_risk",
        "absolute_path_risk",
        "reference_root_write_risk",
        "secret_path_risk",
        "credential_path_risk",
        "binary_target_risk",
        "blocked_target_risk",
        "unresolved_dry_run_conflict_risk",
        "patch_apply_confusion_risk",
        "shell_execution_risk",
        "external_agent_execution_risk",
        "dominion_runtime_risk",
        "unknown",
    }
    assert values(SandboxPathRole) == {
        "sandbox_root",
        "sandbox_manifest_path",
        "sandbox_overlay_root",
        "virtual_target_file",
        "virtual_source_file",
        "future_materialization_target",
        "live_workspace_root",
        "reference_root",
        "blocked_secret_path",
        "blocked_credential_path",
        "blocked_binary_path",
        "external_path",
        "unknown",
    }
    assert values(SandboxPathStatus) == {
        "unknown",
        "valid_metadata_path",
        "valid_future_materialization_path",
        "blocked",
        "outside_root",
        "traversal_detected",
        "absolute_path_blocked",
        "symlink_risk",
        "secret_blocked",
        "credential_blocked",
        "binary_blocked",
        "reference_root_blocked",
        "external_blocked",
        "no_op",
    }
    assert values(SandboxPathDecisionKind) == {
        "allow_path_metadata",
        "allow_future_materialization_path",
        "block_path",
        "block_live_workspace",
        "block_reference_root",
        "block_secret",
        "block_credential",
        "block_binary",
        "require_review",
        "future_gate_required",
        "unknown",
    }
    assert values(SandboxEscapeKind) == {
        "no_escape_detected",
        "path_traversal",
        "absolute_path",
        "symlink_escape_risk",
        "outside_sandbox_root",
        "live_workspace_target",
        "reference_root_target",
        "external_root_target",
        "unknown",
    }
    assert values(OverlayWriteMode) == {
        "no_write",
        "virtual_overlay_metadata",
        "future_overlay_materialization",
        "future_sandbox_write",
        "live_write_blocked",
        "unknown",
    }
    assert values(OverlayMaterializationMode) == {
        "not_materialized",
        "metadata_only",
        "future_sandbox_materialization",
        "blocked",
        "unknown",
    }


def test_flags_allow_policy_metadata_but_preserve_no_write():
    flags = build_sandbox_workspace_flags()

    assert flags.sandbox_workspace_policy_constructed is True
    assert flags.sandbox_root_policy_defined is True
    assert flags.overlay_policy_defined is True
    assert flags.sandbox_manifest_available is True
    assert flags.sandbox_file_map_available is True
    assert flags.live_workspace_write_block_available is True
    assert flags.ready_for_v0364_sandbox_patch_apply_engine is True
    assert flags.ready_for_v0365_sandbox_post_apply_validation is True
    assert flags.ready_for_future_sandbox_materialization_input is True
    assert sandbox_workspace_flags_preserve_no_write(flags)


@pytest.mark.parametrize(
    "flag_name",
    [
        "ready_for_execution",
        "ready_for_sandbox_workspace_materialization",
        "ready_for_sandbox_workspace_write",
        "ready_for_sandbox_patch_apply",
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
def test_flags_reject_unsafe_readiness(flag_name):
    with pytest.raises(ValueError):
        build_sandbox_workspace_flags(**{flag_name: True})


def test_source_ref_policies_and_input_are_metadata_only():
    source_ref = build_sandbox_workspace_source_ref()
    root_policy = build_sandbox_root_policy()
    overlay_policy = build_sandbox_overlay_policy()
    workspace_policy = default_sandbox_workspace_policy(root_policy=root_policy, overlay_policy=overlay_policy)
    workspace_input = build_sandbox_workspace_input()

    assert source_ref.source_kind == SandboxWorkspaceSourceKind.V0362_DRY_RUN_APPLY_SIMULATION_RESULT
    assert sandbox_root_policy_blocks_live_write(root_policy)
    assert root_policy.allow_directory_creation is False
    assert root_policy.allow_file_write is False
    assert root_policy.allow_live_workspace_write is False
    assert overlay_policy.allow_virtual_overlay_metadata is True
    assert overlay_policy.allow_future_materialization_input is True
    assert sandbox_overlay_policy_blocks_materialization(overlay_policy)
    assert workspace_policy.allow_manifest_metadata is True
    assert workspace_policy.allow_file_map_metadata is True
    assert workspace_policy.allow_directory_creation is False
    assert workspace_policy.allow_sandbox_file_write is False
    assert workspace_policy.allow_live_workspace_write is False
    assert workspace_policy.allow_patch_application is False
    assert "directory_creation" in workspace_input.prohibited_runtime_actions
    assert "file_write" in workspace_input.prohibited_runtime_actions
    assert "sandbox_apply" in workspace_input.prohibited_runtime_actions


@pytest.mark.parametrize(
    ("builder", "unsafe_name"),
    [
        (build_sandbox_root_policy, "allow_directory_creation"),
        (build_sandbox_root_policy, "allow_file_write"),
        (build_sandbox_root_policy, "allow_live_workspace_write"),
        (build_sandbox_overlay_policy, "allow_sandbox_materialization"),
        (build_sandbox_overlay_policy, "allow_sandbox_file_write"),
        (build_sandbox_overlay_policy, "allow_live_file_write"),
        (build_sandbox_overlay_policy, "allow_patch_apply"),
        (build_sandbox_overlay_policy, "allow_apply_patch"),
        (build_sandbox_overlay_policy, "allow_git_apply"),
        (build_sandbox_workspace_policy, "allow_directory_creation"),
        (build_sandbox_workspace_policy, "allow_sandbox_file_write"),
        (build_sandbox_workspace_policy, "allow_live_workspace_write"),
        (build_sandbox_workspace_policy, "allow_patch_application"),
    ],
)
def test_policies_reject_unsafe_allow_flags(builder, unsafe_name):
    with pytest.raises(ValueError):
        builder(**{unsafe_name: True})


def test_path_normalization_and_classification_blocks_unsafe_paths():
    assert normalize_sandbox_relative_path_ref("src\\example.py") == "src/example.py"
    assert normalize_sandbox_relative_path_ref("./src/example.py") == "src/example.py"

    with pytest.raises(ValueError):
        normalize_sandbox_relative_path_ref("/abs/example.py")
    with pytest.raises(ValueError):
        normalize_sandbox_relative_path_ref("../example.py")

    safe_path = classify_sandbox_path_ref("src/example.py")
    absolute_path = classify_sandbox_path_ref("C:/workspace/example.py")
    traversal_path = classify_sandbox_path_ref("../workspace/example.py")
    reference_path = classify_sandbox_path_ref("references/OpenCode/file.py")
    live_path = classify_sandbox_path_ref("workspace/src/example.py")
    secret_path = classify_sandbox_path_ref("src/.env")
    credential_path = classify_sandbox_path_ref("src/token.txt")
    binary_path = classify_sandbox_path_ref("assets/logo.png")

    assert safe_path.blocked is False
    assert safe_path.path_status == SandboxPathStatus.VALID_FUTURE_MATERIALIZATION_PATH
    assert absolute_path.path_status == SandboxPathStatus.ABSOLUTE_PATH_BLOCKED
    assert traversal_path.path_status == SandboxPathStatus.TRAVERSAL_DETECTED
    assert reference_path.path_status == SandboxPathStatus.REFERENCE_ROOT_BLOCKED
    assert live_path.decision_kind == SandboxPathDecisionKind.BLOCK_LIVE_WORKSPACE
    assert secret_path.path_role == SandboxPathRole.BLOCKED_SECRET_PATH
    assert credential_path.path_role == SandboxPathRole.BLOCKED_CREDENTIAL_PATH
    assert binary_path.path_status == SandboxPathStatus.BINARY_BLOCKED
    assert all(path.blocked for path in [absolute_path, traversal_path, reference_path, live_path, secret_path, credential_path, binary_path])

    with pytest.raises(ValueError):
        build_sandbox_path_ref(path_status=SandboxPathStatus.ABSOLUTE_PATH_BLOCKED, blocked=False)


def test_file_map_overlay_manifest_plan_and_live_block_are_not_materialized():
    file_map = build_sandbox_file_map_entry()
    overlay = build_sandbox_overlay_entry()
    manifest = build_sandbox_workspace_manifest()
    plan = build_sandbox_workspace_plan()
    live_block = build_sandbox_live_write_block()

    assert file_map.eligible_for_future_materialization is True
    assert file_map.ready_for_write is False
    assert file_map.ready_for_apply is False
    assert overlay.materialized is False
    assert overlay.ready_for_write is False
    assert overlay.ready_for_apply is False
    assert manifest.materialized is False
    assert manifest.ready_for_future_materialization_input is True
    assert manifest.ready_for_sandbox_workspace_materialization is False
    assert manifest.ready_for_sandbox_workspace_write is False
    assert manifest.ready_for_sandbox_patch_apply is False
    assert sandbox_workspace_manifest_is_not_materialized(manifest)
    assert plan.ready_for_v0364_sandbox_patch_apply_engine is True
    assert plan.ready_for_sandbox_workspace_materialization is False
    assert plan.ready_for_sandbox_patch_apply is False
    assert sandbox_live_write_block_blocks_live_write(live_block)

    with pytest.raises(ValueError):
        build_sandbox_file_map_entry(ready_for_write=True)
    with pytest.raises(ValueError):
        build_sandbox_overlay_entry(materialized=True)
    with pytest.raises(ValueError):
        build_sandbox_workspace_manifest(materialized=True)
    with pytest.raises(ValueError):
        build_sandbox_live_write_block(live_workspace_write_allowed=True)


def test_manifest_from_successful_dry_run_consumes_metadata_only():
    result = successful_dry_run_result()
    workspace_input = build_sandbox_workspace_input_from_dry_run_result(result)
    manifest = build_sandbox_manifest_from_dry_run_result(result, workspace_input=workspace_input)
    validation = validate_sandbox_workspace_manifest(manifest)

    assert workspace_input.dry_run_result_id == result.simulation_result_id
    assert manifest.metadata["dry_run_result_id"] == result.simulation_result_id
    assert manifest.file_map_entries[0].target_path_ref == "src/example.py"
    assert manifest.overlay_entries[0].simulated_after_preview == "alpha\nBETA\ngamma"
    assert manifest.ready_for_future_materialization_input is True
    assert manifest.ready_for_sandbox_workspace_materialization is False
    assert manifest.ready_for_sandbox_patch_apply is False
    assert validation.ready_for_future_materialization_input is True
    assert validation.certifies_filesystem_mutation is False


def test_blocked_dry_run_conflict_blocks_future_materialization():
    conflict = build_dry_run_conflict()
    result = build_dry_run_apply_simulation_result(
        simulation_successful=False,
        eligible_for_future_sandbox_workspace_input=False,
        ready_for_v0363_sandbox_workspace_overlay_policy=False,
        ready_for_v0364_sandbox_patch_apply_engine=False,
        conflicts=[conflict],
        conflict_count=1,
        blocking_conflict_count=1,
        file_results=[],
    )
    manifest = build_sandbox_manifest_from_dry_run_result(result)
    validation = validate_sandbox_workspace_manifest(manifest)

    assert manifest.ready_for_future_materialization_input is False
    assert validation.ready_for_future_materialization_input is False
    assert validation.findings[0].risk_kind == SandboxWorkspaceRiskKind.UNRESOLVED_DRY_RUN_CONFLICT_RISK


def test_blocked_path_blocks_future_materialization():
    result = successful_dry_run_result()
    delta = result.file_results[0].simulated_deltas[0]
    blocked_delta = type(delta)(
        simulated_delta_id=delta.simulated_delta_id,
        target_path_ref="references/OpenCode/file.py",
        delta_kind=delta.delta_kind,
        hunk_alignment_ids=delta.hunk_alignment_ids,
        conflict_ids=delta.conflict_ids,
        before_preview=delta.before_preview,
        after_preview=delta.after_preview,
        delta_summary=delta.delta_summary,
        changed=delta.changed,
        redacted=delta.redacted,
        truncated=delta.truncated,
    )
    blocked_result = build_dry_run_apply_simulation_result(
        file_results=[
            type(result.file_results[0])(
                file_result_id=result.file_results[0].file_result_id,
                target_path_ref="references/OpenCode/file.py",
                source_image_id=result.file_results[0].source_image_id,
                target_file_image=result.file_results[0].target_file_image,
                simulated_deltas=[blocked_delta],
                conflicts=[],
                file_result_summary=result.file_results[0].file_result_summary,
                simulation_successful=True,
                ready_for_future_sandbox_workspace_input=True,
            )
        ],
        simulation_successful=True,
        eligible_for_future_sandbox_workspace_input=True,
    )
    manifest = build_sandbox_manifest_from_dry_run_result(blocked_result)
    validation = validate_sandbox_workspace_manifest(manifest)

    assert manifest.blocked_path_count == 1
    assert manifest.ready_for_future_materialization_input is False
    assert validation.findings[0].risk_kind == SandboxWorkspaceRiskKind.REFERENCE_ROOT_WRITE_RISK


def test_decision_report_preview_guarantee_and_readiness_preserve_no_write():
    manifest = build_sandbox_workspace_manifest()
    validation = build_sandbox_workspace_validation_report(manifest_id=manifest.manifest_id)
    decision = build_sandbox_workspace_gate_decision()
    report = build_sandbox_workspace_report(manifest=manifest, validation_report=validation, gate_decision=decision)
    preview = build_sandbox_workspace_run_preview()
    guarantee = build_sandbox_workspace_no_live_write_guarantee()
    readiness = build_v0363_readiness_report()

    assert decision.allow_directory_creation is False
    assert decision.allow_sandbox_workspace_write is False
    assert decision.allow_sandbox_patch_apply is False
    assert report.manifest_ready is True
    assert report.ready_for_execution is False
    assert preview.ready_for_execution is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert readiness.ready_for_sandbox_workspace_policy is True
    assert readiness.ready_for_future_sandbox_materialization_input is True
    assert v0363_readiness_report_is_not_execution_ready(readiness)

    with pytest.raises(ValueError):
        build_sandbox_workspace_gate_decision(allow_patch_application=True)
    with pytest.raises(ValueError):
        build_sandbox_workspace_validation_report(certifies_filesystem_mutation=True)
    with pytest.raises(ValueError):
        build_sandbox_workspace_no_live_write_guarantee(no_sandbox_file_write=False)
    with pytest.raises(ValueError):
        build_v0363_readiness_report(ready_for_execution=True)


def test_module_exports_import_cleanly_from_agent_runtime():
    from chanta_core.agent_runtime import (  # noqa: PLC0415
        SandboxWorkspaceManifest,
        SandboxWorkspacePolicy,
        V0363ReadinessReport,
    )

    assert SandboxWorkspaceManifest is not None
    assert SandboxWorkspacePolicy is not None
    assert V0363ReadinessReport is not None


def test_sandbox_helpers_do_not_contain_runtime_execution_or_file_write_patterns():
    source = inspect.getsource(sandbox)

    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.mkdir",
        ".mkdir(",
        "makedirs",
        "Path.write_text",
        "Path.write_bytes",
        ".write_text(",
        ".write_bytes(",
        ".unlink(",
        ".rename(",
        ".chmod(",
        ".chown(",
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
