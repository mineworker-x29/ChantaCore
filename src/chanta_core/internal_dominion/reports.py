from __future__ import annotations

from typing import Any

from chanta_core.internal_dominion.conformance import DominionConformanceService
from chanta_core.internal_dominion.mapping import (
    DOMINION_EFFECT_TYPES,
    DOMINION_OCEL_EVENT_TYPES,
    DOMINION_OCEL_OBJECT_TYPES,
    DOMINION_OCEL_RELATION_TYPES,
)
from chanta_core.internal_dominion.migration import DominionMigrationAuditService
from chanta_core.internal_dominion.models import (
    INTERNAL_DOMINION_LAYER,
    INTERNAL_DOMINION_STATE,
    INTERNAL_DOMINION_TRACK,
    INTERNAL_DOMINION_VERSION,
    INTERNAL_DOMINION_VERSION_NAME,
    InternalDominionContractReport,
)
from chanta_core.internal_dominion.registry import InternalDominionRegistryService


class InternalDominionReportService:
    def __init__(
        self,
        *,
        registry_service: InternalDominionRegistryService | None = None,
        conformance_service: DominionConformanceService | None = None,
        migration_audit_service: DominionMigrationAuditService | None = None,
    ) -> None:
        self.registry_service = registry_service or InternalDominionRegistryService()
        self.conformance_service = conformance_service or DominionConformanceService(self.registry_service)
        self.migration_audit_service = migration_audit_service or DominionMigrationAuditService()

    def build_contract_report(self) -> InternalDominionContractReport:
        conformance = self.conformance_service.run_conformance()
        migration_findings = self.migration_audit_service.scan_existing_code()
        return InternalDominionContractReport(
            report_id="internal_dominion_contract_report:v0.23.0",
            version=INTERNAL_DOMINION_VERSION,
            layer=INTERNAL_DOMINION_LAYER,
            subject_id="subject:internal_dominion_contract",
            status="contract_only" if conformance.passed else "failed",
            findings=list(conformance.findings),
            migration_findings=migration_findings,
            limitations=[
                "v0.23.0 is contract-only.",
                "No provider adapter dispatch, external runtime touch, provider API call, network, MCP, plugin, shell, local command, or GrowthKernel runtime integration is enabled.",
                "Dispatch/control/run skills are registered only as contract-only stubs.",
            ],
            withdrawal_conditions=[
                "Withdraw if v0.23.x is described as Self-Execution Safety.",
                "Withdraw if provider adapters bypass Dominion gate.",
                "Withdraw if dispatch, external runtime touch, provider API calls, credentials, or GrowthKernel active dependency are introduced.",
            ],
            validity_horizon="Valid until v0.23.1 runtime inventory contract changes or a later provider layer changes Dominion boundaries.",
        )

    def build_pig_report(self) -> dict[str, Any]:
        contract = self.registry_service.build_contract()
        risk = contract.risk_profile
        return {
            "version": INTERNAL_DOMINION_VERSION,
            "layer": INTERNAL_DOMINION_LAYER,
            "subject": "internal_dominion_contract",
            "track": INTERNAL_DOMINION_TRACK,
            "version_name": INTERNAL_DOMINION_VERSION_NAME,
            "taxonomy": {"categories": list(contract.taxonomy.categories)},
            "migration": contract.migration_policy.to_dict(),
            "safety_boundary": {
                "dispatch_enabled": risk.external_dispatch_enabled,
                "external_runtime_touched": risk.external_runtime_touch_enabled,
                "provider_api_call_performed": risk.provider_api_call_enabled,
                "credential_exposed": risk.credential_materialization_enabled,
                "network_enabled": risk.network_enabled,
                "mcp_enabled": risk.mcp_enabled,
                "plugin_enabled": risk.plugin_enabled,
                "llm_judge_enabled": risk.llm_judge_enabled,
                "growthkernel_dependency_required": risk.growthkernel_dependency_required,
            },
            "seed_subjects": [item.subject_id for item in contract.subjects],
            "seed_skill_ids": list(contract.seed_skill_ids),
            "canonical_store": "ocel",
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": INTERNAL_DOMINION_STATE,
            "version": INTERNAL_DOMINION_VERSION,
            "layer": INTERNAL_DOMINION_LAYER,
            "source_read_models": [
                "SelfModificationConsolidationState",
                "DeepSelfConsolidationState",
                "SelfAwarenessConsolidationState",
            ],
            "target_read_models": [
                "InternalDominionContractState",
                "InternalSkillTaxonomyState",
                "DominionProviderInterfaceState",
                "DominionGateContractState",
                "DominionMigrationState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
            "object_coverage": list(DOMINION_OCEL_OBJECT_TYPES),
            "event_coverage": list(DOMINION_OCEL_EVENT_TYPES),
            "relation_coverage": list(DOMINION_OCEL_RELATION_TYPES),
            "canonical_store": "ocel",
        }

    def render_contract_cli(self) -> str:
        contract = self.registry_service.build_contract()
        risk = contract.risk_profile
        return "\n".join(
            [
                "Internal Dominion Contract",
                f"version={contract.version}",
                f"version_name={contract.version_name}",
                f"track={contract.track}",
                f"layer={contract.layer}",
                f"status={contract.status}",
                f"categories={','.join(contract.taxonomy.categories)}",
                "v0.23_self_execution_safety=false",
                "self_execution=v0.24 Local Runtime Provider",
                "GrowthKernel=future_consumer_not_dependency",
                "vendor adapters=future_external_provider_skills",
                f"dispatch_enabled={str(risk.external_dispatch_enabled).lower()}",
                f"external_runtime_touched={str(risk.external_runtime_touch_enabled).lower()}",
                f"provider_api_call_performed={str(risk.provider_api_call_enabled).lower()}",
                f"credential_exposed={str(risk.credential_materialization_enabled)}",
                "canonical_store=ocel",
                "raw_secrets_printed=False",
            ]
        )

    def render_taxonomy_cli(self) -> str:
        taxonomy = self.registry_service.build_contract().taxonomy
        return "\n".join(
            [
                "Internal Skill Taxonomy",
                f"version={INTERNAL_DOMINION_VERSION}",
                f"layer={INTERNAL_DOMINION_LAYER}",
                "status=contract_only",
                f"categories={','.join(taxonomy.categories)}",
                f"dominion_definition={taxonomy.dominion_definition}",
                "vendor_neutral=true",
                "dispatch_enabled=false",
                "external_runtime_touched=false",
                "provider_api_call_performed=false",
                "raw_secrets_printed=False",
            ]
        )

    def render_subjects_cli(self) -> str:
        lines = [
            "Internal Dominion Subjects",
            f"version={INTERNAL_DOMINION_VERSION}",
            f"layer={INTERNAL_DOMINION_LAYER}",
            "status=contract_only",
        ]
        for subject in self.registry_service.list_subjects():
            lines.append(
                f"- subject={subject.subject_id} status={subject.status} "
                f"provider_neutral={str(subject.provider_neutral).lower()} "
                f"dispatch_enabled={str(subject.dispatch_enabled).lower()}"
            )
        lines.extend(
            [
                "external_runtime_touched=false",
                "provider_api_call_performed=false",
                "raw_secrets_printed=False",
            ]
        )
        return "\n".join(lines)

    def render_provider_interface_cli(self) -> str:
        interface = self.registry_service.build_contract().provider_interface
        return "\n".join(
            [
                "Internal Dominion Provider Interface",
                f"version={INTERNAL_DOMINION_VERSION}",
                f"layer={INTERNAL_DOMINION_LAYER}",
                "status=contract_only",
                f"provider_types={','.join(interface.provider_types)}",
                f"required_methods={','.join(interface.required_methods)}",
                f"provider_cannot_bypass_gate={str(interface.provider_cannot_bypass_gate)}",
                f"provider_cannot_store_credentials_in_output={str(interface.provider_cannot_store_credentials_in_output)}",
                f"provider_must_return_ocel_refs={str(interface.provider_must_return_ocel_refs)}",
                f"provider_must_support_status_tracking={str(interface.provider_must_support_status_tracking)}",
                f"provider_must_support_outcome_mapping={str(interface.provider_must_support_outcome_mapping)}",
                "provider_api_call_performed=false",
                "external_runtime_touched=false",
                "raw_secrets_printed=False",
            ]
        )

    def render_migration_audit_cli(self) -> str:
        findings = self.migration_audit_service.scan_existing_code()
        counts: dict[str, int] = {}
        for finding in findings:
            counts[finding.finding_type] = counts.get(finding.finding_type, 0) + 1
        return "\n".join(
            [
                "Internal Dominion Migration Audit",
                f"version={INTERNAL_DOMINION_VERSION}",
                f"layer={INTERNAL_DOMINION_LAYER}",
                "status=read_only",
                f"finding_count={len(findings)}",
                "counts=" + ",".join(f"{key}:{value}" for key, value in sorted(counts.items())),
                "self_execution=v0.24 Local Runtime Provider",
                "GrowthKernel=future_consumer_not_dependency",
                "vendor adapters=future_external_provider_skills",
                "provider_api_call_performed=false",
                "external_runtime_touched=false",
                "raw_secrets_printed=False",
            ]
        )

    def render_pig_report_cli(self) -> str:
        report = self.build_pig_report()
        safety = report["safety_boundary"]
        migration = report["migration"]
        return "\n".join(
            [
                "Internal Dominion PIG Report",
                f"version={report['version']}",
                f"layer={report['layer']}",
                f"subject={report['subject']}",
                f"track={report['track']}",
                f"categories={','.join(report['taxonomy']['categories'])}",
                f"self_execution_reclassified_to={migration['self_execution_reclassified_to']}",
                f"vendor_adapters_reclassified_to={migration['vendor_adapters_reclassified_to']}",
                f"growthkernel_dependency={migration['growthkernel_dependency']}",
                f"dispatch_enabled={str(safety['dispatch_enabled']).lower()}",
                f"external_runtime_touched={str(safety['external_runtime_touched']).lower()}",
                f"provider_api_call_performed={str(safety['provider_api_call_performed']).lower()}",
                f"credential_exposed={str(safety['credential_exposed']).lower()}",
                "canonical_store=ocel",
                "raw_secrets_printed=False",
            ]
        )

    def render_ocpx_projection_cli(self) -> str:
        projection = self.build_ocpx_projection()
        return "\n".join(
            [
                "Internal Dominion OCPX Projection",
                f"version={projection['version']}",
                f"layer={projection['layer']}",
                f"state={projection['state']}",
                f"source_read_models={','.join(projection['source_read_models'])}",
                f"target_read_models={','.join(projection['target_read_models'])}",
                f"effect_types={','.join(projection['effect_types'])}",
                "external_runtime_touched=false",
                "external_control_dispatched=false",
                "provider_api_call_performed=false",
                "canonical_store=ocel",
                "raw_secrets_printed=False",
            ]
        )
