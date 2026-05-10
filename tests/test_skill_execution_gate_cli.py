from chanta_core.cli.main import main


def test_cli_gate_run_workspace_read(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")

    exit_code = main(
        [
            "skill",
            "gate-run",
            "skill:read_workspace_text_file",
            "--root",
            str(tmp_path),
            "--path",
            "note.txt",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=executed" in captured.out
    assert "executed=true" in captured.out
    assert "Traceback" not in captured.out


def test_cli_gate_run_unsupported_is_controlled(capsys) -> None:
    exit_code = main(["skill", "gate-run", "skill:write_file", "--input-json", "{}"])
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "blocked=true" in captured.out
    assert "Traceback" not in captured.out
