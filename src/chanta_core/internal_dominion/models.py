from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


INTERNAL_DOMINION_VERSION = "v0.23.0"
INTERNAL_DOMINION_VERSION_NAME = "OCEL-native Internal Dominion Contract"
INTERNAL_DOMINION_LAYER = "internal_dominion"
INTERNAL_DOMINION_TRACK = "Internal Dominion Foundation"
INTERNAL_DOMINION_STATE = "internal_dominion_contract_registered"


@dataclass(frozen=True)
class InternalSkillTaxonomy:
    categories: list[str] = field(default_factory=lambda: ["observation", "digestion", "dominion"])
    dominion_definition: str = (
        "Vendor-neutral gated control grammar over external runtimes, agents, tools, "
        "workflows, APIs, local runtimes, RPA systems, and enterprise systems."
    )
    dominion_is_vendor_adapter: bool = False
    dominion_is_self_execution: bool = False
    dominion_dispatch_enabled_by_default: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "categories": list(self.categories),
            "dominion_definition": self.dominion_definition,
            "dominion_is_vendor_adapter": self.dominion_is_vendor_adapter,
            "dominion_is_self_execution": self.dominion_is_self_execution,
            "dominion_dispatch_enabled_by_default": self.dominion_dispatch_enabled_by_default,
        }


@dataclass(frozen=True)
class DominionSubject:
    subject_id: str
    name: str
    description: str
    status: str
    provider_neutral: bool
    dispatch_enabled: bool
    introduced_in: str
    ocel_object_types: list[str]
    ocel_event_types: list[str]
    ocel_relation_types: list[str]
    risk_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "subject_id": self.subject_id,
            "name": self.name,
            "description": self.description,
            "status": self.status,
            "provider_neutral": self.provider_neutral,
            "dispatch_enabled": self.dispatch_enabled,
            "introduced_in": self.introduced_in,
            "ocel_object_types": list(self.ocel_object_types),
            "ocel_event_types": list(self.ocel_event_types),
            "ocel_relation_types": list(self.ocel_relation_types),
            "risk_notes": list(self.risk_notes),
        }


@dataclass(frozen=True)
class DominionProviderInterfaceContract:
    provider_types: list[str] = field(
        default_factory=lambda: [
            "local_runtime",
            "rpa_runtime",
            "agent_runtime",
            "workflow_engine",
            "browser_automation",
            "enterprise_api",
            "database_or_etl",
            "custom_system",
        ]
    )
    required_methods: list[str] = field(
        default_factory=lambda: [
            "discover_runtimes",
            "list_capabilities",
            "describe_capability",
            "validate_action",
            "preflight",
            "dispatch",
            "get_status",
            "fetch_output",
            "cancel_or_stop",
            "map_outcome",
        ]
    )
    provider_cannot_bypass_gate: bool = True
    provider_cannot_store_credentials_in_output: bool = True
    provider_must_return_ocel_refs: bool = True
    provider_must_support_status_tracking: bool = True
    provider_must_support_outcome_mapping: bool = True
    contract_only: bool = True
    provider_api_call_enabled: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "provider_types": list(self.provider_types),
            "required_methods": list(self.required_methods),
            "provider_cannot_bypass_gate": self.provider_cannot_bypass_gate,
            "provider_cannot_store_credentials_in_output": self.provider_cannot_store_credentials_in_output,
            "provider_must_return_ocel_refs": self.provider_must_return_ocel_refs,
            "provider_must_support_status_tracking": self.provider_must_support_status_tracking,
            "provider_must_support_outcome_mapping": self.provider_must_support_outcome_mapping,
            "contract_only": self.contract_only,
            "provider_api_call_enabled": self.provider_api_call_enabled,
        }


@dataclass(frozen=True)
class DominionRiskProfile:
    contract_only: bool = True
    external_dispatch_enabled: bool = False
    external_runtime_touch_enabled: bool = False
    provider_api_call_enabled: bool = False
    credential_materialization_enabled: bool = False
    network_enabled: bool = False
    mcp_enabled: bool = False
    plugin_enabled: bool = False
    shell_enabled: bool = False
    local_command_enabled: bool = False
    production_action_enabled: bool = False
    autonomous_dispatch_enabled: bool = False
    memory_mutation_enabled: bool = False
    persona_mutation_enabled: bool = False
    overlay_mutation_enabled: bool = False
    growthkernel_dependency_required: bool = False
    llm_judge_enabled: bool = False
    dangerous_capability: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionGateContract:
    requires_runtime_inventory: bool = True
    requires_capability_observation: bool = True
    requires_capability_digestion: bool = True
    requires_control_request: bool = True
    requires_action_candidate: bool = True
    requires_control_plan: bool = True
    requires_static_safety_check: bool = True
    requires_preflight_before_dispatch: bool = True
    requires_human_gate_for_mutating_action: bool = True
    requires_human_gate_for_production_action: bool = True
    requires_single_use_authorization: bool = True
    requires_idempotency_key: bool = True
    requires_rate_limit_policy: bool = True
    requires_cancel_or_stop_plan: bool = True
    requires_status_tracking: bool = True
    requires_outcome_record: bool = True
    deny_if_credential_exposure_risk: bool = True
    deny_if_provider_bypasses_gate: bool = True
    deny_if_runtime_not_allowlisted: bool = True
    deny_if_capability_not_allowlisted: bool = True

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionObservabilityContract:
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    workbench_visible: bool = True
    envelope_visible: bool = True
    external_control_must_be_ocel_visible: bool = True
    provider_adapter_cannot_bypass_dominion_gate: bool = True

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionEffectPolicy:
    allowed_effect_types_v0_23_0: list[str] = field(
        default_factory=lambda: ["read_only_observation", "state_candidate_created"]
    )
    future_effect_types: list[str] = field(
        default_factory=lambda: [
            "external_runtime_observed",
            "external_action_candidate_created",
            "external_control_plan_created",
            "dominion_gate_created",
            "external_runtime_touched",
            "external_control_dispatched",
            "external_run_started",
            "external_run_status_observed",
            "external_run_output_captured",
            "external_outcome_recorded",
        ]
    )
    forbidden_effect_types_v0_23_0: list[str] = field(
        default_factory=lambda: [
            "external_runtime_touched",
            "external_control_dispatched",
            "external_run_started",
            "network_accessed",
            "plugin_loaded",
            "mcp_connected",
            "shell_executed",
            "workspace_file_changed_by_command",
            "credential_exposed",
        ]
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            "allowed_effect_types_v0_23_0": list(self.allowed_effect_types_v0_23_0),
            "future_effect_types": list(self.future_effect_types),
            "forbidden_effect_types_v0_23_0": list(self.forbidden_effect_types_v0_23_0),
        }


@dataclass(frozen=True)
class DominionMigrationPolicy:
    v0_23_track: str = "Internal Dominion Foundation"
    self_execution_reclassified_to: str = "v0.24.x Local Runtime Provider"
    vendor_adapters_reclassified_to: str = "future external provider skills"
    growthkernel_dependency: str = "future_consumer_not_dependency"
    schumpeter_public_name: str = "ChantaCore Company Edition"
    schumpeter_legacy_status: str = "previous prototype / asset source"

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionMigrationFinding:
    finding_id: str
    finding_type: str
    severity: str
    file_ref: str
    matched_text: str
    recommended_change: str
    fixed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class DominionConformanceFinding:
    finding_id: str
    severity: str
    message: str
    fixed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


@dataclass(frozen=True)
class InternalDominionContractReport:
    report_id: str
    version: str
    layer: str
    subject_id: str
    status: str
    findings: list[DominionConformanceFinding]
    migration_findings: list[DominionMigrationFinding]
    limitations: list[str]
    withdrawal_conditions: list[str]
    validity_horizon: str
    review_status: str = "report_only"

    def to_dict(self) -> dict[str, Any]:
        return {
            "report_id": self.report_id,
            "version": self.version,
            "layer": self.layer,
            "subject_id": self.subject_id,
            "status": self.status,
            "findings": [item.to_dict() for item in self.findings],
            "migration_findings": [item.to_dict() for item in self.migration_findings],
            "limitations": list(self.limitations),
            "withdrawal_conditions": list(self.withdrawal_conditions),
            "validity_horizon": self.validity_horizon,
            "review_status": self.review_status,
        }


@dataclass(frozen=True)
class InternalDominionContract:
    contract_id: str
    version: str
    version_name: str
    track: str
    layer: str
    status: str
    definition: str
    taxonomy: InternalSkillTaxonomy
    subjects: list[DominionSubject]
    seed_skill_ids: list[str]
    provider_interface: DominionProviderInterfaceContract
    risk_profile: DominionRiskProfile
    gate_contract: DominionGateContract
    observability_contract: DominionObservabilityContract
    effect_policy: DominionEffectPolicy
    migration_policy: DominionMigrationPolicy

    def to_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "version": self.version,
            "version_name": self.version_name,
            "track": self.track,
            "layer": self.layer,
            "status": self.status,
            "definition": self.definition,
            "taxonomy": self.taxonomy.to_dict(),
            "subjects": [item.to_dict() for item in self.subjects],
            "seed_skill_ids": list(self.seed_skill_ids),
            "provider_interface": self.provider_interface.to_dict(),
            "risk_profile": self.risk_profile.to_dict(),
            "gate_contract": self.gate_contract.to_dict(),
            "observability_contract": self.observability_contract.to_dict(),
            "effect_policy": self.effect_policy.to_dict(),
            "migration_policy": self.migration_policy.to_dict(),
        }
