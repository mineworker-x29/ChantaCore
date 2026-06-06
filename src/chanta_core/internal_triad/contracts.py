from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.external_dominion.dominion_levels import DominionLevel, normalize_dominion_level
from chanta_core.internal_triad.boundaries import (
    DIGESTION_OUTPUT_ARTIFACT_KINDS,
    DOMINION_OUTPUT_ARTIFACT_KINDS,
    OBSERVATION_OUTPUT_ARTIFACT_KINDS,
    V0310_REQUIRED_PROHIBITED_RUNTIME_ACTIONS,
    TriadSkillBoundaryPolicy,
    _require_non_blank,
    _validate_string_list,
    build_default_triad_boundary_policy,
    triad_boundary_preserves_no_execution,
)
from chanta_core.internal_triad.skill_kinds import (
    V0310_RELEASE_NAME,
    V0310_TRACK,
    V0310_VERSION,
    TriadSkillExecutionMode,
    TriadSkillKind,
    TriadSkillStatus,
    normalize_triad_execution_mode,
    normalize_triad_skill_kind,
    normalize_triad_skill_status,
)


V0310_PROHIBITED_UNTIL_LATER_GATE = [
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
]

_ACTIVE_METADATA_FLAGS = {
    "active_skill_registration",
    "active_artifact_registration",
    "active_registry_mutation",
    "active_memory_mutation",
    "tool_registration",
    "mission_installation",
    "policy_activation",
    "memory_writer_activation",
    "runtime_execution",
    "read_only_tool_execution",
    "external_scan",
}


def _metadata_has_active_flag(metadata: dict[str, Any]) -> bool:
    return any(metadata.get(name) is True for name in _ACTIVE_METADATA_FLAGS)


@dataclass(frozen=True)
class TriadSkillContract:
    contract_id: str
    skill_id: str
    skill_kind: TriadSkillKind | str
    name: str
    purpose: str
    execution_mode: TriadSkillExecutionMode | str
    input_contract_refs: list[str]
    output_contract_refs: list[str]
    boundary_policy: TriadSkillBoundaryPolicy
    required_evidence_refs: list[str] = field(default_factory=list)
    required_ocel_object_types: list[str] = field(default_factory=list)
    required_ocel_event_types: list[str] = field(default_factory=list)
    required_ocel_relation_types: list[str] = field(default_factory=list)
    readiness_status: TriadSkillStatus | str = TriadSkillStatus.CONTRACT_DEFINED
    ready_for_next_stage: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_id", self.contract_id)
        _require_non_blank("skill_id", self.skill_id)
        _require_non_blank("name", self.name)
        _require_non_blank("purpose", self.purpose)
        kind = normalize_triad_skill_kind(self.skill_kind)
        if normalize_triad_skill_kind(self.boundary_policy.skill_kind) is not kind:
            raise ValueError("boundary_policy skill_kind must match contract skill_kind")
        mode = normalize_triad_execution_mode(self.execution_mode)
        if mode is TriadSkillExecutionMode.FUTURE_RUNTIME:
            raise ValueError("future_runtime cannot be an active execution mode in v0.31.0")
        normalize_triad_skill_status(self.readiness_status)
        for name in (
            "input_contract_refs",
            "output_contract_refs",
            "required_evidence_refs",
            "required_ocel_object_types",
            "required_ocel_event_types",
            "required_ocel_relation_types",
            "withdrawal_conditions",
        ):
            _validate_string_list(name, getattr(self, name))
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.0")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.0")
        if not triad_boundary_preserves_no_execution(self.boundary_policy):
            raise ValueError("boundary_policy must preserve no execution")
        if _metadata_has_active_flag(self.metadata):
            raise ValueError("triad skill contract metadata must not imply active registration, execution, or mutation")

    @property
    def active_skill_registration(self) -> bool:
        return False


@dataclass(frozen=True)
class ObservationSkillContract(TriadSkillContract):
    def __post_init__(self) -> None:
        super().__post_init__()
        if normalize_triad_skill_kind(self.skill_kind) is not TriadSkillKind.OBSERVATION:
            raise ValueError("ObservationSkillContract skill_kind must be observation")
        required = {"live_external_scan", "source_ref_fetch"}
        if required - set(self.boundary_policy.prohibited_runtime_actions):
            raise ValueError("ObservationSkillContract must prohibit live external scan and source_ref fetch")
        if not set(OBSERVATION_OUTPUT_ARTIFACT_KINDS).issubset(set(self.boundary_policy.allowed_output_artifact_kinds)):
            raise ValueError("ObservationSkillContract must include observation output artifact kinds")


@dataclass(frozen=True)
class DigestionSkillContract(TriadSkillContract):
    def __post_init__(self) -> None:
        super().__post_init__()
        if normalize_triad_skill_kind(self.skill_kind) is not TriadSkillKind.DIGESTION:
            raise ValueError("DigestionSkillContract skill_kind must be digestion")
        required = {
            "active_skill_registry_mutation",
            "tool_registration",
            "mission_installation",
            "policy_activation",
            "memory_writer_activation",
        }
        if required - set(self.boundary_policy.prohibited_runtime_actions):
            raise ValueError("DigestionSkillContract must prohibit active skill/tool/mission/policy/memory mutation")
        if not set(DIGESTION_OUTPUT_ARTIFACT_KINDS).issubset(set(self.boundary_policy.allowed_output_artifact_kinds)):
            raise ValueError("DigestionSkillContract must include internal candidate output artifact kinds")


@dataclass(frozen=True)
class DominionSkillContract(TriadSkillContract):
    def __post_init__(self) -> None:
        super().__post_init__()
        if normalize_triad_skill_kind(self.skill_kind) is not TriadSkillKind.DOMINION:
            raise ValueError("DominionSkillContract skill_kind must be dominion")
        required = {"external_runtime_control", "provider_invocation", "network", "credential", "command", "browser", "rpa", "gateway", "packet_send"}
        if required - set(self.boundary_policy.prohibited_runtime_actions):
            raise ValueError("DominionSkillContract must prohibit external runtime control surfaces")
        if (
            self.boundary_policy.max_dominion_level is not None
            and normalize_dominion_level(self.boundary_policy.max_dominion_level) > DominionLevel.D3_SIMULATE
        ):
            raise ValueError("DominionSkillContract max_dominion_level must not exceed D3_SIMULATE")
        if not set(DOMINION_OUTPUT_ARTIFACT_KINDS).issubset(set(self.boundary_policy.allowed_output_artifact_kinds)):
            raise ValueError("DominionSkillContract must include dominion output artifact kinds")


@dataclass(frozen=True)
class TriadSkillNoExecutionGuarantee:
    guarantee_id: str
    skill_kind: TriadSkillKind | str
    no_external_execution: bool = True
    no_internal_tool_execution: bool = True
    no_network_access: bool = True
    no_credential_access: bool = True
    no_command_execution: bool = True
    no_provider_invocation: bool = True
    no_browser_automation: bool = True
    no_rpa_control: bool = True
    no_gateway_control: bool = True
    no_packet_send: bool = True
    no_registry_mutation: bool = True
    no_memory_mutation: bool = True
    no_rollback_execution: bool = True
    no_retry_execution: bool = True
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("guarantee_id", self.guarantee_id)
        normalize_triad_skill_kind(self.skill_kind)
        _validate_string_list("evidence_refs", self.evidence_refs)
        for name in (
            "no_external_execution",
            "no_internal_tool_execution",
            "no_network_access",
            "no_credential_access",
            "no_command_execution",
            "no_provider_invocation",
            "no_browser_automation",
            "no_rpa_control",
            "no_gateway_control",
            "no_packet_send",
            "no_registry_mutation",
            "no_memory_mutation",
            "no_rollback_execution",
            "no_retry_execution",
        ):
            if getattr(self, name) is not True:
                raise ValueError(f"{name} must be True in v0.31.0")

    @property
    def runtime_enforcement(self) -> bool:
        return False


@dataclass(frozen=True)
class TriadSkillContractSet:
    contract_set_id: str
    version: str
    observation_contract: TriadSkillContract
    digestion_contract: TriadSkillContract
    dominion_contract: TriadSkillContract
    no_execution_guarantees: list[TriadSkillNoExecutionGuarantee] = field(default_factory=list)
    shared_boundary_policy_refs: list[str] = field(default_factory=list)
    ready_for_v0311_observation_skill_foundation: bool = False
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    evidence_refs: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("contract_set_id", self.contract_set_id)
        if V0310_VERSION not in self.version:
            raise ValueError("version must include v0.31.0")
        if normalize_triad_skill_kind(self.observation_contract.skill_kind) is not TriadSkillKind.OBSERVATION:
            raise ValueError("observation_contract skill_kind must be observation")
        if normalize_triad_skill_kind(self.digestion_contract.skill_kind) is not TriadSkillKind.DIGESTION:
            raise ValueError("digestion_contract skill_kind must be digestion")
        if normalize_triad_skill_kind(self.dominion_contract.skill_kind) is not TriadSkillKind.DOMINION:
            raise ValueError("dominion_contract skill_kind must be dominion")
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.0")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.0")
        _validate_string_list("shared_boundary_policy_refs", self.shared_boundary_policy_refs)
        _validate_string_list("evidence_refs", self.evidence_refs)
        if not all(triad_contract_preserves_no_execution(contract) for contract in (self.observation_contract, self.digestion_contract, self.dominion_contract)):
            raise ValueError("all triad contracts must preserve no execution")


@dataclass(frozen=True)
class V0310ReadinessReport:
    report_id: str
    version: str
    contract_set_id: str
    summary: str
    ready_for_v0311_observation_skill_foundation: bool
    ready_for_execution: bool = False
    ready_for_skill_activation: bool = False
    completed_contracts: list[str] = field(default_factory=list)
    blocked_items: list[str] = field(default_factory=list)
    future_track_items: list[str] = field(default_factory=list)
    prohibited_until_later_gate: list[str] = field(default_factory=lambda: list(V0310_PROHIBITED_UNTIL_LATER_GATE))
    evidence_refs: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_non_blank("report_id", self.report_id)
        if V0310_VERSION not in self.version:
            raise ValueError("version must include v0.31.0")
        _require_non_blank("contract_set_id", self.contract_set_id)
        _require_non_blank("summary", self.summary)
        if self.ready_for_execution is not False:
            raise ValueError("ready_for_execution must always be False in v0.31.0")
        if self.ready_for_skill_activation is not False:
            raise ValueError("ready_for_skill_activation must always be False in v0.31.0")
        for name in ("completed_contracts", "blocked_items", "future_track_items", "prohibited_until_later_gate", "evidence_refs", "withdrawal_conditions"):
            _validate_string_list(name, getattr(self, name))
        missing = set(V0310_PROHIBITED_UNTIL_LATER_GATE) - set(self.prohibited_until_later_gate)
        if missing:
            raise ValueError(f"prohibited_until_later_gate missing required items: {sorted(missing)}")

    @property
    def runtime_enablement(self) -> bool:
        return False


def build_observation_skill_contract() -> TriadSkillContract:
    return ObservationSkillContract(
        contract_id="internal_triad_skill_contract:observation:v0.31.0",
        skill_id="internal_triad_skill:observation",
        skill_kind=TriadSkillKind.OBSERVATION,
        name="ObservationSkillContract",
        purpose="Structure and interpret input artifacts as observation reports without external scanning.",
        execution_mode=TriadSkillExecutionMode.REPORT_ONLY,
        input_contract_refs=["external_dominion_v031_handoff_packet:v0.30.9"],
        output_contract_refs=list(OBSERVATION_OUTPUT_ARTIFACT_KINDS),
        boundary_policy=build_default_triad_boundary_policy(TriadSkillKind.OBSERVATION),
        required_evidence_refs=["v0.30.9 handoff evidence refs"],
        required_ocel_object_types=["artifact", "capability", "target"],
        required_ocel_event_types=["observation_contract_defined"],
        required_ocel_relation_types=["artifact_supports_observation"],
        readiness_status=TriadSkillStatus.CONTRACT_DEFINED,
        ready_for_next_stage=True,
        withdrawal_conditions=[
            "ObservationSkillContract is treated as external scan",
            "source_ref fetch is introduced",
            "ready_for_execution becomes true",
        ],
        metadata={"contract_is_runtime_skill": False, "v0310_contract_only": True},
    )


def build_digestion_skill_contract() -> TriadSkillContract:
    return DigestionSkillContract(
        contract_id="internal_triad_skill_contract:digestion:v0.31.0",
        skill_id="internal_triad_skill:digestion",
        skill_kind=TriadSkillKind.DIGESTION,
        name="DigestionSkillContract",
        purpose="Produce internalization candidates only without active registry, tool, mission, policy, or memory mutation.",
        execution_mode=TriadSkillExecutionMode.CANDIDATE_ONLY,
        input_contract_refs=["external_dominion_v031_handoff_packet:v0.30.9", "observation_report_contract"],
        output_contract_refs=list(DIGESTION_OUTPUT_ARTIFACT_KINDS),
        boundary_policy=build_default_triad_boundary_policy(TriadSkillKind.DIGESTION),
        required_evidence_refs=["v0.30.9 reusable contract refs"],
        required_ocel_object_types=["artifact", "candidate", "policy_candidate"],
        required_ocel_event_types=["digestion_contract_defined"],
        required_ocel_relation_types=["candidate_derived_from_artifact"],
        readiness_status=TriadSkillStatus.CONTRACT_DEFINED,
        ready_for_next_stage=True,
        withdrawal_conditions=[
            "DigestionSkillContract is treated as active internalization",
            "active skill registry mutation is introduced",
            "ready_for_skill_activation becomes true",
        ],
        metadata={"contract_is_runtime_skill": False, "v0310_contract_only": True},
    )


def build_dominion_skill_contract() -> TriadSkillContract:
    return DominionSkillContract(
        contract_id="internal_triad_skill_contract:dominion:v0.31.0",
        skill_id="internal_triad_skill:dominion",
        skill_kind=TriadSkillKind.DOMINION,
        name="DominionSkillContract",
        purpose="Produce governance and control candidates without external runtime control or D4-D9 grants.",
        execution_mode=TriadSkillExecutionMode.GOVERNANCE_ONLY,
        input_contract_refs=["external_dominion_v031_handoff_packet:v0.30.9", "digestion_candidate_contract"],
        output_contract_refs=list(DOMINION_OUTPUT_ARTIFACT_KINDS),
        boundary_policy=build_default_triad_boundary_policy(TriadSkillKind.DOMINION),
        required_evidence_refs=["v0.30.9 D4-D9 future-track refs"],
        required_ocel_object_types=["artifact", "candidate", "dominion_boundary"],
        required_ocel_event_types=["dominion_contract_defined"],
        required_ocel_relation_types=["decision_governs_candidate"],
        readiness_status=TriadSkillStatus.CONTRACT_DEFINED,
        ready_for_next_stage=True,
        withdrawal_conditions=[
            "DominionSkillContract is treated as runtime control",
            "D4-D9 dominion levels become grantable",
            "ready_for_execution becomes true",
        ],
        metadata={"contract_is_runtime_skill": False, "v0310_contract_only": True},
    )


def build_triad_no_execution_guarantee(skill_kind: TriadSkillKind | str) -> TriadSkillNoExecutionGuarantee:
    kind = normalize_triad_skill_kind(skill_kind)
    return TriadSkillNoExecutionGuarantee(
        guarantee_id=f"triad_no_execution_guarantee:{kind.value}:v0.31.0",
        skill_kind=kind,
        evidence_refs=["v0.31.0 contract metadata only"],
        metadata={"guarantee_is_runtime_enforcement": False},
    )


def build_triad_skill_contract_set() -> TriadSkillContractSet:
    observation = build_observation_skill_contract()
    digestion = build_digestion_skill_contract()
    dominion = build_dominion_skill_contract()
    return TriadSkillContractSet(
        contract_set_id="internal_triad_skill_contract_set:v0.31.0",
        version=V0310_VERSION,
        observation_contract=observation,
        digestion_contract=digestion,
        dominion_contract=dominion,
        no_execution_guarantees=[
            build_triad_no_execution_guarantee(TriadSkillKind.OBSERVATION),
            build_triad_no_execution_guarantee(TriadSkillKind.DIGESTION),
            build_triad_no_execution_guarantee(TriadSkillKind.DOMINION),
        ],
        shared_boundary_policy_refs=[
            observation.boundary_policy.boundary_policy_id,
            digestion.boundary_policy.boundary_policy_id,
            dominion.boundary_policy.boundary_policy_id,
        ],
        ready_for_v0311_observation_skill_foundation=True,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        evidence_refs=["v0.30.9 ExternalDominionV031HandoffPacket"],
        metadata={
            "parent_track": V0310_TRACK,
            "release_name": V0310_RELEASE_NAME,
            "contract_set_is_runtime_activation": False,
        },
    )


def build_v0310_readiness_report(contract_set: TriadSkillContractSet) -> V0310ReadinessReport:
    return V0310ReadinessReport(
        report_id="internal_triad_skill_readiness_report:v0.31.0",
        version=V0310_VERSION,
        contract_set_id=contract_set.contract_set_id,
        summary="Internal Triad skill contracts are defined for v0.31.1 design handoff only; not execution or skill activation.",
        ready_for_v0311_observation_skill_foundation=contract_set.ready_for_v0311_observation_skill_foundation,
        ready_for_execution=False,
        ready_for_skill_activation=False,
        completed_contracts=[
            contract_set.observation_contract.contract_id,
            contract_set.digestion_contract.contract_id,
            contract_set.dominion_contract.contract_id,
        ],
        blocked_items=[],
        future_track_items=[
            "read-only tool execution",
            "external observation scanning",
            "active internal skill activation",
            "D4-D9 dominion grants",
        ],
        evidence_refs=list(contract_set.evidence_refs),
        withdrawal_conditions=[
            "v0.31.0 contract artifacts are treated as runtime execution",
            "ready_for_execution becomes true",
            "ready_for_skill_activation becomes true",
            "read-only tool execution or external scanning is introduced",
        ],
        metadata={"readiness_report_is_runtime_enablement": False},
    )


def triad_contract_preserves_no_execution(contract: TriadSkillContract) -> bool:
    return (
        contract.ready_for_execution is False
        and contract.ready_for_skill_activation is False
        and contract.active_skill_registration is False
        and normalize_triad_execution_mode(contract.execution_mode) is not TriadSkillExecutionMode.FUTURE_RUNTIME
        and triad_boundary_preserves_no_execution(contract.boundary_policy)
    )


def triad_contract_set_preserves_no_execution(contract_set: TriadSkillContractSet) -> bool:
    return (
        contract_set.ready_for_execution is False
        and contract_set.ready_for_skill_activation is False
        and all(
            triad_contract_preserves_no_execution(contract)
            for contract in (contract_set.observation_contract, contract_set.digestion_contract, contract_set.dominion_contract)
        )
        and all(guarantee.runtime_enforcement is False for guarantee in contract_set.no_execution_guarantees)
    )


def triad_readiness_report_is_not_runtime_ready(report: V0310ReadinessReport) -> bool:
    return report.ready_for_execution is False and report.ready_for_skill_activation is False and report.runtime_enablement is False
