from __future__ import annotations

from dataclasses import asdict, dataclass, field, is_dataclass
from typing import Any

from chanta_core.public_alpha_schumpeter_preparation import V028ConsolidationReportService
from chanta_core.utility.time import utc_now_iso


V0290_VERSION = "v0.29.0"
V0290_LAYER = "external_provider_adapter"
V0290_TRACK = "External Skill / External Provider Adapter Development"
V0290_NAME = "External Provider Adapter Contract"
V0290_KOREAN_NAME = "External Provider Adapter 계약"
V0290_NEXT_STEP = "v0.29.1 Provider Capability Inventory / Adapter Registry"

V0290_OBJECT_TYPES = [
    "external_provider_adapter_track_policy",
    "external_adapter_contract_request",
    "external_adapter_contract_source_view",
    "external_provider_adapter_contract",
    "external_skill_adapter_contract",
    "adapter_lifecycle_contract",
    "adapter_capability_contract",
    "adapter_input_schema_contract",
    "adapter_output_schema_contract",
    "adapter_effect_boundary_contract",
    "adapter_permission_requirement_contract",
    "adapter_safety_requirement_contract",
    "adapter_credential_requirement_contract",
    "adapter_network_requirement_contract",
    "adapter_audit_requirement_contract",
    "adapter_rollback_noop_requirement_contract",
    "adapter_ocel_visibility_contract",
    "adapter_mock_no_network_requirement_contract",
    "adapter_certification_requirement_contract",
    "provider_invocation_prohibition_contract",
    "command_execution_prohibition_contract",
    "external_adapter_contract_finding",
    "external_adapter_contract_report",
    "v028_consolidation_report",
    "external_adapter_contract_handoff_packet",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

V0290_EVENT_TYPES = [
    "external_adapter_contract_requested",
    "external_adapter_contract_prerequisites_loaded",
    "external_provider_adapter_track_policy_created",
    "external_adapter_contract_source_view_created",
    "external_provider_adapter_contract_created",
    "external_skill_adapter_contract_created",
    "adapter_lifecycle_contract_created",
    "adapter_capability_contract_created",
    "adapter_input_schema_contract_created",
    "adapter_output_schema_contract_created",
    "adapter_effect_boundary_contract_created",
    "adapter_permission_requirement_contract_created",
    "adapter_safety_requirement_contract_created",
    "adapter_credential_requirement_contract_created",
    "adapter_network_requirement_contract_created",
    "adapter_audit_requirement_contract_created",
    "adapter_rollback_noop_requirement_contract_created",
    "adapter_ocel_visibility_contract_created",
    "adapter_mock_no_network_requirement_contract_created",
    "adapter_certification_requirement_contract_created",
    "provider_invocation_prohibition_contract_created",
    "command_execution_prohibition_contract_created",
    "external_adapter_contract_report_created",
    "external_adapter_contract_warning_created",
    "external_adapter_contract_blocked",
]

V0290_EFFECT_TYPES = [
    "read_only_observation",
    "external_adapter_contract_created",
    "adapter_requirement_contract_created",
    "provider_invocation_prohibition_declared",
    "command_execution_prohibition_declared",
    "state_candidate_created",
]

V0290_FORBIDDEN_EFFECT_TYPES = [
    "external_provider_adapter_implemented",
    "external_skill_adapter_implemented",
    "provider_registered",
    "provider_invoked",
    "provider_sdk_invoked",
    "network_called",
    "credential_stored",
    "credential_logged",
    "env_file_created",
    "command_executed",
    "shell_execution_surface_created",
    "subprocess_expansion_added",
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
    "references_runtime_dependency_added",
    "references_code_copied",
    "PIG_execution_authority_enabled",
    "llm_judge_used",
]


def _now() -> str:
    return utc_now_iso()


def _bool(value: bool) -> str:
    return str(value).lower()


def _ref(object_type: str, object_id: str, version: str | None = None) -> dict[str, Any]:
    ref: dict[str, Any] = {"object_type": object_type, "object_id": object_id}
    if version:
        ref["version"] = version
    return ref


class ModelMixin:
    def to_dict(self) -> dict[str, Any]:
        def convert(value: Any) -> Any:
            if is_dataclass(value):
                return {key: convert(item) for key, item in asdict(value).items()}
            if isinstance(value, list):
                return [convert(item) for item in value]
            if isinstance(value, dict):
                return {key: convert(item) for key, item in value.items()}
            return value

        return convert(self)


@dataclass
class ExternalProviderAdapterTrackPolicy(ModelMixin):
    policy_id: str
    version: str = V0290_VERSION
    layer: str = V0290_LAYER
    track_name: str = V0290_TRACK
    contract_only: bool = True
    adapter_implementation_enabled_now: bool = False
    provider_registration_enabled_now: bool = False
    provider_invocation_enabled_now: bool = False
    network_access_enabled_now: bool = False
    credential_storage_enabled_now: bool = False
    command_execution_expansion_enabled_now: bool = False
    rpa_adapter_enabled_now: bool = False
    external_agent_dominion_enabled_now: bool = False
    schumpeter_private_runtime_enabled_now: bool = False
    mock_no_network_required_before_live: bool = True
    permission_gate_required_before_invocation: bool = True
    safety_gate_required_before_invocation: bool = True
    credential_boundary_required_before_invocation: bool = True
    network_boundary_required_before_invocation: bool = True
    audit_required_before_invocation: bool = True
    rollback_or_noop_required_before_invocation: bool = True
    ocel_visibility_required_before_invocation: bool = True
    llm_judge_as_sole_contract_authority_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class ExternalAdapterContractRequest(ModelMixin):
    request_id: str
    v0289_consolidation_report_id: str | None
    v029_handoff_packet_id: str | None
    external_adapter_preflight_report_id: str | None
    requested_contract_scope: str
    strictness: str = "standard"
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class ExternalAdapterContractSourceView(ModelMixin):
    source_view_id: str
    v0289_consolidation_report_ref: dict[str, Any] | None
    v029_readiness_report_ref: dict[str, Any] | None
    v029_handoff_packet_ref: dict[str, Any] | None
    external_adapter_preflight_report_ref: dict[str, Any] | None
    provider_invocation_reopen_criteria_ref: dict[str, Any] | None
    command_execution_reopen_criteria_ref: dict[str, Any] | None
    credential_boundary_preflight_ref: dict[str, Any] | None
    network_boundary_preflight_ref: dict[str, Any] | None
    permission_boundary_preflight_ref: dict[str, Any] | None
    safety_gate_preflight_ref: dict[str, Any] | None
    audit_rollback_ocel_preflight_ref: dict[str, Any] | None
    adapter_certification_preflight_ref: dict[str, Any] | None
    public_private_boundary_report_ref: dict[str, Any] | None
    memory_consolidation_report_ref: dict[str, Any] | None
    workbench_consolidation_report_ref: dict[str, Any] | None
    source_status: str
    ready_for_v0_29_contract: bool | None
    ready_for_provider_invocation: bool = False
    ready_for_command_execution: bool = False
    provider_invocation_detected: bool = False
    network_call_detected: bool = False
    command_execution_detected: bool = False
    credential_value_detected: bool = False
    private_material_detected: bool = False
    raw_provider_output_detected: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class ExternalProviderAdapterContract(ModelMixin):
    contract_id: str
    provider_kind: str
    adapter_contract_name: str = "ExternalProviderAdapterContract"
    contract_status: str = "ready"
    adapter_interface_required: bool = True
    capability_declaration_required: bool = True
    input_schema_required: bool = True
    output_schema_required: bool = True
    effect_boundary_required: bool = True
    permission_requirement_required: bool = True
    safety_requirement_required: bool = True
    credential_requirement_required: bool = True
    network_requirement_required: bool = True
    audit_requirement_required: bool = True
    rollback_noop_requirement_required: bool = True
    ocel_visibility_required: bool = True
    mock_no_network_mode_required: bool = True
    certification_required: bool = True
    adapter_implemented_now: bool = False
    provider_registered_now: bool = False
    provider_invoked_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class ExternalSkillAdapterContract(ModelMixin):
    contract_id: str
    external_skill_contract_name: str = "ExternalSkillAdapterContract"
    skill_manifest_required: bool = True
    skill_capability_declaration_required: bool = True
    skill_effect_boundary_required: bool = True
    skill_permission_scope_required: bool = True
    skill_safety_gate_required: bool = True
    skill_ocel_visibility_required: bool = True
    skill_mock_mode_required: bool = True
    skill_certification_required: bool = True
    external_skill_implemented_now: bool = False
    external_skill_executed_now: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterLifecycleContract(ModelMixin):
    contract_id: str
    allowed_lifecycle_states: list[str]
    lifecycle_transition_requires_audit: bool = True
    registration_is_not_execution: bool = True
    certification_is_not_live_invocation: bool = True
    preview_is_not_unbounded_runtime: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterCapabilityContract(ModelMixin):
    contract_id: str
    capability_declaration_required: bool = True
    capability_id_required: bool = True
    capability_name_required: bool = True
    capability_description_required: bool = True
    input_capability_schema_required: bool = True
    output_capability_schema_required: bool = True
    effect_type_declaration_required: bool = True
    risk_level_required: bool = True
    permission_scope_required: bool = True
    capability_declaration_is_not_permission: bool = True
    capability_declaration_is_not_invocation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterInputSchemaContract(ModelMixin):
    contract_id: str
    input_schema_required: bool = True
    input_validation_required: bool = True
    private_data_boundary_required: bool = True
    credential_reference_boundary_required: bool = True
    raw_secret_input_forbidden: bool = True
    raw_private_payload_forbidden_by_default: bool = True
    schema_version_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterOutputSchemaContract(ModelMixin):
    contract_id: str
    output_schema_required: bool = True
    output_validation_required: bool = True
    raw_provider_output_persistence_forbidden_by_default: bool = True
    output_redaction_policy_required: bool = True
    output_summary_boundary_required: bool = True
    output_error_schema_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterEffectBoundaryContract(ModelMixin):
    contract_id: str
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    effect_boundary_required: bool = True
    external_side_effect_requires_future_gate: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterPermissionRequirementContract(ModelMixin):
    contract_id: str
    permission_gate_required: bool = True
    scoped_permission_required: bool = True
    permission_expiry_required: bool = True
    user_approval_surface_required: bool = True
    approval_record_required: bool = True
    permission_restoration_without_approval_forbidden: bool = True
    deny_first_default_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterSafetyRequirementContract(ModelMixin):
    contract_id: str
    safety_gate_required: bool = True
    risk_classification_required: bool = True
    private_data_check_required: bool = True
    credential_check_required: bool = True
    external_side_effect_check_required: bool = True
    data_exfiltration_check_required: bool = True
    unsafe_adapter_blocks_invocation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterCredentialRequirementContract(ModelMixin):
    contract_id: str
    credential_boundary_required: bool = True
    credential_value_storage_enabled_now: bool = False
    credential_value_logging_forbidden: bool = True
    committed_credentials_forbidden: bool = True
    secret_reference_only_required: bool = True
    external_secret_store_contract_required_later: bool = True
    credential_redaction_required: bool = True
    credential_audit_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterNetworkRequirementContract(ModelMixin):
    contract_id: str
    network_boundary_required: bool = True
    network_access_enabled_now: bool = False
    no_network_default_required: bool = True
    outbound_domain_policy_required: bool = True
    timeout_policy_required: bool = True
    retry_policy_required: bool = True
    request_audit_required: bool = True
    data_exfiltration_boundary_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterAuditRequirementContract(ModelMixin):
    contract_id: str
    audit_required: bool = True
    adapter_lifecycle_audit_required: bool = True
    permission_decision_audit_required: bool = True
    safety_decision_audit_required: bool = True
    invocation_candidate_audit_required: bool = True
    provider_result_audit_required_later: bool = True
    raw_secret_audit_output_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterRollbackNoOpRequirementContract(ModelMixin):
    contract_id: str
    rollback_or_noop_boundary_required: bool = True
    no_op_fallback_required: bool = True
    rollback_plan_required_before_side_effect: bool = True
    failure_classification_required: bool = True
    partial_failure_policy_required: bool = True
    external_side_effect_without_rollback_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterOCELVisibilityContract(ModelMixin):
    contract_id: str
    ocel_visibility_required: bool = True
    adapter_declared_event_required: bool = True
    capability_declared_event_required: bool = True
    permission_decision_event_required: bool = True
    safety_decision_event_required: bool = True
    credential_boundary_event_required: bool = True
    network_boundary_event_required: bool = True
    invocation_candidate_event_required: bool = True
    dry_run_event_required: bool = True
    approval_event_required: bool = True
    audit_event_required: bool = True
    future_provider_invocation_event_required: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterMockNoNetworkRequirementContract(ModelMixin):
    contract_id: str
    mock_mode_required_before_live: bool = True
    no_network_default_required: bool = True
    deterministic_fixture_required: bool = True
    mock_response_schema_required: bool = True
    live_provider_disabled_by_default: bool = True
    credential_not_required_for_mock: bool = True
    provider_sdk_not_required_for_mock: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class AdapterCertificationRequirementContract(ModelMixin):
    contract_id: str
    certification_required_before_preview: bool = True
    adapter_test_matrix_required: bool = True
    boundary_tests_required: bool = True
    mock_mode_certification_required: bool = True
    no_network_certification_required: bool = True
    no_credential_certification_required: bool = True
    ocel_visibility_certification_required: bool = True
    certification_is_not_live_invocation: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class ProviderInvocationProhibitionContract(ModelMixin):
    contract_id: str
    provider_invocation_forbidden_now: bool = True
    provider_registration_forbidden_now: bool = True
    provider_sdk_invocation_forbidden_now: bool = True
    external_api_call_forbidden_now: bool = True
    network_call_forbidden_now: bool = True
    ready_for_provider_invocation: bool = False
    future_reopen_version: str = "v0.29.8 Limited Provider Invocation Preview Gate"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class CommandExecutionProhibitionContract(ModelMixin):
    contract_id: str
    command_execution_expansion_forbidden_now: bool = True
    shell_execution_forbidden_now: bool = True
    shell_true_forbidden: bool = True
    unbounded_subprocess_forbidden: bool = True
    command_execution_reopen_requires_future_contract: bool = True
    ready_for_command_execution: bool = False
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)
    version: str = V0290_VERSION


@dataclass
class ExternalAdapterContractFinding(ModelMixin):
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None


@dataclass
class ExternalAdapterContractReport(ModelMixin):
    report_id: str
    created_at: str
    track_policy: ExternalProviderAdapterTrackPolicy
    request: ExternalAdapterContractRequest
    source_view: ExternalAdapterContractSourceView
    provider_adapter_contract: ExternalProviderAdapterContract
    external_skill_adapter_contract: ExternalSkillAdapterContract
    lifecycle_contract: AdapterLifecycleContract
    capability_contract: AdapterCapabilityContract
    input_schema_contract: AdapterInputSchemaContract
    output_schema_contract: AdapterOutputSchemaContract
    effect_boundary_contract: AdapterEffectBoundaryContract
    permission_requirement_contract: AdapterPermissionRequirementContract
    safety_requirement_contract: AdapterSafetyRequirementContract
    credential_requirement_contract: AdapterCredentialRequirementContract
    network_requirement_contract: AdapterNetworkRequirementContract
    audit_requirement_contract: AdapterAuditRequirementContract
    rollback_noop_requirement_contract: AdapterRollbackNoOpRequirementContract
    ocel_visibility_contract: AdapterOCELVisibilityContract
    mock_no_network_requirement_contract: AdapterMockNoNetworkRequirementContract
    certification_requirement_contract: AdapterCertificationRequirementContract
    provider_invocation_prohibition_contract: ProviderInvocationProhibitionContract
    command_execution_prohibition_contract: CommandExecutionProhibitionContract
    findings: list[ExternalAdapterContractFinding]
    report_status: str
    ready_for_v0_29_1: bool
    ready_for_adapter_registry: bool
    ready_for_adapter_implementation: bool = False
    ready_for_provider_registration: bool = False
    ready_for_provider_invocation: bool = False
    ready_for_network_access: bool = False
    ready_for_command_execution: bool = False
    adapter_implemented: bool = False
    provider_registered: bool = False
    provider_invoked: bool = False
    network_called: bool = False
    command_executed: bool = False
    credential_stored: bool = False
    credential_logged: bool = False
    env_file_created: bool = False
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
    references_runtime_dependency_added: bool = False
    references_code_copied: bool = False
    PIG_execution_authority_enabled: bool = False
    llm_judge_used: bool = False
    next_required_step: str = V0290_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.29.1 Provider Capability Inventory / Adapter Registry begins or External Provider Adapter Contract policy changes."
    version: str = V0290_VERSION


class ExternalAdapterContractPrerequisiteSourceService:
    def load_v0289_consolidation_report(self) -> dict[str, Any] | None:
        return _ref("v028_consolidation_report", "v028_consolidation_report:v0.28.9", "v0.28.9")

    def load_v029_readiness_report(self) -> dict[str, Any] | None:
        return _ref("v029_readiness_report", "v029_readiness_report:v0.28.9", "v0.28.9")

    def load_external_adapter_contract_handoff_packet(self) -> dict[str, Any] | None:
        return _ref("external_adapter_contract_handoff_packet", "external_adapter_contract_handoff_packet:v0.28.9", "v0.28.9")

    def load_external_adapter_preflight_report(self) -> dict[str, Any] | None:
        return _ref("external_adapter_preflight_report", "external_adapter_preflight_report:v0.28.8", "v0.28.8")

    def load_provider_invocation_reopen_criteria(self) -> dict[str, Any] | None:
        return _ref("provider_invocation_reopen_criteria", "provider_invocation_reopen_criteria:v0.28.8", "v0.28.8")

    def load_command_execution_reopen_criteria(self) -> dict[str, Any] | None:
        return _ref("command_execution_reopen_criteria", "command_execution_reopen_criteria:v0.28.8", "v0.28.8")

    def load_credential_boundary_preflight(self) -> dict[str, Any] | None:
        return _ref("credential_boundary_preflight", "credential_boundary_preflight:v0.28.8", "v0.28.8")

    def load_network_boundary_preflight(self) -> dict[str, Any] | None:
        return _ref("network_boundary_preflight", "network_boundary_preflight:v0.28.8", "v0.28.8")

    def load_permission_boundary_preflight(self) -> dict[str, Any] | None:
        return _ref("permission_boundary_preflight", "permission_boundary_preflight:v0.28.8", "v0.28.8")

    def load_safety_gate_preflight(self) -> dict[str, Any] | None:
        return _ref("safety_gate_preflight", "safety_gate_preflight:v0.28.8", "v0.28.8")

    def load_audit_rollback_ocel_preflight(self) -> dict[str, Any] | None:
        return _ref("audit_rollback_ocel_preflight", "audit_rollback_ocel_preflight:v0.28.8", "v0.28.8")

    def load_adapter_certification_preflight(self) -> dict[str, Any] | None:
        return _ref("adapter_certification_preflight", "adapter_certification_preflight:v0.28.8", "v0.28.8")

    def load_public_private_boundary_report(self) -> dict[str, Any] | None:
        return _ref("public_private_boundary_report", "public_private_boundary_report:v0.28.3", "v0.28.3")

    def load_memory_consolidation_report(self) -> dict[str, Any] | None:
        return _ref("memory_consolidation_report", "memory_consolidation_report:v0.27.9", "v0.27.9")

    def load_workbench_consolidation_report(self) -> dict[str, Any] | None:
        return _ref("workbench_consolidation_report", "workbench_consolidation_report:v0.26.9", "v0.26.9")

    def ready_for_v0_29_contract(self) -> bool | None:
        return V028ConsolidationReportService().build_report().v029_readiness_report.ready_for_v0_29_contract


class ExternalProviderAdapterTrackPolicyService:
    def build_policy(self) -> ExternalProviderAdapterTrackPolicy:
        return ExternalProviderAdapterTrackPolicy("external_provider_adapter_track_policy:v0.29.0")


class ExternalAdapterContractRequestService:
    def build_request(self, source: ExternalAdapterContractPrerequisiteSourceService) -> ExternalAdapterContractRequest:
        consolidation = source.load_v0289_consolidation_report()
        handoff = source.load_external_adapter_contract_handoff_packet()
        preflight = source.load_external_adapter_preflight_report()
        refs = [ref for ref in [consolidation, handoff, preflight] if ref is not None]
        return ExternalAdapterContractRequest(
            "external_adapter_contract_request:v0.29.0",
            consolidation["object_id"] if consolidation else None,
            handoff["object_id"] if handoff else None,
            preflight["object_id"] if preflight else None,
            "full_contract_pack",
            source_refs=refs,
        )


class ExternalAdapterContractSourceViewService:
    def build_source_view(self, source: ExternalAdapterContractPrerequisiteSourceService) -> ExternalAdapterContractSourceView:
        return ExternalAdapterContractSourceView(
            "external_adapter_contract_source_view:v0.29.0",
            source.load_v0289_consolidation_report(),
            source.load_v029_readiness_report(),
            source.load_external_adapter_contract_handoff_packet(),
            source.load_external_adapter_preflight_report(),
            source.load_provider_invocation_reopen_criteria(),
            source.load_command_execution_reopen_criteria(),
            source.load_credential_boundary_preflight(),
            source.load_network_boundary_preflight(),
            source.load_permission_boundary_preflight(),
            source.load_safety_gate_preflight(),
            source.load_audit_rollback_ocel_preflight(),
            source.load_adapter_certification_preflight(),
            source.load_public_private_boundary_report(),
            source.load_memory_consolidation_report(),
            source.load_workbench_consolidation_report(),
            "partial",
            source.ready_for_v0_29_contract(),
        )


class ExternalProviderAdapterContractService:
    def build_contract(self, provider_kind: str = "unknown") -> ExternalProviderAdapterContract:
        return ExternalProviderAdapterContract("external_provider_adapter_contract:v0.29.0", provider_kind)


class ExternalSkillAdapterContractService:
    def build_contract(self) -> ExternalSkillAdapterContract:
        return ExternalSkillAdapterContract("external_skill_adapter_contract:v0.29.0")


class AdapterLifecycleContractService:
    STATES = ["declared", "inventoried", "registered", "mocked", "certified_mock", "gated", "dry_run_candidate", "approval_required", "preview_allowed", "disabled", "blocked", "deprecated"]

    def build_contract(self) -> AdapterLifecycleContract:
        return AdapterLifecycleContract("adapter_lifecycle_contract:v0.29.0", list(self.STATES))


class AdapterCapabilityContractService:
    def build_contract(self) -> AdapterCapabilityContract:
        return AdapterCapabilityContract("adapter_capability_contract:v0.29.0")


class AdapterSchemaContractService:
    def build_input_schema_contract(self) -> AdapterInputSchemaContract:
        return AdapterInputSchemaContract("adapter_input_schema_contract:v0.29.0")

    def build_output_schema_contract(self) -> AdapterOutputSchemaContract:
        return AdapterOutputSchemaContract("adapter_output_schema_contract:v0.29.0")


class AdapterEffectBoundaryContractService:
    ALLOWED = ["read_only_observation", "mock_provider_response", "dry_run_plan_created", "invocation_candidate_created", "approval_record_created", "audit_record_created", "ocel_trace_created"]
    FORBIDDEN = ["provider_invoked", "network_called", "command_executed", "credential_stored", "external_side_effect_performed", "file_mutated_by_adapter", "private_data_exfiltrated"]

    def build_contract(self) -> AdapterEffectBoundaryContract:
        return AdapterEffectBoundaryContract("adapter_effect_boundary_contract:v0.29.0", list(self.ALLOWED), list(self.FORBIDDEN))


class AdapterRequirementContractService:
    def build_permission_requirement_contract(self) -> AdapterPermissionRequirementContract:
        return AdapterPermissionRequirementContract("adapter_permission_requirement_contract:v0.29.0")

    def build_safety_requirement_contract(self) -> AdapterSafetyRequirementContract:
        return AdapterSafetyRequirementContract("adapter_safety_requirement_contract:v0.29.0")

    def build_credential_requirement_contract(self) -> AdapterCredentialRequirementContract:
        return AdapterCredentialRequirementContract("adapter_credential_requirement_contract:v0.29.0")

    def build_network_requirement_contract(self) -> AdapterNetworkRequirementContract:
        return AdapterNetworkRequirementContract("adapter_network_requirement_contract:v0.29.0")

    def build_audit_requirement_contract(self) -> AdapterAuditRequirementContract:
        return AdapterAuditRequirementContract("adapter_audit_requirement_contract:v0.29.0")

    def build_rollback_noop_requirement_contract(self) -> AdapterRollbackNoOpRequirementContract:
        return AdapterRollbackNoOpRequirementContract("adapter_rollback_noop_requirement_contract:v0.29.0")

    def build_ocel_visibility_contract(self) -> AdapterOCELVisibilityContract:
        return AdapterOCELVisibilityContract("adapter_ocel_visibility_contract:v0.29.0")

    def build_mock_no_network_requirement_contract(self) -> AdapterMockNoNetworkRequirementContract:
        return AdapterMockNoNetworkRequirementContract("adapter_mock_no_network_requirement_contract:v0.29.0")

    def build_certification_requirement_contract(self) -> AdapterCertificationRequirementContract:
        return AdapterCertificationRequirementContract("adapter_certification_requirement_contract:v0.29.0")


class AdapterProhibitionContractService:
    def build_provider_invocation_prohibition_contract(self) -> ProviderInvocationProhibitionContract:
        return ProviderInvocationProhibitionContract("provider_invocation_prohibition_contract:v0.29.0")

    def build_command_execution_prohibition_contract(self) -> CommandExecutionProhibitionContract:
        return CommandExecutionProhibitionContract("command_execution_prohibition_contract:v0.29.0")


class ExternalAdapterContractFindingService:
    BLOCKED_FINDINGS = {
        "adapter_implementation_attempted",
        "provider_registration_attempted",
        "provider_invocation_attempted",
        "provider_sdk_invocation_attempted",
        "network_call_attempted",
        "credential_storage_attempted",
        "credential_logging_attempted",
        "env_file_creation_attempted",
        "command_execution_attempted",
        "shell_execution_attempted",
        "shell_true_detected",
        "unbounded_subprocess_detected",
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
        "references_runtime_dependency_detected",
        "references_code_copy_detected",
        "PIG_execution_authority_detected",
        "llm_judge_detected",
    }

    def build_findings(self) -> list[ExternalAdapterContractFinding]:
        return [
            ExternalAdapterContractFinding("external_adapter_contract_finding:track_policy_created:v0.29.0", "info", "external_provider_adapter_track_policy_created", "External provider adapter track policy created as contract-only metadata.", _ref("external_provider_adapter_track_policy", "external_provider_adapter_track_policy:v0.29.0", V0290_VERSION), [], None),
            ExternalAdapterContractFinding("external_adapter_contract_finding:provider_contract_created:v0.29.0", "info", "external_provider_adapter_contract_created", "Provider adapter contract created without adapter implementation, provider registration, or provider invocation.", _ref("external_provider_adapter_contract", "external_provider_adapter_contract:v0.29.0", V0290_VERSION), [], "Withdraw if v0.29.0 adds live adapter implementation, registration, invocation, network, credential, or command behavior."),
            ExternalAdapterContractFinding("external_adapter_contract_finding:provider_invocation_prohibited:v0.29.0", "info", "provider_invocation_prohibition_contract_created", "Provider invocation remains forbidden until the future limited preview gate.", _ref("provider_invocation_prohibition_contract", "provider_invocation_prohibition_contract:v0.29.0", V0290_VERSION), [], "Withdraw if ready_for_provider_invocation becomes true before the future gate."),
            ExternalAdapterContractFinding("external_adapter_contract_finding:command_execution_prohibited:v0.29.0", "info", "command_execution_prohibition_contract_created", "Command execution expansion remains forbidden by the contract.", _ref("command_execution_prohibition_contract", "command_execution_prohibition_contract:v0.29.0", V0290_VERSION), [], "Withdraw if ready_for_command_execution becomes true or shell/subprocess expansion is added."),
        ]


class ExternalAdapterContractReportService:
    def build_report(self, report_id: str | None = None) -> ExternalAdapterContractReport:
        source = ExternalAdapterContractPrerequisiteSourceService()
        policy = ExternalProviderAdapterTrackPolicyService().build_policy()
        request = ExternalAdapterContractRequestService().build_request(source)
        source_view = ExternalAdapterContractSourceViewService().build_source_view(source)
        schema = AdapterSchemaContractService()
        requirements = AdapterRequirementContractService()
        prohibitions = AdapterProhibitionContractService()
        findings = ExternalAdapterContractFindingService().build_findings()
        return ExternalAdapterContractReport(
            report_id or "external_adapter_contract_report:v0.29.0",
            _now(),
            policy,
            request,
            source_view,
            ExternalProviderAdapterContractService().build_contract(),
            ExternalSkillAdapterContractService().build_contract(),
            AdapterLifecycleContractService().build_contract(),
            AdapterCapabilityContractService().build_contract(),
            schema.build_input_schema_contract(),
            schema.build_output_schema_contract(),
            AdapterEffectBoundaryContractService().build_contract(),
            requirements.build_permission_requirement_contract(),
            requirements.build_safety_requirement_contract(),
            requirements.build_credential_requirement_contract(),
            requirements.build_network_requirement_contract(),
            requirements.build_audit_requirement_contract(),
            requirements.build_rollback_noop_requirement_contract(),
            requirements.build_ocel_visibility_contract(),
            requirements.build_mock_no_network_requirement_contract(),
            requirements.build_certification_requirement_contract(),
            prohibitions.build_provider_invocation_prohibition_contract(),
            prohibitions.build_command_execution_prohibition_contract(),
            findings,
            "passed",
            True,
            True,
            limitations=["v0.29.0 is contract-only; registry, mock harness, permission gates, credential/network boundaries, dry-run candidates, approval/audit/rollback, certification, and limited invocation remain future versions."],
            withdrawal_conditions=["Withdraw if adapter implementation, provider registration/invocation, provider SDK calls, network access, credential storage/logging/env creation, command execution expansion, RPA/A360/Brity/UiPath, external dominion, Schumpeter runtime, private/raw data exposure, reference dependency/code copy, PIG execution authority, or LLM sole authority appears."],
        )

    def build_all_parts(self, report_id: str | None = None) -> dict[str, Any]:
        report = self.build_report(report_id=report_id)
        return {
            "policy": report.track_policy,
            "source-view": report.source_view,
            "provider": report.provider_adapter_contract,
            "external-skill": report.external_skill_adapter_contract,
            "lifecycle": report.lifecycle_contract,
            "capability": report.capability_contract,
            "input-schema": report.input_schema_contract,
            "output-schema": report.output_schema_contract,
            "effects": report.effect_boundary_contract,
            "permission": report.permission_requirement_contract,
            "safety": report.safety_requirement_contract,
            "credentials": report.credential_requirement_contract,
            "network": report.network_requirement_contract,
            "audit": report.audit_requirement_contract,
            "rollback": report.rollback_noop_requirement_contract,
            "ocel": report.ocel_visibility_contract,
            "mock": report.mock_no_network_requirement_contract,
            "certification": report.certification_requirement_contract,
            "prohibit-provider-invocation": report.provider_invocation_prohibition_contract,
            "prohibit-command-execution": report.command_execution_prohibition_contract,
            "findings": report.findings,
            "report": report,
        }

    def build_pig_report(self) -> dict[str, Any]:
        report = self.build_report()
        return {
            "version": V0290_VERSION,
            "layer": V0290_LAYER,
            "subject": "external_provider_adapter_contract",
            "principles": [
                "Adapter contract is not adapter implementation",
                "Provider adapter contract is not provider invocation",
                "External skill contract is not external skill execution",
                "Capability declaration is not permission",
                "Provider registration is not execution",
                "Credential boundary is not credential storage",
                "Secret reference is not secret value",
                "Network boundary is not network access",
                "v0.29 contract readiness is not provider invocation readiness",
                "No-provider-invocation is the default outcome",
            ],
            "safety_boundary": {
                "adapter_implemented": report.adapter_implemented,
                "provider_registered": report.provider_registered,
                "provider_invoked": report.provider_invoked,
                "network_called": report.network_called,
                "command_executed": report.command_executed,
                "credential_stored": report.credential_stored,
                "credential_logged": report.credential_logged,
                "env_file_created": report.env_file_created,
                "RPA_adapter_implemented": report.RPA_adapter_implemented,
                "A360_adapter_implemented": report.A360_adapter_implemented,
                "Brity_adapter_implemented": report.Brity_adapter_implemented,
                "UiPath_adapter_implemented": report.UiPath_adapter_implemented,
                "external_dominion_implemented": report.external_dominion_implemented,
                "schumpeter_private_runtime_used": report.schumpeter_private_runtime_used,
                "actual_user_data_used": report.actual_user_data_used,
                "actual_company_data_used": report.actual_company_data_used,
                "private_material_exposed": report.private_material_exposed,
                "raw_provider_output_persisted": report.raw_provider_output_persisted,
                "references_runtime_dependency_added": report.references_runtime_dependency_added,
                "references_code_copied": report.references_code_copied,
                "PIG_execution_authority_enabled": report.PIG_execution_authority_enabled,
                "llm_judge_enabled": False,
            },
            "future_direction": [
                "v0.29.1 Provider Capability Inventory / Adapter Registry",
                "v0.29.2 Mock Adapter Harness / No-Network Default",
                "v0.29.3 Permission / Safety / Scope Gate for External Adapters",
                "v0.29.4 Credential / Secret / Network Boundary",
                "v0.29.5 Adapter Invocation Candidate / Dry-Run Plan",
                "v0.29.6 Provider Invocation Approval / Audit / Rollback Boundary",
                "v0.29.7 External Skill Packaging / Certification Matrix",
                "v0.29.8 Limited Provider Invocation Preview Gate",
                "v0.29.9 External Provider Adapter Foundation Consolidation",
            ],
            "next_step": V0290_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "external_provider_adapter_contract_created",
            "version": V0290_VERSION,
            "source_read_models": ["V028ConsolidationState", "V029ReadinessState", "ExternalAdapterContractHandoffState", "ExternalAdapterPreflightState", "ProviderInvocationReopenCriteriaState", "CommandExecutionReopenCriteriaState", "CredentialBoundaryPreflightState", "NetworkBoundaryPreflightState", "PermissionBoundaryPreflightState", "SafetyGatePreflightState", "AuditRollbackOCELPreflightState", "AdapterCertificationPreflightState", "PublicPrivateBoundaryState", "MemoryConsolidationState", "WorkbenchConsolidationState", "PigGuidanceState", "OCPXProjectionState"],
            "target_read_models": ["ExternalProviderAdapterContractState", "ExternalSkillAdapterContractState", "AdapterLifecycleContractState", "AdapterCapabilityContractState", "AdapterSchemaContractState", "AdapterEffectBoundaryContractState", "AdapterPermissionRequirementContractState", "AdapterSafetyRequirementContractState", "AdapterCredentialRequirementContractState", "AdapterNetworkRequirementContractState", "AdapterAuditRequirementContractState", "AdapterRollbackNoOpRequirementContractState", "AdapterOCELVisibilityContractState", "AdapterMockNoNetworkRequirementState", "AdapterCertificationRequirementState", "ProviderInvocationProhibitionState", "V029ReadinessState"],
            "effect_types": V0290_EFFECT_TYPES,
            "forbidden_effect_types": V0290_FORBIDDEN_EFFECT_TYPES,
        }


def render_external_adapter_contract_cli(parts: dict[str, Any], section: str = "report") -> str:
    report: ExternalAdapterContractReport = parts["report"]
    lines = [
        f"External Provider Adapter Contract {section}",
        f"version={report.version}",
        f"layer={report.track_policy.layer}",
        f"report_status={report.report_status}",
        f"ready_for_v0_29_1={_bool(report.ready_for_v0_29_1)}",
        f"ready_for_adapter_registry={_bool(report.ready_for_adapter_registry)}",
        f"ready_for_adapter_implementation={_bool(report.ready_for_adapter_implementation)}",
        f"ready_for_provider_registration={_bool(report.ready_for_provider_registration)}",
        f"ready_for_provider_invocation={_bool(report.ready_for_provider_invocation)}",
        f"ready_for_network_access={_bool(report.ready_for_network_access)}",
        f"ready_for_command_execution={_bool(report.ready_for_command_execution)}",
        f"adapter_implemented={_bool(report.adapter_implemented)}",
        f"provider_registered={_bool(report.provider_registered)}",
        f"provider_invoked={_bool(report.provider_invoked)}",
        f"network_called={_bool(report.network_called)}",
        f"command_executed={_bool(report.command_executed)}",
        f"credential_stored={_bool(report.credential_stored)}",
        f"credential_logged={_bool(report.credential_logged)}",
        f"env_file_created={_bool(report.env_file_created)}",
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
        f"references_runtime_dependency_added={_bool(report.references_runtime_dependency_added)}",
        f"references_code_copied={_bool(report.references_code_copied)}",
        f"PIG_execution_authority_enabled={_bool(report.PIG_execution_authority_enabled)}",
        f"llm_judge_used={_bool(report.llm_judge_used)}",
        f"next_required_step={report.next_required_step}",
    ]
    payload = parts.get(section)
    if payload is not None and payload is not report:
        lines.append(f"section_object={payload.__class__.__name__}")
    return "\n".join(lines)
