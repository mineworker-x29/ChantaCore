import inspect

import pytest

from chanta_core.agent_runtime import (
    ProviderBoundaryKind,
    ProviderCredentialPolicy,
    ProviderCredentialPosture,
    ProviderInvocationLimitPolicy,
    ProviderInvocationModeKind,
    ProviderInvocationPolicy,
    ProviderNetworkPolicy,
    ProviderNetworkPosture,
    ProviderProfileDescriptor,
    ProviderProfileFlagSet,
    ProviderProfileKind,
    ProviderProfileNoInvocationGuarantee,
    ProviderProfileReadinessLevel,
    ProviderProfileRegistry,
    ProviderProfileResolutionDecision,
    ProviderProfileResolutionInput,
    ProviderProfileResolutionReport,
    ProviderProfileRiskKind,
    ProviderProfileRunPreview,
    ProviderProfileSourceKind,
    ProviderProfileSourceRef,
    ProviderProfileStatus,
    ProviderProfileTrustLevel,
    ProviderProfileValidationDecisionKind,
    ProviderProfileValidationFinding,
    ProviderProfileValidationReport,
    ProviderPromptDataPolicy,
    ProviderResponseDataPolicy,
    V0341ReadinessReport,
    build_provider_credential_policy,
    build_provider_invocation_limit_policy,
    build_provider_network_policy,
    build_provider_profile_descriptor,
    build_provider_profile_flags,
    build_provider_profile_no_invocation_guarantee,
    build_provider_profile_registry,
    build_provider_profile_resolution_input,
    build_provider_profile_resolution_report,
    build_provider_profile_run_preview,
    build_provider_profile_source_ref,
    build_provider_prompt_data_policy,
    build_provider_response_data_policy,
    build_v0341_readiness_report,
    default_mock_provider_profile_descriptor,
    default_provider_invocation_policy,
    default_supplied_output_provider_profile_descriptor,
    provider_invocation_policy_blocks_runtime_access,
    provider_profile_descriptor_is_not_invocation,
    provider_profile_flags_preserve_invocation_false,
    provider_profile_registry_is_not_runtime_registry,
    resolve_provider_profile_from_registry,
    v0341_readiness_report_is_not_invocation_ready,
    validate_provider_profile_descriptor,
    validate_provider_profile_registry,
)
from chanta_core.agent_runtime import provider_profile as profile_module


def test_v0341_taxonomies_cover_required_values() -> None:
    assert ProviderProfileKind.MOCK_PROVIDER.value == "mock_provider"
    assert ProviderProfileKind.SUPPLIED_OUTPUT_PROVIDER.value == "supplied_output_provider"
    assert ProviderProfileKind.EXISTING_CHAT_SERVICE_PROVIDER.value == "existing_chat_service_provider"
    assert ProviderProfileKind.LOCAL_OPENAI_COMPATIBLE_FUTURE_GATE.value == "local_openai_compatible_future_gate"
    assert ProviderProfileKind.REMOTE_PROVIDER_FUTURE_GATE.value == "remote_provider_future_gate"
    assert ProviderBoundaryKind.EXISTING_PROVIDER_BOUNDARY_REF.value == "existing_provider_boundary_ref"
    assert ProviderInvocationModeKind.EXISTING_BOUNDARY_FUTURE_GATE.value == "existing_boundary_future_gate"
    assert ProviderProfileStatus.VALID_METADATA.value == "valid_metadata"
    assert ProviderProfileReadinessLevel.DESIGN_HANDOFF_READY_FOR_V0344.value == "design_handoff_ready_for_v0344"
    assert ProviderProfileSourceKind.OPENCODE_REFERENCE_CONTEXT_REF.value == "opencode_reference_context_ref"
    assert ProviderProfileTrustLevel.FUTURE_GATE.value == "future_gate"
    assert ProviderProfileRiskKind.ENV_READ_RISK.value == "env_read_risk"
    assert ProviderProfileRiskKind.REFERENCE_EXECUTION_RISK.value == "reference_execution_risk"
    assert ProviderProfileValidationDecisionKind.ACCEPT_METADATA_ONLY.value == "accept_metadata_only"
    assert ProviderCredentialPosture.NO_CREDENTIALS_REQUIRED.value == "no_credentials_required"
    assert ProviderNetworkPosture.NO_NETWORK_REQUIRED.value == "no_network_required"


def test_flags_allow_metadata_handoff_only_and_preserve_invocation_false() -> None:
    flags = build_provider_profile_flags()
    assert isinstance(flags, ProviderProfileFlagSet)
    assert flags.provider_profile_registry_constructed is True
    assert flags.provider_profile_validation_available is True
    assert flags.provider_invocation_policy_defined is True
    assert flags.ready_for_v0342_model_request_envelope is True
    assert flags.ready_for_v0343_model_response_envelope is True
    assert flags.ready_for_v0344_existing_provider_boundary_adapter is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_controlled_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_existing_boundary_invocation is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_secret_read is False
    assert flags.production_certified is False
    assert provider_profile_flags_preserve_invocation_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_controlled_model_invocation",
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
        "ready_for_shell_execution",
        "ready_for_subprocess_execution",
        "ready_for_command_execution",
        "ready_for_workspace_write",
        "ready_for_code_edit",
        "ready_for_patch_application",
        "ready_for_persistent_trace_write",
        "ready_for_ui_runtime",
    ],
)
def test_flags_reject_unsafe_readiness(unsafe_flag: str) -> None:
    with pytest.raises(ValueError):
        build_provider_profile_flags(**{unsafe_flag: True})


def test_source_ref_is_metadata_only() -> None:
    source = build_provider_profile_source_ref(
        "source:test",
        ProviderProfileSourceKind.EXISTING_CHAT_SERVICE_BOUNDARY_REF,
        "chat_service",
        "Existing chat service boundary ref only.",
        trust_level=ProviderProfileTrustLevel.BOUNDARY_REF_METADATA,
    )
    assert isinstance(source, ProviderProfileSourceRef)
    assert source.provider_call is False
    assert source.credential_access is False
    assert source.network_access is False
    assert source.file_read is False


def test_credential_and_network_policies_block_access() -> None:
    credential = build_provider_credential_policy()
    assert isinstance(credential, ProviderCredentialPolicy)
    assert credential.allow_env_read is False
    assert credential.allow_secret_file_read is False
    assert credential.allow_inline_secret is False
    assert credential.allow_credential_value_storage is False
    assert credential.allow_credential_logging is False
    assert credential.contains_secret_values is False

    for forbidden in ["allow_env_read", "allow_secret_file_read", "allow_inline_secret", "allow_credential_value_storage", "allow_credential_logging"]:
        with pytest.raises(ValueError):
            build_provider_credential_policy(**{forbidden: True})
    with pytest.raises(ValueError):
        build_provider_credential_policy(credential_ref_name="sk-test")

    network = build_provider_network_policy()
    assert isinstance(network, ProviderNetworkPolicy)
    assert network.endpoint_url_value is None
    assert network.allow_direct_network is False
    assert network.allow_endpoint_value_storage is False
    assert network.allow_arbitrary_endpoint is False
    assert network.allow_localhost_direct_call is False
    assert network.allow_remote_direct_call is False
    assert network.network_access is False

    for forbidden in ["allow_direct_network", "allow_endpoint_value_storage", "allow_arbitrary_endpoint", "allow_localhost_direct_call", "allow_remote_direct_call"]:
        with pytest.raises(ValueError):
            build_provider_network_policy(**{forbidden: True})
    with pytest.raises(ValueError):
        build_provider_network_policy(endpoint_url_value="http://example.invalid")


def test_invocation_prompt_and_response_policies_block_runtime_authority() -> None:
    limit = build_provider_invocation_limit_policy()
    assert isinstance(limit, ProviderInvocationLimitPolicy)
    assert limit.max_retries == 0
    assert limit.allow_retries is False
    assert limit.allow_streaming is False
    assert limit.allow_tool_calls is False
    assert limit.allow_function_calls is False
    assert limit.allow_recursive_calls is False
    assert limit.invocation_constraint_metadata_only is True

    for kwargs in [{"max_retries": 1}, {"allow_retries": True}, {"allow_tool_calls": True}, {"allow_function_calls": True}, {"allow_recursive_calls": True}]:
        with pytest.raises(ValueError):
            build_provider_invocation_limit_policy(**kwargs)

    prompt = build_provider_prompt_data_policy()
    assert isinstance(prompt, ProviderPromptDataPolicy)
    assert prompt.allow_raw_prompt_persistence is False
    assert prompt.allow_secret_in_prompt is False
    assert prompt.allow_credential_in_prompt is False
    assert prompt.allow_file_content_in_prompt is False
    assert prompt.allow_unbounded_prompt is False
    assert prompt.redaction_required is True

    response = build_provider_response_data_policy()
    assert isinstance(response, ProviderResponseDataPolicy)
    assert response.allow_raw_response_persistence is False
    assert response.allow_untrusted_response_as_action is False
    assert response.allow_response_tool_calls is False
    assert response.allow_response_patch is False
    assert response.allow_response_command is False
    assert response.allow_unbounded_response is False
    assert response.redaction_required is True
    assert response.quarantine_required is True

    with pytest.raises(ValueError):
        build_provider_prompt_data_policy(allow_secret_in_prompt=True)
    with pytest.raises(ValueError):
        build_provider_response_data_policy(allow_response_command=True)


def test_provider_descriptors_are_metadata_only() -> None:
    mock = default_mock_provider_profile_descriptor()
    supplied = default_supplied_output_provider_profile_descriptor()
    assert isinstance(mock, ProviderProfileDescriptor)
    assert isinstance(supplied, ProviderProfileDescriptor)
    assert mock.enabled is True
    assert supplied.enabled is True
    assert mock.future_gated is False
    assert supplied.future_gated is False
    for descriptor in [mock, supplied]:
        assert descriptor.invocation_allowed is False
        assert descriptor.provider_sdk_allowed is False
        assert descriptor.network_allowed is False
        assert descriptor.credential_access_allowed is False
        assert descriptor.secret_read_allowed is False
        assert provider_profile_descriptor_is_not_invocation(descriptor)

    future_local = build_provider_profile_descriptor(
        "provider_profile:local_future",
        "local_openai_compatible_future_gate",
        ProviderProfileKind.LOCAL_OPENAI_COMPATIBLE_FUTURE_GATE,
    )
    assert future_local.future_gated is True
    assert future_local.enabled is False
    assert future_local.invocation_allowed is False

    with pytest.raises(ValueError):
        default_mock_provider_profile_descriptor(invocation_allowed=True)
    with pytest.raises(ValueError):
        default_mock_provider_profile_descriptor(provider_sdk_allowed=True)
    with pytest.raises(ValueError):
        default_mock_provider_profile_descriptor(network_allowed=True)
    with pytest.raises(ValueError):
        default_mock_provider_profile_descriptor(credential_access_allowed=True)
    with pytest.raises(ValueError):
        build_provider_profile_descriptor("provider_profile:bad_future", "remote", ProviderProfileKind.REMOTE_PROVIDER_FUTURE_GATE, future_gated=False)


def test_registry_and_invocation_policy_are_not_runtime() -> None:
    registry = build_provider_profile_registry()
    assert isinstance(registry, ProviderProfileRegistry)
    assert registry.ready_for_v0342_model_request_envelope is True
    assert registry.ready_for_v0343_model_response_envelope is True
    assert registry.ready_for_v0344_existing_provider_boundary_adapter is True
    assert registry.ready_for_invocation is False
    assert registry.ready_for_execution is False
    assert registry.provider_runtime is False
    assert provider_profile_registry_is_not_runtime_registry(registry)

    policy = default_provider_invocation_policy()
    assert isinstance(policy, ProviderInvocationPolicy)
    assert policy.allow_mock_provider is True
    assert policy.allow_supplied_output_provider is True
    assert policy.allow_existing_boundary_ref is True
    assert policy.allow_existing_boundary_invocation is False
    assert policy.allow_local_provider_invocation is False
    assert policy.allow_remote_provider_invocation is False
    assert policy.allow_direct_provider_sdk is False
    assert policy.allow_direct_network is False
    assert policy.allow_credential_read is False
    assert policy.allow_secret_read is False
    assert policy.allow_tool_calls is False
    assert policy.allow_recursive_calls is False
    assert policy.invocation_permission is False
    assert provider_invocation_policy_blocks_runtime_access(policy)

    for forbidden in [
        "allow_existing_boundary_invocation",
        "allow_local_provider_invocation",
        "allow_remote_provider_invocation",
        "allow_direct_provider_sdk",
        "allow_direct_network",
        "allow_credential_read",
        "allow_secret_read",
        "allow_tool_calls",
        "allow_recursive_calls",
    ]:
        with pytest.raises(ValueError):
            default_provider_invocation_policy(**{forbidden: True})


def test_validation_and_resolution_reports_preserve_no_invocation() -> None:
    registry = build_provider_profile_registry()
    policy = default_provider_invocation_policy()
    finding = validate_provider_profile_descriptor(registry.descriptors[0], policy)
    assert isinstance(finding, ProviderProfileValidationFinding)
    assert finding.decision_kind == ProviderProfileValidationDecisionKind.ACCEPT_METADATA_ONLY
    assert finding.invocation is False

    report = validate_provider_profile_registry(registry, policy)
    assert isinstance(report, ProviderProfileValidationReport)
    assert report.validation_passed is True
    assert report.ready_for_invocation is False
    assert report.ready_for_execution is False
    assert report.runtime_certification is False

    resolution_input = build_provider_profile_resolution_input(
        "resolution_input:test",
        requested_profile_name="mock_provider",
        requested_profile_kind=ProviderProfileKind.MOCK_PROVIDER,
        registry_id=registry.registry_id,
        invocation_policy_id=policy.invocation_policy_id,
    )
    assert isinstance(resolution_input, ProviderProfileResolutionInput)
    assert resolution_input.provider_invocation_request is False

    decision = resolve_provider_profile_from_registry(resolution_input, registry, policy)
    assert isinstance(decision, ProviderProfileResolutionDecision)
    assert decision.selected_provider_profile_id == "provider_profile:mock:v0.34.1"
    assert decision.invocation_allowed is False
    assert decision.provider_invocation_allowed is False
    assert decision.network_allowed is False
    assert decision.credential_access_allowed is False
    assert decision.secret_read_allowed is False
    assert decision.provider_invocation is False

    resolution_report = build_provider_profile_resolution_report(
        resolution_input_id=resolution_input.resolution_input_id,
        resolution_decision_id=decision.resolution_decision_id,
        selected_provider_profile_id=decision.selected_provider_profile_id,
    )
    assert isinstance(resolution_report, ProviderProfileResolutionReport)
    assert resolution_report.ready_for_v0342_model_request_envelope is True
    assert resolution_report.ready_for_v0343_model_response_envelope is True
    assert resolution_report.ready_for_v0344_existing_provider_boundary_adapter is True
    assert resolution_report.ready_for_invocation is False
    assert resolution_report.ready_for_execution is False
    assert resolution_report.invocation is False

    with pytest.raises(ValueError):
        ProviderProfileValidationReport(
            validation_report_id="validation:bad",
            version="v0.34.1",
            registry_id=None,
            descriptor_ids_checked=[],
            valid_metadata_profile_ids=[],
            blocked_profile_ids=["blocked"],
            future_gated_profile_ids=[],
            findings=[],
            validation_passed=True,
            summary="bad",
        )
    with pytest.raises(ValueError):
        ProviderProfileResolutionDecision(
            resolution_decision_id="decision:bad",
            resolution_input_id=resolution_input.resolution_input_id,
            selected_provider_profile_id=None,
            selected_profile_kind=None,
            decision_kind=ProviderProfileValidationDecisionKind.DENY,
            reason="bad",
            invocation_allowed=True,
        )


def test_run_preview_guarantee_and_readiness_are_conservative() -> None:
    preview = build_provider_profile_run_preview()
    assert isinstance(preview, ProviderProfileRunPreview)
    assert preview.invocation is False
    for name in preview.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(preview, name) is True

    guarantee = build_provider_profile_no_invocation_guarantee()
    assert isinstance(guarantee, ProviderProfileNoInvocationGuarantee)
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    readiness = build_v0341_readiness_report()
    assert isinstance(readiness, V0341ReadinessReport)
    assert readiness.ready_for_v0342_model_request_envelope is True
    assert readiness.ready_for_v0343_model_response_envelope is True
    assert readiness.ready_for_v0344_existing_provider_boundary_adapter is True
    assert readiness.ready_for_execution is False
    assert readiness.ready_for_controlled_model_invocation is False
    assert readiness.ready_for_provider_invocation is False
    assert readiness.ready_for_existing_boundary_invocation is False
    assert readiness.ready_for_network_access is False
    assert readiness.ready_for_credential_access is False
    assert readiness.ready_for_secret_read is False
    assert v0341_readiness_report_is_not_invocation_ready(readiness)

    with pytest.raises(ValueError):
        build_v0341_readiness_report(ready_for_provider_invocation=True)
    with pytest.raises(ValueError):
        build_v0341_readiness_report(ready_for_existing_boundary_invocation=True)
    with pytest.raises(ValueError):
        build_v0341_readiness_report(ready_for_network_access=True)
    with pytest.raises(ValueError):
        build_v0341_readiness_report(ready_for_credential_access=True)


def test_direct_dataclass_construction_with_valid_inputs() -> None:
    source = ProviderProfileSourceRef(
        source_ref_id="source:direct",
        source_kind=ProviderProfileSourceKind.TEST_FIXTURE,
        source_id="fixture",
        source_summary="fixture source ref only",
        trust_level=ProviderProfileTrustLevel.TEST_FIXTURE,
    )
    descriptor = ProviderProfileDescriptor(
        provider_profile_id="provider_profile:direct",
        profile_name="mock_direct",
        profile_kind=ProviderProfileKind.MOCK_PROVIDER,
        boundary_kind=ProviderBoundaryKind.MOCK_BOUNDARY,
        invocation_mode=ProviderInvocationModeKind.MOCK_ONLY,
        credential_policy=build_provider_credential_policy("credential_policy:direct"),
        network_policy=build_provider_network_policy("network_policy:direct"),
        limit_policy=build_provider_invocation_limit_policy("limit_policy:direct"),
        prompt_data_policy=build_provider_prompt_data_policy("prompt_policy:direct"),
        response_data_policy=build_provider_response_data_policy("response_policy:direct"),
        source_refs=[source],
        status=ProviderProfileStatus.VALID_METADATA,
        readiness_level=ProviderProfileReadinessLevel.METADATA_VALIDATION_READY,
        description="direct metadata descriptor",
        enabled=True,
    )
    flags = ProviderProfileFlagSet(flag_set_id="flags:direct", provider_profile_registry_constructed=True)
    registry = ProviderProfileRegistry(
        registry_id="registry:direct",
        version="v0.34.1",
        descriptors=[descriptor],
        descriptor_ids=[descriptor.provider_profile_id],
        enabled_profile_names=[descriptor.profile_name],
        disabled_profile_names=[],
        blocked_profile_names=[],
        future_gated_profile_names=[],
        flags=flags,
        source_refs=[source],
        summary="direct registry metadata only",
    )
    assert descriptor.provider_runtime is False
    assert registry.provider_runtime is False
    assert provider_profile_registry_is_not_runtime_registry(registry)


def test_helpers_are_pure_conservative_source() -> None:
    source = inspect.getsource(profile_module)
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
        "ready_for_shell_execution=True",
        "ready_for_subprocess_execution=True",
        "ready_for_command_execution=True",
        "ready_for_workspace_write=True",
        "ready_for_code_edit=True",
        "ready_for_patch_application=True",
        "ready_for_persistent_trace_write=True",
        "ready_for_ui_runtime=True",
        "production_certified=True",
    ]
    compact = source.replace(" ", "")
    for pattern in unsafe_true_patterns:
        assert pattern not in compact
