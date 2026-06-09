from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list
from .patch_proposal_boundary import (
    PatchProposalCapabilityKind,
    PatchProposalSurfaceKind,
    ReferenceHarnessPatternKind,
    ReferencePatternDisposition,
)


V0351_VERSION = "v0.35.1"
V0351_RELEASE_NAME = "v0.35.1 Patch Intent & Scope Policy"
V035_TRACK_NAME = "Controlled Patch Proposal Layer"
DEFAULT_V0350_DIGEST_REF = "docs/versions/v0.35/v0.35.0_reference_pattern_digest.md"
DEFAULT_V0351_DOC_PATH = "docs/versions/v0.35/v0.35.1_patch_intent_scope_policy.md"

UNSAFE_PATCH_INTENT_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_patch_context_collection",
    "ready_for_patch_plan",
    "ready_for_diff_proposal",
    "ready_for_patch_proposal",
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

DEFAULT_NON_GOAL_CAPABILITIES = [
    PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY,
    PatchProposalCapabilityKind.WRITE_WORKSPACE_FILE,
    PatchProposalCapabilityKind.EDIT_CODE_FILE,
    PatchProposalCapabilityKind.RUN_GIT_APPLY,
    PatchProposalCapabilityKind.RUN_APPLY_PATCH,
    PatchProposalCapabilityKind.RUN_TESTS,
    PatchProposalCapabilityKind.EXECUTE_SHELL,
    PatchProposalCapabilityKind.INSTALL_DEPENDENCY,
    PatchProposalCapabilityKind.EXECUTE_REFERENCE_HARNESS,
]

DEFAULT_WITHDRAWAL_CONDITIONS = [
    "Any patch context collection, patch planning, diff proposal, or patch proposal generation path is introduced.",
    "Any patch application, workspace write, code edit, apply_patch, or git apply path is introduced.",
    "Any shell, subprocess, command, test, dependency install, provider, network, credential, or secret path is introduced.",
    "Any reference execution/import/install path or unsafe readiness flag is introduced.",
]


class PatchIntentKind(StrEnum):
    ADD_MISSING_CONTRACT_MODEL = "add_missing_contract_model"
    EXTEND_VALIDATION_RULE = "extend_validation_rule"
    TIGHTEN_SAFETY_BOUNDARY = "tighten_safety_boundary"
    ADD_TEST_COVERAGE = "add_test_coverage"
    UPDATE_DOCUMENTATION = "update_documentation"
    REFACTOR_WITHOUT_BEHAVIOR_CHANGE = "refactor_without_behavior_change"
    ALIGN_WITH_REFERENCE_PATTERN = "align_with_reference_pattern"
    FIX_INCONSISTENCY = "fix_inconsistency"
    CONSOLIDATE_RELEASE_ARTIFACT = "consolidate_release_artifact"
    PREPARE_FUTURE_TRACK = "prepare_future_track"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchIntentSourceKind(StrEnum):
    V0350_BOUNDARY = "v0350_boundary"
    V0350_REFERENCE_PATTERN_DIGEST = "v0350_reference_pattern_digest"
    V0349_HANDOFF_PACKET = "v0349_handoff_packet"
    V0348_CLI_MODEL_BACKED_SURFACE = "v0348_cli_model_backed_surface"
    USER_REQUEST = "user_request"
    MODEL_BACKED_STEP_OUTPUT = "model_backed_step_output"
    REFERENCE_PATTERN_ADAPTATION = "reference_pattern_adaptation"
    MANUAL_DESIGN_NOTE = "manual_design_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class PatchIntentStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    INTENT_CREATED = "intent_created"
    INTENT_VALIDATED = "intent_validated"
    INTENT_VALIDATED_WITH_GAPS = "intent_validated_with_gaps"
    SCOPE_ATTACHED = "scope_attached"
    BLOCKED = "blocked"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATED = "future_gated"
    NO_OP = "no_op"


class PatchIntentReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    INTENT_CONTRACT_READY = "intent_contract_ready"
    SCOPE_POLICY_READY = "scope_policy_ready"
    INTENT_SCOPE_BUNDLE_READY = "intent_scope_bundle_ready"
    DESIGN_HANDOFF_READY_FOR_V0352 = "design_handoff_ready_for_v0352"
    DESIGN_HANDOFF_READY_FOR_V0353 = "design_handoff_ready_for_v0353"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class PatchIntentDecisionKind(StrEnum):
    ALLOW_INTENT_METADATA = "allow_intent_metadata"
    ALLOW_SCOPE_METADATA = "allow_scope_metadata"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class PatchIntentRiskKind(StrEnum):
    VAGUE_INTENT_RISK = "vague_intent_risk"
    OVERBROAD_SCOPE_RISK = "overbroad_scope_risk"
    UNSAFE_REFERENCE_PATTERN_RISK = "unsafe_reference_pattern_risk"
    PATCH_APPLY_RISK = "patch_apply_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    TEST_EXECUTION_RISK = "test_execution_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    CREDENTIAL_EXPOSURE_RISK = "credential_exposure_risk"
    SECRET_EXPOSURE_RISK = "secret_exposure_risk"
    PROVIDER_NETWORK_OPENING_RISK = "provider_network_opening_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    AUTONOMOUS_LOOP_RISK = "autonomous_loop_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    UNKNOWN = "unknown"


class PatchScopeKind(StrEnum):
    SOURCE_MODULE_SCOPE = "source_module_scope"
    TEST_MODULE_SCOPE = "test_module_scope"
    DOCUMENTATION_SCOPE = "documentation_scope"
    VERSION_DOC_SCOPE = "version_doc_scope"
    AGENT_RUNTIME_SCOPE = "agent_runtime_scope"
    REFERENCE_DIGEST_SCOPE = "reference_digest_scope"
    READ_ONLY_REFERENCE_SCOPE = "read_only_reference_scope"
    BLOCKED_REFERENCE_EXECUTION_SCOPE = "blocked_reference_execution_scope"
    BLOCKED_SECRET_SCOPE = "blocked_secret_scope"
    BLOCKED_EXTERNAL_SCOPE = "blocked_external_scope"
    NO_OP_SCOPE = "no_op_scope"
    UNKNOWN = "unknown"


class PatchTargetKind(StrEnum):
    SOURCE_FILE = "source_file"
    TEST_FILE = "test_file"
    DOCUMENTATION_FILE = "documentation_file"
    VERSION_DOCUMENT = "version_document"
    PACKAGE_METADATA = "package_metadata"
    REFERENCE_DIGEST_DOCUMENT = "reference_digest_document"
    REFERENCE_CORPUS_PATH = "reference_corpus_path"
    SECRET_LIKE_FILE = "secret_like_file"
    CREDENTIAL_LIKE_FILE = "credential_like_file"
    BINARY_FILE = "binary_file"
    EXTERNAL_PATH = "external_path"
    UNKNOWN = "unknown"


class PatchScopeDecisionKind(StrEnum):
    ALLOW_SCOPE_METADATA = "allow_scope_metadata"
    ALLOW_TARGET_SELECTOR_METADATA = "allow_target_selector_metadata"
    ALLOW_FUTURE_READONLY_CONTEXT_COLLECTION = "allow_future_readonly_context_collection"
    BLOCK_TARGET = "block_target"
    BLOCK_SCOPE = "block_scope"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class PatchScopeRiskKind(StrEnum):
    OUTSIDE_ROOT_RISK = "outside_root_risk"
    SCOPE_ESCAPE_RISK = "scope_escape_risk"
    SECRET_PATH_RISK = "secret_path_risk"
    CREDENTIAL_PATH_RISK = "credential_path_risk"
    BINARY_PATH_RISK = "binary_path_risk"
    REFERENCE_EXECUTION_RISK = "reference_execution_risk"
    PACKAGE_METADATA_RISK = "package_metadata_risk"
    TEST_DELETION_RISK = "test_deletion_risk"
    SAFETY_DOC_DELETION_RISK = "safety_doc_deletion_risk"
    BROAD_GLOB_RISK = "broad_glob_risk"
    AMBIGUOUS_TARGET_RISK = "ambiguous_target_risk"
    UNKNOWN = "unknown"


class PatchIntentPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"
    DEFERRED = "deferred"
    UNKNOWN = "unknown"


def _validate_version(value: str) -> None:
    _require_non_blank("version", value)
    if V0351_VERSION not in value:
        raise ValueError("version must include v0.35.1")


def _validate_metadata_safe(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be a dict")
    for key in metadata:
        lower = str(key).lower()
        if any(token in lower for token in ("secret", "credential", "api_key", "token", "password")):
            raise ValueError("metadata must not contain credential or secret-like keys")


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
            raise ValueError(f"{name} must always be False in v0.35.1")


@dataclass(frozen=True)
class PatchIntentFlagSet:
    flag_set_id: str
    version: str
    patch_intent_layer_constructed: bool
    patch_scope_policy_defined: bool
    target_selector_defined: bool
    non_goal_register_defined: bool
    reference_digest_consumed: bool
    ready_for_v0352_readonly_patch_context_collector: bool
    ready_for_v0353_reference_informed_patch_plan: bool
    ready_for_patch_intent_artifact: bool
    ready_for_patch_scope_policy: bool
    ready_for_execution: bool = False
    ready_for_patch_context_collection: bool = False
    ready_for_patch_plan: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
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
        _validate_false(self, UNSAFE_PATCH_INTENT_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentSourceRef:
    source_ref_id: str
    source_kind: PatchIntentSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        PatchIntentSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchReferencePatternUse:
    pattern_use_id: str
    source_pattern_id: str | None
    source_digest_id: str | None
    reference_name: str
    observed_pattern_summary: str
    adapted_intent_kind: PatchIntentKind | str
    adapted_scope_note: str
    rejected: bool
    rejection_reason: str | None
    future_track: bool
    confidence: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("pattern_use_id", self.pattern_use_id)
        if self.source_pattern_id is not None:
            _require_non_blank("source_pattern_id", self.source_pattern_id)
        if self.source_digest_id is not None:
            _require_non_blank("source_digest_id", self.source_digest_id)
        _require_non_blank("reference_name", self.reference_name)
        _require_non_blank("observed_pattern_summary", self.observed_pattern_summary)
        PatchIntentKind(self.adapted_intent_kind)
        _require_non_blank("adapted_scope_note", self.adapted_scope_note)
        if self.rejected and not self.rejection_reason:
            raise ValueError("rejected pattern uses must include rejection_reason")
        _require_non_blank("confidence", self.confidence)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentEnvelope:
    intent_id: str
    version: str
    intent_kind: PatchIntentKind | str
    status: PatchIntentStatus | str
    readiness_level: PatchIntentReadinessLevel | str
    priority: PatchIntentPriority | str
    title: str
    problem_statement: str
    rationale: str
    expected_outcome: str
    non_goals_summary: str
    source_refs: list[PatchIntentSourceRef] = field(default_factory=list)
    reference_pattern_uses: list[PatchReferencePatternUse] = field(default_factory=list)
    risk_kinds: list[PatchIntentRiskKind | str] = field(default_factory=list)
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("intent_id", self.intent_id)
        _validate_version(self.version)
        PatchIntentKind(self.intent_kind)
        PatchIntentStatus(self.status)
        PatchIntentReadinessLevel(self.readiness_level)
        PatchIntentPriority(self.priority)
        for name in ("title", "problem_statement", "rationale", "expected_outcome", "non_goals_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_list("source_refs", self.source_refs)
        _validate_list("reference_pattern_uses", self.reference_pattern_uses)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchIntentRiskKind)
        _validate_false(self, ("ready_for_patch_proposal", "ready_for_patch_application", "ready_for_execution"))
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchScopePolicy:
    scope_policy_id: str
    version: str
    scope_kind: PatchScopeKind | str
    allowed_root_refs: list[str] = field(default_factory=list)
    blocked_root_refs: list[str] = field(default_factory=list)
    allowed_path_patterns: list[str] = field(default_factory=list)
    blocked_path_patterns: list[str] = field(default_factory=list)
    allowed_target_kinds: list[PatchTargetKind | str] = field(default_factory=list)
    blocked_target_kinds: list[PatchTargetKind | str] = field(default_factory=list)
    max_target_files: int = 8
    max_scope_depth: int = 4
    allow_source_targets: bool = True
    allow_test_targets: bool = True
    allow_doc_targets: bool = True
    allow_reference_targets_for_readonly_context: bool = True
    allow_secret_targets: bool = False
    allow_credential_targets: bool = False
    allow_binary_targets: bool = False
    allow_external_targets: bool = False
    allow_workspace_write: bool = False
    allow_code_edit: bool = False
    allow_patch_application: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("scope_policy_id", self.scope_policy_id)
        _validate_version(self.version)
        PatchScopeKind(self.scope_kind)
        for name in ("allowed_root_refs", "blocked_root_refs", "allowed_path_patterns", "blocked_path_patterns"):
            _validate_string_list(name, getattr(self, name))
        _validate_enum_list("allowed_target_kinds", self.allowed_target_kinds, PatchTargetKind)
        _validate_enum_list("blocked_target_kinds", self.blocked_target_kinds, PatchTargetKind)
        if self.max_target_files < 0 or self.max_scope_depth < 0:
            raise ValueError("scope numeric limits must be >= 0")
        for name in (
            "allow_secret_targets",
            "allow_credential_targets",
            "allow_binary_targets",
            "allow_external_targets",
            "allow_workspace_write",
            "allow_code_edit",
            "allow_patch_application",
        ):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.35.1")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchTargetSelector:
    selector_id: str
    scope_policy_id: str
    target_kind: PatchTargetKind | str
    target_path_ref: str
    target_summary: str
    selected_for_future_context: bool
    selected_for_future_patch_proposal: bool = False
    selected_for_write: bool = False
    blocked: bool = False
    block_reason: str | None = None
    risk_kinds: list[PatchScopeRiskKind | str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("selector_id", "scope_policy_id", "target_path_ref", "target_summary"):
            _require_non_blank(name, getattr(self, name))
        PatchTargetKind(self.target_kind)
        if self.selected_for_future_patch_proposal is not False:
            raise ValueError("selected_for_future_patch_proposal must be False in v0.35.1")
        if self.selected_for_write is not False:
            raise ValueError("selected_for_write must always be False")
        if self.blocked and not self.block_reason:
            raise ValueError("blocked selectors must include block_reason")
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchScopeRiskKind)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchAllowedTarget:
    allowed_target_id: str
    selector_id: str
    target_kind: PatchTargetKind | str
    target_path_ref: str
    allow_future_readonly_context: bool
    allow_future_patch_proposal: bool = False
    allow_write: bool = False
    allow_apply: bool = False
    reason: str = "Allowed only as future read-only context metadata."
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("allowed_target_id", "selector_id", "target_path_ref", "reason"):
            _require_non_blank(name, getattr(self, name))
        PatchTargetKind(self.target_kind)
        if self.allow_future_patch_proposal is not False:
            raise ValueError("allow_future_patch_proposal must be False in v0.35.1")
        if self.allow_write is not False or self.allow_apply is not False:
            raise ValueError("allow_write and allow_apply must always be False")
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchBlockedTarget:
    blocked_target_id: str
    selector_id: str | None
    target_kind: PatchTargetKind | str
    target_path_ref: str
    risk_kinds: list[PatchScopeRiskKind | str]
    reason: str
    safe_alternative: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocked_target_id", self.blocked_target_id)
        if self.selector_id is not None:
            _require_non_blank("selector_id", self.selector_id)
        PatchTargetKind(self.target_kind)
        _require_non_blank("target_path_ref", self.target_path_ref)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchScopeRiskKind)
        _require_non_blank("reason", self.reason)
        _require_non_blank("safe_alternative", self.safe_alternative)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchNonGoal:
    non_goal_id: str
    title: str
    description: str
    blocked_capability: PatchProposalCapabilityKind | str
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("non_goal_id", "title", "description", "reason"):
            _require_non_blank(name, getattr(self, name))
        PatchProposalCapabilityKind(self.blocked_capability)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchNonGoalRegister:
    register_id: str
    version: str
    non_goals: list[PatchNonGoal]
    prohibited_capabilities: list[PatchProposalCapabilityKind | str]
    prohibited_surfaces: list[PatchProposalSurfaceKind | str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("register_id", self.register_id)
        _validate_version(self.version)
        _validate_list("non_goals", self.non_goals)
        _validate_enum_list("prohibited_capabilities", self.prohibited_capabilities, PatchProposalCapabilityKind)
        _validate_enum_list("prohibited_surfaces", self.prohibited_surfaces, PatchProposalSurfaceKind)
        required = set(DEFAULT_NON_GOAL_CAPABILITIES)
        if not required.issubset({PatchProposalCapabilityKind(item) for item in self.prohibited_capabilities}):
            raise ValueError("prohibited_capabilities must include apply/write/edit/shell/test/install/reference execution")
        _require_non_blank("summary", self.summary)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentValidationFinding:
    finding_id: str
    decision_kind: PatchIntentDecisionKind | str
    risk_kinds: list[PatchIntentRiskKind | str]
    message: str
    blocks_validation: bool
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        PatchIntentDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchIntentRiskKind)
        _require_non_blank("message", self.message)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentValidationReport:
    report_id: str
    version: str
    intent_id: str
    findings: list[PatchIntentValidationFinding]
    valid: bool
    summary: str
    ready_for_execution: bool = False
    ready_for_patch_proposal: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "intent_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        _validate_false(self, ("ready_for_execution", "ready_for_patch_proposal"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchScopeValidationFinding:
    finding_id: str
    decision_kind: PatchScopeDecisionKind | str
    risk_kinds: list[PatchScopeRiskKind | str]
    message: str
    blocks_validation: bool
    target_ref: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        PatchScopeDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, PatchScopeRiskKind)
        _require_non_blank("message", self.message)
        if self.target_ref is not None:
            _require_non_blank("target_ref", self.target_ref)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchScopeValidationReport:
    report_id: str
    version: str
    scope_policy_id: str
    findings: list[PatchScopeValidationFinding]
    valid: bool
    summary: str
    ready_for_execution: bool = False
    ready_for_file_access: bool = False
    ready_for_write: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "scope_policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_list("findings", self.findings)
        _validate_false(self, ("ready_for_execution", "ready_for_file_access", "ready_for_write"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentScopeBundle:
    bundle_id: str
    version: str
    intent: PatchIntentEnvelope
    scope_policy: PatchScopePolicy
    target_selectors: list[PatchTargetSelector]
    allowed_targets: list[PatchAllowedTarget]
    blocked_targets: list[PatchBlockedTarget]
    non_goal_register: PatchNonGoalRegister
    reference_pattern_uses: list[PatchReferencePatternUse]
    intent_validation_report: PatchIntentValidationReport
    scope_validation_report: PatchScopeValidationReport
    status: PatchIntentStatus | str
    readiness_level: PatchIntentReadinessLevel | str
    summary: str
    ready_for_patch_context_collection: bool = False
    ready_for_patch_plan: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("bundle_id", self.bundle_id)
        _validate_version(self.version)
        for name in ("target_selectors", "allowed_targets", "blocked_targets", "reference_pattern_uses"):
            _validate_list(name, getattr(self, name))
        PatchIntentStatus(self.status)
        PatchIntentReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        _validate_false(
            self,
            (
                "ready_for_patch_context_collection",
                "ready_for_patch_plan",
                "ready_for_diff_proposal",
                "ready_for_patch_proposal",
                "ready_for_patch_application",
                "ready_for_execution",
            ),
        )
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentScopeReport:
    report_id: str
    version: str
    bundle_id: str
    status: PatchIntentStatus | str
    readiness_level: PatchIntentReadinessLevel | str
    summary: str
    intent_valid: bool
    scope_valid: bool
    selector_count: int
    blocked_target_count: int
    non_goal_count: int
    ready_for_patch_context_collection: bool = False
    ready_for_patch_plan: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "bundle_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        PatchIntentStatus(self.status)
        PatchIntentReadinessLevel(self.readiness_level)
        for name in ("selector_count", "blocked_target_count", "non_goal_count"):
            if getattr(self, name) < 0:
                raise ValueError(f"{name} must be >= 0")
        _validate_false(self, ("ready_for_patch_context_collection", "ready_for_patch_plan", "ready_for_patch_proposal", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_safe(self.metadata)


@dataclass(frozen=True)
class PatchIntentScopeRunPreview:
    run_preview_id: str
    planned_steps: list[str]
    expected_artifacts: list[str]
    explicitly_not_performed: list[str]
    no_context_collection_guarantee: bool = True
    no_patch_plan_guarantee: bool = True
    no_diff_proposal_guarantee: bool = True
    no_patch_proposal_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_test_execution_guarantee: bool = True
    no_dependency_install_guarantee: bool = True
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
class PatchIntentScopeNoApplyGuarantee:
    guarantee_id: str
    version: str
    no_context_collection: bool = True
    no_patch_plan: bool = True
    no_diff_proposal: bool = True
    no_patch_proposal: bool = True
    no_patch_application: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_apply_patch_runtime_call: bool = True
    no_git_apply_runtime_call: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_test_execution: bool = True
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
class V0351ReadinessReport:
    report_id: str
    version: str
    bundle_id: str | None
    summary: str
    completed_items: list[str]
    blocked_items: list[str]
    future_track_items: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0352_readonly_patch_context_collector: bool = True
    ready_for_v0353_reference_informed_patch_plan: bool = True
    ready_for_patch_intent_artifact: bool = True
    ready_for_patch_scope_policy: bool = True
    ready_for_execution: bool = False
    ready_for_patch_context_collection: bool = False
    ready_for_patch_plan: bool = False
    ready_for_diff_proposal: bool = False
    ready_for_patch_proposal: bool = False
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
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version(self.version)
        if self.bundle_id is not None:
            _require_non_blank("bundle_id", self.bundle_id)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        unsafe_names = tuple(name for name in UNSAFE_PATCH_INTENT_FLAG_NAMES if hasattr(self, name))
        _validate_false(self, unsafe_names)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False")
        _validate_metadata_safe(self.metadata)


def build_patch_intent_flags(flag_set_id: str = "patch_intent_flags:v0.35.1", **kwargs: Any) -> PatchIntentFlagSet:
    return PatchIntentFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0351_VERSION),
        patch_intent_layer_constructed=kwargs.pop("patch_intent_layer_constructed", True),
        patch_scope_policy_defined=kwargs.pop("patch_scope_policy_defined", True),
        target_selector_defined=kwargs.pop("target_selector_defined", True),
        non_goal_register_defined=kwargs.pop("non_goal_register_defined", True),
        reference_digest_consumed=kwargs.pop("reference_digest_consumed", True),
        ready_for_v0352_readonly_patch_context_collector=kwargs.pop("ready_for_v0352_readonly_patch_context_collector", True),
        ready_for_v0353_reference_informed_patch_plan=kwargs.pop("ready_for_v0353_reference_informed_patch_plan", True),
        ready_for_patch_intent_artifact=kwargs.pop("ready_for_patch_intent_artifact", True),
        ready_for_patch_scope_policy=kwargs.pop("ready_for_patch_scope_policy", True),
        **kwargs,
    )


def build_patch_intent_source_ref(source_ref_id: str = "source:v0.35.1:digest", **kwargs: Any) -> PatchIntentSourceRef:
    return PatchIntentSourceRef(
        source_ref_id=source_ref_id,
        source_kind=kwargs.pop("source_kind", PatchIntentSourceKind.V0350_REFERENCE_PATTERN_DIGEST),
        source_id=kwargs.pop("source_id", DEFAULT_V0350_DIGEST_REF),
        source_summary=kwargs.pop("source_summary", "v0.35.0 ReferencePatternDigest consumed as metadata only."),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0350_DIGEST_REF]),
        **kwargs,
    )


def build_patch_reference_pattern_use(pattern_use_id: str = "pattern_use:v0.35.1", **kwargs: Any) -> PatchReferencePatternUse:
    return PatchReferencePatternUse(
        pattern_use_id=pattern_use_id,
        source_pattern_id=kwargs.pop("source_pattern_id", "pattern:reference:v0.35.0"),
        source_digest_id=kwargs.pop("source_digest_id", "reference_pattern_digest:v0.35.0"),
        reference_name=kwargs.pop("reference_name", "ReferencePatternDigest"),
        observed_pattern_summary=kwargs.pop("observed_pattern_summary", "Reference-informed pattern summarized as metadata."),
        adapted_intent_kind=kwargs.pop("adapted_intent_kind", PatchIntentKind.ALIGN_WITH_REFERENCE_PATTERN),
        adapted_scope_note=kwargs.pop("adapted_scope_note", "Use only to shape future read-only scope metadata."),
        rejected=kwargs.pop("rejected", False),
        rejection_reason=kwargs.pop("rejection_reason", None),
        future_track=kwargs.pop("future_track", False),
        confidence=kwargs.pop("confidence", "medium"),
        **kwargs,
    )


def build_patch_intent_envelope(intent_id: str = "intent:v0.35.1", **kwargs: Any) -> PatchIntentEnvelope:
    return PatchIntentEnvelope(
        intent_id=intent_id,
        version=kwargs.pop("version", V0351_VERSION),
        intent_kind=kwargs.pop("intent_kind", PatchIntentKind.ALIGN_WITH_REFERENCE_PATTERN),
        status=kwargs.pop("status", PatchIntentStatus.INTENT_VALIDATED),
        readiness_level=kwargs.pop("readiness_level", PatchIntentReadinessLevel.INTENT_CONTRACT_READY),
        priority=kwargs.pop("priority", PatchIntentPriority.NORMAL),
        title=kwargs.pop("title", "Define patch intent and scope metadata."),
        problem_statement=kwargs.pop("problem_statement", "Future patch proposal work needs bounded intent and scope metadata before context collection."),
        rationale=kwargs.pop("rationale", "Intent and scope boundaries reduce accidental expansion into write/apply behavior."),
        expected_outcome=kwargs.pop("expected_outcome", "A validated metadata artifact for future read-only context collection."),
        non_goals_summary=kwargs.pop("non_goals_summary", "No context collection, planning, diff generation, patch proposal, write, or apply."),
        source_refs=kwargs.pop("source_refs", [build_patch_intent_source_ref()]),
        reference_pattern_uses=kwargs.pop("reference_pattern_uses", [build_patch_reference_pattern_use()]),
        risk_kinds=kwargs.pop("risk_kinds", [PatchIntentRiskKind.OVERBROAD_SCOPE_RISK]),
        **kwargs,
    )


def build_patch_scope_policy(scope_policy_id: str = "scope_policy:v0.35.1", **kwargs: Any) -> PatchScopePolicy:
    return PatchScopePolicy(
        scope_policy_id=scope_policy_id,
        version=kwargs.pop("version", V0351_VERSION),
        scope_kind=kwargs.pop("scope_kind", PatchScopeKind.AGENT_RUNTIME_SCOPE),
        allowed_root_refs=kwargs.pop("allowed_root_refs", ["src/chanta_core/agent_runtime", "tests", "docs/versions/v0.35"]),
        blocked_root_refs=kwargs.pop("blocked_root_refs", ["references", ".git", ".env"]),
        allowed_path_patterns=kwargs.pop("allowed_path_patterns", ["*.py", "*.md"]),
        blocked_path_patterns=kwargs.pop("blocked_path_patterns", ["*.pem", "*.key", ".env", "*secret*", "*token*", "*credential*"]),
        allowed_target_kinds=kwargs.pop("allowed_target_kinds", [PatchTargetKind.SOURCE_FILE, PatchTargetKind.TEST_FILE, PatchTargetKind.DOCUMENTATION_FILE, PatchTargetKind.VERSION_DOCUMENT, PatchTargetKind.REFERENCE_DIGEST_DOCUMENT]),
        blocked_target_kinds=kwargs.pop("blocked_target_kinds", [PatchTargetKind.SECRET_LIKE_FILE, PatchTargetKind.CREDENTIAL_LIKE_FILE, PatchTargetKind.BINARY_FILE, PatchTargetKind.EXTERNAL_PATH]),
        **kwargs,
    )


def default_patch_scope_policy() -> PatchScopePolicy:
    return build_patch_scope_policy()


def build_patch_target_selector(selector_id: str = "selector:v0.35.1:doc", **kwargs: Any) -> PatchTargetSelector:
    return PatchTargetSelector(
        selector_id=selector_id,
        scope_policy_id=kwargs.pop("scope_policy_id", "scope_policy:v0.35.1"),
        target_kind=kwargs.pop("target_kind", PatchTargetKind.VERSION_DOCUMENT),
        target_path_ref=kwargs.pop("target_path_ref", DEFAULT_V0351_DOC_PATH),
        target_summary=kwargs.pop("target_summary", "Future read-only context target metadata for the v0.35.1 document."),
        selected_for_future_context=kwargs.pop("selected_for_future_context", True),
        risk_kinds=kwargs.pop("risk_kinds", []),
        **kwargs,
    )


def build_patch_allowed_target(allowed_target_id: str = "allowed_target:v0.35.1:doc", **kwargs: Any) -> PatchAllowedTarget:
    return PatchAllowedTarget(
        allowed_target_id=allowed_target_id,
        selector_id=kwargs.pop("selector_id", "selector:v0.35.1:doc"),
        target_kind=kwargs.pop("target_kind", PatchTargetKind.VERSION_DOCUMENT),
        target_path_ref=kwargs.pop("target_path_ref", DEFAULT_V0351_DOC_PATH),
        allow_future_readonly_context=kwargs.pop("allow_future_readonly_context", True),
        **kwargs,
    )


def build_patch_blocked_target(blocked_target_id: str = "blocked_target:v0.35.1:secret", **kwargs: Any) -> PatchBlockedTarget:
    return PatchBlockedTarget(
        blocked_target_id=blocked_target_id,
        selector_id=kwargs.pop("selector_id", None),
        target_kind=kwargs.pop("target_kind", PatchTargetKind.SECRET_LIKE_FILE),
        target_path_ref=kwargs.pop("target_path_ref", ".env"),
        risk_kinds=kwargs.pop("risk_kinds", [PatchScopeRiskKind.SECRET_PATH_RISK]),
        reason=kwargs.pop("reason", "Secret-like targets are prohibited from v0.35.1 scope metadata."),
        safe_alternative=kwargs.pop("safe_alternative", "Use non-secret source/test/doc metadata refs only."),
        **kwargs,
    )


def build_patch_non_goal(non_goal_id: str = "non_goal:v0.35.1:apply", **kwargs: Any) -> PatchNonGoal:
    return PatchNonGoal(
        non_goal_id=non_goal_id,
        title=kwargs.pop("title", "No patch application"),
        description=kwargs.pop("description", "v0.35.1 does not apply patches or write files."),
        blocked_capability=kwargs.pop("blocked_capability", PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY),
        reason=kwargs.pop("reason", "Patch application belongs to a later human-approved sandbox track."),
        **kwargs,
    )


def default_patch_non_goal_register() -> PatchNonGoalRegister:
    non_goals = [
        build_patch_non_goal("non_goal:v0.35.1:apply", blocked_capability=PatchProposalCapabilityKind.EXECUTE_PATCH_APPLY, title="No patch application"),
        build_patch_non_goal("non_goal:v0.35.1:write", blocked_capability=PatchProposalCapabilityKind.WRITE_WORKSPACE_FILE, title="No workspace write"),
        build_patch_non_goal("non_goal:v0.35.1:edit", blocked_capability=PatchProposalCapabilityKind.EDIT_CODE_FILE, title="No code edit"),
        build_patch_non_goal("non_goal:v0.35.1:shell", blocked_capability=PatchProposalCapabilityKind.EXECUTE_SHELL, title="No shell execution"),
        build_patch_non_goal("non_goal:v0.35.1:test", blocked_capability=PatchProposalCapabilityKind.RUN_TESTS, title="No test execution"),
        build_patch_non_goal("non_goal:v0.35.1:install", blocked_capability=PatchProposalCapabilityKind.INSTALL_DEPENDENCY, title="No dependency install"),
        build_patch_non_goal("non_goal:v0.35.1:reference", blocked_capability=PatchProposalCapabilityKind.EXECUTE_REFERENCE_HARNESS, title="No reference execution"),
        build_patch_non_goal("non_goal:v0.35.1:apply_patch", blocked_capability=PatchProposalCapabilityKind.RUN_APPLY_PATCH, title="No apply_patch runtime call"),
        build_patch_non_goal("non_goal:v0.35.1:git_apply", blocked_capability=PatchProposalCapabilityKind.RUN_GIT_APPLY, title="No git apply runtime call"),
    ]
    return build_patch_non_goal_register(non_goals=non_goals)


def build_patch_non_goal_register(register_id: str = "non_goal_register:v0.35.1", **kwargs: Any) -> PatchNonGoalRegister:
    return PatchNonGoalRegister(
        register_id=register_id,
        version=kwargs.pop("version", V0351_VERSION),
        non_goals=kwargs.pop("non_goals", [build_patch_non_goal()]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", list(DEFAULT_NON_GOAL_CAPABILITIES)),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [PatchProposalSurfaceKind.PATCH_APPLY, PatchProposalSurfaceKind.FILE_WRITE, PatchProposalSurfaceKind.CODE_EDIT, PatchProposalSurfaceKind.SHELL_COMMAND, PatchProposalSurfaceKind.TEST_EXECUTION, PatchProposalSurfaceKind.DEPENDENCY_INSTALL, PatchProposalSurfaceKind.REFERENCE_CODE_EXECUTION]),
        summary=kwargs.pop("summary", "Non-goal register blocks apply/write/edit/shell/test/install/reference execution."),
        **kwargs,
    )


def build_patch_intent_validation_finding(finding_id: str = "intent_finding:v0.35.1:ok", **kwargs: Any) -> PatchIntentValidationFinding:
    return PatchIntentValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchIntentDecisionKind.ALLOW_INTENT_METADATA),
        risk_kinds=kwargs.pop("risk_kinds", []),
        message=kwargs.pop("message", "Intent metadata is bounded and does not request patch proposal generation."),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_intent_validation_report(report_id: str = "intent_validation:v0.35.1", **kwargs: Any) -> PatchIntentValidationReport:
    findings = kwargs.pop("findings", [build_patch_intent_validation_finding()])
    return PatchIntentValidationReport(
        report_id=report_id,
        version=kwargs.pop("version", V0351_VERSION),
        intent_id=kwargs.pop("intent_id", "intent:v0.35.1"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Intent validation is metadata-only and does not certify execution."),
        **kwargs,
    )


def build_patch_scope_validation_finding(finding_id: str = "scope_finding:v0.35.1:ok", **kwargs: Any) -> PatchScopeValidationFinding:
    return PatchScopeValidationFinding(
        finding_id=finding_id,
        decision_kind=kwargs.pop("decision_kind", PatchScopeDecisionKind.ALLOW_SCOPE_METADATA),
        risk_kinds=kwargs.pop("risk_kinds", []),
        message=kwargs.pop("message", "Scope metadata blocks write/apply and unsafe target kinds."),
        blocks_validation=kwargs.pop("blocks_validation", False),
        **kwargs,
    )


def build_patch_scope_validation_report(report_id: str = "scope_validation:v0.35.1", **kwargs: Any) -> PatchScopeValidationReport:
    findings = kwargs.pop("findings", [build_patch_scope_validation_finding()])
    return PatchScopeValidationReport(
        report_id=report_id,
        version=kwargs.pop("version", V0351_VERSION),
        scope_policy_id=kwargs.pop("scope_policy_id", "scope_policy:v0.35.1"),
        findings=findings,
        valid=kwargs.pop("valid", not any(item.blocks_validation for item in findings)),
        summary=kwargs.pop("summary", "Scope validation is not file access or write permission."),
        **kwargs,
    )


def build_patch_intent_scope_bundle(bundle_id: str = "bundle:v0.35.1", **kwargs: Any) -> PatchIntentScopeBundle:
    intent = kwargs.pop("intent", build_patch_intent_envelope())
    policy = kwargs.pop("scope_policy", build_patch_scope_policy())
    return PatchIntentScopeBundle(
        bundle_id=bundle_id,
        version=kwargs.pop("version", V0351_VERSION),
        intent=intent,
        scope_policy=policy,
        target_selectors=kwargs.pop("target_selectors", [build_patch_target_selector(scope_policy_id=policy.scope_policy_id)]),
        allowed_targets=kwargs.pop("allowed_targets", [build_patch_allowed_target()]),
        blocked_targets=kwargs.pop("blocked_targets", [build_patch_blocked_target()]),
        non_goal_register=kwargs.pop("non_goal_register", default_patch_non_goal_register()),
        reference_pattern_uses=kwargs.pop("reference_pattern_uses", list(intent.reference_pattern_uses)),
        intent_validation_report=kwargs.pop("intent_validation_report", build_patch_intent_validation_report(intent_id=intent.intent_id)),
        scope_validation_report=kwargs.pop("scope_validation_report", build_patch_scope_validation_report(scope_policy_id=policy.scope_policy_id)),
        status=kwargs.pop("status", PatchIntentStatus.SCOPE_ATTACHED),
        readiness_level=kwargs.pop("readiness_level", PatchIntentReadinessLevel.INTENT_SCOPE_BUNDLE_READY),
        summary=kwargs.pop("summary", "Patch intent/scope bundle is metadata only, not a patch plan or proposal."),
        **kwargs,
    )


def build_patch_intent_scope_report(report_id: str = "intent_scope_report:v0.35.1", **kwargs: Any) -> PatchIntentScopeReport:
    bundle = kwargs.pop("bundle", build_patch_intent_scope_bundle())
    return PatchIntentScopeReport(
        report_id=report_id,
        version=kwargs.pop("version", V0351_VERSION),
        bundle_id=kwargs.pop("bundle_id", bundle.bundle_id),
        status=kwargs.pop("status", bundle.status),
        readiness_level=kwargs.pop("readiness_level", bundle.readiness_level),
        summary=kwargs.pop("summary", "Patch intent/scope report summarizes metadata validation only."),
        intent_valid=kwargs.pop("intent_valid", bundle.intent_validation_report.valid),
        scope_valid=kwargs.pop("scope_valid", bundle.scope_validation_report.valid),
        selector_count=kwargs.pop("selector_count", len(bundle.target_selectors)),
        blocked_target_count=kwargs.pop("blocked_target_count", len(bundle.blocked_targets)),
        non_goal_count=kwargs.pop("non_goal_count", len(bundle.non_goal_register.non_goals)),
        **kwargs,
    )


def build_patch_intent_scope_run_preview(run_preview_id: str = "run_preview:v0.35.1", **kwargs: Any) -> PatchIntentScopeRunPreview:
    return PatchIntentScopeRunPreview(
        run_preview_id=run_preview_id,
        planned_steps=kwargs.pop("planned_steps", ["Create intent metadata", "Attach scope policy", "Validate non-goals"]),
        expected_artifacts=kwargs.pop("expected_artifacts", ["PatchIntentEnvelope", "PatchScopePolicy", "PatchIntentScopeBundle"]),
        explicitly_not_performed=kwargs.pop("explicitly_not_performed", ["patch context collection", "patch planning", "diff proposal", "patch application", "workspace write"]),
        **kwargs,
    )


def build_patch_intent_scope_no_apply_guarantee(guarantee_id: str = "no_apply:v0.35.1", **kwargs: Any) -> PatchIntentScopeNoApplyGuarantee:
    return PatchIntentScopeNoApplyGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0351_VERSION), **kwargs)


def build_v0351_readiness_report(report_id: str = "readiness:v0.35.1", **kwargs: Any) -> V0351ReadinessReport:
    return V0351ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0351_VERSION),
        bundle_id=kwargs.pop("bundle_id", "bundle:v0.35.1"),
        summary=kwargs.pop("summary", "v0.35.1 is ready for v0.35.2/v0.35.3 design-stage handoff only."),
        completed_items=kwargs.pop("completed_items", ["Patch intent envelope", "Scope policy", "Target selector", "Non-goal register", "Validation reports"]),
        blocked_items=kwargs.pop("blocked_items", ["patch context collection", "patch planning", "diff proposal", "patch proposal generation", "patch application", "workspace write"]),
        future_track_items=kwargs.pop("future_track_items", ["v0.35.2 read-only context collector", "v0.35.3 reference-informed patch plan"]),
        evidence_refs=kwargs.pop("evidence_refs", [DEFAULT_V0351_DOC_PATH, DEFAULT_V0350_DIGEST_REF]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", list(DEFAULT_WITHDRAWAL_CONDITIONS)),
        **kwargs,
    )


def _intent_kind_for_pattern(pattern: Any) -> PatchIntentKind:
    pattern_kind = str(getattr(pattern, "pattern_kind", "")).lower()
    disposition = str(getattr(pattern, "disposition", "")).lower()
    if "permission" in pattern_kind or "safety" in pattern_kind:
        return PatchIntentKind.TIGHTEN_SAFETY_BOUNDARY
    if "review" in pattern_kind:
        return PatchIntentKind.ADD_MISSING_CONTRACT_MODEL
    if "diff" in pattern_kind or "file_edit" in pattern_kind:
        return PatchIntentKind.PREPARE_FUTURE_TRACK
    if "future" in pattern_kind or "future" in disposition:
        return PatchIntentKind.PREPARE_FUTURE_TRACK
    return PatchIntentKind.ALIGN_WITH_REFERENCE_PATTERN


def build_patch_reference_pattern_uses_from_digest_metadata(digest: Any) -> list[PatchReferencePatternUse]:
    patterns = list(getattr(digest, "patterns", []) or [])
    digest_id = getattr(digest, "digest_id", None)
    uses: list[PatchReferencePatternUse] = []
    for index, pattern in enumerate(patterns):
        disposition = ReferencePatternDisposition(getattr(pattern, "disposition", ReferencePatternDisposition.UNKNOWN))
        rejected = disposition == ReferencePatternDisposition.REJECTED_FOR_SAFETY
        future = disposition == ReferencePatternDisposition.FUTURE_TRACK
        reference_name = str(getattr(pattern, "corpus_kind", "reference"))
        observed_summary = str(getattr(pattern, "pattern_summary", "Reference pattern metadata."))
        rejection_reason = getattr(pattern, "rejection_reason", None)
        future_note = getattr(pattern, "future_track_note", None)
        uses.append(
            build_patch_reference_pattern_use(
                pattern_use_id=f"pattern_use:v0.35.1:{index}",
                source_pattern_id=getattr(pattern, "pattern_id", None),
                source_digest_id=digest_id,
                reference_name=reference_name,
                observed_pattern_summary=observed_summary,
                adapted_intent_kind=_intent_kind_for_pattern(pattern),
                adapted_scope_note=future_note or "Use as bounded scope metadata only; do not execute or copy reference code.",
                rejected=rejected,
                rejection_reason=rejection_reason if rejected else None,
                future_track=future,
                confidence=str(getattr(pattern, "confidence", "unknown")),
            )
        )
    return uses


def validate_patch_intent_envelope(intent: PatchIntentEnvelope) -> PatchIntentValidationReport:
    findings: list[PatchIntentValidationFinding] = []
    if PatchIntentKind(intent.intent_kind) == PatchIntentKind.UNKNOWN:
        findings.append(
            build_patch_intent_validation_finding(
                "intent_finding:unknown",
                decision_kind=PatchIntentDecisionKind.REQUIRE_REVIEW,
                risk_kinds=[PatchIntentRiskKind.VAGUE_INTENT_RISK],
                message="Unknown intent kind requires review.",
                blocks_validation=True,
            )
        )
    if intent.ready_for_patch_proposal or intent.ready_for_execution:
        findings.append(
            build_patch_intent_validation_finding(
                "intent_finding:unsafe_ready",
                decision_kind=PatchIntentDecisionKind.BLOCK,
                risk_kinds=[PatchIntentRiskKind.PATCH_APPLY_RISK],
                message="Intent cannot be ready for proposal or execution in v0.35.1.",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_patch_intent_validation_finding())
    return build_patch_intent_validation_report(intent_id=intent.intent_id, findings=findings)


def validate_patch_scope_policy(policy: PatchScopePolicy) -> PatchScopeValidationReport:
    findings: list[PatchScopeValidationFinding] = []
    if not patch_scope_policy_blocks_write_apply(policy):
        findings.append(
            build_patch_scope_validation_finding(
                "scope_finding:unsafe_policy",
                decision_kind=PatchScopeDecisionKind.BLOCK_SCOPE,
                risk_kinds=[PatchScopeRiskKind.SCOPE_ESCAPE_RISK],
                message="Scope policy must block write/apply and unsafe target kinds.",
                blocks_validation=True,
            )
        )
    if not findings:
        findings.append(build_patch_scope_validation_finding())
    return build_patch_scope_validation_report(scope_policy_id=policy.scope_policy_id, findings=findings)


def validate_patch_target_selector(selector: PatchTargetSelector) -> PatchScopeValidationReport:
    findings: list[PatchScopeValidationFinding] = []
    if not patch_target_selector_is_not_file_access(selector):
        findings.append(
            build_patch_scope_validation_finding(
                "scope_finding:selector_write",
                decision_kind=PatchScopeDecisionKind.BLOCK_TARGET,
                risk_kinds=[PatchScopeRiskKind.SCOPE_ESCAPE_RISK],
                message="Target selector cannot select for write or proposal generation in v0.35.1.",
                blocks_validation=True,
                target_ref=selector.target_path_ref,
            )
        )
    if not findings:
        findings.append(build_patch_scope_validation_finding(target_ref=selector.target_path_ref))
    return build_patch_scope_validation_report(scope_policy_id=selector.scope_policy_id, findings=findings)


def validate_patch_intent_scope_bundle(bundle: PatchIntentScopeBundle) -> PatchIntentScopeReport:
    return build_patch_intent_scope_report(bundle=bundle)


def patch_intent_flags_preserve_no_apply(flags: PatchIntentFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_PATCH_INTENT_FLAG_NAMES) and flags.production_certified is False


def patch_scope_policy_blocks_write_apply(policy: PatchScopePolicy) -> bool:
    unsafe_targets_blocked = all(
        getattr(policy, name) is False
        for name in ("allow_secret_targets", "allow_credential_targets", "allow_binary_targets", "allow_external_targets")
    )
    unsafe_runtime_blocked = policy.allow_workspace_write is False and policy.allow_code_edit is False and policy.allow_patch_application is False
    return unsafe_targets_blocked and unsafe_runtime_blocked


def patch_target_selector_is_not_file_access(selector: PatchTargetSelector) -> bool:
    return selector.selected_for_write is False and selector.selected_for_future_patch_proposal is False


def patch_intent_scope_bundle_is_not_patch_plan(bundle: PatchIntentScopeBundle) -> bool:
    return (
        bundle.ready_for_patch_context_collection is False
        and bundle.ready_for_patch_plan is False
        and bundle.ready_for_diff_proposal is False
        and bundle.ready_for_patch_proposal is False
        and bundle.ready_for_patch_application is False
        and bundle.ready_for_execution is False
    )


def v0351_readiness_report_is_not_execution_ready(report: V0351ReadinessReport) -> bool:
    unsafe_names = tuple(name for name in UNSAFE_PATCH_INTENT_FLAG_NAMES if hasattr(report, name))
    return all(getattr(report, name) is False for name in unsafe_names) and report.production_certified is False
