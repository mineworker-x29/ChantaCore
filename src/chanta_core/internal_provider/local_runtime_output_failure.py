from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
import time
from typing import Any

from chanta_core.internal_provider.gated_local_runtime_execution import (
    LocalRuntimeExecutionBoundaryReport,
    LocalRuntimeExecutionBoundaryReportService,
    LocalRuntimeOutputCapture,
    LocalRuntimeSideEffectScan,
)


LOCAL_RUNTIME_OUTPUT_VERSION = "v0.24.8"
LOCAL_RUNTIME_OUTPUT_VERSION_NAME = "Local Runtime Output / Failure Explanation"
LOCAL_RUNTIME_OUTPUT_KOREAN_NAME = "로컬 런타임 출력·실패 설명 Provider"
LOCAL_RUNTIME_OUTPUT_NEXT_STEP = "v0.24.9 Internal Provider Consolidation"
LOCAL_RUNTIME_PROVIDER_ID = "local_runtime_provider"

LOCAL_RUNTIME_OUTPUT_OBJECT_TYPES = [
    "local_runtime_output_interpretation_policy",
    "local_runtime_output_bundle",
    "local_runtime_output_summary",
    "local_runtime_failure_classification_rule",
    "local_runtime_failure_classification",
    "local_runtime_failure_explanation",
    "local_runtime_diagnostic_finding",
    "local_runtime_exit_status_interpretation",
    "local_runtime_timeout_interpretation",
    "local_runtime_test_result_summary",
    "local_runtime_lint_result_summary",
    "local_runtime_typecheck_result_summary",
    "local_runtime_compile_result_summary",
    "local_runtime_git_result_summary",
    "local_runtime_side_effect_interpretation",
    "local_runtime_next_action_candidate",
    "local_runtime_output_failure_report",
    "local_runtime_output_needs_more_input_candidate",
    "local_runtime_output_no_action_candidate",
    "local_runtime_execution_boundary_report",
    "bounded_local_command_run",
    "local_runtime_process_result",
    "local_runtime_output_capture",
    "local_runtime_side_effect_scan",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

LOCAL_RUNTIME_OUTPUT_EVENT_TYPES = [
    "local_runtime_output_interpretation_requested",
    "local_runtime_output_interpretation_policy_created",
    "local_runtime_output_bundle_created",
    "local_runtime_output_summary_created",
    "local_runtime_failure_classification_rules_loaded",
    "local_runtime_failure_classified",
    "local_runtime_failure_explained",
    "local_runtime_test_result_summarized",
    "local_runtime_lint_result_summarized",
    "local_runtime_typecheck_result_summarized",
    "local_runtime_compile_result_summarized",
    "local_runtime_git_result_summarized",
    "local_runtime_side_effect_interpreted",
    "local_runtime_next_action_candidate_created",
    "local_runtime_output_failure_report_created",
    "local_runtime_output_failure_warning_created",
    "local_runtime_output_failure_blocked",
]

LOCAL_RUNTIME_OUTPUT_RELATION_TYPES = [
    "interprets_local_runtime_output",
    "uses_local_runtime_execution_boundary_report",
    "uses_bounded_local_command_run",
    "uses_local_runtime_process_result",
    "uses_local_runtime_output_capture",
    "uses_local_runtime_side_effect_scan",
    "summarizes_local_runtime_output",
    "classifies_local_runtime_failure",
    "explains_local_runtime_failure",
    "summarizes_test_result",
    "summarizes_lint_result",
    "summarizes_typecheck_result",
    "summarizes_compile_result",
    "summarizes_git_result",
    "interprets_side_effect_scan",
    "creates_next_action_candidate",
    "candidate_does_not_execute_now",
    "candidate_does_not_mutate_files_now",
    "not_command_rerun",
    "not_local_command_executed",
    "not_process_spawned",
    "not_subprocess_called",
    "not_file_mutated",
    "not_patch_applied",
    "prevents_credential_exposure",
    "defers_general_agent_usability_to_v0_25",
    "prepares_internal_provider_consolidation",
    "defers_consolidation_to_v0_24_9",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_local_runtime_execution_boundary_report",
]

LOCAL_RUNTIME_OUTPUT_EFFECT_TYPES = [
    "read_only_observation",
    "local_runtime_output_interpreted",
    "local_runtime_failure_classified",
    "local_runtime_failure_explained",
    "local_runtime_next_action_candidate_created",
    "state_candidate_created",
]

LOCAL_RUNTIME_OUTPUT_FORBIDDEN_EFFECT_TYPES = [
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "process_spawned",
    "subprocess_called",
    "stdout_captured_from_new_process",
    "stderr_captured_from_new_process",
    "unrestricted_shell_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "file_written",
    "file_edited",
    "file_deleted",
    "patch_applied",
    "automatic_repair_performed",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "raw_secret_output",
    "raw_output_dumped",
    "external_provider_called",
    "general_agent_usability_invoked",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_id(value: str | None) -> str:
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", value or "none")[:120] or "none"


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _bounded_lines(text: str | None, max_chars: int, max_lines: int = 20) -> list[str]:
    if not text:
        return []
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    return [line[: max_chars // max(1, max_lines)] for line in lines[:max_lines]]


@dataclass
class LocalRuntimeOutputInterpretationPolicy:
    policy_id: str
    version: str = LOCAL_RUNTIME_OUTPUT_VERSION
    provider_id: str = LOCAL_RUNTIME_PROVIDER_ID
    read_only: bool = True
    interpret_existing_output_only: bool = True
    command_execution_enabled: bool = False
    command_rerun_enabled: bool = False
    subprocess_enabled: bool = False
    shell_enabled: bool = False
    automatic_repair_enabled: bool = False
    file_mutation_enabled: bool = False
    patch_application_enabled: bool = False
    raw_output_dump_enabled: bool = False
    bounded_output_required: bool = True
    redaction_required: bool = True
    private_path_sanitization_required: bool = True
    max_summary_chars: int = 20000
    max_finding_count: int = 200
    max_next_action_candidates: int = 20
    llm_judge_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputBundle:
    bundle_id: str
    execution_report_id: str | None
    run_id: str | None
    process_result_ref: dict[str, Any] | None
    stdout_capture_ref: dict[str, Any] | None
    stderr_capture_ref: dict[str, Any] | None
    side_effect_scan_ref: dict[str, Any] | None
    command_category: str | None
    exit_code: int | None
    timed_out: bool
    stdout_excerpt: str | None
    stderr_excerpt: str | None
    output_bounded: bool
    output_redacted: bool
    version: str = LOCAL_RUNTIME_OUTPUT_VERSION
    raw_output_included: bool = False
    raw_secret_output: bool = False
    private_full_paths_included: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputSummary:
    summary_id: str
    bundle_id: str
    command_category: str | None
    run_status: str
    exit_code: int | None
    timed_out: bool
    stdout_present: bool
    stderr_present: bool
    stdout_truncated: bool
    stderr_truncated: bool
    output_redacted: bool
    high_level_summary: str
    key_lines: list[str]
    omitted_reason: str | None
    raw_output_included: bool = False
    raw_secret_output: bool = False
    private_full_paths_included: bool = False
    summary_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeFailureClassificationRule:
    rule_id: str
    rule_name: str
    command_category: str | None
    pattern_type: str
    patterns: list[str]
    failure_type: str
    severity: str
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeFailureClassification:
    classification_id: str
    bundle_id: str
    primary_failure_type: str
    secondary_failure_types: list[str]
    severity: str
    confidence: str
    matched_rules: list[dict[str, Any]]
    deterministic: bool = True
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeFailureExplanation:
    explanation_id: str
    bundle_id: str
    classification_id: str
    explanation_text: str
    likely_cause: str | None
    supporting_evidence: list[str]
    uncertainty_notes: list[str]
    not_claimed: list[str]
    recommended_next_step_category: str
    automatic_repair_performed: bool = False
    command_rerun_performed: bool = False
    file_mutation_performed: bool = False
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeDiagnosticFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    source_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExitStatusInterpretation:
    interpretation_id: str
    run_id: str | None
    exit_code: int | None
    exit_status_category: str
    message: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeTimeoutInterpretation:
    interpretation_id: str
    run_id: str | None
    timed_out: bool
    timeout_seconds: int | None
    timeout_category: str
    message: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeTestResultSummary:
    summary_id: str
    bundle_id: str
    detected: bool
    passed_count: int | None
    failed_count: int | None
    error_count: int | None
    skipped_count: int | None
    duration_text: str | None
    failed_test_names: list[str]
    summary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeLintResultSummary:
    summary_id: str
    bundle_id: str
    detected: bool
    issue_count: int | None
    rule_codes: list[str]
    files_with_issues: list[str]
    summary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeTypecheckResultSummary:
    summary_id: str
    bundle_id: str
    detected: bool
    error_count: int | None
    files_with_errors: list[str]
    error_codes: list[str]
    summary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCompileResultSummary:
    summary_id: str
    bundle_id: str
    detected: bool
    compile_success: bool | None
    failed_files: list[str]
    error_lines: list[str]
    summary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeGitResultSummary:
    summary_id: str
    bundle_id: str
    detected: bool
    is_git_repository: bool | None
    dirty: bool | None
    changed_file_count: int | None
    diff_stat_excerpt: str | None
    summary_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeSideEffectInterpretation:
    interpretation_id: str
    side_effect_scan_ref: dict[str, Any] | None
    side_effect_status: str
    allowed_changes_count: int
    unexpected_changes_count: int
    changed_files_sanitized: list[dict[str, Any]]
    message: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeNextActionCandidate:
    candidate_id: str
    source_report_id: str
    candidate_type: str
    description: str
    rationale: str
    required_future_track: str | None
    requires_human_or_policy_gate: bool
    version: str = LOCAL_RUNTIME_OUTPUT_VERSION
    executes_now: bool = False
    mutates_files_now: bool = False
    command_rerun_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputFailureReport:
    report_id: str
    created_at: str
    policy: LocalRuntimeOutputInterpretationPolicy
    output_bundle: LocalRuntimeOutputBundle
    output_summary: LocalRuntimeOutputSummary
    exit_status_interpretation: LocalRuntimeExitStatusInterpretation | None
    timeout_interpretation: LocalRuntimeTimeoutInterpretation | None
    failure_classification: LocalRuntimeFailureClassification
    failure_explanation: LocalRuntimeFailureExplanation
    test_result_summary: LocalRuntimeTestResultSummary | None
    lint_result_summary: LocalRuntimeLintResultSummary | None
    typecheck_result_summary: LocalRuntimeTypecheckResultSummary | None
    compile_result_summary: LocalRuntimeCompileResultSummary | None
    git_result_summary: LocalRuntimeGitResultSummary | None
    side_effect_interpretation: LocalRuntimeSideEffectInterpretation | None
    next_action_candidates: list[LocalRuntimeNextActionCandidate]
    findings: list[LocalRuntimeDiagnosticFinding]
    report_status: str
    ready_for_v0_24_9: bool
    output_interpreted: bool
    failure_explained: bool
    version: str = LOCAL_RUNTIME_OUTPUT_VERSION
    ready_for_v0_25: bool = False
    command_rerun_performed: bool = False
    local_command_executed: bool = False
    process_spawned: bool = False
    stdout_captured_from_new_process: bool = False
    stderr_captured_from_new_process: bool = False
    automatic_repair_performed: bool = False
    file_mutation_performed: bool = False
    patch_applied: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_output_dumped: bool = False
    llm_judge_used: bool = False
    next_required_step: str = LOCAL_RUNTIME_OUTPUT_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until bounded run output, side-effect scan, output policy, or failure classification rules change."

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputNeedsMoreInputCandidate:
    candidate_id: str
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "needs_more_input"
    executes_now: bool = False
    mutates_files_now: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputNoActionCandidate:
    candidate_id: str
    reason: str
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "no_action"
    executes_now: bool = False
    mutates_files_now: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class LocalRuntimeOutputSourceService:
    def __init__(self, execution_report: LocalRuntimeExecutionBoundaryReport | None = None) -> None:
        self.execution_report = execution_report

    def load_execution_boundary_report(self, report_id: str | None = None) -> LocalRuntimeExecutionBoundaryReport:
        if self.execution_report is not None:
            return self.execution_report
        return LocalRuntimeExecutionBoundaryReportService().build_report(run=False)

    def load_bounded_run(self, run_id: str | None = None) -> Any | None:
        return self.load_execution_boundary_report().bounded_run

    def load_process_result(self, result_id: str | None = None) -> Any | None:
        return self.load_execution_boundary_report().process_result

    def load_output_captures(self, run_id: str | None = None) -> list[LocalRuntimeOutputCapture]:
        return self.load_execution_boundary_report().output_captures

    def load_side_effect_scan(self, run_id: str | None = None) -> LocalRuntimeSideEffectScan | None:
        return self.load_execution_boundary_report().side_effect_scan


class LocalRuntimeOutputInterpretationPolicyService:
    def build_policy(self) -> LocalRuntimeOutputInterpretationPolicy:
        return LocalRuntimeOutputInterpretationPolicy(
            policy_id="local_runtime_output_interpretation_policy_v0_24_8",
            evidence_refs=[{"type": "read_only_existing_output_only"}],
        )


class LocalRuntimeOutputBundleService:
    def build_output_bundle(
        self,
        execution_report: LocalRuntimeExecutionBoundaryReport,
    ) -> LocalRuntimeOutputBundle:
        stdout_capture = next((capture for capture in execution_report.output_captures if capture.stream == "stdout"), None)
        stderr_capture = next((capture for capture in execution_report.output_captures if capture.stream == "stderr"), None)
        run = execution_report.bounded_run
        result = execution_report.process_result
        command_category = None
        if run and run.process_spec and run.process_spec.argv:
            argv_text = " ".join(run.process_spec.argv)
            if "pytest" in argv_text:
                command_category = "test"
            elif "ruff" in argv_text:
                command_category = "lint"
            elif "mypy" in argv_text:
                command_category = "typecheck"
            elif "compileall" in argv_text:
                command_category = "compile_check"
            elif run.process_spec.argv[0] == "git":
                command_category = "repo_status"
            else:
                command_category = "version_check"
        return LocalRuntimeOutputBundle(
            bundle_id=f"local_runtime_output_bundle:{_safe_id(execution_report.report_id)}",
            execution_report_id=execution_report.report_id,
            run_id=run.run_id if run else None,
            process_result_ref={"result_id": result.result_id} if result else None,
            stdout_capture_ref={"capture_id": stdout_capture.capture_id} if stdout_capture else None,
            stderr_capture_ref={"capture_id": stderr_capture.capture_id} if stderr_capture else None,
            side_effect_scan_ref={"scan_id": execution_report.side_effect_scan.scan_id} if execution_report.side_effect_scan else None,
            command_category=command_category,
            exit_code=result.exit_code if result else None,
            timed_out=bool(result and result.timed_out),
            stdout_excerpt=stdout_capture.text_excerpt if stdout_capture else None,
            stderr_excerpt=stderr_capture.text_excerpt if stderr_capture else None,
            output_bounded=True,
            output_redacted=not execution_report.output_captures or all(capture.redacted or not capture.text_excerpt for capture in execution_report.output_captures),
            evidence_refs=[{"type": "existing_v0_24_7_output_capture"}],
        )


class LocalRuntimeOutputSummaryService:
    def build_summary(self, bundle: LocalRuntimeOutputBundle, policy: LocalRuntimeOutputInterpretationPolicy) -> LocalRuntimeOutputSummary:
        text = "\n".join(part for part in [bundle.stdout_excerpt, bundle.stderr_excerpt] if part)
        key_lines = _bounded_lines(text, policy.max_summary_chars)
        if bundle.timed_out:
            high = "The bounded run timed out; only existing bounded output was interpreted."
        elif bundle.exit_code == 0:
            high = "The bounded run completed successfully."
        elif bundle.exit_code is None:
            high = "No completed process result is available in the existing execution report."
        else:
            high = "The bounded run exited with a nonzero status."
        return LocalRuntimeOutputSummary(
            summary_id=f"local_runtime_output_summary:{_safe_id(bundle.bundle_id)}",
            bundle_id=bundle.bundle_id,
            command_category=bundle.command_category,
            run_status="timeout" if bundle.timed_out else "completed" if bundle.exit_code == 0 else "failed" if bundle.exit_code is not None else "unknown",
            exit_code=bundle.exit_code,
            timed_out=bundle.timed_out,
            stdout_present=bool(bundle.stdout_excerpt),
            stderr_present=bool(bundle.stderr_excerpt),
            stdout_truncated=False,
            stderr_truncated=False,
            output_redacted=bundle.output_redacted,
            high_level_summary=high[: policy.max_summary_chars],
            key_lines=key_lines,
            omitted_reason=None if text else "No existing bounded stdout/stderr capture is available.",
            summary_status="ready" if bundle.output_bounded and bundle.output_redacted else "blocked",
            evidence_refs=[{"type": "bounded_summary"}],
        )


class LocalRuntimeFailureClassificationRuleRegistry:
    def list_rules(self) -> list[LocalRuntimeFailureClassificationRule]:
        specs = [
            ("exit_code_zero_success", "exit code zero", "exit_code", [], "success", "info"),
            ("nonzero_exit_command_failed", "nonzero exit", "exit_code", [], "command_failed", "warning"),
            ("timeout_command_timed_out", "timeout", "timeout", [], "command_timed_out", "warning"),
            ("missing_executable_or_command_not_found", "missing executable", "missing_executable", ["not recognized", "No such file", "not found"], "missing_executable", "warning"),
            ("pytest_failed_pattern", "pytest failed", "stderr_pattern", ["failed", "FAILURES"], "test_failure", "error"),
            ("pytest_no_tests_pattern", "pytest no tests", "stdout_pattern", ["no tests ran"], "configuration_error", "warning"),
            ("ruff_found_issues_pattern", "ruff issues", "stdout_pattern", ["Found ", "error"], "lint_failure", "error"),
            ("mypy_error_pattern", "mypy errors", "stdout_pattern", ["error:", "Found "], "typecheck_failure", "error"),
            ("compileall_error_pattern", "compileall error", "stderr_pattern", ["SyntaxError", "Can't list"], "compile_failure", "error"),
            ("git_not_repository_pattern", "git not repository", "stderr_pattern", ["not a git repository"], "git_not_repository", "warning"),
            ("git_dirty_status_pattern", "git dirty", "stdout_pattern", [" M ", "?? "], "git_state_dirty", "info"),
            ("permission_denied_pattern", "permission denied", "stderr_pattern", ["permission denied", "access is denied"], "permission_error", "error"),
            ("dependency_missing_pattern", "dependency missing", "stderr_pattern", ["No module named", "ModuleNotFoundError"], "dependency_missing", "error"),
            ("unexpected_side_effect_pattern", "unexpected side effect", "side_effect", ["unexpected_changes"], "side_effect_unexpected", "error"),
            ("output_truncated_pattern", "output truncated", "stdout_pattern", ["truncated"], "output_truncated", "warning"),
            ("output_redacted_pattern", "output redacted", "stdout_pattern", ["REDACTED"], "output_redacted", "info"),
        ]
        return [
            LocalRuntimeFailureClassificationRule(
                rule_id=rule_id,
                rule_name=name,
                command_category=None,
                pattern_type=pattern_type,
                patterns=patterns,
                failure_type=failure_type,
                severity=severity,
            )
            for rule_id, name, pattern_type, patterns, failure_type, severity in specs
        ]


class LocalRuntimeFailureClassificationService:
    def classify(
        self,
        bundle: LocalRuntimeOutputBundle,
        output_summary: LocalRuntimeOutputSummary,
        rules: list[LocalRuntimeFailureClassificationRule],
        side_effect_interpretation: LocalRuntimeSideEffectInterpretation | None = None,
    ) -> LocalRuntimeFailureClassification:
        text = "\n".join(part for part in [bundle.stdout_excerpt, bundle.stderr_excerpt] if part).lower()
        matched: list[dict[str, Any]] = []
        if bundle.timed_out:
            matched.append({"rule_id": "timeout_command_timed_out", "failure_type": "command_timed_out"})
        elif bundle.exit_code == 0:
            matched.append({"rule_id": "exit_code_zero_success", "failure_type": "success"})
        elif bundle.exit_code is not None:
            matched.append({"rule_id": "nonzero_exit_command_failed", "failure_type": "command_failed"})
        for rule in rules:
            if rule.patterns and any(pattern.lower() in text for pattern in rule.patterns):
                matched.append({"rule_id": rule.rule_id, "failure_type": rule.failure_type})
        if side_effect_interpretation and side_effect_interpretation.unexpected_changes_count:
            matched.append({"rule_id": "unexpected_side_effect_pattern", "failure_type": "side_effect_unexpected"})
        generic_rule_ids = {"exit_code_zero_success", "nonzero_exit_command_failed"}
        specific_matches = [item for item in matched if item["rule_id"] not in generic_rule_ids]
        preferred_by_category = {
            "test": "test_failure",
            "lint": "lint_failure",
            "typecheck": "typecheck_failure",
            "compile_check": "compile_failure",
            "repo_status": "git_state_dirty",
        }
        preferred_failure = preferred_by_category.get(bundle.command_category or "")
        category_matches = [
            item for item in specific_matches if preferred_failure and item["failure_type"] == preferred_failure
        ]
        if bundle.timed_out:
            primary = "command_timed_out"
        elif bundle.exit_code == 0 and not specific_matches:
            primary = "success"
        elif category_matches:
            primary = category_matches[0]["failure_type"]
        elif specific_matches:
            primary = specific_matches[0]["failure_type"]
        elif matched:
            primary = matched[0]["failure_type"]
        else:
            primary = "unknown"
        secondary = [item["failure_type"] for item in matched if item["failure_type"] != primary]
        severity = "info" if primary in {"success", "git_state_dirty", "output_redacted"} else "warning" if primary in {"unknown", "command_timed_out", "missing_executable", "configuration_error"} else "error"
        confidence = "high" if matched else "low"
        return LocalRuntimeFailureClassification(
            classification_id=f"local_runtime_failure_classification:{_safe_id(bundle.bundle_id)}",
            bundle_id=bundle.bundle_id,
            primary_failure_type=primary,
            secondary_failure_types=secondary,
            severity=severity,
            confidence=confidence,
            matched_rules=matched,
            evidence_refs=[{"type": "deterministic_rules"}],
        )


class LocalRuntimeFailureExplanationService:
    def explain(
        self,
        classification: LocalRuntimeFailureClassification,
        output_summary: LocalRuntimeOutputSummary,
        side_effect_interpretation: LocalRuntimeSideEffectInterpretation | None = None,
    ) -> LocalRuntimeFailureExplanation:
        primary = classification.primary_failure_type
        if primary == "success":
            text = "The existing bounded run result indicates success."
            next_step = "no_action"
            likely = "The command completed with exit code 0."
        elif primary == "unknown":
            text = "The existing bounded output does not contain enough deterministic evidence to classify the result."
            next_step = "inspect_output"
            likely = None
        else:
            text = f"The existing bounded run output matches deterministic classification `{primary}`."
            next_step = "inspect_output"
            likely = f"Matched failure category: {primary}."
        evidence = output_summary.key_lines[:5]
        if side_effect_interpretation:
            evidence.append(side_effect_interpretation.message)
        return LocalRuntimeFailureExplanation(
            explanation_id=f"local_runtime_failure_explanation:{_safe_id(classification.classification_id)}",
            bundle_id=classification.bundle_id,
            classification_id=classification.classification_id,
            explanation_text=text,
            likely_cause=likely,
            supporting_evidence=evidence,
            uncertainty_notes=["This explanation uses existing bounded/redacted output only.", "No command was rerun and no repair was attempted."],
            not_claimed=["No root cause is claimed without matching deterministic evidence.", "No file change or patch was applied."],
            recommended_next_step_category=next_step,
            evidence_refs=[{"type": "deterministic_explanation"}],
        )


class LocalRuntimeSpecializedSummaryService:
    def _text(self, bundle: LocalRuntimeOutputBundle) -> str:
        return "\n".join(part for part in [bundle.stdout_excerpt, bundle.stderr_excerpt] if part)

    def summarize_test_result(self, bundle: LocalRuntimeOutputBundle) -> LocalRuntimeTestResultSummary:
        text = self._text(bundle)
        failed = re.search(r"(\d+)\s+failed", text)
        passed = re.search(r"(\d+)\s+passed", text)
        errors = re.search(r"(\d+)\s+errors?", text)
        skipped = re.search(r"(\d+)\s+skipped", text)
        detected = "pytest" in text.lower() or bool(failed or passed or errors)
        return LocalRuntimeTestResultSummary("test_summary:" + _safe_id(bundle.bundle_id), bundle.bundle_id, detected, int(passed.group(1)) if passed else None, int(failed.group(1)) if failed else None, int(errors.group(1)) if errors else None, int(skipped.group(1)) if skipped else None, None, re.findall(r"FAILED\s+([^\s]+)", text)[:20], "partial" if detected else "unknown")

    def summarize_lint_result(self, bundle: LocalRuntimeOutputBundle) -> LocalRuntimeLintResultSummary:
        text = self._text(bundle)
        codes = sorted(set(re.findall(r"\b([A-Z]\d{3,4})\b", text)))
        files = sorted(set(re.findall(r"([\w./\\-]+\.py)", text)))[:20]
        count = len(codes) if codes else None
        return LocalRuntimeLintResultSummary("lint_summary:" + _safe_id(bundle.bundle_id), bundle.bundle_id, bool(codes or "ruff" in text.lower()), count, codes, files, "partial" if codes else "unknown")

    def summarize_typecheck_result(self, bundle: LocalRuntimeOutputBundle) -> LocalRuntimeTypecheckResultSummary:
        text = self._text(bundle)
        files = sorted(set(re.findall(r"([\w./\\-]+\.py):\d+:", text)))[:20]
        codes = sorted(set(re.findall(r"\[([a-z-]+)\]", text)))[:20]
        count_match = re.search(r"Found\s+(\d+)\s+errors?", text)
        return LocalRuntimeTypecheckResultSummary("typecheck_summary:" + _safe_id(bundle.bundle_id), bundle.bundle_id, bool(files or "mypy" in text.lower()), int(count_match.group(1)) if count_match else None, files, codes, "partial" if files or count_match else "unknown")

    def summarize_compile_result(self, bundle: LocalRuntimeOutputBundle) -> LocalRuntimeCompileResultSummary:
        text = self._text(bundle)
        failed_files = sorted(set(re.findall(r"([\w./\\-]+\.py)", text)))[:20] if "SyntaxError" in text or "Error" in text else []
        return LocalRuntimeCompileResultSummary("compile_summary:" + _safe_id(bundle.bundle_id), bundle.bundle_id, "compileall" in text.lower() or bool(failed_files), False if failed_files else None, failed_files, _bounded_lines(text, 2000, 10), "partial" if failed_files else "unknown")

    def summarize_git_result(self, bundle: LocalRuntimeOutputBundle) -> LocalRuntimeGitResultSummary:
        text = self._text(bundle)
        not_repo = "not a git repository" in text.lower()
        dirty_lines = [line for line in text.splitlines() if line.startswith((" M ", "?? ", "A  ", "D  "))]
        detected = not_repo or bool(dirty_lines) or bundle.command_category == "repo_status"
        return LocalRuntimeGitResultSummary("git_summary:" + _safe_id(bundle.bundle_id), bundle.bundle_id, detected, False if not_repo else None if not detected else True, bool(dirty_lines) if detected else None, len(dirty_lines) if dirty_lines else None, "\n".join(dirty_lines[:20]) or None, "partial" if detected else "unknown")


class LocalRuntimeSideEffectInterpretationService:
    def interpret_side_effect_scan(self, scan: LocalRuntimeSideEffectScan | None) -> LocalRuntimeSideEffectInterpretation:
        if scan is None:
            return LocalRuntimeSideEffectInterpretation(
                "side_effect_interpretation:missing",
                None,
                "unknown",
                0,
                0,
                [],
                "No existing side-effect scan is available.",
            )
        changed = [{"path": item.get("path") or item.get("label") or "sanitized"} for item in scan.changed_files[:20]]
        return LocalRuntimeSideEffectInterpretation(
            interpretation_id=f"side_effect_interpretation:{_safe_id(scan.scan_id)}",
            side_effect_scan_ref={"scan_id": scan.scan_id},
            side_effect_status=scan.side_effect_status,
            allowed_changes_count=scan.allowed_changes_count,
            unexpected_changes_count=scan.unexpected_changes_count,
            changed_files_sanitized=changed,
            message=f"Side-effect scan status is {scan.side_effect_status}.",
            evidence_refs=[{"type": "existing_side_effect_scan"}],
        )


class LocalRuntimeNextActionCandidateService:
    def build_candidates(
        self,
        source_report_id: str,
        classification: LocalRuntimeFailureClassification,
        explanation: LocalRuntimeFailureExplanation,
        policy: LocalRuntimeOutputInterpretationPolicy,
    ) -> list[LocalRuntimeNextActionCandidate]:
        if classification.primary_failure_type == "success":
            specs = [("no_action", "No action is required for a successful bounded run.", None, False)]
        elif classification.primary_failure_type == "unknown":
            specs = [("inspect_output", "Inspect the existing bounded output manually.", None, False), ("needs_more_input", "Provide more context or a specific report id.", None, False)]
        else:
            specs = [
                ("inspect_output", "Inspect bounded output evidence before acting.", None, False),
                ("create_patch_candidate_future", "Create a future patch candidate after human/policy review.", "v0.25+ or later approved repair track", True),
            ]
        return [
            LocalRuntimeNextActionCandidate(
                candidate_id=f"next_action_candidate:{_safe_id(source_report_id)}:{candidate_type}",
                source_report_id=source_report_id,
                candidate_type=candidate_type,
                description=description,
                rationale=explanation.explanation_text,
                required_future_track=future_track,
                requires_human_or_policy_gate=gate,
                evidence_refs=[{"type": "candidate_only_next_action"}],
            )
            for candidate_type, description, future_track, gate in specs[: policy.max_next_action_candidates]
        ]


class LocalRuntimeDiagnosticFindingService:
    def build_findings(
        self,
        summary: LocalRuntimeOutputSummary,
        classification: LocalRuntimeFailureClassification,
        side_effect: LocalRuntimeSideEffectInterpretation | None,
    ) -> list[LocalRuntimeDiagnosticFinding]:
        findings: list[LocalRuntimeDiagnosticFinding] = []
        finding_type = {
            "success": "command_succeeded",
            "command_failed": "command_failed",
            "command_timed_out": "command_timed_out",
            "missing_executable": "missing_executable",
            "test_failure": "test_failure_detected",
            "lint_failure": "lint_failure_detected",
            "typecheck_failure": "typecheck_failure_detected",
            "compile_failure": "compile_failure_detected",
            "git_state_dirty": "git_state_dirty",
            "git_not_repository": "git_not_repository",
        }.get(classification.primary_failure_type, "ok" if classification.primary_failure_type == "unknown" else "command_failed")
        findings.append(LocalRuntimeDiagnosticFinding("diagnostic_finding:" + finding_type, classification.severity, finding_type, f"Primary classification: {classification.primary_failure_type}.", {"bundle_id": summary.bundle_id}, [], "Withdraw if bounded output changes."))
        if summary.stdout_present:
            findings.append(LocalRuntimeDiagnosticFinding("diagnostic_finding:stdout_present", "info", "stdout_present", "Existing stdout capture is present.", {"bundle_id": summary.bundle_id}, [], None))
        if summary.stderr_present:
            findings.append(LocalRuntimeDiagnosticFinding("diagnostic_finding:stderr_present", "warning", "stderr_present", "Existing stderr capture is present.", {"bundle_id": summary.bundle_id}, [], None))
        if summary.output_redacted:
            findings.append(LocalRuntimeDiagnosticFinding("diagnostic_finding:output_redacted", "info", "output_redacted", "Output remains redacted or no output exists.", {"bundle_id": summary.bundle_id}, [], None))
        if side_effect and side_effect.unexpected_changes_count:
            findings.append(LocalRuntimeDiagnosticFinding("diagnostic_finding:unexpected_side_effect_detected", "error", "unexpected_side_effect_detected", "Unexpected side effect was detected in existing scan.", side_effect.side_effect_scan_ref, [], "Withdraw if side-effect scan changes."))
        return findings


class LocalRuntimeOutputFailureReportService:
    def __init__(self, source_service: LocalRuntimeOutputSourceService | None = None) -> None:
        self.source_service = source_service or LocalRuntimeOutputSourceService()

    def build_report(self, report_id: str | None = None) -> LocalRuntimeOutputFailureReport:
        execution_report = self.source_service.load_execution_boundary_report(report_id)
        policy = LocalRuntimeOutputInterpretationPolicyService().build_policy()
        bundle = LocalRuntimeOutputBundleService().build_output_bundle(execution_report)
        summary = LocalRuntimeOutputSummaryService().build_summary(bundle, policy)
        side_effect = LocalRuntimeSideEffectInterpretationService().interpret_side_effect_scan(execution_report.side_effect_scan)
        rules = LocalRuntimeFailureClassificationRuleRegistry().list_rules()
        classification = LocalRuntimeFailureClassificationService().classify(bundle, summary, rules, side_effect)
        explanation = LocalRuntimeFailureExplanationService().explain(classification, summary, side_effect)
        specialized = LocalRuntimeSpecializedSummaryService()
        test_summary = specialized.summarize_test_result(bundle)
        lint_summary = specialized.summarize_lint_result(bundle)
        typecheck_summary = specialized.summarize_typecheck_result(bundle)
        compile_summary = specialized.summarize_compile_result(bundle)
        git_summary = specialized.summarize_git_result(bundle)
        next_actions = LocalRuntimeNextActionCandidateService().build_candidates(execution_report.report_id, classification, explanation, policy)
        findings = LocalRuntimeDiagnosticFindingService().build_findings(summary, classification, side_effect)
        status = "blocked" if summary.summary_status == "blocked" else "warning" if classification.severity in {"warning", "error"} else "passed"
        exit_category = "timeout" if bundle.timed_out else "success" if bundle.exit_code == 0 else "nonzero_failure" if bundle.exit_code is not None else "unknown"
        timeout_category = "timed_out_with_partial_output" if bundle.timed_out and (bundle.stdout_excerpt or bundle.stderr_excerpt) else "timed_out_cleanly" if bundle.timed_out else "not_timed_out"
        return LocalRuntimeOutputFailureReport(
            report_id=f"local_runtime_output_failure_report:{_safe_id(execution_report.report_id)}",
            created_at=_utc_now(),
            policy=policy,
            output_bundle=bundle,
            output_summary=summary,
            exit_status_interpretation=LocalRuntimeExitStatusInterpretation("exit_status:" + _safe_id(bundle.run_id), bundle.run_id, bundle.exit_code, exit_category, f"Exit status category is {exit_category}."),
            timeout_interpretation=LocalRuntimeTimeoutInterpretation("timeout:" + _safe_id(bundle.run_id), bundle.run_id, bundle.timed_out, None, timeout_category, f"Timeout category is {timeout_category}."),
            failure_classification=classification,
            failure_explanation=explanation,
            test_result_summary=test_summary,
            lint_result_summary=lint_summary,
            typecheck_result_summary=typecheck_summary,
            compile_result_summary=compile_summary,
            git_result_summary=git_summary,
            side_effect_interpretation=side_effect,
            next_action_candidates=next_actions,
            findings=findings,
            report_status=status,
            ready_for_v0_24_9=True,
            output_interpreted=True,
            failure_explained=True,
            limitations=["No command is rerun.", "No repair or file mutation is performed.", "Summaries use existing bounded/redacted output only."],
            withdrawal_conditions=["Withdraw if output is no longer bounded/redacted.", "Withdraw if command rerun, subprocess, shell, repair, or mutation is introduced."],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": LOCAL_RUNTIME_OUTPUT_VERSION,
            "layer": "internal_provider",
            "subject": "local_runtime_output_failure_explanation",
            "principles": [
                "output interpretation is not command execution",
                "failure explanation is not automatic repair",
                "next action candidate is not action execution",
                "output summary is not raw output dump",
                "failure classification is deterministic, not LLM judging",
                "no command may be rerun in v0.24.8",
                "no file may be modified in v0.24.8",
            ],
            "safety_boundary": {
                "output_interpreted": True,
                "failure_explained": "conditional",
                "command_rerun_performed": False,
                "local_command_executed": False,
                "process_spawned": False,
                "subprocess_used": False,
                "shell_enabled": False,
                "automatic_repair_performed": False,
                "file_mutation_performed": False,
                "patch_applied": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_output_dumped": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": LOCAL_RUNTIME_OUTPUT_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "local_runtime_output_failure_explained",
            "version": LOCAL_RUNTIME_OUTPUT_VERSION,
            "source_read_models": [
                "LocalRuntimeExecutionBoundaryReportState",
                "BoundedLocalCommandRunState",
                "LocalRuntimeProcessResultState",
                "LocalRuntimeOutputCaptureState",
                "LocalRuntimeSideEffectScanState",
            ],
            "target_read_models": [
                "LocalRuntimeOutputSummaryState",
                "LocalRuntimeFailureClassificationState",
                "LocalRuntimeFailureExplanationState",
                "LocalRuntimeDiagnosticFindingState",
                "LocalRuntimeNextActionCandidateState",
                "V024ReadinessState",
            ],
            "effect_types": LOCAL_RUNTIME_OUTPUT_EFFECT_TYPES,
        }


def render_local_runtime_output_cli(report: LocalRuntimeOutputFailureReport, section: str) -> str:
    lines = [
        f"version={report.version}",
        f"provider={report.policy.provider_id}",
        f"output_interpreted={str(report.output_interpreted).lower()}",
        f"failure_explained={str(report.failure_explained).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"process_spawned={str(report.process_spawned).lower()}",
        f"stdout_captured_from_new_process={str(report.stdout_captured_from_new_process).lower()}",
        f"stderr_captured_from_new_process={str(report.stderr_captured_from_new_process).lower()}",
        f"automatic_repair_performed={str(report.automatic_repair_performed).lower()}",
        f"file_mutation_performed={str(report.file_mutation_performed).lower()}",
        f"patch_applied={str(report.patch_applied).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_output_dumped={str(report.raw_output_dumped).lower()}",
        f"ready_for_v0_24_9={str(report.ready_for_v0_24_9).lower()}",
        f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "output-summary":
        lines.append(f"summary_status={report.output_summary.summary_status}")
        lines.append(f"high_level_summary={report.output_summary.high_level_summary}")
    elif section == "explain-failure":
        lines.append(f"classification={report.failure_classification.primary_failure_type}")
        lines.append(f"explanation={report.failure_explanation.explanation_text}")
    elif section == "diagnostics" or section == "output-findings":
        lines.append("findings:")
        for finding in report.findings:
            lines.append(f"- {finding.severity}:{finding.finding_type}: {finding.message}")
    elif section == "next-actions":
        lines.append("next_actions:")
        for candidate in report.next_action_candidates:
            lines.append(f"- {candidate.candidate_type}: executes_now={str(candidate.executes_now).lower()} mutates_files_now={str(candidate.mutates_files_now).lower()}")
    else:
        lines.append(f"report_status={report.report_status}")
        lines.append(f"primary_failure_type={report.failure_classification.primary_failure_type}")
    return "\n".join(lines)
