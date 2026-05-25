from chanta_core.internal_provider.local_runtime_candidate_provider import (
    LocalCommandArgvCandidateService,
    LocalCommandEnvironmentPolicyCandidateService,
    LocalRuntimeCommandCandidateFindingService,
    LocalRuntimeCommandCandidateSetService,
    LocalRuntimeCommandTemplate,
    LocalRuntimeIntentClassifier,
)


def _argv_for(argv: list[str]):
    intent = LocalRuntimeIntentClassifier().classify_intent("custom", {"category": "diagnostic"})
    template = LocalRuntimeCommandTemplate(
        template_id="custom",
        command_category="diagnostic",
        template_name="custom",
        description="custom inert descriptor",
        argv_template=argv,
        allowed_tools=[argv[0]],
        forbidden_args=[],
    )
    return LocalCommandArgvCandidateService().build_argv_candidate(intent, template, {"target": "tests"})


def test_v0245_arg_risk_detection_blocks_forbidden_network_package_destructive_and_credential() -> None:
    assert _argv_for(["python", "-c", "print(1)"]).contains_forbidden_args is True
    assert _argv_for(["curl", "https://example.invalid"]).network_risk_detected is True
    assert _argv_for(["pip", "install", "x"]).package_install_risk_detected is True
    assert _argv_for(["git", "reset", "--force"]).destructive_risk_detected is True
    assert _argv_for(["python", "--token=secret"]).credential_arg_detected is True
    assert _argv_for(["python", "-c", "print(1)"]).candidate_status == "blocked"


def test_v0245_unresolved_placeholder_and_workspace_cwd_boundary() -> None:
    candidate_set = LocalRuntimeCommandCandidateSetService().build_candidate_set({"category": "test"})
    candidate = candidate_set.candidates[0]
    assert candidate.argv_candidate.contains_unresolved_placeholders is True
    assert candidate.candidate_status == "needs_more_input"

    outside_set = LocalRuntimeCommandCandidateSetService().build_candidate_set({"category": "version_check", "workspace_bound": False})
    outside = outside_set.candidates[0]
    assert outside.cwd_candidate.workspace_bound is False
    assert outside.candidate_status == "needs_more_input"


def test_v0245_credential_env_blocks() -> None:
    intent = LocalRuntimeIntentClassifier().classify_intent("show version", {"category": "version_check"})
    env = LocalCommandEnvironmentPolicyCandidateService().build_env_policy_candidate(intent, ["API_TOKEN"])
    assert env.credential_env_detected is True
    assert env.env_policy_status == "blocked"
    assert env.env_values_materialized is False


def test_v0245_findings_cover_required_boundary_types() -> None:
    candidate_set = LocalRuntimeCommandCandidateSetService().build_candidate_set({"category": "test"})
    findings = LocalRuntimeCommandCandidateFindingService().build_findings(candidate_set)
    finding_types = {finding.finding_type for finding in findings}
    assert "unresolved_argv_placeholder" in finding_types
    assert "static_safety_required_next" in finding_types
    assert "preflight_required_next" in finding_types
    assert "execution_gate_required_future" in finding_types


def test_v0245_no_execution_flags_are_set() -> None:
    candidate = LocalRuntimeCommandCandidateSetService().build_candidate_set({"category": "version_check"}).candidates[0]
    assert candidate.static_safety_checked is False
    assert candidate.preflight_checked is False
    assert candidate.execution_gate_opened is False
    assert candidate.local_command_executed is False
    assert candidate.process_spawned is False
    assert candidate.stdout_captured is False
    assert candidate.stderr_captured is False
    assert candidate.credential_exposed is False
    assert candidate.raw_secret_output is False
