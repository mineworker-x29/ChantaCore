from chanta_core.ocel.store import OCELStore
from chanta_core.ocpx.models import OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.proposal import SkillProposalRouterService


def test_skill_proposal_records_ocel_objects_events_and_relations(tmp_path) -> None:
    store = OCELStore(tmp_path / "proposal.sqlite")
    service = SkillProposalRouterService(ocel_store=store)

    result = service.propose_from_prompt(
        user_prompt="read file docs/example.txt",
        root_path="<WORKSPACE_ROOT>",
    )

    assert result.status == "proposal_available"
    for object_type in [
        "skill_proposal_intent",
        "skill_proposal_requirement",
        "skill_invocation_proposal",
        "skill_proposal_decision",
        "skill_proposal_review_note",
        "skill_proposal_result",
    ]:
        assert store.fetch_objects_by_type(object_type)
    events = {item["event_activity"] for item in store.fetch_recent_events(limit=100)}
    assert "skill_proposal_intent_created" in events
    assert "skill_proposal_requirement_recorded" in events
    assert "skill_invocation_proposal_created" in events
    assert "skill_proposal_decision_recorded" in events
    assert "skill_proposal_result_recorded" in events
    relations = store.fetch_object_object_relations_for_object(result.result_id)
    assert any(item["qualifier"] == "belongs_to_skill_proposal_intent" for item in relations)


def test_skill_proposal_pig_summary_counts(tmp_path) -> None:
    store = OCELStore(tmp_path / "proposal.sqlite")
    service = SkillProposalRouterService(ocel_store=store)
    service.propose_from_prompt(
        user_prompt="read file docs/example.txt",
        root_path="<WORKSPACE_ROOT>",
    )
    service.propose_from_prompt(user_prompt="run shell command")

    objects = []
    for object_type in [
        "skill_proposal_intent",
        "skill_proposal_requirement",
        "skill_invocation_proposal",
        "skill_proposal_decision",
        "skill_proposal_review_note",
        "skill_proposal_result",
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

    assert summary["skill_proposal_intent_count"] == 2
    assert summary["skill_proposal_available_count"] == 1
    assert summary["skill_proposal_unsupported_count"] == 1
    assert summary["skill_proposal_by_skill_id"]["skill:read_workspace_text_file"] == 1
    assert summary["skill_proposal_by_requested_operation"]["shell_execution"] == 1
