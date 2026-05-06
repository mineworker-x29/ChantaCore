from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService
from chanta_core.verification.read_only_skills import ReadOnlyVerificationSkillService


def test_read_only_skills_create_verification_ocel_flow(tmp_path) -> None:
    store = OCELStore(tmp_path / "read_only_verification_flow.sqlite")
    service = ReadOnlyVerificationSkillService(
        verification_service=VerificationService(trace_service=TraceService(ocel_store=store)),
        root=tmp_path,
        ocel_store=store,
    )
    file_path = tmp_path / "exists.txt"
    file_path.write_text("present", encoding="utf-8")
    materialized = tmp_path / "MEMORY.md"
    materialized.write_text(
        "Generated materialized view\nCanonical source: OCEL\nThis file is not canonical.\nEdits do not update canonical source.",
        encoding="utf-8",
    )
    tool_policy = tmp_path / "TOOL_POLICY.md"
    tool_policy.write_text(
        "This file is not PermissionPolicy. It does not grant, deny, allow, ask, block, or sandbox tool usage. Enforcement belongs to a future permission layer.",
        encoding="utf-8",
    )

    results = [
        service.verify_file_exists(path="exists.txt"),
        service.verify_path_type(path="exists.txt", expected_type="file"),
        service.verify_tool_available(tool_name="definitely_missing_tool"),
        service.verify_runtime_python_info(),
        service.verify_ocel_object_type_exists(object_type="verification_result", known_object_types=["verification_result"]),
        service.verify_ocel_event_activity_exists(event_activity="verification_result_recorded", known_event_activities=["verification_result_recorded"]),
        service.verify_materialized_view_warning(path="MEMORY.md"),
        service.verify_tool_registry_view_warning(path="TOOL_POLICY.md"),
    ]

    assert all(result.evidence_ids for result in results)
    activities = {event["event_activity"] for event in store.fetch_recent_events(200)}
    assert {
        "verification_contract_registered",
        "verification_target_registered",
        "verification_run_started",
        "verification_evidence_recorded",
        "verification_result_recorded",
        "verification_run_completed",
    }.issubset(activities)
    assert store.fetch_objects_by_type("verification_target")
    assert store.fetch_objects_by_type("verification_run")
    assert store.fetch_objects_by_type("verification_evidence")
    assert store.fetch_objects_by_type("verification_result")
