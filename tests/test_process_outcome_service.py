from chanta_core.ocel.store import OCELStore
from chanta_core.outcomes import ProcessOutcomeEvaluationService
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService


def _services(tmp_path, name: str):
    store = OCELStore(tmp_path / f"{name}.sqlite")
    trace_service = TraceService(ocel_store=store)
    return store, VerificationService(trace_service=trace_service), ProcessOutcomeEvaluationService(trace_service=trace_service)


def _verification_result(verification_service: VerificationService, status: str = "passed", evidence: bool = True):
    contract = verification_service.register_contract(contract_name=f"{status} contract", contract_type="manual")
    target = verification_service.register_target(target_type="process_instance", target_ref="process_instance:test")
    run = verification_service.start_run(contract_id=contract.contract_id, target_ids=[target.target_id])
    evidence_ids: list[str] = []
    if evidence:
        item = verification_service.record_evidence(
            run_id=run.run_id,
            target_id=target.target_id,
            evidence_kind="manual_note",
            source_kind="manual",
            content=f"{status} evidence",
        )
        evidence_ids.append(item.evidence_id)
    return verification_service.record_result(
        contract_id=contract.contract_id,
        run_id=run.run_id,
        target_id=target.target_id,
        status=status,
        confidence=0.8,
        evidence_ids=evidence_ids,
    )


def test_process_outcome_service_records_lifecycle_events(tmp_path) -> None:
    store, verification_service, service = _services(tmp_path, "outcome_service")
    verification_result = _verification_result(verification_service)
    contract = service.register_contract(
        contract_name="Completion",
        contract_type="process_completion",
        target_type="process_instance",
    )
    criterion = service.register_criterion(
        contract_id=contract.contract_id,
        criterion_type="verification_passed",
        description="Verification must pass.",
    )
    target = service.register_target(
        target_type="process_instance",
        target_ref="process_instance:test",
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
        process_instance_id="process_instance:test",
    )
    signal = service.record_signal(
        target_id=target.target_id,
        signal_type="verification_passed",
        signal_value="passed",
        source_kind="verification_result",
        source_ref=verification_result.result_id,
    )
    evaluation = service.record_evaluation(
        contract_id=contract.contract_id,
        target_id=target.target_id,
        outcome_status="success",
        score=1.0,
        confidence=0.8,
        evidence_coverage=1.0,
        passed_criteria_ids=[criterion.criterion_id],
        signal_ids=[signal.signal_id],
        verification_result_ids=[verification_result.result_id],
    )
    attach = service.attach_evaluation_to_process(
        evaluation_id=evaluation.evaluation_id,
        process_instance_id="process_instance:test",
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert attach["process_status_changed"] is False
    assert {
        "process_outcome_contract_registered",
        "process_outcome_criterion_registered",
        "process_outcome_target_registered",
        "process_outcome_signal_recorded",
        "process_outcome_evaluation_recorded",
        "process_outcome_attached_to_process",
    }.issubset(activities)


def test_evaluate_from_verification_results_status_policy(tmp_path) -> None:
    _, verification_service, service = _services(tmp_path, "outcome_policy")
    contract = service.register_contract(
        contract_name="Strict completion",
        contract_type="process_completion",
        min_required_pass_rate=1.0,
        min_evidence_coverage=1.0,
    )
    target = service.register_target(target_type="process_instance", target_ref="process_instance:test")

    assert service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[],
    ).outcome_status == "inconclusive"

    passed = _verification_result(verification_service, "passed", evidence=True)
    assert service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[passed],
    ).outcome_status == "success"

    inconclusive = _verification_result(verification_service, "inconclusive", evidence=False)
    partial = service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[passed, inconclusive],
    )
    assert partial.outcome_status == "partial_success"
    assert partial.evidence_coverage == 0.5

    failed = _verification_result(verification_service, "failed", evidence=True)
    assert service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[failed],
    ).outcome_status == "failed"

    skipped = _verification_result(verification_service, "skipped", evidence=False)
    assert service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[skipped],
    ).outcome_status == "skipped"

    error = _verification_result(verification_service, "error", evidence=False)
    assert service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[error],
    ).outcome_status == "error"


def test_process_outcome_service_does_not_mutate_runtime_behavior(tmp_path) -> None:
    _, verification_service, service = _services(tmp_path, "outcome_no_mutation")
    result = _verification_result(verification_service)
    contract = service.register_contract(contract_name="Manual", contract_type="manual")
    target = service.register_target(target_type="manual", target_ref="manual:test")

    evaluation = service.evaluate_from_verification_results(
        contract=contract,
        target=target,
        verification_results=[result],
    )

    assert evaluation.evaluation_attrs["runtime_behavior_mutated"] is False
    assert evaluation.evaluation_attrs["tools_blocked_or_modified"] is False
    assert evaluation.score == 1.0
    assert evaluation.confidence == 0.8
    assert evaluation.evidence_coverage == 1.0
