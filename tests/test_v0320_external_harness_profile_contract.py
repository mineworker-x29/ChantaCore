import pytest

from chanta_core.external_harness import (
    ExternalHarnessEvidenceQuality,
    ExternalHarnessObservationBoundary,
    ExternalHarnessObservationMode,
    ExternalHarnessProfile,
    ExternalHarnessProfileKind,
    ExternalHarnessProfileNoExecutionGuarantee,
    ExternalHarnessProfileSet,
    ExternalHarnessProfileStatus,
    ExternalHarnessRiskPosture,
    ExternalHarnessRuntimeReadinessFlagSet,
    ExternalHarnessSurfaceDescriptor,
    ExternalHarnessSurfaceKind,
    build_external_harness_no_execution_guarantee,
    build_external_harness_observation_boundary,
    build_external_harness_profile,
    build_external_harness_profile_set,
    build_external_harness_runtime_readiness_flags,
    build_external_harness_surface_descriptor,
    harness_profile_preserves_no_execution,
)


def test_external_harness_taxonomies_include_required_values() -> None:
    assert {item.value for item in ExternalHarnessProfileKind} >= {
        "opencode_style",
        "openclaw_style",
        "hermes_style",
        "mcp_server_style",
        "provider_runtime_style",
        "browser_runtime_style",
        "rpa_runtime_style",
        "gateway_runtime_style",
        "generic_agent_harness",
        "unknown",
    }
    assert {item.value for item in ExternalHarnessSurfaceKind} >= {
        "file_workspace_surface",
        "tool_registry_surface",
        "plugin_surface",
        "external_plugin_surface",
        "provider_hook_surface",
        "command_execution_surface",
        "configuration_manifest_surface",
        "profile_surface",
        "memory_surface",
        "mission_surface",
        "skill_surface",
        "delegation_surface",
        "gateway_surface",
        "channel_surface",
        "approval_surface",
        "audit_surface",
        "credential_surface",
        "network_surface",
        "browser_surface",
        "rpa_surface",
        "result_envelope_surface",
        "ocel_trace_surface",
        "private_data_surface",
        "raw_output_surface",
        "unknown",
    }
    assert {item.value for item in ExternalHarnessProfileStatus} >= {
        "unknown",
        "draft",
        "profile_ready",
        "profile_ready_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {item.value for item in ExternalHarnessObservationMode} >= {
        "contract_only",
        "manual_profile",
        "reference_static_observation",
        "manifest_only_observation",
        "documentation_only_observation",
        "future_live_scan",
        "future_runtime",
        "unknown",
    }
    assert {item.value for item in ExternalHarnessRiskPosture} >= {
        "unknown",
        "low",
        "medium",
        "high",
        "critical",
        "blocked",
        "future_track",
    }
    assert {item.value for item in ExternalHarnessEvidenceQuality} >= {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_profile",
        "sufficient_for_static_observation",
        "sufficient_for_next_stage_review",
        "conflicting",
        "blocked",
    }


def test_runtime_readiness_flags_are_always_false() -> None:
    flags = build_external_harness_runtime_readiness_flags()

    assert flags.ready_for_execution is False
    assert flags.ready_for_external_harness_execution is False
    assert flags.ready_for_reference_code_execution is False
    assert flags.ready_for_live_scan is False
    assert flags.ready_for_network_access is False
    assert flags.ready_for_credential_access is False
    assert flags.ready_for_command_execution is False
    assert flags.ready_for_provider_invocation is False
    assert flags.ready_for_browser_runtime_control is False
    assert flags.ready_for_rpa_runtime_control is False
    assert flags.ready_for_gateway_control is False
    assert flags.ready_for_packet_send is False
    assert flags.ready_for_registry_mutation is False
    assert flags.ready_for_memory_mutation is False
    assert flags.ready_for_ocel_emission is False
    assert flags.ready_for_ui_runtime is False

    with pytest.raises(ValueError):
        ExternalHarnessRuntimeReadinessFlagSet(
            flag_set_id="bad-flags",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        ExternalHarnessRuntimeReadinessFlagSet(
            flag_set_id="bad-flags",
            ready_for_external_harness_execution=True,
        )
    with pytest.raises(ValueError):
        ExternalHarnessRuntimeReadinessFlagSet(
            flag_set_id="bad-flags",
            ready_for_network_access=True,
        )


def test_surface_descriptor_is_not_permission_and_requires_boundary_for_high_risk() -> None:
    descriptor = build_external_harness_surface_descriptor(
        surface_id="surface:command",
        surface_kind=ExternalHarnessSurfaceKind.COMMAND_EXECUTION_SURFACE,
        name="Command execution surface",
        description="Observed command-capable surface as a contract descriptor only.",
        risk_posture=ExternalHarnessRiskPosture.HIGH,
        evidence_quality=ExternalHarnessEvidenceQuality.SUFFICIENT_FOR_PROFILE,
        boundary_notes=["Remain prohibited until later gate."],
    )

    assert isinstance(descriptor, ExternalHarnessSurfaceDescriptor)
    assert descriptor.is_permission is False

    with pytest.raises(ValueError):
        build_external_harness_surface_descriptor(
            surface_id="surface:unsafe",
            surface_kind=ExternalHarnessSurfaceKind.NETWORK_SURFACE,
            name="Network surface",
            description="High-risk surface without boundary notes.",
            risk_posture=ExternalHarnessRiskPosture.HIGH,
        )


def test_observation_boundary_requires_static_no_runtime_limits() -> None:
    boundary = build_external_harness_observation_boundary("boundary:default")

    assert isinstance(boundary, ExternalHarnessObservationBoundary)
    assert boundary.requires_read_only is True
    assert boundary.requires_no_execution is True
    assert boundary.requires_no_network is True
    assert boundary.requires_no_credentials is True
    assert boundary.requires_no_import_runtime is True
    assert {"execution", "install", "import_runtime", "network", "credential", "command", "provider", "browser", "rpa", "gateway", "packet_send", "registry_mutation", "memory_mutation"}.issubset(
        set(boundary.prohibited_runtime_actions)
    )
    assert boundary.runtime_enforcement is False

    with pytest.raises(ValueError):
        ExternalHarnessObservationBoundary(
            boundary_id="boundary:bad",
            profile_kind=ExternalHarnessProfileKind.UNKNOWN,
            prohibited_runtime_actions=["execution"],
        )
    with pytest.raises(ValueError):
        ExternalHarnessObservationBoundary(
            boundary_id="boundary:bad",
            profile_kind=ExternalHarnessProfileKind.UNKNOWN,
            requires_no_network=False,
        )


def test_external_harness_profile_is_not_harness_execution() -> None:
    boundary = build_external_harness_observation_boundary("boundary:profile")
    descriptor = build_external_harness_surface_descriptor(
        surface_id="surface:profile",
        surface_kind=ExternalHarnessSurfaceKind.PROFILE_SURFACE,
        name="Profile surface",
        description="Static profile descriptor.",
    )
    profile = build_external_harness_profile(
        profile_id="profile:generic",
        harness_kind=ExternalHarnessProfileKind.GENERIC_AGENT_HARNESS,
        display_name="Generic harness profile",
        description="Manual external harness profile contract.",
        declared_surfaces=[descriptor],
        observation_boundaries=[boundary],
        ready_for_v0321_opencode_profile=True,
    )

    assert isinstance(profile, ExternalHarnessProfile)
    assert profile.ready_for_execution is False
    assert profile.harness_execution is False
    assert harness_profile_preserves_no_execution(profile)

    with pytest.raises(ValueError):
        build_external_harness_profile(
            profile_id="profile:future-scan",
            harness_kind=ExternalHarnessProfileKind.UNKNOWN,
            display_name="Future scan",
            description="Invalid active live scan mode.",
            observation_mode=ExternalHarnessObservationMode.FUTURE_LIVE_SCAN,
        )
    with pytest.raises(ValueError):
        ExternalHarnessProfile(
            profile_id="profile:runtime",
            harness_kind=ExternalHarnessProfileKind.UNKNOWN,
            display_name="Runtime",
            description="Invalid runtime readiness.",
            source_ref=None,
            observation_mode=ExternalHarnessObservationMode.CONTRACT_ONLY,
            declared_surfaces=[],
            observation_boundaries=[],
            runtime_readiness=build_external_harness_runtime_readiness_flags(),
            ready_for_execution=True,
        )


def test_profile_set_and_no_execution_guarantee_are_contract_only() -> None:
    profile_set = build_external_harness_profile_set("profile-set:v0.32.0")
    guarantee = build_external_harness_no_execution_guarantee()

    assert isinstance(profile_set, ExternalHarnessProfileSet)
    assert profile_set.version == "v0.32.0"
    assert profile_set.ready_for_execution is False
    assert profile_set.runtime_registry is False
    assert isinstance(guarantee, ExternalHarnessProfileNoExecutionGuarantee)
    assert guarantee.no_harness_execution is True
    assert guarantee.no_reference_code_execution is True
    assert guarantee.no_live_scan is True
    assert guarantee.no_source_ref_fetch is True
    assert guarantee.no_install is True
    assert guarantee.no_import_runtime is True
    assert guarantee.no_network_access is True
    assert guarantee.no_credential_access is True
    assert guarantee.no_command_execution is True
    assert guarantee.no_provider_invocation is True
    assert guarantee.no_browser_automation is True
    assert guarantee.no_rpa_control is True
    assert guarantee.no_gateway_control is True
    assert guarantee.no_packet_send is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_memory_mutation is True
    assert guarantee.no_ocel_emission is True

    with pytest.raises(ValueError):
        ExternalHarnessProfileNoExecutionGuarantee(
            guarantee_id="bad-guarantee",
            version="v0.32.0",
            no_command_execution=False,
        )
