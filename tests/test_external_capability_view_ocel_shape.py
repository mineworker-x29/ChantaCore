from chanta_core.external import ExternalCapabilityImportService, ExternalCapabilityRegistryViewService
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService


def test_external_capability_view_ocel_shape(tmp_path) -> None:
    store = OCELStore(tmp_path / "external_view_shape.sqlite")
    trace_service = TraceService(ocel_store=store)
    import_service = ExternalCapabilityImportService(trace_service=trace_service)
    source = import_service.register_source(source_name="provided", source_type="provided_dict")
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={"name": "external_tool", "type": "tool"},
        source=source,
    )
    note = import_service.record_risk_note(
        descriptor_id=descriptor.descriptor_id,
        candidate_id=candidate.candidate_id,
        risk_level="high",
        risk_categories=["shell_execution"],
        message="Review.",
    )
    view_service = ExternalCapabilityRegistryViewService(trace_service=trace_service, root=tmp_path)

    view_service.refresh_default_external_views(
        root=tmp_path,
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[note],
    )

    activities = {event["event_activity"] for event in store.fetch_recent_events(200)}
    assert {
        "external_capability_registry_snapshot_created",
        "external_capability_registry_view_rendered",
        "external_capability_registry_view_written",
        "external_capability_review_view_rendered",
        "external_capability_review_view_written",
        "external_capability_risk_view_rendered",
        "external_capability_risk_view_written",
    }.issubset(activities)
    assert store.fetch_objects_by_type("external_capability_registry_snapshot")
    assert store.fetch_objects_by_type("materialized_view")
