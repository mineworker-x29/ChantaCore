from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level


class ExternalAvailabilityStatus(StrEnum):
    UNKNOWN = "unknown"
    UNAVAILABLE = "unavailable"
    DOCUMENTATION_ONLY = "documentation_only"
    LOCAL_REFERENCE_ONLY = "local_reference_only"
    CANDIDATE = "candidate"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExternalTrustBoundaryStatus(StrEnum):
    UNKNOWN = "unknown"
    UNTRUSTED = "untrusted"
    OBSERVATION_ONLY = "observation_only"
    DESCRIPTION_ONLY = "description_only"
    DRY_RUN_CANDIDATE = "dry_run_candidate"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExternalBoundarySurface(StrEnum):
    DATA_BOUNDARY = "data_boundary"
    CREDENTIAL_BOUNDARY = "credential_boundary"
    NETWORK_BOUNDARY = "network_boundary"
    COMMAND_BOUNDARY = "command_boundary"
    FILESYSTEM_BOUNDARY = "filesystem_boundary"
    MEMORY_BOUNDARY = "memory_boundary"
    PROVIDER_BOUNDARY = "provider_boundary"
    BROWSER_BOUNDARY = "browser_boundary"
    RPA_BOUNDARY = "rpa_boundary"
    GATEWAY_BOUNDARY = "gateway_boundary"
    DELEGATION_BOUNDARY = "delegation_boundary"
    UNKNOWN = "unknown"


DANGEROUS_BOUNDARY_SURFACES = frozenset(
    {
        ExternalBoundarySurface.CREDENTIAL_BOUNDARY,
        ExternalBoundarySurface.NETWORK_BOUNDARY,
        ExternalBoundarySurface.COMMAND_BOUNDARY,
        ExternalBoundarySurface.BROWSER_BOUNDARY,
        ExternalBoundarySurface.RPA_BOUNDARY,
        ExternalBoundarySurface.GATEWAY_BOUNDARY,
    }
)


def normalize_availability_status(status: ExternalAvailabilityStatus | str) -> ExternalAvailabilityStatus:
    if isinstance(status, ExternalAvailabilityStatus):
        return status
    if isinstance(status, str):
        stripped = status.strip()
        if not stripped:
            raise ValueError("availability_status must not be blank")
        return ExternalAvailabilityStatus(stripped)
    raise TypeError(f"unsupported availability status: {status!r}")


def normalize_trust_status(status: ExternalTrustBoundaryStatus | str) -> ExternalTrustBoundaryStatus:
    if isinstance(status, ExternalTrustBoundaryStatus):
        return status
    if isinstance(status, str):
        stripped = status.strip()
        if not stripped:
            raise ValueError("trust_status must not be blank")
        return ExternalTrustBoundaryStatus(stripped)
    raise TypeError(f"unsupported trust boundary status: {status!r}")


def normalize_boundary_surface(surface: ExternalBoundarySurface | str) -> ExternalBoundarySurface:
    if isinstance(surface, ExternalBoundarySurface):
        return surface
    if isinstance(surface, str):
        stripped = surface.strip()
        if not stripped:
            raise ValueError("boundary surface must not be blank")
        return ExternalBoundarySurface(stripped)
    raise TypeError(f"unsupported boundary surface: {surface!r}")


def _normalize_surfaces(surfaces: list[ExternalBoundarySurface | str]) -> list[ExternalBoundarySurface]:
    if not isinstance(surfaces, list):
        raise TypeError("boundary surfaces must be a list")
    return [normalize_boundary_surface(surface) for surface in surfaces]


@dataclass(frozen=True)
class ExternalTrustBoundaryProfile:
    target_id: str
    trust_status: ExternalTrustBoundaryStatus | str = ExternalTrustBoundaryStatus.UNKNOWN
    max_observable_level: DominionLevel | int | str = DominionLevel.D0_OBSERVE
    allowed_boundary_surfaces: list[ExternalBoundarySurface | str] = field(default_factory=list)
    prohibited_boundary_surfaces: list[ExternalBoundarySurface | str] = field(default_factory=lambda: list(DANGEROUS_BOUNDARY_SURFACES))
    requires_human_review: bool = True
    rationale: str = "No reviewed trust boundary has been established."
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        status = normalize_trust_status(self.trust_status)
        level = normalize_dominion_level(self.max_observable_level)
        if level > DominionLevel.D3_SIMULATE:
            raise ValueError("v0.30.1 trust boundary cannot exceed D3_SIMULATE")
        if status is ExternalTrustBoundaryStatus.BLOCKED and level != DominionLevel.D0_OBSERVE:
            raise ValueError("blocked trust boundary must use D0_OBSERVE as safest ceiling")
        _normalize_surfaces(self.allowed_boundary_surfaces)
        prohibited = set(_normalize_surfaces(self.prohibited_boundary_surfaces))
        if status in {ExternalTrustBoundaryStatus.UNKNOWN, ExternalTrustBoundaryStatus.UNTRUSTED}:
            missing = DANGEROUS_BOUNDARY_SURFACES - prohibited
            if missing:
                raise ValueError("unknown or untrusted boundaries must prohibit dangerous surfaces")

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def dry_run_executes(self) -> bool:
        return False
