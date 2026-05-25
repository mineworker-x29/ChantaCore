from chanta_core.internal_provider.internal_provider_consolidation import (
    INCLUDED_VERSIONS,
    INTERNAL_PROVIDER_CONSOLIDATION_EFFECT_TYPES,
    INTERNAL_PROVIDER_CONSOLIDATION_EVENT_TYPES,
    INTERNAL_PROVIDER_CONSOLIDATION_OBJECT_TYPES,
    InternalProviderCapabilityMap,
    InternalProviderCapabilityMapService,
    InternalProviderConsolidationReport,
    InternalProviderConsolidationReportService,
    InternalProviderConsolidationSourceService,
    InternalProviderConsolidationWorkbenchSnapshot,
    InternalProviderConsolidationWorkbenchSnapshotService,
    InternalProviderCoverageMatrix,
    InternalProviderCoverageMatrixService,
    InternalProviderFoundationSnapshot,
    InternalProviderGapRegister,
    InternalProviderReleaseManifest,
    InternalProviderRoadmapBoundaryReport,
    InternalProviderRuntimeBoundaryReport,
    InternalProviderSafetyBoundaryReport,
    InternalProviderSubjectComponent,
    InternalProviderSubjectComponentService,
    InternalProviderV025ReadinessReport,
)


def test_consolidation_source_service_is_read_only() -> None:
    sources = InternalProviderConsolidationSourceService().load_all_sources()

    assert "v0.23.9" in sources
    assert all(source["read_only"] is True for source in sources.values())
    assert all(source["new_provider_invocation_performed"] is False for source in sources.values())
    assert all(source["new_local_command_executed"] is False for source in sources.values())


def test_foundation_snapshot_and_subject_components_build() -> None:
    service = InternalProviderConsolidationReportService()
    parts = service.build_all_parts()
    snapshot = parts["snapshot"]
    subjects = parts["subjects"]
    subject_ids = {subject.subject_id for subject in subjects}

    assert isinstance(snapshot, InternalProviderFoundationSnapshot)
    assert snapshot.version == "v0.24.9"
    assert snapshot.release_name == "Internal Provider / Local Runtime Provider Foundation v1"
    assert INCLUDED_VERSIONS == [f"v0.24.{index}" for index in range(10)]
    assert snapshot.included_versions == INCLUDED_VERSIONS
    assert {
        "contract",
        "registry",
        "workspace_read",
        "repository_search_file_read",
        "process_inspection",
        "command_candidate",
        "static_safety_preflight",
        "gated_execution",
        "output_failure_explanation",
        "consolidation",
    }.issubset(subject_ids)
    assert all(isinstance(subject, InternalProviderSubjectComponent) for subject in subjects)
    assert all(subject.external_adapter is False for subject in subjects)


def test_capability_map_and_coverage_matrix_build() -> None:
    subjects = InternalProviderSubjectComponentService().build_subject_components()
    capability_map = InternalProviderCapabilityMapService().build_capability_map(subjects)
    coverage = InternalProviderCoverageMatrixService().build_coverage_matrix(subjects)
    skill_ids = {skill_id for entry in capability_map.entries for skill_id in entry.skill_ids}

    assert isinstance(capability_map, InternalProviderCapabilityMap)
    assert "skill:internal_provider_consolidation_view" in skill_ids
    assert "skill:local_runtime_output_summarize" in skill_ids
    assert capability_map.external_adapter_count == 0
    assert capability_map.bounded_execution_capability_count >= 1
    assert isinstance(coverage, InternalProviderCoverageMatrix)
    assert coverage.coverage_status == "complete"
    assert coverage.missing_required_coverage_count == 0
    assert all(row.has_model and row.has_service and row.has_docs for row in coverage.rows)


def test_safety_runtime_roadmap_gap_release_and_readiness_reports_build() -> None:
    parts = InternalProviderConsolidationReportService().build_all_parts()
    safety = parts["safety_boundary"]
    runtime = parts["runtime_boundary"]
    roadmap = parts["roadmap_boundary"]
    gaps = parts["gaps"]
    manifest = parts["release_manifest"]
    readiness = parts["readiness"]

    assert isinstance(safety, InternalProviderSafetyBoundaryReport)
    assert safety.status == "passed"
    assert safety.command_rerun_count == 0
    assert safety.uncontrolled_local_command_execution_count == 0
    assert safety.unrestricted_shell_count == 0
    assert safety.arbitrary_subprocess_count == 0
    assert safety.shell_true_count == 0
    assert safety.os_system_count == 0
    assert safety.network_access_count == 0
    assert safety.package_install_count == 0
    assert safety.destructive_command_count == 0
    assert safety.credential_exposure_count == 0
    assert safety.raw_secret_output_count == 0
    assert safety.llm_judge_count == 0
    assert isinstance(runtime, InternalProviderRuntimeBoundaryReport)
    assert runtime.runtime_boundary_status == "ready"
    assert runtime.bounded_runner_isolated is True
    assert runtime.subprocess_usage_isolated_to_runner is True
    assert runtime.shell_false_enforced is True
    assert runtime.argv_only_enforced is True
    assert runtime.single_use_authorization_enforced is True
    assert isinstance(roadmap, InternalProviderRoadmapBoundaryReport)
    assert roadmap.next_version == "v0.25.0 Agent Surface Contract"
    assert roadmap.roadmap_status == "aligned"
    assert isinstance(gaps, InternalProviderGapRegister)
    assert {"general_agent_usability_not_started", "external_provider_adapters_not_started", "growthkernel_bridge_not_started"}.issubset({gap.gap_id for gap in gaps.gaps})
    assert isinstance(manifest, InternalProviderReleaseManifest)
    assert manifest.release_status == "releasable"
    assert "ask/repl/general agent UX" in manifest.excluded_capabilities
    assert "External Provider Adapter" in manifest.excluded_capabilities
    assert "Schumpeter split / company wrapper" in manifest.excluded_capabilities
    assert isinstance(readiness, InternalProviderV025ReadinessReport)
    assert readiness.ready_for_v0_25 is True
    assert readiness.recommended_next_version == "v0.25.0 Agent Surface Contract"


def test_consolidation_report_and_workbench_snapshot_build() -> None:
    service = InternalProviderConsolidationReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    workbench = InternalProviderConsolidationWorkbenchSnapshotService().build_workbench_snapshot(report)

    assert isinstance(report, InternalProviderConsolidationReport)
    assert report.version == "v0.24.9"
    assert report.readiness_status == "ready"
    assert report.release_status == "releasable"
    assert report.ready_for_v0_25 is True
    assert report.ready_for_v0_26 is False
    assert report.new_provider_invocation_performed is False
    assert report.new_repository_search_performed is False
    assert report.new_file_read_performed is False
    assert report.new_process_inspection_performed is False
    assert report.new_local_command_executed is False
    assert report.command_rerun_performed is False
    assert report.automatic_repair_performed is False
    assert report.file_mutation_performed is False
    assert report.patch_applied is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_output_dumped is False
    assert report.llm_judge_used is False
    assert isinstance(workbench, InternalProviderConsolidationWorkbenchSnapshot)
    assert workbench.read_only is True
    assert workbench.mutation_performed is False


def test_ocel_pig_ocpx_consolidation_coverage_exists() -> None:
    service = InternalProviderConsolidationReportService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert "internal_provider_consolidation_report" in INTERNAL_PROVIDER_CONSOLIDATION_OBJECT_TYPES
    assert "internal_provider_consolidation_report_created" in INTERNAL_PROVIDER_CONSOLIDATION_EVENT_TYPES
    assert "readiness_state_created" in INTERNAL_PROVIDER_CONSOLIDATION_EFFECT_TYPES
    assert pig["version"] == "v0.24.9"
    assert pig["subject"] == "internal_provider_consolidation"
    assert pig["release_name"] == "Internal Provider / Local Runtime Provider Foundation v1"
    assert pig["safety_boundary"]["new_provider_invocation_performed"] is False
    assert pig["safety_boundary"]["new_local_command_executed"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "internal_provider_foundation_v1_consolidated"
    assert "InternalProviderV025ReadinessState" in ocpx["target_read_models"]
