from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any


class ExternalIdentityStatus(StrEnum):
    UNKNOWN = "unknown"
    CLAIMED = "claimed"
    SOURCE_DESCRIBED = "source_described"
    EVIDENCE_LINKED = "evidence_linked"
    REFERENCE_VERIFIED = "reference_verified"
    CONFLICT_DETECTED = "conflict_detected"
    BLOCKED = "blocked"


VERIFIED_IDENTITY_STATUSES = frozenset({ExternalIdentityStatus.REFERENCE_VERIFIED.value})


def normalize_identity_status(status: ExternalIdentityStatus | str) -> ExternalIdentityStatus:
    if isinstance(status, ExternalIdentityStatus):
        return status
    if isinstance(status, str):
        stripped = status.strip()
        if not stripped:
            raise ValueError("identity_status must not be blank")
        return ExternalIdentityStatus(stripped)
    raise TypeError(f"unsupported identity status: {status!r}")


def _require_string_list(values: list[str], field_name: str) -> None:
    if not isinstance(values, list):
        raise TypeError(f"{field_name} must be list[str]")
    if not all(isinstance(value, str) for value in values):
        raise TypeError(f"{field_name} must be list[str]")


@dataclass(frozen=True)
class ExternalIdentityProfile:
    target_id: str
    claimed_name: str | None = None
    claimed_vendor: str | None = None
    claimed_version: str | None = None
    source_ref: str | None = None
    source_kind: str | None = None
    evidence_refs: list[str] = field(default_factory=list)
    identity_status: ExternalIdentityStatus | str = ExternalIdentityStatus.UNKNOWN
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        _require_string_list(self.evidence_refs, "evidence_refs")
        _require_string_list(self.conflict_notes, "conflict_notes")
        status = normalize_identity_status(self.identity_status)
        if status is ExternalIdentityStatus.REFERENCE_VERIFIED and not self.evidence_refs:
            raise ValueError("reference_verified identity requires evidence_refs")
        if status is ExternalIdentityStatus.CONFLICT_DETECTED and not self.conflict_notes:
            raise ValueError("conflict_detected identity requires conflict_notes")

    @property
    def is_claim_verified(self) -> bool:
        return normalize_identity_status(self.identity_status).value in VERIFIED_IDENTITY_STATUSES

    @property
    def is_trusted(self) -> bool:
        return False
