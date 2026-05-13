from chanta_core.ocpx.models import OCPXObjectView, OCPXProcessView
from chanta_core.pig.reports import PIGReportService
from chanta_core.skills.observation_digest_proposal import ObservationDigestProposalService


def test_jsonl_observation_request_maps_to_agent_trace_observe():
    service = ObservationDigestProposalService()

    intent = service.classify_intent("이 JSONL 로그 보고 이 agent가 뭘 했는지 봐줘")

    assert intent.intent_family == "observation"
    assert "skill:agent_trace_observe" in intent.suggested_skill_ids


def test_observation_request_creates_proposal_set_and_missing_inputs():
    service = ObservationDigestProposalService()

    result = service.propose("이 JSONL 로그 보고 이 agent가 뭘 했는지 봐줘")

    assert service.last_set is not None
    assert result.status == "needs_more_input"
    assert result.execution_performed is False
    assert result.review_required is True
    assert any("root_path" in proposal.missing_inputs for proposal in service.last_skill_proposals)


def test_digestion_request_maps_to_external_source_and_static_digest():
    service = ObservationDigestProposalService()

    result = service.propose("이 외부 skill 폴더를 소화해줘")
    skill_ids = [proposal.skill_id for proposal in service.last_skill_proposals]

    assert result.status == "needs_more_input"
    assert "skill:external_skill_source_inspect" in skill_ids
    assert "skill:external_skill_static_digest" in skill_ids


def test_mixed_request_creates_ordered_proposal_set():
    service = ObservationDigestProposalService()

    service.propose("JSONL trace를 관찰하고 external skill 후보로 소화해줘")

    assert service.last_set is not None
    assert service.last_set.family == "mixed_observation_digestion"
    assert service.last_set.set_attrs["ordered_skill_ids"][0] == "skill:agent_trace_observe"
    assert "skill:external_skill_static_digest" in service.last_set.set_attrs["ordered_skill_ids"]


def test_unknown_intent_produces_no_matching_skill():
    service = ObservationDigestProposalService()

    result = service.propose("public generic unrelated request")

    assert result.status == "no_matching_skill"
    assert any(item.finding_type == "no_matching_skill" for item in service.last_findings)


def test_registry_unavailable_degrades_gracefully():
    class BrokenRegistry:
        def build_registry_view(self):
            raise RuntimeError("unavailable")

    service = ObservationDigestProposalService(skill_registry_view_service=BrokenRegistry())

    result = service.propose("JSONL trace를 관찰해줘")

    assert result.created_proposal_count == 1
    assert service.registry_available is False


def test_observation_digest_proposal_pig_counts_are_visible():
    view = OCPXProcessView(
        view_id="view:demo",
        source="test",
        session_id=None,
        events=[],
        objects=[
            OCPXObjectView(
                object_id="intent:one",
                object_type="observation_digest_intent_candidate",
                object_attrs={"intent_family": "observation"},
            ),
            OCPXObjectView(
                object_id="binding:one",
                object_type="observation_digest_proposal_binding",
                object_attrs={"skill_id": "skill:agent_trace_observe"},
            ),
            OCPXObjectView(
                object_id="set:one",
                object_type="observation_digest_proposal_set",
                object_attrs={"status": "needs_more_input"},
            ),
            OCPXObjectView(
                object_id="finding:one",
                object_type="observation_digest_proposal_finding",
                object_attrs={"finding_type": "missing_required_input"},
            ),
        ],
    )

    summary = PIGReportService._observation_digest_proposal_summary(
        {
            "observation_digest_intent_candidate": 1,
            "observation_digest_proposal_binding": 1,
            "observation_digest_proposal_set": 1,
            "observation_digest_proposal_finding": 1,
        },
        {},
        view,
    )

    assert summary["observation_digest_proposal_observation_count"] == 1
    assert summary["observation_digest_proposal_needs_more_input_count"] == 1
    assert summary["observation_digest_proposal_by_skill_id"] == {"skill:agent_trace_observe": 1}
    assert summary["observation_digest_proposal_finding_by_type"] == {"missing_required_input": 1}
