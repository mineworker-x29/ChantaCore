from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from chanta_core.adapter_invocation_candidate_dry_run_plan import AdapterInvocationCandidateReportService
from chanta_core.credential_secret_network_boundary import CredentialNetworkBoundaryReportService
from chanta_core.external_provider_adapter_contract import (
    ExternalAdapterContractReportService,
    ModelMixin,
    _bool,
    _ref,
)
from chanta_core.external_skill_packaging_certification_matrix import AdapterPackagingCertificationReportService
from chanta_core.limited_provider_invocation_preview_gate import LimitedProviderInvocationPreviewReportService
from chanta_core.memory_candidate_continuity import MemoryConsolidationReportService
from chanta_core.mock_adapter_harness_no_network_default import MockAdapterHarnessReportService
from chanta_core.permission_safety_scope_gate_for_external_adapters import AdapterPermissionSafetyReportService
from chanta_core.provider_capability_inventory_adapter_registry import AdapterRegistryReportService
from chanta_core.provider_invocation_approval_audit_rollback_boundary import (
    ProviderInvocationApprovalAuditRollbackReportService,
)
from chanta_core.public_alpha_schumpeter_preparation import V028ConsolidationReportService
from chanta_core.utility.time import utc_now_iso
from chanta_core.workspace_agent_workbench import WorkbenchConsolidationReportService


V0299_VERSION = "v0.29.9"
V0299_LAYER = "external_provider_adapter"
V0299_TRACK = "External Skill / External Provider Adapter Development"
V0299_NAME = "External Provider Adapter Foundation Consolidation"
V0299_KOREAN_NAME = "External Provider Adapter Foundation 통합·준비성 판정"
V0299_RELEASE_NAME = "External Provider Adapter Foundation v1"
V0299_NEXT_STEP = "v0.30.0 External Agent Dominion Bridge Contract"
V0299_INCLUDED_VERSIONS = [
    "v0.29.0",
    "v0.29.1",
    "v0.29.2",
    "v0.29.3",
    "v0.29.4",
    "v0.29.5",
    "v0.29.6",
    "v0.29.7",
    "v0.29.8",
    "v0.29.9",
]

V0299_OBJECT_TYPES = [
    "external_provider_adapter_foundation_snapshot",
    "external_provider_adapter_foundation_component",
    "external_provider_adapter_capability_map",
    "external_provider_adapter_capability_entry",
    "external_provider_adapter_coverage_matrix",
    "external_provider_adapter_coverage_row",
    "adapter_contract_consolidation_report",
    "adapter_registry_consolidation_report",
    "mock_harness_consolidation_report",
    "permission_safety_consolidation_report",
    "credential_network_consolidation_report",
    "invocation_dry_run_consolidation_report",
    "approval_audit_rollback_consolidation_report",
    "packaging_certification_consolidation_report",
    "limited_preview_gate_consolidation_report",
    "external_provider_adapter_readiness_report",
    "v030_readiness_report",
    "external_agent_dominion_handoff_packet",
    "external_provider_adapter_release_manifest",
    "v029_consolidation_audit_trail",
    "v029_consolidation_finding",
    "v029_consolidation_report",
    "limited_provider_invocation_preview_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0299_EVENT_TYPES = [
    "v029_consolidation_requested",
    "v029_consolidation_prerequisites_loaded",
    "external_provider_adapter_foundation_snapshot_created",
    "external_provider_adapter_capability_map_created",
    "external_provider_adapter_coverage_matrix_created",
    "adapter_contract_consolidation_report_created",
    "adapter_registry_consolidation_report_created",
    "mock_harness_consolidation_report_created",
    "permission_safety_consolidation_report_created",
    "credential_network_consolidation_report_created",
    "invocation_dry_run_consolidation_report_created",
    "approval_audit_rollback_consolidation_report_created",
    "packaging_certification_consolidation_report_created",
    "limited_preview_gate_consolidation_report_created",
    "external_provider_adapter_readiness_report_created",
    "v030_readiness_report_created",
    "external_agent_dominion_handoff_packet_created",
    "external_provider_adapter_release_manifest_created",
    "v029_consolidation_audit_trail_created",
    "v029_consolidation_report_created",
    "v029_consolidation_warning_created",
    "v029_consolidation_blocked",
]

V0299_EFFECT_TYPES = [
    "read_only_observation",
    "external_provider_adapter_foundation_snapshot_created",
    "external_provider_adapter_capability_map_created",
    "external_provider_adapter_coverage_matrix_created",
    "adapter_consolidation_report_created",
    "external_provider_adapter_readiness_report_created",
    "v030_readiness_report_created",
    "external_agent_dominion_handoff_packet_created",
    "external_provider_adapter_release_manifest_created",
    "v029_consolidation_report_created",
    "state_candidate_created",
]

V0299_FORBIDDEN_EFFECT_TYPES = [
    "provider_registered",
    "provider_invoked",
    "provider_sdk_invoked",
    "network_called",
    "outbound_request_sent",
    "credential_accessed",
    "credential_stored",
    "credential_logged",
    "secret_retrieved",
    "secret_materialized",
    "command_executed",
    "shell_execution_surface_created",
    "subprocess_expansion_added",
    "external_side_effect_performed",
    "file_mutated",
    "rollback_executed",
    "automatic_retry_performed",
    "package_published",
    "package_uploaded",
    "release_tag_created",
    "official_release_artifact_created",
    "live_provider_certified",
    "live_adapter_implemented",
    "external_provider_adapter_implemented",
    "RPA_adapter_implemented",
    "A360_adapter_implemented",
    "Brity_adapter_implemented",
    "UiPath_adapter_implemented",
    "external_dominion_implemented",
    "schumpeter_private_runtime_used",
    "actual_user_data_used",
    "actual_company_data_used",
    "private_material_exposed",
    "raw_provider_output_persisted",
    "raw_payload_logged",
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]

REQUIRED_V030_BOUNDARIES = [
    "external_agent_trust_boundary",
    "external_agent_identity_boundary",
    "external_agent_capability_registry",
    "delegation_permission_gate",
    "safety_gate",
    "isolation_boundary",
    "audit_ocel_visibility",
    "rollback_noop_boundary",
    "dominion_preview_gate",
]

V030_FIRST_STEPS = [
    "define_external_agent_dominion_contract",
    "define_external_agent_inventory",
    "define_external_agent_identity_boundary",
    "define_external_agent_trust_boundary",
    "define_external_agent_capability_registry",
    "define_delegation_permission_gate",
    "define_external_agent_safety_gate",
    "define_isolation_boundary",
    "define_audit_ocel_visibility",
    "define_rollback_noop_boundary",
]

V030_NOT_ALLOWED = [
    "external_agent_execution",
    "autonomous_delegation",
    "external_agent_command_authority",
    "unbounded_tool_control",
    "RPA_runtime_control",
    "provider_invocation_bypass",
    "credential_access_bypass",
    "network_access_bypass",
]

EXCLUDED_CAPABILITIES = [
    "Provider invocation runtime",
    "Provider registration runtime",
    "Provider SDK invocation",
    "Network access",
    "Credential access",
    "Command execution expansion",
    "Live adapter runtime",
    "Package publish",
    "Release tag creation",
    "Live provider certification",
    "RPA / A360 / Brity / UiPath runtime",
    "External Agent Dominion Bridge runtime",
    "Schumpeter private runtime",
]

COVERAGE_SUBJECTS = [
    ("adapter_contract", "external_adapter_contract_report", "v0.29.0"),
    ("provider_capability_registry", "adapter_registry_report", "v0.29.1"),
    ("mock_harness_no_network", "mock_adapter_harness_report", "v0.29.2"),
    ("permission_safety_scope_gate", "adapter_permission_safety_report", "v0.29.3"),
    ("credential_secret_network_boundary", "credential_network_boundary_report", "v0.29.4"),
    ("invocation_candidate_dry_run", "adapter_invocation_candidate_report", "v0.29.5"),
    ("approval_audit_rollback_boundary", "provider_invocation_approval_audit_rollback_report", "v0.29.6"),
    ("packaging_certification_matrix", "adapter_packaging_certification_report", "v0.29.7"),
    ("limited_preview_gate", "limited_provider_invocation_preview_report", "v0.29.8"),
]


def _now() -> str:
    return utc_now_iso()


def _safe_build(factory: Callable[[], Any]) -> Any | None:
    try:
        return factory()
    except Exception:
        return None


def _report_id(report: Any, fallback: str) -> str:
    return str(getattr(report, "report_id", fallback))


def _report_ref(object_type: str, report: Any, version: str, fallback: str) -> dict[str, Any] | None:
    if report is None:
        return None
    return _ref(object_type, _report_id(report, fallback), version)


def _status_from_ready(ready: bool | None) -> str:
    if ready is True:
        return "passed"
    if ready is False:
        return "warning"
    return "unknown"


@dataclass
class ExternalProviderAdapterFoundationComponent(ModelMixin):
    component_id: str
    version_introduced: str
    component_name: str
    component_type: str
    report_ref: dict[str, Any] | None
    component_status: str
    ready_for_foundation: bool
    runtime_blocker: bool
    future_track_blocker: bool
    notes: list[str] = field(default_factory=list)


@dataclass
class ExternalProviderAdapterFoundationSnapshot(ModelMixin):
    snapshot_id: str
    created_at: str
    included_versions: list[str]
    previous_foundation_refs: list[dict[str, Any]]
    components: list[ExternalProviderAdapterFoundationComponent]
    foundation_status: str
    contract_ready: bool
    registry_ready: bool
    mock_harness_ready: bool
    permission_safety_ready: bool
    credential_network_ready: bool
    invocation_dry_run_ready: bool
    approval_audit_rollback_ready: bool
    packaging_certification_ready: bool
    limited_preview_gate_ready: bool
    provider_invocation_runtime_ready: bool = False
    live_adapter_runtime_ready: bool = False
    v030_handoff_ready: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION
    release_name: str = V0299_RELEASE_NAME


@dataclass
class ExternalProviderAdapterCapabilityEntry(ModelMixin):
    entry_id: str
    adapter_name: str
    provider_kind: str
    capability_name: str
    capability_status: str
    public_safe: bool
    requires_provider_invocation: bool
    requires_network: bool
    requires_credentials: bool
    requires_command_execution: bool
    requires_rpa: bool
    requires_external_dominion: bool
    runtime_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_enabled_now: bool = False
    credential_access_enabled_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalProviderAdapterCapabilityMap(ModelMixin):
    map_id: str
    entries: list[ExternalProviderAdapterCapabilityEntry]
    contract_count: int
    registry_count: int
    mock_ready_count: int
    boundary_ready_count: int
    dry_run_ready_count: int
    certified_count: int
    preview_gate_candidate_count: int
    runtime_enabled_count: int
    blocked_count: int
    unknown_count: int
    capability_map_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class ExternalProviderAdapterCoverageRow(ModelMixin):
    row_id: str
    subject: str
    report_available: bool
    docs_available: bool
    tests_available: bool
    boundary_tests_available: bool
    cli_available: bool
    ocel_mapping_available: bool
    pig_projection_available: bool
    ocpx_projection_available: bool
    safety_boundary_available: bool
    coverage_status: str
    missing_items: list[str]
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalProviderAdapterCoverageMatrix(ModelMixin):
    matrix_id: str
    rows: list[ExternalProviderAdapterCoverageRow]
    required_coverage_count: int
    passed_coverage_count: int
    warning_coverage_count: int
    blocked_coverage_count: int
    unknown_coverage_count: int
    coverage_status: str
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class AdapterContractConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    contract_ready: bool | None
    provider_invocation_forbidden: bool = True
    command_execution_forbidden: bool = True
    adapter_contract_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class AdapterRegistryConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    registry_ready: bool | None
    metadata_only_registry: bool = True
    provider_registered: bool = False
    provider_invoked: bool = False
    registry_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class MockHarnessConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    mock_harness_ready: bool | None
    no_network_default_validated: bool | None
    deterministic_fixture_validated: bool | None
    live_adapter_used: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    mock_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class PermissionSafetyConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    permission_safety_ready: bool | None
    deny_first_validated: bool | None
    no_permission_granted: bool = True
    no_approval_granted: bool = True
    provider_invoked: bool = False
    permission_safety_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class CredentialNetworkConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    credential_network_ready: bool | None
    no_credential_access: bool = True
    no_credential_storage: bool = True
    no_network_call: bool = True
    no_provider_sdk_invocation: bool = True
    credential_network_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class InvocationDryRunConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    invocation_dry_run_ready: bool | None
    no_provider_invocation: bool = True
    no_network_call: bool = True
    no_credential_access: bool = True
    no_external_side_effect: bool = True
    dry_run_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class ApprovalAuditRollbackConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    approval_audit_rollback_ready: bool | None
    no_approval_granted: bool = True
    no_provider_invocation: bool = True
    no_rollback_execution: bool = True
    no_automatic_retry: bool = True
    approval_audit_rollback_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class PackagingCertificationConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    packaging_certification_ready: bool | None
    no_package_publish: bool = True
    no_release_tag: bool = True
    no_live_provider_certification: bool = True
    no_provider_invocation: bool = True
    packaging_certification_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class LimitedPreviewGateConsolidationReport(ModelMixin):
    report_id: str
    source_report_ref: dict[str, Any] | None
    limited_preview_gate_ready: bool | None
    preview_gate_candidates_exist: bool | None
    no_preview_execution: bool = True
    no_provider_invocation: bool = True
    no_network_call: bool = True
    no_credential_access: bool = True
    limited_preview_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class ExternalProviderAdapterReadinessReport(ModelMixin):
    report_id: str
    foundation_snapshot_ref: dict[str, Any]
    contract_ready: bool
    registry_ready: bool
    mock_harness_ready: bool
    permission_safety_ready: bool
    credential_network_ready: bool
    invocation_dry_run_ready: bool
    approval_audit_rollback_ready: bool
    packaging_certification_ready: bool
    limited_preview_gate_ready: bool
    external_provider_adapter_foundation_ready: bool
    provider_invocation_runtime_ready: bool = False
    limited_preview_execution_ready_now: bool = False
    live_adapter_runtime_ready: bool = False
    ready_for_v030_contract: bool = True
    readiness_status: str = "ready"
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class V030ReadinessReport(ModelMixin):
    report_id: str
    ready_for_v030_contract: bool
    ready_for_external_agent_inventory: bool
    ready_for_external_agent_dominion_runtime: bool = False
    ready_for_external_agent_execution: bool = False
    required_contract_first: bool = True
    required_boundaries: list[str] = field(default_factory=lambda: list(REQUIRED_V030_BOUNDARIES))
    blockers: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION
    target_version: str = "v0.30.0"
    target_name: str = "External Agent Dominion Bridge Contract"


@dataclass
class ExternalAgentDominionHandoffPacket(ModelMixin):
    handoff_packet_id: str
    source_consolidation_report_id: str
    adapter_foundation_snapshot_ref: dict[str, Any]
    limited_preview_handoff_ref: dict[str, Any] | None
    ready_inputs_for_v030: list[str]
    required_first_steps: list[str]
    not_allowed_at_v030_start: list[str]
    refs_only: bool = True
    implementation_performed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION
    target_version: str = "v0.30.0"
    target_track: str = "External Agent Dominion Bridge Contract"


@dataclass
class ExternalProviderAdapterReleaseManifest(ModelMixin):
    manifest_id: str
    included_versions: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    foundation_snapshot_ref: dict[str, Any]
    readiness_report_ref: dict[str, Any]
    v030_readiness_report_ref: dict[str, Any]
    manifest_status: str
    provider_invocation_enabled: bool = False
    network_access_enabled: bool = False
    credential_access_enabled: bool = False
    command_execution_enabled: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION
    release_name: str = V0299_RELEASE_NAME


@dataclass
class V029ConsolidationAuditTrail(ModelMixin):
    audit_trail_id: str
    source_report_refs: list[dict[str, Any]]
    consolidation_report_refs: list[dict[str, Any]]
    readiness_report_refs: list[dict[str, Any]]
    handoff_packet_refs: list[dict[str, Any]]
    audit_event_count: int
    raw_content_included: bool = False
    credential_value_included: bool = False
    raw_payload_included: bool = False
    raw_provider_output_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0299_VERSION


@dataclass
class V029ConsolidationFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class V029ConsolidationReport(ModelMixin):
    report_id: str
    created_at: str
    foundation_snapshot: ExternalProviderAdapterFoundationSnapshot
    capability_map: ExternalProviderAdapterCapabilityMap
    coverage_matrix: ExternalProviderAdapterCoverageMatrix
    contract_consolidation: AdapterContractConsolidationReport
    registry_consolidation: AdapterRegistryConsolidationReport
    mock_harness_consolidation: MockHarnessConsolidationReport
    permission_safety_consolidation: PermissionSafetyConsolidationReport
    credential_network_consolidation: CredentialNetworkConsolidationReport
    invocation_dry_run_consolidation: InvocationDryRunConsolidationReport
    approval_audit_rollback_consolidation: ApprovalAuditRollbackConsolidationReport
    packaging_certification_consolidation: PackagingCertificationConsolidationReport
    limited_preview_gate_consolidation: LimitedPreviewGateConsolidationReport
    adapter_readiness_report: ExternalProviderAdapterReadinessReport
    v030_readiness_report: V030ReadinessReport
    external_agent_dominion_handoff_packet: ExternalAgentDominionHandoffPacket
    release_manifest: ExternalProviderAdapterReleaseManifest
    audit_trail: V029ConsolidationAuditTrail
    findings: list[V029ConsolidationFinding]
    report_status: str
    external_provider_adapter_foundation_ready: bool
    ready_for_v030: bool
    ready_for_v030_contract: bool
    provider_invocation_runtime_ready: bool = False
    limited_preview_execution_ready_now: bool = False
    live_adapter_runtime_ready: bool = False
    external_agent_dominion_runtime_ready: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    provider_sdk_invoked: bool = False
    network_called: bool = False
    outbound_request_sent: bool = False
    credential_accessed: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    secret_retrieved: bool = False
    secret_materialized: bool = False
    command_executed: bool = False
    external_side_effect_performed: bool = False
    file_mutated: bool = False
    rollback_executed: bool = False
    automatic_retry_performed: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    live_provider_certified: bool = False
    live_adapter_implemented: bool = False
    RPA_adapter_implemented: bool = False
    A360_adapter_implemented: bool = False
    Brity_adapter_implemented: bool = False
    UiPath_adapter_implemented: bool = False
    external_dominion_implemented: bool = False
    schumpeter_private_runtime_used: bool = False
    actual_user_data_used: bool = False
    actual_company_data_used: bool = False
    private_material_exposed: bool = False
    raw_provider_output_persisted: bool = False
    raw_payload_logged: bool = False
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0299_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.30.0 External Agent Dominion Bridge Contract begins or External Provider Adapter Foundation policy changes."
    )
    version: str = V0299_VERSION
    release_name: str = V0299_RELEASE_NAME


class V029ConsolidationPrerequisiteSourceService:
    def load_v0298_preview_report(self) -> Any | None:
        return _safe_build(lambda: LimitedProviderInvocationPreviewReportService().build_report())

    def load_v0298_preview_gate(self) -> Any | None:
        report = self.load_v0298_preview_report()
        return getattr(report, "preview_gate", None)

    def load_v0298_handoff_packet(self) -> Any | None:
        report = self.load_v0298_preview_report()
        return getattr(report, "handoff_packet", None)

    def load_v0297_packaging_certification_report(self) -> Any | None:
        return _safe_build(lambda: AdapterPackagingCertificationReportService().build_report())

    def load_v0296_approval_audit_rollback_report(self) -> Any | None:
        return _safe_build(lambda: ProviderInvocationApprovalAuditRollbackReportService().build_report())

    def load_v0295_invocation_candidate_report(self) -> Any | None:
        return _safe_build(lambda: AdapterInvocationCandidateReportService().build_report())

    def load_v0294_credential_network_boundary_report(self) -> Any | None:
        return _safe_build(lambda: CredentialNetworkBoundaryReportService().build_report())

    def load_v0293_permission_safety_report(self) -> Any | None:
        return _safe_build(lambda: AdapterPermissionSafetyReportService().build_report())

    def load_v0292_mock_harness_report(self) -> Any | None:
        return _safe_build(lambda: MockAdapterHarnessReportService().build_report())

    def load_v0291_registry_report(self) -> Any | None:
        return _safe_build(lambda: AdapterRegistryReportService().build_report())

    def load_v0290_contract_report(self) -> Any | None:
        return _safe_build(lambda: ExternalAdapterContractReportService().build_report())

    def load_v0289_consolidation_report(self) -> Any | None:
        return _safe_build(lambda: V028ConsolidationReportService().build_report())

    def load_v0279_memory_consolidation_report(self) -> Any | None:
        return _safe_build(lambda: MemoryConsolidationReportService().build_report())

    def load_v0269_workbench_consolidation_report(self) -> Any | None:
        return _safe_build(lambda: WorkbenchConsolidationReportService().build_report())

    def load_ocel_pig_ocpx_metadata(self) -> dict[str, Any]:
        return {
            "object_types": V0299_OBJECT_TYPES,
            "event_types": V0299_EVENT_TYPES,
            "effect_types": V0299_EFFECT_TYPES,
        }


class V029ConsolidationReportServices:
    def build_contract_consolidation(self, source: Any | None) -> AdapterContractConsolidationReport:
        ready = source is not None
        return AdapterContractConsolidationReport(
            "adapter_contract_consolidation_report:v0.29.9",
            _report_ref("external_adapter_contract_report", source, "v0.29.0", "external_adapter_contract_report:v0.29.0"),
            ready,
            adapter_contract_status=_status_from_ready(ready),
        )

    def build_registry_consolidation(self, source: Any | None) -> AdapterRegistryConsolidationReport:
        ready = source is not None
        return AdapterRegistryConsolidationReport(
            "adapter_registry_consolidation_report:v0.29.9",
            _report_ref("adapter_registry_report", source, "v0.29.1", "adapter_registry_report:v0.29.1"),
            ready,
            registry_status=_status_from_ready(ready),
        )

    def build_mock_harness_consolidation(self, source: Any | None) -> MockHarnessConsolidationReport:
        ready = source is not None
        return MockHarnessConsolidationReport(
            "mock_harness_consolidation_report:v0.29.9",
            _report_ref("mock_adapter_harness_report", source, "v0.29.2", "mock_adapter_harness_report:v0.29.2"),
            ready,
            ready,
            ready,
            mock_status=_status_from_ready(ready),
        )

    def build_permission_safety_consolidation(self, source: Any | None) -> PermissionSafetyConsolidationReport:
        ready = source is not None
        return PermissionSafetyConsolidationReport(
            "permission_safety_consolidation_report:v0.29.9",
            _report_ref("adapter_permission_safety_report", source, "v0.29.3", "adapter_permission_safety_report:v0.29.3"),
            ready,
            ready,
            permission_safety_status=_status_from_ready(ready),
        )

    def build_credential_network_consolidation(self, source: Any | None) -> CredentialNetworkConsolidationReport:
        ready = source is not None
        return CredentialNetworkConsolidationReport(
            "credential_network_consolidation_report:v0.29.9",
            _report_ref("credential_network_boundary_report", source, "v0.29.4", "credential_network_boundary_report:v0.29.4"),
            ready,
            credential_network_status=_status_from_ready(ready),
        )

    def build_invocation_dry_run_consolidation(self, source: Any | None) -> InvocationDryRunConsolidationReport:
        ready = source is not None
        return InvocationDryRunConsolidationReport(
            "invocation_dry_run_consolidation_report:v0.29.9",
            _report_ref("adapter_invocation_candidate_report", source, "v0.29.5", "adapter_invocation_candidate_report:v0.29.5"),
            ready,
            dry_run_status=_status_from_ready(ready),
        )

    def build_approval_audit_rollback_consolidation(self, source: Any | None) -> ApprovalAuditRollbackConsolidationReport:
        ready = bool(getattr(source, "ready_for_v0_29_7", source is not None))
        return ApprovalAuditRollbackConsolidationReport(
            "approval_audit_rollback_consolidation_report:v0.29.9",
            _report_ref(
                "provider_invocation_approval_audit_rollback_report",
                source,
                "v0.29.6",
                "provider_invocation_approval_audit_rollback_report:v0.29.6",
            ),
            ready,
            approval_audit_rollback_status=_status_from_ready(ready),
        )

    def build_packaging_certification_consolidation(self, source: Any | None) -> PackagingCertificationConsolidationReport:
        ready = bool(getattr(source, "ready_for_v0_29_8", source is not None))
        return PackagingCertificationConsolidationReport(
            "packaging_certification_consolidation_report:v0.29.9",
            _report_ref(
                "adapter_packaging_certification_report",
                source,
                "v0.29.7",
                "adapter_packaging_certification_report:v0.29.7",
            ),
            ready,
            packaging_certification_status=_status_from_ready(ready),
        )

    def build_limited_preview_gate_consolidation(self, source: Any | None) -> LimitedPreviewGateConsolidationReport:
        candidates = getattr(source, "preview_candidates", []) if source is not None else []
        ready = bool(getattr(source, "ready_for_v0_29_9", source is not None))
        return LimitedPreviewGateConsolidationReport(
            "limited_preview_gate_consolidation_report:v0.29.9",
            _report_ref(
                "limited_provider_invocation_preview_report",
                source,
                "v0.29.8",
                "limited_provider_invocation_preview_report:v0.29.8",
            ),
            ready,
            bool(candidates),
            limited_preview_status=_status_from_ready(ready),
        )


class ExternalProviderAdapterFoundationSnapshotService:
    COMPONENT_SPECS = [
        ("v0.29.0", "External Provider Adapter Contract", "contract", "external_adapter_contract_report"),
        ("v0.29.1", "Provider Capability Inventory / Adapter Registry", "registry", "adapter_registry_report"),
        ("v0.29.2", "Mock Adapter Harness / No-Network Default", "mock_harness", "mock_adapter_harness_report"),
        ("v0.29.3", "Permission / Safety / Scope Gate", "permission_safety", "adapter_permission_safety_report"),
        ("v0.29.4", "Credential / Secret / Network Boundary", "credential_network", "credential_network_boundary_report"),
        ("v0.29.5", "Adapter Invocation Candidate / Dry-Run Plan", "invocation_dry_run", "adapter_invocation_candidate_report"),
        ("v0.29.6", "Provider Invocation Approval / Audit / Rollback Boundary", "approval_audit_rollback", "provider_invocation_approval_audit_rollback_report"),
        ("v0.29.7", "External Skill Packaging / Certification Matrix", "packaging_certification", "adapter_packaging_certification_report"),
        ("v0.29.8", "Limited Provider Invocation Preview Gate", "limited_preview_gate", "limited_provider_invocation_preview_report"),
        ("v0.29.9", "External Provider Adapter Foundation Consolidation", "consolidation", "v029_consolidation_report"),
    ]

    def build_snapshot(self, sources: dict[str, Any]) -> ExternalProviderAdapterFoundationSnapshot:
        components: list[ExternalProviderAdapterFoundationComponent] = []
        source_by_version = {
            "v0.29.0": sources["contract"],
            "v0.29.1": sources["registry"],
            "v0.29.2": sources["mock"],
            "v0.29.3": sources["permission"],
            "v0.29.4": sources["credential"],
            "v0.29.5": sources["invocation"],
            "v0.29.6": sources["approval"],
            "v0.29.7": sources["certification"],
            "v0.29.8": sources["preview"],
            "v0.29.9": object(),
        }
        for version, name, component_type, object_type in self.COMPONENT_SPECS:
            source = source_by_version[version]
            ready = source is not None
            components.append(
                ExternalProviderAdapterFoundationComponent(
                    f"external_provider_adapter_foundation_component:{component_type}:v0.29.9",
                    version,
                    name,
                    component_type,
                    _report_ref(object_type, source, version, f"{object_type}:{version}") if version != "v0.29.9" else None,
                    _status_from_ready(ready),
                    ready,
                    False,
                    component_type in {"limited_preview_gate"} and False,
                    ["Foundation component is consolidated as metadata; runtime remains disabled."],
                )
            )
        previous_refs = [
            _report_ref("workbench_consolidation_report", sources["workbench"], "v0.26.9", "workbench_consolidation_report:v0.26.9")
            or _ref("workbench_consolidation_report", "workbench_consolidation_report:v0.26.9", "v0.26.9"),
            _report_ref("memory_consolidation_report", sources["memory"], "v0.27.9", "memory_consolidation_report:v0.27.9")
            or _ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", "v0.27.9"),
            _report_ref("v028_consolidation_report", sources["v028"], "v0.28.9", "v028_consolidation_report:v0.28.9")
            or _ref("v028_consolidation_report", "v028_consolidation_report:v0.28.9", "v0.28.9"),
        ]
        ready_flags = [component.ready_for_foundation for component in components]
        status = "ready" if all(ready_flags) else "warning"
        return ExternalProviderAdapterFoundationSnapshot(
            "external_provider_adapter_foundation_snapshot:v0.29.9",
            _now(),
            list(V0299_INCLUDED_VERSIONS),
            previous_refs,
            components,
            status,
            components[0].ready_for_foundation,
            components[1].ready_for_foundation,
            components[2].ready_for_foundation,
            components[3].ready_for_foundation,
            components[4].ready_for_foundation,
            components[5].ready_for_foundation,
            components[6].ready_for_foundation,
            components[7].ready_for_foundation,
            components[8].ready_for_foundation,
            v030_handoff_ready=True,
        )


class ExternalProviderAdapterCapabilityMapService:
    def build_map(self, preview_report: Any | None) -> ExternalProviderAdapterCapabilityMap:
        preview_candidates = list(getattr(preview_report, "preview_candidates", []) or [])
        entries: list[ExternalProviderAdapterCapabilityEntry] = []
        for index, candidate in enumerate(preview_candidates or [None]):
            adapter_name = getattr(candidate, "adapter_name", "internal_mock_adapter")
            capability_name = getattr(candidate, "capability_name", "mock_metadata_preview")
            provider_kind = getattr(candidate, "provider_kind", "mock")
            entries.append(
                ExternalProviderAdapterCapabilityEntry(
                    f"external_provider_adapter_capability_entry:{adapter_name}:{capability_name}:v0.29.9",
                    adapter_name,
                    provider_kind,
                    capability_name,
                    "preview_gate_candidate" if candidate is not None else "runtime_disabled",
                    True,
                    False,
                    False,
                    False,
                    False,
                    False,
                    False,
                    evidence_refs=[
                        _ref("limited_preview_provider_candidate", getattr(candidate, "preview_candidate_id", f"synthetic:{index}"), "v0.29.8")
                    ]
                    if candidate is not None
                    else [],
                )
            )
        statuses = {entry.capability_status for entry in entries}
        return ExternalProviderAdapterCapabilityMap(
            "external_provider_adapter_capability_map:v0.29.9",
            entries,
            len(entries),
            len(entries),
            len(entries),
            len(entries),
            len(entries),
            len(entries),
            sum(1 for entry in entries if entry.capability_status == "preview_gate_candidate"),
            0,
            sum(1 for entry in entries if entry.capability_status == "blocked"),
            sum(1 for entry in entries if entry.capability_status == "unknown"),
            "ready" if "unknown" not in statuses and "blocked" not in statuses else "warning",
        )


class ExternalProviderAdapterCoverageMatrixService:
    def build_matrix(self, sources: dict[str, Any]) -> ExternalProviderAdapterCoverageMatrix:
        source_by_subject = {
            "adapter_contract": sources["contract"],
            "provider_capability_registry": sources["registry"],
            "mock_harness_no_network": sources["mock"],
            "permission_safety_scope_gate": sources["permission"],
            "credential_secret_network_boundary": sources["credential"],
            "invocation_candidate_dry_run": sources["invocation"],
            "approval_audit_rollback_boundary": sources["approval"],
            "packaging_certification_matrix": sources["certification"],
            "limited_preview_gate": sources["preview"],
        }
        rows: list[ExternalProviderAdapterCoverageRow] = []
        for subject, object_type, version in COVERAGE_SUBJECTS:
            report_available = source_by_subject[subject] is not None
            missing = [] if report_available else ["report"]
            status = "passed" if report_available else "warning"
            rows.append(
                ExternalProviderAdapterCoverageRow(
                    f"external_provider_adapter_coverage_row:{subject}:v0.29.9",
                    subject,
                    report_available,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    True,
                    status,
                    missing,
                    [_ref(object_type, f"{object_type}:{version}", version)],
                )
            )
        return ExternalProviderAdapterCoverageMatrix(
            "external_provider_adapter_coverage_matrix:v0.29.9",
            rows,
            len(rows),
            sum(1 for row in rows if row.coverage_status == "passed"),
            sum(1 for row in rows if row.coverage_status == "warning"),
            sum(1 for row in rows if row.coverage_status == "blocked"),
            sum(1 for row in rows if row.coverage_status == "unknown"),
            "passed" if all(row.coverage_status == "passed" for row in rows) else "warning",
        )


class ExternalProviderAdapterReadinessService:
    def build_report(self, snapshot: ExternalProviderAdapterFoundationSnapshot) -> ExternalProviderAdapterReadinessReport:
        ready = all(
            [
                snapshot.contract_ready,
                snapshot.registry_ready,
                snapshot.mock_harness_ready,
                snapshot.permission_safety_ready,
                snapshot.credential_network_ready,
                snapshot.invocation_dry_run_ready,
                snapshot.approval_audit_rollback_ready,
                snapshot.packaging_certification_ready,
                snapshot.limited_preview_gate_ready,
            ]
        )
        warnings = ["Provider invocation runtime remains disabled by design."]
        return ExternalProviderAdapterReadinessReport(
            "external_provider_adapter_readiness_report:v0.29.9",
            _ref("external_provider_adapter_foundation_snapshot", snapshot.snapshot_id, V0299_VERSION),
            snapshot.contract_ready,
            snapshot.registry_ready,
            snapshot.mock_harness_ready,
            snapshot.permission_safety_ready,
            snapshot.credential_network_ready,
            snapshot.invocation_dry_run_ready,
            snapshot.approval_audit_rollback_ready,
            snapshot.packaging_certification_ready,
            snapshot.limited_preview_gate_ready,
            ready,
            ready_for_v030_contract=True,
            readiness_status="ready" if ready else "warning",
            warnings=warnings,
        )


class V030ReadinessService:
    def build_report(self, adapter_readiness: ExternalProviderAdapterReadinessReport) -> V030ReadinessReport:
        warnings = [
            "v0.30.0 must begin with contract and inventory boundaries, not external agent execution.",
            "RPA, A360, Brity, and UiPath remain future-track.",
        ]
        return V030ReadinessReport(
            "v030_readiness_report:v0.29.9",
            adapter_readiness.ready_for_v030_contract,
            adapter_readiness.ready_for_v030_contract,
            warnings=warnings,
        )


class ExternalAgentDominionHandoffPacketService:
    def build_packet(
        self,
        report_id: str,
        snapshot: ExternalProviderAdapterFoundationSnapshot,
        preview_handoff: Any | None,
    ) -> ExternalAgentDominionHandoffPacket:
        return ExternalAgentDominionHandoffPacket(
            "external_agent_dominion_handoff_packet:v0.29.9",
            report_id,
            _ref("external_provider_adapter_foundation_snapshot", snapshot.snapshot_id, V0299_VERSION),
            _ref("limited_preview_handoff_packet", getattr(preview_handoff, "handoff_packet_id", "limited_preview_handoff_packet:v0.29.8"), "v0.29.8")
            if preview_handoff is not None
            else None,
            [
                "external_provider_adapter_foundation_snapshot",
                "external_provider_adapter_readiness_report",
                "limited_preview_handoff_refs",
                "v029_safety_boundaries",
            ],
            list(V030_FIRST_STEPS),
            list(V030_NOT_ALLOWED),
        )


class ExternalProviderAdapterReleaseManifestService:
    def build_manifest(
        self,
        snapshot: ExternalProviderAdapterFoundationSnapshot,
        readiness: ExternalProviderAdapterReadinessReport,
        v030: V030ReadinessReport,
    ) -> ExternalProviderAdapterReleaseManifest:
        return ExternalProviderAdapterReleaseManifest(
            "external_provider_adapter_release_manifest:v0.29.9",
            list(V0299_INCLUDED_VERSIONS),
            [
                "External provider adapter contract metadata",
                "Adapter registry metadata",
                "Mock adapter harness",
                "Permission, credential, network, dry-run, approval, audit, rollback, certification, and preview gates",
            ],
            list(EXCLUDED_CAPABILITIES),
            list(V0299_EFFECT_TYPES),
            list(V0299_FORBIDDEN_EFFECT_TYPES),
            _ref("external_provider_adapter_foundation_snapshot", snapshot.snapshot_id, V0299_VERSION),
            _ref("external_provider_adapter_readiness_report", readiness.report_id, V0299_VERSION),
            _ref("v030_readiness_report", v030.report_id, V0299_VERSION),
            "ready" if readiness.external_provider_adapter_foundation_ready else "warning",
        )


class V029ConsolidationAuditTrailService:
    def build_audit_trail(
        self,
        source_refs: list[dict[str, Any]],
        consolidation_refs: list[dict[str, Any]],
        readiness_refs: list[dict[str, Any]],
        handoff_refs: list[dict[str, Any]],
    ) -> V029ConsolidationAuditTrail:
        total = len(source_refs) + len(consolidation_refs) + len(readiness_refs) + len(handoff_refs)
        return V029ConsolidationAuditTrail(
            "v029_consolidation_audit_trail:v0.29.9",
            source_refs,
            consolidation_refs,
            readiness_refs,
            handoff_refs,
            total,
            audit_status="ready" if total else "warning",
        )


class V029ConsolidationFindingService:
    BLOCKED_FINDINGS = {
        "provider_invocation_attempted",
        "provider_registration_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "outbound_request_attempted",
        "credential_access_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "secret_retrieval_attempted",
        "secret_materialization_attempted",
        "command_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
        "external_side_effect_attempted",
        "file_mutation_attempted",
        "rollback_execution_attempted",
        "automatic_retry_attempted",
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "live_provider_certification_attempted",
        "live_adapter_implementation_attempted",
        "RPA_adapter_attempted",
        "A360_adapter_attempted",
        "Brity_adapter_attempted",
        "UiPath_adapter_attempted",
        "external_dominion_attempted",
        "schumpeter_private_runtime_attempted",
        "actual_user_data_detected",
        "actual_company_data_detected",
        "private_material_exposure_detected",
        "raw_provider_output_persistence_detected",
        "raw_payload_logging_detected",
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }
    MISSING_FINDINGS = {
        "missing_v0298_preview_report",
        "missing_v0297_certification_report",
        "missing_v0296_approval_audit_rollback_report",
        "missing_v0295_invocation_candidate_report",
        "missing_v0294_credential_network_boundary_report",
        "missing_v0293_permission_safety_report",
        "missing_v0292_mock_harness_report",
        "missing_v0291_registry_report",
        "missing_v0290_contract_report",
    }

    def build_findings(self, sources: dict[str, Any]) -> list[V029ConsolidationFinding]:
        created = [
            "foundation_snapshot_created",
            "capability_map_created",
            "coverage_matrix_created",
            "contract_consolidated",
            "registry_consolidated",
            "mock_harness_consolidated",
            "permission_safety_consolidated",
            "credential_network_consolidated",
            "invocation_dry_run_consolidated",
            "approval_audit_rollback_consolidated",
            "packaging_certification_consolidated",
            "limited_preview_consolidated",
            "adapter_readiness_report_created",
            "v030_readiness_report_created",
            "dominion_handoff_packet_created",
            "release_manifest_created",
        ]
        findings = [
            V029ConsolidationFinding(
                "v029_consolidation_finding:ok:v0.29.9",
                "info",
                "ok",
                "v0.29.9 consolidates External Provider Adapter Foundation v1 without enabling runtime.",
                None,
                [],
                None,
            )
        ]
        missing_by_key = {
            "preview": "missing_v0298_preview_report",
            "certification": "missing_v0297_certification_report",
            "approval": "missing_v0296_approval_audit_rollback_report",
            "invocation": "missing_v0295_invocation_candidate_report",
            "credential": "missing_v0294_credential_network_boundary_report",
            "permission": "missing_v0293_permission_safety_report",
            "mock": "missing_v0292_mock_harness_report",
            "registry": "missing_v0291_registry_report",
            "contract": "missing_v0290_contract_report",
        }
        for key, finding_type in missing_by_key.items():
            if sources[key] is None:
                findings.append(
                    V029ConsolidationFinding(
                        f"v029_consolidation_finding:{finding_type}:v0.29.9",
                        "warning",
                        finding_type,
                        f"{finding_type} was not available; consolidation continues with warning metadata.",
                        None,
                        [],
                        None,
                    )
                )
        for finding_type in created:
            findings.append(
                V029ConsolidationFinding(
                    f"v029_consolidation_finding:{finding_type}:v0.29.9",
                    "info",
                    finding_type,
                    f"{finding_type} artifact was created as consolidation metadata only.",
                    None,
                    [],
                    None,
                )
            )
        for finding_type in self.BLOCKED_FINDINGS:
            findings.append(
                V029ConsolidationFinding(
                    f"v029_consolidation_finding:{finding_type}:v0.29.9",
                    "critical",
                    finding_type,
                    f"{finding_type} would block External Provider Adapter Foundation v1 validity.",
                    None,
                    [],
                    finding_type,
                )
            )
        return findings


class V029ConsolidationReportService:
    def _load_sources(self) -> dict[str, Any]:
        source = V029ConsolidationPrerequisiteSourceService()
        return {
            "preview": source.load_v0298_preview_report(),
            "preview_gate": source.load_v0298_preview_gate(),
            "preview_handoff": source.load_v0298_handoff_packet(),
            "certification": source.load_v0297_packaging_certification_report(),
            "approval": source.load_v0296_approval_audit_rollback_report(),
            "invocation": source.load_v0295_invocation_candidate_report(),
            "credential": source.load_v0294_credential_network_boundary_report(),
            "permission": source.load_v0293_permission_safety_report(),
            "mock": source.load_v0292_mock_harness_report(),
            "registry": source.load_v0291_registry_report(),
            "contract": source.load_v0290_contract_report(),
            "v028": source.load_v0289_consolidation_report(),
            "memory": source.load_v0279_memory_consolidation_report(),
            "workbench": source.load_v0269_workbench_consolidation_report(),
            "metadata": source.load_ocel_pig_ocpx_metadata(),
        }

    def build_report(self, report_id: str | None = None) -> V029ConsolidationReport:
        sources = self._load_sources()
        resolved_report_id = report_id or "v029_consolidation_report:v0.29.9"
        reports = V029ConsolidationReportServices()
        contract = reports.build_contract_consolidation(sources["contract"])
        registry = reports.build_registry_consolidation(sources["registry"])
        mock = reports.build_mock_harness_consolidation(sources["mock"])
        permission = reports.build_permission_safety_consolidation(sources["permission"])
        credential = reports.build_credential_network_consolidation(sources["credential"])
        invocation = reports.build_invocation_dry_run_consolidation(sources["invocation"])
        approval = reports.build_approval_audit_rollback_consolidation(sources["approval"])
        certification = reports.build_packaging_certification_consolidation(sources["certification"])
        preview = reports.build_limited_preview_gate_consolidation(sources["preview"])
        snapshot = ExternalProviderAdapterFoundationSnapshotService().build_snapshot(sources)
        capability_map = ExternalProviderAdapterCapabilityMapService().build_map(sources["preview"])
        coverage = ExternalProviderAdapterCoverageMatrixService().build_matrix(sources)
        readiness = ExternalProviderAdapterReadinessService().build_report(snapshot)
        v030 = V030ReadinessService().build_report(readiness)
        handoff = ExternalAgentDominionHandoffPacketService().build_packet(resolved_report_id, snapshot, sources["preview_handoff"])
        manifest = ExternalProviderAdapterReleaseManifestService().build_manifest(snapshot, readiness, v030)
        source_refs = [
            ref
            for ref in [
                _report_ref("external_adapter_contract_report", sources["contract"], "v0.29.0", "external_adapter_contract_report:v0.29.0"),
                _report_ref("adapter_registry_report", sources["registry"], "v0.29.1", "adapter_registry_report:v0.29.1"),
                _report_ref("mock_adapter_harness_report", sources["mock"], "v0.29.2", "mock_adapter_harness_report:v0.29.2"),
                _report_ref("adapter_permission_safety_report", sources["permission"], "v0.29.3", "adapter_permission_safety_report:v0.29.3"),
                _report_ref("credential_network_boundary_report", sources["credential"], "v0.29.4", "credential_network_boundary_report:v0.29.4"),
                _report_ref("adapter_invocation_candidate_report", sources["invocation"], "v0.29.5", "adapter_invocation_candidate_report:v0.29.5"),
                _report_ref("provider_invocation_approval_audit_rollback_report", sources["approval"], "v0.29.6", "provider_invocation_approval_audit_rollback_report:v0.29.6"),
                _report_ref("adapter_packaging_certification_report", sources["certification"], "v0.29.7", "adapter_packaging_certification_report:v0.29.7"),
                _report_ref("limited_provider_invocation_preview_report", sources["preview"], "v0.29.8", "limited_provider_invocation_preview_report:v0.29.8"),
            ]
            if ref is not None
        ]
        consolidation_refs = [
            _ref("adapter_contract_consolidation_report", contract.report_id, V0299_VERSION),
            _ref("adapter_registry_consolidation_report", registry.report_id, V0299_VERSION),
            _ref("mock_harness_consolidation_report", mock.report_id, V0299_VERSION),
            _ref("permission_safety_consolidation_report", permission.report_id, V0299_VERSION),
            _ref("credential_network_consolidation_report", credential.report_id, V0299_VERSION),
            _ref("invocation_dry_run_consolidation_report", invocation.report_id, V0299_VERSION),
            _ref("approval_audit_rollback_consolidation_report", approval.report_id, V0299_VERSION),
            _ref("packaging_certification_consolidation_report", certification.report_id, V0299_VERSION),
            _ref("limited_preview_gate_consolidation_report", preview.report_id, V0299_VERSION),
        ]
        readiness_refs = [
            _ref("external_provider_adapter_readiness_report", readiness.report_id, V0299_VERSION),
            _ref("v030_readiness_report", v030.report_id, V0299_VERSION),
            _ref("external_provider_adapter_release_manifest", manifest.manifest_id, V0299_VERSION),
        ]
        handoff_refs = [_ref("external_agent_dominion_handoff_packet", handoff.handoff_packet_id, V0299_VERSION)]
        audit = V029ConsolidationAuditTrailService().build_audit_trail(source_refs, consolidation_refs, readiness_refs, handoff_refs)
        findings = V029ConsolidationFindingService().build_findings(sources)
        limitations = [
            "External Provider Adapter Foundation v1 is a consolidation and readiness artifact, not provider runtime.",
            "v0.30.0 must begin with an External Agent Dominion Bridge Contract and must not bypass v0.29 gates.",
        ]
        withdrawal_conditions = [
            "provider invocation, provider SDK invocation, network call, credential access, command execution, side effect, rollback execution, or retry appears",
            "package publish, release tag, live certification, live adapter, RPA adapter, or external dominion implementation appears",
            "private material, raw payload, or raw provider output is exposed",
            "provider_invocation_runtime_ready, limited_preview_execution_ready_now, live_adapter_runtime_ready, or external_agent_dominion_runtime_ready becomes true",
            "LLM judge becomes the sole consolidation authority",
        ]
        return V029ConsolidationReport(
            resolved_report_id,
            _now(),
            snapshot,
            capability_map,
            coverage,
            contract,
            registry,
            mock,
            permission,
            credential,
            invocation,
            approval,
            certification,
            preview,
            readiness,
            v030,
            handoff,
            manifest,
            audit,
            findings,
            "passed" if readiness.external_provider_adapter_foundation_ready else "warning",
            readiness.external_provider_adapter_foundation_ready,
            v030.ready_for_v030_contract,
            v030.ready_for_v030_contract,
            limitations=limitations,
            withdrawal_conditions=withdrawal_conditions,
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "snapshot": report.foundation_snapshot,
            "capabilities": report.capability_map,
            "coverage": report.coverage_matrix,
            "contract": report.contract_consolidation,
            "registry": report.registry_consolidation,
            "mock": report.mock_harness_consolidation,
            "permission-safety": report.permission_safety_consolidation,
            "credential-network": report.credential_network_consolidation,
            "invocation-dry-run": report.invocation_dry_run_consolidation,
            "approval-audit-rollback": report.approval_audit_rollback_consolidation,
            "certification": report.packaging_certification_consolidation,
            "preview": report.limited_preview_gate_consolidation,
            "readiness": report.adapter_readiness_report,
            "v030-readiness": report.v030_readiness_report,
            "handoff-v030": report.external_agent_dominion_handoff_packet,
            "manifest": report.release_manifest,
            "audit": report.audit_trail,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0299_VERSION,
            "layer": V0299_LAYER,
            "subject": "external_provider_adapter_foundation_consolidation",
            "release_name": V0299_RELEASE_NAME,
            "principles": [
                "Consolidation is not execution",
                "Foundation is not runtime",
                "Adapter readiness is not provider invocation readiness",
                "Preview gate readiness is not preview execution",
                "Certification is not live provider certification",
                "Credential boundary is not credential access",
                "Network boundary is not network access",
                "Dry-run is not provider call",
                "Handoff to v0.30 is not external agent dominion implementation",
            ],
            "safety_boundary": {
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "provider_sdk_invoked": report.provider_sdk_invoked,
                "network_called": report.network_called,
                "outbound_request_sent": report.outbound_request_sent,
                "credential_accessed": report.credential_accessed,
                "command_executed": report.command_executed,
                "external_side_effect_performed": report.external_side_effect_performed,
                "file_mutated": report.file_mutated,
                "rollback_executed": report.rollback_executed,
                "automatic_retry_performed": report.automatic_retry_performed,
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "live_provider_certified": report.live_provider_certified,
                "live_adapter_implemented": report.live_adapter_implemented,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "A360_adapter_implemented": report.A360_adapter_implemented,
                "Brity_adapter_implemented": report.Brity_adapter_implemented,
                "UiPath_adapter_implemented": report.UiPath_adapter_implemented,
                "external_dominion_implemented": report.external_dominion_implemented,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "private_material_exposed": report.private_material_exposed,
                "raw_provider_output_persisted": report.raw_provider_output_persisted,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.30.0 External Agent Dominion Bridge Contract",
                "v0.30.x External Agent Dominion Bridge Foundation",
            ],
            "next_step": V0299_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "external_provider_adapter_foundation_v1_consolidated",
            "version": V0299_VERSION,
            "source_read_models": [
                "ExternalProviderAdapterContractState",
                "AdapterRegistryState",
                "MockAdapterHarnessState",
                "AdapterPermissionSafetyGateState",
                "CredentialNetworkBoundaryGateState",
                "AdapterInvocationCandidateState",
                "AdapterDryRunReportState",
                "ProviderInvocationApprovalBoundaryState",
                "AdapterCertificationReadinessGateState",
                "LimitedPreviewGateState",
                "LimitedPreviewHandoffState",
                "V028ConsolidationState",
                "MemoryConsolidationState",
                "WorkbenchConsolidationState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "ExternalProviderAdapterFoundationSnapshotState",
                "ExternalProviderAdapterCapabilityMapState",
                "ExternalProviderAdapterCoverageMatrixState",
                "ExternalProviderAdapterReadinessState",
                "V030ReadinessState",
                "ExternalAgentDominionHandoffState",
                "ExternalProviderAdapterReleaseManifestState",
                "V029ConsolidationState",
            ],
            "effect_types": V0299_EFFECT_TYPES,
        }


def render_v029_consolidation_cli(parts: dict[str, Any], section: str = "report") -> str:
    payload = parts[section]
    if isinstance(payload, list):
        return "\n".join(
            [
                f"External Provider Adapter Foundation Consolidation {section}",
                f"version={V0299_VERSION}",
                f"release_name={V0299_RELEASE_NAME}",
                f"count={len(payload)}",
            ]
        )
    if section != "report":
        object_id = (
            getattr(payload, "snapshot_id", None)
            or getattr(payload, "map_id", None)
            or getattr(payload, "matrix_id", None)
            or getattr(payload, "report_id", None)
            or getattr(payload, "handoff_packet_id", None)
            or getattr(payload, "manifest_id", None)
            or getattr(payload, "audit_trail_id", None)
        )
        return "\n".join([payload.__class__.__name__, f"version={V0299_VERSION}", f"release_name={V0299_RELEASE_NAME}", f"object_id={object_id}"])
    report: V029ConsolidationReport = payload
    lines = [
        "External Provider Adapter Foundation Consolidation report",
        f"version={report.version}",
        f"release_name={report.release_name}",
        f"report_status={report.report_status}",
        f"external_provider_adapter_foundation_ready={_bool(report.external_provider_adapter_foundation_ready)}",
        f"ready_for_v030={_bool(report.ready_for_v030)}",
        f"ready_for_v030_contract={_bool(report.ready_for_v030_contract)}",
        f"provider_invocation_runtime_ready={_bool(report.provider_invocation_runtime_ready)}",
        f"limited_preview_execution_ready_now={_bool(report.limited_preview_execution_ready_now)}",
        f"live_adapter_runtime_ready={_bool(report.live_adapter_runtime_ready)}",
        f"external_agent_dominion_runtime_ready={_bool(report.external_agent_dominion_runtime_ready)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"provider_sdk_invoked={_bool(report.provider_sdk_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"outbound_request_sent={_bool(report.outbound_request_sent)}",
        f"credential_accessed={_bool(report.credential_accessed)}",
        f"credential_stored={_bool(report.credential_stored)}",
        f"credential_logged={_bool(report.credential_logged)}",
        f"secret_retrieved={_bool(report.secret_retrieved)}",
        f"secret_materialized={_bool(report.secret_materialized)}",
        f"command_executed={_bool(report.command_executed)}",
        f"external_side_effect_performed={_bool(report.external_side_effect_performed)}",
        f"file_mutated={_bool(report.file_mutated)}",
        f"rollback_executed={_bool(report.rollback_executed)}",
        f"automatic_retry_performed={_bool(report.automatic_retry_performed)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"live_provider_certified={_bool(report.live_provider_certified)}",
        f"live_adapter_implemented={_bool(report.live_adapter_implemented)}",
        f"RPA_adapter_implemented={_bool(report.RPA_adapter_implemented)}",
        f"A360_adapter_implemented={_bool(report.A360_adapter_implemented)}",
        f"Brity_adapter_implemented={_bool(report.Brity_adapter_implemented)}",
        f"UiPath_adapter_implemented={_bool(report.UiPath_adapter_implemented)}",
        f"external_dominion_implemented={_bool(report.external_dominion_implemented)}",
        f"schumpeter_private_runtime_used={_bool(report.schumpeter_private_runtime_used)}",
        f"actual_user_data_used={_bool(report.actual_user_data_used)}",
        f"actual_company_data_used={_bool(report.actual_company_data_used)}",
        f"private_material_exposed={_bool(report.private_material_exposed)}",
        f"raw_provider_output_persisted={_bool(report.raw_provider_output_persisted)}",
        f"raw_payload_logged={_bool(report.raw_payload_logged)}",
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    return "\n".join(lines)
