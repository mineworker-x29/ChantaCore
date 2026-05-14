from chanta_core.observation_digest import (
    ObservationDigestionEcosystemConsolidationService,
    capability_maps_to_history_entries,
    consolidation_findings_to_history_entries,
    consolidation_reports_to_history_entries,
    ecosystem_components_to_history_entries,
    ecosystem_snapshots_to_history_entries,
    gap_registers_to_history_entries,
    release_manifests_to_history_entries,
    safety_boundary_reports_to_history_entries,
)


def test_ecosystem_history_entries_use_expected_source() -> None:
    service = ObservationDigestionEcosystemConsolidationService(
        external_candidate_fixtures=[{"candidate_id": "external_candidate:public", "execution_enabled": True}],
    )
    service.consolidate()

    entries = [
        *ecosystem_snapshots_to_history_entries([service.last_snapshot]),
        *ecosystem_components_to_history_entries(service.last_components),
        *capability_maps_to_history_entries(service.last_capability_maps),
        *safety_boundary_reports_to_history_entries([service.last_safety_report]),
        *gap_registers_to_history_entries(service.last_gap_registers),
        *release_manifests_to_history_entries([service.last_release_manifest]),
        *consolidation_findings_to_history_entries(service.last_findings),
        *consolidation_reports_to_history_entries([service.last_report]),
    ]

    assert entries
    assert {item.source for item in entries} == {"observation_digestion_ecosystem_consolidation"}
    assert max(item.priority for item in entries) >= 90

