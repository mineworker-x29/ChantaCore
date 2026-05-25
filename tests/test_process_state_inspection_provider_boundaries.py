from __future__ import annotations

from chanta_core.internal_provider import (
    OCELInspectionRequest,
    OCPXInspectionRequest,
    PIGInspectionRequest,
    ProcessInspectionPolicyService,
    ProcessStateInspectionFindingService,
    ProcessStateInspectionReportService,
)


def _finding_types(markers: list[str]) -> set[str]:
    findings = ProcessStateInspectionFindingService().build_findings(markers=markers)
    return {item.finding_type for item in findings}


def test_missing_sources_are_reported_as_warnings_under_standard_mode() -> None:
    report = ProcessStateInspectionReportService().build_report()
    finding_types = {item.finding_type for item in report.findings}

    assert "missing_pig_reports" in finding_types
    assert "missing_ocpx_projections" in finding_types
    assert report.report_status == "warning"
    assert report.ready_for_v0_24_5 is True


def test_raw_payload_report_and_projection_requests_are_blocked() -> None:
    service = ProcessStateInspectionReportService()
    report = service.build_report(
        ocel_request=OCELInspectionRequest(
            request_id="ocel_request:raw",
            include_raw_payload=True,
        ),
        pig_request=PIGInspectionRequest(
            request_id="pig_request:raw",
            include_raw_report=True,
        ),
        ocpx_request=OCPXInspectionRequest(
            request_id="ocpx_request:raw",
            include_raw_projection=True,
        ),
    )
    finding_types = {item.finding_type for item in report.findings}

    assert "raw_payload_requested" in finding_types
    assert "raw_report_output_blocked" in finding_types
    assert "raw_projection_output_blocked" in finding_types
    assert report.report_status == "blocked"
    assert report.raw_payload_output is False
    assert report.raw_secret_output is False


def test_mutation_recompute_execution_and_external_touch_attempts_block() -> None:
    finding_types = _finding_types(
        [
            "event_log_mutation",
            "ocel_event_append",
            "ocel_object_mutation",
            "ocel_relation_mutation",
            "pig_graph_mutation",
            "pig_recompute",
            "ocpx_projection_mutation",
            "ocpx_recompute",
            "local_command_execution",
            "provider_api_call",
            "external_runtime_touched",
        ]
    )

    assert "event_log_mutation_attempted" in finding_types
    assert "ocel_event_append_attempted" in finding_types
    assert "ocel_object_mutation_attempted" in finding_types
    assert "ocel_relation_mutation_attempted" in finding_types
    assert "pig_graph_mutation_attempted" in finding_types
    assert "pig_recompute_attempted" in finding_types
    assert "ocpx_projection_mutation_attempted" in finding_types
    assert "ocpx_recompute_attempted" in finding_types
    assert "local_command_execution_attempted" in finding_types
    assert "provider_api_call_performed" in finding_types
    assert "external_runtime_touched" in finding_types


def test_privacy_product_and_future_track_attempts_are_findings() -> None:
    finding_types = _finding_types(
        [
            "credential_exposure",
            "raw_secret_output",
            "vendor_hardcoding",
            "growthkernel_dependency",
            "schumpeter_split",
            "general_agent_usability",
            "llm_judge",
        ]
    )

    assert "credential_exposure_detected" in finding_types
    assert "raw_secret_output_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "schumpeter_split_detected" in finding_types
    assert "general_agent_usability_premature" in finding_types
    assert "llm_judge_detected" in finding_types


def test_report_never_sets_forbidden_boundary_flags_true() -> None:
    report = ProcessStateInspectionReportService().build_report(
        markers=[
            "event_log_mutation",
            "pig_recompute",
            "ocpx_recompute",
            "local_command_execution",
            "raw_secret_output",
            "llm_judge",
        ]
    )

    assert report.event_log_mutation_performed is False
    assert report.projection_mutation_performed is False
    assert report.graph_recompute_performed is False
    assert report.local_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_payload_output is False
    assert report.llm_judge_used is False
    assert report.report_status == "blocked"


def test_policy_forbids_all_process_state_mutation_and_local_runtime() -> None:
    policy = ProcessInspectionPolicyService().build_policy()

    assert policy.ocel_mutation_enabled is False
    assert policy.pig_mutation_enabled is False
    assert policy.ocpx_mutation_enabled is False
    assert policy.event_append_enabled is False
    assert policy.projection_recompute_enabled is False
    assert policy.graph_recompute_enabled is False
    assert policy.raw_payload_output_enabled is False
    assert policy.local_command_execution_enabled is False
