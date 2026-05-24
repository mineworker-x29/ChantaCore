from __future__ import annotations

from chanta_core.internal_dominion.mapping import (
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)
from chanta_core.internal_dominion.models import (
    INTERNAL_DOMINION_LAYER,
    INTERNAL_DOMINION_TRACK,
    INTERNAL_DOMINION_VERSION,
    INTERNAL_DOMINION_VERSION_NAME,
    DominionEffectPolicy,
    DominionGateContract,
    DominionObservabilityContract,
    DominionProviderInterfaceContract,
    DominionRiskProfile,
    DominionSubject,
    InternalDominionContract,
    InternalSkillTaxonomy,
    DominionMigrationPolicy,
)


DOMINION_SEED_SUBJECT_IDS = [
    "subject:internal_dominion_contract",
    "subject:runtime_inventory",
    "subject:external_capability_observation",
    "subject:external_capability_digestion",
    "subject:control_request",
    "subject:external_action_candidate",
    "subject:control_plan",
    "subject:target_binding",
    "subject:dominion_static_safety",
    "subject:runtime_preflight",
    "subject:dominion_review_gate",
    "subject:dominion_authorization",
    "subject:bounded_control_dispatch",
    "subject:external_run_tracking",
    "subject:external_outcome_record",
    "subject:dominion_workbench",
    "subject:dominion_consolidation",
]

DOMINION_SEED_SKILL_IDS = [
    "skill:dominion_contract_view",
    "skill:dominion_runtime_inventory",
    "skill:dominion_capability_observe",
    "skill:dominion_capability_digest",
    "skill:dominion_control_request_create",
    "skill:dominion_action_candidate_create",
    "skill:dominion_control_plan_create",
    "skill:dominion_target_binding",
    "skill:dominion_static_safety_check",
    "skill:dominion_runtime_preflight",
    "skill:dominion_review_gate",
    "skill:dominion_authorization_create",
    "skill:dominion_bounded_dispatch",
    "skill:dominion_run_status_track",
    "skill:dominion_run_output_fetch",
    "skill:dominion_outcome_record",
    "skill:dominion_workbench_view",
    "skill:dominion_consolidation_view",
]

_SUBJECT_OBJECT_TYPES = {
    "subject:internal_dominion_contract": "internal_dominion_contract",
    "subject:runtime_inventory": "external_runtime_subject",
    "subject:external_capability_observation": "external_capability_subject",
    "subject:external_capability_digestion": "external_capability_subject",
    "subject:control_request": "control_request_subject",
    "subject:external_action_candidate": "external_action_candidate_subject",
    "subject:control_plan": "control_plan_subject",
    "subject:target_binding": "external_control_surface_subject",
    "subject:dominion_static_safety": "dominion_gate_subject",
    "subject:runtime_preflight": "external_runtime_subject",
    "subject:dominion_review_gate": "dominion_gate_subject",
    "subject:dominion_authorization": "dominion_authorization_subject",
    "subject:bounded_control_dispatch": "bounded_control_dispatch_subject",
    "subject:external_run_tracking": "external_run_tracking_subject",
    "subject:external_outcome_record": "external_outcome_record_subject",
    "subject:dominion_workbench": "internal_dominion_contract_report",
    "subject:dominion_consolidation": "internal_dominion_contract_report",
}

_FUTURE_DISPATCH_SUBJECTS = {
    "subject:bounded_control_dispatch",
    "subject:external_run_tracking",
    "subject:external_outcome_record",
}


class InternalDominionRegistryService:
    def __init__(self, subjects: list[DominionSubject] | None = None) -> None:
        self._subjects = {item.subject_id: item for item in subjects or _build_seed_subjects()}

    def list_subjects(self) -> list[DominionSubject]:
        return [self._subjects[subject_id] for subject_id in DOMINION_SEED_SUBJECT_IDS]

    def list_seed_skill_ids(self) -> list[str]:
        return list(DOMINION_SEED_SKILL_IDS)

    def list_skill_contracts(self) -> list[dict[str, object]]:
        read_only_skills = {
            "skill:dominion_contract_view",
            "skill:dominion_runtime_inventory",
            "skill:dominion_capability_observe",
            "skill:dominion_capability_digest",
        }
        candidate_skills = {"skill:dominion_control_request_create", "skill:dominion_action_candidate_create"}
        plan_only_skills = {"skill:dominion_control_plan_create", "skill:dominion_target_binding"}
        static_rule_skills = {"skill:dominion_static_safety_check"}
        foundation_preflight_skills = {"skill:dominion_runtime_preflight"}
        review_gate_skills = {"skill:dominion_review_gate"}
        gate_authorization_skills = {"skill:dominion_authorization_create"}
        boundary_only_skills = {
            "skill:dominion_bounded_dispatch",
            "skill:dominion_run_status_track",
            "skill:dominion_run_output_fetch",
            "skill:dominion_outcome_record",
        }
        consolidation_only_skills = {
            "skill:dominion_workbench_view",
            "skill:dominion_consolidation_view",
        }
        implemented = (
            read_only_skills
            | candidate_skills
            | plan_only_skills
            | static_rule_skills
            | foundation_preflight_skills
            | review_gate_skills
            | gate_authorization_skills
            | boundary_only_skills
            | consolidation_only_skills
        )
        return [
            {
                "skill_id": skill_id,
                "status": "plan_only"
                if skill_id in plan_only_skills
                else "static_rule_only"
                if skill_id in static_rule_skills
                else "foundation_preflight_only"
                if skill_id in foundation_preflight_skills
                else "review_gate_only"
                if skill_id in review_gate_skills
                else "gate_authorization_only"
                if skill_id in gate_authorization_skills
                else "boundary_only"
                if skill_id in boundary_only_skills
                else "consolidation_only"
                if skill_id in consolidation_only_skills
                else "candidate_only"
                if skill_id in candidate_skills
                else ("read_only" if skill_id in read_only_skills else "contract_only"),
                "stub": skill_id not in implemented,
                "non_dispatching": True,
                "contract_only": skill_id not in implemented,
                "read_only": skill_id in implemented,
                "declarative_inventory_only": skill_id == "skill:dominion_runtime_inventory",
                "declarative_capability_only": skill_id
                in {"skill:dominion_capability_observe", "skill:dominion_capability_digest"},
                "candidate_only": skill_id in candidate_skills,
                "plan_only": skill_id in plan_only_skills,
                "static_rule_only": skill_id in static_rule_skills,
                "foundation_preflight_only": skill_id in foundation_preflight_skills,
                "review_gate_only": skill_id in review_gate_skills,
                "gate_authorization_only": skill_id in gate_authorization_skills,
                "boundary_only": skill_id in boundary_only_skills,
                "consolidation_only": skill_id in consolidation_only_skills,
                "release_readiness_only": skill_id == "skill:dominion_consolidation_view",
                "workbench_snapshot_only": skill_id == "skill:dominion_workbench_view",
                "mutation_performed": False,
                "actual_dispatch_enabled": False,
                "authorization_consumption_enabled": False,
                "live_status_tracking_enabled": False,
                "live_output_fetch_enabled": False,
                "real_external_outcome_record_enabled": False,
                "llm_judge_enabled": False,
                "external_dispatch_enabled": False,
                "external_runtime_touch_enabled": False,
                "provider_api_call_enabled": False,
                "credential_materialization_enabled": False,
                "local_runtime_provider_enabled": False,
                "general_agent_usability_enabled": False,
            }
            for skill_id in DOMINION_SEED_SKILL_IDS
        ]

    def build_contract(self) -> InternalDominionContract:
        return InternalDominionContract(
            contract_id="internal_dominion_contract:v0.23.0",
            version=INTERNAL_DOMINION_VERSION,
            version_name=INTERNAL_DOMINION_VERSION_NAME,
            track=INTERNAL_DOMINION_TRACK,
            layer=INTERNAL_DOMINION_LAYER,
            status="contract_only",
            definition=(
                "Internal Dominion is a vendor-neutral, OCEL-visible, gated control grammar. "
                "It governs external runtimes through inventory, observation, digestion, "
                "control plans, gates, authorization, status tracking, and outcome records. "
                "v0.23.0 does not dispatch, touch external runtimes, or call provider APIs."
            ),
            taxonomy=InternalSkillTaxonomy(),
            subjects=self.list_subjects(),
            seed_skill_ids=self.list_seed_skill_ids(),
            provider_interface=DominionProviderInterfaceContract(),
            risk_profile=DominionRiskProfile(),
            gate_contract=DominionGateContract(),
            observability_contract=DominionObservabilityContract(),
            effect_policy=DominionEffectPolicy(),
            migration_policy=DominionMigrationPolicy(),
        )


def _build_seed_subjects() -> list[DominionSubject]:
    return [_build_subject(subject_id) for subject_id in DOMINION_SEED_SUBJECT_IDS]


def _build_subject(subject_id: str) -> DominionSubject:
    slug = subject_id.removeprefix("subject:")
    object_type = _SUBJECT_OBJECT_TYPES[subject_id]
    future = subject_id in _FUTURE_DISPATCH_SUBJECTS
    if subject_id in {"subject:control_plan", "subject:target_binding"}:
        status = "plan_only"
    elif subject_id == "subject:dominion_static_safety":
        status = "static_rule_only"
    elif subject_id == "subject:runtime_preflight":
        status = "foundation_preflight_only"
    elif subject_id == "subject:dominion_review_gate":
        status = "review_gate_only"
    elif subject_id == "subject:dominion_authorization":
        status = "gate_authorization_only"
    elif subject_id in _FUTURE_DISPATCH_SUBJECTS:
        status = "boundary_only"
    elif subject_id in {"subject:dominion_workbench", "subject:dominion_consolidation"}:
        status = "consolidation_only"
    else:
        status = "future_stub" if future else "contract_only"
    return DominionSubject(
        subject_id=subject_id,
        name=slug.replace("_", " "),
        description=f"Provider-neutral Internal Dominion contract subject for {slug.replace('_', ' ')}.",
        status=status,
        provider_neutral=True,
        dispatch_enabled=False,
        introduced_in=INTERNAL_DOMINION_VERSION,
        ocel_object_types=["dominion_subject", object_type],
        ocel_event_types=[
            "dominion_subject_registered",
            "dominion_conformance_checked",
        ],
        ocel_relation_types=[
            "declares_dominion_subject",
            "requires_ocel_visibility",
            "prevents_provider_gate_bypass",
        ],
        risk_notes=[
            "contract_only",
            "stub" if future else "read_only_contract",
            "non_dispatching",
            "provider_neutral",
            "no_provider_api_call",
            "no_external_runtime_touch",
        ],
    )


def dominion_mapping_snapshot() -> dict[str, list[str]]:
    return {
        "object_types": list(DOMINION_OCEL_OBJECT_TYPES),
        "event_types": list(DOMINION_OCEL_EVENT_TYPES),
        "relation_types": list(DOMINION_OCEL_RELATION_TYPES),
    }
