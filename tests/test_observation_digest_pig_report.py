from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService


def test_pig_observation_digest_counts_are_visible():
    view = OCPXProcessView(
        view_id="view:demo",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="event:demo",
                object_type="agent_observation_normalized_event",
                object_attrs={"observed_activity": "user_message_observed"},
            ),
            OCPXObjectView(
                object_id="run:demo",
                object_type="observed_agent_run",
                object_attrs={"inferred_runtime": "dummy_runtime"},
            ),
            OCPXObjectView(
                object_id="candidate:demo",
                object_type="external_skill_assimilation_candidate",
                object_attrs={"risk_class": "read_only", "review_status": "pending_review"},
            ),
            OCPXObjectView(
                object_id="adapter:demo",
                object_type="external_skill_adapter_candidate",
                object_attrs={"requires_review": True},
            ),
        ],
    )
    object_counts = {
        "agent_observation_normalized_event": 1,
        "observed_agent_run": 1,
        "external_skill_assimilation_candidate": 1,
        "external_skill_adapter_candidate": 1,
    }

    summary = PIGReportService._observation_digest_summary(
        object_counts,
        {"agent_observation_source_inspected": 1},
        view,
    )

    assert summary["agent_observation_normalized_event_count"] == 1
    assert summary["observed_event_by_activity"] == {"user_message_observed": 1}
    assert summary["observed_run_by_source_runtime"] == {"dummy_runtime": 1}
    assert summary["external_candidate_by_risk_class"] == {"read_only": 1}
    assert summary["external_candidate_pending_review_count"] == 1
    assert summary["adapter_candidate_pending_review_count"] == 1
