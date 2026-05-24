from chanta_core.internal_provider import (
    INTERNAL_PROVIDER_ALLOWED_EFFECT_TYPES,
    INTERNAL_PROVIDER_FORBIDDEN_EFFECT_TYPES,
    INTERNAL_PROVIDER_OCEL_EVENT_TYPES,
    INTERNAL_PROVIDER_OCEL_OBJECT_TYPES,
    INTERNAL_PROVIDER_OCEL_RELATION_TYPES,
    INTERNAL_PROVIDER_TYPES,
    InternalProviderContractReportService,
    InternalProviderSafetyBoundaryService,
    InternalProviderSkillRegistryService,
)


def test_internal_provider_contract_builds_with_v0_24_0_identity():
    report = InternalProviderContractReportService().build_report()
    contract = report.contract

    assert contract.version == "v0.24.0"
    assert contract.layer == "internal_provider"
    assert contract.release_track == "Internal Provider / Local Runtime Provider"
    assert contract.status == "contract_only"
    assert report.version == "v0.24.0"
    assert report.report_status == "passed"
    assert report.ready_for_v0_24_1 is True
    assert report.ready_for_v0_25 is False
    assert report.provider_invocation_enabled is False
    assert report.local_runtime_execution_enabled is False
    assert report.local_command_execution_enabled is False
    assert report.workspace_read_execution_enabled is False
    assert report.repository_search_execution_enabled is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.24.1 Provider Registry & Capability Surface"
    assert report.limitations
    assert report.withdrawal_conditions


def test_internal_provider_skills_are_contract_only():
    contracts = InternalProviderSkillRegistryService().list_skill_contracts()
    by_id = {item["skill_id"]: item for item in contracts}

    assert by_id["skill:internal_provider_contract_view"]["implemented"] is True
    assert by_id["skill:internal_provider_contract_view"]["stub"] is False
    assert by_id["skill:internal_provider_contract_view"]["read_only"] is True
    assert by_id["skill:internal_provider_contract_view"]["contract_only"] is True
    for skill_id in [
        "skill:internal_provider_registry_view",
        "skill:internal_provider_capability_surface_view",
        "skill:workspace_read_provider_view",
        "skill:repository_search_provider_view",
        "skill:file_read_provider_view",
        "skill:ocel_inspection_provider_view",
        "skill:pig_inspection_provider_view",
        "skill:ocpx_projection_provider_view",
        "skill:local_runtime_command_candidate_create",
        "skill:local_runtime_static_safety_check",
        "skill:local_runtime_preflight_check",
        "skill:local_runtime_execution_gate",
        "skill:bounded_local_command_run",
        "skill:local_runtime_output_summarize",
        "skill:local_runtime_failure_explain",
        "skill:internal_provider_consolidation_view",
    ]:
        assert by_id[skill_id]["status"] == "contract_only"
        assert by_id[skill_id]["stub"] is True
        assert by_id[skill_id]["provider_invocation_enabled"] is False
        assert by_id[skill_id]["local_command_execution_enabled"] is False


def test_provider_types_include_required_contract_descriptors():
    contract = InternalProviderContractReportService().build_report().contract
    by_type = {item.provider_type: item for item in contract.provider_types}

    assert set(INTERNAL_PROVIDER_TYPES) <= set(by_type)
    for provider_type in INTERNAL_PROVIDER_TYPES:
        descriptor = by_type[provider_type]
        assert descriptor.implementation_status in {"contract_only", "future_track", "blocked"}
        assert descriptor.external_adapter is False
        assert descriptor.provider_api_call_required is False
        assert descriptor.external_runtime_touch_required is False
        assert descriptor.credential_materialization_required is False
        assert descriptor.allowed_effect_types
        assert descriptor.forbidden_effect_types
        assert descriptor.future_versions
    assert by_type["local_runtime_provider"].execution_capable_future is True


def test_capability_contract_requirements_are_strict():
    capability = InternalProviderContractReportService().build_report().contract.capability_contract

    assert capability.capability_id_required is True
    assert capability.provider_type_required is True
    assert capability.input_schema_required is True
    assert capability.output_schema_required is True
    assert capability.effect_type_required is True
    assert capability.permission_policy_required is True
    assert capability.ocel_mapping_required is True
    assert capability.pig_projection_required is True
    assert capability.ocpx_projection_required is True
    assert capability.safety_boundary_required is True
    assert capability.failure_explanation_required is True
    assert capability.raw_secret_output_forbidden is True
    assert capability.private_path_sanitization_required is True


def test_effect_policy_allows_only_contract_effects_and_forbids_execution_effects():
    policy = InternalProviderContractReportService().build_report().contract.effect_policy

    assert policy.allowed_effect_types_v0_24_0 == [
        "read_only_observation",
        "state_candidate_created",
        "provider_contract_declared",
    ]
    assert policy.allowed_effect_types_v0_24_0 == INTERNAL_PROVIDER_ALLOWED_EFFECT_TYPES
    for effect_type in [
        "provider_surface_declared",
        "provider_candidate_created",
        "workspace_tree_observed",
        "repository_search_performed",
        "file_excerpt_read",
        "process_state_inspected",
        "local_command_candidate_created",
        "local_runtime_static_safety_checked",
        "local_runtime_preflight_checked",
        "bounded_local_command_executed",
        "local_output_captured",
        "local_runtime_outcome_candidate_created",
    ]:
        assert effect_type in policy.future_effect_types
    for effect_type in [
        "provider_invoked",
        "workspace_file_read_executed",
        "repository_search_executed",
        "file_content_extracted",
        "local_command_executed",
        "bounded_local_command_executed",
        "unrestricted_shell_executed",
        "network_accessed",
        "package_installed",
        "destructive_command_executed",
        "external_runtime_touched",
        "external_control_dispatched",
        "credential_exposed",
        "raw_secret_output",
        "memory_mutated",
        "persona_mutated",
        "external_provider_called",
    ]:
        assert effect_type in policy.forbidden_effect_types_v0_24_0
        assert effect_type in INTERNAL_PROVIDER_FORBIDDEN_EFFECT_TYPES


def test_permission_policy_is_deny_by_default_and_execution_gated():
    policy = InternalProviderContractReportService().build_report().contract.permission_policy

    assert policy.deny_by_default is True
    assert policy.read_only_requires_policy is True
    assert policy.candidate_creation_requires_policy is True
    assert policy.execution_requires_gate is True
    assert policy.local_runtime_execution_requires_allowlist is True
    assert policy.local_runtime_execution_requires_timeout is True
    assert policy.local_runtime_execution_requires_output_cap is True
    assert policy.local_runtime_execution_requires_redaction is True
    assert policy.local_runtime_execution_requires_side_effect_scan is True
    assert policy.network_forbidden_by_default is True
    assert policy.package_install_forbidden_by_default is True
    assert policy.destructive_command_forbidden_by_default is True
    assert policy.credential_access_forbidden_by_default is True
    assert policy.secret_output_forbidden is True
    assert policy.private_path_sanitization_required is True


def test_invocation_boundary_disables_all_execution_surfaces():
    boundary = InternalProviderContractReportService().build_report().contract.invocation_boundary

    assert boundary.invocation_enabled_v0_24_0 is False
    assert boundary.workspace_read_execution_enabled_v0_24_0 is False
    assert boundary.repository_search_execution_enabled_v0_24_0 is False
    assert boundary.file_read_execution_enabled_v0_24_0 is False
    assert boundary.ocel_inspection_execution_enabled_v0_24_0 is False
    assert boundary.local_runtime_execution_enabled_v0_24_0 is False
    assert boundary.local_command_execution_enabled_v0_24_0 is False
    assert boundary.external_provider_invocation_enabled is False
    assert boundary.shell_execution_enabled is False
    assert boundary.network_enabled is False
    assert boundary.mcp_enabled is False
    assert boundary.plugin_enabled is False
    assert boundary.llm_judge_enabled is False


def test_observability_contract_requires_visibility_and_sanitization():
    contract = InternalProviderContractReportService().build_report().contract.observability_contract

    assert contract.ocel_visible is True
    assert contract.pig_visible is True
    assert contract.ocpx_visible is True
    assert contract.execution_envelope_visible is True
    assert contract.provider_invocation_must_emit_event is True
    assert contract.provider_invocation_must_record_effect_type is True
    assert contract.provider_result_must_be_sanitized is True
    assert contract.provider_failure_must_be_explainable is True
    assert contract.raw_secret_output_forbidden is True
    assert contract.private_path_sanitization_required is True
    assert contract.workbench_visible_future is True


def test_safety_boundary_counts_are_zero_and_nonzero_blocks():
    service = InternalProviderSafetyBoundaryService()
    boundary = service.build_safety_boundary()

    assert boundary.provider_invocation_count == 0
    assert boundary.workspace_file_read_execution_count == 0
    assert boundary.repository_search_execution_count == 0
    assert boundary.file_content_extraction_count == 0
    assert boundary.local_command_execution_count == 0
    assert boundary.bounded_local_command_execution_count == 0
    assert boundary.unrestricted_shell_count == 0
    assert boundary.provider_api_call_count == 0
    assert boundary.external_runtime_touch_count == 0
    assert boundary.external_dispatch_count == 0
    assert boundary.network_access_count == 0
    assert boundary.package_install_count == 0
    assert boundary.destructive_command_count == 0
    assert boundary.credential_exposure_count == 0
    assert boundary.raw_secret_output_count == 0
    assert boundary.llm_judge_count == 0
    assert boundary.external_provider_adapter_count == 0
    assert boundary.schumpeter_split_count == 0
    assert boundary.status == "passed"

    blocked = service.build_safety_boundary(["provider_invocation"])
    assert blocked.provider_invocation_count == 1
    assert blocked.status == "blocked"


def test_roadmap_boundary_points_to_v0_24_1_and_defers_future_tracks():
    boundary = InternalProviderContractReportService().build_report().contract.roadmap_boundary

    assert boundary.current_track == "v0.24.x Internal Provider / Local Runtime Provider"
    assert boundary.current_version_scope == "v0.24.0 contract_only"
    assert boundary.next_version == "v0.24.1 Provider Registry & Capability Surface"
    assert boundary.general_agent_usability_deferred_to == "v0.25.x"
    assert boundary.workspace_workbench_deferred_to == "v0.26.x"
    assert boundary.memory_continuity_deferred_to == "v0.27.x"
    assert boundary.schumpeter_split_deferred_to == "v0.28.x"
    assert boundary.external_provider_adapters_deferred_to == "v0.29.x+"
    assert boundary.growthkernel_bridge_deferred is True
    assert boundary.roadmap_status == "aligned"


def test_ocel_mapping_and_pig_ocpx_projection_exist():
    for object_type in [
        "internal_provider_contract",
        "internal_provider_type_descriptor",
        "internal_provider_capability_contract",
        "internal_provider_effect_policy",
        "internal_provider_permission_policy",
        "internal_provider_invocation_boundary",
        "internal_provider_observability_contract",
        "internal_provider_safety_boundary",
        "internal_provider_roadmap_boundary",
        "internal_provider_contract_finding",
        "internal_provider_contract_report",
        "internal_dominion_consolidation_report",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in INTERNAL_PROVIDER_OCEL_OBJECT_TYPES
    for event_type in [
        "internal_provider_contract_requested",
        "internal_provider_type_descriptors_created",
        "internal_provider_effect_policy_created",
        "internal_provider_permission_policy_created",
        "internal_provider_invocation_boundary_created",
        "internal_provider_observability_contract_created",
        "internal_provider_safety_boundary_created",
        "internal_provider_roadmap_boundary_created",
        "internal_provider_contract_report_created",
        "internal_provider_contract_blocked",
    ]:
        assert event_type in INTERNAL_PROVIDER_OCEL_EVENT_TYPES
    for relation_type in [
        "declares_internal_provider_contract",
        "declares_internal_provider_type",
        "declares_internal_provider_capability_contract",
        "declares_internal_provider_effect_policy",
        "declares_internal_provider_permission_policy",
        "declares_internal_provider_invocation_boundary",
        "declares_internal_provider_observability_contract",
        "declares_internal_provider_safety_boundary",
        "declares_internal_provider_roadmap_boundary",
        "prepares_provider_registry",
        "prepares_workspace_read_provider",
        "prepares_repository_search_provider",
        "prepares_ocel_inspection_provider",
        "prepares_local_runtime_provider",
        "defers_provider_invocation_to_later_v0_24",
        "defers_local_runtime_execution_to_later_v0_24",
        "defers_general_agent_usability_to_v0_25",
        "defers_workspace_workbench_to_v0_26",
        "defers_memory_continuity_to_v0_27",
        "defers_schumpeter_split_to_v0_28",
        "defers_external_provider_adapters_to_v0_29_plus",
        "not_provider_invoked",
        "not_local_command_executed",
        "not_external_runtime_touched",
        "not_external_provider_called",
        "prevents_credential_exposure",
        "visible_in_workbench_future",
        "recorded_in_envelope",
        "derived_from_internal_dominion_consolidation",
    ]:
        assert relation_type in INTERNAL_PROVIDER_OCEL_RELATION_TYPES

    service = InternalProviderContractReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.24.0"
    assert pig["layer"] == "internal_provider"
    assert pig["subject"] == "internal_provider_contract"
    assert "provider is not arbitrary tool execution" in pig["principles"]
    assert pig["safety_boundary"]["provider_invocation_enabled"] is False
    assert pig["safety_boundary"]["workspace_read_execution_enabled"] is False
    assert pig["safety_boundary"]["repository_search_execution_enabled"] is False
    assert pig["safety_boundary"]["local_runtime_execution_enabled"] is False
    assert pig["safety_boundary"]["local_command_execution_enabled"] is False
    assert pig["safety_boundary"]["external_provider_adapter_implemented"] is False
    assert pig["safety_boundary"]["network_enabled"] is False
    assert pig["safety_boundary"]["package_install_enabled"] is False
    assert pig["safety_boundary"]["destructive_command_enabled"] is False
    assert pig["safety_boundary"]["credential_exposed"] is False
    assert pig["safety_boundary"]["raw_secret_output"] is False
    assert pig["safety_boundary"]["schumpeter_split_introduced"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert pig["roadmap"]["v0.24"] == "Internal Provider / Local Runtime Provider"
    assert pig["roadmap"]["v0.25"] == "General Agent Usability & Tool Routing"
    assert pig["roadmap"]["v0.26"] == "Workspace Agent Workbench"
    assert pig["roadmap"]["v0.27"] == "Memory Candidate & Continuity"
    assert pig["roadmap"]["v0.28"] == "Public Alpha / Schumpeter Split Preparation"
    assert pig["roadmap"]["v0.29+"] == "External Skill / External Provider Adapters"

    assert ocpx["state"] == "internal_provider_contract_declared"
    assert ocpx["version"] == "v0.24.0"
    assert "InternalProviderContractState" in ocpx["target_read_models"]
    assert "InternalProviderTypeState" in ocpx["target_read_models"]
    assert "InternalProviderEffectPolicyState" in ocpx["target_read_models"]
    assert "InternalProviderPermissionPolicyState" in ocpx["target_read_models"]
    assert "InternalProviderInvocationBoundaryState" in ocpx["target_read_models"]
    assert "InternalProviderRoadmapBoundaryState" in ocpx["target_read_models"]
    assert ocpx["effect_types"] == [
        "read_only_observation",
        "state_candidate_created",
        "provider_contract_declared",
    ]
