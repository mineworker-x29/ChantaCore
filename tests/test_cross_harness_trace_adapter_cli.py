import json

from chanta_core.cli.main import main


def test_cli_observe_adapters_list(capsys):
    exit_code = main(["observe", "adapters", "list"])

    output = capsys.readouterr().out
    assert exit_code == 0
    assert "Cross-Harness Trace Adapters" in output
    assert "GenericJSONLTranscriptAdapter" in output


def test_cli_inspect_source_and_normalize_json(tmp_path, capsys):
    trace_file = tmp_path / "trace.jsonl"
    trace_file.write_bytes(b'{"id":"u1","role":"user","content":"input"}\n')

    inspect_exit = main(["observe", "adapters", "inspect-source", "--root", str(tmp_path), "--path", "trace.jsonl", "--json"])
    inspect_payload = json.loads(capsys.readouterr().out)
    assert inspect_exit == 0
    assert inspect_payload["selected_adapter_name"] == "GenericJSONLTranscriptAdapter"

    normalize_exit = main(["observe", "adapters", "normalize", "--root", str(tmp_path), "--path", "trace.jsonl", "--runtime", "generic_jsonl", "--json"])
    normalize_payload = json.loads(capsys.readouterr().out)
    assert normalize_exit == 0
    assert normalize_payload["normalized_event_count"] == 1


def test_cli_mapping_rules_and_coverage(capsys):
    assert main(["observe", "adapters", "mapping-rules", "GenericJSONLTranscriptAdapter"]) == 0
    assert "role=user" in capsys.readouterr().out

    assert main(["observe", "adapters", "coverage", "CodexTaskLogAdapter", "--json"]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["coverage_status"] == "stub"
