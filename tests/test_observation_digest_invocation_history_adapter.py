from chanta_core.skills.history_adapter import (
    observation_digest_invocation_findings_to_history_entries,
    observation_digest_invocation_results_to_history_entries,
    observation_digest_runtime_bindings_to_history_entries,
)
from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService


def test_observation_digest_invocation_history_entries():
    service = ObservationDigestSkillInvocationService()
    bindings = service.create_runtime_bindings()
    result = service.invoke_skill(skill_id="skill:unknown", input_payload={})

    entries = [
        *observation_digest_runtime_bindings_to_history_entries(bindings[:1]),
        *observation_digest_invocation_results_to_history_entries([result]),
        *observation_digest_invocation_findings_to_history_entries(service.last_findings),
    ]

    assert {entry.source for entry in entries} == {"observation_digest_invocation"}
    assert any(entry.priority >= 90 for entry in entries)
    assert any(
        any(ref.get("ref_type") == "observation_digest_invocation_result" for ref in entry.refs)
        for entry in entries
    )
