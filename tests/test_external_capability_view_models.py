from chanta_core.external import ExternalCapabilityImportService, ExternalCapabilityRegistryViewService
from chanta_core.external.ids import new_external_capability_registry_snapshot_id
from chanta_core.external.views import ExternalCapabilityRegistrySnapshot
from chanta_core.ocel.store import OCELStore
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def test_registry_snapshot_to_dict_and_id_prefix() -> None:
    snapshot = ExternalCapabilityRegistrySnapshot(
        snapshot_id=new_external_capability_registry_snapshot_id(),
        snapshot_name="snapshot",
        source_ids=["external_capability_source:1"],
        descriptor_ids=["external_capability_descriptor:1"],
        normalization_ids=["external_capability_normalization:1"],
        candidate_ids=["external_assimilation_candidate:1"],
        risk_note_ids=["external_capability_risk_note:1"],
        disabled_candidate_count=1,
        execution_enabled_candidate_count=0,
        pending_review_count=1,
        high_risk_count=1,
        critical_risk_count=0,
        created_at=utc_now_iso(),
        snapshot_attrs={"k": "v"},
    )

    data = snapshot.to_dict()

    assert data["snapshot_id"].startswith("external_capability_registry_snapshot:")
    assert data["disabled_candidate_count"] == 1
    assert data["execution_enabled_candidate_count"] == 0
    assert data["snapshot_attrs"] == {"k": "v"}


def test_snapshot_counts_execution_enabled_without_candidate_mutation(tmp_path) -> None:
    import_service = ExternalCapabilityImportService(
        trace_service=TraceService(ocel_store=OCELStore(tmp_path / "view_models.sqlite")),
    )
    source = import_service.register_source(source_name="provided", source_type="provided_dict")
    descriptor, normalization, candidate = import_service.import_as_disabled_candidate(
        raw_descriptor={"name": "external_tool", "type": "tool"},
        source=source,
    )
    object.__setattr__(candidate, "execution_enabled", True)
    original_status = candidate.activation_status
    view_service = ExternalCapabilityRegistryViewService()

    snapshot = view_service.build_registry_snapshot(
        sources=[source],
        descriptors=[descriptor],
        normalizations=[normalization],
        candidates=[candidate],
        risk_notes=[],
    )

    assert snapshot.execution_enabled_candidate_count == 1
    assert candidate.activation_status == original_status
    assert candidate.execution_enabled is True
