from chanta_core.observation_digest import ObservationDigestionEcosystemConsolidationService


def test_consolidation_report_and_capability_map() -> None:
    service = ObservationDigestionEcosystemConsolidationService()
    report = service.consolidate()

    assert report.status == "completed"
    assert report.total_component_count >= 8
    families = {item.capability_family for item in service.last_capability_maps}
    assert {"observation", "digestion", "adapter_mapping"} <= families
    assert service.last_release_manifest is not None
    assert service.last_release_manifest.included_versions == [f"v0.19.{index}" for index in range(10)]


def test_unavailable_component_degrades_gracefully() -> None:
    service = ObservationDigestionEcosystemConsolidationService(
        unavailable_components={"skill_registry_view"},
    )
    report = service.consolidate()

    assert report.status == "warning"
    assert any(item.component_name == "skill_registry_view" for item in service.last_components)
    assert any(item.finding_type == "component_unavailable" for item in service.last_findings)

