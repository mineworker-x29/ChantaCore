"""v0.38.9 bounded repair proposal loop consolidation metadata.

This module is intentionally limited to pure dataclass construction and
conservative validation. It does not read files, write files, execute commands,
apply patches, run tests, invoke providers, or grant runtime authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0389_VERSION = "v0.38.9"
FOUNDATION_RELEASE_NAME = "Bounded Repair Proposal Loop v1"
V039_RECOMMENDED_TRACK = "Human-approved Sandbox Repair Apply & Re-test Loop"

INCLUDED_V038_VERSIONS = [
    "v0.38.0",
    "v0.38.1",
    "v0.38.2",
    "v0.38.3",
    "v0.38.4",
    "v0.38.5",
    "v0.38.6",
    "v0.38.7",
    "v0.38.8",
]

INCLUDED_MODULES = [
    "repair_proposal_boundary",
    "repair_proposal_evidence",
    "repair_source_context",
    "repair_scope_planning",
    "repair_patch_metadata",
    "repair_proposal_safety",
    "repair_human_review",
    "repair_proposal_loop_trial",
    "repair_cli_surface",
    "repair_proposal_consolidation",
]

INCLUDED_DOCS = [
    "docs/versions/v0.38/v0.38.0_bounded_repair_proposal_boundary.md",
    "docs/versions/v0.38/v0.38.1_repair_proposal_evidence_contract.md",
    "docs/versions/v0.38/v0.38.2_read_only_sandbox_source_context.md",
    "docs/versions/v0.38/v0.38.3_repair_scope_planner_change_intent.md",
    "docs/versions/v0.38/v0.38.4_proposed_diff_code_hunk_metadata.md",
    "docs/versions/v0.38/v0.38.5_repair_proposal_safety_validation.md",
    "docs/versions/v0.38/v0.38.6_human_review_packet_approval_request.md",
    "docs/versions/v0.38/v0.38.7_bounded_repair_proposal_loop_trial.md",
    "docs/versions/v0.38/v0.38.8_cli_repair_proposal_surface.md",
    "docs/versions/v0.38/v0.38.9_bounded_repair_proposal_loop_consolidation.md",
]

INCLUDED_TESTS = [
    "tests/test_v0380_repair_proposal_boundary.py",
    "tests/test_v0381_repair_proposal_evidence_contract.py",
    "tests/test_v0382_read_only_sandbox_source_context.py",
    "tests/test_v0383_repair_scope_planner_change_intent.py",
    "tests/test_v0384_proposed_diff_code_hunk_metadata.py",
    "tests/test_v0385_repair_proposal_safety_validation.py",
    "tests/test_v0386_human_review_packet_approval_request.py",
    "tests/test_v0387_bounded_repair_proposal_loop_trial.py",
    "tests/test_v0388_cli_repair_proposal_surface.py",
    "tests/test_v0389_bounded_repair_proposal_loop_consolidation.py",
]

ENABLED_CAPABILITIES = [
    "repair_proposal_boundary_metadata",
    "repair_proposal_evidence_contract_metadata",
    "repair_proposal_evidence_bundle_metadata",
    "read_only_sandbox_source_context_snapshot_metadata",
    "repair_scope_planning_metadata",
    "repair_change_intent_model_metadata",
    "proposed_diff_metadata",
    "proposed_code_hunk_metadata",
    "proposed_patch_envelope_metadata",
    "repair_proposal_safety_static_validation_metadata",
    "human_review_packet_metadata",
    "approval_request_contract_metadata",
    "one_shot_repair_proposal_loop_packet_metadata",
    "safe_cli_repair_proposal_preview_surface",
    "future_v039_handoff_metadata",
]

PROHIBITED_CAPABILITIES = [
    "live_workspace_read",
    "unbounded_source_read",
    "reference_source_read",
    "secret_read",
    "source_write",
    "sandbox_source_write",
    "patch_file_write",
    "file_edit",
    "patch_application",
    "apply_patch_runtime_call",
    "git_apply_runtime_call",
    "applied_diff_generation",
    "applied_code_hunk_generation",
    "sandbox_repair_apply",
    "live_workspace_apply",
    "repair_execution",
    "automatic_repair",
    "retry_loop",
    "multi_cycle_repair_loop",
    "autonomous_loop_runtime",
    "human_approval_capture",
    "approval_grant",
    "apply_permission",
    "review_packet_file_export",
    "review_packet_external_send",
    "ui_runtime",
    "test_execution",
    "shell_execution",
    "subprocess_execution",
    "arbitrary_command_execution",
    "dependency_install",
    "network_access",
    "model_provider_invocation",
    "codex_cli_invocation",
    "claude_code_invocation",
    "external_agent_execution",
    "general_tool_execution",
    "dominion_runtime",
    "credential_access",
    "persistent_trace_write",
    "external_trace_sink",
    "authority_grant",
    "production_certification",
]

REQUIRED_PROHIBITED_BOUNDARIES = [
    "live_read",
    "unbounded_source_read",
    "secret_read",
    "source_write",
    "patch_file_write",
    "file_edit",
    "patch_application",
    "apply_patch",
    "git_apply",
    "approval_capture",
    "approval_grant",
    "apply_permission",
    "repair_execution",
    "automatic_repair",
    "retry_loop",
    "multi_cycle_loop",
    "autonomous_loop_runtime",
    "test_execution",
    "shell_execution",
    "subprocess_execution",
    "dependency_install",
    "network_access",
    "model_provider_invocation",
    "external_agent_execution",
    "dominion_runtime",
    "persistent_trace_write",
    "UI_runtime",
    "external_control",
    "authority_grant",
]

REQUIRED_PROHIBITED_RUNTIME_SURFACES = [
    "source_write",
    "patch_apply",
    "repair_execution",
    "approval_capture",
    "test_execution",
    "shell",
    "subprocess",
    "install",
    "network",
    "model",
    "external_agent",
    "Dominion",
    "production_certification",
]

RECOMMENDED_V039_ITEMS = [
    "human-approved sandbox apply boundary",
    "approval artifact validation",
    "sandbox-only patch application",
    "sandbox apply result envelope",
    "controlled re-test",
    "before/after comparison",
    "cold repair evaluation",
    "rollback/discard metadata",
]

FUTURE_TRACK_ITEMS = [
    "live apply gate",
    "persistent trace store",
    "UI runtime",
    "external harness adapter",
    "Dominion runtime gated review",
]

PROHIBITED_UNTIL_LATER_GATE = [
    "live apply",
    "live write",
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

UNSAFE_RELEASE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_live_workspace_read",
    "ready_for_unbounded_source_read",
    "ready_for_reference_source_read",
    "ready_for_secret_read",
    "ready_for_source_file_write",
    "ready_for_sandbox_source_write",
    "ready_for_patch_file_write",
    "ready_for_file_edit",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_applied_diff_generation",
    "ready_for_applied_code_hunk_generation",
    "ready_for_new_proposed_diff_generation",
    "ready_for_new_proposed_code_hunk_generation",
    "ready_for_new_proposed_patch_envelope_generation",
    "ready_for_repair_execution",
    "ready_for_repair_apply",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_write",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_automatic_repair",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_repair_loop",
    "ready_for_autonomous_loop_runtime",
    "ready_for_human_approval_capture",
    "ready_for_approval_grant",
    "ready_for_apply_permission",
    "ready_for_test_execution",
    "ready_for_controlled_test_subprocess",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
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
]

UNSAFE_HANDOFF_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_human_approval_capture",
    "ready_for_apply_permission",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_repair_execution",
    "ready_for_test_execution",
    "ready_for_shell_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_model_provider_invocation",
    "ready_for_external_agent_execution",
    "ready_for_dominion_runtime",
]

UNSAFE_REPORT_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_patch_application",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_repair_execution",
    "ready_for_sandbox_repair_apply",
    "ready_for_test_execution",
    "ready_for_human_approval_capture",
    "ready_for_approval_grant",
    "ready_for_apply_permission",
    "ready_for_model_provider_invocation",
    "ready_for_external_agent_execution",
    "ready_for_dominion_runtime",
    "production_certified",
]


class RepairProposalConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class RepairProposalConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_READY = "boundary_ready"
    EVIDENCE_SOURCE_SCOPE_READY = "evidence_source_scope_ready"
    PATCH_METADATA_READY = "patch_metadata_ready"
    SAFETY_REVIEW_READY = "safety_review_ready"
    LOOP_CLI_SURFACE_READY = "loop_cli_surface_ready"
    BOUNDED_REPAIR_PROPOSAL_LOOP_V1_READY = "bounded_repair_proposal_loop_v1_ready"
    HANDOFF_READY_FOR_V039 = "handoff_ready_for_v039"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0389_VERSION not in version:
        raise ValueError("version must include v0.38.9")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise ValueError(f"{name} must be a list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise ValueError(f"{name} must be a dict")


def _validate_false(instance: Any, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name):
            raise ValueError(f"{name} must remain false in v0.38.9")


def _require_subset(name: str, values: list[str], required: list[str]) -> None:
    missing = [item for item in required if item not in values]
    if missing:
        raise ValueError(f"{name} is missing required entries: {missing}")


def _validate_included_versions(values: list[str]) -> None:
    _require_subset("included_versions", values, INCLUDED_V038_VERSIONS)


def _all_bool_values_true(values: dict[str, bool]) -> bool:
    return all(value is True for value in values.values())


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


@dataclass(frozen=True)
class RepairProposalReleaseFlagSet:
    flag_set_id: str
    version: str = V0389_VERSION
    bounded_repair_proposal_loop_v1_ready: bool = True
    ready_for_v039_handoff: bool = True
    ready_for_v039_human_approved_sandbox_repair_apply_contract_input: bool = True
    ready_for_repair_proposal_boundary: bool = True
    ready_for_repair_evidence_contract: bool = True
    ready_for_repair_evidence_bundle: bool = True
    ready_for_repair_evidence_assessment: bool = True
    ready_for_read_only_sandbox_source_context: bool = True
    ready_for_validated_read_only_sandbox_source_read: bool = True
    ready_for_source_context_snapshot: bool = True
    ready_for_bounded_source_excerpt: bool = True
    ready_for_repair_scope_planning: bool = True
    ready_for_repair_change_intent_model: bool = True
    ready_for_affected_file_candidates: bool = True
    ready_for_affected_symbol_candidates: bool = True
    ready_for_proposed_diff_metadata: bool = True
    ready_for_proposed_code_hunk_metadata: bool = True
    ready_for_proposed_patch_envelope_metadata: bool = True
    ready_for_repair_proposal_safety_validation: bool = True
    ready_for_static_patch_metadata_validation: bool = True
    ready_for_boundary_violation_scan: bool = True
    ready_for_unsafe_operation_detection: bool = True
    ready_for_human_review_packet: bool = True
    ready_for_approval_request_contract: bool = True
    ready_for_review_checklist: bool = True
    ready_for_apply_precondition_metadata: bool = True
    ready_for_one_shot_repair_proposal_loop_trial: bool = True
    ready_for_one_shot_loop_packet: bool = True
    ready_for_loop_artifact_bundle: bool = True
    ready_for_loop_step_records: bool = True
    ready_for_loop_stop_condition: bool = True
    ready_for_cli_repair_proposal_surface: bool = True
    ready_for_cli_command_registry: bool = True
    ready_for_cli_argument_parsing: bool = True
    ready_for_cli_preview: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_live_workspace_read: bool = False
    ready_for_unbounded_source_read: bool = False
    ready_for_reference_source_read: bool = False
    ready_for_secret_read: bool = False
    ready_for_source_file_write: bool = False
    ready_for_sandbox_source_write: bool = False
    ready_for_patch_file_write: bool = False
    ready_for_file_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_applied_diff_generation: bool = False
    ready_for_applied_code_hunk_generation: bool = False
    ready_for_new_proposed_diff_generation: bool = False
    ready_for_new_proposed_code_hunk_generation: bool = False
    ready_for_new_proposed_patch_envelope_generation: bool = False
    ready_for_repair_execution: bool = False
    ready_for_repair_apply: bool = False
    ready_for_sandbox_repair_apply: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_repair_loop: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_repair_loop: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_human_approval_capture: bool = False
    ready_for_approval_grant: bool = False
    ready_for_apply_permission: bool = False
    ready_for_test_execution: bool = False
    ready_for_controlled_test_subprocess: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_tool_execution: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_independent_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    max_grantable_level: str | None = None
    future_track_levels: list[str] = field(default_factory=lambda: ["D4", "D5", "D6", "D7", "D8", "D9"])
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_RELEASE_FLAG_NAMES)
        _validate_string_list("future_track_levels", self.future_track_levels)
        _validate_dict("metadata", self.metadata)
        if self.max_grantable_level not in {None, "D0_OBSERVE", "D1_READ", "D2_PROPOSE", "D3_SIMULATE"}:
            raise ValueError("max_grantable_level must be None or no higher than D3_SIMULATE")
        _require_subset("future_track_levels", self.future_track_levels, ["D4", "D5", "D6", "D7", "D8", "D9"])


@dataclass(frozen=True)
class RepairProposalLoopSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_artifact_groups: list[str]
    release_flags: RepairProposalReleaseFlagSet
    consolidation_status: RepairProposalConsolidationStatus | str
    readiness_level: RepairProposalConsolidationReadinessLevel | str
    summary: str
    enabled_capabilities: list[str]
    prohibited_capabilities: list[str]
    evidence_refs: list[str]
    known_gaps: list[str]
    known_risks: list[str]
    withdrawal_conditions: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("snapshot_id", self.snapshot_id)
        _validate_version(self.version)
        _require_non_blank("release_name", self.release_name)
        _require_non_blank("summary", self.summary)
        if self.release_name != FOUNDATION_RELEASE_NAME:
            raise ValueError("release_name should be Bounded Repair Proposal Loop v1")
        for name in (
            "included_versions",
            "included_modules",
            "included_artifact_groups",
            "enabled_capabilities",
            "prohibited_capabilities",
            "evidence_refs",
            "known_gaps",
            "known_risks",
            "withdrawal_conditions",
        ):
            _validate_list(name, getattr(self, name))
        _validate_included_versions(self.included_versions)
        if not repair_proposal_release_flags_preserve_no_runtime(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProposalCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_capabilities: list[str]
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
            "enabled_capabilities",
            "design_stage_capabilities",
            "prohibited_capabilities",
            "future_track_capabilities",
            "evidence_refs",
        ):
            _validate_list(name, getattr(self, name))
        _validate_dict("capability_to_version", self.capability_to_version)
        _validate_dict("prohibited_capability_to_reason", self.prohibited_capability_to_reason)
        _validate_dict("metadata", self.metadata)
        _require_subset("prohibited_capabilities", self.prohibited_capabilities, PROHIBITED_CAPABILITIES)


@dataclass(frozen=True)
class _RepairProposalCoverageBase:
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
        _require_non_blank("coverage_id", self.coverage_id)
        _validate_version(self.version)
        _require_non_blank("stage_version", self.stage_version)
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
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        if self.coverage_complete and self.blocking_gaps:
            raise ValueError("coverage_complete cannot be true when blocking_gaps is non-empty")


@dataclass(frozen=True)
class RepairProposalStageCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairProposalBoundaryCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairProposalEvidenceCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairSourceContextCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairScopePlanningCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairPatchMetadataCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairSafetyValidationCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairHumanReviewCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairLoopTrialCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairCLISurfaceCoverage(_RepairProposalCoverageBase):
    pass


@dataclass(frozen=True)
class RepairProposalBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str]
    active_bounded_boundaries: list[str]
    active_review_boundaries: list[str]
    prohibited_boundaries: list[str]
    future_gate_boundaries: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version(self.version)
        for name in (
            "inherited_boundaries",
            "active_bounded_boundaries",
            "active_review_boundaries",
            "prohibited_boundaries",
            "future_gate_boundaries",
            "evidence_refs",
        ):
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        _require_subset("prohibited_boundaries", self.prohibited_boundaries, REQUIRED_PROHIBITED_BOUNDARIES)


@dataclass(frozen=True)
class RepairProposalRiskRegister:
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
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        _require_subset(
            "prohibited_runtime_surfaces",
            self.prohibited_runtime_surfaces,
            REQUIRED_PROHIBITED_RUNTIME_SURFACES,
        )


@dataclass(frozen=True)
class RepairProposalGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    future_track_items: list[str]
    recommended_v039_items: list[str]
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
            "recommended_v039_items",
            "recommended_later_items",
            "evidence_refs",
        ):
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        _require_subset("recommended_v039_items", self.recommended_v039_items, RECOMMENDED_V039_ITEMS)
        _require_subset("future_track_items", self.future_track_items, FUTURE_TRACK_ITEMS)


@dataclass(frozen=True)
class RepairProposalReleaseManifest:
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
    release_flags: RepairProposalReleaseFlagSet
    known_gaps: list[str]
    known_risks: list[str]
    next_handoff_id: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("release_manifest_id", "version", "release_name", "snapshot_id"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("included_versions", "included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"):
            _validate_list(name, getattr(self, name))
        _require_non_blank("focused_test_command", self.focused_test_command)
        _require_non_blank("full_track_test_command", self.full_track_test_command)
        _validate_included_versions(self.included_versions)
        if not repair_proposal_release_flags_preserve_no_runtime(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairProposalAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str]
    reviewed_test_refs: list[str]
    reviewed_doc_refs: list[str]
    boundary_checks: list[str]
    negative_runtime_checks: list[str]
    proposal_generation_checks: list[str]
    safety_review_checks: list[str]
    cli_surface_checks: list[str]
    no_live_workspace_read_confirmed: bool = True
    bounded_sandbox_source_read_scoped_to_v0382_confirmed: bool = True
    no_unbounded_source_read_confirmed: bool = True
    no_reference_source_read_confirmed: bool = True
    no_secret_read_confirmed: bool = True
    no_source_write_confirmed: bool = True
    no_patch_file_write_confirmed: bool = True
    no_file_edit_confirmed: bool = True
    no_patch_application_confirmed: bool = True
    no_apply_patch_confirmed: bool = True
    no_git_apply_confirmed: bool = True
    no_repair_execution_confirmed: bool = True
    no_automatic_repair_confirmed: bool = True
    no_retry_loop_confirmed: bool = True
    no_multi_cycle_loop_confirmed: bool = True
    no_autonomous_loop_runtime_confirmed: bool = True
    no_approval_capture_confirmed: bool = True
    no_approval_grant_confirmed: bool = True
    no_apply_permission_confirmed: bool = True
    no_test_execution_confirmed: bool = True
    no_shell_execution_confirmed: bool = True
    no_subprocess_execution_confirmed: bool = True
    no_command_execution_confirmed: bool = True
    no_dependency_install_confirmed: bool = True
    no_network_access_confirmed: bool = True
    no_model_provider_invocation_confirmed: bool = True
    no_tool_execution_confirmed: bool = True
    no_external_agent_execution_confirmed: bool = True
    no_claude_code_invocation_confirmed: bool = True
    no_codex_cli_invocation_confirmed: bool = True
    no_dominion_runtime_confirmed: bool = True
    no_persistent_trace_write_confirmed: bool = True
    no_external_trace_sink_confirmed: bool = True
    no_ui_runtime_confirmed: bool = True
    no_authority_grant_confirmed: bool = True
    no_d4_d9_grant_confirmed: bool = True
    no_production_certification_confirmed: bool = True
    unsafe_readiness_flags_false_confirmed: bool = True
    do_nothing_comparison_required_confirmed: bool = True
    human_review_required_confirmed: bool = True
    human_handoff_required_confirmed: bool = True
    evidence_bound_patch_metadata_confirmed: bool = True
    one_shot_loop_only_confirmed: bool = True
    cli_preview_only_confirmed: bool = True
    evidence_refs: list[str] = field(default_factory=list)
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
            "proposal_generation_checks",
            "safety_review_checks",
            "cli_surface_checks",
            "evidence_refs",
        ):
            _validate_list(name, getattr(self, name))
        _validate_dict("metadata", self.metadata)
        confirmations = {
            name: value
            for name, value in self.__dict__.items()
            if name.endswith("_confirmed") and isinstance(value, bool)
        }
        if not _all_bool_values_true(confirmations):
            raise ValueError("all audit confirmation booleans must be true for successful consolidation")


@dataclass(frozen=True)
class _RepairStageConsolidationRecordBase:
    record_id: str
    version: str
    stage_version: str
    completed_capabilities: list[str]
    blocked_capabilities: list[str]
    future_track_items: list[str]
    confirmation_booleans: dict[str, bool]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("record_id", self.record_id)
        _validate_version(self.version)
        _require_non_blank("stage_version", self.stage_version)
        _require_non_blank("summary", self.summary)
        for name in ("completed_capabilities", "blocked_capabilities", "future_track_items"):
            _validate_list(name, getattr(self, name))
        _validate_dict("confirmation_booleans", self.confirmation_booleans)
        _validate_dict("metadata", self.metadata)
        if not _all_bool_values_true(self.confirmation_booleans):
            raise ValueError("confirmation_booleans must all be true")


@dataclass(frozen=True)
class RepairEvidenceConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairSourceContextConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairScopePlanningConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairPatchMetadataConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairSafetyValidationConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairHumanReviewConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairLoopTrialConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class RepairCLISurfaceConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class DigestionDominionRepairConsolidationRecord(_RepairStageConsolidationRecordBase):
    pass


@dataclass(frozen=True)
class V039HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    human_approved_sandbox_apply_items: list[str]
    approval_artifact_validation_items: list[str]
    sandbox_patch_application_contract_items: list[str]
    no_live_apply_items: list[str]
    post_apply_test_items: list[str]
    before_after_comparison_items: list[str]
    cold_repair_evaluation_items: list[str]
    rollback_discard_items: list[str]
    reusable_boundary_items: list[str]
    reusable_evidence_items: list[str]
    reusable_source_context_items: list[str]
    reusable_scope_items: list[str]
    reusable_patch_metadata_items: list[str]
    reusable_safety_items: list[str]
    reusable_human_review_items: list[str]
    reusable_loop_trial_items: list[str]
    reusable_cli_items: list[str]
    required_new_boundaries: list[str]
    prohibited_until_later_gate: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    readiness_level: RepairProposalConsolidationReadinessLevel | str
    ready_for_v039: bool = True
    ready_for_execution: bool = False
    ready_for_human_approval_capture: bool = False
    ready_for_apply_permission: bool = False
    ready_for_sandbox_repair_apply: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_repair_execution: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_dominion_runtime: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in (
            "handoff_id",
            "source_version",
            "target_version_track",
            "source_snapshot_id",
            "recommended_next_track",
            "recommended_next_release",
        ):
            _require_non_blank(name, getattr(self, name))
        if V0389_VERSION not in self.source_version:
            raise ValueError("source_version must include v0.38.9")
        if "v0.39" not in self.target_version_track:
            raise ValueError("target_version_track must refer to v0.39")
        if V039_RECOMMENDED_TRACK not in self.recommended_next_track:
            raise ValueError("recommended_next_track must mention Human-approved Sandbox Repair Apply & Re-test Loop")
        for name in (
            "human_approved_sandbox_apply_items",
            "approval_artifact_validation_items",
            "sandbox_patch_application_contract_items",
            "no_live_apply_items",
            "post_apply_test_items",
            "before_after_comparison_items",
            "cold_repair_evaluation_items",
            "rollback_discard_items",
            "reusable_boundary_items",
            "reusable_evidence_items",
            "reusable_source_context_items",
            "reusable_scope_items",
            "reusable_patch_metadata_items",
            "reusable_safety_items",
            "reusable_human_review_items",
            "reusable_loop_trial_items",
            "reusable_cli_items",
            "required_new_boundaries",
            "prohibited_until_later_gate",
            "future_track_items",
            "evidence_refs",
        ):
            _validate_list(name, getattr(self, name))
        _require_subset("prohibited_until_later_gate", self.prohibited_until_later_gate, PROHIBITED_UNTIL_LATER_GATE)
        _validate_false(self, UNSAFE_HANDOFF_FLAG_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V038ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: RepairProposalConsolidationStatus | str
    readiness_level: RepairProposalConsolidationReadinessLevel | str
    summary: str
    completed_items: list[str]
    enabled_capabilities: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    runtime_not_ready_items: list[str]
    v039_handoff_summary: str
    ready_for_v039: bool
    ready_for_bounded_repair_proposal_loop_v1: bool
    ready_for_repair_proposal_boundary: bool
    ready_for_repair_evidence_contract: bool
    ready_for_read_only_sandbox_source_context: bool
    ready_for_repair_scope_planning: bool
    ready_for_proposed_diff_metadata: bool
    ready_for_proposed_code_hunk_metadata: bool
    ready_for_proposed_patch_envelope_metadata: bool
    ready_for_repair_proposal_safety_validation: bool
    ready_for_human_review_packet: bool
    ready_for_approval_request_contract: bool
    ready_for_one_shot_repair_proposal_loop_trial: bool
    ready_for_cli_repair_proposal_surface: bool
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_repair_execution: bool = False
    ready_for_sandbox_repair_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_human_approval_capture: bool = False
    ready_for_approval_grant: bool = False
    ready_for_apply_permission: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "release_name", "snapshot_id", "release_manifest_id", "summary", "v039_handoff_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in (
            "completed_items",
            "enabled_capabilities",
            "blocked_items",
            "future_track_items",
            "runtime_not_ready_items",
            "evidence_refs",
            "withdrawal_conditions",
        ):
            _validate_list(name, getattr(self, name))
        _validate_false(self, UNSAFE_REPORT_FLAG_NAMES)
        _validate_dict("metadata", self.metadata)


def build_repair_proposal_release_flags(**overrides: Any) -> RepairProposalReleaseFlagSet:
    return RepairProposalReleaseFlagSet(flag_set_id="v0389-release-flags", **overrides)


def build_repair_proposal_loop_snapshot(**overrides: Any) -> RepairProposalLoopSnapshot:
    flags = overrides.pop("release_flags", build_repair_proposal_release_flags())
    defaults = {
        "snapshot_id": "v0389-loop-snapshot",
        "version": V0389_VERSION,
        "release_name": FOUNDATION_RELEASE_NAME,
        "included_versions": list(INCLUDED_V038_VERSIONS),
        "included_modules": list(INCLUDED_MODULES),
        "included_artifact_groups": [
            "boundary",
            "evidence",
            "source_context",
            "scope_planning",
            "patch_metadata",
            "safety_validation",
            "human_review",
            "loop_trial",
            "cli_surface",
        ],
        "release_flags": flags,
        "consolidation_status": RepairProposalConsolidationStatus.CONSOLIDATED,
        "readiness_level": RepairProposalConsolidationReadinessLevel.BOUNDED_REPAIR_PROPOSAL_LOOP_V1_READY,
        "summary": "v0.38.9 consolidates bounded repair proposal metadata into Bounded Repair Proposal Loop v1.",
        "enabled_capabilities": list(ENABLED_CAPABILITIES),
        "prohibited_capabilities": list(PROHIBITED_CAPABILITIES),
        "evidence_refs": list(INCLUDED_DOCS),
        "known_gaps": [],
        "known_risks": ["future v0.39 apply handoff requires new human approval and sandbox-only gates"],
        "withdrawal_conditions": [
            "Withdraw consolidation readiness if any unsafe runtime readiness flag becomes true.",
            "Withdraw v0.39 handoff if blocking gaps are introduced.",
        ],
    }
    return RepairProposalLoopSnapshot(**_with_overrides(defaults, overrides))


def build_repair_proposal_capability_matrix(**overrides: Any) -> RepairProposalCapabilityMatrix:
    return RepairProposalCapabilityMatrix(
        capability_matrix_id="v0389-capability-matrix",
        version=V0389_VERSION,
        enabled_capabilities=list(ENABLED_CAPABILITIES),
        design_stage_capabilities=["v039_handoff_metadata", "human_approved_sandbox_apply_contract_input"],
        prohibited_capabilities=list(PROHIBITED_CAPABILITIES),
        future_track_capabilities=list(RECOMMENDED_V039_ITEMS) + list(FUTURE_TRACK_ITEMS),
        capability_to_version={capability: "v0.38.x" for capability in ENABLED_CAPABILITIES},
        prohibited_capability_to_reason={
            capability: "v0.38.9 consolidates metadata only and does not grant runtime authority"
            for capability in PROHIBITED_CAPABILITIES
        },
        evidence_refs=list(INCLUDED_DOCS),
        **overrides,
    )


def build_repair_proposal_stage_coverage(**overrides: Any) -> RepairProposalStageCoverage:
    return _build_coverage(RepairProposalStageCoverage, "v0389-stage-coverage", "v0.38.x", **overrides)


def build_repair_proposal_boundary_coverage(**overrides: Any) -> RepairProposalBoundaryCoverage:
    return _build_coverage(RepairProposalBoundaryCoverage, "v0389-boundary-coverage", "v0.38.0", **overrides)


def build_repair_proposal_evidence_coverage(**overrides: Any) -> RepairProposalEvidenceCoverage:
    return _build_coverage(RepairProposalEvidenceCoverage, "v0389-evidence-coverage", "v0.38.1", **overrides)


def build_repair_source_context_coverage(**overrides: Any) -> RepairSourceContextCoverage:
    return _build_coverage(RepairSourceContextCoverage, "v0389-source-context-coverage", "v0.38.2", **overrides)


def build_repair_scope_planning_coverage(**overrides: Any) -> RepairScopePlanningCoverage:
    return _build_coverage(RepairScopePlanningCoverage, "v0389-scope-planning-coverage", "v0.38.3", **overrides)


def build_repair_patch_metadata_coverage(**overrides: Any) -> RepairPatchMetadataCoverage:
    return _build_coverage(RepairPatchMetadataCoverage, "v0389-patch-metadata-coverage", "v0.38.4", **overrides)


def build_repair_safety_validation_coverage(**overrides: Any) -> RepairSafetyValidationCoverage:
    return _build_coverage(RepairSafetyValidationCoverage, "v0389-safety-validation-coverage", "v0.38.5", **overrides)


def build_repair_human_review_coverage(**overrides: Any) -> RepairHumanReviewCoverage:
    return _build_coverage(RepairHumanReviewCoverage, "v0389-human-review-coverage", "v0.38.6", **overrides)


def build_repair_loop_trial_coverage(**overrides: Any) -> RepairLoopTrialCoverage:
    return _build_coverage(RepairLoopTrialCoverage, "v0389-loop-trial-coverage", "v0.38.7", **overrides)


def build_repair_cli_surface_coverage(**overrides: Any) -> RepairCLISurfaceCoverage:
    return _build_coverage(RepairCLISurfaceCoverage, "v0389-cli-surface-coverage", "v0.38.8", **overrides)


def _build_coverage(coverage_cls: type[_RepairProposalCoverageBase], coverage_id: str, stage_version: str, **overrides: Any) -> _RepairProposalCoverageBase:
    defaults = {
        "coverage_id": coverage_id,
        "version": V0389_VERSION,
        "stage_version": stage_version,
        "covered_artifact_refs": [f"{stage_version}-metadata-artifacts"],
        "missing_artifact_refs": [],
        "covered_test_refs": [f"tests for {stage_version}"],
        "missing_test_refs": [],
        "covered_doc_refs": [f"docs for {stage_version}"],
        "missing_doc_refs": [],
        "coverage_notes": ["coverage is release-readiness metadata only"],
        "coverage_complete": True,
        "blocking_gaps": [],
        "non_blocking_gaps": [],
        "evidence_refs": [],
    }
    return coverage_cls(**_with_overrides(defaults, overrides))


def build_repair_proposal_boundary_register(**overrides: Any) -> RepairProposalBoundaryRegister:
    return RepairProposalBoundaryRegister(
        boundary_register_id="v0389-boundary-register",
        version=V0389_VERSION,
        inherited_boundaries=["v0.30-v0.38 gate inheritance"],
        active_bounded_boundaries=["bounded_metadata_only", "human_review_required", "do_nothing_comparison_required"],
        active_review_boundaries=["human_review_packet_metadata", "approval_request_contract_metadata"],
        prohibited_boundaries=list(REQUIRED_PROHIBITED_BOUNDARIES),
        future_gate_boundaries=["v039_sandbox_apply_boundary", "v039_controlled_retest_boundary"],
        evidence_refs=list(INCLUDED_DOCS),
        **overrides,
    )


def build_repair_proposal_risk_register(**overrides: Any) -> RepairProposalRiskRegister:
    return RepairProposalRiskRegister(
        risk_register_id="v0389-risk-register",
        version=V0389_VERSION,
        known_risks=["approval/apply confusion", "metadata/runtime confusion", "future handoff overclaim"],
        high_risk_surfaces=["patch application", "approval capture", "test execution", "external agent execution", "Dominion runtime"],
        prohibited_runtime_surfaces=list(REQUIRED_PROHIBITED_RUNTIME_SURFACES),
        mitigations=["unsafe readiness flags remain false", "v0.39 handoff is future-track metadata only"],
        unresolved_risks=["future sandbox apply design requires explicit human approval artifact validation"],
        evidence_refs=list(INCLUDED_DOCS),
        **overrides,
    )


def build_repair_proposal_gap_register(**overrides: Any) -> RepairProposalGapRegister:
    return RepairProposalGapRegister(
        gap_register_id="v0389-gap-register",
        version=V0389_VERSION,
        blocking_gaps=[],
        non_blocking_gaps=["production certification not claimed", "runtime apply not opened"],
        future_track_items=list(FUTURE_TRACK_ITEMS),
        recommended_v039_items=list(RECOMMENDED_V039_ITEMS),
        recommended_later_items=["live apply", "autonomous repair", "external coding agent orchestration", "Dominion runtime"],
        evidence_refs=list(INCLUDED_DOCS),
        **overrides,
    )


def build_repair_proposal_release_manifest(**overrides: Any) -> RepairProposalReleaseManifest:
    flags = overrides.pop("release_flags", build_repair_proposal_release_flags())
    return RepairProposalReleaseManifest(
        release_manifest_id="v0389-release-manifest",
        version=V0389_VERSION,
        release_name=FOUNDATION_RELEASE_NAME,
        snapshot_id="v0389-loop-snapshot",
        included_versions=list(INCLUDED_V038_VERSIONS),
        included_modules=list(INCLUDED_MODULES),
        included_docs=list(INCLUDED_DOCS),
        included_tests=list(INCLUDED_TESTS),
        focused_test_command="python -m pytest tests/test_v0389_bounded_repair_proposal_loop_consolidation.py",
        full_track_test_command="python -m pytest tests/test_v0380_repair_proposal_boundary.py tests/test_v0381_repair_proposal_evidence_contract.py tests/test_v0382_read_only_sandbox_source_context.py tests/test_v0383_repair_scope_planner_change_intent.py tests/test_v0384_proposed_diff_code_hunk_metadata.py tests/test_v0385_repair_proposal_safety_validation.py tests/test_v0386_human_review_packet_approval_request.py tests/test_v0387_bounded_repair_proposal_loop_trial.py tests/test_v0388_cli_repair_proposal_surface.py tests/test_v0389_bounded_repair_proposal_loop_consolidation.py",
        release_flags=flags,
        known_gaps=[],
        known_risks=["v0.39 apply handoff is metadata only"],
        next_handoff_id="v039-handoff-packet",
        **overrides,
    )


def build_repair_proposal_audit_trail(**overrides: Any) -> RepairProposalAuditTrail:
    return RepairProposalAuditTrail(
        audit_trail_id="v0389-audit-trail",
        version=V0389_VERSION,
        reviewed_artifact_refs=list(ENABLED_CAPABILITIES),
        reviewed_test_refs=list(INCLUDED_TESTS),
        reviewed_doc_refs=list(INCLUDED_DOCS),
        boundary_checks=["all unsafe runtime boundaries remain prohibited"],
        negative_runtime_checks=list(PROHIBITED_CAPABILITIES),
        proposal_generation_checks=["v0.38.4 remains proposed metadata only"],
        safety_review_checks=["v0.38.5 remains static metadata validation only"],
        cli_surface_checks=["v0.38.8 remains preview-only and not shell execution"],
        evidence_refs=list(INCLUDED_DOCS),
        **overrides,
    )


def _default_confirmation_booleans() -> dict[str, bool]:
    return {
        "no_runtime_permission_granted": True,
        "no_patch_application": True,
        "no_approval_capture": True,
        "no_test_execution": True,
        "no_model_or_external_agent": True,
        "no_dominion_runtime": True,
        "production_certification_false": True,
    }


def _build_stage_record(record_cls: type[_RepairStageConsolidationRecordBase], record_id: str, stage_version: str, completed: list[str], **overrides: Any) -> _RepairStageConsolidationRecordBase:
    defaults = {
        "record_id": record_id,
        "version": V0389_VERSION,
        "stage_version": stage_version,
        "completed_capabilities": completed,
        "blocked_capabilities": list(PROHIBITED_CAPABILITIES),
        "future_track_items": ["future v0.39 handoff metadata"],
        "confirmation_booleans": _default_confirmation_booleans(),
        "summary": f"{stage_version} consolidated as bounded repair proposal metadata only.",
    }
    return record_cls(**_with_overrides(defaults, overrides))


def build_repair_evidence_consolidation_record(**overrides: Any) -> RepairEvidenceConsolidationRecord:
    return _build_stage_record(RepairEvidenceConsolidationRecord, "v0389-evidence-record", "v0.38.1", ["evidence contract", "evidence bundle"], **overrides)


def build_repair_source_context_consolidation_record(**overrides: Any) -> RepairSourceContextConsolidationRecord:
    return _build_stage_record(RepairSourceContextConsolidationRecord, "v0389-source-context-record", "v0.38.2", ["read-only sandbox source context snapshot"], **overrides)


def build_repair_scope_planning_consolidation_record(**overrides: Any) -> RepairScopePlanningConsolidationRecord:
    return _build_stage_record(RepairScopePlanningConsolidationRecord, "v0389-scope-planning-record", "v0.38.3", ["scope plan", "change intent model"], **overrides)


def build_repair_patch_metadata_consolidation_record(**overrides: Any) -> RepairPatchMetadataConsolidationRecord:
    return _build_stage_record(RepairPatchMetadataConsolidationRecord, "v0389-patch-metadata-record", "v0.38.4", ["proposed diff metadata", "proposed code hunk metadata", "proposed patch envelope metadata"], **overrides)


def build_repair_safety_validation_consolidation_record(**overrides: Any) -> RepairSafetyValidationConsolidationRecord:
    return _build_stage_record(RepairSafetyValidationConsolidationRecord, "v0389-safety-record", "v0.38.5", ["repair proposal safety/static validation metadata"], **overrides)


def build_repair_human_review_consolidation_record(**overrides: Any) -> RepairHumanReviewConsolidationRecord:
    return _build_stage_record(RepairHumanReviewConsolidationRecord, "v0389-human-review-record", "v0.38.6", ["human review packet metadata", "approval request contract metadata"], **overrides)


def build_repair_loop_trial_consolidation_record(**overrides: Any) -> RepairLoopTrialConsolidationRecord:
    return _build_stage_record(RepairLoopTrialConsolidationRecord, "v0389-loop-trial-record", "v0.38.7", ["one-shot repair proposal loop packet metadata"], **overrides)


def build_repair_cli_surface_consolidation_record(**overrides: Any) -> RepairCLISurfaceConsolidationRecord:
    return _build_stage_record(RepairCLISurfaceConsolidationRecord, "v0389-cli-surface-record", "v0.38.8", ["safe CLI preview surface metadata"], **overrides)


def build_digestion_dominion_repair_consolidation_record(**overrides: Any) -> DigestionDominionRepairConsolidationRecord:
    return _build_stage_record(
        DigestionDominionRepairConsolidationRecord,
        "v0389-digestion-dominion-record",
        "v0.38.9",
        [
            "digestion_first_policy_applied",
            "dominion_runtime_blocked",
            "external_agent_execution_blocked",
            "v039_handoff_future_gated",
        ],
        **overrides,
    )


def build_v039_handoff_packet(**overrides: Any) -> V039HandoffPacket:
    return V039HandoffPacket(
        handoff_id="v039-handoff-packet",
        source_version=V0389_VERSION,
        target_version_track="v0.39",
        source_snapshot_id="v0389-loop-snapshot",
        release_manifest_id="v0389-release-manifest",
        recommended_next_track=V039_RECOMMENDED_TRACK,
        recommended_next_release="v0.39.0 Human-approved Sandbox Repair Apply Boundary Foundation",
        human_approved_sandbox_apply_items=["human-approved sandbox repair apply boundary", "explicit approval artifact intake"],
        approval_artifact_validation_items=["approval artifact validation", "approval authenticity validation", "approval expiration validation"],
        sandbox_patch_application_contract_items=["sandbox-only patch application contract", "no live workspace apply"],
        no_live_apply_items=["live apply remains prohibited", "live workspace write remains prohibited"],
        post_apply_test_items=["post-apply controlled re-test through v0.37 test runner boundaries"],
        before_after_comparison_items=["before/after result comparison"],
        cold_repair_evaluation_items=["cold repair improvement evaluation"],
        rollback_discard_items=["rollback metadata", "discard sandbox changes metadata"],
        reusable_boundary_items=["v0.38.0 repair proposal boundary"],
        reusable_evidence_items=["v0.38.1 evidence contract"],
        reusable_source_context_items=["v0.38.2 read-only source context snapshot metadata"],
        reusable_scope_items=["v0.38.3 scope plan and change intent"],
        reusable_patch_metadata_items=["v0.38.4 proposed patch envelope metadata"],
        reusable_safety_items=["v0.38.5 safety/static validation metadata"],
        reusable_human_review_items=["v0.38.6 human review packet and approval request contract"],
        reusable_loop_trial_items=["v0.38.7 one-shot loop packet metadata"],
        reusable_cli_items=["v0.38.8 CLI preview surface metadata"],
        required_new_boundaries=["human approval artifact validation", "sandbox-only apply contract", "controlled retest boundary"],
        prohibited_until_later_gate=list(PROHIBITED_UNTIL_LATER_GATE),
        future_track_items=list(FUTURE_TRACK_ITEMS),
        evidence_refs=list(INCLUDED_DOCS),
        readiness_level=RepairProposalConsolidationReadinessLevel.HANDOFF_READY_FOR_V039,
        **overrides,
    )


def build_v038_consolidation_report(**overrides: Any) -> V038ConsolidationReport:
    return V038ConsolidationReport(
        report_id="v0389-consolidation-report",
        version=V0389_VERSION,
        release_name=FOUNDATION_RELEASE_NAME,
        snapshot_id="v0389-loop-snapshot",
        release_manifest_id="v0389-release-manifest",
        handoff_id="v039-handoff-packet",
        consolidation_status=RepairProposalConsolidationStatus.CONSOLIDATED,
        readiness_level=RepairProposalConsolidationReadinessLevel.BOUNDED_REPAIR_PROPOSAL_LOOP_V1_READY,
        summary="v0.38.9 consolidates Bounded Repair Proposal Loop v1 as metadata foundation only.",
        completed_items=list(ENABLED_CAPABILITIES),
        enabled_capabilities=list(ENABLED_CAPABILITIES),
        blocked_items=list(PROHIBITED_CAPABILITIES),
        future_track_items=list(RECOMMENDED_V039_ITEMS) + list(FUTURE_TRACK_ITEMS),
        runtime_not_ready_items=list(PROHIBITED_CAPABILITIES),
        v039_handoff_summary=f"v0.39 should begin {V039_RECOMMENDED_TRACK} as future-track metadata.",
        ready_for_v039=True,
        ready_for_bounded_repair_proposal_loop_v1=True,
        ready_for_repair_proposal_boundary=True,
        ready_for_repair_evidence_contract=True,
        ready_for_read_only_sandbox_source_context=True,
        ready_for_repair_scope_planning=True,
        ready_for_proposed_diff_metadata=True,
        ready_for_proposed_code_hunk_metadata=True,
        ready_for_proposed_patch_envelope_metadata=True,
        ready_for_repair_proposal_safety_validation=True,
        ready_for_human_review_packet=True,
        ready_for_approval_request_contract=True,
        ready_for_one_shot_repair_proposal_loop_trial=True,
        ready_for_cli_repair_proposal_surface=True,
        evidence_refs=list(INCLUDED_DOCS),
        withdrawal_conditions=[
            "Withdraw if any unsafe readiness flag becomes true.",
            "Withdraw if v0.39 handoff is treated as apply permission.",
        ],
        **overrides,
    )


def repair_proposal_release_flags_preserve_no_runtime(flags: RepairProposalReleaseFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_RELEASE_FLAG_NAMES)


def repair_proposal_snapshot_is_not_runtime(snapshot: RepairProposalLoopSnapshot) -> bool:
    return repair_proposal_release_flags_preserve_no_runtime(snapshot.release_flags) and "repair_execution" in snapshot.prohibited_capabilities


def repair_proposal_capability_matrix_is_not_permission_grant(matrix: RepairProposalCapabilityMatrix) -> bool:
    return all(capability in matrix.prohibited_capabilities for capability in PROHIBITED_CAPABILITIES)


def repair_proposal_audit_confirms_no_runtime(audit: RepairProposalAuditTrail) -> bool:
    confirmations = {
        name: value
        for name, value in audit.__dict__.items()
        if name.endswith("_confirmed") and isinstance(value, bool)
    }
    return _all_bool_values_true(confirmations)


def repair_stage_consolidation_record_is_not_runtime(record: _RepairStageConsolidationRecordBase) -> bool:
    return _all_bool_values_true(record.confirmation_booleans)


def v039_handoff_packet_is_future_track_only(packet: V039HandoffPacket) -> bool:
    return packet.ready_for_v039 and all(getattr(packet, name) is False for name in UNSAFE_HANDOFF_FLAG_NAMES)


def v038_consolidation_report_is_not_execution_ready(report: V038ConsolidationReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_REPORT_FLAG_NAMES)
