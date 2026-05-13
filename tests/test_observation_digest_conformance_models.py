from chanta_core.skills.observation_digest_conformance import (
    ObservationDigestConformanceCheck,
    ObservationDigestConformanceFinding,
    ObservationDigestConformancePolicy,
    ObservationDigestConformanceReport,
    ObservationDigestSmokeCase,
    ObservationDigestSmokeResult,
)
from chanta_core.utility.time import utc_now_iso


def test_observation_digest_conformance_models_to_dict():
    now = utc_now_iso()
    policy = ObservationDigestConformancePolicy(
        policy_id="observation_digest_conformance_policy:test",
        policy_name="test",
        required_skill_ids=["skill:agent_trace_observe"],
        require_registry_entry=True,
        require_onboarding_result=True,
        require_input_contract=True,
        require_output_contract=True,
        require_risk_profile=True,
        require_gate_contract=True,
        require_observability_contract=True,
        require_envelope=True,
        require_ocel_events=True,
        require_pig_visibility=True,
        require_audit_visibility=True,
        require_workbench_visibility=True,
        deny_external_execution=True,
        deny_shell_network_write=True,
        deny_memory_persona_overlay_mutation=True,
        status="active",
        created_at=now,
    )
    check = ObservationDigestConformanceCheck(
        check_id="observation_digest_conformance_check:test",
        skill_id="skill:agent_trace_observe",
        check_type="registry_entry",
        status="passed",
        passed=True,
        severity="info",
        message="ok",
        evidence_refs=[],
        created_at=now,
    )
    case = ObservationDigestSmokeCase(
        smoke_case_id="observation_digest_smoke_case:test",
        skill_id="skill:agent_trace_observe",
        case_name="trace",
        input_payload={"root_path": "redacted"},
        expected_status="completed",
        expected_created_object_types=["observed_agent_run"],
        expected_findings=[],
        should_execute=True,
        should_block=False,
        should_create_envelope=True,
        should_mutate_state=False,
        created_at=now,
    )
    result = ObservationDigestSmokeResult(
        smoke_result_id="observation_digest_smoke_result:test",
        smoke_case_id=case.smoke_case_id,
        skill_id=case.skill_id,
        status="completed",
        passed=True,
        executed=True,
        blocked=False,
        envelope_id="execution_envelope:test",
        created_object_refs=["observed_agent_run:test"],
        finding_ids=[],
        summary="ok",
        created_at=now,
    )
    finding = ObservationDigestConformanceFinding(
        finding_id="observation_digest_conformance_finding:test",
        skill_id=case.skill_id,
        check_id=check.check_id,
        finding_type="none",
        status="passed",
        severity="info",
        message="ok",
        evidence_ref=None,
        created_at=now,
    )
    report = ObservationDigestConformanceReport(
        report_id="observation_digest_conformance_report:test",
        policy_id=policy.policy_id,
        total_skill_count=1,
        passed_skill_count=1,
        failed_skill_count=0,
        warning_skill_count=0,
        total_check_count=1,
        passed_check_count=1,
        failed_check_count=0,
        smoke_case_count=1,
        smoke_passed_count=1,
        smoke_failed_count=0,
        finding_ids=[],
        status="passed",
        summary="ok",
        created_at=now,
    )

    assert policy.to_dict()["deny_shell_network_write"] is True
    assert check.to_dict()["passed"] is True
    assert case.to_dict()["input_payload"]["root_path"] == "<redacted>"
    assert result.to_dict()["envelope_id"] == "execution_envelope:test"
    assert finding.to_dict()["finding_type"] == "none"
    assert report.to_dict()["status"] == "passed"
