from chanta_core.observation import CrossHarnessTraceAdapterService
from chanta_core.skills.history_adapter import (
    cross_harness_adapter_policies_to_history_entries,
    harness_trace_adapter_contracts_to_history_entries,
    harness_trace_adapter_coverage_reports_to_history_entries,
    harness_trace_adapter_findings_to_history_entries,
    harness_trace_adapter_results_to_history_entries,
    harness_trace_mapping_rules_to_history_entries,
    harness_trace_normalization_results_to_history_entries,
    harness_trace_source_inspections_to_history_entries,
)


def test_cross_harness_history_adapters(tmp_path):
    trace_file = tmp_path / "trace.jsonl"
    trace_file.write_bytes(b'{"id":"u1","role":"user","content":"input"}\n')
    service = CrossHarnessTraceAdapterService()
    policy = service.create_default_policy()
    contracts = service.register_adapter_contracts()
    rules = service.register_default_mapping_rules()
    inspection = service.inspect_trace_source(root_path=str(tmp_path), relative_path="trace.jsonl", runtime_hint="generic_jsonl")
    result = service.normalize_file(root_path=str(tmp_path), relative_path="trace.jsonl", runtime_hint="generic_jsonl")
    coverage = service.create_adapter_coverage_report("GenericJSONLTranscriptAdapter")
    finding = service.record_finding(adapter_name="StubAdapter", source_runtime="stub", subject_ref="trace", finding_type="adapter_not_implemented", status="stub", severity="medium", message="Stub only.")
    adapter_result = service.record_result(operation_kind="test", status="completed", adapter_name="GenericJSONLTranscriptAdapter", source_runtime="generic_jsonl", created_object_refs=[], summary="ok")

    entries = []
    entries += cross_harness_adapter_policies_to_history_entries([policy])
    entries += harness_trace_adapter_contracts_to_history_entries(contracts[:1])
    entries += harness_trace_mapping_rules_to_history_entries(rules[:1])
    entries += harness_trace_source_inspections_to_history_entries([inspection])
    entries += harness_trace_normalization_results_to_history_entries([result])
    entries += harness_trace_adapter_coverage_reports_to_history_entries([coverage])
    entries += harness_trace_adapter_findings_to_history_entries([finding])
    entries += harness_trace_adapter_results_to_history_entries([adapter_result])

    assert entries
    assert {entry.source for entry in entries} == {"cross_harness_trace_adapter"}
