from uuid import uuid4


def new_verification_contract_id() -> str:
    return f"verification_contract:{uuid4()}"


def new_verification_target_id() -> str:
    return f"verification_target:{uuid4()}"


def new_verification_requirement_id() -> str:
    return f"verification_requirement:{uuid4()}"


def new_verification_run_id() -> str:
    return f"verification_run:{uuid4()}"


def new_verification_evidence_id() -> str:
    return f"verification_evidence:{uuid4()}"


def new_verification_result_id() -> str:
    return f"verification_result:{uuid4()}"
