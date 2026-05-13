from chanta_core.skills.history_adapter import (
    internal_skill_descriptors_to_history_entries,
    internal_skill_observability_contracts_to_history_entries,
    internal_skill_onboarding_findings_to_history_entries,
    internal_skill_onboarding_results_to_history_entries,
)
from chanta_core.skills.onboarding import InternalSkillOnboardingService


def test_internal_skill_onboarding_history_entries() -> None:
    service = InternalSkillOnboardingService()
    bundle = service.create_read_only_skill_contract_bundle(skill_id="skill:execution_audit")
    accepted = service.validate_onboarding(**bundle)
    blocked_descriptor = service.create_descriptor(
        skill_id="skill:shell_candidate",
        skill_name="Shell Candidate",
        description="Unsafe dummy candidate.",
        capability_category="shell",
        risk_class="shell",
    )
    blocked_bundle = service.create_read_only_skill_contract_bundle(skill_id=blocked_descriptor.skill_id)
    blocked_bundle["descriptor"] = blocked_descriptor
    blocked = service.validate_onboarding(**blocked_bundle)

    descriptor_entry = internal_skill_descriptors_to_history_entries([bundle["descriptor"]])[0]
    result_entries = internal_skill_onboarding_results_to_history_entries([accepted, blocked])
    finding_entry = internal_skill_onboarding_findings_to_history_entries(service.last_findings)[0]
    observability_entry = internal_skill_observability_contracts_to_history_entries(
        [bundle["observability_contract"]]
    )[0]

    assert descriptor_entry.source == "internal_skill_onboarding"
    assert descriptor_entry.priority < result_entries[0].priority
    assert result_entries[0].entry_attrs["status"] == "accepted"
    assert result_entries[1].priority >= 90
    assert finding_entry.priority >= 90
    assert observability_entry.entry_attrs["envelope_required"] is True
