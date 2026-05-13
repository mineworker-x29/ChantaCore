from chanta_core.execution.audit import ExecutionAuditService
from chanta_core.execution.history_adapter import (
    execution_audit_findings_to_history_entries,
    execution_audit_queries_to_history_entries,
    execution_audit_results_to_history_entries,
)
from tests.test_execution_audit_service import build_store


def test_execution_audit_history_entries(tmp_path) -> None:
    store, *_ = build_store(tmp_path)
    service = ExecutionAuditService(ocel_store=store)
    service.query_envelopes(blocked=True)

    query_entries = execution_audit_queries_to_history_entries([service.last_query])
    result_entries = execution_audit_results_to_history_entries([service.last_result])
    finding_entries = execution_audit_findings_to_history_entries(service.last_findings)

    assert query_entries[0].source == "execution_audit"
    assert result_entries[0].source == "execution_audit"
    assert finding_entries[0].source == "execution_audit"
    assert max(item.priority for item in finding_entries) >= 85
