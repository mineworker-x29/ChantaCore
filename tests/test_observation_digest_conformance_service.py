from chanta_core.observation_digest import OBSERVATION_DIGESTION_SKILL_IDS
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.observation_digest_conformance import ObservationDigestConformanceService


class EmptyRegistry:
    last_entries = []

    def build_registry_view(self):
        return object()


def test_default_policy_includes_all_10_target_skills():
    service = ObservationDigestConformanceService()

    policy = service.create_default_policy()

    assert policy.required_skill_ids == sorted(OBSERVATION_DIGESTION_SKILL_IDS)
    assert len(policy.required_skill_ids) == 10


def test_conformance_checks_registry_entry_for_each_skill():
    service = ObservationDigestConformanceService()

    report = service.run_conformance()

    registry_checks = [check for check in service.last_checks if check.check_type == "registry_entry"]
    assert report.total_skill_count == 10
    assert len(registry_checks) == 10
    assert all(check.passed for check in registry_checks)


def test_missing_registry_entry_produces_finding():
    service = ObservationDigestConformanceService(registry_view_service=EmptyRegistry())

    report = service.run_conformance(skill_id="skill:agent_trace_observe")

    assert report.status == "failed"
    assert any(finding.finding_type == "registry_entry" for finding in service.last_findings)


def test_contract_gate_observability_checks_pass_for_seed_skill():
    service = ObservationDigestConformanceService()

    report = service.run_conformance(skill_id="skill:agent_trace_observe")

    check_types = {check.check_type for check in service.last_checks}
    assert report.status == "passed"
    assert {"input_contract", "output_contract", "risk_profile", "gate_contract", "observability_contract"} <= check_types


def test_candidate_safety_check_verifies_non_executable_defaults():
    service = ObservationDigestConformanceService()

    check = service.check_candidate_safety("skill:external_skill_assimilate")

    assert check.passed is True


def test_observation_digest_conformance_pig_counts_are_visible():
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="check:one",
                object_type="observation_digest_conformance_check",
                object_attrs={"check_type": "registry_entry", "skill_id": "skill:agent_trace_observe"},
            ),
            OCPXObjectView(
                object_id="smoke:one",
                object_type="observation_digest_smoke_result",
                object_attrs={"passed": True},
            ),
            OCPXObjectView(
                object_id="finding:one",
                object_type="observation_digest_conformance_finding",
                object_attrs={"finding_type": "missing_contract"},
            ),
            OCPXObjectView(
                object_id="report:one",
                object_type="observation_digest_conformance_report",
                object_attrs={"passed_skill_count": 1, "failed_skill_count": 0},
            ),
        ],
    )

    summary = PIGReportService._observation_digest_conformance_summary(
        {
            "observation_digest_conformance_check": 1,
            "observation_digest_smoke_result": 1,
            "observation_digest_conformance_finding": 1,
            "observation_digest_conformance_report": 1,
        },
        {},
        view,
    )

    assert summary["observation_digest_conformance_check_count"] == 1
    assert summary["observation_digest_smoke_passed_count"] == 1
    assert summary["observation_digest_conformance_finding_by_type"] == {"missing_contract": 1}
