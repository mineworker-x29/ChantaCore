import inspect

import pytest

from chanta_core.agent_runtime import (
    ControlledCredentialPosture,
    ControlledModelInvocationAllowedSurface,
    ControlledModelInvocationBoundary,
    ControlledModelInvocationBoundaryStatus,
    ControlledModelInvocationCapabilityKind,
    ControlledModelInvocationDecisionKind,
    ControlledModelInvocationDeniedAction,
    ControlledModelInvocationFlagSet,
    ControlledModelInvocationGateEvaluation,
    ControlledModelInvocationNoExternalSideEffectGuarantee,
    ControlledModelInvocationPermissionDecision,
    ControlledModelInvocationPermissionRequest,
    ControlledModelInvocationProhibitedSurface,
    ControlledModelInvocationReadinessLevel,
    ControlledModelInvocationRiskKind,
    ControlledModelInvocationRiskRegister,
    ControlledModelInvocationSourceKind,
    ControlledModelInvocationSourceRef,
    ControlledModelInvocationSurfaceKind,
    ControlledModelInvocationTrackKind,
    ControlledNetworkPosture,
    ControlledProviderBoundaryPosture,
    ControlledProviderSurfacePolicy,
    ExistingProviderBoundaryRef,
    V0340ReadinessReport,
    V034RoadmapOverview,
    build_controlled_model_invocation_allowed_surface,
    build_controlled_model_invocation_boundary,
    build_controlled_model_invocation_denied_action,
    build_controlled_model_invocation_flags,
    build_controlled_model_invocation_gate_evaluation,
    build_controlled_model_invocation_no_external_side_effect_guarantee,
    build_controlled_model_invocation_permission_decision,
    build_controlled_model_invocation_permission_request,
    build_controlled_model_invocation_prohibited_surface,
    build_controlled_model_invocation_risk_register,
    build_controlled_model_invocation_source_ref,
    build_controlled_provider_surface_policy,
    build_existing_provider_boundary_ref,
    build_v0340_readiness_report,
    build_v034_roadmap_overview,
    controlled_model_invocation_boundary_is_not_invocation,
    controlled_model_invocation_decision_is_not_invocation,
    controlled_model_invocation_flags_preserve_invocation_false,
    controlled_provider_surface_policy_blocks_direct_access,
    existing_provider_boundary_ref_is_not_invocation,
    v0340_readiness_report_is_not_invocation_ready,
)
from chanta_core.agent_runtime import model_invocation_boundary as boundary_module


def test_v0340_taxonomies_cover_required_values() -> None:
    assert ControlledModelInvocationTrackKind.BOUNDARY_FOUNDATION.value == "boundary_foundation"
    assert ControlledModelInvocationTrackKind.PROVIDER_PROFILE_POLICY.value == "provider_profile_policy"
    assert ControlledModelInvocationTrackKind.CONSOLIDATION.value == "consolidation"
    assert ControlledModelInvocationSurfaceKind.EXISTING_PROVIDER_BOUNDARY.value == "existing_provider_boundary"
    assert ControlledModelInvocationSurfaceKind.PROVIDER_SDK_DIRECT.value == "provider_sdk_direct"
    assert ControlledModelInvocationSurfaceKind.CREDENTIAL_STORE.value == "credential_store"
    assert ControlledModelInvocationSurfaceKind.REFERENCE_CODE.value == "reference_code"
    assert ControlledModelInvocationCapabilityKind.CALL_EXISTING_PROVIDER_BOUNDARY.value == "call_existing_provider_boundary"
    assert ControlledModelInvocationCapabilityKind.CALL_PROVIDER_SDK_DIRECT.value == "call_provider_sdk_direct"
    assert ControlledModelInvocationCapabilityKind.READ_CREDENTIAL.value == "read_credential"
    assert ControlledModelInvocationCapabilityKind.EXECUTE_REFERENCE_CODE.value == "execute_reference_code"
    assert ControlledModelInvocationRiskKind.PROVIDER_INVOCATION_RISK.value == "provider_invocation_risk"
    assert ControlledModelInvocationRiskKind.AUTONOMOUS_LOOP_RISK.value == "autonomous_loop_risk"
    assert ControlledModelInvocationDecisionKind.ALLOW_DESIGN_STAGE_BOUNDARY_DEFINITION.value == "allow_design_stage_boundary_definition"
    assert ControlledModelInvocationBoundaryStatus.BOUNDARY_READY_WITH_GAPS.value == "boundary_ready_with_gaps"
    assert ControlledModelInvocationReadinessLevel.BOUNDARY_CONTRACT_READY.value == "boundary_contract_ready"
    assert ControlledProviderBoundaryPosture.EXISTING_BOUNDARY_REF_ONLY.value == "existing_boundary_ref_only"
    assert ControlledCredentialPosture.NO_CREDENTIAL_ACCESS.value == "no_credential_access"
    assert ControlledNetworkPosture.NO_NETWORK_ACCESS.value == "no_network_access"


def test_flags_allow_boundary_handoff_only_and_preserve_invocation_false() -> None:
    flags = build_controlled_model_invocation_flags()
    assert flags.controlled_model_invocation_boundary_constructed is True
    assert flags.provider_surface_policy_defined is True
    assert flags.model_invocation_risk_register_defined is True
    assert flags.ready_for_v0341_provider_profile_policy is True
    assert flags.ready_for_v0342_model_request_envelope is True
    assert flags.ready_for_execution is False
    assert flags.ready_for_controlled_model_invocation is False
    assert flags.ready_for_real_model_invocation is False
    assert flags.ready_for_model_invocation is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_provider_sdk_invocation is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_secret_read is False
    assert flags.ready_for_agent_step_execution is False
    assert flags.ready_for_general_agent_execution is False
    assert flags.ready_for_autonomous_agent_runtime is False
    assert flags.ready_for_general_tool_execution is False
    assert flags.ready_for_shell_execution is False
    assert flags.ready_for_subprocess_execution is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_workspace_write is False
    assert flags.ready_for_code_edit is False
    assert flags.ready_for_patch_application is False
    assert flags.ready_for_persistent_trace_write is False
    assert flags.ready_for_ui_runtime is False
    assert flags.production_certified is False
    assert controlled_model_invocation_flags_preserve_invocation_false(flags)


@pytest.mark.parametrize(
    "unsafe_flag",
    [
        "ready_for_execution",
        "ready_for_controlled_model_invocation",
        "ready_for_model_invocation",
        "ready_for_provider_invocation",
        "ready_for_provider_sdk_invocation",
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
        build_controlled_model_invocation_flags(**{unsafe_flag: True})


def test_source_ref_and_existing_provider_boundary_ref_are_not_invocation() -> None:
    source = build_controlled_model_invocation_source_ref(
        "source:test",
        ControlledModelInvocationSourceKind.EXISTING_CHAT_SERVICE_BOUNDARY_REF,
        "chat_service",
        "String ref only.",
    )
    assert isinstance(source, ControlledModelInvocationSourceRef)
    assert source.provider_call is False
    assert source.credential_access is False
    assert source.file_read is False

    ref = build_existing_provider_boundary_ref()
    assert isinstance(ref, ExistingProviderBoundaryRef)
    assert ref.direct_invocation_allowed is False
    assert ref.provider_sdk_import_allowed is False
    assert ref.credential_read_allowed is False
    assert ref.network_call_allowed is False
    assert ref.invocation is False
    assert existing_provider_boundary_ref_is_not_invocation(ref)

    with pytest.raises(ValueError):
        build_existing_provider_boundary_ref(direct_invocation_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_ref(provider_sdk_import_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_ref(credential_read_allowed=True)
    with pytest.raises(ValueError):
        build_existing_provider_boundary_ref(network_call_allowed=True)


def test_provider_surface_policy_blocks_direct_access() -> None:
    policy = build_controlled_provider_surface_policy()
    assert isinstance(policy, ControlledProviderSurfacePolicy)
    assert policy.allow_existing_boundary_ref is True
    assert policy.allow_existing_boundary_invocation is False
    assert policy.allow_direct_provider_sdk is False
    assert policy.allow_direct_network is False
    assert policy.allow_credential_read is False
    assert policy.allow_secret_read is False
    assert policy.allow_endpoint_construction is False
    assert policy.allow_recursive_model_call is False
    assert policy.allow_autonomous_loop is False
    assert policy.invocation is False
    assert controlled_provider_surface_policy_blocks_direct_access(policy)

    for forbidden in [
        "allow_existing_boundary_invocation",
        "allow_direct_provider_sdk",
        "allow_direct_network",
        "allow_credential_read",
        "allow_secret_read",
        "allow_endpoint_construction",
        "allow_recursive_model_call",
        "allow_autonomous_loop",
    ]:
        with pytest.raises(ValueError):
            build_controlled_provider_surface_policy(**{forbidden: True})


def test_allowed_and_prohibited_surfaces_are_boundary_metadata() -> None:
    allowed = build_controlled_model_invocation_allowed_surface("allowed:test")
    assert isinstance(allowed, ControlledModelInvocationAllowedSurface)
    assert allowed.allowed_only_for_design_stage is True
    assert allowed.allowed_only_as_ref is True
    assert allowed.executable_in_v0340 is False
    assert allowed.invocation is False

    prohibited = build_controlled_model_invocation_prohibited_surface("prohibited:test")
    assert isinstance(prohibited, ControlledModelInvocationProhibitedSurface)
    assert prohibited.blocks_invocation is True
    assert prohibited.blocks_runtime_readiness is True
    assert prohibited.boundary_metadata is True

    with pytest.raises(ValueError):
        build_controlled_model_invocation_allowed_surface("allowed:bad", executable_in_v0340=True)
    with pytest.raises(ValueError):
        build_controlled_model_invocation_prohibited_surface("prohibited:bad", blocks_invocation=False)


def test_boundary_request_decision_and_gate_preserve_no_invocation() -> None:
    boundary = build_controlled_model_invocation_boundary()
    assert isinstance(boundary, ControlledModelInvocationBoundary)
    assert boundary.ready_for_v0341_provider_profile_policy is True
    assert boundary.ready_for_v0342_model_request_envelope is True
    assert boundary.ready_for_execution is False
    assert boundary.provider_invocation is False
    assert controlled_model_invocation_boundary_is_not_invocation(boundary)

    request = build_controlled_model_invocation_permission_request("request:test")
    assert isinstance(request, ControlledModelInvocationPermissionRequest)
    assert request.invocation is False

    decision = build_controlled_model_invocation_permission_decision("decision:test", request.request_id)
    assert isinstance(decision, ControlledModelInvocationPermissionDecision)
    assert decision.invocation_allowed is False
    assert decision.provider_invocation_allowed is False
    assert decision.provider_sdk_allowed is False
    assert decision.network_allowed is False
    assert decision.credential_access_allowed is False
    assert decision.secret_read_allowed is False
    assert decision.agent_step_execution_allowed is False
    assert controlled_model_invocation_decision_is_not_invocation(decision)

    denied = build_controlled_model_invocation_denied_action("denied:test")
    assert isinstance(denied, ControlledModelInvocationDeniedAction)
    assert denied.safe_outcome is True

    evaluation = build_controlled_model_invocation_gate_evaluation("eval:test", boundary.boundary_id, request.request_id, decision, denied_actions=[denied])
    assert isinstance(evaluation, ControlledModelInvocationGateEvaluation)
    assert evaluation.invocation_allowed is False
    assert evaluation.provider_invocation_allowed is False
    assert evaluation.network_allowed is False
    assert evaluation.credential_access_allowed is False
    assert evaluation.invocation is False

    with pytest.raises(ValueError):
        build_controlled_model_invocation_permission_decision("decision:bad", request.request_id, invocation_allowed=True)
    with pytest.raises(ValueError):
        build_controlled_model_invocation_permission_decision("decision:bad2", request.request_id, provider_invocation_allowed=True)
    with pytest.raises(ValueError):
        build_controlled_model_invocation_permission_decision("decision:bad3", request.request_id, network_allowed=True)
    with pytest.raises(ValueError):
        build_controlled_model_invocation_gate_evaluation("eval:bad", boundary.boundary_id, request.request_id, decision, invocation_allowed=True)


def test_risk_register_guarantee_roadmap_and_readiness_are_conservative() -> None:
    risk = build_controlled_model_invocation_risk_register()
    assert isinstance(risk, ControlledModelInvocationRiskRegister)
    joined_caps = " ".join(str(value) for value in risk.prohibited_capabilities).lower()
    for term in ["provider_sdk", "network", "credential", "secret", "autonomous", "shell", "write", "edit", "patch", "reference"]:
        assert term in joined_caps
    assert risk.permission is False

    guarantee = build_controlled_model_invocation_no_external_side_effect_guarantee()
    assert isinstance(guarantee, ControlledModelInvocationNoExternalSideEffectGuarantee)
    for name in guarantee.__dataclass_fields__:
        if name.startswith("no_"):
            assert getattr(guarantee, name) is True

    roadmap = build_v034_roadmap_overview()
    assert isinstance(roadmap, V034RoadmapOverview)
    assert set(boundary_module.DEFAULT_V034_STAGES).issubset({ControlledModelInvocationTrackKind(value).value for value in roadmap.stages})
    assert "future-gated existing boundary ref only" in roadmap.existing_provider_boundary_role.lower()
    assert roadmap.implementation is False

    report = build_v0340_readiness_report()
    assert isinstance(report, V0340ReadinessReport)
    assert report.ready_for_v0341_provider_profile_policy is True
    assert report.ready_for_v0342_model_request_envelope is True
    assert report.ready_for_execution is False
    assert report.ready_for_controlled_model_invocation is False
    assert report.ready_for_provider_invocation is False
    assert report.ready_for_network_access is False
    assert report.ready_for_credential_access is False
    assert report.ready_for_secret_read is False
    assert v0340_readiness_report_is_not_invocation_ready(report)

    with pytest.raises(ValueError):
        build_v0340_readiness_report(ready_for_controlled_model_invocation=True)
    with pytest.raises(ValueError):
        build_v0340_readiness_report(ready_for_provider_invocation=True)
    with pytest.raises(ValueError):
        build_v0340_readiness_report(ready_for_network_access=True)
    with pytest.raises(ValueError):
        build_v0340_readiness_report(ready_for_credential_access=True)


def test_direct_dataclass_construction_with_valid_inputs() -> None:
    flags = ControlledModelInvocationFlagSet(
        flag_set_id="flags:direct",
        version="v0.34.0",
        controlled_model_invocation_boundary_constructed=True,
    )
    source = ControlledModelInvocationSourceRef(
        source_ref_id="source:direct",
        source_kind=ControlledModelInvocationSourceKind.TEST_FIXTURE,
        source_id="fixture",
        source_summary="fixture ref only",
    )
    ref = ExistingProviderBoundaryRef(
        provider_boundary_ref_id="ref:direct",
        boundary_name="chat_service",
        boundary_kind="future_gated_existing_boundary_ref",
        boundary_summary="ref only",
        allowed_use_in_v0340="future-gated ref only",
        source_refs=[source],
    )
    policy = ControlledProviderSurfacePolicy(
        policy_id="policy:direct",
        allowed_surfaces=[ControlledModelInvocationSurfaceKind.EXISTING_PROVIDER_BOUNDARY],
        prohibited_surfaces=[ControlledModelInvocationSurfaceKind.PROVIDER_SDK_DIRECT],
        prohibited_capabilities=list(boundary_module.DEFAULT_PROHIBITED_CAPABILITIES),
    )
    boundary = ControlledModelInvocationBoundary(
        boundary_id="boundary:direct",
        version="v0.34.0",
        release_name="v0.34.0 Controlled Model Invocation Boundary Foundation",
        provider_surface_policy=policy,
        existing_provider_boundary_refs=[ref],
        allowed_surfaces=[build_controlled_model_invocation_allowed_surface("allowed:direct")],
        prohibited_surfaces=[build_controlled_model_invocation_prohibited_surface("prohibited:direct")],
        flags=flags,
        status=ControlledModelInvocationBoundaryStatus.BOUNDARY_READY,
        readiness_level=ControlledModelInvocationReadinessLevel.BOUNDARY_CONTRACT_READY,
        summary="direct construction remains boundary metadata",
    )
    assert boundary.ready_for_execution is False
    assert ref.invocation is False
    assert policy.invocation is False


def test_helpers_are_pure_conservative_source() -> None:
    source = inspect.getsource(boundary_module)
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
