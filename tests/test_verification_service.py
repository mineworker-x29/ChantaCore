import pytest

from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService
from chanta_core.verification.errors import VerificationResultError


def test_verification_service_records_lifecycle_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "verification_service.sqlite")
    service = VerificationService(trace_service=TraceService(ocel_store=store))

    contract = service.register_contract(
        contract_name="README contract",
        contract_type="file_existence",
    )
    target = service.register_target(target_type="file", target_ref="README.md")
    requirement = service.register_requirement(
        contract_id=contract.contract_id,
        requirement_type="must_exist",
        description="README must be represented by evidence.",
    )
    run = service.start_run(
        contract_id=contract.contract_id,
        target_ids=[target.target_id],
        session_id="session:verification",
        turn_id="conversation_turn:verification",
        process_instance_id="process_instance:verification",
    )
    evidence = service.record_evidence(
        run_id=run.run_id,
        target_id=target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="Manual note only.",
    )
    result = service.record_result(
        contract_id=contract.contract_id,
        run_id=run.run_id,
        target_id=target.target_id,
        status="passed",
        evidence_ids=[evidence.evidence_id],
    )
    completed = service.complete_run(run=run)
    service.attach_result_to_process(
        result_id=result.result_id,
        process_instance_id="process_instance:verification",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert requirement.contract_id == contract.contract_id
    assert completed.status == "completed"
    assert {
        "verification_contract_registered",
        "verification_target_registered",
        "verification_requirement_registered",
        "verification_run_started",
        "verification_run_completed",
        "verification_evidence_recorded",
        "verification_result_recorded",
        "verification_result_attached_to_process",
    }.issubset(activities)


def test_verification_service_run_terminal_events_and_result_validation(tmp_path) -> None:
    store = OCELStore(tmp_path / "verification_service_terminal.sqlite")
    service = VerificationService(trace_service=TraceService(ocel_store=store))
    contract = service.register_contract(contract_name="Manual", contract_type="manual")
    run = service.start_run(contract_id=contract.contract_id, target_ids=[])

    failed = service.fail_run(run=run, error_message="manual failure")
    skipped = service.skip_run(run=run, reason="manual skip")
    with pytest.raises(VerificationResultError):
        service.record_result(contract_id=contract.contract_id, status="failed")

    activities = {event["event_activity"] for event in store.fetch_recent_events(50)}
    assert failed.status == "failed"
    assert skipped.status == "skipped"
    assert "verification_run_failed" in activities
    assert "verification_run_skipped" in activities


def test_verification_service_does_not_execute_real_checks(tmp_path) -> None:
    store = OCELStore(tmp_path / "verification_service_no_checks.sqlite")
    service = VerificationService(trace_service=TraceService(ocel_store=store))
    contract = service.register_contract(
        contract_name="File contract",
        contract_type="file_existence",
    )
    target = service.register_target(
        target_type="file",
        target_ref="definitely-not-checked-by-service.txt",
    )
    run = service.start_run(contract_id=contract.contract_id, target_ids=[target.target_id])

    assert run.status == "running"
    assert not store.fetch_objects_by_type("verification_evidence")
    assert not store.fetch_objects_by_type("verification_result")
