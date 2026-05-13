from pathlib import Path

from chanta_core.digestion import ExternalSkillStaticDigestionService
from chanta_core.skills.history_adapter import (
    external_skill_declared_capabilities_to_history_entries,
    external_skill_instruction_profiles_to_history_entries,
    external_skill_manifest_profiles_to_history_entries,
    external_skill_resource_inventories_to_history_entries,
    external_skill_static_digestion_findings_to_history_entries,
    external_skill_static_digestion_reports_to_history_entries,
    external_skill_static_risk_profiles_to_history_entries,
)


def test_static_digestion_history_entries(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(b"# Generic Skill\n\nDescription: read summarize.\n")
    (skill_dir / "helper.py").write_bytes(b"print('not used')\n")
    service = ExternalSkillStaticDigestionService()
    report = service.create_static_digestion_report(root_path=str(tmp_path), relative_path="skill")

    entries = [
        *external_skill_resource_inventories_to_history_entries([service.last_inventory]),
        *external_skill_manifest_profiles_to_history_entries(service.last_manifest_profiles),
        *external_skill_instruction_profiles_to_history_entries(service.last_instruction_profiles),
        *external_skill_declared_capabilities_to_history_entries(service.last_declared_capabilities),
        *external_skill_static_risk_profiles_to_history_entries([service.last_risk_profile]),
        *external_skill_static_digestion_reports_to_history_entries([report]),
        *external_skill_static_digestion_findings_to_history_entries(service.last_findings),
    ]

    assert entries
    assert {entry.source for entry in entries} == {"external_skill_static_digestion"}
    assert any(entry.priority >= 70 for entry in entries)
