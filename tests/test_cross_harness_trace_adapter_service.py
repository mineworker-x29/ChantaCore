from chanta_core.observation import CrossHarnessTraceAdapterService


def test_normalize_file_creates_v2_events_objects_and_relations(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    trace_file.write_bytes(
        b'{"id":"u1","role":"user","content":"inspect"}\n'
        b'{"id":"a1","role":"assistant","content":"done"}\n'
    )
    service = CrossHarnessTraceAdapterService()

    result = service.normalize_file(root_path=str(tmp_path), relative_path="trace.jsonl", runtime_hint="generic_jsonl")

    assert result.status == "completed"
    assert result.raw_record_count == 2
    assert result.normalized_event_count == 2
    assert result.observed_object_count >= 1
    assert result.observed_relation_count >= 1


def test_chantacore_ocel_like_normalization_maps_envelope(tmp_path):
    trace_file = tmp_path / "trace.json"
    trace_file.write_bytes(
        b'[{"object_id":"env1","object_type":"execution_envelope","object_attrs":{"status":"completed"}}]'
    )
    service = CrossHarnessTraceAdapterService()

    result = service.normalize_file(root_path=str(tmp_path), relative_path="trace.json", runtime_hint="chantacore")

    assert result.status == "completed"
    assert result.normalized_event_count == 1
    assert service.spine_service.last_events[0].canonical_action_type == "record_envelope"
