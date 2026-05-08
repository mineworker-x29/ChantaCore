from chanta_core.external.ocel_import import (
    build_payload_preview,
    count_event_activities,
    count_object_types,
    count_relation_types,
    detect_payload_kind,
    extract_timestamp_range,
    hash_payload_preview,
    sample_ids,
)


def sample_payload() -> dict:
    return {
        "events": [
            {"id": "e1", "activity": "start", "timestamp": "2026-01-01T00:00:00Z"},
            {"id": "e2", "activity": "finish", "timestamp": "2026-01-01T00:01:00Z"},
        ],
        "objects": [
            {"id": "o1", "type": "case"},
            {"id": "o2", "type": "resource"},
        ],
        "relations": [
            {"type": "event_object", "event_id": "e1", "object_id": "o1"},
            {"type": "event_object", "event_id": "e2", "object_id": "o1"},
        ],
    }


def test_payload_helpers_detect_and_summarize_ocel_like_payload() -> None:
    payload = sample_payload()

    assert detect_payload_kind(payload) == "ocel_like"
    assert hash_payload_preview(payload) == hash_payload_preview(payload)
    assert build_payload_preview(payload)["top_level_keys"] == ["events", "objects", "relations"]
    assert count_event_activities(payload["events"]) == {"finish": 1, "start": 1}
    assert count_object_types(payload["objects"]) == {"case": 1, "resource": 1}
    assert count_relation_types(payload["relations"]) == {"event_object": 2}
    assert extract_timestamp_range(payload["events"]) == (
        "2026-01-01T00:00:00Z",
        "2026-01-01T00:01:00Z",
    )
    assert sample_ids(payload["events"], ["id"]) == ["e1", "e2"]


def test_payload_kind_handles_invalid_or_partial_payloads() -> None:
    assert detect_payload_kind({"events": []}) == "event_log"
    assert detect_payload_kind({"objects": []}) == "object_log"
    assert detect_payload_kind({"unexpected": []}) == "unknown"
