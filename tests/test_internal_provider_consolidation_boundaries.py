import inspect
import re

import chanta_core.internal_provider.internal_provider_consolidation as consolidation_module
from chanta_core.internal_provider.internal_provider_consolidation import (
    InternalProviderConsolidationReportService,
    InternalProviderConsolidationSourceService,
)


def test_consolidation_source_has_no_new_runtime_or_mutation_paths() -> None:
    source = inspect.getsource(consolidation_module)

    for forbidden in [
        "subprocess.run",
        "subprocess.Popen",
        "os.system",
        "command_rerun_performed=True",
        "new_provider_invocation_performed=True",
        "new_repository_search_performed=True",
        "new_file_read_performed=True",
        "new_process_inspection_performed=True",
        "new_local_command_executed=True",
        "automatic_repair_performed=True",
        "file_mutation_performed=True",
        "patch_applied=True",
        "credential_exposed=True",
        "raw_secret_output=True",
        "raw_output_dumped=True",
        "external_provider_adapter_implemented=True",
        "external_runtime_touched=True",
        "provider_api_call_performed=True",
        "schumpeter_split_introduced=True",
        "growthkernel_dependency_required=True",
        "general_agent_usability_implemented=True",
        "workspace_agent_workbench_implemented=True",
        "memory_candidate_continuity_implemented=True",
        "llm_judge_used=True",
        "llm_judge_enabled=True",
        "openai",
        "anthropic",
        "chat.completions",
        "eval(",
    ]:
        assert forbidden not in source
    assert re.search(r"(?<![A-Za-z0-9_])shell=True", source) is None


def test_consolidation_report_declares_no_new_provider_or_command_activity() -> None:
    report = InternalProviderConsolidationReportService().build_report()

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


def test_dangerous_safety_counts_are_zero() -> None:
    safety = InternalProviderConsolidationReportService().build_all_parts()["safety_boundary"]

    assert safety.command_rerun_count == 0
    assert safety.uncontrolled_local_command_execution_count == 0
    assert safety.unrestricted_shell_count == 0
    assert safety.arbitrary_subprocess_count == 0
    assert safety.shell_true_count == 0
    assert safety.os_system_count == 0
    assert safety.network_access_count == 0
    assert safety.package_install_count == 0
    assert safety.destructive_command_count == 0
    assert safety.unexpected_file_mutation_count == 0
    assert safety.credential_exposure_count == 0
    assert safety.raw_secret_output_count == 0
    assert safety.raw_output_dump_count == 0
    assert safety.external_provider_adapter_count == 0
    assert safety.external_runtime_touch_count == 0
    assert safety.schumpeter_split_count == 0
    assert safety.llm_judge_count == 0


def test_source_service_only_returns_metadata_refs() -> None:
    source = InternalProviderConsolidationSourceService().load_all_sources()

    assert set(source) == {
        "v0.24.0",
        "v0.24.1",
        "v0.24.2",
        "v0.24.3",
        "v0.24.4",
        "v0.24.5",
        "v0.24.6",
        "v0.24.7",
        "v0.24.8",
        "v0.23.9",
    }
    assert all("subject" in item for item in source.values())
    assert all(item["read_only"] is True for item in source.values())
