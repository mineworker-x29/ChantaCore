import pytest

from chanta_core.agent_runtime import (
    AgentProfileContextRoleKind,
    AgentProfileEvidenceQuality,
    AgentProfileKind,
    AgentProfileLoadoutKind,
    AgentProfileModeBinding,
    AgentProfileModeKind,
    AgentProfilePolicyOverlay,
    AgentProfilePolicyOverlayKind,
    AgentProfileProjectionKind,
    AgentProfileReadinessLevel,
    AgentProfileReferenceContext,
    AgentProfileResolutionDecision,
    AgentProfileResolutionReport,
    AgentProfileResolutionStatus,
    AgentProfileRuntimeFlagSet,
    AgentProfileRuntimeNoExecutionGuarantee,
    AgentProfileRuntimeRunPreview,
    AgentProfileSourceKind,
    AgentProfileSourceRef,
    AgentProfileToolAvailabilityView,
    AgentRuntimeLoadout,
    AgentRuntimeProfile,
    V0331ReadinessReport,
    agent_profile_flags_preserve_runtime_false,
    agent_profile_resolution_report_is_not_runtime,
    agent_reference_context_preserves_no_file_access,
    agent_runtime_profile_is_not_active_session,
    build_agent_profile_mode_binding,
    build_agent_profile_persona_projection,
    build_agent_profile_policy_overlay,
    build_agent_profile_reference_context,
    build_agent_profile_resolution_decision,
    build_agent_profile_resolution_input,
    build_agent_profile_resolution_report,
    build_agent_profile_runtime_flags,
    build_agent_profile_runtime_no_execution_guarantee,
    build_agent_profile_runtime_run_preview,
    build_agent_profile_source_ref,
    build_agent_profile_tool_availability_view,
    build_agent_runtime_loadout,
    build_agent_runtime_profile,
    build_internal_runtime_boundary,
    build_v0331_readiness_report,
    resolve_agent_runtime_profile_from_input,
    v0331_readiness_report_is_not_runtime_ready,
)
from chanta_core.agent_runtime.profile_runtime import (
    DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS,
    RUNTIME_FLAG_NAMES,
)


def test_agent_profile_taxonomies_and_runtime_flags_are_non_runtime():
    assert {item.value for item in AgentProfileKind} == {
        "vera",
        "chanta_core",
        "chanta_research_group",
        "schumpeter",
        "generic_internal_agent",
        "test_profile",
        "unknown",
    }
    assert "coding_assistant" in {item.value for item in AgentProfileModeKind}
    assert "safe_readonly" in {item.value for item in AgentProfileModeKind}
    assert "memory_context_ref" in {item.value for item in AgentProfileSourceKind}
    assert "persona_projection" in {item.value for item in AgentProfileProjectionKind}
    assert "no_provider_invocation" in {item.value for item in AgentProfilePolicyOverlayKind}
    assert "profile_with_tool_availability_view" in {item.value for item in AgentProfileLoadoutKind}
    assert "opencode_reference_role" in {item.value for item in AgentProfileContextRoleKind}
    assert "hermes_reference_role" in {item.value for item in AgentProfileContextRoleKind}
    assert "resolved_with_gaps" in {item.value for item in AgentProfileResolutionStatus}
    assert "design_handoff_ready_for_v0332" in {item.value for item in AgentProfileReadinessLevel}
    assert "sufficient_for_profile_resolution" in {item.value for item in AgentProfileEvidenceQuality}

    flags = build_agent_profile_runtime_flags(
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
    )

    assert flags.ready_for_v0332_prompt_assembly is True
    assert flags.ready_for_v0333_session_runtime is True
    assert agent_profile_flags_preserve_runtime_false(flags)

    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            AgentProfileRuntimeFlagSet(
                flag_set_id=f"flags:bad:{flag_name}",
                version="v0.33.1",
                **{flag_name: True},
            )


def test_source_persona_mode_policy_reference_and_tool_view_preserve_boundaries():
    source_ref = build_agent_profile_source_ref(
        "source:profile",
        AgentProfileSourceKind.MANUAL_PROFILE_SPEC,
        "profile-spec:vera",
        "In-memory Vera profile metadata.",
    )
    persona = build_agent_profile_persona_projection(
        "projection:vera",
        source_refs=[source_ref],
        evidence_quality=AgentProfileEvidenceQuality.SUFFICIENT_FOR_PROFILE_RESOLUTION,
    )
    mode = build_agent_profile_mode_binding(
        "mode:coding",
        mode_kind=AgentProfileModeKind.CODING_ASSISTANT,
        active_context_roles=[
            AgentProfileContextRoleKind.PRIMARY_PERSONA,
            AgentProfileContextRoleKind.OPENCODE_REFERENCE_ROLE,
            AgentProfileContextRoleKind.HERMES_REFERENCE_ROLE,
        ],
        source_refs=[source_ref],
    )
    policy = build_agent_profile_policy_overlay("policy:safe", source_refs=[source_ref])
    reference = build_agent_profile_reference_context("reference:openharness", source_refs=[source_ref])
    tools = build_agent_profile_tool_availability_view(
        "tools:view",
        unavailable_tool_names=["shell", "provider"],
        future_tool_names=["safe_readonly_tool_registry:v0.33.4"],
        source_refs=[source_ref],
    )

    assert source_ref.fetch is False
    assert source_ref.memory_read is False
    assert source_ref.execution is False
    assert persona.authority_grant is False
    assert mode.ready_for_tool_activation is False
    assert mode.ready_for_execution is False
    assert mode.tool_activation is False
    assert policy.required_permission_gate is True
    assert policy.required_safe_fail is True
    assert policy.ready_for_policy_activation is False
    assert policy.active_policy_enforcement is False
    assert reference.opencode_reference_path_ref == "references/OpenCode"
    assert reference.hermes_reference_path_ref == "references/Hermes"
    assert agent_reference_context_preserves_no_file_access(reference)
    assert tools.ready_for_tool_registry_access is False
    assert tools.ready_for_tool_execution is False
    assert tools.tool_registry_access is False

    with pytest.raises(ValueError):
        AgentProfileSourceRef(
            source_ref_id="source:bad",
            source_kind=AgentProfileSourceKind.MEMORY_CONTEXT_REF,
            source_id="memory",
            source_summary="bad",
            metadata={"memory_read": True},
        )
    with pytest.raises(ValueError):
        AgentProfileModeBinding(
            mode_binding_id="mode:bad",
            mode_kind=AgentProfileModeKind.SAFE_READONLY,
            title="bad",
            summary="bad",
            ready_for_tool_activation=True,
        )
    with pytest.raises(ValueError):
        AgentProfilePolicyOverlay(
            policy_overlay_id="policy:bad",
            ready_for_policy_activation=True,
        )
    for flag_name in (
        "ready_for_reference_file_access",
        "ready_for_reference_code_execution",
        "ready_for_reference_import",
        "ready_for_reference_dependency_install",
    ):
        with pytest.raises(ValueError):
            AgentProfileReferenceContext(
                reference_context_id=f"reference:bad:{flag_name}",
                posture="path_reference_only",
                **{flag_name: True},
            )
    with pytest.raises(ValueError):
        AgentProfileToolAvailabilityView(
            tool_availability_view_id="tools:bad",
            summary="bad",
            ready_for_tool_execution=True,
        )


def test_loadout_runtime_profile_input_decision_and_report_are_not_execution():
    source_ref = build_agent_profile_source_ref("source:loadout")
    persona = build_agent_profile_persona_projection("projection:loadout", source_refs=[source_ref])
    mode = build_agent_profile_mode_binding("mode:loadout", source_refs=[source_ref])
    policy = build_agent_profile_policy_overlay("policy:loadout", source_refs=[source_ref])
    reference = build_agent_profile_reference_context("reference:loadout", source_refs=[source_ref])
    tools = build_agent_profile_tool_availability_view("tools:loadout", source_refs=[source_ref])
    loadout = build_agent_runtime_loadout(
        "loadout:1",
        persona,
        mode,
        policy,
        reference_context=reference,
        tool_availability_view=tools,
        source_refs=[source_ref],
        ready_for_prompt_assembly=True,
        ready_for_session_runtime=True,
    )
    flags = build_agent_profile_runtime_flags(
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
    )
    profile = build_agent_runtime_profile(
        "profile:1",
        loadout,
        flags,
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
    )
    resolution_input = build_agent_profile_resolution_input(
        "input:1",
        source_refs=[source_ref],
        requested_context_roles=[AgentProfileContextRoleKind.PRIMARY_PERSONA],
    )
    decision = build_agent_profile_resolution_decision(
        "decision:1",
        resolution_input.resolution_input_id,
        ready_for_profile_resolution=True,
        selected_context_roles=[AgentProfileContextRoleKind.PRIMARY_PERSONA],
        denied_runtime_surfaces=["provider_invocation", "tool_execution"],
    )
    report = build_agent_profile_resolution_report(
        "report:1",
        resolution_input.resolution_input_id,
        runtime_profile_id=profile.runtime_profile_id,
        decision_id=decision.resolution_decision_id,
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
    )

    assert loadout.ready_for_execution is False
    assert loadout.runtime_action is False
    assert agent_runtime_profile_is_not_active_session(profile)
    assert profile.active_session is False
    assert set(DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS).issubset(set(resolution_input.prohibited_runtime_actions))
    assert resolution_input.runtime_execution_request is False
    assert decision.ready_for_execution is False
    assert decision.permission_grant is False
    assert agent_profile_resolution_report_is_not_runtime(report)

    with pytest.raises(ValueError):
        AgentRuntimeLoadout(
            loadout_id="loadout:bad",
            loadout_kind=AgentProfileLoadoutKind.PROFILE_ONLY,
            persona_projection=persona,
            mode_binding=mode,
            policy_overlay=policy,
            reference_context=reference,
            tool_availability_view=tools,
            runtime_boundary_id=None,
            summary="bad",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        AgentRuntimeProfile(
            runtime_profile_id="profile:bad",
            profile_kind=AgentProfileKind.VERA,
            mode_kind=AgentProfileModeKind.DEFAULT,
            display_name="bad",
            description="bad",
            loadout=loadout,
            runtime_flags=flags,
            status=AgentProfileResolutionStatus.RESOLVED,
            readiness_level=AgentProfileReadinessLevel.PROFILE_RESOLUTION_READY,
            summary="bad",
            metadata={"active_session": True},
        )
    with pytest.raises(ValueError):
        AgentProfileResolutionDecision(
            resolution_decision_id="decision:bad",
            resolution_input_id=resolution_input.resolution_input_id,
            decision_kind="resolve",
            summary="bad",
            selected_profile_kind=AgentProfileKind.VERA,
            selected_mode_kind=AgentProfileModeKind.DEFAULT,
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        AgentProfileResolutionReport(
            report_id="report:bad",
            version="v0.33.1",
            resolution_input_id=resolution_input.resolution_input_id,
            runtime_profile_id=None,
            decision_id=None,
            summary="bad",
            status=AgentProfileResolutionStatus.BLOCKED,
            readiness_level=AgentProfileReadinessLevel.BLOCKED,
            ready_for_v0332_prompt_assembly=True,
            blocked_items=["blocked"],
        )


def test_preview_guarantee_readiness_and_resolution_helper_are_conservative():
    preview = build_agent_profile_runtime_run_preview("preview:1")
    guarantee = build_agent_profile_runtime_no_execution_guarantee("guarantee:1")
    readiness = build_v0331_readiness_report(
        "readiness:1",
        ready_for_v0332_prompt_assembly=True,
        ready_for_v0333_session_runtime=True,
        completed_items=["profile runtime contract"],
    )
    boundary = build_internal_runtime_boundary("boundary:v0331")
    source_ref = build_agent_profile_source_ref(
        "source:fake",
        AgentProfileSourceKind.TEST_FIXTURE,
        "fixture:vera-opencode-hermes",
        "Fake in-memory Vera/OpenCode/Hermes profile metadata.",
    )
    resolution_input = build_agent_profile_resolution_input(
        "input:fake",
        requested_profile_kind=AgentProfileKind.VERA,
        requested_mode_kind=AgentProfileModeKind.CODING_ASSISTANT,
        runtime_boundary_id=boundary.boundary_id,
        source_refs=[source_ref],
        requested_context_roles=[
            AgentProfileContextRoleKind.PRIMARY_PERSONA,
            AgentProfileContextRoleKind.OPENCODE_REFERENCE_ROLE,
            AgentProfileContextRoleKind.HERMES_REFERENCE_ROLE,
        ],
    )
    resolved_profile = resolve_agent_runtime_profile_from_input(
        resolution_input,
        boundary,
        profile_metadata={
            "display_name": "Vera",
            "description": "In-memory Vera profile with OpenCode/Hermes reference context.",
        },
    )

    assert all(getattr(preview, name) is True for name in preview.__dataclass_fields__ if name.startswith("no_"))
    assert preview.execution is False
    assert all(getattr(guarantee, name) is True for name in guarantee.__dataclass_fields__ if name.startswith("no_"))
    assert v0331_readiness_report_is_not_runtime_ready(readiness)
    assert set(DEFAULT_PROFILE_PROHIBITED_RUNTIME_ACTIONS).issubset(set(readiness.prohibited_until_later_gate))
    assert agent_runtime_profile_is_not_active_session(resolved_profile)
    assert resolved_profile.loadout.reference_context.path_refs_only is True
    assert resolved_profile.loadout.reference_context.ready_for_reference_file_access is False
    assert resolved_profile.loadout.tool_availability_view.ready_for_tool_execution is False

    with pytest.raises(ValueError):
        AgentProfileRuntimeRunPreview(
            run_preview_id="preview:bad",
            no_provider_invocation_guarantee=False,
        )
    with pytest.raises(ValueError):
        AgentProfileRuntimeNoExecutionGuarantee(
            guarantee_id="guarantee:bad",
            version="v0.33.1",
            no_reference_import=False,
        )
    for flag_name in RUNTIME_FLAG_NAMES:
        with pytest.raises(ValueError):
            V0331ReadinessReport(
                report_id=f"readiness:bad:{flag_name}",
                version="v0.33.1",
                **{flag_name: True},
            )
    with pytest.raises(ValueError):
        resolve_agent_runtime_profile_from_input(
            resolution_input,
            boundary,
            profile_metadata={"file_load": True},
        )
