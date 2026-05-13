from chanta_core.skills.history_adapter import (
    observation_digest_conformance_checks_to_history_entries,
    observation_digest_conformance_findings_to_history_entries,
    observation_digest_conformance_reports_to_history_entries,
    observation_digest_smoke_results_to_history_entries,
)
from chanta_core.skills.observation_digest_conformance import ObservationDigestConformanceService


def test_observation_digest_conformance_history_entries():
    service = ObservationDigestConformanceService()

    report = service.run_conformance(skill_id="skill:missing")

    entries = [
        *observation_digest_conformance_checks_to_history_entries(service.last_checks),
        *observation_digest_conformance_findings_to_history_entries(service.last_findings),
        *observation_digest_conformance_reports_to_history_entries([report]),
        *observation_digest_smoke_results_to_history_entries(service.last_smoke_results),
    ]

    assert {entry.source for entry in entries} == {"observation_digest_conformance"}
    assert any(entry.priority >= 85 for entry in entries)
    assert any(
        any(ref.get("ref_type") == "observation_digest_conformance_report" for ref in entry.refs)
        for entry in entries
    )
