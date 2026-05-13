from chanta_core.observation import CrossHarnessTraceAdapterService


def _plan(service: CrossHarnessTraceAdapterService, tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    trace_file.write_bytes(b'{"id":"probe","role":"user","content":"input"}\n')
    service.create_default_policy()
    service.register_adapter_contracts()
    service.register_default_mapping_rules()
    inspection = service.inspect_trace_source(root_path=str(tmp_path), relative_path="trace.jsonl", runtime_hint="generic_jsonl")
    return service.build_normalization_plan(inspection)


def test_generic_jsonl_rows_map_to_expected_activity_and_action(tmp_path):
    service = CrossHarnessTraceAdapterService()
    plan = _plan(service, tmp_path)

    service.normalize_records(
        [
            {"id": "u1", "role": "user", "content": "input"},
            {"id": "a1", "role": "assistant", "content": "output"},
            {"id": "t1", "tool": "search", "input": {"q": "x"}},
            {"id": "r1", "tool_result": {"ok": True}},
            {"id": "e1", "error": "failed"},
        ],
        plan=plan,
    )

    pairs = [(event.observed_activity, event.canonical_action_type) for event in service.spine_service.last_events]
    assert pairs == [
        ("user_message_observed", "observe_context"),
        ("assistant_message_observed", "emit_response"),
        ("tool_call_observed", "invoke_tool"),
        ("tool_result_observed", "record_outcome"),
        ("error_observed", "record_outcome"),
    ]
    assert all(event.evidence_ref for event in service.spine_service.last_events)
    assert all(event.withdrawal_conditions for event in service.spine_service.last_events)
