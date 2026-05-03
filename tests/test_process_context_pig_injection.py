from chanta_core.pig.context import PIGContext
from chanta_core.runtime.loop.context import ProcessContextAssembler


def fake_pig_context() -> PIGContext:
    return PIGContext(
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
            "start_timestamp": None,
            "end_timestamp": None,
            "duration_seconds": None,
            "event_count": 1,
            "llm_call_count": 0,
            "skill_execution_count": 0,
            "failure_count": 0,
        },
        guide={},
        diagnostics=[],
        recommendations=[],
        context_text="Process Intelligence Context:\n- Scope: recent",
        context_attrs={},
    )


def test_process_context_assembler_injects_pig_context_when_provided() -> None:
    assembler = ProcessContextAssembler()

    messages = assembler.assemble_for_llm_chat(
        user_input="hello",
        system_prompt="system",
        pig_context=fake_pig_context(),
    )

    assert messages == [
        {"role": "system", "content": "system"},
        {
            "role": "system",
            "content": "Process Intelligence Context:\n- Scope: recent",
        },
        {"role": "user", "content": "hello"},
    ]


def test_process_context_assembler_without_pig_context_is_unchanged() -> None:
    assembler = ProcessContextAssembler()

    messages = assembler.assemble_for_llm_chat(
        user_input="hello",
        system_prompt="system",
    )

    assert messages == [
        {"role": "system", "content": "system"},
        {"role": "user", "content": "hello"},
    ]
