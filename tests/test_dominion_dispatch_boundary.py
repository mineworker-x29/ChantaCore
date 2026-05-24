from __future__ import annotations

from chanta_core.cli.main import build_parser, run_dominion
from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    DominionAuthorizationBoundaryCheck,
    DominionAuthorizationConsumptionPolicy,
    DominionAuthorizationScopeDescriptor,
    DominionBoundedDispatchBoundary,
    DominionDispatchBoundaryNeedsMoreInputCandidate,
    DominionDispatchBoundaryNoActionCandidate,
    DominionDispatchBoundaryReport,
    DominionDispatchBoundaryRequest,
    DominionDispatchBoundaryService,
    DominionDispatchCommandDescriptor,
    DominionDispatchModePolicy,
    DominionOutcomeBoundaryDescriptor,
    DominionOutputBoundaryDescriptor,
    DominionProviderDispatchInterfaceBoundary,
    DominionStatusBoundaryDescriptor,
    InternalDominionRegistryService,
)


def _report(**kwargs):
    return DominionDispatchBoundaryService().create_boundary(DominionDispatchBoundaryRequest(**kwargs))


def test_dispatch_boundary_report_can_be_created_from_gate_report_and_authorization():
    report = _report()

    assert isinstance(report, DominionDispatchBoundaryReport)
    assert report.version == "v0.23.8"
    assert report.report_status == "ready_for_consolidation"
    assert report.eligible_for_v0_23_9 is True
    assert report.authorization_check.authorization_valid_for_boundary is True
    assert report.authorization_scope.scope_status == "matched"
    assert report.dispatch_boundary.dispatch_boundary_status == "ready_for_future_dispatch"
    assert report.next_required_step == "v0.23.9 Internal Dominion Consolidation / Release Readiness"


def test_dispatch_boundary_models_can_be_created():
    report = _report()

    assert isinstance(report.authorization_check, DominionAuthorizationBoundaryCheck)
    assert isinstance(report.authorization_scope, DominionAuthorizationScopeDescriptor)
    assert isinstance(report.authorization_consumption_policy, DominionAuthorizationConsumptionPolicy)
    assert isinstance(report.dispatch_mode_policy, DominionDispatchModePolicy)
    assert isinstance(report.dispatch_boundary, DominionBoundedDispatchBoundary)
    assert isinstance(report.dispatch_boundary.command_descriptor, DominionDispatchCommandDescriptor)
    assert isinstance(report.dispatch_boundary.provider_interface_boundary, DominionProviderDispatchInterfaceBoundary)
    assert isinstance(report.status_boundary, DominionStatusBoundaryDescriptor)
    assert isinstance(report.output_boundary, DominionOutputBoundaryDescriptor)
    assert isinstance(report.outcome_boundary, DominionOutcomeBoundaryDescriptor)
    assert DominionDispatchBoundaryNeedsMoreInputCandidate
    assert DominionDispatchBoundaryNoActionCandidate


def test_authorization_boundary_checks_single_use_unconsumed_scope():
    report = _report()
    check = report.authorization_check

    assert check.authorization_exists is True
    assert check.authorization_single_use is True
    assert check.authorization_consumed is False
    assert check.authorization_expired is False
    assert check.authorization_scoped is True
    assert check.scope_matches_gate_report is True
    assert check.scope_matches_preflight is True
    assert check.scope_matches_plan is True
    assert check.scope_matches_action_candidate is True
    assert check.authorization_valid_for_boundary is True
    assert check.authorization_valid_for_live_dispatch is False
    assert check.authorization_consumption_allowed_now is False


def test_authorization_consumption_policy_forbids_consumption_in_v0_23_8():
    policy = _report().authorization_consumption_policy

    assert policy.consumption_allowed_in_v0_23_8 is False
    assert policy.consumption_deferred_to_future_provider_track is True
    assert policy.consume_only_on_actual_dispatch is True
    assert policy.consume_without_dispatch_forbidden is True
    assert policy.single_use_required is True


def test_dispatch_mode_policy_is_boundary_only_and_non_executing():
    policy = _report().dispatch_mode_policy

    assert policy.dispatch_mode == "boundary_only"
    assert policy.live_provider_api_allowed is False
    assert policy.external_runtime_touch_allowed is False
    assert policy.actual_dispatch_allowed is False
    assert policy.simulated_dispatch_allowed is False
    assert policy.boundary_only_allowed is True
    assert policy.network_allowed is False
    assert policy.credential_materialization_allowed is False
    assert policy.run_creation_allowed is False
    assert policy.shell_allowed is False
    assert policy.local_command_allowed is False
    assert policy.local_runtime_provider_enabled is False
    assert policy.external_provider_adapter_enabled is False
    assert policy.llm_judge_allowed is False


def test_command_descriptor_is_descriptor_only_without_payload_materialization():
    descriptor = _report().dispatch_boundary.command_descriptor

    assert descriptor.descriptor_status == "descriptor_only"
    assert descriptor.command_payload_materialized is False
    assert descriptor.credential_values_materialized is False
    assert descriptor.raw_payload_output is False
    assert descriptor.provider_specific_payload_created is False
    assert descriptor.plan_id == "dominion_control_plan:v0.23.4"


def test_provider_status_output_outcome_boundaries_are_created_without_live_work():
    report = _report()
    provider = report.dispatch_boundary.provider_interface_boundary

    assert provider.provider_adapter_required is True
    assert provider.provider_specific_logic_in_core is False
    assert provider.provider_api_call_performed is False
    assert report.status_boundary.live_status_tracking_started is False
    assert report.output_boundary.live_output_fetch_started is False
    assert report.output_boundary.raw_output_allowed is False
    assert report.outcome_boundary.real_external_outcome_recorded is False
    assert report.outcome_boundary.boundary_outcome_record_created is True


def test_missing_gate_report_blocks():
    report = _report(gate_report_id="missing")

    assert report.report_status == "blocked"
    assert any(item.finding_type == "missing_gate_report" for item in report.findings)
    assert report.eligible_for_v0_23_9 is False


def test_gate_not_open_creates_no_action():
    report = _report(gate_report_id="not-open")

    assert report.report_status == "no_action"
    assert any(item.finding_type == "gate_not_open" for item in report.findings)
    assert report.eligible_for_v0_23_9 is False


def test_missing_authorization_creates_needs_more_input():
    report = _report(authorization_id="missing")

    assert report.report_status == "needs_more_input"
    assert any(item.finding_type == "missing_authorization" for item in report.findings)


def test_invalid_authorization_variants_fail_or_block():
    not_single = _report(authorization_id="not-single-use")
    consumed = _report(authorization_id="consumed")
    expired = _report(authorization_id="expired")
    mismatch = _report(authorization_id="scope-mismatch")

    assert not_single.report_status == "failed"
    assert consumed.report_status == "blocked"
    assert expired.report_status in {"failed", "blocked"}
    assert mismatch.report_status == "failed"
    assert any(item.finding_type == "authorization_not_single_use" for item in not_single.findings)
    assert any(item.finding_type == "authorization_already_consumed" for item in consumed.findings)
    assert any(item.finding_type == "authorization_expired" for item in expired.findings)
    assert any(item.finding_type == "authorization_scope_mismatch" for item in mismatch.findings)


def test_live_provider_dispatch_mode_blocks():
    report = _report(dispatch_mode="live_provider_future")

    assert report.report_status == "blocked"
    assert any(item.finding_type == "dispatch_mode_not_allowed" for item in report.findings)


def test_report_safety_flags_remain_false():
    report = _report()

    assert report.safe_to_dispatch is False
    assert report.bounded_dispatch_allowed_now is False
    assert report.actual_dispatch_performed is False
    assert report.simulated_dispatch_performed is False
    assert report.provider_api_call_performed is False
    assert report.external_runtime_touched is False
    assert report.external_run_started is False
    assert report.authorization_consumed is False
    assert report.live_status_tracking_started is False
    assert report.live_output_fetch_started is False
    assert report.real_external_outcome_recorded is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.local_runtime_provider_implemented is False
    assert report.general_agent_usability_implemented is False
    assert report.workspace_agent_workbench_implemented is False
    assert report.memory_candidate_continuity_implemented is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False


def test_forbidden_markers_create_findings_or_blocks():
    cases = {
        "provider-api": "provider_api_call_performed",
        "runtime-touch": "external_runtime_touched",
        "actual-dispatch": "actual_dispatch_attempted",
        "external-run": "external_run_started",
        "authorization-consumption": "authorization_consumption_attempted",
        "credential-materialized": "credential_value_materialized",
        "real-outcome": "real_external_outcome_recorded",
        "self_execution": "self_execution_legacy_detected",
        "growthkernel": "growthkernel_dependency_detected",
        "vendor-hardcoding": "vendor_hardcoding_detected",
        "local-runtime-provider": "local_runtime_provider_attempted_too_early",
        "general-agent-usability": "general_agent_usability_attempted_too_early",
        "schumpeter": "schumpeter_split_attempted_too_early",
    }

    for marker, finding_type in cases.items():
        report = _report(requested_dispatch_note=marker)
        assert any(item.finding_type == finding_type for item in report.findings)


def test_ocel_mapping_exists_for_v0_23_8():
    required_objects = {
        "dominion_dispatch_boundary_request",
        "dominion_authorization_boundary_check",
        "dominion_authorization_scope_descriptor",
        "dominion_authorization_consumption_policy",
        "dominion_dispatch_mode_policy",
        "dominion_dispatch_command_descriptor",
        "dominion_provider_dispatch_interface_boundary",
        "dominion_bounded_dispatch_boundary",
        "dominion_status_boundary_descriptor",
        "dominion_output_boundary_descriptor",
        "dominion_outcome_boundary_descriptor",
        "dominion_dispatch_boundary_finding",
        "dominion_dispatch_boundary_report",
        "dominion_dispatch_boundary_needs_more_input_candidate",
        "dominion_dispatch_boundary_no_action_candidate",
        "dominion_gate_report",
        "dominion_gate_authorization",
        "dominion_control_plan",
        "dominion_runtime_preflight_report",
        "internal_dominion_contract",
        "execution_envelope",
        "pig_report",
        "ocpx_projection",
    }
    required_events = {
        "dominion_dispatch_boundary_requested",
        "dominion_dispatch_boundary_sources_loaded",
        "dominion_authorization_boundary_checked",
        "dominion_authorization_scope_described",
        "dominion_authorization_consumption_policy_created",
        "dominion_dispatch_mode_policy_created",
        "dominion_dispatch_command_descriptor_created",
        "dominion_provider_dispatch_interface_boundary_created",
        "dominion_bounded_dispatch_boundary_created",
        "dominion_status_boundary_created",
        "dominion_output_boundary_created",
        "dominion_outcome_boundary_created",
        "dominion_dispatch_boundary_report_created",
        "dominion_dispatch_boundary_warning_created",
        "dominion_dispatch_boundary_failed",
        "dominion_dispatch_boundary_blocked",
    }
    required_relations = {
        "checks_dominion_authorization_boundary",
        "uses_gate_report",
        "uses_gate_authorization",
        "uses_control_plan",
        "uses_runtime_preflight_report",
        "describes_authorization_scope",
        "defines_authorization_consumption_policy",
        "defines_dispatch_mode_policy",
        "describes_dispatch_command",
        "defines_provider_dispatch_interface_boundary",
        "defines_bounded_dispatch_boundary",
        "defines_status_boundary",
        "defines_output_boundary",
        "defines_outcome_boundary",
        "eligible_for_v0_23_9",
        "ready_for_dominion_consolidation",
        "not_safe_to_dispatch",
        "not_authorization_consumed",
        "not_external_runtime_touched",
        "not_provider_api_called",
        "not_dispatched",
        "not_external_run_started",
        "not_live_status_tracking",
        "not_live_output_fetch",
        "not_real_external_outcome_recorded",
        "prevents_credential_exposure",
        "defers_local_runtime_provider_to_v0_24",
        "defers_general_agent_usability_to_v0_25",
        "defers_workspace_workbench_to_v0_26",
        "defers_memory_continuity_to_v0_27",
        "defers_external_provider_adapters_to_later_track",
        "prevents_schumpeter_split_in_v0_23",
        "visible_in_workbench",
        "recorded_in_envelope",
        "derived_from_dominion_gate_report",
        "derived_from_dominion_gate_authorization",
        "derived_from_control_plan",
        "derived_from_internal_dominion_contract",
    }

    assert required_objects <= set(DOMINION_OCEL_OBJECT_TYPES)
    assert required_events <= set(DOMINION_OCEL_EVENT_TYPES)
    assert required_relations <= set(DOMINION_OCEL_RELATION_TYPES)
    assert set(DOMINION_EFFECT_TYPES) == {
        "read_only_observation",
        "state_candidate_created",
        "gate_state_created",
        "boundary_state_created",
        "consolidation_state_created",
        "workbench_snapshot_created",
    }
    assert "external_runtime_touched" not in DOMINION_EFFECT_TYPES
    assert "external_control_dispatched" not in DOMINION_EFFECT_TYPES
    assert "authorization_consumed" not in DOMINION_EFFECT_TYPES


def test_pig_and_ocpx_reports_cover_v0_23_8():
    service = DominionDispatchBoundaryService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()

    assert pig["version"] == "v0.23.8"
    assert pig["layer"] == "internal_dominion"
    assert pig["subject"] == "authorization_bounded_dispatch_status_outcome_boundary"
    assert "bounded dispatch boundary is not dispatch" in pig["principles"]
    assert pig["safety_boundary"]["boundary_state_created"] is True
    assert pig["safety_boundary"]["authorization_consumed"] is False
    assert pig["safety_boundary"]["actual_dispatch_performed"] is False
    assert pig["safety_boundary"]["live_status_tracking_started"] is False
    assert pig["safety_boundary"]["live_output_fetch_started"] is False
    assert pig["safety_boundary"]["real_external_outcome_recorded"] is False
    assert pig["roadmap"]["v0.24"] == "Internal Provider / Local Runtime Provider"
    assert pig["roadmap"]["v0.25"] == "General Agent Usability & Tool Routing"
    assert pig["roadmap"]["v0.29+"] == "External Skill / External Provider Adapters"
    assert ocpx["state"] == "dominion_dispatch_status_outcome_boundary_created"
    assert "DominionDispatchBoundaryState" in ocpx["target_read_models"]
    assert "DominionAuthorizationBoundaryState" in ocpx["target_read_models"]
    assert "DominionV0239EligibilityState" in ocpx["target_read_models"]


def test_registry_marks_dispatch_status_output_outcome_skills_boundary_only():
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for skill_id in [
        "skill:dominion_bounded_dispatch",
        "skill:dominion_run_status_track",
        "skill:dominion_run_output_fetch",
        "skill:dominion_outcome_record",
    ]:
        assert skills[skill_id]["status"] == "boundary_only"
        assert skills[skill_id]["stub"] is False
        assert skills[skill_id]["boundary_only"] is True
        assert skills[skill_id]["non_dispatching"] is True
        assert skills[skill_id]["actual_dispatch_enabled"] is False
        assert skills[skill_id]["authorization_consumption_enabled"] is False
        assert skills[skill_id]["live_status_tracking_enabled"] is False
        assert skills[skill_id]["live_output_fetch_enabled"] is False
        assert skills[skill_id]["real_external_outcome_record_enabled"] is False


def test_cli_dispatch_boundary_commands_work_and_are_sanitized(capsys):
    parser = build_parser()
    commands = [
        ["dominion", "dispatch-boundary", "create", "--gate-report-id", "dominion_gate_report:v0.23.7", "--authorization-id", "dominion_gate_authorization:v0.23.7"],
        ["dominion", "dispatch-boundary", "report", "--report-id", "dominion_dispatch_boundary_report:v0.23.8"],
        ["dominion", "dispatch-boundary", "authorization", "--report-id", "dominion_dispatch_boundary_report:v0.23.8"],
        ["dominion", "dispatch-boundary", "status", "--report-id", "dominion_dispatch_boundary_report:v0.23.8"],
        ["dominion", "dispatch-boundary", "outcome", "--report-id", "dominion_dispatch_boundary_report:v0.23.8"],
        ["dominion", "dispatch-boundary", "findings", "--report-id", "dominion_dispatch_boundary_report:v0.23.8"],
    ]

    for command in commands:
        assert run_dominion(parser.parse_args(command)) == 0
        output = capsys.readouterr().out
        assert "report_id=dominion_dispatch_boundary_report:v0.23.8" in output
        assert "boundary_id=dominion_bounded_dispatch_boundary:v0.23.8" in output
        assert "authorization_id=dominion_gate_authorization:v0.23.7" in output
        assert "safe_to_dispatch=false" in output
        assert "bounded_dispatch_allowed_now=false" in output
        assert "actual_dispatch_performed=false" in output
        assert "provider_api_call_performed=false" in output
        assert "external_runtime_touched=false" in output
        assert "external_run_started=false" in output
        assert "live_status_tracking_started=false" in output
        assert "live_output_fetch_started=false" in output
        assert "real_external_outcome_recorded=false" in output
        assert "credential_exposed=false" in output
        assert "local_runtime_provider_implemented=false" in output
        assert "general_agent_usability_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "next_required_step=v0.23.9 Internal Dominion Consolidation / Release Readiness" in output
        assert "raw_secrets_printed=false" in output
        assert "private_full_paths_printed=false" in output
        assert "credential_values_printed=false" in output
