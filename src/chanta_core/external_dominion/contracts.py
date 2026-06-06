from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import (
    V0300_VERSION,
    DominionLevel,
    is_v030_grantable_level,
    normalize_dominion_level,
)


V0300_TRACK = "External Dominion Control Plane Foundation"
V0300_RELEASE_NAME = "v0.30.0 External Dominion Contract"
V0300_NEXT_STEP = "v0.30.1 External Target Inventory / Identity / Trust Boundary"

V029_GATE_INHERITANCE_REFS = [
    "v0.29.0 External Provider Adapter Contract",
    "v0.29.1 Provider Capability Inventory / Adapter Registry",
    "v0.29.2 Mock Adapter Harness / No-Network Default",
    "v0.29.3 Permission / Safety / Scope Gate for External Adapters",
    "v0.29.4 Credential / Secret / Network Boundary",
    "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan",
    "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary",
    "v0.29.7 External Skill Packaging / Certification Matrix",
    "v0.29.8 Limited Provider Invocation Preview Gate",
    "v0.29.9 External Provider Adapter Foundation Consolidation",
]

V0300_PROHIBITED_RUNTIME_FLAGS = {
    "provider_invocation_runtime_ready": False,
    "limited_preview_execution_ready_now": False,
    "live_adapter_runtime_ready": False,
    "external_agent_dominion_runtime_ready": False,
    "network_access_ready": False,
    "credential_access_ready": False,
    "command_execution_ready": False,
    "rpa_runtime_control_ready": False,
    "gateway_control_ready": False,
}


class DominionDecisionType(StrEnum):
    DENY = "deny"
    DEFER = "defer"
    NO_OP = "no_op"
    OBSERVE_ONLY = "observe_only"
    DESCRIBE_ONLY = "describe_only"
    DRY_RUN_ONLY = "dry_run_only"
    FUTURE_TRACK = "future_track"


@dataclass(frozen=True)
class ExternalDominionContract:
    contract_id: str
    version: str
    purpose: str
    max_grantable_level: DominionLevel
    prohibited_runtime_flags: dict[str, bool]
    inherited_gate_refs: list[str]
    validity_horizon: str
    withdrawal_conditions: list[str]
    provider_invocation_runtime_ready: bool = False
    limited_preview_execution_ready_now: bool = False
    live_adapter_runtime_ready: bool = False
    external_agent_dominion_runtime_ready: bool = False
    network_access_ready: bool = False
    credential_access_ready: bool = False
    command_execution_ready: bool = False
    rpa_runtime_control_ready: bool = False
    gateway_control_ready: bool = False

    def __post_init__(self) -> None:
        if not self.contract_id.strip():
            raise ValueError("contract_id must not be blank")
        if not self.version.strip():
            raise ValueError("version must not be blank")
        if normalize_dominion_level(self.max_grantable_level) != DominionLevel.D3_SIMULATE:
            raise ValueError("v0.30.0 max grantable level must be D3_SIMULATE")
        for name in V0300_PROHIBITED_RUNTIME_FLAGS:
            if getattr(self, name) is not False:
                raise ValueError(f"{name} must remain false in v0.30.0")
            if self.prohibited_runtime_flags.get(name) is not False:
                raise ValueError(f"prohibited_runtime_flags[{name}] must be false")


@dataclass(frozen=True)
class DominionAuthorityRequest:
    request_id: str
    target_id: str
    requested_level: DominionLevel | int | str
    requested_capabilities: list[str] = field(default_factory=list)
    rationale: str = ""
    evidence_refs: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.request_id.strip():
            raise ValueError("request_id must not be blank")
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        normalize_dominion_level(self.requested_level)

    @property
    def grants_authority(self) -> bool:
        return False


@dataclass(frozen=True)
class DominionDecision:
    decision_id: str
    target_id: str
    requested_level: DominionLevel | int | str
    granted_level: DominionLevel | int | str | None
    decision: DominionDecisionType | str
    reason: str
    evidence_refs: list[str] = field(default_factory=list)
    approval_required: bool = False
    expiry: str | None = None
    withdrawal_conditions: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.decision_id.strip():
            raise ValueError("decision_id must not be blank")
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        if not self.reason.strip():
            raise ValueError("reason must not be blank")
        requested = normalize_dominion_level(self.requested_level)
        decision = DominionDecisionType(self.decision)
        if self.granted_level is not None:
            granted = normalize_dominion_level(self.granted_level)
            if not is_v030_grantable_level(granted):
                raise ValueError("v0.30.0 decisions cannot grant D4+ dominion levels")
            if granted > requested:
                raise ValueError("granted level must not exceed requested level")
        if requested > DominionLevel.D3_SIMULATE and decision not in {
            DominionDecisionType.DENY,
            DominionDecisionType.DEFER,
            DominionDecisionType.FUTURE_TRACK,
            DominionDecisionType.NO_OP,
            DominionDecisionType.OBSERVE_ONLY,
            DominionDecisionType.DESCRIBE_ONLY,
            DominionDecisionType.DRY_RUN_ONLY,
        }:
            raise ValueError("D4+ requests must remain denied, deferred, no-op, or future-track in v0.30.0")

    @property
    def approval_granted(self) -> bool:
        return False


def validate_v030_grant(decision: DominionDecision) -> bool:
    if decision.granted_level is None:
        return True
    return is_v030_grantable_level(decision.granted_level)


def make_v030_contract() -> ExternalDominionContract:
    return ExternalDominionContract(
        contract_id="external_dominion_contract:v0.30.0",
        version=V0300_VERSION,
        purpose=(
            "Define how external targets are represented, classified, constrained, "
            "and reasoned about before any external dominion runtime exists."
        ),
        max_grantable_level=DominionLevel.D3_SIMULATE,
        prohibited_runtime_flags=dict(V0300_PROHIBITED_RUNTIME_FLAGS),
        inherited_gate_refs=list(V029_GATE_INHERITANCE_REFS),
        validity_horizon=(
            "Valid until v0.30.1 External Target Inventory / Identity / Trust Boundary "
            "begins or External Dominion policy changes."
        ),
        withdrawal_conditions=[
            "external agent execution or delegation execution appears",
            "provider invocation, provider SDK invocation, network call, credential access, or command execution appears",
            "browser, RPA, gateway, rollback, retry, or external side-effect runtime appears",
            "D4+ dominion level becomes grantable in v0.30.0",
            "v0.29 provider adapter gates are bypassed",
            "LLM judgment becomes the sole trust or certification authority",
        ],
    )
