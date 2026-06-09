from dataclasses import fields
import inspect
import sys

import pytest

import chanta_core.agent_runtime.sandbox_test_execution as execution_module
from chanta_core.agent_runtime import (
    ControlledTestCommandLine,
    ControlledTestCwdValidation,
    ControlledTestEnvironment,
    ControlledTestSubprocessInvocation,
    ControlledTestSubprocessKind,
    ControlledTestSubprocessPolicy,
    ControlledTestSubprocessResult,
    ControlledTestSubprocessStatus,
    SandboxTestEnvironmentStatus,
    SandboxTestCommandKind,
    SandboxTestExecutionDecision,
    SandboxTestExecutionDecisionKind,
    SandboxTestExecutionFlagSet,
    SandboxTestExecutionInput,
    SandboxTestExecutionMode,
    SandboxTestExecutionNoUnsafeCommandGuarantee,
    SandboxTestExecutionPolicy,
    SandboxTestExecutionReadinessLevel,
    SandboxTestExecutionReport,
    SandboxTestExecutionResult,
    SandboxTestExecutionRiskKind,
    SandboxTestExecutionRunPreview,
    SandboxTestExecutionSourceKind,
    SandboxTestExecutionSourceRef,
    SandboxTestExecutionStatus,
    SandboxTestExecutionValidationFinding,
    SandboxTestExecutionValidationReport,
    SandboxTestNetworkIsolationStatus,
    SandboxTestOutputCapture,
    SandboxTestOutputCaptureStatus,
    SandboxTestOutputStreamKind,
    SandboxTestProcessExitKind,
    SandboxTestTimeoutStatus,
    build_controlled_test_command_line,
    build_controlled_test_command_line_from_contract,
    build_controlled_test_environment,
    build_controlled_test_subprocess_invocation,
    build_controlled_test_subprocess_policy,
    build_controlled_test_subprocess_result,
    build_minimal_test_environment,
    build_sandbox_test_allowed_executable,
    build_sandbox_test_command_spec,
    build_sandbox_test_execution_decision,
    build_sandbox_test_execution_flags,
    build_sandbox_test_execution_input,
    build_sandbox_test_execution_input_from_invocation_contract,
    build_sandbox_test_execution_no_unsafe_command_guarantee,
    build_sandbox_test_execution_policy,
    build_sandbox_test_execution_report,
    build_sandbox_test_execution_result,
    build_sandbox_test_execution_run_preview,
    build_sandbox_test_execution_source_ref,
    build_sandbox_test_execution_validation_finding,
    build_sandbox_test_execution_validation_report,
    build_sandbox_test_invocation_contract,
    build_sandbox_test_output_capture,
    build_v0372_readiness_report,
    bound_and_redact_test_output,
    controlled_test_subprocess_invocation_is_shell_false,
    default_controlled_test_subprocess_policy,
    default_sandbox_test_execution_policy,
    run_controlled_sandbox_test_subprocess,
    run_sandbox_test_execution_engine,
    sandbox_test_execution_flags_preserve_no_unsafe_execution,
    sandbox_test_execution_policy_blocks_arbitrary_shell,
    sandbox_test_execution_result_is_not_production_certification,
    v0372_readiness_report_is_not_general_execution_ready,
    validate_controlled_test_cwd,
    validate_controlled_test_subprocess_invocation,
    validate_sandbox_test_execution_result,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0373_test_result_envelope",
    "ready_for_v0374_test_feedback_failure_diagnosis",
    "ready_for_v0376_vera_codex_one_shot_agent_trial",
    "ready_for_sandbox_test_execution_engine",
    "ready_for_controlled_test_subprocess",
    "ready_for_allowlisted_test_execution",
    "ready_for_pytest_module_execution",
    "ready_for_unittest_module_execution",
    "ready_for_bounded_test_output_capture",
    "ready_for_test_timeout_enforcement",
    "ready_for_minimal_test_environment",
    "ready_for_future_test_result_envelope_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES
    ]


def test_v0372_taxonomies_have_required_values():
    assert {item.value for item in SandboxTestExecutionMode} == {
        "allowlisted_python_module_execution",
        "allowlisted_pytest_execution",
        "allowlisted_unittest_execution",
        "metadata_only",
        "blocked",
        "no_op",
        "unknown",
    }
    assert "v0371_test_invocation_contract" in {item.value for item in SandboxTestExecutionSourceKind}
    assert "execution_completed_with_nonzero_exit" in {item.value for item in SandboxTestExecutionStatus}
    assert "controlled_subprocess_ready" in {item.value for item in SandboxTestExecutionReadinessLevel}
    assert "allow_controlled_sandbox_test_execution" in {item.value for item in SandboxTestExecutionDecisionKind}
    assert "network_hard_isolation_uncertified_risk" in {item.value for item in SandboxTestExecutionRiskKind}
    assert "python_pytest_module_subprocess" in {item.value for item in ControlledTestSubprocessKind}
    assert "completed_nonzero" in {item.value for item in ControlledTestSubprocessStatus}
    assert "exit_zero" in {item.value for item in SandboxTestProcessExitKind}
    assert "stderr" in {item.value for item in SandboxTestOutputStreamKind}
    assert "captured_truncated" in {item.value for item in SandboxTestOutputCaptureStatus}
    assert "timeout_configured" in {item.value for item in SandboxTestTimeoutStatus}
    assert "minimal_env_prepared" in {item.value for item in SandboxTestEnvironmentStatus}
    assert "network_hard_isolation_not_certified" in {item.value for item in SandboxTestNetworkIsolationStatus}


def test_required_models_are_exported():
    for model in (
        SandboxTestExecutionFlagSet,
        SandboxTestExecutionSourceRef,
        SandboxTestExecutionPolicy,
        ControlledTestSubprocessPolicy,
        SandboxTestExecutionInput,
        ControlledTestCommandLine,
        ControlledTestEnvironment,
        ControlledTestCwdValidation,
        ControlledTestSubprocessInvocation,
        ControlledTestSubprocessResult,
        SandboxTestOutputCapture,
        SandboxTestExecutionResult,
        SandboxTestExecutionDecision,
        SandboxTestExecutionValidationFinding,
        SandboxTestExecutionValidationReport,
        SandboxTestExecutionReport,
        SandboxTestExecutionRunPreview,
        SandboxTestExecutionNoUnsafeCommandGuarantee,
    ):
        assert model is not None


def test_flags_allow_controlled_readiness_and_preserve_unsafe_false():
    flags = build_sandbox_test_execution_flags()
    assert flags.sandbox_test_execution_engine_constructed
    assert flags.controlled_subprocess_runner_available
    assert flags.allowlisted_test_execution_available
    assert flags.bounded_output_capture_available
    assert flags.timeout_enforcement_available
    assert flags.minimal_environment_available
    assert flags.ready_for_v0373_test_result_envelope
    assert flags.ready_for_v0374_test_feedback_failure_diagnosis
    assert flags.ready_for_v0376_vera_codex_one_shot_agent_trial
    assert flags.ready_for_sandbox_test_execution_engine
    assert flags.ready_for_controlled_test_subprocess
    assert flags.ready_for_allowlisted_test_execution
    assert flags.ready_for_pytest_module_execution
    assert flags.ready_for_unittest_module_execution
    assert flags.ready_for_bounded_test_output_capture
    assert flags.ready_for_test_timeout_enforcement
    assert flags.ready_for_minimal_test_environment
    assert flags.ready_for_future_test_result_envelope_input
    assert sandbox_test_execution_flags_preserve_no_unsafe_execution(flags)
    for name in _unsafe_flag_names(SandboxTestExecutionFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(SandboxTestExecutionFlagSet) + ["production_certified"])
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_sandbox_test_execution_flags(**{field_name: True})


def test_policies_allow_only_controlled_sandbox_execution():
    policy = default_sandbox_test_execution_policy()
    subprocess_policy = default_controlled_test_subprocess_policy()
    assert policy.allow_controlled_subprocess
    assert policy.allow_allowlisted_test_execution
    assert policy.allow_pytest_module_execution
    assert policy.allow_unittest_module_execution
    assert sandbox_test_execution_policy_blocks_arbitrary_shell(policy)
    for name in (
        "allow_arbitrary_shell",
        "allow_uncontrolled_subprocess",
        "allow_shell",
        "allow_command_execution",
        "allow_dependency_install",
        "allow_network_access",
        "allow_live_workspace_write",
        "allow_patch_application",
        "allow_automatic_repair",
        "allow_external_agent_execution",
        "allow_dominion_runtime",
    ):
        assert getattr(policy, name) is False
        with pytest.raises(ValueError):
            build_sandbox_test_execution_policy(**{name: True})
    assert subprocess_policy.allow_subprocess_run
    assert subprocess_policy.require_structured_argv
    assert subprocess_policy.require_shell_false
    assert subprocess_policy.require_timeout
    assert subprocess_policy.require_sandbox_cwd
    assert subprocess_policy.require_minimal_env
    assert subprocess_policy.require_bounded_output
    for name in (
        "allow_shell_true",
        "allow_command_string",
        "allow_package_manager",
        "allow_external_agent",
        "allow_network_access",
    ):
        assert getattr(subprocess_policy, name) is False
        with pytest.raises(ValueError):
            build_controlled_test_subprocess_policy(**{name: True})


def test_input_command_environment_and_cwd_boundaries(tmp_path):
    source = build_sandbox_test_execution_source_ref()
    execution_input = build_sandbox_test_execution_input(sandbox_cwd_ref=str(tmp_path))
    command_line = build_controlled_test_command_line(argv=[sys.executable, "-m", "pytest", "--version"])
    environment = build_minimal_test_environment()
    cwd = validate_controlled_test_cwd(str(tmp_path), str(tmp_path))
    assert source.source_kind == SandboxTestExecutionSourceKind.V0371_TEST_INVOCATION_CONTRACT
    assert execution_input.timeout_seconds > 0
    assert "shell" in execution_input.prohibited_runtime_actions
    assert command_line.structured_argv
    assert command_line.shell is False
    assert command_line.allowlisted
    assert command_line.contains_blocked_arg is False
    assert environment.minimal_env
    assert environment.inherited_env is False
    assert environment.credential_env_present is False
    assert environment.network_env_present is False
    assert cwd.valid_sandbox_cwd
    assert cwd.live_workspace_cwd is False
    assert cwd.reference_cwd is False
    assert cwd.outside_sandbox_cwd is False
    with pytest.raises(ValueError):
        build_controlled_test_command_line(argv=[sys.executable, "-m", "pytest", "&&"], contains_blocked_arg=True)
    with pytest.raises(ValueError):
        build_controlled_test_environment(inherited_env=True)


def test_cwd_validation_blocks_live_reference_and_outside(tmp_path):
    sandbox_root = tmp_path / "sandbox"
    sandbox_root.mkdir()
    nested = sandbox_root / "pkg"
    nested.mkdir()
    live = tmp_path / "live"
    live.mkdir()
    references = sandbox_root / "references"
    references.mkdir()
    outside = tmp_path / "outside"
    outside.mkdir()
    assert validate_controlled_test_cwd(str(nested), str(sandbox_root)).valid_sandbox_cwd
    live_result = validate_controlled_test_cwd(str(live), str(sandbox_root), str(live))
    reference_result = validate_controlled_test_cwd(str(references), str(sandbox_root))
    outside_result = validate_controlled_test_cwd(str(outside), str(sandbox_root))
    assert live_result.valid_sandbox_cwd is False
    assert live_result.live_workspace_cwd
    assert reference_result.valid_sandbox_cwd is False
    assert reference_result.reference_cwd
    assert outside_result.valid_sandbox_cwd is False
    assert outside_result.outside_sandbox_cwd


def test_invocation_result_output_and_reports_are_not_certification(tmp_path):
    execution_input = build_sandbox_test_execution_input(sandbox_cwd_ref=str(tmp_path))
    invocation = build_controlled_test_subprocess_invocation(execution_input=execution_input)
    result = build_controlled_test_subprocess_result(
        subprocess_invocation_id=invocation.subprocess_invocation_id,
        subprocess_status=ControlledTestSubprocessStatus.COMPLETED,
        exit_kind=SandboxTestProcessExitKind.EXIT_ZERO,
        return_code=0,
        stdout_text="ok",
    )
    capture = build_sandbox_test_output_capture(
        subprocess_result_id=result.subprocess_result_id,
        captured_text="ok",
        original_char_count=2,
        captured_char_count=2,
    )
    execution_result = build_sandbox_test_execution_result(
        execution_input_id=execution_input.execution_input_id,
        subprocess_invocation=invocation,
        subprocess_result=result,
        output_captures=[capture],
        return_code=0,
    )
    decision = build_sandbox_test_execution_decision()
    validation = build_sandbox_test_execution_validation_report(decision=decision)
    report = build_sandbox_test_execution_report(execution_result=execution_result, validation_report=validation)
    preview = build_sandbox_test_execution_run_preview(execution_input_id=execution_input.execution_input_id)
    assert invocation.shell is False
    assert controlled_test_subprocess_invocation_is_shell_false(invocation)
    assert result.shell_used is False
    assert result.dependency_install_attempted is False
    assert result.network_access_allowed is False
    assert result.live_workspace_write_allowed is False
    assert execution_result.production_certified is False
    assert execution_result.ready_for_execution is False
    assert sandbox_test_execution_result_is_not_production_certification(execution_result)
    assert decision.arbitrary_shell_allowed is False
    assert decision.dependency_install_allowed is False
    assert validation.network_policy_blocked
    assert validation.network_hard_isolation_certified is False
    assert report.production_certified is False
    assert preview.ready_for_arbitrary_shell is False
    with pytest.raises(ValueError):
        build_sandbox_test_execution_result(production_certified=True)
    with pytest.raises(ValueError):
        build_sandbox_test_execution_decision(network_access_allowed=True)


def test_output_capture_bounds_and_redacts():
    long_capture = bound_and_redact_test_output("x" * 30, 10)
    secret_capture = bound_and_redact_test_output("TOKEN=abc", 100)
    assert long_capture.truncated
    assert long_capture.captured_char_count == 10
    assert secret_capture.redacted
    assert secret_capture.secret_like_content_detected
    assert "[REDACTED]" in secret_capture.captured_text


def _python_contract(args=None):
    executable = build_sandbox_test_allowed_executable(executable_name=sys.executable)
    command_spec = build_sandbox_test_command_spec(
        command_kind=SandboxTestCommandKind.PYTHON_MODULE_INVOCATION,
        executable=executable,
        module=None,
    )
    contract = build_sandbox_test_invocation_contract(command_spec=command_spec)
    command_line = build_controlled_test_command_line_from_contract(contract, extra_args=args or ["-c", "print('ok')"])
    return contract, command_line


def test_controlled_harmless_python_subprocess_executes_under_tmp_sandbox(tmp_path):
    _, command_line = _python_contract()
    execution_input = build_sandbox_test_execution_input(sandbox_cwd_ref=str(tmp_path), timeout_seconds=10)
    cwd = validate_controlled_test_cwd(str(tmp_path), str(tmp_path))
    invocation = build_controlled_test_subprocess_invocation(
        execution_input=execution_input,
        subprocess_kind=ControlledTestSubprocessKind.PYTHON_MODULE_SUBPROCESS,
        command_line=command_line,
        cwd_validation=cwd,
        timeout_seconds=10,
    )
    result = run_controlled_sandbox_test_subprocess(invocation)
    execution_result = run_sandbox_test_execution_engine(invocation)
    assert result.return_code == 0
    assert result.exit_kind == SandboxTestProcessExitKind.EXIT_ZERO
    assert "ok" in result.stdout_text
    assert result.shell_used is False
    assert execution_result.return_code == 0
    assert execution_result.production_certified is False


def test_nonzero_and_timeout_results_are_process_metadata_only(tmp_path):
    _, nonzero_line = _python_contract(["-c", "raise SystemExit(3)"])
    _, timeout_line = _python_contract(["-c", "from time import sleep\nsleep(2)"])
    execution_input = build_sandbox_test_execution_input(sandbox_cwd_ref=str(tmp_path), timeout_seconds=1)
    cwd = validate_controlled_test_cwd(str(tmp_path), str(tmp_path))
    nonzero_invocation = build_controlled_test_subprocess_invocation(
        execution_input=execution_input,
        subprocess_kind=ControlledTestSubprocessKind.PYTHON_MODULE_SUBPROCESS,
        command_line=nonzero_line,
        cwd_validation=cwd,
        timeout_seconds=5,
    )
    timeout_invocation = build_controlled_test_subprocess_invocation(
        execution_input=execution_input,
        subprocess_kind=ControlledTestSubprocessKind.PYTHON_MODULE_SUBPROCESS,
        command_line=timeout_line,
        cwd_validation=cwd,
        timeout_seconds=1,
    )
    nonzero = run_sandbox_test_execution_engine(nonzero_invocation)
    timed_out = run_sandbox_test_execution_engine(timeout_invocation)
    assert nonzero.return_code == 3
    assert nonzero.execution_status == SandboxTestExecutionStatus.EXECUTION_COMPLETED_WITH_NONZERO_EXIT
    assert nonzero.ready_for_automatic_repair is False
    assert timed_out.timed_out
    assert timed_out.execution_status == SandboxTestExecutionStatus.EXECUTION_TIMED_OUT
    assert timed_out.ready_for_automatic_repair is False


@pytest.mark.parametrize(
    "argv",
    [
        ["bash", "-c", "echo unsafe"],
        ["npm", "test"],
        ["pip", "install", "pytest"],
        ["run-codex"],
        ["dominion"],
        [sys.executable, "-c", "print('x')", "&&"],
    ],
)
def test_blocked_commands_do_not_run(tmp_path, argv):
    execution_input = build_sandbox_test_execution_input(sandbox_cwd_ref=str(tmp_path))
    cwd = validate_controlled_test_cwd(str(tmp_path), str(tmp_path))
    with pytest.raises(ValueError):
        command_line = build_controlled_test_command_line(
            executable_name=argv[0],
            argv=argv,
            contains_blocked_arg=True,
        )
        build_controlled_test_subprocess_invocation(
            execution_input=execution_input,
            command_line=command_line,
            cwd_validation=cwd,
        )


def test_validation_blocks_invalid_invocation_before_run(tmp_path):
    execution_input = build_sandbox_test_execution_input(sandbox_cwd_ref=str(tmp_path))
    outside = tmp_path / "outside"
    outside.mkdir()
    cwd = validate_controlled_test_cwd(str(outside), str(tmp_path / "sandbox"))
    command_line = build_controlled_test_command_line(argv=[sys.executable, "-m", "pytest", "--version"])
    invocation = build_controlled_test_subprocess_invocation(
        execution_input=execution_input,
        command_line=command_line,
        cwd_validation=cwd,
        executable_now=False,
    )
    validation = validate_controlled_test_subprocess_invocation(invocation)
    result = run_controlled_sandbox_test_subprocess(invocation)
    assert validation.findings
    assert result.exit_kind == SandboxTestProcessExitKind.BLOCKED_BEFORE_EXECUTION
    assert result.return_code is None


def test_guarantee_readiness_and_static_subprocess_boundary():
    guarantee = build_sandbox_test_execution_no_unsafe_command_guarantee()
    readiness = build_v0372_readiness_report()
    for field in fields(SandboxTestExecutionNoUnsafeCommandGuarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    assert readiness.ready_for_sandbox_test_execution_engine
    assert readiness.ready_for_controlled_test_subprocess
    assert readiness.ready_for_allowlisted_test_execution
    assert readiness.ready_for_bounded_test_output_capture
    assert readiness.network_policy_blocked
    assert readiness.network_hard_isolation_certified is False
    assert v0372_readiness_report_is_not_general_execution_ready(readiness)
    with pytest.raises(ValueError):
        build_v0372_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v0372_readiness_report(network_hard_isolation_certified=True)
    source = inspect.getsource(execution_module)
    assert "shell=True" not in source
    assert "os.system" not in source
    assert "Path.write_text" not in source
    assert "Path.write_bytes" not in source
    assert "open(" not in source
    assert "import requests" not in source
    assert "import httpx" not in source
    assert "import urllib" not in source
    assert "import aiohttp" not in source
    assert "import socket" not in source
    assert "apply_patch(" not in source
    assert "git apply" not in source
    assert source.count("subprocess.run(") == 1
