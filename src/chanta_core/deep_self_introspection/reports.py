from __future__ import annotations

from typing import Any

from chanta_core.deep_self_introspection.conformance import DeepSelfIntrospectionConformanceService
from chanta_core.deep_self_introspection.models import DeepSelfIntrospectionReport
from chanta_core.deep_self_introspection.registry import DeepSelfIntrospectionRegistryService


class DeepSelfIntrospectionReportService:
    def __init__(
        self,
        *,
        registry_service: DeepSelfIntrospectionRegistryService | None = None,
        conformance_service: DeepSelfIntrospectionConformanceService | None = None,
    ) -> None:
        self.registry_service = registry_service or DeepSelfIntrospectionRegistryService()
        self.conformance_service = conformance_service or DeepSelfIntrospectionConformanceService(self.registry_service)

    def build_pig_report(self) -> dict[str, Any]:
        contract = self.registry_service.build_contract()
        conformance = self.conformance_service.run_conformance()
        return {
            "report_name": "Deep Self-Introspection PIG Report",
            "version": "v0.21.0",
            "layer": "deep_self_introspection",
            "source_layer": "self_awareness",
            "requires_self_awareness_consolidation": "v0.20.9",
            "subjects": [item.subject_id for item in contract.subjects],
            "seed_skill_ids": list(contract.seed_skill_ids),
            "safety_boundary": {
                "read_only": True,
                "mutation_enabled": False,
                "permission_escalation_enabled": False,
                "external_execution_enabled": False,
                "llm_judge_enabled": False,
            },
            "status": "contract_only" if conformance.passed else "failed",
            "conformance_status": conformance.status,
            "canonical_store": "ocel",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        contract = self.registry_service.build_contract()
        conformance = self.conformance_service.run_conformance()
        return {
            "projection_name": "Deep Self-Introspection OCPX Projection",
            "state": "deep_self_introspection_contract_registered",
            "version": "v0.21.0",
            "layer": "deep_self_introspection",
            "source_read_models": [
                "SelfAwarenessReleaseState",
                "SelfAwarenessWorkbenchState",
                "SelfIntentionCandidateState",
                "SelfVerificationState",
                "SelfProjectSurfaceState",
            ],
            "target_read_models": [
                "SelfCapabilityTruthState",
                "SelfRuntimeBoundaryState",
                "SelfPolicyGateState",
                "SelfTraceIntegrityState",
                "SelfContextProjectionState",
                "SelfCandidateMemoryBoundaryState",
                "SelfClaimConsistencyState",
            ],
            "subjects": [item.subject_id for item in contract.subjects],
            "effect_types": ["read_only_observation", "state_candidate_created"],
            "object_coverage": list(contract.ocel_mapping.object_types),
            "event_coverage": list(contract.ocel_mapping.event_types),
            "relation_coverage": list(contract.ocel_mapping.relation_types),
            "conformance_status": conformance.status,
            "canonical_store": "ocel",
        }

    def build_contract_report(self, subject_id: str = "deep_self_introspection") -> DeepSelfIntrospectionReport:
        contract = self.registry_service.build_contract()
        status = "contract_only"
        subject_refs = [{"subject_id": item.subject_id, "status": item.status} for item in contract.subjects]
        return DeepSelfIntrospectionReport(
            report_id=f"deep_self_introspection_report:v0.21.0:{subject_id}",
            version="v0.21.0",
            subject_id=subject_id,
            status=status,
            source_refs=[
                {
                    "ref_type": "self_awareness_consolidation",
                    "ref_id": "v0.20.9",
                    "summary": "Self-Awareness Foundation v1 consolidated read model.",
                }
            ],
            evidence_refs=subject_refs,
            findings=[],
            limitations=[
                "v0.21.0 registers contracts only.",
                "No actual deep introspection analysis is implemented.",
            ],
            withdrawal_conditions=[
                "Withdraw if any seed skill becomes executable.",
                "Withdraw if mutation, permission escalation, external execution, or LLM judge behavior is added.",
                "Withdraw if OCEL mapping is removed or JSONL is introduced as canonical store.",
            ],
            validity_horizon="Valid until v0.21.1 begins subject-specific capability registry awareness.",
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        safety = report["safety_boundary"]
        return "\n".join(
            [
                "Deep Self-Introspection PIG Report",
                "version=v0.21.0",
                "layer=deep_self_introspection",
                "source_layer=self_awareness",
                "requires_self_awareness_consolidation=v0.20.9",
                f"subjects={','.join(report['subjects'])}",
                f"read_only={safety['read_only']}",
                f"mutation_enabled={safety['mutation_enabled']}",
                f"permission_escalation_enabled={safety['permission_escalation_enabled']}",
                f"external_execution_enabled={safety['external_execution_enabled']}",
                f"llm_judge_enabled={safety['llm_judge_enabled']}",
                f"status={report['status']}",
                "canonical_store=ocel",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Deep Self-Introspection OCPX Projection",
                "version=v0.21.0",
                "layer=deep_self_introspection",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                f"conformance_status={projection['conformance_status']}",
                "canonical_store=ocel",
            ]
        )
