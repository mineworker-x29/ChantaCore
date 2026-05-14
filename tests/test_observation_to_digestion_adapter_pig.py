from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService


def test_pig_ocpx_adapter_builder_counts_visible() -> None:
    view = OCPXProcessView(
        view_id="ocpx_process_view:public-dummy",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="observed_capability_candidate:public",
                object_type="observed_capability_candidate",
                object_attrs={"capability_category": "read_file"},
            ),
            OCPXObjectView(
                object_id="observation_digestion_adapter_candidate:public",
                object_type="observation_digestion_adapter_candidate",
                object_attrs={
                    "risk_class": "low",
                    "target_skill_id": "skill:read_workspace_text_file",
                    "mapping_type": "observed_behavior_to_skill_candidate",
                },
            ),
            OCPXObjectView(
                object_id="adapter_unsupported_feature:public",
                object_type="adapter_unsupported_feature",
                object_attrs={"feature_type": "shell_execution"},
            ),
        ],
    )

    summary = PIGReportService._observation_to_digestion_adapter_summary(
        {
            "observed_capability_candidate": 1,
            "observation_digestion_adapter_candidate": 1,
            "adapter_unsupported_feature": 1,
        },
        {},
        view,
    )

    assert summary["observed_capability_candidate_count"] == 1
    assert summary["observation_digestion_adapter_candidate_count"] == 1
    assert summary["adapter_candidate_by_risk_class"]["low"] == 1
    assert summary["adapter_candidate_by_target_skill_id"]["skill:read_workspace_text_file"] == 1
    assert summary["adapter_candidate_by_mapping_type"]["observed_behavior_to_skill_candidate"] == 1
    assert summary["unsupported_feature_by_type"]["shell_execution"] == 1
    assert summary["observed_capability_by_category"]["read_file"] == 1

