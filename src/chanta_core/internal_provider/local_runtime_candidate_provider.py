from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
import time
from typing import Any

from chanta_core.internal_provider.registry import InternalProviderRegistryReportService


LOCAL_RUNTIME_CANDIDATE_VERSION = "v0.24.5"
LOCAL_RUNTIME_PROVIDER_ID = "local_runtime_provider"
LOCAL_RUNTIME_CANDIDATE_VERSION_NAME = "Local Runtime Command Candidate Provider"
LOCAL_RUNTIME_CANDIDATE_KOREAN_NAME = "로컬 런타임 명령 후보 Provider"
LOCAL_RUNTIME_CANDIDATE_NEXT_STEP = "v0.24.6 Local Runtime Static Safety / Preflight"

LOCAL_RUNTIME_CANDIDATE_OBJECT_TYPES = [
    "local_runtime_command_candidate_policy",
    "local_runtime_intent_descriptor",
    "local_runtime_command_template",
    "local_runtime_command_template_catalog",
    "local_command_argv_candidate",
    "local_command_cwd_candidate",
    "local_command_environment_policy_candidate",
    "local_command_timeout_policy_candidate",
    "local_command_output_policy_candidate",
    "local_command_side_effect_risk_preview",
    "local_runtime_command_candidate",
    "local_runtime_command_candidate_set",
    "local_runtime_command_candidate_finding",
    "local_runtime_command_candidate_report",
    "local_runtime_command_needs_more_input_candidate",
    "local_runtime_command_no_action_candidate",
    "internal_provider_registry",
    "internal_provider_capability_surface",
    "workspace_tree_snapshot",
    "repository_file_provider_report",
    "process_state_inspection_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

LOCAL_RUNTIME_CANDIDATE_EVENT_TYPES = [
    "local_runtime_command_candidate_requested",
    "local_runtime_command_candidate_policy_created",
    "local_runtime_intent_classified",
    "local_runtime_command_template_catalog_created",
    "local_runtime_command_template_selected",
    "local_command_argv_candidate_created",
    "local_command_cwd_candidate_created",
    "local_command_environment_policy_candidate_created",
    "local_command_timeout_policy_candidate_created",
    "local_command_output_policy_candidate_created",
    "local_command_side_effect_risk_preview_created",
    "local_runtime_command_candidate_created",
    "local_runtime_command_candidate_set_created",
    "local_runtime_command_candidate_report_created",
    "local_runtime_command_candidate_warning_created",
    "local_runtime_command_candidate_blocked",
]

LOCAL_RUNTIME_CANDIDATE_RELATION_TYPES = [
    "uses_local_runtime_provider",
    "uses_internal_provider_registry",
    "uses_workspace_tree_snapshot",
    "uses_repository_context",
    "uses_process_state_context",
    "classifies_local_runtime_intent",
    "selects_command_template",
    "creates_argv_candidate",
    "creates_cwd_candidate",
    "defines_env_policy_candidate",
    "defines_timeout_policy_candidate",
    "defines_output_policy_candidate",
    "previews_side_effect_risk",
    "creates_local_runtime_command_candidate",
    "candidate_requires_static_safety",
    "candidate_requires_preflight",
    "candidate_requires_execution_gate",
    "defers_static_safety_to_v0_24_6",
    "defers_preflight_to_v0_24_6",
    "defers_execution_gate_to_v0_24_7",
    "not_local_command_executed",
    "not_process_spawned",
    "not_shell_executed",
    "not_subprocess_called",
    "not_external_runtime_touched",
    "prevents_credential_exposure",
    "defers_general_agent_usability_to_v0_25",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_internal_provider_registry",
    "derived_from_workspace_context",
    "derived_from_repository_context",
    "derived_from_process_state_context",
]

LOCAL_RUNTIME_CANDIDATE_EFFECT_TYPES = [
    "read_only_observation",
    "local_command_candidate_created",
    "local_runtime_intent_classified",
    "state_candidate_created",
]

LOCAL_RUNTIME_CANDIDATE_FORBIDDEN_EFFECT_TYPES = [
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

COMMAND_CATEGORIES = {
    "version_check",
    "diagnostic",
    "test",
    "lint",
    "typecheck",
    "compile_check",
    "repo_status",
    "format_check",
    "package_info",
    "unknown",
}

FINDING_TYPES_V0245 = [
    "ok",
    "missing_local_runtime_provider_surface",
    "unsupported_command_intent",
    "unknown_command_category",
    "missing_target_scope",
    "unresolved_target_path",
    "unresolved_argv_placeholder",
    "shell_string_detected",
    "shell_required_detected",
    "forbidden_arg_detected",
    "network_command_detected",
    "package_install_command_detected",
    "destructive_command_detected",
    "credential_arg_detected",
    "credential_env_detected",
    "cwd_outside_workspace",
    "private_cwd_path_sanitized",
    "missing_timeout_policy",
    "missing_output_policy",
    "static_safety_required_next",
    "preflight_required_next",
    "execution_gate_required_future",
    "local_command_execution_attempted",
    "subprocess_detected",
    "provider_api_call_performed",
    "external_runtime_touched",
    "process_spawn_attempted",
    "stdout_capture_attempted",
    "stderr_capture_attempted",
    "raw_secret_output_detected",
    "vendor_hardcoding_detected",
    "growthkernel_dependency_detected",
    "schumpeter_split_detected",
    "general_agent_usability_premature",
    "llm_judge_detected",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_id(value: str | None) -> str:
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", value or "none")[:120] or "none"


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


def _contains_secret_like(text: str) -> bool:
    return bool(re.search(r"(token|secret|password|api[_-]?key|credential)", text, re.I))


def _contains_placeholder(argv: list[str]) -> bool:
    return any("{" in part or "}" in part for part in argv)


def _status_from_blockers(blocked: bool, needs_input: bool, no_action: bool) -> str:
    if blocked:
        return "blocked"
    if no_action:
        return "no_action"
    if needs_input:
        return "needs_more_input"
    return "ready_for_static_safety"


@dataclass
class LocalRuntimeCommandCandidatePolicy:
    policy_id: str
    version: str = LOCAL_RUNTIME_CANDIDATE_VERSION
    provider_id: str = LOCAL_RUNTIME_PROVIDER_ID
    candidate_only: bool = True
    execution_enabled: bool = False
    local_command_execution_enabled: bool = False
    shell_allowed: bool = False
    shell_string_allowed: bool = False
    argv_required: bool = True
    cwd_required: bool = True
    workspace_bound_cwd_required: bool = True
    timeout_policy_required: bool = True
    output_policy_required: bool = True
    side_effect_risk_preview_required: bool = True
    static_safety_required_next: bool = True
    preflight_required_next: bool = True
    execution_gate_required_future: bool = True
    network_commands_forbidden: bool = True
    package_install_forbidden: bool = True
    destructive_commands_forbidden: bool = True
    credential_env_forbidden: bool = True
    secret_output_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeIntentDescriptor:
    intent_id: str
    goal_text: str
    raw_intent_text: str | None
    normalized_intent: str
    command_category: str
    target_scope: str
    risk_preview: str
    needs_more_input: bool
    no_action_recommended: bool
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandTemplate:
    template_id: str
    command_category: str
    template_name: str
    description: str
    argv_template: list[str]
    allowed_tools: list[str]
    forbidden_args: list[str]
    activation_version: str = LOCAL_RUNTIME_CANDIDATE_VERSION
    execution_version: str | None = "v0.24.7"
    candidate_only: bool = True
    shell_required: bool = False
    network_risk: bool = False
    package_install_risk: bool = False
    destructive_risk: bool = False
    workspace_write_risk: bool = False
    static_safety_required: bool = True
    preflight_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandTemplateCatalog:
    catalog_id: str
    templates: list[LocalRuntimeCommandTemplate]
    template_count: int
    categories: list[str]
    catalog_status: str
    version: str = LOCAL_RUNTIME_CANDIDATE_VERSION
    execution_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalCommandArgvCandidate:
    argv_candidate_id: str
    template_id: str | None
    argv: list[str]
    contains_unresolved_placeholders: bool
    contains_forbidden_args: bool
    network_risk_detected: bool
    package_install_risk_detected: bool
    destructive_risk_detected: bool
    credential_arg_detected: bool
    candidate_status: str
    argv_materialized: bool = True
    shell_string: str | None = None
    shell_required: bool = False
    shell_allowed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalCommandCwdCandidate:
    cwd_candidate_id: str
    cwd_ref: dict[str, Any] | None
    sanitized_cwd_label: str | None
    workspace_bound: bool
    private_full_path_output: bool = False
    cwd_status: str = "ready_for_static_safety"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalCommandEnvironmentPolicyCandidate:
    env_policy_candidate_id: str
    allowed_env_keys: list[str]
    denied_env_keys: list[str]
    inherit_environment: bool = False
    credential_env_detected: bool = False
    env_values_materialized: bool = False
    env_policy_status: str = "ready_for_static_safety"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalCommandTimeoutPolicyCandidate:
    timeout_policy_candidate_id: str
    timeout_seconds: int
    timeout_required: bool = True
    timeout_status: str = "ready_for_static_safety"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalCommandOutputPolicyCandidate:
    output_policy_candidate_id: str
    max_stdout_bytes: int
    max_stderr_bytes: int
    capture_stdout: bool = True
    capture_stderr: bool = True
    redact_secret_like_output: bool = True
    raw_output_allowed: bool = False
    output_policy_status: str = "ready_for_static_safety"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalCommandSideEffectRiskPreview:
    risk_preview_id: str
    command_category: str
    workspace_write_risk: bool
    file_delete_risk: bool
    network_risk: bool
    package_install_risk: bool
    destructive_risk: bool
    credential_exposure_risk: bool
    shell_risk: bool
    risk_level: str
    requires_static_safety: bool = True
    requires_preflight: bool = True
    requires_execution_gate: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandCandidate:
    candidate_id: str
    created_at: str
    intent: LocalRuntimeIntentDescriptor
    template: LocalRuntimeCommandTemplate | None
    argv_candidate: LocalCommandArgvCandidate | None
    cwd_candidate: LocalCommandCwdCandidate | None
    env_policy_candidate: LocalCommandEnvironmentPolicyCandidate
    timeout_policy_candidate: LocalCommandTimeoutPolicyCandidate
    output_policy_candidate: LocalCommandOutputPolicyCandidate
    side_effect_risk_preview: LocalCommandSideEffectRiskPreview
    candidate_status: str
    version: str = LOCAL_RUNTIME_CANDIDATE_VERSION
    static_safety_checked: bool = False
    preflight_checked: bool = False
    execution_gate_opened: bool = False
    local_command_executed: bool = False
    process_spawned: bool = False
    stdout_captured: bool = False
    stderr_captured: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandCandidateSet:
    candidate_set_id: str
    request_ref: dict[str, Any]
    candidates: list[LocalRuntimeCommandCandidate]
    selected_candidate_id: str | None
    candidate_count: int
    ready_for_static_safety_count: int
    needs_more_input_count: int
    no_action_count: int
    blocked_count: int
    set_status: str
    version: str = LOCAL_RUNTIME_CANDIDATE_VERSION
    execution_performed: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandCandidateFinding:
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
class LocalRuntimeCommandCandidateReport:
    report_id: str
    created_at: str
    policy: LocalRuntimeCommandCandidatePolicy
    template_catalog: LocalRuntimeCommandTemplateCatalog
    candidate_set: LocalRuntimeCommandCandidateSet
    findings: list[LocalRuntimeCommandCandidateFinding]
    report_status: str
    ready_for_v0_24_6: bool
    command_candidate_created: bool
    version: str = LOCAL_RUNTIME_CANDIDATE_VERSION
    ready_for_v0_25: bool = False
    static_safety_checked: bool = False
    preflight_checked: bool = False
    execution_gate_opened: bool = False
    local_command_executed: bool = False
    process_spawned: bool = False
    stdout_captured: bool = False
    stderr_captured: bool = False
    external_provider_adapter_implemented: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = LOCAL_RUNTIME_CANDIDATE_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until command template catalog, workspace context, repository "
        "context, or local runtime policy changes."
    )

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandNeedsMoreInputCandidate:
    candidate_id: str
    reason: str
    missing_inputs: list[str]
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "needs_more_input"
    local_command_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class LocalRuntimeCommandNoActionCandidate:
    candidate_id: str
    reason: str
    evidence_refs: list[dict[str, Any]]
    candidate_status: str = "no_action"
    local_command_executed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class LocalRuntimeProviderSurfaceSourceService:
    def load_internal_provider_contract(self) -> dict[str, Any]:
        return {"version": "v0.24.0", "status": "available"}

    def load_provider_registry(self) -> dict[str, Any]:
        return InternalProviderRegistryReportService().build_report().to_dict()

    def load_local_runtime_provider_surface(self) -> dict[str, Any] | None:
        report = self.load_provider_registry()
        surfaces = report.get("capability_surfaces") or report.get("registry", {}).get("capability_surfaces", [])
        for surface in surfaces:
            if surface.get("provider_id") in {LOCAL_RUNTIME_PROVIDER_ID, f"internal_provider:{LOCAL_RUNTIME_PROVIDER_ID}"}:
                return surface
        return None

    def load_workspace_snapshot_if_available(self) -> dict[str, Any] | None:
        return {"workspace_ref": {"kind": "workspace_root", "label": "."}}

    def load_repository_context_if_available(self) -> dict[str, Any] | None:
        return {"repository_ref": {"kind": "repository", "label": "current"}}

    def load_process_state_context_if_available(self) -> dict[str, Any] | None:
        return {"process_state_ref": {"kind": "process_state_inspection_report", "version": "v0.24.4"}}


class LocalRuntimeCommandCandidatePolicyService:
    def build_policy(self) -> LocalRuntimeCommandCandidatePolicy:
        return LocalRuntimeCommandCandidatePolicy(
            policy_id="local_runtime_command_candidate_policy_v0_24_5",
            evidence_refs=[{"type": "version", "version": LOCAL_RUNTIME_CANDIDATE_VERSION}],
        )


class LocalRuntimeIntentClassifier:
    def classify_intent(
        self,
        goal_text: str | None = None,
        request_context: dict[str, Any] | None = None,
    ) -> LocalRuntimeIntentDescriptor:
        context = request_context or {}
        raw = goal_text if goal_text is not None else context.get("goal")
        text = (raw or context.get("category") or "").strip()
        normalized = re.sub(r"\s+", " ", text.lower()).strip()
        explicit_category = context.get("category")
        category = explicit_category if explicit_category in COMMAND_CATEGORIES else "unknown"
        if category == "unknown":
            if "version" in normalized:
                category = "version_check"
            elif "status" in normalized or "diff" in normalized:
                category = "repo_status"
            elif "pytest" in normalized or "test" in normalized:
                category = "test"
            elif "ruff" in normalized or "lint" in normalized:
                category = "lint"
            elif "mypy" in normalized or "type" in normalized:
                category = "typecheck"
            elif "compile" in normalized:
                category = "compile_check"
            elif "diagnostic" in normalized or "diagnose" in normalized:
                category = "diagnostic"
        target = context.get("target") or context.get("target_path")
        needs_target = category in {"test", "lint", "typecheck", "compile_check", "format_check"}
        target_scope = "unknown"
        if category in {"version_check", "repo_status", "diagnostic"}:
            target_scope = "repository" if category == "repo_status" else "workspace"
        elif target:
            target_scope = "file" if "." in str(target).split("/")[-1] else "directory"
        risk = "read_only"
        if category == "compile_check":
            risk = "medium"
        if category == "unknown":
            risk = "unknown"
        needs_input = category == "unknown" or (needs_target and not target)
        return LocalRuntimeIntentDescriptor(
            intent_id=f"local_runtime_intent:{_safe_id(category)}:{_safe_id(normalized)}",
            goal_text=text or "unknown local runtime command candidate request",
            raw_intent_text=raw,
            normalized_intent=normalized or "unknown",
            command_category=category,
            target_scope=target_scope,
            risk_preview=risk,
            needs_more_input=needs_input,
            no_action_recommended=False,
            evidence_refs=[{"type": "deterministic_classifier", "version": LOCAL_RUNTIME_CANDIDATE_VERSION}],
        )


class LocalRuntimeCommandTemplateCatalogService:
    def build_catalog(self) -> LocalRuntimeCommandTemplateCatalog:
        forbidden = ["-c", "install", "uninstall", "delete", "remove", "rm", "rmdir", "del", "reset", "push", "--force"]
        specs = [
            ("python_version_check_candidate", "version_check", "Python version check", ["python", "--version"]),
            ("git_status_short_candidate", "repo_status", "Git short status", ["git", "status", "--short"]),
            ("git_diff_stat_candidate", "repo_status", "Git diff stat", ["git", "diff", "--stat"]),
            ("python_compileall_candidate", "compile_check", "Python compileall candidate", ["python", "-m", "compileall", "{target_path}"]),
            ("pytest_candidate", "test", "Pytest candidate", ["python", "-m", "pytest", "{target_path}"]),
            ("ruff_check_candidate", "lint", "Ruff check candidate", ["python", "-m", "ruff", "check", "{target_path}"]),
            ("mypy_candidate", "typecheck", "Mypy candidate", ["python", "-m", "mypy", "{target_path}"]),
        ]
        templates = [
            LocalRuntimeCommandTemplate(
                template_id=template_id,
                command_category=category,
                template_name=name,
                description=f"Inert argv descriptor for {name}; not execution authorization.",
                argv_template=argv,
                allowed_tools=[argv[0]],
                forbidden_args=forbidden,
                workspace_write_risk=template_id == "python_compileall_candidate",
            )
            for template_id, category, name, argv in specs
        ]
        return LocalRuntimeCommandTemplateCatalog(
            catalog_id="local_runtime_command_template_catalog_v0_24_5",
            templates=templates,
            template_count=len(templates),
            categories=sorted({template.command_category for template in templates}),
            catalog_status="declared",
            evidence_refs=[{"type": "inert_template_catalog", "candidate_only": True}],
        )

    def find_templates_for_intent(
        self,
        intent: LocalRuntimeIntentDescriptor,
        catalog: LocalRuntimeCommandTemplateCatalog | None = None,
    ) -> list[LocalRuntimeCommandTemplate]:
        source = catalog or self.build_catalog()
        return [template for template in source.templates if template.command_category == intent.command_category]


class LocalCommandArgvCandidateService:
    forbidden_args = {"-c", "install", "uninstall", "delete", "remove", "rm", "rmdir", "del", "reset", "push", "force", "--force", "--global"}
    network_tools = {"curl", "wget", "ssh", "scp"}
    package_tools = {"pip", "npm"}
    destructive_args = {"delete", "remove", "rm", "rmdir", "del", "reset", "--force"}

    def build_argv_candidate(
        self,
        intent: LocalRuntimeIntentDescriptor,
        template: LocalRuntimeCommandTemplate | None,
        target_context: dict[str, Any] | None = None,
    ) -> LocalCommandArgvCandidate:
        context = target_context or {}
        if template is None:
            return LocalCommandArgvCandidate(
                argv_candidate_id=f"argv_candidate:{_safe_id(intent.intent_id)}",
                template_id=None,
                argv=[],
                contains_unresolved_placeholders=False,
                contains_forbidden_args=False,
                network_risk_detected=False,
                package_install_risk_detected=False,
                destructive_risk_detected=False,
                credential_arg_detected=False,
                candidate_status="needs_more_input",
            )
        target = context.get("target") or context.get("target_path")
        argv = [part.replace("{target_path}", str(target) if target else "{target_path}") for part in template.argv_template]
        unresolved = _contains_placeholder(argv)
        lower_parts = [part.lower() for part in argv]
        forbidden = any(part in self.forbidden_args for part in lower_parts)
        network = any(part in self.network_tools for part in lower_parts)
        package = any(part in self.package_tools or part in {"install", "--install"} for part in lower_parts)
        destructive = any(part in self.destructive_args for part in lower_parts)
        credential = any(_contains_secret_like(part) for part in argv)
        status = _status_from_blockers(
            blocked=network or package or destructive or credential or forbidden,
            needs_input=unresolved,
            no_action=False,
        )
        return LocalCommandArgvCandidate(
            argv_candidate_id=f"argv_candidate:{template.template_id}:{_safe_id(str(target))}",
            template_id=template.template_id,
            argv=argv,
            contains_unresolved_placeholders=unresolved,
            contains_forbidden_args=forbidden,
            network_risk_detected=network,
            package_install_risk_detected=package,
            destructive_risk_detected=destructive,
            credential_arg_detected=credential,
            candidate_status=status,
            evidence_refs=[{"type": "argv_descriptor", "candidate_only": True}],
        )


class LocalCommandCwdCandidateService:
    def build_cwd_candidate(
        self,
        intent: LocalRuntimeIntentDescriptor,
        workspace_context: dict[str, Any] | None = None,
    ) -> LocalCommandCwdCandidate:
        context = workspace_context or {}
        workspace_bound = context.get("workspace_bound", True)
        return LocalCommandCwdCandidate(
            cwd_candidate_id=f"cwd_candidate:{_safe_id(intent.intent_id)}",
            cwd_ref={"kind": "workspace_root", "label": "."} if workspace_bound else None,
            sanitized_cwd_label="." if workspace_bound else None,
            workspace_bound=workspace_bound,
            private_full_path_output=False,
            cwd_status="ready_for_static_safety" if workspace_bound else "needs_more_input",
            evidence_refs=[{"type": "sanitized_workspace_cwd"}],
        )


class LocalCommandEnvironmentPolicyCandidateService:
    def build_env_policy_candidate(self, intent: LocalRuntimeIntentDescriptor, env_keys: list[str] | None = None) -> LocalCommandEnvironmentPolicyCandidate:
        keys = env_keys or []
        credential = any(_contains_secret_like(key) for key in keys)
        return LocalCommandEnvironmentPolicyCandidate(
            env_policy_candidate_id=f"env_policy_candidate:{_safe_id(intent.intent_id)}",
            allowed_env_keys=[],
            denied_env_keys=["TOKEN", "SECRET", "PASSWORD", "API_KEY", "CREDENTIAL"],
            credential_env_detected=credential,
            env_policy_status="blocked" if credential else "ready_for_static_safety",
            evidence_refs=[{"type": "environment_policy", "env_values_materialized": False}],
        )


class LocalCommandTimeoutPolicyCandidateService:
    def build_timeout_policy_candidate(self, intent: LocalRuntimeIntentDescriptor, risk_preview: LocalCommandSideEffectRiskPreview | None = None) -> LocalCommandTimeoutPolicyCandidate:
        timeout = 30 if intent.command_category == "version_check" else 120 if intent.command_category == "test" else 60
        return LocalCommandTimeoutPolicyCandidate(
            timeout_policy_candidate_id=f"timeout_policy_candidate:{_safe_id(intent.intent_id)}",
            timeout_seconds=timeout,
            evidence_refs=[{"type": "timeout_policy", "required": True}],
        )


class LocalCommandOutputPolicyCandidateService:
    def build_output_policy_candidate(self, intent: LocalRuntimeIntentDescriptor, risk_preview: LocalCommandSideEffectRiskPreview | None = None) -> LocalCommandOutputPolicyCandidate:
        return LocalCommandOutputPolicyCandidate(
            output_policy_candidate_id=f"output_policy_candidate:{_safe_id(intent.intent_id)}",
            max_stdout_bytes=20000,
            max_stderr_bytes=20000,
            evidence_refs=[{"type": "output_policy", "raw_output_allowed": False}],
        )


class LocalCommandSideEffectRiskPreviewService:
    def build_risk_preview(
        self,
        intent: LocalRuntimeIntentDescriptor,
        argv_candidate: LocalCommandArgvCandidate | None,
    ) -> LocalCommandSideEffectRiskPreview:
        argv = argv_candidate.argv if argv_candidate else []
        text = " ".join(argv).lower()
        workspace_write = intent.command_category in {"compile_check"}
        file_delete = any(part in text for part in [" rm ", " del ", "delete", "rmdir"])
        network = bool(argv_candidate and argv_candidate.network_risk_detected)
        package = bool(argv_candidate and argv_candidate.package_install_risk_detected)
        destructive = bool(argv_candidate and argv_candidate.destructive_risk_detected)
        credential = bool(argv_candidate and argv_candidate.credential_arg_detected)
        shell_risk = bool(argv_candidate and argv_candidate.shell_required)
        if network:
            level = "blocked"
        elif package:
            level = "blocked"
        elif destructive or credential or shell_risk:
            level = "blocked"
        elif workspace_write:
            level = "medium"
        else:
            level = "read_only" if intent.risk_preview == "read_only" else "unknown"
        return LocalCommandSideEffectRiskPreview(
            risk_preview_id=f"risk_preview:{_safe_id(intent.intent_id)}",
            command_category=intent.command_category,
            workspace_write_risk=workspace_write,
            file_delete_risk=file_delete,
            network_risk=network,
            package_install_risk=package,
            destructive_risk=destructive,
            credential_exposure_risk=credential,
            shell_risk=shell_risk,
            risk_level=level,
            evidence_refs=[{"type": "deterministic_risk_preview"}],
        )


class LocalRuntimeCommandCandidateService:
    def build_candidate(self, request: dict[str, Any] | None = None) -> LocalRuntimeCommandCandidate:
        request = request or {}
        intent = LocalRuntimeIntentClassifier().classify_intent(request.get("goal"), request)
        catalog_service = LocalRuntimeCommandTemplateCatalogService()
        catalog = catalog_service.build_catalog()
        template = next(iter(catalog_service.find_templates_for_intent(intent, catalog)), None)
        argv_candidate = LocalCommandArgvCandidateService().build_argv_candidate(intent, template, request)
        cwd_candidate = LocalCommandCwdCandidateService().build_cwd_candidate(intent, {"workspace_bound": request.get("workspace_bound", True)})
        env_candidate = LocalCommandEnvironmentPolicyCandidateService().build_env_policy_candidate(intent, request.get("env_keys"))
        risk_preview = LocalCommandSideEffectRiskPreviewService().build_risk_preview(intent, argv_candidate)
        timeout_candidate = LocalCommandTimeoutPolicyCandidateService().build_timeout_policy_candidate(intent, risk_preview)
        output_candidate = LocalCommandOutputPolicyCandidateService().build_output_policy_candidate(intent, risk_preview)
        blocked = any(
            status == "blocked"
            for status in [
                argv_candidate.candidate_status,
                cwd_candidate.cwd_status,
                env_candidate.env_policy_status,
                timeout_candidate.timeout_status,
                output_candidate.output_policy_status,
            ]
        ) or risk_preview.risk_level == "blocked"
        needs_input = intent.needs_more_input or any(
            status == "needs_more_input"
            for status in [argv_candidate.candidate_status, cwd_candidate.cwd_status]
        )
        status = _status_from_blockers(blocked=blocked, needs_input=needs_input, no_action=intent.no_action_recommended)
        return LocalRuntimeCommandCandidate(
            candidate_id=f"local_runtime_command_candidate:{_safe_id(intent.command_category)}:{_safe_id(request.get('target') or request.get('goal'))}",
            created_at=_utc_now(),
            intent=intent,
            template=template,
            argv_candidate=argv_candidate,
            cwd_candidate=cwd_candidate,
            env_policy_candidate=env_candidate,
            timeout_policy_candidate=timeout_candidate,
            output_policy_candidate=output_candidate,
            side_effect_risk_preview=risk_preview,
            candidate_status=status,
            evidence_refs=[{"type": "candidate_only", "local_command_executed": False}],
        )


class LocalRuntimeCommandCandidateSetService:
    def build_candidate_set(self, request: dict[str, Any] | None = None) -> LocalRuntimeCommandCandidateSet:
        request = request or {}
        candidate = LocalRuntimeCommandCandidateService().build_candidate(request)
        candidates = [candidate]
        counts = {
            "ready_for_static_safety": sum(1 for item in candidates if item.candidate_status == "ready_for_static_safety"),
            "needs_more_input": sum(1 for item in candidates if item.candidate_status == "needs_more_input"),
            "no_action": sum(1 for item in candidates if item.candidate_status == "no_action"),
            "blocked": sum(1 for item in candidates if item.candidate_status == "blocked"),
        }
        set_status = candidate.candidate_status
        return LocalRuntimeCommandCandidateSet(
            candidate_set_id=f"local_runtime_command_candidate_set:{_safe_id(request.get('goal') or request.get('category'))}",
            request_ref={"kind": "local_runtime_command_candidate_request", "goal": request.get("goal"), "category": request.get("category"), "target": request.get("target")},
            candidates=candidates,
            selected_candidate_id=candidate.candidate_id if candidate.candidate_status == "ready_for_static_safety" else None,
            candidate_count=len(candidates),
            ready_for_static_safety_count=counts["ready_for_static_safety"],
            needs_more_input_count=counts["needs_more_input"],
            no_action_count=counts["no_action"],
            blocked_count=counts["blocked"],
            set_status=set_status,
            evidence_refs=[{"type": "candidate_set", "execution_performed": False}],
        )


class LocalRuntimeCommandCandidateFindingService:
    def build_findings(self, candidate_set: LocalRuntimeCommandCandidateSet, provider_surface_declared: bool = True) -> list[LocalRuntimeCommandCandidateFinding]:
        findings: list[LocalRuntimeCommandCandidateFinding] = []

        def add(severity: str, finding_type: str, message: str, candidate: LocalRuntimeCommandCandidate | None = None) -> None:
            findings.append(
                LocalRuntimeCommandCandidateFinding(
                    finding_id=f"finding:{finding_type}:{len(findings) + 1}",
                    severity=severity,
                    finding_type=finding_type,
                    message=message,
                    candidate_ref={"candidate_id": candidate.candidate_id} if candidate else None,
                    evidence_refs=[{"type": "deterministic_boundary_check", "version": LOCAL_RUNTIME_CANDIDATE_VERSION}],
                    withdrawal_condition="Withdraw if the referenced candidate metadata changes.",
                )
            )

        if not provider_surface_declared:
            add("error", "missing_local_runtime_provider_surface", "local_runtime_provider surface is not declared.")
        for candidate in candidate_set.candidates:
            intent = candidate.intent
            argv = candidate.argv_candidate
            cwd = candidate.cwd_candidate
            env = candidate.env_policy_candidate
            if intent.command_category == "unknown":
                add("warning", "unknown_command_category", "Command category is unknown.", candidate)
            if intent.needs_more_input:
                add("warning", "unsupported_command_intent" if intent.command_category == "unknown" else "unresolved_target_path", "Intent requires more input.", candidate)
            if argv:
                if argv.contains_unresolved_placeholders:
                    add("warning", "unresolved_argv_placeholder", "Argv contains unresolved placeholders.", candidate)
                if argv.shell_string is not None:
                    add("critical", "shell_string_detected", "Shell string is forbidden for v0.24.5 candidates.", candidate)
                if argv.shell_required:
                    add("critical", "shell_required_detected", "Shell-required template is forbidden.", candidate)
                if argv.contains_forbidden_args:
                    add("error", "forbidden_arg_detected", "Forbidden argv token detected.", candidate)
                if argv.network_risk_detected:
                    add("critical", "network_command_detected", "Network command candidate is blocked.", candidate)
                if argv.package_install_risk_detected:
                    add("critical", "package_install_command_detected", "Package install candidate is blocked.", candidate)
                if argv.destructive_risk_detected:
                    add("critical", "destructive_command_detected", "Destructive command candidate is blocked.", candidate)
                if argv.credential_arg_detected:
                    add("critical", "credential_arg_detected", "Credential-like argv token detected.", candidate)
            if cwd:
                if not cwd.workspace_bound:
                    add("critical", "cwd_outside_workspace", "CWD is not workspace-bound.", candidate)
                if cwd.private_full_path_output:
                    add("warning", "private_cwd_path_sanitized", "Private full CWD path must be sanitized.", candidate)
            if env.credential_env_detected:
                add("critical", "credential_env_detected", "Credential-like environment key detected.", candidate)
            if not candidate.timeout_policy_candidate:
                add("error", "missing_timeout_policy", "Timeout policy candidate is required.", candidate)
            if not candidate.output_policy_candidate:
                add("error", "missing_output_policy", "Output policy candidate is required.", candidate)
            add("info", "static_safety_required_next", "Static safety is deferred to v0.24.6.", candidate)
            add("info", "preflight_required_next", "Preflight is deferred to v0.24.6.", candidate)
            add("info", "execution_gate_required_future", "Execution gate is deferred to v0.24.7.", candidate)
        if not findings:
            add("info", "ok", "Local runtime command candidate report has no blocking finding.")
        return findings


class LocalRuntimeCommandCandidateReportService:
    def build_report(self, request: dict[str, Any] | None = None) -> LocalRuntimeCommandCandidateReport:
        request = request or {}
        source = LocalRuntimeProviderSurfaceSourceService()
        provider_surface_declared = source.load_local_runtime_provider_surface() is not None
        policy = LocalRuntimeCommandCandidatePolicyService().build_policy()
        catalog = LocalRuntimeCommandTemplateCatalogService().build_catalog()
        candidate_set = LocalRuntimeCommandCandidateSetService().build_candidate_set(request)
        findings = LocalRuntimeCommandCandidateFindingService().build_findings(candidate_set, provider_surface_declared)
        critical = any(finding.severity == "critical" for finding in findings)
        errors = any(finding.severity == "error" for finding in findings)
        warnings = any(finding.severity == "warning" for finding in findings)
        if critical or candidate_set.blocked_count:
            status = "blocked"
        elif errors:
            status = "failed"
        elif warnings or any(f.finding_type in {"static_safety_required_next", "preflight_required_next", "execution_gate_required_future"} for f in findings):
            status = "warning"
        else:
            status = "passed"
        ready = candidate_set.ready_for_static_safety_count > 0 and status != "blocked"
        return LocalRuntimeCommandCandidateReport(
            report_id=f"local_runtime_command_candidate_report:{_safe_id(request.get('goal') or request.get('category'))}",
            created_at=_utc_now(),
            policy=policy,
            template_catalog=catalog,
            candidate_set=candidate_set,
            findings=findings,
            report_status=status,
            ready_for_v0_24_6=ready,
            command_candidate_created=candidate_set.candidate_count > 0,
            limitations=[
                "Candidates are inert descriptors only.",
                "Static safety, declared preflight, and execution gate are deferred.",
            ],
            withdrawal_conditions=[
                "Withdraw readiness if any candidate is executed before v0.24.7 gate.",
                "Withdraw readiness if shell strings, credential material, or private full paths are introduced.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": LOCAL_RUNTIME_CANDIDATE_VERSION,
            "layer": "internal_provider",
            "subject": "local_runtime_command_candidate_provider",
            "principles": [
                "command candidate is not command execution",
                "argv candidate is not process spawn",
                "command template is not allowlist approval",
                "candidate creation is not static safety pass",
                "candidate creation is not runtime preflight",
                "candidate creation is not execution authorization",
                "local runtime provider is not unrestricted shell",
            ],
            "safety_boundary": {
                "command_candidate_created": "conditional",
                "static_safety_checked": False,
                "preflight_checked": False,
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
            "next_step": LOCAL_RUNTIME_CANDIDATE_NEXT_STEP,
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
            "state": "local_runtime_command_candidate_created",
            "version": LOCAL_RUNTIME_CANDIDATE_VERSION,
            "source_read_models": [
                "InternalProviderRegistryState",
                "InternalProviderCapabilitySurfaceState",
                "WorkspaceReadProviderState",
                "RepositorySearchProviderState",
                "ProcessStateInspectionState",
            ],
            "target_read_models": [
                "LocalRuntimeCommandCandidateState",
                "LocalRuntimeIntentState",
                "LocalCommandArgvCandidateState",
                "LocalCommandPolicyCandidateState",
                "LocalRuntimeSafetyEligibilityState",
                "V024ReadinessState",
            ],
            "effect_types": LOCAL_RUNTIME_CANDIDATE_EFFECT_TYPES,
        }


class LocalRuntimeCommandCandidateSkillService:
    def list_skills(self) -> list[dict[str, Any]]:
        return [
            {
                "skill_id": "skill:local_runtime_command_candidate_create",
                "status": "implemented",
                "version": LOCAL_RUNTIME_CANDIDATE_VERSION,
                "candidate_only": True,
                "local_command_execution_enabled": False,
            },
            {"skill_id": "skill:local_runtime_static_safety_check", "status": "contract_only"},
            {"skill_id": "skill:local_runtime_preflight_check", "status": "contract_only"},
            {"skill_id": "skill:local_runtime_execution_gate", "status": "contract_only"},
            {"skill_id": "skill:bounded_local_command_run", "status": "contract_only"},
            {"skill_id": "skill:local_runtime_output_summarize", "status": "contract_only"},
            {"skill_id": "skill:local_runtime_failure_explain", "status": "contract_only"},
        ]


def render_local_runtime_candidate_cli(report: LocalRuntimeCommandCandidateReport, section: str) -> str:
    lines = [
        f"version={report.version}",
        f"provider={report.policy.provider_id}",
        f"candidate_only={str(report.policy.candidate_only).lower()}",
        f"command_candidate_created={str(report.command_candidate_created).lower()}",
        f"static_safety_checked={str(report.static_safety_checked).lower()}",
        f"preflight_checked={str(report.preflight_checked).lower()}",
        f"execution_gate_opened={str(report.execution_gate_opened).lower()}",
        f"local_command_executed={str(report.local_command_executed).lower()}",
        f"process_spawned={str(report.process_spawned).lower()}",
        f"stdout_captured={str(report.stdout_captured).lower()}",
        f"stderr_captured={str(report.stderr_captured).lower()}",
        f"shell_allowed={str(report.policy.shell_allowed).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"ready_for_v0_24_6={str(report.ready_for_v0_24_6).lower()}",
        f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "templates":
        lines.append("templates:")
        for template in report.template_catalog.templates:
            lines.append(f"- {template.template_id}: argv={template.argv_template} candidate_only={str(template.candidate_only).lower()} shell_required={str(template.shell_required).lower()}")
    elif section == "findings":
        lines.append("findings:")
        for finding in report.findings:
            lines.append(f"- {finding.severity}:{finding.finding_type}: {finding.message}")
    else:
        lines.append(f"report_status={report.report_status}")
        lines.append(f"candidate_set_status={report.candidate_set.set_status}")
        for candidate in report.candidate_set.candidates:
            argv = candidate.argv_candidate.argv if candidate.argv_candidate else []
            lines.append(f"candidate={candidate.candidate_id} status={candidate.candidate_status} category={candidate.intent.command_category} argv={argv}")
    return "\n".join(lines)
