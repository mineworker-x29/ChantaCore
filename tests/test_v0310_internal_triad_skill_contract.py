from __future__ import annotations

import inspect

import pytest

from chanta_core.external_dominion import DominionLevel
from chanta_core.internal_triad import (
    DIGESTION_OUTPUT_ARTIFACT_KINDS,
    DOMINION_OUTPUT_ARTIFACT_KINDS,
    OBSERVATION_OUTPUT_ARTIFACT_KINDS,
    V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    DigestionSkillContract,
    DominionSkillContract,
    ObservationSkillContract,
    TriadSkillBoundaryPolicy,
    TriadSkillContract,
    TriadSkillExecutionMode,
    TriadSkillInputEnvelope,
    TriadSkillKind,
    TriadSkillNoExecutionGuarantee,
    TriadSkillResultEnvelope,
    TriadSkillStatus,
    V0310ReadinessReport,
    build_default_triad_boundary_policy,
    build_digestion_skill_contract,
    build_dominion_skill_contract,
    build_observation_skill_contract,
    build_triad_input_envelope,
    build_triad_no_execution_guarantee,
    build_triad_result_envelope,
    build_triad_skill_contract_set,
    build_v0310_readiness_report,
    normalize_triad_execution_mode,
    normalize_triad_skill_kind,
    normalize_triad_skill_status,
    triad_boundary_preserves_no_execution,
    triad_contract_preserves_no_execution,
    triad_contract_set_preserves_no_execution,
    triad_execution_mode_permits_execution,
    triad_readiness_report_is_not_runtime_ready,
    triad_skill_kind_implies_execution,
)
from chanta_core.internal_triad import boundaries, contracts, envelopes


REQUIRED_ACTIONS = {
    "external_execution",
    "internal_tool_execution",
    "provider_invocation",
    "network",
    "credential",
    "command",
    "browser",
    "rpa",
    "gateway",
    "packet_send",
    "rollback",
    "retry",
    "active_registry_mutation",
    "active_memory_mutation",
}


def test_triad_skill_kind_status_and_execution_mode_values_are_conservative() -> None:
    assert {kind.value for kind in TriadSkillKind} == {"observation", "digestion", "dominion", "unknown"}
    assert normalize_triad_skill_kind("observation") is TriadSkillKind.OBSERVATION
    assert normalize_triad_skill_kind("digestion") is TriadSkillKind.DIGESTION
    assert normalize_triad_skill_kind("dominion") is TriadSkillKind.DOMINION
    assert normalize_triad_skill_kind("unknown") is TriadSkillKind.UNKNOWN
    assert triad_skill_kind_implies_execution(TriadSkillKind.UNKNOWN) is False

    assert {status.value for status in TriadSkillStatus} == {
        "unknown",
        "contract_defined",
        "input_ready",
        "result_ready",
        "blocked",
        "deferred",
        "future_track",
        "no_op",
    }
    assert normalize_triad_skill_status("contract_defined") is TriadSkillStatus.CONTRACT_DEFINED
    assert normalize_triad_skill_status("input_ready") is TriadSkillStatus.INPUT_READY
    assert normalize_triad_skill_status("result_ready") is TriadSkillStatus.RESULT_READY

    assert {mode.value for mode in TriadSkillExecutionMode} == {
        "contract_only",
        "planning_only",
        "report_only",
        "candidate_only",
        "governance_only",
        "future_runtime",
        "unknown",
    }
    assert normalize_triad_execution_mode("future_runtime") is TriadSkillExecutionMode.FUTURE_RUNTIME
    assert triad_execution_mode_permits_execution(TriadSkillExecutionMode.FUTURE_RUNTIME) is False


def test_boundary_policy_creation_and_no_execution_defaults() -> None:
    policy = build_default_triad_boundary_policy(TriadSkillKind.OBSERVATION)

    assert policy.boundary_policy_id
    assert policy.skill_kind == TriadSkillKind.OBSERVATION
    assert REQUIRED_ACTIONS.issubset(set(policy.prohibited_runtime_actions))
    assert policy.requires_evidence_refs is True
    assert policy.requires_ocel_trace_plan is True
    assert policy.no_execution_guarantee is True
    assert policy.no_external_contact_guarantee is True
    assert policy.no_registry_mutation_guarantee is True
    assert policy.no_memory_mutation_guarantee is True
    assert policy.max_dominion_level == DominionLevel.D3_SIMULATE
    assert policy.grants_permission is False
    assert triad_boundary_preserves_no_execution(policy) is True

    with pytest.raises(ValueError, match="boundary_policy_id"):
        TriadSkillBoundaryPolicy(boundary_policy_id="", skill_kind=TriadSkillKind.OBSERVATION)
    with pytest.raises(ValueError, match="D3_SIMULATE"):
        TriadSkillBoundaryPolicy(
            boundary_policy_id="policy:bad",
            skill_kind=TriadSkillKind.DOMINION,
            max_dominion_level=DominionLevel.D4_EXECUTE_READ,
        )
    with pytest.raises(ValueError, match="no_execution_guarantee"):
        TriadSkillBoundaryPolicy(
            boundary_policy_id="policy:bad",
            skill_kind=TriadSkillKind.OBSERVATION,
            no_execution_guarantee=False,
        )


def test_boundary_policy_cannot_allow_runtime_surfaces() -> None:
    for action in REQUIRED_ACTIONS:
        prohibited = [item for item in V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS if item != action]
        with pytest.raises(ValueError, match="missing required"):
            TriadSkillBoundaryPolicy(
                boundary_policy_id=f"policy:missing:{action}",
                skill_kind=TriadSkillKind.UNKNOWN,
                prohibited_runtime_actions=prohibited,
            )


def test_observation_skill_contract_is_not_external_scan() -> None:
    contract = build_observation_skill_contract()

    assert isinstance(contract, ObservationSkillContract)
    assert contract.skill_kind == TriadSkillKind.OBSERVATION
    assert set(OBSERVATION_OUTPUT_ARTIFACT_KINDS).issubset(set(contract.boundary_policy.allowed_output_artifact_kinds))
    assert "live_external_scan" in contract.boundary_policy.prohibited_runtime_actions
    assert "source_ref_fetch" in contract.boundary_policy.prohibited_runtime_actions
    assert contract.ready_for_execution is False
    assert contract.ready_for_skill_activation is False
    assert contract.active_skill_registration is False
    assert triad_contract_preserves_no_execution(contract) is True


def test_digestion_skill_contract_is_not_active_internalization() -> None:
    contract = build_digestion_skill_contract()

    assert isinstance(contract, DigestionSkillContract)
    assert contract.skill_kind == TriadSkillKind.DIGESTION
    assert set(DIGESTION_OUTPUT_ARTIFACT_KINDS).issubset(set(contract.boundary_policy.allowed_output_artifact_kinds))
    for action in (
        "active_skill_registry_mutation",
        "tool_registration",
        "mission_installation",
        "policy_activation",
        "memory_writer_activation",
    ):
        assert action in contract.boundary_policy.prohibited_runtime_actions
    assert contract.ready_for_execution is False
    assert contract.ready_for_skill_activation is False

    with pytest.raises(ValueError, match="metadata"):
        DigestionSkillContract(
            **{**contract.__dict__, "metadata": {"active_skill_registration": True}}
        )


def test_dominion_skill_contract_is_not_runtime_control_and_does_not_grant_d4_d9() -> None:
    contract = build_dominion_skill_contract()

    assert isinstance(contract, DominionSkillContract)
    assert contract.skill_kind == TriadSkillKind.DOMINION
    assert set(DOMINION_OUTPUT_ARTIFACT_KINDS).issubset(set(contract.boundary_policy.allowed_output_artifact_kinds))
    assert contract.boundary_policy.max_dominion_level <= DominionLevel.D3_SIMULATE
    for action in ("external_runtime_control", "provider_invocation", "network", "credential", "command", "browser", "rpa", "gateway", "packet_send"):
        assert action in contract.boundary_policy.prohibited_runtime_actions
    assert contract.ready_for_execution is False
    assert contract.ready_for_skill_activation is False

    with pytest.raises(ValueError, match="D3_SIMULATE"):
        build_default_triad_boundary_policy(TriadSkillKind.DOMINION).__class__(
            boundary_policy_id="policy:bad",
            skill_kind=TriadSkillKind.DOMINION,
            max_dominion_level=DominionLevel.D9_GATEWAY_CONTROL,
        )


def test_triad_skill_contract_rejects_future_runtime_and_execution_activation_flags() -> None:
    policy = build_default_triad_boundary_policy(TriadSkillKind.OBSERVATION)
    base = {
        "contract_id": "contract:observation",
        "skill_id": "skill:observation",
        "skill_kind": TriadSkillKind.OBSERVATION,
        "name": "Observation",
        "purpose": "Define observation contract only.",
        "execution_mode": TriadSkillExecutionMode.CONTRACT_ONLY,
        "input_contract_refs": [],
        "output_contract_refs": [],
        "boundary_policy": policy,
    }

    contract = TriadSkillContract(**base)
    assert contract.ready_for_execution is False
    assert contract.ready_for_skill_activation is False

    with pytest.raises(ValueError, match="contract_id"):
        TriadSkillContract(**{**base, "contract_id": ""})
    with pytest.raises(ValueError, match="skill_id"):
        TriadSkillContract(**{**base, "skill_id": ""})
    with pytest.raises(ValueError, match="name"):
        TriadSkillContract(**{**base, "name": ""})
    with pytest.raises(ValueError, match="purpose"):
        TriadSkillContract(**{**base, "purpose": ""})
    with pytest.raises(ValueError, match="future_runtime"):
        TriadSkillContract(**{**base, "execution_mode": TriadSkillExecutionMode.FUTURE_RUNTIME})
    with pytest.raises(ValueError, match="ready_for_execution"):
        TriadSkillContract(**{**base, "ready_for_execution": True})
    with pytest.raises(ValueError, match="ready_for_skill_activation"):
        TriadSkillContract(**{**base, "ready_for_skill_activation": True})


def test_input_envelope_is_not_execution_request() -> None:
    envelope = build_triad_input_envelope(
        input_id="input:v0.31.0",
        source_version="v0.30.9",
        requested_skill_kind=TriadSkillKind.OBSERVATION,
        task_summary="Create observation contract inputs from v0.30.9 handoff refs.",
        source_artifact_refs=["handoff:v0.30.9"],
        evidence_refs=["evidence:handoff"],
    )

    assert isinstance(envelope, TriadSkillInputEnvelope)
    assert envelope.is_execution_request is False
    assert REQUIRED_ACTIONS.issubset(set(envelope.prohibited_runtime_actions))

    with pytest.raises(ValueError, match="input_id"):
        build_triad_input_envelope("", "v0.30.9", TriadSkillKind.OBSERVATION, "summary")
    with pytest.raises(ValueError, match="source_version"):
        build_triad_input_envelope("input:bad", "", TriadSkillKind.OBSERVATION, "summary")
    with pytest.raises(ValueError, match="task_summary"):
        build_triad_input_envelope("input:bad", "v0.30.9", TriadSkillKind.OBSERVATION, "")
    with pytest.raises(TypeError, match="source_artifact_refs"):
        TriadSkillInputEnvelope(
            input_id="input:bad",
            source_version="v0.30.9",
            requested_skill_kind=TriadSkillKind.OBSERVATION,
            source_artifact_refs="not-list",
            source_target_refs=[],
            source_capability_refs=[],
            source_candidate_refs=[],
            source_report_refs=[],
            task_summary="summary",
        )
    with pytest.raises(ValueError, match="execution request"):
        build_triad_input_envelope(
            "input:bad",
            "v0.30.9",
            TriadSkillKind.OBSERVATION,
            "summary",
            metadata={"execution_request": True},
        )


def test_result_envelope_is_not_active_artifact_registration() -> None:
    envelope = build_triad_result_envelope(
        result_id="result:v0.31.0",
        input_id="input:v0.31.0",
        skill_id="skill:observation",
        skill_kind=TriadSkillKind.OBSERVATION,
        status=TriadSkillStatus.RESULT_READY,
        produced_artifact_refs=["observation_report:contract"],
        ready_for_next_stage=True,
    )

    assert isinstance(envelope, TriadSkillResultEnvelope)
    assert envelope.ready_for_execution is False
    assert envelope.ready_for_skill_activation is False
    assert envelope.active_artifact_registration is False

    no_op = build_triad_result_envelope(
        result_id="result:no-op",
        input_id="input:v0.31.0",
        skill_id="skill:observation",
        skill_kind=TriadSkillKind.OBSERVATION,
        status=TriadSkillStatus.NO_OP,
        no_op_reason="No operation is a valid contract outcome.",
    )
    assert no_op.no_op_reason

    with pytest.raises(ValueError, match="result_id"):
        build_triad_result_envelope("", "input", "skill", TriadSkillKind.OBSERVATION, TriadSkillStatus.NO_OP)
    with pytest.raises(ValueError, match="input_id"):
        build_triad_result_envelope("result", "", "skill", TriadSkillKind.OBSERVATION, TriadSkillStatus.NO_OP)
    with pytest.raises(ValueError, match="skill_id"):
        build_triad_result_envelope("result", "input", "", TriadSkillKind.OBSERVATION, TriadSkillStatus.NO_OP)
    with pytest.raises(ValueError, match="ready_for_execution"):
        TriadSkillResultEnvelope(
            result_id="result:bad",
            input_id="input",
            skill_id="skill",
            skill_kind=TriadSkillKind.OBSERVATION,
            status=TriadSkillStatus.RESULT_READY,
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="ready_for_skill_activation"):
        TriadSkillResultEnvelope(
            result_id="result:bad",
            input_id="input",
            skill_id="skill",
            skill_kind=TriadSkillKind.OBSERVATION,
            status=TriadSkillStatus.RESULT_READY,
            ready_for_skill_activation=True,
        )
    with pytest.raises(ValueError, match="active artifact registration"):
        build_triad_result_envelope(
            "result:bad",
            "input",
            "skill",
            TriadSkillKind.OBSERVATION,
            TriadSkillStatus.RESULT_READY,
            metadata={"active_artifact_registration": True},
        )


def test_no_execution_guarantee_requires_all_no_fields_true() -> None:
    guarantee = build_triad_no_execution_guarantee(TriadSkillKind.DOMINION)

    assert isinstance(guarantee, TriadSkillNoExecutionGuarantee)
    assert guarantee.no_external_execution is True
    assert guarantee.no_internal_tool_execution is True
    assert guarantee.no_network_access is True
    assert guarantee.no_credential_access is True
    assert guarantee.no_command_execution is True
    assert guarantee.no_provider_invocation is True
    assert guarantee.no_browser_automation is True
    assert guarantee.no_rpa_control is True
    assert guarantee.no_gateway_control is True
    assert guarantee.no_packet_send is True
    assert guarantee.no_registry_mutation is True
    assert guarantee.no_memory_mutation is True
    assert guarantee.no_rollback_execution is True
    assert guarantee.no_retry_execution is True
    assert guarantee.runtime_enforcement is False

    with pytest.raises(ValueError, match="guarantee_id"):
        TriadSkillNoExecutionGuarantee(guarantee_id="", skill_kind=TriadSkillKind.OBSERVATION)
    with pytest.raises(ValueError, match="no_network_access"):
        TriadSkillNoExecutionGuarantee(
            guarantee_id="guarantee:bad",
            skill_kind=TriadSkillKind.OBSERVATION,
            no_network_access=False,
        )


def test_contract_set_and_readiness_report_are_v0311_handoff_only() -> None:
    contract_set = build_triad_skill_contract_set()
    report = build_v0310_readiness_report(contract_set)

    assert contract_set.observation_contract.skill_kind == TriadSkillKind.OBSERVATION
    assert contract_set.digestion_contract.skill_kind == TriadSkillKind.DIGESTION
    assert contract_set.dominion_contract.skill_kind == TriadSkillKind.DOMINION
    assert contract_set.ready_for_v0311_observation_skill_foundation is True
    assert contract_set.ready_for_execution is False
    assert contract_set.ready_for_skill_activation is False
    assert triad_contract_set_preserves_no_execution(contract_set) is True

    assert isinstance(report, V0310ReadinessReport)
    assert "v0.31.0" in report.version
    assert report.summary
    assert report.ready_for_v0311_observation_skill_foundation is True
    assert report.ready_for_execution is False
    assert report.ready_for_skill_activation is False
    assert {
        "external_execution",
        "internal_tool_execution",
        "provider_invocation",
        "network",
        "credential",
        "command",
        "browser",
        "rpa",
        "gateway",
        "packet_send",
        "registry_mutation",
        "memory_mutation",
        "rollback",
        "retry",
    }.issubset(set(report.prohibited_until_later_gate))
    assert report.runtime_enablement is False
    assert triad_readiness_report_is_not_runtime_ready(report) is True

    with pytest.raises(ValueError, match="v0.31.0"):
        contract_set.__class__(**{**contract_set.__dict__, "version": "v0.31.1"})
    with pytest.raises(ValueError, match="ready_for_execution"):
        contract_set.__class__(**{**contract_set.__dict__, "ready_for_execution": True})
    with pytest.raises(ValueError, match="ready_for_skill_activation"):
        contract_set.__class__(**{**contract_set.__dict__, "ready_for_skill_activation": True})
    with pytest.raises(ValueError, match="ready_for_execution"):
        V0310ReadinessReport(
            report_id="report:bad",
            version="v0.31.0",
            contract_set_id=contract_set.contract_set_id,
            summary="summary",
            ready_for_v0311_observation_skill_foundation=True,
            ready_for_execution=True,
        )
    with pytest.raises(ValueError, match="ready_for_skill_activation"):
        V0310ReadinessReport(
            report_id="report:bad",
            version="v0.31.0",
            contract_set_id=contract_set.contract_set_id,
            summary="summary",
            ready_for_v0311_observation_skill_foundation=True,
            ready_for_skill_activation=True,
        )


def test_helpers_are_pure_conservative_contract_builders() -> None:
    helpers = [
        build_default_triad_boundary_policy,
        build_observation_skill_contract,
        build_digestion_skill_contract,
        build_dominion_skill_contract,
        build_triad_no_execution_guarantee,
        build_triad_skill_contract_set,
        build_triad_input_envelope,
        build_triad_result_envelope,
        build_v0310_readiness_report,
        triad_boundary_preserves_no_execution,
        triad_contract_preserves_no_execution,
        triad_contract_set_preserves_no_execution,
        triad_readiness_report_is_not_runtime_ready,
    ]

    for helper in helpers:
        source = inspect.getsource(helper)
        assert "ready_for_execution=True" not in source
        assert "ready_for_skill_activation=True" not in source
        assert "subprocess" not in source
        assert "os.system" not in source
        assert "shell=True" not in source
        assert "requests." not in source
        assert "httpx." not in source
        assert "socket." not in source

    implementation_source = "\n".join(
        inspect.getsource(module) for module in (boundaries, contracts, envelopes)
    )
    assert "subprocess" not in implementation_source
    assert "os.system" not in implementation_source
    assert "shell=True" not in implementation_source
    assert "requests." not in implementation_source
    assert "httpx." not in implementation_source
    assert "urllib." not in implementation_source
    assert "aiohttp." not in implementation_source
    assert "socket." not in implementation_source

