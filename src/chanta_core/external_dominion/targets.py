from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ExternalTargetKind(StrEnum):
    EXTERNAL_AGENT_HARNESS = "external_agent_harness"
    EXTERNAL_SKILL_PACKAGE = "external_skill_package"
    EXTERNAL_PROVIDER_RUNTIME = "external_provider_runtime"
    EXTERNAL_GATEWAY = "external_gateway"
    EXTERNAL_CODING_HARNESS = "external_coding_harness"
    EXTERNAL_RPA_RUNTIME = "external_rpa_runtime"
    MCP_SERVER = "mcp_server"
    BROWSER_RUNTIME = "browser_runtime"
    PRIVATE_OVERLAY_CANDIDATE = "private_overlay_candidate"
    UNKNOWN = "unknown"


class ExternalTargetStatus(StrEnum):
    UNKNOWN = "unknown"
    OBSERVED = "observed"
    DESCRIBED = "described"
    TRUSTED_FOR_OBSERVATION = "trusted_for_observation"
    TRUSTED_FOR_DRY_RUN = "trusted_for_dry_run"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


TRUSTED_TARGET_STATUSES = frozenset(
    {
        ExternalTargetStatus.TRUSTED_FOR_OBSERVATION.value,
        ExternalTargetStatus.TRUSTED_FOR_DRY_RUN.value,
    }
)

AVAILABLE_TARGET_STATUSES = frozenset(
    {
        ExternalTargetStatus.OBSERVED.value,
        ExternalTargetStatus.DESCRIBED.value,
        ExternalTargetStatus.TRUSTED_FOR_OBSERVATION.value,
        ExternalTargetStatus.TRUSTED_FOR_DRY_RUN.value,
    }
)


def normalize_target_kind(kind: ExternalTargetKind | str) -> ExternalTargetKind:
    if isinstance(kind, ExternalTargetKind):
        return kind
    if isinstance(kind, str):
        stripped = kind.strip()
        if not stripped:
            raise ValueError("target_kind must not be blank")
        return ExternalTargetKind(stripped)
    raise TypeError(f"unsupported target kind: {kind!r}")


def _status_value(status: ExternalTargetStatus | str) -> str:
    if isinstance(status, ExternalTargetStatus):
        return status.value
    if isinstance(status, str):
        stripped = status.strip()
        if not stripped:
            raise ValueError("status must not be blank")
        return stripped
    raise TypeError(f"unsupported target status: {status!r}")


@dataclass(frozen=True)
class ExternalTargetRecord:
    target_id: str
    target_kind: ExternalTargetKind | str
    display_name: str
    source_ref: str | None = None
    identity_status: str = ExternalTargetStatus.UNKNOWN.value
    trust_status: str = ExternalTargetStatus.UNKNOWN.value
    availability_status: str = ExternalTargetStatus.UNKNOWN.value
    declared_capabilities: list[str] = field(default_factory=list)
    risk_tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        if not self.display_name.strip():
            raise ValueError("display_name must not be blank")
        kind = normalize_target_kind(self.target_kind)
        identity_status = _status_value(self.identity_status)
        trust_status = _status_value(self.trust_status)
        availability_status = _status_value(self.availability_status)
        if kind is ExternalTargetKind.UNKNOWN:
            if trust_status in TRUSTED_TARGET_STATUSES:
                raise ValueError("unknown target kind must not imply trust")
            if availability_status in AVAILABLE_TARGET_STATUSES:
                raise ValueError("unknown target kind must not imply availability")

    @property
    def capabilities_are_permissions(self) -> bool:
        return False

    @property
    def is_trusted(self) -> bool:
        return _status_value(self.trust_status) in TRUSTED_TARGET_STATUSES

    @property
    def is_available(self) -> bool:
        return _status_value(self.availability_status) in AVAILABLE_TARGET_STATUSES
