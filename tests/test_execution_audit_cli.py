from chanta_core.cli.main import main
from tests.test_execution_audit_service import build_store


def test_cli_execution_list_recent_audit_and_show_work(tmp_path, capsys) -> None:
    store, first, *_ = build_store(tmp_path)

    assert main(["execution", "list", "--ocel-db", str(store.db_path), "--limit", "1"]) == 0
    assert "Execution Audit" in capsys.readouterr().out

    assert main(["execution", "recent", "--ocel-db", str(store.db_path), "--limit", "1"]) == 0
    assert "returned_count=1" in capsys.readouterr().out

    assert main(["execution", "audit", "--ocel-db", str(store.db_path), "--blocked"]) == 0
    assert "blocked" in capsys.readouterr().out

    assert main(["execution", "show", first.envelope_id, "--ocel-db", str(store.db_path)]) == 0
    assert "Execution Audit Detail" in capsys.readouterr().out


def test_cli_show_missing_envelope_returns_controlled_not_found(tmp_path, capsys) -> None:
    store, *_ = build_store(tmp_path)

    exit_code = main(["execution", "show", "execution_envelope:missing", "--ocel-db", str(store.db_path)])

    assert exit_code == 1
    assert "status=not_found" in capsys.readouterr().out


def test_cli_json_output_is_redacted(tmp_path, capsys) -> None:
    store, first, *_ = build_store(tmp_path)

    assert main(["execution", "show", first.envelope_id, "--ocel-db", str(store.db_path), "--json"]) == 0
    output = capsys.readouterr().out
    assert "C:\\example\\workspace" not in output
    assert "<REDACTED_PATH>" in output
    assert "<HIDDEN>" in output
