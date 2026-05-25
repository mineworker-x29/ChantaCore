from chanta_core.internal_provider import (
    INTERNAL_PROVIDER_REGISTRY_ALLOWED_EFFECT_TYPES,
    INTERNAL_PROVIDER_REGISTRY_OCEL_EVENT_TYPES,
    INTERNAL_PROVIDER_REGISTRY_OCEL_OBJECT_TYPES,
    INTERNAL_PROVIDER_REGISTRY_OCEL_RELATION_TYPES,
    InternalProviderRegistryReportService,
    InternalProviderRegistrySkillService,
)


REQUIRED_PROVIDERS = {
    "workspace_read_provider",
    "repository_search_provider",
    "file_read_provider",
    "ocel_inspection_provider",
    "pig_inspection_provider",
    "ocpx_projection_provider",
    "local_runtime_provider",
    "diagnostic_provider",
    "candidate_generation_provider",
}


REQUIRED_CAPABILITIES = {
    "workspace_read_provider": {
        "capability:list_workspace_roots",
        "capability:describe_workspace",
        "capability:read_workspace_tree_future",
        "capability:list_file_metadata_future",
    },
    "repository_search_provider": {
        "capability:search_file_names_future",
        "capability:search_text_future",
        "capability:search_symbols_future",
        "capability:rank_repository_matches_future",
    },
    "file_read_provider": {
        "capability:read_file_excerpt_future",
        "capability:read_bounded_file_future",
        "capability:sanitize_file_excerpt_future",
    },
    "ocel_inspection_provider": {
        "capability:list_ocel_event_types_future",
        "capability:list_ocel_object_types_future",
        "capability:inspect_recent_ocel_events_future",
        "capability:inspect_object_trace_future",
    },
    "pig_inspection_provider": {
        "capability:list_pig_reports_future",
        "capability:view_pig_report_future",
    },
    "ocpx_projection_provider": {
        "capability:list_ocpx_projections_future",
        "capability:view_ocpx_projection_future",
    },
    "local_runtime_provider": {
        "capability:create_local_command_candidate_future",
        "capability:check_local_runtime_static_safety_future",
        "capability:check_local_runtime_preflight_future",
        "capability:gated_bounded_local_command_run_future",
    },
    "diagnostic_provider": {
        "capability:create_diagnostic_candidate_future",
        "capability:summarize_diagnostic_result_future",
    },
    "candidate_generation_provider": {
        "capability:create_patch_candidate_future",
        "capability:create_action_candidate_future",
        "capability:create_next_step_candidate_future",
    },
}


def test_internal_provider_registry_report_builds_with_v0_24_1_identity():
    report = InternalProviderRegistryReportService().build_report()

    assert report.version == "v0.24.1"
    assert report.report_status == "passed"
    assert report.ready_for_v0_24_2 is True
    assert report.ready_for_v0_25 is False
    assert report.next_required_step == "v0.24.2 Read-only Workspace Provider"
    assert report.provider_invocation_enabled is False
    assert report.workspace_read_execution_enabled is False
    assert report.repository_search_execution_enabled is False
    assert report.file_read_execution_enabled is False
    assert report.local_runtime_execution_enabled is False
    assert report.local_command_execution_enabled is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.limitations
    assert report.withdrawal_conditions


def test_internal_provider_registry_skills_are_implemented_or_stubbed():
    skills = {item["skill_id"]: item for item in InternalProviderRegistrySkillService().list_skill_contracts()}

    assert skills["skill:internal_provider_contract_view"]["implemented"] is True
    assert skills["skill:internal_provider_registry_view"]["implemented"] is True
    assert skills["skill:internal_provider_registry_view"]["registry_only"] is True
    assert skills["skill:internal_provider_capability_surface_view"]["implemented"] is True
    assert skills["skill:internal_provider_capability_surface_view"]["surface_only"] is True
    for skill_id in [
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
        assert skills[skill_id]["status"] == "contract_only"
        assert skills[skill_id]["stub"] is True
        assert skills[skill_id]["provider_invocation_enabled"] is False
        assert skills[skill_id]["local_command_execution_enabled"] is False


def test_required_provider_refs_are_registered_with_disabled_execution():
    registry = InternalProviderRegistryReportService().build_report().registry
    by_type = {ref.provider_type: ref for ref in registry.provider_refs}

    assert set(by_type) == REQUIRED_PROVIDERS
    for provider_type, ref in by_type.items():
        assert ref.provider_id == f"internal_provider:{provider_type}"
        assert ref.implementation_status in {"declared", "contract_only", "future_track", "disabled", "blocked"}
        assert ref.activation_version
        assert ref.provider_invocation_enabled is False
        assert ref.provider_api_call_enabled is False
        assert ref.external_runtime_touch_enabled is False
        assert ref.local_command_execution_enabled is False
        assert ref.workspace_file_read_execution_enabled is False
        assert ref.repository_search_execution_enabled is False
        assert ref.credential_materialization_enabled is False
        assert ref.external_adapter is False
        assert ref.public_core_safe is True


def test_required_capability_surfaces_and_minimum_capabilities_are_declared():
    registry = InternalProviderRegistryReportService().build_report().registry
    surfaces = {surface.provider_type: surface for surface in registry.capability_surfaces}

    assert set(surfaces) == REQUIRED_PROVIDERS
    for provider_type, required_capabilities in REQUIRED_CAPABILITIES.items():
        surface = surfaces[provider_type]
        capability_ids = {capability.capability_id for capability in surface.capabilities}
        assert required_capabilities <= capability_ids
        assert surface.invocation_enabled is False
        assert surface.execution_enabled is False
        assert surface.read_execution_enabled is False
        assert surface.local_command_execution_enabled is False
        assert surface.external_provider_invocation_enabled is False
        assert surface.credential_materialization_enabled is False
        assert surface.ocel_visible is True
        assert surface.pig_visible is True
        assert surface.ocpx_visible is True


def test_capability_descriptors_are_complete_and_non_invoking():
    registry = InternalProviderRegistryReportService().build_report().registry

    for surface in registry.capability_surfaces:
        for capability in surface.capabilities:
            assert capability.capability_id
            assert capability.provider_id
            assert capability.provider_type
            assert capability.capability_category
            assert capability.introduced_in == "v0.24.1"
            assert capability.activation_version
            assert capability.implementation_status in {"declared", "contract_only", "future_track", "disabled", "blocked"}
            assert capability.input_schema_ref
            assert capability.output_schema_ref
            assert capability.required_permission_policy_ref
            assert capability.required_effect_type == "provider_surface_declared"
            assert capability.allowed_effect_types == INTERNAL_PROVIDER_REGISTRY_ALLOWED_EFFECT_TYPES
            assert capability.forbidden_effect_types
            assert capability.ocel_object_types
            assert capability.ocel_event_types
            assert capability.ocel_relation_types
            assert capability.invocation_enabled is False
            assert capability.raw_secret_output_forbidden is True


def test_registry_status_snapshot_and_surface_report_counts():
    service = InternalProviderRegistryReportService()
    report = service.build_report()
    registry = report.registry
    snapshot = report.snapshot
    surface_report = service.build_surface_report(registry)

    assert registry.provider_count == 9
    assert registry.capability_count == 28
    assert registry.invocation_enabled is False
    assert registry.execution_enabled is False
    assert registry.external_adapter_count == 0
    assert registry.public_core_safe is True
    assert len(registry.provider_statuses) == registry.provider_count
    for status in registry.provider_statuses:
        assert status.registry_ready is True
        assert status.capability_surface_ready is True
        assert status.invocation_ready is False
        assert status.execution_ready is False

    assert snapshot.provider_count == 9
    assert snapshot.capability_surface_count == 9
    assert snapshot.capability_count == 28
    assert snapshot.invocation_enabled_count == 0
    assert snapshot.execution_enabled_count == 0
    assert snapshot.external_adapter_count == 0

    assert surface_report.capability_count == 28
    assert surface_report.invocation_enabled_count == 0
    assert surface_report.future_execution_capability_count == 4
    assert surface_report.report_status == "passed"


def test_registry_findings_cover_blocking_and_missing_conditions():
    service = InternalProviderRegistryReportService()

    markers = [
        "missing_provider_contract",
        "missing_provider_type",
        "missing_provider_ref",
        "missing_capability_surface",
        "missing_capability_descriptor",
        "provider_invocation_enabled",
        "workspace_read_execution_enabled",
        "repository_search_execution_enabled",
        "file_read_execution_enabled",
        "local_command_execution_enabled",
        "local_runtime_execution_enabled",
        "external_adapter",
        "vendor_hardcoding",
        "credential_materialization",
        "raw_secret_output",
        "missing_ocel_mapping",
        "missing_permission_policy_ref",
        "growthkernel_dependency",
        "schumpeter_split",
        "general_agent_usability",
        "llm_judge",
    ]
    report = service.build_report(markers=markers)
    finding_types = {finding.finding_type for finding in report.findings}

    for finding_type in [
        "missing_provider_contract",
        "missing_provider_type",
        "missing_provider_ref",
        "missing_capability_surface",
        "missing_capability_descriptor",
        "provider_invocation_enabled_too_early",
        "workspace_read_execution_enabled_too_early",
        "repository_search_execution_enabled_too_early",
        "file_read_execution_enabled_too_early",
        "local_command_execution_enabled_too_early",
        "local_runtime_execution_enabled_too_early",
        "external_adapter_detected",
        "vendor_hardcoding_detected",
        "credential_materialization_enabled",
        "raw_secret_output_risk",
        "missing_ocel_mapping",
        "missing_permission_policy_ref",
        "growthkernel_dependency_detected",
        "schumpeter_split_detected",
        "general_agent_usability_premature",
        "llm_judge_detected",
    ]:
        assert finding_type in finding_types
    assert report.report_status == "blocked"


def test_registry_ocel_pig_and_ocpx_surfaces():
    service = InternalProviderRegistryReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    for object_type in [
        "internal_provider_registration_request",
        "internal_provider_ref",
        "internal_provider_capability_descriptor",
        "internal_provider_capability_surface",
        "internal_provider_status",
        "internal_provider_registry",
        "internal_provider_registry_snapshot",
        "internal_provider_registry_finding",
        "internal_provider_registry_report",
        "internal_provider_capability_surface_report",
        "internal_provider_contract",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    ]:
        assert object_type in INTERNAL_PROVIDER_REGISTRY_OCEL_OBJECT_TYPES
    for event_type in [
        "internal_provider_registration_requested",
        "internal_provider_contract_loaded",
        "internal_provider_ref_registered",
        "internal_provider_capability_descriptor_registered",
        "internal_provider_capability_surface_created",
        "internal_provider_status_created",
        "internal_provider_registry_created",
        "internal_provider_registry_snapshot_created",
        "internal_provider_registry_report_created",
        "internal_provider_capability_surface_report_created",
        "internal_provider_registry_blocked",
    ]:
        assert event_type in INTERNAL_PROVIDER_REGISTRY_OCEL_EVENT_TYPES
    for relation_type in [
        "registers_internal_provider",
        "declares_provider_capability_surface",
        "declares_provider_capability_descriptor",
        "assigns_provider_status",
        "prepares_workspace_read_provider",
        "prepares_repository_search_provider",
        "prepares_file_read_provider",
        "prepares_ocel_inspection_provider",
        "prepares_pig_inspection_provider",
        "prepares_ocpx_projection_provider",
        "prepares_local_runtime_provider",
        "prepares_diagnostic_provider",
        "prepares_candidate_generation_provider",
        "defers_workspace_read_execution_to_v0_24_2",
        "defers_repository_search_execution_to_v0_24_3",
        "defers_file_read_execution_to_v0_24_3",
        "defers_local_runtime_candidate_to_v0_24_5",
        "not_provider_invoked",
        "not_workspace_file_read",
        "not_repository_searched",
        "not_file_content_extracted",
        "not_local_command_executed",
        "not_external_runtime_touched",
        "not_external_provider_called",
        "prevents_credential_exposure",
        "derived_from_internal_provider_contract",
    ]:
        assert relation_type in INTERNAL_PROVIDER_REGISTRY_OCEL_RELATION_TYPES

    assert pig["version"] == "v0.24.1"
    assert pig["layer"] == "internal_provider"
    assert pig["subject"] == "provider_registry_capability_surface"
    assert "provider registry is not provider invocation" in pig["principles"]
    assert "capability surface is not capability execution" in pig["principles"]
    assert pig["safety_boundary"]["provider_invocation_enabled"] is False
    assert pig["safety_boundary"]["workspace_read_execution_enabled"] is False
    assert pig["safety_boundary"]["repository_search_execution_enabled"] is False
    assert pig["safety_boundary"]["file_read_execution_enabled"] is False
    assert pig["safety_boundary"]["local_runtime_execution_enabled"] is False
    assert pig["safety_boundary"]["local_command_execution_enabled"] is False
    assert pig["safety_boundary"]["external_provider_adapter_implemented"] is False
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

    assert ocpx["state"] == "internal_provider_registry_declared"
    assert ocpx["version"] == "v0.24.1"
    for read_model in [
        "InternalProviderRegistryState",
        "InternalProviderRefState",
        "InternalProviderCapabilitySurfaceState",
        "InternalProviderCapabilityDescriptorState",
        "InternalProviderStatusState",
        "V024ReadinessState",
    ]:
        assert read_model in ocpx["target_read_models"]
    assert ocpx["effect_types"] == INTERNAL_PROVIDER_REGISTRY_ALLOWED_EFFECT_TYPES
