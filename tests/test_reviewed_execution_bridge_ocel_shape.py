from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.proposal import SkillInvocationProposal
from chanta_core.skills.proposal_review import SkillProposalReviewService
from chanta_core.skills.reviewed_execution_bridge import ReviewedExecutionBridgeService
from chanta_core.utility.time import utc_now_iso


def make_proposal(root_path: str, skill_id: str = "skill:read_workspace_text_file") -> SkillInvocationProposal:
    return SkillInvocationProposal(
        proposal_id=f"skill_invocation_proposal:{skill_id.replace(':', '_')}",
        intent_id="skill_proposal_intent:ocel_bridge",
        requirement_id="skill_proposal_requirement:ocel_bridge",
        skill_id=skill_id,
        proposal_status="proposed",
        invocation_mode="review_only",
        proposed_input_payload={"root_path": root_path, "relative_path": "note.txt"},
        missing_inputs=[],
        confidence=0.8,
        reason="ocel bridge",
        review_required=True,
        executable_now=False,
        created_at=utc_now_iso(),
    )


def approve(proposal: SkillInvocationProposal):
    review_service = SkillProposalReviewService()
    review_result = review_service.review_proposal(
        proposal=proposal,
        decision="approve",
        reviewer_type="human",
        reviewer_id="tester",
        reason="approved",
    )
    return review_service.last_decision, review_result


def test_reviewed_execution_bridge_records_ocel_objects_events_and_relations(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    store = OCELStore(tmp_path / "bridge.sqlite")
    proposal = make_proposal(str(tmp_path))
    review_decision, review_result = approve(proposal)
    service = ReviewedExecutionBridgeService(ocel_store=store)

    result = service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )

    assert result.executed is True
    for object_type in [
        "reviewed_execution_bridge_request",
        "reviewed_execution_bridge_decision",
        "reviewed_execution_bridge_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "reviewed_execution_bridge_requested" in events
    assert "reviewed_execution_bridge_decision_recorded" in events
    assert "reviewed_execution_bridge_allowed" in events
    assert "reviewed_execution_bridge_invocation_requested" in events
    assert "reviewed_execution_bridge_gate_completed" in events
    assert "reviewed_execution_bridge_executed" in events
    assert "reviewed_execution_bridge_result_recorded" in events
    relations = store.fetch_object_object_relations_for_object(result.bridge_result_id)
    assert any(item["qualifier"] == "summarizes_bridge_request" for item in relations)
    assert any(item["qualifier"] == "references_skill_execution_gate_result" for item in relations)


def test_reviewed_execution_bridge_pig_summary_counts(tmp_path) -> None:
    (tmp_path / "note.txt").write_bytes(b"public-safe text")
    store = OCELStore(tmp_path / "bridge.sqlite")
    service = ReviewedExecutionBridgeService(ocel_store=store)
    proposal = make_proposal(str(tmp_path))
    review_decision, review_result = approve(proposal)
    service.bridge_reviewed_proposal(
        proposal=proposal,
        review_decision=review_decision,
        review_result=review_result,
    )
    shell_proposal = make_proposal(str(tmp_path), skill_id="skill:shell")
    shell_review_decision, shell_review_result = approve(shell_proposal)
    service.bridge_reviewed_proposal(
        proposal=shell_proposal,
        review_decision=shell_review_decision,
        review_result=shell_review_result,
    )

    objects = []
    for object_type in [
        "reviewed_execution_bridge_request",
        "reviewed_execution_bridge_decision",
        "reviewed_execution_bridge_result",
        "reviewed_execution_bridge_violation",
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

    assert summary["reviewed_execution_bridge_request_count"] == 2
    assert summary["reviewed_execution_bridge_allowed_count"] == 1
    assert summary["reviewed_execution_bridge_unsupported_count"] == 1
    assert summary["reviewed_execution_bridge_executed_count"] == 1
    assert summary["reviewed_execution_bridge_blocked_count"] == 1
    assert summary["reviewed_execution_bridge_by_skill_id"]["skill:read_workspace_text_file"] == 1
    assert summary["reviewed_execution_bridge_violation_by_type"]["shell_not_supported"] == 1
