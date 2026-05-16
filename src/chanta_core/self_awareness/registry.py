from __future__ import annotations

from chanta_core.self_awareness.mapping import (
    SELF_AWARENESS_OCEL_EVENT_TYPES,
    SELF_AWARENESS_OCEL_OBJECT_TYPES,
    SELF_AWARENESS_OCEL_RELATION_TYPES,
)
from chanta_core.self_awareness.models import (
    SELF_AWARENESS_LAYER,
    SELF_AWARENESS_STATE,
    SelfAwarenessCapabilityDescriptor,
    SelfAwarenessGateContract,
    SelfAwarenessObservabilityContract,
    SelfAwarenessRiskProfile,
    SelfAwarenessSkillContract,
)


SELF_AWARENESS_SEED_SKILL_IDS = [
    "skill:self_awareness_workspace_inventory",
    "skill:self_awareness_path_verify",
    "skill:self_awareness_text_read",
    "skill:self_awareness_workspace_search",
    "skill:self_awareness_python_symbols",
    "skill:self_awareness_markdown_structure",
    "skill:self_awareness_project_structure",
    "skill:self_awareness_surface_verify",
    "skill:self_awareness_config_surface",
    "skill:self_awareness_test_surface",
    "skill:self_awareness_capability_registry",
    "skill:self_awareness_runtime_boundary",
    "skill:self_awareness_plan_candidate",
    "skill:self_awareness_todo_candidate",
]

_OUTPUT_BY_SKILL_ID = {
    "skill:self_awareness_workspace_inventory": ("workspace", "workspace_inventory_summary"),
    "skill:self_awareness_path_verify": ("verification", "path_verification_result"),
    "skill:self_awareness_text_read": ("workspace", "text_read_evidence_surface"),
    "skill:self_awareness_workspace_search": ("workspace", "workspace_search_summary"),
    "skill:self_awareness_python_symbols": ("codebase", "python_symbol_summary"),
    "skill:self_awareness_markdown_structure": ("codebase", "markdown_structure_summary"),
    "skill:self_awareness_project_structure": ("codebase", "project_structure_summary"),
    "skill:self_awareness_surface_verify": ("verification", "surface_verification_report"),
    "skill:self_awareness_config_surface": ("runtime", "config_surface_summary"),
    "skill:self_awareness_test_surface": ("verification", "test_surface_summary"),
    "skill:self_awareness_capability_registry": ("runtime", "capability_registry_summary"),
    "skill:self_awareness_runtime_boundary": ("runtime", "runtime_boundary_summary"),
    "skill:self_awareness_plan_candidate": ("candidate", "plan_candidate"),
    "skill:self_awareness_todo_candidate": ("candidate", "todo_candidate"),
}


class SelfAwarenessRegistryService:
    def __init__(self, contracts: list[SelfAwarenessSkillContract] | None = None) -> None:
        self._contracts = {item.skill_id: item for item in contracts or _build_seed_contracts()}

    def list_contracts(self) -> list[SelfAwarenessSkillContract]:
        return [self._contracts[skill_id] for skill_id in self.list_seed_skill_ids()]

    def get_contract(self, skill_id: str) -> SelfAwarenessSkillContract | None:
        return self._contracts.get(skill_id)

    def list_seed_skill_ids(self) -> list[str]:
        return list(SELF_AWARENESS_SEED_SKILL_IDS)

    def summarize_layer(self) -> dict[str, object]:
        contracts = self.list_contracts()
        dangerous = [item for item in contracts if item.risk_profile.dangerous_capability]
        return {
            "layer": SELF_AWARENESS_LAYER,
            "state": SELF_AWARENESS_STATE,
            "contract_count": len(contracts),
            "implemented_count": sum(1 for item in contracts if item.implementation_status == "implemented"),
            "read_only_observation_count": sum(1 for item in contracts if item.effect_type == "read_only_observation"),
            "execution_enabled_count": sum(1 for item in contracts if item.execution_enabled),
            "canonical_mutation_enabled_count": sum(1 for item in contracts if item.canonical_mutation_enabled),
            "dangerous_capability_count": len(dangerous),
            "write_mutation_count": sum(1 for item in contracts if item.risk_profile.mutates_workspace),
            "shell_usage_count": sum(1 for item in contracts if item.risk_profile.uses_shell),
            "network_usage_count": sum(1 for item in contracts if item.risk_profile.uses_network),
            "memory_mutation_count": sum(1 for item in contracts if item.risk_profile.mutates_memory),
            "persona_mutation_count": sum(1 for item in contracts if item.risk_profile.mutates_persona),
            "overlay_mutation_count": sum(1 for item in contracts if item.risk_profile.mutates_overlay),
        }


def _build_seed_contracts() -> list[SelfAwarenessSkillContract]:
    return [_build_contract(skill_id) for skill_id in SELF_AWARENESS_SEED_SKILL_IDS]


def _build_contract(skill_id: str) -> SelfAwarenessSkillContract:
    family, output_kind = _OUTPUT_BY_SKILL_ID[skill_id]
    name = skill_id.removeprefix("skill:").replace("_", " ")
    implemented = skill_id in {
        "skill:self_awareness_workspace_inventory",
        "skill:self_awareness_path_verify",
        "skill:self_awareness_text_read",
        "skill:self_awareness_workspace_search",
        "skill:self_awareness_markdown_structure",
        "skill:self_awareness_python_symbols",
        "skill:self_awareness_project_structure",
        "skill:self_awareness_surface_verify",
        "skill:self_awareness_plan_candidate",
        "skill:self_awareness_todo_candidate",
    }
    return SelfAwarenessSkillContract(
        skill_id=skill_id,
        skill_name=name,
        description=(
            "Read-only self-awareness skill available through the explicit execution gate."
            if implemented
            else "Contract-only self-awareness skill descriptor. "
            "It may describe read-only evidence or candidates but is not implemented in v0.20.9."
        ),
        implementation_status="implemented" if implemented else "contract_only",
        effect_type="read_only_observation" if implemented else "contract_only",
        risk_profile=SelfAwarenessRiskProfile(read_only=True),
        gate_contract=SelfAwarenessGateContract(
            gate_id=f"gate:{skill_id.removeprefix('skill:')}",
            evidence_refs_required=True,
            execution_envelope_required=True,
            allow_skill_execution=implemented,
            allow_canonical_mutation=False,
            gate_attrs={
                "execution_route": "explicit_read_only_gate" if implemented else "not_invokable",
                "workspace_mutation_allowed": False,
                "memory_mutation_allowed": False,
                "persona_mutation_allowed": False,
                "overlay_mutation_allowed": False,
            },
        ),
        observability_contract=SelfAwarenessObservabilityContract(
            observability_id=f"observability:{skill_id.removeprefix('skill:')}",
            ocel_object_types=SELF_AWARENESS_OCEL_OBJECT_TYPES,
            ocel_event_types=SELF_AWARENESS_OCEL_EVENT_TYPES,
            ocel_relation_types=SELF_AWARENESS_OCEL_RELATION_TYPES,
        ),
        capability=SelfAwarenessCapabilityDescriptor(
            capability_id=f"self_awareness_capability:{skill_id.removeprefix('skill:')}",
            skill_id=skill_id,
            capability_name=name,
            capability_family=family,
            output_kind=output_kind,
        ),
        contract_attrs={
            "contract_version": _contract_version(skill_id),
            "self_awareness_is_self_modification": False,
            "actual_inspection_implemented": implemented,
            "file_content_reading_implemented": skill_id
            in {
                "skill:self_awareness_text_read",
                "skill:self_awareness_workspace_search",
                "skill:self_awareness_markdown_structure",
                "skill:self_awareness_python_symbols",
            },
            "metadata_only": skill_id
            in {
                "skill:self_awareness_workspace_inventory",
                "skill:self_awareness_path_verify",
                "skill:self_awareness_project_structure",
            },
            "bounded_literal_search_implemented": skill_id == "skill:self_awareness_workspace_search",
            "summary_candidate_created": skill_id
            in {"skill:self_awareness_markdown_structure", "skill:self_awareness_python_symbols"},
            "project_structure_candidate_created": skill_id == "skill:self_awareness_project_structure",
            "surface_verification_report_created": skill_id == "skill:self_awareness_surface_verify",
            "directed_intention_candidate_created": skill_id
            in {"skill:self_awareness_plan_candidate", "skill:self_awareness_todo_candidate"},
            "plan_candidate_created": skill_id == "skill:self_awareness_plan_candidate",
            "todo_candidate_created": skill_id == "skill:self_awareness_todo_candidate",
            "surface_candidate_detection_only": skill_id
            in {"skill:self_awareness_config_surface", "skill:self_awareness_test_surface"},
            "canonical_promotion_enabled": False,
            "canonical_store": "ocel",
        },
    )


def _contract_version(skill_id: str) -> str:
    if skill_id in {"skill:self_awareness_workspace_inventory", "skill:self_awareness_path_verify"}:
        return "v0.20.1"
    if skill_id == "skill:self_awareness_text_read":
        return "v0.20.2"
    if skill_id == "skill:self_awareness_workspace_search":
        return "v0.20.3"
    if skill_id in {"skill:self_awareness_markdown_structure", "skill:self_awareness_python_symbols"}:
        return "v0.20.4"
    if skill_id == "skill:self_awareness_project_structure":
        return "v0.20.5"
    if skill_id == "skill:self_awareness_surface_verify":
        return "v0.20.6"
    if skill_id in {"skill:self_awareness_plan_candidate", "skill:self_awareness_todo_candidate"}:
        return "v0.20.7"
    return "v0.20.0"
