import inspect

import chanta_core.internal_provider.local_runtime_output_failure as output_module
from chanta_core.internal_provider.local_runtime_output_failure import (
    LocalRuntimeFailureClassificationRuleRegistry,
    LocalRuntimeOutputFailureReportService,
)


def test_output_failure_source_has_no_runtime_execution_paths() -> None:
    source = inspect.getsource(output_module)

    for forbidden in [
        "subprocess.run",
        "subprocess.Popen",
        "os.system",
        "shell=True",
        "command_rerun_performed=True",
        "local_command_executed=True",
        "process_spawned=True",
        "stdout_captured_from_new_process=True",
        "stderr_captured_from_new_process=True",
        "automatic_repair_performed=True",
        "file_mutation_performed=True",
        "patch_applied=True",
        "credential_exposed=True",
        "raw_secret_output=True",
        "raw_output_dumped=True",
        "external_provider_adapter_implemented=True",
        "external_runtime_touched=True",
        "provider_api_call_performed=True",
        "schumpeter_split_introduced=True",
        "growthkernel_dependency_required=True",
        "general_agent_usability_implemented=True",
        "llm_judge_used=True",
        "llm_judge_enabled=True",
        "openai",
        "anthropic",
        "chat.completions",
        "eval(",
    ]:
        assert forbidden not in source


def test_output_failure_report_never_claims_new_capture_or_mutation() -> None:
    report = LocalRuntimeOutputFailureReportService().build_report("execution_report:test")

    assert report.command_rerun_performed is False
    assert report.local_command_executed is False
    assert report.process_spawned is False
    assert report.stdout_captured_from_new_process is False
    assert report.stderr_captured_from_new_process is False
    assert report.automatic_repair_performed is False
    assert report.file_mutation_performed is False
    assert report.patch_applied is False
    assert report.external_provider_adapter_implemented is False
    assert report.raw_output_dumped is False
    assert report.output_summary.raw_output_included is False
    assert report.output_summary.private_full_paths_included is False
    assert report.output_bundle.raw_output_included is False
    assert report.output_bundle.private_full_paths_included is False


def test_next_action_candidates_are_future_only_when_actions_are_needed() -> None:
    report = LocalRuntimeOutputFailureReportService().build_report("execution_report:test")

    assert report.next_action_candidates
    for candidate in report.next_action_candidates:
        assert candidate.executes_now is False
        assert candidate.mutates_files_now is False
        assert candidate.command_rerun_now is False
        assert candidate.candidate_type in {
            "no_action",
            "inspect_output",
            "inspect_file",
            "create_local_runtime_candidate_future",
            "run_static_safety_future",
            "run_preflight_future",
            "run_gated_command_future",
            "create_patch_candidate_future",
            "needs_more_input",
            "blocked",
        }


def test_command_family_names_are_only_classification_rule_text() -> None:
    rules = LocalRuntimeFailureClassificationRuleRegistry().list_rules()
    rule_names = " ".join(rule.rule_id + " " + " ".join(rule.patterns) for rule in rules)

    assert "pytest" in rule_names
    assert "ruff" in rule_names
    assert "mypy" in rule_names
    assert "compileall" in rule_names
