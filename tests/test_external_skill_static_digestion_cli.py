from pathlib import Path

from chanta_core.cli.main import main


def _fixture(root: Path) -> None:
    skill_dir = root / "skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(
        b"""---
name: Generic Static Skill
description: Read and summarize files.
---
# Generic Static Skill
"""
    )
    (skill_dir / "manifest.json").write_bytes(b'{"name":"generic","description":"read summarize"}')
    (skill_dir / "helper.py").write_bytes(b"print('not used')\n")


def test_digest_inventory_cli(tmp_path: Path, capsys) -> None:
    _fixture(tmp_path)

    exit_code = main(["digest", "inventory", "--root", str(tmp_path), "--path", "skill"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "External Skill Static Digestion" in captured.out
    assert "script_count=1" in captured.out
    assert "script_execution_used=false" in captured.out


def test_digest_static_risk_report_cli(tmp_path: Path, capsys) -> None:
    _fixture(tmp_path)

    static_exit = main(["digest", "static", "--root", str(tmp_path), "--path", "skill", "--vendor", "fixture"])
    static_out = capsys.readouterr().out
    risk_exit = main(["digest", "risk", "--root", str(tmp_path), "--path", "skill", "--vendor", "fixture"])
    risk_out = capsys.readouterr().out
    report_exit = main(["digest", "report", "--root", str(tmp_path), "--path", "skill", "--vendor", "fixture"])
    report_out = capsys.readouterr().out

    assert static_exit == 0
    assert "static_profile_id=" in static_out
    assert risk_exit == 0
    assert "risk_class=" in risk_out
    assert report_exit == 0
    assert "canonical_import_enabled=false" in report_out
    assert "execution_enabled=false" in report_out
