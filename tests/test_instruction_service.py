from chanta_core.instructions import InstructionService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_instruction_service_records_instruction_rule_and_preference(tmp_path) -> None:
    store = OCELStore(tmp_path / "instructions.sqlite")
    service = InstructionService(trace_service=TraceService(ocel_store=store))

    instruction = service.register_instruction_artifact(
        instruction_type="project",
        title="Project Rules",
        body="Use OCEL as canonical persistence.",
        session_id="session:test",
        message_id="message:test",
    )
    updated_instruction = service.revise_instruction_artifact(
        instruction=instruction,
        new_body="Use OCEL as canonical persistence. Avoid canonical JSONL.",
    )
    rule = service.register_project_rule(
        rule_type="constraint",
        text="Do not create Markdown memory views in v0.10.1.",
        source_instruction_id=updated_instruction.instruction_id,
    )
    updated_rule = service.revise_project_rule(
        rule=rule,
        new_text="Do not create canonical Markdown memory views in v0.10.1.",
    )
    preference = service.register_user_preference(
        preference_key="report_style",
        preference_value="concise",
        session_id="session:test",
        message_id="message:test",
    )
    updated_preference = service.revise_user_preference(
        preference=preference,
        new_value="concise with evidence",
    )

    activities = [event["event_activity"] for event in store.fetch_recent_events(20)]

    assert updated_instruction.body_hash != instruction.body_hash
    assert updated_rule.text.startswith("Do not create canonical")
    assert updated_preference.preference_value == "concise with evidence"
    assert "instruction_artifact_registered" in activities
    assert "instruction_artifact_revised" in activities
    assert "project_rule_registered" in activities
    assert "project_rule_revised" in activities
    assert "user_preference_registered" in activities
    assert "user_preference_revised" in activities
    assert store.fetch_objects_by_type("instruction_artifact")
    assert store.fetch_objects_by_type("project_rule")
    assert store.fetch_objects_by_type("user_preference")


def test_instruction_service_deprecates_instruction(tmp_path) -> None:
    store = OCELStore(tmp_path / "instruction_deprecated.sqlite")
    service = InstructionService(trace_service=TraceService(ocel_store=store))
    instruction = service.register_instruction_artifact(
        instruction_type="policy",
        title="Old",
        body="old",
    )

    deprecated = service.deprecate_instruction_artifact(
        instruction=instruction,
        reason="test",
    )

    activities = [event["event_activity"] for event in store.fetch_recent_events(10)]
    assert deprecated.status == "deprecated"
    assert "instruction_artifact_deprecated" in activities
