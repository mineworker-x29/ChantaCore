from chanta_core.cli.main import main
from tests.test_personal_runtime_workbench_service import build_workbench_store


def test_cli_workbench_commands_work(tmp_path, capsys) -> None:
    store = build_workbench_store(tmp_path)

    for command in ["status", "recent", "pending", "blockers", "candidates", "summaries", "health"]:
        assert main(["workbench", command, "--ocel-db", str(store.db_path), "--limit", "5"]) == 0
        output = capsys.readouterr().out
        assert "Personal Runtime Workbench" in output
        assert "skills_executed=false" in output


def test_cli_workbench_json_is_redacted(tmp_path, capsys) -> None:
    store = build_workbench_store(tmp_path)

    assert main(["workbench", "candidates", "--ocel-db", str(store.db_path), "--json"]) == 0
    output = capsys.readouterr().out

    assert "C:\\private\\source.txt" not in output
    assert "<REDACTED_PATH>" in output
