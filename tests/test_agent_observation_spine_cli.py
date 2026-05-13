import json

from chanta_core.cli.main import main


def test_cli_observe_spine_ontology_adapters_collectors(capsys) -> None:
    assert main(["observe", "spine", "ontology"]) == 0
    ontology_out = capsys.readouterr().out
    assert "Agent Movement Ontology" in ontology_out
    assert "action_type_count=" in ontology_out

    assert main(["observe", "spine", "adapters"]) == 0
    adapters_out = capsys.readouterr().out
    assert "GenericJSONLTranscriptAdapter" in adapters_out
    assert "execution_enabled=false" in adapters_out

    assert main(["observe", "spine", "collectors"]) == 0
    collectors_out = capsys.readouterr().out
    assert "batch_file" in collectors_out
    assert "event_bus_enabled=false" in collectors_out


def test_cli_observe_spine_normalize(tmp_path, capsys) -> None:
    event_path = tmp_path / "event.json"
    event_path.write_bytes(json.dumps({"id": "u1", "role": "user", "content": "hello"}).encode("utf-8"))

    assert main(["observe", "spine", "normalize", "--event-json-file", str(event_path)]) == 0
    out = capsys.readouterr().out
    assert "Agent Observation Spine" in out
    assert "normalized_event_v2_count=1" in out
