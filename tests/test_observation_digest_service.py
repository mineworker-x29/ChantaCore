import json

from chanta_core.observation_digest import ObservationService
from chanta_core.observation_digest.ids import new_agent_observation_batch_id


def _observed_run_bundle(tmp_path):
    trace_path = tmp_path / "trace.jsonl"
    trace_path.write_bytes(
        "\n".join(
            [
                json.dumps({"id": "u1", "role": "user", "content": "Summarize a public file."}),
                json.dumps({"id": "a1", "role": "assistant", "content": "I will inspect it."}),
                json.dumps({"id": "t1", "tool": "read_file", "input": {"path": "public.txt"}}),
                json.dumps({"id": "r1", "tool_result": "ok", "output": "preview"}),
            ]
        ).encode("utf-8")
    )
    service = ObservationService()
    source = service.inspect_observation_source(
        root_path=str(tmp_path),
        relative_path="trace.jsonl",
        source_runtime="dummy_runtime",
        format_hint="generic_jsonl",
    )
    records = service.parse_generic_jsonl_records(trace_path.read_text(encoding="utf-8"))
    events = service.normalize_observation_records(
        records,
        batch_id=new_agent_observation_batch_id(),
        source_runtime="dummy_runtime",
        source_format="generic_jsonl",
    )
    batch = service.create_observation_batch(
        source=source,
        raw_record_count=len(records),
        normalized_events=events,
    )
    run = service.create_observed_run(source=source, batch=batch, normalized_events=events)
    return service, source, batch, events, run


def test_observed_run_is_created_from_normalized_events(tmp_path):
    _service, source, batch, events, run = _observed_run_bundle(tmp_path)

    assert source.source_format == "generic_jsonl"
    assert batch.normalized_event_count == len(events)
    assert run.event_count == len(events)
    assert run.batch_id == batch.batch_id
    assert run.run_attrs["observed_activity_sequence"][0] == "user_message_observed"


def test_behavior_inference_separates_evidence_categories(tmp_path):
    service, _source, _batch, events, run = _observed_run_bundle(tmp_path)

    inference = service.infer_behavior(observed_run=run, normalized_events=events)

    assert inference.confirmed_observations
    assert inference.data_based_interpretations
    assert inference.likely_hypotheses
    assert inference.estimates
    assert inference.unknown_or_needs_verification
    assert inference.evidence_refs
    assert inference.withdrawal_conditions
    assert 0.0 <= inference.inferred_goal_confidence <= 1.0


def test_process_narrative_is_created_from_inference(tmp_path):
    service, _source, _batch, events, run = _observed_run_bundle(tmp_path)
    inference = service.infer_behavior(observed_run=run, normalized_events=events)

    narrative = service.create_process_narrative(observed_run=run, inference=inference)

    assert narrative.observed_run_id == run.observed_run_id
    assert narrative.inference_id == inference.inference_id
    assert narrative.timeline
    assert narrative.inferred_outcome == inference.outcome_inference
