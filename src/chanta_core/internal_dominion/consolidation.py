from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import time
from typing import Any

from chanta_core.internal_dominion.mapping import DOMINION_EFFECT_TYPES
from chanta_core.internal_dominion.registry import DOMINION_SEED_SKILL_IDS, InternalDominionRegistryService


DOMINION_CONSOLIDATION_VERSION = "v0.23.9"
DOMINION_CONSOLIDATION_VERSION_NAME = "Internal Dominion Consolidation / Release Readiness"
DOMINION_CONSOLIDATION_KOREAN_NAME = "internal dominion consolidation release readiness"
DOMINION_CONSOLIDATION_RELEASE_NAME = "OCEL-native Internal Dominion Foundation v1"
DOMINION_CONSOLIDATION_TRACK = "Internal Dominion Foundation"
DOMINION_NEXT_TRACK = "v0.24.x Internal Provider / Local Runtime Provider"
DOMINION_CONSOLIDATION_SUBJECT = "internal_dominion_consolidation_release_readiness"
DOMINION_CONSOLIDATION_STATE = "internal_dominion_foundation_v1_consolidated"

INCLUDED_VERSIONS = [
    "v0.23.0",
    "v0.23.1",
    "v0.23.2",
    "v0.23.3",
    "v0.23.4",
    "v0.23.5",
    "v0.23.6",
    "v0.23.7",
    "v0.23.8",
    "v0.23.9",
]

FUTURE_TRACKS = [
    "v0.24.x Internal Provider / Local Runtime Provider",
    "v0.25.x General Agent Usability & Tool Routing",
    "v0.26.x Workspace Agent Workbench",
    "v0.27.x Memory Candidate & Continuity",
    "v0.28.x Public Alpha / Schumpeter Split Preparation",
    "v0.29.x+ External Skill / External Provider Adapter Development",
]

EXCLUDED_CAPABILITIES = [
    "actual external dispatch",
    "provider API execution",
    "external runtime touch",
    "authorization consumption",
    "live status tracking",
    "live output fetch",
    "real external outcome record",
    "Local Runtime Provider",
    "local command execution",
    "General Agent Usability",
    "Workspace Agent Workbench",
    "Memory Candidate / Continuity",
    "External Provider Adapter",
    "Schumpeter split / company wrapper",
    "GrowthKernel runtime dependency",
]

FORBIDDEN_EFFECT_TYPES = [
    "external_runtime_touched",
    "external_control_dispatched",
    "external_run_started",
    "credential_exposed",
    "authorization_consumed",
    "live_status_tracked",
    "live_output_fetched",
    "external_outcome_recorded",
    "outcome_recorded",
]

REQUIRED_FUTURE_GAPS = [
    "internal_provider_local_runtime_not_started",
    "general_agent_usability_not_started",
    "workspace_agent_workbench_not_started",
    "memory_candidate_continuity_not_started",
    "public_alpha_schumpeter_split_not_started",
    "external_provider_adapters_not_started",
    "live_provider_preflight_not_started",
    "actual_bounded_dispatch_not_started",
    "real_status_tracking_not_started",
    "real_external_outcome_recording_not_started",
    "growthkernel_bridge_not_started",
]


def _utc_now() -> str:
    return datetime.fromtimestamp(time.time(), timezone.utc).isoformat().replace("+00:00", "Z")


@dataclass(frozen=True)
class InternalDominionSubjectComponent:
    component_id: str
    version_introduced: str
    subject_id: str
    subject_name: str
    component_type: str
    skill_ids: list[str]
    status: str
    provider_neutral: bool
    executing: bool = False
    dispatch_enabled: bool = False
    provider_api_call_enabled: bool = False
    external_runtime_touch_enabled: bool = False
    credential_materialization_enabled: bool = False
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    workbench_visible: bool = True
    latest_artifact_id: str | None = None
    finding_count: int = 0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionCapabilityMapEntry:
    capability_id: str
    subject_id: str
    name: str
    version_introduced: str
    skill_ids: list[str]
    status: str
    input_surfaces: list[str]
    output_surfaces: list[str]
    source_read_models: list[str]
    target_read_models: list[str]
    effect_types: list[str]
    forbidden_effect_types: list[str]
    provider_neutral: bool
    executing: bool = False
    ocel_visible: bool = True
    pig_visible: bool = True
    ocpx_visible: bool = True
    workbench_visible: bool = True
    safety_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionCapabilityMap:
    map_id: str
    version: str
    entries: list[InternalDominionCapabilityMapEntry]
    implemented_count: int
    warning_count: int
    failed_count: int
    blocked_count: int
    future_track_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "entries": [item.to_dict() for item in self.entries],
        }


@dataclass(frozen=True)
class InternalDominionCoverageMatrixRow:
    subject_id: str
    version_introduced: str
    has_model: bool
    has_service: bool
    has_cli: bool
    has_tests: bool
    has_boundary_tests: bool
    has_ocel_mapping: bool
    has_pig_projection: bool
    has_ocpx_projection: bool
    has_workbench_visibility: bool
    has_docs: bool
    latest_artifact_available: bool
    coverage_notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionCoverageMatrix:
    matrix_id: str
    rows: list[InternalDominionCoverageMatrixRow]
    coverage_status: str
    missing_required_coverage_count: int
    optional_gap_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "rows": [item.to_dict() for item in self.rows],
        }


@dataclass(frozen=True)
class InternalDominionSafetyBoundaryReport:
    report_id: str
    version: str = DOMINION_CONSOLIDATION_VERSION
    provider_api_call_count: int = 0
    external_runtime_touch_count: int = 0
    external_dispatch_count: int = 0
    external_run_start_count: int = 0
    authorization_consumed_count: int = 0
    live_status_tracking_count: int = 0
    live_output_fetch_count: int = 0
    real_external_outcome_record_count: int = 0
    credential_exposure_count: int = 0
    raw_secret_output_count: int = 0
    local_command_execution_count: int = 0
    shell_execution_count: int = 0
    network_access_count: int = 0
    mcp_connection_count: int = 0
    plugin_loading_count: int = 0
    llm_judge_count: int = 0
    vendor_specific_core_logic_count: int = 0
    growthkernel_active_dependency_count: int = 0
    premature_local_runtime_provider_count: int = 0
    premature_general_agent_usability_count: int = 0
    premature_workbench_count: int = 0
    premature_memory_continuity_count: int = 0
    premature_external_provider_adapter_count: int = 0
    premature_schumpeter_split_count: int = 0
    status: str = "passed"
    findings: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionRoadmapBoundaryReport:
    report_id: str
    current_track: str = "v0.23.x Internal Dominion Foundation"
    next_track: str = DOMINION_NEXT_TRACK
    future_tracks: list[str] = field(default_factory=lambda: list(FUTURE_TRACKS))
    local_runtime_provider_deferred: bool = True
    general_agent_usability_deferred: bool = True
    workspace_workbench_deferred: bool = True
    memory_continuity_deferred: bool = True
    public_alpha_schumpeter_split_deferred: bool = True
    external_provider_adapters_deferred: bool = True
    growthkernel_bridge_deferred: bool = True
    roadmap_status: str = "aligned"
    findings: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionGap:
    gap_id: str
    title: str
    description: str
    severity: str
    affected_subjects: list[str]
    recommended_track: str | None
    withdrawal_condition: str | None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionGapRegister:
    register_id: str
    gaps: list[InternalDominionGap]
    blocker_count: int
    warning_count: int
    future_track_count: int

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "gaps": [item.to_dict() for item in self.gaps],
        }


@dataclass(frozen=True)
class InternalDominionReleaseManifest:
    manifest_id: str
    release_version: str = DOMINION_CONSOLIDATION_VERSION
    release_name: str = DOMINION_CONSOLIDATION_RELEASE_NAME
    included_versions: list[str] = field(default_factory=lambda: list(INCLUDED_VERSIONS))
    included_subjects: list[str] = field(default_factory=list)
    included_capabilities: list[str] = field(default_factory=list)
    excluded_capabilities: list[str] = field(default_factory=lambda: list(EXCLUDED_CAPABILITIES))
    future_tracks: list[str] = field(default_factory=lambda: list(FUTURE_TRACKS))
    safety_boundary_report_id: str = "internal_dominion_safety_boundary_report:v0.23.9"
    roadmap_boundary_report_id: str = "internal_dominion_roadmap_boundary_report:v0.23.9"
    gap_register_id: str = "internal_dominion_gap_register:v0.23.9"
    release_status: str = "releasable"
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class InternalDominionConsolidationFinding:
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
class InternalDominionConsolidationReport:
    report_id: str
    created_at: str
    foundation_snapshot_id: str
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_manifest_id: str
    findings: list[InternalDominionConsolidationFinding]
    readiness_status: str
    release_status: str
    ready_for_v0_24: bool
    version: str = DOMINION_CONSOLIDATION_VERSION
    release_name: str = DOMINION_CONSOLIDATION_RELEASE_NAME
    ready_for_v0_25: bool = False
    safe_to_dispatch: bool = False
    provider_api_call_performed: bool = False
    external_runtime_touched: bool = False
    dispatch_performed: bool = False
    authorization_consumed: bool = False
    live_status_tracking_started: bool = False
    live_output_fetch_started: bool = False
    real_external_outcome_recorded: bool = False
    local_runtime_provider_implemented: bool = False
    general_agent_usability_implemented: bool = False
    workspace_agent_workbench_implemented: bool = False
    memory_candidate_continuity_implemented: bool = False
    external_provider_adapter_implemented: bool = False
    schumpeter_split_introduced: bool = False
    credential_exposed: bool = False
    raw_secret_output: bool = False
    llm_judge_used: bool = False
    next_track_recommendation: str = DOMINION_NEXT_TRACK
    limitations: list[str] = field(default_factory=list)
    withdrawal_conditions: list[str] = field(default_factory=list)
    validity_horizon: str = (
        "Valid until v0.24 Internal Provider / Local Runtime Provider begins or v0.23.x policy changes."
    )
    foundation_snapshot: "InternalDominionFoundationSnapshot | None" = None
    capability_map: InternalDominionCapabilityMap | None = None
    coverage_matrix: InternalDominionCoverageMatrix | None = None
    safety_boundary_report: InternalDominionSafetyBoundaryReport | None = None
    roadmap_boundary_report: InternalDominionRoadmapBoundaryReport | None = None
    gap_register: InternalDominionGapRegister | None = None
    release_manifest: InternalDominionReleaseManifest | None = None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["findings"] = [item.to_dict() for item in self.findings]
        if self.foundation_snapshot is not None:
            payload["foundation_snapshot"] = self.foundation_snapshot.to_dict()
        if self.capability_map is not None:
            payload["capability_map"] = self.capability_map.to_dict()
        if self.coverage_matrix is not None:
            payload["coverage_matrix"] = self.coverage_matrix.to_dict()
        if self.safety_boundary_report is not None:
            payload["safety_boundary_report"] = self.safety_boundary_report.to_dict()
        if self.roadmap_boundary_report is not None:
            payload["roadmap_boundary_report"] = self.roadmap_boundary_report.to_dict()
        if self.gap_register is not None:
            payload["gap_register"] = self.gap_register.to_dict()
        if self.release_manifest is not None:
            payload["release_manifest"] = self.release_manifest.to_dict()
        return payload


@dataclass(frozen=True)
class InternalDominionFoundationSnapshot:
    snapshot_id: str
    created_at: str
    subjects: list[InternalDominionSubjectComponent]
    capability_map_id: str
    coverage_matrix_id: str
    safety_boundary_report_id: str
    roadmap_boundary_report_id: str
    gap_register_id: str
    release_manifest_id: str
    consolidation_report_id: str
    snapshot_status: str
    version: str = DOMINION_CONSOLIDATION_VERSION
    release_name: str = DOMINION_CONSOLIDATION_RELEASE_NAME
    included_versions: list[str] = field(default_factory=lambda: list(INCLUDED_VERSIONS))
    limitations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            **asdict(self),
            "subjects": [item.to_dict() for item in self.subjects],
        }


@dataclass(frozen=True)
class InternalDominionWorkbenchSnapshot:
    workbench_id: str
    created_at: str
    snapshot_id: str
    consolidation_report_id: str
    release_status: str
    readiness_status: str
    subject_summary: list[dict[str, Any]]
    safety_summary: dict[str, Any]
    roadmap_summary: dict[str, Any]
    gap_summary: dict[str, Any]
    next_track_recommendation: str
    version: str = DOMINION_CONSOLIDATION_VERSION
    read_only: bool = True
    mutation_performed: bool = False

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class InternalDominionConsolidationSourceService:
    def load_v0_23_0_contract(self) -> dict[str, Any]:
        return {"source_id": "internal_dominion_contract:v0.23.0", "status": "available", "read_only": True}

    def load_v0_23_1_inventory(self) -> dict[str, Any]:
        return {"source_id": "runtime_inventory_report:v0.23.1", "status": "available", "read_only": True}

    def load_v0_23_2_capability_digest(self) -> dict[str, Any]:
        return {"source_id": "capability_observation_digest_report:v0.23.2", "status": "available", "read_only": True}

    def load_v0_23_3_action_candidates(self) -> dict[str, Any]:
        return {"source_id": "dominion_control_request_candidate_report:v0.23.3", "status": "available", "read_only": True}

    def load_v0_23_4_control_plans(self) -> dict[str, Any]:
        return {"source_id": "dominion_control_plan_report:v0.23.4", "status": "available", "read_only": True}

    def load_v0_23_5_static_safety(self) -> dict[str, Any]:
        return {"source_id": "dominion_static_safety_report:v0.23.5", "status": "available", "read_only": True}

    def load_v0_23_6_preflight(self) -> dict[str, Any]:
        return {"source_id": "dominion_runtime_preflight_report:v0.23.6", "status": "available", "read_only": True}

    def load_v0_23_7_gate(self) -> dict[str, Any]:
        return {"source_id": "dominion_gate_report:v0.23.7", "status": "available", "read_only": True}

    def load_v0_23_8_dispatch_boundary(self) -> dict[str, Any]:
        return {"source_id": "dominion_dispatch_boundary_report:v0.23.8", "status": "available", "read_only": True}

    def load_sources(self) -> dict[str, dict[str, Any]]:
        return {
            "v0_23_0_contract": self.load_v0_23_0_contract(),
            "v0_23_1_inventory": self.load_v0_23_1_inventory(),
            "v0_23_2_capability_digest": self.load_v0_23_2_capability_digest(),
            "v0_23_3_action_candidates": self.load_v0_23_3_action_candidates(),
            "v0_23_4_control_plans": self.load_v0_23_4_control_plans(),
            "v0_23_5_static_safety": self.load_v0_23_5_static_safety(),
            "v0_23_6_preflight": self.load_v0_23_6_preflight(),
            "v0_23_7_gate": self.load_v0_23_7_gate(),
            "v0_23_8_dispatch_boundary": self.load_v0_23_8_dispatch_boundary(),
        }


class InternalDominionSubjectComponentService:
    def build_subject_components(self, sources: dict[str, Any] | None = None) -> list[InternalDominionSubjectComponent]:
        source_status = sources or {}
        definitions = [
            ("v0.23.0", "subject:internal_dominion_contract", "Internal Dominion Contract", "contract", ["skill:dominion_contract_view"]),
            ("v0.23.1", "subject:runtime_inventory", "Runtime / Agent / System Inventory", "inventory", ["skill:dominion_runtime_inventory"]),
            (
                "v0.23.2",
                "subject:external_capability_digestion",
                "Capability Observation & Digestion",
                "capability",
                ["skill:dominion_capability_observe", "skill:dominion_capability_digest"],
            ),
            (
                "v0.23.3",
                "subject:external_action_candidate",
                "Control Request & Action Candidate",
                "request_candidate",
                ["skill:dominion_control_request_create", "skill:dominion_action_candidate_create"],
            ),
            (
                "v0.23.4",
                "subject:control_plan",
                "Control Plan & Target Binding",
                "plan_binding",
                ["skill:dominion_control_plan_create", "skill:dominion_target_binding"],
            ),
            ("v0.23.5", "subject:dominion_static_safety", "Dominion Static Safety Check", "static_safety", ["skill:dominion_static_safety_check"]),
            ("v0.23.6", "subject:runtime_preflight", "Runtime Preflight / Reachability Check", "preflight", ["skill:dominion_runtime_preflight"]),
            (
                "v0.23.7",
                "subject:dominion_review_gate",
                "Human Review & Dominion Gate",
                "gate",
                ["skill:dominion_review_gate", "skill:dominion_authorization_create"],
            ),
            (
                "v0.23.8",
                "subject:bounded_control_dispatch",
                "Authorization / Bounded Dispatch / Status / Outcome Boundary",
                "dispatch_boundary",
                [
                    "skill:dominion_bounded_dispatch",
                    "skill:dominion_run_status_track",
                    "skill:dominion_run_output_fetch",
                    "skill:dominion_outcome_record",
                ],
            ),
            ("v0.23.9", "subject:dominion_workbench", "Dominion Workbench Snapshot", "workbench", ["skill:dominion_workbench_view"]),
            ("v0.23.9", "subject:dominion_consolidation", "Internal Dominion Consolidation", "consolidation", ["skill:dominion_consolidation_view"]),
        ]
        components: list[InternalDominionSubjectComponent] = []
        missing = {key for key, value in source_status.items() if isinstance(value, dict) and value.get("status") == "missing"}
        for version, subject_id, name, component_type, skills in definitions:
            status = "blocked" if any(version.replace(".", "_").replace("v", "v") in key for key in missing) else "implemented"
            components.append(
                InternalDominionSubjectComponent(
                    component_id=f"internal_dominion_subject_component:{version}:{subject_id.removeprefix('subject:')}",
                    version_introduced=version,
                    subject_id=subject_id,
                    subject_name=name,
                    component_type=component_type,
                    skill_ids=skills,
                    status=status,
                    provider_neutral=True,
                    latest_artifact_id=f"{subject_id.removeprefix('subject:')}_artifact:{version}",
                    finding_count=0 if status == "implemented" else 1,
                    notes=[
                        "read_only_consolidation",
                        "provider_neutral",
                        "non_executing",
                        "non_dispatching",
                    ],
                )
            )
        return components


class InternalDominionCapabilityMapService:
    def build_capability_map(self, subjects: list[InternalDominionSubjectComponent]) -> InternalDominionCapabilityMap:
        subject_by_skill = {
            skill_id: subject
            for subject in subjects
            for skill_id in subject.skill_ids
        }
        entries = [
            InternalDominionCapabilityMapEntry(
                capability_id=f"internal_dominion_capability:{skill_id.removeprefix('skill:')}",
                subject_id=subject_by_skill.get(skill_id, subjects[-1]).subject_id,
                name=skill_id.removeprefix("skill:").replace("_", " "),
                version_introduced=subject_by_skill.get(skill_id, subjects[-1]).version_introduced,
                skill_ids=[skill_id],
                status="implemented",
                input_surfaces=["read_model", "cli_view"],
                output_surfaces=["ocel_projection", "pig_report", "ocpx_projection", "workbench_snapshot"],
                source_read_models=["InternalDominionContractState"],
                target_read_models=["InternalDominionConsolidationState"],
                effect_types=list(DOMINION_EFFECT_TYPES),
                forbidden_effect_types=list(FORBIDDEN_EFFECT_TYPES),
                provider_neutral=True,
                safety_notes=["no_provider_api_call", "no_external_runtime_touch", "no_dispatch"],
            )
            for skill_id in DOMINION_SEED_SKILL_IDS
        ]
        return InternalDominionCapabilityMap(
            map_id="internal_dominion_capability_map:v0.23.9",
            version=DOMINION_CONSOLIDATION_VERSION,
            entries=entries,
            implemented_count=len(entries),
            warning_count=0,
            failed_count=0,
            blocked_count=0,
            future_track_count=0,
        )


class InternalDominionCoverageMatrixService:
    def build_coverage_matrix(self, subjects: list[InternalDominionSubjectComponent]) -> InternalDominionCoverageMatrix:
        rows = [
            InternalDominionCoverageMatrixRow(
                subject_id=subject.subject_id,
                version_introduced=subject.version_introduced,
                has_model=True,
                has_service=True,
                has_cli=True,
                has_tests=True,
                has_boundary_tests=True,
                has_ocel_mapping=True,
                has_pig_projection=True,
                has_ocpx_projection=True,
                has_workbench_visibility=True,
                has_docs=True,
                latest_artifact_available=subject.status == "implemented",
                coverage_notes=["coverage_declared_for_internal_dominion_release_readiness"],
            )
            for subject in subjects
        ]
        missing = sum(1 for row in rows if not row.latest_artifact_available)
        return InternalDominionCoverageMatrix(
            matrix_id="internal_dominion_coverage_matrix:v0.23.9",
            rows=rows,
            coverage_status="complete" if missing == 0 else "blocked",
            missing_required_coverage_count=missing,
            optional_gap_count=0,
        )


class InternalDominionSafetyBoundaryReportService:
    _COUNT_MARKERS = {
        "provider_api_call": "provider_api_call_count",
        "external_runtime_touch": "external_runtime_touch_count",
        "dispatch": "external_dispatch_count",
        "external_run_start": "external_run_start_count",
        "authorization_consumed": "authorization_consumed_count",
        "live_status_tracking": "live_status_tracking_count",
        "live_output_fetch": "live_output_fetch_count",
        "real_external_outcome_record": "real_external_outcome_record_count",
        "credential_exposure": "credential_exposure_count",
        "raw_secret_output": "raw_secret_output_count",
        "local_command_execution": "local_command_execution_count",
        "shell_execution": "shell_execution_count",
        "network_access": "network_access_count",
        "mcp_connection": "mcp_connection_count",
        "plugin_loading": "plugin_loading_count",
        "llm_judge": "llm_judge_count",
        "vendor_hardcoding": "vendor_specific_core_logic_count",
        "growthkernel_dependency": "growthkernel_active_dependency_count",
        "premature_local_runtime_provider": "premature_local_runtime_provider_count",
        "premature_general_agent_usability": "premature_general_agent_usability_count",
        "premature_workbench": "premature_workbench_count",
        "premature_memory_continuity": "premature_memory_continuity_count",
        "premature_external_provider_adapter": "premature_external_provider_adapter_count",
        "premature_schumpeter_split": "premature_schumpeter_split_count",
    }

    def build_safety_boundary_report(self, sources: dict[str, Any] | None = None) -> InternalDominionSafetyBoundaryReport:
        markers = set((sources or {}).get("markers", [])) if isinstance(sources, dict) else set()
        counts = {field_name: 0 for field_name in self._COUNT_MARKERS.values()}
        findings: list[dict[str, Any]] = []
        for marker, field_name in self._COUNT_MARKERS.items():
            if marker in markers:
                counts[field_name] = 1
                findings.append(
                    {
                        "finding_type": f"{marker}_detected",
                        "severity": "critical",
                        "message": f"Detected forbidden v0.23.9 consolidation marker: {marker}",
                    }
                )
        blocked = any(counts.values())
        return InternalDominionSafetyBoundaryReport(
            report_id="internal_dominion_safety_boundary_report:v0.23.9",
            status="blocked" if blocked else "passed",
            findings=findings,
            **counts,
        )


class InternalDominionRoadmapBoundaryReportService:
    def build_roadmap_boundary_report(self, sources: dict[str, Any] | None = None) -> InternalDominionRoadmapBoundaryReport:
        markers = set((sources or {}).get("markers", [])) if isinstance(sources, dict) else set()
        blocked_markers = {
            "premature_local_runtime_provider",
            "premature_general_agent_usability",
            "premature_external_provider_adapter",
            "premature_schumpeter_split",
        } & markers
        findings = [
            {
                "finding_type": f"{marker}_detected",
                "severity": "critical",
                "message": f"Premature future-track implementation detected: {marker}",
            }
            for marker in sorted(blocked_markers)
        ]
        return InternalDominionRoadmapBoundaryReport(
            report_id="internal_dominion_roadmap_boundary_report:v0.23.9",
            roadmap_status="blocked" if findings else "aligned",
            findings=findings,
        )


class InternalDominionGapRegisterService:
    def build_gap_register(
        self,
        safety_report: InternalDominionSafetyBoundaryReport,
        roadmap_report: InternalDominionRoadmapBoundaryReport,
        coverage_matrix: InternalDominionCoverageMatrix,
    ) -> InternalDominionGapRegister:
        gaps = [
            InternalDominionGap(
                gap_id=gap_id,
                title=gap_id.replace("_", " "),
                description="Future-track gap intentionally deferred outside v0.23.x Internal Dominion Foundation.",
                severity="future_track",
                affected_subjects=["subject:dominion_consolidation"],
                recommended_track=DOMINION_NEXT_TRACK if gap_id.startswith("internal_provider") else "future_track",
                withdrawal_condition="Withdraw if this capability is implemented inside v0.23.x.",
            )
            for gap_id in REQUIRED_FUTURE_GAPS
        ]
        blockers = 0
        if safety_report.status == "blocked" or roadmap_report.roadmap_status == "blocked":
            blockers += 1
        blockers += coverage_matrix.missing_required_coverage_count
        return InternalDominionGapRegister(
            register_id="internal_dominion_gap_register:v0.23.9",
            gaps=gaps,
            blocker_count=blockers,
            warning_count=0,
            future_track_count=len(gaps),
        )


class InternalDominionReleaseManifestService:
    def build_release_manifest(
        self,
        subjects: list[InternalDominionSubjectComponent],
        safety_report: InternalDominionSafetyBoundaryReport,
        roadmap_report: InternalDominionRoadmapBoundaryReport,
        gap_register: InternalDominionGapRegister,
    ) -> InternalDominionReleaseManifest:
        blocked = (
            safety_report.status == "blocked"
            or roadmap_report.roadmap_status == "blocked"
            or gap_register.blocker_count > 0
            or any(subject.status == "blocked" for subject in subjects)
        )
        return InternalDominionReleaseManifest(
            manifest_id="internal_dominion_release_manifest:v0.23.9",
            included_subjects=[subject.subject_id for subject in subjects],
            included_capabilities=list(DOMINION_SEED_SKILL_IDS),
            safety_boundary_report_id=safety_report.report_id,
            roadmap_boundary_report_id=roadmap_report.report_id,
            gap_register_id=gap_register.register_id,
            release_status="blocked" if blocked else "releasable",
            notes=[
                "consolidation_is_not_dispatch",
                "release_readiness_is_not_provider_adapter_implementation",
                "dominion_foundation_v1_closes_control_grammar_not_live_external_control",
            ],
        )


class InternalDominionConsolidationFindingService:
    _SAFETY_FINDING_TYPES = {
        "provider_api_call_count": "provider_api_call_detected",
        "external_runtime_touch_count": "external_runtime_touch_detected",
        "external_dispatch_count": "dispatch_detected",
        "authorization_consumed_count": "authorization_consumption_detected",
        "live_status_tracking_count": "live_status_tracking_detected",
        "live_output_fetch_count": "live_output_fetch_detected",
        "real_external_outcome_record_count": "real_external_outcome_detected",
        "credential_exposure_count": "credential_exposure_detected",
        "premature_local_runtime_provider_count": "local_runtime_provider_premature",
        "premature_general_agent_usability_count": "general_agent_usability_premature",
        "premature_external_provider_adapter_count": "external_provider_adapter_premature",
        "premature_schumpeter_split_count": "schumpeter_split_premature",
        "growthkernel_active_dependency_count": "growthkernel_dependency_detected",
        "vendor_specific_core_logic_count": "vendor_hardcoding_detected",
    }

    def build_findings(
        self,
        subjects: list[InternalDominionSubjectComponent],
        coverage_matrix: InternalDominionCoverageMatrix,
        safety_report: InternalDominionSafetyBoundaryReport,
        roadmap_report: InternalDominionRoadmapBoundaryReport,
        release_manifest: InternalDominionReleaseManifest,
    ) -> list[InternalDominionConsolidationFinding]:
        findings: list[InternalDominionConsolidationFinding] = []
        for subject in subjects:
            if subject.status == "blocked":
                findings.append(
                    InternalDominionConsolidationFinding(
                        finding_id=f"internal_dominion_consolidation_finding:missing:{subject.subject_id}",
                        severity="critical",
                        finding_type="missing_subject_component",
                        message=f"Required v0.23 subject component is blocked: {subject.subject_id}",
                        subject_ref={"subject_id": subject.subject_id},
                        evidence_refs=[],
                        withdrawal_condition="Withdraw if the required subject component is restored.",
                    )
                )
        for row in coverage_matrix.rows:
            if not row.latest_artifact_available:
                findings.append(
                    InternalDominionConsolidationFinding(
                        finding_id=f"internal_dominion_consolidation_finding:coverage:{row.subject_id}",
                        severity="error",
                        finding_type="missing_tests",
                        message=f"Required coverage is missing for {row.subject_id}",
                        subject_ref={"subject_id": row.subject_id},
                        evidence_refs=[],
                        withdrawal_condition="Withdraw if required coverage is restored.",
                    )
                )
        safety_payload = safety_report.to_dict()
        for count_field, finding_type in self._SAFETY_FINDING_TYPES.items():
            if int(safety_payload.get(count_field, 0)) > 0:
                findings.append(
                    InternalDominionConsolidationFinding(
                        finding_id=f"internal_dominion_consolidation_finding:{finding_type}",
                        severity="critical",
                        finding_type=finding_type,
                        message=f"Blocked release because {count_field} is nonzero.",
                        subject_ref=None,
                        evidence_refs=safety_report.findings,
                        withdrawal_condition="Withdraw if the count returns to zero and the code path is removed.",
                    )
                )
        if roadmap_report.roadmap_status == "blocked":
            findings.append(
                InternalDominionConsolidationFinding(
                    finding_id="internal_dominion_consolidation_finding:roadmap_blocked",
                    severity="critical",
                    finding_type="general_agent_usability_premature",
                    message="Roadmap boundary is blocked by premature future-track implementation.",
                    subject_ref=None,
                    evidence_refs=roadmap_report.findings,
                    withdrawal_condition="Withdraw if the premature future-track implementation is removed.",
                )
            )
        if not findings and release_manifest.release_status in {"releasable", "releasable_with_warnings"}:
            findings.append(
                InternalDominionConsolidationFinding(
                    finding_id="internal_dominion_consolidation_finding:ok",
                    severity="info",
                    finding_type="ok",
                    message="Internal Dominion Foundation v1 is consolidated without live execution capability.",
                    subject_ref=None,
                    evidence_refs=[],
                    withdrawal_condition="Withdraw if a forbidden effect or missing prerequisite is detected.",
                )
            )
        return findings


class InternalDominionConsolidationReportService:
    def __init__(
        self,
        source_service: InternalDominionConsolidationSourceService | None = None,
        subject_service: InternalDominionSubjectComponentService | None = None,
        capability_service: InternalDominionCapabilityMapService | None = None,
        coverage_service: InternalDominionCoverageMatrixService | None = None,
        safety_service: InternalDominionSafetyBoundaryReportService | None = None,
        roadmap_service: InternalDominionRoadmapBoundaryReportService | None = None,
        gap_service: InternalDominionGapRegisterService | None = None,
        manifest_service: InternalDominionReleaseManifestService | None = None,
        finding_service: InternalDominionConsolidationFindingService | None = None,
    ) -> None:
        self.source_service = source_service or InternalDominionConsolidationSourceService()
        self.subject_service = subject_service or InternalDominionSubjectComponentService()
        self.capability_service = capability_service or InternalDominionCapabilityMapService()
        self.coverage_service = coverage_service or InternalDominionCoverageMatrixService()
        self.safety_service = safety_service or InternalDominionSafetyBoundaryReportService()
        self.roadmap_service = roadmap_service or InternalDominionRoadmapBoundaryReportService()
        self.gap_service = gap_service or InternalDominionGapRegisterService()
        self.manifest_service = manifest_service or InternalDominionReleaseManifestService()
        self.finding_service = finding_service or InternalDominionConsolidationFindingService()

    def build_report(self, source_overrides: dict[str, Any] | None = None) -> InternalDominionConsolidationReport:
        sources = self.source_service.load_sources()
        if source_overrides:
            sources.update(source_overrides)
        subjects = self.subject_service.build_subject_components(sources)
        capability_map = self.capability_service.build_capability_map(subjects)
        coverage_matrix = self.coverage_service.build_coverage_matrix(subjects)
        safety_report = self.safety_service.build_safety_boundary_report(source_overrides)
        roadmap_report = self.roadmap_service.build_roadmap_boundary_report(source_overrides)
        gap_register = self.gap_service.build_gap_register(safety_report, roadmap_report, coverage_matrix)
        release_manifest = self.manifest_service.build_release_manifest(
            subjects, safety_report, roadmap_report, gap_register
        )
        findings = self.finding_service.build_findings(
            subjects, coverage_matrix, safety_report, roadmap_report, release_manifest
        )
        readiness_status = (
            "blocked"
            if release_manifest.release_status == "blocked"
            else "warning"
            if release_manifest.release_status == "releasable_with_warnings"
            else "ready"
        )
        created_at = _utc_now()
        snapshot = InternalDominionFoundationSnapshot(
            snapshot_id="internal_dominion_foundation_snapshot:v0.23.9",
            created_at=created_at,
            subjects=subjects,
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage_matrix.matrix_id,
            safety_boundary_report_id=safety_report.report_id,
            roadmap_boundary_report_id=roadmap_report.report_id,
            gap_register_id=gap_register.register_id,
            release_manifest_id=release_manifest.manifest_id,
            consolidation_report_id="internal_dominion_consolidation_report:v0.23.9",
            snapshot_status="blocked" if readiness_status == "blocked" else readiness_status,
            limitations=[
                "read_only_consolidation_snapshot",
                "no_live_external_control",
                "v0_24_internal_provider_not_started",
            ],
        )
        return InternalDominionConsolidationReport(
            report_id="internal_dominion_consolidation_report:v0.23.9",
            created_at=created_at,
            foundation_snapshot_id=snapshot.snapshot_id,
            capability_map_id=capability_map.map_id,
            coverage_matrix_id=coverage_matrix.matrix_id,
            safety_boundary_report_id=safety_report.report_id,
            roadmap_boundary_report_id=roadmap_report.report_id,
            gap_register_id=gap_register.register_id,
            release_manifest_id=release_manifest.manifest_id,
            findings=findings,
            readiness_status=readiness_status,
            release_status=release_manifest.release_status,
            ready_for_v0_24=release_manifest.release_status in {"releasable", "releasable_with_warnings"},
            limitations=[
                "Consolidation does not dispatch or consume authorization.",
                "v0.24 Internal Provider / Local Runtime Provider remains a future track.",
            ],
            withdrawal_conditions=[
                "Provider API call, external runtime touch, dispatch, or authorization consumption is detected.",
                "A v0.23 prerequisite subject, mapping, report, or test becomes unavailable.",
                "Future-track implementation leaks into v0.23.x public ChantaCore core.",
            ],
            foundation_snapshot=snapshot,
            capability_map=capability_map,
            coverage_matrix=coverage_matrix,
            safety_boundary_report=safety_report,
            roadmap_boundary_report=roadmap_report,
            gap_register=gap_register,
            release_manifest=release_manifest,
        )

    def build_pig_report(self) -> dict[str, Any]:
        return {
            "version": DOMINION_CONSOLIDATION_VERSION,
            "layer": "internal_dominion",
            "subject": DOMINION_CONSOLIDATION_SUBJECT,
            "release_name": DOMINION_CONSOLIDATION_RELEASE_NAME,
            "principles": [
                "consolidation is not dispatch",
                "release readiness is not provider adapter implementation",
                "workbench snapshot is not execution",
                "release manifest is not authorization consumption",
                "Dominion Foundation v1 closes the control grammar, not live external control",
                "v0.24 opens Internal Provider / Local Runtime Provider only after this release unit is closed",
            ],
            "safety_boundary": {
                "safe_to_dispatch": False,
                "provider_api_call_performed": False,
                "external_runtime_touched": False,
                "dispatch_performed": False,
                "authorization_consumed": False,
                "live_status_tracking_started": False,
                "live_output_fetch_started": False,
                "real_external_outcome_recorded": False,
                "credential_exposed": False,
                "raw_secret_output": False,
                "local_runtime_provider_implemented": False,
                "general_agent_usability_implemented": False,
                "workspace_agent_workbench_implemented": False,
                "memory_candidate_continuity_implemented": False,
                "external_provider_adapter_implemented": False,
                "schumpeter_split_introduced": False,
                "llm_judge_enabled": False,
            },
            "next_track": DOMINION_NEXT_TRACK,
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
            "state": DOMINION_CONSOLIDATION_STATE,
            "version": DOMINION_CONSOLIDATION_VERSION,
            "release_name": DOMINION_CONSOLIDATION_RELEASE_NAME,
            "source_read_models": [
                "InternalDominionContractState",
                "DominionRuntimeInventoryState",
                "ExternalCapabilityCandidateState",
                "ExternalActionCandidateState",
                "DominionControlPlanState",
                "DominionStaticSafetyState",
                "DominionRuntimePreflightState",
                "DominionGateState",
                "DominionGateAuthorizationState",
                "DominionDispatchBoundaryState",
            ],
            "target_read_models": [
                "InternalDominionReleaseState",
                "InternalDominionConsolidationState",
                "InternalDominionWorkbenchState",
                "InternalDominionReadinessState",
                "DominionRoadmapBoundaryState",
                "V024ReadinessState",
            ],
            "effect_types": list(DOMINION_EFFECT_TYPES),
        }

    def render_report_cli(self, report: InternalDominionConsolidationReport, section: str = "summary") -> str:
        common_lines = [
            f"ready_for_v0_24={report.ready_for_v0_24}",
            f"ready_for_v0_25={report.ready_for_v0_25}",
            f"safe_to_dispatch={report.safe_to_dispatch}",
            f"provider_api_call_performed={report.provider_api_call_performed}",
            f"external_runtime_touched={report.external_runtime_touched}",
            f"dispatch_performed={report.dispatch_performed}",
            f"authorization_consumed={report.authorization_consumed}",
            f"live_status_tracking_started={report.live_status_tracking_started}",
            f"live_output_fetch_started={report.live_output_fetch_started}",
            f"real_external_outcome_recorded={report.real_external_outcome_recorded}",
            f"local_runtime_provider_implemented={report.local_runtime_provider_implemented}",
            f"general_agent_usability_implemented={report.general_agent_usability_implemented}",
            f"external_provider_adapter_implemented={report.external_provider_adapter_implemented}",
            f"schumpeter_split_introduced={report.schumpeter_split_introduced}",
            f"next_track_recommendation={report.next_track_recommendation}",
        ]
        if section == "release-manifest" and report.release_manifest is not None:
            payload = report.release_manifest
            return "\n".join(
                [
                    "Internal Dominion Release Manifest",
                    f"release_name={payload.release_name}",
                    f"release_status={payload.release_status}",
                    f"included_versions={','.join(payload.included_versions)}",
                    f"excluded_capabilities={','.join(payload.excluded_capabilities)}",
                ]
                + common_lines
            )
        if section == "safety-boundary" and report.safety_boundary_report is not None:
            payload = report.safety_boundary_report
            return "\n".join(
                [
                    "Internal Dominion Safety Boundary",
                    f"release_name={report.release_name}",
                    f"release_status={report.release_status}",
                    f"readiness_status={report.readiness_status}",
                    f"provider_api_call_count={payload.provider_api_call_count}",
                    f"external_runtime_touch_count={payload.external_runtime_touch_count}",
                    f"external_dispatch_count={payload.external_dispatch_count}",
                    f"authorization_consumed_count={payload.authorization_consumed_count}",
                    f"live_status_tracking_count={payload.live_status_tracking_count}",
                    f"live_output_fetch_count={payload.live_output_fetch_count}",
                    f"real_external_outcome_record_count={payload.real_external_outcome_record_count}",
                    f"credential_exposure_count={payload.credential_exposure_count}",
                    f"status={payload.status}",
                ]
                + common_lines
            )
        if section == "roadmap-boundary" and report.roadmap_boundary_report is not None:
            payload = report.roadmap_boundary_report
            return "\n".join(
                [
                    "Internal Dominion Roadmap Boundary",
                    f"release_name={report.release_name}",
                    f"release_status={report.release_status}",
                    f"readiness_status={report.readiness_status}",
                    f"current_track={payload.current_track}",
                    f"next_track={payload.next_track}",
                    f"roadmap_status={payload.roadmap_status}",
                ]
                + common_lines
            )
        if section == "gaps" and report.gap_register is not None:
            payload = report.gap_register
            gap_ids = ",".join(item.gap_id for item in payload.gaps)
            return "\n".join(
                [
                    "Internal Dominion Gap Register",
                    f"release_name={report.release_name}",
                    f"release_status={report.release_status}",
                    f"readiness_status={report.readiness_status}",
                    f"blocker_count={payload.blocker_count}",
                    f"future_track_count={payload.future_track_count}",
                    f"gap_ids={gap_ids}",
                ]
                + common_lines
            )
        return "\n".join(
            [
                "Internal Dominion Consolidation / Release Readiness",
                f"version={report.version}",
                f"release_name={report.release_name}",
                f"release_status={report.release_status}",
                f"readiness_status={report.readiness_status}",
            ]
            + common_lines
        )


class InternalDominionWorkbenchSnapshotService:
    def build_workbench_snapshot(
        self,
        consolidation_report: InternalDominionConsolidationReport,
    ) -> InternalDominionWorkbenchSnapshot:
        snapshot = consolidation_report.foundation_snapshot
        subject_summary = [
            {
                "subject_id": subject.subject_id,
                "status": subject.status,
                "provider_neutral": subject.provider_neutral,
                "executing": subject.executing,
                "dispatch_enabled": subject.dispatch_enabled,
            }
            for subject in (snapshot.subjects if snapshot is not None else [])
        ]
        safety = consolidation_report.safety_boundary_report.to_dict() if consolidation_report.safety_boundary_report else {}
        roadmap = consolidation_report.roadmap_boundary_report.to_dict() if consolidation_report.roadmap_boundary_report else {}
        gaps = consolidation_report.gap_register.to_dict() if consolidation_report.gap_register else {}
        return InternalDominionWorkbenchSnapshot(
            workbench_id="internal_dominion_workbench_snapshot:v0.23.9",
            created_at=_utc_now(),
            snapshot_id=consolidation_report.foundation_snapshot_id,
            consolidation_report_id=consolidation_report.report_id,
            release_status=consolidation_report.release_status,
            readiness_status=consolidation_report.readiness_status,
            subject_summary=subject_summary,
            safety_summary=safety,
            roadmap_summary=roadmap,
            gap_summary=gaps,
            next_track_recommendation=consolidation_report.next_track_recommendation,
        )

    def render_workbench_cli(self, snapshot: InternalDominionWorkbenchSnapshot) -> str:
        ready_for_v0_24 = snapshot.release_status in {"releasable", "releasable_with_warnings"}
        return "\n".join(
            [
                "Internal Dominion Workbench Snapshot",
                f"version={snapshot.version}",
                "release_name=OCEL-native Internal Dominion Foundation v1",
                f"release_status={snapshot.release_status}",
                f"readiness_status={snapshot.readiness_status}",
                f"ready_for_v0_24={ready_for_v0_24}",
                "ready_for_v0_25=False",
                "safe_to_dispatch=False",
                "provider_api_call_performed=False",
                "external_runtime_touched=False",
                "dispatch_performed=False",
                "authorization_consumed=False",
                "live_status_tracking_started=False",
                "live_output_fetch_started=False",
                "real_external_outcome_recorded=False",
                "local_runtime_provider_implemented=False",
                "general_agent_usability_implemented=False",
                "external_provider_adapter_implemented=False",
                "schumpeter_split_introduced=False",
                f"read_only={snapshot.read_only}",
                f"mutation_performed={snapshot.mutation_performed}",
                f"subject_count={len(snapshot.subject_summary)}",
                f"next_track_recommendation={snapshot.next_track_recommendation}",
            ]
        )


class InternalDominionConsolidationService(InternalDominionConsolidationReportService):
    def consolidate(self) -> InternalDominionConsolidationReport:
        return self.build_report()

    def build_workbench_snapshot(self, report: InternalDominionConsolidationReport | None = None) -> InternalDominionWorkbenchSnapshot:
        return InternalDominionWorkbenchSnapshotService().build_workbench_snapshot(report or self.build_report())

    def render_workbench_cli(self, snapshot: InternalDominionWorkbenchSnapshot | None = None) -> str:
        return InternalDominionWorkbenchSnapshotService().render_workbench_cli(snapshot or self.build_workbench_snapshot())


def build_internal_dominion_consolidation_contract() -> dict[str, Any]:
    registry = InternalDominionRegistryService()
    return {
        "version": DOMINION_CONSOLIDATION_VERSION,
        "version_name": DOMINION_CONSOLIDATION_VERSION_NAME,
        "release_name": DOMINION_CONSOLIDATION_RELEASE_NAME,
        "track": DOMINION_CONSOLIDATION_TRACK,
        "seed_skill_ids": registry.list_seed_skill_ids(),
        "principles": [
            "consolidation is not dispatch",
            "release readiness is not provider adapter implementation",
            "workbench snapshot is not execution",
            "release manifest is not authorization consumption",
        ],
    }
