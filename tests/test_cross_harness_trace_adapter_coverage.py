from chanta_core.observation import CrossHarnessTraceAdapterService
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService


def test_coverage_report_for_implemented_and_stub_adapters():
    service = CrossHarnessTraceAdapterService()

    implemented = service.create_adapter_coverage_report("GenericJSONLTranscriptAdapter")
    stub = service.create_adapter_coverage_report("CodexTaskLogAdapter")

    assert implemented.coverage_status == "implemented"
    assert implemented.mapped_event_type_count > 0
    assert stub.coverage_status == "stub"
    assert stub.unmapped_event_type_count >= 1


def test_pig_cross_harness_counts_visible():
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView("contract:1", "harness_trace_adapter_contract", {"implemented": True}),
            OCPXObjectView("plan:1", "harness_trace_normalization_plan", {"source_runtime": "generic_jsonl", "plan_attrs": {"adapter_name": "GenericJSONLTranscriptAdapter"}}),
            OCPXObjectView("rule:1", "harness_trace_mapping_rule", {"target_action_type": "observe_context"}),
            OCPXObjectView("finding:1", "harness_trace_adapter_finding", {"finding_type": "adapter_not_implemented"}),
            OCPXObjectView("event:1", "agent_observation_normalized_event_v2", {"event_attrs": {"adapter_name": "GenericJSONLTranscriptAdapter"}}),
        ],
    )
    summary = PIGReportService._cross_harness_trace_adapter_summary(
        {
            "harness_trace_adapter_contract": 1,
            "harness_trace_normalization_plan": 1,
            "harness_trace_mapping_rule": 1,
            "harness_trace_adapter_finding": 1,
        },
        {},
        view,
    )

    assert summary["harness_trace_adapter_contract_count"] == 1
    assert summary["harness_trace_normalized_event_count"] == 1
    assert summary["harness_trace_normalization_by_adapter"]["GenericJSONLTranscriptAdapter"] == 1
