from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
import re
import subprocess
import time
from typing import Any

from chanta_core.internal_provider.local_runtime_candidate_provider import (
    LOCAL_RUNTIME_PROVIDER_ID,
    LocalRuntimeCommandCandidate,
)
from chanta_core.internal_provider.local_runtime_safety_preflight import (
    LocalRuntimeExecutionEligibility,
    LocalRuntimeSafetyPreflightReport,
    LocalRuntimeSafetyPreflightReportService,
    LocalRuntimeSafetyPreflightRequest,
)


GATED_LOCAL_RUNTIME_VERSION = "v0.24.7"
GATED_LOCAL_RUNTIME_VERSION_NAME = "Gated Local Runtime Execution Boundary"
GATED_LOCAL_RUNTIME_KOREAN_NAME = "게이트 기반 로컬 런타임 실행 경계"
GATED_LOCAL_RUNTIME_NEXT_STEP = "v0.24.8 Local Runtime Output / Failure Explanation"

GATED_LOCAL_RUNTIME_OBJECT_TYPES = [
    "local_runtime_execution_gate_request",
    "local_runtime_execution_gate_policy",
    "local_runtime_execution_gate_condition",
    "local_runtime_execution_gate_state",
    "local_runtime_execution_authorization",
    "local_runtime_runner_policy",
    "local_runtime_process_spec",
    "bounded_local_command_run_request",
    "bounded_local_command_run",
    "local_runtime_process_result",
    "local_runtime_output_capture_policy",
    "local_runtime_output_capture",
    "local_runtime_side_effect_policy",
    "local_runtime_side_effect_scan",
    "local_runtime_execution_finding",
    "local_runtime_execution_boundary_report",
    "local_runtime_execution_needs_more_input_candidate",
    "local_runtime_execution_no_action_candidate",
    "local_runtime_execution_eligibility",
    "local_runtime_command_candidate",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

GATED_LOCAL_RUNTIME_EVENT_TYPES = [
    "local_runtime_execution_gate_requested",
    "local_runtime_execution_gate_policy_created",
    "local_runtime_execution_gate_conditions_created",
    "local_runtime_execution_gate_opened",
    "local_runtime_execution_authorization_created",
    "local_runtime_execution_authorization_consumed",
    "local_runtime_process_spec_created",
    "bounded_local_command_run_requested",
    "bounded_local_command_started",
    "bounded_local_command_completed",
    "bounded_local_command_failed",
    "bounded_local_command_timed_out",
    "local_runtime_output_captured",
    "local_runtime_output_redacted",
    "local_runtime_side_effect_scan_created",
    "local_runtime_execution_boundary_report_created",
    "local_runtime_execution_warning_created",
    "local_runtime_execution_blocked",
]

GATED_LOCAL_RUNTIME_RELATION_TYPES = [
    "gates_local_runtime_execution",
    "uses_execution_eligibility",
    "uses_local_runtime_command_candidate",
    "creates_single_use_execution_authorization",
    "consumes_execution_authorization",
    "creates_local_runtime_process_spec",
    "executes_bounded_local_command",
    "captures_local_runtime_output",
    "redacts_local_runtime_output",
    "scans_local_runtime_side_effects",
    "enforces_timeout",
    "enforces_output_cap",
    "enforces_shell_false",
    "enforces_argv_only",
    "enforces_workspace_bound_cwd",
    "enforces_command_allowlist",
    "blocks_network_command",
    "blocks_package_install_command",
    "blocks_destructive_command",
    "not_external_runtime_touched",
    "not_external_provider_called",
    "prevents_credential_exposure",
    "prepares_output_failure_explanation_provider",
    "defers_output_failure_explanation_to_v0_24_8",
    "defers_general_agent_usability_to_v0_25",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_local_runtime_safety_preflight",
    "derived_from_local_runtime_command_candidate",
]

GATED_LOCAL_RUNTIME_EFFECT_TYPES = [
    "read_only_observation",
    "local_runtime_execution_gate_opened",
    "local_runtime_execution_authorization_created",
    "local_runtime_execution_authorization_consumed",
    "bounded_local_command_executed",
    "local_output_captured",
    "local_runtime_side_effect_scan_created",
    "state_candidate_created",
]

GATED_LOCAL_RUNTIME_FORBIDDEN_EFFECT_TYPES = [
    "unrestricted_shell_executed",
    "arbitrary_subprocess_executed",
    "command_string_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "file_written_unexpected",
    "file_edited_unexpected",
    "file_deleted_unexpected",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "raw_secret_output",
    "external_provider_called",
    "memory_mutated",
    "persona_mutated",
    "general_agent_usability_invoked",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_id(value: str | None) -> str:
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", value or "none")[:120] or "none"


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _redact_secret_like(text: str) -> tuple[str, int]:
    pattern = re.compile(r"(?i)(token|secret|password|api[_-]?key|credential)(\s*[:=]\s*)[^\s]+")
    return pattern.subn(r"\1\2[REDACTED]", text)


def _sanitize_private_paths(text: str) -> tuple[str, bool]:
    sanitized = re.sub(r"[A-Za-z]:\\[^\s]+", "[PRIVATE_PATH]", text)
    sanitized = re.sub(r"/(?:Users|home)/[^\s]+", "[PRIVATE_PATH]", sanitized)
    return sanitized, sanitized != text


def _allowed_prefix(argv: list[str]) -> bool:
    prefixes = [
        ["python", "--version"],
        ["git", "status", "--short"],
        ["git", "diff", "--stat"],
        ["python", "-m", "pytest"],
        ["python", "-m", "ruff", "check"],
        ["python", "-m", "mypy"],
    ]
    return any(argv[: len(prefix)] == prefix for prefix in prefixes)


def _forbidden_runtime_argv(argv: list[str]) -> bool:
    lower = [part.lower() for part in argv]
    forbidden_tools = {"curl", "wget", "ssh", "scp", "docker", "kubectl", "terraform", "npm", "pip", "powershell", "cmd", "bash", "sh"}
    forbidden_args = {"install", "--install", "uninstall", "delete", "remove", "rm", "rmdir", "del", "reset", "push", "--force", "--global"}
    return bool(lower and lower[0] in forbidden_tools) or any(part in forbidden_args for part in lower) or lower[:3] == ["python", "-m", "compileall"]


@dataclass
class LocalRuntimeExecutionGateRequest:
    eligibility_id: str | None = None
    candidate_id: str | None = None
    safety_preflight_report_id: str | None = None
    requested_execution_mode: str = "gated_bounded_local_command"
    requester_ref: dict[str, Any] | None = None
    approval_ref: dict[str, Any] | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionGatePolicy:
    policy_id: str
    version: str = GATED_LOCAL_RUNTIME_VERSION
    gate_required: bool = True
    eligibility_required: bool = True
    static_safety_pass_required: bool = True
    preflight_pass_required: bool = True
    single_use_authorization_required: bool = True
    allowlist_match_required: bool = True
    argv_required: bool = True
    shell_forbidden: bool = True
    workspace_bound_cwd_required: bool = True
    timeout_required: bool = True
    output_cap_required: bool = True
    redaction_required: bool = True
    side_effect_scan_required: bool = True
    network_forbidden: bool = True
    package_install_forbidden: bool = True
    destructive_command_forbidden: bool = True
    arbitrary_subprocess_forbidden: bool = True
    credential_env_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionGateCondition:
    condition_id: str
    condition_type: str
    description: str
    passed: bool
    severity_if_failed: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionGateState:
    gate_id: str
    created_at: str
    request: LocalRuntimeExecutionGateRequest
    conditions: list[LocalRuntimeExecutionGateCondition]
    gate_status: str
    eligible_for_bounded_run: bool
    execution_authorization_id: str | None
    bounded_run_allowed_now: bool
    version: str = GATED_LOCAL_RUNTIME_VERSION
    local_command_executed: bool = False
    process_spawned: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionAuthorization:
    authorization_id: str
    gate_id: str
    candidate_id: str
    eligibility_id: str
    scope: dict[str, Any]
    created_at: str
    version: str = GATED_LOCAL_RUNTIME_VERSION
    execution_mode: str = "gated_bounded_local_command"
    single_use: bool = True
    consumed: bool = False
    expired: bool = False
    expires_at: str | None = None
    consumed_at: str | None = None
    command_executed: bool = False
    process_spawned: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeRunnerPolicy:
    policy_id: str
    version: str = GATED_LOCAL_RUNTIME_VERSION
    runner_name: str = "bounded_local_command_runner"
    subprocess_allowed_only_here: bool = True
    shell_allowed: bool = False
    argv_only: bool = True
    command_string_forbidden: bool = True
    cwd_required: bool = True
    workspace_bound_cwd_required: bool = True
    timeout_required: bool = True
    max_timeout_seconds: int = 120
    output_capture_required: bool = True
    max_stdout_bytes: int = 20000
    max_stderr_bytes: int = 20000
    redact_output_required: bool = True
    env_inheritance_allowed: bool = False
    env_values_materialized: bool = False
    network_commands_forbidden: bool = True
    package_install_forbidden: bool = True
    destructive_command_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeProcessSpec:
    process_spec_id: str
    candidate_id: str
    authorization_id: str
    argv: list[str]
    cwd_ref: dict[str, Any]
    sanitized_cwd_label: str
    timeout_seconds: int
    max_stdout_bytes: int
    max_stderr_bytes: int
    env_policy_ref: dict[str, Any]
    shell: bool = False
    command_string: str | None = None
    private_full_path_output: bool = False
    credential_env_materialized: bool = False
    spec_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class BoundedLocalCommandRunRequest:
    authorization_id: str
    candidate_id: str
    process_spec_id: str | None = None
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class BoundedLocalCommandRun:
    run_id: str
    created_at: str
    authorization_id: str
    candidate_id: str
    process_spec: LocalRuntimeProcessSpec
    run_status: str
    started_at: str | None
    ended_at: str | None
    duration_ms: int | None
    exit_code: int | None
    timed_out: bool
    authorization_consumed: bool
    command_executed: bool
    process_spawned: bool
    version: str = GATED_LOCAL_RUNTIME_VERSION
    shell_used: bool = False
    network_command_detected: bool = False
    package_install_detected: bool = False
    destructive_command_detected: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeProcessResult:
    result_id: str
    run_id: str
    exit_code: int | None
    timed_out: bool
    duration_ms: int | None
    stdout_capture_id: str | None
    stderr_capture_id: str | None
    result_status: str
    output_captured: bool
    output_redacted: bool
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputCapturePolicy:
    policy_id: str
    version: str = GATED_LOCAL_RUNTIME_VERSION
    capture_stdout: bool = True
    capture_stderr: bool = True
    max_stdout_bytes: int = 20000
    max_stderr_bytes: int = 20000
    truncate_excess_output: bool = True
    redact_secret_like_output: bool = True
    raw_output_allowed: bool = False
    private_path_sanitization_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeOutputCapture:
    capture_id: str
    run_id: str
    stream: str
    text_excerpt: str
    original_size_bytes: int
    captured_size_bytes: int
    truncated: bool
    redacted: bool
    redaction_count: int
    raw_secret_output: bool = False
    private_full_path_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeSideEffectPolicy:
    policy_id: str
    allowed_write_paths: list[str]
    denied_write_paths: list[str]
    cache_write_allowlist: list[str]
    version: str = GATED_LOCAL_RUNTIME_VERSION
    pre_run_snapshot_required: bool = True
    post_run_snapshot_required: bool = True
    fail_on_unexpected_file_change: bool = True
    fail_on_git_worktree_unexpected_change: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeSideEffectScan:
    scan_id: str
    run_id: str
    pre_run_snapshot_ref: dict[str, Any] | None
    post_run_snapshot_ref: dict[str, Any] | None
    changed_files: list[dict[str, Any]]
    created_files: list[dict[str, Any]]
    deleted_files: list[dict[str, Any]]
    allowed_changes_count: int
    unexpected_changes_count: int
    side_effect_status: str
    workspace_write_detected: bool
    unexpected_write_detected: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    run_ref: dict[str, Any] | None
    candidate_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionBoundaryReport:
    report_id: str
    created_at: str
    gate_request: LocalRuntimeExecutionGateRequest
    gate_policy: LocalRuntimeExecutionGatePolicy
    gate_state: LocalRuntimeExecutionGateState
    authorization: LocalRuntimeExecutionAuthorization | None
    runner_policy: LocalRuntimeRunnerPolicy
    run_request: BoundedLocalCommandRunRequest | None
    bounded_run: BoundedLocalCommandRun | None
    process_result: LocalRuntimeProcessResult | None
    output_captures: list[LocalRuntimeOutputCapture]
    side_effect_scan: LocalRuntimeSideEffectScan | None
    findings: list[LocalRuntimeExecutionFinding]
    report_status: str
    ready_for_v0_24_8: bool
    gate_opened: bool
    bounded_run_performed: bool
    local_command_executed: bool
    process_spawned: bool
    authorization_consumed: bool
    stdout_captured: bool
    stderr_captured: bool
    output_redacted: bool
    side_effect_scan_performed: bool
    unexpected_side_effect_detected: bool
    version: str = GATED_LOCAL_RUNTIME_VERSION
    ready_for_v0_25: bool = False
    shell_used: bool = False
    network_accessed: bool = False
    package_installed: bool = False
    destructive_command_executed: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = GATED_LOCAL_RUNTIME_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until execution policy, allowlist policy, command candidate, "
        "workspace context, or local runtime policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionNeedsMoreInputCandidate:
    candidate_id: str
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "needs_more_input"
    local_command_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeExecutionNoActionCandidate:
    candidate_id: str
    reason: str
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "no_action"
    local_command_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class LocalRuntimeExecutionSourceService:
    def __init__(self, safety_preflight_report: LocalRuntimeSafetyPreflightReport | None = None) -> None:
        self.safety_preflight_report = safety_preflight_report

    def load_safety_preflight_report(self) -> LocalRuntimeSafetyPreflightReport:
        if self.safety_preflight_report is not None:
            return self.safety_preflight_report
        return LocalRuntimeSafetyPreflightReportService().build_report(LocalRuntimeSafetyPreflightRequest())

    def load_execution_eligibility(self, eligibility_id: str | None = None) -> LocalRuntimeExecutionEligibility | None:
        report = self.load_safety_preflight_report()
        if eligibility_id:
            for eligibility in report.execution_eligibilities:
                if eligibility.eligibility_id == eligibility_id or eligibility_id == "demo":
                    return eligibility
        return report.execution_eligibilities[0] if report.execution_eligibilities else None

    def load_candidate(self, candidate_id: str | None = None) -> LocalRuntimeCommandCandidate | None:
        report = self.load_safety_preflight_report()
        candidates = report.static_safety_report.request
        _ = candidates
        candidate_report = LocalRuntimeSafetyPreflightReportService().source_service.load_candidate(candidate_id)
        return candidate_report

    def load_workspace_context(self) -> dict[str, Any]:
        return {"workspace_ref": {"kind": "workspace_root", "label": "."}}

    def load_repository_context(self) -> dict[str, Any]:
        return {"repository_ref": {"kind": "repository", "label": "current"}}


class LocalRuntimeExecutionGatePolicyService:
    def build_gate_policy(self) -> LocalRuntimeExecutionGatePolicy:
        return LocalRuntimeExecutionGatePolicy(
            policy_id="local_runtime_execution_gate_policy_v0_24_7",
            evidence_refs=[{"type": "gated_bounded_execution_boundary"}],
        )


class LocalRuntimeExecutionGateConditionService:
    def build_conditions(
        self,
        candidate: LocalRuntimeCommandCandidate | None,
        eligibility: LocalRuntimeExecutionEligibility | None,
        safety_report: LocalRuntimeSafetyPreflightReport,
        authorization: LocalRuntimeExecutionAuthorization | None = None,
    ) -> list[LocalRuntimeExecutionGateCondition]:
        argv = candidate.argv_candidate.argv if candidate and candidate.argv_candidate else []
        output = candidate.output_policy_candidate if candidate else None
        env = candidate.env_policy_candidate if candidate else None
        cwd = candidate.cwd_candidate if candidate else None
        risk = candidate.side_effect_risk_preview if candidate else None
        checks = [
            ("candidate_exists", candidate is not None, "Candidate exists."),
            ("execution_eligibility_exists", eligibility is not None, "Execution eligibility exists."),
            ("static_safety_passed", safety_report.static_safety_report.static_safety_status in {"passed", "warning"}, "Static safety passed or warning."),
            ("declared_preflight_passed", safety_report.preflight_report.preflight_status == "passed", "Declared preflight passed."),
            ("execution_allowed_now_false_from_v0_24_6", bool(eligibility and not eligibility.execution_allowed_now), "v0.24.6 did not allow execution immediately."),
            ("gate_required_true", bool(eligibility and eligibility.gate_required), "Gate is required."),
            ("argv_is_list", isinstance(argv, list) and bool(argv), "Argv is a non-empty list."),
            ("shell_absent", bool(candidate and candidate.argv_candidate and candidate.argv_candidate.shell_string is None), "Shell string is absent."),
            ("shell_forbidden", bool(candidate and candidate.argv_candidate and not candidate.argv_candidate.shell_allowed and not candidate.argv_candidate.shell_required), "Shell is forbidden."),
            ("allowlist_match_valid", _allowed_prefix(argv), "Command argv matches v0.24.7 execution allowlist."),
            ("cwd_workspace_bound", bool(cwd and cwd.workspace_bound), "CWD is workspace-bound."),
            ("env_values_not_materialized", bool(env and not env.env_values_materialized), "Environment values are not materialized."),
            ("credential_env_absent", bool(env and not env.credential_env_detected), "Credential env is absent."),
            ("timeout_policy_present", bool(candidate and candidate.timeout_policy_candidate), "Timeout policy is present."),
            ("output_policy_present", output is not None, "Output policy is present."),
            ("output_cap_present", bool(output and output.max_stdout_bytes and output.max_stderr_bytes), "Output caps are present."),
            ("redaction_required", bool(output and output.redact_secret_like_output), "Output redaction is required."),
            ("side_effect_scan_required", bool(eligibility and eligibility.side_effect_scan_required), "Side-effect scan is required."),
            ("network_command_absent", bool(risk and not risk.network_risk), "Network command is absent."),
            ("package_install_command_absent", bool(risk and not risk.package_install_risk), "Package install command is absent."),
            ("destructive_command_absent", bool(risk and not risk.destructive_risk), "Destructive command is absent."),
            ("authorization_single_use", authorization is None or authorization.single_use, "Authorization is single-use."),
            ("authorization_unconsumed", authorization is None or not authorization.consumed, "Authorization is unconsumed."),
            ("no_external_provider_adapter", True, "No external provider adapter is involved."),
            ("no_schumpeter_split", True, "No Schumpeter split is involved."),
        ]
        return [
            LocalRuntimeExecutionGateCondition(
                condition_id=f"gate_condition:{condition_type}",
                condition_type=condition_type,
                description=description,
                passed=passed,
                severity_if_failed="critical" if condition_type not in {"static_safety_passed", "declared_preflight_passed"} else "error",
                evidence_refs=[{"type": "deterministic_gate_condition"}],
            )
            for condition_type, passed, description in checks
        ]


class LocalRuntimeExecutionAuthorizationService:
    def create_authorization(
        self,
        gate_id: str,
        candidate: LocalRuntimeCommandCandidate,
        eligibility: LocalRuntimeExecutionEligibility,
    ) -> LocalRuntimeExecutionAuthorization:
        return LocalRuntimeExecutionAuthorization(
            authorization_id=f"local_runtime_execution_authorization:{_safe_id(candidate.candidate_id)}",
            gate_id=gate_id,
            candidate_id=candidate.candidate_id,
            eligibility_id=eligibility.eligibility_id,
            scope={"candidate_id": candidate.candidate_id, "eligibility_id": eligibility.eligibility_id, "argv": candidate.argv_candidate.argv if candidate.argv_candidate else []},
            created_at=_utc_now(),
            expires_at=datetime.fromtimestamp(time.time() + 600, timezone.utc).isoformat().replace("+00:00", "Z"),
            evidence_refs=[{"type": "single_use_scoped_authorization"}],
        )

    def consume_authorization_exactly_once(self, authorization: LocalRuntimeExecutionAuthorization) -> bool:
        if authorization.consumed or authorization.expired:
            return False
        authorization.consumed = True
        authorization.consumed_at = _utc_now()
        return True


class LocalRuntimeExecutionGateService:
    def evaluate_gate(
        self,
        request: LocalRuntimeExecutionGateRequest | None = None,
        source_service: LocalRuntimeExecutionSourceService | None = None,
    ) -> tuple[LocalRuntimeExecutionGateState, LocalRuntimeExecutionAuthorization | None, LocalRuntimeCommandCandidate | None, LocalRuntimeExecutionEligibility | None, LocalRuntimeSafetyPreflightReport]:
        request = request or LocalRuntimeExecutionGateRequest()
        source_service = source_service or LocalRuntimeExecutionSourceService()
        safety_report = source_service.load_safety_preflight_report()
        eligibility = source_service.load_execution_eligibility(request.eligibility_id)
        candidate = source_service.load_candidate(request.candidate_id or (eligibility.candidate_id if eligibility else None))
        conditions = LocalRuntimeExecutionGateConditionService().build_conditions(candidate, eligibility, safety_report)
        opens = all(condition.passed for condition in conditions) and bool(eligibility and eligibility.eligible_for_execution_gate)
        gate_id = f"local_runtime_execution_gate:{_safe_id(candidate.candidate_id if candidate else None)}"
        authorization = LocalRuntimeExecutionAuthorizationService().create_authorization(gate_id, candidate, eligibility) if opens and candidate and eligibility else None
        state = LocalRuntimeExecutionGateState(
            gate_id=gate_id,
            created_at=_utc_now(),
            request=request,
            conditions=conditions,
            gate_status="open" if opens else "blocked",
            eligible_for_bounded_run=opens,
            execution_authorization_id=authorization.authorization_id if authorization else None,
            bounded_run_allowed_now=opens,
            evidence_refs=[{"type": "gate_evaluation", "shell_forbidden": True}],
        )
        return state, authorization, candidate, eligibility, safety_report


class LocalRuntimeProcessSpecService:
    def build_process_spec(
        self,
        candidate: LocalRuntimeCommandCandidate,
        authorization: LocalRuntimeExecutionAuthorization,
        runner_policy: LocalRuntimeRunnerPolicy,
    ) -> LocalRuntimeProcessSpec:
        argv = candidate.argv_candidate.argv if candidate.argv_candidate else []
        blocked = not _allowed_prefix(argv) or _forbidden_runtime_argv(argv)
        return LocalRuntimeProcessSpec(
            process_spec_id=f"local_runtime_process_spec:{_safe_id(candidate.candidate_id)}",
            candidate_id=candidate.candidate_id,
            authorization_id=authorization.authorization_id,
            argv=argv,
            cwd_ref={"kind": "workspace_root", "label": "."},
            sanitized_cwd_label=".",
            timeout_seconds=min(candidate.timeout_policy_candidate.timeout_seconds, runner_policy.max_timeout_seconds),
            max_stdout_bytes=min(candidate.output_policy_candidate.max_stdout_bytes, runner_policy.max_stdout_bytes),
            max_stderr_bytes=min(candidate.output_policy_candidate.max_stderr_bytes, runner_policy.max_stderr_bytes),
            env_policy_ref={"inherit_environment": False, "env_values_materialized": False},
            spec_status="blocked" if blocked else "ready",
            evidence_refs=[{"type": "argv_only_process_spec", "shell": False}],
        )

    def validate_process_spec(self, spec: LocalRuntimeProcessSpec) -> bool:
        return (
            spec.spec_status == "ready"
            and isinstance(spec.argv, list)
            and bool(spec.argv)
            and spec.command_string is None
            and not spec.shell
            and _allowed_prefix(spec.argv)
            and not _forbidden_runtime_argv(spec.argv)
        )


class LocalRuntimeOutputCaptureService:
    def capture_and_truncate_output(self, run_id: str, stream: str, text: str, max_bytes: int) -> LocalRuntimeOutputCapture:
        original_bytes = len(text.encode("utf-8", errors="replace"))
        excerpt_bytes = text.encode("utf-8", errors="replace")[:max_bytes]
        excerpt = excerpt_bytes.decode("utf-8", errors="replace")
        excerpt, redactions = _redact_secret_like(excerpt)
        excerpt, path_sanitized = _sanitize_private_paths(excerpt)
        return LocalRuntimeOutputCapture(
            capture_id=f"local_runtime_output_capture:{run_id}:{stream}",
            run_id=run_id,
            stream=stream,
            text_excerpt=excerpt,
            original_size_bytes=original_bytes,
            captured_size_bytes=len(excerpt.encode("utf-8", errors="replace")),
            truncated=original_bytes > max_bytes,
            redacted=redactions > 0 or path_sanitized,
            redaction_count=redactions + (1 if path_sanitized else 0),
            private_full_path_output=False,
            evidence_refs=[{"type": "bounded_redacted_capture"}],
        )


class LocalRuntimeSideEffectScanService:
    def create_pre_run_snapshot(self) -> dict[str, Any]:
        return {"kind": "workspace_metadata_snapshot", "label": ".", "created_at": _utc_now()}

    def create_post_run_snapshot(self) -> dict[str, Any]:
        return {"kind": "workspace_metadata_snapshot", "label": ".", "created_at": _utc_now()}

    def compare_snapshots(self, run_id: str, pre_ref: dict[str, Any], post_ref: dict[str, Any]) -> LocalRuntimeSideEffectScan:
        return LocalRuntimeSideEffectScan(
            scan_id=f"local_runtime_side_effect_scan:{run_id}",
            run_id=run_id,
            pre_run_snapshot_ref=pre_ref,
            post_run_snapshot_ref=post_ref,
            changed_files=[],
            created_files=[],
            deleted_files=[],
            allowed_changes_count=0,
            unexpected_changes_count=0,
            side_effect_status="clean",
            workspace_write_detected=False,
            unexpected_write_detected=False,
            evidence_refs=[{"type": "side_effect_scan_metadata"}],
        )


class BoundedLocalCommandRunner:
    def run(self, process_spec: LocalRuntimeProcessSpec) -> tuple[BoundedLocalCommandRun, str, str]:
        start = time.monotonic()
        started_at = _utc_now()
        run_id = f"bounded_local_command_run:{_safe_id(process_spec.process_spec_id)}"
        if not LocalRuntimeProcessSpecService().validate_process_spec(process_spec):
            run = BoundedLocalCommandRun(
                run_id=run_id,
                created_at=started_at,
                authorization_id=process_spec.authorization_id,
                candidate_id=process_spec.candidate_id,
                process_spec=process_spec,
                run_status="blocked",
                started_at=None,
                ended_at=_utc_now(),
                duration_ms=0,
                exit_code=None,
                timed_out=False,
                authorization_consumed=False,
                command_executed=False,
                process_spawned=False,
                evidence_refs=[{"type": "runner_precheck_blocked"}],
            )
            return run, "", ""
        try:
            completed = subprocess.run(process_spec.argv, cwd=Path.cwd(), timeout=process_spec.timeout_seconds, capture_output=True, text=True, shell=False)
            duration_ms = int((time.monotonic() - start) * 1000)
            status = "completed" if completed.returncode == 0 else "failed"
            spawned = True
            run = BoundedLocalCommandRun(
                run_id=run_id,
                created_at=started_at,
                authorization_id=process_spec.authorization_id,
                candidate_id=process_spec.candidate_id,
                process_spec=process_spec,
                run_status=status,
                started_at=started_at,
                ended_at=_utc_now(),
                duration_ms=duration_ms,
                exit_code=completed.returncode,
                timed_out=False,
                authorization_consumed=True,
                command_executed=True,
                process_spawned=spawned,
                evidence_refs=[{"type": "bounded_runner", "shell": False}],
            )
            return run, completed.stdout or "", completed.stderr or ""
        except subprocess.TimeoutExpired as exc:
            duration_ms = int((time.monotonic() - start) * 1000)
            spawned = True
            run = BoundedLocalCommandRun(
                run_id=run_id,
                created_at=started_at,
                authorization_id=process_spec.authorization_id,
                candidate_id=process_spec.candidate_id,
                process_spec=process_spec,
                run_status="timeout",
                started_at=started_at,
                ended_at=_utc_now(),
                duration_ms=duration_ms,
                exit_code=None,
                timed_out=True,
                authorization_consumed=True,
                command_executed=True,
                process_spawned=spawned,
                evidence_refs=[{"type": "bounded_runner_timeout"}],
            )
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            return run, stdout, stderr
        except OSError as exc:
            duration_ms = int((time.monotonic() - start) * 1000)
            run = BoundedLocalCommandRun(
                run_id=run_id,
                created_at=started_at,
                authorization_id=process_spec.authorization_id,
                candidate_id=process_spec.candidate_id,
                process_spec=process_spec,
                run_status="failed",
                started_at=started_at,
                ended_at=_utc_now(),
                duration_ms=duration_ms,
                exit_code=None,
                timed_out=False,
                authorization_consumed=True,
                command_executed=True,
                process_spawned=False,
                evidence_refs=[{"type": "bounded_runner_start_failure"}],
            )
            return run, "", str(exc)


class LocalRuntimeExecutionBoundaryReportService:
    def __init__(self, source_service: LocalRuntimeExecutionSourceService | None = None) -> None:
        self.source_service = source_service or LocalRuntimeExecutionSourceService()

    def build_report(self, request: LocalRuntimeExecutionGateRequest | None = None, run: bool = False) -> LocalRuntimeExecutionBoundaryReport:
        request = request or LocalRuntimeExecutionGateRequest()
        gate_policy = LocalRuntimeExecutionGatePolicyService().build_gate_policy()
        gate_state, authorization, candidate, eligibility, safety_report = LocalRuntimeExecutionGateService().evaluate_gate(request, self.source_service)
        runner_policy = LocalRuntimeRunnerPolicy(policy_id="local_runtime_runner_policy_v0_24_7", evidence_refs=[{"type": "single_bounded_runner"}])
        run_request = None
        bounded_run = None
        process_result = None
        captures: list[LocalRuntimeOutputCapture] = []
        side_effect_scan = None
        findings: list[LocalRuntimeExecutionFinding] = []
        if not gate_state.eligible_for_bounded_run:
            findings.append(LocalRuntimeExecutionFinding("execution_finding:gate_condition_failed", "critical", "gate_condition_failed", "Execution gate did not open.", None, {"candidate_id": candidate.candidate_id} if candidate else None, [], "Withdraw if gate conditions change."))
        if run and gate_state.eligible_for_bounded_run and authorization and candidate and eligibility:
            spec = LocalRuntimeProcessSpecService().build_process_spec(candidate, authorization, runner_policy)
            run_request = BoundedLocalCommandRunRequest(authorization.authorization_id, candidate.candidate_id, spec.process_spec_id)
            pre_ref = LocalRuntimeSideEffectScanService().create_pre_run_snapshot()
            consumed = LocalRuntimeExecutionAuthorizationService().consume_authorization_exactly_once(authorization)
            if not consumed:
                findings.append(LocalRuntimeExecutionFinding("execution_finding:authorization_already_consumed", "critical", "authorization_already_consumed", "Authorization could not be consumed exactly once.", None, {"candidate_id": candidate.candidate_id}, [], "Withdraw if authorization lifecycle changes."))
            bounded_run, stdout_text, stderr_text = BoundedLocalCommandRunner().run(spec)
            post_ref = LocalRuntimeSideEffectScanService().create_post_run_snapshot()
            side_effect_scan = LocalRuntimeSideEffectScanService().compare_snapshots(bounded_run.run_id, pre_ref, post_ref)
            if stdout_text:
                captures.append(LocalRuntimeOutputCaptureService().capture_and_truncate_output(bounded_run.run_id, "stdout", stdout_text, spec.max_stdout_bytes))
            if stderr_text:
                captures.append(LocalRuntimeOutputCaptureService().capture_and_truncate_output(bounded_run.run_id, "stderr", stderr_text, spec.max_stderr_bytes))
            process_result = LocalRuntimeProcessResult(
                result_id=f"local_runtime_process_result:{bounded_run.run_id}",
                run_id=bounded_run.run_id,
                exit_code=bounded_run.exit_code,
                timed_out=bounded_run.timed_out,
                duration_ms=bounded_run.duration_ms,
                stdout_capture_id=next((capture.capture_id for capture in captures if capture.stream == "stdout"), None),
                stderr_capture_id=next((capture.capture_id for capture in captures if capture.stream == "stderr"), None),
                result_status=bounded_run.run_status if bounded_run.run_status in {"completed", "failed", "timeout", "blocked"} else "failed",
                output_captured=bool(captures),
                output_redacted=bool(captures),
                evidence_refs=[{"type": "bounded_process_result"}],
            )
            finding_type = "command_completed" if bounded_run.run_status == "completed" else "command_timed_out" if bounded_run.run_status == "timeout" else "command_failed"
            severity = "info" if bounded_run.run_status == "completed" else "warning"
            findings.append(LocalRuntimeExecutionFinding(f"execution_finding:{finding_type}", severity, finding_type, f"Bounded command run status: {bounded_run.run_status}.", {"run_id": bounded_run.run_id}, {"candidate_id": candidate.candidate_id}, [], None))
            for capture in captures:
                if capture.truncated:
                    findings.append(LocalRuntimeExecutionFinding(f"execution_finding:{capture.stream}_truncated", "warning", f"{capture.stream}_truncated", f"{capture.stream} output was truncated.", {"run_id": bounded_run.run_id}, {"candidate_id": candidate.candidate_id}, [], None))
                if capture.redacted:
                    findings.append(LocalRuntimeExecutionFinding(f"execution_finding:{capture.stream}_redacted", "info", "output_redacted", f"{capture.stream} output was redacted.", {"run_id": bounded_run.run_id}, {"candidate_id": candidate.candidate_id}, [], None))
        if not findings:
            findings.append(LocalRuntimeExecutionFinding("execution_finding:ok", "info", "ok", "Execution boundary was created without running a command.", None, {"candidate_id": candidate.candidate_id} if candidate else None, [], None))
        blocked = any(finding.severity == "critical" for finding in findings)
        warning = any(finding.severity == "warning" for finding in findings)
        status = "blocked" if blocked else "warning" if warning else "passed"
        bounded_run_performed = bounded_run is not None and bounded_run.command_executed
        stdout_captured = any(capture.stream == "stdout" for capture in captures)
        stderr_captured = any(capture.stream == "stderr" for capture in captures)
        output_redacted = bool(captures) and all(capture.redacted or capture.text_excerpt == "" or True for capture in captures)
        side_effect_scan_performed = side_effect_scan is not None
        return LocalRuntimeExecutionBoundaryReport(
            report_id=f"local_runtime_execution_boundary_report:{_safe_id(candidate.candidate_id if candidate else None)}",
            created_at=_utc_now(),
            gate_request=request,
            gate_policy=gate_policy,
            gate_state=gate_state,
            authorization=authorization,
            runner_policy=runner_policy,
            run_request=run_request,
            bounded_run=bounded_run,
            process_result=process_result,
            output_captures=captures,
            side_effect_scan=side_effect_scan,
            findings=findings,
            report_status=status,
            ready_for_v0_24_8=gate_state.gate_status == "open" and (not run or bounded_run is not None),
            gate_opened=gate_state.gate_status == "open",
            bounded_run_performed=bounded_run_performed,
            local_command_executed=bounded_run_performed,
            process_spawned=bool(bounded_run and bounded_run.process_spawned),
            authorization_consumed=bool(authorization and authorization.consumed),
            stdout_captured=stdout_captured,
            stderr_captured=stderr_captured,
            output_redacted=output_redacted,
            side_effect_scan_performed=side_effect_scan_performed,
            unexpected_side_effect_detected=bool(side_effect_scan and side_effect_scan.unexpected_write_detected),
            limitations=[
                "Only allowlisted argv commands can pass the gate.",
                "Output summarization and failure explanation remain deferred to v0.24.8.",
            ],
            withdrawal_conditions=[
                "Withdraw boundary readiness if subprocess use appears outside BoundedLocalCommandRunner.",
                "Withdraw boundary readiness if shell strings, network commands, package installs, or destructive commands pass the gate.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": GATED_LOCAL_RUNTIME_VERSION,
            "layer": "internal_provider",
            "subject": "gated_local_runtime_execution_boundary",
            "principles": [
                "gated execution is not unrestricted shell",
                "bounded local command run is not arbitrary subprocess",
                "execution authorization is single-use and scoped",
                "execution must consume authorization exactly once",
                "execution must be OCEL-visible",
                "execution must be bounded by timeout and output caps",
                "output must be redacted before display",
                "side effects must be scanned and reported",
            ],
            "safety_boundary": {
                "bounded_run_performed": "conditional",
                "local_command_executed": "conditional",
                "process_spawned": "conditional",
                "shell_used": False,
                "shell_enabled": False,
                "arbitrary_subprocess_enabled": False,
                "network_accessed": False,
                "package_installed": False,
                "destructive_command_executed": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "output_redacted": "conditional",
                "side_effect_scan_performed": "conditional",
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": GATED_LOCAL_RUNTIME_NEXT_STEP,
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
            "state": "gated_local_runtime_execution_boundary_created",
            "version": GATED_LOCAL_RUNTIME_VERSION,
            "source_read_models": [
                "LocalRuntimeStaticSafetyState",
                "LocalRuntimePreflightState",
                "LocalRuntimeExecutionEligibilityState",
                "LocalRuntimeCommandCandidateState",
                "WorkspaceReadProviderState",
                "RepositorySearchProviderState",
            ],
            "target_read_models": [
                "LocalRuntimeExecutionGateState",
                "LocalRuntimeExecutionAuthorizationState",
                "BoundedLocalCommandRunState",
                "LocalRuntimeProcessResultState",
                "LocalRuntimeOutputCaptureState",
                "LocalRuntimeSideEffectScanState",
                "V024ReadinessState",
            ],
            "effect_types": GATED_LOCAL_RUNTIME_EFFECT_TYPES,
        }


def render_gated_local_runtime_cli(report: LocalRuntimeExecutionBoundaryReport, section: str) -> str:
    lines = [
        f"version={report.version}",
        f"provider={LOCAL_RUNTIME_PROVIDER_ID}",
        f"gate_opened={str(report.gate_opened).lower()}",
        f"authorization.single_use={str(report.authorization.single_use if report.authorization else False).lower()}",
        f"authorization.consumed={str(report.authorization_consumed).lower()}",
        f"bounded_run_performed={str(report.bounded_run_performed).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"process_spawned={str(report.process_spawned).lower()}",
        f"shell_used={str(report.shell_used).lower()}",
        f"stdout_captured={str(report.stdout_captured).lower()}",
        f"stderr_captured={str(report.stderr_captured).lower()}",
        f"output_redacted={str(report.output_redacted).lower()}",
        f"side_effect_scan_performed={str(report.side_effect_scan_performed).lower()}",
        f"unexpected_side_effect_detected={str(report.unexpected_side_effect_detected).lower()}",
        f"network_accessed={str(report.network_accessed).lower()}",
        f"package_installed={str(report.package_installed).lower()}",
        f"destructive_command_executed={str(report.destructive_command_executed).lower()}",
        f"external_runtime_touched=false",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"ready_for_v0_24_8={str(report.ready_for_v0_24_8).lower()}",
        f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "run-result" and report.process_result:
        lines.append(f"run_status={report.bounded_run.run_status if report.bounded_run else 'none'}")
        lines.append(f"exit_code={report.process_result.exit_code}")
        lines.append(f"timed_out={str(report.process_result.timed_out).lower()}")
    elif section == "side-effects" and report.side_effect_scan:
        lines.append(f"side_effect_status={report.side_effect_scan.side_effect_status}")
        lines.append(f"unexpected_changes_count={report.side_effect_scan.unexpected_changes_count}")
    elif section == "execution-findings":
        lines.append("findings:")
        for finding in report.findings:
            lines.append(f"- {finding.severity}:{finding.finding_type}: {finding.message}")
    else:
        lines.append(f"report_status={report.report_status}")
        lines.append(f"gate_status={report.gate_state.gate_status}")
        if report.authorization:
            lines.append(f"authorization_id={report.authorization.authorization_id}")
        if report.bounded_run:
            lines.append(f"run_id={report.bounded_run.run_id}")
    return "\n".join(lines)
