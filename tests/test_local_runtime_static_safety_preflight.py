from chanta_core.internal_provider.local_runtime_safety_preflight import (
    LOCAL_RUNTIME_SAFETY_EFFECT_TYPES,
    LOCAL_RUNTIME_SAFETY_EVENT_TYPES,
    LOCAL_RUNTIME_SAFETY_OBJECT_TYPES,
    LocalRuntimeCommandAllowlistPolicyService,
    LocalRuntimeDeclaredPreflightPolicyService,
    LocalRuntimeExecutionEligibilityService,
    LocalRuntimeForbiddenPatternPolicyService,
    LocalRuntimeSafetyNeedsMoreInputCandidate,
    LocalRuntimeSafetyNoActionCandidate,
    LocalRuntimeSafetyPreflightReportService,
    LocalRuntimeSafetyPreflightRequest,
    LocalRuntimeStaticSafetyReportService,
    LocalRuntimeStaticSafetyRuleRegistry,
)


def test_v0246_request_policy_rules_and_report_build() -> None:
    request = LocalRuntimeSafetyPreflightRequest(candidate_id="demo")
    assert request.include_static_safety is True
    assert request.include_declared_preflight is True
    assert request.include_allowlist_check is True

    allowlist = LocalRuntimeCommandAllowlistPolicyService().build_allowlist_policy()
    assert allowlist.version == "v0.24.6"
    assert allowlist.deny_by_default is True
    assert allowlist.argv_prefix_required is True
    assert allowlist.shell_forbidden is True
    assert allowlist.shell_string_forbidden is True
    assert allowlist.workspace_bound_cwd_required is True
    assert allowlist.timeout_required is True
    assert allowlist.output_cap_required is True
    assert allowlist.redaction_required is True
    assert allowlist.env_value_materialization_forbidden is True
    assert allowlist.credential_env_forbidden is True
    assert allowlist.network_forbidden_by_default is True
    assert allowlist.package_install_forbidden_by_default is True
    assert allowlist.destructive_command_forbidden_by_default is True

    rules = LocalRuntimeStaticSafetyRuleRegistry().list_rules()
    rule_ids = {rule.rule_id for rule in rules}
    assert "candidate_must_exist" in rule_ids
    assert "argv_prefix_must_match_allowlist" in rule_ids
    assert "local_runtime_execution_deferred_to_v0_24_7" in rule_ids

    report = LocalRuntimeSafetyPreflightReportService().build_report(request)
    assert report.version == "v0.24.6"
    assert report.static_safety_checked is True
    assert report.preflight_checked is True
    assert report.ready_for_v0_24_7 is True
    assert report.ready_for_v0_25 is False
    assert report.execution_allowed_now is False
    assert report.execution_gate_opened is False
    assert report.local_command_executed is False
    assert report.process_spawned is False
    assert report.stdout_captured is False
    assert report.stderr_captured is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_v0246_allowlist_contains_required_descriptors() -> None:
    policy = LocalRuntimeCommandAllowlistPolicyService().build_allowlist_policy()
    entry_ids = {entry.entry_id for entry in policy.entries}
    assert {
        "python_version_check",
        "git_status_short",
        "git_diff_stat",
        "python_compileall",
        "pytest",
        "ruff_check",
        "mypy",
    }.issubset(entry_ids)
    assert all(not entry.shell_allowed for entry in policy.entries)
    assert all(entry.requires_timeout for entry in policy.entries)
    assert all(entry.requires_output_cap for entry in policy.entries)
    assert all(entry.requires_redaction for entry in policy.entries)


def test_v0246_forbidden_pattern_policy_contains_expected_tools_and_args() -> None:
    policy = LocalRuntimeForbiddenPatternPolicyService().build_forbidden_pattern_policy()
    for tool in ["powershell", "cmd", "bash", "sh", "curl", "wget", "ssh", "scp", "docker", "kubectl", "terraform", "npm", "pip"]:
        assert tool in policy.forbidden_tools
    for arg in ["-c", "install", "uninstall", "delete", "remove", "rm", "rmdir", "del", "reset", "push", "force", "--force", "--global"]:
        assert arg in policy.forbidden_arg_patterns
    assert policy.forbidden_env_patterns


def test_v0246_static_safety_and_preflight_reports_pass_for_default_candidate() -> None:
    request = LocalRuntimeSafetyPreflightRequest(candidate_id="demo")
    static_report = LocalRuntimeStaticSafetyReportService().build_report(request)
    assert static_report.static_safety_status == "passed"
    assert static_report.eligible_for_declared_preflight is True
    assert static_report.command_executed is False
    assert static_report.process_spawned is False
    assert static_report.stdout_captured is False
    assert static_report.stderr_captured is False
    assert static_report.execution_gate_opened is False

    combined = LocalRuntimeSafetyPreflightReportService().build_report(request)
    assert combined.preflight_report.policy.declared_preflight_only is True
    assert combined.preflight_report.policy.live_tool_availability_check_enabled is False
    assert combined.preflight_report.policy.live_version_check_enabled is False
    assert combined.preflight_report.policy.command_execution_for_preflight_enabled is False
    assert combined.preflight_report.policy.filesystem_write_check_enabled is False
    assert combined.preflight_report.preflight_status == "passed"
    assert combined.eligible_for_execution_gate is True


def test_v0246_execution_eligibility_is_for_next_gate_only() -> None:
    combined = LocalRuntimeSafetyPreflightReportService().build_report(LocalRuntimeSafetyPreflightRequest())
    eligibility = combined.execution_eligibilities[0]
    assert eligibility.eligible_for_execution_gate is True
    assert eligibility.eligible_next_version == "v0.24.7"
    assert eligibility.allowed_execution_mode_future == "gated_bounded_local_command"
    assert eligibility.execution_allowed_now is False
    assert eligibility.gate_required is True
    assert eligibility.human_or_policy_gate_required is True
    assert eligibility.authorization_required is True
    assert eligibility.single_use_execution_authorization_required is True
    assert eligibility.timeout_required is True
    assert eligibility.output_cap_required is True
    assert eligibility.redaction_required is True
    assert eligibility.side_effect_scan_required is True
    assert eligibility.command_executed is False
    assert eligibility.process_spawned is False


def test_v0246_needs_input_no_action_and_ocel_pig_ocpx() -> None:
    needs_input = LocalRuntimeSafetyNeedsMoreInputCandidate("candidate:needs", "missing target", ["target"], [])
    no_action = LocalRuntimeSafetyNoActionCandidate("candidate:none", "no action", [])
    assert needs_input.candidate_status == "needs_more_input"
    assert no_action.candidate_status == "no_action"
    assert "local_runtime_safety_preflight_report" in LOCAL_RUNTIME_SAFETY_OBJECT_TYPES
    assert "local_runtime_safety_preflight_report_created" in LOCAL_RUNTIME_SAFETY_EVENT_TYPES
    assert "local_runtime_static_safety_checked" in LOCAL_RUNTIME_SAFETY_EFFECT_TYPES
    service = LocalRuntimeSafetyPreflightReportService()
    assert service.build_pig_report()["subject"] == "local_runtime_static_safety_preflight"
    assert service.build_ocpx_projection()["state"] == "local_runtime_command_candidate_safety_preflight_checked"
