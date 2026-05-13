from chanta_core.digestion import (
    ExternalSkillDeclaredCapability,
    ExternalSkillInstructionProfile,
    ExternalSkillManifestProfile,
    ExternalSkillResourceInventory,
    ExternalSkillStaticDigestionFinding,
    ExternalSkillStaticDigestionReport,
    ExternalSkillStaticRiskProfile,
)
from chanta_core.skills.ids import (
    new_external_skill_declared_capability_id,
    new_external_skill_instruction_profile_id,
    new_external_skill_manifest_profile_id,
    new_external_skill_resource_inventory_id,
    new_external_skill_static_digestion_finding_id,
    new_external_skill_static_digestion_report_id,
    new_external_skill_static_risk_profile_id,
)
from chanta_core.utility.time import utc_now_iso


def test_static_digestion_models_to_dict_defaults() -> None:
    now = utc_now_iso()
    inventory = ExternalSkillResourceInventory(
        inventory_id=new_external_skill_resource_inventory_id(),
        source_descriptor_id="external_skill_source_descriptor:fixture",
        source_root_ref="fixture_skill",
        resource_count=1,
        markdown_files=["SKILL.md"],
        manifest_files=["SKILL.md"],
        script_files=[],
        reference_files=[],
        asset_files=[],
        agent_config_files=[],
        mcp_config_files=[],
        unknown_files=[],
        denied_files=[],
        private=False,
        sensitive=False,
        created_at=now,
    )
    manifest = ExternalSkillManifestProfile(
        manifest_profile_id=new_external_skill_manifest_profile_id(),
        source_descriptor_id=inventory.source_descriptor_id,
        manifest_ref="SKILL.md",
        manifest_kind="skill_md_frontmatter",
        parsed_name="Generic Reader",
        parsed_description="Reads and summarizes files.",
        parsed_version="1.0",
        parsed_author="fixture",
        declared_tools=["read"],
        declared_permissions=["read"],
        declared_inputs=["path"],
        declared_outputs=["summary"],
        declared_runtime_requirements=[],
        parse_status="parsed",
        confidence=2.0,
        created_at=now,
    )
    instruction = ExternalSkillInstructionProfile(
        instruction_profile_id=new_external_skill_instruction_profile_id(),
        source_descriptor_id=inventory.source_descriptor_id,
        instruction_ref="SKILL.md",
        instruction_kind="skill_md",
        title="Generic Reader",
        instruction_preview="Read and summarize public files.",
        declared_behavior=["Read files"],
        declared_constraints=["Do not write files"],
        declared_tools=["read"],
        declared_outputs=["summary"],
        max_preview_chars=800,
        full_body_stored=False,
        confidence=1.0,
        created_at=now,
    )
    capability = ExternalSkillDeclaredCapability(
        declared_capability_id=new_external_skill_declared_capability_id(),
        source_descriptor_id=inventory.source_descriptor_id,
        static_profile_id=None,
        capability_name="Generic Reader",
        capability_category="read_only",
        declared_actions=["read", "summarize"],
        declared_objects=["external_skill_source"],
        declared_inputs=["path"],
        declared_outputs=["summary"],
        declared_side_effects=[],
        declared_risk_class="read_only",
        confidence=1.0,
        created_at=now,
    )
    risk = ExternalSkillStaticRiskProfile(
        static_risk_profile_id=new_external_skill_static_risk_profile_id(),
        source_descriptor_id=inventory.source_descriptor_id,
        risk_class="read_only",
        declared_read_only=True,
        declared_write=False,
        declared_shell=False,
        declared_network=False,
        declared_mcp=False,
        declared_plugin=False,
        declared_external_execution=False,
        declared_private_context_access=False,
        risk_evidence_refs=[],
        requires_review=True,
        execution_allowed_by_default=False,
        created_at=now,
    )
    finding = ExternalSkillStaticDigestionFinding(
        finding_id=new_external_skill_static_digestion_finding_id(),
        source_descriptor_id=inventory.source_descriptor_id,
        subject_ref="SKILL.md",
        finding_type="script_present",
        status="review_required",
        severity="medium",
        message="Script was inventoried.",
        evidence_ref="resource_inventory",
        created_at=now,
    )
    report = ExternalSkillStaticDigestionReport(
        report_id=new_external_skill_static_digestion_report_id(),
        source_descriptor_id=inventory.source_descriptor_id,
        inventory_id=inventory.inventory_id,
        manifest_profile_ids=[manifest.manifest_profile_id],
        instruction_profile_ids=[instruction.instruction_profile_id],
        declared_capability_ids=[capability.declared_capability_id],
        static_risk_profile_id=risk.static_risk_profile_id,
        static_profile_id=None,
        assimilation_candidate_id=None,
        adapter_candidate_ids=[],
        finding_ids=[finding.finding_id],
        status="completed_with_findings",
        summary="Static digestion completed.",
        created_at=now,
    )

    assert manifest.to_dict()["confidence"] == 1.0
    assert instruction.to_dict()["full_body_stored"] is False
    assert risk.to_dict()["execution_allowed_by_default"] is False
    assert report.to_dict()["finding_ids"] == [finding.finding_id]
