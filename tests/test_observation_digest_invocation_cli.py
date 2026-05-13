import json

from chanta_core.cli.main import main


def test_cli_observe_run_trace_works(tmp_path, capsys):
    (tmp_path / "trace.jsonl").write_bytes(
        (json.dumps({"role": "user", "content": "hello"}) + "\n").encode("utf-8"),
    )

    exit_code = main(
        [
            "observe",
            "run",
            "trace",
            "--root",
            str(tmp_path),
            "--path",
            "trace.jsonl",
            "--runtime",
            "generic",
            "--format",
            "generic_jsonl",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Observation/Digestion Invocation" in captured.out
    assert "skill_id=skill:agent_trace_observe" in captured.out
    assert "executed=true" in captured.out
    assert "blocked=false" in captured.out
    assert "envelope_id=execution_envelope:" in captured.out


def test_cli_digest_run_static_works(tmp_path, capsys):
    skill_dir = tmp_path / "external_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes("# Generic Skill\n\nDescription: fixture.\n".encode("utf-8"))

    exit_code = main(
        [
            "digest",
            "run",
            "static",
            "--root",
            str(tmp_path),
            "--path",
            "external_skill",
            "--vendor",
            "fixture",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "skill_id=skill:external_skill_static_digest" in captured.out
    assert "executed=true" in captured.out
    assert "shell_network_mcp_plugin_execution=false" in captured.out
