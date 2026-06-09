from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0369_VERSION = "v0.36.9"
FOUNDATION_RELEASE_NAME = "Human-approved Patch Apply Sandbox v1"

INCLUDED_V036_VERSIONS = [
    "v0.36.0",
    "v0.36.1",
    "v0.36.2",
    "v0.36.3",
    "v0.36.4",
    "v0.36.5",
    "v0.36.6",
    "v0.36.7",
    "v0.36.8",
]

V036_MODULES = [
    "patch_apply_boundary",
    "patch_apply_candidate",
    "patch_apply_dry_run",
    "patch_apply_sandbox",
    "patch_apply_engine",
    "patch_apply_validation",
    "agentic_operation_cycle",
    "patch_apply_trace",
    "patch_apply_cli_surface",
]

V036_DOCS = [
    "docs/versions/v0.36/v0.36.0_human_approved_patch_apply_sandbox_boundary.md",
    "docs/versions/v0.36/v0.36.1_apply_candidate_human_approval_contract.md",
    "docs/versions/v0.36/v0.36.2_dry_run_patch_apply_simulation.md",
    "docs/versions/v0.36/v0.36.3_sandbox_workspace_overlay_policy.md",
    "docs/versions/v0.36/v0.36.4_sandbox_patch_apply_engine.md",
    "docs/versions/v0.36/v0.36.5_sandbox_post_apply_validation.md",
    "docs/versions/v0.36/v0.36.6_bounded_agentic_function_task_operation_cycle.md",
    "docs/versions/v0.36/v0.36.7_patch_apply_sandbox_ocel_trace_packet.md",
    "docs/versions/v0.36/v0.36.8_cli_sandbox_apply_agentic_task_surface.md",
]

V036_TESTS = [
    "tests/test_v0360_patch_apply_sandbox_boundary.py",
    "tests/test_v0361_apply_candidate_human_approval_contract.py",
    "tests/test_v0362_dry_run_patch_apply_simulation.py",
    "tests/test_v0363_sandbox_workspace_overlay_policy.py",
    "tests/test_v0364_sandbox_patch_apply_engine.py",
    "tests/test_v0365_sandbox_post_apply_validation.py",
    "tests/test_v0366_agentic_operation_cycle.py",
    "tests/test_v0367_patch_apply_sandbox_ocel_trace.py",
    "tests/test_v0368_cli_sandbox_apply_agentic_surface.py",
]

ENABLED_SANDBOX_CAPABILITIES = [
    "human-approved patch apply sandbox boundary",
    "apply candidate envelope",
    "human approval contract",
    "operator approval evidence validation",
    "model-generated approval rejection",
    "dry-run patch apply simulation",
    "dry-run apply",
    "hunk alignment and conflict detection",
    "in-memory simulated file deltas",
    "sandbox workspace overlay policy",
    "sandbox manifest and file-map metadata",
    "sandbox directory materialization under validated sandbox root",
    "sandbox file write under validated sandbox root",
    "sandbox-only patch apply engine",
    "sandbox patch apply",
    "sandbox write records",
    "sandbox post-apply static validation",
    "sandbox static validation",
    "expected-vs-actual sandbox reconciliation",
    "sandbox safety regression scan",
    "sandbox scope validation",
    "returned in-memory patch apply sandbox trace packet",
    "CLI sandbox apply surface",
    "CLI sandbox apply run through v0.36.4 helper boundaries",
]

ENABLED_BOUNDED_AGENTIC_CAPABILITIES = [
    "bounded agentic function/task operation cycle",
    "single-cycle run packet",
    "mandatory stop reason",
    "mandatory human handoff after cycle",
    "CLI agentic task run once through v0.36.6 helper boundaries",
    "Digestion-first and Dominion-fallback metadata",
    "external-agent-control pattern awareness as blocked metadata",
]

PROHIBITED_CAPABILITIES = [
    "live_workspace_write",
    "live_code_edit",
    "unrestricted_patch_application",
    "apply_patch",
    "git_apply",
    "test_execution",
    "shell_execution",
    "subprocess_execution",
    "command_execution",
    "dependency_install",
    "reference_execution",
    "reference_import",
    "external_agent_execution",
    "claude_code_invocation",
    "codex_cli_invocation",
    "dominion_runtime",
    "infinite_loop",
    "infinite_agent_loop",
    "automatic_repair",
    "multi_cycle_loop",
    "recursive_self_invocation",
    "provider_invocation",
    "direct_network_access",
    "credential_access",
    "secret_read",
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

RECOMMENDED_V037_ITEMS = [
    "controlled sandbox test runner boundary",
    "allowlisted test command policy",
    "timeout",
    "bounded output",
    "no network",
    "no dependency install by default",
    "test result envelope",
    "feedback report",
    "repair suggestion metadata only",
    "human checkpoint",
]

FUTURE_TRACK_ITEMS = [
    "controlled test runner",
    "bounded repair loop",
    "persistent trace store",
    "UI runtime",
    "external harness adapter",
    "Dominion runtime gated review",
]

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_test_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_reference_execution",
    "ready_for_reference_import",
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
    "ready_for_multi_cycle_agentic_loop",
    "ready_for_recursive_self_invocation",
    "ready_for_automatic_retry",
    "ready_for_automatic_repair",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ocel_file_write",
    "ready_for_jsonl_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

NO_AUDIT_CONFIRMATION_NAMES = (
    "no_live_workspace_write_confirmed",
    "no_live_code_edit_confirmed",
    "no_unrestricted_patch_application_confirmed",
    "no_apply_patch_confirmed",
    "no_git_apply_confirmed",
    "no_test_execution_confirmed",
    "no_shell_execution_confirmed",
    "no_subprocess_execution_confirmed",
    "no_command_execution_confirmed",
    "no_dependency_install_confirmed",
    "no_reference_execution_confirmed",
    "no_reference_import_confirmed",
    "no_external_agent_execution_confirmed",
    "no_claude_code_invocation_confirmed",
    "no_codex_cli_invocation_confirmed",
    "no_dominion_runtime_confirmed",
    "no_infinite_agent_loop_confirmed",
    "no_automatic_repair_confirmed",
    "no_multi_cycle_loop_confirmed",
    "no_provider_invocation_confirmed",
    "no_direct_network_access_confirmed",
    "no_credential_access_confirmed",
    "no_secret_read_confirmed",
    "no_general_agent_execution_confirmed",
    "no_autonomous_agent_runtime_confirmed",
    "no_general_tool_execution_confirmed",
    "no_unquarantined_action_execution_confirmed",
    "no_persistent_trace_write_confirmed",
    "no_external_trace_sink_confirmed",
    "no_ui_runtime_confirmed",
    "no_external_control_confirmed",
    "no_authority_grant_confirmed",
    "no_d4_d9_grant_confirmed",
)


class PatchApplySandboxConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class PatchApplySandboxConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    HUMAN_APPROVED_PATCH_APPLY_SANDBOX_READY = "human_approved_patch_apply_sandbox_ready"
    SANDBOX_APPLY_WORKFLOW_READY = "sandbox_apply_workflow_ready"
    BOUNDED_AGENTIC_TASK_READY = "bounded_agentic_task_ready"
    CLI_SANDBOX_APPLY_SURFACE_READY = "cli_sandbox_apply_surface_ready"
    HANDOFF_READY_FOR_V037 = "handoff_ready_for_v037"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.36.9")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True for v0.36.9 consolidation")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0369_VERSION not in version:
        raise ValueError("version must include v0.36.9")


def _validate_versions_include_v036_track(included_versions: list[str]) -> None:
    _validate_string_list("included_versions", included_versions)
    missing = [version for version in INCLUDED_V036_VERSIONS if version not in included_versions]
    if missing:
        raise ValueError(f"included_versions missing {', '.join(missing)}")


def _validate_metadata(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


def _contains_all(container: list[str], required: list[str]) -> bool:
    lowered = {item.lower() for item in container}
    return all(item.lower() in lowered for item in required)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxReleaseFlagSet:
    flag_set_id: str
    version: str
    human_approved_patch_apply_sandbox_v1_ready: bool
    ready_for_v037_handoff: bool
    ready_for_apply_sandbox_boundary: bool
    ready_for_apply_candidate_human_approval_contract: bool
    ready_for_human_approval_evidence_validation: bool
    ready_for_dry_run_apply_simulation: bool
    ready_for_dry_run_hunk_alignment: bool
    ready_for_sandbox_workspace_policy: bool
    ready_for_sandbox_workspace_manifest: bool
    ready_for_sandbox_workspace_materialization: bool
    ready_for_sandbox_workspace_write: bool
    ready_for_sandbox_patch_apply: bool
    ready_for_sandbox_patch_apply_result: bool
    ready_for_sandbox_post_apply_validation: bool
    ready_for_sandbox_reconciliation_report: bool
    ready_for_sandbox_safety_regression_scan: bool
    ready_for_sandbox_scope_validation: bool
    ready_for_bounded_agentic_task_operation_cycle: bool
    ready_for_agentic_function_task_execution: bool
    ready_for_single_cycle_operation_packet: bool
    ready_for_human_handoff_after_cycle: bool
    ready_for_patch_apply_sandbox_trace_packet_creation: bool
    ready_for_bounded_patch_apply_ocel_trace_emission: bool
    ready_for_cli_sandbox_apply_surface: bool
    ready_for_cli_sandbox_apply_run: bool
    ready_for_cli_agentic_task_run_once: bool
    ready_for_execution: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_test_execution: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_reference_execution: bool
    ready_for_reference_import: bool
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
    ready_for_multi_cycle_agentic_loop: bool
    ready_for_recursive_self_invocation: bool
    ready_for_automatic_retry: bool
    ready_for_automatic_repair: bool
    ready_for_general_tool_execution: bool
    ready_for_unquarantined_action_execution: bool
    ready_for_persistent_trace_write: bool
    ready_for_external_trace_sink: bool
    ready_for_ocel_file_write: bool
    ready_for_jsonl_trace_write: bool
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
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_string_list("future_track_levels", self.future_track_levels)
        if self.max_grantable_level is not None and self.max_grantable_level not in {"D0_NONE", "D1_READ", "D2_PLAN", "D3_SIMULATE"}:
            raise ValueError("max_grantable_level must be None or <= D3_SIMULATE")
        for level in ("D4", "D5", "D6", "D7", "D8", "D9"):
            if not any(item.startswith(level) for item in self.future_track_levels):
                raise ValueError("D4-D9 must remain future-track when represented")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_artifact_groups: list[str]
    release_flags: PatchApplySandboxReleaseFlagSet
    consolidation_status: PatchApplySandboxConsolidationStatus | str
    readiness_level: PatchApplySandboxConsolidationReadinessLevel | str
    summary: str
    enabled_sandbox_capabilities: list[str]
    enabled_bounded_agentic_capabilities: list[str]
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
            raise ValueError("release_name should be Human-approved Patch Apply Sandbox v1")
        _validate_versions_include_v036_track(self.included_versions)
        for name in (
            "included_modules",
            "included_artifact_groups",
            "enabled_sandbox_capabilities",
            "enabled_bounded_agentic_capabilities",
            "prohibited_capabilities",
            "evidence_refs",
            "known_gaps",
            "known_risks",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        if not patch_apply_sandbox_flags_preserve_no_live_apply(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        PatchApplySandboxConsolidationStatus(self.consolidation_status)
        PatchApplySandboxConsolidationReadinessLevel(self.readiness_level)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_sandbox_capabilities: list[str]
    enabled_bounded_capabilities: list[str]
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
            "enabled_sandbox_capabilities",
            "enabled_bounded_capabilities",
            "design_stage_capabilities",
            "prohibited_capabilities",
            "future_track_capabilities",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_dict("capability_to_version", self.capability_to_version)
        _validate_dict("prohibited_capability_to_reason", self.prohibited_capability_to_reason)
        required_enabled = ["apply candidate", "dry-run apply", "sandbox patch apply", "sandbox file write", "sandbox static validation"]
        if not all(any(required in item.lower() for item in self.enabled_sandbox_capabilities) for required in required_enabled):
            raise ValueError("enabled_sandbox_capabilities missing v0.36 bounded features")
        if not _contains_all(self.prohibited_capabilities, PROHIBITED_CAPABILITIES[:-1]):
            raise ValueError("prohibited_capabilities missing unsafe runtime capabilities")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxStageCoverage:
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
class PatchApplyBoundaryCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class ApplyCandidateCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class DryRunApplyCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxWorkspaceCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxPatchApplyCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class SandboxPostApplyValidationCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class BoundedAgenticOperationCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class PatchApplyTraceCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class CLISandboxApplySurfaceCoverage(PatchApplySandboxStageCoverage):
    pass


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str]
    active_sandbox_boundaries: list[str]
    active_bounded_agentic_boundaries: list[str]
    prohibited_boundaries: list[str]
    future_gate_boundaries: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version(self.version)
        for name in (
            "inherited_boundaries",
            "active_sandbox_boundaries",
            "active_bounded_agentic_boundaries",
            "prohibited_boundaries",
            "future_gate_boundaries",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not _contains_all(self.prohibited_boundaries, PROHIBITED_CAPABILITIES[:-1]):
            raise ValueError("prohibited_boundaries missing unsafe runtime surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxRiskRegister:
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
        required = [
            "live_workspace_write",
            "live_code_edit",
            "unrestricted_patch_application",
            "apply_patch",
            "git_apply",
            "test_execution",
            "shell_execution",
            "subprocess_execution",
            "command_execution",
            "dependency_install",
            "reference_execution",
            "reference_import",
            "external_agent_execution",
            "dominion_runtime",
            "infinite_loop",
            "automatic_repair",
            "multi_cycle_loop",
            "provider_invocation",
            "direct_network_access",
            "credential_access",
            "secret_read",
            "persistent_trace_write",
            "external_trace_sink",
            "UI_runtime",
            "external_control",
            "authority_grant",
            "D4_D9_grant",
        ]
        if not _contains_all(self.prohibited_runtime_surfaces, required):
            raise ValueError("prohibited_runtime_surfaces missing unsafe surfaces")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    future_track_items: list[str]
    recommended_v037_items: list[str]
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
            "recommended_v037_items",
            "recommended_later_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        if not _contains_all(self.recommended_v037_items, RECOMMENDED_V037_ITEMS):
            raise ValueError("recommended_v037_items missing required v0.37 items")
        if not _contains_all(self.future_track_items, FUTURE_TRACK_ITEMS):
            raise ValueError("future_track_items missing required future-track items")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxReleaseManifest:
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
    release_flags: PatchApplySandboxReleaseFlagSet
    known_gaps: list[str]
    known_risks: list[str]
    next_handoff_id: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("release_manifest_id", "release_name", "snapshot_id", "focused_test_command", "full_track_test_command"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_versions_include_v036_track(self.included_versions)
        for name in ("included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        if not patch_apply_sandbox_flags_preserve_no_live_apply(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class PatchApplySandboxAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str]
    reviewed_test_refs: list[str]
    reviewed_doc_refs: list[str]
    boundary_checks: list[str]
    negative_runtime_checks: list[str]
    sandbox_capability_checks: list[str]
    no_live_workspace_write_confirmed: bool
    no_live_code_edit_confirmed: bool
    no_unrestricted_patch_application_confirmed: bool
    no_apply_patch_confirmed: bool
    no_git_apply_confirmed: bool
    no_test_execution_confirmed: bool
    no_shell_execution_confirmed: bool
    no_subprocess_execution_confirmed: bool
    no_command_execution_confirmed: bool
    no_dependency_install_confirmed: bool
    no_reference_execution_confirmed: bool
    no_reference_import_confirmed: bool
    no_external_agent_execution_confirmed: bool
    no_claude_code_invocation_confirmed: bool
    no_codex_cli_invocation_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_infinite_agent_loop_confirmed: bool
    no_automatic_repair_confirmed: bool
    no_multi_cycle_loop_confirmed: bool
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
    unsafe_readiness_flags_false_confirmed: bool
    sandbox_write_scoped_to_validated_root_confirmed: bool
    single_cycle_agentic_task_confirmed: bool
    human_handoff_required_confirmed: bool
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
            "sandbox_capability_checks",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_true(
            self,
            NO_AUDIT_CONFIRMATION_NAMES
            + (
                "unsafe_readiness_flags_false_confirmed",
                "sandbox_write_scoped_to_validated_root_confirmed",
                "single_cycle_agentic_task_confirmed",
                "human_handoff_required_confirmed",
            ),
        )
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class BoundedAgenticOperationConsolidationRecord:
    bounded_agentic_record_id: str
    version: str
    bounded_function_task_confirmed: bool
    single_cycle_only_confirmed: bool
    human_handoff_required_confirmed: bool
    automatic_retry_blocked: bool
    automatic_repair_blocked: bool
    multi_cycle_loop_blocked: bool
    independent_agent_runtime_blocked: bool
    external_agent_runtime_blocked: bool
    dominion_runtime_blocked: bool
    completed_capabilities: list[str]
    future_track_items: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("bounded_agentic_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_true(
            self,
            (
                "bounded_function_task_confirmed",
                "single_cycle_only_confirmed",
                "human_handoff_required_confirmed",
                "automatic_retry_blocked",
                "automatic_repair_blocked",
                "multi_cycle_loop_blocked",
                "independent_agent_runtime_blocked",
                "external_agent_runtime_blocked",
                "dominion_runtime_blocked",
            ),
        )
        _validate_string_list("completed_capabilities", self.completed_capabilities)
        _validate_string_list("future_track_items", self.future_track_items)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class DigestionDominionSandboxConsolidationRecord:
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
        _validate_true(
            self,
            (
                "digestion_first_policy_confirmed",
                "dominion_fallback_future_gated",
                "external_agent_patterns_recorded",
                "external_agent_execution_blocked",
                "infinite_loop_blocked",
                "recursive_self_invocation_blocked",
                "automatic_repair_loop_blocked",
                "dominion_runtime_blocked",
            ),
        )
        for name in ("safely_digested_items", "rejected_dominion_like_items", "future_track_dominion_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class ExternalAgentControlSandboxConsolidationRecord:
    external_agent_record_id: str
    version: str
    observed_pattern_kinds: list[str]
    blocked_pattern_kinds: list[str]
    future_gated_pattern_kinds: list[str]
    denied_cli_commands: list[str]
    risk_notes: list[str]
    execution_allowed: bool
    external_agent_runtime_allowed: bool
    dominion_runtime_allowed: bool
    infinite_loop_allowed: bool
    automatic_repair_allowed: bool
    multi_cycle_loop_allowed: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("external_agent_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("observed_pattern_kinds", "blocked_pattern_kinds", "future_gated_pattern_kinds", "denied_cli_commands", "risk_notes"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "execution_allowed",
                "external_agent_runtime_allowed",
                "dominion_runtime_allowed",
                "infinite_loop_allowed",
                "automatic_repair_allowed",
                "multi_cycle_loop_allowed",
            ),
        )
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V037HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    controlled_sandbox_test_runner_items: list[str]
    allowlisted_test_command_policy_items: list[str]
    timeout_and_resource_limit_items: list[str]
    bounded_output_items: list[str]
    no_network_items: list[str]
    no_dependency_install_by_default_items: list[str]
    test_result_envelope_items: list[str]
    feedback_report_items: list[str]
    repair_suggestion_metadata_items: list[str]
    human_checkpoint_items: list[str]
    reusable_apply_candidate_items: list[str]
    reusable_dry_run_items: list[str]
    reusable_sandbox_workspace_items: list[str]
    reusable_sandbox_apply_items: list[str]
    reusable_validation_items: list[str]
    reusable_agentic_task_items: list[str]
    reusable_trace_items: list[str]
    reusable_cli_items: list[str]
    required_new_boundaries: list[str]
    prohibited_until_later_gate: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    readiness_level: PatchApplySandboxConsolidationReadinessLevel | str
    ready_for_v037: bool
    ready_for_execution: bool
    ready_for_test_execution: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_shell_execution: bool
    ready_for_dependency_install: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "source_version", "target_version_track", "source_snapshot_id", "recommended_next_track", "recommended_next_release"):
            _require_non_blank(name, getattr(self, name))
        if V0369_VERSION not in self.source_version:
            raise ValueError("source_version must include v0.36.9")
        if "v0.37" not in self.target_version_track:
            raise ValueError("target_version_track must refer to v0.37")
        if "Controlled Sandbox Test Runner & Feedback Loop" not in self.recommended_next_track:
            raise ValueError("recommended_next_track must mention Controlled Sandbox Test Runner & Feedback Loop")
        for name in (
            "controlled_sandbox_test_runner_items",
            "allowlisted_test_command_policy_items",
            "timeout_and_resource_limit_items",
            "bounded_output_items",
            "no_network_items",
            "no_dependency_install_by_default_items",
            "test_result_envelope_items",
            "feedback_report_items",
            "repair_suggestion_metadata_items",
            "human_checkpoint_items",
            "reusable_apply_candidate_items",
            "reusable_dry_run_items",
            "reusable_sandbox_workspace_items",
            "reusable_sandbox_apply_items",
            "reusable_validation_items",
            "reusable_agentic_task_items",
            "reusable_trace_items",
            "reusable_cli_items",
            "required_new_boundaries",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_test_execution",
                "ready_for_live_workspace_write",
                "ready_for_patch_application",
                "ready_for_workspace_write",
                "ready_for_code_edit",
                "ready_for_shell_execution",
                "ready_for_dependency_install",
            ),
        )
        if not _contains_all(self.prohibited_until_later_gate, PROHIBITED_CAPABILITIES[:20]):
            raise ValueError("prohibited_until_later_gate missing unsafe gates")
        PatchApplySandboxConsolidationReadinessLevel(self.readiness_level)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V036ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: PatchApplySandboxConsolidationStatus | str
    readiness_level: PatchApplySandboxConsolidationReadinessLevel | str
    summary: str
    completed_items: list[str]
    enabled_sandbox_items: list[str]
    enabled_bounded_agentic_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    runtime_not_ready_items: list[str]
    v037_handoff_summary: str
    ready_for_v037: bool
    ready_for_human_approved_patch_apply_sandbox_v1: bool
    ready_for_apply_candidate_human_approval_contract: bool
    ready_for_dry_run_apply_simulation: bool
    ready_for_sandbox_workspace_policy: bool
    ready_for_sandbox_patch_apply: bool
    ready_for_sandbox_post_apply_validation: bool
    ready_for_bounded_agentic_task_operation_cycle: bool
    ready_for_patch_apply_sandbox_trace_packet_creation: bool
    ready_for_cli_sandbox_apply_surface: bool
    ready_for_execution: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_test_execution: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_reference_execution: bool
    ready_for_reference_import: bool
    ready_for_external_agent_execution: bool
    ready_for_claude_code_invocation: bool
    ready_for_codex_cli_invocation: bool
    ready_for_dominion_runtime: bool
    ready_for_infinite_agent_loop: bool
    ready_for_automatic_repair: bool
    ready_for_multi_cycle_agentic_loop: bool
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
        for name in ("report_id", "release_name", "snapshot_id", "release_manifest_id", "summary", "v037_handoff_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in (
            "completed_items",
            "enabled_sandbox_items",
            "enabled_bounded_agentic_items",
            "blocked_items",
            "future_track_items",
            "runtime_not_ready_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        _validate_false(
            self,
            (
                "ready_for_execution",
                "ready_for_live_workspace_write",
                "ready_for_patch_application",
                "ready_for_workspace_write",
                "ready_for_code_edit",
                "ready_for_apply_patch",
                "ready_for_git_apply",
                "ready_for_test_execution",
                "ready_for_shell_execution",
                "ready_for_subprocess_execution",
                "ready_for_command_execution",
                "ready_for_dependency_install",
                "ready_for_reference_execution",
                "ready_for_reference_import",
                "ready_for_external_agent_execution",
                "ready_for_claude_code_invocation",
                "ready_for_codex_cli_invocation",
                "ready_for_dominion_runtime",
                "ready_for_infinite_agent_loop",
                "ready_for_automatic_repair",
                "ready_for_multi_cycle_agentic_loop",
                "ready_for_provider_invocation",
                "ready_for_direct_network_access",
                "ready_for_credential_access",
                "ready_for_secret_read",
                "ready_for_general_agent_execution",
                "ready_for_autonomous_agent_runtime",
                "ready_for_general_tool_execution",
                "ready_for_persistent_trace_write",
                "ready_for_external_trace_sink",
                "ready_for_ui_runtime",
                "ready_for_external_control",
                "ready_for_authority_grant",
                "production_certified",
            ),
        )
        PatchApplySandboxConsolidationStatus(self.consolidation_status)
        PatchApplySandboxConsolidationReadinessLevel(self.readiness_level)
        _validate_metadata(self.metadata)


def build_patch_apply_sandbox_release_flags(**kwargs: Any) -> PatchApplySandboxReleaseFlagSet:
    return PatchApplySandboxReleaseFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "patch_apply_sandbox_release_flags:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        human_approved_patch_apply_sandbox_v1_ready=kwargs.pop("human_approved_patch_apply_sandbox_v1_ready", True),
        ready_for_v037_handoff=kwargs.pop("ready_for_v037_handoff", True),
        ready_for_apply_sandbox_boundary=kwargs.pop("ready_for_apply_sandbox_boundary", True),
        ready_for_apply_candidate_human_approval_contract=kwargs.pop("ready_for_apply_candidate_human_approval_contract", True),
        ready_for_human_approval_evidence_validation=kwargs.pop("ready_for_human_approval_evidence_validation", True),
        ready_for_dry_run_apply_simulation=kwargs.pop("ready_for_dry_run_apply_simulation", True),
        ready_for_dry_run_hunk_alignment=kwargs.pop("ready_for_dry_run_hunk_alignment", True),
        ready_for_sandbox_workspace_policy=kwargs.pop("ready_for_sandbox_workspace_policy", True),
        ready_for_sandbox_workspace_manifest=kwargs.pop("ready_for_sandbox_workspace_manifest", True),
        ready_for_sandbox_workspace_materialization=kwargs.pop("ready_for_sandbox_workspace_materialization", True),
        ready_for_sandbox_workspace_write=kwargs.pop("ready_for_sandbox_workspace_write", True),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        ready_for_sandbox_patch_apply_result=kwargs.pop("ready_for_sandbox_patch_apply_result", True),
        ready_for_sandbox_post_apply_validation=kwargs.pop("ready_for_sandbox_post_apply_validation", True),
        ready_for_sandbox_reconciliation_report=kwargs.pop("ready_for_sandbox_reconciliation_report", True),
        ready_for_sandbox_safety_regression_scan=kwargs.pop("ready_for_sandbox_safety_regression_scan", True),
        ready_for_sandbox_scope_validation=kwargs.pop("ready_for_sandbox_scope_validation", True),
        ready_for_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_bounded_agentic_task_operation_cycle", True),
        ready_for_agentic_function_task_execution=kwargs.pop("ready_for_agentic_function_task_execution", True),
        ready_for_single_cycle_operation_packet=kwargs.pop("ready_for_single_cycle_operation_packet", True),
        ready_for_human_handoff_after_cycle=kwargs.pop("ready_for_human_handoff_after_cycle", True),
        ready_for_patch_apply_sandbox_trace_packet_creation=kwargs.pop("ready_for_patch_apply_sandbox_trace_packet_creation", True),
        ready_for_bounded_patch_apply_ocel_trace_emission=kwargs.pop("ready_for_bounded_patch_apply_ocel_trace_emission", True),
        ready_for_cli_sandbox_apply_surface=kwargs.pop("ready_for_cli_sandbox_apply_surface", True),
        ready_for_cli_sandbox_apply_run=kwargs.pop("ready_for_cli_sandbox_apply_run", True),
        ready_for_cli_agentic_task_run_once=kwargs.pop("ready_for_cli_agentic_task_run_once", True),
        max_grantable_level=kwargs.pop("max_grantable_level", "D3_SIMULATE"),
        future_track_levels=kwargs.pop("future_track_levels", ["D4_GATE", "D5_GATE", "D6_GATE", "D7_GATE", "D8_GATE", "D9_GATE"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_FLAG_NAMES},
    )


def build_patch_apply_sandbox_snapshot(**kwargs: Any) -> PatchApplySandboxSnapshot:
    flags = kwargs.pop("release_flags", build_patch_apply_sandbox_release_flags())
    return PatchApplySandboxSnapshot(
        snapshot_id=kwargs.pop("snapshot_id", "patch_apply_sandbox_snapshot:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        included_versions=kwargs.pop("included_versions", list(INCLUDED_V036_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(V036_MODULES)),
        included_artifact_groups=kwargs.pop("included_artifact_groups", ["boundary", "candidate", "dry_run", "workspace", "sandbox_apply", "validation", "agentic", "trace", "cli"]),
        release_flags=flags,
        consolidation_status=kwargs.pop("consolidation_status", PatchApplySandboxConsolidationStatus.CONSOLIDATED),
        readiness_level=kwargs.pop("readiness_level", PatchApplySandboxConsolidationReadinessLevel.HANDOFF_READY_FOR_V037),
        summary=kwargs.pop("summary", "Human-approved Patch Apply Sandbox v1 consolidated without live runtime expansion"),
        enabled_sandbox_capabilities=kwargs.pop("enabled_sandbox_capabilities", list(ENABLED_SANDBOX_CAPABILITIES)),
        enabled_bounded_agentic_capabilities=kwargs.pop("enabled_bounded_agentic_capabilities", list(ENABLED_BOUNDED_AGENTIC_CAPABILITIES)),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(PROHIBITED_CAPABILITIES)),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_TESTS)),
        known_gaps=kwargs.pop("known_gaps", ["test execution remains future track for v0.37"]),
        known_risks=kwargs.pop("known_risks", ["sandbox apply could be confused with live apply without boundary language"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["withdraw if any unsafe runtime readiness flag becomes true"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_sandbox_capability_matrix(**kwargs: Any) -> PatchApplySandboxCapabilityMatrix:
    capability_to_version = {
        "apply candidate": "v0.36.1",
        "dry-run apply": "v0.36.2",
        "sandbox workspace": "v0.36.3",
        "sandbox file write": "v0.36.4",
        "sandbox patch apply": "v0.36.4",
        "sandbox static validation": "v0.36.5",
        "single-cycle agentic task": "v0.36.6",
        "trace packet": "v0.36.7",
        "CLI sandbox surface": "v0.36.8",
    }
    return PatchApplySandboxCapabilityMatrix(
        capability_matrix_id=kwargs.pop("capability_matrix_id", "patch_apply_sandbox_capability_matrix:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        enabled_sandbox_capabilities=kwargs.pop("enabled_sandbox_capabilities", list(ENABLED_SANDBOX_CAPABILITIES)),
        enabled_bounded_capabilities=kwargs.pop("enabled_bounded_capabilities", list(ENABLED_BOUNDED_AGENTIC_CAPABILITIES)),
        design_stage_capabilities=kwargs.pop("design_stage_capabilities", ["v0.37 handoff", "controlled sandbox test runner planning"]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(PROHIBITED_CAPABILITIES)),
        future_track_capabilities=kwargs.pop("future_track_capabilities", list(FUTURE_TRACK_ITEMS)),
        capability_to_version=kwargs.pop("capability_to_version", capability_to_version),
        prohibited_capability_to_reason=kwargs.pop("prohibited_capability_to_reason", {capability: "blocked by v0.36 sandbox boundary" for capability in PROHIBITED_CAPABILITIES}),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_DOCS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_sandbox_stage_coverage(coverage_cls: type[PatchApplySandboxStageCoverage] = PatchApplySandboxStageCoverage, **kwargs: Any) -> PatchApplySandboxStageCoverage:
    return coverage_cls(
        coverage_id=kwargs.pop("coverage_id", f"{coverage_cls.__name__}:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        stage_version=kwargs.pop("stage_version", "v0.36.x"),
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", ["model", "builder", "report"]),
        missing_artifact_refs=kwargs.pop("missing_artifact_refs", []),
        covered_test_refs=kwargs.pop("covered_test_refs", ["focused test"]),
        missing_test_refs=kwargs.pop("missing_test_refs", []),
        covered_doc_refs=kwargs.pop("covered_doc_refs", ["version doc"]),
        missing_doc_refs=kwargs.pop("missing_doc_refs", []),
        coverage_notes=kwargs.pop("coverage_notes", ["coverage is release-readiness metadata only"]),
        coverage_complete=kwargs.pop("coverage_complete", True),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", []),
        evidence_refs=kwargs.pop("evidence_refs", []),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_boundary_coverage(**kwargs: Any) -> PatchApplyBoundaryCoverage:
    return build_patch_apply_sandbox_stage_coverage(PatchApplyBoundaryCoverage, stage_version=kwargs.pop("stage_version", "v0.36.0"), **kwargs)


def build_apply_candidate_coverage(**kwargs: Any) -> ApplyCandidateCoverage:
    return build_patch_apply_sandbox_stage_coverage(ApplyCandidateCoverage, stage_version=kwargs.pop("stage_version", "v0.36.1"), **kwargs)


def build_dry_run_apply_coverage(**kwargs: Any) -> DryRunApplyCoverage:
    return build_patch_apply_sandbox_stage_coverage(DryRunApplyCoverage, stage_version=kwargs.pop("stage_version", "v0.36.2"), **kwargs)


def build_sandbox_workspace_coverage(**kwargs: Any) -> SandboxWorkspaceCoverage:
    return build_patch_apply_sandbox_stage_coverage(SandboxWorkspaceCoverage, stage_version=kwargs.pop("stage_version", "v0.36.3"), **kwargs)


def build_sandbox_patch_apply_coverage(**kwargs: Any) -> SandboxPatchApplyCoverage:
    return build_patch_apply_sandbox_stage_coverage(SandboxPatchApplyCoverage, stage_version=kwargs.pop("stage_version", "v0.36.4"), **kwargs)


def build_sandbox_post_apply_validation_coverage(**kwargs: Any) -> SandboxPostApplyValidationCoverage:
    return build_patch_apply_sandbox_stage_coverage(SandboxPostApplyValidationCoverage, stage_version=kwargs.pop("stage_version", "v0.36.5"), **kwargs)


def build_bounded_agentic_operation_coverage(**kwargs: Any) -> BoundedAgenticOperationCoverage:
    return build_patch_apply_sandbox_stage_coverage(BoundedAgenticOperationCoverage, stage_version=kwargs.pop("stage_version", "v0.36.6"), **kwargs)


def build_patch_apply_trace_coverage(**kwargs: Any) -> PatchApplyTraceCoverage:
    return build_patch_apply_sandbox_stage_coverage(PatchApplyTraceCoverage, stage_version=kwargs.pop("stage_version", "v0.36.7"), **kwargs)


def build_cli_sandbox_apply_surface_coverage(**kwargs: Any) -> CLISandboxApplySurfaceCoverage:
    return build_patch_apply_sandbox_stage_coverage(CLISandboxApplySurfaceCoverage, stage_version=kwargs.pop("stage_version", "v0.36.8"), **kwargs)


def build_patch_apply_sandbox_boundary_register(**kwargs: Any) -> PatchApplySandboxBoundaryRegister:
    return PatchApplySandboxBoundaryRegister(
        boundary_register_id=kwargs.pop("boundary_register_id", "patch_apply_sandbox_boundary_register:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        inherited_boundaries=kwargs.pop("inherited_boundaries", ["v0.30-v0.35 no live runtime authority", "v0.36 sandbox-only apply boundary"]),
        active_sandbox_boundaries=kwargs.pop("active_sandbox_boundaries", ["validated sandbox root", "sandbox-only file write", "sandbox-only patch apply"]),
        active_bounded_agentic_boundaries=kwargs.pop("active_bounded_agentic_boundaries", ["single-cycle operation", "mandatory stop reason", "mandatory human handoff"]),
        prohibited_boundaries=kwargs.pop("prohibited_boundaries", list(PROHIBITED_CAPABILITIES)),
        future_gate_boundaries=kwargs.pop("future_gate_boundaries", list(FUTURE_TRACK_ITEMS)),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_DOCS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_sandbox_risk_register(**kwargs: Any) -> PatchApplySandboxRiskRegister:
    return PatchApplySandboxRiskRegister(
        risk_register_id=kwargs.pop("risk_register_id", "patch_apply_sandbox_risk_register:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        known_risks=kwargs.pop("known_risks", ["sandbox apply confusion with live apply", "agentic wording confusion with autonomous runtime"]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", ["live apply", "test execution", "external agent execution", "Dominion runtime"]),
        prohibited_runtime_surfaces=kwargs.pop("prohibited_runtime_surfaces", list(PROHIBITED_CAPABILITIES)),
        mitigations=kwargs.pop("mitigations", ["unsafe readiness flags remain false", "v0.37 handoff is design-stage only"]),
        unresolved_risks=kwargs.pop("unresolved_risks", ["test feedback loop is not yet implemented"]),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_TESTS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_sandbox_gap_register(**kwargs: Any) -> PatchApplySandboxGapRegister:
    return PatchApplySandboxGapRegister(
        gap_register_id=kwargs.pop("gap_register_id", "patch_apply_sandbox_gap_register:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", ["test execution remains future track"]),
        future_track_items=kwargs.pop("future_track_items", list(FUTURE_TRACK_ITEMS)),
        recommended_v037_items=kwargs.pop("recommended_v037_items", list(RECOMMENDED_V037_ITEMS)),
        recommended_later_items=kwargs.pop("recommended_later_items", ["live apply remains later gated", "Dominion runtime remains later gated"]),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_DOCS)),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_sandbox_release_manifest(**kwargs: Any) -> PatchApplySandboxReleaseManifest:
    flags = kwargs.pop("release_flags", build_patch_apply_sandbox_release_flags())
    return PatchApplySandboxReleaseManifest(
        release_manifest_id=kwargs.pop("release_manifest_id", "patch_apply_sandbox_release_manifest:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        snapshot_id=kwargs.pop("snapshot_id", "patch_apply_sandbox_snapshot:v0.36.9"),
        included_versions=kwargs.pop("included_versions", list(INCLUDED_V036_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(V036_MODULES)),
        included_docs=kwargs.pop("included_docs", list(V036_DOCS)),
        included_tests=kwargs.pop("included_tests", list(V036_TESTS)),
        focused_test_command=kwargs.pop("focused_test_command", "py -m pytest tests/test_v0369_patch_apply_sandbox_consolidation.py"),
        full_track_test_command=kwargs.pop("full_track_test_command", "py -m pytest tests/test_v0360_patch_apply_sandbox_boundary.py ... tests/test_v0369_patch_apply_sandbox_consolidation.py"),
        release_flags=flags,
        known_gaps=kwargs.pop("known_gaps", ["test execution remains future track for v0.37"]),
        known_risks=kwargs.pop("known_risks", ["sandbox apply is not live apply"]),
        next_handoff_id=kwargs.pop("next_handoff_id", "v037_handoff_packet:v0.36.9"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_patch_apply_sandbox_audit_trail(**kwargs: Any) -> PatchApplySandboxAuditTrail:
    return PatchApplySandboxAuditTrail(
        audit_trail_id=kwargs.pop("audit_trail_id", "patch_apply_sandbox_audit_trail:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        reviewed_artifact_refs=kwargs.pop("reviewed_artifact_refs", list(V036_MODULES)),
        reviewed_test_refs=kwargs.pop("reviewed_test_refs", list(V036_TESTS)),
        reviewed_doc_refs=kwargs.pop("reviewed_doc_refs", list(V036_DOCS)),
        boundary_checks=kwargs.pop("boundary_checks", ["sandbox write scoped to validated root", "live write blocked"]),
        negative_runtime_checks=kwargs.pop("negative_runtime_checks", list(PROHIBITED_CAPABILITIES)),
        sandbox_capability_checks=kwargs.pop("sandbox_capability_checks", list(ENABLED_SANDBOX_CAPABILITIES)),
        unsafe_readiness_flags_false_confirmed=kwargs.pop("unsafe_readiness_flags_false_confirmed", True),
        sandbox_write_scoped_to_validated_root_confirmed=kwargs.pop("sandbox_write_scoped_to_validated_root_confirmed", True),
        single_cycle_agentic_task_confirmed=kwargs.pop("single_cycle_agentic_task_confirmed", True),
        human_handoff_required_confirmed=kwargs.pop("human_handoff_required_confirmed", True),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_TESTS)),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in NO_AUDIT_CONFIRMATION_NAMES},
    )


def build_bounded_agentic_operation_consolidation_record(**kwargs: Any) -> BoundedAgenticOperationConsolidationRecord:
    return BoundedAgenticOperationConsolidationRecord(
        bounded_agentic_record_id=kwargs.pop("bounded_agentic_record_id", "bounded_agentic_operation_consolidation_record:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        bounded_function_task_confirmed=kwargs.pop("bounded_function_task_confirmed", True),
        single_cycle_only_confirmed=kwargs.pop("single_cycle_only_confirmed", True),
        human_handoff_required_confirmed=kwargs.pop("human_handoff_required_confirmed", True),
        automatic_retry_blocked=kwargs.pop("automatic_retry_blocked", True),
        automatic_repair_blocked=kwargs.pop("automatic_repair_blocked", True),
        multi_cycle_loop_blocked=kwargs.pop("multi_cycle_loop_blocked", True),
        independent_agent_runtime_blocked=kwargs.pop("independent_agent_runtime_blocked", True),
        external_agent_runtime_blocked=kwargs.pop("external_agent_runtime_blocked", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        completed_capabilities=kwargs.pop("completed_capabilities", list(ENABLED_BOUNDED_AGENTIC_CAPABILITIES)),
        future_track_items=kwargs.pop("future_track_items", ["bounded repair loop remains future gated", "multi-cycle loop remains blocked"]),
        summary=kwargs.pop("summary", "bounded agentic operation remains single-cycle metadata/function operation only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_digestion_dominion_sandbox_consolidation_record(**kwargs: Any) -> DigestionDominionSandboxConsolidationRecord:
    return DigestionDominionSandboxConsolidationRecord(
        digestion_consolidation_id=kwargs.pop("digestion_consolidation_id", "digestion_dominion_sandbox_consolidation_record:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        digestion_first_policy_confirmed=kwargs.pop("digestion_first_policy_confirmed", True),
        dominion_fallback_future_gated=kwargs.pop("dominion_fallback_future_gated", True),
        external_agent_patterns_recorded=kwargs.pop("external_agent_patterns_recorded", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_loop_blocked=kwargs.pop("infinite_loop_blocked", True),
        recursive_self_invocation_blocked=kwargs.pop("recursive_self_invocation_blocked", True),
        automatic_repair_loop_blocked=kwargs.pop("automatic_repair_loop_blocked", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        safely_digested_items=kwargs.pop("safely_digested_items", ["static reference patterns", "sandbox apply lifecycle metadata"]),
        rejected_dominion_like_items=kwargs.pop("rejected_dominion_like_items", ["recursive self invocation", "external agent loop", "Dominion runtime"]),
        future_track_dominion_items=kwargs.pop("future_track_dominion_items", ["Dominion runtime gated review"]),
        summary=kwargs.pop("summary", "Digestion-first policy confirmed; Dominion remains future-gated metadata only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_external_agent_control_sandbox_consolidation_record(**kwargs: Any) -> ExternalAgentControlSandboxConsolidationRecord:
    return ExternalAgentControlSandboxConsolidationRecord(
        external_agent_record_id=kwargs.pop("external_agent_record_id", "external_agent_control_sandbox_consolidation_record:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        observed_pattern_kinds=kwargs.pop("observed_pattern_kinds", ["OpenCode", "Hermes", "OpenClaw", "Claude Code", "Codex CLI"]),
        blocked_pattern_kinds=kwargs.pop("blocked_pattern_kinds", ["external_agent_execution", "recursive_agent", "harness_execute"]),
        future_gated_pattern_kinds=kwargs.pop("future_gated_pattern_kinds", ["external harness adapter"]),
        denied_cli_commands=kwargs.pop("denied_cli_commands", ["run-opencode", "run-hermes", "run-openclaw", "run-claude-code", "run-codex"]),
        risk_notes=kwargs.pop("risk_notes", ["external agent orchestration remains blocked"]),
        execution_allowed=kwargs.pop("execution_allowed", False),
        external_agent_runtime_allowed=kwargs.pop("external_agent_runtime_allowed", False),
        dominion_runtime_allowed=kwargs.pop("dominion_runtime_allowed", False),
        infinite_loop_allowed=kwargs.pop("infinite_loop_allowed", False),
        automatic_repair_allowed=kwargs.pop("automatic_repair_allowed", False),
        multi_cycle_loop_allowed=kwargs.pop("multi_cycle_loop_allowed", False),
        summary=kwargs.pop("summary", "external agent control patterns are recorded as blocked/future-gated metadata only"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v037_handoff_packet(**kwargs: Any) -> V037HandoffPacket:
    return V037HandoffPacket(
        handoff_id=kwargs.pop("handoff_id", "v037_handoff_packet:v0.36.9"),
        source_version=kwargs.pop("source_version", V0369_VERSION),
        target_version_track=kwargs.pop("target_version_track", "v0.37"),
        source_snapshot_id=kwargs.pop("source_snapshot_id", "patch_apply_sandbox_snapshot:v0.36.9"),
        release_manifest_id=kwargs.pop("release_manifest_id", "patch_apply_sandbox_release_manifest:v0.36.9"),
        recommended_next_track=kwargs.pop("recommended_next_track", "Controlled Sandbox Test Runner & Feedback Loop"),
        recommended_next_release=kwargs.pop("recommended_next_release", "v0.37.0 test runner boundary foundation"),
        controlled_sandbox_test_runner_items=kwargs.pop("controlled_sandbox_test_runner_items", ["sandbox-only test runner boundary"]),
        allowlisted_test_command_policy_items=kwargs.pop("allowlisted_test_command_policy_items", ["allowlisted test command policy"]),
        timeout_and_resource_limit_items=kwargs.pop("timeout_and_resource_limit_items", ["timeout", "resource limit"]),
        bounded_output_items=kwargs.pop("bounded_output_items", ["bounded output", "redacted output"]),
        no_network_items=kwargs.pop("no_network_items", ["no network"]),
        no_dependency_install_by_default_items=kwargs.pop("no_dependency_install_by_default_items", ["no dependency install by default"]),
        test_result_envelope_items=kwargs.pop("test_result_envelope_items", ["test result envelope"]),
        feedback_report_items=kwargs.pop("feedback_report_items", ["feedback report"]),
        repair_suggestion_metadata_items=kwargs.pop("repair_suggestion_metadata_items", ["repair suggestion metadata only"]),
        human_checkpoint_items=kwargs.pop("human_checkpoint_items", ["human checkpoint before repair loop"]),
        reusable_apply_candidate_items=kwargs.pop("reusable_apply_candidate_items", ["ApplyCandidateEnvelope"]),
        reusable_dry_run_items=kwargs.pop("reusable_dry_run_items", ["DryRunApplySimulationResult"]),
        reusable_sandbox_workspace_items=kwargs.pop("reusable_sandbox_workspace_items", ["SandboxWorkspaceManifest"]),
        reusable_sandbox_apply_items=kwargs.pop("reusable_sandbox_apply_items", ["SandboxPatchApplyResult"]),
        reusable_validation_items=kwargs.pop("reusable_validation_items", ["SandboxPostApplyValidationReport"]),
        reusable_agentic_task_items=kwargs.pop("reusable_agentic_task_items", ["AgenticOperationRunPacket"]),
        reusable_trace_items=kwargs.pop("reusable_trace_items", ["PatchApplySandboxTracePacket"]),
        reusable_cli_items=kwargs.pop("reusable_cli_items", ["CLISandboxApplySurface"]),
        required_new_boundaries=kwargs.pop("required_new_boundaries", list(RECOMMENDED_V037_ITEMS)),
        prohibited_until_later_gate=kwargs.pop("prohibited_until_later_gate", list(PROHIBITED_CAPABILITIES)),
        future_track_items=kwargs.pop("future_track_items", list(FUTURE_TRACK_ITEMS)),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_DOCS)),
        readiness_level=kwargs.pop("readiness_level", PatchApplySandboxConsolidationReadinessLevel.HANDOFF_READY_FOR_V037),
        ready_for_v037=kwargs.pop("ready_for_v037", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_test_execution=kwargs.pop("ready_for_test_execution", False),
        ready_for_live_workspace_write=kwargs.pop("ready_for_live_workspace_write", False),
        ready_for_patch_application=kwargs.pop("ready_for_patch_application", False),
        ready_for_workspace_write=kwargs.pop("ready_for_workspace_write", False),
        ready_for_code_edit=kwargs.pop("ready_for_code_edit", False),
        ready_for_shell_execution=kwargs.pop("ready_for_shell_execution", False),
        ready_for_dependency_install=kwargs.pop("ready_for_dependency_install", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v036_consolidation_report(**kwargs: Any) -> V036ConsolidationReport:
    return V036ConsolidationReport(
        report_id=kwargs.pop("report_id", "v036_consolidation_report:v0.36.9"),
        version=kwargs.pop("version", V0369_VERSION),
        release_name=kwargs.pop("release_name", FOUNDATION_RELEASE_NAME),
        snapshot_id=kwargs.pop("snapshot_id", "patch_apply_sandbox_snapshot:v0.36.9"),
        release_manifest_id=kwargs.pop("release_manifest_id", "patch_apply_sandbox_release_manifest:v0.36.9"),
        handoff_id=kwargs.pop("handoff_id", "v037_handoff_packet:v0.36.9"),
        consolidation_status=kwargs.pop("consolidation_status", PatchApplySandboxConsolidationStatus.CONSOLIDATED),
        readiness_level=kwargs.pop("readiness_level", PatchApplySandboxConsolidationReadinessLevel.HANDOFF_READY_FOR_V037),
        summary=kwargs.pop("summary", "v0.36.x consolidated as Human-approved Patch Apply Sandbox v1 without live runtime authority"),
        completed_items=kwargs.pop("completed_items", list(ENABLED_SANDBOX_CAPABILITIES + ENABLED_BOUNDED_AGENTIC_CAPABILITIES)),
        enabled_sandbox_items=kwargs.pop("enabled_sandbox_items", list(ENABLED_SANDBOX_CAPABILITIES)),
        enabled_bounded_agentic_items=kwargs.pop("enabled_bounded_agentic_items", list(ENABLED_BOUNDED_AGENTIC_CAPABILITIES)),
        blocked_items=kwargs.pop("blocked_items", list(PROHIBITED_CAPABILITIES)),
        future_track_items=kwargs.pop("future_track_items", list(FUTURE_TRACK_ITEMS)),
        runtime_not_ready_items=kwargs.pop("runtime_not_ready_items", list(PROHIBITED_CAPABILITIES)),
        v037_handoff_summary=kwargs.pop("v037_handoff_summary", "v0.37 should begin Controlled Sandbox Test Runner & Feedback Loop as design-stage handoff"),
        ready_for_v037=kwargs.pop("ready_for_v037", True),
        ready_for_human_approved_patch_apply_sandbox_v1=kwargs.pop("ready_for_human_approved_patch_apply_sandbox_v1", True),
        ready_for_apply_candidate_human_approval_contract=kwargs.pop("ready_for_apply_candidate_human_approval_contract", True),
        ready_for_dry_run_apply_simulation=kwargs.pop("ready_for_dry_run_apply_simulation", True),
        ready_for_sandbox_workspace_policy=kwargs.pop("ready_for_sandbox_workspace_policy", True),
        ready_for_sandbox_patch_apply=kwargs.pop("ready_for_sandbox_patch_apply", True),
        ready_for_sandbox_post_apply_validation=kwargs.pop("ready_for_sandbox_post_apply_validation", True),
        ready_for_bounded_agentic_task_operation_cycle=kwargs.pop("ready_for_bounded_agentic_task_operation_cycle", True),
        ready_for_patch_apply_sandbox_trace_packet_creation=kwargs.pop("ready_for_patch_apply_sandbox_trace_packet_creation", True),
        ready_for_cli_sandbox_apply_surface=kwargs.pop("ready_for_cli_sandbox_apply_surface", True),
        evidence_refs=kwargs.pop("evidence_refs", list(V036_TESTS)),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["withdraw if unsafe runtime authority is introduced"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in (
            "ready_for_execution",
            "ready_for_live_workspace_write",
            "ready_for_patch_application",
            "ready_for_workspace_write",
            "ready_for_code_edit",
            "ready_for_apply_patch",
            "ready_for_git_apply",
            "ready_for_test_execution",
            "ready_for_shell_execution",
            "ready_for_subprocess_execution",
            "ready_for_command_execution",
            "ready_for_dependency_install",
            "ready_for_reference_execution",
            "ready_for_reference_import",
            "ready_for_external_agent_execution",
            "ready_for_claude_code_invocation",
            "ready_for_codex_cli_invocation",
            "ready_for_dominion_runtime",
            "ready_for_infinite_agent_loop",
            "ready_for_automatic_repair",
            "ready_for_multi_cycle_agentic_loop",
            "ready_for_provider_invocation",
            "ready_for_direct_network_access",
            "ready_for_credential_access",
            "ready_for_secret_read",
            "ready_for_general_agent_execution",
            "ready_for_autonomous_agent_runtime",
            "ready_for_general_tool_execution",
            "ready_for_persistent_trace_write",
            "ready_for_external_trace_sink",
            "ready_for_ui_runtime",
            "ready_for_external_control",
            "ready_for_authority_grant",
            "production_certified",
        )},
    )


def patch_apply_sandbox_flags_preserve_no_live_apply(flags: PatchApplySandboxReleaseFlagSet) -> bool:
    return isinstance(flags, PatchApplySandboxReleaseFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def patch_apply_sandbox_snapshot_is_not_live_runtime(snapshot: PatchApplySandboxSnapshot) -> bool:
    return isinstance(snapshot, PatchApplySandboxSnapshot) and patch_apply_sandbox_flags_preserve_no_live_apply(snapshot.release_flags)


def patch_apply_sandbox_capability_matrix_is_not_permission_grant(matrix: PatchApplySandboxCapabilityMatrix) -> bool:
    return isinstance(matrix, PatchApplySandboxCapabilityMatrix) and _contains_all(matrix.prohibited_capabilities, PROHIBITED_CAPABILITIES[:-1])


def patch_apply_sandbox_audit_confirms_no_unsafe_runtime(audit: PatchApplySandboxAuditTrail) -> bool:
    if not isinstance(audit, PatchApplySandboxAuditTrail):
        return False
    return all(getattr(audit, name) is True for name in NO_AUDIT_CONFIRMATION_NAMES) and audit.unsafe_readiness_flags_false_confirmed


def bounded_agentic_consolidation_record_is_not_autonomous_runtime(record: BoundedAgenticOperationConsolidationRecord) -> bool:
    return (
        isinstance(record, BoundedAgenticOperationConsolidationRecord)
        and record.bounded_function_task_confirmed
        and record.single_cycle_only_confirmed
        and record.independent_agent_runtime_blocked
        and record.multi_cycle_loop_blocked
        and record.automatic_repair_blocked
    )


def digestion_dominion_sandbox_record_is_not_runtime(record: DigestionDominionSandboxConsolidationRecord) -> bool:
    return isinstance(record, DigestionDominionSandboxConsolidationRecord) and record.digestion_first_policy_confirmed and record.dominion_runtime_blocked


def external_agent_control_sandbox_record_is_not_execution(record: ExternalAgentControlSandboxConsolidationRecord) -> bool:
    return (
        isinstance(record, ExternalAgentControlSandboxConsolidationRecord)
        and not record.execution_allowed
        and not record.external_agent_runtime_allowed
        and not record.dominion_runtime_allowed
        and not record.infinite_loop_allowed
        and not record.automatic_repair_allowed
        and not record.multi_cycle_loop_allowed
    )


def v037_handoff_packet_is_design_stage_only(packet: V037HandoffPacket) -> bool:
    return (
        isinstance(packet, V037HandoffPacket)
        and packet.ready_for_v037
        and not packet.ready_for_execution
        and not packet.ready_for_test_execution
        and not packet.ready_for_live_workspace_write
        and not packet.ready_for_patch_application
        and not packet.ready_for_shell_execution
        and not packet.ready_for_dependency_install
    )


def v036_consolidation_report_is_not_runtime_ready(report: V036ConsolidationReport) -> bool:
    if not isinstance(report, V036ConsolidationReport):
        return False
    unsafe_names = tuple(name for name in report.__dataclass_fields__ if name.startswith("ready_for_") and name not in {
        "ready_for_v037",
        "ready_for_human_approved_patch_apply_sandbox_v1",
        "ready_for_apply_candidate_human_approval_contract",
        "ready_for_dry_run_apply_simulation",
        "ready_for_sandbox_workspace_policy",
        "ready_for_sandbox_patch_apply",
        "ready_for_sandbox_post_apply_validation",
        "ready_for_bounded_agentic_task_operation_cycle",
        "ready_for_patch_apply_sandbox_trace_packet_creation",
        "ready_for_cli_sandbox_apply_surface",
    })
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
