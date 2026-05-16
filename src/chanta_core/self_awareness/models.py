from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.utility.time import utc_now_iso


SELF_AWARENESS_LAYER = "self_awareness"
SELF_AWARENESS_STATE = "self_awareness_foundation_v1_consolidated"


@dataclass(frozen=True)
class SelfAwarenessRiskProfile:
    read_only: bool = True
    mutates_workspace: bool = False
    mutates_memory: bool = False
    mutates_persona: bool = False
    mutates_overlay: bool = False
    uses_shell: bool = False
    uses_network: bool = False
    uses_mcp: bool = False
    loads_plugin: bool = False
    executes_external_harness: bool = False
    dangerous_capability: bool = False
    risk_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "read_only": self.read_only,
            "mutates_workspace": self.mutates_workspace,
            "mutates_memory": self.mutates_memory,
            "mutates_persona": self.mutates_persona,
            "mutates_overlay": self.mutates_overlay,
            "uses_shell": self.uses_shell,
            "uses_network": self.uses_network,
            "uses_mcp": self.uses_mcp,
            "loads_plugin": self.loads_plugin,
            "executes_external_harness": self.executes_external_harness,
            "dangerous_capability": self.dangerous_capability,
            "risk_attrs": dict(self.risk_attrs),
        }


@dataclass(frozen=True)
class SelfAwarenessGateContract:
    gate_id: str
    evidence_refs_required: bool = True
    execution_envelope_required: bool = True
    allow_skill_execution: bool = False
    allow_canonical_mutation: bool = False
    gate_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gate_id": self.gate_id,
            "evidence_refs_required": self.evidence_refs_required,
            "execution_envelope_required": self.execution_envelope_required,
            "allow_skill_execution": self.allow_skill_execution,
            "allow_canonical_mutation": self.allow_canonical_mutation,
            "gate_attrs": dict(self.gate_attrs),
        }


@dataclass(frozen=True)
class SelfAwarenessObservabilityContract:
    observability_id: str
    ocel_object_types: list[str]
    ocel_event_types: list[str]
    ocel_relation_types: list[str]
    pig_visible: bool = True
    ocpx_visible: bool = True
    workbench_visible: bool = True
    observability_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "observability_id": self.observability_id,
            "ocel_object_types": list(self.ocel_object_types),
            "ocel_event_types": list(self.ocel_event_types),
            "ocel_relation_types": list(self.ocel_relation_types),
            "pig_visible": self.pig_visible,
            "ocpx_visible": self.ocpx_visible,
            "workbench_visible": self.workbench_visible,
            "observability_attrs": dict(self.observability_attrs),
        }


@dataclass(frozen=True)
class SelfAwarenessOCELMapping:
    mapping_id: str
    object_types: list[str]
    event_types: list[str]
    relation_types: list[str]
    canonical_process_substrate: str = "ocel"
    state: str = SELF_AWARENESS_STATE
    mapping_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "mapping_id": self.mapping_id,
            "object_types": list(self.object_types),
            "event_types": list(self.event_types),
            "relation_types": list(self.relation_types),
            "canonical_process_substrate": self.canonical_process_substrate,
            "state": self.state,
            "mapping_attrs": dict(self.mapping_attrs),
        }


@dataclass(frozen=True)
class SelfAwarenessCapabilityDescriptor:
    capability_id: str
    skill_id: str
    capability_name: str
    capability_family: str
    output_kind: str
    state: str = SELF_AWARENESS_STATE
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "skill_id": self.skill_id,
            "capability_name": self.capability_name,
            "capability_family": self.capability_family,
            "output_kind": self.output_kind,
            "state": self.state,
            "descriptor_attrs": dict(self.descriptor_attrs),
        }


@dataclass(frozen=True)
class SelfAwarenessSkillContract:
    skill_id: str
    skill_name: str
    description: str
    capability: SelfAwarenessCapabilityDescriptor
    gate_contract: SelfAwarenessGateContract
    observability_contract: SelfAwarenessObservabilityContract
    layer: str = SELF_AWARENESS_LAYER
    implementation_status: str = SELF_AWARENESS_STATE
    effect_type: str = "contract_only"
    execution_enabled: bool = False
    canonical_mutation_enabled: bool = False
    risk_profile: SelfAwarenessRiskProfile = field(default_factory=SelfAwarenessRiskProfile)
    created_at: str = field(default_factory=utc_now_iso)
    contract_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if self.layer != SELF_AWARENESS_LAYER:
            raise ValueError('self-awareness contracts must use layer="self_awareness"')
        if self.execution_enabled is not False:
            raise ValueError("self-awareness contracts are non-executable in v0.20.0")
        if self.canonical_mutation_enabled is not False:
            raise ValueError("self-awareness contracts cannot mutate canonical state")

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "skill_name": self.skill_name,
            "description": self.description,
            "layer": self.layer,
            "implementation_status": self.implementation_status,
            "effect_type": self.effect_type,
            "execution_enabled": self.execution_enabled,
            "canonical_mutation_enabled": self.canonical_mutation_enabled,
            "risk_profile": self.risk_profile.to_dict(),
            "gate_contract": self.gate_contract.to_dict(),
            "observability_contract": self.observability_contract.to_dict(),
            "capability": self.capability.to_dict(),
            "created_at": self.created_at,
            "contract_attrs": dict(self.contract_attrs),
        }


@dataclass(frozen=True)
class SelfAwarenessConformanceReport:
    report_id: str
    passed: bool
    total_contract_count: int
    checked_contract_count: int
    dangerous_capability_count: int
    workspace_mutation_count: int
    memory_mutation_count: int
    persona_mutation_count: int
    overlay_mutation_count: int
    shell_usage_count: int
    network_usage_count: int
    mcp_usage_count: int
    plugin_loading_count: int
    external_harness_execution_count: int
    execution_enabled_count: int
    canonical_mutation_enabled_count: int
    failed_contract_ids: list[str]
    findings: list[str]
    created_at: str = field(default_factory=utc_now_iso)
    report_attrs: dict[str, Any] = field(default_factory=dict)

    @property
    def status(self) -> str:
        return "passed" if self.passed else "failed"

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "passed": self.passed,
            "status": self.status,
            "total_contract_count": self.total_contract_count,
            "checked_contract_count": self.checked_contract_count,
            "dangerous_capability_count": self.dangerous_capability_count,
            "workspace_mutation_count": self.workspace_mutation_count,
            "memory_mutation_count": self.memory_mutation_count,
            "persona_mutation_count": self.persona_mutation_count,
            "overlay_mutation_count": self.overlay_mutation_count,
            "shell_usage_count": self.shell_usage_count,
            "network_usage_count": self.network_usage_count,
            "mcp_usage_count": self.mcp_usage_count,
            "plugin_loading_count": self.plugin_loading_count,
            "external_harness_execution_count": self.external_harness_execution_count,
            "execution_enabled_count": self.execution_enabled_count,
            "canonical_mutation_enabled_count": self.canonical_mutation_enabled_count,
            "failed_contract_ids": list(self.failed_contract_ids),
            "findings": list(self.findings),
            "created_at": self.created_at,
            "report_attrs": dict(self.report_attrs),
        }
