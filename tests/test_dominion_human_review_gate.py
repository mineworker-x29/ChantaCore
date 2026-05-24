from __future__ import annotations

from chanta_core.cli.main import build_parser, run_dominion
from chanta_core.internal_dominion import (
    APPROVAL_PHRASE,
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    DominionGateAuthorization,
    DominionGateCondition,
    DominionGateFinding,
    DominionGateNeedsMoreInputCandidate,
    DominionGateNoActionCandidate,
    DominionGateRejectionRecord,
    DominionGateReport,
    DominionGateState,
    DominionHumanReviewGateService,
    DominionHumanReviewRequestCreateRequest,
    DominionReviewDecision,
    DominionReviewDecisionInput,
    DominionReviewSourceBundle,
    DominionReviewSummary,
    HUMAN_REVIEW_GATE_NEXT_STEP,
    InternalDominionRegistryService,
)


def _report(
    preflight_report_id: str = "dominion_runtime_preflight_report:v0.23.6",
    decision: str | None = "approve",
    phrase: str | None = APPROVAL_PHRASE,
    rationale: str | None = "operator reviewed declared readiness",
):
    return DominionHumanReviewGateService().review_and_gate(
        DominionHumanReviewRequestCreateRequest(
            preflight_report_id=preflight_report_id,
            requested_review_decision=decision,
            approval_phrase=phrase,
            decision_rationale=rationale,
        )
    )


def test_human_review_gate_doc_records_identity_roadmap_and_boundaries() -> None:
    text = open("docs/versions/v0.23.7_human_review_dominion_gate.md", encoding="utf-8").read()

    assert "Human Review & Dominion Gate" in text
    assert "Korean name: 인간 검토·지배 게이트" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Human review is not dispatch" in text
    assert "Dominion gate is not dispatch" in text
    assert "Gate authorization is not execution" in text
    assert "Gate authorization is single-use and scoped" in text
    assert "v0.24.x: Internal Provider / Local Runtime Provider" in text
    assert "v0.25.x: General Agent Usability & Tool Routing" in text
    assert "v0.26.x: Workspace Agent Workbench" in text
    assert "v0.27.x: Memory Candidate & Continuity" in text
    assert "v0.28.x: Public Alpha / Schumpeter Split Preparation" in text
    assert "v0.29.x+: External Skill / External Provider Adapter Development" in text
    assert "v0.23.8 Authorization / Bounded Dispatch / Status / Outcome Boundary" in text


def test_human_review_gate_report_can_open_with_scoped_unconsumed_authorization() -> None:
    report = _report()

    assert report.version == "v0.23.7"
    assert report.report_id == "dominion_gate_report:v0.23.7"
    assert report.report_status == "open"
    assert report.gate_state is not None
    assert report.gate_state.gate_status == "open"
    assert report.authorization is not None
    assert report.authorization.single_use is True
    assert report.authorization.consumed is False
    assert report.authorization.expired is False
    assert report.authorization.dispatch_performed is False
    assert report.authorization.external_runtime_touched is False
    assert report.authorization.provider_api_call_performed is False
    assert report.authorization.credential_exposed is False
    assert report.authorization.scope["preflight_report_id"] == report.review_source_bundle.preflight_report_ref["report_id"]
    assert report.authorization.scope["plan_id"] == report.review_summary.plan_id
    assert report.authorization.scope["action_candidate_id"] == report.review_summary.action_candidate_id
    assert report.eligible_for_v0_23_8 is True
    assert report.safe_to_dispatch is False
    assert report.bounded_dispatch_allowed_now is False
    assert report.authorization_consumed is False
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
    assert report.next_required_step == HUMAN_REVIEW_GATE_NEXT_STEP


def test_human_review_gate_model_types_are_exported() -> None:
    assert DominionHumanReviewRequestCreateRequest
    assert DominionReviewSourceBundle
    assert DominionReviewSummary
    assert DominionReviewDecisionInput
    assert DominionReviewDecision
    assert DominionGateCondition
    assert DominionGateState
    assert DominionGateAuthorization
    assert DominionGateFinding
    assert DominionGateReport
    assert DominionGateNeedsMoreInputCandidate
    assert DominionGateNoActionCandidate
    assert DominionGateRejectionRecord


def test_review_summary_and_decision_input_are_created() -> None:
    report = _report()
    summary = report.review_summary
    decision_input = report.decision_input

    assert summary.plan_id == "dominion_control_plan:v0.23.4"
    assert summary.action_candidate_id == "external_action_candidate:v0.23.3"
    assert summary.goal_text
    assert summary.provider_summary
    assert summary.runtime_summary
    assert summary.capability_summary
    assert summary.environment
    assert summary.static_safety_status in {"passed", "warning"}
    assert summary.preflight_status in {"passed", "warning"}
    assert summary.eligible_for_dominion_gate is True
    assert summary.safe_to_dispatch is False
    assert summary.raw_secret_output is False
    assert decision_input.requested_review_decision == "approve"
    assert decision_input.explicit_human_approval is True
    assert decision_input.approval_phrase_matches is True
    assert report.review_decision.decision_status == "accepted"


def test_gate_conditions_are_created() -> None:
    condition_types = {item.condition_type for item in _report().gate_state.conditions}

    for expected in {
        "preflight_report_exists",
        "preflight_eligible_for_gate",
        "static_safety_passed_or_acceptable_warning",
        "control_plan_exists",
        "action_candidate_exists",
        "no_provider_api_call",
        "no_external_runtime_touch",
        "no_dispatch_yet",
        "no_credential_exposure",
        "explicit_human_approval_required_for_approve",
        "approval_phrase_required_for_high_risk",
        "approval_phrase_matches_if_required",
        "strong_gate_required_for_production",
        "no_vendor_hardcoding_in_core",
        "no_growthkernel_dependency",
        "no_premature_local_runtime_provider",
        "no_premature_general_agent_usability",
        "no_schumpeter_split",
    }:
        assert expected in condition_types


def test_gate_status_paths_and_no_authorization_outcomes() -> None:
    cases = {
        "reject": ("rejected", "gate_rejected"),
        "no_action": ("no_action", "gate_no_action"),
        "needs_more_input": ("needs_more_input", "gate_needs_more_input"),
        "defer": ("needs_more_input", "gate_needs_more_input"),
    }
    for decision, (status, finding_type) in cases.items():
        report = _report(decision=decision, phrase=None, rationale="operator selected alternate outcome")
        assert report.report_status == status
        assert report.authorization is None
        assert report.authorization_created is False
        assert report.eligible_for_v0_23_8 is False
        assert finding_type in {item.finding_type for item in report.findings}


def test_approve_requires_explicit_review_and_phrase_for_high_risk() -> None:
    missing_input = _report(preflight_report_id="production", decision="approve", phrase=None, rationale=None)
    mismatch = _report(preflight_report_id="production", decision="approve", phrase="wrong phrase")
    approved = _report(preflight_report_id="production", decision="approve", phrase=APPROVAL_PHRASE)

    assert missing_input.report_status in {"blocked", "rejected"}
    assert "explicit_human_approval_missing" in {item.finding_type for item in missing_input.findings}
    assert "approval_phrase_missing" in {item.finding_type for item in missing_input.findings}
    assert mismatch.report_status in {"blocked", "rejected"}
    assert "approval_phrase_mismatch" in {item.finding_type for item in mismatch.findings}
    assert approved.report_status == "open"
    assert approved.authorization is not None
    assert approved.review_summary.production_impacting is True


def test_gate_blocks_hard_source_and_boundary_violations() -> None:
    cases = {
        "missing": "missing_preflight_report",
        "not-eligible": "preflight_not_eligible",
        "static-failed": "static_safety_not_passed",
        "provider-api": "provider_api_call_performed",
        "runtime-touch": "external_runtime_touched",
        "dispatch": "preflight_not_eligible",
        "credential": "credential_exposure_risk",
        "raw-secret": "static_safety_not_passed",
    }
    for preflight_id, finding_type in cases.items():
        report = _report(preflight_report_id=preflight_id)
        assert report.report_status == "blocked"
        assert report.authorization is None
        assert finding_type in {item.finding_type for item in report.findings}
        assert report.safe_to_dispatch is False


def test_no_action_needs_more_input_and_rejection_records_are_non_dispatching() -> None:
    service = DominionHumanReviewGateService()
    no_action = _report(decision="no_action", phrase=None, rationale="risk outweighs value")
    needs_more = _report(decision="needs_more_input", phrase=None, rationale="scope unclear")
    rejected = _report(decision="reject", phrase=None, rationale="operator rejected")

    no_action_candidate = service.create_no_action_candidate(no_action)
    needs_more_candidate = service.create_needs_more_input_candidate(needs_more)
    rejection = service.create_rejection_record(rejected)

    assert no_action_candidate.dispatched is False
    assert no_action_candidate.recommended_review_decision == "no_action"
    assert needs_more_candidate.dispatched is False
    assert needs_more_candidate.recommended_review_decision == "needs_more_input"
    assert rejection.dispatch_allowed is False
    assert rejection.dispatched is False


def test_gate_ocel_pig_ocpx_mapping_and_skill_statuses() -> None:
    service = DominionHumanReviewGateService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for object_type in [
        "dominion_human_review_request_create_request",
        "dominion_review_source_bundle",
        "dominion_review_summary",
        "dominion_review_decision_input",
        "dominion_review_decision",
        "dominion_gate_condition",
        "dominion_gate_state",
        "dominion_gate_authorization",
        "dominion_gate_finding",
        "dominion_gate_report",
        "dominion_gate_needs_more_input_candidate",
        "dominion_gate_no_action_candidate",
        "dominion_gate_rejection_record",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    for event_type in [
        "dominion_human_review_requested",
        "dominion_gate_sources_loaded",
        "dominion_review_decision_recorded",
        "dominion_gate_opened",
        "dominion_gate_authorization_created",
        "dominion_gate_report_created",
        "dominion_gate_blocked",
    ]:
        assert event_type in DOMINION_OCEL_EVENT_TYPES
    for relation_type in [
        "reviews_dominion_preflight",
        "uses_preflight_report",
        "summarizes_for_human_review",
        "records_review_decision",
        "evaluates_gate_condition",
        "opens_dominion_gate",
        "produces_dominion_gate_authorization",
        "authorization_scoped_to_preflight",
        "authorization_scoped_to_plan",
        "authorization_scoped_to_action_candidate",
        "requires_bounded_dispatch_boundary",
        "eligible_for_v0_23_8",
        "not_authorization_consumed",
        "derived_from_runtime_preflight_report",
    ]:
        assert relation_type in DOMINION_OCEL_RELATION_TYPES
    assert set(DOMINION_EFFECT_TYPES) == {
        "read_only_observation",
        "state_candidate_created",
        "gate_state_created",
        "boundary_state_created",
        "consolidation_state_created",
        "workbench_snapshot_created",
    }
    assert pig["version"] == "v0.23.7"
    assert pig["subject"] == "human_review_dominion_gate"
    assert pig["safety_boundary"]["gate_state_created"] is True
    assert pig["safety_boundary"]["authorization_created"] == "conditional"
    assert pig["safety_boundary"]["authorization_consumed"] is False
    assert pig["safety_boundary"]["safe_to_dispatch"] is False
    assert pig["safety_boundary"]["bounded_dispatch_allowed_now"] is False
    assert pig["roadmap"]["v0.24"] == "Internal Provider / Local Runtime Provider"
    assert pig["roadmap"]["v0.25"] == "General Agent Usability & Tool Routing"
    assert ocpx["state"] == "dominion_gate_opened_or_review_recorded"
    assert "DominionHumanReviewState" in ocpx["target_read_models"]
    assert "DominionGateState" in ocpx["target_read_models"]
    assert "DominionGateAuthorizationState" in ocpx["target_read_models"]
    assert "DominionV0238EligibilityState" in ocpx["target_read_models"]
    assert skills["skill:dominion_review_gate"]["status"] == "review_gate_only"
    assert skills["skill:dominion_authorization_create"]["status"] == "gate_authorization_only"
    assert skills["skill:dominion_bounded_dispatch"]["status"] == "boundary_only"


def test_gate_cli_views_are_sanitized(capsys) -> None:
    parser = build_parser()
    commands = [
        [
            "dominion",
            "gate",
            "review",
            "--preflight-report-id",
            "dominion_runtime_preflight_report:v0.23.6",
            "--decision",
            "approve",
            "--approval-phrase",
            APPROVAL_PHRASE,
            "--rationale",
            "operator reviewed declared readiness",
        ],
        [
            "dominion",
            "gate",
            "review",
            "--preflight-report-id",
            "dominion_runtime_preflight_report:v0.23.6",
            "--decision",
            "reject",
            "--rationale",
            "operator rejected",
        ],
        [
            "dominion",
            "gate",
            "review",
            "--preflight-report-id",
            "dominion_runtime_preflight_report:v0.23.6",
            "--decision",
            "no_action",
        ],
        [
            "dominion",
            "gate",
            "review",
            "--preflight-report-id",
            "dominion_runtime_preflight_report:v0.23.6",
            "--decision",
            "needs_more_input",
        ],
        ["dominion", "gate", "report", "--report-id", "dominion_gate_report:v0.23.7"],
        ["dominion", "gate", "state", "--gate-id", "dominion_gate_state:v0.23.7"],
        ["dominion", "gate", "authorization", "--authorization-id", "dominion_gate_authorization:v0.23.7"],
        ["dominion", "gate", "findings", "--report-id", "dominion_gate_report:v0.23.7"],
    ]
    for command in commands:
        args = parser.parse_args(command)
        assert run_dominion(args) == 0
        output = capsys.readouterr().out
        assert "report_id=dominion_gate_report:v0.23.7" in output
        assert "gate_id=dominion_gate_state:v0.23.7" in output
        assert "gate_status=" in output
        assert "review_decision=" in output
        assert "authorization.consumed=false" in output
        assert "safe_to_dispatch=false" in output
        assert "bounded_dispatch_allowed_now=false" in output
        assert "provider_api_call_performed=false" in output
        assert "external_runtime_touched=false" in output
        assert "dispatch_enabled=false" in output
        assert "dispatched=false" in output
        assert "credential_exposed=false" in output
        assert "local_runtime_provider_implemented=false" in output
        assert "general_agent_usability_implemented=false" in output
        assert "schumpeter_split_introduced=false" in output
        assert "next_required_step=v0.23.8 Authorization / Bounded Dispatch / Status / Outcome Boundary" in output
        assert "raw_secrets_printed=False" in output
        assert "private_full_paths_printed=False" in output
