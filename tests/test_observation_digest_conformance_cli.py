import json

from chanta_core.cli.main import main


def _write_smoke_fixtures(root):
    (root / "trace.jsonl").write_bytes(
        (json.dumps({"role": "user", "content": "inspect"}) + "\n").encode("utf-8")
    )
    skill_dir = root / "external_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes("# Generic Skill\n\nDescription: fixture.\n".encode("utf-8"))


def test_cli_conformance_run_works(capsys):
    exit_code = main(["observe-digest", "conformance", "run"])
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Observation/Digestion Conformance" in captured.out
    assert "status=passed" in captured.out
    assert "skill_count=10" in captured.out


def test_cli_conformance_smoke_works(tmp_path, capsys):
    _write_smoke_fixtures(tmp_path)

    exit_code = main(
        [
            "observe-digest",
            "conformance",
            "smoke",
            "--skill-id",
            "skill:agent_trace_observe",
            "--fixture-root",
            str(tmp_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Observation/Digestion Smoke" in captured.out
    assert "skill:agent_trace_observe" in captured.out
    assert "smoke_passed_count=1" in captured.out
