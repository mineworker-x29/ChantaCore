from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.onboarding import InternalSkillOnboardingService


def test_internal_skill_onboarding_records_ocel_objects_events_and_relations(tmp_path) -> None:
    store = OCELStore(tmp_path / "internal_skill_onboarding.sqlite")
    service = InternalSkillOnboardingService(ocel_store=store)
    bundle = service.create_read_only_skill_contract_bundle(skill_id="skill:workspace_summary_from_file")

    result = service.validate_onboarding(**bundle)

    assert result.status == "accepted"
    for object_type in [
        "internal_skill_descriptor",
        "internal_skill_input_contract",
        "internal_skill_output_contract",
        "internal_skill_risk_profile",
        "internal_skill_gate_contract",
        "internal_skill_observability_contract",
        "internal_skill_onboarding_review",
        "internal_skill_onboarding_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "internal_skill_descriptor_registered" in events
    assert "internal_skill_input_contract_registered" in events
    assert "internal_skill_output_contract_registered" in events
    assert "internal_skill_risk_profile_registered" in events
    assert "internal_skill_gate_contract_registered" in events
    assert "internal_skill_observability_contract_registered" in events
    assert "internal_skill_onboarding_review_requested" in events
    assert "internal_skill_onboarding_result_recorded" in events
    assert "internal_skill_onboarding_accepted" in events
    relations = store.fetch_object_object_relations_for_object(result.result_id)
    assert any(item["qualifier"] == "onboarding_result_summarizes_review" for item in relations)
    assert any(item["qualifier"] == "onboarding_result_summarizes_descriptor" for item in relations)


def test_internal_skill_onboarding_pig_ocpx_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "internal_skill_onboarding_pig.sqlite")
    service = InternalSkillOnboardingService(ocel_store=store)
    accepted_bundle = service.create_read_only_skill_contract_bundle(skill_id="skill:execution_audit")
    service.validate_onboarding(**accepted_bundle)
    missing_bundle = service.create_read_only_skill_contract_bundle(skill_id="skill:workbench_status")
    missing_bundle["input_contract"] = None
    service.validate_onboarding(**missing_bundle)
    unsafe_descriptor = service.create_descriptor(
        skill_id="skill:network_candidate",
        skill_name="Network Candidate",
        description="Unsafe dummy candidate.",
        capability_category="network",
        risk_class="network",
    )
    unsafe_bundle = service.create_read_only_skill_contract_bundle(skill_id=unsafe_descriptor.skill_id)
    unsafe_bundle["descriptor"] = unsafe_descriptor
    service.validate_onboarding(**unsafe_bundle)

    objects = []
    for object_type in [
        "internal_skill_descriptor",
        "internal_skill_input_contract",
        "internal_skill_output_contract",
        "internal_skill_risk_profile",
        "internal_skill_gate_contract",
        "internal_skill_observability_contract",
        "internal_skill_onboarding_review",
        "internal_skill_onboarding_finding",
        "internal_skill_onboarding_result",
    ]:
        for row in store.fetch_objects_by_type(object_type):
            objects.append(
                type(
                    "Obj",
                    (),
                    {
                        "object_id": row["object_id"],
                        "object_type": row["object_type"],
                        "object_attrs": row["object_attrs"],
                    },
                )()
            )
    view = OCPXProcessView(view_id="view:test", source="test", session_id=None, events=[], objects=objects)
    summary = PIGReportService._skill_usage_summary(view)

    assert summary["internal_skill_descriptor_count"] >= 3
    assert summary["internal_skill_input_contract_count"] >= 3
    assert summary["internal_skill_output_contract_count"] >= 3
    assert summary["internal_skill_risk_profile_count"] >= 3
    assert summary["internal_skill_gate_contract_count"] >= 3
    assert summary["internal_skill_observability_contract_count"] >= 3
    assert summary["internal_skill_onboarding_review_count"] == 3
    assert summary["internal_skill_onboarding_result_count"] == 3
    assert summary["internal_skill_onboarding_accepted_count"] == 1
    assert summary["internal_skill_onboarding_needs_fix_count"] == 1
    assert summary["internal_skill_onboarding_blocked_count"] == 1
    assert summary["internal_skill_onboarding_by_capability_category"]["audit"] >= 1
    assert summary["internal_skill_onboarding_by_risk_class"]["read_only"] >= 1
    assert summary["internal_skill_onboarding_finding_by_type"]["missing_input_contract"] == 1
    assert summary["internal_skill_onboarding_finding_by_type"]["unsafe_category_blocked"] == 1
