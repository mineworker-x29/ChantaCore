from chanta_core.internal_provider.gated_local_runtime_execution import (
    GATED_LOCAL_RUNTIME_EFFECT_TYPES,
    GATED_LOCAL_RUNTIME_EVENT_TYPES,
    GATED_LOCAL_RUNTIME_OBJECT_TYPES,
    BoundedLocalCommandRunRequest,
    LocalRuntimeExecutionAuthorizationService,
    LocalRuntimeExecutionBoundaryReportService,
    LocalRuntimeExecutionGatePolicyService,
    LocalRuntimeExecutionGateRequest,
    LocalRuntimeExecutionGateService,
    LocalRuntimeExecutionNeedsMoreInputCandidate,
    LocalRuntimeExecutionNoActionCandidate,
    LocalRuntimeProcessSpecService,
    LocalRuntimeRunnerPolicy,
    LocalRuntimeSideEffectPolicy,
)


def test_v0247_gate_policy_and_report_build() -> None:
    policy = LocalRuntimeExecutionGatePolicyService().build_gate_policy()
    assert policy.version == "v0.24.7"
    assert policy.gate_required is True
    assert policy.eligibility_required is True
    assert policy.static_safety_pass_required is True
    assert policy.preflight_pass_required is True
    assert policy.single_use_authorization_required is True
    assert policy.allowlist_match_required is True
    assert policy.argv_required is True
    assert policy.shell_forbidden is True
    assert policy.workspace_bound_cwd_required is True
    assert policy.timeout_required is True
    assert policy.output_cap_required is True
    assert policy.redaction_required is True
    assert policy.side_effect_scan_required is True
    assert policy.network_forbidden is True
    assert policy.package_install_forbidden is True
    assert policy.destructive_command_forbidden is True
    assert policy.arbitrary_subprocess_forbidden is True
    assert policy.credential_env_forbidden is True

    report = LocalRuntimeExecutionBoundaryReportService().build_report(LocalRuntimeExecutionGateRequest(eligibility_id="demo"))
    assert report.version == "v0.24.7"
    assert report.gate_opened is True
    assert report.authorization is not None
    assert report.authorization.single_use is True
    assert report.authorization.consumed is False
    assert report.ready_for_v0_24_8 is True
    assert report.ready_for_v0_25 is False
    assert report.shell_used is False
    assert report.network_accessed is False
    assert report.package_installed is False
    assert report.destructive_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_v0247_required_gate_conditions_exist() -> None:
    state, authorization, candidate, eligibility, safety_report = LocalRuntimeExecutionGateService().evaluate_gate(LocalRuntimeExecutionGateRequest(eligibility_id="demo"))
    assert state.gate_status == "open"
    assert authorization is not None
    condition_types = {condition.condition_type for condition in state.conditions}
    for condition in [
        "candidate_exists",
        "execution_eligibility_exists",
        "static_safety_passed",
        "declared_preflight_passed",
        "gate_required_true",
        "argv_is_list",
        "shell_absent",
        "shell_forbidden",
        "allowlist_match_valid",
        "cwd_workspace_bound",
        "env_values_not_materialized",
        "credential_env_absent",
        "timeout_policy_present",
        "output_policy_present",
        "output_cap_present",
        "redaction_required",
        "side_effect_scan_required",
        "network_command_absent",
        "package_install_command_absent",
        "destructive_command_absent",
        "authorization_single_use",
        "authorization_unconsumed",
        "no_external_provider_adapter",
        "no_schumpeter_split",
    ]:
        assert condition in condition_types
    assert candidate is not None
    assert eligibility is not None
    assert safety_report.ready_for_v0_24_7 is True


def test_v0247_authorization_consumes_exactly_once_and_process_spec_is_safe() -> None:
    state, authorization, candidate, eligibility, _ = LocalRuntimeExecutionGateService().evaluate_gate(LocalRuntimeExecutionGateRequest(eligibility_id="demo"))
    assert state.gate_status == "open"
    assert authorization is not None and candidate is not None and eligibility is not None
    assert authorization.consumed is False
    assert LocalRuntimeExecutionAuthorizationService().consume_authorization_exactly_once(authorization) is True
    assert authorization.consumed is True
    assert LocalRuntimeExecutionAuthorizationService().consume_authorization_exactly_once(authorization) is False

    spec = LocalRuntimeProcessSpecService().build_process_spec(candidate, authorization, LocalRuntimeRunnerPolicy("runner_policy:test"))
    assert isinstance(spec.argv, list)
    assert spec.shell is False
    assert spec.command_string is None
    assert spec.cwd_ref["label"] == "."
    assert spec.private_full_path_output is False
    assert spec.timeout_seconds > 0
    assert spec.max_stdout_bytes > 0
    assert spec.max_stderr_bytes > 0
    assert spec.credential_env_materialized is False


def test_v0247_bounded_run_report_has_capped_redacted_output_and_side_effect_scan() -> None:
    report = LocalRuntimeExecutionBoundaryReportService().build_report(LocalRuntimeExecutionGateRequest(eligibility_id="demo"), run=True)
    assert report.gate_opened is True
    assert report.authorization_consumed is True
    assert report.bounded_run is not None
    assert report.bounded_run.shell_used is False
    assert report.bounded_run.authorization_consumed is True
    assert report.local_command_executed is True
    assert report.process_spawned in {True, False}
    assert report.process_result is not None
    assert report.process_result.result_status in {"completed", "failed", "timeout", "blocked"}
    assert report.output_redacted is True or report.output_captures == []
    assert report.side_effect_scan is not None
    assert report.side_effect_scan_performed is True
    assert report.unexpected_side_effect_detected is False
    assert report.network_accessed is False
    assert report.package_installed is False
    assert report.destructive_command_executed is False


def test_v0247_models_ocel_pig_ocpx_and_no_action_candidates() -> None:
    run_request = BoundedLocalCommandRunRequest("auth", "candidate")
    assert run_request.authorization_id == "auth"
    needs = LocalRuntimeExecutionNeedsMoreInputCandidate("candidate:needs", "missing", ["eligibility"], [])
    no_action = LocalRuntimeExecutionNoActionCandidate("candidate:none", "no action", [])
    assert needs.candidate_status == "needs_more_input"
    assert no_action.candidate_status == "no_action"
    policy = LocalRuntimeSideEffectPolicy(
        policy_id="side_effect_policy:test",
        allowed_write_paths=[],
        denied_write_paths=["*"],
        cache_write_allowlist=[],
    )
    assert policy.pre_run_snapshot_required is True
    assert policy.post_run_snapshot_required is True
    assert "local_runtime_execution_boundary_report" in GATED_LOCAL_RUNTIME_OBJECT_TYPES
    assert "local_runtime_execution_boundary_report_created" in GATED_LOCAL_RUNTIME_EVENT_TYPES
    assert "bounded_local_command_executed" in GATED_LOCAL_RUNTIME_EFFECT_TYPES
    service = LocalRuntimeExecutionBoundaryReportService()
    assert service.build_pig_report()["subject"] == "gated_local_runtime_execution_boundary"
    assert service.build_ocpx_projection()["state"] == "gated_local_runtime_execution_boundary_created"
