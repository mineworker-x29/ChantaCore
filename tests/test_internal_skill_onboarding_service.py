import pytest

from chanta_core.skills.onboarding import InternalSkillOnboardingService


def _bundle(service: InternalSkillOnboardingService):
    return service.create_read_only_skill_contract_bundle(
        skill_id="skill:workspace_summary_from_file"
    )


def test_complete_read_only_skill_contract_validates_accepted_and_disabled() -> None:
    service = InternalSkillOnboardingService()
    result = service.validate_onboarding(**_bundle(service))

    assert result.status == "accepted"
    assert result.accepted is True
    assert result.enabled is False
    assert result.result_attrs["skills_executed"] is False
    assert result.result_attrs["runtime_registered"] is False
    assert result.result_attrs["permission_grants_created"] is False


@pytest.mark.parametrize(
    ("missing_key", "finding_type"),
    [
        ("input_contract", "missing_input_contract"),
        ("output_contract", "missing_output_contract"),
        ("risk_profile", "missing_risk_profile"),
        ("gate_contract", "missing_gate_contract"),
        ("observability_contract", "missing_observability_contract"),
    ],
)
def test_missing_contracts_produce_needs_fix(missing_key: str, finding_type: str) -> None:
    service = InternalSkillOnboardingService()
    bundle = _bundle(service)
    bundle[missing_key] = None

    result = service.validate_onboarding(**bundle)

    assert result.status == "needs_fix"
    assert result.accepted is False
    assert finding_type in {finding.finding_type for finding in service.last_findings}


def test_missing_ocel_mapping_produces_needs_fix() -> None:
    service = InternalSkillOnboardingService()
    bundle = _bundle(service)
    bundle["observability_contract"] = service.create_observability_contract(
        skill_id=bundle["descriptor"].skill_id,
        ocel_object_types=[],
        ocel_event_activities=[],
        required_relations=[],
        pig_report_keys=["internal_skill_descriptor_count"],
        ocpx_projection_keys=["internal_skill_onboarding_by_risk_class"],
    )

    result = service.validate_onboarding(**bundle)

    assert result.status == "needs_fix"
    assert "missing_ocel_mapping" in {finding.finding_type for finding in service.last_findings}


def test_missing_pig_and_ocpx_mapping_produces_needs_fix() -> None:
    service = InternalSkillOnboardingService()
    bundle = _bundle(service)
    bundle["observability_contract"] = service.create_observability_contract(
        skill_id=bundle["descriptor"].skill_id,
        pig_report_keys=[],
        ocpx_projection_keys=[],
    )

    result = service.validate_onboarding(**bundle)
    finding_types = {finding.finding_type for finding in service.last_findings}

    assert result.status == "needs_fix"
    assert "missing_pig_report_mapping" in finding_types
    assert "missing_ocpx_projection_mapping" in finding_types


@pytest.mark.parametrize("risk_class", ["write", "shell", "network", "mcp", "plugin"])
def test_unsafe_risk_classes_are_blocked(risk_class: str) -> None:
    service = InternalSkillOnboardingService()
    descriptor = service.create_descriptor(
        skill_id=f"skill:{risk_class}_candidate",
        skill_name="Unsafe Candidate",
        description="Unsafe public-safe dummy candidate.",
        capability_category=risk_class,
        risk_class=risk_class,
    )
    bundle = service.create_read_only_skill_contract_bundle(skill_id=descriptor.skill_id)
    bundle["descriptor"] = descriptor
    bundle["risk_profile"] = service.create_risk_profile(
        skill_id=descriptor.skill_id,
        risk_class=risk_class,
        read_only=False,
        touches_network=risk_class == "network",
        touches_shell=risk_class == "shell",
    )

    result = service.validate_onboarding(**bundle)

    assert result.status == "blocked"
    assert result.accepted is False
    assert "unsafe_category_blocked" in {finding.finding_type for finding in service.last_findings}


def test_envelope_required_and_visibility_are_enforced() -> None:
    service = InternalSkillOnboardingService()
    bundle = _bundle(service)
    bundle["observability_contract"] = service.create_observability_contract(
        skill_id=bundle["descriptor"].skill_id,
        envelope_required=False,
        audit_visible=False,
        workbench_visible=False,
    )

    result = service.validate_onboarding(**bundle)
    finding_types = {finding.finding_type for finding in service.last_findings}

    assert result.status == "needs_fix"
    assert "missing_envelope_support" in finding_types
    assert "missing_operator_visibility" in finding_types
