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


def test_cli_skill_run_accepts_input_json_file(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        '{"root_path": "' + str(tmp_path).replace("\\", "\\\\") + '", "relative_path": "note.txt"}',
        encoding="utf-8",
    )

    exit_code = main(
        [
            "skill",
            "run",
            "skill:read_workspace_text_file",
            "--input-json-file",
            str(payload_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=completed" in captured.out
    assert "Traceback" not in captured.err


def test_cli_skill_run_invalid_json_shows_safe_received_preview(capsys) -> None:
    exit_code = main(
        [
            "skill",
            "run",
            "skill:read_workspace_text_file",
            "--input-json",
            '{"root_path": "C:\\tmp",',
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "invalid JSON input" in captured.err
    assert "received_preview=" in captured.err
    assert '{"root_path": "C:\\tmp",' in captured.err
    assert "Traceback" not in captured.err


def test_cli_skill_run_rejects_both_inline_and_file_json(tmp_path, capsys) -> None:
    payload_path = tmp_path / "payload.json"
    payload_path.write_text("{}", encoding="utf-8")

    exit_code = main(
        [
            "skill",
            "run",
            "skill:read_workspace_text_file",
            "--input-json",
            "{}",
            "--input-json-file",
            str(payload_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "use either --input-json or --input-json-file" in captured.err
    assert "Traceback" not in captured.err
