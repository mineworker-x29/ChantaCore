from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel
from chanta_core.external_dominion.inventory import ExternalTargetInventoryRecord
from chanta_core.external_dominion.trust import ExternalBoundarySurface, normalize_boundary_surface


class ExternalCapabilityKind(StrEnum):
    TOOL = "tool"
    SKILL = "skill"
    PLUGIN = "plugin"
    PROVIDER = "provider"
    AGENT = "agent"
    GATEWAY_CHANNEL = "gateway_channel"
    MCP_TOOL = "mcp_tool"
    BROWSER_ACTION = "browser_action"
    RPA_ACTION = "rpa_action"
    SCHEDULER = "scheduler"
    MEMORY_SURFACE = "memory_surface"
    DELEGATION_SURFACE = "delegation_surface"
    COMMAND_SURFACE = "command_surface"
    FILESYSTEM_SURFACE = "filesystem_surface"
    UNKNOWN = "unknown"


class ExternalCapabilityObservationStatus(StrEnum):
    UNKNOWN = "unknown"
    DECLARED = "declared"
    SOURCE_DESCRIBED = "source_described"
    EVIDENCE_LINKED = "evidence_linked"
    OBSERVED_BY_MANIFEST = "observed_by_manifest"
    OBSERVED_BY_DOCUMENTATION = "observed_by_documentation"
    CONFLICT_DETECTED = "conflict_detected"
    BLOCKED = "blocked"
    FUTURE_TRACK = "future_track"


class ExternalEffectSurface(StrEnum):
    NONE_OBSERVED = "none_observed"
    READ_ONLY = "read_only"
    WRITE_POSSIBLE = "write_possible"
    COMMAND_POSSIBLE = "command_possible"
    NETWORK_POSSIBLE = "network_possible"
    CREDENTIAL_REQUIRED = "credential_required"
    PROVIDER_INVOCATION_POSSIBLE = "provider_invocation_possible"
    BROWSER_AUTOMATION_POSSIBLE = "browser_automation_possible"
    RPA_CONTROL_POSSIBLE = "rpa_control_possible"
    GATEWAY_MESSAGE_POSSIBLE = "gateway_message_possible"
    MEMORY_MUTATION_POSSIBLE = "memory_mutation_possible"
    DELEGATION_POSSIBLE = "delegation_possible"
    EXTERNAL_SIDE_EFFECT_POSSIBLE = "external_side_effect_possible"
    UNKNOWN = "unknown"


class ExternalRiskSignal(StrEnum):
    UNKNOWN = "unknown"
    PRIVATE_DATA_POSSIBLE = "private_data_possible"
    CREDENTIAL_ACCESS_POSSIBLE = "credential_access_possible"
    NETWORK_ACCESS_POSSIBLE = "network_access_possible"
    COMMAND_EXECUTION_POSSIBLE = "command_execution_possible"
    FILESYSTEM_WRITE_POSSIBLE = "filesystem_write_possible"
    PROVIDER_INVOCATION_POSSIBLE = "provider_invocation_possible"
    BROWSER_AUTOMATION_POSSIBLE = "browser_automation_possible"
    RPA_CONTROL_POSSIBLE = "rpa_control_possible"
    GATEWAY_SEND_POSSIBLE = "gateway_send_possible"
    MEMORY_CONTAMINATION_POSSIBLE = "memory_contamination_possible"
    RAW_OUTPUT_PERSISTENCE_POSSIBLE = "raw_output_persistence_possible"
    AUTONOMOUS_LOOP_POSSIBLE = "autonomous_loop_possible"
    DELEGATED_AGENT_POSSIBLE = "delegated_agent_possible"
    EXTERNAL_SIDE_EFFECT_POSSIBLE = "external_side_effect_possible"
    PROMPT_INJECTION_SURFACE = "prompt_injection_surface"
    HIGH_CONTEXT_BLOAT = "high_context_bloat"
    IDENTITY_AMBIGUITY = "identity_ambiguity"
    TRUST_BOUNDARY_UNCLEAR = "trust_boundary_unclear"


DANGEROUS_EFFECT_SURFACES = frozenset(
    {
        ExternalEffectSurface.WRITE_POSSIBLE,
        ExternalEffectSurface.COMMAND_POSSIBLE,
        ExternalEffectSurface.NETWORK_POSSIBLE,
        ExternalEffectSurface.CREDENTIAL_REQUIRED,
        ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE,
        ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE,
        ExternalEffectSurface.RPA_CONTROL_POSSIBLE,
        ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE,
        ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE,
        ExternalEffectSurface.DELEGATION_POSSIBLE,
        ExternalEffectSurface.EXTERNAL_SIDE_EFFECT_POSSIBLE,
        ExternalEffectSurface.UNKNOWN,
    }
)


RISK_TO_EFFECTS = {
    ExternalRiskSignal.PRIVATE_DATA_POSSIBLE: [ExternalEffectSurface.READ_ONLY],
    ExternalRiskSignal.CREDENTIAL_ACCESS_POSSIBLE: [ExternalEffectSurface.CREDENTIAL_REQUIRED],
    ExternalRiskSignal.NETWORK_ACCESS_POSSIBLE: [ExternalEffectSurface.NETWORK_POSSIBLE],
    ExternalRiskSignal.COMMAND_EXECUTION_POSSIBLE: [ExternalEffectSurface.COMMAND_POSSIBLE],
    ExternalRiskSignal.FILESYSTEM_WRITE_POSSIBLE: [ExternalEffectSurface.WRITE_POSSIBLE],
    ExternalRiskSignal.PROVIDER_INVOCATION_POSSIBLE: [ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE],
    ExternalRiskSignal.BROWSER_AUTOMATION_POSSIBLE: [ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE],
    ExternalRiskSignal.RPA_CONTROL_POSSIBLE: [ExternalEffectSurface.RPA_CONTROL_POSSIBLE],
    ExternalRiskSignal.GATEWAY_SEND_POSSIBLE: [ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE],
    ExternalRiskSignal.MEMORY_CONTAMINATION_POSSIBLE: [ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE],
    ExternalRiskSignal.RAW_OUTPUT_PERSISTENCE_POSSIBLE: [ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE],
    ExternalRiskSignal.AUTONOMOUS_LOOP_POSSIBLE: [ExternalEffectSurface.EXTERNAL_SIDE_EFFECT_POSSIBLE],
    ExternalRiskSignal.DELEGATED_AGENT_POSSIBLE: [ExternalEffectSurface.DELEGATION_POSSIBLE],
    ExternalRiskSignal.EXTERNAL_SIDE_EFFECT_POSSIBLE: [ExternalEffectSurface.EXTERNAL_SIDE_EFFECT_POSSIBLE],
}


EFFECT_TO_BOUNDARIES = {
    ExternalEffectSurface.READ_ONLY: [ExternalBoundarySurface.DATA_BOUNDARY],
    ExternalEffectSurface.WRITE_POSSIBLE: [ExternalBoundarySurface.FILESYSTEM_BOUNDARY],
    ExternalEffectSurface.COMMAND_POSSIBLE: [ExternalBoundarySurface.COMMAND_BOUNDARY],
    ExternalEffectSurface.NETWORK_POSSIBLE: [ExternalBoundarySurface.NETWORK_BOUNDARY],
    ExternalEffectSurface.CREDENTIAL_REQUIRED: [ExternalBoundarySurface.CREDENTIAL_BOUNDARY],
    ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE: [ExternalBoundarySurface.PROVIDER_BOUNDARY],
    ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE: [ExternalBoundarySurface.BROWSER_BOUNDARY],
    ExternalEffectSurface.RPA_CONTROL_POSSIBLE: [ExternalBoundarySurface.RPA_BOUNDARY],
    ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE: [ExternalBoundarySurface.GATEWAY_BOUNDARY],
    ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE: [ExternalBoundarySurface.MEMORY_BOUNDARY],
    ExternalEffectSurface.DELEGATION_POSSIBLE: [ExternalBoundarySurface.DELEGATION_BOUNDARY],
    ExternalEffectSurface.EXTERNAL_SIDE_EFFECT_POSSIBLE: [ExternalBoundarySurface.UNKNOWN],
    ExternalEffectSurface.UNKNOWN: [ExternalBoundarySurface.UNKNOWN],
}


def _unique(values: list[Any]) -> list[Any]:
    result: list[Any] = []
    for value in values:
        if value not in result:
            result.append(value)
    return result


def normalize_capability_kind(value: ExternalCapabilityKind | str) -> ExternalCapabilityKind:
    if isinstance(value, ExternalCapabilityKind):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("capability kind must not be blank")
        return ExternalCapabilityKind(stripped)
    raise TypeError(f"unsupported capability kind: {value!r}")


def normalize_observation_status(value: ExternalCapabilityObservationStatus | str) -> ExternalCapabilityObservationStatus:
    if isinstance(value, ExternalCapabilityObservationStatus):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("observation status must not be blank")
        return ExternalCapabilityObservationStatus(stripped)
    raise TypeError(f"unsupported observation status: {value!r}")


def normalize_effect_surface(value: ExternalEffectSurface | str) -> ExternalEffectSurface:
    if isinstance(value, ExternalEffectSurface):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("effect surface must not be blank")
        return ExternalEffectSurface(stripped)
    raise TypeError(f"unsupported effect surface: {value!r}")


def normalize_risk_signal(value: ExternalRiskSignal | str) -> ExternalRiskSignal:
    if isinstance(value, ExternalRiskSignal):
        return value
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            raise ValueError("risk signal must not be blank")
        return ExternalRiskSignal(stripped)
    raise TypeError(f"unsupported risk signal: {value!r}")


def _normalize_effects(values: list[ExternalEffectSurface | str]) -> list[ExternalEffectSurface]:
    if not isinstance(values, list):
        raise TypeError("effect_surfaces must be a list")
    return [normalize_effect_surface(value) for value in values]


def _normalize_boundaries(values: list[ExternalBoundarySurface | str]) -> list[ExternalBoundarySurface]:
    if not isinstance(values, list):
        raise TypeError("boundary_surfaces must be a list")
    return [normalize_boundary_surface(value) for value in values]


def _normalize_risks(values: list[ExternalRiskSignal | str]) -> list[ExternalRiskSignal]:
    if not isinstance(values, list):
        raise TypeError("risk_signals must be a list")
    return [normalize_risk_signal(value) for value in values]


@dataclass(frozen=True)
class ExternalCapabilityDescriptor:
    capability_id: str
    target_id: str
    name: str
    kind: ExternalCapabilityKind | str = ExternalCapabilityKind.UNKNOWN
    description: str | None = None
    observation_status: ExternalCapabilityObservationStatus | str = ExternalCapabilityObservationStatus.DECLARED
    effect_surfaces: list[ExternalEffectSurface | str] = field(default_factory=lambda: [ExternalEffectSurface.NONE_OBSERVED])
    boundary_surfaces: list[ExternalBoundarySurface | str] = field(default_factory=list)
    risk_signals: list[ExternalRiskSignal | str] = field(default_factory=list)
    declared_inputs: list[str] = field(default_factory=list)
    declared_outputs: list[str] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    confidence: str = "unknown"
    conflict_notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.capability_id.strip():
            raise ValueError("capability_id must not be blank")
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        if not self.name.strip():
            raise ValueError("name must not be blank")
        normalize_capability_kind(self.kind)
        status = normalize_observation_status(self.observation_status)
        _normalize_effects(self.effect_surfaces)
        _normalize_boundaries(self.boundary_surfaces)
        _normalize_risks(self.risk_signals)
        if not isinstance(self.declared_inputs, list) or not all(isinstance(item, str) for item in self.declared_inputs):
            raise TypeError("declared_inputs must be list[str]")
        if not isinstance(self.declared_outputs, list) or not all(isinstance(item, str) for item in self.declared_outputs):
            raise TypeError("declared_outputs must be list[str]")
        if not isinstance(self.evidence_refs, list) or not all(isinstance(item, str) for item in self.evidence_refs):
            raise TypeError("evidence_refs must be list[str]")
        if not isinstance(self.conflict_notes, list) or not all(isinstance(item, str) for item in self.conflict_notes):
            raise TypeError("conflict_notes must be list[str]")
        if status is ExternalCapabilityObservationStatus.EVIDENCE_LINKED and not self.evidence_refs:
            raise ValueError("evidence_linked capability requires evidence_refs")
        if status is ExternalCapabilityObservationStatus.CONFLICT_DETECTED and not self.conflict_notes:
            raise ValueError("conflict_detected capability requires conflict_notes")
        if not self.evidence_refs and self.confidence not in {"unknown", "low", "declared_only"}:
            raise ValueError("confidence must be conservative when no evidence_refs exist")

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False

    @property
    def is_internal_skill(self) -> bool:
        return False


@dataclass(frozen=True)
class CapabilityObservationInput:
    target_id: str
    source_kind: str | None = None
    source_ref: str | None = None
    declared_capabilities: list[dict[str, Any] | ExternalCapabilityDescriptor] = field(default_factory=list)
    evidence_refs: list[str] = field(default_factory=list)
    observer: str | None = None
    notes: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        if not isinstance(self.declared_capabilities, list):
            raise TypeError("declared_capabilities must be a list")
        if not isinstance(self.evidence_refs, list) or not all(isinstance(item, str) for item in self.evidence_refs):
            raise TypeError("evidence_refs must be list[str]")
        if not isinstance(self.notes, list) or not all(isinstance(item, str) for item in self.notes):
            raise TypeError("notes must be list[str]")

    @property
    def source_ref_fetched(self) -> bool:
        return False

    @property
    def executes(self) -> bool:
        return False


@dataclass(frozen=True)
class CapabilityObservationReport:
    report_id: str
    target_id: str
    inventory_id: str | None
    source_kind: str | None
    source_ref: str | None
    capabilities: list[ExternalCapabilityDescriptor]
    aggregate_effect_surfaces: list[ExternalEffectSurface]
    aggregate_boundary_surfaces: list[ExternalBoundarySurface]
    aggregate_risk_signals: list[ExternalRiskSignal]
    credential_need_observed: bool
    network_need_observed: bool
    command_surface_observed: bool
    provider_surface_observed: bool
    browser_surface_observed: bool
    rpa_surface_observed: bool
    gateway_surface_observed: bool
    memory_surface_observed: bool
    delegation_surface_observed: bool
    confidence: str
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    blocked_reasons: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.report_id.strip():
            raise ValueError("report_id must not be blank")
        if not self.target_id.strip():
            raise ValueError("target_id must not be blank")
        if not isinstance(self.capabilities, list):
            raise TypeError("capabilities must be a list")
        if any(capability.target_id != self.target_id for capability in self.capabilities):
            raise ValueError("all capability target_ids must match report target_id")
        if set(self.aggregate_effect_surfaces) != set(aggregate_capability_surfaces(self.capabilities)[0]):
            raise ValueError("aggregate_effect_surfaces must match capabilities")
        if set(self.aggregate_boundary_surfaces) != set(aggregate_capability_surfaces(self.capabilities)[1]):
            raise ValueError("aggregate_boundary_surfaces must match capabilities")
        if set(self.aggregate_risk_signals) != set(aggregate_risk_signals(self.capabilities)):
            raise ValueError("aggregate_risk_signals must match capabilities")
        if not isinstance(self.evidence_refs, list) or not all(isinstance(item, str) for item in self.evidence_refs):
            raise TypeError("evidence_refs must be list[str]")

    @property
    def grants_dominion_level(self) -> bool:
        return False

    @property
    def creates_dominion_decision(self) -> bool:
        return False

    @property
    def creates_internal_skill(self) -> bool:
        return False

    @property
    def creates_dominion_target(self) -> bool:
        return False


@dataclass(frozen=True)
class CapabilityObservationSummary:
    target_id: str
    capability_count: int
    safe_descriptive_count: int
    dangerous_surface_count: int
    has_network_surface: bool
    has_credential_surface: bool
    has_command_surface: bool
    has_provider_surface: bool
    has_browser_surface: bool
    has_rpa_surface: bool
    has_gateway_surface: bool
    has_delegation_surface: bool
    recommendation: str
    rationale: str
    evidence_refs: list[str] = field(default_factory=list)

    @property
    def grants_permission(self) -> bool:
        return False

    @property
    def runtime_ready(self) -> bool:
        return False


def infer_effect_surfaces_from_risk_signals(signals: list[ExternalRiskSignal | str]) -> list[ExternalEffectSurface]:
    effects: list[ExternalEffectSurface] = []
    for signal in _normalize_risks(signals):
        effects.extend(RISK_TO_EFFECTS.get(signal, []))
    return _unique(effects) or [ExternalEffectSurface.NONE_OBSERVED]


def infer_boundary_surfaces_from_effects(effects: list[ExternalEffectSurface | str]) -> list[ExternalBoundarySurface]:
    boundaries: list[ExternalBoundarySurface] = []
    for effect in _normalize_effects(effects):
        boundaries.extend(EFFECT_TO_BOUNDARIES.get(effect, []))
    return _unique(boundaries)


def aggregate_capability_surfaces(capabilities: list[ExternalCapabilityDescriptor]) -> tuple[list[ExternalEffectSurface], list[ExternalBoundarySurface]]:
    effects: list[ExternalEffectSurface] = []
    boundaries: list[ExternalBoundarySurface] = []
    for capability in capabilities:
        capability_effects = _normalize_effects(capability.effect_surfaces)
        capability_boundaries = _normalize_boundaries(capability.boundary_surfaces)
        effects.extend(capability_effects)
        boundaries.extend(capability_boundaries)
        boundaries.extend(infer_boundary_surfaces_from_effects(capability_effects))
    return _unique(effects) or [ExternalEffectSurface.NONE_OBSERVED], _unique(boundaries)


def aggregate_risk_signals(capabilities: list[ExternalCapabilityDescriptor]) -> list[ExternalRiskSignal]:
    risks: list[ExternalRiskSignal] = []
    for capability in capabilities:
        risks.extend(_normalize_risks(capability.risk_signals))
    return _unique(risks)


def capability_report_has_dangerous_surface(report: CapabilityObservationReport) -> bool:
    return bool(set(report.aggregate_effect_surfaces) & DANGEROUS_EFFECT_SURFACES)


def capability_report_can_enter_digestion_review(report: CapabilityObservationReport) -> bool:
    if report.blocked_reasons:
        return False
    if any(
        normalize_observation_status(capability.observation_status)
        in {ExternalCapabilityObservationStatus.BLOCKED, ExternalCapabilityObservationStatus.FUTURE_TRACK}
        for capability in report.capabilities
    ):
        return False
    return bool(report.evidence_refs or any(capability.evidence_refs for capability in report.capabilities))


def capability_report_requires_dominion_review(report: CapabilityObservationReport) -> bool:
    return capability_report_has_dangerous_surface(report)


def summarize_capability_observation(report: CapabilityObservationReport) -> CapabilityObservationSummary:
    dangerous_count = sum(1 for effect in report.aggregate_effect_surfaces if effect in DANGEROUS_EFFECT_SURFACES)
    if report.blocked_reasons:
        recommendation = "blocked"
        rationale = "Capability observation has blocked reasons."
    elif dangerous_count:
        recommendation = "dominion_review_required"
        rationale = "Dangerous effect surfaces require later dominion review without execution."
    elif capability_report_can_enter_digestion_review(report):
        recommendation = "digestion_candidate_possible"
        rationale = "Evidence-linked descriptive capability may enter later digestion review."
    elif report.capabilities:
        recommendation = "describe_only"
        rationale = "Capability remains descriptive only."
    else:
        recommendation = "observe_only"
        rationale = "No capabilities were observed."
    return CapabilityObservationSummary(
        report.target_id,
        len(report.capabilities),
        sum(1 for capability in report.capabilities if not set(_normalize_effects(capability.effect_surfaces)) & DANGEROUS_EFFECT_SURFACES),
        dangerous_count,
        report.network_need_observed,
        report.credential_need_observed,
        report.command_surface_observed,
        report.provider_surface_observed,
        report.browser_surface_observed,
        report.rpa_surface_observed,
        report.gateway_surface_observed,
        report.delegation_surface_observed,
        recommendation,
        rationale,
        list(report.evidence_refs),
    )


def _descriptor_from_declared(target_id: str, index: int, declared: dict[str, Any] | ExternalCapabilityDescriptor, evidence_refs: list[str]) -> ExternalCapabilityDescriptor:
    if isinstance(declared, ExternalCapabilityDescriptor):
        return declared
    risk_signals = declared.get("risk_signals", [])
    effect_surfaces = declared.get("effect_surfaces") or infer_effect_surfaces_from_risk_signals(risk_signals)
    boundary_surfaces = declared.get("boundary_surfaces") or infer_boundary_surfaces_from_effects(effect_surfaces)
    return ExternalCapabilityDescriptor(
        declared.get("capability_id", f"external_capability:{target_id}:{index}"),
        target_id,
        declared.get("name", f"declared_capability_{index}"),
        kind=declared.get("kind", ExternalCapabilityKind.UNKNOWN),
        description=declared.get("description"),
        observation_status=declared.get("observation_status", ExternalCapabilityObservationStatus.DECLARED),
        effect_surfaces=effect_surfaces,
        boundary_surfaces=boundary_surfaces,
        risk_signals=risk_signals,
        declared_inputs=declared.get("declared_inputs", []),
        declared_outputs=declared.get("declared_outputs", []),
        evidence_refs=declared.get("evidence_refs", evidence_refs),
        confidence=declared.get("confidence", "low" if evidence_refs else "declared_only"),
        conflict_notes=declared.get("conflict_notes", []),
        metadata=declared.get("metadata", {}),
    )


def build_capability_observation_report(
    observation_input: CapabilityObservationInput,
    inventory_id: str | None = None,
) -> CapabilityObservationReport:
    capabilities = [
        _descriptor_from_declared(observation_input.target_id, index, declared, observation_input.evidence_refs)
        for index, declared in enumerate(observation_input.declared_capabilities)
    ]
    effects, boundaries = aggregate_capability_surfaces(capabilities)
    risks = aggregate_risk_signals(capabilities)
    return CapabilityObservationReport(
        f"capability_observation_report:{observation_input.target_id}",
        observation_input.target_id,
        inventory_id,
        observation_input.source_kind,
        observation_input.source_ref,
        capabilities,
        effects,
        boundaries,
        risks,
        ExternalEffectSurface.CREDENTIAL_REQUIRED in effects,
        ExternalEffectSurface.NETWORK_POSSIBLE in effects,
        ExternalEffectSurface.COMMAND_POSSIBLE in effects,
        ExternalEffectSurface.PROVIDER_INVOCATION_POSSIBLE in effects,
        ExternalEffectSurface.BROWSER_AUTOMATION_POSSIBLE in effects,
        ExternalEffectSurface.RPA_CONTROL_POSSIBLE in effects,
        ExternalEffectSurface.GATEWAY_MESSAGE_POSSIBLE in effects,
        ExternalEffectSurface.MEMORY_MUTATION_POSSIBLE in effects,
        ExternalEffectSurface.DELEGATION_POSSIBLE in effects,
        "low" if observation_input.evidence_refs else "declared_only",
        evidence_refs=list(observation_input.evidence_refs),
        withdrawal_conditions=[
            "capability observation is treated as permission, certification, skill creation, dominion target creation, or execution readiness",
            "source_ref is fetched or live external observation scanning appears",
            "D4+ DominionLevel is inferred from observed capability surfaces",
        ],
        blocked_reasons=[],
        metadata=dict(observation_input.metadata),
    )


def build_capability_observation_from_inventory(
    record: ExternalTargetInventoryRecord,
    declared_capabilities: list[dict[str, Any] | ExternalCapabilityDescriptor] | None = None,
    evidence_refs: list[str] | None = None,
) -> CapabilityObservationReport:
    capability_items: list[dict[str, Any] | ExternalCapabilityDescriptor]
    if declared_capabilities is None:
        capability_items = [
            {
                "name": capability,
                "kind": ExternalCapabilityKind.UNKNOWN,
                "description": None,
                "observation_status": ExternalCapabilityObservationStatus.DECLARED,
                "risk_signals": [],
                "confidence": "declared_only",
            }
            for capability in record.target.declared_capabilities
        ]
    else:
        capability_items = declared_capabilities
    refs = list(evidence_refs if evidence_refs is not None else record.evidence_refs)
    observation_input = CapabilityObservationInput(
        record.target.target_id,
        source_kind=record.identity.source_kind,
        source_ref=record.target.source_ref,
        declared_capabilities=capability_items,
        evidence_refs=refs,
        observer="v0.30.2_contract_model",
        notes=["source_ref is preserved as a reference and is not fetched."],
        metadata=dict(record.metadata),
    )
    return build_capability_observation_report(observation_input, inventory_id=record.inventory_id)


def capability_observation_infers_dominion_level(report: CapabilityObservationReport) -> DominionLevel:
    return DominionLevel.D3_SIMULATE if capability_report_requires_dominion_review(report) else DominionLevel.D1_DESCRIBE
