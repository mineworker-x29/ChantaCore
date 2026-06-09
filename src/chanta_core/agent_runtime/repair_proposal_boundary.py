from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import _require_non_blank, _validate_string_list


V0380_VERSION = "v0.38.0"
V0380_RELEASE_NAME = "v0.38.0 Bounded Repair Proposal Boundary Foundation"

UNSAFE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_execution",
    "ready_for_source_file_read",
    "ready_for_sandbox_source_read",
    "ready_for_repair_proposal_generation",
    "ready_for_proposed_diff_generation",
    "ready_for_proposed_code_hunk_generation",
    "ready_for_proposed_patch_envelope_generation",
    "ready_for_repair_patch_proposal",
    "ready_for_repair_diff_generation",
    "ready_for_code_hunk_generation",
    "ready_for_repair_execution",
    "ready_for_repair_apply",
    "ready_for_sandbox_repair_apply",
    "ready_for_live_workspace_write",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_apply_patch",
    "ready_for_git_apply",
    "ready_for_automatic_repair",
    "ready_for_repair_loop",
    "ready_for_retry_loop",
    "ready_for_multi_cycle_repair_loop",
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

UNSAFE_POLICY_ALLOW_NAMES = (
    "allow_source_file_read",
    "allow_sandbox_source_read",
    "allow_repair_proposal_generation",
    "allow_proposed_diff_generation",
    "allow_proposed_code_hunk_generation",
    "allow_proposed_patch_envelope_generation",
    "allow_repair_patch_proposal",
    "allow_repair_execution",
    "allow_repair_apply",
    "allow_sandbox_repair_apply",
    "allow_live_workspace_write",
    "allow_patch_application",
    "allow_apply_patch",
    "allow_git_apply",
    "allow_automatic_repair",
    "allow_retry_loop",
    "allow_multi_cycle_repair_loop",
    "allow_test_execution",
    "allow_subprocess",
    "allow_shell",
    "allow_dependency_install",
    "allow_network_access",
    "allow_model_provider_invocation",
    "allow_external_agent_execution",
    "allow_dominion_runtime",
)

UNSAFE_DECISION_ALLOW_NAMES = (
    "source_file_read_allowed",
    "sandbox_source_read_allowed",
    "repair_proposal_generation_allowed",
    "proposed_diff_generation_allowed",
    "proposed_code_hunk_generation_allowed",
    "proposed_patch_envelope_generation_allowed",
    "file_write_allowed",
    "patch_apply_allowed",
    "repair_execution_allowed",
    "test_execution_allowed",
    "subprocess_allowed",
    "shell_allowed",
    "dependency_install_allowed",
    "network_access_allowed",
    "model_provider_invocation_allowed",
    "external_agent_execution_allowed",
    "dominion_runtime_allowed",
)

UNSAFE_SUBPOLICY_ALLOW_NAMES = (
    "executable_in_v0380",
    "allows_file_read",
    "allows_file_write",
    "allows_diff_generation",
    "allows_hunk_generation",
    "allows_patch_generation",
    "allows_patch_apply",
    "allows_repair_execution",
)

UNSAFE_ALLOWED_SURFACE_NAMES = (
    "executable_in_v0380",
    "reads_source",
    "generates_diff",
    "generates_hunk",
    "generates_patch_envelope",
    "writes_file",
    "applies_patch",
    "executes_repair",
)


class RepairProposalTrackKind(StrEnum):
    BOUNDARY_FOUNDATION = "boundary_foundation"
    REPAIR_PROPOSAL_EVIDENCE_CONTRACT = "repair_proposal_evidence_contract"
    READ_ONLY_SANDBOX_SOURCE_CONTEXT = "read_only_sandbox_source_context"
    REPAIR_SCOPE_PLANNER_CHANGE_INTENT = "repair_scope_planner_change_intent"
    PROPOSED_DIFF_CODE_HUNK_METADATA = "proposed_diff_code_hunk_metadata"
    REPAIR_PROPOSAL_SAFETY_VALIDATION = "repair_proposal_safety_validation"
    HUMAN_REVIEW_PACKET = "human_review_packet"
    BOUNDED_REPAIR_PROPOSAL_LOOP_TRIAL = "bounded_repair_proposal_loop_trial"
    CLI_REPAIR_PROPOSAL_SURFACE = "cli_repair_proposal_surface"
    CONSOLIDATION = "consolidation"
    UNKNOWN = "unknown"


class RepairProposalSurfaceKind(StrEnum):
    REPAIR_PROPOSAL_BOUNDARY = "repair_proposal_boundary"
    REPAIR_EVIDENCE_CONTRACT = "repair_evidence_contract"
    READ_ONLY_SANDBOX_SOURCE_CONTEXT = "read_only_sandbox_source_context"
    REPAIR_SCOPE_PLAN = "repair_scope_plan"
    CHANGE_INTENT_MODEL = "change_intent_model"
    PROPOSED_DIFF_METADATA = "proposed_diff_metadata"
    PROPOSED_CODE_HUNK_METADATA = "proposed_code_hunk_metadata"
    PROPOSED_PATCH_ENVELOPE = "proposed_patch_envelope"
    REPAIR_PROPOSAL_SAFETY_VALIDATION = "repair_proposal_safety_validation"
    REPAIR_HUMAN_REVIEW_PACKET = "repair_human_review_packet"
    REPAIR_APPROVAL_REQUEST = "repair_approval_request"
    FUTURE_SANDBOX_REPAIR_APPLY_INPUT = "future_sandbox_repair_apply_input"
    LIVE_WORKSPACE_WRITE = "live_workspace_write"
    FILE_EDIT = "file_edit"
    PATCH_APPLICATION = "patch_application"
    APPLY_PATCH = "apply_patch"
    GIT_APPLY = "git_apply"
    AUTOMATIC_REPAIR = "automatic_repair"
    REPAIR_EXECUTION = "repair_execution"
    ARBITRARY_SHELL = "arbitrary_shell"
    MODEL_PROVIDER_INVOCATION = "model_provider_invocation"
    EXTERNAL_AGENT_EXECUTION = "external_agent_execution"
    DOMINION_RUNTIME = "dominion_runtime"
    UNKNOWN = "unknown"


class RepairProposalCapabilityKind(StrEnum):
    DEFINE_REPAIR_PROPOSAL_BOUNDARY = "define_repair_proposal_boundary"
    DEFINE_REPAIR_EVIDENCE_CONTRACT_BOUNDARY = "define_repair_evidence_contract_boundary"
    DEFINE_READ_ONLY_SOURCE_CONTEXT_BOUNDARY = "define_read_only_source_context_boundary"
    DEFINE_REPAIR_SCOPE_PLANNING_BOUNDARY = "define_repair_scope_planning_boundary"
    DEFINE_CHANGE_INTENT_BOUNDARY = "define_change_intent_boundary"
    DEFINE_PROPOSED_DIFF_METADATA_BOUNDARY = "define_proposed_diff_metadata_boundary"
    DEFINE_PROPOSED_CODE_HUNK_METADATA_BOUNDARY = "define_proposed_code_hunk_metadata_boundary"
    DEFINE_PROPOSED_PATCH_ENVELOPE_BOUNDARY = "define_proposed_patch_envelope_boundary"
    DEFINE_SAFETY_VALIDATION_BOUNDARY = "define_safety_validation_boundary"
    DEFINE_HUMAN_REVIEW_BOUNDARY = "define_human_review_boundary"
    DEFINE_DO_NOTHING_COMPARISON_BOUNDARY = "define_do_nothing_comparison_boundary"
    CREATE_REPAIR_PROPOSAL = "create_repair_proposal"
    READ_SANDBOX_SOURCE = "read_sandbox_source"
    GENERATE_PROPOSED_DIFF = "generate_proposed_diff"
    GENERATE_CODE_HUNK = "generate_code_hunk"
    GENERATE_PATCH_ENVELOPE = "generate_patch_envelope"
    EDIT_FILE = "edit_file"
    APPLY_PATCH_RUNTIME = "apply_patch_runtime"
    GIT_APPLY_RUNTIME = "git_apply_runtime"
    EXECUTE_REPAIR = "execute_repair"
    RUN_TESTS = "run_tests"
    CALL_MODEL_PROVIDER = "call_model_provider"
    INVOKE_EXTERNAL_AGENT = "invoke_external_agent"
    RUN_DOMINION_RUNTIME = "run_dominion_runtime"
    UNKNOWN = "unknown"


class RepairProposalRiskKind(StrEnum):
    REPAIR_EXECUTION_CONFUSION_RISK = "repair_execution_confusion_risk"
    PATCH_PROPOSAL_CONFUSION_RISK = "patch_proposal_confusion_risk"
    DIFF_GENERATION_CONFUSION_RISK = "diff_generation_confusion_risk"
    CODE_HUNK_GENERATION_CONFUSION_RISK = "code_hunk_generation_confusion_risk"
    FILE_EDIT_RISK = "file_edit_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    LIVE_WORKSPACE_WRITE_RISK = "live_workspace_write_risk"
    APPLY_PATCH_RISK = "apply_patch_risk"
    GIT_APPLY_RISK = "git_apply_risk"
    AUTOMATIC_REPAIR_RISK = "automatic_repair_risk"
    RETRY_LOOP_RISK = "retry_loop_risk"
    MULTI_CYCLE_LOOP_RISK = "multi_cycle_loop_risk"
    SOURCE_READ_SCOPE_RISK = "source_read_scope_risk"
    INSUFFICIENT_EVIDENCE_RISK = "insufficient_evidence_risk"
    DO_NOTHING_OMISSION_RISK = "do_nothing_omission_risk"
    HUMAN_REVIEW_OMISSION_RISK = "human_review_omission_risk"
    MODEL_PROVIDER_INVOCATION_RISK = "model_provider_invocation_risk"
    EXTERNAL_AGENT_EXECUTION_RISK = "external_agent_execution_risk"
    DOMINION_RUNTIME_RISK = "dominion_runtime_risk"
    PRODUCTION_CERTIFICATION_CONFUSION_RISK = "production_certification_confusion_risk"
    UNKNOWN = "unknown"


class RepairProposalDecisionKind(StrEnum):
    ALLOW_BOUNDARY_DEFINITION = "allow_boundary_definition"
    ALLOW_EVIDENCE_CONTRACT_BOUNDARY_DEFINITION = "allow_evidence_contract_boundary_definition"
    ALLOW_READ_ONLY_SOURCE_CONTEXT_BOUNDARY_DEFINITION = "allow_read_only_source_context_boundary_definition"
    ALLOW_SCOPE_PLANNING_BOUNDARY_DEFINITION = "allow_scope_planning_boundary_definition"
    ALLOW_CHANGE_INTENT_BOUNDARY_DEFINITION = "allow_change_intent_boundary_definition"
    ALLOW_PROPOSED_DIFF_METADATA_BOUNDARY_DEFINITION = "allow_proposed_diff_metadata_boundary_definition"
    ALLOW_PROPOSED_CODE_HUNK_METADATA_BOUNDARY_DEFINITION = "allow_proposed_code_hunk_metadata_boundary_definition"
    ALLOW_SAFETY_VALIDATION_BOUNDARY_DEFINITION = "allow_safety_validation_boundary_definition"
    ALLOW_HUMAN_REVIEW_BOUNDARY_DEFINITION = "allow_human_review_boundary_definition"
    ALLOW_DO_NOTHING_BOUNDARY_DEFINITION = "allow_do_nothing_boundary_definition"
    ALLOW_DESIGN_STAGE_HANDOFF = "allow_design_stage_handoff"
    DENY = "deny"
    BLOCK = "block"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RepairProposalStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    BOUNDARY_READY = "boundary_ready"
    BOUNDARY_READY_WITH_GAPS = "boundary_ready_with_gaps"
    EVIDENCE_BOUNDARY_READY = "evidence_boundary_ready"
    SOURCE_CONTEXT_BOUNDARY_READY = "source_context_boundary_ready"
    SCOPE_BOUNDARY_READY = "scope_boundary_ready"
    PATCH_METADATA_BOUNDARY_READY = "patch_metadata_boundary_ready"
    REVIEW_BOUNDARY_READY = "review_boundary_ready"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class RepairProposalReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    BOUNDARY_CONTRACT_READY = "boundary_contract_ready"
    BOUNDED_REPAIR_PROPOSAL_BOUNDARY_READY = "bounded_repair_proposal_boundary_ready"
    EVIDENCE_CONTRACT_BOUNDARY_READY = "evidence_contract_boundary_ready"
    SOURCE_CONTEXT_BOUNDARY_READY = "source_context_boundary_ready"
    SCOPE_PLANNING_BOUNDARY_READY = "scope_planning_boundary_ready"
    PATCH_METADATA_BOUNDARY_READY = "patch_metadata_boundary_ready"
    HUMAN_REVIEW_BOUNDARY_READY = "human_review_boundary_ready"
    DESIGN_HANDOFF_READY_FOR_V0381 = "design_handoff_ready_for_v0381"
    DESIGN_HANDOFF_READY_FOR_V0382 = "design_handoff_ready_for_v0382"
    DESIGN_HANDOFF_READY_FOR_V0384 = "design_handoff_ready_for_v0384"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class RepairProposalPosture(StrEnum):
    BOUNDARY_ONLY = "boundary_only"
    PROPOSAL_GENERATION_FUTURE_GATED = "proposal_generation_future_gated"
    PROPOSAL_GENERATION_BLOCKED_IN_V0380 = "proposal_generation_blocked_in_v0380"
    REPAIR_EXECUTION_BLOCKED = "repair_execution_blocked"
    APPLY_BLOCKED = "apply_blocked"
    UNKNOWN = "unknown"


class ProposedDiffPosture(StrEnum):
    NO_DIFF_GENERATION = "no_diff_generation"
    DIFF_METADATA_FUTURE_GATED = "diff_metadata_future_gated"
    DIFF_TEXT_GENERATION_BLOCKED = "diff_text_generation_blocked"
    APPLIED_DIFF_BLOCKED = "applied_diff_blocked"
    UNKNOWN = "unknown"


class ProposedCodeHunkPosture(StrEnum):
    NO_HUNK_GENERATION = "no_hunk_generation"
    HUNK_METADATA_FUTURE_GATED = "hunk_metadata_future_gated"
    CODE_HUNK_GENERATION_BLOCKED = "code_hunk_generation_blocked"
    APPLIED_HUNK_BLOCKED = "applied_hunk_blocked"
    UNKNOWN = "unknown"


class ProposedPatchEnvelopePosture(StrEnum):
    NO_PATCH_ENVELOPE_GENERATION = "no_patch_envelope_generation"
    PATCH_ENVELOPE_FUTURE_GATED = "patch_envelope_future_gated"
    PATCH_APPLICATION_BLOCKED = "patch_application_blocked"
    UNKNOWN = "unknown"


class RepairSourceContextPosture(StrEnum):
    NO_SOURCE_READ = "no_source_read"
    READ_ONLY_SANDBOX_SOURCE_CONTEXT_FUTURE_GATED = "read_only_sandbox_source_context_future_gated"
    LIVE_SOURCE_READ_BLOCKED = "live_source_read_blocked"
    REFERENCE_SOURCE_EXECUTION_BLOCKED = "reference_source_execution_blocked"
    UNKNOWN = "unknown"


class RepairHumanReviewPosture(StrEnum):
    HUMAN_REVIEW_REQUIRED_BOUNDARY = "human_review_required_boundary"
    APPROVAL_REQUEST_FUTURE_GATED = "approval_request_future_gated"
    HUMAN_APPROVAL_NOT_PRESENT = "human_approval_not_present"
    APPLY_WITHOUT_REVIEW_BLOCKED = "apply_without_review_blocked"
    UNKNOWN = "unknown"


class RepairDoNothingPosture(StrEnum):
    DO_NOTHING_BOUNDARY_DEFINED = "do_nothing_boundary_defined"
    DO_NOTHING_COMPARISON_REQUIRED = "do_nothing_comparison_required"
    DO_NOTHING_COMPARISON_FUTURE_GATED = "do_nothing_comparison_future_gated"
    DO_NOTHING_OMISSION_BLOCKED = "do_nothing_omission_blocked"
    UNKNOWN = "unknown"


class RepairProposalSourceKind(StrEnum):
    V0379_TEST_RUNNER_CONSOLIDATION = "v0379_test_runner_consolidation"
    V0377_COLD_AGENT_EVALUATION_REPORT = "v0377_cold_agent_evaluation_report"
    V0376_VERA_CODEX_TRIAL_PACKET = "v0376_vera_codex_trial_packet"
    V0375_REPAIR_SUGGESTION_ENVELOPE = "v0375_repair_suggestion_envelope"
    V0374_TEST_FEEDBACK_REPORT = "v0374_test_feedback_report"
    V0373_TEST_RESULT_ENVELOPE = "v0373_test_result_envelope"
    V0369_PATCH_APPLY_SANDBOX_CONSOLIDATION = "v0369_patch_apply_sandbox_consolidation"
    MANUAL_DESIGN_NOTE = "manual_design_note"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


def _validate_list(name: str, value: list[Any]) -> None:
    if not isinstance(value, list):
        raise TypeError(f"{name} must be list")


def _validate_dict(name: str, value: dict[str, Any]) -> None:
    if not isinstance(value, dict):
        raise TypeError(f"{name} must be dict")


def _validate_version(version: str) -> None:
    _require_non_blank("version", version)
    if V0380_VERSION not in version:
        raise ValueError("version must include v0.38.0")


def _validate_false(instance: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if hasattr(instance, name) and getattr(instance, name) is not False:
            raise ValueError(f"{name} must always be False in v0.38.0")


def _validate_enum_list(name: str, value: list[Any], enum_cls: type[StrEnum]) -> None:
    _validate_list(name, value)
    for item in value:
        enum_cls(item)


def _validate_metadata(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    for key in metadata:
        lowered = str(key).lower()
        if any(token in lowered for token in ("secret_value", "credential_value", "api_key_value", "token_value")):
            raise ValueError("metadata keys must not carry credential or secret values")


@dataclass(frozen=True, kw_only=True)
class RepairProposalFlagSet:
    flag_set_id: str
    version: str
    repair_proposal_boundary_constructed: bool
    repair_proposal_policy_defined: bool
    repair_evidence_contract_boundary_defined: bool
    read_only_source_context_boundary_defined: bool
    repair_scope_planning_boundary_defined: bool
    change_intent_boundary_defined: bool
    proposed_diff_metadata_boundary_defined: bool
    proposed_code_hunk_metadata_boundary_defined: bool
    proposed_patch_envelope_boundary_defined: bool
    repair_safety_validation_boundary_defined: bool
    repair_human_review_boundary_defined: bool
    do_nothing_repair_comparison_boundary_defined: bool
    repair_proposal_risk_register_defined: bool
    ready_for_v0381_repair_proposal_evidence_contract: bool
    ready_for_v0382_read_only_sandbox_source_context: bool
    ready_for_v0383_repair_scope_planner_change_intent: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_v0385_repair_proposal_safety_validation: bool
    ready_for_v0386_human_review_packet: bool
    ready_for_v0387_bounded_repair_proposal_loop_trial: bool
    ready_for_v0388_cli_repair_proposal_surface: bool
    ready_for_bounded_repair_proposal_boundary: bool
    ready_for_repair_proposal_policy_boundary: bool
    ready_for_repair_evidence_contract_boundary: bool
    ready_for_read_only_sandbox_source_context_boundary: bool
    ready_for_repair_scope_planning_boundary: bool
    ready_for_change_intent_boundary: bool
    ready_for_proposed_diff_metadata_boundary: bool
    ready_for_proposed_code_hunk_metadata_boundary: bool
    ready_for_proposed_patch_envelope_boundary: bool
    ready_for_repair_safety_validation_boundary: bool
    ready_for_repair_human_review_boundary: bool
    ready_for_do_nothing_repair_comparison_boundary: bool
    ready_for_future_sandbox_repair_apply_input_boundary: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_proposed_code_hunk_generation: bool
    ready_for_proposed_patch_envelope_generation: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_diff_generation: bool
    ready_for_code_hunk_generation: bool
    ready_for_repair_execution: bool
    ready_for_repair_apply: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_live_workspace_write: bool
    ready_for_patch_application: bool
    ready_for_workspace_write: bool
    ready_for_code_edit: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_automatic_repair: bool
    ready_for_repair_loop: bool
    ready_for_retry_loop: bool
    ready_for_multi_cycle_repair_loop: bool
    ready_for_test_execution: bool
    ready_for_controlled_test_subprocess: bool
    ready_for_shell_execution: bool
    ready_for_subprocess_execution: bool
    ready_for_command_execution: bool
    ready_for_dependency_install: bool
    ready_for_network_access: bool
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
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version(self.version)
        _validate_false(self, UNSAFE_FLAG_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalSourceRef:
    source_ref_id: str
    source_kind: RepairProposalSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("source_ref_id", "source_id", "source_summary"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSourceKind(self.source_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalBoundaryPolicy:
    policy_id: str
    version: str
    repair_posture: RepairProposalPosture | str
    diff_posture: ProposedDiffPosture | str
    hunk_posture: ProposedCodeHunkPosture | str
    patch_envelope_posture: ProposedPatchEnvelopePosture | str
    source_context_posture: RepairSourceContextPosture | str
    human_review_posture: RepairHumanReviewPosture | str
    do_nothing_posture: RepairDoNothingPosture | str
    allowed_surfaces: list[RepairProposalSurfaceKind | str]
    prohibited_surfaces: list[RepairProposalSurfaceKind | str]
    prohibited_capabilities: list[RepairProposalCapabilityKind | str]
    prohibited_runtime_actions: list[str]
    allow_boundary_definition: bool
    allow_evidence_contract_future_gate: bool
    allow_read_only_source_context_future_gate: bool
    allow_scope_planning_future_gate: bool
    allow_change_intent_future_gate: bool
    allow_proposed_diff_metadata_future_gate: bool
    allow_proposed_code_hunk_metadata_future_gate: bool
    allow_proposed_patch_envelope_future_gate: bool
    allow_safety_validation_future_gate: bool
    allow_human_review_future_gate: bool
    allow_do_nothing_comparison_future_gate: bool
    allow_future_sandbox_repair_apply_input_boundary: bool
    allow_source_file_read: bool
    allow_sandbox_source_read: bool
    allow_repair_proposal_generation: bool
    allow_proposed_diff_generation: bool
    allow_proposed_code_hunk_generation: bool
    allow_proposed_patch_envelope_generation: bool
    allow_repair_patch_proposal: bool
    allow_repair_execution: bool
    allow_repair_apply: bool
    allow_sandbox_repair_apply: bool
    allow_live_workspace_write: bool
    allow_patch_application: bool
    allow_apply_patch: bool
    allow_git_apply: bool
    allow_automatic_repair: bool
    allow_retry_loop: bool
    allow_multi_cycle_repair_loop: bool
    allow_test_execution: bool
    allow_subprocess: bool
    allow_shell: bool
    allow_dependency_install: bool
    allow_network_access: bool
    allow_model_provider_invocation: bool
    allow_external_agent_execution: bool
    allow_dominion_runtime: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("policy_id", self.policy_id)
        _validate_version(self.version)
        RepairProposalPosture(self.repair_posture)
        ProposedDiffPosture(self.diff_posture)
        ProposedCodeHunkPosture(self.hunk_posture)
        ProposedPatchEnvelopePosture(self.patch_envelope_posture)
        RepairSourceContextPosture(self.source_context_posture)
        RepairHumanReviewPosture(self.human_review_posture)
        RepairDoNothingPosture(self.do_nothing_posture)
        _validate_enum_list("allowed_surfaces", self.allowed_surfaces, RepairProposalSurfaceKind)
        _validate_enum_list("prohibited_surfaces", self.prohibited_surfaces, RepairProposalSurfaceKind)
        _validate_enum_list("prohibited_capabilities", self.prohibited_capabilities, RepairProposalCapabilityKind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_false(self, UNSAFE_POLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairBoundarySubPolicy:
    policy_id: str
    version: str
    summary: str
    future_gated: bool
    executable_in_v0380: bool
    allows_file_read: bool
    allows_file_write: bool
    allows_diff_generation: bool
    allows_hunk_generation: bool
    allows_patch_generation: bool
    allows_patch_apply: bool
    allows_repair_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("policy_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_false(self, UNSAFE_SUBPOLICY_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairEvidenceBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairSourceContextBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairScopePlanningBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairPatchMetadataBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairSafetyValidationBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairHumanReviewBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairFutureApplyBoundaryPolicy(RepairBoundarySubPolicy):
    pass


@dataclass(frozen=True, kw_only=True)
class RepairProposalAllowedSurface:
    allowed_surface_id: str
    surface_kind: RepairProposalSurfaceKind | str
    capability_kind: RepairProposalCapabilityKind | str
    description: str
    allowed_only_for_design_stage: bool
    executable_in_v0380: bool
    reads_source: bool
    generates_diff: bool
    generates_hunk: bool
    generates_patch_envelope: bool
    writes_file: bool
    applies_patch: bool
    executes_repair: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("allowed_surface_id", "description"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSurfaceKind(self.surface_kind)
        RepairProposalCapabilityKind(self.capability_kind)
        _validate_false(self, UNSAFE_ALLOWED_SURFACE_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalProhibitedSurface:
    prohibited_surface_id: str
    surface_kind: RepairProposalSurfaceKind | str
    risk_kind: RepairProposalRiskKind | str
    capability_kind: RepairProposalCapabilityKind | str
    reason: str
    prohibited_runtime_actions: list[str]
    blocks_proposal_generation: bool
    blocks_repair_execution: bool
    blocks_runtime_readiness: bool
    evidence_refs: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("prohibited_surface_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSurfaceKind(self.surface_kind)
        RepairProposalRiskKind(self.risk_kind)
        RepairProposalCapabilityKind(self.capability_kind)
        _validate_string_list("prohibited_runtime_actions", self.prohibited_runtime_actions)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if not self.blocks_proposal_generation or not self.blocks_repair_execution or not self.blocks_runtime_readiness:
            raise ValueError("unsafe prohibited surfaces must block proposal generation, repair execution, and runtime readiness")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalBoundary:
    boundary_id: str
    version: str
    release_name: str
    boundary_policy: RepairProposalBoundaryPolicy
    evidence_policy: RepairEvidenceBoundaryPolicy
    source_context_policy: RepairSourceContextBoundaryPolicy
    scope_policy: RepairScopePlanningBoundaryPolicy
    patch_metadata_policy: RepairPatchMetadataBoundaryPolicy
    safety_policy: RepairSafetyValidationBoundaryPolicy
    human_review_policy: RepairHumanReviewBoundaryPolicy
    future_apply_policy: RepairFutureApplyBoundaryPolicy
    allowed_surfaces: list[RepairProposalAllowedSurface]
    prohibited_surfaces: list[RepairProposalProhibitedSurface]
    flags: RepairProposalFlagSet
    status: RepairProposalStatus | str
    readiness_level: RepairProposalReadinessLevel | str
    summary: str
    gaps: list[str]
    blocked_reasons: list[str]
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    ready_for_v0381_repair_proposal_evidence_contract: bool
    ready_for_v0382_read_only_sandbox_source_context: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_bounded_repair_proposal_boundary: bool
    ready_for_repair_human_review_boundary: bool
    ready_for_do_nothing_repair_comparison_boundary: bool
    ready_for_execution: bool
    ready_for_source_file_read: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_repair_execution: bool
    ready_for_patch_application: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("boundary_id", "release_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if not repair_proposal_flags_preserve_no_execution(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        for name in ("allowed_surfaces", "prohibited_surfaces", "gaps", "blocked_reasons", "evidence_refs", "withdrawal_conditions"):
            _validate_list(name, getattr(self, name))
        RepairProposalStatus(self.status)
        RepairProposalReadinessLevel(self.readiness_level)
        for name in ("ready_for_execution", "ready_for_source_file_read", "ready_for_repair_proposal_generation", "ready_for_proposed_diff_generation", "ready_for_repair_execution", "ready_for_patch_application"):
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must always be False in v0.38.0")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalPermissionRequest:
    request_id: str
    version: str
    requested_surface: RepairProposalSurfaceKind | str
    requested_capability: RepairProposalCapabilityKind | str
    request_summary: str
    source_refs: list[RepairProposalSourceRef]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("request_id", "request_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalSurfaceKind(self.requested_surface)
        RepairProposalCapabilityKind(self.requested_capability)
        _validate_list("source_refs", self.source_refs)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalPermissionDecision:
    decision_id: str
    request_id: str
    decision_kind: RepairProposalDecisionKind | str
    reason: str
    risk_kinds: list[RepairProposalRiskKind | str]
    evidence_refs: list[str]
    source_file_read_allowed: bool
    sandbox_source_read_allowed: bool
    repair_proposal_generation_allowed: bool
    proposed_diff_generation_allowed: bool
    proposed_code_hunk_generation_allowed: bool
    proposed_patch_envelope_generation_allowed: bool
    file_write_allowed: bool
    patch_apply_allowed: bool
    repair_execution_allowed: bool
    test_execution_allowed: bool
    subprocess_allowed: bool
    shell_allowed: bool
    dependency_install_allowed: bool
    network_access_allowed: bool
    model_provider_invocation_allowed: bool
    external_agent_execution_allowed: bool
    dominion_runtime_allowed: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("decision_id", "request_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairProposalRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, UNSAFE_DECISION_ALLOW_NAMES)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalDeniedAction:
    denied_action_id: str
    request_id: str | None
    decision_id: str | None
    surface_kind: RepairProposalSurfaceKind | str
    capability_kind: RepairProposalCapabilityKind | str
    risk_kinds: list[RepairProposalRiskKind | str]
    reason: str
    safe_alternatives: list[str]
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("denied_action_id", "reason"):
            _require_non_blank(name, getattr(self, name))
        RepairProposalSurfaceKind(self.surface_kind)
        RepairProposalCapabilityKind(self.capability_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairProposalRiskKind)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalGateEvaluation:
    gate_evaluation_id: str
    version: str
    request: RepairProposalPermissionRequest
    decision: RepairProposalPermissionDecision
    denied_action: RepairProposalDeniedAction | None
    gate_summary: str
    passed: bool
    blocked: bool
    ready_for_execution: bool
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("gate_evaluation_id", "gate_summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalRiskRegister:
    risk_register_id: str
    version: str
    risk_kinds: list[RepairProposalRiskKind | str]
    high_risk_surfaces: list[RepairProposalSurfaceKind | str]
    mitigations: list[str]
    unresolved_risks: list[str]
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("risk_register_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_enum_list("risk_kinds", self.risk_kinds, RepairProposalRiskKind)
        _validate_enum_list("high_risk_surfaces", self.high_risk_surfaces, RepairProposalSurfaceKind)
        _validate_string_list("mitigations", self.mitigations)
        _validate_string_list("unresolved_risks", self.unresolved_risks)
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class RepairProposalNoExecutionGuarantee:
    guarantee_id: str
    version: str
    no_source_file_read: bool
    no_sandbox_source_read: bool
    no_repair_proposal_generation: bool
    no_proposed_diff_generation: bool
    no_proposed_code_hunk_generation: bool
    no_proposed_patch_envelope_generation: bool
    no_repair_patch_proposal: bool
    no_file_write: bool
    no_file_edit: bool
    no_patch_application: bool
    no_apply_patch: bool
    no_git_apply: bool
    no_repair_execution: bool
    no_automatic_repair: bool
    no_repair_loop: bool
    no_retry_loop: bool
    no_multi_cycle_repair_loop: bool
    no_test_execution: bool
    no_subprocess_execution: bool
    no_shell_execution: bool
    no_command_execution: bool
    no_dependency_install: bool
    no_network_access: bool
    no_model_provider_invocation: bool
    no_tool_execution: bool
    no_external_agent_execution: bool
    no_claude_code_invocation: bool
    no_codex_cli_invocation: bool
    no_dominion_runtime: bool
    no_provider_invocation: bool
    no_credential_access: bool
    no_secret_read: bool
    no_autonomous_agent_runtime: bool
    no_general_tool_execution: bool
    no_persistent_trace_write: bool
    no_ui_runtime: bool
    no_authority_grant: bool
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("guarantee_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V038RoadmapOverview:
    roadmap_id: str
    version: str
    track_name: str
    roadmap_items: list[str]
    current_release: RepairProposalTrackKind | str
    next_release: RepairProposalTrackKind | str
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("roadmap_id", "track_name", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        _validate_string_list("roadmap_items", self.roadmap_items)
        RepairProposalTrackKind(self.current_release)
        RepairProposalTrackKind(self.next_release)
        for index in range(10):
            if not any(f"v0.38.{index}" in item for item in self.roadmap_items):
                raise ValueError("roadmap_items must include v0.38.0-v0.38.9")
        _validate_metadata(self.metadata)


@dataclass(frozen=True, kw_only=True)
class V0380ReadinessReport:
    readiness_report_id: str
    version: str
    boundary_id: str
    readiness_level: RepairProposalReadinessLevel | str
    status: RepairProposalStatus | str
    summary: str
    evidence_refs: list[str]
    metadata: dict[str, Any]
    repair_proposal_boundary_constructed: bool
    ready_for_v0381_repair_proposal_evidence_contract: bool
    ready_for_v0382_read_only_sandbox_source_context: bool
    ready_for_v0383_repair_scope_planner_change_intent: bool
    ready_for_v0384_proposed_diff_code_hunk_metadata: bool
    ready_for_v0385_repair_proposal_safety_validation: bool
    ready_for_v0386_human_review_packet: bool
    ready_for_v0387_bounded_repair_proposal_loop_trial: bool
    ready_for_v0388_cli_repair_proposal_surface: bool
    ready_for_bounded_repair_proposal_boundary: bool
    ready_for_repair_proposal_policy_boundary: bool
    ready_for_repair_evidence_contract_boundary: bool
    ready_for_read_only_sandbox_source_context_boundary: bool
    ready_for_repair_scope_planning_boundary: bool
    ready_for_change_intent_boundary: bool
    ready_for_proposed_diff_metadata_boundary: bool
    ready_for_proposed_code_hunk_metadata_boundary: bool
    ready_for_proposed_patch_envelope_boundary: bool
    ready_for_repair_safety_validation_boundary: bool
    ready_for_repair_human_review_boundary: bool
    ready_for_do_nothing_repair_comparison_boundary: bool
    ready_for_future_sandbox_repair_apply_input_boundary: bool
    ready_for_execution: bool
    ready_for_general_execution: bool
    ready_for_source_file_read: bool
    ready_for_sandbox_source_read: bool
    ready_for_repair_proposal_generation: bool
    ready_for_proposed_diff_generation: bool
    ready_for_proposed_code_hunk_generation: bool
    ready_for_proposed_patch_envelope_generation: bool
    ready_for_repair_patch_proposal: bool
    ready_for_repair_execution: bool
    ready_for_sandbox_repair_apply: bool
    ready_for_patch_application: bool
    ready_for_apply_patch: bool
    ready_for_git_apply: bool
    ready_for_automatic_repair: bool
    ready_for_test_execution: bool
    ready_for_shell_execution: bool
    ready_for_model_provider_invocation: bool
    ready_for_external_agent_execution: bool
    ready_for_dominion_runtime: bool
    production_certified: bool

    def __post_init__(self) -> None:
        for name in ("readiness_report_id", "boundary_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version(self.version)
        RepairProposalReadinessLevel(self.readiness_level)
        RepairProposalStatus(self.status)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, tuple(name for name in UNSAFE_FLAG_NAMES if hasattr(self, name)))
        _validate_metadata(self.metadata)


def build_repair_proposal_flags(**kwargs: Any) -> RepairProposalFlagSet:
    return RepairProposalFlagSet(
        flag_set_id=kwargs.pop("flag_set_id", "repair_proposal_flags:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        repair_proposal_boundary_constructed=kwargs.pop("repair_proposal_boundary_constructed", True),
        repair_proposal_policy_defined=kwargs.pop("repair_proposal_policy_defined", True),
        repair_evidence_contract_boundary_defined=kwargs.pop("repair_evidence_contract_boundary_defined", True),
        read_only_source_context_boundary_defined=kwargs.pop("read_only_source_context_boundary_defined", True),
        repair_scope_planning_boundary_defined=kwargs.pop("repair_scope_planning_boundary_defined", True),
        change_intent_boundary_defined=kwargs.pop("change_intent_boundary_defined", True),
        proposed_diff_metadata_boundary_defined=kwargs.pop("proposed_diff_metadata_boundary_defined", True),
        proposed_code_hunk_metadata_boundary_defined=kwargs.pop("proposed_code_hunk_metadata_boundary_defined", True),
        proposed_patch_envelope_boundary_defined=kwargs.pop("proposed_patch_envelope_boundary_defined", True),
        repair_safety_validation_boundary_defined=kwargs.pop("repair_safety_validation_boundary_defined", True),
        repair_human_review_boundary_defined=kwargs.pop("repair_human_review_boundary_defined", True),
        do_nothing_repair_comparison_boundary_defined=kwargs.pop("do_nothing_repair_comparison_boundary_defined", True),
        repair_proposal_risk_register_defined=kwargs.pop("repair_proposal_risk_register_defined", True),
        ready_for_v0381_repair_proposal_evidence_contract=kwargs.pop("ready_for_v0381_repair_proposal_evidence_contract", True),
        ready_for_v0382_read_only_sandbox_source_context=kwargs.pop("ready_for_v0382_read_only_sandbox_source_context", True),
        ready_for_v0383_repair_scope_planner_change_intent=kwargs.pop("ready_for_v0383_repair_scope_planner_change_intent", True),
        ready_for_v0384_proposed_diff_code_hunk_metadata=kwargs.pop("ready_for_v0384_proposed_diff_code_hunk_metadata", True),
        ready_for_v0385_repair_proposal_safety_validation=kwargs.pop("ready_for_v0385_repair_proposal_safety_validation", True),
        ready_for_v0386_human_review_packet=kwargs.pop("ready_for_v0386_human_review_packet", True),
        ready_for_v0387_bounded_repair_proposal_loop_trial=kwargs.pop("ready_for_v0387_bounded_repair_proposal_loop_trial", True),
        ready_for_v0388_cli_repair_proposal_surface=kwargs.pop("ready_for_v0388_cli_repair_proposal_surface", True),
        ready_for_bounded_repair_proposal_boundary=kwargs.pop("ready_for_bounded_repair_proposal_boundary", True),
        ready_for_repair_proposal_policy_boundary=kwargs.pop("ready_for_repair_proposal_policy_boundary", True),
        ready_for_repair_evidence_contract_boundary=kwargs.pop("ready_for_repair_evidence_contract_boundary", True),
        ready_for_read_only_sandbox_source_context_boundary=kwargs.pop("ready_for_read_only_sandbox_source_context_boundary", True),
        ready_for_repair_scope_planning_boundary=kwargs.pop("ready_for_repair_scope_planning_boundary", True),
        ready_for_change_intent_boundary=kwargs.pop("ready_for_change_intent_boundary", True),
        ready_for_proposed_diff_metadata_boundary=kwargs.pop("ready_for_proposed_diff_metadata_boundary", True),
        ready_for_proposed_code_hunk_metadata_boundary=kwargs.pop("ready_for_proposed_code_hunk_metadata_boundary", True),
        ready_for_proposed_patch_envelope_boundary=kwargs.pop("ready_for_proposed_patch_envelope_boundary", True),
        ready_for_repair_safety_validation_boundary=kwargs.pop("ready_for_repair_safety_validation_boundary", True),
        ready_for_repair_human_review_boundary=kwargs.pop("ready_for_repair_human_review_boundary", True),
        ready_for_do_nothing_repair_comparison_boundary=kwargs.pop("ready_for_do_nothing_repair_comparison_boundary", True),
        ready_for_future_sandbox_repair_apply_input_boundary=kwargs.pop("ready_for_future_sandbox_repair_apply_input_boundary", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_FLAG_NAMES},
    )


def build_repair_proposal_source_ref(**kwargs: Any) -> RepairProposalSourceRef:
    return RepairProposalSourceRef(
        source_ref_id=kwargs.pop("source_ref_id", "repair_proposal_source_ref:v0.38.0"),
        source_kind=kwargs.pop("source_kind", RepairProposalSourceKind.V0379_TEST_RUNNER_CONSOLIDATION),
        source_id=kwargs.pop("source_id", "v0379_consolidation_report"),
        source_summary=kwargs.pop("source_summary", "v0.37.9 handoff metadata only"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.9 consolidation"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_boundary_policy(**kwargs: Any) -> RepairProposalBoundaryPolicy:
    return RepairProposalBoundaryPolicy(
        policy_id=kwargs.pop("policy_id", "repair_proposal_boundary_policy:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        repair_posture=kwargs.pop("repair_posture", RepairProposalPosture.BOUNDARY_ONLY),
        diff_posture=kwargs.pop("diff_posture", ProposedDiffPosture.NO_DIFF_GENERATION),
        hunk_posture=kwargs.pop("hunk_posture", ProposedCodeHunkPosture.NO_HUNK_GENERATION),
        patch_envelope_posture=kwargs.pop("patch_envelope_posture", ProposedPatchEnvelopePosture.NO_PATCH_ENVELOPE_GENERATION),
        source_context_posture=kwargs.pop("source_context_posture", RepairSourceContextPosture.NO_SOURCE_READ),
        human_review_posture=kwargs.pop("human_review_posture", RepairHumanReviewPosture.HUMAN_REVIEW_REQUIRED_BOUNDARY),
        do_nothing_posture=kwargs.pop("do_nothing_posture", RepairDoNothingPosture.DO_NOTHING_BOUNDARY_DEFINED),
        allowed_surfaces=kwargs.pop("allowed_surfaces", [
            RepairProposalSurfaceKind.REPAIR_PROPOSAL_BOUNDARY,
            RepairProposalSurfaceKind.REPAIR_EVIDENCE_CONTRACT,
            RepairProposalSurfaceKind.REPAIR_SCOPE_PLAN,
            RepairProposalSurfaceKind.PROPOSED_DIFF_METADATA,
            RepairProposalSurfaceKind.PROPOSED_CODE_HUNK_METADATA,
            RepairProposalSurfaceKind.PROPOSED_PATCH_ENVELOPE,
            RepairProposalSurfaceKind.REPAIR_HUMAN_REVIEW_PACKET,
            RepairProposalSurfaceKind.FUTURE_SANDBOX_REPAIR_APPLY_INPUT,
        ]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [
            RepairProposalSurfaceKind.LIVE_WORKSPACE_WRITE,
            RepairProposalSurfaceKind.FILE_EDIT,
            RepairProposalSurfaceKind.PATCH_APPLICATION,
            RepairProposalSurfaceKind.APPLY_PATCH,
            RepairProposalSurfaceKind.GIT_APPLY,
            RepairProposalSurfaceKind.AUTOMATIC_REPAIR,
            RepairProposalSurfaceKind.REPAIR_EXECUTION,
            RepairProposalSurfaceKind.ARBITRARY_SHELL,
            RepairProposalSurfaceKind.MODEL_PROVIDER_INVOCATION,
            RepairProposalSurfaceKind.EXTERNAL_AGENT_EXECUTION,
            RepairProposalSurfaceKind.DOMINION_RUNTIME,
        ]),
        prohibited_capabilities=kwargs.pop("prohibited_capabilities", [
            RepairProposalCapabilityKind.CREATE_REPAIR_PROPOSAL,
            RepairProposalCapabilityKind.READ_SANDBOX_SOURCE,
            RepairProposalCapabilityKind.GENERATE_PROPOSED_DIFF,
            RepairProposalCapabilityKind.GENERATE_CODE_HUNK,
            RepairProposalCapabilityKind.GENERATE_PATCH_ENVELOPE,
            RepairProposalCapabilityKind.EDIT_FILE,
            RepairProposalCapabilityKind.APPLY_PATCH_RUNTIME,
            RepairProposalCapabilityKind.GIT_APPLY_RUNTIME,
            RepairProposalCapabilityKind.EXECUTE_REPAIR,
            RepairProposalCapabilityKind.RUN_TESTS,
            RepairProposalCapabilityKind.CALL_MODEL_PROVIDER,
            RepairProposalCapabilityKind.INVOKE_EXTERNAL_AGENT,
            RepairProposalCapabilityKind.RUN_DOMINION_RUNTIME,
        ]),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["source_read", "proposal_generation", "diff_generation", "hunk_generation", "patch_apply", "repair_execution", "test_execution", "shell", "model_provider", "external_agent", "dominion"]),
        allow_boundary_definition=kwargs.pop("allow_boundary_definition", True),
        allow_evidence_contract_future_gate=kwargs.pop("allow_evidence_contract_future_gate", True),
        allow_read_only_source_context_future_gate=kwargs.pop("allow_read_only_source_context_future_gate", True),
        allow_scope_planning_future_gate=kwargs.pop("allow_scope_planning_future_gate", True),
        allow_change_intent_future_gate=kwargs.pop("allow_change_intent_future_gate", True),
        allow_proposed_diff_metadata_future_gate=kwargs.pop("allow_proposed_diff_metadata_future_gate", True),
        allow_proposed_code_hunk_metadata_future_gate=kwargs.pop("allow_proposed_code_hunk_metadata_future_gate", True),
        allow_proposed_patch_envelope_future_gate=kwargs.pop("allow_proposed_patch_envelope_future_gate", True),
        allow_safety_validation_future_gate=kwargs.pop("allow_safety_validation_future_gate", True),
        allow_human_review_future_gate=kwargs.pop("allow_human_review_future_gate", True),
        allow_do_nothing_comparison_future_gate=kwargs.pop("allow_do_nothing_comparison_future_gate", True),
        allow_future_sandbox_repair_apply_input_boundary=kwargs.pop("allow_future_sandbox_repair_apply_input_boundary", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_POLICY_ALLOW_NAMES},
    )


def _build_subpolicy(cls: type[RepairBoundarySubPolicy], policy_id: str, summary: str, **kwargs: Any) -> RepairBoundarySubPolicy:
    return cls(
        policy_id=kwargs.pop("policy_id", policy_id),
        version=kwargs.pop("version", V0380_VERSION),
        summary=kwargs.pop("summary", summary),
        future_gated=kwargs.pop("future_gated", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_SUBPOLICY_ALLOW_NAMES},
    )


def build_repair_evidence_boundary_policy(**kwargs: Any) -> RepairEvidenceBoundaryPolicy:
    return _build_subpolicy(RepairEvidenceBoundaryPolicy, "repair_evidence_boundary_policy:v0.38.0", "repair evidence contract boundary only", **kwargs)


def build_repair_source_context_boundary_policy(**kwargs: Any) -> RepairSourceContextBoundaryPolicy:
    return _build_subpolicy(RepairSourceContextBoundaryPolicy, "repair_source_context_boundary_policy:v0.38.0", "source context boundary only; no source read in v0.38.0", **kwargs)


def build_repair_scope_planning_boundary_policy(**kwargs: Any) -> RepairScopePlanningBoundaryPolicy:
    return _build_subpolicy(RepairScopePlanningBoundaryPolicy, "repair_scope_planning_boundary_policy:v0.38.0", "repair scope planning boundary only", **kwargs)


def build_repair_patch_metadata_boundary_policy(**kwargs: Any) -> RepairPatchMetadataBoundaryPolicy:
    return _build_subpolicy(RepairPatchMetadataBoundaryPolicy, "repair_patch_metadata_boundary_policy:v0.38.0", "proposed diff, code hunk, and patch envelope metadata boundary only", **kwargs)


def build_repair_safety_validation_boundary_policy(**kwargs: Any) -> RepairSafetyValidationBoundaryPolicy:
    return _build_subpolicy(RepairSafetyValidationBoundaryPolicy, "repair_safety_validation_boundary_policy:v0.38.0", "repair proposal safety validation boundary only", **kwargs)


def build_repair_human_review_boundary_policy(**kwargs: Any) -> RepairHumanReviewBoundaryPolicy:
    return _build_subpolicy(RepairHumanReviewBoundaryPolicy, "repair_human_review_boundary_policy:v0.38.0", "human review requirement boundary only; not approval", **kwargs)


def build_repair_future_apply_boundary_policy(**kwargs: Any) -> RepairFutureApplyBoundaryPolicy:
    return _build_subpolicy(RepairFutureApplyBoundaryPolicy, "repair_future_apply_boundary_policy:v0.38.0", "future sandbox repair apply input boundary only; not apply", **kwargs)


def build_repair_proposal_allowed_surface(**kwargs: Any) -> RepairProposalAllowedSurface:
    return RepairProposalAllowedSurface(
        allowed_surface_id=kwargs.pop("allowed_surface_id", "repair_proposal_allowed_surface:v0.38.0"),
        surface_kind=kwargs.pop("surface_kind", RepairProposalSurfaceKind.REPAIR_PROPOSAL_BOUNDARY),
        capability_kind=kwargs.pop("capability_kind", RepairProposalCapabilityKind.DEFINE_REPAIR_PROPOSAL_BOUNDARY),
        description=kwargs.pop("description", "design-stage repair proposal boundary surface only"),
        allowed_only_for_design_stage=kwargs.pop("allowed_only_for_design_stage", True),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_ALLOWED_SURFACE_NAMES},
    )


def build_repair_proposal_prohibited_surface(**kwargs: Any) -> RepairProposalProhibitedSurface:
    return RepairProposalProhibitedSurface(
        prohibited_surface_id=kwargs.pop("prohibited_surface_id", "repair_proposal_prohibited_surface:v0.38.0"),
        surface_kind=kwargs.pop("surface_kind", RepairProposalSurfaceKind.PATCH_APPLICATION),
        risk_kind=kwargs.pop("risk_kind", RepairProposalRiskKind.PATCH_APPLICATION_RISK),
        capability_kind=kwargs.pop("capability_kind", RepairProposalCapabilityKind.APPLY_PATCH_RUNTIME),
        reason=kwargs.pop("reason", "unsafe repair proposal runtime surface remains blocked"),
        prohibited_runtime_actions=kwargs.pop("prohibited_runtime_actions", ["proposal_generation", "diff_generation", "patch_application", "repair_execution"]),
        blocks_proposal_generation=kwargs.pop("blocks_proposal_generation", True),
        blocks_repair_execution=kwargs.pop("blocks_repair_execution", True),
        blocks_runtime_readiness=kwargs.pop("blocks_runtime_readiness", True),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.0 boundary"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_boundary(**kwargs: Any) -> RepairProposalBoundary:
    flags = kwargs.pop("flags", build_repair_proposal_flags())
    return RepairProposalBoundary(
        boundary_id=kwargs.pop("boundary_id", "repair_proposal_boundary:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        release_name=kwargs.pop("release_name", V0380_RELEASE_NAME),
        boundary_policy=kwargs.pop("boundary_policy", build_repair_proposal_boundary_policy()),
        evidence_policy=kwargs.pop("evidence_policy", build_repair_evidence_boundary_policy()),
        source_context_policy=kwargs.pop("source_context_policy", build_repair_source_context_boundary_policy()),
        scope_policy=kwargs.pop("scope_policy", build_repair_scope_planning_boundary_policy()),
        patch_metadata_policy=kwargs.pop("patch_metadata_policy", build_repair_patch_metadata_boundary_policy()),
        safety_policy=kwargs.pop("safety_policy", build_repair_safety_validation_boundary_policy()),
        human_review_policy=kwargs.pop("human_review_policy", build_repair_human_review_boundary_policy()),
        future_apply_policy=kwargs.pop("future_apply_policy", build_repair_future_apply_boundary_policy()),
        allowed_surfaces=kwargs.pop("allowed_surfaces", [build_repair_proposal_allowed_surface()]),
        prohibited_surfaces=kwargs.pop("prohibited_surfaces", [build_repair_proposal_prohibited_surface()]),
        flags=flags,
        status=kwargs.pop("status", RepairProposalStatus.BOUNDARY_READY),
        readiness_level=kwargs.pop("readiness_level", RepairProposalReadinessLevel.BOUNDED_REPAIR_PROPOSAL_BOUNDARY_READY),
        summary=kwargs.pop("summary", "bounded repair proposal boundary foundation only; no proposal generation"),
        gaps=kwargs.pop("gaps", ["repair evidence contract is v0.38.1", "source context snapshot is v0.38.2", "patch metadata generation is v0.38.4"]),
        blocked_reasons=kwargs.pop("blocked_reasons", ["proposal generation remains disabled", "source read remains disabled", "patch apply remains disabled"]),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.9 handoff"]),
        withdrawal_conditions=kwargs.pop("withdrawal_conditions", ["withdraw if any generation or execution readiness becomes true"]),
        ready_for_v0381_repair_proposal_evidence_contract=kwargs.pop("ready_for_v0381_repair_proposal_evidence_contract", True),
        ready_for_v0382_read_only_sandbox_source_context=kwargs.pop("ready_for_v0382_read_only_sandbox_source_context", True),
        ready_for_v0384_proposed_diff_code_hunk_metadata=kwargs.pop("ready_for_v0384_proposed_diff_code_hunk_metadata", True),
        ready_for_bounded_repair_proposal_boundary=kwargs.pop("ready_for_bounded_repair_proposal_boundary", True),
        ready_for_repair_human_review_boundary=kwargs.pop("ready_for_repair_human_review_boundary", True),
        ready_for_do_nothing_repair_comparison_boundary=kwargs.pop("ready_for_do_nothing_repair_comparison_boundary", True),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        ready_for_source_file_read=kwargs.pop("ready_for_source_file_read", False),
        ready_for_repair_proposal_generation=kwargs.pop("ready_for_repair_proposal_generation", False),
        ready_for_proposed_diff_generation=kwargs.pop("ready_for_proposed_diff_generation", False),
        ready_for_repair_execution=kwargs.pop("ready_for_repair_execution", False),
        ready_for_patch_application=kwargs.pop("ready_for_patch_application", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_permission_request(**kwargs: Any) -> RepairProposalPermissionRequest:
    return RepairProposalPermissionRequest(
        request_id=kwargs.pop("request_id", "repair_proposal_permission_request:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        requested_surface=kwargs.pop("requested_surface", RepairProposalSurfaceKind.REPAIR_PROPOSAL_BOUNDARY),
        requested_capability=kwargs.pop("requested_capability", RepairProposalCapabilityKind.DEFINE_REPAIR_PROPOSAL_BOUNDARY),
        request_summary=kwargs.pop("request_summary", "boundary definition request only"),
        source_refs=kwargs.pop("source_refs", [build_repair_proposal_source_ref()]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_permission_decision(**kwargs: Any) -> RepairProposalPermissionDecision:
    return RepairProposalPermissionDecision(
        decision_id=kwargs.pop("decision_id", "repair_proposal_permission_decision:v0.38.0"),
        request_id=kwargs.pop("request_id", "repair_proposal_permission_request:v0.38.0"),
        decision_kind=kwargs.pop("decision_kind", RepairProposalDecisionKind.ALLOW_BOUNDARY_DEFINITION),
        reason=kwargs.pop("reason", "boundary definition allowed; proposal generation remains blocked"),
        risk_kinds=kwargs.pop("risk_kinds", [RepairProposalRiskKind.PATCH_PROPOSAL_CONFUSION_RISK]),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.38.0 boundary"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, False) for name in UNSAFE_DECISION_ALLOW_NAMES},
    )


def build_repair_proposal_denied_action(**kwargs: Any) -> RepairProposalDeniedAction:
    return RepairProposalDeniedAction(
        denied_action_id=kwargs.pop("denied_action_id", "repair_proposal_denied_action:v0.38.0"),
        request_id=kwargs.pop("request_id", None),
        decision_id=kwargs.pop("decision_id", None),
        surface_kind=kwargs.pop("surface_kind", RepairProposalSurfaceKind.PATCH_APPLICATION),
        capability_kind=kwargs.pop("capability_kind", RepairProposalCapabilityKind.APPLY_PATCH_RUNTIME),
        risk_kinds=kwargs.pop("risk_kinds", [RepairProposalRiskKind.PATCH_APPLICATION_RISK]),
        reason=kwargs.pop("reason", "unsafe repair proposal action denied"),
        safe_alternatives=kwargs.pop("safe_alternatives", ["define boundary", "future evidence contract", "do-nothing alternative"]),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_gate_evaluation(**kwargs: Any) -> RepairProposalGateEvaluation:
    request = kwargs.pop("request", build_repair_proposal_permission_request())
    decision = kwargs.pop("decision", build_repair_proposal_permission_decision(request_id=request.request_id))
    return RepairProposalGateEvaluation(
        gate_evaluation_id=kwargs.pop("gate_evaluation_id", "repair_proposal_gate_evaluation:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        request=request,
        decision=decision,
        denied_action=kwargs.pop("denied_action", None),
        gate_summary=kwargs.pop("gate_summary", "gate evaluation is metadata only"),
        passed=kwargs.pop("passed", True),
        blocked=kwargs.pop("blocked", False),
        ready_for_execution=kwargs.pop("ready_for_execution", False),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_risk_register(**kwargs: Any) -> RepairProposalRiskRegister:
    return RepairProposalRiskRegister(
        risk_register_id=kwargs.pop("risk_register_id", "repair_proposal_risk_register:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        risk_kinds=kwargs.pop("risk_kinds", [
            RepairProposalRiskKind.REPAIR_EXECUTION_CONFUSION_RISK,
            RepairProposalRiskKind.PATCH_PROPOSAL_CONFUSION_RISK,
            RepairProposalRiskKind.DIFF_GENERATION_CONFUSION_RISK,
            RepairProposalRiskKind.CODE_HUNK_GENERATION_CONFUSION_RISK,
            RepairProposalRiskKind.PATCH_APPLICATION_RISK,
            RepairProposalRiskKind.SOURCE_READ_SCOPE_RISK,
            RepairProposalRiskKind.INSUFFICIENT_EVIDENCE_RISK,
            RepairProposalRiskKind.DO_NOTHING_OMISSION_RISK,
            RepairProposalRiskKind.HUMAN_REVIEW_OMISSION_RISK,
            RepairProposalRiskKind.AUTOMATIC_REPAIR_RISK,
            RepairProposalRiskKind.RETRY_LOOP_RISK,
            RepairProposalRiskKind.MULTI_CYCLE_LOOP_RISK,
            RepairProposalRiskKind.MODEL_PROVIDER_INVOCATION_RISK,
            RepairProposalRiskKind.EXTERNAL_AGENT_EXECUTION_RISK,
            RepairProposalRiskKind.DOMINION_RUNTIME_RISK,
        ]),
        high_risk_surfaces=kwargs.pop("high_risk_surfaces", [
            RepairProposalSurfaceKind.PATCH_APPLICATION,
            RepairProposalSurfaceKind.APPLY_PATCH,
            RepairProposalSurfaceKind.GIT_APPLY,
            RepairProposalSurfaceKind.AUTOMATIC_REPAIR,
            RepairProposalSurfaceKind.MODEL_PROVIDER_INVOCATION,
            RepairProposalSurfaceKind.EXTERNAL_AGENT_EXECUTION,
            RepairProposalSurfaceKind.DOMINION_RUNTIME,
        ]),
        mitigations=kwargs.pop("mitigations", ["boundary-only posture", "human review boundary", "do-nothing boundary", "unsafe readiness false"]),
        unresolved_risks=kwargs.pop("unresolved_risks", ["proposal generation remains future-gated"]),
        summary=kwargs.pop("summary", "risk register for future bounded repair proposal loop"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_repair_proposal_no_execution_guarantee(**kwargs: Any) -> RepairProposalNoExecutionGuarantee:
    no_names = tuple(name for name in RepairProposalNoExecutionGuarantee.__dataclass_fields__ if name.startswith("no_"))
    return RepairProposalNoExecutionGuarantee(
        guarantee_id=kwargs.pop("guarantee_id", "repair_proposal_no_execution_guarantee:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        summary=kwargs.pop("summary", "v0.38.0 defines boundaries only and executes/generates/reads nothing"),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, True) for name in no_names},
    )


def build_v038_roadmap_overview(**kwargs: Any) -> V038RoadmapOverview:
    return V038RoadmapOverview(
        roadmap_id=kwargs.pop("roadmap_id", "v038_roadmap_overview:v0.38.0"),
        version=kwargs.pop("version", V0380_VERSION),
        track_name=kwargs.pop("track_name", "Bounded Repair Proposal Loop"),
        roadmap_items=kwargs.pop("roadmap_items", [
            "v0.38.0 Bounded Repair Proposal Boundary Foundation",
            "v0.38.1 Repair Proposal Evidence Contract",
            "v0.38.2 Read-only Sandbox Source Context Snapshot",
            "v0.38.3 Repair Scope Planner & Change Intent Model",
            "v0.38.4 Proposed Diff / Code Hunk Metadata Generation",
            "v0.38.5 Repair Proposal Safety & Static Validation",
            "v0.38.6 Human Review Packet & Approval Request Contract",
            "v0.38.7 Bounded Repair Proposal Loop Trial",
            "v0.38.8 CLI Repair Proposal Surface",
            "v0.38.9 Bounded Repair Proposal Loop Consolidation",
        ]),
        current_release=kwargs.pop("current_release", RepairProposalTrackKind.BOUNDARY_FOUNDATION),
        next_release=kwargs.pop("next_release", RepairProposalTrackKind.REPAIR_PROPOSAL_EVIDENCE_CONTRACT),
        summary=kwargs.pop("summary", "v0.38 roadmap overview; no generation in v0.38.0"),
        metadata=kwargs.pop("metadata", {}),
    )


def build_v0380_readiness_report(**kwargs: Any) -> V0380ReadinessReport:
    safe_defaults = {
        "repair_proposal_boundary_constructed": True,
        "ready_for_v0381_repair_proposal_evidence_contract": True,
        "ready_for_v0382_read_only_sandbox_source_context": True,
        "ready_for_v0383_repair_scope_planner_change_intent": True,
        "ready_for_v0384_proposed_diff_code_hunk_metadata": True,
        "ready_for_v0385_repair_proposal_safety_validation": True,
        "ready_for_v0386_human_review_packet": True,
        "ready_for_v0387_bounded_repair_proposal_loop_trial": True,
        "ready_for_v0388_cli_repair_proposal_surface": True,
        "ready_for_bounded_repair_proposal_boundary": True,
        "ready_for_repair_proposal_policy_boundary": True,
        "ready_for_repair_evidence_contract_boundary": True,
        "ready_for_read_only_sandbox_source_context_boundary": True,
        "ready_for_repair_scope_planning_boundary": True,
        "ready_for_change_intent_boundary": True,
        "ready_for_proposed_diff_metadata_boundary": True,
        "ready_for_proposed_code_hunk_metadata_boundary": True,
        "ready_for_proposed_patch_envelope_boundary": True,
        "ready_for_repair_safety_validation_boundary": True,
        "ready_for_repair_human_review_boundary": True,
        "ready_for_do_nothing_repair_comparison_boundary": True,
        "ready_for_future_sandbox_repair_apply_input_boundary": True,
    }
    return V0380ReadinessReport(
        readiness_report_id=kwargs.pop("readiness_report_id", "v0380_readiness_report"),
        version=kwargs.pop("version", V0380_VERSION),
        boundary_id=kwargs.pop("boundary_id", "repair_proposal_boundary:v0.38.0"),
        readiness_level=kwargs.pop("readiness_level", RepairProposalReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0381),
        status=kwargs.pop("status", RepairProposalStatus.BOUNDARY_READY),
        summary=kwargs.pop("summary", "v0.38.0 boundary ready; generation and execution remain false"),
        evidence_refs=kwargs.pop("evidence_refs", ["v0.37.9 handoff"]),
        metadata=kwargs.pop("metadata", {}),
        **{name: kwargs.pop(name, value) for name, value in safe_defaults.items()},
        **{name: kwargs.pop(name, False) for name in UNSAFE_FLAG_NAMES if name in V0380ReadinessReport.__dataclass_fields__},
    )


def repair_proposal_flags_preserve_no_execution(flags: RepairProposalFlagSet) -> bool:
    return isinstance(flags, RepairProposalFlagSet) and all(getattr(flags, name) is False for name in UNSAFE_FLAG_NAMES)


def repair_proposal_policy_blocks_generation_and_execution(policy: RepairProposalBoundaryPolicy) -> bool:
    return isinstance(policy, RepairProposalBoundaryPolicy) and all(getattr(policy, name) is False for name in UNSAFE_POLICY_ALLOW_NAMES)


def repair_patch_metadata_policy_blocks_generation(policy: RepairPatchMetadataBoundaryPolicy) -> bool:
    return isinstance(policy, RepairPatchMetadataBoundaryPolicy) and not policy.allows_diff_generation and not policy.allows_hunk_generation and not policy.allows_patch_generation


def repair_human_review_policy_is_not_approval(policy: RepairHumanReviewBoundaryPolicy) -> bool:
    return isinstance(policy, RepairHumanReviewBoundaryPolicy) and policy.future_gated and not policy.executable_in_v0380 and not policy.allows_patch_apply


def repair_future_apply_policy_blocks_apply(policy: RepairFutureApplyBoundaryPolicy) -> bool:
    return isinstance(policy, RepairFutureApplyBoundaryPolicy) and not policy.allows_patch_apply and not policy.allows_repair_execution


def repair_proposal_boundary_is_not_generation(boundary: RepairProposalBoundary) -> bool:
    return (
        isinstance(boundary, RepairProposalBoundary)
        and repair_proposal_flags_preserve_no_execution(boundary.flags)
        and not boundary.ready_for_execution
        and not boundary.ready_for_source_file_read
        and not boundary.ready_for_repair_proposal_generation
        and not boundary.ready_for_proposed_diff_generation
        and not boundary.ready_for_repair_execution
        and not boundary.ready_for_patch_application
    )


def repair_proposal_permission_decision_is_not_generation(decision: RepairProposalPermissionDecision) -> bool:
    return isinstance(decision, RepairProposalPermissionDecision) and all(getattr(decision, name) is False for name in UNSAFE_DECISION_ALLOW_NAMES)


def v0380_readiness_report_is_not_execution_ready(report: V0380ReadinessReport) -> bool:
    return isinstance(report, V0380ReadinessReport) and all(
        getattr(report, name) is False for name in UNSAFE_FLAG_NAMES if hasattr(report, name)
    )
