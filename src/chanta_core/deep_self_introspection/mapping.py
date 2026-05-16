from __future__ import annotations

from chanta_core.deep_self_introspection.models import DeepSelfIntrospectionOCELMapping


DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES = [
    "deep_self_introspection_layer",
    "deep_self_introspection_contract",
    "deep_self_introspection_subject",
    "deep_self_introspection_skill_contract",
    "deep_self_introspection_risk_profile",
    "deep_self_introspection_gate_contract",
    "deep_self_introspection_observability_contract",
    "deep_self_introspection_report",
    "capability_registry_subject",
    "runtime_boundary_subject",
    "policy_gate_subject",
    "trace_integrity_subject",
    "context_projection_subject",
    "candidate_memory_boundary_subject",
    "self_claim_consistency_subject",
    "self_awareness_ecosystem_snapshot",
    "self_awareness_consolidation_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
    "capability_registry",
    "capability_record",
    "capability_registry_snapshot",
    "capability_truth_report",
    "capability_truth_finding",
    "capability_risk_profile_view",
    "capability_gate_view",
    "capability_observability_view",
    "skill_contract",
    "self_awareness_capability",
    "external_candidate_capability",
]

DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES = [
    "deep_self_introspection_layer_registered",
    "deep_self_introspection_contract_registered",
    "deep_self_introspection_subject_registered",
    "deep_self_introspection_contract_checked",
    "deep_self_introspection_conformance_report_created",
    "deep_self_introspection_pig_report_created",
    "deep_self_introspection_ocpx_projection_created",
    "deep_self_capability_registry_view_requested",
    "deep_self_capability_registry_snapshot_created",
    "deep_self_capability_risk_view_created",
    "deep_self_capability_gate_view_created",
    "deep_self_capability_observability_view_created",
    "deep_self_capability_truth_check_requested",
    "deep_self_capability_truth_report_created",
    "deep_self_capability_truth_warning_created",
    "deep_self_capability_truth_violation_detected",
]

DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES = [
    "declares_introspection_subject",
    "maps_subject_to_ocel_object",
    "maps_subject_to_ocel_event",
    "maps_subject_to_ocel_relation",
    "requires_source_object",
    "requires_read_model",
    "requires_pig_projection",
    "requires_ocpx_projection",
    "checks_contract",
    "visible_in_workbench",
    "derived_from_self_awareness_consolidation",
    "recorded_in_envelope",
    "views_capability_registry",
    "contains_capability",
    "describes_skill_contract",
    "has_risk_view",
    "has_gate_view",
    "has_observability_view",
    "checks_capability_truth",
    "finds_capability_issue",
    "contradicts_claim",
    "verified_by_registry",
    "derived_from_deep_self_contract",
]

DEEP_SELF_INTROSPECTION_EFFECT_TYPES = [
    "read_only_observation",
    "state_candidate_created",
]

DEEP_SELF_INTROSPECTION_SOURCE_OBJECT_TYPES = [
    "self_awareness_ecosystem_snapshot",
    "self_awareness_consolidation_report",
    "self_awareness_workbench_snapshot",
    "directed_intention_candidate_bundle",
    "surface_verification_report",
    "project_structure_candidate",
]

DEEP_SELF_INTROSPECTION_READ_MODEL_TYPES = [
    "SelfAwarenessReleaseState",
    "SelfAwarenessWorkbenchState",
    "SelfIntentionCandidateState",
    "SelfVerificationState",
    "SelfProjectSurfaceState",
    "SelfCapabilityTruthState",
    "SelfRuntimeBoundaryState",
    "SelfPolicyGateState",
    "SelfTraceIntegrityState",
    "SelfContextProjectionState",
    "SelfCandidateMemoryBoundaryState",
    "SelfClaimConsistencyState",
]

DEEP_SELF_INTROSPECTION_OCEL_MAPPING = DeepSelfIntrospectionOCELMapping(
    object_types=DEEP_SELF_INTROSPECTION_OCEL_OBJECT_TYPES,
    event_types=DEEP_SELF_INTROSPECTION_OCEL_EVENT_TYPES,
    relation_types=DEEP_SELF_INTROSPECTION_OCEL_RELATION_TYPES,
    effect_types=DEEP_SELF_INTROSPECTION_EFFECT_TYPES,
    source_object_types=DEEP_SELF_INTROSPECTION_SOURCE_OBJECT_TYPES,
    read_model_types=DEEP_SELF_INTROSPECTION_READ_MODEL_TYPES,
)
