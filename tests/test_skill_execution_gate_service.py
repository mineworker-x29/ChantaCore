from chanta_core.skills.execution_gate import SkillExecutionGateService


class InvocationProbe:
    def __init__(self) -> None:
        self.calls = 0

    def invoke_explicit_skill(self, **_) -> object:
        self.calls += 1
        return type("Result", (), {"result_id": "explicit_skill_invocation_result:probe", "status": "completed"})()


def test_default_policy_contains_read_only_workspace_skills() -> None:
    policy = SkillExecutionGateService().create_default_policy()

    assert "skill:list_workspace_files" in policy.supported_skill_ids
    assert "skill:read_workspace_text_file" in policy.supported_skill_ids
    assert "skill:summarize_workspace_markdown" in policy.supported_skill_ids
    assert "shell" in policy.denied_skill_categories


def test_read_only_workspace_skill_allowed_by_default_with_permission_warning(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "example.txt").write_bytes(b"public-safe text")
    service = SkillExecutionGateService()
    request = service.create_gate_request(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "docs/example.txt"},
        invocation_mode="test",
    )

    decision = service.evaluate_gate(request=request)

    assert decision.decision == "allow"
    assert decision.can_execute is True
    assert any(finding.finding_type == "permission_context_absent" for finding in service.last_findings)
    assert any(finding.status == "warning" for finding in service.last_findings)


def test_requires_permission_policy_needs_review_without_permission(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "example.txt").write_bytes(b"public-safe text")
    service = SkillExecutionGateService()
    policy = service.create_default_policy(
        requires_permission_for_read_only=True,
        allow_without_permission_for_read_only=False,
    )
    request = service.create_gate_request(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "docs/example.txt"},
        invocation_mode="test",
    )

    decision = service.evaluate_gate(request=request, policy=policy)

    assert decision.decision == "needs_review"
    assert decision.can_execute is False
    assert decision.requires_permission is True


def test_permission_and_session_permission_denial_block_execution(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "example.txt").write_bytes(b"public-safe text")
    probe = InvocationProbe()
    service = SkillExecutionGateService(explicit_skill_invocation_service=probe)

    permission_result = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "docs/example.txt"},
        permission_decision_id="permission_decision:deny",
        request_attrs={"permission_decision": "deny"},
    )
    session_result = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "docs/example.txt"},
        session_permission_resolution_id="session_permission_resolution:deny",
        request_attrs={"session_permission_decision": "deny"},
    )

    assert permission_result.blocked is True
    assert session_result.blocked is True
    assert probe.calls == 0


def test_denied_gate_does_not_call_explicit_invocation() -> None:
    probe = InvocationProbe()
    service = SkillExecutionGateService(explicit_skill_invocation_service=probe)

    result = service.gate_explicit_invocation(
        skill_id="skill:write_file",
        input_payload={"root_path": "<ROOT>", "relative_path": "docs/example.txt"},
    )

    assert result.blocked is True
    assert result.executed is False
    assert probe.calls == 0


def test_allowed_gate_calls_explicit_invocation(tmp_path) -> None:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "example.txt").write_bytes(b"public-safe text")
    probe = InvocationProbe()
    service = SkillExecutionGateService(explicit_skill_invocation_service=probe)

    result = service.gate_explicit_invocation(
        skill_id="skill:read_workspace_text_file",
        input_payload={"root_path": str(tmp_path), "relative_path": "docs/example.txt"},
    )

    assert result.executed is True
    assert result.blocked is False
    assert result.explicit_invocation_result_id == "explicit_skill_invocation_result:probe"
    assert probe.calls == 1
