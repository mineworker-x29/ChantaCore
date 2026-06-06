from __future__ import annotations

import pytest

from chanta_core.external_dominion import (
    DominionDecision,
    DominionLevel,
    ExternalAvailabilityStatus,
    ExternalBoundarySurface,
    ExternalIdentityProfile,
    ExternalIdentityStatus,
    ExternalTargetInventory,
    ExternalTargetKind,
    ExternalTargetRecord,
    ExternalTargetRegistrationRequest,
    ExternalTrustBoundaryProfile,
    ExternalTrustBoundaryStatus,
    can_enter_digestion_flow,
    can_enter_dominion_flow,
    can_enter_observation_flow,
    default_trust_boundary_for_target,
    infer_availability_status_from_request,
    infer_identity_status_from_request,
    make_v030_contract,
)


def _request(**overrides) -> ExternalTargetRegistrationRequest:
    data = {
        "target_id": "target:opencode",
        "target_kind": ExternalTargetKind.EXTERNAL_CODING_HARNESS,
        "display_name": "OpenCode reference",
        "source_ref": "docs:opencode",
        "claimed_vendor": "OpenCode",
        "claimed_version": None,
        "declared_capabilities": ["coding assistance"],
        "risk_tags": ["external_coding_harness"],
        "evidence_refs": ["evidence:public-doc"],
        "metadata": {"homepage": "not evidence unless listed in evidence_refs"},
    }
    data.update(overrides)
    return ExternalTargetRegistrationRequest(**data)


def test_registering_valid_external_target_returns_inventory_record() -> None:
    inventory = ExternalTargetInventory()
    request = _request()
    record = inventory.register(request)

    assert inventory.has("target:opencode") is True
    assert inventory.get("target:opencode") == record
    assert inventory.list_records() == [record]
    assert record.inventory_id == "external_target_inventory_record:target:opencode"
    assert record.target.target_id == record.identity.target_id == record.trust_boundary.target_id
    assert record.identity.identity_status == ExternalIdentityStatus.EVIDENCE_LINKED
    assert record.availability_status == ExternalAvailabilityStatus.CANDIDATE
    assert record.trust_boundary.trust_status == ExternalTrustBoundaryStatus.OBSERVATION_ONLY
    assert record.trust_boundary.max_observable_level == DominionLevel.D1_DESCRIBE
    assert record.target.capabilities_are_permissions is False
    assert record.inventory_is_execution_ready is False
    assert record.evidence_refs_are_runtime_proof is False
    assert record.availability_implies_trust is False
    assert can_enter_observation_flow(record) is True
    assert can_enter_digestion_flow(record) is True
    assert can_enter_dominion_flow(record) is True


def test_blank_target_id_and_display_name_are_rejected() -> None:
    with pytest.raises(ValueError, match="target_id"):
        _request(target_id="")
    with pytest.raises(ValueError, match="display_name"):
        _request(display_name=" ")


def test_duplicate_target_id_is_rejected() -> None:
    inventory = ExternalTargetInventory()
    inventory.register(_request())

    with pytest.raises(ValueError, match="duplicate"):
        inventory.register(_request())


def test_unknown_target_defaults_to_not_trusted_and_not_available() -> None:
    inventory = ExternalTargetInventory()
    record = inventory.register(
        _request(
            target_id="target:unknown",
            target_kind=ExternalTargetKind.UNKNOWN,
            display_name="Unknown target",
            source_ref=None,
            evidence_refs=[],
            declared_capabilities=["claims automation"],
        )
    )

    assert record.target.is_trusted is False
    assert record.target.is_available is False
    assert record.identity.identity_status == ExternalIdentityStatus.CLAIMED
    assert record.availability_status == ExternalAvailabilityStatus.UNKNOWN
    assert record.trust_boundary.trust_status == ExternalTrustBoundaryStatus.UNTRUSTED
    assert record.trust_boundary.max_observable_level == DominionLevel.D0_OBSERVE
    assert can_enter_observation_flow(record) is False
    assert can_enter_digestion_flow(record) is False
    assert can_enter_dominion_flow(record) is False


def test_claimed_identity_is_not_verified_identity_or_trust() -> None:
    profile = ExternalIdentityProfile(
        "target:claimed",
        claimed_name="Claimed Agent",
        identity_status=ExternalIdentityStatus.CLAIMED,
    )

    assert profile.is_claim_verified is False
    assert profile.is_trusted is False


def test_reference_verified_requires_evidence_refs_and_conflict_requires_notes() -> None:
    with pytest.raises(ValueError, match="evidence_refs"):
        ExternalIdentityProfile("target:verified", identity_status=ExternalIdentityStatus.REFERENCE_VERIFIED)

    verified = ExternalIdentityProfile(
        "target:verified",
        evidence_refs=["evidence:internal-reference"],
        identity_status=ExternalIdentityStatus.REFERENCE_VERIFIED,
    )
    assert verified.is_claim_verified is True
    assert verified.is_trusted is False

    with pytest.raises(ValueError, match="conflict_notes"):
        ExternalIdentityProfile("target:conflict", identity_status=ExternalIdentityStatus.CONFLICT_DETECTED)


def test_trust_boundary_cannot_exceed_d3_and_blocked_uses_safest_ceiling() -> None:
    with pytest.raises(ValueError, match="D3_SIMULATE"):
        ExternalTrustBoundaryProfile(
            "target:network",
            trust_status=ExternalTrustBoundaryStatus.DRY_RUN_CANDIDATE,
            max_observable_level=DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        )

    with pytest.raises(ValueError, match="D0_OBSERVE"):
        ExternalTrustBoundaryProfile(
            "target:blocked",
            trust_status=ExternalTrustBoundaryStatus.BLOCKED,
            max_observable_level=DominionLevel.D1_DESCRIBE,
        )

    blocked = ExternalTrustBoundaryProfile(
        "target:blocked",
        trust_status=ExternalTrustBoundaryStatus.BLOCKED,
        max_observable_level=DominionLevel.D0_OBSERVE,
    )
    assert blocked.max_observable_level == DominionLevel.D0_OBSERVE
    assert blocked.grants_permission is False


def test_dangerous_boundaries_are_prohibited_by_default_for_unknown_targets() -> None:
    target = ExternalTargetRecord("target:unknown", ExternalTargetKind.UNKNOWN, "Unknown target")
    boundary = default_trust_boundary_for_target(target)

    assert boundary.trust_status == ExternalTrustBoundaryStatus.UNTRUSTED
    assert {
        ExternalBoundarySurface.CREDENTIAL_BOUNDARY,
        ExternalBoundarySurface.NETWORK_BOUNDARY,
        ExternalBoundarySurface.COMMAND_BOUNDARY,
        ExternalBoundarySurface.BROWSER_BOUNDARY,
        ExternalBoundarySurface.RPA_BOUNDARY,
        ExternalBoundarySurface.GATEWAY_BOUNDARY,
    } <= set(boundary.prohibited_boundary_surfaces)
    assert boundary.grants_permission is False

    with pytest.raises(ValueError, match="dangerous"):
        ExternalTrustBoundaryProfile(
            "target:unsafe",
            trust_status=ExternalTrustBoundaryStatus.UNKNOWN,
            prohibited_boundary_surfaces=[],
        )


def test_registration_does_not_create_decision_or_grant_authority() -> None:
    record = ExternalTargetInventory().register(_request())

    assert not isinstance(record, DominionDecision)
    assert not hasattr(record, "granted_level")
    assert record.trust_boundary.grants_permission is False
    assert record.trust_boundary.dry_run_executes is False
    assert record.target.capabilities_are_permissions is False
    assert record.availability_status == ExternalAvailabilityStatus.CANDIDATE
    assert record.inventory_is_execution_ready is False


def test_inference_helpers_are_conservative_and_metadata_is_not_evidence() -> None:
    source_only = _request(
        target_id="target:source-only",
        source_ref="docs:source",
        evidence_refs=[],
        metadata={"evidence": "metadata is not an evidence_ref"},
    )
    no_source = _request(target_id="target:local", source_ref=None, evidence_refs=[])

    assert infer_identity_status_from_request(source_only) == ExternalIdentityStatus.SOURCE_DESCRIBED
    assert infer_availability_status_from_request(source_only) == ExternalAvailabilityStatus.DOCUMENTATION_ONLY
    assert infer_identity_status_from_request(no_source) == ExternalIdentityStatus.CLAIMED
    assert infer_availability_status_from_request(no_source) == ExternalAvailabilityStatus.LOCAL_REFERENCE_ONLY


def test_flow_helpers_block_conflicted_blocked_and_future_track_records() -> None:
    request = _request(target_id="target:flow")
    record = ExternalTargetInventory().register(request)
    blocked_identity = ExternalIdentityProfile(
        "target:flow",
        identity_status=ExternalIdentityStatus.BLOCKED,
    )
    blocked_boundary = ExternalTrustBoundaryProfile(
        "target:flow",
        trust_status=ExternalTrustBoundaryStatus.BLOCKED,
        max_observable_level=DominionLevel.D0_OBSERVE,
    )
    blocked_record = type(record)(
        record.inventory_id,
        record.target,
        blocked_identity,
        blocked_boundary,
        ExternalAvailabilityStatus.BLOCKED,
        "blocked",
    )

    assert can_enter_observation_flow(blocked_record) is False
    assert can_enter_digestion_flow(blocked_record) is False
    assert can_enter_dominion_flow(blocked_record) is False


def test_d7_d8_d9_cannot_be_inferred_from_inventory() -> None:
    record = ExternalTargetInventory().register(
        _request(
            target_id="target:gateway",
            target_kind=ExternalTargetKind.EXTERNAL_GATEWAY,
            risk_tags=["network", "gateway", "delegation"],
            declared_capabilities=["network preview", "delegate agent", "gateway control"],
        )
    )

    assert record.trust_boundary.max_observable_level <= DominionLevel.D3_SIMULATE
    assert record.trust_boundary.max_observable_level not in {
        DominionLevel.D7_EXECUTE_NETWORK_PREVIEW,
        DominionLevel.D8_DELEGATE_AGENT,
        DominionLevel.D9_GATEWAY_CONTROL,
    }
    assert make_v030_contract().max_grantable_level == DominionLevel.D3_SIMULATE
