from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.engine import OCPXEngine
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.service import PIGService
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


def test_process_instance_runtime_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "process.sqlite")
    runtime = AgentRuntime(
        llm_client=FakeLLMClient(),
        trace_service=TraceService(ocel_store=store),
    )

    result = runtime.run(
        "runtime instance test",
        session_id="test-session-process-instance",
    )

    assert result.response_text == "Hello from fake LLM."

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-process-instance")
    ]
    expected_process_activities = [
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
    assert "session_started" in activities
    assert "conversation_turn_started" in activities
    assert "user_message_received" in activities
    assert "assistant_message_emitted" in activities
    assert "conversation_turn_completed" in activities
    assert _is_contiguous_subsequence(expected_process_activities, activities)

    assert store.fetch_objects_by_type("process_instance")
    assert not store.fetch_objects_by_type("goal")
    assert not store.fetch_objects_by_type("mission")
    assert not store.fetch_objects_by_type("task_instance")
    assert not store.fetch_objects_by_type("step_instance")

    skills = store.fetch_objects_by_type("skill")
    assert [skill["object_id"] for skill in skills] == ["skill:llm_chat"]

    with sqlite3.connect(store.db_path) as connection:
        process_id = connection.execute(
            """
            SELECT object_id
            FROM chanta_object_state
            WHERE object_type = 'process_instance'
            """
        ).fetchone()[0]
        relation_counts = {
            qualifier: int(count)
            for qualifier, count in connection.execute(
                """
                SELECT qualifier, COUNT(*)
                FROM chanta_object_object_relation_ext
                WHERE source_object_id = ?
                    OR target_object_id = ?
                GROUP BY qualifier
                """,
                (process_id, process_id),
            ).fetchall()
        }

    assert relation_counts["derived_from_request"] == 1
    assert relation_counts["handled_in_session"] == 1
    assert relation_counts["executed_by_agent"] == 1
    assert relation_counts["uses_skill"] == 1
    assert relation_counts["outcome_of_process"] == 1
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True

    loader = OCPXLoader(store)
    view = loader.load_process_instance_view(process_id)
    engine = OCPXEngine()
    view_activities = engine.activity_sequence(view)
    assert _is_contiguous_subsequence(expected_process_activities[1:], view_activities)
    assert engine.summarize_process_instance_view(view)["process_instance_count"] == 1

    pig_result = PIGService(loader=loader).analyze_process_instance(process_id)
    assert pig_result["graph"]["nodes"]
    assert pig_result["guide"]["process_instance_count"] == 1


def _is_contiguous_subsequence(expected: list[str], actual: list[str]) -> bool:
    width = len(expected)
    return any(actual[index : index + width] == expected for index in range(len(actual) - width + 1))
