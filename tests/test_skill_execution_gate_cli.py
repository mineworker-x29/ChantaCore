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


def test_cli_gate_run_accepts_input_json_file(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        '{"root_path": "' + str(tmp_path).replace("\\", "\\\\") + '", "relative_path": "note.txt"}',
        encoding="utf-8",
    )

    exit_code = main(
        [
            "skill",
            "gate-run",
            "skill:read_workspace_text_file",
            "--input-json-file",
            str(payload_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=executed" in captured.out
    assert "executed=true" in captured.out
    assert "Traceback" not in captured.err


def test_cli_gate_run_accepts_bom_input_json_file(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    payload_path = tmp_path / "payload.json"
    payload_path.write_text(
        '{"root_path": "' + str(tmp_path).replace("\\", "\\\\") + '", "relative_path": "note.txt"}',
        encoding="utf-8-sig",
    )

    exit_code = main(
        [
            "skill",
            "gate-run",
            "skill:read_workspace_text_file",
            "--input-json-file",
            str(payload_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 0
    assert "status=executed" in captured.out
    assert "executed=true" in captured.out
    assert "Traceback" not in captured.err


def test_cli_gate_run_invalid_json_file_has_controlled_preview(tmp_path, capsys) -> None:
    payload_path = tmp_path / "payload.json"
    payload_path.write_text('{"root_path": "workspace",', encoding="utf-8")

    exit_code = main(
        [
            "skill",
            "gate-run",
            "skill:read_workspace_text_file",
            "--input-json-file",
            str(payload_path),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "invalid JSON input" in captured.err
    assert "source=input_json_file" in captured.err
    assert "received_preview=" in captured.err
    assert "Traceback" not in captured.err


def test_cli_gate_run_blocks_workspace_traversal(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "skill",
            "gate-run",
            "skill:read_workspace_text_file",
            "--root",
            str(tmp_path),
            "--path",
            "..\\..\\secret.md",
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status=blocked" in captured.out
    assert "executed=false" in captured.out
    assert "blocked=true" in captured.out
    assert "first_finding_type=path_traversal" in captured.out
    assert "Traceback" not in captured.out


def test_cli_gate_run_blocks_absolute_relative_path(tmp_path, capsys) -> None:
    exit_code = main(
        [
            "skill",
            "gate-run",
            "skill:read_workspace_text_file",
            "--root",
            str(tmp_path),
            "--path",
            str(tmp_path / "secret.md"),
        ]
    )
    captured = capsys.readouterr()

    assert exit_code == 1
    assert "status=blocked" in captured.out
    assert "executed=false" in captured.out
    assert "blocked=true" in captured.out
    assert "first_finding_type=absolute_path_not_allowed" in captured.out
    assert "Traceback" not in captured.out
