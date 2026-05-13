from chanta_core.skills.registry_view import (
    SkillRegistryEntry,
    SkillRegistryFilter,
    SkillRegistryFinding,
    SkillRegistryResult,
    SkillRegistryView,
)
from chanta_core.utility.time import utc_now_iso


def test_skill_registry_view_models_to_dict():
    created_at = utc_now_iso()
    view = SkillRegistryView(
        registry_view_id="skill_registry_view:demo",
        view_name="demo",
        total_skill_count=1,
        enabled_skill_count=0,
        disabled_skill_count=1,
        candidate_skill_count=1,
        blocked_skill_count=0,
        observation_skill_count=1,
        digestion_skill_count=0,
        external_candidate_count=0,
        created_at=created_at,
    )
    entry = SkillRegistryEntry(
        registry_entry_id="skill_registry_entry:demo",
        registry_view_id=view.registry_view_id,
        skill_id="skill:demo",
        skill_name="Demo",
        description="Public fixture entry.",
        skill_layer="internal_observation",
        skill_origin="test_fixture",
        capability_category="observation",
        risk_class="read_only",
        status="candidate",
        enabled=False,
        execution_enabled=False,
        proposal_enabled=True,
        review_required=False,
        gate_required=True,
        envelope_required=True,
        audit_visible=True,
        workbench_visible=True,
        ocel_observable=True,
        pig_visible=True,
        source_ref=None,
        created_at=created_at,
    )
    registry_filter = SkillRegistryFilter(
        registry_filter_id="skill_registry_filter:demo",
        registry_view_id=view.registry_view_id,
        skill_layer="internal_observation",
        skill_origin=None,
        capability_category=None,
        risk_class=None,
        status=None,
        enabled=None,
        execution_enabled=False,
        ocel_observable=True,
        limit=10,
        created_at=created_at,
    )
    finding = SkillRegistryFinding(
        finding_id="skill_registry_finding:demo",
        registry_view_id=view.registry_view_id,
        skill_id=entry.skill_id,
        finding_type="missing_contract",
        status="needs_fix",
        severity="high",
        message="Demo finding.",
        subject_ref=entry.registry_entry_id,
        created_at=created_at,
    )
    result = SkillRegistryResult(
        registry_result_id="skill_registry_result:demo",
        registry_view_id=view.registry_view_id,
        command_name="list",
        status="completed",
        entry_ids=[entry.registry_entry_id],
        finding_ids=[finding.finding_id],
        summary="Demo result.",
        created_at=created_at,
    )

    assert view.to_dict()["observation_skill_count"] == 1
    assert entry.to_dict()["execution_enabled"] is False
    assert registry_filter.to_dict()["ocel_observable"] is True
    assert finding.to_dict()["finding_type"] == "missing_contract"
    assert result.to_dict()["entry_ids"] == [entry.registry_entry_id]
