from pathlib import Path

from chanta_core.internal_provider import (
    REPOSITORY_FILE_PROVIDER_FORBIDDEN_EFFECT_TYPES,
    FileReadReportService,
    FileReadRequest,
    RepositoryFileProviderFindingService,
    RepositoryProviderPolicyService,
    RepositorySearchReportService,
    RepositorySearchRequest,
)


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "code.py").write_text("def provider():\n    return 'ok'\n", encoding="utf-8")
    return root


def test_forbidden_effects_are_declared_but_not_emitted() -> None:
    for effect in [
        "unrestricted_file_read",
        "full_repository_dump",
        "raw_binary_output",
        "raw_secret_output",
        "file_written",
        "file_edited",
        "file_deleted",
        "repository_mutated",
        "local_command_candidate_created",
        "local_command_executed",
        "bounded_local_command_executed",
        "external_runtime_touched",
        "external_control_dispatched",
        "credential_exposed",
        "external_provider_called",
    ]:
        assert effect in REPOSITORY_FILE_PROVIDER_FORBIDDEN_EFFECT_TYPES


def test_marker_findings_block_dangerous_boundaries() -> None:
    service = RepositoryFileProviderFindingService()
    policy = RepositoryProviderPolicyService().build_search_policy()
    findings = service.build_findings(
        None,
        policy,
        markers=[
            "unrestricted_file_read",
            "full_repository_dump",
            "file_write",
            "file_edit",
            "file_delete",
            "repository_mutation",
            "local_command_execution",
            "provider_api_call",
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
    finding_types = {item.finding_type for item in findings}

    assert "unrestricted_file_read_attempted" in finding_types
    assert "full_repository_dump_attempted" in finding_types
    assert "file_write_attempted" in finding_types
    assert "file_edit_attempted" in finding_types
    assert "file_delete_attempted" in finding_types
    assert "repository_mutation_attempted" in finding_types
    assert "local_command_execution_attempted" in finding_types
    assert "provider_api_call_performed" in finding_types
    assert "external_runtime_touched" in finding_types
    assert "credential_exposure_detected" in finding_types
    assert "raw_secret_output_blocked" in finding_types
    assert "vendor_hardcoding_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types
    assert "general_agent_usability_premature" in finding_types
    assert "llm_judge_detected" in finding_types
    assert all(item.severity in {"critical", "error"} for item in findings)


def test_search_report_blocks_marker_violations(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    report = RepositorySearchReportService(workspace_root=root).build_report(
        RepositorySearchRequest(query_text="provider", search_mode="text"),
        markers=["full_repository_dump", "local_command_execution"],
    )

    assert report.report_status == "blocked"
    assert report.unrestricted_file_read_performed is False
    assert report.full_repository_dump_performed is False
    assert report.local_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False


def test_file_read_blocks_raw_content_request(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    report = FileReadReportService(workspace_root=root).build_report(
        FileReadRequest(relative_path="code.py", read_mode="excerpt", include_raw_content=True)
    )

    assert report.report_status == "blocked"
    assert any(item.finding_type == "unrestricted_file_read_attempted" for item in report.findings)
    assert report.bounded_file_read_performed is False
    assert report.file_excerpt_read_performed is False
    assert report.unrestricted_file_read_performed is False
    assert report.full_file_dump_performed is False
    assert report.binary_raw_output_performed is False
    assert report.file_write_performed is False
    assert report.file_edit_performed is False
    assert report.file_delete_performed is False
    assert report.local_command_executed is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.private_full_paths_included is False


def test_file_read_blocks_invalid_window(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    report = FileReadReportService(workspace_root=root).build_report(
        FileReadRequest(relative_path="code.py", read_mode="excerpt", start_line=10, end_line=1)
    )

    assert report.report_status == "failed"
    assert any(item.finding_type == "unrestricted_file_read_attempted" for item in report.findings)


def test_no_private_full_path_in_search_or_file_report(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    search = RepositorySearchReportService(workspace_root=root).build_report(
        RepositorySearchRequest(query_text="provider", search_mode="text")
    )
    read = FileReadReportService(workspace_root=root).build_report(
        FileReadRequest(relative_path="code.py", read_mode="excerpt")
    )
    rendered_search = RepositorySearchReportService(workspace_root=root).render_report_cli(search)
    rendered_read = FileReadReportService(workspace_root=root).render_report_cli(read, section="excerpt")

    assert str(root) not in rendered_search
    assert str(root) not in rendered_read
    assert "private_full_paths_included=false" in rendered_search
    assert "private_full_paths_included=false" in rendered_read


def test_no_external_or_local_runtime_flags_are_set(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    search = RepositorySearchReportService(workspace_root=root).build_report(
        RepositorySearchRequest(query_text="provider", search_mode="mixed")
    )
    read = FileReadReportService(workspace_root=root).build_report(
        FileReadRequest(relative_path="code.py", read_mode="bounded_file", max_lines=1)
    )

    assert search.local_command_executed is False
    assert search.external_provider_adapter_implemented is False
    assert search.ready_for_v0_25 is False
    assert read.local_command_executed is False
    assert read.file_write_performed is False
    assert read.file_edit_performed is False
    assert read.file_delete_performed is False
    assert read.llm_judge_used is False
