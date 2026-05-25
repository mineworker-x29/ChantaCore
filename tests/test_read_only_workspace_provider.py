from pathlib import Path

from chanta_core.internal_provider import (
    WORKSPACE_PROVIDER_EFFECT_TYPES,
    WORKSPACE_PROVIDER_EVENT_TYPES,
    WORKSPACE_PROVIDER_OBJECT_TYPES,
    WORKSPACE_PROVIDER_RELATION_TYPES,
    ReadOnlyWorkspaceProviderService,
    WorkspaceIgnorePolicyService,
    WorkspacePathSanitizationService,
    WorkspaceReadFindingService,
    WorkspaceReadPolicyService,
    WorkspaceReadProviderSkillService,
    WorkspaceReadReportService,
    WorkspaceRootDescriptor,
    WorkspaceRootDiscoveryService,
    WorkspaceTreeRequest,
    WorkspaceTreeTraversalService,
)


def _workspace(tmp_path: Path) -> Path:
    (tmp_path / "src" / "pkg").mkdir(parents=True)
    (tmp_path / "tests").mkdir()
    (tmp_path / ".git").mkdir()
    (tmp_path / ".hidden").write_text("hidden", encoding="utf-8")
    (tmp_path / "src" / "pkg" / "module.py").write_text("print('not read')", encoding="utf-8")
    (tmp_path / "tests" / "test_module.py").write_text("def test_x(): pass", encoding="utf-8")
    (tmp_path / "README.md").write_text("# docs", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]", encoding="utf-8")
    (tmp_path / "token.txt").write_text("secret-looking name", encoding="utf-8")
    (tmp_path / ".git" / "config").write_text("ignored", encoding="utf-8")
    return tmp_path


def _service(root: Path) -> WorkspaceReadReportService:
    sanitizer = WorkspacePathSanitizationService()
    return WorkspaceReadReportService(
        root_service=WorkspaceRootDiscoveryService(workspace_root=root, sanitizer=sanitizer),
        sanitizer=sanitizer,
    )


def test_workspace_read_policy_ignore_and_sanitization_models_build(tmp_path):
    policy = WorkspaceReadPolicyService().build_policy()
    ignore = WorkspaceIgnorePolicyService().build_ignore_policy()
    sanitizer = WorkspacePathSanitizationService()
    request = WorkspaceTreeRequest(max_depth=3, max_entries=500)

    assert policy.version == "v0.24.2"
    assert policy.read_only is True
    assert policy.file_content_read_enabled is False
    assert policy.file_excerpt_read_enabled is False
    assert policy.repository_search_enabled is False
    assert policy.local_command_execution_enabled is False
    assert policy.follow_symlinks is False
    assert policy.include_hidden_files_default is False
    assert policy.include_ignored_files_default is False
    assert policy.max_depth_default > 0
    assert policy.max_entries_default > 0
    assert policy.private_path_sanitization_required is True
    assert policy.credential_path_masking_required is True
    assert policy.raw_secret_output_forbidden is True
    assert request.include_file_content is False
    assert request.include_file_excerpt is False

    for ignored in [".git", ".venv", "venv", "node_modules", "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache", "dist", "build"]:
        assert ignored in ignore.default_ignored_dirs
    for secret_pattern in [".env", "*.pem", "*.key", "id_rsa", "secrets.*", "credentials.*", "token*"]:
        assert secret_pattern in ignore.secret_like_patterns
    assert ignore.apply_before_output is True
    assert ignore.include_ignored_files is False
    assert sanitizer.build_policy().show_relative_paths_only is True
    assert sanitizer.sanitize_path("token.txt") == "[secret-like]"


def test_workspace_provider_declared_and_skill_activated():
    skills = {item["skill_id"]: item for item in WorkspaceReadProviderSkillService().list_skill_contracts()}

    assert skills["skill:workspace_read_provider_view"]["implemented"] is True
    assert skills["skill:workspace_read_provider_view"]["workspace_tree_metadata_only"] is True
    assert skills["skill:internal_provider_contract_view"]["implemented"] is True
    assert skills["skill:internal_provider_registry_view"]["implemented"] is True
    assert skills["skill:internal_provider_capability_surface_view"]["implemented"] is True
    for future_skill in [
        "skill:repository_search_provider_view",
        "skill:file_read_provider_view",
        "skill:local_runtime_command_candidate_create",
        "skill:bounded_local_command_run",
    ]:
        assert skills[future_skill]["stub"] is True
        assert skills[future_skill]["local_command_execution_enabled"] is False


def test_workspace_read_report_observes_tree_and_metadata_without_content(tmp_path):
    root = _workspace(tmp_path)
    report = _service(root).build_report(WorkspaceTreeRequest(max_depth=4, max_entries=100))

    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_24_3 is True
    assert report.ready_for_v0_25 is False
    assert report.provider_invocation_performed is True
    assert report.workspace_tree_observed is True
    assert report.workspace_metadata_observed is True
    assert report.file_content_read_performed is False
    assert report.file_excerpt_read_performed is False
    assert report.repository_search_performed is False
    assert report.local_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.24.3 Repository Search / File Read Provider"

    assert report.snapshot.version == "v0.24.2"
    assert report.snapshot.file_content_read_performed is False
    assert report.snapshot.repository_search_performed is False
    assert report.snapshot.local_command_executed is False
    assert report.snapshot.external_runtime_touched is False
    assert report.summary.raw_file_content_included is False
    assert report.summary.private_full_paths_included is False
    assert report.summary.extension_counts[".py"] >= 2
    assert report.summary.file_kind_counts["source"] >= 1
    assert report.summary.file_kind_counts["test"] >= 1
    assert report.summary.file_kind_counts["docs"] >= 1
    assert report.summary.file_kind_counts["config"] >= 1
    assert report.summary.secret_like_files_masked_count >= 1

    all_paths = [item.sanitized_path for item in report.snapshot.directories] + [
        item.sanitized_path for item in report.snapshot.files
    ]
    assert "src/pkg/module.py" in all_paths
    assert "token.txt" not in all_paths
    assert ".git/config" not in all_paths
    assert ".hidden" not in all_paths
    assert all(str(root) not in path for path in all_paths)
    assert all(item.file_content_read is False for item in report.snapshot.directories)
    assert all(item.file_content_read is False and item.file_excerpt_read is False for item in report.snapshot.files)
    assert all(item.private_full_path_output is False for item in report.snapshot.files)


def test_workspace_traversal_limits_hidden_ignored_and_symlink_policy(tmp_path):
    root = _workspace(tmp_path)
    (root / "a" / "b" / "c").mkdir(parents=True)
    (root / "a" / "b" / "c" / "deep.py").write_text("not read", encoding="utf-8")
    try:
        (root / "link_to_src").symlink_to(root / "src", target_is_directory=True)
    except OSError:
        pass

    depth_report = _service(root).build_report(WorkspaceTreeRequest(max_depth=1, max_entries=100))
    entry_report = _service(root).build_report(WorkspaceTreeRequest(max_depth=5, max_entries=2))

    assert depth_report.snapshot.truncated is True
    assert depth_report.snapshot.truncation_reason == "max_depth_exceeded"
    assert any(item.finding_type == "max_depth_exceeded" for item in depth_report.findings)
    assert entry_report.snapshot.truncated is True
    assert entry_report.snapshot.truncation_reason == "max_entries_exceeded"
    assert any(item.finding_type == "max_entries_exceeded" for item in entry_report.findings)
    assert any(item.finding_type == "ignored_path_skipped" for item in depth_report.findings + entry_report.findings)
    assert any(item.finding_type == "hidden_path_skipped" for item in depth_report.findings + entry_report.findings)
    assert any(item.symlink is False for item in depth_report.snapshot.directories)


def test_workspace_missing_root_strict_fails(tmp_path):
    missing = tmp_path / "missing"
    service = _service(missing)
    report = service.build_report(WorkspaceTreeRequest(strictness="strict"))

    assert report.report_status == "failed"
    assert report.ready_for_v0_24_3 is False
    assert any(item.finding_type in {"root_missing_or_unresolved", "root_not_allowed"} for item in report.findings)


def test_workspace_blocking_markers_and_content_requests_create_findings(tmp_path):
    root = _workspace(tmp_path)
    service = _service(root)
    report = service.build_report(
        WorkspaceTreeRequest(include_file_content=True, include_file_excerpt=True),
        markers=[
            "repository_search_attempted",
            "local_command_execution_attempted",
            "provider_api_call_performed",
            "external_runtime_touched",
            "credential_exposure",
            "raw_secret_output",
            "vendor_hardcoding",
            "growthkernel_dependency",
            "schumpeter_split",
            "general_agent_usability",
            "llm_judge",
        ],
    )
    finding_types = {item.finding_type for item in report.findings}

    assert report.report_status == "blocked"
    assert "file_content_read_attempted" in finding_types
    assert "file_excerpt_read_attempted" in finding_types
    assert "repository_search_attempted" in finding_types
    assert "local_command_execution_attempted" in finding_types
    assert "provider_api_call_performed" in finding_types
    assert "external_runtime_touched" in finding_types
    assert "credential_exposure_detected" in finding_types
    assert "raw_secret_output_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types
    assert "general_agent_usability_premature" in finding_types
    assert "llm_judge_detected" in finding_types


def test_workspace_ocel_pig_ocpx_projection_builds(tmp_path):
    root = _workspace(tmp_path)
    service = _service(root)
    report = service.build_report()
    pig = service.build_pig_report(report)
    ocpx = service.build_ocpx_projection()

    for object_type in [
        "workspace_read_provider_policy",
        "workspace_root_descriptor",
        "workspace_ignore_pattern",
        "workspace_ignore_policy",
        "workspace_path_sanitization_policy",
        "workspace_tree_request",
        "workspace_directory_node",
        "workspace_file_metadata",
        "workspace_tree_snapshot",
        "workspace_metadata_summary",
        "workspace_read_finding",
        "workspace_read_report",
    ]:
        assert object_type in WORKSPACE_PROVIDER_OBJECT_TYPES
    for event_type in ["workspace_read_requested", "workspace_tree_snapshot_created", "workspace_read_report_created"]:
        assert event_type in WORKSPACE_PROVIDER_EVENT_TYPES
    for relation_type in ["not_file_content_read", "not_repository_searched", "derived_from_internal_provider_registry"]:
        assert relation_type in WORKSPACE_PROVIDER_RELATION_TYPES
    assert WORKSPACE_PROVIDER_EFFECT_TYPES == [
        "read_only_observation",
        "workspace_tree_observed",
        "workspace_metadata_observed",
        "state_candidate_created",
    ]
    assert pig["version"] == "v0.24.2"
    assert pig["layer"] == "internal_provider"
    assert pig["subject"] == "read_only_workspace_provider"
    assert pig["safety_boundary"]["workspace_tree_observed"] is True
    assert pig["safety_boundary"]["workspace_metadata_observed"] is True
    assert pig["safety_boundary"]["file_content_read_performed"] is False
    assert pig["safety_boundary"]["repository_search_performed"] is False
    assert pig["safety_boundary"]["private_full_paths_included"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "workspace_tree_metadata_observed"
    assert "WorkspaceReadProviderState" in ocpx["target_read_models"]
    assert "WorkspaceTreeState" in ocpx["target_read_models"]
    assert "WorkspaceMetadataState" in ocpx["target_read_models"]


def test_read_only_workspace_provider_service_observes_workspace(tmp_path):
    root = _workspace(tmp_path)
    report_service = _service(root)
    provider = ReadOnlyWorkspaceProviderService(report_service=report_service)
    report = provider.observe_workspace(WorkspaceTreeRequest(max_depth=2))

    assert report.version == "v0.24.2"
    assert report.snapshot.policy.provider_id == "workspace_read_provider"
    assert report.snapshot.policy.read_only is True
