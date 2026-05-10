from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.invocation import ExplicitSkillInvocationService


def test_explicit_skill_invocation_records_ocel_objects_events_and_relations(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    store = OCELStore(tmp_path / "invocation.sqlite")
    service = ExplicitSkillInvocationService(ocel_store=store)

    result = service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    assert result.status == "completed"
    for object_type in [
        "explicit_skill_invocation_request",
        "explicit_skill_invocation_input",
        "explicit_skill_invocation_decision",
        "explicit_skill_invocation_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "explicit_skill_invocation_requested" in events
    assert "explicit_skill_invocation_input_recorded" in events
    assert "explicit_skill_invocation_input_validated" in events
    assert "explicit_skill_invocation_decided" in events
    assert "explicit_skill_invocation_started" in events
    assert "explicit_skill_invocation_completed" in events
    relations = store.fetch_object_object_relations_for_object(result.result_id)
    assert any(item["qualifier"] == "belongs_to_invocation_request" for item in relations)


def test_explicit_skill_invocation_pig_summary_counts(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    store = OCELStore(tmp_path / "invocation.sqlite")
    service = ExplicitSkillInvocationService(ocel_store=store)
    service.invoke_explicit_skill(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )
    service.invoke_explicit_skill(
        skill_id="skill:write_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    object_type_counts = {}
    objects = []
    for object_type in [
        "explicit_skill_invocation_request",
        "explicit_skill_invocation_input",
        "explicit_skill_invocation_decision",
        "explicit_skill_invocation_result",
        "explicit_skill_invocation_violation",
    ]:
        rows = store.fetch_objects_by_type(object_type)
        object_type_counts[object_type] = len(rows)
        for row in rows:
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
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=objects,
    )

    summary = PIGReportService._skill_usage_summary(view)

    assert summary["explicit_skill_invocation_request_count"] == 2
    assert summary["explicit_skill_invocation_completed_count"] == 1
    assert summary["explicit_skill_invocation_unsupported_count"] == 1
    assert summary["explicit_skill_invocation_by_skill_id"]["skill:read_workspace_text_file"] == 1
    assert summary["explicit_skill_invocation_violation_by_type"]["unsupported_skill"] == 1
