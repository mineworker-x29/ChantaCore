from contextlib import redirect_stdout
from io import StringIO

from chanta_core.internal_provider import InternalProviderRegistryReportService
from chanta_core.cli.main import main


def test_registry_report_never_enables_execution_surfaces():
    report = InternalProviderRegistryReportService().build_report()

    assert report.provider_invocation_enabled is False
    assert report.workspace_read_execution_enabled is False
    assert report.repository_search_execution_enabled is False
    assert report.file_read_execution_enabled is False
    assert report.local_runtime_execution_enabled is False
    assert report.local_command_execution_enabled is False
    assert report.external_provider_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    for ref in report.registry.provider_refs:
        assert ref.provider_invocation_enabled is False
        assert ref.workspace_file_read_execution_enabled is False
        assert ref.repository_search_execution_enabled is False
        assert ref.local_command_execution_enabled is False
    for surface in report.registry.capability_surfaces:
        assert surface.invocation_enabled is False
        assert surface.execution_enabled is False
        assert surface.read_execution_enabled is False
        for capability in surface.capabilities:
            assert capability.invocation_enabled is False
            assert "provider_invoked" in capability.forbidden_effect_types
            assert "workspace_file_read_executed" in capability.forbidden_effect_types
            assert "repository_search_executed" in capability.forbidden_effect_types
            assert "file_content_extracted" in capability.forbidden_effect_types
            assert "local_command_candidate_created" in capability.forbidden_effect_types
            assert "local_command_executed" in capability.forbidden_effect_types
            assert "bounded_local_command_executed" in capability.forbidden_effect_types


def test_registry_cli_outputs_sanitized_boundary_fields():
    commands = [
        ["provider", "registry"],
        ["provider", "registry", "snapshot"],
        ["provider", "registry", "report"],
        ["provider", "list"],
        ["provider", "surfaces"],
        ["provider", "surface", "--provider-id", "internal_provider:workspace_read_provider"],
        ["provider", "capabilities", "--provider-id", "internal_provider:workspace_read_provider"],
        ["provider", "status"],
    ]

    for command in commands:
        buffer = StringIO()
        with redirect_stdout(buffer):
            exit_code = main(command)
        output = buffer.getvalue()
        assert exit_code == 0
        assert "version=v0.24.1" in output
        assert "layer=internal_provider" in output
        assert "provider_count=" in output
        assert "capability_count=" in output
        assert "invocation_enabled=False" in output
        assert "execution_enabled=False" in output
        assert "workspace_read_execution_enabled=False" in output
        assert "repository_search_execution_enabled=False" in output
        assert "file_read_execution_enabled=False" in output
        assert "local_runtime_execution_enabled=False" in output
        assert "local_command_execution_enabled=False" in output
        assert "external_provider_adapter_implemented=False" in output
        assert "schumpeter_split_introduced=False" in output
        assert "ready_for_v0_24_2=True" in output
        assert "ready_for_v0_25=False" in output
        assert "next_required_step=v0.24.2 Read-only Workspace Provider" in output
        assert "raw secrets" not in output
        assert "credential_value" not in output
        assert "ChantaResearchGroup" + "_Members" not in output

    workspace_capability_output = StringIO()
    with redirect_stdout(workspace_capability_output):
        exit_code = main(["provider", "capabilities", "--provider-id", "internal_provider:workspace_read_provider"])
    assert exit_code == 0
    workspace_capability_text = workspace_capability_output.getvalue()
    assert "capability:list_workspace_roots" in workspace_capability_text
    assert "capability:search_text_future" not in workspace_capability_text


def test_registry_docs_record_identity_and_non_goals():
    text = open("docs/versions/v0.24/v0.24.1_provider_registry_capability_surface.md", encoding="utf-8").read()

    assert "Provider Registry & Capability Surface" in text
    assert "Provider 레지스트리·Capability 표면" in text
    assert "Track: Internal Provider / Local Runtime Provider" in text
    assert "Provider registry is not provider invocation" in text
    assert "Capability surface is not capability execution" in text
    assert "Provider registration is not workspace read" in text
    assert "Provider registration is not repository search" in text
    assert "Provider registration is not local runtime execution" in text
    assert "v0.24.2 Read-only Workspace Provider" in text
    assert "provider_invoked=True" not in text
    assert "credential values, raw secrets, or private full paths" in text


def test_no_private_or_vendor_runtime_material_in_registry_source_or_docs():
    combined = (
        open("src/chanta_core/internal_provider/registry.py", encoding="utf-8").read()
        + open("docs/versions/v0.24/v0.24.1_provider_registry_capability_surface.md", encoding="utf-8").read()
    )

    assert "ChantaResearchGroup" + "_Members" not in combined
    assert "Ve" + "ra material" not in combined
    for vendor in ["A360", "Automation Anywhere", "Brity", "UiPath", "Power Automate"]:
        assert vendor not in combined
    for token in [
        "provider_invoked=True",
        "provider_invocation_enabled=True",
        "workspace_file_read_executed=True",
        "workspace_read_execution_enabled=True",
        "repository_search_executed=True",
        "repository_search_execution_enabled=True",
        "file_content_extracted=True",
        "file_read_execution_enabled=True",
        "local_command_candidate_created=True",
        "local_command_executed=True",
        "local_command_execution_enabled=True",
        "bounded_local_command_executed=True",
        "local_runtime_execution_enabled=True",
        "external_provider_adapter_implemented=True",
        "external_runtime_touched=True",
        "credential_exposed=True",
        "raw_secret_output=True",
        "network_enabled=True",
        "growthkernel_dependency_required=True",
    ]:
        assert token not in combined
