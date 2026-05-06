from __future__ import annotations

from pathlib import Path

from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.verification import VerificationService


def main() -> int:
    store = OCELStore(Path("data/verification/test_verification_contracts.sqlite"))
    service = VerificationService(trace_service=TraceService(ocel_store=store))

    contract = service.register_contract(
        contract_name="README exists contract",
        contract_type="file_existence",
        required_evidence_kinds=["manual_note"],
        pass_criteria={"manual_confirmation": True},
    )
    target = service.register_target(
        target_type="file",
        target_ref="README.md",
        target_label="README",
    )
    service.register_requirement(
        contract_id=contract.contract_id,
        requirement_type="must_exist",
        description="README.md should be present according to supplied evidence.",
        evidence_kind="manual_note",
    )
    run = service.start_run(
        contract_id=contract.contract_id,
        target_ids=[target.target_id],
    )
    evidence = service.record_evidence(
        run_id=run.run_id,
        target_id=target.target_id,
        evidence_kind="manual_note",
        source_kind="manual",
        content="Manual evidence only. No file check was executed.",
        confidence=0.75,
    )
    result = service.record_result(
        contract_id=contract.contract_id,
        run_id=run.run_id,
        target_id=target.target_id,
        status="passed",
        evidence_ids=[evidence.evidence_id],
        reason="Manual evidence was supplied.",
    )
    completed = service.complete_run(run=run)

    print(f"contract_id: {contract.contract_id}")
    print(f"target_id: {target.target_id}")
    print(f"run_id: {completed.run_id}")
    print(f"evidence_id: {evidence.evidence_id}")
    print(f"result_id: {result.result_id}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
