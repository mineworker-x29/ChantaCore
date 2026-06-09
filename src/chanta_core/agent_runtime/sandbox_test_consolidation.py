from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0379_VERSION = "v0.37.9"
FOUNDATION_RELEASE_NAME = "Controlled Sandbox Test Runner & Vera-Codex Agent Evaluation v1"

INCLUDED_V037_VERSIONS = [
    "v0.37.0",
    "v0.37.1",
    "v0.37.2",
    "v0.37.3",
    "v0.37.4",
    "v0.37.5",
    "v0.37.6",
    "v0.37.7",
    "v0.37.8",
]

V037_MODULES = [
    "sandbox_test_boundary",
    "sandbox_test_command_policy",
    "sandbox_test_execution",
    "sandbox_test_result",
    "sandbox_test_feedback",
    "sandbox_repair_suggestion",
    "vera_codex_trial",
    "agent_performance_evaluation",
    "sandbox_test_cli_surface",
]

V037_DOCS = [
    "docs/versions/v0.37/v0.37.0_controlled_sandbox_test_runner_boundary.md",
    "docs/versions/v0.37/v0.37.1_allowlisted_test_command_policy.md",
    "docs/versions/v0.37/v0.37.2_sandbox_test_execution_engine.md",
    "docs/versions/v0.37/v0.37.3_test_result_envelope.md",
    "docs/versions/v0.37/v0.37.4_test_feedback_failure_diagnosis.md",
    "docs/versions/v0.37/v0.37.5_repair_suggestion_metadata.md",
    "docs/versions/v0.37/v0.37.6_vera_codex_one_shot_trial.md",
    "docs/versions/v0.37/v0.37.7_cold_agent_performance_evaluation.md",
    "docs/versions/v0.37/v0.37.8_cli_test_runner_agent_evaluation_surface.md",
]

V037_TESTS = [
    "tests/test_v0370_sandbox_test_runner_boundary.py",
    "tests/test_v0371_allowlisted_test_command_policy.py",
    "tests/test_v0372_sandbox_test_execution_engine.py",
    "tests/test_v0373_test_result_envelope.py",
    "tests/test_v0374_test_feedback_failure_diagnosis.py",
    "tests/test_v0375_repair_suggestion_metadata.py",
    "tests/test_v0376_vera_codex_one_shot_trial.py",
    "tests/test_v0377_cold_agent_performance_evaluation.py",
    "tests/test_v0378_cli_test_runner_agent_evaluation_surface.py",
]

ENABLED_TEST_RUNNER_CAPABILITIES = [
    "controlled sandbox test runner boundary",
    "allowlisted test command policy",
    "test invocation contract",
    "structured command specs",
    "sandbox cwd policy",
    "timeout contract",
    "bounded output capture",
    "minimal environment contract",
    "controlled sandbox test execution through v0.37.2 helper boundaries",
    "controlled test subprocess via v0.37.2 only",
    "test result envelope",
    "test output classifier",
    "process exit classification",
    "failure class classification",
    "evidence snippet extraction and redaction",
    "test feedback report",
    "failure diagnosis report",
]

ENABLED_AGENT_EVALUATION_CAPABILITIES = [
    "repair suggestion metadata",
    "repair scope metadata",
    "repair human-review requirement",
    "do-nothing repair comparison",
    "future repair proposal input metadata",
    "Vera-Codex one-shot trial metadata",
    "Vera-Codex evidence bundle",
    "bounded decision trace without chain-of-thought",
    "mandatory stop reason",
    "mandatory human handoff",
    "cold agent performance evaluation",
    "evidence-grounded scorecard",
    "boundary compliance assessment",
    "mandatory do-nothing comparison",
    "failure condition assessment",
    "CLI Test Runner & Agent Evaluation Surface",
    "CLI dispatch to bounded v0.37 helpers",
]

PROHIBITED_CAPABILITIES = [
    "arbitrary_shell",
    "direct_subprocess",
    "uncontrolled_subprocess",
    "raw_pytest",
    "raw_unittest",
    "raw_npm_test",
    "package_script",
    "raw_pip",
    "dependency_install",
    "network_access",
    "direct_network_access",
    "live_workspace_write",
    "live_code_edit",
    "patch_application",
    "workspace_write",
    "code_edit",
    "apply_patch",
    "git_apply",
    "repair_patch_proposal",
    "repair_diff_generation",
    "code_hunk_generation",
    "automatic_repair",
    "repair_execution",
    "retry_loop",
    "multi_cycle_loop",
    "model_provider_invocation",
    "provider_invocation",
    "tool_execution",
    "external_agent_execution",
    "claude_code_invocation",
    "codex_cli_invocation",
    "OpenCode_execution",
    "Hermes_execution",
    "OpenClaw_execution",
    "Dominion_runtime",
    "infinite_loop",
    "infinite_agent_loop",
    "recursive_self_invocation",
    "credential_access",
    "secret_read",
    "general_agent_execution",
    "autonomous_agent_runtime",
    "independent_agent_runtime",
    "general_tool_execution",
    "unquarantined_action_execution",
    "persistent_trace_write",
    "external_trace_sink",
    "ocel_file_write",
    "jsonl_trace_write",
    "UI_runtime",
    "external_control",
    "authority_grant",
    "D4_D9_grant",
    "production_certification",
]

PROHIBITED_BOUNDARIES = [
    "arbitrary_shell",
    "direct_subprocess",
    "uncontrolled_subprocess",
    "raw_pytest",
    "package_script",
    "dependency_install",
    "network_access",
    "live_workspace_write",
    "live_code_edit",
    "patch_application",
    "apply_patch",
    "git_apply",
    "repair_patch_proposal",
    "repair_diff_generation",
    "code_hunk_generation",
    "automatic_repair",
    "repair_execution",
    "retry_loop",
    "multi_cycle_loop",
    "model_provider_invocation",
    "tool_execution",
    "external_agent_execution",
    "claude_code_invocation",
    "codex_cli_invocation",
    "dominion_runtime",
    "infinite_loop",
    "credential_access",
    "secret_read",
    "persistent_trace",
    "UI_runtime",
    "external_control",
    "authority_grant",
]

PROHIBITED_RUNTIME_SURFACES = [
    "shell",
    "direct_subprocess",
    "uncontrolled_subprocess",
    "dependency_install",
    "network_access",
    "live_write",
    "live_edit",
    "patch_apply",
    "repair_patch_proposal",
    "auto_repair",
    "model_invocation",
    "tool_execution",
    "external_agent",
    "Dominion",
    "credential_access",
    "persistent_trace",
    "UI",
    "authority",
]

RECOMMENDED_V038_ITEMS = [
    "bounded repair proposal boundary",
    "repair proposal evidence contract",
    "proposed diff metadata",
    "code hunk proposal metadata",
    "no apply by default",
    "human approval before apply",
    "sandbox-only proposal validation",
    "do-nothing comparison",
    "cold evaluation feedback integration",
]

FUTURE_TRACK_ITEMS = [
    "bounded repair proposal loop",
    "sandbox repair apply gate",
    "persistent trace store",
    "UI runtime",
    "external harness adapter",
    "Dominion runtime gated review",
]

WITHDRAWAL_CONDITIONS = [
    "withdraw if arbitrary shell or direct subprocess is introduced",
    "withdraw if repair suggestion metadata is treated as repair patch proposal",
    "withdraw if Vera-Codex trial is treated as model provider invocation or autonomous runtime",
    "withdraw if cold scorecard is treated as production certification",
    "withdraw if unsafe readiness flags become true",
]

UNSAFE_RELEASE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_shell_execution",
    "ready_for_direct_subprocess",
    "ready_for_uncontrolled_subprocess",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_repair_patch_proposal",
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_automatic_repair",
    "ready_for_repair_execution",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_model_provider_invocation",
    "ready_for_tool_execution",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_dominion_runtime",
    "ready_for_infinite_agent_loop",
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_independent_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

REPORT_UNSAFE_READY_NAMES = UNSAFE_RELEASE_FLAG_NAMES + (
    "ready_for_direct_network_access",
)


class SandboxTestRunnerConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class SandboxTestRunnerConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    CONTROLLED_SANDBOX_TEST_RUNNER_READY = "controlled_sandbox_test_runner_ready"
    TEST_RESULT_FEEDBACK_PIPELINE_READY = "test_result_feedback_pipeline_ready"
    VERA_CODEX_EVALUATION_READY = "vera_codex_evaluation_ready"
    CLI_SURFACE_READY = "cli_surface_ready"
    HANDOFF_READY_FOR_V038 = "handoff_ready_for_v038"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0379_VERSION not in version:
        raise ValueError("version must include v0.37.9")


def _validate_metadata(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.37.9")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True for v0.37.9 consolidation")


def _validate_versions_include_v037_track(included_versions: list[str]) -> None:
    _validate_string_list("included_versions", included_versions)
    missing = [version for version in INCLUDED_V037_VERSIONS if version not in included_versions]
    if missing:
        raise ValueError(f"included_versions missing {', '.join(missing)}")


def _contains_all(container: list[str], required: list[str]) -> bool:
    lowered = {item.lower() for item in container}
    return all(item.lower() in lowered for item in required)


def _contains_substrings(container: list[str], required: list[str]) -> bool:
    joined = " ".join(container).lower()
    return all(item.lower() in joined for item in required)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerReleaseFlagSet:
    flag_set_id: str
    version: str
    controlled_sandbox_test_runner_v1_ready: bool
    ready_for_v038_handoff: bool
    ready_for_test_runner_boundary: bool
    ready_for_controlled_test_command_policy: bool
    ready_for_test_invocation_contract: bool
    ready_for_controlled_sandbox_test_execution: bool
    ready_for_controlled_test_subprocess_via_v0372: bool
    ready_for_bounded_test_output_capture: bool
    ready_for_test_result_envelope: bool
    ready_for_test_output_classifier: bool
    ready_for_test_feedback_report: bool
    ready_for_failure_diagnosis_report: bool
    ready_for_repair_suggestion_metadata: bool
    ready_for_repair_scope_metadata: bool
    ready_for_future_repair_proposal_input: bool
    ready_for_vera_codex_one_shot_agent_trial: bool
    ready_for_vera_codex_evidence_bundle: bool
    ready_for_vera_codex_decision_trace: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_cold_agent_scorecard: bool
    ready_for_do_nothing_comparison: bool
    ready_for_cli_test_runner_surface: bool
    ready_for_cli_sandbox_test_run: bool
    ready_for_cli_vera_trial_run_once: bool
    ready_for_cli_cold_scorecard: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_shell_execution: bool
    ready_for_direct_subprocess: bool
    ready_for_uncontrolled_subprocess: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_automatic_repair: bool
    ready_for_repair_execution: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_model_provider_invocation: bool
    ready_for_tool_execution: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_provider_invocation: bool
    ready_for_direct_network_access: bool
    ready_for_credential_access: bool
    ready_for_secret_read: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_independent_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_ui_runtime: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    max_grantable_level: str | None
    future_track_levels: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_RELEASE_FLAG_NAMES)
        _validate_string_list("future_track_levels", self.future_track_levels)
        if self.max_grantable_level is not None and self.max_grantable_level not in {"D0_NONE", "D1_READ", "D2_PLAN", "D3_SIMULATE"}:
            raise ValueError("max_grantable_level must be None or <= D3_SIMULATE")
        for level in ("D4", "D5", "D6", "D7", "D8", "D9"):
            if not any(item.startswith(level) for item in self.future_track_levels):
                raise ValueError("D4-D9 must remain future-track when represented")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerEvaluationSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_artifact_groups: list[str]
    release_flags: SandboxTestRunnerReleaseFlagSet
    consolidation_status: SandboxTestRunnerConsolidationStatus | str
    readiness_level: SandboxTestRunnerConsolidationReadinessLevel | str
    summary: str
    enabled_test_runner_capabilities: list[str]
    enabled_agent_evaluation_capabilities: list[str]
    prohibited_capabilities: list[str]
    evidence_refs: list[str]
    known_gaps: list[str]
    known_risks: list[str]
    withdrawal_conditions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("snapshot_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if FOUNDATION_RELEASE_NAME not in self.release_name:
            raise ValueError("release_name should be Controlled Sandbox Test Runner & Vera-Codex Agent Evaluation v1")
        _validate_versions_include_v037_track(self.included_versions)
        for name in (
            "included_modules",
            "included_artifact_groups",
            "enabled_test_runner_capabilities",
            "enabled_agent_evaluation_capabilities",
            "prohibited_capabilities",
            "evidence_refs",
            "known_gaps",
            "known_risks",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        if not sandbox_test_runner_flags_preserve_no_unsafe_runtime(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        SandboxTestRunnerConsolidationStatus(self.consolidation_status)
        SandboxTestRunnerConsolidationReadinessLevel(self.readiness_level)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_test_runner_capabilities: list[str]
    enabled_agent_evaluation_capabilities: list[str]
    design_stage_capabilities: list[str]
    prohibited_capabilities: list[str]
    future_track_capabilities: list[str]
    capability_to_version: dict[str, str]
    prohibited_capability_to_reason: dict[str, str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("capability_matrix_id", self.capability_matrix_id)
        _validate_version(self.version)
        for name in (
            "enabled_test_runner_capabilities",
            "enabled_agent_evaluation_capabilities",
            "design_stage_capabilities",
            "prohibited_capabilities",
            "future_track_capabilities",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_dict("capability_to_version", self.capability_to_version)
        _validate_dict("prohibited_capability_to_reason", self.prohibited_capability_to_reason)
        if not _contains_substrings(
            self.enabled_test_runner_capabilities,
            ["boundary", "allowlisted", "invocation contract", "controlled sandbox test execution", "result envelope", "feedback report"],
        ):
            raise ValueError("enabled_test_runner_capabilities missing v0.37 bounded features")
        if not _contains_substrings(
            self.enabled_agent_evaluation_capabilities,
            ["repair suggestion metadata", "one-shot", "cold agent", "scorecard", "CLI"],
        ):
            raise ValueError("enabled_agent_evaluation_capabilities missing v0.37 evaluation features")
        if not _contains_all(self.prohibited_capabilities, PROHIBITED_CAPABILITIES):
            raise ValueError("prohibited_capabilities missing unsafe runtime capabilities")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerStageCoverage:
    coverage_id: str
    version: str
    stage_version: str
    covered_artifact_refs: list[str]
    missing_artifact_refs: list[str]
    covered_test_refs: list[str]
    missing_test_refs: list[str]
    covered_doc_refs: list[str]
    missing_doc_refs: list[str]
    coverage_notes: list[str]
    coverage_complete: bool
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("coverage_id", "stage_version"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in (
            "covered_artifact_refs",
            "missing_artifact_refs",
            "covered_test_refs",
            "missing_test_refs",
            "covered_doc_refs",
            "missing_doc_refs",
            "coverage_notes",
            "blocking_gaps",
            "non_blocking_gaps",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.coverage_complete and self.blocking_gaps:
            raise ValueError("coverage_complete cannot be True with blocking gaps")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestBoundaryCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxTestCommandPolicyCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxTestExecutionEngineCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxTestResultEnvelopeCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxTestFeedbackCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxRepairSuggestionCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class VeraCodexTrialCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class ColdAgentEvaluationCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class CLITestRunnerSurfaceCoverage(SandboxTestRunnerStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str]
    active_controlled_boundaries: list[str]
    active_agent_evaluation_boundaries: list[str]
    prohibited_boundaries: list[str]
    future_gate_boundaries: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version(self.version)
        for name in (
            "inherited_boundaries",
            "active_controlled_boundaries",
            "active_agent_evaluation_boundaries",
            "prohibited_boundaries",
            "future_gate_boundaries",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not _contains_all(self.prohibited_boundaries, PROHIBITED_BOUNDARIES):
            raise ValueError("prohibited_boundaries missing unsafe surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerRiskRegister:
    risk_register_id: str
    version: str
    known_risks: list[str]
    high_risk_surfaces: list[str]
    prohibited_runtime_surfaces: list[str]
    mitigations: list[str]
    unresolved_risks: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version(self.version)
        for name in (
            "known_risks",
            "high_risk_surfaces",
            "prohibited_runtime_surfaces",
            "mitigations",
            "unresolved_risks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not _contains_all(self.prohibited_runtime_surfaces, PROHIBITED_RUNTIME_SURFACES):
            raise ValueError("prohibited_runtime_surfaces missing unsafe surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    future_track_items: list[str]
    recommended_v038_items: list[str]
    recommended_later_items: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version(self.version)
        for name in (
            "blocking_gaps",
            "non_blocking_gaps",
            "future_track_items",
            "recommended_v038_items",
            "recommended_later_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not _contains_all(self.recommended_v038_items, RECOMMENDED_V038_ITEMS):
            raise ValueError("recommended_v038_items missing bounded repair proposal items")
        if not _contains_all(self.future_track_items, FUTURE_TRACK_ITEMS):
            raise ValueError("future_track_items missing expected future gates")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerReleaseManifest:
    release_manifest_id: str
    version: str
    release_name: str
    snapshot_id: str
    included_versions: list[str]
    included_modules: list[str]
    included_docs: list[str]
    included_tests: list[str]
    focused_test_command: str
    full_track_test_command: str
    release_flags: SandboxTestRunnerReleaseFlagSet
    known_gaps: list[str]
    known_risks: list[str]
    next_handoff_id: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("release_manifest_id", "release_name", "snapshot_id", "focused_test_command", "full_track_test_command"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if FOUNDATION_RELEASE_NAME not in self.release_name:
            raise ValueError("release_name should be foundation release name")
        _validate_versions_include_v037_track(self.included_versions)
        for name in ("included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        if not sandbox_test_runner_flags_preserve_no_unsafe_runtime(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class SandboxTestRunnerAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str]
    reviewed_test_refs: list[str]
    reviewed_doc_refs: list[str]
    boundary_checks: list[str]
    negative_runtime_checks: list[str]
    controlled_test_checks: list[str]
    agent_evaluation_checks: list[str]
    no_shell_execution_confirmed: bool
    no_direct_subprocess_confirmed: bool
    no_uncontrolled_subprocess_confirmed: bool
    controlled_subprocess_scoped_to_v0372_confirmed: bool
    no_raw_pytest_cli_execution_confirmed: bool
    no_dependency_install_confirmed: bool
    no_network_access_confirmed: bool
    no_live_workspace_write_confirmed: bool
    no_live_code_edit_confirmed: bool
    no_patch_application_confirmed: bool
    no_apply_patch_confirmed: bool
    no_git_apply_confirmed: bool
    no_repair_patch_proposal_confirmed: bool
    no_repair_diff_generation_confirmed: bool
    no_code_hunk_generation_confirmed: bool
    no_automatic_repair_confirmed: bool
    no_repair_execution_confirmed: bool
    no_retry_loop_confirmed: bool
    no_multi_cycle_loop_confirmed: bool
    no_model_provider_invocation_confirmed: bool
    no_tool_execution_confirmed: bool
    no_external_agent_execution_confirmed: bool
    no_claude_code_invocation_confirmed: bool
    no_codex_cli_invocation_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_infinite_agent_loop_confirmed: bool
    no_provider_invocation_confirmed: bool
    no_direct_network_access_confirmed: bool
    no_credential_access_confirmed: bool
    no_secret_read_confirmed: bool
    no_general_agent_execution_confirmed: bool
    no_autonomous_agent_runtime_confirmed: bool
    no_general_tool_execution_confirmed: bool
    no_unquarantined_action_execution_confirmed: bool
    no_persistent_trace_write_confirmed: bool
    no_external_trace_sink_confirmed: bool
    no_ui_runtime_confirmed: bool
    no_external_control_confirmed: bool
    no_authority_grant_confirmed: bool
    no_d4_d9_grant_confirmed: bool
    no_production_certification_confirmed: bool
    unsafe_readiness_flags_false_confirmed: bool
    do_nothing_comparison_required_confirmed: bool
    human_handoff_required_confirmed: bool
    evidence_bounded_scorecard_confirmed: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _validate_version(self.version)
        for name in (
            "reviewed_artifact_refs",
            "reviewed_test_refs",
            "reviewed_doc_refs",
            "boundary_checks",
            "negative_runtime_checks",
            "controlled_test_checks",
            "agent_evaluation_checks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        confirmation_names = tuple(name for name in self.__dataclass_fields__ if name.endswith("_confirmed"))
        _validate_true(self, confirmation_names)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ControlledTestExecutionConsolidationRecord:
    controlled_test_record_id: str
    version: str
    controlled_test_execution_confirmed: bool
    controlled_subprocess_scoped_to_v0372_confirmed: bool
    structured_argv_confirmed: bool
    shell_false_confirmed: bool
    sandbox_cwd_confirmed: bool
    timeout_confirmed: bool
    bounded_output_confirmed: bool
    minimal_env_confirmed: bool
    arbitrary_shell_blocked: bool
    direct_subprocess_blocked: bool
    dependency_install_blocked: bool
    network_access_blocked: bool
    live_workspace_blocked: bool
    completed_capabilities: list[str]
    future_track_items: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("controlled_test_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        confirmation_names = tuple(
            name for name, value in self.__dict__.items() if isinstance(value, bool)
        )
        _validate_true(self, confirmation_names)
        for name in ("completed_capabilities", "future_track_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class VeraCodexTrialConsolidationRecord:
    vera_trial_record_id: str
    version: str
    one_shot_trial_confirmed: bool
    max_trial_count_one_confirmed: bool
    max_cycle_count_one_confirmed: bool
    human_handoff_required_confirmed: bool
    stop_reason_required_confirmed: bool
    do_nothing_assessment_required_confirmed: bool
    no_model_invocation_confirmed: bool
    no_tool_execution_confirmed: bool
    no_external_agent_confirmed: bool
    no_repair_execution_confirmed: bool
    no_chain_of_thought_output_confirmed: bool
    completed_capabilities: list[str]
    future_track_items: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("vera_trial_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, tuple(name for name, value in self.__dict__.items() if isinstance(value, bool)))
        for name in ("completed_capabilities", "future_track_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ColdEvaluationConsolidationRecord:
    cold_evaluation_record_id: str
    version: str
    cold_scorecard_confirmed: bool
    evidence_grounding_confirmed: bool
    do_nothing_comparison_confirmed: bool
    boundary_compliance_assessment_confirmed: bool
    failure_condition_assessment_confirmed: bool
    pass_requires_evidence_confirmed: bool
    inconclusive_allowed_confirmed: bool
    production_certification_blocked: bool
    runtime_execution_blocked: bool
    completed_capabilities: list[str]
    future_track_items: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("cold_evaluation_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, tuple(name for name, value in self.__dict__.items() if isinstance(value, bool)))
        for name in ("completed_capabilities", "future_track_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class CLITestRunnerSurfaceConsolidationRecord:
    cli_surface_record_id: str
    version: str
    cli_surface_confirmed: bool
    safe_command_set_confirmed: bool
    denied_command_set_confirmed: bool
    argv_not_shell_confirmed: bool
    direct_subprocess_blocked: bool
    raw_pytest_blocked: bool
    package_manager_blocked: bool
    install_blocked: bool
    network_blocked: bool
    repair_commands_blocked: bool
    model_provider_commands_blocked: bool
    external_agent_commands_blocked: bool
    dominion_commands_blocked: bool
    bounded_dispatch_confirmed: bool
    completed_capabilities: list[str]
    future_track_items: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("cli_surface_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, tuple(name for name, value in self.__dict__.items() if isinstance(value, bool)))
        for name in ("completed_capabilities", "future_track_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class DigestionDominionTestRunnerConsolidationRecord:
    digestion_consolidation_id: str
    version: str
    digestion_first_policy_confirmed: bool
    dominion_fallback_future_gated: bool
    external_agent_patterns_recorded: bool
    external_agent_execution_blocked: bool
    infinite_loop_blocked: bool
    recursive_self_invocation_blocked: bool
    automatic_repair_loop_blocked: bool
    dominion_runtime_blocked: bool
    safely_digested_items: list[str]
    rejected_dominion_like_items: list[str]
    future_track_dominion_items: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("digestion_consolidation_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(self, tuple(name for name, value in self.__dict__.items() if isinstance(value, bool)))
        for name in ("safely_digested_items", "rejected_dominion_like_items", "future_track_dominion_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V038HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    bounded_repair_proposal_items: list[str]
    repair_proposal_boundary_items: list[str]
    repair_evidence_contract_items: list[str]
    proposed_diff_metadata_items: list[str]
    code_hunk_proposal_metadata_items: list[str]
    no_apply_by_default_items: list[str]
    human_approval_before_apply_items: list[str]
    sandbox_only_proposal_validation_items: list[str]
    do_nothing_comparison_items: list[str]
    cold_evaluation_feedback_items: list[str]
    reusable_test_runner_items: list[str]
    reusable_result_envelope_items: list[str]
    reusable_feedback_items: list[str]
    reusable_repair_suggestion_items: list[str]
    reusable_vera_trial_items: list[str]
    reusable_cold_evaluation_items: list[str]
    reusable_cli_items: list[str]
    required_new_boundaries: list[str]
    prohibited_until_later_gate: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    readiness_level: SandboxTestRunnerConsolidationReadinessLevel | str
    ready_for_v038: bool
    ready_for_execution: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_execution: bool
    ready_for_patch_application: bool
    ready_for_live_workspace_write: bool
    ready_for_shell_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "source_version", "target_version_track", "source_snapshot_id", "recommended_next_track", "recommended_next_release"):
            _require_non_blank(name, getattr(self, name))
        if V0379_VERSION not in self.source_version:
            raise ValueError("source_version must include v0.37.9")
        if "v0.38" not in self.target_version_track:
            raise ValueError("target_version_track should refer to v0.38")
        if "Bounded Repair Proposal Loop" not in self.recommended_next_track:
            raise ValueError("recommended_next_track should mention Bounded Repair Proposal Loop")
        for name in (
            "bounded_repair_proposal_items",
            "repair_proposal_boundary_items",
            "repair_evidence_contract_items",
            "proposed_diff_metadata_items",
            "code_hunk_proposal_metadata_items",
            "no_apply_by_default_items",
            "human_approval_before_apply_items",
            "sandbox_only_proposal_validation_items",
            "do_nothing_comparison_items",
            "cold_evaluation_feedback_items",
            "reusable_test_runner_items",
            "reusable_result_envelope_items",
            "reusable_feedback_items",
            "reusable_repair_suggestion_items",
            "reusable_vera_trial_items",
            "reusable_cold_evaluation_items",
            "reusable_cli_items",
            "required_new_boundaries",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        SandboxTestRunnerConsolidationReadinessLevel(self.readiness_level)
        if not self.ready_for_v038:
            raise ValueError("ready_for_v038 should be True for design-stage handoff without blocking gaps")
        for name in (
            "ready_for_execution",
            "ready_for_repair_patch_proposal",
            "ready_for_repair_execution",
            "ready_for_patch_application",
            "ready_for_live_workspace_write",
            "ready_for_shell_execution",
            "ready_for_dependency_install",
            "ready_for_network_access",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.37.9 handoff")
        required_prohibited = [
            "live write",
            "live apply",
            "apply_patch",
            "git apply",
            "unrestricted shell",
            "dependency install",
            "direct provider",
            "direct network",
            "credential access",
            "external agent execution",
            "Dominion runtime",
            "infinite loop",
            "automatic repair",
            "multi-cycle loop",
            "UI runtime",
            "authority grant",
        ]
        if not _contains_all(self.prohibited_until_later_gate, required_prohibited):
            raise ValueError("prohibited_until_later_gate missing required unsafe gates")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V037ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: SandboxTestRunnerConsolidationStatus | str
    readiness_level: SandboxTestRunnerConsolidationReadinessLevel | str
    summary: str
    completed_items: list[str]
    enabled_test_runner_items: list[str]
    enabled_agent_evaluation_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    runtime_not_ready_items: list[str]
    v038_handoff_summary: str
    ready_for_v038: bool
    ready_for_controlled_sandbox_test_runner_v1: bool
    ready_for_controlled_test_command_policy: bool
    ready_for_controlled_sandbox_test_execution: bool
    ready_for_test_result_envelope: bool
    ready_for_test_feedback_report: bool
    ready_for_repair_suggestion_metadata: bool
    ready_for_vera_codex_one_shot_agent_trial: bool
    ready_for_cold_agent_performance_evaluation: bool
    ready_for_cli_test_runner_surface: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_shell_execution: bool
    ready_for_direct_subprocess: bool
    ready_for_uncontrolled_subprocess: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_automatic_repair: bool
    ready_for_repair_execution: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_model_provider_invocation: bool
    ready_for_tool_execution: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_provider_invocation: bool
    ready_for_direct_network_access: bool
    ready_for_credential_access: bool
    ready_for_secret_read: bool
    ready_for_general_agent_execution: bool
    ready_for_autonomous_agent_runtime: bool
    ready_for_general_tool_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_ui_runtime: bool
    ready_for_external_control: bool
    ready_for_authority_grant: bool
    production_certified: bool
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "release_name", "snapshot_id", "release_manifest_id", "summary", "v038_handoff_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if FOUNDATION_RELEASE_NAME not in self.release_name:
            raise ValueError("release_name should be foundation release name")
        SandboxTestRunnerConsolidationStatus(self.consolidation_status)
        SandboxTestRunnerConsolidationReadinessLevel(self.readiness_level)
        for name in (
            "completed_items",
            "enabled_test_runner_items",
            "enabled_agent_evaluation_items",
            "blocked_items",
            "future_track_items",
            "runtime_not_ready_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, tuple(name for name in REPORT_UNSAFE_READY_NAMES if hasattr(self, name)))
        _validate_metadata(self.metadata)


def build_sandbox_test_runner_release_flags(**kwargs: Any) -> SandboxTestRunnerReleaseFlagSet:
    return SandboxTestRunnerReleaseFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "sandbox_test_runner_release_flags:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        controlled_sandbox_test_runner_v1_ready=kwargs.pop("controlled_sandbox_test_runner_v1_ready", True),
        ready_for_v038_handoff=kwargs.pop("ready_for_v038_handoff", True),
        ready_for_test_runner_boundary=kwargs.pop("ready_for_test_runner_boundary", True),
        ready_for_controlled_test_command_policy=kwargs.pop("ready_for_controlled_test_command_policy", True),
        ready_for_test_invocation_contract=kwargs.pop("ready_for_test_invocation_contract", True),
        ready_for_controlled_sandbox_test_execution=kwargs.pop("ready_for_controlled_sandbox_test_execution", True),
        ready_for_controlled_test_subprocess_via_v0372=kwargs.pop("ready_for_controlled_test_subprocess_via_v0372", True),
        ready_for_bounded_test_output_capture=kwargs.pop("ready_for_bounded_test_output_capture", True),
        ready_for_test_result_envelope=kwargs.pop("ready_for_test_result_envelope", True),
        ready_for_test_output_classifier=kwargs.pop("ready_for_test_output_classifier", True),
        ready_for_test_feedback_report=kwargs.pop("ready_for_test_feedback_report", True),
        ready_for_failure_diagnosis_report=kwargs.pop("ready_for_failure_diagnosis_report", True),
        ready_for_repair_suggestion_metadata=kwargs.pop("ready_for_repair_suggestion_metadata", True),
        ready_for_repair_scope_metadata=kwargs.pop("ready_for_repair_scope_metadata", True),
        ready_for_future_repair_proposal_input=kwargs.pop("ready_for_future_repair_proposal_input", True),
        ready_for_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_vera_codex_one_shot_agent_trial", True),
        ready_for_vera_codex_evidence_bundle=kwargs.pop("ready_for_vera_codex_evidence_bundle", True),
        ready_for_vera_codex_decision_trace=kwargs.pop("ready_for_vera_codex_decision_trace", True),
        ready_for_cold_agent_performance_evaluation=kwargs.pop("ready_for_cold_agent_performance_evaluation", True),
        ready_for_cold_agent_scorecard=kwargs.pop("ready_for_cold_agent_scorecard", True),
        ready_for_do_nothing_comparison=kwargs.pop("ready_for_do_nothing_comparison", True),
        ready_for_cli_test_runner_surface=kwargs.pop("ready_for_cli_test_runner_surface", True),
        ready_for_cli_sandbox_test_run=kwargs.pop("ready_for_cli_sandbox_test_run", True),
        ready_for_cli_vera_trial_run_once=kwargs.pop("ready_for_cli_vera_trial_run_once", True),
        ready_for_cli_cold_scorecard=kwargs.pop("ready_for_cli_cold_scorecard", True),
        max_grantable_level=kwargs.pop("max_grantable_level", "D3_SIMULATE"),
        future_track_levels=kwargs.pop("future_track_levels", ["D4_SANDBOX_APPLY_GATE", "D5_CONTROLLED_WRITE", "D6_PROVIDER", "D7_EXTERNAL_AGENT", "D8_DOMINION", "D9_AUTHORITY"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_RELEASE_FLAG_NAMES},
    )


def build_sandbox_test_runner_evaluation_snapshot(**kwargs: Any) -> SandboxTestRunnerEvaluationSnapshot:
    flags = kwargs.pop("release_flags", build_sandbox_test_runner_release_flags())
    return SandboxTestRunnerEvaluationSnapshot(
        snapshot_id=kwargs.pop("snapshot_id", "sandbox_test_runner_snapshot:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        included_versions=kwargs.pop("included_versions", list(INCLUDED_V037_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(V037_MODULES)),
        included_artifact_groups=kwargs.pop("included_artifact_groups", ["test runner", "result envelope", "feedback", "repair suggestion metadata", "Vera-Codex trial", "cold scorecard", "CLI surface"]),
        release_flags=flags,
        consolidation_status=kwargs.pop("consolidation_status", SandboxTestRunnerConsolidationStatus.CONSOLIDATED),
        readiness_level=kwargs.pop("readiness_level", SandboxTestRunnerConsolidationReadinessLevel.HANDOFF_READY_FOR_V038),
        summary=kwargs.pop("summary", "v0.37.x consolidated as bounded Controlled Sandbox Test Runner & Vera-Codex Agent Evaluation v1"),
        enabled_test_runner_capabilities=kwargs.pop("enabled_test_runner_capabilities", list(ENABLED_TEST_RUNNER_CAPABILITIES)),
        enabled_agent_evaluation_capabilities=kwargs.pop("enabled_agent_evaluation_capabilities", list(ENABLED_AGENT_EVALUATION_CAPABILITIES)),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(PROHIBITED_CAPABILITIES)),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_TESTS)),
        known_gaps=kwargs.pop("known_gaps", ["repair proposal generation remains v0.38 future track"]),
        known_risks=kwargs.pop("known_risks", ["controlled subprocess may be confused with general shell if boundary text is ignored"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(WITHDRAWAL_CONDITIONS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_capability_matrix(**kwargs: Any) -> SandboxTestRunnerCapabilityMatrix:
    prohibited = kwargs.pop("prohibited_capabilities", list(PROHIBITED_CAPABILITIES))
    return SandboxTestRunnerCapabilityMatrix(
        capability_matrix_id=kwargs.pop("capability_matrix_id", "sandbox_test_runner_capability_matrix:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        enabled_test_runner_capabilities=kwargs.pop("enabled_test_runner_capabilities", list(ENABLED_TEST_RUNNER_CAPABILITIES)),
        enabled_agent_evaluation_capabilities=kwargs.pop("enabled_agent_evaluation_capabilities", list(ENABLED_AGENT_EVALUATION_CAPABILITIES)),
        design_stage_capabilities=kwargs.pop("design_stage_capabilities", ["v0.38 Bounded Repair Proposal Loop handoff"]),
        prohibited_capabilities=prohibited,
        future_track_capabilities=kwargs.pop("future_track_capabilities", list(FUTURE_TRACK_ITEMS)),
        capability_to_version=kwargs.pop("capability_to_version", {
            "controlled sandbox test runner boundary": "v0.37.0",
            "allowlisted test command policy": "v0.37.1",
            "controlled sandbox test execution": "v0.37.2",
            "test result envelope": "v0.37.3",
            "test feedback report": "v0.37.4",
            "repair suggestion metadata": "v0.37.5",
            "Vera-Codex one-shot trial": "v0.37.6",
            "cold agent scorecard": "v0.37.7",
            "CLI surface": "v0.37.8",
        }),
        prohibited_capability_to_reason=kwargs.pop("prohibited_capability_to_reason", {capability: "not opened by v0.37.x consolidation" for capability in prohibited}),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_DOCS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_stage_coverage(**kwargs: Any) -> SandboxTestRunnerStageCoverage:
    return SandboxTestRunnerStageCoverage(
        coverage_id=kwargs.pop("coverage_id", "sandbox_test_runner_stage_coverage:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        stage_version=kwargs.pop("stage_version", "v0.37.x"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", list(V037_MODULES)),
        missing_artifact_refs=kwargs.pop("missing_artifact_refs", []),
        covered_test_refs=kwargs.pop("covered_test_refs", list(V037_TESTS)),
        missing_test_refs=kwargs.pop("missing_test_refs", []),
        covered_doc_refs=kwargs.pop("covered_doc_refs", list(V037_DOCS)),
        missing_doc_refs=kwargs.pop("missing_doc_refs", []),
        coverage_notes=kwargs.pop("coverage_notes", ["consolidation coverage metadata only"]),
        coverage_complete=kwargs.pop("coverage_complete", True),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", ["repair proposal generation remains v0.38 handoff"]),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_TESTS)),
        metadata=kwargs.pop("metadata", {}),
    )


def _build_specific_coverage(cls: type[SandboxTestRunnerStageCoverage], stage_version: str, module_ref: str, test_ref: str, doc_ref: str, **kwargs: Any) -> SandboxTestRunnerStageCoverage:
    return cls(
        coverage_id=kwargs.pop("coverage_id", f"{cls.__name__}:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        stage_version=kwargs.pop("stage_version", stage_version),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", [module_ref]),
        missing_artifact_refs=kwargs.pop("missing_artifact_refs", []),
        covered_test_refs=kwargs.pop("covered_test_refs", [test_ref]),
        missing_test_refs=kwargs.pop("missing_test_refs", []),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [doc_ref]),
        missing_doc_refs=kwargs.pop("missing_doc_refs", []),
        coverage_notes=kwargs.pop("coverage_notes", ["stage covered by source, docs, and tests"]),
        coverage_complete=kwargs.pop("coverage_complete", True),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", []),
        evidence_refs=kwargs.pop("evidence_refs", [test_ref, doc_ref]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_boundary_coverage(**kwargs: Any) -> SandboxTestBoundaryCoverage:
    return _build_specific_coverage(SandboxTestBoundaryCoverage, "v0.37.0", "sandbox_test_boundary", V037_TESTS[0], V037_DOCS[0], **kwargs)


def build_sandbox_test_command_policy_coverage(**kwargs: Any) -> SandboxTestCommandPolicyCoverage:
    return _build_specific_coverage(SandboxTestCommandPolicyCoverage, "v0.37.1", "sandbox_test_command_policy", V037_TESTS[1], V037_DOCS[1], **kwargs)


def build_sandbox_test_execution_engine_coverage(**kwargs: Any) -> SandboxTestExecutionEngineCoverage:
    return _build_specific_coverage(SandboxTestExecutionEngineCoverage, "v0.37.2", "sandbox_test_execution", V037_TESTS[2], V037_DOCS[2], **kwargs)


def build_sandbox_test_result_envelope_coverage(**kwargs: Any) -> SandboxTestResultEnvelopeCoverage:
    return _build_specific_coverage(SandboxTestResultEnvelopeCoverage, "v0.37.3", "sandbox_test_result", V037_TESTS[3], V037_DOCS[3], **kwargs)


def build_sandbox_test_feedback_coverage(**kwargs: Any) -> SandboxTestFeedbackCoverage:
    return _build_specific_coverage(SandboxTestFeedbackCoverage, "v0.37.4", "sandbox_test_feedback", V037_TESTS[4], V037_DOCS[4], **kwargs)


def build_sandbox_repair_suggestion_coverage(**kwargs: Any) -> SandboxRepairSuggestionCoverage:
    return _build_specific_coverage(SandboxRepairSuggestionCoverage, "v0.37.5", "sandbox_repair_suggestion", V037_TESTS[5], V037_DOCS[5], **kwargs)


def build_vera_codex_trial_coverage(**kwargs: Any) -> VeraCodexTrialCoverage:
    return _build_specific_coverage(VeraCodexTrialCoverage, "v0.37.6", "vera_codex_trial", V037_TESTS[6], V037_DOCS[6], **kwargs)


def build_cold_agent_evaluation_coverage(**kwargs: Any) -> ColdAgentEvaluationCoverage:
    return _build_specific_coverage(ColdAgentEvaluationCoverage, "v0.37.7", "agent_performance_evaluation", V037_TESTS[7], V037_DOCS[7], **kwargs)


def build_cli_test_runner_surface_coverage(**kwargs: Any) -> CLITestRunnerSurfaceCoverage:
    return _build_specific_coverage(CLITestRunnerSurfaceCoverage, "v0.37.8", "sandbox_test_cli_surface", V037_TESTS[8], V037_DOCS[8], **kwargs)


def build_sandbox_test_runner_boundary_register(**kwargs: Any) -> SandboxTestRunnerBoundaryRegister:
    return SandboxTestRunnerBoundaryRegister(
        boundary_register_id=kwargs.pop("boundary_register_id", "sandbox_test_runner_boundary_register:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        inherited_boundaries=kwargs.pop("inherited_boundaries", ["v0.30-v0.36 gate inheritance", "v0.36.9 human-approved patch apply sandbox remains separate"]),
        active_controlled_boundaries=kwargs.pop("active_controlled_boundaries", ["allowlisted command policy", "validated sandbox cwd", "controlled subprocess via v0.37.2 helper only", "bounded output", "minimal env"]),
        active_agent_evaluation_boundaries=kwargs.pop("active_agent_evaluation_boundaries", ["one-shot trial", "mandatory human handoff", "cold scorecard evidence requirement", "do-nothing comparison"]),
        prohibited_boundaries=kwargs.pop("prohibited_boundaries", list(PROHIBITED_BOUNDARIES)),
        future_gate_boundaries=kwargs.pop("future_gate_boundaries", list(RECOMMENDED_V038_ITEMS + FUTURE_TRACK_ITEMS)),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_DOCS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_risk_register(**kwargs: Any) -> SandboxTestRunnerRiskRegister:
    return SandboxTestRunnerRiskRegister(
        risk_register_id=kwargs.pop("risk_register_id", "sandbox_test_runner_risk_register:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        known_risks=kwargs.pop("known_risks", ["controlled subprocess may be overread as general execution", "repair suggestion metadata may be overread as repair permission"]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", ["CLI surface", "controlled test execution boundary", "future repair proposal handoff"]),
        prohibited_runtime_surfaces=kwargs.pop("prohibited_runtime_surfaces", list(PROHIBITED_RUNTIME_SURFACES)),
        mitigations=kwargs.pop("mitigations", ["unsafe flags forced false", "v0.37.2 scoping recorded", "human handoff required", "do-nothing comparison required"]),
        unresolved_risks=kwargs.pop("unresolved_risks", ["v0.38 repair proposal boundaries not implemented yet"]),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_TESTS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_gap_register(**kwargs: Any) -> SandboxTestRunnerGapRegister:
    return SandboxTestRunnerGapRegister(
        gap_register_id=kwargs.pop("gap_register_id", "sandbox_test_runner_gap_register:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", ["production certification intentionally absent", "repair proposal generation intentionally absent"]),
        future_track_items=kwargs.pop("future_track_items", list(FUTURE_TRACK_ITEMS)),
        recommended_v038_items=kwargs.pop("recommended_v038_items", list(RECOMMENDED_V038_ITEMS)),
        recommended_later_items=kwargs.pop("recommended_later_items", ["sandbox repair apply gate", "persistent trace store", "UI runtime", "external harness adapter", "Dominion runtime gated review"]),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_DOCS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_release_manifest(**kwargs: Any) -> SandboxTestRunnerReleaseManifest:
    flags = kwargs.pop("release_flags", build_sandbox_test_runner_release_flags())
    return SandboxTestRunnerReleaseManifest(
        release_manifest_id=kwargs.pop("release_manifest_id", "sandbox_test_runner_release_manifest:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        snapshot_id=kwargs.pop("snapshot_id", "sandbox_test_runner_snapshot:v0.37.9"),
        included_versions=kwargs.pop("included_versions", list(INCLUDED_V037_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(V037_MODULES)),
        included_docs=kwargs.pop("included_docs", list(V037_DOCS)),
        included_tests=kwargs.pop("included_tests", list(V037_TESTS)),
        focused_test_command=kwargs.pop("focused_test_command", "py -m pytest tests/test_v0379_controlled_sandbox_test_runner_consolidation.py"),
        full_track_test_command=kwargs.pop("full_track_test_command", "py -m pytest tests/test_v0370_sandbox_test_runner_boundary.py ... tests/test_v0379_controlled_sandbox_test_runner_consolidation.py"),
        release_flags=flags,
        known_gaps=kwargs.pop("known_gaps", ["repair proposal generation deferred to v0.38"]),
        known_risks=kwargs.pop("known_risks", ["bounded test execution is not arbitrary shell"]),
        next_handoff_id=kwargs.pop("next_handoff_id", "v038_handoff_packet:v0.37.9"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_sandbox_test_runner_audit_trail(**kwargs: Any) -> SandboxTestRunnerAuditTrail:
    confirmation_defaults = {
        name: kwargs.pop(name, True)
        for name in SandboxTestRunnerAuditTrail.__dataclass_fields__
        if name.endswith("_confirmed")
    }
    return SandboxTestRunnerAuditTrail(
        audit_trail_id=kwargs.pop("audit_trail_id", "sandbox_test_runner_audit_trail:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        reviewed_artifact_refs=kwargs.pop("reviewed_artifact_refs", list(V037_MODULES)),
        reviewed_test_refs=kwargs.pop("reviewed_test_refs", list(V037_TESTS)),
        reviewed_doc_refs=kwargs.pop("reviewed_doc_refs", list(V037_DOCS)),
        boundary_checks=kwargs.pop("boundary_checks", ["v0.37.2 controlled helper boundary", "no shell", "no repair proposal", "no provider"]),
        negative_runtime_checks=kwargs.pop("negative_runtime_checks", list(PROHIBITED_CAPABILITIES)),
        controlled_test_checks=kwargs.pop("controlled_test_checks", ["structured argv", "shell false", "sandbox cwd", "timeout", "bounded output", "minimal env"]),
        agent_evaluation_checks=kwargs.pop("agent_evaluation_checks", ["one-shot", "human handoff", "do-nothing comparison", "evidence-bounded scorecard"]),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_TESTS)),
        metadata=kwargs.pop("metadata", {}),
        **confirmation_defaults,
    )


def build_controlled_test_execution_consolidation_record(**kwargs: Any) -> ControlledTestExecutionConsolidationRecord:
    return ControlledTestExecutionConsolidationRecord(
        controlled_test_record_id=kwargs.pop("controlled_test_record_id", "controlled_test_execution_consolidation_record:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        controlled_test_execution_confirmed=kwargs.pop("controlled_test_execution_confirmed", True),
        controlled_subprocess_scoped_to_v0372_confirmed=kwargs.pop("controlled_subprocess_scoped_to_v0372_confirmed", True),
        structured_argv_confirmed=kwargs.pop("structured_argv_confirmed", True),
        shell_false_confirmed=kwargs.pop("shell_false_confirmed", True),
        sandbox_cwd_confirmed=kwargs.pop("sandbox_cwd_confirmed", True),
        timeout_confirmed=kwargs.pop("timeout_confirmed", True),
        bounded_output_confirmed=kwargs.pop("bounded_output_confirmed", True),
        minimal_env_confirmed=kwargs.pop("minimal_env_confirmed", True),
        arbitrary_shell_blocked=kwargs.pop("arbitrary_shell_blocked", True),
        direct_subprocess_blocked=kwargs.pop("direct_subprocess_blocked", True),
        dependency_install_blocked=kwargs.pop("dependency_install_blocked", True),
        network_access_blocked=kwargs.pop("network_access_blocked", True),
        live_workspace_blocked=kwargs.pop("live_workspace_blocked", True),
        completed_capabilities=kwargs.pop("completed_capabilities", ["controlled sandbox test execution", "structured argv", "bounded output capture"]),
        future_track_items=kwargs.pop("future_track_items", ["sandbox-only repair proposal validation"]),
        summary=kwargs.pop("summary", "controlled test execution is consolidated as v0.37.2-scoped helper readiness only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_vera_codex_trial_consolidation_record(**kwargs: Any) -> VeraCodexTrialConsolidationRecord:
    return VeraCodexTrialConsolidationRecord(
        vera_trial_record_id=kwargs.pop("vera_trial_record_id", "vera_codex_trial_consolidation_record:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        one_shot_trial_confirmed=kwargs.pop("one_shot_trial_confirmed", True),
        max_trial_count_one_confirmed=kwargs.pop("max_trial_count_one_confirmed", True),
        max_cycle_count_one_confirmed=kwargs.pop("max_cycle_count_one_confirmed", True),
        human_handoff_required_confirmed=kwargs.pop("human_handoff_required_confirmed", True),
        stop_reason_required_confirmed=kwargs.pop("stop_reason_required_confirmed", True),
        do_nothing_assessment_required_confirmed=kwargs.pop("do_nothing_assessment_required_confirmed", True),
        no_model_invocation_confirmed=kwargs.pop("no_model_invocation_confirmed", True),
        no_tool_execution_confirmed=kwargs.pop("no_tool_execution_confirmed", True),
        no_external_agent_confirmed=kwargs.pop("no_external_agent_confirmed", True),
        no_repair_execution_confirmed=kwargs.pop("no_repair_execution_confirmed", True),
        no_chain_of_thought_output_confirmed=kwargs.pop("no_chain_of_thought_output_confirmed", True),
        completed_capabilities=kwargs.pop("completed_capabilities", ["Vera-Codex one-shot trial", "evidence bundle", "mandatory handoff"]),
        future_track_items=kwargs.pop("future_track_items", ["bounded repair proposal feedback integration"]),
        summary=kwargs.pop("summary", "Vera-Codex trial remains one-shot evaluation metadata only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_cold_evaluation_consolidation_record(**kwargs: Any) -> ColdEvaluationConsolidationRecord:
    return ColdEvaluationConsolidationRecord(
        cold_evaluation_record_id=kwargs.pop("cold_evaluation_record_id", "cold_evaluation_consolidation_record:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        cold_scorecard_confirmed=kwargs.pop("cold_scorecard_confirmed", True),
        evidence_grounding_confirmed=kwargs.pop("evidence_grounding_confirmed", True),
        do_nothing_comparison_confirmed=kwargs.pop("do_nothing_comparison_confirmed", True),
        boundary_compliance_assessment_confirmed=kwargs.pop("boundary_compliance_assessment_confirmed", True),
        failure_condition_assessment_confirmed=kwargs.pop("failure_condition_assessment_confirmed", True),
        pass_requires_evidence_confirmed=kwargs.pop("pass_requires_evidence_confirmed", True),
        inconclusive_allowed_confirmed=kwargs.pop("inconclusive_allowed_confirmed", True),
        production_certification_blocked=kwargs.pop("production_certification_blocked", True),
        runtime_execution_blocked=kwargs.pop("runtime_execution_blocked", True),
        completed_capabilities=kwargs.pop("completed_capabilities", ["cold scorecard", "evidence grounding", "do-nothing comparison", "failure condition assessment"]),
        future_track_items=kwargs.pop("future_track_items", ["repair proposal scorecard feedback"]),
        summary=kwargs.pop("summary", "cold evaluation remains human decision support, not production certification"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_cli_test_runner_surface_consolidation_record(**kwargs: Any) -> CLITestRunnerSurfaceConsolidationRecord:
    return CLITestRunnerSurfaceConsolidationRecord(
        cli_surface_record_id=kwargs.pop("cli_surface_record_id", "cli_test_runner_surface_consolidation_record:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        cli_surface_confirmed=kwargs.pop("cli_surface_confirmed", True),
        safe_command_set_confirmed=kwargs.pop("safe_command_set_confirmed", True),
        denied_command_set_confirmed=kwargs.pop("denied_command_set_confirmed", True),
        argv_not_shell_confirmed=kwargs.pop("argv_not_shell_confirmed", True),
        direct_subprocess_blocked=kwargs.pop("direct_subprocess_blocked", True),
        raw_pytest_blocked=kwargs.pop("raw_pytest_blocked", True),
        package_manager_blocked=kwargs.pop("package_manager_blocked", True),
        install_blocked=kwargs.pop("install_blocked", True),
        network_blocked=kwargs.pop("network_blocked", True),
        repair_commands_blocked=kwargs.pop("repair_commands_blocked", True),
        model_provider_commands_blocked=kwargs.pop("model_provider_commands_blocked", True),
        external_agent_commands_blocked=kwargs.pop("external_agent_commands_blocked", True),
        dominion_commands_blocked=kwargs.pop("dominion_commands_blocked", True),
        bounded_dispatch_confirmed=kwargs.pop("bounded_dispatch_confirmed", True),
        completed_capabilities=kwargs.pop("completed_capabilities", ["CLI safe commands", "denied unsafe commands", "bounded helper dispatch metadata"]),
        future_track_items=kwargs.pop("future_track_items", ["repair proposal CLI preview only in v0.38"]),
        summary=kwargs.pop("summary", "CLI surface remains bounded handler surface, not shell"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_digestion_dominion_test_runner_consolidation_record(**kwargs: Any) -> DigestionDominionTestRunnerConsolidationRecord:
    return DigestionDominionTestRunnerConsolidationRecord(
        digestion_consolidation_id=kwargs.pop("digestion_consolidation_id", "digestion_dominion_test_runner_consolidation_record:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        digestion_first_policy_confirmed=kwargs.pop("digestion_first_policy_confirmed", True),
        dominion_fallback_future_gated=kwargs.pop("dominion_fallback_future_gated", True),
        external_agent_patterns_recorded=kwargs.pop("external_agent_patterns_recorded", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_loop_blocked=kwargs.pop("infinite_loop_blocked", True),
        recursive_self_invocation_blocked=kwargs.pop("recursive_self_invocation_blocked", True),
        automatic_repair_loop_blocked=kwargs.pop("automatic_repair_loop_blocked", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        safely_digested_items=kwargs.pop("safely_digested_items", ["static reference patterns", "bounded test runner patterns", "blocked external-agent-control patterns"]),
        rejected_dominion_like_items=kwargs.pop("rejected_dominion_like_items", ["recursive self invocation", "external agent loop", "Dominion runtime", "automatic repair loop"]),
        future_track_dominion_items=kwargs.pop("future_track_dominion_items", ["Dominion runtime gated review"]),
        summary=kwargs.pop("summary", "Digestion-first confirmed; Dominion remains blocked/future-gated metadata only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v038_handoff_packet(**kwargs: Any) -> V038HandoffPacket:
    return V038HandoffPacket(
        handoff_id=kwargs.pop("handoff_id", "v038_handoff_packet:v0.37.9"),
        source_version=kwargs.pop("source_version", V0379_VERSION),
        target_version_track=kwargs.pop("target_version_track", "v0.38"),
        source_snapshot_id=kwargs.pop("source_snapshot_id", "sandbox_test_runner_snapshot:v0.37.9"),
        release_manifest_id=kwargs.pop("release_manifest_id", "sandbox_test_runner_release_manifest:v0.37.9"),
        recommended_next_track=kwargs.pop("recommended_next_track", "Bounded Repair Proposal Loop"),
        recommended_next_release=kwargs.pop("recommended_next_release", "v0.38.0 Bounded Repair Proposal Boundary Foundation"),
        bounded_repair_proposal_items=kwargs.pop("bounded_repair_proposal_items", ["bounded repair proposal loop", "proposal metadata only"]),
        repair_proposal_boundary_items=kwargs.pop("repair_proposal_boundary_items", ["bounded repair proposal boundary"]),
        repair_evidence_contract_items=kwargs.pop("repair_evidence_contract_items", ["repair proposal evidence contract"]),
        proposed_diff_metadata_items=kwargs.pop("proposed_diff_metadata_items", ["proposed diff metadata"]),
        code_hunk_proposal_metadata_items=kwargs.pop("code_hunk_proposal_metadata_items", ["code hunk proposal metadata"]),
        no_apply_by_default_items=kwargs.pop("no_apply_by_default_items", ["no apply by default"]),
        human_approval_before_apply_items=kwargs.pop("human_approval_before_apply_items", ["human approval before apply"]),
        sandbox_only_proposal_validation_items=kwargs.pop("sandbox_only_proposal_validation_items", ["sandbox-only proposal validation"]),
        do_nothing_comparison_items=kwargs.pop("do_nothing_comparison_items", ["do-nothing comparison"]),
        cold_evaluation_feedback_items=kwargs.pop("cold_evaluation_feedback_items", ["cold evaluation feedback integration"]),
        reusable_test_runner_items=kwargs.pop("reusable_test_runner_items", ["allowlisted command policy", "controlled v0.37.2 sandbox test execution boundary"]),
        reusable_result_envelope_items=kwargs.pop("reusable_result_envelope_items", ["test result envelope", "output classifier"]),
        reusable_feedback_items=kwargs.pop("reusable_feedback_items", ["feedback report", "failure diagnosis metadata"]),
        reusable_repair_suggestion_items=kwargs.pop("reusable_repair_suggestion_items", ["repair suggestion metadata", "human review requirement"]),
        reusable_vera_trial_items=kwargs.pop("reusable_vera_trial_items", ["Vera-Codex one-shot trial packet", "human handoff"]),
        reusable_cold_evaluation_items=kwargs.pop("reusable_cold_evaluation_items", ["cold scorecard", "do-nothing comparison", "boundary compliance assessment"]),
        reusable_cli_items=kwargs.pop("reusable_cli_items", ["CLI bounded surface", "unsafe command denial"]),
        required_new_boundaries=kwargs.pop("required_new_boundaries", list(RECOMMENDED_V038_ITEMS)),
        prohibited_until_later_gate=kwargs.pop("prohibited_until_later_gate", [
            "live write",
            "live apply",
            "apply_patch",
            "git apply",
            "unrestricted shell",
            "dependency install",
            "direct provider",
            "direct network",
            "credential access",
            "external agent execution",
            "Dominion runtime",
            "infinite loop",
            "automatic repair",
            "multi-cycle loop",
            "UI runtime",
            "authority grant",
        ]),
        future_track_items=kwargs.pop("future_track_items", list(FUTURE_TRACK_ITEMS)),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_DOCS)),
        readiness_level=kwargs.pop("readiness_level", SandboxTestRunnerConsolidationReadinessLevel.HANDOFF_READY_FOR_V038),
        ready_for_v038=kwargs.pop("ready_for_v038", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_repair_patch_proposal=kwargs.pop("ready_for_repair_patch_proposal", False),
        ready_for_repair_execution=kwargs.pop("ready_for_repair_execution", False),
        ready_for_patch_application=kwargs.pop("ready_for_patch_application", False),
        ready_for_live_workspace_write=kwargs.pop("ready_for_live_workspace_write", False),
        ready_for_shell_execution=kwargs.pop("ready_for_shell_execution", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        ready_for_network_access=kwargs.pop("ready_for_network_access", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v037_consolidation_report(**kwargs: Any) -> V037ConsolidationReport:
    unsafe_names = {
        name: kwargs.pop(name, False)
        for name in V037ConsolidationReport.__dataclass_fields__
        if name.startswith("ready_for_")
        and name
        not in {
            "ready_for_v038",
            "ready_for_controlled_sandbox_test_runner_v1",
            "ready_for_controlled_test_command_policy",
            "ready_for_controlled_sandbox_test_execution",
            "ready_for_test_result_envelope",
            "ready_for_test_feedback_report",
            "ready_for_repair_suggestion_metadata",
            "ready_for_vera_codex_one_shot_agent_trial",
            "ready_for_cold_agent_performance_evaluation",
            "ready_for_cli_test_runner_surface",
        }
    }
    unsafe_names["production_certified"] = kwargs.pop("production_certified", False)
    return V037ConsolidationReport(
        report_id=kwargs.pop("report_id", "v037_consolidation_report:v0.37.9"),
        version=kwargs.pop("version", V0379_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        snapshot_id=kwargs.pop("snapshot_id", "sandbox_test_runner_snapshot:v0.37.9"),
        release_manifest_id=kwargs.pop("release_manifest_id", "sandbox_test_runner_release_manifest:v0.37.9"),
        handoff_id=kwargs.pop("handoff_id", "v038_handoff_packet:v0.37.9"),
        consolidation_status=kwargs.pop("consolidation_status", SandboxTestRunnerConsolidationStatus.CONSOLIDATED),
        readiness_level=kwargs.pop("readiness_level", SandboxTestRunnerConsolidationReadinessLevel.HANDOFF_READY_FOR_V038),
        summary=kwargs.pop("summary", "v0.37.x consolidated as bounded Controlled Sandbox Test Runner & Vera-Codex Agent Evaluation v1"),
        completed_items=kwargs.pop("completed_items", list(ENABLED_TEST_RUNNER_CAPABILITIES + ENABLED_AGENT_EVALUATION_CAPABILITIES)),
        enabled_test_runner_items=kwargs.pop("enabled_test_runner_items", list(ENABLED_TEST_RUNNER_CAPABILITIES)),
        enabled_agent_evaluation_items=kwargs.pop("enabled_agent_evaluation_items", list(ENABLED_AGENT_EVALUATION_CAPABILITIES)),
        blocked_items=kwargs.pop("blocked_items", list(PROHIBITED_CAPABILITIES)),
        future_track_items=kwargs.pop("future_track_items", list(FUTURE_TRACK_ITEMS)),
        runtime_not_ready_items=kwargs.pop("runtime_not_ready_items", list(PROHIBITED_CAPABILITIES)),
        v038_handoff_summary=kwargs.pop("v038_handoff_summary", "v0.38 handoff is Bounded Repair Proposal Loop, design-stage only"),
        ready_for_v038=kwargs.pop("ready_for_v038", True),
        ready_for_controlled_sandbox_test_runner_v1=kwargs.pop("ready_for_controlled_sandbox_test_runner_v1", True),
        ready_for_controlled_test_command_policy=kwargs.pop("ready_for_controlled_test_command_policy", True),
        ready_for_controlled_sandbox_test_execution=kwargs.pop("ready_for_controlled_sandbox_test_execution", True),
        ready_for_test_result_envelope=kwargs.pop("ready_for_test_result_envelope", True),
        ready_for_test_feedback_report=kwargs.pop("ready_for_test_feedback_report", True),
        ready_for_repair_suggestion_metadata=kwargs.pop("ready_for_repair_suggestion_metadata", True),
        ready_for_vera_codex_one_shot_agent_trial=kwargs.pop("ready_for_vera_codex_one_shot_agent_trial", True),
        ready_for_cold_agent_performance_evaluation=kwargs.pop("ready_for_cold_agent_performance_evaluation", True),
        ready_for_cli_test_runner_surface=kwargs.pop("ready_for_cli_test_runner_surface", True),
        evidence_refs=kwargs.pop("evidence_refs", list(V037_TESTS)),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(WITHDRAWAL_CONDITIONS)),
        metadata=kwargs.pop("metadata", {}),
        **unsafe_names,
    )


def sandbox_test_runner_flags_preserve_no_unsafe_runtime(flags: SandboxTestRunnerReleaseFlagSet) -> bool:
    return isinstance(flags, SandboxTestRunnerReleaseFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_RELEASE_FLAG_NAMES)


def sandbox_test_runner_snapshot_is_not_production_runtime(snapshot: SandboxTestRunnerEvaluationSnapshot) -> bool:
    return isinstance(snapshot, SandboxTestRunnerEvaluationSnapshot) and sandbox_test_runner_flags_preserve_no_unsafe_runtime(snapshot.release_flags)


def sandbox_test_runner_capability_matrix_is_not_permission_grant(matrix: SandboxTestRunnerCapabilityMatrix) -> bool:
    return isinstance(matrix, SandboxTestRunnerCapabilityMatrix) and _contains_all(matrix.prohibited_capabilities, PROHIBITED_CAPABILITIES)


def sandbox_test_runner_audit_confirms_no_unsafe_runtime(audit: SandboxTestRunnerAuditTrail) -> bool:
    if not isinstance(audit, SandboxTestRunnerAuditTrail):
        return False
    confirmation_names = tuple(name for name in audit.__dataclass_fields__ if name.endswith("_confirmed"))
    return all(getattr(audit, name) is True for name in confirmation_names)


def controlled_test_execution_consolidation_record_is_scoped(record: ControlledTestExecutionConsolidationRecord) -> bool:
    return (
        isinstance(record, ControlledTestExecutionConsolidationRecord)
        and record.controlled_test_execution_confirmed
        and record.controlled_subprocess_scoped_to_v0372_confirmed
        and record.shell_false_confirmed
        and record.direct_subprocess_blocked
        and record.dependency_install_blocked
        and record.network_access_blocked
    )


def vera_codex_trial_consolidation_record_is_not_autonomous_runtime(record: VeraCodexTrialConsolidationRecord) -> bool:
    return (
        isinstance(record, VeraCodexTrialConsolidationRecord)
        and record.one_shot_trial_confirmed
        and record.max_trial_count_one_confirmed
        and record.max_cycle_count_one_confirmed
        and record.human_handoff_required_confirmed
        and record.no_model_invocation_confirmed
        and record.no_external_agent_confirmed
    )


def cold_evaluation_consolidation_record_is_not_production_certification(record: ColdEvaluationConsolidationRecord) -> bool:
    return (
        isinstance(record, ColdEvaluationConsolidationRecord)
        and record.cold_scorecard_confirmed
        and record.pass_requires_evidence_confirmed
        and record.do_nothing_comparison_confirmed
        and record.production_certification_blocked
        and record.runtime_execution_blocked
    )


def cli_test_runner_surface_consolidation_record_is_not_shell(record: CLITestRunnerSurfaceConsolidationRecord) -> bool:
    return (
        isinstance(record, CLITestRunnerSurfaceConsolidationRecord)
        and record.cli_surface_confirmed
        and record.argv_not_shell_confirmed
        and record.direct_subprocess_blocked
        and record.raw_pytest_blocked
        and record.external_agent_commands_blocked
        and record.dominion_commands_blocked
    )


def digestion_dominion_test_runner_record_is_not_runtime(record: DigestionDominionTestRunnerConsolidationRecord) -> bool:
    return (
        isinstance(record, DigestionDominionTestRunnerConsolidationRecord)
        and record.digestion_first_policy_confirmed
        and record.dominion_fallback_future_gated
        and record.external_agent_execution_blocked
        and record.infinite_loop_blocked
        and record.automatic_repair_loop_blocked
        and record.dominion_runtime_blocked
    )


def v038_handoff_packet_is_design_stage_only(packet: V038HandoffPacket) -> bool:
    return (
        isinstance(packet, V038HandoffPacket)
        and packet.ready_for_v038
        and not packet.ready_for_execution
        and not packet.ready_for_repair_patch_proposal
        and not packet.ready_for_repair_execution
        and not packet.ready_for_patch_application
        and not packet.ready_for_live_workspace_write
        and not packet.ready_for_shell_execution
        and not packet.ready_for_dependency_install
        and not packet.ready_for_network_access
    )


def v037_consolidation_report_is_not_runtime_ready(report: V037ConsolidationReport) -> bool:
    if not isinstance(report, V037ConsolidationReport):
        return False
    safe_names = {
        "ready_for_v038",
        "ready_for_controlled_sandbox_test_runner_v1",
        "ready_for_controlled_test_command_policy",
        "ready_for_controlled_sandbox_test_execution",
        "ready_for_test_result_envelope",
        "ready_for_test_feedback_report",
        "ready_for_repair_suggestion_metadata",
        "ready_for_vera_codex_one_shot_agent_trial",
        "ready_for_cold_agent_performance_evaluation",
        "ready_for_cli_test_runner_surface",
    }
    unsafe_names = tuple(name for name in report.__dataclass_fields__ if name.startswith("ready_for_") and name not in safe_names)
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
