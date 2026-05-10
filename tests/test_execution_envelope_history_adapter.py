from chanta_core.execution import ExecutionEnvelopeService
from chanta_core.execution.history_adapter import (
    execution_envelopes_to_history_entries,
    execution_outcome_summaries_to_history_entries,
    execution_provenance_records_to_history_entries,
)


def test_execution_envelope_history_entries() -> None:
    service = ExecutionEnvelopeService()
    envelope = service.create_envelope(
        execution_kind="manual",
        execution_subject_id="subject:test",
        skill_id="skill:read_workspace_text_file",
        status="blocked",
        execution_allowed=False,
        execution_performed=False,
        blocked=True,
    )
    provenance = service.record_provenance(envelope=envelope, gate_result_id="skill_execution_gate_result:test")
    summary = service.record_outcome_summary(envelope=envelope, finding_ids=["finding:test"])

    envelope_entries = execution_envelopes_to_history_entries([envelope])
    provenance_entries = execution_provenance_records_to_history_entries([provenance])
    summary_entries = execution_outcome_summaries_to_history_entries([summary])

    assert envelope_entries[0].source == "execution_envelope"
    assert envelope_entries[0].priority >= 80
    assert provenance_entries[0].entry_attrs["has_gate"] is True
    assert summary_entries[0].entry_attrs["blocked"] is True
