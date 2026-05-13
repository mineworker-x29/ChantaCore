from chanta_core.skills.observation_digest_invocation import ObservationDigestSkillInvocationService


def test_unknown_skill_id_is_blocked():
    service = ObservationDigestSkillInvocationService()

    result = service.invoke_skill(skill_id="skill:unknown", input_payload={})

    assert result.executed is False
    assert result.blocked is True
    assert any(finding.finding_type == "unsupported_skill" for finding in service.last_findings)


def test_missing_required_input_returns_finding():
    service = ObservationDigestSkillInvocationService()

    result = service.invoke_skill(skill_id="skill:agent_trace_observe", input_payload={})

    assert result.blocked is True
    assert any(finding.finding_type == "missing_required_input" for finding in service.last_findings)


def test_invocation_policy_blocks_external_execution_surfaces():
    service = ObservationDigestSkillInvocationService()

    policy = service.create_default_policy()

    assert policy.allow_external_harness_execution is False
    assert policy.allow_script_execution is False
    assert policy.allow_shell is False
    assert policy.allow_network is False
    assert policy.allow_mcp is False
    assert policy.allow_plugin is False
    assert policy.allow_write is False
    assert policy.require_explicit_invocation is True
    assert policy.require_gate is True
    assert policy.require_envelope is True
