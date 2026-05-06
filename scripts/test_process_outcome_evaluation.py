from __future__ import annotations

from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.outcomes import ProcessOutcomeEvaluationService
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService


def main() -> None:
    store = OCELStore(Path("data/verification/test_process_outcome_evaluation.sqlite"))
    trace_service = TraceService(ocel_store=store)
    verification_service = VerificationService(trace_service=trace_service)
    outcome_service = ProcessOutcomeEvaluationService(trace_service=trace_service)

    verification_contract = verification_service.register_contract(
        contract_name="Sample verification",
        contract_type="manual",
    )
    verification_target = verification_service.register_target(
        target_type="process_instance",
        target_ref="process_instance:sample",
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
        content="Sample deterministic evidence.",
    )
    verification_result = verification_service.record_result(
        contract_id=verification_contract.contract_id,
        run_id=run.run_id,
        target_id=verification_target.target_id,
        status="passed",
        confidence=0.9,
        evidence_ids=[evidence.evidence_id],
    )
    verification_service.complete_run(run=run)

    outcome_contract = outcome_service.register_contract(
        contract_name="Sample process completion",
        contract_type="process_completion",
        target_type="process_instance",
        min_required_pass_rate=1.0,
        min_evidence_coverage=1.0,
    )
    outcome_target = outcome_service.register_target(
        target_type="process_instance",
        target_ref="process_instance:sample",
        process_instance_id="process_instance:sample",
    )
    evaluation = outcome_service.evaluate_from_verification_results(
        contract=outcome_contract,
        target=outcome_target,
        verification_results=[verification_result],
    )

    print(f"verification_result_ids={evaluation.verification_result_ids}")
    print(f"outcome_evaluation_id={evaluation.evaluation_id}")
    print(f"outcome_status={evaluation.outcome_status}")
    print(f"score={evaluation.score}")
    print(f"confidence={evaluation.confidence}")
    print(f"evidence_coverage={evaluation.evidence_coverage}")


if __name__ == "__main__":
    main()
