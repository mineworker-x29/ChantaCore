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
from .model_backed_step import ModelBackedStepExecutionRecord, ModelBackedStepOutput, ModelBackedStepStatus
from .model_output_quarantine import (
    ModelOutputActionCandidate,
    ModelOutputActionQuarantineDecision,
    ModelOutputActionQuarantinePacket,
    ModelOutputActionRouteKind,
    ModelOutputActionSafeRoute,
)
from .provider_adapter import ExistingProviderBoundaryInvocationResult, ExistingProviderBoundaryOutcomeKind


V0347_VERSION = "v0.34.7"
V0347_RELEASE_NAME = "v0.34.7 Model Invocation OCEL Trace Packet"

DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS = [
    ".env",
    "secret",
    "key",
    "api_key",
    "token",
    "credential",
    "bearer ",
    "pem",
    "id_rsa",
    "raw prompt",
    "raw response",
    "raw model output",
]

DEFAULT_MODEL_INVOCATION_PROHIBITED_TRACE_CONTENT = [
    "raw prompt",
    "raw response",
    "raw model output",
    "file content",
    "secrets",
    "credentials",
    "tokens",
    "unbounded output",
]

DEFAULT_V0347_PROHIBITED_UNTIL_LATER_GATE = [
    "provider invocation",
    "existing boundary invocation",
    "agent step execution",
    "tool execution",
    "workspace inspection execution",
    "file read",
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch application",
    "raw prompt persistence",
    "raw response persistence",
    "raw model output persistence",
    "secret content trace",
    "credential content trace",
    "token content trace",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_V0347_WITHDRAWAL_CONDITIONS = [
    "Any provider, existing-boundary, agent-step, tool, workspace inspection, shell, command, write, edit, or patch execution path is introduced.",
    "Any file/database/log trace write, persistent trace write, external trace sink, raw prompt/response/model-output persistence, or unsafe readiness flag is introduced.",
    "Any secret, credential, token, full file content, or unbounded payload is retained in trace attributes.",
]

UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_ocel_emission",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_provider_invocation",
    "ready_for_existing_boundary_invocation",
    "ready_for_agent_step_execution",
    "ready_for_tool_execution",
    "ready_for_workspace_inspection_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_raw_prompt_persistence",
    "ready_for_raw_response_persistence",
    "ready_for_raw_model_output_persistence",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_network_access",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


class ModelInvocationTraceEventKind(StrEnum):
    MODEL_REQUEST_ENVELOPE_CREATED = "model_request_envelope_created"
    MODEL_REQUEST_ENVELOPE_VALIDATED = "model_request_envelope_validated"
    PROVIDER_PROFILE_BOUND_TO_REQUEST = "provider_profile_bound_to_request"
    EXISTING_PROVIDER_BOUNDARY_INVOCATION_REQUESTED = "existing_provider_boundary_invocation_requested"
    EXISTING_PROVIDER_BOUNDARY_INVOCATION_ALLOWED = "existing_provider_boundary_invocation_allowed"
    EXISTING_PROVIDER_BOUNDARY_INVOCATION_BLOCKED = "existing_provider_boundary_invocation_blocked"
    EXISTING_PROVIDER_BOUNDARY_CALL_STARTED = "existing_provider_boundary_call_started"
    EXISTING_PROVIDER_BOUNDARY_CALL_COMPLETED = "existing_provider_boundary_call_completed"
    EXISTING_PROVIDER_BOUNDARY_CALL_SAFE_FAILED = "existing_provider_boundary_call_safe_failed"
    MODEL_RESPONSE_ENVELOPE_CREATED = "model_response_envelope_created"
    MODEL_RESPONSE_SANITIZED = "model_response_sanitized"
    MODEL_RESPONSE_VALIDATED = "model_response_validated"
    MODEL_OUTPUT_ACTION_SIGNAL_DETECTED = "model_output_action_signal_detected"
    MODEL_OUTPUT_ACTION_CANDIDATE_EXTRACTED = "model_output_action_candidate_extracted"
    MODEL_OUTPUT_ACTION_CANDIDATE_BLOCKED = "model_output_action_candidate_blocked"
    MODEL_OUTPUT_ACTION_QUARANTINED = "model_output_action_quarantined"
    MODEL_OUTPUT_SAFE_ROUTE_CREATED = "model_output_safe_route_created"
    MODEL_BACKED_STEP_PLANNED = "model_backed_step_planned"
    MODEL_BACKED_STEP_ALLOWED = "model_backed_step_allowed"
    MODEL_BACKED_STEP_COMPLETED = "model_backed_step_completed"
    MODEL_BACKED_STEP_BLOCKED = "model_backed_step_blocked"
    MODEL_BACKED_STEP_SAFE_FAILED = "model_backed_step_safe_failed"
    UNKNOWN = "unknown"


class ModelInvocationTraceObjectType(StrEnum):
    MODEL_REQUEST_ENVELOPE = "model_request_envelope"
    MODEL_PROMPT_PAYLOAD_REF = "model_prompt_payload_ref"
    PROVIDER_PROFILE = "provider_profile"
    PROVIDER_BINDING = "provider_binding"
    EXISTING_PROVIDER_BOUNDARY_ADAPTER = "existing_provider_boundary_adapter"
    EXISTING_PROVIDER_BOUNDARY_INVOCATION = "existing_provider_boundary_invocation"
    EXISTING_PROVIDER_BOUNDARY_CALL_RECORD = "existing_provider_boundary_call_record"
    MODEL_RESPONSE_ENVELOPE = "model_response_envelope"
    SANITIZED_RESPONSE_PAYLOAD = "sanitized_response_payload"
    MODEL_RESPONSE_RISK_SIGNAL = "model_response_risk_signal"
    MODEL_RESPONSE_ACTION_SIGNAL = "model_response_action_signal"
    MODEL_OUTPUT_ACTION_CANDIDATE = "model_output_action_candidate"
    MODEL_OUTPUT_QUARANTINE_DECISION = "model_output_quarantine_decision"
    MODEL_OUTPUT_QUARANTINE_PACKET = "model_output_quarantine_packet"
    MODEL_OUTPUT_SAFE_ROUTE = "model_output_safe_route"
    MODEL_BACKED_STEP_INPUT = "model_backed_step_input"
    MODEL_BACKED_STEP_DECISION = "model_backed_step_decision"
    MODEL_BACKED_STEP_OUTPUT = "model_backed_step_output"
    MODEL_BACKED_STEP_EXECUTION_RECORD = "model_backed_step_execution_record"
    AGENT_STEP_OUTPUT_REF = "agent_step_output_ref"
    REFERENCE_CONTEXT = "reference_context"
    UNKNOWN = "unknown"


class ModelInvocationTraceRelationType(StrEnum):
    REQUEST_USES_PROMPT_PAYLOAD = "request_uses_prompt_payload"
    REQUEST_BOUND_TO_PROVIDER_PROFILE = "request_bound_to_provider_profile"
    REQUEST_BOUND_TO_PROVIDER_POLICY = "request_bound_to_provider_policy"
    BOUNDARY_INVOCATION_USES_REQUEST = "boundary_invocation_uses_request"
    BOUNDARY_DECISION_EVALUATES_REQUEST = "boundary_decision_evaluates_request"
    BOUNDARY_CALL_RETURNS_RESPONSE = "boundary_call_returns_response"
    RESPONSE_CREATED_FROM_BOUNDARY_RESULT = "response_created_from_boundary_result"
    RESPONSE_SANITIZED_INTO_PAYLOAD = "response_sanitized_into_payload"
    RESPONSE_HAS_RISK_SIGNAL = "response_has_risk_signal"
    RESPONSE_HAS_ACTION_SIGNAL = "response_has_action_signal"
    ACTION_SIGNAL_EXTRACTS_CANDIDATE = "action_signal_extracts_candidate"
    CANDIDATE_HAS_QUARANTINE_DECISION = "candidate_has_quarantine_decision"
    CANDIDATE_BLOCKED_BY_DECISION = "candidate_blocked_by_decision"
    CANDIDATE_ROUTED_TO_SAFE_ROUTE = "candidate_routed_to_safe_route"
    QUARANTINE_PACKET_CONTAINS_CANDIDATE = "quarantine_packet_contains_candidate"
    QUARANTINE_PACKET_CONTAINS_DECISION = "quarantine_packet_contains_decision"
    MODEL_BACKED_STEP_USES_QUARANTINE_PACKET = "model_backed_step_uses_quarantine_packet"
    MODEL_BACKED_STEP_USES_RESPONSE_ENVELOPE = "model_backed_step_uses_response_envelope"
    MODEL_BACKED_STEP_PRODUCES_OUTPUT = "model_backed_step_produces_output"
    MODEL_BACKED_STEP_HAS_EXECUTION_RECORD = "model_backed_step_has_execution_record"
    TRACE_PACKET_CONTAINS_EVENT = "trace_packet_contains_event"
    TRACE_PACKET_CONTAINS_OBJECT = "trace_packet_contains_object"
    UNKNOWN = "unknown"


class ModelInvocationTraceAttributeKind(StrEnum):
    SUMMARY = "summary"
    STATUS = "status"
    READINESS_LEVEL = "readiness_level"
    DECISION_KIND = "decision_kind"
    OUTCOME_KIND = "outcome_kind"
    RISK_KIND = "risk_kind"
    ROUTE_KIND = "route_kind"
    PROVIDER_PROFILE_KIND = "provider_profile_kind"
    INVOCATION_MODE = "invocation_mode"
    BOUNDARY_KIND = "boundary_kind"
    REDACTION_STATUS = "redaction_status"
    TRUNCATION_STATUS = "truncation_status"
    BOUNDED_PAYLOAD = "bounded_payload"
    SOURCE_REF = "source_ref"
    EVIDENCE_REF = "evidence_ref"
    PROMPT_PAYLOAD_REF = "prompt_payload_ref"
    RESPONSE_ENVELOPE_REF = "response_envelope_ref"
    QUARANTINE_PACKET_REF = "quarantine_packet_ref"
    MODEL_BACKED_STEP_REF = "model_backed_step_ref"
    TIMESTAMP = "timestamp"
    UNKNOWN = "unknown"


class ModelInvocationTraceSinkKind(StrEnum):
    RETURNED_TRACE_PACKET = "returned_trace_packet"
    IN_MEMORY_TEST_SINK = "in_memory_test_sink"
    DISABLED = "disabled"
    FUTURE_INTERNAL_OCEL_STORE = "future_internal_ocel_store"
    EXTERNAL_TRACE_SINK_BLOCKED = "external_trace_sink_blocked"
    UNKNOWN = "unknown"


class ModelInvocationTraceStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    POLICY_CHECKED = "policy_checked"
    EMITTED_AS_PACKET = "emitted_as_packet"
    EMITTED_TO_IN_MEMORY_SINK = "emitted_to_in_memory_sink"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class ModelInvocationTraceDecisionKind(StrEnum):
    ALLOW_TRACE_PACKET_CREATION = "allow_trace_packet_creation"
    ALLOW_IN_MEMORY_TEST_SINK = "allow_in_memory_test_sink"
    DENY = "deny"
    BLOCK = "block"
    SKIP = "skip"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ModelInvocationTraceRiskKind(StrEnum):
    RAW_PROMPT_PERSISTENCE_RISK = "raw_prompt_persistence_risk"
    RAW_RESPONSE_PERSISTENCE_RISK = "raw_response_persistence_risk"
    RAW_MODEL_OUTPUT_PERSISTENCE_RISK = "raw_model_output_persistence_risk"
    SECRET_CONTENT_TRACE_RISK = "secret_content_trace_risk"
    CREDENTIAL_CONTENT_TRACE_RISK = "credential_content_trace_risk"
    TOKEN_CONTENT_TRACE_RISK = "token_content_trace_risk"
    UNBOUNDED_PAYLOAD_RISK = "unbounded_payload_risk"
    FULL_FILE_CONTENT_TRACE_RISK = "full_file_content_trace_risk"
    PROVIDER_INVOCATION_CONFUSION_RISK = "provider_invocation_confusion_risk"
    EXISTING_BOUNDARY_INVOCATION_CONFUSION_RISK = "existing_boundary_invocation_confusion_risk"
    ACTION_EXECUTION_CONFUSION_RISK = "action_execution_confusion_risk"
    TOOL_EXECUTION_CONFUSION_RISK = "tool_execution_confusion_risk"
    PATCH_EXECUTION_CONFUSION_RISK = "patch_execution_confusion_risk"
    PERSISTENT_TRACE_WRITE_RISK = "persistent_trace_write_risk"
    EXTERNAL_TRACE_SINK_RISK = "external_trace_sink_risk"
    REFERENCE_CONTENT_LEAK_RISK = "reference_content_leak_risk"
    UNKNOWN = "unknown"


class ModelInvocationTraceSourceKind(StrEnum):
    V0346_MODEL_BACKED_STEP_OUTPUT = "v0346_model_backed_step_output"
    V0346_MODEL_BACKED_STEP_EXECUTION_RECORD = "v0346_model_backed_step_execution_record"
    V0345_QUARANTINE_PACKET = "v0345_quarantine_packet"
    V0345_ACTION_CANDIDATE = "v0345_action_candidate"
    V0345_QUARANTINE_DECISION = "v0345_quarantine_decision"
    V0345_SAFE_ROUTE = "v0345_safe_route"
    V0344_PROVIDER_BOUNDARY_RESULT = "v0344_provider_boundary_result"
    V0344_PROVIDER_BOUNDARY_CALL_RECORD = "v0344_provider_boundary_call_record"
    V0343_RESPONSE_ENVELOPE = "v0343_response_envelope"
    V0343_SANITIZED_RESPONSE_PAYLOAD = "v0343_sanitized_response_payload"
    V0342_REQUEST_ENVELOPE = "v0342_request_envelope"
    V0342_PROMPT_PAYLOAD_REF = "v0342_prompt_payload_ref"
    V0341_PROVIDER_PROFILE = "v0341_provider_profile"
    V0340_BOUNDARY = "v0340_boundary"
    TEST_FIXTURE = "test_fixture"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    UNKNOWN = "unknown"


class ModelInvocationTraceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    TRACE_CONTRACT_READY = "trace_contract_ready"
    TRACE_PACKET_READY = "trace_packet_ready"
    BOUNDED_MODEL_INVOCATION_TRACE_READY = "bounded_model_invocation_trace_ready"
    DESIGN_HANDOFF_READY_FOR_V0348 = "design_handoff_ready_for_v0348"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


def _validate_version_includes_v0347(version: str) -> None:
    _require_non_blank("version", version)
    if V0347_VERSION not in version:
        raise ValueError("version must include v0.34.7")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.7")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.7")


def _validate_non_negative(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _has_prohibited_payload(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _validate_prohibited_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited_payload_patterns", values)
    lowered = " | ".join(values).lower()
    for required in ("secret", "key", "token", "credential", "pem", "id_rsa"):
        if required not in lowered:
            raise ValueError("prohibited_payload_patterns missing v0.34.7 secret-like pattern")


def _validate_metadata_no_trace_side_effect(metadata: dict[str, Any]) -> None:
    if not isinstance(metadata, dict):
        raise TypeError("metadata must be dict")
    if _metadata_flag_true(
        metadata,
        {
            "provider_invocation",
            "existing_boundary_invocation",
            "agent_step_execution",
            "tool_execution",
            "workspace_inspection_execution",
            "file_read",
            "file_write",
            "persistent_trace_write",
            "external_trace_sink",
            "raw_prompt_persistence",
            "raw_response_persistence",
            "raw_model_output_persistence",
            "credential_access",
            "secret_read",
            "network_access",
            "workspace_write",
            "code_edit",
            "patch_application",
            "registry_mutation",
            "memory_mutation",
            "ui_runtime",
            "authority_grant",
        },
    ):
        raise ValueError("v0.34.7 metadata cannot imply execution, persistence, or external trace sinks")


def _validate_trace_attributes(name: str, values: dict[str, Any], max_chars: int, patterns: list[str]) -> None:
    if not isinstance(values, dict):
        raise TypeError(f"{name} must be dict")
    for key, value in values.items():
        if not isinstance(key, str):
            raise TypeError(f"{name} keys must be strings")
        preview = str(value)
        if len(preview) > max_chars:
            raise ValueError(f"{name} values must be bounded")
        if _has_prohibited_payload(preview, patterns) and "redacted" not in preview.lower():
            raise ValueError(f"{name} must not include raw/secret-like trace content")


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


def _sanitize_preview(value: Any, policy: "ModelInvocationTracePolicy") -> tuple[str, bool, bool]:
    if value is None:
        preview = ""
    elif isinstance(value, dict):
        keys = sorted(str(key) for key in value.keys())[:6]
        preview = f"dict(keys={','.join(keys)}, count={len(value)})"
    elif isinstance(value, (list, tuple, set)):
        preview = f"{type(value).__name__}(count={len(value)})"
    else:
        preview = str(value)
    redacted = False
    if _has_prohibited_payload(preview, policy.prohibited_payload_patterns):
        preview = "[redacted]"
        redacted = True
    truncated = False
    if len(preview) > policy.max_attribute_chars:
        suffix = "...[truncated]"
        preview = preview[: max(policy.max_attribute_chars - len(suffix), 0)] + suffix
        truncated = True
    return preview, redacted, truncated


@dataclass(frozen=True)
class ModelInvocationTraceFlagSet:
    flag_set_id: str
    version: str = V0347_VERSION
    model_invocation_trace_packet_constructed: bool = False
    model_invocation_trace_validation_available: bool = False
    bounded_model_invocation_ocel_trace_emission_enabled: bool = False
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_execution: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_bounded_model_invocation_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_network_access: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    production_certified: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0347(self.version)
        _validate_false(self, UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.7")
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceSourceRef:
    source_ref_id: str
    source_kind: ModelInvocationTraceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ModelInvocationTraceSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_trace_side_effect(self.metadata)

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
class ModelInvocationTracePolicy:
    trace_policy_id: str
    allowed_event_kinds: list[ModelInvocationTraceEventKind | str] = field(default_factory=list)
    allowed_object_types: list[ModelInvocationTraceObjectType | str] = field(default_factory=list)
    allowed_relation_types: list[ModelInvocationTraceRelationType | str] = field(default_factory=list)
    allowed_sink_kinds: list[ModelInvocationTraceSinkKind | str] = field(default_factory=list)
    prohibited_attribute_kinds: list[ModelInvocationTraceAttributeKind | str] = field(default_factory=list)
    prohibited_payload_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS))
    max_attribute_chars: int = 160
    max_event_count: int = 100
    max_object_count: int = 100
    max_relation_count: int = 100
    allow_raw_prompt: bool = False
    allow_raw_response: bool = False
    allow_raw_model_output: bool = False
    allow_secret_content: bool = False
    allow_credential_content: bool = False
    allow_token_content: bool = False
    allow_full_file_content: bool = False
    allow_persistent_write: bool = False
    allow_external_sink: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_policy_id", self.trace_policy_id)
        _validate_enum_list("allowed_event_kinds", self.allowed_event_kinds, ModelInvocationTraceEventKind)
        _validate_enum_list("allowed_object_types", self.allowed_object_types, ModelInvocationTraceObjectType)
        _validate_enum_list("allowed_relation_types", self.allowed_relation_types, ModelInvocationTraceRelationType)
        _validate_enum_list("allowed_sink_kinds", self.allowed_sink_kinds, ModelInvocationTraceSinkKind)
        _validate_enum_list("prohibited_attribute_kinds", self.prohibited_attribute_kinds, ModelInvocationTraceAttributeKind)
        _validate_prohibited_patterns(self.prohibited_payload_patterns)
        for name in ("max_attribute_chars", "max_event_count", "max_object_count", "max_relation_count"):
            _validate_non_negative(name, getattr(self, name))
        _validate_false(
            self,
            (
                "allow_raw_prompt",
                "allow_raw_response",
                "allow_raw_model_output",
                "allow_secret_content",
                "allow_credential_content",
                "allow_token_content",
                "allow_full_file_content",
                "allow_persistent_write",
                "allow_external_sink",
            ),
        )
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceObject:
    object_id: str
    object_type: ModelInvocationTraceObjectType | str
    object_key: str
    attributes: dict[str, Any] = field(default_factory=dict)
    source_refs: list[ModelInvocationTraceSourceRef] = field(default_factory=list)
    redacted: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("object_id", self.object_id)
        ModelInvocationTraceObjectType(self.object_type)
        _require_non_blank("object_key", self.object_key)
        _validate_trace_attributes("attributes", self.attributes, int(self.metadata.get("max_attribute_chars", 160)), self.metadata.get("prohibited_payload_patterns", DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS))
        _validate_object_list("source_refs", self.source_refs, ModelInvocationTraceSourceRef)
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceEvent:
    event_id: str
    event_kind: ModelInvocationTraceEventKind | str
    event_label: str
    timestamp: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    related_object_ids: list[str] = field(default_factory=list)
    source_refs: list[ModelInvocationTraceSourceRef] = field(default_factory=list)
    redacted: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("event_id", self.event_id)
        ModelInvocationTraceEventKind(self.event_kind)
        _require_non_blank("event_label", self.event_label)
        _validate_trace_attributes("attributes", self.attributes, int(self.metadata.get("max_attribute_chars", 160)), self.metadata.get("prohibited_payload_patterns", DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS))
        _validate_string_list("related_object_ids", self.related_object_ids)
        _validate_object_list("source_refs", self.source_refs, ModelInvocationTraceSourceRef)
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceRelation:
    relation_id: str
    relation_type: ModelInvocationTraceRelationType | str
    source_object_id: str
    target_object_id: str
    event_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("relation_id", self.relation_id)
        ModelInvocationTraceRelationType(self.relation_type)
        _require_non_blank("source_object_id", self.source_object_id)
        _require_non_blank("target_object_id", self.target_object_id)
        _validate_trace_attributes("attributes", self.attributes, int(self.metadata.get("max_attribute_chars", 160)), self.metadata.get("prohibited_payload_patterns", DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS))
        _validate_metadata_no_trace_side_effect(self.metadata)

    @property
    def registry_mutation(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelInvocationTraceAttribute:
    attribute_id: str
    attribute_kind: ModelInvocationTraceAttributeKind | str
    key: str
    value_preview: str
    redacted: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("attribute_id", self.attribute_id)
        ModelInvocationTraceAttributeKind(self.attribute_kind)
        _require_non_blank("key", self.key)
        max_chars = int(self.metadata.get("max_attribute_chars", 160))
        if len(self.value_preview) > max_chars:
            raise ValueError("value_preview must be bounded")
        patterns = self.metadata.get("prohibited_payload_patterns", DEFAULT_MODEL_INVOCATION_TRACE_PROHIBITED_PAYLOAD_PATTERNS)
        if _has_prohibited_payload(self.value_preview, patterns) and not self.redacted:
            raise ValueError("attribute must not contain raw/secret-like trace content")
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTracePacket:
    trace_packet_id: str
    version: str
    sink_kind: ModelInvocationTraceSinkKind | str
    objects: list[ModelInvocationTraceObject] = field(default_factory=list)
    events: list[ModelInvocationTraceEvent] = field(default_factory=list)
    relations: list[ModelInvocationTraceRelation] = field(default_factory=list)
    attributes: list[ModelInvocationTraceAttribute] = field(default_factory=list)
    source_refs: list[ModelInvocationTraceSourceRef] = field(default_factory=list)
    status: ModelInvocationTraceStatus | str = ModelInvocationTraceStatus.EMITTED_AS_PACKET
    redaction_applied: bool = False
    truncated: bool = False
    summary: str = "Model invocation trace packet; returned artifact only."
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_packet_id", self.trace_packet_id)
        _validate_version_includes_v0347(self.version)
        ModelInvocationTraceSinkKind(self.sink_kind)
        _validate_object_list("objects", self.objects, ModelInvocationTraceObject)
        _validate_object_list("events", self.events, ModelInvocationTraceEvent)
        _validate_object_list("relations", self.relations, ModelInvocationTraceRelation)
        _validate_object_list("attributes", self.attributes, ModelInvocationTraceAttribute)
        _validate_object_list("source_refs", self.source_refs, ModelInvocationTraceSourceRef)
        ModelInvocationTraceStatus(self.status)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_persistent_write", "ready_for_external_sink", "ready_for_execution"))
        _validate_metadata_no_trace_side_effect(self.metadata)

    @property
    def persistent_storage(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelInvocationTraceEmissionInput:
    emission_input_id: str
    source_version: str
    request_envelope_id: str | None = None
    response_envelope_id: str | None = None
    provider_boundary_result_id: str | None = None
    quarantine_packet_id: str | None = None
    model_backed_step_output_id: str | None = None
    model_backed_step_execution_record_id: str | None = None
    requested_sink_kind: ModelInvocationTraceSinkKind | str = ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET
    task_summary: str = "Model invocation trace emission input."
    source_refs: list[ModelInvocationTraceSourceRef] = field(default_factory=list)
    prohibited_trace_content: list[str] = field(default_factory=lambda: list(DEFAULT_MODEL_INVOCATION_PROHIBITED_TRACE_CONTENT))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emission_input_id", self.emission_input_id)
        _require_non_blank("source_version", self.source_version)
        _validate_version_includes_v0347(self.source_version)
        ModelInvocationTraceSinkKind(self.requested_sink_kind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_object_list("source_refs", self.source_refs, ModelInvocationTraceSourceRef)
        _validate_contains_terms(
            "prohibited_trace_content",
            self.prohibited_trace_content,
            ["raw prompt", "raw response", "raw model output", "file content", "secrets", "credentials", "tokens", "unbounded output"],
        )
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceEmissionDecision:
    decision_id: str
    emission_input_id: str
    decision_kind: ModelInvocationTraceDecisionKind | str
    reason: str
    allowed_sink_kind: ModelInvocationTraceSinkKind | str | None = None
    risk_kinds: list[ModelInvocationTraceRiskKind | str] = field(default_factory=list)
    redaction_required: bool = True
    truncation_required: bool = True
    persistent_write_allowed: bool = False
    external_sink_allowed: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("decision_id", self.decision_id)
        _require_non_blank("emission_input_id", self.emission_input_id)
        ModelInvocationTraceDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        if self.allowed_sink_kind is not None:
            ModelInvocationTraceSinkKind(self.allowed_sink_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelInvocationTraceRiskKind)
        _validate_false(self, ("persistent_write_allowed", "external_sink_allowed", "ready_for_execution"))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceValidationReport:
    validation_report_id: str
    version: str
    trace_packet_id: str | None = None
    checked_event_ids: list[str] = field(default_factory=list)
    checked_object_ids: list[str] = field(default_factory=list)
    checked_relation_ids: list[str] = field(default_factory=list)
    risk_kinds: list[ModelInvocationTraceRiskKind | str] = field(default_factory=list)
    redacted_field_count: int = 0
    truncated_field_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validation_passed: bool = True
    summary: str = "Model invocation trace validation report; not certification."
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version_includes_v0347(self.version)
        _require_non_blank("summary", self.summary)
        for name in ("checked_event_ids", "checked_object_ids", "checked_relation_ids", "blocked_items", "warnings"):
            _validate_string_list(name, getattr(self, name))
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelInvocationTraceRiskKind)
        for name in ("redacted_field_count", "truncated_field_count"):
            _validate_non_negative(name, getattr(self, name))
        if self.blocked_items and self.validation_passed:
            raise ValueError("validation_passed cannot be True if blocked_items are present")
        _validate_false(self, ("ready_for_persistent_write", "ready_for_external_sink", "ready_for_execution"))
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceEmissionReport:
    report_id: str
    version: str
    emission_input_id: str
    trace_packet_id: str | None = None
    validation_report_id: str | None = None
    status: ModelInvocationTraceStatus | str = ModelInvocationTraceStatus.EMITTED_AS_PACKET
    readiness_level: ModelInvocationTraceReadinessLevel | str = ModelInvocationTraceReadinessLevel.BOUNDED_MODEL_INVOCATION_TRACE_READY
    summary: str = "Model invocation trace emission report; no persistent write."
    event_count: int = 0
    object_count: int = 0
    relation_count: int = 0
    redacted_field_count: int = 0
    truncated_field_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_bounded_model_invocation_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_V0347_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("report_id", "version", "emission_input_id", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0347(self.version)
        ModelInvocationTraceStatus(self.status)
        ModelInvocationTraceReadinessLevel(self.readiness_level)
        for name in ("event_count", "object_count", "relation_count", "redacted_field_count", "truncated_field_count"):
            _validate_non_negative(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_general_ocel_emission", "ready_for_persistent_trace_write", "ready_for_external_trace_sink", "ready_for_execution"))
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceEmitter:
    emitter_id: str
    version: str
    supported_event_kinds: list[ModelInvocationTraceEventKind | str]
    supported_object_types: list[ModelInvocationTraceObjectType | str]
    supported_relation_types: list[ModelInvocationTraceRelationType | str]
    supported_sink_kinds: list[ModelInvocationTraceSinkKind | str]
    trace_policy: ModelInvocationTracePolicy
    flags: ModelInvocationTraceFlagSet
    summary: str = "Model invocation trace emitter returns bounded packets only."
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("emitter_id", "version", "summary"):
            _require_non_blank(name, getattr(self, name))
        _validate_version_includes_v0347(self.version)
        _validate_enum_list("supported_event_kinds", self.supported_event_kinds, ModelInvocationTraceEventKind)
        _validate_enum_list("supported_object_types", self.supported_object_types, ModelInvocationTraceObjectType)
        _validate_enum_list("supported_relation_types", self.supported_relation_types, ModelInvocationTraceRelationType)
        _validate_enum_list("supported_sink_kinds", self.supported_sink_kinds, ModelInvocationTraceSinkKind)
        if not isinstance(self.trace_policy, ModelInvocationTracePolicy):
            raise TypeError("trace_policy must be ModelInvocationTracePolicy")
        if not isinstance(self.flags, ModelInvocationTraceFlagSet):
            raise TypeError("flags must be ModelInvocationTraceFlagSet")
        if not model_invocation_trace_flags_preserve_unsafe_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        _validate_false(self, ("ready_for_persistent_trace_write", "ready_for_external_sink", "ready_for_execution"))
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceRunPreview:
    run_preview_id: str
    emitter_id: str | None = None
    planned_steps: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    explicitly_not_performed: list[str] = field(default_factory=list)
    no_provider_invocation_guarantee: bool = True
    no_existing_boundary_invocation_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_file_read_guarantee: bool = True
    no_shell_execution_guarantee: bool = True
    no_subprocess_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_raw_prompt_persistence_guarantee: bool = True
    no_raw_response_persistence_guarantee: bool = True
    no_raw_model_output_persistence_guarantee: bool = True
    no_secret_content_trace_guarantee: bool = True
    no_credential_content_trace_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_external_trace_sink_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class ModelInvocationTraceNoPersistenceGuarantee:
    guarantee_id: str
    version: str
    no_provider_invocation: bool = True
    no_existing_boundary_invocation: bool = True
    no_agent_step_execution: bool = True
    no_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_file_read: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_raw_prompt_persistence: bool = True
    no_raw_response_persistence: bool = True
    no_raw_model_output_persistence: bool = True
    no_secret_content_trace: bool = True
    no_credential_content_trace: bool = True
    no_token_content_trace: bool = True
    no_full_file_content_trace: bool = True
    no_persistent_trace_write: bool = True
    no_external_trace_sink: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0347(self.version)
        _validate_true(self, tuple(name for name in self.__dataclass_fields__ if name.startswith("no_")))
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_trace_side_effect(self.metadata)


@dataclass(frozen=True)
class V0347ReadinessReport:
    report_id: str
    version: str
    emitter_id: str | None = None
    trace_packet_id: str | None = None
    trace_emission_report_id: str | None = None
    validation_report_id: str | None = None
    summary: str = "v0.34.7 model invocation trace packet readiness only."
    ready_for_v0348_cli_model_backed_agent_step_surface: bool = False
    ready_for_execution: bool = False
    ready_for_model_invocation_trace_packet_creation: bool = False
    ready_for_bounded_model_invocation_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_tool_execution: bool = False
    ready_for_workspace_inspection_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_raw_prompt_persistence: bool = False
    ready_for_raw_response_persistence: bool = False
    ready_for_raw_model_output_persistence: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_network_access: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_V0347_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_V0347_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0347(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            [
                "provider invocation",
                "existing boundary invocation",
                "agent step execution",
                "tool execution",
                "workspace inspection execution",
                "file read",
                "shell",
                "subprocess",
                "command",
                "workspace write",
                "code edit",
                "patch application",
                "raw prompt persistence",
                "raw response persistence",
                "raw model output persistence",
                "secret content trace",
                "credential content trace",
                "token content trace",
                "persistent trace write",
                "external trace sink",
                "UI runtime",
                "external control",
                "authority grant",
            ],
        )
        _validate_metadata_no_trace_side_effect(self.metadata)


def build_model_invocation_trace_flags(flag_set_id: str = "model_invocation_trace_flags:v0.34.7", **kwargs: Any) -> ModelInvocationTraceFlagSet:
    return ModelInvocationTraceFlagSet(flag_set_id=flag_set_id, version=kwargs.pop("version", V0347_VERSION), **kwargs)


def build_model_invocation_trace_source_ref(
    source_ref_id: str = "model_invocation_trace_source_ref:v0.34.7",
    source_kind: ModelInvocationTraceSourceKind | str = ModelInvocationTraceSourceKind.TEST_FIXTURE,
    source_id: str = "model_invocation_trace_source:v0.34.7",
    source_summary: str = "Model invocation trace source ref metadata only.",
    **kwargs: Any,
) -> ModelInvocationTraceSourceRef:
    return ModelInvocationTraceSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_model_invocation_trace_policy(trace_policy_id: str = "model_invocation_trace_policy:v0.34.7", **kwargs: Any) -> ModelInvocationTracePolicy:
    return ModelInvocationTracePolicy(trace_policy_id=trace_policy_id, **kwargs)


def default_model_invocation_trace_policy(**kwargs: Any) -> ModelInvocationTracePolicy:
    return build_model_invocation_trace_policy(
        allowed_sink_kinds=kwargs.pop("allowed_sink_kinds", [ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET, ModelInvocationTraceSinkKind.IN_MEMORY_TEST_SINK, ModelInvocationTraceSinkKind.DISABLED]),
        **kwargs,
    )


def _sanitize_attribute_dict(attributes: dict[str, Any], policy: ModelInvocationTracePolicy) -> tuple[dict[str, str], bool, bool]:
    sanitized: dict[str, str] = {}
    redacted = False
    truncated = False
    for key, value in attributes.items():
        preview, was_redacted, was_truncated = _sanitize_preview(value, policy)
        sanitized[str(key)] = preview
        redacted = redacted or was_redacted
        truncated = truncated or was_truncated
    return sanitized, redacted, truncated


def build_model_invocation_trace_object(
    object_id: str = "model_invocation_trace_object:v0.34.7",
    object_type: ModelInvocationTraceObjectType | str = ModelInvocationTraceObjectType.UNKNOWN,
    object_key: str = "model_invocation_trace_object_key:v0.34.7",
    attributes: dict[str, Any] | None = None,
    source_refs: list[ModelInvocationTraceSourceRef] | None = None,
    policy: ModelInvocationTracePolicy | None = None,
    **kwargs: Any,
) -> ModelInvocationTraceObject:
    policy = policy or default_model_invocation_trace_policy()
    sanitized, redacted, truncated = _sanitize_attribute_dict(attributes or {}, policy)
    return ModelInvocationTraceObject(
        object_id=object_id,
        object_type=object_type,
        object_key=object_key,
        attributes=sanitized,
        source_refs=source_refs or [],
        redacted=kwargs.pop("redacted", redacted),
        truncated=kwargs.pop("truncated", truncated),
        metadata=kwargs.pop("metadata", {"max_attribute_chars": policy.max_attribute_chars, "prohibited_payload_patterns": policy.prohibited_payload_patterns}),
        **kwargs,
    )


def build_model_invocation_trace_event(
    event_id: str = "model_invocation_trace_event:v0.34.7",
    event_kind: ModelInvocationTraceEventKind | str = ModelInvocationTraceEventKind.UNKNOWN,
    event_label: str = "Model invocation trace event.",
    attributes: dict[str, Any] | None = None,
    related_object_ids: list[str] | None = None,
    source_refs: list[ModelInvocationTraceSourceRef] | None = None,
    policy: ModelInvocationTracePolicy | None = None,
    **kwargs: Any,
) -> ModelInvocationTraceEvent:
    policy = policy or default_model_invocation_trace_policy()
    sanitized, redacted, truncated = _sanitize_attribute_dict(attributes or {}, policy)
    return ModelInvocationTraceEvent(
        event_id=event_id,
        event_kind=event_kind,
        event_label=event_label,
        timestamp=kwargs.pop("timestamp", None),
        attributes=sanitized,
        related_object_ids=related_object_ids or [],
        source_refs=source_refs or [],
        redacted=kwargs.pop("redacted", redacted),
        truncated=kwargs.pop("truncated", truncated),
        metadata=kwargs.pop("metadata", {"max_attribute_chars": policy.max_attribute_chars, "prohibited_payload_patterns": policy.prohibited_payload_patterns}),
        **kwargs,
    )


def build_model_invocation_trace_relation(
    relation_id: str = "model_invocation_trace_relation:v0.34.7",
    relation_type: ModelInvocationTraceRelationType | str = ModelInvocationTraceRelationType.UNKNOWN,
    source_object_id: str = "source_object:v0.34.7",
    target_object_id: str = "target_object:v0.34.7",
    policy: ModelInvocationTracePolicy | None = None,
    **kwargs: Any,
) -> ModelInvocationTraceRelation:
    policy = policy or default_model_invocation_trace_policy()
    sanitized, _redacted, _truncated = _sanitize_attribute_dict(kwargs.pop("attributes", {}), policy)
    return ModelInvocationTraceRelation(
        relation_id=relation_id,
        relation_type=relation_type,
        source_object_id=source_object_id,
        target_object_id=target_object_id,
        event_id=kwargs.pop("event_id", None),
        attributes=sanitized,
        metadata=kwargs.pop("metadata", {"max_attribute_chars": policy.max_attribute_chars, "prohibited_payload_patterns": policy.prohibited_payload_patterns}),
        **kwargs,
    )


def build_model_invocation_trace_attribute(
    attribute_id: str = "model_invocation_trace_attribute:v0.34.7",
    attribute_kind: ModelInvocationTraceAttributeKind | str = ModelInvocationTraceAttributeKind.SUMMARY,
    key: str = "summary",
    value: Any = "bounded",
    policy: ModelInvocationTracePolicy | None = None,
    **kwargs: Any,
) -> ModelInvocationTraceAttribute:
    policy = policy or default_model_invocation_trace_policy()
    value_preview, redacted, truncated = _sanitize_preview(value, policy)
    return ModelInvocationTraceAttribute(
        attribute_id=attribute_id,
        attribute_kind=attribute_kind,
        key=key,
        value_preview=kwargs.pop("value_preview", value_preview),
        redacted=kwargs.pop("redacted", redacted),
        truncated=kwargs.pop("truncated", truncated),
        metadata=kwargs.pop("metadata", {"max_attribute_chars": policy.max_attribute_chars, "prohibited_payload_patterns": policy.prohibited_payload_patterns}),
        **kwargs,
    )


def sanitize_model_invocation_trace_attribute_value(value: Any, policy: ModelInvocationTracePolicy | None = None) -> ModelInvocationTraceAttribute:
    return build_model_invocation_trace_attribute(value=value, policy=policy)


def build_model_invocation_trace_packet(trace_packet_id: str = "model_invocation_trace_packet:v0.34.7", **kwargs: Any) -> ModelInvocationTracePacket:
    return ModelInvocationTracePacket(
        trace_packet_id=trace_packet_id,
        version=kwargs.pop("version", V0347_VERSION),
        sink_kind=kwargs.pop("sink_kind", ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET),
        **kwargs,
    )


def build_model_invocation_trace_emission_input(emission_input_id: str = "model_invocation_trace_emission_input:v0.34.7", **kwargs: Any) -> ModelInvocationTraceEmissionInput:
    return ModelInvocationTraceEmissionInput(emission_input_id=emission_input_id, source_version=kwargs.pop("source_version", V0347_VERSION), **kwargs)


def build_model_invocation_trace_emission_decision(decision_id: str = "model_invocation_trace_emission_decision:v0.34.7", **kwargs: Any) -> ModelInvocationTraceEmissionDecision:
    return ModelInvocationTraceEmissionDecision(
        decision_id=decision_id,
        emission_input_id=kwargs.pop("emission_input_id", "model_invocation_trace_emission_input:v0.34.7"),
        decision_kind=kwargs.pop("decision_kind", ModelInvocationTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION),
        reason=kwargs.pop("reason", "Returned model invocation trace packet creation is allowed; no persistence."),
        allowed_sink_kind=kwargs.pop("allowed_sink_kind", ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET),
        **kwargs,
    )


def build_model_invocation_trace_validation_report(validation_report_id: str = "model_invocation_trace_validation_report:v0.34.7", **kwargs: Any) -> ModelInvocationTraceValidationReport:
    return ModelInvocationTraceValidationReport(validation_report_id=validation_report_id, version=kwargs.pop("version", V0347_VERSION), **kwargs)


def build_model_invocation_trace_emission_report(report_id: str = "model_invocation_trace_emission_report:v0.34.7", **kwargs: Any) -> ModelInvocationTraceEmissionReport:
    return ModelInvocationTraceEmissionReport(
        report_id=report_id,
        version=kwargs.pop("version", V0347_VERSION),
        emission_input_id=kwargs.pop("emission_input_id", "model_invocation_trace_emission_input:v0.34.7"),
        **kwargs,
    )


def build_model_invocation_trace_emitter(emitter_id: str = "model_invocation_trace_emitter:v0.34.7", **kwargs: Any) -> ModelInvocationTraceEmitter:
    return ModelInvocationTraceEmitter(
        emitter_id=emitter_id,
        version=kwargs.pop("version", V0347_VERSION),
        supported_event_kinds=kwargs.pop("supported_event_kinds", list(ModelInvocationTraceEventKind)),
        supported_object_types=kwargs.pop("supported_object_types", list(ModelInvocationTraceObjectType)),
        supported_relation_types=kwargs.pop("supported_relation_types", list(ModelInvocationTraceRelationType)),
        supported_sink_kinds=kwargs.pop("supported_sink_kinds", [ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET, ModelInvocationTraceSinkKind.IN_MEMORY_TEST_SINK, ModelInvocationTraceSinkKind.DISABLED]),
        trace_policy=kwargs.pop("trace_policy", default_model_invocation_trace_policy()),
        flags=kwargs.pop("flags", build_model_invocation_trace_flags(model_invocation_trace_packet_constructed=True, model_invocation_trace_validation_available=True, bounded_model_invocation_ocel_trace_emission_enabled=True, ready_for_model_invocation_trace_packet_creation=True, ready_for_bounded_model_invocation_ocel_trace_emission=True)),
        ready_for_model_invocation_trace_packet_creation=kwargs.pop("ready_for_model_invocation_trace_packet_creation", True),
        **kwargs,
    )


def build_model_invocation_trace_run_preview(run_preview_id: str = "model_invocation_trace_run_preview:v0.34.7", **kwargs: Any) -> ModelInvocationTraceRunPreview:
    return ModelInvocationTraceRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_model_invocation_trace_no_persistence_guarantee(
    guarantee_id: str = "model_invocation_trace_no_persistence_guarantee:v0.34.7",
    **kwargs: Any,
) -> ModelInvocationTraceNoPersistenceGuarantee:
    return ModelInvocationTraceNoPersistenceGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0347_VERSION), **kwargs)


def build_v0347_readiness_report(report_id: str = "v0347_readiness_report", **kwargs: Any) -> V0347ReadinessReport:
    return V0347ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0347_VERSION),
        ready_for_v0348_cli_model_backed_agent_step_surface=kwargs.pop("ready_for_v0348_cli_model_backed_agent_step_surface", True),
        ready_for_model_invocation_trace_packet_creation=kwargs.pop("ready_for_model_invocation_trace_packet_creation", True),
        ready_for_bounded_model_invocation_ocel_trace_emission=kwargs.pop("ready_for_bounded_model_invocation_ocel_trace_emission", True),
        completed_items=kwargs.pop("completed_items", ["trace policy", "trace packet", "trace validation", "readiness report"]),
        future_track_items=kwargs.pop("future_track_items", ["CLI model-backed agent step surface"]),
        **kwargs,
    )


def validate_model_invocation_trace_packet(
    packet: ModelInvocationTracePacket,
    policy: ModelInvocationTracePolicy | None = None,
) -> ModelInvocationTraceValidationReport:
    if not isinstance(packet, ModelInvocationTracePacket):
        raise TypeError("packet must be ModelInvocationTracePacket")
    policy = policy or default_model_invocation_trace_policy()
    blocked_items: list[str] = []
    warnings: list[str] = []
    risk_kinds: list[ModelInvocationTraceRiskKind] = []
    if packet.ready_for_persistent_write or packet.ready_for_external_sink or packet.ready_for_execution:
        blocked_items.append("packet attempted persistence, external sink, or execution readiness")
        risk_kinds.append(ModelInvocationTraceRiskKind.PERSISTENT_TRACE_WRITE_RISK)
    all_values: list[str] = []
    for obj in packet.objects:
        all_values.extend(str(value) for value in obj.attributes.values())
    for event in packet.events:
        all_values.extend(str(value) for value in event.attributes.values())
    for relation in packet.relations:
        all_values.extend(str(value) for value in relation.attributes.values())
    all_values.extend(attribute.value_preview for attribute in packet.attributes)
    if any(_has_prohibited_payload(value, policy.prohibited_payload_patterns) and "redacted" not in value.lower() for value in all_values):
        blocked_items.append("trace packet contains raw or secret-like content")
        risk_kinds.append(ModelInvocationTraceRiskKind.SECRET_CONTENT_TRACE_RISK)
    if len(packet.events) > policy.max_event_count:
        warnings.append("event count exceeds policy limit")
        risk_kinds.append(ModelInvocationTraceRiskKind.UNBOUNDED_PAYLOAD_RISK)
    redacted_count = sum(1 for item in [*packet.objects, *packet.events, *packet.attributes] if getattr(item, "redacted", False))
    truncated_count = sum(1 for item in [*packet.objects, *packet.events, *packet.attributes] if getattr(item, "truncated", False))
    return build_model_invocation_trace_validation_report(
        trace_packet_id=packet.trace_packet_id,
        checked_event_ids=[event.event_id for event in packet.events],
        checked_object_ids=[obj.object_id for obj in packet.objects],
        checked_relation_ids=[relation.relation_id for relation in packet.relations],
        risk_kinds=risk_kinds,
        redacted_field_count=redacted_count,
        truncated_field_count=truncated_count,
        blocked_items=blocked_items,
        warnings=warnings,
        validation_passed=not blocked_items,
        summary="Model invocation trace packet validated without persistence readiness.",
    )


def decide_model_invocation_trace_emission(
    emission_input: ModelInvocationTraceEmissionInput,
    policy: ModelInvocationTracePolicy | None = None,
) -> ModelInvocationTraceEmissionDecision:
    if not isinstance(emission_input, ModelInvocationTraceEmissionInput):
        raise TypeError("emission_input must be ModelInvocationTraceEmissionInput")
    policy = policy or default_model_invocation_trace_policy()
    sink = ModelInvocationTraceSinkKind(emission_input.requested_sink_kind)
    if sink in {ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET, ModelInvocationTraceSinkKind.IN_MEMORY_TEST_SINK} and sink in policy.allowed_sink_kinds:
        decision_kind = ModelInvocationTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK if sink == ModelInvocationTraceSinkKind.IN_MEMORY_TEST_SINK else ModelInvocationTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION
        return build_model_invocation_trace_emission_decision(
            decision_id=f"{emission_input.emission_input_id}:decision",
            emission_input_id=emission_input.emission_input_id,
            decision_kind=decision_kind,
            allowed_sink_kind=sink,
            reason="Requested model invocation trace sink is returned/in-memory only; no persistence.",
        )
    return build_model_invocation_trace_emission_decision(
        decision_id=f"{emission_input.emission_input_id}:decision",
        emission_input_id=emission_input.emission_input_id,
        decision_kind=ModelInvocationTraceDecisionKind.BLOCK,
        allowed_sink_kind=None,
        risk_kinds=[ModelInvocationTraceRiskKind.EXTERNAL_TRACE_SINK_RISK],
        reason="Requested sink is persistent, external, unknown, or otherwise blocked.",
    )


def build_model_invocation_trace_packet_from_model_backed_step_output(
    step_output: ModelBackedStepOutput,
    policy: ModelInvocationTracePolicy | None = None,
) -> ModelInvocationTracePacket:
    if not isinstance(step_output, ModelBackedStepOutput):
        raise TypeError("step_output must be ModelBackedStepOutput")
    policy = policy or default_model_invocation_trace_policy()
    source_ref = build_model_invocation_trace_source_ref(
        f"source:{step_output.step_output_id}",
        ModelInvocationTraceSourceKind.V0346_MODEL_BACKED_STEP_OUTPUT,
        step_output.step_output_id,
        "v0.34.6 ModelBackedStepOutput supplied in memory.",
    )
    output_object_id = f"object:model_backed_step_output:{step_output.step_output_id}"
    record_object_id = f"object:model_backed_step_execution_record:{step_output.execution_record.execution_record_id}"
    objects = [
        build_model_invocation_trace_object(
            output_object_id,
            ModelInvocationTraceObjectType.MODEL_BACKED_STEP_OUTPUT,
            step_output.step_output_id,
            {
                "status": str(step_output.status),
                "outcome_kind": str(step_output.outcome_kind),
                "final_response_present": step_output.final_response_text is not None,
                "ask_user_present": step_output.ask_user_message is not None,
                "quarantine_packet_ref": step_output.quarantine_packet_ref or "",
                "agent_step_output_ref": step_output.agent_step_output_ref or "",
                "redacted": step_output.redacted,
                "truncated": step_output.truncated,
            },
            [source_ref],
            policy,
        ),
        build_model_invocation_trace_object(
            record_object_id,
            ModelInvocationTraceObjectType.MODEL_BACKED_STEP_EXECUTION_RECORD,
            step_output.execution_record.execution_record_id,
            {
                "status": str(step_output.execution_record.status),
                "bounded_step": step_output.execution_record.executed_bounded_model_backed_step,
                "existing_boundary_adapter": step_output.execution_record.executed_existing_boundary_adapter_call,
                "direct_provider": step_output.execution_record.executed_direct_provider_call,
                "raw_prompt_persisted": step_output.execution_record.persisted_raw_prompt,
                "raw_response_persisted": step_output.execution_record.persisted_raw_response,
            },
            [source_ref],
            policy,
        ),
    ]
    status = ModelBackedStepStatus(step_output.status)
    event_kind = ModelInvocationTraceEventKind.MODEL_BACKED_STEP_COMPLETED
    if status == ModelBackedStepStatus.BLOCKED:
        event_kind = ModelInvocationTraceEventKind.MODEL_BACKED_STEP_BLOCKED
    elif status == ModelBackedStepStatus.SAFE_FAILED:
        event_kind = ModelInvocationTraceEventKind.MODEL_BACKED_STEP_SAFE_FAILED
    events = [
        build_model_invocation_trace_event(
            f"event:{step_output.step_output_id}:completed",
            event_kind,
            "Model-backed step artifact traced without executing it.",
            {"status": str(step_output.status), "ready_for_execution": step_output.ready_for_execution},
            [output_object_id, record_object_id],
            [source_ref],
            policy,
        )
    ]
    relations = [
        build_model_invocation_trace_relation(
            f"relation:{step_output.step_output_id}:has_record",
            ModelInvocationTraceRelationType.MODEL_BACKED_STEP_HAS_EXECUTION_RECORD,
            output_object_id,
            record_object_id,
            policy=policy,
        )
    ]
    if step_output.quarantine_packet_ref is not None:
        quarantine_object_id = f"object:quarantine_packet:{step_output.quarantine_packet_ref}"
        objects.append(
            build_model_invocation_trace_object(
                quarantine_object_id,
                ModelInvocationTraceObjectType.MODEL_OUTPUT_QUARANTINE_PACKET,
                step_output.quarantine_packet_ref,
                {"summary": "Quarantine packet ref only; candidates not executed."},
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_model_invocation_trace_relation(
                f"relation:{step_output.step_output_id}:uses_quarantine",
                ModelInvocationTraceRelationType.MODEL_BACKED_STEP_USES_QUARANTINE_PACKET,
                output_object_id,
                quarantine_object_id,
                policy=policy,
            )
        )
    attributes = [sanitize_model_invocation_trace_attribute_value(step_output.summary, policy)]
    redaction_applied = any(obj.redacted for obj in objects) or any(event.redacted for event in events) or any(attribute.redacted for attribute in attributes)
    truncated = any(obj.truncated for obj in objects) or any(event.truncated for event in events) or any(attribute.truncated for attribute in attributes)
    return build_model_invocation_trace_packet(
        f"trace_packet:{step_output.step_output_id}",
        objects=objects,
        events=events,
        relations=relations,
        attributes=attributes,
        source_refs=[source_ref],
        redaction_applied=redaction_applied,
        truncated=truncated,
        summary="Bounded trace packet from supplied v0.34.6 model-backed step output; raw output omitted.",
    )


def build_model_invocation_trace_packet_from_provider_boundary_result(
    result: ExistingProviderBoundaryInvocationResult,
    policy: ModelInvocationTracePolicy | None = None,
) -> ModelInvocationTracePacket:
    if not isinstance(result, ExistingProviderBoundaryInvocationResult):
        raise TypeError("result must be ExistingProviderBoundaryInvocationResult")
    policy = policy or default_model_invocation_trace_policy()
    source_ref = build_model_invocation_trace_source_ref(
        f"source:{result.invocation_result_id}",
        ModelInvocationTraceSourceKind.V0344_PROVIDER_BOUNDARY_RESULT,
        result.invocation_result_id,
        "v0.34.4 ExistingProviderBoundaryInvocationResult supplied in memory.",
    )
    result_object_id = f"object:provider_boundary_result:{result.invocation_result_id}"
    response_object_id = f"object:model_response_envelope:{result.response_envelope_id or 'none'}"
    objects = [
        build_model_invocation_trace_object(
            result_object_id,
            ModelInvocationTraceObjectType.EXISTING_PROVIDER_BOUNDARY_INVOCATION,
            result.invocation_result_id,
            {
                "outcome_kind": str(result.outcome_kind),
                "response_char_count": result.response_char_count,
                "response_preview_present": result.response_text_preview is not None,
                "redacted": result.redacted,
                "truncated": result.truncated,
                "ready_for_execution": result.ready_for_execution,
            },
            [source_ref],
            policy,
        )
    ]
    events = []
    outcome = ExistingProviderBoundaryOutcomeKind(result.outcome_kind)
    if outcome == ExistingProviderBoundaryOutcomeKind.SAFE_FAIL_RESULT:
        event_kind = ModelInvocationTraceEventKind.EXISTING_PROVIDER_BOUNDARY_CALL_SAFE_FAILED
    elif outcome == ExistingProviderBoundaryOutcomeKind.BLOCKED_RESULT:
        event_kind = ModelInvocationTraceEventKind.EXISTING_PROVIDER_BOUNDARY_INVOCATION_BLOCKED
    else:
        event_kind = ModelInvocationTraceEventKind.EXISTING_PROVIDER_BOUNDARY_CALL_COMPLETED
    events.append(
        build_model_invocation_trace_event(
            f"event:{result.invocation_result_id}:result",
            event_kind,
            "Existing boundary result artifact traced without invoking boundary.",
            {"outcome_kind": str(result.outcome_kind), "response_envelope_ref": result.response_envelope_id or ""},
            [result_object_id],
            [source_ref],
            policy,
        )
    )
    relations = []
    if result.response_envelope_id is not None:
        objects.append(
            build_model_invocation_trace_object(
                response_object_id,
                ModelInvocationTraceObjectType.MODEL_RESPONSE_ENVELOPE,
                result.response_envelope_id,
                {"summary": "Response envelope ref only; raw response omitted."},
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_model_invocation_trace_relation(
                f"relation:{result.invocation_result_id}:returns_response",
                ModelInvocationTraceRelationType.BOUNDARY_CALL_RETURNS_RESPONSE,
                result_object_id,
                response_object_id,
                policy=policy,
            )
        )
    return build_model_invocation_trace_packet(
        f"trace_packet:{result.invocation_result_id}",
        objects=objects,
        events=events,
        relations=relations,
        source_refs=[source_ref],
        summary="Bounded trace packet from supplied v0.34.4 boundary result; no boundary invocation.",
    )


def build_model_invocation_trace_packet_from_quarantine_packet(
    packet: ModelOutputActionQuarantinePacket,
    policy: ModelInvocationTracePolicy | None = None,
) -> ModelInvocationTracePacket:
    if not isinstance(packet, ModelOutputActionQuarantinePacket):
        raise TypeError("packet must be ModelOutputActionQuarantinePacket")
    policy = policy or default_model_invocation_trace_policy()
    source_ref = build_model_invocation_trace_source_ref(
        f"source:{packet.quarantine_packet_id}",
        ModelInvocationTraceSourceKind.V0345_QUARANTINE_PACKET,
        packet.quarantine_packet_id,
        "v0.34.5 ModelOutputActionQuarantinePacket supplied in memory.",
    )
    packet_object_id = f"object:quarantine_packet:{packet.quarantine_packet_id}"
    objects = [
        build_model_invocation_trace_object(
            packet_object_id,
            ModelInvocationTraceObjectType.MODEL_OUTPUT_QUARANTINE_PACKET,
            packet.quarantine_packet_id,
            {
                "candidate_count": packet.candidate_set.candidate_count,
                "decision_count": len(packet.decisions),
                "safe_route_count": len(packet.safe_routes),
                "blocked_count": len(packet.blocked_records),
                "action_queue": packet.action_queue,
            },
            [source_ref],
            policy,
        )
    ]
    events = [
        build_model_invocation_trace_event(
            f"event:{packet.quarantine_packet_id}:quarantined",
            ModelInvocationTraceEventKind.MODEL_OUTPUT_ACTION_QUARANTINED,
            "Model output quarantine packet traced without executing candidates.",
            {"status": str(packet.status), "ready_for_execution": packet.ready_for_execution},
            [packet_object_id],
            [source_ref],
            policy,
        )
    ]
    relations: list[ModelInvocationTraceRelation] = []
    for candidate in packet.candidate_set.candidates:
        candidate_object_id = f"object:candidate:{candidate.candidate_id}"
        objects.append(_object_from_candidate(candidate, candidate_object_id, [source_ref], policy))
        events.append(
            build_model_invocation_trace_event(
                f"event:{candidate.candidate_id}:extracted",
                ModelInvocationTraceEventKind.MODEL_OUTPUT_ACTION_CANDIDATE_EXTRACTED,
                "Action candidate traced as quarantine metadata only.",
                {"candidate_kind": str(candidate.candidate_kind), "blocked": candidate.blocked_from_execution},
                [packet_object_id, candidate_object_id],
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_model_invocation_trace_relation(
                f"relation:{packet.quarantine_packet_id}:contains_candidate:{candidate.candidate_id}",
                ModelInvocationTraceRelationType.QUARANTINE_PACKET_CONTAINS_CANDIDATE,
                packet_object_id,
                candidate_object_id,
                policy=policy,
            )
        )
    for decision in packet.decisions:
        decision_object_id = f"object:decision:{decision.decision_id}"
        objects.append(_object_from_decision(decision, decision_object_id, [source_ref], policy))
        relations.append(
            build_model_invocation_trace_relation(
                f"relation:{packet.quarantine_packet_id}:contains_decision:{decision.decision_id}",
                ModelInvocationTraceRelationType.QUARANTINE_PACKET_CONTAINS_DECISION,
                packet_object_id,
                decision_object_id,
                policy=policy,
            )
        )
    for safe_route in packet.safe_routes:
        route_object_id = f"object:safe_route:{safe_route.safe_route_id}"
        objects.append(_object_from_safe_route(safe_route, route_object_id, [source_ref], policy))
        relations.append(
            build_model_invocation_trace_relation(
                f"relation:{safe_route.candidate_id}:safe_route:{safe_route.safe_route_id}",
                ModelInvocationTraceRelationType.CANDIDATE_ROUTED_TO_SAFE_ROUTE,
                f"object:candidate:{safe_route.candidate_id}",
                route_object_id,
                policy=policy,
            )
        )
    return build_model_invocation_trace_packet(
        f"trace_packet:{packet.quarantine_packet_id}",
        objects=objects,
        events=events,
        relations=relations,
        source_refs=[source_ref],
        summary="Bounded trace packet from supplied v0.34.5 quarantine packet; no candidate execution.",
    )


def _object_from_candidate(candidate: ModelOutputActionCandidate, object_id: str, source_refs: list[ModelInvocationTraceSourceRef], policy: ModelInvocationTracePolicy) -> ModelInvocationTraceObject:
    return build_model_invocation_trace_object(
        object_id,
        ModelInvocationTraceObjectType.MODEL_OUTPUT_ACTION_CANDIDATE,
        candidate.candidate_id,
        {
            "candidate_kind": str(candidate.candidate_kind),
            "proposed_route": str(candidate.proposed_route),
            "blocked_from_execution": candidate.blocked_from_execution,
            "future_gated": candidate.future_gated,
            "preview_status": "bounded/redacted preview omitted from trace",
        },
        source_refs,
        policy,
    )


def _object_from_decision(decision: ModelOutputActionQuarantineDecision, object_id: str, source_refs: list[ModelInvocationTraceSourceRef], policy: ModelInvocationTracePolicy) -> ModelInvocationTraceObject:
    return build_model_invocation_trace_object(
        object_id,
        ModelInvocationTraceObjectType.MODEL_OUTPUT_QUARANTINE_DECISION,
        decision.decision_id,
        {
            "decision_kind": str(decision.decision_kind),
            "route_kind": str(decision.route_kind),
            "action_execution_allowed": decision.action_execution_allowed,
            "provider_invocation_allowed": decision.provider_invocation_allowed,
        },
        source_refs,
        policy,
    )


def _object_from_safe_route(safe_route: ModelOutputActionSafeRoute, object_id: str, source_refs: list[ModelInvocationTraceSourceRef], policy: ModelInvocationTracePolicy) -> ModelInvocationTraceObject:
    return build_model_invocation_trace_object(
        object_id,
        ModelInvocationTraceObjectType.MODEL_OUTPUT_SAFE_ROUTE,
        safe_route.safe_route_id,
        {
            "route_kind": str(safe_route.route_kind),
            "non_executing": safe_route.non_executing,
            "future_handoff_only": safe_route.future_handoff_only,
            "ready_for_execution": safe_route.ready_for_execution,
        },
        source_refs,
        policy,
    )


def emit_model_invocation_trace_packet(
    emission_input: ModelInvocationTraceEmissionInput,
    emitter: ModelInvocationTraceEmitter,
    supplied_artifacts: dict[str, Any] | None = None,
) -> ModelInvocationTracePacket:
    if not isinstance(emission_input, ModelInvocationTraceEmissionInput):
        raise TypeError("emission_input must be ModelInvocationTraceEmissionInput")
    if not isinstance(emitter, ModelInvocationTraceEmitter):
        raise TypeError("emitter must be ModelInvocationTraceEmitter")
    artifacts = supplied_artifacts or {}
    decision = decide_model_invocation_trace_emission(emission_input, emitter.trace_policy)
    if ModelInvocationTraceDecisionKind(decision.decision_kind) not in {
        ModelInvocationTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION,
        ModelInvocationTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK,
    }:
        return build_model_invocation_trace_packet(
            f"trace_packet:{emission_input.emission_input_id}:blocked",
            status=ModelInvocationTraceStatus.BLOCKED,
            summary="Model invocation trace emission blocked; no sink write occurred.",
            metadata={"decision_id": decision.decision_id},
        )
    if "packet" in artifacts and isinstance(artifacts["packet"], ModelInvocationTracePacket):
        packet = artifacts["packet"]
    elif "model_backed_step_output" in artifacts:
        packet = build_model_invocation_trace_packet_from_model_backed_step_output(artifacts["model_backed_step_output"], emitter.trace_policy)
    elif "provider_boundary_result" in artifacts:
        packet = build_model_invocation_trace_packet_from_provider_boundary_result(artifacts["provider_boundary_result"], emitter.trace_policy)
    elif "quarantine_packet" in artifacts:
        packet = build_model_invocation_trace_packet_from_quarantine_packet(artifacts["quarantine_packet"], emitter.trace_policy)
    else:
        packet = build_model_invocation_trace_packet(
            f"trace_packet:{emission_input.emission_input_id}",
            sink_kind=decision.allowed_sink_kind or ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET,
            summary="Empty model invocation trace packet from supplied in-memory input.",
            metadata={"decision_id": decision.decision_id},
        )
    validation = validate_model_invocation_trace_packet(packet, emitter.trace_policy)
    if not validation.validation_passed:
        return build_model_invocation_trace_packet(
            f"trace_packet:{emission_input.emission_input_id}:validation_blocked",
            status=ModelInvocationTraceStatus.BLOCKED,
            summary="Model invocation trace packet failed validation; unsafe packet was not emitted.",
            metadata={"decision_id": decision.decision_id, "validation_report_id": validation.validation_report_id},
        )
    return packet


def model_invocation_trace_flags_preserve_unsafe_false(flags: ModelInvocationTraceFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES) and flags.production_certified is False


def model_invocation_trace_packet_is_not_persistence(packet: ModelInvocationTracePacket) -> bool:
    return (
        packet.persistent_storage is False
        and packet.ready_for_persistent_write is False
        and packet.ready_for_external_sink is False
        and packet.ready_for_execution is False
        and ModelInvocationTraceSinkKind(packet.sink_kind)
        in {ModelInvocationTraceSinkKind.RETURNED_TRACE_PACKET, ModelInvocationTraceSinkKind.IN_MEMORY_TEST_SINK, ModelInvocationTraceSinkKind.DISABLED}
    )


def model_invocation_trace_policy_blocks_raw_payloads(policy: ModelInvocationTracePolicy) -> bool:
    return (
        policy.allow_raw_prompt is False
        and policy.allow_raw_response is False
        and policy.allow_raw_model_output is False
        and policy.allow_secret_content is False
        and policy.allow_credential_content is False
        and policy.allow_token_content is False
        and policy.allow_full_file_content is False
        and policy.allow_persistent_write is False
        and policy.allow_external_sink is False
    )


def model_invocation_trace_report_is_not_persistent_write(report: ModelInvocationTraceEmissionReport) -> bool:
    return (
        report.ready_for_general_ocel_emission is False
        and report.ready_for_persistent_trace_write is False
        and report.ready_for_external_trace_sink is False
        and report.ready_for_execution is False
    )


def v0347_readiness_report_is_not_execution_ready(report: V0347ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_MODEL_INVOCATION_TRACE_FLAG_NAMES)
