from pathlib import Path

from chanta_core.digestion import ExternalSkillStaticDigestionService


def test_traversal_is_rejected(tmp_path: Path) -> None:
    service = ExternalSkillStaticDigestionService()
    descriptor = service.digestion_service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="../outside",
    )

    inventory = service.inspect_resource_inventory(
        root_path=str(tmp_path),
        relative_path="../outside",
        source_descriptor=descriptor,
    )

    assert inventory.inventory_attrs["status"] == "blocked"
    assert any(finding.finding_type == "workspace_boundary_violation" for finding in service.last_findings)


def test_script_files_are_inventoried_without_activation(tmp_path: Path) -> None:
    skill_dir = tmp_path / "skill"
    skill_dir.mkdir()
    marker = tmp_path / "marker.txt"
    (skill_dir / "SKILL.md").write_bytes(b"# Generic Skill\n\nDescription: read summarize.\n")
    (skill_dir / "helper.py").write_bytes(
        f"from pathlib import Path\nPath({str(marker)!r}).write_bytes(b'changed')\n".encode("utf-8")
    )

    service = ExternalSkillStaticDigestionService()
    report = service.create_static_digestion_report(root_path=str(tmp_path), relative_path="skill")

    assert report.status == "completed_with_findings"
    assert service.last_inventory is not None
    assert service.last_inventory.script_files == ["helper.py"]
    assert not marker.exists()
    assert report.report_attrs["script_execution_used"] is False
    assert report.report_attrs["external_harness_execution_used"] is False
    assert report.report_attrs["canonical_import_enabled"] is False
    assert report.report_attrs["execution_enabled"] is False
