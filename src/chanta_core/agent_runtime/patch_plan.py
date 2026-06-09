from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_context import PatchContextEvidenceBundle, PatchContextSnapshot
from .patch_intent import PatchIntentScopeBundle
from .patch_proposal_boundary import ReferencePatternDisposition
from .patch_intent import PatchTargetKind


V0353_VERSION = "v0.35.3"
V0353_RELEASE_NAME = "v0.35.3 Reference-informed Patch Plan & Change Set Graph"
DEFAULT_V0353_DOC_PATH = "docs/versions/v0.35/v0.35.3_reference_informed_patch_plan_change_set_graph.md"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"
DEFAULT_V0352_CONTEXT_DOC_REF = "docs/versions/v0.35/v0.35.2_readonly_patch_context_reference_corpus_collector.md"

DEFAULT_PROHIBITED_RUNTIME_ACTIONS = [
    "diff_proposal_generation",
    "patch_proposal_generation",
    "patch_hunk_generation",
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
    "provider_invocation",
    "direct_network_access",
    "credential_access",
    "secret_read",
]

UNSAFE_PATCH_PLAN_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_diff_proposal",
    "ready_for_patch_proposal",
    "ready_for_patch_hunk_generation",
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
    "ready_for_provider_invocation",
    "ready_for_direct_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_unquarantined_action_execution",
    "ready_for_persistent_trace_write",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class PatchPlanMode(StrEnum):
    INTENT_SCOPE_ONLY = "intent_scope_only"
    CONTEXT_SNAPSHOT_INFORMED = "context_snapshot_informed"
    REFERENCE_DIGEST_INFORMED = "reference_digest_informed"
    COMBINED_CONTEXT_AND_REFERENCE_INFORMED = "combined_context_and_reference_informed"
    BLOCKED = "blocked"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchPlanSourceKind(StrEnum):
    V0352_PATCH_CONTEXT_SNAPSHOT = "v0352_patch_context_snapshot"
    V0352_EVIDENCE_BUNDLE = "v0352_evidence_bundle"
    V0351_PATCH_INTENT_SCOPE_BUNDLE = "v0351_patch_intent_scope_bundle"
    V0351_PATCH_INTENT_ENVELOPE = "v0351_patch_intent_envelope"
    V0351_PATCH_SCOPE_POLICY = "v0351_patch_scope_policy"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    REFERENCE_PATTERN_ADAPTATION = "reference_pattern_adaptation"
    USER_REQUEST = "user_request"
    MODEL_BACKED_STEP_OUTPUT = "model_backed_step_output"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchPlanStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    PLAN_CREATED = "plan_created"
    PLAN_VALIDATED = "plan_validated"
    PLAN_VALIDATED_WITH_GAPS = "plan_validated_with_gaps"
    CHANGE_SET_GRAPH_CREATED = "change_set_graph_created"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class PatchPlanReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    PLAN_CONTRACT_READY = "plan_contract_ready"
    CHANGE_SET_GRAPH_READY = "change_set_graph_ready"
    REFERENCE_INFORMED_PLAN_READY = "reference_informed_plan_ready"
    DESIGN_HANDOFF_READY_FOR_V0354 = "design_handoff_ready_for_v0354"
    DESIGN_HANDOFF_READY_FOR_V0355 = "design_handoff_ready_for_v0355"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchPlanDecisionKind(StrEnum):
    ALLOW_PLAN_METADATA = "allow_plan_metadata"
    ALLOW_CHANGE_SET_GRAPH_METADATA = "allow_change_set_graph_metadata"
    ALLOW_TARGET_FILE_PLAN_METADATA = "allow_target_file_plan_metadata"
    ALLOW_TEST_PLAN_METADATA = "allow_test_plan_metadata"
    ALLOW_DOCUMENTATION_PLAN_METADATA = "allow_documentation_plan_metadata"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchPlanRiskKind(StrEnum):
    INSUFFICIENT_CONTEXT_RISK = "insufficient_context_risk"
    OVERBROAD_CHANGE_SET_RISK = "overbroad_change_set_risk"
    UNSAFE_REFERENCE_PATTERN_RISK = "unsafe_reference_pattern_risk"
    SCOPE_ESCAPE_RISK = "scope_escape_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    PATCH_DIFF_GENERATION_RISK = "patch_diff_generation_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    PROVIDER_NETWORK_OPENING_RISK = "provider_network_opening_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    COPIED_CODE_RISK = "copied_code_risk"
    LICENSE_OR_ATTRIBUTION_RISK = "license_or_attribution_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class PatchChangeKind(StrEnum):
    ADD_CONTRACT_MODEL = "add_contract_model"
    EXTEND_CONTRACT_MODEL = "extend_contract_model"
    ADD_VALIDATION_HELPER = "add_validation_helper"
    STRENGTHEN_VALIDATION_RULE = "strengthen_validation_rule"
    ADD_READINESS_REPORT = "add_readiness_report"
    ADD_BOUNDARY_POLICY = "add_boundary_policy"
    ADD_TEST_CASE = "add_test_case"
    UPDATE_DOCUMENTATION = "update_documentation"
    REFACTOR_INTERNAL_STRUCTURE = "refactor_internal_structure"
    ALIGN_WITH_REFERENCE_PATTERN = "align_with_reference_pattern"
    ADD_TRACE_ARTIFACT = "add_trace_artifact"
    ADD_CLI_SURFACE_METADATA = "add_cli_surface_metadata"
    NO_OP_CHANGE = "no_op_change"
    UNKNOWN = "unknown"


class PatchChangeNodeStatus(StrEnum):
    UNKNOWN = "unknown"
    PROPOSED = "proposed"
    PLANNED = "planned"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class PatchDependencyKind(StrEnum):
    REQUIRES_MODEL_BEFORE_TEST = "requires_model_before_test"
    REQUIRES_POLICY_BEFORE_BOUNDARY = "requires_policy_before_boundary"
    REQUIRES_CONTEXT_BEFORE_PLAN = "requires_context_before_plan"
    REQUIRES_PLAN_BEFORE_DIFF = "requires_plan_before_diff"
    REQUIRES_RISK_SCAN_BEFORE_REVIEW = "requires_risk_scan_before_review"
    REQUIRES_DOC_UPDATE_AFTER_MODEL = "requires_doc_update_after_model"
    CONFLICTS_WITH = "conflicts_with"
    BLOCKS = "blocks"
    RELATED_TO = "related_to"
    NO_DEPENDENCY = "no_dependency"
    UNKNOWN = "unknown"


class PatchChangeSetGraphStatus(StrEnum):
    UNKNOWN = "unknown"
    GRAPH_CREATED = "graph_created"
    GRAPH_VALIDATED = "graph_validated"
    GRAPH_VALIDATED_WITH_GAPS = "graph_validated_with_gaps"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0353_VERSION not in value:
        raise ValueError("version must include v0.35.3")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    for key in metadata:
        lower = str(key).lower()
        if any(token in lower for token in ("secret", "credential", "api_key", "token", "password")):
            raise ValueError("metadata must not contain secret-like keys")


def _validate_list(name: str, value: Any) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be a list")


def _validate_enum_list(name: str, value: list[Any], enum_type: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_type(item)


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.35.3")


@dataclass(frozen=True)
class PatchPlanFlagSet:
    flag_set_id: str
    version: str
    patch_plan_layer_constructed: bool
    change_set_graph_defined: bool
    target_file_plan_defined: bool
    test_plan_defined: bool
    documentation_plan_defined: bool
    reference_informed_planning_available: bool
    ready_for_v0354_diff_proposal_envelope: bool
    ready_for_v0355_patch_risk_conformance_scanner: bool
    ready_for_patch_plan: bool
    ready_for_change_set_graph: bool
    ready_for_reference_informed_patch_plan: bool
    ready_for_execution: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_hunk_generation: bool = False
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
    ready_for_provider_invocation: bool = False
    ready_for_direct_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_unquarantined_action_execution: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_PATCH_PLAN_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanSourceRef:
    source_ref_id: str
    source_kind: PatchPlanSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PatchPlanSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class ReferenceInformedPatchPatternUse:
    pattern_use_id: str
    source_pattern_id: str | None
    source_digest_id: str | None
    source_context_snapshot_id: str | None
    reference_name: str
    observed_pattern_summary: str
    planning_adaptation: str
    applied_to_change_node_ids: list[str]
    rejected: bool
    rejection_reason: str | None
    future_track: bool
    confidence: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("pattern_use_id", self.pattern_use_id)
        for name in ("source_pattern_id", "source_digest_id", "source_context_snapshot_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        _require_non_blank("reference_name", self.reference_name)
        _require_non_blank("observed_pattern_summary", self.observed_pattern_summary)
        _require_non_blank("planning_adaptation", self.planning_adaptation)
        _validate_string_list("applied_to_change_node_ids", self.applied_to_change_node_ids)
        if self.rejected and not self.rejection_reason:
            raise ValueError("rejected pattern uses must include rejection_reason")
        _require_non_blank("confidence", self.confidence)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanningPolicy:
    planning_policy_id: str
    version: str
    allowed_change_kinds: list[PatchChangeKind | str]
    blocked_change_kinds: list[PatchChangeKind | str]
    allowed_target_kinds: list[PatchTargetKind | str]
    blocked_target_kinds: list[PatchTargetKind | str]
    max_change_nodes: int
    max_dependency_edges: int
    max_target_files: int
    require_context_snapshot: bool
    require_intent_scope_bundle: bool
    require_non_goal_register: bool
    allow_reference_informed_patterns: bool
    allow_future_diff_handoff: bool
    allow_diff_text: bool = False
    allow_patch_hunks: bool = False
    allow_patch_apply: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_test_execution: bool = False
    allow_dependency_install: bool = False
    allow_shell: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("planning_policy_id", self.planning_policy_id)
        _validate_version(self.version)
        _validate_enum_list("allowed_change_kinds", self.allowed_change_kinds, PatchChangeKind)
        _validate_enum_list("blocked_change_kinds", self.blocked_change_kinds, PatchChangeKind)
        _validate_enum_list("allowed_target_kinds", self.allowed_target_kinds, PatchTargetKind)
        _validate_enum_list("blocked_target_kinds", self.blocked_target_kinds, PatchTargetKind)
        for name in ("max_change_nodes", "max_dependency_edges", "max_target_files"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        for name in ("allow_diff_text", "allow_patch_hunks", "allow_patch_apply", "allow_workspace_write", "allow_code_edit", "allow_test_execution", "allow_dependency_install", "allow_shell"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.3")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanningInput:
    planning_input_id: str
    version: str
    intent_scope_bundle_id: str | None
    patch_context_snapshot_id: str | None
    evidence_bundle_id: str | None
    reference_pattern_digest_id: str | None
    planning_mode: PatchPlanMode | str
    task_summary: str
    source_refs: list[PatchPlanSourceRef]
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("planning_input_id", self.planning_input_id)
        _validate_version(self.version)
        for name in ("intent_scope_bundle_id", "patch_context_snapshot_id", "evidence_bundle_id", "reference_pattern_digest_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        PatchPlanMode(self.planning_mode)
        _require_non_blank("task_summary", self.task_summary)
        _validate_list("source_refs", self.source_refs)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        required = {"diff_proposal_generation", "patch_proposal_generation", "patch_application", "workspace_write", "code_edit", "shell_execution", "test_execution", "dependency_install", "reference_execution", "provider_invocation", "direct_network_access", "credential_access"}
        if not required.issubset(set(self.prohibited_runtime_actions)):
            raise ValueError("prohibited_runtime_actions must include unsafe runtime actions")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchChangeNode:
    change_node_id: str
    change_kind: PatchChangeKind | str
    status: PatchChangeNodeStatus | str
    title: str
    rationale: str
    target_file_refs: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    risk_kinds: list[PatchPlanRiskKind | str] = field(default_factory=list)
    reference_pattern_use_ids: list[str] = field(default_factory=list)
    blocked_reason: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("change_node_id", self.change_node_id)
        PatchChangeKind(self.change_kind)
        status = PatchChangeNodeStatus(self.status)
        _require_non_blank("title", self.title)
        _require_non_blank("rationale", self.rationale)
        _validate_string_list("target_file_refs", self.target_file_refs)
        _validate_string_list("expected_artifacts", self.expected_artifacts)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchPlanRiskKind)
        _validate_string_list("reference_pattern_use_ids", self.reference_pattern_use_ids)
        if status == PatchChangeNodeStatus.BLOCKED and not self.blocked_reason:
            raise ValueError("blocked nodes must include blocked_reason")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchDependencyEdge:
    dependency_edge_id: str
    dependency_kind: PatchDependencyKind | str
    source_change_node_id: str
    target_change_node_id: str
    rationale: str
    blocking: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("dependency_edge_id", self.dependency_edge_id)
        PatchDependencyKind(self.dependency_kind)
        _require_non_blank("source_change_node_id", self.source_change_node_id)
        _require_non_blank("target_change_node_id", self.target_change_node_id)
        _require_non_blank("rationale", self.rationale)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchTargetFilePlan:
    target_file_plan_id: str
    target_path_ref: str
    target_kind: PatchTargetKind | str
    planned_change_node_ids: list[str]
    planned_role: str
    rationale: str
    allowed_for_future_diff: bool
    allowed_for_write: bool = False
    allowed_for_apply: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("target_file_plan_id", self.target_file_plan_id)
        _require_non_blank("target_path_ref", self.target_path_ref)
        PatchTargetKind(self.target_kind)
        _validate_string_list("planned_change_node_ids", self.planned_change_node_ids)
        _require_non_blank("planned_role", self.planned_role)
        _require_non_blank("rationale", self.rationale)
        if self.allowed_for_write is not False or self.allowed_for_apply is not False:
            raise ValueError("target file plans must not allow write/apply")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchTestPlan:
    test_plan_id: str
    related_change_node_ids: list[str]
    test_target_refs: list[str]
    test_strategy_summary: str
    expected_test_coverage: list[str]
    ready_for_test_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("test_plan_id", self.test_plan_id)
        _validate_string_list("related_change_node_ids", self.related_change_node_ids)
        _validate_string_list("test_target_refs", self.test_target_refs)
        _require_non_blank("test_strategy_summary", self.test_strategy_summary)
        _validate_string_list("expected_test_coverage", self.expected_test_coverage)
        if self.ready_for_test_execution is not False:
            raise ValueError("ready_for_test_execution must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchDocumentationPlan:
    documentation_plan_id: str
    related_change_node_ids: list[str]
    doc_target_refs: list[str]
    documentation_summary: str
    expected_doc_updates: list[str]
    ready_for_doc_write: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("documentation_plan_id", self.documentation_plan_id)
        _validate_string_list("related_change_node_ids", self.related_change_node_ids)
        _validate_string_list("doc_target_refs", self.doc_target_refs)
        _require_non_blank("documentation_summary", self.documentation_summary)
        _validate_string_list("expected_doc_updates", self.expected_doc_updates)
        if self.ready_for_doc_write is not False:
            raise ValueError("ready_for_doc_write must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchChangeSetGraph:
    change_set_graph_id: str
    version: str
    planning_input_id: str
    change_nodes: list[PatchChangeNode]
    dependency_edges: list[PatchDependencyEdge]
    target_file_plans: list[PatchTargetFilePlan]
    test_plans: list[PatchTestPlan]
    documentation_plans: list[PatchDocumentationPlan]
    status: PatchChangeSetGraphStatus | str
    summary: str
    ready_for_v0354_diff_proposal_envelope: bool
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("change_set_graph_id", self.change_set_graph_id)
        _validate_version(self.version)
        _require_non_blank("planning_input_id", self.planning_input_id)
        for name in ("change_nodes", "dependency_edges", "target_file_plans", "test_plans", "documentation_plans"):
            _validate_list(name, getattr(self, name))
        PatchChangeSetGraphStatus(self.status)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlan:
    patch_plan_id: str
    version: str
    planning_input_id: str
    plan_mode: PatchPlanMode | str
    status: PatchPlanStatus | str
    readiness_level: PatchPlanReadinessLevel | str
    title: str
    plan_summary: str
    intent_id: str | None
    context_snapshot_id: str | None
    reference_digest_id: str | None
    change_set_graph: PatchChangeSetGraph
    reference_pattern_uses: list[ReferenceInformedPatchPatternUse]
    risk_kinds: list[PatchPlanRiskKind | str]
    gaps: list[str]
    ready_for_v0354_diff_proposal_envelope: bool
    ready_for_v0355_patch_risk_conformance_scanner: bool
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("patch_plan_id", "planning_input_id", "title", "plan_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchPlanMode(self.plan_mode)
        PatchPlanStatus(self.status)
        PatchPlanReadinessLevel(self.readiness_level)
        for name in ("intent_id", "context_snapshot_id", "reference_digest_id"):
            if getattr(self, name) is not None:
                _require_non_blank(name, getattr(self, name))
        _validate_list("reference_pattern_uses", self.reference_pattern_uses)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchPlanRiskKind)
        _validate_string_list("gaps", self.gaps)
        _validate_false(self, ("ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_patch_application", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanValidationFinding:
    finding_id: str
    decision_kind: PatchPlanDecisionKind | str
    risk_kinds: list[PatchPlanRiskKind | str]
    message: str
    blocks_validation: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        PatchPlanDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchPlanRiskKind)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanValidationReport:
    validation_report_id: str
    version: str
    patch_plan_id: str | None
    findings: list[PatchPlanValidationFinding]
    valid: bool
    summary: str
    ready_for_execution: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        if self.patch_plan_id is not None:
            _require_non_blank("patch_plan_id", self.patch_plan_id)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_execution", "ready_for_diff_proposal", "ready_for_patch_proposal"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchChangeSetValidationFinding(PatchPlanValidationFinding):
    pass


@dataclass(frozen=True)
class PatchChangeSetValidationReport:
    validation_report_id: str
    version: str
    change_set_graph_id: str | None
    findings: list[PatchChangeSetValidationFinding]
    valid: bool
    summary: str
    ready_for_execution: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version(self.version)
        if self.change_set_graph_id is not None:
            _require_non_blank("change_set_graph_id", self.change_set_graph_id)
        _validate_list("findings", self.findings)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_execution", "ready_for_diff_proposal", "ready_for_patch_proposal"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanReport:
    report_id: str
    version: str
    patch_plan_id: str
    change_set_graph_id: str
    summary: str
    plan_ready: bool
    change_set_graph_ready: bool
    reference_informed_plan_ready: bool
    gap_items: list[str]
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "patch_plan_id", "change_set_graph_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("gap_items", self.gap_items)
        _validate_false(self, ("ready_for_diff_proposal", "ready_for_patch_proposal", "ready_for_patch_application", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_diff_proposal_guarantee: bool = True
    no_patch_proposal_guarantee: bool = True
    no_patch_hunk_generation_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_test_execution_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_reference_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchPlanNoDiffNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_diff_proposal: bool = True
    no_patch_proposal: bool = True
    no_patch_hunk_generation: bool = True
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_test_execution: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_dependency_install: bool = True
    no_reference_execution: bool = True
    no_reference_import: bool = True
    no_provider_invocation: bool = True
    no_direct_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_autonomous_runtime: bool = True
    no_general_tool_execution: bool = True
    no_persistent_trace_write: bool = True
    no_ui_runtime: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class V0353ReadinessReport:
    report_id: str
    version: str
    patch_plan_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0354_diff_proposal_envelope: bool = True
    ready_for_v0355_patch_risk_conformance_scanner: bool = True
    ready_for_patch_plan: bool = True
    ready_for_change_set_graph: bool = True
    ready_for_reference_informed_patch_plan: bool = True
    ready_for_execution: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_hunk_generation: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_apply_patch: bool = False
    ready_for_git_apply: bool = False
    ready_for_test_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_dependency_install: bool = False
    ready_for_reference_execution: bool = False
    ready_for_reference_import: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        if self.patch_plan_id is not None:
            _require_non_blank("patch_plan_id", self.patch_plan_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_PATCH_PLAN_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_patch_plan_flags(flag_set_id: str = "patch_plan_flags:v0.35.3", **kwargs: Any) -> PatchPlanFlagSet:
    return PatchPlanFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0353_VERSION),
        patch_plan_layer_constructed=kwargs.pop("patch_plan_layer_constructed", True),
        change_set_graph_defined=kwargs.pop("change_set_graph_defined", True),
        target_file_plan_defined=kwargs.pop("target_file_plan_defined", True),
        test_plan_defined=kwargs.pop("test_plan_defined", True),
        documentation_plan_defined=kwargs.pop("documentation_plan_defined", True),
        reference_informed_planning_available=kwargs.pop("reference_informed_planning_available", True),
        ready_for_v0354_diff_proposal_envelope=kwargs.pop("ready_for_v0354_diff_proposal_envelope", True),
        ready_for_v0355_patch_risk_conformance_scanner=kwargs.pop("ready_for_v0355_patch_risk_conformance_scanner", True),
        ready_for_patch_plan=kwargs.pop("ready_for_patch_plan", True),
        ready_for_change_set_graph=kwargs.pop("ready_for_change_set_graph", True),
        ready_for_reference_informed_patch_plan=kwargs.pop("ready_for_reference_informed_patch_plan", True),
        **kwargs,
    )


def build_patch_plan_source_ref(source_ref_id: str = "patch_plan_source:v0.35.3", **kwargs: Any) -> PatchPlanSourceRef:
    return PatchPlanSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchPlanSourceKind.V0352_PATCH_CONTEXT_SNAPSHOT),
        source_id=kwargs.pop("source_id", "context_snapshot:v0.35.2"),
        source_summary=kwargs.pop("source_summary", "Supplied v0.35.2 context snapshot metadata."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0352_CONTEXT_DOC_REF]),
        **kwargs,
    )


def build_reference_informed_patch_pattern_use(pattern_use_id: str = "pattern_use:v0.35.3", **kwargs: Any) -> ReferenceInformedPatchPatternUse:
    return ReferenceInformedPatchPatternUse(
        pattern_use_id=pattern_use_id,
        source_pattern_id=kwargs.pop("source_pattern_id", "pattern:reference:v0.35.0"),
        source_digest_id=kwargs.pop("source_digest_id", "reference_pattern_digest:v0.35.0"),
        source_context_snapshot_id=kwargs.pop("source_context_snapshot_id", "context_snapshot:v0.35.2"),
        reference_name=kwargs.pop("reference_name", "ReferencePatternDigest"),
        observed_pattern_summary=kwargs.pop("observed_pattern_summary", "Reference pattern summarized as planning metadata."),
        planning_adaptation=kwargs.pop("planning_adaptation", "Use as planning metadata only; do not copy implementation bodies."),
        applied_to_change_node_ids=kwargs.pop("applied_to_change_node_ids", ["change_node:v0.35.3:model"]),
        rejected=kwargs.pop("rejected", False),
        rejection_reason=kwargs.pop("rejection_reason", None),
        future_track=kwargs.pop("future_track", False),
        confidence=kwargs.pop("confidence", "medium"),
        **kwargs,
    )


def build_patch_planning_policy(planning_policy_id: str = "planning_policy:v0.35.3", **kwargs: Any) -> PatchPlanningPolicy:
    return PatchPlanningPolicy(
        planning_policy_id=planning_policy_id,
        version=kwargs.pop("version", V0353_VERSION),
        allowed_change_kinds=kwargs.pop("allowed_change_kinds", [PatchChangeKind.ADD_CONTRACT_MODEL, PatchChangeKind.ADD_VALIDATION_HELPER, PatchChangeKind.ADD_TEST_CASE, PatchChangeKind.UPDATE_DOCUMENTATION, PatchChangeKind.ALIGN_WITH_REFERENCE_PATTERN]),
        blocked_change_kinds=kwargs.pop("blocked_change_kinds", [PatchChangeKind.UNKNOWN]),
        allowed_target_kinds=kwargs.pop("allowed_target_kinds", [PatchTargetKind.SOURCE_FILE, PatchTargetKind.TEST_FILE, PatchTargetKind.DOCUMENTATION_FILE, PatchTargetKind.VERSION_DOCUMENT]),
        blocked_target_kinds=kwargs.pop("blocked_target_kinds", [PatchTargetKind.SECRET_LIKE_FILE, PatchTargetKind.CREDENTIAL_LIKE_FILE, PatchTargetKind.BINARY_FILE, PatchTargetKind.EXTERNAL_PATH]),
        max_change_nodes=kwargs.pop("max_change_nodes", 12),
        max_dependency_edges=kwargs.pop("max_dependency_edges", 16),
        max_target_files=kwargs.pop("max_target_files", 8),
        require_context_snapshot=kwargs.pop("require_context_snapshot", True),
        require_intent_scope_bundle=kwargs.pop("require_intent_scope_bundle", True),
        require_non_goal_register=kwargs.pop("require_non_goal_register", True),
        allow_reference_informed_patterns=kwargs.pop("allow_reference_informed_patterns", True),
        allow_future_diff_handoff=kwargs.pop("allow_future_diff_handoff", True),
        **kwargs,
    )


def default_patch_planning_policy() -> PatchPlanningPolicy:
    return build_patch_planning_policy()


def build_patch_planning_input(planning_input_id: str = "planning_input:v0.35.3", **kwargs: Any) -> PatchPlanningInput:
    return PatchPlanningInput(
        planning_input_id=planning_input_id,
        version=kwargs.pop("version", V0353_VERSION),
        intent_scope_bundle_id=kwargs.pop("intent_scope_bundle_id", "bundle:v0.35.1"),
        patch_context_snapshot_id=kwargs.pop("patch_context_snapshot_id", "context_snapshot:v0.35.2"),
        evidence_bundle_id=kwargs.pop("evidence_bundle_id", "evidence_bundle:v0.35.2"),
        reference_pattern_digest_id=kwargs.pop("reference_pattern_digest_id", "reference_pattern_digest:v0.35.0"),
        planning_mode=kwargs.pop("planning_mode", PatchPlanMode.COMBINED_CONTEXT_AND_REFERENCE_INFORMED),
        task_summary=kwargs.pop("task_summary", "Create non-mutating reference-informed patch plan metadata."),
        source_refs=kwargs.pop("source_refs", [build_patch_plan_source_ref()]),
        **kwargs,
    )


def build_patch_planning_input_from_context_snapshot(snapshot: PatchContextSnapshot, **kwargs: Any) -> PatchPlanningInput:
    return build_patch_planning_input(
        patch_context_snapshot_id=snapshot.context_snapshot_id,
        evidence_bundle_id=snapshot.evidence_bundle.evidence_bundle_id,
        **kwargs,
    )


def build_patch_change_node(change_node_id: str = "change_node:v0.35.3:model", **kwargs: Any) -> PatchChangeNode:
    return PatchChangeNode(
        change_node_id=change_node_id,
        change_kind=kwargs.pop("change_kind", PatchChangeKind.ADD_CONTRACT_MODEL),
        status=kwargs.pop("status", PatchChangeNodeStatus.PLANNED),
        title=kwargs.pop("title", "Add or extend contract model metadata."),
        rationale=kwargs.pop("rationale", "Planning artifact identifies a future non-mutating model change."),
        target_file_refs=kwargs.pop("target_file_refs", ["src/chanta_core/agent_runtime/patch_plan.py"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["dataclass", "validation helper"]),
        risk_kinds=kwargs.pop("risk_kinds", []),
        reference_pattern_use_ids=kwargs.pop("reference_pattern_use_ids", []),
        **kwargs,
    )


def build_patch_dependency_edge(dependency_edge_id: str = "dependency:v0.35.3:model_before_test", **kwargs: Any) -> PatchDependencyEdge:
    return PatchDependencyEdge(
        dependency_edge_id=dependency_edge_id,
        dependency_kind=kwargs.pop("dependency_kind", PatchDependencyKind.REQUIRES_MODEL_BEFORE_TEST),
        source_change_node_id=kwargs.pop("source_change_node_id", "change_node:v0.35.3:model"),
        target_change_node_id=kwargs.pop("target_change_node_id", "change_node:v0.35.3:test"),
        rationale=kwargs.pop("rationale", "Test planning depends on model planning metadata."),
        blocking=kwargs.pop("blocking", True),
        **kwargs,
    )


def build_patch_target_file_plan(target_file_plan_id: str = "target_file_plan:v0.35.3:model", **kwargs: Any) -> PatchTargetFilePlan:
    return PatchTargetFilePlan(
        target_file_plan_id=target_file_plan_id,
        target_path_ref=kwargs.pop("target_path_ref", "src/chanta_core/agent_runtime/patch_plan.py"),
        target_kind=kwargs.pop("target_kind", PatchTargetKind.SOURCE_FILE),
        planned_change_node_ids=kwargs.pop("planned_change_node_ids", ["change_node:v0.35.3:model"]),
        planned_role=kwargs.pop("planned_role", "future contract model target"),
        rationale=kwargs.pop("rationale", "Target file plan is metadata for future diff proposal only."),
        allowed_for_future_diff=kwargs.pop("allowed_for_future_diff", True),
        **kwargs,
    )


def build_patch_test_plan(test_plan_id: str = "test_plan:v0.35.3", **kwargs: Any) -> PatchTestPlan:
    return PatchTestPlan(
        test_plan_id=test_plan_id,
        related_change_node_ids=kwargs.pop("related_change_node_ids", ["change_node:v0.35.3:test"]),
        test_target_refs=kwargs.pop("test_target_refs", ["tests/test_v0353_reference_informed_patch_plan.py"]),
        test_strategy_summary=kwargs.pop("test_strategy_summary", "Future tests should validate metadata boundaries without execution readiness."),
        expected_test_coverage=kwargs.pop("expected_test_coverage", ["flags", "policy", "graph", "plan", "unsafe readiness"]),
        **kwargs,
    )


def build_patch_documentation_plan(documentation_plan_id: str = "doc_plan:v0.35.3", **kwargs: Any) -> PatchDocumentationPlan:
    return PatchDocumentationPlan(
        documentation_plan_id=documentation_plan_id,
        related_change_node_ids=kwargs.pop("related_change_node_ids", ["change_node:v0.35.3:doc"]),
        doc_target_refs=kwargs.pop("doc_target_refs", [DEFAULT_V0353_DOC_PATH]),
        documentation_summary=kwargs.pop("documentation_summary", "Future documentation should describe planning without diff/proposal/apply readiness."),
        expected_doc_updates=kwargs.pop("expected_doc_updates", ["release boundary", "taxonomy", "hard prohibitions"]),
        **kwargs,
    )


def build_patch_change_set_graph(change_set_graph_id: str = "change_set_graph:v0.35.3", **kwargs: Any) -> PatchChangeSetGraph:
    return PatchChangeSetGraph(
        change_set_graph_id=change_set_graph_id,
        version=kwargs.pop("version", V0353_VERSION),
        planning_input_id=kwargs.pop("planning_input_id", "planning_input:v0.35.3"),
        change_nodes=kwargs.pop("change_nodes", [build_patch_change_node(), build_patch_change_node("change_node:v0.35.3:test", change_kind=PatchChangeKind.ADD_TEST_CASE, title="Plan future test coverage"), build_patch_change_node("change_node:v0.35.3:doc", change_kind=PatchChangeKind.UPDATE_DOCUMENTATION, title="Plan future documentation update")]),
        dependency_edges=kwargs.pop("dependency_edges", [build_patch_dependency_edge()]),
        target_file_plans=kwargs.pop("target_file_plans", [build_patch_target_file_plan()]),
        test_plans=kwargs.pop("test_plans", [build_patch_test_plan()]),
        documentation_plans=kwargs.pop("documentation_plans", [build_patch_documentation_plan()]),
        status=kwargs.pop("status", PatchChangeSetGraphStatus.GRAPH_CREATED),
        summary=kwargs.pop("summary", "Change-set graph is planning metadata, not diff/proposal/apply."),
        ready_for_v0354_diff_proposal_envelope=kwargs.pop("ready_for_v0354_diff_proposal_envelope", True),
        **kwargs,
    )


def build_patch_plan(patch_plan_id: str = "patch_plan:v0.35.3", **kwargs: Any) -> PatchPlan:
    graph = kwargs.pop("change_set_graph", build_patch_change_set_graph())
    return PatchPlan(
        patch_plan_id=patch_plan_id,
        version=kwargs.pop("version", V0353_VERSION),
        planning_input_id=kwargs.pop("planning_input_id", graph.planning_input_id),
        plan_mode=kwargs.pop("plan_mode", PatchPlanMode.COMBINED_CONTEXT_AND_REFERENCE_INFORMED),
        status=kwargs.pop("status", PatchPlanStatus.PLAN_CREATED),
        readiness_level=kwargs.pop("readiness_level", PatchPlanReadinessLevel.REFERENCE_INFORMED_PLAN_READY),
        title=kwargs.pop("title", "Reference-informed non-mutating patch plan."),
        plan_summary=kwargs.pop("plan_summary", "Patch plan describes future changes without diff text, hunks, apply, or writes."),
        intent_id=kwargs.pop("intent_id", "intent:v0.35.1"),
        context_snapshot_id=kwargs.pop("context_snapshot_id", "context_snapshot:v0.35.2"),
        reference_digest_id=kwargs.pop("reference_digest_id", "reference_pattern_digest:v0.35.0"),
        change_set_graph=graph,
        reference_pattern_uses=kwargs.pop("reference_pattern_uses", [build_reference_informed_patch_pattern_use()]),
        risk_kinds=kwargs.pop("risk_kinds", [PatchPlanRiskKind.PATCH_DIFF_GENERATION_RISK]),
        gaps=kwargs.pop("gaps", []),
        ready_for_v0354_diff_proposal_envelope=kwargs.pop("ready_for_v0354_diff_proposal_envelope", True),
        ready_for_v0355_patch_risk_conformance_scanner=kwargs.pop("ready_for_v0355_patch_risk_conformance_scanner", True),
        **kwargs,
    )


def build_reference_informed_patch_pattern_uses_from_digest_and_context(digest: Any | None = None, context_snapshot: PatchContextSnapshot | None = None) -> list[ReferenceInformedPatchPatternUse]:
    uses: list[ReferenceInformedPatchPatternUse] = []
    patterns = list(getattr(digest, "patterns", []) or [])
    for index, pattern in enumerate(patterns):
        disposition = ReferencePatternDisposition(getattr(pattern, "disposition", ReferencePatternDisposition.UNKNOWN))
        rejected = disposition == ReferencePatternDisposition.REJECTED_FOR_SAFETY
        future = disposition == ReferencePatternDisposition.FUTURE_TRACK
        uses.append(
            build_reference_informed_patch_pattern_use(
                pattern_use_id=f"pattern_use:v0.35.3:{index}",
                source_pattern_id=getattr(pattern, "pattern_id", None),
                source_digest_id=getattr(digest, "digest_id", None),
                source_context_snapshot_id=getattr(context_snapshot, "context_snapshot_id", None),
                reference_name=str(getattr(pattern, "corpus_kind", "reference")),
                observed_pattern_summary=str(getattr(pattern, "pattern_summary", "Reference pattern metadata.")),
                planning_adaptation=str(getattr(pattern, "chantacore_adaptation", "Use as planning metadata only.")),
                applied_to_change_node_ids=["change_node:v0.35.3:model"] if not rejected else [],
                rejected=rejected,
                rejection_reason=getattr(pattern, "rejection_reason", None) if rejected else None,
                future_track=future,
                confidence=str(getattr(pattern, "confidence", "unknown")),
            )
        )
    for index, ref_summary in enumerate(list(getattr(context_snapshot, "reference_summaries", []) or [])):
        uses.append(
            build_reference_informed_patch_pattern_use(
                pattern_use_id=f"pattern_use:v0.35.3:context:{index}",
                source_pattern_id=None,
                source_digest_id=None,
                source_context_snapshot_id=getattr(context_snapshot, "context_snapshot_id", None),
                reference_name=str(getattr(ref_summary, "corpus_kind", "context_reference")),
                observed_pattern_summary=str(getattr(ref_summary, "summary", "Context reference summary metadata.")),
                planning_adaptation="Use context reference summary as planning metadata only.",
                applied_to_change_node_ids=["change_node:v0.35.3:model"],
                rejected=False,
                rejection_reason=None,
                future_track=False,
                confidence="medium",
            )
        )
    return uses


def build_patch_change_set_graph_from_intent_context(intent_scope_bundle: PatchIntentScopeBundle | None = None, context_snapshot: PatchContextSnapshot | None = None, policy: PatchPlanningPolicy | None = None) -> PatchChangeSetGraph:
    policy = policy or default_patch_planning_policy()
    gaps: list[str] = []
    nodes: list[PatchChangeNode] = []
    if intent_scope_bundle is None and policy.require_intent_scope_bundle:
        gaps.append("missing intent scope bundle")
    if context_snapshot is None and policy.require_context_snapshot:
        gaps.append("missing context snapshot")
    if gaps:
        nodes.append(
            build_patch_change_node(
                "change_node:v0.35.3:blocked",
                change_kind=PatchChangeKind.NO_OP_CHANGE,
                status=PatchChangeNodeStatus.BLOCKED,
                title="Planning blocked due to missing required metadata.",
                rationale="Missing context or intent metadata must produce gaps instead of unsafe expansion.",
                target_file_refs=[],
                expected_artifacts=[],
                risk_kinds=[PatchPlanRiskKind.INSUFFICIENT_CONTEXT_RISK],
                blocked_reason="; ".join(gaps),
            )
        )
        return build_patch_change_set_graph(change_nodes=nodes, dependency_edges=[], target_file_plans=[], test_plans=[], documentation_plans=[], status=PatchChangeSetGraphStatus.BLOCKED, summary="Change-set graph blocked due to missing metadata.")
    target_refs = []
    if context_snapshot is not None:
        target_refs = [summary.path_ref for summary in context_snapshot.file_summaries[: policy.max_target_files]]
    nodes = [
        build_patch_change_node(target_file_refs=target_refs[:1] or ["src/chanta_core/agent_runtime/patch_plan.py"]),
        build_patch_change_node("change_node:v0.35.3:test", change_kind=PatchChangeKind.ADD_TEST_CASE, title="Plan future test coverage", target_file_refs=["tests/test_v0353_reference_informed_patch_plan.py"]),
        build_patch_change_node("change_node:v0.35.3:doc", change_kind=PatchChangeKind.UPDATE_DOCUMENTATION, title="Plan future documentation update", target_file_refs=[DEFAULT_V0353_DOC_PATH]),
    ]
    return build_patch_change_set_graph(change_nodes=nodes[: policy.max_change_nodes])


def build_patch_plan_validation_finding(finding_id: str = "plan_finding:v0.35.3:ok", **kwargs: Any) -> PatchPlanValidationFinding:
    return PatchPlanValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchPlanDecisionKind.ALLOW_PLAN_METADATA),
        risk_kinds=kwargs.pop("risk_kinds", []),
        message=kwargs.pop("message", "Patch plan remains metadata only."),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_plan_validation_report(validation_report_id: str = "plan_validation:v0.35.3", **kwargs: Any) -> PatchPlanValidationReport:
    findings = kwargs.pop("findings", [build_patch_plan_validation_finding()])
    return PatchPlanValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0353_VERSION),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Plan validation does not certify execution, diff, or proposal readiness."),
        **kwargs,
    )


def build_patch_change_set_validation_finding(finding_id: str = "graph_finding:v0.35.3:ok", **kwargs: Any) -> PatchChangeSetValidationFinding:
    return PatchChangeSetValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchPlanDecisionKind.ALLOW_CHANGE_SET_GRAPH_METADATA),
        risk_kinds=kwargs.pop("risk_kinds", []),
        message=kwargs.pop("message", "Change-set graph remains metadata only."),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_change_set_validation_report(validation_report_id: str = "graph_validation:v0.35.3", **kwargs: Any) -> PatchChangeSetValidationReport:
    findings = kwargs.pop("findings", [build_patch_change_set_validation_finding()])
    return PatchChangeSetValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0353_VERSION),
        change_set_graph_id=kwargs.pop("change_set_graph_id", "change_set_graph:v0.35.3"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Graph validation does not certify execution, diff, or proposal readiness."),
        **kwargs,
    )


def build_patch_plan_report(report_id: str = "plan_report:v0.35.3", **kwargs: Any) -> PatchPlanReport:
    return PatchPlanReport(
        report_id=report_id,
        version=kwargs.pop("version", V0353_VERSION),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        change_set_graph_id=kwargs.pop("change_set_graph_id", "change_set_graph:v0.35.3"),
        summary=kwargs.pop("summary", "Patch plan report marks plan/graph metadata ready only."),
        plan_ready=kwargs.pop("plan_ready", True),
        change_set_graph_ready=kwargs.pop("change_set_graph_ready", True),
        reference_informed_plan_ready=kwargs.pop("reference_informed_plan_ready", True),
        gap_items=kwargs.pop("gap_items", []),
        **kwargs,
    )


def build_patch_plan_run_preview(run_preview_id: str = "plan_run_preview:v0.35.3", **kwargs: Any) -> PatchPlanRunPreview:
    return PatchPlanRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["validate supplied metadata", "create change nodes", "create dependency edges", "create plan report"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["PatchPlan", "PatchChangeSetGraph", "PatchPlanReport"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["diff proposal", "patch proposal", "patch hunk generation", "patch apply", "workspace write", "test execution"]),
        **kwargs,
    )


def build_patch_plan_no_diff_no_apply_guarantee(guarantee_id: str = "no_diff_no_apply:v0.35.3", **kwargs: Any) -> PatchPlanNoDiffNoApplyGuarantee:
    return PatchPlanNoDiffNoApplyGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0353_VERSION), **kwargs)


def build_v0353_readiness_report(report_id: str = "readiness:v0.35.3", **kwargs: Any) -> V0353ReadinessReport:
    return V0353ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0353_VERSION),
        patch_plan_id=kwargs.pop("patch_plan_id", "patch_plan:v0.35.3"),
        summary=kwargs.pop("summary", "v0.35.3 is ready for v0.35.4/v0.35.5 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["PatchPlan", "PatchChangeSetGraph", "Change nodes", "Dependency edges", "Target/test/doc plans"]),
        blocked_items=kwargs.pop("blocked_items", ["diff proposal", "patch proposal", "patch hunk generation", "patch application", "workspace write"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.4 Diff Proposal Envelope", "v0.35.5 Patch Risk & Conformance Scanner"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0353_DOC_PATH, DEFAULT_V0352_CONTEXT_DOC_REF, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["Any diff/proposal/hunk/apply/write/execution path is introduced."]),
        **kwargs,
    )


def validate_patch_change_set_graph(graph: PatchChangeSetGraph) -> PatchChangeSetValidationReport:
    findings: list[PatchChangeSetValidationFinding] = []
    if not patch_change_set_graph_is_not_diff_proposal(graph):
        findings.append(
            build_patch_change_set_validation_finding(
                "graph_finding:unsafe_ready",
                decision_kind=PatchPlanDecisionKind.BLOCK,
                risk_kinds=[PatchPlanRiskKind.PATCH_DIFF_GENERATION_RISK],
                message="Graph cannot be diff/proposal/execution ready.",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_patch_change_set_validation_finding())
    return build_patch_change_set_validation_report(change_set_graph_id=graph.change_set_graph_id, findings=findings)


def validate_patch_plan(plan: PatchPlan) -> PatchPlanValidationReport:
    findings: list[PatchPlanValidationFinding] = []
    if not patch_plan_is_not_patch_proposal(plan):
        findings.append(
            build_patch_plan_validation_finding(
                "plan_finding:unsafe_ready",
                decision_kind=PatchPlanDecisionKind.BLOCK,
                risk_kinds=[PatchPlanRiskKind.PATCH_DIFF_GENERATION_RISK, PatchPlanRiskKind.PATCH_APPLY_RISK],
                message="Plan cannot be diff/proposal/apply/execution ready.",
                blocks_validation=True,
            )
        )
    if plan.gaps:
        findings.append(
            build_patch_plan_validation_finding(
                "plan_finding:gaps",
                decision_kind=PatchPlanDecisionKind.REQUIRE_REVIEW,
                risk_kinds=[PatchPlanRiskKind.INSUFFICIENT_CONTEXT_RISK],
                message="Plan contains gaps and requires review before future handoff.",
                blocks_validation=False,
            )
        )
    if not findings:
        findings.append(build_patch_plan_validation_finding())
    return build_patch_plan_validation_report(patch_plan_id=plan.patch_plan_id, findings=findings)


def patch_plan_flags_preserve_no_diff_no_apply(flags: PatchPlanFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_PLAN_FLAG_NAMES) and flags.production_certified is False


def patch_planning_policy_blocks_diff_apply(policy: PatchPlanningPolicy) -> bool:
    return (
        policy.allow_diff_text is False
        and policy.allow_patch_hunks is False
        and policy.allow_patch_apply is False
        and policy.allow_workspace_write is False
        and policy.allow_code_edit is False
        and policy.allow_test_execution is False
        and policy.allow_dependency_install is False
        and policy.allow_shell is False
    )


def patch_change_set_graph_is_not_diff_proposal(graph: PatchChangeSetGraph) -> bool:
    return graph.ready_for_diff_proposal is False and graph.ready_for_patch_proposal is False and graph.ready_for_execution is False


def patch_plan_is_not_patch_proposal(plan: PatchPlan) -> bool:
    return plan.ready_for_diff_proposal is False and plan.ready_for_patch_proposal is False and plan.ready_for_patch_application is False and plan.ready_for_execution is False


def v0353_readiness_report_is_not_execution_ready(report: V0353ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_PATCH_PLAN_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
