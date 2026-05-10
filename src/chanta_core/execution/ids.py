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
