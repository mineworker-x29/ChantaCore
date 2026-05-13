from chanta_core.skills.history_adapter import (
    skill_registry_entries_to_history_entries,
    skill_registry_findings_to_history_entries,
    skill_registry_results_to_history_entries,
    skill_registry_views_to_history_entries,
)
from chanta_core.skills.registry_view import SkillRegistryViewService


def test_skill_registry_history_adapters_use_registry_source():
    service = SkillRegistryViewService()
    view = service.build_registry_view()
    entries = service.apply_filter(skill_layer="internal_observation")
    result = service.record_result(command_name="observation", entries=entries)
    service.record_finding(
        registry_view_id=view.registry_view_id,
        skill_id="skill:demo",
        finding_type="missing_contract",
        status="needs_fix",
        severity="high",
        message="Public fixture finding.",
    )

    history_entries = [
        *skill_registry_views_to_history_entries([view]),
        *skill_registry_entries_to_history_entries(entries),
        *skill_registry_results_to_history_entries([result]),
        *skill_registry_findings_to_history_entries(service.last_findings),
    ]

    assert {item.source for item in history_entries} == {"skill_registry_view"}
    assert any(item.priority >= 85 for item in history_entries)
    assert any(
        any(ref.get("ref_type") == "skill_registry_entry" for ref in item.refs)
        for item in history_entries
    )
