import json

from chanta_core.cli.main import main
from tests.test_execution_result_promotion_service import build_execution_result


def test_cli_candidate_from_envelope_list_show_review(tmp_path, capsys) -> None:
    store, envelope, *_ = build_execution_result(tmp_path)

    assert main(
        [
            "promotion",
            "candidate-from-envelope",
            envelope.envelope_id,
            "--target",
            "memory_candidate",
            "--ocel-db",
            str(store.db_path),
        ]
    ) == 0
    created = capsys.readouterr().out
    assert "pending_review" in created

    assert main(["promotion", "list", "--ocel-db", str(store.db_path)]) == 0
    listed = capsys.readouterr().out
    assert "memory_candidate" in listed
    candidate_id = listed.splitlines()[1].split(" | ")[0]

    assert main(["promotion", "show", candidate_id, "--ocel-db", str(store.db_path)]) == 0
    assert "canonical_promotion_enabled=false" in capsys.readouterr().out

    assert main(
        [
            "promotion",
            "review",
            candidate_id,
            "--decision",
            "no_action",
            "--ocel-db",
            str(store.db_path),
        ]
    ) == 0
    assert "promoted=false" in capsys.readouterr().out


def test_cli_candidate_from_envelope_json_file(tmp_path, capsys) -> None:
    _, envelope, output, summary = build_execution_result(tmp_path)
    payload = {
        "envelope": envelope.to_dict(),
        "output_snapshot": output.to_dict(),
        "outcome_summary": summary.to_dict(),
    }
    path = tmp_path / "envelope.json"
    path.write_bytes(json.dumps(payload).encode("utf-8"))

    assert main(
        [
            "promotion",
            "candidate-from-envelope",
            "--envelope-json-file",
            str(path),
            "--target",
            "workspace_summary_candidate",
            "--json",
        ]
    ) == 0
    output_text = capsys.readouterr().out
    assert "pending_review" in output_text
    assert "public-safe execution result" in output_text
