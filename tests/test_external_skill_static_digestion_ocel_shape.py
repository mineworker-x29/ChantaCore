from pathlib import Path

from chanta_core.digestion import ExternalSkillStaticDigestionService
from chanta_core.ocel.store import OCELStore


def test_static_digestion_emits_ocel_objects_and_events(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(b"# Generic Skill\n\nDescription: read summarize.\n")

    store = OCELStore()
    service = ExternalSkillStaticDigestionService(ocel_store=store)
    service.create_static_digestion_report(root_path=str(tmp_path), relative_path="skill")

    object_types = {
        object_type
        for object_type in [
            "external_skill_resource_inventory",
            "external_skill_manifest_profile",
            "external_skill_instruction_profile",
            "external_skill_declared_capability",
            "external_skill_static_risk_profile",
            "external_skill_static_digestion_report",
        ]
        if store.fetch_objects_by_type(object_type)
    }
    activities = {row["event_activity"] for row in store.fetch_recent_events(limit=20)}

    assert "external_skill_resource_inventory" in object_types
    assert "external_skill_manifest_profile" in object_types
    assert "external_skill_instruction_profile" in object_types
    assert "external_skill_declared_capability" in object_types
    assert "external_skill_static_risk_profile" in object_types
    assert "external_skill_static_digestion_report" in object_types
    assert "external_skill_resource_inventory_created" in activities
    assert "external_skill_static_digestion_report_created" in activities
