from chanta_core.external.history_adapter import external_capability_registry_snapshots_to_history_entries
from chanta_core.external.views import ExternalCapabilityRegistrySnapshot
from chanta_core.utility.time import utc_now_iso


def test_registry_snapshot_history_adapter_refs_and_priority() -> None:
    snapshot = ExternalCapabilityRegistrySnapshot(
        snapshot_id="external_capability_registry_snapshot:history",
        snapshot_name="history",
        source_ids=["external_capability_source:history"],
        descriptor_ids=["external_capability_descriptor:history"],
        normalization_ids=["external_capability_normalization:history"],
        candidate_ids=["external_assimilation_candidate:history"],
        risk_note_ids=["external_capability_risk_note:history"],
        disabled_candidate_count=1,
        execution_enabled_candidate_count=1,
        pending_review_count=1,
        high_risk_count=1,
        critical_risk_count=0,
        created_at=utc_now_iso(),
        snapshot_attrs={},
    )

    entry = external_capability_registry_snapshots_to_history_entries([snapshot])[0]

    assert entry.source == "external_capability_view"
    assert entry.refs[0]["snapshot_id"] == snapshot.snapshot_id
    assert entry.refs[0]["source_ids"] == snapshot.source_ids
    assert entry.refs[0]["descriptor_ids"] == snapshot.descriptor_ids
    assert entry.refs[0]["candidate_ids"] == snapshot.candidate_ids
    assert entry.refs[0]["risk_note_ids"] == snapshot.risk_note_ids
    assert entry.priority >= 90
