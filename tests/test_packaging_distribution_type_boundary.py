from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    BuildBackendReadinessReport,
    CLISmokePlan,
    CLISmokeReport,
    DependencyBoundaryPolicy,
    DevDependencyReport,
    DistributionArtifactPolicy,
    ImportSmokePlan,
    ImportSmokeReport,
    OptionalDependencyGroupReport,
    PackageDataBoundaryReport,
    PackageIncludeExcludePolicy,
    PackagePublishBlocker,
    PackagingDistributionTypeBoundaryPolicy,
    PackagingFinding,
    PackagingReadinessGate,
    PackagingReadinessReport,
    PackagingReadinessReportService,
    PackagingReadinessRequest,
    PackagingRemediationItem,
    PackagingRemediationPlan,
    PackagingSourceView,
    PyTypedMarkerReport,
    PyprojectPackageMetadataReport,
    PytestRuntimeDependencyViolationReport,
    RuntimeDependencyReport,
    SdistBuildSmokePlan,
    SdistBuildSmokeReport,
    TypeDistributionBoundaryReport,
    V0282_EFFECT_TYPES,
    V0282_EVENT_TYPES,
    V0282_FORBIDDEN_EFFECT_TYPES,
    V0282_OBJECT_TYPES,
    WheelBuildSmokePlan,
    WheelBuildSmokeReport,
)


def _parts() -> dict:
    return PackagingReadinessReportService().build_all_parts()


def test_packaging_boundary_models_build() -> None:
    parts = _parts()
    report = parts["report"]

    assert isinstance(parts["policy"], PackagingDistributionTypeBoundaryPolicy)
    assert isinstance(parts["request"], PackagingReadinessRequest)
    assert isinstance(parts["source-view"], PackagingSourceView)
    assert isinstance(parts["pyproject"], PyprojectPackageMetadataReport)
    assert isinstance(parts["dependencies"], DependencyBoundaryPolicy)
    assert isinstance(parts["runtime-deps"], RuntimeDependencyReport)
    assert isinstance(parts["dev-deps"], DevDependencyReport)
    assert isinstance(parts["optional-deps"], OptionalDependencyGroupReport)
    assert isinstance(parts["pytest-boundary"], PytestRuntimeDependencyViolationReport)
    assert isinstance(parts["build-backend"], BuildBackendReadinessReport)
    assert isinstance(parts["include-exclude"], PackageIncludeExcludePolicy)
    assert isinstance(parts["package-data"], PackageDataBoundaryReport)
    assert isinstance(parts["py-typed"], PyTypedMarkerReport)
    assert isinstance(parts["type-boundary"], TypeDistributionBoundaryReport)
    assert isinstance(report.wheel_build_smoke_plan, WheelBuildSmokePlan)
    assert isinstance(parts["wheel-smoke"], WheelBuildSmokeReport)
    assert isinstance(report.sdist_build_smoke_plan, SdistBuildSmokePlan)
    assert isinstance(parts["sdist-smoke"], SdistBuildSmokeReport)
    assert isinstance(report.import_smoke_plan, ImportSmokePlan)
    assert isinstance(parts["import-smoke"], ImportSmokeReport)
    assert isinstance(report.cli_smoke_plan, CLISmokePlan)
    assert isinstance(parts["cli-smoke"], CLISmokeReport)
    assert isinstance(report.distribution_artifact_policy, DistributionArtifactPolicy)
    assert isinstance(parts["publish-blocker"], PackagePublishBlocker)
    assert isinstance(parts["remediation"], PackagingRemediationPlan)
    assert isinstance(parts["remediation"].remediation_items[0], PackagingRemediationItem)
    assert isinstance(parts["readiness"], PackagingReadinessGate)
    assert isinstance(report.findings[0], PackagingFinding)
    assert isinstance(report, PackagingReadinessReport)


def test_packaging_policy_source_and_pyproject_metadata() -> None:
    parts = _parts()
    policy = parts["policy"]
    source = parts["source-view"]
    pyproject = parts["pyproject"]

    assert policy.version == "v0.28.2"
    assert policy.layer == "public_alpha_schumpeter_preparation"
    assert policy.packaging_boundary_enabled is True
    assert policy.package_distribution_readiness_enabled is True
    assert policy.package_publish_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.official_release_artifact_enabled_now is False
    assert policy.wheel_smoke_enabled is True
    assert policy.sdist_smoke_enabled is True
    assert policy.import_smoke_enabled is True
    assert policy.cli_smoke_enabled is True
    assert policy.py_typed_required is True
    assert policy.runtime_dev_dependency_separation_required is True
    assert policy.pytest_runtime_dependency_forbidden is True
    assert policy.runtime_data_package_inclusion_forbidden is True
    assert policy.references_package_inclusion_forbidden_by_default is True
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert policy.external_adapter_enabled_now is False
    assert policy.schumpeter_split_enabled_now is False
    assert policy.llm_judge_as_sole_packaging_authority_forbidden is True
    assert source.release_hygiene_gate_report_ref is not None
    assert source.pyproject_present is True
    assert source.package_layout_known is True
    assert source.raw_secret_included is False
    assert source.credential_included is False
    assert source.company_private_material_included is False
    assert pyproject.pyproject_present is True
    assert pyproject.project_name == "chanta-core"
    assert pyproject.project_version == "0.30.0"
    assert pyproject.build_backend == "setuptools.build_meta"
    assert pyproject.project_description_present is True
    assert pyproject.authors_present is True
    assert pyproject.readme_metadata_present is True


def test_dependency_package_data_type_and_smoke_boundaries() -> None:
    parts = _parts()
    deps = parts["runtime-deps"]
    pytest_boundary = parts["pytest-boundary"]
    include = parts["include-exclude"]
    package_data = parts["package-data"]
    py_typed = parts["py-typed"]
    type_boundary = parts["type-boundary"]
    report = parts["report"]

    assert parts["dependencies"].pytest_must_not_be_runtime_dependency is True
    assert deps.runtime_dependency_count >= 1
    assert deps.pytest_in_runtime_dependencies is True
    assert deps.test_tooling_in_runtime_dependencies
    assert deps.external_provider_sdk_runtime_dependencies
    assert pytest_boundary.pytest_detected_in_runtime is True
    assert pytest_boundary.blocks_package_distribution_ready is True
    assert include.tests_excluded_from_runtime_package_by_default is True
    assert include.docs_excluded_from_runtime_package_by_default is True
    assert include.data_runtime_artifacts_excluded is True
    assert include.references_excluded_by_default is True
    assert include.raw_trace_excluded is True
    assert include.raw_transcript_excluded is True
    assert include.raw_provider_output_excluded is True
    assert include.secrets_excluded is True
    assert include.credentials_excluded is True
    assert include.company_private_material_excluded is True
    assert package_data.runtime_data_included is False
    assert package_data.references_included is False
    assert package_data.raw_trace_included is False
    assert package_data.raw_transcript_included is False
    assert package_data.raw_provider_output_included is False
    assert package_data.secret_included is False
    assert package_data.credential_included is False
    assert package_data.company_private_material_included is False
    assert py_typed.py_typed_present in {True, False}
    assert type_boundary.type_check_runtime_required is False
    assert report.wheel_build_smoke_plan.publish_allowed_now is False
    assert report.wheel_build_smoke_report.wheel_artifact_published is False
    assert report.sdist_build_smoke_plan.publish_allowed_now is False
    assert report.sdist_build_smoke_report.sdist_artifact_published is False
    assert report.import_smoke_plan.external_provider_invocation_allowed is False
    assert report.import_smoke_plan.command_execution_expansion_allowed is False
    assert report.import_smoke_report.provider_invoked is False
    assert report.import_smoke_report.command_executed is False
    assert report.cli_smoke_plan.provider_invocation_allowed is False
    assert report.cli_smoke_plan.command_execution_expansion_allowed is False
    assert report.cli_smoke_report.provider_invoked is False
    assert report.cli_smoke_report.command_executed is False


def test_publish_blocker_readiness_report_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = PackagingReadinessReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert parts["publish-blocker"].package_publish_blocked is True
    assert parts["publish-blocker"].package_upload_blocked is True
    assert parts["publish-blocker"].release_tag_creation_blocked is True
    assert parts["readiness"].package_distribution_ready is False
    assert parts["readiness"].public_alpha_release_ready is False
    assert report.ready_for_v0_28_3 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.public_alpha_ready is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.official_release_artifact_created is False
    assert report.auto_fix_performed is False
    assert report.schumpeter_split_implemented is False
    assert report.external_adapter_implemented is False
    assert report.provider_invoked is False
    assert report.command_executed is False
    assert report.company_private_material_exposed is False
    assert report.credential_exposed is False
    assert report.raw_trace_exposed is False
    assert report.raw_transcript_exposed is False
    assert report.raw_provider_output_exposed is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.28.3 Public-Private Boundary / Redaction / Reference Policy"
    assert "packaging_readiness_report" in V0282_OBJECT_TYPES
    assert "packaging_readiness_report_created" in V0282_EVENT_TYPES
    assert "packaging_boundary_created" in V0282_EFFECT_TYPES
    assert "package_published" in V0282_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.28.2"
    assert pig["subject"] == "packaging_distribution_type_boundary"
    assert ocpx["state"] == "packaging_distribution_type_boundary_created"
    assert "PackagingBoundaryState" in ocpx["target_read_models"]

    for command in [
        "policy",
        "source-view",
        "pyproject",
        "dependencies",
        "runtime-deps",
        "dev-deps",
        "optional-deps",
        "pytest-boundary",
        "build-backend",
        "include-exclude",
        "package-data",
        "py-typed",
        "type-boundary",
        "wheel-smoke",
        "sdist-smoke",
        "import-smoke",
        "cli-smoke",
        "publish-blocker",
        "remediation",
        "readiness",
        "report",
    ]:
        assert main(["alpha", "packaging", command]) == 0
        output = capsys.readouterr().out
        assert "version=v0.28.2" in output
        assert "ready_for_v0_28_3=true" in output
        assert "ready_for_public_alpha_release_claim=false" in output
        assert "public_alpha_ready=false" in output
        assert "package_published=false" in output
        assert "release_tag_created=false" in output
        assert "official_release_artifact_created=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "llm_judge_used=false" in output
