import json

from chanta_core.observation_digest import ObservationService
from chanta_core.observation_digest.ids import new_agent_observation_batch_id


def test_generic_jsonl_user_assistant_rows_normalize():
    raw = "\n".join(
        [
            json.dumps({"id": "one", "role": "user", "content": "hello"}),
            json.dumps({"id": "two", "role": "assistant", "content": "received"}),
        ]
    )
    service = ObservationService()

    records = service.parse_generic_jsonl_records(raw)
    events = service.normalize_observation_records(
        records,
        batch_id=new_agent_observation_batch_id(),
        source_runtime="dummy_runtime",
        source_format="generic_jsonl",
    )

    assert [event.observed_activity for event in events] == [
        "user_message_observed",
        "assistant_message_observed",
    ]
    assert all(0.0 <= event.confidence <= 1.0 for event in events)
    assert all(event.evidence_ref for event in events)


def test_generic_jsonl_tool_call_result_rows_normalize():
    raw = "\n".join(
        [
            json.dumps({"id": "call", "tool": "read_file", "input": {"path": "a.txt"}}),
            json.dumps({"id": "result", "tool_result": "ok", "output": "file preview"}),
        ]
    )
    service = ObservationService()

    records = service.parse_generic_jsonl_records(raw)
    events = service.normalize_observation_records(
        records,
        batch_id=new_agent_observation_batch_id(),
        source_runtime="dummy_runtime",
        source_format="generic_jsonl",
    )

    assert [event.observed_activity for event in events] == [
        "tool_call_observed",
        "tool_result_observed",
    ]
    assert events[0].event_attrs["tool_name"] == "read_file"
    assert events[1].output_preview
