from __future__ import annotations

from typing import Any

from chanta_core.self_modification_safety.conformance import SelfModificationConformanceService
from chanta_core.self_modification_safety.models import (
    SELF_MODIFICATION_SAFETY_VERSION,
    SelfModificationContractReport,
)
from chanta_core.self_modification_safety.registry import SelfModificationRegistryService


PRINCIPLES = [
    "self-modification safety is not self-modification",
    "patch candidate is not patch apply",
    "diff preview is not file mutation",
    "review approval is not execution",
    "apply requires explicit apply gate",
    "rollback plan is required before mutation",
    "post-apply verification is mandatory after mutation",
]


class SelfModificationReportService:
    def __init__(
        self,
        *,
        registry_service: SelfModificationRegistryService | None = None,
        conformance_service: SelfModificationConformanceService | None = None,
    ) -> None:
        self.registry_service = registry_service or SelfModificationRegistryService()
        self.conformance_service = conformance_service or SelfModificationConformanceService(self.registry_service)

    def build_contract_report(self, subject_id: str = "self_modification_safety") -> SelfModificationContractReport:
        contract = self.registry_service.build_contract()
        subject_refs = [{"subject_id": item.subject_id, "status": item.status} for item in contract.subjects]
        return SelfModificationContractReport(
            report_id=f"self_modification_contract_report:v0.22.0:{subject_id}",
            version=SELF_MODIFICATION_SAFETY_VERSION,
            layer=contract.layer,
            subject_id=subject_id,
            status="contract_only",
            source_refs=[
                {
                    "ref_type": "deep_self_consolidation",
                    "ref_id": "v0.21.9",
                    "summary": "OCEL-native Deep Self-Introspection Foundation v1 consolidated read model.",
                },
                {
                    "ref_type": "self_awareness_consolidation",
                    "ref_id": "v0.20.9",
                    "summary": "OCEL-native Self-Awareness Foundation v1 consolidated read model.",
                },
            ],
            evidence_refs=subject_refs,
            findings=[],
            limitations=[
                "v0.22.0 registers contracts only.",
                "No file write, patch generation, patch application, dry-run execution, or shell/test/lint execution is implemented.",
            ],
            withdrawal_conditions=[
                "Withdraw if any seed skill becomes executable.",
                "Withdraw if file write, patch application, shell execution, or LLM patch generation is enabled.",
                "Withdraw if OCEL mapping is removed or a non-OCEL canonical store is introduced.",
            ],
            validity_horizon="Valid until v0.22.1 begins request and patch candidate records.",
        )

    def build_pig_report(self) -> dict[str, Any]:
        contract = self.registry_service.build_contract()
        conformance = self.conformance_service.run_conformance()
        risk = contract.risk_profile
        return {
            "report_name": "Self-Modification Safety PIG Report",
            "version": SELF_MODIFICATION_SAFETY_VERSION,
            "layer": "self_modification_safety",
            "status": "contract_only" if conformance.passed else "failed",
            "requires_deep_self_introspection_consolidation": "v0.21.9",
            "principles": list(PRINCIPLES),
            "subjects": [item.subject_id for item in contract.subjects],
            "seed_skill_ids": list(contract.seed_skill_ids),
            "safety_boundary": {
                "contract_only": risk.contract_only,
                "file_write_enabled": risk.file_write_enabled,
                "apply_patch_enabled": risk.apply_patch_enabled,
                "shell_enabled": risk.shell_enabled,
                "test_execution_enabled": risk.test_execution_enabled,
                "lint_execution_enabled": risk.lint_execution_enabled,
                "network_enabled": risk.network_enabled,
                "mcp_enabled": risk.mcp_enabled,
                "plugin_enabled": risk.plugin_enabled,
                "external_harness_enabled": risk.external_harness_enabled,
                "memory_mutation_enabled": risk.memory_mutation_enabled,
                "persona_mutation_enabled": risk.persona_mutation_enabled,
                "overlay_mutation_enabled": risk.overlay_mutation_enabled,
                "autonomous_apply_enabled": risk.autonomous_apply_enabled,
                "llm_patch_generation_enabled": risk.llm_patch_generation_enabled,
                "llm_judge_enabled": risk.llm_judge_enabled,
                "dangerous_capability": risk.dangerous_capability,
            },
            "conformance_status": conformance.status,
            "canonical_store": "ocel",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        contract = self.registry_service.build_contract()
        conformance = self.conformance_service.run_conformance()
        return {
            "projection_name": "Self-Modification Safety OCPX Projection",
            "state": "self_modification_safety_contract_registered",
            "version": SELF_MODIFICATION_SAFETY_VERSION,
            "layer": "self_modification_safety",
            "source_read_models": [
                "DeepSelfConsolidationState",
                "DeepSelfReadinessState",
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
                "SelfTraceIntegrityState",
                "SelfCandidateMemoryBoundaryState",
            ],
            "target_read_models": [
                "SelfModificationSafetyContractState",
                "SelfModificationLifecyclePolicyState",
                "SelfModificationPatchPolicyState",
                "SelfModificationGateContractState",
            ],
            "subjects": [item.subject_id for item in contract.subjects],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "object_coverage": list(contract.ocel_mapping.object_types),
            "event_coverage": list(contract.ocel_mapping.event_types),
            "relation_coverage": list(contract.ocel_mapping.relation_types),
            "conformance_status": conformance.status,
            "canonical_store": "ocel",
        }

    def render_contract_cli(self) -> str:
        contract = self.registry_service.build_contract()
        risk = contract.risk_profile
        return "\n".join(
            [
                "Self-Modification Safety Contract",
                "version=v0.22.0",
                "layer=self_modification_safety",
                "status=contract_only",
                f"seed_subjects={','.join(item.subject_id for item in contract.subjects)}",
                f"seed_skill_ids={','.join(contract.seed_skill_ids)}",
                f"file_write_enabled={str(risk.file_write_enabled).lower()}",
                f"apply_patch_enabled={str(risk.apply_patch_enabled).lower()}",
                f"autonomous_apply_enabled={str(risk.autonomous_apply_enabled).lower()}",
                f"llm_patch_generation_enabled={str(risk.llm_patch_generation_enabled).lower()}",
                f"llm_judge_enabled={str(risk.llm_judge_enabled).lower()}",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
                "canonical_store=ocel",
            ]
        )

    def render_subjects_cli(self) -> str:
        subjects = self.registry_service.list_subjects()
        lines = [
            "Self-Modification Safety Subjects",
            "layer=self_modification_safety",
            "status=contract_only",
        ]
        lines.extend(f"- subject={item.subject_id} status={item.status}" for item in subjects)
        lines.extend(
            [
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )
        return "\n".join(lines)

    def render_lifecycle_cli(self) -> str:
        policy = self.registry_service.build_contract().lifecycle_policy
        return "\n".join(
            [
                "Self-Modification Lifecycle Policy",
                "layer=self_modification_safety",
                "status=contract_only",
                f"states={','.join(policy.states)}",
                "transitions=" + ",".join(f"{item['from']}->{item['to']}" for item in policy.transitions),
                f"mutation_transitions_executable={str(policy.mutation_transitions_executable).lower()}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_patch_policy_cli(self) -> str:
        policy = self.registry_service.build_contract().allowed_patch_policy
        return "\n".join(
            [
                "Self-Modification Patch Policy",
                "layer=self_modification_safety",
                "status=contract_only",
                f"allowed_patch_types={','.join(policy.allowed_patch_types)}",
                f"forbidden_patch_types={','.join(policy.forbidden_patch_types)}",
                f"max_files_per_patch={policy.max_files_per_patch}",
                f"max_hunks_per_file={policy.max_hunks_per_file}",
                f"max_added_lines={policy.max_added_lines}",
                f"max_removed_lines={policy.max_removed_lines}",
                f"requires_anchor_text={str(policy.requires_anchor_text).lower()}",
                f"requires_workspace_path_policy={str(policy.requires_workspace_path_policy).lower()}",
                f"allows_binary_files={str(policy.allows_binary_files).lower()}",
                f"allows_secret_files={str(policy.allows_secret_files).lower()}",
                f"allows_private_paths={str(policy.allows_private_paths).lower()}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        safety = report["safety_boundary"]
        return "\n".join(
            [
                "Self-Modification Safety PIG Report",
                "version=v0.22.0",
                "layer=self_modification_safety",
                f"status={report['status']}",
                "requires_deep_self_introspection_consolidation=v0.21.9",
                f"principles={','.join(report['principles'])}",
                f"file_write_enabled={str(safety['file_write_enabled']).lower()}",
                f"apply_patch_enabled={str(safety['apply_patch_enabled']).lower()}",
                f"autonomous_apply_enabled={str(safety['autonomous_apply_enabled']).lower()}",
                f"llm_patch_generation_enabled={str(safety['llm_patch_generation_enabled']).lower()}",
                f"llm_judge_enabled={str(safety['llm_judge_enabled']).lower()}",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
                "canonical_store=ocel",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Self-Modification Safety OCPX Projection",
                "version=v0.22.0",
                "layer=self_modification_safety",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                f"conformance_status={projection['conformance_status']}",
                "file_write_enabled=false",
                "apply_patch_enabled=false",
                "no_file_mutation_occurred=true",
                "private_full_paths_printed=False",
                "raw_file_content_printed=False",
                "raw_secrets_printed=False",
                "canonical_store=ocel",
            ]
        )
