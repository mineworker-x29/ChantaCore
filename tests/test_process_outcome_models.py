import pytest

from chanta_core.outcomes.errors import ProcessOutcomeEvaluationError
from chanta_core.outcomes.ids import (
    new_process_outcome_contract_id,
    new_process_outcome_criterion_id,
    new_process_outcome_evaluation_id,
    new_process_outcome_signal_id,
    new_process_outcome_target_id,
)
from chanta_core.outcomes.models import (
    ProcessOutcomeContract,
    ProcessOutcomeCriterion,
    ProcessOutcomeEvaluation,
    ProcessOutcomeSignal,
    ProcessOutcomeTarget,
)
from chanta_core.utility.time import utc_now_iso


def test_process_outcome_model_to_dicts_and_id_prefixes() -> None:
    now = utc_now_iso()
    contract = ProcessOutcomeContract(
        contract_id=new_process_outcome_contract_id(),
        contract_name="Completion",
        contract_type="process_completion",
        description="Evidence based completion.",
        status="active",
        target_type="process_instance",
        required_verification_contract_ids=["verification_contract:1"],
        min_required_pass_rate=1.0,
        min_evidence_coverage=1.0,
        severity="high",
        created_at=now,
        updated_at=now,
        contract_attrs={"scope": "test"},
    )
    criterion = ProcessOutcomeCriterion(
        criterion_id=new_process_outcome_criterion_id(),
        contract_id=contract.contract_id,
        criterion_type="verification_passed",
        description="Required checks pass.",
        required=True,
        weight=1.0,
        expected_statuses=["passed"],
        status="active",
        criterion_attrs={},
    )
    target = ProcessOutcomeTarget(
        target_id=new_process_outcome_target_id(),
        target_type="process_instance",
        target_ref="process_instance:test",
        target_label="Test process",
        session_id="session:test",
        turn_id="conversation_turn:test",
        message_id="message:test",
        process_instance_id="process_instance:test",
        status="active",
        created_at=now,
        target_attrs={},
    )
    signal = ProcessOutcomeSignal(
        signal_id=new_process_outcome_signal_id(),
        target_id=target.target_id,
        signal_type="verification_passed",
        signal_value="passed",
        strength=0.9,
        source_kind="verification_result",
        source_ref="verification_result:test",
        created_at=now,
        signal_attrs={},
    )
    evaluation = ProcessOutcomeEvaluation(
        evaluation_id=new_process_outcome_evaluation_id(),
        contract_id=contract.contract_id,
        target_id=target.target_id,
        outcome_status="success",
        score=1.0,
        confidence=0.9,
        evidence_coverage=1.0,
        passed_criteria_ids=[criterion.criterion_id],
        failed_criteria_ids=[],
        signal_ids=[signal.signal_id],
        verification_result_ids=["verification_result:test"],
        reason="all passed",
        created_at=now,
        evaluation_attrs={},
    )

    assert contract.to_dict()["contract_id"].startswith("process_outcome_contract:")
    assert criterion.to_dict()["criterion_id"].startswith("process_outcome_criterion:")
    assert target.to_dict()["target_id"].startswith("process_outcome_target:")
    assert signal.to_dict()["signal_id"].startswith("process_outcome_signal:")
    assert evaluation.to_dict()["evaluation_id"].startswith("process_outcome_evaluation:")


def test_process_outcome_evaluation_requires_basis_for_terminal_statuses() -> None:
    now = utc_now_iso()
    with pytest.raises(ProcessOutcomeEvaluationError):
        ProcessOutcomeEvaluation(
            evaluation_id=new_process_outcome_evaluation_id(),
            contract_id="process_outcome_contract:test",
            target_id="process_outcome_target:test",
            outcome_status="failed",
            score=0.0,
            confidence=0.0,
            evidence_coverage=0.0,
            passed_criteria_ids=[],
            failed_criteria_ids=[],
            signal_ids=[],
            verification_result_ids=[],
            reason=None,
            created_at=now,
            evaluation_attrs={},
        )


def test_process_outcome_probability_fields_are_validated() -> None:
    now = utc_now_iso()
    with pytest.raises(ProcessOutcomeEvaluationError):
        ProcessOutcomeEvaluation(
            evaluation_id=new_process_outcome_evaluation_id(),
            contract_id="process_outcome_contract:test",
            target_id="process_outcome_target:test",
            outcome_status="success",
            score=1.2,
            confidence=0.0,
            evidence_coverage=1.0,
            passed_criteria_ids=[],
            failed_criteria_ids=[],
            signal_ids=["process_outcome_signal:test"],
            verification_result_ids=[],
            reason=None,
            created_at=now,
            evaluation_attrs={},
        )
