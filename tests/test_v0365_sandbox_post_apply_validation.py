from pathlib import Path

import pytest

from chanta_core.agent_runtime.patch_apply_dry_run import (
    build_dry_run_apply_input,
    build_dry_run_source_image,
    run_dry_run_apply_simulation,
)
from chanta_core.agent_runtime.patch_apply_engine import (
    SandboxFileWriteRecord,
    build_sandbox_materialization_plan_from_manifest,
    build_sandbox_patch_apply_input_from_manifest,
    run_sandbox_patch_apply,
)
from chanta_core.agent_runtime.patch_apply_sandbox import (
    build_sandbox_manifest_from_dry_run_result,
    build_sandbox_workspace_input_from_dry_run_result,
)
from chanta_core.agent_runtime.patch_apply_validation import (
    SandboxFileObservationStatus,
    SandboxPostApplyValidationMode,
    SandboxReconciliationFindingKind,
    SandboxSafetyRegressionKind,
    SandboxValidationCheckKind,
    SandboxValidationDecisionKind,
    SandboxValidationReadinessLevel,
    SandboxValidationRiskKind,
    SandboxValidationSeverity,
    SandboxValidationSourceKind,
    SandboxValidationStatus,
    V0365ReadinessReport,
    build_sandbox_actual_file_state,
    build_sandbox_applied_file_observation,
    build_sandbox_expected_file_state,
    build_sandbox_file_content_comparison,
    build_sandbox_post_apply_no_live_write_no_test_guarantee,
    build_sandbox_post_apply_validation_decision,
    build_sandbox_post_apply_validation_flags,
    build_sandbox_post_apply_validation_input,
    build_sandbox_post_apply_validation_input_from_apply_result,
    build_sandbox_post_apply_validation_policy,
    build_sandbox_post_apply_validation_report,
    build_sandbox_post_apply_validation_run_preview,
    build_sandbox_proposal_reconciliation_report,
    build_sandbox_reconciliation_finding,
    build_sandbox_safety_regression_finding,
    build_sandbox_safety_regression_report,
    build_sandbox_scope_validation_finding,
    build_sandbox_scope_validation_report,
    build_sandbox_static_validation_report,
    build_sandbox_validation_finding,
    build_sandbox_validation_source_ref,
    build_v0365_readiness_report,
    compare_expected_actual_sandbox_file_state,
    default_sandbox_post_apply_validation_policy,
    read_sandbox_file_snapshot_under_policy,
    reconcile_sandbox_apply_result,
    run_sandbox_post_apply_validation,
    sandbox_post_apply_decision_is_not_apply_permission,
    sandbox_post_apply_flags_preserve_no_write_no_test,
    sandbox_post_apply_policy_blocks_write_test,
    sandbox_reconciliation_report_is_not_repair,
    sandbox_validation_report_is_not_test_execution,
    scan_sandbox_file_static_safety,
    v0365_readiness_report_is_not_execution_ready,
    validate_sandbox_post_apply_validation_report,
    validate_sandbox_scope_after_apply,
    validate_sandbox_validation_path_containment,
)


SIMPLE_DIFF = """--- a/src/example.py
+++ b/src/example.py
@@ -1,3 +1,3 @@
 alpha
-beta
+BETA
 gamma
"""


def _sandbox_apply_fixture(tmp_path):
    dry_input = build_dry_run_apply_input()
    source_image = build_dry_run_source_image(source_text="alpha\nbeta\ngamma\n")
    dry_result = run_dry_run_apply_simulation(dry_input, SIMPLE_DIFF, [source_image])
    workspace_input = build_sandbox_workspace_input_from_dry_run_result(
        dry_result,
        requested_sandbox_root_ref=str(tmp_path),
    )
    manifest = build_sandbox_manifest_from_dry_run_result(dry_result, workspace_input=workspace_input)
    apply_input = build_sandbox_patch_apply_input_from_manifest(manifest, sandbox_root_ref=str(tmp_path))
    plan = build_sandbox_materialization_plan_from_manifest(manifest, apply_input)
    apply_result = run_sandbox_patch_apply(apply_input, plan)
    return dry_result, manifest, apply_result


def test_v0365_taxonomies_have_expected_values():
    assert [item.value for item in SandboxPostApplyValidationMode] == [
        "validate_write_records_only",
        "validate_sandbox_file_snapshots",
        "validate_expected_vs_actual_content",
        "validate_scope_and_safety",
        "full_static_reconciliation",
        "metadata_only",
        "blocked",
        "no_op",
        "unknown",
    ]
    assert "v0364_sandbox_patch_apply_result" in [item.value for item in SandboxValidationSourceKind]
    assert "validation_completed" in [item.value for item in SandboxValidationStatus]
    assert "reconciliation_report_ready" in [item.value for item in SandboxValidationReadinessLevel]
    assert "allow_future_agentic_task_input" in [item.value for item in SandboxValidationDecisionKind]
    assert "automatic_repair_risk" in [item.value for item in SandboxValidationRiskKind]
    assert "no_test_execution_check" in [item.value for item in SandboxValidationCheckKind]
    assert "observed" in [item.value for item in SandboxFileObservationStatus]
    assert "content_mismatch" in [item.value for item in SandboxReconciliationFindingKind]
    assert "dominion_runtime_introduced" in [item.value for item in SandboxSafetyRegressionKind]
    assert "blocked" in [item.value for item in SandboxValidationSeverity]


def test_flags_allow_validation_readiness_but_block_unsafe_readiness():
    flags = build_sandbox_post_apply_validation_flags()
    assert flags.sandbox_post_apply_validation_constructed is True
    assert flags.ready_for_sandbox_post_apply_validation is True
    assert flags.ready_for_sandbox_static_validation is True
    assert flags.ready_for_sandbox_reconciliation_report is True
    assert flags.ready_for_sandbox_safety_regression_scan is True
    assert flags.ready_for_sandbox_scope_validation is True
    assert flags.ready_for_future_agentic_task_operation_input is True
    assert flags.ready_for_v0366_bounded_agentic_task_operation_cycle is True
    assert flags.ready_for_v0367_patch_apply_sandbox_ocel_trace_packet is True
    assert sandbox_post_apply_flags_preserve_no_write_no_test(flags)


@pytest.mark.parametrize(
    "field",
    [
        "ready_for_execution",
        "ready_for_sandbox_repair",
        "ready_for_automatic_repair",
        "ready_for_multi_cycle_repair_loop",
        "ready_for_live_workspace_write",
        "ready_for_patch_application",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_apply_patch",
        "ready_for_git_apply",
        "ready_for_test_execution",
        "ready_for_shell_execution",
    ],
)
def test_flags_reject_unsafe_true_values(field):
    with pytest.raises(ValueError):
        build_sandbox_post_apply_validation_flags(**{field: True})


def test_policy_allows_sandbox_read_validation_but_blocks_write_apply_test_shell_repair():
    policy = default_sandbox_post_apply_validation_policy()
    assert policy.allow_sandbox_file_read is True
    assert policy.allow_write_record_validation is True
    assert policy.allow_expected_actual_comparison is True
    assert policy.allow_static_safety_scan is True
    assert policy.allow_reconciliation_report is True
    assert policy.allow_future_agentic_task_input is True
    assert sandbox_post_apply_policy_blocks_write_test(policy)


@pytest.mark.parametrize(
    "field",
    [
        "allow_sandbox_file_write",
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
        "allow_automatic_repair",
        "allow_multi_cycle_repair_loop",
    ],
)
def test_policy_rejects_unsafe_permissions(field):
    with pytest.raises(ValueError):
        build_sandbox_post_apply_validation_policy(**{field: True})


def test_source_ref_and_input_are_validation_metadata_not_apply_request():
    source_ref = build_sandbox_validation_source_ref(
        source_kind=SandboxValidationSourceKind.V0364_SANDBOX_PATCH_APPLY_RESULT,
        source_id="apply-result-1",
    )
    validation_input = build_sandbox_post_apply_validation_input(
        sandbox_apply_result_id="apply-result-1",
        sandbox_root_ref="sandbox-root",
        source_refs=[source_ref],
    )
    assert validation_input.requested_mode == SandboxPostApplyValidationMode.FULL_STATIC_RECONCILIATION
    assert "repair_loop" in validation_input.prohibited_runtime_actions
    assert source_ref.source_kind == SandboxValidationSourceKind.V0364_SANDBOX_PATCH_APPLY_RESULT


def test_expected_actual_state_and_observation_are_no_write_no_apply_metadata():
    expected = build_sandbox_expected_file_state(target_path_ref="src/example.py", expected_content="alpha\n")
    actual = build_sandbox_actual_file_state(sandbox_path_ref="src/example.py", actual_content="alpha\n")
    observation = build_sandbox_applied_file_observation(expected_state=expected, actual_state=actual)
    assert expected.expected_content_hash == actual.actual_content_hash
    assert actual.file_exists is True
    assert observation.ready_for_write is False
    assert observation.ready_for_apply is False


def test_content_comparison_detects_match_and_mismatch():
    expected = build_sandbox_expected_file_state(target_path_ref="src/example.py", expected_content="alpha\n")
    matching_actual = build_sandbox_actual_file_state(sandbox_path_ref="src/example.py", actual_content="alpha\n")
    mismatch_actual = build_sandbox_actual_file_state(sandbox_path_ref="src/example.py", actual_content="beta\n")
    match = compare_expected_actual_sandbox_file_state(expected, matching_actual)
    mismatch = compare_expected_actual_sandbox_file_state(expected, mismatch_actual)
    assert match.matches_expected is True
    assert mismatch.matches_expected is False
    assert mismatch.finding_kind == SandboxReconciliationFindingKind.CONTENT_MISMATCH


def test_tmp_path_sandbox_file_read_validation_works(tmp_path):
    _dry, _manifest, apply_result = _sandbox_apply_fixture(tmp_path)
    actual = read_sandbox_file_snapshot_under_policy(str(tmp_path), "src/example.py")
    assert actual.file_exists is True
    assert actual.actual_content_hash is not None
    assert actual.bytes_read > 0
    assert apply_result.sandbox_apply_successful is True


@pytest.mark.parametrize("bad_path", ["../escape.py", "C:/escape.py", "references/OpenCode/x.py", "workspace/live.py"])
def test_sandbox_read_path_containment_blocks_unsafe_paths(tmp_path, bad_path):
    with pytest.raises(ValueError):
        validate_sandbox_validation_path_containment(str(tmp_path), bad_path)
    with pytest.raises(ValueError):
        read_sandbox_file_snapshot_under_policy(str(tmp_path), bad_path)


def test_symlink_escape_read_is_blocked_when_symlink_available(tmp_path):
    outside = tmp_path.parent / "outside_sandbox_validation.txt"
    outside.write_text("outside", encoding="utf-8")
    link = tmp_path / "src" / "linked.txt"
    link.parent.mkdir(parents=True, exist_ok=True)
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("symlink creation unavailable on this platform")
    with pytest.raises(ValueError):
        read_sandbox_file_snapshot_under_policy(str(tmp_path), "src/linked.txt")


def test_reconciliation_detects_missing_expected_file_and_unexpected_write_record(tmp_path):
    _dry, _manifest, apply_result = _sandbox_apply_fixture(tmp_path)
    missing_expected = build_sandbox_expected_file_state(
        expected_state_id="expected-missing",
        target_path_ref="src/missing.py",
        expected_content="missing\n",
    )
    unexpected_record = SandboxFileWriteRecord(
        write_record_id="unexpected-record",
        write_operation_id="unexpected-op",
        sandbox_root_ref=str(tmp_path),
        sandbox_path_ref="src/unexpected.py",
        write_status="written",
        bytes_written=1,
        write_summary="synthetic unexpected sandbox-only write record",
    )
    altered_result = build_sandbox_post_apply_validation_input_from_apply_result(apply_result)
    assert altered_result.sandbox_apply_result_id == apply_result.sandbox_apply_result_id
    result_with_unexpected = apply_result.__class__(
        **{**apply_result.__dict__, "write_records": [*apply_result.write_records, unexpected_record]}
    )
    report = reconcile_sandbox_apply_result(result_with_unexpected, expected_states=[missing_expected], actual_states=[])
    kinds = {finding.finding_kind for finding in report.findings}
    assert SandboxReconciliationFindingKind.MISSING_EXPECTED_FILE in kinds
    assert SandboxReconciliationFindingKind.UNEXPECTED_WRITE_RECORD in kinds
    assert sandbox_reconciliation_report_is_not_repair(report)


def test_static_safety_scan_detects_unsafe_patterns_as_metadata():
    content = "\n".join(
        [
            "ready_for_execution=True",
            "subprocess",
            "pytest",
            "pip install package",
            "import requests",
            "os.environ",
            "SECRET",
            "Claude Code",
            "dominion_runtime",
        ]
    )
    actual = build_sandbox_actual_file_state(sandbox_path_ref="src/example.py", actual_content=content, metadata={"full_text": content})
    report = scan_sandbox_file_static_safety(actual)
    regression_kinds = {finding.regression_kind for finding in report.findings}
    assert SandboxSafetyRegressionKind.UNSAFE_READINESS_FLAG_INTRODUCED in regression_kinds
    assert SandboxSafetyRegressionKind.SUBPROCESS_OR_COMMAND_EXECUTION_INTRODUCED in regression_kinds
    assert SandboxSafetyRegressionKind.TEST_EXECUTION_INTRODUCED in regression_kinds
    assert SandboxSafetyRegressionKind.DEPENDENCY_INSTALL_INTRODUCED in regression_kinds
    assert SandboxSafetyRegressionKind.PROVIDER_NETWORK_BOUNDARY_OPENED in regression_kinds
    assert SandboxSafetyRegressionKind.CREDENTIAL_BOUNDARY_OPENED in regression_kinds
    assert SandboxSafetyRegressionKind.EXTERNAL_AGENT_INVOCATION_INTRODUCED in regression_kinds
    assert SandboxSafetyRegressionKind.DOMINION_RUNTIME_INTRODUCED in regression_kinds


def test_scope_validation_confirms_no_outside_live_reference_paths(tmp_path):
    _dry, _manifest, apply_result = _sandbox_apply_fixture(tmp_path)
    report = validate_sandbox_scope_after_apply(apply_result)
    assert report.scope_valid is True
    assert report.no_outside_sandbox_paths is True
    assert report.no_live_workspace_paths is True
    assert report.no_reference_paths is True


def test_run_post_apply_validation_successful_but_not_test_or_production(tmp_path):
    _dry, _manifest, apply_result = _sandbox_apply_fixture(tmp_path)
    validation_input = build_sandbox_post_apply_validation_input_from_apply_result(apply_result)
    report = run_sandbox_post_apply_validation(validation_input, apply_result)
    assert report.validation_successful is True
    assert report.ready_for_future_agentic_task_operation_input is True
    assert report.production_certified is False
    assert report.test_execution_performed is False
    assert report.ready_for_execution is False
    assert sandbox_validation_report_is_not_test_execution(report)


def test_report_builders_and_decision_preserve_no_repair_write_apply_test_shell():
    validation_finding = build_sandbox_validation_finding()
    scope_finding = build_sandbox_scope_validation_finding()
    safety_finding = build_sandbox_safety_regression_finding()
    reconciliation_finding = build_sandbox_reconciliation_finding()
    reconciliation_report = build_sandbox_proposal_reconciliation_report(findings=[reconciliation_finding], matches_expected=False)
    static_report = build_sandbox_static_validation_report(findings=[validation_finding])
    safety_report = build_sandbox_safety_regression_report(findings=[safety_finding])
    scope_report = build_sandbox_scope_validation_report(findings=[scope_finding])
    decision = build_sandbox_post_apply_validation_decision(allow_future_agentic_task_input=False)
    report = build_sandbox_post_apply_validation_report(
        reconciliation_report=reconciliation_report,
        static_validation_report=static_report,
        safety_regression_report=safety_report,
        scope_validation_report=scope_report,
        decision=decision,
        validation_successful=False,
    )
    assert sandbox_post_apply_decision_is_not_apply_permission(decision)
    assert sandbox_validation_report_is_not_test_execution(report)
    assert validate_sandbox_post_apply_validation_report(report).static_validation_successful is True


def test_guarantee_and_readiness_keep_unsafe_flags_false():
    guarantee = build_sandbox_post_apply_no_live_write_no_test_guarantee()
    preview = build_sandbox_post_apply_validation_run_preview()
    readiness = build_v0365_readiness_report()
    assert guarantee.no_sandbox_write is True
    assert guarantee.no_test_execution is True
    assert preview.ready_for_sandbox_post_apply_validation is True
    assert isinstance(readiness, V0365ReadinessReport)
    assert readiness.ready_for_sandbox_repair is False
    assert readiness.ready_for_automatic_repair is False
    assert readiness.ready_for_multi_cycle_repair_loop is False
    assert v0365_readiness_report_is_not_execution_ready(readiness)


@pytest.mark.parametrize(
    "field",
    [
        "allow_repair",
        "allow_write",
        "allow_apply",
        "allow_test_execution",
        "allow_shell",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ],
)
def test_decision_rejects_unsafe_permissions(field):
    with pytest.raises(ValueError):
        build_sandbox_post_apply_validation_decision(**{field: True})


def test_validation_module_has_no_write_apply_shell_runtime_calls():
    source = Path("src/chanta_core/agent_runtime/patch_apply_validation.py").read_text(encoding="utf-8")
    assert ".write_text(" not in source
    assert ".write_bytes(" not in source
    assert "target_path.open(\"w\"" not in source
    assert "subprocess.run" not in source
    assert "os.system" not in source
    assert "shell=True" not in source
    assert "git apply" not in source
    assert "apply_patch(" not in source
    assert "pytest.main" not in source
