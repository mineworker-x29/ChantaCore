from chanta_core.skills.execution_gate import SkillExecutionGateService
from chanta_core.skills.history_adapter import (
    skill_execution_gate_decisions_to_history_entries,
    skill_execution_gate_findings_to_history_entries,
    skill_execution_gate_results_to_history_entries,
)


def test_skill_execution_gate_history_entries_use_expected_source_and_priority() -> None:
    service = SkillExecutionGateService()
    result = service.gate_explicit_invocation(
        skill_id="skill:write_file",
        input_payload={"root_path": "<ROOT>", "relative_path": "docs/example.txt"},
    )

    decision_entries = skill_execution_gate_decisions_to_history_entries([service.last_decision])
    result_entries = skill_execution_gate_results_to_history_entries([result])
    finding_entries = skill_execution_gate_findings_to_history_entries(service.last_findings)

    assert decision_entries[0].source == "skill_execution_gate"
    assert decision_entries[0].priority >= 80
    assert result_entries[0].entry_attrs["blocked"] is True
    assert finding_entries[0].entry_attrs["status"] == "failed"
