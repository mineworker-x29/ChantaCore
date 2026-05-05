from chanta_core.pig.context import PIGContext


def test_pig_context_to_dict_preserves_fields() -> None:
    context = PIGContext(
        source="pig",
        scope="recent",
        process_instance_id=None,
        session_id=None,
        activity_sequence=["receive_user_request"],
        event_activity_counts={"receive_user_request": 1},
        object_type_counts={"session": 1},
        relation_coverage={
            "events_total": 1,
            "events_with_related_objects": 1,
            "events_without_related_objects": 0,
            "coverage_ratio": 1.0,
        },
        basic_variant={
            "variant_key": "receive_user_request",
            "activity_sequence": ["receive_user_request"],
            "event_count": 1,
        },
        performance_summary={
            "start_timestamp": "2026-05-02T00:00:00Z",
            "end_timestamp": "2026-05-02T00:00:00Z",
            "duration_seconds": 0.0,
            "event_count": 1,
            "llm_call_count": 0,
            "skill_execution_count": 0,
            "failure_count": 0,
        },
        guide={"event_count": 1},
        diagnostics=[],
        recommendations=[],
        context_text="Process Intelligence Context:\n- Scope: recent",
        context_attrs={"limit": 20},
    )

    data = context.to_dict()

    assert data["context_text"] == context.context_text
    assert data["activity_sequence"] == ["receive_user_request"]
    assert data["relation_coverage"]["coverage_ratio"] == 1.0
    assert data["diagnostics"] == []
    assert data["recommendations"] == []
    assert data["performance_summary"]["failure_count"] == 0

    block = context.to_context_block()
    assert block.block_type == "pig_context"
    assert block.content == context.context_text
