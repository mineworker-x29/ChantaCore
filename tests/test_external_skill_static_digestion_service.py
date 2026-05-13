from pathlib import Path

from chanta_core.digestion import ExternalSkillStaticDigestionService


def _fixture(root: Path) -> Path:
    skill_dir = root / "fixture_skill"
    (skill_dir / "references").mkdir(parents=True)
    (skill_dir / "assets").mkdir()
    (skill_dir / "scripts").mkdir()
    (skill_dir / "SKILL.md").write_bytes(
        b"""---
name: Generic Reader
description: Reads, searches, and summarizes public files.
version: "1.0"
author: fixture
tools: [read, search, summarize]
inputs: [path]
outputs: [summary]
permissions: [read]
---
# Generic Reader

This capability can read and summarize external skill instructions.
Do not write files.
"""
    )
    (skill_dir / "manifest.json").write_bytes(
        b'{"name":"generic-reader","description":"read search summarize","tools":["read"],"inputs":["path"],"outputs":["summary"]}'
    )
    (skill_dir / "skill.toml").write_bytes(b'name = "generic-reader-toml"\ndescription = "read files"\n')
    (skill_dir / "references" / "guide.md").write_bytes(b"# Guide\nReference material.")
    (skill_dir / "assets" / "icon.png").write_bytes(b"\x89PNG\r\n")
    (skill_dir / "scripts" / "helper.py").write_bytes(b"print('not executed')\n")
    return skill_dir


def test_inventory_detects_resource_kinds(tmp_path: Path) -> None:
    _fixture(tmp_path)
    service = ExternalSkillStaticDigestionService()
    descriptor = service.digestion_service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="fixture_skill",
    )

    inventory = service.inspect_resource_inventory(
        root_path=str(tmp_path),
        relative_path="fixture_skill",
        source_descriptor=descriptor,
    )

    assert "SKILL.md" in inventory.markdown_files
    assert "manifest.json" in inventory.manifest_files
    assert "scripts/helper.py" in inventory.script_files
    assert "references/guide.md" in inventory.reference_files
    assert "assets/icon.png" in inventory.asset_files
    assert inventory.inventory_attrs["script_execution_used"] is False


def test_static_report_parses_frontmatter_manifest_preview_and_capability(tmp_path: Path) -> None:
    _fixture(tmp_path)
    service = ExternalSkillStaticDigestionService()

    report = service.create_static_digestion_report(
        root_path=str(tmp_path),
        relative_path="fixture_skill",
        vendor_hint="fixture",
    )

    skill_manifest = next(
        profile for profile in service.last_manifest_profiles if profile.manifest_kind == "skill_md_frontmatter"
    )
    instruction = service.last_instruction_profiles[0]
    capability = service.last_declared_capabilities[0]
    assert report.status == "completed_with_findings"
    assert skill_manifest.parsed_name == "Generic Reader"
    assert skill_manifest.parsed_description.startswith("Reads")
    assert instruction.instruction_preview
    assert instruction.full_body_stored is False
    assert {"read", "search", "summarize"}.issubset(set(capability.declared_actions))
    assert service.last_risk_profile is not None
    assert service.last_risk_profile.execution_allowed_by_default is False


def test_generic_yaml_manifest_fails_safely_when_not_mapping(tmp_path: Path) -> None:
    skill_dir = tmp_path / "fixture_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(b"# Generic Skill\n")
    (skill_dir / "manifest.yaml").write_bytes(b"- not\n- a\n- mapping\n")
    service = ExternalSkillStaticDigestionService()
    descriptor = service.digestion_service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="fixture_skill",
    )

    profile = service.parse_generic_manifest(
        root_path=str(tmp_path),
        relative_path="fixture_skill",
        manifest_ref="manifest.yaml",
        source_descriptor=descriptor,
    )

    assert profile.parse_status in {"parsed", "failed"}
    assert profile.manifest_attrs["full_raw_body_stored"] is False
