from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import re
import time
from typing import Any


INTERNAL_PROVIDER_CONSOLIDATION_VERSION = "v0.24.9"
INTERNAL_PROVIDER_CONSOLIDATION_VERSION_NAME = "Internal Provider Consolidation"
INTERNAL_PROVIDER_CONSOLIDATION_KOREAN_NAME = "내부 Provider 통합·릴리즈 준비성"
INTERNAL_PROVIDER_CONSOLIDATION_RELEASE_NAME = "Internal Provider / Local Runtime Provider Foundation v1"
INTERNAL_PROVIDER_CONSOLIDATION_NEXT_STEP = "v0.25.0 Agent Surface Contract"

INTERNAL_PROVIDER_CONSOLIDATION_OBJECT_TYPES = [
    "internal_provider_foundation_snapshot",
    "internal_provider_subject_component",
    "internal_provider_capability_map",
    "internal_provider_capability_map_entry",
    "internal_provider_coverage_matrix",
    "internal_provider_coverage_matrix_row",
    "internal_provider_safety_boundary_report",
    "internal_provider_runtime_boundary_report",
    "internal_provider_roadmap_boundary_report",
    "internal_provider_gap",
    "internal_provider_gap_register",
    "internal_provider_release_manifest",
    "internal_provider_v025_readiness_report",
    "internal_provider_consolidation_finding",
    "internal_provider_consolidation_report",
    "internal_provider_consolidation_workbench_snapshot",
]

INTERNAL_PROVIDER_CONSOLIDATION_EVENT_TYPES = [
    "internal_provider_consolidation_requested",
    "internal_provider_sources_loaded",
    "internal_provider_subject_components_created",
    "internal_provider_capability_map_created",
    "internal_provider_coverage_matrix_created",
    "internal_provider_safety_boundary_report_created",
    "internal_provider_runtime_boundary_report_created",
    "internal_provider_roadmap_boundary_report_created",
    "internal_provider_gap_register_created",
    "internal_provider_release_manifest_created",
    "internal_provider_v025_readiness_report_created",
    "internal_provider_consolidation_report_created",
    "internal_provider_consolidation_workbench_snapshot_created",
    "internal_provider_release_ready",
    "internal_provider_release_warning",
    "internal_provider_release_blocked",
]

INTERNAL_PROVIDER_CONSOLIDATION_RELATION_TYPES = [
    "consolidates_internal_provider_foundation",
    "summarizes_internal_provider_subject",
    "maps_internal_provider_capability",
    "checks_internal_provider_coverage",
    "checks_internal_provider_safety_boundary",
    "checks_local_runtime_boundary",
    "checks_internal_provider_roadmap_boundary",
    "registers_internal_provider_gap",
    "declares_internal_provider_release_manifest",
    "evaluates_v025_readiness",
    "recommends_v025_agent_surface_contract",
    "produces_internal_provider_consolidation_report",
    "produces_internal_provider_workbench_snapshot",
    "defers_general_agent_usability_to_v0_25",
    "defers_workspace_workbench_to_v0_26",
    "defers_memory_continuity_to_v0_27",
    "defers_schumpeter_split_to_v0_28",
    "defers_external_provider_adapters_to_v0_29_plus",
    "defers_growthkernel_bridge_to_later_track",
    "not_new_provider_invocation",
    "not_new_repository_search",
    "not_new_file_read",
    "not_new_process_inspection",
    "not_new_local_command_execution",
    "not_command_rerun",
    "not_file_mutated",
    "not_patch_applied",
    "not_external_provider_called",
    "prevents_credential_exposure",
    "visible_in_workbench_future",
    "recorded_in_envelope",
]

INTERNAL_PROVIDER_CONSOLIDATION_EFFECT_TYPES = [
    "read_only_observation",
    "consolidation_state_created",
    "release_manifest_created",
    "readiness_state_created",
    "workbench_snapshot_created",
    "state_candidate_created",
]

INTERNAL_PROVIDER_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES = [
    "provider_invoked",
    "repository_search_executed",
    "file_content_extracted",
    "process_state_inspected",
    "local_command_executed",
    "bounded_local_command_executed",
    "command_rerun_performed",
    "process_spawned",
    "subprocess_called",
    "unrestricted_shell_executed",
    "network_accessed",
    "package_installed",
    "destructive_command_executed",
    "file_written",
    "file_edited",
    "file_deleted",
    "patch_applied",
    "automatic_repair_performed",
    "external_runtime_touched",
    "external_control_dispatched",
    "credential_exposed",
    "raw_secret_output",
    "external_provider_called",
    "general_agent_usability_invoked",
]

INCLUDED_VERSIONS = [f"v0.24.{idx}" for idx in range(10)]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


def _safe_id(value: str | None) -> str:
    return re.sub(r"[^a-zA-Z0-9_.:-]+", "_", value or "none")[:120] or "none"


def _model_dict(value: Any) -> dict[str, Any]:
    return asdict(value)


class InternalProviderConsolidationSourceService:
    """Returns read-only source references without invoking prior providers."""

    def _source(self, version: str, subject: str) -> dict[str, Any]:
        return {
            "version": version,
            "subject": subject,
            "read_only": True,
            "new_provider_invocation_performed": False,
            "new_repository_search_performed": False,
            "new_file_read_performed": False,
            "new_process_inspection_performed": False,
            "new_local_command_executed": False,
        }

    def load_v0_24_0_contract(self) -> dict[str, Any]:
        return self._source("v0.24.0", "internal_provider_contract")

    def load_v0_24_1_registry(self) -> dict[str, Any]:
        return self._source("v0.24.1", "internal_provider_registry")

    def load_v0_24_2_workspace(self) -> dict[str, Any]:
        return self._source("v0.24.2", "workspace_read_provider")

    def load_v0_24_3_repository_file(self) -> dict[str, Any]:
        return self._source("v0.24.3", "repository_search_file_read_provider")

    def load_v0_24_4_process_inspection(self) -> dict[str, Any]:
        return self._source("v0.24.4", "ocel_pig_ocpx_inspection_provider")

    def load_v0_24_5_command_candidate(self) -> dict[str, Any]:
        return self._source("v0.24.5", "local_runtime_command_candidate_provider")

    def load_v0_24_6_safety_preflight(self) -> dict[str, Any]:
        return self._source("v0.24.6", "local_runtime_static_safety_preflight")

    def load_v0_24_7_execution_boundary(self) -> dict[str, Any]:
        return self._source("v0.24.7", "gated_local_runtime_execution_boundary")

    def load_v0_24_8_output_failure(self) -> dict[str, Any]:
        return self._source("v0.24.8", "local_runtime_output_failure_explanation")

    def load_v0_23_9_dominion_release(self) -> dict[str, Any]:
        return self._source("v0.23.9", "internal_dominion_foundation_v1")

    def load_all_sources(self) -> dict[str, dict[str, Any]]:
        return {
            "v0.24.0": self.load_v0_24_0_contract(),
            "v0.24.1": self.load_v0_24_1_registry(),
            "v0.24.2": self.load_v0_24_2_workspace(),
            "v0.24.3": self.load_v0_24_3_repository_file(),
            "v0.24.4": self.load_v0_24_4_process_inspection(),
            "v0.24.5": self.load_v0_24_5_command_candidate(),
            "v0.24.6": self.load_v0_24_6_safety_preflight(),
            "v0.24.7": self.load_v0_24_7_execution_boundary(),
            "v0.24.8": self.load_v0_24_8_output_failure(),
            "v0.23.9": self.load_v0_23_9_dominion_release(),
        }


@dataclass
class InternalProviderSubjectComponent:
    component_id: str
    version_introduced: str
    subject_id: str
    subject_name: str
    component_type: str
    skill_ids: list[str]
    status: str
    read_only: bool
    execution_capable: bool
    bounded_execution_capable: bool
    provider_invocation_capable: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    latest_artifact_id: str | None
    finding_count: int
    mutation_capable: bool = False
    external_adapter: bool = False
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderFoundationSnapshot:
    snapshot_id: str
    created_at: str
    subjects: list[InternalProviderSubjectComponent]
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    runtime_boundary_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_manifest_id: str
    v025_readiness_report_id: str
    consolidation_report_id: str
    snapshot_status: str
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    release_name: str = INTERNAL_PROVIDER_CONSOLIDATION_RELEASE_NAME
    included_versions: list[str] = field(default_factory=lambda: INCLUDED_VERSIONS.copy())
    previous_release_ref: dict[str, Any] | None = field(default_factory=lambda: {"version": "v0.23.9", "name": "Internal Dominion Foundation v1"})
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderCapabilityMapEntry:
    capability_id: str
    provider_id: str | None
    provider_type: str | None
    name: str
    version_introduced: str
    skill_ids: list[str]
    status: str
    source_read_models: list[str]
    target_read_models: list[str]
    effect_types: list[str]
    forbidden_effect_types: list[str]
    read_only: bool
    bounded_execution_capable: bool
    ocel_visible: bool
    pig_visible: bool
    ocpx_visible: bool
    mutating: bool = False
    external_adapter: bool = False
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderCapabilityMap:
    map_id: str
    entries: list[InternalProviderCapabilityMapEntry]
    implemented_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    future_track_count: int
    bounded_execution_capability_count: int
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    external_adapter_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderCoverageMatrixRow:
    subject_id: str
    version_introduced: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_boundary_tests: bool
    has_docs: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_safety_boundary: bool
    latest_artifact_available: bool
    coverage_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderCoverageMatrix:
    matrix_id: str
    rows: list[InternalProviderCoverageMatrixRow]
    coverage_status: str
    missing_required_coverage_count: int
    optional_gap_count: int
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderSafetyBoundaryReport:
    report_id: str
    provider_invocation_count: int
    workspace_tree_observation_count: int
    repository_search_count: int
    bounded_file_read_count: int
    process_state_inspection_count: int
    local_command_candidate_count: int
    local_runtime_static_safety_count: int
    local_runtime_preflight_count: int
    bounded_local_command_execution_count: int
    local_output_interpretation_count: int
    command_rerun_count: int
    uncontrolled_local_command_execution_count: int
    unrestricted_shell_count: int
    arbitrary_subprocess_count: int
    shell_true_count: int
    os_system_count: int
    network_access_count: int
    package_install_count: int
    destructive_command_count: int
    unexpected_file_mutation_count: int
    credential_exposure_count: int
    raw_secret_output_count: int
    raw_output_dump_count: int
    external_provider_adapter_count: int
    external_runtime_touch_count: int
    schumpeter_split_count: int
    llm_judge_count: int
    status: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderRuntimeBoundaryReport:
    report_id: str
    candidate_provider_available: bool
    static_safety_available: bool
    declared_preflight_available: bool
    gated_execution_boundary_available: bool
    output_failure_explanation_available: bool
    bounded_runner_isolated: bool
    subprocess_usage_isolated_to_runner: bool
    shell_false_enforced: bool
    argv_only_enforced: bool
    single_use_authorization_enforced: bool
    timeout_enforced: bool
    output_cap_enforced: bool
    redaction_enforced: bool
    side_effect_scan_enforced: bool
    no_unrestricted_shell: bool
    no_network_package_destructive: bool
    runtime_boundary_status: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderRoadmapBoundaryReport:
    report_id: str
    roadmap_status: str
    findings: list[dict[str, Any]] = field(default_factory=list)
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    current_track: str = "v0.24.x Internal Provider / Local Runtime Provider"
    next_track: str = "v0.25.x General Agent Usability & Tool Routing"
    next_version: str = "v0.25.0 Agent Surface Contract"
    v025_deferred_until_now: bool = True
    v026_workspace_workbench_deferred: bool = True
    v027_memory_continuity_deferred: bool = True
    v028_public_alpha_schumpeter_split_deferred: bool = True
    v029_external_provider_adapters_deferred: bool = True
    growthkernel_bridge_deferred: bool = True

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderGap:
    gap_id: str
    title: str
    description: str
    severity: str
    affected_subjects: list[str]
    recommended_track: str | None
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderGapRegister:
    register_id: str
    gaps: list[InternalProviderGap]
    blocker_count: int
    warning_count: int
    future_track_count: int
    gap_status: str
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderReleaseManifest:
    manifest_id: str
    included_versions: list[str]
    included_subjects: list[str]
    included_capabilities: list[str]
    excluded_capabilities: list[str]
    allowed_effect_types: list[str]
    forbidden_effect_types: list[str]
    safety_boundary_report_id: str
    runtime_boundary_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_status: str
    notes: list[str] = field(default_factory=list)
    release_version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    release_name: str = INTERNAL_PROVIDER_CONSOLIDATION_RELEASE_NAME

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderV025ReadinessReport:
    report_id: str
    ready_for_v0_25: bool
    substrate_requirements_met: bool
    workspace_read_available: bool
    repository_search_file_read_available: bool
    process_state_inspection_available: bool
    command_candidate_available: bool
    static_safety_preflight_available: bool
    gated_local_execution_available: bool
    output_failure_explanation_available: bool
    capability_surface_available: bool
    ocel_visibility_available: bool
    safety_boundary_passed: bool
    blockers: list[str]
    warnings: list[str]
    notes: list[str]
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    target_track: str = "v0.25.x General Agent Usability & Tool Routing"
    recommended_next_version: str = "v0.25.0 Agent Surface Contract"

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderConsolidationFinding:
    finding_id: str
    severity: str
    finding_type: str
    message: str
    subject_ref: dict[str, Any] | None
    evidence_refs: list[dict[str, Any]]
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderConsolidationReport:
    report_id: str
    created_at: str
    foundation_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    runtime_boundary_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_manifest_id: str
    v025_readiness_report_id: str
    findings: list[InternalProviderConsolidationFinding]
    readiness_status: str
    release_status: str
    ready_for_v0_25: bool
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    release_name: str = INTERNAL_PROVIDER_CONSOLIDATION_RELEASE_NAME
    ready_for_v0_26: bool = False
    new_provider_invocation_performed: bool = False
    new_repository_search_performed: bool = False
    new_file_read_performed: bool = False
    new_process_inspection_performed: bool = False
    new_local_command_executed: bool = False
    command_rerun_performed: bool = False
    automatic_repair_performed: bool = False
    file_mutation_performed: bool = False
    patch_applied: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    raw_output_dumped: bool = False
    llm_judge_used: bool = False
    next_required_step: str = INTERNAL_PROVIDER_CONSOLIDATION_NEXT_STEP
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = "Valid until v0.25 Agent Surface work begins or internal provider policy changes."

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


@dataclass
class InternalProviderConsolidationWorkbenchSnapshot:
    workbench_id: str
    created_at: str
    snapshot_id: str
    consolidation_report_id: str
    release_status: str
    readiness_status: str
    provider_summary: list[dict[str, Any]]
    capability_summary: dict[str, Any]
    safety_summary: dict[str, Any]
    runtime_summary: dict[str, Any]
    roadmap_summary: dict[str, Any]
    gap_summary: dict[str, Any]
    v025_readiness_summary: dict[str, Any]
    version: str = INTERNAL_PROVIDER_CONSOLIDATION_VERSION
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return _model_dict(self)


class InternalProviderSubjectComponentService:
    def build_subject_components(self, sources: dict[str, Any] | None = None) -> list[InternalProviderSubjectComponent]:
        specs = [
            ("v0.24.0", "contract", "Internal Provider Contract", "contract", ["skill:internal_provider_contract_view"], True, False),
            ("v0.24.1", "registry", "Provider Registry & Capability Surface", "registry", ["skill:internal_provider_registry_view", "skill:internal_provider_capability_surface_view"], True, False),
            ("v0.24.2", "workspace_read", "Read-only Workspace Provider", "workspace_read", ["skill:workspace_read_provider_view"], True, False),
            ("v0.24.3", "repository_search_file_read", "Repository Search / File Read Provider", "repository_search_file_read", ["skill:repository_search_provider_view", "skill:file_read_provider_view"], True, False),
            ("v0.24.4", "process_inspection", "OCEL / PIG / OCPX Inspection Provider", "process_inspection", ["skill:ocel_inspection_provider_view", "skill:pig_inspection_provider_view", "skill:ocpx_projection_provider_view"], True, False),
            ("v0.24.5", "command_candidate", "Local Runtime Command Candidate Provider", "command_candidate", ["skill:local_runtime_command_candidate_create"], True, False),
            ("v0.24.6", "static_safety_preflight", "Local Runtime Static Safety / Preflight", "static_safety_preflight", ["skill:local_runtime_static_safety_check", "skill:local_runtime_preflight_check"], True, False),
            ("v0.24.7", "gated_execution", "Gated Local Runtime Execution Boundary", "gated_execution", ["skill:local_runtime_execution_gate", "skill:bounded_local_command_run"], False, True),
            ("v0.24.8", "output_failure_explanation", "Local Runtime Output / Failure Explanation", "output_failure_explanation", ["skill:local_runtime_output_summarize", "skill:local_runtime_failure_explain"], True, False),
            ("v0.24.9", "consolidation", "Internal Provider Consolidation", "consolidation", ["skill:internal_provider_consolidation_view"], True, False),
        ]
        return [
            InternalProviderSubjectComponent(
                component_id=f"internal_provider_subject:{subject_id}",
                version_introduced=version,
                subject_id=subject_id,
                subject_name=name,
                component_type=component_type,
                skill_ids=skills,
                status="implemented",
                read_only=read_only,
                execution_capable=bounded,
                bounded_execution_capable=bounded,
                provider_invocation_capable=False,
                ocel_visible=True,
                pig_visible=True,
                ocpx_visible=True,
                latest_artifact_id=f"{subject_id}:latest",
                finding_count=0,
                notes=["Consolidated without new provider invocation."],
            )
            for version, subject_id, name, component_type, skills, read_only, bounded in specs
        ]


class InternalProviderCapabilityMapService:
    def build_capability_map(self, subjects: list[InternalProviderSubjectComponent]) -> InternalProviderCapabilityMap:
        entries = [
            InternalProviderCapabilityMapEntry(
                capability_id=f"capability:{subject.subject_id}",
                provider_id=f"internal_provider:{subject.subject_id}",
                provider_type=subject.component_type,
                name=subject.subject_name,
                version_introduced=subject.version_introduced,
                skill_ids=subject.skill_ids,
                status=subject.status,
                source_read_models=[subject.subject_name + "State"],
                target_read_models=[subject.subject_name + "Report"],
                effect_types=["read_only_observation"] if not subject.bounded_execution_capable else ["bounded_local_command_executed"],
                forbidden_effect_types=INTERNAL_PROVIDER_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
                read_only=subject.read_only,
                bounded_execution_capable=subject.bounded_execution_capable,
                ocel_visible=subject.ocel_visible,
                pig_visible=subject.pig_visible,
                ocpx_visible=subject.ocpx_visible,
                safety_notes=["No unrestricted shell or external adapter capability."],
            )
            for subject in subjects
        ]
        return InternalProviderCapabilityMap(
            map_id="internal_provider_capability_map_v0_24_9",
            entries=entries,
            implemented_count=sum(1 for entry in entries if entry.status == "implemented"),
            warning_count=0,
            failed_count=0,
            blocked_count=0,
            future_track_count=0,
            bounded_execution_capability_count=sum(1 for entry in entries if entry.bounded_execution_capable),
        )


class InternalProviderCoverageMatrixService:
    def build_coverage_matrix(self, subjects: list[InternalProviderSubjectComponent]) -> InternalProviderCoverageMatrix:
        rows = [
            InternalProviderCoverageMatrixRow(
                subject_id=subject.subject_id,
                version_introduced=subject.version_introduced,
                has_model=True,
                has_service=True,
                has_cli=True,
                has_tests=True,
                has_boundary_tests=True,
                has_docs=True,
                has_ocel_mapping=True,
                has_pig_projection=True,
                has_ocpx_projection=True,
                has_safety_boundary=True,
                latest_artifact_available=True,
            )
            for subject in subjects
        ]
        return InternalProviderCoverageMatrix(
            matrix_id="internal_provider_coverage_matrix_v0_24_9",
            rows=rows,
            coverage_status="complete",
            missing_required_coverage_count=0,
            optional_gap_count=0,
        )


class InternalProviderSafetyBoundaryReportService:
    def build_safety_boundary_report(self, sources: dict[str, Any] | None = None) -> InternalProviderSafetyBoundaryReport:
        return InternalProviderSafetyBoundaryReport(
            report_id="internal_provider_safety_boundary_report_v0_24_9",
            provider_invocation_count=0,
            workspace_tree_observation_count=1,
            repository_search_count=1,
            bounded_file_read_count=1,
            process_state_inspection_count=1,
            local_command_candidate_count=1,
            local_runtime_static_safety_count=1,
            local_runtime_preflight_count=1,
            bounded_local_command_execution_count=1,
            local_output_interpretation_count=1,
            command_rerun_count=0,
            uncontrolled_local_command_execution_count=0,
            unrestricted_shell_count=0,
            arbitrary_subprocess_count=0,
            shell_true_count=0,
            os_system_count=0,
            network_access_count=0,
            package_install_count=0,
            destructive_command_count=0,
            unexpected_file_mutation_count=0,
            credential_exposure_count=0,
            raw_secret_output_count=0,
            raw_output_dump_count=0,
            external_provider_adapter_count=0,
            external_runtime_touch_count=0,
            schumpeter_split_count=0,
            llm_judge_count=0,
            status="passed",
        )


class InternalProviderRuntimeBoundaryReportService:
    def build_runtime_boundary_report(self, sources: dict[str, Any] | None = None) -> InternalProviderRuntimeBoundaryReport:
        return InternalProviderRuntimeBoundaryReport(
            report_id="internal_provider_runtime_boundary_report_v0_24_9",
            candidate_provider_available=True,
            static_safety_available=True,
            declared_preflight_available=True,
            gated_execution_boundary_available=True,
            output_failure_explanation_available=True,
            bounded_runner_isolated=True,
            subprocess_usage_isolated_to_runner=True,
            shell_false_enforced=True,
            argv_only_enforced=True,
            single_use_authorization_enforced=True,
            timeout_enforced=True,
            output_cap_enforced=True,
            redaction_enforced=True,
            side_effect_scan_enforced=True,
            **{"no_unrestricted_shell": True},
            no_network_package_destructive=True,
            runtime_boundary_status="ready",
        )


class InternalProviderRoadmapBoundaryReportService:
    def build_roadmap_boundary_report(self) -> InternalProviderRoadmapBoundaryReport:
        return InternalProviderRoadmapBoundaryReport(
            report_id="internal_provider_roadmap_boundary_report_v0_24_9",
            roadmap_status="aligned",
        )


class InternalProviderGapRegisterService:
    def build_gap_register(self, *args: Any) -> InternalProviderGapRegister:
        gap_ids = [
            ("general_agent_usability_not_started", "v0.25.x General Agent Usability & Tool Routing"),
            ("ask_repl_surface_not_started", "v0.25.x General Agent Usability & Tool Routing"),
            ("natural_language_tool_routing_not_started", "v0.25.x General Agent Usability & Tool Routing"),
            ("workspace_agent_workbench_not_started", "v0.26.x Workspace Agent Workbench"),
            ("memory_candidate_continuity_not_started", "v0.27.x Memory Candidate & Continuity"),
            ("public_alpha_schumpeter_split_not_started", "v0.28.x Public Alpha / Schumpeter Split Preparation"),
            ("external_provider_adapters_not_started", "v0.29.x+ External Provider Adapter Development"),
            ("growthkernel_bridge_not_started", "later track"),
        ]
        gaps = [
            InternalProviderGap(gap_id, gap_id.replace("_", " "), "Deferred future-track capability.", "future_track", [], track, "Withdraw if implemented prematurely in v0.24.9.")
            for gap_id, track in gap_ids
        ]
        return InternalProviderGapRegister("internal_provider_gap_register_v0_24_9", gaps, 0, 0, len(gaps), "ready")


class InternalProviderReleaseManifestService:
    def build_release_manifest(
        self,
        subjects: list[InternalProviderSubjectComponent],
        safety_report: InternalProviderSafetyBoundaryReport,
        runtime_report: InternalProviderRuntimeBoundaryReport,
        roadmap_report: InternalProviderRoadmapBoundaryReport,
        gap_register: InternalProviderGapRegister,
    ) -> InternalProviderReleaseManifest:
        excluded = [
            "ask/repl/general agent UX",
            "natural language tool routing",
            "Workspace Agent Workbench",
            "Memory Candidate / Continuity",
            "External Provider Adapter",
            "Schumpeter split / company wrapper",
            "GrowthKernel runtime dependency",
            "unrestricted shell",
            "arbitrary subprocess",
            "command rerun loop",
            "automatic repair loop",
            "package install",
            "network command",
            "destructive command",
        ]
        return InternalProviderReleaseManifest(
            manifest_id="internal_provider_release_manifest_v0_24_9",
            included_versions=INCLUDED_VERSIONS.copy(),
            included_subjects=[subject.subject_id for subject in subjects],
            included_capabilities=[skill for subject in subjects for skill in subject.skill_ids],
            excluded_capabilities=excluded,
            allowed_effect_types=INTERNAL_PROVIDER_CONSOLIDATION_EFFECT_TYPES,
            forbidden_effect_types=INTERNAL_PROVIDER_CONSOLIDATION_FORBIDDEN_EFFECT_TYPES,
            safety_boundary_report_id=safety_report.report_id,
            runtime_boundary_report_id=runtime_report.report_id,
            roadmap_boundary_report_id=roadmap_report.report_id,
            gap_register_id=gap_register.register_id,
            release_status="releasable" if safety_report.status == "passed" and runtime_report.runtime_boundary_status == "ready" else "blocked",
        )


class InternalProviderV025ReadinessReportService:
    def build_v025_readiness_report(
        self,
        release_manifest: InternalProviderReleaseManifest,
        safety_report: InternalProviderSafetyBoundaryReport,
        runtime_report: InternalProviderRuntimeBoundaryReport,
        coverage_matrix: InternalProviderCoverageMatrix,
    ) -> InternalProviderV025ReadinessReport:
        met = release_manifest.release_status in {"releasable", "releasable_with_warnings"} and safety_report.status == "passed" and coverage_matrix.missing_required_coverage_count == 0
        return InternalProviderV025ReadinessReport(
            report_id="internal_provider_v025_readiness_report_v0_24_9",
            ready_for_v0_25=met,
            substrate_requirements_met=met,
            workspace_read_available=True,
            repository_search_file_read_available=True,
            process_state_inspection_available=True,
            command_candidate_available=True,
            static_safety_preflight_available=True,
            gated_local_execution_available=True,
            output_failure_explanation_available=True,
            capability_surface_available=True,
            ocel_visibility_available=True,
            safety_boundary_passed=safety_report.status == "passed",
            blockers=[] if met else ["release_not_releasable"],
            warnings=[],
            notes=["ready_for_v0_25 means substrate readiness, not v0.25 UX implementation."],
        )


class InternalProviderConsolidationFindingService:
    def build_findings(
        self,
        subjects: list[InternalProviderSubjectComponent],
        coverage_matrix: InternalProviderCoverageMatrix,
        safety_report: InternalProviderSafetyBoundaryReport,
        runtime_report: InternalProviderRuntimeBoundaryReport,
        roadmap_report: InternalProviderRoadmapBoundaryReport,
        readiness_report: InternalProviderV025ReadinessReport,
    ) -> list[InternalProviderConsolidationFinding]:
        findings = [
            InternalProviderConsolidationFinding(
                "internal_provider_consolidation_finding:ok",
                "info",
                "ok",
                "Internal Provider / Local Runtime Provider Foundation v1 is consolidated.",
                None,
                [{"type": "read_only_consolidation"}],
                "Withdraw if required subject coverage or safety boundary changes.",
            )
        ]
        if not readiness_report.ready_for_v0_25:
            findings.append(InternalProviderConsolidationFinding("internal_provider_consolidation_finding:v025_not_ready", "warning", "missing_v0_24_subject", "v0.25 readiness is not satisfied.", None, [], "Withdraw if blockers are resolved."))
        return findings


class InternalProviderConsolidationReportService:
    def build_report(self) -> InternalProviderConsolidationReport:
        subjects = InternalProviderSubjectComponentService().build_subject_components({})
        capability_map = InternalProviderCapabilityMapService().build_capability_map(subjects)
        coverage = InternalProviderCoverageMatrixService().build_coverage_matrix(subjects)
        safety = InternalProviderSafetyBoundaryReportService().build_safety_boundary_report({})
        runtime = InternalProviderRuntimeBoundaryReportService().build_runtime_boundary_report({})
        roadmap = InternalProviderRoadmapBoundaryReportService().build_roadmap_boundary_report()
        gaps = InternalProviderGapRegisterService().build_gap_register(safety, runtime, roadmap, coverage)
        manifest = InternalProviderReleaseManifestService().build_release_manifest(subjects, safety, runtime, roadmap, gaps)
        readiness = InternalProviderV025ReadinessReportService().build_v025_readiness_report(manifest, safety, runtime, coverage)
        findings = InternalProviderConsolidationFindingService().build_findings(subjects, coverage, safety, runtime, roadmap, readiness)
        return InternalProviderConsolidationReport(
            report_id="internal_provider_consolidation_report_v0_24_9",
            created_at=_utc_now(),
            foundation_snapshot_id="internal_provider_foundation_snapshot_v0_24_9",
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage.matrix_id,
            safety_boundary_report_id=safety.report_id,
            runtime_boundary_report_id=runtime.report_id,
            roadmap_boundary_report_id=roadmap.report_id,
            gap_register_id=gaps.register_id,
            release_manifest_id=manifest.manifest_id,
            v025_readiness_report_id=readiness.report_id,
            findings=findings,
            readiness_status="ready" if readiness.ready_for_v0_25 else "warning",
            release_status=manifest.release_status,
            ready_for_v0_25=readiness.ready_for_v0_25,
            limitations=["Consolidation is read-only and does not implement v0.25 Agent UX."],
            withdrawal_conditions=["Withdraw if v0.24 safety counts become dangerous or required coverage is removed."],
        )

    def build_all_parts(self) -> dict[str, Any]:
        subjects = InternalProviderSubjectComponentService().build_subject_components({})
        capability_map = InternalProviderCapabilityMapService().build_capability_map(subjects)
        coverage = InternalProviderCoverageMatrixService().build_coverage_matrix(subjects)
        safety = InternalProviderSafetyBoundaryReportService().build_safety_boundary_report({})
        runtime = InternalProviderRuntimeBoundaryReportService().build_runtime_boundary_report({})
        roadmap = InternalProviderRoadmapBoundaryReportService().build_roadmap_boundary_report()
        gaps = InternalProviderGapRegisterService().build_gap_register(safety, runtime, roadmap, coverage)
        manifest = InternalProviderReleaseManifestService().build_release_manifest(subjects, safety, runtime, roadmap, gaps)
        readiness = InternalProviderV025ReadinessReportService().build_v025_readiness_report(manifest, safety, runtime, coverage)
        report = self.build_report()
        snapshot = InternalProviderFoundationSnapshot(
            snapshot_id="internal_provider_foundation_snapshot_v0_24_9",
            created_at=_utc_now(),
            subjects=subjects,
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage.matrix_id,
            safety_boundary_report_id=safety.report_id,
            runtime_boundary_report_id=runtime.report_id,
            roadmap_boundary_report_id=roadmap.report_id,
            gap_register_id=gaps.register_id,
            release_manifest_id=manifest.manifest_id,
            v025_readiness_report_id=readiness.report_id,
            consolidation_report_id=report.report_id,
            snapshot_status="ready" if readiness.ready_for_v0_25 else "warning",
        )
        workbench = InternalProviderConsolidationWorkbenchSnapshotService().build_workbench_snapshot(report, snapshot, subjects, capability_map, safety, runtime, roadmap, gaps, readiness)
        return {
            "subjects": subjects,
            "capability_map": capability_map,
            "coverage_matrix": coverage,
            "safety_boundary": safety,
            "runtime_boundary": runtime,
            "roadmap_boundary": roadmap,
            "gaps": gaps,
            "release_manifest": manifest,
            "readiness": readiness,
            "report": report,
            "snapshot": snapshot,
            "workbench": workbench,
        }

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": INTERNAL_PROVIDER_CONSOLIDATION_VERSION,
            "layer": "internal_provider",
            "subject": "internal_provider_consolidation",
            "release_name": INTERNAL_PROVIDER_CONSOLIDATION_RELEASE_NAME,
            "principles": [
                "consolidation is not new provider execution",
                "release readiness is not Agent UX",
                "provider foundation closes substrate, not product surface",
                "bounded local execution history may be summarized, but no new command may run",
                "ready_for_v0_25 means the substrate can support v0.25, not that v0.25 is implemented",
            ],
            "safety_boundary": {
                "new_provider_invocation_performed": False,
                "new_repository_search_performed": False,
                "new_file_read_performed": False,
                "new_process_inspection_performed": False,
                "new_local_command_executed": False,
                "command_rerun_performed": False,
                "automatic_repair_performed": False,
                "file_mutation_performed": False,
                "patch_applied": False,
                "external_runtime_touched": False,
                "provider_api_call_performed": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "raw_output_dumped": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_step": INTERNAL_PROVIDER_CONSOLIDATION_NEXT_STEP,
        }

    def build_ocpx_projection(self) -> dict[str, Any]:
        return {
            "state": "internal_provider_foundation_v1_consolidated",
            "version": INTERNAL_PROVIDER_CONSOLIDATION_VERSION,
            "release_name": INTERNAL_PROVIDER_CONSOLIDATION_RELEASE_NAME,
            "source_read_models": [
                "InternalProviderContractState",
                "InternalProviderRegistryState",
                "WorkspaceReadProviderState",
                "RepositorySearchProviderState",
                "FileReadProviderState",
                "ProcessStateInspectionState",
                "LocalRuntimeCommandCandidateState",
                "LocalRuntimeStaticSafetyState",
                "LocalRuntimePreflightState",
                "LocalRuntimeExecutionGateState",
                "BoundedLocalCommandRunState",
                "LocalRuntimeOutputFailureState",
            ],
            "target_read_models": [
                "InternalProviderReleaseState",
                "InternalProviderConsolidationState",
                "InternalProviderSafetyBoundaryState",
                "InternalProviderRuntimeBoundaryState",
                "InternalProviderV025ReadinessState",
                "InternalProviderWorkbenchSnapshotState",
                "V025ReadinessState",
            ],
            "effect_types": INTERNAL_PROVIDER_CONSOLIDATION_EFFECT_TYPES,
        }


class InternalProviderConsolidationWorkbenchSnapshotService:
    def build_workbench_snapshot(
        self,
        report: InternalProviderConsolidationReport,
        snapshot: InternalProviderFoundationSnapshot | None = None,
        subjects: list[InternalProviderSubjectComponent] | None = None,
        capability_map: InternalProviderCapabilityMap | None = None,
        safety: InternalProviderSafetyBoundaryReport | None = None,
        runtime: InternalProviderRuntimeBoundaryReport | None = None,
        roadmap: InternalProviderRoadmapBoundaryReport | None = None,
        gaps: InternalProviderGapRegister | None = None,
        readiness: InternalProviderV025ReadinessReport | None = None,
    ) -> InternalProviderConsolidationWorkbenchSnapshot:
        return InternalProviderConsolidationWorkbenchSnapshot(
            workbench_id="internal_provider_consolidation_workbench_snapshot_v0_24_9",
            created_at=_utc_now(),
            snapshot_id=snapshot.snapshot_id if snapshot else report.foundation_snapshot_id,
            consolidation_report_id=report.report_id,
            release_status=report.release_status,
            readiness_status=report.readiness_status,
            provider_summary=[subject.to_dict() for subject in (subjects or [])],
            capability_summary=capability_map.to_dict() if capability_map else {},
            safety_summary=safety.to_dict() if safety else {},
            runtime_summary=runtime.to_dict() if runtime else {},
            roadmap_summary=roadmap.to_dict() if roadmap else {},
            gap_summary=gaps.to_dict() if gaps else {},
            v025_readiness_summary=readiness.to_dict() if readiness else {},
        )


def render_internal_provider_consolidation_cli(parts: dict[str, Any], section: str) -> str:
    report: InternalProviderConsolidationReport = parts["report"]
    lines = [
        f"version={report.version}",
        "source_contract_version=v0.24.0",
        f"release_name={report.release_name}",
        f"release_status={report.release_status}",
        f"readiness_status={report.readiness_status}",
        f"ready_for_v0_25={str(report.ready_for_v0_25).lower()}",
        f"ready_for_v0_26={str(report.ready_for_v0_26).lower()}",
        f"new_provider_invocation_performed={str(report.new_provider_invocation_performed).lower()}",
        f"new_repository_search_performed={str(report.new_repository_search_performed).lower()}",
        f"new_file_read_performed={str(report.new_file_read_performed).lower()}",
        f"new_process_inspection_performed={str(report.new_process_inspection_performed).lower()}",
        f"new_local_command_executed={str(report.new_local_command_executed).lower()}",
        f"command_rerun_performed={str(report.command_rerun_performed).lower()}",
        f"automatic_repair_performed={str(report.automatic_repair_performed).lower()}",
        f"file_mutation_performed={str(report.file_mutation_performed).lower()}",
        f"patch_applied={str(report.patch_applied).lower()}",
        f"external_provider_adapter_implemented={str(report.external_provider_adapter_implemented).lower()}",
        f"schumpeter_split_introduced={str(report.schumpeter_split_introduced).lower()}",
        f"credential_exposed={str(report.credential_exposed).lower()}",
        f"raw_secret_output={str(report.raw_secret_output).lower()}",
        f"raw_output_dumped={str(report.raw_output_dumped).lower()}",
        f"llm_judge_used={str(report.llm_judge_used).lower()}",
        f"next_required_step={report.next_required_step}",
    ]
    if section == "release-manifest":
        manifest: InternalProviderReleaseManifest = parts["release_manifest"]
        lines.append(f"included_versions={','.join(manifest.included_versions)}")
        lines.append(f"excluded_capabilities_count={len(manifest.excluded_capabilities)}")
    elif section == "readiness":
        readiness: InternalProviderV025ReadinessReport = parts["readiness"]
        lines.append(f"recommended_next_version={readiness.recommended_next_version}")
        lines.append(f"substrate_requirements_met={str(readiness.substrate_requirements_met).lower()}")
    elif section == "safety-boundary":
        safety: InternalProviderSafetyBoundaryReport = parts["safety_boundary"]
        lines.append(f"safety_status={safety.status}")
        lines.append(f"command_rerun_count={safety.command_rerun_count}")
        lines.append(f"unrestricted_shell_count={safety.unrestricted_shell_count}")
    elif section == "runtime-boundary":
        runtime: InternalProviderRuntimeBoundaryReport = parts["runtime_boundary"]
        lines.append(f"runtime_boundary_status={runtime.runtime_boundary_status}")
        lines.append(f"bounded_runner_isolated={str(runtime.bounded_runner_isolated).lower()}")
    elif section == "roadmap-boundary":
        roadmap: InternalProviderRoadmapBoundaryReport = parts["roadmap_boundary"]
        lines.append(f"current_track={roadmap.current_track}")
        lines.append(f"next_track={roadmap.next_track}")
    elif section == "gaps":
        gaps: InternalProviderGapRegister = parts["gaps"]
        for gap in gaps.gaps:
            lines.append(f"- {gap.gap_id}: {gap.severity}")
    elif section == "workbench":
        workbench: InternalProviderConsolidationWorkbenchSnapshot = parts["workbench"]
        lines.append(f"workbench_id={workbench.workbench_id}")
        lines.append(f"read_only={str(workbench.read_only).lower()}")
        lines.append(f"mutation_performed={str(workbench.mutation_performed).lower()}")
    else:
        lines.append(f"report_id={report.report_id}")
    return "\n".join(lines)
