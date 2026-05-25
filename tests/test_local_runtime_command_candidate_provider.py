from chanta_core.internal_provider.local_runtime_candidate_provider import (
    LOCAL_RUNTIME_CANDIDATE_EFFECT_TYPES,
    LOCAL_RUNTIME_CANDIDATE_EVENT_TYPES,
    LOCAL_RUNTIME_CANDIDATE_OBJECT_TYPES,
    LocalCommandArgvCandidateService,
    LocalCommandCwdCandidateService,
    LocalCommandEnvironmentPolicyCandidateService,
    LocalCommandOutputPolicyCandidateService,
    LocalCommandSideEffectRiskPreviewService,
    LocalCommandTimeoutPolicyCandidateService,
    LocalRuntimeCommandCandidatePolicyService,
    LocalRuntimeCommandCandidateReportService,
    LocalRuntimeCommandCandidateService,
    LocalRuntimeCommandCandidateSetService,
    LocalRuntimeCommandNeedsMoreInputCandidate,
    LocalRuntimeCommandNoActionCandidate,
    LocalRuntimeCommandTemplateCatalogService,
    LocalRuntimeIntentClassifier,
)
from chanta_core.internal_provider.registry import InternalProviderRegistryReportService


def test_v0245_policy_and_report_builds() -> None:
    policy = LocalRuntimeCommandCandidatePolicyService().build_policy()
    assert policy.version == "v0.24.5"
    assert policy.provider_id == "local_runtime_provider"
    assert policy.candidate_only is True
    assert policy.execution_enabled is False
    assert policy.local_command_execution_enabled is False
    assert policy.shell_allowed is False
    assert policy.shell_string_allowed is False
    assert policy.argv_required is True
    assert policy.cwd_required is True
    assert policy.workspace_bound_cwd_required is True
    assert policy.timeout_policy_required is True
    assert policy.output_policy_required is True
    assert policy.side_effect_risk_preview_required is True
    assert policy.static_safety_required_next is True
    assert policy.preflight_required_next is True
    assert policy.execution_gate_required_future is True
    assert policy.network_commands_forbidden is True
    assert policy.package_install_forbidden is True
    assert policy.destructive_commands_forbidden is True
    assert policy.credential_env_forbidden is True
    assert policy.secret_output_forbidden is True

    report = LocalRuntimeCommandCandidateReportService().build_report({"category": "version_check"})
    assert report.version == "v0.24.5"
    assert report.command_candidate_created is True
    assert report.ready_for_v0_24_6 is True
    assert report.ready_for_v0_25 is False
    assert report.static_safety_checked is False
    assert report.preflight_checked is False
    assert report.execution_gate_opened is False
    assert report.local_command_executed is False
    assert report.process_spawned is False
    assert report.stdout_captured is False
    assert report.stderr_captured is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_v0245_template_catalog_contains_required_inert_templates() -> None:
    catalog = LocalRuntimeCommandTemplateCatalogService().build_catalog()
    template_ids = {template.template_id for template in catalog.templates}
    assert {
        "python_version_check_candidate",
        "git_status_short_candidate",
        "git_diff_stat_candidate",
        "python_compileall_candidate",
        "pytest_candidate",
        "ruff_check_candidate",
        "mypy_candidate",
    }.issubset(template_ids)
    assert catalog.execution_enabled is False
    assert all(template.candidate_only for template in catalog.templates)
    assert all(not template.shell_required for template in catalog.templates)
    assert all(template.static_safety_required for template in catalog.templates)
    assert all(template.preflight_required for template in catalog.templates)
    assert all(template.execution_version == "v0.24.7" for template in catalog.templates)


def test_v0245_intent_classifier_supported_and_unknown() -> None:
    classifier = LocalRuntimeIntentClassifier()
    assert classifier.classify_intent("show python version").command_category == "version_check"
    assert classifier.classify_intent("repo status").command_category == "repo_status"
    assert classifier.classify_intent("run tests", {"target": "tests"}).command_category == "test"
    assert classifier.classify_intent("lint source", {"target": "."}).command_category == "lint"
    assert classifier.classify_intent("typecheck package", {"target": "src"}).command_category == "typecheck"
    assert classifier.classify_intent("compile package", {"target": "src"}).command_category == "compile_check"
    assert classifier.classify_intent("diagnostic view").command_category == "diagnostic"
    unknown = classifier.classify_intent("do something unclear")
    assert unknown.command_category == "unknown"
    assert unknown.needs_more_input is True


def test_v0245_candidate_components_build() -> None:
    candidate = LocalRuntimeCommandCandidateService().build_candidate({"category": "test", "target": "tests"})
    assert candidate.intent.command_category == "test"
    assert candidate.argv_candidate is not None
    assert isinstance(candidate.argv_candidate.argv, list)
    assert candidate.argv_candidate.shell_string is None
    assert candidate.argv_candidate.shell_required is False
    assert candidate.argv_candidate.shell_allowed is False
    assert candidate.cwd_candidate is not None
    assert candidate.cwd_candidate.workspace_bound is True
    assert candidate.cwd_candidate.private_full_path_output is False
    assert candidate.env_policy_candidate.inherit_environment is False
    assert candidate.env_policy_candidate.env_values_materialized is False
    assert candidate.timeout_policy_candidate.timeout_required is True
    assert candidate.output_policy_candidate.raw_output_allowed is False
    assert candidate.output_policy_candidate.redact_secret_like_output is True
    assert candidate.side_effect_risk_preview.requires_static_safety is True
    assert candidate.side_effect_risk_preview.requires_preflight is True
    assert candidate.side_effect_risk_preview.requires_execution_gate is True
    assert candidate.candidate_status == "ready_for_static_safety"

    candidate_set = LocalRuntimeCommandCandidateSetService().build_candidate_set({"category": "test", "target": "tests"})
    assert candidate_set.candidate_count == 1
    assert candidate_set.ready_for_static_safety_count == 1


def test_v0245_needs_more_input_and_no_action_candidates_build() -> None:
    needs_input = LocalRuntimeCommandNeedsMoreInputCandidate(
        candidate_id="candidate:needs_input",
        reason="target missing",
        missing_inputs=["target_path"],
        evidence_refs=[],
    )
    no_action = LocalRuntimeCommandNoActionCandidate(
        candidate_id="candidate:no_action",
        reason="no action requested",
        evidence_refs=[],
    )
    assert needs_input.candidate_status == "needs_more_input"
    assert needs_input.local_command_executed is False
    assert no_action.candidate_status == "no_action"
    assert no_action.local_command_executed is False


def test_v0245_local_runtime_provider_declared_in_registry() -> None:
    report = InternalProviderRegistryReportService().build_report().to_dict()
    surfaces = report["registry"]["capability_surfaces"]
    assert any(surface["provider_id"] == "internal_provider:local_runtime_provider" for surface in surfaces)


def test_v0245_ocel_mapping_and_pig_ocpx_exist() -> None:
    assert "local_runtime_command_candidate_report" in LOCAL_RUNTIME_CANDIDATE_OBJECT_TYPES
    assert "local_runtime_command_candidate_report_created" in LOCAL_RUNTIME_CANDIDATE_EVENT_TYPES
    assert "local_command_candidate_created" in LOCAL_RUNTIME_CANDIDATE_EFFECT_TYPES
    service = LocalRuntimeCommandCandidateReportService()
    assert service.build_pig_report()["subject"] == "local_runtime_command_candidate_provider"
    assert service.build_ocpx_projection()["state"] == "local_runtime_command_candidate_created"
