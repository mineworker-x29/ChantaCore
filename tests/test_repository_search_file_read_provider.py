from pathlib import Path

from chanta_core.internal_provider import (
    FILE_READ_PROVIDER_ID,
    REPOSITORY_FILE_PROVIDER_EFFECT_TYPES,
    REPOSITORY_FILE_PROVIDER_EVENT_TYPES,
    REPOSITORY_FILE_PROVIDER_OBJECT_TYPES,
    REPOSITORY_FILE_PROVIDER_RELATION_TYPES,
    REPOSITORY_FILE_PROVIDER_VERSION,
    REPOSITORY_SEARCH_PROVIDER_ID,
    FileReadPolicy,
    FileReadPolicyService,
    FileReadReportService,
    FileReadRequest,
    FileReadSanitizationReport,
    FileReadWindowService,
    RepositoryFileProviderReportService,
    RepositoryFileProviderService,
    RepositoryFileProviderSkillService,
    RepositoryProviderPolicy,
    RepositoryProviderPolicyService,
    RepositorySearchQueryService,
    RepositorySearchReportService,
    RepositorySearchRequest,
    RepositorySearchScope,
    RepositorySearchScopeService,
)
from chanta_core.cli.main import main
from chanta_core.internal_provider.registry import InternalProviderRegistryReportService


def _repo(tmp_path: Path) -> Path:
    root = tmp_path / "repo"
    root.mkdir()
    (root / "src").mkdir()
    (root / "src" / "provider_core.py").write_text(
        "class InternalProvider:\n"
        "    def search_provider(self):\n"
        "        return 'provider'\n"
        "TOKEN_EXAMPLE=secret-value\n",
        encoding="utf-8",
    )
    (root / "README.md").write_text("# Provider\nRepository provider docs\n", encoding="utf-8")
    (root / ".hidden.py").write_text("provider hidden\n", encoding="utf-8")
    (root / ".env").write_text("TOKEN_EXAMPLE=secret-value\n", encoding="utf-8")
    (root / "image.png").write_bytes(b"\x89PNG\x00")
    return root


def test_repository_provider_policy_builds() -> None:
    policy = RepositoryProviderPolicyService().build_search_policy()

    assert isinstance(policy, RepositoryProviderPolicy)
    assert policy.version == REPOSITORY_FILE_PROVIDER_VERSION
    assert policy.provider_id == REPOSITORY_SEARCH_PROVIDER_ID
    assert policy.read_only is True
    assert policy.file_name_search_enabled is True
    assert policy.text_search_enabled is True
    assert policy.symbol_search_enabled is True
    assert policy.full_repository_dump_enabled is False
    assert policy.unrestricted_file_read_enabled is False
    assert policy.file_write_enabled is False
    assert policy.file_edit_enabled is False
    assert policy.file_delete_enabled is False
    assert policy.local_command_execution_enabled is False
    assert policy.follow_symlinks is False
    assert policy.include_hidden_files_default is False
    assert policy.include_ignored_files_default is False
    assert policy.max_files_scanned_default > 0
    assert policy.max_matches_default > 0
    assert policy.max_match_context_lines_default > 0
    assert policy.max_output_chars_default > 0
    assert policy.binary_file_scan_enabled is False
    assert policy.secret_redaction_required is True
    assert policy.private_path_sanitization_required is True
    assert policy.raw_secret_output_forbidden is True


def test_search_scope_and_query_build(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    policy = RepositoryProviderPolicyService().build_search_policy()
    request = RepositorySearchRequest(query_text=" InternalProvider ", search_mode="symbol", max_matches=5)
    scope = RepositorySearchScopeService(root).build_scope(request, None, policy)
    query = RepositorySearchQueryService().build_query(request)

    assert isinstance(scope, RepositorySearchScope)
    assert scope.root_ids
    assert "*" in scope.include_globs
    assert "**/*" in scope.include_globs
    assert ".png" in scope.denied_extensions
    assert scope.include_hidden_files is False
    assert scope.include_ignored_files is False
    assert scope.follow_symlinks is False
    assert scope.max_files_scanned == policy.max_files_scanned_default
    assert scope.max_matches == 5
    assert query.normalized_query_text == "InternalProvider"
    assert query.regex_enabled is False
    assert query.literal_search is True
    assert query.query_status == "ready"


def test_provider_surfaces_declared_in_v0_24_1_registry() -> None:
    report = InternalProviderRegistryReportService().build_report()
    provider_ids = {ref.provider_id for ref in report.registry.provider_refs}
    provider_types = {ref.provider_type for ref in report.registry.provider_refs}

    assert any(item.endswith(REPOSITORY_SEARCH_PROVIDER_ID) for item in provider_ids)
    assert any(item.endswith(FILE_READ_PROVIDER_ID) for item in provider_ids)
    assert REPOSITORY_SEARCH_PROVIDER_ID in provider_types
    assert FILE_READ_PROVIDER_ID in provider_types


def test_repository_file_provider_skills_are_implemented_without_local_execution() -> None:
    skills = {item["skill_id"]: item for item in RepositoryFileProviderSkillService().list_skill_contracts()}

    assert skills["skill:repository_search_provider_view"]["status"] == "implemented"
    assert skills["skill:file_read_provider_view"]["status"] == "implemented"
    assert skills["skill:repository_search_provider_view"]["read_only"] is True
    assert skills["skill:file_read_provider_view"]["read_only"] is True
    assert skills["skill:repository_search_provider_view"]["local_command_execution_enabled"] is False
    assert skills["skill:file_read_provider_view"]["external_provider_invocation_enabled"] is False
    assert skills["skill:local_runtime_command_candidate_create"]["status"] == "contract_only"


def test_file_name_text_symbol_search_are_bounded_and_sanitized(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    service = RepositorySearchReportService(workspace_root=root)

    file_name = service.build_report(RepositorySearchRequest(query_text="provider_core", search_mode="file_name", max_matches=10))
    text = service.build_report(RepositorySearchRequest(query_text="provider", search_mode="text", max_matches=10))
    symbol = service.build_report(RepositorySearchRequest(query_text="InternalProvider", search_mode="symbol", max_matches=10))

    assert file_name.report_status in {"passed", "warning"}
    assert text.report_status in {"passed", "warning"}
    assert symbol.report_status in {"passed", "warning"}
    assert any(match.match_type == "file_name" for match in file_name.result.matches)
    assert any(match.match_type == "text" for match in text.result.matches)
    assert any(match.match_type == "symbol" for match in symbol.result.matches)
    for report in [file_name, text, symbol]:
        assert report.repository_search_performed is True
        assert report.unrestricted_file_read_performed is False
        assert report.full_repository_dump_performed is False
        assert report.local_command_executed is False
        assert report.raw_secret_output is False
        assert report.private_full_paths_included is False
        for match in report.result.matches:
            assert str(root) not in match.sanitized_path
            assert match.private_full_path_output is False
            assert match.raw_secret_output is False


def test_search_limits_hidden_ignored_binary_and_redaction(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    service = RepositorySearchReportService(workspace_root=root)
    limited = service.build_report(RepositorySearchRequest(query_text="provider", search_mode="mixed", max_matches=1))
    all_scan = service.build_report(RepositorySearchRequest(query_text="does-not-match", search_mode="mixed", max_matches=10))
    secret = service.build_report(RepositorySearchRequest(query_text="TOKEN_EXAMPLE", search_mode="text", max_matches=10))

    assert limited.result.truncated is True
    assert limited.result.truncation_reason in {"max_matches_exceeded", "max_output_chars_exceeded"}
    assert all_scan.result.binary_skipped_count >= 1
    assert all_scan.result.ignored_file_count >= 1
    assert secret.result.redacted_match_count >= 1
    assert "[REDACTED]" in "\n".join(match.matched_line or "" for match in secret.result.matches)
    assert "secret-value" not in "\n".join(match.matched_line or "" for match in secret.result.matches)


def test_file_read_policy_and_window_build() -> None:
    policy = FileReadPolicyService().build_file_read_policy()
    window = FileReadWindowService().build_window(
        FileReadRequest(relative_path="README.md", read_mode="excerpt", max_lines=5, max_bytes=100),
        policy,
    )

    assert isinstance(policy, FileReadPolicy)
    assert policy.provider_id == FILE_READ_PROVIDER_ID
    assert policy.read_only is True
    assert policy.bounded_file_read_enabled is True
    assert policy.file_excerpt_read_enabled is True
    assert policy.unrestricted_file_read_enabled is False
    assert policy.full_file_dump_enabled is False
    assert policy.binary_raw_output_enabled is False
    assert policy.file_write_enabled is False
    assert policy.file_edit_enabled is False
    assert policy.file_delete_enabled is False
    assert policy.max_bytes_per_read_default > 0
    assert policy.max_lines_per_read_default > 0
    assert policy.max_file_size_readable_default > 0
    assert window.bounded is True
    assert window.window_status == "ready"


def test_file_excerpt_and_bounded_file_read_are_sanitized(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    service = FileReadReportService(workspace_root=root)

    excerpt = service.build_report(FileReadRequest(relative_path="src/provider_core.py", read_mode="excerpt", start_line=1, end_line=4))
    bounded = service.build_report(FileReadRequest(relative_path="src/provider_core.py", read_mode="bounded_file", max_lines=2))

    assert excerpt.report_status in {"passed", "warning"}
    assert bounded.report_status in {"passed", "warning"}
    assert excerpt.file_excerpt_read_performed is True
    assert bounded.bounded_file_read_performed is True
    assert excerpt.unrestricted_file_read_performed is False
    assert bounded.full_file_dump_performed is False
    assert excerpt.file_write_performed is False
    assert excerpt.file_edit_performed is False
    assert excerpt.file_delete_performed is False
    assert excerpt.local_command_executed is False
    assert excerpt.raw_secret_output is False
    assert excerpt.private_full_paths_included is False
    assert excerpt.excerpt is not None
    assert "secret-value" not in "\n".join(excerpt.excerpt.content_lines)
    assert isinstance(excerpt.sanitization_report, FileReadSanitizationReport)


def test_binary_and_outside_path_are_blocked(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    service = FileReadReportService(workspace_root=root)

    binary_report = service.build_report(FileReadRequest(relative_path="image.png", read_mode="excerpt"))
    outside_report = service.build_report(FileReadRequest(relative_path="../outside.txt", read_mode="excerpt"))

    assert binary_report.report_status == "failed"
    assert any(item.finding_type == "binary_raw_output_blocked" for item in binary_report.findings)
    assert outside_report.report_status == "blocked"
    assert any(item.finding_type == "path_outside_workspace" for item in outside_report.findings)


def test_repository_file_provider_report_pig_and_ocpx(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    search = RepositorySearchReportService(workspace_root=root).build_report(
        RepositorySearchRequest(query_text="provider", search_mode="text", max_matches=5)
    )
    read = FileReadReportService(workspace_root=root).build_report(
        FileReadRequest(relative_path="README.md", read_mode="excerpt", max_lines=5)
    )
    service = RepositoryFileProviderReportService()
    combined = service.build_combined_report([search], [read])
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert combined.report_status in {"passed", "warning"}
    assert combined.ready_for_v0_24_4 is True
    assert combined.ready_for_v0_25 is False
    assert combined.repository_search_performed is True
    assert combined.file_excerpt_read_performed is True
    assert combined.unrestricted_file_read_performed is False
    assert combined.full_repository_dump_performed is False
    assert combined.file_write_performed is False
    assert combined.file_edit_performed is False
    assert combined.file_delete_performed is False
    assert combined.local_command_executed is False
    assert combined.external_provider_adapter_implemented is False
    assert combined.credential_exposed is False
    assert combined.raw_secret_output is False
    assert combined.private_full_paths_included is False
    assert combined.llm_judge_used is False
    assert pig["version"] == REPOSITORY_FILE_PROVIDER_VERSION
    assert pig["subject"] == "repository_search_file_read_provider"
    assert pig["safety_boundary"]["full_repository_dump_performed"] is False
    assert ocpx["state"] == "repository_search_file_read_enabled"
    assert "RepositorySearchProviderState" in ocpx["target_read_models"]
    assert "FileReadExcerptState" in ocpx["target_read_models"]


def test_ocel_mapping_exists() -> None:
    for object_type in [
        "repository_provider_policy",
        "repository_search_scope",
        "repository_search_request",
        "repository_search_query",
        "repository_search_match",
        "repository_search_result",
        "repository_search_report",
        "file_read_policy",
        "file_read_request",
        "file_read_window",
        "file_read_excerpt",
        "file_read_sanitization_report",
        "file_read_report",
        "repository_file_provider_finding",
        "repository_file_provider_report",
        "workspace_tree_snapshot",
    ]:
        assert object_type in REPOSITORY_FILE_PROVIDER_OBJECT_TYPES
    for event_type in [
        "repository_search_requested",
        "repository_file_name_search_performed",
        "repository_text_search_performed",
        "repository_symbol_search_performed",
        "file_excerpt_read",
        "bounded_file_read",
        "repository_file_provider_blocked",
    ]:
        assert event_type in REPOSITORY_FILE_PROVIDER_EVENT_TYPES
    for relation_type in [
        "uses_repository_search_provider",
        "uses_file_read_provider",
        "redacts_secret_like_content",
        "blocks_binary_raw_output",
        "not_unrestricted_file_read",
        "not_full_repository_dump",
        "not_file_written",
        "not_local_command_executed",
    ]:
        assert relation_type in REPOSITORY_FILE_PROVIDER_RELATION_TYPES
    for effect_type in [
        "read_only_observation",
        "repository_search_performed",
        "file_excerpt_read",
        "bounded_file_read",
        "repository_match_observed",
        "state_candidate_created",
    ]:
        assert effect_type in REPOSITORY_FILE_PROVIDER_EFFECT_TYPES


def test_cli_provider_repo_and_file_commands() -> None:
    assert main(["provider", "repo", "search", "--query", "provider", "--mode", "file_name", "--max-matches", "5"]) == 0
    assert main(["provider", "repo", "report"]) == 0
    assert main(["provider", "repo", "findings"]) == 0
    assert main(["provider", "file", "excerpt", "--path", "README.md", "--max-lines", "5"]) == 0
    assert main(["provider", "file", "read", "--path", "README.md", "--start-line", "1", "--end-line", "5"]) == 0
    assert main(["provider", "file", "report"]) == 0


def test_repository_file_provider_service_facade(tmp_path: Path) -> None:
    root = _repo(tmp_path)
    service = RepositoryFileProviderService(workspace_root=root)

    search = service.search_repository(RepositorySearchRequest(query_text="provider", search_mode="text", max_matches=5))
    read = service.read_file(FileReadRequest(relative_path="README.md", read_mode="excerpt", max_lines=2))

    assert search.repository_search_performed is True
    assert read.file_excerpt_read_performed is True
