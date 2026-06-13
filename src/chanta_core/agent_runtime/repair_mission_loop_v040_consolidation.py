"""v0.40.9 final v0.40 consolidation and v0.41 handoff metadata.

This module is consolidation-only. It creates reports, inventories, gap
records, startup-plan metadata, restore packets, and handoff records. It does
not execute commands, submit prompts, invoke providers, invoke subagents, create
child sessions, mutate files, use network access, or implement v0.41 runtime.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank
from .repair_mission_loop_boundary import (
    HumanCheckpointGate,
    IterationState,
    LoopBudgetGate,
    MissionLoopEnvelope,
    PromptSubmissionBoundary,
    ProviderBoundaryGate,
    StopConditionContract,
    V040ReadinessReport,
    VerifierSubagentBoundary,
)
from .repair_mission_loop_checkpoint_hardening import CheckpointHardeningReadinessReport, V0404RestorePacket
from .repair_mission_loop_cli_preview_surface import (
    CLIExecutionTestPreviewSurface,
    CLIPreviewSurfaceReadinessReport,
    V0408IntegratedRestorePacket,
)
from .repair_mission_loop_evidence_matrix import (
    BoundaryCoverageReadinessReport,
    RehearsalEvidenceMatrix,
    V0407IntegratedRestorePacket,
)
from .repair_mission_loop_negative_gates import (
    DeniedRuntimeActionCoverageMatrix,
    NegativeRuntimeGateReadinessReport,
)
from .repair_mission_loop_provider_prompt_boundary import (
    ProviderPromptBoundaryReadinessReport,
    V0405IntegratedRestorePacket,
)
from .repair_mission_loop_rehearsal import DefaultPersonalStandaloneGapRegister, SandboxRehearsalReadinessReport
from .repair_mission_loop_two_iteration import (
    ManualTwoIterationReadinessReport,
    NoAutonomousContinuationGuarantee,
    StandaloneRuntimeStillClosedRecord,
)
from .repair_mission_loop_verifier_subagent_boundary import (
    V0406IntegratedRestorePacket,
    VerifierSubagentBoundaryReadinessReport,
)


V0409_VERSION = "v0.40.9"
V0409_RELEASE_NAME = "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff"
V0409_TRACK_NAME = (
    "Standalone-Agent Preparation Track: Controlled MissionLoop Boundary + Sandbox Rehearsal + "
    "Manual Checkpoint Gate + Negative Runtime Gate Regression + Scope-Bound Human Approval + "
    "Provider / Prompt Boundary Deepening + Verifier Subagent Boundary Deepening + Rehearsal "
    "Evidence Matrix & Boundary Coverage Consolidation + CLI Execution-Test Preview Surface + "
    "v0.41 Default Personal Runtime Handoff"
)
INTEGRATED_DOC_PATH = (
    "docs/versions/v0.40/"
    "v0.40.9_controlled_mission_loop_preparation_consolidation_v041_handoff_restore.md"
)


class V040ConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_NOTES = "consolidated_with_notes"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    V041_HANDOFF_READY = "v041_handoff_ready"
    BLOCKED = "blocked"
    REJECTED = "rejected"
    REVIEW_REQUIRED = "review_required"


class V040ConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_PREPARATION_COMPLETE = "boundary_preparation_complete"
    REHEARSAL_PREPARATION_COMPLETE = "rehearsal_preparation_complete"
    NEGATIVE_GATE_COMPLETE = "negative_gate_complete"
    CHECKPOINT_HARDENING_COMPLETE = "checkpoint_hardening_complete"
    PROVIDER_PROMPT_BOUNDARY_COMPLETE = "provider_prompt_boundary_complete"
    VERIFIER_SUBAGENT_BOUNDARY_COMPLETE = "verifier_subagent_boundary_complete"
    COVERAGE_CONSOLIDATION_COMPLETE = "coverage_consolidation_complete"
    CLI_PREVIEW_SURFACE_COMPLETE = "cli_preview_surface_complete"
    V040_FINAL_CONSOLIDATION_COMPLETE = "v040_final_consolidation_complete"
    V041_DESIGN_HANDOFF_READY = "v041_design_handoff_ready"
    BLOCKED = "blocked"


BASELINE_VERSIONS: tuple[str, ...] = (
    "v0.40.0 Controlled Multi-Iteration Mission Loop Boundary Foundation",
    "v0.40.1 Sandbox Rehearsal Runner & Standalone Agent Readiness Clarification",
    "v0.40.2 Manual Two-Iteration Rehearsal & Human Checkpoint Enforcement",
    "v0.40.3 Negative Runtime Gate Regression & Denied Runtime Action Coverage",
    "v0.40.4 Human Checkpoint Hardening & Scope-Bound Approval Contract",
    "v0.40.5 Provider / Prompt Boundary Deepening & Integrated Restore Handoff",
    "v0.40.6 Verifier Subagent Boundary Deepening & Integrated Restore Handoff",
    "v0.40.7 Rehearsal Evidence Matrix & Boundary Coverage Consolidation",
    "v0.40.8 CLI Execution-Test Preview Surface & Integrated Restore Handoff",
    "v0.40.9 Controlled Mission Loop Preparation Consolidation & v0.41 Default Personal Runtime Handoff",
)
OPEN_METADATA_PREVIEW_CAPABILITIES: tuple[str, ...] = (
    "mission_loop_boundary",
    "dry_run_simulation",
    "sandbox_rehearsal",
    "manual_two_iteration_rehearsal",
    "negative_runtime_gate_regression",
    "scope_bound_checkpoint_approval",
    "prompt_dispatch_candidate_metadata",
    "prompt_submission_gate",
    "provider_invocation_gate",
    "provider_output_quarantine_contract",
    "verifier_subagent_request_draft",
    "verifier_role_contract",
    "verifier_evidence_requirement",
    "verifier_context_isolation_contract",
    "verifier_dispatch_gate",
    "verifier_result_quarantine_contract",
    "rehearsal_evidence_matrix",
    "boundary_coverage_consolidation",
    "cli_preview_surface",
    "integrated_restore_handoff",
)
SNAPSHOT_OPEN_CAPABILITIES: tuple[str, ...] = (
    *OPEN_METADATA_PREVIEW_CAPABILITIES[:-1],
    "v040_final_consolidation",
    "v041_gap_register",
    "v041_startup_plan",
    "integrated_restore_document",
)
CLOSED_RUNTIME_CAPABILITIES: tuple[str, ...] = (
    "standalone_default_personal_runtime",
    "actual_cli_runtime_execution",
    "actual_apply_command",
    "actual_retest_command",
    "actual_test_execution",
    "actual_prompt_submission",
    "actual_model_provider_invocation",
    "actual_subagent_invocation",
    "actual_child_session_creation",
    "parent_raw_transcript_sharing",
    "subagent_permission_grant",
    "live_workspace_apply",
    "autonomous_loop_runtime",
    "automatic_repair_loop",
    "retry_loop",
    "network_access",
    "credential_access",
    "dominion_runtime",
    "production_certification",
)
BOUNDARY_NAMES: tuple[str, ...] = (
    "mission_loop_boundary",
    "dry_run_boundary",
    "sandbox_rehearsal_boundary",
    "manual_checkpoint_boundary",
    "negative_runtime_gate_boundary",
    "scope_bound_approval_boundary",
    "prompt_submission_boundary",
    "provider_invocation_boundary",
    "provider_output_quarantine_boundary",
    "verifier_subagent_boundary",
    "evidence_matrix_boundary",
    "cli_preview_boundary",
    "restore_handoff_boundary",
    "standalone_runtime_closed_boundary",
)
SAFETY_CLOSURE_SURFACES: tuple[str, ...] = (
    "execution",
    "general_execution",
    "cli_runtime_execution",
    "apply_command",
    "retest_command",
    "test_execution",
    "live_workspace_apply",
    "prompt_submission_to_model",
    "model_provider_invocation",
    "subagent_invocation",
    "child_session_creation",
    "parent_raw_transcript_sharing",
    "external_agent_execution",
    "autonomous_loop_runtime",
    "automatic_repair",
    "retry_loop",
    "multi_cycle_loop",
    "standalone_default_personal_runtime",
    "dominion_runtime",
    "production_certification",
)
REQUIRED_FALSE_FLAGS: tuple[str, ...] = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_cli_runtime_execution",
    "ready_for_apply_command",
    "ready_for_retest_command",
    "ready_for_test_execution",
    "ready_for_live_workspace_apply",
    "ready_for_prompt_submission_to_model",
    "ready_for_model_provider_invocation",
    "ready_for_subagent_invocation",
    "ready_for_child_session_creation",
    "ready_for_parent_raw_transcript_sharing",
    "ready_for_external_agent_execution",
    "ready_for_autonomous_loop_runtime",
    "ready_for_automatic_repair",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_loop",
    "ready_for_standalone_default_personal_runtime",
    "ready_for_v041_runtime_execution",
    "ready_for_first_default_personal_smoke_run",
    "ready_for_dominion_runtime",
    "production_certified",
)
REQUIRED_V041_COMPONENTS: tuple[str, ...] = (
    "PersonalRoot",
    "DefaultPersonalProfileRuntime",
    "SoulRoleDomainPromptAssembly",
    "SessionStore",
    "UserInputSurface",
    "ChatServiceOrCLIEntry",
    "Orchestrator",
    "MinimalAgentLoop",
    "ReadOnlySkillRegistry",
    "SkillSelector",
    "ReadOnlySkillExecutor",
    "ObservationCollector",
    "ResponseRenderer",
    "EventTraceEmitter",
    "RestoreContextLoader",
    "SafetyBoundaryLoader",
    "V040CompatibilityGate",
    "DefaultPersonalSmokeScenario",
)
REQUIRED_RESTORE_SECTION_IDS: tuple[str, ...] = (
    "restore_purpose",
    "one_screen_restore_summary",
    "current_version_and_track",
    "repository_baseline_assumptions",
    "version_chain_summary",
    "current_implemented_modules",
    "current_test_files",
    "current_documentation_files",
    "v040_stage_summary",
    "v040_final_capability_matrix",
    "v040_boundary_inventory",
    "v040_safety_closure_register",
    "v040_artifact_inventory",
    "v040_test_coverage_summary",
    "v040_restore_index",
    "standalone_runtime_still_closed",
    "v041_required_runtime_components",
    "v041_standalone_runtime_gap_register",
    "v041_default_personal_startup_plan",
    "v041_default_personal_smoke_scenario",
    "v041_runtime_opening_gates",
    "v041_acceleration_assessment",
    "capability_matrix",
    "safety_flag_canonical_values",
    "how_to_verify_this_state",
    "required_test_commands",
    "expected_test_interpretation",
    "known_limitations",
    "withdrawal_conditions",
    "v0410_handoff",
    "copy_paste_restore_prompt",
)


@dataclass(frozen=True)
class V040StageSummary:
    stage_id: str
    version: str
    release_name: str
    primary_purpose: str
    opened_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    implementation_artifact_refs: tuple[str, ...]
    test_refs: tuple[str, ...]
    doc_refs: tuple[str, ...]
    restore_refs: tuple[str, ...]
    handoff_target: str
    safety_notes: tuple[str, ...]
    consolidation_status: str


@dataclass(frozen=True)
class V040CapabilityMatrix:
    matrix_id: str
    open_metadata_preview_capabilities: tuple[str, ...]
    closed_runtime_capabilities: tuple[str, ...]
    evidence_refs: tuple[str, ...]
    consolidation_status: str
    permission_grant: bool = False
    production_certified: bool = False


@dataclass(frozen=True)
class V040BoundaryInventory:
    inventory_id: str
    boundaries: tuple[dict[str, Any], ...]
    all_major_boundaries_listed: bool
    runtime_authority_granted: bool = False


@dataclass(frozen=True)
class V040SafetyClosureRegister:
    register_id: str
    closure_items: dict[str, dict[str, Any]]
    all_closures_confirmed: bool
    unsafe_readiness_true_count: int
    runtime_authority_granted: bool = False


@dataclass(frozen=True)
class V040ArtifactInventory:
    inventory_id: str
    implementation_modules: tuple[str, ...]
    test_files: tuple[str, ...]
    documentation_files: tuple[str, ...]
    known_optional_docs: tuple[str, ...]
    missing_or_advisory_only_items: tuple[str, ...]


@dataclass(frozen=True)
class V040TestCoverageSummary:
    summary_id: str
    focused_v0409_test: str
    regression_v0408: str
    regression_v0407: str
    regression_v0406: str
    regression_v0405: str
    regression_v0404: str
    regression_v0403: str
    regression_v0402: str
    regression_v0401: str
    regression_v0400: str
    regression_v0399: str
    aggregate_attempted: bool
    skipped_or_not_run_reason: str | None


@dataclass(frozen=True)
class V040RestoreIndex:
    index_id: str
    restore_docs: tuple[str, ...]
    integrated_restore_docs: tuple[str, ...]
    copy_paste_restore_prompt_exists: bool
    capability_matrix_exists: bool
    safety_flag_table_exists: bool
    next_handoff_exists: bool
    does_not_claim_standalone_runtime_opened: bool


@dataclass(frozen=True)
class V040StandaloneRuntimeStillClosedRecord:
    record_id: str = "v040-standalone-runtime-still-closed"
    profile_runtime_opened: bool = False
    chat_service_opened: bool = False
    orchestrator_opened: bool = False
    agent_loop_opened: bool = False
    skill_loader_opened: bool = False
    skill_executor_opened: bool = False
    read_only_skill_registry_opened: bool = False
    event_trace_emitter_opened: bool = False
    session_store_opened: bool = False
    user_facing_cli_opened: bool = False
    standalone_default_personal_runtime_opened: bool = False


@dataclass(frozen=True)
class V041RequiredRuntimeComponent:
    component_id: str
    component_name: str
    required_for: str
    current_status: str
    target_version: str
    blocking_if_missing: bool
    safety_notes: tuple[str, ...]
    evidence_refs: tuple[str, ...]


@dataclass(frozen=True)
class V041StandaloneRuntimeGap:
    gap_id: str
    component_name: str
    missing: bool
    blocking: bool
    target_version: str
    evidence_refs: tuple[str, ...]
    note: str


@dataclass(frozen=True)
class V041StandaloneRuntimeGapRegister:
    register_id: str
    required_components: tuple[V041RequiredRuntimeComponent, ...]
    gaps: tuple[V041StandaloneRuntimeGap, ...]
    standalone_runtime_started: bool
    ready_for_v041_runtime_execution: bool
    ready_for_first_smoke_run: bool
    no_v041_component_implemented_in_v0409: bool


@dataclass(frozen=True)
class V041DefaultPersonalStartupPlan:
    plan_id: str
    stages: tuple[dict[str, Any], ...]
    recommended_sequence: tuple[str, ...]


@dataclass(frozen=True)
class V041DefaultPersonalSmokeScenario:
    scenario_id: str
    input_text: str
    expected_runtime_path: tuple[str, ...]
    design_only: bool
    executed: bool
    marks_runtime_ready: bool


@dataclass(frozen=True)
class V041RuntimeOpeningGate:
    gate_id: str
    required_gates: dict[str, bool]
    design_targets_only: bool
    current_v0409_runtime_opened: bool


@dataclass(frozen=True)
class V041AccelerationAssessment:
    assessment_id: str
    earliest_candidate_target: str
    recommendation: str
    missing_components: tuple[str, ...]
    non_authoritative: bool
    ready_for_standalone_default_personal_runtime: bool


@dataclass(frozen=True)
class V0409ConsolidationAuditRecord:
    audit_id: str
    all_v040_stages_summarized: bool
    all_major_boundaries_inventoried: bool
    all_unsafe_runtime_capabilities_closed: bool
    restore_index_complete: bool
    v041_gap_register_produced: bool
    v041_startup_plan_produced: bool
    no_runtime_expansion_introduced: bool
    no_standalone_runtime_opened: bool
    no_production_certification_claimed: bool


@dataclass(frozen=True)
class V0409SafetyReport:
    report_id: str
    safe_for_v0409_consolidation: bool
    safe_for_runtime_execution: bool
    safe_for_cli_runtime_execution: bool
    safe_for_live_workspace_apply: bool
    safe_for_prompt_submission: bool
    safe_for_model_provider_invocation: bool
    safe_for_subagent_invocation: bool
    safe_for_child_session_creation: bool
    safe_for_parent_raw_transcript_sharing: bool
    safe_for_network_access: bool
    safe_for_credential_access: bool
    safe_for_standalone_default_personal_runtime: bool
    safe_for_dominion_runtime: bool
    production_certified: bool
    ready_for_v041_design_handoff: bool


@dataclass(frozen=True)
class V0409ReadinessReport:
    report_id: str
    v040_final_consolidation_defined: bool
    v040_capability_matrix_ready: bool
    v040_boundary_inventory_ready: bool
    v040_safety_closure_register_ready: bool
    v040_artifact_inventory_ready: bool
    v040_test_coverage_summary_ready: bool
    v040_restore_index_ready: bool
    v041_gap_register_ready: bool
    v041_startup_plan_ready: bool
    v041_smoke_scenario_defined: bool
    v041_handoff_ready: bool
    integrated_restore_document_ready: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_cli_runtime_execution: bool
    ready_for_apply_command: bool
    ready_for_retest_command: bool
    ready_for_test_execution: bool
    ready_for_live_workspace_apply: bool
    ready_for_prompt_submission_to_model: bool
    ready_for_model_provider_invocation: bool
    ready_for_subagent_invocation: bool
    ready_for_child_session_creation: bool
    ready_for_parent_raw_transcript_sharing: bool
    ready_for_external_agent_execution: bool
    ready_for_autonomous_loop_runtime: bool
    ready_for_automatic_repair: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_loop: bool
    ready_for_standalone_default_personal_runtime: bool
    ready_for_v041_runtime_execution: bool
    ready_for_first_default_personal_smoke_run: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V0409IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool
    content_summary: str
    restore_value: str


@dataclass(frozen=True)
class V0409IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    implemented_modules: tuple[str, ...]
    test_files: tuple[str, ...]
    docs: tuple[str, ...]
    open_capabilities: tuple[str, ...]
    closed_capabilities: tuple[str, ...]
    next_recommended_version: str
    next_recommended_focus: str


@dataclass(frozen=True)
class V0409IntegratedRestorePacket:
    restore_packet_id: str
    snapshot: V0409IntegratedRestoreContextSnapshot
    restore_sections: tuple[V0409IntegratedRestoreSection, ...]
    required_test_commands: tuple[str, ...]
    required_false_flags: tuple[str, ...]
    restore_prompt_summary: str
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0409IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool
    suitable_for_new_session_handoff: bool


@dataclass(frozen=True)
class V0410DefaultPersonalProfileRuntimeHandoff:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    required_inputs_from_v0409: tuple[str, ...]
    still_closed: tuple[str, ...]
    risk_notes: tuple[str, ...]


def _with_overrides(defaults: dict[str, Any], overrides: dict[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _stage_defaults() -> dict[str, dict[str, Any]]:
    return {
        "v0.40.0": {
            "release_name": "Controlled Multi-Iteration Mission Loop Boundary Foundation",
            "primary_purpose": "Define mission-loop boundary and dry-run simulation metadata.",
            "opened_capabilities": ("mission_loop_boundary", "dry_run_simulation"),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_boundary.py",),
            "tests": ("tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py",),
            "docs": ("docs/versions/v0.40/v0.40.0_controlled_multi_iteration_mission_loop_boundary.md",),
            "restore": (),
            "handoff": "v0.40.1 Sandbox rehearsal runner",
        },
        "v0.40.1": {
            "release_name": "Sandbox Rehearsal Runner & Standalone Agent Readiness Clarification",
            "primary_purpose": "Add sandbox rehearsal metadata and standalone gap register.",
            "opened_capabilities": ("sandbox_rehearsal",),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_rehearsal.py",),
            "tests": ("tests/test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",),
            "docs": ("docs/versions/v0.40/v0.40.1_sandbox_rehearsal_runner_standalone_readiness.md",),
            "restore": (),
            "handoff": "v0.40.2 Manual two-iteration rehearsal",
        },
        "v0.40.2": {
            "release_name": "Manual Two-Iteration Rehearsal & Human Checkpoint Enforcement",
            "primary_purpose": "Require manual checkpoint between two bounded rehearsal iterations.",
            "opened_capabilities": ("manual_two_iteration_rehearsal",),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_two_iteration.py",),
            "tests": ("tests/test_v0402_manual_two_iteration_rehearsal.py",),
            "docs": ("docs/versions/v0.40/v0.40.2_manual_two_iteration_rehearsal.md",),
            "restore": (),
            "handoff": "v0.40.3 Negative runtime gate regression",
        },
        "v0.40.3": {
            "release_name": "Negative Runtime Gate Regression & Denied Runtime Action Coverage",
            "primary_purpose": "Record denied unsafe runtime action coverage.",
            "opened_capabilities": ("negative_runtime_gate_regression",),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_negative_gates.py",),
            "tests": ("tests/test_v0403_negative_runtime_gate_regression.py",),
            "docs": ("docs/versions/v0.40/v0.40.3_negative_runtime_gate_regression.md",),
            "restore": (),
            "handoff": "v0.40.4 Human checkpoint hardening",
        },
        "v0.40.4": {
            "release_name": "Human Checkpoint Hardening & Scope-Bound Approval Contract",
            "primary_purpose": "Harden approval with freshness, artifact binding, revocation, and expiry metadata.",
            "opened_capabilities": ("scope_bound_checkpoint_approval",),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_checkpoint_hardening.py",),
            "tests": ("tests/test_v0404_human_checkpoint_hardening_restore.py",),
            "docs": ("docs/versions/v0.40/v0.40.4_human_checkpoint_hardening_restore.md",),
            "restore": ("docs/versions/v0.40/v0.40.4_human_checkpoint_hardening_restore.md",),
            "handoff": "v0.40.5 Provider / prompt boundary deepening",
        },
        "v0.40.5": {
            "release_name": "Provider / Prompt Boundary Deepening & Integrated Restore Handoff",
            "primary_purpose": "Define prompt candidate, prompt submission gate, provider gate, and output quarantine.",
            "opened_capabilities": (
                "prompt_dispatch_candidate_metadata",
                "prompt_submission_gate",
                "provider_invocation_gate",
                "provider_output_quarantine_contract",
            ),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_provider_prompt_boundary.py",),
            "tests": ("tests/test_v0405_provider_prompt_boundary_deepening_restore.py",),
            "docs": ("docs/versions/v0.40/v0.40.5_provider_prompt_boundary_deepening_restore.md",),
            "restore": ("docs/versions/v0.40/v0.40.5_provider_prompt_boundary_deepening_restore.md",),
            "handoff": "v0.40.6 Verifier subagent boundary deepening",
        },
        "v0.40.6": {
            "release_name": "Verifier Subagent Boundary Deepening & Integrated Restore Handoff",
            "primary_purpose": "Define verifier request drafts, role/evidence/context gates, and result quarantine.",
            "opened_capabilities": (
                "verifier_subagent_request_draft",
                "verifier_role_contract",
                "verifier_evidence_requirement",
                "verifier_context_isolation_contract",
                "verifier_dispatch_gate",
                "verifier_result_quarantine_contract",
            ),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_verifier_subagent_boundary.py",),
            "tests": ("tests/test_v0406_verifier_subagent_boundary_deepening_restore.py",),
            "docs": ("docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening_restore.md",),
            "restore": ("docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening_restore.md",),
            "handoff": "v0.40.7 Rehearsal evidence matrix",
        },
        "v0.40.7": {
            "release_name": "Rehearsal Evidence Matrix & Boundary Coverage Consolidation",
            "primary_purpose": "Consolidate coverage, evidence, denied action, restore, and readiness flags.",
            "opened_capabilities": ("rehearsal_evidence_matrix", "boundary_coverage_consolidation"),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_evidence_matrix.py",),
            "tests": ("tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py",),
            "docs": ("docs/versions/v0.40/v0.40.7_rehearsal_evidence_matrix_boundary_coverage_restore.md",),
            "restore": ("docs/versions/v0.40/v0.40.7_rehearsal_evidence_matrix_boundary_coverage_restore.md",),
            "handoff": "v0.40.8 CLI preview surface",
        },
        "v0.40.8": {
            "release_name": "CLI Execution-Test Preview Surface & Integrated Restore Handoff",
            "primary_purpose": "Define preview-only CLI metadata and deterministic read-only views.",
            "opened_capabilities": ("cli_preview_surface",),
            "implementation": ("src/chanta_core/agent_runtime/repair_mission_loop_cli_preview_surface.py",),
            "tests": ("tests/test_v0408_cli_execution_test_preview_surface_restore.py",),
            "docs": ("docs/versions/v0.40/v0.40.8_cli_execution_test_preview_surface_restore.md",),
            "restore": ("docs/versions/v0.40/v0.40.8_cli_execution_test_preview_surface_restore.md",),
            "handoff": "v0.40.9 Final v0.40 consolidation",
        },
    }


def create_v040_stage_summary(version: str = "v0.40.8", **overrides: Any) -> V040StageSummary:
    _require_non_blank(version, "version")
    stages = _stage_defaults()
    if version not in stages:
        raise ValueError(f"unknown v0.40 stage for consolidation: {version}")
    stage = stages[version]
    defaults = {
        "stage_id": f"stage-{version.replace('.', '-')}",
        "version": version,
        "release_name": stage["release_name"],
        "primary_purpose": stage["primary_purpose"],
        "opened_capabilities": stage["opened_capabilities"],
        "closed_capabilities": CLOSED_RUNTIME_CAPABILITIES,
        "implementation_artifact_refs": stage["implementation"],
        "test_refs": stage["tests"],
        "doc_refs": stage["docs"],
        "restore_refs": stage["restore"],
        "handoff_target": stage["handoff"],
        "safety_notes": (
            "runtime authority remains closed",
            "production certification remains false",
        ),
        "consolidation_status": V040ConsolidationStatus.CONSOLIDATED.value,
    }
    return V040StageSummary(**_with_overrides(defaults, overrides))


def build_v040_stage_summaries() -> tuple[V040StageSummary, ...]:
    return tuple(create_v040_stage_summary(version) for version in _stage_defaults())


def build_v040_capability_matrix(**overrides: Any) -> V040CapabilityMatrix:
    defaults = {
        "matrix_id": "v040-final-capability-matrix",
        "open_metadata_preview_capabilities": OPEN_METADATA_PREVIEW_CAPABILITIES,
        "closed_runtime_capabilities": CLOSED_RUNTIME_CAPABILITIES,
        "evidence_refs": (
            "V040StageSummary",
            "V040BoundaryInventory",
            "V040SafetyClosureRegister",
            "V040RestoreIndex",
        ),
        "consolidation_status": V040ConsolidationStatus.V041_HANDOFF_READY.value,
        "permission_grant": False,
        "production_certified": False,
    }
    return V040CapabilityMatrix(**_with_overrides(defaults, overrides))


def build_v040_boundary_inventory(**overrides: Any) -> V040BoundaryInventory:
    version_by_boundary = {
        "mission_loop_boundary": "v0.40.0",
        "dry_run_boundary": "v0.40.0",
        "sandbox_rehearsal_boundary": "v0.40.1",
        "manual_checkpoint_boundary": "v0.40.2",
        "negative_runtime_gate_boundary": "v0.40.3",
        "scope_bound_approval_boundary": "v0.40.4",
        "prompt_submission_boundary": "v0.40.5",
        "provider_invocation_boundary": "v0.40.5",
        "provider_output_quarantine_boundary": "v0.40.5",
        "verifier_subagent_boundary": "v0.40.6",
        "evidence_matrix_boundary": "v0.40.7",
        "cli_preview_boundary": "v0.40.8",
        "restore_handoff_boundary": "v0.40.9",
        "standalone_runtime_closed_boundary": "v0.40.9",
    }
    boundaries = tuple(
        {
            "boundary_name": boundary,
            "owner_version": version_by_boundary[boundary],
            "owner_artifact": _stage_defaults().get(version_by_boundary[boundary], {}).get(
                "implementation", ("src/chanta_core/agent_runtime/repair_mission_loop_v040_consolidation.py",)
            )[0],
            "owner_test": _stage_defaults().get(version_by_boundary[boundary], {}).get(
                "tests", ("tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",)
            )[0],
            "owner_doc": _stage_defaults().get(version_by_boundary[boundary], {}).get(
                "docs", (INTEGRATED_DOC_PATH,)
            )[0],
            "status": "closed_runtime_boundary" if "closed" in boundary else "metadata_or_preview_boundary",
            "runtime_authority_granted": False,
        }
        for boundary in BOUNDARY_NAMES
    )
    defaults = {
        "inventory_id": "v040-boundary-inventory",
        "boundaries": boundaries,
        "all_major_boundaries_listed": len(boundaries) == len(BOUNDARY_NAMES),
        "runtime_authority_granted": False,
    }
    return V040BoundaryInventory(**_with_overrides(defaults, overrides))


def build_v040_safety_closure_register(**overrides: Any) -> V040SafetyClosureRegister:
    items = {
        surface: {
            "closed": True,
            "readiness_flag": False,
            "evidence_refs": ("V040CapabilityMatrix", "V0409ReadinessReport"),
            "withdrawal_condition": f"withdraw if {surface} becomes enabled in v0.40.9",
        }
        for surface in SAFETY_CLOSURE_SURFACES
    }
    defaults = {
        "register_id": "v040-safety-closure-register",
        "closure_items": items,
        "all_closures_confirmed": all(item["closed"] and item["readiness_flag"] is False for item in items.values()),
        "unsafe_readiness_true_count": sum(1 for item in items.values() if item["readiness_flag"] is True),
        "runtime_authority_granted": False,
    }
    return V040SafetyClosureRegister(**_with_overrides(defaults, overrides))


def build_v040_artifact_inventory(**overrides: Any) -> V040ArtifactInventory:
    modules = tuple(
        stage["implementation"][0]
        for stage in _stage_defaults().values()
    ) + ("src/chanta_core/agent_runtime/repair_mission_loop_v040_consolidation.py",)
    tests = tuple(stage["tests"][0] for stage in _stage_defaults().values()) + (
        "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
    )
    docs = tuple(stage["docs"][0] for stage in _stage_defaults().values()) + (INTEGRATED_DOC_PATH,)
    defaults = {
        "inventory_id": "v040-artifact-inventory",
        "implementation_modules": modules,
        "test_files": tests,
        "documentation_files": docs,
        "known_optional_docs": ("docs/versions/README.md",),
        "missing_or_advisory_only_items": ("prior aggregate test output is runtime-local evidence",),
    }
    return V040ArtifactInventory(**_with_overrides(defaults, overrides))


def build_v040_test_coverage_summary(**overrides: Any) -> V040TestCoverageSummary:
    defaults = {
        "summary_id": "v040-test-coverage-summary",
        "focused_v0409_test": "tests/test_v0409_controlled_mission_loop_preparation_consolidation_restore.py",
        "regression_v0408": "tests/test_v0408_cli_execution_test_preview_surface_restore.py",
        "regression_v0407": "tests/test_v0407_rehearsal_evidence_matrix_boundary_coverage_restore.py",
        "regression_v0406": "tests/test_v0406_verifier_subagent_boundary_deepening_restore.py",
        "regression_v0405": "tests/test_v0405_provider_prompt_boundary_deepening_restore.py",
        "regression_v0404": "tests/test_v0404_human_checkpoint_hardening_restore.py",
        "regression_v0403": "tests/test_v0403_negative_runtime_gate_regression.py",
        "regression_v0402": "tests/test_v0402_manual_two_iteration_rehearsal.py",
        "regression_v0401": "tests/test_v0401_sandbox_rehearsal_runner_standalone_readiness.py",
        "regression_v0400": "tests/test_v0400_controlled_multi_iteration_mission_loop_boundary.py",
        "regression_v0399": "tests/test_v0399_human_approved_sandbox_repair_apply_self_prompting_loop_consolidation.py",
        "aggregate_attempted": False,
        "skipped_or_not_run_reason": "set by verification run result outside this metadata module",
    }
    return V040TestCoverageSummary(**_with_overrides(defaults, overrides))


def build_v040_restore_index(**overrides: Any) -> V040RestoreIndex:
    docs = (
        "docs/versions/v0.40/v0.40.4_human_checkpoint_hardening_restore.md",
        "docs/versions/v0.40/v0.40.5_provider_prompt_boundary_deepening_restore.md",
        "docs/versions/v0.40/v0.40.6_verifier_subagent_boundary_deepening_restore.md",
        "docs/versions/v0.40/v0.40.7_rehearsal_evidence_matrix_boundary_coverage_restore.md",
        "docs/versions/v0.40/v0.40.8_cli_execution_test_preview_surface_restore.md",
        INTEGRATED_DOC_PATH,
    )
    defaults = {
        "index_id": "v040-restore-index",
        "restore_docs": docs,
        "integrated_restore_docs": docs[1:],
        "copy_paste_restore_prompt_exists": True,
        "capability_matrix_exists": True,
        "safety_flag_table_exists": True,
        "next_handoff_exists": True,
        "does_not_claim_standalone_runtime_opened": True,
    }
    return V040RestoreIndex(**_with_overrides(defaults, overrides))


def create_v040_standalone_runtime_still_closed_record(**overrides: Any) -> V040StandaloneRuntimeStillClosedRecord:
    return V040StandaloneRuntimeStillClosedRecord(**overrides)


def create_v041_required_runtime_component(
    component_name: str = "DefaultPersonalProfileRuntime",
    target_version: str = "v0.41.0",
    **overrides: Any,
) -> V041RequiredRuntimeComponent:
    _require_non_blank(component_name, "component_name")
    defaults = {
        "component_id": f"v041-component-{component_name.lower()}",
        "component_name": component_name,
        "required_for": "standalone Default Personal runtime",
        "current_status": "missing_in_v0409",
        "target_version": target_version,
        "blocking_if_missing": True,
        "safety_notes": ("v0.40.9 defines the gap only", "no v0.41 runtime is implemented here"),
        "evidence_refs": ("V041StandaloneRuntimeGapRegister", "V041DefaultPersonalStartupPlan"),
    }
    return V041RequiredRuntimeComponent(**_with_overrides(defaults, overrides))


def create_v041_standalone_runtime_gap(
    component_name: str = "DefaultPersonalProfileRuntime",
    target_version: str = "v0.41.0",
    **overrides: Any,
) -> V041StandaloneRuntimeGap:
    defaults = {
        "gap_id": f"v041-gap-{component_name.lower()}",
        "component_name": component_name,
        "missing": True,
        "blocking": True,
        "target_version": target_version,
        "evidence_refs": ("V041RequiredRuntimeComponent",),
        "note": "Required runtime component is future-gated beyond v0.40.9.",
    }
    return V041StandaloneRuntimeGap(**_with_overrides(defaults, overrides))


def build_v041_standalone_runtime_gap_register(**overrides: Any) -> V041StandaloneRuntimeGapRegister:
    version_targets = {
        "PersonalRoot": "v0.41.0",
        "DefaultPersonalProfileRuntime": "v0.41.0",
        "SoulRoleDomainPromptAssembly": "v0.41.2",
        "SessionStore": "v0.41.0",
        "UserInputSurface": "v0.41.1",
        "ChatServiceOrCLIEntry": "v0.41.1",
        "Orchestrator": "v0.41.4",
        "MinimalAgentLoop": "v0.41.4",
        "ReadOnlySkillRegistry": "v0.41.3",
        "SkillSelector": "v0.41.3",
        "ReadOnlySkillExecutor": "v0.41.3",
        "ObservationCollector": "v0.41.4",
        "ResponseRenderer": "v0.41.4",
        "EventTraceEmitter": "v0.41.5",
        "RestoreContextLoader": "v0.41.0",
        "SafetyBoundaryLoader": "v0.41.0",
        "V040CompatibilityGate": "v0.41.0",
        "DefaultPersonalSmokeScenario": "v0.41.6",
    }
    components = tuple(
        create_v041_required_runtime_component(name, version_targets[name])
        for name in REQUIRED_V041_COMPONENTS
    )
    gaps = tuple(create_v041_standalone_runtime_gap(name, version_targets[name]) for name in REQUIRED_V041_COMPONENTS)
    defaults = {
        "register_id": "v041-standalone-runtime-gap-register",
        "required_components": components,
        "gaps": gaps,
        "standalone_runtime_started": False,
        "ready_for_v041_runtime_execution": False,
        "ready_for_first_smoke_run": False,
        "no_v041_component_implemented_in_v0409": True,
    }
    return V041StandaloneRuntimeGapRegister(**_with_overrides(defaults, overrides))


def create_v041_default_personal_startup_plan(**overrides: Any) -> V041DefaultPersonalStartupPlan:
    stage_defs = (
        ("v0.41.0", "Default Personal Profile Runtime", ("DefaultPersonalProfileRuntime", "RestoreContextLoader", "SafetyBoundaryLoader")),
        ("v0.41.1", "User-facing CLI Entry", ("UserInputSurface", "ChatServiceOrCLIEntry")),
        ("v0.41.2", "Prompt Assembly / Soul-Role-Domain Binding", ("SoulRoleDomainPromptAssembly",)),
        ("v0.41.3", "Read-only Skill Registry", ("ReadOnlySkillRegistry", "SkillSelector", "ReadOnlySkillExecutor")),
        ("v0.41.4", "Minimal AgentLoop", ("Orchestrator", "MinimalAgentLoop", "ObservationCollector", "ResponseRenderer")),
        ("v0.41.5", "Event / Trace Emission", ("EventTraceEmitter",)),
        ("v0.41.6", "First Default Personal Smoke Run", ("DefaultPersonalSmokeScenario",)),
    )
    stages = tuple(
        {
            "target_version": version,
            "purpose": purpose,
            "required_artifacts": artifacts,
            "required_tests": tuple(f"test_{version.replace('.', '').replace('v', 'v')}_{artifact.lower()}" for artifact in artifacts),
            "opens": (purpose,),
            "still_closed": (
                "production_certification",
                "dominion_runtime",
                "live_workspace_apply",
                "unbounded_autonomous_runtime",
            ),
            "withdrawal_conditions": (
                "unsafe readiness flag becomes true",
                "provider, prompt, subagent, or live workspace authority opens outside scope",
            ),
        }
        for version, purpose, artifacts in stage_defs
    )
    defaults = {
        "plan_id": "v041-default-personal-startup-plan",
        "stages": stages,
        "recommended_sequence": tuple(version for version, _, _ in stage_defs),
    }
    return V041DefaultPersonalStartupPlan(**_with_overrides(defaults, overrides))


def create_v041_default_personal_smoke_scenario(**overrides: Any) -> V041DefaultPersonalSmokeScenario:
    defaults = {
        "scenario_id": "v041-default-personal-smoke-scenario-design",
        "input_text": "Vera, 현재 ChantaCore 상태를 요약하고 다음에 무엇을 해야 하는지 알려줘.",
        "expected_runtime_path": (
            "UserInput",
            "DefaultPersonalProfileRuntime",
            "PromptAssembly",
            "CLIEntry or ChatService entry",
            "Orchestrator",
            "MinimalAgentLoop",
            "ReadOnlySkillRegistry",
            "status_summary / restore_summary / trace_recent style read-only skill",
            "ObservationCollector",
            "ResponseRenderer",
            "EventTraceEmitter",
        ),
        "design_only": True,
        "executed": False,
        "marks_runtime_ready": False,
    }
    return V041DefaultPersonalSmokeScenario(**_with_overrides(defaults, overrides))


def create_v041_runtime_opening_gate(**overrides: Any) -> V041RuntimeOpeningGate:
    gates = {
        "profile_loaded": False,
        "prompt_assembled": False,
        "user_input_received": False,
        "entry_surface_available": False,
        "orchestrator_available": False,
        "agent_loop_available": False,
        "read_only_skill_registry_available": False,
        "read_only_skill_executor_available": False,
        "response_renderer_available": False,
        "event_trace_emitter_available": False,
        "safety_boundaries_loaded": False,
        "v040_unsafe_flags_false": True,
        "smoke_scenario_passed": False,
    }
    defaults = {
        "gate_id": "v041-runtime-opening-gate-design",
        "required_gates": gates,
        "design_targets_only": True,
        "current_v0409_runtime_opened": False,
    }
    return V041RuntimeOpeningGate(**_with_overrides(defaults, overrides))


def assess_v041_acceleration(
    missing_components: tuple[str, ...] = (
        "ProfileRuntime",
        "CLIEntry",
        "PromptAssembly",
        "AgentLoop",
        "ReadOnlySkillRegistry",
        "ReadOnlySkillExecutor",
        "ResponseRenderer",
        "EventTraceEmitter",
    ),
    **overrides: Any,
) -> V041AccelerationAssessment:
    missing = set(missing_components)
    if {
        "ProfileRuntime",
        "CLIEntry",
        "PromptAssembly",
        "AgentLoop",
        "ReadOnlySkillRegistry",
        "ReadOnlySkillExecutor",
        "ResponseRenderer",
        "EventTraceEmitter",
    }.issubset(missing):
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    elif {"ProfileRuntime", "CLIEntry", "PromptAssembly"}.isdisjoint(missing) and "ReadOnlySkillRegistry" in missing:
        earliest = "v0.41.5"
        recommendation = "possible_mild_acceleration"
    elif {"ProfileRuntime", "CLIEntry", "PromptAssembly", "ReadOnlySkillRegistry", "MinimalAgentLoop", "EventTraceEmitter"}.isdisjoint(missing):
        earliest = "v0.41.4"
        recommendation = "possible_acceleration_after_v0413"
    else:
        earliest = "v0.41.6"
        recommendation = "keep_conservative_target"
    defaults = {
        "assessment_id": "v041-acceleration-assessment-v0409",
        "earliest_candidate_target": earliest,
        "recommendation": recommendation,
        "missing_components": missing_components,
        "non_authoritative": True,
        "ready_for_standalone_default_personal_runtime": False,
    }
    return V041AccelerationAssessment(**_with_overrides(defaults, overrides))


def create_v0409_consolidation_audit_record(**overrides: Any) -> V0409ConsolidationAuditRecord:
    defaults = {
        "audit_id": "v0409-consolidation-audit",
        "all_v040_stages_summarized": True,
        "all_major_boundaries_inventoried": True,
        "all_unsafe_runtime_capabilities_closed": True,
        "restore_index_complete": True,
        "v041_gap_register_produced": True,
        "v041_startup_plan_produced": True,
        "no_runtime_expansion_introduced": True,
        "no_standalone_runtime_opened": True,
        "no_production_certification_claimed": True,
    }
    return V0409ConsolidationAuditRecord(**_with_overrides(defaults, overrides))


def create_v0409_safety_report(**overrides: Any) -> V0409SafetyReport:
    closure = build_v040_safety_closure_register()
    defaults = {
        "report_id": "v0409-safety-report",
        "safe_for_v0409_consolidation": closure.all_closures_confirmed and closure.unsafe_readiness_true_count == 0,
        "safe_for_runtime_execution": False,
        "safe_for_cli_runtime_execution": False,
        "safe_for_live_workspace_apply": False,
        "safe_for_prompt_submission": False,
        "safe_for_model_provider_invocation": False,
        "safe_for_subagent_invocation": False,
        "safe_for_child_session_creation": False,
        "safe_for_parent_raw_transcript_sharing": False,
        "safe_for_network_access": False,
        "safe_for_credential_access": False,
        "safe_for_standalone_default_personal_runtime": False,
        "safe_for_dominion_runtime": False,
        "production_certified": False,
        "ready_for_v041_design_handoff": True,
    }
    return V0409SafetyReport(**_with_overrides(defaults, overrides))


def create_v0409_readiness_report(**overrides: Any) -> V0409ReadinessReport:
    defaults = {
        "report_id": "v0409-readiness-report",
        "v040_final_consolidation_defined": True,
        "v040_capability_matrix_ready": True,
        "v040_boundary_inventory_ready": True,
        "v040_safety_closure_register_ready": True,
        "v040_artifact_inventory_ready": True,
        "v040_test_coverage_summary_ready": True,
        "v040_restore_index_ready": True,
        "v041_gap_register_ready": True,
        "v041_startup_plan_ready": True,
        "v041_smoke_scenario_defined": True,
        "v041_handoff_ready": True,
        "integrated_restore_document_ready": True,
        **{flag: False for flag in REQUIRED_FALSE_FLAGS},
    }
    return V0409ReadinessReport(**_with_overrides(defaults, overrides))


def create_v0409_integrated_restore_sections() -> tuple[V0409IntegratedRestoreSection, ...]:
    return tuple(
        V0409IntegratedRestoreSection(
            section_id=section_id,
            title=section_id.replace("_", " ").title(),
            required=True,
            content_summary=f"{section_id} is required for v0.40.9 integrated restore.",
            restore_value=f"restore:{section_id}",
        )
        for section_id in REQUIRED_RESTORE_SECTION_IDS
    )


def create_v0409_integrated_restore_context_snapshot(**overrides: Any) -> V0409IntegratedRestoreContextSnapshot:
    inventory = build_v040_artifact_inventory()
    defaults = {
        "snapshot_id": "integrated-restore-snapshot-v0409",
        "current_version": V0409_RELEASE_NAME,
        "current_track": V0409_TRACK_NAME,
        "baseline_versions": BASELINE_VERSIONS,
        "implemented_modules": inventory.implementation_modules,
        "test_files": inventory.test_files,
        "docs": inventory.documentation_files,
        "open_capabilities": SNAPSHOT_OPEN_CAPABILITIES,
        "closed_capabilities": CLOSED_RUNTIME_CAPABILITIES,
        "next_recommended_version": "v0.41.0 Default Personal Profile Runtime",
        "next_recommended_focus": "Profile runtime plus restore and safety loading only, without full AgentLoop or smoke run",
    }
    return V0409IntegratedRestoreContextSnapshot(**_with_overrides(defaults, overrides))


def create_v0409_integrated_restore_packet(**overrides: Any) -> V0409IntegratedRestorePacket:
    defaults = {
        "restore_packet_id": "integrated-restore-packet-v0409",
        "snapshot": create_v0409_integrated_restore_context_snapshot(),
        "restore_sections": create_v0409_integrated_restore_sections(),
        "required_test_commands": (
            "focused_v0409_consolidation",
            "v0408_cli_preview_regression",
            "v0407_evidence_matrix_regression",
            "v0406_verifier_subagent_regression",
            "v0405_provider_prompt_regression",
            "v0404_checkpoint_hardening_regression",
            "v0403_negative_gate_regression",
            "v0402_manual_checkpoint_regression",
            "v0401_sandbox_rehearsal_regression",
            "v0400_boundary_regression",
            "v0399_sandbox_repair_regression",
        ),
        "required_false_flags": REQUIRED_FALSE_FLAGS,
        "restore_prompt_summary": "Continue ChantaCore after final v0.40 consolidation into v0.41.0 profile runtime design.",
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0409IntegratedRestorePacket(**_with_overrides(defaults, overrides))


def create_v0409_integrated_restore_document_manifest(**overrides: Any) -> V0409IntegratedRestoreDocumentManifest:
    defaults = {
        "manifest_id": "integrated-restore-document-manifest-v0409",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": False,
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": True,
        "suitable_for_new_session_handoff": True,
    }
    return V0409IntegratedRestoreDocumentManifest(**_with_overrides(defaults, overrides))


def create_v0410_default_personal_profile_runtime_handoff(**overrides: Any) -> V0410DefaultPersonalProfileRuntimeHandoff:
    defaults = {
        "handoff_id": "v0410-default-personal-profile-runtime-handoff",
        "target_version": "v0.41.0 Default Personal Profile Runtime",
        "recommended_focus": (
            "create DefaultPersonalProfileRuntime artifact",
            "define personal root and profile config",
            "load soul/role/domain/profile metadata",
            "define profile runtime state without AgentLoop execution",
            "define restore context loader",
            "define safety boundary loader",
            "define v0.40 compatibility gate",
            "no model/provider invocation unless explicitly scoped later",
            "no autonomous loop",
            "no live workspace apply",
            "no production certification",
        ),
        "required_inputs_from_v0409": (
            "V040CapabilityMatrix",
            "V040SafetyClosureRegister",
            "V041StandaloneRuntimeGapRegister",
            "V041DefaultPersonalStartupPlan",
            "V0409IntegratedRestorePacket",
        ),
        "still_closed": CLOSED_RUNTIME_CAPABILITIES,
        "risk_notes": (
            "v0.41.0 should start with profile runtime and restore/safety loading only",
            "full AgentLoop and first smoke run remain later gates",
        ),
    }
    return V0410DefaultPersonalProfileRuntimeHandoff(**_with_overrides(defaults, overrides))


def v040_capability_matrix_is_not_permission_grant(matrix: V040CapabilityMatrix) -> bool:
    return matrix.permission_grant is False and matrix.production_certified is False


def v040_boundary_inventory_preserves_no_runtime_authority(inventory: V040BoundaryInventory) -> bool:
    return inventory.runtime_authority_granted is False and all(
        boundary["runtime_authority_granted"] is False for boundary in inventory.boundaries
    )


def v040_safety_closure_register_preserves_closed(register: V040SafetyClosureRegister) -> bool:
    return (
        register.all_closures_confirmed
        and register.unsafe_readiness_true_count == 0
        and register.runtime_authority_granted is False
    )


def v040_standalone_runtime_record_preserves_closed(record: V040StandaloneRuntimeStillClosedRecord) -> bool:
    return all(value is False for key, value in record.__dict__.items() if key.endswith("_opened"))


def v041_gap_register_is_design_only(register: V041StandaloneRuntimeGapRegister) -> bool:
    return (
        register.standalone_runtime_started is False
        and register.ready_for_v041_runtime_execution is False
        and register.ready_for_first_smoke_run is False
        and register.no_v041_component_implemented_in_v0409 is True
    )


def v041_smoke_scenario_is_not_executed(scenario: V041DefaultPersonalSmokeScenario) -> bool:
    return scenario.design_only and not scenario.executed and not scenario.marks_runtime_ready


def v041_runtime_opening_gate_is_design_only(gate: V041RuntimeOpeningGate) -> bool:
    return gate.design_targets_only and gate.current_v0409_runtime_opened is False


def v041_acceleration_assessment_is_non_authoritative(assessment: V041AccelerationAssessment) -> bool:
    return assessment.non_authoritative and assessment.ready_for_standalone_default_personal_runtime is False


def v0409_readiness_preserves_no_unsafe_runtime(report: V0409ReadinessReport) -> bool:
    return all(getattr(report, flag) is False for flag in REQUIRED_FALSE_FLAGS)


def integrated_restore_packet_uses_single_doc(packet: V0409IntegratedRestorePacket) -> bool:
    return packet.single_integrated_doc_path == INTEGRATED_DOC_PATH and packet.separate_restore_doc_created is False


__all__ = [
    "BASELINE_VERSIONS",
    "BOUNDARY_NAMES",
    "CLOSED_RUNTIME_CAPABILITIES",
    "INTEGRATED_DOC_PATH",
    "OPEN_METADATA_PREVIEW_CAPABILITIES",
    "REQUIRED_FALSE_FLAGS",
    "REQUIRED_RESTORE_SECTION_IDS",
    "REQUIRED_V041_COMPONENTS",
    "SAFETY_CLOSURE_SURFACES",
    "SNAPSHOT_OPEN_CAPABILITIES",
    "V0409_RELEASE_NAME",
    "V0409_TRACK_NAME",
    "V0409_VERSION",
    "BoundaryCoverageReadinessReport",
    "CheckpointHardeningReadinessReport",
    "CLIExecutionTestPreviewSurface",
    "CLIPreviewSurfaceReadinessReport",
    "DefaultPersonalStandaloneGapRegister",
    "DeniedRuntimeActionCoverageMatrix",
    "HumanCheckpointGate",
    "IterationState",
    "LoopBudgetGate",
    "ManualTwoIterationReadinessReport",
    "MissionLoopEnvelope",
    "NegativeRuntimeGateReadinessReport",
    "NoAutonomousContinuationGuarantee",
    "PromptSubmissionBoundary",
    "ProviderBoundaryGate",
    "ProviderPromptBoundaryReadinessReport",
    "RehearsalEvidenceMatrix",
    "SandboxRehearsalReadinessReport",
    "StandaloneRuntimeStillClosedRecord",
    "StopConditionContract",
    "V0404RestorePacket",
    "V0405IntegratedRestorePacket",
    "V0406IntegratedRestorePacket",
    "V0407IntegratedRestorePacket",
    "V0408IntegratedRestorePacket",
    "V040ArtifactInventory",
    "V040BoundaryInventory",
    "V040CapabilityMatrix",
    "V040ConsolidationReadinessLevel",
    "V040ConsolidationStatus",
    "V040RestoreIndex",
    "V040SafetyClosureRegister",
    "V040StageSummary",
    "V040StandaloneRuntimeStillClosedRecord",
    "V040TestCoverageSummary",
    "V040ReadinessReport",
    "V0409ConsolidationAuditRecord",
    "V0409IntegratedRestoreContextSnapshot",
    "V0409IntegratedRestoreDocumentManifest",
    "V0409IntegratedRestorePacket",
    "V0409IntegratedRestoreSection",
    "V0409ReadinessReport",
    "V0409SafetyReport",
    "V0410DefaultPersonalProfileRuntimeHandoff",
    "V041AccelerationAssessment",
    "V041DefaultPersonalSmokeScenario",
    "V041DefaultPersonalStartupPlan",
    "V041RequiredRuntimeComponent",
    "V041RuntimeOpeningGate",
    "V041StandaloneRuntimeGap",
    "V041StandaloneRuntimeGapRegister",
    "VerifierSubagentBoundary",
    "VerifierSubagentBoundaryReadinessReport",
    "assess_v041_acceleration",
    "build_v040_artifact_inventory",
    "build_v040_boundary_inventory",
    "build_v040_capability_matrix",
    "build_v040_restore_index",
    "build_v040_safety_closure_register",
    "build_v040_stage_summaries",
    "build_v040_test_coverage_summary",
    "build_v041_standalone_runtime_gap_register",
    "create_v040_stage_summary",
    "create_v040_standalone_runtime_still_closed_record",
    "create_v0409_consolidation_audit_record",
    "create_v0409_integrated_restore_context_snapshot",
    "create_v0409_integrated_restore_document_manifest",
    "create_v0409_integrated_restore_packet",
    "create_v0409_integrated_restore_sections",
    "create_v0409_readiness_report",
    "create_v0409_safety_report",
    "create_v0410_default_personal_profile_runtime_handoff",
    "create_v041_default_personal_smoke_scenario",
    "create_v041_default_personal_startup_plan",
    "create_v041_required_runtime_component",
    "create_v041_runtime_opening_gate",
    "create_v041_standalone_runtime_gap",
    "integrated_restore_packet_uses_single_doc",
    "v0409_readiness_preserves_no_unsafe_runtime",
    "v040_boundary_inventory_preserves_no_runtime_authority",
    "v040_capability_matrix_is_not_permission_grant",
    "v040_safety_closure_register_preserves_closed",
    "v040_standalone_runtime_record_preserves_closed",
    "v041_acceleration_assessment_is_non_authoritative",
    "v041_gap_register_is_design_only",
    "v041_runtime_opening_gate_is_design_only",
    "v041_smoke_scenario_is_not_executed",
]
