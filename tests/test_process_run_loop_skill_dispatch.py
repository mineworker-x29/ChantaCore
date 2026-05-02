from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.runtime.loop import ProcessRunLoop
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
        return "Hello from dispatched skill."


def test_process_run_loop_dispatches_llm_chat_skill(tmp_path) -> None:
    store = OCELStore(tmp_path / "skill_dispatch.sqlite")
    loop = ProcessRunLoop(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )

    result = loop.run(
        process_instance_id="process_instance:test-skill-dispatch",
        session_id="test-session-skill-dispatch",
        agent_id="chanta_core_default",
        user_input="skill dispatch test",
        system_prompt="You are a test agent.",
    )

    assert result.status == "completed"
    assert result.response_text == "Hello from dispatched skill."
    assert result.observations[0].success is True
    assert result.observations[0].output_attrs["skill_id"] == "skill:llm_chat"
    assert result.observations[0].output_attrs["skill_name"] == "llm_chat"

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-skill-dispatch")
    ]
    assert activities == [
        "start_process_run_loop",
        "decide_next_activity",
        "select_skill",
        "execute_skill",
        "assemble_context",
        "call_llm",
        "receive_llm_response",
        "observe_result",
        "record_outcome",
        "complete_process_instance",
    ]

    skills = store.fetch_objects_by_type("skill")
    assert [skill["object_id"] for skill in skills] == ["skill:llm_chat"]

    with sqlite3.connect(store.db_path) as connection:
        selected_skill_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_event_object_relation_ext AS relation
            JOIN chanta_event_payload AS event
                ON event.event_id = relation.event_id
            WHERE event.event_activity = 'select_skill'
                AND relation.object_id = 'skill:llm_chat'
                AND relation.qualifier = 'selected_skill'
            """
        ).fetchone()[0]
        executed_skill_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_event_object_relation_ext AS relation
            JOIN chanta_event_payload AS event
                ON event.event_id = relation.event_id
            WHERE event.event_activity = 'execute_skill'
                AND relation.object_id = 'skill:llm_chat'
                AND relation.qualifier = 'executed_skill'
            """
        ).fetchone()[0]

    assert int(selected_skill_count) == 1
    assert int(executed_skill_count) == 1
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True
