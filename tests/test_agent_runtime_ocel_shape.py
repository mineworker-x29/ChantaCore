from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.runtime.agent_runtime import AgentRuntime
from chanta_core.traces.trace_service import TraceService


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FakeLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        return "Hello from fake LLM."


def test_agent_runtime_writes_expected_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "test_ocel.sqlite")
    trace_service = TraceService(ocel_store=store)
    runtime = AgentRuntime(
        llm_client=FakeLLMClient(),
        trace_service=trace_service,
    )

    result = runtime.run(
        "shape test",
        session_id="test-session-ocel-shape",
    )

    assert [event.event_type for event in result.events] == [
        "user_request_received",
        "agent_run_started",
        "process_run_loop_started",
        "next_activity_decided",
        "skill_decision_recorded",
        "skill_selected",
        "skill_executed",
        "context_assembled",
        "llm_call_started",
        "llm_response_received",
        "result_observed",
        "outcome_recorded",
        "process_instance_completed",
    ]
    assert store.fetch_event_count() == 13
    assert store.fetch_object_count() >= 11
    assert store.fetch_event_object_relation_count() > 0
    assert store.fetch_object_object_relation_count() > 0

    object_types = {
        object_type
        for object_type in [
            "session",
            "agent",
            "user_request",
            "process_instance",
            "skill",
            "prompt",
            "llm_call",
            "llm_response",
            "outcome",
        ]
        if store.fetch_objects_by_type(object_type)
    }
    assert object_types == {
        "session",
        "agent",
        "user_request",
        "process_instance",
        "skill",
        "prompt",
        "llm_call",
        "llm_response",
        "outcome",
    }

    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True

    activities = [event["event_activity"] for event in store.fetch_events_by_session(
        "test-session-ocel-shape"
    )]
    assert activities == [
        "receive_user_request",
        "start_process_instance",
        "start_process_run_loop",
        "decide_next_activity",
        "decide_skill",
        "select_skill",
        "execute_skill",
        "assemble_context",
        "call_llm",
        "receive_llm_response",
        "observe_result",
        "record_outcome",
        "complete_process_instance",
    ]

    with sqlite3.connect(store.db_path) as connection:
        row = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_object_object_relation_ext
            WHERE source_object_id LIKE 'request:%'
                AND target_object_id = ?
                AND qualifier = ?
            """,
            (
                "session:test-session-ocel-shape",
                "belongs_to_session",
            ),
        ).fetchone()
    assert int(row[0]) == 1

    with sqlite3.connect(store.db_path) as connection:
        row = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_object_object_relation_ext
            WHERE source_object_id LIKE 'process_instance:%'
                AND target_object_id LIKE 'request:%'
                AND qualifier = ?
            """,
            ("derived_from_request",),
        ).fetchone()
    assert int(row[0]) == 1
