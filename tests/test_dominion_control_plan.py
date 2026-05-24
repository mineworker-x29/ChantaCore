from __future__ import annotations

from chanta_core.cli.main import build_parser, run_dominion
from chanta_core.internal_dominion import (
    CONTROL_PLAN_NEXT_STEP,
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    CapabilityBinding,
    ControlSurfaceBinding,
    DominionCancelOrStopPlanDescriptor,
    DominionControlPlanCreateRequest,
    DominionControlPlanService,
    DominionInputBinding,
    DominionOutputPolicy,
    DominionRateLimitPolicy,
    DominionStatusTrackingPolicy,
    EnvironmentBinding,
    InternalDominionRegistryService,
    ProviderBinding,
    RuntimeBinding,
)


def test_control_plan_doc_records_v0_23_4_identity_and_boundaries() -> None:
    text = open("docs/versions/v0.23.4_control_plan_target_binding.md", encoding="utf-8").read()

    assert "Control Plan & Target Binding" in text
    assert "제어 계획·대상 바인딩" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Control plan is not dispatch" in text
    assert "Target binding is not runtime touch" in text
    assert "Input binding is not credential materialization" in text
    assert "Control plan is not preflight" in text
    assert "Control plan is not authorization" in text
    assert "v0.23.5 Dominion Static Safety Check" in text


def test_control_plan_can_be_created_from_action_candidate() -> None:
    report = DominionControlPlanService().create_control_plan(DominionControlPlanCreateRequest())

    assert report.version == "v0.23.4"
    assert report.report_status == "planned"
    assert report.next_required_step == CONTROL_PLAN_NEXT_STEP
    assert report.plan is not None
    plan = report.plan
    assert plan.plan_status == "planned"
    assert plan.readiness == "ready_for_static_safety"
    assert plan.provider_binding.binding_status == "bound"
    assert plan.runtime_binding.binding_status == "bound"
    assert plan.capability_binding.binding_status == "bound"
    assert plan.control_surface_binding is not None
    assert plan.control_surface_binding.binding_status == "bound"
    assert plan.environment_binding.binding_status == "bound"
    assert plan.input_binding is not None
    assert plan.output_policy.capture_required is True
    assert plan.output_policy.redaction_required is True
    assert plan.output_policy.raw_output_allowed is False
    assert plan.status_tracking_policy.status_tracking_required is True
    assert plan.idempotency_policy.idempotency_required is False
    assert plan.rate_limit_policy.rate_limit_required is False
    assert plan.cancel_or_stop_plan is not None
    assert plan.cancel_or_stop_plan.execution_enabled is False
    assert plan.cancel_or_stop_plan.executed is False
    assert plan.static_safety_required is True
    assert plan.static_safety_checked is False
    assert plan.preflight_required is True
    assert plan.preflight_checked is False
    assert plan.human_gate_required is True
    assert plan.human_gate_opened is False
    assert plan.authorization_required is True
    assert plan.authorization_created is False
    assert plan.dispatch_enabled is False
    assert plan.dispatched is False
    assert plan.external_runtime_touched is False
    assert plan.provider_api_call_performed is False
    assert plan.credential_exposed is False
    assert plan.raw_secret_output is False


def test_control_plan_model_types_are_exported() -> None:
    assert ProviderBinding
    assert RuntimeBinding
    assert CapabilityBinding
    assert ControlSurfaceBinding
    assert EnvironmentBinding
    assert DominionInputBinding
    assert DominionOutputPolicy
    assert DominionStatusTrackingPolicy
    assert DominionRateLimitPolicy
    assert DominionCancelOrStopPlanDescriptor


def test_missing_dispatched_required_input_and_credential_paths() -> None:
    missing = DominionControlPlanService().create_control_plan(
        DominionControlPlanCreateRequest(action_candidate_id="external_action_candidate:missing")
    )
    assert missing.report_status == "needs_more_input"
    assert "missing_action_candidate" in {item.finding_type for item in missing.findings}

    dispatched = DominionControlPlanService().create_control_plan(
        DominionControlPlanCreateRequest(source_refs=[{"action_candidate_dispatched": True}])
    )
    assert dispatched.report_status == "failed"
    assert "candidate_already_dispatched" in {item.finding_type for item in dispatched.findings}

    required = DominionControlPlanService().create_control_plan(
        DominionControlPlanCreateRequest(source_refs=[{"required_input_missing": True}])
    )
    assert required.report_status == "needs_more_input"
    assert "input_required_field_missing" in {item.finding_type for item in required.findings}

    blocked = DominionControlPlanService().create_control_plan(
        DominionControlPlanCreateRequest(requested_input_overrides={"credential_value": "hidden"})
    )
    assert blocked.report_status == "blocked"
    assert "credential_value_detected" in {item.finding_type for item in blocked.findings}
    assert blocked.plan is not None
    assert blocked.plan.input_binding is not None
    assert blocked.plan.input_binding.raw_secret_output is False
    assert "hidden" not in str(blocked.to_dict())


def test_binding_policy_constraints_and_environment_rules() -> None:
    report = DominionControlPlanService().create_control_plan(
        DominionControlPlanCreateRequest(requested_environment="production")
    )
    plan = report.plan
    assert plan is not None
    assert plan.environment_binding.production_impacting is True
    assert plan.environment_binding.requires_human_gate_for_dispatch is True
    assert plan.environment_binding.requires_strong_gate_for_mutation is True
    assert plan.environment_binding.dispatch_allowed is False
    assert "production_environment_bound" in {item.finding_type for item in report.findings}

    constraints = {item.constraint_type for item in plan.constraints}
    for expected in {
        "no_dispatch_in_v0_23_4",
        "no_preflight_in_v0_23_4",
        "no_static_safety_pass_in_v0_23_4",
        "no_human_gate_in_v0_23_4",
        "no_authorization_in_v0_23_4",
        "requires_static_safety_v0_23_5",
        "requires_preflight_v0_23_6",
        "requires_dominion_gate_v0_23_7",
        "requires_bounded_dispatch_v0_23_8",
        "requires_status_tracking_v0_23_8",
        "requires_outcome_record_v0_23_8",
        "no_credential_value_materialization",
        "provider_adapter_future_track",
    }:
        assert expected in constraints


def test_control_plan_migration_findings_from_sanitized_notes() -> None:
    report = DominionControlPlanService().create_control_plan(
        DominionControlPlanCreateRequest(
            constraints=[
                "self_execution legacy marker",
                "GrowthKernel dependency marker",
                "vendor hardcoding marker",
                "provider api call performed marker",
                "external runtime touched marker",
                "dispatch enabled too early marker",
            ]
        )
    )
    finding_types = {item.finding_type for item in report.findings}
    assert "self_execution_legacy_detected" in finding_types
    assert "growthkernel_dependency_detected" in finding_types
    assert "vendor_hardcoding_detected" in finding_types
    assert "provider_api_call_performed" in finding_types
    assert "external_runtime_touched" in finding_types
    assert "dispatch_enabled_too_early" in finding_types
    assert report.report_status == "blocked"


def test_control_plan_ocel_pig_ocpx_mapping_and_skill_statuses() -> None:
    service = DominionControlPlanService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for object_type in [
        "dominion_control_plan_create_request",
        "dominion_control_plan",
        "provider_binding",
        "runtime_binding",
        "capability_binding",
        "control_surface_binding",
        "environment_binding",
        "dominion_input_binding",
        "dominion_output_policy",
        "dominion_status_tracking_policy",
        "dominion_idempotency_policy",
        "dominion_rate_limit_policy",
        "dominion_cancel_or_stop_plan_descriptor",
        "dominion_control_plan_constraint",
        "dominion_control_plan_finding",
        "dominion_control_plan_report",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    assert "dominion_control_plan_requested" in DOMINION_OCEL_EVENT_TYPES
    assert "dominion_control_plan_created" in DOMINION_OCEL_EVENT_TYPES
    assert "plans_external_control" in DOMINION_OCEL_RELATION_TYPES
    assert "binds_provider" in DOMINION_OCEL_RELATION_TYPES
    assert "not_dispatched" in DOMINION_OCEL_RELATION_TYPES
    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert pig["version"] == "v0.23.4"
    assert pig["subject"] == "control_plan_target_binding"
    assert pig["safety_boundary"]["static_safety_checked"] is False
    assert pig["safety_boundary"]["preflight_checked"] is False
    assert pig["safety_boundary"]["authorization_created"] is False
    assert pig["safety_boundary"]["dispatched"] is False
    assert ocpx["state"] == "dominion_control_plan_bound"
    assert "DominionControlPlanState" in ocpx["target_read_models"]
    assert "DominionPlanPolicyState" in ocpx["target_read_models"]
    assert skills["skill:dominion_control_plan_create"]["status"] == "plan_only"
    assert skills["skill:dominion_target_binding"]["status"] == "plan_only"
    assert skills["skill:dominion_static_safety_check"]["status"] == "static_rule_only"
    assert skills["skill:dominion_runtime_preflight"]["status"] == "foundation_preflight_only"
    assert skills["skill:dominion_authorization_create"]["status"] == "gate_authorization_only"
    assert skills["skill:dominion_bounded_dispatch"]["status"] == "boundary_only"


def test_control_plan_cli_views_are_sanitized(capsys) -> None:
    parser = build_parser()
    commands = [
        ["dominion", "control", "plan", "create", "--action-candidate-id", "external_action_candidate:v0.23.3"],
        ["dominion", "control", "plan", "view", "--plan-id", "dominion_control_plan:v0.23.4"],
        ["dominion", "control", "plan", "bindings", "--plan-id", "dominion_control_plan:v0.23.4"],
        ["dominion", "control", "plan", "policies", "--plan-id", "dominion_control_plan:v0.23.4"],
        ["dominion", "control", "plan", "findings", "--plan-id", "dominion_control_plan:v0.23.4"],
        ["dominion", "control", "plan", "report", "--report-id", "dominion_control_plan_report:v0.23.4"],
    ]
    for command in commands:
        args = parser.parse_args(command)
        assert run_dominion(args) == 0
        output = capsys.readouterr().out
        assert "plan_id=dominion_control_plan:v0.23.4" in output
        assert "action_candidate_id=external_action_candidate:v0.23.3" in output
        assert "plan_status=planned" in output
        assert "readiness=ready_for_static_safety" in output
        assert "provider_binding_status=bound" in output
        assert "runtime_binding_status=bound" in output
        assert "capability_binding_status=bound" in output
        assert "environment=local" in output
        assert "static_safety_checked=false" in output
        assert "preflight_checked=false" in output
        assert "human_gate_opened=false" in output
        assert "authorization_created=false" in output
        assert "dispatch_enabled=false" in output
        assert "dispatched=false" in output
        assert "external_runtime_touched=false" in output
        assert "provider_api_call_performed=false" in output
        assert "credential_exposed=false" in output
        assert "next_required_step=v0.23.5 Dominion Static Safety Check" in output
        assert "raw_secrets_printed=False" in output
        assert "private_full_paths_printed=False" in output
