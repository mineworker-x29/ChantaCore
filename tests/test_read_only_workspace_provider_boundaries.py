from contextlib import redirect_stdout
from io import StringIO

from chanta_core.cli.main import main
from chanta_core.internal_provider import WorkspaceReadReportService, WorkspaceTreeRequest


def _run_cli(command: list[str]) -> str:
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(command)
    assert exit_code == 0
    return buffer.getvalue()


def test_workspace_provider_boundary_flags_are_false():
    report = WorkspaceReadReportService().build_report(WorkspaceTreeRequest(max_depth=1, max_entries=20))

    assert report.file_content_read_performed is False
    assert report.file_excerpt_read_performed is False
    assert report.repository_search_performed is False
    assert report.local_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.summary.private_full_paths_included is False
    for item in report.snapshot.files:
        assert item.file_content_read is False
        assert item.file_excerpt_read is False
        assert item.raw_secret_output is False
        assert item.private_full_path_output is False


def test_workspace_cli_outputs_sanitized_boundary_fields():
    commands = [
        ["provider", "workspace", "roots"],
        ["provider", "workspace", "tree", "--max-depth", "1", "--max-entries", "20"],
        ["provider", "workspace", "metadata", "--max-depth", "1", "--max-entries", "20"],
        ["provider", "workspace", "summary", "--max-depth", "1", "--max-entries", "20"],
        ["provider", "workspace", "report", "--max-depth", "1", "--max-entries", "20"],
        ["provider", "workspace", "findings", "--max-depth", "1", "--max-entries", "20"],
    ]

    for command in commands:
        output = _run_cli(command)
        assert "version=v0.24.2" in output
        assert "provider=workspace_read_provider" in output
        assert "read_only=true" in output
        assert "file_content_read_performed=False" in output
        assert "file_excerpt_read_performed=False" in output
        assert "repository_search_performed=False" in output
        assert "local_command_executed=False" in output
        assert "external_runtime_touched=False" in output
        assert "credential_exposed=False" in output
        assert "raw_secret_output=False" in output
        assert "private_full_paths_included=False" in output
        assert "ready_for_v0_24_3=" in output
        assert "ready_for_v0_25=False" in output
        assert "next_required_step=v0.24.3 Repository Search / File Read Provider" in output
        assert "credential_value" not in output
        assert "raw secrets" not in output
        assert "ChantaResearchGroup" + "_Members" not in output


def test_workspace_docs_record_identity_and_non_goals():
    text = open("docs/versions/v0.24/v0.24.2_read_only_workspace_provider.md", encoding="utf-8").read()

    assert "Read-only Workspace Provider" in text
    assert "읽기 전용 워크스페이스 Provider" in text
    assert "Track: Internal Provider / Local Runtime Provider" in text
    assert "Workspace provider is read-only" in text
    assert "Workspace tree observation is not file content reading" in text
    assert "File metadata is not file content" in text
    assert "v0.24.3 Repository Search / File Read Provider" in text
    assert "file_content_read=True" not in text
    assert "repository_search_performed=True" not in text
    assert "local_command_executed=True" not in text


def test_workspace_provider_changed_surface_has_no_vendor_or_private_material():
    sources = [
        open("src/chanta_core/internal_provider/workspace_provider.py", encoding="utf-8").read(),
        open("docs/versions/v0.24/v0.24.2_read_only_workspace_provider.md", encoding="utf-8").read(),
    ]
    combined = "\n".join(sources)

    assert "Ve" + "ra material" not in combined
    for vendor in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert vendor not in combined
    for token in [
        "file_content_extracted=True",
        "file_content_read=True",
        "file_content_read_performed=True",
        "file_excerpt_read=True",
        "file_excerpt_read_performed=True",
        "repository_search_executed=True",
        "repository_search_performed=True",
        "local_command_candidate_created=True",
        "local_command_executed=True",
        "local_command_execution_enabled=True",
        "bounded_local_command_executed=True",
        "external_provider_adapter_implemented=True",
        "external_runtime_touched=True",
        "credential_exposed=True",
        "raw_secret_output=True",
        "private_full_path_output=True",
        "private_full_paths_included=True",
        "network_enabled=True",
        "growthkernel_dependency_required=True",
    ]:
        assert token not in combined
