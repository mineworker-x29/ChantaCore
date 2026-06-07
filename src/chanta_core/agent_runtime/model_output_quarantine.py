from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)
from .model_response import (
    ModelResponseActionSignal,
    ModelResponseActionSignalKind,
    ModelResponseEnvelope,
    ModelSanitizedResponsePayload,
)


V0345_VERSION = "v0.34.5"
V0345_RELEASE_NAME = "v0.34.5 Model Output Action Quarantine"
DEFAULT_MAX_ACTION_CANDIDATE_PREVIEW_CHARS = 2000
DEFAULT_MAX_ACTION_CANDIDATE_COUNT = 50

UNSAFE_ACTION_CANDIDATE_KINDS = {
    "unsupported_tool_candidate",
    "shell_command_candidate",
    "command_execution_candidate",
    "workspace_write_candidate",
    "code_edit_candidate",
    "patch_candidate",
    "patch_application_candidate",
    "dependency_install_candidate",
    "provider_reinvoke_candidate",
    "network_access_candidate",
    "credential_access_candidate",
    "secret_read_candidate",
    "external_harness_execution_candidate",
    "opencode_execution_candidate",
    "hermes_execution_candidate",
    "openclaw_execution_candidate",
    "reference_code_execution_candidate",
    "browser_rpa_gateway_candidate",
    "authority_grant_candidate",
    "unknown",
}

FUTURE_ROUTE_CANDIDATE_KINDS = {"safe_workspace_inspection_candidate", "safe_readonly_tool_candidate"}
NON_EXECUTING_ALLOWED_CANDIDATE_KINDS = {"final_response_candidate", "ask_user_candidate", "no_op_candidate"}

DEFAULT_QUARANTINE_PROHIBITED_UNTIL_LATER_GATE = [
    "action execution",
    "tool execution",
    "workspace inspection execution",
    "workspace write",
    "code edit",
    "patch proposal",
    "patch application",
    "shell execution",
    "subprocess execution",
    "command execution",
    "provider invocation",
    "existing boundary invocation",
    "network access",
    "credential access",
    "secret read",
    "agent step execution",
    "general agent execution",
    "autonomous loop",
    "reference code execution",
    "reference import",
    "dependency install",
    "raw response persistence",
    "raw model output persistence",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_QUARANTINE_WITHDRAWAL_CONDITIONS = [
    "Any action, tool, workspace inspection, provider, shell, command, write, edit, patch, reference, or harness execution path is introduced.",
    "Any patch proposal, patch application, raw output persistence, network access, credential access, or secret read path is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

UNSAFE_QUARANTINE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_action_execution",
    "ready_for_tool_execution",
    "ready_for_general_tool_execution",
    "ready_for_safe_workspace_inspection_execution",
    "ready_for_patch_proposal",
    "ready_for_patch_application",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_provider_invocation",
    "ready_for_existing_boundary_invocation",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_agent_step_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_raw_response_persistence",
    "ready_for_raw_model_output_persistence",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class ModelOutputActionCandidateKind(StrEnum):
    FINAL_RESPONSE_CANDIDATE = "final_response_candidate"
    ASK_USER_CANDIDATE = "ask_user_candidate"
    NO_OP_CANDIDATE = "no_op_candidate"
    SAFE_WORKSPACE_INSPECTION_CANDIDATE = "safe_workspace_inspection_candidate"
    SAFE_READONLY_TOOL_CANDIDATE = "safe_readonly_tool_candidate"
    UNSUPPORTED_TOOL_CANDIDATE = "unsupported_tool_candidate"
    SHELL_COMMAND_CANDIDATE = "shell_command_candidate"
    COMMAND_EXECUTION_CANDIDATE = "command_execution_candidate"
    WORKSPACE_WRITE_CANDIDATE = "workspace_write_candidate"
    CODE_EDIT_CANDIDATE = "code_edit_candidate"
    PATCH_CANDIDATE = "patch_candidate"
    PATCH_APPLICATION_CANDIDATE = "patch_application_candidate"
    DEPENDENCY_INSTALL_CANDIDATE = "dependency_install_candidate"
    PROVIDER_REINVOKE_CANDIDATE = "provider_reinvoke_candidate"
    NETWORK_ACCESS_CANDIDATE = "network_access_candidate"
    CREDENTIAL_ACCESS_CANDIDATE = "credential_access_candidate"
    SECRET_READ_CANDIDATE = "secret_read_candidate"
    EXTERNAL_HARNESS_EXECUTION_CANDIDATE = "external_harness_execution_candidate"
    OPENCODE_EXECUTION_CANDIDATE = "opencode_execution_candidate"
    HERMES_EXECUTION_CANDIDATE = "hermes_execution_candidate"
    OPENCLAW_EXECUTION_CANDIDATE = "openclaw_execution_candidate"
    REFERENCE_CODE_EXECUTION_CANDIDATE = "reference_code_execution_candidate"
    BROWSER_RPA_GATEWAY_CANDIDATE = "browser_rpa_gateway_candidate"
    AUTHORITY_GRANT_CANDIDATE = "authority_grant_candidate"
    UNKNOWN = "unknown"


class ModelOutputActionSourceKind(StrEnum):
    V0343_MODEL_RESPONSE_ACTION_SIGNAL = "v0343_model_response_action_signal"
    V0343_SANITIZED_RESPONSE_PAYLOAD = "v0343_sanitized_response_payload"
    V0343_MODEL_RESPONSE_ENVELOPE = "v0343_model_response_envelope"
    V0344_EXISTING_PROVIDER_BOUNDARY_RESULT = "v0344_existing_provider_boundary_result"
    V0342_MODEL_REQUEST_ENVELOPE = "v0342_model_request_envelope"
    SUPPLIED_RESPONSE_FIXTURE = "supplied_response_fixture"
    TEST_FIXTURE = "test_fixture"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    UNKNOWN = "unknown"


class ModelOutputActionTrustLevel(StrEnum):
    UNTRUSTED_MODEL_OUTPUT = "untrusted_model_output"
    SANITIZED_BUT_UNTRUSTED = "sanitized_but_untrusted"
    BOUNDARY_FILTERED = "boundary_filtered"
    TEST_FIXTURE = "test_fixture"
    BLOCKED = "blocked"
    UNKNOWN = "unknown"


class ModelOutputActionRiskKind(StrEnum):
    MODEL_OUTPUT_AS_AUTHORITY_RISK = "model_output_as_authority_risk"
    UNSAFE_TOOL_EXECUTION_RISK = "unsafe_tool_execution_risk"
    SHELL_EXECUTION_RISK = "shell_execution_risk"
    COMMAND_EXECUTION_RISK = "command_execution_risk"
    WORKSPACE_WRITE_RISK = "workspace_write_risk"
    CODE_EDIT_RISK = "code_edit_risk"
    PATCH_GENERATION_RISK = "patch_generation_risk"
    PATCH_APPLICATION_RISK = "patch_application_risk"
    DEPENDENCY_INSTALL_RISK = "dependency_install_risk"
    PROVIDER_REINVOKE_RISK = "provider_reinvoke_risk"
    NETWORK_ACCESS_RISK = "network_access_risk"
    CREDENTIAL_ACCESS_RISK = "credential_access_risk"
    SECRET_READ_RISK = "secret_read_risk"
    EXTERNAL_HARNESS_EXECUTION_RISK = "external_harness_execution_risk"
    REFERENCE_CODE_EXECUTION_RISK = "reference_code_execution_risk"
    BROWSER_RPA_GATEWAY_RISK = "browser_rpa_gateway_risk"
    AUTHORITY_GRANT_RISK = "authority_grant_risk"
    BOUNDARY_OVERRIDE_RISK = "boundary_override_risk"
    RAW_OUTPUT_PERSISTENCE_RISK = "raw_output_persistence_risk"
    UNKNOWN = "unknown"


class ModelOutputActionRouteKind(StrEnum):
    FINAL_RESPONSE_ROUTE = "final_response_route"
    ASK_USER_ROUTE = "ask_user_route"
    NO_OP_ROUTE = "no_op_route"
    FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE = "future_safe_workspace_inspection_route"
    FUTURE_AGENT_STEP_RUNNER_ROUTE = "future_agent_step_runner_route"
    FUTURE_PATCH_PROPOSAL_TRACK = "future_patch_proposal_track"
    BLOCKED_ROUTE = "blocked_route"
    REVIEW_REQUIRED_ROUTE = "review_required_route"
    FUTURE_GATE_ROUTE = "future_gate_route"
    UNKNOWN = "unknown"


class ModelOutputActionDecisionKind(StrEnum):
    ALLOW_NON_EXECUTING_FINAL_RESPONSE = "allow_non_executing_final_response"
    ALLOW_NON_EXECUTING_ASK_USER = "allow_non_executing_ask_user"
    ALLOW_NON_EXECUTING_NO_OP = "allow_non_executing_no_op"
    ALLOW_FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE = "allow_future_safe_workspace_inspection_route"
    ALLOW_FUTURE_AGENT_STEP_RUNNER_ROUTE = "allow_future_agent_step_runner_route"
    BLOCK_UNSAFE_CANDIDATE = "block_unsafe_candidate"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    NO_OP = "no_op"
    UNKNOWN = "unknown"


class ModelOutputActionQuarantineStatus(StrEnum):
    UNKNOWN = "unknown"
    EXTRACTED = "extracted"
    CLASSIFIED = "classified"
    QUARANTINED = "quarantined"
    BLOCKED = "blocked"
    ALLOWED_AS_NON_EXECUTING_ROUTE = "allowed_as_non_executing_route"
    FUTURE_GATED = "future_gated"
    REVIEW_REQUIRED = "review_required"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class ModelOutputActionReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    QUARANTINE_CONTRACT_READY = "quarantine_contract_ready"
    CANDIDATE_EXTRACTION_READY = "candidate_extraction_ready"
    QUARANTINE_VALIDATION_READY = "quarantine_validation_ready"
    DESIGN_HANDOFF_READY_FOR_V0346 = "design_handoff_ready_for_v0346"
    DESIGN_HANDOFF_READY_FOR_V0347 = "design_handoff_ready_for_v0347"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ModelOutputActionSignalStrength(StrEnum):
    UNKNOWN = "unknown"
    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"
    EXPLICIT = "explicit"
    BLOCKED = "blocked"


def _validate_version_includes_v0345(version: str) -> None:
    _require_non_blank("version", version)
    if V0345_VERSION not in version:
        raise ValueError("version must include v0.34.5")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.5")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.5")


def _validate_dict(name: str, value: dict[str, Any] | None) -> None:
    if value is not None and (not isinstance(value, dict) or not all(isinstance(key, str) for key in value)):
        raise TypeError(f"{name} must be dict[str, Any] or None")


def _validate_non_negative(name: str, value: int) -> None:
    if value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_metadata_no_execution(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "action_execution",
            "tool_execution",
            "workspace_inspection_execution",
            "provider_invocation",
            "existing_boundary_invocation",
            "network_access",
            "credential_access",
            "secret_read",
            "agent_step_execution",
            "shell_execution",
            "command_execution",
            "workspace_write",
            "code_edit",
            "patch_proposal",
            "patch_application",
            "raw_response_persistence",
            "raw_model_output_persistence",
            "persistent_trace_write",
            "authority_grant",
        },
    ):
        raise ValueError("v0.34.5 metadata cannot imply execution, provider access, patching, or persistence")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


def _bounded(value: str, limit: int) -> tuple[str, bool]:
    if len(value) <= limit:
        return value, False
    return value[:limit], True


def _is_unsafe_candidate_kind(candidate_kind: ModelOutputActionCandidateKind | str) -> bool:
    return ModelOutputActionCandidateKind(candidate_kind).value in UNSAFE_ACTION_CANDIDATE_KINDS


def _is_future_route_candidate_kind(candidate_kind: ModelOutputActionCandidateKind | str) -> bool:
    return ModelOutputActionCandidateKind(candidate_kind).value in FUTURE_ROUTE_CANDIDATE_KINDS


def _is_non_executing_allowed_candidate_kind(candidate_kind: ModelOutputActionCandidateKind | str) -> bool:
    return ModelOutputActionCandidateKind(candidate_kind).value in NON_EXECUTING_ALLOWED_CANDIDATE_KINDS


def _candidate_kind_from_action_signal(signal: ModelResponseActionSignal) -> ModelOutputActionCandidateKind:
    signal_kind = ModelResponseActionSignalKind(signal.signal_kind)
    mapping = {
        ModelResponseActionSignalKind.NO_ACTION_SIGNAL: ModelOutputActionCandidateKind.NO_OP_CANDIDATE,
        ModelResponseActionSignalKind.FINAL_ANSWER_LIKE: ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE,
        ModelResponseActionSignalKind.TOOL_CALL_LIKE: ModelOutputActionCandidateKind.UNSUPPORTED_TOOL_CANDIDATE,
        ModelResponseActionSignalKind.FUNCTION_CALL_LIKE: ModelOutputActionCandidateKind.UNSUPPORTED_TOOL_CANDIDATE,
        ModelResponseActionSignalKind.SHELL_COMMAND_LIKE: ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE,
        ModelResponseActionSignalKind.FILE_WRITE_LIKE: ModelOutputActionCandidateKind.WORKSPACE_WRITE_CANDIDATE,
        ModelResponseActionSignalKind.CODE_EDIT_LIKE: ModelOutputActionCandidateKind.CODE_EDIT_CANDIDATE,
        ModelResponseActionSignalKind.PATCH_LIKE: ModelOutputActionCandidateKind.PATCH_CANDIDATE,
        ModelResponseActionSignalKind.DEPENDENCY_INSTALL_LIKE: ModelOutputActionCandidateKind.DEPENDENCY_INSTALL_CANDIDATE,
        ModelResponseActionSignalKind.PROVIDER_REINVOKE_LIKE: ModelOutputActionCandidateKind.PROVIDER_REINVOKE_CANDIDATE,
        ModelResponseActionSignalKind.NETWORK_ACCESS_LIKE: ModelOutputActionCandidateKind.NETWORK_ACCESS_CANDIDATE,
        ModelResponseActionSignalKind.CREDENTIAL_REQUEST_LIKE: ModelOutputActionCandidateKind.CREDENTIAL_ACCESS_CANDIDATE,
        ModelResponseActionSignalKind.EXTERNAL_HARNESS_EXECUTE_LIKE: ModelOutputActionCandidateKind.EXTERNAL_HARNESS_EXECUTION_CANDIDATE,
        ModelResponseActionSignalKind.REFERENCE_CODE_EXECUTE_LIKE: ModelOutputActionCandidateKind.REFERENCE_CODE_EXECUTION_CANDIDATE,
        ModelResponseActionSignalKind.BROWSER_RPA_GATEWAY_LIKE: ModelOutputActionCandidateKind.BROWSER_RPA_GATEWAY_CANDIDATE,
        ModelResponseActionSignalKind.AUTHORITY_GRANT_LIKE: ModelOutputActionCandidateKind.AUTHORITY_GRANT_CANDIDATE,
        ModelResponseActionSignalKind.UNKNOWN: ModelOutputActionCandidateKind.UNKNOWN,
    }
    return mapping[signal_kind]


def _risks_for_candidate_kind(candidate_kind: ModelOutputActionCandidateKind | str) -> list[ModelOutputActionRiskKind]:
    kind = ModelOutputActionCandidateKind(candidate_kind)
    mapping: dict[ModelOutputActionCandidateKind, list[ModelOutputActionRiskKind]] = {
        ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE: [ModelOutputActionRiskKind.MODEL_OUTPUT_AS_AUTHORITY_RISK],
        ModelOutputActionCandidateKind.ASK_USER_CANDIDATE: [],
        ModelOutputActionCandidateKind.NO_OP_CANDIDATE: [],
        ModelOutputActionCandidateKind.SAFE_WORKSPACE_INSPECTION_CANDIDATE: [ModelOutputActionRiskKind.UNSAFE_TOOL_EXECUTION_RISK],
        ModelOutputActionCandidateKind.SAFE_READONLY_TOOL_CANDIDATE: [ModelOutputActionRiskKind.UNSAFE_TOOL_EXECUTION_RISK],
        ModelOutputActionCandidateKind.UNSUPPORTED_TOOL_CANDIDATE: [ModelOutputActionRiskKind.UNSAFE_TOOL_EXECUTION_RISK],
        ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE: [ModelOutputActionRiskKind.SHELL_EXECUTION_RISK, ModelOutputActionRiskKind.COMMAND_EXECUTION_RISK],
        ModelOutputActionCandidateKind.COMMAND_EXECUTION_CANDIDATE: [ModelOutputActionRiskKind.COMMAND_EXECUTION_RISK],
        ModelOutputActionCandidateKind.WORKSPACE_WRITE_CANDIDATE: [ModelOutputActionRiskKind.WORKSPACE_WRITE_RISK],
        ModelOutputActionCandidateKind.CODE_EDIT_CANDIDATE: [ModelOutputActionRiskKind.CODE_EDIT_RISK],
        ModelOutputActionCandidateKind.PATCH_CANDIDATE: [ModelOutputActionRiskKind.PATCH_GENERATION_RISK],
        ModelOutputActionCandidateKind.PATCH_APPLICATION_CANDIDATE: [ModelOutputActionRiskKind.PATCH_APPLICATION_RISK],
        ModelOutputActionCandidateKind.DEPENDENCY_INSTALL_CANDIDATE: [ModelOutputActionRiskKind.DEPENDENCY_INSTALL_RISK],
        ModelOutputActionCandidateKind.PROVIDER_REINVOKE_CANDIDATE: [ModelOutputActionRiskKind.PROVIDER_REINVOKE_RISK],
        ModelOutputActionCandidateKind.NETWORK_ACCESS_CANDIDATE: [ModelOutputActionRiskKind.NETWORK_ACCESS_RISK],
        ModelOutputActionCandidateKind.CREDENTIAL_ACCESS_CANDIDATE: [ModelOutputActionRiskKind.CREDENTIAL_ACCESS_RISK],
        ModelOutputActionCandidateKind.SECRET_READ_CANDIDATE: [ModelOutputActionRiskKind.SECRET_READ_RISK],
        ModelOutputActionCandidateKind.EXTERNAL_HARNESS_EXECUTION_CANDIDATE: [ModelOutputActionRiskKind.EXTERNAL_HARNESS_EXECUTION_RISK],
        ModelOutputActionCandidateKind.OPENCODE_EXECUTION_CANDIDATE: [ModelOutputActionRiskKind.EXTERNAL_HARNESS_EXECUTION_RISK],
        ModelOutputActionCandidateKind.HERMES_EXECUTION_CANDIDATE: [ModelOutputActionRiskKind.EXTERNAL_HARNESS_EXECUTION_RISK],
        ModelOutputActionCandidateKind.OPENCLAW_EXECUTION_CANDIDATE: [ModelOutputActionRiskKind.EXTERNAL_HARNESS_EXECUTION_RISK],
        ModelOutputActionCandidateKind.REFERENCE_CODE_EXECUTION_CANDIDATE: [ModelOutputActionRiskKind.REFERENCE_CODE_EXECUTION_RISK],
        ModelOutputActionCandidateKind.BROWSER_RPA_GATEWAY_CANDIDATE: [ModelOutputActionRiskKind.BROWSER_RPA_GATEWAY_RISK],
        ModelOutputActionCandidateKind.AUTHORITY_GRANT_CANDIDATE: [ModelOutputActionRiskKind.AUTHORITY_GRANT_RISK],
        ModelOutputActionCandidateKind.UNKNOWN: [ModelOutputActionRiskKind.UNKNOWN],
    }
    return mapping[kind]


def _route_for_candidate_kind(candidate_kind: ModelOutputActionCandidateKind | str) -> ModelOutputActionRouteKind:
    kind = ModelOutputActionCandidateKind(candidate_kind)
    if kind == ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE:
        return ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE
    if kind == ModelOutputActionCandidateKind.ASK_USER_CANDIDATE:
        return ModelOutputActionRouteKind.ASK_USER_ROUTE
    if kind == ModelOutputActionCandidateKind.NO_OP_CANDIDATE:
        return ModelOutputActionRouteKind.NO_OP_ROUTE
    if kind == ModelOutputActionCandidateKind.SAFE_WORKSPACE_INSPECTION_CANDIDATE:
        return ModelOutputActionRouteKind.FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE
    if kind == ModelOutputActionCandidateKind.SAFE_READONLY_TOOL_CANDIDATE:
        return ModelOutputActionRouteKind.FUTURE_AGENT_STEP_RUNNER_ROUTE
    if kind == ModelOutputActionCandidateKind.PATCH_CANDIDATE:
        return ModelOutputActionRouteKind.FUTURE_PATCH_PROPOSAL_TRACK
    return ModelOutputActionRouteKind.BLOCKED_ROUTE


@dataclass(frozen=True)
class ModelOutputActionQuarantineFlagSet:
    flag_set_id: str
    version: str = V0345_VERSION
    action_quarantine_constructed: bool = False
    candidate_extraction_available: bool = False
    candidate_classification_available: bool = False
    quarantine_validation_available: bool = False
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_execution: bool = False
    ready_for_action_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0345(self.version)
        _validate_false(self, UNSAFE_QUARANTINE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.5")
        _validate_metadata_no_execution(self.metadata)


@dataclass(frozen=True)
class ModelOutputActionSourceRef:
    source_ref_id: str
    source_kind: ModelOutputActionSourceKind | str
    source_id: str
    source_summary: str
    trust_level: ModelOutputActionTrustLevel | str = ModelOutputActionTrustLevel.SANITIZED_BUT_UNTRUSTED
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ModelOutputActionSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        ModelOutputActionTrustLevel(self.trust_level)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionExtractionPolicy:
    extraction_policy_id: str
    max_candidate_count: int = DEFAULT_MAX_ACTION_CANDIDATE_COUNT
    max_candidate_preview_chars: int = DEFAULT_MAX_ACTION_CANDIDATE_PREVIEW_CHARS
    allow_final_response_candidate: bool = True
    allow_ask_user_candidate: bool = True
    allow_no_op_candidate: bool = True
    allow_safe_workspace_inspection_candidate: bool = True
    allow_patch_candidate: bool = False
    allow_command_candidate: bool = False
    allow_provider_reinvoke_candidate: bool = False
    allow_credential_candidate: bool = False
    allow_external_harness_candidate: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("extraction_policy_id", self.extraction_policy_id)
        _validate_non_negative("max_candidate_count", self.max_candidate_count)
        _validate_non_negative("max_candidate_preview_chars", self.max_candidate_preview_chars)
        _validate_false(self, ("allow_patch_candidate", "allow_command_candidate", "allow_provider_reinvoke_candidate", "allow_credential_candidate", "allow_external_harness_candidate"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionCandidate:
    candidate_id: str
    candidate_kind: ModelOutputActionCandidateKind | str
    source_signal_id: str | None
    source_response_envelope_id: str | None
    candidate_summary: str
    candidate_preview: str
    signal_strength: ModelOutputActionSignalStrength | str
    risk_kinds: list[ModelOutputActionRiskKind | str] = field(default_factory=list)
    proposed_route: ModelOutputActionRouteKind | str = ModelOutputActionRouteKind.BLOCKED_ROUTE
    source_refs: list[ModelOutputActionSourceRef] = field(default_factory=list)
    blocked_from_execution: bool = True
    requires_review: bool = False
    future_gated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_id", self.candidate_id)
        candidate_kind = ModelOutputActionCandidateKind(self.candidate_kind)
        _require_non_blank("candidate_summary", self.candidate_summary)
        if len(self.candidate_preview) > DEFAULT_MAX_ACTION_CANDIDATE_PREVIEW_CHARS:
            raise ValueError("candidate_preview must be bounded")
        ModelOutputActionSignalStrength(self.signal_strength)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelOutputActionRiskKind)
        ModelOutputActionRouteKind(self.proposed_route)
        _validate_object_list("source_refs", self.source_refs, ModelOutputActionSourceRef)
        if _is_unsafe_candidate_kind(candidate_kind) and self.blocked_from_execution is not True:
            raise ValueError("unsafe candidates must be blocked_from_execution in v0.34.5")
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionCandidateSet:
    candidate_set_id: str
    source_response_envelope_id: str | None
    candidates: list[ModelOutputActionCandidate]
    candidate_count: int
    blocked_candidate_count: int
    safe_route_candidate_count: int
    future_gated_candidate_count: int
    summary: str
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("candidate_set_id", self.candidate_set_id)
        _validate_object_list("candidates", self.candidates, ModelOutputActionCandidate)
        for name in ("candidate_count", "blocked_candidate_count", "safe_route_candidate_count", "future_gated_candidate_count"):
            _validate_non_negative(name, getattr(self, name))
        if self.candidate_count != len(self.candidates):
            raise ValueError("candidate_count must match candidates length")
        _require_non_blank("summary", self.summary)
        _validate_metadata_no_execution(self.metadata)

    @property
    def action_queue(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionRiskAssessment:
    risk_assessment_id: str
    candidate_id: str
    risk_kinds: list[ModelOutputActionRiskKind | str]
    severity: str
    summary: str
    must_block: bool
    requires_review: bool = False
    future_track: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_assessment_id", self.risk_assessment_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelOutputActionRiskKind)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        high_risk = any(ModelOutputActionRiskKind(risk).value not in {"model_output_as_authority_risk"} for risk in self.risk_kinds)
        if high_risk and self.must_block is not True:
            raise ValueError("high-risk candidates must have must_block True")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)

    @property
    def remediation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionRoutePolicy:
    route_policy_id: str
    allowed_routes: list[ModelOutputActionRouteKind | str] = field(default_factory=list)
    blocked_routes: list[ModelOutputActionRouteKind | str] = field(default_factory=list)
    future_gated_routes: list[ModelOutputActionRouteKind | str] = field(default_factory=list)
    prohibited_candidate_kinds: list[ModelOutputActionCandidateKind | str] = field(default_factory=list)
    allow_final_response_route: bool = True
    allow_ask_user_route: bool = True
    allow_no_op_route: bool = True
    allow_future_safe_workspace_inspection_route: bool = True
    allow_future_agent_step_runner_route: bool = True
    allow_patch_proposal_route: bool = False
    allow_action_execution: bool = False
    allow_tool_execution: bool = False
    allow_workspace_write: bool = False
    allow_command_execution: bool = False
    allow_provider_reinvoke: bool = False
    allow_credential_access: bool = False
    allow_external_harness_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("route_policy_id", self.route_policy_id)
        _validate_enum_list("allowed_routes", self.allowed_routes, ModelOutputActionRouteKind)
        _validate_enum_list("blocked_routes", self.blocked_routes, ModelOutputActionRouteKind)
        _validate_enum_list("future_gated_routes", self.future_gated_routes, ModelOutputActionRouteKind)
        _validate_enum_list("prohibited_candidate_kinds", self.prohibited_candidate_kinds, ModelOutputActionCandidateKind)
        _validate_false(
            self,
            (
                "allow_patch_proposal_route",
                "allow_action_execution",
                "allow_tool_execution",
                "allow_workspace_write",
                "allow_command_execution",
                "allow_provider_reinvoke",
                "allow_credential_access",
                "allow_external_harness_execution",
            ),
        )
        _validate_metadata_no_execution(self.metadata)


@dataclass(frozen=True)
class ModelOutputActionQuarantineDecision:
    decision_id: str
    candidate_id: str
    decision_kind: ModelOutputActionDecisionKind | str
    route_kind: ModelOutputActionRouteKind | str
    reason: str
    risk_kinds: list[ModelOutputActionRiskKind | str] = field(default_factory=list)
    allowed_as_non_executing_route: bool = False
    allowed_for_future_handoff: bool = False
    action_execution_allowed: bool = False
    tool_execution_allowed: bool = False
    workspace_write_allowed: bool = False
    command_execution_allowed: bool = False
    provider_invocation_allowed: bool = False
    credential_access_allowed: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("candidate_id", self.candidate_id)
        decision_kind = ModelOutputActionDecisionKind(self.decision_kind)
        route_kind = ModelOutputActionRouteKind(self.route_kind)
        _require_non_blank("reason", self.reason)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelOutputActionRiskKind)
        if self.allowed_as_non_executing_route and route_kind not in {ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE, ModelOutputActionRouteKind.ASK_USER_ROUTE, ModelOutputActionRouteKind.NO_OP_ROUTE}:
            raise ValueError("allowed_as_non_executing_route is only for final/ask/no-op routes")
        if self.allowed_for_future_handoff and route_kind not in {ModelOutputActionRouteKind.FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE, ModelOutputActionRouteKind.FUTURE_AGENT_STEP_RUNNER_ROUTE, ModelOutputActionRouteKind.FUTURE_GATE_ROUTE}:
            raise ValueError("allowed_for_future_handoff is only for future non-executing routes")
        if decision_kind == ModelOutputActionDecisionKind.BLOCK_UNSAFE_CANDIDATE and route_kind != ModelOutputActionRouteKind.BLOCKED_ROUTE:
            raise ValueError("blocked unsafe candidates must use blocked_route")
        _validate_false(self, ("action_execution_allowed", "tool_execution_allowed", "workspace_write_allowed", "command_execution_allowed", "provider_invocation_allowed", "credential_access_allowed"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionBlockedRecord:
    blocked_record_id: str
    candidate_id: str
    decision_id: str | None
    blocked_candidate_kind: ModelOutputActionCandidateKind | str
    risk_kinds: list[ModelOutputActionRiskKind | str]
    reason: str
    safe_alternatives: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("blocked_record_id", self.blocked_record_id)
        _require_non_blank("candidate_id", self.candidate_id)
        ModelOutputActionCandidateKind(self.blocked_candidate_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelOutputActionRiskKind)
        _require_non_blank("reason", self.reason)
        _validate_string_list("safe_alternatives", self.safe_alternatives)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)

    @property
    def safe_outcome(self) -> bool:
        return True

    @property
    def remediation_execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionSafeRoute:
    safe_route_id: str
    candidate_id: str
    decision_id: str
    route_kind: ModelOutputActionRouteKind | str
    route_summary: str
    handoff_target_version: str | None
    non_executing: bool = True
    future_handoff_only: bool = False
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("safe_route_id", self.safe_route_id)
        _require_non_blank("candidate_id", self.candidate_id)
        _require_non_blank("decision_id", self.decision_id)
        route_kind = ModelOutputActionRouteKind(self.route_kind)
        _require_non_blank("route_summary", self.route_summary)
        if self.non_executing is not True:
            raise ValueError("safe routes must be non_executing in v0.34.5")
        if route_kind in {ModelOutputActionRouteKind.FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE, ModelOutputActionRouteKind.FUTURE_AGENT_STEP_RUNNER_ROUTE, ModelOutputActionRouteKind.FUTURE_GATE_ROUTE} and self.future_handoff_only is not True:
            raise ValueError("future routes must be future_handoff_only")
        _validate_false(self, ("ready_for_execution",))
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionQuarantinePacket:
    quarantine_packet_id: str
    version: str
    source_response_envelope_id: str | None
    candidate_set: ModelOutputActionCandidateSet
    decisions: list[ModelOutputActionQuarantineDecision]
    blocked_records: list[ModelOutputActionBlockedRecord]
    safe_routes: list[ModelOutputActionSafeRoute]
    status: ModelOutputActionQuarantineStatus | str
    summary: str
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("quarantine_packet_id", self.quarantine_packet_id)
        _validate_version_includes_v0345(self.version)
        if not isinstance(self.candidate_set, ModelOutputActionCandidateSet):
            raise TypeError("candidate_set must be ModelOutputActionCandidateSet")
        _validate_object_list("decisions", self.decisions, ModelOutputActionQuarantineDecision)
        _validate_object_list("blocked_records", self.blocked_records, ModelOutputActionBlockedRecord)
        _validate_object_list("safe_routes", self.safe_routes, ModelOutputActionSafeRoute)
        ModelOutputActionQuarantineStatus(self.status)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_action_execution", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def action_queue(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionQuarantineValidationReport:
    validation_report_id: str
    version: str
    quarantine_packet_id: str | None
    checked_candidate_ids: list[str]
    blocked_candidate_ids: list[str]
    safe_route_ids: list[str]
    validation_passed: bool
    action_execution_blocked: bool
    tool_execution_blocked: bool
    workspace_write_blocked: bool
    command_execution_blocked: bool
    provider_invocation_blocked: bool
    credential_access_blocked: bool
    warnings: list[str]
    summary: str
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version_includes_v0345(self.version)
        for name in ("checked_candidate_ids", "blocked_candidate_ids", "safe_route_ids", "warnings"):
            _validate_string_list(name, getattr(self, name))
        _validate_true(self, ("action_execution_blocked", "tool_execution_blocked", "workspace_write_blocked", "command_execution_blocked", "provider_invocation_blocked", "credential_access_blocked"))
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_action_execution", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionQuarantineReport:
    report_id: str
    version: str
    quarantine_packet_id: str | None
    validation_report_id: str | None
    status: ModelOutputActionQuarantineStatus | str
    readiness_level: ModelOutputActionReadinessLevel | str
    summary: str
    candidate_count: int = 0
    blocked_candidate_count: int = 0
    safe_route_count: int = 0
    future_gated_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_QUARANTINE_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0345(self.version)
        ModelOutputActionQuarantineStatus(self.status)
        ModelOutputActionReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("candidate_count", "blocked_candidate_count", "safe_route_count", "future_gated_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_action_execution", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionQuarantineRunPreview:
    run_preview_id: str
    quarantine_packet_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["extract action-like candidates", "assess risk", "create quarantine decisions"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["ModelOutputActionCandidateSet", "ModelOutputActionQuarantinePacket", "V0345ReadinessReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_QUARANTINE_PROHIBITED_UNTIL_LATER_GATE))
    no_action_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_proposal_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_existing_boundary_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_dependency_install_guarantee: bool = True
    no_raw_response_persistence_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.5")
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelOutputActionNoExecutionGuarantee:
    guarantee_id: str
    version: str = V0345_VERSION
    no_action_execution: bool = True
    no_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_proposal: bool = True
    no_patch_application: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_provider_invocation: bool = True
    no_existing_boundary_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_agent_step_execution: bool = True
    no_general_agent_execution: bool = True
    no_autonomous_agent_runtime: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_raw_response_persistence: bool = True
    no_raw_model_output_persistence: bool = True
    no_persistent_trace_write: bool = True
    no_external_trace_sink: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0345(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.5")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)


@dataclass(frozen=True)
class V0345ReadinessReport:
    report_id: str
    version: str
    quarantine_packet_id: str | None
    quarantine_report_id: str | None
    validation_report_id: str | None
    summary: str
    ready_for_v0346_agent_step_runner_model_integration: bool = False
    ready_for_v0347_model_invocation_ocel_trace_packet: bool = False
    ready_for_execution: bool = False
    ready_for_action_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_safe_workspace_inspection_execution: bool = False
    ready_for_patch_proposal: bool = False
    ready_for_patch_application: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_QUARANTINE_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_QUARANTINE_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0345(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_QUARANTINE_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            ["action execution", "tool execution", "workspace inspection execution", "workspace write", "code edit", "patch proposal", "patch application", "shell", "subprocess", "command", "provider invocation", "existing boundary invocation", "network access", "credential access", "secret read", "agent step execution", "general agent execution", "autonomous loop", "reference code execution", "reference import", "dependency install", "raw response persistence", "raw model output persistence", "persistent trace write", "external trace sink", "UI runtime", "external control", "authority grant"],
        )
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution_readiness(self) -> bool:
        return False


def build_model_output_action_flags(flag_set_id: str = "model_output_action_quarantine_flags:v0.34.5", **kwargs: Any) -> ModelOutputActionQuarantineFlagSet:
    return ModelOutputActionQuarantineFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0345_VERSION),
        action_quarantine_constructed=kwargs.pop("action_quarantine_constructed", True),
        candidate_extraction_available=kwargs.pop("candidate_extraction_available", True),
        candidate_classification_available=kwargs.pop("candidate_classification_available", True),
        quarantine_validation_available=kwargs.pop("quarantine_validation_available", True),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_v0347_model_invocation_ocel_trace_packet=kwargs.pop("ready_for_v0347_model_invocation_ocel_trace_packet", True),
        **kwargs,
    )


def build_model_output_action_source_ref(
    source_ref_id: str,
    source_kind: ModelOutputActionSourceKind | str = ModelOutputActionSourceKind.V0343_MODEL_RESPONSE_ACTION_SIGNAL,
    source_id: str = "model_output_action_source",
    source_summary: str = "Model output action source ref only; no fetch/read/execute.",
    **kwargs: Any,
) -> ModelOutputActionSourceRef:
    return ModelOutputActionSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_model_output_action_extraction_policy(
    extraction_policy_id: str = "model_output_action_extraction_policy:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionExtractionPolicy:
    return ModelOutputActionExtractionPolicy(extraction_policy_id=extraction_policy_id, **kwargs)


def default_model_output_action_extraction_policy(**kwargs: Any) -> ModelOutputActionExtractionPolicy:
    return build_model_output_action_extraction_policy(**kwargs)


def build_model_output_action_candidate(candidate_id: str = "model_output_action_candidate:v0.34.5", **kwargs: Any) -> ModelOutputActionCandidate:
    candidate_kind = kwargs.pop("candidate_kind", ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE)
    candidate_kind_enum = ModelOutputActionCandidateKind(candidate_kind)
    return ModelOutputActionCandidate(
        candidate_id=candidate_id,
        candidate_kind=candidate_kind_enum,
        source_signal_id=kwargs.pop("source_signal_id", None),
        source_response_envelope_id=kwargs.pop("source_response_envelope_id", None),
        candidate_summary=kwargs.pop("candidate_summary", "Model output action candidate metadata only."),
        candidate_preview=kwargs.pop("candidate_preview", "bounded candidate preview"),
        signal_strength=kwargs.pop("signal_strength", ModelOutputActionSignalStrength.MODERATE),
        risk_kinds=kwargs.pop("risk_kinds", _risks_for_candidate_kind(candidate_kind_enum)),
        proposed_route=kwargs.pop("proposed_route", _route_for_candidate_kind(candidate_kind_enum)),
        blocked_from_execution=kwargs.pop("blocked_from_execution", _is_unsafe_candidate_kind(candidate_kind_enum)),
        requires_review=kwargs.pop("requires_review", candidate_kind_enum == ModelOutputActionCandidateKind.UNKNOWN),
        future_gated=kwargs.pop("future_gated", _is_future_route_candidate_kind(candidate_kind_enum) or candidate_kind_enum == ModelOutputActionCandidateKind.PATCH_CANDIDATE),
        **kwargs,
    )


def build_model_output_action_candidate_set(
    candidate_set_id: str = "model_output_action_candidate_set:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionCandidateSet:
    candidates = kwargs.pop("candidates", [])
    return ModelOutputActionCandidateSet(
        candidate_set_id=candidate_set_id,
        source_response_envelope_id=kwargs.pop("source_response_envelope_id", None),
        candidates=candidates,
        candidate_count=kwargs.pop("candidate_count", len(candidates)),
        blocked_candidate_count=kwargs.pop("blocked_candidate_count", sum(1 for candidate in candidates if candidate.blocked_from_execution)),
        safe_route_candidate_count=kwargs.pop("safe_route_candidate_count", sum(1 for candidate in candidates if _is_non_executing_allowed_candidate_kind(candidate.candidate_kind))),
        future_gated_candidate_count=kwargs.pop("future_gated_candidate_count", sum(1 for candidate in candidates if candidate.future_gated)),
        summary=kwargs.pop("summary", "Model output action candidate set; not action queue."),
        **kwargs,
    )


def build_model_output_action_risk_assessment(
    risk_assessment_id: str = "model_output_action_risk_assessment:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionRiskAssessment:
    risk_kinds = kwargs.pop("risk_kinds", [])
    return ModelOutputActionRiskAssessment(
        risk_assessment_id=risk_assessment_id,
        candidate_id=kwargs.pop("candidate_id", "model_output_action_candidate:v0.34.5"),
        risk_kinds=risk_kinds,
        severity=kwargs.pop("severity", "high" if risk_kinds else "low"),
        summary=kwargs.pop("summary", "Model output action risk assessment; no remediation execution."),
        must_block=kwargs.pop("must_block", any(ModelOutputActionRiskKind(risk).value not in {"model_output_as_authority_risk"} for risk in risk_kinds)),
        **kwargs,
    )


def build_model_output_action_route_policy(route_policy_id: str = "model_output_action_route_policy:v0.34.5", **kwargs: Any) -> ModelOutputActionRoutePolicy:
    return ModelOutputActionRoutePolicy(
        route_policy_id=route_policy_id,
        allowed_routes=kwargs.pop("allowed_routes", [ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE, ModelOutputActionRouteKind.ASK_USER_ROUTE, ModelOutputActionRouteKind.NO_OP_ROUTE]),
        blocked_routes=kwargs.pop("blocked_routes", [ModelOutputActionRouteKind.BLOCKED_ROUTE]),
        future_gated_routes=kwargs.pop("future_gated_routes", [ModelOutputActionRouteKind.FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE, ModelOutputActionRouteKind.FUTURE_AGENT_STEP_RUNNER_ROUTE, ModelOutputActionRouteKind.FUTURE_PATCH_PROPOSAL_TRACK]),
        prohibited_candidate_kinds=kwargs.pop("prohibited_candidate_kinds", [ModelOutputActionCandidateKind.SHELL_COMMAND_CANDIDATE, ModelOutputActionCandidateKind.PATCH_CANDIDATE, ModelOutputActionCandidateKind.PROVIDER_REINVOKE_CANDIDATE, ModelOutputActionCandidateKind.CREDENTIAL_ACCESS_CANDIDATE, ModelOutputActionCandidateKind.EXTERNAL_HARNESS_EXECUTION_CANDIDATE]),
        **kwargs,
    )


def default_model_output_action_route_policy(**kwargs: Any) -> ModelOutputActionRoutePolicy:
    return build_model_output_action_route_policy(**kwargs)


def build_model_output_action_quarantine_decision(
    decision_id: str = "model_output_action_quarantine_decision:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionQuarantineDecision:
    return ModelOutputActionQuarantineDecision(
        decision_id=decision_id,
        candidate_id=kwargs.pop("candidate_id", "model_output_action_candidate:v0.34.5"),
        decision_kind=kwargs.pop("decision_kind", ModelOutputActionDecisionKind.ALLOW_NON_EXECUTING_FINAL_RESPONSE),
        route_kind=kwargs.pop("route_kind", ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE),
        reason=kwargs.pop("reason", "Allowed only as non-executing route metadata."),
        allowed_as_non_executing_route=kwargs.pop("allowed_as_non_executing_route", True),
        **kwargs,
    )


def build_model_output_action_blocked_record(
    blocked_record_id: str = "model_output_action_blocked_record:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionBlockedRecord:
    return ModelOutputActionBlockedRecord(
        blocked_record_id=blocked_record_id,
        candidate_id=kwargs.pop("candidate_id", "model_output_action_candidate:v0.34.5"),
        decision_id=kwargs.pop("decision_id", None),
        blocked_candidate_kind=kwargs.pop("blocked_candidate_kind", ModelOutputActionCandidateKind.UNKNOWN),
        risk_kinds=kwargs.pop("risk_kinds", [ModelOutputActionRiskKind.UNKNOWN]),
        reason=kwargs.pop("reason", "Unsafe model-output candidate blocked by quarantine."),
        safe_alternatives=kwargs.pop("safe_alternatives", ["final response", "ask user", "no-op"]),
        **kwargs,
    )


def build_model_output_action_safe_route(
    safe_route_id: str = "model_output_action_safe_route:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionSafeRoute:
    return ModelOutputActionSafeRoute(
        safe_route_id=safe_route_id,
        candidate_id=kwargs.pop("candidate_id", "model_output_action_candidate:v0.34.5"),
        decision_id=kwargs.pop("decision_id", "model_output_action_quarantine_decision:v0.34.5"),
        route_kind=kwargs.pop("route_kind", ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE),
        route_summary=kwargs.pop("route_summary", "Safe route metadata only; non-executing."),
        handoff_target_version=kwargs.pop("handoff_target_version", None),
        **kwargs,
    )


def assess_model_output_action_candidate_risk(
    candidate: ModelOutputActionCandidate,
    policy: ModelOutputActionRoutePolicy | None = None,
) -> ModelOutputActionRiskAssessment:
    if not isinstance(candidate, ModelOutputActionCandidate):
        raise TypeError("candidate must be ModelOutputActionCandidate")
    policy = policy or default_model_output_action_route_policy()
    must_block = candidate.blocked_from_execution or ModelOutputActionCandidateKind(candidate.candidate_kind) in policy.prohibited_candidate_kinds
    return build_model_output_action_risk_assessment(
        risk_assessment_id=f"risk_assessment:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        risk_kinds=candidate.risk_kinds,
        severity="high" if must_block else "low",
        must_block=must_block,
        requires_review=candidate.requires_review,
        future_track=candidate.future_gated,
        summary="Candidate risk assessed without executing or remediating model output.",
    )


def decide_model_output_action_route(
    candidate: ModelOutputActionCandidate,
    route_policy: ModelOutputActionRoutePolicy | None = None,
) -> ModelOutputActionQuarantineDecision:
    if not isinstance(candidate, ModelOutputActionCandidate):
        raise TypeError("candidate must be ModelOutputActionCandidate")
    route_policy = route_policy or default_model_output_action_route_policy()
    candidate_kind = ModelOutputActionCandidateKind(candidate.candidate_kind)
    route_kind = ModelOutputActionRouteKind(candidate.proposed_route)
    if _is_non_executing_allowed_candidate_kind(candidate_kind):
        decision_map = {
            ModelOutputActionRouteKind.FINAL_RESPONSE_ROUTE: ModelOutputActionDecisionKind.ALLOW_NON_EXECUTING_FINAL_RESPONSE,
            ModelOutputActionRouteKind.ASK_USER_ROUTE: ModelOutputActionDecisionKind.ALLOW_NON_EXECUTING_ASK_USER,
            ModelOutputActionRouteKind.NO_OP_ROUTE: ModelOutputActionDecisionKind.ALLOW_NON_EXECUTING_NO_OP,
        }
        return build_model_output_action_quarantine_decision(
            decision_id=f"decision:{candidate.candidate_id}",
            candidate_id=candidate.candidate_id,
            decision_kind=decision_map.get(route_kind, ModelOutputActionDecisionKind.NO_OP),
            route_kind=route_kind,
            risk_kinds=candidate.risk_kinds,
            allowed_as_non_executing_route=True,
            reason="Candidate allowed only as non-executing output route.",
        )
    if _is_future_route_candidate_kind(candidate_kind):
        return build_model_output_action_quarantine_decision(
            decision_id=f"decision:{candidate.candidate_id}",
            candidate_id=candidate.candidate_id,
            decision_kind=ModelOutputActionDecisionKind.ALLOW_FUTURE_SAFE_WORKSPACE_INSPECTION_ROUTE,
            route_kind=route_kind,
            risk_kinds=candidate.risk_kinds,
            allowed_as_non_executing_route=False,
            allowed_for_future_handoff=True,
            reason="Candidate marked only for future non-executing handoff.",
        )
    return build_model_output_action_quarantine_decision(
        decision_id=f"decision:{candidate.candidate_id}",
        candidate_id=candidate.candidate_id,
        decision_kind=ModelOutputActionDecisionKind.BLOCK_UNSAFE_CANDIDATE,
        route_kind=ModelOutputActionRouteKind.BLOCKED_ROUTE,
        risk_kinds=candidate.risk_kinds,
        allowed_as_non_executing_route=False,
        allowed_for_future_handoff=False,
        reason="Unsafe model-output candidate blocked from execution.",
    )


def _candidate_from_signal(signal: ModelResponseActionSignal, index: int, source_response_envelope_id: str | None = None) -> ModelOutputActionCandidate:
    candidate_kind = _candidate_kind_from_action_signal(signal)
    preview, _ = _bounded(signal.extracted_preview, DEFAULT_MAX_ACTION_CANDIDATE_PREVIEW_CHARS)
    return build_model_output_action_candidate(
        candidate_id=f"candidate:{signal.action_signal_id}:{index}",
        candidate_kind=candidate_kind,
        source_signal_id=signal.action_signal_id,
        source_response_envelope_id=source_response_envelope_id,
        candidate_summary=signal.signal_summary,
        candidate_preview=preview,
        signal_strength=ModelOutputActionSignalStrength.EXPLICIT if signal.blocked_from_execution else ModelOutputActionSignalStrength.MODERATE,
    )


def extract_model_output_action_candidates_from_action_signals(
    action_signals: list[ModelResponseActionSignal],
    source_response_envelope_id: str | None = None,
    extraction_policy: ModelOutputActionExtractionPolicy | None = None,
) -> list[ModelOutputActionCandidate]:
    if not isinstance(action_signals, list):
        raise TypeError("action_signals must be list")
    _validate_object_list("action_signals", action_signals, ModelResponseActionSignal)
    policy = extraction_policy or default_model_output_action_extraction_policy()
    return [_candidate_from_signal(signal, index, source_response_envelope_id) for index, signal in enumerate(action_signals[: policy.max_candidate_count])]


def extract_model_output_action_candidates_from_response_envelope(
    response_envelope: ModelResponseEnvelope,
    extraction_policy: ModelOutputActionExtractionPolicy | None = None,
) -> ModelOutputActionCandidateSet:
    if not isinstance(response_envelope, ModelResponseEnvelope):
        raise TypeError("response_envelope must be ModelResponseEnvelope")
    candidates = extract_model_output_action_candidates_from_action_signals(
        response_envelope.sanitized_payload.action_signals,
        source_response_envelope_id=response_envelope.response_envelope_id,
        extraction_policy=extraction_policy,
    )
    if not candidates and response_envelope.sanitized_payload.response_preview:
        candidates = [
            build_model_output_action_candidate(
                candidate_id=f"candidate:final_response:{response_envelope.response_envelope_id}",
                candidate_kind=ModelOutputActionCandidateKind.FINAL_RESPONSE_CANDIDATE,
                source_response_envelope_id=response_envelope.response_envelope_id,
                candidate_summary="Sanitized response can be routed only as non-executing final response.",
                candidate_preview=response_envelope.sanitized_payload.response_preview,
                blocked_from_execution=False,
            )
        ]
    return build_model_output_action_candidate_set(
        source_response_envelope_id=response_envelope.response_envelope_id,
        candidates=candidates,
    )


def build_model_output_action_quarantine_packet(
    quarantine_packet_id: str = "model_output_action_quarantine_packet:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionQuarantinePacket:
    return ModelOutputActionQuarantinePacket(
        quarantine_packet_id=quarantine_packet_id,
        version=kwargs.pop("version", V0345_VERSION),
        source_response_envelope_id=kwargs.pop("source_response_envelope_id", None),
        candidate_set=kwargs.pop("candidate_set", build_model_output_action_candidate_set()),
        decisions=kwargs.pop("decisions", []),
        blocked_records=kwargs.pop("blocked_records", []),
        safe_routes=kwargs.pop("safe_routes", []),
        status=kwargs.pop("status", ModelOutputActionQuarantineStatus.QUARANTINED),
        summary=kwargs.pop("summary", "Model output action quarantine packet; not action queue."),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_v0347_model_invocation_ocel_trace_packet=kwargs.pop("ready_for_v0347_model_invocation_ocel_trace_packet", True),
        **kwargs,
    )


def build_model_output_action_quarantine_packet_from_candidates(
    candidates: list[ModelOutputActionCandidate],
    route_policy: ModelOutputActionRoutePolicy | None = None,
    **kwargs: Any,
) -> ModelOutputActionQuarantinePacket:
    route_policy = route_policy or default_model_output_action_route_policy()
    decisions = [decide_model_output_action_route(candidate, route_policy) for candidate in candidates]
    blocked_records = [
        build_model_output_action_blocked_record(
            blocked_record_id=f"blocked:{candidate.candidate_id}",
            candidate_id=candidate.candidate_id,
            decision_id=decision.decision_id,
            blocked_candidate_kind=candidate.candidate_kind,
            risk_kinds=candidate.risk_kinds or [ModelOutputActionRiskKind.UNKNOWN],
            reason=decision.reason,
        )
        for candidate, decision in zip(candidates, decisions)
        if decision.route_kind == ModelOutputActionRouteKind.BLOCKED_ROUTE
    ]
    safe_routes = [
        build_model_output_action_safe_route(
            safe_route_id=f"safe_route:{candidate.candidate_id}",
            candidate_id=candidate.candidate_id,
            decision_id=decision.decision_id,
            route_kind=decision.route_kind,
            route_summary=decision.reason,
            handoff_target_version="v0.34.6" if decision.allowed_for_future_handoff else None,
            future_handoff_only=decision.allowed_for_future_handoff,
            ready_for_v0346_agent_step_runner_model_integration=decision.allowed_for_future_handoff,
        )
        for candidate, decision in zip(candidates, decisions)
        if decision.allowed_as_non_executing_route or decision.allowed_for_future_handoff
    ]
    return build_model_output_action_quarantine_packet(
        candidate_set=build_model_output_action_candidate_set(candidates=candidates),
        decisions=decisions,
        blocked_records=blocked_records,
        safe_routes=safe_routes,
        **kwargs,
    )


def build_model_output_action_quarantine_validation_report(
    validation_report_id: str = "model_output_action_quarantine_validation_report:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionQuarantineValidationReport:
    return ModelOutputActionQuarantineValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0345_VERSION),
        quarantine_packet_id=kwargs.pop("quarantine_packet_id", None),
        checked_candidate_ids=kwargs.pop("checked_candidate_ids", []),
        blocked_candidate_ids=kwargs.pop("blocked_candidate_ids", []),
        safe_route_ids=kwargs.pop("safe_route_ids", []),
        validation_passed=kwargs.pop("validation_passed", True),
        action_execution_blocked=kwargs.pop("action_execution_blocked", True),
        tool_execution_blocked=kwargs.pop("tool_execution_blocked", True),
        workspace_write_blocked=kwargs.pop("workspace_write_blocked", True),
        command_execution_blocked=kwargs.pop("command_execution_blocked", True),
        provider_invocation_blocked=kwargs.pop("provider_invocation_blocked", True),
        credential_access_blocked=kwargs.pop("credential_access_blocked", True),
        warnings=kwargs.pop("warnings", []),
        summary=kwargs.pop("summary", "Model output action quarantine validation report; not execution certification."),
        **kwargs,
    )


def validate_model_output_action_quarantine_packet(
    packet: ModelOutputActionQuarantinePacket,
    route_policy: ModelOutputActionRoutePolicy | None = None,
) -> ModelOutputActionQuarantineValidationReport:
    if not isinstance(packet, ModelOutputActionQuarantinePacket):
        raise TypeError("packet must be ModelOutputActionQuarantinePacket")
    route_policy = route_policy or default_model_output_action_route_policy()
    checked_candidate_ids = [candidate.candidate_id for candidate in packet.candidate_set.candidates]
    blocked_candidate_ids = [record.candidate_id for record in packet.blocked_records]
    safe_route_ids = [route.safe_route_id for route in packet.safe_routes]
    warnings: list[str] = []
    if any(decision.action_execution_allowed or decision.tool_execution_allowed or decision.workspace_write_allowed or decision.command_execution_allowed or decision.provider_invocation_allowed or decision.credential_access_allowed for decision in packet.decisions):
        warnings.append("A decision attempted unsafe execution permission.")
    if route_policy.allow_action_execution or route_policy.allow_tool_execution:
        warnings.append("Route policy attempted unsafe execution permission.")
    return build_model_output_action_quarantine_validation_report(
        quarantine_packet_id=packet.quarantine_packet_id,
        checked_candidate_ids=checked_candidate_ids,
        blocked_candidate_ids=blocked_candidate_ids,
        safe_route_ids=safe_route_ids,
        validation_passed=not warnings,
        warnings=warnings,
        summary="Model output action quarantine packet validated as non-executing metadata.",
    )


def build_model_output_action_quarantine_report(
    report_id: str = "model_output_action_quarantine_report:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionQuarantineReport:
    return ModelOutputActionQuarantineReport(
        report_id=report_id,
        version=kwargs.pop("version", V0345_VERSION),
        quarantine_packet_id=kwargs.pop("quarantine_packet_id", None),
        validation_report_id=kwargs.pop("validation_report_id", None),
        status=kwargs.pop("status", ModelOutputActionQuarantineStatus.QUARANTINED),
        readiness_level=kwargs.pop("readiness_level", ModelOutputActionReadinessLevel.QUARANTINE_VALIDATION_READY),
        summary=kwargs.pop("summary", "Model output action quarantine report; no action execution."),
        candidate_count=kwargs.pop("candidate_count", 0),
        blocked_candidate_count=kwargs.pop("blocked_candidate_count", 0),
        safe_route_count=kwargs.pop("safe_route_count", 0),
        future_gated_count=kwargs.pop("future_gated_count", 0),
        completed_items=kwargs.pop("completed_items", ["candidate extraction", "risk assessment", "quarantine decisions"]),
        future_track_items=kwargs.pop("future_track_items", ["agent step runner model integration", "model invocation OCEL trace packet"]),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_v0347_model_invocation_ocel_trace_packet=kwargs.pop("ready_for_v0347_model_invocation_ocel_trace_packet", True),
        **kwargs,
    )


def build_model_output_action_quarantine_run_preview(
    run_preview_id: str = "model_output_action_quarantine_run_preview:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionQuarantineRunPreview:
    return ModelOutputActionQuarantineRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_model_output_action_no_execution_guarantee(
    guarantee_id: str = "model_output_action_no_execution_guarantee:v0.34.5",
    **kwargs: Any,
) -> ModelOutputActionNoExecutionGuarantee:
    return ModelOutputActionNoExecutionGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0345_VERSION), **kwargs)


def build_v0345_readiness_report(report_id: str = "v0345_readiness_report", **kwargs: Any) -> V0345ReadinessReport:
    return V0345ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0345_VERSION),
        quarantine_packet_id=kwargs.pop("quarantine_packet_id", "model_output_action_quarantine_packet:v0.34.5"),
        quarantine_report_id=kwargs.pop("quarantine_report_id", "model_output_action_quarantine_report:v0.34.5"),
        validation_report_id=kwargs.pop("validation_report_id", "model_output_action_quarantine_validation_report:v0.34.5"),
        summary=kwargs.pop("summary", "v0.34.5 defines model output action quarantine metadata only; no execution readiness."),
        ready_for_v0346_agent_step_runner_model_integration=kwargs.pop("ready_for_v0346_agent_step_runner_model_integration", True),
        ready_for_v0347_model_invocation_ocel_trace_packet=kwargs.pop("ready_for_v0347_model_invocation_ocel_trace_packet", True),
        completed_items=kwargs.pop("completed_items", ["candidate extraction", "risk assessment", "route decisions", "blocked records", "safe routes"]),
        future_track_items=kwargs.pop("future_track_items", ["agent step runner model integration", "model invocation OCEL trace packet"]),
        **kwargs,
    )


def model_output_action_flags_preserve_execution_false(flags: ModelOutputActionQuarantineFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_QUARANTINE_FLAG_NAMES) and flags.production_certified is False


def model_output_action_candidate_is_not_execution(candidate: ModelOutputActionCandidate) -> bool:
    return candidate.execution is False and (not _is_unsafe_candidate_kind(candidate.candidate_kind) or candidate.blocked_from_execution is True)


def model_output_action_decision_is_not_execution(decision: ModelOutputActionQuarantineDecision) -> bool:
    return (
        decision.execution_permission is False
        and decision.action_execution_allowed is False
        and decision.tool_execution_allowed is False
        and decision.workspace_write_allowed is False
        and decision.command_execution_allowed is False
        and decision.provider_invocation_allowed is False
        and decision.credential_access_allowed is False
    )


def model_output_action_safe_route_is_not_execution(route: ModelOutputActionSafeRoute) -> bool:
    return route.execution is False and route.non_executing is True and route.ready_for_execution is False


def v0345_readiness_report_is_not_execution_ready(report: V0345ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_QUARANTINE_FLAG_NAMES) and report.execution_readiness is False
