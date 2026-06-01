from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.public_alpha_schumpeter_preparation import (
    CIWorkflowPresenceReport,
    ChangelogPresenceReport,
    CleanWorktreeReport,
    ContributingPresenceReport,
    DeferAlphaDecision,
    ForbiddenRepositoryArtifactScanReport,
    GitignoreHygieneReport,
    LicensePresenceReport,
    NoReleaseDecision,
    PublicAlphaReleaseClaimGate,
    PyTypedPresenceReport,
    PyprojectHygieneReport,
    ReferencesDirectoryInventory,
    ReferencesGovernancePolicyReport,
    ReferencesLicenseBoundaryReport,
    ReleaseHygieneBlockingGatePolicy,
    ReleaseHygieneGateReport,
    ReleaseHygieneGateReportService,
    ReleaseTagReadinessReport,
    RepositoryGovernancePolicy,
    RepositoryGovernanceRemediationItem,
    RepositoryGovernanceRemediationPlan,
    RepositoryStateSnapshot,
    RootGovernanceFileReport,
    RuntimeArtifactTrackingReport,
    RuntimeDataHygieneReport,
    ThirdPartyNoticeReport,
    VersionConsistencyReport,
    V0281_EFFECT_TYPES,
    V0281_EVENT_TYPES,
    V0281_FORBIDDEN_EFFECT_TYPES,
    V0281_OBJECT_TYPES,
)


def _parts() -> dict:
    return ReleaseHygieneGateReportService().build_all_parts()


def test_release_hygiene_gate_models_build() -> None:
    parts = _parts()
    report = parts["report"]

    assert isinstance(parts["policy"], ReleaseHygieneBlockingGatePolicy)
    assert isinstance(parts["governance_policy"], RepositoryGovernancePolicy)
    assert isinstance(parts["snapshot"], RepositoryStateSnapshot)
    assert isinstance(parts["version"], VersionConsistencyReport)
    assert isinstance(parts["worktree"], CleanWorktreeReport)
    assert isinstance(parts["tag"], ReleaseTagReadinessReport)
    assert isinstance(parts["governance-files"], RootGovernanceFileReport)
    assert isinstance(parts["license"], LicensePresenceReport)
    assert isinstance(parts["changelog"], ChangelogPresenceReport)
    assert isinstance(parts["contributing"], ContributingPresenceReport)
    assert isinstance(parts["third-party"], ThirdPartyNoticeReport)
    assert isinstance(parts["pyproject"], PyprojectHygieneReport)
    assert isinstance(parts["py-typed"], PyTypedPresenceReport)
    assert isinstance(parts["ci"], CIWorkflowPresenceReport)
    assert isinstance(parts["gitignore"], GitignoreHygieneReport)
    assert isinstance(parts["data"], RuntimeDataHygieneReport)
    assert isinstance(parts["artifacts"], RuntimeArtifactTrackingReport)
    assert isinstance(parts["references"], ReferencesDirectoryInventory)
    assert isinstance(parts["references-license"], ReferencesLicenseBoundaryReport)
    assert isinstance(parts["references-policy"], ReferencesGovernancePolicyReport)
    assert isinstance(parts["forbidden-scan"], ForbiddenRepositoryArtifactScanReport)
    assert isinstance(parts["remediation"], RepositoryGovernanceRemediationPlan)
    assert isinstance(parts["remediation"].remediation_items[0], RepositoryGovernanceRemediationItem)
    assert isinstance(parts["no-release"], NoReleaseDecision)
    assert isinstance(parts["defer-alpha"], DeferAlphaDecision)
    assert isinstance(parts["release-claim"], PublicAlphaReleaseClaimGate)
    assert isinstance(report, ReleaseHygieneGateReport)


def test_gate_policy_governance_snapshot_and_readiness() -> None:
    parts = _parts()
    policy = parts["policy"]
    governance = parts["governance_policy"]
    snapshot = parts["snapshot"]
    report = parts["report"]

    assert policy.version == "v0.28.1"
    assert policy.layer == "public_alpha_schumpeter_preparation"
    assert policy.gate_type == "blocking_gate"
    assert policy.public_alpha_release_claim_requires_gate_pass is True
    assert policy.repository_release_ready_requires_gate_pass is True
    assert policy.hygiene_unknown_is_not_passed is True
    assert policy.failed_required_check_blocks_release is True
    assert policy.no_release_is_valid_outcome is True
    assert policy.defer_alpha_is_valid_outcome is True
    assert policy.auto_fix_enabled_now is False
    assert policy.release_tag_creation_enabled_now is False
    assert policy.package_publish_enabled_now is False
    assert policy.company_split_enabled_now is False
    assert policy.external_adapter_enabled_now is False
    assert policy.provider_invocation_enabled_now is False
    assert policy.command_execution_enabled_now is False
    assert {
        "version_consistency",
        "clean_worktree",
        "release_tag_policy",
        "license_presence",
        "changelog_presence",
        "third_party_notices_when_references_exist",
        "pyproject_hygiene",
        "py_typed_presence",
        "ci_workflow_presence",
        "gitignore_hygiene",
        "runtime_data_hygiene",
        "references_governance_policy",
        "forbidden_artifact_scan",
    } <= set(policy.required_checks)
    assert governance.license_required is True
    assert governance.changelog_required is True
    assert governance.third_party_notices_required_when_references_exist is True
    assert governance.references_policy_required_when_references_exist is True
    assert governance.auto_remediation_enabled_now is False
    assert snapshot.source_mode in {"file_metadata_readonly", "unknown"}
    assert snapshot.pyproject_ref is not None
    assert snapshot.gitignore_present in {True, False, None}
    assert report.ready_for_v0_28_2 is True
    assert report.ready_for_public_alpha_release_claim is False
    assert report.repository_release_ready is False
    assert report.package_distribution_ready is False
    assert report.public_alpha_ready is False


def test_hygiene_reports_surface_blockers_without_autofix() -> None:
    parts = _parts()

    assert parts["version"].expected_version == "0.28.1"
    assert parts["version"].versions_match is False
    assert parts["worktree"].worktree_status_known is False
    assert parts["worktree"].worktree_status == "unknown"
    assert parts["worktree"].blocks_release_claim is True
    assert parts["tag"].expected_tag == "v0.28.1"
    assert parts["tag"].release_tag_created_now is False
    assert parts["tag"].blocks_release_claim is True
    assert parts["license"].auto_license_created_now is False
    assert parts["changelog"].auto_changelog_created_now is False
    assert parts["third-party"].third_party_notices_required == parts["third-party"].references_dir_present
    assert parts["pyproject"].pytest_in_runtime_dependencies is True
    assert parts["pyproject"].blocks_release_claim is True
    assert parts["py-typed"].py_typed_present in {True, False}
    assert parts["ci"].github_workflows_dir_present in {True, False}
    assert parts["gitignore"].ignores_sqlite in {True, False, None}
    assert parts["data"].tracked_sqlite_count == 0
    assert parts["artifacts"].artifact_patterns_checked == [
        "*.sqlite",
        "*.db",
        "*.bak",
        "*.log",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "dist/",
        "build/",
        "*.egg-info",
    ]
    assert parts["references-license"].references_runtime_dependency_count == 0
    assert parts["references-license"].references_code_copy_count == 0
    assert parts["forbidden-scan"].scan_mode == "file_path_pattern_only"
    assert parts["forbidden-scan"].credential_like_artifact_count == 0
    assert parts["remediation"].auto_fix_performed is False
    assert parts["no-release"].public_alpha_release_claim_allowed is False
    assert parts["defer-alpha"].public_alpha_release_claim_allowed is False
    assert parts["release-claim"].public_alpha_release_claim_allowed is False


def test_release_hygiene_report_flags_ocel_pig_ocpx_and_cli(capsys) -> None:
    service = ReleaseHygieneGateReportService()
    parts = service.build_all_parts()
    report = parts["report"]
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert report.auto_fix_performed is False
    assert report.package_published is False
    assert report.release_tag_created is False
    assert report.public_alpha_release_implemented is False
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
    assert report.next_required_step == "v0.28.2 Packaging / Distribution / Type Boundary"
    assert "release_hygiene_gate_report" in V0281_OBJECT_TYPES
    assert "release_hygiene_gate_report_created" in V0281_EVENT_TYPES
    assert "release_hygiene_gate_evaluated" in V0281_EFFECT_TYPES
    assert "auto_fix_performed" in V0281_FORBIDDEN_EFFECT_TYPES
    assert pig["version"] == "v0.28.1"
    assert pig["subject"] == "release_hygiene_repository_governance_blocking_gate"
    assert ocpx["state"] == "release_hygiene_repository_governance_blocking_gate_evaluated"
    assert "ReleaseHygieneGateState" in ocpx["target_read_models"]

    for command in [
        "gate",
        "snapshot",
        "version",
        "worktree",
        "tag",
        "governance-files",
        "license",
        "changelog",
        "third-party",
        "pyproject",
        "py-typed",
        "ci",
        "gitignore",
        "data",
        "artifacts",
        "references",
        "forbidden-scan",
        "remediation",
        "release-claim",
        "report",
    ]:
        assert main(["alpha", "hygiene", command]) == 0
        output = capsys.readouterr().out
        assert "version=v0.28.1" in output
        assert "gate_type=blocking_gate" in output
        assert "ready_for_v0_28_2=true" in output
        assert "ready_for_public_alpha_release_claim=false" in output
        assert "repository_release_ready=false" in output
        assert "package_distribution_ready=false" in output
        assert "public_alpha_ready=false" in output
        assert "auto_fix_performed=false" in output
        assert "package_published=false" in output
        assert "release_tag_created=false" in output
        assert "provider_invoked=false" in output
        assert "command_executed=false" in output
        assert "llm_judge_used=false" in output
