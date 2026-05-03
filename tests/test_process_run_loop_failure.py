from __future__ import annotations

import sqlite3
from dataclasses import dataclass

from chanta_core.llm.types import ChatMessage
from chanta_core.ocel.store import OCELStore
from chanta_core.ocel.validators import OCELValidator
from chanta_core.ocpx.loader import OCPXLoader
from chanta_core.pig.service import PIGService
from chanta_core.runtime.loop import ProcessRunLoop, ProcessRunPolicy
from chanta_core.traces.trace_service import TraceService


@dataclass(frozen=True)
class FakeLLMSettings:
    provider: str = "fake_provider"
    model: str = "fake_model"


class FakeFailingLLMClient:
    settings = FakeLLMSettings()

    def chat_messages(
        self,
        messages: list[ChatMessage],
        temperature: float = 0.7,
        max_tokens: int = 384,
    ) -> str:
        raise RuntimeError("fake LLM failure")


def test_process_run_loop_failure_records_ocel_error_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "loop_failure.sqlite")
    loop = ProcessRunLoop(
        llm_client=FakeFailingLLMClient(),
        trace_service=TraceService(ocel_store=store),
        policy=ProcessRunPolicy(raise_on_failure=False),
    )

    result = loop.run(
        process_instance_id="process_instance:test-loop-failure",
        session_id="test-session-loop-failure",
        agent_id="chanta_core_default",
        user_input="loop failure test",
        system_prompt="You are a test agent.",
    )

    assert result.status == "failed"
    assert result.response_text == ""
    assert result.result_attrs["success"] is False
    assert result.result_attrs["evaluation_mode"] == "runtime_basic"
    assert result.result_attrs["exception_type"] == "RuntimeError"
    assert result.result_attrs["failure_stage"] == "call_llm"
    assert len(result.observations) >= 1
    assert result.observations[-1].success is False
    assert "fake LLM failure" in str(result.observations[-1].error)

    activities = [
        event["event_activity"]
        for event in store.fetch_events_by_session("test-session-loop-failure")
    ]
    assert activities == [
        "start_process_run_loop",
        "decide_next_activity",
        "decide_skill",
        "select_skill",
        "execute_skill",
        "assemble_context",
        "call_llm",
        "fail_skill_execution",
        "observe_result",
        "fail_process_instance",
    ]

    assert store.fetch_objects_by_type("error")
    assert store.fetch_objects_by_type("process_instance")

    with sqlite3.connect(store.db_path) as connection:
        observed_error_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_event_object_relation_ext AS relation
            JOIN chanta_event_payload AS event
                ON event.event_id = relation.event_id
            JOIN chanta_object_state AS object_state
                ON object_state.object_id = relation.object_id
            WHERE event.event_activity = 'fail_process_instance'
                AND relation.qualifier = 'observed_error'
                AND object_state.object_type = 'error'
            """
        ).fetchone()[0]
        error_from_process_count = connection.execute(
            """
            SELECT COUNT(*)
            FROM chanta_object_object_relation_ext
            WHERE source_object_id LIKE 'error:%'
                AND target_object_id = 'process_instance:test-loop-failure'
                AND qualifier = 'error_from_process'
            """
        ).fetchone()[0]

    assert int(observed_error_count) == 1
    assert int(error_from_process_count) >= 1
    assert OCELValidator(store).validate_duplicate_relations()["valid"] is True

    loader = OCPXLoader(store)
    view = loader.load_process_instance_view("process_instance:test-loop-failure")
    assert "fail_process_instance" in [event.event_activity for event in view.events]
    assert "fail_skill_execution" in [event.event_activity for event in view.events]
    assert any(item.object_type == "error" for item in view.objects)

    pig_result = PIGService(loader=loader).analyze_process_instance(
        "process_instance:test-loop-failure"
    )
    assert pig_result["graph"]["nodes"]
    assert any(
        item["diagnostic_id"] == "failed_process_instance"
        for item in pig_result["diagnostics"]
    )
