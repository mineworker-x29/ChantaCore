from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
import time
from typing import Any

from chanta_core.internal_provider.local_runtime_candidate_provider import (
    LOCAL_RUNTIME_PROVIDER_ID,
    LocalRuntimeCommandCandidate,
    LocalRuntimeCommandCandidateReport,
    LocalRuntimeCommandCandidateReportService,
)


LOCAL_RUNTIME_SAFETY_VERSION = "v0.24.6"
LOCAL_RUNTIME_SAFETY_VERSION_NAME = "Local Runtime Static Safety / Preflight"
LOCAL_RUNTIME_SAFETY_KOREAN_NAME = "로컬 런타임 정적 안전성·사전점검"
LOCAL_RUNTIME_SAFETY_NEXT_STEP = "v0.24.7 Gated Local Runtime Execution Boundary"

LOCAL_RUNTIME_SAFETY_OBJECT_TYPES = [
    "local_runtime_safety_preflight_request",
    "local_runtime_command_allowlist_entry",
    "local_runtime_command_allowlist_policy",
    "local_runtime_forbidden_pattern_policy",
    "local_runtime_static_safety_rule",
    "local_runtime_static_safety_rule_result",
    "local_runtime_static_safety_finding",
    "local_runtime_static_safety_report",
    "local_runtime_declared_preflight_policy",
    "local_runtime_declared_preflight_check",
    "local_runtime_declared_preflight_result",
    "local_runtime_preflight_finding",
    "local_runtime_preflight_report",
    "local_runtime_execution_eligibility",
    "local_runtime_safety_preflight_report",
    "local_runtime_safety_needs_more_input_candidate",
    "local_runtime_safety_no_action_candidate",
    "local_runtime_command_candidate",
    "local_runtime_command_candidate_report",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

LOCAL_RUNTIME_SAFETY_EVENT_TYPES = [
    "local_runtime_safety_preflight_requested",
    "local_runtime_command_allowlist_policy_created",
    "local_runtime_forbidden_pattern_policy_created",
    "local_runtime_static_safety_rules_loaded",
    "local_runtime_static_safety_checked",
    "local_runtime_static_safety_report_created",
    "local_runtime_declared_preflight_policy_created",
    "local_runtime_declared_preflight_checked",
    "local_runtime_preflight_report_created",
    "local_runtime_execution_eligibility_created",
    "local_runtime_safety_preflight_report_created",
    "local_runtime_safety_warning_created",
    "local_runtime_safety_blocked",
]

LOCAL_RUNTIME_SAFETY_RELATION_TYPES = [
    "checks_local_runtime_static_safety",
    "checks_local_runtime_declared_preflight",
    "uses_local_runtime_command_candidate",
    "uses_local_runtime_provider",
    "uses_internal_provider_registry",
    "applies_command_allowlist_policy",
    "applies_forbidden_pattern_policy",
    "evaluates_static_safety_rule",
    "produces_static_safety_result",
    "produces_preflight_result",
    "produces_execution_eligibility",
    "eligible_for_execution_gate",
    "defers_execution_gate_to_v0_24_7",
    "not_local_command_executed",
    "not_process_spawned",
    "not_shell_executed",
    "not_subprocess_called",
    "not_stdout_captured",
    "not_stderr_captured",
    "not_external_runtime_touched",
    "prevents_credential_exposure",
    "defers_general_agent_usability_to_v0_25",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_local_runtime_command_candidate",
    "derived_from_internal_provider_registry",
]

LOCAL_RUNTIME_SAFETY_EFFECT_TYPES = [
    "read_only_observation",
    "local_runtime_static_safety_checked",
    "local_runtime_preflight_checked",
    "local_runtime_execution_eligibility_created",
    "state_candidate_created",
]

LOCAL_RUNTIME_SAFETY_FORBIDDEN_EFFECT_TYPES = [
    "local_command_executed",
    "bounded_local_command_executed",
    "process_spawned",
    "stdout_captured",
    "stderr_captured",
    "unrestricted_shell_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "file_written",
    "file_edited",
    "file_deleted",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "raw_secret_output",
    "external_provider_called",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_id(value: str | None) -> str:
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", value or "none")[:120] or "none"


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


@dataclass
class LocalRuntimeSafetyPreflightRequest:
    candidate_report_id: str | None = None
    candidate_set_id: str | None = None
    candidate_id: str | None = None
    include_static_safety: bool = True
    include_declared_preflight: bool = True
    include_allowlist_check: bool = True
    include_cwd_boundary_check: bool = True
    include_env_policy_check: bool = True
    include_timeout_policy_check: bool = True
    include_output_policy_check: bool = True
    include_side_effect_risk_check: bool = True
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandAllowlistEntry:
    entry_id: str
    command_category: str
    tool_name: str
    allowed_argv_prefix: list[str]
    allowed_arg_patterns: list[str]
    denied_arg_patterns: list[str]
    allowed_target_kinds: list[str]
    requires_workspace_bound_cwd: bool = True
    requires_timeout: bool = True
    requires_output_cap: bool = True
    requires_redaction: bool = True
    network_allowed: bool = False
    package_install_allowed: bool = False
    destructive_allowed: bool = False
    shell_allowed: bool = False
    status: str = "active"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandAllowlistPolicy:
    policy_id: str
    entries: list[LocalRuntimeCommandAllowlistEntry]
    version: str = LOCAL_RUNTIME_SAFETY_VERSION
    deny_by_default: bool = True
    argv_prefix_required: bool = True
    shell_forbidden: bool = True
    shell_string_forbidden: bool = True
    workspace_bound_cwd_required: bool = True
    timeout_required: bool = True
    output_cap_required: bool = True
    redaction_required: bool = True
    env_value_materialization_forbidden: bool = True
    credential_env_forbidden: bool = True
    network_forbidden_by_default: bool = True
    package_install_forbidden_by_default: bool = True
    destructive_command_forbidden_by_default: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeForbiddenPatternPolicy:
    policy_id: str
    forbidden_tools: list[str]
    forbidden_arg_patterns: list[str]
    forbidden_path_patterns: list[str]
    forbidden_env_patterns: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeStaticSafetyRule:
    rule_id: str
    category: str
    severity_if_failed: str
    description: str
    enabled: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeStaticSafetyRuleResult:
    result_id: str
    rule_id: str
    category: str
    passed: bool
    severity: str
    message: str
    candidate_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeStaticSafetyFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    candidate_ref: dict[str, Any] | None
    rule_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeStaticSafetyReport:
    report_id: str
    created_at: str
    request: LocalRuntimeSafetyPreflightRequest
    allowlist_policy: LocalRuntimeCommandAllowlistPolicy
    forbidden_pattern_policy: LocalRuntimeForbiddenPatternPolicy
    rules: list[LocalRuntimeStaticSafetyRule]
    rule_results: list[LocalRuntimeStaticSafetyRuleResult]
    findings: list[LocalRuntimeStaticSafetyFinding]
    checked_candidate_count: int
    passed_candidate_count: int
    warning_candidate_count: int
    failed_candidate_count: int
    blocked_candidate_count: int
    static_safety_status: str
    eligible_for_declared_preflight: bool
    version: str = LOCAL_RUNTIME_SAFETY_VERSION
    command_executed: bool = False
    process_spawned: bool = False
    stdout_captured: bool = False
    stderr_captured: bool = False
    execution_gate_opened: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeDeclaredPreflightPolicy:
    policy_id: str
    version: str = LOCAL_RUNTIME_SAFETY_VERSION
    declared_preflight_only: bool = True
    live_tool_availability_check_enabled: bool = False
    live_version_check_enabled: bool = False
    command_execution_for_preflight_enabled: bool = False
    filesystem_write_check_enabled: bool = False
    cwd_boundary_check_required: bool = True
    allowlist_pass_required: bool = True
    timeout_policy_required: bool = True
    output_policy_required: bool = True
    side_effect_risk_preview_required: bool = True
    execution_gate_required_next: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeDeclaredPreflightCheck:
    check_id: str
    candidate_id: str
    check_type: str
    passed: bool
    status: str
    message: str
    live_check_performed: bool = False
    command_executed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeDeclaredPreflightResult:
    result_id: str
    candidate_id: str
    checks: list[LocalRuntimeDeclaredPreflightCheck]
    passed_check_count: int
    warning_check_count: int
    failed_check_count: int
    blocked_check_count: int
    declared_preflight_status: str
    live_preflight_performed: bool = False
    command_executed: bool = False
    process_spawned: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimePreflightFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    candidate_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimePreflightReport:
    report_id: str
    created_at: str
    request: LocalRuntimeSafetyPreflightRequest
    policy: LocalRuntimeDeclaredPreflightPolicy
    preflight_results: list[LocalRuntimeDeclaredPreflightResult]
    findings: list[LocalRuntimePreflightFinding]
    checked_candidate_count: int
    passed_candidate_count: int
    warning_candidate_count: int
    failed_candidate_count: int
    blocked_candidate_count: int
    preflight_status: str
    eligible_for_execution_gate: bool
    version: str = LOCAL_RUNTIME_SAFETY_VERSION
    live_preflight_performed: bool = False
    command_executed: bool = False
    process_spawned: bool = False
    stdout_captured: bool = False
    stderr_captured: bool = False
    execution_gate_opened: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionEligibility:
    eligibility_id: str
    candidate_id: str
    static_safety_report_id: str
    preflight_report_id: str
    eligible_for_execution_gate: bool
    version: str = LOCAL_RUNTIME_SAFETY_VERSION
    eligible_next_version: str = "v0.24.7"
    allowed_execution_mode_future: str = "gated_bounded_local_command"
    execution_allowed_now: bool = False
    gate_required: bool = True
    human_or_policy_gate_required: bool = True
    authorization_required: bool = True
    single_use_execution_authorization_required: bool = True
    timeout_required: bool = True
    output_cap_required: bool = True
    redaction_required: bool = True
    side_effect_scan_required: bool = True
    command_executed: bool = False
    process_spawned: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeSafetyPreflightReport:
    report_id: str
    created_at: str
    request: LocalRuntimeSafetyPreflightRequest
    static_safety_report: LocalRuntimeStaticSafetyReport
    preflight_report: LocalRuntimePreflightReport
    execution_eligibilities: list[LocalRuntimeExecutionEligibility]
    findings: list[dict[str, Any]]
    report_status: str
    ready_for_v0_24_7: bool
    static_safety_checked: bool
    preflight_checked: bool
    eligible_for_execution_gate: bool
    version: str = LOCAL_RUNTIME_SAFETY_VERSION
    ready_for_v0_25: bool = False
    execution_allowed_now: bool = False
    execution_gate_opened: bool = False
    local_command_executed: bool = False
    process_spawned: bool = False
    stdout_captured: bool = False
    stderr_captured: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = LOCAL_RUNTIME_SAFETY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until command candidate, allowlist policy, workspace context, "
        "repository context, or local runtime policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeSafetyNeedsMoreInputCandidate:
    candidate_id: str
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "needs_more_input"
    local_command_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeSafetyNoActionCandidate:
    candidate_id: str
    reason: str
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "no_action"
    local_command_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class LocalRuntimeSafetySourceService:
    def __init__(self, candidate_report: LocalRuntimeCommandCandidateReport | None = None) -> None:
        self.candidate_report = candidate_report

    def load_candidate_report(self, candidate_report_id: str | None = None) -> LocalRuntimeCommandCandidateReport:
        if self.candidate_report is not None:
            return self.candidate_report
        return LocalRuntimeCommandCandidateReportService().build_report({"goal": "check python version", "category": "version_check"})

    def load_candidate_set(self, candidate_set_id: str | None = None) -> Any:
        return self.load_candidate_report().candidate_set

    def load_candidate(self, candidate_id: str | None = None) -> LocalRuntimeCommandCandidate | None:
        candidates = self.load_candidate_report().candidate_set.candidates
        if candidate_id:
            for candidate in candidates:
                if candidate.candidate_id == candidate_id or candidate_id == "demo":
                    return candidate
        return candidates[0] if candidates else None

    def load_workspace_context(self) -> dict[str, Any]:
        return {"workspace_ref": {"kind": "workspace_root", "label": "."}}

    def load_repository_context(self) -> dict[str, Any]:
        return {"repository_ref": {"kind": "repository", "label": "current"}}

    def load_process_state_context(self) -> dict[str, Any]:
        return {"process_state_ref": {"version": "v0.24.4"}}


class LocalRuntimeCommandAllowlistPolicyService:
    def build_allowlist_policy(self) -> LocalRuntimeCommandAllowlistPolicy:
        specs = [
            ("python_version_check", "version_check", "python", ["python", "--version"]),
            ("git_status_short", "repo_status", "git", ["git", "status", "--short"]),
            ("git_diff_stat", "repo_status", "git", ["git", "diff", "--stat"]),
            ("python_compileall", "compile_check", "python", ["python", "-m", "compileall"]),
            ("pytest", "test", "python", ["python", "-m", "pytest"]),
            ("ruff_check", "lint", "python", ["python", "-m", "ruff", "check"]),
            ("mypy", "typecheck", "python", ["python", "-m", "mypy"]),
        ]
        entries = [
            LocalRuntimeCommandAllowlistEntry(
                entry_id=entry_id,
                command_category=category,
                tool_name=tool,
                allowed_argv_prefix=prefix,
                allowed_arg_patterns=["relative_path", "workspace_path", "no_shell"],
                denied_arg_patterns=["-c", "install", "delete", "remove", "rm", "--force"],
                allowed_target_kinds=["workspace", "repository", "directory", "file", "package", "unknown"],
                evidence_refs=[{"type": "static_descriptor_only", "not_execution_authorization": True}],
            )
            for entry_id, category, tool, prefix in specs
        ]
        return LocalRuntimeCommandAllowlistPolicy(
            policy_id="local_runtime_command_allowlist_policy_v0_24_6",
            entries=entries,
            evidence_refs=[{"type": "allowlist_policy", "authorization": False}],
        )

    def match_argv_prefix(self, candidate: LocalRuntimeCommandCandidate, policy: LocalRuntimeCommandAllowlistPolicy | None = None) -> bool:
        policy = policy or self.build_allowlist_policy()
        argv = candidate.argv_candidate.argv if candidate.argv_candidate else []
        return any(argv[: len(entry.allowed_argv_prefix)] == entry.allowed_argv_prefix for entry in policy.entries)


class LocalRuntimeForbiddenPatternPolicyService:
    def build_forbidden_pattern_policy(self) -> LocalRuntimeForbiddenPatternPolicy:
        return LocalRuntimeForbiddenPatternPolicy(
            policy_id="local_runtime_forbidden_pattern_policy_v0_24_6",
            forbidden_tools=["powershell", "cmd", "bash", "sh", "curl", "wget", "ssh", "scp", "docker", "kubectl", "terraform", "npm", "pip"],
            forbidden_arg_patterns=["-c", "--install", "install", "uninstall", "delete", "remove", "rm", "rmdir", "del", "reset", "push", "force", "--force", "--global"],
            forbidden_path_patterns=["..", "~", "$HOME"],
            forbidden_env_patterns=["TOKEN", "SECRET", "PASSWORD", "API_KEY", "CREDENTIAL"],
            evidence_refs=[{"type": "deterministic_forbidden_patterns"}],
        )

    def detect_forbidden_tool(self, candidate: LocalRuntimeCommandCandidate, policy: LocalRuntimeForbiddenPatternPolicy | None = None) -> bool:
        policy = policy or self.build_forbidden_pattern_policy()
        argv = candidate.argv_candidate.argv if candidate.argv_candidate else []
        return bool(argv and argv[0].lower() in policy.forbidden_tools)

    def detect_forbidden_args(self, candidate: LocalRuntimeCommandCandidate, policy: LocalRuntimeForbiddenPatternPolicy | None = None) -> bool:
        policy = policy or self.build_forbidden_pattern_policy()
        argv = [part.lower() for part in (candidate.argv_candidate.argv if candidate.argv_candidate else [])]
        return any(part in policy.forbidden_arg_patterns for part in argv)


class LocalRuntimeStaticSafetyRuleRegistry:
    def list_rules(self) -> list[LocalRuntimeStaticSafetyRule]:
        specs = [
            ("candidate_must_exist", "candidate_lifecycle", "critical"),
            ("candidate_must_not_be_executed", "candidate_lifecycle", "critical"),
            ("candidate_must_not_have_process_spawned", "candidate_lifecycle", "critical"),
            ("argv_must_be_list", "argv_structure", "error"),
            ("shell_string_must_be_absent", "shell_safety", "critical"),
            ("shell_must_be_forbidden", "shell_safety", "critical"),
            ("argv_prefix_must_match_allowlist", "allowlist", "error"),
            ("forbidden_args_must_be_absent", "forbidden_pattern", "critical"),
            ("cwd_must_be_workspace_bound", "cwd_boundary", "critical"),
            ("private_cwd_path_must_be_sanitized", "cwd_boundary", "warning"),
            ("env_values_must_not_be_materialized", "env_safety", "critical"),
            ("credential_env_must_be_absent", "credential_safety", "critical"),
            ("timeout_policy_must_exist", "timeout_policy", "error"),
            ("output_policy_must_exist", "output_policy", "error"),
            ("raw_output_must_be_forbidden", "output_policy", "critical"),
            ("redaction_must_be_required", "output_policy", "error"),
            ("network_command_must_be_blocked", "side_effect_risk", "critical"),
            ("package_install_must_be_blocked", "side_effect_risk", "critical"),
            ("destructive_command_must_be_blocked", "side_effect_risk", "critical"),
            ("static_safety_must_not_execute_command", "roadmap_boundary", "critical"),
            ("preflight_must_not_execute_command", "roadmap_boundary", "critical"),
            ("execution_gate_must_remain_closed", "roadmap_boundary", "critical"),
            ("local_runtime_execution_deferred_to_v0_24_7", "roadmap_boundary", "info"),
        ]
        return [
            LocalRuntimeStaticSafetyRule(
                rule_id=rule_id,
                category=category,
                severity_if_failed=severity,
                description=f"v0.24.6 static safety rule: {rule_id}",
            )
            for rule_id, category, severity in specs
        ]


class LocalRuntimeStaticSafetyRuleEngine:
    def evaluate_candidate(
        self,
        candidate: LocalRuntimeCommandCandidate | None,
        allowlist_policy: LocalRuntimeCommandAllowlistPolicy,
        forbidden_policy: LocalRuntimeForbiddenPatternPolicy,
        rules: list[LocalRuntimeStaticSafetyRule],
    ) -> tuple[list[LocalRuntimeStaticSafetyRuleResult], list[LocalRuntimeStaticSafetyFinding], str]:
        results: list[LocalRuntimeStaticSafetyRuleResult] = []
        findings: list[LocalRuntimeStaticSafetyFinding] = []

        def rule_passed(rule_id: str) -> bool:
            if candidate is None:
                return rule_id not in {"candidate_must_exist"}
            argv_candidate = candidate.argv_candidate
            cwd = candidate.cwd_candidate
            env = candidate.env_policy_candidate
            output = candidate.output_policy_candidate
            risk = candidate.side_effect_risk_preview
            checks = {
                "candidate_must_exist": True,
                "candidate_must_not_be_executed": not candidate.local_command_executed,
                "candidate_must_not_have_process_spawned": not candidate.process_spawned,
                "argv_must_be_list": isinstance(argv_candidate.argv if argv_candidate else None, list),
                "shell_string_must_be_absent": argv_candidate is None or argv_candidate.shell_string is None,
                "shell_must_be_forbidden": argv_candidate is None or (not argv_candidate.shell_required and not argv_candidate.shell_allowed),
                "argv_prefix_must_match_allowlist": LocalRuntimeCommandAllowlistPolicyService().match_argv_prefix(candidate, allowlist_policy),
                "forbidden_args_must_be_absent": not LocalRuntimeForbiddenPatternPolicyService().detect_forbidden_args(candidate, forbidden_policy),
                "cwd_must_be_workspace_bound": bool(cwd and cwd.workspace_bound),
                "private_cwd_path_must_be_sanitized": bool(cwd and not cwd.private_full_path_output),
                "env_values_must_not_be_materialized": not env.env_values_materialized,
                "credential_env_must_be_absent": not env.credential_env_detected,
                "timeout_policy_must_exist": candidate.timeout_policy_candidate is not None,
                "output_policy_must_exist": output is not None,
                "raw_output_must_be_forbidden": bool(output and not output.raw_output_allowed),
                "redaction_must_be_required": bool(output and output.redact_secret_like_output),
                "network_command_must_be_blocked": not risk.network_risk,
                "package_install_must_be_blocked": not risk.package_install_risk,
                "destructive_command_must_be_blocked": not risk.destructive_risk,
                "static_safety_must_not_execute_command": True,
                "preflight_must_not_execute_command": True,
                "execution_gate_must_remain_closed": not candidate.execution_gate_opened,
                "local_runtime_execution_deferred_to_v0_24_7": True,
            }
            return checks.get(rule_id, True)

        finding_map = {
            "candidate_must_exist": "missing_candidate",
            "candidate_must_not_be_executed": "candidate_already_executed",
            "candidate_must_not_have_process_spawned": "process_spawn_detected",
            "argv_must_be_list": "argv_not_list",
            "shell_string_must_be_absent": "shell_string_detected",
            "shell_must_be_forbidden": "shell_required_detected",
            "argv_prefix_must_match_allowlist": "allowlist_mismatch",
            "forbidden_args_must_be_absent": "forbidden_arg_detected",
            "cwd_must_be_workspace_bound": "cwd_outside_workspace",
            "private_cwd_path_must_be_sanitized": "private_cwd_path_not_sanitized",
            "env_values_must_not_be_materialized": "env_values_materialized",
            "credential_env_must_be_absent": "credential_env_detected",
            "timeout_policy_must_exist": "timeout_policy_missing",
            "output_policy_must_exist": "output_policy_missing",
            "raw_output_must_be_forbidden": "raw_output_allowed",
            "redaction_must_be_required": "redaction_missing",
            "network_command_must_be_blocked": "network_command_detected",
            "package_install_must_be_blocked": "package_install_command_detected",
            "destructive_command_must_be_blocked": "destructive_command_detected",
            "execution_gate_must_remain_closed": "execution_gate_opened_too_early",
        }
        candidate_ref = {"candidate_id": candidate.candidate_id} if candidate else None
        for rule in rules:
            passed = rule_passed(rule.rule_id)
            severity = "info" if passed else rule.severity_if_failed
            results.append(
                LocalRuntimeStaticSafetyRuleResult(
                    result_id=f"static_safety_rule_result:{rule.rule_id}:{_safe_id(candidate.candidate_id if candidate else None)}",
                    rule_id=rule.rule_id,
                    category=rule.category,
                    passed=passed,
                    severity=severity,
                    message=("passed" if passed else "failed") + f": {rule.description}",
                    candidate_ref=candidate_ref,
                    evidence_refs=[{"type": "deterministic_rule_result"}],
                )
            )
            if not passed:
                findings.append(
                    LocalRuntimeStaticSafetyFinding(
                        finding_id=f"static_safety_finding:{finding_map.get(rule.rule_id, rule.rule_id)}",
                        severity=severity,
                        finding_type=finding_map.get(rule.rule_id, rule.rule_id),
                        message=f"Static safety rule failed: {rule.rule_id}",
                        candidate_ref=candidate_ref,
                        rule_ref={"rule_id": rule.rule_id},
                        evidence_refs=[{"type": "static_safety_rule"}],
                        withdrawal_condition="Withdraw if candidate metadata or policy changes.",
                )
            )
        if candidate and candidate.argv_candidate and candidate.argv_candidate.contains_unresolved_placeholders:
            findings.append(
                LocalRuntimeStaticSafetyFinding(
                    finding_id="static_safety_finding:unresolved_argv_placeholder",
                    severity="error",
                    finding_type="unresolved_argv_placeholder",
                    message="Argv contains unresolved placeholders.",
                    candidate_ref=candidate_ref,
                    rule_ref={"rule_id": "argv_placeholders_must_be_resolved"},
                    evidence_refs=[{"type": "static_safety_rule"}],
                    withdrawal_condition="Withdraw if target path is provided and argv is materialized.",
                )
            )
        if not findings:
            findings.append(
                LocalRuntimeStaticSafetyFinding(
                    finding_id="static_safety_finding:ok",
                    severity="info",
                    finding_type="ok",
                    message="Candidate passed deterministic static safety.",
                    candidate_ref=candidate_ref,
                    rule_ref=None,
                    evidence_refs=[{"type": "static_safety_rule"}],
                    withdrawal_condition=None,
                )
            )
        if any(f.severity == "critical" for f in findings):
            status = "blocked"
        elif any(f.severity == "error" for f in findings):
            status = "failed"
        elif any(f.severity == "warning" for f in findings):
            status = "warning"
        else:
            status = "passed"
        return results, findings, status


class LocalRuntimeStaticSafetyReportService:
    def __init__(self, source_service: LocalRuntimeSafetySourceService | None = None) -> None:
        self.source_service = source_service or LocalRuntimeSafetySourceService()

    def build_report(self, request: LocalRuntimeSafetyPreflightRequest | None = None) -> LocalRuntimeStaticSafetyReport:
        request = request or LocalRuntimeSafetyPreflightRequest()
        candidate = self.source_service.load_candidate(request.candidate_id)
        allowlist = LocalRuntimeCommandAllowlistPolicyService().build_allowlist_policy()
        forbidden = LocalRuntimeForbiddenPatternPolicyService().build_forbidden_pattern_policy()
        rules = LocalRuntimeStaticSafetyRuleRegistry().list_rules()
        rule_results, findings, status = LocalRuntimeStaticSafetyRuleEngine().evaluate_candidate(candidate, allowlist, forbidden, rules)
        checked = 1 if candidate else 0
        return LocalRuntimeStaticSafetyReport(
            report_id=f"local_runtime_static_safety_report:{_safe_id(request.candidate_id or (candidate.candidate_id if candidate else None))}",
            created_at=_utc_now(),
            request=request,
            allowlist_policy=allowlist,
            forbidden_pattern_policy=forbidden,
            rules=rules,
            rule_results=rule_results,
            findings=findings,
            checked_candidate_count=checked,
            passed_candidate_count=1 if status == "passed" else 0,
            warning_candidate_count=1 if status == "warning" else 0,
            failed_candidate_count=1 if status == "failed" else 0,
            blocked_candidate_count=1 if status == "blocked" else 0,
            static_safety_status=status,
            eligible_for_declared_preflight=status in {"passed", "warning"},
            evidence_refs=[{"type": "non_executing_static_safety", "provider": LOCAL_RUNTIME_PROVIDER_ID}],
        )


class LocalRuntimeDeclaredPreflightPolicyService:
    def build_policy(self) -> LocalRuntimeDeclaredPreflightPolicy:
        return LocalRuntimeDeclaredPreflightPolicy(
            policy_id="local_runtime_declared_preflight_policy_v0_24_6",
            evidence_refs=[{"type": "declared_preflight_only", "live_checks": False}],
        )


class LocalRuntimeDeclaredPreflightService:
    def check_candidate(
        self,
        candidate: LocalRuntimeCommandCandidate | None,
        static_safety_report: LocalRuntimeStaticSafetyReport,
    ) -> LocalRuntimeDeclaredPreflightResult:
        candidate_id = candidate.candidate_id if candidate else "missing"
        allowlist_match = bool(candidate and LocalRuntimeCommandAllowlistPolicyService().match_argv_prefix(candidate, static_safety_report.allowlist_policy))
        checks = [
            ("candidate_status", bool(candidate and candidate.candidate_status in {"ready_for_static_safety", "needs_more_input", "no_action"}), "Candidate status is declared."),
            ("allowlist_compatibility", allowlist_match, "Argv prefix is compatible with static allowlist."),
            ("cwd_boundary", bool(candidate and candidate.cwd_candidate and candidate.cwd_candidate.workspace_bound), "CWD is workspace-bound."),
            ("env_policy", bool(candidate and not candidate.env_policy_candidate.env_values_materialized and not candidate.env_policy_candidate.credential_env_detected), "Environment policy is non-materialized."),
            ("timeout_policy", bool(candidate and candidate.timeout_policy_candidate and candidate.timeout_policy_candidate.timeout_required), "Timeout policy exists."),
            ("output_policy", bool(candidate and candidate.output_policy_candidate and candidate.output_policy_candidate.redact_secret_like_output and not candidate.output_policy_candidate.raw_output_allowed), "Output cap and redaction are declared."),
            ("side_effect_risk", bool(candidate and candidate.side_effect_risk_preview.risk_level in {"read_only", "low", "medium", "unknown"}), "Side-effect risk preview is present."),
            ("next_gate_requirements", static_safety_report.eligible_for_declared_preflight, "Execution gate remains next required step."),
        ]
        check_models = [
            LocalRuntimeDeclaredPreflightCheck(
                check_id=f"declared_preflight_check:{candidate_id}:{check_type}",
                candidate_id=candidate_id,
                check_type=check_type,
                passed=passed,
                status="passed" if passed else "failed",
                message=message,
                evidence_refs=[{"type": "declared_metadata_check"}],
            )
            for check_type, passed, message in checks
        ]
        failed = sum(1 for item in check_models if item.status == "failed")
        status = "passed" if failed == 0 else "failed"
        return LocalRuntimeDeclaredPreflightResult(
            result_id=f"declared_preflight_result:{candidate_id}",
            candidate_id=candidate_id,
            checks=check_models,
            passed_check_count=sum(1 for item in check_models if item.status == "passed"),
            warning_check_count=0,
            failed_check_count=failed,
            blocked_check_count=0,
            declared_preflight_status=status,
            evidence_refs=[{"type": "declared_preflight_only"}],
        )


class LocalRuntimePreflightReportService:
    def __init__(self, source_service: LocalRuntimeSafetySourceService | None = None) -> None:
        self.source_service = source_service or LocalRuntimeSafetySourceService()

    def build_report(
        self,
        request: LocalRuntimeSafetyPreflightRequest | None = None,
        static_safety_report: LocalRuntimeStaticSafetyReport | None = None,
    ) -> LocalRuntimePreflightReport:
        request = request or LocalRuntimeSafetyPreflightRequest()
        static_safety_report = static_safety_report or LocalRuntimeStaticSafetyReportService(self.source_service).build_report(request)
        candidate = self.source_service.load_candidate(request.candidate_id)
        policy = LocalRuntimeDeclaredPreflightPolicyService().build_policy()
        result = LocalRuntimeDeclaredPreflightService().check_candidate(candidate, static_safety_report)
        findings: list[LocalRuntimePreflightFinding] = []
        if not static_safety_report.eligible_for_declared_preflight:
            findings.append(LocalRuntimePreflightFinding("preflight_finding:static_safety_not_passed", "error", "static_safety_not_passed", "Static safety did not pass.", {"candidate_id": result.candidate_id}, [], "Withdraw if static safety report changes."))
        if result.declared_preflight_status != "passed":
            findings.append(LocalRuntimePreflightFinding("preflight_finding:declared_preflight_not_possible", "error", "declared_preflight_not_possible", "Declared preflight checks did not pass.", {"candidate_id": result.candidate_id}, [], "Withdraw if candidate metadata changes."))
        if not findings:
            findings.append(LocalRuntimePreflightFinding("preflight_finding:ok", "info", "ok", "Declared preflight passed without live checks.", {"candidate_id": result.candidate_id}, [], None))
        status = "passed" if result.declared_preflight_status == "passed" and static_safety_report.eligible_for_declared_preflight else "failed"
        return LocalRuntimePreflightReport(
            report_id=f"local_runtime_preflight_report:{_safe_id(result.candidate_id)}",
            created_at=_utc_now(),
            request=request,
            policy=policy,
            preflight_results=[result],
            findings=findings,
            checked_candidate_count=1 if candidate else 0,
            passed_candidate_count=1 if status == "passed" else 0,
            warning_candidate_count=0,
            failed_candidate_count=1 if status == "failed" else 0,
            blocked_candidate_count=0,
            preflight_status=status,
            eligible_for_execution_gate=status == "passed",
            evidence_refs=[{"type": "declared_preflight_only", "live_preflight_performed": False}],
        )


class LocalRuntimeExecutionEligibilityService:
    def build_eligibility(
        self,
        candidate: LocalRuntimeCommandCandidate | None,
        static_safety_report: LocalRuntimeStaticSafetyReport,
        preflight_report: LocalRuntimePreflightReport,
    ) -> LocalRuntimeExecutionEligibility:
        candidate_id = candidate.candidate_id if candidate else "missing"
        eligible = static_safety_report.eligible_for_declared_preflight and preflight_report.eligible_for_execution_gate
        return LocalRuntimeExecutionEligibility(
            eligibility_id=f"local_runtime_execution_eligibility:{_safe_id(candidate_id)}",
            candidate_id=candidate_id,
            static_safety_report_id=static_safety_report.report_id,
            preflight_report_id=preflight_report.report_id,
            eligible_for_execution_gate=eligible,
            evidence_refs=[{"type": "execution_gate_eligibility_only", "execution_allowed_now": False}],
        )


class LocalRuntimeSafetyPreflightReportService:
    def __init__(self, source_service: LocalRuntimeSafetySourceService | None = None) -> None:
        self.source_service = source_service or LocalRuntimeSafetySourceService()

    def build_report(self, request: LocalRuntimeSafetyPreflightRequest | None = None) -> LocalRuntimeSafetyPreflightReport:
        request = request or LocalRuntimeSafetyPreflightRequest()
        static_report = LocalRuntimeStaticSafetyReportService(self.source_service).build_report(request)
        preflight_report = LocalRuntimePreflightReportService(self.source_service).build_report(request, static_report)
        candidate = self.source_service.load_candidate(request.candidate_id)
        eligibility = LocalRuntimeExecutionEligibilityService().build_eligibility(candidate, static_report, preflight_report)
        findings = [finding.to_dict() for finding in static_report.findings] + [finding.to_dict() for finding in preflight_report.findings]
        if static_report.static_safety_status == "blocked":
            status = "blocked"
        elif static_report.static_safety_status == "failed" or preflight_report.preflight_status == "failed":
            status = "failed"
        elif static_report.static_safety_status == "warning" or preflight_report.preflight_status == "warning":
            status = "warning"
        else:
            status = "passed"
        return LocalRuntimeSafetyPreflightReport(
            report_id=f"local_runtime_safety_preflight_report:{_safe_id(request.candidate_id or (candidate.candidate_id if candidate else None))}",
            created_at=_utc_now(),
            request=request,
            static_safety_report=static_report,
            preflight_report=preflight_report,
            execution_eligibilities=[eligibility],
            findings=findings,
            report_status=status,
            ready_for_v0_24_7=eligibility.eligible_for_execution_gate,
            static_safety_checked=True,
            preflight_checked=True,
            eligible_for_execution_gate=eligibility.eligible_for_execution_gate,
            limitations=[
                "Declared preflight does not execute commands or perform live tool checks.",
                "Execution eligibility only permits moving to the v0.24.7 gate.",
            ],
            withdrawal_conditions=[
                "Withdraw eligibility if the candidate, allowlist, or workspace boundary changes.",
                "Withdraw eligibility if any live command check is introduced before v0.24.7.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": LOCAL_RUNTIME_SAFETY_VERSION,
            "layer": "internal_provider",
            "subject": "local_runtime_static_safety_preflight",
            "principles": [
                "static safety check is not command execution",
                "declared preflight is not live command execution",
                "preflight is not process spawn",
                "allowlist compatibility is not authorization to execute",
                "execution eligibility is not execution",
                "execution eligibility only permits moving to v0.24.7 execution gate",
            ],
            "safety_boundary": {
                "static_safety_checked": True,
                "preflight_checked": True,
                "declared_preflight_only": True,
                "live_preflight_performed": False,
                "execution_allowed_now": False,
                "execution_gate_opened": False,
                "local_command_executed": False,
                "process_spawned": False,
                "stdout_captured": False,
                "stderr_captured": False,
                "shell_enabled": False,
                "subprocess_used": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": LOCAL_RUNTIME_SAFETY_NEXT_STEP,
            "roadmap": {
                "v0.24": "Internal Provider / Local Runtime Provider",
                "v0.25": "General Agent Usability & Tool Routing",
                "v0.26": "Workspace Agent Workbench",
                "v0.27": "Memory Candidate & Continuity",
                "v0.28": "Public Alpha / Schumpeter Split Preparation",
                "v0.29+": "External Skill / External Provider Adapters",
            },
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "local_runtime_command_candidate_safety_preflight_checked",
            "version": LOCAL_RUNTIME_SAFETY_VERSION,
            "source_read_models": [
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
                "LocalRuntimeCommandCandidateState",
                "LocalRuntimeIntentState",
                "LocalCommandArgvCandidateState",
                "WorkspaceReadProviderState",
                "RepositorySearchProviderState",
                "ProcessStateInspectionState",
            ],
            "target_read_models": [
                "LocalRuntimeStaticSafetyState",
                "LocalRuntimePreflightState",
                "LocalRuntimeExecutionEligibilityState",
                "LocalRuntimeGateReadinessState",
                "V024ReadinessState",
            ],
            "effect_types": LOCAL_RUNTIME_SAFETY_EFFECT_TYPES,
        }


def render_local_runtime_safety_cli(report: LocalRuntimeSafetyPreflightReport, section: str) -> str:
    lines = [
        f"version={report.version}",
        f"provider={LOCAL_RUNTIME_PROVIDER_ID}",
        f"static_safety_checked={str(report.static_safety_checked).lower()}",
        f"preflight_checked={str(report.preflight_checked).lower()}",
        f"declared_preflight_only={str(report.preflight_report.policy.declared_preflight_only).lower()}",
        f"live_preflight_performed={str(report.preflight_report.live_preflight_performed).lower()}",
        f"execution_allowed_now={str(report.execution_allowed_now).lower()}",
        f"execution_gate_opened={str(report.execution_gate_opened).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"process_spawned={str(report.process_spawned).lower()}",
        f"stdout_captured={str(report.stdout_captured).lower()}",
        f"stderr_captured={str(report.stderr_captured).lower()}",
        "shell_allowed=false",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"eligible_for_execution_gate={str(report.eligible_for_execution_gate).lower()}",
        f"ready_for_v0_24_7={str(report.ready_for_v0_24_7).lower()}",
        f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "allowlist":
        lines.append("allowlist:")
        for entry in report.static_safety_report.allowlist_policy.entries:
            lines.append(f"- {entry.entry_id}: prefix={entry.allowed_argv_prefix} shell_allowed={str(entry.shell_allowed).lower()}")
    elif section in {"safety", "safety-report"}:
        lines.append(f"static_safety_status={report.static_safety_report.static_safety_status}")
        lines.append(f"eligible_for_declared_preflight={str(report.static_safety_report.eligible_for_declared_preflight).lower()}")
        for finding in report.static_safety_report.findings:
            lines.append(f"- {finding.severity}:{finding.finding_type}: {finding.message}")
    elif section in {"preflight", "preflight-report"}:
        lines.append(f"preflight_status={report.preflight_report.preflight_status}")
        for finding in report.preflight_report.findings:
            lines.append(f"- {finding.severity}:{finding.finding_type}: {finding.message}")
    elif section == "eligibility":
        for eligibility in report.execution_eligibilities:
            lines.append(f"eligibility={eligibility.eligibility_id} candidate={eligibility.candidate_id} eligible_for_execution_gate={str(eligibility.eligible_for_execution_gate).lower()} execution_allowed_now={str(eligibility.execution_allowed_now).lower()}")
    elif section == "safety-findings":
        lines.append("findings:")
        for finding in report.findings:
            lines.append(f"- {finding.get('severity')}:{finding.get('finding_type')}: {finding.get('message')}")
    else:
        lines.append(f"report_status={report.report_status}")
    return "\n".join(lines)
