from chanta_core.cli.main import main


def test_workspace_summary_from_file_and_candidate_cli(tmp_path, capsys) -> None:
    (tmp_path / "README.md").write_bytes(b"# Title\n\n## Part\nBody")
    db_path = tmp_path / "summary.sqlite"

    assert main([
        "workspace-summary",
        "from-file",
        "--root",
        str(tmp_path),
        "--path",
        "README.md",
        "--ocel-db",
        str(db_path),
    ]) == 0
    output = capsys.readouterr().out
    assert "Workspace Read Summary" in output
    assert "Title" in output

    assert main(["workspace-summary", "show", output.split("summary_result_id=")[1].splitlines()[0], "--ocel-db", str(db_path)]) == 0
    assert "Workspace Read Summary" in capsys.readouterr().out


def test_workspace_summary_from_file_rejects_traversal(tmp_path, capsys) -> None:
    (tmp_path / "note.txt").write_bytes(b"safe")

    exit_code = main([
        "workspace-summary",
        "from-file",
        "--root",
        str(tmp_path),
        "--path",
        "..\\outside.txt",
        "--ocel-db",
        str(tmp_path / "summary.sqlite"),
    ])

    assert exit_code == 1
    assert "failed" in capsys.readouterr().out
