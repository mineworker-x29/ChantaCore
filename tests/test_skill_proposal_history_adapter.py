from chanta_core.skills.history_adapter import (
    skill_invocation_proposals_to_history_entries,
    skill_proposal_intents_to_history_entries,
    skill_proposal_results_to_history_entries,
    skill_proposal_review_notes_to_history_entries,
)
from chanta_core.skills.proposal import SkillProposalRouterService


def test_skill_proposal_history_entries_use_expected_source_and_priority() -> None:
    service = SkillProposalRouterService()
    result = service.propose_from_prompt(user_prompt="read file")

    intent_entries = skill_proposal_intents_to_history_entries([service.last_intent])
    proposal_entries = skill_invocation_proposals_to_history_entries(service.last_proposals)
    result_entries = skill_proposal_results_to_history_entries([result])
    note_entries = skill_proposal_review_notes_to_history_entries(service.last_review_notes)

    assert intent_entries[0].source == "skill_proposal"
    assert proposal_entries[0].priority >= 70
    assert result_entries[0].entry_attrs["proposal_only"] is True
    assert any(entry.entry_attrs["note_type"] == "missing_input" for entry in note_entries)
