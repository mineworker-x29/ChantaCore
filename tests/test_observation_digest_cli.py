import json

from chanta_core.cli.main import main


def test_observe_trace_cli_outputs_redacted_summary(tmp_path, capsys):
    trace_path = tmp_path / "trace.jsonl"
    trace_path.write_bytes(
        "\n".join(
            [
                json.dumps({"id": "u1", "role": "user", "content": "hello"}),
                json.dumps({"id": "a1", "role": "assistant", "content": "received"}),
            ]
        ).encode("utf-8")
    )

    exit_code = main(
        [
            "observe",
            "trace",
            "--root",
            str(tmp_path),
            "--path",
            "trace.jsonl",
            "--runtime",
            "dummy_runtime",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Observation" in captured.out
    assert "normalized_event_count=2" in captured.out
    assert "hello" not in captured.out


def test_digest_static_cli_outputs_safe_profile(tmp_path, capsys):
    skill_dir = tmp_path / "public_skill"
    skill_dir.mkdir()
    (skill_dir / "SKILL.md").write_bytes(
        "\n".join(
            [
                "# Public Dummy Skill",
                "Description: public fixture.",
                "Inputs: relative_path",
                "Outputs: summary",
            ]
        ).encode("utf-8")
    )

    exit_code = main(
        [
            "digest",
            "static",
            "--root",
            str(tmp_path),
            "--path",
            "public_skill",
            "--vendor",
            "dummy_vendor",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "Digestion" in captured.out
    assert "static_profile_id=" in captured.out
    assert "full_raw_body_stored=false" in captured.out


def test_cli_rejects_path_traversal(tmp_path, capsys):
    exit_code = main(
        [
            "observe",
            "source-inspect",
            "--root",
            str(tmp_path),
            "--path",
            "../outside.jsonl",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "blocked" in captured.out
