import inspect

import pytest

from chanta_core.agent_runtime import (
    ExistingProviderBoundaryAdapterDescriptor,
    ExistingProviderBoundaryAdapterFlagSet,
    ExistingProviderBoundaryAdapterKind,
    ExistingProviderBoundaryAdapterPolicy,
    ExistingProviderBoundaryAdapterStatus,
    ExistingProviderBoundaryAdapterValidationReport,
    ExistingProviderBoundaryCallPosture,
    ExistingProviderBoundaryCallRecord,
    ExistingProviderBoundaryCallableRef,
    ExistingProviderBoundaryDecisionKind,
    ExistingProviderBoundaryInvocationDecision,
    ExistingProviderBoundaryInvocationInput,
    ExistingProviderBoundaryInvocationReport,
    ExistingProviderBoundaryInvocationResult,
    ExistingProviderBoundaryNoDirectAccessGuarantee,
    ExistingProviderBoundaryOutcomeKind,
    ExistingProviderBoundaryReadinessLevel,
    ExistingProviderBoundaryRiskKind,
    ExistingProviderBoundaryRunPreview,
    ExistingProviderBoundarySourceKind,
    ExistingProviderBoundarySourceRef,
    ExistingProviderInvocationMode,
    V0344ReadinessReport,
    build_existing_provider_boundary_adapter_descriptor,
    build_existing_provider_boundary_adapter_flags,
    build_existing_provider_boundary_adapter_policy,
    build_existing_provider_boundary_adapter_validation_report,
    build_existing_provider_boundary_call_record,
    build_existing_provider_boundary_callable_ref,
    build_existing_provider_boundary_invocation_decision,
    build_existing_provider_boundary_invocation_input,
    build_existing_provider_boundary_invocation_report,
    build_existing_provider_boundary_invocation_result,
    build_existing_provider_boundary_no_direct_access_guarantee,
    build_existing_provider_boundary_run_preview,
    build_existing_provider_boundary_source_ref,
    build_model_request_envelope,
    build_model_response_envelope_from_boundary_result,
    build_v0344_readiness_report,
    decide_existing_provider_boundary_invocation,
    default_existing_provider_boundary_adapter_policy,
    existing_provider_boundary_adapter_blocks_direct_access,
    existing_provider_boundary_decision_blocks_unsafe_access,
    existing_provider_boundary_flags_preserve_direct_access_false,
    existing_provider_boundary_result_is_not_action,
    invoke_existing_provider_boundary_adapter,
    v0344_readiness_report_is_not_general_execution_ready,
    validate_existing_provider_boundary_adapter_descriptor,
)
from chanta_core.agent_runtime import provider_adapter as adapter_module


def test_v0344_taxonomies_cover_required_values() -> None:
    assert ExistingProviderBoundaryAdapterKind.INJECTED_CALLABLE_ADAPTER.value == "injected_callable_adapter"
    assert ExistingProviderBoundaryAdapterKind.EXISTING_CHAT_SERVICE_BOUNDARY_ADAPTER.value == "existing_chat_service_boundary_adapter"
    assert ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY.value == "injected_existing_boundary"
    assert ExistingProviderInvocationMode.PROJECT_LOCAL_EXISTING_BOUNDARY.value == "project_local_existing_boundary"
    assert ExistingProviderBoundaryAdapterStatus.INVOCATION_COMPLETED.value == "invocation_completed"
    assert ExistingProviderBoundaryReadinessLevel.CONTROLLED_EXISTING_BOUNDARY_INVOCATION_READY.value == "controlled_existing_boundary_invocation_ready"
    assert ExistingProviderBoundaryDecisionKind.ALLOW_INJECTED_EXISTING_BOUNDARY_CALL.value == "allow_injected_existing_boundary_call"
    assert ExistingProviderBoundaryOutcomeKind.EXISTING_BOUNDARY_RESPONSE_RETURNED.value == "existing_boundary_response_returned"
    assert ExistingProviderBoundaryRiskKind.DIRECT_PROVIDER_SDK_RISK.value == "direct_provider_sdk_risk"
    assert ExistingProviderBoundaryRiskKind.EXTERNAL_HARNESS_EXECUTION_RISK.value == "external_harness_execution_risk"
    assert ExistingProviderBoundarySourceKind.INJECTED_CALLABLE_REF.value == "injected_callable_ref"
    assert ExistingProviderBoundaryCallPosture.DIRECT_NETWORK_BLOCKED.value == "direct_network_blocked"


def test_flags_allow_controlled_existing_boundary_only_and_block_direct_access() -> None:
    flags = build_existing_provider_boundary_adapter_flags()
    assert isinstance(flags, ExistingProviderBoundaryAdapterFlagSet)
    assert flags.existing_provider_boundary_adapter_constructed is True
    assert flags.adapter_validation_available is True
    assert flags.controlled_existing_boundary_call_available is True
    assert flags.response_envelope_bridge_available is True
    assert flags.ready_for_v0345_model_output_action_quarantine is True
    assert flags.ready_for_v0346_agent_step_runner_model_integration is True
    assert flags.ready_for_controlled_model_invocation is True
    assert flags.ready_for_existing_boundary_invocation is True
    assert flags.ready_for_real_model_invocation is True
    assert flags.ready_for_model_invocation is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_direct_provider_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_provider_sdk_invocation is False
    assert flags.ready_for_direct_network_access is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_secret_read is False
    assert flags.ready_for_tool_calls is False
    assert flags.ready_for_function_calls is False
    assert flags.ready_for_action_execution is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_raw_prompt_persistence is False
    assert flags.ready_for_raw_response_persistence is False
    assert flags.production_certified is False
    assert existing_provider_boundary_flags_preserve_direct_access_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_direct_provider_invocation",
        "ready_for_provider_sdk_invocation",
        "ready_for_direct_network_access",
        "ready_for_network_access",
        "ready_for_credential_access",
        "ready_for_secret_read",
        "ready_for_action_execution",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_patch_application",
        "ready_for_raw_prompt_persistence",
        "ready_for_raw_response_persistence",
    ],
)
def test_flags_reject_unsafe_direct_access(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_existing_provider_boundary_adapter_flags(**{unsafe_flag: True})


def test_source_ref_callable_ref_and_policy_block_direct_access() -> None:
    source = build_existing_provider_boundary_source_ref(
        "source:callable:test",
        ExistingProviderBoundarySourceKind.INJECTED_CALLABLE_REF,
        "callable:test",
        "Injected callable ref only.",
    )
    assert isinstance(source, ExistingProviderBoundarySourceRef)
    assert source.sdk_access is False
    assert source.network_access is False
    assert source.credential_access is False

    callable_ref = build_existing_provider_boundary_callable_ref(source_refs=[source])
    assert isinstance(callable_ref, ExistingProviderBoundaryCallableRef)
    assert callable_ref.direct_sdk is False
    assert callable_ref.direct_network is False
    assert callable_ref.credential_reader is False
    assert callable_ref.secret_reader is False
    assert callable_ref.shell_based is False
    assert callable_ref.credential_access is False

    for forbidden in ["direct_sdk", "direct_network", "credential_reader", "secret_reader", "shell_based"]:
        with pytest.raises(ValueError):
            build_existing_provider_boundary_callable_ref(**{forbidden: True})

    policy = default_existing_provider_boundary_adapter_policy()
    assert isinstance(policy, ExistingProviderBoundaryAdapterPolicy)
    assert policy.allow_injected_existing_boundary_call is True
    assert policy.allow_direct_provider_sdk is False
    assert policy.allow_direct_network is False
    assert policy.allow_credential_read is False
    assert policy.allow_secret_read is False
    assert policy.allow_tool_calls is False
    assert policy.allow_function_calls is False
    assert policy.allow_action_execution is False
    assert policy.allow_raw_prompt_persistence is False
    assert policy.allow_raw_response_persistence is False
    assert policy.invocation is False

    for forbidden in ["allow_direct_provider_sdk", "allow_direct_network", "allow_credential_read", "allow_secret_read", "allow_tool_calls", "allow_action_execution", "allow_raw_response_persistence"]:
        with pytest.raises(ValueError):
            build_existing_provider_boundary_adapter_policy(**{forbidden: True})


def test_adapter_descriptor_input_and_decision_are_gated() -> None:
    adapter = build_existing_provider_boundary_adapter_descriptor()
    assert isinstance(adapter, ExistingProviderBoundaryAdapterDescriptor)
    assert adapter.ready_for_controlled_invocation is True
    assert adapter.ready_for_direct_provider_invocation is False
    assert adapter.ready_for_execution is False
    assert adapter.new_provider_sdk_adapter is False
    assert existing_provider_boundary_adapter_blocks_direct_access(adapter)

    with pytest.raises(ValueError):
        build_existing_provider_boundary_adapter_descriptor(
            invocation_mode=ExistingProviderInvocationMode.NO_INVOCATION,
            ready_for_controlled_invocation=True,
        )
    with pytest.raises(ValueError):
        build_existing_provider_boundary_adapter_descriptor(ready_for_direct_provider_invocation=True)

    invocation_input = build_existing_provider_boundary_invocation_input()
    assert isinstance(invocation_input, ExistingProviderBoundaryInvocationInput)
    assert invocation_input.direct_sdk_network_request is False

    decision = decide_existing_provider_boundary_invocation(invocation_input, adapter, build_model_request_envelope())
    assert isinstance(decision, ExistingProviderBoundaryInvocationDecision)
    assert decision.controlled_existing_boundary_invocation_allowed is True
    assert decision.allowed_invocation_mode == ExistingProviderInvocationMode.INJECTED_EXISTING_BOUNDARY
    assert existing_provider_boundary_decision_blocks_unsafe_access(decision)

    with pytest.raises(ValueError):
        build_existing_provider_boundary_invocation_decision(direct_provider_invocation_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_invocation_decision(provider_sdk_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_invocation_decision(direct_network_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_invocation_decision(credential_access_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_invocation_decision(action_execution_allowed=True)


def test_call_record_result_validation_and_invocation_reports_are_safe() -> None:
    record = build_existing_provider_boundary_call_record(
        call_started=True,
        call_completed=True,
        used_injected_callable=True,
    )
    assert isinstance(record, ExistingProviderBoundaryCallRecord)
    assert record.used_injected_callable is True
    assert record.used_direct_provider_sdk is False
    assert record.used_direct_network_client is False
    assert record.read_credentials is False
    assert record.read_secrets is False
    assert record.executed_shell is False
    assert record.executed_tools is False
    assert record.wrote_workspace is False
    assert record.raw_prompt_persisted is False
    assert record.raw_response_persisted is False
    assert record.persistent_log is False

    for forbidden in ["used_direct_provider_sdk", "used_direct_network_client", "read_credentials", "read_secrets", "executed_shell", "executed_tools", "wrote_workspace", "raw_prompt_persisted", "raw_response_persisted"]:
        with pytest.raises(ValueError):
            build_existing_provider_boundary_call_record(**{forbidden: True})

    result = build_existing_provider_boundary_invocation_result(
        outcome_kind=ExistingProviderBoundaryOutcomeKind.RESPONSE_ENVELOPE_CREATED,
        response_text_preview="bounded response preview",
        response_char_count=24,
        response_envelope_id="model_response_envelope:test",
        ready_for_v0345_model_output_action_quarantine=True,
        blocked_reason=None,
    )
    assert isinstance(result, ExistingProviderBoundaryInvocationResult)
    assert result.ready_for_action_execution is False
    assert result.ready_for_execution is False
    assert existing_provider_boundary_result_is_not_action(result)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_invocation_result(ready_for_action_execution=True)

    validation = build_existing_provider_boundary_adapter_validation_report(ready_for_controlled_existing_boundary_invocation=True)
    assert isinstance(validation, ExistingProviderBoundaryAdapterValidationReport)
    assert validation.direct_sdk_blocked is True
    assert validation.direct_network_blocked is True
    assert validation.credential_access_blocked is True
    assert validation.secret_read_blocked is True
    assert validation.raw_persistence_blocked is True
    assert validation.ready_for_direct_provider_invocation is False
    assert validation.ready_for_execution is False
    assert validation.certification is False
    with pytest.raises(ValueError):
        build_existing_provider_boundary_adapter_validation_report(direct_sdk_blocked=False)

    report = build_existing_provider_boundary_invocation_report(call_count=1, completed_call_count=1)
    assert isinstance(report, ExistingProviderBoundaryInvocationReport)
    assert report.ready_for_controlled_existing_boundary_invocation is True
    assert report.ready_for_direct_provider_invocation is False
    assert report.ready_for_action_execution is False
    assert report.ready_for_execution is False
    assert report.runtime_expansion is False


def test_fake_injected_callable_invokes_only_after_policy_and_sanitizes_response() -> None:
    calls: list[str] = []

    def fake_boundary(invocation_input: ExistingProviderBoundaryInvocationInput) -> str:
        calls.append(invocation_input.invocation_input_id)
        return "secret=value tool_call run command powershell"

    adapter = build_existing_provider_boundary_adapter_descriptor()
    invocation_input = build_existing_provider_boundary_invocation_input()
    result = invoke_existing_provider_boundary_adapter(invocation_input, adapter, boundary_callable=fake_boundary)

    assert calls == [invocation_input.invocation_input_id]
    assert result.outcome_kind == ExistingProviderBoundaryOutcomeKind.EXISTING_BOUNDARY_RESPONSE_RETURNED
    assert result.response_envelope_id is not None
    assert result.ready_for_v0345_model_output_action_quarantine is True
    assert result.ready_for_action_execution is False
    assert result.ready_for_execution is False
    assert "secret=value" not in (result.response_text_preview or "")
    assert existing_provider_boundary_result_is_not_action(result)

    response_envelope = build_model_response_envelope_from_boundary_result("secret=value tool_call")
    assert response_envelope.provider_call is False
    assert response_envelope.action is False
    assert response_envelope.sanitized_payload.action_signals


def test_missing_callable_and_blocked_decision_do_not_invoke() -> None:
    adapter = build_existing_provider_boundary_adapter_descriptor()
    invocation_input = build_existing_provider_boundary_invocation_input()
    result = invoke_existing_provider_boundary_adapter(invocation_input, adapter)
    assert result.outcome_kind == ExistingProviderBoundaryOutcomeKind.NO_OP_RESULT
    assert result.blocked_reason is not None
    assert result.ready_for_execution is False

    blocked_policy = build_existing_provider_boundary_adapter_policy(allowed_invocation_modes=[])
    blocked_adapter = build_existing_provider_boundary_adapter_descriptor(adapter_policy=blocked_policy)
    calls: list[str] = []

    def should_not_call(_: ExistingProviderBoundaryInvocationInput) -> str:
        calls.append("called")
        return "unexpected"

    blocked_result = invoke_existing_provider_boundary_adapter(invocation_input, blocked_adapter, boundary_callable=should_not_call)
    assert calls == []
    assert blocked_result.outcome_kind == ExistingProviderBoundaryOutcomeKind.BLOCKED_RESULT
    assert blocked_result.ready_for_execution is False


def test_callable_exception_returns_safe_fail() -> None:
    def failing_boundary(_: ExistingProviderBoundaryInvocationInput) -> str:
        raise RuntimeError("controlled fake failure")

    result = invoke_existing_provider_boundary_adapter(
        build_existing_provider_boundary_invocation_input(),
        build_existing_provider_boundary_adapter_descriptor(),
        boundary_callable=failing_boundary,
    )
    assert result.outcome_kind == ExistingProviderBoundaryOutcomeKind.SAFE_FAIL_RESULT
    assert result.safe_fail_reason == "controlled fake failure"
    assert result.ready_for_action_execution is False
    assert result.ready_for_execution is False


def test_run_preview_guarantee_and_readiness_are_conservative() -> None:
    preview = build_existing_provider_boundary_run_preview()
    assert isinstance(preview, ExistingProviderBoundaryRunPreview)
    assert preview.direct_provider_invocation is False
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_existing_provider_boundary_no_direct_access_guarantee()
    assert isinstance(guarantee, ExistingProviderBoundaryNoDirectAccessGuarantee)
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0344_readiness_report()
    assert isinstance(readiness, V0344ReadinessReport)
    assert readiness.ready_for_controlled_model_invocation is True
    assert readiness.ready_for_existing_boundary_invocation is True
    assert readiness.ready_for_real_model_invocation is True
    assert readiness.ready_for_model_invocation is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_direct_provider_invocation is False
    assert readiness.ready_for_provider_sdk_invocation is False
    assert readiness.ready_for_direct_network_access is False
    assert readiness.ready_for_network_access is False
    assert readiness.ready_for_credential_access is False
    assert readiness.ready_for_secret_read is False
    assert readiness.ready_for_action_execution is False
    assert readiness.ready_for_workspace_write is False
    assert readiness.ready_for_raw_prompt_persistence is False
    assert readiness.ready_for_raw_response_persistence is False
    assert v0344_readiness_report_is_not_general_execution_ready(readiness)

    with pytest.raises(ValueError):
        build_v0344_readiness_report(ready_for_execution=True)
    with pytest.raises(ValueError):
        build_v0344_readiness_report(ready_for_direct_provider_invocation=True)
    with pytest.raises(ValueError):
        build_v0344_readiness_report(ready_for_provider_sdk_invocation=True)
    with pytest.raises(ValueError):
        build_v0344_readiness_report(ready_for_credential_access=True)


def test_helpers_are_conservative_source_except_injected_callable() -> None:
    source = inspect.getsource(adapter_module)
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
        "openai",
        "anthropic",
        "ollama",
        "lmstudio",
    ]
    lowered = source.lower()
    for pattern in forbidden_patterns:
        assert pattern.lower() not in lowered

    unsafe_true_patterns = [
        "ready_for_execution=True",
        "ready_for_direct_provider_invocation=True",
        "ready_for_provider_sdk_invocation=True",
        "ready_for_direct_network_access=True",
        "ready_for_network_access=True",
        "ready_for_credential_access=True",
        "ready_for_secret_read=True",
        "ready_for_action_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_raw_prompt_persistence=True",
        "ready_for_raw_response_persistence=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
