from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from .boundary import (
    _metadata_flag_true,
    _require_non_blank,
    _validate_object_list,
    _validate_string_list,
)


V0343_VERSION = "v0.34.3"
V0343_RELEASE_NAME = "v0.34.3 Model Response Envelope & Sanitizer"
DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS = 2000
DEFAULT_MAX_SANITIZED_RESPONSE_CHARS = 4000
DEFAULT_MAX_ACTION_SIGNAL_COUNT = 20

DEFAULT_SECRET_LIKE_PATTERNS = [
    ".env",
    "secret",
    "token",
    "key",
    "credential",
    "api_key",
    "password",
]

DEFAULT_RESPONSE_PROHIBITED_RUNTIME_ACTIONS = [
    "controlled model invocation",
    "real model invocation",
    "model invocation",
    "provider invocation",
    "provider SDK invocation",
    "existing boundary invocation",
    "network access",
    "credential access",
    "secret read",
    "env read",
    "agent step execution",
    "general agent execution",
    "autonomous loop",
    "general tool execution",
    "tool calls",
    "function calls",
    "action execution",
    "shell execution",
    "subprocess execution",
    "command execution",
    "workspace write",
    "code edit",
    "patch application",
    "raw response persistence",
    "raw model output persistence",
    "external harness execution",
    "reference code execution",
    "reference import",
    "dependency install",
    "persistent trace write",
    "external trace sink",
    "UI runtime",
    "external control",
    "authority grant",
]

DEFAULT_RESPONSE_WITHDRAWAL_CONDITIONS = [
    "Any model/provider/existing-boundary invocation path is introduced.",
    "Any model output, action, tool, function, shell, patch, command, or reference execution path is introduced.",
    "Any raw response or raw model output persistence path is introduced.",
    "Any unsafe readiness flag or production_certified becomes true.",
]

UNSAFE_MODEL_RESPONSE_FLAG_NAMES = (
    "ready_for_execution",
    "ready_for_controlled_model_invocation",
    "ready_for_real_model_invocation",
    "ready_for_model_invocation",
    "ready_for_provider_invocation",
    "ready_for_provider_sdk_invocation",
    "ready_for_existing_boundary_invocation",
    "ready_for_network_access",
    "ready_for_credential_access",
    "ready_for_secret_read",
    "ready_for_agent_step_execution",
    "ready_for_general_agent_execution",
    "ready_for_autonomous_agent_runtime",
    "ready_for_general_tool_execution",
    "ready_for_tool_calls",
    "ready_for_function_calls",
    "ready_for_action_execution",
    "ready_for_shell_execution",
    "ready_for_subprocess_execution",
    "ready_for_command_execution",
    "ready_for_workspace_write",
    "ready_for_code_edit",
    "ready_for_patch_application",
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


class ModelResponseEnvelopeKind(StrEnum):
    SUPPLIED_RESPONSE_ENVELOPE = "supplied_response_envelope"
    MOCK_RESPONSE_ENVELOPE = "mock_response_envelope"
    FUTURE_PROVIDER_RESPONSE_ENVELOPE = "future_provider_response_envelope"
    SANITIZED_RESPONSE_ENVELOPE = "sanitized_response_envelope"
    BLOCKED_RESPONSE_ENVELOPE = "blocked_response_envelope"
    NO_OP_RESPONSE_ENVELOPE = "no_op_response_envelope"
    UNKNOWN = "unknown"


class ModelResponsePayloadFormat(StrEnum):
    PLAIN_TEXT_RESPONSE = "plain_text_response"
    STRUCTURED_RESPONSE = "structured_response"
    JSON_LIKE_RESPONSE = "json_like_response"
    MARKDOWN_RESPONSE = "markdown_response"
    RESPONSE_REF_ONLY = "response_ref_only"
    REDACTED_PREVIEW_ONLY = "redacted_preview_only"
    TEST_FIXTURE = "test_fixture"
    UNKNOWN = "unknown"


class ModelResponseSourceKind(StrEnum):
    V0342_MODEL_REQUEST_ENVELOPE = "v0342_model_request_envelope"
    V0341_PROVIDER_PROFILE = "v0341_provider_profile"
    V0340_MODEL_INVOCATION_BOUNDARY = "v0340_model_invocation_boundary"
    SUPPLIED_MODEL_RESPONSE = "supplied_model_response"
    MOCK_MODEL_RESPONSE = "mock_model_response"
    FUTURE_PROVIDER_RESPONSE = "future_provider_response"
    TEST_FIXTURE = "test_fixture"
    REFERENCE_CONTEXT_REF = "reference_context_ref"
    OPENCODE_REFERENCE_CONTEXT_REF = "opencode_reference_context_ref"
    HERMES_REFERENCE_CONTEXT_REF = "hermes_reference_context_ref"
    UNKNOWN = "unknown"


class ModelResponseStatus(StrEnum):
    UNKNOWN = "unknown"
    DRAFT = "draft"
    ENVELOPE_CONSTRUCTED = "envelope_constructed"
    SANITIZED = "sanitized"
    SANITIZED_WITH_WARNINGS = "sanitized_with_warnings"
    VALIDATED = "validated"
    BLOCKED = "blocked"
    DEFERRED = "deferred"
    FUTURE_TRACK = "future_track"
    NO_OP = "no_op"


class ModelResponseReadinessLevel(StrEnum):
    NOT_READY = "not_ready"
    RESPONSE_CONTRACT_READY = "response_contract_ready"
    SANITIZATION_READY = "sanitization_ready"
    VALIDATION_READY = "validation_ready"
    DESIGN_HANDOFF_READY_FOR_V0344 = "design_handoff_ready_for_v0344"
    DESIGN_HANDOFF_READY_FOR_V0345 = "design_handoff_ready_for_v0345"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ModelResponseSanitizationDecisionKind(StrEnum):
    ACCEPT_SANITIZED_PREVIEW = "accept_sanitized_preview"
    ACCEPT_WITH_REDACTION = "accept_with_redaction"
    ACCEPT_WITH_TRUNCATION = "accept_with_truncation"
    BLOCK_SECRET_CONTENT = "block_secret_content"
    BLOCK_CREDENTIAL_CONTENT = "block_credential_content"
    BLOCK_UNSAFE_ACTION_SIGNAL = "block_unsafe_action_signal"
    BLOCK_UNBOUNDED_RESPONSE = "block_unbounded_response"
    NO_OP = "no_op"
    REQUIRE_REVIEW = "require_review"
    FUTURE_GATE_REQUIRED = "future_gate_required"
    UNKNOWN = "unknown"


class ModelResponseRiskKind(StrEnum):
    RAW_RESPONSE_PERSISTENCE_RISK = "raw_response_persistence_risk"
    SECRET_IN_RESPONSE_RISK = "secret_in_response_risk"
    CREDENTIAL_IN_RESPONSE_RISK = "credential_in_response_risk"
    TOKEN_IN_RESPONSE_RISK = "token_in_response_risk"
    UNBOUNDED_RESPONSE_RISK = "unbounded_response_risk"
    MODEL_OUTPUT_AS_ACTION_RISK = "model_output_as_action_risk"
    TOOL_CALL_LIKE_OUTPUT_RISK = "tool_call_like_output_risk"
    FUNCTION_CALL_LIKE_OUTPUT_RISK = "function_call_like_output_risk"
    COMMAND_EXECUTION_SUGGESTION_RISK = "command_execution_suggestion_risk"
    PATCH_SUGGESTION_RISK = "patch_suggestion_risk"
    WORKSPACE_WRITE_SUGGESTION_RISK = "workspace_write_suggestion_risk"
    PROVIDER_REINVOKE_SUGGESTION_RISK = "provider_reinvoke_suggestion_risk"
    NETWORK_ACCESS_SUGGESTION_RISK = "network_access_suggestion_risk"
    CREDENTIAL_REQUEST_SUGGESTION_RISK = "credential_request_suggestion_risk"
    EXTERNAL_HARNESS_EXECUTION_SUGGESTION_RISK = "external_harness_execution_suggestion_risk"
    REFERENCE_EXECUTION_SUGGESTION_RISK = "reference_execution_suggestion_risk"
    BOUNDARY_OVERRIDE_RISK = "boundary_override_risk"
    PROMPT_INJECTION_ECHO_RISK = "prompt_injection_echo_risk"
    UNKNOWN = "unknown"


class ModelResponseDataSensitivityKind(StrEnum):
    PUBLIC = "public"
    INTERNAL = "internal"
    USER_SUPPLIED = "user_supplied"
    REFERENCE_CONTEXT = "reference_context"
    UNTRUSTED_MODEL_OUTPUT = "untrusted_model_output"
    SECRET_LIKE = "secret_like"
    CREDENTIAL_LIKE = "credential_like"
    TOKEN_LIKE = "token_like"
    UNSAFE_ACTION_LIKE = "unsafe_action_like"
    UNKNOWN = "unknown"


class ModelResponseActionSignalKind(StrEnum):
    NO_ACTION_SIGNAL = "no_action_signal"
    FINAL_ANSWER_LIKE = "final_answer_like"
    TOOL_CALL_LIKE = "tool_call_like"
    FUNCTION_CALL_LIKE = "function_call_like"
    SHELL_COMMAND_LIKE = "shell_command_like"
    FILE_WRITE_LIKE = "file_write_like"
    CODE_EDIT_LIKE = "code_edit_like"
    PATCH_LIKE = "patch_like"
    DEPENDENCY_INSTALL_LIKE = "dependency_install_like"
    PROVIDER_REINVOKE_LIKE = "provider_reinvoke_like"
    NETWORK_ACCESS_LIKE = "network_access_like"
    CREDENTIAL_REQUEST_LIKE = "credential_request_like"
    EXTERNAL_HARNESS_EXECUTE_LIKE = "external_harness_execute_like"
    REFERENCE_CODE_EXECUTE_LIKE = "reference_code_execute_like"
    BROWSER_RPA_GATEWAY_LIKE = "browser_rpa_gateway_like"
    AUTHORITY_GRANT_LIKE = "authority_grant_like"
    UNKNOWN = "unknown"


def _validate_version_includes_v0343(version: str) -> None:
    _require_non_blank("version", version)
    if V0343_VERSION not in version:
        raise ValueError("version must include v0.34.3")


def _validate_false(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not False:
            raise ValueError(f"{name} must always be False in v0.34.3")


def _validate_true(obj: Any, names: tuple[str, ...]) -> None:
    for name in names:
        if getattr(obj, name) is not True:
            raise ValueError(f"{name} must always be True in v0.34.3")


def _validate_dict(name: str, value: dict[str, Any] | None) -> None:
    if value is not None and (not isinstance(value, dict) or not all(isinstance(key, str) for key in value)):
        raise TypeError(f"{name} must be dict[str, Any] or None")


def _validate_enum_list(name: str, values: list[Any], enum_type: type[StrEnum]) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{name} must be list")
    for value in values:
        enum_type(value)


def _validate_non_negative(name: str, value: int | None) -> None:
    if value is not None and value < 0:
        raise ValueError(f"{name} must be >= 0")


def _validate_metadata_no_execution(metadata: dict[str, Any]) -> None:
    _validate_dict("metadata", metadata)
    if _metadata_flag_true(
        metadata,
        {
            "model_invocation",
            "provider_invocation",
            "existing_boundary_invocation",
            "provider_sdk_import",
            "network_call",
            "credential_access",
            "secret_read",
            "env_read",
            "model_output_execution",
            "action_execution",
            "tool_call_execution",
            "function_call_execution",
            "shell_execution",
            "command_execution",
            "workspace_write",
            "patch_application",
            "raw_response_persistence",
            "raw_model_output_persistence",
            "persistent_trace_write",
        },
    ):
        raise ValueError("v0.34.3 metadata cannot imply invocation, execution, or raw response persistence")


def _validate_secret_patterns(name: str, values: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in DEFAULT_SECRET_LIKE_PATTERNS if term not in lowered]
    if missing:
        raise ValueError(f"{name} must include secret-like defaults: {missing}")


def _looks_like_secret_value(value: str) -> bool:
    lowered = value.strip().lower()
    return lowered.startswith("sk-") or any(marker in lowered for marker in ("secret=", "token=", "key=", "credential=", "api_key=", "password="))


def _contains_any(text: str, needles: tuple[str, ...]) -> bool:
    lowered = text.lower()
    return any(needle in lowered for needle in needles)


def _bounded(value: str, limit: int) -> tuple[str, bool]:
    if len(value) <= limit:
        return value, False
    return value[:limit], True


def _redact_response_text(value: str) -> tuple[str, int]:
    redacted = value
    count = 0
    replacements = (
        (r"\bsecret\s*=\s*\S+", "secret:[redacted]"),
        (r"\btoken\s*=\s*\S+", "token:[redacted]"),
        (r"\bkey\s*=\s*\S+", "key:[redacted]"),
        (r"\bcredential\s*=\s*\S+", "credential:[redacted]"),
        (r"\bapi_key\s*=\s*\S+", "api_key:[redacted]"),
        (r"\bpassword\s*=\s*\S+", "password:[redacted]"),
        (r"\bsk-[A-Za-z0-9_-]+", "[redacted-token]"),
    )
    for pattern, replacement in replacements:
        redacted, substitutions = re.subn(pattern, replacement, redacted, flags=re.IGNORECASE)
        count += substitutions
    return redacted, count


def _validate_contains_terms(name: str, values: list[str], terms: list[str]) -> None:
    _validate_string_list(name, values)
    lowered = " | ".join(values).lower()
    missing = [term for term in terms if term.lower() not in lowered]
    if missing:
        raise ValueError(f"{name} missing required terms: {missing}")


@dataclass(frozen=True)
class ModelResponseFlagSet:
    flag_set_id: str
    version: str = V0343_VERSION
    response_envelope_constructed: bool = False
    response_sanitizer_available: bool = False
    response_validation_available: bool = False
    response_action_signal_detection_available: bool = False
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_execution: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_tool_calls: bool = False
    ready_for_function_calls: bool = False
    ready_for_action_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
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
        _validate_version_includes_v0343(self.version)
        _validate_false(self, UNSAFE_MODEL_RESPONSE_FLAG_NAMES)
        if self.production_certified is not False:
            raise ValueError("production_certified must always be False in v0.34.3")
        _validate_metadata_no_execution(self.metadata)


@dataclass(frozen=True)
class ModelResponseSourceRef:
    source_ref_id: str
    source_kind: ModelResponseSourceKind | str
    source_id: str
    source_summary: str
    sensitivity: ModelResponseDataSensitivityKind | str = ModelResponseDataSensitivityKind.UNTRUSTED_MODEL_OUTPUT
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("source_ref_id", self.source_ref_id)
        ModelResponseSourceKind(self.source_kind)
        _require_non_blank("source_id", self.source_id)
        _require_non_blank("source_summary", self.source_summary)
        ModelResponseDataSensitivityKind(self.sensitivity)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def file_read(self) -> bool:
        return False

    @property
    def credential_access(self) -> bool:
        return False

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelRawResponseRef:
    raw_response_ref_id: str
    response_source_kind: ModelResponseSourceKind | str
    response_summary: str
    raw_response_preview: str
    raw_response_char_count: int
    redacted: bool
    truncated: bool
    contains_secret_like_content: bool
    contains_credential_like_content: bool
    contains_token_like_content: bool
    source_refs: list[ModelResponseSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("raw_response_ref_id", self.raw_response_ref_id)
        ModelResponseSourceKind(self.response_source_kind)
        _require_non_blank("response_summary", self.response_summary)
        if len(self.raw_response_preview) > DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS:
            raise ValueError("raw_response_preview must be bounded")
        _validate_non_negative("raw_response_char_count", self.raw_response_char_count)
        _validate_false(
            self,
            ("contains_secret_like_content", "contains_credential_like_content", "contains_token_like_content"),
        )
        if _looks_like_secret_value(self.raw_response_preview):
            raise ValueError("raw_response_preview must not contain secret-like values after sanitization")
        _validate_object_list("source_refs", self.source_refs, ModelResponseSourceRef)
        _validate_metadata_no_execution(self.metadata)

    @property
    def raw_response_persistence(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseSanitizationPolicy:
    sanitization_policy_id: str
    max_raw_preview_chars: int = DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS
    max_sanitized_chars: int = DEFAULT_MAX_SANITIZED_RESPONSE_CHARS
    max_action_signal_count: int = DEFAULT_MAX_ACTION_SIGNAL_COUNT
    redact_secret_like_content: bool = True
    redact_credential_like_content: bool = True
    redact_token_like_content: bool = True
    block_secret_like_content: bool = True
    block_credential_like_content: bool = True
    block_unbounded_response: bool = True
    block_command_like_output: bool = True
    block_patch_like_output: bool = True
    block_provider_reinvoke_like_output: bool = True
    block_external_harness_like_output: bool = True
    allow_raw_response_persistence: bool = False
    allow_action_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("sanitization_policy_id", self.sanitization_policy_id)
        for name in ("max_raw_preview_chars", "max_sanitized_chars", "max_action_signal_count"):
            _validate_non_negative(name, getattr(self, name))
        _validate_true(
            self,
            (
                "redact_secret_like_content",
                "redact_credential_like_content",
                "redact_token_like_content",
                "block_secret_like_content",
                "block_credential_like_content",
                "block_unbounded_response",
                "block_command_like_output",
                "block_patch_like_output",
                "block_provider_reinvoke_like_output",
                "block_external_harness_like_output",
            ),
        )
        _validate_false(self, ("allow_raw_response_persistence", "allow_action_execution"))
        _validate_metadata_no_execution(self.metadata)


@dataclass(frozen=True)
class ModelResponseRedactionRule:
    redaction_rule_id: str
    rule_name: str
    sensitivity_kind: ModelResponseDataSensitivityKind | str
    pattern_label: str
    replacement_text: str
    enabled: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for name in ("redaction_rule_id", "rule_name", "pattern_label", "replacement_text"):
            _require_non_blank(name, getattr(self, name))
        ModelResponseDataSensitivityKind(self.sensitivity_kind)
        if _looks_like_secret_value(self.pattern_label) or _looks_like_secret_value(self.replacement_text):
            raise ValueError("redaction rules must not store real secret values")
        _validate_metadata_no_execution(self.metadata)

    @property
    def credential_access(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseRiskSignal:
    risk_signal_id: str
    risk_kind: ModelResponseRiskKind | str
    severity: str
    summary: str
    affected_source_refs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    blocked: bool = False
    requires_quarantine: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("risk_signal_id", self.risk_signal_id)
        risk_kind = ModelResponseRiskKind(self.risk_kind)
        _require_non_blank("severity", self.severity)
        _require_non_blank("summary", self.summary)
        _validate_string_list("affected_source_refs", self.affected_source_refs)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if risk_kind != ModelResponseRiskKind.UNKNOWN and not (self.blocked or self.requires_quarantine):
            raise ValueError("high-risk response signals must be blocked or require quarantine")
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseActionSignal:
    action_signal_id: str
    signal_kind: ModelResponseActionSignalKind | str
    signal_summary: str
    confidence: str
    extracted_preview: str
    risk_kinds: list[ModelResponseRiskKind | str] = field(default_factory=list)
    requires_quarantine: bool = False
    blocked_from_execution: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("action_signal_id", self.action_signal_id)
        signal_kind = ModelResponseActionSignalKind(self.signal_kind)
        _require_non_blank("signal_summary", self.signal_summary)
        _require_non_blank("confidence", self.confidence)
        if len(self.extracted_preview) > DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS:
            raise ValueError("extracted_preview must be bounded")
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelResponseRiskKind)
        if signal_kind not in {ModelResponseActionSignalKind.NO_ACTION_SIGNAL, ModelResponseActionSignalKind.FINAL_ANSWER_LIKE}:
            if self.blocked_from_execution is not True:
                raise ValueError("unsafe action signals must be blocked_from_execution in v0.34.3")
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelSanitizedResponsePayload:
    sanitized_payload_id: str
    payload_format: ModelResponsePayloadFormat | str
    sanitized_text: str
    sanitized_summary: str
    response_preview: str
    redacted: bool
    truncated: bool
    redacted_field_count: int
    truncated_field_count: int
    risk_signals: list[ModelResponseRiskSignal] = field(default_factory=list)
    action_signals: list[ModelResponseActionSignal] = field(default_factory=list)
    source_refs: list[ModelResponseSourceRef] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("sanitized_payload_id", self.sanitized_payload_id)
        ModelResponsePayloadFormat(self.payload_format)
        _require_non_blank("sanitized_summary", self.sanitized_summary)
        if len(self.sanitized_text) > DEFAULT_MAX_SANITIZED_RESPONSE_CHARS:
            raise ValueError("sanitized_text must be bounded")
        if len(self.response_preview) > DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS:
            raise ValueError("response_preview must be bounded")
        _validate_non_negative("redacted_field_count", self.redacted_field_count)
        _validate_non_negative("truncated_field_count", self.truncated_field_count)
        _validate_object_list("risk_signals", self.risk_signals, ModelResponseRiskSignal)
        _validate_object_list("action_signals", self.action_signals, ModelResponseActionSignal)
        _validate_object_list("source_refs", self.source_refs, ModelResponseSourceRef)
        _validate_metadata_no_execution(self.metadata)

    @property
    def raw_response_persistence(self) -> bool:
        return False

    @property
    def action(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseEnvelopeInput:
    envelope_input_id: str
    source_version: str
    request_envelope_id: str | None
    provider_profile_id: str | None
    response_source_kind: ModelResponseSourceKind | str
    supplied_response_text: str | None
    supplied_structured_response: dict[str, Any] | None
    task_summary: str
    source_refs: list[ModelResponseSourceRef] = field(default_factory=list)
    prohibited_runtime_actions: list[str] = field(default_factory=lambda: list(DEFAULT_RESPONSE_PROHIBITED_RUNTIME_ACTIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        _validate_version_includes_v0343(self.source_version)
        ModelResponseSourceKind(self.response_source_kind)
        if self.supplied_response_text is not None and len(self.supplied_response_text) > DEFAULT_MAX_SANITIZED_RESPONSE_CHARS * 10:
            raise ValueError("supplied_response_text must be bounded")
        _validate_dict("supplied_structured_response", self.supplied_structured_response)
        _require_non_blank("task_summary", self.task_summary)
        _validate_object_list("source_refs", self.source_refs, ModelResponseSourceRef)
        _validate_contains_terms(
            "prohibited_runtime_actions",
            self.prohibited_runtime_actions,
            ["action execution", "provider invocation", "provider SDK", "network", "credential", "secret read", "tool calls", "function calls", "shell", "command", "write", "edit", "patch", "external harness execution", "reference code execution"],
        )
        _validate_metadata_no_execution(self.metadata)

    @property
    def provider_invocation_request(self) -> bool:
        return False

    @property
    def action_execution_request(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseEnvelope:
    response_envelope_id: str
    version: str
    envelope_kind: ModelResponseEnvelopeKind | str
    status: ModelResponseStatus | str
    readiness_level: ModelResponseReadinessLevel | str
    request_envelope_id: str | None
    raw_response_ref: ModelRawResponseRef | None
    sanitized_payload: ModelSanitizedResponsePayload
    sanitization_policy_id: str | None
    source_refs: list[ModelResponseSourceRef]
    summary: str
    validation_report_id: str | None = None
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_invocation: bool = False
    ready_for_action_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("response_envelope_id", self.response_envelope_id)
        _validate_version_includes_v0343(self.version)
        ModelResponseEnvelopeKind(self.envelope_kind)
        ModelResponseStatus(self.status)
        ModelResponseReadinessLevel(self.readiness_level)
        if self.raw_response_ref is not None and not isinstance(self.raw_response_ref, ModelRawResponseRef):
            raise TypeError("raw_response_ref must be ModelRawResponseRef or None")
        if not isinstance(self.sanitized_payload, ModelSanitizedResponsePayload):
            raise TypeError("sanitized_payload must be ModelSanitizedResponsePayload")
        _validate_object_list("source_refs", self.source_refs, ModelResponseSourceRef)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_invocation", "ready_for_action_execution", "ready_for_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def provider_call(self) -> bool:
        return False

    @property
    def action(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseSanitizationReport:
    sanitization_report_id: str
    version: str
    response_envelope_id: str | None
    sanitized_payload_id: str | None
    decision_kind: ModelResponseSanitizationDecisionKind | str
    risk_signals: list[ModelResponseRiskSignal]
    action_signals: list[ModelResponseActionSignal]
    redaction_applied: bool
    truncation_applied: bool
    blocked: bool
    requires_quarantine: bool
    summary: str
    ready_for_action_execution: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("sanitization_report_id", self.sanitization_report_id)
        _validate_version_includes_v0343(self.version)
        ModelResponseSanitizationDecisionKind(self.decision_kind)
        _validate_object_list("risk_signals", self.risk_signals, ModelResponseRiskSignal)
        _validate_object_list("action_signals", self.action_signals, ModelResponseActionSignal)
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_action_execution", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def action_permission(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseValidationFinding:
    finding_id: str
    response_envelope_id: str | None
    decision_kind: ModelResponseSanitizationDecisionKind | str
    risk_kinds: list[ModelResponseRiskKind | str]
    summary: str
    blocked: bool = False
    requires_quarantine: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("finding_id", self.finding_id)
        ModelResponseSanitizationDecisionKind(self.decision_kind)
        _validate_enum_list("risk_kinds", self.risk_kinds, ModelResponseRiskKind)
        _require_non_blank("summary", self.summary)
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseValidationReport:
    validation_report_id: str
    version: str
    response_envelope_id: str | None
    findings: list[ModelResponseValidationFinding]
    validation_passed: bool
    blocked_reasons: list[str]
    warning_items: list[str]
    redaction_applied: bool
    response_bounded: bool
    action_signals_blocked: bool
    raw_persistence_blocked: bool
    summary: str
    ready_for_action_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_execution: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("validation_report_id", self.validation_report_id)
        _validate_version_includes_v0343(self.version)
        _validate_object_list("findings", self.findings, ModelResponseValidationFinding)
        _validate_string_list("blocked_reasons", self.blocked_reasons)
        _validate_string_list("warning_items", self.warning_items)
        if self.validation_passed and self.blocked_reasons:
            raise ValueError("validation_passed cannot be True if blocked_reasons is non-empty")
        if self.action_signals_blocked is not True:
            raise ValueError("action_signals_blocked should be True in v0.34.3")
        if self.raw_persistence_blocked is not True:
            raise ValueError("raw_persistence_blocked should be True in v0.34.3")
        _require_non_blank("summary", self.summary)
        _validate_false(self, ("ready_for_action_execution", "ready_for_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution_certification(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseEnvelopeReport:
    report_id: str
    version: str
    envelope_input_id: str
    response_envelope_id: str | None
    sanitization_report_id: str | None
    validation_report_id: str | None
    status: ModelResponseStatus | str
    readiness_level: ModelResponseReadinessLevel | str
    summary: str
    completed_items: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    gaps: list[str] = field(default_factory=list)
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_invocation: bool = False
    ready_for_action_execution: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_execution: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_RESPONSE_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0343(self.version)
        _require_non_blank("envelope_input_id", self.envelope_input_id)
        ModelResponseStatus(self.status)
        ModelResponseReadinessLevel(self.readiness_level)
        _require_non_blank("summary", self.summary)
        for name in ("completed_items", "blocked_items", "future_track_items", "gaps", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        if (self.ready_for_v0344_existing_provider_boundary_adapter or self.ready_for_v0345_model_output_action_quarantine) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_false(self, ("ready_for_invocation", "ready_for_action_execution", "ready_for_provider_invocation", "ready_for_execution"))
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseRunPreview:
    run_preview_id: str
    response_envelope_id: str | None = None
    planned_steps: list[str] = field(default_factory=lambda: ["wrap supplied response text", "sanitize and redact response preview", "detect risk and action signals"])
    expected_artifacts: list[str] = field(default_factory=lambda: ["ModelResponseEnvelope", "ModelSanitizedResponsePayload", "ModelResponseSanitizationReport", "V0343ReadinessReport"])
    explicitly_not_performed: list[str] = field(default_factory=lambda: list(DEFAULT_RESPONSE_PROHIBITED_RUNTIME_ACTIONS))
    no_model_invocation_guarantee: bool = True
    no_real_model_invocation_guarantee: bool = True
    no_provider_invocation_guarantee: bool = True
    no_provider_sdk_invocation_guarantee: bool = True
    no_existing_boundary_invocation_guarantee: bool = True
    no_network_access_guarantee: bool = True
    no_credential_access_guarantee: bool = True
    no_secret_read_guarantee: bool = True
    no_env_read_guarantee: bool = True
    no_agent_step_execution_guarantee: bool = True
    no_tool_execution_guarantee: bool = True
    no_tool_call_execution_guarantee: bool = True
    no_function_call_execution_guarantee: bool = True
    no_action_execution_guarantee: bool = True
    no_command_execution_guarantee: bool = True
    no_workspace_write_guarantee: bool = True
    no_code_edit_guarantee: bool = True
    no_patch_application_guarantee: bool = True
    no_raw_response_persistence_guarantee: bool = True
    no_raw_model_output_persistence_guarantee: bool = True
    no_reference_code_execution_guarantee: bool = True
    no_reference_import_guarantee: bool = True
    no_dependency_install_guarantee: bool = True
    no_persistent_trace_write_guarantee: bool = True
    no_ui_runtime_guarantee: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("run_preview_id", self.run_preview_id)
        for name in ("planned_steps", "expected_artifacts", "explicitly_not_performed"):
            _validate_string_list(name, getattr(self, name))
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.3")
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution(self) -> bool:
        return False


@dataclass(frozen=True)
class ModelResponseNoExecutionGuarantee:
    guarantee_id: str
    version: str = V0343_VERSION
    no_model_invocation: bool = True
    no_real_model_invocation: bool = True
    no_provider_invocation: bool = True
    no_provider_sdk_invocation: bool = True
    no_existing_boundary_invocation: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_secret_read: bool = True
    no_env_read: bool = True
    no_agent_step_execution: bool = True
    no_tool_execution: bool = True
    no_tool_call_execution: bool = True
    no_function_call_execution: bool = True
    no_action_execution: bool = True
    no_shell_execution: bool = True
    no_subprocess: bool = True
    no_command_execution: bool = True
    no_workspace_write: bool = True
    no_code_edit: bool = True
    no_patch_application: bool = True
    no_raw_response_persistence: bool = True
    no_raw_model_output_persistence: bool = True
    no_reference_code_execution: bool = True
    no_reference_import: bool = True
    no_reference_dependency_install: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_persistent_trace_write: bool = True
    no_external_trace_sink: bool = True
    no_ui_runtime: bool = True
    no_external_control: bool = True
    no_authority_grant: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        _validate_version_includes_v0343(self.version)
        for name in self.__dataclass_fields__:
            if name.startswith("no_") and getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.34.3")
        _validate_string_list("evidence_refs", self.evidence_refs)
        _validate_metadata_no_execution(self.metadata)


@dataclass(frozen=True)
class V0343ReadinessReport:
    report_id: str
    version: str
    response_envelope_id: str | None
    envelope_report_id: str | None
    validation_report_id: str | None
    sanitization_report_id: str | None
    summary: str
    ready_for_v0344_existing_provider_boundary_adapter: bool = False
    ready_for_v0345_model_output_action_quarantine: bool = False
    ready_for_execution: bool = False
    ready_for_controlled_model_invocation: bool = False
    ready_for_real_model_invocation: bool = False
    ready_for_model_invocation: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_provider_sdk_invocation: bool = False
    ready_for_existing_boundary_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_secret_read: bool = False
    ready_for_agent_step_execution: bool = False
    ready_for_general_agent_execution: bool = False
    ready_for_autonomous_agent_runtime: bool = False
    ready_for_general_tool_execution: bool = False
    ready_for_tool_calls: bool = False
    ready_for_function_calls: bool = False
    ready_for_action_execution: bool = False
    ready_for_shell_execution: bool = False
    ready_for_subprocess_execution: bool = False
    ready_for_command_execution: bool = False
    ready_for_workspace_write: bool = False
    ready_for_code_edit: bool = False
    ready_for_patch_application: bool = False
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
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(DEFAULT_RESPONSE_PROHIBITED_RUNTIME_ACTIONS))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=lambda: list(DEFAULT_RESPONSE_WITHDRAWAL_CONDITIONS))
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        _validate_version_includes_v0343(self.version)
        _require_non_blank("summary", self.summary)
        _validate_false(self, UNSAFE_MODEL_RESPONSE_FLAG_NAMES)
        for name in ("completed_items", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        _validate_contains_terms(
            "prohibited_until_later_gate",
            self.prohibited_until_later_gate,
            ["controlled model invocation", "real model invocation", "model invocation", "provider invocation", "provider SDK invocation", "existing boundary invocation", "network access", "credential access", "secret read", "env read", "agent step execution", "autonomous loop", "general tool execution", "tool calls", "function calls", "action execution", "shell", "subprocess", "command", "workspace write", "code edit", "patch application", "raw response persistence", "raw model output persistence", "reference code execution", "reference import", "dependency install", "persistent trace write", "external trace sink", "UI runtime", "authority grant"],
        )
        if (self.ready_for_v0344_existing_provider_boundary_adapter or self.ready_for_v0345_model_output_action_quarantine) and self.blocked_items:
            raise ValueError("design-stage handoff readiness is not allowed with blocked_items")
        _validate_metadata_no_execution(self.metadata)

    @property
    def execution_readiness(self) -> bool:
        return False


def build_model_response_flags(flag_set_id: str = "model_response_flags:v0.34.3", **kwargs: Any) -> ModelResponseFlagSet:
    return ModelResponseFlagSet(
        flag_set_id=flag_set_id,
        version=kwargs.pop("version", V0343_VERSION),
        response_envelope_constructed=kwargs.pop("response_envelope_constructed", True),
        response_sanitizer_available=kwargs.pop("response_sanitizer_available", True),
        response_validation_available=kwargs.pop("response_validation_available", True),
        response_action_signal_detection_available=kwargs.pop("response_action_signal_detection_available", True),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        **kwargs,
    )


def build_model_response_source_ref(
    source_ref_id: str,
    source_kind: ModelResponseSourceKind | str = ModelResponseSourceKind.SUPPLIED_MODEL_RESPONSE,
    source_id: str = "model_response_source",
    source_summary: str = "Model response source ref only; no fetch/read/execute.",
    **kwargs: Any,
) -> ModelResponseSourceRef:
    return ModelResponseSourceRef(
        source_ref_id=source_ref_id,
        source_kind=source_kind,
        source_id=source_id,
        source_summary=source_summary,
        **kwargs,
    )


def build_model_raw_response_ref(raw_response_ref_id: str = "model_raw_response_ref:v0.34.3", **kwargs: Any) -> ModelRawResponseRef:
    return ModelRawResponseRef(
        raw_response_ref_id=raw_response_ref_id,
        response_source_kind=kwargs.pop("response_source_kind", ModelResponseSourceKind.SUPPLIED_MODEL_RESPONSE),
        response_summary=kwargs.pop("response_summary", "Bounded redacted raw response ref only."),
        raw_response_preview=kwargs.pop("raw_response_preview", "bounded redacted response preview"),
        raw_response_char_count=kwargs.pop("raw_response_char_count", 0),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        contains_secret_like_content=kwargs.pop("contains_secret_like_content", False),
        contains_credential_like_content=kwargs.pop("contains_credential_like_content", False),
        contains_token_like_content=kwargs.pop("contains_token_like_content", False),
        **kwargs,
    )


def build_model_response_sanitization_policy(
    sanitization_policy_id: str = "model_response_sanitization_policy:v0.34.3",
    **kwargs: Any,
) -> ModelResponseSanitizationPolicy:
    return ModelResponseSanitizationPolicy(sanitization_policy_id=sanitization_policy_id, **kwargs)


def default_model_response_sanitization_policy(**kwargs: Any) -> ModelResponseSanitizationPolicy:
    return build_model_response_sanitization_policy(**kwargs)


def build_model_response_redaction_rule(
    redaction_rule_id: str,
    **kwargs: Any,
) -> ModelResponseRedactionRule:
    return ModelResponseRedactionRule(
        redaction_rule_id=redaction_rule_id,
        rule_name=kwargs.pop("rule_name", "secret-like response redaction"),
        sensitivity_kind=kwargs.pop("sensitivity_kind", ModelResponseDataSensitivityKind.SECRET_LIKE),
        pattern_label=kwargs.pop("pattern_label", "secret-like pattern label only"),
        replacement_text=kwargs.pop("replacement_text", "[redacted]"),
        **kwargs,
    )


def default_model_response_redaction_rules() -> list[ModelResponseRedactionRule]:
    return [
        build_model_response_redaction_rule("redaction:secret", sensitivity_kind=ModelResponseDataSensitivityKind.SECRET_LIKE),
        build_model_response_redaction_rule("redaction:credential", sensitivity_kind=ModelResponseDataSensitivityKind.CREDENTIAL_LIKE, pattern_label="credential-like pattern label only"),
        build_model_response_redaction_rule("redaction:token", sensitivity_kind=ModelResponseDataSensitivityKind.TOKEN_LIKE, pattern_label="token-like pattern label only"),
    ]


def build_model_response_risk_signal(
    risk_signal_id: str,
    risk_kind: ModelResponseRiskKind | str = ModelResponseRiskKind.MODEL_OUTPUT_AS_ACTION_RISK,
    **kwargs: Any,
) -> ModelResponseRiskSignal:
    return ModelResponseRiskSignal(
        risk_signal_id=risk_signal_id,
        risk_kind=risk_kind,
        severity=kwargs.pop("severity", "high"),
        summary=kwargs.pop("summary", "Model response risk signal; advisory only."),
        blocked=kwargs.pop("blocked", True),
        requires_quarantine=kwargs.pop("requires_quarantine", True),
        **kwargs,
    )


def build_model_response_action_signal(
    action_signal_id: str,
    signal_kind: ModelResponseActionSignalKind | str = ModelResponseActionSignalKind.TOOL_CALL_LIKE,
    **kwargs: Any,
) -> ModelResponseActionSignal:
    return ModelResponseActionSignal(
        action_signal_id=action_signal_id,
        signal_kind=signal_kind,
        signal_summary=kwargs.pop("signal_summary", "Action-like response signal; detection artifact only."),
        confidence=kwargs.pop("confidence", "medium"),
        extracted_preview=kwargs.pop("extracted_preview", "bounded action-like preview"),
        risk_kinds=kwargs.pop("risk_kinds", [ModelResponseRiskKind.MODEL_OUTPUT_AS_ACTION_RISK]),
        requires_quarantine=kwargs.pop("requires_quarantine", True),
        blocked_from_execution=kwargs.pop("blocked_from_execution", True),
        **kwargs,
    )


def detect_model_response_action_signals(
    text: str,
    policy: ModelResponseSanitizationPolicy | None = None,
) -> list[ModelResponseActionSignal]:
    if not isinstance(text, str):
        raise TypeError("text must be str")
    policy = policy or default_model_response_sanitization_policy()
    signals: list[ModelResponseActionSignal] = []
    checks: list[tuple[tuple[str, ...], ModelResponseActionSignalKind, list[ModelResponseRiskKind]]] = [
        (("tool_call", '"tool"', "call tool"), ModelResponseActionSignalKind.TOOL_CALL_LIKE, [ModelResponseRiskKind.TOOL_CALL_LIKE_OUTPUT_RISK]),
        (("function_call", '"function"', "call function"), ModelResponseActionSignalKind.FUNCTION_CALL_LIKE, [ModelResponseRiskKind.FUNCTION_CALL_LIKE_OUTPUT_RISK]),
        (("powershell", "cmd.exe", "bash ", "run command", "shell command"), ModelResponseActionSignalKind.SHELL_COMMAND_LIKE, [ModelResponseRiskKind.COMMAND_EXECUTION_SUGGESTION_RISK]),
        (("write file", "save file", "create file"), ModelResponseActionSignalKind.FILE_WRITE_LIKE, [ModelResponseRiskKind.WORKSPACE_WRITE_SUGGESTION_RISK]),
        (("edit code", "modify code", "replace code"), ModelResponseActionSignalKind.CODE_EDIT_LIKE, [ModelResponseRiskKind.WORKSPACE_WRITE_SUGGESTION_RISK]),
        (("diff --git", "apply_patch", "patch file"), ModelResponseActionSignalKind.PATCH_LIKE, [ModelResponseRiskKind.PATCH_SUGGESTION_RISK]),
        (("pip install", "npm install", "poetry add"), ModelResponseActionSignalKind.DEPENDENCY_INSTALL_LIKE, [ModelResponseRiskKind.EXTERNAL_HARNESS_EXECUTION_SUGGESTION_RISK]),
        (("call openai", "call claude", "invoke provider", "call provider"), ModelResponseActionSignalKind.PROVIDER_REINVOKE_LIKE, [ModelResponseRiskKind.PROVIDER_REINVOKE_SUGGESTION_RISK]),
        (("http://", "https://", "fetch url", "webhook"), ModelResponseActionSignalKind.NETWORK_ACCESS_LIKE, [ModelResponseRiskKind.NETWORK_ACCESS_SUGGESTION_RISK]),
        (("api key", "credential", "secret", "token"), ModelResponseActionSignalKind.CREDENTIAL_REQUEST_LIKE, [ModelResponseRiskKind.CREDENTIAL_REQUEST_SUGGESTION_RISK]),
        (("execute opencode", "run hermes", "run openclaw", "external harness"), ModelResponseActionSignalKind.EXTERNAL_HARNESS_EXECUTE_LIKE, [ModelResponseRiskKind.EXTERNAL_HARNESS_EXECUTION_SUGGESTION_RISK]),
        (("import references/", "execute references/", "run references/"), ModelResponseActionSignalKind.REFERENCE_CODE_EXECUTE_LIKE, [ModelResponseRiskKind.REFERENCE_EXECUTION_SUGGESTION_RISK]),
        (("browser automation", "rpa", "gateway"), ModelResponseActionSignalKind.BROWSER_RPA_GATEWAY_LIKE, [ModelResponseRiskKind.MODEL_OUTPUT_AS_ACTION_RISK]),
        (("grant authority", "d4", "d9"), ModelResponseActionSignalKind.AUTHORITY_GRANT_LIKE, [ModelResponseRiskKind.BOUNDARY_OVERRIDE_RISK]),
    ]
    for needles, signal_kind, risks in checks:
        if _contains_any(text, needles):
            preview, _ = _bounded(text, DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS)
            signals.append(
                build_model_response_action_signal(
                    f"action_signal:{signal_kind.value}:{len(signals)}",
                    signal_kind,
                    extracted_preview=preview,
                    risk_kinds=risks,
                    requires_quarantine=True,
                    blocked_from_execution=True,
                )
            )
            if len(signals) >= policy.max_action_signal_count:
                break
    return signals


def detect_model_response_risk_signals(
    text: str,
    policy: ModelResponseSanitizationPolicy | None = None,
) -> list[ModelResponseRiskSignal]:
    if not isinstance(text, str):
        raise TypeError("text must be str")
    policy = policy or default_model_response_sanitization_policy()
    risks: list[ModelResponseRiskSignal] = []
    risk_checks: list[tuple[tuple[str, ...], ModelResponseRiskKind, str]] = [
        (("secret=",), ModelResponseRiskKind.SECRET_IN_RESPONSE_RISK, "secret-like response content"),
        (("credential=", "api_key=", "password="), ModelResponseRiskKind.CREDENTIAL_IN_RESPONSE_RISK, "credential-like response content"),
        (("token=", "sk-"), ModelResponseRiskKind.TOKEN_IN_RESPONSE_RISK, "token-like response content"),
        (("ignore previous", "override policy", "bypass boundary"), ModelResponseRiskKind.BOUNDARY_OVERRIDE_RISK, "boundary override or prompt-injection echo"),
    ]
    if len(text) > policy.max_sanitized_chars:
        risks.append(
            build_model_response_risk_signal(
                "risk:unbounded_response",
                ModelResponseRiskKind.UNBOUNDED_RESPONSE_RISK,
                summary="Response exceeds bounded sanitizer limit.",
                blocked=True,
                requires_quarantine=False,
            )
        )
    for needles, risk_kind, summary in risk_checks:
        if _contains_any(text, needles):
            risks.append(build_model_response_risk_signal(f"risk:{risk_kind.value}:{len(risks)}", risk_kind, summary=summary, blocked=True, requires_quarantine=True))
    for signal in detect_model_response_action_signals(text, policy):
        for risk_kind in signal.risk_kinds:
            risks.append(build_model_response_risk_signal(f"risk:{str(risk_kind)}:{len(risks)}", risk_kind, summary=signal.signal_summary, blocked=True, requires_quarantine=True))
    return risks


def build_model_sanitized_response_payload(
    sanitized_payload_id: str = "model_sanitized_response_payload:v0.34.3",
    **kwargs: Any,
) -> ModelSanitizedResponsePayload:
    return ModelSanitizedResponsePayload(
        sanitized_payload_id=sanitized_payload_id,
        payload_format=kwargs.pop("payload_format", ModelResponsePayloadFormat.REDACTED_PREVIEW_ONLY),
        sanitized_text=kwargs.pop("sanitized_text", "bounded sanitized response"),
        sanitized_summary=kwargs.pop("sanitized_summary", "Sanitized response payload; no action execution."),
        response_preview=kwargs.pop("response_preview", "bounded sanitized response"),
        redacted=kwargs.pop("redacted", True),
        truncated=kwargs.pop("truncated", False),
        redacted_field_count=kwargs.pop("redacted_field_count", 0),
        truncated_field_count=kwargs.pop("truncated_field_count", 0),
        **kwargs,
    )


def sanitize_model_response_text(
    raw_text: str,
    policy: ModelResponseSanitizationPolicy | None = None,
) -> ModelSanitizedResponsePayload:
    if not isinstance(raw_text, str):
        raise TypeError("raw_text must be str")
    policy = policy or default_model_response_sanitization_policy()
    redacted_text, redacted_count = _redact_response_text(raw_text)
    bounded_text, truncated = _bounded(redacted_text, policy.max_sanitized_chars)
    preview, preview_truncated = _bounded(bounded_text, policy.max_raw_preview_chars)
    risk_signals = detect_model_response_risk_signals(raw_text, policy)
    action_signals = detect_model_response_action_signals(raw_text, policy)
    return build_model_sanitized_response_payload(
        sanitized_text=bounded_text,
        response_preview=preview,
        redacted=redacted_count > 0,
        truncated=truncated or preview_truncated,
        redacted_field_count=redacted_count,
        truncated_field_count=1 if truncated or preview_truncated else 0,
        risk_signals=risk_signals,
        action_signals=action_signals,
    )


def build_model_response_envelope_input(
    envelope_input_id: str = "model_response_envelope_input:v0.34.3",
    **kwargs: Any,
) -> ModelResponseEnvelopeInput:
    return ModelResponseEnvelopeInput(
        envelope_input_id=envelope_input_id,
        source_version=kwargs.pop("source_version", V0343_VERSION),
        request_envelope_id=kwargs.pop("request_envelope_id", None),
        provider_profile_id=kwargs.pop("provider_profile_id", None),
        response_source_kind=kwargs.pop("response_source_kind", ModelResponseSourceKind.SUPPLIED_MODEL_RESPONSE),
        supplied_response_text=kwargs.pop("supplied_response_text", None),
        supplied_structured_response=kwargs.pop("supplied_structured_response", None),
        task_summary=kwargs.pop("task_summary", "Build response envelope metadata only."),
        **kwargs,
    )


def build_model_response_envelope(
    response_envelope_id: str = "model_response_envelope:v0.34.3",
    **kwargs: Any,
) -> ModelResponseEnvelope:
    return ModelResponseEnvelope(
        response_envelope_id=response_envelope_id,
        version=kwargs.pop("version", V0343_VERSION),
        envelope_kind=kwargs.pop("envelope_kind", ModelResponseEnvelopeKind.SANITIZED_RESPONSE_ENVELOPE),
        status=kwargs.pop("status", ModelResponseStatus.SANITIZED_WITH_WARNINGS),
        readiness_level=kwargs.pop("readiness_level", ModelResponseReadinessLevel.SANITIZATION_READY),
        request_envelope_id=kwargs.pop("request_envelope_id", None),
        raw_response_ref=kwargs.pop("raw_response_ref", build_model_raw_response_ref()),
        sanitized_payload=kwargs.pop("sanitized_payload", build_model_sanitized_response_payload()),
        sanitization_policy_id=kwargs.pop("sanitization_policy_id", "model_response_sanitization_policy:v0.34.3"),
        source_refs=kwargs.pop("source_refs", []),
        summary=kwargs.pop("summary", "Model response envelope metadata only; no action execution."),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        **kwargs,
    )


def build_model_response_envelope_from_supplied_text(
    supplied_response_text: str,
    response_envelope_id: str = "model_response_envelope:supplied:v0.34.3",
    policy: ModelResponseSanitizationPolicy | None = None,
    **kwargs: Any,
) -> ModelResponseEnvelope:
    policy = policy or default_model_response_sanitization_policy()
    source_ref = build_model_response_source_ref(
        "source:supplied_model_response:v0.34.3",
        ModelResponseSourceKind.SUPPLIED_MODEL_RESPONSE,
        "supplied_response_text",
        "Supplied in-memory response text source only.",
    )
    sanitized = sanitize_model_response_text(supplied_response_text, policy)
    raw_preview_text, redacted_count = _redact_response_text(supplied_response_text)
    raw_preview, truncated = _bounded(raw_preview_text, policy.max_raw_preview_chars)
    raw_ref = build_model_raw_response_ref(
        raw_response_ref_id=f"raw_response_ref:{response_envelope_id}",
        response_source_kind=ModelResponseSourceKind.SUPPLIED_MODEL_RESPONSE,
        response_summary="Bounded redacted raw response ref from supplied in-memory text.",
        raw_response_preview=raw_preview,
        raw_response_char_count=len(supplied_response_text),
        redacted=redacted_count > 0,
        truncated=truncated,
        source_refs=[source_ref],
    )
    return build_model_response_envelope(
        response_envelope_id=response_envelope_id,
        envelope_kind=kwargs.pop("envelope_kind", ModelResponseEnvelopeKind.SUPPLIED_RESPONSE_ENVELOPE),
        raw_response_ref=raw_ref,
        sanitized_payload=sanitized,
        source_refs=kwargs.pop("source_refs", [source_ref]),
        **kwargs,
    )


def build_model_response_sanitization_report(
    sanitization_report_id: str = "model_response_sanitization_report:v0.34.3",
    **kwargs: Any,
) -> ModelResponseSanitizationReport:
    return ModelResponseSanitizationReport(
        sanitization_report_id=sanitization_report_id,
        version=kwargs.pop("version", V0343_VERSION),
        response_envelope_id=kwargs.pop("response_envelope_id", None),
        sanitized_payload_id=kwargs.pop("sanitized_payload_id", None),
        decision_kind=kwargs.pop("decision_kind", ModelResponseSanitizationDecisionKind.ACCEPT_WITH_REDACTION),
        risk_signals=kwargs.pop("risk_signals", []),
        action_signals=kwargs.pop("action_signals", []),
        redaction_applied=kwargs.pop("redaction_applied", True),
        truncation_applied=kwargs.pop("truncation_applied", False),
        blocked=kwargs.pop("blocked", False),
        requires_quarantine=kwargs.pop("requires_quarantine", False),
        summary=kwargs.pop("summary", "Model response sanitization report; no action permission."),
        **kwargs,
    )


def build_model_response_validation_finding(
    finding_id: str,
    **kwargs: Any,
) -> ModelResponseValidationFinding:
    return ModelResponseValidationFinding(
        finding_id=finding_id,
        response_envelope_id=kwargs.pop("response_envelope_id", None),
        decision_kind=kwargs.pop("decision_kind", ModelResponseSanitizationDecisionKind.ACCEPT_SANITIZED_PREVIEW),
        risk_kinds=kwargs.pop("risk_kinds", []),
        summary=kwargs.pop("summary", "Model response validation finding; no execution."),
        **kwargs,
    )


def build_model_response_validation_report(
    validation_report_id: str = "model_response_validation_report:v0.34.3",
    **kwargs: Any,
) -> ModelResponseValidationReport:
    return ModelResponseValidationReport(
        validation_report_id=validation_report_id,
        version=kwargs.pop("version", V0343_VERSION),
        response_envelope_id=kwargs.pop("response_envelope_id", None),
        findings=kwargs.pop("findings", []),
        validation_passed=kwargs.pop("validation_passed", True),
        blocked_reasons=kwargs.pop("blocked_reasons", []),
        warning_items=kwargs.pop("warning_items", []),
        redaction_applied=kwargs.pop("redaction_applied", True),
        response_bounded=kwargs.pop("response_bounded", True),
        action_signals_blocked=kwargs.pop("action_signals_blocked", True),
        raw_persistence_blocked=kwargs.pop("raw_persistence_blocked", True),
        summary=kwargs.pop("summary", "Model response validation report; no execution certification."),
        **kwargs,
    )


def validate_model_response_envelope(
    envelope: ModelResponseEnvelope,
    policy: ModelResponseSanitizationPolicy | None = None,
) -> ModelResponseValidationReport:
    if not isinstance(envelope, ModelResponseEnvelope):
        raise TypeError("envelope must be ModelResponseEnvelope")
    policy = policy or default_model_response_sanitization_policy()
    blocked_reasons: list[str] = []
    findings: list[ModelResponseValidationFinding] = []
    if not model_response_envelope_is_not_action(envelope):
        blocked_reasons.append("Envelope attempted action/provider/execution readiness.")
    if envelope.raw_response_ref is not None and not model_raw_response_ref_is_not_persistence(envelope.raw_response_ref):
        blocked_reasons.append("Raw response ref failed no-persistence validation.")
    if envelope.sanitized_payload.action_signals:
        findings.append(
            build_model_response_validation_finding(
                "finding:action_signals_quarantine",
                response_envelope_id=envelope.response_envelope_id,
                decision_kind=ModelResponseSanitizationDecisionKind.BLOCK_UNSAFE_ACTION_SIGNAL,
                risk_kinds=[ModelResponseRiskKind.MODEL_OUTPUT_AS_ACTION_RISK],
                summary="Action-like output is blocked from execution and prepared for future quarantine.",
                blocked=True,
                requires_quarantine=True,
            )
        )
    if envelope.sanitized_payload.truncated and policy.block_unbounded_response:
        findings.append(
            build_model_response_validation_finding(
                "finding:bounded_response",
                response_envelope_id=envelope.response_envelope_id,
                decision_kind=ModelResponseSanitizationDecisionKind.ACCEPT_WITH_TRUNCATION,
                risk_kinds=[ModelResponseRiskKind.UNBOUNDED_RESPONSE_RISK],
                summary="Response was truncated to bounded sanitizer limits.",
                blocked=False,
                requires_quarantine=False,
            )
        )
    return build_model_response_validation_report(
        response_envelope_id=envelope.response_envelope_id,
        findings=findings,
        validation_passed=not blocked_reasons,
        blocked_reasons=blocked_reasons,
        warning_items=[finding.summary for finding in findings if not finding.blocked],
        redaction_applied=envelope.sanitized_payload.redacted,
        response_bounded=len(envelope.sanitized_payload.sanitized_text) <= policy.max_sanitized_chars,
        action_signals_blocked=all(signal.blocked_from_execution for signal in envelope.sanitized_payload.action_signals),
        raw_persistence_blocked=True,
        summary="Model response envelope validated as no-execution sanitizer artifact.",
    )


def build_model_response_envelope_report(
    report_id: str = "model_response_envelope_report:v0.34.3",
    **kwargs: Any,
) -> ModelResponseEnvelopeReport:
    return ModelResponseEnvelopeReport(
        report_id=report_id,
        version=kwargs.pop("version", V0343_VERSION),
        envelope_input_id=kwargs.pop("envelope_input_id", "model_response_envelope_input:v0.34.3"),
        response_envelope_id=kwargs.pop("response_envelope_id", "model_response_envelope:v0.34.3"),
        sanitization_report_id=kwargs.pop("sanitization_report_id", "model_response_sanitization_report:v0.34.3"),
        validation_report_id=kwargs.pop("validation_report_id", "model_response_validation_report:v0.34.3"),
        status=kwargs.pop("status", ModelResponseStatus.SANITIZED_WITH_WARNINGS),
        readiness_level=kwargs.pop("readiness_level", ModelResponseReadinessLevel.VALIDATION_READY),
        summary=kwargs.pop("summary", "Model response envelope report; no invocation or action execution."),
        completed_items=kwargs.pop("completed_items", ["response envelope", "sanitized payload", "risk signals", "action signals", "validation report"]),
        future_track_items=kwargs.pop("future_track_items", ["existing provider boundary adapter", "model output action quarantine"]),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        **kwargs,
    )


def build_model_response_run_preview(run_preview_id: str = "model_response_run_preview:v0.34.3", **kwargs: Any) -> ModelResponseRunPreview:
    return ModelResponseRunPreview(run_preview_id=run_preview_id, **kwargs)


def build_model_response_no_execution_guarantee(
    guarantee_id: str = "model_response_no_execution_guarantee:v0.34.3",
    **kwargs: Any,
) -> ModelResponseNoExecutionGuarantee:
    return ModelResponseNoExecutionGuarantee(guarantee_id=guarantee_id, version=kwargs.pop("version", V0343_VERSION), **kwargs)


def build_v0343_readiness_report(report_id: str = "v0343_readiness_report", **kwargs: Any) -> V0343ReadinessReport:
    return V0343ReadinessReport(
        report_id=report_id,
        version=kwargs.pop("version", V0343_VERSION),
        response_envelope_id=kwargs.pop("response_envelope_id", "model_response_envelope:v0.34.3"),
        envelope_report_id=kwargs.pop("envelope_report_id", "model_response_envelope_report:v0.34.3"),
        validation_report_id=kwargs.pop("validation_report_id", "model_response_validation_report:v0.34.3"),
        sanitization_report_id=kwargs.pop("sanitization_report_id", "model_response_sanitization_report:v0.34.3"),
        summary=kwargs.pop("summary", "v0.34.3 defines Model Response Envelope & Sanitizer metadata only; no action readiness."),
        ready_for_v0344_existing_provider_boundary_adapter=kwargs.pop("ready_for_v0344_existing_provider_boundary_adapter", True),
        ready_for_v0345_model_output_action_quarantine=kwargs.pop("ready_for_v0345_model_output_action_quarantine", True),
        completed_items=kwargs.pop("completed_items", ["response envelope", "sanitizer", "redaction rules", "risk signals", "action signals", "validation report"]),
        future_track_items=kwargs.pop("future_track_items", ["existing provider boundary adapter", "model output action quarantine"]),
        **kwargs,
    )


def model_response_flags_preserve_execution_false(flags: ModelResponseFlagSet) -> bool:
    return all(getattr(flags, name) is False for name in UNSAFE_MODEL_RESPONSE_FLAG_NAMES) and flags.production_certified is False


def model_raw_response_ref_is_not_persistence(raw_ref: ModelRawResponseRef) -> bool:
    return (
        raw_ref.raw_response_persistence is False
        and len(raw_ref.raw_response_preview) <= DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS
        and raw_ref.contains_secret_like_content is False
        and raw_ref.contains_credential_like_content is False
        and raw_ref.contains_token_like_content is False
    )


def model_response_envelope_is_not_action(envelope: ModelResponseEnvelope) -> bool:
    return (
        envelope.provider_call is False
        and envelope.action is False
        and envelope.ready_for_invocation is False
        and envelope.ready_for_action_execution is False
        and envelope.ready_for_provider_invocation is False
        and envelope.ready_for_execution is False
        and envelope.sanitized_payload.action is False
    )


def model_response_validation_report_blocks_action_execution(report: ModelResponseValidationReport) -> bool:
    return (
        report.execution_certification is False
        and report.action_signals_blocked is True
        and report.raw_persistence_blocked is True
        and report.ready_for_action_execution is False
        and report.ready_for_provider_invocation is False
        and report.ready_for_execution is False
    )


def v0343_readiness_report_is_not_execution_ready(report: V0343ReadinessReport) -> bool:
    return all(getattr(report, name) is False for name in UNSAFE_MODEL_RESPONSE_FLAG_NAMES) and report.execution_readiness is False
