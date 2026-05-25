from __future__ import annotations

import subprocess
import sys

from chanta_core.internal_dominion import (
    CONTROL_REQUEST_NEXT_STEP,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
    ControlTargetRef,
    DominionActionInputDraft,
    DominionControlRequestCandidateService,
    DominionControlRequestCreateRequest,
    DominionNeedsMoreInputCandidate,
    DominionNoActionCandidate,
    ExternalActionCandidate,
    InternalDominionRegistryService,
)


def test_control_request_doc_records_v0_23_3_identity_and_boundaries() -> None:
    text = open("docs/versions/v0.23/v0.23.3_control_request_action_candidate.md", encoding="utf-8").read()

    assert "Control Request & Action Candidate" in text
    assert "Track: Internal Dominion Foundation" in text
    assert "Control request is not dispatch" in text
    assert "Control request is not control plan" in text
    assert "Action candidate is not external runtime touch" in text
    assert "Action candidate is not preflight" in text
    assert "Action candidate is not authorization" in text
    assert "No-action and needs-more-input are valid outcomes" in text
    assert "v0.23.4 Control Plan & Target Binding" in text


def test_control_request_and_external_action_candidate_can_be_created() -> None:
    report = DominionControlRequestCandidateService().create_request_and_candidate(
        DominionControlRequestCreateRequest(goal_text="observe status", requested_action_verb="observe")
    )

    assert report.version == "v0.23.3"
    assert report.report_status == "candidate_created"
    assert report.request.request_status == "candidate_created"
    assert report.request.review_status == "request_only"
    assert report.action_candidate is not None
    candidate = report.action_candidate
    assert candidate.candidate_status == "candidate_only"
    assert candidate.lifecycle_state == "action_candidate_created"
    assert candidate.control_plan_required is True
    assert candidate.target_binding_required is True
    assert candidate.static_safety_required is True
    assert candidate.preflight_required is True
    assert candidate.human_gate_required is True
    assert candidate.authorization_required is True
    assert candidate.status_tracking_required is True
    assert candidate.outcome_record_required is True
    assert candidate.control_plan_created is False
    assert candidate.target_bound is False
    assert candidate.static_safety_checked is False
    assert candidate.preflight_checked is False
    assert candidate.human_gate_opened is False
    assert candidate.authorization_created is False
    assert candidate.dispatch_enabled is False
    assert candidate.dispatched is False
    assert candidate.external_runtime_touched is False
    assert candidate.provider_api_call_performed is False
    assert candidate.credential_exposed is False
    assert candidate.raw_secret_output is False
    assert report.next_required_step == CONTROL_REQUEST_NEXT_STEP


def test_missing_unknown_credential_and_destructive_paths_create_expected_candidates() -> None:
    missing = DominionControlRequestCandidateService().create_request_and_candidate(
        DominionControlRequestCreateRequest(
            goal_text="do something",
            capability_candidate_ids=["missing"],
            requested_action_verb="unknown",
        )
    )
    assert missing.report_status == "needs_more_input"
    assert missing.needs_more_input_candidate is not None

    blocked = DominionControlRequestCandidateService().create_request_and_candidate(
        DominionControlRequestCreateRequest(
            goal_text="observe status",
            requested_action_verb="observe",
            requested_inputs={"credential_value": "hidden"},
        )
    )
    assert blocked.report_status == "blocked"
    assert "credential_value_detected" in {item.finding_type for item in blocked.findings}

    no_action = DominionControlRequestCandidateService().create_request_and_candidate(
        DominionControlRequestCreateRequest(goal_text="delete production", requested_action_verb="delete")
    )
    assert no_action.report_status == "no_action"
    assert no_action.no_action_candidate is not None


def test_control_models_and_constraints_are_candidate_only() -> None:
    target = ControlTargetRef("target:1", "runtime", runtime_id="runtime:1", target_status="resolved")
    input_draft = DominionActionInputDraft(
        "draft:1",
        "candidate:1",
        {"schema_id": "schema:1"},
        {"field": "value"},
        ["missing"],
        ["credential_ref"],
        credential_values_present=False,
    )
    no_action = DominionNoActionCandidate("no:1", "request:1", "reason", [])
    needs_more = DominionNeedsMoreInputCandidate("more:1", "request:1", "reason", ["field"], [])

    assert target.dispatch_enabled is False
    assert target.external_runtime_touched is False
    assert target.provider_api_call_performed is False
    assert input_draft.raw_secret_output is False
    assert no_action.candidate_status == "candidate_only"
    assert no_action.dispatched is False
    assert needs_more.candidate_status == "candidate_only"
    assert needs_more.dispatched is False


def test_control_pig_ocpx_mapping_and_skill_statuses() -> None:
    service = DominionControlRequestCandidateService()
    pig = service.build_pig_report()
    ocpx = service.build_ocpx_projection()
    skills = {item["skill_id"]: item for item in InternalDominionRegistryService().list_skill_contracts()}

    for object_type in [
        "dominion_control_request_create_request",
        "dominion_control_request",
        "control_target_ref",
        "dominion_action_intent_descriptor",
        "dominion_action_input_draft",
        "dominion_control_constraint",
        "dominion_preliminary_action_risk",
        "dominion_action_candidate_finding",
        "external_action_candidate",
        "dominion_no_action_candidate",
        "dominion_needs_more_input_candidate",
        "dominion_control_request_candidate_report",
    ]:
        assert object_type in DOMINION_OCEL_OBJECT_TYPES
    assert "dominion_control_request_received" in DOMINION_OCEL_EVENT_TYPES
    assert "external_action_candidate_created" in DOMINION_OCEL_EVENT_TYPES
    assert "requests_external_control" in DOMINION_OCEL_RELATION_TYPES
    assert "not_dispatched" in DOMINION_OCEL_RELATION_TYPES
    assert pig["version"] == "v0.23.3"
    assert pig["subject"] == "control_request_action_candidate"
    assert pig["safety_boundary"]["control_plan_created"] is False
    assert pig["safety_boundary"]["preflight_checked"] is False
    assert pig["safety_boundary"]["authorization_created"] is False
    assert pig["safety_boundary"]["dispatched"] is False
    assert ocpx["state"] == "dominion_external_action_candidate_created"
    assert "ExternalActionCandidateState" in ocpx["target_read_models"]
    assert skills["skill:dominion_control_request_create"]["status"] == "candidate_only"
    assert skills["skill:dominion_action_candidate_create"]["status"] == "candidate_only"
    assert skills["skill:dominion_control_plan_create"]["status"] == "plan_only"


def test_control_cli_views_are_sanitized() -> None:
    commands = [
        ["control", "request", "create", "--goal", "observe status"],
        ["control", "request", "report", "--report-id", "dominion_control_request_candidate_report:v0.23.3"],
        ["action", "candidate", "create", "--goal", "observe status"],
        ["action", "candidates"],
        ["action", "candidate", "view", "--candidate-id", "external_action_candidate:v0.23.3"],
        ["action", "candidate", "findings", "--candidate-id", "external_action_candidate:v0.23.3"],
    ]
    for command in commands:
        completed = subprocess.run(
            [sys.executable, "-m", "chantacore.cli", "dominion", *command],
            check=False,
            capture_output=True,
            text=True,
        )
        assert completed.returncode == 0
        assert "request_id=" in completed.stdout
        assert "action_candidate_id=" in completed.stdout
        assert "candidate_status=candidate_only" in completed.stdout
        assert "control_plan_created=false" in completed.stdout
        assert "preflight_checked=false" in completed.stdout
        assert "human_gate_opened=false" in completed.stdout
        assert "authorization_created=false" in completed.stdout
        assert "dispatch_enabled=false" in completed.stdout
        assert "dispatched=false" in completed.stdout
        assert "external_runtime_touched=false" in completed.stdout
        assert "provider_api_call_performed=false" in completed.stdout
        assert "credential_exposed=false" in completed.stdout
        assert "next_required_step=v0.23.4 Control Plan & Target Binding" in completed.stdout
        assert "raw_secrets_printed=False" in completed.stdout
        assert "private_full_paths_printed=False" in completed.stdout
