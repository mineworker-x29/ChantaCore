from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService


def test_verification_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "verification_shape.sqlite")
    service = VerificationService(trace_service=TraceService(ocel_store=store))

    contract = service.register_contract(
        contract_name="Tool availability contract",
        contract_type="tool_availability",
        required_evidence_kinds=["manual_note"],
    )
    target = service.register_target(target_type="tool", target_ref="tool:workspace")
    service.register_requirement(
        contract_id=contract.contract_id,
        requirement_type="must_be_available",
        description="Tool availability must be represented by supplied evidence.",
    )
    run = service.start_run(contract_id=contract.contract_id, target_ids=[target.target_id])
    evidence = service.record_evidence(
        run_id=run.run_id,
        target_id=target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="Manual observation.",
    )
    service.record_result(
        contract_id=contract.contract_id,
        run_id=run.run_id,
        target_id=target.target_id,
        status="passed",
        evidence_ids=[evidence.evidence_id],
    )
    service.complete_run(run=run)

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert {
        "verification_contract_registered",
        "verification_target_registered",
        "verification_requirement_registered",
        "verification_run_started",
        "verification_run_completed",
        "verification_evidence_recorded",
        "verification_result_recorded",
    }.issubset(activities)
    assert store.fetch_objects_by_type("verification_contract")
    assert store.fetch_objects_by_type("verification_target")
    assert store.fetch_objects_by_type("verification_requirement")
    assert store.fetch_objects_by_type("verification_run")
    assert store.fetch_objects_by_type("verification_evidence")
    assert store.fetch_objects_by_type("verification_result")

    result = store.fetch_objects_by_type("verification_result")[0]["object_attrs"]
    assert result["evidence_ids"] == [evidence.evidence_id]
