from __future__ import annotations

from uuid import uuid4


def new_explicit_skill_invocation_request_id() -> str:
    return f"explicit_skill_invocation_request:{uuid4()}"


def new_explicit_skill_invocation_input_id() -> str:
    return f"explicit_skill_invocation_input:{uuid4()}"


def new_explicit_skill_invocation_decision_id() -> str:
    return f"explicit_skill_invocation_decision:{uuid4()}"


def new_explicit_skill_invocation_result_id() -> str:
    return f"explicit_skill_invocation_result:{uuid4()}"


def new_explicit_skill_invocation_violation_id() -> str:
    return f"explicit_skill_invocation_violation:{uuid4()}"


def new_skill_proposal_intent_id() -> str:
    return f"skill_proposal_intent:{uuid4()}"


def new_skill_proposal_requirement_id() -> str:
    return f"skill_proposal_requirement:{uuid4()}"


def new_skill_invocation_proposal_id() -> str:
    return f"skill_invocation_proposal:{uuid4()}"


def new_skill_proposal_decision_id() -> str:
    return f"skill_proposal_decision:{uuid4()}"


def new_skill_proposal_review_note_id() -> str:
    return f"skill_proposal_review_note:{uuid4()}"


def new_skill_proposal_result_id() -> str:
    return f"skill_proposal_result:{uuid4()}"


def new_read_only_execution_gate_policy_id() -> str:
    return f"read_only_execution_gate_policy:{uuid4()}"


def new_skill_execution_gate_request_id() -> str:
    return f"skill_execution_gate_request:{uuid4()}"


def new_skill_execution_gate_decision_id() -> str:
    return f"skill_execution_gate_decision:{uuid4()}"


def new_skill_execution_gate_finding_id() -> str:
    return f"skill_execution_gate_finding:{uuid4()}"


def new_skill_execution_gate_result_id() -> str:
    return f"skill_execution_gate_result:{uuid4()}"
