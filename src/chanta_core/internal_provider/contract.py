from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import time
from typing import Any


INTERNAL_PROVIDER_VERSION = "v0.24.0"
INTERNAL_PROVIDER_VERSION_NAME = "Internal Provider Contract"
INTERNAL_PROVIDER_KOREAN_NAME = "internal provider contract"
INTERNAL_PROVIDER_LAYER = "internal_provider"
INTERNAL_PROVIDER_TRACK = "Internal Provider / Local Runtime Provider"
INTERNAL_PROVIDER_STATUS = "contract_only"
INTERNAL_PROVIDER_STATE = "internal_provider_contract_declared"
INTERNAL_PROVIDER_NEXT_STEP = "v0.24.1 Provider Registry & Capability Surface"

INTERNAL_PROVIDER_ALLOWED_EFFECT_TYPES = [
    "read_only_observation",
    "state_candidate_created",
    "provider_contract_declared",
]

INTERNAL_PROVIDER_FUTURE_EFFECT_TYPES = [
    "provider_surface_declared",
    "provider_candidate_created",
    "workspace_tree_observed",
    "repository_search_performed",
    "file_excerpt_read",
    "process_state_inspected",
    "local_command_candidate_created",
    "local_runtime_static_safety_checked",
    "local_runtime_preflight_checked",
    "bounded_local_command_executed",
    "local_output_captured",
    "local_runtime_outcome_candidate_created",
]

INTERNAL_PROVIDER_FORBIDDEN_EFFECT_TYPES = [
    "provider_invoked",
    "workspace_file_read_executed",
    "repository_search_executed",
    "file_content_extracted",
    "local_command_executed",
    "bounded_local_command_executed",
    "unrestricted_shell_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "raw_secret_output",
    "memory_mutated",
    "persona_mutated",
    "external_provider_called",
]

INTERNAL_PROVIDER_OCEL_OBJECT_TYPES = [
    "internal_provider_contract",
    "internal_provider_type_descriptor",
    "internal_provider_capability_contract",
    "internal_provider_effect_policy",
    "internal_provider_permission_policy",
    "internal_provider_invocation_boundary",
    "internal_provider_observability_contract",
    "internal_provider_safety_boundary",
    "internal_provider_roadmap_boundary",
    "internal_provider_contract_finding",
    "internal_provider_contract_report",
    "internal_dominion_consolidation_report",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]

INTERNAL_PROVIDER_OCEL_EVENT_TYPES = [
    "internal_provider_contract_requested",
    "internal_provider_type_descriptors_created",
    "internal_provider_effect_policy_created",
    "internal_provider_permission_policy_created",
    "internal_provider_invocation_boundary_created",
    "internal_provider_observability_contract_created",
    "internal_provider_safety_boundary_created",
    "internal_provider_roadmap_boundary_created",
    "internal_provider_contract_report_created",
    "internal_provider_contract_blocked",
]

INTERNAL_PROVIDER_OCEL_RELATION_TYPES = [
    "declares_internal_provider_contract",
    "declares_internal_provider_type",
    "declares_internal_provider_capability_contract",
    "declares_internal_provider_effect_policy",
    "declares_internal_provider_permission_policy",
    "declares_internal_provider_invocation_boundary",
    "declares_internal_provider_observability_contract",
    "declares_internal_provider_safety_boundary",
    "declares_internal_provider_roadmap_boundary",
    "prepares_provider_registry",
    "prepares_workspace_read_provider",
    "prepares_repository_search_provider",
    "prepares_ocel_inspection_provider",
    "prepares_local_runtime_provider",
    "defers_provider_invocation_to_later_v0_24",
    "defers_local_runtime_execution_to_later_v0_24",
    "defers_general_agent_usability_to_v0_25",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_schumpeter_split_to_v0_28",
    "defers_external_provider_adapters_to_v0_29_plus",
    "not_provider_invoked",
    "not_local_command_executed",
    "not_external_runtime_touched",
    "not_external_provider_called",
    "prevents_credential_exposure",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_internal_dominion_consolidation",
]

INTERNAL_PROVIDER_SKILL_IDS = [
    "skill:internal_provider_contract_view",
    "skill:internal_provider_registry_view",
    "skill:internal_provider_capability_surface_view",
    "skill:workspace_read_provider_view",
    "skill:repository_search_provider_view",
    "skill:file_read_provider_view",
    "skill:ocel_inspection_provider_view",
    "skill:pig_inspection_provider_view",
    "skill:ocpx_projection_provider_view",
    "skill:local_runtime_command_candidate_create",
    "skill:local_runtime_static_safety_check",
    "skill:local_runtime_preflight_check",
    "skill:local_runtime_execution_gate",
    "skill:bounded_local_command_run",
    "skill:local_runtime_output_summarize",
    "skill:local_runtime_failure_explain",
    "skill:internal_provider_consolidation_view",
]

INTERNAL_PROVIDER_TYPES = [
    "workspace_read_provider",
    "repository_search_provider",
    "file_read_provider",
    "ocel_inspection_provider",
    "pig_inspection_provider",
    "ocpx_projection_provider",
    "local_runtime_provider",
    "diagnostic_provider",
    "candidate_generation_provider",
    "unknown",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class InternalProviderTypeDescriptor:
    provider_type_id: str
    provider_type: str
    description: str
    introduced_in: str = INTERNAL_PROVIDER_VERSION
    implementation_status: str = "contract_only"
    read_only_default: bool = True
    execution_capable_future: bool = False
    external_adapter: bool = False
    provider_api_call_required: bool = False
    external_runtime_touch_required: bool = False
    credential_materialization_required: bool = False
    allowed_effect_types: list[str] = field(default_factory=lambda: list(INTERNAL_PROVIDER_ALLOWED_EFFECT_TYPES))
    forbidden_effect_types: list[str] = field(default_factory=lambda: list(INTERNAL_PROVIDER_FORBIDDEN_EFFECT_TYPES))
    future_versions: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderCapabilityContract:
    contract_id: str
    capability_id_required: bool = True
    provider_type_required: bool = True
    input_schema_required: bool = True
    output_schema_required: bool = True
    effect_type_required: bool = True
    permission_policy_required: bool = True
    ocel_mapping_required: bool = True
    pig_projection_required: bool = True
    ocpx_projection_required: bool = True
    safety_boundary_required: bool = True
    failure_explanation_required: bool = True
    raw_secret_output_forbidden: bool = True
    private_path_sanitization_required: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderEffectPolicy:
    policy_id: str
    allowed_effect_types_v0_24_0: list[str]
    future_effect_types: list[str]
    forbidden_effect_types_v0_24_0: list[str]
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderPermissionPolicy:
    policy_id: str
    deny_by_default: bool = True
    read_only_requires_policy: bool = True
    candidate_creation_requires_policy: bool = True
    execution_requires_gate: bool = True
    local_runtime_execution_requires_allowlist: bool = True
    local_runtime_execution_requires_timeout: bool = True
    local_runtime_execution_requires_output_cap: bool = True
    local_runtime_execution_requires_redaction: bool = True
    local_runtime_execution_requires_side_effect_scan: bool = True
    network_forbidden_by_default: bool = True
    package_install_forbidden_by_default: bool = True
    destructive_command_forbidden_by_default: bool = True
    credential_access_forbidden_by_default: bool = True
    secret_output_forbidden: bool = True
    private_path_sanitization_required: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderInvocationBoundary:
    boundary_id: str
    invocation_enabled_v0_24_0: bool = False
    workspace_read_execution_enabled_v0_24_0: bool = False
    repository_search_execution_enabled_v0_24_0: bool = False
    file_read_execution_enabled_v0_24_0: bool = False
    ocel_inspection_execution_enabled_v0_24_0: bool = False
    local_runtime_execution_enabled_v0_24_0: bool = False
    local_command_execution_enabled_v0_24_0: bool = False
    external_provider_invocation_enabled: bool = False
    shell_execution_enabled: bool = False
    network_enabled: bool = False
    mcp_enabled: bool = False
    plugin_enabled: bool = False
    llm_judge_enabled: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderObservabilityContract:
    contract_id: str
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    execution_envelope_visible: bool = True
    provider_invocation_must_emit_event: bool = True
    provider_invocation_must_record_effect_type: bool = True
    provider_result_must_be_sanitized: bool = True
    provider_failure_must_be_explainable: bool = True
    raw_secret_output_forbidden: bool = True
    private_path_sanitization_required: bool = True
    workbench_visible_future: bool = True
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderSafetyBoundary:
    boundary_id: str
    provider_invocation_count: int = 0
    workspace_file_read_execution_count: int = 0
    repository_search_execution_count: int = 0
    file_content_extraction_count: int = 0
    local_command_execution_count: int = 0
    bounded_local_command_execution_count: int = 0
    unrestricted_shell_count: int = 0
    provider_api_call_count: int = 0
    external_runtime_touch_count: int = 0
    external_dispatch_count: int = 0
    network_access_count: int = 0
    package_install_count: int = 0
    destructive_command_count: int = 0
    credential_exposure_count: int = 0
    raw_secret_output_count: int = 0
    llm_judge_count: int = 0
    external_provider_adapter_count: int = 0
    schumpeter_split_count: int = 0
    status: str = "passed"
    findings: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderRoadmapBoundary:
    boundary_id: str
    current_track: str = "v0.24.x Internal Provider / Local Runtime Provider"
    current_version_scope: str = "v0.24.0 contract_only"
    next_version: str = INTERNAL_PROVIDER_NEXT_STEP
    general_agent_usability_deferred_to: str = "v0.25.x"
    workspace_workbench_deferred_to: str = "v0.26.x"
    memory_continuity_deferred_to: str = "v0.27.x"
    schumpeter_split_deferred_to: str = "v0.28.x"
    external_provider_adapters_deferred_to: str = "v0.29.x+"
    growthkernel_bridge_deferred: bool = True
    roadmap_status: str = "aligned"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderContract:
    contract_id: str
    definition: str
    provider_types: list[InternalProviderTypeDescriptor]
    capability_contract: InternalProviderCapabilityContract
    effect_policy: InternalProviderEffectPolicy
    permission_policy: InternalProviderPermissionPolicy
    invocation_boundary: InternalProviderInvocationBoundary
    observability_contract: InternalProviderObservabilityContract
    safety_boundary: InternalProviderSafetyBoundary
    roadmap_boundary: InternalProviderRoadmapBoundary
    version: str = INTERNAL_PROVIDER_VERSION
    layer: str = INTERNAL_PROVIDER_LAYER
    release_track: str = INTERNAL_PROVIDER_TRACK
    status: str = INTERNAL_PROVIDER_STATUS
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "provider_types": [item.to_dict() for item in self.provider_types],
            "capability_contract": self.capability_contract.to_dict(),
            "effect_policy": self.effect_policy.to_dict(),
            "permission_policy": self.permission_policy.to_dict(),
            "invocation_boundary": self.invocation_boundary.to_dict(),
            "observability_contract": self.observability_contract.to_dict(),
            "safety_boundary": self.safety_boundary.to_dict(),
            "roadmap_boundary": self.roadmap_boundary.to_dict(),
        }


@dataclass(frozen=True)
class InternalProviderContractFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalProviderContractReport:
    report_id: str
    created_at: str
    contract: InternalProviderContract
    findings: list[InternalProviderContractFinding]
    report_status: str
    ready_for_v0_24_1: bool
    version: str = INTERNAL_PROVIDER_VERSION
    ready_for_v0_25: bool = False
    provider_invocation_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    local_command_execution_enabled: bool = False
    workspace_read_execution_enabled: bool = False
    repository_search_execution_enabled: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = INTERNAL_PROVIDER_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until provider registry implementation begins or internal provider policy changes."

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "contract": self.contract.to_dict(),
            "findings": [item.to_dict() for item in self.findings],
        }


class InternalProviderSkillRegistryService:
    def list_skill_contracts(self) -> list[dict[str, Any]]:
        return [
            {
                "skill_id": skill_id,
                "status": "contract_only",
                "implemented": skill_id == "skill:internal_provider_contract_view",
                "stub": skill_id != "skill:internal_provider_contract_view",
                "read_only": True,
                "contract_only": True,
                "provider_invocation_enabled": False,
                "workspace_read_execution_enabled": False,
                "repository_search_execution_enabled": False,
                "file_read_execution_enabled": False,
                "local_runtime_execution_enabled": False,
                "local_command_execution_enabled": False,
                "external_provider_adapter_enabled": False,
                "llm_judge_enabled": False,
            }
            for skill_id in INTERNAL_PROVIDER_SKILL_IDS
        ]


class InternalProviderTypeRegistryService:
    def list_provider_types(self) -> list[InternalProviderTypeDescriptor]:
        descriptions = {
            "workspace_read_provider": "Contract descriptor for future policy-governed workspace read surfaces.",
            "repository_search_provider": "Contract descriptor for future policy-governed repository search surfaces.",
            "file_read_provider": "Contract descriptor for future policy-governed file excerpt surfaces.",
            "ocel_inspection_provider": "Contract descriptor for future OCEL inspection surfaces.",
            "pig_inspection_provider": "Contract descriptor for future PIG inspection surfaces.",
            "ocpx_projection_provider": "Contract descriptor for future OCPX projection surfaces.",
            "local_runtime_provider": "Contract descriptor for future bounded local runtime surfaces.",
            "diagnostic_provider": "Contract descriptor for future diagnostic provider surfaces.",
            "candidate_generation_provider": "Contract descriptor for future provider candidate generation surfaces.",
            "unknown": "Fallback contract descriptor for unresolved provider types.",
        }
        return [
            InternalProviderTypeDescriptor(
                provider_type_id=f"internal_provider_type:{provider_type}",
                provider_type=provider_type,
                description=descriptions[provider_type],
                implementation_status="contract_only" if provider_type != "unknown" else "future_track",
                read_only_default=provider_type != "local_runtime_provider",
                execution_capable_future=provider_type == "local_runtime_provider",
                future_versions=["v0.24.1+"] if provider_type != "unknown" else ["future_track"],
                notes=[
                    "provider_is_not_external_adapter",
                    "provider_invocation_disabled_in_v0_24_0",
                    "local_runtime_provider_is_not_unrestricted_shell",
                ],
            )
            for provider_type in INTERNAL_PROVIDER_TYPES
        ]


class InternalProviderEffectPolicyService:
    def build_effect_policy(self) -> InternalProviderEffectPolicy:
        return InternalProviderEffectPolicy(
            policy_id="internal_provider_effect_policy:v0.24.0",
            allowed_effect_types_v0_24_0=list(INTERNAL_PROVIDER_ALLOWED_EFFECT_TYPES),
            future_effect_types=list(INTERNAL_PROVIDER_FUTURE_EFFECT_TYPES),
            forbidden_effect_types_v0_24_0=list(INTERNAL_PROVIDER_FORBIDDEN_EFFECT_TYPES),
            notes=["provider_invocation_must_be_gated_by_effect_type"],
        )


class InternalProviderPermissionPolicyService:
    def build_permission_policy(self) -> InternalProviderPermissionPolicy:
        return InternalProviderPermissionPolicy(
            policy_id="internal_provider_permission_policy:v0.24.0",
            notes=[
                "deny_by_default",
                "read_only_requires_policy",
                "local_runtime_future_execution_requires_allowlist_timeout_output_cap_redaction_side_effect_scan",
            ],
        )


class InternalProviderInvocationBoundaryService:
    def build_invocation_boundary(self) -> InternalProviderInvocationBoundary:
        return InternalProviderInvocationBoundary(
            boundary_id="internal_provider_invocation_boundary:v0.24.0",
            notes=[
                "v0_24_0_contract_only",
                "no_provider_invocation",
                "no_workspace_repo_file_read_execution",
                "no_local_command_execution",
            ],
        )


class InternalProviderObservabilityContractService:
    def build_observability_contract(self) -> InternalProviderObservabilityContract:
        return InternalProviderObservabilityContract(
            contract_id="internal_provider_observability_contract:v0.24.0",
            notes=[
                "ocel_pig_ocpx_visible",
                "provider_results_must_be_sanitized",
                "provider_failures_must_be_explainable",
            ],
        )


class InternalProviderSafetyBoundaryService:
    _COUNT_MARKERS = {
        "provider_invocation": "provider_invocation_count",
        "workspace_file_read_execution": "workspace_file_read_execution_count",
        "repository_search_execution": "repository_search_execution_count",
        "file_content_extraction": "file_content_extraction_count",
        "local_command_execution": "local_command_execution_count",
        "bounded_local_command_execution": "bounded_local_command_execution_count",
        "unrestricted_shell": "unrestricted_shell_count",
        "provider_api_call": "provider_api_call_count",
        "external_runtime_touch": "external_runtime_touch_count",
        "external_dispatch": "external_dispatch_count",
        "network_access": "network_access_count",
        "package_install": "package_install_count",
        "destructive_command": "destructive_command_count",
        "credential_exposure": "credential_exposure_count",
        "raw_secret_output": "raw_secret_output_count",
        "llm_judge": "llm_judge_count",
        "external_provider_adapter": "external_provider_adapter_count",
        "schumpeter_split": "schumpeter_split_count",
    }

    def build_safety_boundary(self, markers: list[str] | None = None) -> InternalProviderSafetyBoundary:
        marker_set = set(markers or [])
        counts = {field_name: 0 for field_name in self._COUNT_MARKERS.values()}
        findings: list[dict[str, Any]] = []
        for marker, field_name in self._COUNT_MARKERS.items():
            if marker in marker_set:
                counts[field_name] = 1
                findings.append(
                    {
                        "finding_type": f"{marker}_detected",
                        "severity": "critical",
                        "message": f"Detected forbidden v0.24.0 internal provider marker: {marker}",
                    }
                )
        blocked = any(counts.values())
        return InternalProviderSafetyBoundary(
            boundary_id="internal_provider_safety_boundary:v0.24.0",
            status="blocked" if blocked else "passed",
            findings=findings,
            **counts,
        )


class InternalProviderRoadmapBoundaryService:
    def build_roadmap_boundary(self, markers: list[str] | None = None) -> InternalProviderRoadmapBoundary:
        marker_set = set(markers or [])
        blocked = bool(
            {
                "general_agent_usability",
                "workspace_workbench",
                "memory_continuity",
                "external_provider_adapter",
                "schumpeter_split",
            }
            & marker_set
        )
        return InternalProviderRoadmapBoundary(
            boundary_id="internal_provider_roadmap_boundary:v0.24.0",
            roadmap_status="blocked" if blocked else "aligned",
            notes=[
                "v0_24_0_contract_only",
                "v0_25_general_agent_usability_deferred",
                "v0_29_external_provider_adapters_deferred",
            ],
        )


class InternalProviderContractFindingService:
    def build_findings(self, contract: InternalProviderContract) -> list[InternalProviderContractFinding]:
        findings: list[InternalProviderContractFinding] = []
        if not contract.provider_types:
            findings.append(_finding("critical", "provider_type_missing", "Provider types are missing."))
        if not contract.effect_policy:
            findings.append(_finding("critical", "effect_policy_missing", "Effect policy is missing."))
        if not contract.permission_policy:
            findings.append(_finding("critical", "permission_policy_missing", "Permission policy is missing."))
        if not contract.observability_contract:
            findings.append(
                _finding("critical", "observability_contract_missing", "Observability contract is missing.")
            )
        boundary = contract.invocation_boundary
        if boundary.invocation_enabled_v0_24_0:
            findings.append(
                _finding("critical", "provider_invocation_enabled_too_early", "Provider invocation is enabled.")
            )
        if boundary.workspace_read_execution_enabled_v0_24_0:
            findings.append(
                _finding(
                    "critical",
                    "workspace_read_execution_enabled_too_early",
                    "Workspace read execution is enabled.",
                )
            )
        if boundary.repository_search_execution_enabled_v0_24_0:
            findings.append(
                _finding(
                    "critical",
                    "repository_search_execution_enabled_too_early",
                    "Repository search execution is enabled.",
                )
            )
        if boundary.local_runtime_execution_enabled_v0_24_0:
            findings.append(
                _finding(
                    "critical",
                    "local_runtime_execution_enabled_too_early",
                    "Local runtime execution is enabled.",
                )
            )
        if boundary.local_command_execution_enabled_v0_24_0:
            findings.append(
                _finding(
                    "critical",
                    "local_command_execution_enabled_too_early",
                    "Local command execution is enabled.",
                )
            )
        if boundary.shell_execution_enabled:
            findings.append(_finding("critical", "unrestricted_shell_enabled", "Shell execution is enabled."))
        if boundary.network_enabled:
            findings.append(_finding("critical", "network_enabled", "Network access is enabled."))
        safety = contract.safety_boundary
        safety_payload = safety.to_dict()
        safety_findings = {
            "credential_exposure_count": "credential_exposure_detected",
            "raw_secret_output_count": "raw_secret_output_detected",
            "external_provider_adapter_count": "external_provider_adapter_detected",
            "schumpeter_split_count": "schumpeter_split_detected",
            "llm_judge_count": "llm_judge_detected",
            "network_access_count": "network_enabled",
            "package_install_count": "package_install_enabled",
            "destructive_command_count": "destructive_command_enabled",
        }
        for count_field, finding_type in safety_findings.items():
            if int(safety_payload.get(count_field, 0)) > 0:
                findings.append(
                    _finding("critical", finding_type, f"Safety boundary count is nonzero: {count_field}")
                )
        for count_field, value in safety_payload.items():
            if count_field.endswith("_count") and int(value or 0) > 0 and all(
                count_field not in item.message for item in findings
            ):
                findings.append(
                    _finding(
                        "critical",
                        "provider_invocation_enabled_too_early",
                        f"Safety boundary count is nonzero: {count_field}",
                    )
                )
        if contract.roadmap_boundary.roadmap_status == "blocked":
            findings.append(
                _finding(
                    "critical",
                    "general_agent_usability_premature",
                    "Roadmap boundary detected premature future-track implementation.",
                )
            )
        if not findings:
            findings.append(_finding("info", "ok", "Internal Provider Contract is contract-only and non-executing."))
        return findings


class InternalProviderContractService:
    def __init__(
        self,
        type_registry: InternalProviderTypeRegistryService | None = None,
        effect_policy_service: InternalProviderEffectPolicyService | None = None,
        permission_policy_service: InternalProviderPermissionPolicyService | None = None,
        invocation_boundary_service: InternalProviderInvocationBoundaryService | None = None,
        observability_service: InternalProviderObservabilityContractService | None = None,
        safety_service: InternalProviderSafetyBoundaryService | None = None,
        roadmap_service: InternalProviderRoadmapBoundaryService | None = None,
    ) -> None:
        self.type_registry = type_registry or InternalProviderTypeRegistryService()
        self.effect_policy_service = effect_policy_service or InternalProviderEffectPolicyService()
        self.permission_policy_service = permission_policy_service or InternalProviderPermissionPolicyService()
        self.invocation_boundary_service = invocation_boundary_service or InternalProviderInvocationBoundaryService()
        self.observability_service = observability_service or InternalProviderObservabilityContractService()
        self.safety_service = safety_service or InternalProviderSafetyBoundaryService()
        self.roadmap_service = roadmap_service or InternalProviderRoadmapBoundaryService()

    def build_contract(self, markers: list[str] | None = None) -> InternalProviderContract:
        return InternalProviderContract(
            contract_id="internal_provider_contract:v0.24.0",
            definition=(
                "Internal provider is a public-core-safe, OCEL-visible internal capability surface. "
                "v0.24.0 declares contracts only and does not invoke providers, read files, search "
                "repositories, execute local commands, or call external provider APIs."
            ),
            provider_types=self.type_registry.list_provider_types(),
            capability_contract=InternalProviderCapabilityContract(
                contract_id="internal_provider_capability_contract:v0.24.0",
                notes=["capability_surfaces_are_declared_not_invoked"],
            ),
            effect_policy=self.effect_policy_service.build_effect_policy(),
            permission_policy=self.permission_policy_service.build_permission_policy(),
            invocation_boundary=self.invocation_boundary_service.build_invocation_boundary(),
            observability_contract=self.observability_service.build_observability_contract(),
            safety_boundary=self.safety_service.build_safety_boundary(markers),
            roadmap_boundary=self.roadmap_service.build_roadmap_boundary(markers),
            notes=[
                "provider_is_not_arbitrary_tool_execution",
                "provider_is_not_external_adapter",
                "provider_is_not_agent_ux",
                "local_runtime_provider_is_not_unrestricted_shell",
            ],
        )

    def view_contract(self) -> InternalProviderContract:
        return self.build_contract()


class InternalProviderContractReportService:
    def __init__(
        self,
        contract_service: InternalProviderContractService | None = None,
        finding_service: InternalProviderContractFindingService | None = None,
    ) -> None:
        self.contract_service = contract_service or InternalProviderContractService()
        self.finding_service = finding_service or InternalProviderContractFindingService()

    def build_report(self, markers: list[str] | None = None) -> InternalProviderContractReport:
        contract = self.contract_service.build_contract(markers)
        findings = self.finding_service.build_findings(contract)
        blocked = any(item.severity == "critical" for item in findings)
        return InternalProviderContractReport(
            report_id="internal_provider_contract_report:v0.24.0",
            created_at=_utc_now(),
            contract=contract,
            findings=findings,
            report_status="blocked" if blocked else "passed",
            ready_for_v0_24_1=not blocked,
            limitations=[
                "v0.24.0 is contract-only.",
                "Provider invocation, workspace/repo/file read execution, and local command execution are disabled.",
            ],
            withdrawal_conditions=[
                "Provider invocation or local command execution becomes enabled.",
                "Credential exposure, raw secret output, external adapter logic, or Schumpeter split is introduced.",
                "A future-track implementation leaks into v0.24.0 contract-only scope.",
            ],
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": INTERNAL_PROVIDER_VERSION,
            "layer": INTERNAL_PROVIDER_LAYER,
            "subject": "internal_provider_contract",
            "principles": [
                "provider is not arbitrary tool execution",
                "provider is not external adapter",
                "provider is not agent UX",
                "provider is an OCEL-visible internal capability surface",
                "provider invocation must be gated by effect type",
                "local runtime provider is not unrestricted shell",
            ],
            "safety_boundary": {
                "provider_invocation_enabled": False,
                "workspace_read_execution_enabled": False,
                "repository_search_execution_enabled": False,
                "file_read_execution_enabled": False,
                "local_runtime_execution_enabled": False,
                "local_command_execution_enabled": False,
                "external_provider_adapter_implemented": False,
                "unrestricted_shell_enabled": False,
                "network_enabled": False,
                "package_install_enabled": False,
                "destructive_command_enabled": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": INTERNAL_PROVIDER_NEXT_STEP,
            "roadmap": {
                "v0.24": "Internal Provider / Local Runtime Provider",
                "v0.25": "General Agent Usability & Tool Routing",
                "v0.26": "Workspace Agent Workbench",
                "v0.27": "Memory Candidate & Continuity",
                "v0.28": "Public Alpha / Schumpeter Split Preparation",
                "v0.29+": "External Skill / External Provider Adapters",
            },
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": INTERNAL_PROVIDER_STATE,
            "version": INTERNAL_PROVIDER_VERSION,
            "source_read_models": [
                "InternalDominionConsolidationState",
                "InternalDominionReleaseState",
                "V024ReadinessState",
            ],
            "target_read_models": [
                "InternalProviderContractState",
                "InternalProviderTypeState",
                "InternalProviderEffectPolicyState",
                "InternalProviderPermissionPolicyState",
                "InternalProviderInvocationBoundaryState",
                "InternalProviderRoadmapBoundaryState",
            ],
            "effect_types": list(INTERNAL_PROVIDER_ALLOWED_EFFECT_TYPES),
        }

    def render_report_cli(self, report: InternalProviderContractReport, section: str = "contract") -> str:
        common = [
            f"version={report.version}",
            f"layer={report.contract.layer}",
            f"status={report.contract.status}",
            f"provider_invocation_enabled={report.provider_invocation_enabled}",
            f"workspace_read_execution_enabled={report.workspace_read_execution_enabled}",
            f"repository_search_execution_enabled={report.repository_search_execution_enabled}",
            f"local_runtime_execution_enabled={report.local_runtime_execution_enabled}",
            f"local_command_execution_enabled={report.local_command_execution_enabled}",
            f"external_provider_adapter_implemented={report.external_provider_adapter_implemented}",
            f"schumpeter_split_introduced={report.schumpeter_split_introduced}",
            f"ready_for_v0_24_1={report.ready_for_v0_24_1}",
            f"ready_for_v0_25={report.ready_for_v0_25}",
            f"next_required_step={report.next_required_step}",
        ]
        if section == "types":
            type_list = ",".join(item.provider_type for item in report.contract.provider_types)
            return "\n".join(["Internal Provider Types", f"provider_types={type_list}"] + common)
        if section == "effect-policy":
            policy = report.contract.effect_policy
            return "\n".join(
                [
                    "Internal Provider Effect Policy",
                    f"allowed_effect_types_v0_24_0={','.join(policy.allowed_effect_types_v0_24_0)}",
                    f"forbidden_effect_type_count={len(policy.forbidden_effect_types_v0_24_0)}",
                ]
                + common
            )
        if section == "permission-policy":
            policy = report.contract.permission_policy
            return "\n".join(
                [
                    "Internal Provider Permission Policy",
                    f"deny_by_default={policy.deny_by_default}",
                    f"read_only_requires_policy={policy.read_only_requires_policy}",
                    f"execution_requires_gate={policy.execution_requires_gate}",
                ]
                + common
            )
        if section == "invocation-boundary":
            boundary = report.contract.invocation_boundary
            return "\n".join(
                [
                    "Internal Provider Invocation Boundary",
                    f"invocation_enabled_v0_24_0={boundary.invocation_enabled_v0_24_0}",
                    f"workspace_read_execution_enabled_v0_24_0={boundary.workspace_read_execution_enabled_v0_24_0}",
                    f"repository_search_execution_enabled_v0_24_0={boundary.repository_search_execution_enabled_v0_24_0}",
                    f"local_command_execution_enabled_v0_24_0={boundary.local_command_execution_enabled_v0_24_0}",
                ]
                + common
            )
        if section == "observability":
            contract = report.contract.observability_contract
            return "\n".join(
                [
                    "Internal Provider Observability Contract",
                    f"ocel_visible={contract.ocel_visible}",
                    f"pig_visible={contract.pig_visible}",
                    f"ocpx_visible={contract.ocpx_visible}",
                    f"provider_result_must_be_sanitized={contract.provider_result_must_be_sanitized}",
                ]
                + common
            )
        if section == "safety-boundary":
            boundary = report.contract.safety_boundary
            return "\n".join(
                [
                    "Internal Provider Safety Boundary",
                    f"provider_invocation_count={boundary.provider_invocation_count}",
                    f"workspace_file_read_execution_count={boundary.workspace_file_read_execution_count}",
                    f"repository_search_execution_count={boundary.repository_search_execution_count}",
                    f"local_command_execution_count={boundary.local_command_execution_count}",
                    f"network_access_count={boundary.network_access_count}",
                    f"status={boundary.status}",
                ]
                + common
            )
        if section == "roadmap-boundary":
            boundary = report.contract.roadmap_boundary
            return "\n".join(
                [
                    "Internal Provider Roadmap Boundary",
                    f"current_track={boundary.current_track}",
                    f"current_version_scope={boundary.current_version_scope}",
                    f"next_version={boundary.next_version}",
                    f"roadmap_status={boundary.roadmap_status}",
                ]
                + common
            )
        return "\n".join(
            [
                "Internal Provider Contract",
                f"version_name={INTERNAL_PROVIDER_VERSION_NAME}",
                f"release_track={report.contract.release_track}",
                f"report_status={report.report_status}",
            ]
            + common
        )


class InternalProviderContractViewService(InternalProviderContractReportService):
    def view_contract(self) -> InternalProviderContract:
        return self.contract_service.view_contract()


def _finding(severity: str, finding_type: str, message: str) -> InternalProviderContractFinding:
    return InternalProviderContractFinding(
        finding_id=f"internal_provider_contract_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        subject_ref=None,
        evidence_refs=[],
        withdrawal_condition="Withdraw if the contract-only boundary no longer holds.",
    )
