from chanta_core.observation_digest import DigestionService, ObservationService
from chanta_core.skills.execution_gate import SkillExecutionGateService


def test_observation_source_rejects_traversal_outside_root(tmp_path):
    service = ObservationService()

    source = service.inspect_observation_source(
        root_path=str(tmp_path),
        relative_path="../outside.jsonl",
        source_runtime="dummy_runtime",
        format_hint="generic_jsonl",
    )

    assert source.source_attrs["status"] == "blocked"
    assert service.last_findings
    assert service.last_findings[0].finding_type in {"path_traversal", "outside_workspace"}


def test_external_skill_source_rejects_traversal_outside_root(tmp_path):
    service = DigestionService()

    descriptor = service.inspect_external_skill_source(
        root_path=str(tmp_path),
        relative_path="../outside",
        vendor_hint="dummy_vendor",
    )

    assert descriptor.descriptor_attrs["status"] == "blocked"
    assert service.last_findings
    assert service.last_findings[0].finding_type in {"path_traversal", "outside_workspace"}


def test_read_only_gate_blocks_unsafe_path_and_missing_root(tmp_path):
    gate = SkillExecutionGateService()

    traversal_result = gate.gate_explicit_invocation(
        skill_id="skill:external_skill_source_inspect",
        input_payload={"root_path": str(tmp_path), "relative_path": "../outside"},
    )
    missing_root_result = gate.gate_explicit_invocation(
        skill_id="skill:agent_observation_source_inspect",
        input_payload={"relative_path": "trace.jsonl"},
    )

    assert traversal_result.blocked is True
    assert missing_root_result.blocked is True
