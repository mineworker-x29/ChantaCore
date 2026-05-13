from chanta_core.execution.promotion import ExecutionResultPromotionService
from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from tests.test_execution_result_promotion_service import build_execution_result


def test_execution_result_promotion_ocel_objects_and_events(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)

    service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="memory_candidate",
    )
    service.review_candidate(candidate=service.last_candidate, decision="no_action")

    assert store.fetch_objects_by_type("execution_result_promotion_policy")
    assert store.fetch_objects_by_type("execution_result_promotion_candidate")
    assert store.fetch_objects_by_type("execution_result_promotion_review_request")
    assert store.fetch_objects_by_type("execution_result_promotion_decision")
    assert store.fetch_objects_by_type("execution_result_promotion_result")
    activities = {event["event_activity"] for event in store.fetch_recent_events(100)}
    assert "execution_result_promotion_candidate_created" in activities
    assert "execution_result_promotion_no_action_selected" in activities
    assert "execution_result_promotion_result_recorded" in activities


def test_execution_result_promotion_pig_counts(tmp_path) -> None:
    store, envelope, output, summary = build_execution_result(tmp_path)
    service = ExecutionResultPromotionService(ocel_store=store)
    service.create_candidate_from_envelope(
        envelope=envelope,
        output_snapshot=output,
        outcome_summary=summary,
        target_kind="memory_candidate",
        private=True,
    )
    service.review_candidate(candidate=service.last_candidate, decision="approved_for_later_promotion")
    service.review_candidate(candidate=service.last_candidate, decision="rejected")
    service.review_candidate(candidate=service.last_candidate, decision="no_action")

    objects = []
    for object_type in [
        "execution_result_promotion_policy",
        "execution_result_promotion_candidate",
        "execution_result_promotion_review_request",
        "execution_result_promotion_decision",
        "execution_result_promotion_finding",
        "execution_result_promotion_result",
    ]:
        for row in store.fetch_objects_by_type(object_type):
            objects.append(
                OCPXObjectView(
                    object_id=row["object_id"],
                    object_type=row["object_type"],
                    object_attrs=row["object_attrs"],
                )
            )
    summary_view = PIGReportService._skill_usage_summary(
        OCPXProcessView(view_id="view:test", source="test", session_id=None, events=[], objects=objects)
    )

    assert summary_view["execution_result_promotion_candidate_count"] == 1
    assert summary_view["execution_result_promotion_pending_review_count"] == 1
    assert summary_view["execution_result_promotion_approved_for_later_count"] == 1
    assert summary_view["execution_result_promotion_rejected_count"] == 1
    assert summary_view["execution_result_promotion_no_action_count"] == 1
    assert summary_view["execution_result_promotion_private_risk_count"] == 1
    assert summary_view["execution_result_promotion_by_target_kind"]["memory_candidate"] == 1
