from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.utility.time import utc_now_iso


def make_proposal(
    *,
    skill_id: str = "skill:read_workspace_text_file",
    missing_inputs: list[str] | None = None,
) -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id=f"skill_invocation_proposal:{skill_id.replace(':', '_')}",
        intent_id="skill_proposal_intent:ocel",
        requirement_id="skill_proposal_requirement:ocel",
        skill_id=skill_id,
        proposal_status="incomplete" if missing_inputs else "proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": "<WORKSPACE_ROOT>", "relative_path": "docs/example.txt"},
        missing_inputs=list(missing_inputs or []),
        confidence=0.8,
        reason="ocel test",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def test_skill_proposal_review_records_ocel_objects_events_and_relations(tmp_path) -> None:
    store = OCELStore(tmp_path / "review.sqlite")
    service = SkillProposalReviewService(ocel_store=store)

    result = service.review_proposal(
        proposal=make_proposal(),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="complete read-only proposal",
    )

    assert result.status == "approved"
    for object_type in [
        "skill_proposal_review_contract",
        "skill_proposal_review_request",
        "skill_proposal_review_decision",
        "skill_proposal_review_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "skill_proposal_review_contract_registered" in events
    assert "skill_proposal_review_requested" in events
    assert "skill_proposal_review_decision_recorded" in events
    assert "skill_proposal_review_result_recorded" in events
    assert "skill_proposal_review_approved" in events
    relations = store.fetch_object_object_relations_for_object(result.review_result_id)
    assert any(item["qualifier"] == "summarizes_review_request" for item in relations)
    assert any(item["qualifier"] == "references_decision" for item in relations)


def test_skill_proposal_review_pig_summary_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "review.sqlite")
    service = SkillProposalReviewService(ocel_store=store)
    service.review_proposal(
        proposal=make_proposal(),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="complete read-only proposal",
    )
    service.review_proposal(
        proposal=make_proposal(skill_id="skill:shell"),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="try shell",
    )
    service.review_proposal(
        proposal=make_proposal(missing_inputs=["root_path"]),
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="try missing",
    )
    service.review_proposal(
        proposal=make_proposal(),
        decision="no-action",
        reviewer_type="human",
        reviewer_id="tester",
        reason="do nothing",
    )

    objects = []
    for object_type in [
        "skill_proposal_review_contract",
        "skill_proposal_review_request",
        "skill_proposal_review_decision",
        "skill_proposal_review_finding",
        "skill_proposal_review_result",
    ]:
        for row in store.fetch_objects_by_type(object_type):
            objects.append(
                type(
                    "Obj",
                    (),
                    {
                        "object_id": row["object_id"],
                        "object_type": row["object_type"],
                        "object_attrs": row["object_attrs"],
                    },
                )()
            )
    view = OCPXProcessView(
        view_id="view:test",
        source="test",
        session_id=None,
        events=[],
        objects=objects,
    )

    summary = PIGReportService._skill_usage_summary(view)

    assert summary["skill_proposal_review_request_count"] == 4
    assert summary["skill_proposal_review_approved_count"] == 1
    assert summary["skill_proposal_review_rejected_count"] == 1
    assert summary["skill_proposal_review_needs_more_input_count"] == 1
    assert summary["skill_proposal_review_no_action_count"] == 1
    assert summary["skill_proposal_review_bridge_candidate_count"] == 1
    assert summary["skill_proposal_review_by_skill_id"]["skill:read_workspace_text_file"] == 3
    assert summary["skill_proposal_review_by_decision"]["approved_for_explicit_invocation"] == 3
