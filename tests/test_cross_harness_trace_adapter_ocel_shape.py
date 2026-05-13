from chanta_core.ocel.store import OCELStore
from chanta_core.observation import CrossHarnessTraceAdapterService


def test_ocel_objects_and_events_are_emitted(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    trace_file.write_bytes(b'{"id":"u1","role":"user","content":"input"}\n')
    store = OCELStore(tmp_path / "ocel.sqlite")
    service = CrossHarnessTraceAdapterService(ocel_store=store)

    service.create_default_policy()
    service.register_adapter_contracts()
    service.register_default_mapping_rules()
    service.normalize_file(root_path=str(tmp_path), relative_path="trace.jsonl", runtime_hint="generic_jsonl")

    assert store.fetch_objects_by_type("cross_harness_trace_adapter_policy")
    assert store.fetch_objects_by_type("harness_trace_adapter_contract")
    assert store.fetch_objects_by_type("harness_trace_mapping_rule")
    assert store.fetch_objects_by_type("harness_trace_normalization_result")
    assert store.fetch_objects_by_type("agent_observation_normalized_event_v2")
    assert any(
        event["event_activity"] == "harness_trace_normalization_completed"
        for event in store.fetch_recent_events(limit=50)
    )
