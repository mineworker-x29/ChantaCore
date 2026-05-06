from __future__ import annotations

from uuid import uuid4


def new_process_outcome_contract_id() -> str:
    return f"process_outcome_contract:{uuid4()}"


def new_process_outcome_criterion_id() -> str:
    return f"process_outcome_criterion:{uuid4()}"


def new_process_outcome_target_id() -> str:
    return f"process_outcome_target:{uuid4()}"


def new_process_outcome_signal_id() -> str:
    return f"process_outcome_signal:{uuid4()}"


def new_process_outcome_evaluation_id() -> str:
    return f"process_outcome_evaluation:{uuid4()}"
