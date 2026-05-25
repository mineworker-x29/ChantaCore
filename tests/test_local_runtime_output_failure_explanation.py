from chanta_core.internal_provider.local_runtime_output_failure import (
    LOCAL_RUNTIME_OUTPUT_EFFECT_TYPES,
    LOCAL_RUNTIME_OUTPUT_EVENT_TYPES,
    LOCAL_RUNTIME_OUTPUT_OBJECT_TYPES,
    LocalRuntimeCompileResultSummary,
    LocalRuntimeDiagnosticFinding,
    LocalRuntimeExitStatusInterpretation,
    LocalRuntimeFailureClassification,
    LocalRuntimeFailureClassificationRule,
    LocalRuntimeFailureClassificationRuleRegistry,
    LocalRuntimeFailureClassificationService,
    LocalRuntimeFailureExplanation,
    LocalRuntimeFailureExplanationService,
    LocalRuntimeGitResultSummary,
    LocalRuntimeLintResultSummary,
    LocalRuntimeNextActionCandidate,
    LocalRuntimeOutputBundle,
    LocalRuntimeOutputFailureReport,
    LocalRuntimeOutputFailureReportService,
    LocalRuntimeOutputInterpretationPolicy,
    LocalRuntimeOutputInterpretationPolicyService,
    LocalRuntimeOutputNeedsMoreInputCandidate,
    LocalRuntimeOutputNoActionCandidate,
    LocalRuntimeOutputSummary,
    LocalRuntimeOutputSummaryService,
    LocalRuntimeSideEffectInterpretation,
    LocalRuntimeSpecializedSummaryService,
    LocalRuntimeTestResultSummary,
    LocalRuntimeTimeoutInterpretation,
    LocalRuntimeTypecheckResultSummary,
)


def _bundle(
    *,
    stdout: str = "",
    stderr: str = "",
    exit_code: int | None = 1,
    timed_out: bool = False,
    category: str | None = "test",
) -> LocalRuntimeOutputBundle:
    return LocalRuntimeOutputBundle(
        bundle_id="bundle:test",
        execution_report_id="execution_report:test",
        run_id="run:test",
        process_result_ref={"run_status": "completed"},
        stdout_capture_ref={"truncated": False},
        stderr_capture_ref={"truncated": False},
        side_effect_scan_ref=None,
        command_category=category,
        exit_code=exit_code,
        timed_out=timed_out,
        stdout_excerpt=stdout,
        stderr_excerpt=stderr,
        output_bounded=True,
        output_redacted=True,
    )


def test_output_failure_models_build() -> None:
    policy = LocalRuntimeOutputInterpretationPolicyService().build_policy()
    bundle = _bundle(stdout="1 failed in 0.12s")
    summary = LocalRuntimeOutputSummaryService().build_summary(bundle, policy)
    classification = LocalRuntimeFailureClassificationService().classify(
        bundle,
        summary,
        LocalRuntimeFailureClassificationRuleRegistry().list_rules(),
    )
    explanation = LocalRuntimeFailureExplanationService().explain(classification, summary)

    assert isinstance(policy, LocalRuntimeOutputInterpretationPolicy)
    assert isinstance(bundle, LocalRuntimeOutputBundle)
    assert isinstance(summary, LocalRuntimeOutputSummary)
    assert isinstance(classification, LocalRuntimeFailureClassification)
    assert isinstance(explanation, LocalRuntimeFailureExplanation)
    assert isinstance(LocalRuntimeDiagnosticFinding("finding:test", "info", "ok", "ok", None, [], None), LocalRuntimeDiagnosticFinding)
    assert isinstance(LocalRuntimeExitStatusInterpretation("exit:test", "run:test", 0, "success", "ok", []), LocalRuntimeExitStatusInterpretation)
    assert isinstance(LocalRuntimeTimeoutInterpretation("timeout:test", "run:test", False, 30, "not_timed_out", "ok", []), LocalRuntimeTimeoutInterpretation)
    assert isinstance(LocalRuntimeTestResultSummary("test:test", bundle.bundle_id, True, 1, 0, 0, 0, None, [], "ready", []), LocalRuntimeTestResultSummary)
    assert isinstance(LocalRuntimeLintResultSummary("lint:test", bundle.bundle_id, False, None, [], [], "unknown", []), LocalRuntimeLintResultSummary)
    assert isinstance(LocalRuntimeTypecheckResultSummary("type:test", bundle.bundle_id, False, None, [], [], "unknown", []), LocalRuntimeTypecheckResultSummary)
    assert isinstance(LocalRuntimeCompileResultSummary("compile:test", bundle.bundle_id, False, None, [], [], "unknown", []), LocalRuntimeCompileResultSummary)
    assert isinstance(LocalRuntimeGitResultSummary("git:test", bundle.bundle_id, False, None, None, None, None, "unknown", []), LocalRuntimeGitResultSummary)
    assert isinstance(LocalRuntimeSideEffectInterpretation("side:test", None, "clean", 0, 0, [], "clean", []), LocalRuntimeSideEffectInterpretation)
    assert isinstance(LocalRuntimeNextActionCandidate("next:test", "report:test", "inspect_output", "inspect", "rationale", None, True), LocalRuntimeNextActionCandidate)
    assert isinstance(LocalRuntimeOutputNeedsMoreInputCandidate("needs:test", "missing", ["run_id"], []), LocalRuntimeOutputNeedsMoreInputCandidate)
    assert isinstance(LocalRuntimeOutputNoActionCandidate("none:test", "success", []), LocalRuntimeOutputNoActionCandidate)


def test_policy_is_read_only_and_non_executing() -> None:
    policy = LocalRuntimeOutputInterpretationPolicyService().build_policy()

    assert policy.version == "v0.24.8"
    assert policy.provider_id == "local_runtime_provider"
    assert policy.read_only is True
    assert policy.interpret_existing_output_only is True
    assert policy.command_execution_enabled is False
    assert policy.command_rerun_enabled is False
    assert policy.subprocess_enabled is False
    assert policy.shell_enabled is False
    assert policy.automatic_repair_enabled is False
    assert policy.file_mutation_enabled is False
    assert policy.patch_application_enabled is False
    assert policy.raw_output_dump_enabled is False
    assert policy.bounded_output_required is True
    assert policy.redaction_required is True
    assert policy.private_path_sanitization_required is True
    assert policy.llm_judge_enabled is False


def test_required_classification_rules_exist() -> None:
    rules = LocalRuntimeFailureClassificationRuleRegistry().list_rules()
    rule_ids = {rule.rule_id for rule in rules}

    assert isinstance(rules[0], LocalRuntimeFailureClassificationRule)
    assert {
        "exit_code_zero_success",
        "nonzero_exit_command_failed",
        "timeout_command_timed_out",
        "missing_executable_or_command_not_found",
        "pytest_failed_pattern",
        "pytest_no_tests_pattern",
        "ruff_found_issues_pattern",
        "mypy_error_pattern",
        "compileall_error_pattern",
        "git_not_repository_pattern",
        "git_dirty_status_pattern",
        "permission_denied_pattern",
        "dependency_missing_pattern",
        "unexpected_side_effect_pattern",
        "output_truncated_pattern",
        "output_redacted_pattern",
    }.issubset(rule_ids)
    assert all(rule.enabled for rule in rules)


def test_failure_classification_patterns_are_deterministic() -> None:
    service = LocalRuntimeFailureClassificationService()
    summary_service = LocalRuntimeOutputSummaryService()
    policy = LocalRuntimeOutputInterpretationPolicyService().build_policy()
    rules = LocalRuntimeFailureClassificationRuleRegistry().list_rules()

    cases = [
        (_bundle(stdout="", exit_code=0), "success"),
        (_bundle(stdout="", exit_code=2), "command_failed"),
        (_bundle(stderr="No such file or directory", exit_code=1), "missing_executable"),
        (_bundle(stdout="1 failed, 2 passed in 0.10s", exit_code=1), "test_failure"),
        (_bundle(stdout="no tests ran in 0.01s", exit_code=5), "configuration_error"),
        (_bundle(stdout="Found 2 errors.", exit_code=1, category="lint"), "lint_failure"),
        (_bundle(stderr="main.py:1: error: incompatible type", exit_code=1, category="typecheck"), "typecheck_failure"),
        (_bundle(stderr="SyntaxError: invalid syntax", exit_code=1, category="compile_check"), "compile_failure"),
        (_bundle(stderr="fatal: not a git repository", exit_code=128, category="repo_status"), "git_not_repository"),
        (_bundle(stdout=" M src/example.py", exit_code=0, category="repo_status"), "git_state_dirty"),
        (_bundle(stderr="permission denied", exit_code=1), "permission_error"),
        (_bundle(stderr="No module named missing_pkg", exit_code=1), "dependency_missing"),
        (_bundle(stdout="", exit_code=None, timed_out=True), "command_timed_out"),
    ]
    for bundle, expected in cases:
        summary = summary_service.build_summary(bundle, policy)
        classification = service.classify(bundle, summary, rules)
        assert classification.primary_failure_type == expected
        assert classification.deterministic is True
        assert classification.llm_judge_used is False


def test_specialized_summaries_degrade_without_hallucinated_counts() -> None:
    service = LocalRuntimeSpecializedSummaryService()

    test_summary = service.summarize_test_result(_bundle(stdout="3 failed, 7 passed, 1 skipped in 1.23s"))
    lint_summary = service.summarize_lint_result(_bundle(stdout="src/a.py:1:1: F401 unused import", category="lint"))
    type_summary = service.summarize_typecheck_result(_bundle(stderr="src/a.py:1: error: bad [attr-defined]\nFound 1 error in 1 file", category="typecheck"))
    compile_summary = service.summarize_compile_result(_bundle(stderr="*** Error compiling 'a.py'...\nSyntaxError: bad", category="compile_check"))
    git_summary = service.summarize_git_result(_bundle(stdout=" M src/a.py\n?? src/b.py", category="repo_status", exit_code=0))
    unknown_test = service.summarize_test_result(_bundle(stdout="unstructured", category="test"))

    assert test_summary.failed_count == 3
    assert test_summary.passed_count == 7
    assert lint_summary.rule_codes == ["F401"]
    assert type_summary.error_count == 1
    assert "src/a.py" in type_summary.files_with_errors
    assert compile_summary.compile_success is False
    assert git_summary.dirty is True
    assert git_summary.changed_file_count == 2
    assert unknown_test.summary_status in {"partial", "unknown"}


def test_output_failure_report_builds_with_safety_flags_false() -> None:
    report = LocalRuntimeOutputFailureReportService().build_report("execution_report:test")

    assert isinstance(report, LocalRuntimeOutputFailureReport)
    assert report.version == "v0.24.8"
    assert report.ready_for_v0_24_9 is True
    assert report.ready_for_v0_25 is False
    assert report.output_interpreted is True
    assert report.failure_explained is True
    assert report.command_rerun_performed is False
    assert report.local_command_executed is False
    assert report.process_spawned is False
    assert report.stdout_captured_from_new_process is False
    assert report.stderr_captured_from_new_process is False
    assert report.automatic_repair_performed is False
    assert report.file_mutation_performed is False
    assert report.patch_applied is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_output_dumped is False
    assert report.llm_judge_used is False
    assert all(candidate.executes_now is False for candidate in report.next_action_candidates)
    assert all(candidate.mutates_files_now is False for candidate in report.next_action_candidates)


def test_ocel_pig_ocpx_coverage_exists() -> None:
    service = LocalRuntimeOutputFailureReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "local_runtime_output_failure_report" in LOCAL_RUNTIME_OUTPUT_OBJECT_TYPES
    assert "local_runtime_failure_explained" in LOCAL_RUNTIME_OUTPUT_EVENT_TYPES
    assert "local_runtime_failure_explained" in LOCAL_RUNTIME_OUTPUT_EFFECT_TYPES
    assert pig["version"] == "v0.24.8"
    assert pig["subject"] == "local_runtime_output_failure_explanation"
    assert pig["safety_boundary"]["command_rerun_performed"] is False
    assert pig["safety_boundary"]["file_mutation_performed"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "local_runtime_output_failure_explained"
    assert "LocalRuntimeFailureExplanationState" in ocpx["target_read_models"]
