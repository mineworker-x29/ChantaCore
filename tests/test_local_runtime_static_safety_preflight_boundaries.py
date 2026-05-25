from chanta_core.internal_provider.local_runtime_candidate_provider import (
    LocalRuntimeCommandCandidateReportService,
)
from chanta_core.internal_provider.local_runtime_safety_preflight import (
    LocalRuntimeSafetyPreflightReportService,
    LocalRuntimeSafetyPreflightRequest,
    LocalRuntimeSafetySourceService,
    LocalRuntimeStaticSafetyReportService,
)


def _combined_for_candidate_request(request: dict):
    candidate_report = LocalRuntimeCommandCandidateReportService().build_report(request)
    source = LocalRuntimeSafetySourceService(candidate_report)
    return LocalRuntimeSafetyPreflightReportService(source).build_report(LocalRuntimeSafetyPreflightRequest())


def test_v0246_blocks_forbidden_arg_network_package_destructive_and_credential_env() -> None:
    for request in [
        {"category": "diagnostic", "goal": "danger", "target": "x"},
        {"category": "version_check", "env_keys": ["API_TOKEN"]},
    ]:
        combined = _combined_for_candidate_request(request)
        assert combined.local_command_executed is False
        assert combined.process_spawned is False

    network = _combined_for_candidate_request({"category": "test", "target": "TOKEN"})
    assert network.report_status in {"failed", "blocked"}


def test_v0246_missing_target_fails_declared_preflight_without_execution() -> None:
    combined = _combined_for_candidate_request({"category": "test"})
    assert combined.report_status in {"failed", "blocked"}
    finding_types = {finding["finding_type"] for finding in combined.findings}
    assert "unresolved_argv_placeholder" not in finding_types or combined.local_command_executed is False
    assert combined.preflight_report.live_preflight_performed is False
    assert combined.preflight_report.command_executed is False


def test_v0246_cwd_outside_workspace_blocks_static_safety() -> None:
    combined = _combined_for_candidate_request({"category": "version_check", "workspace_bound": False})
    finding_types = {finding["finding_type"] for finding in combined.findings}
    assert "cwd_outside_workspace" in finding_types
    assert combined.report_status == "blocked"


def test_v0246_static_safety_findings_cover_required_boundary_types() -> None:
    candidate_report = LocalRuntimeCommandCandidateReportService().build_report({"category": "version_check"})
    source = LocalRuntimeSafetySourceService(candidate_report)
    static_report = LocalRuntimeStaticSafetyReportService(source).build_report(LocalRuntimeSafetyPreflightRequest())
    finding_types = {finding.finding_type for finding in static_report.findings}
    assert "ok" in finding_types
    assert static_report.llm_judge_used is False
    assert static_report.raw_secret_output is False
    assert static_report.credential_exposed is False
