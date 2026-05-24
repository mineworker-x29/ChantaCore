from contextlib import redirect_stdout
from io import StringIO

from chanta_core.cli.main import main
from chanta_core.internal_provider import InternalProviderContractReportService


def test_contract_report_blocks_on_dangerous_markers():
    service = InternalProviderContractReportService()
    marker_to_count = {
        "workspace_file_read_execution": "workspace_file_read_execution_count",
        "repository_search_execution": "repository_search_execution_count",
        "file_content_extraction": "file_content_extraction_count",
        "local_command_execution": "local_command_execution_count",
        "bounded_local_command_execution": "bounded_local_command_execution_count",
        "unrestricted_shell": "unrestricted_shell_count",
        "network_access": "network_access_count",
        "package_install": "package_install_count",
        "destructive_command": "destructive_command_count",
        "credential_exposure": "credential_exposure_count",
        "raw_secret_output": "raw_secret_output_count",
        "external_provider_adapter": "external_provider_adapter_count",
        "schumpeter_split": "schumpeter_split_count",
        "llm_judge": "llm_judge_count",
    }

    for marker, count_field in marker_to_count.items():
        report = service.build_report([marker])
        assert report.report_status == "blocked"
        assert report.ready_for_v0_24_1 is False
        assert getattr(report.contract.safety_boundary, count_field) == 1


def test_no_non_goal_execution_flags_are_enabled():
    report = InternalProviderContractReportService().build_report()
    boundary = report.contract.invocation_boundary
    safety = report.contract.safety_boundary

    assert report.provider_invocation_enabled is False
    assert report.workspace_read_execution_enabled is False
    assert report.repository_search_execution_enabled is False
    assert report.local_runtime_execution_enabled is False
    assert report.local_command_execution_enabled is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False

    assert boundary.invocation_enabled_v0_24_0 is False
    assert boundary.workspace_read_execution_enabled_v0_24_0 is False
    assert boundary.repository_search_execution_enabled_v0_24_0 is False
    assert boundary.file_read_execution_enabled_v0_24_0 is False
    assert boundary.ocel_inspection_execution_enabled_v0_24_0 is False
    assert boundary.local_runtime_execution_enabled_v0_24_0 is False
    assert boundary.local_command_execution_enabled_v0_24_0 is False
    assert boundary.external_provider_invocation_enabled is False
    assert boundary.shell_execution_enabled is False
    assert boundary.network_enabled is False
    assert boundary.mcp_enabled is False
    assert boundary.plugin_enabled is False
    assert boundary.llm_judge_enabled is False

    assert safety.provider_invocation_count == 0
    assert safety.workspace_file_read_execution_count == 0
    assert safety.repository_search_execution_count == 0
    assert safety.file_content_extraction_count == 0
    assert safety.local_command_execution_count == 0
    assert safety.bounded_local_command_execution_count == 0
    assert safety.unrestricted_shell_count == 0
    assert safety.network_access_count == 0
    assert safety.package_install_count == 0
    assert safety.destructive_command_count == 0
    assert safety.credential_exposure_count == 0
    assert safety.raw_secret_output_count == 0


def test_cli_provider_contract_views_work_and_are_sanitized():
    commands = [
        ["provider", "contract"],
        ["provider", "types"],
        ["provider", "effect-policy"],
        ["provider", "permission-policy"],
        ["provider", "invocation-boundary"],
        ["provider", "observability"],
        ["provider", "safety-boundary"],
        ["provider", "roadmap-boundary"],
    ]

    for command in commands:
        buffer = StringIO()
        with redirect_stdout(buffer):
            exit_code = main(command)
        output = buffer.getvalue()

        assert exit_code == 0
        assert "version=v0.24.0" in output
        assert "layer=internal_provider" in output
        assert "status=contract_only" in output
        assert "provider_invocation_enabled=False" in output
        assert "workspace_read_execution_enabled=False" in output
        assert "repository_search_execution_enabled=False" in output
        assert "local_runtime_execution_enabled=False" in output
        assert "local_command_execution_enabled=False" in output
        assert "external_provider_adapter_implemented=False" in output
        assert "schumpeter_split_introduced=False" in output
        assert "ready_for_v0_24_1=True" in output
        assert "ready_for_v0_25=False" in output
        assert "next_required_step=v0.24.1 Provider Registry & Capability Surface" in output
        assert "credential_value" not in output
        assert "raw_secret" not in output
        assert "D:\\" not in output


def test_cli_contract_summary_contains_track_and_status():
    buffer = StringIO()
    with redirect_stdout(buffer):
        exit_code = main(["provider", "contract"])

    output = buffer.getvalue()
    assert exit_code == 0
    assert "Internal Provider Contract" in output
    assert "version_name=Internal Provider Contract" in output
    assert "release_track=Internal Provider / Local Runtime Provider" in output
    assert "report_status=passed" in output
