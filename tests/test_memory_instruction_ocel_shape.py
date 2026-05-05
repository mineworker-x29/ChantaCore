from chanta_core.instructions import InstructionService
from chanta_core.memory import MemoryService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_memory_instruction_ocel_object_and_event_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "memory_instruction_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    memory_service = MemoryService(trace_service=trace_service)
    instruction_service = InstructionService(trace_service=trace_service)

    memory = memory_service.create_memory_entry(
        memory_type="semantic",
        title="OCEL",
        content="Memory uses OCEL.",
        session_id="session:test",
        message_id="message:test",
    )
    memory_service.revise_memory_entry(
        memory=memory,
        new_content="Memory and instruction use OCEL.",
    )
    instruction = instruction_service.register_instruction_artifact(
        instruction_type="project",
        title="Project",
        body="Use OCEL.",
    )
    instruction_service.register_project_rule(
        rule_type="constraint",
        text="No canonical JSONL memory.",
        source_instruction_id=instruction.instruction_id,
    )
    instruction_service.register_user_preference(
        preference_key="style",
        preference_value="direct",
        session_id="session:test",
        message_id="message:test",
    )

    object_types = {
        object_type
        for object_type in [
            "memory_entry",
            "memory_revision",
            "instruction_artifact",
            "project_rule",
            "user_preference",
        ]
        if store.fetch_objects_by_type(object_type)
    }
    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}

    assert object_types == {
        "memory_entry",
        "memory_revision",
        "instruction_artifact",
        "project_rule",
        "user_preference",
    }
    for activity in [
        "memory_entry_created",
        "memory_revision_recorded",
        "memory_entry_revised",
        "instruction_artifact_registered",
        "project_rule_registered",
        "user_preference_registered",
    ]:
        assert activity in activities
