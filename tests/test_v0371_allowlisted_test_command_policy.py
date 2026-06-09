from dataclasses import fields
import inspect

import pytest

import chanta_core.agent_runtime.sandbox_test_command_policy as policy_module
from chanta_core.agent_runtime import (
    SandboxTestAllowedExecutable,
    SandboxTestAllowedModule,
    SandboxTestArgumentKind,
    SandboxTestArgumentSpec,
    SandboxTestCommandAllowlist,
    SandboxTestCommandDecisionKind,
    SandboxTestCommandDenylist,
    SandboxTestCommandFlagSet,
    SandboxTestCommandKind,
    SandboxTestCommandNoExecutionGuarantee,
    SandboxTestCommandPolicyReport,
    SandboxTestCommandReadinessLevel,
    SandboxTestCommandRiskKind,
    SandboxTestCommandSourceRef,
    SandboxTestCommandSpec,
    SandboxTestCommandStatus,
    SandboxTestCwdKind,
    SandboxTestDependencyPosture,
    SandboxTestDeniedCommand,
    SandboxTestEnvironmentContract,
    SandboxTestEnvironmentMode,
    SandboxTestExecutableKind,
    SandboxTestInvocationContract,
    SandboxTestInvocationDecision,
    SandboxTestInvocationRequest,
    SandboxTestInvocationRunPreview,
    SandboxTestInvocationSourceKind,
    SandboxTestInvocationValidationFinding,
    SandboxTestInvocationValidationReport,
    SandboxTestNetworkPosture,
    SandboxTestOutputCaptureContract,
    SandboxTestOutputCaptureMode,
    SandboxTestResourceLimitKind,
    SandboxTestResourceLimitPolicy,
    SandboxTestSandboxCwdPolicy,
    SandboxTestTimeoutKind,
    SandboxTestTimeoutPolicy,
    V0371ReadinessReport,
    build_sandbox_test_allowed_executable,
    build_sandbox_test_allowed_module,
    build_sandbox_test_argument_spec,
    build_sandbox_test_command_allowlist,
    build_sandbox_test_command_denylist,
    build_sandbox_test_command_flags,
    build_sandbox_test_command_no_execution_guarantee,
    build_sandbox_test_command_policy_report,
    build_sandbox_test_command_source_ref,
    build_sandbox_test_command_spec,
    build_sandbox_test_denied_command,
    build_sandbox_test_environment_contract,
    build_sandbox_test_invocation_contract,
    build_sandbox_test_invocation_decision,
    build_sandbox_test_invocation_request,
    build_sandbox_test_invocation_run_preview,
    build_sandbox_test_invocation_validation_finding,
    build_sandbox_test_invocation_validation_report,
    build_sandbox_test_output_capture_contract,
    build_sandbox_test_resource_limit_policy,
    build_sandbox_test_sandbox_cwd_policy,
    build_sandbox_test_timeout_policy,
    build_v0371_readiness_report,
    decide_sandbox_test_invocation_eligibility,
    default_sandbox_test_command_allowlist,
    default_sandbox_test_command_denylist,
    default_sandbox_test_invocation_contract,
    sandbox_test_command_flags_preserve_no_execution,
    sandbox_test_command_spec_is_not_execution,
    sandbox_test_denylist_blocks_shell_install_network,
    sandbox_test_invocation_contract_is_not_execution,
    sandbox_test_invocation_decision_is_not_execution,
    v0371_readiness_report_is_not_execution_ready,
    validate_sandbox_test_invocation_request,
)


SAFE_FLAG_NAMES = {
    "ready_for_v0372_sandbox_test_execution_engine",
    "ready_for_v0373_test_result_envelope",
    "ready_for_v0376_vera_codex_one_shot_agent_trial",
    "ready_for_allowlisted_test_command_policy",
    "ready_for_structured_test_command_spec",
    "ready_for_test_invocation_contract",
    "ready_for_sandbox_cwd_policy",
    "ready_for_test_timeout_policy",
    "ready_for_test_output_capture_contract",
    "ready_for_future_sandbox_test_execution_input",
}


def _unsafe_flag_names(cls):
    return [
        field.name
        for field in fields(cls)
        if field.name.startswith("ready_for_") and field.name not in SAFE_FLAG_NAMES
    ]


def test_v0371_taxonomies_have_required_values():
    assert {item.value for item in SandboxTestCommandKind} == {
        "python_pytest_module",
        "python_pytest_file",
        "python_pytest_node",
        "python_unittest_module",
        "python_module_invocation",
        "metadata_only",
        "blocked_shell_command",
        "blocked_package_script",
        "blocked_dependency_install",
        "blocked_network_command",
        "blocked_external_agent_command",
        "blocked_dominion_command",
        "blocked_repair_command",
        "blocked_multi_cycle_command",
        "no_op",
        "unknown",
    }
    assert {item.value for item in SandboxTestInvocationSourceKind} == {
        "v0370_sandbox_test_runner_boundary",
        "v0369_patch_apply_sandbox_consolidation",
        "v0368_cli_sandbox_apply_surface",
        "v0367_patch_apply_trace_packet",
        "v0366_agentic_operation_run_packet",
        "v0365_post_apply_validation_report",
        "structured_command_request",
        "cli_like_argv",
        "manual_operator_input",
        "test_fixture",
        "unknown",
    }
    assert "eligible_for_future_sandbox_test_execution" in {item.value for item in SandboxTestCommandStatus}
    assert "design_handoff_ready_for_v0372" in {item.value for item in SandboxTestCommandReadinessLevel}
    assert "allow_future_sandbox_test_execution_input" in {item.value for item in SandboxTestCommandDecisionKind}
    assert "shell_metacharacter_risk" in {item.value for item in SandboxTestCommandRiskKind}
    assert "python_executable" in {item.value for item in SandboxTestExecutableKind}
    assert "unsafe_shell_fragment" in {item.value for item in SandboxTestArgumentKind}
    assert "sandbox_root" in {item.value for item in SandboxTestCwdKind}
    assert "bounded_timeout" in {item.value for item in SandboxTestTimeoutKind}
    assert "default_limits" in {item.value for item in SandboxTestResourceLimitKind}
    assert "bounded_stdout_stderr_future_gated" in {item.value for item in SandboxTestOutputCaptureMode}
    assert "minimal_sandbox_env" in {item.value for item in SandboxTestEnvironmentMode}
    assert "network_blocked" in {item.value for item in SandboxTestNetworkPosture}
    assert "missing_dependency_does_not_allow_install" in {item.value for item in SandboxTestDependencyPosture}


def test_required_models_are_exported():
    for model in (
        SandboxTestCommandFlagSet,
        SandboxTestCommandSourceRef,
        SandboxTestAllowedExecutable,
        SandboxTestAllowedModule,
        SandboxTestArgumentSpec,
        SandboxTestCommandSpec,
        SandboxTestCommandAllowlist,
        SandboxTestCommandDenylist,
        SandboxTestSandboxCwdPolicy,
        SandboxTestTimeoutPolicy,
        SandboxTestResourceLimitPolicy,
        SandboxTestOutputCaptureContract,
        SandboxTestEnvironmentContract,
        SandboxTestInvocationContract,
        SandboxTestInvocationRequest,
        SandboxTestInvocationDecision,
        SandboxTestDeniedCommand,
        SandboxTestInvocationValidationFinding,
        SandboxTestInvocationValidationReport,
        SandboxTestCommandPolicyReport,
        SandboxTestInvocationRunPreview,
        SandboxTestCommandNoExecutionGuarantee,
        V0371ReadinessReport,
    ):
        assert model is not None


def test_flags_allow_policy_readiness_and_preserve_no_execution():
    flags = build_sandbox_test_command_flags()
    assert flags.allowlisted_test_command_policy_constructed
    assert flags.structured_command_spec_available
    assert flags.test_command_allowlist_available
    assert flags.test_command_denylist_available
    assert flags.test_invocation_contract_available
    assert flags.sandbox_cwd_policy_available
    assert flags.timeout_policy_available
    assert flags.output_capture_contract_available
    assert flags.environment_contract_available
    assert flags.ready_for_v0372_sandbox_test_execution_engine
    assert flags.ready_for_v0373_test_result_envelope
    assert flags.ready_for_v0376_vera_codex_one_shot_agent_trial
    assert flags.ready_for_allowlisted_test_command_policy
    assert flags.ready_for_structured_test_command_spec
    assert flags.ready_for_test_invocation_contract
    assert flags.ready_for_sandbox_cwd_policy
    assert flags.ready_for_test_timeout_policy
    assert flags.ready_for_test_output_capture_contract
    assert flags.ready_for_future_sandbox_test_execution_input
    assert sandbox_test_command_flags_preserve_no_execution(flags)
    for name in _unsafe_flag_names(SandboxTestCommandFlagSet) + ["production_certified"]:
        assert getattr(flags, name) is False


@pytest.mark.parametrize("field_name", _unsafe_flag_names(SandboxTestCommandFlagSet) + ["production_certified"])
def test_flags_reject_unsafe_true(field_name):
    with pytest.raises(ValueError):
        build_sandbox_test_command_flags(**{field_name: True})


def test_source_ref_is_metadata_only():
    source = build_sandbox_test_command_source_ref()
    assert source.source_kind == SandboxTestInvocationSourceKind.V0370_SANDBOX_TEST_RUNNER_BOUNDARY
    assert source.evidence_refs


def test_allowed_executable_allows_python_future_metadata_only():
    executable = build_sandbox_test_allowed_executable()
    assert executable.executable_kind == SandboxTestExecutableKind.PYTHON_EXECUTABLE
    assert executable.allowed_for_future_execution
    assert executable.executable_now is False
    assert executable.shell is False
    assert executable.package_manager is False
    assert executable.external_agent is False


@pytest.mark.parametrize(
    "kwargs",
    [
        {"executable_kind": SandboxTestExecutableKind.SHELL_EXECUTABLE, "executable_name": "bash"},
        {"executable_kind": SandboxTestExecutableKind.PACKAGE_MANAGER_EXECUTABLE, "executable_name": "pip"},
        {"executable_kind": SandboxTestExecutableKind.EXTERNAL_AGENT_EXECUTABLE, "executable_name": "run-codex"},
        {"executable_now": True},
        {"shell": True},
        {"package_manager": True},
        {"external_agent": True},
    ],
)
def test_allowed_executable_rejects_unsafe_authority(kwargs):
    with pytest.raises(ValueError):
        build_sandbox_test_allowed_executable(**kwargs)


def test_allowed_module_allows_pytest_and_unittest_future_metadata_only():
    pytest_module = build_sandbox_test_allowed_module(module_name="pytest")
    unittest_module = build_sandbox_test_allowed_module(module_name="unittest")
    assert pytest_module.allowed_for_future_execution
    assert unittest_module.allowed_for_future_execution
    assert pytest_module.executable_now is False
    assert unittest_module.executable_now is False


def test_argument_spec_blocks_unsafe_patterns():
    spec = build_sandbox_test_argument_spec()
    assert ";" in spec.blocked_patterns
    assert "http://" in spec.blocked_patterns
    assert "run-codex" in spec.blocked_patterns
    assert "dominion" in spec.blocked_patterns
    assert spec.max_chars >= 0


def test_command_spec_is_future_eligible_but_not_execution():
    spec = build_sandbox_test_command_spec()
    assert spec.allowed_for_future_sandbox_execution
    assert spec.executable_now is False
    assert spec.shell_allowed is False
    assert spec.dependency_install_allowed is False
    assert spec.network_allowed is False
    assert spec.live_workspace_allowed is False
    assert sandbox_test_command_spec_is_not_execution(spec)
    with pytest.raises(ValueError):
        build_sandbox_test_command_spec(executable_now=True)
    with pytest.raises(ValueError):
        build_sandbox_test_command_spec(shell_allowed=True)
    with pytest.raises(ValueError):
        build_sandbox_test_command_spec(cwd_kind=SandboxTestCwdKind.LIVE_WORKSPACE_ROOT)


def test_allowlist_and_denylist_are_future_only_and_block_unsafe_surfaces():
    allowlist = default_sandbox_test_command_allowlist()
    denylist = default_sandbox_test_command_denylist()
    assert allowlist.future_execution_only
    assert allowlist.executable_now is False
    assert allowlist.allowed_command_specs
    assert sandbox_test_denylist_blocks_shell_install_network(denylist)
    assert "bash" in denylist.blocked_command_names
    assert "pip" in denylist.blocked_command_names
    assert "run-codex" in denylist.blocked_command_names
    assert "dominion" in denylist.blocked_command_names
    with pytest.raises(ValueError):
        build_sandbox_test_command_allowlist(executable_now=True)
    with pytest.raises(ValueError):
        build_sandbox_test_command_denylist(blocks_shell=False)


def test_cwd_timeout_resource_output_and_environment_contracts_block_runtime_escape():
    cwd = build_sandbox_test_sandbox_cwd_policy()
    timeout = build_sandbox_test_timeout_policy()
    resource = build_sandbox_test_resource_limit_policy()
    output = build_sandbox_test_output_capture_contract()
    env = build_sandbox_test_environment_contract()
    assert SandboxTestCwdKind.LIVE_WORKSPACE_ROOT in cwd.blocked_cwd_kinds
    assert SandboxTestCwdKind.REFERENCES_ROOT in cwd.blocked_cwd_kinds
    assert SandboxTestCwdKind.EXTERNAL_ROOT in cwd.blocked_cwd_kinds
    assert cwd.allow_live_workspace_cwd is False
    assert timeout.require_timeout
    assert timeout.allow_unbounded_timeout is False
    assert resource.require_resource_limits
    assert resource.allow_unbounded_resources is False
    assert output.redact_secrets
    assert output.block_raw_secret_output
    assert output.allow_output_capture_now is False
    assert env.require_minimal_env
    assert env.block_inherited_env
    assert env.block_credential_env
    assert env.allow_env_now is False
    with pytest.raises(ValueError):
        build_sandbox_test_timeout_policy(allow_unbounded_timeout=True)
    with pytest.raises(ValueError):
        build_sandbox_test_resource_limit_policy(allow_unbounded_resources=True)
    with pytest.raises(ValueError):
        build_sandbox_test_output_capture_contract(allow_output_capture_now=True)
    with pytest.raises(ValueError):
        build_sandbox_test_environment_contract(allow_env_now=True)


def test_invocation_contract_future_eligible_but_not_execution_and_preserves_do_nothing():
    contract = default_sandbox_test_invocation_contract()
    assert contract.eligible_for_future_sandbox_test_execution
    assert contract.do_nothing_baseline_required_for_future_evaluation
    assert sandbox_test_invocation_contract_is_not_execution(contract)
    assert contract.executable_now is False
    assert contract.test_execution_allowed is False
    assert contract.subprocess_allowed is False
    assert contract.shell_allowed is False
    assert contract.dependency_install_allowed is False
    assert contract.network_allowed is False
    with pytest.raises(ValueError):
        build_sandbox_test_invocation_contract(subprocess_allowed=True)
    with pytest.raises(ValueError):
        build_sandbox_test_invocation_contract(test_execution_allowed=True)


def test_request_decision_and_validation_are_metadata_only():
    request = build_sandbox_test_invocation_request()
    decision = decide_sandbox_test_invocation_eligibility(request)
    report = validate_sandbox_test_invocation_request(request)
    assert request.requested_executable_name == "python"
    assert decision.eligible_for_future_sandbox_test_execution
    assert decision.executable_now is False
    assert decision.test_execution_allowed is False
    assert decision.controlled_subprocess_allowed is False
    assert decision.shell_allowed is False
    assert sandbox_test_invocation_decision_is_not_execution(decision)
    assert report.eligible_for_future_sandbox_test_execution
    assert report.certifies_test_execution is False
    with pytest.raises(ValueError):
        build_sandbox_test_invocation_decision(test_execution_allowed=True)


@pytest.mark.parametrize(
    "request_kwargs",
    [
        {"requested_executable_name": "bash"},
        {"requested_executable_name": "npm"},
        {"requested_executable_name": "pip"},
        {"requested_args": ["install", "pytest"]},
        {"requested_executable_name": "run-claude-code"},
        {"requested_executable_name": "run-codex"},
        {"requested_executable_name": "run-opencode"},
        {"requested_executable_name": "run-hermes"},
        {"requested_executable_name": "dominion"},
        {"requested_executable_name": "auto-repair"},
        {"requested_executable_name": "multi-cycle"},
        {"requested_args": ["tests/test_example.py", "&&", "echo"]},
        {"requested_args": ["https://example.invalid"]},
        {"requested_cwd_kind": SandboxTestCwdKind.LIVE_WORKSPACE_ROOT},
        {"requested_timeout_seconds": None},
        {"requested_command_kind": SandboxTestCommandKind.UNKNOWN},
    ],
)
def test_unsafe_invocation_requests_are_blocked(request_kwargs):
    request = build_sandbox_test_invocation_request(**request_kwargs)
    decision = decide_sandbox_test_invocation_eligibility(request)
    assert decision.eligible_for_future_sandbox_test_execution is False
    assert decision.command_status == SandboxTestCommandStatus.BLOCKED
    assert decision.decision_kind == SandboxTestCommandDecisionKind.BLOCK
    assert decision.risk_kinds
    assert sandbox_test_invocation_decision_is_not_execution(decision)


def test_denied_command_is_safe_outcome():
    denied = build_sandbox_test_denied_command()
    assert denied.reason
    assert denied.safe_alternatives


def test_reports_previews_and_no_execution_guarantee():
    finding = build_sandbox_test_invocation_validation_finding()
    policy_report = build_sandbox_test_command_policy_report()
    preview = build_sandbox_test_invocation_run_preview()
    guarantee = build_sandbox_test_command_no_execution_guarantee()
    readiness = build_v0371_readiness_report()
    assert finding.message
    assert policy_report.allowlist_ready
    assert policy_report.ready_for_test_execution is False
    assert preview.future_eligible
    assert preview.executable_now is False
    for field in fields(SandboxTestCommandNoExecutionGuarantee):
        if field.name.startswith("no_"):
            assert getattr(guarantee, field.name) is True
    assert readiness.ready_for_allowlisted_test_command_policy
    assert readiness.ready_for_structured_test_command_spec
    assert readiness.ready_for_test_invocation_contract
    assert readiness.ready_for_future_sandbox_test_execution_input
    assert readiness.ready_for_v0372_sandbox_test_execution_engine
    assert readiness.ready_for_v0373_test_result_envelope
    assert readiness.ready_for_v0376_vera_codex_one_shot_agent_trial
    assert v0371_readiness_report_is_not_execution_ready(readiness)
    with pytest.raises(ValueError):
        build_v0371_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_sandbox_test_command_no_execution_guarantee(no_test_execution=False)


def test_helper_functions_are_pure_metadata_and_static_source_has_no_runtime_patterns():
    source = inspect.getsource(policy_module)
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "Path.write_text",
        "Path.write_bytes",
        "open(",
        "import requests",
        "import httpx",
        "import urllib",
        "import aiohttp",
        "import socket",
        "eval(",
        "exec(",
        "apply_patch(",
        "git apply",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source
    safe_request = build_sandbox_test_invocation_request()
    safe_decision = decide_sandbox_test_invocation_eligibility(safe_request)
    unsafe_request = build_sandbox_test_invocation_request(requested_executable_name="bash")
    unsafe_decision = decide_sandbox_test_invocation_eligibility(unsafe_request)
    assert safe_decision.eligible_for_future_sandbox_test_execution
    assert unsafe_decision.eligible_for_future_sandbox_test_execution is False
    assert sandbox_test_invocation_decision_is_not_execution(safe_decision)
    assert sandbox_test_invocation_decision_is_not_execution(unsafe_decision)
