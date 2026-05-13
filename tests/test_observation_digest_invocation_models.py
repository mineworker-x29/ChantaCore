from chanta_core.skills.observation_digest_invocation import (
    ObservationDigestInvocationFinding,
    ObservationDigestInvocationPolicy,
    ObservationDigestInvocationResult,
    ObservationDigestSkillRuntimeBinding,
)
from chanta_core.utility.time import utc_now_iso


def test_observation_digest_invocation_models_to_dict():
    binding = ObservationDigestSkillRuntimeBinding(
        binding_id="observation_digest_skill_runtime_binding:test",
        skill_id="skill:agent_trace_observe",
        skill_family="observation",
        handler_name="observe_trace_from_file",
        service_name="ObservationService",
        input_contract_ref="input",
        output_contract_ref="output",
        gate_required=True,
        gate_kind="read_only_explicit_gate",
        envelope_required=True,
        read_only=True,
        enabled=True,
        created_at=utc_now_iso(),
    )
    policy = ObservationDigestInvocationPolicy(
        policy_id="observation_digest_invocation_policy:test",
        policy_name="test",
        allowed_skill_ids=["skill:agent_trace_observe"],
        denied_skill_ids=[],
        allow_file_read=True,
        allow_external_harness_execution=False,
        allow_script_execution=False,
        allow_shell=False,
        allow_network=False,
        allow_mcp=False,
        allow_plugin=False,
        allow_write=False,
        require_explicit_invocation=True,
        require_gate=True,
        require_envelope=True,
        max_input_chars=100000,
        max_records=1000,
        created_at=utc_now_iso(),
    )
    finding = ObservationDigestInvocationFinding(
        finding_id="observation_digest_invocation_finding:test",
        invocation_id="explicit:test",
        skill_id="skill:agent_trace_observe",
        finding_type="missing_required_input",
        status="failed",
        severity="medium",
        message="missing",
        subject_ref="skill:agent_trace_observe",
        created_at=utc_now_iso(),
    )
    result = ObservationDigestInvocationResult(
        result_id="observation_digest_invocation_result:test",
        skill_id="skill:agent_trace_observe",
        status="completed",
        executed=True,
        blocked=False,
        output_ref="observed_agent_run:test",
        output_preview={"status": "completed"},
        envelope_id="execution_envelope:test",
        finding_ids=[],
        created_object_refs=["observed_agent_run:test"],
        created_at=utc_now_iso(),
    )

    assert binding.to_dict()["gate_required"] is True
    assert policy.to_dict()["allow_shell"] is False
    assert finding.to_dict()["finding_type"] == "missing_required_input"
    assert result.to_dict()["executed"] is True
