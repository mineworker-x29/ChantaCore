from __future__ import annotations

from chanta_core.cli.main import main
from chanta_core.internal_provider import (
    OCEL_INSPECTION_PROVIDER_ID,
    OCPX_PROJECTION_PROVIDER_ID,
    PIG_INSPECTION_PROVIDER_ID,
    PROCESS_INSPECTION_EFFECT_TYPES,
    PROCESS_INSPECTION_EVENT_TYPES,
    PROCESS_INSPECTION_FORBIDDEN_EFFECT_TYPES,
    PROCESS_INSPECTION_OBJECT_TYPES,
    PROCESS_INSPECTION_RELATION_TYPES,
    OCELInspectionRequest,
    OCELObjectTraceRequest,
    OCELTypeCatalogService,
    OCPXInspectionRequest,
    PIGInspectionRequest,
    InternalProviderRegistryReportService,
    ProcessInspectionPolicyService,
    ProcessInspectionProviderContractSourceService,
    ProcessInspectionProviderSkillService,
    ProcessInspectionScopeService,
    ProcessStateInspectionReportService,
)


def _source_service() -> ProcessInspectionProviderContractSourceService:
    return ProcessInspectionProviderContractSourceService(
        ocel_events=[
            {
                "event_id": "event:1",
                "event_type": "internal_provider_registry_created",
                "event_timestamp": "2026-05-24T00:00:00Z",
                "event_attrs": {"token_value": "super-secret-token"},
                "related_objects": [
                    {
                        "object_id": "provider:registry",
                        "object_type": "internal_provider_registry",
                        "qualifier": "registry",
                    }
                ],
            },
            {
                "event_id": "event:2",
                "event_type": "repository_search_report_created",
                "event_timestamp": "2026-05-24T00:01:00Z",
                "event_attrs": {"status": "passed"},
                "related_objects": [
                    {
                        "object_id": "provider:registry",
                        "object_type": "internal_provider_registry",
                        "qualifier": "registry",
                    }
                ],
            },
        ],
        pig_reports=[
            {
                "report_id": "pig:v0.24.4",
                "version": "v0.24.4",
                "layer": "internal_provider",
                "subject": "ocel_pig_ocpx_inspection_provider",
                "body": "api_key=raw-secret-value",
            }
        ],
        ocpx_projections=[
            {
                "projection_id": "ocpx:v0.24.4",
                "version": "v0.24.4",
                "state": "process_intelligence_state_inspected",
                "source_read_models": ["InternalProviderRegistryState"],
                "target_read_models": ["ProcessStateInspectionState", "V024ReadinessState"],
                "effect_types": ["read_only_observation", "process_state_inspected"],
                "body": "credential: raw-secret-value",
            }
        ],
    )


def test_process_inspection_policy_and_scope_build() -> None:
    policy = ProcessInspectionPolicyService().build_policy()
    scope = ProcessInspectionScopeService().build_scope()

    assert policy.version == "v0.24.4"
    assert policy.provider_ids == [
        OCEL_INSPECTION_PROVIDER_ID,
        PIG_INSPECTION_PROVIDER_ID,
        OCPX_PROJECTION_PROVIDER_ID,
    ]
    assert policy.read_only is True
    assert policy.ocel_mutation_enabled is False
    assert policy.pig_mutation_enabled is False
    assert policy.ocpx_mutation_enabled is False
    assert policy.event_append_enabled is False
    assert policy.projection_recompute_enabled is False
    assert policy.graph_recompute_enabled is False
    assert policy.raw_payload_output_enabled is False
    assert policy.secret_redaction_required is True
    assert policy.private_path_sanitization_required is True
    assert policy.local_command_execution_enabled is False
    assert scope.max_recent_events == policy.max_recent_events_default
    assert scope.max_trace_events == policy.max_trace_events_default
    assert scope.max_report_chars == policy.max_report_chars_default
    assert scope.max_projection_chars == policy.max_projection_chars_default


def test_process_inspection_skills_are_activated_and_future_runtime_stubs_remain() -> None:
    service = ProcessInspectionProviderSkillService()
    skills = service.build_skill_statuses()

    assert skills["skill:ocel_inspection_provider_view"] == "implemented"
    assert skills["skill:pig_inspection_provider_view"] == "implemented"
    assert skills["skill:ocpx_projection_provider_view"] == "implemented"
    assert skills["skill:repository_search_provider_view"] == "implemented"
    assert skills["skill:file_read_provider_view"] == "implemented"
    assert skills["skill:local_runtime_command_candidate_create"] == "contract_only"
    assert skills["skill:bounded_local_command_run"] == "contract_only"


def test_process_inspection_providers_are_declared_in_registry() -> None:
    registry = InternalProviderRegistryReportService().build_report().registry
    provider_types = {item.provider_type for item in registry.provider_refs}

    assert OCEL_INSPECTION_PROVIDER_ID in provider_types
    assert PIG_INSPECTION_PROVIDER_ID in provider_types
    assert OCPX_PROJECTION_PROVIDER_ID in provider_types


def test_ocel_catalog_and_mapping_entries_exist() -> None:
    catalog = OCELTypeCatalogService().build_catalog()

    assert catalog.version == "v0.24.4"
    assert catalog.event_type_count > 0
    assert catalog.object_type_count > 0
    assert catalog.relation_type_count > 0
    assert all(item.raw_payload_output is False for item in catalog.event_types)
    assert "process_inspection_provider_policy" in PROCESS_INSPECTION_OBJECT_TYPES
    assert "process_state_inspection_report_created" in PROCESS_INSPECTION_EVENT_TYPES
    assert "not_ocel_mutated" in PROCESS_INSPECTION_RELATION_TYPES
    assert "process_state_inspected" in PROCESS_INSPECTION_EFFECT_TYPES
    assert "ocel_event_appended" in PROCESS_INSPECTION_FORBIDDEN_EFFECT_TYPES


def test_recent_event_view_is_bounded_and_sanitized() -> None:
    service = ProcessStateInspectionReportService(source_service=_source_service())
    report = service.build_report(
        ocel_request=OCELInspectionRequest(
            request_id="ocel_request:test",
            recent_event_limit=1,
            include_payload_preview=True,
        )
    )

    assert report.ocel_recent_event_view is not None
    assert report.ocel_recent_event_view.event_count == 1
    assert report.ocel_recent_event_view.truncated is True
    assert report.ocel_recent_event_view.raw_payload_included is False
    assert report.ocel_recent_event_view.redaction_applied is True
    assert report.credential_exposed is False
    assert report.raw_secret_output is False


def test_object_trace_view_is_bounded_and_non_mutating() -> None:
    service = ProcessStateInspectionReportService(source_service=_source_service())
    report = service.build_report(
        trace_requests=[
            OCELObjectTraceRequest(
                object_id="provider:registry",
                max_events=1,
                include_event_payload_preview=True,
            )
        ]
    )

    trace = report.ocel_trace_views[0]
    assert trace.event_count == 1
    assert trace.truncated is True
    assert trace.raw_payload_included is False
    assert trace.raw_secret_output is False
    assert report.event_log_mutation_performed is False
    assert report.projection_mutation_performed is False
    assert report.graph_recompute_performed is False


def test_pig_and_ocpx_views_are_bounded_sanitized_and_indexed() -> None:
    service = ProcessStateInspectionReportService(source_service=_source_service())
    report = service.build_report(
        pig_request=PIGInspectionRequest(
            request_id="pig_request:test",
            include_report_body=True,
            max_report_chars=80,
        ),
        ocpx_request=OCPXInspectionRequest(
            request_id="ocpx_request:test",
            include_projection_body=True,
            max_projection_chars=80,
        ),
    )

    assert report.pig_inspection_report is not None
    assert report.pig_inspection_report.index is not None
    assert report.pig_inspection_report.index.report_count == 1
    assert report.pig_inspection_report.report_views[0].raw_report_included is False
    assert report.pig_inspection_report.report_views[0].redaction_applied is True
    assert report.ocpx_inspection_report is not None
    assert report.ocpx_inspection_report.index is not None
    assert report.ocpx_inspection_report.index.projection_count == 1
    assert report.ocpx_inspection_report.projection_views[0].raw_projection_included is False
    assert report.ocpx_inspection_report.projection_views[0].redaction_applied is True


def test_process_state_report_builds_with_readiness_and_boundaries() -> None:
    report = ProcessStateInspectionReportService(source_service=_source_service()).build_report()

    assert report.version == "v0.24.4"
    assert report.report_status in {"passed", "warning"}
    assert report.ready_for_v0_24_5 is True
    assert report.ready_for_v0_25 is False
    assert report.ocel_inspection_performed is True
    assert report.pig_inspection_performed is True
    assert report.ocpx_inspection_performed is True
    assert report.local_command_executed is False
    assert report.external_provider_adapter_implemented is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.raw_payload_output is False
    assert report.llm_judge_used is False
    assert report.next_required_step == "v0.24.5 Local Runtime Command Candidate Provider"


def test_pig_and_ocpx_projection_reports_build() -> None:
    service = ProcessStateInspectionReportService(source_service=_source_service())
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.24.4"
    assert pig["layer"] == "internal_provider"
    assert pig["subject"] == "ocel_pig_ocpx_inspection_provider"
    assert pig["safety_boundary"]["event_log_mutation_performed"] is False
    assert pig["safety_boundary"]["projection_mutation_performed"] is False
    assert pig["safety_boundary"]["graph_recompute_performed"] is False
    assert ocpx["state"] == "process_intelligence_state_inspected"
    assert "OCELInspectionProviderState" in ocpx["target_read_models"]
    assert "ProcessStateInspectionState" in ocpx["target_read_models"]


def test_process_cli_views_work(capsys) -> None:
    assert main(["provider", "process", "ocel", "types"]) == 0
    assert "version=v0.24.4" in capsys.readouterr().out
    assert main(["provider", "process", "ocel", "events", "--limit", "50"]) == 0
    assert "provider=ocel_inspection_provider" in capsys.readouterr().out
    assert main(["provider", "process", "ocel", "trace", "--object-id", "provider:registry", "--max-events", "100"]) == 0
    assert "raw_payload_output=false" in capsys.readouterr().out
    assert main(["provider", "process", "pig", "list"]) == 0
    assert "provider=pig_inspection_provider" in capsys.readouterr().out
    assert main(["provider", "process", "ocpx", "list"]) == 0
    assert "provider=ocpx_projection_provider" in capsys.readouterr().out
    assert main(["provider", "process", "report"]) == 0
    assert "ready_for_v0_25=false" in capsys.readouterr().out
    assert main(["provider", "process", "findings"]) == 0
    output = capsys.readouterr().out
    assert "local_command_executed=false" in output
    assert "raw_secret_output=false" in output
