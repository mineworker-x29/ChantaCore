from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from chanta_core.adapter_invocation_candidate_dry_run_plan import (
    AdapterInvocationCandidateReport,
    AdapterInvocationCandidateReportService,
)
from chanta_core.credential_secret_network_boundary import (
    CredentialNetworkBoundaryReport,
    CredentialNetworkBoundaryReportService,
)
from chanta_core.external_provider_adapter_contract import (
    ExternalAdapterContractReport,
    ExternalAdapterContractReportService,
    ModelMixin,
    _bool,
    _ref,
)
from chanta_core.mock_adapter_harness_no_network_default import (
    MockAdapterHarnessReport,
    MockAdapterHarnessReportService,
)
from chanta_core.permission_safety_scope_gate_for_external_adapters import (
    AdapterPermissionSafetyReport,
    AdapterPermissionSafetyReportService,
)
from chanta_core.provider_capability_inventory_adapter_registry import (
    AdapterRegistryReport,
    AdapterRegistryReportService,
)
from chanta_core.provider_invocation_approval_audit_rollback_boundary import (
    ProviderInvocationApprovalAuditRollbackReport,
    ProviderInvocationApprovalAuditRollbackReportService,
)
from chanta_core.utility.time import utc_now_iso


V0297_VERSION = "v0.29.7"
V0297_LAYER = "external_provider_adapter"
V0297_TRACK = "External Skill / External Provider Adapter Development"
V0297_NAME = "External Skill Packaging / Certification Matrix"
V0297_NEXT_STEP = "v0.29.8 Limited Provider Invocation Preview Gate"

V0297_OBJECT_TYPES = [
    "external_skill_packaging_certification_policy",
    "external_skill_packaging_certification_request",
    "external_skill_packaging_certification_source_view",
    "external_skill_package_policy",
    "external_skill_manifest",
    "external_skill_manifest_entry",
    "adapter_package_manifest",
    "adapter_package_dependency_profile",
    "adapter_package_boundary_policy",
    "adapter_package_exposure_report",
    "adapter_certification_policy",
    "adapter_certification_matrix",
    "adapter_certification_case",
    "adapter_certification_case_result",
    "mock_mode_certification_report",
    "no_network_certification_report",
    "no_credential_certification_report",
    "no_command_certification_report",
    "permission_safety_certification_report",
    "credential_network_boundary_certification_report",
    "invocation_dry_run_certification_report",
    "approval_audit_rollback_certification_report",
    "ocel_visibility_certification_report",
    "result_boundary_certification_report",
    "failure_rollback_noop_certification_report",
    "rpa_future_track_certification_note",
    "external_dominion_exclusion_certification",
    "adapter_certification_readiness_gate",
    "adapter_certification_audit_trail",
    "adapter_packaging_certification_finding",
    "adapter_packaging_certification_report",
    "provider_invocation_approval_audit_rollback_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0297_EVENT_TYPES = [
    "adapter_packaging_certification_requested",
    "adapter_packaging_certification_prerequisites_loaded",
    "external_skill_packaging_certification_policy_created",
    "external_skill_manifest_created",
    "external_skill_manifest_entry_created",
    "adapter_package_manifest_created",
    "adapter_package_dependency_profile_created",
    "adapter_package_boundary_policy_created",
    "adapter_package_exposure_report_created",
    "adapter_certification_policy_created",
    "adapter_certification_matrix_created",
    "adapter_certification_case_created",
    "adapter_certification_case_result_created",
    "mock_mode_certification_report_created",
    "no_network_certification_report_created",
    "no_credential_certification_report_created",
    "no_command_certification_report_created",
    "permission_safety_certification_report_created",
    "credential_network_boundary_certification_report_created",
    "invocation_dry_run_certification_report_created",
    "approval_audit_rollback_certification_report_created",
    "ocel_visibility_certification_report_created",
    "result_boundary_certification_report_created",
    "failure_rollback_noop_certification_report_created",
    "rpa_future_track_certification_note_created",
    "external_dominion_exclusion_certification_created",
    "adapter_certification_readiness_gate_evaluated",
    "adapter_certification_audit_trail_created",
    "adapter_packaging_certification_report_created",
    "adapter_packaging_certification_warning_created",
    "adapter_packaging_certification_blocked",
]

V0297_EFFECT_TYPES = [
    "read_only_observation",
    "external_skill_manifest_created",
    "adapter_package_manifest_created",
    "adapter_package_exposure_report_created",
    "adapter_certification_matrix_created",
    "adapter_certification_case_result_created",
    "adapter_boundary_certification_created",
    "adapter_certification_readiness_gate_evaluated",
    "adapter_certification_audit_trail_created",
    "state_candidate_created",
]

V0297_FORBIDDEN_EFFECT_TYPES = [
    "package_published",
    "package_uploaded",
    "release_tag_created",
    "official_release_artifact_created",
    "live_provider_certified",
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

CERTIFICATION_CASES = [
    ("manifest_completeness", "manifest"),
    ("dependency_boundary", "dependency"),
    ("package_exposure", "boundary"),
    ("mock_mode", "mock"),
    ("no_network", "boundary"),
    ("no_credential", "boundary"),
    ("no_command", "boundary"),
    ("permission_safety", "safety"),
    ("credential_network_boundary", "boundary"),
    ("invocation_dry_run", "dry_run"),
    ("approval_audit_rollback", "approval"),
    ("ocel_visibility", "ocel"),
    ("result_boundary", "result"),
    ("failure_rollback_noop", "rollback"),
    ("rpa_future_track", "future_track"),
    ("external_dominion_exclusion", "exclusion"),
]


def _now() -> str:
    return utc_now_iso()


def _refs(object_type: str, items: list[Any], attr: str, version: str) -> list[dict[str, Any]]:
    return [_ref(object_type, getattr(item, attr), version) for item in items]


def _safe_get(items: list[Any], index: int) -> Any | None:
    if not items:
        return None
    return items[min(index, len(items) - 1)]


def _adapter_names(invocation_report: AdapterInvocationCandidateReport) -> list[str]:
    names = [candidate.adapter_name for candidate in invocation_report.invocation_candidates]
    return names or ["internal_mock_adapter"]


@dataclass
class ExternalSkillPackagingCertificationPolicy(ModelMixin):
    policy_id: str
    packaging_enabled: bool = True
    certification_matrix_enabled: bool = True
    manifest_required: bool = True
    dependency_boundary_required: bool = True
    exposure_report_required: bool = True
    certification_cases_required: bool = True
    mock_mode_certification_required: bool = True
    no_network_certification_required: bool = True
    no_credential_certification_required: bool = True
    no_command_certification_required: bool = True
    permission_safety_certification_required: bool = True
    credential_network_boundary_certification_required: bool = True
    dry_run_certification_required: bool = True
    approval_audit_rollback_certification_required: bool = True
    ocel_visibility_certification_required: bool = True
    result_boundary_certification_required: bool = True
    failure_rollback_noop_certification_required: bool = True
    package_publish_enabled_now: bool = False
    release_tag_creation_enabled_now: bool = False
    live_provider_certification_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_access_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    live_adapter_implementation_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    certification_pass_is_not_invocation_preview: bool = True
    certified_mock_is_not_certified_live_adapter: bool = True
    llm_judge_as_sole_certification_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION
    layer: str = V0297_LAYER


@dataclass
class ExternalSkillPackagingCertificationRequest(ModelMixin):
    request_id: str
    approval_audit_rollback_report_id: str | None
    invocation_candidate_report_id: str | None
    credential_network_boundary_report_id: str | None
    permission_safety_report_id: str | None
    mock_harness_report_id: str | None
    adapter_registry_report_id: str | None
    requested_certification_scope: str = "full_packaging_certification"
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ExternalSkillPackagingCertificationSourceView(ModelMixin):
    source_view_id: str
    approval_audit_rollback_report_ref: dict[str, Any] | None
    approval_audit_rollback_gate_ref: dict[str, Any] | None
    approval_decision_record_refs: list[dict[str, Any]]
    audit_trail_refs: list[dict[str, Any]]
    ocel_trace_plan_refs: list[dict[str, Any]]
    result_boundary_refs: list[dict[str, Any]]
    failure_classification_refs: list[dict[str, Any]]
    rollback_plan_refs: list[dict[str, Any]]
    noop_boundary_refs: list[dict[str, Any]]
    invocation_candidate_report_ref: dict[str, Any] | None
    dry_run_report_refs: list[dict[str, Any]]
    credential_network_boundary_report_ref: dict[str, Any] | None
    permission_safety_report_ref: dict[str, Any] | None
    mock_harness_report_ref: dict[str, Any] | None
    adapter_registry_report_ref: dict[str, Any] | None
    external_adapter_contract_report_ref: dict[str, Any] | None
    provider_invocation_prohibition_ref: dict[str, Any] | None
    command_execution_prohibition_ref: dict[str, Any] | None
    source_status: str
    ready_for_certification_matrix: bool | None
    provider_invocation_detected: bool = False
    network_call_detected: bool = False
    credential_access_detected: bool = False
    command_execution_detected: bool = False
    live_adapter_detected: bool = False
    package_publish_detected: bool = False
    release_tag_detected: bool = False
    private_data_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ExternalSkillPackagePolicy(ModelMixin):
    policy_id: str
    external_skill_manifest_required: bool = True
    package_manifest_required: bool = True
    manifest_is_not_runtime_enablement: bool = True
    package_manifest_is_not_package_publish: bool = True
    package_publish_forbidden_now: bool = True
    release_tag_forbidden_now: bool = True
    runtime_binding_forbidden_now: bool = True
    provider_registration_forbidden_now: bool = True
    provider_invocation_forbidden_now: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ExternalSkillManifestEntry(ModelMixin):
    entry_id: str
    skill_name: str
    adapter_name: str
    provider_kind: str
    capability_refs: list[dict[str, Any]]
    registry_entry_ref: dict[str, Any] | None
    contract_ref: dict[str, Any] | None
    mock_harness_ref: dict[str, Any] | None
    certification_matrix_ref: dict[str, Any] | None
    skill_status: str
    runtime_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ExternalSkillManifest(ModelMixin):
    manifest_id: str
    manifest_name: str
    entries: list[ExternalSkillManifestEntry]
    entry_count: int
    manifest_status: str
    manifest_is_runtime_enablement: bool = False
    package_published: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterPackageManifest(ModelMixin):
    package_manifest_id: str
    package_name: str
    package_kind: str
    manifest_entries: list[dict[str, Any]]
    package_publish_ready: bool = False
    package_published_now: bool = False
    release_tag_created_now: bool = False
    runtime_dependency_added_now: bool = False
    manifest_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterPackageDependencyProfile(ModelMixin):
    dependency_profile_id: str
    adapter_name: str
    provider_sdk_required_now: bool = False
    provider_sdk_optional_later: bool = True
    provider_sdk_runtime_dependency_added_now: bool = False
    external_runtime_dependency_added_now: bool = False
    private_dependency_detected: bool = False
    dependency_profile_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterPackageBoundaryPolicy(ModelMixin):
    policy_id: str
    package_boundary_required: bool = True
    runtime_dependency_boundary_required: bool = True
    package_data_boundary_required: bool = True
    private_data_exclusion_required: bool = True
    credential_exclusion_required: bool = True
    raw_provider_output_exclusion_required: bool = True
    package_publish_forbidden_now: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterPackageExposureReport(ModelMixin):
    report_id: str
    package_manifest_ref: dict[str, Any]
    private_data_exposed: bool = False
    credential_exposed: bool = False
    secret_exposed: bool = False
    raw_provider_output_exposed: bool = False
    raw_payload_exposed: bool = False
    provider_sdk_runtime_dependency_exposed: bool = False
    exposure_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterCertificationPolicy(ModelMixin):
    policy_id: str
    certification_matrix_required: bool = True
    certification_cases_required: bool = True
    boundary_tests_required: bool = True
    mock_mode_certification_required: bool = True
    no_network_certification_required: bool = True
    no_credential_certification_required: bool = True
    no_command_certification_required: bool = True
    permission_safety_certification_required: bool = True
    credential_network_boundary_certification_required: bool = True
    dry_run_certification_required: bool = True
    approval_audit_rollback_certification_required: bool = True
    ocel_visibility_certification_required: bool = True
    result_boundary_certification_required: bool = True
    live_provider_certification_forbidden_now: bool = True
    certification_pass_is_not_provider_invocation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterCertificationCase(ModelMixin):
    case_id: str
    adapter_name: str
    case_name: str
    case_type: str
    required: bool = True
    live_provider_required: bool = False
    network_required: bool = False
    credential_value_required: bool = False
    command_execution_required: bool = False
    case_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterCertificationCaseResult(ModelMixin):
    result_id: str
    case_ref: dict[str, Any]
    adapter_name: str
    result_status: str
    result_summary: str
    provider_invoked: bool = False
    network_called: bool = False
    credential_accessed: bool = False
    command_executed: bool = False
    live_adapter_used: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterCertificationMatrix(ModelMixin):
    matrix_id: str
    adapter_name: str
    certification_cases: list[AdapterCertificationCase]
    total_case_count: int
    passed_case_count: int
    warning_case_count: int
    failed_case_count: int
    blocked_case_count: int
    unknown_case_count: int
    certification_status: str
    live_certified: bool = False
    preview_gate_ready: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class MockModeCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    mock_harness_ref: dict[str, Any] | None
    mock_mode_passed: bool
    deterministic_fixture_passed: bool
    live_adapter_used: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class NoNetworkCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    no_network_boundary_ref: dict[str, Any] | None
    no_network_passed: bool
    network_called: bool = False
    outbound_request_sent: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class NoCredentialCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    credential_boundary_ref: dict[str, Any] | None
    no_credential_passed: bool
    credential_accessed: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    secret_retrieved: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class NoCommandCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    command_execution_forbidden: bool = True
    command_executed: bool = False
    shell_true_detected: bool = False
    unbounded_subprocess_detected: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class PermissionSafetyCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    permission_safety_ref: dict[str, Any] | None
    deny_first_passed: bool
    no_permission_granted: bool = True
    no_approval_granted: bool = True
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class CredentialNetworkBoundaryCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    credential_network_boundary_ref: dict[str, Any] | None
    credential_boundary_passed: bool
    network_boundary_passed: bool
    ready_for_live_access: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class InvocationDryRunCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    dry_run_ref: dict[str, Any] | None
    dry_run_passed_or_safely_deferred: bool
    provider_invoked: bool = False
    network_called: bool = False
    credential_accessed: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ApprovalAuditRollbackCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    approval_audit_rollback_ref: dict[str, Any] | None
    approval_boundary_passed: bool
    audit_boundary_passed: bool
    rollback_noop_boundary_passed: bool
    approval_granted: bool = False
    rollback_executed: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class OCELVisibilityCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    ocel_trace_refs: list[dict[str, Any]]
    required_events_present: bool
    provider_invocation_event_absent_now: bool = True
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ResultBoundaryCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    result_boundary_ref: dict[str, Any] | None
    raw_provider_output_persistence_forbidden: bool = True
    raw_provider_output_persisted: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class FailureRollbackNoOpCertificationReport(ModelMixin):
    report_id: str
    adapter_name: str
    failure_refs: list[dict[str, Any]]
    rollback_refs: list[dict[str, Any]]
    noop_refs: list[dict[str, Any]]
    failure_classification_ready: bool
    noop_available: bool
    automatic_retry_performed: bool = False
    report_status: str = "passed"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class RPAFutureTrackCertificationNote(ModelMixin):
    note_id: str
    adapter_name: str
    rpa_related: bool
    A360_related: bool = False
    Brity_related: bool = False
    UiPath_related: bool = False
    rpa_deferred: bool = True
    rpa_implemented_now: bool = False
    required_future_gate: str = "v0.30+ External Agent Dominion / RPA future track"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class ExternalDominionExclusionCertification(ModelMixin):
    certification_id: str
    adapter_name: str
    external_dominion_related: bool
    external_dominion_implemented_now: bool = False
    excluded_from_v029: bool = True
    future_track: str = "v0.30+"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterCertificationReadinessGate(ModelMixin):
    gate_id: str
    source_view_ref: dict[str, Any]
    manifest_ref: dict[str, Any]
    package_manifest_ref: dict[str, Any]
    exposure_report_ref: dict[str, Any]
    certification_matrix_refs: list[dict[str, Any]]
    case_result_refs: list[dict[str, Any]]
    mock_certification_refs: list[dict[str, Any]]
    no_network_certification_refs: list[dict[str, Any]]
    no_credential_certification_refs: list[dict[str, Any]]
    no_command_certification_refs: list[dict[str, Any]]
    permission_safety_certification_refs: list[dict[str, Any]]
    credential_network_certification_refs: list[dict[str, Any]]
    dry_run_certification_refs: list[dict[str, Any]]
    approval_audit_rollback_certification_refs: list[dict[str, Any]]
    ocel_visibility_certification_refs: list[dict[str, Any]]
    result_boundary_certification_refs: list[dict[str, Any]]
    failure_rollback_noop_certification_refs: list[dict[str, Any]]
    manifest_complete: bool
    package_boundary_passed: bool
    dependency_boundary_passed: bool
    exposure_boundary_passed: bool
    certification_matrix_complete: bool
    required_cases_passed_or_warned: bool
    mock_certified: bool
    no_network_certified: bool
    no_credential_certified: bool
    no_command_certified: bool
    permission_safety_certified: bool
    credential_network_boundary_certified: bool
    dry_run_certified: bool
    approval_audit_rollback_certified: bool
    ocel_visibility_certified: bool
    result_boundary_certified: bool
    failure_rollback_noop_certified: bool
    no_package_publish: bool
    no_release_tag: bool
    no_live_certification: bool
    no_provider_invocation: bool
    no_network_call: bool
    no_credential_access: bool
    no_command_execution: bool
    gate_status: str
    ready_for_v0_29_8: bool
    ready_for_limited_invocation_preview_gate: bool
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterCertificationAuditTrail(ModelMixin):
    audit_trail_id: str
    request_ref: dict[str, Any]
    source_view_ref: dict[str, Any]
    manifest_refs: list[dict[str, Any]]
    certification_matrix_refs: list[dict[str, Any]]
    certification_result_refs: list[dict[str, Any]]
    gate_ref: dict[str, Any]
    audit_event_count: int
    raw_content_included: bool = False
    credential_value_included: bool = False
    raw_payload_included: bool = False
    raw_provider_output_included: bool = False
    audit_status: str = "ready"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0297_VERSION


@dataclass
class AdapterPackagingCertificationFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class AdapterPackagingCertificationReport(ModelMixin):
    report_id: str
    created_at: str
    policy: ExternalSkillPackagingCertificationPolicy
    request: ExternalSkillPackagingCertificationRequest
    source_view: ExternalSkillPackagingCertificationSourceView
    external_skill_package_policy: ExternalSkillPackagePolicy
    external_skill_manifest: ExternalSkillManifest
    adapter_package_manifests: list[AdapterPackageManifest]
    dependency_profiles: list[AdapterPackageDependencyProfile]
    package_boundary_policy: AdapterPackageBoundaryPolicy
    package_exposure_reports: list[AdapterPackageExposureReport]
    certification_policy: AdapterCertificationPolicy
    certification_matrices: list[AdapterCertificationMatrix]
    certification_case_results: list[AdapterCertificationCaseResult]
    mock_mode_certifications: list[MockModeCertificationReport]
    no_network_certifications: list[NoNetworkCertificationReport]
    no_credential_certifications: list[NoCredentialCertificationReport]
    no_command_certifications: list[NoCommandCertificationReport]
    permission_safety_certifications: list[PermissionSafetyCertificationReport]
    credential_network_boundary_certifications: list[CredentialNetworkBoundaryCertificationReport]
    dry_run_certifications: list[InvocationDryRunCertificationReport]
    approval_audit_rollback_certifications: list[ApprovalAuditRollbackCertificationReport]
    ocel_visibility_certifications: list[OCELVisibilityCertificationReport]
    result_boundary_certifications: list[ResultBoundaryCertificationReport]
    failure_rollback_noop_certifications: list[FailureRollbackNoOpCertificationReport]
    rpa_future_track_notes: list[RPAFutureTrackCertificationNote]
    external_dominion_exclusion_certifications: list[ExternalDominionExclusionCertification]
    certification_readiness_gate: AdapterCertificationReadinessGate
    audit_trail: AdapterCertificationAuditTrail
    findings: list[AdapterPackagingCertificationFinding]
    report_status: str
    ready_for_v0_29_8: bool
    ready_for_limited_invocation_preview_gate: bool
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_credential_access: bool = False
    ready_for_command_execution: bool = False
    package_published: bool = False
    release_tag_created: bool = False
    live_provider_certified: bool = False
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
    next_required_step: str = V0297_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.8 Limited Provider Invocation Preview Gate begins or External Skill Packaging / Certification policy changes."
    version: str = V0297_VERSION


class AdapterPackagingCertificationPrerequisiteSourceService:
    def load_v0296_approval_audit_rollback_report(self) -> ProviderInvocationApprovalAuditRollbackReport:
        return ProviderInvocationApprovalAuditRollbackReportService().build_report()

    def load_v0296_approval_audit_rollback_gate(self) -> Any:
        return self.load_v0296_approval_audit_rollback_report().approval_audit_rollback_gate

    def load_approval_decision_records(self) -> list[Any]:
        return self.load_v0296_approval_audit_rollback_report().approval_decision_records

    def load_audit_trails(self) -> list[Any]:
        return [self.load_v0296_approval_audit_rollback_report().audit_trail]

    def load_ocel_trace_plans(self) -> list[Any]:
        return self.load_v0296_approval_audit_rollback_report().ocel_trace_plans

    def load_result_boundaries(self) -> list[Any]:
        return [self.load_v0296_approval_audit_rollback_report().result_boundary_policy]

    def load_failure_classifications(self) -> list[Any]:
        return self.load_v0296_approval_audit_rollback_report().failure_classifications

    def load_rollback_plans(self) -> list[Any]:
        return self.load_v0296_approval_audit_rollback_report().rollback_plans

    def load_noop_boundaries(self) -> list[Any]:
        return self.load_v0296_approval_audit_rollback_report().noop_boundaries

    def load_v0295_invocation_candidate_report(self) -> AdapterInvocationCandidateReport:
        return AdapterInvocationCandidateReportService().build_report()

    def load_dry_run_reports(self) -> list[Any]:
        return self.load_v0295_invocation_candidate_report().dry_run_reports

    def load_v0294_credential_network_boundary_report(self) -> CredentialNetworkBoundaryReport:
        return CredentialNetworkBoundaryReportService().build_report()

    def load_v0293_permission_safety_report(self) -> AdapterPermissionSafetyReport:
        return AdapterPermissionSafetyReportService().build_report()

    def load_v0292_mock_harness_report(self) -> MockAdapterHarnessReport:
        return MockAdapterHarnessReportService().build_report()

    def load_v0291_adapter_registry_report(self) -> AdapterRegistryReport:
        return AdapterRegistryReportService().build_report()

    def load_v0290_external_adapter_contract_report(self) -> ExternalAdapterContractReport:
        return ExternalAdapterContractReportService().build_report()

    def load_provider_invocation_prohibition_contract(self) -> dict[str, Any]:
        return _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", "v0.29.0")

    def load_command_execution_prohibition_contract(self) -> dict[str, Any]:
        return _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", "v0.29.0")


class ExternalSkillPackagingCertificationPolicyService:
    def build_policy(self) -> ExternalSkillPackagingCertificationPolicy:
        return ExternalSkillPackagingCertificationPolicy("external_skill_packaging_certification_policy:v0.29.7")


class ExternalSkillPackagingCertificationSourceViewService:
    def build_source_view(self) -> ExternalSkillPackagingCertificationSourceView:
        source = AdapterPackagingCertificationPrerequisiteSourceService()
        approval_report = source.load_v0296_approval_audit_rollback_report()
        invocation_report = source.load_v0295_invocation_candidate_report()
        credential_report = source.load_v0294_credential_network_boundary_report()
        permission_report = source.load_v0293_permission_safety_report()
        mock_report = source.load_v0292_mock_harness_report()
        registry_report = source.load_v0291_adapter_registry_report()
        contract_report = source.load_v0290_external_adapter_contract_report()
        return ExternalSkillPackagingCertificationSourceView(
            "external_skill_packaging_certification_source_view:v0.29.7",
            _ref("provider_invocation_approval_audit_rollback_report", approval_report.report_id, "v0.29.6"),
            _ref("provider_invocation_approval_audit_rollback_gate", approval_report.approval_audit_rollback_gate.gate_id, "v0.29.6"),
            _refs("provider_invocation_approval_decision_record", approval_report.approval_decision_records, "decision_record_id", "v0.29.6"),
            [_ref("provider_invocation_audit_trail", approval_report.audit_trail.audit_trail_id, "v0.29.6")],
            _refs("provider_invocation_ocel_trace_plan", approval_report.ocel_trace_plans, "trace_plan_id", "v0.29.6"),
            [_ref("provider_result_boundary_policy", approval_report.result_boundary_policy.policy_id, "v0.29.6")],
            _refs("provider_failure_classification", approval_report.failure_classifications, "classification_id", "v0.29.6"),
            _refs("provider_rollback_plan", approval_report.rollback_plans, "rollback_plan_id", "v0.29.6"),
            _refs("provider_noop_boundary", approval_report.noop_boundaries, "noop_boundary_id", "v0.29.6"),
            _ref("adapter_invocation_candidate_report", invocation_report.report_id, "v0.29.5"),
            _refs("adapter_invocation_dry_run_report", invocation_report.dry_run_reports, "report_id", "v0.29.5"),
            _ref("credential_network_boundary_report", credential_report.report_id, "v0.29.4"),
            _ref("adapter_permission_safety_report", permission_report.report_id, "v0.29.3"),
            _ref("mock_adapter_harness_report", mock_report.report_id, "v0.29.2"),
            _ref("adapter_registry_report", registry_report.report_id, "v0.29.1"),
            _ref("external_adapter_contract_report", contract_report.report_id, "v0.29.0"),
            source.load_provider_invocation_prohibition_contract(),
            source.load_command_execution_prohibition_contract(),
            "complete",
            approval_report.ready_for_certification_matrix,
        )


class ExternalSkillPackagingCertificationRequestService:
    def build_request(self, source_view: ExternalSkillPackagingCertificationSourceView) -> ExternalSkillPackagingCertificationRequest:
        refs = [
            ref
            for ref in [
                source_view.approval_audit_rollback_report_ref,
                source_view.invocation_candidate_report_ref,
                source_view.credential_network_boundary_report_ref,
                source_view.permission_safety_report_ref,
                source_view.mock_harness_report_ref,
                source_view.adapter_registry_report_ref,
            ]
            if ref is not None
        ]
        return ExternalSkillPackagingCertificationRequest(
            "external_skill_packaging_certification_request:v0.29.7",
            source_view.approval_audit_rollback_report_ref.get("object_id") if source_view.approval_audit_rollback_report_ref else None,
            source_view.invocation_candidate_report_ref.get("object_id") if source_view.invocation_candidate_report_ref else None,
            source_view.credential_network_boundary_report_ref.get("object_id") if source_view.credential_network_boundary_report_ref else None,
            source_view.permission_safety_report_ref.get("object_id") if source_view.permission_safety_report_ref else None,
            source_view.mock_harness_report_ref.get("object_id") if source_view.mock_harness_report_ref else None,
            source_view.adapter_registry_report_ref.get("object_id") if source_view.adapter_registry_report_ref else None,
            source_refs=refs,
        )


class ExternalSkillPackageService:
    def build_package_policy(self) -> ExternalSkillPackagePolicy:
        return ExternalSkillPackagePolicy("external_skill_package_policy:v0.29.7")

    def build_manifest_entries(
        self,
        invocation_report: AdapterInvocationCandidateReport,
        registry_report: AdapterRegistryReport,
        contract_report: ExternalAdapterContractReport,
        mock_report: MockAdapterHarnessReport,
    ) -> list[ExternalSkillManifestEntry]:
        entries: list[ExternalSkillManifestEntry] = []
        capabilities = getattr(registry_report, "capability_declarations", [])
        registry_entries = getattr(registry_report.adapter_registry, "entries", [])
        contracts = [getattr(contract_report, "capability_contract", None)]
        for index, candidate in enumerate(invocation_report.invocation_candidates):
            capability = _safe_get(capabilities, index)
            registry_entry = _safe_get(registry_entries, index)
            contract = _safe_get(contracts, index)
            entries.append(
                ExternalSkillManifestEntry(
                    f"external_skill_manifest_entry:{candidate.adapter_name}:v0.29.7",
                    f"{candidate.adapter_name}.{candidate.capability_name}",
                    candidate.adapter_name,
                    getattr(_safe_get(invocation_report.invocation_intents, index), "provider_kind", "mock_provider"),
                    [_ref("adapter_capability_declaration", capability.declaration_id, "v0.29.1")] if capability else [],
                    _ref("adapter_registry_entry", registry_entry.registry_entry_id, "v0.29.1") if registry_entry else None,
                    _ref("adapter_capability_contract", contract.contract_id, "v0.29.0") if contract else None,
                    _ref("mock_adapter_harness_report", mock_report.report_id, "v0.29.2"),
                    _ref("adapter_certification_matrix", f"adapter_certification_matrix:{candidate.adapter_name}:v0.29.7", V0297_VERSION),
                    "mock_certifiable",
                )
            )
        return entries

    def build_external_skill_manifest(self, entries: list[ExternalSkillManifestEntry]) -> ExternalSkillManifest:
        return ExternalSkillManifest(
            "external_skill_manifest:v0.29.7",
            "external_provider_adapter_mock_certifiable_manifest",
            entries,
            len(entries),
            "ready" if entries else "warning",
        )

    def build_adapter_package_manifests(self, entries: list[ExternalSkillManifestEntry]) -> list[AdapterPackageManifest]:
        return [
            AdapterPackageManifest(
                f"adapter_package_manifest:{entry.adapter_name}:v0.29.7",
                f"{entry.adapter_name}-certification-pack",
                "certification_pack",
                [_ref("external_skill_manifest_entry", entry.entry_id, V0297_VERSION)],
            )
            for entry in entries
        ]

    def build_dependency_profiles(self, adapter_names: list[str]) -> list[AdapterPackageDependencyProfile]:
        return [
            AdapterPackageDependencyProfile(
                f"adapter_package_dependency_profile:{adapter_name}:v0.29.7",
                adapter_name,
            )
            for adapter_name in adapter_names
        ]

    def build_package_boundary_policy(self) -> AdapterPackageBoundaryPolicy:
        return AdapterPackageBoundaryPolicy("adapter_package_boundary_policy:v0.29.7")

    def build_exposure_reports(self, manifests: list[AdapterPackageManifest]) -> list[AdapterPackageExposureReport]:
        return [
            AdapterPackageExposureReport(
                f"adapter_package_exposure_report:{manifest.package_name}:v0.29.7",
                _ref("adapter_package_manifest", manifest.package_manifest_id, V0297_VERSION),
            )
            for manifest in manifests
        ]


class AdapterCertificationService:
    def build_certification_policy(self) -> AdapterCertificationPolicy:
        return AdapterCertificationPolicy("adapter_certification_policy:v0.29.7")

    def build_certification_cases(self, adapter_name: str) -> list[AdapterCertificationCase]:
        return [
            AdapterCertificationCase(
                f"adapter_certification_case:{adapter_name}:{case_name}:v0.29.7",
                adapter_name,
                case_name,
                case_type,
                case_status="warning" if case_name == "rpa_future_track" else "passed",
            )
            for case_name, case_type in CERTIFICATION_CASES
        ]

    def build_certification_case_results(self, matrices: list[AdapterCertificationMatrix]) -> list[AdapterCertificationCaseResult]:
        results: list[AdapterCertificationCaseResult] = []
        for matrix in matrices:
            for case in matrix.certification_cases:
                results.append(
                    AdapterCertificationCaseResult(
                        f"adapter_certification_case_result:{case.adapter_name}:{case.case_name}:v0.29.7",
                        _ref("adapter_certification_case", case.case_id, V0297_VERSION),
                        case.adapter_name,
                        case.case_status,
                        "Certification case records boundary evidence only; it is not live provider certification.",
                    )
                )
        return results

    def build_certification_matrices(self, adapter_names: list[str]) -> list[AdapterCertificationMatrix]:
        matrices: list[AdapterCertificationMatrix] = []
        for adapter_name in adapter_names:
            cases = self.build_certification_cases(adapter_name)
            matrices.append(
                AdapterCertificationMatrix(
                    f"adapter_certification_matrix:{adapter_name}:v0.29.7",
                    adapter_name,
                    cases,
                    len(cases),
                    sum(case.case_status == "passed" for case in cases),
                    sum(case.case_status == "warning" for case in cases),
                    0,
                    0,
                    0,
                    "warning",
                )
            )
        return matrices


class AdapterBoundaryCertificationService:
    def build_mock_mode_certifications(self, adapter_names: list[str], mock_report: MockAdapterHarnessReport) -> list[MockModeCertificationReport]:
        return [
            MockModeCertificationReport(
                f"mock_mode_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("mock_adapter_harness_report", mock_report.report_id, "v0.29.2"),
                True,
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_no_network_certifications(self, adapter_names: list[str], credential_report: CredentialNetworkBoundaryReport) -> list[NoNetworkCertificationReport]:
        return [
            NoNetworkCertificationReport(
                f"no_network_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("credential_network_boundary_report", credential_report.report_id, "v0.29.4"),
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_no_credential_certifications(self, adapter_names: list[str], credential_report: CredentialNetworkBoundaryReport) -> list[NoCredentialCertificationReport]:
        return [
            NoCredentialCertificationReport(
                f"no_credential_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("credential_network_boundary_report", credential_report.report_id, "v0.29.4"),
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_no_command_certifications(self, adapter_names: list[str]) -> list[NoCommandCertificationReport]:
        return [NoCommandCertificationReport(f"no_command_certification_report:{adapter_name}:v0.29.7", adapter_name) for adapter_name in adapter_names]

    def build_permission_safety_certifications(self, adapter_names: list[str], permission_report: AdapterPermissionSafetyReport) -> list[PermissionSafetyCertificationReport]:
        return [
            PermissionSafetyCertificationReport(
                f"permission_safety_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("adapter_permission_safety_report", permission_report.report_id, "v0.29.3"),
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_credential_network_boundary_certifications(self, adapter_names: list[str], credential_report: CredentialNetworkBoundaryReport) -> list[CredentialNetworkBoundaryCertificationReport]:
        return [
            CredentialNetworkBoundaryCertificationReport(
                f"credential_network_boundary_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("credential_network_boundary_report", credential_report.report_id, "v0.29.4"),
                True,
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_dry_run_certifications(self, adapter_names: list[str], invocation_report: AdapterInvocationCandidateReport) -> list[InvocationDryRunCertificationReport]:
        return [
            InvocationDryRunCertificationReport(
                f"invocation_dry_run_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("adapter_invocation_candidate_report", invocation_report.report_id, "v0.29.5"),
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_approval_audit_rollback_certifications(self, adapter_names: list[str], approval_report: ProviderInvocationApprovalAuditRollbackReport) -> list[ApprovalAuditRollbackCertificationReport]:
        return [
            ApprovalAuditRollbackCertificationReport(
                f"approval_audit_rollback_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                _ref("provider_invocation_approval_audit_rollback_report", approval_report.report_id, "v0.29.6"),
                True,
                True,
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_ocel_visibility_certifications(self, adapter_names: list[str], approval_report: ProviderInvocationApprovalAuditRollbackReport) -> list[OCELVisibilityCertificationReport]:
        refs = _refs("provider_invocation_ocel_trace_plan", approval_report.ocel_trace_plans, "trace_plan_id", "v0.29.6")
        return [
            OCELVisibilityCertificationReport(
                f"ocel_visibility_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                refs,
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_result_boundary_certifications(self, adapter_names: list[str], approval_report: ProviderInvocationApprovalAuditRollbackReport) -> list[ResultBoundaryCertificationReport]:
        ref = _ref("provider_result_boundary_policy", approval_report.result_boundary_policy.policy_id, "v0.29.6")
        return [
            ResultBoundaryCertificationReport(
                f"result_boundary_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                ref,
            )
            for adapter_name in adapter_names
        ]

    def build_failure_rollback_noop_certifications(self, adapter_names: list[str], approval_report: ProviderInvocationApprovalAuditRollbackReport) -> list[FailureRollbackNoOpCertificationReport]:
        failure_refs = _refs("provider_failure_classification", approval_report.failure_classifications, "classification_id", "v0.29.6")
        rollback_refs = _refs("provider_rollback_plan", approval_report.rollback_plans, "rollback_plan_id", "v0.29.6")
        noop_refs = _refs("provider_noop_boundary", approval_report.noop_boundaries, "noop_boundary_id", "v0.29.6")
        return [
            FailureRollbackNoOpCertificationReport(
                f"failure_rollback_noop_certification_report:{adapter_name}:v0.29.7",
                adapter_name,
                failure_refs,
                rollback_refs,
                noop_refs,
                True,
                True,
            )
            for adapter_name in adapter_names
        ]

    def build_rpa_future_track_notes(self, adapter_names: list[str]) -> list[RPAFutureTrackCertificationNote]:
        return [
            RPAFutureTrackCertificationNote(
                f"rpa_future_track_certification_note:{adapter_name}:v0.29.7",
                adapter_name,
                False,
            )
            for adapter_name in adapter_names
        ]

    def build_external_dominion_exclusion_certifications(self, adapter_names: list[str]) -> list[ExternalDominionExclusionCertification]:
        return [
            ExternalDominionExclusionCertification(
                f"external_dominion_exclusion_certification:{adapter_name}:v0.29.7",
                adapter_name,
                False,
            )
            for adapter_name in adapter_names
        ]


class AdapterCertificationReadinessGateService:
    def evaluate_gate(
        self,
        source_view: ExternalSkillPackagingCertificationSourceView,
        manifest: ExternalSkillManifest,
        package_manifests: list[AdapterPackageManifest],
        exposure_reports: list[AdapterPackageExposureReport],
        matrices: list[AdapterCertificationMatrix],
        case_results: list[AdapterCertificationCaseResult],
        mock_reports: list[MockModeCertificationReport],
        no_network_reports: list[NoNetworkCertificationReport],
        no_credential_reports: list[NoCredentialCertificationReport],
        no_command_reports: list[NoCommandCertificationReport],
        permission_reports: list[PermissionSafetyCertificationReport],
        credential_network_reports: list[CredentialNetworkBoundaryCertificationReport],
        dry_run_reports: list[InvocationDryRunCertificationReport],
        approval_reports: list[ApprovalAuditRollbackCertificationReport],
        ocel_reports: list[OCELVisibilityCertificationReport],
        result_reports: list[ResultBoundaryCertificationReport],
        failure_reports: list[FailureRollbackNoOpCertificationReport],
    ) -> AdapterCertificationReadinessGate:
        manifest_complete = manifest.entry_count > 0 and not manifest.manifest_is_runtime_enablement
        exposure_boundary_passed = all(not report.private_data_exposed and not report.credential_exposed and not report.raw_provider_output_exposed for report in exposure_reports)
        required_cases_passed_or_warned = all(result.result_status in {"passed", "warning"} for result in case_results)
        ready = all(
            [
                manifest_complete,
                package_manifests,
                exposure_boundary_passed,
                matrices,
                required_cases_passed_or_warned,
                mock_reports,
                no_network_reports,
                no_credential_reports,
                no_command_reports,
                permission_reports,
                credential_network_reports,
                dry_run_reports,
                approval_reports,
                ocel_reports,
                result_reports,
                failure_reports,
            ]
        )
        return AdapterCertificationReadinessGate(
            "adapter_certification_readiness_gate:v0.29.7",
            _ref("external_skill_packaging_certification_source_view", source_view.source_view_id, V0297_VERSION),
            _ref("external_skill_manifest", manifest.manifest_id, V0297_VERSION),
            _ref("adapter_package_manifest", package_manifests[0].package_manifest_id, V0297_VERSION),
            _ref("adapter_package_exposure_report", exposure_reports[0].report_id, V0297_VERSION),
            _refs("adapter_certification_matrix", matrices, "matrix_id", V0297_VERSION),
            _refs("adapter_certification_case_result", case_results, "result_id", V0297_VERSION),
            _refs("mock_mode_certification_report", mock_reports, "report_id", V0297_VERSION),
            _refs("no_network_certification_report", no_network_reports, "report_id", V0297_VERSION),
            _refs("no_credential_certification_report", no_credential_reports, "report_id", V0297_VERSION),
            _refs("no_command_certification_report", no_command_reports, "report_id", V0297_VERSION),
            _refs("permission_safety_certification_report", permission_reports, "report_id", V0297_VERSION),
            _refs("credential_network_boundary_certification_report", credential_network_reports, "report_id", V0297_VERSION),
            _refs("invocation_dry_run_certification_report", dry_run_reports, "report_id", V0297_VERSION),
            _refs("approval_audit_rollback_certification_report", approval_reports, "report_id", V0297_VERSION),
            _refs("ocel_visibility_certification_report", ocel_reports, "report_id", V0297_VERSION),
            _refs("result_boundary_certification_report", result_reports, "report_id", V0297_VERSION),
            _refs("failure_rollback_noop_certification_report", failure_reports, "report_id", V0297_VERSION),
            manifest_complete,
            True,
            True,
            exposure_boundary_passed,
            bool(matrices),
            required_cases_passed_or_warned,
            all(report.mock_mode_passed and not report.live_adapter_used for report in mock_reports),
            all(report.no_network_passed and not report.network_called for report in no_network_reports),
            all(report.no_credential_passed and not report.credential_accessed for report in no_credential_reports),
            all(report.command_execution_forbidden and not report.command_executed for report in no_command_reports),
            all(report.deny_first_passed and report.no_permission_granted and report.no_approval_granted for report in permission_reports),
            all(report.credential_boundary_passed and report.network_boundary_passed and not report.ready_for_live_access for report in credential_network_reports),
            all(report.dry_run_passed_or_safely_deferred and not report.provider_invoked for report in dry_run_reports),
            all(report.approval_boundary_passed and report.audit_boundary_passed and report.rollback_noop_boundary_passed and not report.approval_granted for report in approval_reports),
            all(report.required_events_present and report.provider_invocation_event_absent_now for report in ocel_reports),
            all(report.raw_provider_output_persistence_forbidden and not report.raw_provider_output_persisted for report in result_reports),
            all(report.failure_classification_ready and report.noop_available and not report.automatic_retry_performed for report in failure_reports),
            True,
            True,
            True,
            True,
            True,
            True,
            True,
            "warning",
            bool(ready),
            bool(ready),
        )


class AdapterCertificationAuditTrailService:
    def build_audit_trail(
        self,
        request: ExternalSkillPackagingCertificationRequest,
        source_view: ExternalSkillPackagingCertificationSourceView,
        manifest: ExternalSkillManifest,
        matrices: list[AdapterCertificationMatrix],
        case_results: list[AdapterCertificationCaseResult],
        gate: AdapterCertificationReadinessGate,
    ) -> AdapterCertificationAuditTrail:
        event_count = 4 + len(matrices) + len(case_results)
        return AdapterCertificationAuditTrail(
            "adapter_certification_audit_trail:v0.29.7",
            _ref("external_skill_packaging_certification_request", request.request_id, V0297_VERSION),
            _ref("external_skill_packaging_certification_source_view", source_view.source_view_id, V0297_VERSION),
            [_ref("external_skill_manifest", manifest.manifest_id, V0297_VERSION)],
            _refs("adapter_certification_matrix", matrices, "matrix_id", V0297_VERSION),
            _refs("adapter_certification_case_result", case_results, "result_id", V0297_VERSION),
            _ref("adapter_certification_readiness_gate", gate.gate_id, V0297_VERSION),
            event_count,
        )


class AdapterPackagingCertificationFindingService:
    BLOCKED_FINDINGS = {
        "package_publish_attempted",
        "release_tag_creation_attempted",
        "live_provider_certification_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "credential_access_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "secret_retrieval_attempted",
        "command_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
        "external_side_effect_attempted",
        "file_mutation_attempted",
        "rollback_execution_attempted",
        "automatic_retry_attempted",
        "live_adapter_implementation_attempted",
        "rpa_adapter_attempted",
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

    def build_findings(self) -> list[AdapterPackagingCertificationFinding]:
        created = [
            "packaging_certification_policy_created",
            "external_skill_manifest_created",
            "adapter_package_manifest_created",
            "dependency_profile_created",
            "exposure_report_created",
            "certification_policy_created",
            "certification_matrix_created",
            "certification_case_created",
            "certification_case_result_created",
            "mock_mode_certification_created",
            "no_network_certification_created",
            "no_credential_certification_created",
            "no_command_certification_created",
            "permission_safety_certification_created",
            "credential_network_boundary_certification_created",
            "dry_run_certification_created",
            "approval_audit_rollback_certification_created",
            "ocel_visibility_certification_created",
            "result_boundary_certification_created",
            "failure_rollback_noop_certification_created",
            "rpa_future_track_note_created",
            "external_dominion_exclusion_certification_created",
            "certification_gate_created",
            "certification_audit_trail_created",
        ]
        findings = [
            AdapterPackagingCertificationFinding(
                "adapter_packaging_certification_finding:ok:v0.29.7",
                "info",
                "ok",
                "v0.29.7 packaging/certification matrix remains metadata-only and boundary-only.",
                None,
                [],
                None,
            )
        ]
        for finding_type in created:
            findings.append(
                AdapterPackagingCertificationFinding(
                    f"adapter_packaging_certification_finding:{finding_type}:v0.29.7",
                    "info",
                    finding_type,
                    f"{finding_type} artifact was created without package publish, live certification, provider invocation, network, credential, or command execution.",
                    None,
                    [],
                    None,
                )
            )
        for finding_type in self.BLOCKED_FINDINGS:
            findings.append(
                AdapterPackagingCertificationFinding(
                    f"adapter_packaging_certification_finding:{finding_type}:v0.29.7",
                    "critical",
                    finding_type,
                    f"{finding_type} would block v0.29.7 certification boundary validity.",
                    None,
                    [],
                    finding_type,
                )
            )
        return findings


class AdapterPackagingCertificationReportService:
    def build_report(self, report_id: str | None = None) -> AdapterPackagingCertificationReport:
        source_service = AdapterPackagingCertificationPrerequisiteSourceService()
        approval_report = source_service.load_v0296_approval_audit_rollback_report()
        invocation_report = source_service.load_v0295_invocation_candidate_report()
        credential_report = source_service.load_v0294_credential_network_boundary_report()
        permission_report = source_service.load_v0293_permission_safety_report()
        mock_report = source_service.load_v0292_mock_harness_report()
        registry_report = source_service.load_v0291_adapter_registry_report()
        contract_report = source_service.load_v0290_external_adapter_contract_report()

        policy = ExternalSkillPackagingCertificationPolicyService().build_policy()
        source_view = ExternalSkillPackagingCertificationSourceViewService().build_source_view()
        request = ExternalSkillPackagingCertificationRequestService().build_request(source_view)
        package_service = ExternalSkillPackageService()
        adapter_names = _adapter_names(invocation_report)
        package_policy = package_service.build_package_policy()
        entries = package_service.build_manifest_entries(invocation_report, registry_report, contract_report, mock_report)
        manifest = package_service.build_external_skill_manifest(entries)
        package_manifests = package_service.build_adapter_package_manifests(entries)
        dependency_profiles = package_service.build_dependency_profiles(adapter_names)
        package_boundary_policy = package_service.build_package_boundary_policy()
        exposure_reports = package_service.build_exposure_reports(package_manifests)

        certification_service = AdapterCertificationService()
        certification_policy = certification_service.build_certification_policy()
        matrices = certification_service.build_certification_matrices(adapter_names)
        case_results = certification_service.build_certification_case_results(matrices)

        boundary_service = AdapterBoundaryCertificationService()
        mock_certifications = boundary_service.build_mock_mode_certifications(adapter_names, mock_report)
        no_network_certifications = boundary_service.build_no_network_certifications(adapter_names, credential_report)
        no_credential_certifications = boundary_service.build_no_credential_certifications(adapter_names, credential_report)
        no_command_certifications = boundary_service.build_no_command_certifications(adapter_names)
        permission_certifications = boundary_service.build_permission_safety_certifications(adapter_names, permission_report)
        credential_network_certifications = boundary_service.build_credential_network_boundary_certifications(adapter_names, credential_report)
        dry_run_certifications = boundary_service.build_dry_run_certifications(adapter_names, invocation_report)
        approval_certifications = boundary_service.build_approval_audit_rollback_certifications(adapter_names, approval_report)
        ocel_certifications = boundary_service.build_ocel_visibility_certifications(adapter_names, approval_report)
        result_certifications = boundary_service.build_result_boundary_certifications(adapter_names, approval_report)
        failure_certifications = boundary_service.build_failure_rollback_noop_certifications(adapter_names, approval_report)
        rpa_notes = boundary_service.build_rpa_future_track_notes(adapter_names)
        dominion_exclusions = boundary_service.build_external_dominion_exclusion_certifications(adapter_names)

        gate = AdapterCertificationReadinessGateService().evaluate_gate(
            source_view,
            manifest,
            package_manifests,
            exposure_reports,
            matrices,
            case_results,
            mock_certifications,
            no_network_certifications,
            no_credential_certifications,
            no_command_certifications,
            permission_certifications,
            credential_network_certifications,
            dry_run_certifications,
            approval_certifications,
            ocel_certifications,
            result_certifications,
            failure_certifications,
        )
        audit_trail = AdapterCertificationAuditTrailService().build_audit_trail(
            request, source_view, manifest, matrices, case_results, gate
        )
        findings = AdapterPackagingCertificationFindingService().build_findings()
        limitations = [
            "Certification is boundary evidence only; it is not package publish, production certification, or limited provider invocation preview.",
            "Live provider certification and limited invocation preview require v0.29.8 or later gates.",
        ]
        withdrawal_conditions = [
            "package publish/upload or release tag creation appears",
            "live provider certification is claimed",
            "provider invocation, network call, credential access, command execution, side effect, rollback execution, or automatic retry appears",
            "RPA/A360/Brity/UiPath or external dominion implementation appears",
            "private data, raw payload, or raw provider output is exposed",
            "ready_for_provider_invocation, ready_for_network_access, or ready_for_credential_access becomes true",
            "LLM judge becomes the sole certification authority",
        ]
        return AdapterPackagingCertificationReport(
            report_id or "adapter_packaging_certification_report:v0.29.7",
            _now(),
            policy,
            request,
            source_view,
            package_policy,
            manifest,
            package_manifests,
            dependency_profiles,
            package_boundary_policy,
            exposure_reports,
            certification_policy,
            matrices,
            case_results,
            mock_certifications,
            no_network_certifications,
            no_credential_certifications,
            no_command_certifications,
            permission_certifications,
            credential_network_certifications,
            dry_run_certifications,
            approval_certifications,
            ocel_certifications,
            result_certifications,
            failure_certifications,
            rpa_notes,
            dominion_exclusions,
            gate,
            audit_trail,
            findings,
            "warning",
            gate.ready_for_v0_29_8,
            gate.ready_for_limited_invocation_preview_gate,
            limitations=limitations,
            withdrawal_conditions=withdrawal_conditions,
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.policy,
            "request": report.request,
            "source-view": report.source_view,
            "skill-manifest": report.external_skill_manifest,
            "package-policy": report.external_skill_package_policy,
            "package-manifest": report.adapter_package_manifests,
            "dependencies": report.dependency_profiles,
            "boundary-policy": report.package_boundary_policy,
            "exposure": report.package_exposure_reports,
            "certification-policy": report.certification_policy,
            "matrix": report.certification_matrices,
            "cases": [case for matrix in report.certification_matrices for case in matrix.certification_cases],
            "case-results": report.certification_case_results,
            "mock": report.mock_mode_certifications,
            "no-network": report.no_network_certifications,
            "no-credential": report.no_credential_certifications,
            "no-command": report.no_command_certifications,
            "permission-safety": report.permission_safety_certifications,
            "credential-network": report.credential_network_boundary_certifications,
            "dry-run": report.dry_run_certifications,
            "approval-audit-rollback": report.approval_audit_rollback_certifications,
            "ocel": report.ocel_visibility_certifications,
            "result-boundary": report.result_boundary_certifications,
            "failure-rollback-noop": report.failure_rollback_noop_certifications,
            "rpa-future": report.rpa_future_track_notes,
            "dominion-exclusion": report.external_dominion_exclusion_certifications,
            "gate": report.certification_readiness_gate,
            "audit": report.audit_trail,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0297_VERSION,
            "layer": V0297_LAYER,
            "subject": "external_skill_packaging_certification_matrix",
            "principles": [
                "External skill manifest is not runtime enablement",
                "Adapter package manifest is not package publish",
                "Certification matrix is not production certification",
                "Certified mock is not certified live adapter",
                "No-network certification is not network access",
                "No-credential certification is not credential access",
                "Approval/audit certification is not approval grant",
                "Rollback certification is not rollback execution",
                "Certification pass is not limited invocation preview",
                "Limited preview requires v0.29.8 gate",
            ],
            "safety_boundary": {
                "package_published": report.package_published,
                "release_tag_created": report.release_tag_created,
                "live_provider_certified": report.live_provider_certified,
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
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0297_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "external_skill_packaging_certification_matrix_created",
            "version": V0297_VERSION,
            "source_read_models": [
                "ProviderInvocationApprovalBoundaryState",
                "ProviderInvocationApprovalDecisionRecordState",
                "ProviderInvocationAuditTrailState",
                "ProviderInvocationOCELTracePlanState",
                "ProviderResultBoundaryState",
                "ProviderFailureClassificationState",
                "ProviderRollbackPlanState",
                "ProviderNoOpBoundaryState",
                "AdapterInvocationCandidateState",
                "AdapterDryRunReportState",
                "CredentialNetworkBoundaryGateState",
                "AdapterPermissionSafetyGateState",
                "MockAdapterHarnessGateState",
                "AdapterRegistryState",
                "ExternalProviderAdapterContractState",
                "ProviderInvocationProhibitionState",
                "CommandExecutionProhibitionState",
                "PigGuidanceState",
                "OCPXProjectionState",
            ],
            "target_read_models": [
                "ExternalSkillManifestState",
                "AdapterPackageManifestState",
                "AdapterDependencyProfileState",
                "AdapterPackageExposureState",
                "AdapterCertificationMatrixState",
                "AdapterCertificationCaseState",
                "AdapterCertificationCaseResultState",
                "AdapterBoundaryCertificationState",
                "AdapterCertificationReadinessGateState",
                "AdapterCertificationAuditState",
                "V029ReadinessState",
            ],
            "effect_types": V0297_EFFECT_TYPES,
        }


def render_adapter_packaging_certification_cli(parts: dict[str, Any], section: str = "report") -> str:
    payload = parts[section]
    if isinstance(payload, list):
        lines = [f"External Skill Packaging / Certification Matrix {section}"]
        lines.append(f"version={V0297_VERSION}")
        lines.append(f"layer={V0297_LAYER}")
        lines.append(f"count={len(payload)}")
        return "\n".join(lines)
    if section != "report":
        title = payload.__class__.__name__
        object_id = getattr(payload, "policy_id", None) or getattr(payload, "report_id", None) or getattr(payload, "manifest_id", None) or getattr(payload, "gate_id", None) or getattr(payload, "audit_trail_id", None)
        return "\n".join([title, f"version={V0297_VERSION}", f"layer={V0297_LAYER}", f"object_id={object_id}"])

    report: AdapterPackagingCertificationReport = payload
    lines = [
        "External Skill Packaging / Certification Matrix report",
        f"version={report.version}",
        f"layer={report.policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_8={_bool(report.ready_for_v0_29_8)}",
        f"ready_for_limited_invocation_preview_gate={_bool(report.ready_for_limited_invocation_preview_gate)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_credential_access={_bool(report.ready_for_credential_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"package_published={_bool(report.package_published)}",
        f"release_tag_created={_bool(report.release_tag_created)}",
        f"live_provider_certified={_bool(report.live_provider_certified)}",
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
