from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.execution_gate import SkillExecutionGateService


def test_skill_execution_gate_records_ocel_objects_events_and_relations(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    store = OCELStore(tmp_path / "gate.sqlite")
    service = SkillExecutionGateService(ocel_store=store)

    result = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    assert result.executed is True
    for object_type in [
        "read_only_execution_gate_policy",
        "skill_execution_gate_request",
        "skill_execution_gate_decision",
        "skill_execution_gate_finding",
        "skill_execution_gate_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "read_only_execution_gate_policy_registered" in events
    assert "skill_execution_gate_requested" in events
    assert "skill_execution_gate_decision_recorded" in events
    assert "skill_execution_gate_allowed" in events
    assert "skill_execution_gate_result_recorded" in events
    relations = store.fetch_object_object_relations_for_object(result.gate_result_id)
    assert any(item["qualifier"] == "belongs_to_skill_execution_gate_request" for item in relations)


def test_skill_execution_gate_pig_summary_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "gate.sqlite")
    service = SkillExecutionGateService(ocel_store=store)
    service.gate_explicit_invocation(
        skill_id="skill:list_workspace_files",
        input_payload={"root_path": str(tmp_path), "relative_path": "."},
        invocation_mode="test",
    )
    service.gate_explicit_invocation(
        skill_id="skill:write_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "note.txt"},
        invocation_mode="test",
    )

    objects = []
    for object_type in [
        "skill_execution_gate_request",
        "skill_execution_gate_decision",
        "skill_execution_gate_finding",
        "skill_execution_gate_result",
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
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=objects,
    )

    summary = PIGReportService._skill_usage_summary(view)

    assert summary["skill_execution_gate_request_count"] == 2
    assert summary["skill_execution_gate_allowed_count"] == 1
    assert summary["skill_execution_gate_denied_count"] == 1
    assert summary["skill_execution_gate_executed_count"] == 1
    assert summary["skill_execution_gate_blocked_count"] == 1
    assert summary["skill_execution_gate_by_skill_id"]["skill:write_file"] == 1
    assert summary["skill_execution_gate_finding_by_type"]["write_not_allowed"] == 1
