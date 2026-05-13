from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def clamp_confidence(value: float | int | None, default: float = 0.0) -> float:
    try:
        numeric = float(default if value is None else value)
    except (TypeError, ValueError):
        numeric = default
    return max(0.0, min(1.0, numeric))


@dataclass(frozen=True)
class AgentObservationSource:
    source_id: str
    source_name: str
    source_kind: str
    source_runtime: str
    source_version: str | None
    source_format: str
    location_ref: str | None
    collection_mode: str
    trusted: bool
    private: bool
    created_at: str
    source_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_id": self.source_id,
            "source_name": self.source_name,
            "source_kind": self.source_kind,
            "source_runtime": self.source_runtime,
            "source_version": self.source_version,
            "source_format": self.source_format,
            "location_ref": self.location_ref,
            "collection_mode": self.collection_mode,
            "trusted": self.trusted,
            "private": self.private,
            "created_at": self.created_at,
            "source_attrs": dict(self.source_attrs),
        }


@dataclass(frozen=True)
class AgentObservationBatch:
    batch_id: str
    source_id: str
    input_format: str
    raw_record_count: int
    normalized_event_count: int
    status: str
    confidence: float
    created_at: str
    batch_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "batch_id": self.batch_id,
            "source_id": self.source_id,
            "input_format": self.input_format,
            "raw_record_count": self.raw_record_count,
            "normalized_event_count": self.normalized_event_count,
            "status": self.status,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "batch_attrs": dict(self.batch_attrs),
        }


@dataclass(frozen=True)
class AgentObservationNormalizedEvent:
    normalized_event_id: str
    batch_id: str
    source_event_id: str | None
    source_runtime: str
    source_format: str
    observed_activity: str
    observed_timestamp: str | None
    actor_type: str | None
    actor_ref: str | None
    object_refs: list[str]
    input_preview: str | None
    output_preview: str | None
    confidence: float
    evidence_ref: str | None
    uncertainty_notes: list[str]
    created_at: str
    event_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "normalized_event_id": self.normalized_event_id,
            "batch_id": self.batch_id,
            "source_event_id": self.source_event_id,
            "source_runtime": self.source_runtime,
            "source_format": self.source_format,
            "observed_activity": self.observed_activity,
            "observed_timestamp": self.observed_timestamp,
            "actor_type": self.actor_type,
            "actor_ref": self.actor_ref,
            "object_refs": list(self.object_refs),
            "input_preview": self.input_preview,
            "output_preview": self.output_preview,
            "confidence": self.confidence,
            "evidence_ref": self.evidence_ref,
            "uncertainty_notes": list(self.uncertainty_notes),
            "created_at": self.created_at,
            "event_attrs": dict(self.event_attrs),
        }


@dataclass(frozen=True)
class ObservedAgentRun:
    observed_run_id: str
    source_id: str
    batch_id: str
    source_agent_id: str | None
    source_session_id: str | None
    inferred_runtime: str
    event_count: int
    object_count: int
    relation_count: int
    observation_confidence: float
    created_at: str
    run_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "observation_confidence", clamp_confidence(self.observation_confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "observed_run_id": self.observed_run_id,
            "source_id": self.source_id,
            "batch_id": self.batch_id,
            "source_agent_id": self.source_agent_id,
            "source_session_id": self.source_session_id,
            "inferred_runtime": self.inferred_runtime,
            "event_count": self.event_count,
            "object_count": self.object_count,
            "relation_count": self.relation_count,
            "observation_confidence": self.observation_confidence,
            "created_at": self.created_at,
            "run_attrs": dict(self.run_attrs),
        }


@dataclass(frozen=True)
class AgentBehaviorInference:
    inference_id: str
    observed_run_id: str
    inferred_goal: str | None
    inferred_goal_confidence: float
    inferred_task_type: str | None
    inferred_action_sequence: list[str]
    inferred_skill_sequence: list[str]
    inferred_tool_sequence: list[str]
    touched_object_types: list[str]
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
        object.__setattr__(self, "inferred_goal_confidence", clamp_confidence(self.inferred_goal_confidence))
        object.__setattr__(self, "outcome_confidence", clamp_confidence(self.outcome_confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "inference_id": self.inference_id,
            "observed_run_id": self.observed_run_id,
            "inferred_goal": self.inferred_goal,
            "inferred_goal_confidence": self.inferred_goal_confidence,
            "inferred_task_type": self.inferred_task_type,
            "inferred_action_sequence": list(self.inferred_action_sequence),
            "inferred_skill_sequence": list(self.inferred_skill_sequence),
            "inferred_tool_sequence": list(self.inferred_tool_sequence),
            "touched_object_types": list(self.touched_object_types),
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
class AgentProcessNarrative:
    narrative_id: str
    observed_run_id: str
    inference_id: str
    title: str
    concise_summary: str
    timeline: list[str]
    key_actions: list[str]
    key_objects: list[str]
    blocked_or_failed_steps: list[str]
    inferred_outcome: str | None
    confidence: float
    created_at: str
    narrative_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "narrative_id": self.narrative_id,
            "observed_run_id": self.observed_run_id,
            "inference_id": self.inference_id,
            "title": self.title,
            "concise_summary": self.concise_summary,
            "timeline": list(self.timeline),
            "key_actions": list(self.key_actions),
            "key_objects": list(self.key_objects),
            "blocked_or_failed_steps": list(self.blocked_or_failed_steps),
            "inferred_outcome": self.inferred_outcome,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "narrative_attrs": dict(self.narrative_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillSourceDescriptor:
    source_descriptor_id: str
    source_kind: str
    source_runtime: str
    vendor_hint: str | None
    source_root_ref: str | None
    detected_files: list[str]
    detected_manifest_refs: list[str]
    confidence: float
    created_at: str
    descriptor_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "source_descriptor_id": self.source_descriptor_id,
            "source_kind": self.source_kind,
            "source_runtime": self.source_runtime,
            "vendor_hint": self.vendor_hint,
            "source_root_ref": self.source_root_ref,
            "detected_files": list(self.detected_files),
            "detected_manifest_refs": list(self.detected_manifest_refs),
            "confidence": self.confidence,
            "created_at": self.created_at,
            "descriptor_attrs": dict(self.descriptor_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillStaticProfile:
    static_profile_id: str
    source_descriptor_id: str
    declared_name: str | None
    declared_description: str | None
    declared_tools: list[str]
    declared_inputs: list[str]
    declared_outputs: list[str]
    declared_risks: list[str]
    instruction_preview: str | None
    confidence: float
    created_at: str
    profile_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "static_profile_id": self.static_profile_id,
            "source_descriptor_id": self.source_descriptor_id,
            "declared_name": self.declared_name,
            "declared_description": self.declared_description,
            "declared_tools": list(self.declared_tools),
            "declared_inputs": list(self.declared_inputs),
            "declared_outputs": list(self.declared_outputs),
            "declared_risks": list(self.declared_risks),
            "instruction_preview": self.instruction_preview,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "profile_attrs": dict(self.profile_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillBehaviorFingerprint:
    fingerprint_id: str
    observed_run_id: str
    source_runtime: str
    source_skill_name: str | None
    source_tool_name: str | None
    observed_event_count: int
    observed_sequence: list[str]
    object_types_touched: list[str]
    input_shape_summary: dict[str, Any]
    output_shape_summary: dict[str, Any]
    side_effect_profile: str
    permission_profile: str
    verification_profile: str
    failure_modes: list[str]
    recovery_patterns: list[str]
    recommended_chantacore_category: str
    risk_class: str
    confidence: float
    evidence_refs: list[str]
    created_at: str
    fingerprint_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "fingerprint_id": self.fingerprint_id,
            "observed_run_id": self.observed_run_id,
            "source_runtime": self.source_runtime,
            "source_skill_name": self.source_skill_name,
            "source_tool_name": self.source_tool_name,
            "observed_event_count": self.observed_event_count,
            "observed_sequence": list(self.observed_sequence),
            "object_types_touched": list(self.object_types_touched),
            "input_shape_summary": dict(self.input_shape_summary),
            "output_shape_summary": dict(self.output_shape_summary),
            "side_effect_profile": self.side_effect_profile,
            "permission_profile": self.permission_profile,
            "verification_profile": self.verification_profile,
            "failure_modes": list(self.failure_modes),
            "recovery_patterns": list(self.recovery_patterns),
            "recommended_chantacore_category": self.recommended_chantacore_category,
            "risk_class": self.risk_class,
            "confidence": self.confidence,
            "evidence_refs": list(self.evidence_refs),
            "created_at": self.created_at,
            "fingerprint_attrs": dict(self.fingerprint_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillAssimilationCandidate:
    candidate_id: str
    source_runtime: str
    source_skill_ref: str | None
    source_kind: str
    static_profile_id: str | None
    behavior_fingerprint_id: str | None
    proposed_chantacore_skill_id: str
    proposed_execution_type: str
    adapter_candidate_ids: list[str]
    risk_class: str
    confidence: float
    evidence_refs: list[str]
    created_at: str
    review_status: str = "pending_review"
    canonical_import_enabled: bool = False
    execution_enabled: bool = False
    candidate_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))
        if self.canonical_import_enabled is not False:
            raise ValueError("canonical_import_enabled must default to False")
        if self.execution_enabled is not False:
            raise ValueError("execution_enabled must default to False")

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "source_runtime": self.source_runtime,
            "source_skill_ref": self.source_skill_ref,
            "source_kind": self.source_kind,
            "static_profile_id": self.static_profile_id,
            "behavior_fingerprint_id": self.behavior_fingerprint_id,
            "proposed_chantacore_skill_id": self.proposed_chantacore_skill_id,
            "proposed_execution_type": self.proposed_execution_type,
            "adapter_candidate_ids": list(self.adapter_candidate_ids),
            "risk_class": self.risk_class,
            "confidence": self.confidence,
            "evidence_refs": list(self.evidence_refs),
            "review_status": self.review_status,
            "canonical_import_enabled": self.canonical_import_enabled,
            "execution_enabled": self.execution_enabled,
            "created_at": self.created_at,
            "candidate_attrs": dict(self.candidate_attrs),
        }


@dataclass(frozen=True)
class ExternalSkillAdapterCandidate:
    adapter_candidate_id: str
    source_skill_ref: str | None
    target_skill_id: str
    mapping_type: str
    mapping_confidence: float
    required_input_mapping: dict[str, Any]
    output_mapping: dict[str, Any]
    unsupported_features: list[str]
    created_at: str
    requires_review: bool = True
    execution_enabled: bool = False
    adapter_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "mapping_confidence", clamp_confidence(self.mapping_confidence))
        if self.execution_enabled is not False:
            raise ValueError("execution_enabled must default to False")

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_candidate_id": self.adapter_candidate_id,
            "source_skill_ref": self.source_skill_ref,
            "target_skill_id": self.target_skill_id,
            "mapping_type": self.mapping_type,
            "mapping_confidence": self.mapping_confidence,
            "required_input_mapping": dict(self.required_input_mapping),
            "output_mapping": dict(self.output_mapping),
            "unsupported_features": list(self.unsupported_features),
            "requires_review": self.requires_review,
            "execution_enabled": self.execution_enabled,
            "created_at": self.created_at,
            "adapter_attrs": dict(self.adapter_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionFinding:
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
class ObservationDigestionResult:
    result_id: str
    operation_kind: str
    subject_ref: str | None
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
            "subject_ref": self.subject_ref,
            "status": self.status,
            "created_object_refs": list(self.created_object_refs),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }
