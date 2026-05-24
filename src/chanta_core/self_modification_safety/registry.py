from __future__ import annotations

from chanta_core.self_modification_safety.mapping import SELF_MODIFICATION_OCEL_MAPPING
from chanta_core.self_modification_safety.models import (
    SELF_MODIFICATION_SAFETY_LAYER,
    SELF_MODIFICATION_SAFETY_VERSION,
    SelfModificationAllowedPatchPolicy,
    SelfModificationGateContract,
    SelfModificationLifecyclePolicy,
    SelfModificationObservabilityContract,
    SelfModificationRiskProfile,
    SelfModificationSafetyContract,
    SelfModificationSubject,
)


SELF_MODIFICATION_SEED_SUBJECT_IDS = [
    "subject:modification_request",
    "subject:patch_candidate",
    "subject:diff_preview",
    "subject:patch_static_safety",
    "subject:patch_dry_run",
    "subject:modification_review_gate",
    "subject:patch_apply_gate",
    "subject:rollback_plan",
    "subject:bounded_patch_apply",
    "subject:post_apply_verification",
    "subject:modification_outcome",
    "subject:self_modification_workbench",
    "subject:self_modification_consolidation",
]

SELF_MODIFICATION_SEED_SKILL_IDS = [
    "skill:self_modification_request_create",
    "skill:self_modification_patch_candidate_create",
    "skill:self_modification_patch_draft_create",
    "skill:self_modification_diff_preview",
    "skill:self_modification_static_safety_check",
    "skill:self_modification_static_safety_report",
    "skill:self_modification_dry_run",
    "skill:self_modification_applicability_check",
    "skill:self_modification_review_gate",
    "skill:self_modification_apply_gate",
    "skill:self_modification_rollback_plan",
    "skill:self_modification_bounded_patch_apply",
    "skill:self_modification_post_apply_verify",
    "skill:self_modification_outcome_record",
    "skill:self_modification_workbench_view",
    "skill:self_modification_timeline_view",
    "skill:self_modification_findings_view",
    "skill:self_modification_consolidation_view",
]

LIFECYCLE_STATES = [
    "requested",
    "candidate_created",
    "preview_created",
    "safety_checked",
    "dry_run_checked",
    "pending_review",
    "approved_for_apply",
    "apply_gate_opened",
    "applied",
    "post_apply_verified",
    "outcome_recorded",
    "blocked",
    "rejected",
    "no_action",
    "needs_more_input",
]

LIFECYCLE_TRANSITIONS = [
    {"from": "requested", "to": "candidate_created", "transition": "create_candidate"},
    {"from": "candidate_created", "to": "preview_created", "transition": "create_preview"},
    {"from": "preview_created", "to": "safety_checked", "transition": "check_static_safety"},
    {"from": "safety_checked", "to": "dry_run_checked", "transition": "record_dry_run_result"},
    {"from": "dry_run_checked", "to": "pending_review", "transition": "request_human_review"},
    {"from": "pending_review", "to": "approved_for_apply", "transition": "record_review_approval"},
    {"from": "approved_for_apply", "to": "apply_gate_opened", "transition": "open_apply_gate"},
    {"from": "apply_gate_opened", "to": "applied", "transition": "future_apply_transition"},
    {"from": "applied", "to": "post_apply_verified", "transition": "verify_after_apply"},
    {"from": "post_apply_verified", "to": "outcome_recorded", "transition": "record_outcome"},
]

_SUBJECT_OBJECT_TYPE = {
    "subject:modification_request": "modification_request_subject",
    "subject:patch_candidate": "patch_candidate_subject",
    "subject:diff_preview": "diff_preview_subject",
    "subject:patch_static_safety": "patch_static_safety_subject",
    "subject:patch_dry_run": "patch_dry_run_subject",
    "subject:modification_review_gate": "modification_review_gate_subject",
    "subject:patch_apply_gate": "patch_apply_gate_subject",
    "subject:rollback_plan": "rollback_plan_subject",
    "subject:bounded_patch_apply": "bounded_patch_apply_subject",
    "subject:post_apply_verification": "post_apply_verification_subject",
    "subject:modification_outcome": "modification_outcome_subject",
    "subject:self_modification_workbench": "self_modification_workbench_subject",
    "subject:self_modification_consolidation": "self_modification_consolidation_subject",
}

_SUBJECT_DESCRIPTION = {
    "subject:modification_request": "Contract for later modification request records.",
    "subject:patch_candidate": "Contract for later bounded patch candidates.",
    "subject:diff_preview": "Contract for later sanitized diff previews.",
    "subject:patch_static_safety": "Contract for later static safety reports.",
    "subject:patch_dry_run": "Contract for later dry-run result records.",
    "subject:modification_review_gate": "Contract for later human review gate records.",
    "subject:patch_apply_gate": "Contract for later explicit apply gate records.",
    "subject:rollback_plan": "Contract for later rollback plan records.",
    "subject:bounded_patch_apply": "Contract and runtime owner for bounded patch apply records.",
    "subject:post_apply_verification": "Contract for later post-apply verification records.",
    "subject:modification_outcome": "Contract for later modification outcome records.",
    "subject:self_modification_workbench": "Read-only workbench over the self-modification safety pipeline.",
    "subject:self_modification_consolidation": "Read-only consolidation report for Self-Modification Safety Foundation v1.",
}


class SelfModificationRegistryService:
    def __init__(self, subjects: list[SelfModificationSubject] | None = None) -> None:
        self._subjects = {item.subject_id: item for item in subjects or _build_seed_subjects()}

    def list_subjects(self) -> list[SelfModificationSubject]:
        return [self._subjects[subject_id] for subject_id in SELF_MODIFICATION_SEED_SUBJECT_IDS]

    def get_subject(self, subject_id: str) -> SelfModificationSubject | None:
        return self._subjects.get(subject_id)

    def list_seed_skill_ids(self) -> list[str]:
        return list(SELF_MODIFICATION_SEED_SKILL_IDS)

    def list_skill_contracts(self) -> list[dict[str, object]]:
        implemented = {
            "skill:self_modification_request_create",
            "skill:self_modification_patch_candidate_create",
            "skill:self_modification_patch_draft_create",
            "skill:self_modification_diff_preview",
            "skill:self_modification_static_safety_check",
            "skill:self_modification_static_safety_report",
            "skill:self_modification_dry_run",
            "skill:self_modification_applicability_check",
            "skill:self_modification_review_gate",
            "skill:self_modification_apply_gate",
            "skill:self_modification_rollback_plan",
            "skill:self_modification_bounded_patch_apply",
            "skill:self_modification_post_apply_verify",
            "skill:self_modification_outcome_record",
            "skill:self_modification_workbench_view",
            "skill:self_modification_timeline_view",
            "skill:self_modification_findings_view",
            "skill:self_modification_consolidation_view",
        }
        return [
            {
                "skill_id": skill_id,
                "status": "implemented" if skill_id in implemented else "contract_only",
                "candidate_only": skill_id in implemented and skill_id != "skill:self_modification_bounded_patch_apply",
                "stub": skill_id not in implemented,
                "non_executable": skill_id != "skill:self_modification_bounded_patch_apply",
                "file_write_enabled": skill_id == "skill:self_modification_bounded_patch_apply",
                "apply_patch_enabled": False,
                "diff_generation_enabled": False,
                "preview_generation_enabled": skill_id in {
                    "skill:self_modification_patch_draft_create",
                    "skill:self_modification_diff_preview",
                },
                "static_safety_check_enabled": skill_id
                in {
                    "skill:self_modification_static_safety_check",
                    "skill:self_modification_static_safety_report",
                },
                "dry_run_enabled": skill_id
                in {
                    "skill:self_modification_dry_run",
                    "skill:self_modification_applicability_check",
                },
                "in_memory_only": skill_id
                in {
                    "skill:self_modification_dry_run",
                    "skill:self_modification_applicability_check",
                },
                "review_gate_enabled": skill_id == "skill:self_modification_review_gate",
                "apply_gate_state_enabled": skill_id == "skill:self_modification_apply_gate",
                "rollback_plan_descriptor_enabled": skill_id == "skill:self_modification_rollback_plan",
                "bounded_file_write_enabled": skill_id == "skill:self_modification_bounded_patch_apply",
                "patch_apply_enabled": skill_id == "skill:self_modification_bounded_patch_apply",
                "post_apply_verify_enabled": skill_id == "skill:self_modification_post_apply_verify",
                "outcome_record_enabled": skill_id == "skill:self_modification_outcome_record",
                "workbench_view_enabled": skill_id == "skill:self_modification_workbench_view",
                "timeline_view_enabled": skill_id == "skill:self_modification_timeline_view",
                "findings_view_enabled": skill_id == "skill:self_modification_findings_view",
                "consolidation_view_enabled": skill_id == "skill:self_modification_consolidation_view",
            }
            for skill_id in SELF_MODIFICATION_SEED_SKILL_IDS
        ]

    def build_lifecycle_policy(self) -> SelfModificationLifecyclePolicy:
        return SelfModificationLifecyclePolicy(
            states=list(LIFECYCLE_STATES),
            transitions=[dict(item) for item in LIFECYCLE_TRANSITIONS],
            mutation_transitions_executable=False,
            notes=[
                "v0.22.0 defines lifecycle states only.",
                "The apply transition is future/deferred and is not executable in v0.22.0.",
            ],
        )

    def build_contract(self) -> SelfModificationSafetyContract:
        return SelfModificationSafetyContract(
            contract_id="self_modification_safety_contract:v0.22.0",
            version=SELF_MODIFICATION_SAFETY_VERSION,
            definition=(
                "Contract-only OCEL-native Self-Modification Safety layer. "
                "Patch candidates, previews, review gates, apply gates, rollback plans, "
                "and post-apply verification are specified but not executed."
            ),
            subjects=self.list_subjects(),
            seed_skill_ids=self.list_seed_skill_ids(),
            risk_profile=SelfModificationRiskProfile(),
            gate_contract=SelfModificationGateContract(),
            observability_contract=SelfModificationObservabilityContract(),
            allowed_patch_policy=SelfModificationAllowedPatchPolicy(),
            lifecycle_policy=self.build_lifecycle_policy(),
            ocel_mapping=SELF_MODIFICATION_OCEL_MAPPING,
            layer=SELF_MODIFICATION_SAFETY_LAYER,
        )


def _build_seed_subjects() -> list[SelfModificationSubject]:
    return [_build_subject(subject_id) for subject_id in SELF_MODIFICATION_SEED_SUBJECT_IDS]


def _build_subject(subject_id: str) -> SelfModificationSubject:
    readable_name = subject_id.removeprefix("subject:").replace("_", " ")
    object_type = _SUBJECT_OBJECT_TYPE[subject_id]
    return SelfModificationSubject(
        subject_id=subject_id,
        name=readable_name,
        description=_SUBJECT_DESCRIPTION[subject_id],
        subject_type="contract_subject",
        introduced_in=SELF_MODIFICATION_SAFETY_VERSION,
        status="contract_only",
        ocel_object_types=["self_modification_subject", object_type],
        ocel_event_types=[
            "self_modification_subject_registered",
            "self_modification_contract_checked",
        ],
        ocel_relation_types=[
            "declares_modification_subject",
            "maps_subject_to_ocel_object",
            "maps_subject_to_ocel_event",
            "maps_subject_to_ocel_relation",
        ],
        required_source_objects=[
            "deep_self_consolidation_report",
            "capability_truth_report",
            "runtime_boundary_truth_report",
            "policy_gate_truth_report",
            "trace_integrity_report",
            "candidate_memory_boundary_report",
        ],
        required_read_models=[
            "DeepSelfConsolidationState",
            "DeepSelfReadinessState",
            "SelfCapabilityTruthState",
            "SelfRuntimeBoundaryState",
            "SelfPolicyGateState",
            "SelfTraceIntegrityState",
            "SelfCandidateMemoryBoundaryState",
        ],
        risk_notes=[
            "contract_only",
            "stub",
            "non_executable",
            "no_file_write_in_v0.22.0",
            "no_patch_application_in_v0.22.0",
            "ocel_native_required",
        ],
    )
