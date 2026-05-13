from __future__ import annotations

from uuid import uuid4


def new_execution_envelope_id() -> str:
    return f"execution_envelope:{uuid4()}"


def new_execution_provenance_record_id() -> str:
    return f"execution_provenance_record:{uuid4()}"


def new_execution_input_snapshot_id() -> str:
    return f"execution_input_snapshot:{uuid4()}"


def new_execution_output_snapshot_id() -> str:
    return f"execution_output_snapshot:{uuid4()}"


def new_execution_artifact_ref_id() -> str:
    return f"execution_artifact_ref:{uuid4()}"


def new_execution_outcome_summary_id() -> str:
    return f"execution_outcome_summary:{uuid4()}"


def new_execution_audit_query_id() -> str:
    return f"execution_audit_query:{uuid4()}"


def new_execution_audit_filter_id() -> str:
    return f"execution_audit_filter:{uuid4()}"


def new_execution_audit_record_view_id() -> str:
    return f"execution_audit_record_view:{uuid4()}"


def new_execution_audit_result_id() -> str:
    return f"execution_audit_result:{uuid4()}"


def new_execution_audit_finding_id() -> str:
    return f"execution_audit_finding:{uuid4()}"


def new_execution_result_promotion_policy_id() -> str:
    return f"execution_result_promotion_policy:{uuid4()}"


def new_execution_result_promotion_candidate_id() -> str:
    return f"execution_result_promotion_candidate:{uuid4()}"


def new_execution_result_promotion_review_request_id() -> str:
    return f"execution_result_promotion_review_request:{uuid4()}"


def new_execution_result_promotion_decision_id() -> str:
    return f"execution_result_promotion_decision:{uuid4()}"


def new_execution_result_promotion_finding_id() -> str:
    return f"execution_result_promotion_finding:{uuid4()}"


def new_execution_result_promotion_result_id() -> str:
    return f"execution_result_promotion_result:{uuid4()}"
