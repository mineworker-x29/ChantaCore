from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0359_VERSION = "v0.35.9"
V0359_RELEASE_NAME = "v0.35.9 Controlled Patch Proposal Layer Consolidation"
CONTROLLED_PATCH_PROPOSAL_LAYER_V1 = "Controlled Patch Proposal Layer v1"

V035_INCLUDED_VERSIONS = [
    "v0.35.0",
    "v0.35.1",
    "v0.35.2",
    "v0.35.3",
    "v0.35.4",
    "v0.35.5",
    "v0.35.6",
    "v0.35.7",
    "v0.35.8",
]

DEFAULT_INCLUDED_MODULES = [
    "src/chanta_core/agent_runtime/patch_proposal_boundary.py",
    "src/chanta_core/agent_runtime/patch_intent.py",
    "src/chanta_core/agent_runtime/patch_context.py",
    "src/chanta_core/agent_runtime/patch_plan.py",
    "src/chanta_core/agent_runtime/patch_diff_proposal.py",
    "src/chanta_core/agent_runtime/patch_risk.py",
    "src/chanta_core/agent_runtime/patch_review.py",
    "src/chanta_core/agent_runtime/patch_ocel_trace.py",
    "src/chanta_core/agent_runtime/patch_cli_surface.py",
]

DEFAULT_INCLUDED_DOCS = [
    "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md",
    "docs/versions/v0.35/v0.35.1_patch_intent_scope_policy.md",
    "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md",
    "docs/versions/v0.35/v0.35.3_reference_informed_patch_plan_change_set_graph.md",
    "docs/versions/v0.35/v0.35.4_diff_proposal_envelope.md",
    "docs/versions/v0.35/v0.35.5_patch_risk_conformance_scanner.md",
    "docs/versions/v0.35/v0.35.6_human_review_packet_approval_gate_metadata.md",
    "docs/versions/v0.35/v0.35.7_patch_proposal_ocel_trace_packet.md",
    "docs/versions/v0.35/v0.35.8_cli_patch_proposal_surface.md",
]

DEFAULT_INCLUDED_TESTS = [
    "tests/test_v0350_controlled_patch_proposal_boundary.py",
    "tests/test_v0351_patch_intent_scope_policy.py",
    "tests/test_v0352_readonly_patch_context_collector.py",
    "tests/test_v0353_reference_informed_patch_plan.py",
    "tests/test_v0354_diff_proposal_envelope.py",
    "tests/test_v0355_patch_risk_conformance_scanner.py",
    "tests/test_v0356_human_review_packet_approval_gate_metadata.py",
    "tests/test_v0357_patch_proposal_ocel_trace_packet.py",
    "tests/test_v0358_cli_patch_proposal_surface.py",
]

DEFAULT_CONTROLLED_CAPABILITIES = [
    "controlled patch proposal boundary definition",
    "ReferencePatternDigest read-only digestion",
    "patch intent and scope metadata",
    "read-only patch context snapshots",
    "reference-informed patch plan metadata",
    "diff proposal envelope artifacts",
    "patch risk and conformance reports",
    "human review packet metadata",
    "returned patch proposal trace packets",
    "CLI patch proposal preview surface",
]

DEFAULT_BOUNDED_CAPABILITIES = [
    "bounded unified diff proposal text",
    "structured patch proposal metadata",
    "patch file proposal metadata",
    "patch hunk proposal metadata",
    "safety regression scan metadata",
    "scope violation scan metadata",
    "approval gate metadata without apply permission",
    "Digestion-first / Dominion-fallback metadata",
    "external-agent-control pattern blocked/future-gated metadata",
]

DEFAULT_PROHIBITED_CAPABILITIES = [
    "patch application",
    "workspace write",
    "code edit",
    "apply_patch runtime call",
    "git apply runtime call",
    "test execution",
    "shell execution",
    "subprocess execution",
    "command execution",
    "dependency install",
    "reference execution",
    "reference import",
    "external agent execution",
    "Claude Code invocation",
    "Codex CLI invocation",
    "Dominion runtime",
    "infinite agent loop",
    "provider invocation",
    "direct network access",
    "credential access",
    "secret read",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
    "D4-D9 authority grant",
]

DEFAULT_PROHIBITED_RUNTIME_SURFACES = [
    "patch_application",
    "workspace_write",
    "code_edit",
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
    "infinite_agent_loop",
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

DEFAULT_FUTURE_TRACK_ITEMS = [
    "human-approved patch apply sandbox",
    "dry-run apply simulation",
    "rollback plan",
    "controlled test runner",
    "persistent trace store",
    "UI runtime",
    "external harness adapter",
    "Dominion runtime gated review",
]

DEFAULT_WITHDRAWAL_CONDITIONS = [
    "Any patch application, workspace write, code edit, apply_patch, or git apply path is introduced.",
    "Any shell, subprocess, command, test execution, dependency install, provider, network, credential, or secret path is introduced.",
    "Any reference execution/import, external agent invocation, Dominion runtime, infinite loop, persistent trace, UI runtime, or authority grant is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

UNSAFE_RELEASE_FLAG_NAMES = (
    "ready_for_execution",
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
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)

REPORT_UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
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
    "ready_for_general_tool_execution",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
    "production_certified",
)


class ControlledPatchProposalConsolidationStatus(StrEnum):
    UNKNOWN = "unknown"
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    CONSOLIDATED = "consolidated"
    CONSOLIDATED_WITH_GAPS = "consolidated_with_gaps"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ControlledPatchProposalConsolidationReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    CONTRACT_READY = "contract_ready"
    CONTROLLED_PATCH_PROPOSAL_LAYER_READY = "controlled_patch_proposal_layer_ready"
    PATCH_PROPOSAL_ARTIFACT_READY = "patch_proposal_artifact_ready"
    REVIEW_PACKET_READY = "review_packet_ready"
    CLI_PATCH_SURFACE_READY = "cli_patch_surface_ready"
    HANDOFF_READY_FOR_V036 = "handoff_ready_for_v036"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0359_VERSION not in version:
        raise ValueError("version must include v0.35.9")


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.9")


def _validate_true(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(instance, name) is not True:
            raise ValueError(f"{name} must be True for successful v0.35.9 consolidation")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret", "credential", "api_key", "token")):
            raise ValueError("metadata keys must not request credential or secret material")


def _validate_includes_v035_versions(values: list[str]) -> None:
    _validate_string_list("included_versions", values)
    missing = [version for version in V035_INCLUDED_VERSIONS if version not in values]
    if missing:
        raise ValueError(f"included_versions must include v0.35.0 through v0.35.8: {missing}")


@dataclass(frozen=True)
class ControlledPatchProposalReleaseFlagSet:
    flag_set_id: str
    version: str
    controlled_patch_proposal_layer_v1_ready: bool
    ready_for_v036_handoff: bool
    ready_for_patch_intent_scope_policy: bool
    ready_for_reference_pattern_digest: bool
    ready_for_readonly_patch_context_collection: bool
    ready_for_patch_context_snapshot: bool
    ready_for_reference_informed_patch_plan: bool
    ready_for_change_set_graph: bool
    ready_for_diff_proposal_artifact: bool
    ready_for_unified_diff_proposal: bool
    ready_for_structured_patch_proposal: bool
    ready_for_patch_hunk_proposal: bool
    ready_for_patch_risk_conformance_scan: bool
    ready_for_patch_safety_regression_scan: bool
    ready_for_patch_scope_violation_scan: bool
    ready_for_human_review_packet: bool
    ready_for_approval_gate_metadata: bool
    ready_for_patch_proposal_trace_packet_creation: bool
    ready_for_bounded_patch_proposal_ocel_trace_emission: bool
    ready_for_cli_patch_proposal_surface: bool
    ready_for_bounded_cli_patch_proposal_preview: bool
    ready_for_digestion_dominion_trace_metadata: bool
    ready_for_external_agent_control_pattern_trace: bool
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
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
        if self.max_grantable_level not in {None, "D0", "D1", "D2", "D3", "D3_SIMULATE"}:
            raise ValueError("max_grantable_level must be None or <= D3_SIMULATE")
        for level in ("D4", "D5", "D6", "D7", "D8", "D9"):
            if level not in self.future_track_levels:
                raise ValueError("D4-D9 must remain future-track levels")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalSnapshot:
    snapshot_id: str
    version: str
    release_name: str
    included_versions: list[str]
    included_modules: list[str]
    included_artifact_groups: list[str]
    release_flags: ControlledPatchProposalReleaseFlagSet
    consolidation_status: ControlledPatchProposalConsolidationStatus | str
    readiness_level: ControlledPatchProposalConsolidationReadinessLevel | str
    summary: str
    controlled_capabilities: list[str]
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
        if CONTROLLED_PATCH_PROPOSAL_LAYER_V1 not in self.release_name:
            raise ValueError("release_name should be Controlled Patch Proposal Layer v1")
        _validate_includes_v035_versions(self.included_versions)
        for name in ("included_modules", "included_artifact_groups", "controlled_capabilities", "prohibited_capabilities", "evidence_refs", "known_gaps", "known_risks", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if not controlled_patch_proposal_flags_preserve_no_apply(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        ControlledPatchProposalConsolidationStatus(self.consolidation_status)
        ControlledPatchProposalConsolidationReadinessLevel(self.readiness_level)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalCapabilityMatrix:
    capability_matrix_id: str
    version: str
    enabled_controlled_capabilities: list[str]
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
        for name in ("enabled_controlled_capabilities", "enabled_bounded_capabilities", "design_stage_capabilities", "prohibited_capabilities", "future_track_capabilities", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        for name in ("capability_to_version", "prohibited_capability_to_reason"):
            _validate_dict(name, getattr(self, name))
        for required in DEFAULT_PROHIBITED_CAPABILITIES:
            if required not in self.prohibited_capabilities:
                raise ValueError(f"prohibited_capabilities missing {required}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalStageCoverage:
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
        for name in ("covered_artifact_refs", "missing_artifact_refs", "covered_test_refs", "missing_test_refs", "covered_doc_refs", "missing_doc_refs", "coverage_notes", "blocking_gaps", "non_blocking_gaps", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        if self.coverage_complete and self.blocking_gaps:
            raise ValueError("coverage_complete cannot be True with blocking gaps")
        _validate_metadata_safe(self.metadata)


class PatchBoundaryCoverage(ControlledPatchProposalStageCoverage):
    pass


class ReferenceDigestCoverage(ControlledPatchProposalStageCoverage):
    pass


class PatchIntentScopeCoverage(ControlledPatchProposalStageCoverage):
    pass


class PatchContextCoverage(ControlledPatchProposalStageCoverage):
    pass


class PatchPlanCoverage(ControlledPatchProposalStageCoverage):
    pass


class DiffProposalCoverage(ControlledPatchProposalStageCoverage):
    pass


class PatchRiskCoverage(ControlledPatchProposalStageCoverage):
    pass


class PatchReviewCoverage(ControlledPatchProposalStageCoverage):
    pass


class PatchProposalTraceCoverage(ControlledPatchProposalStageCoverage):
    pass


class CLIPatchProposalSurfaceCoverage(ControlledPatchProposalStageCoverage):
    pass


@dataclass(frozen=True)
class ControlledPatchProposalBoundaryRegister:
    boundary_register_id: str
    version: str
    inherited_boundaries: list[str]
    active_controlled_boundaries: list[str]
    active_bounded_boundaries: list[str]
    prohibited_boundaries: list[str]
    future_gate_boundaries: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("boundary_register_id", self.boundary_register_id)
        _validate_version(self.version)
        for name in ("inherited_boundaries", "active_controlled_boundaries", "active_bounded_boundaries", "prohibited_boundaries", "future_gate_boundaries", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        required = ["patch_apply", "workspace_write", "code_edit", "apply_patch", "git_apply", "test_execution", "shell", "subprocess", "command", "dependency_install", "reference_execution", "reference_import", "external_agent_execution", "claude_code_invocation", "codex_cli_invocation", "dominion_runtime", "infinite_agent_loop", "provider_invocation", "direct_network", "credential_access", "secret_read", "persistent_trace", "UI_runtime", "external_control", "authority_grant"]
        for item in required:
            if item not in self.prohibited_boundaries:
                raise ValueError(f"prohibited_boundaries missing {item}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalRiskRegister:
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
        for name in ("known_risks", "high_risk_surfaces", "prohibited_runtime_surfaces", "mitigations", "unresolved_risks", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        for item in DEFAULT_PROHIBITED_RUNTIME_SURFACES:
            if item not in self.prohibited_runtime_surfaces:
                raise ValueError(f"prohibited_runtime_surfaces missing {item}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalGapRegister:
    gap_register_id: str
    version: str
    blocking_gaps: list[str]
    non_blocking_gaps: list[str]
    future_track_items: list[str]
    recommended_v036_items: list[str]
    recommended_later_items: list[str]
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("gap_register_id", self.gap_register_id)
        _validate_version(self.version)
        for name in ("blocking_gaps", "non_blocking_gaps", "future_track_items", "recommended_v036_items", "recommended_later_items", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        for item in DEFAULT_FUTURE_TRACK_ITEMS:
            if item not in self.future_track_items:
                raise ValueError(f"future_track_items missing {item}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalReleaseManifest:
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
    release_flags: ControlledPatchProposalReleaseFlagSet
    known_gaps: list[str]
    known_risks: list[str]
    next_handoff_id: str | None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("release_manifest_id", "release_name", "snapshot_id", "focused_test_command", "full_track_test_command"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_includes_v035_versions(self.included_versions)
        for name in ("included_modules", "included_docs", "included_tests", "known_gaps", "known_risks"):
            _validate_string_list(name, getattr(self, name))
        if not controlled_patch_proposal_flags_preserve_no_apply(self.release_flags):
            raise ValueError("release_flags must preserve unsafe readiness false")
        if self.next_handoff_id is not None:
            _require_non_blank("next_handoff_id", self.next_handoff_id)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ControlledPatchProposalAuditTrail:
    audit_trail_id: str
    version: str
    reviewed_artifact_refs: list[str]
    reviewed_test_refs: list[str]
    reviewed_doc_refs: list[str]
    boundary_checks: list[str]
    negative_runtime_checks: list[str]
    controlled_capability_checks: list[str]
    no_patch_application_confirmed: bool = True
    no_workspace_write_confirmed: bool = True
    no_code_edit_confirmed: bool = True
    no_apply_patch_confirmed: bool = True
    no_git_apply_confirmed: bool = True
    no_test_execution_confirmed: bool = True
    no_shell_execution_confirmed: bool = True
    no_subprocess_execution_confirmed: bool = True
    no_command_execution_confirmed: bool = True
    no_dependency_install_confirmed: bool = True
    no_reference_execution_confirmed: bool = True
    no_reference_import_confirmed: bool = True
    no_external_agent_execution_confirmed: bool = True
    no_claude_code_invocation_confirmed: bool = True
    no_codex_cli_invocation_confirmed: bool = True
    no_dominion_runtime_confirmed: bool = True
    no_infinite_agent_loop_confirmed: bool = True
    no_provider_invocation_confirmed: bool = True
    no_direct_network_access_confirmed: bool = True
    no_credential_access_confirmed: bool = True
    no_secret_read_confirmed: bool = True
    no_general_agent_execution_confirmed: bool = True
    no_autonomous_agent_runtime_confirmed: bool = True
    no_general_tool_execution_confirmed: bool = True
    no_unquarantined_action_execution_confirmed: bool = True
    no_persistent_trace_write_confirmed: bool = True
    no_external_trace_sink_confirmed: bool = True
    no_ui_runtime_confirmed: bool = True
    no_external_control_confirmed: bool = True
    no_authority_grant_confirmed: bool = True
    no_d4_d9_grant_confirmed: bool = True
    unsafe_readiness_flags_false_confirmed: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("audit_trail_id", self.audit_trail_id)
        _validate_version(self.version)
        for name in ("reviewed_artifact_refs", "reviewed_test_refs", "reviewed_doc_refs", "boundary_checks", "negative_runtime_checks", "controlled_capability_checks", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") or name == "unsafe_readiness_flags_false_confirmed":
                if getattr(self, name) is not True:
                    raise ValueError(f"{name} must be True for successful consolidation")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class DigestionDominionConsolidationRecord:
    digestion_consolidation_id: str
    version: str
    digestion_first_policy_confirmed: bool
    dominion_fallback_future_gated: bool
    external_agent_patterns_recorded: bool
    external_agent_execution_blocked: bool
    infinite_loop_blocked: bool
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
        _validate_true(self, ("digestion_first_policy_confirmed", "dominion_fallback_future_gated", "external_agent_execution_blocked", "infinite_loop_blocked", "dominion_runtime_blocked"))
        for name in ("safely_digested_items", "rejected_dominion_like_items", "future_track_dominion_items"):
            _validate_string_list(name, getattr(self, name))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ExternalAgentControlPatternConsolidationRecord:
    external_agent_record_id: str
    version: str
    observed_pattern_kinds: list[str]
    blocked_pattern_kinds: list[str]
    future_gated_pattern_kinds: list[str]
    denied_cli_commands: list[str]
    risk_notes: list[str]
    execution_allowed: bool
    dominion_runtime_allowed: bool
    infinite_loop_allowed: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("external_agent_record_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in ("observed_pattern_kinds", "blocked_pattern_kinds", "future_gated_pattern_kinds", "denied_cli_commands", "risk_notes"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("execution_allowed", "dominion_runtime_allowed", "infinite_loop_allowed"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V036HandoffPacket:
    handoff_id: str
    source_version: str
    target_version_track: str
    source_snapshot_id: str
    release_manifest_id: str | None
    recommended_next_track: str
    recommended_next_release: str
    human_approved_patch_apply_sandbox_items: list[str]
    dry_run_apply_simulation_items: list[str]
    apply_sandbox_policy_items: list[str]
    rollback_plan_items: list[str]
    human_confirmation_items: list[str]
    reusable_intent_scope_items: list[str]
    reusable_context_items: list[str]
    reusable_plan_items: list[str]
    reusable_diff_items: list[str]
    reusable_risk_items: list[str]
    reusable_review_items: list[str]
    reusable_trace_items: list[str]
    reusable_cli_items: list[str]
    required_new_boundaries: list[str]
    prohibited_until_later_gate: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    readiness_level: ControlledPatchProposalConsolidationReadinessLevel | str
    ready_for_v036: bool
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("handoff_id", "source_version", "target_version_track", "source_snapshot_id", "recommended_next_track", "recommended_next_release"):
            _require_non_blank(name, getattr(self, name))
        if V0359_VERSION not in self.source_version:
            raise ValueError("source_version must include v0.35.9")
        if "v0.36" not in self.target_version_track:
            raise ValueError("target_version_track should refer to v0.36")
        if "Human-approved Patch Apply Sandbox" not in self.recommended_next_track:
            raise ValueError("recommended_next_track should mention Human-approved Patch Apply Sandbox")
        if self.release_manifest_id is not None:
            _require_non_blank("release_manifest_id", self.release_manifest_id)
        for name in ("human_approved_patch_apply_sandbox_items", "dry_run_apply_simulation_items", "apply_sandbox_policy_items", "rollback_plan_items", "human_confirmation_items", "reusable_intent_scope_items", "reusable_context_items", "reusable_plan_items", "reusable_diff_items", "reusable_risk_items", "reusable_review_items", "reusable_trace_items", "reusable_cli_items", "required_new_boundaries", "prohibited_until_later_gate", "future_track_items", "evidence_refs"):
            _validate_string_list(name, getattr(self, name))
        ControlledPatchProposalConsolidationReadinessLevel(self.readiness_level)
        _validate_false(self, ("ready_for_execution", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_apply_patch", "ready_for_git_apply"))
        required = ["patch application", "workspace write", "code edit", "apply_patch", "git apply", "shell", "command", "test execution", "dependency install", "direct provider", "direct network", "credential access", "external agent execution", "Dominion runtime", "infinite loop", "UI runtime", "authority grant"]
        for item in required:
            if item not in self.prohibited_until_later_gate:
                raise ValueError(f"prohibited_until_later_gate missing {item}")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V035ConsolidationReport:
    report_id: str
    version: str
    release_name: str
    snapshot_id: str
    release_manifest_id: str
    handoff_id: str | None
    consolidation_status: ControlledPatchProposalConsolidationStatus | str
    readiness_level: ControlledPatchProposalConsolidationReadinessLevel | str
    summary: str
    completed_items: list[str]
    controlled_enabled_items: list[str]
    bounded_enabled_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    runtime_not_ready_items: list[str]
    v036_handoff_summary: str
    ready_for_v036: bool
    ready_for_controlled_patch_proposal_layer_v1: bool
    ready_for_patch_intent_scope_policy: bool
    ready_for_readonly_patch_context_collection: bool
    ready_for_reference_informed_patch_plan: bool
    ready_for_diff_proposal_artifact: bool
    ready_for_patch_risk_conformance_scan: bool
    ready_for_human_review_packet: bool
    ready_for_patch_proposal_trace_packet_creation: bool
    ready_for_cli_patch_proposal_surface: bool
    ready_for_execution: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    ready_for_external_agent_execution: bool = False
    ready_for_claude_code_invocation: bool = False
    ready_for_codex_cli_invocation: bool = False
    ready_for_dominion_runtime: bool = False
    ready_for_infinite_agent_loop: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "release_name", "snapshot_id", "release_manifest_id", "summary", "v036_handoff_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.handoff_id is not None:
            _require_non_blank("handoff_id", self.handoff_id)
        ControlledPatchProposalConsolidationStatus(self.consolidation_status)
        ControlledPatchProposalConsolidationReadinessLevel(self.readiness_level)
        for name in ("completed_items", "controlled_enabled_items", "bounded_enabled_items", "blocked_items", "future_track_items", "runtime_not_ready_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, REPORT_UNSAFE_FLAG_NAMES)
        _validate_metadata_safe(self.metadata)


def build_controlled_patch_proposal_release_flags(flag_set_id: str = "controlled_patch_release_flags:v0.35.9", **kwargs: Any) -> ControlledPatchProposalReleaseFlagSet:
    return ControlledPatchProposalReleaseFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0359_VERSION),
        controlled_patch_proposal_layer_v1_ready=kwargs.pop("controlled_patch_proposal_layer_v1_ready", True),
        ready_for_v036_handoff=kwargs.pop("ready_for_v036_handoff", True),
        ready_for_patch_intent_scope_policy=kwargs.pop("ready_for_patch_intent_scope_policy", True),
        ready_for_reference_pattern_digest=kwargs.pop("ready_for_reference_pattern_digest", True),
        ready_for_readonly_patch_context_collection=kwargs.pop("ready_for_readonly_patch_context_collection", True),
        ready_for_patch_context_snapshot=kwargs.pop("ready_for_patch_context_snapshot", True),
        ready_for_reference_informed_patch_plan=kwargs.pop("ready_for_reference_informed_patch_plan", True),
        ready_for_change_set_graph=kwargs.pop("ready_for_change_set_graph", True),
        ready_for_diff_proposal_artifact=kwargs.pop("ready_for_diff_proposal_artifact", True),
        ready_for_unified_diff_proposal=kwargs.pop("ready_for_unified_diff_proposal", True),
        ready_for_structured_patch_proposal=kwargs.pop("ready_for_structured_patch_proposal", True),
        ready_for_patch_hunk_proposal=kwargs.pop("ready_for_patch_hunk_proposal", True),
        ready_for_patch_risk_conformance_scan=kwargs.pop("ready_for_patch_risk_conformance_scan", True),
        ready_for_patch_safety_regression_scan=kwargs.pop("ready_for_patch_safety_regression_scan", True),
        ready_for_patch_scope_violation_scan=kwargs.pop("ready_for_patch_scope_violation_scan", True),
        ready_for_human_review_packet=kwargs.pop("ready_for_human_review_packet", True),
        ready_for_approval_gate_metadata=kwargs.pop("ready_for_approval_gate_metadata", True),
        ready_for_patch_proposal_trace_packet_creation=kwargs.pop("ready_for_patch_proposal_trace_packet_creation", True),
        ready_for_bounded_patch_proposal_ocel_trace_emission=kwargs.pop("ready_for_bounded_patch_proposal_ocel_trace_emission", True),
        ready_for_cli_patch_proposal_surface=kwargs.pop("ready_for_cli_patch_proposal_surface", True),
        ready_for_bounded_cli_patch_proposal_preview=kwargs.pop("ready_for_bounded_cli_patch_proposal_preview", True),
        ready_for_digestion_dominion_trace_metadata=kwargs.pop("ready_for_digestion_dominion_trace_metadata", True),
        ready_for_external_agent_control_pattern_trace=kwargs.pop("ready_for_external_agent_control_pattern_trace", True),
        **kwargs,
    )


def build_controlled_patch_proposal_snapshot(snapshot_id: str = "controlled_patch_snapshot:v0.35.9", release_flags: ControlledPatchProposalReleaseFlagSet | None = None, **kwargs: Any) -> ControlledPatchProposalSnapshot:
    return ControlledPatchProposalSnapshot(
        snapshot_id=snapshot_id,
        version=kwargs.pop("version", V0359_VERSION),
        release_name=kwargs.pop("release_name", CONTROLLED_PATCH_PROPOSAL_LAYER_V1),
        included_versions=kwargs.pop("included_versions", list(V035_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(DEFAULT_INCLUDED_MODULES)),
        included_artifact_groups=kwargs.pop("included_artifact_groups", ["boundary", "intent", "context", "plan", "diff", "risk", "review", "trace", "cli"]),
        release_flags=release_flags or kwargs.pop("release_flags", build_controlled_patch_proposal_release_flags()),
        consolidation_status=kwargs.pop("consolidation_status", ControlledPatchProposalConsolidationStatus.CONSOLIDATED),
        readiness_level=kwargs.pop("readiness_level", ControlledPatchProposalConsolidationReadinessLevel.HANDOFF_READY_FOR_V036),
        summary=kwargs.pop("summary", "Controlled Patch Proposal Layer v1 consolidated as bounded proposal artifacts only."),
        controlled_capabilities=kwargs.pop("controlled_capabilities", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        known_gaps=kwargs.pop("known_gaps", []),
        known_risks=kwargs.pop("known_risks", ["patch proposal may be confused with patch application"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def build_controlled_patch_proposal_capability_matrix(capability_matrix_id: str = "controlled_patch_capability_matrix:v0.35.9", **kwargs: Any) -> ControlledPatchProposalCapabilityMatrix:
    prohibited = kwargs.pop("prohibited_capabilities", list(DEFAULT_PROHIBITED_CAPABILITIES))
    return ControlledPatchProposalCapabilityMatrix(
        capability_matrix_id=capability_matrix_id,
        version=kwargs.pop("version", V0359_VERSION),
        enabled_controlled_capabilities=kwargs.pop("enabled_controlled_capabilities", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        enabled_bounded_capabilities=kwargs.pop("enabled_bounded_capabilities", list(DEFAULT_BOUNDED_CAPABILITIES)),
        design_stage_capabilities=kwargs.pop("design_stage_capabilities", ["v0.36 Human-approved Patch Apply Sandbox handoff"]),
        prohibited_capabilities=prohibited,
        future_track_capabilities=kwargs.pop("future_track_capabilities", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        capability_to_version=kwargs.pop("capability_to_version", {capability: "v0.35.x" for capability in DEFAULT_CONTROLLED_CAPABILITIES}),
        prohibited_capability_to_reason=kwargs.pop("prohibited_capability_to_reason", {capability: "Not opened by v0.35.x" for capability in prohibited}),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        **kwargs,
    )


def build_controlled_patch_proposal_stage_coverage(coverage_id: str = "coverage:v0.35.9:stage", stage_version: str = "v0.35.0", coverage_class: type[ControlledPatchProposalStageCoverage] = ControlledPatchProposalStageCoverage, **kwargs: Any) -> ControlledPatchProposalStageCoverage:
    return coverage_class(
        coverage_id=coverage_id,
        version=kwargs.pop("version", V0359_VERSION),
        stage_version=stage_version,
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", []),
        missing_artifact_refs=kwargs.pop("missing_artifact_refs", []),
        covered_test_refs=kwargs.pop("covered_test_refs", []),
        missing_test_refs=kwargs.pop("missing_test_refs", []),
        covered_doc_refs=kwargs.pop("covered_doc_refs", []),
        missing_doc_refs=kwargs.pop("missing_doc_refs", []),
        coverage_notes=kwargs.pop("coverage_notes", ["coverage metadata only; not certification"]),
        coverage_complete=kwargs.pop("coverage_complete", True),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", []),
        evidence_refs=kwargs.pop("evidence_refs", []),
        **kwargs,
    )


def _specific_coverage(index: int, coverage_class: type[ControlledPatchProposalStageCoverage], name: str, **kwargs: Any) -> ControlledPatchProposalStageCoverage:
    return build_controlled_patch_proposal_stage_coverage(
        coverage_id=kwargs.pop("coverage_id", f"coverage:v0.35.9:{name}"),
        stage_version=V035_INCLUDED_VERSIONS[index],
        coverage_class=coverage_class,
        covered_artifact_refs=kwargs.pop("covered_artifact_refs", [DEFAULT_INCLUDED_MODULES[index]]),
        covered_test_refs=kwargs.pop("covered_test_refs", [DEFAULT_INCLUDED_TESTS[index]]),
        covered_doc_refs=kwargs.pop("covered_doc_refs", [DEFAULT_INCLUDED_DOCS[index]]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_INCLUDED_DOCS[index], DEFAULT_INCLUDED_TESTS[index]]),
        **kwargs,
    )


def build_patch_boundary_coverage(**kwargs: Any) -> PatchBoundaryCoverage:
    return _specific_coverage(0, PatchBoundaryCoverage, "boundary", **kwargs)


def build_reference_digest_coverage(**kwargs: Any) -> ReferenceDigestCoverage:
    return _specific_coverage(0, ReferenceDigestCoverage, "reference_digest", **kwargs)


def build_patch_intent_scope_coverage(**kwargs: Any) -> PatchIntentScopeCoverage:
    return _specific_coverage(1, PatchIntentScopeCoverage, "intent_scope", **kwargs)


def build_patch_context_coverage(**kwargs: Any) -> PatchContextCoverage:
    return _specific_coverage(2, PatchContextCoverage, "context", **kwargs)


def build_patch_plan_coverage(**kwargs: Any) -> PatchPlanCoverage:
    return _specific_coverage(3, PatchPlanCoverage, "plan", **kwargs)


def build_diff_proposal_coverage(**kwargs: Any) -> DiffProposalCoverage:
    return _specific_coverage(4, DiffProposalCoverage, "diff", **kwargs)


def build_patch_risk_coverage(**kwargs: Any) -> PatchRiskCoverage:
    return _specific_coverage(5, PatchRiskCoverage, "risk", **kwargs)


def build_patch_review_coverage(**kwargs: Any) -> PatchReviewCoverage:
    return _specific_coverage(6, PatchReviewCoverage, "review", **kwargs)


def build_patch_proposal_trace_coverage(**kwargs: Any) -> PatchProposalTraceCoverage:
    return _specific_coverage(7, PatchProposalTraceCoverage, "trace", **kwargs)


def build_cli_patch_proposal_surface_coverage(**kwargs: Any) -> CLIPatchProposalSurfaceCoverage:
    return _specific_coverage(8, CLIPatchProposalSurfaceCoverage, "cli", **kwargs)


def build_controlled_patch_proposal_boundary_register(boundary_register_id: str = "controlled_patch_boundary_register:v0.35.9", **kwargs: Any) -> ControlledPatchProposalBoundaryRegister:
    return ControlledPatchProposalBoundaryRegister(
        boundary_register_id=boundary_register_id,
        version=kwargs.pop("version", V0359_VERSION),
        inherited_boundaries=kwargs.pop("inherited_boundaries", ["v0.30 external Dominion control plane", "v0.33 internal runtime boundary", "v0.34 controlled model invocation boundary"]),
        active_controlled_boundaries=kwargs.pop("active_controlled_boundaries", ["patch proposal artifact creation", "review metadata", "risk scan metadata", "trace packet metadata", "CLI preview metadata"]),
        active_bounded_boundaries=kwargs.pop("active_bounded_boundaries", ["bounded unified diff text", "bounded CLI output", "returned trace packet"]),
        prohibited_boundaries=kwargs.pop("prohibited_boundaries", ["patch_apply", "workspace_write", "code_edit", "apply_patch", "git_apply", "test_execution", "shell", "subprocess", "command", "dependency_install", "reference_execution", "reference_import", "external_agent_execution", "claude_code_invocation", "codex_cli_invocation", "dominion_runtime", "infinite_agent_loop", "provider_invocation", "direct_network", "credential_access", "secret_read", "persistent_trace", "UI_runtime", "external_control", "authority_grant"]),
        future_gate_boundaries=kwargs.pop("future_gate_boundaries", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        **kwargs,
    )


def build_controlled_patch_proposal_risk_register(risk_register_id: str = "controlled_patch_risk_register:v0.35.9", **kwargs: Any) -> ControlledPatchProposalRiskRegister:
    return ControlledPatchProposalRiskRegister(
        risk_register_id=risk_register_id,
        version=kwargs.pop("version", V0359_VERSION),
        known_risks=kwargs.pop("known_risks", ["diff artifact confused with git apply", "review approval confused with apply permission", "CLI preview confused with shell execution"]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", ["patch application", "external agent loop", "Dominion runtime", "persistent trace write"]),
        prohibited_runtime_surfaces=kwargs.pop("prohibited_runtime_surfaces", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        mitigations=kwargs.pop("mitigations", ["all unsafe readiness flags false", "v0.35 artifacts only", "v0.36 handoff requires sandbox"]),
        unresolved_risks=kwargs.pop("unresolved_risks", ["future apply sandbox not implemented in v0.35"]),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        **kwargs,
    )


def build_controlled_patch_proposal_gap_register(gap_register_id: str = "controlled_patch_gap_register:v0.35.9", **kwargs: Any) -> ControlledPatchProposalGapRegister:
    return ControlledPatchProposalGapRegister(
        gap_register_id=gap_register_id,
        version=kwargs.pop("version", V0359_VERSION),
        blocking_gaps=kwargs.pop("blocking_gaps", []),
        non_blocking_gaps=kwargs.pop("non_blocking_gaps", ["no real patch apply sandbox in v0.35"]),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        recommended_v036_items=kwargs.pop("recommended_v036_items", ["human-approved patch apply sandbox", "dry-run apply simulation", "rollback plan", "explicit apply boundary"]),
        recommended_later_items=kwargs.pop("recommended_later_items", ["controlled test runner", "persistent trace store", "UI runtime", "Dominion runtime gated review"]),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        **kwargs,
    )


def build_controlled_patch_proposal_release_manifest(release_manifest_id: str = "controlled_patch_release_manifest:v0.35.9", release_flags: ControlledPatchProposalReleaseFlagSet | None = None, **kwargs: Any) -> ControlledPatchProposalReleaseManifest:
    return ControlledPatchProposalReleaseManifest(
        release_manifest_id=release_manifest_id,
        version=kwargs.pop("version", V0359_VERSION),
        release_name=kwargs.pop("release_name", CONTROLLED_PATCH_PROPOSAL_LAYER_V1),
        snapshot_id=kwargs.pop("snapshot_id", "controlled_patch_snapshot:v0.35.9"),
        included_versions=kwargs.pop("included_versions", list(V035_INCLUDED_VERSIONS)),
        included_modules=kwargs.pop("included_modules", list(DEFAULT_INCLUDED_MODULES)),
        included_docs=kwargs.pop("included_docs", list(DEFAULT_INCLUDED_DOCS)),
        included_tests=kwargs.pop("included_tests", list(DEFAULT_INCLUDED_TESTS)),
        focused_test_command=kwargs.pop("focused_test_command", "python -m pytest tests/test_v0359_controlled_patch_proposal_layer_consolidation.py"),
        full_track_test_command=kwargs.pop("full_track_test_command", "python -m pytest tests/test_v0350_controlled_patch_proposal_boundary.py ... tests/test_v0359_controlled_patch_proposal_layer_consolidation.py"),
        release_flags=release_flags or kwargs.pop("release_flags", build_controlled_patch_proposal_release_flags()),
        known_gaps=kwargs.pop("known_gaps", []),
        known_risks=kwargs.pop("known_risks", ["v0.36 apply sandbox not implemented in v0.35"]),
        next_handoff_id=kwargs.pop("next_handoff_id", "v036_handoff:v0.35.9"),
        **kwargs,
    )


def build_controlled_patch_proposal_audit_trail(audit_trail_id: str = "controlled_patch_audit_trail:v0.35.9", **kwargs: Any) -> ControlledPatchProposalAuditTrail:
    return ControlledPatchProposalAuditTrail(
        audit_trail_id=audit_trail_id,
        version=kwargs.pop("version", V0359_VERSION),
        reviewed_artifact_refs=kwargs.pop("reviewed_artifact_refs", list(DEFAULT_INCLUDED_MODULES)),
        reviewed_test_refs=kwargs.pop("reviewed_test_refs", list(DEFAULT_INCLUDED_TESTS)),
        reviewed_doc_refs=kwargs.pop("reviewed_doc_refs", list(DEFAULT_INCLUDED_DOCS)),
        boundary_checks=kwargs.pop("boundary_checks", ["v0.35 unsafe readiness flags remain false", "proposal artifact is not apply"]),
        negative_runtime_checks=kwargs.pop("negative_runtime_checks", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        controlled_capability_checks=kwargs.pop("controlled_capability_checks", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        **kwargs,
    )


def build_digestion_dominion_consolidation_record(digestion_consolidation_id: str = "digestion_dominion_consolidation:v0.35.9", **kwargs: Any) -> DigestionDominionConsolidationRecord:
    return DigestionDominionConsolidationRecord(
        digestion_consolidation_id=digestion_consolidation_id,
        version=kwargs.pop("version", V0359_VERSION),
        digestion_first_policy_confirmed=kwargs.pop("digestion_first_policy_confirmed", True),
        dominion_fallback_future_gated=kwargs.pop("dominion_fallback_future_gated", True),
        external_agent_patterns_recorded=kwargs.pop("external_agent_patterns_recorded", True),
        external_agent_execution_blocked=kwargs.pop("external_agent_execution_blocked", True),
        infinite_loop_blocked=kwargs.pop("infinite_loop_blocked", True),
        dominion_runtime_blocked=kwargs.pop("dominion_runtime_blocked", True),
        safely_digested_items=kwargs.pop("safely_digested_items", ["OpenCode/Hermes static pattern summaries", "ReferencePatternDigest adaptation notes"]),
        rejected_dominion_like_items=kwargs.pop("rejected_dominion_like_items", ["Codex-to-Claude-Code loop", "OpenCode/Hermes execution loop"]),
        future_track_dominion_items=kwargs.pop("future_track_dominion_items", ["Dominion runtime gated review", "external control audit gate"]),
        summary=kwargs.pop("summary", "Digestion-first / Dominion-fallback consolidated as metadata only."),
        **kwargs,
    )


def build_external_agent_control_pattern_consolidation_record(external_agent_record_id: str = "external_agent_consolidation:v0.35.9", **kwargs: Any) -> ExternalAgentControlPatternConsolidationRecord:
    return ExternalAgentControlPatternConsolidationRecord(
        external_agent_record_id=external_agent_record_id,
        version=kwargs.pop("version", V0359_VERSION),
        observed_pattern_kinds=kwargs.pop("observed_pattern_kinds", ["codex_to_claude_code_loop", "opencode_execution_loop", "hermes_execution_loop", "dominion_like_external_control"]),
        blocked_pattern_kinds=kwargs.pop("blocked_pattern_kinds", ["external_agent_execution", "reference_harness_execution", "infinite_agent_loop"]),
        future_gated_pattern_kinds=kwargs.pop("future_gated_pattern_kinds", ["dominion_runtime", "external_agent_orchestration"]),
        denied_cli_commands=kwargs.pop("denied_cli_commands", ["run-claude-code", "run-codex", "run-opencode", "run-hermes", "run-openclaw", "dominion", "external-agent-loop", "infinite-loop"]),
        risk_notes=kwargs.pop("risk_notes", ["external agent control patterns are metadata only"]),
        execution_allowed=kwargs.pop("execution_allowed", False),
        dominion_runtime_allowed=kwargs.pop("dominion_runtime_allowed", False),
        infinite_loop_allowed=kwargs.pop("infinite_loop_allowed", False),
        summary=kwargs.pop("summary", "External-agent-control patterns consolidated as blocked/future-gated metadata only."),
        **kwargs,
    )


def build_v036_handoff_packet(handoff_id: str = "v036_handoff:v0.35.9", **kwargs: Any) -> V036HandoffPacket:
    return V036HandoffPacket(
        handoff_id=handoff_id,
        source_version=kwargs.pop("source_version", V0359_VERSION),
        target_version_track=kwargs.pop("target_version_track", "v0.36"),
        source_snapshot_id=kwargs.pop("source_snapshot_id", "controlled_patch_snapshot:v0.35.9"),
        release_manifest_id=kwargs.pop("release_manifest_id", "controlled_patch_release_manifest:v0.35.9"),
        recommended_next_track=kwargs.pop("recommended_next_track", "Human-approved Patch Apply Sandbox"),
        recommended_next_release=kwargs.pop("recommended_next_release", "v0.36.0 Patch Apply Sandbox Dry-run Simulation"),
        human_approved_patch_apply_sandbox_items=kwargs.pop("human_approved_patch_apply_sandbox_items", ["human approval gate", "explicit apply boundary", "scope gate"]),
        dry_run_apply_simulation_items=kwargs.pop("dry_run_apply_simulation_items", ["dry-run apply simulation metadata", "detect conflicts without writing"]),
        apply_sandbox_policy_items=kwargs.pop("apply_sandbox_policy_items", ["no secret", "no shell", "no network", "bounded target scope"]),
        rollback_plan_items=kwargs.pop("rollback_plan_items", ["rollback metadata", "pre-apply snapshot refs"]),
        human_confirmation_items=kwargs.pop("human_confirmation_items", ["review packet approval", "risk report acceptance", "scope confirmation"]),
        reusable_intent_scope_items=kwargs.pop("reusable_intent_scope_items", ["v0.35.1 PatchIntentScopeBundle"]),
        reusable_context_items=kwargs.pop("reusable_context_items", ["v0.35.2 PatchContextSnapshot"]),
        reusable_plan_items=kwargs.pop("reusable_plan_items", ["v0.35.3 PatchPlan"]),
        reusable_diff_items=kwargs.pop("reusable_diff_items", ["v0.35.4 DiffProposalEnvelope"]),
        reusable_risk_items=kwargs.pop("reusable_risk_items", ["v0.35.5 PatchProposalRiskReport"]),
        reusable_review_items=kwargs.pop("reusable_review_items", ["v0.35.6 PatchReviewPacket"]),
        reusable_trace_items=kwargs.pop("reusable_trace_items", ["v0.35.7 PatchProposalTracePacket"]),
        reusable_cli_items=kwargs.pop("reusable_cli_items", ["v0.35.8 CLI patch proposal preview"]),
        required_new_boundaries=kwargs.pop("required_new_boundaries", ["apply sandbox policy", "rollback plan", "no-secret/no-shell/no-network checks"]),
        prohibited_until_later_gate=kwargs.pop("prohibited_until_later_gate", ["patch application", "workspace write", "code edit", "apply_patch", "git apply", "shell", "command", "test execution", "dependency install", "direct provider", "direct network", "credential access", "external agent execution", "Dominion runtime", "infinite loop", "UI runtime", "authority grant"]),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        readiness_level=kwargs.pop("readiness_level", ControlledPatchProposalConsolidationReadinessLevel.HANDOFF_READY_FOR_V036),
        ready_for_v036=kwargs.pop("ready_for_v036", True),
        **kwargs,
    )


def build_v035_consolidation_report(report_id: str = "v035_consolidation_report:v0.35.9", **kwargs: Any) -> V035ConsolidationReport:
    return V035ConsolidationReport(
        report_id=report_id,
        version=kwargs.pop("version", V0359_VERSION),
        release_name=kwargs.pop("release_name", CONTROLLED_PATCH_PROPOSAL_LAYER_V1),
        snapshot_id=kwargs.pop("snapshot_id", "controlled_patch_snapshot:v0.35.9"),
        release_manifest_id=kwargs.pop("release_manifest_id", "controlled_patch_release_manifest:v0.35.9"),
        handoff_id=kwargs.pop("handoff_id", "v036_handoff:v0.35.9"),
        consolidation_status=kwargs.pop("consolidation_status", ControlledPatchProposalConsolidationStatus.CONSOLIDATED),
        readiness_level=kwargs.pop("readiness_level", ControlledPatchProposalConsolidationReadinessLevel.HANDOFF_READY_FOR_V036),
        summary=kwargs.pop("summary", "Controlled Patch Proposal Layer v1 consolidated; proposal artifacts ready, apply remains false."),
        completed_items=kwargs.pop("completed_items", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        controlled_enabled_items=kwargs.pop("controlled_enabled_items", list(DEFAULT_CONTROLLED_CAPABILITIES)),
        bounded_enabled_items=kwargs.pop("bounded_enabled_items", list(DEFAULT_BOUNDED_CAPABILITIES)),
        blocked_items=kwargs.pop("blocked_items", list(DEFAULT_PROHIBITED_CAPABILITIES)),
        future_track_items=kwargs.pop("future_track_items", list(DEFAULT_FUTURE_TRACK_ITEMS)),
        runtime_not_ready_items=kwargs.pop("runtime_not_ready_items", list(DEFAULT_PROHIBITED_RUNTIME_SURFACES)),
        v036_handoff_summary=kwargs.pop("v036_handoff_summary", "Recommended next track is Human-approved Patch Apply Sandbox beginning with dry-run apply simulation."),
        ready_for_v036=kwargs.pop("ready_for_v036", True),
        ready_for_controlled_patch_proposal_layer_v1=kwargs.pop("ready_for_controlled_patch_proposal_layer_v1", True),
        ready_for_patch_intent_scope_policy=kwargs.pop("ready_for_patch_intent_scope_policy", True),
        ready_for_readonly_patch_context_collection=kwargs.pop("ready_for_readonly_patch_context_collection", True),
        ready_for_reference_informed_patch_plan=kwargs.pop("ready_for_reference_informed_patch_plan", True),
        ready_for_diff_proposal_artifact=kwargs.pop("ready_for_diff_proposal_artifact", True),
        ready_for_patch_risk_conformance_scan=kwargs.pop("ready_for_patch_risk_conformance_scan", True),
        ready_for_human_review_packet=kwargs.pop("ready_for_human_review_packet", True),
        ready_for_patch_proposal_trace_packet_creation=kwargs.pop("ready_for_patch_proposal_trace_packet_creation", True),
        ready_for_cli_patch_proposal_surface=kwargs.pop("ready_for_cli_patch_proposal_surface", True),
        evidence_refs=kwargs.pop("evidence_refs", list(DEFAULT_INCLUDED_DOCS)),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def controlled_patch_proposal_flags_preserve_no_apply(flags: ControlledPatchProposalReleaseFlagSet) -> bool:
    return isinstance(flags, ControlledPatchProposalReleaseFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_RELEASE_FLAG_NAMES)


def controlled_patch_proposal_snapshot_is_not_runtime_expansion(snapshot: ControlledPatchProposalSnapshot) -> bool:
    return controlled_patch_proposal_flags_preserve_no_apply(snapshot.release_flags)


def controlled_patch_proposal_capability_matrix_is_not_permission_grant(matrix: ControlledPatchProposalCapabilityMatrix) -> bool:
    return all(item in matrix.prohibited_capabilities for item in DEFAULT_PROHIBITED_CAPABILITIES)


def controlled_patch_proposal_audit_confirms_no_unsafe_runtime(audit: ControlledPatchProposalAuditTrail) -> bool:
    return all(getattr(audit, name) is True for name in audit.__dataclass_fields__ if name.startswith("no_")) and audit.unsafe_readiness_flags_false_confirmed is True


def digestion_dominion_consolidation_record_is_not_runtime(record: DigestionDominionConsolidationRecord) -> bool:
    return record.dominion_runtime_blocked is True and record.external_agent_execution_blocked is True and record.infinite_loop_blocked is True


def external_agent_control_pattern_record_is_not_execution(record: ExternalAgentControlPatternConsolidationRecord) -> bool:
    return record.execution_allowed is False and record.dominion_runtime_allowed is False and record.infinite_loop_allowed is False


def v036_handoff_packet_is_design_stage_only(packet: V036HandoffPacket) -> bool:
    return not any(getattr(packet, name) for name in ("ready_for_execution", "ready_for_patch_application", "ready_for_workspace_write", "ready_for_code_edit", "ready_for_apply_patch", "ready_for_git_apply"))


def v035_consolidation_report_is_not_runtime_ready(report: V035ConsolidationReport) -> bool:
    return all(getattr(report, name) is False for name in REPORT_UNSAFE_FLAG_NAMES)
