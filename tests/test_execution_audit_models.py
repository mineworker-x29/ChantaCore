from chanta_core.execution.audit import (
    ExecutionAuditFilter,
    ExecutionAuditFinding,
    ExecutionAuditQuery,
    ExecutionAuditRecordView,
    ExecutionAuditResult,
)
from chanta_core.utility.time import utc_now_iso


def test_execution_audit_models_to_dict() -> None:
    now = utc_now_iso()
    query = ExecutionAuditQuery(
        audit_query_id="execution_audit_query:test",
        query_type="list",
        requested_by="tester",
        session_id="session:test",
        turn_id="turn:test",
        limit=5,
        show_paths=False,
        show_full_payloads=False,
        created_at=now,
    )
    audit_filter = ExecutionAuditFilter(
        audit_filter_id="execution_audit_filter:test",
        audit_query_id=query.audit_query_id,
        envelope_id=None,
        skill_id="skill:read_workspace_text_file",
        session_id="session:test",
        turn_id=None,
        process_instance_id=None,
        status="completed",
        execution_kind=None,
        blocked=False,
        failed=False,
        since=None,
        until=None,
        limit=5,
        created_at=now,
    )
    view = ExecutionAuditRecordView(
        record_view_id="execution_audit_record_view:test",
        audit_query_id=query.audit_query_id,
        envelope_id="execution_envelope:test",
        execution_kind="gated_skill_invocation",
        skill_id="skill:read_workspace_text_file",
        status="completed",
        execution_allowed=True,
        execution_performed=True,
        blocked=False,
        session_id="session:test",
        turn_id=None,
        process_instance_id=None,
        gate_decision_id="skill_execution_gate_decision:test",
        gate_result_id="skill_execution_gate_result:test",
        explicit_invocation_result_id="explicit_skill_invocation_result:test",
        output_snapshot_id="execution_output_snapshot:test",
        output_preview={"content": "preview"},
        input_preview={"relative_path": "<REDACTED_PATH>"},
        redacted=True,
        created_at=now,
    )
    finding = ExecutionAuditFinding(
        finding_id="execution_audit_finding:test",
        audit_query_id=query.audit_query_id,
        envelope_id=view.envelope_id,
        finding_type="full_payload_hidden",
        status="hidden",
        severity="low",
        message="hidden",
        subject_ref=view.envelope_id,
        created_at=now,
    )
    result = ExecutionAuditResult(
        audit_result_id="execution_audit_result:test",
        audit_query_id=query.audit_query_id,
        filter_id=audit_filter.audit_filter_id,
        status="completed",
        matched_count=1,
        returned_count=1,
        record_view_ids=[view.record_view_id],
        finding_ids=[finding.finding_id],
        summary="completed",
        created_at=now,
    )

    assert query.to_dict()["query_type"] == "list"
    assert audit_filter.to_dict()["skill_id"] == "skill:read_workspace_text_file"
    assert view.to_dict()["redacted"] is True
    assert finding.to_dict()["finding_type"] == "full_payload_hidden"
    assert result.to_dict()["returned_count"] == 1
