from chanta_core.skills.observation_digest_conformance import ObservationDigestConformanceService


def test_conformance_policy_does_not_enable_forbidden_surfaces():
    service = ObservationDigestConformanceService()

    policy = service.create_default_policy()

    assert policy.deny_external_execution is True
    assert policy.deny_shell_network_write is True
    assert policy.deny_memory_persona_overlay_mutation is True
    assert policy.policy_attrs["adds_execution_capability"] is False


def test_boundary_checks_detect_forbidden_execution_flags_if_simulated():
    service = ObservationDigestConformanceService()

    finding = service.record_finding(
        skill_id="skill:agent_trace_observe",
        check_id=None,
        finding_type="external_execution_boundary",
        status="failed",
        severity="high",
        message="simulated forbidden external execution flag",
    )

    assert finding.finding_type == "external_execution_boundary"
    assert finding.severity == "high"
