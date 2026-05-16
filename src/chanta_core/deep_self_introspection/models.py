from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


DEEP_SELF_INTROSPECTION_LAYER = "deep_self_introspection"
DEEP_SELF_INTROSPECTION_VERSION = "v0.21.0"
DEEP_SELF_INTROSPECTION_STATE = "deep_self_introspection_contract_registered"


@dataclass(frozen=True)
class DeepSelfIntrospectionSubject:
    subject_id: str
    name: str
    description: str
    subject_type: str
    introduced_in: str
    status: str
    ocel_object_types: list[str]
    ocel_event_types: list[str]
    ocel_relation_types: list[str]
    required_source_objects: list[str]
    required_read_models: list[str]
    risk_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "name": self.name,
            "description": self.description,
            "subject_type": self.subject_type,
            "introduced_in": self.introduced_in,
            "status": self.status,
            "ocel_object_types": list(self.ocel_object_types),
            "ocel_event_types": list(self.ocel_event_types),
            "ocel_relation_types": list(self.ocel_relation_types),
            "required_source_objects": list(self.required_source_objects),
            "required_read_models": list(self.required_read_models),
            "risk_notes": list(self.risk_notes),
        }


@dataclass(frozen=True)
class DeepSelfIntrospectionRiskProfile:
    read_only: bool = True
    ocel_read_only: bool = True
    uses_existing_self_awareness_graph: bool = True
    mutates_workspace: bool = False
    mutates_memory: bool = False
    mutates_persona: bool = False
    mutates_overlay: bool = False
    mutates_capability_registry: bool = False
    mutates_policy: bool = False
    grants_permission: bool = False
    creates_task: bool = False
    materializes_candidate: bool = False
    promotes_candidate: bool = False
    uses_shell: bool = False
    uses_network: bool = False
    uses_mcp: bool = False
    loads_plugin: bool = False
    executes_external_harness: bool = False
    uses_llm_judge: bool = False
    dangerous_capability: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DeepSelfIntrospectionGateContract:
    requires_explicit_invocation: bool = True
    requires_read_only_gate: bool = True
    requires_execution_envelope: bool = True
    requires_ocel_source_refs: bool = True
    requires_subject_contract: bool = True
    deny_if_missing_ocel_source: bool = True
    deny_if_mutation_requested: bool = True
    deny_if_permission_escalation_requested: bool = True
    deny_if_external_execution_requested: bool = True

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DeepSelfIntrospectionObservabilityContract:
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    workbench_visible: bool = True
    audit_visible: bool = True
    envelope_visible: bool = True
    evidence_refs_required: bool = True
    withdrawal_conditions_required: bool = True
    validity_horizon_required: bool = True

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DeepSelfIntrospectionOCELMapping:
    object_types: list[str]
    event_types: list[str]
    relation_types: list[str]
    effect_types: list[str]
    source_object_types: list[str]
    read_model_types: list[str]

    def to_dict(self) -> dict[str, Any]:
        return {
            "object_types": list(self.object_types),
            "event_types": list(self.event_types),
            "relation_types": list(self.relation_types),
            "effect_types": list(self.effect_types),
            "source_object_types": list(self.source_object_types),
            "read_model_types": list(self.read_model_types),
        }


@dataclass(frozen=True)
class DeepSelfIntrospectionReport:
    report_id: str
    version: str
    subject_id: str
    status: str
    source_refs: list[dict[str, Any]]
    evidence_refs: list[dict[str, Any]]
    findings: list[dict[str, Any]]
    limitations: list[str]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"
    canonical_promotion_enabled: bool = False
    promoted: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "subject_id": self.subject_id,
            "status": self.status,
            "source_refs": [dict(item) for item in self.source_refs],
            "evidence_refs": [dict(item) for item in self.evidence_refs],
            "findings": [dict(item) for item in self.findings],
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
            "canonical_promotion_enabled": self.canonical_promotion_enabled,
            "promoted": self.promoted,
        }


@dataclass(frozen=True)
class DeepSelfIntrospectionContract:
    contract_id: str
    version: str
    definition: str
    subjects: list[DeepSelfIntrospectionSubject]
    seed_skill_ids: list[str]
    risk_profile: DeepSelfIntrospectionRiskProfile
    gate_contract: DeepSelfIntrospectionGateContract
    observability_contract: DeepSelfIntrospectionObservabilityContract
    ocel_mapping: DeepSelfIntrospectionOCELMapping
    pig_projection_required: bool = True
    ocpx_projection_required: bool = True
    workbench_visibility_required: bool = True
    status: str = "contract_only"
    layer: str = DEEP_SELF_INTROSPECTION_LAYER

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "version": self.version,
            "layer": self.layer,
            "definition": self.definition,
            "subjects": [item.to_dict() for item in self.subjects],
            "seed_skill_ids": list(self.seed_skill_ids),
            "risk_profile": self.risk_profile.to_dict(),
            "gate_contract": self.gate_contract.to_dict(),
            "observability_contract": self.observability_contract.to_dict(),
            "ocel_mapping": self.ocel_mapping.to_dict(),
            "pig_projection_required": self.pig_projection_required,
            "ocpx_projection_required": self.ocpx_projection_required,
            "workbench_visibility_required": self.workbench_visibility_required,
            "status": self.status,
        }
