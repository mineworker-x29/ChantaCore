from chanta_core.cli.main import main


def test_cli_skill_propose_prints_preview_only(capsys) -> None:
    exit_code = main(
        [
            "skill",
            "propose",
            "read file docs/example.txt",
            "--root",
            "<WORKSPACE_ROOT>",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=proposal_available" in captured.out
    assert "suggested_cli_command=chanta-cli skill run skill:read_workspace_text_file" in captured.out
    assert "skills_executed=false" in captured.out
    assert "Traceback" not in captured.out


def test_cli_skill_propose_unsupported_is_controlled(capsys) -> None:
    exit_code = main(["skill", "propose", "run shell command"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status=unsupported" in captured.out
    assert "Traceback" not in captured.out


def test_cli_skill_propose_json_output(capsys) -> None:
    exit_code = main(
        [
            "skill",
            "propose",
            "list files",
            "--root",
            "<WORKSPACE_ROOT>",
            "--json",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert '"status": "proposal_available"' in captured.out
    assert "skills_executed" in captured.out
