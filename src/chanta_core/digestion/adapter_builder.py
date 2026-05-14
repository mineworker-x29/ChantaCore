from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from chanta_core.context.history import ContextHistoryEntry, new_context_history_entry_id
from chanta_core.observation import AgentBehaviorInferenceV2
from chanta_core.observation_digest import ExternalSkillBehaviorFingerprint, ObservedAgentRun
from chanta_core.observation_digest.models import clamp_confidence
from chanta_core.ocel.models import OCELEvent, OCELObject, OCELRecord, OCELRelation
from chanta_core.ocel.store import OCELStore
from chanta_core.skills.ids import (
    new_adapter_input_mapping_spec_id,
    new_adapter_output_mapping_spec_id,
    new_adapter_unsupported_feature_id,
    new_chantacore_target_skill_candidate_id,
    new_observation_digestion_adapter_build_result_id,
    new_observation_digestion_adapter_candidate_id,
    new_observation_digestion_adapter_finding_id,
    new_observation_digestion_adapter_review_request_id,
    new_observation_to_digestion_adapter_policy_id,
    new_observed_capability_candidate_id,
)
from chanta_core.traces.trace_service import TraceService
from chanta_core.utility.time import utc_now_iso


ADAPTER_BUILDER_SOURCE = "observation_to_digestion_adapter_builder"

SUPPORTED_TARGETS: dict[str, tuple[str, str, str]] = {
    "read_file": ("skill:read_workspace_text_file", "read_only_workspace", "workspace_read"),
    "search_file": ("skill:grep_workspace_text", "read_only_workspace", "workspace_search"),
    "summarize_content": ("skill:summarize_workspace_markdown", "read_only_workspace", "workspace_summary"),
    "create_candidate": ("skill:external_skill_assimilate", "digestion", "candidate_creation"),
    "verify_result": ("skill:observation_digest_conformance", "digestion", "verification"),
    "delegate_task": ("skill:delegation_packet_review", "future_track", "delegation_review"),
    "observation": ("skill:agent_behavior_infer", "observation", "behavior_inference"),
    "digestion": ("skill:external_skill_static_digest", "digestion", "static_digest"),
}

UNSUPPORTED_FUTURE_TRACKS: dict[str, str] = {
    "shell_execution": "v0.20+ shell safety track",
    "write_file": "v0.20+ write/apply_patch safety track",
    "network_access": "v0.20+ network safety track",
    "mcp_connection": "v0.20+ MCP safety track",
    "plugin_loading": "v0.20+ plugin safety track",
    "external_harness_execution": "v0.20+ external harness sandbox track",
}

UNSUPPORTED_CATEGORIES = set(UNSUPPORTED_FUTURE_TRACKS)


@dataclass(frozen=True)
class ObservationToDigestionAdapterPolicy:
    policy_id: str
    policy_name: str
    allowed_source_kinds: list[str]
    allowed_target_skill_layers: list[str]
    denied_target_capabilities: list[str]
    allow_auto_adapter_activation: bool = False
    allow_canonical_skill_import: bool = False
    allow_execution_enablement: bool = False
    require_review: bool = True
    require_evidence_refs: bool = True
    require_confidence: bool = True
    require_withdrawal_conditions: bool = True
    min_mapping_confidence_for_candidate: float = 0.35
    max_adapter_candidates_per_run: int = 8
    status: str = "active"
    created_at: str = field(default_factory=utc_now_iso)
    policy_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(
            self,
            "min_mapping_confidence_for_candidate",
            clamp_confidence(self.min_mapping_confidence_for_candidate, 0.35),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "policy_id": self.policy_id,
            "policy_name": self.policy_name,
            "allowed_source_kinds": list(self.allowed_source_kinds),
            "allowed_target_skill_layers": list(self.allowed_target_skill_layers),
            "denied_target_capabilities": list(self.denied_target_capabilities),
            "allow_auto_adapter_activation": self.allow_auto_adapter_activation,
            "allow_canonical_skill_import": self.allow_canonical_skill_import,
            "allow_execution_enablement": self.allow_execution_enablement,
            "require_review": self.require_review,
            "require_evidence_refs": self.require_evidence_refs,
            "require_confidence": self.require_confidence,
            "require_withdrawal_conditions": self.require_withdrawal_conditions,
            "min_mapping_confidence_for_candidate": self.min_mapping_confidence_for_candidate,
            "max_adapter_candidates_per_run": self.max_adapter_candidates_per_run,
            "status": self.status,
            "created_at": self.created_at,
            "policy_attrs": dict(self.policy_attrs),
        }


@dataclass(frozen=True)
class ObservedCapabilityCandidate:
    observed_capability_id: str
    observed_run_id: str | None
    inference_id: str | None
    fingerprint_id: str | None
    capability_name: str
    capability_category: str
    observed_action_sequence: list[str]
    observed_object_types: list[str]
    observed_effect_profile: list[str]
    observed_input_shape: dict[str, Any]
    observed_output_shape: dict[str, Any]
    risk_class: str
    confidence: float
    evidence_refs: list[str]
    withdrawal_conditions: list[str]
    created_at: str
    capability_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "observed_capability_id": self.observed_capability_id,
            "observed_run_id": self.observed_run_id,
            "inference_id": self.inference_id,
            "fingerprint_id": self.fingerprint_id,
            "capability_name": self.capability_name,
            "capability_category": self.capability_category,
            "observed_action_sequence": list(self.observed_action_sequence),
            "observed_object_types": list(self.observed_object_types),
            "observed_effect_profile": list(self.observed_effect_profile),
            "observed_input_shape": dict(self.observed_input_shape),
            "observed_output_shape": dict(self.observed_output_shape),
            "risk_class": self.risk_class,
            "confidence": self.confidence,
            "evidence_refs": list(self.evidence_refs),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "created_at": self.created_at,
            "capability_attrs": dict(self.capability_attrs),
        }


@dataclass(frozen=True)
class ChantaCoreTargetSkillCandidate:
    target_candidate_id: str
    observed_capability_id: str
    target_skill_id: str
    target_skill_layer: str
    target_capability_category: str
    match_reason: str
    match_confidence: float
    supported_now: bool
    requires_future_track: bool
    created_at: str
    target_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "match_confidence", clamp_confidence(self.match_confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "target_candidate_id": self.target_candidate_id,
            "observed_capability_id": self.observed_capability_id,
            "target_skill_id": self.target_skill_id,
            "target_skill_layer": self.target_skill_layer,
            "target_capability_category": self.target_capability_category,
            "match_reason": self.match_reason,
            "match_confidence": self.match_confidence,
            "supported_now": self.supported_now,
            "requires_future_track": self.requires_future_track,
            "created_at": self.created_at,
            "target_attrs": dict(self.target_attrs),
        }


@dataclass(frozen=True)
class AdapterInputMappingSpec:
    input_mapping_id: str
    adapter_candidate_id: str
    source_input_shape: dict[str, Any]
    target_input_schema: dict[str, Any]
    field_mappings: dict[str, str]
    missing_required_fields: list[str]
    default_values: dict[str, Any]
    transformation_notes: list[str]
    confidence: float
    created_at: str
    input_mapping_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "input_mapping_id": self.input_mapping_id,
            "adapter_candidate_id": self.adapter_candidate_id,
            "source_input_shape": dict(self.source_input_shape),
            "target_input_schema": dict(self.target_input_schema),
            "field_mappings": dict(self.field_mappings),
            "missing_required_fields": list(self.missing_required_fields),
            "default_values": dict(self.default_values),
            "transformation_notes": list(self.transformation_notes),
            "confidence": self.confidence,
            "created_at": self.created_at,
            "input_mapping_attrs": dict(self.input_mapping_attrs),
        }


@dataclass(frozen=True)
class AdapterOutputMappingSpec:
    output_mapping_id: str
    adapter_candidate_id: str
    source_output_shape: dict[str, Any]
    target_output_schema: dict[str, Any]
    field_mappings: dict[str, str]
    unsupported_output_fields: list[str]
    preview_strategy: str
    confidence: float
    created_at: str
    output_mapping_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "confidence", clamp_confidence(self.confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "output_mapping_id": self.output_mapping_id,
            "adapter_candidate_id": self.adapter_candidate_id,
            "source_output_shape": dict(self.source_output_shape),
            "target_output_schema": dict(self.target_output_schema),
            "field_mappings": dict(self.field_mappings),
            "unsupported_output_fields": list(self.unsupported_output_fields),
            "preview_strategy": self.preview_strategy,
            "confidence": self.confidence,
            "created_at": self.created_at,
            "output_mapping_attrs": dict(self.output_mapping_attrs),
        }


@dataclass(frozen=True)
class AdapterUnsupportedFeature:
    unsupported_feature_id: str
    adapter_candidate_id: str
    observed_capability_id: str
    feature_type: str
    severity: str
    message: str
    future_track_hint: str
    evidence_refs: list[str]
    created_at: str
    feature_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "unsupported_feature_id": self.unsupported_feature_id,
            "adapter_candidate_id": self.adapter_candidate_id,
            "observed_capability_id": self.observed_capability_id,
            "feature_type": self.feature_type,
            "severity": self.severity,
            "message": self.message,
            "future_track_hint": self.future_track_hint,
            "evidence_refs": list(self.evidence_refs),
            "created_at": self.created_at,
            "feature_attrs": dict(self.feature_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionAdapterCandidate:
    adapter_candidate_id: str
    observed_capability_id: str
    target_candidate_id: str
    source_runtime: str | None
    source_skill_ref: str | None
    source_tool_ref: str | None
    target_skill_id: str
    mapping_type: str
    mapping_confidence: float
    input_mapping_id: str
    output_mapping_id: str
    unsupported_feature_ids: list[str]
    risk_class: str
    review_status: str = "pending_review"
    requires_review: bool = True
    canonical_import_enabled: bool = False
    execution_enabled: bool = False
    created_at: str = field(default_factory=utc_now_iso)
    adapter_attrs: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        object.__setattr__(self, "mapping_confidence", clamp_confidence(self.mapping_confidence))

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter_candidate_id": self.adapter_candidate_id,
            "observed_capability_id": self.observed_capability_id,
            "target_candidate_id": self.target_candidate_id,
            "source_runtime": self.source_runtime,
            "source_skill_ref": self.source_skill_ref,
            "source_tool_ref": self.source_tool_ref,
            "target_skill_id": self.target_skill_id,
            "mapping_type": self.mapping_type,
            "mapping_confidence": self.mapping_confidence,
            "input_mapping_id": self.input_mapping_id,
            "output_mapping_id": self.output_mapping_id,
            "unsupported_feature_ids": list(self.unsupported_feature_ids),
            "risk_class": self.risk_class,
            "review_status": self.review_status,
            "requires_review": self.requires_review,
            "canonical_import_enabled": self.canonical_import_enabled,
            "execution_enabled": self.execution_enabled,
            "created_at": self.created_at,
            "adapter_attrs": dict(self.adapter_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionAdapterReviewRequest:
    review_request_id: str
    adapter_candidate_id: str
    requested_by: str
    review_reason: str
    status: str
    created_at: str
    request_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "review_request_id": self.review_request_id,
            "adapter_candidate_id": self.adapter_candidate_id,
            "requested_by": self.requested_by,
            "review_reason": self.review_reason,
            "status": self.status,
            "created_at": self.created_at,
            "request_attrs": dict(self.request_attrs),
        }


@dataclass(frozen=True)
class ObservationDigestionAdapterFinding:
    finding_id: str
    subject_ref: str
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
class ObservationDigestionAdapterBuildResult:
    build_result_id: str
    operation_kind: str
    status: str
    observed_run_id: str | None
    inference_id: str | None
    observed_capability_ids: list[str]
    target_candidate_ids: list[str]
    adapter_candidate_ids: list[str]
    unsupported_feature_ids: list[str]
    finding_ids: list[str]
    summary: str
    created_at: str
    result_attrs: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "build_result_id": self.build_result_id,
            "operation_kind": self.operation_kind,
            "status": self.status,
            "observed_run_id": self.observed_run_id,
            "inference_id": self.inference_id,
            "observed_capability_ids": list(self.observed_capability_ids),
            "target_candidate_ids": list(self.target_candidate_ids),
            "adapter_candidate_ids": list(self.adapter_candidate_ids),
            "unsupported_feature_ids": list(self.unsupported_feature_ids),
            "finding_ids": list(self.finding_ids),
            "summary": self.summary,
            "created_at": self.created_at,
            "result_attrs": dict(self.result_attrs),
        }


class ObservationToDigestionAdapterBuilderService:
    def __init__(self, trace_service: TraceService | None = None, ocel_store: OCELStore | None = None) -> None:
        self.trace_service = trace_service or TraceService(ocel_store=ocel_store or OCELStore())
        self.last_policy: ObservationToDigestionAdapterPolicy | None = None
        self.last_observed_capabilities: list[ObservedCapabilityCandidate] = []
        self.last_target_candidates: list[ChantaCoreTargetSkillCandidate] = []
        self.last_input_mappings: list[AdapterInputMappingSpec] = []
        self.last_output_mappings: list[AdapterOutputMappingSpec] = []
        self.last_unsupported_features: list[AdapterUnsupportedFeature] = []
        self.last_adapter_candidates: list[ObservationDigestionAdapterCandidate] = []
        self.last_review_requests: list[ObservationDigestionAdapterReviewRequest] = []
        self.last_findings: list[ObservationDigestionAdapterFinding] = []
        self.last_result: ObservationDigestionAdapterBuildResult | None = None

    def create_default_policy(self, **overrides: Any) -> ObservationToDigestionAdapterPolicy:
        payload = {
            "policy_id": new_observation_to_digestion_adapter_policy_id(),
            "policy_name": "default_observation_to_digestion_adapter_policy",
            "allowed_source_kinds": ["behavior_inference_v2", "behavior_fingerprint", "observed_agent_run"],
            "allowed_target_skill_layers": ["read_only_workspace", "observation", "digestion", "future_track"],
            "denied_target_capabilities": sorted(UNSUPPORTED_CATEGORIES),
            "allow_auto_adapter_activation": False,
            "allow_canonical_skill_import": False,
            "allow_execution_enablement": False,
            "require_review": True,
            "require_evidence_refs": True,
            "require_confidence": True,
            "require_withdrawal_conditions": True,
            "min_mapping_confidence_for_candidate": 0.35,
            "max_adapter_candidates_per_run": 8,
            "status": "active",
            "created_at": utc_now_iso(),
            "policy_attrs": {"read_only": True, "deterministic_mapping": True},
        }
        payload.update(overrides)
        policy = ObservationToDigestionAdapterPolicy(**payload)
        self.last_policy = policy
        self._record_model(
            "observation_to_digestion_adapter_policy_registered",
            "observation_to_digestion_adapter_policy",
            policy.policy_id,
            policy,
        )
        return policy

    def extract_observed_capabilities(
        self,
        *,
        inference: AgentBehaviorInferenceV2 | None = None,
        fingerprint: ExternalSkillBehaviorFingerprint | None = None,
        observed_run: ObservedAgentRun | None = None,
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> list[ObservedCapabilityCandidate]:
        source_kind = self._source_kind(inference=inference, fingerprint=fingerprint, observed_run=observed_run)
        effective_policy = policy or self.last_policy or self.create_default_policy()
        if source_kind not in effective_policy.allowed_source_kinds:
            self.record_finding(
                subject_ref=source_kind,
                finding_type="source_kind_not_allowed",
                status="open",
                severity="high",
                message=f"Source kind is not allowed by policy: {source_kind}",
                evidence_ref=None,
            )
            return []

        source = self._source_profile(inference=inference, fingerprint=fingerprint, observed_run=observed_run)
        categories = self._categories_from_signals(
            source["action_sequence"],
            source["object_types"],
            source["effect_profile"],
            source["extra_text"],
            source.get("recommended_category"),
        )
        if not categories:
            categories = ["verify_result"]

        candidates: list[ObservedCapabilityCandidate] = []
        for category in categories[: effective_policy.max_adapter_candidates_per_run]:
            candidate = ObservedCapabilityCandidate(
                observed_capability_id=new_observed_capability_candidate_id(),
                observed_run_id=source["observed_run_id"],
                inference_id=source["inference_id"],
                fingerprint_id=source["fingerprint_id"],
                capability_name=f"observed_{category}",
                capability_category=category,
                observed_action_sequence=source["action_sequence"],
                observed_object_types=source["object_types"],
                observed_effect_profile=source["effect_profile"],
                observed_input_shape=source["input_shape"],
                observed_output_shape=source["output_shape"],
                risk_class=self._risk_class_for(category, source["risk_class"]),
                confidence=source["confidence"],
                evidence_refs=source["evidence_refs"],
                withdrawal_conditions=source["withdrawal_conditions"],
                created_at=utc_now_iso(),
                capability_attrs={"source_kind": source_kind, "read_only": True},
            )
            self.last_observed_capabilities.append(candidate)
            candidates.append(candidate)
            links = []
            object_links = []
            if candidate.inference_id:
                links.append(("agent_behavior_inference_v2_object", candidate.inference_id))
                object_links.append(
                    (
                        candidate.observed_capability_id,
                        candidate.inference_id,
                        "observed_capability_derived_from_behavior_inference",
                    )
                )
            if candidate.fingerprint_id:
                links.append(("external_skill_behavior_fingerprint_object", candidate.fingerprint_id))
                object_links.append(
                    (
                        candidate.observed_capability_id,
                        candidate.fingerprint_id,
                        "observed_capability_derived_from_fingerprint",
                    )
                )
            self._record_model(
                "observed_capability_candidate_created",
                "observed_capability_candidate",
                candidate.observed_capability_id,
                candidate,
                links=links,
                object_links=object_links,
            )
        return candidates

    def match_target_skills(
        self,
        capabilities: list[ObservedCapabilityCandidate],
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> list[ChantaCoreTargetSkillCandidate]:
        effective_policy = policy or self.last_policy or self.create_default_policy()
        targets: list[ChantaCoreTargetSkillCandidate] = []
        for capability in capabilities:
            unsupported = capability.capability_category in UNSUPPORTED_CATEGORIES
            skill_id, layer, target_category = self._target_for_category(capability.capability_category)
            confidence = self._match_confidence(capability, unsupported=unsupported)
            target = ChantaCoreTargetSkillCandidate(
                target_candidate_id=new_chantacore_target_skill_candidate_id(),
                observed_capability_id=capability.observed_capability_id,
                target_skill_id=skill_id,
                target_skill_layer=layer,
                target_capability_category=target_category,
                match_reason=self._match_reason(capability.capability_category, unsupported),
                match_confidence=confidence,
                supported_now=not unsupported,
                requires_future_track=unsupported,
                created_at=utc_now_iso(),
                target_attrs={"policy_id": effective_policy.policy_id, "deterministic": True},
            )
            self.last_target_candidates.append(target)
            targets.append(target)
            self._record_model(
                "chantacore_target_skill_candidate_created",
                "chantacore_target_skill_candidate",
                target.target_candidate_id,
                target,
                links=[("observed_capability_candidate_object", capability.observed_capability_id)],
                object_links=[
                    (
                        target.target_candidate_id,
                        capability.observed_capability_id,
                        "target_skill_candidate_maps_observed_capability",
                    )
                ],
            )
            if confidence < effective_policy.min_mapping_confidence_for_candidate:
                self.record_finding(
                    subject_ref=target.target_candidate_id,
                    finding_type="low_mapping_confidence",
                    status="open",
                    severity="medium",
                    message=(
                        f"Mapping confidence {confidence:.2f} is below policy threshold "
                        f"{effective_policy.min_mapping_confidence_for_candidate:.2f}."
                    ),
                    evidence_ref=(capability.evidence_refs[0] if capability.evidence_refs else None),
                )
        return targets

    def create_input_mapping_spec(
        self,
        *,
        adapter_candidate_id: str,
        capability: ObservedCapabilityCandidate,
        target: ChantaCoreTargetSkillCandidate,
    ) -> AdapterInputMappingSpec:
        required = self._required_input_fields(capability.capability_category)
        source_shape = dict(capability.observed_input_shape)
        missing = [field_name for field_name in required if field_name not in source_shape]
        mappings = {field_name: field_name for field_name in required if field_name in source_shape}
        spec = AdapterInputMappingSpec(
            input_mapping_id=new_adapter_input_mapping_spec_id(),
            adapter_candidate_id=adapter_candidate_id,
            source_input_shape=source_shape,
            target_input_schema={"target_skill_id": target.target_skill_id, "required_fields": required},
            field_mappings=mappings,
            missing_required_fields=missing,
            default_values={"read_only": True},
            transformation_notes=[
                "Mapping is a reviewable candidate only.",
                "No source behavior is replayed during mapping.",
            ],
            confidence=max(0.0, target.match_confidence - (0.05 * len(missing))),
            created_at=utc_now_iso(),
            input_mapping_attrs={"read_only": True},
        )
        self.last_input_mappings.append(spec)
        self._record_model(
            "adapter_input_mapping_spec_created",
            "adapter_input_mapping_spec",
            spec.input_mapping_id,
            spec,
            links=[("observation_digestion_adapter_candidate_object", adapter_candidate_id)],
            object_links=[(spec.input_mapping_id, adapter_candidate_id, "input_mapping_belongs_to_adapter_candidate")],
        )
        return spec

    def create_output_mapping_spec(
        self,
        *,
        adapter_candidate_id: str,
        capability: ObservedCapabilityCandidate,
        target: ChantaCoreTargetSkillCandidate,
    ) -> AdapterOutputMappingSpec:
        source_shape = dict(capability.observed_output_shape)
        unsupported = sorted(set(source_shape) & {"side_effect", "permission_change", "external_result"})
        spec = AdapterOutputMappingSpec(
            output_mapping_id=new_adapter_output_mapping_spec_id(),
            adapter_candidate_id=adapter_candidate_id,
            source_output_shape=source_shape,
            target_output_schema={"target_skill_id": target.target_skill_id, "fields": ["summary", "evidence_refs"]},
            field_mappings={key: key for key in source_shape if key not in unsupported},
            unsupported_output_fields=unsupported,
            preview_strategy="redacted_summary_only",
            confidence=max(0.0, target.match_confidence - (0.05 * len(unsupported))),
            created_at=utc_now_iso(),
            output_mapping_attrs={"read_only": True},
        )
        self.last_output_mappings.append(spec)
        self._record_model(
            "adapter_output_mapping_spec_created",
            "adapter_output_mapping_spec",
            spec.output_mapping_id,
            spec,
            links=[("observation_digestion_adapter_candidate_object", adapter_candidate_id)],
            object_links=[(spec.output_mapping_id, adapter_candidate_id, "output_mapping_belongs_to_adapter_candidate")],
        )
        return spec

    def detect_unsupported_features(
        self,
        *,
        adapter_candidate_id: str,
        capability: ObservedCapabilityCandidate,
    ) -> list[AdapterUnsupportedFeature]:
        if capability.capability_category not in UNSUPPORTED_CATEGORIES:
            return []
        feature = AdapterUnsupportedFeature(
            unsupported_feature_id=new_adapter_unsupported_feature_id(),
            adapter_candidate_id=adapter_candidate_id,
            observed_capability_id=capability.observed_capability_id,
            feature_type=capability.capability_category,
            severity="high",
            message=f"Observed capability requires unsupported feature: {capability.capability_category}.",
            future_track_hint=UNSUPPORTED_FUTURE_TRACKS[capability.capability_category],
            evidence_refs=list(capability.evidence_refs),
            created_at=utc_now_iso(),
            feature_attrs={"review_required": True},
        )
        self.last_unsupported_features.append(feature)
        self._record_model(
            "adapter_unsupported_feature_recorded",
            "adapter_unsupported_feature",
            feature.unsupported_feature_id,
            feature,
            links=[("observation_digestion_adapter_candidate_object", adapter_candidate_id)],
            object_links=[
                (
                    feature.unsupported_feature_id,
                    adapter_candidate_id,
                    "unsupported_feature_belongs_to_adapter_candidate",
                )
            ],
        )
        return [feature]

    def create_adapter_candidate(
        self,
        *,
        capability: ObservedCapabilityCandidate,
        target: ChantaCoreTargetSkillCandidate,
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> ObservationDigestionAdapterCandidate | None:
        effective_policy = policy or self.last_policy or self.create_default_policy()
        if target.match_confidence < effective_policy.min_mapping_confidence_for_candidate:
            return None
        adapter_candidate_id = new_observation_digestion_adapter_candidate_id()
        input_mapping = self.create_input_mapping_spec(
            adapter_candidate_id=adapter_candidate_id,
            capability=capability,
            target=target,
        )
        output_mapping = self.create_output_mapping_spec(
            adapter_candidate_id=adapter_candidate_id,
            capability=capability,
            target=target,
        )
        unsupported_features = self.detect_unsupported_features(
            adapter_candidate_id=adapter_candidate_id,
            capability=capability,
        )
        mapping_confidence = min(target.match_confidence, input_mapping.confidence, output_mapping.confidence)
        candidate = ObservationDigestionAdapterCandidate(
            adapter_candidate_id=adapter_candidate_id,
            observed_capability_id=capability.observed_capability_id,
            target_candidate_id=target.target_candidate_id,
            source_runtime=capability.capability_attrs.get("source_runtime"),
            source_skill_ref=capability.capability_attrs.get("source_skill_ref"),
            source_tool_ref=capability.capability_attrs.get("source_tool_ref"),
            target_skill_id=target.target_skill_id,
            mapping_type="future_track_required" if unsupported_features else "observed_behavior_to_skill_candidate",
            mapping_confidence=mapping_confidence,
            input_mapping_id=input_mapping.input_mapping_id,
            output_mapping_id=output_mapping.output_mapping_id,
            unsupported_feature_ids=[item.unsupported_feature_id for item in unsupported_features],
            risk_class=capability.risk_class,
            review_status="pending_review",
            requires_review=True,
            canonical_import_enabled=False,
            execution_enabled=False,
            created_at=utc_now_iso(),
            adapter_attrs={"policy_id": effective_policy.policy_id, "candidate_only": True, "read_only": True},
        )
        self.last_adapter_candidates.append(candidate)
        self._record_model(
            "observation_digestion_adapter_candidate_created",
            "observation_digestion_adapter_candidate",
            candidate.adapter_candidate_id,
            candidate,
            links=[
                ("observed_capability_candidate_object", capability.observed_capability_id),
                ("chantacore_target_skill_candidate_object", target.target_candidate_id),
            ],
            object_links=[
                (
                    candidate.adapter_candidate_id,
                    capability.observed_capability_id,
                    "adapter_candidate_uses_observed_capability",
                ),
                (
                    candidate.adapter_candidate_id,
                    target.target_candidate_id,
                    "adapter_candidate_targets_skill_candidate",
                ),
            ],
        )
        return candidate

    def create_review_request(
        self,
        candidate: ObservationDigestionAdapterCandidate,
        *,
        requested_by: str = ADAPTER_BUILDER_SOURCE,
        review_reason: str | None = None,
    ) -> ObservationDigestionAdapterReviewRequest:
        request = ObservationDigestionAdapterReviewRequest(
            review_request_id=new_observation_digestion_adapter_review_request_id(),
            adapter_candidate_id=candidate.adapter_candidate_id,
            requested_by=requested_by,
            review_reason=review_reason or "Adapter candidates require review before any future activation path.",
            status="pending_review",
            created_at=utc_now_iso(),
            request_attrs={"canonical_import_enabled": False, "execution_enabled": False},
        )
        self.last_review_requests.append(request)
        self._record_model(
            "observation_digestion_adapter_review_requested",
            "observation_digestion_adapter_review_request",
            request.review_request_id,
            request,
            links=[("observation_digestion_adapter_candidate_object", candidate.adapter_candidate_id)],
            object_links=[(request.review_request_id, candidate.adapter_candidate_id, "review_request_reviews_adapter_candidate")],
        )
        return request

    def build_from_behavior_inference(
        self,
        inference: AgentBehaviorInferenceV2,
        *,
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> ObservationDigestionAdapterBuildResult:
        return self._build(operation_kind="from_behavior_inference", inference=inference, policy=policy)

    def build_from_behavior_fingerprint(
        self,
        fingerprint: ExternalSkillBehaviorFingerprint,
        *,
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> ObservationDigestionAdapterBuildResult:
        return self._build(operation_kind="from_behavior_fingerprint", fingerprint=fingerprint, policy=policy)

    def build_from_observed_run(
        self,
        observed_run: ObservedAgentRun,
        *,
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> ObservationDigestionAdapterBuildResult:
        return self._build(operation_kind="from_observed_run", observed_run=observed_run, policy=policy)

    def record_finding(
        self,
        *,
        subject_ref: str,
        finding_type: str,
        status: str,
        severity: str,
        message: str,
        evidence_ref: str | None,
        finding_attrs: dict[str, Any] | None = None,
    ) -> ObservationDigestionAdapterFinding:
        finding = ObservationDigestionAdapterFinding(
            finding_id=new_observation_digestion_adapter_finding_id(),
            subject_ref=subject_ref,
            finding_type=finding_type,
            status=status,
            severity=severity,
            message=message,
            evidence_ref=evidence_ref,
            created_at=utc_now_iso(),
            finding_attrs=finding_attrs or {},
        )
        self.last_findings.append(finding)
        self._record_model(
            "observation_digestion_adapter_finding_recorded",
            "observation_digestion_adapter_finding",
            finding.finding_id,
            finding,
            object_links=[(finding.finding_id, subject_ref, "finding_belongs_to_adapter_build")],
        )
        return finding

    def record_result(
        self,
        *,
        operation_kind: str,
        status: str,
        observed_run_id: str | None,
        inference_id: str | None,
        summary: str,
    ) -> ObservationDigestionAdapterBuildResult:
        result = ObservationDigestionAdapterBuildResult(
            build_result_id=new_observation_digestion_adapter_build_result_id(),
            operation_kind=operation_kind,
            status=status,
            observed_run_id=observed_run_id,
            inference_id=inference_id,
            observed_capability_ids=[item.observed_capability_id for item in self.last_observed_capabilities],
            target_candidate_ids=[item.target_candidate_id for item in self.last_target_candidates],
            adapter_candidate_ids=[item.adapter_candidate_id for item in self.last_adapter_candidates],
            unsupported_feature_ids=[item.unsupported_feature_id for item in self.last_unsupported_features],
            finding_ids=[item.finding_id for item in self.last_findings],
            summary=summary,
            created_at=utc_now_iso(),
            result_attrs={
                "canonical_import_enabled": False,
                "execution_enabled": False,
                "review_required": True,
            },
        )
        self.last_result = result
        object_links = [
            (result.build_result_id, adapter.adapter_candidate_id, "build_result_summarizes_adapter_build")
            for adapter in self.last_adapter_candidates
        ]
        object_links.extend(
            (result.build_result_id, finding.finding_id, "finding_belongs_to_adapter_build")
            for finding in self.last_findings
        )
        self._record_model(
            "observation_digestion_adapter_build_result_recorded",
            "observation_digestion_adapter_build_result",
            result.build_result_id,
            result,
            object_links=object_links,
        )
        return result

    def render_adapter_build_cli(
        self,
        result: ObservationDigestionAdapterBuildResult | None = None,
    ) -> str:
        active_result = result or self.last_result
        lines = ["Observation-to-Digestion Adapter Build"]
        if active_result:
            lines.append(f"status={active_result.status}")
            lines.append(f"result_id={active_result.build_result_id}")
            lines.append(f"summary={active_result.summary}")
        lines.append(f"observed_capabilities={len(self.last_observed_capabilities)}")
        for capability in self.last_observed_capabilities:
            lines.append(
                f"- observed_capability {capability.observed_capability_id} "
                f"category={capability.capability_category} confidence={capability.confidence:.2f}"
            )
        lines.append(f"target_skill_candidates={len(self.last_target_candidates)}")
        for target in self.last_target_candidates:
            lines.append(
                f"- target_candidate {target.target_candidate_id} target_skill_id={target.target_skill_id} "
                f"supported_now={str(target.supported_now).lower()}"
            )
        lines.append(f"adapter_candidates={len(self.last_adapter_candidates)}")
        for candidate in self.last_adapter_candidates:
            lines.append(
                f"- adapter_candidate {candidate.adapter_candidate_id} target_skill_id={candidate.target_skill_id} "
                f"review_status={candidate.review_status} "
                f"canonical_import_enabled={str(candidate.canonical_import_enabled).lower()} "
                f"execution_enabled={str(candidate.execution_enabled).lower()}"
            )
        lines.append(f"unsupported_features={len(self.last_unsupported_features)}")
        for feature in self.last_unsupported_features:
            lines.append(f"- unsupported {feature.feature_type} future_track={feature.future_track_hint}")
        lines.append("review_status=pending_review")
        lines.append("canonical_import_enabled=false")
        lines.append("execution_enabled=false")
        return "\n".join(lines)

    def _build(
        self,
        *,
        operation_kind: str,
        inference: AgentBehaviorInferenceV2 | None = None,
        fingerprint: ExternalSkillBehaviorFingerprint | None = None,
        observed_run: ObservedAgentRun | None = None,
        policy: ObservationToDigestionAdapterPolicy | None = None,
    ) -> ObservationDigestionAdapterBuildResult:
        self._clear_last_build()
        effective_policy = policy or self.create_default_policy()
        capabilities = self.extract_observed_capabilities(
            inference=inference,
            fingerprint=fingerprint,
            observed_run=observed_run,
            policy=effective_policy,
        )
        targets = self.match_target_skills(capabilities, policy=effective_policy)
        target_by_capability = {item.observed_capability_id: item for item in targets}
        for capability in capabilities:
            target = target_by_capability.get(capability.observed_capability_id)
            if target is None:
                continue
            candidate = self.create_adapter_candidate(capability=capability, target=target, policy=effective_policy)
            if candidate is not None:
                self.create_review_request(candidate)
        status = "completed" if capabilities else "no_capabilities"
        observed_run_id = (
            getattr(inference, "observed_run_id", None)
            or getattr(fingerprint, "observed_run_id", None)
            or getattr(observed_run, "observed_run_id", None)
        )
        inference_id = getattr(inference, "inference_id", None)
        return self.record_result(
            operation_kind=operation_kind,
            status=status,
            observed_run_id=observed_run_id,
            inference_id=inference_id,
            summary=(
                f"capabilities={len(self.last_observed_capabilities)} "
                f"targets={len(self.last_target_candidates)} adapters={len(self.last_adapter_candidates)} "
                f"unsupported={len(self.last_unsupported_features)}"
            ),
        )

    def _clear_last_build(self) -> None:
        self.last_observed_capabilities = []
        self.last_target_candidates = []
        self.last_input_mappings = []
        self.last_output_mappings = []
        self.last_unsupported_features = []
        self.last_adapter_candidates = []
        self.last_review_requests = []
        self.last_findings = []
        self.last_result = None

    def _record_model(
        self,
        activity: str,
        object_type: str,
        object_id: str,
        model: Any,
        *,
        links: list[tuple[str, str]] | None = None,
        object_links: list[tuple[str, str, str]] | None = None,
    ) -> None:
        event_id = f"event:{uuid4()}"
        objects = [OCELObject(object_id=object_id, object_type=object_type, object_attrs=model.to_dict())]
        relations = [
            OCELRelation.event_object(event_id=event_id, object_id=object_id, qualifier=f"{object_type}_object")
        ]
        for _, linked_object_id in links or []:
            relations.append(
                OCELRelation.event_object(
                    event_id=event_id,
                    object_id=linked_object_id,
                    qualifier="related_object",
                )
            )
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
                    event_attrs={"source": ADAPTER_BUILDER_SOURCE, "read_only": True, "candidate_only": True},
                ),
                objects=objects,
                relations=relations,
            )
        )

    @staticmethod
    def _source_kind(
        *,
        inference: AgentBehaviorInferenceV2 | None,
        fingerprint: ExternalSkillBehaviorFingerprint | None,
        observed_run: ObservedAgentRun | None,
    ) -> str:
        if inference is not None:
            return "behavior_inference_v2"
        if fingerprint is not None:
            return "behavior_fingerprint"
        if observed_run is not None:
            return "observed_agent_run"
        return "unknown"

    @staticmethod
    def _source_profile(
        *,
        inference: AgentBehaviorInferenceV2 | None,
        fingerprint: ExternalSkillBehaviorFingerprint | None,
        observed_run: ObservedAgentRun | None,
    ) -> dict[str, Any]:
        if inference is not None:
            action_sequence = _list_strings(
                [*inference.inferred_action_sequence, *inference.inferred_skill_sequence, *inference.inferred_tool_sequence]
            )
            return {
                "observed_run_id": inference.observed_run_id,
                "inference_id": inference.inference_id,
                "fingerprint_id": None,
                "action_sequence": action_sequence,
                "object_types": _list_strings(inference.touched_object_types),
                "effect_profile": _list_strings(inference.effect_profile),
                "input_shape": {"action_sequence": "list", "object_refs": "list"},
                "output_shape": {"outcome_inference": "text", "evidence_refs": "list"},
                "risk_class": "medium" if inference.failure_signals else "low",
                "confidence": min(inference.inferred_goal_confidence, inference.outcome_confidence),
                "evidence_refs": _list_strings(inference.evidence_refs) or [inference.inference_id],
                "withdrawal_conditions": _list_strings(inference.withdrawal_conditions)
                or ["Withdraw if source inference is corrected or evidence refs are invalidated."],
                "recommended_category": None,
                "extra_text": " ".join(
                    _list_strings(
                        [
                            inference.inferred_intent or "",
                            inference.inferred_task_type or "",
                            inference.outcome_inference or "",
                            *inference.confirmed_observations,
                        ]
                    )
                ),
            }
        if fingerprint is not None:
            return {
                "observed_run_id": fingerprint.observed_run_id,
                "inference_id": None,
                "fingerprint_id": fingerprint.fingerprint_id,
                "action_sequence": _list_strings(fingerprint.observed_sequence),
                "object_types": _list_strings(fingerprint.object_types_touched),
                "effect_profile": _list_strings(
                    [fingerprint.side_effect_profile, fingerprint.permission_profile, fingerprint.verification_profile]
                ),
                "input_shape": dict(fingerprint.input_shape_summary),
                "output_shape": dict(fingerprint.output_shape_summary),
                "risk_class": fingerprint.risk_class,
                "confidence": fingerprint.confidence,
                "evidence_refs": _list_strings(fingerprint.evidence_refs) or [fingerprint.fingerprint_id],
                "withdrawal_conditions": ["Withdraw if behavior fingerprint is superseded by reviewed observation."],
                "recommended_category": fingerprint.recommended_chantacore_category,
                "extra_text": " ".join(
                    _list_strings(
                        [
                            fingerprint.source_runtime,
                            fingerprint.source_skill_name or "",
                            fingerprint.source_tool_name or "",
                            fingerprint.side_effect_profile,
                            fingerprint.permission_profile,
                            fingerprint.verification_profile,
                        ]
                    )
                ),
                "source_runtime": fingerprint.source_runtime,
                "source_skill_ref": fingerprint.source_skill_name,
                "source_tool_ref": fingerprint.source_tool_name,
            }
        run_attrs = dict(observed_run.run_attrs) if observed_run is not None else {}
        action_sequence = _list_strings(
            run_attrs.get("observed_sequence")
            or run_attrs.get("inferred_action_sequence")
            or run_attrs.get("action_sequence")
            or run_attrs.get("activities")
            or []
        )
        object_types = _list_strings(run_attrs.get("object_types_touched") or run_attrs.get("object_types") or [])
        effect_profile = _list_strings(run_attrs.get("effect_profile") or run_attrs.get("effects") or [])
        return {
            "observed_run_id": getattr(observed_run, "observed_run_id", None),
            "inference_id": None,
            "fingerprint_id": None,
            "action_sequence": action_sequence,
            "object_types": object_types,
            "effect_profile": effect_profile,
            "input_shape": dict(run_attrs.get("input_shape") or {"observed_run": "summary"}),
            "output_shape": dict(run_attrs.get("output_shape") or {"observation": "summary"}),
            "risk_class": str(run_attrs.get("risk_class") or "medium"),
            "confidence": getattr(observed_run, "observation_confidence", 0.0),
            "evidence_refs": [getattr(observed_run, "observed_run_id", "observed_run:unknown")],
            "withdrawal_conditions": ["Withdraw if observed run summary is replaced by higher fidelity trace data."],
            "recommended_category": run_attrs.get("recommended_chantacore_category"),
            "extra_text": " ".join(_list_strings([str(value) for value in run_attrs.values()])),
            "source_runtime": getattr(observed_run, "inferred_runtime", None),
            "source_skill_ref": None,
            "source_tool_ref": None,
        }

    @staticmethod
    def _categories_from_signals(
        action_sequence: list[str],
        object_types: list[str],
        effect_profile: list[str],
        extra_text: str,
        recommended_category: str | None = None,
    ) -> list[str]:
        blob = " ".join([*action_sequence, *object_types, *effect_profile, extra_text, recommended_category or ""]).lower()
        categories: list[str] = []
        checks = [
            ("network_access", ["external_system_touched", "http", "url", "network"]),
            ("mcp_connection", ["mcp", "server", "tool resource"]),
            ("plugin_loading", ["plugin", "load", "extension"]),
            ("write_file", ["workspace_file_changed", "write", "edit", "patch"]),
            ("shell_execution", ["execute_action", "shell", "command"]),
            ("read_file", ["read_object", "file_read_observed"]),
            ("search_file", ["search_object", "file_search_observed"]),
            ("summarize_content", ["summarize_object", "summary_observed"]),
            ("create_candidate", ["create_candidate"]),
            ("verify_result", ["verify_result"]),
            ("delegate_task", ["delegate_task"]),
            ("observation", ["agent_trace_observe", "agent_behavior_infer"]),
            ("digestion", ["external_skill_static_digest", "external_skill_assimilate"]),
        ]
        for category, hints in checks:
            if any(hint in blob for hint in hints):
                categories.append(category)
        return _dedupe(categories)

    @staticmethod
    def _risk_class_for(category: str, source_risk: str | None) -> str:
        if category in UNSUPPORTED_CATEGORIES:
            return "high"
        if source_risk in {"low", "medium", "high", "critical"}:
            return str(source_risk)
        return "low"

    @staticmethod
    def _target_for_category(category: str) -> tuple[str, str, str]:
        if category in SUPPORTED_TARGETS:
            return SUPPORTED_TARGETS[category]
        if category in UNSUPPORTED_CATEGORIES:
            return (f"future:{category}", "future_track", category)
        return ("future:review_required", "future_track", category)

    @staticmethod
    def _match_confidence(capability: ObservedCapabilityCandidate, *, unsupported: bool) -> float:
        base = capability.confidence
        if unsupported:
            return max(0.35, min(base, 0.55))
        return min(1.0, max(0.0, base * 0.95))

    @staticmethod
    def _match_reason(category: str, unsupported: bool) -> str:
        if unsupported:
            return f"Category {category} is recognized but requires a future safety track."
        return f"Category {category} matched by deterministic observation-to-digestion rule."

    @staticmethod
    def _required_input_fields(category: str) -> list[str]:
        if category == "read_file":
            return ["root_ref", "relative_path"]
        if category == "search_file":
            return ["root_ref", "query"]
        if category == "summarize_content":
            return ["content_ref"]
        return ["observed_capability_id"]


def behavior_inference_v2_from_dict(data: dict[str, Any]) -> AgentBehaviorInferenceV2:
    return AgentBehaviorInferenceV2(
        inference_id=str(data.get("inference_id") or "agent_behavior_inference_v2:loaded"),
        observed_run_id=str(data.get("observed_run_id") or "observed_agent_run:loaded"),
        inferred_goal=data.get("inferred_goal"),
        inferred_goal_confidence=clamp_confidence(data.get("inferred_goal_confidence"), 0.0),
        inferred_intent=data.get("inferred_intent"),
        inferred_task_type=data.get("inferred_task_type"),
        inferred_action_sequence=_list_strings(data.get("inferred_action_sequence")),
        inferred_skill_sequence=_list_strings(data.get("inferred_skill_sequence")),
        inferred_tool_sequence=_list_strings(data.get("inferred_tool_sequence")),
        touched_object_types=_list_strings(data.get("touched_object_types")),
        effect_profile=_list_strings(data.get("effect_profile")),
        outcome_inference=data.get("outcome_inference"),
        outcome_confidence=clamp_confidence(data.get("outcome_confidence"), 0.0),
        confirmed_observations=_list_strings(data.get("confirmed_observations")),
        data_based_interpretations=_list_strings(data.get("data_based_interpretations")),
        likely_hypotheses=_list_strings(data.get("likely_hypotheses")),
        estimates=_list_strings(data.get("estimates")),
        unknown_or_needs_verification=_list_strings(data.get("unknown_or_needs_verification")),
        failure_signals=_list_strings(data.get("failure_signals")),
        recovery_signals=_list_strings(data.get("recovery_signals")),
        evidence_refs=_list_strings(data.get("evidence_refs")),
        uncertainty_notes=_list_strings(data.get("uncertainty_notes")),
        withdrawal_conditions=_list_strings(data.get("withdrawal_conditions")),
        created_at=str(data.get("created_at") or utc_now_iso()),
        inference_attrs=dict(data.get("inference_attrs") or {}),
    )


def observed_capability_candidates_to_history_entries(
    candidates: list[ObservedCapabilityCandidate],
) -> list[ContextHistoryEntry]:
    return [
        _history_entry(
            content=f"Observed capability candidate: {item.capability_category}\nConfidence: {item.confidence:.2f}",
            created_at=item.created_at,
            priority=85 if item.capability_category in UNSUPPORTED_CATEGORIES else 55,
            refs=[{"ref_type": "observed_capability_candidate", "ref_id": item.observed_capability_id}],
            attrs={"observed_capability_id": item.observed_capability_id, "category": item.capability_category},
        )
        for item in candidates
    ]


def target_skill_candidates_to_history_entries(
    candidates: list[ChantaCoreTargetSkillCandidate],
) -> list[ContextHistoryEntry]:
    return [
        _history_entry(
            content=f"Target skill candidate: {item.target_skill_id}\nSupported now: {item.supported_now}",
            created_at=item.created_at,
            priority=70 if item.requires_future_track else 55,
            refs=[{"ref_type": "chantacore_target_skill_candidate", "ref_id": item.target_candidate_id}],
            attrs={"target_candidate_id": item.target_candidate_id, "target_skill_id": item.target_skill_id},
        )
        for item in candidates
    ]


def adapter_candidates_to_history_entries(
    candidates: list[ObservationDigestionAdapterCandidate],
) -> list[ContextHistoryEntry]:
    return [
        _history_entry(
            content=f"Observation digestion adapter candidate: {item.target_skill_id}\nReview: {item.review_status}",
            created_at=item.created_at,
            priority=70 if item.review_status == "pending_review" else 55,
            refs=[{"ref_type": "observation_digestion_adapter_candidate", "ref_id": item.adapter_candidate_id}],
            attrs={
                "adapter_candidate_id": item.adapter_candidate_id,
                "review_status": item.review_status,
                "canonical_import_enabled": item.canonical_import_enabled,
                "execution_enabled": item.execution_enabled,
            },
        )
        for item in candidates
    ]


def unsupported_features_to_history_entries(features: list[AdapterUnsupportedFeature]) -> list[ContextHistoryEntry]:
    return [
        _history_entry(
            content=f"Unsupported adapter feature: {item.feature_type}\n{item.future_track_hint}",
            created_at=item.created_at,
            priority=90 if item.severity in {"high", "critical"} else 75,
            refs=[{"ref_type": "adapter_unsupported_feature", "ref_id": item.unsupported_feature_id}],
            attrs={"unsupported_feature_id": item.unsupported_feature_id, "feature_type": item.feature_type},
        )
        for item in features
    ]


def adapter_build_results_to_history_entries(
    results: list[ObservationDigestionAdapterBuildResult],
) -> list[ContextHistoryEntry]:
    return [
        _history_entry(
            content=f"Adapter build result: {item.operation_kind}\n{item.summary}",
            created_at=item.created_at,
            priority=55 if item.status == "completed" else 70,
            refs=[{"ref_type": "observation_digestion_adapter_build_result", "ref_id": item.build_result_id}],
            attrs={"build_result_id": item.build_result_id, "status": item.status},
        )
        for item in results
    ]


def adapter_findings_to_history_entries(findings: list[ObservationDigestionAdapterFinding]) -> list[ContextHistoryEntry]:
    return [
        _history_entry(
            content=f"Adapter builder finding: {item.finding_type}\n{item.message}",
            created_at=item.created_at,
            priority=70 if item.severity == "medium" else 85,
            refs=[{"ref_type": "observation_digestion_adapter_finding", "ref_id": item.finding_id}],
            attrs={"finding_id": item.finding_id, "severity": item.severity, "status": item.status},
        )
        for item in findings
    ]


def _history_entry(
    *,
    content: str,
    created_at: str,
    priority: int,
    refs: list[dict[str, Any]],
    attrs: dict[str, Any],
) -> ContextHistoryEntry:
    return ContextHistoryEntry(
        entry_id=new_context_history_entry_id(),
        session_id=None,
        process_instance_id=None,
        role="context",
        content=content,
        created_at=created_at,
        source=ADAPTER_BUILDER_SOURCE,
        priority=priority,
        refs=refs,
        entry_attrs=attrs,
    )


def _list_strings(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value] if value else []
    if isinstance(value, (list, tuple, set)):
        return [str(item) for item in value if str(item)]
    return [str(value)]


def _dedupe(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value not in seen:
            seen.add(value)
            result.append(value)
    return result
