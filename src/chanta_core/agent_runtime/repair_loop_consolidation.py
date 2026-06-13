"""v0.39.9 repair loop consolidation metadata.

This module consolidates v0.39.0 through v0.39.8 as report and handoff
metadata only. It does not execute sandbox apply, re-tests, comparisons,
process-state reconstruction, prompts, models, subagents, external agents,
commands, trace persistence, Dominion runtime, or production certification.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank


V0399_VERSION = "v0.39.9"
V0399_RELEASE_NAME = "v0.39.9 Human-approved Sandbox Repair Apply & Self-Prompting Loop Consolidation"
V039_FOUNDATION_RELEASE_NAME = "Human-approved Sandbox Repair Apply & Re-test Loop v1 with PI-native Self-Prompting Mission Loop Boundary"
V040_TARGET_TRACK = "Controlled Multi-Iteration Mission Loop & Subagent Verification Boundary"
V040_NEXT_RELEASE = "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation"


class RepairLoopConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_WARNINGS = "consolidated_with_warnings"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    HANDOFF_READY_FOR_V040 = "handoff_ready_for_v040"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RepairLoopConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_FOUNDATION_READY = "boundary_foundation_ready"
    APPROVAL_WORKSPACE_APPLY_READY = "approval_workspace_apply_ready"
    RETEST_COMPARISON_READY = "retest_comparison_ready"
    PROCESS_STATE_SELF_PROMPTING_READY = "process_state_self_prompting_ready"
    CLI_SURFACE_READY = "cli_surface_ready"
    HUMAN_APPROVED_SANDBOX_REPAIR_APPLY_LOOP_V1_READY = "human_approved_sandbox_repair_apply_loop_v1_ready"
    DESIGN_HANDOFF_READY_FOR_V040 = "design_handoff_ready_for_v040"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairLoopConsolidationSourceKind(StrEnum):
    V0398_CLI_LOOP_SURFACE_REPORT = "v0398_cli_loop_surface_report"
    V0398_LOOP_BUNDLE_VIEW = "v0398_loop_bundle_view"
    V0398_HANDOFF_PACKET = "v0398_handoff_packet"
    V0397_SELF_PROMPTING_REPORT = "v0397_self_prompting_report"
    V0397_DRAFT_PACKET = "v0397_draft_packet"
    V0396_PROCESS_STATE_RECONSTRUCTION_REPORT = "v0396_process_state_reconstruction_report"
    V0395_OUTCOME_COMPARISON_REPORT = "v0395_outcome_comparison_report"
    V0394_POST_APPLY_RETEST_RESULT = "v0394_post_apply_retest_result"
    V0393_SANDBOX_APPLY_RESULT = "v0393_sandbox_apply_result"
    V0392_WORKSPACE_ISOLATION_DECISION = "v0392_workspace_isolation_decision"
    V0391_APPROVAL_ARTIFACT_DECISION = "v0391_approval_artifact_decision"
    V0390_APPLY_BOUNDARY_REPORT = "v0390_apply_boundary_report"
    V0389_REPAIR_PROPOSAL_CONSOLIDATION_REPORT = "v0389_repair_proposal_consolidation_report"
    LOOP_ENGINEERING_PI_NATIVE_NOTE = "loop_engineering_pi_native_note"
    MANUAL_OPERATOR_NOTE = "manual_operator_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


V039_INCLUDED_VERSIONS = [
    "v0.39.0",
    "v0.39.1",
    "v0.39.2",
    "v0.39.3",
    "v0.39.4",
    "v0.39.5",
    "v0.39.6",
    "v0.39.7",
    "v0.39.8",
]

V039_STAGE_NAMES = {
    "v0.39.0": "Human-approved Sandbox Repair Apply Boundary + PI-native Self-Prompting Mission Loop Boundary",
    "v0.39.1": "Approval Artifact Intake & Authenticity Gate",
    "v0.39.2": "Sandbox Repair Workspace Isolation Contract",
    "v0.39.3": "Human-approved Patch Materialization & Sandbox Apply",
    "v0.39.4": "Post-Apply Controlled Re-test",
    "v0.39.5": "Before / After Repair Outcome Comparison",
    "v0.39.6": "PI-native Repair Process-State Reconstruction",
    "v0.39.7": "Self-Prompting Next-Action Draft & Subagent Prompt Contract",
    "v0.39.8": "CLI Sandbox Repair Apply / Re-test / Loop-State Surface",
}

UNSAFE_FLAG_NAMES = [
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_live_workspace_apply",
    "ready_for_live_workspace_write",
    "ready_for_approval_less_apply",
    "ready_for_unbounded_workspace_mutation",
    "ready_for_patch_file_export",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_arbitrary_test_execution",
    "ready_for_arbitrary_command_execution",
    "ready_for_shell_execution",
    "ready_for_raw_subprocess_execution",
    "ready_for_dependency_install",
    "ready_for_network_access",
    "ready_for_prompt_submission_to_model",
    "ready_for_model_provider_invocation",
    "ready_for_self_prompt_execution",
    "ready_for_next_action_execution",
    "ready_for_subagent_invocation",
    "ready_for_external_agent_execution",
    "ready_for_claude_code_invocation",
    "ready_for_codex_cli_invocation",
    "ready_for_opencode_invocation",
    "ready_for_hermes_invocation",
    "ready_for_openclaw_invocation",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_repair_execution",
    "ready_for_ocel_file_write",
    "ready_for_jsonl_trace_write",
    "ready_for_ocpx_state_persistence",
    "ready_for_pig_recommendation_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_dominion_runtime",
    "ready_for_d4_d9_authority_grant",
    "production_certified",
]

AUDIT_TRUE_NAMES = [
    "no_live_apply_confirmed",
    "no_approval_less_apply_confirmed",
    "bounded_sandbox_apply_only_confirmed",
    "controlled_retest_only_confirmed",
    "no_arbitrary_test_execution_confirmed",
    "no_arbitrary_command_confirmed",
    "no_shell_confirmed",
    "no_raw_subprocess_confirmed",
    "no_prompt_submission_confirmed",
    "no_model_invocation_confirmed",
    "no_prompt_execution_confirmed",
    "no_next_action_execution_confirmed",
    "no_subagent_invocation_confirmed",
    "no_external_agent_confirmed",
    "no_autonomous_loop_confirmed",
    "no_retry_loop_confirmed",
    "no_multi_cycle_loop_confirmed",
    "no_automatic_repair_confirmed",
    "no_dominion_runtime_confirmed",
    "no_ocel_file_write_confirmed",
    "no_ocpx_persistence_confirmed",
    "no_pig_execution_confirmed",
    "no_persistent_trace_write_confirmed",
    "no_production_certification_confirmed",
    "human_handoff_required_confirmed",
    "loop_engineering_absorbed_as_pi_native_confirmed",
    "unsafe_readiness_flags_false_confirmed",
]


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    values = defaults.copy()
    values.update(overrides)
    return values


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0399_VERSION not in version:
        raise ValueError("version must include v0.39.9")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_dict(name: str, value: Any) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be a dict")


def _validate_false(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must remain False in v0.39.9")


def _validate_true(instance: object, names: list[str]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True")


def _require_versions(name: str, versions: list[str]) -> None:
    _validate_list(name, versions)
    missing = [version for version in V039_INCLUDED_VERSIONS if version not in versions]
    if missing:
        raise ValueError(f"{name} must include {', '.join(missing)}")


@dataclass(frozen=True)
class RepairLoopConsolidationFlagSet:
    flag_set_id: str
    version: str
    v039_loop_consolidation_layer_constructed: bool = True
    human_approved_sandbox_repair_apply_loop_v1_ready: bool = True
    ready_for_v040_handoff: bool = True
    ready_for_v040_controlled_multi_iteration_loop_boundary_input: bool = True
    ready_for_v040_subagent_verification_boundary_input: bool = True
    ready_for_v040_model_provider_boundary_input: bool = True
    ready_for_v0390_apply_boundary: bool = True
    ready_for_v0391_approval_artifact_gate: bool = True
    ready_for_v0392_workspace_isolation_contract: bool = True
    ready_for_v0393_bounded_sandbox_patch_materialization: bool = True
    ready_for_v0393_bounded_sandbox_apply: bool = True
    ready_for_v0394_controlled_post_apply_retest: bool = True
    ready_for_v0395_before_after_comparison: bool = True
    ready_for_v0396_process_state_reconstruction_metadata: bool = True
    ready_for_v0397_self_prompting_draft_contract: bool = True
    ready_for_v0398_cli_loop_state_surface: bool = True
    ready_for_bounded_sandbox_target_read: bool = True
    ready_for_bounded_sandbox_target_write: bool = True
    ready_for_controlled_runner_retest_boundary: bool = True
    ready_for_process_state_driven_next_action_draft: bool = True
    ready_for_agent_to_subagent_prompt_draft: bool = True
    ready_for_human_handoff_prompt: bool = True
    ready_for_cli_preview_surface: bool = True
    ready_for_execution: bool = False
    ready_for_general_execution: bool = False
    ready_for_live_workspace_apply: bool = False
    ready_for_live_workspace_write: bool = False
    ready_for_approval_less_apply: bool = False
    ready_for_unbounded_workspace_mutation: bool = False
    ready_for_patch_file_export: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_arbitrary_test_execution: bool = False
    ready_for_arbitrary_command_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_raw_subprocess_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_network_access: bool = False
    ready_for_prompt_submission_to_model: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_self_prompt_execution: bool = False
    ready_for_next_action_execution: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_opencode_invocation: bool = False
    ready_for_hermes_invocation: bool = False
    ready_for_openclaw_invocation: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_automatic_repair: bool = False
    ready_for_retry_loop: bool = False
    ready_for_multi_cycle_loop: bool = False
    ready_for_repair_execution: bool = False
    ready_for_ocel_file_write: bool = False
    ready_for_jsonl_trace_write: bool = False
    ready_for_ocpx_state_persistence: bool = False
    ready_for_pig_recommendation_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_d4_d9_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopConsolidationSourceRef:
    source_ref_id: str
    source_kind: RepairLoopConsolidationSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopTrackSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_docs: list[str]
    included_tests: list[str]
    release_flags: RepairLoopConsolidationFlagSet
    consolidation_status: RepairLoopConsolidationStatus | str
    readiness_level: RepairLoopConsolidationReadinessLevel | str
    snapshot_summary: str
    enabled_bounded_capabilities: list[str]
    blocked_capabilities: list[str]
    future_track_capabilities: list[str]
    known_gaps: list[str]
    known_risks: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["snapshot_id", "version", "release_name", "snapshot_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _require_versions("included_versions", self.included_versions)
        for name in [
            "included_modules",
            "included_docs",
            "included_tests",
            "enabled_bounded_capabilities",
            "blocked_capabilities",
            "future_track_capabilities",
            "known_gaps",
            "known_risks",
            "evidence_refs",
        ]:
            _validate_list(name, getattr(self, name))
        if not repair_loop_consolidation_flags_preserve_no_unsafe_runtime(self.release_flags):
            raise ValueError("release_flags must preserve unsafe runtime false")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_bounded_capabilities: list[str]
    preview_only_capabilities: list[str]
    metadata_only_capabilities: list[str]
    blocked_capabilities: list[str]
    future_track_capabilities: list[str]
    capability_to_stage: dict[str, str]
    blocked_capability_to_reason: dict[str, str]
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("capability_matrix_id", self.capability_matrix_id)
        _validate_version(self.version)
        for name in [
            "enabled_bounded_capabilities",
            "preview_only_capabilities",
            "metadata_only_capabilities",
            "blocked_capabilities",
            "future_track_capabilities",
            "evidence_refs",
        ]:
            _validate_list(name, getattr(self, name))
        _validate_dict("capability_to_stage", self.capability_to_stage)
        _validate_dict("blocked_capability_to_reason", self.blocked_capability_to_reason)
        required_blocked = ["live apply", "prompt execution", "subagent invocation", "model invocation", "external agent", "autonomous loop", "Dominion", "production certification"]
        for item in required_blocked:
            if not any(item.lower() in cap.lower() for cap in self.blocked_capabilities):
                raise ValueError(f"blocked_capabilities must include {item}")
        if not any("CLI" in cap and "preview" in cap for cap in self.preview_only_capabilities):
            raise ValueError("preview_only_capabilities must include v0.39.8 CLI surface")
        if not any("process-state" in cap.lower() for cap in self.metadata_only_capabilities):
            raise ValueError("metadata_only_capabilities must include process-state reconstruction")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopStageCoverage:
    coverage_id: str
    version: str
    stage_version: str
    stage_name: str
    covered_artifact_refs: list[str]
    covered_test_refs: list[str]
    covered_doc_refs: list[str]
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    coverage_notes: list[str]
    coverage_complete: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["coverage_id", "version", "stage_version", "stage_name"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["covered_artifact_refs", "covered_test_refs", "covered_doc_refs", "blocking_gaps", "non_blocking_gaps", "coverage_notes", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        if self.blocking_gaps and self.coverage_complete:
            raise ValueError("coverage_complete must be False when blocking_gaps is non-empty")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str]
    v039_opened_boundaries: list[str]
    active_bounded_runtime_boundaries: list[str]
    preview_only_boundaries: list[str]
    metadata_only_boundaries: list[str]
    prohibited_boundaries: list[str]
    future_gate_boundaries: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version(self.version)
        for name in [
            "inherited_boundaries",
            "v039_opened_boundaries",
            "active_bounded_runtime_boundaries",
            "preview_only_boundaries",
            "metadata_only_boundaries",
            "prohibited_boundaries",
            "future_gate_boundaries",
            "evidence_refs",
        ]:
            _validate_list(name, getattr(self, name))
        required = ["live apply", "approval-less apply", "prompt execution", "model invocation", "subagent invocation", "external agent", "shell/subprocess", "arbitrary command", "autonomous loop", "retry loop", "multi-cycle loop", "Dominion", "production certification"]
        for item in required:
            if not any(item.lower() in boundary.lower() for boundary in self.prohibited_boundaries):
                raise ValueError(f"prohibited_boundaries must include {item}")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopRiskRegister:
    risk_register_id: str
    version: str
    known_risks: list[str]
    high_risk_surfaces: list[str]
    mitigations: list[str]
    unresolved_risks: list[str]
    future_watch_items: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_register_id", self.risk_register_id)
        _validate_version(self.version)
        for name in ["known_risks", "high_risk_surfaces", "mitigations", "unresolved_risks", "future_watch_items", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        required = ["approval confusion", "sandbox/live confusion", "prompt execution confusion", "subagent invocation confusion", "autonomous loop risk", "production certification confusion", "cognitive surrender", "token cost loop explosion", "Dominion/runtime authority risk"]
        for item in required:
            if not any(item.lower() in risk.lower() for risk in self.known_risks):
                raise ValueError(f"known_risks must include {item}")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    future_track_items: list[str]
    recommended_v040_items: list[str]
    recommended_later_items: list[str]
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version(self.version)
        for name in ["blocking_gaps", "non_blocking_gaps", "future_track_items", "recommended_v040_items", "recommended_later_items", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        required = ["controlled multi-iteration boundary", "verifier subagent boundary", "model/provider boundary", "loop budget gate", "stop-condition contract", "human checkpoint gate"]
        for item in required:
            if not any(item.lower() in gap.lower() for gap in self.recommended_v040_items):
                raise ValueError(f"recommended_v040_items must include {item}")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopReleaseManifest:
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
    release_flags: RepairLoopConsolidationFlagSet
    known_gaps: list[str]
    known_risks: list[str]
    next_handoff_id: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["release_manifest_id", "version", "release_name", "snapshot_id", "focused_test_command", "full_track_test_command"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _require_versions("included_versions", self.included_versions)
        for name in ["included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"]:
            _validate_list(name, getattr(self, name))
        if not repair_loop_consolidation_flags_preserve_no_unsafe_runtime(self.release_flags):
            raise ValueError("release_flags must preserve unsafe runtime false")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str]
    reviewed_test_refs: list[str]
    reviewed_doc_refs: list[str]
    boundary_checks: list[str]
    runtime_checks: list[str]
    loop_safety_checks: list[str]
    no_live_apply_confirmed: bool
    no_approval_less_apply_confirmed: bool
    bounded_sandbox_apply_only_confirmed: bool
    controlled_retest_only_confirmed: bool
    no_arbitrary_test_execution_confirmed: bool
    no_arbitrary_command_confirmed: bool
    no_shell_confirmed: bool
    no_raw_subprocess_confirmed: bool
    no_prompt_submission_confirmed: bool
    no_model_invocation_confirmed: bool
    no_prompt_execution_confirmed: bool
    no_next_action_execution_confirmed: bool
    no_subagent_invocation_confirmed: bool
    no_external_agent_confirmed: bool
    no_autonomous_loop_confirmed: bool
    no_retry_loop_confirmed: bool
    no_multi_cycle_loop_confirmed: bool
    no_automatic_repair_confirmed: bool
    no_dominion_runtime_confirmed: bool
    no_ocel_file_write_confirmed: bool
    no_ocpx_persistence_confirmed: bool
    no_pig_execution_confirmed: bool
    no_persistent_trace_write_confirmed: bool
    no_production_certification_confirmed: bool
    human_handoff_required_confirmed: bool
    loop_engineering_absorbed_as_pi_native_confirmed: bool
    unsafe_readiness_flags_false_confirmed: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _validate_version(self.version)
        for name in ["reviewed_artifact_refs", "reviewed_test_refs", "reviewed_doc_refs", "boundary_checks", "runtime_checks", "loop_safety_checks", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_true(self, AUDIT_TRUE_NAMES)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopStageConsolidationRecord:
    record_id: str
    version: str
    stage_version: str
    stage_name: str
    completed_capabilities: list[str]
    blocked_capabilities: list[str]
    future_track_items: list[str]
    confirmation_booleans: dict[str, bool]
    summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["record_id", "version", "stage_version", "stage_name", "summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ["completed_capabilities", "blocked_capabilities", "future_track_items", "evidence_refs"]:
            _validate_list(name, getattr(self, name))
        _validate_dict("confirmation_booleans", self.confirmation_booleans)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class LoopEngineeringPINativeConsolidationRecord:
    record_id: str
    version: str
    external_term: str
    adopted_as_top_level_concept: bool
    pi_native_terms: list[str]
    absorbed_patterns: list[str]
    rejected_patterns: list[str]
    safety_interpretation: str
    human_handoff_required: bool
    autonomous_loop_opened: bool
    subagent_invocation_opened: bool
    prompt_execution_opened: bool
    model_invocation_opened: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["record_id", "version", "external_term", "safety_interpretation"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.external_term != "Loop Engineering":
            raise ValueError("external_term should be Loop Engineering")
        if self.adopted_as_top_level_concept is not False:
            raise ValueError("Loop Engineering must not be adopted as top-level ChantaCore concept")
        _validate_list("pi_native_terms", self.pi_native_terms)
        _validate_list("absorbed_patterns", self.absorbed_patterns)
        _validate_list("rejected_patterns", self.rejected_patterns)
        if "Self-Prompting Mission Loop" not in self.pi_native_terms or "Process-State-Driven Self-Prompting" not in self.pi_native_terms:
            raise ValueError("pi_native_terms must include Self-Prompting Mission Loop and Process-State-Driven Self-Prompting")
        _validate_true(self, ["human_handoff_required"])
        _validate_false(self, ["autonomous_loop_opened", "subagent_invocation_opened", "prompt_execution_opened", "model_invocation_opened"])
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V040HandoffPacket:
    handoff_id: str
    version: str
    source_track: str
    target_track: str
    recommended_next_release: str
    handoff_summary: str
    reusable_v039_capabilities: list[str]
    required_new_boundaries: list[str]
    proposed_v040_stage_plan: list[str]
    prohibited_until_future_gate: list[str]
    required_human_gates: list[str]
    required_loop_safety_gates: list[str]
    required_budget_gates: list[str]
    required_subagent_gates: list[str]
    required_model_provider_gates: list[str]
    ready_for_v040_design_handoff: bool
    ready_for_v040_execution: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_prompt_execution: bool = False
    ready_for_live_apply: bool = False
    ready_for_dominion_runtime: bool = False
    production_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["handoff_id", "version", "source_track", "target_track", "recommended_next_release", "handoff_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if V040_TARGET_TRACK not in self.target_track:
            raise ValueError("target_track should mention Controlled Multi-Iteration Mission Loop & Subagent Verification Boundary")
        for name in [
            "reusable_v039_capabilities",
            "required_new_boundaries",
            "proposed_v040_stage_plan",
            "prohibited_until_future_gate",
            "required_human_gates",
            "required_loop_safety_gates",
            "required_budget_gates",
            "required_subagent_gates",
            "required_model_provider_gates",
            "evidence_refs",
        ]:
            _validate_list(name, getattr(self, name))
        _validate_false(
            self,
            [
                "ready_for_v040_execution",
                "ready_for_autonomous_loop_runtime",
                "ready_for_subagent_invocation",
                "ready_for_model_provider_invocation",
                "ready_for_prompt_execution",
                "ready_for_live_apply",
                "ready_for_dominion_runtime",
                "production_certified",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class V039ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot: RepairLoopTrackSnapshot
    capability_matrix: RepairLoopCapabilityMatrix
    stage_coverages: list[RepairLoopStageCoverage]
    boundary_register: RepairLoopBoundaryRegister
    risk_register: RepairLoopRiskRegister
    gap_register: RepairLoopGapRegister
    release_manifest: RepairLoopReleaseManifest
    audit_trail: RepairLoopAuditTrail
    stage_records: list[RepairLoopStageConsolidationRecord]
    loop_engineering_record: LoopEngineeringPINativeConsolidationRecord
    v040_handoff_packet: V040HandoffPacket
    consolidation_status: RepairLoopConsolidationStatus | str
    readiness_level: RepairLoopConsolidationReadinessLevel | str
    report_summary: str
    ready_for_v040_handoff: bool
    human_approved_sandbox_repair_apply_loop_v1_ready: bool
    production_certified: bool = False
    ready_for_execution: bool = False
    ready_for_live_apply: bool = False
    ready_for_prompt_execution: bool = False
    ready_for_subagent_invocation: bool = False
    ready_for_model_provider_invocation: bool = False
    ready_for_autonomous_loop_runtime: bool = False
    ready_for_dominion_runtime: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ["report_id", "version", "release_name", "report_summary"]:
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("stage_coverages", self.stage_coverages)
        _validate_list("stage_records", self.stage_records)
        _validate_list("evidence_refs", self.evidence_refs)
        _validate_false(
            self,
            [
                "production_certified",
                "ready_for_execution",
                "ready_for_live_apply",
                "ready_for_prompt_execution",
                "ready_for_subagent_invocation",
                "ready_for_model_provider_invocation",
                "ready_for_autonomous_loop_runtime",
                "ready_for_dominion_runtime",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopConsolidationValidationFinding:
    finding_id: str
    finding_summary: str
    blocked: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        _require_non_blank("finding_summary", self.finding_summary)
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopConsolidationValidationReport:
    validation_report_id: str
    version: str
    validation_summary: str
    findings: list[RepairLoopConsolidationValidationFinding]
    consolidation_only_confirmed: bool
    no_new_runtime_expansion_confirmed: bool
    no_runtime_execution_confirmed: bool
    no_production_certification_confirmed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        _require_non_blank("validation_summary", self.validation_summary)
        _validate_list("findings", self.findings)
        _validate_true(
            self,
            [
                "consolidation_only_confirmed",
                "no_new_runtime_expansion_confirmed",
                "no_runtime_execution_confirmed",
                "no_production_certification_confirmed",
            ],
        )
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopConsolidationRunPreview:
    preview_id: str
    version: str
    preview_summary: str
    planned_consolidation_steps: list[str]
    consolidation_only: bool = True
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("preview_id", self.preview_id)
        _validate_version(self.version)
        _require_non_blank("preview_summary", self.preview_summary)
        _validate_list("planned_consolidation_steps", self.planned_consolidation_steps)
        if self.consolidation_only is not True or self.ready_for_execution is not False:
            raise ValueError("run preview must remain consolidation-only")
        _validate_dict("metadata", self.metadata)


@dataclass(frozen=True)
class RepairLoopNoUnsafeExpansionGuarantee:
    guarantee_id: str
    version: str
    guarantee_summary: str
    no_runtime_execution: bool = True
    no_live_apply: bool = True
    no_approval_less_apply: bool = True
    no_arbitrary_command: bool = True
    no_shell: bool = True
    no_raw_subprocess: bool = True
    no_prompt_submission: bool = True
    no_model_invocation: bool = True
    no_prompt_execution: bool = True
    no_next_action_execution: bool = True
    no_subagent_invocation: bool = True
    no_external_agent: bool = True
    no_autonomous_loop: bool = True
    no_retry_loop: bool = True
    no_multi_cycle_loop: bool = True
    no_automatic_repair: bool = True
    no_dominion_runtime: bool = True
    no_ocel_file_write: bool = True
    no_ocpx_persistence: bool = True
    no_persistent_trace_write: bool = True
    no_production_certification: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        _require_non_blank("guarantee_summary", self.guarantee_summary)
        _validate_true(
            self,
            [
                "no_runtime_execution",
                "no_live_apply",
                "no_approval_less_apply",
                "no_arbitrary_command",
                "no_shell",
                "no_raw_subprocess",
                "no_prompt_submission",
                "no_model_invocation",
                "no_prompt_execution",
                "no_next_action_execution",
                "no_subagent_invocation",
                "no_external_agent",
                "no_autonomous_loop",
                "no_retry_loop",
                "no_multi_cycle_loop",
                "no_automatic_repair",
                "no_dominion_runtime",
                "no_ocel_file_write",
                "no_ocpx_persistence",
                "no_persistent_trace_write",
                "no_production_certification",
            ],
        )
        _validate_dict("metadata", self.metadata)


def default_v039_included_versions() -> list[str]:
    return V039_INCLUDED_VERSIONS.copy()


def default_v039_stage_plan() -> list[dict[str, str]]:
    return [{"stage_version": version, "stage_name": V039_STAGE_NAMES[version]} for version in V039_INCLUDED_VERSIONS]


def default_v040_handoff_plan() -> list[str]:
    return [
        "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation",
        "max-iteration policy",
        "loop stop-condition contract",
        "verifier subagent boundary metadata",
        "model/provider boundary gate",
        "loop budget / token budget gate",
        "human checkpoint gate",
        "no autonomous infinite loop",
        "no production certification",
    ]


def _included_modules() -> list[str]:
    return [
        "repair_apply_boundary.py",
        "repair_approval_artifact.py",
        "repair_workspace_isolation.py",
        "repair_sandbox_apply.py",
        "repair_post_apply_retest.py",
        "repair_outcome_comparison.py",
        "repair_process_state_reconstruction.py",
        "repair_self_prompting.py",
        "repair_loop_state_cli_surface.py",
        "repair_loop_consolidation.py",
    ]


def _included_docs() -> list[str]:
    return [f"docs/versions/v0.39/v{version[1:]}_stage.md" for version in V039_INCLUDED_VERSIONS]


def _included_tests() -> list[str]:
    return [
        "tests/test_v0390_human_approved_sandbox_repair_apply_boundary.py",
        "tests/test_v0391_approval_artifact_intake_authenticity_gate.py",
        "tests/test_v0392_sandbox_repair_workspace_isolation.py",
        "tests/test_v0393_human_approved_patch_materialization_sandbox_apply.py",
        "tests/test_v0394_post_apply_controlled_retest.py",
        "tests/test_v0395_before_after_repair_outcome_comparison.py",
        "tests/test_v0396_pi_native_repair_process_state_reconstruction.py",
        "tests/test_v0397_self_prompting_next_action_draft_subagent_prompt_contract.py",
        "tests/test_v0398_cli_sandbox_repair_apply_retest_loop_state_surface.py",
        "tests/test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
    ]


def _enabled_bounded_capabilities() -> list[str]:
    return [
        "human-approved sandbox apply boundary",
        "approval artifact gate",
        "sandbox workspace isolation contract",
        "bounded sandbox patch materialization",
        "bounded sandbox-only text replacement apply",
        "sandbox apply transaction/result/audit",
        "controlled post-apply re-test through v0.37 runner boundary",
        "bounded test output capture",
    ]


def _metadata_capabilities() -> list[str]:
    return [
        "before/after repair outcome comparison metadata",
        "repair effectiveness assessment metadata",
        "PI-native process-state reconstruction metadata",
        "OCEL-style event envelope metadata",
        "OCPX-style process-state projection metadata",
        "PIG diagnostic input metadata",
        "self-prompting next-action draft metadata",
        "agent-to-subagent prompt draft metadata",
        "human handoff prompt metadata",
    ]


def _blocked_capabilities() -> list[str]:
    return [
        "live apply",
        "approval-less apply",
        "prompt execution",
        "model invocation",
        "subagent invocation",
        "external agent execution",
        "autonomous loop runtime",
        "retry loop",
        "multi-cycle loop",
        "automatic repair",
        "Dominion runtime",
        "production certification",
    ]


def build_repair_loop_consolidation_flags(**overrides: Any) -> RepairLoopConsolidationFlagSet:
    return RepairLoopConsolidationFlagSet(**_with_overrides({"flag_set_id": "v0399-consolidation-flags", "version": V0399_VERSION}, overrides))


def build_repair_loop_consolidation_source_ref(**overrides: Any) -> RepairLoopConsolidationSourceRef:
    defaults = {
        "source_ref_id": "v0399-source-ref",
        "source_kind": RepairLoopConsolidationSourceKind.V0398_CLI_LOOP_SURFACE_REPORT,
        "source_id": "v0398-cli-surface-report",
        "source_summary": "v0.39.8 CLI preview surface metadata for consolidation.",
        "evidence_refs": ["v0398-cli-surface-report"],
    }
    return RepairLoopConsolidationSourceRef(**_with_overrides(defaults, overrides))


def build_repair_loop_track_snapshot(**overrides: Any) -> RepairLoopTrackSnapshot:
    flags = overrides.pop("release_flags", build_repair_loop_consolidation_flags())
    defaults = {
        "snapshot_id": "v0399-track-snapshot",
        "version": V0399_VERSION,
        "release_name": V039_FOUNDATION_RELEASE_NAME,
        "included_versions": default_v039_included_versions(),
        "included_modules": _included_modules(),
        "included_docs": _included_docs(),
        "included_tests": _included_tests(),
        "release_flags": flags,
        "consolidation_status": RepairLoopConsolidationStatus.HANDOFF_READY_FOR_V040,
        "readiness_level": RepairLoopConsolidationReadinessLevel.HUMAN_APPROVED_SANDBOX_REPAIR_APPLY_LOOP_V1_READY,
        "snapshot_summary": "v0.39.0-v0.39.8 consolidated as bounded v1 repair loop foundation metadata.",
        "enabled_bounded_capabilities": _enabled_bounded_capabilities(),
        "blocked_capabilities": _blocked_capabilities(),
        "future_track_capabilities": ["controlled multi-iteration mission loop", "verifier subagent boundary", "model/provider boundary gate"],
        "known_gaps": ["no controlled multi-iteration boundary yet", "no subagent invocation gate yet", "no model provider boundary yet"],
        "known_risks": ["approval confusion", "autonomous loop risk", "production certification confusion"],
        "evidence_refs": ["v0390-v0398-tests"],
    }
    return RepairLoopTrackSnapshot(**_with_overrides(defaults, overrides))


def build_repair_loop_capability_matrix(**overrides: Any) -> RepairLoopCapabilityMatrix:
    enabled = _enabled_bounded_capabilities()
    metadata_only = _metadata_capabilities()
    blocked = _blocked_capabilities()
    defaults = {
        "capability_matrix_id": "v0399-capability-matrix",
        "version": V0399_VERSION,
        "enabled_bounded_capabilities": enabled,
        "preview_only_capabilities": ["v0.39.8 CLI loop-state preview surface"],
        "metadata_only_capabilities": metadata_only,
        "blocked_capabilities": blocked,
        "future_track_capabilities": ["v0.40 controlled multi-iteration loop boundary", "v0.40 verifier subagent boundary", "v0.40 model/provider boundary gate"],
        "capability_to_stage": {
            "sandbox apply": "v0.39.3",
            "controlled re-test": "v0.39.4",
            "before/after comparison": "v0.39.5",
            "process-state reconstruction": "v0.39.6",
            "self-prompt drafts": "v0.39.7",
            "CLI preview": "v0.39.8",
        },
        "blocked_capability_to_reason": {cap: "requires future human-gated boundary" for cap in blocked},
        "evidence_refs": ["v0390-v0398-stage-records"],
    }
    return RepairLoopCapabilityMatrix(**_with_overrides(defaults, overrides))


def build_repair_loop_stage_coverage(**overrides: Any) -> RepairLoopStageCoverage:
    stage_version = overrides.pop("stage_version", "v0.39.8")
    defaults = {
        "coverage_id": f"coverage-{stage_version.replace('.', '')}",
        "version": V0399_VERSION,
        "stage_version": stage_version,
        "stage_name": V039_STAGE_NAMES.get(stage_version, "Unknown v0.39 stage"),
        "covered_artifact_refs": [f"{stage_version}-module"],
        "covered_test_refs": [f"{stage_version}-tests"],
        "covered_doc_refs": [f"{stage_version}-docs"],
        "blocking_gaps": [],
        "non_blocking_gaps": ["future runtime expansion remains gated"],
        "coverage_notes": ["coverage is release-track metadata, not production certification"],
        "coverage_complete": True,
        "evidence_refs": [stage_version],
    }
    return RepairLoopStageCoverage(**_with_overrides(defaults, overrides))


def build_repair_loop_boundary_register(**overrides: Any) -> RepairLoopBoundaryRegister:
    defaults = {
        "boundary_register_id": "v0399-boundary-register",
        "version": V0399_VERSION,
        "inherited_boundaries": ["v0.37 controlled test runner boundary", "v0.38 bounded proposal loop boundary"],
        "v039_opened_boundaries": ["approval artifact gate", "workspace isolation contract", "bounded sandbox apply", "controlled post-apply re-test", "CLI preview surface"],
        "active_bounded_runtime_boundaries": ["sandbox-only apply", "controlled post-apply re-test"],
        "preview_only_boundaries": ["self-prompt draft preview", "subagent prompt draft preview", "CLI loop-state surface"],
        "metadata_only_boundaries": ["before/after comparison", "process-state reconstruction", "PIG diagnostic input"],
        "prohibited_boundaries": [
            "live apply",
            "approval-less apply",
            "prompt execution",
            "model invocation",
            "subagent invocation",
            "external agent",
            "shell/subprocess",
            "arbitrary command",
            "autonomous loop",
            "retry loop",
            "multi-cycle loop",
            "Dominion",
            "production certification",
        ],
        "future_gate_boundaries": ["controlled multi-iteration loop", "verifier subagent gate", "model/provider gate"],
        "evidence_refs": ["v039-boundaries"],
    }
    return RepairLoopBoundaryRegister(**_with_overrides(defaults, overrides))


def build_repair_loop_risk_register(**overrides: Any) -> RepairLoopRiskRegister:
    defaults = {
        "risk_register_id": "v0399-risk-register",
        "version": V0399_VERSION,
        "known_risks": [
            "approval confusion",
            "sandbox/live confusion",
            "prompt execution confusion",
            "subagent invocation confusion",
            "autonomous loop risk",
            "production certification confusion",
            "cognitive surrender",
            "token cost loop explosion",
            "Dominion/runtime authority risk",
        ],
        "high_risk_surfaces": ["live apply", "model invocation", "subagent invocation", "autonomous loop", "Dominion"],
        "mitigations": ["human handoff", "unsafe readiness false", "draft-only prompt contracts", "preview-only CLI surface"],
        "unresolved_risks": ["multi-iteration boundaries not yet implemented", "subagent invocation authenticity gate absent"],
        "future_watch_items": ["v0.40 loop budget gate", "v0.40 stop-condition contract"],
        "evidence_refs": ["v039-risk-register"],
    }
    return RepairLoopRiskRegister(**_with_overrides(defaults, overrides))


def build_repair_loop_gap_register(**overrides: Any) -> RepairLoopGapRegister:
    defaults = {
        "gap_register_id": "v0399-gap-register",
        "version": V0399_VERSION,
        "blocking_gaps": [],
        "non_blocking_gaps": ["no v0.40 implementation yet", "no verifier subagent invocation gate yet"],
        "future_track_items": ["live apply gate", "persistent trace store", "UI runtime", "external harness adapter", "Dominion gated review"],
        "recommended_v040_items": [
            "controlled multi-iteration boundary",
            "verifier subagent boundary",
            "model/provider boundary",
            "loop budget gate",
            "stop-condition contract",
            "human checkpoint gate",
        ],
        "recommended_later_items": ["live workspace apply gate", "persistent trace store", "Dominion gated review"],
        "evidence_refs": ["v040-handoff-plan"],
    }
    return RepairLoopGapRegister(**_with_overrides(defaults, overrides))


def build_repair_loop_release_manifest(**overrides: Any) -> RepairLoopReleaseManifest:
    flags = overrides.pop("release_flags", build_repair_loop_consolidation_flags())
    defaults = {
        "release_manifest_id": "v0399-release-manifest",
        "version": V0399_VERSION,
        "release_name": V039_FOUNDATION_RELEASE_NAME,
        "snapshot_id": "v0399-track-snapshot",
        "included_versions": default_v039_included_versions(),
        "included_modules": _included_modules(),
        "included_docs": _included_docs(),
        "included_tests": _included_tests(),
        "focused_test_command": "py -m pytest tests/test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        "full_track_test_command": "py -m pytest tests/test_v0390_human_approved_sandbox_repair_apply_boundary.py tests/test_v0391_approval_artifact_intake_authenticity_gate.py tests/test_v0392_sandbox_repair_workspace_isolation.py tests/test_v0393_human_approved_patch_materialization_sandbox_apply.py tests/test_v0394_post_apply_controlled_retest.py tests/test_v0395_before_after_repair_outcome_comparison.py tests/test_v0396_pi_native_repair_process_state_reconstruction.py tests/test_v0397_self_prompting_next_action_draft_subagent_prompt_contract.py tests/test_v0398_cli_sandbox_repair_apply_retest_loop_state_surface.py tests/test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        "release_flags": flags,
        "known_gaps": ["v0.40 loop boundaries not implemented"],
        "known_risks": ["autonomous loop risk", "production certification confusion"],
        "next_handoff_id": "v040-handoff-packet",
    }
    return RepairLoopReleaseManifest(**_with_overrides(defaults, overrides))


def build_repair_loop_audit_trail(**overrides: Any) -> RepairLoopAuditTrail:
    defaults = {
        "audit_trail_id": "v0399-audit-trail",
        "version": V0399_VERSION,
        "reviewed_artifact_refs": _included_modules(),
        "reviewed_test_refs": _included_tests(),
        "reviewed_doc_refs": _included_docs(),
        "boundary_checks": ["bounded sandbox apply only", "controlled re-test only", "draft-only prompts", "preview-only CLI"],
        "runtime_checks": ["no live apply", "no shell", "no model invocation", "no subagent invocation"],
        "loop_safety_checks": ["human handoff required", "no autonomous loop", "no retry loop", "no multi-cycle loop"],
        **{name: True for name in AUDIT_TRUE_NAMES},
        "evidence_refs": ["v0399-consolidation-tests"],
    }
    return RepairLoopAuditTrail(**_with_overrides(defaults, overrides))


def build_repair_loop_stage_consolidation_record(**overrides: Any) -> RepairLoopStageConsolidationRecord:
    stage_version = overrides.pop("stage_version", "v0.39.8")
    defaults = {
        "record_id": f"record-{stage_version.replace('.', '')}",
        "version": V0399_VERSION,
        "stage_version": stage_version,
        "stage_name": V039_STAGE_NAMES.get(stage_version, "Unknown v0.39 stage"),
        "completed_capabilities": [V039_STAGE_NAMES.get(stage_version, "stage metadata")],
        "blocked_capabilities": _blocked_capabilities(),
        "future_track_items": ["v0.40 controlled multi-iteration boundary"],
        "confirmation_booleans": {"metadata_only_consolidation": True, "production_certified": False},
        "summary": f"{stage_version} consolidated into v0.39.9 track snapshot.",
        "evidence_refs": [stage_version],
    }
    return RepairLoopStageConsolidationRecord(**_with_overrides(defaults, overrides))


def build_loop_engineering_pi_native_consolidation_record(**overrides: Any) -> LoopEngineeringPINativeConsolidationRecord:
    defaults = {
        "record_id": "v0399-loop-engineering-pi-native",
        "version": V0399_VERSION,
        "external_term": "Loop Engineering",
        "adopted_as_top_level_concept": False,
        "pi_native_terms": [
            "Self-Prompting Mission Loop",
            "PI-native Mission Execution Loop",
            "Process-State-Driven Self-Prompting",
            "Agent-to-Subagent Prompting Cycle",
            "Human-Handoff-Gated Next-Action Draft",
            "CLI Loop-State Surface",
            "Process-State Repair Bundle",
        ],
        "absorbed_patterns": [
            "system/loop prompts as draft-only process-state-driven prompt artifact generation",
            "worktree/parallel isolation as sandbox workspace isolation contract",
            "maker/checker split as subagent verification request draft",
            "external memory/state file as process-state reconstruction metadata",
            "loop control panel as CLI preview surface",
        ],
        "rejected_patterns": ["unrestricted autonomous loop", "prompt execution", "subagent invocation", "external agent execution", "cognitive surrender"],
        "safety_interpretation": "Loop patterns are absorbed as PI-native metadata and draft contracts with mandatory human handoff.",
        "human_handoff_required": True,
        "autonomous_loop_opened": False,
        "subagent_invocation_opened": False,
        "prompt_execution_opened": False,
        "model_invocation_opened": False,
        "evidence_refs": ["v0396-v0398-loop-surface"],
    }
    return LoopEngineeringPINativeConsolidationRecord(**_with_overrides(defaults, overrides))


def build_v040_handoff_packet(**overrides: Any) -> V040HandoffPacket:
    defaults = {
        "handoff_id": "v040-handoff-packet",
        "version": V0399_VERSION,
        "source_track": V039_FOUNDATION_RELEASE_NAME,
        "target_track": V040_TARGET_TRACK,
        "recommended_next_release": V040_NEXT_RELEASE,
        "handoff_summary": "Design-stage handoff to controlled multi-iteration and subagent verification boundaries.",
        "reusable_v039_capabilities": _enabled_bounded_capabilities() + _metadata_capabilities() + ["CLI loop-state preview surface"],
        "required_new_boundaries": ["controlled multi-iteration mission loop boundary", "verifier subagent boundary metadata", "model/provider boundary gate"],
        "proposed_v040_stage_plan": default_v040_handoff_plan(),
        "prohibited_until_future_gate": ["unrestricted autonomous loops", "automatic repair loops", "arbitrary subagent execution", "external coding agent execution", "uncontrolled model provider invocation", "live workspace apply", "Dominion runtime", "production certification"],
        "required_human_gates": ["human checkpoint gate", "human handoff after each iteration"],
        "required_loop_safety_gates": ["max iteration policy", "stop-condition contract", "no autonomous infinite loop"],
        "required_budget_gates": ["loop budget gate", "token budget gate"],
        "required_subagent_gates": ["verifier subagent boundary", "subagent invocation authenticity/safety gate"],
        "required_model_provider_gates": ["model/provider boundary gate", "provider invocation approval gate"],
        "ready_for_v040_design_handoff": True,
        "evidence_refs": ["v0399-gap-register"],
    }
    return V040HandoffPacket(**_with_overrides(defaults, overrides))


def build_v039_consolidation_report(**overrides: Any) -> V039ConsolidationReport:
    snapshot = overrides.pop("snapshot", build_repair_loop_track_snapshot())
    matrix = overrides.pop("capability_matrix", build_repair_loop_capability_matrix())
    coverages = overrides.pop("stage_coverages", [build_repair_loop_stage_coverage(stage_version=version) for version in V039_INCLUDED_VERSIONS])
    boundary = overrides.pop("boundary_register", build_repair_loop_boundary_register())
    risk = overrides.pop("risk_register", build_repair_loop_risk_register())
    gaps = overrides.pop("gap_register", build_repair_loop_gap_register())
    manifest = overrides.pop("release_manifest", build_repair_loop_release_manifest())
    audit = overrides.pop("audit_trail", build_repair_loop_audit_trail())
    records = overrides.pop("stage_records", [build_repair_loop_stage_consolidation_record(stage_version=version) for version in V039_INCLUDED_VERSIONS])
    loop_record = overrides.pop("loop_engineering_record", build_loop_engineering_pi_native_consolidation_record())
    handoff = overrides.pop("v040_handoff_packet", build_v040_handoff_packet())
    defaults = {
        "report_id": "v0399-consolidation-report",
        "version": V0399_VERSION,
        "release_name": V039_FOUNDATION_RELEASE_NAME,
        "snapshot": snapshot,
        "capability_matrix": matrix,
        "stage_coverages": coverages,
        "boundary_register": boundary,
        "risk_register": risk,
        "gap_register": gaps,
        "release_manifest": manifest,
        "audit_trail": audit,
        "stage_records": records,
        "loop_engineering_record": loop_record,
        "v040_handoff_packet": handoff,
        "consolidation_status": RepairLoopConsolidationStatus.HANDOFF_READY_FOR_V040,
        "readiness_level": RepairLoopConsolidationReadinessLevel.HUMAN_APPROVED_SANDBOX_REPAIR_APPLY_LOOP_V1_READY,
        "report_summary": "v0.39.x consolidated as Human-approved Sandbox Repair Apply & Re-test Loop v1 with PI-native self-prompting boundary.",
        "ready_for_v040_handoff": True,
        "human_approved_sandbox_repair_apply_loop_v1_ready": True,
        "evidence_refs": ["v0399-track-snapshot", "v040-handoff-packet"],
    }
    return V039ConsolidationReport(**_with_overrides(defaults, overrides))


def build_repair_loop_consolidation_validation_finding(**overrides: Any) -> RepairLoopConsolidationValidationFinding:
    defaults = {
        "finding_id": "v0399-validation-finding",
        "finding_summary": "Consolidation introduces no new runtime authority.",
        "blocked": False,
    }
    return RepairLoopConsolidationValidationFinding(**_with_overrides(defaults, overrides))


def build_repair_loop_consolidation_validation_report(**overrides: Any) -> RepairLoopConsolidationValidationReport:
    defaults = {
        "validation_report_id": "v0399-validation-report",
        "version": V0399_VERSION,
        "validation_summary": "Validation confirms consolidation-only behavior and no unsafe runtime expansion.",
        "findings": [build_repair_loop_consolidation_validation_finding()],
        "consolidation_only_confirmed": True,
        "no_new_runtime_expansion_confirmed": True,
        "no_runtime_execution_confirmed": True,
        "no_production_certification_confirmed": True,
    }
    return RepairLoopConsolidationValidationReport(**_with_overrides(defaults, overrides))


def build_repair_loop_consolidation_run_preview(**overrides: Any) -> RepairLoopConsolidationRunPreview:
    defaults = {
        "preview_id": "v0399-run-preview",
        "version": V0399_VERSION,
        "preview_summary": "Preview lists consolidation metadata steps only.",
        "planned_consolidation_steps": ["TrackSnapshot", "CapabilityMatrix", "Registers", "AuditTrail", "V040HandoffPacket", "V039ConsolidationReport"],
    }
    return RepairLoopConsolidationRunPreview(**_with_overrides(defaults, overrides))


def build_repair_loop_no_unsafe_expansion_guarantee(**overrides: Any) -> RepairLoopNoUnsafeExpansionGuarantee:
    defaults = {
        "guarantee_id": "v0399-no-unsafe-expansion",
        "version": V0399_VERSION,
        "guarantee_summary": "v0.39.9 is consolidation-only and opens no unsafe runtime/action/persistence authority.",
    }
    return RepairLoopNoUnsafeExpansionGuarantee(**_with_overrides(defaults, overrides))


def repair_loop_consolidation_flags_preserve_no_unsafe_runtime(flags: RepairLoopConsolidationFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_loop_capability_matrix_is_not_permission_grant(matrix: RepairLoopCapabilityMatrix) -> bool:
    return bool(matrix.blocked_capabilities) and "permission" not in " ".join(matrix.enabled_bounded_capabilities).lower()


def repair_loop_audit_confirms_no_unsafe_runtime(audit: RepairLoopAuditTrail) -> bool:
    return all(getattr(audit, name) is True for name in AUDIT_TRUE_NAMES)


def loop_engineering_record_is_pi_native_absorption(record: LoopEngineeringPINativeConsolidationRecord) -> bool:
    return (
        record.external_term == "Loop Engineering"
        and record.adopted_as_top_level_concept is False
        and "Self-Prompting Mission Loop" in record.pi_native_terms
        and record.human_handoff_required is True
        and record.autonomous_loop_opened is False
        and record.subagent_invocation_opened is False
        and record.prompt_execution_opened is False
        and record.model_invocation_opened is False
    )


def v040_handoff_packet_is_design_only(packet: V040HandoffPacket) -> bool:
    return (
        packet.ready_for_v040_design_handoff is True
        and packet.ready_for_v040_execution is False
        and packet.ready_for_autonomous_loop_runtime is False
        and packet.ready_for_subagent_invocation is False
        and packet.ready_for_model_provider_invocation is False
        and packet.ready_for_prompt_execution is False
        and packet.ready_for_live_apply is False
        and packet.ready_for_dominion_runtime is False
        and packet.production_certified is False
    )


def v039_consolidation_report_is_not_execution_ready(report: V039ConsolidationReport) -> bool:
    return (
        report.ready_for_v040_handoff is True
        and report.human_approved_sandbox_repair_apply_loop_v1_ready is True
        and report.production_certified is False
        and report.ready_for_execution is False
        and report.ready_for_live_apply is False
        and report.ready_for_prompt_execution is False
        and report.ready_for_subagent_invocation is False
        and report.ready_for_model_provider_invocation is False
        and report.ready_for_autonomous_loop_runtime is False
        and report.ready_for_dominion_runtime is False
    )
