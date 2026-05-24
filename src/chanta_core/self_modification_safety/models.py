from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


SELF_MODIFICATION_SAFETY_LAYER = "self_modification_safety"
SELF_MODIFICATION_SAFETY_VERSION = "v0.22.0"
SELF_MODIFICATION_SAFETY_STATE = "self_modification_safety_contract_registered"


@dataclass(frozen=True)
class SelfModificationSubject:
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
class SelfModificationRiskProfile:
    contract_only: bool = True
    file_write_enabled: bool = False
    apply_patch_enabled: bool = False
    shell_enabled: bool = False
    test_execution_enabled: bool = False
    lint_execution_enabled: bool = False
    network_enabled: bool = False
    mcp_enabled: bool = False
    plugin_enabled: bool = False
    external_harness_enabled: bool = False
    memory_mutation_enabled: bool = False
    persona_mutation_enabled: bool = False
    overlay_mutation_enabled: bool = False
    autonomous_apply_enabled: bool = False
    llm_patch_generation_enabled: bool = False
    llm_judge_enabled: bool = False
    dangerous_capability: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class SelfModificationGateContract:
    requires_modification_request: bool = True
    requires_patch_candidate: bool = True
    requires_diff_preview: bool = True
    requires_static_safety_check: bool = True
    requires_dry_run_before_apply: bool = True
    requires_human_review_before_apply: bool = True
    requires_explicit_apply_gate: bool = True
    requires_rollback_plan: bool = True
    requires_post_apply_verification: bool = True
    deny_if_unreviewed: bool = True
    deny_if_no_rollback_plan: bool = True
    deny_if_no_dry_run: bool = True
    deny_if_private_boundary_risk: bool = True
    deny_if_patch_scope_exceeds_limit: bool = True

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class SelfModificationObservabilityContract:
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
class SelfModificationAllowedPatchPolicy:
    allowed_patch_types: list[str] = field(
        default_factory=lambda: [
            "text_replace",
            "insert_after",
            "append_block",
            "comment_only_change",
        ]
    )
    forbidden_patch_types: list[str] = field(
        default_factory=lambda: [
            "binary_patch",
            "broad_rewrite",
            "delete_file",
            "rename_file",
            "chmod_change",
            "dependency_install",
            "secret_file_change",
            "generated_file_mass_update",
        ]
    )
    max_files_per_patch: int = 1
    max_hunks_per_file: int = 3
    max_added_lines: int = 80
    max_removed_lines: int = 80
    requires_anchor_text: bool = True
    requires_workspace_path_policy: bool = True
    allows_binary_files: bool = False
    allows_secret_files: bool = False
    allows_private_paths: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_patch_types": list(self.allowed_patch_types),
            "forbidden_patch_types": list(self.forbidden_patch_types),
            "max_files_per_patch": self.max_files_per_patch,
            "max_hunks_per_file": self.max_hunks_per_file,
            "max_added_lines": self.max_added_lines,
            "max_removed_lines": self.max_removed_lines,
            "requires_anchor_text": self.requires_anchor_text,
            "requires_workspace_path_policy": self.requires_workspace_path_policy,
            "allows_binary_files": self.allows_binary_files,
            "allows_secret_files": self.allows_secret_files,
            "allows_private_paths": self.allows_private_paths,
        }


@dataclass(frozen=True)
class SelfModificationLifecyclePolicy:
    states: list[str]
    transitions: list[dict[str, str]]
    mutation_transitions_executable: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "states": list(self.states),
            "transitions": [dict(item) for item in self.transitions],
            "mutation_transitions_executable": self.mutation_transitions_executable,
            "notes": list(self.notes),
        }


@dataclass(frozen=True)
class SelfModificationOCELMapping:
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
class SelfModificationContractReport:
    report_id: str
    version: str
    layer: str
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
            "layer": self.layer,
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
class SelfModificationSafetyContract:
    contract_id: str
    version: str
    definition: str
    subjects: list[SelfModificationSubject]
    seed_skill_ids: list[str]
    risk_profile: SelfModificationRiskProfile
    gate_contract: SelfModificationGateContract
    observability_contract: SelfModificationObservabilityContract
    allowed_patch_policy: SelfModificationAllowedPatchPolicy
    lifecycle_policy: SelfModificationLifecyclePolicy
    ocel_mapping: SelfModificationOCELMapping
    pig_projection_required: bool = True
    ocpx_projection_required: bool = True
    workbench_visibility_required: bool = True
    status: str = "contract_only"
    layer: str = SELF_MODIFICATION_SAFETY_LAYER

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
            "allowed_patch_policy": self.allowed_patch_policy.to_dict(),
            "lifecycle_policy": self.lifecycle_policy.to_dict(),
            "ocel_mapping": self.ocel_mapping.to_dict(),
            "pig_projection_required": self.pig_projection_required,
            "ocpx_projection_required": self.ocpx_projection_required,
            "workbench_visibility_required": self.workbench_visibility_required,
            "status": self.status,
        }
