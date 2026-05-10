from chanta_core.cli.main import main


def test_cli_skill_run_requires_skill_id(capsys) -> None:
    exit_code = main(["skill", "run", "--input-json", "{}"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "skill_id is required" in captured.err
    assert "Traceback" not in captured.err


def test_cli_unsupported_skill_has_controlled_diagnostic(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "skill",
            "run",
            "skill:write_file",
            "--input-json",
            "{}",
            "--root",
            str(tmp_path),
            "--path",
            "note.txt",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status=unsupported" in captured.out
    assert "Traceback" not in captured.out


def test_cli_workspace_read_with_explicit_skill_id(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")

    exit_code = main(
        [
            "skill",
            "run",
            "skill:read_workspace_text_file",
            "--root",
            str(tmp_path),
            "--path",
            "note.txt",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=completed" in captured.out
    assert "natural_language_routing=false" in captured.out
