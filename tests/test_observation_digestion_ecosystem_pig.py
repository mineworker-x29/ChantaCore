from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService


def test_pig_ocpx_ecosystem_counts_visible() -> None:
    view = OCPXProcessView(
        view_id="ocpx_process_view:public-ecosystem",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="observation_digestion_ecosystem_snapshot:public",
                object_type="observation_digestion_ecosystem_snapshot",
                object_attrs={"executable_external_candidate_count": 0},
            ),
            OCPXObjectView(
                object_id="observation_digestion_ecosystem_component:public",
                object_type="observation_digestion_ecosystem_component",
                object_attrs={"component_kind": "internal_skill", "readiness_level": "ready"},
            ),
            OCPXObjectView(
                object_id="observation_digestion_capability_map:public",
                object_type="observation_digestion_capability_map",
                object_attrs={"capability_family": "observation"},
            ),
            OCPXObjectView(
                object_id="observation_digestion_gap_register:public",
                object_type="observation_digestion_gap_register",
                object_attrs={"gap_type": "safety", "gap_attrs": {"future_track": True}},
            ),
        ],
    )

    summary = PIGReportService._observation_digestion_ecosystem_summary(
        {
            "observation_digestion_ecosystem_snapshot": 1,
            "observation_digestion_ecosystem_component": 1,
            "observation_digestion_capability_map": 1,
            "observation_digestion_gap_register": 1,
        },
        {},
        view,
    )

    assert summary["observation_digestion_ecosystem_snapshot_count"] == 1
    assert summary["observation_digestion_ecosystem_component_count"] == 1
    assert summary["observation_digestion_ready_component_count"] == 1
    assert summary["observation_digestion_future_track_gap_count"] == 1
    assert summary["observation_digestion_executable_external_candidate_count"] == 0
    assert summary["observation_digestion_by_component_kind"]["internal_skill"] == 1
    assert summary["observation_digestion_by_capability_family"]["observation"] == 1
    assert summary["observation_digestion_gap_by_type"]["safety"] == 1

