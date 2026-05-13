from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.observation.ontology import (
    ACTION_TYPES,
    CONFIDENCE_CLASSES,
    EFFECT_TYPES,
    OBJECT_TYPES,
    RELATION_TYPES,
    default_ontology_specs,
)
from chanta_core.observation_digest import ObservedAgentRun
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_agent_behavior_inference_v2_id,
    new_agent_fleet_observation_snapshot_id,
    new_agent_instance_id,
    new_agent_movement_ontology_term_id,
    new_agent_observation_adapter_profile_id,
    new_agent_observation_collector_contract_id,
    new_agent_observation_correction_id,
    new_agent_observation_normalized_event_v2_id,
    new_agent_observation_review_id,
    new_agent_observation_spine_finding_id,
    new_agent_observation_spine_policy_id,
    new_agent_observation_spine_result_id,
    new_agent_runtime_descriptor_id,
    new_observation_export_policy_id,
    new_observation_redaction_policy_id,
    new_observed_agent_object_id,
    new_observed_agent_relation_id,
    new_runtime_environment_snapshot_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


def _clamp_confidence(value: float | int | None, default: float = 0.0) -> float:
    try:
        numeric = float(default if value is None else value)
    except (TypeError, ValueError):
        numeric = default
    return max(0.0, min(1.0, numeric))


def _preview(value: Any, max_chars: int = 400) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        text = value
    else:
        text = json.dumps(value, ensure_ascii=False, sort_keys=True)
    text = " ".join(text.split())
    return text[:max_chars]


@dataclass(frozen=True)
class AgentInstance:
    agent_instance_id: str
    source_runtime: str
    source_version: str | None
    source_agent_id: str | None
    source_agent_name: str | None
    host_ref: str | None
    workspace_ref: str | None
    profile_ref: str | None
    operator_ref: str | None
    privacy_scope: str
    trusted: bool
    created_at: str
    instance_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "agent_instance_id": self.agent_instance_id,
            "source_runtime": self.source_runtime,
            "source_version": self.source_version,
            "source_agent_id": self.source_agent_id,
            "source_agent_name": self.source_agent_name,
            "host_ref": self.host_ref,
            "workspace_ref": self.workspace_ref,
            "profile_ref": self.profile_ref,
            "operator_ref": self.operator_ref,
            "privacy_scope": self.privacy_scope,
            "trusted": self.trusted,
            "created_at": self.created_at,
            "instance_attrs": dict(self.instance_attrs),
        }


@dataclass(frozen=True)
class AgentRuntimeDescriptor:
    runtime_descriptor_id: str
    runtime_name: str
    runtime_kind: str
    runtime_version: str | None
    harness_family: str | None
    supports_ocel_export: bool
    supports_jsonl_transcript: bool
    supports_tool_lifecycle_events: bool
    supports_permission_events: bool
    supports_sidecar_observation: bool
    supports_event_bus: bool
    created_at: str
    runtime_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "runtime_descriptor_id": self.runtime_descriptor_id,
            "runtime_name": self.runtime_name,
            "runtime_kind": self.runtime_kind,
            "runtime_version": self.runtime_version,
            "harness_family": self.harness_family,
            "supports_ocel_export": self.supports_ocel_export,
            "supports_jsonl_transcript": self.supports_jsonl_transcript,
            "supports_tool_lifecycle_events": self.supports_tool_lifecycle_events,
            "supports_permission_events": self.supports_permission_events,
            "supports_sidecar_observation": self.supports_sidecar_observation,
            "supports_event_bus": self.supports_event_bus,
            "created_at": self.created_at,
            "runtime_attrs": dict(self.runtime_attrs),
        }


@dataclass(frozen=True)
class RuntimeEnvironmentSnapshot:
    environment_snapshot_id: str
    agent_instance_id: str
    observed_run_id: str | None
    runtime_kind: str
    workspace_ref: str | None
    sandbox_enabled: bool
    network_enabled: bool
    shell_enabled: bool
    write_enabled: bool
    permission_mode: str
    model_ref: str | None
    tool_surface_hash: str | None
    created_at: str
    environment_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "environment_snapshot_id": self.environment_snapshot_id,
            "agent_instance_id": self.agent_instance_id,
            "observed_run_id": self.observed_run_id,
            "runtime_kind": self.runtime_kind,
            "workspace_ref": self.workspace_ref,
            "sandbox_enabled": self.sandbox_enabled,
            "network_enabled": self.network_enabled,
            "shell_enabled": self.shell_enabled,
            "write_enabled": self.write_enabled,
            "permission_mode": self.permission_mode,
            "model_ref": self.model_ref,
            "tool_surface_hash": self.tool_surface_hash,
            "created_at": self.created_at,
            "environment_attrs": dict(self.environment_attrs),
        }


@dataclass(frozen=True)
class AgentObservationSpinePolicy:
    policy_id: str
    policy_name: str
    allow_batch_file_observation: bool
    allow_tail_file_observation: bool
    allow_runtime_hook_observation: bool
    allow_event_bus_observation: bool
    allow_sidecar_observation: bool
    require_redaction: bool
    require_confidence: bool
    require_evidence_refs: bool
    require_withdrawal_conditions: bool
    allow_causal_claims_by_default: bool
    max_raw_records: int
    max_preview_chars: int
    status: str
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "allow_batch_file_observation": self.allow_batch_file_observation,
            "allow_tail_file_observation": self.allow_tail_file_observation,
            "allow_runtime_hook_observation": self.allow_runtime_hook_observation,
            "allow_event_bus_observation": self.allow_event_bus_observation,
            "allow_sidecar_observation": self.allow_sidecar_observation,
            "require_redaction": self.require_redaction,
            "require_confidence": self.require_confidence,
            "require_evidence_refs": self.require_evidence_refs,
            "require_withdrawal_conditions": self.require_withdrawal_conditions,
            "allow_causal_claims_by_default": self.allow_causal_claims_by_default,
            "max_raw_records": self.max_raw_records,
            "max_preview_chars": self.max_preview_chars,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class AgentObservationCollectorContract:
    collector_contract_id: str
    collector_kind: str
    implemented: bool
    enabled: bool
    source_kinds_supported: list[str]
    output_event_schema_version: str
    requires_redaction_policy: bool
    created_at: str
    collector_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "collector_contract_id": self.collector_contract_id,
            "collector_kind": self.collector_kind,
            "implemented": self.implemented,
            "enabled": self.enabled,
            "source_kinds_supported": list(self.source_kinds_supported),
            "output_event_schema_version": self.output_event_schema_version,
            "requires_redaction_policy": self.requires_redaction_policy,
            "created_at": self.created_at,
            "collector_attrs": dict(self.collector_attrs),
        }


@dataclass(frozen=True)
class AgentObservationAdapterProfile:
    adapter_profile_id: str
    adapter_name: str
    source_runtime: str
    supported_formats: list[str]
    supported_event_types: list[str]
    confidence_policy: str
    schema_version: str
    adapter_version: str
    implemented: bool
    created_at: str
    adapter_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_profile_id": self.adapter_profile_id,
            "adapter_name": self.adapter_name,
            "source_runtime": self.source_runtime,
            "supported_formats": list(self.supported_formats),
            "supported_event_types": list(self.supported_event_types),
            "confidence_policy": self.confidence_policy,
            "schema_version": self.schema_version,
            "adapter_version": self.adapter_version,
            "implemented": self.implemented,
            "created_at": self.created_at,
            "adapter_attrs": dict(self.adapter_attrs),
        }


@dataclass(frozen=True)
class AgentMovementOntologyTerm:
    ontology_term_id: str
    term_kind: str
    term_value: str
    description: str
    parent_term: str | None
    stable: bool
    created_at: str
    term_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ontology_term_id": self.ontology_term_id,
            "term_kind": self.term_kind,
            "term_value": self.term_value,
            "description": self.description,
            "parent_term": self.parent_term,
            "stable": self.stable,
            "created_at": self.created_at,
            "term_attrs": dict(self.term_attrs),
        }


@dataclass(frozen=True)
class AgentObservationNormalizedEventV2:
    normalized_event_id: str
    batch_id: str | None
    source_event_id: str | None
    source_runtime: str
    source_format: str
    source_schema_version: str | None
    adapter_version: str
    observed_activity: str
    canonical_action_type: str
    observed_timestamp: str | None
    actor_type: str | None
    actor_ref: str | None
    object_refs: list[str]
    effect_type: str
    input_preview: str | None
    output_preview: str | None
    confidence: float
    confidence_class: str
    evidence_ref: str | None
    uncertainty_notes: list[str]
    withdrawal_conditions: list[str]
    created_at: str
    event_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "normalized_event_id": self.normalized_event_id,
            "batch_id": self.batch_id,
            "source_event_id": self.source_event_id,
            "source_runtime": self.source_runtime,
            "source_format": self.source_format,
            "source_schema_version": self.source_schema_version,
            "adapter_version": self.adapter_version,
            "observed_activity": self.observed_activity,
            "canonical_action_type": self.canonical_action_type,
            "observed_timestamp": self.observed_timestamp,
            "actor_type": self.actor_type,
            "actor_ref": self.actor_ref,
            "object_refs": list(self.object_refs),
            "effect_type": self.effect_type,
            "input_preview": self.input_preview,
            "output_preview": self.output_preview,
            "confidence": self.confidence,
            "confidence_class": self.confidence_class,
            "evidence_ref": self.evidence_ref,
            "uncertainty_notes": list(self.uncertainty_notes),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "created_at": self.created_at,
            "event_attrs": dict(self.event_attrs),
        }


@dataclass(frozen=True)
class ObservedAgentObject:
    observed_object_id: str
    observed_run_id: str
    object_type: str
    object_ref: str
    source_object_ref: str | None
    confidence: float
    evidence_refs: list[str]
    created_at: str
    object_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "observed_object_id": self.observed_object_id,
            "observed_run_id": self.observed_run_id,
            "object_type": self.object_type,
            "object_ref": self.object_ref,
            "source_object_ref": self.source_object_ref,
            "confidence": self.confidence,
            "evidence_refs": list(self.evidence_refs),
            "created_at": self.created_at,
            "object_attrs": dict(self.object_attrs),
        }


@dataclass(frozen=True)
class ObservedAgentRelation:
    observed_relation_id: str
    observed_run_id: str
    source_ref: str
    target_ref: str
    relation_type: str
    confidence: float
    causal_claim: bool
    evidence_refs: list[str]
    uncertainty_notes: list[str]
    created_at: str
    relation_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", _clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "observed_relation_id": self.observed_relation_id,
            "observed_run_id": self.observed_run_id,
            "source_ref": self.source_ref,
            "target_ref": self.target_ref,
            "relation_type": self.relation_type,
            "confidence": self.confidence,
            "causal_claim": self.causal_claim,
            "evidence_refs": list(self.evidence_refs),
            "uncertainty_notes": list(self.uncertainty_notes),
            "created_at": self.created_at,
            "relation_attrs": dict(self.relation_attrs),
        }


@dataclass(frozen=True)
class AgentBehaviorInferenceV2:
    inference_id: str
    observed_run_id: str
    inferred_goal: str | None
    inferred_goal_confidence: float
    inferred_intent: str | None
    inferred_task_type: str | None
    inferred_action_sequence: list[str]
    inferred_skill_sequence: list[str]
    inferred_tool_sequence: list[str]
    touched_object_types: list[str]
    effect_profile: list[str]
    outcome_inference: str | None
    outcome_confidence: float
    confirmed_observations: list[str]
    data_based_interpretations: list[str]
    likely_hypotheses: list[str]
    estimates: list[str]
    unknown_or_needs_verification: list[str]
    failure_signals: list[str]
    recovery_signals: list[str]
    evidence_refs: list[str]
    uncertainty_notes: list[str]
    withdrawal_conditions: list[str]
    created_at: str
    inference_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "inferred_goal_confidence", _clamp_confidence(self.inferred_goal_confidence))
        object.__setattr__(self, "outcome_confidence", _clamp_confidence(self.outcome_confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "inference_id": self.inference_id,
            "observed_run_id": self.observed_run_id,
            "inferred_goal": self.inferred_goal,
            "inferred_goal_confidence": self.inferred_goal_confidence,
            "inferred_intent": self.inferred_intent,
            "inferred_task_type": self.inferred_task_type,
            "inferred_action_sequence": list(self.inferred_action_sequence),
            "inferred_skill_sequence": list(self.inferred_skill_sequence),
            "inferred_tool_sequence": list(self.inferred_tool_sequence),
            "touched_object_types": list(self.touched_object_types),
            "effect_profile": list(self.effect_profile),
            "outcome_inference": self.outcome_inference,
            "outcome_confidence": self.outcome_confidence,
            "confirmed_observations": list(self.confirmed_observations),
            "data_based_interpretations": list(self.data_based_interpretations),
            "likely_hypotheses": list(self.likely_hypotheses),
            "estimates": list(self.estimates),
            "unknown_or_needs_verification": list(self.unknown_or_needs_verification),
            "failure_signals": list(self.failure_signals),
            "recovery_signals": list(self.recovery_signals),
            "evidence_refs": list(self.evidence_refs),
            "uncertainty_notes": list(self.uncertainty_notes),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "created_at": self.created_at,
            "inference_attrs": dict(self.inference_attrs),
        }


@dataclass(frozen=True)
class AgentObservationReview:
    review_id: str
    observed_run_id: str
    inference_id: str | None
    review_status: str
    reviewer_type: str
    reviewer_id: str | None
    decision: str
    reason: str | None
    created_at: str
    review_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_id": self.review_id,
            "observed_run_id": self.observed_run_id,
            "inference_id": self.inference_id,
            "review_status": self.review_status,
            "reviewer_type": self.reviewer_type,
            "reviewer_id": self.reviewer_id,
            "decision": self.decision,
            "reason": self.reason,
            "created_at": self.created_at,
            "review_attrs": dict(self.review_attrs),
        }


@dataclass(frozen=True)
class AgentObservationCorrection:
    correction_id: str
    review_id: str
    corrected_field: str
    old_value_preview: str | None
    new_value_preview: str | None
    correction_reason: str | None
    created_at: str
    correction_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "correction_id": self.correction_id,
            "review_id": self.review_id,
            "corrected_field": self.corrected_field,
            "old_value_preview": self.old_value_preview,
            "new_value_preview": self.new_value_preview,
            "correction_reason": self.correction_reason,
            "created_at": self.created_at,
            "correction_attrs": dict(self.correction_attrs),
        }


@dataclass(frozen=True)
class ObservationRedactionPolicy:
    redaction_policy_id: str
    policy_name: str
    redact_private_paths: bool
    redact_full_bodies: bool
    redact_secrets: bool
    redact_user_identifiers: bool
    max_preview_chars: int
    allowed_export_fields: list[str]
    denied_export_fields: list[str]
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "redaction_policy_id": self.redaction_policy_id,
            "policy_name": self.policy_name,
            "redact_private_paths": self.redact_private_paths,
            "redact_full_bodies": self.redact_full_bodies,
            "redact_secrets": self.redact_secrets,
            "redact_user_identifiers": self.redact_user_identifiers,
            "max_preview_chars": self.max_preview_chars,
            "allowed_export_fields": list(self.allowed_export_fields),
            "denied_export_fields": list(self.denied_export_fields),
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class ObservationExportPolicy:
    export_policy_id: str
    policy_name: str
    export_mode: str
    allow_raw_transcript_export: bool
    allow_full_file_body_export: bool
    allow_private_memory_export: bool
    require_operator_approval: bool
    require_redaction: bool
    created_at: str
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "export_policy_id": self.export_policy_id,
            "policy_name": self.policy_name,
            "export_mode": self.export_mode,
            "allow_raw_transcript_export": self.allow_raw_transcript_export,
            "allow_full_file_body_export": self.allow_full_file_body_export,
            "allow_private_memory_export": self.allow_private_memory_export,
            "require_operator_approval": self.require_operator_approval,
            "require_redaction": self.require_redaction,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class AgentFleetObservationSnapshot:
    fleet_snapshot_id: str
    agent_instance_count: int
    observed_run_count: int
    source_runtime_counts: dict[str, int]
    action_type_counts: dict[str, int]
    object_type_counts: dict[str, int]
    failure_signal_counts: dict[str, int]
    candidate_pattern_count: int
    created_at: str
    snapshot_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "fleet_snapshot_id": self.fleet_snapshot_id,
            "agent_instance_count": self.agent_instance_count,
            "observed_run_count": self.observed_run_count,
            "source_runtime_counts": dict(self.source_runtime_counts),
            "action_type_counts": dict(self.action_type_counts),
            "object_type_counts": dict(self.object_type_counts),
            "failure_signal_counts": dict(self.failure_signal_counts),
            "candidate_pattern_count": self.candidate_pattern_count,
            "created_at": self.created_at,
            "snapshot_attrs": dict(self.snapshot_attrs),
        }


@dataclass(frozen=True)
class AgentObservationSpineFinding:
    finding_id: str
    subject_ref: str | None
    finding_type: str
    status: str
    severity: str
    message: str
    evidence_ref: str | None
    created_at: str
    finding_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "finding_id": self.finding_id,
            "subject_ref": self.subject_ref,
            "finding_type": self.finding_type,
            "status": self.status,
            "severity": self.severity,
            "message": self.message,
            "evidence_ref": self.evidence_ref,
            "created_at": self.created_at,
            "finding_attrs": dict(self.finding_attrs),
        }


@dataclass(frozen=True)
class AgentObservationSpineResult:
    result_id: str
    operation_kind: str
    status: str
    created_object_refs: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "result_id": self.result_id,
            "operation_kind": self.operation_kind,
            "status": self.status,
            "created_object_refs": list(self.created_object_refs),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class AgentObservationSpineService:
    def __init__(
        self,
        *,
        trace_service: TraceService | None = None,
        ocel_store: OCELStore | None = None,
    ) -> None:
        if trace_service is not None:
            self.trace_service = trace_service
        elif ocel_store is not None:
            self.trace_service = TraceService(ocel_store=ocel_store)
        else:
            self.trace_service = TraceService()
        self.last_policy: AgentObservationSpinePolicy | None = None
        self.last_collectors: list[AgentObservationCollectorContract] = []
        self.last_adapters: list[AgentObservationAdapterProfile] = []
        self.last_terms: list[AgentMovementOntologyTerm] = []
        self.last_events: list[AgentObservationNormalizedEventV2] = []
        self.last_objects: list[ObservedAgentObject] = []
        self.last_relations: list[ObservedAgentRelation] = []
        self.last_inference: AgentBehaviorInferenceV2 | None = None
        self.last_redaction_policy: ObservationRedactionPolicy | None = None
        self.last_export_policy: ObservationExportPolicy | None = None
        self.last_fleet_snapshot: AgentFleetObservationSnapshot | None = None
        self.last_findings: list[AgentObservationSpineFinding] = []
        self.last_result: AgentObservationSpineResult | None = None

    def create_default_policy(self) -> AgentObservationSpinePolicy:
        policy = AgentObservationSpinePolicy(
            policy_id=new_agent_observation_spine_policy_id(),
            policy_name="default_agent_observation_spine_policy",
            allow_batch_file_observation=True,
            allow_tail_file_observation=False,
            allow_runtime_hook_observation=False,
            allow_event_bus_observation=False,
            allow_sidecar_observation=False,
            require_redaction=True,
            require_confidence=True,
            require_evidence_refs=True,
            require_withdrawal_conditions=True,
            allow_causal_claims_by_default=False,
            max_raw_records=1000,
            max_preview_chars=400,
            status="active",
            created_at=utc_now_iso(),
            policy_attrs={"contract_only_live_collection": True, "read_only": True},
        )
        self.last_policy = policy
        self._record_model("agent_observation_spine_policy_registered", "agent_observation_spine_policy", policy.policy_id, policy)
        return policy

    def register_runtime_descriptor(
        self,
        *,
        runtime_name: str = "generic_runtime",
        runtime_kind: str = "generic_agent_runtime",
        runtime_version: str | None = None,
        harness_family: str | None = None,
        supports_ocel_export: bool = False,
        supports_jsonl_transcript: bool = True,
        supports_tool_lifecycle_events: bool = False,
        supports_permission_events: bool = False,
        supports_sidecar_observation: bool = False,
        supports_event_bus: bool = False,
    ) -> AgentRuntimeDescriptor:
        descriptor = AgentRuntimeDescriptor(
            runtime_descriptor_id=new_agent_runtime_descriptor_id(),
            runtime_name=runtime_name,
            runtime_kind=runtime_kind,
            runtime_version=runtime_version,
            harness_family=harness_family,
            supports_ocel_export=supports_ocel_export,
            supports_jsonl_transcript=supports_jsonl_transcript,
            supports_tool_lifecycle_events=supports_tool_lifecycle_events,
            supports_permission_events=supports_permission_events,
            supports_sidecar_observation=supports_sidecar_observation,
            supports_event_bus=supports_event_bus,
            created_at=utc_now_iso(),
            runtime_attrs={"read_only": True},
        )
        self._record_model(
            "agent_runtime_descriptor_registered",
            "agent_runtime_descriptor",
            descriptor.runtime_descriptor_id,
            descriptor,
        )
        return descriptor

    def register_agent_instance(
        self,
        *,
        source_runtime: str = "generic_runtime",
        source_version: str | None = None,
        source_agent_id: str | None = None,
        source_agent_name: str | None = None,
        host_ref: str | None = None,
        workspace_ref: str | None = None,
        profile_ref: str | None = None,
        operator_ref: str | None = None,
        privacy_scope: str = "public_safe",
        trusted: bool = False,
    ) -> AgentInstance:
        instance = AgentInstance(
            agent_instance_id=new_agent_instance_id(),
            source_runtime=source_runtime,
            source_version=source_version,
            source_agent_id=source_agent_id,
            source_agent_name=source_agent_name,
            host_ref=host_ref,
            workspace_ref=workspace_ref,
            profile_ref=profile_ref,
            operator_ref=operator_ref,
            privacy_scope=privacy_scope,
            trusted=trusted,
            created_at=utc_now_iso(),
            instance_attrs={"read_only": True, "redacted": True},
        )
        self._record_model("agent_instance_registered", "agent_instance", instance.agent_instance_id, instance)
        return instance

    def create_environment_snapshot(
        self,
        *,
        agent_instance: AgentInstance,
        observed_run_id: str | None = None,
        runtime_kind: str = "generic_agent_runtime",
        workspace_ref: str | None = None,
        sandbox_enabled: bool = True,
        network_enabled: bool = False,
        shell_enabled: bool = False,
        write_enabled: bool = False,
        permission_mode: str = "read_only",
        model_ref: str | None = None,
        tool_surface_hash: str | None = None,
    ) -> RuntimeEnvironmentSnapshot:
        snapshot = RuntimeEnvironmentSnapshot(
            environment_snapshot_id=new_runtime_environment_snapshot_id(),
            agent_instance_id=agent_instance.agent_instance_id,
            observed_run_id=observed_run_id,
            runtime_kind=runtime_kind,
            workspace_ref=workspace_ref,
            sandbox_enabled=sandbox_enabled,
            network_enabled=network_enabled,
            shell_enabled=shell_enabled,
            write_enabled=write_enabled,
            permission_mode=permission_mode,
            model_ref=model_ref,
            tool_surface_hash=tool_surface_hash,
            created_at=utc_now_iso(),
            environment_attrs={"read_only": True, "snapshot_only": True},
        )
        self._record_model(
            "runtime_environment_snapshot_created",
            "runtime_environment_snapshot",
            snapshot.environment_snapshot_id,
            snapshot,
            object_links=[
                (
                    snapshot.environment_snapshot_id,
                    agent_instance.agent_instance_id,
                    "environment_snapshot_belongs_to_agent_instance",
                )
            ],
        )
        return snapshot

    def register_collector_contracts(self) -> list[AgentObservationCollectorContract]:
        specs = [
            ("batch_file", True, True, ["generic_jsonl", "ocel_like"]),
            ("tail_file", False, False, ["generic_jsonl"]),
            ("runtime_hook", False, False, ["runtime_event"]),
            ("event_bus", False, False, ["event_stream"]),
            ("sidecar", False, False, ["sidecar_event"]),
        ]
        self.last_collectors = [
            AgentObservationCollectorContract(
                collector_contract_id=new_agent_observation_collector_contract_id(),
                collector_kind=kind,
                implemented=implemented,
                enabled=enabled,
                source_kinds_supported=formats,
                output_event_schema_version="agent_observation_v2",
                requires_redaction_policy=True,
                created_at=utc_now_iso(),
                collector_attrs={
                    "live_collection": False if kind != "batch_file" else None,
                    "contract_only": not implemented,
                    "read_only": True,
                },
            )
            for kind, implemented, enabled, formats in specs
        ]
        for item in self.last_collectors:
            self._record_model(
                "agent_observation_collector_contract_registered",
                "agent_observation_collector_contract",
                item.collector_contract_id,
                item,
            )
        return list(self.last_collectors)

    def register_adapter_profiles(self) -> list[AgentObservationAdapterProfile]:
        specs = [
            ("ChantaCoreOCELAdapter", "chantacore", ["ocel_like"], True),
            ("GenericJSONLTranscriptAdapter", "generic_jsonl", ["jsonl"], True),
            ("SchumpeterAgentEventAdapter", "schumpeter_agent", ["jsonl"], False),
            ("OpenCodeToolLifecycleAdapter", "opencode", ["tool_lifecycle"], False),
            ("ClaudeCodeTranscriptAdapter", "claude_code", ["transcript"], False),
            ("CodexTaskLogAdapter", "codex_task_log", ["task_log"], False),
            ("OpenClawGatewayLogAdapter", "openclaw_gateway", ["gateway_log"], False),
            ("HermesMissionLogAdapter", "hermes_mission", ["mission_log"], False),
        ]
        self.last_adapters = [
            AgentObservationAdapterProfile(
                adapter_profile_id=new_agent_observation_adapter_profile_id(),
                adapter_name=name,
                source_runtime=runtime,
                supported_formats=formats,
                supported_event_types=["message", "tool", "permission", "gate", "outcome", "error"],
                confidence_policy="deterministic_adapter_confidence",
                schema_version="agent_observation_v2",
                adapter_version="0.19.6",
                implemented=implemented,
                created_at=utc_now_iso(),
                adapter_attrs={"contract_only": not implemented, "execution_enabled": False},
            )
            for name, runtime, formats, implemented in specs
        ]
        for item in self.last_adapters:
            self._record_model(
                "agent_observation_adapter_profile_registered",
                "agent_observation_adapter_profile",
                item.adapter_profile_id,
                item,
            )
        return list(self.last_adapters)

    def register_movement_ontology_terms(self) -> list[AgentMovementOntologyTerm]:
        self.last_terms = [
            AgentMovementOntologyTerm(
                ontology_term_id=new_agent_movement_ontology_term_id(),
                term_kind=kind,
                term_value=value,
                description=description,
                parent_term=parent,
                stable=True,
                created_at=utc_now_iso(),
                term_attrs={"schema_version": "agent_observation_v2"},
            )
            for kind, value, description, parent in default_ontology_specs()
        ]
        for term in self.last_terms:
            self._record_model(
                "agent_movement_ontology_term_registered",
                "agent_movement_ontology_term",
                term.ontology_term_id,
                term,
            )
        return list(self.last_terms)

    def normalize_event_v2(
        self,
        event: dict[str, Any],
        *,
        batch_id: str | None = None,
        source_runtime: str = "generic_jsonl",
        source_format: str = "generic_jsonl",
        adapter_version: str = "0.19.6",
    ) -> AgentObservationNormalizedEventV2:
        action, observed_activity, effect = _classify_event(event)
        confidence = _clamp_confidence(event.get("confidence"), 0.7)
        confidence_class = str(event.get("confidence_class") or "confirmed_observation")
        if confidence_class not in CONFIDENCE_CLASSES:
            confidence_class = "unknown"
        evidence_ref = str(event.get("evidence_ref") or event.get("id") or f"event:{uuid4()}")
        withdrawal = list(event.get("withdrawal_conditions") or ["Withdraw if source record is incomplete or contradicted."])
        normalized = AgentObservationNormalizedEventV2(
            normalized_event_id=new_agent_observation_normalized_event_v2_id(),
            batch_id=batch_id,
            source_event_id=str(event.get("id") or event.get("event_id") or "") or None,
            source_runtime=str(event.get("source_runtime") or source_runtime),
            source_format=str(event.get("source_format") or source_format),
            source_schema_version=str(event.get("schema_version") or event.get("source_schema_version") or "") or None,
            adapter_version=adapter_version,
            observed_activity=observed_activity,
            canonical_action_type=action,
            observed_timestamp=event.get("timestamp") or event.get("time"),
            actor_type=str(event.get("actor_type") or ("user" if event.get("role") == "user" else "agent")),
            actor_ref=event.get("actor_ref") or event.get("role"),
            object_refs=_event_object_refs(event),
            effect_type=effect,
            input_preview=_preview(event.get("input") or event.get("content")),
            output_preview=_preview(event.get("output") or event.get("result")),
            confidence=confidence,
            confidence_class=confidence_class,
            evidence_ref=evidence_ref,
            uncertainty_notes=list(event.get("uncertainty_notes") or []),
            withdrawal_conditions=withdrawal,
            created_at=utc_now_iso(),
            event_attrs={"redacted": True, "full_body_stored": False},
        )
        self.last_events.append(normalized)
        self._record_model(
            "agent_observation_event_v2_normalized",
            "agent_observation_normalized_event_v2",
            normalized.normalized_event_id,
            normalized,
        )
        return normalized

    def create_observed_objects(
        self,
        *,
        observed_run_id: str,
        events: list[AgentObservationNormalizedEventV2] | None = None,
    ) -> list[ObservedAgentObject]:
        selected_events = list(events or self.last_events)
        seen: set[str] = set()
        objects: list[ObservedAgentObject] = []
        for event in selected_events:
            for ref in event.object_refs:
                if ref in seen:
                    continue
                seen.add(ref)
                object_type = ref.split(":", 1)[0] if ":" in ref else "unknown_object"
                if object_type not in OBJECT_TYPES:
                    object_type = "unknown_object"
                item = ObservedAgentObject(
                    observed_object_id=new_observed_agent_object_id(),
                    observed_run_id=observed_run_id,
                    object_type=object_type,
                    object_ref=ref,
                    source_object_ref=ref,
                    confidence=min(event.confidence, 0.8),
                    evidence_refs=[event.evidence_ref] if event.evidence_ref else [],
                    created_at=utc_now_iso(),
                    object_attrs={"redacted": True},
                )
                objects.append(item)
                self._record_model("observed_agent_object_created", "observed_agent_object", item.observed_object_id, item)
        self.last_objects.extend(objects)
        return objects

    def create_observed_relations(
        self,
        *,
        observed_run_id: str,
        events: list[AgentObservationNormalizedEventV2] | None = None,
    ) -> list[ObservedAgentRelation]:
        selected_events = list(events or self.last_events)
        relations: list[ObservedAgentRelation] = []
        for left, right in zip(selected_events, selected_events[1:]):
            relation = ObservedAgentRelation(
                observed_relation_id=new_observed_agent_relation_id(),
                observed_run_id=observed_run_id,
                source_ref=left.normalized_event_id,
                target_ref=right.normalized_event_id,
                relation_type="followed_by",
                confidence=min(left.confidence, right.confidence, 0.75),
                causal_claim=False,
                evidence_refs=[ref for ref in [left.evidence_ref, right.evidence_ref] if ref],
                uncertainty_notes=["Temporal adjacency is not treated as causality."],
                created_at=utc_now_iso(),
                relation_attrs={"redacted": True},
            )
            relations.append(relation)
            self._record_model(
                "observed_agent_relation_created",
                "observed_agent_relation",
                relation.observed_relation_id,
                relation,
            )
        self.last_relations.extend(relations)
        return relations

    def create_behavior_inference_v2(
        self,
        *,
        observed_run: ObservedAgentRun,
        events: list[AgentObservationNormalizedEventV2] | None = None,
    ) -> AgentBehaviorInferenceV2:
        selected_events = list(events or self.last_events)
        actions = [event.canonical_action_type for event in selected_events]
        tools = [ref for event in selected_events for ref in event.object_refs if ref.startswith("tool:")]
        skills = [ref for event in selected_events for ref in event.object_refs if ref.startswith("skill:")]
        object_types = sorted({(ref.split(":", 1)[0] if ":" in ref else "unknown_object") for event in selected_events for ref in event.object_refs})
        failures = [event.observed_activity for event in selected_events if event.canonical_action_type == "recover_failure" or event.effect_type == "gate_blocked"]
        recoveries = [event.observed_activity for event in selected_events if event.canonical_action_type in {"recover_failure", "verify_result"}]
        inference = AgentBehaviorInferenceV2(
            inference_id=new_agent_behavior_inference_v2_id(),
            observed_run_id=observed_run.observed_run_id,
            inferred_goal="insufficient_evidence_for_goal" if not actions else "respond_to_observed_task",
            inferred_goal_confidence=0.45 if actions else 0.1,
            inferred_intent="derived_from_observed_sequence" if actions else None,
            inferred_task_type="agent_trace_review" if actions else None,
            inferred_action_sequence=actions,
            inferred_skill_sequence=skills,
            inferred_tool_sequence=tools,
            touched_object_types=object_types,
            effect_profile=sorted({event.effect_type for event in selected_events}),
            outcome_inference="outcome_requires_review",
            outcome_confidence=0.35,
            confirmed_observations=[f"Observed {event.canonical_action_type}." for event in selected_events],
            data_based_interpretations=["Action sequence was derived from normalized event types."] if actions else [],
            likely_hypotheses=["The agent was working through a task flow."] if len(actions) > 1 else [],
            estimates=[f"Observed event count is {len(selected_events)}."],
            unknown_or_needs_verification=["Goal, success, and causality require review."],
            failure_signals=failures,
            recovery_signals=recoveries,
            evidence_refs=[event.evidence_ref for event in selected_events if event.evidence_ref],
            uncertainty_notes=["Inference is deterministic and non-causal by default."],
            withdrawal_conditions=["Withdraw if normalized events are incomplete, contradicted, or misclassified."],
            created_at=utc_now_iso(),
            inference_attrs={"confidence_class": "behavior_inference", "causal_claims_made": False},
        )
        self.last_inference = inference
        self._record_model(
            "agent_behavior_inference_v2_created",
            "agent_behavior_inference_v2",
            inference.inference_id,
            inference,
        )
        return inference

    def create_observation_review(
        self,
        *,
        observed_run_id: str,
        inference_id: str | None = None,
        review_status: str = "pending_review",
        reviewer_type: str = "human",
        reviewer_id: str | None = None,
        decision: str = "no_decision",
        reason: str | None = None,
    ) -> AgentObservationReview:
        review = AgentObservationReview(
            review_id=new_agent_observation_review_id(),
            observed_run_id=observed_run_id,
            inference_id=inference_id,
            review_status=review_status,
            reviewer_type=reviewer_type,
            reviewer_id=reviewer_id,
            decision=decision,
            reason=reason,
            created_at=utc_now_iso(),
            review_attrs={"manual_review_required": True},
        )
        self._record_model("agent_observation_review_recorded", "agent_observation_review", review.review_id, review)
        return review

    def create_observation_correction(
        self,
        *,
        review_id: str,
        corrected_field: str,
        old_value: Any = None,
        new_value: Any = None,
        correction_reason: str | None = None,
    ) -> AgentObservationCorrection:
        correction = AgentObservationCorrection(
            correction_id=new_agent_observation_correction_id(),
            review_id=review_id,
            corrected_field=corrected_field,
            old_value_preview=_preview(old_value),
            new_value_preview=_preview(new_value),
            correction_reason=correction_reason,
            created_at=utc_now_iso(),
            correction_attrs={"full_body_stored": False},
        )
        self._record_model(
            "agent_observation_correction_recorded",
            "agent_observation_correction",
            correction.correction_id,
            correction,
        )
        return correction

    def create_redaction_policy(self) -> ObservationRedactionPolicy:
        policy = ObservationRedactionPolicy(
            redaction_policy_id=new_observation_redaction_policy_id(),
            policy_name="default_observation_redaction_policy",
            redact_private_paths=True,
            redact_full_bodies=True,
            redact_secrets=True,
            redact_user_identifiers=True,
            max_preview_chars=400,
            allowed_export_fields=[
                "normalized_event_id",
                "canonical_action_type",
                "effect_type",
                "confidence",
                "evidence_ref",
            ],
            denied_export_fields=["raw_transcript", "full_file_body", "secret", "user_identifier"],
            created_at=utc_now_iso(),
            policy_attrs={"default_safe": True},
        )
        self.last_redaction_policy = policy
        self._record_model("observation_redaction_policy_registered", "observation_redaction_policy", policy.redaction_policy_id, policy)
        return policy

    def create_export_policy(self) -> ObservationExportPolicy:
        policy = ObservationExportPolicy(
            export_policy_id=new_observation_export_policy_id(),
            policy_name="default_observation_export_policy",
            export_mode="redacted_summary_only",
            allow_raw_transcript_export=False,
            allow_full_file_body_export=False,
            allow_private_memory_export=False,
            require_operator_approval=True,
            require_redaction=True,
            created_at=utc_now_iso(),
            policy_attrs={"default_safe": True},
        )
        self.last_export_policy = policy
        self._record_model("observation_export_policy_registered", "observation_export_policy", policy.export_policy_id, policy)
        return policy

    def create_fleet_snapshot(
        self,
        *,
        agent_instances: list[AgentInstance] | None = None,
        observed_runs: list[ObservedAgentRun] | None = None,
        events: list[AgentObservationNormalizedEventV2] | None = None,
        observed_objects: list[ObservedAgentObject] | None = None,
        inferences: list[AgentBehaviorInferenceV2] | None = None,
    ) -> AgentFleetObservationSnapshot:
        agent_instances = list(agent_instances or [])
        observed_runs = list(observed_runs or [])
        events = list(events or self.last_events)
        observed_objects = list(observed_objects or self.last_objects)
        inferences = list(inferences or ([self.last_inference] if self.last_inference else []))
        snapshot = AgentFleetObservationSnapshot(
            fleet_snapshot_id=new_agent_fleet_observation_snapshot_id(),
            agent_instance_count=len(agent_instances),
            observed_run_count=len(observed_runs),
            source_runtime_counts=_count_values([agent.source_runtime for agent in agent_instances]),
            action_type_counts=_count_values([event.canonical_action_type for event in events]),
            object_type_counts=_count_values([obj.object_type for obj in observed_objects]),
            failure_signal_counts=_count_values([signal for inference in inferences for signal in inference.failure_signals]),
            candidate_pattern_count=sum(1 for event in events if event.effect_type in {"candidate_created", "state_candidate_created"}),
            created_at=utc_now_iso(),
            snapshot_attrs={"aggregate_only": True, "raw_body_stored": False},
        )
        self.last_fleet_snapshot = snapshot
        self._record_model(
            "agent_fleet_observation_snapshot_created",
            "agent_fleet_observation_snapshot",
            snapshot.fleet_snapshot_id,
            snapshot,
        )
        return snapshot

    def record_finding(
        self,
        *,
        subject_ref: str | None,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None = None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> AgentObservationSpineFinding:
        finding = AgentObservationSpineFinding(
            finding_id=new_agent_observation_spine_finding_id(),
            subject_ref=subject_ref,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            created_at=utc_now_iso(),
            finding_attrs=dict(finding_attrs or {}),
        )
        self.last_findings.append(finding)
        self._record_model(
            "agent_observation_spine_finding_recorded",
            "agent_observation_spine_finding",
            finding.finding_id,
            finding,
        )
        return finding

    def record_result(
        self,
        *,
        operation_kind: str,
        status: str,
        created_object_refs: list[str],
        summary: str,
    ) -> AgentObservationSpineResult:
        result = AgentObservationSpineResult(
            result_id=new_agent_observation_spine_result_id(),
            operation_kind=operation_kind,
            status=status,
            created_object_refs=list(created_object_refs),
            finding_ids=[finding.finding_id for finding in self.last_findings],
            summary=summary,
            created_at=utc_now_iso(),
            result_attrs={"read_only": True, "live_collection": False},
        )
        self.last_result = result
        self._record_model(
            "agent_observation_spine_result_recorded",
            "agent_observation_spine_result",
            result.result_id,
            result,
        )
        return result

    def render_spine_summary(self, value: Any | None = None) -> str:
        item = value or self.last_result or self.last_fleet_snapshot or self.last_inference
        data = item.to_dict() if hasattr(item, "to_dict") else dict(item or {})
        lines = ["Agent Observation Spine"]
        for key in ["status", "operation_kind", "summary", "inference_id", "fleet_snapshot_id"]:
            if data.get(key) is not None:
                lines.append(f"{key}={data[key]}")
        lines.append(f"ontology_term_count={len(self.last_terms)}")
        lines.append(f"adapter_profile_count={len(self.last_adapters)}")
        lines.append(f"collector_contract_count={len(self.last_collectors)}")
        lines.append(f"normalized_event_v2_count={len(self.last_events)}")
        lines.append("sidecar_enabled=false")
        lines.append("event_bus_enabled=false")
        lines.append("external_execution_used=false")
        return "\n".join(lines)

    def render_ontology_cli(self) -> str:
        if not self.last_terms:
            self.register_movement_ontology_terms()
        counts = _count_values([term.term_kind for term in self.last_terms])
        return "\n".join(
            [
                "Agent Movement Ontology",
                *(f"{key}_count={counts[key]}" for key in sorted(counts)),
                "stable=true",
            ]
        )

    def render_fleet_snapshot_cli(self, snapshot: AgentFleetObservationSnapshot | None = None) -> str:
        item = snapshot or self.last_fleet_snapshot or self.create_fleet_snapshot()
        return "\n".join(
            [
                "Agent Fleet Observation Snapshot",
                f"fleet_snapshot_id={item.fleet_snapshot_id}",
                f"agent_instance_count={item.agent_instance_count}",
                f"observed_run_count={item.observed_run_count}",
                f"candidate_pattern_count={item.candidate_pattern_count}",
                "aggregate_only=true",
            ]
        )

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        event_id = f"event:{uuid4()}"
        relations = [OCELRelation.event_object(event_id=event_id, object_id=object_id, qualifier=f"{object_type}_object")]
        for source_id, target_id, qualifier in object_links or []:
            relations.append(
                OCELRelation.object_object(
                    source_object_id=source_id,
                    target_object_id=target_id,
                    qualifier=qualifier,
                )
            )
        self.trace_service.record_session_ocel_record(
            OCELRecord(
                event=OCELEvent(
                    event_id=event_id,
                    event_activity=activity,
                    event_timestamp=utc_now_iso(),
                    event_attrs={"source": "agent_observation_spine", "read_only": True},
                ),
                objects=[OCELObject(object_id=object_id, object_type=object_type, object_attrs=model.to_dict())],
                relations=relations,
            )
        )


def _classify_event(event: dict[str, Any]) -> tuple[str, str, str]:
    role = event.get("role")
    if role == "user":
        return "observe_context", "user_message_observed", "read_only_observation"
    if role == "assistant":
        return "emit_response", "assistant_message_observed", "no_effect"
    if event.get("tool") or event.get("tool_call") or event.get("name"):
        return "invoke_tool", "tool_call_observed", "unknown_side_effect"
    if event.get("tool_result") or event.get("result") or event.get("output"):
        return "verify_result", "tool_result_observed", "read_only_observation"
    if event.get("permission"):
        return "request_permission", "permission_observed", "permission_requested"
    if event.get("gate"):
        return "gate_action", "gate_observed", "gate_blocked" if event.get("blocked") else "no_effect"
    if event.get("error"):
        return "recover_failure", "error_observed", "unknown_side_effect"
    return "unknown_action", "unknown_event_observed", "unknown_side_effect"


def _event_object_refs(event: dict[str, Any]) -> list[str]:
    refs = event.get("object_refs")
    if isinstance(refs, list):
        return [str(ref) for ref in refs]
    if event.get("tool") or event.get("name"):
        return [f"tool:{event.get('tool') or event.get('name')}"]
    if event.get("skill_id"):
        return [str(event["skill_id"])]
    if event.get("file"):
        return [f"file:{event['file']}"]
    if event.get("role"):
        return [f"message:{event.get('id') or event.get('role')}"]
    return ["unknown_object:unknown"]


def _count_values(values: list[str]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for value in values:
        key = str(value or "unknown")
        counts[key] = counts.get(key, 0) + 1
    return counts
