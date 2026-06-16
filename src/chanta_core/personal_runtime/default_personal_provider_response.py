"""v0.42.8 configured provider response parsing and identity stabilization.

This module is deliberately narrow: it parses OpenAI-compatible response
shapes, defines runtime identity prompt metadata, and stabilizes command
surface routing. It does not add provider tools, function calling, shell,
edit/apply, subagents, broad scans, autonomous loops, or production
certification.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass, is_dataclass
from enum import StrEnum
from pathlib import Path
from typing import Any, Mapping, Sequence


V0428_VERSION = "v0.42.8"
V0428_RELEASE_NAME = "v0.42.8 Configured Provider Response Parsing & Runtime Identity Stabilization"
V0428_TRACK_NAME = "v0.42 Default Personal Runtime UX Hardening Track"
INTEGRATED_DOC_PATH = "docs/versions/v0.42/v0.42.8_provider_response_identity_command_surface_restore.md"


class V042ProviderResponseParseStatus(StrEnum):
    PARSED = "parsed"
    PARSED_EMPTY = "parsed_empty"
    MISSING_CHOICES = "missing_choices"
    MISSING_MESSAGE = "missing_message"
    MISSING_CONTENT = "missing_content"
    PROVIDER_REASONING_WITHOUT_FINAL = "provider_reasoning_without_final"
    INVALID_RESPONSE_SHAPE = "invalid_response_shape"
    PARSE_ERROR = "parse_error"
    TIMEOUT = "timeout"
    CONNECTION_ERROR = "connection_error"
    UNKNOWN = "unknown"


class V042ProviderResponseErrorClass(StrEnum):
    NONE = "none"
    PROVIDER_EMPTY_RESPONSE = "provider_empty_response"
    RESPONSE_PARSE_EMPTY = "response_parse_empty"
    RESPONSE_PARSE_ERROR = "response_parse_error"
    PROVIDER_REASONING_WITHOUT_FINAL = "provider_reasoning_without_final"
    PROVIDER_INVALID_RESPONSE = "provider_invalid_response"
    PROVIDER_TIMEOUT = "provider_timeout"
    PROVIDER_CONNECTION_ERROR = "provider_connection_error"
    MODEL_NOT_FOUND = "model_not_found"
    UNKNOWN_PROVIDER_ERROR = "unknown_provider_error"


@dataclass(frozen=True)
class V042ProviderResponseShapeSummary:
    summary_id: str
    has_choices: bool
    choices_count: int
    has_message: bool
    has_message_content: bool
    has_text: bool
    has_reasoning_content: bool
    has_delta_content: bool
    has_output_text: bool
    finish_reason: str | None
    provider_model: str | None
    prompt_tokens: int | None
    completion_tokens: int | None
    total_tokens: int | None
    raw_shape_label: str


@dataclass(frozen=True)
class V042ProviderResponseParsePolicy:
    policy_id: str
    prefer_message_content: bool
    allow_text_fallback: bool
    allow_output_text_fallback: bool
    allow_delta_content_fallback: bool
    allow_reasoning_content_as_final: bool
    treat_empty_content_as_failure: bool
    capture_reasoning_as_diagnostic: bool
    max_diagnostic_chars: int


@dataclass(frozen=True)
class V042ProviderResponseParseResult:
    result_id: str
    status: str
    error_class: str
    assistant_text: str
    assistant_text_present: bool
    extracted_from_field: str | None
    content_length: int
    reasoning_content_detected: bool
    final_content_detected: bool
    response_shape_summary: V042ProviderResponseShapeSummary
    diagnostic_summary: str
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042ProviderEmptyResponseDecision:
    decision_id: str
    empty_response_detected: bool
    mark_run_completed: bool
    append_normal_assistant_turn: bool
    record_assistant_response_success: bool
    status: str
    error_class: str
    next_actions: tuple[str, ...]


@dataclass(frozen=True)
class V042RuntimeIdentityPrompt:
    prompt_id: str
    runtime_identity: str
    provider_identity_policy: str
    language_policy: str
    safety_policy: str
    prompt_text: str
    included_in_configured_provider_run: bool
    included_in_mock_provider_run: bool


@dataclass(frozen=True)
class V042RuntimeIdentityInjectionReport:
    report_id: str
    prompt_assembled: bool
    runtime_identity_included: bool
    provider_model: str | None
    runtime_identity: str
    provider_identity_is_implementation_detail: bool
    system_message_count: int
    user_message_count: int
    ready_for_provider_payload: bool


@dataclass(frozen=True)
class V042ProviderIdentitySeparationReport:
    report_id: str
    provider_model: str
    runtime_identity: str
    base_model_identity_allowed_as_primary: bool
    provider_identity_allowed_as_implementation_detail: bool
    expected_identity_answer_policy: str


@dataclass(frozen=True)
class V042RunResponseRecordingPolicy:
    policy_id: str
    require_non_empty_assistant_text_for_success: bool
    append_empty_assistant_turn_as_success: bool
    record_empty_response_as_failure: bool
    trace_parse_status_required: bool
    run_report_parse_fields_required: bool


@dataclass(frozen=True)
class V042RunResponseRecordingDecision:
    decision_id: str
    parse_result: V042ProviderResponseParseResult
    should_append_assistant_turn: bool
    should_record_assistant_response_success: bool
    run_status: str
    response_valid: bool
    error_class: str
    normal_assistant_turn_appended: bool


@dataclass(frozen=True)
class V042ConfiguredRunFailureReport:
    report_id: str
    run_id: str | None
    session_id: str | None
    error_class: str
    response_parse_status: str
    provider_model: str | None
    base_url: str | None
    timeout_seconds: int | None
    next_actions: tuple[str, ...]
    provider_invoked: bool
    prompt_submitted: bool
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042RunReportResponseFields:
    response_parse_status: str | None
    response_error_class: str | None
    response_extracted_from_field: str | None
    response_content_length: int | None
    response_finish_reason: str | None
    provider_model: str | None
    runtime_identity_included: bool | None
    provider_identity_is_implementation_detail: bool | None
    empty_response_detected: bool | None
    next_action: str | None


@dataclass(frozen=True)
class V042ResponseParseTraceRecord:
    trace_record_id: str
    event_kind: str
    run_id: str | None
    session_id: str | None
    response_parse_status: str
    error_class: str
    content_length: int
    extracted_from_field: str | None
    provider_model: str | None
    shell_executed: bool
    subagent_invoked: bool
    production_certified: bool


@dataclass(frozen=True)
class V042CommandSurfaceStabilizationPolicy:
    policy_id: str
    preserve_direct_run_command: bool
    run_show_last_supported: bool
    run_history_supported: bool
    session_show_last_supported: bool
    unrecognized_show_args_redirected: bool
    help_priority_over_validation: bool


@dataclass(frozen=True)
class V042CommandSurfaceStabilizationResult:
    result_id: str
    run_help_fixed: bool
    run_show_last_no_longer_unrecognized: bool
    run_history_available_or_redirected: bool
    session_show_last_available_or_redirected: bool
    direct_run_preserved: bool
    user_guidance_text: str


@dataclass(frozen=True)
class V042ProviderReasoningModelTroubleshootingGuide:
    guide_id: str
    symptoms: tuple[str, ...]
    likely_causes: tuple[str, ...]
    recommended_actions: tuple[str, ...]
    safe_commands: tuple[str, ...]
    unsafe_actions_not_taken: tuple[str, ...]


@dataclass(frozen=True)
class V0428ReadinessReport:
    provider_response_parser_ready: bool
    empty_response_detection_ready: bool
    configured_run_failure_classification_ready: bool
    runtime_identity_prompt_ready: bool
    provider_identity_separation_ready: bool
    run_report_response_fields_ready: bool
    response_parse_trace_ready: bool
    command_surface_stabilization_ready: bool
    reasoning_model_troubleshooting_ready: bool
    integrated_restore_document_ready: bool
    v043_handoff_update_ready: bool
    ready_for_provider_doctor_completion: bool
    ready_for_provider_tool_calling: bool
    ready_for_function_calling: bool
    ready_for_shell_execution: bool
    ready_for_file_edit: bool
    ready_for_patch_apply: bool
    ready_for_arbitrary_file_read: bool
    ready_for_broad_filesystem_scan: bool
    ready_for_repo_search: bool
    ready_for_subagent_invocation: bool
    ready_for_general_agent_loop: bool
    ready_for_multi_step_agent_loop: bool
    ready_for_autonomous_retry_loop: bool
    ready_for_dominion_runtime: bool
    production_certified: bool


@dataclass(frozen=True)
class V043UserOperationPilotHandoffUpdate:
    handoff_id: str
    target_version: str
    recommended_focus: tuple[str, ...]
    still_closed: tuple[str, ...]


@dataclass(frozen=True)
class V0428IntegratedRestoreSection:
    section_id: str
    title: str
    required: bool


@dataclass(frozen=True)
class V0428IntegratedRestoreContextSnapshot:
    snapshot_id: str
    current_version: str
    current_track: str
    baseline_versions: tuple[str, ...]
    user_observed_failures: tuple[str, ...]
    still_closed: tuple[str, ...]
    integrated_doc_path: str
    next_recommended_version: str


@dataclass(frozen=True)
class V0428IntegratedRestorePacket:
    packet_id: str
    context_snapshot: V0428IntegratedRestoreContextSnapshot
    sections: tuple[V0428IntegratedRestoreSection, ...]
    single_integrated_doc_path: str
    separate_restore_doc_created: bool


@dataclass(frozen=True)
class V0428IntegratedRestoreDocumentManifest:
    manifest_id: str
    integrated_doc_path: str
    integrated_doc_required: bool
    separate_restore_doc_allowed: bool
    separate_restore_doc_created: bool
    copy_paste_restore_prompt_required: bool
    required_sections_present: bool


REQUIRED_V0428_DOC_SECTIONS: tuple[str, ...] = (
    "Restore Purpose",
    "One-Screen Restore Summary",
    "Current Version and Track Identity",
    "Project Context for New Codex Session",
    "User-observed Failure Evidence",
    "Provider Connectivity Baseline",
    "Configured Provider Empty Response Bug",
    "Direct LM Studio Response Shape Observation",
    "Runtime Identity Stabilization",
    "Provider Response Parser Contract",
    "Empty Response Handling Contract",
    "Run-report Response Fields",
    "Response Parse Trace Events",
    "Session Append Policy",
    "Command Surface Stabilization",
    "Reasoning Model Troubleshooting Guide",
    "Still-Closed Capabilities",
    "Required Test Commands",
    "Manual Test Commands",
    "Withdrawal Conditions",
    "v0.43 Recommended Next Step",
    "Copy-Paste Restore Prompt for Future GPT/Codex Session",
)

V0428_STILL_CLOSED: tuple[str, ...] = (
    "provider_doctor_completion",
    "provider_tool_calling",
    "function_calling",
    "shell_execution",
    "file_edit",
    "patch_apply",
    "arbitrary_file_read",
    "broad_filesystem_scan",
    "repo_search",
    "subagent_invocation",
    "general_agent_loop",
    "multi_step_agent_loop",
    "autonomous_retry_loop",
    "dominion_runtime",
    "production_certification",
)


def _merge(defaults: Mapping[str, Any], overrides: Mapping[str, Any]) -> dict[str, Any]:
    merged = dict(defaults)
    merged.update(overrides)
    return merged


def _json_ready(value: Any) -> Any:
    if is_dataclass(value):
        return {key: _json_ready(item) for key, item in asdict(value).items()}
    if isinstance(value, tuple):
        return [_json_ready(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _json_ready(item) for key, item in value.items()}
    return value


def _first_choice(response: Mapping[str, Any]) -> Mapping[str, Any] | None:
    choices = response.get("choices")
    if not isinstance(choices, list) or not choices:
        return None
    first = choices[0]
    return first if isinstance(first, Mapping) else None


def _usage_int(response: Mapping[str, Any], key: str) -> int | None:
    usage = response.get("usage")
    if not isinstance(usage, Mapping):
        return None
    value = usage.get(key)
    return int(value) if isinstance(value, int) else None


def _text_or_none(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def create_v042_provider_response_parse_policy(**overrides: Any) -> V042ProviderResponseParsePolicy:
    defaults = {
        "policy_id": "v042-provider-response-parse-policy",
        "prefer_message_content": True,
        "allow_text_fallback": True,
        "allow_output_text_fallback": True,
        "allow_delta_content_fallback": False,
        "allow_reasoning_content_as_final": False,
        "treat_empty_content_as_failure": True,
        "capture_reasoning_as_diagnostic": True,
        "max_diagnostic_chars": 400,
    }
    return V042ProviderResponseParsePolicy(**_merge(defaults, overrides))


def summarize_v042_provider_response_shape(response: Any, **overrides: Any) -> V042ProviderResponseShapeSummary:
    data = response if isinstance(response, Mapping) else {}
    choices = data.get("choices")
    choices_count = len(choices) if isinstance(choices, list) else 0
    first = _first_choice(data)
    message = first.get("message") if first else None
    message_map = message if isinstance(message, Mapping) else {}
    delta = first.get("delta") if first else None
    delta_map = delta if isinstance(delta, Mapping) else {}
    defaults = {
        "summary_id": "v042-provider-response-shape-summary",
        "has_choices": isinstance(choices, list) and choices_count > 0,
        "choices_count": choices_count,
        "has_message": isinstance(message, Mapping),
        "has_message_content": "content" in message_map and message_map.get("content") is not None,
        "has_text": bool(first and first.get("text") is not None),
        "has_reasoning_content": bool(
            message_map.get("reasoning_content") is not None or message_map.get("reasoning") is not None
        ),
        "has_delta_content": bool(delta_map.get("content") is not None),
        "has_output_text": data.get("output_text") is not None,
        "finish_reason": str(first.get("finish_reason")) if first and first.get("finish_reason") is not None else None,
        "provider_model": str(data.get("model")) if data.get("model") is not None else None,
        "prompt_tokens": _usage_int(data, "prompt_tokens"),
        "completion_tokens": _usage_int(data, "completion_tokens"),
        "total_tokens": _usage_int(data, "total_tokens"),
        "raw_shape_label": "openai_chat_completion" if isinstance(choices, list) else type(response).__name__,
    }
    return V042ProviderResponseShapeSummary(**_merge(defaults, overrides))


def parse_v042_openai_compatible_response(
    response: Any,
    policy: V042ProviderResponseParsePolicy | None = None,
    **overrides: Any,
) -> V042ProviderResponseParseResult:
    policy = policy or create_v042_provider_response_parse_policy()
    try:
        if not isinstance(response, Mapping):
            summary = summarize_v042_provider_response_shape(response)
            return _parse_result(
                summary,
                V042ProviderResponseParseStatus.INVALID_RESPONSE_SHAPE.value,
                V042ProviderResponseErrorClass.PROVIDER_INVALID_RESPONSE.value,
                "",
                None,
                "provider response was not a JSON object",
                **overrides,
            )
        summary = summarize_v042_provider_response_shape(response)
        first = _first_choice(response)
        if first is None:
            return _parse_result(
                summary,
                V042ProviderResponseParseStatus.MISSING_CHOICES.value,
                V042ProviderResponseErrorClass.PROVIDER_INVALID_RESPONSE.value,
                "",
                None,
                "response did not contain choices[0]",
                **overrides,
            )
        message = first.get("message")
        message_map = message if isinstance(message, Mapping) else None
        reasoning = None
        if message_map is not None:
            reasoning = _text_or_none(message_map.get("reasoning_content") or message_map.get("reasoning"))
        extracted_from: str | None = None
        text: str | None = None
        final_field_seen = False
        if policy.prefer_message_content:
            if message_map is None:
                if first.get("text") is None and response.get("output_text") is None:
                    return _parse_result(
                        summary,
                        V042ProviderResponseParseStatus.MISSING_MESSAGE.value,
                        V042ProviderResponseErrorClass.PROVIDER_INVALID_RESPONSE.value,
                        "",
                        None,
                        "choices[0].message was missing",
                        **overrides,
                    )
            elif "content" in message_map:
                final_field_seen = True
                text = _text_or_none(message_map.get("content"))
                extracted_from = "choices[0].message.content"
        if (text is None or text == "") and policy.allow_text_fallback and first.get("text") is not None:
            final_field_seen = True
            text = _text_or_none(first.get("text"))
            extracted_from = "choices[0].text"
        if (text is None or text == "") and policy.allow_output_text_fallback and response.get("output_text") is not None:
            final_field_seen = True
            text = _text_or_none(response.get("output_text"))
            extracted_from = "output_text"
        delta = first.get("delta")
        if (
            (text is None or text == "")
            and policy.allow_delta_content_fallback
            and isinstance(delta, Mapping)
            and delta.get("content") is not None
        ):
            final_field_seen = True
            text = _text_or_none(delta.get("content"))
            extracted_from = "choices[0].delta.content"
        if text is None:
            if reasoning:
                return _parse_result(
                    summary,
                    V042ProviderResponseParseStatus.PROVIDER_REASONING_WITHOUT_FINAL.value,
                    V042ProviderResponseErrorClass.PROVIDER_REASONING_WITHOUT_FINAL.value,
                    "",
                    None,
                    "reasoning content detected but no final assistant content field was present",
                    **overrides,
                )
            return _parse_result(
                summary,
                V042ProviderResponseParseStatus.MISSING_CONTENT.value if final_field_seen is False else V042ProviderResponseParseStatus.PARSED_EMPTY.value,
                V042ProviderResponseErrorClass.RESPONSE_PARSE_EMPTY.value,
                "",
                extracted_from,
                "no final assistant content was present",
                **overrides,
            )
        assistant_text = text.strip()
        if not assistant_text and policy.treat_empty_content_as_failure:
            status = (
                V042ProviderResponseParseStatus.PROVIDER_REASONING_WITHOUT_FINAL.value
                if reasoning and not policy.allow_reasoning_content_as_final
                else V042ProviderResponseParseStatus.PARSED_EMPTY.value
            )
            error = (
                V042ProviderResponseErrorClass.PROVIDER_REASONING_WITHOUT_FINAL.value
                if status == V042ProviderResponseParseStatus.PROVIDER_REASONING_WITHOUT_FINAL.value
                else V042ProviderResponseErrorClass.PROVIDER_EMPTY_RESPONSE.value
            )
            return _parse_result(
                summary,
                status,
                error,
                "",
                extracted_from,
                "final assistant content was empty or whitespace",
                **overrides,
            )
        return _parse_result(
            summary,
            V042ProviderResponseParseStatus.PARSED.value,
            V042ProviderResponseErrorClass.NONE.value,
            assistant_text,
            extracted_from,
            "final assistant content parsed",
            **overrides,
        )
    except Exception as exc:  # pragma: no cover - defensive parser boundary
        summary = summarize_v042_provider_response_shape(response)
        return _parse_result(
            summary,
            V042ProviderResponseParseStatus.PARSE_ERROR.value,
            V042ProviderResponseErrorClass.RESPONSE_PARSE_ERROR.value,
            "",
            None,
            f"parser exception: {exc}",
            **overrides,
        )


def _parse_result(
    summary: V042ProviderResponseShapeSummary,
    status: str,
    error_class: str,
    assistant_text: str,
    extracted_from_field: str | None,
    diagnostic_summary: str,
    **overrides: Any,
) -> V042ProviderResponseParseResult:
    content_length = len(assistant_text)
    defaults = {
        "result_id": "v042-provider-response-parse-result",
        "status": status,
        "error_class": error_class,
        "assistant_text": assistant_text,
        "assistant_text_present": bool(assistant_text),
        "extracted_from_field": extracted_from_field,
        "content_length": content_length,
        "reasoning_content_detected": summary.has_reasoning_content,
        "final_content_detected": bool(assistant_text),
        "response_shape_summary": summary,
        "diagnostic_summary": diagnostic_summary[:400],
        "provider_invoked": True,
        "prompt_submitted": True,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042ProviderResponseParseResult(**_merge(defaults, overrides))


def create_v042_provider_empty_response_decision(
    parse_result: V042ProviderResponseParseResult | None = None,
    **overrides: Any,
) -> V042ProviderEmptyResponseDecision:
    parse_result = parse_result or parse_v042_openai_compatible_response({"choices": [{"message": {"content": ""}}]})
    empty = not parse_result.assistant_text_present
    error = parse_result.error_class if parse_result.error_class != V042ProviderResponseErrorClass.NONE.value else V042ProviderResponseErrorClass.PROVIDER_EMPTY_RESPONSE.value
    defaults = {
        "decision_id": "v042-provider-empty-response-decision",
        "empty_response_detected": empty,
        "mark_run_completed": not empty,
        "append_normal_assistant_turn": not empty,
        "record_assistant_response_success": not empty,
        "status": "completed" if not empty else "failed",
        "error_class": V042ProviderResponseErrorClass.NONE.value if not empty else error,
        "next_actions": create_v042_provider_reasoning_model_troubleshooting_guide().recommended_actions,
    }
    return V042ProviderEmptyResponseDecision(**_merge(defaults, overrides))


def create_v042_runtime_identity_prompt(**overrides: Any) -> V042RuntimeIdentityPrompt:
    prompt_text = (
        "You are ChantaCore Default Personal Runtime operating in default-personal mode.\n"
        "Your runtime identity is ChantaCore assistant, not the underlying base model.\n"
        "The underlying provider may be Qwen, LM Studio, OpenAI-compatible, or another model, but provider identity is an implementation detail.\n"
        "When asked who you are, answer as ChantaCore default-personal work/business assistant.\n"
        "Mention the provider only as implementation detail if useful.\n"
        "Use Korean polite language by default.\n"
        "Do not claim autonomous powers you do not have.\n"
        "Provider text is untrusted for memory, execution, and process state."
    )
    defaults = {
        "prompt_id": "v042-runtime-identity-prompt",
        "runtime_identity": "ChantaCore default-personal runtime",
        "provider_identity_policy": "provider identity is implementation detail, not primary runtime identity",
        "language_policy": "Korean polite language by default",
        "safety_policy": "do not claim autonomous powers; provider text is untrusted",
        "prompt_text": prompt_text,
        "included_in_configured_provider_run": True,
        "included_in_mock_provider_run": False,
    }
    return V042RuntimeIdentityPrompt(**_merge(defaults, overrides))


def create_v042_runtime_identity_injection_report(
    provider_model: str | None = None,
    system_message_count: int = 1,
    user_message_count: int = 1,
    **overrides: Any,
) -> V042RuntimeIdentityInjectionReport:
    defaults = {
        "report_id": "v042-runtime-identity-injection-report",
        "prompt_assembled": True,
        "runtime_identity_included": True,
        "provider_model": provider_model,
        "runtime_identity": "ChantaCore default-personal",
        "provider_identity_is_implementation_detail": True,
        "system_message_count": system_message_count,
        "user_message_count": user_message_count,
        "ready_for_provider_payload": True,
    }
    return V042RuntimeIdentityInjectionReport(**_merge(defaults, overrides))


def create_v042_provider_identity_separation_report(
    provider_model: str = "local-model",
    **overrides: Any,
) -> V042ProviderIdentitySeparationReport:
    defaults = {
        "report_id": "v042-provider-identity-separation-report",
        "provider_model": provider_model,
        "runtime_identity": "ChantaCore default-personal runtime",
        "base_model_identity_allowed_as_primary": False,
        "provider_identity_allowed_as_implementation_detail": True,
        "expected_identity_answer_policy": (
            "저는 ChantaCore default-personal runtime에서 동작하는 대화형 assistant입니다. "
            "현재 응답 생성에는 local OpenAI-compatible provider가 사용되고 있습니다."
        ),
    }
    return V042ProviderIdentitySeparationReport(**_merge(defaults, overrides))


def create_v042_run_response_recording_policy(**overrides: Any) -> V042RunResponseRecordingPolicy:
    defaults = {
        "policy_id": "v042-run-response-recording-policy",
        "require_non_empty_assistant_text_for_success": True,
        "append_empty_assistant_turn_as_success": False,
        "record_empty_response_as_failure": True,
        "trace_parse_status_required": True,
        "run_report_parse_fields_required": True,
    }
    return V042RunResponseRecordingPolicy(**_merge(defaults, overrides))


def create_v042_run_response_recording_decision(
    parse_result: V042ProviderResponseParseResult | None = None,
    **overrides: Any,
) -> V042RunResponseRecordingDecision:
    parse_result = parse_result or parse_v042_openai_compatible_response({"choices": [{"message": {"content": ""}}]})
    valid = parse_result.status == V042ProviderResponseParseStatus.PARSED.value and parse_result.assistant_text_present
    defaults = {
        "decision_id": "v042-run-response-recording-decision",
        "parse_result": parse_result,
        "should_append_assistant_turn": valid,
        "should_record_assistant_response_success": valid,
        "run_status": "completed" if valid else "failed",
        "response_valid": valid,
        "error_class": V042ProviderResponseErrorClass.NONE.value if valid else parse_result.error_class,
        "normal_assistant_turn_appended": valid,
    }
    return V042RunResponseRecordingDecision(**_merge(defaults, overrides))


def create_v042_configured_run_failure_report(
    run_id: str | None = None,
    session_id: str | None = None,
    parse_result: V042ProviderResponseParseResult | None = None,
    provider_model: str | None = None,
    base_url: str | None = None,
    timeout_seconds: int | None = None,
    **overrides: Any,
) -> V042ConfiguredRunFailureReport:
    parse_result = parse_result or parse_v042_openai_compatible_response({"choices": [{"message": {"content": ""}}]})
    defaults = {
        "report_id": "v042-configured-run-failure-report",
        "run_id": run_id,
        "session_id": session_id,
        "error_class": parse_result.error_class,
        "response_parse_status": parse_result.status,
        "provider_model": provider_model or parse_result.response_shape_summary.provider_model,
        "base_url": base_url,
        "timeout_seconds": timeout_seconds,
        "next_actions": create_v042_provider_reasoning_model_troubleshooting_guide().recommended_actions,
        "provider_invoked": True,
        "prompt_submitted": True,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042ConfiguredRunFailureReport(**_merge(defaults, overrides))


def create_v042_run_report_response_fields(
    parse_result: V042ProviderResponseParseResult | None = None,
    runtime_identity_included: bool | None = True,
    provider_identity_is_implementation_detail: bool | None = True,
    **overrides: Any,
) -> V042RunReportResponseFields:
    if parse_result is None:
        defaults = {
            "response_parse_status": None,
            "response_error_class": None,
            "response_extracted_from_field": None,
            "response_content_length": None,
            "response_finish_reason": None,
            "provider_model": None,
            "runtime_identity_included": None,
            "provider_identity_is_implementation_detail": None,
            "empty_response_detected": None,
            "next_action": None,
        }
    else:
        guide = create_v042_provider_reasoning_model_troubleshooting_guide()
        defaults = {
            "response_parse_status": parse_result.status,
            "response_error_class": parse_result.error_class,
            "response_extracted_from_field": parse_result.extracted_from_field,
            "response_content_length": parse_result.content_length,
            "response_finish_reason": parse_result.response_shape_summary.finish_reason,
            "provider_model": parse_result.response_shape_summary.provider_model,
            "runtime_identity_included": runtime_identity_included,
            "provider_identity_is_implementation_detail": provider_identity_is_implementation_detail,
            "empty_response_detected": not parse_result.assistant_text_present,
            "next_action": "; ".join(guide.recommended_actions[:4]) if not parse_result.assistant_text_present else None,
        }
    return V042RunReportResponseFields(**_merge(defaults, overrides))


def create_v042_response_parse_trace_record(
    parse_result: V042ProviderResponseParseResult | None = None,
    run_id: str | None = None,
    session_id: str | None = None,
    **overrides: Any,
) -> V042ResponseParseTraceRecord:
    parse_result = parse_result or parse_v042_openai_compatible_response({"choices": [{"message": {"content": "ok"}}]})
    event_kind = "provider_text_response_parsed" if parse_result.status == V042ProviderResponseParseStatus.PARSED.value else "provider_text_response_parse_failed"
    if not parse_result.assistant_text_present:
        event_kind = "provider_text_response_empty"
    defaults = {
        "trace_record_id": "v042-response-parse-trace-record",
        "event_kind": event_kind,
        "run_id": run_id,
        "session_id": session_id,
        "response_parse_status": parse_result.status,
        "error_class": parse_result.error_class,
        "content_length": parse_result.content_length,
        "extracted_from_field": parse_result.extracted_from_field,
        "provider_model": parse_result.response_shape_summary.provider_model,
        "shell_executed": False,
        "subagent_invoked": False,
        "production_certified": False,
    }
    return V042ResponseParseTraceRecord(**_merge(defaults, overrides))


def create_v042_command_surface_stabilization_policy(**overrides: Any) -> V042CommandSurfaceStabilizationPolicy:
    defaults = {
        "policy_id": "v042-command-surface-stabilization-policy",
        "preserve_direct_run_command": True,
        "run_show_last_supported": True,
        "run_history_supported": True,
        "session_show_last_supported": True,
        "unrecognized_show_args_redirected": True,
        "help_priority_over_validation": True,
    }
    return V042CommandSurfaceStabilizationPolicy(**_merge(defaults, overrides))


def create_v042_command_surface_stabilization_result(**overrides: Any) -> V042CommandSurfaceStabilizationResult:
    defaults = {
        "result_id": "v042-command-surface-stabilization-result",
        "run_help_fixed": True,
        "run_show_last_no_longer_unrecognized": True,
        "run_history_available_or_redirected": True,
        "session_show_last_available_or_redirected": True,
        "direct_run_preserved": True,
        "user_guidance_text": "Use chanta-cli run show last, chanta-cli run history, or chanta-cli session show last for inspection.",
    }
    return V042CommandSurfaceStabilizationResult(**_merge(defaults, overrides))


def create_v042_provider_reasoning_model_troubleshooting_guide(**overrides: Any) -> V042ProviderReasoningModelTroubleshootingGuide:
    defaults = {
        "guide_id": "v042-provider-reasoning-model-troubleshooting-guide",
        "symptoms": (
            "completion tokens exist but message.content is empty",
            "choices[0].message.content is missing, null, or whitespace",
            "reasoning_content exists without final answer content",
        ),
        "likely_causes": (
            "reasoning-heavy local model generated internal tokens but no final answer",
            "LM Studio chat template did not emit final assistant content",
            "PowerShell top-level rendering hid nested message fields",
            "max_tokens was too small for the model to reach a final answer",
        ),
        "recommended_actions": (
            "inspect raw provider response JSON",
            "increase max_tokens",
            "ask for final answer only",
            "check LM Studio model/template settings",
            "try a smaller model",
            "run provider connectivity to confirm model id",
            "run a direct /chat/completions test",
            "do not treat empty response as completed success",
        ),
        "safe_commands": (
            "chanta-cli provider connectivity",
            "chanta-cli run-report last",
            "chanta-cli trace timeline --limit 20",
        ),
        "unsafe_actions_not_taken": (
            "provider tool calling",
            "function calling",
            "shell execution",
            "subagent invocation",
            "production certification",
        ),
    }
    return V042ProviderReasoningModelTroubleshootingGuide(**_merge(defaults, overrides))


def create_v0428_readiness_report(**overrides: Any) -> V0428ReadinessReport:
    defaults = {
        "provider_response_parser_ready": True,
        "empty_response_detection_ready": True,
        "configured_run_failure_classification_ready": True,
        "runtime_identity_prompt_ready": True,
        "provider_identity_separation_ready": True,
        "run_report_response_fields_ready": True,
        "response_parse_trace_ready": True,
        "command_surface_stabilization_ready": True,
        "reasoning_model_troubleshooting_ready": True,
        "integrated_restore_document_ready": True,
        "v043_handoff_update_ready": True,
        "ready_for_provider_doctor_completion": False,
        "ready_for_provider_tool_calling": False,
        "ready_for_function_calling": False,
        "ready_for_shell_execution": False,
        "ready_for_file_edit": False,
        "ready_for_patch_apply": False,
        "ready_for_arbitrary_file_read": False,
        "ready_for_broad_filesystem_scan": False,
        "ready_for_repo_search": False,
        "ready_for_subagent_invocation": False,
        "ready_for_general_agent_loop": False,
        "ready_for_multi_step_agent_loop": False,
        "ready_for_autonomous_retry_loop": False,
        "ready_for_dominion_runtime": False,
        "production_certified": False,
    }
    return V0428ReadinessReport(**_merge(defaults, overrides))


def create_v043_user_operation_pilot_handoff_update(**overrides: Any) -> V043UserOperationPilotHandoffUpdate:
    defaults = {
        "handoff_id": "v043-user-operation-pilot-handoff-update",
        "target_version": "v0.43.0 User Operation Pilot",
        "recommended_focus": (
            "manual user operation pilot",
            "provider response quality observations",
            "session/run/trace review loop",
            "no new high-risk runtime powers until v0.42 UX evidence is stable",
        ),
        "still_closed": V0428_STILL_CLOSED,
    }
    return V043UserOperationPilotHandoffUpdate(**_merge(defaults, overrides))


def create_v0428_integrated_restore_context_snapshot(**overrides: Any) -> V0428IntegratedRestoreContextSnapshot:
    defaults = {
        "snapshot_id": "v0428-integrated-restore-context-snapshot",
        "current_version": V0428_RELEASE_NAME,
        "current_track": V0428_TRACK_NAME,
        "baseline_versions": (
            "v0.41.6 installable default-personal runtime",
            "v0.42.7 provider connectivity and chat UX stabilization",
        ),
        "user_observed_failures": (
            'assistant_response_preview="" with status="completed"',
            "configured provider returned empty visible assistant response",
            "runtime identity sometimes answered as base model identity",
            "chanta-cli run show last produced confusing argparse error",
        ),
        "still_closed": V0428_STILL_CLOSED,
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "next_recommended_version": "v0.43.0 User Operation Pilot",
    }
    return V0428IntegratedRestoreContextSnapshot(**_merge(defaults, overrides))


def create_v0428_integrated_restore_packet(**overrides: Any) -> V0428IntegratedRestorePacket:
    sections = tuple(V0428IntegratedRestoreSection(section.lower().replace(" ", "_").replace("-", "_"), section, True) for section in REQUIRED_V0428_DOC_SECTIONS)
    defaults = {
        "packet_id": "v0428-integrated-restore-packet",
        "context_snapshot": create_v0428_integrated_restore_context_snapshot(),
        "sections": sections,
        "single_integrated_doc_path": INTEGRATED_DOC_PATH,
        "separate_restore_doc_created": False,
    }
    return V0428IntegratedRestorePacket(**_merge(defaults, overrides))


def create_v0428_integrated_restore_document_manifest(**overrides: Any) -> V0428IntegratedRestoreDocumentManifest:
    path = Path(INTEGRATED_DOC_PATH)
    text = path.read_text(encoding="utf-8") if path.exists() else ""
    required_present = bool(text) and all(f"## {section}" in text for section in REQUIRED_V0428_DOC_SECTIONS)
    forbidden_docs = [
        Path("docs/versions/v0.42/v0.42.8_restore_document.md"),
        Path("docs/versions/v0.42/v0.42.8_provider_response.md"),
        Path("docs/versions/v0.42/v0.42.8_runtime_identity.md"),
        Path("docs/versions/v0.42/v0.42.8_command_surface.md"),
    ]
    defaults = {
        "manifest_id": "v0428-integrated-restore-document-manifest",
        "integrated_doc_path": INTEGRATED_DOC_PATH,
        "integrated_doc_required": True,
        "separate_restore_doc_allowed": False,
        "separate_restore_doc_created": any(item.exists() for item in forbidden_docs),
        "copy_paste_restore_prompt_required": True,
        "required_sections_present": required_present,
    }
    return V0428IntegratedRestoreDocumentManifest(**_merge(defaults, overrides))


def _run_with_v0423_command_surface(args: Sequence[str]) -> int | None:
    if len(args) >= 2 and args[0] == "run" and args[1] in {"show", "history"}:
        from chanta_core.personal_runtime.default_personal_trace_history import main as v0423_main

        return v0423_main(args)
    if len(args) >= 2 and args[0] == "session" and args[1] == "show":
        from chanta_core.personal_runtime.default_personal_trace_history import main as v0423_main

        return v0423_main(args)
    return None


def main(argv: Sequence[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    if args and args[0] in {"--version", "version"}:
        print(f"chanta-cli v0.41.1 (runtime {V0428_VERSION}; {V0428_RELEASE_NAME})")
        return 0
    routed = _run_with_v0423_command_surface(args)
    if routed is not None:
        return routed
    from chanta_core.personal_runtime.default_personal_provider_connectivity import main as v0427_main

    return v0427_main(args)


__all__ = [
    name
    for name in globals()
    if name.startswith("V042")
    or name.startswith("V043")
    or name.startswith("create_v042")
    or name.startswith("create_v043")
    or name.startswith("parse_v042")
    or name.startswith("summarize_v042")
    or name == "main"
]
