from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    AlphaArchitectureOverviewGuide,
    AlphaCLIReferenceGuide,
    AlphaDemoScenarioDocumentation,
    AlphaDocumentSet,
    AlphaDocumentSpec,
    AlphaDocumentationConsistencyReport,
    AlphaDocumentationHandoffPacket,
    AlphaDocumentationLinkIntegrityReport,
    AlphaDocumentationPolicy,
    AlphaDocumentationReadinessGate,
    AlphaDocumentationReadinessReport,
    AlphaDocumentationReadinessReportService,
    AlphaDocumentationRequest,
    AlphaDocumentationSafetyBoundaryReport,
    AlphaDocumentationSourceView,
    AlphaExampleDataManifest,
    AlphaExamplePackManifest,
    AlphaExamplePackPolicy,
    AlphaExternalAdapterFutureTrackNote,
    AlphaMemoryFoundationGuide,
    AlphaOCELNativeCoreGuide,
    AlphaOnboardingChecklist,
    AlphaPublicPrivateBoundaryGuide,
    AlphaQuickstartGuide,
    AlphaReadmePlan,
    AlphaRuntimeProfileGuide,
    AlphaSafetyBoundariesGuide,
    AlphaSchumpeterPreparationGuide,
    AlphaSmokeDemoGuide,
    AlphaSyntheticExampleBundle,
    AlphaWorkbenchFoundationGuide,
    V0287_EFFECT_TYPES,
    V0287_FORBIDDEN_EFFECT_TYPES,
)


def _report() -> AlphaDocumentationReadinessReport:
    return AlphaDocumentationReadinessReportService().build_report()


def test_v0287_documentation_models_build() -> None:
    report = _report()

    assert isinstance(report.documentation_policy, AlphaDocumentationPolicy)
    assert isinstance(report.request, AlphaDocumentationRequest)
    assert isinstance(report.source_view, AlphaDocumentationSourceView)
    assert isinstance(report.document_set, AlphaDocumentSet)
    assert all(isinstance(item, AlphaDocumentSpec) for item in report.document_set.documents)
    assert isinstance(report.readme_plan, AlphaReadmePlan)
    assert isinstance(report.quickstart_guide, AlphaQuickstartGuide)
    assert isinstance(report.architecture_overview_guide, AlphaArchitectureOverviewGuide)
    assert isinstance(report.ocel_native_core_guide, AlphaOCELNativeCoreGuide)
    assert isinstance(report.workbench_foundation_guide, AlphaWorkbenchFoundationGuide)
    assert isinstance(report.memory_foundation_guide, AlphaMemoryFoundationGuide)
    assert isinstance(report.runtime_profile_guide, AlphaRuntimeProfileGuide)
    assert isinstance(report.smoke_demo_guide, AlphaSmokeDemoGuide)
    assert isinstance(report.cli_reference_guide, AlphaCLIReferenceGuide)
    assert isinstance(report.safety_boundaries_guide, AlphaSafetyBoundariesGuide)
    assert isinstance(report.public_private_boundary_guide, AlphaPublicPrivateBoundaryGuide)
    assert isinstance(report.schumpeter_preparation_guide, AlphaSchumpeterPreparationGuide)
    assert isinstance(report.external_adapter_future_track_note, AlphaExternalAdapterFutureTrackNote)
    assert isinstance(report.example_pack_policy, AlphaExamplePackPolicy)
    assert isinstance(report.example_pack_manifest, AlphaExamplePackManifest)
    assert isinstance(report.example_data_manifest, AlphaExampleDataManifest)
    assert isinstance(report.synthetic_example_bundle, AlphaSyntheticExampleBundle)
    assert all(isinstance(item, AlphaDemoScenarioDocumentation) for item in report.demo_scenario_documentation)
    assert isinstance(report.onboarding_checklist, AlphaOnboardingChecklist)
    assert isinstance(report.link_integrity_report, AlphaDocumentationLinkIntegrityReport)
    assert isinstance(report.safety_boundary_report, AlphaDocumentationSafetyBoundaryReport)
    assert isinstance(report.consistency_report, AlphaDocumentationConsistencyReport)
    assert isinstance(report.documentation_readiness_gate, AlphaDocumentationReadinessGate)
    assert isinstance(report.handoff_packet, AlphaDocumentationHandoffPacket)


def test_v0287_policy_source_and_document_set_are_public_safe() -> None:
    report = _report()
    policy = report.documentation_policy

    assert policy.version == "v0.28.7"
    assert policy.documentation_enabled is True
    assert policy.onboarding_enabled is True
    assert policy.example_pack_enabled is True
    assert policy.public_safe_docs_required is True
    assert policy.synthetic_examples_required_by_default is True
    assert policy.docs_must_match_feature_flags is True
    assert policy.docs_must_not_overclaim_capabilities is True
    assert policy.future_track_must_be_labeled is True
    assert policy.private_material_forbidden is True
    assert policy.credential_exposure_forbidden is True
    assert policy.secret_exposure_forbidden is True
    assert policy.raw_trace_exposure_forbidden is True
    assert policy.raw_transcript_exposure_forbidden is True
    assert policy.raw_provider_output_exposure_forbidden is True
    assert policy.actual_user_data_forbidden is True
    assert policy.actual_company_data_forbidden is True
    assert policy.provider_invocation_docs_forbidden_now is True
    assert policy.command_execution_expansion_docs_forbidden_now is True
    assert policy.external_adapter_docs_must_be_future_track_only is True
    assert policy.schumpeter_runtime_docs_forbidden_now is True
    assert policy.package_publish_docs_forbidden_now is True
    assert policy.release_tag_docs_forbidden_now is True
    assert policy.llm_judge_as_sole_documentation_authority_forbidden is True

    source = report.source_view
    assert source.runtime_profile_report_ref is not None
    assert source.operator_handoff_packet_ref is not None
    assert source.smoke_scenario_catalog_ref is not None
    assert source.ocel_demo_pack_ref is not None
    assert source.ocpx_projection_demo_ref is not None
    assert source.pig_report_demo_ref is not None
    assert source.workbench_report_demo_ref is not None
    assert source.memory_foundation_demo_ref is not None
    assert source.continuity_preview_demo_ref is not None
    assert source.safety_boundary_demo_ref is not None
    assert source.cli_workflow_demo_ref is not None
    assert source.schumpeter_preparation_report_ref is not None
    assert source.public_private_boundary_report_ref is not None
    assert source.packaging_readiness_report_ref is not None
    assert source.release_hygiene_gate_report_ref is not None
    assert source.existing_doc_refs
    assert source.example_candidate_refs
    assert source.public_safe_demo_refs
    assert source.blocked_private_refs
    assert source.private_material_detected is False
    assert source.credential_detected is False
    assert source.secret_detected is False
    assert source.raw_trace_detected is False
    assert source.raw_transcript_detected is False
    assert source.raw_provider_output_detected is False

    doc_names = {item.doc_name for item in report.document_set.documents}
    expected_docs = {"README.md", "QUICKSTART.md", "ARCHITECTURE.md", "SAFETY_BOUNDARIES.md", "PUBLIC_PRIVATE_BOUNDARY.md", "WORKBENCH_FOUNDATION.md", "MEMORY_FOUNDATION.md", "PUBLIC_ALPHA_RUNTIME_PROFILE.md", "SMOKE_DEMO_FLOW.md", "CLI_REFERENCE.md", "EXAMPLES.md", "SCHUMPETER_PREPARATION.md", "EXTERNAL_ADAPTER_FUTURE_TRACK.md", "ONBOARDING_CHECKLIST.md"}
    assert expected_docs <= doc_names
    assert report.document_set.required_doc_count >= len(expected_docs)
    assert report.document_set.missing_required_doc_count == 0
    assert all(item.public_safe_required is True for item in report.document_set.documents)
    assert all(item.private_material_allowed is False for item in report.document_set.documents)


def test_v0287_guides_match_feature_flags_and_boundaries() -> None:
    report = _report()

    assert {"project_summary", "current_status", "public_alpha_scope", "enabled_preview_disabled_features", "safety_boundaries", "public_private_boundary", "examples_link", "Schumpeter_preparation_note", "external_adapter_future_track_note", "limitations"} <= set(report.readme_plan.required_sections)
    assert report.readme_plan.overclaim_detected is False
    assert {"provider_invocation", "command_execution_expansion", "package_publish", "release_tag_creation", "Schumpeter_private_runtime", "external_adapter_run"} <= set(report.quickstart_guide.forbidden_steps)
    assert report.quickstart_guide.uses_private_data is False
    assert report.quickstart_guide.invokes_provider is False
    assert report.quickstart_guide.executes_command_expansion is False
    assert "OCEL_native_core" in report.architecture_overview_guide.sections
    assert "Future_external_adapter_boundary" in report.architecture_overview_guide.sections
    assert report.architecture_overview_guide.claims_production_ready is False

    assert report.ocel_native_core_guide.explains_ocel_store is True
    assert report.ocel_native_core_guide.uses_synthetic_examples_only is True
    assert "trace_explorer" in report.workbench_foundation_guide.covered_surfaces
    assert report.workbench_foundation_guide.provider_invocation_claimed is False
    assert report.workbench_foundation_guide.command_execution_claimed is False
    assert "injection_boundary_preview" in report.memory_foundation_guide.covered_memory_surfaces
    assert report.memory_foundation_guide.autonomous_memory_execution_claimed is False
    assert report.memory_foundation_guide.runtime_injection_claimed is False
    assert report.runtime_profile_guide.enabled_features_documented is True
    assert report.runtime_profile_guide.preview_features_documented is True
    assert report.runtime_profile_guide.disabled_future_features_documented is True
    assert report.runtime_profile_guide.production_runtime_claimed is False
    assert report.smoke_demo_guide.documents_synthetic_ocel_demo is True
    assert report.smoke_demo_guide.documents_cli_demo is True
    assert report.smoke_demo_guide.uses_actual_data is False
    assert report.smoke_demo_guide.invokes_provider is False
    assert report.smoke_demo_guide.expands_command_execution is False
    assert "alpha runtime" in report.cli_reference_guide.documented_cli_groups
    assert report.cli_reference_guide.documents_provider_invocation is False
    assert report.cli_reference_guide.documents_command_execution_expansion is False
    assert {"no_provider_invocation", "no_command_execution_expansion", "no_network_calls", "no_runtime_continuity_injection", "no_autonomous_memory_execution", "no_private_data", "no_credentials", "no_raw_traces", "no_raw_transcripts", "no_raw_provider_outputs", "no_external_adapter", "no_Schumpeter_private_runtime"} <= set(report.safety_boundaries_guide.covered_boundaries)
    assert report.safety_boundaries_guide.contradictions_detected is False


def test_v0287_schumpeter_future_track_examples_and_readiness() -> None:
    report = _report()

    assert report.public_private_boundary_guide.explains_public_core_private_overlay is True
    assert report.public_private_boundary_guide.explains_private_artifact_exclusions is True
    assert report.public_private_boundary_guide.private_material_exposed is False
    assert report.schumpeter_preparation_guide.explains_preparation_only is True
    assert report.schumpeter_preparation_guide.explains_private_overlay_contract is True
    assert report.schumpeter_preparation_guide.explains_deferred_runtime is True
    assert report.schumpeter_preparation_guide.explains_RPA_adapter_deferral is True
    assert report.schumpeter_preparation_guide.claims_runtime_implemented is False
    assert report.schumpeter_preparation_guide.exposes_company_material is False
    assert report.external_adapter_future_track_note.explains_v029_contract_first is True
    assert report.external_adapter_future_track_note.explains_adapter_preflight_required is True
    assert report.external_adapter_future_track_note.explains_provider_invocation_not_enabled is True
    assert report.external_adapter_future_track_note.explains_RPA_future_track is True
    assert report.external_adapter_future_track_note.claims_adapter_implemented is False

    assert report.example_pack_policy.synthetic_examples_required is True
    assert report.example_pack_manifest.example_count == report.example_pack_manifest.synthetic_example_count
    assert report.example_pack_manifest.contains_private_data is False
    assert report.example_pack_manifest.contains_credentials is False
    assert report.example_pack_manifest.contains_raw_trace is False
    assert report.example_pack_manifest.contains_raw_transcript is False
    assert report.example_pack_manifest.contains_raw_provider_output is False
    assert report.example_data_manifest.actual_user_data_used is False
    assert report.example_data_manifest.actual_company_data_used is False
    assert report.example_data_manifest.raw_trace_used is False
    assert report.example_data_manifest.raw_transcript_used is False
    assert report.example_data_manifest.raw_provider_output_used is False
    assert report.synthetic_example_bundle.synthetic_only is True
    assert report.synthetic_example_bundle.reproducible is True
    assert report.synthetic_example_bundle.contains_private_identifiers is False
    assert all(item.overclaims_execution is False and item.uses_private_data is False for item in report.demo_scenario_documentation)

    assert {"read_project_status", "install_or_setup_locally", "inspect_feature_flags", "run_or_review_smoke_demo", "inspect_safety_boundaries", "inspect_public_private_boundary", "inspect_examples", "understand_disabled_future_tracks", "understand_no_provider_invocation", "understand_no_command_execution_expansion"} <= set(report.onboarding_checklist.required_items)
    assert report.link_integrity_report.missing_link_count == 0
    assert report.safety_boundary_report.production_runtime_claim_count == 0
    assert report.safety_boundary_report.provider_invocation_claim_count == 0
    assert report.safety_boundary_report.command_execution_expansion_claim_count == 0
    assert report.safety_boundary_report.external_adapter_claim_count == 0
    assert report.safety_boundary_report.schumpeter_runtime_claim_count == 0
    assert report.safety_boundary_report.private_material_exposure_count == 0
    assert report.safety_boundary_report.credential_exposure_count == 0
    assert report.safety_boundary_report.raw_trace_exposure_count == 0
    assert report.safety_boundary_report.raw_transcript_exposure_count == 0
    assert report.safety_boundary_report.raw_provider_output_exposure_count == 0
    assert report.consistency_report.enabled_feature_overclaim_count == 0
    assert report.consistency_report.preview_feature_overclaim_count == 0
    assert report.consistency_report.disabled_feature_overclaim_count == 0
    assert report.consistency_report.future_track_mislabel_count == 0
    assert report.documentation_readiness_gate.docs_ready_for_v0_28_8 is True
    assert report.documentation_readiness_gate.public_alpha_release_claim_allowed is False
    assert report.handoff_packet.target_version == "v0.28.8"
    assert report.handoff_packet.refs_only is True
    assert report.handoff_packet.implementation_performed_now is False
    assert {"public_alpha_release", "package_publish", "release_tag_creation", "production_runtime", "external_provider_adapter", "RPA_adapter", "A360_adapter", "Brity_adapter", "UiPath_adapter", "Schumpeter_private_runtime", "runtime_continuity_injection", "autonomous_memory_execution"} <= set(report.handoff_packet.not_implemented_now)


def test_v0287_report_flags_mappings_and_cli_commands() -> None:
    service = AlphaDocumentationReadinessReportService()
    report = service.build_report()

    assert report.ready_for_v0_28_8 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.documentation_ready is True
    assert report.onboarding_ready is True
    assert report.example_pack_ready is True
    assert report.public_alpha_ready is False
    for flag in [
        "public_alpha_release_implemented",
        "package_published",
        "release_tag_created",
        "production_runtime_claimed",
        "provider_invocation_documented_as_enabled",
        "command_execution_expansion_documented_as_enabled",
        "external_adapter_documented_as_enabled",
        "RPA_adapter_documented_as_enabled",
        "schumpeter_private_runtime_documented_as_enabled",
        "actual_user_data_used",
        "actual_company_data_used",
        "private_material_exposed",
        "credential_exposed",
        "secret_exposed",
        "raw_trace_exposed",
        "raw_transcript_exposed",
        "raw_provider_output_exposed",
        "provider_invoked",
        "command_executed",
        "network_called",
        "runtime_continuity_injected",
        "external_adapter_implemented",
        "references_runtime_dependency_added",
        "references_code_copied",
        "llm_judge_used",
    ]:
        assert getattr(report, flag) is False

    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    assert pig["version"] == "v0.28.7"
    assert pig["subject"] == "alpha_documentation_onboarding_example_pack"
    assert ocpx["state"] == "alpha_documentation_onboarding_example_pack_created"
    assert "alpha_documentation_created" in V0287_EFFECT_TYPES
    assert "state_candidate_created" in V0287_EFFECT_TYPES
    assert "package_published" in V0287_FORBIDDEN_EFFECT_TYPES
    assert "AlphaDocumentationState" in ocpx["target_read_models"]

    docs_commands = ["policy", "source-view", "document-set", "readme", "quickstart", "architecture", "ocel-core", "workbench", "memory", "runtime-profile", "smoke-demo", "cli-reference", "safety", "public-private", "schumpeter", "external-adapter-future", "onboarding", "links", "safety-report", "consistency", "readiness", "handoff", "report"]
    for command in docs_commands:
        assert main(["alpha", "docs", command]) == 0
    for command in ["policy", "manifest", "data-manifest", "synthetic-bundle"]:
        assert main(["alpha", "examples", command]) == 0
