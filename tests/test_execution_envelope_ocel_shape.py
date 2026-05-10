from chanta_core.execution import ExecutionEnvelopeService
from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_execution_envelope_records_ocel_objects_events_and_relations(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    store = OCELStore(tmp_path / "envelope.sqlite")
    invocation_service = ExplicitSkillInvocationService()
    invocation_result = invocation_service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )
    envelope_service = ExecutionEnvelopeService(ocel_store=store)

    envelope = envelope_service.wrap_explicit_invocation_result(
        invocation_result=invocation_result,
        invocation_request=invocation_service.last_request,
        invocation_input=invocation_service.last_input,
    )

    for object_type in [
        "execution_envelope",
        "execution_provenance_record",
        "execution_input_snapshot",
        "execution_output_snapshot",
        "execution_outcome_summary",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "execution_envelope_created" in events
    assert "execution_provenance_recorded" in events
    assert "execution_input_snapshot_recorded" in events
    assert "execution_output_snapshot_recorded" in events
    assert "execution_outcome_summary_recorded" in events
    assert "execution_envelope_completed" in events
    relations = store.fetch_object_object_relations_for_object(envelope_service.last_provenance.provenance_id)
    assert any(item["qualifier"] == "belongs_to_execution_envelope" for item in relations)
    assert envelope.status == "completed"


def test_execution_envelope_pig_summary_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "envelope.sqlite")
    service = ExecutionEnvelopeService(ocel_store=store)
    envelope = service.create_envelope(
        execution_kind="gated_skill_invocation",
        execution_subject_id="skill_execution_gate_result:test",
        skill_id="skill:read_workspace_text_file",
        status="completed",
        execution_allowed=True,
        execution_performed=True,
        blocked=False,
    )
    service.record_input_snapshot(envelope=envelope, input_payload={"relative_path": "note.txt"})
    service.record_output_snapshot(envelope=envelope, output_payload={"output_text": "public-safe text"})
    service.record_provenance(envelope=envelope, gate_result_id="skill_execution_gate_result:test")
    service.record_outcome_summary(envelope=envelope, output_snapshot_id=service.last_output_snapshot.output_snapshot_id)

    objects = []
    for object_type in [
        "execution_envelope",
        "execution_provenance_record",
        "execution_input_snapshot",
        "execution_output_snapshot",
        "execution_outcome_summary",
    ]:
        for row in store.fetch_objects_by_type(object_type):
            objects.append(
                type(
                    "Obj",
                    (),
                    {
                        "object_id": row["object_id"],
                        "object_type": row["object_type"],
                        "object_attrs": row["object_attrs"],
                    },
                )()
            )
    view = OCPXProcessView(view_id="view:test", source="test", session_id=None, events=[], objects=objects)

    summary = PIGReportService._skill_usage_summary(view)

    assert summary["execution_envelope_count"] == 1
    assert summary["execution_provenance_record_count"] == 1
    assert summary["execution_input_snapshot_count"] == 1
    assert summary["execution_output_snapshot_count"] == 1
    assert summary["execution_outcome_summary_count"] == 1
    assert summary["execution_completed_count"] == 1
    assert summary["execution_by_kind"]["gated_skill_invocation"] == 1
    assert summary["execution_with_gate_count"] == 1
    assert summary["execution_full_input_stored_count"] == 0
    assert summary["execution_full_output_stored_count"] == 0
