from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel
from chanta_core.external_dominion.identity import (
    ExternalIdentityProfile,
    ExternalIdentityStatus,
    normalize_identity_status,
)
from chanta_core.external_dominion.targets import (
    ExternalTargetKind,
    ExternalTargetRecord,
    normalize_target_kind,
)
from chanta_core.external_dominion.trust import (
    DANGEROUS_BOUNDARY_SURFACES,
    ExternalAvailabilityStatus,
    ExternalBoundarySurface,
    ExternalTrustBoundaryProfile,
    ExternalTrustBoundaryStatus,
    normalize_availability_status,
    normalize_trust_status,
)


NON_EXECUTION_INVENTORY_STATUSES = {
    "registered",
    "inventory_only",
    "identity_pending",
    "trust_boundary_pending",
    "blocked",
    "future_track",
    "unknown",
}


@dataclass(frozen=True)
class ExternalTargetRegistrationRequest:
    target_id: str
    target_kind: ExternalTargetKind | str
    display_name: str
    source_ref: str | None = None
    claimed_vendor: str | None = None
    claimed_version: str | None = None
    declared_capabilities: list[str] = field(default_factory=list)
    risk_tags: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        if not self.display_name.strip():
            raise ValueError("display_name must not be blank")
        normalize_target_kind(self.target_kind)
        if not isinstance(self.declared_capabilities, list) or not all(isinstance(item, str) for item in self.declared_capabilities):
            raise TypeError("declared_capabilities must be list[str]")
        if not isinstance(self.risk_tags, list) or not all(isinstance(item, str) for item in self.risk_tags):
            raise TypeError("risk_tags must be list[str]")
        if not isinstance(self.evidence_refs, list) or not all(isinstance(item, str) for item in self.evidence_refs):
            raise TypeError("evidence_refs must be list[str]")

    @property
    def declared_capabilities_are_permissions(self) -> bool:
        return False

    @property
    def risk_tags_are_decisions(self) -> bool:
        return False


@dataclass(frozen=True)
class ExternalTargetInventoryRecord:
    inventory_id: str
    target: ExternalTargetRecord
    identity: ExternalIdentityProfile
    trust_boundary: ExternalTrustBoundaryProfile
    availability_status: ExternalAvailabilityStatus | str
    inventory_status: str
    created_at: str | None = None
    updated_at: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.inventory_id.strip():
            raise ValueError("inventory_id must not be blank")
        if self.target.target_id != self.identity.target_id:
            raise ValueError("target and identity target_id must match")
        if self.target.target_id != self.trust_boundary.target_id:
            raise ValueError("target and trust_boundary target_id must match")
        normalize_availability_status(self.availability_status)
        if self.inventory_status not in NON_EXECUTION_INVENTORY_STATUSES:
            raise ValueError("inventory_status must not imply execution readiness")
        if not isinstance(self.evidence_refs, list) or not all(isinstance(item, str) for item in self.evidence_refs):
            raise TypeError("evidence_refs must be list[str]")

    @property
    def inventory_is_execution_ready(self) -> bool:
        return False

    @property
    def evidence_refs_are_runtime_proof(self) -> bool:
        return False

    @property
    def availability_implies_trust(self) -> bool:
        return False


def infer_identity_status_from_request(request: ExternalTargetRegistrationRequest) -> ExternalIdentityStatus:
    if request.evidence_refs:
        return ExternalIdentityStatus.EVIDENCE_LINKED
    if request.source_ref:
        return ExternalIdentityStatus.SOURCE_DESCRIBED
    if request.display_name or request.claimed_vendor or request.claimed_version:
        return ExternalIdentityStatus.CLAIMED
    return ExternalIdentityStatus.UNKNOWN


def infer_availability_status_from_request(request: ExternalTargetRegistrationRequest) -> ExternalAvailabilityStatus:
    if normalize_target_kind(request.target_kind) is ExternalTargetKind.UNKNOWN:
        return ExternalAvailabilityStatus.UNKNOWN
    if request.source_ref and request.evidence_refs:
        return ExternalAvailabilityStatus.CANDIDATE
    if request.source_ref:
        return ExternalAvailabilityStatus.DOCUMENTATION_ONLY
    return ExternalAvailabilityStatus.LOCAL_REFERENCE_ONLY


def default_trust_boundary_for_target(target: ExternalTargetRecord) -> ExternalTrustBoundaryProfile:
    kind = normalize_target_kind(target.target_kind)
    if kind is ExternalTargetKind.UNKNOWN:
        return ExternalTrustBoundaryProfile(
            target.target_id,
            trust_status=ExternalTrustBoundaryStatus.UNTRUSTED,
            max_observable_level=DominionLevel.D0_OBSERVE,
            allowed_boundary_surfaces=[],
            prohibited_boundary_surfaces=list(DANGEROUS_BOUNDARY_SURFACES),
            requires_human_review=True,
            rationale="Unknown external target defaults to untrusted inventory-only treatment.",
            evidence_refs=[],
            withdrawal_conditions=["target identity or trust evidence changes"],
        )
    return ExternalTrustBoundaryProfile(
        target.target_id,
        trust_status=ExternalTrustBoundaryStatus.OBSERVATION_ONLY,
        max_observable_level=DominionLevel.D1_DESCRIBE,
        allowed_boundary_surfaces=[ExternalBoundarySurface.DATA_BOUNDARY],
        prohibited_boundary_surfaces=list(DANGEROUS_BOUNDARY_SURFACES),
        requires_human_review=True,
        rationale="Registered target may be described from provided metadata only.",
        evidence_refs=[],
        withdrawal_conditions=["target requests execution, credentials, network, browser, RPA, gateway, or delegation"],
    )


def can_enter_observation_flow(record: ExternalTargetInventoryRecord) -> bool:
    trust_status = normalize_trust_status(record.trust_boundary.trust_status)
    availability = normalize_availability_status(record.availability_status)
    return trust_status in {
        ExternalTrustBoundaryStatus.OBSERVATION_ONLY,
        ExternalTrustBoundaryStatus.DESCRIPTION_ONLY,
        ExternalTrustBoundaryStatus.DRY_RUN_CANDIDATE,
    } and availability not in {
        ExternalAvailabilityStatus.BLOCKED,
        ExternalAvailabilityStatus.FUTURE_TRACK,
        ExternalAvailabilityStatus.UNAVAILABLE,
    }


def can_enter_digestion_flow(record: ExternalTargetInventoryRecord) -> bool:
    identity_status = normalize_identity_status(record.identity.identity_status)
    trust_status = normalize_trust_status(record.trust_boundary.trust_status)
    availability = normalize_availability_status(record.availability_status)
    return (
        identity_status in {
            ExternalIdentityStatus.SOURCE_DESCRIBED,
            ExternalIdentityStatus.EVIDENCE_LINKED,
            ExternalIdentityStatus.REFERENCE_VERIFIED,
        }
        and trust_status not in {ExternalTrustBoundaryStatus.BLOCKED, ExternalTrustBoundaryStatus.FUTURE_TRACK}
        and availability not in {ExternalAvailabilityStatus.BLOCKED, ExternalAvailabilityStatus.FUTURE_TRACK, ExternalAvailabilityStatus.UNAVAILABLE}
    )


def can_enter_dominion_flow(record: ExternalTargetInventoryRecord) -> bool:
    trust_status = normalize_trust_status(record.trust_boundary.trust_status)
    availability = normalize_availability_status(record.availability_status)
    has_boundary_classification = bool(record.trust_boundary.prohibited_boundary_surfaces or record.trust_boundary.allowed_boundary_surfaces)
    return (
        has_boundary_classification
        and trust_status in {
            ExternalTrustBoundaryStatus.OBSERVATION_ONLY,
            ExternalTrustBoundaryStatus.DESCRIPTION_ONLY,
            ExternalTrustBoundaryStatus.DRY_RUN_CANDIDATE,
        }
        and availability not in {ExternalAvailabilityStatus.BLOCKED, ExternalAvailabilityStatus.FUTURE_TRACK, ExternalAvailabilityStatus.UNAVAILABLE}
    )


class ExternalTargetInventory:
    def __init__(self) -> None:
        self._records: dict[str, ExternalTargetInventoryRecord] = {}

    def register(self, request: ExternalTargetRegistrationRequest) -> ExternalTargetInventoryRecord:
        if request.target_id in self._records:
            raise ValueError(f"duplicate target_id: {request.target_id}")
        identity_status = infer_identity_status_from_request(request)
        availability_status = infer_availability_status_from_request(request)
        trust_status = ExternalTrustBoundaryStatus.UNTRUSTED if availability_status is ExternalAvailabilityStatus.UNKNOWN else ExternalTrustBoundaryStatus.OBSERVATION_ONLY
        target = ExternalTargetRecord(
            request.target_id,
            request.target_kind,
            request.display_name,
            source_ref=request.source_ref,
            identity_status=identity_status.value,
            trust_status=trust_status.value,
            availability_status=availability_status.value,
            declared_capabilities=list(request.declared_capabilities),
            risk_tags=list(request.risk_tags),
            metadata=dict(request.metadata),
        )
        identity = ExternalIdentityProfile(
            request.target_id,
            claimed_name=request.display_name,
            claimed_vendor=request.claimed_vendor,
            claimed_version=request.claimed_version,
            source_ref=request.source_ref,
            source_kind="provided_ref" if request.source_ref else None,
            evidence_refs=list(request.evidence_refs),
            identity_status=identity_status,
            metadata=dict(request.metadata),
        )
        trust_boundary = default_trust_boundary_for_target(target)
        record = ExternalTargetInventoryRecord(
            f"external_target_inventory_record:{request.target_id}",
            target,
            identity,
            trust_boundary,
            availability_status,
            "registered",
            evidence_refs=list(request.evidence_refs),
            notes=["Inventory registration is not execution."],
            metadata=dict(request.metadata),
        )
        self._records[request.target_id] = record
        return record

    def get(self, target_id: str) -> ExternalTargetInventoryRecord | None:
        return self._records.get(target_id)

    def list_records(self) -> list[ExternalTargetInventoryRecord]:
        return list(self._records.values())

    def has(self, target_id: str) -> bool:
        return target_id in self._records
