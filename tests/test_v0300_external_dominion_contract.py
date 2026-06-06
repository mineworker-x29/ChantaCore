from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    DominionAuthorityRequest,
    DominionDecision,
    DominionDecisionType,
    DominionLevel,
    ExternalTargetKind,
    ExternalTargetRecord,
    ExternalTargetStatus,
    is_execution_level,
    is_v030_grantable_level,
    make_v030_contract,
    validate_v030_grant,
)


def test_dominion_level_grantability_is_capped_at_d3() -> None:
    grantable = {
        DominionLevel.D0_OBSERVE,
        DominionLevel.D1_DESCRIBE,
        DominionLevel.D2_PLAN,
        DominionLevel.D3_SIMULATE,
    }
    future_track = {
        DominionLevel.D4_EXECUTE_READ,
        DominionLevel.D5_EXECUTE_WRITE_PROPOSAL,
        DominionLevel.D6_EXECUTE_SANDBOX,
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }

    assert all(is_v030_grantable_level(level) for level in grantable)
    assert all(not is_execution_level(level) for level in grantable)
    assert all(not is_v030_grantable_level(level) for level in future_track)
    assert all(is_execution_level(level) for level in future_track)
    assert DominionLevel.D3_SIMULATE < DominionLevel.D4_EXECUTE_READ


def test_external_target_record_validates_identity_fields() -> None:
    with pytest.raises(ValueError, match="target_id"):
        ExternalTargetRecord("", ExternalTargetKind.EXTERNAL_AGENT_HARNESS, "Hermes-like harness")
    with pytest.raises(ValueError, match="display_name"):
        ExternalTargetRecord("target:1", ExternalTargetKind.EXTERNAL_AGENT_HARNESS, " ")


def test_unknown_target_does_not_become_trusted_or_available() -> None:
    target = ExternalTargetRecord(
        "target:unknown",
        ExternalTargetKind.UNKNOWN,
        "Unknown external target",
        identity_status=ExternalTargetStatus.UNKNOWN,
        trust_status=ExternalTargetStatus.UNKNOWN,
        availability_status=ExternalTargetStatus.UNKNOWN,
        declared_capabilities=["claims external automation"],
    )

    assert target.is_trusted is False
    assert target.is_available is False
    assert target.capabilities_are_permissions is False

    with pytest.raises(ValueError, match="trust"):
        ExternalTargetRecord(
            "target:bad-trust",
            ExternalTargetKind.UNKNOWN,
            "Bad trust",
            trust_status=ExternalTargetStatus.TRUSTED_FOR_OBSERVATION,
        )
    with pytest.raises(ValueError, match="availability"):
        ExternalTargetRecord(
            "target:bad-availability",
            ExternalTargetKind.UNKNOWN,
            "Bad availability",
            availability_status=ExternalTargetStatus.OBSERVED,
        )


def test_authority_request_grants_nothing() -> None:
    request = DominionAuthorityRequest(
        "request:delegate",
        "target:agent",
        DominionLevel.D8_DELEGATE_AGENT,
        requested_capabilities=["delegate coding task"],
        rationale="future-track request only",
        evidence_refs=["evidence:v0.30.0"],
    )

    assert request.requested_level == DominionLevel.D8_DELEGATE_AGENT
    assert request.grants_authority is False


def test_dominion_decision_cannot_grant_d4_or_above() -> None:
    with pytest.raises(ValueError, match="D4"):
        DominionDecision(
            "decision:bad-d4",
            "target:reader",
            DominionLevel.D4_EXECUTE_READ,
            DominionLevel.D4_EXECUTE_READ,
            DominionDecisionType.DRY_RUN_ONLY,
            "D4 cannot be granted in v0.30.0",
            evidence_refs=["evidence:v0.30.0"],
        )

    with pytest.raises(ValueError, match="D4"):
        DominionDecision(
            "decision:bad-d7",
            "target:network-preview",
            DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
            DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
            DominionDecisionType.FUTURE_TRACK,
            "D7 cannot be granted in v0.30.0",
            evidence_refs=["evidence:v0.30.0"],
        )

    with pytest.raises(ValueError, match="D4"):
        DominionDecision(
            "decision:bad-d8",
            "target:delegate",
            DominionLevel.D8_DELEGATE_AGENT,
            DominionLevel.D8_DELEGATE_AGENT,
            DominionDecisionType.FUTURE_TRACK,
            "D8 cannot be granted in v0.30.0",
            evidence_refs=["evidence:v0.30.0"],
        )

    with pytest.raises(ValueError, match="D4"):
        DominionDecision(
            "decision:bad-d9",
            "target:gateway",
            DominionLevel.D9_GATEWAY_CONTROL,
            DominionLevel.D9_GATEWAY_CONTROL,
            DominionDecisionType.FUTURE_TRACK,
            "D9 cannot be granted in v0.30.0",
            evidence_refs=["evidence:v0.30.0"],
        )


def test_d4_plus_requests_can_only_receive_d3_or_lower_non_execution_decisions() -> None:
    decision = DominionDecision(
        "decision:bounded-simulation",
        "target:agent",
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D3_SIMULATE,
        DominionDecisionType.FUTURE_TRACK,
        "Future delegation request can only be represented as bounded simulation.",
        evidence_refs=["evidence:v0.30.0"],
        approval_required=True,
    )

    assert validate_v030_grant(decision) is True
    assert decision.granted_level == DominionLevel.D3_SIMULATE
    assert decision.approval_required is True
    assert decision.approval_granted is False


def test_denied_or_deferred_decisions_do_not_grant_authority() -> None:
    denied = DominionDecision(
        "decision:deny-network-preview",
        "target:gateway",
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        None,
        DominionDecisionType.DENY,
        "Network preview execution is future-track.",
        evidence_refs=["evidence:v0.30.0"],
        approval_required=True,
    )
    deferred = DominionDecision(
        "decision:defer-gateway",
        "target:gateway",
        DominionLevel.D9_GATEWAY_CONTROL,
        None,
        DominionDecisionType.DEFER,
        "Gateway control requires later boundaries.",
        evidence_refs=["evidence:v0.30.0"],
    )

    assert denied.granted_level is None
    assert denied.approval_required is True
    assert denied.approval_granted is False
    assert validate_v030_grant(denied) is True
    assert deferred.granted_level is None
    assert validate_v030_grant(deferred) is True


def test_make_v030_contract_keeps_all_runtime_readiness_false_and_inherits_v029_gates() -> None:
    contract = make_v030_contract()

    assert contract.version == "v0.30.0"
    assert contract.max_grantable_level == DominionLevel.D3_SIMULATE
    assert contract.provider_invocation_runtime_ready is False
    assert contract.limited_preview_execution_ready_now is False
    assert contract.live_adapter_runtime_ready is False
    assert contract.external_agent_dominion_runtime_ready is False
    assert contract.network_access_ready is False
    assert contract.credential_access_ready is False
    assert contract.command_execution_ready is False
    assert contract.rpa_runtime_control_ready is False
    assert contract.gateway_control_ready is False
    assert all(value is False for value in contract.prohibited_runtime_flags.values())
    assert len(contract.inherited_gate_refs) == 10
    assert any("v0.29.0" in ref for ref in contract.inherited_gate_refs)
    assert any("v0.29.9" in ref for ref in contract.inherited_gate_refs)
    assert "v0.30.1" in contract.validity_horizon
