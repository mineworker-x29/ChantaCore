from chanta_core.ocel.store import OCELStore
from chanta_core.outcomes import ProcessOutcomeEvaluationService
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService


def test_process_outcome_ocel_shape_contains_expected_objects_and_events(tmp_path) -> None:
    store = OCELStore(tmp_path / "process_outcome_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    verification_service = VerificationService(trace_service=trace_service)
    service = ProcessOutcomeEvaluationService(trace_service=trace_service)

    verification_contract = verification_service.register_contract(
        contract_name="Manual verification",
        contract_type="manual",
    )
    verification_target = verification_service.register_target(
        target_type="process_instance",
        target_ref="process_instance:shape",
    )
    run = verification_service.start_run(
        contract_id=verification_contract.contract_id,
        target_ids=[verification_target.target_id],
    )
    evidence = verification_service.record_evidence(
        run_id=run.run_id,
        target_id=verification_target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="Shape evidence.",
    )
    verification_result = verification_service.record_result(
        contract_id=verification_contract.contract_id,
        run_id=run.run_id,
        target_id=verification_target.target_id,
        status="passed",
        evidence_ids=[evidence.evidence_id],
    )
    contract = service.register_contract(
        contract_name="Outcome shape",
        contract_type="process_completion",
    )
    service.register_criterion(
        contract_id=contract.contract_id,
        criterion_type="verification_passed",
        description="Verification must pass.",
    )
    target = service.register_target(
        target_type="process_instance",
        target_ref="process_instance:shape",
        process_instance_id="process_instance:shape",
    )
    evaluation = service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[verification_result],
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert {
        "process_outcome_contract_registered",
        "process_outcome_criterion_registered",
        "process_outcome_target_registered",
        "process_outcome_signal_recorded",
        "process_outcome_evaluation_started",
        "process_outcome_evaluation_recorded",
    }.issubset(activities)
    assert store.fetch_objects_by_type("process_outcome_contract")
    assert store.fetch_objects_by_type("process_outcome_criterion")
    assert store.fetch_objects_by_type("process_outcome_target")
    assert store.fetch_objects_by_type("process_outcome_signal")
    assert store.fetch_objects_by_type("process_outcome_evaluation")
    assert evaluation.verification_result_ids == [verification_result.result_id]
