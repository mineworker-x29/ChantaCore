from __future__ import annotations

from chanta_core.cli.main import build_parser, run_dominion
from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    CapabilityReadinessCheckResult,
    ControlSurfaceReadinessCheckResult,
    CredentialBoundaryReadinessCheckResult,
    DominionDeclaredReachabilityDescriptor,
    DominionPreflightModePolicy,
    DominionRuntimePreflightFinding,
    DominionRuntimePreflightNeedsMoreInputCandidate,
    DominionRuntimePreflightReport,
    DominionRuntimePreflightRequest,
    DominionRuntimePreflightService,
    EnvironmentReadinessCheckResult,
    IOReadinessCheckResult,
    InternalDominionRegistryService,
    OperationalReadinessCheckResult,
    ProviderReadinessCheckResult,
    RuntimeReadinessCheckResult,
    RUNTIME_PREFLIGHT_NEXT_STEP,
)


def _report(
    plan_id: str = "dominion_control_plan:v0.23.4",
    static_safety_report_id: str | None = "dominion_static_safety_report:v0.23.5",
    preflight_mode: str = "declared_only",
):
    return DominionRuntimePreflightService().check_preflight(
        DominionRuntimePreflightRequest(
            plan_id=plan_id,
            static_safety_report_id=static_safety_report_id,
            preflight_mode=preflight_mode,
        )
    )


def test_runtime_preflight_doc_records_identity_roadmap_and_boundaries() -> None:
    text = open("docs/versions/v0.23.6_runtime_preflight_reachability_check.md", encoding="utf-8").read()

    assert "Runtime Preflight / Reachability Check" in text
    assert "Korean name" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "foundation-level Dominion runtime preflight" in text
    assert "Preflight is not dispatch" in text
    assert "Preflight is not authorization" in text
    assert "Preflight is not provider-specific adapter execution" in text
    assert "Foundation preflight must not call provider APIs" in text
    assert "v0.24.x: Internal Provider / Local Runtime Provider" in text
    assert "v0.25.x: General Agent Usability & Tool Routing" in text
    assert "v0.26.x: Workspace Agent Workbench" in text
    assert "v0.27.x: Memory Candidate & Continuity" in text
    assert "v0.28.x: Public Alpha / Schumpeter Split Preparation" in text
    assert "v0.29.x+: External Skill / External Provider Adapter Development" in text
    assert "v0.23.7 Human Review & Dominion Gate" in text


def test_runtime_preflight_report_can_be_created_from_static_safety_and_plan() -> None:
    report = _report()

    assert report.version == "v0.23.6"
    assert report.report_id == "dominion_runtime_preflight_report:v0.23.6"
    assert report.plan_id == "dominion_control_plan:v0.23.4"
    assert report.static_safety_report_id == "dominion_static_safety_report:v0.23.5"
    assert report.preflight_status in {"passed", "warning"}
    assert report.eligible_for_dominion_gate is True
    assert report.safe_to_dispatch is False
    assert report.live_preflight_performed is False
    assert report.provider_api_call_performed is False
    assert report.external_runtime_touched is False
    assert report.dispatch_enabled is False
    assert report.dispatched is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.local_runtime_provider_implemented is False
    assert report.general_agent_usability_implemented is False
    assert report.workspace_agent_workbench_implemented is False
    assert report.memory_candidate_continuity_implemented is False
    assert report.external_provider_adapter_implemented is False
    assert report.schumpeter_split_introduced is False
    assert report.next_required_step == RUNTIME_PREFLIGHT_NEXT_STEP
    assert report.reachability_descriptor is not None
    assert report.provider_readiness is not None
    assert report.runtime_readiness is not None
    assert report.capability_readiness is not None
    assert report.control_surface_readiness is not None
    assert report.credential_boundary_readiness is not None
    assert report.environment_readiness is not None
    assert report.io_readiness is not None
    assert report.operational_readiness is not None


def test_runtime_preflight_model_types_are_exported() -> None:
    assert DominionRuntimePreflightRequest
    assert DominionPreflightModePolicy
    assert DominionDeclaredReachabilityDescriptor
    assert ProviderReadinessCheckResult
    assert RuntimeReadinessCheckResult
    assert CapabilityReadinessCheckResult
    assert ControlSurfaceReadinessCheckResult
    assert CredentialBoundaryReadinessCheckResult
    assert EnvironmentReadinessCheckResult
    assert IOReadinessCheckResult
    assert OperationalReadinessCheckResult
    assert DominionRuntimePreflightFinding
    assert DominionRuntimePreflightReport
    assert DominionRuntimePreflightNeedsMoreInputCandidate


def test_preflight_mode_policy_defaults_and_future_modes() -> None:
    report = _report()
    policy = report.preflight_mode_policy

    assert policy.preflight_mode == "declared_only"
    assert policy.live_provider_api_allowed is False
    assert policy.external_runtime_touch_allowed is False
    assert policy.network_allowed is False
    assert policy.credential_materialization_allowed is False
    assert policy.dispatch_allowed is False
    assert policy.run_creation_allowed is False
    assert policy.shell_allowed is False
    assert policy.local_command_allowed is False
    assert policy.local_runtime_provider_enabled is False
    assert policy.general_agent_usability_enabled is False
    assert policy.llm_judge_allowed is False
    assert policy.declared_descriptor_required is True
    assert policy.provider_adapter_required_for_live is True

    future = _report(preflight_mode="live_read_only_future")
    assert future.preflight_status == "blocked"
    assert "preflight_mode_not_allowed" in {item.finding_type for item in future.findings}


def test_declared_reachability_descriptor_is_non_live() -> None:
    descriptor = _report().reachability_descriptor

    assert descriptor is not None
    assert descriptor.reachability_source == "declared_inventory"
    assert descriptor.runtime_declared_available is True
    assert descriptor.provider_declared_available is True
    assert descriptor.control_surface_declared_available is True
    assert descriptor.credential_boundary_declared is True
    assert descriptor.status_tracking_declared is True
    assert descriptor.output_fetch_declared is True
    assert descriptor.cancel_or_stop_declared is True
    assert descriptor.live_verification_performed is False
    assert descriptor.provider_api_call_performed is False
    assert descriptor.external_runtime_touched is False


def test_runtime_preflight_status_paths() -> None:
    cases = {
        "missing": ("blocked", "missing_control_plan"),
        "provider-missing": ("failed", "provider_binding_missing"),
        "runtime-missing": ("failed", "runtime_binding_missing"),
        "capability-missing": ("failed", "capability_availability_unknown"),
        "environment-unknown": ("failed", "environment_unknown"),
        "production": ("warning", "production_environment_requires_gate"),
        "credential": ("blocked", "credential_value_materialized"),
        "raw-secret": ("blocked", "credential_value_output"),
        "provider-api": ("blocked", "provider_api_call_performed"),
        "runtime-touch": ("blocked", "external_runtime_touched"),
        "no-redaction": ("failed", "output_capture_not_ready"),
        "no-status": ("warning", "status_tracking_unavailable"),
        "no-idempotency": ("failed", "idempotency_unavailable"),
        "no-rate": ("failed", "rate_limit_unavailable"),
        "no-cancel": ("warning", "cancel_or_stop_unavailable"),
    }
    for plan_id, (status, finding_type) in cases.items():
        report = _report(plan_id)
        assert report.preflight_status == status
        assert finding_type in {item.finding_type for item in report.findings}
        assert report.safe_to_dispatch is False
        if status == "warning":
            assert report.eligible_for_dominion_gate is True
        if status == "blocked":
            assert report.eligible_for_dominion_gate is False


def test_missing_or_failed_static_safety_controls_status() -> None:
    missing = _report(static_safety_report_id="missing")
    failed = _report(static_safety_report_id="failed")
    blocked = _report(static_safety_report_id="blocked")

    assert missing.preflight_status == "failed"
    assert "missing_static_safety_report" in {item.finding_type for item in missing.findings}
    assert failed.preflight_status == "failed"
    assert "static_safety_not_passed" in {item.finding_type for item in failed.findings}
    assert blocked.preflight_status == "blocked"
    assert "static_safety_not_passed" in {item.finding_type for item in blocked.findings}


def test_runtime_preflight_ocel_pig_ocpx_mapping_and_skill_statuses() -> None:
    service = DominionRuntimePreflightService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for object_type in [
        "dominion_runtime_preflight_request",
        "dominion_preflight_mode_policy",
        "dominion_declared_reachability_descriptor",
        "provider_readiness_check_result",
        "runtime_readiness_check_result",
        "capability_readiness_check_result",
        "control_surface_readiness_check_result",
        "credential_boundary_readiness_check_result",
        "environment_readiness_check_result",
        "io_readiness_check_result",
        "operational_readiness_check_result",
        "dominion_runtime_preflight_finding",
        "dominion_runtime_preflight_report",
        "dominion_runtime_preflight_needs_more_input_candidate",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    for event_type in [
        "dominion_runtime_preflight_requested",
        "dominion_runtime_preflight_report_created",
        "dominion_runtime_preflight_blocked",
    ]:
        assert event_type in DOMINION_OCEL_EVENT_TYPES
    for relation_type in [
        "checks_runtime_preflight",
        "uses_static_safety_report",
        "uses_declared_reachability",
        "checks_provider_readiness",
        "checks_runtime_readiness",
        "eligible_for_dominion_gate",
        "defers_local_runtime_provider_to_v0_24",
        "defers_general_agent_usability_to_v0_25",
        "prevents_schumpeter_split_in_v0_23",
        "derived_from_static_safety_report",
    ]:
        assert relation_type in DOMINION_OCEL_RELATION_TYPES
    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert pig["version"] == "v0.23.6"
    assert pig["subject"] == "runtime_preflight_reachability_check"
    assert pig["safety_boundary"]["safe_to_dispatch"] is False
    assert pig["safety_boundary"]["live_preflight_performed"] is False
    assert pig["safety_boundary"]["local_runtime_provider_implemented"] is False
    assert pig["roadmap"]["v0.24"] == "Internal Provider / Local Runtime Provider"
    assert pig["roadmap"]["v0.25"] == "General Agent Usability & Tool Routing"
    assert pig["roadmap"]["v0.26"] == "Workspace Agent Workbench"
    assert pig["roadmap"]["v0.27"] == "Memory Candidate & Continuity"
    assert pig["roadmap"]["v0.28"] == "Public Alpha / Schumpeter Split Preparation"
    assert pig["roadmap"]["v0.29+"] == "External Skill / External Provider Adapters"
    assert ocpx["state"] == "dominion_runtime_preflight_checked"
    assert "DominionRuntimePreflightState" in ocpx["target_read_models"]
    assert "DominionReadinessState" in ocpx["target_read_models"]
    assert "DominionGateEligibilityState" in ocpx["target_read_models"]
    assert "DominionRoadmapBoundaryState" in ocpx["target_read_models"]
    assert skills["skill:dominion_runtime_preflight"]["status"] == "foundation_preflight_only"
    assert skills["skill:dominion_runtime_preflight"]["read_only"] is True
    assert skills["skill:dominion_review_gate"]["status"] == "review_gate_only"
    assert skills["skill:dominion_authorization_create"]["status"] == "gate_authorization_only"
    assert skills["skill:dominion_bounded_dispatch"]["status"] == "boundary_only"


def test_runtime_preflight_cli_views_are_sanitized(capsys) -> None:
    parser = build_parser()
    commands = [
        [
            "dominion",
            "preflight",
            "check",
            "--plan-id",
            "dominion_control_plan:v0.23.4",
            "--static-safety-report-id",
            "dominion_static_safety_report:v0.23.5",
        ],
        [
            "dominion",
            "preflight",
            "summary",
            "--plan-id",
            "dominion_control_plan:v0.23.4",
        ],
        [
            "dominion",
            "preflight",
            "report",
            "--report-id",
            "dominion_runtime_preflight_report:v0.23.6",
        ],
        [
            "dominion",
            "preflight",
            "findings",
            "--report-id",
            "dominion_runtime_preflight_report:v0.23.6",
        ],
    ]
    for command in commands:
        args = parser.parse_args(command)
        assert run_dominion(args) == 0
        output = capsys.readouterr().out
        assert "report_id=dominion_runtime_preflight_report:v0.23.6" in output
        assert "plan_id=dominion_control_plan:v0.23.4" in output
        assert "preflight_status=" in output
        assert "preflight_mode=declared_only" in output
        assert "eligible_for_dominion_gate=true" in output
        assert "safe_to_dispatch=false" in output
        assert "live_preflight_performed=false" in output
        assert "provider_api_call_performed=false" in output
        assert "external_runtime_touched=false" in output
        assert "dispatch_enabled=false" in output
        assert "dispatched=false" in output
        assert "credential_exposed=false" in output
        assert "local_runtime_provider_implemented=false" in output
        assert "general_agent_usability_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "next_required_step=v0.23.7 Human Review & Dominion Gate" in output
        assert "raw_secrets_printed=False" in output
        assert "private_full_paths_printed=False" in output
