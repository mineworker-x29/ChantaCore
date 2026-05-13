import json

from chanta_core.ocel.store import OCELStore
from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService


def test_observation_digest_invocation_emits_ocel_shape(tmp_path):
    store = OCELStore(tmp_path / "invocation.sqlite")
    trace_path = tmp_path / "trace.jsonl"
    trace_path.write_bytes((json.dumps({"role": "user", "content": "hello"}) + "\n").encode("utf-8"))
    service = ObservationDigestSkillInvocationService(ocel_store=store)

    result = service.invoke_skill(
        skill_id="skill:agent_trace_observe",
        input_payload={
            "root_path": str(tmp_path),
            "relative_path": "trace.jsonl",
            "source_runtime": "generic",
            "format_hint": "generic_jsonl",
        },
    )

    event_activities = {event["event_activity"] for event in store.fetch_recent_events(limit=120)}
    assert result.envelope_id
    assert store.fetch_objects_by_type("observation_digest_skill_runtime_binding")
    assert store.fetch_objects_by_type("observation_digest_invocation_policy")
    assert store.fetch_objects_by_type("observation_digest_invocation_result")
    assert store.fetch_objects_by_type("execution_envelope")
    assert "observation_digest_skill_invocation_requested" in event_activities
    assert "observation_digest_skill_invocation_gate_checked" in event_activities
    assert "observation_digest_skill_invocation_completed" in event_activities
    assert "observation_digest_invocation_result_recorded" in event_activities
    assert store.fetch_object_object_relation_count() > 0
