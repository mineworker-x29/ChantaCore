import inspect

import pytest

from chanta_core.agent_runtime import (
    ModelRawResponseRef,
    ModelResponseActionSignal,
    ModelResponseActionSignalKind,
    ModelResponseDataSensitivityKind,
    ModelResponseEnvelope,
    ModelResponseEnvelopeInput,
    ModelResponseEnvelopeKind,
    ModelResponseEnvelopeReport,
    ModelResponseFlagSet,
    ModelResponseNoExecutionGuarantee,
    ModelResponsePayloadFormat,
    ModelResponseReadinessLevel,
    ModelResponseRedactionRule,
    ModelResponseRiskKind,
    ModelResponseRiskSignal,
    ModelResponseRunPreview,
    ModelResponseSanitizationDecisionKind,
    ModelResponseSanitizationPolicy,
    ModelResponseSanitizationReport,
    ModelResponseSourceKind,
    ModelResponseSourceRef,
    ModelResponseStatus,
    ModelResponseValidationReport,
    ModelSanitizedResponsePayload,
    V0343ReadinessReport,
    build_model_raw_response_ref,
    build_model_response_action_signal,
    build_model_response_envelope,
    build_model_response_envelope_from_supplied_text,
    build_model_response_envelope_input,
    build_model_response_envelope_report,
    build_model_response_flags,
    build_model_response_no_execution_guarantee,
    build_model_response_redaction_rule,
    build_model_response_risk_signal,
    build_model_response_run_preview,
    build_model_response_sanitization_policy,
    build_model_response_sanitization_report,
    build_model_response_source_ref,
    build_model_response_validation_report,
    build_model_sanitized_response_payload,
    build_v0343_readiness_report,
    default_model_response_redaction_rules,
    default_model_response_sanitization_policy,
    detect_model_response_action_signals,
    detect_model_response_risk_signals,
    model_raw_response_ref_is_not_persistence,
    model_response_envelope_is_not_action,
    model_response_flags_preserve_execution_false,
    model_response_validation_report_blocks_action_execution,
    sanitize_model_response_text,
    v0343_readiness_report_is_not_execution_ready,
    validate_model_response_envelope,
)
from chanta_core.agent_runtime import model_response as response_module


def test_v0343_taxonomies_cover_required_values() -> None:
    assert ModelResponseEnvelopeKind.SUPPLIED_RESPONSE_ENVELOPE.value == "supplied_response_envelope"
    assert ModelResponseEnvelopeKind.FUTURE_PROVIDER_RESPONSE_ENVELOPE.value == "future_provider_response_envelope"
    assert ModelResponsePayloadFormat.JSON_LIKE_RESPONSE.value == "json_like_response"
    assert ModelResponsePayloadFormat.REDACTED_PREVIEW_ONLY.value == "redacted_preview_only"
    assert ModelResponseSourceKind.V0342_MODEL_REQUEST_ENVELOPE.value == "v0342_model_request_envelope"
    assert ModelResponseSourceKind.HERMES_REFERENCE_CONTEXT_REF.value == "hermes_reference_context_ref"
    assert ModelResponseStatus.SANITIZED_WITH_WARNINGS.value == "sanitized_with_warnings"
    assert ModelResponseReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0345.value == "design_handoff_ready_for_v0345"
    assert ModelResponseSanitizationDecisionKind.BLOCK_UNSAFE_ACTION_SIGNAL.value == "block_unsafe_action_signal"
    assert ModelResponseRiskKind.COMMAND_EXECUTION_SUGGESTION_RISK.value == "command_execution_suggestion_risk"
    assert ModelResponseRiskKind.REFERENCE_EXECUTION_SUGGESTION_RISK.value == "reference_execution_suggestion_risk"
    assert ModelResponseDataSensitivityKind.UNTRUSTED_MODEL_OUTPUT.value == "untrusted_model_output"
    assert ModelResponseActionSignalKind.PATCH_LIKE.value == "patch_like"


def test_flags_allow_handoff_only_and_preserve_execution_false() -> None:
    flags = build_model_response_flags()
    assert isinstance(flags, ModelResponseFlagSet)
    assert flags.response_envelope_constructed is True
    assert flags.response_sanitizer_available is True
    assert flags.response_validation_available is True
    assert flags.response_action_signal_detection_available is True
    assert flags.ready_for_v0344_existing_provider_boundary_adapter is True
    assert flags.ready_for_v0345_model_output_action_quarantine is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_controlled_model_invocation is False
    assert flags.ready_for_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_existing_boundary_invocation is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_tool_calls is False
    assert flags.ready_for_function_calls is False
    assert flags.ready_for_action_execution is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_raw_response_persistence is False
    assert flags.ready_for_raw_model_output_persistence is False
    assert flags.production_certified is False
    assert model_response_flags_preserve_execution_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_controlled_model_invocation",
        "ready_for_model_invocation",
        "ready_for_provider_invocation",
        "ready_for_existing_boundary_invocation",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_action_execution",
        "ready_for_tool_calls",
        "ready_for_function_calls",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_patch_application",
        "ready_for_raw_response_persistence",
        "ready_for_raw_model_output_persistence",
    ],
)
def test_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_model_response_flags(**{unsafe_flag: True})


def test_source_ref_and_raw_ref_are_bounded_metadata_only() -> None:
    source = build_model_response_source_ref(
        "source:response:test",
        ModelResponseSourceKind.SUPPLIED_MODEL_RESPONSE,
        "response:test",
        "Supplied response ref only.",
    )
    assert isinstance(source, ModelResponseSourceRef)
    assert source.provider_call is False
    assert source.file_read is False
    assert source.credential_access is False
    assert source.execution is False

    raw_ref = build_model_raw_response_ref(source_refs=[source])
    assert isinstance(raw_ref, ModelRawResponseRef)
    assert len(raw_ref.raw_response_preview) <= response_module.DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS
    assert raw_ref.contains_secret_like_content is False
    assert raw_ref.contains_credential_like_content is False
    assert raw_ref.contains_token_like_content is False
    assert raw_ref.raw_response_persistence is False
    assert model_raw_response_ref_is_not_persistence(raw_ref)

    with pytest.raises(ValueError):
        build_model_raw_response_ref(raw_response_preview="secret=value")
    with pytest.raises(ValueError):
        build_model_raw_response_ref(contains_token_like_content=True)


def test_sanitization_policy_redaction_rule_risk_and_action_signal_are_conservative() -> None:
    policy = default_model_response_sanitization_policy()
    assert isinstance(policy, ModelResponseSanitizationPolicy)
    assert policy.allow_raw_response_persistence is False
    assert policy.allow_action_execution is False
    assert policy.block_command_like_output is True
    assert policy.block_patch_like_output is True
    assert policy.block_provider_reinvoke_like_output is True
    assert policy.block_external_harness_like_output is True

    with pytest.raises(ValueError):
        build_model_response_sanitization_policy(allow_raw_response_persistence=True)
    with pytest.raises(ValueError):
        build_model_response_sanitization_policy(allow_action_execution=True)
    with pytest.raises(ValueError):
        build_model_response_sanitization_policy(block_command_like_output=False)

    rules = default_model_response_redaction_rules()
    assert all(isinstance(rule, ModelResponseRedactionRule) for rule in rules)
    assert all(rule.credential_access is False for rule in rules)
    with pytest.raises(ValueError):
        build_model_response_redaction_rule("redaction:bad", pattern_label="secret=value")

    risk = build_model_response_risk_signal("risk:command", ModelResponseRiskKind.COMMAND_EXECUTION_SUGGESTION_RISK)
    assert isinstance(risk, ModelResponseRiskSignal)
    assert risk.execution is False
    assert risk.blocked is True or risk.requires_quarantine is True
    with pytest.raises(ValueError):
        build_model_response_risk_signal("risk:bad", blocked=False, requires_quarantine=False)

    action = build_model_response_action_signal("action:shell", ModelResponseActionSignalKind.SHELL_COMMAND_LIKE)
    assert isinstance(action, ModelResponseActionSignal)
    assert action.execution is False
    assert action.blocked_from_execution is True
    with pytest.raises(ValueError):
        build_model_response_action_signal("action:bad", ModelResponseActionSignalKind.PATCH_LIKE, blocked_from_execution=False)


def test_sanitized_payload_is_bounded_redacted_and_not_action() -> None:
    signal = build_model_response_action_signal("action:tool", ModelResponseActionSignalKind.TOOL_CALL_LIKE)
    payload = build_model_sanitized_response_payload(
        sanitized_text="bounded sanitized text",
        response_preview="bounded sanitized preview",
        action_signals=[signal],
    )
    assert isinstance(payload, ModelSanitizedResponsePayload)
    assert len(payload.sanitized_text) <= response_module.DEFAULT_MAX_SANITIZED_RESPONSE_CHARS
    assert len(payload.response_preview) <= response_module.DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS
    assert payload.raw_response_persistence is False
    assert payload.action is False

    with pytest.raises(ValueError):
        build_model_sanitized_response_payload(sanitized_text="x" * (response_module.DEFAULT_MAX_SANITIZED_RESPONSE_CHARS + 1))
    with pytest.raises(ValueError):
        build_model_sanitized_response_payload(response_preview="x" * (response_module.DEFAULT_MAX_RAW_RESPONSE_PREVIEW_CHARS + 1))


def test_envelope_input_and_envelope_are_not_provider_invocation_or_action() -> None:
    envelope_input = build_model_response_envelope_input(supplied_response_text="safe response text")
    assert isinstance(envelope_input, ModelResponseEnvelopeInput)
    assert envelope_input.provider_invocation_request is False
    assert envelope_input.action_execution_request is False

    envelope = build_model_response_envelope()
    assert isinstance(envelope, ModelResponseEnvelope)
    assert envelope.ready_for_v0344_existing_provider_boundary_adapter is True
    assert envelope.ready_for_v0345_model_output_action_quarantine is True
    assert envelope.ready_for_invocation is False
    assert envelope.ready_for_action_execution is False
    assert envelope.ready_for_provider_invocation is False
    assert envelope.ready_for_execution is False
    assert envelope.provider_call is False
    assert envelope.action is False
    assert model_response_envelope_is_not_action(envelope)

    with pytest.raises(ValueError):
        build_model_response_envelope(ready_for_action_execution=True)
    with pytest.raises(ValueError):
        build_model_response_envelope(ready_for_provider_invocation=True)


def test_sanitization_validation_and_envelope_reports_are_not_execution() -> None:
    envelope = build_model_response_envelope_from_supplied_text("Please run command powershell and apply a patch file.")
    sanitization_report = build_model_response_sanitization_report(
        response_envelope_id=envelope.response_envelope_id,
        sanitized_payload_id=envelope.sanitized_payload.sanitized_payload_id,
        risk_signals=envelope.sanitized_payload.risk_signals,
        action_signals=envelope.sanitized_payload.action_signals,
        requires_quarantine=True,
    )
    assert isinstance(sanitization_report, ModelResponseSanitizationReport)
    assert sanitization_report.ready_for_action_execution is False
    assert sanitization_report.ready_for_execution is False
    assert sanitization_report.action_permission is False

    validation_report = validate_model_response_envelope(envelope)
    assert isinstance(validation_report, ModelResponseValidationReport)
    assert validation_report.action_signals_blocked is True
    assert validation_report.raw_persistence_blocked is True
    assert validation_report.ready_for_action_execution is False
    assert validation_report.ready_for_provider_invocation is False
    assert validation_report.ready_for_execution is False
    assert validation_report.execution_certification is False
    assert model_response_validation_report_blocks_action_execution(validation_report)

    envelope_report = build_model_response_envelope_report()
    assert isinstance(envelope_report, ModelResponseEnvelopeReport)
    assert envelope_report.ready_for_v0344_existing_provider_boundary_adapter is True
    assert envelope_report.ready_for_v0345_model_output_action_quarantine is True
    assert envelope_report.ready_for_invocation is False
    assert envelope_report.ready_for_action_execution is False
    assert envelope_report.ready_for_provider_invocation is False
    assert envelope_report.ready_for_execution is False
    assert envelope_report.execution is False

    with pytest.raises(ValueError):
        build_model_response_sanitization_report(ready_for_action_execution=True)
    with pytest.raises(ValueError):
        build_model_response_validation_report(action_signals_blocked=False)
    with pytest.raises(ValueError):
        build_model_response_validation_report(raw_persistence_blocked=False)
    with pytest.raises(ValueError):
        build_model_response_validation_report(blocked_reasons=["blocked"], validation_passed=True)


def test_run_preview_guarantee_and_readiness_are_conservative() -> None:
    preview = build_model_response_run_preview()
    assert isinstance(preview, ModelResponseRunPreview)
    assert preview.execution is False
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_model_response_no_execution_guarantee()
    assert isinstance(guarantee, ModelResponseNoExecutionGuarantee)
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0343_readiness_report()
    assert isinstance(readiness, V0343ReadinessReport)
    assert readiness.ready_for_v0344_existing_provider_boundary_adapter is True
    assert readiness.ready_for_v0345_model_output_action_quarantine is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_controlled_model_invocation is False
    assert readiness.ready_for_model_invocation is False
    assert readiness.ready_for_provider_invocation is False
    assert readiness.ready_for_action_execution is False
    assert readiness.ready_for_tool_calls is False
    assert readiness.ready_for_function_calls is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_patch_application is False
    assert readiness.ready_for_raw_response_persistence is False
    assert readiness.ready_for_raw_model_output_persistence is False
    assert v0343_readiness_report_is_not_execution_ready(readiness)

    with pytest.raises(ValueError):
        build_v0343_readiness_report(ready_for_model_invocation=True)
    with pytest.raises(ValueError):
        build_v0343_readiness_report(ready_for_action_execution=True)
    with pytest.raises(ValueError):
        build_v0343_readiness_report(ready_for_raw_response_persistence=True)


def test_sanitizer_redacts_and_detects_unsafe_response_signals() -> None:
    raw = (
        "secret=value token=abc key=123 api_key=456 password=pw "
        "run command powershell; diff --git; tool_call; function_call; "
        "call openai; fetch url https://example.test; credential request; "
        "run Hermes external harness; import references/module; grant authority D9"
    )
    payload = sanitize_model_response_text(raw)
    assert "value" not in payload.sanitized_text
    assert "token=abc" not in payload.sanitized_text
    assert "api_key=456" not in payload.sanitized_text
    assert payload.redacted is True
    assert payload.action is False

    action_kinds = {signal.signal_kind for signal in payload.action_signals}
    assert ModelResponseActionSignalKind.SHELL_COMMAND_LIKE in action_kinds
    assert ModelResponseActionSignalKind.PATCH_LIKE in action_kinds
    assert ModelResponseActionSignalKind.TOOL_CALL_LIKE in action_kinds
    assert ModelResponseActionSignalKind.FUNCTION_CALL_LIKE in action_kinds
    assert ModelResponseActionSignalKind.PROVIDER_REINVOKE_LIKE in action_kinds
    assert ModelResponseActionSignalKind.NETWORK_ACCESS_LIKE in action_kinds
    assert ModelResponseActionSignalKind.CREDENTIAL_REQUEST_LIKE in action_kinds
    assert ModelResponseActionSignalKind.EXTERNAL_HARNESS_EXECUTE_LIKE in action_kinds
    assert ModelResponseActionSignalKind.REFERENCE_CODE_EXECUTE_LIKE in action_kinds
    assert all(signal.blocked_from_execution for signal in payload.action_signals)

    risk_kinds = {risk.risk_kind for risk in payload.risk_signals}
    assert ModelResponseRiskKind.SECRET_IN_RESPONSE_RISK in risk_kinds
    assert ModelResponseRiskKind.TOKEN_IN_RESPONSE_RISK in risk_kinds
    assert ModelResponseRiskKind.CREDENTIAL_IN_RESPONSE_RISK in risk_kinds

    assert detect_model_response_action_signals(raw)
    assert detect_model_response_risk_signals(raw)


def test_build_response_envelope_from_supplied_text_uses_no_provider_call() -> None:
    envelope = build_model_response_envelope_from_supplied_text("safe final answer only")
    assert isinstance(envelope, ModelResponseEnvelope)
    assert envelope.envelope_kind == ModelResponseEnvelopeKind.SUPPLIED_RESPONSE_ENVELOPE
    assert envelope.raw_response_ref is not None
    assert envelope.provider_call is False
    assert envelope.action is False
    assert envelope.ready_for_action_execution is False
    assert envelope.ready_for_provider_invocation is False
    assert model_response_envelope_is_not_action(envelope)


def test_direct_dataclass_construction_with_valid_inputs() -> None:
    source = ModelResponseSourceRef(
        source_ref_id="source:direct",
        source_kind=ModelResponseSourceKind.TEST_FIXTURE,
        source_id="fixture",
        source_summary="fixture response source only",
        sensitivity=ModelResponseDataSensitivityKind.UNTRUSTED_MODEL_OUTPUT,
    )
    raw_ref = ModelRawResponseRef(
        raw_response_ref_id="raw:direct",
        response_source_kind=ModelResponseSourceKind.TEST_FIXTURE,
        response_summary="bounded direct raw ref",
        raw_response_preview="bounded redacted preview",
        raw_response_char_count=24,
        redacted=True,
        truncated=False,
        contains_secret_like_content=False,
        contains_credential_like_content=False,
        contains_token_like_content=False,
        source_refs=[source],
    )
    payload = ModelSanitizedResponsePayload(
        sanitized_payload_id="sanitized:direct",
        payload_format=ModelResponsePayloadFormat.TEST_FIXTURE,
        sanitized_text="bounded sanitized direct text",
        sanitized_summary="direct sanitized payload",
        response_preview="bounded sanitized direct preview",
        redacted=True,
        truncated=False,
        redacted_field_count=0,
        truncated_field_count=0,
        source_refs=[source],
    )
    envelope = ModelResponseEnvelope(
        response_envelope_id="response:direct",
        version="v0.34.3",
        envelope_kind=ModelResponseEnvelopeKind.MOCK_RESPONSE_ENVELOPE,
        status=ModelResponseStatus.SANITIZED,
        readiness_level=ModelResponseReadinessLevel.SANITIZATION_READY,
        request_envelope_id=None,
        raw_response_ref=raw_ref,
        sanitized_payload=payload,
        sanitization_policy_id="policy:direct",
        source_refs=[source],
        summary="direct response envelope metadata only",
    )
    assert model_response_envelope_is_not_action(envelope)


def test_helpers_are_pure_conservative_source() -> None:
    source = inspect.getsource(response_module)
    forbidden_patterns = [
        "import subprocess",
        "subprocess.",
        "os.system",
        "shell=True",
        "requests.",
        "httpx.",
        "urllib.",
        "aiohttp.",
        "socket.",
        "eval(",
        "exec(",
        "importlib",
        "write_text(",
        "write_bytes(",
        "open(",
        "unlink(",
        ".rmdir(",
        ".mkdir(",
        ".rename(",
        "Path.replace(",
        ".chmod(",
        ".chown(",
        "shutil.",
        "sqlite",
        "logging.",
        "os.environ",
        "dotenv",
    ]
    for pattern in forbidden_patterns:
        assert pattern not in source

    unsafe_true_patterns = [
        "ready_for_execution=True",
        "ready_for_controlled_model_invocation=True",
        "ready_for_real_model_invocation=True",
        "ready_for_model_invocation=True",
        "ready_for_provider_invocation=True",
        "ready_for_provider_sdk_invocation=True",
        "ready_for_existing_boundary_invocation=True",
        "ready_for_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_secret_read=True",
        "ready_for_agent_step_execution=True",
        "ready_for_general_agent_execution=True",
        "ready_for_autonomous_agent_runtime=True",
        "ready_for_general_tool_execution=True",
        "ready_for_tool_calls=True",
        "ready_for_function_calls=True",
        "ready_for_action_execution=True",
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_command_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_raw_response_persistence=True",
        "ready_for_raw_model_output_persistence=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_ui_runtime=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
