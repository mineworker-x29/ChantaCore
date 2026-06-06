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
from .session_runtime import AgentRuntimeSessionSnapshot
from .step_runner import AgentStepOutput


V0337_VERSION = "v0.33.7"
V0337_RELEASE_NAME = "v0.33.7 Runtime OCEL Trace Emitter"

DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS = [
    ".env",
    "secret",
    "key",
    "token",
    "credential",
    "pem",
    "id_rsa",
]

DEFAULT_PROHIBITED_TRACE_CONTENT = [
    "raw model output",
    "raw tool output",
    "file content",
    "secrets",
    "credentials",
    "tokens",
    "unbounded output",
]

DEFAULT_V0337_PROHIBITED_UNTIL_LATER_GATE = [
    "real model invocation",
    "provider invocation",
    "general agent execution",
    "general tool execution",
    "command execution",
    "network access",
    "credential access",
    "workspace write",
    "code edit",
    "patch application",
    "reference code execution",
    "reference import",
    "dependency install",
    "secret content trace",
    "credential content trace",
    "raw model output persistence",
    "raw tool output persistence",
    "full file content trace",
    "persistent trace write",
    "external trace sink",
    "registry mutation",
    "memory mutation",
    "UI runtime",
    "external control",
    "authority grant",
]


class RuntimeOCELTraceEventKind(StrEnum):
    AGENT_SESSION_CREATED = "agent_session_created"
    AGENT_SESSION_BOUNDARY_ATTACHED = "agent_session_boundary_attached"
    AGENT_PROFILE_ATTACHED = "agent_profile_attached"
    PROMPT_OUTPUT_ATTACHED = "prompt_output_attached"
    AGENT_TURN_CREATED = "agent_turn_created"
    AGENT_STEP_STARTED = "agent_step_started"
    SUPPLIED_MODEL_OUTPUT_ATTACHED = "supplied_model_output_attached"
    ACTION_PROPOSED = "action_proposed"
    ACTION_ALLOWED = "action_allowed"
    ACTION_BLOCKED = "action_blocked"
    SAFE_TOOL_REQUEST_CREATED = "safe_tool_request_created"
    SAFE_TOOL_RESULT_ATTACHED = "safe_tool_result_attached"
    FINAL_RESPONSE_READY = "final_response_ready"
    NO_OP_RECORDED = "no_op_recorded"
    SAFE_FAIL_RECORDED = "safe_fail_recorded"
    AGENT_STEP_COMPLETED = "agent_step_completed"
    AGENT_TURN_COMPLETED = "agent_turn_completed"
    AGENT_SESSION_COMPLETED = "agent_session_completed"
    UNKNOWN = "unknown"


class RuntimeOCELObjectType(StrEnum):
    AGENT_SESSION = "agent_session"
    AGENT_TURN = "agent_turn"
    AGENT_STEP = "agent_step"
    RUNTIME_BOUNDARY = "runtime_boundary"
    RUNTIME_PROFILE = "runtime_profile"
    PROMPT_OUTPUT = "prompt_output"
    SUPPLIED_MODEL_OUTPUT = "supplied_model_output"
    ACTION_PROPOSAL = "action_proposal"
    ACTION_DECISION = "action_decision"
    SAFE_TOOL_REQUEST = "safe_tool_request"
    SAFE_TOOL_RESULT = "safe_tool_result"
    WORKSPACE_INSPECTION_RESULT = "workspace_inspection_result"
    REFERENCE_CONTEXT = "reference_context"
    NO_OP_RECORD = "no_op_record"
    SAFE_FAIL_RECORD = "safe_fail_record"
    UNKNOWN = "unknown"


class RuntimeOCELRelationType(StrEnum):
    SESSION_HAS_TURN = "session_has_turn"
    TURN_HAS_STEP = "turn_has_step"
    STEP_USES_PROFILE = "step_uses_profile"
    STEP_USES_PROMPT = "step_uses_prompt"
    STEP_ATTACHES_MODEL_OUTPUT = "step_attaches_model_output"
    STEP_PROPOSES_ACTION = "step_proposes_action"
    DECISION_EVALUATES_PROPOSAL = "decision_evaluates_proposal"
    DECISION_ALLOWS_SAFE_TOOL = "decision_allows_safe_tool"
    DECISION_BLOCKS_ACTION = "decision_blocks_action"
    SAFE_TOOL_REQUEST_FOR_PROPOSAL = "safe_tool_request_for_proposal"
    SAFE_TOOL_RESULT_FOR_REQUEST = "safe_tool_result_for_request"
    STEP_OBSERVES_TOOL_RESULT = "step_observes_tool_result"
    STEP_PRODUCES_RESPONSE = "step_produces_response"
    SESSION_HAS_TERMINAL_OUTCOME = "session_has_terminal_outcome"
    UNKNOWN = "unknown"


class RuntimeOCELAttributeKind(StrEnum):
    SUMMARY = "summary"
    STATUS = "status"
    DECISION_KIND = "decision_kind"
    RESULT_KIND = "result_kind"
    RISK_KIND = "risk_kind"
    REDACTION_STATUS = "redaction_status"
    BOUNDED_OUTPUT = "bounded_output"
    SOURCE_REF = "source_ref"
    EVIDENCE_REF = "evidence_ref"
    PATH_REF = "path_ref"
    SAFE_TOOL_NAME = "safe_tool_name"
    TOKEN_COUNT_ESTIMATE = "token_count_estimate"
    TIMESTAMP = "timestamp"
    UNKNOWN = "unknown"


class RuntimeOCELTraceSinkKind(StrEnum):
    RETURNED_TRACE_PACKET = "returned_trace_packet"
    IN_MEMORY_TEST_SINK = "in_memory_test_sink"
    DISABLED = "disabled"
    FUTURE_INTERNAL_OCEL_STORE = "future_internal_ocel_store"
    EXTERNAL_TRACE_SINK_BLOCKED = "external_trace_sink_blocked"
    UNKNOWN = "unknown"


class RuntimeOCELTraceStatus(StrEnum):
    UNKNOWN = "unknown"
    PLANNED = "planned"
    POLICY_CHECKED = "policy_checked"
    EMITTED_AS_PACKET = "emitted_as_packet"
    EMITTED_TO_IN_MEMORY_SINK = "emitted_to_in_memory_sink"
    BLOCKED = "blocked"
    SKIPPED = "skipped"
    NO_OP = "no_op"
    SAFE_FAILED = "safe_failed"


class RuntimeOCELTraceDecisionKind(StrEnum):
    ALLOW_TRACE_PACKET_CREATION = "allow_trace_packet_creation"
    ALLOW_IN_MEMORY_TEST_SINK = "allow_in_memory_test_sink"
    DENY = "deny"
    BLOCK = "block"
    SKIP = "skip"
    NO_OP = "no_op"
    ASK_USER_REQUIRED = "ask_user_required"
    REVIEW_REQUIRED = "review_required"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class RuntimeOCELTraceRiskKind(StrEnum):
    RAW_MODEL_OUTPUT_PERSISTENCE_RISK = "raw_model_output_persistence_risk"
    SECRET_CONTENT_TRACE_RISK = "secret_content_trace_risk"
    CREDENTIAL_TRACE_RISK = "credential_trace_risk"
    UNBOUNDED_PAYLOAD_RISK = "unbounded_payload_risk"
    RAW_TOOL_OUTPUT_PERSISTENCE_RISK = "raw_tool_output_persistence_risk"
    FULL_FILE_CONTENT_TRACE_RISK = "full_file_content_trace_risk"
    EXTERNAL_TRACE_SINK_RISK = "external_trace_sink_risk"
    DATABASE_WRITE_RISK = "database_write_risk"
    RUNTIME_LOG_WRITE_RISK = "runtime_log_write_risk"
    REFERENCE_CONTENT_LEAK_RISK = "reference_content_leak_risk"
    EXTERNAL_HARNESS_TRACE_CONFUSION_RISK = "external_harness_trace_confusion_risk"
    PROVIDER_INVOCATION_CONFUSION_RISK = "provider_invocation_confusion_risk"
    UNKNOWN = "unknown"


class RuntimeOCELTraceSourceKind(StrEnum):
    V0336_AGENT_STEP_OUTPUT = "v0336_agent_step_output"
    V0336_AGENT_STEP_EXECUTION_RECORD = "v0336_agent_step_execution_record"
    V0336_ACTION_PROPOSAL = "v0336_action_proposal"
    V0336_ACTION_DECISION = "v0336_action_decision"
    V0336_SAFE_TOOL_RESULT = "v0336_safe_tool_result"
    V0335_WORKSPACE_INSPECTION_RESULT = "v0335_workspace_inspection_result"
    V0333_SESSION_RUNTIME = "v0333_session_runtime"
    V0332_PROMPT_ASSEMBLY = "v0332_prompt_assembly"
    V0331_PROFILE_RUNTIME = "v0331_profile_runtime"
    V0330_RUNTIME_BOUNDARY = "v0330_runtime_boundary"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    OPENCLAW_REFERENCE_CONTEXT_REF = "openclaw_reference_context_ref"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class RuntimeOCELTraceReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    TRACE_CONTRACT_READY = "trace_contract_ready"
    TRACE_PACKET_READY = "trace_packet_ready"
    BOUNDED_INTERNAL_TRACE_EMISSION_READY = "bounded_internal_trace_emission_ready"
    DESIGN_HANDOFF_READY_FOR_V0338 = "design_handoff_ready_for_v0338"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


UNSAFE_RUNTIME_OCEL_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_general_agent_execution",
    "ready_for_real_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_general_tool_execution",
    "ready_for_command_execution",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
    "ready_for_registry_mutation",
    "ready_for_memory_mutation",
    "ready_for_general_ocel_emission",
    "ready_for_persistent_trace_write",
    "ready_for_external_trace_sink",
    "ready_for_ui_runtime",
    "ready_for_external_control",
    "ready_for_authority_grant",
)


def _validate_version_includes_v0337(version: str) -> None:
    _require_non_blank("version", version)
    if V0337_VERSION not in version:
        raise ValueError("version must include v0.33.7")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.33.7")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_non_negative_int(name: str, value: int) -> None:
    if not isinstance(value, int) or value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_source_ref_list(values: list["RuntimeOCELSourceRef"]) -> None:
    _validate_object_list("source_refs", values, RuntimeOCELSourceRef)


def _string_has_prohibited_payload(value: str, patterns: list[str]) -> bool:
    lowered = value.lower()
    return any(pattern.lower() in lowered for pattern in patterns)


def _validate_prohibited_patterns(values: list[str]) -> None:
    _validate_string_list("prohibited_payload_patterns", values)
    lowered = [value.lower() for value in values]
    for required in DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS:
        if required.lower() not in lowered:
            raise ValueError("prohibited_payload_patterns missing v0.33.7 secret-like pattern")


def _validate_trace_attributes(name: str, values: dict[str, Any], max_chars: int = 160) -> None:
    if not isinstance(values, dict):
        raise TypeError(f"{name} must be dict")
    for key, value in values.items():
        if not isinstance(key, str):
            raise TypeError(f"{name} keys must be strings")
        preview = str(value)
        if len(preview) > max_chars:
            raise ValueError(f"{name} values must be bounded")
        if _string_has_prohibited_payload(preview, DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS) and "redacted" not in preview.lower():
            raise ValueError(f"{name} must not include secret-like trace content")


def _bounded_preview(value: Any, policy: "RuntimeOCELTracePolicy") -> tuple[str, bool, bool]:
    if value is None:
        preview = ""
    elif isinstance(value, dict):
        keys = sorted(str(key) for key in value.keys())[:5]
        preview = f"dict(keys={','.join(keys)}, count={len(value)})"
    elif isinstance(value, (list, tuple, set)):
        preview = f"{type(value).__name__}(count={len(value)})"
    else:
        preview = str(value)

    redacted = False
    if _string_has_prohibited_payload(preview, policy.prohibited_payload_patterns):
        preview = "[redacted]"
        redacted = True

    truncated = False
    if len(preview) > policy.max_attribute_chars:
        preview = preview[: max(policy.max_attribute_chars - 14, 0)] + "...[truncated]"
        truncated = True
    return preview, redacted, truncated


@dataclass(frozen=True)
class RuntimeOCELFlagSet:
    flag_set_id: str
    version: str = V0337_VERSION
    trace_emitter_constructed: bool = False
    trace_artifact_creation_enabled: bool = False
    bounded_runtime_ocel_trace_emission_enabled: bool = False
    in_memory_trace_sink_enabled: bool = False
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_bounded_internal_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("flag_set_id", self.flag_set_id)
        _validate_version_includes_v0337(self.version)
        _validate_false(self, UNSAFE_RUNTIME_OCEL_FLAG_NAMES)
        if _metadata_flag_true(self.metadata, {"persistent_trace_write", "external_trace_sink", "provider_invocation"}):
            raise ValueError("RuntimeOCELFlagSet is not persistent/general runtime readiness")


@dataclass(frozen=True)
class RuntimeOCELSourceRef:
    source_ref_id: str
    source_kind: RuntimeOCELTraceSourceKind | str
    source_id: str
    source_summary: str
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        RuntimeOCELTraceSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if _metadata_flag_true(self.metadata, {"fetch", "file_read", "execution"}):
            raise ValueError("RuntimeOCELSourceRef is not fetch, file read, or execution")

    @property
    def fetch(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class RuntimeOCELTracePolicy:
    trace_policy_id: str
    allowed_event_kinds: list[RuntimeOCELTraceEventKind | str] = field(default_factory=list)
    allowed_object_types: list[RuntimeOCELObjectType | str] = field(default_factory=list)
    allowed_relation_types: list[RuntimeOCELRelationType | str] = field(default_factory=list)
    allowed_sink_kinds: list[RuntimeOCELTraceSinkKind | str] = field(default_factory=list)
    prohibited_attribute_kinds: list[RuntimeOCELAttributeKind | str] = field(default_factory=list)
    prohibited_payload_patterns: list[str] = field(default_factory=lambda: list(DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS))
    max_attribute_chars: int = 160
    max_event_count: int = 100
    max_object_count: int = 100
    max_relation_count: int = 100
    allow_raw_model_output: bool = False
    allow_raw_tool_output: bool = False
    allow_file_content: bool = False
    allow_secret_content: bool = False
    allow_credential_content: bool = False
    allow_persistent_write: bool = False
    allow_external_sink: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_policy_id", self.trace_policy_id)
        _validate_enum_list("allowed_event_kinds", self.allowed_event_kinds, RuntimeOCELTraceEventKind)
        _validate_enum_list("allowed_object_types", self.allowed_object_types, RuntimeOCELObjectType)
        _validate_enum_list("allowed_relation_types", self.allowed_relation_types, RuntimeOCELRelationType)
        _validate_enum_list("allowed_sink_kinds", self.allowed_sink_kinds, RuntimeOCELTraceSinkKind)
        _validate_enum_list("prohibited_attribute_kinds", self.prohibited_attribute_kinds, RuntimeOCELAttributeKind)
        _validate_prohibited_patterns(self.prohibited_payload_patterns)
        for name in ("max_attribute_chars", "max_event_count", "max_object_count", "max_relation_count"):
            _validate_non_negative_int(name, getattr(self, name))
        _validate_false(
            self,
            (
                "allow_raw_model_output",
                "allow_raw_tool_output",
                "allow_file_content",
                "allow_secret_content",
                "allow_credential_content",
                "allow_persistent_write",
                "allow_external_sink",
            ),
        )


@dataclass(frozen=True)
class RuntimeOCELObject:
    object_id: str
    object_type: RuntimeOCELObjectType | str
    object_key: str
    attributes: dict[str, Any] = field(default_factory=dict)
    source_refs: list[RuntimeOCELSourceRef] = field(default_factory=list)
    redacted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("object_id", self.object_id)
        RuntimeOCELObjectType(self.object_type)
        _require_non_blank("object_key", self.object_key)
        _validate_trace_attributes("attributes", self.attributes, int(self.metadata.get("max_attribute_chars", 160)))
        _validate_source_ref_list(self.source_refs)


@dataclass(frozen=True)
class RuntimeOCELEvent:
    event_id: str
    event_kind: RuntimeOCELTraceEventKind | str
    event_label: str
    timestamp: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    related_object_ids: list[str] = field(default_factory=list)
    source_refs: list[RuntimeOCELSourceRef] = field(default_factory=list)
    redacted: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("event_id", self.event_id)
        RuntimeOCELTraceEventKind(self.event_kind)
        _require_non_blank("event_label", self.event_label)
        _validate_trace_attributes("attributes", self.attributes, int(self.metadata.get("max_attribute_chars", 160)))
        _validate_string_list("related_object_ids", self.related_object_ids)
        _validate_source_ref_list(self.source_refs)


@dataclass(frozen=True)
class RuntimeOCELRelation:
    relation_id: str
    relation_type: RuntimeOCELRelationType | str
    source_object_id: str
    target_object_id: str
    event_id: str | None = None
    attributes: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("relation_id", self.relation_id)
        RuntimeOCELRelationType(self.relation_type)
        _require_non_blank("source_object_id", self.source_object_id)
        _require_non_blank("target_object_id", self.target_object_id)
        _validate_trace_attributes("attributes", self.attributes, int(self.metadata.get("max_attribute_chars", 160)))


@dataclass(frozen=True)
class RuntimeOCELAttribute:
    attribute_id: str
    attribute_kind: RuntimeOCELAttributeKind | str
    key: str
    value_preview: str
    redacted: bool = False
    truncated: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("attribute_id", self.attribute_id)
        RuntimeOCELAttributeKind(self.attribute_kind)
        _require_non_blank("key", self.key)
        if len(self.value_preview) > int(self.metadata.get("max_attribute_chars", 160)):
            raise ValueError("value_preview must be bounded")
        if _string_has_prohibited_payload(self.value_preview, DEFAULT_TRACE_PROHIBITED_PAYLOAD_PATTERNS) and not self.redacted:
            raise ValueError("attribute must not contain raw secret or unbounded content")


@dataclass(frozen=True)
class RuntimeOCELTracePacket:
    trace_packet_id: str
    version: str
    sink_kind: RuntimeOCELTraceSinkKind | str
    objects: list[RuntimeOCELObject] = field(default_factory=list)
    events: list[RuntimeOCELEvent] = field(default_factory=list)
    relations: list[RuntimeOCELRelation] = field(default_factory=list)
    attributes: list[RuntimeOCELAttribute] = field(default_factory=list)
    source_refs: list[RuntimeOCELSourceRef] = field(default_factory=list)
    status: RuntimeOCELTraceStatus | str = RuntimeOCELTraceStatus.EMITTED_AS_PACKET
    redaction_applied: bool = False
    truncated: bool = False
    summary: str = "Returned bounded runtime OCEL trace packet artifact."
    ready_for_persistent_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("trace_packet_id", self.trace_packet_id)
        _validate_version_includes_v0337(self.version)
        RuntimeOCELTraceSinkKind(self.sink_kind)
        _validate_object_list("objects", self.objects, RuntimeOCELObject)
        _validate_object_list("events", self.events, RuntimeOCELEvent)
        _validate_object_list("relations", self.relations, RuntimeOCELRelation)
        _validate_object_list("attributes", self.attributes, RuntimeOCELAttribute)
        _validate_source_ref_list(self.source_refs)
        RuntimeOCELTraceStatus(self.status)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_persistent_write", "ready_for_external_sink", "ready_for_execution"))


@dataclass(frozen=True)
class RuntimeOCELTraceEmissionInput:
    emission_input_id: str
    source_version: str
    agent_step_output_id: str | None = None
    agent_step_execution_record_id: str | None = None
    session_id: str | None = None
    turn_id: str | None = None
    prompt_output_id: str | None = None
    runtime_profile_id: str | None = None
    source_refs: list[RuntimeOCELSourceRef] = field(default_factory=list)
    requested_sink_kind: RuntimeOCELTraceSinkKind | str = RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET
    task_summary: str = "Create bounded internal runtime OCEL trace artifact."
    prohibited_trace_content: list[str] = field(default_factory=lambda: list(DEFAULT_PROHIBITED_TRACE_CONTENT))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emission_input_id", self.emission_input_id)
        _validate_version_includes_v0337(self.source_version)
        _validate_source_ref_list(self.source_refs)
        RuntimeOCELTraceSinkKind(self.requested_sink_kind)
        _require_non_blank("task_summary", self.task_summary)
        _validate_string_list("prohibited_trace_content", self.prohibited_trace_content)
        lowered = [value.lower() for value in self.prohibited_trace_content]
        for required in DEFAULT_PROHIBITED_TRACE_CONTENT:
            if required.lower() not in lowered:
                raise ValueError("prohibited_trace_content missing v0.33.7 raw/secret/unbounded prohibition")
        if _metadata_flag_true(self.metadata, {"provider_execution", "tool_execution"}):
            raise ValueError("RuntimeOCELTraceEmissionInput is not provider/tool execution request")


@dataclass(frozen=True)
class RuntimeOCELTraceEmissionDecision:
    decision_id: str
    emission_input_id: str
    decision_kind: RuntimeOCELTraceDecisionKind | str
    reason: str
    allowed_sink_kind: RuntimeOCELTraceSinkKind | str | None = None
    risk_kinds: list[RuntimeOCELTraceRiskKind | str] = field(default_factory=list)
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
        RuntimeOCELTraceDecisionKind(self.decision_kind)
        _require_non_blank("reason", self.reason)
        if self.allowed_sink_kind is not None:
            RuntimeOCELTraceSinkKind(self.allowed_sink_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, RuntimeOCELTraceRiskKind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_false(self, ("persistent_write_allowed", "external_sink_allowed", "ready_for_execution"))


@dataclass(frozen=True)
class RuntimeOCELTraceValidationReport:
    validation_report_id: str
    trace_packet_id: str | None = None
    checked_event_ids: list[str] = field(default_factory=list)
    checked_object_ids: list[str] = field(default_factory=list)
    checked_relation_ids: list[str] = field(default_factory=list)
    risk_kinds: list[RuntimeOCELTraceRiskKind | str] = field(default_factory=list)
    redacted_field_count: int = 0
    truncated_field_count: int = 0
    blocked_items: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    validation_passed: bool = True
    summary: str = "Runtime OCEL trace packet validation report."
    ready_for_persistent_write: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        for name in ("checked_event_ids", "checked_object_ids", "checked_relation_ids", "blocked_items", "warnings"):
            _validate_string_list(name, getattr(self, name))
        _validate_enum_list("risk_kinds", self.risk_kinds, RuntimeOCELTraceRiskKind)
        _validate_non_negative_int("redacted_field_count", self.redacted_field_count)
        _validate_non_negative_int("truncated_field_count", self.truncated_field_count)
        if self.blocked_items and self.validation_passed:
            raise ValueError("validation_passed cannot be True if blocked_items non-empty")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_persistent_write", "ready_for_execution"))


@dataclass(frozen=True)
class RuntimeOCELTraceEmissionReport:
    report_id: str
    version: str
    emission_input_id: str
    trace_packet_id: str | None = None
    validation_report_id: str | None = None
    status: RuntimeOCELTraceStatus | str = RuntimeOCELTraceStatus.EMITTED_AS_PACKET
    readiness_level: RuntimeOCELTraceReadinessLevel | str = RuntimeOCELTraceReadinessLevel.TRACE_PACKET_READY
    summary: str = "Runtime OCEL trace emission report."
    event_count: int = 0
    object_count: int = 0
    relation_count: int = 0
    redacted_field_count: int = 0
    truncated_field_count: int = 0
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_bounded_internal_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0337(self.version)
        _require_non_blank("emission_input_id", self.emission_input_id)
        RuntimeOCELTraceStatus(self.status)
        RuntimeOCELTraceReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("event_count", "object_count", "relation_count", "redacted_field_count", "truncated_field_count"):
            _validate_non_negative_int(name, getattr(self, name))
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_false(self, ("ready_for_general_ocel_emission", "ready_for_persistent_trace_write", "ready_for_external_trace_sink", "ready_for_execution"))
        if self.ready_for_bounded_internal_ocel_trace_emission and self.blocked_items:
            raise ValueError("bounded trace emission readiness is not allowed with blocked_items")


@dataclass(frozen=True)
class RuntimeOCELTraceEmitter:
    emitter_id: str
    version: str
    supported_event_kinds: list[RuntimeOCELTraceEventKind | str]
    supported_object_types: list[RuntimeOCELObjectType | str]
    supported_relation_types: list[RuntimeOCELRelationType | str]
    supported_sink_kinds: list[RuntimeOCELTraceSinkKind | str]
    trace_policy: RuntimeOCELTracePolicy
    flags: RuntimeOCELFlagSet
    summary: str = "Bounded internal runtime OCEL trace emitter."
    ready_for_bounded_internal_trace_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_sink: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("emitter_id", self.emitter_id)
        _validate_version_includes_v0337(self.version)
        _validate_enum_list("supported_event_kinds", self.supported_event_kinds, RuntimeOCELTraceEventKind)
        _validate_enum_list("supported_object_types", self.supported_object_types, RuntimeOCELObjectType)
        _validate_enum_list("supported_relation_types", self.supported_relation_types, RuntimeOCELRelationType)
        _validate_enum_list("supported_sink_kinds", self.supported_sink_kinds, RuntimeOCELTraceSinkKind)
        if not isinstance(self.trace_policy, RuntimeOCELTracePolicy):
            raise TypeError("trace_policy must be RuntimeOCELTracePolicy")
        if not isinstance(self.flags, RuntimeOCELFlagSet):
            raise TypeError("flags must be RuntimeOCELFlagSet")
        if not runtime_ocel_flags_preserve_unsafe_runtime_false(self.flags):
            raise ValueError("flags must preserve unsafe readiness false")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_persistent_trace_write", "ready_for_external_sink", "ready_for_execution"))


@dataclass(frozen=True)
class RuntimeOCELRunPreview:
    run_preview_id: str
    emitter_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["policy check", "sanitize attributes", "return trace packet"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["RuntimeOCELTracePacket", "RuntimeOCELTraceValidationReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_V0337_PROHIBITED_UNTIL_LATER_GATE))
    no_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_workspace_inspection_execution_guarantee: bool = True
    no_file_read_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_reference_dependency_install_guarantee: bool = True
    no_secret_content_trace_guarantee: bool = True
    no_raw_output_persistence_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_external_trace_sink_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")


@dataclass(frozen=True)
class RuntimeOCELNoExternalSideEffectGuarantee:
    guarantee_id: str
    version: str
    no_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_agent_step_execution: bool = True
    no_tool_execution: bool = True
    no_workspace_inspection_execution: bool = True
    no_file_read: bool = True
    no_command_execution: bool = True
    no_subprocess: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_file_creation: bool = True
    no_file_deletion: bool = True
    no_file_rename: bool = True
    no_chmod_chown: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_secret_content_trace: bool = True
    no_credential_content_trace: bool = True
    no_raw_model_output_persistence: bool = True
    no_raw_tool_output_persistence: bool = True
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
        _validate_version_includes_v0337(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True")
        _validate_string_list("evidence_refs", self.evidence_refs)


@dataclass(frozen=True)
class V0337ReadinessReport:
    report_id: str
    version: str
    emitter_id: str | None = None
    trace_packet_id: str | None = None
    trace_emission_report_id: str | None = None
    validation_report_id: str | None = None
    summary: str = "v0.33.7 bounded internal runtime OCEL trace artifact readiness report."
    bounded_runtime_ocel_trace_emission_enabled: bool = False
    trace_artifact_creation_enabled: bool = False
    ready_for_v0338_cli_agent_run_surface: bool = False
    ready_for_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
    ready_for_registry_mutation: bool = False
    ready_for_memory_mutation: bool = False
    ready_for_bounded_internal_ocel_trace_emission: bool = False
    ready_for_general_ocel_emission: bool = False
    ready_for_persistent_trace_write: bool = False
    ready_for_external_trace_sink: bool = False
    ready_for_ui_runtime: bool = False
    ready_for_external_control: bool = False
    ready_for_authority_grant: bool = False
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_V0337_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0337(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_RUNTIME_OCEL_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        lowered = [value.lower() for value in self.prohibited_until_later_gate]
        for required in DEFAULT_V0337_PROHIBITED_UNTIL_LATER_GATE:
            if required.lower() not in lowered:
                raise ValueError("prohibited_until_later_gate missing v0.33.7 prohibition")
        if self.ready_for_bounded_internal_ocel_trace_emission and self.blocked_items:
            raise ValueError("bounded trace readiness is not allowed with blocked_items")


def default_runtime_ocel_trace_policy() -> RuntimeOCELTracePolicy:
    return RuntimeOCELTracePolicy(
        trace_policy_id="runtime_ocel_trace_policy:v0.33.7",
        allowed_event_kinds=[item for item in RuntimeOCELTraceEventKind if item != RuntimeOCELTraceEventKind.UNKNOWN],
        allowed_object_types=[item for item in RuntimeOCELObjectType if item != RuntimeOCELObjectType.UNKNOWN],
        allowed_relation_types=[item for item in RuntimeOCELRelationType if item != RuntimeOCELRelationType.UNKNOWN],
        allowed_sink_kinds=[
            RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET,
            RuntimeOCELTraceSinkKind.IN_MEMORY_TEST_SINK,
            RuntimeOCELTraceSinkKind.DISABLED,
        ],
    )


def build_runtime_ocel_flags(flag_set_id: str = "runtime_ocel_flags:v0.33.7", **kwargs: Any) -> RuntimeOCELFlagSet:
    return RuntimeOCELFlagSet(flag_set_id=flag_set_id, version=V0337_VERSION, **kwargs)


def build_runtime_ocel_source_ref(
    source_ref_id: str,
    source_kind: RuntimeOCELTraceSourceKind | str = RuntimeOCELTraceSourceKind.TEST_FIXTURE,
    source_id: str = "test_fixture",
    source_summary: str = "Provided in-memory trace source.",
    **kwargs: Any,
) -> RuntimeOCELSourceRef:
    return RuntimeOCELSourceRef(source_ref_id=source_ref_id, source_kind=source_kind, source_id=source_id, source_summary=source_summary, **kwargs)


def build_runtime_ocel_trace_policy(trace_policy_id: str = "runtime_ocel_trace_policy:v0.33.7", **kwargs: Any) -> RuntimeOCELTracePolicy:
    defaults = default_runtime_ocel_trace_policy()
    return RuntimeOCELTracePolicy(
        trace_policy_id=trace_policy_id,
        allowed_event_kinds=kwargs.pop("allowed_event_kinds", list(defaults.allowed_event_kinds)),
        allowed_object_types=kwargs.pop("allowed_object_types", list(defaults.allowed_object_types)),
        allowed_relation_types=kwargs.pop("allowed_relation_types", list(defaults.allowed_relation_types)),
        allowed_sink_kinds=kwargs.pop("allowed_sink_kinds", list(defaults.allowed_sink_kinds)),
        **kwargs,
    )


def _sanitize_attributes(values: dict[str, Any], policy: RuntimeOCELTracePolicy) -> tuple[dict[str, str], bool, bool]:
    sanitized: dict[str, str] = {}
    redacted = False
    truncated = False
    for key, value in values.items():
        preview, was_redacted, was_truncated = _bounded_preview(value, policy)
        sanitized[str(key)] = preview
        redacted = redacted or was_redacted
        truncated = truncated or was_truncated
    return sanitized, redacted, truncated


def build_runtime_ocel_object(
    object_id: str,
    object_type: RuntimeOCELObjectType | str,
    object_key: str,
    attributes: dict[str, Any] | None = None,
    source_refs: list[RuntimeOCELSourceRef] | None = None,
    policy: RuntimeOCELTracePolicy | None = None,
    **kwargs: Any,
) -> RuntimeOCELObject:
    active_policy = policy or default_runtime_ocel_trace_policy()
    sanitized, redacted, _ = _sanitize_attributes(attributes or {}, active_policy)
    return RuntimeOCELObject(
        object_id=object_id,
        object_type=object_type,
        object_key=object_key,
        attributes=sanitized,
        source_refs=source_refs or [],
        redacted=kwargs.pop("redacted", redacted),
        metadata={**kwargs.pop("metadata", {}), "max_attribute_chars": active_policy.max_attribute_chars},
        **kwargs,
    )


def build_runtime_ocel_event(
    event_id: str,
    event_kind: RuntimeOCELTraceEventKind | str,
    event_label: str,
    attributes: dict[str, Any] | None = None,
    related_object_ids: list[str] | None = None,
    source_refs: list[RuntimeOCELSourceRef] | None = None,
    policy: RuntimeOCELTracePolicy | None = None,
    **kwargs: Any,
) -> RuntimeOCELEvent:
    active_policy = policy or default_runtime_ocel_trace_policy()
    sanitized, redacted, _ = _sanitize_attributes(attributes or {}, active_policy)
    return RuntimeOCELEvent(
        event_id=event_id,
        event_kind=event_kind,
        event_label=event_label,
        attributes=sanitized,
        related_object_ids=related_object_ids or [],
        source_refs=source_refs or [],
        redacted=kwargs.pop("redacted", redacted),
        metadata={**kwargs.pop("metadata", {}), "max_attribute_chars": active_policy.max_attribute_chars},
        **kwargs,
    )


def build_runtime_ocel_relation(
    relation_id: str,
    relation_type: RuntimeOCELRelationType | str,
    source_object_id: str,
    target_object_id: str,
    attributes: dict[str, Any] | None = None,
    policy: RuntimeOCELTracePolicy | None = None,
    **kwargs: Any,
) -> RuntimeOCELRelation:
    active_policy = policy or default_runtime_ocel_trace_policy()
    sanitized, _, _ = _sanitize_attributes(attributes or {}, active_policy)
    return RuntimeOCELRelation(
        relation_id=relation_id,
        relation_type=relation_type,
        source_object_id=source_object_id,
        target_object_id=target_object_id,
        attributes=sanitized,
        metadata={**kwargs.pop("metadata", {}), "max_attribute_chars": active_policy.max_attribute_chars},
        **kwargs,
    )


def build_runtime_ocel_attribute(
    attribute_id: str,
    attribute_kind: RuntimeOCELAttributeKind | str,
    key: str,
    value_preview: str,
    policy: RuntimeOCELTracePolicy | None = None,
    **kwargs: Any,
) -> RuntimeOCELAttribute:
    active_policy = policy or default_runtime_ocel_trace_policy()
    preview, redacted, truncated = _bounded_preview(value_preview, active_policy)
    return RuntimeOCELAttribute(
        attribute_id=attribute_id,
        attribute_kind=attribute_kind,
        key=key,
        value_preview=preview,
        redacted=kwargs.pop("redacted", redacted),
        truncated=kwargs.pop("truncated", truncated),
        metadata={**kwargs.pop("metadata", {}), "max_attribute_chars": active_policy.max_attribute_chars},
        **kwargs,
    )


def build_runtime_ocel_trace_packet(
    trace_packet_id: str,
    sink_kind: RuntimeOCELTraceSinkKind | str = RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET,
    **kwargs: Any,
) -> RuntimeOCELTracePacket:
    return RuntimeOCELTracePacket(trace_packet_id=trace_packet_id, version=V0337_VERSION, sink_kind=sink_kind, **kwargs)


def build_runtime_ocel_trace_emission_input(emission_input_id: str, **kwargs: Any) -> RuntimeOCELTraceEmissionInput:
    return RuntimeOCELTraceEmissionInput(emission_input_id=emission_input_id, source_version=V0337_VERSION, **kwargs)


def build_runtime_ocel_trace_emission_decision(
    decision_id: str,
    emission_input_id: str,
    decision_kind: RuntimeOCELTraceDecisionKind | str,
    reason: str,
    **kwargs: Any,
) -> RuntimeOCELTraceEmissionDecision:
    return RuntimeOCELTraceEmissionDecision(
        decision_id=decision_id,
        emission_input_id=emission_input_id,
        decision_kind=decision_kind,
        reason=reason,
        **kwargs,
    )


def build_runtime_ocel_trace_validation_report(validation_report_id: str, **kwargs: Any) -> RuntimeOCELTraceValidationReport:
    return RuntimeOCELTraceValidationReport(validation_report_id=validation_report_id, **kwargs)


def build_runtime_ocel_trace_emission_report(report_id: str, emission_input_id: str, **kwargs: Any) -> RuntimeOCELTraceEmissionReport:
    return RuntimeOCELTraceEmissionReport(report_id=report_id, version=V0337_VERSION, emission_input_id=emission_input_id, **kwargs)


def build_runtime_ocel_trace_emitter(emitter_id: str = "runtime_ocel_trace_emitter:v0.33.7", **kwargs: Any) -> RuntimeOCELTraceEmitter:
    policy = kwargs.pop("trace_policy", default_runtime_ocel_trace_policy())
    flags = kwargs.pop(
        "flags",
        build_runtime_ocel_flags(
            trace_emitter_constructed=True,
            trace_artifact_creation_enabled=True,
            bounded_runtime_ocel_trace_emission_enabled=True,
            ready_for_v0338_cli_agent_run_surface=True,
            ready_for_bounded_internal_ocel_trace_emission=True,
        ),
    )
    return RuntimeOCELTraceEmitter(
        emitter_id=emitter_id,
        version=V0337_VERSION,
        supported_event_kinds=kwargs.pop("supported_event_kinds", list(policy.allowed_event_kinds)),
        supported_object_types=kwargs.pop("supported_object_types", list(policy.allowed_object_types)),
        supported_relation_types=kwargs.pop("supported_relation_types", list(policy.allowed_relation_types)),
        supported_sink_kinds=kwargs.pop("supported_sink_kinds", list(policy.allowed_sink_kinds)),
        trace_policy=policy,
        flags=flags,
        ready_for_bounded_internal_trace_emission=kwargs.pop("ready_for_bounded_internal_trace_emission", True),
        **kwargs,
    )


def build_runtime_ocel_run_preview(run_preview_id: str, **kwargs: Any) -> RuntimeOCELRunPreview:
    return RuntimeOCELRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_runtime_ocel_no_external_side_effect_guarantee(
    guarantee_id: str = "runtime_ocel_no_external_side_effect:v0.33.7",
    **kwargs: Any,
) -> RuntimeOCELNoExternalSideEffectGuarantee:
    return RuntimeOCELNoExternalSideEffectGuarantee(guarantee_id=guarantee_id, version=V0337_VERSION, **kwargs)


def build_v0337_readiness_report(report_id: str = "v0337_readiness_report", **kwargs: Any) -> V0337ReadinessReport:
    return V0337ReadinessReport(report_id=report_id, version=V0337_VERSION, **kwargs)


def sanitize_runtime_ocel_attribute_value(value: Any, policy: RuntimeOCELTracePolicy) -> RuntimeOCELAttribute:
    if not isinstance(policy, RuntimeOCELTracePolicy):
        raise TypeError("policy must be RuntimeOCELTracePolicy")
    preview, redacted, truncated = _bounded_preview(value, policy)
    return RuntimeOCELAttribute(
        attribute_id="runtime_ocel_attribute:sanitized",
        attribute_kind=RuntimeOCELAttributeKind.BOUNDED_OUTPUT,
        key="value",
        value_preview=preview,
        redacted=redacted,
        truncated=truncated,
        metadata={"max_attribute_chars": policy.max_attribute_chars},
    )


def validate_runtime_ocel_trace_packet(packet: RuntimeOCELTracePacket, policy: RuntimeOCELTracePolicy) -> RuntimeOCELTraceValidationReport:
    if not isinstance(packet, RuntimeOCELTracePacket):
        raise TypeError("packet must be RuntimeOCELTracePacket")
    if not isinstance(policy, RuntimeOCELTracePolicy):
        raise TypeError("policy must be RuntimeOCELTracePolicy")

    blocked_items: list[str] = []
    warnings: list[str] = []
    risks: list[RuntimeOCELTraceRiskKind | str] = []
    if len(packet.events) > policy.max_event_count:
        blocked_items.append("event_count_exceeds_policy")
        risks.append(RuntimeOCELTraceRiskKind.UNBOUNDED_PAYLOAD_RISK)
    if len(packet.objects) > policy.max_object_count:
        blocked_items.append("object_count_exceeds_policy")
        risks.append(RuntimeOCELTraceRiskKind.UNBOUNDED_PAYLOAD_RISK)
    if len(packet.relations) > policy.max_relation_count:
        blocked_items.append("relation_count_exceeds_policy")
        risks.append(RuntimeOCELTraceRiskKind.UNBOUNDED_PAYLOAD_RISK)
    if packet.ready_for_persistent_write or packet.ready_for_external_sink or packet.ready_for_execution:
        blocked_items.append("packet_ready_for_forbidden_sink_or_execution")
        risks.append(RuntimeOCELTraceRiskKind.EXTERNAL_TRACE_SINK_RISK)

    redacted_count = sum(1 for attribute in packet.attributes if attribute.redacted)
    truncated_count = sum(1 for attribute in packet.attributes if attribute.truncated)

    for attribute in packet.attributes:
        if _string_has_prohibited_payload(attribute.value_preview, policy.prohibited_payload_patterns) and not attribute.redacted:
            blocked_items.append(f"unsafe_attribute:{attribute.attribute_id}")
            risks.append(RuntimeOCELTraceRiskKind.SECRET_CONTENT_TRACE_RISK)
        if len(attribute.value_preview) > policy.max_attribute_chars:
            blocked_items.append(f"unbounded_attribute:{attribute.attribute_id}")
            risks.append(RuntimeOCELTraceRiskKind.UNBOUNDED_PAYLOAD_RISK)

    for event in packet.events:
        if RuntimeOCELTraceEventKind(event.event_kind) not in policy.allowed_event_kinds:
            blocked_items.append(f"event_kind_not_allowed:{event.event_id}")
        for key, value in event.attributes.items():
            if _string_has_prohibited_payload(str(value), policy.prohibited_payload_patterns) and "redacted" not in str(value).lower():
                blocked_items.append(f"unsafe_event_attribute:{event.event_id}:{key}")
                risks.append(RuntimeOCELTraceRiskKind.SECRET_CONTENT_TRACE_RISK)

    for obj in packet.objects:
        if RuntimeOCELObjectType(obj.object_type) not in policy.allowed_object_types:
            blocked_items.append(f"object_type_not_allowed:{obj.object_id}")
        for key, value in obj.attributes.items():
            if _string_has_prohibited_payload(str(value), policy.prohibited_payload_patterns) and "redacted" not in str(value).lower():
                blocked_items.append(f"unsafe_object_attribute:{obj.object_id}:{key}")
                risks.append(RuntimeOCELTraceRiskKind.SECRET_CONTENT_TRACE_RISK)

    for relation in packet.relations:
        if RuntimeOCELRelationType(relation.relation_type) not in policy.allowed_relation_types:
            blocked_items.append(f"relation_type_not_allowed:{relation.relation_id}")

    validation_passed = not blocked_items
    return build_runtime_ocel_trace_validation_report(
        f"{packet.trace_packet_id}:validation",
        trace_packet_id=packet.trace_packet_id,
        checked_event_ids=[event.event_id for event in packet.events],
        checked_object_ids=[obj.object_id for obj in packet.objects],
        checked_relation_ids=[relation.relation_id for relation in packet.relations],
        risk_kinds=list(dict.fromkeys(risks)),
        redacted_field_count=redacted_count,
        truncated_field_count=truncated_count,
        blocked_items=blocked_items,
        warnings=warnings,
        validation_passed=validation_passed,
        summary="Runtime OCEL trace packet passed policy validation." if validation_passed else "Runtime OCEL trace packet was blocked by policy validation.",
    )


def _source_ref_for_step_output(step_output: AgentStepOutput) -> RuntimeOCELSourceRef:
    return build_runtime_ocel_source_ref(
        f"source:{step_output.step_output_id}",
        RuntimeOCELTraceSourceKind.V0336_AGENT_STEP_OUTPUT,
        step_output.step_output_id,
        "v0.33.6 in-memory AgentStepOutput artifact.",
    )


def build_runtime_ocel_packet_from_agent_step_output(
    step_output: AgentStepOutput,
    policy: RuntimeOCELTracePolicy,
) -> RuntimeOCELTracePacket:
    if not isinstance(step_output, AgentStepOutput):
        raise TypeError("step_output must be AgentStepOutput")
    if not isinstance(policy, RuntimeOCELTracePolicy):
        raise TypeError("policy must be RuntimeOCELTracePolicy")

    source_ref = _source_ref_for_step_output(step_output)
    step_object_id = f"object:agent_step:{step_output.step_input_id}"
    execution_record_object_id = f"object:agent_step_record:{step_output.execution_record.execution_record_id}"
    objects = [
        build_runtime_ocel_object(
            step_object_id,
            RuntimeOCELObjectType.AGENT_STEP,
            step_output.step_input_id,
            {
                "status": str(step_output.status),
                "result_kind": str(step_output.result_kind),
                "summary": step_output.summary,
                "final_response_present": step_output.final_response_text is not None,
                "final_response_chars": len(step_output.final_response_text or ""),
            },
            [source_ref],
            policy,
        ),
        build_runtime_ocel_object(
            execution_record_object_id,
            RuntimeOCELObjectType.AGENT_STEP,
            step_output.execution_record.execution_record_id,
            {
                "status": str(step_output.execution_record.status),
                "executed_bounded_step": step_output.execution_record.executed_bounded_step,
                "executed_real_model_call": step_output.execution_record.executed_real_model_call,
                "executed_general_tool_call": step_output.execution_record.executed_general_tool_call,
            },
            [source_ref],
            policy,
        ),
    ]
    events = [
        build_runtime_ocel_event(
            f"event:{step_output.step_output_id}:started",
            RuntimeOCELTraceEventKind.AGENT_STEP_STARTED,
            "Agent step trace started",
            {"status": str(step_output.status), "bounded_output": True},
            [step_object_id],
            [source_ref],
            policy,
        )
    ]
    relations: list[RuntimeOCELRelation] = []

    if step_output.action_proposal is not None:
        proposal_object_id = f"object:action_proposal:{step_output.action_proposal.proposal_id}"
        objects.append(
            build_runtime_ocel_object(
                proposal_object_id,
                RuntimeOCELObjectType.ACTION_PROPOSAL,
                step_output.action_proposal.proposal_id,
                {
                    "proposal_kind": str(step_output.action_proposal.proposal_kind),
                    "proposed_tool_name": step_output.action_proposal.proposed_tool_name or "",
                    "risk_count": len(step_output.action_proposal.risk_kinds),
                },
                [source_ref],
                policy,
            )
        )
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:action_proposed",
                RuntimeOCELTraceEventKind.ACTION_PROPOSED,
                "Action proposal attached",
                {"proposal_kind": str(step_output.action_proposal.proposal_kind)},
                [step_object_id, proposal_object_id],
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_runtime_ocel_relation(
                f"relation:{step_output.step_output_id}:step_proposes_action",
                RuntimeOCELRelationType.STEP_PROPOSES_ACTION,
                step_object_id,
                proposal_object_id,
                policy=policy,
            )
        )

    if step_output.action_decision is not None:
        decision_object_id = f"object:action_decision:{step_output.action_decision.decision_id}"
        objects.append(
            build_runtime_ocel_object(
                decision_object_id,
                RuntimeOCELObjectType.ACTION_DECISION,
                step_output.action_decision.decision_id,
                {
                    "decision_kind": str(step_output.action_decision.decision_kind),
                    "allowed_tool_name": step_output.action_decision.allowed_tool_name or "",
                    "block_reason_count": len(step_output.action_decision.block_reasons),
                },
                [source_ref],
                policy,
            )
        )
        decision_allowed = step_output.action_decision.execution_allowed or str(step_output.action_decision.decision_kind) == "allow_final_response"
        event_kind = RuntimeOCELTraceEventKind.ACTION_ALLOWED if decision_allowed else RuntimeOCELTraceEventKind.ACTION_BLOCKED
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:action_decision",
                event_kind,
                "Action decision attached",
                {"decision_kind": str(step_output.action_decision.decision_kind)},
                [step_object_id, decision_object_id],
                [source_ref],
                policy,
            )
        )
        if step_output.action_proposal is not None:
            proposal_object_id = f"object:action_proposal:{step_output.action_proposal.proposal_id}"
            relations.append(
                build_runtime_ocel_relation(
                    f"relation:{step_output.step_output_id}:decision_evaluates_proposal",
                    RuntimeOCELRelationType.DECISION_EVALUATES_PROPOSAL,
                    decision_object_id,
                    proposal_object_id,
                    policy=policy,
                )
            )
            relation_kind = RuntimeOCELRelationType.DECISION_ALLOWS_SAFE_TOOL if step_output.action_decision.execution_allowed else RuntimeOCELRelationType.DECISION_BLOCKS_ACTION
            relations.append(
                build_runtime_ocel_relation(
                    f"relation:{step_output.step_output_id}:decision_outcome",
                    relation_kind,
                    decision_object_id,
                    proposal_object_id,
                    policy=policy,
                )
            )

    if step_output.safe_tool_result is not None:
        safe_tool_request_object_id = f"object:safe_tool_request:{step_output.safe_tool_result.safe_tool_request_id}"
        safe_tool_object_id = f"object:safe_tool_result:{step_output.safe_tool_result.safe_tool_result_id}"
        objects.append(
            build_runtime_ocel_object(
                safe_tool_request_object_id,
                RuntimeOCELObjectType.SAFE_TOOL_REQUEST,
                step_output.safe_tool_result.safe_tool_request_id,
                {
                    "tool_name": step_output.safe_tool_result.tool_name,
                    "bounded_readonly": step_output.safe_tool_result.bounded_readonly,
                },
                [source_ref],
                policy,
            )
        )
        objects.append(
            build_runtime_ocel_object(
                safe_tool_object_id,
                RuntimeOCELObjectType.SAFE_TOOL_RESULT,
                step_output.safe_tool_result.safe_tool_result_id,
                {
                    "tool_name": step_output.safe_tool_result.tool_name,
                    "result_kind": str(step_output.safe_tool_result.result_kind),
                    "bounded_readonly": step_output.safe_tool_result.bounded_readonly,
                    "skipped_or_denied": step_output.safe_tool_result.skipped_or_denied,
                    "workspace_inspection_result_ref": step_output.safe_tool_result.workspace_inspection_result_ref or "",
                },
                [source_ref],
                policy,
            )
        )
        if step_output.safe_tool_result.workspace_inspection_result_ref is not None:
            workspace_object_id = f"object:workspace_inspection_result:{step_output.safe_tool_result.workspace_inspection_result_ref}"
            objects.append(
                build_runtime_ocel_object(
                    workspace_object_id,
                    RuntimeOCELObjectType.WORKSPACE_INSPECTION_RESULT,
                    step_output.safe_tool_result.workspace_inspection_result_ref,
                    {
                        "summary": "Workspace inspection result ref only; no tool output copied.",
                        "bounded_output": True,
                    },
                    [source_ref],
                    policy,
                )
            )
            relations.append(
                build_runtime_ocel_relation(
                    f"relation:{step_output.step_output_id}:tool_result_workspace_ref",
                    RuntimeOCELRelationType.STEP_OBSERVES_TOOL_RESULT,
                    safe_tool_object_id,
                    workspace_object_id,
                    policy=policy,
                )
            )
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:safe_tool_request",
                RuntimeOCELTraceEventKind.SAFE_TOOL_REQUEST_CREATED,
                "Safe tool request summary attached",
                {"safe_tool_name": step_output.safe_tool_result.tool_name, "bounded_output": True},
                [step_object_id, safe_tool_request_object_id],
                [source_ref],
                policy,
            )
        )
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:safe_tool_result",
                RuntimeOCELTraceEventKind.SAFE_TOOL_RESULT_ATTACHED,
                "Safe tool result summary attached",
                {"safe_tool_name": step_output.safe_tool_result.tool_name, "bounded_output": True},
                [step_object_id, safe_tool_object_id],
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_runtime_ocel_relation(
                f"relation:{step_output.step_output_id}:safe_tool_result_for_request",
                RuntimeOCELRelationType.SAFE_TOOL_RESULT_FOR_REQUEST,
                safe_tool_request_object_id,
                safe_tool_object_id,
                policy=policy,
            )
        )
        relations.append(
            build_runtime_ocel_relation(
                f"relation:{step_output.step_output_id}:step_observes_tool_result",
                RuntimeOCELRelationType.STEP_OBSERVES_TOOL_RESULT,
                step_object_id,
                safe_tool_object_id,
                policy=policy,
            )
        )
        if step_output.action_proposal is not None:
            proposal_object_id = f"object:action_proposal:{step_output.action_proposal.proposal_id}"
            relations.append(
                build_runtime_ocel_relation(
                    f"relation:{step_output.step_output_id}:safe_tool_request_for_proposal",
                    RuntimeOCELRelationType.SAFE_TOOL_REQUEST_FOR_PROPOSAL,
                    safe_tool_request_object_id,
                    proposal_object_id,
                    policy=policy,
                )
            )
    elif step_output.final_response_text is not None:
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:final_response_ready",
                RuntimeOCELTraceEventKind.FINAL_RESPONSE_READY,
                "Final response ready without raw response trace",
                {"bounded_output": True, "response_chars": len(step_output.final_response_text)},
                [step_object_id],
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_runtime_ocel_relation(
                f"relation:{step_output.step_output_id}:step_produces_response",
                RuntimeOCELRelationType.STEP_PRODUCES_RESPONSE,
                step_object_id,
                execution_record_object_id,
                policy=policy,
            )
        )
    elif step_output.no_op_reason is not None:
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:no_op",
                RuntimeOCELTraceEventKind.NO_OP_RECORDED,
                "No-op result recorded",
                {"status": str(step_output.status)},
                [step_object_id],
                [source_ref],
                policy,
            )
        )
    elif step_output.safe_fail_reason is not None:
        events.append(
            build_runtime_ocel_event(
                f"event:{step_output.step_output_id}:safe_fail",
                RuntimeOCELTraceEventKind.SAFE_FAIL_RECORDED,
                "Safe-fail result recorded",
                {"status": str(step_output.status)},
                [step_object_id],
                [source_ref],
                policy,
            )
        )

    events.append(
        build_runtime_ocel_event(
            f"event:{step_output.step_output_id}:completed",
            RuntimeOCELTraceEventKind.AGENT_STEP_COMPLETED,
            "Agent step trace completed",
            {"status": str(step_output.status), "ready_for_execution": step_output.ready_for_execution},
            [step_object_id],
            [source_ref],
            policy,
        )
    )
    attributes = [
        sanitize_runtime_ocel_attribute_value(step_output.summary, policy),
    ]
    redaction_applied = any(obj.redacted for obj in objects) or any(event.redacted for event in events) or any(attribute.redacted for attribute in attributes)
    truncated = any(attribute.truncated for attribute in attributes)
    return build_runtime_ocel_trace_packet(
        f"trace_packet:{step_output.step_output_id}",
        objects=objects,
        events=events,
        relations=relations,
        attributes=attributes,
        source_refs=[source_ref],
        redaction_applied=redaction_applied,
        truncated=truncated,
        summary="Bounded trace packet from supplied v0.33.6 AgentStepOutput; raw output omitted.",
    )


def build_runtime_ocel_packet_from_session_snapshot(
    snapshot: AgentRuntimeSessionSnapshot,
    policy: RuntimeOCELTracePolicy,
) -> RuntimeOCELTracePacket:
    if not isinstance(snapshot, AgentRuntimeSessionSnapshot):
        raise TypeError("snapshot must be AgentRuntimeSessionSnapshot")
    if not isinstance(policy, RuntimeOCELTracePolicy):
        raise TypeError("policy must be RuntimeOCELTracePolicy")

    source_ref = build_runtime_ocel_source_ref(
        f"source:{snapshot.snapshot_id}",
        RuntimeOCELTraceSourceKind.V0333_SESSION_RUNTIME,
        snapshot.snapshot_id,
        "v0.33.3 in-memory AgentRuntimeSessionSnapshot artifact.",
    )
    session_object_id = f"object:agent_session:{snapshot.session.session_id}"
    objects = [
        build_runtime_ocel_object(
            session_object_id,
            RuntimeOCELObjectType.AGENT_SESSION,
            snapshot.session.session_id,
            {
                "status": str(snapshot.session.state),
                "summary": snapshot.session.summary,
                "active_turn_count": len(snapshot.session.active_turn_ids),
                "completed_turn_count": len(snapshot.session.completed_turn_ids),
            },
            [source_ref],
            policy,
        )
    ]
    events = [
        build_runtime_ocel_event(
            f"event:{snapshot.snapshot_id}:session_created",
            RuntimeOCELTraceEventKind.AGENT_SESSION_CREATED,
            "Session snapshot traced",
            {"status": str(snapshot.session.state)},
            [session_object_id],
            [source_ref],
            policy,
        )
    ]
    relations: list[RuntimeOCELRelation] = []
    for turn_id in snapshot.session.active_turn_ids + snapshot.session.completed_turn_ids:
        turn_object_id = f"object:agent_turn:{turn_id}"
        objects.append(
            build_runtime_ocel_object(
                turn_object_id,
                RuntimeOCELObjectType.AGENT_TURN,
                turn_id,
                {"summary": "Turn id from bounded session snapshot.", "source_ref": snapshot.snapshot_id},
                [source_ref],
                policy,
            )
        )
        events.append(
            build_runtime_ocel_event(
                f"event:{snapshot.snapshot_id}:turn:{turn_id}",
                RuntimeOCELTraceEventKind.AGENT_TURN_CREATED,
                "Turn reference traced",
                {"status": "referenced"},
                [turn_object_id],
                [source_ref],
                policy,
            )
        )
        relations.append(
            build_runtime_ocel_relation(
                f"relation:{snapshot.snapshot_id}:session_has_turn:{turn_id}",
                RuntimeOCELRelationType.SESSION_HAS_TURN,
                session_object_id,
                turn_object_id,
                policy=policy,
            )
        )
    return build_runtime_ocel_trace_packet(
        f"trace_packet:{snapshot.snapshot_id}",
        objects=objects,
        events=events,
        relations=relations,
        source_refs=[source_ref],
        summary="Bounded trace packet from supplied v0.33.3 AgentRuntimeSessionSnapshot.",
    )


def decide_runtime_ocel_trace_emission(
    emission_input: RuntimeOCELTraceEmissionInput,
    policy: RuntimeOCELTracePolicy,
) -> RuntimeOCELTraceEmissionDecision:
    if not isinstance(emission_input, RuntimeOCELTraceEmissionInput):
        raise TypeError("emission_input must be RuntimeOCELTraceEmissionInput")
    if not isinstance(policy, RuntimeOCELTracePolicy):
        raise TypeError("policy must be RuntimeOCELTracePolicy")

    sink_kind = RuntimeOCELTraceSinkKind(emission_input.requested_sink_kind)
    if sink_kind == RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET and sink_kind in policy.allowed_sink_kinds:
        return build_runtime_ocel_trace_emission_decision(
            f"{emission_input.emission_input_id}:decision",
            emission_input.emission_input_id,
            RuntimeOCELTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION,
            "Returned trace packet creation is allowed; no persistent write.",
            allowed_sink_kind=sink_kind,
        )
    if sink_kind == RuntimeOCELTraceSinkKind.IN_MEMORY_TEST_SINK and sink_kind in policy.allowed_sink_kinds:
        return build_runtime_ocel_trace_emission_decision(
            f"{emission_input.emission_input_id}:decision",
            emission_input.emission_input_id,
            RuntimeOCELTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK,
            "In-memory test sink is allowed only as returned artifact metadata.",
            allowed_sink_kind=sink_kind,
        )
    return build_runtime_ocel_trace_emission_decision(
        f"{emission_input.emission_input_id}:decision",
        emission_input.emission_input_id,
        RuntimeOCELTraceDecisionKind.BLOCK,
        "Requested sink is persistent, external, unknown, or otherwise blocked in v0.33.7.",
        allowed_sink_kind=None,
        risk_kinds=[RuntimeOCELTraceRiskKind.EXTERNAL_TRACE_SINK_RISK],
    )


def emit_runtime_ocel_trace_packet(
    emission_input: RuntimeOCELTraceEmissionInput,
    emitter: RuntimeOCELTraceEmitter,
    supplied_artifacts: dict[str, Any] | None = None,
) -> RuntimeOCELTracePacket:
    if not isinstance(emission_input, RuntimeOCELTraceEmissionInput):
        raise TypeError("emission_input must be RuntimeOCELTraceEmissionInput")
    if not isinstance(emitter, RuntimeOCELTraceEmitter):
        raise TypeError("emitter must be RuntimeOCELTraceEmitter")
    artifacts = supplied_artifacts or {}
    decision = decide_runtime_ocel_trace_emission(emission_input, emitter.trace_policy)
    if RuntimeOCELTraceDecisionKind(decision.decision_kind) not in {
        RuntimeOCELTraceDecisionKind.ALLOW_TRACE_PACKET_CREATION,
        RuntimeOCELTraceDecisionKind.ALLOW_IN_MEMORY_TEST_SINK,
    }:
        return build_runtime_ocel_trace_packet(
            f"trace_packet:{emission_input.emission_input_id}:blocked",
            sink_kind=RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET,
            status=RuntimeOCELTraceStatus.BLOCKED,
            summary="Trace emission request was blocked; no sink write occurred.",
            metadata={"decision_id": decision.decision_id},
        )
    if "packet" in artifacts and isinstance(artifacts["packet"], RuntimeOCELTracePacket):
        packet = artifacts["packet"]
    elif "step_output" in artifacts:
        packet = build_runtime_ocel_packet_from_agent_step_output(artifacts["step_output"], emitter.trace_policy)
    elif "session_snapshot" in artifacts:
        packet = build_runtime_ocel_packet_from_session_snapshot(artifacts["session_snapshot"], emitter.trace_policy)
    else:
        packet = build_runtime_ocel_trace_packet(
            f"trace_packet:{emission_input.emission_input_id}",
            sink_kind=decision.allowed_sink_kind or RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET,
            summary="Empty bounded trace packet from supplied in-memory emission input.",
            metadata={"decision_id": decision.decision_id},
        )
    validation = validate_runtime_ocel_trace_packet(packet, emitter.trace_policy)
    if not validation.validation_passed:
        return build_runtime_ocel_trace_packet(
            f"trace_packet:{emission_input.emission_input_id}:validation_blocked",
            sink_kind=RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET,
            status=RuntimeOCELTraceStatus.BLOCKED,
            summary="Trace packet failed validation; unsafe packet was not emitted.",
            metadata={"decision_id": decision.decision_id, "validation_report_id": validation.validation_report_id},
        )
    return packet


def runtime_ocel_flags_preserve_unsafe_runtime_false(flags: RuntimeOCELFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_RUNTIME_OCEL_FLAG_NAMES)


def runtime_ocel_packet_is_not_persistence(packet: RuntimeOCELTracePacket) -> bool:
    return (
        packet.ready_for_persistent_write is False
        and packet.ready_for_external_sink is False
        and packet.ready_for_execution is False
        and RuntimeOCELTraceSinkKind(packet.sink_kind)
        in {RuntimeOCELTraceSinkKind.RETURNED_TRACE_PACKET, RuntimeOCELTraceSinkKind.IN_MEMORY_TEST_SINK, RuntimeOCELTraceSinkKind.DISABLED}
    )


def runtime_ocel_policy_blocks_raw_outputs(policy: RuntimeOCELTracePolicy) -> bool:
    return (
        policy.allow_raw_model_output is False
        and policy.allow_raw_tool_output is False
        and policy.allow_file_content is False
        and policy.allow_secret_content is False
        and policy.allow_credential_content is False
        and policy.allow_persistent_write is False
        and policy.allow_external_sink is False
    )


def runtime_ocel_trace_report_is_not_persistent_write(report: RuntimeOCELTraceEmissionReport) -> bool:
    return (
        report.ready_for_general_ocel_emission is False
        and report.ready_for_persistent_trace_write is False
        and report.ready_for_external_trace_sink is False
        and report.ready_for_execution is False
    )


def v0337_readiness_report_is_not_general_runtime_ready(report: V0337ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_RUNTIME_OCEL_FLAG_NAMES)
