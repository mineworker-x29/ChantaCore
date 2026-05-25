from __future__ import annotations

from chanta_core.cli.main import build_parser, run_dominion
from chanta_core.internal_dominion import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    DominionStaticRuleRegistry,
    DominionStaticSafetyCategoryResult,
    DominionStaticSafetyCheckRequest,
    DominionStaticSafetyFinding,
    DominionStaticSafetyNeedsMoreInputCandidate,
    DominionStaticSafetyNoActionCandidate,
    DominionStaticSafetyReport,
    DominionStaticSafetyRule,
    DominionStaticSafetyRuleResult,
    DominionStaticSafetyService,
    InternalDominionRegistryService,
    STATIC_SAFETY_NEXT_STEP,
)


def _report(plan_id: str = "dominion_control_plan:v0.23.4"):
    return DominionStaticSafetyService().check_static_safety(DominionStaticSafetyCheckRequest(plan_id=plan_id))


def test_static_safety_doc_records_v0_23_5_identity_and_boundaries() -> None:
    text = open("docs/versions/v0.23/v0.23.5_dominion_static_safety_check.md", encoding="utf-8").read()

    assert "Dominion Static Safety Check" in text
    assert "지배 정적 안전성 검사" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Static safety check is not preflight" in text
    assert "Static safety check is not provider API call" in text
    assert "Static safety check is not external runtime touch" in text
    assert "Static safety check is not authorization" in text
    assert "Static safety check is not dispatch" in text
    assert "v0.23.6 Runtime Preflight / Reachability Check" in text


def test_static_safety_report_can_be_created_from_control_plan() -> None:
    report = _report()

    assert report.version == "v0.23.5"
    assert report.report_id == "dominion_static_safety_report:v0.23.5"
    assert report.plan_id == "dominion_control_plan:v0.23.4"
    assert report.static_safety_status == "passed"
    assert report.eligible_for_preflight is True
    assert report.safe_to_dispatch is False
    assert report.preflight_required is True
    assert report.human_gate_required is True
    assert report.authorization_required is True
    assert report.status_tracking_required is True
    assert report.outcome_record_required is True
    assert report.runtime_touched is False
    assert report.provider_api_call_performed is False
    assert report.dispatch_enabled is False
    assert report.dispatched is False
    assert report.credential_exposed is False
    assert report.raw_secret_output is False
    assert report.llm_judge_used is False
    assert report.next_required_step == STATIC_SAFETY_NEXT_STEP
    assert report.checked_rule_count >= 20
    assert report.passed_rule_count == report.checked_rule_count
    assert report.warning_count == 0
    assert report.error_count == 0
    assert report.critical_count == 0


def test_static_safety_model_types_and_rule_categories_are_exported() -> None:
    assert DominionStaticSafetyCheckRequest
    assert DominionStaticSafetyRule
    assert DominionStaticSafetyRuleResult
    assert DominionStaticSafetyFinding
    assert DominionStaticSafetyCategoryResult
    assert DominionStaticSafetyReport
    assert DominionStaticSafetyNoActionCandidate
    assert DominionStaticSafetyNeedsMoreInputCandidate

    categories = {item.category for item in DominionStaticRuleRegistry().list_rules()}
    for expected in {
        "lifecycle",
        "provider",
        "runtime",
        "capability",
        "environment",
        "input_credential",
        "output_policy",
        "status_outcome",
        "idempotency_rate",
        "cancel_stop",
        "migration_continuity",
    }:
        assert expected in categories


def test_static_safety_status_paths() -> None:
    cases = {
        "missing": ("blocked", "missing_control_plan"),
        "dispatched": ("blocked", "control_plan_already_dispatched"),
        "provider-missing": ("failed", "provider_binding_missing"),
        "runtime-missing": ("failed", "runtime_binding_missing"),
        "capability-missing": ("failed", "capability_binding_missing"),
        "environment-unknown": ("failed", "environment_unknown"),
        "production": ("warning", "production_environment_requires_strong_gate"),
        "credential": ("blocked", "credential_value_detected"),
        "raw-secret": ("blocked", "raw_secret_output_detected"),
        "no-redaction": ("failed", "output_redaction_missing"),
        "no-status": ("warning", "status_tracking_missing"),
        "no-outcome": ("warning", "outcome_record_missing"),
        "no-idempotency": ("warning", "idempotency_missing"),
        "no-rate": ("warning", "rate_limit_missing"),
        "no-cancel": ("warning", "cancel_or_stop_plan_missing"),
        "provider-specific": ("failed", "provider_specific_logic_in_core"),
        "provider-api": ("blocked", "provider_api_call_performed"),
        "runtime-touch": ("blocked", "external_runtime_touched"),
        "preflight": ("failed", "preflight_gate_or_authorization_already_marked"),
    }
    for plan_id, (status, finding_type) in cases.items():
        report = _report(plan_id)
        assert report.static_safety_status == status
        assert finding_type in {item.finding_type for item in report.findings}
        if status == "blocked":
            assert report.eligible_for_preflight is False
        if status == "warning":
            assert report.eligible_for_preflight is True
        assert report.safe_to_dispatch is False


def test_static_safety_ocel_pig_ocpx_mapping_and_skill_statuses() -> None:
    service = DominionStaticSafetyService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for object_type in [
        "dominion_static_safety_check_request",
        "dominion_static_safety_rule",
        "dominion_static_safety_rule_result",
        "dominion_static_safety_category_result",
        "dominion_static_safety_finding",
        "dominion_static_safety_report",
        "dominion_static_safety_no_action_candidate",
        "dominion_static_safety_needs_more_input_candidate",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    assert "dominion_static_safety_check_requested" in DOMINION_OCEL_EVENT_TYPES
    assert "dominion_static_safety_report_created" in DOMINION_OCEL_EVENT_TYPES
    assert "dominion_static_safety_blocked" in DOMINION_OCEL_EVENT_TYPES
    assert "checks_dominion_static_safety" in DOMINION_OCEL_RELATION_TYPES
    assert "eligible_for_runtime_preflight" in DOMINION_OCEL_RELATION_TYPES
    assert "not_safe_to_dispatch" in DOMINION_OCEL_RELATION_TYPES
    assert {"read_only_observation", "state_candidate_created"} <= set(DOMINION_EFFECT_TYPES)
    assert pig["version"] == "v0.23.5"
    assert pig["subject"] == "dominion_static_safety_check"
    assert pig["safety_boundary"]["safe_to_dispatch"] is False
    assert pig["safety_boundary"]["provider_api_call_performed"] is False
    assert pig["safety_boundary"]["llm_judge_enabled"] is False
    assert ocpx["state"] == "dominion_control_plan_static_safety_checked"
    assert "DominionStaticSafetyState" in ocpx["target_read_models"]
    assert "DominionPreflightEligibilityState" in ocpx["target_read_models"]
    assert skills["skill:dominion_static_safety_check"]["status"] == "static_rule_only"
    assert skills["skill:dominion_static_safety_check"]["read_only"] is True
    assert skills["skill:dominion_runtime_preflight"]["status"] == "foundation_preflight_only"
    assert skills["skill:dominion_review_gate"]["status"] == "review_gate_only"
    assert skills["skill:dominion_authorization_create"]["status"] == "gate_authorization_only"
    assert skills["skill:dominion_bounded_dispatch"]["status"] == "boundary_only"


def test_static_safety_cli_views_are_sanitized(capsys) -> None:
    parser = build_parser()
    commands = [
        ["dominion", "static-safety", "check", "--plan-id", "dominion_control_plan:v0.23.4"],
        ["dominion", "static-safety", "summary", "--plan-id", "dominion_control_plan:v0.23.4"],
        ["dominion", "static-safety", "report", "--report-id", "dominion_static_safety_report:v0.23.5"],
        ["dominion", "static-safety", "findings", "--report-id", "dominion_static_safety_report:v0.23.5"],
        ["dominion", "static-safety", "rules"],
    ]
    for command in commands:
        args = parser.parse_args(command)
        assert run_dominion(args) == 0
        output = capsys.readouterr().out
        assert "report_id=dominion_static_safety_report:v0.23.5" in output
        assert "plan_id=dominion_control_plan:v0.23.4" in output
        assert "static_safety_status=passed" in output
        assert "eligible_for_preflight=true" in output
        assert "safe_to_dispatch=false" in output
        assert "preflight_required=true" in output
        assert "human_gate_required=true" in output
        assert "authorization_required=true" in output
        assert "dispatch_enabled=false" in output
        assert "dispatched=false" in output
        assert "external_runtime_touched=false" in output
        assert "provider_api_call_performed=false" in output
        assert "credential_exposed=false" in output
        assert "next_required_step=v0.23.6 Runtime Preflight / Reachability Check" in output
        assert "raw_secrets_printed=False" in output
        assert "private_full_paths_printed=False" in output
