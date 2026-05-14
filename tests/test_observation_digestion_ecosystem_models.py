from chanta_core.observation_digest import (
    ObservationDigestionEcosystemComponent,
    ObservationDigestionEcosystemConsolidationService,
)
from chanta_core.utility.time import utc_now_iso


def test_ecosystem_snapshot_can_be_created_with_skill_counts() -> None:
    service = ObservationDigestionEcosystemConsolidationService()
    snapshot = service.create_ecosystem_snapshot()

    assert snapshot.version == "0.19.9"
    assert snapshot.observation_skill_count > 0
    assert snapshot.digestion_skill_count > 0
    assert snapshot.executable_external_candidate_count == 0


def test_component_readiness_levels_work() -> None:
    component = ObservationDigestionEcosystemComponent(
        component_id="observation_digestion_ecosystem_component:public-dummy",
        snapshot_id="observation_digestion_ecosystem_snapshot:public-dummy",
        component_name="public_dummy_component",
        component_kind="future_track",
        status="planned",
        readiness_level="future_track",
        object_refs=[],
        dependency_refs=[],
        finding_refs=[],
        created_at=utc_now_iso(),
    )

    assert component.to_dict()["readiness_level"] == "future_track"

