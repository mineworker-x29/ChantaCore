from chanta_core.agent_surface import (
    AGENT_SURFACE_CONTRACT_EFFECT_TYPES,
    AGENT_SURFACE_CONTRACT_EVENT_TYPES,
    AGENT_SURFACE_CONTRACT_OBJECT_TYPES,
    AgentReferenceArchitecturePolicy,
    AgentSurfaceContract,
    AgentSurfaceContractReport,
    AgentSurfaceContractReportService,
    AgentSurfaceEffectPolicy,
    AgentSurfaceEvidencePolicy,
    AgentSurfaceModeDescriptor,
    AgentSurfaceObservabilityContract,
    AgentSurfaceOutcomePolicy,
    AgentSurfacePermissionPolicy,
    AgentSurfacePrerequisiteSourceService,
    AgentSurfaceRoadmapBoundary,
    AgentSurfaceRoutingBoundary,
    AgentSurfaceSafetyBoundary,
)
from chanta_core.cli.main import main


def test_prerequisite_sources_are_read_only_metadata_refs() -> None:
    sources = AgentSurfacePrerequisiteSourceService().load_all_sources()

    assert "v0.24.9_consolidation" in sources
    assert "v0.24.9_v025_readiness" in sources
    assert all(source["read_only"] is True for source in sources.values())
    assert all(source["new_provider_invocation_performed"] is False for source in sources.values())
    assert all(source["new_local_command_executed"] is False for source in sources.values())
    assert all(source["credential_read_performed"] is False for source in sources.values())


def test_agent_surface_contract_builds_with_required_sections() -> None:
    parts = AgentSurfaceContractReportService().build_all_parts()
    contract = parts["contract"]
    mode_names = {mode.mode_name for mode in contract.surface_modes}

    assert isinstance(contract, AgentSurfaceContract)
    assert contract.version == "v0.25.0"
    assert contract.layer == "agent_surface"
    assert contract.status == "contract_only"
    assert {
        "contract_view",
        "single_turn_ask_future",
        "repl_future",
        "provider_routing_future",
        "diagnostic_future",
        "read_only_answer_future",
        "bounded_execution_future",
        "blocked",
        "unknown",
    }.issubset(mode_names)
    assert all(isinstance(mode, AgentSurfaceModeDescriptor) for mode in contract.surface_modes)
    assert all(mode.memory_capable_future is False for mode in contract.surface_modes)
    assert all(mode.external_adapter_capable_future is False for mode in contract.surface_modes)


def test_request_and_response_envelope_contracts_build() -> None:
    contract = AgentSurfaceContractReportService().build_report().contract
    request = contract.request_envelope_contract
    response = contract.response_envelope_contract

    assert request.user_request_required is True
    assert request.request_id_required is True
    assert request.surface_mode_required is True
    assert request.raw_secret_input_storage_forbidden is True
    assert request.persistent_memory_write_forbidden is True
    assert request.persona_mutation_forbidden is True
    assert response.response_id_required is True
    assert response.request_ref_required is True
    assert response.outcome_required is True
    assert response.evidence_bundle_required_if_provider_used is True
    assert response.no_action_rationale_required is True
    assert response.blocked_rationale_required is True
    assert response.raw_secret_output_forbidden is True
    assert response.final_conclusion_once is True


def test_outcome_permission_effect_and_routing_policies_build() -> None:
    contract = AgentSurfaceContractReportService().build_report().contract
    outcome = contract.outcome_policy
    permission = contract.permission_policy
    effect = contract.effect_policy
    routing = contract.routing_boundary

    assert isinstance(outcome, AgentSurfaceOutcomePolicy)
    assert {"answered", "routed_future", "needs_more_input", "clarification_requested", "no_action", "blocked", "deferred", "failed"}.issubset(outcome.allowed_outcomes)
    assert outcome.no_action_is_valid is True
    assert outcome.clarification_is_valid is True
    assert outcome.local_runtime_execution_requires_v0_24_gate is True
    assert isinstance(permission, AgentSurfacePermissionPolicy)
    assert permission.deny_by_default is True
    assert permission.user_request_not_permission is True
    assert permission.local_runtime_execution_requires_single_use_authorization is True
    assert permission.external_provider_adapter_forbidden is True
    assert permission.external_agent_adapter_forbidden is True
    assert permission.memory_promotion_forbidden is True
    assert permission.persona_mutation_forbidden is True
    assert permission.llm_safety_judge_forbidden is True
    assert isinstance(effect, AgentSurfaceEffectPolicy)
    assert effect.allowed_effect_types_v0_25_0 == ["read_only_observation", "state_candidate_created", "agent_surface_contract_declared"]
    assert "agent_ask_executed" in effect.forbidden_effect_types_v0_25_0
    assert "agent_repl_started" in effect.forbidden_effect_types_v0_25_0
    assert "tool_route_executed" in effect.forbidden_effect_types_v0_25_0
    assert "provider_invoked" in effect.forbidden_effect_types_v0_25_0
    assert "local_command_executed" in effect.forbidden_effect_types_v0_25_0
    assert isinstance(routing, AgentSurfaceRoutingBoundary)
    assert routing.route_plan_enabled_v0_25_0 is False
    assert routing.provider_invocation_enabled_v0_25_0 is False
    assert routing.local_runtime_execution_enabled_v0_25_0 is False
    assert routing.ask_enabled_v0_25_0 is False
    assert routing.repl_enabled_v0_25_0 is False
    assert routing.direct_tool_call_forbidden is True
    assert routing.no_provider_boundary_bypass is True


def test_evidence_observability_safety_roadmap_and_reference_policy_build() -> None:
    contract = AgentSurfaceContractReportService().build_report().contract
    evidence = contract.evidence_policy
    observability = contract.observability_contract
    safety = contract.safety_boundary
    roadmap = contract.roadmap_boundary
    reference = contract.reference_architecture_policy

    assert isinstance(evidence, AgentSurfaceEvidencePolicy)
    assert evidence.evidence_required_for_provider_outputs is True
    assert evidence.fact_inference_uncertainty_separation_required is True
    assert evidence.raw_provider_output_dump_forbidden is True
    assert evidence.raw_secret_output_forbidden is True
    assert isinstance(observability, AgentSurfaceObservabilityContract)
    assert observability.ocel_visible is True
    assert observability.pig_visible is True
    assert observability.ocpx_visible is True
    assert observability.execution_envelope_visible is True
    assert observability.no_action_must_be_recorded is True
    assert isinstance(safety, AgentSurfaceSafetyBoundary)
    assert safety.status == "passed"
    assert safety.agent_ask_execution_count == 0
    assert safety.agent_repl_execution_count == 0
    assert safety.tool_route_execution_count == 0
    assert safety.provider_invocation_count == 0
    assert safety.local_command_execution_count == 0
    assert safety.memory_promotion_count == 0
    assert safety.credential_exposure_count == 0
    assert safety.llm_judge_for_safety_count == 0
    assert isinstance(roadmap, AgentSurfaceRoadmapBoundary)
    assert roadmap.next_version == "v0.25.1 Turn Envelope & Interaction Context"
    assert roadmap.workspace_workbench_deferred_to == "v0.26.x"
    assert roadmap.memory_continuity_deferred_to == "v0.27.x"
    assert roadmap.external_provider_adapters_deferred_to == "v0.29.x+"
    assert roadmap.external_agent_dominion_deferred_to == "v0.30.x+"
    assert isinstance(reference, AgentReferenceArchitecturePolicy)
    assert reference.direct_implementation_strategy is True
    assert reference.architecture_pattern_absorption_allowed is True
    assert reference.opencode_reference_allowed is True
    assert reference.openclaw_reference_allowed is True
    assert reference.hermes_reference_allowed is True
    assert reference.opencode_runtime_dependency_allowed is False
    assert reference.openclaw_runtime_dependency_allowed is False
    assert reference.hermes_runtime_dependency_allowed is False
    assert reference.external_agent_runtime_control_allowed is False


def test_contract_report_pig_ocpx_and_cli_build() -> None:
    service = AgentSurfaceContractReportService()
    report = service.build_report()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert isinstance(report, AgentSurfaceContractReport)
    assert report.report_status == "passed"
    assert report.ready_for_v0_25_1 is True
    assert report.ready_for_v0_26 is False
    assert report.agent_ask_enabled is False
    assert report.agent_repl_enabled is False
    assert report.tool_route_execution_enabled is False
    assert report.provider_invocation_enabled is False
    assert report.local_runtime_execution_enabled is False
    assert report.external_provider_adapter_implemented is False
    assert report.external_agent_adapter_implemented is False
    assert report.memory_continuity_implemented is False
    assert report.workspace_workbench_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert "agent_surface_contract" in AGENT_SURFACE_CONTRACT_OBJECT_TYPES
    assert "agent_surface_contract_report_created" in AGENT_SURFACE_CONTRACT_EVENT_TYPES
    assert AGENT_SURFACE_CONTRACT_EFFECT_TYPES == ["read_only_observation", "state_candidate_created", "agent_surface_contract_declared"]
    assert pig["version"] == "v0.25.0"
    assert pig["layer"] == "agent_surface"
    assert pig["subject"] == "agent_surface_contract"
    assert pig["safety_boundary"]["agent_ask_enabled"] is False
    assert pig["safety_boundary"]["provider_invocation_enabled"] is False
    assert ocpx["state"] == "agent_surface_contract_declared"
    assert "AgentSurfaceContractState" in ocpx["target_read_models"]
    assert main(["agent", "contract"]) == 0
    assert main(["agent", "modes"]) == 0
    assert main(["agent", "reference-architecture"]) == 0
