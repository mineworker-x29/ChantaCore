import json

from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService


def test_traversal_path_is_rejected(tmp_path):
    (tmp_path / "trace.jsonl").write_bytes(
        (json.dumps({"role": "user", "content": "hello"}) + "\n").encode("utf-8"),
    )
    service = ObservationDigestSkillInvocationService()

    result = service.invoke_skill(
        skill_id="skill:agent_trace_observe",
        input_payload={
            "root_path": str(tmp_path),
            "relative_path": "..\\trace.jsonl",
            "source_runtime": "generic",
            "format_hint": "generic_jsonl",
        },
    )

    assert result.executed is False
    assert result.blocked is True
    assert any(finding.finding_type == "path_traversal" for finding in service.last_findings)


def test_outside_root_absolute_path_is_rejected(tmp_path):
    outside = tmp_path.parent / "outside_trace.jsonl"
    outside.write_bytes((json.dumps({"role": "user", "content": "hello"}) + "\n").encode("utf-8"))
    service = ObservationDigestSkillInvocationService()

    result = service.invoke_skill(
        skill_id="skill:agent_trace_observe",
        input_payload={
            "root_path": str(tmp_path),
            "relative_path": str(outside),
            "source_runtime": "generic",
            "format_hint": "generic_jsonl",
        },
    )

    assert result.blocked is True
    assert any(
        finding.finding_type in {"outside_workspace", "workspace_boundary_violation"}
        for finding in service.last_findings
    )
