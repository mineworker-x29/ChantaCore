from __future__ import annotations

from chanta_core.deep_self_introspection.mapping import (
    DEEP_SELF_INTROSPECTION_OCEL_MAPPING,
)
from chanta_core.deep_self_introspection.models import (
    DEEP_SELF_INTROSPECTION_LAYER,
    DEEP_SELF_INTROSPECTION_VERSION,
    DeepSelfIntrospectionContract,
    DeepSelfIntrospectionGateContract,
    DeepSelfIntrospectionObservabilityContract,
    DeepSelfIntrospectionRiskProfile,
    DeepSelfIntrospectionSubject,
)


DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS = [
    "subject:capability_registry",
    "subject:runtime_boundary",
    "subject:policy_gate",
    "subject:trace_integrity",
    "subject:context_projection",
    "subject:candidate_memory_boundary",
    "subject:self_claim_consistency",
]

DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS = [
    "skill:deep_self_capability_registry_view",
    "skill:deep_self_runtime_boundary_view",
    "skill:deep_self_policy_gate_map",
    "skill:deep_self_trace_integrity_check",
    "skill:deep_self_context_projection_view",
    "skill:deep_self_candidate_memory_boundary_report",
    "skill:deep_self_claim_consistency_check",
]

_SUBJECT_OBJECT_TYPE = {
    "subject:capability_registry": "capability_registry_subject",
    "subject:runtime_boundary": "runtime_boundary_subject",
    "subject:policy_gate": "policy_gate_subject",
    "subject:trace_integrity": "trace_integrity_subject",
    "subject:context_projection": "context_projection_subject",
    "subject:candidate_memory_boundary": "candidate_memory_boundary_subject",
    "subject:self_claim_consistency": "self_claim_consistency_subject",
}

_SUBJECT_READ_MODEL = {
    "subject:capability_registry": "SelfCapabilityTruthState",
    "subject:runtime_boundary": "SelfRuntimeBoundaryState",
    "subject:policy_gate": "SelfPolicyGateState",
    "subject:trace_integrity": "SelfTraceIntegrityState",
    "subject:context_projection": "SelfContextProjectionState",
    "subject:candidate_memory_boundary": "SelfCandidateMemoryBoundaryState",
    "subject:self_claim_consistency": "SelfClaimConsistencyState",
}

_SUBJECT_DESCRIPTION = {
    "subject:capability_registry": "Contract for later capability registry truth awareness.",
    "subject:runtime_boundary": "Contract for later runtime boundary awareness.",
    "subject:policy_gate": "Contract for later policy and gate consistency mapping.",
    "subject:trace_integrity": "Contract for later OCEL trace integrity checking.",
    "subject:context_projection": "Contract for later context projection awareness.",
    "subject:candidate_memory_boundary": "Contract for later candidate and memory boundary checks.",
    "subject:self_claim_consistency": "Contract for later self-claim consistency checking.",
}


class DeepSelfIntrospectionRegistryService:
    def __init__(self, subjects: list[DeepSelfIntrospectionSubject] | None = None) -> None:
        self._subjects = {item.subject_id: item for item in subjects or _build_seed_subjects()}

    def list_subjects(self) -> list[DeepSelfIntrospectionSubject]:
        return [self._subjects[subject_id] for subject_id in DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS]

    def get_subject(self, subject_id: str) -> DeepSelfIntrospectionSubject | None:
        return self._subjects.get(subject_id)

    def list_seed_skill_ids(self) -> list[str]:
        return list(DEEP_SELF_INTROSPECTION_SEED_SKILL_IDS)

    def build_contract(self) -> DeepSelfIntrospectionContract:
        return DeepSelfIntrospectionContract(
            contract_id="deep_self_introspection_contract:v0.21.0",
            version=DEEP_SELF_INTROSPECTION_VERSION,
            definition=(
                "Contract-only OCEL-native Deep Self-Introspection layer for future runtime, "
                "capability, policy, context, trace, candidate-memory, and self-claim consistency views."
            ),
            subjects=self.list_subjects(),
            seed_skill_ids=self.list_seed_skill_ids(),
            risk_profile=DeepSelfIntrospectionRiskProfile(),
            gate_contract=DeepSelfIntrospectionGateContract(),
            observability_contract=DeepSelfIntrospectionObservabilityContract(),
            ocel_mapping=DEEP_SELF_INTROSPECTION_OCEL_MAPPING,
            layer=DEEP_SELF_INTROSPECTION_LAYER,
        )


def _build_seed_subjects() -> list[DeepSelfIntrospectionSubject]:
    return [_build_subject(subject_id) for subject_id in DEEP_SELF_INTROSPECTION_SEED_SUBJECT_IDS]


def _build_subject(subject_id: str) -> DeepSelfIntrospectionSubject:
    readable_name = subject_id.removeprefix("subject:").replace("_", " ")
    object_type = _SUBJECT_OBJECT_TYPE[subject_id]
    return DeepSelfIntrospectionSubject(
        subject_id=subject_id,
        name=readable_name,
        description=_SUBJECT_DESCRIPTION[subject_id],
        subject_type="contract_subject",
        introduced_in=DEEP_SELF_INTROSPECTION_VERSION,
        status="contract_only",
        ocel_object_types=["deep_self_introspection_subject", object_type],
        ocel_event_types=[
            "deep_self_introspection_subject_registered",
            "deep_self_introspection_contract_checked",
        ],
        ocel_relation_types=[
            "declares_introspection_subject",
            "maps_subject_to_ocel_object",
            "maps_subject_to_ocel_event",
            "maps_subject_to_ocel_relation",
            "requires_source_object",
            "requires_read_model",
        ],
        required_source_objects=[
            "self_awareness_ecosystem_snapshot",
            "self_awareness_consolidation_report",
        ],
        required_read_models=[
            "SelfAwarenessReleaseState",
            "SelfAwarenessWorkbenchState",
            _SUBJECT_READ_MODEL[subject_id],
        ],
        risk_notes=[
            "contract_only",
            "non_executable",
            "no_actual_analysis_in_v0.21.0",
            "ocel_native_required",
        ],
    )
