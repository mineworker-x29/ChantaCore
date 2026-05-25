from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import time
from typing import Any

from chanta_core.internal_provider.contract import (
    INTERNAL_PROVIDER_FORBIDDEN_EFFECT_TYPES,
    INTERNAL_PROVIDER_LAYER,
    INTERNAL_PROVIDER_TRACK,
    INTERNAL_PROVIDER_TYPES,
    InternalProviderContract,
    InternalProviderContractReportService,
)


INTERNAL_PROVIDER_REGISTRY_VERSION = "v0.24.1"
INTERNAL_PROVIDER_REGISTRY_VERSION_NAME = "Provider Registry & Capability Surface"
INTERNAL_PROVIDER_REGISTRY_KOREAN_NAME = "Provider 레지스트리·Capability 표면"
INTERNAL_PROVIDER_REGISTRY_STATE = "internal_provider_registry_declared"
INTERNAL_PROVIDER_REGISTRY_NEXT_STEP = "v0.24.2 Read-only Workspace Provider"
INTERNAL_PROVIDER_REGISTRY_ALLOWED_EFFECT_TYPES = [
    "read_only_observation",
    "state_candidate_created",
    "provider_surface_declared",
]
INTERNAL_PROVIDER_REGISTRY_FORBIDDEN_EFFECT_TYPES = [
    "provider_invoked",
    "workspace_file_read_executed",
    "repository_search_executed",
    "file_content_extracted",
    "file_excerpt_read",
    "local_command_candidate_created",
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
    "external_provider_called",
]
INTERNAL_PROVIDER_REGISTRY_OCEL_OBJECT_TYPES = [
    "internal_provider_registration_request",
    "internal_provider_ref",
    "internal_provider_capability_descriptor",
    "internal_provider_capability_surface",
    "internal_provider_status",
    "internal_provider_registry",
    "internal_provider_registry_snapshot",
    "internal_provider_registry_finding",
    "internal_provider_registry_report",
    "internal_provider_capability_surface_report",
    "internal_provider_contract",
    "execution_envelope",
    "pig_report",
    "ocpx_projection",
]
INTERNAL_PROVIDER_REGISTRY_OCEL_EVENT_TYPES = [
    "internal_provider_registration_requested",
    "internal_provider_contract_loaded",
    "internal_provider_ref_registered",
    "internal_provider_capability_descriptor_registered",
    "internal_provider_capability_surface_created",
    "internal_provider_status_created",
    "internal_provider_registry_created",
    "internal_provider_registry_snapshot_created",
    "internal_provider_registry_report_created",
    "internal_provider_capability_surface_report_created",
    "internal_provider_registry_blocked",
]
INTERNAL_PROVIDER_REGISTRY_OCEL_RELATION_TYPES = [
    "registers_internal_provider",
    "declares_provider_capability_surface",
    "declares_provider_capability_descriptor",
    "assigns_provider_status",
    "prepares_workspace_read_provider",
    "prepares_repository_search_provider",
    "prepares_file_read_provider",
    "prepares_ocel_inspection_provider",
    "prepares_pig_inspection_provider",
    "prepares_ocpx_projection_provider",
    "prepares_local_runtime_provider",
    "prepares_diagnostic_provider",
    "prepares_candidate_generation_provider",
    "defers_provider_invocation_to_later_v0_24",
    "defers_workspace_read_execution_to_v0_24_2",
    "defers_repository_search_execution_to_v0_24_3",
    "defers_file_read_execution_to_v0_24_3",
    "defers_process_state_inspection_execution_to_v0_24_4",
    "defers_local_runtime_candidate_to_v0_24_5",
    "defers_local_runtime_execution_to_later_v0_24",
    "defers_general_agent_usability_to_v0_25",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_schumpeter_split_to_v0_28",
    "defers_external_provider_adapters_to_v0_29_plus",
    "not_provider_invoked",
    "not_workspace_file_read",
    "not_repository_searched",
    "not_file_content_extracted",
    "not_local_command_executed",
    "not_external_runtime_touched",
    "not_external_provider_called",
    "prevents_credential_exposure",
    "visible_in_workbench_future",
    "recorded_in_envelope",
    "derived_from_internal_provider_contract",
]


@dataclass
class InternalProviderRegistrationRequest:
    requested_provider_types: list[str] = field(default_factory=list)
    include_workspace_read_provider: bool = True
    include_repository_search_provider: bool = True
    include_file_read_provider: bool = True
    include_ocel_inspection_provider: bool = True
    include_pig_inspection_provider: bool = True
    include_ocpx_projection_provider: bool = True
    include_local_runtime_provider: bool = True
    include_diagnostic_provider: bool = True
    include_candidate_generation_provider: bool = True
    source_refs: list[dict[str, Any]] = field(default_factory=list)
    strictness: str = "standard"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderRef:
    provider_id: str
    provider_type: str
    provider_name: str
    description: str
    introduced_in: str = INTERNAL_PROVIDER_REGISTRY_VERSION
    implementation_status: str = "declared"
    activation_version: str | None = None
    read_only_default: bool = True
    execution_capable_future: bool = False
    provider_invocation_enabled: bool = False
    provider_api_call_enabled: bool = False
    external_runtime_touch_enabled: bool = False
    local_command_execution_enabled: bool = False
    workspace_file_read_execution_enabled: bool = False
    repository_search_execution_enabled: bool = False
    credential_materialization_enabled: bool = False
    external_adapter: bool = False
    public_core_safe: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderCapabilityDescriptor:
    capability_id: str
    provider_id: str
    provider_type: str
    capability_name: str
    capability_category: str
    description: str
    introduced_in: str
    activation_version: str | None
    implementation_status: str
    input_schema_ref: dict[str, Any] | None
    output_schema_ref: dict[str, Any] | None
    required_permission_policy_ref: dict[str, Any] | None
    required_effect_type: str
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    ocel_object_types: list[str]
    ocel_event_types: list[str]
    ocel_relation_types: list[str]
    read_only: bool
    execution_capable_future: bool
    invocation_enabled: bool = False
    credential_sensitive: bool = False
    private_path_sensitive: bool = False
    raw_secret_output_forbidden: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderCapabilitySurface:
    surface_id: str
    provider_id: str
    provider_type: str
    provider_name: str
    capabilities: list[InternalProviderCapabilityDescriptor]
    surface_status: str = "declared"
    invocation_enabled: bool = False
    execution_enabled: bool = False
    read_execution_enabled: bool = False
    local_command_execution_enabled: bool = False
    external_provider_invocation_enabled: bool = False
    credential_materialization_enabled: bool = False
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderStatus:
    status_id: str
    provider_id: str
    provider_type: str
    lifecycle_status: str
    implementation_status: str
    health_status: str = "not_applicable"
    invocation_ready: bool = False
    registry_ready: bool = True
    capability_surface_ready: bool = True
    execution_ready: bool = False
    finding_count: int = 0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderRegistry:
    registry_id: str
    provider_refs: list[InternalProviderRef]
    capability_surfaces: list[InternalProviderCapabilitySurface]
    provider_statuses: list[InternalProviderStatus]
    version: str = INTERNAL_PROVIDER_REGISTRY_VERSION
    registry_status: str = "declared"
    provider_count: int = 0
    capability_count: int = 0
    invocation_enabled: bool = False
    execution_enabled: bool = False
    external_adapter_count: int = 0
    public_core_safe: bool = True
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderRegistrySnapshot:
    snapshot_id: str
    created_at: str
    registry: InternalProviderRegistry
    version: str = INTERNAL_PROVIDER_REGISTRY_VERSION
    provider_count: int = 0
    capability_surface_count: int = 0
    capability_count: int = 0
    implemented_count: int = 0
    future_track_count: int = 0
    blocked_count: int = 0
    invocation_enabled_count: int = 0
    execution_enabled_count: int = 0
    external_adapter_count: int = 0
    snapshot_status: str = "declared"
    evidence_refs: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderRegistryFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    provider_ref: dict[str, Any] | None
    capability_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderRegistryReport:
    report_id: str
    created_at: str
    request: InternalProviderRegistrationRequest
    registry: InternalProviderRegistry
    snapshot: InternalProviderRegistrySnapshot
    findings: list[InternalProviderRegistryFinding]
    version: str = INTERNAL_PROVIDER_REGISTRY_VERSION
    report_status: str = "passed"
    ready_for_v0_24_2: bool = True
    ready_for_v0_25: bool = False
    provider_invocation_enabled: bool = False
    workspace_read_execution_enabled: bool = False
    repository_search_execution_enabled: bool = False
    file_read_execution_enabled: bool = False
    local_runtime_execution_enabled: bool = False
    local_command_execution_enabled: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_required_step: str = INTERNAL_PROVIDER_REGISTRY_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until provider registry implementation changes or provider capability surfaces are activated."
    )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class InternalProviderCapabilitySurfaceReport:
    report_id: str
    provider_surfaces: list[InternalProviderCapabilitySurface]
    capability_count: int
    read_only_capability_count: int
    future_execution_capability_count: int
    invocation_enabled_count: int
    forbidden_effect_count: int
    findings: list[InternalProviderRegistryFinding]
    version: str = INTERNAL_PROVIDER_REGISTRY_VERSION
    report_status: str = "passed"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class InternalProviderContractSourceService:
    def load_internal_provider_contract(self) -> InternalProviderContract:
        return InternalProviderContractReportService().build_report().contract


class InternalProviderRegistrySkillService:
    def list_skill_contracts(self) -> list[dict[str, Any]]:
        implemented = {
            "skill:internal_provider_contract_view",
            "skill:internal_provider_registry_view",
            "skill:internal_provider_capability_surface_view",
        }
        skills = [
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
        return [
            {
                "skill_id": skill_id,
                "status": "implemented" if skill_id in implemented else "contract_only",
                "implemented": skill_id in implemented,
                "stub": skill_id not in implemented,
                "read_only": True,
                "registry_only": skill_id == "skill:internal_provider_registry_view",
                "surface_only": skill_id == "skill:internal_provider_capability_surface_view",
                "contract_only": skill_id not in implemented or skill_id == "skill:internal_provider_contract_view",
                "provider_invocation_enabled": False,
                "local_command_execution_enabled": False,
            }
            for skill_id in skills
        ]


class InternalProviderRefFactory:
    _PROVIDER_META: dict[str, dict[str, Any]] = {
        "workspace_read_provider": {
            "name": "Workspace Read Provider",
            "description": "Declared provider for future read-only workspace observation.",
            "activation": "v0.24.2",
            "read_only": True,
            "future_exec": False,
        },
        "repository_search_provider": {
            "name": "Repository Search Provider",
            "description": "Declared provider for future repository search surfaces.",
            "activation": "v0.24.3",
            "read_only": True,
            "future_exec": False,
        },
        "file_read_provider": {
            "name": "File Read Provider",
            "description": "Declared provider for future bounded file excerpt reads.",
            "activation": "v0.24.3",
            "read_only": True,
            "future_exec": False,
        },
        "ocel_inspection_provider": {
            "name": "OCEL Inspection Provider",
            "description": "Declared provider for future OCEL inspection surfaces.",
            "activation": "v0.24.4",
            "read_only": True,
            "future_exec": False,
        },
        "pig_inspection_provider": {
            "name": "PIG Inspection Provider",
            "description": "Declared provider for future PIG report inspection surfaces.",
            "activation": "v0.24.4",
            "read_only": True,
            "future_exec": False,
        },
        "ocpx_projection_provider": {
            "name": "OCPX Projection Provider",
            "description": "Declared provider for future OCPX projection inspection surfaces.",
            "activation": "v0.24.4",
            "read_only": True,
            "future_exec": False,
        },
        "local_runtime_provider": {
            "name": "Local Runtime Provider",
            "description": "Declared provider for future gated local runtime candidate and execution boundaries.",
            "activation": "v0.24.5-v0.24.7",
            "read_only": False,
            "future_exec": True,
        },
        "diagnostic_provider": {
            "name": "Diagnostic Provider",
            "description": "Declared provider for future diagnostic candidate and result summaries.",
            "activation": "v0.24.5-v0.24.8",
            "read_only": True,
            "future_exec": False,
        },
        "candidate_generation_provider": {
            "name": "Candidate Generation Provider",
            "description": "Declared provider for future bounded candidate generation surfaces.",
            "activation": "v0.24.x/v0.25.x",
            "read_only": True,
            "future_exec": False,
        },
    }

    def build_provider_refs(
        self,
        request: InternalProviderRegistrationRequest,
        contract: InternalProviderContract,
    ) -> list[InternalProviderRef]:
        selected = set(request.requested_provider_types or [])
        if not selected:
            include_flags = {
                "workspace_read_provider": request.include_workspace_read_provider,
                "repository_search_provider": request.include_repository_search_provider,
                "file_read_provider": request.include_file_read_provider,
                "ocel_inspection_provider": request.include_ocel_inspection_provider,
                "pig_inspection_provider": request.include_pig_inspection_provider,
                "ocpx_projection_provider": request.include_ocpx_projection_provider,
                "local_runtime_provider": request.include_local_runtime_provider,
                "diagnostic_provider": request.include_diagnostic_provider,
                "candidate_generation_provider": request.include_candidate_generation_provider,
            }
            selected = {provider_type for provider_type, include in include_flags.items() if include}
        known_contract_types = {item.provider_type for item in contract.provider_types}
        refs: list[InternalProviderRef] = []
        for provider_type in INTERNAL_PROVIDER_TYPES:
            if provider_type == "unknown" or provider_type not in selected:
                continue
            meta = self._PROVIDER_META[provider_type]
            refs.append(
                InternalProviderRef(
                    provider_id=f"internal_provider:{provider_type}",
                    provider_type=provider_type,
                    provider_name=meta["name"],
                    description=meta["description"],
                    implementation_status="declared" if provider_type in known_contract_types else "blocked",
                    activation_version=meta["activation"],
                    read_only_default=meta["read_only"],
                    execution_capable_future=meta["future_exec"],
                    evidence_refs=[{"type": "contract", "id": contract.contract_id}],
                )
            )
        return refs


class InternalProviderCapabilitySurfaceFactory:
    _CAPABILITIES: dict[str, list[tuple[str, str, str, bool]]] = {
        "workspace_read_provider": [
            ("list_workspace_roots", "workspace_observation", "v0.24.2", False),
            ("describe_workspace", "workspace_observation", "v0.24.2", False),
            ("read_workspace_tree_future", "workspace_observation", "v0.24.2", False),
            ("list_file_metadata_future", "workspace_observation", "v0.24.2", False),
        ],
        "repository_search_provider": [
            ("search_file_names_future", "repository_search", "v0.24.3", False),
            ("search_text_future", "repository_search", "v0.24.3", False),
            ("search_symbols_future", "repository_search", "v0.24.3", False),
            ("rank_repository_matches_future", "repository_search", "v0.24.3", False),
        ],
        "file_read_provider": [
            ("read_file_excerpt_future", "file_read", "v0.24.3", False),
            ("read_bounded_file_future", "file_read", "v0.24.3", False),
            ("sanitize_file_excerpt_future", "file_read", "v0.24.3", False),
        ],
        "ocel_inspection_provider": [
            ("list_ocel_event_types_future", "process_state_inspection", "v0.24.4", False),
            ("list_ocel_object_types_future", "process_state_inspection", "v0.24.4", False),
            ("inspect_recent_ocel_events_future", "process_state_inspection", "v0.24.4", False),
            ("inspect_object_trace_future", "process_state_inspection", "v0.24.4", False),
        ],
        "pig_inspection_provider": [
            ("list_pig_reports_future", "process_state_inspection", "v0.24.4", False),
            ("view_pig_report_future", "process_state_inspection", "v0.24.4", False),
        ],
        "ocpx_projection_provider": [
            ("list_ocpx_projections_future", "process_state_inspection", "v0.24.4", False),
            ("view_ocpx_projection_future", "process_state_inspection", "v0.24.4", False),
        ],
        "local_runtime_provider": [
            ("create_local_command_candidate_future", "local_runtime_candidate", "v0.24.5", True),
            ("check_local_runtime_static_safety_future", "local_runtime_safety", "v0.24.6", True),
            ("check_local_runtime_preflight_future", "local_runtime_safety", "v0.24.6", True),
            ("gated_bounded_local_command_run_future", "local_runtime_execution_boundary", "v0.24.7", True),
        ],
        "diagnostic_provider": [
            ("create_diagnostic_candidate_future", "diagnostic", "v0.24.5", False),
            ("summarize_diagnostic_result_future", "diagnostic", "v0.24.8", False),
        ],
        "candidate_generation_provider": [
            ("create_patch_candidate_future", "candidate_generation", "v0.24.x/v0.25.x", False),
            ("create_action_candidate_future", "candidate_generation", "v0.24.x/v0.25.x", False),
            ("create_next_step_candidate_future", "candidate_generation", "v0.24.x/v0.25.x", False),
        ],
    }

    def build_capability_surfaces(
        self,
        provider_refs: list[InternalProviderRef],
        contract: InternalProviderContract,
    ) -> list[InternalProviderCapabilitySurface]:
        surfaces: list[InternalProviderCapabilitySurface] = []
        for ref in provider_refs:
            capabilities = [
                self._descriptor(ref, name, category, activation, future_exec, contract)
                for name, category, activation, future_exec in self._CAPABILITIES.get(ref.provider_type, [])
            ]
            surfaces.append(
                InternalProviderCapabilitySurface(
                    surface_id=f"internal_provider_surface:{ref.provider_type}",
                    provider_id=ref.provider_id,
                    provider_type=ref.provider_type,
                    provider_name=ref.provider_name,
                    capabilities=capabilities,
                    surface_status="declared" if capabilities else "partial",
                    evidence_refs=[{"type": "provider_ref", "id": ref.provider_id}],
                )
            )
        return surfaces

    def _descriptor(
        self,
        ref: InternalProviderRef,
        name: str,
        category: str,
        activation: str,
        future_exec: bool,
        contract: InternalProviderContract,
    ) -> InternalProviderCapabilityDescriptor:
        permission_ref = {"type": "permission_policy", "id": contract.permission_policy.policy_id}
        effect = "provider_surface_declared"
        return InternalProviderCapabilityDescriptor(
            capability_id=f"capability:{name}",
            provider_id=ref.provider_id,
            provider_type=ref.provider_type,
            capability_name=name,
            capability_category=category,
            description=f"Declared v0.24.1 surface for future {name}.",
            introduced_in=INTERNAL_PROVIDER_REGISTRY_VERSION,
            activation_version=activation,
            implementation_status="declared",
            input_schema_ref={"type": "schema", "id": f"{name}:input"},
            output_schema_ref={"type": "schema", "id": f"{name}:output"},
            required_permission_policy_ref=permission_ref,
            required_effect_type=effect,
            allowed_effect_types=list(INTERNAL_PROVIDER_REGISTRY_ALLOWED_EFFECT_TYPES),
            forbidden_effect_types=list(INTERNAL_PROVIDER_REGISTRY_FORBIDDEN_EFFECT_TYPES),
            ocel_object_types=["internal_provider_capability_descriptor"],
            ocel_event_types=["internal_provider_capability_descriptor_registered"],
            ocel_relation_types=["declares_provider_capability_descriptor"],
            read_only=not future_exec,
            execution_capable_future=future_exec,
            private_path_sensitive=ref.provider_type in {"workspace_read_provider", "file_read_provider"},
            evidence_refs=[{"type": "contract", "id": contract.contract_id}],
        )


class InternalProviderStatusService:
    def build_provider_statuses(
        self,
        provider_refs: list[InternalProviderRef],
        capability_surfaces: list[InternalProviderCapabilitySurface],
    ) -> list[InternalProviderStatus]:
        surface_by_provider = {surface.provider_id: surface for surface in capability_surfaces}
        return [
            InternalProviderStatus(
                status_id=f"internal_provider_status:{ref.provider_type}",
                provider_id=ref.provider_id,
                provider_type=ref.provider_type,
                lifecycle_status="available_future",
                implementation_status=ref.implementation_status,
                capability_surface_ready=bool(surface_by_provider.get(ref.provider_id)),
                notes=["v0.24.1 registry/surface only; invocation remains disabled."],
            )
            for ref in provider_refs
        ]


class InternalProviderRegistryService:
    def __init__(
        self,
        source_service: InternalProviderContractSourceService | None = None,
        ref_factory: InternalProviderRefFactory | None = None,
        surface_factory: InternalProviderCapabilitySurfaceFactory | None = None,
        status_service: InternalProviderStatusService | None = None,
    ) -> None:
        self.source_service = source_service or InternalProviderContractSourceService()
        self.ref_factory = ref_factory or InternalProviderRefFactory()
        self.surface_factory = surface_factory or InternalProviderCapabilitySurfaceFactory()
        self.status_service = status_service or InternalProviderStatusService()

    def build_registry(self, request: InternalProviderRegistrationRequest | None = None) -> InternalProviderRegistry:
        request = request or InternalProviderRegistrationRequest()
        contract = self.source_service.load_internal_provider_contract()
        refs = self.ref_factory.build_provider_refs(request, contract)
        surfaces = self.surface_factory.build_capability_surfaces(refs, contract)
        statuses = self.status_service.build_provider_statuses(refs, surfaces)
        capability_count = sum(len(surface.capabilities) for surface in surfaces)
        external_adapter_count = sum(1 for ref in refs if ref.external_adapter)
        blocked = any(ref.implementation_status == "blocked" for ref in refs)
        return InternalProviderRegistry(
            registry_id="internal_provider_registry:v0.24.1",
            provider_refs=refs,
            capability_surfaces=surfaces,
            provider_statuses=statuses,
            registry_status="blocked" if blocked else "declared",
            provider_count=len(refs),
            capability_count=capability_count,
            external_adapter_count=external_adapter_count,
            public_core_safe=external_adapter_count == 0,
            evidence_refs=[{"type": "contract", "id": contract.contract_id}],
        )


class InternalProviderRegistrySnapshotService:
    def build_snapshot(self, registry: InternalProviderRegistry) -> InternalProviderRegistrySnapshot:
        invocation_enabled_count = sum(1 for ref in registry.provider_refs if ref.provider_invocation_enabled)
        execution_enabled_count = sum(1 for surface in registry.capability_surfaces if surface.execution_enabled)
        future_track_count = sum(1 for ref in registry.provider_refs if ref.execution_capable_future)
        blocked_count = sum(1 for ref in registry.provider_refs if ref.implementation_status == "blocked")
        return InternalProviderRegistrySnapshot(
            snapshot_id="internal_provider_registry_snapshot:v0.24.1",
            created_at=_now(),
            registry=registry,
            provider_count=registry.provider_count,
            capability_surface_count=len(registry.capability_surfaces),
            capability_count=registry.capability_count,
            implemented_count=0,
            future_track_count=future_track_count,
            blocked_count=blocked_count,
            invocation_enabled_count=invocation_enabled_count,
            execution_enabled_count=execution_enabled_count,
            external_adapter_count=registry.external_adapter_count,
            snapshot_status="blocked" if blocked_count else "declared",
        )


class InternalProviderRegistryFindingService:
    _MARKER_FINDINGS = {
        "missing_provider_contract": ("error", "missing_provider_contract"),
        "missing_provider_type": ("error", "missing_provider_type"),
        "missing_provider_ref": ("error", "missing_provider_ref"),
        "missing_capability_surface": ("error", "missing_capability_surface"),
        "missing_capability_descriptor": ("error", "missing_capability_descriptor"),
        "provider_invocation_enabled": ("critical", "provider_invocation_enabled_too_early"),
        "workspace_read_execution_enabled": ("critical", "workspace_read_execution_enabled_too_early"),
        "repository_search_execution_enabled": ("critical", "repository_search_execution_enabled_too_early"),
        "file_read_execution_enabled": ("critical", "file_read_execution_enabled_too_early"),
        "local_command_execution_enabled": ("critical", "local_command_execution_enabled_too_early"),
        "local_runtime_execution_enabled": ("critical", "local_runtime_execution_enabled_too_early"),
        "external_adapter": ("critical", "external_adapter_detected"),
        "vendor_hardcoding": ("critical", "vendor_hardcoding_detected"),
        "credential_materialization": ("critical", "credential_materialization_enabled"),
        "raw_secret_output": ("critical", "raw_secret_output_risk"),
        "missing_ocel_mapping": ("error", "missing_ocel_mapping"),
        "missing_permission_policy_ref": ("error", "missing_permission_policy_ref"),
        "growthkernel_dependency": ("critical", "growthkernel_dependency_detected"),
        "schumpeter_split": ("critical", "schumpeter_split_detected"),
        "general_agent_usability": ("critical", "general_agent_usability_premature"),
        "llm_judge": ("critical", "llm_judge_detected"),
    }

    def build_findings(
        self,
        registry: InternalProviderRegistry,
        snapshot: InternalProviderRegistrySnapshot,
        contract: InternalProviderContract | None,
        markers: list[str] | None = None,
    ) -> list[InternalProviderRegistryFinding]:
        findings: list[InternalProviderRegistryFinding] = []
        if contract is None:
            findings.append(_finding("error", "missing_provider_contract", "Internal Provider Contract is missing."))
        required = {
            "workspace_read_provider",
            "repository_search_provider",
            "file_read_provider",
            "ocel_inspection_provider",
            "pig_inspection_provider",
            "ocpx_projection_provider",
            "local_runtime_provider",
            "diagnostic_provider",
            "candidate_generation_provider",
        }
        present = {ref.provider_type for ref in registry.provider_refs}
        for missing in sorted(required - present):
            findings.append(_finding("error", "missing_provider_ref", f"Required provider ref missing: {missing}."))
        surface_by_provider = {surface.provider_type: surface for surface in registry.capability_surfaces}
        for ref in registry.provider_refs:
            if not ref.provider_type:
                findings.append(_finding("error", "missing_provider_type", "Provider type is missing."))
            if ref.provider_invocation_enabled:
                findings.append(_finding("critical", "provider_invocation_enabled_too_early", ref.provider_id))
            if ref.external_adapter:
                findings.append(_finding("critical", "external_adapter_detected", ref.provider_id))
            surface = surface_by_provider.get(ref.provider_type)
            if not surface:
                findings.append(_finding("error", "missing_capability_surface", ref.provider_id))
                continue
            if not surface.capabilities:
                findings.append(_finding("error", "missing_capability_descriptor", ref.provider_id))
            for capability in surface.capabilities:
                if capability.invocation_enabled:
                    findings.append(_finding("critical", "capability_invocation_enabled_too_early", capability.capability_id))
                if not capability.required_effect_type:
                    findings.append(_finding("error", "missing_capability_descriptor", capability.capability_id))
                if not capability.required_permission_policy_ref:
                    findings.append(_finding("error", "missing_permission_policy_ref", capability.capability_id))
                if not capability.ocel_object_types or not capability.ocel_event_types or not capability.ocel_relation_types:
                    findings.append(_finding("error", "missing_ocel_mapping", capability.capability_id))
        for marker in markers or []:
            severity, finding_type = self._MARKER_FINDINGS.get(marker, ("warning", marker))
            findings.append(_finding(severity, finding_type, f"Marker detected: {marker}."))
        if not findings:
            findings.append(_finding("info", "ok", "Provider registry and capability surfaces are declared only."))
        return findings


class InternalProviderRegistryReportService:
    def __init__(
        self,
        source_service: InternalProviderContractSourceService | None = None,
        registry_service: InternalProviderRegistryService | None = None,
        snapshot_service: InternalProviderRegistrySnapshotService | None = None,
        finding_service: InternalProviderRegistryFindingService | None = None,
    ) -> None:
        self.source_service = source_service or InternalProviderContractSourceService()
        self.registry_service = registry_service or InternalProviderRegistryService(source_service=self.source_service)
        self.snapshot_service = snapshot_service or InternalProviderRegistrySnapshotService()
        self.finding_service = finding_service or InternalProviderRegistryFindingService()

    def build_report(
        self,
        request: InternalProviderRegistrationRequest | None = None,
        markers: list[str] | None = None,
    ) -> InternalProviderRegistryReport:
        request = request or InternalProviderRegistrationRequest()
        contract = self.source_service.load_internal_provider_contract()
        registry = self.registry_service.build_registry(request)
        snapshot = self.snapshot_service.build_snapshot(registry)
        findings = self.finding_service.build_findings(registry, snapshot, contract, markers)
        status = _status_from_findings(findings)
        return InternalProviderRegistryReport(
            report_id="internal_provider_registry_report:v0.24.1",
            created_at=_now(),
            request=request,
            registry=registry,
            snapshot=snapshot,
            findings=findings,
            report_status=status,
            ready_for_v0_24_2=status in {"passed", "warning"}
            and any(ref.provider_type == "workspace_read_provider" for ref in registry.provider_refs),
            limitations=[
                "v0.24.1 declares provider registry and capability surfaces only.",
                "Provider invocation and all read/execution surfaces remain disabled.",
                "Local Runtime Provider is declared as future surface only.",
            ],
            withdrawal_conditions=[
                "Withdraw if provider invocation becomes enabled in v0.24.1.",
                "Withdraw if workspace/repository/file read execution is added in v0.24.1.",
                "Withdraw if local command candidate creation or execution is added in v0.24.1.",
                "Withdraw if credentials, raw secrets, vendor runtime logic, or Schumpeter split logic are introduced.",
            ],
        )

    def build_surface_report(self, registry: InternalProviderRegistry | None = None) -> InternalProviderCapabilitySurfaceReport:
        registry = registry or self.registry_service.build_registry()
        snapshot = self.snapshot_service.build_snapshot(registry)
        findings = self.finding_service.build_findings(registry, snapshot, self.source_service.load_internal_provider_contract())
        capabilities = [capability for surface in registry.capability_surfaces for capability in surface.capabilities]
        return InternalProviderCapabilitySurfaceReport(
            report_id="internal_provider_capability_surface_report:v0.24.1",
            provider_surfaces=registry.capability_surfaces,
            capability_count=len(capabilities),
            read_only_capability_count=sum(1 for capability in capabilities if capability.read_only),
            future_execution_capability_count=sum(1 for capability in capabilities if capability.execution_capable_future),
            invocation_enabled_count=sum(1 for capability in capabilities if capability.invocation_enabled),
            forbidden_effect_count=sum(len(capability.forbidden_effect_types) for capability in capabilities),
            report_status=_status_from_findings(findings),
            findings=findings,
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": INTERNAL_PROVIDER_REGISTRY_VERSION,
            "layer": INTERNAL_PROVIDER_LAYER,
            "subject": "provider_registry_capability_surface",
            "principles": [
                "provider registry is not provider invocation",
                "capability surface is not capability execution",
                "provider registration is not workspace read",
                "provider registration is not repository search",
                "provider registration is not local runtime execution",
                "every provider capability is deny-by-default until activation version",
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
            "next_step": INTERNAL_PROVIDER_REGISTRY_NEXT_STEP,
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
            "state": INTERNAL_PROVIDER_REGISTRY_STATE,
            "version": INTERNAL_PROVIDER_REGISTRY_VERSION,
            "source_read_models": [
                "InternalProviderContractState",
                "InternalProviderEffectPolicyState",
                "InternalProviderPermissionPolicyState",
                "InternalProviderInvocationBoundaryState",
            ],
            "target_read_models": [
                "InternalProviderRegistryState",
                "InternalProviderRefState",
                "InternalProviderCapabilitySurfaceState",
                "InternalProviderCapabilityDescriptorState",
                "InternalProviderStatusState",
                "V024ReadinessState",
            ],
            "effect_types": list(INTERNAL_PROVIDER_REGISTRY_ALLOWED_EFFECT_TYPES),
        }

    def render_report_cli(
        self,
        report: InternalProviderRegistryReport,
        section: str = "registry",
        provider_id: str | None = None,
    ) -> str:
        common = [
            f"version={report.version}",
            f"layer={INTERNAL_PROVIDER_LAYER}",
            f"registry_status={report.registry.registry_status}",
            f"provider_count={report.registry.provider_count}",
            f"capability_count={report.registry.capability_count}",
            f"invocation_enabled={report.registry.invocation_enabled}",
            f"execution_enabled={report.registry.execution_enabled}",
            f"workspace_read_execution_enabled={report.workspace_read_execution_enabled}",
            f"repository_search_execution_enabled={report.repository_search_execution_enabled}",
            f"file_read_execution_enabled={report.file_read_execution_enabled}",
            f"local_runtime_execution_enabled={report.local_runtime_execution_enabled}",
            f"local_command_execution_enabled={report.local_command_execution_enabled}",
            f"external_provider_adapter_implemented={report.external_provider_adapter_implemented}",
            f"schumpeter_split_introduced={report.schumpeter_split_introduced}",
            f"ready_for_v0_24_2={report.ready_for_v0_24_2}",
            f"ready_for_v0_25={report.ready_for_v0_25}",
            f"next_required_step={report.next_required_step}",
        ]
        if section == "list":
            providers = ",".join(ref.provider_type for ref in report.registry.provider_refs)
            return "\n".join(["Internal Provider List", f"providers={providers}"] + common)
        if section in {"surfaces", "surface"}:
            surfaces = ",".join(
                surface.provider_id
                for surface in report.registry.capability_surfaces
                if provider_id is None or surface.provider_id == provider_id
            )
            return "\n".join(["Internal Provider Capability Surfaces", f"surfaces={surfaces}"] + common)
        if section == "capabilities":
            capabilities = ",".join(
                capability.capability_id
                for surface in report.registry.capability_surfaces
                if provider_id is None or surface.provider_id == provider_id
                for capability in surface.capabilities
            )
            return "\n".join(["Internal Provider Capabilities", f"capabilities={capabilities}"] + common)
        if section == "status":
            statuses = ",".join(status.lifecycle_status for status in report.registry.provider_statuses)
            return "\n".join(["Internal Provider Status", f"statuses={statuses}"] + common)
        if section == "snapshot":
            snapshot = report.snapshot
            return "\n".join(
                [
                    "Internal Provider Registry Snapshot",
                    f"capability_surface_count={snapshot.capability_surface_count}",
                    f"invocation_enabled_count={snapshot.invocation_enabled_count}",
                    f"execution_enabled_count={snapshot.execution_enabled_count}",
                    f"external_adapter_count={snapshot.external_adapter_count}",
                ]
                + common
            )
        if section == "report":
            findings = ",".join(finding.finding_type for finding in report.findings)
            return "\n".join(["Internal Provider Registry Report", f"report_status={report.report_status}", f"findings={findings}"] + common)
        return "\n".join(["Internal Provider Registry", f"report_status={report.report_status}"] + common)


def _finding(severity: str, finding_type: str, message: str) -> InternalProviderRegistryFinding:
    return InternalProviderRegistryFinding(
        finding_id=f"internal_provider_registry_finding:{finding_type}",
        severity=severity,
        finding_type=finding_type,
        message=message,
        provider_ref=None,
        capability_ref=None,
        evidence_refs=[{"type": "policy", "id": INTERNAL_PROVIDER_REGISTRY_VERSION}],
        withdrawal_condition="Resolve the finding and rebuild the provider registry report.",
    )


def _status_from_findings(findings: list[InternalProviderRegistryFinding]) -> str:
    severities = {finding.severity for finding in findings}
    if "critical" in severities:
        return "blocked"
    if "error" in severities:
        return "failed"
    if "warning" in severities:
        return "warning"
    return "passed"


def _now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).replace(microsecond=0).isoformat()
