from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    AlphaCLIWorkflowDemo,
    AlphaContinuityPreviewDemo,
    AlphaDisabledFutureTrackFeatureSet,
    AlphaEnabledFeatureSet,
    AlphaMemoryFoundationDemo,
    AlphaOCELDemoPack,
    AlphaOCPXProjectionDemo,
    AlphaOperatorHandoffPacket,
    AlphaOperatorSurfacePolicy,
    AlphaPIGReportDemo,
    AlphaPreviewOnlyFeatureSet,
    AlphaRuntimeCapabilityEntry,
    AlphaRuntimeCapabilityMatrix,
    AlphaRuntimeProfileReport,
    AlphaRuntimeProfileReportService,
    AlphaSafetyBoundaryDemo,
    AlphaSmokeInputBundle,
    AlphaSmokeRunPlan,
    AlphaSmokeRunReport,
    AlphaSmokeScenario,
    AlphaSmokeScenarioCatalog,
    AlphaSyntheticDemoDataPolicy,
    AlphaWorkbenchReportDemo,
    PublicAlphaFeatureFlag,
    PublicAlphaFeatureFlagMatrix,
    PublicAlphaRuntimeProfilePolicy,
    PublicAlphaRuntimeProfileRequest,
    PublicAlphaRuntimeSourceView,
    V0286_EFFECT_TYPES,
    V0286_FORBIDDEN_EFFECT_TYPES,
)


def _parts():
    return AlphaRuntimeProfileReportService().build_all_parts()


def test_v0286_runtime_profile_models_build() -> None:
    parts = _parts()
    report = parts["report"]

    assert isinstance(report.runtime_profile_policy, PublicAlphaRuntimeProfilePolicy)
    assert isinstance(report.request, PublicAlphaRuntimeProfileRequest)
    assert isinstance(report.source_view, PublicAlphaRuntimeSourceView)
    assert isinstance(report.feature_flag_matrix, PublicAlphaFeatureFlagMatrix)
    assert all(isinstance(item, PublicAlphaFeatureFlag) for item in report.feature_flag_matrix.feature_flags)
    assert isinstance(report.enabled_feature_set, AlphaEnabledFeatureSet)
    assert isinstance(report.preview_only_feature_set, AlphaPreviewOnlyFeatureSet)
    assert isinstance(report.disabled_future_track_feature_set, AlphaDisabledFutureTrackFeatureSet)
    assert isinstance(report.runtime_capability_matrix, AlphaRuntimeCapabilityMatrix)
    assert all(isinstance(item, AlphaRuntimeCapabilityEntry) for item in report.runtime_capability_matrix.capability_entries)
    assert isinstance(report.operator_surface_policy, AlphaOperatorSurfacePolicy)
    assert isinstance(report.smoke_scenario_catalog, AlphaSmokeScenarioCatalog)
    assert all(isinstance(item, AlphaSmokeScenario) for item in report.smoke_scenario_catalog.scenarios)
    assert isinstance(report.smoke_input_bundle, AlphaSmokeInputBundle)
    assert isinstance(report.synthetic_demo_data_policy, AlphaSyntheticDemoDataPolicy)
    assert isinstance(report.ocel_demo_pack, AlphaOCELDemoPack)
    assert isinstance(report.ocpx_projection_demo, AlphaOCPXProjectionDemo)
    assert isinstance(report.pig_report_demo, AlphaPIGReportDemo)
    assert isinstance(report.workbench_report_demo, AlphaWorkbenchReportDemo)
    assert isinstance(report.memory_foundation_demo, AlphaMemoryFoundationDemo)
    assert isinstance(report.continuity_preview_demo, AlphaContinuityPreviewDemo)
    assert isinstance(report.safety_boundary_demo, AlphaSafetyBoundaryDemo)
    assert isinstance(report.cli_workflow_demo, AlphaCLIWorkflowDemo)
    assert isinstance(report.smoke_run_plan, AlphaSmokeRunPlan)
    assert isinstance(report.smoke_run_report, AlphaSmokeRunReport)
    assert isinstance(report.operator_handoff_packet, AlphaOperatorHandoffPacket)
    assert isinstance(report, AlphaRuntimeProfileReport)


def test_v0286_policy_source_and_feature_sets_are_public_safe() -> None:
    report = _parts()["report"]
    policy = report.runtime_profile_policy

    assert policy.version == "v0.28.6"
    assert policy.runtime_profile_enabled is True
    assert policy.smoke_demo_flow_enabled is True
    assert policy.deterministic_demo_required is True
    assert policy.public_safe_data_required is True
    assert policy.synthetic_data_required_by_default is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.network_call_enabled_now is False
    assert policy.command_execution_expansion_enabled_now is False
    assert policy.shell_execution_enabled_now is False
    assert policy.runtime_continuity_injection_enabled_now is False
    assert policy.autonomous_memory_execution_enabled_now is False
    assert policy.production_runtime_enabled_now is False
    assert policy.schumpeter_private_overlay_runtime_enabled_now is False
    assert policy.external_adapter_enabled_now is False
    assert policy.rpa_adapter_enabled_now is False
    assert policy.actual_user_data_forbidden is True
    assert policy.actual_company_data_forbidden is True
    assert policy.raw_trace_forbidden is True
    assert policy.raw_transcript_forbidden is True
    assert policy.raw_provider_output_forbidden is True
    assert policy.credential_forbidden is True
    assert policy.secret_forbidden is True
    assert policy.references_runtime_dependency_forbidden is True
    assert policy.references_code_copy_forbidden is True
    assert policy.PIG_execution_authority_forbidden is True
    assert policy.llm_judge_as_sole_smoke_authority_forbidden is True

    source = report.source_view
    assert source.schumpeter_preparation_report_ref is not None
    assert source.schumpeter_handoff_packet_ref is not None
    assert source.public_private_boundary_report_ref is not None
    assert source.packaging_readiness_report_ref is not None
    assert source.release_hygiene_gate_report_ref is not None
    assert source.memory_consolidation_report_ref is not None
    assert source.workbench_consolidation_report_ref is not None
    assert source.import_smoke_report_ref is not None
    assert source.cli_smoke_report_ref is not None
    assert source.available_public_safe_refs
    assert source.available_demo_refs
    assert source.blocked_private_refs
    assert source.disabled_future_track_refs
    assert source.schumpeter_private_overlay_dependency_detected is False
    assert source.private_data_detected is False
    assert source.credential_detected is False
    assert source.raw_trace_detected is False
    assert source.raw_transcript_detected is False
    assert source.raw_provider_output_detected is False

    enabled = set(report.enabled_feature_set.expected_enabled_features)
    assert {"OCEL_store_validation", "OCPX_projection_demo", "PIG_report_demo", "Workbench_report_surfaces", "Memory_foundation_report_surfaces", "CLI_report_surfaces", "synthetic_demo_data_loading", "safety_boundary_demo"} <= enabled
    preview = set(report.preview_only_feature_set.expected_preview_features)
    assert {"continuity_context_pack_preview", "continuity_injection_bundle_preview", "durable_memory_registry_dry_run_preview", "Schumpeter_private_overlay_manifest_preview", "external_adapter_preflight_preview"} <= preview
    disabled = set(report.disabled_future_track_feature_set.expected_disabled_or_future_features)
    assert {"provider_invocation", "command_execution_expansion", "runtime_continuity_injection", "autonomous_memory_driven_execution", "external_provider_adapter", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "Schumpeter_company_runtime", "production_runtime"} <= disabled


def test_v0286_capabilities_smoke_scenarios_and_demo_data() -> None:
    report = _parts()["report"]

    assert report.feature_flag_matrix.enabled_count >= 8
    assert report.feature_flag_matrix.preview_only_count >= 5
    assert report.feature_flag_matrix.disabled_count >= 4
    assert report.feature_flag_matrix.future_track_count >= 7
    assert all(item.requires_provider_invocation is False for item in report.feature_flag_matrix.feature_flags)
    assert all(item.requires_command_execution is False for item in report.feature_flag_matrix.feature_flags)
    assert all(item.requires_private_data is False for item in report.feature_flag_matrix.feature_flags)
    assert all(item.requires_schumpeter_private_overlay is False for item in report.feature_flag_matrix.feature_flags)

    for entry in report.runtime_capability_matrix.capability_entries:
        assert entry.invokes_provider is False
        assert entry.executes_command is False
        assert entry.mutates_files is False
        assert entry.uses_private_data is False
        assert entry.uses_schumpeter_private_overlay is False

    scenarios = {item.scenario_name: item for item in report.smoke_scenario_catalog.scenarios}
    expected = {"version_check", "import_smoke", "cli_help_smoke", "synthetic_ocel_load", "ocpx_projection_demo", "pig_report_demo", "workbench_report_demo", "memory_foundation_report_demo", "durable_registry_dry_run_demo", "continuity_context_preview_demo", "safety_boundary_demo", "forbidden_pattern_scan_demo"}
    assert expected <= set(scenarios)
    for scenario in scenarios.values():
        assert scenario.deterministic is True
        assert scenario.uses_synthetic_data_only is True
        assert scenario.uses_private_data is False
        assert scenario.invokes_provider is False
        assert scenario.executes_command is False
        assert scenario.mutates_files is False
        assert scenario.requires_network is False

    assert report.smoke_input_bundle.synthetic_only is True
    assert report.smoke_input_bundle.contains_private_data is False
    assert report.smoke_input_bundle.contains_credentials is False
    assert report.smoke_input_bundle.contains_raw_trace is False
    assert report.smoke_input_bundle.contains_raw_transcript is False
    assert report.smoke_input_bundle.contains_raw_provider_output is False
    assert report.synthetic_demo_data_policy.synthetic_data_required_by_default is True
    assert report.synthetic_demo_data_policy.demo_data_must_be_reproducible is True
    assert report.ocel_demo_pack.synthetic_only is True
    assert report.ocel_demo_pack.contains_private_data is False


def test_v0286_demo_surfaces_smoke_report_handoff_and_mappings() -> None:
    service = AlphaRuntimeProfileReportService()
    report = service.build_report()

    assert report.ocpx_projection_demo.provider_invoked is False
    assert report.ocpx_projection_demo.command_executed is False
    assert report.pig_report_demo.PIG_execution_authority_enabled is False
    assert report.pig_report_demo.provider_invoked is False
    assert report.pig_report_demo.command_executed is False
    assert "trace_explorer_report" in report.workbench_report_demo.expected_workbench_surfaces
    assert report.workbench_report_demo.file_mutated is False
    assert "memory_contract_report" in report.memory_foundation_demo.expected_memory_surfaces
    assert report.memory_foundation_demo.autonomous_memory_execution_enabled is False
    assert report.memory_foundation_demo.runtime_continuity_injected is False
    assert report.continuity_preview_demo.preview_is_not_runtime_injection is True
    assert report.continuity_preview_demo.runtime_continuity_injected is False
    assert report.continuity_preview_demo.default_agent_context_mutated is False
    assert report.continuity_preview_demo.decision_service_mutated is False
    assert report.continuity_preview_demo.skill_router_mutated is False
    assert "provider_invocation_forbidden" in report.safety_boundary_demo.expected_safety_checks
    assert "Schumpeter_private_overlay_runtime_forbidden" in report.safety_boundary_demo.expected_safety_checks
    assert report.safety_boundary_demo.all_forbidden_flags_false is True
    assert "provider invocation" in report.cli_workflow_demo.forbidden_cli_targets
    assert report.cli_workflow_demo.provider_invoked is False
    assert report.cli_workflow_demo.command_executed is False

    plan = report.smoke_run_plan
    assert plan.run_mode == "metadata_only"
    assert plan.provider_invocation_allowed is False
    assert plan.command_execution_expansion_allowed is False
    assert plan.network_allowed is False
    assert plan.file_mutation_allowed is False
    smoke = report.smoke_run_report
    assert smoke.provider_invoked is False
    assert smoke.command_executed is False
    assert smoke.network_called is False
    assert smoke.file_mutated is False
    assert smoke.private_data_used is False
    assert smoke.raw_trace_used is False
    assert smoke.raw_transcript_used is False
    assert smoke.raw_provider_output_used is False

    handoff = report.operator_handoff_packet
    assert handoff.target_version == "v0.28.7"
    assert handoff.refs_only is True
    assert handoff.implementation_performed_now is False
    assert {"production_runtime", "package_publish", "release_tag_creation", "external_provider_adapter", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "runtime_continuity_injection", "autonomous_memory_driven_execution", "Schumpeter_private_overlay_runtime", "company_deployment"} <= set(handoff.not_implemented_now)

    assert report.ready_for_v0_28_7 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.public_alpha_ready is False
    assert report.public_alpha_runtime_profile_ready is True
    assert report.public_alpha_smoke_flow_ready is True
    for flag in [
        "production_runtime_implemented",
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "official_release_artifact_created",
        "schumpeter_private_runtime_used",
        "company_wrapper_implemented",
        "external_adapter_implemented",
        "RPA_adapter_implemented",
        "A360_adapter_implemented",
        "Brity_adapter_implemented",
        "UiPath_adapter_implemented",
        "provider_invoked",
        "command_executed",
        "network_called",
        "runtime_continuity_injected",
        "autonomous_memory_execution_enabled",
        "actual_user_data_used",
        "actual_company_data_used",
        "raw_trace_used",
        "raw_transcript_used",
        "raw_provider_output_used",
        "credential_exposed",
        "secret_exposed",
        "references_runtime_dependency_added",
        "references_code_copied",
        "PIG_execution_authority_enabled",
        "llm_judge_used",
    ]:
        assert getattr(report, flag) is False

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    assert pig["version"] == "v0.28.6"
    assert pig["subject"] == "public_alpha_runtime_profile_smoke_demo_flow"
    assert ocpx["state"] == "public_alpha_runtime_profile_smoke_demo_flow_created"
    assert "public_alpha_runtime_profile_created" in V0286_EFFECT_TYPES
    assert "production_runtime_implemented" in V0286_FORBIDDEN_EFFECT_TYPES
    assert "PublicAlphaRuntimeProfileState" in ocpx["target_read_models"]


def test_v0286_runtime_and_smoke_cli_commands_work() -> None:
    runtime_commands = ["policy", "source-view", "feature-flags", "enabled", "preview-only", "disabled", "capabilities", "operator-surface", "handoff", "report"]
    smoke_commands = ["scenarios", "inputs", "synthetic-policy", "ocel-demo", "ocpx-demo", "pig-demo", "workbench-demo", "memory-demo", "continuity-preview", "safety-demo", "cli-demo", "plan", "report"]

    for command_name in runtime_commands:
        assert main(["alpha", "runtime", command_name]) == 0
    for command_name in smoke_commands:
        assert main(["alpha", "smoke", command_name]) == 0
