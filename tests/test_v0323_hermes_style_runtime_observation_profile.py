import pytest

from chanta_core.external_harness import (
    HermesApprovalAuditBoundaryRequirement,
    HermesCapabilityKind,
    HermesConfigManifestObservation,
    HermesDelegationBoundaryObservation,
    HermesDigestionHint,
    HermesDominionHint,
    HermesEvidenceQuality,
    HermesHarnessSurfaceKind,
    HermesMemorySurfaceObservation,
    HermesMissionSurfaceObservation,
    HermesNoExecutionGuarantee,
    HermesObservationFinding,
    HermesObservationFocusKind,
    HermesObservationOutput,
    HermesObservationRunPreview,
    HermesObservationStatus,
    HermesProfileSurfaceObservation,
    HermesProviderRoutingBoundaryObservation,
    HermesReferenceSourceRef,
    HermesRiskSignal,
    HermesRiskSignalKind,
    HermesRuntimeIsolationBoundaryObservation,
    HermesSkillSurfaceObservation,
    HermesStaticObservationInput,
    HermesStyleObservationProfile,
    HermesSurfaceObservation,
    HermesToolSurfaceObservation,
    ReferenceFileInventoryEntry,
    V0323ReadinessReport,
    build_hermes_approval_audit_boundary_requirement,
    build_hermes_config_manifest_observation,
    build_hermes_delegation_boundary_observation,
    build_hermes_digestion_hint,
    build_hermes_dominion_hint,
    build_hermes_memory_surface_observation,
    build_hermes_mission_surface_observation,
    build_hermes_no_execution_guarantee,
    build_hermes_observation_finding,
    build_hermes_observation_output,
    build_hermes_observation_run_preview,
    build_hermes_profile_surface_observation,
    build_hermes_provider_routing_boundary_observation,
    build_hermes_reference_source_ref,
    build_hermes_risk_signal,
    build_hermes_runtime_isolation_boundary_observation,
    build_hermes_skill_surface_observation,
    build_hermes_static_observation_input,
    build_hermes_style_observation_profile,
    build_hermes_surface_observation,
    build_hermes_tool_surface_observation,
    build_v0323_readiness_report,
    classify_inventory_entry_as_hermes_surface,
    hermes_output_is_not_manifest_or_digestive_runtime,
    hermes_profile_preserves_no_execution,
    hermes_run_preview_preserves_no_execution,
    infer_hermes_capability_from_surface,
    infer_hermes_risk_signals_from_inventory_entry,
    v0323_readiness_report_is_not_runtime_ready,
)


def test_hermes_taxonomies_include_required_values() -> None:
    assert {item.value for item in HermesHarnessSurfaceKind} >= {
        "profile_surface",
        "memory_surface",
        "mission_surface",
        "skill_surface",
        "tool_surface",
        "delegation_surface",
        "provider_routing_surface",
        "runtime_surface",
        "container_isolation_surface",
        "authorization_surface",
        "approval_boundary_surface",
        "audit_boundary_surface",
        "configuration_manifest_surface",
        "dependency_manifest_surface",
        "result_envelope_surface",
        "ocel_trace_surface",
        "private_data_surface",
        "credential_surface",
        "network_surface",
        "command_execution_surface",
        "gateway_surface",
        "unknown",
    }
    assert {item.value for item in HermesObservationFocusKind} >= {
        "profile_model",
        "memory_model",
        "mission_model",
        "skill_model",
        "tool_model",
        "delegation_model",
        "provider_routing_model",
        "runtime_model",
        "container_isolation_boundary",
        "authorization_boundary",
        "approval_boundary",
        "audit_boundary",
        "configuration_manifest",
        "dependency_manifest",
        "result_envelope",
        "ocel_trace_relevance",
        "private_data_boundary",
        "credential_boundary",
        "network_boundary",
        "command_boundary",
        "gateway_boundary",
        "digestion_relevance",
        "dominion_relevance",
        "unknown",
    }
    assert {item.value for item in HermesCapabilityKind} >= {
        "define_profile",
        "activate_profile",
        "read_memory",
        "write_memory",
        "define_mission",
        "install_mission",
        "execute_mission",
        "define_skill",
        "register_skill",
        "execute_skill",
        "define_tool",
        "register_tool",
        "invoke_tool",
        "delegate_agent",
        "route_provider",
        "invoke_provider",
        "start_runtime",
        "start_container",
        "enforce_authorization",
        "request_approval",
        "grant_approval",
        "record_audit",
        "emit_result_envelope",
        "emit_ocel_trace",
        "access_private_data",
        "use_credential",
        "access_network",
        "execute_command",
        "unknown",
    }
    assert {item.value for item in HermesRiskSignalKind} >= {
        "profile_activation_risk",
        "memory_access_risk",
        "memory_mutation_risk",
        "mission_installation_risk",
        "mission_execution_risk",
        "skill_registration_risk",
        "skill_execution_risk",
        "tool_registration_risk",
        "tool_invocation_risk",
        "delegation_execution_risk",
        "provider_routing_risk",
        "provider_invocation_risk",
        "runtime_start_risk",
        "container_runtime_risk",
        "authorization_bypass_risk",
        "approval_bypass_risk",
        "audit_gap_risk",
        "private_data_exposure_risk",
        "credential_access_risk",
        "network_access_risk",
        "command_execution_risk",
        "gateway_control_risk",
        "raw_output_persistence_risk",
        "ocel_emission_risk",
        "unknown",
    }
    assert {item.value for item in HermesObservationStatus} >= {
        "unknown",
        "draft",
        "observed",
        "observed_with_gaps",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert {item.value for item in HermesEvidenceQuality} >= {
        "unknown",
        "none",
        "weak",
        "partial",
        "sufficient_for_static_observation",
        "sufficient_for_profile",
        "sufficient_for_manifest_extraction_review",
        "conflicting",
        "blocked",
    }


def test_reference_source_ref_is_path_reference_only() -> None:
    source_ref = build_hermes_reference_source_ref(
        source_ref_id="hermes-ref:1",
        reference_source_id="source:hermes",
        reference_inventory_id="inventory:hermes",
        reference_entry_ids=["entry:profile"],
        local_path_ref="references/Hermes",
    )

    assert isinstance(source_ref, HermesReferenceSourceRef)
    assert source_ref.source_fetch is False
    assert source_ref.execution is False

    with pytest.raises(ValueError):
        HermesReferenceSourceRef(source_ref_id="bad", source_label="")
    with pytest.raises(ValueError):
        HermesReferenceSourceRef(source_ref_id="bad", metadata={"execution": True})


def test_surface_observation_requires_boundaries_for_high_risk_capabilities() -> None:
    observation = build_hermes_surface_observation(
        observation_id="surface:memory",
        surface_kind=HermesHarnessSurfaceKind.MEMORY_SURFACE,
        focus_kind=HermesObservationFocusKind.MEMORY_MODEL,
        capability_kind=HermesCapabilityKind.READ_MEMORY,
        title="Memory risk surface",
        summary="Memory surface is observed as risk only.",
        risk_signal_kinds=[HermesRiskSignalKind.MEMORY_ACCESS_RISK],
    )

    assert isinstance(observation, HermesSurfaceObservation)
    assert observation.permission is False
    assert "memory access" in observation.prohibited_runtime_actions

    with pytest.raises(ValueError):
        HermesSurfaceObservation(
            observation_id="surface:bad",
            surface_kind=HermesHarnessSurfaceKind.TOOL_SURFACE,
            focus_kind=HermesObservationFocusKind.TOOL_MODEL,
            capability_kind=HermesCapabilityKind.INVOKE_TOOL,
            title="Tool",
            summary="Missing prohibited runtime actions.",
        )


def test_profile_memory_mission_skill_tool_delegation_provider_runtime_approval_and_config_are_non_runtime() -> None:
    profile = build_hermes_profile_surface_observation(
        "profile:obs",
        possible_profile_paths=["profiles/default.json"],
        profile_activation_risk_detected=True,
    )
    memory = build_hermes_memory_surface_observation(
        "memory:obs",
        possible_memory_schema_paths=["memory/schema.json"],
        possible_memory_writer_paths=["memory/writer.py"],
        memory_access_risk_detected=True,
    )
    mission = build_hermes_mission_surface_observation(
        "mission:obs",
        possible_mission_manifest_paths=["missions/mission.json"],
        mission_execution_risk_detected=True,
    )
    skill = build_hermes_skill_surface_observation(
        "skill:obs",
        possible_skill_manifest_paths=["skills/skill.json"],
        skill_execution_risk_detected=True,
    )
    tool = build_hermes_tool_surface_observation(
        "tool:obs",
        possible_tool_manifest_paths=["tools/tool.json"],
        tool_invocation_risk_detected=True,
    )
    delegation = build_hermes_delegation_boundary_observation(
        "delegation:boundary",
        possible_agent_route_paths=["delegation/agents.json"],
        delegation_execution_risk_detected=True,
    )
    provider = build_hermes_provider_routing_boundary_observation(
        "provider:boundary",
        possible_provider_router_paths=["providers/router.json"],
        provider_invocation_risk_detected=True,
    )
    runtime = build_hermes_runtime_isolation_boundary_observation(
        "runtime:boundary",
        possible_container_paths=["Dockerfile"],
        runtime_start_risk_detected=True,
    )
    approval = build_hermes_approval_audit_boundary_requirement(
        "approval-audit:boundary",
        approval_required_for_surfaces=[HermesHarnessSurfaceKind.TOOL_SURFACE],
        approval_gap_detected=True,
    )
    config = build_hermes_config_manifest_observation(
        "config:obs",
        possible_package_manifest_paths=["package.json"],
        possible_profile_manifest_paths=["profiles/default.json"],
        possible_script_entries=["run"],
    )

    assert isinstance(profile, HermesProfileSurfaceObservation)
    assert profile.ready_for_profile_activation is False
    assert profile.ready_for_private_data_access is False
    assert profile.profile_activation is False
    assert isinstance(memory, HermesMemorySurfaceObservation)
    assert memory.ready_for_memory_access is False
    assert memory.ready_for_memory_write is False
    assert memory.ready_for_memory_mutation is False
    assert memory.memory_access_or_mutation is False
    assert isinstance(mission, HermesMissionSurfaceObservation)
    assert mission.ready_for_mission_installation is False
    assert mission.ready_for_mission_execution is False
    assert mission.mission_install_or_execution is False
    assert isinstance(skill, HermesSkillSurfaceObservation)
    assert skill.ready_for_skill_registration is False
    assert skill.ready_for_skill_execution is False
    assert skill.skill_registration_or_execution is False
    assert isinstance(tool, HermesToolSurfaceObservation)
    assert tool.ready_for_tool_registration is False
    assert tool.ready_for_tool_invocation is False
    assert tool.ready_for_command_execution is False
    assert tool.tool_registration_or_invocation is False
    assert isinstance(delegation, HermesDelegationBoundaryObservation)
    assert delegation.ready_for_delegation_execution is False
    assert delegation.ready_for_external_agent_runtime is False
    assert delegation.delegation_execution is False
    assert isinstance(provider, HermesProviderRoutingBoundaryObservation)
    assert provider.ready_for_provider_routing is False
    assert provider.ready_for_provider_invocation is False
    assert provider.ready_for_network_access is False
    assert provider.ready_for_credential_access is False
    assert provider.provider_invocation is False
    assert isinstance(runtime, HermesRuntimeIsolationBoundaryObservation)
    assert runtime.ready_for_hermes_runtime is False
    assert runtime.ready_for_container_runtime is False
    assert runtime.ready_for_command_execution is False
    assert runtime.runtime_or_container_start is False
    assert isinstance(approval, HermesApprovalAuditBoundaryRequirement)
    assert approval.approval_granted is False
    assert approval.ready_for_approval_execution is False
    assert approval.approval_or_audit_execution is False
    assert isinstance(config, HermesConfigManifestObservation)
    assert config.ready_for_dependency_install is False
    assert config.ready_for_script_execution is False
    assert config.dependency_install is False

    with pytest.raises(ValueError):
        HermesProfileSurfaceObservation(profile_observation_id="bad", ready_for_profile_activation=True)
    with pytest.raises(ValueError):
        HermesMemorySurfaceObservation(memory_observation_id="bad", ready_for_memory_access=True)
    with pytest.raises(ValueError):
        HermesMissionSurfaceObservation(mission_observation_id="bad", ready_for_mission_execution=True)
    with pytest.raises(ValueError):
        HermesSkillSurfaceObservation(skill_observation_id="bad", ready_for_skill_execution=True)
    with pytest.raises(ValueError):
        HermesToolSurfaceObservation(tool_observation_id="bad", ready_for_tool_invocation=True)
    with pytest.raises(ValueError):
        HermesDelegationBoundaryObservation(delegation_boundary_id="bad", ready_for_delegation_execution=True)
    with pytest.raises(ValueError):
        HermesProviderRoutingBoundaryObservation(provider_routing_boundary_id="bad", ready_for_provider_invocation=True)
    with pytest.raises(ValueError):
        HermesRuntimeIsolationBoundaryObservation(runtime_isolation_boundary_id="bad", ready_for_hermes_runtime=True)
    with pytest.raises(ValueError):
        HermesApprovalAuditBoundaryRequirement(approval_audit_boundary_id="bad", approval_granted=True)


def test_input_finding_risk_and_hints_are_signals_only() -> None:
    static_input = build_hermes_static_observation_input(
        "hermes-input:1",
        requested_focus=[HermesObservationFocusKind.MEMORY_MODEL],
    )
    finding = build_hermes_observation_finding(
        finding_id="finding:1",
        hermes_input_id=static_input.hermes_input_id,
        surface_kind=HermesHarnessSurfaceKind.MEMORY_SURFACE,
        capability_kind=HermesCapabilityKind.READ_MEMORY,
        summary="Memory surface appears in static inventory.",
        digestion_relevance=True,
        dominion_relevance=True,
    )
    risk = build_hermes_risk_signal(
        risk_signal_id="risk:1",
        finding_id=finding.finding_id,
        signal_kind=HermesRiskSignalKind.MEMORY_ACCESS_RISK,
        severity="critical",
        summary="Memory access risk remains prohibited.",
        recommended_boundary="No memory access until later gate.",
    )
    digestion = build_hermes_digestion_hint(
        digestion_hint_id="digestion:1",
        finding_ids=[finding.finding_id],
        candidate_focus=HermesObservationFocusKind.MEMORY_MODEL,
        summary="Static digestion relevance only.",
    )
    dominion = build_hermes_dominion_hint(
        dominion_hint_id="dominion:1",
        finding_ids=[finding.finding_id],
        risk_signal_ids=[risk.risk_signal_id],
        suggested_boundary="Keep runtime and memory access prohibited.",
        summary="Dominion boundary hint only.",
    )

    assert isinstance(static_input, HermesStaticObservationInput)
    assert static_input.execution_request is False
    assert "Hermes execution" in static_input.prohibited_runtime_actions
    assert "Hermes runtime start" in static_input.prohibited_runtime_actions
    assert isinstance(finding, HermesObservationFinding)
    assert finding.digestion_candidate is False
    assert finding.dominion_target is False
    assert isinstance(risk, HermesRiskSignal)
    assert risk.authority_grant is False
    assert isinstance(digestion, HermesDigestionHint)
    assert digestion.ready_for_internal_candidate_creation is False
    assert digestion.internal_skill_candidate is False
    assert isinstance(dominion, HermesDominionHint)
    assert dominion.ready_for_dominion_target_creation is False
    assert dominion.ready_for_external_control is False
    assert dominion.dominion_target is False

    with pytest.raises(ValueError):
        build_hermes_risk_signal(
            risk_signal_id="risk:bad",
            finding_id=None,
            signal_kind=HermesRiskSignalKind.PROVIDER_INVOCATION_RISK,
            severity="high",
            summary="Missing conservative route.",
        )
    with pytest.raises(ValueError):
        HermesDigestionHint(
            digestion_hint_id="digestion:bad",
            finding_ids=[],
            candidate_focus=HermesObservationFocusKind.DIGESTION_RELEVANCE,
            suggested_internal_candidate_kind=None,
            summary="Bad readiness.",
            ready_for_internal_candidate_creation=True,
        )
    with pytest.raises(ValueError):
        HermesDominionHint(
            dominion_hint_id="dominion:bad",
            finding_ids=[],
            risk_signal_ids=[],
            suggested_boundary="Boundary",
            summary="Bad readiness.",
            ready_for_dominion_target_creation=True,
        )


def test_profile_output_preview_guarantee_and_readiness_are_non_runtime() -> None:
    profile = build_hermes_style_observation_profile(
        hermes_profile_id="hermes-profile:1",
        display_name="Hermes-style profile",
        description="Static Hermes-style runtime/profile observation profile.",
    )
    output = build_hermes_observation_output(
        hermes_output_id="hermes-output:1",
        hermes_input_id="hermes-input:1",
        hermes_profile=profile,
    )
    preview = build_hermes_observation_run_preview(
        planned_steps=["Build static observations from inventory metadata."],
        expected_artifacts=["HermesObservationOutput"],
        explicitly_not_performed=["Hermes execution", "Hermes runtime start", "memory access"],
    )
    guarantee = build_hermes_no_execution_guarantee()
    report = build_v0323_readiness_report(
        hermes_profile_id=profile.hermes_profile_id,
        hermes_output_id=output.hermes_output_id,
    )

    assert isinstance(profile, HermesStyleObservationProfile)
    assert hermes_profile_preserves_no_execution(profile)
    assert isinstance(output, HermesObservationOutput)
    assert hermes_output_is_not_manifest_or_digestive_runtime(output)
    assert isinstance(preview, HermesObservationRunPreview)
    assert hermes_run_preview_preserves_no_execution(preview)
    assert isinstance(guarantee, HermesNoExecutionGuarantee)
    assert guarantee.no_hermes_execution is True
    assert guarantee.no_hermes_runtime_start is True
    assert guarantee.no_reference_code_execution is True
    assert guarantee.no_dependency_install is True
    assert guarantee.no_import_runtime is True
    assert guarantee.no_profile_activation is True
    assert guarantee.no_memory_access is True
    assert guarantee.no_memory_write is True
    assert guarantee.no_memory_mutation is True
    assert guarantee.no_mission_installation is True
    assert guarantee.no_mission_execution is True
    assert guarantee.no_skill_registration is True
    assert guarantee.no_skill_execution is True
    assert guarantee.no_tool_registration is True
    assert guarantee.no_tool_invocation is True
    assert guarantee.no_delegation_execution is True
    assert guarantee.no_provider_routing is True
    assert guarantee.no_provider_invocation is True
    assert guarantee.no_container_runtime is True
    assert guarantee.no_approval_execution is True
    assert guarantee.no_network_access is True
    assert guarantee.no_credential_access is True
    assert guarantee.no_secret_file_read is True
    assert guarantee.no_command_execution is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_ocel_emission is True
    assert isinstance(report, V0323ReadinessReport)
    assert v0323_readiness_report_is_not_runtime_ready(report)
    assert {"Hermes execution", "Hermes runtime start", "reference code execution", "install", "import runtime", "profile activation", "memory access", "memory write", "mission installation", "mission execution", "skill registration", "skill execution", "tool registration", "tool invocation", "delegation execution", "provider routing", "provider invocation", "container runtime", "approval execution", "network", "credential", "secret file read", "command", "registry mutation", "OCEL emission"}.issubset(set(report.prohibited_until_later_gate))

    with pytest.raises(ValueError):
        HermesStyleObservationProfile(
            hermes_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_execution=True,
        )
    with pytest.raises(ValueError):
        HermesStyleObservationProfile(
            hermes_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_hermes_execution=True,
        )
    with pytest.raises(ValueError):
        HermesStyleObservationProfile(
            hermes_profile_id="profile:bad",
            base_harness_profile_id=None,
            display_name="Bad",
            description="Bad runtime flag.",
            ready_for_hermes_runtime=True,
        )
    with pytest.raises(ValueError):
        V0323ReadinessReport(
            report_id="report:bad",
            version="v0.32.3",
            hermes_profile_id=None,
            hermes_output_id=None,
            summary="Bad readiness.",
            ready_for_memory_access=True,
        )


def test_inventory_metadata_classification_is_static_and_non_executing(tmp_path) -> None:
    fake_root = tmp_path / "references" / "Hermes"
    profile_entry = ReferenceFileInventoryEntry(
        entry_id="entry:profile",
        source_id="source:hermes",
        relative_path="profiles/default.json",
        file_name="default.json",
        file_extension=".json",
        detected_kind="manifest_candidate",
        metadata={"local_path_ref": str(fake_root)},
    )
    memory_entry = ReferenceFileInventoryEntry(
        entry_id="entry:memory",
        source_id="source:hermes",
        relative_path="memory/store/schema.json",
        file_name="schema.json",
        file_extension=".json",
    )
    provider_entry = ReferenceFileInventoryEntry(
        entry_id="entry:provider",
        source_id="source:hermes",
        relative_path="providers/router.json",
        file_name="router.json",
        file_extension=".json",
    )
    container_entry = ReferenceFileInventoryEntry(
        entry_id="entry:container",
        source_id="source:hermes",
        relative_path="runtime/Dockerfile",
        file_name="Dockerfile",
        file_extension=None,
    )

    profile_surface = classify_inventory_entry_as_hermes_surface(profile_entry)
    memory_surface = classify_inventory_entry_as_hermes_surface(memory_entry)
    provider_surface = classify_inventory_entry_as_hermes_surface(provider_entry)
    container_surface = classify_inventory_entry_as_hermes_surface(container_entry)

    assert profile_surface == HermesHarnessSurfaceKind.PROFILE_SURFACE
    assert infer_hermes_capability_from_surface(profile_surface) == HermesCapabilityKind.DEFINE_PROFILE
    assert HermesRiskSignalKind.PROFILE_ACTIVATION_RISK in infer_hermes_risk_signals_from_inventory_entry(profile_entry)
    assert memory_surface == HermesHarnessSurfaceKind.MEMORY_SURFACE
    assert HermesRiskSignalKind.MEMORY_ACCESS_RISK in infer_hermes_risk_signals_from_inventory_entry(memory_entry)
    assert provider_surface == HermesHarnessSurfaceKind.PROVIDER_ROUTING_SURFACE
    assert HermesRiskSignalKind.PROVIDER_INVOCATION_RISK in infer_hermes_risk_signals_from_inventory_entry(provider_entry)
    assert container_surface == HermesHarnessSurfaceKind.CONTAINER_ISOLATION_SURFACE
    assert HermesRiskSignalKind.CONTAINER_RUNTIME_RISK in infer_hermes_risk_signals_from_inventory_entry(container_entry)
