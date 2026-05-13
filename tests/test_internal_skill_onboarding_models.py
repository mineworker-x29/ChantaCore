from chanta_core.skills.onboarding import (
    InternalSkillDescriptor,
    InternalSkillGateContract,
    InternalSkillInputContract,
    InternalSkillObservabilityContract,
    InternalSkillOnboardingFinding,
    InternalSkillOnboardingResult,
    InternalSkillOnboardingReview,
    InternalSkillOutputContract,
    InternalSkillRiskProfile,
    InternalSkillOnboardingService,
)
from chanta_core.utility.time import utc_now_iso


def test_internal_skill_onboarding_models_to_dict() -> None:
    now = utc_now_iso()
    descriptor = InternalSkillDescriptor(
        descriptor_id="internal_skill_descriptor:test",
        skill_id="skill:dummy_read",
        skill_name="Dummy Read",
        description="Public-safe dummy descriptor.",
        capability_category="read_only",
        risk_class="read_only",
        invocation_modes=["explicit_cli"],
        supported=True,
        enabled_by_default=False,
        owner_module="chanta_core.skills",
        created_at=now,
    )
    input_contract = InternalSkillInputContract(
        input_contract_id="internal_skill_input_contract:test",
        skill_id=descriptor.skill_id,
        required_fields=["root_path"],
        optional_fields=["relative_path"],
        field_types={"root_path": "str"},
        validation_rules=["explicit_input_only"],
        redacted_fields=["root_path"],
        created_at=now,
    )
    output_contract = InternalSkillOutputContract(
        output_contract_id="internal_skill_output_contract:test",
        skill_id=descriptor.skill_id,
        output_kind="diagnostic",
        required_fields=["status"],
        preview_fields=["summary"],
        sensitive_fields=[],
        max_preview_chars=200,
        full_output_allowed=False,
        created_at=now,
    )
    risk = InternalSkillRiskProfile(
        risk_profile_id="internal_skill_risk_profile:test",
        skill_id=descriptor.skill_id,
        risk_class="read_only",
        reversible=True,
        read_only=True,
        touches_filesystem=False,
        touches_network=False,
        touches_shell=False,
        touches_private_context=False,
        requires_review=True,
        requires_permission=False,
        created_at=now,
    )
    gate = InternalSkillGateContract(
        gate_contract_id="internal_skill_gate_contract:test",
        skill_id=descriptor.skill_id,
        gate_required=True,
        gate_kind="read_only_execution_gate",
        supported_gate_policy_ids=["read_only_execution_gate"],
        deny_if_gate_missing=True,
        deny_if_permission_missing=False,
        deny_if_workspace_boundary_unknown=True,
        created_at=now,
    )
    observability = InternalSkillObservabilityContract(
        observability_contract_id="internal_skill_observability_contract:test",
        skill_id=descriptor.skill_id,
        ocel_object_types=["internal_skill_descriptor"],
        ocel_event_activities=["internal_skill_descriptor_registered"],
        required_relations=["input_contract_belongs_to_descriptor"],
        envelope_required=True,
        audit_visible=True,
        workbench_visible=True,
        pig_report_keys=["internal_skill_descriptor_count"],
        ocpx_projection_keys=["internal_skill_onboarding_by_risk_class"],
        created_at=now,
    )
    review = InternalSkillOnboardingReview(
        review_id="internal_skill_onboarding_review:test",
        skill_id=descriptor.skill_id,
        descriptor_id=descriptor.descriptor_id,
        status="requested",
        reviewer_type="test",
        reviewer_id="tester",
        reason="test",
        created_at=now,
    )
    finding = InternalSkillOnboardingFinding(
        finding_id="internal_skill_onboarding_finding:test",
        skill_id=descriptor.skill_id,
        finding_type="missing_input_contract",
        status="failed",
        severity="high",
        message="Missing.",
        subject_ref=descriptor.descriptor_id,
        created_at=now,
    )
    result = InternalSkillOnboardingResult(
        result_id="internal_skill_onboarding_result:test",
        skill_id=descriptor.skill_id,
        descriptor_id=descriptor.descriptor_id,
        review_id=review.review_id,
        status="needs_fix",
        accepted=False,
        enabled=False,
        finding_ids=[finding.finding_id],
        summary="needs_fix",
        created_at=now,
    )

    assert descriptor.to_dict()["enabled_by_default"] is False
    assert input_contract.to_dict()["required_fields"] == ["root_path"]
    assert output_contract.to_dict()["full_output_allowed"] is False
    assert risk.to_dict()["read_only"] is True
    assert gate.to_dict()["gate_required"] is True
    assert observability.to_dict()["envelope_required"] is True
    assert review.to_dict()["reviewer_id"] == "tester"
    assert finding.to_dict()["severity"] == "high"
    assert result.to_dict()["enabled"] is False
    assert InternalSkillOnboardingService is not None
