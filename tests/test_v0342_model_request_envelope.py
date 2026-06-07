import inspect

import pytest

from chanta_core.agent_runtime import (
    ModelPromptPayloadRef,
    ModelRequestDataSensitivityKind,
    ModelRequestEnvelope,
    ModelRequestEnvelopeInput,
    ModelRequestEnvelopeKind,
    ModelRequestEnvelopeReport,
    ModelRequestFlagSet,
    ModelRequestNoInvocationGuarantee,
    ModelRequestOutputPolicy,
    ModelRequestPayloadFormat,
    ModelRequestProviderBinding,
    ModelRequestReadinessLevel,
    ModelRequestRiskKind,
    ModelRequestRunPreview,
    ModelRequestSafetyConstraints,
    ModelRequestSourceKind,
    ModelRequestSourceRef,
    ModelRequestStatus,
    ModelRequestStopPolicy,
    ModelRequestTimeoutPolicy,
    ModelRequestTokenBudget,
    ModelRequestValidationDecisionKind,
    ModelRequestValidationFinding,
    ModelRequestValidationReport,
    V0342ReadinessReport,
    build_model_prompt_payload_ref,
    build_model_request_envelope,
    build_model_request_envelope_input,
    build_model_request_envelope_report,
    build_model_request_flags,
    build_model_request_no_invocation_guarantee,
    build_model_request_output_policy,
    build_model_request_provider_binding,
    build_model_request_run_preview,
    build_model_request_safety_constraints,
    build_model_request_source_ref,
    build_model_request_stop_policy,
    build_model_request_timeout_policy,
    build_model_request_token_budget,
    build_model_request_validation_report,
    build_prompt_assembly_output,
    build_prompt_payload_ref_from_prompt_assembly_output,
    build_v0342_readiness_report,
    default_mock_provider_profile_descriptor,
    default_model_request_output_policy,
    default_model_request_safety_constraints,
    default_model_request_stop_policy,
    default_model_request_timeout_policy,
    default_model_request_token_budget,
    default_provider_invocation_policy,
    model_prompt_payload_ref_is_not_raw_persistence,
    model_request_envelope_is_not_invocation,
    model_request_flags_preserve_invocation_false,
    model_request_validation_report_is_not_invocation,
    v0342_readiness_report_is_not_invocation_ready,
    validate_model_prompt_payload_ref,
    validate_model_request_envelope,
)
from chanta_core.agent_runtime import model_request as request_module


def test_v0342_taxonomies_cover_required_values() -> None:
    assert ModelRequestEnvelopeKind.PROMPT_ASSEMBLY_REQUEST.value == "prompt_assembly_request"
    assert ModelRequestEnvelopeKind.EXISTING_BOUNDARY_FUTURE_GATE_REQUEST.value == "existing_boundary_future_gate_request"
    assert ModelRequestPayloadFormat.MESSAGE_LIST.value == "message_list"
    assert ModelRequestPayloadFormat.REDACTED_PREVIEW_ONLY.value == "redacted_preview_only"
    assert ModelRequestSourceKind.V0332_PROMPT_ASSEMBLY_OUTPUT.value == "v0332_prompt_assembly_output"
    assert ModelRequestSourceKind.HERMES_REFERENCE_CONTEXT_REF.value == "hermes_reference_context_ref"
    assert ModelRequestStatus.VALIDATED_WITH_GAPS.value == "validated_with_gaps"
    assert ModelRequestReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0344.value == "design_handoff_ready_for_v0344"
    assert ModelRequestValidationDecisionKind.ACCEPT_ENVELOPE_METADATA_ONLY.value == "accept_envelope_metadata_only"
    assert ModelRequestRiskKind.RAW_PROMPT_PERSISTENCE_RISK.value == "raw_prompt_persistence_risk"
    assert ModelRequestRiskKind.RECURSIVE_CALL_RISK.value == "recursive_call_risk"
    assert ModelRequestDataSensitivityKind.SECRET_LIKE.value == "secret_like"


def test_flags_allow_envelope_handoff_only_and_preserve_invocation_false() -> None:
    flags = build_model_request_flags()
    assert isinstance(flags, ModelRequestFlagSet)
    assert flags.model_request_envelope_constructed is True
    assert flags.prompt_payload_ref_constructed is True
    assert flags.model_request_validation_available is True
    assert flags.ready_for_v0343_model_response_envelope is True
    assert flags.ready_for_v0344_existing_provider_boundary_adapter is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_controlled_model_invocation is False
    assert flags.ready_for_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_existing_boundary_invocation is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_tool_calls is False
    assert flags.ready_for_function_calls is False
    assert flags.ready_for_recursive_calls is False
    assert flags.ready_for_raw_prompt_persistence is False
    assert flags.production_certified is False
    assert model_request_flags_preserve_invocation_false(flags)


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
        "ready_for_tool_calls",
        "ready_for_function_calls",
        "ready_for_recursive_calls",
        "ready_for_raw_prompt_persistence",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_patch_application",
    ],
)
def test_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_model_request_flags(**{unsafe_flag: True})


def test_source_ref_and_prompt_payload_ref_are_bounded_metadata() -> None:
    source = build_model_request_source_ref(
        "source:test",
        ModelRequestSourceKind.V0332_PROMPT_ASSEMBLY_OUTPUT,
        "prompt_output:test",
        "Prompt output ref only.",
        sensitivity=ModelRequestDataSensitivityKind.INTERNAL,
    )
    assert isinstance(source, ModelRequestSourceRef)
    assert source.provider_call is False
    assert source.file_read is False
    assert source.credential_access is False

    payload = build_model_prompt_payload_ref(source_refs=[source])
    assert isinstance(payload, ModelPromptPayloadRef)
    assert len(payload.prompt_preview) <= request_module.DEFAULT_MAX_PROMPT_PREVIEW_CHARS
    assert payload.contains_secret_like_content is False
    assert payload.contains_credential_like_content is False
    assert payload.contains_token_like_content is False
    assert payload.raw_prompt_persistence is False
    assert model_prompt_payload_ref_is_not_raw_persistence(payload)

    with pytest.raises(ValueError):
        build_model_request_source_ref("source:bad", sensitivity=ModelRequestDataSensitivityKind.SECRET_LIKE)
    with pytest.raises(ValueError):
        build_model_prompt_payload_ref(contains_secret_like_content=True)
    with pytest.raises(ValueError):
        build_model_prompt_payload_ref(contains_credential_like_content=True)
    with pytest.raises(ValueError):
        build_model_prompt_payload_ref(contains_token_like_content=True)
    with pytest.raises(ValueError):
        build_model_prompt_payload_ref(prompt_preview="token=abc")


def test_prompt_payload_ref_from_prompt_assembly_output_uses_bounded_redacted_preview() -> None:
    prompt_output = build_prompt_assembly_output(
        "prompt_output:v0342:test",
        "assembly_input:v0342:test",
        assembled_prompt_text="Summarize this safe request.",
        token_budget_estimate=42,
    )
    payload = build_prompt_payload_ref_from_prompt_assembly_output(prompt_output)
    assert payload.prompt_output_id == "prompt_output:v0342:test"
    assert payload.estimated_prompt_tokens == 42
    assert payload.redacted is True
    assert payload.contains_secret_like_content is False
    assert model_prompt_payload_ref_is_not_raw_persistence(payload)

    long_prompt = build_prompt_assembly_output(
        "prompt_output:v0342:long",
        "assembly_input:v0342:long",
        assembled_prompt_text="x" * (request_module.DEFAULT_MAX_PROMPT_PREVIEW_CHARS + 20),
    )
    long_payload = build_prompt_payload_ref_from_prompt_assembly_output(long_prompt)
    assert long_payload.truncated is True
    assert len(long_payload.prompt_preview) <= request_module.DEFAULT_MAX_PROMPT_PREVIEW_CHARS


def test_token_stop_timeout_and_output_policies_are_conservative() -> None:
    budget = default_model_request_token_budget()
    assert isinstance(budget, ModelRequestTokenBudget)
    assert budget.allow_unbounded_prompt is False
    assert budget.allow_unbounded_response is False
    with pytest.raises(ValueError):
        build_model_request_token_budget(allow_unbounded_prompt=True)
    with pytest.raises(ValueError):
        build_model_request_token_budget(allow_unbounded_response=True)

    stop = default_model_request_stop_policy(stop_sequences=["END"])
    assert isinstance(stop, ModelRequestStopPolicy)
    assert stop.provider_call is False
    with pytest.raises(ValueError):
        build_model_request_stop_policy(stop_sequences=["a", "b"], max_stop_sequence_count=1)

    timeout = default_model_request_timeout_policy()
    assert isinstance(timeout, ModelRequestTimeoutPolicy)
    assert timeout.allow_streaming is False
    assert timeout.allow_retries is False
    assert timeout.max_retries == 0
    assert timeout.network_access is False
    with pytest.raises(ValueError):
        build_model_request_timeout_policy(allow_retries=True)
    with pytest.raises(ValueError):
        build_model_request_timeout_policy(max_retries=1)

    output = default_model_request_output_policy()
    assert isinstance(output, ModelRequestOutputPolicy)
    assert output.allow_raw_response_persistence is False
    assert output.allow_tool_calls is False
    assert output.allow_function_calls is False
    assert output.allow_patch_output is False
    assert output.allow_command_output is False
    assert output.allow_untrusted_action is False
    assert output.require_response_envelope is True
    assert output.require_response_sanitizer is True
    assert output.require_action_quarantine is True
    for kwargs in [{"allow_raw_response_persistence": True}, {"allow_tool_calls": True}, {"allow_function_calls": True}, {"allow_patch_output": True}, {"allow_command_output": True}, {"allow_untrusted_action": True}]:
        with pytest.raises(ValueError):
            build_model_request_output_policy(**kwargs)


def test_safety_constraints_require_no_tool_function_recursive_and_raw_prompt() -> None:
    constraints = default_model_request_safety_constraints()
    assert isinstance(constraints, ModelRequestSafetyConstraints)
    joined_content = " ".join(constraints.prohibited_request_content).lower()
    for term in ["secret", "token", "key", "credential"]:
        assert term in joined_content
    assert constraints.require_provider_profile_validation is True
    assert constraints.require_prompt_redaction is True
    assert constraints.require_token_budget is True
    assert constraints.require_output_policy is True
    assert constraints.require_no_tool_calls is True
    assert constraints.require_no_function_calls is True
    assert constraints.require_no_recursive_calls is True
    assert constraints.require_no_raw_prompt_persistence is True
    assert constraints.runtime_enforcement is False
    with pytest.raises(ValueError):
        build_model_request_safety_constraints(require_no_tool_calls=False)


def test_provider_binding_envelope_input_and_envelope_are_not_invocation() -> None:
    provider_profile = default_mock_provider_profile_descriptor()
    invocation_policy = default_provider_invocation_policy()
    binding = build_model_request_provider_binding(provider_profile=provider_profile, invocation_policy=invocation_policy)
    assert isinstance(binding, ModelRequestProviderBinding)
    assert binding.provider_profile_id == provider_profile.provider_profile_id
    assert binding.invocation_allowed is False
    assert binding.provider_invocation_allowed is False
    assert binding.network_allowed is False
    assert binding.credential_access_allowed is False
    assert binding.provider_call is False

    for forbidden in ["invocation_allowed", "provider_invocation_allowed", "network_allowed", "credential_access_allowed"]:
        with pytest.raises(ValueError):
            build_model_request_provider_binding(**{forbidden: True})

    envelope_input = build_model_request_envelope_input()
    assert isinstance(envelope_input, ModelRequestEnvelopeInput)
    assert envelope_input.provider_invocation_request is False

    envelope = build_model_request_envelope(provider_binding=binding)
    assert isinstance(envelope, ModelRequestEnvelope)
    assert envelope.ready_for_v0343_model_response_envelope is True
    assert envelope.ready_for_v0344_existing_provider_boundary_adapter is True
    assert envelope.ready_for_invocation is False
    assert envelope.ready_for_provider_invocation is False
    assert envelope.ready_for_execution is False
    assert envelope.provider_call is False
    assert model_request_envelope_is_not_invocation(envelope)

    with pytest.raises(ValueError):
        build_model_request_envelope(ready_for_invocation=True)
    with pytest.raises(ValueError):
        build_model_request_envelope(ready_for_provider_invocation=True)


def test_validation_and_envelope_reports_are_not_invocation() -> None:
    payload = build_model_prompt_payload_ref()
    finding = validate_model_prompt_payload_ref(payload)
    assert isinstance(finding, ModelRequestValidationFinding)
    assert finding.decision_kind == ModelRequestValidationDecisionKind.ACCEPT_ENVELOPE_METADATA_ONLY
    assert finding.invocation is False

    envelope = build_model_request_envelope(payload_ref=payload)
    report = validate_model_request_envelope(envelope)
    assert isinstance(report, ModelRequestValidationReport)
    assert report.validation_passed is True
    assert report.ready_for_invocation is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_execution is False
    assert report.invocation_certification is False
    assert model_request_validation_report_is_not_invocation(report)

    envelope_report = build_model_request_envelope_report()
    assert isinstance(envelope_report, ModelRequestEnvelopeReport)
    assert envelope_report.ready_for_v0343_model_response_envelope is True
    assert envelope_report.ready_for_v0344_existing_provider_boundary_adapter is True
    assert envelope_report.ready_for_invocation is False
    assert envelope_report.ready_for_provider_invocation is False
    assert envelope_report.ready_for_execution is False
    assert envelope_report.invocation is False

    with pytest.raises(ValueError):
        build_model_request_validation_report(blocked_reasons=["blocked"], validation_passed=True)
    with pytest.raises(ValueError):
        build_model_request_validation_report(ready_for_invocation=True)


def test_run_preview_guarantee_and_readiness_are_conservative() -> None:
    preview = build_model_request_run_preview()
    assert isinstance(preview, ModelRequestRunPreview)
    assert preview.invocation is False
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_model_request_no_invocation_guarantee()
    assert isinstance(guarantee, ModelRequestNoInvocationGuarantee)
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0342_readiness_report()
    assert isinstance(readiness, V0342ReadinessReport)
    assert readiness.ready_for_v0343_model_response_envelope is True
    assert readiness.ready_for_v0344_existing_provider_boundary_adapter is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_controlled_model_invocation is False
    assert readiness.ready_for_model_invocation is False
    assert readiness.ready_for_provider_invocation is False
    assert readiness.ready_for_existing_boundary_invocation is False
    assert readiness.ready_for_network_access is False
    assert readiness.ready_for_credential_access is False
    assert readiness.ready_for_tool_calls is False
    assert readiness.ready_for_function_calls is False
    assert readiness.ready_for_recursive_calls is False
    assert readiness.ready_for_raw_prompt_persistence is False
    assert v0342_readiness_report_is_not_invocation_ready(readiness)

    with pytest.raises(ValueError):
        build_v0342_readiness_report(ready_for_model_invocation=True)
    with pytest.raises(ValueError):
        build_v0342_readiness_report(ready_for_provider_invocation=True)
    with pytest.raises(ValueError):
        build_v0342_readiness_report(ready_for_existing_boundary_invocation=True)
    with pytest.raises(ValueError):
        build_v0342_readiness_report(ready_for_raw_prompt_persistence=True)


def test_direct_dataclass_construction_with_valid_inputs() -> None:
    source = ModelRequestSourceRef(
        source_ref_id="source:direct",
        source_kind=ModelRequestSourceKind.TEST_FIXTURE,
        source_id="fixture",
        source_summary="fixture source ref only",
        sensitivity=ModelRequestDataSensitivityKind.USER_SUPPLIED,
    )
    payload = ModelPromptPayloadRef(
        prompt_payload_ref_id="payload:direct",
        payload_format=ModelRequestPayloadFormat.TEST_FIXTURE,
        prompt_output_id=None,
        prompt_summary="direct payload",
        prompt_preview="safe bounded preview",
        message_count=1,
        estimated_prompt_chars=20,
        estimated_prompt_tokens=5,
        redacted=True,
        truncated=False,
        contains_secret_like_content=False,
        contains_credential_like_content=False,
        contains_token_like_content=False,
        source_refs=[source],
    )
    binding = ModelRequestProviderBinding(
        provider_binding_id="binding:direct",
        provider_profile_id="provider_profile:mock:v0.34.1",
        provider_profile_name="mock_provider",
        provider_profile_kind="mock_provider",
        provider_boundary_ref_id=None,
        invocation_policy_id="provider_invocation_policy:v0.34.1",
        binding_summary="direct binding metadata only",
        source_refs=[source],
    )
    envelope = ModelRequestEnvelope(
        request_envelope_id="envelope:direct",
        version="v0.34.2",
        envelope_kind=ModelRequestEnvelopeKind.MOCK_PROVIDER_TEST_REQUEST,
        status=ModelRequestStatus.VALIDATED,
        readiness_level=ModelRequestReadinessLevel.ENVELOPE_VALIDATION_READY,
        payload_ref=payload,
        provider_binding=binding,
        token_budget=build_model_request_token_budget("budget:direct"),
        stop_policy=build_model_request_stop_policy("stop:direct"),
        timeout_policy=build_model_request_timeout_policy("timeout:direct"),
        output_policy=build_model_request_output_policy("output:direct"),
        safety_constraints=build_model_request_safety_constraints("safety:direct"),
        source_refs=[source],
        summary="direct envelope metadata only",
    )
    assert model_request_envelope_is_not_invocation(envelope)


def test_helpers_are_pure_conservative_source() -> None:
    source = inspect.getsource(request_module)
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
        "ready_for_recursive_calls=True",
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_command_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_raw_prompt_persistence=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_ui_runtime=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
