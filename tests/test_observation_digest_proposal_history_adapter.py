from chanta_core.skills.history_adapter import (
    observation_digest_intents_to_history_entries,
    observation_digest_proposal_findings_to_history_entries,
    observation_digest_proposal_results_to_history_entries,
    observation_digest_proposal_sets_to_history_entries,
)
from chanta_core.skills.observation_digest_proposal import ObservationDigestProposalService


def test_observation_digest_proposal_history_entries():
    service = ObservationDigestProposalService()

    result = service.propose("public generic unrelated request")

    entries = [
        *observation_digest_intents_to_history_entries(service.last_intents),
        *observation_digest_proposal_sets_to_history_entries([service.last_set]),
        *observation_digest_proposal_results_to_history_entries([result]),
        *observation_digest_proposal_findings_to_history_entries(service.last_findings),
    ]

    assert {entry.source for entry in entries} == {"observation_digest_proposal"}
    assert any(entry.priority >= 90 for entry in entries)
    assert any(
        any(ref.get("ref_type") == "observation_digest_proposal_result" for ref in entry.refs)
        for entry in entries
    )
